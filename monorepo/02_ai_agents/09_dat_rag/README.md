# 09 — Dynamic Alpha Tuning + RAG

**Темы каталога:** #7 (DAT для RAG), #11 (RAG для Drive)
**Кластер A-J:** A/C
**Приоритет:** А (12-14 — можно начинать сейчас)
**Уровень готовности:** ★★★★★

## Что это

**RAG (Retrieval-Augmented Generation)** — поиск релевантных фрагментов в индексе и подача их LLM как контекста. Стандартная техника.

**Dynamic Alpha Tuning** — адаптивное взвешивание keyword-search vs semantic-search. Когда запрос точный (номер закона) — keyword. Когда смысловой — vectors.

## Почему это центральная тема

RAG — основа **всех содержательных проектов** автора:
- Поиск по корпусу SGB (300+ разговоров)
- Поиск по 70 модулям соцуслуг
- Поиск по медицинским данным CareMate
- Поиск по новостям AI-newsroom
- Личная база знаний (Инфо-Бонсай)

## Современный стек RAG

| Компонент | Реализация |
|-----------|-----------|
| Индекс | ChromaDB / pgvector / Qdrant / Meilisearch |
| Эмбеддинги | BGE / mxbai-embed-large / sentence-transformers |
| Reranker | bge-reranker / cohere-reranker |
| Чанкинг | Recursive / Semantic / Hierarchical |
| Извлечение | LlamaIndex / Haystack / LangChain |

## DAT — динамическое взвешивание

```
запрос → классификатор (точный / смысловой)
            ↓                          ↓
        keyword (BM25)           semantic (vectors)
            ↓                          ↓
        ──────── α + (1-α) ────────────
                       ↓
                 итоговый ранг
```

α меняется от 0.0 (чистая семантика) до 1.0 (чистый keyword) в зависимости от классификации запроса.

## Применение в проектах автора

- **SozialPlaner** — RAG по 70 модулям + 50+ шаблонам Widerspruch
- **Telegram-бот** — оффлайн-RAG для команд `/widerspruch`, `/budget`, `/sgb`
- **Книга по SGB** — генерация разделов из RAG-источников
- **CareMate** — RAG по 105 сценариям заботы

## Связи

- `01_micro_agents` — каждый агент использует RAG
- `08_kblam` — следующее поколение
- `08_knowledge_methodology/02_info_bonsai` — личный RAG-«второй мозг»
- `08_knowledge_methodology/03_yaml_pipelines` — оркестрация RAG-пайплайнов

## Дальнейшие шаги

1. **Сегодня:** ChromaDB + LlamaIndex на корпусе SGB
2. **Неделя:** интеграция в Telegram-бот SozialHelper
3. **Месяц:** проверка точности → A/B с разными α в DAT
4. **Квартал:** Hierarchical RAG (по уровням пирамиды знаний)
