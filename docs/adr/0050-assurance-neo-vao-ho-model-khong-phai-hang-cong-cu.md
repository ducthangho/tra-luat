# ADR-0050 — cross_approved neo vào họ model, không vào hãng công cụ

- **Trạng thái:** Accepted (2026-09-18, quyết định kiến trúc do Đặc tả r2 đề xuất, chủ kho `ducthangho` phê duyệt tại https://github.com/ducthangho/tra-luat/issues/551#issuecomment-5726836582, thực thi theo Packet #551)

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

## Hai hành vi ĐÃ CÓ mà chưa ai khai — khai ở đây (Packet #551 revision 4)

Cả hai do verdict lượt 3 (`sha256 935a0c3792c5221eba24455188ecd0b873718c6c8e72134031269b8bd6f54dc0`) đo được trên `ops/bien_nhan_v2.py`. Chúng **không phải sơ hở**; chúng là chủ ý chưa được viết ra. Một hành vi đúng mà im lặng vẫn dẫn người đọc đi sai hướng, nên nó được khai ở đây thay vì bị sửa đi.

6. **Một người audit bảo chứng cho CẢ HAI vai.** Khi mức bằng chứng là `khai_co_audit`, cổng chấp nhận trường `nguoi_audit` / `audit_actor` **không mang tiền tố vai** ở mức top-level của biên nhận, cho cả vai `reviewer` lẫn vai `executor`. Nghĩa là **một** trường audit duy nhất thoả cho cả hai bên. Đây là chủ ý — một biên nhận, một người audit — chứ không phải chỗ quên. Hệ quả phải biết: biên nhận khi ấy **không phân biệt được** *"đã audit cả hai model"* với *"đã audit một model"*. Ai cần phân biệt thì khai thêm `executor_nguoi_audit` riêng; cổng đọc cả hai dạng.

   Ca đo: `khai_co_audit` + `nguoi_audit` chỉ ở top-level ⇒ **QUA** · `khai_co_audit` + `executor_nguoi_audit` riêng ⇒ **QUA** · `khai_co_audit` + không có người audit nào ⇒ **CHẶN** (đối chứng).

7. **Khoá model ở top-level tính là KHAI ĐÈ của vai reviewer.** `model` · `ho_model` · `model_family` · `canonical_model` đặt ở mức top-level của biên nhận (không nằm trong `model_reviewer_identity`) được cổng đọc là khai đè model của **vai reviewer**, nên kéo theo đòi `model_evidence`. Lý do: ở top-level hai vai dùng chung một không gian tên, và vai `executor` đã có tiền tố riêng (`executor_model`, …) để tự phân biệt; phần còn lại thuộc về reviewer.

   Ca đo: thêm khoá top-level `model` ⇒ **CHẶN** *"khai đè model reviewer … thiếu mức bằng chứng"* · thêm `ho_model` ⇒ **CHẶN**. Đo trên dữ liệu thật của kho: **0/184** biên nhận hiện có mang khoá ấy ở top-level ⇒ đây là **nới phạm vi chưa khai**, không phải hồi quy. Bên trong khối `model_<vai>_identity` thì ngược lại: khoá **không** mang tiền tố, cho cả hai vai — xem mục 8.

8. **Khối `model_<vai>_identity` tra khoá KHÔNG tiền tố, đối xứng hai vai.** Bên trong `model_reviewer_identity` và `model_executor_identity`, cổng đọc `model_family` · `ho_model` · `canonical_model` · `model` · `model_evidence` · `bang_chung_model` **không** mang tiền tố vai. Tiền tố `executor_` chỉ còn nghĩa ở mức top-level. Trước revision 4, tiền tố bị áp cho cả bên trong khối, nên `model_executor_identity: {model: …}` bị **bỏ qua lặng lẽ** trong khi `model_reviewer_identity: {model: …}` chạy — bất đối xứng ở đúng trường mà `cross_approved` treo lên. Đo trước khi đổi: dạng **có** tiền tố bên trong khối xuất hiện **0/184** lần, nên việc thôi đọc nó không thu hẹp biên nhận nào đang tồn tại.
