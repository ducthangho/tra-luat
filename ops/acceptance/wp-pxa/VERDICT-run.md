# WP-PXA r1 — Review bằng chứng đo sau sửa (lượt review 2/2)

- **Reviewer:** Codex CLI 0.155.1 chạy **ngay trên ASUS** (tài khoản `admin`), gọi với `-m gpt-6-astra --sandbox workspace-write`, chỉ được ghi vào thư mục `out` riêng. Reviewer tự khai "GPT-6 / Codex; exact deployment suffix is not exposed, so I cannot attest `gpt-6-astra`", nên model thật được ghi là **`KHONG_do_duoc`** (chỉ biết model đã yêu cầu).
- **Thời gian:** 17:05:56Z–17:11:55Z, rc 0. Băm prompt `81712E4F…0809`. Verdict lưu tại `C:\Users\admin\tl-work\wp-pxa-review\out\VERDICT.md`.
- **Đối tượng:** mã `be9ca02` gồm module `bb96cd58…`, test `f539c32d…` và SKILL `cc970931…`; bằng chứng Desktop N2 chuyển sang ở dạng bộ con (zip gốc `9813dae0…`, MANIFEST `3d7a91d5…`, relay `8f6f2988…`); bằng chứng ASUS A2.

## Verdict: `approve_scoped`, không có P0/P1/P2 mới

| Kiểm | Kết quả theo reviewer |
|---|---|
| Toàn vẹn | HEAD và băm ba tệp khớp MANIFEST. 16 tệp chuyển sang khớp kích thước và băm. Băm bản sao harness và `source_hashes` trong mọi report đều khớp mã |
| Desktop Activation | PS5.1 và PS7: **30/30** (en-AU, mặc định), **36/36** (tr-TR, có counterexample). Mỗi ID chạy đúng một lần; các danh sách failed/setup/skipped/id_errors đều rỗng |
| Counterexample | CX01–CX06 đều `killed` đúng ca đích (PA04, PA10, PA16, PA19, PA27, PA29) với đúng lý do, không có timeout |
| Hồi quy cũ | Manifest 12/12, Config 46/46, Control 38/38 trên cả hai bản PowerShell (đọc từ dòng RESULT trong log thô). Ba ca Config báo "unavailable" giữ nguyên như trước |
| ASUS A2 | sạch → OK/3226; thêm `version.dll` → `ARTIFACT_EXTRA`; gỡ → OK/3226. Reviewer tự đọc lại cây (`tree-readback.json`) cũng ra OK/3226 |
| Kiểm thêm tại chỗ | Reviewer tự chạy harness trên ASUS: PS5.1 en-US **30/30**, PS7 vi-VN **36/36**. Mỗi mutant của chính reviewer đều ra 29/30, đỏ đúng ca đích |
| PA29 | Thời gian parse/duyệt cây: PS5.1 119/1124 ms và 95/1249 ms; PS7 399/1018 ms và 371/991 ms. Thiết kế tách token một lần nên **hợp lý là tuyến tính**. Ngưỡng 20 s đủ bắt hồi quy bậc hai nhưng không chứng minh độ phức tạp |
| Bộ đọc JSON | Độ chặt được giữ: dấu phân cách, số, escape, ký tự điều khiển, dữ liệu thừa phía sau, khoá trùng (so Ordinal), độ sâu 32. Mười phép dò so với `ProximaConfig` cho kết quả trùng. Không có API riêng của PS7 |

## Giới hạn reviewer nêu
- **Phạm vi chặn:** B2 chỉ bị từ chối khi bên gọi tôn trọng kết quả kiểm. D3 chỉ được ngăn giữa những bên **cùng dùng guard** và giữ khoá suốt thời gian app chạy.
- **Ngoài phạm vi cưỡng chế:** mở Proxima bằng tay; tiến trình mở hoặc tệp đổi **sau** khi chụp snapshot; bản thân sản phẩm và mã P4 (không đổi).
- **Tiến trình elevated không đọc được CommandLine:** trả `NOT_MEASURED`, trừ khi đã có bằng chứng busy rõ ràng.
- **Escape surrogate không ghép cặp** vẫn được chấp nhận, như parser cũ và như ngữ pháp RFC cho phép.
- **Chưa xem:** zip đầy đủ, 6 report JSON cũ, bản sao harness, script đóng băng. Kết quả quét secret rc 0 là bằng chứng chuyển tiếp, reviewer không quét lại.
