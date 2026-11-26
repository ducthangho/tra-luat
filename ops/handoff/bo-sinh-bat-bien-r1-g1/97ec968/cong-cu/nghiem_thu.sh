#!/usr/bin/env bash
# Nghiệm thu mục 5 (bước 1-6) của đặc tả bo-sinh-bat-bien r1: hai vế (nen = base, sau = head) dựng và chạy trong CÙNG một lệnh.
set -u
S="$1"; RA="$2"; mkdir -p "$RA"
export PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1
chay() {  # chay <ve> <nhan> <lenh...>
  local ve="$1" nhan="$2"; shift 2
  local t0 t1 rc
  t0=$(date +%s.%N)
  ( cd "$S/$ve" && "$@" ) > "$RA/$ve-$nhan.log" 2>&1; rc=$?
  t1=$(date +%s.%N)
  printf '%s | %s | rc=%s | %.1fs | %s\n' "$ve" "$nhan" "$rc" "$(echo "$t1 - $t0" | bc)" "$(tail -n 4 "$RA/$ve-$nhan.log" | tr '\n' '~' | cut -c1-260)"
}
PHA="${3:-thoi-gian}"
for ve in nen sau; do
  echo "== $ve $(git -C "$S/$ve" rev-parse HEAD) tree=$(git -C "$S/$ve" rev-parse 'HEAD^{tree}') ban=$(git -C "$S/$ve" status --porcelain | wc -l) shallow=$(git -C "$S/$ve" rev-parse --is-shallow-repository)"
done
if [ "$PHA" = thoi-gian ]; then   # hai bo test co tran thoi gian: xen ke nen/sau, khong chay gi khac cung luc
  for mau in 1 2; do   # HAI mau moi ve (dieu phoi yeu cau sau review luot 2), tuan tu, xen ke nen/sau
    for t in "test-b ops/land_evidence_nguon_test.py" "test-a ops/gate_output_doi_chieu_test.py"; do
      for ve in nen sau; do chay "$ve" "${t%% *}-mau$mau" python3 -B "${t##* }"; done
    done
  done
else
  for ve in nen sau; do
    chay "$ve" land-evidence python3 -B ops/land_evidence_nguon.py --root .
    chay "$ve" ci-dang-ky python3 -B .claude/dev/ci_dang_ky_test.py
    chay "$ve" selftest python3 scripts/tl.py --selftest
    chay "$ve" ruff python3 -m ruff check --select F ops/land_evidence_nguon_test.py ops/gate_output_doi_chieu_test.py
  done
fi
for ve in nen sau; do echo "   $ve ban sau khi chay: $(git -C "$S/$ve" status --porcelain | wc -l)"; done
echo "XONG TRON VEN $PHA"
