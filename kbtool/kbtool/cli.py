"""kbtool CLI — единая точка входа.

Команды:
  kbtool inventory <path>   — статистика корпуса
  kbtool links <path>       — проверка markdown-ссылок
  kbtool structure <path>   — проверка наличия README в папках
  kbtool cluster <path>     — TF-IDF кластеризация по темам (newsgroups)
  kbtool dedup <path>       — поиск дублирующихся абзацев
  kbtool concepts <path>    — концепт-граф
  kbtool health <path>      — агрегированный health-балл
  kbtool all <path>         — всё сразу + единый отчёт

Опции:
  -o, --out FILE        куда писать отчёт (по умолчанию <path>/kbtool_report.md)
  --readme-nav          считать README навигацией, а не контентом
  --threshold FLOAT     порог кластеризации (по умолч. 0.15)
  --json                машинный вывод
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .paths import resolve_docs
from .profile import Profile
from .corpus import load
from .checks import inventory, check_links, check_structure
from .analyze import cluster, dedup, concept_graph
from .health import score
from .tree import plan_tree, render_plan, materialize, apply_inplace
from .rag import build_index, load_index, search, answer, index_path
from .watch import watch
from .server import serve
from . import semantic as semplugin


def _profile(args) -> Profile:
    p = Profile.from_env()
    if getattr(args, "readme_nav", False):
        p.readme_is_content = False
    return p


def _emit(args, data: dict, md: str, default_name: str):
    if getattr(args, "json", False):
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    print(md)


def cmd_inventory(args):
    docs = resolve_docs(args.path)
    inv = inventory(docs)
    md = (f"# Инвентаризация\n\n- Корень: `{inv['root']}`\n"
          f"- Markdown-файлов: {inv['markdown_files']}\n"
          f"- Байт: {inv['total_bytes']:,}\n- Строк: {inv['total_lines']:,}\n"
          f"- Папок верхнего уровня: {len(inv['top_level_dirs'])}\n")
    _emit(args, inv, md, "inventory")


def cmd_links(args):
    docs = resolve_docs(args.path)
    res = check_links(docs)
    c = res["counts"]
    md = (f"# Ссылки\n\n- Файлов: {c['files']}, ссылок: {c['links']}, "
          f"внешних: {c['external']}, ок: {c['ok']}, **битых: {c['broken']}**\n")
    for b in res["broken"][:50]:
        md += f"\n- `{b['file']}` → `{b['url']}`"
    _emit(args, res, md, "links")


def cmd_structure(args):
    docs = resolve_docs(args.path)
    res = check_structure(docs)
    md = (f"# Структура\n\n- Папок проверено: {res['checked']}, "
          f"**проблем: {len(res['issues'])}**\n")
    for i in res["issues"][:50]:
        md += f"\n- `{i['dir']}`: нет {', '.join(i['missing'])}"
    _emit(args, res, md, "structure")


def cmd_cluster(args):
    docs = resolve_docs(args.path)
    corpus = load(docs, _profile(args), exclude_dirs=set(getattr(args, "exclude", [])))
    cl = cluster(corpus, threshold=args.threshold)
    md = f"# Кластеры ({len(cl)})\n\nДокументов: {len(corpus)}\n"
    for i, c in enumerate(cl[:60], 1):
        md += f"\n## {i}. {c['label']} ({c['size']})\n"
        for f in c["files"][:12]:
            md += f"- {f}\n"
    _emit(args, {"docs": len(corpus), "clusters": cl}, md, "clusters")


def cmd_dedup(args):
    docs = resolve_docs(args.path)
    corpus = load(docs, _profile(args), exclude_dirs=set(getattr(args, "exclude", [])))
    pairs = dedup(corpus)
    md = f"# Дубликаты\n\nДокументов: {len(corpus)}, **похожих пар: {len(pairs)}**\n"
    for p in pairs[:50]:
        md += f"\n- `{p['a']}` ↔ `{p['b']}` (Jaccard {p['jaccard']})"
    _emit(args, {"pairs": pairs}, md, "dedup")


def cmd_concepts(args):
    docs = resolve_docs(args.path)
    corpus = load(docs, _profile(args), exclude_dirs=set(getattr(args, "exclude", [])))
    g = concept_graph(corpus)
    md = (f"# Концепт-граф\n\nУзлов: {len(g['nodes'])}, рёбер: {len(g['edges'])}\n"
          f"Топ-концепты: {', '.join(g['top'])}\n")
    _emit(args, g, md, "concepts")


def cmd_health(args):
    docs = resolve_docs(args.path)
    prof = _profile(args)
    excl = set(getattr(args, "exclude", []))
    corpus = load(docs, prof, exclude_dirs=excl)
    inv = inventory(docs, excl)
    links = check_links(docs, excl)
    struct = check_structure(docs, exclude=excl)
    dups = dedup(corpus)
    cl = cluster(corpus, threshold=args.threshold)
    h = score(inv, links, struct, dups, cl)
    md = f"# Health: {h['overall']}/100\n\n| Метрика | Значение | Балл |\n|---|---|---|\n"
    for name, val, sc in h["metrics"]:
        md += f"| {name} | {val} | {sc} |\n"
    _emit(args, h, md, "health")


def cmd_all(args):
    docs = resolve_docs(args.path)
    prof = _profile(args)
    excl = set(getattr(args, "exclude", []))
    corpus = load(docs, prof, exclude_dirs=excl)
    inv = inventory(docs, excl)
    links = check_links(docs, excl)
    struct = check_structure(docs, exclude=excl)
    dups = dedup(corpus)
    cl = cluster(corpus, threshold=args.threshold)
    g = concept_graph(corpus)
    h = score(inv, links, struct, dups, cl)

    md = [f"# kbtool отчёт — {docs}", "",
          f"_kbtool v{__version__}_", "",
          "## Health",
          f"**{h['overall']}/100**", "",
          "| Метрика | Значение | Балл |", "|---|---|---|"]
    for name, val, sc in h["metrics"]:
        md.append(f"| {name} | {val} | {sc} |")
    md += ["", "## Инвентаризация",
           f"- Файлов: {inv['markdown_files']}, байт: {inv['total_bytes']:,}, "
           f"папок: {len(inv['top_level_dirs'])}",
           "", "## Ссылки",
           f"- Битых: {links['counts']['broken']} из {links['counts']['links']}",
           "", "## Структура",
           f"- Проблем: {len(struct['issues'])}",
           "", "## Дубликаты",
           f"- Похожих пар: {len(dups)}",
           "", f"## Кластеры ({len(cl)})"]
    for i, c in enumerate(cl[:40], 1):
        md.append(f"{i}. **{c['label']}** ({c['size']})")
    md += ["", "## Концепт-граф",
           f"- Узлов: {len(g['nodes'])}, рёбер: {len(g['edges'])}",
           f"- Топ: {', '.join(g['top'])}", ""]

    report = "\n".join(md) + "\n"
    # По умолчанию отчёт пишем в CWD, НЕ в корпус (без побочных эффектов на репо)
    out = Path(args.out) if args.out else (Path.cwd() / "kbtool_report.md")
    out.write_text(report, encoding="utf-8")
    print(f"Health: {h['overall']}/100  |  файлов: {inv['markdown_files']}  |  "
          f"кластеров: {len(cl)}  |  битых ссылок: {links['counts']['broken']}  |  "
          f"дублей: {len(dups)}")
    print(f"Отчёт: {out}")


def cmd_tree(args):
    docs = resolve_docs(args.path)
    prof = _profile(args)
    excl = set(getattr(args, "exclude", []))
    corpus = load(docs, prof, exclude_dirs=excl)
    cl = cluster(corpus, threshold=args.threshold)
    plan = plan_tree(corpus, cl, misc_threshold=args.misc_threshold)

    if getattr(args, "json", False):
        print(json.dumps({"plan": plan}, ensure_ascii=False, indent=2))
        return

    # Режим 1: материализовать копию (безопасно)
    if args.out:
        n = materialize(plan, docs, Path(args.out))
        print(f"Скопировано {n} файлов в новое дерево: {args.out}")
        print(f"Оригинал {docs} НЕ изменён.")
        # план рядом
        (Path(args.out) / "_TREE_PLAN.md").write_text(render_plan(plan), encoding="utf-8")
        return

    # Режим 2: применить in-place (деструктивно)
    if args.apply:
        print(f"⚠ ВНИМАНИЕ: будет перемещено {len(plan)} файлов IN-PLACE в {docs}")
        if not args.yes:
            print("Добавьте --yes для подтверждения. Сейчас показан только план:")
            print(render_plan(plan))
            return
        n = apply_inplace(plan, docs, use_git=not args.no_git)
        print(f"Перемещено {n} файлов in-place. Проверьте git status.")
        return

    # Режим 3 (по умолчанию): dry-run
    print(render_plan(plan))
    print(f"\n[dry-run] Ничего не перемещено. Используйте:")
    print(f"  --out DIR   материализовать копию (безопасно)")
    print(f"  --apply --yes  переместить in-place (деструктивно)")


def cmd_index(args):
    docs = resolve_docs(args.path)
    excl = set(getattr(args, "exclude", []))
    idx = build_index(docs, _profile(args), excl)
    print(f"Индекс построен: {len(idx['docs'])} документов → {index_path(docs)}")


def cmd_search(args):
    docs = resolve_docs(args.path)
    idx = load_index(docs)
    if idx is None:
        print("Индекс не найден. Запустите: kbtool index <path>")
        return
    hits = search(idx, args.query, top_k=args.k, method=args.method)
    if getattr(args, "json", False):
        print(json.dumps([h.__dict__ for h in hits], ensure_ascii=False, indent=2))
        return
    for i, h in enumerate(hits, 1):
        print(f"\n[{i}] {h.title}  (score {h.score})")
        print(f"    {h.doc_id}")
        print(f"    {h.snippet[:200]}…")


def cmd_ask(args):
    docs = resolve_docs(args.path)
    idx = load_index(docs)
    if idx is None:
        print("Индекс не найден. Запустите: kbtool index <path>")
        return
    res = answer(idx, args.query, top_k=args.k)
    if getattr(args, "json", False):
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return
    print(f"# {res['question']}\n\n{res['answer']}\n\n## Источники")
    for c in res["citations"]:
        print(f"  [{c['n']}] {c['title']}  ({c['doc_id']}, score {c['score']})")


def cmd_watch(args):
    docs = resolve_docs(args.path)
    prof = _profile(args)
    excl = set(getattr(args, "exclude", []))

    def on_change(added, modified, removed):
        from datetime import datetime
        ts = datetime.now().strftime("%H:%M:%S")
        delta = (f"+{len(added)} ~{len(modified)} -{len(removed)}")
        # пересчёт health
        corpus = load(docs, prof, exclude_dirs=excl)
        inv = inventory(docs, excl); links = check_links(docs, excl)
        struct = check_structure(docs, exclude=excl)
        dups = dedup(corpus); cl = cluster(corpus, threshold=args.threshold)
        h = score(inv, links, struct, dups, cl)
        print(f"[{ts}] {delta}  health={h['overall']}/100  links_broken={links['counts']['broken']}")
        if args.reindex:
            build_index(docs, prof, excl)
            print(f"           индекс обновлён")

    watch(docs, excl, on_change, interval=args.interval)


def cmd_serve(args):
    docs = resolve_docs(args.path)
    prof = _profile(args)
    excl = set(getattr(args, "exclude", []))
    serve(docs, args.port, excl, prof)


def cmd_semantic(args):
    print("semantic-плагин:")
    print(f"  установлен: {semplugin.available()}")
    if not semplugin.available():
        print("  pip install kbtool[semantic]   # добавит sentence-transformers")
        return
    docs = resolve_docs(args.path)
    prof = _profile(args)
    excl = set(getattr(args, "exclude", []))
    corpus = load(docs, prof, exclude_dirs=excl)
    print(f"  Строю эмбеддинги для {len(corpus)} документов…")
    vecs = semplugin.embed_texts([d.text[:2000] for d in corpus])
    if not vecs:
        print("  Не удалось построить эмбеддинги.")
        return
    out = docs / ".kbtool" / "embeddings.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(
        {d.rel: v for d, v in zip(corpus, vecs)}, ensure_ascii=False
    ), encoding="utf-8")
    print(f"  Сохранено: {out}")


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="kbtool",
                                 description="Переносимый аудит и структурирование больших хаотичных markdown-баз")
    ap.add_argument("--version", action="version", version=f"kbtool {__version__}")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p):
        p.add_argument("path", nargs="?", default=None, help="путь к корпусу (или env KBTOOL_DOCS)")
        p.add_argument("--readme-nav", action="store_true", help="README — навигация, не контент")
        p.add_argument("--threshold", type=float, default=0.15, help="порог кластеризации")
        p.add_argument("--exclude", nargs="*", default=[], help="имена папок-исключений (напр. _audit node_modules)")
        p.add_argument("--json", action="store_true", help="машинный вывод")
        p.add_argument("-o", "--out", default=None, help="файл отчёта (для all)")

    for name, fn in [("inventory", cmd_inventory), ("links", cmd_links),
                     ("structure", cmd_structure), ("cluster", cmd_cluster),
                     ("dedup", cmd_dedup), ("concepts", cmd_concepts),
                     ("health", cmd_health), ("all", cmd_all)]:
        p = sub.add_parser(name)
        common(p)
        p.set_defaults(func=fn)

    # tree — отдельные опции (реорганизация)
    pt = sub.add_parser("tree", help="разложить хаос в дерево по темам")
    common(pt)
    pt.add_argument("--apply", action="store_true", help="переместить in-place (деструктивно)")
    pt.add_argument("--yes", action="store_true", help="подтвердить --apply")
    pt.add_argument("--no-git", action="store_true", help="не использовать git mv")
    pt.add_argument("--misc-threshold", type=int, default=1,
                    help="кластеры размера <= N идут в 00_misc/")
    pt.set_defaults(func=cmd_tree)

    # index — построить поисковый индекс
    pi = sub.add_parser("index", help="построить поисковый индекс корпуса")
    common(pi)
    pi.set_defaults(func=cmd_index)

    # search — найти документы
    ps = sub.add_parser("search", help="поиск по корпусу")
    common(ps)
    ps.add_argument("query", help="ключевые слова")
    ps.add_argument("-k", type=int, default=5)
    ps.add_argument("--method", choices=["bm25", "keyword"], default="bm25")
    ps.set_defaults(func=cmd_search)

    # ask — вопросно-ответный режим
    pa = sub.add_parser("ask", help="ответ с цитатами по корпусу")
    common(pa)
    pa.add_argument("query", help="вопрос")
    pa.add_argument("-k", type=int, default=5)
    pa.set_defaults(func=cmd_ask)

    # watch — инкрементальный re-audit
    pw = sub.add_parser("watch", help="следить за изменениями, пересчитывать health")
    common(pw)
    pw.add_argument("--interval", type=float, default=2.0)
    pw.add_argument("--reindex", action="store_true", help="перестраивать индекс при изменениях")
    pw.set_defaults(func=cmd_watch)

    # serve — HTTP-дашборд
    psrv = sub.add_parser("serve", help="HTTP-дашборд health + поиск")
    common(psrv)
    psrv.add_argument("--port", type=int, default=8765)
    psrv.set_defaults(func=cmd_serve)

    # semantic — опциональный плагин
    psem = sub.add_parser("semantic", help="опциональные эмбеддинги (sentence-transformers)")
    common(psem)
    psem.set_defaults(func=cmd_semantic)

    return ap


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
