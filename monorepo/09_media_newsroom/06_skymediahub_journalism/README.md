# 06 — SkyMediaHub как поставщик контента

**Уровень готовности:** ★★★

## Что это

Связка **SkyMediaHub Bavaria** (`03_drones_skymediahub/01_skymediahub_bavaria`) с **AI-newsroom**: дроны снимают, ИИ обрабатывает в новости.

## Поток данных

```
Дроны (TetraDrone, Pathfinder, и т.д.)
   ↓ съёмка видео + телеметрия
DroneCompute Hub (Edge AI)
   ↓ предварительный анализ
AI-newsroom pipeline
   ├── Извлечение событий из видео
   ├── Описание через LLM
   ├── Связь с базой знаний
   └── Генерация статьи
   ↓
Публикация (региональные новости)
```

## Сценарии применения

### 1. Сельхоз-новости
- Agro-Scout снимает поля
- ИИ обнаруживает аномалии (вредители, засуха)
- Автоматическая статья «Saxony farmers report 15% drought»

### 2. Региональные новости
- TetraDrone снимает события (фестивали, аварии)
- ИИ описывает что происходит
- Локальная пресса публикует

### 3. Гражданская журналистика
- Pathfinder на участках, недоступных для людей
- ИИ генерирует репортаж
- Sandboxed для защиты приватности

## Связи

- `03_drones_skymediahub/` — кластер дронов
- `03_drones_skymediahub/09_drone_compute_hub` — Edge AI
- `01_ai_newsroom` — главная цепочка
- `08_dronemedia_content` — техника контента

## Стратегия

1. POC: Agro-Scout + AI-newsroom для саксонских фермеров
2. Партнёрство с Sächsische Zeitung
3. Включение в SkyMediaHub-заявку Bayern Innovativ
