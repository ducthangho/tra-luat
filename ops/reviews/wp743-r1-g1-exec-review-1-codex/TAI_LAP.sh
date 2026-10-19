#!/usr/bin/env bash
# Tai lap hai cay tam ma cac driver cua reviewer (evidence/reviewer/{measure,semantics,pid_collision}.py) doc CUNG:
#   /tmp/review743-head  = commit 80e0fac0a4ab8c74486cf3bab1a73e1dec600994 (head da review)
#   /tmp/review743-base  = commit 9fddb1d19e8e5b753bb687673846d484fb710182 (nen)
# Driver la hien vat NGUYEN BYTE cua luot review (SHA256SUMS) nen KHONG sua; script nay dung lai dung dau vao cua no.
# Reviewer dung `cp -a` mot clone thuong cho head va `git archive` cho base; o day ca hai la clone thuong (`.git` la THU
# MUC) de tranh bay worktree ma CLAUDE.md da ghi. Ton tai san thi DUNG, khong ghi de.
#
# Dung:  bash TAI_LAP.sh [url-kho]   roi, tu thu muc evidence/reviewer:
#   PYTHONDONTWRITEBYTECODE=1 python3.13 -B semantics.py
#   PYTHONDONTWRITEBYTECODE=1 python3.13 -B measure.py
#   PYTHONDONTWRITEBYTECODE=1 python3.13 -B pid_collision.py 10
set -euo pipefail
KHO="${1:-https://github.com/ducthangho/tra-luat.git}"
for cap in "head:80e0fac0a4ab8c74486cf3bab1a73e1dec600994" "base:9fddb1d19e8e5b753bb687673846d484fb710182"; do
  ten="${cap%%:*}"; sha="${cap#*:}"; dich="/tmp/review743-$ten"
  if [ -e "$dich" ]; then echo "DUNG: $dich da ton tai — xoa tay neu muon dung lai" >&2; exit 2; fi
  git clone -q "$KHO" "$dich"
  git -C "$dich" checkout -q --detach "$sha"
  git -C "$dich" config core.abbrev 7
  test "$(git -C "$dich" rev-parse HEAD)" = "$sha"
  echo "OK $ten $sha -> $dich"
done
