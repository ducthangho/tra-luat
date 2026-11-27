"""Readback REST (GITHUB_PAT) cho ho so land PR #1565 (#1539 bo-sinh-bat-bien r1 g1). Dung: python3 readback_1565.py <thu_muc_ra>"""
import json, os, pathlib, sys, urllib.request

OUT = pathlib.Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
API = "https://api.github.com/repos/ducthangho/tra-luat"
H, M, PR, RUN, M9 = ("97ec9686184fdf55dc1736007e6fdcb186122465", "e209579adfca823926cdfad87579f360b7bacb26", "1565", "45914294573",
                    "45881791951")


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
    f"readback-run-m9-{M9}.json": f"/actions/runs/{M9}",
    f"readback-jobs-m9-{M9}.json": f"/actions/runs/{M9}/jobs?per_page=100",
    "readback-issue-1539.json": "/issues/1539",
    "readback-mo-packet-7174327296.json": "/issues/comments/7174327296",
    "readback-va-luot-cuoi-7191685771.json": "/issues/comments/7191685771",
    "readback-review-luot4-7196524386.json": "/issues/comments/7196524386",
    "readback-mien-p3-7197313309.json": "/issues/comments/7197313309",
    "readback-nang-tran-7197354187.json": "/issues/comments/7197354187",
    "readback-review-approve-luot5-7197552662.json": "/issues/comments/7197552662",
    "readback-doi-chieu-adr0060-7197622402.json": "/issues/comments/7197622402",
    "readback-ghi-ho-phien-khac-7198120977.json": "/issues/comments/7198120977",
    "readback-giu-luot5-7198178108.json": "/issues/comments/7198178108",
    "readback-luat9-pr-m9-7201303279.json": "/issues/comments/7201303279",
    "readback-connector-7201350451.json": "/issues/comments/7201350451",
    "readback-audit-uy-quyen-7206056707.json": "/issues/comments/7206056707",
    "readback-so-audit-7206087221.json": "/issues/comments/7206087221",
    "readback-duyet-merge-7206098855.json": "/issues/comments/7206098855",
    "readback-bien-nhan-merge-7206110372.json": "/issues/comments/7206110372",
}
for ten, path in ITEMS.items():
    d = get(path)
    p = OUT / ten; p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(ten, "ok")
