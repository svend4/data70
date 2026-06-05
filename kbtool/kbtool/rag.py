"""Поисковый индекс корпуса + keyword/BM25/гибридный поиск + ответ с цитатами.

Stdlib-only. Индекс — JSON, сохраняется в .kbtool/ внутри корпуса (1 файл).
"""

from __future__ import annotations

import json
import math
import re
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

from .corpus import Doc, tokenize, load
from .profile import Profile

INDEX_DIR = ".kbtool"
INDEX_FILE = "index.json"


@dataclass
class Hit:
    doc_id: str
    score: float
    snippet: str
    title: str


def index_path(docs_root: Path) -> Path:
    return docs_root / INDEX_DIR / INDEX_FILE


def _title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def _passages(text: str, max_len: int = 400) -> list[str]:
    """Грубо нарезаем по абзацам, склеиваем короткие."""
    paras = re.split(r"\n\s*\n", text)
    out: list[str] = []
    buf = ""
    for p in paras:
        p = re.sub(r"\s+", " ", p).strip()
        if not p:
            continue
        if len(buf) + len(p) + 1 <= max_len:
            buf = (buf + " " + p) if buf else p
        else:
            if buf:
                out.append(buf)
            buf = p[:max_len]
    if buf:
        out.append(buf)
    return out


def build_index(docs_root: Path, profile: Profile | None = None,
                exclude_dirs: set[str] | None = None) -> dict:
    """Строит и сохраняет индекс. Возвращает структуру индекса.

    Формат:
      {
        "docs": {doc_id: {"title", "tokens": [...], "passages": [...]}},
        "df":   {term: doc_freq},
        "n":    int,
        "built_at": iso,
      }
    """
    prof = profile or Profile.from_env()
    corpus = load(docs_root, prof, exclude_dirs=exclude_dirs)
    docs_data: dict[str, dict] = {}
    df: Counter = Counter()
    for d in corpus:
        passages = _passages(d.text)
        docs_data[d.rel] = {
            "title": _title(d.text, Path(d.rel).stem),
            "tokens": d.tokens,
            "passages": passages,
        }
        df.update(set(d.tokens))
    idx = {
        "docs": docs_data,
        "df": dict(df),
        "n": len(corpus),
        "built_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "root": str(docs_root),
    }
    out = index_path(docs_root)
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(idx, ensure_ascii=False), encoding="utf-8")
    return idx


def load_index(docs_root: Path) -> dict | None:
    p = index_path(docs_root)
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


# --- BM25 ---------------------------------------------------------------------

def _bm25_score(query_tokens: list[str], doc_tokens: list[str],
                df: dict[str, int], n_docs: int, avgdl: float,
                k1: float = 1.5, b: float = 0.75) -> float:
    if not doc_tokens:
        return 0.0
    tf = Counter(doc_tokens)
    dl = len(doc_tokens)
    score = 0.0
    for t in query_tokens:
        if t not in tf:
            continue
        idf = math.log((n_docs - df.get(t, 0) + 0.5) / (df.get(t, 0) + 0.5) + 1)
        denom = tf[t] + k1 * (1 - b + b * dl / (avgdl or 1))
        score += idf * (tf[t] * (k1 + 1)) / denom
    return score


def search(idx: dict, query: str, top_k: int = 5,
           method: str = "bm25") -> list[Hit]:
    q_tokens = tokenize(query)
    if not q_tokens or not idx.get("docs"):
        return []
    docs = idx["docs"]
    df = idx["df"]
    n = idx["n"] or 1
    avgdl = sum(len(d["tokens"]) for d in docs.values()) / (len(docs) or 1)

    scored: list[tuple[str, float]] = []
    for doc_id, d in docs.items():
        if method == "keyword":
            tf = Counter(d["tokens"])
            s = sum(tf.get(t, 0) for t in q_tokens)
        else:  # bm25
            s = _bm25_score(q_tokens, d["tokens"], df, n, avgdl)
        if s > 0:
            scored.append((doc_id, s))
    scored.sort(key=lambda x: -x[1])

    hits: list[Hit] = []
    for doc_id, s in scored[:top_k]:
        d = docs[doc_id]
        # лучший пассаж — по числу term-hits
        best, best_score = d["passages"][0] if d["passages"] else "", -1
        for p in d["passages"]:
            ptoks = set(tokenize(p))
            ps = sum(1 for t in q_tokens if t in ptoks)
            if ps > best_score:
                best, best_score = p, ps
        hits.append(Hit(doc_id=doc_id, score=round(s, 3),
                        snippet=best[:300], title=d["title"]))
    return hits


def answer(idx: dict, question: str, top_k: int = 5) -> dict:
    """Простой extractive 'ответ' = склейка лучших пассажей с цитатами.

    Это offline echo-answerer (как fallback в lorenzo). Реальный LLM можно
    подключить как плагин — но для исходной задачи 'спросить что-то про
    большой архив' и этого часто достаточно.
    """
    hits = search(idx, question, top_k=top_k, method="bm25")
    if not hits:
        return {"question": question, "answer": "Ничего не найдено.", "citations": []}
    body = "\n\n".join(f"[{i+1}] {h.snippet}" for i, h in enumerate(hits))
    cites = [{"n": i + 1, "doc_id": h.doc_id, "title": h.title,
              "score": h.score} for i, h in enumerate(hits)]
    return {"question": question, "answer": body, "citations": cites}
