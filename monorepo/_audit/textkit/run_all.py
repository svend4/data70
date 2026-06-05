#!/usr/bin/env python3
"""run_all.py — полный машинный аудит data70 через все портированные scripts/.

Прогоняет каждый improve_*.py из lib/ как отдельный процесс с TEXTKIT_DOCS=monorepo.
Собирает: код возврата, время, размер вывода, stdout/stderr. Пишет сводный отчёт.

Запуск:
    cd monorepo/_audit/textkit
    python3 run_all.py

Опции:
    --readme-as-content   установить TEXTKIT_README_IS_CONTENT=1 (для data70 — нужно)
    --timeout SEC         таймаут на скрипт (по умолчанию 120 сек)
    --skip PATTERN ...    регексп(ы) — какие скрипты пропустить
    --only PATTERN ...    регексп(ы) — только эти скрипты
    --dry-run             показать, что бы запустилось, без исполнения
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
LIB = HERE / "lib"
REPORTS = HERE.parent / "reports"
REPORTS.mkdir(exist_ok=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--docs", default=str(Path(HERE).parent.parent),
                    help="Путь к корпусу markdown (по умолч. monorepo/)")
    ap.add_argument("--readme-as-content", action="store_true", default=True)
    ap.add_argument("--no-readme-as-content", dest="readme_as_content", action="store_false")
    ap.add_argument("--timeout", type=int, default=120)
    ap.add_argument("--skip", nargs="*", default=[])
    ap.add_argument("--only", nargs="*", default=[])
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    env = os.environ.copy()
    env["TEXTKIT_DOCS"] = args.docs
    if args.readme_as_content:
        env["TEXTKIT_README_IS_CONTENT"] = "1"
    env["PYTHONPATH"] = str(LIB) + os.pathsep + env.get("PYTHONPATH", "")

    scripts = sorted(LIB.glob("improve_*.py"))

    if args.only:
        rx_only = [re.compile(p) for p in args.only]
        scripts = [s for s in scripts if any(r.search(s.name) for r in rx_only)]
    if args.skip:
        rx_skip = [re.compile(p) for p in args.skip]
        scripts = [s for s in scripts if not any(r.search(s.name) for r in rx_skip)]

    print(f"Корпус:    {args.docs}")
    print(f"Скриптов:  {len(scripts)}")
    print(f"Таймаут:   {args.timeout} сек")
    print()

    if args.dry_run:
        for s in scripts:
            print(f"  would-run  {s.name}")
        return 0

    results = []
    t_start = time.time()
    for i, s in enumerate(scripts, 1):
        t0 = time.time()
        try:
            proc = subprocess.run(
                [sys.executable, str(s)],
                cwd=LIB,
                env=env,
                capture_output=True,
                text=True,
                timeout=args.timeout,
            )
            rc = proc.returncode
            out = proc.stdout
            err = proc.stderr
            status = "ok" if rc == 0 else "err"
        except subprocess.TimeoutExpired:
            rc = -1
            out, err = "", "TIMEOUT"
            status = "timeout"
        except Exception as e:
            rc = -2
            out, err = "", str(e)
            status = "crash"
        dt = time.time() - t0

        # короткий маркер для прогресса
        flag = {"ok": "✓", "err": "✗", "timeout": "⏱", "crash": "💥"}[status]
        print(f"  [{i:3d}/{len(scripts)}] {flag} {s.name:<45s} {dt:6.2f}s rc={rc}")

        results.append({
            "script": s.name,
            "status": status,
            "rc": rc,
            "duration_s": round(dt, 3),
            "stdout_tail": out.splitlines()[-3:] if out else [],
            "stderr_tail": err.splitlines()[-5:] if err else [],
        })

    total = time.time() - t_start
    counts = {k: 0 for k in ["ok", "err", "timeout", "crash"]}
    for r in results:
        counts[r["status"]] += 1

    print()
    print(f"Итого: ok={counts['ok']}  err={counts['err']}  "
          f"timeout={counts['timeout']}  crash={counts['crash']}   "
          f"общее время {total:.1f} сек")

    # сохраняем JSON
    out_json = REPORTS / "full_machine_audit.json"
    out_json.write_text(json.dumps({
        "docs": args.docs,
        "readme_as_content": args.readme_as_content,
        "total_scripts": len(scripts),
        "counts": counts,
        "duration_total_s": round(total, 2),
        "results": results,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"JSON: {out_json}")

    # пишем краткий markdown-сводник
    md = REPORTS / "full_machine_audit.md"
    lines = [
        "# Полный машинный аудит data70 — все портированные lorenzo-инструменты",
        "",
        f"- Корпус: `{args.docs}`",
        f"- README=контент: {args.readme_as_content}",
        f"- Скриптов запущено: **{len(scripts)}**",
        f"- ✓ ok: **{counts['ok']}**  ✗ err: **{counts['err']}**  "
        f"⏱ timeout: **{counts['timeout']}**  💥 crash: **{counts['crash']}**",
        f"- Общее время: {total:.1f} сек",
        "",
        "## Скрипты с ошибками",
        "",
    ]
    failed = [r for r in results if r["status"] != "ok"]
    if not failed:
        lines.append("Нет.")
    else:
        lines.append("| Скрипт | Статус | rc | Последние строки stderr |")
        lines.append("|--------|--------|---:|--------------------------|")
        for r in failed:
            tail = " / ".join(r["stderr_tail"])[:160].replace("|", "\\|")
            lines.append(f"| `{r['script']}` | {r['status']} | {r['rc']} | {tail} |")

    lines += [
        "",
        "## Успешные скрипты (топ-30 по длительности)",
        "",
        "| Скрипт | Время (с) | Последние строки stdout |",
        "|--------|----------:|--------------------------|",
    ]
    success = sorted([r for r in results if r["status"] == "ok"],
                     key=lambda r: -r["duration_s"])[:30]
    for r in success:
        tail = " / ".join(r["stdout_tail"])[:160].replace("|", "\\|")
        lines.append(f"| `{r['script']}` | {r['duration_s']} | {tail} |")

    md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"MD:   {md}")
    return 0 if counts["crash"] + counts["timeout"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
