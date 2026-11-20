"""Readback REST (GITHUB_PAT) cho ho so land PR #1431 (#433 P2c-R). Dung: python readback_1431.py <thu_muc_ra>"""
import json, os, pathlib, sys, urllib.request

OUT = pathlib.Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
API = "https://api.github.com/repos/ducthangho/tra-luat"
H, M, D, PR = "e5e118483792981addb30006c900b10fd2e3b72f", "b71f4459896dd04b8e3f8ee2ceb05082a2d87bb4", "9311ccf6554b210cc84c7a88b0cf1195ba6646ea", "1431"
H2 = "b0166982733dff9e4abd8c447a30713a6f951476"


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
    "readback-audit-7025276047.json": "/issues/comments/7025276047",
    "readback-uy-quyen-7022989269.json": "/issues/comments/7022989269",
    "readback-uy-quyen-r1-7015777433.json": "/issues/comments/7015777433",
    "readback-no-pk1-7015527750.json": "/issues/comments/7015527750",
    "readback-do-native-7025233459.json": "/issues/comments/7025233459",
    "hau-due-9311ccf/readback-pr-1432.json": "/pulls/1432",
    "hau-due-9311ccf/readback-pr1432-comments.json": "/issues/1432/comments?per_page=100",
    f"hau-due-9311ccf/readback-checkruns-head-{H2[:7]}.json": f"/commits/{H2}/check-runs?per_page=100",
    f"hau-due-9311ccf/readback-commit-{D[:7]}.json": f"/commits/{D}",
    f"hau-due-9311ccf/readback-runs-merge-{D[:7]}.json": f"/actions/runs?head_sha={D}&per_page=100",
}
for r in ("44639124743", "44625011865"):
    ITEMS[f"readback-run-{r}.json"] = f"/actions/runs/{r}"
    ITEMS[f"readback-jobs-{r}.json"] = f"/actions/runs/{r}/jobs?per_page=100"
ITEMS["hau-due-9311ccf/readback-run-44646501671.json"] = "/actions/runs/44646501671"
ITEMS["hau-due-9311ccf/readback-jobs-44646501671.json"] = "/actions/runs/44646501671/jobs?per_page=100"
for ten, path in ITEMS.items():
    d = get(path)
    p = OUT / ten; p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(ten, "ok")
