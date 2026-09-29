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
#       cham bang CHINH ham cham cua (b) (`cham_b`) va doi ket qua DO vi rc=141 moi lan (khong phai loi vo can).
#   (d) duong chay that — dong trich phai NAM TREN DUONG CHAY: chay CHINH tep (ban sao TAM cat sau dong trich) voi
#       dau vao gia offline 20000 dong, doi dong chung minh ghi gia tri dung. Dong trong ham khong goi / here-doc /
#       sau `exit` => dong chung minh khong chay => DO. (Khop van ban chua phai la co mat tren duong chay.)
#   (e) B1 — `lam()` cua ops/don_ref_chot_test.sh: khop dau doi so + >= 20000 doi so dem KHONG duoc noi fallback.
# Dong duoc trich theo TEN BIEN dau ra (`^BIEN=`), KHONG chep lai; khong ra dung MOT dong => KHONG DO DUOC.
# --goc: thu muc goc chua ops/{cai_cong_cu,cai_actionlint,dung_goi_review,don_ref_chot_test}.sh (de do baseline).
# Ma thoat: 0 = N/N · 1 = co phep do DO · 2 = KHONG DO DUOC (dung sai / trich khong ra / thieu tep — nen TEN tep).
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

DV_TEN=(mot-dong nhieu-dong crlf cr-giua-dong rong dong-dau-rong khong-LF-cuoi co-LF-cuoi chi-CR crlf-dong-dau-rong thuc-te glob-mot-dong glob-dong-dau glob-crlf)
DV_GT=('a' $'a\nb\nc' $'a\r\nb\r\n' $'a\rb\nc' '' $'\nsecond' $'a\nb' $'a\nb\n' $'\r' $'\r\nb' $'1.7.7\ninstalled by downloading\nbuilt with go1.22'
       '*' $'a*b?c[d]e%s%%\nz*' $'x*?\r\n[y]%')

TMP="$(mktemp -d)"
trap 'rm -rf -- "$TMP"' EXIT
W5=ops/don_ref_chot_test.sh
# F2: thieu tep nao => KHONG DO DUOC nen TEN tep, TRUOC moi phep do/chep (khong de `cp` chet rc=1 giua chung).
for f in "${TEP[@]}" "$W5"; do [ -f "$GOC/$f" ] || khong_do "thieu tep $GOC/$f"; done

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

# Ham cham cua (b) — (b) VA (c) di qua CHINH no (F3): doi nhanh cham nay thanh luon-dung thi (c) do.
cham_b() {  # cham_b DONG VAO -> KQ=DAT (rc=0 moi lan) | DO; so dem o DEM_*
  dem_rc "$1" "$2"
  if [ "$DEM_0" -eq "$LAN" ]; then KQ=DAT; else KQ=DO; fi
}

# (d) fixture offline: bo phat "1.7.7" CRLF + DONG_LON dong (moi `| head -1` cu deu an SIGPIPE), goi tar.gz chua
# `actionlint` gia (cho W2/W3), khong mang, khong cai that, chi ghi trong $TMP.
GIA="$TMP/gia"; mkdir -p "$TMP/goi"
printf '#!/bin/sh\nprintf "1.7.7\\r\\n"; seq 1 %s\n' "$DONG_LON" > "$GIA"
cp -- "$GIA" "$TMP/goi/actionlint"; chmod +x "$GIA" "$TMP/goi/actionlint"
tar -czf "$TMP/goi.tar.gz" -C "$TMP/goi" actionlint || khong_do "khong dung duoc goi gia (tar)"
if command -v sha256sum >/dev/null 2>&1; then SHA="$(sha256sum < "$TMP/goi.tar.gz")"
elif command -v shasum >/dev/null 2>&1; then SHA="$(shasum -a 256 < "$TMP/goi.tar.gz")"
else khong_do "thieu sha256sum/shasum de dung goi gia"; fi
SHA="${SHA%% *}"

