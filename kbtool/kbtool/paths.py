"""Разрешение путей — где находится корпус. Не привязано ни к какому репо.

Приоритет:
1. Явный аргумент пути (CLI)
2. env KBTOOL_DOCS
3. ./docs если существует, иначе текущая директория
"""

from __future__ import annotations

import os
from pathlib import Path


def resolve_docs(explicit: str | None = None) -> Path:
    if explicit:
        return Path(explicit).expanduser().resolve()
    env = os.environ.get("KBTOOL_DOCS")
    if env:
        return Path(env).expanduser().resolve()
    cwd = Path.cwd()
    docs = cwd / "docs"
    return (docs if docs.exists() else cwd).resolve()
