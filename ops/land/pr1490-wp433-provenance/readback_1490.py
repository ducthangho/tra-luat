"""Readback REST (GITHUB_PAT) cho ho so land PR #1490 (#433 packet SECRETS-SET-BUNDLE-KIEU r5). Dung: python readback_1490.py <thu_muc_ra>"""
import json, os, pathlib, sys, urllib.request

OUT = pathlib.Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
API = "https://api.github.com/repos/ducthangho/tra-luat"
H, M, PR, RUN = "26fbacd9d4ba73f8e83359e9af060a76b32cae08", "29c22f7d1f92321978d4d1dff16bd80d9ea744e0", "1490", "44903948558"


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
    "readback-issue-433.json": "/issues/433",
    "readback-audit-7062218542.json": "/issues/comments/7062218542",
    "readback-uy-quyen-ngoai-le-r5-7059899882.json": "/issues/comments/7059899882",
    "readback-so-cap-lease-r10-7059922647.json": "/issues/comments/7059922647",
    "readback-so-xet-lai-r3-7059747094.json": "/issues/comments/7059747094",
    "readback-lease-chieu-7059991008.json": "/issues/comments/7059991008",
    "readback-handoff-7060365474.json": "/issues/comments/7060365474",
    "readback-verdict-chieu-7060873064.json": "/issues/comments/7060873064",
    "readback-run-lease-44903991291.json": "/actions/runs/44903991291",
}
for ten, path in ITEMS.items():
    d = get(path)
    p = OUT / ten; p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(ten, "ok")
