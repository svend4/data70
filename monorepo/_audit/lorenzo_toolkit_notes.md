# Заметки: применение lorenzo/docs-toolkit к data70

_Сессия эксперимента: клонирование `svend4/lorenzo` и пробный прогон на `data70/monorepo/`._

## Что есть в lorenzo

- **`docs-toolkit/`** — Python-пакет, 496 модулей, CLI `docstoolkit`
- **`scripts/`** — 223 batch-скрипта `improve_*.py`

CLI команды: `init`, `doctor`, `ingest`, `index`, `search`, `rag`, `agent`, `kg`,
`taxonomy`, `eval`, `serve`, `skills`, `history`, `voice`, `assets`, `profile`, `diff-bulk`.

Релевантные модули для data70: `clustering`, `classifier`, `doc_taxonomy`,
`taxonomy`, `doc_concept_map`, `kg`, `rag`, `self_rag`, `adversarial`, `agent`,
`citation_parser`, `concept_drift`, `eval`, `online_eval`.

## Что проверено фактически

| Команда / скрипт | Статус | Замечания |
|------------------|--------|-----------|
| `docstoolkit doctor` | ✅ работает | 5 ok / 9 warnings (опц. зависимости) |
| `docstoolkit ingest` | ✅ доступна | PDF/HTML/DOCX/EPUB → md |
| `docstoolkit index build` | ❌ требует подготовки | ищет существующий `search_index.json` |
| `docstoolkit search` | ❌ зависит от index | то же |
| `docstoolkit taxonomy` | ❌ TypeError | `TaxonomyConfig(max_depth=...)` баг в `rag/advanced.py:115` |
| `docstoolkit kg index/query` | ⏳ не запускал | требует индекс |
| `scripts/improve_card_index.py --build` | ⚠️ работает, но не на data70 | `ROOT = Path(__file__).parent.parent` жёстко привязан к layout lorenzo |

## Ключевое ограничение

**Все 223 скрипта `scripts/improve_*.py` через `Path(__file__).parent.parent`
жёстко привязаны к layout lorenzo.** Запуск из любой папки даёт
индексацию `lorenzo/docs/`, не data70. Конфиг `docstoolkit.toml` они игнорируют.

CLI `docstoolkit *` — уважает конфиг, но часть команд имеет баги или требует
подготовленного индекса.

## CardEnvelope формат (полезно)

Каждый `.md` → JSON-карточка:

```json
{
  "card_id": "sha256:0056b9e7ab8f1795",
  "card_type": "doc",
  "state": "raw",
  "sources": ["docs/.../path.md"],
  "edges": [
    {"to": "docs/.../other.md", "rel": "references"},
    {"to": "docs/.../yet.md", "rel": "contradicts"}
  ]
}
```

Типизированные edges (`references` / `contradicts` / `extends` / `related`)
сильнее моих неявных «Связи:» в data70. Это образец для будущего расширения.

## Три варианта применения к data70

### Вариант A — встроить data70 как раздел в lorenzo

```bash
cd /home/user/lorenzo
ln -s /home/user/data70/monorepo docs/data70
python scripts/improve_card_index.py --build --section data70
python scripts/improve_clusters.py --section data70
python scripts/improve_contradiction_check.py --section data70
python scripts/improve_concept_graph.py --section data70
```

- ✅ Все 223 скрипта работают без правки кода
- ❌ Создаёт зависимость data70 от lorenzo, артефакты лежат в lorenzo/cards
- 📌 Подходит, если data70 рассматривается как одна из тем lorenzo

### Вариант B — адаптировать выбранные скрипты под data70

Скопировать 5-10 ключевых в `data70/monorepo/_audit/scripts/from_lorenzo/`,
заменить `ROOT = Path(__file__).parent.parent` на конфигурируемый путь
(через env или argparse). Список приоритета:

1. `improve_card_index.py` — типизированные CardEnvelope
2. `improve_clusters.py` — машинная переклассификация
3. `improve_contradiction_check.py` — семантические противоречия
4. `improve_concept_graph.py` — граф связей
5. `improve_dedup.py` — настоящая дедупликация
6. `improve_embedding_index.py` — векторный индекс
7. `improve_reclassify.py` — пересборка таксономии

- ✅ data70 остаётся автономным
- ❌ Один раз надо адаптировать 5-10 скриптов (по 1-3 строки)
- 📌 Подходит, если data70 должен жить отдельно

### Вариант C — поставить toolkit как библиотеку

```bash
cd /home/user/lorenzo/docs-toolkit && pip install -e .
cd /home/user/data70 && docstoolkit doctor
```

Работают только CLI (без 223 batch-скриптов).

- ✅ Чисто, без копирования файлов
- ❌ Большая часть полезных скриптов недоступна
- 📌 Подходит для production-RAG-сервиса (`docstoolkit serve`)

## Что было создано в этой сессии

- `/home/user/data70/docstoolkit.toml` — конфиг для будущих запусков
- `/home/user/data70/docstoolkit_demo.toml` — пример из lorenzo (бэкап)
- Клон lorenzo в `/home/user/lorenzo/` (не часть data70, локальный workspace)

## Рекомендация

**Вариант A для прототипа, Вариант B для production.**

Сначала Вариант A — быстро получить машинный взгляд на data70 (кластеризация,
противоречия, граф). Сравнить с моим `_audit/` отчётом (структура, ссылки,
покрытие 88, Phase 5/6). Это будет **четвёртая независимая проверка**
структуры data70 — поверх:

1. `_audit/` (мои детерминированные скрипты)
2. Параллельных scout-агентов (Phase 6)
3. Adversarial verifier (Phase 5)
4. **Lorenzo machine-clustering (это будет 4-я)**

Если результаты сходятся — структура data70 устойчива к разным методам анализа.
Если расходятся — это указывает на пробелы или предвзятость одного из подходов.

После прототипа — Вариант B: вынести 5-7 скриптов в `_audit/scripts/from_lorenzo/`
с адаптацией ROOT, чтобы data70 мог независимо переаудитироваться.
