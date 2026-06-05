#!/usr/bin/env python3
"""Фаза 5 — Сверка с первоисточниками (заглушка для LLM-фазы).

Динамически выбирает файлы для проверки на основе очередей из предыдущих фаз
(repair, enrich, conflicts). Для каждого подбирает соответствующий первоисточник
в корне репозитория (analysis_*.md, part*.md) и формирует промпт для LLM.

В этой версии: только подготовка работы. Реальные LLM-вызовы — в TODO.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = ROOT.parent
AUDIT = Path(__file__).resolve().parents[1]
REPORTS = AUDIT / "reports"
QUEUES = AUDIT / "queues"

# Маппинг кластера → первоисточник
SOURCE_MAP = {
    "01_social_law": ["analysis_04_social_law.md"],
    "02_ai_agents": ["analysis_ai_topics.md", "part10_deep_analysis.md", "part10_new_topics.md"],
    "03_drones_skymediahub": ["analysis_02_top_projects.md", "analysis_03_inventions.md"],
    "04_robotics_caremate": ["analysis_02_top_projects.md", "analysis_03_inventions.md"],
    "05_software_automation": ["analysis_02_top_projects.md", "part13_tech_stacks.md"],
    "06_business_funding": ["analysis_05_recommendations.md", "part14_business_models.md"],
    "07_inventions_patents": ["analysis_03_inventions.md"],
    "08_knowledge_methodology": ["part11_connections.md"],
    "09_media_newsroom": ["part10_new_topics.md"],
    "10_health_accessibility": ["analysis_04_social_law.md", "analysis_02_top_projects.md"],
    "superprojects": ["part11_connections.md", "part13_tech_stacks.md", "part14_business_models.md"],
}


def cluster_of(path: str) -> str | None:
    """monorepo/01_social_law/X/README.md → 01_social_law"""
    parts = Path(path).parts
    for p in parts:
        if "_" in p and p[:2].isdigit():
            return p
        if p in {"superprojects", "88_topics_full", "99_archive_links"}:
            return p
    return None


def build_jobs() -> list[dict]:
    jobs: list[dict] = []

    # Загружаем очереди (могут не существовать, если фазы не запускались)
    flagged_paths: set[str] = set()

    for queue_name in ["enrich.json", "create.json", "conflicts.json"]:
        qpath = QUEUES / queue_name
        if not qpath.exists():
            continue
        data = json.loads(qpath.read_text(encoding="utf-8"))
        for item in data:
            # очереди разной формы; вытаскиваем file/target
            for key in ("file", "target_resolved", "path"):
                if key in item and isinstance(item[key], str):
                    flagged_paths.add(item[key])
                    break

    # Также добавляем сущности с конфликтами
    conflicts_path = QUEUES / "conflicts.json"
    if conflicts_path.exists():
        conflicts = json.loads(conflicts_path.read_text(encoding="utf-8"))
        for c in conflicts:
            # сущность → 3-5 показательных файлов
            ent = c["entity"]
            picks = set()
            for cluster_c in c.get("conflicts", []):
                for cl in cluster_c["clusters"][:3]:
                    for f in cl["files"][:2]:
                        picks.add(f)
            for f in picks:
                flagged_paths.add(f)

    for f in sorted(flagged_paths):
        cluster = cluster_of(f)
        sources = SOURCE_MAP.get(cluster or "", [])
        jobs.append({
            "card": f,
            "cluster": cluster,
            "primary_sources": sources,
            "llm_prompt_template": (
                "Сравни карточку `{card}` с первоисточниками: {sources}.\n"
                "Проверь:\n"
                "1) Не выдумано ли число/факт, отсутствующий в источнике?\n"
                "2) Совпадает ли заявленный приоритет / бюджет / срок?\n"
                "3) Нет ли важной информации из источника, упущенной в карточке?\n"
                "Верни структурированный JSON: {{distortions: [], omissions: [], confirmations: []}}."
            ),
        })

    return jobs


def main() -> None:
    jobs = build_jobs()
    (QUEUES / "fidelity_jobs.json").write_text(
        json.dumps(jobs, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    md = [
        "# Фаза 5 — Сверка с первоисточниками (заглушка)",
        "",
        "## Сводка",
        "",
        f"- Файлов на проверку: **{len(jobs)}**",
        "- LLM-вызовы: не выполнены (требуется ключ Claude/Ollama)",
        "",
        "## Стратегия",
        "",
        "Когда будет настроен LLM:",
        "1. Берём по 5-10 jobs за раз (батч)",
        "2. Дешёвый Llama-роутинг: тривиальные совпадения отметить сразу",
        "3. Spot-check через Claude Sonnet на 20% выборки",
        "4. Opus — только для критичных (юр., патенты, мед.)",
        "",
        "## Подготовлено jobs",
        "",
        "| Карточка | Кластер | Источников |",
        "|----------|---------|----------:|",
    ]
    for j in jobs[:40]:
        md.append(f"| `{j['card']}` | {j['cluster']} | {len(j['primary_sources'])} |")
    if len(jobs) > 40:
        md.append(f"\n_…ещё {len(jobs) - 40} — см. queues/fidelity_jobs.json_")

    (REPORTS / "05_fidelity.md").write_text("\n".join(md), encoding="utf-8")
    print(f"[phase_5] jobs_prepared={len(jobs)} llm_calls=0 (stub)")


if __name__ == "__main__":
    main()
