"""Агрегированный health-балл из проверок и аналитики."""

from __future__ import annotations


def score(inv: dict, links: dict, struct: dict,
          dups: list, clusters: list) -> dict:
    metrics = []

    # ссылки
    lc = links["counts"]
    link_score = 100 if lc["broken"] == 0 else max(0, 100 - lc["broken"] * 5)
    metrics.append(("Внутренние ссылки", f"{lc['broken']} сломано", link_score))

    # структура
    iss = len(struct["issues"])
    struct_score = 100 if iss == 0 else max(0, 100 - iss * 3)
    metrics.append(("Структура (README)", f"{iss} проблем", struct_score))

    # дубликаты
    dup_score = 100 if not dups else max(0, 100 - len(dups) * 5)
    metrics.append(("Дубликаты", f"{len(dups)} похожих пар", dup_score))

    # связность (доля файлов в кластерах >1)
    total_files = sum(c["size"] for c in clusters) or 1
    grouped = sum(c["size"] for c in clusters if c["size"] > 1)
    cohesion = round(grouped / total_files * 100)
    metrics.append(("Тематическая связность", f"{cohesion}% в кластерах", cohesion))

    overall = round(sum(m[2] for m in metrics) / len(metrics))
    return {"overall": overall, "metrics": metrics}
