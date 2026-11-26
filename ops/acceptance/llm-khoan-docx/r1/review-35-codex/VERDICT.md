# Verdict packet #1525 r35 lượt 35 — Codex

reviewed_sha: 8b6782620a6a365d7e5c890481d19a0077609f2e  
reviewed_tree: 62fc458c8fd507b0137da1551cadf9347ac78f45  
base_sha: 64b7f2c14776d5d0e1d34a6be4725490956f5bec

VERDICT: REQUEST_CHANGES

Dòng verdict là tạm trong lúc đối chiếu mã và chạy các phép đo.

## Preflight

- Checkout detached. `git merge-base` trả đúng base đã giao, tree nền `0cc14e79cecd2ce44bc4dc6cff92cadb31fd7ee4`. Diff làm việc và diff index đầu lượt rỗng. Mục ignored sẵn có là thư mục rỗng `.codex/`. [Đặc tả r35](../ops/specs/llm-khoan-docx-r35.md)
- Lease #1525 r35/g1, Review Class khai báo và hiệu lực `sensitive`, hiệu lực đến 23:15 UTC ngày 26-11-2026. Trần 36, đã dùng 35 trước run này. Blob spec `d55a47273d26b52ca0dfa568b7922eba41363e4e`, SHA-256 `cb8cfc2e5217cd68bfe4ac729fb919bf4913bf5df17e1e755a87b11fc531f3dc` khớp lease. Đối chiếu 36/36 cặp lease/spec với bytes tại HEAD và hash đã khai. Bia mộ khớp hai chiều 35/35 cặp từ #1514 r9 qua #1525 r1 đến r35. [Lease r35](../ops/leases/llm-khoan-docx-r35-g1-claude.yaml)
- Write set 186 path, SHA-256 tính lại `ba2cd9b80167774cacdb6b9d70b1645ab3035e8e75b2408e89d493fe4fce4ea7`. Bản vá r35 từ `5bc6abdb987f075666609a336be0207f977f2605` khớp 10/10. Diff packet từ `fcb12b3873c3bec2c339029136243ed2c804ce05` khớp 182/182 sau khi bỏ bốn hồ sơ #1514 như prompt. Toàn PR có 230 path, 48 path ngoài lease r35 thuộc lịch sử #1514. SHA-256 của ba diff `git diff --binary <mốc> HEAD` lần lượt là `f2f60cdbdd733574931bf3a3a6d8d57caaa18dc466f8f3dff9515a71332a79b2`, `9d8ce3117f94329f37e247bc232f5fcd7c1297f62a8446528d3a57627a8b96f2` và `ad022978e40a5cccf9c4a0e2d808aa274c4385cffc7d0b32fe04b3a6278e7a06`.
- Executor theo lease là `anthropic_claude / claude_code / machine/local`, quyền đứng ghi từ phiên `session_015GtxrZQYT3Vt8PJdXrjEKg`. Reviewer `openai_codex / codex_cli / machine`, launcher run `db0f1b9b0b67455cbaea22514060f35d`, context và checkout riêng. Prompt snapshot SHA-256 `b1a683594c019e6db5a5ae6a65832c7f4e6779923ac9e3bdf55be3235eab1a9d`, checkpoint SHA-256 `b399986ed54fc52ad6b412cf6d38f370becf7eb754ac511d2e180ed084ff4e0f` khớp run. Sandbox `workspace-write` theo cấu hình phiên, mạng hạn chế. Model và effort phục vụ `KHONG_DO_DUOC` từ metadata run. Phiên đang ghi verdict chưa có rc terminal và hash stdout của launcher.

## Đối chiếu lượt 34 và đặc tả r35

