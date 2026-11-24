#!/usr/bin/env bash
# Chay 16 manh nen cua packet_loop_test (dung lenh CI: packet_loop_test_manh.py --manh i/16), 4 tien trinh, roi job gom.
# dung: chay_manh.sh <goc kho> <thu muc ra>
set -u
GOC="$1"; RA="$2"
mkdir -p "$RA/manh"
cd "$GOC" || exit 2
echo "HEAD=$(git rev-parse HEAD) bat_dau=$(date -u +%FT%TZ)" > "$RA/manh.tong"
export PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1 PYTHONIOENCODING=utf-8
seq 0 15 | xargs -P 4 -I{} sh -c 'python3 .claude/dev/packet_loop_test_manh.py --manh {}/16 --ra "$0/manh/manh-{}.json" > "$0/manh-{}.log" 2>&1; echo "manh {} rc=$?" >> "$0/manh.tong"' "$RA"
PACKET_LOOP=chay KQ_MANH=success python3 .claude/dev/packet_loop_test_manh.py --gom "$RA/manh" --n 16 > "$RA/gom.log" 2>&1
echo "gom rc=$? ket_thuc=$(date -u +%FT%TZ)" >> "$RA/manh.tong"
echo HOAN_TAT >> "$RA/manh.tong"
