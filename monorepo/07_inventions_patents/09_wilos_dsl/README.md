# 09 — WILOS — патентная карточка

**Тема каталога:** #57
**Категория:** C (Языки)
**Новизна:** ★★★★
**Применимость:** ★★★★
**Статус:** Опубликовать + патент на конкретные нюансы

## Суть изобретения

**WILOS** — Domain-Specific Language (DSL) для координации роя БПЛА. Включает:
- Лексику (токены)
- Грамматику (синтаксис)
- Семантику (значения)
- Архетипы поведения (готовые шаблоны: разведка, защита, перевозка)

**Ключевая инновация:** специализированный язык для роя, ориентированный на формальное описание поведения, а не отдельных команд.

## Prior art

| Аналог | Особенность | Чем отличается |
|--------|-------------|----------------|
| **Buzz** (McGill) | Академический DSL для роя | WILOS — практичный, с архетипами |
| **MAVLink** | Протокол для отдельного дрона | WILOS — для роя |
| **ROS2 launch** | Конфигурация запуска | WILOS — runtime поведение |
| **PDDL** | Планирование задач (academic) | WILOS — реалтайм |

## Что заявляется

1. **Грамматика языка** — формальная спецификация
2. **Архетипы поведения** — готовые конструкции (разведка, защита, рой)
3. **Компилятор** в Forth-байткод (для бортового исполнения)
4. **Семантика взаимодействия** — как dronы общаются друг с другом

## Стратегия (двойная)

1. **Open-source публикация** (GitHub + arXiv) — это **создаёт prior art** против конкурентов и привлекает разработчиков.
2. **Параллельно — патент** на конкретные нюансы реализации (компилятор, архетипы, оптимизации).

## Пример WILOS-кода

```wilos
swarm AgroScout {
  members: 10
  archetype: reconnaissance
  
  task scan_field(field_id) {
    distribute uniformly
    altitude: 50m
    overlap: 20%
    
    for each member {
      collect: NDVI
      timestamp: every 30s
    }
    
    on critical_finding {
      notify ground_station
      mark location
    }
    
    on battery_low {
      return to charging_hub
    }
  }
}
```

## Применение

- Forth-Рой (`superprojects/05_forth_swarm/`)
- Agro-Scout (`03_drones_skymediahub/11_agro_scout`)
- TetraDrone-кит для образования

## Партнёры (для академической публикации)

- **TU Dresden Autonomous Systems**
- **Fraunhofer IPMS**
- **DLR (Deutsches Zentrum für Luft- und Raumfahrt)**

## Связи

- `02_ai_agents/03_one_bit_llm` — Forth-интеллект исполняет WILOS
- `17_tcb_movement_lang` — связанный язык движений
- `22_forth_intelligence` — runtime
- `superprojects/05_forth_swarm/` — суперпроект
