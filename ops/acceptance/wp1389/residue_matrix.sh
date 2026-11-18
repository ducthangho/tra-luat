#!/usr/bin/env bash
# Ma tran phan chung cho buoc don du luong daemon cua playwright-browser SKILL.md (packet #1389).
# Chay TREN BYTE CUA SKILL: trich doan giua hai dong danh dau trong khoi Cleanup bash, va hai dong kiem
# truoc `open` trong khoi Capture bash. Khong goi CLI, khong mang, khong trinh duyet; moi tep nam trong $SCRATCH.
# Dung: bash residue_matrix.sh <SKILL.md> <SCRATCH (thu muc rong, ngoai Git)>
set -euo pipefail
SKILL=$1; SCRATCH=$2
[ -f "$SKILL" ] && [ -d "$SCRATCH" ] && [ -z "$(ls -A "$SCRATCH")" ] || { echo "usage: SKILL.md + empty SCRATCH" >&2; exit 2; }
SCRATCH=$(cd "$SCRATCH" && pwd -P)
NONCE=tl-pw-0123456789ab; OTHER=tl-pw-ba9876543210; H=aaaaaaaaaaaaaaaa; H2=bbbbbbbbbbbbbbbb

frag_cleanup=$(awk '/^  # --- du-luong-daemon: bat dau$/{f=1} f{print} /^  # --- du-luong-daemon: het$/{f=0}' "$SKILL" |
  awk 'BEGIN{n=0} /^  # --- du-luong-daemon: bat dau$/{n++} n==1{print}')
n_markers=$(grep -c '^  # --- du-luong-daemon: bat dau$' "$SKILL" || true)
[ "$n_markers" -eq 2 ] || { echo "FAIL: can 2 cap danh dau (bash+ps), thay $n_markers" >&2; exit 1; }
frag_cleanup=$(printf '%s\n' "$frag_cleanup" | awk '/^  # --- du-luong-daemon: het$/{print; exit} {print}')
grep -q 'mapfile -t hit' <<<"$frag_cleanup" || { echo "FAIL: khong trich duoc doan bash" >&2; exit 1; }
frag_pre=$(grep -E '^  (D="\$\{XDG_CACHE_HOME:-\$HOME/\.cache\}/ms-playwright/daemon"   # |if \[ -e "\$D" \]; then pre=)' "$SKILL")
[ "$(printf '%s\n' "$frag_pre" | wc -l)" -eq 2 ] || { echo "FAIL: khong trich duoc 2 dong kiem truoc open" >&2; exit 1; }
printf '%s\n' "$frag_cleanup" > "$SCRATCH/frag_cleanup.sh"; printf '%s\n' "$frag_pre" > "$SCRATCH/frag_pre.sh"
echo "SOURCE $(sha256sum < "$SKILL" | cut -c1-64) cleanup_frag $(sha256sum < "$SCRATCH/frag_cleanup.sh" | cut -c1-64) pre_frag $(sha256sum < "$SCRATCH/frag_pre.sh" | cut -c1-64)"

PASS=0; FAIL=0; CASE_DIR=
new_case() { CASE_DIR="$SCRATCH/case-$1"; mkdir -p "$CASE_DIR/cache/ms-playwright/daemon/$H" "$CASE_DIR/run"
  printf 'own stderr %s\n' "$1" > "$CASE_DIR/cache/ms-playwright/daemon/$H/$NONCE.err"
  # mo coi cua phien khac va mot .err cu: KHONG BAO GIO duoc dung toi
  printf 'other\n' > "$CASE_DIR/cache/ms-playwright/daemon/$H/$OTHER.err"
  printf '{}\n' > "$CASE_DIR/cache/ms-playwright/daemon/$H/$OTHER.session"
  mkdir -p "$CASE_DIR/cache/ms-playwright/daemon/$H2"; printf 'legacy\n' > "$CASE_DIR/cache/ms-playwright/daemon/$H2/tl-pw-111111111111.err"; }
