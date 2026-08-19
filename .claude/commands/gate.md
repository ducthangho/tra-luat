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

**HAI CHẾ ĐỘ, và chọn sai thì hoặc không đo được gì hoặc rửa được bằng chứng.**

Mặc định `--require-clean`: cây phải SẠCH, bằng chứng gắn vào đúng một commit và TÁI DÙNG ĐƯỢC.
Nhưng luồng `release-checklist.md` chạy `/gate` ở **bước 5** rồi mới commit ở **bước 7**, nên ở
đúng luồng ấy mặc định này làm MỌI subgate thoát `preflight` mã 2 trước khi chạy lệnh — tức
**không test được thay đổi đang chờ**, đúng lúc cần test nhất (P1 cross-review PR "#141").

Đặt `GATE_CAY_BAN=1` để chạy trên cây đang bẩn. Đánh đổi khai thẳng: bằng chứng lượt đó
**KHÔNG BAO GIỜ tái dùng được** — `gate_lifecycle.py validate` từ chối bằng chứng sinh trên cây
bẩn (mismatch `worktree_clean`, chốt có sẵn). Đó là chủ đích, không phải hạn chế: thứ vừa test là nội dung
CHƯA có trong lịch sử, nên nó không thể là chứng cho bất kỳ commit nào. Muốn bằng chứng tái dùng
được thì commit trước rồi chạy lại ở chế độ mặc định.

Chạy đúng script này bằng Bash tool (1 call), làm việc tại repo tra-luat:

```bash
cd /c/qh/tra-luat && P=/c/Python313/python
mkdir -p scripts/.tl_state/gate
BASE_SHA=$(git merge-base origin/master HEAD 2>/dev/null || git rev-parse HEAD)
HEAD_SHA=$(git rev-parse HEAD)
# Chế độ cây bẩn phải là OPT-IN tường minh và phải NÓI RA, kẻo người đọc log sau này
# tưởng đây là lượt gate bình thường rồi trích nó làm chứng cho một commit.
if [ "${GATE_CAY_BAN:-0}" = "1" ]; then
  SACH=()
  echo "  [gate] CHE DO CAY BAN: dang test thay doi CHUA commit."
  echo "  [gate] Bang chung luot nay KHONG tai dung duoc (validate se tu choi)."
else
  SACH=(--require-clean)
fi
declare -A RC
g() {
  local n="$1" positive="$2"; shift 2
  $P .claude/dev/gate_lifecycle.py run \
    --kind heavy --name "$n" --repo . \
    --evidence "scripts/.tl_state/gate/${n}.json" \
    --output "scripts/.tl_state/gate/${n}.out" \
    --expected-head "$HEAD_SHA" --base-sha "$BASE_SHA" "${SACH[@]}" \
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
