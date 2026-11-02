#!/usr/bin/env bash
# kiem-merge tren PR #1127, head 06a5a40, chay tu goc kho (repo khong nong, refs/remotes/origin/master moi).
# K4 doc review offline luot 8 (review-offline/run/*-r8.*). Doi so 1 = "am" => bo hai co --dot-bien-du-* (ve am cua K7).
D=ops/land/pr1127-wp1120-provenance
DD=(--dot-bien-du-runs "$D/kiem-merge/ddr.json" --dot-bien-du-jobs "$D/kiem-merge/ddj.json")
[ "${1:-}" = am ] && DD=()
python3 .claude/dev/packet_loop.py kiem-merge --root . --repo ducthangho/tra-luat --pr 1127 \
  --head 06a5a40735d5f486c9ffdedeb9a5ccbfc5c17897 --base f4b513da5802d439aedbe58ae4a5cd38ff47d6ab \
  --spec ops/specs/KIEM-MERGE-M9-r1.md --lease "$D/kiem-merge/lease-truoc-rut-han.yaml" \
  --workflow-runs "$D/kiem-merge/wr.json" --workflow-jobs "$D/kiem-merge/wj.json" --check-runs "$D/kiem-merge/cr.json" \
  --connector "$D/kiem-merge/cn.json" --offline-run-json "$D/review-offline/run/run-r8.json" \
  --offline-stdout "$D/review-offline/run/stdout-r8.log" --windows-json "$D/kiem-merge/win.json" "${DD[@]}"
