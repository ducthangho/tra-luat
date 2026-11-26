# Verdict packet #1525 r21 lượt 21 — Codex

reviewed_sha: 3d21bd16411594ab811a964e9b2b2e5172228850
reviewed_tree: 301db27bf6021c1c7752b965f54e5ad2b8bb7f56
base_sha: 64b7f2c14776d5d0e1d34a6be4725490956f5bec
VERDICT: REQUEST_CHANGES

## Đối chiếu lượt 20 và đặc tả r21

- Preflight trên checkout detached của `ducthangho/tra-luat`, ref cục bộ `origin/ccr-89c0d2e2-inanqb` cùng trỏ exact head. Tree base `0cc14e79cecd2ce44bc4dc6cff92cadb31fd7ee4`. Baseline nghiệm thu `64b7f2c14776d5d0e1d34a6be4725490956f5bec`, mốc kế thừa #1514 `fcb12b3873c3bec2c339029136243ed2c804ce05`, continuation base và cha trực tiếp `8689b606479e83c39bc02aa38ea9d8fa32ec61c4`. Hai mốc đầu là tổ tiên của head, head lượt 20 `8a685fe0031d4d537cbefc6589087b4fc45d7334` là tổ tiên của continuation base.
- Nguồn đặc tả do prompt chỉ định là `3d21bd16411594ab811a964e9b2b2e5172228850:ops/specs/llm-khoan-docx-r21.md`, blob `0e10b0888f524f1396e378c81539221a8e5e5e7d`. Băm SHA-256 checkout `37fa1d510ffc34ea383328dd1da6b39b1984e8f4b2ed60489b22071b2021ef45` khớp lease r21/g1 (blob `e9d140dd9289b69b20188f3a4dd7007aa78336a2`). Đã đối chiếu **21/21** cặp bia mộ hai chiều #1514 r9 ↔ #1525 r1 ↔ … ↔ r21, **22/22** băm đặc tả trong chuỗi, cùng branch/base/generation. Lease ghi `sensitive`, hạn 18:15 UTC 26-11-2026, lượt **21/21** và dẫn quyết định đứng của chủ kho. [Spec r21](../ops/specs/llm-khoan-docx-r21.md) · [Lease r21](../ops/leases/llm-khoan-docx-r21-g1-claude.yaml)
- Write set 116 đường dẫn, SHA-256 `85a19685d69c6e0f817ed762006c0554a11216a5094d690ed476158ae87d3ff1` sau sắp xếp và kết LF. Diff bản vá **8/8** và diff #1525 **112/112** đường dẫn nằm trong write set sau khi bỏ hồ sơ #1514 theo prompt. Diff toàn PR có 160 đường dẫn, gồm 48 đường dẫn kế thừa #1514 ngoài write set r21.
- Reviewer `openai_codex / codex_cli / machine`, launcher 1.6.2, run `e9929547d0384961a686e9142c71fd8d`, Codex CLI 0.172.0. SHA-256 của prompt `fde93805d620d3ce9cdb2e3e0f489967c16f2bfa7ab65a78d087ed61c581f6a4` khớp metadata của run. Lease khai Executor `claude / claude_code / machine/local` (provider `anthropic_claude`) và phiên giao việc `session_015GtxrZQYT3Vt8PJdXrjEKg`. Môi trường Linux x86_64, Python 3.13.18, Git 2.43.0, `core.abbrev=7`, shallow, sandbox `workspace-write` với metadata Git chỉ đọc. [Protocol §8.1–8.3](../docs/PROTOCOL_DA_PHIEN.md#L770)

| Mục | Trạng thái | Bằng chứng |
| --- | --- | --- |
| W1 · V1 · §2.22–§2.23 · markup qua số hiệu | **CHƯA VÁ trong bộ đọc dùng chung. Giới hạn đã duyệt** | `--markup-strict` vẫn đi qua `tl extract`. Ca giả lập rc 3 đo chốt dừng trước model. Gạch qua style trong producer nằm trong phạm vi giới hạn r21, nên W1 đã ra khỏi danh sách finding mở. [Spec](../ops/specs/llm-khoan-docx-r21.md#L280) · [Chốt](../scripts/tl_core/llm_route.py#L1508) · [Ca V1](../scripts/tl_core/llm_route_test.py#L675) |
| W2 · §2.23 · khoảng trắng khi lọc | **VÁ MỘT PHẦN** | Hai ca dương và mutant tương ứng khóa khoảng trắng văn tự trong run gạch và trong `w:del`. Nhánh `del/moveFrom` vẫn bỏ cấu trúc phân cách trong khi chính sách r222 giữ. X1 phân tích phần còn mở ở `--tep .docx`. Mất tab/ngắt của đường số hiệu là giới hạn đã duyệt. [Ca W2](../scripts/tl_core/llm_route_test.py#L1433) · [Nhánh đọc](../scripts/tl_core/llm_route.py#L1024) |
| W3 · §2.23 · strict với nguồn sạch/cache và CAP | **ĐÃ VÁ THẬT ở hướng dẫn CAP. CHƯA VÁ trong producer, giới hạn đã duyệt** | CAP chỉ sang DOCX một Điều. Spec khai chặn cả export sạch và consolidated, hướng dẫn công khai nêu chặn export sạch. Hai hành vi strict của bộ đọc dùng chung nằm trong ngoại lệ r21. [CAP](../scripts/tl_core/llm_route.py#L1528) · [Giới hạn](../ops/specs/llm-khoan-docx-r21.md#L280) |
| W4 · V4 · §2.22–§2.23 · nhãn điểm thô | **ĐÃ VÁ THẬT với nhãn đã báo. Lớp còn mở** | Bắt chữ hoa, chữ lặp và dạng chấm/ngoặc, đối chứng chữ viết tắt và e-mail qua. Hai mutant gỡ miền hoa/lặp đều chết. Miền nhãn sinh từ cấu trúc vẫn rộng hơn quy tắc nhận điểm ở đầu dòng thô, xem X3. [Regex](../scripts/tl_core/llm_route.py#L490) · [Ca đối chứng](../scripts/tl_core/llm_route_test.py#L686) |
| W5 · §2.23 · cấp lặp | **ĐÃ VÁ THẬT với hai dạng đã báo. Lớp còn mở** | Cấp bằng nhau sau chuyển về số, kể cả `lvlOverride`, đều đặt cờ lỗi trên danh sách đang dùng. Hai mutant và ca dương danh sách lỗi không dùng đều đạt. Các trường quyết định số đọc bằng `.find()` vẫn có thể âm thầm chọn một giá trị trong khai báo mâu thuẫn, xem X2. [Đọc cấp](../scripts/tl_core/llm_route.py#L738) · [Override](../scripts/tl_core/llm_route.py#L784) · [Ca chặn](../scripts/tl_core/llm_route_test.py#L1618) |
| §1–§2.3 · bất biến, K1 từ #1514 | **ĐÃ VÁ THẬT với hai nhánh K1** | Sau số khoản, dòng điểm nhận diện được trả `None`, tiếp dòng mở bằng “là” rơi vào nhánh từ chối dòng không số. Ở nguồn mất số, tiếp dòng mở “là” thiếu vế thuật ngữ nên phép so chặn. Số, vị trí, số lượng và hai vế của mỗi khoản đều được so. `ca_wp1514` qua fixture Điều 3 và ba đầu ra lưu sẵn 8/8. Đối chiếu base→head cho thấy cờ CLI và các hàm gọi model giữ nguyên. Cả hai tuyến luôn có `can_nguoi_duyet: true` và nhãn đúng nguồn phân đoạn. [Tách thô](../scripts/tl_core/llm_route.py#L1244) · [So](../scripts/tl_core/llm_route.py#L1403) · [Đầu ra](../scripts/tl_core/ops_misc.py#L3130) |
| §2.1–§2.9 · A1/A6, B1/B2, C1/C2, D1/D4/D6, E1/E3/E4, F1/F2 | **HẾT ĐỐI TƯỢNG** với thuật toán cắt cuối Điều, đếm trong bảng, điểm gõ tay và `KhongCauTruc`. **ĐÃ VÁ THẬT** với các chốt hiện hành | Đoạn có nội dung đầu tiên phải là tiêu đề đích đúng hình dạng, vùng kéo đến hết tệp. Bảng/khối lạ, đoạn mơ hồ, ngắt mềm, đoạn đánh số rỗng và đoạn không số sau khoản đầu đều bị chặn. DOCX không có số tự động ném `ValueError`, CLI trả rc 2. Điểm phải là cấp con của cùng danh sách. [Vùng](../scripts/tl_core/llm_route.py#L1134) · [Chọn mẫu CLI](../scripts/tl_core/ops_misc.py#L3027) |
| §2.4–§2.15, §2.22 · A2/A5, B2/B5, C2, D2, E6, F3–F5, G1/G3, H4, J1/J3, K3, L4, M2, V2 | **ĐÃ VÁ THẬT với các biểu hiện đã khóa** | `start` vắng lấy 0, override theo cấp, mỗi `numId` có bộ đếm riêng; tăng cấp cha xóa cấp con, nhảy cấp bị chặn. Chuẩn hóa ID theo chuỗi ASCII, chặn ID/cấp không hợp lệ khi dùng, số trên 999, style ảnh hưởng cấp, số kế thừa từ mặc định đoạn. Một danh sách, số khoản liên tục từ 1, định dạng cấp khoản thập phân đúng placeholder. Ca có `startOverride` khác `start` và reset cấp con đều qua. X2 ghi phần còn mở. [Định nghĩa số](../scripts/tl_core/llm_route.py#L715) · [Đếm](../scripts/tl_core/llm_route.py#L1117) · [Ca dương](../scripts/tl_core/llm_route_test.py#L1323) |
| §2.4–§2.9 · A3/A6, C3, D6, F2 · câu dẫn, từ nối và dấu phân cách | **ĐÃ VÁ THẬT** với các tình huống đã báo | Tối đa một câu dẫn chuẩn nguyên đoạn trước khoản đầu, hoặc vắng. Chốt dấu phân cách nhìn nguyên thân mỗi đoạn DOCX. Từ nối chỉ dò ở đoạn mở khoản. Khi chuẩn nguồn đúng, đầu ra tự bỏ, gộp, cắt, tráo khoản hoặc tách điểm riêng sẽ lệch, kể cả model giữ nguyên thứ tự chữ. [Câu dẫn](../scripts/tl_core/llm_route.py#L1224) · [So theo vị trí](../scripts/tl_core/llm_route.py#L1414) |
| §2.4–§2.16, §2.19 · A4, B3/B4/B6, C4/C5, D3/D5, E2/E5, F6, G2/G4, H2/H5, J2/J5, K1, L1/L5, M2, N3, S3 | **ĐÃ VÁ THẬT với các biểu hiện đã khóa** | Part chính/numbering/styles định vị qua URI Transitional và quan hệ đúng part. Đọc bytes XML gốc, chặn `mc:`, sửa dấu đoạn, move thiếu ID/mất cân và toggle nhiều tầng chưa giải được. Lọc chữ gạch/xóa/chuyển đi, giữ chữ chèn/chuyển đến. Các ca dương khóa content control, `w:ptab`, `w:noBreakHyphen`, mốc perm, encoding XML, chữ đã bỏ sau ngắt trang. X1 ghi chỗ mất phân cách còn lại. [Quan hệ](../scripts/tl_core/llm_route.py#L674) · [Đọc run](../scripts/tl_core/llm_route.py#L939) · [Chốt markup](../scripts/tl_core/llm_route.py#L1084) |
| §2.10–§2.21 · G6, H1, K2, L2/L3, M1, N1/N2, Q1/Q2, R1–R3, S1/S2, T1/T2, U1/U2 | **ĐÃ VÁ THẬT trong miền r21**. Biến đổi ở producer là giới hạn đã duyệt | Chốt trên chữ còn hiệu lực trước chuẩn hóa khoảng trắng, chặn tiền tố Điều trong thân và tiêu đề Chương/Mục/Phần theo mẫu. Chữ số chỉ còn ASCII. Chặn số gõ tay dạng ngoặc kín dính chữ số. TXT giải mã UTF-8, kiểm trước tách dòng, bỏ đúng một BOM trong mỗi phép đọc. Sanitize/cache và cắt Điều ở `tl extract` thuộc U2/V3. [Ký tự](../scripts/tl_core/llm_route.py#L553) · [Tiền tố](../scripts/tl_core/llm_route.py#L1156) · [TXT CLI](../scripts/tl_core/ops_misc.py#L3057) |
| §3 · A7/A8, B7/B8, C6/C7, D4, E5, F5, G5, H3, J4, K4, L6, Q2 | **ĐÃ VÁ THẬT với các ca và chốt hiện hành đã đối chiếu** | Bảng mutant có neo riêng cho dấu gạch điểm gõ tay, ID trừu tượng, quan hệ của part đã đổi tên, `startOverride`, reset cấp con, đọc XML gốc và sáu thay đổi r21. Ca CLI có mock cho rc 0/5/2. Mô tả §3 áp dụng hợp đồng một Điều. [Mutant r21](../scripts/tl_core/llm_route_test.py#L1819) · [CLI selftest](../scripts/tl_selftest.py#L32229) |

## Findings

### X1 [P1] DOCX làm dính từ khi run xóa hoặc chuyển đi chỉ chứa tab/ngắt — `scripts/tl_core/llm_route.py:1024`

**Kịch bản.** Một dấu phân cách duy nhất giữa hai từ còn hiệu lực nằm trong một run đã xóa hoặc chuyển đi. Word có thể lưu dấu ấy thành phần tử tab hay ngắt, thay vì một ký tự trắng trong phần tử chữ. Sau lọc, hai từ dính liền và trở thành chuẩn đưa cho model. Nếu vị trí ở giữa định nghĩa, từ nối và số khoản vẫn đúng, nên đầu ra chép theo chuẩn đã dính có thể qua kiểm và được ghi `--out`.

**Căn cứ và hạng.** §2.23 W2 nhận chính sách r222. `chunk_payload` của r222 chuyển `w:tab`/`w:br`/`w:cr` thành khoảng trắng trước khi quyết có giữ mẩu rỗng chữ hay không. Trình đọc DOCX chỉ gom `w:t` và `w:delText` trong `w:del`/`w:moveFrom`, dù trong run thường nó đã biết chuyển các phần tử phân cách. Lưới phụ r222 còn giữ `w:delText` lạc chỉ có khoảng trắng, còn nhánh run hiện bỏ thẳng phần tử đó. Phần r21 đã đo chỉ dùng khoảng trắng chứa trong phần tử chữ. P1 vì chuẩn của đường cấu trúc có thể xác nhận chữ đã biến đổi. [Chính sách r222](../scripts/docx_markup.py#L93) · [Lưới phụ](../scripts/docx_markup.py#L236) · [Ca W2](../scripts/tl_core/llm_route_test.py#L1433) · [Đối chiếu](../scripts/tl_core/llm_route.py#L1425)

**Đề xuất.** Dùng cùng nghĩa phân cách khi đọc ruột run gạch, `del` và `moveFrom`. Giữ trường hợp thực sự chỉ có khoảng trắng, tiếp tục bỏ chữ đã loại và chặn khi phần tử còn lại có thể đổi ranh giới nhưng chưa giải được. Phép đóng lớp cần cả khoảng trắng văn tự và phần tử phân cách, cùng đối chứng có chữ bị xóa và mẩu thật sự rỗng.

### X2 [P1] Một danh sách có thể được nhận dù một cấp khai nhiều giá trị bắt đầu — `scripts/tl_core/llm_route.py:750`

**Kịch bản.** Danh sách được dùng có một cấp khoản duy nhất, song trong chính cấp đó có hai giá trị bắt đầu khác nhau, giá trị đầu là 1. Bản vá W5 nhìn thấy đúng một `w:lvl` và không đặt cờ lỗi. Bộ đọc chọn `w:start` đầu tiên, tạo chuỗi 1 trở đi và chấp nhận cấu trúc. Vấn đề cùng lớp có ở `numFmt`, `lvlText` và liên kết `w:abstractNumId` trong từng `w:num`: `.find()` chọn phần tử đầu khi có nhiều khai báo. Cửa `startOverride` kiểm đúng một phần tử con nên chặn được dạng tương ứng trong override.

**Căn cứ và hạng.** Mỗi trường trên quyết định cách dựng chuẩn số. Chỉ cần chuỗi theo cách đọc đầu tiên đúng 1…N là chốt cuối qua, dù khai báo dùng để dựng nó mâu thuẫn. Đây là lỗi fail-closed P1 cùng lớp W5 đối với đường khẳng định ranh giới từ cấu trúc. Suy luận này dựa trên mã chọn giá trị và không cần giả định Word sẽ chọn phần tử thứ hai. Cách Word sửa hoặc từ chối gói mâu thuẫn chưa được đo. [Chọn giá trị](../scripts/tl_core/llm_route.py#L750) · [Liên kết danh sách](../scripts/tl_core/llm_route.py#L770) · [Chốt override](../scripts/tl_core/llm_route.py#L794) · [Kiểm số khoản](../scripts/tl_core/llm_route.py#L1213)

**Đề xuất.** Kiểm số lượng phần tử trước khi diễn giải các trường đơn trị có ảnh hưởng đến ID, cấp, số bắt đầu và nhãn. Áp dụng cùng nguyên tắc cho `numPr` của đoạn. Dùng dấu lỗi của A5 đối với định nghĩa danh sách và chỉ chặn khi Điều dùng định nghĩa ấy. Đối chứng cần giữ trường hợp vắng `start` hợp lệ, chỉ một `startOverride` và định nghĩa lỗi không dùng.

### X3 [P2] Đường thô vẫn có thể nâng điểm thành khoản khi nhãn chữ dùng dấu gạch — `scripts/tl_core/llm_route.py:496`

**Kịch bản.** Nguồn thô đã mất số khoản nhưng còn một dòng điểm có nhãn chữ kèm gạch ở sau chữ. Dòng mở khoản phía trước và dòng điểm đều có đủ hình dạng câu định nghĩa và dấu chấm cuối. Đây là nhãn mà bộ đọc DOCX có thể dựng hợp lệ từ placeholder chữ và dấu gạch, kể cả khi có khoảng trắng giữa chúng. Vì dấu gạch đứng sau chữ, `_RE_DIEM` không nhận đó là điểm. Nhánh nguồn mất số xem nó là một khoản độc lập.

**Căn cứ và hạng.** Lớp `ranh-gioi-khoan` còn một hình dạng có nhãn phân biệt được. Nhãn còn nguyên, ký tự nằm trong danh sách cho phép và dữ liệu có thể đi thẳng qua `--tep` TXT. Quy tắc số nội dòng và ngoặc không loại hình dạng này. P2 cùng lý do với W4/K1, vì phép so thô khẳng định phần chép theo phân đoạn của bộ quét và luôn yêu cầu người dùng duyệt ranh giới. Hai biểu hiện K1 cũ đã đóng. [Miền nhãn cấu trúc](../scripts/tl_core/llm_route.py#L886) · [Nhận dòng thô](../scripts/tl_core/llm_route.py#L1272) · [Phạm vi kiểm](../scripts/tl_core/llm_route.py#L1240)

**Đề xuất.** Chốt ranh giới thô theo miền nhãn điểm mà lệnh công bố hỗ trợ. Bắt thêm dạng nhãn chữ kèm dấu gạch ở đầu dòng mà vẫn giữ đối chứng cho chữ viết tắt và từ ghép có gạch nối. Trường hợp mất luôn nhãn và không còn tín hiệu phân biệt vẫn thuộc duyệt ranh giới của người dùng.

| Lớp | Hạng cao nhất còn mở | Lịch sử và điều kiện đóng |
| --- | --- | --- |
| `docx-markup-du-thao` | Hết finding trong phạm vi r21 | V1/W1/W3. W1 và phần strict của W3 còn hành vi trong producer dùng chung, hiện là giới hạn theo quyết định chủ kho. Hướng dẫn CAP đã sửa. Không tính việc khai giới hạn là vá runtime. |
| `docx-khoang-trang-sau-loc` | P1 · X1 | Nối W2/r222. Giữ phân cách trên cả ba nhánh loại nội dung khi ruột chỉ có khoảng trắng, với các dạng biểu diễn khác nhau. |
| `docx-so-hien-thi` | P1 · X2 | Nối A2/B2/G1/J1/V2/W5. Hai dạng cấp trùng đã đóng, còn đọc trường đơn trị mâu thuẫn. Phép kiểm phải chứng minh danh sách đang dùng dừng trước khi đếm, danh sách lỗi ngoài Điều vẫn qua. |
| `ranh-gioi-khoan` | P2 · X3 | Nối K1/V4/W4. Điểm và tiếp dòng K1 đã đóng. Kiểm bao phủ các dạng nhãn điểm quan sát được ở tuyến thô, đồng thời giữ đối chứng từng khoản một dòng. |

Còn **3 lớp, 3 finding** gồm 0 P0, 2 P1, 1 P2, 0 P3. Trong 4 lớp mở ở lượt 20, 3 còn biểu hiện. Lớp markup của producer ra khỏi phạm vi theo r21. Điều kiện severity M1 của ADR-0060 chưa đạt. [Verdict lượt 20](../ops/acceptance/llm-khoan-docx/r1/review-20-codex/VERDICT.md) · [Protocol §8.3](../docs/PROTOCOL_DA_PHIEN.md#L812) · [ADR-0060 M1–M2](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32)

## Kết quả test và đột biến

Các lệnh dưới đây chạy trên clone cục bộ detached trong `/tmp/wp1525-r21-codex.jAKVrI/`, cùng `core.abbrev=7`, không tạo bytecode. Mỗi log và mã thoát lưu riêng. Head và base có đúng OID/tree đã ghi ở trên. Dữ liệu tạm và log của test nằm ngoài checkout review.

| Lệnh | Trạng thái | Mã thoát và bằng chứng dương |
| --- | --- | --- |
| `python scripts/tl_core/llm_route_test.py` | `passed` | rc 0, **63/63** ca, **217/217** mutant bị giết, gồm **120/120** tên có tiền tố `wp1525_` trong bảng. `route.log`. |
| `python scripts/tl.py --deterministic workflow-audit --strict --json` | `passed` | rc 0, `ok=true`, 194 lệnh, 26 card, 11 nhóm, 60 task, 0 lỗi, 0 cảnh báo. `workflow.log`. |
| `python scripts/tl.py --deterministic golden-test --json` | `passed` | rc 0, **20/20** ca và 20/20 bản chiếu ổn định. Byte thô 19/20 ổn định. Ca `hygiene_sweep_fixture` có biến động đã khai và `diff={}` sau chiếu. `golden.log`. |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | `passed` | rc 0, **187/187** tệp, danh sách sai/thiếu/thừa rỗng. Hai package hash khớp `c23afb4023ae03b7a88d941dddc424840c68d433349e164a825d6b0d114d2f78`. `release.log`. |
| `python ops/lease_publish.py check --root . ops/leases/llm-khoan-docx-r21-g1-claude.yaml` | `passed` cục bộ | rc 0, lease #1525 neo đúng base, hạn 18:15 UTC. Hai lớp GitHub của lệnh ghi `skipped`. `lease.log`. |
| `python scripts/tl.py --deterministic determinism-audit --strict --json` | `passed` | rc 0, **15/15** kiểm tra `ok=true`. `determinism.log`. |
| `python scripts/tl.py --deterministic doc-claims-check --strict --json` | `failed` trên hai SHA | rc 2 cả head/base, 131 tệp, 407 advisory, cùng 4 cờ cứng `SHA_NOT_A_COMMIT` trong clone shallow. So mảng `flags` trả rc 0. `claims.log` / `claims-base.log`. Gate strict còn đỏ. |
| Contract ghim/probe Ruff qua `loi_ruff_ci()` của `.claude/dev/ci_dang_ky_test.py` | `passed` | rc 0, `RUFF_CONTRACT 3 []`. `ruff-contract.log`. |
| `ruff check --no-cache --select F scripts/tl.py --output-format concise` | `failed` về lint tuyệt đối, **đạt delta** | Ruff 0.16.9, rc 1 cả hai mốc, **12 F821** mỗi mốc, đầu ra trùng byte. Đo thêm cùng bộ quy tắc trên năm tệp Python sửa trong PR và `tl.py`: rc 1, 4.816 báo cáo ở mỗi mốc (khác số dòng ở ba vị trí đã có trong `ops_misc.py`). `ruff-tl-*.log` / `ruff-lint-*.log`. |
| `python scripts/tl.py --selftest` · head, lần đầu | `failed` | rc 1, **1773/1790**, transport **12/12**. Ca DOCX mới `r1525_llm_khai_niem_tep_docx_cau_truc` đạt. `selftest.log`. |
| `python scripts/tl.py --selftest` · base, lần đầu | `failed` | rc 1, **1772/1789**, transport **12/12**. `selftest-base.log`. |
| `git diff --check` · bản vá r21 và diff packet #1525 | `passed` | rc 0 với hai dải `8689b60..HEAD` và `fcb12b3..HEAD` sau loại hồ sơ #1514 theo prompt. |
| `git diff --check` · toàn PR và phần kế thừa #1514 | `failed` | rc 2 trên cả `64b7f2c..HEAD` và `64b7f2c..fcb12b3`. Cùng ba khoảng trắng cuối dòng trong verdict #1514 lượt 8. [Hồ sơ kế thừa](../ops/acceptance/llm-ranh-gioi-khoan/r1/review-8-codex/VERDICT.md#L3) |

Harness chạy đột biến trên bản sao tạm của module. Nó yêu cầu neo đúng một lần, từ chối lỗi import và lỗi không liên quan, chỉ tính khi đúng ca đích ném `TinHieuChotCa`. Sáu mutant mới r21 đều bị bắt. [Bảng mutant](../scripts/tl_core/llm_route_test.py#L1819) · [Harness](../scripts/tl_core/llm_route_test.py#L2086)

| Mutant r21 | Điều được ca đích khóa |
| --- | --- |
| `wp1525_diem_bo_chu_hoa`, `wp1525_diem_bo_chu_lap` | Nhãn chữ hoa có ngoặc và chữ lặp có chấm vẫn bị chặn trong nguồn mất số. |
| `wp1525_gach_bo_ca_khoang_trang`, `wp1525_del_bo_ca_khoang_trang` | Khoảng trắng văn tự trong run gạch hoặc `w:del` còn sau lọc. |
| `wp1525_lvl_trung_ghi_de`, `wp1525_override_trung_ghi_de` | Trùng cấp và trùng override trên danh sách đang dùng phải bị chặn. |

Lượt selftest đầu có cùng **17** ID đỏ. So trạng thái tất cả ID chung sau khi loại đúng ca DOCX mới ở head, `diff -u` trả rc 0. Có 14 ca đã báo với `/tmp/.git` rỗng (8 `r973_bootstrap_*`, 5 `wp433_*`, và `wp727_tl_gws_refresh`). Hai ca L2 `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` và `r268_l2_trichotomy_theo_trang_thai_object` cùng đỏ trên hai mốc trong môi trường Git có ký commit mặc định. Ca `wp1099_nlm_nap_lai` cùng báo không đọc được base của `references/RASOAT_HOSO_LOOP.md`. Các ca r222, strict extract r186 và r380 đầu vào llm đều qua ở hai mốc.

Đối chứng dùng `TMPDIR` riêng và tắt ký commit chỉ cho tiến trình `python scripts/tl.py --selftest` (`GIT_CONFIG_COUNT=1`, `GIT_CONFIG_KEY_0=commit.gpgsign`, `GIT_CONFIG_VALUE_0=false`). Hai ca L2 chuyển sang đạt ở cả hai mốc. Lượt này vẫn `failed` rc 1 ở cả head **1775/1790** và base **1774/1789**, cùng 15 ID đỏ. So trạng thái các ID chung trả rc 0. `selftest-retry.log` / `selftest-base-retry.log`.

Lượt cuối chạy cùng lệnh và môi trường đối chứng trên hai clone bổ sung kho object chỉ đọc từ checkout được giao. Ca `wp1099_nlm_nap_lai` chuyển sang đạt ở hai mốc sau khi đọc được commit `358451e80b573d148807717bece3fd973915fbad`. Selftest head **1776/1790**, base **1775/1789**, transport **12/12** mỗi mốc, rc 1 cả hai (`failed`). Cùng 14 ca đỏ thuộc các nhóm `/tmp/.git` rỗng. So tập ID đỏ và toàn bộ **1.801** dòng trạng thái ID chung, gồm transport, trả rc 0. Head có thêm ca DOCX r1525 đạt. Gate N/N vẫn đỏ, delta ca đỏ bằng 0. Log `selftest-full-local.log` có SHA-256 `c04d00ce08577105561f5e35fd361e978851e0fb5e943fe7f834a3d2641fd2a6`, log `selftest-base-full-local.log` có SHA-256 `0ec1095106caeade4ce4c7d3476f47557a8b026d42cddb3a9080426ecaf099a6`.

Chạy lại `doc-claims-check` với kho object cục bộ được giao làm alternate chỉ đọc cho hai clone mới. Ba cờ của phép đo đầu đổi sang advisory khi đọc được object. Gate vẫn `failed` rc 2 ở cả head và base, với 410 advisory và cùng một cờ cứng tại `docs/PROTOCOL_DA_PHIEN.md:1680`. Object `9941d8af52aeede1c78ea4e232fbe9a8d5272033` cũng vắng trong checkout được giao. So mảng `flags` của hai mốc trả rc 0. `claims-full-local.log` / `claims-base-full-local.log`.

## Không đo được

- X1–X3 dựa trên đường thực thi đọc từ mã. Chưa có phép đo đầu-cuối tương ứng, mẫu export thật hoặc phép đo cách Word xử lý khai báo số mâu thuẫn. Test sẵn có khóa các phản chứng và đối chứng liệt kê ở trên.
- Với §2.5, ca sẵn có chứng minh các marker bookmark/comment/perm, content control, `w:ptab` và ngắt trang cuối đoạn được nhận trong các hình dạng đã hỗ trợ. Các dạng bảng, Strict, trường, ký hiệu, hình, chú thích và markup compatibility thuộc giới hạn công bố. Chưa có đủ bằng chứng offline để xác nhận một phần tử thường gặp trong export thật của Word/Google Docs bị chặn oan ngoài giới hạn ấy. Tần suất và khác biệt theo phiên bản ứng dụng cũng chưa đo được. [Danh sách hiện hành](../scripts/tl_core/llm_route.py#L602) · [Hướng dẫn DOCX](../docs/GOI_AGENT_DA_NEN.md#L390)
- `skipped` với hai lớp kiểm Issue/PR và comment GitHub của lệnh lease. `not_run` với GitHub, CI từ xa, lời gọi model thật, Windows bản địa và bare lint đúng bản pin CI 0.15.15. Windows là `required` theo ADR-0060 M3 vì diff PR sửa dòng Python có `encoding=`. Bằng chứng bắt buộc ở những bề mặt này còn thiếu. [ADR-0060 M3](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L43) · [Dòng đổi encoding](../scripts/tl_core/ops_misc.py#L3061)
- Model và effort phục vụ ghi `KHONG_DO_DUOC` theo metadata run còn mở. Tương tự, trạng thái terminal, rc con và hash đầu ra ổn định do launcher ghi sau khi run kết thúc. Repo nguồn Executor và head từ xa nằm ngoài phạm vi quan sát của lượt offline.

## Đọc lại checkout và kết luận

`git rev-parse HEAD 'HEAD^{tree}'` khớp ở đầu và cuối lượt. `git diff --quiet` và `git diff --cached --quiet` đều rc 0 ở checkout review và hai clone đối chứng cuối. Checkout review chỉ có `.review/VERDICT.md` mới và thư mục `.codex/` đã bị ignore từ lúc preflight. Các trạng thái này mô tả hai lần quan sát. [Protocol §8.2](../docs/PROTOCOL_DA_PHIEN.md#L797)

Lượt 21 dùng hết số lượt ghi trong lease r21. Hai P1 và một P2 còn mở. Điều kiện merge theo ADR-0060 M1, áp mặc định qua ADR-0062, chưa đạt. Cổng selftest N/N, doc-claims strict và bằng chứng Windows/CI exact head cũng chưa đủ. [ADR-0060 M1](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32) · [ADR-0062 N1](../docs/adr/0062-adr-0060-mac-dinh-va-dong-bang-adr-0054.md#L13)

P2_mo: 1

VERDICT: REQUEST_CHANGES
