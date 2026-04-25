# 16 — MVP Backlog (Internet Function OS)

**Уровень готовности:** ★★★★

## Что это

**Backlog работ** для разработки MVP Internet Function OS. CSV с эпиками и задачами — разделение полной концепции (`01_internet_function_os`) на 6-9 месяцев работы.

## Эпики

| Эпик | Описание | Срок | Команда |
|------|----------|------|---------|
| E1. Function Registry | БД и API для блоков | 1 мес. | Backend + DB |
| E2. Vocabulary/Schema | Онтология типов | 1 мес. | Backend + ML |
| E3. Composer UI | Drag-and-drop конструктор | 2-3 мес. | Frontend |
| E4. 10 Blueprint демо | Готовые сценарии | 1 мес. | Backend |
| E5. Trust Layer | Проверки безопасности и права | 1 мес. | Backend + Юрист |
| E6. AI-помощник | Помощник в Composer | 1 мес. | ML + Frontend |
| E7. Auth & Billing | Регистрация + Stripe | 0.5 мес. | Backend |
| E8. Marketplace | Магазин агентов и Blueprint | 1 мес. | Fullstack |
| E9. Документация и onboarding | Учебные материалы | 0.5 мес. | Tech writer |

## Задачи (примеры)

### E1. Function Registry
- [ ] PostgreSQL-схема для функций
- [ ] CRUD API (FastAPI)
- [ ] Импорт CSV из `14_function_registry`
- [ ] Поиск по категориям
- [ ] Версионирование функций

### E3. Composer UI
- [ ] Базовый drag-and-drop с React Flow
- [ ] Палитра функций (фильтр + поиск)
- [ ] Соединение узлов с типизацией
- [ ] Превью результата
- [ ] Экспорт Blueprint как YAML

## Команда

| Роль | Кол-во | Задачи |
|------|--------|--------|
| Fullstack | 2 | E1, E3, E4, E7 |
| ML-инженер | 1 | E2, E6 |
| DevOps | 1 | Сборка, CI/CD, Tauri |
| **Итого** | **4** | **MVP за 4-5 мес.** |

## Бюджет

- Зарплаты (4 чел. × 5 мес.) — €80-120K (DACH-ставки)
- Инфраструктура (Hetzner + API) — €2-5K/мес
- Модели — €0 (Ollama)
- **Итого:** €100-150K

## Финансирование

Главный кандидат — **EXIST-Gründerstipendium** (€150K/год):
- 4 человека по €1500/мес = €72K/год
- Расходы — €30K/год
- Перекрывает MVP

См. `06_business_funding/02_exist_gruenderstipendium`.

## Связи

- `01_internet_function_os` — родительская концепция
- `14_function_registry` — компонент
- `15_blueprints_oneclick` — компонент
- `06_business_funding/18_neuro_os_freemium` — бизнес-модель
- `06_business_funding/02_exist_gruenderstipendium` — финансирование
- `superprojects/01_neuro_os/` — как это вписано в более крупный проект

## Дальнейшие шаги

1. Финализация эпиков и задач в Linear / Jira
2. Бюджетирование по реальным DACH-ставкам
3. Подача EXIST-заявки
4. Найм 1-2 человек на старт (Frontend + Fullstack)
