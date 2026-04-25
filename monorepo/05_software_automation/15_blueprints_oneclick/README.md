# 15 — 10 Blueprint-связок «one-click»

**Уровень готовности:** ★★★★★

## Что это

**Готовые автоматизации** для типичных бизнес-задач. Каждая собрана из блоков `14_function_registry`. Пользователь нажимает «Установить» — Blueprint разворачивается за минуты.

## 10 готовых Blueprint

| # | Название | Что делает |
|---|----------|-----------|
| 1 | **Лиды → CRM → email** | Форма → CRM → приветственный email |
| 2 | **Заказы → склад → доставка** | E-commerce-цепочка |
| 3 | **Бэкап файлов → S3** | Регулярный бэкап + отчёт |
| 4 | **Соцсети → дайджест** | Сбор постов → email-дайджест |
| 5 | **API-мониторинг → Telegram** | Проверка статуса → уведомление |
| 6 | **Календарь → Slack reminder** | Календарные события → reminder |
| 7 | **PDF → AI summary → email** | Документ → суммаризация → отправка |
| 8 | **Расходы → категоризация → отчёт** | Финансовая автоматизация |
| 9 | **Кандидаты → ATS → собеседование** | HR-pipeline |
| 10 | **Контент → перевод → публикация** | Multilingual content pipeline |

## Структура Blueprint

```yaml
blueprint:
  id: leads_crm_email
  name: "Lead-to-Welcome"
  description: "Capture leads, save to CRM, send welcome email"
  estimated_setup_min: 5
  
  required_accounts:
    - typeform (or alternative)
    - hubspot (or alternative)
    - sendgrid (or alternative)
    
  flow:
    - trigger:
        function: typeform_submission
    - step:
        function: hubspot_contact_create
        map:
          email: "{{trigger.email}}"
          name: "{{trigger.first_name}} {{trigger.last_name}}"
    - step:
        function: sendgrid_send
        map:
          to: "{{trigger.email}}"
          template: welcome_v1
          
  outputs:
    - typeform_submission_id
    - hubspot_contact_id
    - sendgrid_message_id
```

## Зачем это нужно

1. **Маркетинг** — «10 готовых рабочих сценариев»
2. **Onboarding** — пользователь сразу видит ценность
3. **Образование** — Blueprint как учебный материал
4. **Маркетплейс** — авторы могут добавлять свои

## Связь с темами

- **#65 — 105 сценариев цифровой заботы** (`04_robotics_caremate/09_105_care_scenarios`) — родственная концепция, но для CareMate
- **#70 — Микрофраншизы** (`06_business_funding/07_microfranchise`) — Blueprint как микрофраншиза

## Расширение каталога

С 10 → 100+ Blueprint:
- Юридические pipeline (для SozialPlaner) — `01_social_law/`
- Сельхоз pipeline (для Agro-Scout) — `03_drones_skymediahub/11_agro_scout`
- Newsroom pipeline (`09_media_newsroom/`)
- CareMate pipeline (105 сценариев)

## Связи

- `01_internet_function_os` — Blueprint = верхний уровень IFOS
- `14_function_registry` — из чего собраны
- `16_mvp_backlog` — план развития
- `04_robotics_caremate/09_105_care_scenarios` — родственная концепция
