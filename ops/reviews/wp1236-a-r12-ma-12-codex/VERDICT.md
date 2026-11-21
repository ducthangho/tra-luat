Review mã wp1236 đợt A, r12, lượt 12: **changes_requested**.

HEAD `9d8f6009a35727118015f26fc831e575c8103229`  
Tree `cdf0b59ad2ff23677a8707b12be69585c1db6aae`  
SPEC SHA256 `4589daf1fd666b03a68b7d7dcd5c60903c10e946963fd324c9ee6185ed8e2dc7`

Reviewer: `openai_codex / codex_cli / machine`, độc lập với executor Claude. Model và effort thực phục vụ: `KHONG_DO_DUOC`.

- **T01 — P2 — `test-thieu-chot`: thiếu ca bắt buộc của luật 8.** Vũ trụ a131 có 878 ký tự, chỉ gồm 694/138.495 chữ/số Unicode ngoài ASCII theo `isalnum()`; thiếu 137.801. Chưa có bảng 128 ASCII cho các vị trí SHA, OS và tên tệp. Ba đối chứng lazy chỉ gọi hàm lá; consumer đọc tệp thiếu các category và ký tự ngoài BMP ở văn bản tự do. Đo tại `coverage_a131.json`. Đây là nghĩa vụ ca mà luật 9 vẫn giữ, không phải nâng mức đột biến ngoài bảng.
- **T02 — P3 — `test-thieu-chot`, phân hạng `ngoai_bang_dong`: 5 đột biến sống**, mỗi ID qua đủ 47 ca: `r12i_head_uppercase`, `r12i_os_digit7`, `r12i_filename_Z`, `r12i_skip_old_ascii_name`, `r12i_skip_v3_ascii_name`. Đã xét B → A → ngoài, ghim cặp và đo đối chứng HEAD/mutant. **Chờ miễn chủ kho** neo exact SHA, hoặc đóng bằng ca. Miễn T02 không đóng T01.

| Đối chiếu lượt trước | Nhãn trên HEAD |
|---|---|
| S01 — `test-thieu-chot` | **VÁ HỜ / VA_MOT_PHAN**: reason đã được bảo vệ; thay đổi acceptance Unicode theo r12 không tính là vá; T01 còn mở |
| S02 — `test-thieu-chot` | **ĐÃ VÁ THẬT**: hai ID lịch sử đều GIET bởi a132, đúng tín hiệu ca |
| `yaml-ngoai-schema-bi-chan` | ĐÃ VÁ THẬT — ngoài schema được bỏ qua, lỗi UTF-8 có đối chứng |
| `k2-mat-loi-doc` | ĐÃ VÁ THẬT — lỗi đọc, duyệt và symlink giữ đúng lý do |
| `cli-vong-yaml-traceback` | ĐÃ VÁ THẬT — vòng YAML, lỗi stat và CLI rc2 đúng |
| `mo-ta-duong-dan-lech-hop-dong` | ĐÃ VÁ THẬT — `./tệp` hợp lệ; đường tuyệt đối, `..`, symlink bị chặn |
| `hop-dong-dau-vao-dau-ra-chua-chot` | ĐÃ VÁ THẬT — producer → consumer ở hai chế độ mô phỏng và CLI đạt |

Hội tụ lượt 11→12: **0/1**. Giữ 6 slug lịch sử, 1 lớp mở. `test-thieu-chot` tái diễn qua 12 lượt; giữ checkpoint theo §12, không tự mở vòng vá tiếp theo.

| Phép đo | Kết quả |
|---|---|
| Regex và hành vi r12 | 10/10 regex nguyên văn; không có lớp Unicode viết tắt hoặc `re.ASCII`. Ba đối chứng lazy qua consumer, casefold và LF đúng |
| Suite nguyên bản | rc0; **47/47 ca, 146/146 đột biến**, tự kiểm và tổng ĐẠT |
| Tập ô đóng băng | Đúng băm; **125/125** qua hai tuyến |
| Ruff 0.15.15, select F | rc0 trên ba tệp; contract pin/probe riêng: 3 chốt, 0 lỗi |
| Đăng ký test | rc0; 1226/1226 phản chứng, TỔNG ĐẠT |
| Diff | `diff --check` rc0; 3 tệp, **+2014/−0**, dưới trần 2100; thêm đúng 1 mục đăng ký |
| A | **798 = 783 GIET + 15 TUONG_DUONG**, kiểm từng chứng minh |
| B gốc | Đúng 201 ID và băm; **140 GIET + 8 TUONG_DUONG + 53 KHONG_AP_DUNG** |
| B kèm 47 cặp chuyển neo | **248 = 187 GIET + 8 TUONG_DUONG + 53 KHONG_AP_DUNG**; 28 CHOT_DA_BO có chứng minh riêng và 538 đối chứng ASCII; các đối chứng ngược GIET |
| Replay độc lập | **993 = 970 GIET + 23 tương đương**; chạy 970 ca đích và 23×47 ca. Lệnh `do` nguyên bản đã ngắt rc130; **không khai HOAN_TAT riêng** |
| Selftest HEAD / nền | Cả hai **rc1, 1768/1784**, cùng 16 ca đỏ, delta 0. Khác lời khai 1770/1784; gate vẫn **FAILED** |
| Windows native / CI | `not_run`; mô phỏng `nt` không thay phép đo Windows |

Chi tiết và hướng sửa nằm trong `VERDICT.json`. Bằng chứng chính: `prior_audit.json`, `coverage_a131.json`, `independent_pairs.jsonl`, `independent_witnesses.json`, `ledger_A_verified.json`, `ledger_B_201_verified.json`, `ledger_B_248_verified.json`, `replay_summary.json`, `selftest_delta.json`. Lệnh, mã thoát và băm stdout/stderr nằm trong các tệp `*.run.json`.

Giới hạn: không gọi mạng/GitHub. SPEC offline khớp SHA256 và Git blob; Git object nguồn đặc tả không có trong clone. Snapshot 17339 tệp đầu/cuối không có delta; không có thay đổi checkout quan sát được. Đây là review nội dung, không phải quyền land hoặc human audit E5.

KET_LUAN: changes_requested
