#!/usr/bin/env bash
# ops/do_sigpipe.sh [--lan N] [--goc THU_MUC] — phep do phan chung cho #675: khong con pipeline
# "nguoi doc thoat som" (`| head -1`) duoi `set -e` + `pipefail` trong 3 script ops + B1 cua W5.
#
# CO CHE: `printf '%s\n' "$X" | head -1` — neu head thoat truoc lan ghi sau, printf an SIGPIPE, pipefail
# day 141 len, `set -e` giet script khong in gi. Dau vao 20000 dong: tat dinh rc=141.
#
# KIEN TRUC (r2 g3): KHONG chay ban TRICH. Moi phep do chay CHINH tep (khong cat, khong trich van ban roi
# chay ban trich) trong fixture offline va doc DAU VET O DIEM SU DUNG:
#   (d) W1: lenh cai da GOI + probe thay PATH/env moi · W2: kiem ban + stdout + GITHUB_PATH · W3: dong
#       `cong-cu.txt` + ket luan. Chay LAN lan; moi lan phai rc=0 VA dau vet dung (rc va dau vet la hai chot rieng).
#   (c) tu kiem — dua dong ve dang pipeline cu tren BAN SAO TAM roi goi CHINH `cham_diem` ay: no PHAI ghi DO
#       vi rc=141. Chi MOT duong quyet dinh cap/khuoc diem (`cham_diem`, `cham_b1`); (c) khong co nhanh cham rieng.
#   (e) B1 — nap CHINH W5 (`source`, khong sed) duoi DEBUG trap; tai moi ca `lam ...` cua W5 doc `declare -f lam`
#       THAT (ham dang song, ke ca dinh nghia lai/ham chet), chay `lam` + 20000 doi so voi `env` la recorder.
#   (a) tuong duong BIEU THUC — dong trich `^BIEN=` chay tren tap dau vao ne (khong noi gi ve duong chay; (d) noi).
# Dung cu thieu / fixture hong / producer loi hoac ngan -> rc=2 KHONG DO DUOC; khong bao gio xanh im lang.
# --goc: thu muc goc chua ops/{cai_cong_cu,cai_actionlint,dung_goi_review,don_ref_chot_test}.sh + .github/workflows/ops-don-ref.yml.
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
for f in "${TEP[@]}" "$W5" .github/workflows/ops-don-ref.yml; do [ -f "$GOC/$f" ] || khong_do "thieu tep $GOC/$f"; done
for t in git tar awk od find xargs comm sort wc python3; do command -v "$t" >/dev/null 2>&1 || khong_do "thieu cong cu $t"; done
if command -v sha256sum >/dev/null 2>&1; then SHACMD=(sha256sum)
elif command -v shasum >/dev/null 2>&1; then SHACMD=(shasum -a 256)
else khong_do "thieu sha256sum/shasum"; fi

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

# (a) Dang cu chay `set -u` (khong pipefail) de doi chung TAT DINH.
chay_gia_tri() {  # chay_gia_tri CHE_DO DONG VAO RA DAU_VAO -> in [gia tri]
  local ma="set -$1; $3=\$1; $2; printf '[%s]' \"\${$4}\""
  bash -c "$ma" _ "$5"
}

# ── (d) fixture offline. Producer (awk) dung MOT lan o day va bi kiem rc + so dong (G3): loi/ngan => KHONG DO DUOC.
GIA="$TMP/gia"; PY="$TMP/py"; mkdir -p "$TMP/goi"
cat > "$GIA" <<EOF
#!/bin/sh
printf '1.7.7\r\n'; awk 'BEGIN{for(i=1;i<=$DONG_LON;i++)print i}'
EOF
cat > "$PY" <<EOF
#!/bin/sh
case "\$2" in
  cai-lenh) printf '%s\r\n' 'printf "%s\n" cai >> "\$SENT_TEP"; printf "%s\n" "\$FIX_DICH"' FIX_X=ok
            awk 'BEGIN{for(i=1;i<=$DONG_LON;i++)printf "%d\r\n",i}' ;;
  kiem-tra) printf 'probe %s %s\n' "\${PATH%%:*}" "\$FIX_X" >> "\$SENT_TEP" ;;
