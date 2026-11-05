#!/bin/bash
set -u
H=aad4865c734e7c146463b13ed1750a47e6a9cb8f; R=ducthangho/tra-luat; S=/tmp/claude-0/-home-user-tra-luat/a36066d5-3305-5c52-9b82-9292b9ec44d7/scratchpad; K=$S/km2; V=$S/rv3/runs/dc4d673c
mkdir -p $K && cd $K || exit 9
gh api "repos/$R/actions/runs?head_sha=$H&per_page=100" > runs.json
gh api "repos/$R/commits/$H/check-runs?per_page=100" > check-runs.json
gh api "repos/$R/actions/runs/41387206828/jobs?per_page=100" > jobs.json
gh api "repos/$R/actions/workflows/ci-dot-bien-du.yml/runs?head_sha=$H&per_page=100" > dbd-runs.json
gh api "repos/$R/actions/runs/41376496652/jobs?per_page=100" > dbd-jobs.json
gh api repos/$R/issues/comments/6569226312 > chu-kho.json
python3 - <<'P'
import json,subprocess
R="ducthangho/tra-luat";H="aad4865c734e7c146463b13ed1750a47e6a9cb8f"
g=lambda p: json.loads(subprocess.check_output(["gh","api",p]))
d={"repo":R,"pr":1141,"head_sha":H}
for k,p in (("issue_comments",f"repos/{R}/issues/1141/comments?per_page=100"),("reviews",f"repos/{R}/pulls/1141/reviews?per_page=100"),("review_comments",f"repos/{R}/pulls/1141/comments?per_page=100")):
    it=g(p); d[k]={"total_count":len(it),"items":it}
json.dump(d,open("connector.json","w"))
for f in ("runs.json","check-runs.json","jobs.json"):
    x=json.load(open(f)); k=[k for k in x if isinstance(x[k],list)][0]; print(f,x["total_count"],len(x[k]))
P
git -C /home/user/tra-luat show origin/ops/ci-concurrency-master-r1-lease:ops/leases/ci-concurrency-master-r1-g1-claude-remote-20261102.yaml > lease.yaml
cd /home/user/tra-luat && git fetch -q origin
python .claude/dev/packet_loop.py kiem-merge --root . --repo $R --head $H --base 9091cf52cf20ac197c1a356d6a33cac6bab0b318 --spec ops/specs/CI-CONCURRENCY-MASTER-r1.md --lease $K/lease.yaml --workflow-runs $K/runs.json --check-runs $K/check-runs.json --connector $K/connector.json --offline-run-json $V/run.json --offline-stdout $V/stdout.log --pr 1141 --workflow-jobs $K/jobs.json --chu-kho-comment $K/chu-kho.json --dot-bien-du-runs $K/dbd-runs.json --dot-bien-du-jobs $K/dbd-jobs.json
echo rc=$?
