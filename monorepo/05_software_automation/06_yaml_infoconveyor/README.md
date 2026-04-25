# 06 — YAML+GPT инфоконвейер

**Тема каталога:** #53 (приоритет А-14)
**Уровень готовности:** ★★★★

## Что это

**Инфоконвейер** — конфигурируемый ETL/ELT-пайплайн для **обработки информации**:
- Сбор из источников
- Извлечение / нормализация
- Анализ через ИИ
- Хранение и публикация

Описывается в **YAML** (человекочитаемый), исполняется в Python/Airflow/Prefect.

## Пример YAML-пайплайна

```yaml
pipeline:
  name: sgb_news_digest
  schedule: "0 8 * * *"  # каждый день в 8:00
  
  sources:
    - type: rss
      url: https://www.bsg.bund.de/feed
      filter: "Persönliches Budget"
    - type: web
      url: https://www.sozialgerichtsbarkeit.de
      crawler: playwright
    - type: api
      endpoint: https://juris.de/api/v2/decisions
      auth: $JURIS_TOKEN
      
  pipeline:
    - step: dedupe
    - step: ner
      model: spacy_de
      entities: [person, organization, paragraph]
    - step: classify
      model: ollama/llama3.1:8b
      prompt: |
        Категоризируй: 
        - Persönliches Budget
        - Pflegegrad
        - Kostenschieberei
    - step: summarize
      model: ollama/llama3.1:8b
      max_tokens: 200
      
  outputs:
    - type: telegram
      channel: @sozialhelper_de
    - type: email
      to: digest@example.com
    - type: github
      repo: my/sgb-archive
      path: digest/{date}.md
```

## Зачем это нужно

1. **Версионирование** — пайплайны в Git
2. **Декларативность** — что делать, а не как
3. **Композиция** — объединение пайплайнов
4. **Тестируемость** — каждый шаг изолирован
5. **Open-source** — можно публиковать и обмениваться

## Применение

| Сценарий | Пайплайн |
|----------|----------|
| Юридический мониторинг | `01_social_law` — ежедневный дайджест |
| AI-newsroom | `09_media_newsroom/01_ai_newsroom` — генерация новостей |
| CareMate отчёты | `04_robotics_caremate/02_caremate_hub` — отчёты для Pflegekasse |
| Книга по SGB | сборка из RAG → структурированные главы |

## Технологии

- **YAML** — описание
- **Pydantic** — валидация схемы
- **Apache Airflow / Prefect** — оркестрация
- **Python operators** — каждый шаг
- **Ollama / Claude API** — ИИ-шаги

## Связи

- `01_internet_function_os` — пайплайны как часть IFOS
- `02_ai_agents/09_dat_rag` — RAG как один из шагов
- `08_knowledge_methodology/03_yaml_pipelines` — методологическая надстройка
- `08_knowledge_methodology/01_pyramid_4_levels` — пайплайн как способ движения информации между уровнями

## Дальнейшие шаги

1. Спецификация YAML-схемы
2. Эталонный исполнитель на Python
3. Каталог 10 готовых пайплайнов
4. Запуск как часть SmartOfficeProto
