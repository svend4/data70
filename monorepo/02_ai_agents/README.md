# 02 — ИИ, агенты и инфраструктура

**~100 разговоров · 4.1 МБ текста · уровень готовности 4/5**

## О чём этот кластер

Сводный кластер всего, что относится к **искусственному интеллекту, агентам, моделям, инфраструктуре**. Объединяет аналитические кластеры **A** (Архитектура ИИ нового поколения) и **B** (Инфраструктура и платформы ИИ) из `part12_catalog.md`.

Тематическое разделение:
- **Подпапки 01–02:** агенты и локальные модели (фундамент всего)
- **Подпапки 03–14:** новые архитектуры и парадигмы (1-Bit, MoE, LCM, RAG, KBLaM, Neurosymbolic и т.д.)
- **Подпапки 15–25:** инфраструктура (ОС, P2P, чипы, шины, бенчмарки)

## Подпапки

### Агенты и локальные модели
| № | Подпапка | Тема |
|---|----------|------|
| 01 | `01_micro_agents` | #13 Micro-ИИ агенты (хаб, 20+ связей) |
| 02 | `02_local_offline_models` | #14 Локальные нейросети оффлайн (хаб, 18+ связей) |
| 03 | `03_one_bit_llm` | #3 1-Bit LLM / квантизация |

### Архитектуры
| № | Подпапка | Тема |
|---|----------|------|
| 04 | `04_mcp_protocol` | Model Context Protocol |
| 05 | `05_collaboration_llm` | #1 Коллаборация LLM-моделей |
| 06 | `06_sparse_moe` | #2 Sparse Expert Models / MoE |
| 07 | `07_lcm_cognitive` | #4 LCM (Large Cognitive Models) |
| 08 | `08_kblam` | #5, #31 KBLaM |
| 09 | `09_dat_rag` | #7 Dynamic Alpha Tuning + #11 RAG |
| 10 | `10_neurosymbolic` | #9 Neurosymbolic AI |
| 11 | `11_diffusion_text` | #10 Диффузионная генерация текста |
| 12 | `12_kolmogorov_nn` | #8 Нейросети по Колмогорову |
| 13 | `13_three_level_arch` | #32, #56 Трёхуровневая архитектура |
| 14 | `14_bees_ants_bio` | Биомодель «Пчёлы и Муравьи» |

### Инфраструктура
| № | Подпапка | Тема |
|---|----------|------|
| 15 | `15_warmwind_os` | #43 Warmwind OS |
| 16 | `16_exo_p2p` | #42 Exo P2P |
| 17 | `17_helix_parallelism` | #15, #37, #40 NVIDIA Helix + CXL |
| 18 | `18_cim_chips` | #6, #54 Compute-in-Memory + Techifab |
| 19 | `19_npu_risc_v` | #16, #17 RISC-V GPU + NPU |
| 20 | `20_decentralized_compute` | #18, #88 Децентрализованные вычисления |
| 21 | `21_livemcp_bench` | #19 LiveMCP-101 бенчмарк |
| 22 | `22_semantic_bus` | #85 Семантический автобус |
| 23 | `23_vast_ai_os` | #72 VAST AI OS |
| 24 | `24_cloud_ru_evolution` | #73 Cloud.ru Evolution Stack AI |
| 25 | `25_ollama_local` | Ollama, llama.cpp, GGUF локально |

## Зачем это нужно

1. **Технологический фундамент** для НейроОС, НейроПортала, CareMate, Forth-Роя
2. **Patentable идеи:** Forth-интеллект, биомодель Пчёлы/Муравьи, семантический автобус
3. **R&D-направление:** SAB Sachsen, Horizon Europe, EXIST-Grants

## Связи с другими кластерами

- `05_software_automation` — ИИ применяется через no-code и Internet Function OS
- `08_knowledge_methodology` — пирамида знаний поверх RAG
- `04_robotics_caremate` — рой роботов использует Forth-интеллект
- `07_inventions_patents` — патентные идеи

## Источники

- `analysis_ai_topics.md` (60 КБ — главный источник)
- `extracted_ai_topics.txt` (332 КБ)
- `extracted_ai_topics_batch2.txt` (200 КБ)
- `part10_deep_analysis.md`, `part10_new_topics.md`
- `part13_tech_stacks.md` — стеки 5 суперпроектов
