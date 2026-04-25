# 99 — Ссылки на исходный архив

## Назначение

Эта папка — **карта оригинальных файлов** в корне репозитория. Все они **сохранены без изменений** — служат первоисточниками для всей новой структуры в `monorepo/`.

## Файлы корня репозитория

### Манифест и обзор
- `MANIFEST.md` — история трёх архивов, призыв
- `README.md` — корневое описание

### Сырые экспорты ChatGPT
- `chatgpt_export_full.txt` (7.6 МБ) — первый экспорт (131 разговор)
- `chat_export/chat_export_001.txt` … `153.txt` (79 МБ) — второй экспорт (1105 разговоров)

### Извлечённые материалы
- `extracted_ai_topics.txt` (332 КБ)
- `extracted_ai_topics_batch2.txt` (200 КБ)

### Аналитика
- `analysis_01_overview.md` — обзор
- `analysis_02_top_projects.md` — топ-10 проектов
- `analysis_03_inventions.md` — изобретения
- `analysis_04_social_law.md` — социальное право
- `analysis_05_recommendations.md` — стратегия
- `analysis_1105_conversations.md` — сводка
- `analysis_ai_topics.md` (60 КБ) — детально про ИИ-темы

### Отчёты по частям
- `part10_deep_analysis.md` — глубокий анализ
- `part10_new_topics.md` — темы #71-88
- `part11_connections.md` — кластеры, связи, мета-паттерны
- `part12_catalog.md` — каталог 88 тем
- `part13_tech_stacks.md` — стеки 5 суперпроектов
- `part14_business_models.md` — бизнес-модели

### Технические утилиты
- `prepare_for_infom.py` — скрипт для Inform
- `infom_import.json` — входные данные
- `infom_snapshot.json` — снимок состояния

## Важное

**Ничего из этого не редактируется**. Новая структура `monorepo/` использует эти файлы как первоисточники, ссылается на них через относительные пути:

```markdown
[analysis_03_inventions.md](../../analysis_03_inventions.md)
[part12_catalog.md](../../part12_catalog.md)
```

## Карта «откуда взято что в монорепозитории»

| Из файла-источника | В подпапку монорепозитория |
|---------------------|---------------------------|
| `analysis_04_social_law.md` | `01_social_law/` (весь кластер) |
| `analysis_ai_topics.md` | `02_ai_agents/` (детально) |
| `analysis_02_top_projects.md` | `superprojects/` (5 суперпроектов) |
| `analysis_03_inventions.md` | `07_inventions_patents/` |
| `part12_catalog.md` | `00_index/catalog_88_topics.md` |
| `part11_connections.md` | `00_index/clusters_overview.md` + `superprojects/` |
| `part13_tech_stacks.md` | `superprojects/` (стеки) |
| `part14_business_models.md` | `06_business_funding/` + `superprojects/` |
| `analysis_05_recommendations.md` | `00_index/three_waves_roadmap.md` + `06_business_funding/01_three_waves_strategy/` |

## Для исследователей

Если читаете этот архив:
1. Начните с `00_index/clusters_overview.md` — обзор всего
2. Затем `00_index/catalog_88_topics.md` — каталог тем
3. Затем `00_index/superprojects.md` — концепции
4. Глубокое погружение — в подпапки кластеров
5. Сырые материалы — в файлах корня и `chat_export/`

## Лицензия

Открытый доступ. Используйте свободно — автор выложил это, чтобы идеи не погибли в третий раз. См. `MANIFEST.md`.
