#!/usr/bin/env bash
# Gate luot 6 tren dung SHA ung vien: chay_gate2.sh (luat 9, dot bien khai bao, selftest, ci_dang_ky, ruff, diff-check, adr-song, doctrine-scan)
# + cac phep do rieng cua luot 3. Chay khi KHONG co phep do nang nao khac (A/B) dang chay.
# dung: chay_gate3.sh <scratchpad> <goc kho> <sha ung vien> <thu muc ra>
set -u
S="$1"; GOC="$2"; SHA="$3"; RA="$4"
[ ! -e "$RA" ] || { echo "KHONG_DO_DUOC: $RA da ton tai"; exit 2; }
mkdir -p "$RA/x"
[ "$(git -C "$GOC" rev-parse HEAD)" = "$SHA" ] && [ -z "$(git -C "$GOC" status --porcelain)" ] || { echo "KHONG_DO_DUOC: HEAD khac $SHA hoac cay ban"; exit 2; }
bash "$S/gate/chay_gate2.sh" "$GOC" "$RA" "$S/luat9" "$S/chay_ca.py"
export PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1 PYTHONIOENCODING=utf-8
X="$RA/x"; T="$X/tong"
cd "$GOC" || exit 2
echo "bat_dau=$(date -u +%FT%TZ) HEAD=$(git rev-parse HEAD)" > "$T"
python3 "$S/gate/ma_tran_c4.py" "$GOC" > "$X/ma_tran_c4.log" 2>&1; echo "ma_tran rc=$?" >> "$T"
git fetch -q origin '+refs/heads/*:refs/remotes/origin/*'; M=$(git rev-parse origin/master)
python3 "$S/gate/do_kho_that.py" "$S/rig_ab5/sau/.claude/dev/packet_loop.py" "$GOC" "$M" "$X/kho_that_8aab9da.tsv" > "$X/kho_that.log" 2>&1
python3 "$S/gate/do_kho_that.py" .claude/dev/packet_loop.py "$GOC" "$M" "$X/kho_that_$(git rev-parse --short HEAD).tsv" >> "$X/kho_that.log" 2>&1
cmp "$X/kho_that_8aab9da.tsv" "$X/kho_that_$(git rev-parse --short HEAD).tsv" >> "$X/kho_that.log" 2>&1; echo "kho_that cmp rc=$? master=$M" >> "$T"
git ls-tree -r -t -z --name-only "$M" -- ops/land | python3 -c "
import sys,unicodedata
ns=[x for x in sys.stdin.buffer.read().decode().split('\0') if x]
ks={}
for n in ns: ks.setdefault(unicodedata.normalize('NFC',n).casefold(),[]).append(n)
print('master', '$M', 'muc ops/land (ca thu muc):',len(ns),'· nhom trung khoa:',sum(len(v)>1 for v in ks.values()))" >> "$X/kho_that.log" 2>&1
for r in "$S/rig_ab5/sau" "$GOC"; do echo "## $(git -C "$r" rev-parse HEAD) sach=$(git -C "$r" status --porcelain | wc -l)"; python3 "$S/gate/do_probe_l2.py" "$r" 2>&1 | grep -v Warning | tail -2; done > "$X/probe_l2.log"; echo "probe rc=$?" >> "$T"
for r in "$S/rig_ab5/sau" "$GOC"; do echo "## $(git -C "$r" rev-parse HEAD)"; python3 "$S/gate/do_mc11.py" "$r" 2>&1 | grep -v Warning | tail -6; done > "$X/mc11.log"; echo "mc11 rc=$?" >> "$T"
python3 "$S/gate/do_m3.py" "$GOC" "$S/rig_ab5/sau/.claude/dev/packet_loop.py" 2>&1 | grep -v Warning | grep -v trong_bang > "$X/m3_mo_hinh.log"; echo "m3_mo_hinh rc=$?" >> "$T"
bash "$S/gate/do_probe_l4.sh" "$GOC" "$X/pm" origin/ops/wp1236-bc-lease > "$X/probe_l4.log" 2>&1; echo "probe_l4 rc=$?" >> "$T"; rm -f "$X/pm/repo"
for r in "$S/rig_ab5/sau" "$GOC"; do bash "$S/gate/do_probe_l5.sh" "$r" "$X/p5-$(git -C "$r" rev-parse --short HEAD)" "$GOC" origin/ops/wp1236-bc-lease; done > "$X/probe_l5.log" 2>&1; echo "probe_l5 rc=$?" >> "$T"
GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null python3 "$S/gate/do_dich_symlink.py" > "$X/dich_symlink.log" 2>&1; echo "dich_symlink rc=$?" >> "$T"
for r in "$S/rig_ab6/nen" "$S/rig_ab6/sau"; do (cd "$r" && echo "## $(git rev-parse HEAD) · $(python3 -m ruff --version)"; python3 -m ruff check --no-cache --select F --statistics .claude/dev/packet_loop.py .claude/dev/packet_loop_test.py; echo "rc=$?"); done > "$X/ruff_nen.log" 2>&1
echo "ket_thuc=$(date -u +%FT%TZ) HEAD=$(git rev-parse HEAD) sach=$(git status --porcelain | wc -l)" >> "$T"
echo HOAN_TAT >> "$T"
