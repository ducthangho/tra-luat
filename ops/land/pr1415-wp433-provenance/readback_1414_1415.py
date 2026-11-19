"""Readback REST (GITHUB_PAT) cho ho so land PR #1414 / #1415. Dung: python readback_1414_1415.py <1414|1415> <thu_muc_ra>"""
import json, os, pathlib, sys, urllib.request

PR = sys.argv[1]; OUT = pathlib.Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
API = "https://api.github.com/repos/ducthangho/tra-luat"
CAU_HINH = {
    "1414": dict(H="9804f642ad9c7abcc9e7ae4877c2ff133ef31f00", M="0ca331b4a11835913bb91618d310a34e65599c20", I="387",
                 RUNS=["44489280770", "44489280629"], H1="966ee16"),
    "1415": dict(H="6e49b6807886e1d42b22245dd394a2f19a99bfb5", M="417b59397669e6966da2b546537279d15e2ba0c0", I="433",
                 RUNS=["44489289788"], H1=None),
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
