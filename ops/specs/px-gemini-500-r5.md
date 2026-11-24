# Đặc tả packet px-gemini-500 revision 5 — errata tối thiểu cho r1/r2 (#1457)

Bối cảnh: revision 3 (`364af41`) và 4 (`4f30c0e`) viết lại r1/r2 RESULTS và không hội tụ (tỷ lệ đóng lớp §12: 0/10, rồi 2/11); cả hai
không push. Quyết định xét lại: https://github.com/ducthangho/tra-luat/issues/1457#issuecomment-7053038602. Chủ kho chọn errata tối thiểu
và cấp thêm 2 lời gọi Codex: https://github.com/ducthangho/tra-luat/issues/1457#issuecomment-7053593796.

## 1. Việc
1. Chèn đúng một khối trích dẫn "Đính chính (revision 5, #1457)" ngay sau dòng tiêu đề của `ops/acceptance/px-gemini-500/r1/RESULTS.md`
   và `ops/acceptance/px-gemini-500/r2/RESULTS.md`. Khối ấy trỏ tới các verdict trên #1457 và Issue nợ #1471, nói rằng kết luận trong tệp
   là lời khai chưa xác minh trong kho.
2. Không đổi byte nào khác của hai tệp. Không sửa đặc tả, lease r1–r4. Không bia mộ.
3. Không thêm định danh vận hành mới (tên tài khoản, UUID máy hay tiền tố, ID phiên) vào tệp nào của revision này.

## 2. Ranh giới
- Review Class `sensitive`. Review offline trên SHA ứng viên trước push (ADR-0060 M5/M12); PR mở draft; connector khi còn draft (M6, C1).
- Lời gọi Codex cho PR này: 2 theo ghi hộ trên (1 offline trước push, 1 `@codex review` khi draft). Không gọi thêm khi chưa có E2 mới.
- 0 thao tác VM, 0 lời gọi inference.
- Lease r5 chỉ cấp khi `ai-dang-giu` ra 0 cho cả write set (lease r4, nhánh cục bộ không push, hết hạn 2026-11-21T03:01:42Z).

## 3. Nghiệm thu
- `git diff` base..ứng viên trên hai tệp RESULTS chỉ gồm các dòng thêm của khối đính chính.
- `python scripts/tl.py --selftest` N/N; `git diff --check` sạch; `ops/lease_publish.py check` rc=0 cho lease r5.
