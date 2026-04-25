# 14 — Function Registry

**Уровень готовности:** ★★★★★ (CSV с 60 записями)

## Что это

**Реестр атомарных функций** — каталог программных блоков с их «паспортами». Часть Internet Function OS (`01_internet_function_os`).

В архиве автора уже **60 готовых записей** для:
- WordPress (плагины как функции)
- Make.com (коннекторы)
- n8n (узлы)

## Структура «паспорта функции»

```yaml
function:
  id: stripe_payment_create
  name: "Stripe: Create Payment"
  category: payment
  source: make_com
  
  inputs:
    - name: amount
      type: number
      unit: euro_cents
      required: true
    - name: currency
      type: string
      default: EUR
    - name: customer_email
      type: email
      required: true
      
  outputs:
    - name: payment_intent_id
      type: string
    - name: status
      type: enum
      values: [pending, succeeded, failed]
    - name: redirect_url
      type: url
      
  cost:
    monthly: 0  # бесплатно у Make
    per_run: 0  # бесплатно
    stripe_fee: "1.4% + €0.25"
    
  risks:
    legal: 
      - GDPR (PSD2)
      - PCI-DSS handled by Stripe
    business:
      - chargeback_risk
    technical:
      - api_rate_limit_5_per_sec
      
  compatible_with:
    - shopify_order_created
    - hubspot_deal_won
    - typeform_submission
```

## CSV-каталог 60 записей

Папка содержит готовый CSV-файл (`functions.csv`) с этими записями. Структура колонок:

`id, name, category, source, inputs, outputs, monthly_cost, per_run_cost, risks, lat, license`

## Применение

1. **IFOS Composer** — пользователь видит каталог и собирает Blueprint
2. **API для разработчиков** — поиск функций по категории/совместимости
3. **Маркетинг** — «60+ блоков из коробки, расширяемо»
4. **Юр. аудит** — Trust Layer проверяет риски всех функций в Blueprint

## Расширение

Для роста до 200-1000 записей:
- Импорт каталога Make.com / n8n / Zapier
- Краудсорсинг (Pull Request от сообщества)
- AI-генерация (анализ документации API → паспорт)

## Связи

- `01_internet_function_os` — родительская концепция
- `15_blueprints_oneclick` — связки из этих функций
- `16_mvp_backlog` — план разработки
- `02_ai_agents/04_mcp_protocol` — MCP-серверы как одна из категорий
