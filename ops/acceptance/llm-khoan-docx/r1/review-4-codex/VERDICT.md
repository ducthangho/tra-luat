# Verdict packet #1525 r4 lượt 4 — Codex

reviewed_sha: fa3a8e2047ccbdb4c20eb11f117732658a653b92
reviewed_tree: c88b49297da37d58be06d5dfc856491a99d07956
base_sha: 64b7f2c14776d5d0e1d34a6be4725490956f5bec

VERDICT: REQUEST_CHANGES

Kết luận trên exact head có 0 P0, 3 P1, 3 P2 và 0 P3 mở. K1 đã đóng trên đường thô. Điều kiện merge ADR-0060 M1 chưa đạt.

## Preflight

- Checkout detached khớp exact head/tree. Merge base khớp SHA được giao, origin cấu hình cho `ducthangho/tra-luat`, `core.abbrev=7`. Index và tracked worktree sạch ở đầu lượt.
- Packet #1525, revision 4, generation 1, `sensitive`. SHA-256 đặc tả khớp lease `114ed997845edaf1cf9320c654a3fa28495e78229ab4a4a7c0d569ebf7ac06f7`. Lease còn hạn đến `2026-11-25T17:48:00Z` khi kiểm. Lượt 4/5.
- So tên tệp từ `fcb12b3` đến head, sau khi loại hồ sơ nghiệm thu #1514 đúng phạm vi prompt, không có tệp ngoài write set. Bia mộ nối hai chiều #1514 r9 ↔ #1525 r1 ↔ r2 ↔ r3 ↔ r4.
- Assignment nhận dạng Executor `claude` / `claude_code` / `machine/local`. Reviewer `openai_codex` / `codex_cli` / `machine`, run `4484c05726fb4adfac819f04e9ac2648`, sandbox `workspace-write` với `.git` chỉ đọc. Linux x86_64, Python 3.13.18, Git 2.43.0.

## Đối chiếu lượt 3 và đặc tả r4

Nguồn đối chiếu là lượt 1 `3d247516aaeb0ad3d836a2dc51dda13052fdbe47`, lượt 2 `38c481f792b3f44d7500e93249153af63c0165db`, lượt 3 `b0f3cb9ea1cca141f12eb462ced60f949d1ed0a4` và lượt 10 #1514 `fcb12b3873c3bec2c339029136243ed2c804ce05`. [A1–A8](../ops/acceptance/llm-khoan-docx/r1/review-1-codex/VERDICT.md) · [B1–B8](../ops/acceptance/llm-khoan-docx/r1/review-2-codex/VERDICT.md) · [C1–C7](../ops/acceptance/llm-khoan-docx/r1/review-3-codex/VERDICT.md) · [K1](../ops/acceptance/llm-ranh-gioi-khoan/r1/review-10-codex/VERDICT.md#L35)

