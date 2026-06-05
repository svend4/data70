# textkit — универсальная экстракция технических инструментов

Ответ на вопрос: «как сделать инструменты lorenzo универсальными, отвязав
техническую сторону от информационной, и перенести в любой репозиторий».

## Диагноз

В репо `svend4/lorenzo` две части:

| Часть | Что | Универсальность |
|-------|-----|------------------|
| `docs-toolkit/` (pip-пакет) | CLI-обёртка, 496 модулей | Объявлен «универсальным», но **скромный** — уважает конфиг, но мало готовых операций |
| `scripts/improve_*.py` (223 шт.) | **Реальные алгоритмы** обработки текста | **Мощные, но прибиты** к layout lorenzo |

Измерено на 221 скрипте:
- **197** хардкодят `ROOT = Path(__file__).parent.parent`
- **176** хардкодят `DOCS = ROOT / "docs"`
- Только **2** используют пакет docstoolkit
- **187** — чистый stdlib (без numpy/sklearn/anthropic) → максимально переносимы

**Вывод:** вся мощь — в самодостаточных скриптах. Они не зависят от пакета.
Привязка к lorenzo — это **2 строки** + несколько контентных допущений.

## Два слоя связанности (и как их снять)

### Слой 1 — пути (ГДЕ файлы)
Захардкожено: `ROOT = Path(__file__).parent.parent; DOCS = ROOT/"docs"`.
**Решение:** `tk_paths.py` — резолвер через env `TEXTKIT_DOCS`.
**Снимается механически** портером `port.py` (183 скрипта за один прогон, 0 ошибок).

### Слой 2 — контентные соглашения (КАК устроен контент)
Захардкожено: например `improve_clusters.py` пропускает `README.md` как
навигацию. В lorenzo верно; в data70 README.md = **основной контент** →
пропускалось 180 из 220 файлов.
**Решение:** `tk_profile.py` — соглашения через env (`TEXTKIT_README_IS_CONTENT`,
`TEXTKIT_MIN_TOKENS`). Требует точечной правки скриптов, использующих допущения.

## Файлы комплекта

```
textkit/
├── README.md          этот файл
├── tk_paths.py        слой 1: резолвер путей (env-driven)        [исходник в lib/]
├── tk_profile.py      слой 2: контентные соглашения             [исходник в lib/]
├── port.py            экстрактор: lorenzo/scripts → переносимый lib/
└── lib/               портированные скрипты (gitignored, регенерируются port.py)
    ├── tk_paths.py
    ├── tk_profile.py
    ├── improve_clusters.py     (пример: ROOT→tk_paths, README→tk_profile)
    └── … 183 скрипта
```

## Как пользоваться

```bash
# 1. Один раз: портировать инструменты из донора
cd monorepo/_audit/textkit
python3 port.py --source /home/user/lorenzo/scripts --dest lib

# 2. Запускать на ЛЮБОМ репо — путь задаётся через env
cd lib
TEXTKIT_DOCS=/home/user/data70/monorepo python3 improve_clusters.py
TEXTKIT_DOCS=/path/to/any/other/repo python3 improve_broken_links.py

# 3. Для репо, где README = контент (как data70):
TEXTKIT_DOCS=/home/user/data70/monorepo TEXTKIT_README_IS_CONTENT=1 \
  python3 improve_clusters.py
```

Перенести в ДРУГОЙ репозиторий = скопировать папку `textkit/` туда. Всё.
Никакой привязки к data70 или lorenzo — пути и соглашения снаружи, через env.

## Проверено на data70 (реальные прогоны)

| Скрипт | Результат | Кросс-валидация |
|--------|-----------|------------------|
| `improve_clusters.py` | 234 файла → 110 кластеров | **Переоткрыл мою ручную структуру**: SGB→соцправо, TetraDrone→дроны, ROS→роботы, Ollama→ИИ, Haystack→медиа, Pflegegrad→здоровье |
| `improve_broken_links.py` | 0 битых ссылок | **Совпало** с `_audit/01b_check_links.py` (0) |

Результаты: `_audit/reports/machine_clusters.md`, `machine_broken_links.md`.

## Что это доказывает

1. **Технику МОЖНО отделить от данных** — связанность была поверхностной (2 строки + skip-list), не структурной.
2. **183 инструмента стали переносимыми** одним прогоном портера.
3. **Машинная кластеризация подтвердила ручную структуру data70** — 4-я независимая проверка (после `_audit/`, scout-агентов, adversarial-verifier).

## Полный список инструментов (по категориям)

Портированные 183 скрипта покрывают:
- **Структура**: backlinks, broken_links, auto_toc, auto_linker, dependency_map
- **Классификация**: clusters, concepts, concept_graph, reclassify, merge_by_topic
- **Качество**: dedup, contradiction_check, paragraph_quality, autocorrect, density
- **Индексы**: card_index, citation_index, keyword_index, named_entity_index, embedding_index, ann_index
- **Контент**: abstract, auto_summarize, action_items, abbreviations, autofill
- **Графы**: card_graph, concept_graph, graph_search
- **Экспорт**: export_json, export_html, export_csv

Полный перечень: `python3 port.py --source <...> --dry-run`.

## Ограничения

- 38 скриптов пропущены портером: внешние зависимости (numpy/sklearn/anthropic)
  или не-improve/utils. Портируются флагом `--all` с пометкой EXTERNAL-DEPS.
- ~114 скриптов имеют слой-2 допущения (lorenzo-специфичные имена файлов
  CONTACTS/HEALTH/SCORING). Работают, но для идеального результата нужна
  точечная адаптация через `tk_profile.py` (как сделано для README в clusters).
- Скрипты пишут вывод в `DOCS/` (напр. CLUSTERS.md). Для data70 эти файлы
  перенаправлены в `_audit/reports/` вручную.
