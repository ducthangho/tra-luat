#!/usr/bin/env bash
# Ma tran phan chung cho buoc don du luong daemon cua playwright-browser SKILL.md (packet #1389).
# Chay TREN BYTE CUA SKILL: trich NOI DUNG giua cap dong danh dau (khong gom dong danh dau) trong khoi bash:
#   "  # --- du-luong-daemon: bat dau|het"              (Cleanup)
#   "  # --- du-luong-daemon-truoc-open: bat dau|het"   (Capture, truoc open)
# Moi cap phai xuat hien DUNG 2 lan (bash + PowerShell); lay lan thu nhat. Khong goi CLI, khong mang, khong trinh duyet.
# Dung: bash residue_matrix.sh <SKILL.md> <SCRATCH (thu muc rong, ngoai Git)>
set -euo pipefail
SKILL=$1; SCRATCH=$2
[ -f "$SKILL" ] && [ -d "$SCRATCH" ] && [ -z "$(ls -A "$SCRATCH")" ] || { echo "usage: SKILL.md + empty SCRATCH" >&2; exit 2; }
SCRATCH=$(cd "$SCRATCH" && pwd -P)
NONCE=tl-pw-0123456789ab; OTHER=tl-pw-ba9876543210; H=aaaaaaaaaaaaaaaa; H2=bbbbbbbbbbbbbbbb

