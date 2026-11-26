#!/usr/bin/env bash
# Gate tren dung SHA ung vien (sau 16 manh nen): luat 9 (bo quet ghim qua bo noi), dot bien khai bao, selftest, ruff, ci_dang_ky_test.
# dung: chay_gate2.sh <goc kho> <thu muc ra> <thu muc luat9 (d2b_noi.py, ledger.py)> <chay_ca.py>
set -u
GOC="$1"; RA="$2"; L="$3"; CHAY_CA="$4"
mkdir -p "$RA/luat9"
cd "$GOC" || exit 2
export PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1 PYTHONIOENCODING=utf-8
T="$RA/gate2.tong"
echo "HEAD=$(git rev-parse HEAD) cay_sach=$(git status --porcelain | wc -l) bat_dau=$(date -u +%FT%TZ)" > "$T"
# --- luat 9
cp "$L/d2b_noi.py" "$L/ledger.py" "$RA/luat9/"; : > "$RA/luat9/kho_rong.jsonl"
python3 "$RA/luat9/d2b_noi.py" trich .claude/dev/packet_loop.py "$RA/luat9/d2b_trich.py" > "$RA/luat9/do.log" 2>&1
WP1236C_GOC="$GOC" python3 ops/reviews/wp1236-r10-soan/quet_dot_bien.py do "$RA/luat9/d2b_trich.py" "$RA/luat9/d2b_noi.py" "$RA/luat9/kho_rong.jsonl" --thu-muc-ra "$RA/luat9/D" --song-song 4 >> "$RA/luat9/do.log" 2>&1
echo "luat9 do rc=$? $(grep -c '^HOAN_TAT' "$RA/luat9/do.log") HOAN_TAT · $(grep '^TONG' "$RA/luat9/do.log")" >> "$T"
python3 "$RA/luat9/ledger.py" "$RA/luat9/D" "$RA/luat9/d2b_trich.py" "$RA/luat9/ledger_A.tsv" >> "$T" 2>&1; echo "ledger rc=$?" >> "$T"
# --- dot bien khai bao: ho d2b_ + cac ho dung chung fixture/nhanh phan hang da sua (c1106_, wp1124_, b4_)
(cd .claude/dev && python3 "$CHAY_CA" "$GOC" db d2b_ c1106_ wp1124_ b4_ > "$RA/dot_bien_khai_bao.log" 2>&1); echo "dot bien khai bao rc=$? · $(grep -c '^ok ' "$RA/dot_bien_khai_bao.log") ok · $(grep -c '^DO ' "$RA/dot_bien_khai_bao.log") do · $(tail -1 "$RA/dot_bien_khai_bao.log")" >> "$T"
# --- selftest, ruff, ci_dang_ky, diff-check
python3 scripts/tl.py --selftest > "$RA/selftest.log" 2>&1; echo "selftest rc=$? · $(grep -E '[0-9]+/[0-9]+' "$RA/selftest.log" | tail -1 | cut -c1-160)" >> "$T"
python3 .claude/dev/ci_dang_ky_test.py > "$RA/ci_dang_ky.log" 2>&1; echo "ci_dang_ky_test rc=$? · $(tail -2 "$RA/ci_dang_ky.log" | tr '\n' ' ' | cut -c1-160)" >> "$T"
python3 -m ruff check --select F --statistics .claude/dev/packet_loop.py .claude/dev/packet_loop_test.py > "$RA/ruff_head.log" 2>&1
echo "ruff head: $(grep -E '^ *[0-9]+' "$RA/ruff_head.log" | tr '\t\n' ' ;') · $(python3 -m ruff --version)" >> "$T"
git diff --check origin/master...HEAD > "$RA/diff_check.log" 2>&1; echo "git diff --check rc=$?" >> "$T"
python3 .claude/dev/packet_loop.py adr-song --root . > /dev/null 2>&1; echo "adr-song rc=$?" >> "$T"
python3 .claude/dev/packet_loop.py doctrine-scan --root . > /dev/null 2>&1; echo "doctrine-scan rc=$?" >> "$T"
echo "numstat: $(git diff --numstat origin/master...HEAD | tr '\t\n' ' ;')" >> "$T"
echo "HEAD_cuoi=$(git rev-parse HEAD) cay_sach=$(git status --porcelain | wc -l) ket_thuc=$(date -u +%FT%TZ)" >> "$T"
echo HOAN_TAT >> "$T"
