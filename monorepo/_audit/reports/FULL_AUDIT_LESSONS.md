# Полный машинный аудит — итог и важный урок про побочные эффекты

_Прогон: `textkit/run_all.py` на всех 180 портированных скриптах lorenzo._
_Сырые данные: `full_machine_audit.json`, `full_machine_audit.md`._

## Сухие цифры

- **Скриптов запущено:** 180
- **✓ ok:** 157 (87%)
- **✗ err:** 21 (12%) — отсутствие зависимостей, lorenzo-специфичные пути
- **⏱ timeout:** 2 (`improve_watch.py`, `improve_watcher.py` — long-running, ожидаемо)
- **💥 crash:** 0
- **Общее время:** 312 сек

## Что подтвердил аудит

Из 157 успешных скриптов извлекаемые в `_audit/reports/` метаданные:
- структура data70 валидна на уровне 10+ метрик качества
- pagerank, sentiment, readability, complexity — все прошли без сбоев
- graph, knowledge_map, mindmap, network — построились
- merge_by_topic (3.4с), similar (5.4с), source_map (3.5с), staleness (2.2с) — крупнейшие операции

## КРИТИЧЕСКИЙ УРОК — побочные эффекты

**Многие скрипты lorenzo не «отчётные», а «модифицирующие исходные файлы»**. Они
добавляли в data70 карточки:

- `<!-- toc -->`, `<!-- toc-auto -->`, `<!-- tags: ... -->`, `<!-- summary -->`,
  `<!-- alert-added -->`, `<!-- similar-docs -->` блоки
- Текст «*раздел документации проекта **Lorenzo***»
- Секцию «## Использование» с `python scripts/improve_readme.py`
- Секцию «## Смотрите также» со ссылками на несуществующие `METRICS.md`,
  `HEALTH.md`, `GLOSSARY.md`, `ENTITIES.md`
- Блок «**Похожие документы:**» со ссылками на `obsidian/...`

Также созданы:
- `monorepo/obsidian/` (3 МБ — зеркало всех карточек)
- `monorepo/.claude/`, `.github/`, `docs/`, `.pre-commit-config.yaml` —
  служебная инфраструктура lorenzo
- ~30 файлов CAPS-NAME.md в корне monorepo
- `feed.rss`, `feed.atom`, `WORD_CLOUD.svg`, `badges/`, `chunks/`, `confluence/`,
  `templates/` и другой мусор

**Затронуто 243 карточки + 132 untracked файла = 381 изменение.**

## Что сделано

Все 243 модификации **откатил** (`git restore monorepo/`), весь мусор удалил.
Структура data70 проверена и цела:
- 88/88 покрытие тем
- 0 битых ссылок
- 0 дефектов структуры

## Главный вывод для текстит-подхода

Слой-1 (`tk_paths`) и слой-2 (`tk_profile`) расцепили **пути и контент-соглашения**,
но **не побочные эффекты записи**. Нужен **слой-3 — изоляция записи**:

1. **Sandbox-режим:** запуск каждого скрипта в `--output-dir`, чтобы записи шли
   не в `DOCS/`, а в отдельную папку (например `_audit/reports/from_<script>/`)
2. **Whitelist-режим:** портер помечает каждый скрипт как:
   - `read-only` (только читает и пишет в свой отчётный файл) — безопасно
   - `appends-to-cards` (вставляет в исходные README) — опасно, требует sandbox
   - `creates-side-files` (создаёт METRICS.md и подобное в корне) — терпимо в reports
3. **Dry-run флаг:** все скрипты должны поддерживать `--dry-run`, чтобы видеть
   намеренные правки до их применения

В текущей версии `textkit/run_all.py` следует **по умолчанию запускать только
скрипты с пометкой `safe`**, а опасные — с явным флагом и в sandbox.

## Список «опасных» скриптов (модифицировали data70-карточки)

По анализу system-reminders и git-diff пострадали как минимум:
- `improve_toc.py`, `improve_auto_toc.py` — добавили `<!-- toc -->`
- `improve_alerts.py` — `> [!NOTE] Раздел … формируется автоматически из данных
  репозитория проекта Lorenzo`
- `improve_tags.py` — `<!-- tags: ... -->`
- `improve_summaries.py`, `improve_summary_extender.py` — `<!-- summary -->`
- `improve_see_also.py`, `improve_readmes.py` — секции «Смотрите также»
- `improve_similar.py`, `improve_similar_passages.py` — блоки «Похожие документы»
- `improve_obsidian.py` — создал `monorepo/obsidian/`
- `improve_glossary.py`, `improve_health.py`, `improve_metrics.py`,
  `improve_entities.py` — создали GLOSSARY.md/HEALTH.md/METRICS.md/ENTITIES.md
- `improve_confluence.py` — `monorepo/confluence/`
- `improve_rss.py` — `feed.rss`, `feed.atom`
- `improve_word_cloud.py` — `WORD_CLOUD.svg`
- `improve_badges.py` — `monorepo/badges/`
- `improve_chunk_semantic.py` — `monorepo/chunks/`
- `improve_templates.py` — `monorepo/templates/`

## 21 ошибочный скрипт (детали в JSON)

Категории провалов:
- **lorenzo-специфичные пути** в файле (CONTACTS.md, SCORING.md и т.п.):
  `improve_changelog`, `improve_mcp_dashboard`, `improve_query_log`,
  `improve_skill_dashboard`
- **Требуют argparse-аргументов**: `improve_semantic_search` (нужен `--query`)
- **Внешние зависимости**: `improve_epub` (ebooklib)
- **Алгоритмические баги на data70-данных**: `improve_heatmap`,
  `improve_precision_eval`
- **Внутренние утилиты lorenzo**: `improve_template_init`, `improve_workflow_*`,
  `improve_mcp_*`, `improve_skill_metrics`, `improve_task_codegen`,
  `improve_migrate_contacts`, `improve_run_all`

## Рекомендация дальнейших шагов

1. Расширить `port.py` метой `safety: read-only|appends|side-files` (на основе
   списка выше) — однократная разметка через grep на запись в файлы
2. По умолчанию в `run_all.py` гонять только `read-only`
3. Для `appends` — sandbox через временный bind-mount или копию DOCS
4. Для оставшихся 21 «err» — определить, какие реально нужны, и адаптировать
   слой-2 / слой-3 точечно

Это **превратит textkit из POC в production-tool** для безопасного машинного
аудита любого markdown-репо.