extract() { # $1 = ten cap danh dau, $2 = tep ra. In noi dung giua cap THU NHAT, kiem du 2 cap va khong long nhau.
  awk -v B="  # --- $1: bat dau" -v E="  # --- $1: het" -v OUT="$2" '
    $0 == B { if (open) { bad = 1 } open = 1; nb++; next }
    $0 == E { if (!open) { bad = 1 } open = 0; ne++; next }
    open && nb == 1 { print > OUT }
    END { if (bad || open || nb != 2 || ne != 2) { printf "FAIL: cap danh dau %s sai (bat dau=%d het=%d)\n", B, nb, ne > "/dev/stderr"; exit 1 } }' "$SKILL"; }
extract du-luong-daemon "$SCRATCH/frag_cleanup.sh"
extract du-luong-daemon-truoc-open "$SCRATCH/frag_pre.sh"
grep -q 'mapfile -d' "$SCRATCH/frag_cleanup.sh" || { echo "FAIL: doan cleanup khong phai ban bash" >&2; exit 1; }
grep -q 'find "\$D"' "$SCRATCH/frag_pre.sh" || { echo "FAIL: doan truoc-open khong phai ban bash" >&2; exit 1; }
echo "SOURCE $(sha256sum < "$SKILL" | cut -c1-64) cleanup_frag $(sha256sum < "$SCRATCH/frag_cleanup.sh" | cut -c1-64) pre_frag $(sha256sum < "$SCRATCH/frag_pre.sh" | cut -c1-64)"

PASS=0; FAIL=0; CASE_DIR=
ok() { PASS=$((PASS+1)); echo "PASS $*"; }
ko() { FAIL=$((FAIL+1)); echo "FAIL $*"; [ -f "$CASE_DIR/out" ] && sed 's/^/    /' "$CASE_DIR/out"; return 0; }
OWN() { echo "$CASE_DIR/cache/ms-playwright/daemon/$H/$NONCE.err"; }
new_case() { CASE_DIR="$SCRATCH/case-$1"; local d="$CASE_DIR/cache/ms-playwright/daemon"
  mkdir -p "$d/$H" "$d/$H2" "$CASE_DIR/run" "$CASE_DIR/home" "$CASE_DIR/bin"
  printf 'own stderr %s\n' "$1" > "$d/$H/$NONCE.err"
  # moi cua phien khac va mot .err cu: KHONG BAO GIO duoc dung toi
  printf 'other\n' > "$d/$H/$OTHER.err"; printf '{}\n' > "$d/$H/$OTHER.session"
  printf 'legacy\n' > "$d/$H2/tl-pw-111111111111.err"; }
# Anh chup tung tep KHONG mang nonce: duong dan, loai, kich thuoc, mtime, sha256 noi dung.
decoys() { (cd "$CASE_DIR" && find cache -path "*$NONCE*" -prune -o -type f -printf '%p\t%s\t%T@\n' | LC_ALL=C sort |
  while IFS=$'\t' read -r p s t; do printf '%s\t%s\t%s\t%s\n' "$p" "$s" "$t" "$(sha256sum < "$p" | cut -c1-64)"; done | sha256sum | cut -c1-64); }
no_new_outputs() { [ ! -e "$CASE_DIR/run/11-daemon.err" ] && [ ! -e "$CASE_DIR/run/11-daemon-path.txt" ]; }
run_frag() { # $1 = tep doan; con lai: bien moi truong them (KEY=VAL)
  local body=$1; shift
  ( cd "$CASE_DIR/home" && env -i HOME="$CASE_DIR/home" PATH="$CASE_DIR/bin:/usr/bin:/bin" XDG_CACHE_HOME="$CASE_DIR/cache" \
    TL_PW_SESSION=$NONCE TL_PW_RUN="$CASE_DIR/run" "$@" bash -c "( set -u
$(cat "$body")
echo RESIDUE_OK )" ) > "$CASE_DIR/out" 2>&1 && echo 0 || echo $?; }
run_pre() { local body=$1; shift
  ( cd "$CASE_DIR/home" && env -i HOME="$CASE_DIR/home" PATH="$CASE_DIR/bin:/usr/bin:/bin" XDG_CACHE_HOME="$CASE_DIR/cache" \
    TL_PW_SESSION=$NONCE "$@" bash -c "( set -Eeuo pipefail; trap 'echo \"STOP: \$BASH_COMMAND\" >&2' ERR
$(cat "$body")
echo RESIDUE_OK )" ) > "$CASE_DIR/out" 2>&1 && echo 0 || echo $?; }
is_ok() { [ "$1" = 0 ] && grep -qx RESIDUE_OK "$CASE_DIR/out"; }
is_stop() { [ "$1" != 0 ] && ! grep -qx RESIDUE_OK "$CASE_DIR/out" && grep -q STOP "$CASE_DIR/out"; }
# expect_stop NAME RC D0 [tep phai con, nguyen sha:...]
expect_stop() { local n=$1 rc=$2 d0=$3 bad=; shift 3
  is_stop "$rc" || bad="khong dung dung cach"
  [ "$d0" = "$(decoys)" ] || bad="$bad; moi bi doi"
  for spec in "$@"; do local p=${spec%%=*} h=${spec#*=}; [ -e "$p" ] && [ "$(sha256sum < "$p" | cut -c1-64)" = "$h" ] || bad="$bad; $p doi/mat"; done
  if [ -z "$bad" ]; then ok "$n rc=$rc"; else ko "$n rc=$rc ($bad)"; fi; }
sha() { sha256sum < "$1" | cut -c1-64; }
F=$SCRATCH/frag_cleanup.sh; P=$SCRATCH/frag_pre.sh

# ---- duong dung
for c in P1 P2; do new_case $c; [ $c = P2 ] && : > "$(OWN)"; d0=$(decoys); own=$(sha "$(OWN)"); rc=$(run_frag "$F")
  if is_ok "$rc" && [ "$d0" = "$(decoys)" ] && [ ! -e "$(OWN)" ] && [ "$(sha "$CASE_DIR/run/11-daemon.err")" = "$own" ] &&
     [ "$(cat "$CASE_DIR/run/11-daemon-path.txt")" = "$(OWN)" ]; then ok "$c-positive (goc da xoa, ban sao trung byte, duong dan dung, moi nguyen)"
  else ko "$c-positive rc=$rc"; fi; done
# ---- phan chung (moi ca: STOP, moi nguyen noi dung/mtime, tep mang nonce con nguyen, KHONG tao output 11)
new_case N1; rm "$(OWN)"; d0=$(decoys); rc=$(run_frag "$F"); expect_stop N1-zero-match "$rc" "$d0"; no_new_outputs || ko "N1 output 11"
new_case N2; printf 'dup\n' > "$CASE_DIR/cache/ms-playwright/daemon/$H2/$NONCE.err"; d0=$(decoys); rc=$(run_frag "$F")
expect_stop N2-two-hash-dirs "$rc" "$d0" "$(OWN)=$(sha "$(OWN)")" "$CASE_DIR/cache/ms-playwright/daemon/$H2/$NONCE.err=$(sha "$CASE_DIR/cache/ms-playwright/daemon/$H2/$NONCE.err")"; no_new_outputs || ko "N2 output 11"
new_case N3; S=$CASE_DIR/cache/ms-playwright/daemon/$H/$NONCE.session; printf '{}\n' > "$S"; d0=$(decoys); rc=$(run_frag "$F")
expect_stop N3-session-left "$rc" "$d0" "$(OWN)=$(sha "$(OWN)")" "$S=$(sha "$S")"; no_new_outputs || ko "N3 output 11"
new_case N4; U=$CASE_DIR/cache/ms-playwright/daemon/$H/ud-$NONCE-chromium; mkdir "$U"; printf 'x\n' > "$U/Prefs"; d0=$(decoys); rc=$(run_frag "$F")
expect_stop N4-userdata-left "$rc" "$d0" "$(OWN)=$(sha "$(OWN)")" "$U/Prefs=$(sha "$U/Prefs")"; no_new_outputs || ko "N4 output 11"
new_case N5; rm "$(OWN)"; ln -s "$CASE_DIR/cache/ms-playwright/daemon/$H/$OTHER.err" "$(OWN)"; d0=$(decoys); rc=$(run_frag "$F")
expect_stop N5-err-symlink "$rc" "$d0"; [ -L "$(OWN)" ] && no_new_outputs || ko "N5 link mat/output 11"
new_case N6; mkdir -p "$CASE_DIR/elsewhere"; mv "$(OWN)" "$CASE_DIR/elsewhere/"; ln -s "$CASE_DIR/elsewhere" "$CASE_DIR/cache/ms-playwright/daemon/cccccccccccccccc"; d0=$(decoys)
rc=$(run_frag "$F"); expect_stop N6-hashdir-symlink "$rc" "$d0" "$CASE_DIR/elsewhere/$NONCE.err=$(sha "$CASE_DIR/elsewhere/$NONCE.err")"; no_new_outputs || ko "N6 output 11"
new_case N7; mv "$CASE_DIR/cache/ms-playwright/daemon" "$CASE_DIR/real-daemon"; ln -s "$CASE_DIR/real-daemon" "$CASE_DIR/cache/ms-playwright/daemon"; d0=$(decoys)
rc=$(run_frag "$F"); expect_stop N7-daemon-symlink "$rc" "$d0" "$CASE_DIR/real-daemon/$H/$NONCE.err=$(sha "$CASE_DIR/real-daemon/$H/$NONCE.err")"; no_new_outputs || ko "N7 output 11"
for v in err path; do new_case N8-$v; [ $v = err ] && o=11-daemon.err || o=11-daemon-path.txt; printf 'old\n' > "$CASE_DIR/run/$o"; d0=$(decoys); rc=$(run_frag "$F")
  expect_stop N8-stale-$o "$rc" "$d0" "$(OWN)=$(sha "$(OWN)")" "$CASE_DIR/run/$o=$(printf 'old\n' | sha256sum | cut -c1-64)"; done
new_case N9; mkdir "$CASE_DIR/cache/ms-playwright/daemon/not-a-hash"; mv "$(OWN)" "$CASE_DIR/cache/ms-playwright/daemon/not-a-hash/"; d0=$(decoys)
rc=$(run_frag "$F"); expect_stop N9-bad-hash-name "$rc" "$d0" "$CASE_DIR/cache/ms-playwright/daemon/not-a-hash/$NONCE.err=$(sha "$CASE_DIR/cache/ms-playwright/daemon/not-a-hash/$NONCE.err")"; no_new_outputs || ko "N9 output 11"
new_case N10; d0=$(decoys); rc=$(run_frag "$F" PWTEST_DAEMON_SESSION_DIR="$CASE_DIR/x"); expect_stop N10-pwtest-hook "$rc" "$d0" "$(OWN)=$(sha "$(OWN)")"; no_new_outputs || ko "N10 output 11"
new_case N11; rm "$(OWN)"; mkdir "$(OWN)"; d0=$(decoys); rc=$(run_frag "$F"); expect_stop N11-err-is-dir "$rc" "$d0"; [ -d "$(OWN)" ] && no_new_outputs || ko "N11"
new_case N12; rm -r "$CASE_DIR/cache/ms-playwright/daemon"; d0=$(decoys); rc=$(run_frag "$F"); expect_stop N12-no-registry "$rc" "$d0"; no_new_outputs || ko "N12 output 11"
new_case N14; W=$CASE_DIR/cache/ms-playwright/daemon/$H/${NONCE}Xerr; mv "$(OWN)" "$W"; d0=$(decoys); rc=$(run_frag "$F")
expect_stop N14-wrong-suffix "$rc" "$d0" "$W=$(sha "$W")"; no_new_outputs || ko "N14 output 11"
# N15: phep quet tra MOT muc hop le roi loi (gia lap thu muc khong liet ke duoc; may nay chay root nen khong dung chmod duoc)
fake_find() { cat > "$CASE_DIR/bin/find" <<EOF
#!/bin/bash
printf '%s\0' "$(OWN)"; echo "find: '\$1/dddddddddddddddd': Permission denied" >&2; exit 1
EOF
  chmod +x "$CASE_DIR/bin/find"; }
new_case N15; fake_find; d0=$(decoys); rc=$(run_frag "$F"); expect_stop N15-scan-error "$rc" "$d0" "$(OWN)=$(sha "$(OWN)")"; no_new_outputs || ko "N15 output 11"
new_case N16; NL="$CASE_DIR/cache/ms-playwright/daemon/$H2/x
$NONCE.err"; printf 'nl\n' > "$NL"; d0=$(decoys); rc=$(run_frag "$F")
expect_stop N16-newline-name "$rc" "$d0" "$(OWN)=$(sha "$(OWN)")" "$NL=$(sha "$NL")"; no_new_outputs || ko "N16 output 11"
new_case N17; mkdir -p "$CASE_DIR/home/rel"; cp -a "$CASE_DIR/cache" "$CASE_DIR/home/rel/"; R17=$CASE_DIR/home/rel/cache/ms-playwright/daemon/$H/$NONCE.err
d0=$(decoys); rc=$(run_frag "$F" XDG_CACHE_HOME=rel/cache); [ -e "$R17" ] || ko "N17 tep trong cache tuong doi mat"; expect_stop N17-relative-cache "$rc" "$d0" "$(OWN)=$(sha "$(OWN)")"; no_new_outputs || ko "N17 output 11"
# ---- kiem truoc open (chay duoi set -Eeuo pipefail nhu khoi Capture)
new_case C1; rm "$(OWN)"; d0=$(decoys); rc=$(run_pre "$P"); { is_ok "$rc" && [ "$d0" = "$(decoys)" ]; } && ok "C1-pre-clean rc=$rc" || ko "C1-pre-clean rc=$rc"
new_case C2; d0=$(decoys); rc=$(run_pre "$P"); expect_stop C2-pre-nonce-present "$rc" "$d0" "$(OWN)=$(sha "$(OWN)")"
new_case C3; rm -r "$CASE_DIR/cache/ms-playwright"; rc=$(run_pre "$P"); is_ok "$rc" && ok "C3-pre-no-registry rc=$rc" || ko "C3-pre-no-registry rc=$rc"
# C4: cache tuong doi, va sổ CLI (nhin tu work) da co .err cung nonce: phai dung truoc open
new_case C4; mkdir -p "$CASE_DIR/home/rel"; mv "$CASE_DIR/cache" "$CASE_DIR/home/rel/"; rc=$(run_pre "$P" XDG_CACHE_HOME=rel/cache)
is_stop "$rc" && ok "C4-pre-relative-cache rc=$rc" || ko "C4-pre-relative-cache rc=$rc"
new_case C5; rm "$(OWN)"; rc=$(run_pre "$P" PWTEST_DAEMON_SESSION_DIR="$CASE_DIR/x"); is_stop "$rc" && ok "C5-pre-pwtest-hook rc=$rc" || ko "C5-pre-pwtest-hook rc=$rc"
new_case C6; mv "$(OWN)" "$CASE_DIR/cache/ms-playwright/daemon/$NONCE.err"; rc=$(run_pre "$P")
is_ok "$rc" && ok "C6-pre-depth1-ignored (chi do do sau 2, nhu CLI) rc=$rc" || ko "C6-pre-depth1-ignored rc=$rc"

# ---- dot bien: moi ban vá yeu di phai lam ca dich LOT (RESIDUE_OK)
mut() { # name target file sed_expr
  local name=$1 target=$2 src=$3 expr=$4 m="$SCRATCH/mut-$1.sh" rc
  sed -E "$expr" "$src" > "$m"
  cmp -s "$m" "$src" && { ko "MUT $name: sed khong doi gi"; return; }
  new_case "M-$name"; local extra=() runner=run_frag
  case "$target" in
    N2) printf 'dup\n' > "$CASE_DIR/cache/ms-playwright/daemon/$H2/$NONCE.err";;
    N3) printf '{}\n' > "$CASE_DIR/cache/ms-playwright/daemon/$H/$NONCE.session";;
    N5) rm "$(OWN)"; ln -s "$CASE_DIR/cache/ms-playwright/daemon/$H/$OTHER.err" "$(OWN)";;
    N7) mv "$CASE_DIR/cache/ms-playwright/daemon" "$CASE_DIR/real-daemon"; ln -s "$CASE_DIR/real-daemon" "$CASE_DIR/cache/ms-playwright/daemon";;
    N8) printf 'old\n' > "$CASE_DIR/run/11-daemon.err";;
    N9) mkdir "$CASE_DIR/cache/ms-playwright/daemon/not-a-hash"; mv "$(OWN)" "$CASE_DIR/cache/ms-playwright/daemon/not-a-hash/";;
    N10) extra=(PWTEST_DAEMON_SESSION_DIR=x);;
    N14) mv "$(OWN)" "$CASE_DIR/cache/ms-playwright/daemon/$H/${NONCE}Xerr";;
    N15) fake_find;;
    N17) mkdir -p "$CASE_DIR/home/rel"; cp -a "$CASE_DIR/cache" "$CASE_DIR/home/rel/"; extra=(XDG_CACHE_HOME=rel/cache);;
    C4) runner=run_pre; rm "$(OWN)"; mkdir -p "$CASE_DIR/home/rel"; mv "$CASE_DIR/cache" "$CASE_DIR/home/rel/"; extra=(XDG_CACHE_HOME=rel/cache);;
    C5) runner=run_pre; rm "$(OWN)"; extra=(PWTEST_DAEMON_SESSION_DIR=x);;
  esac
  rc=$($runner "$m" "${extra[@]}")
  if is_ok "$rc"; then ok "MUT $name -> $target lot (chot co rang)"; else ko "MUT $name -> $target van chan (chot khong do duoc)"; fi; }
