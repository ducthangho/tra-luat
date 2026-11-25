#!/usr/bin/env bash
# Ve KHONG HOI QUY (dieu phoi, 11:58Z 24-11): packet_loop_test DAY DU tren base va head, hai clone dung trong MOT lenh (ab_dot_bien.sh),
# chay XEN KE trong cung mot lenh. Moi viec = <ve>:<pha>:<chi so>, pha = manh (nen i/16) | db (dot bien j/16). Chay lai thi bo qua viec da co ket qua.
# dung: ab_du.sh <thu muc rig co nen/ va sau/> <thu muc ra> <so tien trinh> <viec>...
set -u
RIG="$1"; RA="$2"; P="$3"; shift 3
mkdir -p "$RA/nen/manh" "$RA/sau/manh"
export PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1 PYTHONIOENCODING=utf-8 RIG RA
mot() {
  ve="${1%%:*}"; r="${1#*:}"; pha="${r%%:*}"; i="${r##*:}"
  grep -q "^$ve $pha $i rc=" "$RA/ab.tong" 2>/dev/null && return 0
  cd "$RIG/$ve" || return 2
  h="$(git rev-parse HEAD)"; t0=$(date +%s)
  if [ "$pha" = manh ]; then
    python3 .claude/dev/packet_loop_test_manh.py --manh "$i/16" --ra "$RA/$ve/manh/manh-$i.json" > "$RA/$ve/manh-$i.log" 2>&1
  else
    python3 .claude/dev/packet_loop_test_manh.py --dot-bien "$i/16" > "$RA/$ve/db-$i.log" 2>&1
  fi
  echo "$ve $pha $i rc=$? HEAD=$h cay_sach=$(git status --porcelain | wc -l) $(( $(date +%s) - t0 ))s $(date -u +%FT%TZ)" >> "$RA/ab.tong"
}
export -f mot
printf '%s\n' "$@" | xargs -P "$P" -I{} bash -c 'mot {}'
echo "LO_XONG $* $(date -u +%FT%TZ)" >> "$RA/ab.tong"
