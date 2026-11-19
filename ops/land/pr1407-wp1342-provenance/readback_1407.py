"""Readback REST (GITHUB_PAT) cho ho so land PR #1407. Dung: python readback_1407.py <thu_muc_ra>"""
import json, os, pathlib, sys, urllib.request

OUT = pathlib.Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
API = "https://api.github.com/repos/ducthangho/tra-luat"
H = "46d39071989fd77582ef8d1d61a7ab7de90a12ba"; M = "a2c7d759866502e7da318e4f83e17d5f77491eb5"


def get(path):
    rq = urllib.request.Request(API + path, headers={"Authorization": "Bearer " + os.environ["GITHUB_PAT"], "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(rq, timeout=60) as r:
        return json.loads(r.read())


ITEMS = {
    "readback-pr-1407.json": "/pulls/1407",
    "readback-pr1407-comments.json": "/issues/1407/comments?per_page=100",
    "readback-pr1407-reviews.json": "/pulls/1407/reviews?per_page=100",
    "readback-pr1407-review-comments.json": "/pulls/1407/comments?per_page=100",
    "readback-pr1407-commits.json": "/pulls/1407/commits?per_page=100",
    "readback-checkruns-head-46d3907.json": f"/commits/{H}/check-runs?per_page=100",
    "readback-runs-head-46d3907.json": f"/actions/runs?head_sha={H}&per_page=100",
    "readback-checkruns-head-728ecca.json": "/commits/728eccab3886e5fbba1eeb76c6b770068bae9226/check-runs?per_page=100",
    "readback-commit-a2c7d75.json": f"/commits/{M}",
    "readback-runs-merge-a2c7d75.json": f"/actions/runs?head_sha={M}&per_page=100",
    "readback-issue-1342.json": "/issues/1342",
}
for ten, path in ITEMS.items():
    d = get(path)
    (OUT / ten).write_text(json.dumps(d, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(ten, "ok")
