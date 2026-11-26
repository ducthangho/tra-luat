"""Thu readback REST (GITHUB_PAT) cho `packet_loop.py kiem-merge`. Dùng: python3 thu_kiem_merge.py <ra> <head> <pr> <comment_chu_kho_id> [dot_bien_du_run_id]"""
import json, os, pathlib, sys, urllib.request

OUT = pathlib.Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
H, PR, CK = sys.argv[2], int(sys.argv[3]), sys.argv[4]
DB = sys.argv[5] if len(sys.argv) > 5 else None
REPO = "ducthangho/tra-luat"
API = f"https://api.github.com/repos/{REPO}"


def get(path):
    rq = urllib.request.Request(API + path, headers={"Authorization": "Bearer " + os.environ["GITHUB_PAT"], "Accept": "application/vnd.github+json",
                                                    "X-GitHub-Api-Version": "2022-11-28"})
    with urllib.request.urlopen(rq, timeout=60) as r:
        return json.loads(r.read())


def luu(ten, d):
    (OUT / ten).write_text(json.dumps(d, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(ten, "ok")


def tat_ca(path, khoa=None):
    """Đủ trang; trả (list, total_count nếu có)."""
    ds, tong, p = [], None, 1
    while True:
        d = get(f"{path}{'&' if '?' in path else '?'}per_page=100&page={p}")
        muc = d[khoa] if khoa else d
        tong = d.get("total_count") if khoa else None
        ds += muc
        if len(muc) < 100:
            return ds, tong
        p += 1


runs, t = tat_ca(f"/actions/runs?head_sha={H}", "workflow_runs")
luu("workflow-runs.json", {"total_count": t, "workflow_runs": runs})
ci = [r for r in runs if r["path"] == ".github/workflows/ci.yml"]
for r in ci:
    js, tj = tat_ca(f"/actions/runs/{r['id']}/jobs?filter=all", "jobs")
    luu(f"workflow-jobs-{r['id']}.json", {"total_count": tj, "jobs": js})
cr, tc = tat_ca(f"/commits/{H}/check-runs?filter=all", "check_runs")
luu("check-runs.json", {"total_count": tc, "check_runs": cr})
con = {"repo": REPO, "pr": PR, "head_sha": H}
for k, path in (("issue_comments", f"/issues/{PR}/comments"), ("reviews", f"/pulls/{PR}/reviews"), ("review_comments", f"/pulls/{PR}/comments")):
    ds, _ = tat_ca(path)
    con[k] = {"total_count": len(ds), "items": ds}
luu("connector.json", con)
luu(f"chu-kho-comment-{CK}.json", get(f"/issues/comments/{CK}"))
if DB:
    dr = get(f"/actions/runs/{DB}")
    luu("dot-bien-du-runs.json", {"total_count": 1, "workflow_runs": [dr]})
    js, tj = tat_ca(f"/actions/runs/{DB}/jobs?filter=latest", "jobs")
    luu(f"dot-bien-du-jobs-{DB}.json", {"total_count": tj, "jobs": js})
