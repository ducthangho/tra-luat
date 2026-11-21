#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export PYTHONDONTWRITEBYTECODE=1 TMPDIR="$PWD/rv/tmp" GIT_ALLOW_PROTOCOL=file
base=e2f28fb39c519511a61d1fdba5b1fc8f77bb76b8
candidate=4f648e5b784aa4e19f0385eee68cd75e69e1dd18
date -u +%FT%TZ
git -c core.hooksPath=/dev/null clone --quiet --no-hardlinks ./kho rv/nen
git -C rv/nen config core.abbrev 7
git -C rv/nen -c core.hooksPath=/dev/null checkout --quiet --detach "$base"
git -c core.hooksPath=/dev/null clone --quiet --no-hardlinks ./kho rv/sau
git -C rv/sau config core.abbrev 7
git -C rv/sau -c core.hooksPath=/dev/null checkout --quiet --detach "$candidate"
for lane in nen sau; do
    git -C "rv/$lane" rev-parse HEAD HEAD^{tree}
    test "$(git -C "rv/$lane" rev-parse --is-shallow-repository)" = false
    git -C "rv/$lane" cat-file -t 358451e8
    git -C "rv/$lane" config --get core.abbrev
    test -z "$(git -C "rv/$lane" status --porcelain)"
done
date -u +%FT%TZ
touch rv/log/clones.ready
matrix() {
    local lane=$1 rc=0
    date -u +%FT%TZ > "rv/log/matrix-$lane.start"
    python3 -u -B rv/spec/ma_tran_r11.py "rv/$lane" > "rv/log/matrix-$lane.out" 2>&1 || rc=$?
    date -u +%FT%TZ > "rv/log/matrix-$lane.end"
    printf '%s\n' "$rc" > "rv/log/matrix-$lane.rc"
}
matrix nen &
base_pid=$!
matrix sau &
candidate_pid=$!
wait "$base_pid"
wait "$candidate_pid"
date -u +%FT%TZ > rv/log/a6.start
rc=0
python3 -B rv/spec/doi_chieu_don_dieu.py rv/log/matrix-nen.out rv/log/matrix-sau.out > rv/log/a6.out 2>&1 || rc=$?
date -u +%FT%TZ > rv/log/a6.end
printf '%s\n' "$rc" > rv/log/a6.rc
exit "$rc"
