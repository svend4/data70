# Фаза 5 — Сверка с первоисточниками (заглушка)

## Сводка

- Файлов на проверку: **41**
- LLM-вызовы: не выполнены (требуется ключ Claude/Ollama)

## Стратегия

Когда будет настроен LLM:
1. Берём по 5-10 jobs за раз (батч)
2. Дешёвый Llama-роутинг: тривиальные совпадения отметить сразу
3. Spot-check через Claude Sonnet на 20% выборки
4. Opus — только для критичных (юр., патенты, мед.)

## Подготовлено jobs

| Карточка | Кластер | Источников |
|----------|---------|----------:|
| `00_index/superprojects.md` | 00_index | 0 |
| `00_index/three_waves_roadmap.md` | 00_index | 0 |
| `01_social_law/README.md` | 01_social_law | 1 |
| `01_social_law/next_steps.md` | 01_social_law | 1 |
| `02_ai_agents` | 02_ai_agents | 3 |
| `02_ai_agents/16_exo_p2p/README.md` | 02_ai_agents | 3 |
| `03_drones_skymediahub/01_skymediahub_bavaria/README.md` | 03_drones_skymediahub | 2 |
| `03_drones_skymediahub/02_tetradrone/README.md` | 03_drones_skymediahub | 2 |
| `03_drones_skymediahub/11_agro_scout/README.md` | 03_drones_skymediahub | 2 |
| `03_drones_skymediahub/14_dual_use_concept/README.md` | 03_drones_skymediahub | 2 |
| `03_drones_skymediahub/README.md` | 03_drones_skymediahub | 2 |
| `03_drones_skymediahub/next_steps.md` | 03_drones_skymediahub | 2 |
| `04_robotics_caremate/01_15_robot_zoo/README.md` | 04_robotics_caremate | 2 |
| `04_robotics_caremate/08_agro_robots/README.md` | 04_robotics_caremate | 2 |
| `04_robotics_caremate/09_105_care_scenarios/README.md` | 04_robotics_caremate | 2 |
| `05_software_automation` | 05_software_automation | 2 |
| `05_software_automation/01_internet_function_os/README.md` | 05_software_automation | 2 |
| `05_software_automation/02_smart_office_proto/README.md` | 05_software_automation | 2 |
| `05_software_automation/08_b2b_neuronet/README.md` | 05_software_automation | 2 |
| `06_business_funding/01_three_waves_strategy/README.md` | 06_business_funding | 2 |
| `06_business_funding/03_bayern_innovativ/README.md` | 06_business_funding | 2 |
| `06_business_funding/04_horizon_eic/README.md` | 06_business_funding | 2 |
| `06_business_funding/07_microfranchise/README.md` | 06_business_funding | 2 |
| `06_business_funding/10_geoarb/README.md` | 06_business_funding | 2 |
| `06_business_funding/11_digital_caravan/README.md` | 06_business_funding | 2 |
| `06_business_funding/18_neuro_os_freemium/README.md` | 06_business_funding | 2 |
| `06_business_funding/19_caremate_b2b2c/README.md` | 06_business_funding | 2 |
| `06_business_funding/20_neuroportal_content/README.md` | 06_business_funding | 2 |
| `06_business_funding/21_forth_swarm_hardware/README.md` | 06_business_funding | 2 |
| `06_business_funding/README.md` | 06_business_funding | 2 |
| `06_business_funding/map.md` | 06_business_funding | 2 |
| `07_inventions_patents/README.md` | 07_inventions_patents | 1 |
| `07_inventions_patents/map.md` | 07_inventions_patents | 1 |
| `08_knowledge_methodology/next_steps.md` | 08_knowledge_methodology | 1 |
| `09_media_newsroom/next_steps.md` | 09_media_newsroom | 1 |
| `10_health_accessibility` | 10_health_accessibility | 2 |
| `superprojects/01_neuro_os/README.md` | superprojects | 3 |
| `superprojects/02_digital_caravan/README.md` | superprojects | 3 |
| `superprojects/03_caremate_total/README.md` | superprojects | 3 |
| `superprojects/04_neuroportal/README.md` | superprojects | 3 |

_…ещё 1 — см. queues/fidelity_jobs.json_