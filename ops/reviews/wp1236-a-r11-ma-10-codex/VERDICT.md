**Verdict: changes_requested — wp1236 đợt A, r11, lượt 10.**

Reviewed SHA: `9c17a34d4f9ae8a4adcb80d5592bc72f6748be5e`  
Tree: `79e64fe41eb129eaad47aca6c754a18ceedf5b02`  
Spec SHA-256: `30386131d8017bf982ca0be7707c8d5fd3035e9586c5f94a446f45c40fc863d1`

| Finding | Mức | Kết quả |
|---|---|---|
| Q01 · `test-thieu-chot` | P2 | 16 đột biến Unicode mới sống qua 46/46 ca, vi phạm luật 4. Có phản chứng độc lập ở hàm lá và `kiem_ho_so`. P01 mới đóng mười biểu hiện cũ. |
| Q02 · `test-thieu-chot` | P3 | Giữ P03: `r9b_event_tab`, `r9b_name_inner_spaces` sống; mỗi ID có 0/125 ô phân biệt. Đúng `ngoai_bang_dong`, **chờ miễn chủ kho** neo SHA trên. |

Đối chiếu lượt 9: **P01 VÁ HỜ; P02 ĐÃ VÁ THẬT; P03 CHƯA VÁ**. P02 đã đọc byte, thư mục, tên tương đối và cả hai mẫu hồ sơ từ hạt giống: nguồn khác có băm khớp làm kết quả đổi đúng. Năm lớp lịch sử khác được đo lại và giữ ĐÃ VÁ THẬT. Hội tụ **0/1 theo lớp**, không tính P02 thành một lớp riêng; lớp `test-thieu-chot` tiếp tục lặp và cần xét lại cách phủ toàn miền tại checkpoint.

| Phép đo | Kết quả |
|---|---|
| Suite native | rc0; 46/46 ca,146/146 đột biến; tự kiểm và TỔNG ĐẠT |
| Ruff0.15.15 `--select F`, đúng ba tệp, `--no-cache` | rc0 |
| `ci_dang_ky_test.py` | rc0; TỔNG ĐẠT |
| Diff base lease → HEAD | 3 tệp,+1850/−0, dưới trần2100; `diff --check` rc0 |
| Luật5, đủ167 ID | 153 GIET,7 TUONG_DUONG,5 KHONG_AP_DUNG có căn cứ/thay thế,2 NGOAI_BANG_DONG chờ miễn |
| Luật6 | 45 hàng có neo; đủ125 ID ô; replay độc lập125/125 đúng; dependency seed đạt |
| Quét độc lập mới | 19 cặp: 16 sống luật4, 3 bị giết; ghim kho mới và kho cộng dồn186 ID |
| Selftest HEAD / nền2719f81 | **rc1, 1768/1784 cả hai; cùng16 lỗi; delta0**. Không tái hiện1770/1784. Đây là `failed`, không phải pass bất biến(a). |
| Windows native, CI, LIVE | `not_run` trong review offline |

Bằng chứng chính: [VERDICT.json](VERDICT.json), [ledger mới](ledger_kho_moi_luot10.jsonl), [cặp đột biến](kho_dot_bien_luot10.jsonl), [phản chứng](independent_witnesses.json), [nguồn và tuyến](seed_and_routes.json), [ledger167](ledger_167_verified.jsonl), [selftest delta](selftest_delta.json). JSON ghi command, mã thoát con thật, stdout/stderr và băm; các lần setup lỗi/ngắt tách riêng.

Hướng vá Q01: bảng ngữ pháp dùng chung cho hai tuyến, bao các thành phần URL/ngày/\S, Unicode Nd ngoài toàn độ và whitespace gồm xuống dòng; giữ đối chứng đúng lý do. Không đổi mã sản phẩm hay bảng125 ô để làm test xanh. Miễn Q02 không đóng Q01.

Reviewer: `openai_codex / codex_cli / machine`, session `01a1fd72-c67a-78a3-b57e-ea0577a98af9`; model/effort phục vụ `KHONG_DO_DUOC`. Linux/Python3.13.18; native suite chạy riêng, replay reviewer có cache parse YAML thuần và archive bất biến. Không gọi mạng. Checkout có 17339 tệp được băm trước/sau, không có delta byte, HEAD/tree/diff/index/untracked/ignored giữ nguyên; selftest chỉ chạy ở bản sao dưới `work/`.

KET_LUAN: changes_requested
