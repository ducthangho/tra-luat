#!/usr/bin/env bash
# Mot manh cua luot DOT BIEN DU (dung lenh workflow packet-loop-dot-bien: packet_loop_test_manh.py --dot-bien j/16).
# dung: chay_dot_bien.sh <goc kho> <thu muc ra> <j>...   (cac manh chay TUAN TU trong mot lenh)
set -u
GOC="$1"; RA="$2"; shift 2
mkdir -p "$RA"
cd "$GOC" || exit 2
export PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1 PYTHONIOENCODING=utf-8
for j in "$@"; do
  echo "db $j bat_dau HEAD=$(git rev-parse HEAD) $(date -u +%FT%TZ)" >> "$RA/db.tong"
  python3 .claude/dev/packet_loop_test_manh.py --dot-bien "$j/16" > "$RA/db-$j.log" 2>&1
  echo "db $j rc=$? HEAD=$(git rev-parse HEAD) cay_sach=$(git status --porcelain | wc -l) $(date -u +%FT%TZ) · $(grep '^MẢNH:' "$RA/db-$j.log" | tail -1)" >> "$RA/db.tong"
done
