# Verdict packet #1525 r30 lượt 30 — Codex

reviewed_sha: 749e6ac89c770a59f353e5f3dd40ce82deae7715
reviewed_tree: 94aba3284fcb64bb3e9ee6203b6ad36422bf1d77
base_sha: 64b7f2c14776d5d0e1d34a6be4725490956f5bec
base_tree: 0cc14e79cecd2ce44bc4dc6cff92cadb31fd7ee4

## Phạm vi và preflight

- Reviewer độc lập `openai_codex / codex_cli / machine`, run launcher `b4b028e76860478282e99618287bf767`. Executor ghi trong lease là `claude / claude_code / machine/local`, tương ứng `anthropic_claude` trong bảng provider. Sandbox thực tế `workspace-write`. Class khai báo và hiệu lực cùng là `sensitive`. SHA-256 của prompt là `6943135f6570a3a2a36244d359e07c2a60afb291590db49981b01bd3c886c4b2`, khớp checkpoint cùng exact SHA. [Checkpoint](../../run/b4b028e7/checkpoint.json) · [Run](../../run/b4b028e7/run.json) · [Bảng provider](../ops/KE_HOACH_THI_CONG_DA_PROVIDER.md#L26)
- Checkout detached của `ducthangho/tra-luat` có ref local `ccr-89c0d2e2-inanqb` trỏ đúng head, merge base đúng SHA giao review. Diff bản vá từ `3bfed5fa820641f9332d65fa4e32a7254cf667d9`, diff packet từ `fcb12b3873c3bec2c339029136243ed2c804ce05`, diff toàn PR từ base trên. Lease r30/g1 hết hạn 2026-11-26 21:10 UTC, có 29 lời gọi trước lượt 30 và inference budget 0. Spec trên đĩa và Git blob head có SHA-256 `c2214b70bae3917be476ed8bb16087e919117c760c6fd00fbebc60b1ba247893`, khớp lease. Quyền đứng nâng trần và ngoại lệ M5 được ghi trong spec. [Lease](../ops/leases/llm-khoan-docx-r30-g1-claude.yaml) · [Spec](../ops/specs/llm-khoan-docx-r30.md)
- Write set khai 161 đường dẫn, SHA-256 sau sắp xếp `b2a9c439110d4f329a7f34a7124977c0b3d54a4d44e4db12f9ea3757a429268c`. Diff bản vá có 8/8 đường dẫn thuộc lease. Diff packet có 161 đường dẫn, trong đó 157/157 thuộc lease sau khi trừ 4 hồ sơ #1514 theo prompt. Diff toàn PR có 205 đường dẫn, gồm 48 đường dẫn hồ sơ, lease và spec kế thừa từ #1514 ngoài write set r30. Kiểm 30/30 cặp bia mộ hai chiều từ #1514 r9 ⇄ #1525 r1 ⇄ … ⇄ r30, 31/31 hash spec trên đĩa và Git blob. Cùng branch, base và generation. [Bia mộ #1514](../ops/leases/llm-ranh-gioi-khoan-r9-g1-claude.yaml#L97) · [Tiền nhiệm r30](../ops/leases/llm-khoan-docx-r29-g1-claude.yaml#L198)

## Đối chiếu lượt 29 và đặc tả r30

| Mục | Trạng thái | Bằng chứng |
| --- | --- | --- |
| Lượt 29 F2 · §2.32 | **ĐÃ VÁ THẬT** biểu hiện ID vắng. **VÁ MỘT PHẦN** lớp | `pStyle` có ID vắng đánh dấu đoạn lạ và chặn khi định vị Điều. Mutant bỏ chốt chết ở ca đích. ID có mặt nhưng sai loại vẫn đi qua phép tra hiện tại, xem G1. [Bản vá](../scripts/tl_core/llm_route.py#L1098) · [Ca F2](../scripts/tl_core/llm_route_test.py#L1710) |
| Lượt 29 F1 · §2.28–§2.32 | **ĐÃ VÁ THẬT** các dạng nhiều dấu cuối đã báo. **VÁ SINH LỖI MỚI** ở biên giữa số khoản và thân | Chốt nhiều thành phần nhìn trước số đơn, mutant nâng ngưỡng từ hai lên ba dấu chết ở ca đích. Chốt mới có thể lấy dấu mở ngoặc của thân làm dấu thứ hai của nhãn. Miền chặn trước số đơn vẫn hở với số–dấu–chữ kết thúc bằng placeholder, xem G2. [Chốt r30](../scripts/tl_core/llm_route.py#L526) · [Ưu tiên nhánh](../scripts/tl_core/llm_route.py#L1436) |
| §1, §2.2–§2.3 · K1 #1514 | **ĐÃ VÁ THẬT** hai cơ chế đã báo | Dòng điểm có nhãn thông dụng bị chặn cả nguồn có số lẫn mất số. Dòng tiếp mở bằng “là” trong nguồn có số rơi vào nhánh dòng thiếu số. Ở nguồn mất số, phép so loại mục thiếu vế thuật ngữ. Ba đầu ra lưu sẵn của Điều 3 Luật 134/2025/QH15 vẫn đủ 8/8 trong suite. Route model và cờ `can_nguoi_duyet: true` được giữ. [K1 gốc](../ops/acceptance/llm-ranh-gioi-khoan/r1/review-10-codex/VERDICT.md#L35) · [CLI](../scripts/tl_core/ops_misc.py#L3130) |
| §2.1, §2.4–§2.17 · vị trí Điều, câu dẫn, điểm | **ĐÃ VÁ THẬT** các biểu hiện còn trong hợp đồng. **HẾT ĐỐI TƯỢNG** với luật cắt cuối Điều, đếm qua bảng và nhận điểm tay thành đoạn riêng | Tiêu đề khớp nguyên đoạn, đúng số và mở đầu nội dung. Cây khối giữ thứ tự tài liệu, chặn bảng/khối lạ, kiểm tiền tố cấu trúc trên mọi đoạn còn lại đến hết tệp. Sau khoản đầu, mỗi đoạn có chữ đều cần đánh số. Trước khoản đầu, chỉ có tối đa một câu dẫn chuẩn khớp cả đoạn. Thiếu đánh số tự động ném `ValueError`, CLI trả rc 2, lối `KhongCauTruc` đã bị gỡ. [Duyệt khối](../scripts/tl_core/llm_route.py#L993) · [Ranh giới](../scripts/tl_core/llm_route.py#L1298) · [Câu dẫn](../scripts/tl_core/llm_route.py#L1388) · [CLI](../scripts/tl_core/ops_misc.py#L3037) |
| §2.4–§2.15, §2.22–§2.26 · số Word | **ĐÃ VÁ THẬT** các biểu hiện đã báo trong miền hỗ trợ | `start` mặc định 0, `startOverride` thay giá trị cấp. Đếm từng `numId`, xóa trạng thái cấp con khi cấp cha tăng và chặn nhảy qua cấp chưa xuất hiện. Ghép khoản buộc một danh sách, cấp khoản thập phân và nhãn đúng cấp, số từ 1 liên tục. Các chốt ID/cấp trùng, thuộc tính đơn trị, style/kiểu restart ngoài miền và trần 999 được đối chiếu với ca sẵn có. [Định nghĩa](../scripts/tl_core/llm_route.py#L783) · [Bộ đếm và ghép](../scripts/tl_core/llm_route.py#L1270) |
| §2.5–§2.13, §2.23–§2.29 · chữ còn hiệu lực | **ĐÃ VÁ THẬT** các biểu hiện gốc về sửa văn bản và khoảng trắng. Lớp phân giải style còn mở ở G1 | Đọc XML gốc, đánh giá gạch đơn/kép riêng, định dạng trực tiếp ghi đè, nhiều toggle chưa giải được thì chặn. Bỏ chữ trong `del`/`moveFrom`, giữ `ins`/`moveTo`, chặn sửa dấu đoạn và move mất cặp. Dùng chung đọc chữ theo `xml:space`, giữ phần chỉ có phân cách. Cờ ngắt và phần tử lạ tính sau khi đã lọc run. [Đọc run](../scripts/tl_core/llm_route.py#L1083) · [Sửa dấu đoạn](../scripts/tl_core/llm_route.py#L1253) |
| §2.14–§2.21 · part, tiền tố và ký tự | **ĐÃ VÁ THẬT** trong miền công bố | Quan hệ part dùng URI Transitional đầy đủ, tương đối theo part chính, XML chính đọc từ bytes. Khối dùng QName, chữ được kiểm trước quyết định nhận đoạn và đường thô kiểm trước tách dòng, bỏ một BOM. Chặn chữ ngoài tập và dẫn chiếu mở đoạn thuộc giới hạn đã khai. [Quan hệ](../scripts/tl_core/llm_route.py#L742) · [Ký tự](../scripts/tl_core/llm_route.py#L622) · [Vùng](../scripts/tl_core/llm_route.py#L1320) |
| §2.22–§2.23 · đường số hiệu | **ĐÃ VÁ THẬT** ở chốt strict. U2, V3, W1, W3 và phần số hiệu của W2 thuộc giới hạn đã duyệt | CLI dùng `tl extract --markup-strict`, kiểm rc, mốc Điều và tín hiệu cắt trần. Làm sạch cache, regex cắt Điều và kết quả lọc markup của bộ đọc dùng chung thuộc các giới hạn đã khai. G2 nằm trong bộ tách thô sau lớp đọc nguồn, gồm cả `--tep` văn bản. [Lời gọi extract](../scripts/tl_core/llm_route.py#L1672) · [Giới hạn](../ops/specs/llm-khoan-docx-r30.md#L267) |
| §3 · so nguyên văn, CLI, đột biến | **ĐẠT** trên các ca hiện có | Phép so giữ số lượng, thứ tự, số khoản, cả hai vế và dòng điểm. DOCX lấy từ nối ở đoạn mở khoản. CLI chỉ ghi `--out` khi khớp, định tuyến vẫn nhận danh sách khoản cấu trúc làm nguồn so. Các ca cũ và mới đi qua harness, xem kết quả bên dưới. Khi bộ đọc đã dựng sai nguồn như G1/G2, model và phép so có thể cùng dùng một nguồn sai. [Phép so](../scripts/tl_core/llm_route.py#L1571) · [Ghi đầu ra](../scripts/tl_core/ops_misc.py#L3136) |

### Các finding lịch sử

Các ID dưới đây đọc cùng số lượt. Trạng thái đóng áp dụng cho biểu hiện gốc với neo thực thi ở bảng trên. G1/G2 giữ các slug lớp cũ.

| Lượt #1525 | Đối chiếu trên r30 |
| --- | --- |
| [1](../ops/acceptance/llm-khoan-docx/r1/review-1-codex/VERDICT.md) | A1 phần cắt và A6 **HẾT ĐỐI TƯỢNG**. Phần còn lại của A1 và A2–A5, A7–A8 **ĐÃ VÁ THẬT**. Chữ gạch do phân giải style thuộc G1. |
| [2](../ops/acceptance/llm-khoan-docx/r1/review-2-codex/VERDICT.md) | Phần cắt của B1 và đếm bảng của B2 **HẾT ĐỐI TƯỢNG**. Phần còn lại của B1/B2 và B3–B8 **ĐÃ VÁ THẬT**. Chốt gạch kép độc lập, nối không ngắt thành dấu gạch, metadata wrapper không cản văn bản. |
| [3](../ops/acceptance/llm-khoan-docx/r1/review-3-codex/VERDICT.md) | C1 về điểm cắt và C2 về đếm hàng/ô **HẾT ĐỐI TƯỢNG**. Phần còn lại C1/C2 và C3–C7 **ĐÃ VÁ THẬT**. Chốt ngắt, nhãn chữ lặp sau Z, ngoặc/trích dẫn, toggle và content control. |
| [4](../ops/acceptance/llm-khoan-docx/r1/review-4-codex/VERDICT.md) | D1 phần cắt **HẾT ĐỐI TƯỢNG**, phần bỏ fallback **ĐÃ VÁ THẬT**. D2–D4/D6 **ĐÃ VÁ THẬT**. D5 thuộc giới hạn DOCX Strict đã khai. |
| [5](../ops/acceptance/llm-khoan-docx/r1/review-5-codex/VERDICT.md) | E1/E3/E4 **HẾT ĐỐI TƯỢNG**. E2/E5/E6 **ĐÃ VÁ THẬT**. Có ca toggle nhiều tầng, đọc cây gốc, move và miền cấp. |
| [6](../ops/acceptance/llm-khoan-docx/r1/review-6-codex/VERDICT.md) | F1 cắt cuối và F2 nhận điểm gõ tay **HẾT ĐỐI TƯỢNG**. F3–F6 **ĐÃ VÁ THẬT** qua chuẩn hóa ID, trần số, ca cấp override, `ptab` và kiểm cặp move. |
| [7](../ops/acceptance/llm-khoan-docx/r1/review-7-codex/VERDICT.md) | G1–G6 **ĐÃ VÁ THẬT**. Chốt ID/cấp tổ tiên, đọc part styles theo quan hệ, ngắt trang/cột cuối đoạn và tiêu đề không phân biệt hoa thường. |
| [8](../ops/acceptance/llm-khoan-docx/r1/review-8-codex/VERDICT.md) | H1–H5 **ĐÃ VÁ THẬT**. Chốt tiền tố Điều, quan hệ gốc, mutant part đổi tên, numId lỗi qua style và chữ sau ngắt. |
| [9](../ops/acceptance/llm-khoan-docx/r1/review-9-codex/VERDICT.md) | J1–J5 **ĐÃ VÁ THẬT**. Chặn đánh số qua style, phần tử mc, nhãn ngoài miền. Đọc rels của part chính và chỉ tính chữ còn hiệu lực sau ngắt. |
| [10](../ops/acceptance/llm-khoan-docx/r1/review-10-codex/VERDICT.md) | K1–K4 **ĐÃ VÁ THẬT**. Kiểm mc ở ba part, tiêu đề viết thứ tự bằng chữ, khớp toàn `lvlText`, sửa mô tả hành vi đọc hết tệp. |
| [11](../ops/acceptance/llm-khoan-docx/r1/review-11-codex/VERDICT.md) | L1–L6 **ĐÃ VÁ THẬT**. URI kiểu đầy đủ, cấm tiền tố Điều, giới hạn tiêu đề lớn, thuộc tính số lỗi có chẩn đoán, parse bytes và cập nhật hướng dẫn. |
| [12](../ops/acceptance/llm-khoan-docx/r1/review-12-codex/VERDICT.md) | M1–M2 **ĐÃ VÁ THẬT**. Cấm tiền tố độc lập dấu cuối, giá trị số/cấp và mốc move thiếu ID có chẩn đoán. |
| [13](../ops/acceptance/llm-khoan-docx/r1/review-13-codex/VERDICT.md) | N1–N3 **ĐÃ VÁ THẬT**. Chiếu dấu trước dò tiền tố, chuẩn hóa ID bằng chuỗi, chọn khối bằng QName. |
| [14](../ops/acceptance/llm-khoan-docx/r1/review-14-codex/VERDICT.md) | Q1/Q2 **ĐÃ VÁ THẬT**. Chốt ký tự gốc và hướng dẫn giữ nguyên lời dẫn chiếu. |
| [15](../ops/acceptance/llm-khoan-docx/r1/review-15-codex/VERDICT.md) | R1–R3 **ĐÃ VÁ THẬT**. Cấm ký tự lạ trước gộp, nhận số gõ tay ngoặc kín, giữ chốt ký tự ở đường thô. |
| [16](../ops/acceptance/llm-khoan-docx/r1/review-16-codex/VERDICT.md) | S1–S3 **ĐÃ VÁ THẬT**. Tập cho phép thay danh sách cấm, kiểm trước tách dòng, cho qua mốc quyền chỉnh sửa. |
| [17](../ops/acceptance/llm-khoan-docx/r1/review-17-codex/VERDICT.md) | T1/T2 **ĐÃ VÁ THẬT** tại cửa vào packet. Số mũ ra khỏi tập, chỉ một lớp bỏ BOM, producer dùng chung thuộc U2. |
| [18](../ops/acceptance/llm-khoan-docx/r1/review-18-codex/VERDICT.md) | U1 **ĐÃ VÁ THẬT**, miền chữ số chỉ còn ASCII. U2 là giới hạn đã duyệt. |
| [19](../ops/acceptance/llm-khoan-docx/r1/review-19-codex/VERDICT.md) | V1/V2/V4 **ĐÃ VÁ THẬT**. Strict, chặn số mặc định đoạn, chặn nhãn chữ kết chấm. V3 là giới hạn đã duyệt. |
| [20](../ops/acceptance/llm-khoan-docx/r1/review-20-codex/VERDICT.md) | W2 DOCX và W4/W5 **ĐÃ VÁ THẬT**. Giữ mẩu phân cách, chặn nhãn hoa/lặp và cấp hoặc override trùng. W1/W3 và W2 số hiệu là giới hạn đã duyệt. |
| [21](../ops/acceptance/llm-khoan-docx/r1/review-21-codex/VERDICT.md) | X1–X3 **ĐÃ VÁ THẬT**. Giữ tab/ngắt thuần, kiểm trường đơn trị, chặn nhãn chữ nối gạch có khoảng đệm. |
| [22](../ops/acceptance/llm-khoan-docx/r1/review-22-codex/VERDICT.md) | Y1–Y3 **ĐÃ VÁ THẬT** cho các dạng đã báo. Dùng chung đọc ruột, chốt nút chọn vùng và ID style trùng, nhận khoảng đệm nhãn. |
| [23](../ops/acceptance/llm-khoan-docx/r1/review-23-codex/VERDICT.md) | Z1–Z4 **ĐÃ VÁ THẬT**. Nhận phần tử lạ trong mẩu bỏ, chặn ZIP trùng, nhãn số–số có ngoặc, mutant đơn trị riêng. |
| [24](../ops/acceptance/llm-khoan-docx/r1/review-24-codex/VERDICT.md) | A1/A2 **ĐÃ VÁ THẬT**. Kế thừa `xml:space`, chốt nhãn hai số kết gạch. |
| [25](../ops/acceptance/llm-khoan-docx/r1/review-25-codex/VERDICT.md) | B1 **VÁ MỘT PHẦN** theo G2. B2/B3 **ĐÃ VÁ THẬT** qua mutant đặt lại `xml:space`, phần chữ đã bỏ, `delText` lạc và cờ ngắt. |
| [26](../ops/acceptance/llm-khoan-docx/r1/review-26-codex/VERDICT.md) | C1 **ĐÃ VÁ THẬT** dạng số đa cấp đã báo, **VÁ MỘT PHẦN** lớp theo G2. C2 **ĐÃ VÁ THẬT** với phần tử lạ trong run đã bỏ. |
| [27](../ops/acceptance/llm-khoan-docx/r1/review-27-codex/VERDICT.md) | D1 **ĐÃ VÁ THẬT** với dạng số–chữ có dấu cuối và các dạng cũ trong ca, **VÁ MỘT PHẦN** lớp theo G2. |
| [28](../ops/acceptance/llm-khoan-docx/r1/review-28-codex/VERDICT.md) | E1 **ĐÃ VÁ THẬT** dạng có dấu đầu theo hai mutant đích, **VÁ MỘT PHẦN** lớp theo G2. |
| [29](../ops/acceptance/llm-khoan-docx/r1/review-29-codex/VERDICT.md) | F1/F2 theo hai dòng đầu của bảng đối chiếu. |

Với #1514, K1 và các biến thể ghép dòng G1/H1/J1 **ĐÃ VÁ THẬT**. A1/A2/D3/E2/F2 về câu dẫn, C1 về tiêu đề dính thân và A3/C2/D1/E1/F1 về dấu kết hoặc số nội dòng vẫn có chốt và ca lịch sử. A4 vẫn có đối chứng 8/8, D2 và phần C2 đã công bố thuộc giới hạn đường thô. B1 lượt 1 về bề mặt đã được giải quyết trong run hiện hành. Khi nguồn mất toàn bộ thông tin cấp, hai dòng tự đủ hai vế và dấu kết vẫn có thể thành hai khoản. Dấu số tiểu mục trùng hình dạng và trùng số khoản thật qua cùng nhánh số đơn. Đây là các giới hạn ranh giới đã khai. G2 chỉ ra phần có dấu thuộc miền nhãn đã cam kết và chặn oan mới của r30. [Lịch sử #1514](../ops/acceptance/llm-ranh-gioi-khoan/r1/review-10-codex/VERDICT.md#L35) · [Ca lịch sử](../scripts/tl_core/llm_route_test.py#L1073) · [Phạm vi thô](../scripts/tl_core/llm_route.py#L1404)

## Findings

### G1 [P1] Tham chiếu style có ID đúng nhưng sai loại vẫn làm sai chữ gạch — `scripts/tl_core/llm_route.py:917`, `:1100`

**Kịch bản.** Đoạn khoản đánh số trực tiếp có `pStyle` tham chiếu một ID tồn tại nhưng thuộc character style. Style đoạn mặc định mang gạch và style ký tự bị tham chiếu không mang gạch. Tiêu đề dùng style đoạn rõ ràng. Khi tham chiếu sai loại bị bỏ qua, style đoạn mặc định áp dụng. Cơ chế ngược cũng xảy ra khi `rStyle` trỏ vào một paragraph style mang gạch. Bộ đọc có thể bỏ chữ còn hiệu lực do áp nhầm style đoạn lên run.

**Căn cứ.** `_doc_kieu` đưa mọi style vào một bảng theo ID, đọc `w:type` để chọn style đoạn mặc định rồi bỏ loại khỏi tuple lưu. Chốt F2 chỉ kiểm có ID trong bảng. Cả phép tính gạch đoạn và gạch run đều gọi cùng hàm đi chuỗi ID không phân loại. Vì số khoản khai trực tiếp, chốt đánh số theo style không loại được đoạn. Đối chiếu cục bộ với cách tra style của python-docx 1.2.0 cho thấy `Styles.get_by_id` kiểm cả loại và trả mặc định đúng loại khi tham chiếu sai. Đây là đối chiếu qua mã, chưa dựng tệp hay chạy Word. [Bảng style](../scripts/tl_core/llm_route.py#L884) · [Tra chuỗi style](../scripts/tl_core/llm_route.py#L929) · [Chọn style](../scripts/tl_core/llm_route.py#L1089)

**Hạng P1 và đề xuất.** Đường cấu trúc có thể xác nhận chữ đã gạch bỏ hoặc một định nghĩa đã mất chữ, vì model và phép so cùng nhận bản trích sai. Áp dụng một quy tắc phân giải style theo loại cho điểm vào đoạn, điểm vào run và chuỗi `basedOn`. Từ chối tham chiếu không phân giải được cho loại cần dùng hoặc áp dụng fallback đã xác minh. Phép kiểm đóng lớp cần giữ đối chứng cho style đoạn/ký tự hợp lệ, ID vắng, ID sai loại, kế thừa sai loại và gạch đơn/kép. [Hợp đồng F2](../ops/specs/llm-khoan-docx-r30.md#L370) · [M1–M2](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32)

### G2 [P2] Chốt nhãn thô vừa bỏ sót nhãn số–chữ vừa lấy dấu mở thân làm dấu nhãn — `scripts/tl_core/llm_route.py:526`, `:1436`

**Kịch bản và căn cứ.** Một điểm có nhãn gồm placeholder số, dấu chấm rồi placeholder chữ, kết thúc ngay sau chữ và cách phần nội dung bằng khoảng trắng. Nếu số mở nhãn trùng số khoản kế, `_RE_NHIEU_CAP` đòi thêm dấu sau thành phần chữ nên bỏ qua nhãn này. Nhánh `_RE_SO_KHOAN` nhận số và dấu chấm trước khi `_RE_DIEM` được xét. Chữ nhãn còn lại thành một phần thuật ngữ. Khi dòng điểm có đủ hai vế, dấu kết, không có số nội dòng và dãy số liên tục, kết quả theo phân đoạn ấy có thể được chấp nhận. Dạng này có dấu nối nên nằm trong tuyên bố miền nhãn của §2.29, dù có vùng giao với khoản thật có thân bắt đầu bằng một chữ cái mà §2.30 bảo toàn.

Ở chiều chặn oan, một khoản thô bắt đầu bằng số, dấu chấm rồi một cụm ngoặc tròn cân bằng ở đầu thuật ngữ. Chốt ngoặc đã bỏ dấu số trước khi xét và cho qua cụm cân bằng. Nhánh mới của r30 vẫn thấy dấu chấm và dấu mở ngoặc là hai dấu liên tiếp quanh một placeholder, trả `None` cho cả nguồn trước khi xét chữ trong ngoặc. Bản trước cần một thành phần nhãn tiếp theo nên cho qua khi trong ngoặc bắt đầu bằng từ đầy đủ. Giới hạn ký tự không áp dụng vì tất cả dấu trong tình huống này đều được phép. [Ngữ pháp](../scripts/tl_core/llm_route.py#L490) · [Tách khoản](../scripts/tl_core/llm_route.py#L1427) · [Kiểm dấu phân cách](../scripts/tl_core/llm_route.py#L1491) · [Miền nhãn](../ops/specs/llm-khoan-docx-r30.md#L348)

**Hạng P2 và đề xuất.** Nhận sai cần nguồn mất cấp, nhãn trùng số kế và dòng thỏa các chốt còn lại. Đầu ra vẫn khai phạm vi phân đoạn thô và yêu cầu duyệt ranh giới. Chiều còn lại từ chối một khoản hợp lệ. Đối chiếu ngữ pháp nhận diện với miền nhãn bộ dựng sinh ra và định nghĩa rõ phần giao với thân khoản, gồm chữ cuối nhãn và dấu mở cụm nội dung. Nếu quyết định từ chối vùng giao, ghi rõ dạng khoản hợp lệ bị ảnh hưởng và giữ đối chứng cho các dạng đã cam kết đọc. [Tiền lệ F1](../ops/acceptance/llm-khoan-docx/r1/review-29-codex/VERDICT.md#L67) · [Phạm vi thô](../scripts/tl_core/llm_route.py#L1404)

| Lớp | Finding mở | Lịch sử và cách kiểm đóng |
| --- | --- | --- |
| `docx-markup-du-thao` | G1 · P1 | A4 lượt 1 → B3/C4/E2 → F2 lượt 29. ID vắng đã có phản chứng. Cần xác minh phân giải kiểu ở tất cả tầng có thể đổi chữ còn hiệu lực. |
| `ranh-gioi-khoan` | G2 · P2 | K1 #1514 → V4/W4/X3/Y3/Z3/A2 lượt 24/B1/C1/D1 → E1/F1. Cần kiểm cả chiều nhận nhãn điểm và chiều bảo toàn thân khoản trên cùng miền, giữ đối chứng câu dẫn, điểm gõ tay và nguồn một dòng. |
| `docx-so-hien-thi` | 0 biểu hiện đã báo còn mở trong miền đo | A2/B2/G1/J1/V2/W5/X2/Y2/Z2. Kiểm start/override, reset, nhiều numId, định nghĩa lỗi dùng và không dùng. |
| `docx-test-doc-lap` | 0 biểu hiện đã báo còn mở trong miền đo | A7/B7/C6/D4/E5/F5/G5/H3/J4/Z4/B2. Harness ghi nhận mutant đến đúng assertion. Kịch bản mới cần ca riêng để đóng G1/G2. |

Đối chiếu danh sách phần tử §2.5 và các bổ sung cho thấy mốc quyền, bookmark/comment, content control, hyperlink, tab và ngắt không chia từ đã có nhánh xử lý. Trường, hình, chú thích, markup tương thích, bảng, ngắt mềm và đánh số qua style nằm trong giới hạn hướng dẫn. Chưa xác lập phần tử phổ biến khác của Word/Google Docs gây từ chối ngoài các giới hạn bằng vật liệu của phiên này. [Danh sách phần tử](../scripts/tl_core/llm_route.py#L649) · [Hướng dẫn DOCX](../docs/GOI_AGENT_DA_NEN.md#L390)

## Kết quả test và đột biến

Các phép đo chạy tại hai bản sao detached cùng SHA/tree tương ứng trong `/tmp/wp1525-r30-review.rZLgORwd/`. Linux x86_64, Python 3.13.18, Git 2.43.0, Codex CLI 0.172.0, Ruff 0.15.15, `core.abbrev=7` và `PYTHONDONTWRITEBYTECODE=1`. Log và mã thoát nằm cùng thư mục scratch theo cặp `*.log` / `*.rc`.

| Lệnh | Trạng thái | Mã thoát và bằng chứng |
| --- | --- | --- |
| `python scripts/tl_core/llm_route_test.py` | `passed` | rc 0, **63/63** ca và **253/253** đột biến bị giết. `head-route.log`. |
| `python scripts/tl.py --deterministic workflow-audit --strict --json` | `passed` | rc 0, `ok=true`, 194 lệnh, 26 card, 11 nhóm, 60 task, 0 lỗi/cảnh báo. `head-audit.log`. |
| `python scripts/tl.py --deterministic golden-test --json` | `passed` | rc 0, `ok=true`, **20/20** fixture khớp, **20/20** bản chiếu ổn định, **19/20** byte thô ổn định. Chênh lệch đã khai ở `hygiene_sweep_fixture`, trường `snapshot_age_s`. `head-golden.log`. |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | `passed` | rc 0, `ok=true`, **187/187** tệp, sai/thiếu/thừa đều 0. Package hash khớp `dd4b15d0dac9b937ac972534f6eaa6ddaaa4638d9f5b3787584d26aa8f695d4a`. `head-release.log`. |
| `python ops/lease_publish.py check --root . ops/leases/llm-khoan-docx-r30-g1-claude.yaml` | `passed` cục bộ | rc 0, “ĐĂNG ĐƯỢC”, #1525, neo `64b7f2c14776`, hết hạn 21:10 UTC. `head-lease.log`. |
| `python scripts/tl.py --selftest` trên head | `failed` | rc 1, **1774/1790**, transport **12/12**. Ca `r1525_llm_khai_niem_tep_docx_cau_truc` đạt. `head-selftest.log`. |
| `python scripts/tl.py --selftest` trên base | `failed` | rc 1, **1773/1789**, transport **12/12**. Cùng 16 ca đỏ với head. `base-selftest.log`. |
| `python scripts/tl.py --deterministic determinism-audit --strict --json` | `passed` | rc 0, `ok=true`, **15/15** chốt. `head-determinism.log`. |
| `python scripts/tl.py --deterministic doc-claims-check --strict --json` trên head và base | `failed` cả hai | rc 2 mỗi bản, cùng cờ cứng `SHA_NOT_A_COMMIT` cho `9941d8af52aeede1c78ea4e232fbe9a8d5272033`, `docs/PROTOCOL_DA_PHIEN.md:1680`. Object vắng trong checkout shallow. `head-doc-claims.log`, `base-doc-claims.log`. |
| `python -m ruff check --no-cache --select F --output-format json scripts/tl.py` trên head và base | `failed` lint, tiêu chí delta đạt | rc 1 mỗi bản, cùng 12 F821 và 0 F401. Chẩn đoán JSON giống nhau theo đường dẫn tương đối. `head-ruff.log`, `base-ruff.log`. |
| `python -m ruff check --no-cache --select F --output-format json scripts/tl_core/llm_route.py scripts/tl_core/llm_route_test.py` trên head | `passed` | rc 0, danh sách chẩn đoán `[]`. `head-ruff-module.log`. |
| `loi_ruff_ci()` qua `runpy.run_path(".claude/dev/ci_dang_ky_test.py")` | `passed` | rc 0, `RUFF_CONTRACT 3 []` cho hợp đồng pin/probe workflow. `head-ruff-contract.log`. |
| `git diff --check 3bfed5f HEAD`, `git diff --check fcb12b3 HEAD`, `git diff --check 64b7f2c HEAD` | `passed` bản vá và packet, `failed` toàn PR | rc lần lượt 0, 0, 2. Toàn PR có ba dấu ngắt Markdown bằng khoảng trắng ở hồ sơ #1514 lượt 8, dòng 3–5. |

`DOT_BIEN` chạy bản chỉnh sửa trong thư mục tạm và chỉ tính kill khi ca đích ném `TinHieuChotCa`. Chạy lại bằng `python -B -m pdb scripts/tl_core/llm_route_test.py`, điểm dừng dòng 2269 với điều kiện `ten.startswith("wp1525_")`, in tên mutant, ca đích và ngoại lệ đang xử lý. Rc 0, suite vẫn 63/63, 253/253 và **156/156** mutant `wp1525_*` vào đúng nhánh assertion. SHA-256 log `head-target-mutants.log` là `4743bb0a6fe63c86162be0940a94b5ba36e3aa1c6c15989f139d3105c27b713e`. [Harness](../scripts/tl_core/llm_route_test.py#L2250)

| Mutant có sẵn | Ca đích và tín hiệu |
| --- | --- |
| `wp1525_mot_cho_hai_dau` | `ca_khoan_mat_so_co_diem_dat`: nâng ngưỡng lên ba dấu làm dạng hai dấu được bộ tách nhận lại. |
| `wp1525_pstyle_dut_khong_chan` | `ca_cau_truc_docx_chan`: bỏ chốt ID vắng làm ca đích qua cửa đọc. |
| `wp1525_tho_nhan_diem` | `ca_wp1514_luot9`: bỏ chốt dòng điểm khiến các dòng điểm vào danh sách khoản thô. |
| `wp1525_khong_dat_lai_cap_con` | `ca_cau_truc_docx_dat`: điểm ở khoản sau chạy tiếp đến c thay vì bắt đầu lại. |
| `wp1525_bo_qua_start_override` | `ca_cau_truc_docx_dat`: ca dương bị từ chối vì số khoản khởi đầu 5. |

Mutant lịch sử `wp1525_nhieu_cap_mot_dau` đã được bỏ khỏi bảng r30. Với fixture nhiều dấu cũ, nhánh mới kiểm hai dấu có thể chặn độc lập ngay trước khi phép thử phân biệt số dấu trong nhánh nối hai placeholder. Hai mutant mới kiểm đúng tính chất của r30 trong các ca sẵn có. [Bảng mutant](../scripts/tl_core/llm_route_test.py#L1932) · [Ngữ pháp](../scripts/tl_core/llm_route.py#L526)

`cmp head-selftest.fail-ids base-selftest.fail-ids` trả rc 0, delta ID lỗi bằng 0. Trong 16 ca cùng đỏ, 14 thuộc nhóm môi trường `/tmp/.git` rỗng đã nêu trong prompt (8 `r973_bootstrap_*`, 5 `wp433_*` và `wp727_tl_gws_refresh`). Hai ca còn lại là `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` và `r268_l2_trichotomy_theo_trang_thai_object`. SHA-256 log head `a9e3773b1234adcdf6489bf5ed01fbfc185e06c1e8d4aca2dc7cf7eee0a26af2`, base `ac7513b12b97a094f07ba169b93f6d9ee6a1c690489e88b88f89bf591ce53260`.

## Không đo được

- G1/G2 dựa trên lần theo đường thực thi. Phép đo ứng dụng Word/Google Docs đối với kịch bản mới và tần suất xuất hiện cần mẫu ngoài bộ ca hiện có. Không có DOCX được Git theo dõi trong checkout này.
- Sáu lệnh trong prompt có `skipped=0`. Phần `not_run` gồm Windows bản địa, CI từ xa, hai phép GitHub của lease, model thật và LIVE. Windows thuộc `required` theo M3 vì diff toàn PR đổi dòng Python có `encoding=`. [M3](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L43)
- Model và effort phục vụ ở launcher là `KHONG_DO_DUOC` trong metadata hiện có. Rc con, SHA-256 stdout và trạng thái terminal của run chỉ có thể xác minh sau khi launcher hoàn tất. Trạng thái nhánh quan sát ở mức refs và Git objects cục bộ.

## Readback và kết luận

Head/tree khớp ở đầu và cuối. `git diff --exit-code` và `git diff --cached --exit-code` đều rc 0. Checkout giao review có `.codex/` rỗng đã hiện diện từ đầu và chỉ thêm `.review/VERDICT.md`. Hai bản sao đo giữ nguyên tracked/index và exact SHA/tree, có fixture golden và state test ignored trong scratch. Snapshot xác nhận delta quan sát được giữa hai mốc. Repo nguồn của Executor ngoài phạm vi quan sát.

Còn **0 P0, 1 P1, 1 P2, 0 P3**. Hai finding bao gồm bốn biểu hiện trên hai lớp. Cả hai lớp mở ở lượt 29 đều còn mở, tỷ lệ đóng lớp là 0/2 theo §8.3 và §12. G1 dẫn tới `REQUEST_CHANGES` theo ngưỡng verdict được giao. G1 và G2 đều chặn merge theo ADR-0060 M1. Selftest N/N và doc-claims strict của §5 vẫn chưa đạt dù delta lỗi bằng 0. Bằng chứng Windows/CI trên exact head còn thiếu. Lượt này đã dùng lời gọi 30/30 của lease r30. [ADR-0060](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32) · [ADR-0062](../docs/adr/0062-adr-0060-mac-dinh-va-dong-bang-adr-0054.md#L12)

P2_mo: 1
VERDICT: REQUEST_CHANGES
