# Полный машинный аудит data70 — все портированные lorenzo-инструменты

- Корпус: `/home/user/data70/monorepo`
- README=контент: True
- Скриптов запущено: **180**
- ✓ ok: **157**  ✗ err: **21**  ⏱ timeout: **2**  💥 crash: **0**
- Общее время: 312.1 сек

## Скрипты с ошибками

| Скрипт | Статус | rc | Последние строки stderr |
|--------|--------|---:|--------------------------|
| `improve_benchmark.py` | err | 1 |  |
| `improve_changelog.py` | err | 1 |          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ /   File "/usr/lib/python3.11/pathlib.py", line 1044, in open /     return io.op |
| `improve_epub.py` | err | 1 |  |
| `improve_heatmap.py` | err | 1 |                                 ^ /   File "/home/user/data70/monorepo/_audit/textkit/lib/improve_heatmap.py", line 78, in <dictcomp> /     topic: max(matrix[to |
| `improve_hot_cards.py` | err | 1 |  |
| `improve_mcp_dashboard.py` | err | 1 |          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ /   File "/usr/lib/python3.11/pathlib.py", line 1044, in open /     return io.op |
| `improve_mcp_test.py` | err | 1 |  |
| `improve_migrate_contacts.py` | err | 1 |  |
| `improve_precision_eval.py` | err | 1 |  |
| `improve_query_log.py` | err | 1 |          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ /   File "/usr/lib/python3.11/pathlib.py", line 1044, in open /     return io.op |
| `improve_run_all.py` | err | 1 |  |
| `improve_semantic_search.py` | err | 2 | usage: improve_semantic_search.py [-h] --query ТЕКСТ /                                   [--mode {hybrid,semantic,bm25,full}] /                                  |
| `improve_skill_dashboard.py` | err | 1 |          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ /   File "/usr/lib/python3.11/pathlib.py", line 1044, in open /     return io.op |
| `improve_skill_metrics.py` | err | 1 |  |
| `improve_task_codegen.py` | err | 1 |  |
| `improve_template_init.py` | err | 1 |  |
| `improve_template_integrity.py` | err | 1 |  |
| `improve_template_migrate.py` | err | 1 |  |
| `improve_validate_templates.py` | err | 1 |  |
| `improve_watch.py` | timeout | -1 | TIMEOUT |
| `improve_watcher.py` | timeout | -1 | TIMEOUT |
| `improve_workflow_run.py` | err | 1 |  |
| `improve_workflow_v2.py` | err | 1 |  |

## Успешные скрипты (топ-30 по длительности)

| Скрипт | Время (с) | Последние строки stdout |
|--------|----------:|--------------------------|
| `improve_link_preview.py` | 19.918 |    Проверено новых: 14 /   wrote: monorepo/LINK_PREVIEW.md /   ✅ 7 \| 🔄 0 \| ❌ 7 |
| `improve_similar.py` | 5.411 | Поиск похожих документов... /   wrote: monorepo/SIMILAR.md /   похожих пар: 1268, обновлено файлов: 623 |
| `improve_source_map.py` | 3.506 |   wrote: monorepo/SOURCE_MAP.md /   категории: {'✍️ Ручной': 632} /   авторов: 3 |
| `improve_merge_by_topic.py` | 3.399 |  /   Было бы объединено ~79,371 слов в 12 файлов /   Запустите с --apply для реального слияния. |
| `improve_github_tracker.py` | 3.11 | Найдено событий: 0 /  / ℹ️  Запустите с --apply чтобы создать карточки (0 новых) |
| `improve_staleness.py` | 2.185 | 🕰  improve_staleness.py — поиск устаревших документов (порог: 30д) /   wrote: monorepo/STALENESS.md /   устаревших: 213, без метаданных: 316, коротких: 3 |
| `improve_similar_passages.py` | 1.546 |   wrote: monorepo/SIMILAR_PASSAGES.md /   похожих пар: 2138 /   топ сходство: 1.0 |
| `improve_named_entity_index.py` | 1.115 |   🏢 orgs: 6 /   👤 people: 6 /   📅 dates: 5 |
| `improve_subtopic_fill.py` | 0.978 |  /   Будет дополнено: 13 файлов  \|  Пропущено: 0 /   Запустите с --apply для реальной записи. |
| `improve_entities.py` | 0.946 | Извлечение именованных сущностей... /   wrote: monorepo/ENTITIES.md /   людей: 4, проектов: 19, орг: 8, технологий: 24, GitHub URL: 4 |
| `improve_abbreviations.py` | 0.729 | Словарь аббревиатур... /   wrote: monorepo/ABBREVIATIONS.md /   аббревиатур: 51 |
| `improve_consistency.py` | 0.704 | Проверка согласованности терминов... /   wrote: monorepo/CONSISTENCY.md /   проблем найдено: 3 |
| `improve_missing.py` | 0.687 | Анализ пробелов в документации... /   wrote: monorepo/MISSING.md /   ✅ 13  ⚠️ 5  ❌ 7 |
| `improve_contradiction_check.py` | 0.683 |  /   wrote: monorepo/CONTRADICTIONS.md /   противоречий: 220 |
| `improve_concepts.py` | 0.648 | Извлечение определений понятий... /   wrote: monorepo/CONCEPTS.md /   понятий: 549 |
| `improve_sentinel_check.py` | 0.619 |   wrote: monorepo/SENTINEL.md /   PII: 4, код: 0, creds: 0, HTTP: 21, лицензии: 0 /   ⚠️  Итого критических: 4 |
| `improve_pagerank.py` | 0.558 | Running PageRank… /  / Saved: /home/user/data70/monorepo/pagerank.json  (661 entries) |
| `improve_questions.py` | 0.555 | Извлечение открытых вопросов... /   wrote: monorepo/QUESTIONS.md /   вопросов: 7 |
| `improve_timeline_events.py` | 0.521 |   2025: 16 /   2026: 75 /   2027: 4 |
| `improve_textrank.py` | 0.511 |  /   wrote: monorepo/SUMMARIES.md /   Запустите с --apply для вставки резюме в файлы. |
| `improve_topic_model.py` | 0.501 |  /   wrote: monorepo/TOPIC_MODEL.md /   тем: 6, документов: 644 |
| `improve_keyword_index.py` | 0.479 |   wrote: monorepo/KEYWORD_INDEX.md /   wrote: monorepo/keyword_index.json /   топ-5: связи, уровень, готовности, caremate, agents |
| `improve_search_repl.py` | 0.477 |  /   >  /   Выход. |
| `improve_glossary.py` | 0.475 | Извлечение URL... /   wrote: monorepo/LINKS.md / Готово. |
| `improve_timeline.py` | 0.433 | Извлечение дат и временных маркеров... /   найдено записей: 579 /   wrote: monorepo/TIMELINE.md |
| `improve_search_index.py` | 0.419 |   всего слов: 291,685 /   wrote: monorepo/search_index.json (2515 KB) /   wrote: docs/SEARCH.md |
| `improve_readability_v2.py` | 0.409 |   wrote: monorepo/READABILITY.md /   средний FRE: 0.7/100 /   сложных (<30): 613 |
| `improve_confluence.py` | 0.396 |   Конвертировано: 257/257 файлов /   Вывод: monorepo/confluence/ /   Формат: .wiki — Confluence Wiki Markup |
| `improve_question_extractor.py` | 0.388 |    🔓 Открытый вопрос: 1 /  /   wrote: monorepo/QUESTIONS.md |
| `improve_see_also.py` | 0.383 | Добавление 'See Also' блоков... /   wrote: monorepo/SEE_ALSO.md /   вставлено блоков: 107, файлов в карте: 107 |
