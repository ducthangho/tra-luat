# Verdict packet #1525 r8 lượt 8 — Codex

reviewed_sha: 6d28f34d8505b79bdedccbdf6d66e5852976947e
reviewed_tree: 4e296723b005dbee8f5214dc688f6db4abc61a92
base_sha: 64b7f2c14776d5d0e1d34a6be4725490956f5bec

## Preflight

Checkout detached, `core.abbrev=7`. Git xác nhận base là tổ tiên của head. SHA-256 của blob và bản làm việc `ops/specs/llm-khoan-docx-r8.md` đều là `404341284a66ec6a774542948a141b7256bdace1d687c314a624ea366cadd290`, khớp lease #1525 r8/g1. Lease chỉ định class `sensitive` và Codex CLI. Hạn lease 21:52 UTC ngày 25-11-2026, lượt này là 8/9. Trên diff từ `fcb12b3873c3bec2c339029136243ed2c804ce05` theo phạm vi prompt, toàn bộ 47 path nằm trong write set có hash `a7ba1077150c97ab1e489a936cd496cc14fad3c624e7339babad935ffe0a240b`.

Run `ecf67d1878634c4084e50cf51eb4c94a` qua `.claude/dev/launcher.py run`. `run.json` xác nhận reviewer `openai_codex / codex_cli / machine`, exact head và hash prompt `62875292bd419bb4df5889e83ffe09c3e27f972b5ab2bce6bd1aa6cee18ede2b`. Executor theo lease là `claude / claude_code / machine/local`, họ Claude. Đây là phiên review riêng, Linux 6.18.44, Python 3.13.18, sandbox `workspace-write` theo cấu hình phiên. Tại lúc lập verdict, launcher còn `dang_chay`. Model và effort phục vụ `KHONG_DO_DUOC` từ run đang chạy.

Hai phía bia mộ khớp từng cặp `thay_the_cho` và `da_bi_thay_the`: #1514 r9 ↔ #1525 r1 ↔ r2 ↔ r3 ↔ r4 ↔ r5 ↔ r6 ↔ r7 ↔ r8. r8 không có bia mộ kế nhiệm. Hồ sơ thêm của #1514 thuộc phần loại trừ của prompt. Base trong lease là baseline toàn PR; diff riêng #1525 bắt đầu ở `fcb12b3`, diff bản vá lần này ở `0680db3`.

## Đối chiếu lượt 7 và đặc tả r8

Nguồn lượt 7 là verdict trên `4badb3d`. Các mục r2–r8 trong spec được áp theo thứ tự thay thế.

