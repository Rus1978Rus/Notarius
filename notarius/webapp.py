# SPDX-License-Identifier: LicenseRef-Proprietary
# SPDX-FileCopyrightText: 2026 Ruslan Malyavskiy
"""NOTARIUS — local web app (AD-93): a real, usable window on the engine.

Run:
    python3 -m notarius.webapp          # opens http://127.0.0.1:8788 in a browser
    python3 -m notarius web             # same, via the CLI

You paste (or drop) two documents — your REFERENCE and what ARRIVED — press
Check, and the SAME engine behind `notarius check` (analyze.py) reports WHERE
and WHAT changed, plus hidden invisible characters and look-alike domains.
A second tab scans a single document on its own.

Privacy: the server binds to 127.0.0.1 only. Nothing leaves your machine — no
outbound calls, no upload, no telemetry. Only stdlib (the engine itself uses
PyNaCl, but this compare/scan path is pure stdlib).

Boundary (candidly): it shows WHERE the lie is and flags hidden manipulation;
it does not judge intent (TRACE_LOCATES_THE_LIE ≠ TRACE_PROVES_THE_TRUTH).
"""

from __future__ import annotations

import json
import sys
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from notarius.analyze import analyze_documents, scan_document

_MAX_BODY = 8 * 1024 * 1024        # 8 MB guard


