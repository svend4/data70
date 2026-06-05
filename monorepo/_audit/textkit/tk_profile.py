"""tk_profile.py — слой 2: контентные соглашения репозитория.

Слой 1 (tk_paths.py) решает ГДЕ файлы (пути).
Слой 2 (этот файл) решает КАК устроен контент — соглашения, которые в
исходных lorenzo-скриптах были захардкожены под конкретный репозиторий.

Пример проблемы: improve_clusters.py пропускал файлы README.md, считая их
навигацией. В lorenzo это верно. В data70 README.md = основной контент
каждой темы → пропуск ломал кластеризацию (40 из 220 файлов).

Этот модуль выносит такие соглашения в env-конфигурацию.
"""

from __future__ import annotations

import os

# Файлы, которые скрипты ГЕНЕРИРУЮТ (всегда исключать из анализа)
GENERATED_FILES = {
    "CLUSTERS.md", "TAGS.md", "GLOSSARY.md", "CROSSREFS.md",
    "PRIORITIES.md", "QA.md", "SEARCH.md", "BROKEN_LINKS.md",
    "HEALTH.md", "SCORING.md", "METRICS.md",
}

# Является ли README.md контентом (True для data70) или навигацией (False для lorenzo)
README_IS_CONTENT = os.environ.get("TEXTKIT_README_IS_CONTENT") == "1"

# Минимум токенов, чтобы файл считался содержательным
MIN_TOKENS = int(os.environ.get("TEXTKIT_MIN_TOKENS", "30"))


def skip_files() -> set[str]:
    """Множество имён файлов, которые анализ должен пропускать."""
    skip = set(GENERATED_FILES)
    if not README_IS_CONTENT:
        skip.add("README.md")
    return skip


def describe() -> str:
    return (
        f"README_IS_CONTENT={README_IS_CONTENT}\n"
        f"MIN_TOKENS={MIN_TOKENS}\n"
        f"skip_files={sorted(skip_files())}"
    )


if __name__ == "__main__":
    print(describe())