mut exact-one N2 "$F" 's/\[ "\$\{#hit\[@\]\}" -eq 1 \]/[ "${#hit[@]}" -ge 1 ]/'
mut name-glob N3 "$F" 's/-name "\*\$TL_PW_SESSION\*"/-name "$TL_PW_SESSION.err"/'
mut no-symlink-check N5 "$F" 's/\[ -f "\$f" \] && \[ ! -L "\$f" \]/[ -e "$f" ]/'
mut daemon-symlink N7 "$F" 's/\[ -d "\$D" \] && \[ ! -L "\$D" \]/[ -d "$D" ]/; s/find "\$D" /find -L "$D" /'
mut stale-output N8 "$F" 's/\[ ! -e "\$TL_PW_RUN\/\$ten" \] && \[ ! -L "\$TL_PW_RUN\/\$ten" \]/true/'
mut hash-shape N9 "$F" 's/\^\[0-9a-f\]\{16\}\$/^[^\/]+$/'
mut pwtest-hook N10 "$F" 's/\[ -z "\$\{PWTEST_DAEMON_SESSION_DIR\+x\}" \]/true/'
mut dot-wildcard N14 "$F" 's/\[ "\$\{f##\*\/\}" = "\$TL_PW_SESSION\.err" \]/[[ "${f##*\/}" =~ ^"$TL_PW_SESSION".err$ ]]/'
mut no-scan-rc N15 "$F" 's/wait "\$!" \|\|/true ||/'
mut relative-cache N17 "$F" 's/case "\$D" in \/\*\) ;; \*\) echo/case "$D" in *) ;; \/*) echo/'
mut pre-relative C4 "$P" 's/case "\$D" in \/\*\) ;; \*\) false;; esac/true/'
mut pre-hook C5 "$P" 's/\[ -z "\$\{PWTEST_DAEMON_SESSION_DIR\+x\}" \];/true;/'

echo "TONG: $PASS dat / $((PASS+FAIL))"
[ "$FAIL" -eq 0 ]
