#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
root=$PWD
export GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL="$root/rv/offline-git.config"
export GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file PYTHONDONTWRITEBYTECODE=1 TMPDIR="$root/rv/tmp"
date -u +%FT%TZ > rv/log/cleanup.start
python3 -B rv/clean-probe-output.py > rv/log/cleanup.out
date -u +%FT%TZ > rv/log/cleanup.end
date -u +%FT%TZ > rv/log/final-snapshot.start
(
    cd rv/sau
    python3 -c "import sys; sys.path.insert(0,'scripts'); from tl_core import test_fragments as tf; tf.write_bundled_modules('scripts/test_fragments', 'scripts')"
    git diff --exit-code -- scripts/tl_test_fragments_bundled.py scripts/tl_test_fragments_bundled_2.py
    python3 scripts/tl.py release-manifest --out RELEASE_MANIFEST.json > "$root/rv/log/manifest-final.out"
    git diff --exit-code -- RELEASE_MANIFEST.json
    git status --porcelain=v1
) > rv/log/regenerate-final.out
bash rv/check-snapshot.sh > rv/log/final-snapshot.out
date -u +%FT%TZ > rv/log/final-snapshot.end
