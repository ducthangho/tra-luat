"""Readback run/jobs + trich dong tong ket tu log job cua mot lan chay launcher-windows.yml. Dung: python trich_launcher.py <run> <thu_muc>"""
import hashlib, json, os, pathlib, re, sys, urllib.error, urllib.request
R, O = sys.argv[1], pathlib.Path(sys.argv[2]); O.mkdir(parents=True, exist_ok=True)
API = "https://api.github.com/repos/ducthangho/tra-luat"
H = {"Authorization": "Bearer " + os.environ["GITHUB_PAT"], "Accept": "application/vnd.github+json"}
def get(p):
    with urllib.request.urlopen(urllib.request.Request(API + p, headers=H), timeout=60) as r:
        return json.loads(r.read())
class _K(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None
def log(jid):
    try:
        with urllib.request.build_opener(_K).open(urllib.request.Request(f"{API}/actions/jobs/{jid}/logs", headers=H), timeout=120) as r:
            return r.read()  # tra thang 200, khong qua redirect
    except urllib.error.HTTPError as e:
        loc = e.headers["Location"]
    with urllib.request.urlopen(loc, timeout=120) as r:  # URL ky san, khong gui token
        return r.read()
run = get(f"/actions/runs/{R}"); jobs = get(f"/actions/runs/{R}/jobs?per_page=100")
for t, d in ((f"readback-run-{R}.json", run), (f"readback-jobs-{R}.json", jobs)):
    (O / t).write_text(json.dumps(d, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
out = []
for j in sorted(jobs["jobs"], key=lambda j: j["id"]):
    b = log(j["id"]); s = b.decode("utf-8", "replace")
    out.append(f"## job {j['id']} {j['name']} log_sha256={hashlib.sha256(b).hexdigest()}")
    for ln in s.splitlines():
        m = re.search(r"(\d+/\d+ ca DA CHAY QUA.*|DOT BIEN: .*)$", ln)
        if m:
            out.append(m.group(1).rstrip())
(O / f"launcher-windows-{R}.trich.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print(run["conclusion"], run["head_sha"]); print("\n".join(out))
