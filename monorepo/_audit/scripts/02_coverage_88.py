#!/usr/bin/env python3
"""Фаза 2 — Покрытие 88 тем.

Парсит таблицу из 00_index/catalog_88_topics.md.
Для каждой темы извлекает целевую подпапку и проверяет:
  - существует ли папка
  - есть ли README.md
  - упоминается ли в README номер темы (#N)
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUDIT = Path(__file__).resolve().parents[1]
REPORTS = AUDIT / "reports"
QUEUES = AUDIT / "queues"

CATALOG = ROOT / "00_index" / "catalog_88_topics.md"

# Парсим строки вида: | 13 | Micro-ИИ агенты | B/C | 02_ai_agents/01_micro_agents |
ROW_RE = re.compile(
    r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|$"
)


def parse_catalog() -> list[dict]:
    text = CATALOG.read_text(encoding="utf-8")
    topics: list[dict] = []
    for line in text.splitlines():
        m = ROW_RE.match(line)
        if not m:
            continue
        num = m.group(1)
        if not num.isdigit():
            continue
        topics.append({
            "id": int(num),
            "name": m.group(2).strip(),
            "abj": m.group(3).strip(),
            "target_raw": m.group(4).strip(),
        })
    return topics


def resolve_target(target_raw: str) -> Path | None:
    """Извлекает первую подпапку из текста колонки."""
    # Берём первое слово вида XX_yyy/XX_zzz
    m = re.search(r"`?(\d{2}_[a-z0-9_]+/\d{2}_[a-z0-9_]+)`?", target_raw)
    if m:
        return ROOT / m.group(1)
    # Может быть только кластер: 02_ai_agents
    m = re.search(r"`?(\d{2}_[a-z0-9_]+)`?", target_raw)
    if m:
        return ROOT / m.group(1)
    return None


def main() -> None:
    topics = parse_catalog()
    if not topics:
        print("[phase_2] WARNING: catalog parse returned 0 rows; check regex.")

    covered: list[dict] = []
    partial: list[dict] = []
    missing: list[dict] = []

    for t in topics:
        target = resolve_target(t["target_raw"])
        record = {
            "id": t["id"],
            "name": t["name"],
            "target_raw": t["target_raw"],
            "target_resolved": str(target.relative_to(ROOT)) if target else None,
        }

        if target is None:
            record["status"] = "no_target_in_catalog"
            partial.append(record)
            continue

        if not target.exists():
            record["status"] = "folder_missing"
            missing.append(record)
            continue

        readme = target / "README.md"
        if not readme.exists():
            record["status"] = "readme_missing"
            missing.append(record)
            continue

        content = readme.read_text(encoding="utf-8", errors="ignore")
        mentions = (
            f"#{t['id']} " in content
            or f"#{t['id']}," in content
            or f"#{t['id']}\n" in content
            or f"#{t['id']})" in content
            or f"Тема каталога:** #{t['id']}" in content
            or f"Темы каталога:** #{t['id']}" in content
            or re.search(rf"#\s*{t['id']}\b", content) is not None
        )
        if mentions:
            record["status"] = "covered"
            covered.append(record)
        else:
            record["status"] = "covered_no_topic_id_mention"
            partial.append(record)

    md = [
        "# Фаза 2 — Покрытие 88 тем",
        "",
        "## Сводка",
        "",
        f"- Всего тем разобрано из каталога: **{len(topics)}**",
        f"- Полностью покрыто (карточка + упоминание #N): **{len(covered)}**",
        f"- Частично (карточка есть, но #N не упомянут): **{len(partial)}**",
        f"- Отсутствует: **{len(missing)}**",
        "",
    ]

    if missing:
        md.append("## Отсутствующие карточки")
        md.append("")
        md.append("| # | Тема | Цель из каталога | Статус |")
        md.append("|---|------|------------------|--------|")
        for r in missing:
            md.append(f"| {r['id']} | {r['name']} | `{r['target_resolved']}` | {r['status']} |")
        md.append("")

    if partial:
        md.append("## Частично покрытые (нет упоминания #N в README)")
        md.append("")
        md.append("| # | Тема | Подпапка |")
        md.append("|---|------|----------|")
        for r in partial[:50]:
            md.append(f"| {r['id']} | {r['name']} | `{r['target_resolved']}` |")
        if len(partial) > 50:
            md.append(f"\n_…ещё {len(partial) - 50} — см. queues/enrich.json_")
        md.append("")

    (REPORTS / "02_coverage_88.md").write_text("\n".join(md), encoding="utf-8")
    (QUEUES / "enrich.json").write_text(
        json.dumps(partial, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (QUEUES / "create.json").write_text(
        json.dumps(missing, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(
        f"[phase_2] topics={len(topics)} covered={len(covered)} "
        f"partial={len(partial)} missing={len(missing)}"
    )


if __name__ == "__main__":
    main()
