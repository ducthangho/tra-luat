#!/usr/bin/env bash
# Ma tran phan chung cho buoc don du luong daemon cua playwright-browser SKILL.md (packet #1389).
# Chay TREN BYTE CUA SKILL: trich NOI DUNG giua cap dong danh dau (khong gom dong danh dau) trong khoi bash:
#   "  # --- du-luong-daemon-truoc-open: bat dau|het"   (Capture, truoc open)
#   "  # --- du-luong-daemon-dau-cleanup: bat dau|het"  (Cleanup, truoc close)
#   "  # --- du-luong-daemon: bat dau|het"              (Cleanup, sau 10-verify)
# Moi cap phai xuat hien DUNG 2 lan (bash + PowerShell); lay lan thu nhat. Dong `node -e` cua SKILL chay THAT bang node,
# nhung tren registry.js GIA (tra so phien do ca chi dinh qua FX_*); registry.js that cua ban ghim do o luot native.
# Khong goi CLI, khong mang, khong trinh duyet.
# Dung: bash residue_matrix.sh <SKILL.md> <SCRATCH (thu muc rong, ngoai Git)> [<duong dan node>]
set -euo pipefail
SKILL=$1; SCRATCH=$2; NODE=${3:-$(command -v node || true)}
[ -f "$SKILL" ] && [ -d "$SCRATCH" ] && [ -z "$(ls -A "$SCRATCH")" ] && [ -x "$NODE" ] ||
  { echo "usage: SKILL.md + empty SCRATCH + node" >&2; exit 2; }
SCRATCH=$(cd "$SCRATCH" && pwd -P)
NONCE=tl-pw-0123456789ab; OTHER=tl-pw-ba9876543210; H=aaaaaaaaaaaaaaaa; H2=bbbbbbbbbbbbbbbb

