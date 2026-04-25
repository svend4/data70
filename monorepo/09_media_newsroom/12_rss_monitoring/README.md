# 12 — Мониторинг RSS-источников

**Уровень готовности:** ★★★★

## Что это

Базовый этап AI-newsroom: **постоянный мониторинг** новостных источников через RSS, API, scrapers.

## Источники для проектов автора

### Социальное право (SozialPlaner)
- BSG (Bundessozialgericht) RSS
- BVerfG (Bundesverfassungsgericht) RSS
- BMAS (Министерство труда) RSS
- Sozialgerichtsbarkeit.de
- VdK Magazine

### Дроны (SkyMediaHub)
- EASA Newsroom
- Drone Industry Association DACH
- Dronescene.com

### ИИ (НейроОС)
- Hugging Face blog
- arXiv cs.AI
- AnthropicNews
- Hacker News

### Pflege (CareMate)
- Pflegekasse-новости
- AOK Bundesverband
- Caritas / Diakonie newsrooms

## Технологии

- **Feedparser** (Python) — RSS/Atom
- **Newspaper3k** — full-text
- **Scrapy / Playwright** — для сайтов без RSS
- **Apache Airflow / Prefect** — расписание

## Pipeline

```
Cron → Feedparser → Dedupe → Filter (keywords) → 
   → Embedding → Сохранение → Notification (если интересно)
```

## Применение

- **Telegram-канал** «Sozialrecht Updates»
- **Daily digest** для подписчиков
- **Trend analysis** — что обсуждается
- **Lead generation** — для SaaS

## Связи

- `01_ai_newsroom` — потребитель
- `08_knowledge_methodology/03_yaml_pipelines` — оркестрация
- `06_business_funding/15_telegram_bot_sozialhelper` — лидогенерация

## Стратегия

1. Каталог 50+ источников по 5 темам автора
2. POC pipeline на собственных нуждах
3. Telegram-канал как маркетинговый канал
