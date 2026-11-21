#!/usr/bin/env bash
# Gate N1-N5 (SECRETS-SET-BUNDLE-KIEU r5 §4) — hai clone dựng trong MỘT lệnh, mọi phép so ghim hai OID đầy đủ.
# bash gate_n5.sh <nguon_clone> <BASE_SHA> <CAND_SHA> <thu_muc_ra> <thu_muc_handoff>
set -u
SRC="$1"; B="$2"; H="$3"; RA="$4"; HO="$5"
mkdir -p "$RA"; cd "$RA" || exit 9
for pair in "nen:$B" "sau:$H"; do n="${pair%%:*}"; s="${pair#*:}"
  git clone -q --no-local "$SRC" "$RA/$n" && git -C "$RA/$n" -c advice.detachedHead=false checkout -q "$s" && git -C "$RA/$n" config core.abbrev 7 \
  && git -C "$RA/$n" config core.autocrlf false && git -C "$RA/$n" config core.eol lf; done
log(){ printf '%s %s\n' "$(date -u +%FT%TZ)" "$*" | tee -a "$RA/gate.log"; }
log "nen=$(git -C nen rev-parse HEAD) sau=$(git -C sau rev-parse HEAD) shallow=$(git -C sau rev-parse --is-shallow-repository) gitdir_la_thu_muc=$([ -d sau/.git ] && echo 1)"
export PYTHONDONTWRITEBYTECODE=1
for n in nen sau; do (
  cd "$RA/$n" || exit 9; T="$RA/tmp-$n"; mkdir -p "$T/home"; export HOME="$T/home" TMPDIR="$T"
  python3 scripts/tl.py --selftest > "$RA/$n.selftest.txt" 2>&1; echo "rc=$?" >> "$RA/$n.selftest.txt"
  python3 scripts/tl.py test-fragments-check --json > "$RA/$n.tfc.json" 2>"$RA/$n.tfc.err"; echo "rc=$?" > "$RA/$n.tfc.rc"
  python3 .github/checks/bundle_fragment_check.py --json > "$RA/$n.bfc.json" 2>"$RA/$n.bfc.err"; echo "rc=$?" > "$RA/$n.bfc.rc"
  python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json > "$RA/$n.rv.json" 2>&1; echo "rc=$?" > "$RA/$n.rv.rc"
  python3 scripts/tl.py workflow-audit --strict --json > "$RA/$n.wa.json" 2>&1; echo "rc=$?" > "$RA/$n.wa.rc"
  python3 scripts/tl.py golden-test --json > "$RA/$n.golden.json" 2>&1; echo "rc=$?" > "$RA/$n.golden.rc"
  python3 .githooks/eol_policy_test.py > "$RA/$n.eol.txt" 2>&1; echo "rc=$?" >> "$RA/$n.eol.txt"
  python3 .claude/dev/packet_loop.py doctrine-scan --root . > "$RA/$n.doctrine.txt" 2>&1; echo "rc=$?" >> "$RA/$n.doctrine.txt"
  python3 .claude/dev/packet_loop.py adr-song --root . > "$RA/$n.adr.txt" 2>&1; echo "rc=$?" >> "$RA/$n.adr.txt"
  for f in scripts/tl.py scripts/tl_gws.py scripts/tl_test_fragments_bundled.py scripts/tl_test_fragments_bundled_2.py scripts/tl_selftest.py; do
    printf '%s %s\n' "$f" "$(python3 -m ruff check --select F --output-format concise "$f" 2>/dev/null | grep -c ': F')"; done > "$RA/$n.ruff.txt"
  python3 -m ruff check --select F scripts/test_fragments/ > "$RA/$n.ruff_frag.txt" 2>&1; echo "rc=$?" >> "$RA/$n.ruff_frag.txt"
  python3 - > "$RA/$n.wp433.txt" 2>&1 <<'PY'
import glob, importlib.util, os, sys
sys.path.insert(0, "scripts"); import tl
for p in sorted(glob.glob("scripts/test_fragments/wp433_*.py")):
    sp = importlib.util.spec_from_file_location(os.path.basename(p)[:-3], p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    print("FRAG", os.path.basename(p), m.run(tl), flush=True)
PY
  echo "rc=$?" >> "$RA/$n.wp433.txt"
) & done; wait
log "selftest nen: $(tail -2 "$RA/nen.selftest.txt" | tr '\n' ' ')"
log "selftest sau: $(tail -2 "$RA/sau.selftest.txt" | tr '\n' ' ')"
git -C "$RA/sau" diff --check "$B" "$H"; log "diff --check $B $H rc=$?"
git -C "$RA/sau" diff --numstat "$B" "$H" > "$RA/numstat.txt"; log "numstat $B $H: $(awk '{a+=$1;d+=$2;n++} END{print n" tep +"a"/-"d}' "$RA/numstat.txt")"
git -C "$RA/sau" diff --name-only "$B" "$H" > "$RA/duong.txt"
git -C "$RA/sau" show "$B:scripts/tl_gws.py" > "$RA/tl_gws_base.py"
( cd "$RA/sau" && WP433_SS_BAN_DO="$RA/ban_do_ung_vien.json" python3 -c "
import sys; sys.path.insert(0,'scripts'); import tl, importlib.util
sp=importlib.util.spec_from_file_location('f','scripts/test_fragments/wp433_secrets_set_bundle.py'); f=importlib.util.module_from_spec(sp); sp.loader.exec_module(f)
print('RUN_UNG_VIEN', f.run(tl))" ) > "$RA/n123_ung_vien.txt" 2>&1; log "n123 ung vien: $(grep RUN_ "$RA/n123_ung_vien.txt")"
python3 -B "$HO/rig_n4.py" "$RA/sau" "$HO/ma-tran-n4.json" "$RA/n4" "$RA/tl_gws_base.py" > "$RA/n4.txt" 2>&1; log "N4 rc=$? $(tail -1 "$RA/n4.txt")"
log XONG
