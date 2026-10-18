#!/usr/bin/env bash
# B6 lan 2: suite day du chay TUAN TU (mot tien trinh mot luc) — tach "t72 do tai/thu tu" khoi hoi quy.
A=$1; G=$2
for py in python3.11 python3.12; do for v in nen cay; do
  $G/chay_log.sh $G/log/B6_suite_tuan_tu_${v}_$py.log $A/$v $py -- $py -B .claude/dev/launcher_test.py
done; done
echo XONG_TUAN_TU
