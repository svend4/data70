"""Smoke-тест kbtool на временном мини-корпусе."""

import tempfile
from pathlib import Path

from kbtool.paths import resolve_docs
from kbtool.profile import Profile
from kbtool.corpus import load, tokenize
from kbtool.checks import inventory, check_links, check_structure
from kbtool.analyze import cluster, dedup, concept_graph
from kbtool.health import score


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
