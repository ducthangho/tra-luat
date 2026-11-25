#!/usr/bin/env python3
"""Do lai moc Checkout + Gate output cho PR #1510 tu log GOC (logs/*.log.gz, tai bang gh api .../jobs/<id>/logs).
Chay: python ops/land/pr1510-r1509-acl-codex-provenance/do_lai.py  (khong mang, chi doc tep canh no)."""
import glob, gzip, hashlib, json, os, re, sys
D = os.path.dirname(os.path.abspath(__file__))
M = "a03a28ef076503c7fe93c208a4998c32590a977f"
khai = dict(re.findall(r"== job (\d+) sha256=([0-9a-f]{64})", open(os.path.join(D, "log-markers-a03a28e.txt"), encoding="utf-8").read()))
jobs = {}
for r in ("45418608259", "45418608352"):
    for j in json.load(open(os.path.join(D, f"readback-jobs-{r}.json"), encoding="utf-8"))["jobs"]:
        jobs[str(j["id"])] = (r, j["run_attempt"], j["name"], j["labels"], j["conclusion"], j["runner_id"])
loi = 0
tong = {"job": 0, "sha_khop": 0, "checkout_M": 0, "exit_khac_0": 0, "marker_duong": 0}
for f in sorted(glob.glob(os.path.join(D, "logs", "*.log.gz"))):
    jid = os.path.basename(f)[:-7]
    b = gzip.open(f).read()
    t = re.sub(r"(?m)^\S+Z ", "", b.decode("utf-8", "replace"))
    sha_ok = hashlib.sha256(b).hexdigest() == khai.get(jid)
    # checkout: lenh `git log -1 --format=%H` cua actions/checkout in ra dung M (OID commit co dinh tree + parents)
    co = bool(re.search(r"git(?:\.exe\")? log -1 --format=%H\s*\n" + M, t))
    ex = re.findall(r"Process completed with exit code ([1-9]\d*)", t)
    mk = len(re.findall(r"DOT BIEN: (\d+)/\1 |\"ok\": true|TỔNG: ĐẠT|\"returncode\": 0", t))
    r, att, name, lab, concl, rid = jobs[jid]
    print(f"{jid} run={r} attempt={att} labels={lab} runner_id={rid} concl={concl} sha256_khop={sha_ok} checkout_M={co} exit_khac_0={len(ex)} marker_duong={mk} | {name}")
    tong["job"] += 1; tong["sha_khop"] += sha_ok; tong["checkout_M"] += co; tong["exit_khac_0"] += len(ex); tong["marker_duong"] += mk
    loi += (not sha_ok) or (not co) or bool(ex) or concl != "success" or att != 1 or rid == 0
print("TONG", json.dumps(tong))
print("KET_LUAN", "DAT" if loi == 0 and tong["job"] == len(jobs) == 41 else f"DO ({loi} job loi)")
sys.exit(0 if loi == 0 else 1)
