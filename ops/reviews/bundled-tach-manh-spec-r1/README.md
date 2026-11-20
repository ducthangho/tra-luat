# Bằng chứng đặc tả BUNDLED-TACH-MANH r1

Đo 2026-11-20 trên clone ĐẦY ĐỦ (không nông) của `origin/master` `0f9aa2a2cc697129e1f5be72feddf60986286865`, Linux, Python 3.13.
Nguyên mẫu được commit CỤC BỘ trong clone tạm (không push) vì `.githooks/eol_policy_test.py` dựng bản sao cây bằng `git ls-files`.

| tệp | nội dung |
|---|---|
| `nguyen-mau.diff` | diff nguyên mẫu `0f9aa2a..proto` cho `scripts/tl_core/`, `.githooks/`, `references/`, `scripts/test_fragments/` (không gồm hai tệp bundled sinh tự động); dòng ngữ cảnh rỗng đã bỏ dấu cách cuối cho `git diff --check`, `git apply --check` trên `0f9aa2a` vẫn đạt |
| `numstat.txt` | numstat 7 tệp của nguyên mẫu |
| `wp433_bundled_tach_manh.nguyen-mau.py` | fragment nguyên mẫu (8 nhãn) |
| `do-nguyen-mau.txt` | lượt đo đầu (trước khi commit cục bộ). Dòng `30/32 dat` của `eol_policy_test` là TẠO TÁC rig: bản sao cây lấy theo `git ls-files` nên thiếu tệp chưa commit; sau commit cục bộ ra `32/32 dat`, base cũng `32/32 dat` |
| `do-cuoi.txt` | lượt đo cuối trên proto HEAD (selftest 1785/1785, tfc, bfc, release-verify 186/186, py_size warn rỗng, golden, eol, ruff, doctrine-scan) |
| `dot-bien.txt` | 6 đột biến: a–f, mỗi cái làm đỏ ĐÚNG nhãn đích; dòng `c_bo_han_manh` đầu văng IndexError (tín dụng giả) → đã thêm chốt độ dài, đo lại `False ['nhieu_manh']` |
| `phan-chung-secrets-set.txt` | áp fragment `wp433_secrets_set_bundle.py` + `tl_gws.py` của `origin/agent/wp433-r8-g1-claude` lên nguyên mẫu, tái sinh: hai mảnh 189.328 / 117.343 B, `py_size.warn == []`, `test-fragments-check` ok, selftest `1786/1786` |
