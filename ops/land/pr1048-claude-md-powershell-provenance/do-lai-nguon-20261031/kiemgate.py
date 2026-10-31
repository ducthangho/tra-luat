# kiem-gate offline: ten bat buoc = moi job khong skipped cua attempt cuoi cua run; doc readback trong thu muc P.
import json,subprocess,sys,os
P=sys.argv[1]; sha=sys.argv[2]; runs=sys.argv[3:]
print("# kiem-gate offline tren readback-check-runs-<sha>-all.json (filter=all); ten bat buoc = moi job khong skipped cua attempt cuoi cua run do.")
for r in runs:
    run=json.load(open(f"{P}/readback-run-{r}.json")); jobs=json.load(open(f"{P}/readback-jobs-{r}.json"))
    att=run["run_attempt"]; js=[j for j in jobs["jobs"] if j.get("run_attempt",att)==att and j["conclusion"]!="skipped"]
    names=sorted(j["name"] for j in js)
    print(f"== run {r} attempt {att} event {run['event']} conclusion {run['conclusion']} suite {run['check_suite_id']} {len(names)} ten (bo skipped)",flush=True)
    p=subprocess.run([sys.executable,".claude/dev/packet_loop.py","kiem-gate","--head",sha,"--check-runs",f"{P}/readback-check-runs-{sha[:7]}-all.json",*[a for n in names for a in ("--bat-buoc",n)],"--check-suite",str(run["check_suite_id"])],capture_output=True,text=True)
    sys.stdout.write(p.stdout+p.stderr); print(f"rc={p.returncode}")
