#!/usr/bin/env python3
"""Фаза 3 — Извлечение фактов из всех карточек.

Извлекаем regex-ом: бюджеты (€...), сроки (... мес), приоритеты (★...),
номера параграфов (§ N SGB ...), MRR-цели, проценты конверсии.

Группируем по сущностям ("НейроОС", "CareMate" и т.п.) для следующей фазы.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[2]
AUDIT = Path(__file__).resolve().parents[1]
REPORTS = AUDIT / "reports"

# Сущности, которые отслеживаем (можно расширять)
ENTITIES = {
    "NeuroOS": [r"НейроОС", r"NeuroOS", r"Internet Function OS", r"\bIFOS\b"],
    "CareMate": [r"CareMate"],
    "SkyMediaHub": [r"SkyMediaHub"],
    "DigitalCaravan": [r"Цифровой Караван", r"Digital Caravan"],
    "NeuroPortal": [r"НейроПортал", r"NeuroPortal"],
    "ForthSwarm": [r"Forth[- ]Рой", r"Forth Swarm"],
    "SozialPlaner": [r"SozialPlaner"],
    "TetraDrone": [r"TetraDrone"],
    "FlamberRotor": [r"FlamberRotor"],
    "RobotZoo": [r"15 робот", r"роботов-зверей", r"robot zoo"],
    "WILOS": [r"\bWILOS\b"],
}

# Шаблоны фактов
BUDGET_RE = re.compile(r"€\s*(\d{1,3}(?:[\s,]?\d{3})*(?:[-–]\s*\d{1,3}(?:[\s,]?\d{3})*)?\s*[KMkmМмК]?)")
TIMELINE_RE = re.compile(r"(\d+(?:[-–]\d+)?)\s*мес")
STARS_RE = re.compile(r"★{1,5}")
PARAGRAPH_RE = re.compile(r"§\s*\d+[a-z]?\s*SGB\s*[IVX]+|§\s*\d+[a-z]?\s*Bay[A-Za-z]+|Art\.\s*\d+\s*UN-BRK")
MRR_RE = re.compile(r"€\s*(\d+(?:[-–]\d+)?\s*K)\s*MRR", re.IGNORECASE)


def detect_entities(text: str) -> set[str]:
    found = set()
    for name, patterns in ENTITIES.items():
        for p in patterns:
            if re.search(p, text):
                found.add(name)
                break
    return found


def extract_from_file(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="ignore")
    return {
        "path": str(path.relative_to(ROOT)),
        "entities": sorted(detect_entities(text)),
        "budgets": BUDGET_RE.findall(text)[:20],  # лимит для здравомыслия
        "timelines_mes": TIMELINE_RE.findall(text)[:20],
        "stars": STARS_RE.findall(text)[:5],
        "paragraphs": list(set(PARAGRAPH_RE.findall(text)))[:20],
        "mrr": MRR_RE.findall(text)[:5],
    }


def main() -> None:
    by_file: list[dict] = []
    by_entity: dict[str, list[dict]] = defaultdict(list)

    for md in sorted(ROOT.rglob("*.md")):
        if "_audit" in md.parts:
            continue
        rec = extract_from_file(md)
        # пропускаем «пустые» записи
        if not any([rec["entities"], rec["budgets"], rec["timelines_mes"],
                    rec["paragraphs"], rec["mrr"]]):
            continue
        by_file.append(rec)
        for ent in rec["entities"]:
            by_entity[ent].append({
                "file": rec["path"],
                "budgets": rec["budgets"],
                "timelines_mes": rec["timelines_mes"],
                "mrr": rec["mrr"],
            })

    output = {
        "by_file": by_file,
        "by_entity": dict(by_entity),
    }
    (REPORTS / "03_facts.json").write_text(
        json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # Краткий отчёт
    md = [
        "# Фаза 3 — Извлечение фактов",
        "",
        "## Сводка",
        "",
        f"- Файлов с фактами: **{len(by_file)}**",
        f"- Отслеживаемых сущностей: **{len(ENTITIES)}**",
        f"- Сущностей встречено: **{len(by_entity)}**",
        "",
        "## По сущностям (упоминаний)",
        "",
        "| Сущность | Файлов |",
        "|----------|-------:|",
    ]
    for ent in sorted(by_entity, key=lambda k: -len(by_entity[k])):
        md.append(f"| {ent} | {len(by_entity[ent])} |")
    md.append("")

    (REPORTS / "03_facts.md").write_text("\n".join(md), encoding="utf-8")
    print(f"[phase_3] files_with_facts={len(by_file)} entities={len(by_entity)}")


if __name__ == "__main__":
    main()
