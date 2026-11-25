"""Tai artifact wd.json + readback run/jobs cua luot ops-do-workflow-definition. Dung: python wd_dl.py <wd_run> <run_do> <thu_muc>"""
import io, json, os, pathlib, sys, urllib.request, zipfile
W, R, O = sys.argv[1], sys.argv[2], pathlib.Path(sys.argv[3]); O.mkdir(parents=True, exist_ok=True)
API = "https://api.github.com/repos/ducthangho/tra-luat"
def get(u, raw=False):
    rq = urllib.request.Request(u if u.startswith("http") else API + u, headers={"Authorization": "Bearer " + os.environ["GITHUB_PAT"], "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(rq, timeout=60) as r:
        b = r.read()
    return b if raw else json.loads(b)
for ten, p in ((f"readback-run-{W}.json", f"/actions/runs/{W}"), (f"readback-jobs-{W}.json", f"/actions/runs/{W}/jobs?per_page=100")):
    (O / ten).write_text(json.dumps(get(p), ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
arts = [a for a in get(f"/actions/runs/{W}/artifacts")["artifacts"] if a["name"] == f"workflow-definition-{R}"]
assert len(arts) == 1, arts
class _K(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None
try:
    urllib.request.build_opener(_K).open(urllib.request.Request(arts[0]["archive_download_url"], headers={"Authorization": "Bearer " + os.environ["GITHUB_PAT"]}), timeout=60)
    raise SystemExit("khong redirect")
except urllib.error.HTTPError as e:
    loc = e.headers["Location"]
with urllib.request.urlopen(loc, timeout=60) as r:  # URL ky san, KHONG gui token toi kho blob
    z = zipfile.ZipFile(io.BytesIO(r.read()))
assert z.namelist() == ["wd.json"], z.namelist()
(O / f"wd-{R}.json").write_bytes(z.read("wd.json"))
print(json.loads(z.read("wd.json"))["trang_thai"])
