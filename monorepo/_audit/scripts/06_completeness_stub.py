#!/usr/bin/env python3
"""Фаза 6 — Полнота chat_export/ (заглушка).

Самая дорогая фаза: пересканировать 79 МБ оригинальных разговоров
и проверить, не пропустили ли мы темы.

В этой версии — только статистика готовности к запуску.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
AUDIT = Path(__file__).resolve().parents[1]
REPORTS = AUDIT / "reports"


def main() -> None:
    chat_dir = REPO_ROOT / "chat_export"
    files = sorted(chat_dir.glob("chat_export_*.txt")) if chat_dir.exists() else []
    total_bytes = sum(f.stat().st_size for f in files)

    # Базовая статистика: сколько примерно токенов
    # ~4 символа на токен в среднем для рус/нем/анг смеси
    approx_tokens = total_bytes // 4

    md = [
        "# Фаза 6 — Полнота сканирования chat_export/",
        "",
        "## Сводка",
        "",
        f"- Файлов экспорта: **{len(files)}**",
        f"- Объём: **{total_bytes:,}** байт ({total_bytes / 1024 / 1024:.1f} МБ)",
        f"- Примерно токенов (LLM): **~{approx_tokens:,}**",
        "",
        "## Оценка стоимости полного прохода",
        "",
        "| Модель | Цена за 1M токенов | Стоимость прохода |",
        "|--------|--------------------|-------------------|",
        f"| Haiku 4.5 (вход) | $1 | ~${approx_tokens / 1_000_000:.2f} |",
        f"| Sonnet 4.6 (вход) | $3 | ~${approx_tokens / 1_000_000 * 3:.2f} |",
        f"| Opus 4.7/4.8 (вход) | $15 | ~${approx_tokens / 1_000_000 * 15:.2f} |",
        "",
        "## Стратегия запуска (когда нужно)",
        "",
        "1. **Map-reduce**: чанкуем каждый файл по 30K токенов",
        "2. **Map**: дешёвый Haiku → извлекает темы + суть каждого разговора",
        "3. **Reduce**: Sonnet → группирует похожие темы, мерджит с существующими 88",
        "4. **Diff**: сравниваем с catalog_88_topics.md → видим, что новое",
        "5. **Sample QA**: Opus → проверяет 10% результатов как контроль качества",
        "",
        "Полный проход — €40-100 в зависимости от модели.",
        "Уменьшение стоимости: prompt caching (90% скидка на повторные чанки).",
        "",
        "## Не запущено",
        "",
        "Эта фаза требует явного разрешения и API-ключа. Использовать `run_all.py --include-phase-6`.",
    ]

    (REPORTS / "06_completeness.md").write_text("\n".join(md), encoding="utf-8")
    print(f"[phase_6] chat_files={len(files)} bytes={total_bytes:,} llm_calls=0 (stub)")


if __name__ == "__main__":
    main()
