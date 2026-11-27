# Verdict packet #1525 r9 lượt 9 — Codex

reviewed_sha: 4c647c8846939281d268e3efb2abe9c22d985e03
reviewed_tree: 816d345e578babf728dfc8eb55ed98fdad81e912
base_sha: 64b7f2c14776d5d0e1d34a6be4725490956f5bec
base_tree: 0cc14e79cecd2ce44bc4dc6cff92cadb31fd7ee4

## Preflight

- Checkout detached của `ducthangho/tra-luat`. Ref cục bộ và remote-tracking của nhánh `ccr-89c0d2e2-inanqb` cùng trỏ exact head. Base và mốc cuối của #1514 `fcb12b3873c3bec2c339029136243ed2c804ce05` đều là tổ tiên. `origin/master` trong bản sao có OID riêng `5259239d763c9ffc1677f033bd9a9cf23ede9299`. Baseline đo là OID trong spec/lease. Git đầu phiên có `core.abbrev=7` và diff/index rỗng.
- Packet #1525 r9/g1, class `sensitive`, lượt 9/9 (8 đã dùng), lease hết hạn 22:12 UTC ngày 25-11-2026. SHA-256 của blob đặc tả và tệp làm việc đều là `59633727270693a21fe000ef6affcaa02e2f8bf92207e50c054267cb386d2875`, khớp lease. SHA-256 write set theo đường dẫn sắp xếp/LF là `3ddac135121df32256a2aced80567d2eb27f22e1e6bf42c0e5491b5285d8f270`. Toàn bộ 52 đường dẫn của diff từ `fcb12b3` sau loại hồ sơ #1514 theo prompt, và cả 8 đường dẫn của bản vá từ `58fe4ed`, nằm trong write set. `thay_the_cho` và `da_bi_thay_the` khớp hai chiều ở cả 9 cặp liên tiếp #1514 r9 ↔ #1525 r1 ↔ r2 ↔ r3 ↔ r4 ↔ r5 ↔ r6 ↔ r7 ↔ r8 ↔ r9. r9 là đầu chuỗi hiện hành. [Lease](../ops/leases/llm-khoan-docx-r9-g1-claude.yaml) · [Đặc tả](../ops/specs/llm-khoan-docx-r9.md)
- Run `bdc94141060c48a094cde99622e7da46` xác nhận reviewer `openai_codex / codex_cli / machine`, exact head và thiết lập checkout độc lập. SHA-256 prompt `e3bb844ff0b035947310a21e06c712de476965cbd967ce935aeb79a8fdcc43da` khớp `run.json` và checkpoint. Executor theo lease là `claude / claude_code / machine/local` (`anthropic_claude` theo bảng provider). Sandbox `workspace-write` theo cấu hình phiên. Linux 6.18.44, x86_64, Python 3.13.18, Git 2.43.0 và Codex CLI 0.172.0. Model và effort phục vụ `KHONG_DO_DUOC` từ dữ liệu launcher đang chạy. [Protocol §8.1](../docs/PROTOCOL_DA_PHIEN.md#L770)

## Đối chiếu lượt 8 và đặc tả r9

Lượt 8 review `6d28f34d8505b79bdedccbdf6d66e5852976947e`. Các điểm sửa đổi từ §2.4 đến §2.11 được áp theo thứ tự. Trạng thái từng biểu hiện cũ và trạng thái toàn lớp được ghi riêng theo §8.3. [Verdict lượt 8](../ops/acceptance/llm-khoan-docx/r1/review-8-codex/VERDICT.md)

| Mục | Trạng thái | Bằng chứng |
| --- | --- | --- |
| H1 · §2.11 · tiêu đề viết hoa | **ĐÃ VÁ THẬT** với tiền tố viết trong chữ đoạn | `_RE_DIEU_BAT_KY` dùng `re.IGNORECASE`. Ca tiêu đề viết hoa ở cấp con cùng numId bị chặn, đột biến phân biệt hoa thường bị giết. Tiêu đề tự sinh qua nhãn Word còn J3. [Mã](../scripts/tl_core/llm_route.py#L523) · [Ca](../scripts/tl_core/llm_route_test.py#L1420) |
| H2 · §2.11 · part chính và các quan hệ | **ĐÃ VÁ THẬT** cho chọn part chính, **VÁ MỘT PHẦN** về bằng chứng cho tổ hợp part chính đổi tên và rels riêng | `_phan_chinh` theo quan hệ gốc và ca dương có cả XML dư ở tên cũ. Ca part đích vắng trả lỗi. Theo mã, `_phan_qua_quan_he` dựng đường dẫn từ part đã chọn. Vô hiệu riêng việc dựng đường dẫn ấy vẫn xanh, xem J4. [Mã](../scripts/tl_core/llm_route.py#L605) · [Ca](../scripts/tl_core/llm_route_test.py#L1340) |
| H3 · §2.11/§3 · ba đột biến thiếu | **ĐÃ VÁ THẬT** cho ba biểu hiện đã báo | `wp1525_gop_doan_khong_so`, `wp1525_id_khong_chuan_hoa`, `wp1525_numbering_ten_mac_dinh` đều được gắn ca đích riêng và bị giết. Điểm chữ, numId thường và styles đổi tên vẫn có ca. Độ phủ kết hợp part và diễn giải §3 còn J4. [Ba ca](../scripts/tl_core/llm_route_test.py#L1372) · [Bảng](../scripts/tl_core/llm_route_test.py#L1623) |
| H4 · §2.11 · numId lỗi qua style | **ĐÃ VÁ THẬT** với biểu hiện lượt 8 | `!` giữ riêng ID sai, sau ưu tiên numId trực tiếp mới gắn `la`. Ca dùng style lỗi ở câu dẫn giết `wp1525_numid_style_loi_la_vang`. Cấp kế thừa khi có numId trực tiếp còn J1. [Đọc style](../scripts/tl_core/llm_route.py#L710) · [Áp style](../scripts/tl_core/llm_route.py#L893) · [Ca](../scripts/tl_core/llm_route_test.py#L1427) |
| H5 · §2.11 · chữ sau ngắt trang/cột | **VÁ SINH LỖI MỚI** | Chữ giữ lại sau ngắt trang bị chặn, đột biến `wp1525_chu_sau_ngat_trang` chết. Ca ngắt trang cuối đoạn vẫn đạt. Ngắt cột đi cùng nhánh mã. Chữ gạch bỏ sau ngắt vẫn có thể bật cờ trước khi lọc run, xem J5. [Mã](../scripts/tl_core/llm_route.py#L846) · [Ca cuối đoạn](../scripts/tl_core/llm_route_test.py#L1331) · [Ca giữa đoạn](../scripts/tl_core/llm_route_test.py#L1430) |
| §1, §2.1–§2.2 · bất biến và CLI | **ĐẠT** trong phạm vi đã đo | Định tuyến model giữ nguyên theo diff, cờ CLI giữ nguyên. Nhánh ZIP buộc `--dieu`, cấm gắn số hiệu và chuyển khoản cấu trúc tới phép so. Kết quả gắn `can_nguoi_duyet: true` và đúng `pham_vi_kiem` theo đường. Fixture Điều 3 và ba kết quả đã lưu vẫn khớp 8/8. [CLI](../scripts/tl_core/ops_misc.py#L3025) · [Phạm vi](../scripts/tl_core/ops_misc.py#L3113) |
| A1/B1/C1/D1/E1/F1, G6 · §2.4–§2.10 · chọn vùng | **HẾT ĐỐI TƯỢNG do hợp đồng r7** cho mọi heuristic cắt giữa tệp, **ĐÃ VÁ THẬT** cho tiêu đề đích viết hoa G6 | Đoạn có nội dung đầu là tiêu đề đúng Điều, sau đó đọc tới hết tệp hoặc báo lỗi. Bảng hoặc khối lạ chặn toàn tệp. Ca tiêu đề dính thân, ngắt mềm, tiêu đề tự đánh số, thêm tiêu đề và sai số Điều vẫn đạt. Trường hợp nhãn hiển thị sinh tiền tố còn J3. [Vùng Điều](../scripts/tl_core/llm_route.py#L977) |
| A2/B2/C2/D2/E6/F3/F4/F5, G1/G3 · §2.4–§2.10 · số hiển thị | **ĐÃ VÁ THẬT** cho các ca cũ, **HẾT ĐỐI TƯỢNG** với duyệt bảng và bộ đếm tổ tiên giả | Start vắng = 0. Ca override 5→1 đạt. Tách `numId`, reset cấp con khi cấp cha tăng, bác nhảy cấp, giới hạn 0–8 và trần 999. Nhãn chữ kiểm a…z, aa, bb. Cùng danh sách và dãy khoản từ 1 là điều kiện nhận. Chặn `lvlRestart`, `isLgl` bật, liên kết style, restart section, định danh sai hoặc trùng theo các ca đích. Cách xác định cấp trước bộ đếm còn J1. [Định nghĩa](../scripts/tl_core/llm_route.py#L623) · [Bộ đếm](../scripts/tl_core/llm_route.py#L949) · [Ca](../scripts/tl_core/llm_route_test.py#L1273) |
| A3/C3/D6 · §2.4–§2.7 · từ nối, dấu phân cách | **ĐÃ VÁ THẬT** | Dò “là” chỉ trong đoạn mở khoản, ngoài ngoặc/trích dẫn và trước dấu hai chấm cấp khoản. Kiểm dấu phân cách trên chữ mọi đoạn trước khi so hai vế. Miễn chốt cho điểm gõ tay hết đối tượng. [Chốt dấu](../scripts/tl_core/llm_route.py#L1063) · [So](../scripts/tl_core/llm_route.py#L1237) |
| A4/B3/C4/D3/E2/E5, G2 · §2.4–§2.10 · dự thảo | **ĐÃ VÁ THẬT** cho các ca cũ về lọc trực tiếp và theo style | Dùng cây XML gốc. Bỏ `del`, `delText`, `moveFrom`. Giữ `ins`, `moveTo`. Chặn sửa dấu đoạn. Gạch đơn/kép tính riêng. Nhiều tầng chưa rõ thì chặn, trực tiếp quyết định. Ca E5 giữ đoạn khi run rỗng liền trước run gạch, styles đổi tên lọc được. Thuộc tính tương thích trong `rPr` còn J2, và tương tác ngắt trang ở J5. [Đọc run](../scripts/tl_core/llm_route.py#L825) · [Dấu đoạn](../scripts/tl_core/llm_route.py#L935) |
| A5/E3/E4 · §2.4/§2.8 · bảng, danh sách không dùng | **HẾT ĐỐI TƯỢNG do hợp đồng r7** với phần ngoài Điều và hàng/ô bảng | Tệp một Điều từ chối bảng. Định nghĩa danh sách không hỗ trợ nhưng không dùng có ca dương. XML không parse được vẫn có thể dừng ngay khi nạp part. [Ca A5](../scripts/tl_core/llm_route_test.py#L1278) |
| A6/F2 và K1 · §2.3/§2.9 · điểm gõ tay, tiếp dòng | **HẾT ĐỐI TƯỢNG** với việc nhận điểm gõ tay ở DOCX, **ĐÃ VÁ THẬT** với K1 | Điểm gõ tay riêng đoạn sau khoản đầu bị chặn. Cấp con phải tự động cùng numId. Ở đường thô, dòng khớp `_RE_DIEM` bị chặn cả hai kiểu nguồn. Nguồn có số chặn dòng mở bằng “là” ngay ở nhánh dòng không số. Nguồn mất số đưa dòng đó qua phép so, từ chối do vế thuật ngữ rỗng. Ca một dòng là đối chứng. [Đường thô](../scripts/tl_core/llm_route.py#L1097) · [Ca K1](../scripts/tl_core/llm_route_test.py#L1170) |
| B4/B5/B6/C5/D5/F6, G4 · §2.5–§2.10 · phần tử và ngắt | **ĐÃ VÁ THẬT** cho các biểu hiện cũ được đo. G4 còn J5 | Cho tab/ptab, dấu nối không ngắt, các wrapper đã khai và mốc move cân. Số thập phân đầu khoản giữ nguyên. Phần tử hiển thị ngoài danh sách, Strict và ngắt mềm bị chặn như đã khai. [Danh sách](../scripts/tl_core/llm_route.py#L529) · [Ca](../scripts/tl_core/llm_route_test.py#L1287) |
| A7/B7/C6/D4/E5/F5, G5 · §3 · test | **ĐÃ VÁ THẬT** ở các ca đích cũ, **VÁ MỘT PHẦN** ở hợp đồng nghiệm thu hiện hành | Các ca ranh giới, startOverride, markup, miền cấp và ba đột biến H3 đều có. Cụm ca còn thiếu tổ hợp rels của part chính đổi tên. Văn bản §3 còn ghi dừng ở Điều kế tiếp trong khi theo r7 phải từ chối tệp chứa Điều khác. [§3](../ops/specs/llm-khoan-docx-r9.md#L151) |
| A8/B8/C7 · hướng dẫn | **ĐÃ VÁ THẬT** theo các điểm báo trước | Hướng dẫn nêu một khoản một dòng ở TXT, một Điều một DOCX, nhãn khoản `%N.` hoặc `%N)`, điểm tự động cùng danh sách và chặn style-only. [Hướng dẫn](../docs/GOI_AGENT_DA_NEN.md#L370) |

**`KhongCauTruc` và câu dẫn.** §2.7 D1 đã thay fallback ở §2.1–§2.2. Hai module hiện hành không còn `KhongCauTruc`. Thiếu đánh số tự động hay cấu trúc mơ hồ ở nhánh ZIP dẫn tới rc 2, trước lời gọi model. Chỉ tệp UTF-8 và tuyến số hiệu qua `extract` vào đường thô. DOCX bỏ tối đa một câu dẫn đúng toàn mẫu ở trước khoản đầu. Chốt `la`, số và ngắt trong vùng áp trước bước bỏ đoạn rỗng. [DOCX](../scripts/tl_core/llm_route.py#L999) · [Câu dẫn](../scripts/tl_core/llm_route.py#L1063) · [CLI](../scripts/tl_core/ops_misc.py#L3037)

**Phạm vi phép so đường thô.** Nếu phân đoạn nguồn đúng, so vị trí, số lượng và toàn bộ hai vế loại được đầu ra tự bỏ, gộp, cắt hay tráo khoản. Bố cục đã mất vẫn có thể làm một lời dẫn hoặc tiếp dòng đủ hình dạng thành một khoản, một tiểu mục trùng số thành khoản kế, hoặc nhiều phần đã dồn lên một dòng thành một khoản. Dấu điểm ngoài mẫu có thể đi theo nhánh này ở nguồn mất số nếu cả dòng tự khớp hình dạng thuật ngữ và định nghĩa. Bản bị cắt trước khi thành TXT hay chữ gạch/xóa đã bị làm phẳng không thể được phát hiện từ các dòng còn lại. Tuyến số hiệu chặn cảnh báo CAP và chuyển tiếp cảnh báo markup của `extract`. Bản chữ được đối chiếu là bản tuyến đọc trả về, luôn mang cờ cần duyệt ranh giới. [Phạm vi](../scripts/tl_core/llm_route.py#L1079) · [CAP](../scripts/tl_core/llm_route.py#L1342) · [CLI](../scripts/tl_core/ops_misc.py#L3084)

## Findings

### J1 [P1] Cấp đánh số từ style có thể nhập một khoản thành điểm — scripts/tl_core/llm_route.py:710, :893, :1045

**Kịch bản và căn cứ.** Một style đoạn khai danh sách và `ilvl` khác 0. Trên đoạn, numId được khai trực tiếp, ilvl vắng, danh sách không có liên kết `lvl/pStyle`. Với đánh số từ style, Word bỏ qua `ilvl` của style và dùng liên kết style với cấp nếu có. Reader lại tra `ilvl` từ chuỗi style, sau đó lấy numId trực tiếp và hạ `tu_style` về false. Trong trường hợp này nó mang cấp từ style vào numPr trực tiếp, thay cho cấp mặc định 0. Một khoản cấp 0 của Word có thể bị xếp cấp 1 sau một khoản đã mở, trong cùng numId. Bộ đếm cấp 0 vẫn liên tục trên tập mà reader phân được. Mục kế tiếp bị dịch số và mô hình có thể đạt phép so bằng cách chép cả khoản bị nhập như điểm. Trình chặn style-only ở dòng 1009 không thấy trường hợp này. P1 vì có thể nhận nguyên văn của một phân đoạn sai trên đường công bố ranh giới từ cấu trúc. [Đọc cấp và phân vai](../scripts/tl_core/llm_route.py#L893) · [Lịch sử B2](../ops/acceptance/llm-khoan-docx/r1/review-2-codex/VERDICT.md#L43)

**Đề xuất.** Ở `_phan_tich_doan`, xác định ilvl cùng nguồn hiệu lực của numPr, hoặc từ chối trường hợp lai có thể làm thay đổi cấp. Khóa ca có numId trực tiếp và ilvl chỉ từ style, giữ đối chứng ilvl trực tiếp 0 và 1. Giữ chốt `lvl/pStyle` cùng ưu tiên numId trực tiếp hợp lệ trước ID lỗi của style. Chặn mọi đoạn có style sẽ loại cả style chỉ mang định dạng.

### J2 [P1] Thuộc tính gạch trong nhánh tương thích có thể bị bỏ qua — scripts/tl_core/llm_route.py:705, :825, :862

**Kịch bản và căn cứ.** Khi thuộc tính gạch có hiệu lực nằm trong nhánh được chọn của `mc:AlternateContent` bên trong `w:rPr`, tra con trực tiếp `rPr.find(w:strike)` hoặc `dstrike` không thấy nó. `rPr` được bỏ qua nguyên khối trong danh sách con của run, nên cờ `la` cũng không bật. Cách lấy thuộc tính trực tiếp trong `_doc_kieu` có cùng khoảng trống với `rPr` của style và docDefaults. Chữ còn trong `w:t` được đưa vào khoản rồi thành chính chuẩn so. P1 vì kết quả khớp chuẩn nội bộ có thể chứa chữ đã gạch bỏ của dự thảo. Đây là kết luận theo nhánh xử lý XML, chưa đo Word với tài liệu cụ thể. [Đọc thuộc tính style](../scripts/tl_core/llm_route.py#L705) · [Đọc run](../scripts/tl_core/llm_route.py#L825)

**Đề xuất.** Kiểm bất định ở các cây thuộc tính có ảnh hưởng tới chữ và số trước khi bỏ qua chúng. Chỉ tiếp tục khi đã chọn được nhánh tương thích theo chính sách được hỗ trợ hoặc xác định cây đó không ảnh hưởng. Khóa ca thuộc tính gạch trong nhánh tương thích và ca đối chứng định dạng trực tiếp, style và metadata vô hại. Quét đệ quy mọi `strike` sẽ có thể lấy cả thuộc tính ở nhánh không được chọn hoặc bản thuộc tính cũ trong `rPrChange`.

### J3 [P1] Chốt thêm tiêu đề chỉ đọc thân đoạn, bỏ qua nhãn tự động — scripts/tl_core/llm_route.py:763, :999, :1047

**Kịch bản và căn cứ.** Chốt §2.9 chỉ dò tiền tố Điều/Chương/Mục/Phần trên `d["chu"]`. Một tiêu đề có tiền tố và số sinh từ `lvlText` cấp con cùng numId có thể có thân chỉ chứa tên tiêu đề. `_nhan` cho phép nhãn cấp con mang tiền tố chữ và giữ cả nhãn khi nối vào khoản. Vì chốt tìm trước khi dựng nhãn, hình dạng tiêu đề thuộc điều kiện từ chối vẫn được nhập vào định nghĩa và có thể khớp nguyên văn theo phân đoạn đã nhập. H1 đã khóa tiền tố nằm trong chữ đoạn. P1 vì đường cấu trúc có thể nhận thêm nội dung dưới một tiêu đề khác, dù phép kiểm một Điều được báo đã qua. [Nhận diện](../scripts/tl_core/llm_route.py#L999) · [Nối nhãn](../scripts/tl_core/llm_route.py#L1042)

**Đề xuất.** Sau khi có cấp và nhãn hiệu lực, áp chốt tiêu đề cho cả chữ hiển thị ở đầu đoạn rồi mới nối điểm. Khóa ca tiêu đề dùng nhãn tự động và đối chứng một điểm có dẫn chiếu Điều trong thân. Chỉ dò đầu đoạn để tránh từ chối dẫn chiếu thông thường.

### J4 [P2] Suite chưa khóa việc đọc rels riêng của part chính đổi tên — scripts/tl_core/llm_route_test.py:1340, :1388, :1627

**Kịch bản và căn cứ.** Ca part chính đổi tên có bản XML dư ở tên mặc định, nhưng part mới không có tệp quan hệ riêng và dùng fallback numbering mặc định. Ca numbering đổi tên dùng part chính mặc định. Trên bản sao, tôi thay đầu vào của `posixpath.split` từ `chinh` thành tên part cố định trong `_phan_qua_quan_he`. Suite vẫn rc 0, 62/62 ca và 168/168 đột biến có sẵn. Vì vậy hồi quy nửa sau H2 không bị bắt. §3 vẫn mô tả ca “dừng ở Điều kế tiếp” của hợp đồng cũ, trong khi §2.9 yêu cầu từ chối. P2 vì thiếu bằng chứng hồi quy theo §2.11/§3, còn code ứng viên hiện tại có chuyển đúng `chinh`. [Ca part chính](../scripts/tl_core/llm_route_test.py#L1340) · [Ca numbering](../scripts/tl_core/llm_route_test.py#L1388) · [§3](../ops/specs/llm-khoan-docx-r9.md#L151)

**Đề xuất.** Dùng part chính đổi cả đường dẫn thư mục với rels riêng dẫn đến numbering và styles, để tệp rels ở tên cũ trỏ nơi khác. Ca đích cần phân biệt đầu ra dựa trên đúng số và đúng chữ đã lọc. Thêm vào `DOT_BIEN` thay đổi chỉ làm mất đường dẫn rels đã chọn, giữ riêng ca fallback tối giản và ba ca H3. Cập nhật câu §3 theo từ chối tệp nhiều Điều. Ca chỉ kiểm lỗi mở ZIP có thể làm đột biến chết sớm vì lý do khác.

### J5 [P2] Chữ gạch bỏ sau ngắt trang làm đoạn bị từ chối — scripts/tl_core/llm_route.py:846, :866, :1004

**Kịch bản và căn cứ.** Trong một đoạn dự thảo, ngắt trang/cột đi sau toàn bộ chữ còn hiệu lực, sau đó chỉ có một run gạch bỏ. Reader vẫn kiểm chữ của run ấy tại dòng 851 trước khi bỏ run ở dòng 866, khiến `ngat` sống đến chốt vùng ở dòng 1004. Nội dung giữ lại thực tế kết thúc ở ngắt, nhưng H5 từ chối cả Điều. Nội dung bọc `w:del` đi qua nhánh bỏ sớm và không gây hiệu ứng này. Đây là tương tác giữa hai định dạng Word được đặc tả hỗ trợ. P2 vì chặn một Điều có thể đọc, không xác nhận chữ sai. [Thứ tự xử lý](../scripts/tl_core/llm_route.py#L846) · [Chốt vùng](../scripts/tl_core/llm_route.py#L1004)

**Đề xuất.** Tính `ngat` của H5 trên phần chữ sau khi lọc revision, giữ riêng quyết định đối với phần tử chưa hiểu. Đối chứng một ngắt cuối đoạn có chữ gạch bỏ phía sau và một ngắt có chữ giữ lại phía sau. Cần giữ ca số gõ tay sau ngắt để việc lọc chữ không vô tình mở lại đường gộp ở H5.

### Lịch sử lớp

| Slug | Lượt nguồn và biểu hiện còn mở | Hạng cao nhất | Cách đóng lớp |
| --- | --- | --- | --- |
| `docx-so-hien-thi` | A2/B2/C2/D2/F3/G1/H4 → J1. Các ca trần, reset, startOverride, ID và numId lỗi ở H4 đạt. | P1 | Đối chiếu cấp Word hiệu lực khi khai trực tiếp xen style rồi đo đủ số và các điểm của khoản. |
| `docx-markup-du-thao` | A4/B3/C4/D3/E2/G2/H2 → J2. H2 đóng chọn XML chính theo quan hệ gốc trên ca đã đo. | P1 | Xác thực cây thuộc tính tương thích trước khi chọn chữ làm chuẩn. Sửa ở lớp thuộc tính, độc lập với đường dẫn part. |
| `ranh-gioi-khoan` | F1/G6/H1 → J3. K1 trên hai đường ghép thô đã đóng. Cắt vùng theo tiền tố hết đối tượng. | P1 | Dò tiêu đề cả chữ đoạn lẫn nhãn hiệu lực trước khi gắn điểm. |
| `do-phu-chot-docx` | A7/B7/C6/D4/E5/F5/G5/H3 → J4. Ba đột biến H3 đã chết đúng ca đích, phép kết hợp H2 vẫn thiếu. | P2 | Ca rels kết hợp và đột biến hẹp phải đỏ đúng vì chọn sai part. Chỉnh §3 theo hợp đồng r7. |
| `docx-ngat-trinh-bay` | G4/H5 → J5. Ca chữ giữ lại sau ngắt trang đã đóng. | P2 | Đối chứng chữ giữ và chữ bỏ sau ngắt, giữ chốt với số gõ tay sau ngắt. |

Có 5 biểu hiện mở trên 5 lớp. Tập cũ có các biểu hiện đã đóng theo bảng đối chiếu, nhưng 5 lớp trên vẫn mở. Mức P1 áp khi đường cấu trúc có thể nhận nguyên văn sai. P2 áp khi chặn oan hoặc hụt phép kiểm hồi quy. Theo ADR-0060 M1 và ADR-0062, cả P1 lẫn P2 mở đều chặn merge. Lượt 9 đã dùng hết trần được giao. [Protocol §8.3](../docs/PROTOCOL_DA_PHIEN.md#L812) · [ADR-0060](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32) · [ADR-0062](../docs/adr/0062-adr-0060-mac-dinh-va-dong-bang-adr-0054.md#L12)

## Kết quả test và đột biến

Đo bằng bản sao cục bộ ở exact SHA và tree ở đầu báo cáo. Tắt ghi bytecode, lưu stdout/stderr và mã thoát tại `/tmp/wp1525-r9-review.Txs3eM/`. Rerun golden và selftest dùng `core.abbrev=7` như checkout được giao.

| Lệnh | Trạng thái | Mã thoát và bằng chứng |
| --- | --- | --- |
| `python scripts/tl_core/llm_route_test.py` | `passed` | rc 0, **62/62** ca, **168/168** đột biến bị giết, gồm **71/71** mục `wp1525_*`. `llm.log` |
| `python scripts/tl.py --deterministic workflow-audit --strict --json` | `passed` | rc 0, `ok=true`, 26 card, 60 task, 194 lệnh hiện diện, 0 lỗi, 0 cảnh báo. `audit.log` |
| `python scripts/tl.py --deterministic golden-test --json`, clone đầu | `failed` | rc 2, 19/20. Clone mặc định chưa ghim `core.abbrev`. `doc_claims_check_fixture` đổi thứ tự cờ do ngưỡng độ dài SHA. `golden.log` |
| Cùng lệnh golden trên exact head, ghim `core.abbrev=7` | `passed` | rc 0, `ok=true`, **20/20** ca, 20/20 bản chiếu ổn định, byte thô 19/20. `hygiene_sweep_fixture` có `diff={}` sau chiếu. `golden-pinned.log` |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | `passed` | rc 0, `ok=true`, **187/187** tệp, 0 tệp sai/thiếu/thừa. Băm gói đọc lại `1a14cee5922e117a57ee29e407b95dcf9251bced854735f8913a5c64e51b2b4d` khớp manifest. `release.log` |
| `python ops/lease_publish.py check --root . ops/leases/llm-khoan-docx-r9-g1-claude.yaml` | `passed` cục bộ | rc 0, “ĐĂNG ĐƯỢC”, Issue #1525, neo `64b7f2c14776`, hạn 22:12 UTC. Phép `check` chỉ ở cục bộ. `lease.log` |
| `python scripts/tl.py --selftest`, hai clone ban đầu | `failed` | rc 1 mỗi lượt. Head **1772/1790**, base **1771/1789**, transport 12/12 mỗi lượt. Cùng 18 ca đỏ, ca CLI #1525 mới đạt. Bốn ca kiểm claim SHA có mặt trong tập đỏ của clone chưa ghim. `self-head.log`, `self-base.log` |
| Cùng lệnh selftest ở head và base, ghim `core.abbrev=7` | `failed` | rc 1 mỗi lượt. Head **1774/1790**, base **1773/1789**, transport **12/12** mỗi lượt. Cùng **16 ca đỏ**, ca duy nhất thêm ở head là `r1525_llm_khai_niem_tep_docx_cau_truc` và ca này đạt. `self-head-pinned.log`, `self-base-pinned.log` |
| `python scripts/tl_core/llm_route_test.py`, trên bản đột biến J4 | `passed` trên bản đột biến | rc 0, **62/62**, **168/168**. Đột biến hẹp J4 sống sót. `mutant-h2.diff`, `mutant-h2.log` |
| `git diff --check 58fe4ed HEAD` và `git diff --check fcb12b3 HEAD -- . ':!ops/acceptance/llm-ranh-gioi-khoan'` | `passed` | rc 0 mỗi diff. Snapshot diff toàn PR gồm 100 đường dẫn, diff riêng packet gồm 52 đường dẫn theo phạm vi lọc. |

Harness sẵn có kiểm đúng một neo và chỉ cộng khi ca đích ném `TinHieuChotCa`. Tôi chạy lại bằng `python -B -m pdb … scripts/tl_core/llm_route_test.py`, đặt breakpoint có điều kiện tại dòng 1823. Rc trình gỡ lỗi 0, chương trình test thoát 0. Log `mutation-targets.log` có SHA-256 `ce170ee3a69d33ab5b0b900a5fddceef44e4939632effe5c26b5eb283ed07180`. [Harness](../scripts/tl_core/llm_route_test.py#L1803)

| Đột biến sẵn có | Điểm dừng quan sát được |
| --- | --- |
| `wp1525_dieu_phan_biet_hoa` | Tiêu đề Điều viết hoa ở cấp con lọt chốt trong `ca_cau_truc_docx_chan` (H1). |
| `wp1525_phan_chinh_mac_dinh` | Reader lấy nội dung từ part chính cũ trong `ca_cau_truc_docx_dat` (H2). |
| `wp1525_numid_style_loi_la_vang` | Câu dẫn có numId lỗi qua style lọt chốt trong `ca_cau_truc_docx_chan` (H4). |
| `wp1525_chu_sau_ngat_trang` | Chữ sau ngắt trang lọt chốt trong `ca_cau_truc_docx_chan` (H5). |
| `wp1525_tho_nhan_diem` | Điểm độc lập biến thành khoản ở đối chứng có đủ dấu câu trong `ca_wp1514_luot9`. Ca gốc kiểm cả nguồn có và mất số. |
| Ba đột biến H3 | Đổi lại tên cố định của part numbering và giữ nguyên abstractNumId đều làm đỏ đúng ca đích vì thiếu numId/cấp trong part đã chọn. Đột biến ghép điểm gõ tay chết ở assertion của ca dấu gạch. Rc trình gỡ lỗi và suite đều 0. `mutation-h3.log`, SHA-256 `0f314f95ee48564e785e280a5ee961859320ee76b4886f2a4b70813678655f1a`. |

Bản đột biến J4 chỉ thay một dòng trong clone tạm và dùng lại toàn suite. Tệp diff có SHA-256 `d23f682f8fadf3103a9bb6404c66d54088b218d514b3dd131346f8b58a2e5942`. Ca tiếp dòng “là” của nguồn có số có assertion sẵn trong `ca_ranh_gioi_luot4`. [Ca tiếp dòng](../scripts/tl_core/llm_route_test.py#L808)

Selftest có ghim chạy cùng môi trường từ 14:27:13 UTC và kết thúc lần lượt base 14:31:55, head 14:31:57. `diff -u` hai tập dòng `[FAIL]` trả rc 0. `diff -u` toàn bộ dòng `[OK]`/`[FAIL]` sau khi loại ca mới của head cũng trả rc 0. Tập đỏ gồm 8 `r973_bootstrap_*`, 5 `wp433_*`, `wp727_tl_gws_refresh` và 2 ca `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim`, `r268_l2_trichotomy_theo_trang_thai_object`. Mười bốn ca đầu trùng nhóm `/tmp/.git` rỗng đã nêu trong prompt. Hai ca sau cũng đỏ trên base và từng hiện diện trong verdict #1514. Sau khi ghim, `r218_docclaims_l2_sha_khong_ton_tai` và `r264_doc_claims_phu_docs` qua ở cả hai cây. Đây là kết quả selftest đỏ cùng nền, chênh lệch ca đỏ bằng 0. SHA-256 log head `d259bba60bccc6de1452eec2deaa7fb9621f1aee2ad7c761d635af9ce4c29353`, log base `800c746dfbefd5ce10f1a808f8e3da83347c08348eb9c59c225c843e99cb048d`. [Verdict #1514](../ops/acceptance/llm-ranh-gioi-khoan/r1/review-10-codex/VERDICT.md)

## Không đo được

- J1, J2, J3 và J5 là kết luận đọc mã. Kiểm cách Word áp cấp từ style, chọn nhánh markup tương thích, trình bày tiêu đề từ nhãn và hiển thị ngắt cạnh chữ đã bỏ cần nguồn hoặc ca mới. Lượt này dùng bộ test đã có. J4 có số đo đột biến trên bản sao.
- Danh sách §2.5 và các bổ sung đã bao các dạng bookmark, proofing, comment anchor, hyperlink, tab và dấu nối không ngắt nêu trong mã. Trường, hình, ký hiệu, chú thích, bảng, style-only và Strict bị chặn theo giới hạn đã khai. Chưa xác lập một phần tử thiếu thường gặp khác của Word/Google Docs từ hiện vật được giao. J5 là chặn oan do thứ tự lọc trên hai tính năng được hỗ trợ. Tần suất gặp trong bản export thực tế và nguyên nhân cụ thể của hai ca Git mini-repo còn đỏ chưa đo được. [Danh sách](../scripts/tl_core/llm_route.py#L529) · [Giới hạn người dùng](../docs/GOI_AGENT_DA_NEN.md#L390)
- `not_run` trong lượt đo offline này gồm `determinism-audit --strict`, `doc-claims-check --strict` độc lập, Ruff contract và Ruff lint. GitHub/CI và các lớp GitHub của kiểm lease cũng `not_run`. ADR-0060 M3 phân loại Windows là `required` do diff Python thêm dòng có `encoding=`, phép đo Windows bản địa `not_run`. Không ghi các phép này là `passed` hay `skipped`. [§5 của đặc tả](../ops/specs/llm-khoan-docx-r9.md#L165) · [ADR-0060 M3](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L48)
- Terminal status, mã thoát của tiến trình reviewer và băm stdout của launcher chỉ có thể đọc lại sau khi writer kết thúc. Báo cáo này neo vào run đang chạy và mã thoát thực của từng phép đo.

Readback cuối giữ nguyên exact head và tree ghi đầu báo cáo. Diff tracked và index đều rỗng. `.review/VERDICT.md` là tệp untracked duy nhất, `.codex/` rỗng đã hiện trong kiểm ignored đầu phiên. Snapshot xác nhận trạng thái ở hai mốc quan sát. Kết luận dưới đây là verdict review của exact SHA này. Với 3 P1 và 2 P2 mở, điều kiện merge M1 chưa đạt.

P2_mo: 2
VERDICT: REQUEST_CHANGES
