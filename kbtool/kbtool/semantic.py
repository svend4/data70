"""Опциональный semantic-плагин: эмбеддинги через sentence-transformers.

Если пакет недоступен — функции возвращают None, и вызывающий код должен
использовать TF-IDF (модули analyze.py / rag.py).

Установка:
    pip install kbtool[semantic]
"""

from __future__ import annotations

import math
from pathlib import Path


def available() -> bool:
    try:
        import sentence_transformers  # noqa
        return True
    except ImportError:
        return False


def _get_model(name: str = "paraphrase-multilingual-MiniLM-L12-v2"):
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(name)


def embed_texts(texts: list[str], model_name: str | None = None):
    """Возвращает list[list[float]] эмбеддингов или None если пакет недоступен."""
    if not available():
        return None
    model = _get_model(model_name or "paraphrase-multilingual-MiniLM-L12-v2")
    return model.encode(texts, normalize_embeddings=True).tolist()


def cosine(a: list[float], b: list[float]) -> float:
    num = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return num / (na * nb) if na and nb else 0.0


def semantic_search(query: str, doc_embeddings: dict[str, list[float]],
                    top_k: int = 5) -> list[tuple[str, float]]:
    """doc_embeddings = {doc_id: vector}. Возвращает [(doc_id, score)]."""
    if not available():
        return []
    qvec = embed_texts([query])
    if not qvec:
        return []
    qv = qvec[0]
    scored = [(doc_id, cosine(qv, v)) for doc_id, v in doc_embeddings.items()]
    scored.sort(key=lambda x: -x[1])
    return scored[:top_k]
