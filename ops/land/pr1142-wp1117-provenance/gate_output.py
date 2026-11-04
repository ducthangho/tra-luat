import hashlib, json, os, sys, urllib.error, urllib.request
TOK = os.environ["GITHUB_PAT"]
API = "https://api.github.com/repos/ducthangho/tra-luat/"
class _KhongChuyenHuong(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def raw(u):
    """GET REST. Log job tra 302 sang kho blob: theo TAY, KHONG mang token sang host khac (nhu ops/ci_provenance.py:goi_that;
    connector P2 r4469672182 — urlopen mac dinh chuyen ca header Authorization theo redirect)."""
    req = urllib.request.Request(API + u, headers={"Authorization": "Bearer " + TOK, "Accept": "application/vnd.github+json"})
    try:
        return urllib.request.build_opener(_KhongChuyenHuong).open(req, timeout=120).read()
    except urllib.error.HTTPError as e:
        loc = e.headers.get("Location") if e.code in (301, 302, 303, 307, 308) else None
        if not loc:
            raise
    return urllib.request.urlopen(urllib.request.Request(loc), timeout=120).read()   # chuoi tran: khong header token
rid, ra = sys.argv[1], sys.argv[2]
r = json.loads(raw(f"actions/runs/{rid}")); js = json.loads(raw(f"actions/runs/{rid}/jobs?per_page=100"))["jobs"]
out = [f"# Gate output run {rid} attempt {r['run_attempt']} ({r['event']}, {r['path']}, nhanh {r['head_branch']}, head {r['head_sha']}) — log REST tung job, doc 2026-11-04", ""]
for j in sorted(js, key=lambda j: j["name"]):
    if j["conclusion"] == "skipped":
        out.append(f"JOB {j['id']} {j['name']}: skipped"); continue
    b = raw(f"actions/jobs/{j['id']}/logs")
    out.append(f"JOB {j['id']} {j['name']} {j['labels']} conclusion={j['conclusion']} runner_id={j['runner_id']} bytes={len(b)} sha256={hashlib.sha256(b).hexdigest()} ##[error]={b.count(b'##[error]')}")
open(ra, "w", encoding="utf-8").write("\n".join(out) + "\n"); print(len(js), "job")