esac
EOF
kiem_nguon() {  # kiem_nguon SO_DONG CMD... : producer phai rc=0 va dung SO_DONG dong (khong nuot loi bang process substitution)
  local mong="$1" out n; shift
  out="$("$@")" || khong_do "producer fixture that bai: $*"
  n="$(printf '%s\n' "$out" | wc -l)"
  [ "$n" -eq "$mong" ] || khong_do "producer fixture ra $n dong, can $mong: $*"
}
chmod +x "$GIA" "$PY"
kiem_nguon "$((DONG_LON + 1))" "$GIA"
kiem_nguon "$((DONG_LON + 2))" "$PY" x cai-lenh
cp -- "$GIA" "$TMP/goi/actionlint"
tar -czf "$TMP/goi.tar.gz" -C "$TMP/goi" actionlint || khong_do "khong dung duoc goi gia (tar)"
SHA="$("${SHACMD[@]}" < "$TMP/goi.tar.gz")" || khong_do "khong bam duoc goi gia"
SHA="${SHA%% *}"

DO_RC=0; DO_GT=""; MONG_GT=""
chay_diem() {  # chay_diem I GOC K -> DO_RC, DO_GT (dau vet o diem su dung), MONG_GT: chay CHINH tep, khong cat
  local i="$1" w="$TMP/d-$1-$3" rc=0 a c
  rm -rf -- "$w"; mkdir -p "$w/ops" "$w/bin" "$w/dich" || khong_do "khong dung duoc fixture $w"
  cp -- "$2/${TEP[$i]}" "$w/${TEP[$i]}" || khong_do "khong chep duoc $2/${TEP[$i]}"
  for a in curl wget ssh; do printf '#!/bin/sh\n>> "%s/mang"\nexit 22\n' "$w" > "$w/bin/$a"; chmod +x "$w/bin/$a"; done
  local E=(env -i HOME="$w" TMPDIR="$w" LC_ALL=C PATH="$w/bin:$PATH" GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1)
  case "$i" in
    0) cp -- "$PY" "$w/bin/python"
       E+=(SENT_TEP="$w/sent" FIX_DICH="$w/dich")
       "${E[@]}" bash "$w/${TEP[0]}" actionlint >/dev/null 2>&1 || rc=$?
       MONG_GT=$'cai\nprobe '"$w/dich ok"; DO_GT="(khong ghi)"; if [ -f "$w/sent" ]; then DO_GT="$(<"$w/sent")"; fi ;;
    1) E+=(AL_VER=1.7.7 AL_NEN=Linux AL_GOI="$TMP/goi.tar.gz" AL_SHA256="$SHA" AL_DICH="$w/al" GITHUB_PATH="$w/ghp")
       "${E[@]}" bash "$w/${TEP[1]}" >"$w/out" 2>&1 || rc=$?
       MONG_GT="$w/al|$w/al"; DO_GT="(khong ghi)"; if [ -f "$w/ghp" ]; then DO_GT="$(<"$w/out")|$(<"$w/ghp")"; fi ;;
    *) # W3 goi installer: BO CAI GIA (chep binary gia) de diem W3 do DOC LAP voi W2.
       printf '%s\n' "mkdir -p \"\$AL_DICH\" && cp \"$GIA\" \"\$AL_DICH/actionlint\"" > "$w/ops/cai_actionlint.sh"
       printf '#!/bin/sh\nprintf "ShellCheck - shell script analysis tool\\nversion: 0.9.0\\n"\n' > "$w/bin/shellcheck"; chmod +x "$w/bin/shellcheck"
       ( cd "$w" && git init -q && git -c commit.gpgsign=false -c user.name=t -c user.email=t@t commit -q --allow-empty -m t \
           && git remote add origin "$w" ) || khong_do "khong dung duoc kho git gia $w"
       "${E[@]}" bash "$w/${TEP[2]}" "$w/r" "$(git -C "$w" rev-parse HEAD)" "$w" >"$w/out" 2>&1 || rc=$?
       MONG_GT="actionlint|1.7.7|GOI DU DE TAI DO: 1/1/1 ref, 0 lech"; DO_GT="(khong ghi)"
       if [ -f "$w/r/cong-cu.txt" ]; then
         IFS=$'\t' read -r a _ c < "$w/r/cong-cu.txt" || true; DO_GT="$a|$c|$(tail -n 1 "$w/out")"
       fi ;;
  esac
  if [ -e "$w/mang" ]; then khong_do "fixture $w cham mang (curl/wget/ssh gia bi goi)"; fi
  DO_RC=$rc
}

