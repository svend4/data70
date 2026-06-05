"""Мини-HTTP-дашборд: health, search, ask. Stdlib http.server, без зависимостей.

Эндпоинты:
  GET /              HTML-дашборд
  GET /api/health    JSON health
  GET /api/search?q=...&k=5&method=bm25
  GET /api/ask?q=...&k=5
"""

from __future__ import annotations

import html
import json
import urllib.parse as up
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from .checks import inventory, check_links, check_structure
from .corpus import load
from .analyze import cluster, dedup
from .health import score
from .profile import Profile
from .rag import build_index, load_index, search, answer


class _State:
    docs: Path
    exclude: set[str]
    profile: Profile
    index: dict | None = None


def _refresh_index(s: _State) -> dict:
    s.index = build_index(s.docs, s.profile, s.exclude)
    return s.index


def _health(s: _State) -> dict:
    corpus = load(s.docs, s.profile, exclude_dirs=s.exclude)
    inv = inventory(s.docs, s.exclude)
    links = check_links(s.docs, s.exclude)
    struct = check_structure(s.docs, exclude=s.exclude)
    dups = dedup(corpus)
    cl = cluster(corpus, threshold=0.15)
    h = score(inv, links, struct, dups, cl)
    h["inventory"] = inv
    h["clusters_count"] = len(cl)
    return h


def make_handler(state: _State):
    class H(BaseHTTPRequestHandler):
        def log_message(self, *a, **kw):  # тише в консоль
            pass

        def _json(self, data, code=200):
            body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _html(self, body: str, code=200):
            data = body.encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            parsed = up.urlparse(self.path)
            qs = up.parse_qs(parsed.query)
            path = parsed.path
            try:
                if path == "/":
                    self._html(_render_dashboard(state))
                    return
                if path == "/api/health":
                    self._json(_health(state)); return
                if path == "/api/search":
                    q = (qs.get("q") or [""])[0]
                    k = int((qs.get("k") or ["5"])[0])
                    method = (qs.get("method") or ["bm25"])[0]
                    if not state.index:
                        state.index = load_index(state.docs) or _refresh_index(state)
                    hits = search(state.index, q, top_k=k, method=method)
                    self._json([h.__dict__ for h in hits]); return
                if path == "/api/ask":
                    q = (qs.get("q") or [""])[0]
                    k = int((qs.get("k") or ["5"])[0])
                    if not state.index:
                        state.index = load_index(state.docs) or _refresh_index(state)
                    self._json(answer(state.index, q, top_k=k)); return
                self._json({"error": "not found", "path": path}, 404)
            except Exception as e:
                self._json({"error": str(e)}, 500)

    return H


def _render_dashboard(state: _State) -> str:
    h = _health(state)
    metrics_rows = "".join(
        f"<tr><td>{html.escape(n)}</td><td>{html.escape(str(v))}</td><td>{s}</td></tr>"
        for n, v, s in h["metrics"]
    )
    inv = h["inventory"]
    return f"""<!doctype html>
<html lang="ru"><meta charset="utf-8">
<title>kbtool — {html.escape(str(state.docs))}</title>
<style>
 body{{font-family:system-ui,sans-serif;max-width:880px;margin:2em auto;padding:0 1em}}
 .score{{font-size:3em;font-weight:bold}}
 table{{border-collapse:collapse;width:100%;margin:1em 0}}
 th,td{{border:1px solid #ddd;padding:.4em .6em;text-align:left}}
 th{{background:#f4f4f4}}
 input{{padding:.4em;width:60%}}
 button{{padding:.4em 1em}}
 pre{{background:#f8f8f8;padding:1em;overflow:auto;white-space:pre-wrap}}
</style>
<h1>kbtool</h1>
<p><code>{html.escape(str(state.docs))}</code></p>
<div class="score">{h['overall']}/100</div>
<table><tr><th>Метрика</th><th>Значение</th><th>Балл</th></tr>{metrics_rows}</table>
<p>Файлов: {inv['markdown_files']}, байт: {inv['total_bytes']:,}, кластеров: {h['clusters_count']}</p>

<h2>Поиск по корпусу</h2>
<form onsubmit="event.preventDefault();go('search')">
  <input id="q" placeholder="ключевые слова…">
  <button>Найти</button>
  <button type="button" onclick="go('ask')">Ответить</button>
</form>
<pre id="out">—</pre>
<script>
async function go(kind) {{
  const q = document.getElementById('q').value;
  const r = await fetch('/api/' + kind + '?q=' + encodeURIComponent(q));
  const d = await r.json();
  document.getElementById('out').textContent = JSON.stringify(d, null, 2);
}}
</script>

<p style="color:#888;font-size:.85em">API: <code>/api/health</code>, <code>/api/search?q=...</code>, <code>/api/ask?q=...</code></p>
</html>"""


def serve(docs: Path, port: int, exclude: set[str], profile: Profile):
    state = _State()
    state.docs = docs
    state.exclude = exclude
    state.profile = profile
    state.index = load_index(docs)
    if state.index is None:
        print("Индекс не найден — строю…")
        _refresh_index(state)
        print(f"Индекс готов: {len(state.index['docs'])} документов")
    Handler = make_handler(state)
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"kbtool serve → http://127.0.0.1:{port}  (Ctrl+C для выхода)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nserve: остановлен")
