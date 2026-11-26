#!/usr/bin/env bash
# Luật 9 (mục 5 bước 8 của đặc tả): bộ quét ghim `do` cho hai cặp module/test, trên nen (base) và sau (head).
set -u
S="$1"; RA="$2"; SS="${3:-3}"
export PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1
Q=ops/reviews/wp1236-r10-soan/quet_dot_bien.py
for cap in "B ops/land_evidence_nguon.py ops/land_evidence_nguon_test.py $RA/kho_rong.jsonl" "A ops/gate_output_doi_chieu.py ops/gate_output_doi_chieu_test.py $RA/kho_A.jsonl"; do
  set -- $cap
  for ve in sau nen; do
    D="$RA/$1-$ve"; mkdir -p "$D"
    t0=$(date -u +%FT%TZ)
    ( cd "$S/$ve" && sha256sum "$Q" "$2" "$3" "$4" && python3 "$Q" do "$2" "$3" "$4" --thu-muc-ra "$D" --song-song "$SS" ) > "$D/do.log" 2>&1
    echo "$1 $ve rc=$? $t0 -> $(date -u +%FT%TZ) | $(grep -E '^TONG ' "$D/do.log") | $(grep -c '^HOAN_TAT' "$D/do.log") HOAN_TAT | ban=$(git -C "$S/$ve" status --porcelain | wc -l)"
  done
done
echo "XONG TRON VEN luat9"
