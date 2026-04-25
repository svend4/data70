# 14 — Contract Net Protocol для распределения задач

**Уровень готовности:** ★★★★

## Что это

**Contract Net Protocol (CNP)** — классический алгоритм распределения задач в распределённой системе агентов. Разработан Reid Smith (1980), стандарт для multi-agent systems.

В контексте роя 15 роботов используется для **динамического распределения** задач: какой робот делает что в данный момент.

## Принцип работы

```
1. ANNOUNCEMENT — Менеджер задач объявляет задачу всем роботам
   "Принести стакан воды из кухни в спальню"

2. BIDS — Каждый робот, который может, делает «ставку»:
   • Снегирь: «Я могу, но летать с водой опасно. Bid: low»
   • Енот: «Я могу. Bid: high (мягкий гриппер)»
   • Барсук: «Я могу, но я медленный. Bid: medium»

3. AWARD — Менеджер выбирает лучшую ставку и присуждает задачу
   • Енот выигрывает

4. CONFIRMATION — Енот подтверждает приём задачи

5. EXECUTION — Енот выполняет

6. RESULT — Енот возвращает результат

7. PAYMENT (если применимо) — Менеджер «выплачивает» энергию/токены
```

## Зачем именно CNP

| Альтернатива | Минус |
|--------------|-------|
| Centralized scheduling | Single point of failure |
| Round-robin | Не учитывает компетенции |
| Auction-based | Дороже в реализации |
| **Contract Net** | Простой + проверен временем |

## Расширения для роя зверей

1. **Multi-stage tasks** — задача разбивается на части, разные роботы делают разные стадии
2. **Coalition formation** — несколько роботов объединяются для одной задачи (тяжёлый предмет)
3. **Energy-aware bidding** — робот учитывает свой остаток батареи
4. **Skill-matched bidding** — bid рассчитывается по `12_yaml_manifests/skills`

## Реализация

```python
class ContractNetProtocol:
    def announce(self, task):
        # broadcast task to all robots in mesh
        for robot in self.swarm:
            robot.receive_announcement(task)
    
    def collect_bids(self, task, timeout=2.0):
        bids = []
        # wait for bids from robots
        return bids
    
    def award(self, task, bids):
        winner = max(bids, key=lambda b: b.score)
        return winner.robot
    
    def monitor_execution(self, task, robot):
        # detect failure, reassign if needed
        pass
```

## Связи

- `01_15_robot_zoo` — кто участвует
- `04_orchestrator_ros2` — где реализован
- `12_yaml_manifests` — источник параметров для bidding
- `02_ai_agents/01_micro_agents` — параллельный паттерн (микроагенты тоже могут CNP)

## Дальнейшие шаги

1. POC на 3 роботах-эмуляторах в Gazebo
2. Эссе «Contract Net for Heterogeneous Robot Swarms» (на arXiv)
3. Интеграция с Forth-интеллектом для бортового CNP-клиента
