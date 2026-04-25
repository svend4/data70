# 02 — Haystack + pgvector пайплайн

**Уровень готовности:** ★★★★

## Что это

Конкретный технологический стек для AI-newsroom:

- **Haystack 2.0** (deepset) — RAG-фреймворк
- **PostgreSQL + pgvector** — единая БД для структуры и векторов
- **mxbai-embed-large** — embeddings
- **Claude API + Ollama** — LLM

## Почему именно эти

| Решение | Альтернатива | Чем лучше |
|---------|--------------|-----------|
| **Haystack** | LangChain | Проще для production |
| **pgvector** | ChromaDB | Единая БД с реляционными |
| **mxbai-embed-large** | OpenAI ada | Open-source, быстрее |
| **Claude API** | GPT-5 | Лучше для длинных контекстов |
| **Ollama** | llama.cpp напрямую | Удобнее DevX |

## Архитектура

```
┌────────────────────────────────────┐
│  PostgreSQL 16 + pgvector          │
│  ├── articles (структура)          │
│  ├── embeddings (vec)              │
│  ├── entities (NER результаты)     │
│  └── metadata (авторы, даты)        │
└────────────┬───────────────────────┘
             ↓
┌────────────────────────────────────┐
│  Haystack 2.0 Pipeline             │
│  ├── Reader (FAISS/pgvector)       │
│  ├── Retriever (BM25 + Dense)      │
│  ├── Reranker (cross-encoder)      │
│  └── Generator (Claude/Llama)      │
└────────────────────────────────────┘
```

## Образец кода (концепт)

```python
from haystack import Pipeline
from haystack.components.retrievers import PgvectorEmbeddingRetriever
from haystack.components.generators import ClaudeGenerator
from haystack.components.builders import PromptBuilder

pipeline = Pipeline()
pipeline.add_component("retriever", PgvectorEmbeddingRetriever(...))
pipeline.add_component("prompt", PromptBuilder(template=template))
pipeline.add_component("generator", ClaudeGenerator(...))
pipeline.connect("retriever.documents", "prompt.documents")
pipeline.connect("prompt", "generator")

result = pipeline.run({"retriever": {"query": "Persönliches Budget BSG 2025"}})
```

## Применение

- Базовый стек для всех ИИ-текстовых проектов автора
- SozialPlaner SaaS
- AI-newsroom
- НейроПортал

## Связи

- `01_ai_newsroom` — главный потребитель
- `02_ai_agents/09_dat_rag` — концептуальная основа
- `02_ai_agents/25_ollama_local` — локальный fallback

## Дальнейшие шаги

1. POC на собственных данных (SGB)
2. Бенчмарк скорости / качества vs LangChain + ChromaDB
3. Документация
