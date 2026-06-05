"""tk_paths.py — универсальный резолвер путей для переносимых текст-инструментов.

Заменяет жёсткую привязку lorenzo-скриптов:
    ROOT = Path(__file__).parent.parent
    DOCS = ROOT / "docs"

на конфигурацию через переменные окружения. Любой скрипт, импортирующий
ROOT/DOCS отсюда, работает с ЛЮБЫМ репозиторием без правки кода.

Приоритет разрешения:
1. TEXTKIT_DOCS  — прямой путь к папке с .md (например /home/user/data70/monorepo)
2. TEXTKIT_ROOT  — корень репо; DOCS = ROOT/"docs"
3. cwd           — текущая директория; DOCS = cwd/"docs" или cwd, если docs нет

Использование:
    TEXTKIT_DOCS=/path/to/docs python improve_clusters.py
"""

from __future__ import annotations

import os
from pathlib import Path


def _resolve() -> tuple[Path, Path]:
    docs_env = os.environ.get("TEXTKIT_DOCS")
    if docs_env:
        docs = Path(docs_env).expanduser().resolve()
        return docs.parent, docs

    root_env = os.environ.get("TEXTKIT_ROOT")
    if root_env:
        root = Path(root_env).expanduser().resolve()
        docs = root / "docs"
        if not docs.exists():
            docs = root  # репо без отдельной docs/ — markdown в корне
        return root, docs

    cwd = Path.cwd().resolve()
    docs = cwd / "docs"
    if not docs.exists():
        docs = cwd
    return cwd, docs


ROOT, DOCS = _resolve()

# Доп. пути, на которые иногда ссылаются скрипты
SCRIPTS = ROOT / "scripts"
SOURCES = ROOT / "sources"


def describe() -> str:
    return f"ROOT={ROOT}\nDOCS={DOCS}\nexists={DOCS.exists()}"


if __name__ == "__main__":
    print(describe())
