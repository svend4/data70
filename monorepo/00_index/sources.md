# Соответствие новой структуры и старых файлов

Все исходники остаются в корне репозитория и **не переписываются**. Новая структура `monorepo/` ссылается на них.

## Сырые экспорты ChatGPT

| Файл | Описание | Что отражает в монорепо |
|------|----------|-------------------------|
| `chatgpt_export_full.txt` | Первый экспорт (131 разговор, 7.6 МБ) | Все кластеры, преимущественно ранние идеи |
| `chat_export/chat_export_001.txt` … `153.txt` | Второй экспорт (1105 разговоров, 79 МБ) | Полный корпус |
| `extracted_ai_topics.txt` (332 КБ) | Извлечённые ИИ-темы, выборка 1 | 02_ai_agents, 05_software_automation |
| `extracted_ai_topics_batch2.txt` (200 КБ) | Извлечённые ИИ-темы, выборка 2 | 02_ai_agents (#71-88) |

## Аналитические части и своды

| Файл | Описание | Где использован |
|------|----------|-----------------|
| `MANIFEST.md` | История трёх архивов, призыв | 00_index, README |
| `README.md` | Корневое описание | 00_index |
| `analysis_01_overview.md` | Обзор 1105 разговоров | 00_index/clusters_overview.md |
| `analysis_02_top_projects.md` | Топ-10 проектов | superprojects/ |
| `analysis_03_inventions.md` | Изобретения | 00_index/inventions_index.md, 07_inventions_patents/ |
| `analysis_04_social_law.md` | Соцправо | 01_social_law/ |
| `analysis_05_recommendations.md` | Стратегия монетизации | 00_index/three_waves_roadmap.md, 06_business_funding/ |
| `analysis_1105_conversations.md` | Сводка 1105 | 00_index |
| `analysis_ai_topics.md` (60 КБ) | Все ИИ-темы детально | 02_ai_agents (особенно темы #1-#88) |

## Отчёты по частям (parts)

| Файл | Описание | Где использован |
|------|----------|-----------------|
| `part10_deep_analysis.md` | Глубокий анализ ИИ-тем | 02_ai_agents |
| `part10_new_topics.md` | Темы #71-#88 | 02_ai_agents, 05_software_automation, 06_business_funding |
| `part11_connections.md` | Кластеры, хабы, мета-паттерны, суперпроекты | 00_index/clusters_overview.md, superprojects/ |
| `part12_catalog.md` | Единый каталог 88 тем | 00_index/catalog_88_topics.md |
| `part13_tech_stacks.md` | Стеки 5 суперпроектов | superprojects/, 02_ai_agents |
| `part14_business_models.md` | Бизнес-модели | 06_business_funding/, superprojects/ |

## Технические утилиты

| Файл | Описание |
|------|----------|
| `prepare_for_infom.py` | Скрипт подготовки данных для Inform |
| `infom_import.json` | Входные данные для Inform |
| `infom_snapshot.json` | Снимок состояния для Inform |

## Принцип ссылок

В новых файлах используются Markdown-ссылки относительно корня:

```markdown
[Источник: analysis_03_inventions.md](../../analysis_03_inventions.md)
[Каталог 88 тем](../../00_index/catalog_88_topics.md)
[Папка 01_social_law](../../01_social_law/)
```

## Что НЕ делается

- Не удаляются и не переименовываются файлы корня
- Не редактируется `analysis_*.md` и `part*.md`
- Не трогаются экспорты `chat_export/` и `chatgpt_export_full.txt`
- Не меняется `prepare_for_infom.py` и JSON-снимки

## Что МОЖНО делать дальше

- Дополнять `monorepo/` новыми материалами (заявки, патенты, MVP-планы)
- Создавать в подпапках `concept.md`, `mvp.md`, `roadmap.md`, `funding.md`, `risks.md`, `sources.md`
- Связывать карточки между кластерами через ссылки
