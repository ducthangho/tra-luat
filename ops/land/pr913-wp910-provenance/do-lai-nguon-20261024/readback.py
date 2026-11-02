"""Readback GET qua proxy phien bang GITHUB_PAT; ghi JSON nguyen trang (tat ca trang) vao thu muc dich."""
import json, os, sys, urllib.request
OUT = sys.argv[1]
API = "https://api.github.com/repos/ducthangho/tra-luat/"
H = {"Authorization": "Bearer " + os.environ["GITHUB_PAT"], "Accept": "application/vnd.github+json"}
def get(path):
    req = urllib.request.Request(API + path, headers=H)
    with urllib.request.urlopen(req) as r:
        return json.load(r)
def get_all(path, key=None):
    out, page = [], 1
    while True:
        sep = "&" if "?" in path else "?"
        d = get(f"{path}{sep}per_page=100&page={page}")
        items = d[key] if key else d
        out.extend(items)
        if len(items) < 100:
            return {key: out, "total_count": d.get("total_count")} if key else out
        page += 1
def ghi(ten, obj):
    with open(os.path.join(OUT, ten), "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("ghi", ten)
for item in sys.argv[2:]:
    kind, _, arg = item.partition(":")
    if kind == "pr": ghi(f"readback-pr-{arg}.json", get(f"pulls/{arg}"))
    elif kind == "events": ghi(f"readback-events-{arg}.json", get_all(f"issues/{arg}/events"))
    elif kind == "reviews": ghi(f"readback-reviews-{arg}.json", get_all(f"pulls/{arg}/reviews"))
    elif kind == "review-comments": ghi(f"readback-review-comments-{arg}.json", get_all(f"pulls/{arg}/comments"))
    elif kind == "comments": ghi(f"readback-comments-{arg}.json", get_all(f"issues/{arg}/comments"))
    elif kind == "issue": ghi(f"readback-issue-{arg}.json", get(f"issues/{arg}"))
    elif kind == "comment": ghi(f"readback-comment-{arg}.json", get(f"issues/comments/{arg}"))
    elif kind == "run": ghi(f"readback-run-{arg}.json", get(f"actions/runs/{arg}"))
    elif kind == "jobs": ghi(f"readback-jobs-{arg}.json", get_all(f"actions/runs/{arg}/jobs?filter=all", "jobs"))
    elif kind == "checkruns": ghi(f"readback-check-runs-{arg[:7]}-all.json", get_all(f"commits/{arg}/check-runs?filter=all", "check_runs"))
    else: raise SystemExit("khong biet " + item)
