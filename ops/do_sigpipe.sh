#!/usr/bin/env bash
# ops/do_sigpipe.sh [--lan N] [--goc THU_MUC] — phep do phan chung cho #675: khong con pipeline
# "nguoi doc thoat som" (`| head -1`) duoi `set -e` + `pipefail` trong 3 script ops.
#
# CO CHE: builtin `printf '%s\n' "$X"` goi mot write() moi dong. Neu `head` thoat truoc lan ghi sau,
# printf an SIGPIPE, pipefail day 141 len, `set -e` giet script khong in gi. Do: 2/3000 (dau vao 2 dong),
# tat dinh 10/10 rc=141 (20000 dong).
#
# DO GI:
#   (a) tuong duong  — dong TRICH TU CHINH script va dang pipeline cu (dung san o day lam doi chung)
#       cho CUNG gia tri tren tap dau vao 1 dong/nhieu dong/CRLF/rong/dong dau rong/khong LF cuoi.
#   (b) tat dinh     — dau vao 20000 dong trong `bash -c 'set -euo pipefail; ...'`: dang cu PHAI rc=141
#       moi lan (chung minh dau vao co rang), dong trich PHAI rc=0 moi lan.
#   (c) tu kiem      — dua dong trich ve dang pipeline TREN BAN SAO TAM (khong bao gio tren tep that);
#       (b) PHAI do va do DUNG ly do (rc=141 moi lan, khong phai loi vo can).
# Dong duoc trich theo TEN BIEN dau ra (`^BIEN=`), KHONG chep lai; khong ra dung MOT dong => KHONG DO DUOC.
# --goc: thu muc goc chua ops/{cai_cong_cu,cai_actionlint,dung_goi_review}.sh (de do baseline, khong dung tep that).
# Ma thoat: 0 = N/N · 1 = co phep do DO · 2 = KHONG DO DUOC (dung sai / trich khong ra / thieu tep).
set -euo pipefail

DONG_LON=20000
LAN=10
GOC="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

khong_do() { echo "KHÔNG ĐO ĐƯỢC: $*" >&2; exit 2; }

while [ $# -gt 0 ]; do
  case "$1" in
    --lan)  [ $# -ge 2 ] || khong_do "--lan thieu gia tri"; LAN="$2"; shift 2 ;;
    --goc)  [ $# -ge 2 ] || khong_do "--goc thieu gia tri"
            GOC="$(cd -- "$2" 2>/dev/null && pwd)" || khong_do "--goc khong vao duoc: $2"; shift 2 ;;
    *) echo "dung: $0 [--lan N] [--goc THU_MUC]" >&2; exit 2 ;;
  esac
done
[[ "$LAN" =~ ^[1-9][0-9]*$ ]] || khong_do "--lan phai la so nguyen duong, nhan '$LAN'"

# Ba diem do. Chi so i: ten · tep · bien DAU RA (dong trich gan bien nay) · bien DAU VAO · dang cu.
TEN=(cai_cong_cu cai_actionlint dung_goi_review)
TEP=(ops/cai_cong_cu.sh ops/cai_actionlint.sh ops/dung_goi_review.sh)
RA=(LENH DONG1 al_ban)
VAO=(DAU_RA RA al_raw)
CU=(
  "$(cat <<'EOF'
LENH="$(printf '%s\n' "$DAU_RA" | head -1)"
EOF
)"
  "$(cat <<'EOF'
DONG1="$(printf '%s\n' "$RA" | head -1 | tr -d '\r')"
EOF
)"
  "$(cat <<'EOF'
al_ban=$(printf '%s' "$al_raw" | head -1 | tr -d '\r')
EOF
)"
)

DV_TEN=(mot-dong nhieu-dong crlf cr-giua-dong rong dong-dau-rong khong-LF-cuoi co-LF-cuoi chi-CR crlf-dong-dau-rong thuc-te)
DV_GT=('a' $'a\nb\nc' $'a\r\nb\r\n' $'a\rb\nc' '' $'\nsecond' $'a\nb' $'a\nb\n' $'\r' $'\r\nb' $'1.7.7\ninstalled by downloading\nbuilt with go1.22')

TMP="$(mktemp -d)"
trap 'rm -rf -- "$TMP"' EXIT

TRICH_DONG=""; TRICH_SO=0
trich() {  # trich GOC I -> TRICH_DONG, TRICH_SO. Khong ra dung MOT dong thi KHONG DO DUOC.
  local f="$1/${TEP[$2]}" kh
  [ -f "$f" ] || khong_do "thieu tep $f"
  mapfile -t kh < <(grep -nE "^[[:space:]]*${RA[$2]}=" "$f" || true)
  [ "${#kh[@]}" -eq 1 ] || khong_do "${TEP[$2]}: '^${RA[$2]}=' ra ${#kh[@]} dong, can dung 1"
  TRICH_DONG="${kh[0]#*:}"; TRICH_SO="${kh[0]%%:*}"
  case "$TRICH_DONG" in *"${VAO[$2]}"*) ;; *) khong_do "${TEP[$2]}:$TRICH_SO khong doc bien dau vao ${VAO[$2]}" ;; esac
  case "$TRICH_DONG" in *\\) khong_do "${TEP[$2]}:$TRICH_SO ket thuc bang '\\' (nhieu dong)" ;; esac
}

