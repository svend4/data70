#!/usr/bin/env python3
"""Применить безопасные автофиксы из отчёта audit.

Что чинит:
1. Битые иллюстративные ссылки в naming_conventions.md и sources.md
2. Создаёт map.md и next_steps.md в 00_index/
3. Добавляет упоминание #N в 5 неотмеченных карточках

Запускать после полного аудита.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUDIT = Path(__file__).resolve().parents[1]


def fix_naming_conventions():
    p = ROOT / "00_index" / "naming_conventions.md"
    text = p.read_text(encoding="utf-8")
    # Заменяем пример-ссылки на правильные (для глубины 00_index/ или 01_X/YY/)
    fixes = {
        "[см. 02_ai_agents/01_micro_agents](../../02_ai_agents/01_micro_agents/README.md)":
            "[см. 02_ai_agents/01_micro_agents](../02_ai_agents/01_micro_agents/README.md)",
        "[analysis_04_social_law.md](../../../analysis_04_social_law.md)":
            "[analysis_04_social_law.md](../../analysis_04_social_law.md)",
    }
    changes = 0
    for old, new in fixes.items():
        if old in text:
            text = text.replace(old, new)
            changes += 1
    if changes:
        p.write_text(text, encoding="utf-8")
        print(f"[fix] naming_conventions.md: {changes} fixes")


def fix_sources():
    p = ROOT / "00_index" / "sources.md"
    text = p.read_text(encoding="utf-8")
    # 00_index/sources.md → ссылки уровня 00_index/ должны быть без двойного ../..
    fixes = {
        "[Каталог 88 тем](../../00_index/catalog_88_topics.md)":
            "[Каталог 88 тем](catalog_88_topics.md)",
        "[Папка 01_social_law](../../01_social_law/)":
            "[Папка 01_social_law](../01_social_law/)",
    }
    changes = 0
    for old, new in fixes.items():
        if old in text:
            text = text.replace(old, new)
            changes += 1
    if changes:
        p.write_text(text, encoding="utf-8")
        print(f"[fix] sources.md: {changes} fixes")


def add_index_map():
    p = ROOT / "00_index" / "map.md"
    if p.exists():
        return
    content = """# Карта папки 00_index/

Эта папка — навигационная для всего монорепо. В отличие от тематических
кластеров (01-10), здесь нет подпапок-тем, а есть **набор сквозных индексных файлов**.

## Файлы

- `README.md` — общее описание + список кластеров верхнего уровня
- `catalog_88_topics.md` — таблица всех 88 тем со ссылками
- `clusters_overview.md` — сравнение 11 кластеров
- `superprojects.md` — 5 суперпроектов (НейроОС, Караван, CareMate, НейроПортал, Forth-Рой)
- `inventions_index.md` — патентабельные идеи (24 шт.)
- `three_waves_roadmap.md` — стратегия монетизации
- `sources.md` — связь с первоисточниками в корне репозитория
- `naming_conventions.md` — правила именования

## Что считать «map» этой папки

Эта папка сама по себе — карта всего репо. См. также `STRUCTURE.md` в корне `monorepo/`.
"""
    p.write_text(content, encoding="utf-8")
    print("[fix] created 00_index/map.md")


def add_index_next_steps():
    p = ROOT / "00_index" / "next_steps.md"
    if p.exists():
        return
    content = """# Следующие шаги для папки 00_index/

Этой папке развиваться особо некуда — она навигационная. Возможные шаги:

## Поддержание актуальности

- При добавлении новой темы — обновить `catalog_88_topics.md`
- При появлении нового кластера — обновить `clusters_overview.md`
- При запуске audit — сверять с `_audit/reports/REPORT.md`

## Что может быть добавлено в будущем

- `glossary.md` — словарь терминов (SGB, MVP, RAG, NER и т.д.)
- `changelog.md` — история изменений монорепо
- `roadmap_2026_2027.md` — годовая карта развития

## Автогенерируемые файлы

Многие индексы здесь можно генерировать автоматически из реального состояния папок
(см. `_audit/scripts/00_inventory.py`). При большом росте — переход на генерацию.
"""
    p.write_text(content, encoding="utf-8")
    print("[fix] created 00_index/next_steps.md")


def add_topic_id_references():
    """Добавить упоминание #N в карточки, где оно отсутствует."""
    enrich_path = AUDIT / "queues" / "enrich.json"
    if not enrich_path.exists():
        return
    data = json.loads(enrich_path.read_text(encoding="utf-8"))

    # Только карточки с конкретной подпапкой (не cluster-level)
    fixes_done = 0
    for item in data:
        target = item.get("target_resolved")
        if not target or "/" not in target:
            continue  # cluster-level — пропускаем
        readme = ROOT / target / "README.md"
        if not readme.exists():
            continue
        content = readme.read_text(encoding="utf-8")
        topic_id = item["id"]
        topic_name = item["name"]

        # Если уже есть «#N» где-то — не трогаем (probably catch failed)
        if f"#{topic_id}" in content:
            continue

        # Добавляем строку в шапку после первого заголовка
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if line.startswith("**Тема каталога:**") or line.startswith("**Темы каталога:**"):
                # Уже есть, но без правильного формата — пропускаем
                break
            if line.startswith("# ") and i + 2 < len(lines):
                # Вставляем после первого пустого после заголовка
                for j in range(i + 1, min(i + 5, len(lines))):
                    if lines[j].strip() == "":
                        lines.insert(j + 1, f"**Тема каталога:** #{topic_id} ({topic_name})")
                        lines.insert(j + 2, "")
                        fixes_done += 1
                        break
                break

        new_content = "\n".join(lines)
        if new_content != content:
            readme.write_text(new_content, encoding="utf-8")

    print(f"[fix] topic_id annotations: {fixes_done}")


def main():
    fix_naming_conventions()
    fix_sources()
    add_index_map()
    add_index_next_steps()
    add_topic_id_references()
    print("[done] safe autofixes applied")


if __name__ == "__main__":
    main()
