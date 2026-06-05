#!/usr/bin/env python3
"""Фаза 4 — Проверка согласованности данных.

Для каждой ключевой сущности (CareMate, NeuroOS, ...) собирает:
- уникальные бюджеты
- уникальные сроки
- уникальные MRR-цели

Если для одной сущности встречается несовместимый набор значений —
выводит конфликт. Допускаем диапазоны (€100-150K совпадает с €150K).
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from collections import defaultdict

AUDIT = Path(__file__).resolve().parents[1]
REPORTS = AUDIT / "reports"
QUEUES = AUDIT / "queues"


def normalize_budget(b: str) -> tuple[int, int] | None:
    """€100-150K → (100000, 150000). €30K → (30000, 30000). None при разборе."""
    s = b.replace(" ", "").replace(",", "").replace(".", "")
    s = s.replace("–", "-").replace("К", "K").replace("k", "K").replace("М", "M").replace("m", "M")
    m = re.match(r"(\d+)(?:-(\d+))?([KM])?$", s)
    if not m:
        return None
    lo = int(m.group(1))
    hi = int(m.group(2)) if m.group(2) else lo
    mult = {"K": 1000, "M": 1_000_000}.get(m.group(3), 1)
    return (lo * mult, hi * mult)


def ranges_overlap(a: tuple[int, int], b: tuple[int, int]) -> bool:
    return a[0] <= b[1] and b[0] <= a[1]


def normalize_timeline(t: str) -> tuple[int, int] | None:
    s = t.replace("–", "-")
    m = re.match(r"(\d+)(?:-(\d+))?$", s)
    if not m:
        return None
    lo = int(m.group(1))
    hi = int(m.group(2)) if m.group(2) else lo
    return (lo, hi)


def analyze(entity: str, entries: list[dict]) -> dict:
    budgets_raw: list[tuple[str, str]] = []
    timelines_raw: list[tuple[str, str]] = []
    mrr_raw: list[tuple[str, str]] = []
    for e in entries:
        for b in e.get("budgets", []):
            budgets_raw.append((b, e["file"]))
        for t in e.get("timelines_mes", []):
            timelines_raw.append((t, e["file"]))
        for m in e.get("mrr", []):
            mrr_raw.append((m, e["file"]))

    # Уникальные «отпечатки» с примерами файлов
    def cluster(items: list[tuple[str, str]], normer) -> tuple[list[dict], list[dict]]:
        clusters: dict[tuple[int, int], dict] = {}
        unrecognized = []
        for raw, file in items:
            norm = normer(raw)
            if norm is None:
                unrecognized.append({"value": raw, "file": file})
                continue
            # ищем совместимый кластер
            placed = False
            for key in list(clusters.keys()):
                if ranges_overlap(key, norm):
                    # расширяем кластер
                    new_key = (min(key[0], norm[0]), max(key[1], norm[1]))
                    c = clusters.pop(key)
                    c["files"].append(file)
                    c["raw"].append(raw)
                    clusters[new_key] = c
                    placed = True
                    break
            if not placed:
                clusters[norm] = {"range": list(norm), "files": [file], "raw": [raw]}
        return list(clusters.values()), unrecognized

    budget_clusters, budget_unrec = cluster(budgets_raw, normalize_budget)
    timeline_clusters, _ = cluster(timelines_raw, normalize_timeline)
    mrr_clusters, _ = cluster(mrr_raw, normalize_budget)

    # Конфликт: больше одного несовместимого кластера
    conflicts = []
    if len(budget_clusters) > 1:
        # отсортируем по размеру
        budget_clusters.sort(key=lambda c: c["range"][0])
        conflicts.append({
            "field": "budget",
            "clusters": budget_clusters,
        })
    if len(timeline_clusters) > 1:
        timeline_clusters.sort(key=lambda c: c["range"][0])
        conflicts.append({
            "field": "timeline_months",
            "clusters": timeline_clusters,
        })
    if len(mrr_clusters) > 1:
        mrr_clusters.sort(key=lambda c: c["range"][0])
        conflicts.append({
            "field": "mrr",
            "clusters": mrr_clusters,
        })

    return {
        "entity": entity,
        "total_files": len(entries),
        "budget_clusters_count": len(budget_clusters),
        "timeline_clusters_count": len(timeline_clusters),
        "mrr_clusters_count": len(mrr_clusters),
        "conflicts": conflicts,
    }


def main() -> None:
    facts = json.loads((REPORTS / "03_facts.json").read_text(encoding="utf-8"))
    by_entity = facts["by_entity"]

    results = []
    for ent, entries in by_entity.items():
        results.append(analyze(ent, entries))

    md = [
        "# Фаза 4 — Согласованность данных",
        "",
        "## Сводка",
        "",
        "| Сущность | Файлов | Бюджет-кластеров | Срок-кластеров | MRR-кластеров |",
        "|----------|-------:|-----------------:|---------------:|--------------:|",
    ]
    for r in sorted(results, key=lambda x: -x["total_files"]):
        md.append(
            f"| {r['entity']} | {r['total_files']} | {r['budget_clusters_count']} "
            f"| {r['timeline_clusters_count']} | {r['mrr_clusters_count']} |"
        )
    md.append("")

    conflicts_only = [r for r in results if r["conflicts"]]
    md.append("## Сущности с потенциальными конфликтами")
    md.append("")
    if not conflicts_only:
        md.append("Не обнаружено.")
    else:
        md.append("Замечание: «кластер» — это группа совместимых диапазонов "
                  "(например, €100K и €100-150K — один кластер).")
        md.append("Несколько кластеров — повод проверить, не одна ли это сущность с разной разметкой.")
        md.append("")
        for r in conflicts_only:
            md.append(f"### {r['entity']}")
            md.append("")
            for c in r["conflicts"]:
                md.append(f"**{c['field']}**: {len(c['clusters'])} кластеров")
                for cl in c["clusters"]:
                    raws = ", ".join(sorted(set(cl["raw"]))[:5])
                    files_count = len(cl["files"])
                    md.append(f"- диапазон `{cl['range']}` (упомянут как: {raws}) — в {files_count} файлах")
                md.append("")

    (REPORTS / "04_consistency.md").write_text("\n".join(md), encoding="utf-8")
    (QUEUES / "conflicts.json").write_text(
        json.dumps(conflicts_only, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"[phase_4] entities={len(results)} with_conflicts={len(conflicts_only)}")


if __name__ == "__main__":
    main()
