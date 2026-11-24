#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file
for repo in kho rv/nen rv/sau; do
    echo "[$repo]"
    git -C "$repo" rev-parse HEAD HEAD^{tree}
    git -C "$repo" diff --exit-code
    git -C "$repo" diff --cached --exit-code
    state=$(git -C "$repo" status --porcelain=v1 --untracked-files=all --ignored)
    test -z "$state" || printf '%s\n' "$state"
    test -z "$state"
    sha256sum "$repo/scripts/test_fragments/wp433_bundled_tach_manh.py" \
              "$repo/scripts/tl_test_fragments_bundled.py" \
              "$repo/scripts/tl_test_fragments_bundled_2.py" \
              "$repo/RELEASE_MANIFEST.json"
done
cmp kho/scripts/test_fragments/wp433_bundled_tach_manh.py rv/sau/scripts/test_fragments/wp433_bundled_tach_manh.py
cmp kho/scripts/tl_test_fragments_bundled.py rv/sau/scripts/tl_test_fragments_bundled.py
cmp kho/scripts/tl_test_fragments_bundled_2.py rv/sau/scripts/tl_test_fragments_bundled_2.py
cmp kho/RELEASE_MANIFEST.json rv/sau/RELEASE_MANIFEST.json
