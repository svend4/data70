# 25 — Ollama, llama.cpp, GGUF локально

**Кластер A-J:** B
**Уровень готовности:** ★★★★★ (производство)
**Приоритет:** А — практический инструментарий

## Что это

Практическая «полка» инструментов для локального запуска LLM, которые автор использует и предлагает использовать в проектах.

## Стек

| Инструмент | Что делает |
|-----------|-----------|
| **llama.cpp** | C++-библиотека для inference квантизованных LLM |
| **GGUF** | Формат файла с квантизованной моделью |
| **Ollama** | UX-обёртка над llama.cpp + REST API |
| **LM Studio** | GUI для тестирования моделей |
| **Open WebUI** | Веб-интерфейс к Ollama |
| **vLLM** | Production-grade серверный inference |
| **Text Generation Inference (TGI)** | HuggingFace эталон |
| **MLX** (Apple) | Оптимизация под Apple Silicon |

## Конкретные команды

```bash
# Установка Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Запуск Llama 3.1 8B
ollama run llama3.1:8b

# Pull другой модели
ollama pull qwen2.5:14b
ollama pull phi3.5:3.8b

# REST API
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.1:8b",
  "prompt": "Schreibe Widerspruch gegen Bescheid..."
}'
```

## Рекомендуемые модели (2025-2026)

| Модель | Размер | RAM | Назначение |
|--------|--------|-----|-----------|
| `llama3.1:8b` | 5 ГБ | 8 ГБ | База на всё |
| `mistral:7b` | 4 ГБ | 8 ГБ | Скорость |
| `qwen2.5:14b` | 9 ГБ | 16 ГБ | Многоязычность |
| `phi3.5:3.8b` | 2 ГБ | 4 ГБ | Edge / встроенные |
| `gemma2:9b` | 6 ГБ | 12 ГБ | CPU-friendly |
| `mxbai-embed-large` | 700 МБ | — | Embeddings |
| `bge-reranker-large` | 1 ГБ | — | Reranking |

## Применение в проектах автора

- **SozialPlaner** — `llama3.1:8b` для черновика Widerspruch локально
- **CareMate** — `phi3.5` на edge-устройствах
- **Telegram-бот** — `qwen2.5:14b` для DE/RU
- **Newsroom** — `mxbai-embed-large` для индексации

## Связи

- `02_local_offline_models` — концептуальная тема
- `03_one_bit_llm` — следующий шаг (BitNet через llama.cpp)
- `09_dat_rag` — Ollama + ChromaDB как локальный RAG-стек

## Учебный материал (для книги/курса)

- «Ollama за 10 минут» — стартовый туториал
- «Локальный RAG за час» — Ollama + ChromaDB + LlamaIndex
- «Pflegeheim-RAG за день» — production-кейс
