# Карта кластера 03_drones_skymediahub

## Логические группы

```
03_drones_skymediahub/
│
├── ЗОНТИЧНАЯ КОНЦЕПЦИЯ
│   └── 01_skymediahub_bavaria       экосистема
│
├── ОДНОРАЗОВЫЕ / ДЕШЁВЫЕ ДРОНЫ
│   ├── 02_tetradrone                из Tetra Pak (биоразлагаемый)
│   └── 11_agro_scout                сельхоз-мониторинг
│
├── СПЕЦИАЛИЗИРОВАННЫЕ ДРОНЫ
│   ├── 03_flamberrotor              волнообразные лопасти
│   ├── 06_pentagrammacopter         5-роторный
│   ├── 07_water_drone_hydrofoil     водный
│   ├── 10_molniya2_vtol             VTOL разведка
│   └── 13_pathfinder                разведка местности
│
├── ТЯЖЁЛЫЕ ПЛАТФОРМЫ
│   ├── 05_baba_yaga                 тяжёлый гражданский
│   └── 12_ufo_shield                купольный
│
├── ИНФРАСТРУКТУРНЫЕ
│   ├── 04_optofiber_chain           магистраль 100 км
│   └── 09_drone_compute_hub         ЦОД для дронов
│
├── ОПТИКА
│   └── 08_4k_compound_camera        28 матриц 600×600
│
├── ПОЛИТИКА И ПАРТНЁРСТВА
│   ├── 14_dual_use_concept          архитектура использования
│   ├── 15_partner_letters           письма (DE)
│   ├── 16_fraunhofer_techhub        контакты
│   └── 17_bundeswehr_conversion     UGV-конверсия
```

## Связи между подпапками

- `01_skymediahub_bavaria` — содержит ссылки на все 13 проектов дронов
- `02_tetradrone` + `08_4k_compound_camera` → дешёвый агродрон с высокой оптикой
- `04_optofiber_chain` + `09_drone_compute_hub` → инфраструктура связи
- `15_partner_letters` отправлены в `16_fraunhofer_techhub` и `17_bundeswehr_conversion`

## Связи с патентами (`07_inventions_patents`)

| Подпапка дронов | Патентная папка |
|----------------|-----------------|
| `02_tetradrone` | `07_inventions_patents/01_tetradrone` (★★★★★) |
| `03_flamberrotor` | `07_inventions_patents/02_flamberrotor` (★★★★★) |
| `04_optofiber_chain` | `07_inventions_patents/03_optofiber_drone_chain` (★★★★) |
| `06_pentagrammacopter` | `07_inventions_patents/04_pentagrammacopter` (★★★) |
| `07_water_drone_hydrofoil` | `07_inventions_patents/05_water_drone` (★★★) |
| `08_4k_compound_camera` | `07_inventions_patents/16_4k_compound_camera` (★★★★) |

## Уровни проработки

| Подпапка | Уровень |
|----------|---------|
| 01_skymediahub_bavaria | ★★★★ — концепция + 13 проектов |
| 02_tetradrone | ★★★★ — описание + сравнение с Sypaq |
| 03_flamberrotor | ★★★ — теория, нужен CFD |
| 04_optofiber_chain | ★★★★★ — расчёт завершён |
| 05_baba_yaga | ★★★ — концепт |
| 06_pentagrammacopter | ★★ — ранний концепт |
| 07_water_drone_hydrofoil | ★★★ — описание конструкции |
| 08_4k_compound_camera | ★★★★ — детальный расчёт |
| 09_drone_compute_hub | ★★★ — концепт |
| 10_molniya2_vtol | ★★★ — спецификация |
| 11_agro_scout | ★★★ — концепт |
| 12_ufo_shield | ★★ — идея |
| 13_pathfinder | ★★ — идея |
| 14_dual_use_concept | ★★★★ — обоснование |
| 15_partner_letters | ★★★★★ — готовы к отправке |
| 16_fraunhofer_techhub | ★★★ — контакты |
| 17_bundeswehr_conversion | ★★★★ — концепт + аргументация |
