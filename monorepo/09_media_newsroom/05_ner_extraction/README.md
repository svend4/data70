# 05 — NER (Named Entity Recognition)

**Уровень готовности:** ★★★

## Что это

NER — извлечение **именованных сущностей** из текста: лиц, мест, организаций, дат, цифр, параграфов закона, медицинских терминов.

В контексте AI-newsroom — критический этап обработки.

## Категории сущностей

| Тип | Примеры | Применение |
|-----|---------|-----------|
| **Person** | Olaf Scholz, Dr. Müller | Персоны в новостях |
| **Organization** | BMAS, BSG, Caritas | Учреждения |
| **Location** | Dresden, Sachsen, EU | География |
| **Date** | 2026-04-25, Q1 2026 | Хронология |
| **Money** | €150 000, $5.5B | Финансы |
| **Paragraph** | § 14 SGB IX | Юридические ссылки |
| **Medical** | Pflegegrad 2, GdB 70 | Медицинские термины |
| **Product** | TetraDrone, CareMate | Продукты |

## Технологии

| Модель | Качество | Скорость |
|--------|----------|----------|
| **spaCy de_core_news_lg** | хорошее | быстро |
| **Stanza** (Stanford) | очень хорошо | средне |
| **Flair** | очень хорошо | средне |
| **GLiNER** | новое, гибко | средне |
| **LLM-based** (Claude/GPT) | отлично | дорого |

## Применение в проектах автора

### SozialPlaner (юридический NER)
- Параграфы SGB
- Aktenzeichen судов
- Имена ведомств
- Даты в Bescheid

### CareMate (медицинский NER)
- Pflegegrad / GdB
- Медикаменты
- Диагнозы
- Витальные показатели

### AI-newsroom (общий NER)
- Все категории
- Связь между сущностями (Knowledge Graph)

## Связи

- `01_ai_newsroom` — главный потребитель
- `02_haystack_pgvector_pipeline` — стек
- `02_ai_agents/10_neurosymbolic` — NER + правила
- `01_social_law/05_sgb_paragraphs` — каталог параграфов

## Дальнейшие шаги

1. POC: spaCy на корпусе SGB
2. Custom NER для юридических сущностей (через Prodigy)
3. Интеграция в pipeline
