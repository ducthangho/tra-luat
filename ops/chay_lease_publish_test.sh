#!/usr/bin/env bash
# Gom cai `actionlint` va chay lease-publish selftest trong MOT loi goi.
#
# VI SAO. Hai buoc YAML rieng tung cho phep workflow chay bo test tren mot runner
# khong duoc cap cong cu (installer o job khac, nam sau test, hoac bi `if: false`).
# Goi lai `cai_actionlint.sh` o day lam hai hanh vi khong tach roi duoc: installer
# hong thi bo test khong chay; installer xanh thi PATH cua CHINH tien trinh nay duoc
# cap truoc khi bo test chay.
#
# GIOI HAN CO CHU Y. Script nay khong the tu chung minh workflow da goi no. Cau hoi
# do thuoc required status check `PLAT-X5-required-status-check`, khong thuoc mot bo
# test tu kiem van ban YAML cua chinh no.
set -euo pipefail

GOC="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

# Dat dich o wrapper de biet chinh xac thu muc can dua vao PATH trong CUNG loi goi.
# `GITHUB_PATH` chi co hieu luc cho BUOC Actions ke tiep, nen mot wrapper khong duoc
# dua vao no de cap cong cu cho bo test chay ngay sau installer.
AL_DICH="${AL_DICH:-${RUNNER_TEMP:-/tmp}/actionlint}"
export AL_DICH
bash "$GOC/ops/cai_actionlint.sh"

DUONG_ACTIONLINT="$AL_DICH"
if command -v cygpath >/dev/null 2>&1; then
  DUONG_ACTIONLINT="$(cygpath -u "$AL_DICH")"
fi
export PATH="$DUONG_ACTIONLINT:$PATH"

command -v actionlint >/dev/null 2>&1 || {
  printf '%s\n' "chay_lease_publish_test: installer xanh nhung PATH khong co actionlint" >&2
  exit 10
}

# Windows thuong chi co `python`; Linux co the chi co `python3`; launcher cuc bo co
# the chi co `py`. Moi nhanh deu CHAY that, khong co nhanh bo qua duoc dem la dat.
if command -v python >/dev/null 2>&1; then
  PYTHON_LEASE=(python)
elif command -v python3 >/dev/null 2>&1; then
  PYTHON_LEASE=(python3)
elif command -v py >/dev/null 2>&1; then
  PYTHON_LEASE=(py -3)
else
  printf '%s\n' "chay_lease_publish_test: khong tim thay python, python3 hay py" >&2
  exit 11
fi

# PYTHONUNBUFFERED=1 (packet #504 M2, #499 C3): stdout cua buoc CI la ONG nen Python dem KHOI;
# khi job bi huy o tran `timeout-minutes` thi moi thu chua xa mat theo — "DONG IN CUOI CUNG
# != CA CHAY CUOI CUNG". Nhat ky `>>> vao` / `<<< ra` tung ca cua bo test chi dinh vi duoc
# ca dang chay; tat dem Python cho ca cac print khac O DAY, truoc `exec`.
export PYTHONUNBUFFERED=1

# `exec` giu nguyen ma thoat cua bo test; khong pipeline, khong `tail`/`head` nuot rc.
exec "${PYTHON_LEASE[@]}" "$GOC/ops/lease_publish_test.py"
