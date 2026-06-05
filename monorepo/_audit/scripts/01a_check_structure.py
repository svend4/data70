#!/usr/bin/env python3
"""Фаза 1a — Структурные проверки.

Правила:
- Каждый кластер 00-10 должен иметь README.md, map.md, next_steps.md.
- Каждая тематическая подпапка должна иметь README.md.
- Служебные папки (superprojects, 99_archive_links, 88_topics_full) — только README.md.
"""

from __future__ import annotations

import json
from pathlib import Path

AUDIT = Path(__file__).resolve().parents[1]
REPORTS = AUDIT / "reports"
QUEUES = AUDIT / "queues"
QUEUES.mkdir(exist_ok=True)


def main() -> None:
    inv = json.loads((REPORTS / "00_inventory.json").read_text(encoding="utf-8"))

    full_clusters = {"00_index", "01_social_law", "02_ai_agents", "03_drones_skymediahub",
                     "04_robotics_caremate", "05_software_automation", "06_business_funding",
                     "07_inventions_patents", "08_knowledge_methodology", "09_media_newsroom",
                     "10_health_accessibility"}
    misc_clusters = {"superprojects", "99_archive_links", "88_topics_full"}

    defects: list[dict] = []
    cluster_lines: list[str] = []

    for name, c in inv["clusters"].items():
        is_full = name in full_clusters
        is_misc = name in misc_clusters or c.get("misc")

        issues: list[str] = []
        if not c.get("has_readme"):
            issues.append("missing_README.md")
        if is_full:
            if not c.get("has_map"):
                issues.append("missing_map.md")
            if not c.get("has_next_steps"):
                issues.append("missing_next_steps.md")

        # подпапки
        missing_topic_readmes: list[str] = []
        for topic_name, t in c.get("topics", {}).items():
            if not t.get("has_readme"):
                missing_topic_readmes.append(topic_name)

        for tname in missing_topic_readmes:
            issues.append(f"topic_missing_README:{tname}")

        if issues:
            defects.append({"cluster": name, "issues": issues})

        topics_count = len(c.get("topics", {}))
        status = "OK" if not issues else f"{len(issues)} issues"
        cluster_lines.append(
            f"| `{name}` | {'full' if is_full else 'misc'} "
            f"| {topics_count} | {status} |"
        )

    # Pепорт
    md = [
        "# Фаза 1a — Структура",
        "",
        "## Сводка",
        "",
        f"- Кластеров проверено: **{len(inv['clusters'])}**",
        f"- Кластеров с дефектами: **{len(defects)}**",
        f"- Кластеров OK: **{len(inv['clusters']) - len(defects)}**",
        "",
        "## По кластерам",
        "",
        "| Кластер | Тип | Подпапок | Статус |",
        "|---------|-----|---------:|--------|",
        *cluster_lines,
        "",
    ]
    if defects:
        md.append("## Дефекты")
        md.append("")
        for d in defects:
            md.append(f"### `{d['cluster']}`")
            for issue in d["issues"]:
                md.append(f"- {issue}")
            md.append("")
    else:
        md.append("## Дефекты")
        md.append("")
        md.append("Не обнаружено.")
        md.append("")

    (REPORTS / "01a_structure.md").write_text("\n".join(md), encoding="utf-8")
    (QUEUES / "repair.json").write_text(
        json.dumps(defects, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"[phase_1a] defects_clusters={len(defects)}")


if __name__ == "__main__":
    main()
