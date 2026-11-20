#!/bin/bash
# Dung HAI clone (nen/sau) trong MOT lenh roi do. Dung: do.sh <repo-nguon> <sha-base> <sha-head> <thu-muc-ra>
set -u
SRC=$1; A=$2; B=$3; OUT=$4
rm -rf "$OUT"; mkdir -p "$OUT/tmp"
export TMPDIR="$OUT/tmp" PYTHONDONTWRITEBYTECODE=1
for pair in "nen:$A" "sau:$B"; do
  n=${pair%%:*}; s=${pair#*:}
  git clone -q --no-hardlinks "$SRC" "$OUT/$n" && git -C "$OUT/$n" checkout -q --detach "$s" && git -C "$OUT/$n" config core.abbrev 7
  echo "$n $(git -C "$OUT/$n" rev-parse HEAD) shallow=$(git -C "$OUT/$n" rev-parse --is-shallow-repository)"
done > "$OUT/dinh-danh.txt"
chay() { # ten thu-muc lenh...
  local ten=$1 dir=$2; shift 2
  local t0; t0=$(date -u +%FT%TZ)
  (cd "$dir" && "$@") > "$OUT/$ten.out" 2> "$OUT/$ten.err"; local rc=$?
  echo "$ten | rc=$rc | $t0 | $*" >> "$OUT/tong.txt"
}
RUFF="scripts/tl.py scripts/tl_core/test_fragments.py scripts/tl_core/release.py scripts/tl_selftest.py .githooks/eol_policy_test.py"
for n in nen sau; do
  D="$OUT/$n"
  chay $n-eol "$D" python .githooks/eol_policy_test.py
  chay $n-selftest-worker "$D" python scripts/tl.py --selftest
  chay $n-ruff "$D" python -m ruff check --select F --statistics $RUFF
  if [ $n = sau ]; then
    chay $n-ruff-frag "$D" python -m ruff check --select F scripts/test_fragments/wp433_bundled_tach_manh.py
    chay $n-manifest "$D" python scripts/tl.py release-manifest --out RELEASE_MANIFEST.json
    chay $n-selftest-m8 "$D" python scripts/tl.py --selftest
    chay $n-rv "$D" python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json
    chay $n-manifest-diff "$D" git diff --numstat
  fi
  chay $n-tfc "$D" python scripts/tl.py test-fragments-check --json
  chay $n-bfc "$D" python .github/checks/bundle_fragment_check.py --json
  chay $n-wa "$D" python scripts/tl.py workflow-audit --strict --json
  chay $n-golden "$D" python scripts/tl.py golden-test --json
  chay $n-diffcheck "$D" git diff --check "$A" HEAD
  chay $n-doctrine "$D" python .claude/dev/packet_loop.py doctrine-scan --root .
  chay $n-adr "$D" python .claude/dev/packet_loop.py adr-song --root .
  chay $n-status "$D" git status --short
done
echo XONG >> "$OUT/tong.txt"
