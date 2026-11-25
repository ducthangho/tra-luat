#!/usr/bin/env bash
# A/B luot 4: dung hai clone (base f602325, ung vien) trong MOT lenh, chay xen ke 16 manh nen + 16 manh dot bien moi ve, roi gom va lap bang.
# dung: ab4_chay.sh <scratchpad> <kho nguon> <sha ung vien>
set -u
S="$1"; NGUON="$2"; SAU="$3"; NEN=f602325574c62184caf16309631f5f680ca5cee2
RIG="$S/rig_ab4"; RA="$S/gate/ab4"
[ ! -e "$RIG" ] && [ ! -e "$RA" ] || { echo "KHONG_DO_DUOC: $RIG hoac $RA da ton tai"; exit 2; }
mkdir -p "$S/gate"
bash "$S/gate/ab_dung.sh" "$NGUON" "$RIG" "$NEN" "$SAU" > "$S/gate/ab4_dung.log" 2>&1 || { cat "$S/gate/ab4_dung.log"; exit 2; }
cat "$S/gate/ab4_dung.log"
J=""; for pha in manh db; do for i in $(seq 0 15); do J="$J nen:$pha:$i sau:$pha:$i"; done; done
# shellcheck disable=SC2086
bash "$S/gate/ab_du.sh" "$RIG" "$RA" 4 $J
for ve in nen sau; do
  (cd "$RIG/$ve" && PACKET_LOOP=chay KQ_MANH=success python3 .claude/dev/packet_loop_test_manh.py --gom "$RA/$ve/manh" --n 16 > "$RA/$ve/gom.log" 2>&1; echo "$ve gom rc=$? HEAD=$(git rev-parse HEAD) sach=$(git status --porcelain | wc -l)")
done
python3 "$S/gate/ab_so.py" "$RA" "$RA/bang_so.md"; echo "ab_so rc=$?"
tail -12 "$RA/bang_so.md"
