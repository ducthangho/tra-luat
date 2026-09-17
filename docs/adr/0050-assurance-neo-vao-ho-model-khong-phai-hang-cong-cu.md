# ADR-0050 — cross_approved neo vào họ model, không vào hãng công cụ

- **Trạng thái:** Accepted (2026-09-17, chỉ thị chủ kho `ducthangho`, thực thi theo Packet #551)

`cross_approved` trong `docs/PROTOCOL_DA_PHIEN.md` §8 được định nghĩa lại: neo vào **HỌ MODEL đã phục vụ lượt chạy**, không neo vào **HÃNG CÔNG CỤ** (`provider`).

## Bối cảnh và mâu thuẫn đo được

Kho từng tồn tại hai khẳng định mâu thuẫn trực tiếp:

- `ops/specs/doctrine-scan-dao-sang-danh-sach-cho-phep-r1.md:13`: *"Cặp agy↔claude khác provider nên thoả §8 mục 1"* ⇒ là `cross_approved`.
- `ops/specs/ag-t0-01b-r3.md:47-51`: *"Sai. Một phiên AG đặt `--model claude-opus-4-6-thinking` rồi được một phiên Claude Code review là cùng một họ model, khác vỏ công cụ — tức `same_provider_approved` đội lốt `cross_approved`"*.

Phát hiện của `ag-t0-01b-r3` phản ánh đúng bản chất an toàn của protocol: mục đích của `cross_approved` là bảo đảm hai tư duy mô hình độc lập phản biện chéo nhau. Nếu cùng một họ model (cùng trọng số/họ huấn luyện) chạy qua hai giao diện CLI khác nhau (ví dụ Antigravity gọi Claude rồi Claude Code review lại) thì bản chất vẫn là tự duyệt chéo trong cùng họ, tạo ra ảo tưởng bảo chứng.

Mặt khác, ở tầng schema, `docs/PROTOCOL_DA_PHIEN.md` đã có trường `model_reviewer_identity` tách bạch giữa `provider` và `model`, nhưng cổng kiểm định chưa đối chiếu họ model của hai bên.

## Quyết định kiến trúc

1. **Neo vào họ model thực tế**: `cross_approved` đòi hỏi Reviewer và Executor phải sử dụng hai họ model độc lập phục vụ lượt chạy (ví dụ Claude review GPT hoặc Gemini review Claude). Các cặp công cụ khác nhau nhưng cùng chạy một họ model chỉ đạt mức `same_provider_approved`.
2. **Ba mức bằng chứng model**:
   - `do_may`: máy đo trực tiếp từng lượt chạy (ví dụ qua trường `modelUsage[*].canonicalModel` của telemetry);
   - `khai_co_audit`: người khai kèm người audit xác nhận; mức này bắt buộc phải tự khai là yếu hơn `do_may` ngay tại chỗ dùng;
   - `khong_do_duoc`: không có dữ liệu đo máy hoặc không xác minh được model thực tế đã phục vụ.
3. **Bảng cho phép ánh xạ mặc định**: Cổng `ops/bien_nhan_v2.py` duy trì bảng ánh xạ mặc định từ `provider → họ model mặc định`, đồng thời cho phép biên nhận khai đè bằng trường model có bằng chứng đo lường hoặc audit hợp lệ.
4. **Bất biến an toàn giữ nguyên**: `same_provider_approved` vẫn **không** thay thế `cross_approved` cho Review Class `sensitive`.
5. **Không hồi tố**: Quyết định này áp dụng cho các lượt review và biên nhận phát sinh từ thời điểm đóng băng đặc tả #551 trở đi; không đọc lại hay thay đổi mức bảo chứng của các biên nhận đã land trong lịch sử.
