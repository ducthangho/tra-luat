"""Doi chieu than `run:` tung buoc cua workflow tai MOT commit voi than buoc in trong log job (dong ESC[36;1m).

Dung: python3 doi_chieu_buoc.py <commit> <thu_muc_log>
  <thu_muc_log> chua job-<id>.log tai qua GET /actions/jobs/<id>/logs (log KHONG commit; bam o SHA256SUMS-log-va-artifact.txt).
Chay trong mot clone co commit ay. Phuong phap = ops/land/pr696-wp668-provenance/doi_chieu_buoc.py (chep), chi doi bang JOBS va WF cho PR #701 (them ops-thu-hoi-admission.yml).
Gioi han: chi chung minh than buoc da chay khop dinh nghia theo thu tu; KHONG chung minh bytes ngoai than buoc.
"""
import json
import os
import re
import subprocess
import sys

import yaml

commit, logdir = sys.argv[1], sys.argv[2]
JOBS = {  # job id -> (workflow, job key): run 36816901782 (pull_request, 9d7a523), 36816901794 + 36820845090 (thu-hoi, pull_request_target), 36821075373 (push, 163fd5d)
    "110223837721": ('ci', 'chuan-bi'),
    "110223856580": ('ci', 'gate-packet-loop'),
    "110223856617": ('ci', 'gate-ops'),
    "110223856664": ('ci', 'gate'),
    "110223856674": ('ci', 'gate-registry'),
    "110223856794": ('ci', 'gate-cong-cu'),
    "110223856796": ('ci', 'gate-cong-cu'),
    "110223856808": ('ci', 'gate-cong-cu'),
    "110223856829": ('ci', 'gate-cong-cu'),
    "110223856832": ('ci', 'gate-cong-cu'),
    "110223856857": ('ci', 'gate-cong-cu'),
    "110223856860": ('ci', 'gate-cong-cu'),
    "110223856885": ('ci', 'gate-cong-cu'),
    "110228105307": ('ci', 'gate-cong-cu-gop'),
    "110223837650": ('thu', 'thu-hoi'),
    "110235879821": ('thu', 'thu-hoi'),
    "110236563916": ('ci', 'chuan-bi'),
    "110236586544": ('ci', 'gate-packet-loop'),
    "110236586550": ('ci', 'gate-ops'),
    "110236586567": ('ci', 'gate'),
    "110236586570": ('ci', 'gate-registry'),
    "110236586616": ('ci', 'gate-cong-cu'),
    "110236586633": ('ci', 'gate-cong-cu'),
    "110236586662": ('ci', 'gate-cong-cu'),
    "110236586695": ('ci', 'gate-cong-cu'),
    "110236586713": ('ci', 'gate-cong-cu'),
    "110236586718": ('ci', 'gate-cong-cu'),
    "110236586745": ('ci', 'gate-cong-cu'),
    "110236586755": ('ci', 'gate-cong-cu'),
    "110241086195": ('ci', 'gate-cong-cu-gop'),
}
WF = {"ci": ".github/workflows/ci.yml", "thu": ".github/workflows/ops-thu-hoi-admission.yml"}
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
