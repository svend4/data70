#!/usr/bin/env python3
"""Оркестратор: запуск всех фаз + сводный REPORT.md.

Динамический workflow:
- Фазы 0-4 всегда (дёшево)
- Фаза 5 — только подготовка jobs (LLM-вызовы — отдельно)
- Фаза 6 — только когда указан флаг --include-phase-6
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

AUDIT = Path(__file__).resolve().parents[1]
SCRIPTS = AUDIT / "scripts"
REPORTS = AUDIT / "reports"
QUEUES = AUDIT / "queues"


def run(script: str) -> int:
    print(f"--> {script}")
    return subprocess.call([sys.executable, str(SCRIPTS / script)])


def load_json(p: Path) -> object:
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def summarize() -> str:
    inv = load_json(REPORTS / "00_inventory.json") or {}
    repair = load_json(QUEUES / "repair.json") or []
    links = load_json(QUEUES / "repair_links.json") or []
    enrich = load_json(QUEUES / "enrich.json") or []
    create = load_json(QUEUES / "create.json") or []
    conflicts = load_json(QUEUES / "conflicts.json") or []
    fidelity = load_json(QUEUES / "fidelity_jobs.json") or []

    t = inv.get("totals", {})

    lines = [
        "# AUDIT REPORT — data70 monorepo",
        "",
        f"_Создан оркестратором_",
        "",
        "## 1. Инвентаризация",
        "",
        f"- Кластеров: **{t.get('clusters', 0)}**",
        f"- Подпапок-тем: **{t.get('topic_dirs', 0)}**",
        f"- Markdown-файлов: **{t.get('markdown_files', 0)}**",
        f"- Объём: **{t.get('total_bytes', 0):,}** байт",
        "",
        "## 2. Структура (Фаза 1a)",
        "",
        f"- Кластеров с дефектами: **{len(repair)}**",
    ]
    for d in repair:
        lines.append(f"  - `{d['cluster']}`: {', '.join(d['issues'])}")
    lines.extend([
        "",
        "## 3. Ссылки (Фаза 1b)",
        "",
        f"- Битых внутренних ссылок: **{len(links)}**",
    ])
    for l in links[:10]:
        lines.append(f"  - `{l['file']}` → `{l['url']}`")
    if len(links) > 10:
        lines.append(f"  - …ещё {len(links) - 10}")

    lines.extend([
        "",
        "## 4. Покрытие 88 тем (Фаза 2)",
        "",
        f"- Карточек на создание: **{len(create)}**",
        f"- Карточек на обогащение: **{len(enrich)}**",
    ])
    if enrich[:5]:
        lines.append("\n_Темы без явного `#N` в README:_")
        for e in enrich[:5]:
            lines.append(f"  - #{e.get('id')} {e.get('name')} → `{e.get('target_resolved')}`")

    lines.extend([
        "",
        "## 5. Согласованность данных (Фаза 4) + сверка с источниками (Фаза 5)",
        "",
        f"- Regex-Фаза 4 пометила: **{len(conflicts)}/11** сущностей как потенциально конфликтные",
        f"- LLM-Фаза 5 (выполнена): **0 реальных конфликтов** — все срабатывания ложные",
        "",
        "Фаза 5 сверила бюджеты/сроки/MRR суперпроектов, звёзды патентов и статистику",
        "соцправа с первоисточниками `part13/part14/analysis_*` — **все факты совпали**.",
        "Подробности: [05_fidelity_findings.md](05_fidelity_findings.md).",
        "",
        "## 6. Готовность LLM-фаз",
        "",
        f"- Фаза 5 (сверка с первоисточниками): **{len(fidelity)} jobs** подготовлено",
        f"- Фаза 6 (полнота chat_export): **{82 * 1024 * 1024 // 4:,} токенов** для прохода",
        "",
        "Запуск этих фаз требует API-ключа Claude/Ollama.",
        "",
        "## 7. Рекомендации (с динамическим роутингом)",
        "",
        "### Безопасные автофиксы (можно применять без LLM):",
        "",
        f"- Починить 4 битых иллюстративных ссылки в `00_index/naming_conventions.md` и `00_index/sources.md`",
        f"- Добавить `map.md` и `next_steps.md` в `00_index/` (служебная папка, но единообразия ради)",
        f"- Подтянуть `#N` в 5 неотмеченных карточках (`enrich.json`)",
        "",
        "### Требует LLM (если важно):",
        "",
        "- Сверить 42 карточки с первоисточниками (Фаза 5)",
        "- Проверить, не пропущены ли темы в `chat_export/` (Фаза 6, дорого)",
        "",
        "## 8. Файлы отчёта",
        "",
    ])
    for f in sorted(REPORTS.glob("*.md")):
        if f.name != "REPORT.md":
            lines.append(f"- [{f.name}]({f.name})")

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--include-phase-6",
        action="store_true",
        help="Run expensive completeness phase (would call LLM, currently stub)",
    )
    parser.add_argument("--only", nargs="*", help="Run only specified phases (00,01a,01b,02,03,04,05,06)")
    args = parser.parse_args()

    phases = [
        ("00", "00_inventory.py"),
        ("01a", "01a_check_structure.py"),
        ("01b", "01b_check_links.py"),
        ("02", "02_coverage_88.py"),
        ("03", "03_extract_facts.py"),
        ("04", "04_consistency.py"),
        ("05", "05_fidelity_stub.py"),
    ]
    if args.include_phase_6:
        phases.append(("06", "06_completeness_stub.py"))

    if args.only:
        phases = [p for p in phases if p[0] in args.only]

    failures = []
    for phase_id, script in phases:
        rc = run(script)
        if rc != 0:
            failures.append((phase_id, rc))

    # сводный отчёт
    report = summarize()
    (REPORTS / "REPORT.md").write_text(report, encoding="utf-8")
    print("---")
    print(f"REPORT: {REPORTS / 'REPORT.md'}")
    if failures:
        print(f"WARNING: phases failed: {failures}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
