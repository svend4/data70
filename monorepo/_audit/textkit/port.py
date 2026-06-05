#!/usr/bin/env python3
"""port.py — извлекает технические скрипты из репо-донора (lorenzo) в
переносимый, контент-агностичный комплект.

Что делает:
1. Берёт scripts/*.py из донора.
2. Отбирает чистые stdlib-скрипты (без numpy/sklearn/anthropic/openai/...).
3. Переписывает 2 строки привязки:
     ROOT = Path(__file__).parent.parent   →  from tk_paths import ROOT, DOCS, SCRIPTS, SOURCES
     DOCS = ROOT / "docs"                   →  (удаляется — берётся из tk_paths)
4. Копирует локальные хелперы (utils_*.py) с той же обработкой.
5. Кладёт всё в lib/ рядом с tk_paths.py — становится переносимым.

После портирования скрипт работает на ЛЮБОМ репо:
    TEXTKIT_DOCS=/path/to/docs python lib/improve_clusters.py

Запуск:
    python port.py --source /home/user/lorenzo/scripts --dest lib
    python port.py --source /home/user/lorenzo/scripts --dest lib --all   # включая внешне-зависимые (помечает)
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent

# Внешние пакеты, наличие которых означает «не чистый stdlib»
EXTERNAL = re.compile(
    r"^\s*(?:import|from)\s+"
    r"(numpy|scipy|sklearn|pandas|docstoolkit|anthropic|openai|requests|"
    r"yaml|bs4|markdown|nltk|spacy|torch|transformers|faiss|chromadb|"
    r"sentence_transformers|tiktoken)\b",
    re.MULTILINE,
)

ROOT_LINE = re.compile(r"^ROOT\s*=\s*Path\(__file__\)\.parent\.parent\s*$", re.MULTILINE)
DOCS_LINE = re.compile(r"^DOCS\s*=\s*ROOT\s*/\s*[\"']docs[\"']\s*$", re.MULTILINE)
INLINE_PP = re.compile(r"Path\(__file__\)\.parent\.parent")

IMPORT_SHIM = "from tk_paths import ROOT, DOCS, SCRIPTS, SOURCES  # [ported] universal paths"


def is_pure_stdlib(text: str) -> bool:
    return EXTERNAL.search(text) is None


def transform(text: str) -> tuple[str, list[str]]:
    """Возвращает (новый_текст, список_заметок)."""
    notes: list[str] = []

    if ROOT_LINE.search(text):
        text = ROOT_LINE.sub(IMPORT_SHIM, text, count=1)
        notes.append("ROOT→tk_paths")
    elif INLINE_PP.search(text):
        notes.append("WARN: inline parent.parent — нужна ручная проверка")

    if DOCS_LINE.search(text):
        text = DOCS_LINE.sub("# DOCS импортирован из tk_paths  # [ported]", text, count=1)
        notes.append("DOCS→tk_paths")

    return text, notes


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, help="папка scripts/ донора")
    ap.add_argument("--dest", default="lib", help="куда писать (отн. этого файла)")
    ap.add_argument("--all", action="store_true", help="портировать и внешне-зависимые (с пометкой)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    src = Path(args.source).expanduser().resolve()
    dest = (HERE / args.dest).resolve()
    dest.mkdir(parents=True, exist_ok=True)

    py_files = sorted(src.glob("*.py"))
    ported, skipped, warned = [], [], []

    for f in py_files:
        name = f.name
        # берём improve_* и utils_* (хелперы)
        if not (name.startswith("improve_") or name.startswith("utils_")):
            skipped.append((name, "не improve_/utils_"))
            continue

        text = f.read_text(encoding="utf-8", errors="ignore")
        pure = is_pure_stdlib(text)
        if not pure and not args.all:
            skipped.append((name, "внешние зависимости"))
            continue

        new_text, notes = transform(text)
        if not pure:
            notes.append("EXTERNAL-DEPS")
            warned.append(name)
        if any(n.startswith("WARN") for n in notes):
            warned.append(name)

        if not args.dry_run:
            (dest / name).write_text(new_text, encoding="utf-8")
        ported.append((name, notes))

    print(f"Источник:  {src}")
    print(f"Назначение: {dest}")
    print(f"Портировано: {len(ported)}  Пропущено: {len(skipped)}  С предупреждениями: {len(set(warned))}")
    print()
    if warned:
        print("Скрипты, требующие внимания:")
        for n in sorted(set(warned)):
            print(f"  ⚠ {n}")
    print()
    print("Примеры портированных:")
    for name, notes in ported[:15]:
        print(f"  ✓ {name}  [{', '.join(notes) or 'без изменений'}]")


if __name__ == "__main__":
    main()
