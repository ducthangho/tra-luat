"""Doi chieu than `run:` tung buoc cua workflow tai MOT commit voi than buoc in trong log job (dong ESC[36;1m).

Dung: python3 doi_chieu_buoc.py <commit> <thu_muc_log>
  <thu_muc_log> chua job-<id>.log tai qua GET /actions/jobs/<id>/logs (log KHONG commit; bam o SHA256SUMS-log-va-artifact.txt).
Chay trong mot clone co commit ay. Phuong phap = ops/land/pr666-wp650-provenance/doi_chieu_buoc.py, doi bang job va commit.
Gioi han: chi chung minh than buoc da chay khop dinh nghia theo thu tu; KHONG chung minh bytes ngoai than buoc.
"""
import json
import os
import re
import subprocess
import sys

import yaml

commit, logdir = sys.argv[1], sys.argv[2]
JOBS = {  # job id -> (workflow, job key) cua run 36696528580 (ci.yml) va 36696528630 (launcher-windows.yml)
    "109832781733": ("ci", "gate"), "109832783087": ("ci", "gate-packet-loop"),
    "109832781847": ("ci", "gate-ops"), "109832781963": ("ci", "gate-cong-cu"),
    "109832782054": ("ci", "gate-cong-cu"), "109832782147": ("ci", "gate-cong-cu"),
    "109832781925": ("ci", "gate-cong-cu"), "109832782454": ("ci", "gate-cong-cu"),
    "109832782231": ("ci", "gate-cong-cu"), "109832782080": ("ci", "gate-cong-cu"),
    "109832782109": ("ci", "gate-cong-cu"), "109838992820": ("ci", "gate-cong-cu-gop"),
    "109832739668": ("ci", "chuan-bi"),
    "109825710705": ("lw", "launcher"), "109825711407": ("lw", "launcher"),
}
WF = {"ci": ".github/workflows/ci.yml", "lw": ".github/workflows/launcher-windows.yml"}
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
