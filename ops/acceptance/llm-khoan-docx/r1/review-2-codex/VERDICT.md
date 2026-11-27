# Verdict packet #1525 r2 lượt 2 — Codex

reviewed_sha: 38c481f792b3f44d7500e93249153af63c0165db
reviewed_tree: 9ffe00f09df0fe612a5cbaa4e8ecf21bf61daa48

## Xác minh đầu vào

- Checkout detached của `ducthangho/tra-luat`, base/merge-base `64b7f2c14776d5d0e1d34a6be4725490956f5bec`, nền tiếp nối #1514 `fcb12b3873c3bec2c339029136243ed2c804ce05`. Git `core.abbrev=7`.
- Packet #1525 r2/g1, class `sensitive`, lời gọi 2/5. Blob `38c481f792b3f44d7500e93249153af63c0165db:ops/specs/llm-khoan-docx-r2.md` có OID `01de388eb69a00c1752e62e35d43f63dff2713c3`. SHA-256 của blob và bản làm việc cùng khớp lease `849aaaa56fd7cfda641b4a6c9a7c96638b3f8d5e92b1ed1ae9712f7aaa89e57b`.
- Reviewer `openai_codex / codex_cli / machine`, run `ec07f36a01cc49f584da76370958fe6c` theo launcher. SHA-256 prompt đúng với `run.json`. Lease khai executor `claude / claude_code / machine/local`.
- Hash write set tính lại theo các đường dẫn sắp xếp và kết thúc bằng LF khớp `48a5ec327076da9f7d7b21a6aa28e34fe435a38d67a5e99577818782f8d9ea2c`. Diff toàn PR có 65 đường dẫn. Diff `fcb12b3..HEAD` còn 17 đường dẫn sau khi bỏ bốn tệp hồ sơ #1514 theo prompt. Cả 17 thuộc lease r2. Diff vá `fa1e3d0..HEAD` có chín đường dẫn trong cùng write set.
- Chuỗi lease trên cùng nhánh `ccr-89c0d2e2-inanqb` khớp cả hai chiều `thay_the_cho` và `da_bi_thay_the` ở r9 #1514 ↔ r1 #1525 ↔ r2 #1525. Lease r2 hết hạn 17:07 UTC ngày 25-11-2026. [Lease r9](../ops/leases/llm-ranh-gioi-khoan-r9-g1-claude.yaml) · [Lease r1](../ops/leases/llm-khoan-docx-r1-g1-claude.yaml) · [Lease r2](../ops/leases/llm-khoan-docx-r2-g1-claude.yaml)
- Linux, Python 3.13.18, Git 2.43.0, Codex CLI 0.172.0. Sandbox `workspace-write`, checkout sản phẩm giữ nguyên tracked/index. Model và effort phục vụ là `KHONG_DO_DUOC` trong hồ sơ launcher đang chạy. Nguồn nhận dạng executor là lease và bản ghi giao việc.

## Đối chiếu lượt 1 và đặc tả r2

