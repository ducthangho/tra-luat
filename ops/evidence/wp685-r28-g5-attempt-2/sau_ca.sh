#!/usr/bin/env bash
# B1-B4, B8: sau ca moi (t156..t161), moi ca mot lan. attempt 2: rc tong = 1 neu BAT KY ca nao rc!=0 (ban attempt 1
# tra rc cua lenh echo cuoi, tuc luon 0 — rc cua tung ca chi doc duoc o dong "### tNNN rc=").
py=$1; tong=0
for c in t156 t157 t158 t159 t160 t161; do echo "### $c"; $py -B .claude/dev/launcher_test.py --lap-ca $c --lan 1; r=$?; echo "### $c rc=$r"; [ $r -ne 0 ] && tong=1; done
echo "### TONG rc=$tong"; exit $tong
