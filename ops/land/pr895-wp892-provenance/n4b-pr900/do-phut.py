#!/usr/bin/env python3
"""Phut runner = tong (completed_at - started_at) cac job khong skipped, attempt cuoi; doc tu readback-jobs-*.json."""
import json, sys
from datetime import datetime
t = lambda s: datetime.fromisoformat(s.replace("Z", "+00:00"))
for p in sys.argv[1:]:
    jobs = json.load(open(p, encoding="utf-8"))["jobs"]
    last = max(j["run_attempt"] for j in jobs)
    jl = [j for j in jobs if j["run_attempt"] == last and j["conclusion"] != "skipped" and j["started_at"] and j["completed_at"]]
    m = lambda f: sum((t(j["completed_at"]) - t(j["started_at"])).total_seconds() for j in jl if f(j["name"])) / 60
    sk = sorted(j["name"] for j in jobs if j["run_attempt"] == last and j["conclusion"] == "skipped")
    print(f"{p}: job={len(jobs)} chay={len(jl)} tong={m(lambda n: True):.1f} phut gate-cong-cu*={m(lambda n: n.startswith('gate-cong-cu')):.1f} phut skipped={sk}")
