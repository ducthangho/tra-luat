#!/bin/bash
# Nghiem thu #1288 tren c0b8e11 (sau) vs bab2279 (nen); hai clone dung trong MOT lenh truoc do.
S=/tmp/claude-0/-home-user-tra-luat/79a88adb-aaca-57d8-8d60-0e2c734dd105/scratchpad/nt1288
K=/home/user/tra-luat/ops/land/pr1270-wp1179-provenance/kiem-merge
cd $S; [ -d h1270 ] || { git clone -q /home/user/tra-luat h1270 && (cd h1270 && git checkout -q 5824094e78a0afe9d0af8866df45c50b24334767 && git config core.abbrev 7); }
date -u +"# luc %Y-%m-%dT%H:%M:%SZ"
echo "# C5 — kiem-merge tren dau vao that PR #1270 (ops/land/pr1270-wp1179-provenance/kiem-merge/, cwd h1270 @ $(git -C h1270 rev-parse HEAD))"
for n in nen sau; do
  echo "## $n $(git -C $n rev-parse HEAD) packet_loop.py blob $(git -C $n rev-parse HEAD:.claude/dev/packet_loop.py)"
  rm -rf st-$n; (cd h1270 && python3 ../$n/.claude/dev/packet_loop.py --state-dir ../st-$n kiem-merge --root . --repo ducthangho/tra-luat --pr 1270 --head 5824094e78a0afe9d0af8866df45c50b24334767 --base 3cc0bc7b1dd26955b6fd4cc96612d9fbacc8a8d4 --spec ops/specs/wp1179-c1a1b-r9.md --lease $K/lease.yaml --workflow-runs $K/runs.json --check-runs $K/check-runs.json --workflow-jobs $K/jobs.json --connector $K/connector.json --human-audit-comment $K/audit.json --human-remote-run $K/remote-run-som.json --chu-kho-comment $K/chu-kho.json --dot-bien-du-runs $K/dbd-runs.json --dot-bien-du-jobs $K/dbd-jobs.json 2>&1); echo "rc=$?"
done
echo "# C6"
for n in nen sau; do echo "## $n"; (cd $n && python3 .claude/dev/packet_loop.py doctrine-scan --root . >/dev/null 2>&1; echo "doctrine-scan rc=$?"; python3 .claude/dev/packet_loop.py adr-song --root . >/dev/null 2>&1; echo "adr-song rc=$?"; for f in .claude/dev/packet_loop.py .claude/dev/packet_loop_test.py; do echo "ruff F $f: $(python3 -m ruff check --select F --output-format concise $f 2>/dev/null | grep -cE ':[0-9]+:[0-9]+: F')"; done); done
echo "# C3 — packet_loop_test toan bo"
for n in nen sau; do echo "## $n"; (cd $n && python3 .claude/dev/packet_loop_test.py > ../plt-$n.out 2>&1; echo "rc=$?"; grep -E 'SỐ LIỆU|^TỔNG' ../plt-$n.out | tail -3; echo "k3s ca: $(grep -cE '^(OK|ĐẠT|PASS).*k3s_|k3s_' ../plt-$n.out)"); done