# ── Ghi diem. Che do CON (CON=1): ghi vao CON_* de (c) hoi "cham co ghi DO khong", KHONG cong vao bo dem cha.
TONG=0; DAT=0; CON=0; CON_DO=0; CON_LY=""
ghi() {  # ghi <0|1> nhan chi-tiet
  if [ "$CON" -eq 1 ]; then
    if [ "$1" -ne 0 ]; then CON_DO=$((CON_DO + 1)); CON_LY+="$2 $3;"; fi
    return 0
  fi
  TONG=$((TONG + 1))
  if [ "$1" -eq 0 ]; then DAT=$((DAT + 1)); else printf '  ĐỎ  %s  %s\n' "$2" "$3"; fi
}
tu_kiem() {  # tu_kiem NHAN MAU CMD... : (c) chay CHINH ham cham CMD tren ban sao dot bien; no PHAI ghi DO, ly do chua MAU
  local nhan="$1" mau="$2"; shift 2
  CON=1; CON_DO=0; CON_LY=""
  "$@"
  CON=0
  if [ "$CON_DO" -ge 1 ] && [[ "$CON_LY" == *"$mau"* ]]; then ghi 0 "" ""
  else ghi 1 "(c) $nhan" "cham phai ghi DO co '$mau'; ghi $CON_DO DO, ly do='$CON_LY'"; fi
}

# MOT duong quyet dinh cap/khuoc diem (d). Ca head lan ban sao dot bien (c) deu di qua day.
cham_diem() {  # cham_diem I GOC
  local i="$1" k n0=0 n141=0 nk=0 sai=0 lan_sai=""
  for ((k = 0; k < LAN; k++)); do
    chay_diem "$i" "$2" "$k"
    case "$DO_RC" in 0) n0=$((n0 + 1)) ;; 141) n141=$((n141 + 1)) ;; *) nk=$((nk + 1)) ;; esac
    if [ "$DO_RC" -eq 0 ] && [ "$DO_GT" != "$MONG_GT" ]; then sai=$((sai + 1)); lan_sai="$DO_GT"; fi
  done
  if [ "$n0" -eq "$LAN" ] && [ "$sai" -eq 0 ]; then ghi 0 "" ""
  else ghi 1 "(d) ${TEN[$i]}/chay-toan-bo" "rc0=$n0 rc141=$n141 khac=$nk dau-vet-sai=$sai (mong '$MONG_GT', thay '$lan_sai')"; fi
}

