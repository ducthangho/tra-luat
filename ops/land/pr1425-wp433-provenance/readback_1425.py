"""Readback REST (GITHUB_PAT) cho ho so land PR #1425 (#433 P2c-C1). Dung: python readback_1425.py <thu_muc_ra>"""
import json, os, pathlib, sys, urllib.request

OUT = pathlib.Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
API = "https://api.github.com/repos/ducthangho/tra-luat"
H, M, PR = "724a9e55727c82cc0c5ad7d3c4479cfb69be791b", "20eac111b1f95567bf2ec87260888f77222eea3b", "1425"


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
    "readback-issue-433.json": "/issues/433",
    "readback-audit-7015578352.json": "/issues/comments/7015578352",
    "readback-uy-quyen-7009529083.json": "/issues/comments/7009529083",
    "readback-no-pk1-7015527750.json": "/issues/comments/7015527750",
    "readback-do-native-7015486966.json": "/issues/comments/7015486966",
    "readback-lease-dang-7011275136.json": "/issues/comments/7011275136",
}
for r in ("44569159263", "44549085747", "44549085783"):
    ITEMS[f"readback-run-{r}.json"] = f"/actions/runs/{r}"
    ITEMS[f"readback-jobs-{r}.json"] = f"/actions/runs/{r}/jobs?per_page=100"
for ten, path in ITEMS.items():
    d = get(path)
    (OUT / ten).write_text(json.dumps(d, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(ten, "ok")
