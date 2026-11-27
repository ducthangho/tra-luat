# Verdict packet #1525 r31 lượt 31 — Codex

reviewed_sha: 7e9cde7e8e6160895e71d2ceab1520c342786188
reviewed_tree: cd66215a4ef9fbe6b375182e3466f888d95885da
base_sha: 64b7f2c14776d5d0e1d34a6be4725490956f5bec
base_tree: 0cc14e79cecd2ce44bc4dc6cff92cadb31fd7ee4

## Phạm vi và preflight

- Review độc lập trên checkout detached của `ducthangho/tra-luat`. Ref local `ccr-89c0d2e2-inanqb` và ref theo dõi `origin/ccr-89c0d2e2-inanqb` trỏ exact head. Merge base khớp SHA giao review. Diff bản vá từ `a9cf41516383864d3fc2b6786dedf651a879c2e3`, diff packet từ `fcb12b3873c3bec2c339029136243ed2c804ce05`, diff toàn PR từ base trên.
- Reviewer `openai_codex / codex_cli / machine` qua launcher, run `881443026a734556a6a433f281beb936`. SHA-256 prompt `415240f930527f47f02158c2d892c155ec31df5ccbe0e4e51edd82880a6e0d9c` khớp checkpoint và exact head. Sandbox `workspace-write` theo permission profile của phiên. Executor `claude / claude_code / machine/local` theo lease, tương ứng `anthropic_claude` trong bảng provider. Class khai báo và hiệu lực đều là `sensitive`. [Checkpoint](../../run/88144302/checkpoint.json) · [Run](../../run/88144302/run.json) · [Bảng provider](../ops/KE_HOACH_THI_CONG_DA_PROVIDER.md#L26)
- Lease #1525 r31/g1 còn hạn tới 2026-11-26 21:29 UTC tại lúc kiểm, lượt này là 31/31, inference budget 0. SHA-256 đặc tả trên đĩa và Git blob `ba165c56c0cbbee8cb23b09ac1c93dbde176fb54b00f80cc727ce4eaedff267a` khớp lease. Quyền đứng của chủ kho, hợp đồng một Điều và ngoại lệ M5 có ghi trong đặc tả. [Lease](../ops/leases/llm-khoan-docx-r31-g1-claude.yaml) · [Đặc tả](../ops/specs/llm-khoan-docx-r31.md)
- Write set có 166 đường dẫn, hash sau sắp xếp `458781f63bf512ed4fdd9ba37105505813f5475b095d3109f6668dfed11fc0c6`. Bản vá có 8/8 đường dẫn thuộc lease. Diff packet có 166 đường dẫn, 162/162 thuộc lease sau khi trừ 4 hồ sơ #1514 theo prompt. Diff toàn PR có 210 đường dẫn, 48 đường dẫn ngoài lease r31 thuộc hồ sơ, lease và spec kế thừa #1514. Đối chiếu **31/31** cặp bia mộ hai chiều #1514 r9 ⇄ #1525 r1 ⇄ … ⇄ r31 và **32/32** hash spec trên đĩa và Git blob. Branch, base và generation nhất quán. [Bia mộ #1514](../ops/leases/llm-ranh-gioi-khoan-r9-g1-claude.yaml#L97) · [Tiền nhiệm r31](../ops/leases/llm-khoan-docx-r30-g1-claude.yaml)

## Đối chiếu lượt 30 và đặc tả r31

| Mục | Trạng thái | Bằng chứng |
| --- | --- | --- |
| Lượt 30 G1 · §2.32–§2.33 | **ĐÃ VÁ THẬT** ba biểu hiện trực tiếp. **VÁ MỘT PHẦN** lớp và **VÁ SINH LỖI MỚI** trong bảng style | `pStyle` và `rStyle` trỏ sai loại bị chặn, `basedOn` nối khác loại bị từ chối. Các mutant tương ứng đỏ cùng lý do đích. Chọn style mặc định vẫn xét loại thô trước khi áp mặc định `paragraph` của r31, xem H1. Vòng duyệt mới có thể tra nhầm metadata như định nghĩa style, xem H3. [Bảng style](../scripts/tl_core/llm_route.py#L903) · [Điểm vào đoạn/run](../scripts/tl_core/llm_route.py#L1094) · [Ca G1](../scripts/tl_core/llm_route_test.py#L1720) |
| Lượt 30 G2 · §2.28–§2.33 | **ĐÃ VÁ THẬT** hai biểu hiện gốc. **VÁ MỘT PHẦN** lớp | Ca nhãn số–dấu–chữ liền bị từ chối, khoanh thân mở bằng cụm ngoặc cân bằng qua, thân mở bằng chữ cái có đệm vẫn qua. Khi khoảng đệm đứng trước dấu mà chữ vẫn dính dấu, chốt mới và nhánh số khoản quyết khác nhau, xem H2. [Ngữ pháp](../scripts/tl_core/llm_route.py#L526) · [Thứ tự nhánh](../scripts/tl_core/llm_route.py#L1452) · [Ca G2](../scripts/tl_core/llm_route_test.py#L714) |
| §1, §2.2–§2.3 · K1 #1514 | **ĐÃ VÁ THẬT** hai đường ghép gốc | Dòng có nhãn điểm thông dụng bị chặn ở cả nguồn có số lẫn mất số. Dòng không số mở bằng “là” trong nguồn có số rơi vào nhánh từ chối, còn nguồn mất số bị phép so loại nếu thiếu vế thuật ngữ. Ba kết quả đã lưu của Điều 3 Luật 134/2025/QH15 đạt 8/8 trong suite. Route model và cờ `can_nguoi_duyet: true` được giữ. [K1 gốc](../ops/acceptance/llm-ranh-gioi-khoan/r1/review-10-codex/VERDICT.md#L35) · [Tách thô](../scripts/tl_core/llm_route.py#L1456) · [Ca hồi quy](../scripts/tl_core/llm_route_test.py#L1256) · [CLI](../scripts/tl_core/ops_misc.py#L3120) |
| §2.1, §2.4–§2.17 · vùng Điều, câu dẫn, điểm và fallback | **ĐÃ VÁ THẬT** các biểu hiện từng báo trong hợp đồng còn hiệu lực. **HẾT ĐỐI TƯỢNG** với luật cắt cuối Điều, duyệt số qua bảng và nhận điểm gõ tay thành đoạn riêng | Tiêu đề nguyên đoạn khớp số đích và đứng đầu nội dung. Bộ đọc kiểm mọi đoạn tới hết tệp, chặn bảng, khối lạ và tiền tố cấu trúc đã định nghĩa. Sau khoản đầu, đoạn có chữ phải được đánh số tự động. Trước khoản đầu, chỉ một câu dẫn chuẩn khớp cả đoạn hoặc vắng. Điều thiếu số tự động ném `ValueError`, CLI trả rc 2. Đường lùi `KhongCauTruc` đã bỏ. [Duyệt khối](../scripts/tl_core/llm_route.py#L1004) · [Chọn Điều](../scripts/tl_core/llm_route.py#L1317) · [Điểm và câu dẫn](../scripts/tl_core/llm_route.py#L1372) · [CLI](../scripts/tl_core/ops_misc.py#L3037) |
| §2.4–§2.15, §2.22–§2.26 · số Word | **ĐÃ VÁ THẬT** các biểu hiện từng báo trong miền hỗ trợ | `start` mặc định 0. `startOverride` thay giá trị khởi tạo. Bộ đếm tách `numId`, đặt lại cấp con khi cấp cha tăng và chặn nhảy cấp. Bước ghép buộc một `numId`, nhãn khoản thập phân của chính cấp ấy và số khoản liên tục từ 1. Có ca xác thực ID/cấp trùng, giới hạn 999, trường đơn trị, restart và đánh số qua style ngoài miền. [Định nghĩa](../scripts/tl_core/llm_route.py#L786) · [Bộ đếm](../scripts/tl_core/llm_route.py#L1294) · [Bước ghép](../scripts/tl_core/llm_route.py#L1358) |
| §2.5–§2.13, §2.23–§2.29 · chữ còn hiệu lực | **ĐÃ VÁ THẬT** các biểu hiện gốc về chữ bị bỏ, phân cách và ngắt. Lớp phân giải style còn mở | XML gốc giữ ranh giới đoạn. Gạch đơn/kép tính riêng và định dạng trực tiếp ghi đè. Bộ đọc bỏ chữ trong `del`/`moveFrom`, giữ chữ trong `ins`/`moveTo`, chặn sửa dấu đoạn và mốc move thiếu cặp. Một hàm đọc theo `xml:space`, giữ mẩu bị bỏ chỉ chứa phân cách. Cờ ngắt và phần tử văn bản lạ tính sau khi lọc run. H1 còn có thể đổi chữ của một đoạn được nhận. [Đọc chữ](../scripts/tl_core/llm_route.py#L1039) · [Lọc run](../scripts/tl_core/llm_route.py#L1116) · [Sửa dấu đoạn](../scripts/tl_core/llm_route.py#L1269) |
| §2.14–§2.21 · part, tiền tố và ký tự | **ĐÃ VÁ THẬT** trong miền công bố | Chọn part theo URI Transitional đầy đủ và tệp quan hệ của part chính. Parser nhận bytes. QName phân biệt namespace, chữ gốc kiểm trước gộp khoảng trắng, đường thô gỡ một BOM trước kiểm và tách dòng. Giá chặn ký tự ngoài tập và dẫn chiếu ở đầu đoạn đã được khai. [Quan hệ](../scripts/tl_core/llm_route.py#L745) · [Ký tự](../scripts/tl_core/llm_route.py#L619) · [Vùng](../scripts/tl_core/llm_route.py#L1336) |
| §2.22–§2.23 · đường số hiệu | **ĐÃ VÁ THẬT** chốt strict. U2, V3, W1, W3 và phần số hiệu của W2 thuộc giới hạn đã duyệt | Lời gọi có `--markup-strict`, bắt rc, mốc Điều và tín hiệu cắt trần. Làm sạch cache, cắt Điều theo regex và lọc markup của bộ đọc dùng chung thuộc các giới hạn đã công bố. H2 ở bộ tách thô sau tầng đọc nguồn, áp cả `--tep` văn bản. [Lời gọi extract](../scripts/tl_core/llm_route.py#L1692) · [Giới hạn](../ops/specs/llm-khoan-docx-r31.md#L268) |
| §3 · so nguyên văn, CLI, đột biến | **ĐẠT** trên các ca có sẵn | Phép so giữ số lượng, thứ tự, số khoản, hai vế và dòng điểm, chỉ dò từ nối trong đoạn mở khoản DOCX. CLI chỉ ghi `--out` khi phép so đạt. Nếu đầu vào của phép so đã sai do H1 hoặc H2, phép so vẫn dùng bản phân đoạn ấy. [Phép so](../scripts/tl_core/llm_route.py#L1587) · [Ghi đầu ra](../scripts/tl_core/ops_misc.py#L3133) · [Harness](../scripts/tl_core/llm_route_test.py#L2269) |

### Các finding lịch sử

ID đọc cùng số lượt. Bảng ghi trạng thái của biểu hiện đã báo. Phần lớp còn mở được nối vào H1/H2/H3 và bảng lớp bên dưới. [Đối chiếu lượt 30 trên `749e6ac89c770a59f353e5f3dd40ce82deae7715`](../ops/acceptance/llm-khoan-docx/r1/review-30-codex/VERDICT.md)

| Lượt #1525 | Đối chiếu trên r31 |
| --- | --- |
| [1](../ops/acceptance/llm-khoan-docx/r1/review-1-codex/VERDICT.md) | A1 phần cắt và A6 **HẾT ĐỐI TƯỢNG**. Phần còn lại của A1, A2–A5 và A7–A8 **ĐÃ VÁ THẬT** ở các ca gốc. Lớp chữ gạch của A4 còn H1. |
| [2](../ops/acceptance/llm-khoan-docx/r1/review-2-codex/VERDICT.md) | Phần cắt B1 và đếm bảng B2 **HẾT ĐỐI TƯỢNG**. Phần còn lại B1/B2 và B3–B8 **ĐÃ VÁ THẬT**. Chốt gạch kép độc lập, dấu nối không ngắt và metadata wrapper vẫn có đường đọc đã sửa. |
| [3](../ops/acceptance/llm-khoan-docx/r1/review-3-codex/VERDICT.md) | C1 phần điểm cắt và C2 phần đếm hàng/ô **HẾT ĐỐI TƯỢNG**. Phần còn lại C1/C2 và C3–C7 **ĐÃ VÁ THẬT** qua chốt ngắt, nhãn chữ sau Z, dấu phân cách, toggle và content control. |
| [4](../ops/acceptance/llm-khoan-docx/r1/review-4-codex/VERDICT.md) | D1 phần cắt **HẾT ĐỐI TƯỢNG**, bỏ fallback **ĐÃ VÁ THẬT**. D2–D4 và D6 **ĐÃ VÁ THẬT**. D5 thuộc giới hạn DOCX Strict đã khai. |
| [5](../ops/acceptance/llm-khoan-docx/r1/review-5-codex/VERDICT.md) | E1/E3/E4 **HẾT ĐỐI TƯỢNG**. E2/E5/E6 **ĐÃ VÁ THẬT**, có ca toggle, XML gốc, move và miền cấp. |
| [6](../ops/acceptance/llm-khoan-docx/r1/review-6-codex/VERDICT.md) | F1 cắt Điều và F2 nhận điểm tay **HẾT ĐỐI TƯỢNG**. F3–F6 **ĐÃ VÁ THẬT**, kiểm ID, trần, cấp override, tab theo vị trí và cặp move. |
| [7](../ops/acceptance/llm-khoan-docx/r1/review-7-codex/VERDICT.md) | G1–G6 **ĐÃ VÁ THẬT**. Kiểm cấp tổ tiên, part styles, ngắt trang/cột cuối đoạn và tiêu đề không phân biệt hoa thường. |
| [8](../ops/acceptance/llm-khoan-docx/r1/review-8-codex/VERDICT.md) | H1–H5 **ĐÃ VÁ THẬT**. Kiểm tiền tố Điều, quan hệ gốc, mutant đổi tên, numId lỗi qua style và chữ sau ngắt. |
| [9](../ops/acceptance/llm-khoan-docx/r1/review-9-codex/VERDICT.md) | J1–J5 **ĐÃ VÁ THẬT**. Chốt đánh số qua style, phần tử `mc`, nhãn ngoài miền, rels của part đổi tên và ngắt sau lọc. |
| [10](../ops/acceptance/llm-khoan-docx/r1/review-10-codex/VERDICT.md) | K1–K4 **ĐÃ VÁ THẬT**. Kiểm `mc` ở ba part, số thứ tự bằng chữ, khớp toàn `lvlText` và mô tả đọc hết tệp. |
| [11](../ops/acceptance/llm-khoan-docx/r1/review-11-codex/VERDICT.md) | L1–L6 **ĐÃ VÁ THẬT**. URI đầy đủ, cấm tiền tố Điều, giới hạn tiêu đề lớn, chẩn đoán số lỗi, parse bytes và hướng dẫn. |
| [12](../ops/acceptance/llm-khoan-docx/r1/review-12-codex/VERDICT.md) | M1–M2 **ĐÃ VÁ THẬT** cho biểu hiện đã báo. Chốt tiền tố độc lập dấu cuối và xử lý số/cấp, mốc move thiếu ID. |
| [13](../ops/acceptance/llm-khoan-docx/r1/review-13-codex/VERDICT.md) | N1–N3 **ĐÃ VÁ THẬT**. Chiếu dấu trước dò tiền tố, chuẩn hóa ID bằng chuỗi, duyệt khối theo QName. |
| [14](../ops/acceptance/llm-khoan-docx/r1/review-14-codex/VERDICT.md) | Q1/Q2 **ĐÃ VÁ THẬT** qua chốt ký tự gốc và hướng dẫn giữ nguyên dẫn chiếu. |
| [15](../ops/acceptance/llm-khoan-docx/r1/review-15-codex/VERDICT.md) | R1–R3 **ĐÃ VÁ THẬT**. Chặn ký tự trước gộp, số gõ tay ngoặc kín, chốt ký tự ở đường thô. |
| [16](../ops/acceptance/llm-khoan-docx/r1/review-16-codex/VERDICT.md) | S1–S3 **ĐÃ VÁ THẬT**. Danh sách cho phép, kiểm trước tách dòng và cho qua mốc quyền. |
| [17](../ops/acceptance/llm-khoan-docx/r1/review-17-codex/VERDICT.md) | T1/T2 **ĐÃ VÁ THẬT** ở cửa packet. Số mũ đã ra khỏi tập, gỡ một BOM. Bộ đọc chung thuộc U2. |
| [18](../ops/acceptance/llm-khoan-docx/r1/review-18-codex/VERDICT.md) | U1 **ĐÃ VÁ THẬT**. Miền chữ số là ASCII. U2 thuộc giới hạn đã duyệt. |
| [19](../ops/acceptance/llm-khoan-docx/r1/review-19-codex/VERDICT.md) | V1/V2/V4 **ĐÃ VÁ THẬT**. Strict, từ chối số khai ở mặc định đoạn và nhãn điểm chữ kết chấm. V3 thuộc giới hạn đã duyệt. |
| [20](../ops/acceptance/llm-khoan-docx/r1/review-20-codex/VERDICT.md) | W2 DOCX và W4/W5 **ĐÃ VÁ THẬT**. Giữ mẩu phân cách, chặn nhãn hoa/lặp, cấp hoặc override trùng. W1/W3 và W2 số hiệu thuộc giới hạn đã duyệt. |
| [21](../ops/acceptance/llm-khoan-docx/r1/review-21-codex/VERDICT.md) | X1–X3 **ĐÃ VÁ THẬT** ở dạng đã báo. Giữ tab/ngắt thuần, kiểm trường đơn trị, chặn nhãn chữ nối gạch có khoảng đệm. |
| [22](../ops/acceptance/llm-khoan-docx/r1/review-22-codex/VERDICT.md) | Y1–Y3 **ĐÃ VÁ THẬT** ở dạng đã báo. Dùng chung đọc ruột, kiểm nút chọn vùng, ID style trùng và nhận nhãn có đệm. |
| [23](../ops/acceptance/llm-khoan-docx/r1/review-23-codex/VERDICT.md) | Z1–Z4 **ĐÃ VÁ THẬT**. Phần tử lạ trong mẩu bỏ, ZIP trùng tên, nhãn số–số có ngoặc và mutant đơn trị riêng. |
| [24](../ops/acceptance/llm-khoan-docx/r1/review-24-codex/VERDICT.md) | A1/A2 **ĐÃ VÁ THẬT**. Đọc kế thừa `xml:space`, chặn nhãn hai số kết gạch. |
| [25](../ops/acceptance/llm-khoan-docx/r1/review-25-codex/VERDICT.md) | B1 **VÁ MỘT PHẦN**, hiện thân còn lại ở H2. B2/B3 **ĐÃ VÁ THẬT** qua mutant đặt lại `xml:space`, ruột đã bỏ, `delText` lạc và cờ ngắt. |
| [26](../ops/acceptance/llm-khoan-docx/r1/review-26-codex/VERDICT.md) | C1 **ĐÃ VÁ THẬT** ở dạng số đa cấp đã báo, **VÁ MỘT PHẦN** lớp theo H2. C2 **ĐÃ VÁ THẬT** với phần tử lạ trong run đã bỏ. |
| [27](../ops/acceptance/llm-khoan-docx/r1/review-27-codex/VERDICT.md) | D1 **ĐÃ VÁ THẬT** ở dạng số–chữ có dấu cuối và các dạng cũ trong ca, **VÁ MỘT PHẦN** lớp theo H2. |
| [28](../ops/acceptance/llm-khoan-docx/r1/review-28-codex/VERDICT.md) | E1 **ĐÃ VÁ THẬT** ở các dạng có dấu đầu đã báo, **VÁ MỘT PHẦN** lớp theo H2. |
| [29](../ops/acceptance/llm-khoan-docx/r1/review-29-codex/VERDICT.md) | F1 **ĐÃ VÁ THẬT** ở các dạng nhiều dấu cuối đã báo, **VÁ MỘT PHẦN** lớp theo H2. F2 **ĐÃ VÁ THẬT** với `pStyle` vắng, lớp phân giải mặc định còn H1. |
| [30](../ops/acceptance/llm-khoan-docx/r1/review-30-codex/VERDICT.md) | G1/G2 theo hai dòng đầu của bảng đối chiếu. |

Với #1514, A1/A2/D3/E2/F2 về câu dẫn, C1 về tiêu đề dính thân, A3/C2/D1/E1/F1 về dấu kết hoặc số nội dòng và G1/H1/J1/K1 về ghép dòng đều có chốt hiện hành. A4 giữ đối chứng 8/8. D2 và phần C2 liên quan ngoại lệ nội dòng thuộc giới hạn thô đã khai. B1 lượt 1 về bề mặt đã giải quyết trong run hiện hành. Nếu nguồn mất thông tin cấp và các dòng đều đủ hai vế và dấu kết, bộ quét vẫn có thể nhận từng dòng là một khoản. Dấu số tiểu mục trùng hình dạng và trùng số khoản kế cũng qua cửa số đơn. Hai tình huống đồng hình này thuộc bước duyệt ranh giới đã khai. H2 nằm trong miền nhãn có dấu mà packet cam kết nhận diện. [Verdict #1514](../ops/acceptance/llm-ranh-gioi-khoan/r1/review-10-codex/VERDICT.md) · [Phạm vi thô](../scripts/tl_core/llm_route.py#L1420) · [Hợp đồng nhãn](../ops/specs/llm-khoan-docx-r31.md#L349)

## Findings

### H1 [P1] Chọn style đoạn mặc định bằng loại thô có thể giữ chữ gạch bỏ — scripts/tl_core/llm_route.py:922

**Kịch bản và căn cứ.** Style mặc định của đoạn có gạch ngang và khai `w:default` nhưng bỏ `w:type`. Theo §2.33, đây là style đoạn. Tiêu đề dùng một paragraph style sạch được khai tường minh. Các đoạn khoản đánh số trực tiếp, không có `pStyle` và có chữ bị gạch theo mặc định. `_doc_kieu` chỉ gán `mac_dinh_doan` khi thuộc tính loại thô đúng bằng `paragraph`. Bảng `loai` được tạo sau đó mới áp mặc định `paragraph` và không cập nhật lựa chọn mặc định. `_phan_tich_doan` lấy style mặc định đã bị bỏ qua, vì vắng `pStyle` nên cũng không bật chốt kiểu sai. Khi số và chữ còn lại thỏa các chốt, chữ mà hợp đồng yêu cầu lọc có thể đi vào cả prompt lẫn nguồn so của `lech_nguyen_van`. Suy luận từ mã và §2.33. [Chọn mặc định và tính loại](../scripts/tl_core/llm_route.py#L920) · [Áp mặc định khi đọc đoạn](../scripts/tl_core/llm_route.py#L1100) · [§2.33 G1](../ops/specs/llm-khoan-docx-r31.md#L377)

**Hạng và đề xuất.** P1 vì đường cấu trúc có thể xác nhận chữ đã gạch bỏ. Tính loại hiệu lực một lần và dùng cho việc chọn mặc định, xác thực điểm vào đoạn/run và chuỗi kế thừa. Phép kiểm đóng lớp cần so mặc định khai loại tường minh và mặc định dựa vào loại ngầm định, giữ đối chứng style mặc định sạch, trực tiếp ghi đè, ID vắng và ID sai loại. Các ca r31 hiện khai tường minh `w:type="paragraph"` ở style mặc định. [Ca hiện có](../scripts/tl_core/llm_route_test.py#L1715) · [ADR-0060 M1–M2](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32)

### H2 [P2] Khoảng đệm trước dấu nối cho phép nhận nhãn số–chữ thành khoản — scripts/tl_core/llm_route.py:526

**Kịch bản và căn cứ.** Bản thô mất cấp có một điểm mang nhãn từ hai placeholder, số rồi chữ cái lặp đứng riêng. Dấu chấm hoặc ngoặc đóng đứng giữa hai placeholder. Có đệm ngang giữa số và dấu, chữ cái dính ngay sau dấu và nhãn kết thúc sau chữ. `lvlText` cho phép đệm ở đây. Chữ của điểm theo sau với đủ hai vế và dấu kết. Số ở đầu nhãn trùng số khoản kế, các khoản còn lại qua chốt số và dấu kết. Nhánh mới của `_RE_NHIEU_CAP` đòi số kề dấu, nhánh có `_NOI_NHIEU` lại đòi dấu sau chữ. `_RE_SO_KHOAN` chấp nhận đệm trước dấu và nhận phần số trước khi `_RE_DIEM` được xét. Chữ nhãn còn trong thuật ngữ, điểm có thể thành khoản riêng và đầu ra khớp bản phân đoạn sai đó. Khoảng đệm ở đây nằm **trước dấu**, còn ngoại lệ §2.33 giữ khoản có đệm **sau dấu**, giữa dấu và chữ mở thân. Suy luận từ mã. [Chốt nhãn](../scripts/tl_core/llm_route.py#L514) · [Chốt số đơn](../scripts/tl_core/llm_route.py#L490) · [Thứ tự ưu tiên](../scripts/tl_core/llm_route.py#L1452) · [Miền nhãn](../ops/specs/llm-khoan-docx-r31.md#L349)

**Hạng và đề xuất.** P2 theo G2 và K1 vì lỗi nhận sai cần nguồn mất cấp, số trùng, đủ hai vế, dấu kết và đầu ra khớp bản phân đoạn. Đầu ra mang phạm vi thô và yêu cầu duyệt. Đối chiếu toàn miền khoảng đệm của nhãn với miền nhận số khoản và giữ nguyên ngoại lệ thân mở bằng chữ hoặc cụm ngoặc. Kiểm cả hai phía của dấu nối và hai cửa nhận số, kiểu số trần và kiểu ngoặc kín. [Tiền lệ G2](../ops/acceptance/llm-khoan-docx/r1/review-30-codex/VERDICT.md#L76) · [§2.33 G2](../ops/specs/llm-khoan-docx-r31.md#L382)

### H3 [P2] ID style trùng khóa metadata làm vỡ bước phân giải trên toàn tệp — scripts/tl_core/llm_route.py:928

**Kịch bản và căn cứ.** Part styles có một styleId trùng khóa mà bộ đọc dùng để lưu cờ đánh số mặc định. Style được đưa vào `kq` như mọi định nghĩa. Sau đó metadata `#numPr_mac_dinh` ghi đè tuple của style bằng bool. Vòng kiểm loại mới của r31 vẫn lặp qua ID đó trong `loai` và lập tức đọc `kq[sid][0]`, gây `TypeError`, kể cả khi đoạn nào cũng không dùng style ấy. Handler DOCX không bắt `TypeError`. Đây là lớp va chạm giữa ID tài liệu và khóa nội bộ. Khóa `#loai` mới cũng có thể ghi đè tuple của một ID cùng tên, rồi lần tra gạch hoặc số thử lập chỉ mục tuple trên một dict. Suy luận từ mã. [Bảng và metadata](../scripts/tl_core/llm_route.py#L918) · [Tra chuỗi](../scripts/tl_core/llm_route.py#L940) · [Handler](../scripts/tl_core/ops_misc.py#L3043)

**Hạng và đề xuất.** P2 vì đọc một tệp có ID va chạm có thể thoát bằng traceback thay cho một kết quả hoặc chẩn đoán rc 2. Đường này chưa tới bước xác nhận nguyên văn. Lưu chỉ số metadata tách khỏi bảng định nghĩa, hoặc từ chối rõ mọi ID dành riêng trước khi đưa vào bảng. Phép kiểm đóng lớp cần bao phủ cả định nghĩa có dùng và không dùng. [Tiền lệ M2](../ops/acceptance/llm-khoan-docx/r1/review-12-codex/VERDICT.md) · [§2.15](../ops/specs/llm-khoan-docx-r31.md#L204)

| Lớp | Finding đang mở | Lịch sử và phép kiểm đóng |
| --- | --- | --- |
| `docx-markup-du-thao` | H1 · P1 | A4 lượt 1 → B3/C4/E2 → F2 lượt 29 → G1 lượt 30 → H1. Kiểm loại hiệu lực nhất quán ở các tầng có thể đổi chữ. |
| `ranh-gioi-khoan` | H2 · P2 | K1 #1514 → V4/W4/X3/Y3/Z3/A2 lượt 24/B1/C1/D1/E1/F1 → G2 lượt 30 → H2. Kiểm biên nhãn và thân theo cả hai chiều, với miền đệm của bộ dựng và các ngoại lệ đã khai. |
| `docx-khoa-bang-style` | H3 · P2 | Y2 lượt 22 kiểm xung đột giữa hai định nghĩa. H3 là va chạm giữa định nghĩa và metadata của bộ đọc. Cách đóng lớp là phân biệt hai miền khóa hoặc xác thực ngay khi nhập, độc lập với việc suy loại H1. |
| `docx-so-hien-thi` | 0 biểu hiện đã báo còn mở trong miền đo | A2/B2/G1/J1/V2/W5/X2/Y2/Z2. Kiểm start/override, reset, nhiều numId và định nghĩa lỗi dùng hoặc không dùng. |
| `docx-test-doc-lap` | 0 biểu hiện đã báo còn mở trong miền đo | A7/B7/C6/D4/E5/F5/G5/H3/J4/Z4/B2. Trace xác nhận các mutant có sẵn vào đúng assertion đích. Ca dành cho H1–H3 chưa có trong phép đo này. |

Đối chiếu danh sách phần tử cho thấy bookmark, comment, mốc quyền, hyperlink, content control, dấu nối không ngắt, tab và ngắt trang do Word render đã có nhánh. Ký hiệu, hình, trường, chú thích, bảng, ngắt mềm và phần tử tương thích nằm trong giới hạn công bố. Chưa xác lập được một phần tử phổ biến của bản Word hoặc Google Docs export bị từ chối ngoài các giới hạn đó bằng vật liệu được giao. [Danh sách phần tử](../scripts/tl_core/llm_route.py#L652) · [Giới hạn trong hướng dẫn](../docs/GOI_AGENT_DA_NEN.md#L392)

## Kết quả test và đột biến

Hai clone cục bộ detached ở exact head và base, Linux x86_64, Python 3.13.18, Git 2.43.0, `core.abbrev=7`, `PYTHONDONTWRITEBYTECODE=1`. Log và mã thoát tại `/tmp/wp1525-r31-review.VbBo6Z0m/`. Bản sao sạch dùng để tránh đưa verdict vào kiểm kê release.

| Lệnh | Trạng thái | Mã thoát và bằng chứng |
| --- | --- | --- |
| `python scripts/tl_core/llm_route_test.py` | `passed` | rc 0, **63/63** ca và **258/258** mutant bị giết. `head-route.log`. |
| `python scripts/tl.py --deterministic workflow-audit --strict --json` | `passed` | rc 0, `ok=true`, 26 card, 60 task, 194 lệnh hiện diện, 0 lỗi, 0 cảnh báo. `head-workflow.log`. |
| `python scripts/tl.py --deterministic golden-test --json` | `passed` | rc 0, `ok=true`, **20/20** ca, byte thô và bản chiếu cùng ổn định 20/20. `head-golden.log`. |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | `passed` | rc 0, `ok=true`, **187/187** tệp, 0 sai, thiếu hoặc thừa. Package hash khớp `700ee8d73e55f13ea6ba14a50a5b0ca6be8355bec7d29d273812d60f10c57219`. `head-release.log`. |
| `python ops/lease_publish.py check --root . ops/leases/llm-khoan-docx-r31-g1-claude.yaml` | `passed` cục bộ | rc 0, “ĐĂNG ĐƯỢC”, Issue #1525, neo `64b7f2c14776`, hạn 21:29 UTC. `head-lease.log`. |
| `python scripts/tl.py --selftest` trên head và base | `failed` trên cả hai, delta ID lỗi = 0 | Head **1774/1790**, base **1773/1789**, rc 1 mỗi bản. `r1525_llm_khai_niem_tep_docx_cau_truc` đạt trên head. `{head,base}-selftest.log`. |
| `python scripts/tl.py --deterministic determinism-audit --strict --json` | `passed` | rc 0, `ok=true`, **15/15** phép đạt. `head-determinism.log`. |
| `python scripts/tl.py --deterministic doc-claims-check --strict --json` trên head và base | `failed` | rc 2 mỗi bản, cùng 1 cờ cứng `SHA_NOT_A_COMMIT` cho `9941d8af52aeede1c78ea4e232fbe9a8d5272033` ở `docs/PROTOCOL_DA_PHIEN.md:1680`. Object vắng trong checkout shallow. `{head,base}-docclaims.log`. |
| `python -m ruff check --no-cache --select F --output-format json scripts/tl.py` trên head và base | `failed` lint, tiêu chí delta đạt | Ruff 0.15.15, rc 1 mỗi bản, 12 F821 và 0 F401. JSON giống nhau sau khi quy đường dẫn về tương đối. `{head,base}-ruff.log`. |
| `python -m ruff check --no-cache --select F --output-format json scripts/tl_core/llm_route.py scripts/tl_core/llm_route_test.py` | `passed` | rc 0, chẩn đoán `[]`. `head-ruff-modules.log`. |
| `loi_ruff_ci()` qua `runpy.run_path(".claude/dev/ci_dang_ky_test.py")` | `passed` | rc 0, `RUFF_CONTRACT 3 []` cho hợp đồng pin/probe workflow. `head-ruff-contract.log`. |
| `git diff --check a9cf415 HEAD`, `git diff --check fcb12b3 HEAD`, `git diff --check 64b7f2c HEAD` | `passed` bản vá và packet, `failed` toàn PR | rc 0, 0, 2. Ba dấu ngắt Markdown bằng khoảng trắng ở hồ sơ #1514 lượt 8, dòng 3–5. |

Bảng `DOT_BIEN` chép module đột biến vào thư mục tạm. Chạy lại suite bằng `python -B -m pdb scripts/tl_core/llm_route_test.py`, breakpoint dòng 2289 với điều kiện `ten.startswith("wp1525_")` và in tên mutant, ca đích, `str(sys.exception())`. Rc 0, **161/161** mutant `wp1525_*` tới đúng nhánh `TinHieuChotCa`. SHA-256 `head-target-mutants.log` là `aef13e013e45c5195886b3b3c25e04baf61e765e504b16794783c512d218ab1b`. [Harness](../scripts/tl_core/llm_route_test.py#L2269)

| Mutant | Ca đích và tín hiệu đỏ |
| --- | --- |
| `wp1525_pstyle_dut_khong_chan` | `ca_cau_truc_docx_chan`, `pStyle` trỏ character style lọt qua. |
| `wp1525_pstyle_vang_khong_chan` | `ca_cau_truc_docx_chan`, `pStyle` trỏ style vắng lọt qua. |
| `wp1525_rstyle_sai_loai`, `wp1525_basedon_doi_loai` | `ca_cau_truc_docx_chan`, từng chốt bỏ đi làm đúng ca sai loại tương ứng qua. |
| `wp1525_bo_so_dinh_chu_rieng`, `wp1525_mot_cho_hai_dau` | `ca_khoan_mat_so_co_diem_dat`, dạng số dính chữ và dạng hai dấu theo số lần lượt lọt. |
| `wp1525_hai_dau_nhan_ngoac_mo` | `ca_khoan_mat_so_co_diem_dat`, từ chối oan khoản có thân mở ngoặc khi coi ngoặc mở là dấu nhãn thứ hai. |
| `wp1525_tho_nhan_diem` | `ca_wp1514_luot9`, các dòng điểm lọt vào danh sách khoản thô. |
| `wp1525_khong_dat_lai_cap_con`, `wp1525_bo_qua_start_override` | `ca_cau_truc_docx_dat`, nhãn điểm khoản sau tiếp tục sang c; bỏ override thì bắt đầu khoản ở 5. |

`cmp head-selftest.fail-ids base-selftest.fail-ids` trả rc 0. Trong 16 ID cùng đỏ, 14 thuộc nhóm `/tmp/.git` rỗng đã nêu trong prompt, gồm 8 `r973_bootstrap_*`, 5 `wp433_*` và `wp727_tl_gws_refresh`. Hai ID đỏ sẵn còn lại là `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` và `r268_l2_trichotomy_theo_trang_thai_object`. SHA-256 log head `9039f3882296c059a84d887fd6ffd324286d3fa9e7dea09084d9c22676261731`, base `767ed511f1ff6faf88507abc8bc580db697636d4a31110a3896c8a4af424256c`.

## Không đo được

- H1–H3 dựa trên luồng thực thi và hợp đồng. Tái hiện các trường hợp mới hoặc định lượng tần suất chúng xuất hiện trong Word và Google Docs cần tệp/ca mới, ngoài phạm vi lượt này. Không có DOCX được Git theo dõi trong checkout.
- Sáu lệnh prompt đều kết thúc. Không có lệnh nào trong sáu lệnh bị `skipped`. Các nhánh selftest chỉ chạy trên Windows được ghi trong log theo từng nhóm. `not_run` gồm Windows bản địa, CI và connector từ xa, hai phép GitHub của lease, model thật và LIVE. Windows `required` theo M3 vì diff toàn PR có dòng Python mới hoặc sửa chứa `encoding=`. [ADR-0060 M3](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L43)
- Model và effort phục vụ là `KHONG_DO_DUOC` từ metadata hiện có. Launcher vẫn ghi `dang_chay` khi đọc. Rc con, stdout hash và trạng thái terminal của launcher chỉ xác minh được khi run kết thúc.

## Readback và kết luận

Head và tree khớp ở đầu và cuối. `git diff --exit-code` và `git diff --cached --exit-code` đều rc 0 ở checkout được giao và hai clone đo. Checkout được giao có `.codex/` rỗng từ đầu và thêm `.review/VERDICT.md`. Fixture golden và state tự sinh nằm trong clone tạm. Kết quả snapshot xác nhận delta quan sát được giữa hai mốc. Repo nguồn của Executor ngoài phạm vi quan sát.

Còn **0 P0, 1 P1, 2 P2, 0 P3**. Hai lớp mở từ lượt 30 đều còn mở, tỷ lệ đóng lớp **0/2** và có thêm một lớp va chạm khóa. H1 quyết định `REQUEST_CHANGES` theo ngưỡng của prompt. CHƯA ĐỦ ĐIỀU KIỆN MERGE vì H1–H3 còn mở, selftest chưa đạt N/N, doc-claims strict còn đỏ trong checkout shallow và thiếu Windows/CI/connector trên exact head. Lượt này là lời gọi **31/31** của lease r31. [Protocol §8.3](../docs/PROTOCOL_DA_PHIEN.md#L812) · [ADR-0060](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32) · [ADR-0062](../docs/adr/0062-adr-0060-mac-dinh-va-dong-bang-adr-0054.md#L12)

P2_mo: 2
VERDICT: REQUEST_CHANGES
