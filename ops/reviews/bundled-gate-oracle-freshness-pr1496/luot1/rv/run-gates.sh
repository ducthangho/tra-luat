#!/usr/bin/env bash
set -u
cd "$(dirname "$0")/.."
root=$PWD
export PYTHONDONTWRITEBYTECODE=1 TMPDIR="$root/rv/tmp" GIT_ALLOW_PROTOCOL=file
export GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL="$root/rv/offline-git.config"
export RUFF_CACHE_DIR="$root/rv/tmp/ruff-cache"
: > "$root/rv/log/gates.tsv"
run() {
    local lane=$1 name=$2 start end rc=0
    shift 2
    start=$(date -u +%FT%TZ)
    (cd "$root/rv/$lane" && "$@") > "$root/rv/log/$lane-$name.out" 2>&1 || rc=$?
    end=$(date -u +%FT%TZ)
    printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$lane" "$name" "$rc" "$start" "$end" "$*" >> "$root/rv/log/gates.tsv"
}
gates() {
    local lane=$1
    run "$lane" selftest python3 scripts/tl.py --selftest
    run "$lane" fragments python3 scripts/tl.py test-fragments-check --json
    run "$lane" bundle python3 .github/checks/bundle_fragment_check.py --json
    run "$lane" verify python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json
    run "$lane" workflow python3 scripts/tl.py workflow-audit --strict --json
    run "$lane" golden python3 scripts/tl.py golden-test --json
    run "$lane" eol python3 .githooks/eol_policy_test.py
    run "$lane" ruff-version python3 -m ruff --version
    run "$lane" ruff python3 -m ruff check --no-cache --select F scripts/test_fragments/wp433_bundled_tach_manh.py
    run "$lane" doctrine python3 .claude/dev/packet_loop.py doctrine-scan --root .
    run "$lane" adr python3 .claude/dev/packet_loop.py adr-song --root .
}
gates nen &
base_pid=$!
gates sau &
candidate_pid=$!
wait "$base_pid"
wait "$candidate_pid"
run sau diffcheck git diff --check e2f28fb39c519511a61d1fdba5b1fc8f77bb76b8 HEAD
run sau names git diff --name-only e2f28fb39c519511a61d1fdba5b1fc8f77bb76b8 HEAD
run sau regen-bundle python3 -c "import sys; sys.path.insert(0,'scripts'); from tl_core import test_fragments as tf; tf.write_bundled_modules('scripts/test_fragments', 'scripts')"
run sau regen-bundle-diff git diff --exit-code -- scripts/tl_test_fragments_bundled.py scripts/tl_test_fragments_bundled_2.py
run sau regen-manifest python3 scripts/tl.py release-manifest --out RELEASE_MANIFEST.json
run sau status git status --porcelain=v1 --untracked-files=all --ignored
