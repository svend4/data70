# Отчёт об устаревших документах

> _Порог: 30 дней. Обновлено: 2026-06-05_

---




_Порог: 30 дней. Обновлено: 2026-06-05_

Найдено проблем: **310** файлов

## Без метаданных (нет summary или тегов) — 307 файлов

| Файл | Слов | Проблемы |
|------|------|---------|
| `textkit_sandbox_onusqmjx/00_index/README.md` | 58 | нет summary, короткий (58 слов) |
| `textkit_sandbox_onusqmjx/01_social_law/README.md` | 106 | нет summary |
| `textkit_sandbox_onusqmjx/02_ai_agents/README.md` | 156 | нет summary, нет тегов |
| `textkit_sandbox_onusqmjx/03_drones_skymediahub/README.md` | 116 | нет summary, нет тегов |
| `textkit_sandbox_onusqmjx/04_robotics_caremate/README.md` | 101 | нет summary, нет тегов |
| `textkit_sandbox_onusqmjx/05_software_automation/README.md` | 111 | нет summary |
| `textkit_sandbox_onusqmjx/06_business_funding/README.md` | 136 | нет summary |
| `textkit_sandbox_onusqmjx/07_inventions_patents/README.md` | 151 | нет summary, нет тегов |
| `textkit_sandbox_onusqmjx/08_knowledge_methodology/README.md` | 101 | нет summary |
| `textkit_sandbox_onusqmjx/09_media_newsroom/README.md` | 91 | нет summary, короткий (91 слов) |
| `textkit_sandbox_onusqmjx/10_health_accessibility/README.md` | 101 | нет summary |
| `textkit_sandbox_onusqmjx/88_topics_full/README.md` | 26 | нет summary, нет тегов, короткий (26 слов) |
| `textkit_sandbox_onusqmjx/QUESTIONS.md` | 40 | нет summary, нет тегов, короткий (40 слов) |
| `textkit_sandbox_onusqmjx/READING_LIST.md` | 415 | нет summary, нет тегов |
| `textkit_sandbox_onusqmjx/READING_ORDER.md` | 116 | нет summary, нет тегов |
| `textkit_sandbox_onusqmjx/REGISTRY.md` | 124 | нет summary, нет тегов |
| `textkit_sandbox_onusqmjx/REPORT.md` | 245 | нет summary, нет тегов |
| `textkit_sandbox_onusqmjx/RISK_REGISTER.md` | 635 | нет summary, нет тегов |
| `textkit_sandbox_onusqmjx/SCHEDULE.md` | 245 | нет summary, нет тегов |
| `textkit_sandbox_onusqmjx/SCORING.md` | 346 | нет summary, нет тегов |

## Короткие (< 100 слов, заготовки) — 3 файлов

| Файл | Слов |
|------|------|
| `textkit_sandbox_onusqmjx/GITHUB_TRACKER.md` | 97 |
| `textkit_sandbox_onusqmjx/LINKS.md` | 99 |
| `textkit_sandbox_onusqmjx/QA.md` | 93 |

## Рекомендуемые действия

```bash
# Добавить summary и теги к файлам без метаданных
python scripts/improve_summaries.py
python scripts/improve_tags.py

# Обогатить короткие файлы через LLM
python scripts/improve_llm_enrich.py --section 05-habr-projects
```