| Mục | Trạng thái | Bằng chứng |
| --- | --- | --- |
| G1 · §2.10 · ID và nhảy cấp | **ĐÃ VÁ THẬT** cho hai biểu hiện lượt 7 | `_so_id` dùng miền ASCII, định nghĩa ID sai không ghép được, numId trực tiếp sai gắn cờ `la`. Mỗi cấp tổ tiên phải có mục đã thực sự đếm. `wp1525_id_long_leo` và `wp1525_nhan_nhay_cap` chết đúng ca. Nếu ID sai đến từ style, `_doc_kieu` còn xem nó như vắng, một chỗ lệch câu chữ của §2.10 được ghi ở H4. [ID](../scripts/tl_core/llm_route.py#L574) · [Bộ đếm](../scripts/tl_core/llm_route.py#L934) |
| G2 · §2.10 · quan hệ part | **VÁ MỘT PHẦN** ở lớp chọn nguồn XML | Styles ở tên khác thực sự được đọc và chữ gạch bị lọc. Quan hệ styles trỏ part vắng bị chặn trong ca đích. Styles và numbering cùng dùng hàm giải quan hệ part. Part chính của gói và tệp quan hệ của nó vẫn bị cố định tên, xem H2. Độ phủ riêng numbering ở H3. [Giải quan hệ](../scripts/tl_core/llm_route.py#L584) · [Ca G2](../scripts/tl_core/llm_route_test.py#L1321) |
| G3 · F4 · §2.9–§2.10 | **HẾT ĐỐI TƯỢNG** với nhánh tổ tiên giả | `dem` chỉ nhận số của cấp thực sự có đoạn và kiểm trần trước khi sao vào snapshot. `_nhan` đọc từ snapshot đó. Ca start/override quá trần và vượt trần do tăng bộ đếm có sẵn. [Trần](../scripts/tl_core/llm_route.py#L940) · [Ca F4](../scripts/tl_core/llm_route_test.py#L1436) |
| G4 · §2.10 · page/column break | **VÁ SINH LỖI MỚI** | Ngắt trang ở cuối khoản qua đúng ca dương, ngắt mềm còn bị chặn. Gộp mọi ngắt trang/cột thành khoảng trắng làm mất mốc trước số gõ tay nằm sau ngắt, xem H5. [Run](../scripts/tl_core/llm_route.py#L829) · [Ca G4](../scripts/tl_core/llm_route_test.py#L1331) |
| G5 · §2.10 và §3 | **VÁ MỘT PHẦN** | Đã tách mẫu điểm gạch và mẫu abstract ID. Hai đột biến hẹp ở scratch đều chết đúng ca. `DOT_BIEN` vẫn thiếu hai mục riêng như §2.10 yêu cầu. [Mẫu](../scripts/tl_core/llm_route_test.py#L1337) · [Bảng đột biến](../scripts/tl_core/llm_route_test.py#L1515) · H3 |
| G6 · §2.10 và F1 | **VÁ MỘT PHẦN** | Tiêu đề đầu viết hoa qua đúng ca. Quy tắc đó chưa áp cho dò tiêu đề thứ hai nên cùng một hình dạng tiêu đề được nhận ở đầu lại có thể đi vào nội dung khi đánh số như cấp con. Mẫu dò trong vùng đã có từ trước r8. Xem H1. [Ca G6](../scripts/tl_core/llm_route_test.py#L1334) · [Hai mẫu](../scripts/tl_core/llm_route.py#L960) |
| A1/B1/C1/D1/E1/F1 · §2.4–§2.9 · vùng Điều | **HẾT ĐỐI TƯỢNG do hợp đồng r7** với lỗi cắt giữa tài liệu | Đoạn đầu có chữ, số hoặc cờ lạ phải là tiêu đề đích. Mọi đoạn sau đi hết tệp hoặc trả lỗi. Bảng/khối lạ chặn toàn tệp. Tiêu đề dính thân, ngắt mềm và đoạn đánh số rỗng có ca riêng. Nhánh dò tiêu đề thứ hai còn H1. Việc từ chối tệp nhiều Điều là quyết định đã khai. [Vùng Điều](../scripts/tl_core/llm_route.py#L951) · [Ca F1](../scripts/tl_core/llm_route_test.py#L1395) |
| A2/B2/C2/D2/E6/F3/F5 · §2.4–§2.9 · đánh số | **ĐÃ VÁ THẬT** cho các biểu hiện cũ đã đo | Mặc định start 0. Override 5→1 có ca dương riêng. Bộ đếm tách theo numId và reset cấp con khi cấp cha tăng. Cấp khoản buộc decimal và mẫu %N. hoặc %N). Cấp con khác numId, nhảy cấp, số khoản đứt quãng, restart section, cấp ngoài miền và liên kết style/cấp không hỗ trợ đều bị chặn. Nhãn chữ sau Z có đối chứng aa/bb. Bảng lồng hết đối tượng. [Định nghĩa và override](../scripts/tl_core/llm_route.py#L617) · [Phân vai](../scripts/tl_core/llm_route.py#L991) |
| A3/C3/D6 · §2.4–§2.7 · từ nối và dấu phân cách | **ĐÃ VÁ THẬT** | `doc_dieu_cau_truc` đo dấu phân cách trên chữ từng đoạn, không lẫn nhãn tự động. `lech_nguyen_van` tìm “là” chỉ trong đoạn mở khoản, ngoài ngoặc/trích dẫn và trước dấu hai chấm cấp khoản. Ca điểm nhãn chữ hoa không thể cung cấp từ nối cho khoản. Phần miễn chốt cho điểm gõ tay hết đối tượng. [Chốt đoạn](../scripts/tl_core/llm_route.py#L1037) · [Phép so](../scripts/tl_core/llm_route.py#L1211) |
| A4/B3/C4/D3/E2/E5 · §2.4–§2.8 · dự thảo | **ĐÃ VÁ THẬT** cho các biểu hiện cũ | Đọc cây XML gốc, bỏ `del`, `delText`, `moveFrom`, giữ chữ `ins`/`moveTo`, chặn sửa dấu đoạn. Strike/dstrike tính riêng theo docDefaults, style đoạn/ký tự và định dạng trực tiếp. Một tầng bật thì bỏ, nhiều tầng bật chưa có định dạng trực tiếp quyết định thì chặn. Đối chứng giữ ranh giới khi run rỗng và bỏ chữ moveFrom. Nợ regex `docx_markup.py` của E5 đã khai. H2 liên quan chọn XML trước bước này. [Lọc run](../scripts/tl_core/llm_route.py#L796) · [Dấu đoạn](../scripts/tl_core/llm_route.py#L905) |
| A5/E3/E4 · §2.4/§2.8 | **HẾT ĐỐI TƯỢNG do hợp đồng r7** với khoản ngoài vùng và hàng/ô | Bảng bị từ chối toàn tệp. Định nghĩa danh sách không hỗ trợ nhưng không dùng vẫn có ca dương. XML lỗi cú pháp và lỗi chuyển kiểu lúc nạp part có thể chặn trước bước so danh sách được dùng. [Ca A5](../scripts/tl_core/llm_route_test.py#L1278) · [Chốt bảng](../scripts/tl_core/llm_route.py#L951) |
| A6/F2 · điểm gõ tay | **HẾT ĐỐI TƯỢNG do hợp đồng r7** với việc nhận điểm dính thân, **ĐÃ VÁ THẬT** với nhánh nhập điểm gõ tay thành điểm tự động | Đoạn chữ không có số sau khoản đầu trả lỗi, gồm cả chữ cái và gạch. Trước khoản đầu chỉ nhận câu dẫn chuẩn. Đột biến hẹp cho dấu gạch chết đúng mẫu mới. Số gõ tay đầu đoạn có số tự động bị chặn, thân mở bằng số thập phân vẫn được nhận. Trường hợp số gõ tay nằm sau ngắt trình bày xem H5. [Chốt điểm](../scripts/tl_core/llm_route.py#L1005) · [Ca](../scripts/tl_core/llm_route_test.py#L1375) |
| B4/B5/B6/C5/D5/F6 · §2.5–§2.9 · phần tử | **ĐÃ VÁ THẬT** cho các phần tử đã báo | Giữ dấu nối không ngắt, tab/ptab thành khoảng trắng, giữ chữ trong wrapper hợp lệ, bỏ metadata wrapper. So mốc move cân theo ID và lọc chữ trong moveFrom. Chặn phần tử hiển thị chưa hiểu và Strict theo giới hạn đã khai. [Danh sách cho phép](../scripts/tl_core/llm_route.py#L529) · [Ca markup và wrapper](../scripts/tl_core/llm_route_test.py#L1287) |
| A7/B7/C6/D4/E5/F5 · §3 · nghiệm thu hành vi | **VÁ MỘT PHẦN** | Có phản chứng riêng cho startOverride, XML gốc, mốc move, bảng, tiêu đề lạ/ngắt, phạm vi cấp override. Bảng-trước-fallback và dừng ở Điều kế tiếp thuộc hợp đồng cũ. §3 còn câu “dừng ở Điều kế tiếp”, còn ca hiện hành kiểm từ chối thêm tiêu đề. Các khoảng trống còn lại ở H3. |
| A8/B8/C7 · hướng dẫn | **ĐÃ VÁ THẬT** cho những chỗ đã báo | Hướng dẫn nêu một khoản một dòng ở đường thô, một Điều một DOCX, khoản %N. hoặc %N), điểm tự động cùng danh sách, chặn style-only, và `can_nguoi_duyet`. [Hướng dẫn](../docs/GOI_AGENT_DA_NEN.md#L368) |
| §1, §2.1–§2.2 · CLI, câu dẫn, đối chiếu | **ĐẠT** trên hành vi đã đo, có các lỗi đầu vào ở H1, H2 và H5 | ZIP nhận qua chữ ký, cần `--dieu` và cấm kèm số hiệu. Trước khoản đầu, DOCX chỉ có thể bỏ tối đa một câu dẫn khớp toàn mẫu. Chữ và số từ cấu trúc đi thẳng vào phép so, kiểm số mục/thứ tự và cả hai vế theo khoản. `can_nguoi_duyet: true` và `pham_vi_kiem` theo đường. Các hàm gọi model và cờ CLI giữ theo spec. Fixture Điều 3 và ba kết quả lưu đều đạt 8/8. [Handler](../scripts/tl_core/ops_misc.py#L3030) · [Phép so](../scripts/tl_core/llm_route.py#L1211) |
| K1 (#1514 r9) · §2.3 · đường thô | **ĐÃ VÁ THẬT** | `_RE_DIEM` trả None trên cả nguồn có số và mất số. Dòng tiếp “là” ở nguồn có số đi vào nhánh dòng không số và trả None. Ở nguồn mất số, dòng mở bằng “là” thiếu vế thuật ngữ nên không thể qua phép so. Đột biến bỏ chốt điểm và đột biến bỏ qua dòng không số đều bị bắt. [Phân đoạn thô](../scripts/tl_core/llm_route.py#L1057) |

**Fallback.** D1 thay luật cũ tại §2.1 và §2.2. Không còn `KhongCauTruc` trong hai module. DOCX thiếu đánh số hoặc cấu trúc mơ hồ trả rc 2 ngay ở nhánh DOCX. Số hiệu qua `tl extract` và tệp UTF-8 đi thẳng đường thô. [Nhánh không đánh số](../scripts/tl_core/llm_route.py#L987) · [Handler](../scripts/tl_core/ops_misc.py#L3037)

**Ranh giới thô còn lại.** Khi nguồn mất bố cục, lời dẫn nhóm hoặc phần tiếp dòng có đủ hình dạng định nghĩa độc lập, hoặc tiểu mục mang số tình cờ nối đúng dãy, vẫn có thể bị phân thành khoản riêng. Ngược lại, hai phần đã dồn vào một dòng mà không để lại số nội dòng/dấu mơ hồ có thể được so như một khoản. Không thể phát hiện phần đã bị cắt trước khi đưa vào TXT chỉ từ các dòng còn lại. Đây là giới hạn đường thô đã khai. TXT cũng mất dấu vết gạch/xóa đã làm phẳng. Với tuyến số hiệu, mã giữ cảnh báo `[markup]` của extract và chặn CAP. Một extract rc 0 kèm cảnh báo vẫn được so trên bản chữ nó trả, đúng phạm vi tuyến thô. [Phạm vi](../docs/GOI_AGENT_DA_NEN.md#L368) · [Đọc extract](../scripts/tl_core/llm_route.py#L1316) · [Chuyển tiếp cảnh báo](../scripts/tl_core/ops_misc.py#L3083)

## Findings

### H1 [P1] Tiêu đề Điều thứ hai viết hoa có thể bị nhập vào một khoản — `scripts/tl_core/llm_route.py:524`, `:960`, `:974`

Mẫu tiêu đề đích không phân biệt hoa thường. `_RE_DIEU_BAT_KY` trong vùng còn phân biệt. Khi đoạn tiêu đề thứ hai viết hoa được gán số tự động cấp con của cùng danh sách, chốt đoạn không số không áp dụng. Mã nối cả đoạn vào định nghĩa của khoản trước. `lech_nguyen_van` dùng từ nối ở đầu khoản hợp lệ và có thể chấp nhận cả phần tiêu đề bị nhập. Với tiêu đề không số ở cuối Điều, chốt đoạn không số vẫn bắt được.

P1 vì kết quả có thể chứa chữ của một Điều khác và đạt đối chiếu. Nên chia sẻ việc nhận diện tiền tố Điều giữa chốt đầu tệp và chốt trong vùng. Phép kiểm đóng lớp cần tiêu đề viết hoa ở cấp con cùng numId, đối chứng tiêu đề viết hoa hợp lệ ở đầu tệp và trích dẫn giữa thân khoản. Chốt phải giữ điều kiện đầu đoạn để tránh từ chối mọi chỗ dẫn chiếu Điều trong nội dung. [Định vị](../scripts/tl_core/llm_route.py#L954) · [Phân vai](../scripts/tl_core/llm_route.py#L1016)

### H2 [P1] Bộ đọc chưa neo part chính vào quan hệ gốc của gói — `scripts/tl_core/llm_route.py:584`, `:901`

Bộ dựng DOCX của kho khai part chính qua quan hệ `officeDocument` trong `_rels/.rels`. Bộ đọc mở cứng `word/document.xml` và tìm quan hệ styles/numbering từ rels của chính tên cứng này. Khi part chính nằm ở tên khác, nếu tên cũ vắng thì tệp bị từ chối. Nếu ZIP còn bản XML cũ ở tên mặc định và nó tự khớp tiêu đề, kiểu và numbering, bộ đọc dùng bản cũ làm chuẩn. Phép so có thể đạt trên bản có thiếu khoản hoặc chữ gạch bỏ khác part mà Word mở. Đây là suy luận luồng đọc, chưa đo cách Word mở gói có part dư.

P1 vì chọn sai part có thể xác nhận sai nguyên văn. Nên phân giải quan hệ gốc nội bộ duy nhất và lấy rels từ part đã chọn, hoặc dừng nếu part được chỉ định khác đường đã hỗ trợ. Phép kiểm đóng lớp cần đối chứng main part mặc định và main part đổi tên, trong đó có bản XML dư không được dùng, và kiểm part trỏ thiếu. Cần xử lý rõ gói tối giản không khai rels, vì các fixture hiện hành dùng dạng này. Chặn mọi target không chuẩn mà không xác định phạm vi có thể loại tệp Word có part mang tên khác nhưng hợp lệ. [Bộ dựng](../scripts/tl_core/the_thuc.py#L1800) · [Bộ đọc](../scripts/tl_core/llm_route.py#L889)

### H3 [P2] Bảng đột biến chưa khoá riêng ba chốt đã sửa — `scripts/tl_core/llm_route_test.py:1375`, `:1532`, `:1573`

Ca điểm gạch và abstract ID đã tách, nhưng đột biến sẵn `wp1525_gop_doan_khong_so` chết trước ở đoạn thường, còn `wp1525_id_khong_chuan_hoa` chết trước ở numId. G2 có ca đổi tên part styles, còn part numbering luôn ở tên mặc định trong các quan hệ fixture hiện có. Trên scratch, vô hiệu mỗi chốt G5 riêng làm đỏ đúng một ca. Vô hiệu giải quan hệ cho numbering vẫn xanh toàn suite. Mô tả §3 về dừng ở Điều kế tiếp còn thuộc hợp đồng cũ.

P2 vì thiếu bằng chứng hồi quy theo §2.10 G5 và §3, trong khi hành vi đã nêu của G5 có thật. Nên đưa hai đột biến hẹp G5 vào chính `DOT_BIEN`, bổ sung đối chứng đổi tên part numbering và khóa ca đích ở bước giải quan hệ. Cần giữ ca dương cho numId chuẩn hóa và điểm tự động. Tránh chốt bằng một lỗi dùng chung xuất hiện trước ca đích hoặc bằng nguyên chuỗi thông báo lỗi. [Ca dương](../scripts/tl_core/llm_route_test.py#L1318) · [Bảng đột biến](../scripts/tl_core/llm_route_test.py#L1573)

### H4 [P2] NumId không hợp lệ khai trong style bị coi là vắng — `scripts/tl_core/llm_route.py:692`, `:711`, `:870`

`_doc_kieu` lưu `None` cho cả trường hợp không có `w:numId` lẫn có mà sai miền ASCII. `_theo_kieu` tiếp tục theo `basedOn` hoặc kết luận không số. Trong trường hợp không tìm được số từ tổ tiên, một đoạn tiêu đề hoặc câu dẫn dùng style đó vẫn có thể đi qua như đoạn không số. G1 yêu cầu đoạn trỏ ID không hợp lệ thành đoạn lạ. Trực tiếp trỏ ID sai đã có chốt. Với đoạn nội dung thường sau khoản đầu, chốt không số vẫn từ chối.

P2 vì đây là hụt xác thực trên đầu vào lỗi, chưa có đường đã chứng minh nhận sai chữ hoặc số khoản từ biểu hiện này. Nên giữ dấu hiệu ID lỗi riêng với ID vắng và kiểm sau khi áp ưu tiên của numId trực tiếp. Ca khoá cần phân biệt style có ID sai với style chỉ kế thừa, và giữ đối chứng numId trực tiếp hợp lệ đè style. Chặn toàn part styles vì style không dùng có ID lỗi sẽ mở rộng phạm vi từ chối. [Đọc style](../scripts/tl_core/llm_route.py#L676) · [Tính số hiệu lực](../scripts/tl_core/llm_route.py#L870)

### H5 [P1] Ngắt trang hoặc cột che số khoản gõ tay trong đoạn đánh số tự động — `scripts/tl_core/llm_route.py:833`, `:885`, `:1017`

R8 thay ngắt trang/cột bằng khoảng trắng trước khi kiểm. Nếu sau ngắt có một số khoản gõ tay đứng đầu phần chữ mới về mặt hiển thị, `_RE_SO_GO_TAY_DOCX` chỉ nhìn đầu đoạn XML đã gộp. Đường cấu trúc cũng không có phép dò số nội dòng của đường thô. Khi khoản đầu có từ nối hợp lệ, phần chữ mở bằng số gõ tay có thể bị nhập vào định nghĩa ấy và đạt phép so. R7 từ chối ngắt này trước khi phân đoạn.

P1 vì mất ranh giới khi chuẩn hóa tạo đường nhận một định nghĩa gộp. Nên giữ vị trí ngắt trình bày trong `_phan_tich_doan` đến bước kiểm số gõ tay. Phép kiểm đóng lớp cần cả ngắt trang và ngắt cột trước một dấu số khoản, cùng ca đối chứng chỉ phân trang. Chỉ kiểm ở đầu phần chữ tiếp sau ngắt để giảm nguy cơ chặn một phép dẫn chiếu số hợp lệ trong thân đoạn. [Chốt ngắt](../scripts/tl_core/llm_route.py#L829) · [Chốt số gõ tay](../scripts/tl_core/llm_route.py#L1016)

### Lịch sử lớp

| Slug | Biểu hiện trên exact head | Phép kiểm đóng lớp |
| --- | --- | --- |
| `ranh-gioi-khoan` | H1 P1. K1 đã đóng, F1 cắt tiền tố hết đối tượng theo r7, G6 sửa đầu Điều nhưng bất nhất trong vùng. | Ca âm tiêu đề viết hoa thứ hai và ca dương tiêu đề viết hoa ở đầu. |
| `docx-markup-du-thao` | H2 P1 kế tiếp G2. Chọn đúng styles part cho tên tài liệu mặc định đã đạt; còn mỏ neo part chính có thể làm sai cả vùng và markup. | So với part chính thực tế có markup, từ tên mặc định và tên khác. |
| `do-phu-chot-docx` | H3 P2 tiếp G5, có thêm biểu hiện trên numbering part. | Các đột biến hẹp chết đúng ca trong suite thường. |
| `docx-so-hien-thi` | H4 P2. G1 trực tiếp và nhảy cấp đã đóng trên ca cũ; lỗi ID qua style vẫn mất dấu. | Đối chứng ID sai, ID vắng, basedOn và ưu tiên trực tiếp. |
| `docx-gioi-han-bo-dem` | G3 hết đối tượng vì bỏ khởi tạo cấp tổ tiên. | Không tính vào tử số đóng lớp khi đổi cơ chế. |
| `docx-chu-hien-thi` | H5 P1. G4 đã nhận ngắt trang/cột thuần trình bày. Cùng chỗ chuẩn hóa có thể làm mất mốc mở đầu phần chữ sau ngắt. | Xác nhận layout thuần và giữ mốc trước số gõ tay. |

Có 5 lớp mở và 5 finding. H3 có ba khoảng trống đột biến. So sáu lớp mở ở lượt 7, G3 hết đối tượng. Năm lớp còn lại giữ dấu vết qua H1–H5. Tỷ lệ đóng lớp theo §8.3 và §12 là 0/6. Hai chuyển tiếp dưới 50% liên tiếp là tín hiệu Review Rescue Checkpoint trước khi quyết định lượt kế. Ngân sách vẫn ghi 8/9. [Protocol §8.3](../docs/PROTOCOL_DA_PHIEN.md#L812) · [Protocol §12](../docs/PROTOCOL_DA_PHIEN.md#L1128)

## Kết quả test và đột biến

Các lệnh dùng Python 3.13.18 với `PYTHONDONTWRITEBYTECODE=1`, Git 2.43.0 và `core.abbrev=7`. Kết quả head neo vào SHA/tree ở đầu báo cáo. Base đối chứng là `64b7f2c14776d5d0e1d34a6be4725490956f5bec`, tree `0cc14e79cecd2ce44bc4dc6cff92cadb31fd7ee4`. Raw logs ở `/tmp/wp1525-review8.CDMGEwPC`.

| Lệnh | Trạng thái | Rc và bằng chứng dương hoặc lỗi |
| --- | --- | --- |
| `python scripts/tl_core/llm_route_test.py` | `passed` | 0. **59/59** ca, **163/163** đột biến chết, trong đó **66/66** tên `wp1525_*`. `llm.log`. |
| `python scripts/tl.py --deterministic workflow-audit --strict --json` | `passed` | 0. `ok=true`, 194 lệnh, 26 card, 11 nhóm, 60 task, 0 lỗi và 0 cảnh báo. `workflow.log`. |
| `python scripts/tl.py --deterministic golden-test --json` | `passed` | 0. `ok=true`, **20/20** ca đạt, 20/20 bản chiếu và 20/20 byte thô ổn định. `golden.log`. |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | `passed` trên bản sao sạch cùng head | 0. `ok=true`, **187/187** tệp, không có tệp thiếu/thừa/sai. Package hash `bf2853e6cf542403ea8ed8e646f866d1e8e3f6e1026e2bbe6bfdc3d5c81c9437`. `clean-head-release.log`. |
| Cùng lệnh `release-verify` tại checkout đang ghi verdict | `failed` | 2. `ok=false`, tệp thừa duy nhất `.review/VERDICT.md`. Package hash vẫn khớp. `release.log`. |
| `python ops/lease_publish.py check --root . ops/leases/llm-khoan-docx-r8-g1-claude.yaml` | `passed` cục bộ | 0. “ĐĂNG ĐƯỢC”, issue #1525, neo base `64b7f2c14776`, hạn 21:52 UTC. Hai phép kiểm loại Issue/PR và comment từ GitHub là `not_run`. `lease.log`. |
| `python scripts/tl.py --selftest` | `failed` trên head và base | 1 cả hai. Head **1.774/1.790**, base **1.773/1.789**, transport **12/12** cả hai. Tập 16 ca đỏ giống hệt nhau. Chỉ thêm ca đạt `r1525_llm_khai_niem_tep_docx_cau_truc` với model giả, đo rc 0/5/2. `selftest.log`, `base-selftest.log`. |
| `python scripts/tl.py --deterministic determinism-audit --strict --json` | `passed` | 0. `ok=true`, **15/15** chốt. `determinism.log`. |
| `python scripts/tl.py --deterministic doc-claims-check --strict --json` | `failed` trên head và base | 2 cả hai, 131 tệp quét. Cùng một cờ cứng `SHA_NOT_A_COMMIT` tại protocol dòng 1680 cho `9941d8af52aeede1c78ea4e232fbe9a8d5272033`. `git cat-file -t` xác nhận object không có trong checkout shallow. Delta cờ cứng 0. `docclaims.log`, `base-docclaims.log`. |
| `python -B -c 'import runpy,sys; m=runpy.run_path(".claude/dev/ci_dang_ky_test.py"); errors,count=m["loi_ruff_ci"](); print("RUFF_CONTRACT",count,errors); sys.exit(bool(errors) or count == 0)'` | `passed` ở hợp đồng pin/probe | 0. `RUFF_CONTRACT 3 []`. `ruff-contract.log`. |
| `python -m ruff check --no-cache --select F scripts/tl.py` | `failed` trên head và base, delta F đạt | Ruff 0.15.15, rc 1 cả hai. Cùng 12 F821 và 0 F401, log trùng từng byte. `ruff.log`, `base-ruff.log`. |
| `python -m ruff check --no-cache --select F scripts/tl_core/llm_route.py scripts/tl_core/llm_route_test.py` | `passed` | 0. 0 chẩn đoán. `ruff-modules.log`. |
| `git diff --check 0680db3 HEAD` và `git diff --check fcb12b3 HEAD` | `passed` | 0 cả hai. Diff toàn PR `git diff --check 64b7f2c HEAD` rc 2 do ba đuôi khoảng trắng dùng làm xuống dòng cứng Markdown trong hồ sơ #1514 lượt 8. `pr-diff-check.log`. |

Hai tập ca đỏ selftest đã sắp xếp cho `cmp` rc 0. Gồm 8 ca `r973_bootstrap_*`, 5 ca `wp433_*` và `wp727_tl_gws_refresh` khi hiện diện `/tmp/.git` rỗng, cùng `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` và `r268_l2_trichotomy_theo_trang_thai_object`. Delta ca đỏ bằng 0. Điều kiện selftest N/N của §5 vẫn thiếu. SHA-256 log head `53a3beeeaea90591582284b78992f896a7d670f857a163cf3495bb049606ac7f`, log base `5ce09289d0fd9d1082c8695a4f0ccf6f27392f7a54b8e80e2a281b8a336510f8`.

Tôi chạy lại suite có sẵn bằng `python -B -m pdb scripts/tl_core/llm_route_test.py` trên bản sao head, dừng ở nhánh bắt `TinHieuChotCa` dòng 1773 cho tên `wp1525_*`. Pdb rc 0, suite 59/59 và 163/163. Thu được 66 tín hiệu đích. Harness yêu cầu đúng một neo thay, module đột biến nạp được và ca đích ném đúng loại tín hiệu. SHA-256 `pdb-mutants.log`: `95c438959d36d60b4913e122bfa494e746d023076b7d641b1edb88d2972db88f`. [Harness](../scripts/tl_core/llm_route_test.py#L1753)

| Đột biến có sẵn | Tín hiệu thực tế |
| --- | --- |
| `wp1525_id_long_leo`, `wp1525_nhan_nhay_cap` | Ca không còn chặn numId phi số và ca không còn chặn điểm nhảy cấp. |
| `wp1525_styles_ten_mac_dinh`, `wp1525_quan_he_part_vang` | Chữ gạch “CŨ” vào khoản và quan hệ styles trỏ part vắng được nhận. |
| `wp1525_ngat_trang_la_ngat_mem`, `wp1525_tieu_de_phan_biet_hoa` | Chặn oan ngắt trang hoặc tiêu đề viết hoa. |
| `wp1525_gop_doan_khong_so`, `wp1525_id_khong_chuan_hoa` | Chết ở đoạn thường giữa các khoản và ca biến thể numId. Hai tín hiệu riêng của G5 ở phép đo bổ sung bên dưới. |
| `wp1525_tho_nhan_diem`, `dong_la_trong_nguon_co_so_bi_bo_qua` | Ca đích nhận dòng điểm hoặc bỏ qua dòng không số trong nguồn có số. |

Ba phép bổ sung chỉ sửa `llm_route.py` trên các bản sao tạm, mỗi lần chạy nguyên `python scripts/tl_core/llm_route_test.py`. Mọi ca và chuỗi thử nghiệm giữ theo suite có sẵn.

| Đột biến hẹp | Kết quả |
| --- | --- |
| Cho riêng đoạn điểm gõ tay mở bằng dấu gạch nhập vào khoản đang mở | **Bị giết**, rc 1, **58/59**, 163/163 đột biến có sẵn. Lỗi đúng mẫu “diem go tay gach (F2, G5): phai bi chan”. `mutant-dash.log`, `mutant-dash.diff`. |
| Bỏ chuẩn hóa riêng abstractNumId ở định nghĩa và tham chiếu, giữ nguyên numId | **Bị giết**, rc 1, **58/59**, 163/163 đột biến có sẵn. Ca dương 00↔0 bị chặn ở bước tìm định nghĩa numbering. `mutant-abstract.log`, `mutant-abstract.diff`. |
| Dùng tên `word/numbering.xml` cố định, bỏ giải quan hệ riêng cho numbering | **Sống**, rc 0, **59/59**, 163/163 đột biến có sẵn. `mutant-numbering.log`, `mutant-numbering.diff`. |

## Không đo được

- H1, H2, H4 và H5 là đối chiếu mã. Không có ca mới, chuỗi thử mới, tệp DOCX mới hoặc script dò mới. Chưa đo hành vi mở part chính tên khác có part dư, vị trí hiển thị sau ngắt trang/cột, cấp hiệu lực khi số trực tiếp thiếu `ilvl` và style cung cấp cấp, hay ngữ nghĩa move ngoài phép cân ID.
- Không có DOCX Word/Google Docs đã xuất sẵn trong cây Git. Danh sách cho phép chứa tab/ptab, mốc trang tự động, bookmark, comment, proofing, hyperlink, content control và wrapper customXml. Đọc mã cho thấy wrapper nội dòng chỉ hướng chữ `w:dir`/`w:bdo` nằm ngoài danh sách và sẽ bị chặn, nhưng chưa có bằng chứng chúng phổ biến trong DOCX văn bản luật của hai trình xuất. Chưa xác nhận P2 tương thích cho phần tử phổ biến nào ngoài giới hạn đã khai về bảng, trường, ký hiệu/hình, chú thích, ngắt mềm, style-only và Strict.
- Windows native là `required` theo ADR-0060 M3 vì diff toàn PR thêm dòng mã có `encoding=`. Windows native và CI exact head là `not_run`, chưa đo trong lượt offline. `full_mutant_audit` của CI là `not_run`, phạm vi diff không kích hoạt M9. Kiểm GitHub, model thật, và LIVE là `not_run`. Có **0** lệnh `skipped` trong sáu lệnh của prompt. [ADR-0060 M3/M9](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L43)
- Launcher đang chạy khi lập verdict. Rc terminal của tiến trình con và hash stdout toàn lượt phải đọc sau khi run kết thúc. Model/effort phục vụ vẫn `KHONG_DO_DUOC` trong run đang mở. Repo nguồn của Executor và head trên GitHub nằm ngoài quan sát offline.
- Ở checkout giao review, golden/selftest sinh `references/golden/fixtures/` và `scripts/.tl_state/` ignored. Đã chuyển hiện vật phát sinh ra scratch sau khi test dừng. Cuối lượt, HEAD/tree khớp đầu lượt, diff tracked và index rc 0. Chỉ còn verdict mới và thư mục ignored `.codex/` có sẵn. Hai mốc này chứng minh delta quan sát được. Nội dung `.codex/` nằm ngoài phép đọc.

## Kết luận

**0 P0, 3 P1, 2 P2, 0 P3** mở. K1 đã đóng. Exact head chưa đủ điều kiện merge theo ADR-0060 M1, áp mặc định qua ADR-0062. [ADR-0060 M1](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32) · [ADR-0062](../docs/adr/0062-adr-0060-mac-dinh-va-dong-bang-adr-0054.md#L10)

P2_mo: 2

VERDICT: REQUEST_CHANGES
