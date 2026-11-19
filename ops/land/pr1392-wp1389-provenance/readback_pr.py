"""Readback REST (GITHUB_PAT) cho mot ho so land. Dung: python readback_pr.py <thu_muc_ra> <pr> <head_sha> <merge_sha> <issue> [run_id ...]"""
import json, os, pathlib, sys, time, urllib.error, urllib.request

OUT = pathlib.Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
PR, H, M, I, RUNS = sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6:]
API = "https://api.github.com/repos/ducthangho/tra-luat"


def get(path):
    for lan in range(5):   # proxy co the tra 503 "Egress is over the account limit": doi roi thu lai, khong doi duong
        try:
            rq = urllib.request.Request(API + path, headers={"Authorization": "Bearer " + os.environ["GITHUB_PAT"], "Accept": "application/vnd.github+json"})
            with urllib.request.urlopen(rq, timeout=60) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code not in (429, 503) or lan == 4:
                raise
            time.sleep(20)


ITEMS = {
    f"readback-pr-{PR}.json": f"/pulls/{PR}",
    f"readback-pr{PR}-comments.json": f"/issues/{PR}/comments?per_page=100",
    f"readback-pr{PR}-reviews.json": f"/pulls/{PR}/reviews?per_page=100",
    f"readback-pr{PR}-review-comments.json": f"/pulls/{PR}/comments?per_page=100",
    f"readback-pr{PR}-commits.json": f"/pulls/{PR}/commits?per_page=100",
    f"readback-pr{PR}-files.json": f"/pulls/{PR}/files?per_page=100",
    f"readback-checkruns-head-{H[:7]}.json": f"/commits/{H}/check-runs?per_page=100",
    f"readback-runs-head-{H[:7]}.json": f"/actions/runs?head_sha={H}&per_page=100",
    f"readback-commit-{M[:7]}.json": f"/commits/{M}",
    f"readback-runs-merge-{M[:7]}.json": f"/actions/runs?head_sha={M}&per_page=100",
    f"readback-issue-{I}.json": f"/issues/{I}",
}
for r in RUNS:
    ITEMS[f"readback-run-{r}.json"] = f"/actions/runs/{r}"
    ITEMS[f"readback-jobs-{r}.json"] = f"/actions/runs/{r}/jobs?per_page=100"
for ten, path in ITEMS.items():
    (OUT / ten).write_text(json.dumps(get(path), ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(ten, "ok")
