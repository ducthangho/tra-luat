#!/usr/bin/env bash
# kiem-merge tren PR #1231, head d5d521e, base = origin/master a57eade, chay tu goc kho (khong nong).
K=ops/land/pr1231-wp1105-provenance/kiem-merge
python3 .claude/dev/packet_loop.py kiem-merge --root . --repo ducthangho/tra-luat --pr 1231 \
  --head d5d521e3e600e9c549cf5dc9263ffc4385c13407 --base a57eade23dd5b54564be47d4f124511cf87aa1fa \
  --spec ops/specs/launcher-sandbox-lay-mau-r3.md --lease "$K/lease-g3.yaml" \
  --workflow-runs "$K/wr.json" --workflow-jobs "$K/wj.json" --check-runs "$K/cr.json" \
  --connector "$K/cn.json" --offline-run-json "$K/run-offline-l4.json" --offline-stdout "$K/stdout-offline-l4.log" \
  --chu-kho-comment "$K/chu-kho.json" --dot-bien-du-runs "$K/ddr.json" --dot-bien-du-jobs "$K/ddj.json"
