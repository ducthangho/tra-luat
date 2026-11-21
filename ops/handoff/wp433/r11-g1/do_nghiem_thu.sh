#!/bin/bash
# Đo nghiệm thu A0–A6 của BUNDLED-GATE-ORACLE-FRESHNESS r5: hai clone (base, C) dựng trong MỘT lệnh, trên đĩa.
# Dùng: do_nghiem_thu.sh <repo> <base_sha> <c_sha> <spec_oid> <thư-mục-ra>
set -u
SRC=$1; A=$2; B=$3; SPEC=$4; OUT=$5
mkdir -p "$OUT/tmp" "$OUT/hv"; export TMPDIR="$OUT/tmp" PYTHONDONTWRITEBYTECODE=1
for f in ma_tran_r11.py doi_chieu_don_dieu.py; do git -C "$SRC" show "$SPEC:ops/reviews/bundled-gate-oracle-spec-r5/$f" > "$OUT/hv/$f"; done
sha256sum "$OUT/hv/"* > "$OUT/hv-bam.txt"
for pair in "nen:$A" "sau:$B"; do
  n=${pair%%:*}; s=${pair#*:}
  git clone -q --no-hardlinks "$SRC" "$OUT/$n" && git -C "$OUT/$n" checkout -q --detach "$s" && git -C "$OUT/$n" config core.abbrev 7
  echo "$n $(git -C "$OUT/$n" rev-parse HEAD) shallow=$(git -C "$OUT/$n" rev-parse --is-shallow-repository) obj358451e8=$(git -C "$OUT/$n" cat-file -t 358451e8 2>&1)"
done > "$OUT/dinh-danh.txt"
chay() { local ten=$1 dir=$2; shift 2; local t0; t0=$(date -u +%FT%TZ)
  (cd "$dir" && "$@") > "$OUT/$ten.out" 2> "$OUT/$ten.err"; echo "$ten | rc=$? | $t0 | $(date -u +%FT%TZ) | $*" >> "$OUT/tong.txt"; }
# A0, A2, A3: ma trận trên cả hai, song song
( chay mt-nen "$OUT/nen" python3 -B "$OUT/hv/ma_tran_r11.py" "$OUT/nen" ) &
( chay mt-sau "$OUT/sau" python3 -B "$OUT/hv/ma_tran_r11.py" "$OUT/sau" ) &
# A4 trên C và base (tuần tự với nhau, song song với ma trận)
(
for n in nen sau; do
  D="$OUT/$n"
  chay $n-selftest "$D" python3 scripts/tl.py --selftest
  chay $n-tfc "$D" python3 scripts/tl.py test-fragments-check --json
  chay $n-bfc "$D" python3 .github/checks/bundle_fragment_check.py --json
  chay $n-rv "$D" python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json
  chay $n-wa "$D" python3 scripts/tl.py workflow-audit --strict --json
  chay $n-golden "$D" python3 scripts/tl.py golden-test --json
  chay $n-eol "$D" python3 .githooks/eol_policy_test.py
  chay $n-ruff "$D" python3 -m ruff check --select F scripts/test_fragments/wp433_bundled_tach_manh.py
  chay $n-doctrine "$D" python3 .claude/dev/packet_loop.py doctrine-scan --root .
  chay $n-adr "$D" python3 .claude/dev/packet_loop.py adr-song --root .
done
D="$OUT/sau"
chay sau-diffcheck "$D" git diff --check "$A" HEAD
chay sau-namestat "$D" git diff --name-only "$A" HEAD
chay sau-numstat "$D" git diff --numstat "$A" HEAD
# A5: chạy lại hai bộ sinh trên C, cây phải sạch
chay sau-sinh-lai "$D" python3 -c "import sys; sys.path.insert(0,'scripts'); from tl_core import test_fragments as tf; tf.write_bundled_modules('scripts/test_fragments','scripts')"
chay sau-manifest-lai "$D" python3 scripts/tl.py release-manifest --out RELEASE_MANIFEST.json
chay sau-status "$D" git status --porcelain
) &
wait
# A6
chay a6 "$OUT" python3 "$OUT/hv/doi_chieu_don_dieu.py" "$OUT/mt-nen.out" "$OUT/mt-sau.out"
echo "XONG $(date -u +%FT%TZ)" >> "$OUT/tong.txt"
