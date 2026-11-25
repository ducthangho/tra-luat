"""Readback REST (GITHUB_PAT) cho ho so land PR #1526 (#1236 dot B r12 G1). Dung: python readback_1502.py <thu_muc_ra>"""
import json, os, pathlib, sys, urllib.request

OUT = pathlib.Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
API = "https://api.github.com/repos/ducthangho/tra-luat"
H, M, PR, RUN = "bca55c1cd09c57180d60b05d5ca1813828ae1d10", "d0868dbf7f6324755aa4ed0f3e02d4efa84866f0", "1526", "45635133079"


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
    "readback-run-m9-45627980445.json": "/actions/runs/45627980445",
    "readback-jobs-m9-45627980445.json": "/actions/runs/45627980445/jobs?per_page=100",
    "readback-issue-1236.json": "/issues/1236",
    "readback-audit-e5-7165411240.json": "/issues/comments/7165411240",
    "readback-review-approve-luot5-7164671225.json": "/issues/comments/7164671225",
    "readback-review-luot4-7153650148.json": "/issues/comments/7153650148",
    "readback-mien-p3-7156364013.json": "/issues/comments/7156364013",
    "readback-mien-ghi-ho-7153679183.json": "/issues/comments/7153679183",
    "readback-windows-m3-7161189686.json": "/issues/comments/7161189686",
    "readback-nang-tran-7152104422.json": "/issues/comments/7152104422",
    "readback-kiem-merge-7165287059.json": "/issues/comments/7165287059",
    "readback-connector-7164097497.json": "/issues/comments/7164097497",
}
for ten, path in ITEMS.items():
    d = get(path)
    p = OUT / ten; p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(ten, "ok")