# Dang cu o (a) chay `set -u` (khong pipefail) de doi chung TAT DINH; duoi pipefail no la thu bi do o (b).
chay_gia_tri() {  # chay_gia_tri CHE_DO DONG VAO RA DAU_VAO -> in [gia tri]
  local ma="set -$1; $3=\$1; $2; printf '[%s]' \"\${$4}\""
  bash -c "$ma" _ "$5"
}

DEM_0=0; DEM_141=0; DEM_KHAC=0
dem_rc() {  # dem_rc DONG VAO -> DEM_*: chay LAN lan duoi set -euo pipefail voi DONG_LON dong
  local ma="set -euo pipefail; $2=\"\$(seq 1 $DONG_LON)\"; $1; :" k rc
  DEM_0=0; DEM_141=0; DEM_KHAC=0
  for ((k = 0; k < LAN; k++)); do
    rc=0; bash -c "$ma" >/dev/null 2>&1 || rc=$?
    case "$rc" in 0) DEM_0=$((DEM_0 + 1)) ;; 141) DEM_141=$((DEM_141 + 1)) ;; *) DEM_KHAC=$((DEM_KHAC + 1)) ;; esac
  done
}

TONG=0; DAT=0
ghi() {  # ghi <0|1> nhan chi-tiet
  TONG=$((TONG + 1))
  if [ "$1" -eq 0 ]; then DAT=$((DAT + 1)); else printf '  ĐỎ  %s  %s\n' "$2" "$3"; fi
}

DK="bash $BASH_VERSION, $(nproc 2>/dev/null || echo '?') loi, $LAN lan, $DONG_LON dong"
echo "do_sigpipe: goc=$GOC · $DK"
for i in "${!TEN[@]}"; do
  trich "$GOC" "$i"
  dong="$TRICH_DONG"
  printf '%s  %s:%s\n    %s\n' "${TEN[$i]}" "${TEP[$i]}" "$TRICH_SO" "$dong"

  # (a) tuong duong tren tap dau vao
  for j in "${!DV_TEN[@]}"; do
    rc=0; moi="$(chay_gia_tri euo\ pipefail "$dong" "${VAO[$i]}" "${RA[$i]}" "${DV_GT[$j]}")" || rc=$?
    rc2=0; cu="$(chay_gia_tri u "${CU[$i]}" "${VAO[$i]}" "${RA[$i]}" "${DV_GT[$j]}")" || rc2=$?
    if [ "$rc" -eq 0 ] && [ "$rc2" -eq 0 ] && [ "$moi" = "$cu" ]; then ghi 0 "" ""
    else ghi 1 "(a) ${TEN[$i]}/${DV_TEN[$j]}" "trich rc=$rc '$moi' · cu rc=$rc2 '$cu'"; fi
  done

  # (b) tat dinh: doi chung dang cu 141 moi lan, dong trich 0 moi lan
  dem_rc "${CU[$i]}" "${VAO[$i]}"
  if [ "$DEM_141" -eq "$LAN" ]; then ghi 0 "" ""
  else ghi 1 "(b) ${TEN[$i]}/doi-chung-dang-cu" "can 141 x$LAN, do rc0=$DEM_0 rc141=$DEM_141 khac=$DEM_KHAC (dau vao khong co rang)"; fi
  dem_rc "$dong" "${VAO[$i]}"
  if [ "$DEM_0" -eq "$LAN" ]; then ghi 0 "" ""
  else ghi 1 "(b) ${TEN[$i]}/dong-trich" "can rc=0 x$LAN, do rc0=$DEM_0 rc141=$DEM_141 khac=$DEM_KHAC"; fi

  # (c) tu kiem: dua dong trich ve dang cu tren BAN SAO TAM; (b) phai do, va do DUNG ly do (141)
  mkdir -p "$TMP/mut-$i/ops"
  for f in "${TEP[@]}"; do cp -- "$GOC/$f" "$TMP/mut-$i/$f"; done
  {
    head -n "$((TRICH_SO - 1))" "$GOC/${TEP[$i]}"
    printf '%s\n' "${CU[$i]}"
    tail -n "+$((TRICH_SO + 1))" "$GOC/${TEP[$i]}"
  } > "$TMP/mut-$i/${TEP[$i]}"
  trich "$TMP/mut-$i" "$i"
  [ "$TRICH_DONG" = "${CU[$i]}" ] || khong_do "dot bien ${TEN[$i]} khong dua duoc dong ve dang cu"
  dem_rc "$TRICH_DONG" "${VAO[$i]}"
  if [ "$DEM_141" -eq "$LAN" ]; then ghi 0 "" ""
  else ghi 1 "(c) ${TEN[$i]}/dot-bien-pipeline" "phai DO bang rc=141 x$LAN, do rc0=$DEM_0 rc141=$DEM_141 khac=$DEM_KHAC"; fi
done

# Ca CO MAT khac ca co DO: so phep da ghi phai bang so phep khai bao (vong lap khong duoc nuot ca nao).
MONG=$(( ${#TEN[@]} * (${#DV_TEN[@]} + 3) ))
[ "$TONG" -eq "$MONG" ] || khong_do "ghi $TONG phep, khai bao $MONG"

if [ "$DAT" -eq "$TONG" ]; then
  echo "do_sigpipe: $DAT/$TONG DAT ($DK)"
  exit 0
fi
echo "do_sigpipe: $DAT/$TONG — CO PHEP DO ĐỎ ($DK)"
exit 1
