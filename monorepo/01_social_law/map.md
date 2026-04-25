# Карта кластера 01_social_law

## Логическая структура

```
01_social_law/
├── ПРАВОВАЯ БАЗА
│   ├── 05_sgb_paragraphs     SGB IX, XII, V, X
│   ├── 14_un_brk_agg         UN-BRK, AGG
│   └── 15_kindergeld_ao      AO § 171
│
├── ИНСТРУМЕНТЫ ПОЛЬЗОВАТЕЛЯ
│   ├── 02_widerspruch_templates  возражения
│   ├── 03_klage_sozialgericht    иски
│   ├── 11_medical_letters        медписьма
│   └── 07_master_dossier         личное дело
│
├── КАТАЛОГИ УСЛУГ
│   ├── 01_persoenliches_budget   PB по § 29 SGB IX
│   ├── 04_pflege_assistenz       часы, ставки
│   ├── 08_70_modules_catalog     70 модулей
│   ├── 12_assistive_services_50  50+ ассистенций
│   └── 10_ru_de_comparison       сравнение РФ-DE
│
└── СУДЕБНАЯ ПРАКТИКА И СТРАТЕГИЯ
    ├── 09_bsg_judgements         решения BSG
    ├── 13_legal_strategy         план Sozialgericht
    └── 06_kostenschieberei       нарушения § 14 SGB IX
```

## Связи между подпапками

- `01_persoenliches_budget` опирается на `05_sgb_paragraphs` и `09_bsg_judgements`
- `02_widerspruch_templates` использует `06_kostenschieberei` как основной аргумент
- `04_pflege_assistenz` берёт ставки из `08_70_modules_catalog`
- `07_master_dossier` сводит в одно место материалы из всех подпапок
- `13_legal_strategy` — мета-инструкция, как пользоваться остальным

## Уровни проработки

| Подпапка | Уровень |
|----------|---------|
| 01_persoenliches_budget | ★★★★★ — готов к подаче |
| 02_widerspruch_templates | ★★★★★ — 5 вариантов |
| 03_klage_sozialgericht | ★★★★ — нужна редактура под суд |
| 04_pflege_assistenz | ★★★★★ — расчёты завершены |
| 05_sgb_paragraphs | ★★★★ — каталог |
| 06_kostenschieberei | ★★★★ — аналитика |
| 07_master_dossier | ★★★★★ — заполняемый шаблон |
| 08_70_modules_catalog | ★★★★★ — мегашаблон |
| 09_bsg_judgements | ★★★ — подборка |
| 10_ru_de_comparison | ★★★ — справочник |
| 11_medical_letters | ★★★★★ — 1365 сообщений |
| 12_assistive_services_50 | ★★★★ — каталог |
| 13_legal_strategy | ★★★★ — план |
| 14_un_brk_agg | ★★★ — обзор |
| 15_kindergeld_ao | ★★★ — частный кейс |
