# kbtool

**Переносимый CLI для аудита и структурирования больших хаотичных
markdown/текстовых баз знаний.** Stdlib-only, без зависимостей, работает на
**любом** репозитории — просто укажи путь.

Эволюция инструментов из `monorepo/_audit/`: всё ценное (детерминированные
проверки + TF-IDF кластеризация + дедуп + концепт-граф + health) собрано в один
независимый pip-устанавливаемый пакет, отвязанный от data70 и lorenzo.

## Зачем

Когда у тебя репозиторий с тысячами файлов неструктурированной информации
(заметки, переписки, идеи, документы), kbtool отвечает на вопросы:
- Насколько он здоров? (один балл 0-100)
- Какие темы в нём есть? (автоматическая кластеризация — «newsgroups»)
- Есть ли дубли, битые ссылки, структурные дыры?
- Как связаны концепты? (граф)

## Ключевое отличие от lorenzo-скриптов

| | lorenzo `improve_*.py` | **kbtool** |
|---|------------------------|------------|
| Привязка к репо | жёсткая (`Path(__file__).parent.parent`) | нет — путь как аргумент |
| Зависимости | разные | **нет (stdlib)** |
| Побочные эффекты | **пишут в твои файлы** | **read-only**, отчёт в cwd |
| Установка | vendored | `pip install` |
| Команд | 223 разрозненных | 8 связных |

**kbtool ничего не меняет в корпусе** — только читает и пишет один отчёт в
текущую директорию. Безопасен на любом репо без sandbox.

## Установка

```bash
cd kbtool
pip install -e .
```

После этого команда `kbtool` доступна глобально.

## Использование

```bash
# Полный аудит + единый отчёт
kbtool all /path/to/repo

# Отдельные команды
kbtool inventory /path/to/repo                    # статистика
kbtool links     /path/to/repo                    # битые markdown-ссылки
kbtool structure /path/to/repo                    # папки без README
kbtool cluster   /path/to/repo                    # темы (TF-IDF, «newsgroups»)
kbtool dedup     /path/to/repo                    # дублирующиеся абзацы
kbtool concepts  /path/to/repo                    # концепт-граф
kbtool health    /path/to/repo                    # один балл 0-100
kbtool tree      /path/to/repo                    # ХАОС → дерево папок по темам

# Поиск и вопросы по корпусу
kbtool index     /path/to/repo                    # построить поисковый индекс (BM25)
kbtool search    /path/to/repo "ключевые слова"   # найти документы
kbtool ask       /path/to/repo "вопрос"           # ответ с цитатами

# Сервисы
kbtool watch     /path/to/repo --reindex          # инкрементальный re-audit
kbtool serve     /path/to/repo --port 8765        # HTTP-дашборд + API
kbtool semantic  /path/to/repo                    # опц. эмбеддинги (sentence-transformers)

# Опции
kbtool all . --exclude _audit node_modules   # исключить папки
kbtool all . --readme-nav                     # README = навигация, не контент
kbtool all . --threshold 0.2                  # порог кластеризации
kbtool cluster . --json                       # машинный вывод
kbtool all . -o report.md                     # куда писать отчёт
```

Путь можно не указывать — берётся из env `KBTOOL_DOCS` или текущей директории.

## Команды

| Команда | Что делает | Меняет файлы? |
|---------|-----------|---------------|
| `inventory` | Файлы, байты, строки, папки | нет |
| `links` | Проверка всех `[..](..)` | нет |
| `structure` | README в листовых папках | нет |
| `cluster` | TF-IDF + косинус → темы | нет |
| `dedup` | Jaccard по хешам абзацев | нет |
| `concepts` | Совстречаемость топ-терминов | нет |
| `health` | Агрегат 4 метрик → балл | нет |
| `all` | Всё + отчёт | только отчёт в cwd |
| `tree` | Хаос → дерево по темам | см. ниже (3 режима) |

## `kbtool tree` — реорганизация хаоса в дерево

Берёт результат кластеризации и раскладывает файлы по тематическим папкам с
авто-именами (топ-термины кластера, транслитерация кириллицы). **Три режима по
убыванию безопасности:**

```bash
# 1) dry-run (по умолчанию) — только показать план, ничего не трогать
kbtool tree /path/to/chaotic/repo

# 2) материализовать КОПИЮ дерева в новую папку — оригинал НЕ трогается
kbtool tree /path/to/repo --out /path/to/organized

# 3) переместить файлы IN-PLACE (деструктивно, требует подтверждения)
kbtool tree /path/to/repo --apply --yes        # использует git mv если есть .git
```