# ── (e) B1. Driver nap CHINH W5 (`source`); DEBUG trap (-T) bat MOI ca `lam ...` cua W5.
# shellcheck disable=SC2016  # driver la van ban bash, chu y khong khai trien o day
B1_DRV='set -uT; OUT=$1; W5=$2; N=$3; LAN=$4; H0=""; PAD=()
for ((k = 1; k <= N; k++)); do PAD+=("P$k=x"); done
[ "${#PAD[@]}" -eq "$N" ] || exit 97
lay() {
  local v k nr nn
  for v in khop khong chuoi; do for ((k = 0; k < LAN; k++)); do
    rm -f "$OUT.env"; env() { printf "%s\n" "$@" > "$OUT.env"; }
    case "$v" in
      khop)  lam t 0 xoa-nhanh r1 sha thu GIA_REF_STATE=explicit NEO_TEP=explicit "${PAD[@]}" ;;
      khong) lam t 0 xoa-nhanh r1 sha thu "${PAD[@]}" ;;
      chuoi) lam t 0 xoa-nhanh r1 sha thu XGIA_REF_STATE=z NEO_TEP_X=z "${PAD[@]}" ;;
    esac >/dev/null 2>&1
    unset -f env
    nr=$(grep -c "^GIA_REF_STATE=" "$OUT.env" || true); nn=$(grep -c "^NEO_TEP=" "$OUT.env" || true)
    printf "%s\t%s\t%s\t%s\t%s\n" "$v" "$nr" "$nn" "$(grep -m1 "^GIA_REF_STATE=" "$OUT.env" || true)" "$(grep -m1 "^NEO_TEP=" "$OUT.env" || true)" >> "$OUT"
  done; done
}
trampa() { case "$BASH_COMMAND" in "lam "*)
  local h; h="$(declare -f lam | cksum)"
  if [ -z "$H0" ]; then H0="$h"; lay; elif [ "$h" != "$H0" ]; then echo redef >> "$OUT"; fi ;; esac; return 0; }
trap() { case "$*" in *DEBUG*) ;; *) builtin trap "$@" ;; esac; }  # W5 khong duoc go/doi trap DEBUG cua driver
builtin trap trampa DEBUG
. "$W5"'
V_TAG=(khop khong chuoi)
V_TEN=(khop-dau-tuong-minh khong-khop-mac-dinh chuoi-con-khong-phai-dau)
cham_b1() {  # cham_b1 GOC : nap CHINH W5 duoi driver; moi bien the phai cho `env` DUNG 1 dong moi bien, dung gia tri
  local vi tag nr nn r n bad dem
  rm -f -- "$TMP/b1.out"
  bash -c "$B1_DRV" _ "$TMP/b1.out" "$1/$W5" "$DONG_LON" "$LAN" >/dev/null 2>"$TMP/b1.err" || true
  [ -s "$TMP/b1.out" ] || khong_do "W5 khong toi ca lam() nao ($(tail -n 2 "$TMP/b1.err" | tr '\n' ' '))"
  for vi in "${!V_TAG[@]}"; do
    bad=0; dem=0
    while IFS=$'\t' read -r tag nr nn r n; do
      [ "$tag" = "${V_TAG[$vi]}" ] || continue
      dem=$((dem + 1))
      if [ "$nr" != 1 ] || [ "$nn" != 1 ]; then bad=$((bad + 1))
      elif [ "$tag" = khop ]; then
        if [ "$r" != GIA_REF_STATE=explicit ] || [ "$n" != NEO_TEP=explicit ]; then bad=$((bad + 1)); fi
      elif [[ "$r" != GIA_REF_STATE=*/refstate ]] || [[ "$n" != NEO_TEP=*/neo_auto ]]; then bad=$((bad + 1)); fi
    done < "$TMP/b1.out"
    if [ "$dem" -eq "$LAN" ] && [ "$bad" -eq 0 ]; then ghi 0 "" ""
    else ghi 1 "(e) B1/${V_TEN[$vi]}" "mong $LAN lan dung, thay $dem lan, sai $bad (moi bien DUNG 1 dong)"; fi
  done
  if grep -q '^redef' "$TMP/b1.out"; then ghi 1 "(e) B1/lam-bi-dinh-nghia-lai" "declare -f lam doi giua cac ca cua W5"; else ghi 0 "" ""; fi
}

