"""Readback REST (GITHUB_PAT) cho ho so land PR #1453 (#433 packet P2BW). Dung: python readback_1441.py <thu_muc_ra>"""
import json, os, pathlib, sys, urllib.request

OUT = pathlib.Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
API = "https://api.github.com/repos/ducthangho/tra-luat"
H, M, D, PR = "4e9306b668cac7797b9cd952b8699c4da603df55", "00ee83998487d289324566f230b67b5923a9a9d9", "66eae513b5e7a2263038ebce7e009e8d2fe52578", "1453"
H2 = "31d68ef2ff399692f20a86b0abf5db1064b21f01"
HD = "hau-due-66eae51"


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
    "readback-audit-7035862456.json": "/issues/comments/7035862456",
    "readback-uy-quyen-7034275292.json": "/issues/comments/7034275292",
    "readback-no-p2b-7030544194.json": "/issues/comments/7030544194",
    "readback-do-native-7035419629.json": "/issues/comments/7035419629",
    f"{HD}/readback-pr-1454.json": "/pulls/1454",
    f"{HD}/readback-pr1454-comments.json": "/issues/1454/comments?per_page=100",
    f"{HD}/readback-checkruns-head-{H2[:7]}.json": f"/commits/{H2}/check-runs?per_page=100",
    f"{HD}/readback-commit-{D[:7]}.json": f"/commits/{D}",
    f"{HD}/readback-runs-merge-{D[:7]}.json": f"/actions/runs?head_sha={D}&per_page=100",
}
for r in ("44711337223",):
    ITEMS[f"readback-run-{r}.json"] = f"/actions/runs/{r}"
    ITEMS[f"readback-jobs-{r}.json"] = f"/actions/runs/{r}/jobs?per_page=100"
ITEMS[f"{HD}/readback-run-44717155521.json"] = "/actions/runs/44717155521"
ITEMS[f"{HD}/readback-jobs-44717155521.json"] = "/actions/runs/44717155521/jobs?per_page=100"
for ten, path in ITEMS.items():
    d = get(path)
    p = OUT / ten; p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(ten, "ok")
