#!/usr/bin/env python3
"""classify.py — статическая разметка безопасности портированных скриптов.

Грепает каждый lib/improve_*.py на операции записи и относит к категории:
  - read_only        : пишет только в свой отчётный файл (CAPS.md в DOCS-корне) или печатает
  - appends_to_cards : вписывает в существующие .md (rglob + write_text/open 'a'|'w')
  - creates_subdirs  : создаёт подпапки (obsidian/, badges/, chunks/, …)
  - unknown          : не удалось определить

Это эвристика для приоритезации, НЕ замена sandbox. Sandbox (run_all --sandbox)
гарантирует изоляцию независимо от этой разметки.

Запуск:
    python3 classify.py            # таблица в stdout
    python3 classify.py --json     # JSON
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
LIB = HERE / "lib"

# Признаки записи в существующие карточки (опасно)
APPEND_CARD = re.compile(
    r"\.rglob\(['\"]\*\.md['\"]\).*?(write_text|open\([^)]*['\"][aw]['\"])",
    re.DOTALL,
)
WRITE_TEXT = re.compile(r"\.write_text\(")
OPEN_WRITE = re.compile(r"open\([^)]*,\s*['\"][aw]")
MKDIR = re.compile(r"\.mkdir\(|makedirs\(")
SUBDIR_CREATE = re.compile(r"(obsidian|badges|chunks|confluence|templates|feed)\b")

# Признак записи в один отчётный файл в DOCS-корне (терпимо)
REPORT_OUT = re.compile(r"DOCS\s*/\s*['\"][A-Z_]+\.(md|json|svg|rss|atom|csv|html|dot)['\"]")


def classify_one(text: str) -> tuple[str, list[str]]:
    notes = []
    writes = bool(WRITE_TEXT.search(text) or OPEN_WRITE.search(text))
    mkdirs = bool(MKDIR.search(text))
    subdirs = bool(SUBDIR_CREATE.search(text))
    report_out = bool(REPORT_OUT.search(text))

    # вписывает в карточки: rglob по .md И запись, при этом цикл по файлам с записью
    iterates_and_writes = (
        ".rglob" in text and writes
        and re.search(r"for\s+\w+\s+in\s+.*rglob", text)
        and (".write_text" in text)
    )

    if not writes and not mkdirs:
        return "read_only", ["только печать/чтение"]

    if iterates_and_writes and not report_out:
        notes.append("итерирует .md + write_text → вероятно вписывает в карточки")
        return "appends_to_cards", notes

    if mkdirs and subdirs:
        notes.append("создаёт служебные подпапки")
        return "creates_subdirs", notes

    if report_out and not iterates_and_writes:
        notes.append("пишет в один CAPS-отчёт в DOCS-корне")
        return "read_only", notes

    if writes:
        notes.append("есть запись — точная цель не ясна, см. sandbox")
        return "unknown", notes

    return "unknown", ["не определено"]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    rows = []
    for f in sorted(LIB.glob("improve_*.py")):
        text = f.read_text(encoding="utf-8", errors="ignore")
        cat, notes = classify_one(text)
        rows.append({"script": f.name, "category": cat, "notes": notes})

    counts: dict[str, int] = {}
    for r in rows:
        counts[r["category"]] = counts.get(r["category"], 0) + 1

    if args.json:
        print(json.dumps({"counts": counts, "scripts": rows},
                         ensure_ascii=False, indent=2))
        return

    print("# Классификация безопасности скриптов\n")
    for cat in ["read_only", "creates_subdirs", "appends_to_cards", "unknown"]:
        items = [r for r in rows if r["category"] == cat]
        print(f"## {cat} ({len(items)})")
        for r in items:
            note = f"  — {r['notes'][0]}" if r["notes"] else ""
            print(f"  {r['script']}{note}")
        print()
    print("Итого:", counts)


if __name__ == "__main__":
    main()
