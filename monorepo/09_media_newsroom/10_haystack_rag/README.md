# 10 — Haystack RAG-фреймворк

**Уровень готовности:** ★★★★

## Что это

**Haystack 2.0** (deepset.ai) — production-grade фреймворк для RAG. Главные компоненты:

- **DocumentStore** (BM25 + векторный)
- **Retriever** (поиск)
- **Reranker** (улучшение)
- **Generator** (LLM)
- **Pipeline** (граф компонентов)

## Чем отличается от LangChain

| Признак | Haystack | LangChain |
|---------|----------|-----------|
| Зрелость | Высокая | Средняя |
| Production | Готов | Менее стабильный |
| Сообщество | Меньше | Больше |
| Документация | Отличная | Средняя |
| Простота | Высокая | Высокая |

Для **production AI-newsroom** Haystack — лучший выбор.

## Применение

- AI-newsroom — главная цепочка
- SozialPlaner SaaS — RAG-движок
- НейроПортал — поиск по контенту
- Telegram-бот — поиск по SGB

## Стек Haystack

```python
from haystack import Pipeline, Document
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.components.retrievers import PgvectorEmbeddingRetriever
from haystack.components.rankers import TransformersSimilarityRanker
from haystack.components.generators import OpenAIGenerator, AnthropicGenerator
```

## Связи

- `02_haystack_pgvector_pipeline` — конкретная конфигурация
- `01_ai_newsroom` — главное применение
- `02_ai_agents/09_dat_rag` — концептуальная база