| Mục | Trạng thái | Bằng chứng |
| --- | --- | --- |
| `ranh-gioi-khoan` lượt 34 · §2.28–§2.37 | **VÁ MỘT PHẦN** | Bộ quét bắt dải chữ cùng kiểu, nhãn ghép số/chữ, đầu thân dính và có đệm, gạch trước nháy/ngoặc. Ca dương giữ các mẫu đã duyệt, gồm `Tp.`. Cửa nhận số vẫn bỏ qua nhánh bullet/phần tiền tố của ngữ pháp cũ khi soi thân sau số. Xem finding bên dưới. [Mã](../scripts/tl_core/llm_route.py#L658) · [Ca](../scripts/tl_core/llm_route_test.py#L1931) |
| `can-tai-nguyen-doc-nguon` lượt 34 · §2.37 | **VÁ MỘT PHẦN** | `_ket_thuc_cau` quét lùi, thay nối lặp bằng danh sách dòng, có chốt độ sâu, giới hạn số trước `int`, độ dài nhãn và tổng chữ. Một số chốt đến sau công việc cần giới hạn. Riêng trần chữ số chỉ có hiệu lực khi so sau model. Xem finding bên dưới. [Quét lùi](../scripts/tl_core/llm_route.py#L1622) · [Gom khoản](../scripts/tl_core/llm_route.py#L1518) · [CLI](../scripts/tl_core/ops_misc.py#L3095) |
| `ranh-gioi-ky-tu` lượt 34 · §2.16–§2.21, §2.37 | **ĐÃ VÁ THẬT** trong miền chữ hiệu lực của hai bộ đọc | `_phan_tich_doan` ghi cờ từ chữ sau giải XML và xử lý markup, trước gộp trắng. `doc_dieu_docx` kiểm mọi đoạn trước lọc đoạn trắng, tiêu đề và vùng Điều. Đoạn chỉ có trắng ngoài miền bị chặn ở cả ba vị trí. Đối chứng đoạn rỗng và ký tự trong mẩu bị bỏ qua. Nguồn UTF-8 và chữ nhận từ `extract` kiểm trước tách dòng; một BOM đầu được xử lý theo hợp đồng. Thay đổi trước biên của bộ đọc chung thuộc U2. [Cờ ký tự](../scripts/tl_core/llm_route.py#L1364) · [Chốt mọi đoạn](../scripts/tl_core/llm_route.py#L1447) · [Ca](../scripts/tl_core/llm_route_test.py#L1971) |
| §1, §2.2–§2.3 · K1 #1514 | **ĐÃ VÁ THẬT** với hai đường ghép gốc | Dòng điểm đứng riêng mà bộ quét nhận được bị chặn, và dòng tiếp mở “là” trong nguồn có số thiếu nhãn khoản nên bị chặn. Nguồn mất số xử lý mỗi dòng riêng, dòng chỉ mở bằng “là” thiếu vế thuật ngữ khi so. Điều 3 Luật 134/2025/QH15 và ba đầu ra lưu đều 8/8 theo fixture sẵn có. `can_nguoi_duyet: true`, hai giá trị `pham_vi_kiem`, bề mặt CLI và các hàm gọi model giữ nguyên theo diff. [K1 gốc](../ops/acceptance/llm-ranh-gioi-khoan/r1/review-10-codex/VERDICT.md#L35) · [Tách](../scripts/tl_core/llm_route.py#L1589) · [So](../scripts/tl_core/llm_route.py#L1724) · [JSON](../scripts/tl_core/ops_misc.py#L3132) |
| §2.1, §2.4–§2.18 · Vị trí Điều, điểm gõ tay, câu dẫn | **ĐÃ VÁ THẬT** đối với các biểu hiện còn thuộc hợp đồng. Cắt Điều, đếm trong bảng và tiếp nhận đoạn điểm gõ tay **HẾT ĐỐI TƯỢNG** theo r7 | Tiêu đề đứng đầu phần có nội dung, khớp cả đoạn và đúng số được yêu cầu, thiếu số Word và ngắt mềm. Vùng đi tới hết tệp, chặn bảng, khối lạ và tiêu đề thứ hai trong miền đã công bố. Đoạn không số có chữ sau khoản đầu bị chặn. Trước khoản đầu chỉ được một câu dẫn khớp toàn mẫu. [Quét khối](../scripts/tl_core/llm_route.py#L1134) · [Chọn vùng](../scripts/tl_core/llm_route.py#L1444) · [Câu dẫn](../scripts/tl_core/llm_route.py#L1539) |
| §2.4–§2.18, §2.22–§2.26 · Số Word | **ĐÃ VÁ THẬT** với biểu hiện lịch sử trong miền hỗ trợ | `start` vắng mặc định 0, `startOverride` thay gốc của đúng cấp. Bộ đếm riêng theo `numId` và bỏ bộ đếm cấp con khi cấp cha tăng. Chặn thiếu tổ tiên, cấp/ID lỗi, trùng đơn trị, override ngoài miền và hai danh sách thuộc vùng. Khoản phải decimal với nhãn của chính cấp, dãy từ 1. Ca dương có override khác gốc, nhãn chữ sau Z và reset. [Định nghĩa](../scripts/tl_core/llm_route.py#L910) · [Bộ đếm](../scripts/tl_core/llm_route.py#L1417) · [Kiểm cấp khoản](../scripts/tl_core/llm_route.py#L1490) |
| §2.5–§2.13, §2.23–§2.29, §2.32–§2.35 · Markup và style | **ĐÃ VÁ THẬT** với biểu hiện lịch sử ở đường cấu trúc | Gạch đơn/kép có hiệu lực, `del` và `moveFrom` được lọc; giữ `ins`, `moveTo` và mẩu phân cách theo hợp đồng. `xml:space` kế thừa và đặt lại theo cây. Kiểm dấu đoạn, phần tử lạ và ngắt theo nội dung hiệu lực. Phép so đếm khoản, so thứ tự và trọn hai vế, dò từ nối trong đoạn mở khoản cấu trúc. [Style](../scripts/tl_core/llm_route.py#L1011) · [Markup](../scripts/tl_core/llm_route.py#L1169) · [Phép so](../scripts/tl_core/llm_route.py#L1724) |
| §2.7 D1, §2.9 · `KhongCauTruc` | **ĐÃ VÁ THẬT** | DOCX thiếu đánh số tự động thoát `ValueError` sang rc 2. Phân tuyến theo chữ ký tệp, nhánh DOCX không rơi xuống nhánh UTF-8. [Chốt](../scripts/tl_core/llm_route.py#L1487) · [CLI](../scripts/tl_core/ops_misc.py#L3027) |
| §2.21 U2, §2.22 V1/V3, §2.23 W1–W3 · Đường số hiệu | **ĐẠT** theo quyết định đã ghi | `--markup-strict` và cảnh báo trần export được kiểm trước model. Phạm vi bộ đọc chung đã khai gồm ký tự mất trước cache, cắt Điều theo regex, gạch qua style, strict chặn oan và chuyển XML–chữ có thể bỏ tab/ngắt. Vấn đề phân loại nhãn của lượt này nằm sau `extract`, đồng thời có trên đường UTF-8. [Đọc qua extract](../scripts/tl_core/llm_route.py#L1832) · [Giới hạn](../docs/GOI_AGENT_DA_NEN.md#L393) |
| §3 · Ca và đột biến | **ĐẠT** với các phép kiểm đã viết. **VÁ MỘT PHẦN** với miền của hai lớp còn mở | Hợp đồng ca đích kiểm neo duy nhất, xác nhận `TinHieuChotCa` trên bản tạm. Ca tích hợp dùng model giả. Ma trận r35 chưa thử bullet trong thân khoản và chưa khóa trần chữ số qua CLI. Kết quả và chi tiết đột biến ở dưới. [Ma trận](../scripts/tl_core/llm_route_test.py#L1920) · [Harness](../scripts/tl_core/llm_route_test.py#L2389) |

### Đối chiếu lịch sử #1525

Mỗi dòng áp trạng thái cho biểu hiện gốc của lượt ghi trong cột đầu. Tình trạng toàn miền nằm ở bảng trên và các finding hiện hành. Đã rà lại chuỗi verdict đến exact head r35, đối chiếu điều khoản thay thế và giữ ID theo lượt. [Hồ sơ lượt 1–34](../ops/acceptance/llm-khoan-docx/r1) · [Bảng đối chiếu nguồn lượt 34](../ops/acceptance/llm-khoan-docx/r1/review-34-codex/VERDICT.md)

| Lượt / SHA nguồn | Trạng thái trên r35 và chốt |
| --- | --- |
| 1 · `3d24751` | **ĐÃ VÁ THẬT** phần A1 về kiểm tiêu đề/khối, A2–A4, A5 về chỉ dựng nhãn danh sách dùng, A7–A8. A1 phần cắt, A5 phần đọc ngoài Điều và A6 **HẾT ĐỐI TƯỢNG** theo r7. |
| 2 · `38c481f` | **ĐÃ VÁ THẬT** B1 phần tiêu đề nguyên đoạn, B2 phần số/style, B3–B8. Cắt vùng B1 và duyệt bảng B2 **HẾT ĐỐI TƯỢNG**. |
| 3 · `b0f3cb9` | **ĐÃ VÁ THẬT** C1 phần ngắt tiêu đề, C2 phần nhãn chữ sau Z, C3–C7. Cắt vùng C1 và đếm trong bảng C2 **HẾT ĐỐI TƯỢNG**. |
| 4 · `fa3a8e2` | D1 **HẾT ĐỐI TƯỢNG** với cắt Điều và lùi thô. **ĐÃ VÁ THẬT** D2–D4 và cửa dấu phân cách của D6. D5 có chẩn đoán và giới hạn Strict đã khai. |
| 5 · `3c1e143` | **ĐÃ VÁ THẬT** E2, E5, E6. E1, E3, E4 **HẾT ĐỐI TƯỢNG** theo r7. |
| 6 · `6781d11` | F1 **HẾT ĐỐI TƯỢNG**. **ĐÃ VÁ THẬT** F2 (chặn đoạn có chữ không số sau khoản), F3–F6 (ID, trần số, override/cấp, tab căn lề và mốc move). |
| 7 · `4badb3d` | **ĐÃ VÁ THẬT** G1–G2, G4–G6. G3 **HẾT ĐỐI TƯỢNG** vì thiếu cấp cha bị chặn trước khi dựng nhãn. |
| 8 · `6d28f34` | **ĐÃ VÁ THẬT** H1–H5 bằng chốt tiêu đề, quan hệ part, ca đích, ID style lỗi và ngắt có chữ hiệu lực theo sau. |
| 9 · `4c647c8` | **ĐÃ VÁ THẬT** J1–J5. Cửa `mc:` đã chuyển sang cả part, nhãn không chứa chữ trần. |
| 10 · `674a28c` | **ĐÃ VÁ THẬT** K1–K4 của #1525. |
| 11 · `e1ed11f` | **ĐÃ VÁ THẬT** L1–L6. Phần L2 được bao bởi chốt tiền tố r14. |
| 12 · `f305663` | **ĐÃ VÁ THẬT** M1–M2. Chốt tiền tố giữ riêng với chữ so, tham số nguyên vắng/lỗi bị báo. |
| 13 · `069b734` | **ĐÃ VÁ THẬT** N1–N3 với tiền tố, ID dài và QName đầy đủ. |
| 14 · `0447395` | **ĐÃ VÁ THẬT** Q1–Q2. Kiểm ký tự gốc và hướng dẫn giữ nguyên chữ dẫn chiếu. |
| 15 · `b5cff42` | **ĐÃ VÁ THẬT** R1–R3. Khe trước tiêu đề bổ sung ở lượt 34 đã có chốt r35. |
| 16 · `7a913aa` | **ĐÃ VÁ THẬT** S1–S3. S2 kiểm trên chữ hiệu lực của mọi đoạn. |
| 17 · `8f31901` | **ĐÃ VÁ THẬT** T1–T2 cho phần trong packet. Biến đổi của bộ đọc chung thuộc U2. |
| 18 · `5ed4386` | **ĐÃ VÁ THẬT** U1. U2 thuộc giới hạn số hiệu được duyệt. |
| 19 · `7c4abd7` | **ĐÃ VÁ THẬT** V1–V2 và biểu hiện V4 trên dòng đứng riêng. V3 thuộc giới hạn số hiệu được duyệt. |
| 20 · `8a685fe` | **ĐÃ VÁ THẬT** W2 DOCX và biểu hiện gốc W4–W5. W1, W3 và phần W2 số hiệu thuộc giới hạn đã duyệt. |
| 21 · `3d21bd1` | **ĐÃ VÁ THẬT** X1–X3 ở ca gốc. |
| 22 · `fbddd47` | **ĐÃ VÁ THẬT** Y1–Y3 ở ca gốc, tra style nhập qua miền ID được khóa thêm ở r33. |
| 23 · `30e3e07` | **ĐÃ VÁ THẬT** Z1–Z4 ở ca gốc. |
| 24 · `b755fef` | **ĐÃ VÁ THẬT** A1–A2 ở ca gốc. |
| 25 · `659d9f2` | **ĐÃ VÁ THẬT** B1–B3 ở ca gốc. B1 toàn miền vẫn **VÁ MỘT PHẦN**, xem lớp ranh giới. |
| 26 · `475fee9` | **ĐÃ VÁ THẬT** C1–C2 ở ca gốc. C1 toàn miền vẫn **VÁ MỘT PHẦN**. |
| 27 · `9972282` | **ĐÃ VÁ THẬT** D1 ở ca gốc. D1 toàn miền vẫn **VÁ MỘT PHẦN**. |
| 28 · `0e1c112` | **ĐÃ VÁ THẬT** E1 ở ca gốc. E1 toàn miền vẫn **VÁ MỘT PHẦN**. |
| 29 · `291919e` | **ĐÃ VÁ THẬT** F1–F2 ở ca gốc. F1 toàn miền vẫn **VÁ MỘT PHẦN**. |
| 30 · `749e6ac` | **ĐÃ VÁ THẬT** G1–G2 ở ca gốc. G2 toàn miền vẫn **VÁ MỘT PHẦN**. |
| 31 · `7e9cde7` | **ĐÃ VÁ THẬT** H1–H3 ở ca gốc. H2 toàn miền vẫn **VÁ MỘT PHẦN**. |
| 32 · `571e83f` | **ĐÃ VÁ THẬT** I1 và diện dải chữ có dấu đã có ca của I2. I2 toàn miền vẫn **VÁ MỘT PHẦN**. |
| 33 · `3278bfe` | **ĐÃ VÁ THẬT** J1 trong mẫu r35 và J2 về quay lui cấp số nhân. Lớp nhãn và lớp tài nguyên vẫn **VÁ MỘT PHẦN**. |
| 34 · `a3ef89a` | Ranh giới khoản và ngân sách đọc **VÁ MỘT PHẦN**. Ranh giới ký tự **ĐÃ VÁ THẬT** trong miền hợp đồng; xem bảng chính. |

Với #1514 r9, tiêu đề/câu dẫn (C1, A1/A2/D3/E2/F2), dấu kết và số nội dòng (A3/C2/D1/E1/F1), cùng phép so chữ và xuống dòng (X2–X4) vẫn có chốt và ca. Hai hành vi ghép của G1/H1/J1/K1 đã đóng ở đường thô, theo hợp đồng một dòng. A4 giữ kết quả 8/8 trên ba bản lưu. B1 thuộc bằng chứng launcher. D2 và ngoại lệ số ở cuối dòng của C2 thuộc giới hạn #1514 đã công bố. [Verdict #1514 lượt 10](../ops/acceptance/llm-ranh-gioi-khoan/r1/review-10-codex/VERDICT.md) · [Đặc tả #1514 r9](../ops/specs/llm-ranh-gioi-khoan-r9.md)

## Findings THEO LỚP

| Lớp | Nguồn | Hạng mở cao nhất | Biểu hiện còn mở |
| --- | --- | --- | --- |
| `ranh-gioi-khoan` | K1 #1514, V4 → J1 #1525, lớp lượt 34 trên `a3ef89a` | P2 | Hai biểu hiện cùng ngữ pháp phân nhánh (bullet sau số và thành phần ghép chỉ có dấu tiền tố). |
| `can-tai-nguyen-doc-nguon` | F4/E6, J2, lớp lượt 34 trên `a3ef89a` | P2 | Chốt muộn ở đầu vào thô, chi phí tiền xử lý DOCX, trần dựng kết quả DOCX. |
| `ranh-gioi-ky-tu` | R1/R3/S1/S2/T1/T2/U1/U2, lớp lượt 34 trên `a3ef89a` | Đã đóng trong hợp đồng | Lưới kiểm ký tự ở mọi đoạn và trước khi rẽ chọn vùng. U2 giữ theo quyết định chủ kho. |

### Lớp `ranh-gioi-khoan` [P2] — `scripts/tl_core/llm_route.py:658–671`

- **Bất biến.** Cùng một nhãn có ranh giới nhìn thấy trong miền đã công bố phải bị nhận diện trước khi chấp nhận một dòng làm khoản, kể cả khi nhãn đứng ngay sau số khoản. Hai nguồn thô và hai vị trí phải dùng cùng quy tắc.
- **Miền.** Tập dấu bullet, dấu đầu/giữa/cuối theo `lvlText`, số một cấp và nhiều cấp, placeholder chữ đơn/lặp/ghép và chữ–số, khoảng đệm ngang, thân dính và mở bằng trích dẫn/ngoặc. Xét cả đầu dòng mất số và đầu thân sau số khoản, gồm mọi hình dạng số đơn của `_RE_SO_KHOAN`. Khe thứ nhất là bullet `•` và `+`: `_RE_DIEM` nhận hai dấu này ở đầu dòng, nhưng sau số khoản nhánh `m` chỉ gọi `_nhan_dau`. Hai dấu không nằm trong `_DAU_NHAN` hoặc tập thành phần. Không nhánh nào trong `_RE_NHIEU_CAP` đo hai dấu này. Vì thế số hợp lệ vẫn được nhận và bullet vào thuật ngữ. Các dạng gạch có thể được chặn từ trước bởi nhánh nhiều dấu của regex cũ. Khe thứ hai nằm ở nhãn ghép chữ cùng kiểu có dấu chấm tiền tố và khoảng đệm phân định thân, nhưng thiếu dấu hậu tố. `_nhan_dau` nuốt dấu tiền tố rồi không xác nhận dải chữ, dù còn dấu phân biệt nhìn thấy. Nhánh tiền tố cũ của `_RE_DIEM` chỉ nhận một chữ lặp, nên dòng mất số có thể giữ cả nhãn. Hai nhánh đều nằm sau mọi giới hạn riêng của `extract`. [Dấu và ngữ pháp](../scripts/tl_core/llm_route.py#L524) · [Xác nhận thành phần](../scripts/tl_core/llm_route.py#L632) · [Phân nhánh](../scripts/tl_core/llm_route.py#L658)
- **Ảnh hưởng và hạng.** `_bo_dau_dong` tiêu thụ số thật ở vế đầu. Sau đó bullet không làm hỏng phép cân ngoặc hoặc chốt số nội dòng; dấu kết và từ nối còn có thể hợp lệ. Ở nguồn mất số, nhãn có dấu chấm tiền tố cũng có thể còn nguyên trong khoản. Khi model sao đúng phân đoạn sai đó, `lech_nguyen_van` so theo chính phân đoạn đã nhận. P2 theo K1/J1 vì cần bố cục thô cụ thể, số liên tục nếu có, và đầu ra khớp phân đoạn ấy. Cờ duyệt vẫn đi cùng kết quả. [Kiểm dấu](../scripts/tl_core/llm_route.py#L1646) · [So với phân đoạn](../scripts/tl_core/llm_route.py#L1724) · [ADR-0060 M1–M2](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32)
- **Hint patch.** Phác thảo, chưa áp. Cho một tokenizer giữ offset và vai trò từng token. Dùng chung bảng bullet và dấu `lvlText`, kiểm nhãn trước khi tách số khoản, sau đó gọi lại đúng phép nhận nhãn từ offset đầu thân. Nhãn có dấu tiền tố phải giữ thông tin dấu cho quyết định cuối, kể cả dải ghép chữ. Dùng span tách được để kiểm cân ngoặc trên đúng thân. Đưa các đối chứng đã duyệt vào cùng một bảng ngoại lệ. Thay `_RE_NHIEU_CAP` và phần nhận nhãn của `_RE_DIEM` bằng quyết định của tokenizer sau khi đối chiếu mọi ca lịch sử. Dấu bullet đi thẳng vào cùng kết quả `nhan`, nên cả hai vị trí nhận diện đồng nhất.
  
  ```text
  quet_nhan_dau_dong(dong):
      tokens = doc_tien_to(dong, DAU_LVLTEXT, BULLET)
      ket_qua = phan_loai(tokens, cho_phep_so_khoan_don=True)
      nếu ket_qua là số đơn và phan_loai_tai(ket_qua.dau_than, cho_phep_so_khoan_don=False) là nhãn:
          trả nhãn
      trả ket_qua cùng span thân dùng cho kiểm dấu
  ```

- **Hint test.** Dùng ma trận kiểu nhãn × vị trí (dòng mất số, đầu thân có/không đệm sau số) × dạng số đơn. Đưa toàn bộ bullet, dấu tiền tố/giữa/hậu tố, chữ lặp/ghép và thân có ngoặc/nháy vào ca âm. Cần chứng minh cả `tach_khoan` từ chối và phép so báo chưa xác minh. Giữ đối chứng viết tắt hoa đầu, từ ghép, mã hạng, thân mở bằng cụm ngoặc, ca K1 hai dòng và fixture 8 khoản. Đột biến bỏ đọc span thân, bỏ terminal bullet hoặc bỏ sử dụng dấu tiền tố phải làm đỏ ca đích.
- **Vùng giao đã khai.** Việc cho phép `Tp.`, `Ths.` theo kiểu chữ hoa đầu là hợp lý nếu giữ cho đúng dải hoa đầu + chữ thường giống chữ viết tắt. Dấu mở ngoặc sát thân có thể trùng hình dạng dấu nhãn, còn nhãn chỉ cách bằng trắng có thể trùng từ đầu thân. Giữ các giới hạn quanh những dạng thực sự không phân biệt được. Câu giới hạn đề xuất là “Khi dấu mở nằm sát cả nhãn lẫn thân, hoặc cách viết nhãn trùng một từ viết tắt hay một phần thân hợp lệ, văn bản thô cần người duyệt ranh giới. Bullet và dấu tiền tố nhận diện được vẫn bị chặn.” Phần sửa này không cần nới giới hạn để bao hai biểu hiện trên. [§2.37](../ops/specs/llm-khoan-docx-r35.md#L412)

### Lớp `can-tai-nguyen-doc-nguon` [P2] — `scripts/tl_core/ops_misc.py:3060,3095` · `scripts/tl_core/llm_route.py:690,1122,1527`

- **Bất biến.** Ngân sách phải chặn trước phép đọc, mở rộng hoặc gọi model cần giới hạn. Mỗi nguồn trong miền có chi phí theo byte/node/token đã giới hạn. Khi vượt, CLI trả lỗi nguồn có kiểm soát trước model và đầu ra cấu trúc báo `ValueError`.
- **Miền.** (1) Text local đọc toàn tệp rồi strip trước khi chốt 400.000 ký tự. Đường số hiệu nhận stdout/stderr đã capture, có timeout và chốt trần export riêng. Trần ứng dụng vẫn chạy sau khi đã có toàn bộ chữ. Trần 4 chữ số chỉ có ở `quet_nhan_dau_dong`, gọi từ `lech_nguyen_van` sau `goi`. Cả hai đường thô có thể tiêu một lượt model cho dòng vượt trần chữ số và chỉ báo lệch rc 5 nếu model trả hợp lệ. (2) DOCX có giới hạn byte từng member và trần sâu, nhưng parse tạo cây trước khi đếm sâu, và chưa chặn chiều rộng/số node/gói trước cấp phát. Duyệt chuỗi `basedOn` lặp theo đoạn/run, có thể nhân số tham chiếu với độ dài chuỗi dù XML nông. `_nhan` chạy regex có hai vế lặp cùng ngữ pháp quanh một placeholder bắt buộc, dễ xét lại đuôi khi có nhiều vị trí đặt placeholder và metadata sai ở cuối. Sau đó cả `re.sub` và `strip` đã tạo chuỗi rồi mới đo 64. (3) Dựng Điều gom dòng bằng list đã loại chi phí nối lặp, nhưng chốt tổng sau khi đã phân tích mọi đoạn, giữ nội dung và nối chuỗi từng khoản. Phép cộng thêm một cho mọi dòng còn tính một ký tự phân cách sau dòng cuối. Điều dựng đúng 400.000 ký tự bị từ chối theo công thức hiện tại. [Đọc tệp](../scripts/tl_core/ops_misc.py#L3054) · [Điểm gọi model](../scripts/tl_core/llm_route.py#L1862) · [ZIP/XML](../scripts/tl_core/llm_route.py#L1379) · [Chuỗi style](../scripts/tl_core/llm_route.py#L1068) · [Nhãn](../scripts/tl_core/llm_route.py#L1102) · [Tổng](../scripts/tl_core/llm_route.py#L1525)
- **Ảnh hưởng và hạng.** P2 vì nguồn ngoài ngân sách có thể gây chậm, thất bại tài nguyên hoặc tiêu model sai hợp đồng trong một lệnh cục bộ. Chốt tổng sai một ký tự gây chặn oan ở đúng biên. Các nhánh này chưa chỉ ra kết quả sai vượt xác minh. Ngưỡng công bố cho Điều dài là lựa chọn hợp lý. Khoảng cách nằm ở vị trí áp ngưỡng, sự nhất quán với chữ đã chuẩn hóa và chi phí nạp metadata đứng trước nó. [§2.37](../ops/specs/llm-khoan-docx-r35.md#L423)
- **Hint patch.** Phác thảo, chưa áp. Dùng hợp đồng ngân sách ngay ở bộ tiếp nhận nguồn. Đọc UTF-8 có giới hạn trên dữ liệu đã giải mã và có giới hạn byte I/O tương ứng. Dùng kết quả tiền kiểm cho CLI lẫn phép so, với lý do riêng cho quá số chữ số để CLI trả rc 2 trước model, và giữ luồng rc 5 cho phân đoạn mơ hồ theo hợp đồng hiện có. Phía DOCX, kiểm chi phí ZIP khi mở gói, áp giới hạn tổng/member và sâu/node ở parser, tính trước thông tin style một lần cho mỗi ID hợp lệ. Quét token `lvlText` một lần, ghi độ dài tăng dần, chặn trước khi dựng chuỗi. Trừ ngân sách Điều khi thêm đoạn/nhãn và tính đúng số dấu xuống dòng giữa các dòng. Mọi cửa đọc đi qua ngân sách trước thao tác tương ứng.
  
  ```text
  doc_nguon:
      đọc có giới hạn và kiểm ngân sách theo từng loại nguồn
      nếu thô: kiểm tiền tố số trong lượt quét, giữ kết quả phân đoạn hoặc lý do
      nếu DOCX: nạp metadata có giới hạn, dựng kết quả khi còn đủ ngân sách
      trả van_ban và kết quả phân đoạn
  cmd_llm_khai_niem:
      lỗi quá ngân sách → rc 2
      gọi model, rồi so với kết quả phân đoạn đã đọc
  ```

- **Hint test.** Kiểm đúng trần và ngay trên trần, gồm chữ Unicode/biên trắng, số khoản 4 và trên 4 chữ số trên cả hai đường thô. Với model giả, khẳng định số lời gọi bằng 0 ở lỗi ngân sách. Phủ XML sâu và rộng, part quan hệ, chuỗi style tái sử dụng, metadata nhãn trước mở rộng và cả tổng nhiều đoạn nhỏ thay vì chỉ một đoạn lớn. Đột biến đẩy chốt ra sau model/parse/mở rộng hoặc tính thừa dấu xuống dòng cuối phải làm đỏ nhóm tương ứng. Dùng đếm byte/node/token trước các kiểm thời gian để khóa vị trí chốt.

## Kết quả test và đột biến

Môi trường Linux x86_64, Python 3.13.18, Git 2.43.0, Codex CLI 0.172.0, Ruff 0.15.15. Git dùng `core.abbrev=7`, bytecode tắt, cache và log tại `/tmp/wp1525-r35-review.PK5KSHNU`. Các lệnh đo head ở đầu báo cáo, trừ các hàng ghi rõ base. Lượt chạy trên cây bàn giao phát sinh fixture/cache ignored. Hai thư mục ấy đã được chuyển vào scratch của run sau khi selftest kết thúc; kiểm Git sau đó chỉ thấy tệp verdict và thư mục rỗng ignored có sẵn. Bản sao sạch detached dùng Git objects cục bộ cho phép đo release strict và đối chứng baseline.

| Lệnh | Phạm vi, trạng thái, rc | Bằng chứng dương hoặc chẩn đoán |
| --- | --- | --- |
| `python scripts/tl_core/llm_route_test.py` | Head, `passed`, rc 0 | **64/64 ca, 275/275 đột biến**, gồm 178/178 mục `wp1525_*`. `llm.log` SHA-256 `4ed665b5a2959aaa8e2082c018d44bf6e25a903ab093fd99173d49f144b609c1`. |
| `python scripts/tl.py --deterministic workflow-audit --strict --json` | Head, `passed`, rc 0 | `ok=true`, 26 card, 11 nhóm, 60 task, 194 lệnh khả dụng, 0 lỗi/cảnh báo. `workflow.log`. |
| `python scripts/tl.py --deterministic golden-test --json` | Head, `passed`, rc 0 | `ok=true`, **20/20**, 20/20 projection ổn định và 20/20 stdout ổn định. `golden.log`. |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | Head có tệp verdict, `failed`, rc 2. Bản sao sạch cùng head, `passed`, rc 0 | Lần đầu 187/187 khớp, strict báo đúng một tệp thừa `.review/VERDICT.md`. Bản sao sạch `ok=true`, expected = checked = **187**, 0 thiếu/thừa/lệch, package hash khớp. `release.log`, `release-clean.log`. |
| `python ops/lease_publish.py check --root . ops/leases/llm-khoan-docx-r35-g1-claude.yaml` | Head, phần cục bộ `passed`, rc 0 | Validator in “ĐĂNG ĐƯỢC” cho đúng lease, issue và base. Nó ghi rõ hai lớp GitHub bị bỏ qua; ghi `skipped` cho hai lớp đó. `lease.log`. |
| `python scripts/tl.py --selftest` | Head, `failed`, rc 1 | **1774/1790**, transport **12/12**, ca `r1525_llm_khai_niem_tep_docx_cau_truc` đạt. `selftest-head.log`. |
| `python scripts/tl.py --selftest` | Base, `failed`, rc 1 | **1773/1789**, transport **12/12**. `selftest-base.log`. |
| `python scripts/tl.py --deterministic determinism-audit --strict --json` | Head, `passed`, rc 0 | `ok=true`, **15/15**. `determinism.log`. |
| `python scripts/tl.py --deterministic doc-claims-check --strict --json` | Head và base, `failed`, rc 2 mỗi cây | Mỗi cây quét 131 tệp, cùng một cờ cứng `SHA_NOT_A_COMMIT` cho `9941d8af52aeede1c78ea4e232fbe9a8d5272033` tại protocol dòng 1680. Object vắng trong checkout shallow, `git cat-file -t` rc 128. `claims-head.log`, `claims-base.log`. |
| `loi_ruff_ci()` từ `.claude/dev/ci_dang_ky_test.py` qua `python -B -c` | Head, pin/probe `passed`, rc 0 | `RUFF_CONTRACT 3 []`. `ruff-contract.log`. |
| `python -m ruff check --no-cache --select F scripts/tl.py` | Head và base, bare lint `failed`, rc 1 mỗi cây. Delta F `passed` | 12 lỗi mỗi cây, hai log trùng byte, SHA-256 `5fe63d91f6092b479ca73219b31e3c3554a23019e5c1e35861755990b5f9513c`. `ruff-head.log`, `ruff-base.log`. |
| Windows exact SHA theo M3, provenance CI/GitHub theo §10.2 | `not_run` | Diff có dòng Python với `encoding=` nên M3 yêu cầu Windows. Phạm vi đo lượt này là Linux offline. [ADR-0060 M3](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L41) |

Tập ID selftest đỏ của head và base trùng byte sau khi lọc và sắp thứ tự. SHA-256 của danh sách `9a408c897ef51a8232ff433d755334c1d1187fe0bb67e2f75a3bd5836b15a139`. Gồm 8 ca `r973_bootstrap_*`, 5 ca `wp433_*` và `wp727_tl_gws_refresh` trong môi trường có `/tmp/.git` rỗng, cộng `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` và `r268_l2_trichotomy_theo_trang_thai_object`. Delta tập lỗi bằng 0; selftest N/N vẫn đỏ. SHA-256 log head `32f2cd6cb044b44ed0fdf8323ca43381c5eb031213a2594fc7273aba3e8e6155`, log base `a50b9d72a58af1a3148a7cd7a43bc65a46ea2b1d96303445901ff6a3742851fd`.

Đột biến dùng `DOT_BIEN` sẵn có. Harness đọc mã gốc, áp mỗi bộ neo duy nhất trong bản sao module dưới `/tmp`, và chỉ đếm bị giết khi ca đích ném `TinHieuChotCa`. Head ghi 0 đột biến sống, lọt vì lỗi nạp, hoặc không áp được. Nhóm r35 gồm 7 đột biến bộ quét, 6 đột biến ngân sách và 1 đột biến vị trí chốt ký tự. Phép chạy phụ `python -B -m pdb scripts/tl_core/llm_route_test.py` trên bản sao head với breakpoint `2416`, điều kiện `ten.startswith("wp1525_")`, ghi dương 10 tín hiệu đầu của nhóm r35, gồm bỏ quét đầu thân/đầu dòng, ranh giới, trì hoãn xác nhận, đệm nối, hai đối chứng ngoại lệ, trần chữ số, trần thô và quét dấu kết. Log phụ có lỗi lệnh PDB `end` và chỉ ghi 10 breakpoint dù suite con rc 0, nên phép đếm 178/178 dựa trên harness thường và bảng khai báo. Các đột biến XML sâu, nhãn dài, tổng DOCX và chốt ký tự nằm trong tổng đã đo. [Bảng r35](../scripts/tl_core/llm_route_test.py#L2003) · [Harness](../scripts/tl_core/llm_route_test.py#L2389)

## Không đo được

- Các biểu hiện mới của hai lớp P2 là suy luận đọc mã. Các ca đầu-cuối chính xác cho nhãn, số khoản quá dài qua CLI, tải ZIP/XML/style và ngưỡng tổng DOCX cần fixture mới. Ca sẵn kiểm các phần đã nêu trong bảng kết quả.
- Dạng DOCX thường gặp bị chặn oan ngoài giới hạn công bố chưa có bằng chứng dương trong các mẫu sẵn có. Tab/ptab, hyperlink, content control, bookmark, proof/permission/comment markers và ngắt trình bày đã có nhánh xử lý. Wrapper hướng chữ `w:dir`/`w:bdo` sẽ rơi vào nhánh lạ theo mã; tần suất ở export Word/Google Docs và tiếng Việt chưa được đo. Chưa khẳng định render phức tạp của Word cho mốc move, style ẩn hay content control có liên kết dữ liệu. [Danh sách phần tử](../scripts/tl_core/llm_route.py#L776) · [Quét nội dòng](../scripts/tl_core/llm_route.py#L1315)
- Live, model thật, gói export Word/Google Docs ngoài fixture, CI/GitHub và Windows thuộc `not_run`. Thông tin model/effort phục vụ và rc/stdout terminal của đúng launcher run chưa đo được trong phiên tạo tệp.

