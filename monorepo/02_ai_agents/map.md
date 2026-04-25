# Карта кластера 02_ai_agents

## Логические группы

```
02_ai_agents/
│
├── СЛОЙ ИСПОЛНИТЕЛЕЙ (микроагенты, локальные модели)
│   ├── 01_micro_agents              хаб 20+ связей
│   ├── 02_local_offline_models      хаб 18+ связей
│   ├── 03_one_bit_llm               для edge-устройств
│   └── 25_ollama_local              практический инструментарий
│
├── СЛОЙ АРХИТЕКТУР
│   ├── 04_mcp_protocol              стандарт связи агентов
│   ├── 05_collaboration_llm         коллаборация моделей
│   ├── 06_sparse_moe                разреженные эксперты
│   ├── 07_lcm_cognitive             когнитивные модели
│   ├── 08_kblam                     внешняя БЗ как контекст
│   ├── 09_dat_rag                   динамический RAG
│   ├── 10_neurosymbolic             символическая надстройка
│   ├── 11_diffusion_text            диффузионная генерация
│   ├── 12_kolmogorov_nn             альтернативная математика
│   ├── 13_three_level_arch          оперативный/тактический/стратегический
│   └── 14_bees_ants_bio             биомодель Пчёлы/Муравьи
│
├── СЛОЙ ОПЕРАЦИОННЫХ СИСТЕМ
│   ├── 15_warmwind_os               RPA-ОС
│   ├── 23_vast_ai_os                для дата-центров
│   └── 24_cloud_ru_evolution        российская гибридная
│
├── СЛОЙ РАСПРЕДЕЛЁННЫХ ВЫЧИСЛЕНИЙ
│   ├── 16_exo_p2p                   домашние устройства как кластер
│   ├── 20_decentralized_compute     Akash, Golem, iExec
│   └── 22_semantic_bus              шина данных между процессами
│
├── СЛОЙ ЖЕЛЕЗА
│   ├── 17_helix_parallelism         NVIDIA Helix + CXL
│   ├── 18_cim_chips                 Compute-in-Memory
│   └── 19_npu_risc_v                NPU + RISC-V для ИИ
│
└── СЛОЙ КАЧЕСТВА
    └── 21_livemcp_bench             бенчмарки агентов
```

## Хабы (наибольшее число связей)

| Подпапка | Связей | Роль |
|----------|--------|------|
| `01_micro_agents` (#13) | 20+ | Универсальный исполнитель |
| `02_local_offline_models` (#14) | 18+ | Фундамент оффлайн |
| `20_decentralized_compute` (#18) | 15+ | Инфраструктурный хаб |
| `09_dat_rag` (#11) | 14+ | Информационный поиск |

## Стек по слоям (для НейроОС)

```
UI (Tauri/PWA)                    ← из 05_software_automation
   ↓
Семантический автобус (NATS)      ← 22_semantic_bus
   ↓
Микроагенты (LangGraph + CrewAI)  ← 01_micro_agents
   ↓
RAG-движок (LlamaIndex+ChromaDB)  ← 09_dat_rag
   ↓
Локальные модели (Ollama)         ← 02_local_offline_models, 25_ollama_local
   ↓
Распределение (Exo + libp2p)      ← 16_exo_p2p
   ↓
Железо (NPU/CiM)                  ← 18_cim_chips, 19_npu_risc_v
```

## Что зрелое / что концепт

| Зрелость | Подпапки |
|----------|----------|
| **Производство (есть продукты)** | 02_local_offline_models, 25_ollama_local, 09_dat_rag |
| **Альфа/MVP-готовность** | 01_micro_agents, 04_mcp_protocol, 16_exo_p2p, 22_semantic_bus |
| **Концепты с расчётами** | 15_warmwind_os, 23_vast_ai_os, 13_three_level_arch |
| **Идеи и эссе** | 03_one_bit_llm, 06_sparse_moe, 12_kolmogorov_nn, 14_bees_ants_bio |