# ── the single-page UI (self-contained) ───────────────────────────────
PAGE = r"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>NOTARIUS — check your document</title>
<style>
 :root{--navy:#0E2A3F;--ink:#1B2A36;--mut:#5B6B77;--line:#E2E8EE;--bg:#F5F8FB;
   --card:#fff;--teal:#1C7E8C;--red:#C0392B;--amber:#C77A11;--green:#2E7D57;}
 *{box-sizing:border-box}
 body{margin:0;background:var(--bg);color:var(--ink);
   font:16px/1.5 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;}
 .wrap{max-width:1060px;margin:0 auto;padding:0 20px 46px;}
 .banner{background:linear-gradient(135deg,#0E2A3F,#123B57);color:#EAF2F7;
   padding:24px 30px;border-radius:0 0 18px 18px;box-shadow:0 8px 24px #0e2a3f22;}
 .brand{display:flex;align-items:center;gap:13px;margin-bottom:10px;}
 .mark{width:40px;height:40px;border-radius:9px;border:2px solid #7FD3C9;display:grid;
   place-items:center;font-weight:800;color:#7FD3C9;font-size:20px;}
 h1{margin:0;font-size:23px;font-weight:800;letter-spacing:.5px;}
 .tag{color:#9FC0CF;font-size:12px;font-weight:600;letter-spacing:2px;text-transform:uppercase;}
 .lede{margin:0;font-size:15px;color:#DCE9F0;max-width:820px;}
 .lede b{color:#fff;}.lede i{color:#8FB8C7;}
 .tabs{display:flex;gap:8px;margin:22px 0 14px;}
 .tab{border:1px solid var(--line);background:#fff;color:var(--navy);border-radius:10px;
   padding:10px 16px;font:600 14px inherit;cursor:pointer;}
 .tab.on{background:var(--navy);color:#fff;border-color:var(--navy);}
 .grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;}
 @media(max-width:760px){.grid{grid-template-columns:1fr}}
 .box{background:var(--card);border:1px solid var(--line);border-radius:13px;padding:14px;}
 .box h3{margin:0 0 8px;font-size:12px;letter-spacing:1.3px;text-transform:uppercase;color:var(--mut);}
 textarea{width:100%;min-height:150px;border:1px solid var(--line);border-radius:9px;padding:10px;
   font:13.5px/1.55 Consolas,Menlo,monospace;resize:vertical;color:#24333F;background:#FCFDFE;}
 .file{margin-top:8px;font-size:12.5px;color:var(--mut);}
 .row{display:flex;gap:12px;align-items:center;margin:16px 0 6px;flex-wrap:wrap;}
 .btn{border:0;cursor:pointer;font:700 15px inherit;padding:12px 22px;border-radius:10px;
   background:var(--teal);color:#fff;box-shadow:0 2px 10px #1c7e8c33;}
 .btn:hover{filter:brightness(1.1)} .btn.ghost{background:#fff;color:var(--navy);border:1px solid var(--line);box-shadow:none;}
 .out{margin-top:18px;}
 .verdict{border-radius:13px;padding:15px 18px;margin-bottom:14px;font-weight:700;font-size:16px;
   display:flex;gap:12px;align-items:center;}
 .v-ok{background:#E4F2EA;color:#1f6f4e;border:1px solid #BFE3CE;}
 .v-bad{background:#FBE7E3;color:#A5341F;border:1px solid #F1C7BF;}
 .f{display:grid;grid-template-columns:auto 1fr;gap:12px;background:#fff;border:1px solid var(--line);
   border-radius:11px;padding:12px 14px;margin-bottom:10px;}
 .ln{align-self:start;background:var(--navy);color:#fff;font:700 12px Consolas,monospace;
   border-radius:7px;padding:3px 9px;white-space:nowrap;}
 .ft{font-weight:700;font-size:14.5px;margin-bottom:3px;}
 .pill{font:700 11px Consolas,monospace;padding:2px 8px;border-radius:20px;margin-left:7px;vertical-align:middle;}
 .p-high{background:#F7E1DE;color:var(--red);}.p-medium{background:#F6ECD8;color:var(--amber);}
 .p-low{background:#E1EAF1;color:#1C4E6E;}.p-info{background:#E1EAF1;color:#1C4E6E;}
 .fd{font-size:13.5px;color:#4C5A65;}
 .diff{font:12.5px Consolas,monospace;margin-top:5px;}
 .diff .was{color:#9a5b52;text-decoration:line-through;} .diff .now{color:#1e6f57;font-weight:700;}
 .flag{background:#FBE7E3;color:#A5341F;border:1px solid #F1C7BF;border-radius:11px;padding:11px 14px;
   margin-bottom:10px;font-size:14px;}
 .flag.amber{background:#FBF3E2;color:#7a5410;border-color:#EAD6A8;}
 .empty{color:#9AA9B4;text-align:center;padding:26px;}
 .foot{margin-top:22px;color:#7A8b96;font-size:12px;text-align:center;}
 .foot b{color:#4C5A65;}
</style></head><body>
<div class="banner"><div class="wrap" style="padding:0">
  <div class="brand"><div class="mark">N</div><div>
    <h1>NOTARIUS</h1><div class="tag">check your document · runs on your machine</div></div></div>
  <p class="lede"><b>Paste your reference and what arrived</b> — NOTARIUS shows WHERE and WHAT changed,
    plus hidden characters and look-alike domains. <i>It locates the lie; it does not judge intent.</i></p>
</div></div>
<div class="wrap">
  <div class="tabs">
    <button class="tab on" id="tabCompare" onclick="showTab('compare')">Compare two documents</button>
    <button class="tab" id="tabScan" onclick="showTab('scan')">Scan one document</button>
  </div>

  <div id="paneCompare">
    <div class="grid">
      <div class="box"><h3>Reference (your original)</h3>
        <textarea id="ref" placeholder="Paste your reference text…"></textarea>
        <input class="file" type="file" onchange="loadFile(this,'ref')"></div>
      <div class="box"><h3>Received (what arrived)</h3>
        <textarea id="rcv" placeholder="Paste what you received…"></textarea>
        <input class="file" type="file" onchange="loadFile(this,'rcv')"></div>
    </div>
    <div class="row"><button class="btn" onclick="runCompare()">Check ▶</button>
      <button class="btn ghost" onclick="demo()">Load a demo example</button></div>
  </div>

  <div id="paneScan" style="display:none">
    <div class="box"><h3>Document to scan</h3>
      <textarea id="one" placeholder="Paste a document to scan for hidden characters and look-alike domains…"></textarea>
      <input class="file" type="file" onchange="loadFile(this,'one')"></div>
    <div class="row"><button class="btn" onclick="runScan()">Scan ▶</button></div>
  </div>

  <div class="out" id="out"></div>
  <div class="foot"><b>NOTARIUS</b> · research prototype · runs offline on 127.0.0.1 · nothing leaves your machine ·
    it locates the lie, it does not prove intent</div>
</div>
<script>
 function showTab(t){
   document.getElementById('paneCompare').style.display = t==='compare'?'block':'none';
   document.getElementById('paneScan').style.display    = t==='scan'?'block':'none';
   document.getElementById('tabCompare').classList.toggle('on',t==='compare');
   document.getElementById('tabScan').classList.toggle('on',t==='scan');
   document.getElementById('out').innerHTML='';
 }
 function loadFile(input,id){ const f=input.files[0]; if(!f) return;
   const r=new FileReader(); r.onload=()=>document.getElementById(id).value=r.result; r.readAsText(f); }
 function esc(s){return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
 function marker(s){ // make invisible/zero-width chars visible in the output
   return esc(s).replace(/[​-‏‪-‮⁠﻿­]/g,
     m=>'<span style="background:#8A5A0B;color:#fff;border-radius:3px;padding:0 3px;font-size:10px">U+'+
        m.codePointAt(0).toString(16).toUpperCase().padStart(4,'0')+'</span>'); }
 async function post(path,body){
   const r=await fetch(path,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
   if(!r.ok) throw new Error('server '+r.status); return r.json(); }

 async function runCompare(){
   const ref=document.getElementById('ref').value, rcv=document.getElementById('rcv').value;
   if(!ref && !rcv){ out('<div class="empty">Paste both documents (or load the demo).</div>'); return; }
   try{ render(await post('/api/compare',{reference:ref,received:rcv})); }
   catch(e){ out('<div class="flag">Could not reach the local engine: '+esc(e.message)+'</div>'); }
 }
 async function runScan(){
   const t=document.getElementById('one').value;
   if(!t){ out('<div class="empty">Paste a document to scan.</div>'); return; }
   try{ renderScan(await post('/api/scan',{text:t})); }
   catch(e){ out('<div class="flag">Could not reach the local engine: '+esc(e.message)+'</div>'); }
 }
 function out(h){ document.getElementById('out').innerHTML=h; }

 function flags(res){
   let h='';
   var sig=(res.hidden&&res.hidden.signature)||'';
   if(res.hidden && res.hidden.risk==='ALARM' && !/homoglyph|host|url|userinfo/i.test(sig))
     h+='<div class="flag">⚑ Hidden invisible characters — <b>'+esc(sig)+
        '</b>. '+esc(res.hidden.reason||'')+'</div>';
   (res.url_risks||[]).forEach(u=>{ h+='<div class="flag amber">⚑ Suspicious domain <b>'+
     esc(u.token||'')+'</b> — '+esc(u.issue||'')+' ('+esc(u.risk||'')+')</div>'; });
   return h;
 }
 function render(res){
   if(res.identical){ out('<div class="verdict v-ok">✔ Untouched — identical to your reference.</div>'+flags(res)); return; }
   let h='<div class="verdict v-bad">✘ '+esc(res.summary)+'</div>'+flags(res);
   (res.findings||[]).forEach(f=>{
     h+='<div class="f"><div class="ln">line '+f.line+'</div><div>'+
        '<div class="ft">'+esc(f.category)+'<span class="pill p-'+esc(f.review)+'">'+esc(f.review)+'</span></div>'+
        '<div class="fd">'+esc(f.human)+'</div>'+
        '<div class="diff"><span class="was">'+marker(f.was)+'</span> &nbsp;→&nbsp; <span class="now">'+marker(f.now)+'</span></div>'+
        '</div></div>'; });
   out(h);
 }
 function renderScan(res){
   const ok = (!res.hidden||res.hidden.risk==='OK') && !(res.url_risks||[]).length;
   let h = ok ? '<div class="verdict v-ok">✔ '+esc(res.summary)+'</div>'
              : '<div class="verdict v-bad">⚑ '+esc(res.summary)+'</div>';
   out(h+flags(res)); }

 function demo(){
   document.getElementById('ref').value =
     "Invoice No.77\npayer: Client LLC\namount payable: 1 000 000 USD\nreply-to: paypal.com\n";
   document.getElementById('rcv').value =
     "Invoice No.77\npayer: Client LLC\namount payable: 9 000 000 USD\nreply-to: paypаl.com\n";
   runCompare();
 }
</script></body></html>"""


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):            # keep the console quiet
        pass

    def _send(self, code, body, ctype="application/json"):
        data = body if isinstance(body, bytes) else body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype + "; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _read_json(self):
        n = int(self.headers.get("Content-Length", 0))
        if n <= 0 or n > _MAX_BODY:
            return None
        return json.loads(self.rfile.read(n).decode("utf-8"))

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._send(200, PAGE, "text/html")
        elif self.path == "/health":
            self._send(200, json.dumps({"ok": True}))
        else:
            self._send(404, json.dumps({"error": "not found"}))

    def do_POST(self):
        try:
            payload = self._read_json()
            if payload is None:
                return self._send(400, json.dumps({"error": "bad body"}))
            if self.path == "/api/compare":
                res = analyze_documents(payload.get("reference", ""),
                                        payload.get("received", ""))
                return self._send(200, json.dumps(res, ensure_ascii=False))
            if self.path == "/api/scan":
                res = scan_document(payload.get("text", ""))
                return self._send(200, json.dumps(res, ensure_ascii=False))
            self._send(404, json.dumps({"error": "not found"}))
        except Exception as e:                       # never leak a stack to the page
            self._send(500, json.dumps({"error": type(e).__name__}))


def serve(host: str = "127.0.0.1", port: int = 8788, open_browser: bool = True) -> None:
    httpd = ThreadingHTTPServer((host, port), Handler)
    url = f"http://{host}:{port}"
    print(f"NOTARIUS is running at {url}")
    print("  This is local only — nothing leaves your machine. Press Ctrl+C to stop.")
    if open_browser:
        try:
            webbrowser.open(url)
        except Exception:
            pass
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
        httpd.server_close()


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    port = 8788
    for a in argv:                                   # optional: --port 9000
        if a.isdigit():
            port = int(a)
    serve(port=port)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
