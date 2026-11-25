# Verdict packet #1525 r10 lượt 10 — Codex

reviewed_sha: 674a28c6c42342f9ab34651cbadea411a0d05c1d
reviewed_tree: b74cf2aeec95c418697e7989ebeea12f4c3b81c2
base_sha: 64b7f2c14776d5d0e1d34a6be4725490956f5bec
base_tree: 0cc14e79cecd2ce44bc4dc6cff92cadb31fd7ee4

## Preflight

- Checkout detached của `ducthangho/tra-luat`. Ref cục bộ và remote-tracking của `ccr-89c0d2e2-inanqb` đều trỏ exact head. Base và mốc cuối #1514 `fcb12b3873c3bec2c339029136243ed2c804ce05` là tổ tiên của head. Mốc bản vá r10 là `494f009eb969d57ee2bdca46dca69d879a07e3e9`, commit lưu hồ sơ lượt 9, trong đó verdict neo ứng viên r9 `4c647c8846939281d268e3efb2abe9c22d985e03`. `origin/master` trong bản sao ghi OID `5259239d763c9ffc1677f033bd9a9cf23ede9299`. Baseline nghiệm thu lấy từ spec và lease.
- Packet #1525 r10/g1, Review Class `sensitive`. Preflight lúc 14:42 UTC ngày 25-11-2026, hạn lease 22:35 UTC. Lượt này là lời gọi 10/11, với 9 đã dùng và ngân sách gọi model của packet là 0. Blob spec tại exact head là `212515e8e7dba242ecf718992dd3ab92ffe8536c`. SHA-256 của blob và bản làm việc cùng là `6f64b9fac394b2b53b7b1d2b525760ec29a2b39f7b091b8bfea11ccdecd0a813`, khớp lease. [Đặc tả](../ops/specs/llm-khoan-docx-r10.md) · [Lease](../ops/leases/llm-khoan-docx-r10-g1-claude.yaml)
- Hash 64 đường dẫn write set, sắp xếp và nối LF, là `ab81c9b08b36ab521423c1ac9b0bd2ad64f35afcee115a64a22bb1575341c841`, khớp lease. So `git diff --name-only --no-renames -z fcb12b3 HEAD` sau loại hồ sơ `ops/acceptance/llm-ranh-gioi-khoan/` còn 57 đường dẫn, tất cả nằm trong write set. Tám đường dẫn ở diff từ `494f009` cũng thuộc tập này. Kiểm cặp `thay_the_cho` / `da_bi_thay_the` đủ 10/10 liên kết #1514 r9 ↔ #1525 r1 ↔ … ↔ r10, đầu r10 chưa có successor. Kiểm SHA-256 blob đặc tả so với lease tương ứng đủ 10/10 đời #1525. [Bia mộ #1514](../ops/leases/llm-ranh-gioi-khoan-r9-g1-claude.yaml) · [Lease #1525 r1](../ops/leases/llm-khoan-docx-r1-g1-claude.yaml)
- Run `400461c06c464e21a608684834263914` qua launcher 1.6.2 ghi reviewer `openai_codex`, `codex_cli`, `machine`. Checkpoint neo exact head và SHA-256 prompt `e20cefeca7bb3ed24424604438106c2559fddb88ee63249c123b6c613ab865a4`, khớp bytes và run metadata. Executor theo lease là `claude` / `claude_code` / `machine/local`. Sandbox thực tế `workspace-write`, checkout review riêng, Linux 6.18.44-fc-v880 x86_64, Python 3.13.18, Git 2.43.0, `core.abbrev=7`. [Protocol §8.1](../docs/PROTOCOL_DA_PHIEN.md#L770)

## Đối chiếu lượt 9 và đặc tả r10

Các bổ sung §2.4–§2.12 thay điểm tương ứng của các mục trước. Trạng thái trong bảng áp cho từng biểu hiện, với trạng thái toàn lớp ở phần Findings. [Verdict lượt 9](../ops/acceptance/llm-khoan-docx/r1/review-9-codex/VERDICT.md)

| Mục | Trạng thái | Bằng chứng |
| --- | --- | --- |
| J1 · §2.12 · cấp từ style | **ĐÃ VÁ THẬT** với đường lai lượt 9 | `tu_style` nhận cả `ilvl` và `numId` từ chuỗi `basedOn`, giữ cờ khi đọc numId trực tiếp. Đoạn mang số theo style bị chặn trước khi ghép. `wp1525_style_chi_ilvl_bo_qua` chết đúng ca đã khai. [Mã](../scripts/tl_core/llm_route.py#L904) · [Ca](../scripts/tl_core/llm_route_test.py#L1449) |
| J2 · §2.12 · định dạng tương thích | **VÁ MỘT PHẦN** | Ba đột biến ở thuộc tính trực tiếp của run, đoạn và styles đều chết. Thuộc tính tương thích dưới `numPr` của style, ngoài cây thuộc tính style đã nhận, hoặc ở level của numbering vẫn có thể bị bỏ qua. Xem K1. [Styles](../scripts/tl_core/llm_route.py#L694) · [Ca](../scripts/tl_core/llm_route_test.py#L1453) |
| J3 · §2.12 · nhãn có chữ | **VÁ MỘT PHẦN** | Nhãn chứa chữ như ca tiêu đề lượt 9 bị chặn, đột biến `wp1525_lvltext_co_chu` chết. Quy tắc chỉ cho placeholder và dấu chưa được cưỡng chế toàn nhãn. Tiền tố tiêu đề viết trong thân đoạn còn K2. [Mã](../scripts/tl_core/llm_route.py#L767) · [Ca](../scripts/tl_core/llm_route_test.py#L1462) |
| J4 · §2.12/§3 · rels của part chính | **VÁ MỘT PHẦN** | Ca riêng đọc `word/_rels/chinh.xml.rels` để chọn đúng numbering. Đột biến quay về tên mặc định chết đúng ca. §3 vẫn mô tả dừng ở Điều kế tiếp, xem K4. [Ca](../scripts/tl_core/llm_route_test.py#L1401) · [§3](../ops/specs/llm-khoan-docx-r10.md#L159) |
| J5 · §2.12 · ngắt trước chữ gạch | **ĐÃ VÁ THẬT** với biểu hiện lượt 9 | Cờ chữ sau ngắt chỉ được chuyển sang lỗi sau khi run vượt bước lọc gạch. Ca dương chữ bị gạch sau ngắt trang đạt, đột biến cũ chết. Ca có chữ còn hiệu lực sau ngắt vẫn từ chối. Ngắt cột dùng chung nhánh. [Mã](../scripts/tl_core/llm_route.py#L855) · [Ca dương](../scripts/tl_core/llm_route_test.py#L1347) |
| §1, §2.1–§2.2 · bất biến và CLI | **ĐẠT** cho các hành vi đã kiểm | Bản vá giữ các đường gọi model và cờ CLI. Ca Điều 3 và ba kết quả lưu vẫn kiểm 8/8. ZIP buộc `--dieu`, cấm số hiệu kèm theo và sẵn có ca CLI rc 0/5/2 dùng stub. Cờ `can_nguoi_duyet: true` và `pham_vi_kiem` được ghi theo nguồn. Rủi ro trước phép so ở K1–K2. [Ca 8/8](../scripts/tl_core/llm_route_test.py#L1060) · [ZIP](../scripts/tl_core/ops_misc.py#L3025) · [Đầu ra](../scripts/tl_core/ops_misc.py#L3126) |
| A1/B1/C1/D1/E1/F1 · §2.4–§2.9 · chọn vùng và fallback | **HẾT ĐỐI TƯỢNG do hợp đồng r7** với cách cắt vùng giữa tệp. **ĐÃ VÁ THẬT** với việc bỏ fallback | Vùng chạy tới hết tệp. Tiêu đề đích phải là đoạn đầu có nội dung, đúng số, đúng hình dạng, có chữ đọc được, không số tự động và không ngắt mềm. Bảng/khối lạ ở bất kỳ đâu bị chặn. Không có numbering tự động trả `ValueError`, CLI rc 2 trước model. G6 và H1 đã xử lý hoa thường trong miền mẫu. K2 nằm ở mẫu nhận diện tiêu đề còn hẹp. [Chọn vùng](../scripts/tl_core/llm_route.py#L992) · [CLI](../scripts/tl_core/ops_misc.py#L3037) |
| A2/B2/C2/D2/E6/F3/F4/F5/G1/G3/H4 · §2.4–§2.11 · số Word | **ĐÃ VÁ THẬT** với các ca số cũ, **HẾT ĐỐI TƯỢNG do hợp đồng r7** với đếm trong bảng | `start` vắng là 0, đối chứng `startOverride` 5→1 đạt. Bộ đếm tách theo numId, reset cấp con, chặn tổ tiên chưa có mục, giới hạn cấp 0–8 và trần 999. ID thập phân ASCII được chuẩn hoá và trùng thì chặn, style ID lỗi giữ dấu riêng. Khoản phải cùng danh sách, nhãn `decimal` đúng cấp và dãy số từ 1. Chốt các dạng restart/style link đã khai có mặt. K1 và K3 chỉ ra phần kiểm định nghĩa còn hở. [Numbering](../scripts/tl_core/llm_route.py#L623) · [Bộ đếm](../scripts/tl_core/llm_route.py#L964) · [Phân vai](../scripts/tl_core/llm_route.py#L1032) |
| A3/C3/D6 · §2.4–§2.7 · từ nối và dấu | **ĐÃ VÁ THẬT** với biểu hiện cũ | Dò từ nối chỉ trong đoạn mở khoản, ngoài ngoặc/trích dẫn và trước dấu hai chấm cấp khoản. Chốt dấu phân cách áp trên chữ mọi đoạn của vùng. Miễn chốt riêng cho điểm gõ tay hết đối tượng. Omit, gộp, cắt, tráo khoản ở đầu ra bị phát hiện khi chuẩn phân đoạn nguồn đúng. [Chốt dấu](../scripts/tl_core/llm_route.py#L1078) · [So đủ hai vế](../scripts/tl_core/llm_route.py#L1252) |
| A4/B3/C4/D3/E2/E5/G2/H2 · §2.4–§2.11 · markup và định vị part | **ĐÃ VÁ THẬT** cho các biểu hiện và ca cũ đã xác định. Lớp còn K1 | Đọc cây XML gốc, bỏ `del`/`delText`/`moveFrom`, giữ `ins`/`moveTo`, chặn revision dấu đoạn. Hai loại gạch tính riêng, nhiều tầng chặn khi thiếu định dạng trực tiếp quyết định. Các đột biến regex cũ, moveFrom, style và part chính đều chết. Part chính theo quan hệ gốc, styles/numbering theo rels của part đã chọn. [Styles](../scripts/tl_core/llm_route.py#L694) · [Run](../scripts/tl_core/llm_route.py#L832) · [Part chính](../scripts/tl_core/llm_route.py#L605) |
| A5/E3/E4 · §2.4/§2.8 · danh sách ngoài Điều và bảng | **HẾT ĐỐI TƯỢNG do hợp đồng r7** với đoạn ngoài Điều và duyệt hàng/ô | Bảng bị chặn toàn tệp. Định nghĩa numbering không hỗ trợ nhưng không được dùng có ca dương. Lỗi parse của part vẫn làm dừng ngay khi nạp. [Kiểm danh sách dùng](../scripts/tl_core/llm_route.py#L1032) · [Ca dương](../scripts/tl_core/llm_route_test.py#L1278) |
| A6/F2 · §2.4/§2.9 · điểm gõ tay DOCX | **HẾT ĐỐI TƯỢNG do hợp đồng r7** với yêu cầu nhận điểm gõ tay. **ĐÃ VÁ THẬT** cho đường ghép cũ | Đoạn không số sau khoản đầu trả lỗi. Điểm chữ và điểm gạch có ca riêng. Cấp con phải cùng danh sách, có đủ tổ tiên. Trước khoản đầu chỉ được vắng hoặc đúng một câu dẫn khớp toàn mẫu. [Ghép khoản](../scripts/tl_core/llm_route.py#L1046) · [Câu dẫn](../scripts/tl_core/llm_route.py#L1088) |
| B4/B5/B6/C5/D5/F6/G4/H5 · §2.5–§2.11 · phần tử và ngắt | **ĐÃ VÁ THẬT** với các biểu hiện cũ | Các ca `noBreakHyphen`, tab/ptab, wrapper, mốc move, số thập phân, Strict và ngắt đều đạt. Chữ hữu hiệu sau ngắt trang bị chặn, ngắt cuối đoạn được nhận. Khác biệt giữa điểm gõ tay và đầu thân khoản có số thập phân đã được kiểm. [Danh sách](../scripts/tl_core/llm_route.py#L529) · [Ca](../scripts/tl_core/llm_route_test.py#L1268) |
| A7/B7/C6/D4/E5/F5/G5/H3 · §3 · test độc lập | **ĐÃ VÁ THẬT** với các ca đích lịch sử còn thuộc hợp đồng | Harness xác nhận các đột biến số, markup, dấu, wrapper, gạch tay, chuẩn hoá abstract ID và numbering đổi tên chết tại ca đã khai. Tổ hợp rels part chính có ca riêng mới. Phần mô tả §3 còn K4. [Bảng đột biến](../scripts/tl_core/llm_route_test.py#L1578) · [Harness](../scripts/tl_core/llm_route_test.py#L1845) |
| A8/B8/C7 · hướng dẫn | **ĐÃ VÁ THẬT** với mâu thuẫn đã báo | Tài liệu nêu một khoản một dòng ở TXT, một Điều một DOCX, cả hai kiểu dấu cuối nhãn khoản, không nhận numbering qua style và chỉ nhận điểm tự động cùng danh sách. [Hướng dẫn](../docs/GOI_AGENT_DA_NEN.md#L370) |
| K1 **của #1514** · §2.3 · điểm và tiếp dòng “là” | **ĐÃ VÁ THẬT** cho cả hai đường ghép | `_RE_DIEM` khớp thì cả hai loại nguồn trả `None`. Với nguồn có số, dòng mở bằng “là” rơi xuống nhánh từ chối mọi dòng không số. Nguồn mất số không ghép dòng, phép so từ chối mục mở bằng “là” do vế thuật ngữ rỗng. Ca nguồn có/mất số và tiếp dòng nguồn có số đều có sẵn. [Bộ tách](../scripts/tl_core/llm_route.py#L1121) · [Ca điểm](../scripts/tl_core/llm_route_test.py#L1170) · [Ca tiếp dòng](../scripts/tl_core/llm_route_test.py#L808) |

**Đường thô.** Hai cửa K1 đã đóng. Một dấu điểm ngoài miền `_RE_DIEM` trong nguồn mất số vẫn có thể thành dòng định nghĩa tự đứng nếu qua đủ các chốt. Một tiểu mục mang số trùng số khoản kế có thể lọt khi toàn nguồn đã bị làm phẳng và các dòng đều đạt dãy số, dấu kết, chốt dấu phân cách và từ nối. Tệp đã cắt trước khi đưa vào, hoặc chữ đã gạch/xoá bị làm phẳng thành TXT, cũng có thể khớp chính văn bản còn lại. Đây là giới hạn đường thô đã được ghi ở lượt 9. Tuyến số hiệu chặn cảnh báo CAP và chuyển tiếp cảnh báo markup từ `tl extract`. [Lượt 9](../ops/acceptance/llm-khoan-docx/r1/review-9-codex/VERDICT.md#L42) · [Phạm vi đường thô](../scripts/tl_core/llm_route.py#L1094) · [CAP](../scripts/tl_core/llm_route.py#L1357)

## Findings

### K1 [P1] Nhánh tương thích còn có thể đổi chữ hoặc số hiển thị mà reader bỏ qua — `scripts/tl_core/llm_route.py:645,704,714`

**Kịch bản và căn cứ.** Nếu một `w:style` nằm trong nhánh `mc:AlternateContent` ở cấp `w:styles`, thuộc tính gạch bên trong style ấy có thể gồm toàn con namespace `w` hợp lệ. Phép quét dòng 704 chỉ nhìn con trực tiếp của `rPr` và `pPr`, vì thế không thấy wrapper ở trên. `goc.findall(w:style)` bỏ qua style đó, rồi các hàm tra style coi ID được đoạn hoặc run trỏ tới là không có định dạng. Một run gạch theo style có thể trở thành chữ chuẩn của khoản. Cùng khe xử lý tồn tại ở `numbering.xml`. Nếu nhánh tương thích ở cấp `w:lvl` đưa vào một quy tắc `lvlRestart` làm cấp con tiếp tục, reader không thấy con trực tiếp `lvlRestart` và vẫn reset cấp con mỗi lần cấp cha tăng. Nhãn điểm sai sau reset trở thành chuẩn so. Riêng `mc:AlternateContent` trong `w:numPr` dưới `w:pPr` của style cũng nằm ngoài phép quét dòng 704, dù bản vá đã kiểm vị trí tương ứng ở numPr của đoạn. Hạng P1 vì chuẩn so cấu trúc có thể bao gồm chữ đã bỏ hoặc nhãn khác số hiển thị. Đây là lần theo mã, chưa tái lập trên Word. [Tra style](../scripts/tl_core/llm_route.py#L733) · [Đọc run](../scripts/tl_core/llm_route.py#L832) · [Reset](../scripts/tl_core/llm_route.py#L979)

**Đề xuất.** Kiểm lớp markup compatibility tại nơi đọc các định nghĩa và cây thuộc tính quyết định chữ/số. Khi chưa giải được một lựa chọn có thể đổi style, cấp hoặc cách reset, từ chối trước khi tạo chuẩn so. Kiểm cả cây được chọn và đối chứng định dạng trực tiếp hoạt động bình thường.

### K2 [P1] Tiêu đề Phần dùng số thứ tự viết bằng chữ có thể nhập vào khoản — `scripts/tl_core/llm_route.py:525,1015,1062`

**Kịch bản và căn cứ.** §2.9 yêu cầu từ chối đoạn mở bằng tiêu đề Điều, Chương, Mục hoặc Phần trong vùng. Regex hiện đòi sau Chương/Mục/Phần là số Ả Rập hoặc ký tự La Mã. Một tiêu đề Phần với số thứ tự viết bằng chữ lọt bước này. Nếu đoạn ấy mang numbering cấp con của chính danh sách đang mở, các guard phần tử, số gõ tay, cùng numId và dãy số khoản vẫn có thể qua. Nhánh cấp con nối tiêu đề vào định nghĩa khoản trước và phép so có thể trả khớp theo khối đã nối. Trường hợp tiêu đề đứng riêng không số đã bị chặn. Hạng P1 vì vi phạm điều kiện một Điều của đường cấu trúc có thể chuyển thêm nội dung sang khoản đã kiểm. [Hợp đồng một Điều](../ops/specs/llm-khoan-docx-r10.md#L116) · [Guard](../scripts/tl_core/llm_route.py#L1014) · [Phân vai](../scripts/tl_core/llm_route.py#L1057)

**Đề xuất.** Nhận diện các kiểu số thứ tự của tiêu đề cấu trúc, kể cả kiểu viết bằng chữ. Đo phản chứng tiêu đề nằm ở cấp con cùng danh sách và đối chứng dẫn chiếu Phần ở giữa thân khoản.

### K3 [P2] Kiểm `lvlText` chưa thực thi danh sách cho phép của J3 — `scripts/tl_core/llm_route.py:767,786`

**Kịch bản và căn cứ.** Nhánh nhãn không phải bullet xóa các đoạn khớp `%\d` rồi chỉ tìm ký tự từ loại chữ. Sau đó chỉ cần kết quả dựng nhãn khác rỗng. Một chuỗi nhập bằng chữ số trần, một dấu phần trăm không tạo placeholder, hoặc ký tự định dạng vô hình có thể qua. Điều đó rộng hơn hợp đồng placeholder và dấu, và một nhãn cố định bằng số có thể xuất hiện dù không tham chiếu bộ đếm. Hạng P2 vì đây là thiếu điều kiện chặn theo spec, với đầu ra sai chưa được xác lập riêng cho dạng này. [J3](../ops/specs/llm-khoan-docx-r10.md#L153) · [Kiểm nhãn](../scripts/tl_core/llm_route.py#L767)

**Đề xuất.** Kiểm toàn chuỗi nhãn của các dạng dùng số theo miền placeholder/các dấu được hỗ trợ. Giữ rõ phép chuẩn hoá bullet sang dấu gạch theo đặc tả.

### K4 [P2] §3 vẫn mô tả ca dương theo quy tắc điểm cắt đã bị thay — `ops/specs/llm-khoan-docx-r10.md:162`

**Kịch bản và căn cứ.** Phần J4 về đọc rels riêng đã có ca đích và đột biến. Nửa còn lại của finding vẫn còn. §3 ghi ca dương “dừng ở Điều kế tiếp”, trong khi ca dương đọc tới hết một Điều, và ca âm từ chối tệp chứa tiêu đề Điều khác. Giữ hai mô tả nghiệm thu đối nghịch làm mơ hồ oracle của ca đối chứng ở một revision đóng băng. Hạng P2 vì sai hợp đồng nghiệm thu. Đường runtime hiện từ chối tiêu đề Điều thông thường ở vùng. [§3](../ops/specs/llm-khoan-docx-r10.md#L159) · [Ca âm](../scripts/tl_core/llm_route_test.py#L1477) · [J4 lượt 9](../ops/acceptance/llm-khoan-docx/r1/review-9-codex/VERDICT.md#L72)

**Đề xuất.** Ở revision đặc tả tiếp theo, mô tả ca dương một Điều và ca âm chứa Điều khác bằng đúng hành vi r7. Giữ riêng ca rels của part chính đổi tên.

| Lớp | Biểu hiện kế thừa và đang mở | Hạng cao nhất | Bằng chứng cần để đóng |
| --- | --- | --- | --- |
| `docx-markup-du-thao` | A4/B3/C4/D3/E2/G2/H2 → J2 → K1. Chốt tương thích trực tiếp có ca dương/âm. K1 còn style và định nghĩa numbering. | P1 | Kiểm thuộc tính hiệu lực ở cả part styles và numbering trước khi phân đoạn. |
| `ranh-gioi-khoan` | A1/F1/G6/H1 → J3 → K2. Phần cắt sớm r7 hết đối tượng. K1 của #1514 đã đóng ở đường thô. | P1 | Nhận diện tiêu đề trước khi nối cấp con và khóa ca một Điều. |
| `docx-so-hien-thi` | A2/B2/C2/D2/F3/G1/H4 → J1. Đường lai J1 đóng. K3 là biểu hiện về miền nhãn, liên quan J3. | P2 | Kiểm toàn nhãn theo miền đã công bố, giữ đối chứng start, override và reset. |
| `do-phu-chot-docx` | A7/B7/C6/D4/E5/F5/G5/H3 → J4 → K4. Đột biến rels đã chết. | P2 | §3 diễn đạt đúng ca dương và ca âm r7. |

Tổng cộng 4 finding trên 4 lớp còn mở. Lớp `docx-ngat-trinh-bay` G4/H5 → J5 đóng biểu hiện đã báo. Đây là lượt 10/11. Các lớp markup và ranh giới đã lặp qua nhiều lượt và thuộc diện Review Rescue Checkpoint theo §12. Theo ADR-0060 M1, exact head này chưa đạt điều kiện merge. [Protocol §8.3](../docs/PROTOCOL_DA_PHIEN.md#L812) · [Protocol §12](../docs/PROTOCOL_DA_PHIEN.md#L1097) · [ADR-0060 M1](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32) · [ADR-0062](../docs/adr/0062-adr-0060-mac-dinh-va-dong-bang-adr-0054.md#L10)

## Kết quả test và đột biến

Các lệnh dưới đây dùng `PYTHONDONTWRITEBYTECODE=1`. Log và rc lưu tại `/tmp/wp1525-review.eUTwLqki/`. Hai checkout đều ghim `core.abbrev=7`.

| Lệnh | Trạng thái | Rc và bằng chứng dương hoặc nguyên nhân |
| --- | --- | --- |
| `python scripts/tl_core/llm_route_test.py` | `passed` | rc 0, **63/63** ca, **175/175** đột biến chết tại ca đích, gồm **78/78** mục `wp1525_*`. `llm_route.log` và `mutation-targets.log`. |
| `python scripts/tl.py --deterministic workflow-audit --strict --json` | `passed` | rc 0, `ok=true`, 26 card, 60 task, 194 lệnh hiện diện, 0 lỗi và 0 cảnh báo. `workflow.log`. |
| `python scripts/tl.py --deterministic golden-test --json` | `passed` | rc 0, `ok=true`, **20/20** ca, bản chiếu ổn định **20/20**, byte thô ổn định **19/20**. `hygiene_sweep_fixture` có `diff={}` sau chiếu. `golden.log`. |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json`, checkout review | `failed` | rc 2, **187/187** tệp đã kiểm, `extra_files=[".review/VERDICT.md"]` vì verdict đã được ghi sớm. `release.log`. |
| Cùng lệnh release trên clone sạch ở exact head/tree | `passed` | rc 0, `ok=true`, **187/187** tệp, 0 sai/thiếu/thừa. Băm đọc lại `8266ef41b1eb28568e5af9142173c4432f9bd3f71461ce2c54ccbecec3fd6035` khớp manifest. `release-clean-head.txt`, `release-clean.log`. |
| `python ops/lease_publish.py check --root . ops/leases/llm-khoan-docx-r10-g1-claude.yaml` | `passed` cục bộ | rc 0, “ĐĂNG ĐƯỢC”, Issue #1525, neo `64b7f2c14776`, hết hạn 22:35 UTC. `lease.log`. |
| `python scripts/tl.py --selftest`, head | `failed` | rc 1, **1774/1790**, transport **12/12**, ca CLI mới #1525 **OK**. `selftest.log`. |
| Cùng lệnh selftest, clone ở exact baseline | `failed` | rc 1, **1773/1789**, transport **12/12**. `base.log`. |
| `git diff --check 494f009 HEAD` và `git diff --check fcb12b3 HEAD -- . ':!ops/acceptance/llm-ranh-gioi-khoan/'` | `passed` | rc 0 cho từng diff. |
| `git diff --check 64b7f2c HEAD` và `git diff --check 64b7f2c fcb12b3` | `failed` | rc 2 mỗi lần, cùng ba dòng xuống hàng Markdown có khoảng trắng cuối dòng trong [hồ sơ #1514](../ops/acceptance/llm-ranh-gioi-khoan/r1/review-8-codex/VERDICT.md#L3). Diff toàn PR có 105 đường dẫn. |

`diff -u` giữa hai danh sách dòng `[FAIL]` trả rc 0. `diff -u` giữa toàn bộ dòng `[OK]`/`[FAIL]` cũng trả rc 0 sau khi loại đúng ca mới #1525 khỏi head. Cả hai có cùng 16 ca đỏ. Trong đó 8 `r973_bootstrap_*`, 5 `wp433_*` và `wp727_tl_gws_refresh` thuộc nhóm `/tmp/.git` rỗng prompt đã ghi. Hai ca còn lại là `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` và `r268_l2_trichotomy_theo_trang_thai_object`, cũng đỏ trên nền. Chênh lệch theo tên ca đỏ là 0 và selftest vẫn chưa đạt N/N. SHA-256 log head `964975aaa36028df4a07858a902c89fcf7fce2ade5b11d1d33d5e993a2136aa2`, log base `e874d957e2fcc7b453a26983353b6c39808c15d654e9629bd8556d1e91df729e`.

Tôi chạy thêm `python -m pdb` trên chính `scripts/tl_core/llm_route_test.py`, đặt breakpoint có điều kiện cho `wp1525_*` tại dòng 1865, sau khi ca đích ném `TinHieuChotCa`. Rc trình gỡ lỗi và suite đều 0. Có 78 hit tên đột biến/ca đích. SHA-256 log `a28a46d101827269dc495e7a8eef1ad59992d6530cceab2a9daeb0e5ae588be5`. Harness mở module đã đột biến ở thư mục tạm, yêu cầu đúng một neo và chỉ tính sống/chết theo ca đích. [Harness](../scripts/tl_core/llm_route_test.py#L1845)

| Đột biến sẵn có | Ca đích quan sát được |
| --- | --- |
| `wp1525_style_chi_ilvl_bo_qua`, `wp1525_mc_trong_rpr_bo_qua`, `wp1525_mc_trong_styles_bo_qua`, `wp1525_mc_trong_ppr_bo_qua`, `wp1525_lvltext_co_chu` | `ca_cau_truc_docx_chan`. Gồm J1, ba vị trí trực tiếp của J2 và tiền tố chữ của J3. |
| `wp1525_rels_part_chinh_mac_dinh` | `ca_cau_truc_docx_rels_part_chinh`. J4 mất tệp quan hệ của part đã chọn. |
| `wp1525_gach_sau_ngat_la_ngat` | `ca_cau_truc_docx_dat`. J5 chặn lại đối chứng chỉ còn chữ gạch sau ngắt. |
| `wp1525_tho_nhan_diem` | `ca_wp1514_luot9`. Guard cho nguồn thô có hoặc mất số. |

Không có lệnh nào trong sáu lệnh prompt mang trạng thái `skipped`.

## Không đo được

- K1–K3 là kết luận đọc mã. Tổ hợp tương thích xác định style/cấp Word, tiêu đề Phần viết số thứ tự bằng chữ ở cấp con, và các nhãn ngoài miền J3 chưa được đo bằng ca mới. Hình thức tiêu đề số thứ tự viết chữ có mô tả trong tài liệu repo. Ca đột biến sẵn có giết các biểu hiện đã nêu trong bảng, với độ phủ giới hạn ở các fixture đó. [Thể thức](../references/THE_THUC_TRINH_BAY.md#L313)
- Chưa xác lập thêm phần tử Word/Google Docs thường gặp bị chặn oan ngoài phạm vi đã công bố. §2.5 và các bổ sung đã nhận bookmark, comment anchor, proofing, hyperlink, tab/ptab, dấu nối không ngắt và các wrapper có trong ca sẵn. Bảng, hình, trường, ký hiệu, chú thích, Strict, đánh số qua style và tệp nhiều Điều thuộc giới hạn đã khai. Độ phổ biến trên bản export thực tế và hành vi ứng dụng với các tổ hợp OOXML chưa có mẫu vẫn chưa đo. [Danh sách phần tử](../scripts/tl_core/llm_route.py#L529) · [Giới hạn người dùng](../docs/GOI_AGENT_DA_NEN.md#L390)
- `not_run` trong lượt kiểm chứng này gồm `determinism-audit --strict`, `doc-claims-check --strict` độc lập, Ruff contract/lint, GitHub/CI và hai lớp GitHub của kiểm lease. Windows là `required` theo ADR-0060 M3 vì diff toàn PR thêm dòng Python có `encoding=`. Windows bản địa và Windows CI còn `not_run`. [§5 của đặc tả](../ops/specs/llm-khoan-docx-r10.md#L174) · [ADR-0060 M3](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L43)
- Codex CLI cục bộ báo 0.172.0. Model/effort phục vụ lượt, terminal rc của reviewer và băm stdout cuối của launcher chưa xác minh qua dữ liệu của run đang hoạt động. Snapshot đầu/cuối đo delta quan sát được trong checkout giao. Repo Executor và head từ máy chủ nằm ngoài phép đo offline.

Head và tree cuối khớp preflight. Diff tracked và index rỗng. Ca chạy lần đầu sinh fixture và cache ignored trong checkout, đã chuyển hai thư mục phát sinh sang scratch. Readback chỉ còn `.review/VERDICT.md` untracked và `.codex/` ignored đã thấy từ đầu. Không có fixture hay chuỗi phản chứng mới. Không dùng dịch vụ model hoặc GitHub.

Exact head có **0 P0, 2 P1, 2 P2, 0 P3** mở. Hai P1 chặn verdict approve và bốn finding chặn merge theo M1. Các gate bắt buộc còn đỏ hoặc chưa đo được nêu ở trên.

P2_mo: 2
VERDICT: REQUEST_CHANGES