| Mục | Trạng thái | Bằng chứng |
| --- | --- | --- |
| §1, bất biến | Đạt trong phạm vi đã đo | Diff giữ bốn hàm gọi model và tập cờ CLI. Handler giữ `can_nguoi_duyet: true` và chọn đúng nhãn theo việc có danh sách khoản cấu trúc. Ca #1514 kiểm Điều 3 nguồn mất số và ba kết quả đã lưu, mỗi bản 8/8. Diff `tach_khoan` thay hai nhánh nhận nhiều dòng bằng nhánh chặn, giữ các chốt còn lại. [Handler](../scripts/tl_core/ops_misc.py#L3117) · [Ca đối chứng](../scripts/tl_core/llm_route_test.py#L1038) |
| A1 · §2.1, §2.4, vùng Điều | **VÁ MỘT PHẦN** | Nội dung trong `sdtContent` được giữ. Ca chặn xác nhận bảng trước fallback, hai tiêu đề, ngắt mềm ở tiêu đề đích và đoạn giống tiêu đề có số tự động. B1 còn đường cắt/gộp vùng và fallback sai. B2 còn lỗi đếm bảng lồng. B6 còn lỗi thuộc tính khối `customXml`. [Duyệt khối](../scripts/tl_core/llm_route.py#L693) · [Ca dương](../scripts/tl_core/llm_route_test.py#L1273) · [Ca chặn](../scripts/tl_core/llm_route_test.py#L1315) |
| A2 · §2.1, §2.4, số Word | **VÁ MỘT PHẦN** | Có bộ đếm riêng theo `numId`, đọc `start` và override, mặc định `start` vắng là 0, và kiểm nhãn cấp khoản theo chính cấp đó. Ca đã có xác nhận override 5→1, dãy nối từ Điều trước bị chặn, điểm đặt lại dưới khoản kế và hai danh sách trong Điều bị chặn. Chốt `lvlRestart`, `isLgl` bật và liên kết style của abstract được triển khai. B2 còn sai số vì cấp đánh số qua style và số lần duyệt. [Định nghĩa](../scripts/tl_core/llm_route.py#L576) · [Bộ đếm](../scripts/tl_core/llm_route.py#L782) · [Override](../scripts/tl_core/llm_route_test.py#L1277) |
| A3 · §2.4, từ nối | **ĐÃ VÁ THẬT** | Dò “là” ở chữ đoạn mở khoản. Ca đích có điểm nhãn chữ hoa cho kết quả lệch khi lấy từ nối của điểm, và đột biến trở lại dò cả khoản bị giết. Với nguồn so đúng, thứ tự, số lượng và toàn bộ hai vế đều được kiểm. B1 nói về dữ liệu đi vào đoạn mở khoản trước phép dò. [Phép so](../scripts/tl_core/llm_route.py#L1045) · [Ca A3](../scripts/tl_core/llm_route_test.py#L1286) |
| A4 · §2.1, §2.4, markup | **VÁ MỘT PHẦN** | Gọi bộ lọc chung trước khi dựng văn bản. Đọc gạch ngang theo namespace và style cho các dạng sẵn có, quét sửa dấu đoạn trên XML gốc. Ca dương giữ nguyên văn sau khi lọc gạch trực tiếp. Ca âm chặn gạch còn sót và sửa dấu đoạn. B3 còn bỏ sót một thuộc tính gạch đang hiệu lực. [Bộ lọc và dấu đoạn](../scripts/tl_core/llm_route.py#L755) · [Ca A4](../scripts/tl_core/llm_route_test.py#L1328) |
| A5 · §2.4, danh sách ngoài Điều | **ĐÃ VÁ THẬT** cho biểu hiện đã báo | Danh sách không hỗ trợ mang lý do riêng. Việc xác thực và dựng nhãn chỉ diễn ra cho danh sách được dùng trong Điều đích. Ca dương có danh sách độc lập ngoài Điều chứa override lạ và cấp số La Mã. [Phạm vi kiểm](../scripts/tl_core/llm_route.py#L830) · [Ca A5](../scripts/tl_core/llm_route_test.py#L1282) |
| A6 · §2.4, điểm gõ tay | **ĐÃ VÁ THẬT** | Dấu điểm liền thân được nối vào khoản đang mở, giữ dấu và xuống dòng. Ca dương bao phủ cả dấu chữ và dấu gạch, đột biến đòi khoảng trắng bị giết. Câu dẫn chỉ bỏ khi vắng hoặc đúng một đoạn khớp toàn câu chuẩn ở trước khoản đầu. [Xử lý điểm](../scripts/tl_core/llm_route.py#L845) · [Ca A6](../scripts/tl_core/llm_route_test.py#L1269) · [Câu dẫn](../scripts/tl_core/llm_route.py#L876) |
| §2.2, CLI và fallback | Đúng định tuyến tại handler, còn B1–B4 về nguồn so | Chữ ký ZIP chọn đường cấu trúc, yêu cầu `--dieu`, cấm ghép số hiệu. Các lỗi đọc cấu trúc được đổi thành rc 2. Chỉ `KhongCauTruc` chuyển sang đường thô. `--out` chỉ ghi khi danh sách lệch rỗng. [Định tuyến](../scripts/tl_core/ops_misc.py#L3027) · [Ghi đầu ra](../scripts/tl_core/ops_misc.py#L3130) |
| K1 · §2.3, đường thô | **ĐÃ VÁ THẬT** cho cả hai nhánh K1 | Dòng điểm khớp `_RE_DIEM` trả `None` trên cả nguồn có số và mất số. Ở nguồn có số, dòng tiếp mở bằng “là” rơi vào nhánh từ chối dòng không số. Ở nguồn mất số, dòng như vậy qua bộ tách dưới dạng một mục nhưng phép so loại vì thiếu vế thuật ngữ. [Bộ tách](../scripts/tl_core/llm_route.py#L914) · [Kiểm hai vế](../scripts/tl_core/llm_route.py#L1067) |
| A7 · §2.4 và §3, test | **VÁ MỘT PHẦN** | Override khác giá trị gốc, điểm gõ tay, bảng khi fallback và một số đột biến đích đã có. Chốt bảng-trước-fallback vẫn thiếu đột biến độc lập. Còn các nhánh bắt buộc chưa có cặp mẫu/đột biến ở B7. [Ca DOCX](../scripts/tl_core/llm_route_test.py#L1247) · [Bảng DOT_BIEN](../scripts/tl_core/llm_route_test.py#L1384) |
| A8 · §2.4, hướng dẫn đường thô | **ĐÃ VÁ THẬT** | Hướng dẫn thống nhất nguyên tắc mỗi khoản một dòng. Chỗ lặp lại cũng nêu cùng quy tắc. B8 ghi lỗi riêng ở đoạn mô tả đường cấu trúc. [Hướng dẫn](../docs/GOI_AGENT_DA_NEN.md#L373) |

**Phần còn lại của lớp `ranh-gioi-khoan` trên đường thô.** Sau khi mất bố cục, một lời dẫn nhóm hoặc các dòng vốn cùng một khoản có thể qua nếu từng dòng trông như một định nghĩa hoàn chỉnh, có hai vế và dấu kết câu. Với nguồn có số, một mục con mất thụt lề có thể mang đúng hình số khoản kế tiếp nếu dãy còn liên tục và mục trước đã đủ điều kiện kết câu. Đây là giới hạn phân đoạn thô đã nêu. B1 ghi đường `.docx` làm mất ranh giới trước khi bộ quét thô nhìn thấy chữ. [Phạm vi kết quả](../scripts/tl_core/llm_route.py#L887) · [Verdict lượt 1](../ops/acceptance/llm-khoan-docx/r1/review-1-codex/VERDICT.md)

## Findings

Các đường đi dưới đây được đối chiếu trên mã của exact head. Hạng P1 áp khi oracle của đường cấu trúc có thể sai mà phép so vẫn cho rc 0 hoặc ghi `--out`. Hạng P2 áp cho từ chối đầu vào hợp lệ hoặc thiếu phép kiểm bắt buộc. Hạng P3 áp cho sai lệch hướng dẫn. [Protocol §8 và §8.3](../docs/PROTOCOL_DA_PHIEN.md#L634) · [ADR-0060 M1–M2](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32)

### B1 [P1] Vùng Điều vẫn có thể mất hoặc gộp khoản trước phép so — `scripts/tl_core/llm_route.py:736,803,825`

- **Kịch bản và căn cứ.** Một đoạn có thể chứa thân khoản rồi ngắt dòng mềm trước một khoản gõ số tay cùng đoạn. Parser đổi `br/cr` thành dấu cách. Nó chỉ dùng cờ `ngat` ở tiêu đề đích, còn chốt số gõ tay chỉ nhìn đầu đoạn. Đường cấu trúc có thể nhận hai khoản thành một. Nếu toàn vùng vốn dùng số tay, chốt đánh số nội dòng của đường thô bắt được nhiều trường hợp. Tuy nhiên, khi hai dòng đầy đủ đã mất số, quá trình chuyển sang `KhongCauTruc` có thể gộp chúng trước khi `tach_khoan` đọc. Đầu ra chép đúng khoản đã gộp sẽ khớp hai vế.
- **Kịch bản và căn cứ.** Với tiêu đề đích chứa cả thân khoản trên cùng dòng, regex chỉ khớp tiền tố. Toàn bộ tiêu đề bị loại khỏi danh sách khoản so sánh. Nếu các đoạn sau tạo được một dãy hợp lệ, phép so có thể qua với phần thân bị bỏ. Một tiêu đề ghép như vậy bị chặn khi chuyển đúng sang đường thô vì đường đó kiểm cả dòng. Ranh giới kết thúc cũng được quyết trước khi kiểm `con_bo`, nên một đoạn mở giống tiêu đề còn chứa markup bỏ sót có thể cắt ngắn Điều. Ngoài ra, đoạn đánh số có chữ rỗng bị loại trước khi tạo `co_so`. Khi đó vùng vẫn có số tự động nhưng có thể bị chuyển sang đường thô, trái điều kiện §2.1 của `KhongCauTruc`.
- **Đề xuất.** Xác minh cả đoạn làm tiêu đề và đoạn dùng làm ranh giới. Giữ hoặc từ chối ngắt mềm có nội dung khi chúng che ranh giới. Quyết đường fallback trên các đoạn đánh số trước bước bỏ chữ rỗng. Đối chứng việc có hay không có dấu ngắt, chữ đánh dấu bỏ và đoạn đánh số rỗng. [Đọc ngắt](../scripts/tl_core/llm_route.py#L736) · [Cắt vùng và fallback](../scripts/tl_core/llm_route.py#L803) · [Chốt tiêu đề thô](../scripts/tl_core/llm_route.py#L905)

### B2 [P1] Cấp gắn với style và lượt duyệt bảng lồng làm sai bộ đếm Word — `scripts/tl_core/llm_route.py:591,702,743`

- **Kịch bản và căn cứ.** Danh sách nhiều cấp của Word có thể liên kết paragraph style với cấp bằng `w:lvl/w:pStyle`. Khi đánh số đến từ paragraph style, liên kết đó chọn cấp hiển thị. Parser chỉ lấy `numId` và `ilvl` theo `basedOn`, mặc định cấp 0 khi thiếu `ilvl`. Nó không đọc `w:lvl/w:pStyle`. Một điểm liên kết với cấp con, có nội dung đủ hai vế, có thể bị bộ đếm xếp thành khoản mới. Dãy giả vẫn liên tục và mục đúng phía sau bị đổi số. Ca style sẵn có chỉ đi qua cấp 0.
- **Kịch bản và căn cứ.** `el.iter(w:tc)` lấy cả ô bảng lồng. Gọi đệ quy từ ô ngoài đã duyệt bảng lồng, sau đó vòng ngoài duyệt lại ô lồng. Đoạn trong ô bị đếm hai lần và có thể sai thứ tự so với đoạn sau bảng lồng trong cùng ô. Bảng trước Điều không bị chốt cấm bảng trong vùng chặn. Ví dụ bằng lời, danh sách bắt đầu từ 0 và mục số 0 nằm trong bảng lồng trước Điều. Khoản hiển thị số 1 đầu Điều bị nâng thành 2 và bị chặn oan. Một khối chưa hiểu nằm trước Điều cũng có thể che một mục của cùng `numId`, làm sai theo chiều ngược lại do khối lạ chỉ mang sentinel.
- **Đề xuất.** Giải quyết cấp theo liên kết style của danh sách, hoặc dừng khi gặp cách gán cấp chưa hỗ trợ. Duyệt từng hàng và ô đúng một lần. Trước khi xác nhận số hiển thị, xác minh các khối trước Điều có thể ảnh hưởng danh sách đang dùng. Đo cùng bộ dữ liệu với cấp trực tiếp, cấp qua style, bảng lồng và nhiều `numId`. [Đọc định nghĩa](../scripts/tl_core/llm_route.py#L586) · [Duyệt bảng](../scripts/tl_core/llm_route.py#L693) · [Số hiệu lực](../scripts/tl_core/llm_route.py#L743)

### B3 [P1] Tắt gạch đơn có thể che gạch kép còn hiệu lực — `scripts/tl_core/llm_route.py:638,724`

- **Kịch bản và căn cứ.** Run thừa hưởng gạch kép từ character style, còn định dạng trực tiếp chỉ tắt gạch đơn. Bộ lọc chung chỉ nhìn định dạng trực tiếp trong run, nên giữ chữ. Bộ đọc gộp `strike` và `dstrike` của style thành một cờ. Khi gặp `strike` tắt trực tiếp, nó ghi đè cờ và bỏ mất gạch kép đang hiệu lực. Chữ gạch kép còn được nối vào oracle và có thể được nhận là nguyên văn. Tương tự, ở tiền tố khác, thuộc tính gạch đơn bật có thể bị ghi đè bởi gạch kép tắt. Bộ đọc cũng chưa nạp mặc định run từ `docDefaults`.
- **Đề xuất.** Tính hiệu lực riêng cho từng thuộc tính xuyên qua các tầng hợp lệ, rồi mới quyết có chữ bị gạch còn sót. Chặn kiểu định dạng không giải quyết được theo hợp đồng. Đối chứng gạch đơn tắt với gạch kép bật, đổi tiền tố và style mặc định. [Gộp thuộc tính style](../scripts/tl_core/llm_route.py#L638) · [Ghi đè thuộc tính run](../scripts/tl_core/llm_route.py#L724) · [Bộ lọc trực tiếp](../scripts/docx_markup.py#L74)

### B4 [P1] Dấu nối không ngắt dòng của Word biến mất khỏi nguyên văn — `scripts/tl_core/llm_route.py:720,736`

- **Kịch bản và căn cứ.** Dấu nối không ngắt có thể nằm trong run dưới dạng `w:noBreakHyphen`, giữa hai phần chữ. Bộ đọc chỉ nối `w:t` và ánh xạ một số tab/ngắt dòng. Dấu nối biến mất, hai phần chữ bị dính và phép so có thể nhận kết quả đã mất dấu. Cùng bộ đọc cấp chữ cho đường cấu trúc và `KhongCauTruc`. Việc bỏ dấu này khác với chuẩn hóa khoảng trắng mà phép so cho phép.
- **Đề xuất.** Ánh xạ phần tử hiển thị theo Word hoặc dừng với dạng chưa hiểu. Kiểm cả ký tự hiển thị ngoài `w:t` và chọn đúng nội dung khi một run có các nhánh trình bày thay thế. [Trích chữ](../scripts/tl_core/llm_route.py#L720) · [So nguyên văn](../scripts/tl_core/llm_route.py#L1058)

### B5 [P2] Thân định nghĩa mở bằng số thập phân bị coi là số khoản gõ tay — `scripts/tl_core/llm_route.py:527,857`

- **Kịch bản và căn cứ.** Một mục danh sách tự động mở bằng tên đại lượng hoặc một ký hiệu dạng số thập phân dùng dấu chấm. Mẫu DOCX khớp dãy số và dấu chấm, rồi chặn ngay cả khi dấu chấm đi liền chữ số tiếp theo. Mẫu số thô có điều kiện bảo vệ dạng thập phân. Nguồn DOCX hợp lệ bị rc 2, trong khi giới hạn đã khai là số thứ tự gõ tay lẫn số tự động.
- **Đề xuất.** Phân biệt dấu số thứ tự với dấu chấm thập phân. Giữ đối chứng chặn số gõ tay và chấp nhận số thập phân đầu thân. [Hai mẫu số](../scripts/tl_core/llm_route.py#L490) · [Nhánh từ chối](../scripts/tl_core/llm_route.py#L856)

### B6 [P2] Metadata hợp lệ trong `customXml` làm cả Điều bị chặn — `scripts/tl_core/llm_route.py:708,821`

- **Kịch bản và căn cứ.** Khối `w:customXml` có thể chứa `w:customXmlPr` mô tả chính wrapper trước các đoạn. Khi đi vào toàn bộ con của wrapper, bộ đọc biến metadata thành một khối lạ. Một Điều có các đoạn và danh sách được hỗ trợ bên trong wrapper đó bị rc 2, dù §2.4 nêu hỗ trợ đi vào `w:customXml`.
- **Đề xuất.** Bỏ qua phần thuộc tính tại đúng vị trí và giữ fail-closed cho khối chứa nội dung chưa hỗ trợ. Đối chứng cùng khoản có và không có metadata wrapper. [Duyệt wrapper](../scripts/tl_core/llm_route.py#L704) · [Chặn khối lạ](../scripts/tl_core/llm_route.py#L820)

### B7 [P2] Các chốt bắt buộc còn thiếu phép đột biến độc lập — `scripts/tl_core/llm_route_test.py:1293,1386`

- **Kịch bản và căn cứ.** Đột biến bảng hiện bỏ toàn bộ chốt loại khối. Ca đích dừng ở assertion bảng có số, đứng trước ca bảng khi fallback. Con số đột biến bị giết vì vậy chưa chứng minh thứ tự chặn bảng trước fallback. Bộ ca còn thiếu cặp mẫu và đột biến riêng cho `numFmt` không hỗ trợ ở điểm cấp con, tiêu đề đích đánh số tự động và liên kết `numStyleLink/styleLink`. Ca `lowerLetter` ở cấp khoản đo chốt cấp khoản phải decimal. Ca danh sách La Mã có override lạ ngoài Điều đo phạm vi xác thực.
- **Đề xuất.** Tách đột biến chỉ đưa fallback qua chốt bảng, thêm đối chứng theo từng nhánh nêu trên và yêu cầu chính assertion đích giết đột biến. Hạng P2 vì §2.4 A7 và §3 đặt đây là điều kiện nghiệm thu riêng. [Ca chặn](../scripts/tl_core/llm_route_test.py#L1293) · [Bảng đột biến](../scripts/tl_core/llm_route_test.py#L1384) · [Đặc tả](../ops/specs/llm-khoan-docx-r2.md#L59)

### B8 [P3] Hướng dẫn DOCX vẫn ghi chặn đánh số qua style — `docs/GOI_AGENT_DA_NEN.md:390`

Hướng dẫn liệt kê “đánh số qua style” trong các trường hợp rc 2. §2.4 A2 đã thay quy tắc đó và ca dương đã kiểm một style gián tiếp qua `basedOn`. Người dùng có thể bỏ qua một nguồn hợp lệ. Cập nhật phần hướng dẫn theo quy tắc r2 khi chốt lại phạm vi style được hỗ trợ. [Hướng dẫn](../docs/GOI_AGENT_DA_NEN.md#L390) · [Đặc tả r2](../ops/specs/llm-khoan-docx-r2.md#L50)

### Lịch sử theo lớp

| Slug lớp | Biểu hiện và hạng còn mở | Nguồn, cách đóng và phần chưa đo |
| --- | --- | --- |
| `ranh-gioi-khoan` | K1 đóng trên đường thô, A3 đóng, A1 còn B1 · P1 | K1 ở `fcb12b3`, A1/A3 ở `3d24751`. Xác minh ranh giới trước khi bỏ tiêu đề hoặc tạo đầu khoản. Đối chứng ngắt mềm, markup ở điểm cắt, đoạn đánh số rỗng và fallback. |
| `docx-so-hien-thi` | A2 còn B2 · P1 | Từ `3d24751`. Xác minh cấp hiệu lực và bộ đếm Word, gồm trường hợp bảng lồng trước Điều. |
| `docx-markup-du-thao` | A4 còn B3 · P1 | Từ `3d24751`. Xác minh hai loại gạch qua định dạng trực tiếp và style. |
| `docx-kiem-danh-sach-ngoai-vung` | A5 đóng | Từ `3d24751`. Ca dương danh sách độc lập ngoài Điều đạt. |
| `docx-dau-diem-go-tay` | A6 đóng | Từ `3d24751`. Hai dạng dấu liền chữ đạt và đột biến bị giết. |
| `do-phu-chot-docx` | A7 còn B7 · P2 | Từ `3d24751`. Bổ sung từng cặp mẫu và đột biến đúng nhánh. |
| `huong-dan-duong-tho` | A8 đóng | Từ `3d24751`. Đối chiếu quy tắc một dòng trong hướng dẫn với §2.3 và mã. |
| `docx-chu-hien-thi` | B4 · P1 | Mới ở lượt 2. Đối chứng dấu nối word run và so đúng ký tự hiển thị. |
| `docx-nhan-dien-so-go-tay` | B5 · P2 | Mới ở lượt 2. Đối chứng dấu chấm thập phân và dấu phân cách số thứ tự. |
| `docx-khoi-customxml` | B6 · P2 | Mới ở lượt 2. Metadata wrapper phải qua, khối chứa nội dung chưa hiểu phải bị chặn. |
| `huong-dan-duong-docx` | B8 · P3 | Mới ở lượt 2. Đồng bộ hướng dẫn với phạm vi style thực tế. |

Đóng 4/8 mục A1–A8 và 3/7 lớp còn mở ở cuối lượt 1. Có bốn lớp mới và tám finding còn mở ở lượt 2. Lớp `ranh-gioi-khoan` đã qua Review Rescue Checkpoint ở #1514 và còn biểu hiện trên đường cấu trúc qua cả hai lượt #1525. Giữ lịch sử lớp khi xét hướng tiếp theo. [Protocol §8.3](../docs/PROTOCOL_DA_PHIEN.md#L812) · [Protocol §12](../docs/PROTOCOL_DA_PHIEN.md#L1097)

## Kết quả test và đột biến

Chạy với `PYTHONDONTWRITEBYTECODE=1`. Log và mã thoát từng lệnh ở `/tmp/wp1525-review-kwRnqu/`. Bảng băm `logs.sha256` có SHA-256 `ba9bfd88593b40d467e4078b1a7910c8e7ee06a3f8c2c91c9ad1e9ed9538b8ce`.

| Lệnh | Trạng thái | Mã thoát và bằng chứng |
| --- | --- | --- |
| `python scripts/tl_core/llm_route_test.py` | `passed` | rc 0, **58/58** ca, **127/127** đột biến bị giết, gồm **30/30** mục `wp1525_*`. Runner chỉ tính chết khi chính ca đích ném `TinHieuChotCa`. Mỗi đột biến chạy trên module ở thư mục tạm do runner tạo. `llm.log`. |
| `python scripts/tl.py --deterministic workflow-audit --strict --json` | `passed` | rc 0, `ok=true`, 26 card, 60 task, 194 lệnh, 0 lỗi và 0 cảnh báo. `workflow.log`. |
| `python scripts/tl.py --deterministic golden-test --json` | `passed` | rc 0, `ok=true`, 20/20 ca và 20/20 bản chiếu ổn định, 19/20 raw ổn định. `hygiene_sweep_fixture` chỉ lệch `snapshot_age_s`, đúng khóa volatile đã khai, 0 khóa lệch ngoài khai báo. `golden.log`. |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | `passed` ở bản sao sạch của exact head | rc 0, `ok=true`, 187/187 tệp, package hash khớp, 0 thiếu/thừa/sai. Lần đầu trên checkout review rc 2 vì `.review/VERDICT.md` được ghi sớm và bị tính là một tệp thừa. `release-clean.log`, `release.log`. |
| `python ops/lease_publish.py check --root . ops/leases/llm-khoan-docx-r2-g1-claude.yaml` | `passed` cục bộ | rc 0, “ĐĂNG ĐƯỢC”, Issue #1525, neo `64b7f2c14776`, hạn 17:07 UTC. Hai lớp kiểm GitHub nằm ngoài lệnh `check`. `lease.log`. |
| `python scripts/tl.py --selftest` ở head | `failed` | rc 1, **1774/1790**, 16 ca đỏ. Ca mới `r1525_llm_khai_niem_tep_docx_cau_truc` đạt, kiểm handler với model giả qua rc 0/5/2 và metadata. `self-head.log`. |
| `python scripts/tl.py --selftest` ở base | `failed` | rc 1, **1773/1789**, cùng 16 ID đỏ. Mọi dòng trạng thái chung khớp, dòng thêm duy nhất là ca DOCX mới đạt ở head. `self-base.log`. |
| `python scripts/tl.py --deterministic determinism-audit --strict --json` | `passed` | rc 0, `ok=true`, 15/15 check. `determinism.log`. |
| `python scripts/tl.py doc-claims-check --strict --json` ở head và base | `failed` cả hai lượt | rc 2 ở mỗi SHA. Cùng cờ `SHA_NOT_A_COMMIT` cho `9941d8af52aeede1c78ea4e232fbe9a8d5272033` ở protocol dòng 1680. `git cat-file -t` rc 128 trong bản sao được giao. `claims.log`, `claims-base.log`. |
| Probe `loi_ruff_ci()` trong `.claude/dev/ci_dang_ky_test.py` theo adapter | `passed` | rc 0, `RUFF_CONTRACT 3 []`. Đây là phép đo pin/probe của workflow. `ruff-contract.log`. |
| `ruff check --no-cache --select F scripts/tl.py` ở head và base | `failed` thô, đạt tiêu chí delta | Ruff 0.16.9, rc 1 cả hai, cùng 12 F821 và 0 F401, log khớp byte. Delta 0. `ruff-head.log`, `ruff-base.log`. |
| `git diff --check fcb12b3 HEAD` | `passed` | rc 0, không có cảnh báo trong delta lần này. |
| `git diff --check 64b7f2c HEAD` | `failed` | rc 2, ba dòng trailing whitespace trong biên bản #1514 lượt 8. Log khớp với phép đo `64b7f2c..fcb12b3`. `diff-check-pr.log`, `diff-check-prior.log`. |

Trong 16 ID selftest đỏ ở cả hai SHA, 14 ID khớp nhóm môi trường prompt đã báo với `/tmp/.git` rỗng, gồm tám `r973_bootstrap_*`, năm `wp433_*` và `wp727_tl_gws_refresh`. Hai ID còn lại là `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` và `r268_l2_trichotomy_theo_trang_thai_object`. So tập ID đỏ cho delta 0. Selftest N/N và `doc-claims-check --strict` vẫn chưa đạt theo §5. Sáu lệnh trong prompt đều đã chạy và không có lệnh nào mang trạng thái `skipped`.

## Không đo được

- B1–B6 là kết luận từ đường đi trong mã. Chưa có phép chạy trực tiếp các kịch bản đó trên tài liệu Word hoặc Google Docs, cũng chưa đo tần suất hay tỷ lệ chặn oan trên corpus. Ngoài ca mặc định đang có, kiểu restart ở các cấp bỏ bước và nhãn chữ ngoài 26 mục chưa được đối chiếu với văn bản do Word hiển thị. Lượt này dùng ca và đột biến sẵn có.
- Windows `required` theo ADR-0060 M3. Diff toàn PR thêm dòng dùng `encoding=` trong selftest và kế thừa phạm vi Windows của #1514 đã ghi ở verdict lượt 10. Windows local, Windows CI và provenance CI trên exact head là `not_run` trong lượt offline này. [ADR-0060 M3](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L43) · [Verdict #1514](../ops/acceptance/llm-ranh-gioi-khoan/r1/review-10-codex/VERDICT.md#L82)
- Xác minh GitHub, đường model thật và LIVE là `not_run`. Rc con và SHA-256 stdout terminal của launcher chỉ đo được sau khi writer kết thúc. Hồ sơ chạy tại thời điểm xuất verdict báo `dang_chay`.

## Readback và kết luận

HEAD và tree cuối khớp đầu lượt. `git diff --exit-code` và `git diff --cached --exit-code` đều rc 0. Tôi đã chuyển fixture và state ignored do bộ test sẵn có sinh trong checkout sang scratch. Status cuối chỉ còn `.review/VERDICT.md` và thư mục `.codex/` rỗng có từ đầu. Snapshot chứng minh delta quan sát được ở hai mốc. Checkout executor nằm ngoài phạm vi quan sát.

Còn **0 P0 · 4 P1 · 3 P2 · 1 P3**. **CHƯA ĐỦ ĐIỀU KIỆN MERGE** theo ADR-0060 M1 và các gate ghi trên. [ADR-0060 M1](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32)

P2_mo: 3

VERDICT: REQUEST_CHANGES
