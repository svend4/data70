# 12 — YAML-манифесты роботов

**Уровень готовности:** ★★★★★

## Что это

**Машиночитаемые YAML-описания** каждого из 15 роботов-зверей. Содержат:

- Идентификатор и тип
- Физические параметры (масса, размер, IP)
- Навыки (skills) — что робот умеет
- Сенсоры (датчики)
- Актуаторы (моторы, грипперы)
- Энергетика (батарея, время работы, время зарядки)
- Коммуникации (Wi-Fi, Matter, BLE)
- Совместимость с другими роботами

## Зачем YAML-формат

1. **Машиночитаемость** — оркестратор парсит и понимает возможности робота
2. **Версионируемость** — Git-friendly
3. **Открытый стандарт** — может стать референсом для отрасли
4. **Composer** — пользователь собирает рой из YAML-каталога
5. **Маркетинг** — open-source эстетика

## Полный пример (Снегирь)

```yaml
robot:
  id: snegir
  name: "Снегирь / Bullfinch"
  category: aerial-courier
  version: 1.0
  manufacturer: caremate-zoo
  
  physical:
    mass_kg: 0.5
    dimensions_mm: [180, 180, 80]
    ip_rating: IP54
    
  skills:
    - id: pickup
      payload_max_g: 200
    - id: indoor_navigation
      visibility_min_m: 0.5
    - id: voice_command_basic
      languages: [de, ru, en]
    - id: face_recognition
      latency_ms_max: 200
      
  sensors:
    - type: rgb_camera
      resolution_mp: 5
      fov_deg: 110
    - type: imu
      axes: 9
    - type: tof_distance
      range_m: 2
      
  actuators:
    - type: brushless_motor
      count: 4
      thrust_g_max: 200
    - type: gripper
      payload_max_g: 200
      
  energy:
    battery_type: lipo
    capacity_mah: 2000
    runtime_min_max: 25
    charge_time_min: 30
    
  comms:
    - protocol: wifi_5
      ssid_join: caremate-mesh
    - protocol: matter
      role: device
    - protocol: ros2_dds
      domain: caremate
      
  compatible_with:
    - id: caremate_hub
      version: ">=1.0"
    - id: orchestrator_ros2
      version: ">=2.0"
```

## Применение

- **Оркестратор** парсит манифесты и распределяет задачи
- **Маркетплейс роботов** — пользователь добавляет робота → манифест добавляет возможности
- **Документация** — автоматическая генерация PDF из YAML
- **Тестирование** — fuzzing на основе schema

## Стандарт схемы

Все манифесты соответствуют единой JSON-Schema (можно сгенерировать `manifest.schema.json`). Это обеспечивает:
- Валидацию
- Автодополнение в IDE
- Совместимость

## Связи

- `01_15_robot_zoo` — описывает какие
- `04_orchestrator_ros2` — потребитель манифестов
- `14_contract_net_protocol` — использует skills для распределения задач
- `02_ai_agents/22_semantic_bus` — параллель: семантические описания

## Дальнейшие шаги

1. Все 15 манифестов в едином GitHub-репо `caremate/robot-zoo-manifests`
2. JSON-Schema валидатор
3. CLI-tool для проверки манифеста
4. Web-каталог с фильтром по skills
