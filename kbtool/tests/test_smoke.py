"""Smoke-тест kbtool на временном мини-корпусе."""

import tempfile
from pathlib import Path

from kbtool.paths import resolve_docs
from kbtool.profile import Profile
from kbtool.corpus import load, tokenize
from kbtool.checks import inventory, check_links, check_structure
from kbtool.analyze import cluster, dedup, concept_graph
from kbtool.health import score
from kbtool.tree import plan_tree, materialize, _slug
from kbtool.rag import build_index, load_index, search, answer
from kbtool import semantic as semplugin


def _fixture() -> Path:
    d = Path(tempfile.mkdtemp(prefix="kbtool_test_"))
    (d / "a").mkdir()
    (d / "b").mkdir()
    (d / "a" / "README.md").write_text(
        "# Дроны\n\nTetraDrone это корпус из Tetra Pak. Дрон лёгкий и дешёвый. "
        "Беспилотник для сельского хозяйства и мониторинга полей дронами.\n",
        encoding="utf-8")
    (d / "b" / "README.md").write_text(
        "# Право\n\nPersönliches Budget по SGB IX. Widerspruch против Sozialamt. "
        "Социальное право Германии и пособия для инвалидов и ухода.\n",
        encoding="utf-8")
    (d / "a" / "more.md").write_text(
        "# Ещё дроны\n\nДрон, беспилотник, TetraDrone, мониторинг полей, "
        "сельское хозяйство дронами и корпус Tetra Pak для дрона.\n",
        encoding="utf-8")
    return d


def test_tokenize():
    toks = tokenize("Дрон и беспилотник the drone")
    assert "дрон" in toks and "беспилотник" in toks
    assert "и" not in toks and "the" not in toks


def test_pipeline():
    d = _fixture()
    prof = Profile(readme_is_content=True, min_tokens=5)
    corpus = load(d, prof)
    assert len(corpus) == 3

    inv = inventory(d)
    assert inv["markdown_files"] == 3

    links = check_links(d)
    assert links["counts"]["broken"] == 0

    struct = check_structure(d)
    assert isinstance(struct["issues"], list)

    cl = cluster(corpus, threshold=0.05)
    assert len(cl) >= 1
    # два дрон-файла должны попасть в один кластер
    sizes = sorted(c["size"] for c in cl)
    assert sizes[-1] >= 2

    dups = dedup(corpus)
    assert isinstance(dups, list)

    g = concept_graph(corpus)
    assert len(g["nodes"]) > 0

    h = score(inv, links, struct, dups, cl)
    assert 0 <= h["overall"] <= 100


def test_resolve_paths():
    d = _fixture()
    assert resolve_docs(str(d)) == d.resolve()


def test_slug_transliterates():
    assert _slug(["дрон", "беспилотник"]) == "dron_bespilotnik"
    assert _slug(["the", "это"]) == "misc"  # стопслова → misc


def test_tree_materialize_is_nondestructive():
    d = _fixture()
    prof = Profile(readme_is_content=True, min_tokens=5)
    corpus = load(d, prof)
    cl = cluster(corpus, threshold=0.05)
    plan = plan_tree(corpus, cl, misc_threshold=0)
    assert len(plan) == len(corpus)
    # все dst уникальны
    dsts = [p["dst"] for p in plan]
    assert len(dsts) == len(set(dsts))

    out = Path(tempfile.mkdtemp(prefix="kbtool_tree_"))
    n = materialize(plan, d, out)
    assert n == len(corpus)
    # оригинал цел
    assert (d / "a" / "README.md").exists()
    # копия создана с деревом
    copied = list(out.rglob("*.md"))
    assert len(copied) == len(corpus)


def test_index_search_ask():
    d = _fixture()
    prof = Profile(readme_is_content=True, min_tokens=5)
    idx = build_index(d, prof)
    assert idx["n"] == 3
    assert (d / ".kbtool" / "index.json").exists()
    # round-trip с диска
    idx2 = load_index(d)
    assert idx2 is not None
    # поиск находит дрон-документы
    hits = search(idx2, "TetraDrone Tetra Pak", top_k=2)
    assert len(hits) >= 1
    assert any("дрон" in h.snippet.lower() or "tetra" in h.snippet.lower()
               for h in hits)
    # ответ имеет цитаты
    res = answer(idx2, "что такое TetraDrone")
    assert res["citations"]


def test_semantic_plugin_graceful():
    # без установки sentence-transformers — graceful fallback
    if not semplugin.available():
        assert semplugin.embed_texts(["test"]) is None
        assert semplugin.semantic_search("q", {}) == []
