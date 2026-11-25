#!/usr/bin/env bash
# Đo vùng PR2 (wp1463) trong MỘT lệnh trên một SHA master: phan_chung() (3 bản nạp) + lượt day_du của bộ (bo_day_du).
# Dùng: bash do_vung_pr2.sh <SHA> <thu_muc_ra> [đường_dẫn_thêm_vào_Z ...]
# Không ghi gì vào kho làm việc; clone riêng từ GitHub, core.abbrev 7.
set -euo pipefail
SHA="$1"; OUT="$(mkdir -p "$2" && cd "$2" && pwd)"; shift 2
HERE="$(cd "$(dirname "$0")" && pwd)"
command -v actionlint >/dev/null && command -v shellcheck >/dev/null || { echo "KHÔNG ĐO ĐƯỢC: thiếu actionlint/shellcheck"; exit 3; }
CL="$OUT/kho"
git clone -q https://github.com/ducthangho/tra-luat.git "$CL"
git -C "$CL" checkout -q "$SHA"; git -C "$CL" config core.abbrev 7
git -C "$CL" ls-files -z | tr '\0' '\n' | sort > "$OUT/tracked"
echo "SHA $(git -C "$CL" rev-parse HEAD)" | tee "$OUT/KET_QUA.txt"
for mo in nguyen bon go; do
  echo "== phan_chung $mo" | tee -a "$OUT/KET_QUA.txt"
  python3 -B "$HERE/probe_pc.py" "$CL" "$mo" "$OUT/tracked" "$@" 2>&1 | tee -a "$OUT/KET_QUA.txt"
done
echo "== bo_day_du" | tee -a "$OUT/KET_QUA.txt"
: > "$OUT/open.log"
t0=$(date +%s)
set +e
( cd "$CL" && PYTHONPATH="$HERE/hook" AUDIT_OPEN_LOG="$OUT/open.log" python3 -B ops/ci_provenance_test.py ) > "$OUT/day_du.out" 2>&1
rc=$?; set -e
echo "rc $rc wall $(( $(date +%s)-t0 ))s cpu $(nproc)" | tee -a "$OUT/KET_QUA.txt"
tail -5 "$OUT/day_du.out" | tee -a "$OUT/KET_QUA.txt"
sed "s#^$CL/##" "$OUT/open.log" | sort -u > "$OUT/opened"
comm -12 "$OUT/tracked" "$OUT/opened" > "$OUT/bo_day_du.set"
python3 -B "$HERE/probe_pc.py" --oracle "$OUT/bo_day_du.set" "$@" | tee -a "$OUT/KET_QUA.txt"