extract() { # $1 = ten cap, $2 = tep ra. Noi dung giua cap THU NHAT; kiem du 2 cap, khong long nhau.
  awk -v B="  # --- $1: bat dau" -v E="  # --- $1: het" -v OUT="$2" '
    $0 == B { if (open) { bad = 1 } open = 1; nb++; next }
    $0 == E { if (!open) { bad = 1 } open = 0; ne++; next }
    open && nb == 1 { print > OUT }
    END { if (bad || open || nb != 2 || ne != 2) { printf "FAIL: cap danh dau %s sai (bat dau=%d het=%d)\n", B, nb, ne > "/dev/stderr"; exit 1 } }' "$SKILL"; }
extract du-luong-daemon-truoc-open "$SCRATCH/frag_pre.sh"
extract du-luong-daemon-dau-cleanup "$SCRATCH/frag_dau.sh"
extract du-luong-daemon "$SCRATCH/frag_cleanup.sh"
grep -q 'find "\$D"' "$SCRATCH/frag_pre.sh" && grep -q 'TL_PW_NODE' "$SCRATCH/frag_dau.sh" && grep -q 'mapfile -d' "$SCRATCH/frag_cleanup.sh" ||
  { echo "FAIL: doan trich khong phai ban bash" >&2; exit 1; }
cat "$SCRATCH/frag_dau.sh" "$SCRATCH/frag_cleanup.sh" > "$SCRATCH/frag_dau_cleanup.sh"
# chi doan don (D/DH dat san tu FX_*): de do rieng cac chot cua doan don ma doan dau-cleanup cung kiem
{ printf 'D=$FX_BASE; DH=$FX_DIR\n'; cat "$SCRATCH/frag_cleanup.sh"; } > "$SCRATCH/frag_res_only.sh"
echo "SOURCE $(sha256sum < "$SKILL" | cut -c1-64) pre_frag $(sha256sum < "$SCRATCH/frag_pre.sh" | cut -c1-64) dau_frag $(sha256sum < "$SCRATCH/frag_dau.sh" | cut -c1-64) cleanup_frag $(sha256sum < "$SCRATCH/frag_cleanup.sh" | cut -c1-64) node $("$NODE" --version)"

PASS=0; FAIL=0; CASE_DIR=
ok() { PASS=$((PASS+1)); echo "PASS $*"; }
ko() { FAIL=$((FAIL+1)); echo "FAIL $*"; [ -f "$CASE_DIR/out" ] && sed 's/^/    /' "$CASE_DIR/out"; return 0; }
sha() { sha256sum < "$1" | cut -c1-64; }
BASE() { echo "$CASE_DIR/cache/ms-playwright/daemon"; }
OWN() { echo "$(BASE)/$H/$NONCE.err"; }
new_case() { CASE_DIR="$SCRATCH/case-$1"; local d; d=$(BASE)
  mkdir -p "$d/$H" "$d/$H2" "$CASE_DIR/run" "$CASE_DIR/home" "$CASE_DIR/bin" "$CASE_DIR/work" \
    "$CASE_DIR/install/node_modules/playwright-core/lib/tools/cli-client"
  printf 'module.exports={baseDaemonDir:()=>process.env.FX_BASE,createClientInfo:()=>({daemonProfilesDir:process.env.FX_DIR,workspaceDir:process.env.FX_WS||undefined})};\n' \
    > "$CASE_DIR/install/node_modules/playwright-core/lib/tools/cli-client/registry.js"
  printf 'own stderr %s\n' "$1" > "$d/$H/$NONCE.err"
  # moi cua phien khac va mot .err cu: KHONG BAO GIO duoc dung toi
  printf 'other\n' > "$d/$H/$OTHER.err"; printf '{}\n' > "$d/$H/$OTHER.session"
  printf 'legacy\n' > "$d/$H2/tl-pw-111111111111.err"
  printf '%s\n%s\n%s\n' "$d" "$d/$H" "$NONCE" > "$CASE_DIR/run/00-sophien.txt"; }   # nhu Capture da ghi
# Anh chup tung tep KHONG mang nonce: duong dan, kich thuoc, mtime, sha256 noi dung.
decoys() { (cd "$CASE_DIR" && find cache -path "*$NONCE*" -prune -o -type f -printf '%p\t%s\t%T@\n' | LC_ALL=C sort |
  while IFS=$'\t' read -r p s t; do printf '%s\t%s\t%s\t%s\n' "$p" "$s" "$t" "$(sha256sum < "$p" | cut -c1-64)"; done | sha256sum | cut -c1-64); }
# snap: anh chup TRUOC khi chay cho cac tep phai giu (ten|loai|sha|mtime), so lai SAU khi chay
snap() { local p; for p in "$@"; do printf '%s|%s|%s|%s\n' "$p" "$(stat -c %F "$p" 2>/dev/null)" \
  "$( [ -f "$p" ] && sha "$p" || echo -)" "$(stat -c %Y.%y "$p" 2>/dev/null)"; done; }
no_new_outputs() { [ ! -e "$CASE_DIR/run/11-daemon.err" ] && [ ! -e "$CASE_DIR/run/11-daemon-path.txt" ]; }
envs() { echo HOME="$CASE_DIR/home" PATH="$CASE_DIR/bin:/usr/bin:/bin" XDG_CACHE_HOME="$CASE_DIR/cache" TL_PW_SESSION=$NONCE \
  TL_PW_RUN="$CASE_DIR/run" TL_PW_ROOT="$CASE_DIR" TL_PW_INSTALL="$CASE_DIR/install" TL_PW_NODE="$NODE" \
  FX_BASE="$(BASE)" FX_DIR="$(BASE)/$H"; }
run_frag() { # $1 = tep doan (set -u nhu khoi Cleanup); con lai: KEY=VAL ghi de
  local body=$1; shift
  ( cd "$CASE_DIR/home" && env -i $(envs) "$@" bash -c "( set -u
$(cat "$body")
echo RESIDUE_OK )" ) > "$CASE_DIR/out" 2>&1 && echo 0 || echo $?; }
run_pre() { # doan truoc open chay trong subshell co set -Eeuo pipefail + trap ERR y nhu khoi Capture
  local body=$1; shift
  ( cd "$CASE_DIR/home" && env -i $(envs) "$@" bash -c "( set -Eeuo pipefail; trap 'echo \"STOP: \$BASH_COMMAND — chạy Cleanup\" >&2' ERR
$(cat "$body")
echo RESIDUE_OK )" ) > "$CASE_DIR/out" 2>&1 && echo 0 || echo $?; }
is_ok() { [ "$1" = 0 ] && grep -qx RESIDUE_OK "$CASE_DIR/out"; }
is_stop() { [ "$1" != 0 ] && ! grep -qx RESIDUE_OK "$CASE_DIR/out" && grep -q STOP "$CASE_DIR/out"; }
# expect_stop NAME RC D0 SNAP_TRUOC [--outputs]: STOP, moi nguyen, tep da chup nguyen, khong output 11 moi
expect_stop() { local n=$1 rc=$2 d0=$3 s0=$4 o=${5:-} bad=
  is_stop "$rc" || bad="khong dung dung cach"
  [ "$d0" = "$(decoys)" ] || bad="$bad; moi bi doi"
  [ -z "$s0" ] || [ "$s0" = "$(snap $(printf '%s\n' "$s0" | cut -d'|' -f1))" ] || bad="$bad; tep phai giu bi doi/mat"
  [ "$o" = --outputs ] || no_new_outputs || bad="$bad; co output 11 moi"
  if [ -z "$bad" ]; then ok "$n rc=$rc"; else ko "$n rc=$rc ($bad)"; fi; }
expect_ok() { local n=$1 rc=$2 d0=$3 own=$4
  if is_ok "$rc" && [ "$d0" = "$(decoys)" ] && [ ! -e "$(OWN)" ] && [ "$(sha "$CASE_DIR/run/11-daemon.err")" = "$own" ] &&
     [ "$(cat "$CASE_DIR/run/11-daemon-path.txt")" = "$(OWN)" ]; then ok "$n (goc da xoa, ban sao trung byte, duong dan dung, moi nguyen)"
  else ko "$n rc=$rc"; fi; }
fake_find() { printf '#!/bin/bash\nprintf "%%s\\0" "%s"; echo "find: $1/dddddddddddddddd: Permission denied" >&2; exit 1\n' "$(OWN)" > "$CASE_DIR/bin/find"; chmod +x "$CASE_DIR/bin/find"; }
fake_find_empty() { printf '#!/bin/bash\necho "find: $1/dddddddddddddddd: Permission denied" >&2; exit 1\n' > "$CASE_DIR/bin/find"; chmod +x "$CASE_DIR/bin/find"; }
P=$SCRATCH/frag_pre.sh; DAU=$SCRATCH/frag_dau.sh; F=$SCRATCH/frag_dau_cleanup.sh; R=$SCRATCH/frag_res_only.sh

# ===== Cleanup (dau-cleanup + don du luong) =====
for c in P1 P2; do new_case $c; [ $c = P2 ] && : > "$(OWN)"; d0=$(decoys); own=$(sha "$(OWN)"); rc=$(run_frag "$F"); expect_ok "$c-positive" "$rc" "$d0" "$own"; done
new_case N1; rm "$(OWN)"; d0=$(decoys); rc=$(run_frag "$F"); expect_stop N1-zero-match "$rc" "$d0" ""
new_case N2; DUP=$(BASE)/$H2/$NONCE.err; printf 'dup\n' > "$DUP"; d0=$(decoys); s0=$(snap "$(OWN)" "$DUP"); rc=$(run_frag "$F"); expect_stop N2-two-hash-dirs "$rc" "$d0" "$s0"
new_case N3; S=$(BASE)/$H/$NONCE.session; printf '{}\n' > "$S"; d0=$(decoys); s0=$(snap "$(OWN)" "$S"); rc=$(run_frag "$F"); expect_stop N3-session-left "$rc" "$d0" "$s0"
new_case N4; U=$(BASE)/$H/ud-$NONCE-chromium; mkdir "$U"; printf 'x\n' > "$U/Prefs"; d0=$(decoys); s0=$(snap "$(OWN)" "$U/Prefs"); rc=$(run_frag "$F"); expect_stop N4-userdata-left "$rc" "$d0" "$s0"
new_case N5; rm "$(OWN)"; ln -s "$(BASE)/$H/$OTHER.err" "$(OWN)"; d0=$(decoys); rc=$(run_frag "$F"); expect_stop N5-err-symlink "$rc" "$d0" ""; [ -L "$(OWN)" ] || ko "N5 link mat"
new_case N6; mkdir -p "$CASE_DIR/elsewhere"; mv "$(OWN)" "$CASE_DIR/elsewhere/"; ln -s "$CASE_DIR/elsewhere" "$(BASE)/cccccccccccccccc"; d0=$(decoys)
s0=$(snap "$CASE_DIR/elsewhere/$NONCE.err"); rc=$(run_frag "$F"); expect_stop N6-other-hashdir-symlink "$rc" "$d0" "$s0"
new_case N7; mv "$(BASE)" "$CASE_DIR/real-daemon"; ln -s "$CASE_DIR/real-daemon" "$(BASE)"; d0=$(decoys); s0=$(snap "$CASE_DIR/real-daemon/$H/$NONCE.err")
rc=$(run_frag "$F"); expect_stop N7-daemon-symlink "$rc" "$d0" "$s0"
for v in err path; do new_case N8-$v; if [ $v = err ]; then o=11-daemon.err; other=11-daemon-path.txt; else o=11-daemon-path.txt; other=11-daemon.err; fi
  printf 'old\n' > "$CASE_DIR/run/$o"; d0=$(decoys); s0=$(snap "$(OWN)" "$CASE_DIR/run/$o"); rc=$(run_frag "$F")
  expect_stop "N8-stale-$o" "$rc" "$d0" "$s0" --outputs; [ ! -e "$CASE_DIR/run/$other" ] || ko "N8-$v tao $other"; done
new_case N9; mkdir "$(BASE)/not-a-hash"; mv "$(OWN)" "$(BASE)/not-a-hash/"; d0=$(decoys); s0=$(snap "$(BASE)/not-a-hash/$NONCE.err")
rc=$(run_frag "$F"); expect_stop N9-bad-hash-name "$rc" "$d0" "$s0"
new_case N10; d0=$(decoys); s0=$(snap "$(OWN)"); rc=$(run_frag "$F" PWTEST_DAEMON_SESSION_DIR="$CASE_DIR/x"); expect_stop N10-pwtest-hook "$rc" "$d0" "$s0"
new_case N11; rm "$(OWN)"; mkdir "$(OWN)"; d0=$(decoys); rc=$(run_frag "$F"); expect_stop N11-err-is-dir "$rc" "$d0" ""; [ -d "$(OWN)" ] || ko N11
new_case N12; rm -r "$(BASE)"; d0=$(decoys); rc=$(run_frag "$F"); expect_stop N12-no-registry "$rc" "$d0" ""
new_case N14; W=$(BASE)/$H/${NONCE}Xerr; mv "$(OWN)" "$W"; d0=$(decoys); s0=$(snap "$W"); rc=$(run_frag "$F"); expect_stop N14-wrong-suffix "$rc" "$d0" "$s0"
new_case N15; fake_find; d0=$(decoys); s0=$(snap "$(OWN)"); rc=$(run_frag "$F"); expect_stop N15-scan-error "$rc" "$d0" "$s0"
new_case N16; NL="$(BASE)/$H2/x
$NONCE.err"; printf 'nl\n' > "$NL"; d0=$(decoys); s0=$(snap "$(OWN)"); nl0=$(sha "$NL"); rc=$(run_frag "$F"); expect_stop N16-newline-name "$rc" "$d0" "$s0"
[ "$(sha "$NL")" = "$nl0" ] || ko "N16 tep ten co xuong dong bi doi/mat"
new_case N17; mkdir -p "$CASE_DIR/home/rel"; cp -a "$CASE_DIR/cache" "$CASE_DIR/home/rel/"; printf 'rel/cache/ms-playwright/daemon\nrel/cache/ms-playwright/daemon/%s\n%s\n' $H $NONCE > "$CASE_DIR/run/00-sophien.txt"
d0=$(decoys); s0=$(snap "$(OWN)" "$CASE_DIR/home/rel/cache/ms-playwright/daemon/$H/$NONCE.err")
rc=$(run_frag "$F" FX_BASE=rel/cache/ms-playwright/daemon FX_DIR=rel/cache/ms-playwright/daemon/$H); expect_stop N17-relative-cache "$rc" "$d0" "$s0"
new_case N18; mv "$(OWN)" "$(BASE)/$H2/"; d0=$(decoys); s0=$(snap "$(BASE)/$H2/$NONCE.err"); rc=$(run_frag "$F"); expect_stop N18-err-in-other-install-dir "$rc" "$d0" "$s0"
new_case N19; mv "$(BASE)/$H" "$CASE_DIR/real-hash"; ln -s "$CASE_DIR/real-hash" "$(BASE)/$H"; d0=$(decoys); s0=$(snap "$CASE_DIR/real-hash/$NONCE.err")
rc=$(run_frag "$F"); expect_stop N19-own-hashdir-symlink "$rc" "$d0" "$s0"
# dau-cleanup: phai dung TRUOC close (chi chay doan dau)
new_case D1; rm "$CASE_DIR/run/00-sophien.txt"; d0=$(decoys); s0=$(snap "$(OWN)"); rc=$(run_frag "$DAU"); expect_stop D1-no-capture-record "$rc" "$d0" "$s0"
new_case D2; d0=$(decoys); s0=$(snap "$(OWN)"); rc=$(run_frag "$DAU" FX_DIR="$(BASE)/$H2"); expect_stop D2-registry-changed "$rc" "$d0" "$s0"
new_case D3; d0=$(decoys); s0=$(snap "$(OWN)"); rc=$(run_frag "$DAU" FX_WS=/somewhere); expect_stop D3-cli-workspace-mode "$rc" "$d0" "$s0"
new_case D4; rc=$(run_frag "$DAU"); is_ok "$rc" && ok "D4-dau-matches rc=$rc" || ko "D4-dau-matches rc=$rc"
new_case D5; mv "$(BASE)" "$CASE_DIR/real-daemon"; ln -s "$CASE_DIR/real-daemon" "$(BASE)"; d0=$(decoys); s0=$(snap "$CASE_DIR/real-daemon/$H/$NONCE.err")
rc=$(run_frag "$DAU"); expect_stop D5-daemon-link-at-cleanup-start "$rc" "$d0" "$s0"
new_case D6; mv "$(BASE)/$H" "$CASE_DIR/real-hash"; ln -s "$CASE_DIR/real-hash" "$(BASE)/$H"; d0=$(decoys); s0=$(snap "$CASE_DIR/real-hash/$NONCE.err")
rc=$(run_frag "$DAU"); expect_stop D6-hash-link-at-cleanup-start "$rc" "$d0" "$s0"
new_case D7; printf '%s\n%s\n%s\n' "$(BASE)" "$(BASE)/$H" "$OTHER" > "$CASE_DIR/run/00-sophien.txt"; d0=$(decoys); s0=$(snap "$(OWN)")
rc=$(run_frag "$DAU"); expect_stop D7-record-of-other-nonce "$rc" "$d0" "$s0"
new_case D8; d0=$(decoys); s0=$(snap "$(OWN)"); rc=$(run_frag "$DAU" PWTEST_DAEMON_SESSION_DIR=x); expect_stop D8-pwtest-hook-at-cleanup-start "$rc" "$d0" "$s0"

# ===== truoc open =====
pre_ok() { local n=$1 rc=$2; if is_ok "$rc" && [ "$(cat "$CASE_DIR/run/00-sophien.txt" 2>/dev/null)" = "$(BASE)
$(BASE)/$H
$NONCE" ]; then ok "$n rc=$rc (00-sophien.txt dung)"; else ko "$n rc=$rc"; fi; }
pre_stop() { local n=$1 rc=$2 bad=; is_stop "$rc" || bad="khong dung"; grep -q 'KHÔNG chạy Cleanup' "$CASE_DIR/out" || bad="$bad; thieu 'KHONG chay Cleanup'"
  ! grep -q '— chạy Cleanup' "$CASE_DIR/out" || bad="$bad; trap ERR bao 'chay Cleanup'"; [ ! -e "$CASE_DIR/run/00-sophien.txt" ] || bad="$bad; co 00-sophien.txt"
  if [ -z "$bad" ]; then ok "$n rc=$rc"; else ko "$n rc=$rc ($bad)"; fi; }
newp() { new_case "$1"; rm "$CASE_DIR/run/00-sophien.txt"; }
newp C1; rm "$(OWN)"; rc=$(run_pre "$P"); pre_ok C1-pre-clean "$rc"
newp C2; s0=$(snap "$(OWN)"); rc=$(run_pre "$P"); pre_stop C2-pre-nonce-present "$rc"; [ "$s0" = "$(snap "$(OWN)")" ] || ko "C2 tep doi"
newp C3; rm -r "$CASE_DIR/cache/ms-playwright"; rc=$(run_pre "$P"); pre_ok C3-pre-no-registry "$rc"
newp C4; rm "$(OWN)"; rc=$(run_pre "$P" FX_BASE=rel/d FX_DIR=rel/d/$H); pre_stop C4-pre-relative "$rc"
newp C5; rm "$(OWN)"; rc=$(run_pre "$P" PWTEST_DAEMON_SESSION_DIR="$CASE_DIR/x"); pre_stop C5-pre-pwtest-hook "$rc"
newp C6; mv "$(OWN)" "$(BASE)/$NONCE.err"; rc=$(run_pre "$P"); pre_ok "C6-pre-depth1-ignored (nhu CLI)" "$rc"
newp C7; rm "$(OWN)"; fake_find_empty; rc=$(run_pre "$P"); pre_stop C7-pre-scan-error "$rc"
newp C8; rm "$(OWN)"; rc=$(run_pre "$P" FX_WS=/somewhere); pre_stop C8-pre-cli-workspace-mode "$rc"
newp C9; rm "$(OWN)"; mv "$(BASE)" "$CASE_DIR/real-daemon"; ln -s "$CASE_DIR/real-daemon" "$(BASE)"; rc=$(run_pre "$P"); pre_stop C9-pre-daemon-symlink "$rc"
newp C10; rm "$(OWN)"; mv "$(BASE)/$H" "$CASE_DIR/real-hash"; ln -s "$CASE_DIR/real-hash" "$(BASE)/$H"; rc=$(run_pre "$P"); pre_stop C10-pre-hashdir-symlink "$rc"
newp C11; rm "$(OWN)"; rc=$(run_pre "$P" FX_DIR="$(BASE)/not-a-hash"); pre_stop C11-pre-bad-hash-shape "$rc"
newp C12; rm "$(OWN)"; rc=$(run_pre "$P" FX_DIR="$CASE_DIR/elsewhere/$H"); pre_stop C12-pre-hash-not-under-base "$rc"
newp C13; rm "$(OWN)"; rc=$(run_pre "$P" TL_PW_NODE=/nonexistent/node); pre_stop C13-pre-node-missing "$rc"

# ===== TOAN LUONG: chinh khoi bash Capture (khoi 3) + Cleanup (khoi 5) cua SKILL, voi CLI GIA co nhat ky va trang thai =====
awk 'BEGIN{n=0} /^```bash$/{n++; inb=1; next} /^```$/{inb=0; next} inb{print > (OUTD "/block" n ".sh")}' OUTD="$SCRATCH" "$SKILL"
grep -q 'chay_ghi 01-open open about:blank' "$SCRATCH/block3.sh" && grep -q "echo 'CLEANUP OK'" "$SCRATCH/block5.sh" ||
  { echo "FAIL: khong tim thay khoi Capture/Cleanup bash" >&2; exit 1; }
# Capture: thay URL; dong chu thich "Chay khoi Kiem pin" thay bang ghi 00-pins.log = PIN OK (Kiem pin do o luot native)
sed -e "s#'<https://nguon-cong-khai/duong-dan>'#'https://example.com/'#" \
    -e 's#^\# Chạy khối Kiểm pin bash ở trên dạng:.*#printf "PIN OK\\n" > "$TL_PW_RUN/00-pins.log"#' "$SCRATCH/block3.sh" > "$SCRATCH/flow_capture.sh"
grep -q 'PIN OK\\n" > "\$TL_PW_RUN/00-pins.log"' "$SCRATCH/flow_capture.sh" || { echo "FAIL: khong thay duoc dong Kiem pin" >&2; exit 1; }
cat > "$SCRATCH/fakecli.js" <<'JS'
// CLI gia: ghi nhat ky lenh, giu trang thai phien, tao/xoa tep trong so phien FX_DIR nhu daemon that.
const fs = require('fs'), path = require('path');
const a = process.argv.slice(2); const ses = (a.find(x => x.startsWith('--session=')) || '').slice(10);
const cmd = a.find(x => !x.startsWith('--')); const root = process.env.TL_PW_ROOT, dir = process.env.FX_DIR;
fs.appendFileSync(path.join(root, 'fakecli.log'), cmd + ' ' + ses + '\n');
const st = path.join(root, 'fakestate'); fs.mkdirSync(st, { recursive: true }); const sf = path.join(st, ses);
const state = fs.existsSync(sf) ? fs.readFileSync(sf, 'utf8') : 'none'; const out = o => process.stdout.write(JSON.stringify(o, null, 2) + '\n');
if (cmd === 'open') { fs.mkdirSync(dir, { recursive: true }); fs.writeFileSync(path.join(dir, ses + '.err'), '');
  fs.writeFileSync(path.join(dir, ses + '.session'), '{}'); fs.writeFileSync(sf, 'open'); out({}); }
else if (cmd === 'close') { if (state === 'open') { fs.writeFileSync(sf, 'closed'); out({ session: ses, status: 'closed' }); } else out({ session: ses, status: 'not-open' }); }
else if (cmd === 'delete-data') { try { fs.unlinkSync(path.join(dir, ses + '.session')); } catch (e) {} out({ session: ses, deleted: false }); }
else if (cmd === 'tab-list' && state !== 'open') { out({ isError: true, error: "The browser '" + ses + "' is not open, please run open first" }); process.exit(1); }
else if (cmd === 'tab-list') out({ result: '- 0: (current) [Example Domain](https://example.com/)' });
else if (cmd === 'requests') out({ result: '1. [GET] https://example.com/ => [200] ' });
else out({});
JS
flow() { # flow <ten> <capture-file> <cleanup-file> [ham-chen-giua] : chay Capture roi Cleanup trong CUNG shell
  CASE_DIR="$SCRATCH/flow-$1"; mkdir -p "$CASE_DIR/runs" "$CASE_DIR/work" "$CASE_DIR/home" "$CASE_DIR/cache" \
    "$CASE_DIR/install/node_modules/playwright-core/lib/tools/cli-client"
  printf 'module.exports={baseDaemonDir:()=>process.env.FX_BASE,createClientInfo:()=>({daemonProfilesDir:process.env.FX_DIR,workspaceDir:process.env.FX_WS||undefined})};\n' \
    > "$CASE_DIR/install/node_modules/playwright-core/lib/tools/cli-client/registry.js"
  mkdir -p "$(BASE)/$H2"; printf 'legacy\n' > "$(BASE)/$H2/tl-pw-111111111111.err"
  { echo 'set -u'; echo "export TL_PW_ROOT='$CASE_DIR' TL_PW_NODE='$NODE' TL_PW_CLI='$SCRATCH/fakecli.js' TL_PW_INSTALL='$CASE_DIR/install'"
    echo "export FX_BASE='$(BASE)' FX_DIR='$(BASE)/$H' ${FLOW_ENV:-}"
    cat "$2"; echo 'echo "CAPTURE_RC=$?"'; echo 'printf "%s\n" "$TL_PW_SESSION" > "$TL_PW_ROOT/nonce.txt"'
    echo "${FLOW_BETWEEN:-:}"; cat "$3"; echo 'echo "CLEANUP_RC=$?"'; } > "$CASE_DIR/flow.sh"
  ( cd "$CASE_DIR/home" && env -i HOME="$CASE_DIR/home" PATH=/usr/bin:/bin bash "$CASE_DIR/flow.sh" ) > "$CASE_DIR/out" 2>&1 || true; }
log() { tr '\n' ' ' < "$CASE_DIR/fakecli.log" 2>/dev/null | sed "s/ $(cat "$CASE_DIR/nonce.txt" 2>/dev/null)//g; s/ *$//"; }
# E1: duong dung toan luong
FLOW_ENV= FLOW_BETWEEN=: flow E1 "$SCRATCH/flow_capture.sh" "$SCRATCH/block5.sh"
n=$(cat "$CASE_DIR/nonce.txt"); if grep -qx 'CLEANUP OK' "$CASE_DIR/out" && [ "$(log)" = "open goto tab-list requests close delete-data tab-list" ] &&
  [ ! -e "$(BASE)/$H/$n.err" ] && [ "$(sed -n 3p "$CASE_DIR"/runs/*/00-sophien.txt)" = "$n" ] && [ -s "$CASE_DIR"/runs/*/SHA256SUMS ] &&
  grep -q 00-sophien "$CASE_DIR"/runs/*/SHA256SUMS && grep -q 11-daemon.err "$CASE_DIR"/runs/*/SHA256SUMS
then ok "E1-full-flow (thu tu lenh dung, du luong da don, hash gom 00/11)"; else ko "E1-full-flow log=[$(log)]"; fi
# E2: Cleanup dung run cua phien nay nhung nonce cua phien KHAC dang mo cung ban cai => khong goi close
OTHERN=tl-pw-cccccccccccc
FLOW_ENV= FLOW_BETWEEN="(cd \"\$TL_PW_ROOT/work\" && \"\$TL_PW_NODE\" \"\$TL_PW_CLI\" --session=$OTHERN open about:blank --json >/dev/null); export TL_PW_SESSION=$OTHERN" \
  flow E2 "$SCRATCH/flow_capture.sh" "$SCRATCH/block5.sh"
if ! grep -q "^close" "$CASE_DIR/fakecli.log" && ! grep -qx 'CLEANUP OK' "$CASE_DIR/out" && [ -e "$(BASE)/$H/$OTHERN.err" ] && [ -e "$(BASE)/$H/$OTHERN.session" ]
then ok "E2-run-A-nonce-B (khong goi close/delete-data, phien kia nguyen)"; else ko "E2-run-A-nonce-B log=[$(log)]"; fi
# E3: giua Capture va Cleanup, thu muc hash bi thay bang symlink => dung truoc close
FLOW_BETWEEN="mv \"\$FX_DIR\" \"\$TL_PW_ROOT/real-hash\" && ln -s \"\$TL_PW_ROOT/real-hash\" \"\$FX_DIR\"" flow E3 "$SCRATCH/flow_capture.sh" "$SCRATCH/block5.sh"
n=$(cat "$CASE_DIR/nonce.txt"); if ! grep -q "^close" "$CASE_DIR/fakecli.log" && ! grep -qx 'CLEANUP OK' "$CASE_DIR/out" && [ -e "$CASE_DIR/real-hash/$n.err" ]
then ok "E3-hash-link-between-steps (khong goi close, dich nguyen)"; else ko "E3-hash-link-between-steps log=[$(log)]"; fi
# E4: kiem truoc open dung (CLI o che do workspace) => khong open, khong 00-sophien, Cleanup khong goi close
FLOW_ENV="FX_WS=/somewhere" FLOW_BETWEEN=: flow E4 "$SCRATCH/flow_capture.sh" "$SCRATCH/block5.sh"
if [ ! -e "$CASE_DIR/fakecli.log" ] && grep -q 'KHÔNG chạy Cleanup' "$CASE_DIR/out" && ! ls "$CASE_DIR"/runs/*/00-sophien.txt >/dev/null 2>&1 && ! grep -qx 'CLEANUP OK' "$CASE_DIR/out"
then ok "E4-preflight-stop (khong open, khong 00, Cleanup khong goi close)"; else ko "E4-preflight-stop log=[$(log)]"; fi
# Dot bien toan luong: dua doan dau-cleanup ra SAU 10-verify => E2 phai goi close (bat duoc)
awk '/^  # --- du-luong-daemon-dau-cleanup: bat dau$/{skip=1} skip{buf=buf $0 "\n"} /^  # --- du-luong-daemon-dau-cleanup: het$/{skip=0; next} !skip{ if ($0 == "  # --- du-luong-daemon: bat dau") printf "%s", buf; print }' \
  "$SCRATCH/block5.sh" > "$SCRATCH/mut-block5-dau-late.sh"
cmp -s "$SCRATCH/mut-block5-dau-late.sh" "$SCRATCH/block5.sh" && ko "MUT dau-after-close: khong doi gi"
FLOW_ENV= FLOW_BETWEEN="(cd \"\$TL_PW_ROOT/work\" && \"\$TL_PW_NODE\" \"\$TL_PW_CLI\" --session=$OTHERN open about:blank --json >/dev/null); export TL_PW_SESSION=$OTHERN" \
  flow M-E2 "$SCRATCH/flow_capture.sh" "$SCRATCH/mut-block5-dau-late.sh"
grep -q "^close" "$CASE_DIR/fakecli.log" && ok "MUT dau-after-close -> E2 goi close (chot truoc close co rang)" || ko "MUT dau-after-close -> E2 van khong goi close"

# ===== dot bien: moi chot bi go phai lam ca dich LOT (RESIDUE_OK) =====
mut() { # name target file sed_expr
  local name=$1 target=$2 src=$3 expr=$4 m="$SCRATCH/mut-$1.sh" rc extra=() runner=run_frag
  sed -E "$expr" "$src" > "$m"
  cmp -s "$m" "$src" && { ko "MUT $name: sed khong doi gi"; return; }
  new_case "M-$name"
  case "$target" in
    N2) printf 'dup\n' > "$(BASE)/$H2/$NONCE.err";;
    N3) printf '{}\n' > "$(BASE)/$H/$NONCE.session";;
    N5) rm "$(OWN)"; ln -s "$(BASE)/$H/$OTHER.err" "$(OWN)";;
    N7) mv "$(BASE)" "$CASE_DIR/real-daemon"; ln -s "$CASE_DIR/real-daemon" "$(BASE)";;
    N8) printf 'old\n' > "$CASE_DIR/run/11-daemon.err";;
    N10) extra=(PWTEST_DAEMON_SESSION_DIR=x);;
    N14) mv "$(OWN)" "$(BASE)/$H/${NONCE}Xerr";;
    N15) fake_find;;
    N17) mkdir -p "$CASE_DIR/home/rel"; cp -a "$CASE_DIR/cache" "$CASE_DIR/home/rel/"
         printf 'rel/cache/ms-playwright/daemon\nrel/cache/ms-playwright/daemon/%s\n%s\n' $H $NONCE > "$CASE_DIR/run/00-sophien.txt"
         extra=(FX_BASE=rel/cache/ms-playwright/daemon FX_DIR=rel/cache/ms-playwright/daemon/$H);;
    N18) mv "$(OWN)" "$(BASE)/$H2/";;
    D1) rm "$CASE_DIR/run/00-sophien.txt";;
    D2) extra=(FX_DIR="$(BASE)/$H2");;
    D5) mv "$(BASE)" "$CASE_DIR/real-daemon"; ln -s "$CASE_DIR/real-daemon" "$(BASE)";;
    D7) printf '%s\n%s\n%s\n' "$(BASE)" "$(BASE)/$H" "$OTHER" > "$CASE_DIR/run/00-sophien.txt";;
    C4) runner=run_pre; rm "$CASE_DIR/run/00-sophien.txt" "$(OWN)"; extra=(FX_BASE=rel/d FX_DIR=rel/d/$H);;
    C5) runner=run_pre; rm "$CASE_DIR/run/00-sophien.txt" "$(OWN)"; extra=(PWTEST_DAEMON_SESSION_DIR=x);;
    C7) runner=run_pre; rm "$CASE_DIR/run/00-sophien.txt" "$(OWN)"; fake_find_empty;;
    C9) runner=run_pre; rm "$CASE_DIR/run/00-sophien.txt" "$(OWN)"; mv "$(BASE)" "$CASE_DIR/real-daemon"; ln -s "$CASE_DIR/real-daemon" "$(BASE)";;
    C11) runner=run_pre; rm "$CASE_DIR/run/00-sophien.txt" "$(OWN)"; extra=(FX_DIR="$(BASE)/not-a-hash");;
  esac
  rc=$($runner "$m" "${extra[@]}")
  if is_ok "$rc"; then ok "MUT $name -> $target lot (chot co rang)"; else ko "MUT $name -> $target van chan (chot khong do duoc)"; fi; }
