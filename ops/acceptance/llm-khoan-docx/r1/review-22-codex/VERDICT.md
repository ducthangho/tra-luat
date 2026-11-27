# Verdict packet #1525 r22 lượt 22 — Codex

reviewed_sha: fbddd4771e7ac3359f19a88d13b841b8d23624fc
tree_sha: 278ad782083f89fb6c2db46fa08580b7e66f40f5
base_sha: 64b7f2c14776d5d0e1d34a6be4725490956f5bec
VERDICT: REQUEST_CHANGES

## Đối chiếu lượt 21 và đặc tả r22

- Checkout detached của `ducthangho/tra-luat`. Ref cục bộ `origin/ccr-89c0d2e2-inanqb` trỏ cùng head. Base là tổ tiên của head, tree base `0cc14e79cecd2ce44bc4dc6cff92cadb31fd7ee4`. Mốc kế thừa #1514 là `fcb12b3873c3bec2c339029136243ed2c804ce05`, mốc trước bản vá r22 là `343b413c70b9efa35964d8db6f70f1066d80def3`.
- Lease r22/g1 khai `sensitive`, 21 lượt trước trên trần 22, và quyền đứng của chủ kho. Blob spec `a80f4d070a2b54a5f9e64c0d589e8a3cf909232b` có SHA-256 `58971cf7a79d27a32698f28ab4fc7a61a8a508391dde19f7d01c131eb2633ebc`, khớp lease (blob `e946acb1eba83a09cc02c7e2059a928aaa213f4c`). So YAML được **22/22** cặp `da_bi_thay_the` ↔ `thay_the_cho` và **23/23** spec hash từ #1514 r9 tới #1525 r22. Launcher bắt đầu 10:46:12 UTC, trước mốc `leased_at_utc` 10:50 UTC trong lease Executor. `lease_publish.py check` trả 0 theo phép kiểm hạn cục bộ (§4 protocol). Mốc bắt đầu lease Executor và thời điểm launcher review là dữ liệu riêng. [Spec](../ops/specs/llm-khoan-docx-r22.md) · [Lease](../ops/leases/llm-khoan-docx-r22-g1-claude.yaml) · [Protocol §4](../docs/PROTOCOL_DA_PHIEN.md#L241)
- Write set **121** đường dẫn, SHA-256 `17bfcc9e7c90b8b110db83ef84e5ba20763e8cfe508a2096d2343107d99882ae` sau sắp xếp và kết LF. Diff r22 **8/8**, diff packet **117/117** sau khi loại bốn đường dẫn hồ sơ #1514 theo prompt. Trong diff toàn PR **165** đường dẫn, 48 ngoài write set r22 gồm 44 kế thừa ở mốc `fcb12b3` và bốn tệp hồ sơ kết thúc #1514 đã loại. `git diff` các dải, SHA-256 theo thứ tự PR, packet, r22 là `21cd906727d86624d67f29b32b79acaa3ce79a3fdb806c14cb28540fa3b1ac77`, `06c73996943b7d55daa9a2a822cd21db920fb6df107e42e1407b0f657476187c`, `c44ad8a70529acb99eb3e6a3c222996d2c7184657e9c512e04b6845dbc22dd25`.
- Reviewer `openai_codex / codex_cli / machine`, Codex CLI 0.172.0, launcher 1.6.2, run `9c1dd1c9c2b44411a56b38e3bda347d2`. Prompt SHA-256 `e83ee0d098ceed0827dbebcba84fe4a369ad343db1b5e9396aed41cf6eae43b4` khớp `run.json`. Executor `anthropic_claude / claude_code / machine/local` theo lease, chỉ thị gắn với `session_015GtxrZQYT3Vt8PJdXrjEKg`. Linux x86_64, Python 3.13.18, Git 2.43.0, shallow, `core.abbrev=7`, sandbox `workspace-write` với metadata Git của checkout review chỉ đọc. Model và effort phục vụ `KHONG_DO_DUOC` trong lúc phát verdict. [Protocol §8.1](../docs/PROTOCOL_DA_PHIEN.md#L770)

| Mục | Trạng thái | Bằng chứng |
| --- | --- | --- |
| X1 · lượt 21 `3d21bd16411594ab811a964e9b2b2e5172228850` · §2.24 | **ĐÃ VÁ THẬT** cho hai biểu hiện báo ở lượt 21, **VÁ MỘT PHẦN** với lớp | `_ruot_bi_bo` nhận tab/ptab/br/cr qua cùng nhánh cho cả `del` và `moveFrom`; `delText` lạc chỉ có khoảng trắng được giữ. Hai mutant r22 chết ở ca dương. Nhánh run gạch vẫn phân loại ruột khác nhánh chung, xem Y1. [Mã](../scripts/tl_core/llm_route.py#L966) · [Ca](../scripts/tl_core/llm_route_test.py#L1442) |
| X2 · lượt 21 · §2.24 | **ĐÃ VÁ THẬT** cho các trường được nêu, **VÁ MỘT PHẦN** với lớp | `lvl` và liên kết `abstractNumId` lặp đánh dấu lỗi định nghĩa; `numPr` và `basedOn` lặp chặn part. Đối chứng danh sách lỗi không dùng vẫn qua. Gốc body, ruột content control và khóa style còn có thể được chọn ngầm, xem Y2. [Mã](../scripts/tl_core/llm_route.py#L617) · [Ca](../scripts/tl_core/llm_route_test.py#L1630) |
| X3 · lượt 21 · §2.24 | **ĐÃ VÁ THẬT** cho hai dạng đã báo, **VÁ MỘT PHẦN** với lớp | Regex nhận nhãn chữ + gạch khi giữa chúng có không hoặc một dấu cách ASCII và sau gạch có khoảng trắng. Ca dương thô vẫn nhận từ ghép và chữ viết tắt, mutant bỏ nhánh gạch chết. Còn dạng nhãn phân biệt được trong miền mà DOCX sinh ra, xem Y3. [Regex](../scripts/tl_core/llm_route.py#L497) · [Ca](../scripts/tl_core/llm_route_test.py#L686) |
| §1–§2.3 · K1 từ #1514 | **ĐÃ VÁ THẬT** cho hai biểu hiện K1 | Dòng điểm nhận diện được luôn trả `None`. Sau khoản có số, dòng mở bằng “là” là dòng không số nên cũng trả `None`. Ở nguồn mất số, phép so từ chối vế thuật ngữ rỗng. `ca_wp1514_luot9` khóa các dòng điểm, `ca_wp1514_luot2` giữ fixture Điều 3 và ba kết quả lưu 8/8. Hai tuyến gắn `can_nguoi_duyet` và `pham_vi_kiem` tương ứng. So toàn văn theo vị trí, số lượng, số thứ tự và hai vế, vì vậy bỏ/cắt/gộp/tráo mục bị bắt nếu chuẩn nguồn đã dựng đúng. Phạm vi diff giữ nguyên cờ CLI và mã gọi model. [Tách khoản](../scripts/tl_core/llm_route.py#L1291) · [Phép so](../scripts/tl_core/llm_route.py#L1450) · [CLI](../scripts/tl_core/ops_misc.py#L3133) |
| §2.4–§2.9 · A1/A6, B1/B2, C1/C2, D1/D4/D6, E1/E3/E4, F1/F2 | **HẾT ĐỐI TƯỢNG** cho thuật toán cắt cuối Điều, đếm bảng, điểm gõ tay và `KhongCauTruc`. Chốt r7 hoạt động trên cây đã đi qua bộ duyệt | Tiêu đề đích là đoạn có nội dung đầu. Vùng kéo tới hết tệp. Bảng/khối lạ, ngắt mềm, đoạn đánh số rỗng và đoạn không số sau khoản đầu bị từ chối. Câu dẫn trước khoản đầu chỉ có thể vắng hoặc đúng một câu chuẩn; DOCX thiếu số và lỗi cấu trúc đều ra rc 2, đường CLI không rơi sang văn bản thô. Vùng duyệt vẫn có thể mất nội dung ở wrapper mâu thuẫn, xem Y2. [Vùng Điều](../scripts/tl_core/llm_route.py#L1181) · [Câu dẫn](../scripts/tl_core/llm_route.py#L1271) · [CLI](../scripts/tl_core/ops_misc.py#L3037) |
| §2.4–§2.11 · A2/A5, B2/B5, C2, D2, E6, F3/F4/F5, G1/G3, H4 · bộ đếm | **ĐÃ VÁ THẬT** cho các dạng đã báo, với lớp còn mở ở Y2 | Đếm từng `numId`, lấy `startOverride` đè `start`, mặc định `start=0` nếu vắng, xóa bộ đếm cấp con khi tiến cấp cha và từ chối nhảy cấp. Cấp khoản phải là decimal cùng placeholder, khoản liên tục từ 1, một danh sách. Chặn `lvlRestart`, liên kết style, đánh lại sau ngắt section, `ilvl` ngoài miền và thứ tự trên 999. Ca dương đo `startOverride` khác `start` và đặt lại điểm ở khoản sau; ca âm chặn `numId` khác. [Định nghĩa](../scripts/tl_core/llm_route.py#L735) · [Bộ đếm](../scripts/tl_core/llm_route.py#L1167) · [Gom khoản](../scripts/tl_core/llm_route.py#L1225) |
| §2.4–§2.8 · A3/A4, B3/B4/B6, C3/C4/C5, D3/D5, E2/E5 | **ĐÃ VÁ THẬT** cho các biểu hiện đã báo trong DOCX, ngoại trừ phần lớp X1/Y1 | Dò từ nối chỉ ở đoạn mở khoản, từ chối dấu phân cách mơ hồ. Đọc XML gốc; gạch đơn/kép tính riêng, gạch trực tiếp đè chuỗi style và tầng bật mâu thuẫn bị chặn. `del/moveFrom` lọc, `ins/moveTo` đọc, sửa dấu đoạn bị chặn. Dấu nối không ngắt còn trong chữ; content control inline và metadata wrapper có ca dương. Strict là giới hạn đã khai. [Bộ đọc](../scripts/tl_core/llm_route.py#L981) · [Từ nối](../scripts/tl_core/llm_route.py#L1470) |
| §2.9–§2.15 · F6, G2/G4/G6, H1–H5, J1–J5, K1–K4, L1–L6, M1/M2 | **ĐÃ VÁ THẬT** theo hợp đồng đang hiệu lực, **HẾT ĐỐI TƯỢNG** với phép cắt cuối cũ | Có ca cho ptab, phạm vi move, ngắt trang/cột, tiêu đề không phân biệt hoa thường, part chính/part số/style theo URI quan hệ chính xác và XML UTF-16. `mc:` bị chặn trước khi đọc; nhãn chỉ có placeholder và dấu cho phép. `numPr` kế thừa không được dùng làm ranh giới. Những thay đổi chốt tiền tố sau M1 theo §2.16–§2.21 áp thay mẫu cũ. [Quan hệ](../scripts/tl_core/llm_route.py#L694) · [Nhãn](../scripts/tl_core/llm_route.py#L913) · [Chốt vùng](../scripts/tl_core/llm_route.py#L1208) |
| §2.16–§2.21 · N1–N3, Q1/Q2, R1–R3, S1–S3, T1/T2, U1/U2 | **ĐÃ VÁ THẬT** cho tiền tố và ký tự tới được parser. Phần U2 trong bộ đọc dùng chung là giới hạn đã duyệt | Cấm tiền tố trong thân sau khi chiếu đầu đoạn, danh sách cho phép kiểm trước tách/gộp, BOM một tầng, loại số mũ, số gõ tay dạng ngoặc kín bị chặn và QName khối được đối chiếu. Hướng dẫn yêu cầu xử lý thủ công khi dẫn chiếu mở đầu và giữ nguyên chữ nguồn. `tl extract` có thể lọc ký tự trước parser theo giới hạn U2. [Ký tự](../scripts/tl_core/llm_route.py#L545) · [Hướng dẫn](../docs/GOI_AGENT_DA_NEN.md#L397) |
| §2.22–§2.23 · V1–V4, W1–W5 | **ĐÃ VÁ THẬT** cho truyền strict, chặn mặc định đoạn, CAP, cấp trùng và các dạng điểm đã báo. **VÁ MỘT PHẦN** ở lớp W2/W4/W5 | `--markup-strict` và rc 3 chặn trước model, `docDefaults/pPrDefault/numPr` bị từ chối, `lvl/lvlOverride` cùng cấp báo lỗi khi dùng. Ranh giới và markup của bộ đọc dùng chung ở V3, W1/W3, phần số hiệu W2 là giới hạn được chủ kho duyệt. Phần DOCX và TXT tiếp tục có biểu hiện Y1–Y3. [Strict và CAP](../scripts/tl_core/llm_route.py#L1555) · [Giới hạn](../ops/specs/llm-khoan-docx-r22.md#L280) |
| §3 · A7/A8, B7/B8, C6/C7, D4, E5, F5, G5, H3, J4, K4, L6 | **ĐÃ VÁ THẬT** cho các ca/hướng dẫn lịch sử còn hiệu lực. Phạm vi ca mới ghi bên dưới | Tám mutant r22 chết ở ca đích của bảng có sẵn. Các mutant xóa cả guard theo part không chứng minh độc lập từng phần tử và từng ngữ cảnh wrapper. Hướng dẫn công bố một Điều mỗi DOCX, một dòng mỗi khoản trên đường thô, nhãn cấp được hỗ trợ và giới hạn số hiệu. [Đột biến](../scripts/tl_core/llm_route_test.py#L1839) · [Hướng dẫn](../docs/GOI_AGENT_DA_NEN.md#L390) |

## Findings

### Y1 [P1] Run gạch có thể giữ dấu cách từ nội dung đã bỏ gồm cả chữ — `scripts/tl_core/llm_route.py:1033`

**Kịch bản.** Trong phần giữa định nghĩa, một run gạch chứa cả `delText` có chữ và một phần tử phân cách. Bộ đọc bỏ chữ khỏi `chu_run` ở nhánh `delText`, rồi dùng chính `chu_run` để quyết định giữ khoảng trắng. Dấu phân cách còn lại đủ để run được coi là chỉ có khoảng trắng. Chuẩn so có thể giữ một dấu tách từ vốn nằm trong mẩu sửa đổi phải được bỏ trọn.

**Căn cứ và hạng.** Chính sách W2/X1 quyết định theo cả ruột của mẩu trước khi bỏ chữ. `chunk_payload` tính `delText` có chữ, và `_ruot_bi_bo` cũng làm vậy ở `del/moveFrom`. Run gạch dùng phép đọc khác, nên cùng loại nội dung có hai cách quyết định. P1 vì chữ đưa cho model và chuẩn tự so cùng sai trên đường công bố xác minh từ cấu trúc. Vị trí trong thân định nghĩa cho phép trình tự khoản và từ nối vẫn hợp lệ. [Chính sách](../ops/specs/llm-khoan-docx-r22.md#L285) · [Chính sách r222](../scripts/docx_markup.py#L93) · [Nhánh run gạch](../scripts/tl_core/llm_route.py#L1033)

**Đề xuất.** Dùng cùng phép phân loại ruột trước khi loại cho run gạch, `del` và `moveFrom`. Phân biệt ruột rỗng, toàn dấu phân cách, có chữ và có phần tử chưa biết cách hiển thị. Khóa cả đối chứng giữ dấu cách với đối chứng bỏ trọn mẩu pha chữ và dấu phân cách.

### Y2 [P1] Bộ đọc có thể bỏ khoản hoặc chọn style ngầm khi cây có nhiều ứng viên cho cùng một vị trí — `scripts/tl_core/llm_route.py:957`, `:1065`, `:1150`, `:867`

**Kịch bản.** Content control cấp khối có hai phần `sdtContent`. Phần đầu chứa tiêu đề và các khoản đầu đánh số liên tục, phần sau chứa các khoản còn lại của Điều. Phép duyệt chọn phần đầu, nên các chốt một Điều và số khoản liên tục chỉ thấy tiền tố. Cùng cơ chế xảy ra với hai `w:body` hoặc control nội dòng có hai phần nội dung. Ngoài đường chọn cây, hai định nghĩa cùng `styleId` cũng có thể âm thầm đổi cách tính gạch và số, vì định nghĩa sau ghi đè định nghĩa trước.

**Căn cứ và hạng.** Luật r22 đóng các trường kiểu số/thuộc tính đã liệt kê, nhưng bảng đơn trị của part chính chưa chứa `document/body` và `sdt/sdtContent`. Cả ba vị trí còn dùng `.find()`, rồi coi tập đã chọn là đủ để xác thực. Wrapper cấp khối còn bỏ qua hoàn toàn khi thiếu `sdtContent`, và cả hai nhánh wrapper bỏ qua con cùng cấp ngoài phần nội dung đã chọn. `_doc_kieu` đọc khóa lặp theo quy tắc ghi đè của dict. P1 vì dữ liệu mâu thuẫn có thể qua như một Điều đã dựng đủ, không cần giả thiết Word chọn bản thứ hai. Cách Word sửa hay từ chối gói mâu thuẫn chưa đo. [Bảng đơn trị](../scripts/tl_core/llm_route.py#L617) · [Bộ duyệt khối](../scripts/tl_core/llm_route.py#L943) · [Control inline](../scripts/tl_core/llm_route.py#L1064) · [Chọn body](../scripts/tl_core/llm_route.py#L1150) · [Khóa style](../scripts/tl_core/llm_route.py#L854)

**Đề xuất.** Xác thực vị trí và số lượng của các nút tạo ra cây, cùng tính duy nhất của các khóa dùng để quyết style, trước khi diễn giải. Dùng một quy tắc chung cho wrapper khối và inline, xác nhận metadata hợp lệ và chỉ đi tiếp khi nội dung có đúng một cách chọn. Giữ scope A5 cho định nghĩa danh sách không dùng.

### Y3 [P2] Khoảng đệm hoặc dấu hợp lệ trong nhãn điểm có thể nâng điểm thành khoản ở đường thô — `scripts/tl_core/llm_route.py:497`

**Kịch bản.** TXT mất số khoản nhưng còn nhãn điểm chữ. Word có thể lưu nhiều dấu cách giữa placeholder chữ và dấu gạch hoặc dấu chấm trong `lvlText`; văn bản thô còn có thể biểu diễn khoảng đệm bằng tab hay NBSP. Nếu dòng điểm và khoản trước đều có từ nối cấp dòng và kết câu, nhãn lọt qua chốt được xem là phần đầu thuật ngữ của khoản riêng.

**Căn cứ và hạng.** `_nhan` cho phép nhiều dấu cách trước dấu, còn `_RE_DIEM` chỉ cho tối đa một dấu cách ASCII trước gạch và yêu cầu dấu chấm liền chữ. Nhãn chữ đặt trong cặp ngoặc có khoảng đệm cũng có thể qua chốt cân bằng ngoặc. Cấp con decimal ghép cấp cha như `lvlText=%1.%2.` có biểu hiện cùng lớp. Chốt đầu dòng loại ứng viên số vì sau dấu chấm đầu còn chữ số, còn chốt số nội dòng không bắt phần số đứng sau dấu chấm. Các ký tự thuộc miền cho phép của cả hai tuyến, kể cả TXT tại chỗ. Khi `co_so` sai, mỗi dòng còn lại thành khoản. P2 theo W4/X3 và K1 vì tuyến thô công bố kiểm theo phân đoạn của bộ quét và giữ bước duyệt ranh giới, dù kết quả ghép với nhãn có thể qua và được ghi. [Miền nhãn](../scripts/tl_core/llm_route.py#L913) · [Số nội dòng](../scripts/tl_core/llm_route.py#L516) · [Tách thô](../scripts/tl_core/llm_route.py#L1319) · [Phạm vi kiểm](../scripts/tl_core/llm_route.py#L1287)

**Đề xuất.** Quy định một ngữ pháp nhãn phân biệt được trên văn bản thô, với khoảng đệm ngang nhất quán cho các dấu đã hỗ trợ. Dùng cùng miền cho tách khoản và dò từ nối. Đối chứng cho từ ghép và chữ viết tắt vẫn cần giữ. Khi nhãn mất hoàn toàn hoặc chỉ còn chữ có thể thuộc thuật ngữ, quyết định ranh giới thuộc bước duyệt đã công bố.

| Lớp | Hạng cao nhất mở | Lịch sử và phép đóng |
| --- | --- | --- |
| `docx-khoang-trang-sau-loc` | P1 · Y1 | W2 → X1 → Y1. Đo cùng phân loại ruột cho ba nhánh, có dấu phân cách văn tự/cấu trúc và mẩu pha chữ. |
| `docx-so-hien-thi` | P1 · Y2 | A2/B2/G1/J1/V2/W5 → X2 → Y2. Cùng nguyên nhân chọn một giá trị trong khai báo mâu thuẫn, mở rộng phép đóng tới các nút chọn vùng và khóa style. Giữ các chốt đã đo cho số. |
| `ranh-gioi-khoan` | P2 · Y3 | K1 #1514/V4/W4 → X3 → Y3. Hai biểu hiện K1 đã đóng. Đo miền nhãn còn đọc được và đối chứng khoản đúng một dòng. |
| `docx-markup-du-thao` | Trong giới hạn đã duyệt | V1/W1/W3. Strict được truyền; hạn chế riêng của producer ở đường số hiệu theo §2.21–§2.23. |

Còn **3 finding trên 3 lớp**, gồm **0 P0, 2 P1, 1 P2, 0 P3**. Điều kiện severity theo ADR-0060 M1 chưa đạt. [Protocol §8.3](../docs/PROTOCOL_DA_PHIEN.md#L812) · [ADR-0060 M1–M2](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32) · [ADR-0062](../docs/adr/0062-adr-0060-mac-dinh-va-dong-bang-adr-0054.md#L13)

## Kết quả test và đột biến

Log và mã thoát lưu trong `/tmp/wp1525-r22-review.CgLKVKb9/`. Các clone đối chứng dùng object store được giao ở chế độ đọc và giữ `core.abbrev=7`. Biến `PYTHONDONTWRITEBYTECODE=1` và `GIT_OPTIONAL_LOCKS=0` áp cho các lượt đo.

| Lệnh | Trạng thái | Mã thoát và bằng chứng dương |
| --- | --- | --- |
| `python scripts/tl_core/llm_route_test.py` | `passed` | rc 0, **63/63** ca, **225/225** mutant bị giết, gồm **128/128** mục `wp1525_*` và **8/8** mutant r22. `head.llm-route.log`. |
| `python scripts/tl.py --deterministic workflow-audit --strict --json` | `passed` | rc 0, `ok=true`, 194 lệnh, 26 card, 11 nhóm, 60 task, 0 lỗi, 0 cảnh báo. `head.workflow.log`. |
| `python scripts/tl.py --deterministic golden-test --json` | `passed` | rc 0, **20/20** ca, **20/20** bản chiếu ổn định. **19/20** byte thô ổn định. `hygiene_sweep_fixture` có drift thô với `diff={}` sau chiếu. `head.golden.log`. |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | `passed` trên clone head sạch | rc 0, **187/187** tệp, danh sách sai/thiếu/thừa rỗng. Hash gói kỳ vọng và thực tế cùng `86596d75c85d849a42248d6a0a7ec17cd9539796fd12baf937f5966805d1d71c`. Lần đo ở checkout ghi verdict là `failed` rc 2, tập tệp thừa chỉ có `.review/VERDICT.md`. `clean-head.release.log`, `head.release.log`. |
| `python ops/lease_publish.py check --root . ops/leases/llm-khoan-docx-r22-g1-claude.yaml` | `passed` cục bộ | rc 0, lease #1525 neo đúng base, hết hạn 18:50 UTC. Hai lớp GitHub của lệnh báo `skipped`. `head.lease.log`. |
| `python scripts/tl.py --deterministic determinism-audit --strict --json` | `passed` | rc 0, **15/15** kiểm tra có `ok=true`. `head.determinism.log`. |
| `python scripts/tl.py --deterministic doc-claims-check --strict --json` | `failed` ở cả hai SHA | rc 2, 131 tệp, 410 advisory và cùng cờ cứng `SHA_NOT_A_COMMIT` tại `docs/PROTOCOL_DA_PHIEN.md:1680`. So mảng `flags` head/base rc 0. `git cat-file -t` cho OID này trả rc 128 ở bản sao được giao. `head.doc-claims.log`, `base.doc-claims.log`. |
| Ghim/probe Ruff qua `loi_ruff_ci()` của `.claude/dev/ci_dang_ky_test.py` | `passed` | rc 0, `RUFF_CONTRACT 3 []`. `head.ruff-contract.log`. |
| `python -m ruff check --no-cache --select F --output-format json scripts/tl.py` | `failed` tuyệt đối, delta đạt | Ruff 0.16.9, rc 1 ở cả hai SHA, **12 F821** mỗi mốc. So JSON bỏ đường dẫn tuyệt đối trả rc 0. `head.ruff.log`, `base.ruff.log`. |
| `python scripts/tl.py --selftest` · head trong checkout verdict | `failed` | rc 1, **1773/1790**, transport **12/12**, ca DOCX `r1525_llm_khai_niem_tep_docx_cau_truc` đạt. `head.selftest.log`. |
| `python scripts/tl.py --selftest` · base sạch | `failed` | rc 1, **1773/1789**, transport **12/12**. `base.selftest.log`. |
| `python scripts/tl.py --selftest` · head sạch | `failed` | rc 1, **1774/1790**, transport **12/12**. Ca DOCX của packet đạt. `clean-head.selftest.log`. |
| `git diff --check` · bản vá r22, diff packet #1525 | `passed` | rc 0 với `343b413..HEAD` và `fcb12b3..HEAD` sau loại hồ sơ #1514 theo prompt. |
| `git diff --check` · toàn PR, diff kế thừa #1514 | `failed` ở cả hai dải | rc 2, cùng ba khoảng trắng cuối dòng trong verdict #1514 lượt 8. Hai log khớp byte. `pr.diff-check.log`, `inherited.diff-check.log`. |

So danh sách ID đỏ của head sạch và base sạch trả rc 0. Cả hai có cùng **16 ca đỏ** gồm 14 ca `r973_bootstrap_*` / `wp433_*` / `wp727_tl_gws_refresh` trong môi trường có `/tmp/.git` rỗng, cộng `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` và `r268_l2_trichotomy_theo_trang_thai_object`. Ca duy nhất bổ sung vào tập đạt là `r1525_llm_khai_niem_tep_docx_cau_truc`. `wp44_release_bundle_topology_under_200` chỉ đỏ khi đo trong checkout có verdict và đạt khi chạy lại trên clone head sạch. Kết quả selftest sạch có delta lỗi bằng 0 và vẫn chưa đạt N/N của §5. `clean-head.fail-ids`, `base.fail-ids`.

SHA-256 log tuyến LLM `8d00deed84da7696cce4edc10a61a5f7ae68485473fcbdd70e05502b51f59aa5`, release sạch `28b2b20f79e72ffe7fab3f51952ba7a72ded91f52320d7fda66941db4ccaa95a`, selftest head sạch `5feb5febe18de22bf811574ca99168e0c3e203518d84461af22132771f6fe476`, selftest base `921ec28c6f4beca7f9f4001ef5edff6b9297b84e39b1c56938bc675ba32833d8`.

Harness có sẵn áp đột biến vào bản sao tạm của `llm_route.py`, đòi neo đúng một lần và chỉ đếm mutant chết khi ca đích ném `TinHieuChotCa`. Các ca X1/X2/X3 đạt trên module gốc và các mutant dưới đây đều bị bắt. [Bảng mutant](../scripts/tl_core/llm_route_test.py#L1839) · [Harness](../scripts/tl_core/llm_route_test.py#L2115)

| Mutant r22 | Điều ca đích khóa |
| --- | --- |
| `wp1525_ruot_bo_tab_khong_la_cach` | `ca_cau_truc_docx_dat` bắt mất phân cách khi tab nằm trong `w:del`. |
| `wp1525_deltext_lac_bo_cach` | Cùng ca dương bắt mất phân cách của `delText` lạc chỉ có khoảng trắng. |
| `wp1525_bo_don_tri_document` · `wp1525_bo_don_tri_styles` | `ca_cau_truc_docx_chan` bắt bỏ chốt `numPr` lặp ở đoạn và `basedOn` lặp trong style. |
| `wp1525_bo_don_tri_lvl` · `wp1525_bo_don_tri_num` | Cùng ca âm bắt bỏ chốt `start` lặp ở cấp và liên kết `abstractNumId` lặp trong danh sách. |
| `wp1525_don_tri_lvl_nem_ngay` | Ca dương A5 bắt việc từ chối cả tệp do định nghĩa lỗi không dùng. |
| `wp1525_diem_bo_dang_gach` | `ca_khoan_mat_so_co_diem_dat` bắt việc cho điểm dạng chữ + gạch thành khoản. Cùng ca giữ đối chứng từ ghép và chữ viết tắt. |

K1 có thêm ca `ca_ranh_gioi_luot4` đo dòng tiếp mở bằng “là” ở nguồn có số, và `ca_wp1514_luot9` đo nguồn có số/mất số với điểm trên dòng riêng, kể cả khi mọi dòng kết thúc bằng dấu chấm. `wp1525_tho_nhan_diem` bị giết ở ca thứ hai. [Tiếp dòng](../scripts/tl_core/llm_route_test.py#L854) · [Điểm](../scripts/tl_core/llm_route_test.py#L1222)

## Không đo được

- Y1–Y3 dựa trên đường thực thi đọc từ mã. Phần chưa đo gồm ca đầu-cuối cho các hình dạng đã mô tả, cách Word sửa hoặc từ chối các cấu trúc mâu thuẫn và tần suất của các dạng nhãn trong bản export thực. Phạm vi lượt này dùng ca và đột biến có sẵn.
- Với §2.5, các dạng bookmark/comment/perm, hyperlink, content control, tab và ngắt trang cuối đoạn đã có hỗ trợ trong mã hoặc ca sẵn có. Bảng, ngắt mềm trong đoạn, trường, ký hiệu, hình, chú thích và phần tử `mc:` nằm trong giới hạn. Chưa có bằng chứng đủ về một phần tử phổ biến trong export Word/Google Doc thực bị chặn oan ngoài các giới hạn đã khai. [Danh sách phần tử](../scripts/tl_core/llm_route.py#L604) · [Hướng dẫn](../docs/GOI_AGENT_DA_NEN.md#L390)
- `skipped` cho hai lớp GitHub của lệnh lease. `not_run` cho GitHub/CI từ xa, model thật, Windows bản địa và bare lint đúng bản pin CI 0.15.15. Windows là `required` theo ADR-0060 M3 vì diff có dòng Python đổi `encoding=`. Các kết quả ở đây là phép đo Linux cục bộ. [ADR-0060 M3](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L43) · [Dòng được đổi](../scripts/tl_core/ops_misc.py#L3061)
- Repo nguồn Executor, trạng thái head từ xa và bằng chứng terminal của launcher nằm ngoài phép đo này. Mã thoát con, hash stdout và hash verdict ổn định thuộc biên nhận do launcher ghi sau khi run kết thúc.

## Đọc lại checkout và kết luận

`git rev-parse HEAD 'HEAD^{tree}'` trùng ở hai mốc, diff binary của worktree và index rỗng. Sau khi chuyển dữ liệu sinh trong lúc test ra scratch, `git status --porcelain=v1 --untracked-files=all --ignored=matching` chỉ có `.review/VERDICT.md` mới và `.codex/` đã bị ignore từ đầu. Snapshot mô tả hai lần quan sát. Cả hai clone đối chứng có diff tracked và index rỗng. [Protocol §8.2](../docs/PROTOCOL_DA_PHIEN.md#L797)

Hai P1 và một P2 còn mở. Lượt này dùng lời gọi 22/22 của lease r22. Điều kiện merge theo ADR-0060 M1 chưa đạt. Selftest N/N, doc-claims strict và bằng chứng CI/Windows exact head cũng chưa đủ. [ADR-0060](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32)

P2_mo: 1

VERDICT: REQUEST_CHANGES
