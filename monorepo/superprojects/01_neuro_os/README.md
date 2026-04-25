# Суперпроект 1: НейроОС

**Бюджет MVP:** €100-150K
**Срок MVP:** 4-5 мес
**Бизнес-модель:** Freemium SaaS + Marketplace
**MRR на 24 мес:** €35-50K
**Безубыточность:** ~24 мес

## Что это

**Internet Function OS / НейроОС** — операционная система, в которой ИИ — не приложение, а ядро. Объединяет:
- Микроагенты как процессы
- Семантический автобус как шину
- Локальные модели как «движки»
- Пирамиду знаний как файловую систему

## Темы каталога

#13, #14, #41, #43, #46, #53, #56, #72, #74, #76, #77, #85, #87

## Кластеры монорепозитория

- `02_ai_agents/01_micro_agents` — пчелиный слой
- `02_ai_agents/02_local_offline_models` — локальные модели
- `02_ai_agents/22_semantic_bus` — шина данных
- `02_ai_agents/09_dat_rag` — RAG-движок
- `05_software_automation/01_internet_function_os` — Function Registry
- `05_software_automation/14_function_registry` + `15_blueprints_oneclick` — компоненты
- `05_software_automation/16_mvp_backlog` — план разработки
- `08_knowledge_methodology/01_pyramid_4_levels` — архитектура

## Бизнес-модель

| Тариф | Цена | Что входит |
|-------|------|-----------|
| Free | €0 | Локально, базовые агенты |
| Pro | €9/мес | Облако, продвинутые агенты |
| Team | €19/мес/чел | Коллаборация |
| Enterprise | от €499/мес | On-premise, SLA |

Доп. источники: маркетплейс агентов и Blueprint (30% комиссия).

## Стек

```
UI (Tauri/PWA)
   ↓
Семантический автобус (NATS JetStream)
   ↓
Микроагенты (LangGraph + CrewAI)
   ↓
RAG-движок (Haystack/LlamaIndex + ChromaDB)
   ↓
Локальные модели (Ollama)
   ↓
Распределение (Exo P2P)
```

## Команда

| Роль | Чел. |
|------|------|
| Fullstack (Python/React) | 2 |
| ML-инженер | 1 |
| DevOps | 1 |

## Финансирование

- **EXIST-Gründerstipendium** — €150K (главное)
- **INVEST-Zuschuss** — для ангелов
- **Pre-seed** — €300K-1M (после MVP)

## Путь к окупаемости

```
Мес 1-6:    MVP, бета, 500 free
Мес 7-12:   Pro, 200 платящих = €1.8K MRR
Мес 13-18:  Team + маркетплейс, €12K MRR
Мес 19-24:  Enterprise, €35-50K MRR
Мес 24:     Безубыточность
```
