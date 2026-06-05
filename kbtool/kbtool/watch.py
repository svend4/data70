"""Инкрементальный watcher: при изменении файла обновляет индекс и пересчитывает
health. Stdlib-only (mtime-poll, без inotify).
"""

from __future__ import annotations

import time
from pathlib import Path

from .corpus import TEXT_EXT


def _snapshot(docs_root: Path, exclude: set[str]) -> dict[str, float]:
    snap: dict[str, float] = {}
    for f in docs_root.rglob("*"):
        if not f.is_file() or f.suffix.lower() not in TEXT_EXT:
            continue
        parts = f.relative_to(docs_root).parts
        if any(p.startswith(".") or p == "__pycache__" for p in parts):
            continue
        if exclude & set(parts):
            continue
        try:
            snap[str(f.relative_to(docs_root))] = f.stat().st_mtime
        except OSError:
            pass
    return snap


def watch(docs_root: Path, exclude: set[str], on_change, interval: float = 2.0):
    """Цикл-поллер. on_change(added, modified, removed) вызывается при дельте.

    Прерывается KeyboardInterrupt.
    """
    prev = _snapshot(docs_root, exclude)
    print(f"watch: {docs_root}  (poll {interval}s, Ctrl+C для выхода)")
    print(f"  стартовый snapshot: {len(prev)} файлов")
    try:
        while True:
            time.sleep(interval)
            cur = _snapshot(docs_root, exclude)
            added = [k for k in cur if k not in prev]
            removed = [k for k in prev if k not in cur]
            modified = [k for k in cur if k in prev and cur[k] != prev[k]]
            if added or removed or modified:
                on_change(added, modified, removed)
                prev = cur
    except KeyboardInterrupt:
        print("\nwatch: остановлен")
