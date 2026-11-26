"""Readback REST (GITHUB_PAT) cho ho so land PR #1543 (#1236 dot C r12 G1). Dung: python readback_1543.py <thu_muc_ra>"""
import json, os, pathlib, sys, urllib.request

OUT = pathlib.Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
API = "https://api.github.com/repos/ducthangho/tra-luat"
H, M, PR, RUN = "45944c7c3f4c75beaa87f36138b2bba9fb9198a3", "1fac6ced8e5a8c76fdb2699edac779a4251f6149", "1543", "45781748817"


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
    "readback-run-m9-45776250489.json": "/actions/runs/45776250489",
    "readback-jobs-m9-45776250489.json": "/actions/runs/45776250489/jobs?per_page=100",
    "readback-issue-1236.json": "/issues/1236",
    "readback-audit-e5-7186383775.json": "/issues/comments/7186383775",
    "readback-review-approve-luot6-7185457116.json": "/issues/comments/7185457116",
    "readback-windows-m3-7184957862.json": "/issues/comments/7184957862",
    "readback-no-do-3-7185620689.json": "/issues/comments/7185620689",
    "readback-quyet-dinh-ab-7182681531.json": "/issues/comments/7182681531",
    "readback-danh-sach-cho-phep-7180063460.json": "/issues/comments/7180063460",
    "readback-nang-tran-7170968907.json": "/issues/comments/7170968907",
    "readback-connector-7185594874.json": "/issues/comments/7185594874",
}
for ten, path in ITEMS.items():
    d = get(path)
    p = OUT / ten; p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(ten, "ok")
