#!/usr/bin/env bash
# kiem-merge tren PR #1242, head 97cb2dd, chay tu goc kho (repo khong nong, refs/remotes/origin/master moi) — phien
# session_015GtxrZX3cx55Fs3dp8KLdr, 2026-11-05T18:19Z. Ket qua: kiem-merge.out ("ĐỦ ĐIỀU KIỆN MERGE trên 97cb2dd…"), rc=0.
D=ops/land/pr1242-wp1237-provenance/kiem-merge
python3 .claude/dev/packet_loop.py kiem-merge --root . --repo ducthangho/tra-luat --pr 1242 \
  --head 97cb2dda246886c7d4bec2bea4a4b89342403a65 --base fe84620f897913c7f6c2ce5a0c7316a49655e82f \
  --spec ops/specs/wp1237-r1.md --lease "$D/lease.yaml" \
  --workflow-runs "$D/wr.json" --workflow-jobs "$D/wj.json" --check-runs "$D/cr.json" --connector "$D/cn.json" \
  --offline-run-json "$D/run-offline-l4.json" --offline-stdout "$D/stdout-offline-l4.log" \
  --windows-json "$D/win.json" --dot-bien-du-runs "$D/ddr.json" --dot-bien-du-jobs "$D/ddj.json"
