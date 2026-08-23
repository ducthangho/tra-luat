#!/usr/bin/env bash
# ops/cai_cong_cu.sh <ten> — doc ops/cong_cu.yaml (G1), cai roi DO LAI bang cong_cu.py,
# KHONG tin rc trinh cai (r244). Giu 2 tinh chat cua cai_actionlint.sh: ban ghim o MOT noi
# (YAML) · KHONG `command -v` roi thoat som (T5). `cai.lenh` PHAI in duong dan vua cai lam
# DONG CUOI stdout de dua vao PATH truoc buoc DO LAI; khong in duong dan (vd pip) thi
# `[ -d ]` tra sai an toan.
set -euo pipefail
GOC="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd -- "$GOC"  # cong thuc YAML la duong dan TUONG DOI; doc lap CWD nguoi goi
TEN="${1:-}"
[ -n "$TEN" ] || { echo "cai_cong_cu: thieu ten cong cu (vi du: actionlint)" >&2; exit 2; }
# Windows thuong chi co `python`; Linux/macOS co the chi co `python3` (CLAUDE.md).
if command -v python >/dev/null 2>&1; then PY=(python)
elif command -v python3 >/dev/null 2>&1; then PY=(python3)
elif command -v py >/dev/null 2>&1; then PY=(py -3)
else echo "cai_cong_cu: khong tim thay python, python3 hay py" >&2; exit 4
fi
DAU_RA="$("${PY[@]}" "$GOC/ops/cong_cu.py" cai-lenh "$TEN")" || {
  echo "cai_cong_cu: '$TEN' khong co cong thuc cai tu dong cho nen nay" >&2
  exit 3
}
LENH="$(printf '%s\n' "$DAU_RA" | head -1)"
while IFS= read -r dong; do
  case "$dong" in *=*) export "${dong?}" ;; esac
done < <(printf '%s\n' "$DAU_RA" | tail -n +2)

# eval TREN LENH doc tu ban ke cua CHINH kho — khong phai dau vao nguoi dung/mang ngoai.
KET_QUA_CAI="$(eval "$LENH")"
DICH="$(printf '%s\n' "$KET_QUA_CAI" | tail -1)"
[ -d "$DICH" ] && export PATH="$DICH:$PATH"

"${PY[@]}" "$GOC/ops/cong_cu.py" kiem-tra --chi "$TEN" --json
