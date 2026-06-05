# Сравнение: что из lorenzo вошло в kbtool, а что нет

_Детальная инвентаризация. Источник: lorenzo = **187 скриптов** `improve_*.py` +
**~489 модулей** пакета `docstoolkit`. Цель = `kbtool` (14 команд, 12 модулей)._

## Важное различие двух интеграций

В data70 есть **два разных** результата работы с lorenzo:

| | `monorepo/_audit/textkit/` | `kbtool/` |
|---|---------------------------|-----------|
| Что | **Портер** + 183 скрипта lorenzo дословно (path-patched) | **Чистая переписка** ключевых функций |
| Код lorenzo внутри | да (скопирован, 2 строки изменены) | **нет** — только идеи/алгоритмы |
| Зависимость от lorenzo | да (нужен клон) | **нет** — автономно |
| Назначение | прогнать ВСЕ инструменты lorenzo | переносимое самостоятельное приложение |

**Этот документ про `kbtool`** (приложение). textkit покрывает 183/187 скриптов
дословно, но он — обёртка над lorenzo, не самостоятельное приложение.

---

## ЧАСТЬ 1. Скрипты lorenzo (187) → kbtool

Сгруппированы по функциям. ✅ = есть эквивалент в kbtool, ⚠️ = частично, ❌ = нет.

### Структура и ссылки (16 скриптов)
| lorenzo | kbtool | статус |
|---------|--------|--------|
| broken_links | `links` | ✅ |
| readmes, heading_audit | `structure` | ⚠️ только наличие README |
| backlinks, crossrefs, crosslink_all, see_also | — | ❌ |
| dependency_map, orphans, network | — | ❌ |
| sitemap, toc, auto_toc, outline, footnotes | — | ❌ |

### Кластеризация и классификация (7)
| lorenzo | kbtool | статус |
|---------|--------|--------|
| clusters | `cluster` (TF-IDF) | ✅ |
| concepts, concept_graph | `concepts` | ✅ |
| reclassify, merge_by_topic | `tree` | ✅ (реорганизация) |
| topic_model (LDA-стиль) | — | ❌ |
| classifier | — | ❌ |

### Дубликаты и сходство (8)
| lorenzo | kbtool | статус |
|---------|--------|--------|
| dedup | `dedup` (Jaccard) | ✅ |
| duplicate_across | `dedup` | ⚠️ покрыто частично |
| similar, similar_passages | — | ❌ (cross-doc сходство) |
| compare, compare_docs, external_compare, cross_section | — | ❌ |

### Поиск и RAG (10)
| lorenzo | kbtool | статус |
|---------|--------|--------|
| search_index, keyword_index | `index` + `search` | ✅ |
| passage_retrieval | `ask` (extractive) | ✅ |
| semantic_embeddings, embedding_index | `semantic` (плагин) | ⚠️ опц., не в поиске |
| ann_index | — | ❌ (приближённый поиск) |
| faceted_search, multi_query, search_repl | — | ❌ |
| semantic_search (в поиске) | — | ❌ |

### Health / метрики / отчёты (11)
| lorenzo | kbtool | статус |
|---------|--------|--------|
| health, scoring, metrics | `health` (агрегат) | ✅ |
| stats, inventory-аналог | `inventory` | ✅ |
| report, export_report | `all` (отчёт) | ✅ |
| kpi, kpi_snapshot | — | ❌ |
| badges, status_badges | — | ❌ |

### Watch / сервер / инфра (8)
| lorenzo | kbtool | статус |
|---------|--------|--------|
| watch, watcher, file_watcher_sim | `watch` | ✅ |
| serve.py (в пакете) | `serve` (своя реализация) | ✅ |
| run_all | (textkit `run_all.py`) | ⚠️ вне kbtool |
| benchmark, schedule | — | ❌ |

### NLP-извлечение (10) — НЕ интегрировано
entities, named_entity_index, citation_index, citations, textrank,
text_segmenter, chunk_semantic, extract_code, extract_tables, keyword (как анализ)
→ **❌ всё. kbtool не делает NER, цитаты, textrank, извлечение кода/таблиц.**

### Качество текста (12) — НЕ интегрировано
spellcheck, autocorrect, readability_v2, complexity, passive_voice,
vocabulary_richness, density, paragraph_quality, empty_sections, content_gaps,
missing, sentiment → **❌ всё. kbtool не анализирует качество прозы.**

### Генерация контента (17) — НЕ интегрировано (by design read-only)
abstract, auto_summarize, summaries, summary_extender, progressive_summarize,
faq, qa, questions, question_extractor, narrative, gap_filler, subtopic_fill,
auto_linker, autofill, proposal_gen, recipe, abbreviations
→ **❌ всё. kbtool принципиально ничего не генерирует и не пишет в карточки.**

### Экспорт (7)
| lorenzo | kbtool | статус |
|---------|--------|--------|
| export_json | `--json` флаг | ⚠️ частично |
| export_csv, export_html | — | ❌ |
| obsidian, epub, rss, confluence | — | ❌ |

### Карточки и граф знаний (13) — почти не интегрировано
card_index, card_graph, card_promote, bulk_decay, decay_checker, knowledge_map,
knowledge_evolution, knowledge_snapshot, pagerank, graph, graph_search, mindmap
→ `concepts` даёт базовый граф ⚠️; **остальное ❌** (CardEnvelope, pagerank,
mindmap, decay-механика).