DK="bash $BASH_VERSION, $(nproc 2>/dev/null || echo '?') loi, $LAN lan, $DONG_LON dong"
echo "do_sigpipe: goc=$GOC · $DK"
for i in "${!TEN[@]}"; do
  trich "$GOC" "$i"
  dong="$TRICH_DONG"
  printf '%s  %s:%s\n    %s\n' "${TEN[$i]}" "${TEP[$i]}" "$TRICH_SO" "$dong"

  # (a) tuong duong BIEU THUC tren tap dau vao
  for j in "${!DV_TEN[@]}"; do
    rc=0; moi="$(chay_gia_tri euo\ pipefail "$dong" "${VAO[$i]}" "${RA[$i]}" "${DV_GT[$j]}")" || rc=$?
    rc2=0; cu="$(chay_gia_tri u "${CU[$i]}" "${VAO[$i]}" "${RA[$i]}" "${DV_GT[$j]}")" || rc2=$?
    if [ "$rc" -eq 0 ] && [ "$rc2" -eq 0 ] && [ "$moi" = "$cu" ]; then ghi 0 "" ""
    else ghi 1 "(a) ${TEN[$i]}/${DV_TEN[$j]}" "trich rc=$rc '$moi' · cu rc=$rc2 '$cu'"; fi
  done

  # (d) chay CHINH tep, doc dau vet o diem su dung
  cham_diem "$i" "$GOC"

  # (c) tu kiem: dua dong ve dang cu tren BAN SAO TAM; CHINH `cham_diem` phai ghi DO vi 141 moi lan
  mkdir -p "$TMP/mut-$i/ops" || khong_do "khong tao duoc $TMP/mut-$i"
  cp -- "$GOC/${TEP[$i]}" "$TMP/mut-$i/${TEP[$i]}" || khong_do "khong chep duoc $GOC/${TEP[$i]}"
  {
    head -n "$((TRICH_SO - 1))" "$GOC/${TEP[$i]}"
    printf '%s\n' "${CU[$i]}"
    tail -n "+$((TRICH_SO + 1))" "$GOC/${TEP[$i]}"
  } > "$TMP/mut-$i/${TEP[$i]}"
  trich "$TMP/mut-$i" "$i"
  [ "$TRICH_DONG" = "${CU[$i]}" ] || khong_do "dot bien ${TEN[$i]} khong dua duoc dong ve dang cu"
  tu_kiem "${TEN[$i]}/dot-bien-pipeline" "rc141=$LAN " cham_diem "$i" "$TMP/mut-$i"
done

# (e) B1 tren W5 that; (c) ban sao W5 dua 2 phep do ve `printf | grep -q` — CHINH `cham_b1` phai ghi DO o bien the khop-dau
cham_b1 "$GOC"
mkdir -p "$TMP/mut-b1/ops" "$TMP/mut-b1/.github/workflows"
cp -- "$GOC/.github/workflows/ops-don-ref.yml" "$TMP/mut-b1/.github/workflows/"
src="$(<"$GOC/$W5")"
for m in ref:GIA_REF_STATE neo:NEO_TEP; do  # dua tung phep do ve dang cu: `printf | grep -q` (SIGPIPE -> `!` dao nhanh)
  src="${src/"  if [ \"\$mac_${m%%:*}\" -eq 1 ]; then"/"  if ! printf '%s\\n' \"\$@\" | grep -q '^${m#*:}='; then"}"
done
printf '%s\n' "$src" > "$TMP/mut-b1/$W5"
# Ban sao PHAI mang dang cu that o CA HAI phep do (cay nen co san; cay nua-vao thi thay not phan con lai).
if ! grep -qF "| grep -q '^GIA_REF_STATE='" "$TMP/mut-b1/$W5" || ! grep -qF "| grep -q '^NEO_TEP='" "$TMP/mut-b1/$W5"; then
  khong_do "$W5: dot bien B1 khong dua duoc CA HAI phep do ve dang cu"
fi
tu_kiem "B1/dot-bien-printf-grep" "khop-dau-tuong-minh" cham_b1 "$TMP/mut-b1"

# Ca CO MAT khac ca co DO: so phep da ghi phai bang so phep khai bao (vong lap khong duoc nuot ca nao).
MONG=$(( ${#TEN[@]} * (${#DV_TEN[@]} + 2) + 5 ))
[ "$TONG" -eq "$MONG" ] || khong_do "ghi $TONG phep, khai bao $MONG"

if [ "$DAT" -eq "$TONG" ]; then
  echo "do_sigpipe: $DAT/$TONG DAT ($DK)"
  exit 0
fi
echo "do_sigpipe: $DAT/$TONG — CO PHEP DO ĐỎ ($DK)"
exit 1
