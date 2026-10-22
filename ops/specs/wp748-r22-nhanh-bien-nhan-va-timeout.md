# WP748 r22/g22 — vá F01 (kiểm biên nhận thời gian) và F02 (timeout giết cả cây) trong `ops/nhanh_don_duoc_test.py`

## Thẩm quyền và nguồn gốc

Chỉ thị chủ kho: "Cấp packet r22 vá F01 và F02 đi" (phiên Claude Code `session_014eUnFtkty9fZicFG9T1Wei`, 2026-10-22T06:59Z),
ghi hộ ở https://github.com/ducthangho/tra-luat/issues/748#issuecomment-6334796777. Executor: Claude Code (`anthropic_claude`,
`claude_code`, remote Linux). Reviewer: phiên Codex độc lập chỉ đọc qua `launcher.py run`, neo đúng head cuối. Review Class
`sensitive`. Base `origin/master` `9e9a74b2a396ef458d25c51a5563efafbb45ba0c` (tree `9fc05c9986f711d1961e040dc7345850d0133294`);
`ops/nhanh_don_duoc_test.py` trùng byte với `3818bd4`.

Nguồn finding: run launcher `03c4f6be` neo `3818bd4` (verdict trong PR #867, `ops/land/pr849-wp748-provenance/verdicts/`).

## Lỗi

- **F01 timing-receipt-validation** — `_loi_gop_dich` chỉ đòi `bat_dau`/`ket_thuc` là chuỗi khác rỗng; trần 540 s chỉ đo bằng
  `giay` khai riêng. Biên nhận `bat_dau=ket_thuc="invalid"`, mốc đảo ngược, hoặc khoảng 900 s với `giay=0` vẫn ra
  `targeted_mutant_gate: DAT`.
- **F02 timeout-descendant-containment** — `run()` dùng `subprocess.run(..., timeout=_TRAN_GIAY_CON)`: quá hạn chỉ giết con trực
  tiếp; cháu (git, harness con) sống tiếp, giữ tệp fixture/ống; trên Windows `communicate()` sau giết không có hạn nên có thể treo.

## Write set hiệu lực

1. `ops/nhanh_don_duoc_test.py`

Băm `sorted NFC casefold compact UTF-8 JSON` ghi trong lease. Quét `ai-dang-giu` 2026-10-22T06:59:14Z trên 530/530 ref: `NGƯỜI_GIỮ 0`.

## Thay đổi

- F01: phân tích `bat_dau`/`ket_thuc` thành thời điểm UTC có múi giờ; từ chối sai định dạng, đảo ngược, và lệch giữa
  `ket_thuc - bat_dau` với `giay` vượt dung sai khai rõ. Trần 540 s giữ nguyên ngữ nghĩa.
- F02: tiến trình con chạy trong nhóm/phiên riêng (POSIX `start_new_session`; Windows `CREATE_NEW_PROCESS_GROUP`); quá hạn thì
  giết CẢ CÂY rồi thu output có hạn; vẫn trả rc 124, fail-closed như cũ.
- Mỗi finding một phản chứng riêng + một đột biến riêng làm phản chứng ĐỎ. Không skip ca, không nới assertion.

## Chấp nhận

- `python3 ops/nhanh_don_duoc_test.py` (chế độ mặc định có tự đột biến) N/N; ruff F delta so master = 0.
- CI bắt buộc xanh trên head cuối; `full_mutant_audit` trên head cuối.
- Codex review qua `launcher.py run` trên head cuối: 0 P0/P1/P2.
- Chủ kho duyệt lần cuối trên SHA cụ thể trước merge. Land bookkeeping là bước riêng.

## Dừng

Dừng và báo khi: người giữ chồng lấn, cần ghi ngoài write set, hoặc thiếu bằng chứng dương.
