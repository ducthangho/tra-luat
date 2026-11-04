import hashlib, json, os, sys, urllib.request
API = "https://api.github.com/repos/ducthangho/tra-luat/"
def raw(u):
    return urllib.request.urlopen(urllib.request.Request(API + u, headers={"Authorization": "Bearer " + os.environ["GITHUB_PAT"], "Accept": "application/vnd.github+json"}), timeout=120).read()
rid, ra = sys.argv[1], sys.argv[2]
r = json.loads(raw(f"actions/runs/{rid}")); js = json.loads(raw(f"actions/runs/{rid}/jobs?per_page=100"))["jobs"]
out = [f"# Gate output run {rid} attempt {r['run_attempt']} ({r['event']}, {r['path']}, nhanh {r['head_branch']}, head {r['head_sha']}) — log REST tung job, doc 2026-11-04", ""]
for j in sorted(js, key=lambda j: j["name"]):
    if j["conclusion"] == "skipped":
        out.append(f"JOB {j['id']} {j['name']}: skipped"); continue
    b = raw(f"actions/jobs/{j['id']}/logs")
    out.append(f"JOB {j['id']} {j['name']} {j['labels']} conclusion={j['conclusion']} runner_id={j['runner_id']} bytes={len(b)} sha256={hashlib.sha256(b).hexdigest()} ##[error]={b.count(b'##[error]')}")
open(ra, "w", encoding="utf-8").write("\n".join(out) + "\n"); print(len(js), "job")
