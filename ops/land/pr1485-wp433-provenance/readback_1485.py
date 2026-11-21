"""Readback REST (GITHUB_PAT) cho ho so land PR #1485 (#433 packet BUNDLED-TACH-MANH). Dung: python readback_1485.py <thu_muc_ra>"""
import json, os, pathlib, sys, urllib.request

OUT = pathlib.Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
API = "https://api.github.com/repos/ducthangho/tra-luat"
H, M, PR, RUN = "5293a855564e8966092d49542be3bb29d5ed3787", "96cd0120d2aa0ba555641fdde90c9d4fbd8b9c89", "1485", "44875152707"


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
    "readback-audit-7058495018.json": "/issues/comments/7058495018",
    "readback-uy-quyen-r9-7053681301.json": "/issues/comments/7053681301",
    "readback-so-xet-lai-7058076373.json": "/issues/comments/7058076373",
    "readback-so-cap-lease-g5-7056652494.json": "/issues/comments/7056652494",
    "readback-handoff-luot3-7057612559.json": "/issues/comments/7057612559",
}
for ten, path in ITEMS.items():
    d = get(path)
    p = OUT / ten; p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(ten, "ok")