| Mục | Trạng thái | Bằng chứng |
| --- | --- | --- |
| C1 · A1 · B1 | VÁ MỘT PHẦN | Tiêu đề đích có ngắt mềm bị chặn dù chữ khớp mẫu. Cờ `con_bo`, `la`, `ngat` ở điểm cắt có ba chốt riêng. Kiểm Điều kế tiếp loại được Điều khác số, song một đoạn thân giống Điều kế hoặc Chương/Mục/Phần vẫn cắt sớm. D1. [Mã](../scripts/tl_core/llm_route.py#L902) · [Ca đích](../scripts/tl_core/llm_route_test.py#L1359) |
| C2 · A2 · B2 | C2 ĐÃ VÁ THẬT ở hai biểu hiện đã báo, A2 còn D2 | Duyệt wrapper đúng thứ tự ở cấp hàng/ô, giữ đếm bảng lồng một lần. `_chu_cai` lặp cùng chữ sau Z, ca thử khóa cả nhãn thường và hoa. `start=0`, override 5→1, reset cấp con và hai `numId` có ca sẵn. Phạm vi đếm còn một kiểu reset ngoài các chốt hiện tại. D2. [Mã](../scripts/tl_core/llm_route.py#L693) · [Ca đích](../scripts/tl_core/llm_route_test.py#L1271) |
| C3 · A3 | C3 VÁ MỘT PHẦN, A3 ĐÃ VÁ THẬT | Ca dấu trích dẫn ngoài danh sách trong đầu khoản giết đột biến bỏ chốt. Từ nối tiếp tục lấy riêng từ đoạn mở, kể cả khi điểm dùng nhãn chữ hoa. Quyết định bỏ dấu điểm của C3 còn dựa vào tiền tố thay cho vai trò đoạn. D6. [Mã](../scripts/tl_core/llm_route.py#L1005) · [So nguyên văn](../scripts/tl_core/llm_route.py#L1195) · [Ca đích](../scripts/tl_core/llm_route_test.py#L1366) |
| C4 · A4 · B3 | C4 và B3 ĐÃ VÁ THẬT ở chuỗi style, A4 còn D3 | Cờ đơn và kép giữ riêng. `false` ở style con giữ khả năng gạch của cha, tắt trực tiếp ở run có ca dương. `docDefaults`, namespace khác và dấu đoạn trên XML gốc có ca âm. Phép lọc markup trước khi đọc cấu trúc còn có thể làm mất chữ hoặc ranh giới. D3. [Mã](../scripts/tl_core/llm_route.py#L679) · [Ca đích](../scripts/tl_core/llm_route_test.py#L1313) |
| C5 · B4 · B6 | ĐÃ VÁ THẬT đối với các biểu hiện đã báo | `w:sdt` nội dòng đi vào `w:sdtContent`, giữ chữ trong ca dương. `noBreakHyphen` sinh dấu gạch nối. Phần tử hiển thị ngoài miền đặt `la`, metadata wrapper được bỏ qua. DOCX Strict bị chặn ở cấp namespace. D5. [Mã](../scripts/tl_core/llm_route.py#L791) · [Ca đích](../scripts/tl_core/llm_route_test.py#L1308) |
| C6 · A7 · B7 | VÁ MỘT PHẦN | Các biểu hiện C6 lượt 3 có đối chứng riêng, gồm tách `la`/ngắt/markup ở ranh giới, tiêu đề đích khớp mẫu nhưng có ngắt, `numStyleLink` và `styleLink`. Hai đột biến độc lập còn sống ở tiêu đề đích và khối lạ của bảng. D4. [Ca âm](../scripts/tl_core/llm_route_test.py#L1361) · [Đột biến](../scripts/tl_core/llm_route_test.py#L1507) |
| C7 · B8 · A8 | ĐÃ VÁ THẬT | Hướng dẫn liệt kê `%N.` và `%N)`, phân biệt numbering chỉ qua style trong/ngoài Điều, và giữ quy tắc một dòng cho đường thô. [Hướng dẫn](../docs/GOI_AGENT_DA_NEN.md#L373) |
| A5 · A6 · B5 | ĐÃ VÁ THẬT ở các ca đã báo | Danh sách La Mã độc lập có override không hỗ trợ ở ngoài Điều vẫn để Điều đích đạt. Điểm gõ tay dính thân được giữ. Đầu thân là số thập phân vẫn đọc được. [Các ca](../scripts/tl_core/llm_route_test.py#L1263) |
| §1 | Đạt với dữ liệu đã đo | `goi`, `duong_api`, `duong_sub`, `_chay_co_moc` và tập cờ CLI giữ nguyên từ base. Handler luôn mang `can_nguoi_duyet: true` và chọn `pham_vi_kiem` theo ranh giới dùng để so. Ca hồi quy Điều 3 và ba kết quả lưu đạt 8/8 mỗi bản. [Handler](../scripts/tl_core/ops_misc.py#L3127) · [Ca 8/8](../scripts/tl_core/llm_route_test.py#L1034) |
| §2.1, §2.4–§2.6 | Còn D1–D6 | Reader thư viện chuẩn đọc thành phần ZIP qua reader bounded khi nạp được. Câu dẫn cấu trúc vắng hoặc đúng một đoạn khớp toàn câu chuẩn. Nhiều `numId` trong vùng và cấp con trước khoản đầu bị chặn. Đoạn không số sau khoản chỉ được nối khi khớp dấu điểm gõ tay đã khai. [Reader](../scripts/tl_core/llm_route.py#L552) · [Cấp khoản và điểm](../scripts/tl_core/llm_route.py#L958) |
| §2.2 | Đạt định tuyến, dữ liệu trước fallback còn D1 và D3 | ZIP magic chọn DOCX, cần `--dieu`, cấm kèm số hiệu. Chỉ `KhongCauTruc` lùi thô, sau các chốt bảng/khối lạ, ngắt mềm, markup còn sót, numbering rỗng và numbering chỉ qua style trong vùng đã chọn. `--out` chỉ ghi khi phép so hết lệch. [Handler](../scripts/tl_core/ops_misc.py#L3027) · [Các chốt trước fallback](../scripts/tl_core/llm_route.py#L938) |
| §2.3 · K1 | ĐÃ VÁ THẬT | `_RE_DIEM` chặn cả nguồn có số và mất số. Tiếp dòng mở bằng “là” trong nguồn có số rơi vào nhánh dòng không số và trả `None`. Với nguồn mất số, vế thuật ngữ rỗng làm phép so lệch. Ca Q3 và hai nhánh nguồn trong J1 đạt. [Chốt](../scripts/tl_core/llm_route.py#L1039) · [Q3](../scripts/tl_core/llm_route_test.py#L772) · [J1](../scripts/tl_core/llm_route_test.py#L1170) |
| §3 | VÁ MỘT PHẦN | Test dương giữ chữ, điểm và số, test âm đo lệch đầu ra và từ chối cấu trúc. Ca CLI dùng model giả đo rc 0/5/2. Bộ đo có 152 đột biến, còn khe ở D4. [Test đơn vị](../scripts/tl_core/llm_route_test.py#L1247) · [Selftest CLI](../scripts/tl_selftest.py#L32285) |

**Đường thô.** Giới hạn `ranh-gioi-khoan` đã khai vẫn hiện diện. Khi dữ liệu mất thụt lề hoặc mất số, hai dòng trông đều như định nghĩa hoàn chỉnh có thể bị nhận là hai khoản. Số tiểu mục mất thụt lề cũng có thể tình cờ nối đúng dãy số khoản. Phép so đối chiếu toàn bộ hai vế, số lượng, vị trí và `stt` theo đúng phân đoạn đã nhận. Với nguồn DOCX lùi về thô, D1 và D3 còn có thể làm văn bản giao cho bộ tách bị thiếu từ trước. [Phạm vi kiểm thô](../scripts/tl_core/llm_route.py#L1021) · [Phép so](../scripts/tl_core/llm_route.py#L1179)

## Findings

P1 áp cho đường có thể cho kết quả sai qua `lech_nguyen_van` và ghi `--out`. P2 áp cho từ chối oan một định dạng hợp lệ hoặc cho chốt bắt buộc còn thiếu bằng chứng. Điều kiện merge M1 đòi 0 P0, P1 và P2 mở. [Protocol §8](../docs/PROTOCOL_DA_PHIEN.md#L634) · [ADR-0060 M1–M2](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32) · [ADR-0062](../docs/adr/0062-adr-0060-mac-dinh-va-dong-bang-adr-0054.md#L10)

### D1 [P1] Tiền tố Điều kế tiếp vẫn có thể cắt mất các khoản sau — `scripts/tl_core/llm_route.py:919`

**Kịch bản và căn cứ.** Sau một số khoản hợp lệ, nội dung có đoạn không đánh số trích Điều mang đúng số kế tiếp, hay mở bằng tham chiếu Chương/Mục/Phần mang số. Khi đoạn này không có cờ markup, phần tử lạ hay ngắt mềm, vòng lặp `break` theo tiền tố. `_dieu_ke_tiep` chỉ xét số/hậu tố của dấu mở. Ranh giới lớn còn đi thẳng đến `break`. Các khoản sau không vào `vung`, nên cả chốt đoạn không số lẫn chốt liên tục chỉ thấy phần đầu. Phép so có thể chấp nhận đầy đủ phần đầu ấy và ghi tệp dù đã bỏ khoản thật, ở cả đường cấu trúc và DOCX số tay đi qua `KhongCauTruc`. Đây là biểu hiện còn mở của C1, A1 và B1.

**Đề xuất.** Xác minh vai trò tiêu đề bằng tín hiệu cấu trúc hoặc trả lỗi khi ranh giới chỉ có bằng chứng từ tiền tố. Giữ ca dương Điều kế có tên riêng và kiểm phần nội dung sau một tham chiếu đặt trong thân. [Điểm cắt](../scripts/tl_core/llm_route.py#L919) · [Fallback](../scripts/tl_core/llm_route.py#L953)

### D2 [P1] Bộ đếm giữ qua ngắt section dù định nghĩa Word yêu cầu đánh số lại — `scripts/tl_core/llm_route.py:594,878`

**Kịch bản và căn cứ.** `w15:restartNumberingAfterBreak` là thuộc tính Word trên `abstractNum` để khởi động lại danh sách ở chỗ ngắt section. `_doc_danh_so` chỉ lấy mức và các dấu hiệu không hỗ trợ được liệt kê, còn `_phan_tich_doan` bỏ qua `sectPr` trong `pPr`. `bo_dem_tl` vì vậy giữ nguyên số theo `numId` qua section. Nếu một mục cùng danh sách bắt đầu ở 0 trước ngắt, rồi khoản đầu của Điều sau ngắt hiển thị lại 0, mã sẽ đếm khoản đó là 1. Dãy tự dựng có thể đạt chốt liên tục, rồi xác nhận JSON với `stt` sai. Reset cấp con khi cha tăng và `startOverride` đã có ca sẵn, nhưng xử lý section là một đường riêng.

**Đề xuất.** Tính reset section đối với danh sách Word có thuộc tính này, hoặc báo danh sách không hỗ trợ khi Điều đích dùng nó. Giữ các đối chứng start, override và numId độc lập. [Đọc định nghĩa](../scripts/tl_core/llm_route.py#L583) · [Chạy bộ đếm](../scripts/tl_core/llm_route.py#L878) · [Chốt liên tục](../scripts/tl_core/llm_route.py#L984) · [MS-DOCX §2.5.2.1](https://learn.microsoft.com/en-us/openspecs/office_standards/ms-docx/cbddeff8-01aa-4486-a48e-6a83dede4f13)

### D3 [P1] Regex lọc gạch ngang có thể nuốt ranh giới đoạn và chữ còn hiệu lực — `scripts/docx_markup.py:50,74,245`

**Kịch bản và căn cứ.** Mẫu `_RE_RUN` cho phép bắt đầu ở một run rỗng tự đóng và kéo tới `</w:r>` kế tiếp. Nếu run rỗng đứng cuối khoản trước và run đầu khoản sau bị gạch trực tiếp, `_strike_on` có thể tìm gạch của run sau trong cùng match. `_cut_block` khi đó xóa cả hai đầu mút đoạn và thuộc tính numbering nằm giữa. Phần chữ được giữ ở khoản sau có thể nối vào khoản trước trong XML vẫn parse được. Chốt sửa đổi dấu đoạn chỉ tìm marker revision trên XML gốc, nên thao tác gộp do regex sinh ra đi qua chốt. Phép so sau đó có thể chấp nhận khoản gộp. Một đường mất chữ cùng lớp là `w:strike` tắt trực tiếp với thuộc tính XML nháy đơn hoặc `val` dùng tiền tố tương đương. `_RE_VAL` chỉ đọc `w:val` nháy kép, nên có thể xóa run đang hiển thị trước khi bộ phân tích namespace thấy nó.

**Đề xuất.** Lọc các node markup theo cây và namespace, giữ nguyên nút đoạn cùng các run đứng ngoài node bị bỏ. Khi dùng bộ lọc chung, bảo đảm phép kiểm cấu trúc phát hiện được nếu đầu ra lọc đổi ranh giới đoạn. [Regex và giá trị gạch](../scripts/docx_markup.py#L43) · [Cắt markup](../scripts/docx_markup.py#L243) · [Thứ tự đọc DOCX](../scripts/tl_core/llm_route.py#L863)

### D4 [P2] Hai chốt từ chối còn sống khi vô hiệu hóa riêng — `scripts/tl_core/llm_route_test.py:1333,1487`

**Kịch bản và căn cứ.** Trên bản sao cùng SHA/tree, ép `la=False` duy nhất cho tiêu đề đích ngay trước chốt dòng 913. Chạy lại bộ hiện có trả rc 0, 59/59 ca và 152/152 đột biến. Trong một lần riêng trên bản sao đã phục hồi, bỏ phát marker `la` cho phần tử lạ trong bảng ở dòng 762. Kết quả vẫn rc 0, 59/59 và 152/152. Các đột biến giữ nguyên các neo trong `DOT_BIEN`. Chốt một tiêu đề đích có chữ khớp mẫu nhưng chứa phần tử chưa hiểu, và chốt nhánh bảng có thể che mục cần đếm trước Điều, đều thiếu ca phân biệt. §2.6 C6 và §3 yêu cầu bằng chứng riêng cho từng chốt.

**Đề xuất.** Bổ sung đối chứng cho từng chốt, mỗi ca chỉ có nguyên nhân từ chối tương ứng. Giữ ba ca đã tách cho ranh giới kết thúc Điều. [Chốt tiêu đề](../scripts/tl_core/llm_route.py#L909) · [Chốt bảng](../scripts/tl_core/llm_route.py#L747) · [Yêu cầu](../ops/specs/llm-khoan-docx-r4.md#L89)

### D5 [P2] DOCX Strict của Word bị từ chối ở namespace gốc — `scripts/tl_core/llm_route.py:520,875`

**Kịch bản và căn cứ.** Word có định dạng lưu Strict Open XML Document, vẫn là `.docx`. WordprocessingML Strict dùng namespace `http://purl.oclc.org/ooxml/wordprocessingml/main`. Reader cố định URI Transitional cho toàn bộ phần tử, nên ngay cả Điều có đoạn và danh sách đơn giản cũng rơi vào lỗi thiếu `w:body`. §2.5 liệt kê phạm vi ở mức phần tử và hướng dẫn nói đến DOCX của Word, thiếu giới hạn chỉ đọc Transitional. Đây là một ca từ chối oan có thể suy trực tiếp từ mã. Tần suất dùng Strict trong văn bản luật chưa đo.

**Đề xuất.** Khai rõ giới hạn Transitional với chẩn đoán phù hợp, hoặc nhận diện namespace và hỗ trợ nhất quán ở cả tài liệu, numbering, styles và lọc markup. [Namespace](../scripts/tl_core/llm_route.py#L520) · [Kiểm body](../scripts/tl_core/llm_route.py#L875) · [Phạm vi hướng dẫn](../docs/GOI_AGENT_DA_NEN.md#L390) · [Định dạng Word](https://learn.microsoft.com/en-us/office/compatibility/office-file-format-reference) · [Ánh xạ namespace Strict](https://learn.microsoft.com/en-us/office/open-xml/about-the-open-xml-sdk)

### D6 [P2] Chốt dấu phân cách miễn kiểm tiền tố điểm cả trên đoạn đánh số tự động — `scripts/tl_core/llm_route.py:997,1013`

**Kịch bản và căn cứ.** `chu_doan` chỉ giữ chuỗi, làm mất vai trò đoạn. `doc_dieu_cau_truc` gỡ tiền tố mang hình dấu điểm ở mọi đoạn, kể cả thân một khoản có số tự động. Một ngoặc đóng thuộc chính chữ của đoạn có thể vì vậy bị bỏ khỏi đầu vào `_dong_mo_ho`, trong khi phép so vẫn dùng chữ gốc. §2.6 C3 chỉ cho gỡ dấu điểm gõ tay, tức đoạn không số đã được nhận đúng vai trò ở dòng 978. Đây là khe của chốt bắt buộc, chưa có bằng chứng nó làm đổi điểm tách từ nối trong một tài liệu thật.

**Đề xuất.** Dùng vai trò đoạn đã xác định để quyết định có bỏ dấu điểm hay không. Đo độc lập đoạn tự động và đối chứng điểm gõ tay hợp lệ. [Phân vai](../scripts/tl_core/llm_route.py#L972) · [Chốt mơ hồ](../scripts/tl_core/llm_route.py#L1005) · [Đặc tả C3](../ops/specs/llm-khoan-docx-r4.md#L86)

### Lịch sử theo lớp

| Lớp | Biểu hiện mở ở exact head | Điều kiện đóng |
| --- | --- | --- |
| `ranh-gioi-khoan` | D1 tiếp A1/B1/C1, D6 tiếp C3. Cao nhất P1. K1 và A3 đã đóng ở biểu hiện cụ thể. | Xác thực điểm cắt và kiểm đúng vai trò đoạn, qua cả đường cấu trúc và fallback. |
| `docx-so-hien-thi` | D2, P1. Hai biểu hiện C2 về wrapper và nhãn chữ đã đóng. | Kiểm hoặc từ chối reset section, giữ đối chứng cấp con và numId. |
| `docx-markup-du-thao` | D3, P1. Biểu hiện toggle C4 đã đóng. | Chứng minh lọc markup giữ phần chữ được giữ và giữ ranh giới đoạn nguyên gốc. |
| `do-phu-chot-docx` | D4, P2. Hai đột biến độc lập chưa bị bắt. | Ca đích đỏ đúng lý do trên từng đột biến, baseline đạt. |
| `docx-namespace` | D5, P2, lớp mới về định dạng đầu vào. | Công bố và chẩn đoán giới hạn hoặc kiểm bản Strict đầy đủ qua CLI. |

Năm lớp mở với sáu finding. Trong sáu lớp mở từ lượt 3, hai lớp đóng theo các biểu hiện đã báo là `docx-chu-hien-thi` (C5) và `huong-dan-duong-docx` (C7). Bốn lớp còn mở qua lần chuyển này, tỷ lệ 2/6. Các lớp lặp giữ nguyên slug và tiếp tục thuộc Review Rescue Checkpoint đã nêu ở lượt 3. Lượt này dùng lời gọi 4/5. [Lịch sử lượt 3](../ops/acceptance/llm-khoan-docx/r1/review-3-codex/VERDICT.md#L94) · [Protocol §8.3](../docs/PROTOCOL_DA_PHIEN.md#L812) · [Protocol §12](../docs/PROTOCOL_DA_PHIEN.md#L1097)

## Kết quả test và đột biến

Các lệnh chạy trong Linux x86_64, Python 3.13.18, Git 2.43.0, `core.abbrev=7`, với `PYTHONDONTWRITEBYTECODE=1`. Log và mã thoát lưu trong `/tmp/wp1525-r4-review.sLjav2m9/`. Bản sao sạch cùng head/tree dùng cho release verify và hai đột biến độc lập. Bản sao base detached có tree `0cc14e79cecd2ce44bc4dc6cff92cadb31fd7ee4`.

| Lệnh và phạm vi | Trạng thái | Mã thoát và bằng chứng dương |
| --- | --- | --- |
| `python scripts/tl_core/llm_route_test.py` | `passed` | rc 0, 59/59 ca, 152/152 đột biến, gồm 55 mục `wp1525_*`. Runner chỉ tính giết khi ca đích báo `TinHieuChotCa`. `route.log` |
| Cùng lệnh trên, lần lượt trên hai bản đột biến D4 | `failed` theo tiêu chí giết hai đột biến bổ sung | Mỗi lượt rc 0, 59/59 ca và 152/152 đột biến có sẵn. Hai đột biến bổ sung sống. Delta mã và log riêng `mutant_tieu_de_la.{diff,log}`, `mutant_khoi_la_bang.{diff,log}`. |
| `python scripts/tl.py --deterministic workflow-audit --strict --json` | `passed` | rc 0, `ok=true`, 26 cards, 60 tasks, 194 lệnh, 0 lỗi và 0 cảnh báo. `workflow.log` |
| `python scripts/tl.py --deterministic golden-test --json` | `passed` | rc 0, `ok=true`, 20/20 ca. `golden.log` |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` trên checkout có verdict | `failed` | rc 2, `ok=false`, 187/187 tệp khớp hash. Tệp thừa duy nhất là `.review/VERDICT.md`, do prompt yêu cầu tạo sớm. `release.log` |
| Cùng lệnh `release-verify` trên bản sao sạch cùng head/tree | `passed` | rc 0, `ok=true`, 187/187 tệp, 0 tệp thừa, `package_hash_match=true`. `release_clean.log` |
| `python ops/lease_publish.py check --root . ops/leases/llm-khoan-docx-r4-g1-claude.yaml` | `passed` cục bộ | rc 0, “ĐĂNG ĐƯỢC”, Issue #1525, neo `64b7f2c14776`, hết hạn `2026-11-25T17:48:00Z`. Hai lớp GitHub nằm ngoài lệnh check cục bộ. |
| `python scripts/tl.py --selftest` trên head | `failed` | rc 1, 1774/1790. `[OK] r1525_llm_khai_niem_tep_docx_cau_truc`. `selftest.log` |
| `python scripts/tl.py --selftest` trên base | `failed` | rc 1, 1773/1789. So danh sách 16 dòng `[FAIL]` đã sắp xếp trả diff rỗng, rc 0. `selftest_base.log` |
| `git diff --check fcb12b3 HEAD` | `passed` | rc 0, phạm vi packet #1525. |
| `git diff --check 64b7f2c HEAD` | `failed` | rc 2, ba dòng có Markdown hard break ở hồ sơ #1514 lượt 8 có từ trước #1525. [Hồ sơ](../ops/acceptance/llm-ranh-gioi-khoan/r1/review-8-codex/VERDICT.md#L3) |

Hai selftest chạy khi `/tmp/.git` là thư mục rỗng. Cả hai cùng đỏ 14 ca thuộc `r973_bootstrap_*`, `wp433_*`, `wp727_tl_gws_refresh` đã báo trong prompt, cùng hai ca dùng Git trong repo tạm là `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` và `r268_l2_trichotomy_theo_trang_thai_object`. Đã đo cùng tập 16 ca đỏ và một ca CLI #1525 mới đạt ở head. Gate N/N vẫn đỏ trong môi trường này. Không thấy ca `skipped` được báo bởi sáu lệnh của prompt. [Ca r226](../scripts/tl_selftest.py#L27758) · [Ca r268](../scripts/tl_selftest.py#L29379)

Readback giữ HEAD `fa3a8e2047ccbdb4c20eb11f117732658a653b92` và tree `c88b49297da37d58be06d5dfc856491a99d07956`. `git diff --exit-code` và `git diff --cached --exit-code` đều rc 0. Đã chuyển fixture và state ignored do test sinh ra sang scratch. Snapshot cuối còn `.review/VERDICT.md` và thư mục ignored rỗng `.codex/` có sẵn từ đầu. Hai bản đột biến đã khôi phục tệp trong bản sao tạm.

## Không đo được

- D1–D3, D5 và D6 là kết luận đọc mã, chưa tái hiện với fixture mới hoặc Word/Google Docs bản địa. Các mục Word Standard trong D2 và D5 dùng tài liệu định dạng của Microsoft để xác định ý nghĩa thuộc tính, phần thực thi được suy từ mã candidate. Chưa đo mức độ phổ biến của DOCX Strict trong corpus luật hay phần tử bị thiếu riêng trong bản xuất Google Docs. `w:ptab` là phần tử Word hợp lệ biểu diễn tab theo vị trí, vắng trong danh sách cho phép tại dòng 538 và sẽ bị đánh dấu `la` nếu có trong Điều. Tần suất tab này trong thân văn bản luật chưa có bằng chứng để xếp thêm finding. [Định nghĩa PositionalTab](https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.wordprocessing.positionaltab?view=openxml-3.0.1)
- Một số cảnh báo tài liệu thuộc các giới hạn công bố, gồm trường, hình, chú thích, ngắt mềm, numbering chỉ qua style trong Điều và yêu cầu `can_nguoi_duyet`. Các bộ test sẵn có không cho số đo tần suất từng dạng đầu vào.
- `determinism-audit --strict`, `doc-claims-check --strict` và Ruff F delta trong §5 là `not_run` trong lượt kiểm chứng sáu lệnh này. Windows là `required` theo M3 vì diff thêm dòng Python có `encoding=`. Windows, CI và hai lớp kiểm lease qua GitHub đều `not_run` trong lượt offline. [Spec §5](../ops/specs/llm-khoan-docx-r4.md#L106) · [ADR-0060 M3](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L43)
- Model/effort phục vụ `KHONG_DO_DUOC` từ bản ghi launcher đang chạy. Receipt terminal, rc của lượt Codex và stdout hash thuộc readback sau khi launcher kết thúc. Snapshot chỉ chứng minh trạng thái quan sát được tại hai mốc. [Protocol §8.1–§8.2](../docs/PROTOCOL_DA_PHIEN.md#L770)

P2_mo: 3
VERDICT: REQUEST_CHANGES
