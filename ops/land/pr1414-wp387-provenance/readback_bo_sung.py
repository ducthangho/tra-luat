"""Readback REST bo sung (GITHUB_PAT): mot comment theo id va/hoac mot PR. Dung: python readback_bo_sung.py <thu_muc> <ten_tep>=<duong REST>..."""
import json, os, pathlib, sys, urllib.request
O = pathlib.Path(sys.argv[1]); O.mkdir(parents=True, exist_ok=True)
for cap in sys.argv[2:]:
    ten, path = cap.split("=", 1)
    rq = urllib.request.Request("https://api.github.com/repos/ducthangho/tra-luat" + path, headers={"Authorization": "Bearer " + os.environ["GITHUB_PAT"], "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(rq, timeout=60) as r:
        d = json.loads(r.read())
    (O / ten).write_text(json.dumps(d, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(ten, "ok")
