# Подключение юридических MCP-серверов (немецкое / EU-право)

Памятка: как включить немецкие юридические MCP-серверы для сессий **Claude Code
on the web** в этом репозитории. Проверено по `docs.claude.com`
(claude-code-on-the-web) и README серверов, июнь 2026.

> ⚠️ **Любые изменения вступают в силу со СЛЕДУЮЩЕЙ сессии, не в текущей.**

## Уже настроено в этом репозитории

Файл `.mcp.json` в корне подключает **metaneutrons/german-legal-mcp**
(Bundes-/Landesrecht, Rechtsprechung im Internet, EUR-Lex, InfoCuria/EuGH, DIP
Bundestag). Сервер запускается внутри VM через `npx` (Node предустановлен).
Версия закреплена: `@1.2.2`. Лицензия GPL-3.0, без аутентификации.

## Что нужно сделать вам в интерфейсе claude.ai

### 1. Сеть окружения → Custom (ОБЯЗАТЕЛЬНО для metaneutrons)

Без этого сервер запустится, но поиск по законам вернёт пусто: немецких
госсайтов нет в дефолтном allowlist (там только реестры пакетов + GitHub).

Иконка облака (выбор окружения) → навести на окружение → шестерёнка →
**Network access** → **Custom** → отметить «Also include default list of common
package managers» → в **Allowed domains** добавить:

```
gesetze-im-internet.de
www.gesetze-im-internet.de
rechtsprechung-im-internet.de
www.rechtsprechung-im-internet.de
dip.bundestag.de
search.dip.bundestag.de
eur-lex.europa.eu
curia.europa.eu
```

Если какие-то запросы всё равно пустые — посмотрите, на какой хост реально
ходит сервер, и добавьте его; либо временно поставьте уровень **Full**.

### 2. Ansvar — добавить как КОННЕКТОР (не через .mcp.json)

Ansvar-шлюз использует OAuth, который из VM headless не проходит. Поэтому
подключаем его как коннектор — его трафик идёт через серверы Anthropic, и
allowlist для него не нужен:

claude.ai → **Connectors** → **Add custom connector** → URL:

```
https://gateway.ansvar.eu/mcp
```

→ пройти OAuth → **включить коннектор для сессии**. Даёт gesetze-im-internet
(6 870 законов / 91 843 §§), rechtsprechung-im-internet, DIP Bundestag.
Free tier: 50 запросов/день, Apache-2.0.

## Проверка (в следующей сессии)

- Команда `/mcp` покажет статус подключённых серверов.
- Попросите Claude прогнать тест-план: тексты § 103 / § 104 Abs. 3 SGB IX,
  § 43 SGB I, §§ 13/57/64f SGB XII; дело **B 8 SO 7/24 R**; **BT-Drs. 18/9522**.

## Опционально (продвинутое)

- **inooLabs/gesetze-verwaltungsvorschriften-mcp** (Verwaltungsvorschriften) —
  Python-сервер; в `.mcp.json` не вынесен, т.к. нужен клон кода + `pip install`
  + домен `verwaltungsvorschriften-im-internet.de`. Подключать вручную.
- **Ansvar EU_compliance** — тот же шлюз Ansvar (вторично для немецкого дела).
- **borghei/AI-Skills-German-Law** — это плагины/скиллы, НЕ MCP: объявляются в
  `.claude/settings.json` (marketplace / enabledPlugins), а не как коннектор.

## Безопасность

- Версия metaneutrons закреплена (`@1.2.2`) — `npx` не подтянет неожиданный код.
- Серверы читают **открытые** госисточники, но текст ваших запросов виден шлюзу
  (для Ansvar) — для чувствительных формулировок предпочтителен self-host.
- Лицензии: Ansvar — Apache-2.0; metaneutrons — GPL-3.0; inooLabs — не указана.

Источники: `docs.claude.com/en/claude-code-on-the-web`,
`github.com/metaneutrons/german-legal-mcp`,
`github.com/Ansvar-Systems/German-law-mcp`.