chay_that() {  # chay_that I (sau `trich`): chay ban sao TAM cat SAU dong trich + dong chung minh -> DO_RC, DO_GT
  local i="$1" rc=0
  local d="$TMP/that-$i"
  mkdir -p "$d/ops" "$d/bin" || khong_do "khong dung duoc fixture $d"
  cp -- "$GIA" "$d/bin/python" || khong_do "khong chep duoc bo phat gia vao $d/bin"
  # W3 goi installer: dung BO CAI GIA (chep binary gia) de diem W3 do DOC LAP voi W2 — W2 baseline khong lam W3 do theo.
  printf '%s\n' "mkdir -p \"\$AL_DICH\" && cp \"$GIA\" \"\$AL_DICH/actionlint\"" > "$d/ops/cai_actionlint.sh"
  { head -n "$TRICH_SO" "$GOC/${TEP[$i]}"; printf '%s\n' "printf '%s' \"\$${RA[$i]}\" > \"\$SENT_TEP\"; exit 0"; } > "$d/${TEP[$i]}"
  local E=(env SENT_TEP="$d/sent" AL_VER=1.7.7 AL_NEN=Linux AL_GOI="$TMP/goi.tar.gz" AL_SHA256="$SHA" AL_DICH="$d/al" PATH="$d/bin:$PATH")
  case "$i" in
    0) "${E[@]}" bash "$d/${TEP[0]}" actionlint ;;
    1) "${E[@]}" bash "$d/${TEP[1]}" ;;
    *) ( cd "$d" && git init -q && git -c commit.gpgsign=false -c user.name=t -c user.email=t@t commit -q --allow-empty -m t \
           && git remote add origin "$d" ) || khong_do "khong dung duoc kho git gia $d"
       "${E[@]}" bash "$d/${TEP[2]}" "$d/r" "$(git -C "$d" rev-parse HEAD)" "$d" ;;
  esac >/dev/null 2>&1 || rc=$?
  DO_RC=$rc; DO_GT="(khong ghi)"; if [ -f "$d/sent" ]; then DO_GT="$(<"$d/sent")"; fi
}