Опции: `--threshold` (детальность кластеров), `--misc-threshold N` (кластеры
размером ≤ N → `00_misc/`).

**Пример (реальный хаос):** `lorenzo/docs` — 1610 файлов плоской свалки →
~107 тематических папок (`05_llm_agent/`, `101_export_json/`, ...), оригинал цел.

Имена папок: `NN_термин1_термин2` с числовым префиксом для порядка;
singleton-кластеры группируются в `00_misc/`; коллизии имён → суффикс `_2`.

## Проверено на двух репозиториях

| Репо | Файлов | Health | Битых ссылок | Дублей |
|------|-------:|-------:|-------------:|-------:|
| data70/monorepo | 223 | **95/100** | 0 | 0 |
| lorenzo/docs | 2785 | **24/100** | 792 | 95 |

Один и тот же инструмент, два разных вердикта — переносимость работает.

## Конфигурация через env

```bash
export KBTOOL_DOCS=/path/to/repo        # путь по умолчанию
export KBTOOL_README_IS_CONTENT=1       # README — контент (1) или навигация (0)
export KBTOOL_MIN_TOKENS=20             # минимум токенов для содержательного файла
```

## Архитектура

```
kbtool/
├── paths.py      резолвер путей (env/arg)
├── profile.py    контент-соглашения (README, min-tokens, skip)
├── corpus.py     загрузка + токенизация (RU+EN стопслова)
├── checks.py     инвентаризация, ссылки, структура (read-only)
├── analyze.py    TF-IDF кластеризация, дедуп, концепт-граф
├── health.py     агрегат метрик в балл 0-100
└── cli.py        8 команд, единая точка входа
```

3 слоя расцепления (из опыта переноса lorenzo-инструментов):
1. **пути** — `paths.py` (env/arg, не хардкод)
2. **контент-соглашения** — `profile.py` (README=контент?)
3. **изоляция записи** — by design read-only, отчёт в cwd

## Тесты

```bash
pip install -e ".[dev]"
pytest tests/
# или без pytest:
python3 -c "from tests.test_smoke import *; test_tokenize(); test_pipeline(); test_resolve_paths()"
```

## Расширение

kbtool — ядро. Опциональные тяжёлые возможности (semantic embeddings, RAG,
agent) можно добавить как плагины через `pip install kbtool[semantic]`, не ломая
stdlib-ядро. Для production-RAG см. `docs-toolkit` lorenzo.

## Поиск и Q&A по корпусу

```bash
kbtool index   /path/to/repo                 # построить индекс (1 JSON в .kbtool/)
kbtool search  /path/to/repo "TetraDrone патент" -k 5 --method bm25
kbtool ask     /path/to/repo "какие гранты для CareMate"
```

Индекс — один JSON-файл в `.kbtool/index.json` внутри корпуса. Метод по умолчанию
BM25, есть keyword. Поиск возвращает doc_id, score, snippet, title. `ask`
склеивает лучшие пассажи в extractive-ответ с пронумерованными цитатами.

## HTTP-дашборд

```bash
kbtool serve /path/to/repo --port 8765
# → http://127.0.0.1:8765
```

Эндпоинты:
- `GET /` — HTML-дашборд с баллом, метриками, поиском
- `GET /api/health` — JSON health
- `GET /api/search?q=...&k=5&method=bm25` — поиск
- `GET /api/ask?q=...&k=5` — extractive ответ с цитатами

Stdlib `http.server`, без зависимостей.

## Watch — инкрементальный re-audit

```bash
kbtool watch /path/to/repo --interval 2 --reindex
```

Поллит mtime, при изменениях печатает `[hh:mm:ss] +1 ~3 -0 health=95/100 …`,
опционально перестраивает индекс. Ctrl+C — выход.

## Semantic-плагин (опционально)

```bash
pip install kbtool[semantic]       # добавляет sentence-transformers
kbtool semantic /path/to/repo      # строит эмбеддинги в .kbtool/embeddings.json
```

Без установки команда `semantic` сообщает статус и подсказывает — graceful
fallback, ядро остаётся stdlib-only.

## Дорожная карта

- [x] `kbtool tree` — авто-реорганизация хаоса в дерево
- [x] `kbtool index` / `search` / `ask` — поисковый индекс + BM25 + extractive Q&A
- [x] `kbtool watch` — инкрементальный re-audit
- [x] `kbtool serve` — HTTP-дашборд + REST API
- [x] semantic-плагин — опц. эмбеддинги
- [ ] LLM-плагин (Anthropic/OpenAI/Ollama) для abstractive ответов через `ask`
- [ ] Federation — мульти-репо поиск

## Лицензия

MIT.
