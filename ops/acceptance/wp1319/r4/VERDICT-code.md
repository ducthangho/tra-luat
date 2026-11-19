# WP1319 r4 — Review mã harness trước khi chạy (lượt review 1/2)

- Reviewer: Claude subagent mới (general-purpose), chỉ đọc, context mới. Model tự khai `claude-opus-5-5`, effort `KHONG_do_duoc` (phiên điều phối yêu cầu xhigh).
- Đối tượng: `r4_native.py` sha256 `6c814f14a9ae0fe6b326f41352c3c54fd764203050f4cc5a2d1ffa9925fecfe9` và `test_r4_pure.py` `c8e217b61bfb2055ad837fcd46b31951c3318661a9113082c5726aa3c3f4e3fd`. Đây là sản phẩm của Codex Executor lượt 1/3, run `702483193dcc4d1a9c84e1614e20f971`. Mã nằm ngoài kho (scratch phiên điều phối).
- Reviewer đã kiểm khớp băm, chạy `py_compile` và 5/5 unittest. Không sửa tệp nào.

## Verdict: `request_changes`

Phần đúng:
- Mọi ghi đều nằm trong WORK.
- Không ghi `__pycache__` vào thư mục P4.
- Khoá host: đường HOST_BUSY không ghi gì; chỉ truncate khi nội dung vẫn là của mình và job đã rỗng.
- Chỉ giết tiến trình qua `JobProcess`.
- `p4_prespawn_check` sao đúng `run()` của P4, không thêm kiểm đủ tệp, nên B2 đo đúng hành vi P4.
- Thứ tự dọn dẹp đúng.

| # | Mức | Finding (rút gọn) |
|---|---|---|
| 1 | **P0** | Ảnh chụp tiến trình qua PowerShell 5.1 xuất theo code page console, rồi bị giải mã UTF-8 strict. Đường dẫn tiếng Việt của tiến trình khác làm preflight STOP, hoặc làm A/B1/C FAIL giả |
| 2 | P1 | A/B1 đạt khi bị từ chối vì bất kỳ ngoại lệ nào, kể cả không liên quan việc sửa tệp. Cần `rejection_attributed` |
| 3 | P1 | D3 tính là "bị từ chối" khi tiến trình thoát vì bất kỳ lý do gì, kể cả crash. D1 nhận mọi OSError. Cần marker dương |
| 4 | P1 | Không có đối chứng dương cho bộ lọc tiến trình. Token có thể khớp nhầm chính harness |
| 5 | P1 | Cổng 19222 chỉ được kiểm ở preflight, không kiểm lại ngay trước khi spawn như P4 |
| 6–18 | P2 | Bỏ C/D nếu A/B dọn không sạch; phân biệt `not_run` với FAIL; `INTERRUPTED`; hit của D3 lẫn vào C; quét log electron-log; poll lúc thoát; tệp kết quả khi STOP; ghi JSON nguyên tử; lọc tiền tố trước `resolve()`; `safe_output` với SOURCE/CODE/PARENT; khoảng trống so đặc tả (export-manifest, tải máy, số tệp nguồn, profile còn nguyên); handler HTTP gặp request hỏng; thêm unittest |

Kế thừa từ P4, không phải lỗi harness:
- Thư mục known-folder của Electron bỏ qua biến APPDATA, nên "isolated home" chỉ cô lập một phần.
- Proxy Deny không phủ các lời gọi mạng mà Node thực hiện trực tiếp.

## Xử lý
Toàn bộ 18 mục đã giao Codex Executor ở lượt 2/3 (`FIX1.md`). Phiên điều phối sẽ đối chiếu diff từng mục trước khi chạy. Lượt review 2/2 sẽ review gói đóng băng sau khi chạy, kèm mã đã sửa.
