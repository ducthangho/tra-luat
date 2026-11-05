"""Phan chung connector P2 r4469672182: raw() cua danh_gia_gate.py/gate_output.py khong duoc mang Authorization sang host dich
cua redirect. Dung 2 server cuc bo: A (127.0.0.1) tra 302 -> B (localhost, host KHAC). Ghi header B nhan duoc.
Cach goi: python3 phan_chung_redirect.py <tep.py> ; in DAT neu B KHONG thay Authorization va than tra ve dung."""
import http.server, importlib.util, os, sys, threading
nhan = {}
class B(http.server.BaseHTTPRequestHandler):
    def do_GET(s):
        nhan["auth"] = s.headers.get("Authorization"); s.send_response(200); s.end_headers(); s.wfile.write(b"LOG-OK")
    def log_message(s, *a): pass
sb = http.server.HTTPServer(("127.0.0.1", 0), B); pb = sb.server_port
class A(http.server.BaseHTTPRequestHandler):
    def do_GET(s):
        s.send_response(302); s.send_header("Location", f"http://localhost:{pb}/blob"); s.end_headers()
    def log_message(s, *a): pass
sa = http.server.HTTPServer(("127.0.0.1", 0), A)
for x in (sa, sb): threading.Thread(target=x.serve_forever, daemon=True).start()
os.environ["GITHUB_PAT"] = "TOKEN-GIA-PHAN-CHUNG"
for k in ("HTTP_PROXY", "http_proxy", "HTTPS_PROXY", "https_proxy"): os.environ.pop(k, None)
os.environ["NO_PROXY"] = "*"
import types
nguon = open(sys.argv[1], encoding="utf-8").read()
nguon = nguon.split("\nrid, ra =")[0].split("\nif __name__")[0]   # chi phan dinh nghia (gate_output.py chay lenh o muc module)
m = types.ModuleType("m"); exec(compile(nguon, sys.argv[1], "exec"), m.__dict__)
m.API = f"http://127.0.0.1:{sa.server_port}/"
than = m.raw("actions/jobs/1/logs")
ok = than == b"LOG-OK" and nhan.get("auth") is None
print(("DAT" if ok else "DO"), "than=", than, "B nhan Authorization=", nhan.get("auth"))
sys.exit(0 if ok else 1)
