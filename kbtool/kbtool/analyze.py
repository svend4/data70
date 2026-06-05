"""Аналитика: TF-IDF кластеризация, дедупликация, концепт-граф. Pure stdlib."""

from __future__ import annotations

import hashlib
import math
import re
from collections import Counter, defaultdict

from .corpus import Doc


# --- TF-IDF + косинус ---------------------------------------------------------

def _tfidf(docs: list[Doc]) -> dict[str, dict[str, float]]:
    n = len(docs)
    df: Counter = Counter()
    for d in docs:
        df.update(set(d.tokens))
    out: dict[str, dict[str, float]] = {}
    for d in docs:
        tf = Counter(d.tokens)
        total = len(d.tokens) or 1
        vec = {}
        for term, c in tf.items():
            idf = math.log((n + 1) / (df[term] + 1)) + 1
            vec[term] = (c / total) * idf
        out[d.rel] = vec
    return out


def _cosine(a: dict[str, float], b: dict[str, float]) -> float:
    common = set(a) & set(b)
    if not common:
        return 0.0
    num = sum(a[t] * b[t] for t in common)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    return num / (na * nb) if na and nb else 0.0


def cluster(docs: list[Doc], threshold: float = 0.15) -> list[dict]:
    """Жадная агломерация по косинусной близости TF-IDF."""
    vecs = _tfidf(docs)
    rels = [d.rel for d in docs]
    assigned: dict[str, int] = {}
    clusters: list[list[str]] = []
    for i, ri in enumerate(rels):
        if ri in assigned:
            continue
        group = [ri]
        assigned[ri] = len(clusters)
        for rj in rels[i + 1:]:
            if rj in assigned:
                continue
            if _cosine(vecs[ri], vecs[rj]) >= threshold:
                group.append(rj)
                assigned[rj] = len(clusters)
        clusters.append(group)
    # ярлыки кластеров — топ-термины
    result = []
    for grp in clusters:
        agg: Counter = Counter()
        for r in grp:
            agg.update(vecs[r])
        label = ", ".join(t for t, _ in agg.most_common(4))
        result.append({"label": label, "size": len(grp), "files": grp})
    result.sort(key=lambda c: -c["size"])
    return result


# --- Дедупликация по абзацам --------------------------------------------------

def _para_hashes(text: str) -> set[str]:
    hashes = set()
    for para in re.split(r"\n\s*\n", text):
        norm = re.sub(r"\s+", " ", para.strip().lower())
        if len(norm) >= 80:  # только содержательные абзацы
            hashes.add(hashlib.sha1(norm.encode()).hexdigest())
    return hashes


def dedup(docs: list[Doc], jaccard_min: float = 0.5) -> list[dict]:
    hmaps = {d.rel: _para_hashes(d.text) for d in docs}
    hmaps = {k: v for k, v in hmaps.items() if v}
    rels = list(hmaps)
    pairs = []
    for i in range(len(rels)):
        for j in range(i + 1, len(rels)):
            a, b = hmaps[rels[i]], hmaps[rels[j]]
            inter = a & b
            if not inter:
                continue
            jac = len(inter) / len(a | b)
            if jac >= jaccard_min:
                pairs.append({"a": rels[i], "b": rels[j],
                              "jaccard": round(jac, 3), "shared": len(inter)})
    pairs.sort(key=lambda p: -p["jaccard"])
    return pairs


# --- Концепт-граф (совстречаемость топ-терминов) ------------------------------

def concept_graph(docs: list[Doc], top_concepts: int = 40,
                  min_edge: int = 2) -> dict:
    freq: Counter = Counter()
    per_doc: list[set[str]] = []
    for d in docs:
        terms = set(t for t, _ in Counter(d.tokens).most_common(15))
        per_doc.append(terms)
        freq.update(terms)
    top = {t for t, _ in freq.most_common(top_concepts)}
    edges: Counter = Counter()
    for terms in per_doc:
        rel = sorted(terms & top)
        for i in range(len(rel)):
            for j in range(i + 1, len(rel)):
                edges[(rel[i], rel[j])] += 1
    edge_list = [{"a": a, "b": b, "weight": w}
                 for (a, b), w in edges.items() if w >= min_edge]
    edge_list.sort(key=lambda e: -e["weight"])
    return {
        "nodes": sorted(top),
        "top": [t for t, _ in freq.most_common(10)],
        "edges": edge_list,
    }
