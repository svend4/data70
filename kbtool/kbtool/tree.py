"""Построение дерева папок из кластеров — «хаос → структура».

Берёт результат кластеризации и раскладывает файлы по тематическим папкам.

Режимы (по убыванию безопасности):
  dry-run     показать план, ничего не трогать         (по умолчанию)
  out DIR     материализовать КОПИЮ дерева в DIR        (оригинал цел)
  apply       переместить файлы in-place (git mv)       (деструктивно, opt-in)
"""

from __future__ import annotations

import re
import shutil
import subprocess
from collections import Counter
from pathlib import Path

from .corpus import Doc, STOPWORDS

# Термины, бесполезные как имена папок
BAD_LABEL = STOPWORDS | {
    "readme", "это", "что", "the", "for", "мес", "тема", "уровень",
    "готовности", "каталога", "type", "name", "файлов", "также",
}


def _slug(terms: list[str], maxlen: int = 30) -> str:
    """term-list → ascii-safe snake_case ярлык папки."""
    picked = [t for t in terms if t not in BAD_LABEL and len(t) >= 3][:2]
    if not picked:
        # все термины бесполезны как имя — честно помечаем misc
        return "misc"
    raw = "_".join(picked)
    # транслитерация кириллицы для максимальной переносимости ФС
    table = {
        "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "e",
        "ж": "zh", "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m",
        "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u",
        "ф": "f", "х": "h", "ц": "c", "ч": "ch", "ш": "sh", "щ": "sch",
        "ъ": "", "ы": "y", "ь": "", "э": "e", "ю": "yu", "я": "ya",
    }
    out = "".join(table.get(ch, ch) for ch in raw.lower())
    out = re.sub(r"[^a-z0-9_]+", "_", out).strip("_")
    return (out or "misc")[:maxlen]


def plan_tree(docs: list[Doc], clusters: list[dict],
              misc_threshold: int = 1) -> list[dict]:
    """Строит план перемещений: src_rel → dst_rel.

    Кластеры размера <= misc_threshold идут в 00_misc/.
    """
    # имя папки на кластер
    used: Counter = Counter()
    cluster_dir: dict[int, str] = {}
    # сначала крупные кластеры получают номера 01..NN, мелочь — 00_misc
    big = [c for c in clusters if c["size"] > misc_threshold]
    big.sort(key=lambda c: -c["size"])
    for idx, c in enumerate(big, 1):
        terms = [t.strip() for t in c["label"].split(",")]
        base = _slug(terms)
        used[base] += 1
        suffix = f"_{used[base]}" if used[base] > 1 else ""
        cluster_dir[id(c)] = f"{idx:02d}_{base}{suffix}"

    plan: list[dict] = []
    seen_dst: set[str] = set()
    for c in clusters:
        folder = cluster_dir.get(id(c), "00_misc")
        for src_rel in c["files"]:
            name = Path(src_rel).name
            dst = f"{folder}/{name}"
            # коллизии имён внутри папки → суффикс _2, _3
            n = 2
            while dst in seen_dst:
                stem = Path(name).stem
                ext = Path(name).suffix
                dst = f"{folder}/{stem}_{n}{ext}"
                n += 1
            seen_dst.add(dst)
            plan.append({"src": src_rel, "dst": dst, "cluster": c["label"]})
    return plan


def render_plan(plan: list[dict]) -> str:
    by_folder: dict[str, list[dict]] = {}
    for p in plan:
        folder = p["dst"].split("/", 1)[0]
        by_folder.setdefault(folder, []).append(p)
    lines = [f"# План дерева: {len(plan)} файлов → {len(by_folder)} папок", ""]
    for folder in sorted(by_folder):
        items = by_folder[folder]
        lines.append(f"## {folder}/ ({len(items)})")
        for p in items[:15]:
            lines.append(f"  {p['src']}  →  {p['dst']}")
        if len(items) > 15:
            lines.append(f"  …ещё {len(items) - 15}")
        lines.append("")
    return "\n".join(lines)


def materialize(plan: list[dict], src_root: Path, out_dir: Path) -> int:
    """Копирует файлы в новое дерево out_dir. Оригинал не трогается."""
    out_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for p in plan:
        src = src_root / p["src"]
        dst = out_dir / p["dst"]
        dst.parent.mkdir(parents=True, exist_ok=True)
        try:
            shutil.copy2(src, dst)
            count += 1
        except Exception:
            pass
    return count


def apply_inplace(plan: list[dict], src_root: Path, use_git: bool = True) -> int:
    """Перемещает файлы in-place. Деструктивно. Пытается git mv."""
    count = 0
    git_ok = use_git and (src_root / ".git").exists()
    if not git_ok:
        # ищем git-корень выше
        cur = src_root
        for _ in range(5):
            if (cur / ".git").exists():
                git_ok = use_git
                break
            cur = cur.parent
    for p in plan:
        src = src_root / p["src"]
        dst = src_root / p["dst"]
        if src.resolve() == dst.resolve():
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        moved = False
        if git_ok:
            try:
                subprocess.run(["git", "mv", "-f", str(src), str(dst)],
                               cwd=src_root, check=True,
                               capture_output=True)
                moved = True
            except Exception:
                moved = False
        if not moved:
            try:
                shutil.move(str(src), str(dst))
                moved = True
            except Exception:
                pass
        if moved:
            count += 1
    return count
