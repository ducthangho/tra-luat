#!/bin/bash
# N4: ap fragment secrets-set + tl_gws.py cua r8 len head, tai sinh bundled, do. Khong commit.
set -u
SRC=$1; H=$2; R8=$3; OUT=$4
rm -rf "$OUT"; mkdir -p "$OUT/tmp"; export TMPDIR="$OUT/tmp" PYTHONDONTWRITEBYTECODE=1
git clone -q --no-hardlinks "$SRC" "$OUT/r" && cd "$OUT/r" && git checkout -q --detach "$H" && git config core.abbrev 7
git -C "$SRC" show "$R8:scripts/test_fragments/wp433_secrets_set_bundle.py" > scripts/test_fragments/wp433_secrets_set_bundle.py
git -C "$SRC" show "$R8:scripts/tl_gws.py" > scripts/tl_gws.py
python -c "
import sys; sys.path.insert(0,'scripts')
from tl_core import test_fragments as tf
print(tf.write_bundled_modules('scripts/test_fragments','scripts'))"; echo "write rc=$?"
wc -c scripts/tl_test_fragments_bundled*.py
python scripts/tl.py release-manifest --out RELEASE_MANIFEST.json > "$OUT/manifest.out" 2>&1; echo "manifest rc=$?"
python scripts/tl.py test-fragments-check --json > "$OUT/tfc.out" 2>"$OUT/tfc.err"; echo "tfc rc=$? $(date -u +%FT%TZ)"
python scripts/tl.py workflow-audit --strict --json > "$OUT/wa.out" 2>"$OUT/wa.err"; echo "wa rc=$?"
python scripts/tl.py --selftest > "$OUT/selftest.out" 2>"$OUT/selftest.err"; echo "selftest rc=$? $(date -u +%FT%TZ)"
git status --short
echo XONG