decoys() { (cd "$CASE_DIR/cache" && find . -path "*$NONCE*" -prune -o -type f -printf '%p %s %T@\n' | LC_ALL=C sort | sha256sum | cut -c1-64); }
run_frag() { # $1 = fragment file; extra env via env
  env -i HOME="$CASE_DIR/home" PATH=/usr/bin:/bin XDG_CACHE_HOME="$CASE_DIR/cache" TL_PW_SESSION=$NONCE \
    TL_PW_RUN="$CASE_DIR/run" "${@:2}" bash -c "( set -u
$(cat "$1")
echo RESIDUE_OK )" > "$CASE_DIR/out" 2>&1 && echo 0 || echo $?; }
expect() { # name want(ok|stop) rc [own_must_remain yes|no] decoy_before
  local name=$1 want=$2 rc=$3 own=$4 d0=$5 ok=1 d1; d1=$(decoys)
  [ "$d0" = "$d1" ] || { ok=0; echo "  decoys changed"; }
  if [ "$want" = ok ]; then [ "$rc" = 0 ] && grep -qx RESIDUE_OK "$CASE_DIR/out" || ok=0
  else [ "$rc" != 0 ] && ! grep -qx RESIDUE_OK "$CASE_DIR/out" && grep -q STOP "$CASE_DIR/out" || ok=0; fi
  if [ "$own" = yes ]; then [ -e "$CASE_DIR/cache/ms-playwright/daemon/$H/$NONCE.err" ] || [ -L "$CASE_DIR/cache/ms-playwright/daemon/$H/$NONCE.err" ] || { ok=0; echo "  own .err missing"; }; fi
  if [ $ok = 1 ]; then PASS=$((PASS+1)); echo "PASS $name rc=$rc"; else FAIL=$((FAIL+1)); echo "FAIL $name rc=$rc"; sed 's/^/    /' "$CASE_DIR/out"; fi; }

# P1: duong dung
new_case P1; d0=$(decoys); own_sha=$(sha256sum < "$CASE_DIR/cache/ms-playwright/daemon/$H/$NONCE.err")
rc=$(run_frag "$SCRATCH/frag_cleanup.sh"); expect P1-positive ok "$rc" no "$d0"
if [ -e "$CASE_DIR/cache/ms-playwright/daemon/$H/$NONCE.err" ] || [ "$(sha256sum < "$CASE_DIR/run/11-daemon.err")" != "$own_sha" ] ||
   [ "$(cat "$CASE_DIR/run/11-daemon-path.txt")" != "$CASE_DIR/cache/ms-playwright/daemon/$H/$NONCE.err" ]; then
  FAIL=$((FAIL+1)); echo "FAIL P1-artefacts"; else PASS=$((PASS+1)); echo "PASS P1-artefacts (goc da xoa, ban sao trung byte, duong dan dung)"; fi
