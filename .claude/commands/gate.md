---
description: Full gate T3/T5 hoặc fallback — 8 bước tuần tự, một heavy gate/host, evidence JSON từng lệnh và rc thật
---

Chạy FULL GATE của tra-luat theo §6.5 kế hoạch guard-va-boc-tl-core. Đây là gate cho T3/T5 hoặc fallback
fail-closed, **không** phải lệnh mặc định sau mỗi edit. T0–T2 dùng `/gate-targeted`; nếu CI đã có full evidence
trên đúng exact identity thì Reviewer validate/reuse evidence thay vì lặp lại cùng full local.

**BẮT BUỘC kiểm rc THẬT của TỪNG lệnh** — sự cố cũ: `cmd | python -c ...` làm rc của cmd bị pipe NUỐT →
commit lọt khi gate ĐỎ. Mỗi gate ghi output ra FILE rồi mới parse; rc lấy từ chính lệnh, không qua pipe.
Mọi lệnh dưới đây đi qua `gate_lifecycle.py`, nên trên một physical host không có hai heavy gate chạy đồng thời;
duration, exact identity và rc được ghi ở `scripts/.tl_state/gate/*.json`.

Chạy đúng script này bằng Bash tool (1 call), làm việc tại repo tra-luat:

```bash
cd /c/qh/tra-luat && P=/c/Python313/python
mkdir -p scripts/.tl_state/gate
BASE_SHA=$(git merge-base origin/master HEAD 2>/dev/null || git rev-parse HEAD)
HEAD_SHA=$(git rev-parse HEAD)
declare -A RC
g() {
  local n="$1" positive="$2"; shift 2
  $P .claude/dev/gate_lifecycle.py run \
    --kind heavy --name "$n" --repo . \
    --evidence "scripts/.tl_state/gate/${n}.json" \
    --output "scripts/.tl_state/gate/${n}.out" \
    --expected-head "$HEAD_SHA" --base-sha "$BASE_SHA" --require-clean \
    --selected-test "$n" \
    --wait-seconds 900 --timeout-seconds 1200 --positive-regex "$positive" --quiet -- "$@"
  RC[$n]=$?
}

g selftest      '(?m)^.*\b([1-9][0-9]*)/\1\b[^\r\n]*\r?\n?\Z' $P scripts/tl.py --selftest
g gen_inst      '(?m)^.*\b([1-9][0-9]*)/\1\b[^\r\n]*\r?\n?\Z' $P scripts/gen_instructions.py --selftest
g workflow      '"ok"\s*:\s*true' $P scripts/tl.py workflow-audit --strict --json
g golden        '"ok"\s*:\s*true' $P scripts/tl.py golden-test --json          # KHÔNG BAO GIỜ --write ở đây (R6)
g docclaims     '"ok"\s*:\s*true' $P scripts/tl.py doc-claims-check --strict --json   # r219 nối vào (r218 làm lệnh mà QUÊN nối)
g determinism   '"ok"\s*:\s*true' $P scripts/tl.py determinism-audit --strict --json
g relcheck      '"ok"\s*:\s*true' $P scripts/tl.py release-check --full --json
g relverify     '"ok"\s*:\s*true' $P scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json

FAIL=0
for n in selftest gen_inst workflow golden docclaims determinism relcheck relverify; do
  ok="rc=${RC[$n]}"
  extra=""
  case "$n" in
    selftest)  extra=$(tail -1 "scripts/.tl_state/gate/${n}.out") ;;
    gen_inst)  extra=$(tail -1 "scripts/.tl_state/gate/${n}.out") ;;
    *)         extra=$(grep -o '"ok": *\(true\|false\)' "scripts/.tl_state/gate/${n}.out" | head -1) ;;
  esac
  if [ "${RC[$n]}" -ne 0 ]; then FAIL=1; verdict="FAIL"; else
    case "$n" in
      selftest|gen_inst) echo "$extra" | grep -qE '([0-9]+)/\1' && verdict="PASS" || { verdict="FAIL"; FAIL=1; } ;;
      *) echo "$extra" | grep -q '"ok": *true' && verdict="PASS" || { verdict="FAIL"; FAIL=1; } ;;
    esac
  fi
  printf '  [%s] %-12s %s %s\n' "$verdict" "$n" "$ok" "$extra"
done
[ $FAIL -eq 0 ] && echo "== GATE XANH TRỌN ==" || echo "== GATE ĐỎ — DỪNG, không commit/release (soi scripts/.tl_state/gate/*.out) =="
exit $FAIL
```

Sau khi chạy: báo bảng PASS/FAIL từng gate. Gate ĐỎ → DỪNG NGAY (không commit, không release, không
`golden-test --write` — golden diff = BUG của thay đổi, theo R6). Output dài cần đào sâu → giao agent
`tl-auditor` tiêu hoá file trong `scripts/.tl_state/gate/`, phiên chính chỉ nhận kết luận.
