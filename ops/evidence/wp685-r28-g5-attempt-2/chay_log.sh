#!/usr/bin/env bash
# wp685 r28 g5 attempt 2. Dung: chay_log.sh <tep log> <cay do (cwd)> <python3.1x> -- <lenh...>
# Khoi moi truong r28 (o `environment`, (a)-(d)) DUNG DAU log theo dang khoi r22, roi DANH TINH cua CHINH cay do:
# `git rev-parse HEAD HEAD^{tree}` va `git status --porcelain` (truoc VA sau lenh), sha256 hai tep write set, lenh
# nguyen van, gio UTC, rc. Khong sua log sau khi ghi.
LOG=$1; CWD=$2; PYV=$3; shift 4
{
  echo "# UTC $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  for c in "uname -s" "uname -r" "uname -m" "cat /etc/os-release" "python3.11 -V" "python3.12 -V" "uname -a"; do
    echo "\$ $c"; $c 2>&1; echo "# rc=$?"
  done
  echo "# cwd: $CWD"
  echo "\$ git rev-parse HEAD HEAD^{tree}"; git -C "$CWD" rev-parse HEAD 'HEAD^{tree}' 2>&1; echo "# rc=$?"
  echo "\$ git status --porcelain"; git -C "$CWD" status --porcelain 2>&1; echo "# rc=$?"
  echo "\$ sha256sum .claude/dev/launcher.py .claude/dev/launcher_test.py"; (cd "$CWD" && sha256sum .claude/dev/launcher.py .claude/dev/launcher_test.py 2>&1)
  echo "# lenh: $*"
  echo "# runtime: $($PYV -V 2>&1) ($(command -v $PYV))"
  echo "# bat dau UTC $(date -u +%Y-%m-%dT%H:%M:%SZ)"
} > "$LOG"
( cd "$CWD" && PYTHONDONTWRITEBYTECODE=1 "$@" ) >> "$LOG" 2>&1 < /dev/null
RC=$?
{
  echo "# ket thuc UTC $(date -u +%Y-%m-%dT%H:%M:%SZ) rc=$RC"
  echo "# sau lenh: git rev-parse HEAD HEAD^{tree} = $(git -C "$CWD" rev-parse HEAD 'HEAD^{tree}' | tr '\n' ' ')"
  echo "# sau lenh: git status --porcelain = [$(git -C "$CWD" status --porcelain | tr '\n' ';')]"
} >> "$LOG"
exit $RC
