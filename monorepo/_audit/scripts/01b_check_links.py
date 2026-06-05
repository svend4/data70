#!/usr/bin/env python3
"""Фаза 1b — Проверка markdown-ссылок.

Парсит все [text](path) во всех .md внутри monorepo/.
Для каждой ссылки проверяет:
- является ли она внутренней (не http/https/mailto)
- разрешается ли путь
- куда указывает (файл, директория, не существует)

Якоря (#section) обрезаются для проверки существования файла.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]  # monorepo/
REPO_ROOT = ROOT.parent  # data70/ (для ссылок наверх в архив)
AUDIT = Path(__file__).resolve().parents[1]
REPORTS = AUDIT / "reports"
QUEUES = AUDIT / "queues"

# [text](url) или [text][ref] — учитываем только первый вид
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


def is_external(url: str) -> bool:
    if url.startswith(("http://", "https://", "mailto:", "ftp://", "tel:")):
        return True
    parsed = urlparse(url)
    return bool(parsed.scheme)


def resolve_link(source_file: Path, url: str) -> tuple[str, Path | None]:
    # обрезаем якорь
    target = url.split("#", 1)[0]
    if not target:
        return "anchor_only", None
    candidate = (source_file.parent / target).resolve()
    if candidate.exists():
        if candidate.is_dir():
            return "directory", candidate
        return "file", candidate
    return "broken", candidate


def main() -> None:
    issues: list[dict] = []
    counts = {
        "files_scanned": 0,
        "links_total": 0,
        "external": 0,
        "internal_file": 0,
        "internal_dir": 0,
        "broken": 0,
        "anchor_only": 0,
    }
    broken_by_file: dict[str, list[dict]] = {}

    for md in sorted(ROOT.rglob("*.md")):
        # пропустить _audit/reports/ — они сгенерированы и могут ссылаться куда угодно
        if "_audit" in md.parts:
            continue
        counts["files_scanned"] += 1
        text = md.read_text(encoding="utf-8", errors="ignore")
        rel = md.relative_to(ROOT)
        for match in LINK_RE.finditer(text):
            text_part, url = match.group(1), match.group(2)
            counts["links_total"] += 1

            if is_external(url):
                counts["external"] += 1
                continue

            status, resolved = resolve_link(md, url)
            status_map = {
                "file": "internal_file",
                "directory": "internal_dir",
                "anchor_only": "anchor_only",
                "broken": "broken",
            }
            counts[status_map.get(status, "broken")] += 1

            if status == "broken":
                rec = {
                    "text": text_part,
                    "url": url,
                    "expected_at": str(resolved) if resolved else None,
                }
                broken_by_file.setdefault(str(rel), []).append(rec)
                issues.append({"file": str(rel), **rec})

    # Отчёт
    md = [
        "# Фаза 1b — Markdown-ссылки",
        "",
        "## Сводка",
        "",
        f"- Просмотрено .md-файлов: **{counts['files_scanned']}**",
        f"- Всего ссылок: **{counts['links_total']}**",
        f"- Внешних (http/mailto/…): **{counts['external']}**",
        f"- Внутренних на файл: **{counts.get('internal_file', 0)}**",
        f"- Внутренних на каталог: **{counts.get('internal_dir', 0)}**",
        f"- Только якорь: **{counts.get('anchor_only', 0)}**",
        f"- Битых: **{counts.get('broken', 0)}**",
        "",
    ]

    if broken_by_file:
        md.append("## Битые ссылки (по файлам)")
        md.append("")
        for fname, recs in sorted(broken_by_file.items()):
            md.append(f"### `{fname}`")
            md.append("")
            md.append("| Текст | URL |")
            md.append("|-------|-----|")
            for r in recs:
                md.append(f"| {r['text'][:50]} | `{r['url']}` |")
            md.append("")
    else:
        md.append("## Битые ссылки")
        md.append("")
        md.append("Не обнаружено.")
        md.append("")

    (REPORTS / "01b_links.md").write_text("\n".join(md), encoding="utf-8")
    (QUEUES / "repair_links.json").write_text(
        json.dumps(issues, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(
        f"[phase_1b] files={counts['files_scanned']} links={counts['links_total']} "
        f"broken={counts.get('broken', 0)}"
    )


if __name__ == "__main__":
    main()