# (e) B1: chay CHINH ham `lam()` trich tu W5 voi `env` la ham ghi lai doi so (khong chay gi that), duoi pipefail nhu W5.
{ cat <<'EOF'
set -uo pipefail; TAM=$1; shift; S1=s1; QUA=0; HONG=0
env() { printf '%s\n' "$@" > "$TAM/env.log"; }
EOF
  sed -n '/^lam() {/,/^}/p' "$GOC/$W5"
  cat <<'EOF'
lam t 0 xoa-nhanh r1 sha thu "$@"
EOF
} > "$TMP/b1.sh"
grep -q '^lam() {' "$TMP/b1.sh" || khong_do "$W5: khong trich duoc ham lam()"
mapfile -t PAD < <(seq -f 'P%g=x' 1 "$DONG_LON")
mkdir -p "$TMP/b1"
b1() {  # b1 NHAN REF_MONG NEO_MONG ARG... : moi lan lam() phai chuyen cho env DUNG MOT dong moi bien, dung gia tri mong
  local nhan="$1" rmong="$2" nmong="$3" k nr nn tot=1; shift 3
  for ((k = 0; k < LAN; k++)); do
    rm -f -- "$TMP/b1/env.log"; bash "$TMP/b1.sh" "$TMP/b1" "$@" >/dev/null 2>&1 || true
    nr="$(grep -c '^GIA_REF_STATE=' "$TMP/b1/env.log" 2>/dev/null || true)"; nn="$(grep -c '^NEO_TEP=' "$TMP/b1/env.log" 2>/dev/null || true)"
    if [ "$nr" = 1 ] && [ "$nn" = 1 ] && grep -qxF "GIA_REF_STATE=$rmong" "$TMP/b1/env.log" && grep -qxF "NEO_TEP=$nmong" "$TMP/b1/env.log"; then :
    else tot=0; break; fi
  done
  if [ "$tot" -eq 1 ]; then ghi 0 "" ""; else ghi 1 "(e) B1/$nhan" "lan $((k + 1)): GIA_REF_STATE x${nr:-0} NEO_TEP x${nn:-0}; mong moi bien DUNG 1 dong '$rmong' / '$nmong'"; fi
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
  cham_b "$dong" "${VAO[$i]}"
  if [ "$KQ" = DAT ]; then ghi 0 "" ""
  else ghi 1 "(b) ${TEN[$i]}/dong-trich" "can rc=0 x$LAN, do rc0=$DEM_0 rc141=$DEM_141 khac=$DEM_KHAC"; fi

  # (d) duong chay that: dong trich phai chay that, tren dau vao 20000 dong, va ghi gia tri dung
  chay_that "$i"
  if [ "$DO_RC" -eq 0 ] && [ "$DO_GT" = "1.7.7" ]; then ghi 0 "" ""
  else ghi 1 "(d) ${TEN[$i]}/duong-chay-that" "chay that rc=$DO_RC, dong chung minh ghi '$DO_GT' (mong rc=0 va '1.7.7')"; fi

  # (c) tu kiem: dua dong trich ve dang cu tren BAN SAO TAM; CHINH ham cham (b) phai cham no DO, dung ly do (141)
  mkdir -p "$TMP/mut-$i/ops" || khong_do "khong tao duoc $TMP/mut-$i"
  for f in "${TEP[@]}"; do cp -- "$GOC/$f" "$TMP/mut-$i/$f" || khong_do "khong chep duoc $GOC/$f"; done
  {
    head -n "$((TRICH_SO - 1))" "$GOC/${TEP[$i]}"
    printf '%s\n' "${CU[$i]}"
    tail -n "+$((TRICH_SO + 1))" "$GOC/${TEP[$i]}"
  } > "$TMP/mut-$i/${TEP[$i]}"
  trich "$TMP/mut-$i" "$i"
  [ "$TRICH_DONG" = "${CU[$i]}" ] || khong_do "dot bien ${TEN[$i]} khong dua duoc dong ve dang cu"
  cham_b "$TRICH_DONG" "${VAO[$i]}"
  if [ "$KQ" = DO ] && [ "$DEM_141" -eq "$LAN" ]; then ghi 0 "" ""
  else ghi 1 "(c) ${TEN[$i]}/dot-bien-pipeline" "(b) phai cham DO bang rc=141 x$LAN, cham ra $KQ, do rc0=$DEM_0 rc141=$DEM_141 khac=$DEM_KHAC"; fi
done

# (e) B1: khop dau + 20000 doi so dem KHONG noi fallback; khong khop (ke ca tien to la khop-chuoi-con) van noi mac dinh
b1 khop-dau-tuong-minh explicit explicit GIA_REF_STATE=explicit NEO_TEP=explicit "${PAD[@]}"
b1 khong-khop-mac-dinh "$TMP/b1/refstate" "$TMP/b1/neo_auto" "${PAD[@]}"
b1 chuoi-con-khong-phai-dau "$TMP/b1/refstate" "$TMP/b1/neo_auto" XGIA_REF_STATE=z NEO_TEP_X=z "${PAD[@]}"

# Ca CO MAT khac ca co DO: so phep da ghi phai bang so phep khai bao (vong lap khong duoc nuot ca nao).
MONG=$(( ${#TEN[@]} * (${#DV_TEN[@]} + 4) + 3 ))
[ "$TONG" -eq "$MONG" ] || khong_do "ghi $TONG phep, khai bao $MONG"

if [ "$DAT" -eq "$TONG" ]; then
  echo "do_sigpipe: $DAT/$TONG DAT ($DK)"
  exit 0
fi
echo "do_sigpipe: $DAT/$TONG — CO PHEP DO ĐỎ ($DK)"
exit 1