# P2: .err rong (0 byte) nhu do that tren Linux/Desktop
new_case P2; : > "$CASE_DIR/cache/ms-playwright/daemon/$H/$NONCE.err"; d0=$(decoys)
rc=$(run_frag "$SCRATCH/frag_cleanup.sh"); expect P2-empty-err ok "$rc" no "$d0"
# N1: khong co muc nao
new_case N1; rm "$CASE_DIR/cache/ms-playwright/daemon/$H/$NONCE.err"; d0=$(decoys)
rc=$(run_frag "$SCRATCH/frag_cleanup.sh"); expect N1-zero-match stop "$rc" no "$d0"
# N2: cung nonce o hai thu muc hash
new_case N2; printf 'dup\n' > "$CASE_DIR/cache/ms-playwright/daemon/$H2/$NONCE.err"; d0=$(decoys)
rc=$(run_frag "$SCRATCH/frag_cleanup.sh"); expect N2-two-hash-dirs stop "$rc" yes "$d0"
[ -e "$CASE_DIR/cache/ms-playwright/daemon/$H2/$NONCE.err" ] && { PASS=$((PASS+1)); echo "PASS N2-dup-kept"; } || { FAIL=$((FAIL+1)); echo "FAIL N2-dup-kept"; }
# N3: .session con sot (delete-data chua xoa)
new_case N3; printf '{}\n' > "$CASE_DIR/cache/ms-playwright/daemon/$H/$NONCE.session"; d0=$(decoys)
rc=$(run_frag "$SCRATCH/frag_cleanup.sh"); expect N3-session-left stop "$rc" yes "$d0"
# N4: ud-<nonce>-* con sot
new_case N4; mkdir "$CASE_DIR/cache/ms-playwright/daemon/$H/ud-$NONCE-chromium"; d0=$(decoys)
rc=$(run_frag "$SCRATCH/frag_cleanup.sh"); expect N4-userdata-left stop "$rc" yes "$d0"
# N5: .err la symlink toi tep cua phien khac
new_case N5; rm "$CASE_DIR/cache/ms-playwright/daemon/$H/$NONCE.err"
ln -s "$CASE_DIR/cache/ms-playwright/daemon/$H/$OTHER.err" "$CASE_DIR/cache/ms-playwright/daemon/$H/$NONCE.err"; d0=$(decoys)
rc=$(run_frag "$SCRATCH/frag_cleanup.sh"); expect N5-err-symlink stop "$rc" yes "$d0"
# N6: thu muc hash la symlink
new_case N6; mkdir -p "$CASE_DIR/elsewhere"; mv "$CASE_DIR/cache/ms-playwright/daemon/$H/$NONCE.err" "$CASE_DIR/elsewhere/"
ln -s "$CASE_DIR/elsewhere" "$CASE_DIR/cache/ms-playwright/daemon/cccccccccccccccc"; d0=$(decoys)
rc=$(run_frag "$SCRATCH/frag_cleanup.sh"); expect N6-hashdir-symlink stop "$rc" no "$d0"
[ -e "$CASE_DIR/elsewhere/$NONCE.err" ] && { PASS=$((PASS+1)); echo "PASS N6-target-kept"; } || { FAIL=$((FAIL+1)); echo "FAIL N6-target-kept"; }
# N7: so phien la symlink
new_case N7; mv "$CASE_DIR/cache/ms-playwright/daemon" "$CASE_DIR/real-daemon"; ln -s "$CASE_DIR/real-daemon" "$CASE_DIR/cache/ms-playwright/daemon"; d0=$(decoys)
rc=$(run_frag "$SCRATCH/frag_cleanup.sh"); expect N7-daemon-symlink stop "$rc" no "$d0"
[ -e "$CASE_DIR/real-daemon/$H/$NONCE.err" ] && { PASS=$((PASS+1)); echo "PASS N7-target-kept"; } || { FAIL=$((FAIL+1)); echo "FAIL N7-target-kept"; }
# N8: output cu trong run
new_case N8; printf 'old\n' > "$CASE_DIR/run/11-daemon.err"; d0=$(decoys)
rc=$(run_frag "$SCRATCH/frag_cleanup.sh"); expect N8-stale-output stop "$rc" yes "$d0"
[ "$(cat "$CASE_DIR/run/11-daemon.err")" = old ] && { PASS=$((PASS+1)); echo "PASS N8-old-kept"; } || { FAIL=$((FAIL+1)); echo "FAIL N8-old-kept"; }
# N9: ten thu muc hash sai dang
new_case N9; mkdir "$CASE_DIR/cache/ms-playwright/daemon/not-a-hash"; mv "$CASE_DIR/cache/ms-playwright/daemon/$H/$NONCE.err" "$CASE_DIR/cache/ms-playwright/daemon/not-a-hash/"; d0=$(decoys)
rc=$(run_frag "$SCRATCH/frag_cleanup.sh"); expect N9-bad-hash-name stop "$rc" no "$d0"
[ -e "$CASE_DIR/cache/ms-playwright/daemon/not-a-hash/$NONCE.err" ] && { PASS=$((PASS+1)); echo "PASS N9-kept"; } || { FAIL=$((FAIL+1)); echo "FAIL N9-kept"; }
# N10: hook test PWTEST_DAEMON_SESSION_DIR dat
new_case N10; d0=$(decoys)
rc=$(run_frag "$SCRATCH/frag_cleanup.sh" PWTEST_DAEMON_SESSION_DIR="$CASE_DIR/x"); expect N10-pwtest-hook stop "$rc" yes "$d0"
# N11: .err la thu muc
new_case N11; rm "$CASE_DIR/cache/ms-playwright/daemon/$H/$NONCE.err"; mkdir "$CASE_DIR/cache/ms-playwright/daemon/$H/$NONCE.err"; d0=$(decoys)
rc=$(run_frag "$SCRATCH/frag_cleanup.sh"); expect N11-err-is-dir stop "$rc" yes "$d0"
# N12: chua co so phien
new_case N12; rm -r "$CASE_DIR/cache/ms-playwright/daemon"; mkdir -p "$CASE_DIR/cache/ms-playwright"; d0=$(decoys)
rc=$(run_frag "$SCRATCH/frag_cleanup.sh"); expect N12-no-registry stop "$rc" no "$d0"
# C1/C2/C3: kiem truoc open (chay duoi set -Eeuo pipefail nhu khoi Capture)
run_pre() { env -i HOME="$CASE_DIR/home" PATH=/usr/bin:/bin XDG_CACHE_HOME="$CASE_DIR/cache" TL_PW_SESSION=$NONCE bash -c "( set -Eeuo pipefail
$(cat "$SCRATCH/frag_pre.sh")
echo RESIDUE_OK )" > "$CASE_DIR/out" 2>&1 && echo 0 || echo $?; }
new_case C1; rm "$CASE_DIR/cache/ms-playwright/daemon/$H/$NONCE.err"; d0=$(decoys); rc=$(run_pre)
[ "$rc" = 0 ] && grep -qx RESIDUE_OK "$CASE_DIR/out" && [ "$d0" = "$(decoys)" ] && { PASS=$((PASS+1)); echo "PASS C1-pre-clean rc=$rc"; } || { FAIL=$((FAIL+1)); echo "FAIL C1-pre-clean rc=$rc"; }
new_case C2; d0=$(decoys); rc=$(run_pre)
[ "$rc" != 0 ] && ! grep -qx RESIDUE_OK "$CASE_DIR/out" && [ -e "$CASE_DIR/cache/ms-playwright/daemon/$H/$NONCE.err" ] && { PASS=$((PASS+1)); echo "PASS C2-pre-nonce-present rc=$rc"; } || { FAIL=$((FAIL+1)); echo "FAIL C2-pre-nonce-present rc=$rc"; }
new_case C3; rm -r "$CASE_DIR/cache/ms-playwright"; rc=$(run_pre)
[ "$rc" = 0 ] && grep -qx RESIDUE_OK "$CASE_DIR/out" && { PASS=$((PASS+1)); echo "PASS C3-pre-no-registry rc=$rc"; } || { FAIL=$((FAIL+1)); echo "FAIL C3-pre-no-registry rc=$rc"; }

