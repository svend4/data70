# Полный машинный аудит data70 — все портированные lorenzo-инструменты

- Корпус: `/home/user/data70/monorepo`
- README=контент: True
- Скриптов запущено: **180**
- ✓ ok: **158**  ✗ err: **20**  ⏱ timeout: **2**  💥 crash: **0**
- Общее время: 299.2 сек

## Скрипты с ошибками

| Скрипт | Статус | rc | Последние строки stderr |
|--------|--------|---:|--------------------------|
| `improve_benchmark.py` | err | 1 |  |
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
| `improve_link_preview.py` | 15.443 |    Проверено новых: 9 /   wrote: textkit_sandbox_onusqmjx/LINK_PREVIEW.md /   ✅ 6 \| 🔄 0 \| ❌ 3 |
| `improve_similar.py` | 5.237 | Поиск похожих документов... /   wrote: textkit_sandbox_onusqmjx/SIMILAR.md /   похожих пар: 1193, обновлено файлов: 581 |
| `improve_github_tracker.py` | 2.788 | Найдено событий: 0 /  / ℹ️  Запустите с --apply чтобы создать карточки (0 новых) |
| `improve_merge_by_topic.py` | 2.318 |  /   Было бы объединено ~61,594 слов в 7 файлов /   Запустите с --apply для реального слияния. |
| `improve_similar_passages.py` | 1.431 |   wrote: textkit_sandbox_onusqmjx/SIMILAR_PASSAGES.md /   похожих пар: 4137 /   топ сходство: 1.0 |
| `improve_staleness.py` | 1.378 | 🕰  improve_staleness.py — поиск устаревших документов (порог: 30д) /   wrote: textkit_sandbox_onusqmjx/STALENESS.md /   устаревших: 0, без метаданных: 307, коро |
| `improve_source_map.py` | 1.291 |   wrote: textkit_sandbox_onusqmjx/SOURCE_MAP.md /   категории: {'✍️ Ручной': 590} /   авторов: 1 |
| `improve_named_entity_index.py` | 0.963 |   🏢 orgs: 6 /   👤 people: 6 /   📅 dates: 5 |
| `improve_subtopic_fill.py` | 0.931 |  /   Будет дополнено: 14 файлов  \|  Пропущено: 0 /   Запустите с --apply для реальной записи. |
| `improve_entities.py` | 0.847 | Извлечение именованных сущностей... /   wrote: textkit_sandbox_onusqmjx/ENTITIES.md /   людей: 2, проектов: 18, орг: 8, технологий: 24, GitHub URL: 4 |
| `improve_sentinel_check.py` | 0.614 |   wrote: textkit_sandbox_onusqmjx/SENTINEL.md /   PII: 4, код: 0, creds: 0, HTTP: 8, лицензии: 0 /   ⚠️  Итого критических: 4 |
| `improve_consistency.py` | 0.613 | Проверка согласованности терминов... /   wrote: textkit_sandbox_onusqmjx/CONSISTENCY.md /   проблем найдено: 2 |
| `improve_missing.py` | 0.582 | Анализ пробелов в документации... /   wrote: textkit_sandbox_onusqmjx/MISSING.md /   ✅ 13  ⚠️ 4  ❌ 8 |
| `improve_concepts.py` | 0.564 | Извлечение определений понятий... /   wrote: textkit_sandbox_onusqmjx/CONCEPTS.md /   понятий: 529 |
| `improve_questions.py` | 0.525 | Извлечение открытых вопросов... /   wrote: textkit_sandbox_onusqmjx/QUESTIONS.md /   вопросов: 4 |
| `improve_abbreviations.py` | 0.518 | Словарь аббревиатур... /   wrote: textkit_sandbox_onusqmjx/ABBREVIATIONS.md /   аббревиатур: 49 |
| `improve_keyword_index.py` | 0.506 |   wrote: textkit_sandbox_onusqmjx/KEYWORD_INDEX.md /   wrote: textkit_sandbox_onusqmjx/keyword_index.json /   топ-5: связи, уровень, готовности, caremate, приме |
| `improve_textrank.py` | 0.498 |  /   wrote: textkit_sandbox_onusqmjx/SUMMARIES.md /   Запустите с --apply для вставки резюме в файлы. |
| `improve_topic_model.py` | 0.497 |  /   wrote: textkit_sandbox_onusqmjx/TOPIC_MODEL.md /   тем: 6, документов: 602 |
| `improve_timeline_events.py` | 0.488 |   2025: 16 /   2026: 71 /   2027: 4 |
| `improve_glossary.py` | 0.423 | Извлечение URL... /   wrote: textkit_sandbox_onusqmjx/LINKS.md / Готово. |
| `improve_search_index.py` | 0.401 |   всего слов: 258,600 /   wrote: textkit_sandbox_onusqmjx/search_index.json (2349 KB) /   wrote: docs/SEARCH.md |
| `improve_search_repl.py` | 0.385 |  /   >  /   Выход. |
| `improve_timeline.py` | 0.385 | Извлечение дат и временных маркеров... /   найдено записей: 298 /   wrote: textkit_sandbox_onusqmjx/TIMELINE.md |
| `improve_readability_v2.py` | 0.382 |   wrote: textkit_sandbox_onusqmjx/READABILITY.md /   средний FRE: 0.6/100 /   сложных (<30): 574 |
| `improve_contradiction_check.py` | 0.374 |  /   wrote: textkit_sandbox_onusqmjx/CONTRADICTIONS.md /   противоречий: 171 |
| `improve_question_extractor.py` | 0.348 |    🔓 Открытый вопрос: 1 /  /   wrote: textkit_sandbox_onusqmjx/QUESTIONS.md |
| `improve_passage_retrieval.py` | 0.34 |    wrote: textkit_sandbox_onusqmjx/passages.json /  /   Используйте --query "текст" для поиска. |
| `improve_confluence.py` | 0.335 |   Конвертировано: 237/237 файлов /   Вывод: textkit_sandbox_onusqmjx/confluence/ /   Формат: .wiki — Confluence Wiki Markup |
| `improve_see_also.py` | 0.333 | Добавление 'See Also' блоков... /   wrote: textkit_sandbox_onusqmjx/SEE_ALSO.md /   вставлено блоков: 89, файлов в карте: 89 |
