"""So tap BO QUA va KHONG DO DUOC cua lane launcher-windows.yml giua hai run (base vs merge), theo tung job (windows-latest, ubuntu-latest).
Dung: python so_lane_launcher.py <run_base> <run_merge> <tep_ra>. Log job tai qua REST (redirect theo tay, khong gui token sang kho blob)."""
import hashlib, json, os, re, sys, urllib.error, urllib.request
RB, RM, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
API = "https://api.github.com/repos/ducthangho/tra-luat"
H = {"Authorization": "Bearer " + os.environ["GITHUB_PAT"], "Accept": "application/vnd.github+json"}
class _K(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None
def get(p):
    return json.loads(urllib.request.urlopen(urllib.request.Request(API + p, headers=H), timeout=60).read())
def log(j):
    try:
        return urllib.request.build_opener(_K).open(urllib.request.Request(f"{API}/actions/jobs/{j}/logs", headers=H), timeout=120).read()
    except urllib.error.HTTPError as e:
        return urllib.request.urlopen(e.headers["Location"], timeout=120).read()
TS = re.compile(r"^\d{4}-\d\d-\d\dT[\d:.]+Z ")
def tap(run):
    kq = {}
    run_j = get(f"/actions/runs/{run}")
    for j in get(f"/actions/runs/{run}/jobs?per_page=100")["jobs"]:
        b = log(j["id"]); s = b.decode("utf-8", "replace")
        ls = [TS.sub("", x) for x in s.splitlines()]
        bo = sorted({m.group(1).rstrip(":") for x in ls for m in [re.match(r"^\s*BO QUA (\S+)", x)] if m})
        kdd = sorted({m.group(1) for x in ls for m in [re.match(r"^\s*(\S+)\s+KHONG DO DUOC", x)] if m})
        tong = [x.strip() for x in ls if re.search(r"ca DA CHAY QUA|^DOT BIEN: ", x.strip())]
        kq[j["name"]] = dict(job=j["id"], runner=j["labels"], log_sha256=hashlib.sha256(b).hexdigest(), bo_qua=bo, khong_do_duoc=kdd, tong=tong)
    return run_j["head_sha"], kq
hb, b = tap(RB); hm, m = tap(RM)
out = [f"# so lane launcher-windows.yml: base run {RB} (head {hb}) vs merge run {RM} (head {hm})"]
for ten in sorted(m):
    x, y = b.get(ten), m[ten]
    out.append(f"\n== {ten}")
    for nhan, d in (("base", x), ("merge", y)):
        out.append(f"{nhan}: job {d['job']} log_sha256 {d['log_sha256']} tong {d['tong']} | bo_qua {len(d['bo_qua'])} | khong_do_duoc {len(d['khong_do_duoc'])}")
    out.append(f"bo_qua base - merge ({len(set(x['bo_qua']) - set(y['bo_qua']))}): {sorted(set(x['bo_qua']) - set(y['bo_qua']))}")
    out.append(f"bo_qua merge - base ({len(set(y['bo_qua']) - set(x['bo_qua']))}): {sorted(set(y['bo_qua']) - set(x['bo_qua']))}")
    out.append(f"khong_do_duoc merge - base: {sorted(set(y['khong_do_duoc']) - set(x['khong_do_duoc']))}")
    out.append(f"khong_do_duoc base - merge: {sorted(set(x['khong_do_duoc']) - set(y['khong_do_duoc']))}")
    out.append(f"khong_do_duoc merge: {y['khong_do_duoc']}")
open(OUT, "w", encoding="utf-8").write("\n".join(out) + "\n")
print("\n".join(out))
