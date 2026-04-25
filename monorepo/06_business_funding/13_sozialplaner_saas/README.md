# 13 — SozialPlaner SaaS

**Цена:** €29-99/мес. за рабочее место
**MVP бюджет:** €30K
**Срок MVP:** 4-5 мес.
**Финансирование:** EXIST-Gründerstipendium

## Что это

**SozialPlaner** — веб-платформа для **Pflegedienste, Sozialstationen, юристов соцправа** в Германии. Объединяет:

- Каталог услуг (из `01_social_law/08_70_modules_catalog`)
- Генератор документов (Widerspruch, Klage, Antrag)
- Таймлайн дел клиентов (Master Dossier)
- Калькулятор Persönliches Budget и Pflegeassistenz
- Прецедентная база BSG
- Bytebot-автоматизация заполнения порталов ведомств

## Целевая аудитория

| Сегмент | Потенциал | Цена |
|---------|-----------|------|
| Pflegedienste | 15 000+ в DE | €29-49/мес/раб.место |
| Sozialstationen | 5 000+ | €29-49 |
| Юристы соцправа | 2 000+ | €99/мес |
| Caritas/Diakonie/AWO | 6 крупных | €500-2000/мес (white-label) |
| Sozialarbeiter | 50 000+ | €19-29/мес |

## Тарифы

| Тариф | Цена | Что включено |
|-------|------|-----------|
| Starter | €29/мес | 1 раб. место, до 50 клиентов |
| Pro | €49/мес | 1 раб. место, безлимит, генерация документов |
| Team | €99/мес | до 5 раб. мест |
| Enterprise | €499+/мес | white-label, on-premise |

## Контент готов на 80%

В архиве автора **уже есть**:
- 70+ модулей соцуслуг
- 50+ шаблонов документов
- 105 сценариев заботы
- Master Dossier
- Анализ BSG-практики
- Каталог 50+ ассистентских услуг

Нужно только **обернуть в UI и API**.

## Технологический стек

| Слой | Стек |
|------|------|
| Frontend | Next.js + TypeScript |
| Backend | Python (FastAPI) или Node.js |
| Database | PostgreSQL + pgvector |
| Auth | Supabase Auth / Clerk |
| AI | Claude API + локальный Ollama |
| Payments | Stripe |
| Hosting | Hetzner DE / Vercel |

## Конкурентное преимущество

- **Уникальный контент** — нет аналогов с такой глубиной SGB-разбора
- **Личный опыт автора** — продукт делается «изнутри» соцсистемы
- **Многоязычие** — немецкий + русский (для мигрантов)
- **GDPR-friendly** — локальный ИИ для приватных данных

## Маркетинг

1. **LinkedIn outreach** — Sozialarbeiter в DE
2. **Conference talks** — Kongress Soziale Sicherung
3. **Партнёрство** с Sozialverband VdK (2M членов)
4. **Контент-маркетинг** — статьи на kanzlei.de, anwalt.de
5. **Free tier** — Telegram-бот для лидогенерации

## Связи

- `01_social_law/` — весь содержательный кластер
- `02_ai_agents/09_dat_rag` — RAG-движок
- `02_exist_gruenderstipendium` — главное финансирование
- `15_telegram_bot_sozialhelper` — лидогенерация

## Дальнейшие шаги

1. Лендинг + ранний доступ (waitlist)
2. Бизнес-план для EXIST (4-8 нед.)
3. Найм 1 fullstack + 1 ML-инженер (через TU Dresden)
4. MVP за 4-5 мес.
5. Первые 10 клиентов из Дрездена
