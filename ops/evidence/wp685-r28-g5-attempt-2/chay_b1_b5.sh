#!/usr/bin/env bash
# B1-B5, B8 + ruff/numstat tren cay SACH 3089b54 (cay), nen ab457c6 (nen), va nen + test ung vien (nen_testuv).
# Toi da 4 song song; moi con deu wait.
A=$1; G=$2; L=$G/log; SPEC=$A/spec_r28.md; C=$G/chay_log.sh
for py in python3.11 python3.12; do
  $C $L/B1-B4_B8_cay_$py.log $A/cay $py -- $G/sau_ca.sh $py &
  $C $L/B1-B4_B8_nen_testuv_$py.log $A/nen_testuv $py -- $G/sau_ca.sh $py &
done
wait
for py in python3.11 python3.12; do
  $C $L/B2_chot_tinh_$py.log $A/cay $py -- $py -B $G/chot_tinh_r12.py $A/nen/.claude/dev/launcher.py .claude/dev/launcher.py .claude/dev/launcher_test.py
done
$C $L/B4_san_windows.log $A/cay python3.12 -- bash -c "python3.12 -B $G/san_windows.py $A/nen/.claude/dev/launcher_test.py; r1=\$?; python3.12 -B $G/san_windows.py .claude/dev/launcher_test.py; r2=\$?; exit \$((r1|r2))"
for v in nen cay; do
  $C $L/B6_ruff_$v.log $A/$v python3.12 -- bash -c "ruff --version; ruff check --no-cache --select F --target-version py311 --output-format concise .claude/dev/launcher.py .claude/dev/launcher_test.py"
done
$C $L/B6_git_numstat_grep.log $A/cay python3.12 -- bash -c "git diff --numstat ab457c651eb4428705f0492163080b661c858b72 HEAD; git diff --check ab457c651eb4428705f0492163080b661c858b72 HEAD; echo diff-check rc=\$?; git diff --name-only ab457c651eb4428705f0492163080b661c858b72 HEAD; git grep -n 'linux:' -- .claude/dev/launcher.py; git diff --quiet 423b4ba14078701859b9e6ac101a68a3fc4ddef4 ab457c651eb4428705f0492163080b661c858b72 -- .claude/dev/launcher.py .claude/dev/launcher_test.py; echo write-set-nen-nghiem-thu=ab457c6 rc=\$?"
for py in python3.11 python3.12; do
  $C $L/B5_AW_D_$py.log $A/cay $py -- $py -B $G/bang_chung_aw_d.py .claude/dev $A/tam/aw_$py all $SPEC $L/bang_D_$py.json &
  $C $L/B5_E_$py.log $A/cay $py -- $py -B $G/bang_chung_e.py .claude/dev $A/tam/e_$py $SPEC $L/bang_E_$py.json &
done
wait
for py in python3.11 python3.12; do
  $C $L/B5_D_phan_chung_$py.log $A/cay $py -- $py -B $G/phan_chung_d.py $G/bang_chung_aw_d.py .claude/dev $A/tam/pc_$py $SPEC &
done
wait
echo XONG_B1_B5
