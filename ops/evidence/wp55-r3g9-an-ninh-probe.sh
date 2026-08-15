#!/usr/bin/env bash
# Phản chứng CHẠY ĐƯỢC cho finding `work-packet-secret-check-prints-secret` (P1 an ninh).
#
# Neo SHA BẤT BIẾN, không ref di động. Chạy từ gốc kho:
#   bash ops/evidence/wp55-r3g9-an-ninh-probe.sh
#
# Không đọc biến bí mật THẬT nào: chỉ bơm một giá trị GIẢ 27 ký tự.

set -u

TRUOC=1a4525a20aa360476a6f59cb157c21097919c457   # head đang bị soi ở lượt review 10
SAU=df5c09cb1f3553cadd3c8d53420420d1d4334438     # head có bản vá an ninh
FAKE='ghp_FAKE_TOKEN_abcdef123456'               # 27 ký tự, GIẢ

# Bóc NGUYÊN VĂN khối lệnh chứa TEN_BIEN ra khỏi adapter tại một SHA.
boc() {
  git show "$1":.claude/skills/work-packet/SKILL.md | python3 -c '
import sys
t=sys.stdin.read().splitlines()
i=0
while i<len(t):
    if t[i].lstrip().startswith("```"):
        j=i+1
        while j<len(t) and not t[j].lstrip().startswith("```"): j+=1
        b="\n".join(t[i+1:j])
        if "TEN_BIEN" in b:
            print(b); sys.exit(0)
        i=j+1; continue
    i+=1
sys.exit(1)'
}

do_mot() {
  nhan="$1"; sha="$2"
  lenh="$(boc "$sha")"
  echo "== $nhan ($sha)"
  echo "-- lệnh trong adapter:"
  echo "$lenh"
  out="$(TEN_BIEN="$FAKE" bash -c "$lenh" 2>&1)"; rc=$?
  echo "-- stdout+stderr: $out"
  echo "-- rc=$rc"
  case "$out" in
    *"$FAKE"*) echo "-- KẾT LUẬN: RÒ RỈ — giá trị giả xuất hiện nguyên văn" ;;
    *)         echo "-- KẾT LUẬN: SẠCH — giá trị giả KHÔNG xuất hiện" ;;
  esac
  echo
}

do_mot "TRƯỚC khi vá" "$TRUOC"
do_mot "SAU khi vá"  "$SAU"

# Vì sao dùng `:+x` chứ không `:-`: dạng `:-` sạch stdout nhưng vẫn in token ra
# vết `set -x`, mà stderr của agent cũng đi vào transcript.
echo "== vết set -x, hai dạng vá khả dĩ"
for d in 'if [ -n "${TEN_BIEN:+x}" ]; then echo "có, ${#TEN_BIEN} ký tự"; else echo "chưa đặt"; fi' \
         'if [ -n "${TEN_BIEN:-}" ];  then echo "có, ${#TEN_BIEN} ký tự"; else echo "chưa đặt"; fi'; do
  v="$(TEN_BIEN="$FAKE" bash -c "set -x; $d" 2>&1)"
  case "$v" in
    *"$FAKE"*) echo "-- RÒ RỈ ra vết : $d" ;;
    *)         echo "-- sạch cả vết  : $d" ;;
  esac
done
