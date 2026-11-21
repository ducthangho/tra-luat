Review độc lập lượt 9, wp1236 đợt A theo r11: **changes_requested** — 2 finding P2 và 1 finding P3, cùng lớp `test-thieu-chot`.

`reviewed_sha`: `2719f81dd5c3f89e4986f6710ed2145cfd4c057b`  
Tree: `612ebd0d81cb1b92f9bb19cea5adc670bbc8f987`  
Đặc tả SHA-256: `30386131d8017bf982ca0be7707c8d5fd3035e9586c5f94a446f45c40fc863d1`.

Provider `openai_codex`, surface `codex_cli`, transport `machine`; Linux, Python 3.13.18. Model/effort phục vụ: `KHONG_DO_DUOC`.

- **P01 — P2:** 10 đột biến ngữ pháp không tương đương sống qua đủ 45/45 ca: số Unicode trong bảy vị trí của tệp đánh giá, khóa landed, khoảng trắng đầu token và dấu phân cách whitespace. Đây là nghĩa vụ **luật 4, xét trước luật 6**. Các bảng a120/a121/a122 còn thiếu tuyến consumer. Ledger 45 hàng đủ ID, nhưng bảy nhóm con trỏ thiếu ca kiểm phía đối lập; đã xác định ca giết ở nơi khác.
- **P02 — P2:** `chay_o` kiểm băm hạt giống nhưng vẫn đọc fixture qua `FX`/`THU_MUC_THAT` và tự dựng hồ sơ consumer. Bốn phép kiểm dependency cho thấy đổi đầu vào trong `hat_giong` không đổi đầu vào thực được đo. Vi phạm trực tiếp yêu cầu nguồn dữ liệu của luật 6; không khẳng định 125 ô hiện tại cho kết quả sai.
- **P03 — P3, `ngoai_bang_dong`:** hai biến thể chấp nhận TAB cuối event và gom khoảng trắng bên trong tên job sống qua 45/45 ca. Không ô nào trong 125 ô phân biệt được chúng; phân hạng đúng **luật 6(b)**. Chưa có miễn của chủ kho neo exact SHA này.

Đối chiếu §8.3: **N01 VÁ HỜ (vá một phần); N02 ĐÃ VÁ THẬT về ledger theo r11; N03 ĐÃ VÁ THẬT.** Bốn lớp lịch sử còn lại được kiểm lại và giữ đóng. Hội tụ theo lớp **1/2**; `test-thieu-chot` vẫn lặp từ ba lượt trở lên. Bảng lớp, nguồn SHA và nối slug đầy đủ trong [VERDICT.json](VERDICT.json).

Kết quả đo mới:

| Phép đo | Kết quả |
|---|---|
| Suite chính | 45/45 ca; 146/146 đột biến; tự kiểm ĐẠT; rc 0 |
| Ruff F trên ba tệp | rc 0; Ruff 0.15.15 |
| Đăng ký CI | 31/31; hợp đồng Ruff 3/3; phản chứng 1226/1226; rc 0 |
| Diff | 3 tệp, +1795/−0 dòng ≤ trần 2100; `diff --check` rc 0 |
| Bảng đóng | Sinh đúng đối tượng đóng băng, băm chuẩn `628e2704…`; replay độc lập 125 hàm lá và 119 consumer đúng kỳ vọng; 6 ô chỉ đo head |
| Kho 152 ID | 140 GIET đúng ca; 7 TUONG_DUONG; 5 KHONG_AP_DUNG có nhãn cuối hợp lệ |
| Luật 7 và seam | Producer→consumer: 2 xanh + 8 đỏ đúng; m65/m79 bị giết qua a128; CHI_POSIX còn 9 mục cần symlink |
| Quét độc lập | 15 đột biến × 45 ca: 12 sống không tương đương, 3 bị giết, không lỗi chạy/vô can |

Từng đột biến mới có cặp neo/thay, phép đo helper và consumer, cùng phân hạng trong [kho mới](kho_dot_bien_reviewer_luot9.jsonl), [ledger mới](ledger_kho_moi_luot9.jsonl) và [đối chứng](independent_contrasts.json). Kho cộng dồn có 167 ID. Bảy biến thể dùng kiểm con trỏ ledger đã bị ca khác giết; không tính chúng là đột biến sống qua toàn suite.

`tl.py --selftest` trên ứng viên và base `010046f2141799ec6ffc9cfa1322d49df3f3f680` đều **1768/1784, rc 1**, cùng 16 ca đỏ, delta = 0. Đây vẫn là kết quả **failed**, không xác nhận lời khai 1784/1784. Xem [đối chiếu selftest](selftest_comparison.json). Windows native và CI **not_run**; mô phỏng hai chế độ không thay Windows local bắt buộc.

**Sự cố read-only của lượt review:** selftest đã sinh 20 tệp ignored trong checkout. Đã giữ bản sao dưới `work/selftest_side_effects/`, xác minh chúng không tồn tại ở snapshot đầu rồi dọn đúng các tệp mới ấy. Không tệp tracked hay tệp có sẵn nào đổi; snapshot cuối khớp lại 17.339 tệp, HEAD và tree ban đầu. Không tuyên bố checkout chưa từng bị ghi; chi tiết ở [read_only_incident.json](read_only_incident.json).

Không commit, push, gọi mạng, merge hay LIVE. Đã hết lời gọi Codex 10/10 theo assignment; trả checkpoint cùng bằng chứng, không tự mở lượt tiếp. Chưa đủ điều kiện approve/merge. Kiểm schema phải ra `HOP_LE`; biên nhận lưu tại `kiem_verdict.txt`.

KET_LUAN: changes_requested
