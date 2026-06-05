"""Загрузка корпуса: сканирование markdown/текстовых файлов в документы."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .profile import Profile

STOPWORDS = {
    # ru
    "и", "в", "не", "на", "что", "с", "по", "это", "как", "из", "для", "к",
    "а", "но", "то", "или", "от", "о", "при", "за", "уже", "чем", "так", "же",
    "его", "её", "их", "все", "они", "он", "она", "мы", "вы", "я", "бы", "быть",
    "только", "ещё", "также", "этого", "этой", "том", "может", "нет", "да",
    "такой", "самый", "один", "два", "три", "если",
    # en
    "the", "a", "an", "of", "in", "to", "and", "is", "are", "for", "that",
    "this", "with", "be", "by", "as", "at", "or", "not", "it", "on", "от",
}

TEXT_EXT = {".md", ".markdown", ".txt", ".rst"}
WORD_RE = re.compile(r"[а-яёa-z][а-яёa-z\-]{2,}")


@dataclass
class Doc:
    path: Path
    rel: str
    text: str
    tokens: list[str]


def tokenize(text: str) -> list[str]:
    return [w for w in WORD_RE.findall(text.lower()) if w not in STOPWORDS]


def load(docs_root: Path, profile: Profile,
         exts: set[str] | None = None,
         exclude_dirs: set[str] | None = None) -> list[Doc]:
    exts = exts or TEXT_EXT
    skip = profile.skip_names()
    exclude_dirs = exclude_dirs or set()
    out: list[Doc] = []
    for f in sorted(docs_root.rglob("*")):
        if not f.is_file() or f.suffix.lower() not in exts:
            continue
        if f.name in skip:
            continue
        # пропускаем служебные/скрытые папки + явные исключения
        rel_parts = f.relative_to(docs_root).parts
        if any(part.startswith(".") or part == "__pycache__" for part in f.parts):
            continue
        if exclude_dirs & set(rel_parts):
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        toks = tokenize(text)
        if len(toks) < profile.min_tokens:
            continue
        out.append(Doc(path=f, rel=str(f.relative_to(docs_root)),
                       text=text, tokens=toks))
    return out