### Интеграции (6) — НЕ интегрировано
mcp_test, mcp_dashboard, github_issues, github_tracker, webhooks, collab_finder
→ **❌ всё. kbtool не интегрирован с MCP / GitHub / webhooks.**

### LLM-функции (5) — НЕ интегрировано
llm_contact, llm_enrich, llm_gaps, llm_qa, llm_summary
→ **❌ всё. `ask` extractive (склейка пассажей), без LLM-генерации.**

### Мета / governance / временное (20+) — НЕ интегрировано
tech_radar, onboarding, risk_register, registry, decisions, changelog, audit_db,
consistency, validate, templates, contacts, timeline, timeline_events,
version_diff, staleness, progress, digest, alerts, и др.
→ **❌ всё.**

---

## ЧАСТЬ 2. Пакет docstoolkit (10 README-возможностей) → kbtool

| # | Возможность пакета | kbtool | статус |
|---|--------------------|--------|--------|
| 1 | Локальный RAG (5 retrievers × 4 answerers) | keyword+bm25, echo | ⚠️ 2/5 retrievers, 1/4 answerers |
| 2 | Adaptive multi-hop retrieval | — | ❌ |
| 3 | Streaming SSE | — | ❌ (serve отдаёт обычный JSON) |
| 4 | Agent loop (ReAct + plan-execute) | — | ❌ |
| 5 | Workflow DAG | — | ❌ (был в textkit, не в kbtool) |
| 6 | A/B experiments | — | ❌ |
| 7 | Eval / golden P/R/F1 | — | ❌ |
| 8 | Conversation memory | — | ❌ |
| 9 | Federation (мульти-репо) | — | ❌ |
| 10 | Observability (OTel/Prometheus) | базовый health | ⚠️ нет метрик-экспорта |

**Из 10 продвинутых возможностей пакета: 0 полных, 2 частичных (RAG, health).**

---

## ИТОГОВЫЙ ПОДСЧЁТ

| Категория | Всего в lorenzo | ✅ полно | ⚠️ частично | ❌ нет |
|-----------|----------------:|--------:|-----------:|------:|
| Скрипты `improve_*` | 187 | ~13 | ~7 | ~167 |
| Возможности пакета | 10 | 0 | 2 | 8 |

**kbtool покрывает ~10-15% поверхности lorenzo** — но это **ядро** для задачи
«структурировать и запрашивать большой хаотичный архив»:
аудит + кластеризация + дерево + поиск + health + сервер.

---

## ЧТО ИМЕННО ВОШЛО (полный список ✅)

1. `inventory` — статистика корпуса (≈ lorenzo stats)
2. `links` — битые ссылки (≈ broken_links)
3. `structure` — наличие README (≈ readmes, частично)
4. `cluster` — TF-IDF кластеризация (≈ clusters)
5. `concepts` — концепт-граф (≈ concept_graph)
6. `dedup` — дубли абзацев (≈ dedup)
7. `health` — агрегированный балл (≈ health + scoring + metrics)
8. `tree` — реорганизация в дерево (≈ reclassify + merge_by_topic)
9. `index` — поисковый индекс (≈ search_index + keyword_index)
10. `search` — BM25/keyword поиск (≈ passage_retrieval)
11. `ask` — extractive Q&A (≈ rag echo-answerer)
12. `watch` — инкрементальный мониторинг (≈ watch/watcher)
13. `serve` — HTTP-дашборд (≈ serve.py)
14. `semantic` — опц. эмбеддинги (≈ semantic_embeddings, плагин)

---

## ЧЕГО НЕТ И ЧТО БЫ ДАЛО НАИБОЛЬШУЮ ПОЛЬЗУ (приоритет добавления)

| Приоритет | Функция lorenzo | Зачем для большого архива |
|-----------|-----------------|---------------------------|
| 🔥 высокий | **LLM-answerer** (llm_qa) | настоящие abstractive-ответы вместо склейки |
| 🔥 высокий | **NER + citation_index** | извлечение сущностей/ссылок для графа знаний |
| 🔥 высокий | **backlinks + crossrefs** | автосвязывание карточек (решает orphans-проблему) |
| 🟡 средний | **pagerank + knowledge_map** | важность узлов в графе |
| 🟡 средний | **federation** | поиск сразу по нескольким репо |
| 🟡 средний | **export obsidian/html** | переносимость в другие инструменты |
| 🟡 средний | **textrank/summaries** | авто-резюме длинных документов |
| 🟢 низкий | **eval/golden P/R/F1** | формальное качество поиска |
| 🟢 низкий | **A/B experiments** | сравнение retriever-методов |
| 🟢 низкий | timeline, staleness, kpi | временная динамика |

---

## ЧЕСТНЫЙ ВЫВОД

- **kbtool — это «ядро 80/20»**: 14 команд покрывают самые частые задачи
  (структурировать хаос + искать + оценить здоровье), что = ~10-15% функций
  lorenzo, но ~80% реальной пользы для исходной задачи.
- **kbtool автономен** (stdlib, без lorenzo) и безопасен (read-only) — в обмен
  на отсутствие генерации, governance, продвинутого RAG, NLP-извлечения.
- **textkit** (отдельно) даёт доступ ко ВСЕМ 183 скриптам lorenzo, но ценой
  зависимости от клона lorenzo и риска побочных эффектов (нужен sandbox).
- Для «полного» приложения не хватает прежде всего: **LLM-ответов, NER,
  автосвязывания (backlinks), federation**. Это понятная дорожная карта.
