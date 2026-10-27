# Hồ sơ review đặc tả MAY-ADR-0054 (wp796/wp797) trên PR #798

Đặc tả wp796/wp797 r1–r10 đã **rút** khỏi cây cuối của PR #798 (commit rút ngay sau `2cd0bcd`), theo chủ kho
17-10-2026: *"Tách packet nhỏ"*. Thư mục này giữ verdict và prompt của các lượt **Codex CLI offline** (lời gọi chạy
trên commit cục bộ trước khi đẩy); verdict connector nằm trên PR #798.

| lượt | reviewer | đặc tả | commit | P1 | P2 | ghi chú |
|---|---|---|---|---|---|---|
| connector 1 | connector | r1 | `8a7fc22` | 9 | 2 | đếm finding |
| connector 2 | connector | r2 | `753b41e` | 6 | 5 | đếm finding |
| connector 3 | connector | r3 | `53e35f2` | 12 | 1 | đếm finding |
| CLI | Codex CLI | r4 | `51821ae` | 2 | 3 | đếm lớp; prompt lọc theo mô hình tin cậy |
| CLI | Codex CLI | r5 | `6154b00` | 2 | 4 | như trên |
| CLI | Codex CLI | r6 | `807661f` | 2 | 3 | như trên |
| CLI | Codex CLI | r7 | `7284aa9` | 0 | 2 | như trên |
| connector 4 | connector | r8 | `3f99c8f` | 9 | 3 | đếm finding — lộ việc prompt lọc đã che lỗi |
| CLI | Codex CLI | r9 | `0d19ff1` | 5 | 4 | đếm lớp; prompt **không lọc**, chuẩn connector |
| CLI | Codex CLI | r10 | `2cd0bcd` | 7 | 4 | đếm lớp; phân kỳ ⇒ dừng |

Bài học: một đặc tả mô tả cả máy trạng thái bằng văn xuôi không hội tụ dưới review — mỗi revision thêm cơ chế nên thêm
bề mặt. Và prompt dặn reviewer *bỏ qua* một hạng lỗi làm số P1 về 0 giả (r7) — đúng bệnh "cổng xanh nhờ được dặn xanh".
