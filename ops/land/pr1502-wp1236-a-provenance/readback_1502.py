"""Readback REST (GITHUB_PAT) cho ho so land PR #1502 (#1236 dot A r12 G2). Dung: python readback_1502.py <thu_muc_ra>"""
import json, os, pathlib, sys, urllib.request

OUT = pathlib.Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
API = "https://api.github.com/repos/ducthangho/tra-luat"
H, M, PR, RUN = "835655b6b5d8ad2add49f04ded92d3fd3f42515e", "9d61d4efe6b59c20c12ba87420efd7dfd6e224bc", "1502", "45376074845"


def get(path):
    rq = urllib.request.Request(API + path, headers={"Authorization": "Bearer " + os.environ["GITHUB_PAT"], "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(rq, timeout=60) as r:
        return json.loads(r.read())


ITEMS = {
    f"readback-pr-{PR}.json": f"/pulls/{PR}",
    f"readback-pr{PR}-comments.json": f"/issues/{PR}/comments?per_page=100",
    f"readback-pr{PR}-reviews.json": f"/pulls/{PR}/reviews?per_page=100",
    f"readback-pr{PR}-review-comments.json": f"/pulls/{PR}/comments?per_page=100",
    f"readback-pr{PR}-commits.json": f"/pulls/{PR}/commits?per_page=100",
    f"readback-checkruns-head-{H[:7]}.json": f"/commits/{H}/check-runs?per_page=100",
    f"readback-runs-head-{H[:7]}.json": f"/actions/runs?head_sha={H}&per_page=100",
    f"readback-commit-{M[:7]}.json": f"/commits/{M}",
    f"readback-runs-merge-{M[:7]}.json": f"/actions/runs?head_sha={M}&per_page=100",
    f"readback-run-{RUN}.json": f"/actions/runs/{RUN}",
    f"readback-jobs-{RUN}.json": f"/actions/runs/{RUN}/jobs?per_page=100",
    "readback-issue-1236.json": "/issues/1236",
    "readback-tien-do-7123865566.json": "/issues/comments/7123865566",
    "readback-review-approve-7125514979.json": "/issues/comments/7125514979",
    "readback-windows-mien-7127447632.json": "/issues/comments/7127447632",
    "readback-audit-e5-7107992503.json": "/issues/comments/7107992503",
    "readback-cap-lease-g2-7082184146.json": "/issues/comments/7082184146",
    "readback-ghi-ho-1459-7129098397.json": "/issues/comments/7129098397",
    "readback-pr-1459.json": "/pulls/1459",
    "readback-pr-1465.json": "/pulls/1465",
}
for ten, path in ITEMS.items():
    d = get(path)
    p = OUT / ten; p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(ten, "ok")