# Dot bien: moi ban vá yeu di phai lam DO it nhat mot ca (ca dich ghi ro).
mut() { # name target_case sed_expr
  local name=$1 target=$2 expr=$3 m="$SCRATCH/mut-$1.sh" rc
  sed -E "$expr" "$SCRATCH/frag_cleanup.sh" > "$m"
  cmp -s "$m" "$SCRATCH/frag_cleanup.sh" && { FAIL=$((FAIL+1)); echo "FAIL MUT $name: sed khong doi gi"; return; }
  case "$target" in
    N2) new_case "M-$name"; printf 'dup\n' > "$CASE_DIR/cache/ms-playwright/daemon/$H2/$NONCE.err";;
    N3) new_case "M-$name"; printf '{}\n' > "$CASE_DIR/cache/ms-playwright/daemon/$H/$NONCE.session";;
    N5) new_case "M-$name"; rm "$CASE_DIR/cache/ms-playwright/daemon/$H/$NONCE.err"; ln -s "$CASE_DIR/cache/ms-playwright/daemon/$H/$OTHER.err" "$CASE_DIR/cache/ms-playwright/daemon/$H/$NONCE.err";;
    N7) new_case "M-$name"; mv "$CASE_DIR/cache/ms-playwright/daemon" "$CASE_DIR/real-daemon"; ln -s "$CASE_DIR/real-daemon" "$CASE_DIR/cache/ms-playwright/daemon";;
    N8) new_case "M-$name"; printf 'old\n' > "$CASE_DIR/run/11-daemon.err";;
    N9) new_case "M-$name"; mkdir "$CASE_DIR/cache/ms-playwright/daemon/not-a-hash"; mv "$CASE_DIR/cache/ms-playwright/daemon/$H/$NONCE.err" "$CASE_DIR/cache/ms-playwright/daemon/not-a-hash/";;
    N10) new_case "M-$name";;
  esac
  if [ "$target" = N10 ]; then rc=$(run_frag "$m" PWTEST_DAEMON_SESSION_DIR=x); else rc=$(run_frag "$m"); fi
  if [ "$rc" = 0 ] && grep -qx RESIDUE_OK "$CASE_DIR/out"; then PASS=$((PASS+1)); echo "PASS MUT $name -> $target lot (chot co rang)"
  else FAIL=$((FAIL+1)); echo "FAIL MUT $name -> $target van chan (chot khong do duoc)"; fi; }
mut exact-one N2 's/\[ "\$\{#hit\[@\]\}" -eq 1 \]/[ "${#hit[@]}" -ge 1 ]/'
mut name-glob N3 's/-name "\*\$TL_PW_SESSION\*"/-name "$TL_PW_SESSION.err"/'
mut no-symlink-check N5 's/\[ -f "\$f" \] && \[ ! -L "\$f" \]/[ -e "$f" ]/'
mut daemon-symlink N7 's/\[ -d "\$D" \] && \[ ! -L "\$D" \]/[ -d "$D" ]/; s/find "\$D" /find -L "$D" /'
mut stale-output N8 's/\[ ! -e "\$TL_PW_RUN\/\$ten" \] && \[ ! -L "\$TL_PW_RUN\/\$ten" \]/true/; s/cp -- /cp -f -- /'
mut hash-shape N9 's/\[0-9a-f\]\{16\}/[^\/]+/'
mut pwtest-hook N10 's/\[ -z "\$\{PWTEST_DAEMON_SESSION_DIR\+x\}" \]/true/'

echo "TONG: $PASS dat / $((PASS+FAIL))"
[ "$FAIL" -eq 0 ]
