#!/usr/bin/env bash
# B6: suite day du + --dot-bien, nen ab457c6 va ung vien 3089b54, hai Python; toi da 4 song song, moi con deu wait.
A=$1; G=$2; L=$G/log
for py in python3.11 python3.12; do
  for v in nen cay; do
    $G/chay_log.sh $L/B6_suite_${v}_$py.log $A/$v $py -- $py -B .claude/dev/launcher_test.py &
  done
done
wait
for py in python3.11 python3.12; do
  for v in nen cay; do
    $G/chay_log.sh $L/B6_dotbien_${v}_$py.log $A/$v $py -- $py -B .claude/dev/launcher_test.py --dot-bien &
  done
done
wait
echo XONG_B6
