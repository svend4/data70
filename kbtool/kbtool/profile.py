"""Контентные соглашения корпуса (слой 2).

Разные репо устроены по-разному: где-то README — навигация, где-то — основной
контент. Эти соглашения настраиваются через env или CLI, чтобы инструмент был
универсальным.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field

# Файлы, которые инструмент сам генерирует — всегда исключать из анализа
GENERATED = {
    "CLUSTERS.md", "DUPLICATES.md", "CONCEPTS.md", "HEALTH.md", "REPORT.md",
    "STRUCTURE_AUDIT.md", "LINKS.md", "INVENTORY.md", "kbtool_report.md",
}


@dataclass
class Profile:
    readme_is_content: bool = True
    min_tokens: int = 20
    extra_skip: set[str] = field(default_factory=set)

    @classmethod
    def from_env(cls) -> "Profile":
        return cls(
            readme_is_content=os.environ.get("KBTOOL_README_IS_CONTENT", "1") == "1",
            min_tokens=int(os.environ.get("KBTOOL_MIN_TOKENS", "20")),
        )

    def skip_names(self) -> set[str]:
        skip = set(GENERATED) | set(self.extra_skip)
        if not self.readme_is_content:
            skip.add("README.md")
        return skip
