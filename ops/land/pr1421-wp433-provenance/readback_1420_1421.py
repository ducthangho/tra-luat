"""Readback REST (GITHUB_PAT) cho ho so land PR #1420 / #1421. Dung: python readback_1420_1421.py <1420|1421> <thu_muc_ra>"""
import json, os, pathlib, sys, urllib.request

PR = sys.argv[1]; OUT = pathlib.Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
API = "https://api.github.com/repos/ducthangho/tra-luat"
CAU_HINH = {
    "1420": dict(H="2de12d38cda7d4bfe1f6f8c970e7ccd77e44a4de", M="d89e0002f863a8fc8f374787a4dbd81e04f66c4d", I="1342",
                 RUNS=["44526317417", "44526317637"], H1=None),
    "1421": dict(H="bec60a9cf3757a9beedab45241a50d6aa2169fe7", M="c6487ff884c61085c939a75a37c657006ee690f2", I="433",
                 RUNS=["44533503543"], H1=None),
}
C = CAU_HINH[PR]; H, M = C["H"], C["M"]


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
    f"readback-issue-{C['I']}.json": f"/issues/{C['I']}",
}
for r in C["RUNS"]:
    ITEMS[f"readback-run-{r}.json"] = f"/actions/runs/{r}"
    ITEMS[f"readback-jobs-{r}.json"] = f"/actions/runs/{r}/jobs?per_page=100"
for ten, path in ITEMS.items():
    d = get(path)
    (OUT / ten).write_text(json.dumps(d, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(ten, "ok")