# exact-one: thu tu `find` phu thuoc thu muc, nen thu hai thu tu tao tep; chot co rang neu MOT thu tu lam ca lot
sed -E 's/\[ "\$\{#hit\[@\]\}" -eq 1 \]/[ "${#hit[@]}" -ge 1 ]/' "$F" > "$SCRATCH/mut-exact-one.sh"
if cmp -s "$SCRATCH/mut-exact-one.sh" "$F"; then ko "MUT exact-one: sed khong doi gi"; else lot=0
  for order in session-first session-last; do new_case "M-exact-one-$order"; rm "$(OWN)"; S=$(BASE)/$H/$NONCE.session
    if [ $order = session-first ]; then printf '{}\n' > "$S"; printf 'own\n' > "$(OWN)"; else printf 'own\n' > "$(OWN)"; printf '{}\n' > "$S"; fi
    rc=$(run_frag "$SCRATCH/mut-exact-one.sh"); is_ok "$rc" && lot=1; done
  [ $lot = 1 ] && ok "MUT exact-one -> N3 (mot trong hai thu tu) lot (chot co rang)" || ko "MUT exact-one -> N3 van chan o ca hai thu tu"; fi
mut name-glob N3 "$F" 's/-name "\*\$TL_PW_SESSION\*" -print0/-name "$TL_PW_SESSION.err" -print0/'
mut no-symlink-check N5 "$F" 's/\[ -f "\$f" \] && \[ ! -L "\$f" \]/[ -e "$f" ]/'
mut daemon-symlink N7 "$R" 's/\[ -d "\$D" \] && \[ ! -L "\$D" \]/[ -d "$D" ]/; s/find "\$D" /find -L "$D" /'
mut stale-output N8 "$F" 's/\[ ! -e "\$TL_PW_RUN\/\$ten" \] && \[ ! -L "\$TL_PW_RUN\/\$ten" \]/true/'
mut pwtest-hook N10 "$R" 's/\[ -z "\$\{PWTEST_DAEMON_SESSION_DIR\+x\}" \] \|\|/true ||/'
mut exact-path N14 "$F" 's/\[ "\$f" = "\$DH\/\$TL_PW_SESSION\.err" \]/[[ "${f##*\/}" =~ ^"$TL_PW_SESSION".err$ ]]/'
mut no-scan-rc N15 "$F" 's/wait "\$!" \|\|/true ||/'
mut relative-cache N17 "$F" 's/case "\$D" in \/\*\) ;; \*\) echo/case "$D" in *) ;; \/*) echo/'
mut install-dir-binding N18 "$F" 's/\[ "\$f" = "\$DH\/\$TL_PW_SESSION\.err" \]/[ "${f##*\/}" = "$TL_PW_SESSION.err" ]/'
mut no-capture-record D1 "$DAU" 's/\[ -f "\$TL_PW_RUN\/00-sophien\.txt" \] && \[ ! -L "\$TL_PW_RUN\/00-sophien\.txt" \] &&/true \&\&/; s/\[ "\$\(cat "\$TL_PW_RUN\/00-sophien\.txt"\)" = "\$D"\$.\\n."\$DH"\$.\\n."\$TL_PW_SESSION" \]/true/'
mut no-registry-compare D2 "$DAU" 's/\[ "\$\(cat "\$TL_PW_RUN\/00-sophien\.txt"\)" = "\$D"\$.\\n."\$DH"\$.\\n."\$TL_PW_SESSION" \]/true/'
mut no-nonce-binding D7 "$DAU" 's/\[ "\$\(cat "\$TL_PW_RUN\/00-sophien\.txt"\)" = "\$D"\$.\\n."\$DH"\$.\\n."\$TL_PW_SESSION" \]/[ "$(head -n 2 "$TL_PW_RUN\/00-sophien.txt")" = "$D"$'"'"'\\n'"'"'"$DH" ]/'
mut dau-link D5 "$DAU" 's/\[ -z "\$\{PWTEST_DAEMON_SESSION_DIR\+x\}" \] && \[ -d "\$D" \] && \[ ! -L "\$D" \] && \[ -d "\$DH" \] && \[ ! -L "\$DH" \] \|\|/[ -z "${PWTEST_DAEMON_SESSION_DIR+x}" ] ||/'
mut pre-relative C4 "$P" 's/case "\$D" in \/\*\) ;; \*\) false;; esac/true/'
mut pre-hook C5 "$P" 's/\[ -z "\$\{PWTEST_DAEMON_SESSION_DIR\+x\}" \] &&/true \&\&/'
mut pre-scan-rc C7 "$P" 's/pre=\$\(\[ ! -e "\$D" \] \|\| find (.*) -print\)/pre=$([ ! -e "$D" ] || find \1 -print || true)/'
mut pre-link C9 "$P" 's/\[ ! -L "\$D" \] && \[ ! -L "\$DH" \] &&/true \&\&/'
mut pre-shape C11 "$P" 's/\[\[ "\$\{DH##\*\/\}" =~ \^\[0-9a-f\]\{16\}\$ \]\] &&/true \&\&/'

echo "TONG: $PASS dat / $((PASS+FAIL))"
[ "$FAIL" -eq 0 ]
