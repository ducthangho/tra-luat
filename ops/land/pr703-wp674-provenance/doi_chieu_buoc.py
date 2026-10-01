"""Doi chieu than `run:` tung buoc cua workflow tai MOT commit voi than buoc in trong log job (dong ESC[36;1m).

Dung: python3 doi_chieu_buoc.py <commit> <thu_muc_log> <readback-jobs-RUN.json> [...]
  <thu_muc_log> chua <run>-<job id>.txt tai qua GET /actions/jobs/<id>/logs (log KHONG commit; bam o SHA256SUMS-log.txt).
Chep tu ops/land/pr701-wp687-provenance/doi_chieu_buoc.py; chi doi: bang JOBS doc tu readback-jobs-*.json (ten job ->
khoa job trong workflow bang cat phan " (" cua ten), thay vi ghi cung.
Gioi han: chi chung minh than buoc da chay khop dinh nghia theo thu tu; KHONG chung minh bytes ngoai than buoc.
"""
import json
import os
import re
import subprocess
import sys

import yaml

commit, logdir, jobfiles = sys.argv[1], sys.argv[2], sys.argv[3:]
WF = {"ci": ".github/workflows/ci.yml", "thu": ".github/workflows/ops-thu-hoi-admission.yml"}
DEFS = {k: yaml.safe_load(subprocess.run(["git", "show", f"{commit}:{p}"], capture_output=True,
                                         text=True, check=True).stdout) for k, p in WF.items()}
JOBS = {}
for jf in jobfiles:
    run = re.search(r"readback-jobs-(\d+)\.json", jf).group(1)
    for j in json.load(open(jf, encoding="utf-8"))["jobs"]:
        if j["status"] != "completed" or j["conclusion"] == "skipped":
            continue
        key = j["name"].split(" (")[0]
        w = "thu" if key == "thu-hoi" else "ci"
        JOBS[f"{run}-{j['id']}"] = (w, key)
TS = re.compile(r"^\S+Z ")
ESC = "\x1b[36;1m"
out = {}
for jid, (w, name) in JOBS.items():
    f = os.path.join(logdir, f"{jid}.txt")
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
