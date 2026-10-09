"""Doi chieu than `run:` tung buoc cua workflow tai MOT commit voi than buoc in trong log job (dong ESC[36;1m).

Dung: python3 doi_chieu_buoc.py <commit> <thu_muc_log>
  <thu_muc_log> chua job-<id>.log tai qua GET /actions/jobs/<id>/logs (log KHONG commit; bam o SHA256SUMS-log-va-artifact.txt).
Chay trong mot clone co commit ay. Phuong phap = ops/land/pr696-wp668-provenance/doi_chieu_buoc.py (chep), chi doi bang JOBS va WF cho PR #689.
Gioi han: chi chung minh than buoc da chay khop dinh nghia theo thu tu; KHONG chung minh bytes ngoai than buoc.
"""
import json
import os
import re
import subprocess
import sys

import yaml

commit, logdir = sys.argv[1], sys.argv[2]
JOBS = {  # job id -> (workflow, job key) cua run 36792473622 (pull_request, 0614f7f) va 36798575727 (push, 20ec8d5), ci.yml
    "110148322748": ('ci', 'chuan-bi'),
    "110148349586": ('ci', 'gate-ops'),
    "110148349603": ('ci', 'gate-packet-loop'),
    "110148349622": ('ci', 'gate'),
    "110148349624": ('ci', 'gate-registry'),
    "110148349648": ('ci', 'gate-cong-cu'),
    "110148349659": ('ci', 'gate-cong-cu'),
    "110148349677": ('ci', 'gate-cong-cu'),
    "110148349691": ('ci', 'gate-cong-cu'),
    "110148349708": ('ci', 'gate-cong-cu'),
    "110148349710": ('ci', 'gate-cong-cu'),
    "110148349756": ('ci', 'gate-cong-cu'),
    "110148349815": ('ci', 'gate-cong-cu'),
    "110153193715": ('ci', 'gate-cong-cu-gop'),
    "110172104369": ('ci', 'chuan-bi'),
    "110172127258": ('ci', 'gate-packet-loop'),
    "110172127260": ('ci', 'gate-ops'),
    "110172127274": ('ci', 'gate-registry'),
    "110172127294": ('ci', 'gate-cong-cu'),
    "110172127299": ('ci', 'gate'),
    "110172127300": ('ci', 'gate-cong-cu'),
    "110172127302": ('ci', 'gate-cong-cu'),
    "110172127307": ('ci', 'gate-cong-cu'),
    "110172127324": ('ci', 'gate-cong-cu'),
    "110172127341": ('ci', 'gate-cong-cu'),
    "110172127376": ('ci', 'gate-cong-cu'),
    "110172127397": ('ci', 'gate-cong-cu'),
    "110176880597": ('ci', 'gate-cong-cu-gop'),
}
WF = {"ci": ".github/workflows/ci.yml"}
DEFS = {k: yaml.safe_load(subprocess.run(["git", "show", f"{commit}:{p}"], capture_output=True,
                                         text=True, check=True).stdout) for k, p in WF.items()}
TS = re.compile(r"^\S+Z ")
ESC = "\x1b[36;1m"
out = {}
for jid, (w, name) in JOBS.items():
    f = os.path.join(logdir, f"job-{jid}.log")
    if not os.path.exists(f):
        out[jid] = dict(job=name, loi="thieu log")
        continue
    runs = [s["run"].rstrip("\n").split("\n") for s in DEFS[w]["jobs"][name]["steps"] if "run" in s]
    got, cur = [], None
    for x in open(f, encoding="utf-8", errors="replace"):
        x = TS.sub("", x.rstrip("\r\n"))
        if x.startswith("##[group]Run "):
            cur = []
            got.append(cur)
            continue
        if cur is not None and x.startswith(ESC):
            cur.append(x[len(ESC):].replace("\x1b[0m", ""))
        elif cur is not None and cur:
            cur = None
    got = [g for g in got if g]
    i, ok, matched = 0, True, 0
    for g in got:
        while i < len(runs) and [l.rstrip() for l in runs[i]] != [l.rstrip() for l in g]:
            i += 1
        if i == len(runs):
            ok = False
            break
        matched += 1
        i += 1
    out[jid] = dict(job=name, wf=WF[w], runs_defined=len(runs), runs_in_log=len(got), matched=matched,
                    all_in_order=ok)
print(json.dumps(out, indent=1))
