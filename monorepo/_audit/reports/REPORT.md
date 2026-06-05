# AUDIT REPORT — data70 monorepo

_Создан оркестратором_

## 1. Инвентаризация

- Кластеров: **13**
- Подпапок-тем: **172**
- Markdown-файлов: **215**
- Объём: **699,551** байт

## 2. Структура (Фаза 1a)

- Кластеров с дефектами: **2**
  - `contacts`: missing_README.md
  - `snapshots`: missing_README.md

## 3. Ссылки (Фаза 1b)

- Битых внутренних ссылок: **0**

## 4. Покрытие 88 тем (Фаза 2)

- Карточек на создание: **0**
- Карточек на обогащение: **0**

## 5. Согласованность данных (Фаза 4) + сверка с источниками (Фаза 5)

- Regex-Фаза 4 пометила: **11/11** сущностей как потенциально конфликтные
- LLM-Фаза 5 (выполнена): **0 реальных конфликтов** — все срабатывания ложные

Фаза 5 сверила бюджеты/сроки/MRR суперпроектов, звёзды патентов и статистику
соцправа с первоисточниками `part13/part14/analysis_*` — **все факты совпали**.
Подробности: [05_fidelity_findings.md](05_fidelity_findings.md).

## 6. Готовность LLM-фаз

- Фаза 5 (сверка с первоисточниками): **38 jobs** подготовлено
- Фаза 6 (полнота chat_export): **21,495,808 токенов** для прохода

Запуск этих фаз требует API-ключа Claude/Ollama.

## 7. Рекомендации (с динамическим роутингом)

### Безопасные автофиксы (можно применять без LLM):

- Починить 4 битых иллюстративных ссылки в `00_index/naming_conventions.md` и `00_index/sources.md`
- Добавить `map.md` и `next_steps.md` в `00_index/` (служебная папка, но единообразия ради)
- Подтянуть `#N` в 5 неотмеченных карточках (`enrich.json`)

### Требует LLM (если важно):

- Сверить 42 карточки с первоисточниками (Фаза 5)
- Проверить, не пропущены ли темы в `chat_export/` (Фаза 6, дорого)

## 8. Файлы отчёта

- [00_inventory.md](00_inventory.md)
- [01a_structure.md](01a_structure.md)
- [01b_links.md](01b_links.md)
- [02_coverage_88.md](02_coverage_88.md)
- [03_facts.md](03_facts.md)
- [04_consistency.md](04_consistency.md)
- [05_fidelity.md](05_fidelity.md)
- [05_fidelity_findings.md](05_fidelity_findings.md)
- [06_completeness.md](06_completeness.md)
- [06_completeness_findings.md](06_completeness_findings.md)
- [MACHINE_AUDIT.md](MACHINE_AUDIT.md)
- [full_machine_audit.md](full_machine_audit.md)
- [machine_broken_links.md](machine_broken_links.md)
- [machine_clusters.md](machine_clusters.md)
- [machine_concept_graph.md](machine_concept_graph.md)
- [machine_contradictions.md](machine_contradictions.md)
- [machine_duplicates.md](machine_duplicates.md)
