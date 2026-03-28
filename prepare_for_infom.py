#!/usr/bin/env python3
"""
Подготовка данных из 1105 разговоров ChatGPT для InfoM GraphRAG.

Извлекает из каждого разговора:
- Название (сущность)
- Тематический кластер
- Ключевые концепции
- Связи между разговорами через общие темы

Выход: JSON-файл для загрузки в InfoM через infom_mcp.py
"""
import re
import json
import os
from collections import defaultdict

CHAT_DIR = os.path.join(os.path.dirname(__file__), "chat_export")
OUTPUT = os.path.join(os.path.dirname(__file__), "infom_import.json")


# ── Тематические кластеры и их архетипы ─────────────────────────────────────

THEME_RULES = [
    # (keywords, theme_name, archetype)
    (["социал", "pflege", "persönliches budget", "персональный бюджет", "инвалид",
      "behindert", "widerspruch", "sgb", "antrag", "sozialgericht", "pflegegrad"],
     "Социальное право", "MSCF"),

    (["дрон", "бпла", "uav", "квадрокоптер", "fpv", "protector", "ugv",
      "молния", "tetradrone", "skymedia", "wilos", "flamber"],
     "Дроны и БПЛА", "MDCO"),

    (["робот", "robot", "servo", "рой", "колесо", "тележк", "механизм"],
     "Робототехника", "MDEO"),

    (["нейросет", "llm", "gpt", "модел", "1-bit", "ollama", "langchain",
      "rag", "agent", "агент", "мультиагент", "moltbook"],
     "ИИ и нейросети", "ADCO"),

    (["make.com", "n8n", "автоматизац", "automation", "no-code"],
     "Автоматизация", "ADEO"),

    (["бизнес", "стартап", "startup", "маркет", "монетиз", "франшиз",
      "b2b", "metaworld", "skymediahub"],
     "Бизнес и стартапы", "MDCF"),

    (["программиров", "github", "код", "code", "react", "python", "html",
      "javascript", "калькулятор", "вайб"],
     "Программирование", "ADCO"),

    (["золот", "сечени", "фибоначч", "пропорц", "математи", "геометр",
      "пирамид", "дуализм", "двойственност"],
     "Математика и гармония", "ASCO"),

    (["медицин", "здоров", "болезн", "врач", "эвтаназ", "pflege",
      "caremate", "пожил", "уход"],
     "Медицина и уход", "MDEF"),

    (["офис", "smartoffice", "виртуальн", "экстранет", "crm"],
     "Виртуальный офис", "ADEO"),

    (["журналист", "медиа", "osint", "видео", "youtube", "блог"],
     "Медиа и журналистика", "MDEO"),

    (["велосипед", "bicycle", "транспорт", "кочев", "караван"],
     "Транспорт и мобильность", "MDEO"),

    (["цветоч", "магазин", "blumen", "shopify", "дропшип"],
     "E-commerce", "MDCF"),

    (["кластер", "сервер", "raspberry", "supermicro", "docker"],
     "Серверы и инфраструктура", "MSCO"),

    (["буддизм", "пхова", "таро", "у-синь", "эзотери", "медитац",
      "трансгуманизм", "астролог"],
     "Философия и духовность", "ASEF"),

    (["тсб", "бой", "крюков", "касаткин", "движени"],
     "Боевые искусства (ТСБ)", "MDEF"),

    (["internet function", "нейроос", "пирамида знаний", "infom",
      "четырёхуровнев", "zettelkasten"],
     "Управление знаниями", "ASCO"),
]


def classify_conversation(title: str, body: str) -> tuple[str, str]:
    """Определяет тему и архетип по заголовку и телу."""
    text = (title + " " + body[:500]).lower()
    best_score = 0
    best_theme = "Разное"
    best_arch = "ASEF"

    for keywords, theme, arch in THEME_RULES:
        score = sum(1 for kw in keywords if kw in text)
        if score > best_score:
            best_score = score
            best_theme = theme
            best_arch = arch

    return best_theme, best_arch


