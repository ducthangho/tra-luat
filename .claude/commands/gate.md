---
description: Full-gate offline 8 bước (selftest + gen_instructions + 3 audit strict + doc-claims-check + golden 0-diff + release-check/verify) — kiểm rc THẬT từng lệnh, pipefail-ĐÚNG, không tin "ok: true" trôi qua pipe
---

Chạy FULL GATE của tra-luat theo §6.5 kế hoạch guard-va-boc-tl-core. **BẮT BUỘC kiểm rc THẬT của TỪNG
lệnh** — sự cố cũ: `cmd | python -c ...` làm rc của cmd bị pipe NUỐT → commit lọt khi gate ĐỎ. Vì vậy:
mỗi gate ghi output ra FILE rồi mới parse; rc lấy từ chính lệnh, không qua pipe.

Chạy đúng script này bằng Bash tool (1 call), làm việc tại repo tra-luat:

```bash
cd /c/qh/tra-luat && P=/c/Python313/python
mkdir -p scripts/.tl_state/gate
declare -A RC
g() { local n="$1"; shift; "$@" > "scripts/.tl_state/gate/${n}.out" 2>&1; RC[$n]=$?; }

g selftest      $P scripts/tl.py --selftest
g gen_inst      $P scripts/gen_instructions.py --selftest
g workflow      $P scripts/tl.py workflow-audit --strict --json
g golden        $P scripts/tl.py golden-test --json          # KHÔNG BAO GIỜ --write ở đây (R6)
g docclaims     $P scripts/tl.py doc-claims-check --strict --json   # r219 nối vào (r218 làm lệnh mà QUÊN nối)
g determinism   $P scripts/tl.py determinism-audit --strict --json
g relcheck      $P scripts/tl.py release-check --full --json
g relverify     $P scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json

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
