# Следующие шаги — кластер 02_ai_agents

## Краткосрочно (0-3 мес.)

1. **Прототип RAG-стека на Ollama** — подпапки `02_local_offline_models` + `09_dat_rag` + `25_ollama_local`
   - Цель: базовый RAG-движок для книги по SGB → бот → SaaS
   - Стек: Python + LlamaIndex + ChromaDB + Ollama (Llama 3.1 8B Q4)
   - Срок: 2-4 недели

2. **MVP микроагентов на LangGraph** — `01_micro_agents`
   - Простой агент: парсит PDF → извлекает параграфы SGB → отвечает на запросы
   - Срок: 4-6 недель

3. **MCP-интеграция** — `04_mcp_protocol`
   - Подключить локальный RAG к Claude Code как MCP-сервер
   - Срок: 2 недели

## Среднесрочно (3-12 мес.)

1. **НейроОС MVP**
   - Объединить: микроагенты + RAG + локальные модели + семантический автобус
   - Стек: Tauri + Python + NATS JetStream
   - Бюджет: €100-150K
   - Финансирование: EXIST-Gründerstipendium

2. **Бенчмарк LiveMCP-101** — `21_livemcp_bench`
   - Прогнать собственных агентов на LiveMCP
   - Опубликовать результаты как маркетинг

3. **Эссе для Hacker News** — `06_sparse_moe`, `12_kolmogorov_nn`, `14_bees_ants_bio`
   - Привлечение разработчиков к проекту
   - Подготовка к pre-seed раунду

## Долгосрочно (12-36 мес.)

1. **Forth-интеллект на ESP32** — связано с `07_inventions_patents/22_forth_intelligence`
   - Прототип ультралёгкого ИИ для бортовой платформы дрона
   - Партнёрство с Fraunhofer IPMS Dresden

2. **Распределённый кластер на Exo** — `16_exo_p2p`
   - Сеть из 5-10 домашних устройств как мини-датацентр
   - Эксперимент с моделями 70B+

3. **Семантический автобус как стандарт** — `22_semantic_bus`
   - Спецификация + open-source эталонная реализация
   - Привлечь Anthropic / OpenAI / Mistral как партнёров

## Темы для статей и заявок

| Тема | Источник | Куда подать |
|------|----------|-------------|
| «Forth-интеллект для роботов» | 07_inventions_patents/22 | EIC Pathfinder |
| «Биомодель Пчёлы и Муравьи» | 14_bees_ants_bio | NeurIPS workshop |
| «Семантический автобус для смартфонов» | 22_semantic_bus | ACM CHI |
| «Domain-specific RAG для соцправа» | 09_dat_rag | EU AI Conference |
| «Локальные модели для приватности» | 02_local_offline_models | DSGVO compliance journal |

## Связи

- `superprojects/01_neuro_os/` — главный потребитель этих компонентов
- `04_robotics_caremate` — для роя роботов нужен Forth-интеллект
- `08_knowledge_methodology` — пирамида знаний работает поверх RAG-движка