def extract_key_concepts(title: str, body: str, max_concepts: int = 5) -> list[str]:
    """Извлекает ключевые концепции из разговора (простой TF подход)."""
    # Берём заголовок + первые 2000 символов тела
    text = (title + " " + body[:2000]).lower()

    # Удаляем служебные слова
    stop_words = {
        "это", "что", "как", "для", "или", "при", "так", "все", "они",
        "его", "она", "мне", "вам", "нас", "вот", "уже", "ещё", "тоже",
        "быть", "если", "есть", "будет", "было", "были", "может", "нужно",
        "можно", "также", "очень", "просто", "только", "которые", "который",
        "которая", "которое", "пользователь", "ассистент", "привет",
        "спасибо", "пожалуйста", "здравствуйте", "the", "and", "for",
        "that", "this", "with", "from", "have", "are", "was", "not",
    }

    # Извлекаем слова 4+ символов
    words = re.findall(r'[а-яёa-z]{4,}', text)
    word_freq = defaultdict(int)
    for w in words:
        if w not in stop_words:
            word_freq[w] += 1

    # Топ по частоте
    top = sorted(word_freq.items(), key=lambda x: -x[1])[:max_concepts]
    return [w for w, _ in top]


def parse_all_conversations() -> list[dict]:
    """Парсит все файлы chat_export и возвращает список разговоров."""
    conversations = []

    for i in range(1, 154):
        fname = os.path.join(CHAT_DIR, f"chat_export_{i:03d}.txt")
        if not os.path.exists(fname):
            continue

        with open(fname, "r") as f:
            content = f.read()

        parts = re.split(r"={80}\nРАЗГОВОР (\d+)/1105: (.+)\n={80}", content)

        for j in range(1, len(parts) - 2, 3):
            num = int(parts[j])
            title = parts[j + 1].strip()
            body = parts[j + 2].strip()

            # Пропускаем тривиальные
            msg_count = body.count("--- ПОЛЬЗОВАТЕЛЬ ---") + body.count("--- АССИСТЕНТ ---")
            char_count = len(body)

            if char_count < 200 or msg_count < 2:
                continue

            theme, archetype = classify_conversation(title, body)
            concepts = extract_key_concepts(title, body)

            conversations.append({
                "num": num,
                "title": title,
                "theme": theme,
                "archetype": archetype,
                "concepts": concepts,
                "msg_count": msg_count,
                "char_count": char_count,
                "depth": min(5, 1 + char_count // 50000),  # 1-5 scale
            })

    return conversations


def build_infom_graph(conversations: list[dict]) -> dict:
    """
    Строит граф для InfoM:
    - Ноды = темы (кластеры) + ключевые проекты + концепции
    - Рёбра = принадлежность разговоров к темам, связи через общие концепции
    """
    nodes = []
    edges = []
    node_ids = set()

    # 1. Ноды-темы (кластеры)
    theme_stats = defaultdict(lambda: {"count": 0, "chars": 0, "convs": []})
    for conv in conversations:
        t = conv["theme"]
        theme_stats[t]["count"] += 1
        theme_stats[t]["chars"] += conv["char_count"]
        theme_stats[t]["convs"].append(conv["num"])

    for theme, stats in theme_stats.items():
        tid = f"theme_{theme.replace(' ', '_').lower()}"
        # Определяем архетип темы по первому совпадению
        arch = "ASEF"
        for conv in conversations:
            if conv["theme"] == theme:
                arch = conv["archetype"]
                break

        nodes.append({
            "id": tid,
            "label": theme,
            "archetype": arch,
            "weight": min(1.0, stats["count"] / 50),
            "metadata": {
                "type": "theme",
                "conversations": stats["count"],
                "total_chars": stats["chars"],
            }
        })
        node_ids.add(tid)

    # 2. Ноды — ключевые проекты (разговоры с depth >= 3)
    deep_convs = [c for c in conversations if c["depth"] >= 3]
    for conv in deep_convs[:100]:  # максимум 100 ключевых
        cid = f"conv_{conv['num']}"
        nodes.append({
            "id": cid,
            "label": conv["title"][:60],
            "archetype": conv["archetype"],
            "weight": min(1.0, conv["char_count"] / 500000),
            "metadata": {
                "type": "project",
                "num": conv["num"],
                "messages": conv["msg_count"],
                "chars": conv["char_count"],
                "depth": conv["depth"],
                "concepts": conv["concepts"],
            }
        })
        node_ids.add(cid)

        # Ребро: проект → тема
        tid = f"theme_{conv['theme'].replace(' ', '_').lower()}"
        if tid in node_ids:
            edges.append({
                "source": cid,
                "target": tid,
                "label": "принадлежит теме",
                "weight": 0.8,
            })

    # 3. Ноды — ключевые концепции (частые через все разговоры)
    concept_freq = defaultdict(int)
    concept_themes = defaultdict(set)
    concept_convs = defaultdict(list)

    for conv in conversations:
        for c in conv["concepts"]:
            concept_freq[c] += 1
            concept_themes[c].add(conv["theme"])
            if len(concept_convs[c]) < 10:
                concept_convs[c].append(conv["num"])

    # Берём концепции, встречающиеся в 3+ разговорах и 2+ темах
    cross_concepts = [
        (c, freq) for c, freq in concept_freq.items()
        if freq >= 3 and len(concept_themes[c]) >= 2
    ]
    cross_concepts.sort(key=lambda x: -x[1])

    for concept, freq in cross_concepts[:80]:  # макс 80
        cid = f"concept_{concept}"
        if cid in node_ids:
            continue
        nodes.append({
            "id": cid,
            "label": concept,
            "archetype": "ASCO",
            "weight": min(1.0, freq / 20),
            "metadata": {
                "type": "concept",
                "frequency": freq,
                "themes": list(concept_themes[concept]),
            }
        })
        node_ids.add(cid)

        # Рёбра: концепция → все связанные темы
        for theme in concept_themes[concept]:
            tid = f"theme_{theme.replace(' ', '_').lower()}"
            if tid in node_ids:
                edges.append({
                    "source": cid,
                    "target": tid,
                    "label": "встречается в",
                    "weight": 0.5,
                })

    # 4. Рёбра между темами (через общие концепции)
    theme_pairs = defaultdict(int)
    for concept, themes in concept_themes.items():
        themes_list = list(themes)
        for i in range(len(themes_list)):
            for j in range(i + 1, len(themes_list)):
                pair = tuple(sorted([themes_list[i], themes_list[j]]))
                theme_pairs[pair] += concept_freq[concept]

    for (t1, t2), strength in sorted(theme_pairs.items(), key=lambda x: -x[1])[:30]:
        tid1 = f"theme_{t1.replace(' ', '_').lower()}"
        tid2 = f"theme_{t2.replace(' ', '_').lower()}"
        if tid1 in node_ids and tid2 in node_ids:
            edges.append({
                "source": tid1,
                "target": tid2,
                "label": "связана через концепции",
                "weight": min(0.9, strength / 50),
                "directed": False,
            })

    return {
        "metadata": {
            "source": "ChatGPT export (1105 conversations)",
            "total_conversations": len(conversations),
            "deep_conversations": len(deep_convs),
            "themes": len(theme_stats),
            "cross_concepts": len(cross_concepts),
        },
        "nodes": nodes,
        "edges": edges,
    }


def main():
    print("Парсинг разговоров...", flush=True)
    conversations = parse_all_conversations()
    print(f"  Содержательных разговоров: {len(conversations)}")

    print("Построение графа...", flush=True)
    graph = build_infom_graph(conversations)
    print(f"  Нод:  {len(graph['nodes'])}")
    print(f"  Рёбер: {len(graph['edges'])}")

    # Статистика по темам
    print("\nТемы:")
    theme_nodes = [n for n in graph["nodes"] if n["metadata"].get("type") == "theme"]
    for tn in sorted(theme_nodes, key=lambda x: -x["metadata"]["conversations"]):
        print(f"  {tn['label']:30s} {tn['metadata']['conversations']:4d} разговоров  "
              f"{tn['metadata']['total_chars']//1024:5d} КБ  [{tn['archetype']}]")

    # Сохраняем
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)
    print(f"\nСохранено: {OUTPUT} ({os.path.getsize(OUTPUT) // 1024} КБ)")

    # Также сохраняем в формате InfoM snapshot (для прямой загрузки)
    snapshot = {
        "saved_at": "2026-03-28T00:00:00",
        "nodes": [
            {
                "id": n["id"],
                "label": n["label"],
                "archetype": n.get("archetype", ""),
                "weight": n.get("weight", 1.0),
                "embedding": [],  # InfoM вычислит через SemanticAdapter
                "metadata": n.get("metadata", {}),
            }
            for n in graph["nodes"]
        ],
        "edges": [
            {
                "source": e["source"],
                "target": e["target"],
                "label": e.get("label", "связан"),
                "weight": e.get("weight", 0.7),
                "directed": e.get("directed", True),
            }
            for e in graph["edges"]
        ],
    }
    snapshot_path = os.path.join(os.path.dirname(__file__), "infom_snapshot.json")
    with open(snapshot_path, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2)
    print(f"Снапшот: {snapshot_path} ({os.path.getsize(snapshot_path) // 1024} КБ)")


if __name__ == "__main__":
    main()
