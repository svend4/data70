#!/usr/bin/env python3
"""Фаза 0 — Инвентаризация монорепо.

Собирает дерево, метрики, базовую карту ожиданий.
Только чтение. Пишет в reports/00_inventory.{json,md}.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]  # monorepo/
AUDIT = Path(__file__).resolve().parents[1]  # _audit/
REPORTS = AUDIT / "reports"
REPORTS.mkdir(exist_ok=True)


def is_cluster_dir(name: str) -> bool:
    """Кластер верхнего уровня: 00-99 + подчёркивание + имя."""
    if len(name) < 4:
        return False
    return name[:2].isdigit() and name[2] == "_"


def is_topic_dir(name: str) -> bool:
    """Тематическая подпапка кластера: те же правила."""
    return is_cluster_dir(name)


def scan() -> dict:
    inventory: dict = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "root": str(ROOT),
        "clusters": {},
        "totals": {
            "clusters": 0,
            "topic_dirs": 0,
            "markdown_files": 0,
            "total_bytes": 0,
            "total_lines": 0,
        },
    }

    # Игнорируем сам _audit и не-кластерные служебные папки на уровне monorepo
    for entry in sorted(ROOT.iterdir()):
        if not entry.is_dir():
            continue
        if entry.name.startswith("_"):
            continue
        if entry.name in {"chat_export"}:  # это в корне репо, не должно быть здесь
            continue

        if is_cluster_dir(entry.name):
            cluster = scan_cluster(entry)
            inventory["clusters"][entry.name] = cluster
            inventory["totals"]["clusters"] += 1
            inventory["totals"]["topic_dirs"] += len(cluster["topics"])
            inventory["totals"]["markdown_files"] += cluster["markdown_files"]
            inventory["totals"]["total_bytes"] += cluster["bytes"]
            inventory["totals"]["total_lines"] += cluster["lines"]
        else:
            # superprojects/, 88_topics_full/ и т.п. — служебные, но всё равно учтём
            misc = scan_cluster(entry)
            misc["misc"] = True
            inventory["clusters"][entry.name] = misc

    return inventory


def scan_cluster(cluster_dir: Path) -> dict:
    info = {
        "path": str(cluster_dir.relative_to(ROOT)),
        "has_readme": (cluster_dir / "README.md").exists(),
        "has_map": (cluster_dir / "map.md").exists(),
        "has_next_steps": (cluster_dir / "next_steps.md").exists(),
        "topics": {},
        "markdown_files": 0,
        "bytes": 0,
        "lines": 0,
    }

    for sub in sorted(cluster_dir.iterdir()):
        if sub.is_dir():
            topic_info = scan_topic(sub)
            info["topics"][sub.name] = topic_info
            info["markdown_files"] += topic_info["markdown_files"]
            info["bytes"] += topic_info["bytes"]
            info["lines"] += topic_info["lines"]
        elif sub.is_file() and sub.suffix == ".md":
            size = sub.stat().st_size
            lines = sum(1 for _ in sub.open("r", encoding="utf-8", errors="ignore"))
            info["markdown_files"] += 1
            info["bytes"] += size
            info["lines"] += lines

    return info


def scan_topic(topic_dir: Path) -> dict:
    info = {
        "path": str(topic_dir.relative_to(ROOT)),
        "has_readme": (topic_dir / "README.md").exists(),
        "markdown_files": 0,
        "bytes": 0,
        "lines": 0,
        "extra_files": [],
    }
    for f in sorted(topic_dir.rglob("*")):
        if f.is_file():
            if f.suffix == ".md":
                info["markdown_files"] += 1
                info["bytes"] += f.stat().st_size
                info["lines"] += sum(1 for _ in f.open("r", encoding="utf-8", errors="ignore"))
                if f.name != "README.md":
                    info["extra_files"].append(str(f.relative_to(topic_dir)))
    return info


def render_md(inv: dict) -> str:
    t = inv["totals"]
    lines = [
        "# Фаза 0 — Инвентаризация",
        "",
        f"_Создан: {inv['generated_at']}_",
        "",
        "## Сводка",
        "",
        f"- Кластеров (включая служебные): **{len(inv['clusters'])}**",
        f"- Кластеров-тематических: **{t['clusters']}**",
        f"- Тематических подпапок: **{t['topic_dirs']}**",
        f"- Markdown-файлов: **{t['markdown_files']}**",
        f"- Объём текста: **{t['total_bytes']:,} байт**",
        f"- Строк: **{t['total_lines']:,}**",
        "",
        "## Кластеры",
        "",
        "| Папка | README | map | next_steps | Подпапок | md-файлов | байт |",
        "|-------|:------:|:---:|:----------:|---------:|----------:|-----:|",
    ]
    for name, c in inv["clusters"].items():
        lines.append(
            f"| `{name}` | {'✓' if c.get('has_readme') else '✗'} "
            f"| {'✓' if c.get('has_map') else '—'} "
            f"| {'✓' if c.get('has_next_steps') else '—'} "
            f"| {len(c.get('topics', {}))} "
            f"| {c.get('markdown_files', 0)} "
            f"| {c.get('bytes', 0):,} |"
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    inv = scan()
    (REPORTS / "00_inventory.json").write_text(
        json.dumps(inv, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (REPORTS / "00_inventory.md").write_text(render_md(inv), encoding="utf-8")
    t = inv["totals"]
    print(
        f"[phase_0] clusters={t['clusters']} topics={t['topic_dirs']} "
        f"md={t['markdown_files']} bytes={t['total_bytes']:,}"
    )


if __name__ == "__main__":
    main()
