# Следующие шаги — кластер 04_robotics_caremate

## Краткосрочно (0-3 мес.)

1. **Прототипы 2-3 ключевых роботов** — `01_15_robot_zoo`
   - Снегирь (доставка) — простейший: дрон + грипперы
   - Бобр (уборка) — на базе Roomba + ML-сегментация
   - Стриж (курьер) — мини-дрон в комнате
   - Срок: 8-12 недель
   - Бюджет: €1-3K за прототип

2. **YAML-манифесты в открытом доступе** — `12_yaml_manifests`
   - Публикация на GitHub под MIT
   - Маркетинг: «открытая платформа для бытовой робототехники»

3. **CareMate Hub MVP без IoT** — `02_caremate_hub`
   - Только мобильное приложение с 5 сценариями из `09_105_care_scenarios`
   - Бюджет: €3-5K (MVP)
   - Партнёр: 1-2 Pflegeheim в Дрездене

## Среднесрочно (3-12 мес.)

1. **Подача патентной заявки на рой роботов-зверей**
   - DPMA (Германия) → потом EPO (Европа)
   - `07_inventions_patents/06_robot_zoo_15`
   - Бюджет: €5-15K

2. **Kickstarter «TetraRobot Zoo Kit»**
   - 5 базовых роботов в комплекте + ПО
   - Цена: €99-499
   - Целевая сумма: €100K
   - `06_business_funding/06_kickstarter`

3. **CareMate Total пилот**
   - 3 учреждения, 50 коек
   - Сертификация DiGA / Krankenkasse-партнёрство
   - Бюджет: €150-220K
   - `06_business_funding/19_caremate_b2b2c`

## Долгосрочно (12-36 мес.)

1. **EIC Accelerator заявка**
   - Тема: «Specialized Robot Swarm for Aging Population»
   - Сумма: €0.5-2.5M
   - Партнёры: Fraunhofer IPA Stuttgart (робототехника)

2. **AAL Programme** для CareMate
   - Сумма: до €500K
   - Тема: «Multi-Robot Care for Independent Living»

3. **Международное масштабирование**
   - DACH → ЕС → США/Канада
   - White-label для крупных провайдеров ухода

## Партнёры

| Партнёр | Тема |
|---------|------|
| **Fraunhofer IPA Stuttgart** | Робототехника, Service Robots |
| **TU Dresden — Cluster of Excellence CeTI** | Тактильные интерфейсы |
| **Pflegekasse / AOK** | Pilots в Pflegeheim |
| **Caritas / Diakonie** | Сеть учреждений |
| **iRobot / Roborock** | Бытовые роботы (для лицензии) |

## Связи с другими кластерами

- `01_social_law/08_70_modules_catalog` — основа для 105 сценариев
- `03_drones_skymediahub/01_skymediahub_bavaria` — общая роевая платформа
- `02_ai_agents/22_semantic_bus` — связь между роботами
- `07_inventions_patents/06_robot_zoo_15` — патентный трек
- `superprojects/03_caremate_total/` — продуктовый трек
- `superprojects/05_forth_swarm/` — рой как платформа

## Риски

| Риск | Митигация |
|------|-----------|
| Безопасность (рой в доме) | Сертификация TÜV |
| Кибербезопасность | Локальная коммуникация (Matter, без облака) |
| Сложность настройки | App-Onboarding с ИИ-помощником |
| Конкуренция iRobot/Dyson | Ниша «много мелких» вместо «один большой» |
| Стоимость кита | Фокус на B2B (Pflegeheim) → потом B2C |
