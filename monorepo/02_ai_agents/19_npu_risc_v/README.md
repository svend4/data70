# 19 — NPU и RISC-V для GPU

**Темы каталога:** #16, #17
**Кластер A-J:** B
**Уровень готовности:** ★★★

## Что это

**NPU (Neural Processing Unit)** — специализированный ускоритель для нейронных вычислений в современных смартфонах, ноутбуках, ИИ-камерах. Apple Neural Engine, Qualcomm Hexagon NPU, AMD XDNA, Intel NPU.

**RISC-V для GPU** — открытая ISA для GPU/AI-ускорителей. Открытая альтернатива монополиям NVIDIA/AMD. Проекты: Vortex (Georgia Tech), VOLT, OpenGPU.

## Зачем это нужно

1. **NPU** — массово в каждом устройстве, инструмент для edge-ИИ
2. **RISC-V** — открытый стандарт без vendor lock-in
3. Сочетание: специализированные чипы под ИИ + открытая архитектура

## Применение

- **CareMate** — NPU смартфона/планшета для локальной обработки голоса (Whisper)
- **Forth-Рой** — RISC-V микроконтроллер с NPU как бортовая платформа
- **НейроОС** — использование NPU когда есть, GPU когда мощнее, CPU как fallback

## Современные NPU (мощность TOPS)

| Платформа | NPU TOPS | Используется |
|-----------|----------|--------------|
| Apple M4 | 38 | Apple Intelligence |
| Snapdragon 8 Gen 4 | 45 | Android AI |
| Intel Core Ultra | 11-48 | Copilot+ PCs |
| AMD Ryzen AI | 50 | Notebook AI |
| Tenstorrent Wormhole | 165 | Открытый ускоритель |

## Связи

- `02_local_offline_models` — целевая платформа
- `03_one_bit_llm` — идеально подходит для NPU
- `22_semantic_bus` — NPU как часть AI Runtime
- `18_cim_chips` — следующее поколение

## Дальнейшие шаги

1. Эксперимент: Whisper на Apple NPU (Apple Silicon Mac)
2. Тест Tenstorrent для open-source альтернативы NVIDIA
3. Эссе «Whisper на NPU» — для маркетинга CareMate

## Источники

- Tenstorrent Wormhole, Blackhole roadmaps
- RISC-V International AI Working Group
- Vortex GPU paper (GT)
