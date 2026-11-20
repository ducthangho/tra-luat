"""Readback REST (GITHUB_PAT) cho ho so land PR #1441 (#433 packet N). Dung: python readback_1441.py <thu_muc_ra>"""
import json, os, pathlib, sys, urllib.request

OUT = pathlib.Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
API = "https://api.github.com/repos/ducthangho/tra-luat"
H, H1, M, D, PR = "adda58d59f259475a925d8b61a554f732455978b", "143115a2b43a42f483db8cb0b3aa0a75b68e1d94", "64fa5156794dfb6a2dd9e8f257ee759ab07c9c35", "a31c680c8880786848f832a35554d9e84078b270", "1441"
H2 = "50278595c732adc1906131ddc869e8e241c1bdd9"
HD = "hau-due-a31c680"


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
    f"readback-checkruns-head-{H1[:7]}.json": f"/commits/{H1}/check-runs?per_page=100",
    f"readback-runs-head-{H1[:7]}.json": f"/actions/runs?head_sha={H1}&per_page=100",
    f"readback-commit-{M[:7]}.json": f"/commits/{M}",
    f"readback-runs-merge-{M[:7]}.json": f"/actions/runs?head_sha={M}&per_page=100",
    "readback-issue-433.json": "/issues/433",
    "readback-audit-7032248877.json": "/issues/comments/7032248877",
    "readback-uy-quyen-7030997566.json": "/issues/comments/7030997566",
    "readback-uy-quyen-r1-7028469434.json": "/issues/comments/7028469434",
    "readback-no-p2b-7030544194.json": "/issues/comments/7030544194",
    "readback-no-goc-7008271757.json": "/issues/comments/7008271757",
    "readback-no-pk1-7015527750.json": "/issues/comments/7015527750",
    "readback-do-native-7030452526.json": "/issues/comments/7030452526",
    "readback-do-native-7032232129.json": "/issues/comments/7032232129",
    f"{HD}/readback-pr-1449.json": "/pulls/1449",
    f"{HD}/readback-pr1449-comments.json": "/issues/1449/comments?per_page=100",
    f"{HD}/readback-checkruns-head-{H2[:7]}.json": f"/commits/{H2}/check-runs?per_page=100",
    f"{HD}/readback-commit-{D[:7]}.json": f"/commits/{D}",
    f"{HD}/readback-runs-merge-{D[:7]}.json": f"/actions/runs?head_sha={D}&per_page=100",
    f"{HD}/readback-pr-1447.json": "/pulls/1447",
}
for r in ("44687835603",):
    ITEMS[f"readback-run-{r}.json"] = f"/actions/runs/{r}"
    ITEMS[f"readback-jobs-{r}.json"] = f"/actions/runs/{r}/jobs?per_page=100"
ITEMS[f"{HD}/readback-run-44692028749.json"] = "/actions/runs/44692028749"
ITEMS[f"{HD}/readback-jobs-44692028749.json"] = "/actions/runs/44692028749/jobs?per_page=100"
for ten, path in ITEMS.items():
    d = get(path)
    p = OUT / ten; p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(ten, "ok")
