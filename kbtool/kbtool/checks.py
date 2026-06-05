"""Детерминированные проверки: инвентаризация, структура, ссылки. Read-only."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlparse

LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


def _excluded(f: Path, root: Path, exclude: set[str]) -> bool:
    parts = f.relative_to(root).parts
    if any(p.startswith(".") or p == "__pycache__" for p in parts):
        return True
    return bool(exclude & set(parts))


def inventory(docs_root: Path, exclude: set[str] | None = None) -> dict:
    exclude = exclude or set()
    md = [f for f in docs_root.rglob("*.md") if not _excluded(f, docs_root, exclude)]
    total_bytes = sum(f.stat().st_size for f in md)
    total_lines = 0
    for f in md:
        try:
            total_lines += sum(1 for _ in f.open("r", encoding="utf-8", errors="ignore"))
        except Exception:
            pass
    # верхнеуровневые папки
    top = sorted([d.name for d in docs_root.iterdir()
                  if d.is_dir() and not d.name.startswith(".")])
    return {
        "root": str(docs_root),
        "markdown_files": len(md),
        "total_bytes": total_bytes,
        "total_lines": total_lines,
        "top_level_dirs": top,
    }


def check_links(docs_root: Path, exclude: set[str] | None = None) -> dict:
    exclude = exclude or set()
    broken: list[dict] = []
    counts = {"files": 0, "links": 0, "external": 0, "ok": 0, "broken": 0}
    for f in sorted(docs_root.rglob("*.md")):
        if _excluded(f, docs_root, exclude):
            continue
        counts["files"] += 1
        text = f.read_text(encoding="utf-8", errors="ignore")
        for m in LINK_RE.finditer(text):
            label, url = m.group(1), m.group(2)
            counts["links"] += 1
            if urlparse(url).scheme or url.startswith(("http", "mailto:", "#")):
                counts["external"] += 1
                continue
            try:
                target = (f.parent / url.split("#", 1)[0]).resolve()
                exists = target.exists()
            except (OSError, ValueError):
                # слишком длинный путь / некорректные символы — считаем битым
                exists = False
            if exists:
                counts["ok"] += 1
            else:
                counts["broken"] += 1
                broken.append({"file": str(f.relative_to(docs_root)),
                               "label": label, "url": url})
    return {"counts": counts, "broken": broken}


def check_structure(docs_root: Path, require: tuple[str, ...] = ("README.md",),
                    exclude: set[str] | None = None) -> dict:
    """Проверяет, что каждая непустая папка имеет требуемые файлы."""
    exclude = exclude or set()
    issues: list[dict] = []
    checked = 0
    for d in sorted(docs_root.rglob("*")):
        if not d.is_dir() or _excluded(d, docs_root, exclude):
            continue
        has_md = any(f.suffix == ".md" for f in d.iterdir() if f.is_file())
        has_subdirs = any(s.is_dir() for s in d.iterdir())
        if not has_md and not has_subdirs:
            continue
        checked += 1
        try:
            missing = [r for r in require if not (d / r).exists()]
        except (OSError, ValueError):
            continue
        # требуем README только у листовых папок с .md, но без подпапок-тем
        leaf_with_content = has_md and not any(
            s.is_dir() and any(x.suffix == ".md" for x in s.iterdir() if x.is_file())
            for s in d.iterdir() if s.is_dir()
        )
        if missing and leaf_with_content:
            issues.append({"dir": str(d.relative_to(docs_root)), "missing": missing})
    return {"checked": checked, "issues": issues}
