#!/usr/bin/env bash
# PHEP DO DELTA CHI PHI — MOT lenh, hai vong lap, cung cac buoc, chay lien nhau.
# Ban truoc dung `/usr/bin/env time -f` ma container KHONG co GNU time => moi luot
# chet ngay, log 1 dong, script van in ra binh thuong va bao "so ca chay: 0".
# Dung chung benh "rc=0 + output rong" ma CLAUDE.md to cao. Nay co CHOT DUONG:
# thieu dong tong ket thi in KHONG_DO_DUOC va thoat khac 0.
set -u
export PATH="/tmp/actionlint:$PATH"
D=$(mktemp -d /tmp/dohaive-XXXXXX)
ma=0
for cap in "nen:dc02c9beed42bd2ea44a80a2e34e1bbe3acfc6c5" "sau:HEAD_WP530"; do
  ten="${cap%%:*}"; sha="${cap##*:}"
  [ "$sha" = "HEAD_WP530" ] && sha=$(git -C /home/user/tra-luat rev-parse HEAD)
  git clone -q /home/user/tra-luat "$D/$ten"
  git -C "$D/$ten" checkout -q --detach "$sha"
  git -C "$D/$ten" config core.abbrev 7
  t0=$(date +%s.%N)
  ( cd "$D/$ten" && python3 ops/lease_publish_test.py > "$D/$ten.log" 2>&1 )
  rc=$?
  t1=$(date +%s.%N)
  echo "=== VE $ten  sha=$(git -C "$D/$ten" rev-parse --short HEAD)  rc=$rc ==="
  if ! grep -qE "^lease_publish: [0-9]+/[0-9]+ dat|^lease_publish: [0-9]+/[0-9]+ đạt" "$D/$ten.log"; then
    echo "  KHONG_DO_DUOC: khong co dong tong ket trong log ($(wc -l < "$D/$ten.log") dong)"
    tail -3 "$D/$ten.log" | sed 's/^/    /'
    ma=1; continue
  fi
  grep -E "^lease_publish:" "$D/$ten.log" | sed 's/^/  /'
  printf '  TONG_GIAY %.1f\n' "$(echo "$t1 - $t0" | bc)"
  grep -E "^<<< ra t125" "$D/$ten.log" | sed 's/^/  /'
  echo "  so ca chay: $(grep -cE '^<<< ra ' "$D/$ten.log")"
done
echo "=== log giu o $D · ma=$ma ==="
exit $ma
