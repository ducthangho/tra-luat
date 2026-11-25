# Verdict packet #1525 r5 lượt 5 — Codex

reviewed_sha: 3c1e1436996468419875d05a7adefe8d5bd21a76

reviewed_tree: 4dd50a1bb7d376331e80058e4e55e5d507b28104

base_sha: 64b7f2c14776d5d0e1d34a6be4725490956f5bec

## Preflight

- Checkout riêng ở detached HEAD, origin `ducthangho/tra-luat`, base là merge-base. Hai mốc đọc diff là `fcb12b3873c3bec2c339029136243ed2c804ce05` cho #1525 và `571c6754820887afccc64322fddaa0d124a659e4` cho bản vá r5. Toàn PR có 80 đường dẫn. R5 có 9 đường dẫn. Diff #1525 có 32 đường dẫn sau khi bỏ hồ sơ #1514 như prompt chỉ định. Cả 32 thuộc write set của lease r5. Băm write set là `3aee8cbb884be0fd21beb564edd0901c38b2e47764d6584166d0cdc5999f75b7`.
- Nguồn đặc tả là blob `c51f0d4bc44c889e0d2d86bb5e5b2a1bdae58232` tại exact head, đường dẫn `ops/specs/llm-khoan-docx-r5.md`. SHA-256 của blob và tệp checkout đều bằng `339bd40626c3bc1f72265ac6475741cc3650f6f45bccb08c77dd598ec5d4172b`, khớp lease revision 5, generation 1, effective Review Class `sensitive`. Năm cặp kề trong chuỗi #1514 r9 → #1525 r1 → r2 → r3 → r4 → r5 khớp hai chiều `thay_the_cho` và `da_bi_thay_the`. R5 còn hạn tới 18:06 UTC ngày 25-11-2026 khi kiểm. [Đặc tả](../ops/specs/llm-khoan-docx-r5.md) · [Lease](../ops/leases/llm-khoan-docx-r5-g1-claude.yaml)
- Reviewer `openai_codex / codex_cli / machine`, họ `openai`, run `b92db2b35ac8468596d0a09c00881933`, theo prompt và metadata launcher cùng run. Sandbox thực tế `workspace-write`, mạng hạn chế, approval `never`. Model và effort phục vụ `KHONG_DO_DUOC`. Executor theo lease là `anthropic_claude / claude_code / machine/local`, họ `claude`, phiên điều phối ghi `session_015GtxrZQYT3Vt8PJdXrjEKg`. Lượt review 5/5.

## Đối chiếu lượt 4 và đặc tả r5

Lượt 1–4 lần lượt neo `3d247516aaeb0ad3d836a2dc51dda13052fdbe47`, `38c481f792b3f44d7500e93249153af63c0165db`, `b0f3cb9ea1cca141f12eb462ced60f949d1ed0a4` và `fa3a8e2047ccbdb4c20eb11f117732658a653b92`. [Lượt 1](../ops/acceptance/llm-khoan-docx/r1/review-1-codex/VERDICT.md) · [Lượt 2](../ops/acceptance/llm-khoan-docx/r1/review-2-codex/VERDICT.md) · [Lượt 3](../ops/acceptance/llm-khoan-docx/r1/review-3-codex/VERDICT.md) · [Lượt 4](../ops/acceptance/llm-khoan-docx/r1/review-4-codex/VERDICT.md)

| Mục | Trạng thái | Bằng chứng |
| --- | --- | --- |
| D1 · A1/B1/C1 · §2.7 | **VÁ MỘT PHẦN** | Đã bỏ `KhongCauTruc`. Điều không có numbering tự động trả lỗi cấu trúc, CLI trả rc 2. Sau mốc cắt, cùng `numId` bị chặn với cả tiền tố Điều và Chương. Đột biến `wp1525_nhan_khoan_tiep_sau_cat` bị giết. Điểm gõ tay hoặc danh sách khác phía sau vẫn có thể bị mất. Xem E1. [Điểm cắt và guard](../scripts/tl_core/llm_route.py#L921) · [Ca D1](../scripts/tl_core/llm_route_test.py#L1433) |
| D2 · A2/B2/C2 · §2.7 | **ĐÃ VÁ THẬT** với reset section | `restartNumberingAfterBreak` bật làm định nghĩa được đánh dấu không hỗ trợ. Fixture dùng namespace Word 2012 và đột biến `wp1525_nhan_restart_section` bị giết. Lớp số hiển thị còn E3, ở đầu vào của bộ đếm. [Đọc định nghĩa](../scripts/tl_core/llm_route.py#L574) · [Ca D2](../scripts/tl_core/llm_route_test.py#L1438) |
| D3 · A4/B3/C4 · §2.7 | **VÁ SINH LỖI MỚI** | Chính xác lỗi regex cũ đã rời đường DOCX. Chốt dấu đoạn đọc XML gốc. Đối chứng gạch trực tiếp, namespace khác, style kế thừa, gạch kép và tắt trực tiếp đều đạt. Khi chuyển từ từ chối sang bỏ chữ, phép OR qua chuỗi style có thể xóa chữ còn hiệu lực. Hai đột biến bổ sung về D3 còn sống. Xem E2 và E5. [Duyệt run](../scripts/tl_core/llm_route.py#L772) · [Ca markup](../scripts/tl_core/llm_route_test.py#L1386) |
| D4 · A7/B7/C6 · §2.7 | **ĐÃ VÁ THẬT** với hai đột biến đã báo | Hai mẫu tách biệt đo tiêu đề khớp nhưng có phần tử lạ và phần tử lạ ở cấp hàng trước Điều. `wp1525_nhan_tieu_de_la` và `wp1525_bang_la_bo_qua` đều bị giết. E4 là chặn oan ở cấp ô. E5 là độ phủ của phần lọc markup. [Mẫu D4](../scripts/tl_core/llm_route_test.py#L1442) · [Bảng đột biến](../scripts/tl_core/llm_route_test.py#L1537) |
| D5 · §2.7 | **ĐÃ VÁ THẬT** theo giới hạn r5 | Chỉ nhận gốc WordprocessingML Transitional. Strict nhận chẩn đoán nêu rõ định dạng. `wp1525_nhan_strict` bị giết. R5 đã công bố giới hạn. [Cửa namespace](../scripts/tl_core/llm_route.py#L866) · [Ca Strict](../scripts/tl_core/llm_route_test.py#L1285) |
| D6 · A3/C3 · §2.7 | **ĐÃ VÁ THẬT** | Chốt phân cách gỡ tiền tố ở đúng đoạn đã được xếp là điểm gõ tay. Đoạn đánh số tự động mở bằng tiền tố điểm bị chặn nếu còn ngoặc đóng lẻ. `wp1525_go_dau_diem_moi_doan` bị giết. Từ nối chỉ lấy từ đoạn mở khoản, kể cả khi điểm có chữ “là”. [Phân vai và kiểm](../scripts/tl_core/llm_route.py#L974) · [Guard](../scripts/tl_core/llm_route.py#L1012) · [Ca D6](../scripts/tl_core/llm_route_test.py#L1445) |
| §1 · bất biến | Đạt trong phạm vi kiểm | Hai đường luôn trả `can_nguoi_duyet: true` và gắn phạm vi theo ranh giới thật sự được dùng. Code gọi model và tập cờ CLI giữ nguyên. Ba kết quả lưu Điều 3 Luật 134/2025/QH15 đều đạt 8/8 trong ca hồi quy hiện có. [Handler](../scripts/tl_core/ops_misc.py#L3123) · [Fixture](../scripts/tl_core/llm_route_test.py#L1060) |
| §2.1 · §2.4–§2.6 | **VÁ MỘT PHẦN** | ZIP/XML dùng thư viện chuẩn và reader có trần. Đã đo `start=0`, `startOverride` khác `start`, reset cấp con, bảng lồng/wrapper, nhãn chữ sau Z và nhiều `numId` trong vùng. Hai `numId` trong vùng bị chặn. Ngữ pháp nhãn khoản chỉ là số của cấp đó với dấu chấm hoặc ngoặc đóng. A5 giữ đối chứng danh sách lạ độc lập ngoài Điều. A6 giữ điểm gõ tay dính thân. B4/B5/B6/C5 giữ các đối chứng dấu nối, thập phân, metadata wrapper và content control nội dòng. Vùng trước Điều còn E3/E4. [Bộ đếm](../scripts/tl_core/llm_route.py#L878) · [Ca dương](../scripts/tl_core/llm_route_test.py#L1247) |
| §2.2 · CLI | Đạt định tuyến | ZIP magic vào DOCX, yêu cầu `--dieu`, cấm kèm số hiệu. DOCX mơ hồ trả rc 2 ngay tại handler. `--tep` UTF-8 và `<số hiệu>` vẫn chọn văn bản thô. `--out` chỉ ghi khi phép so hết lệch. [Handler](../scripts/tl_core/ops_misc.py#L3025) · [Cửa ghi](../scripts/tl_core/ops_misc.py#L3127) |
| §2.3 · K1 | **ĐÃ VÁ THẬT** cho hai đường đã báo | Mọi dòng khớp `_RE_DIEM` bị từ chối dù nguồn có số hay mất số. Dòng tiếp mở bằng “là” ở nguồn có số trả `None`. Ở nguồn mất số, nó thành một ứng viên có vế thuật ngữ rỗng và phép so báo lệch. Số nhìn thấy vẫn phải liên tục từ 1. Ca Q3, ca có điểm ở hai loại nguồn và đột biến `wp1525_tho_nhan_diem` đạt. A8/B8/C7 được phản ánh trong hướng dẫn hiện hành. [Quét thô](../scripts/tl_core/llm_route.py#L1042) · [Ca Q3](../scripts/tl_core/llm_route_test.py#L808) · [Hướng dẫn](../docs/GOI_AGENT_DA_NEN.md#L373) |
| §3 · A7/B7/C6 | **VÁ MỘT PHẦN** | 59/59 ca, 155/155 đột biến có sẵn, gồm 58 `wp1525_*`. Các mẫu D4 đạt tiêu chí chốt riêng. Hai đột biến bổ sung trên bản sao vẫn sống. Xem E5 và bảng kết quả. [Runner](../scripts/tl_core/llm_route_test.py#L1717) |

**Câu dẫn và phép so.** DOCX chỉ bỏ một câu dẫn khớp toàn đoạn, đặt trước khoản đầu, hoặc chấp nhận khi vắng. Đường thô chỉ bỏ ở dòng đầu sau tiêu đề. Trên danh sách khoản đã dựng, phép so buộc số, thứ tự và số lượng mục, rồi so đủ hai vế theo vị trí từ nối, giữ xuống dòng. Sai sót còn mở xảy ra trước phép so, khi dựng nguồn đối chiếu. [Câu dẫn](../scripts/tl_core/llm_route.py#L1008) · [So nguyên văn](../scripts/tl_core/llm_route.py#L1182)

**Giới hạn còn lại của đường thô.** Các ranh giới thực đã mất khi flatten vẫn không suy ra được nếu mỗi dòng còn lại tự có đủ hình thức một định nghĩa. Đây là giả định một dòng một khoản đã khai, khác hai nhánh ghép dòng K1. Với tệp TXT đã mất định dạng, bộ so cũng không biết chữ nào từng bị gạch. Đường số hiệu chạy `tl extract` và chuyển tiếp cảnh báo `[markup]` qua stderr. Khi có văn bản trả về và không chạm CAP, cảnh báo ấy không tự làm sai phép so hoặc chặn `--out`. Đây là giới hạn nguồn thô kế thừa, tách khỏi lọc XML của r5. [Đọc qua extract](../scripts/tl_core/llm_route.py#L1287) · [Chuyển tiếp cảnh báo](../scripts/tl_core/ops_misc.py#L3084) · [Phạm vi kiểm](../scripts/tl_core/llm_route.py#L1024)

## Findings

### E1 [P1] Điểm cắt vẫn có thể bỏ phần cuối Điều — `scripts/tl_core/llm_route.py:923`

Sau một khoản tự động, nội dung có thể chứa một đoạn thường mở giống Điều kế tiếp hoặc Chương/Mục/Phần. Nếu phần còn lại có điểm gõ tay, đoạn tiếp, bảng, hoặc khoản đánh số với một `numId` khác, chốt cùng `numId` sau mốc cắt không thấy chúng. Kiểm khối lạ, điểm và nhiều danh sách chạy trên `vung` đã cắt. Đầu ra khớp phần đầu có thể nhận rc 0 và ghi `--out` dù cả nội dung sau mốc giả bị bỏ, kể cả nội dung lẽ ra phải khiến bộ đọc dừng. Hạng P1 theo cùng hậu quả toàn vẹn với D1.

Đề xuất yêu cầu bằng chứng cấu trúc cho điểm cắt ngoài tiền tố, hoặc dừng khi chưa xác định được. Tiêu chí đóng lớp cần giữ ca dương Điều kế tiếp thật và kiểm điểm cắt giả khi phía sau là điểm tay, đoạn thường, khối chưa hiểu hoặc danh sách mới. [Chọn mốc](../scripts/tl_core/llm_route.py#L921) · [Chốt danh sách còn tiếp](../scripts/tl_core/llm_route.py#L963) · [D1 lượt 4](../ops/acceptance/llm-khoan-docx/r1/review-4-codex/VERDICT.md#L44)

### E2 [P1] Phép OR của style có thể xóa chữ vẫn hiển thị — `scripts/tl_core/llm_route.py:672`

`w:strike` trong style là thuộc tính toggle. Hai lần bật trên hai style trong cùng chuỗi `basedOn` có thể đảo trạng thái hai lần. Ví dụ bằng lời, một đoạn định nghĩa có run bình thường tiếp nối bởi run mang style con và cả style cha lẫn style con đều bật gạch đơn, không có định dạng trực tiếp. Bộ đọc trả `True` ngay ở tầng đầu tiên gặp cờ bật, rồi loại cả run. Nếu phần còn lại vẫn tạo thành định nghĩa có hai vế, bản thiếu chữ có thể qua phép so. Cách tính bảo thủ đã khai ở hướng dẫn; r5 dùng kết quả ấy để xóa chữ thay cho từ chối, nên hậu quả ở đây là mất nội dung và vẫn rc 0. Hạng P1 cùng lớp D3/A4.

Đề xuất tính hiệu lực toggle theo thứ tự các tầng và giữ quyền ghi đè trực tiếp của run. Khi chưa giải được formatting, dừng đọc Điều. Tiêu chí đóng lớp phải kiểm cả chữ thực sự bị gạch và chữ còn hiệu lực sau hai lần toggle. [Chuỗi style](../scripts/tl_core/llm_route.py#L672) · [Cửa bỏ run](../scripts/tl_core/llm_route.py#L798) · [D3 lượt 4](../ops/acceptance/llm-khoan-docx/r1/review-4-codex/VERDICT.md#L56)

### E3 [P1] Hàng bảng bị xóa vẫn có thể làm tăng bộ đếm Word — `scripts/tl_core/llm_route.py:740`

Hàng bị xóa bằng Track Changes mang `w:del` trong `w:trPr`. Bộ duyệt hiện bỏ qua toàn bộ `trPr` và vẫn đếm các đoạn trong hàng. Chốt sửa đổi dấu đoạn chỉ quét `w:rPr`. Với bảng trước Điều có ô không chứa `tcPr`, một mục đã xóa cùng `numId` có thể làm bộ đếm tiêu thụ số 0 từ `start=0`. Khi chấp nhận các thay đổi trong Word, khoản còn hiệu lực đầu tiên mới là mục mang số 0. Code thấy số 1, qua chốt liên tục và có thể ghi kết quả gán sai số khoản. Trường hợp cùng bộ đếm bắt đầu từ 1 cũng có thể chặn oan một Điều hợp lệ. Hạng P1 vì nhánh `start=0` nhận số khoản sai.

Đề xuất xác định trạng thái hàng và ô trước khi tính bộ đếm. Dừng khi gặp sửa đổi cấu trúc bảng chưa hỗ trợ và có thể ảnh hưởng đếm trước Điều. Đối chứng cần giữ số của một hàng bình thường có cùng `numId` và loại ảnh hưởng của hàng đã xóa. [Duyệt bảng](../scripts/tl_core/llm_route.py#L740) · [Chốt dấu đoạn](../scripts/tl_core/llm_route.py#L870) · [Bộ đếm](../scripts/tl_core/llm_route.py#L889) · [Đối chứng start=0 sẵn có](../scripts/tl_core/llm_route_test.py#L1311)

### E4 [P2] Thuộc tính ô bảng hợp lệ làm DOCX bị chặn oan — `scripts/tl_core/llm_route.py:746`

Ô bảng của Word thường có `w:tcPr` để khai chiều rộng, viền hoặc thuộc tính ô. Cấp bảng và hàng đã cho qua metadata tương ứng. Cấp ô chuyển cả `w:tc` vào `_doan_trong`, nơi `tcPr` bị đánh dấu là khối lạ. Một bảng bình thường nằm trước Điều đích vì vậy có thể làm cả lệnh trả rc 2. Giới hạn “bảng trong Điều” và “khối lạ trước Điều” không bao hàm thuộc tính ô chuẩn của bảng nằm ngoài Điều. Các mẫu bảng dương trong suite DOCX không có `tcPr`. Hạng P2 vì từ chối nguồn có thể đọc được.

Đề xuất nhận diện metadata ở đúng cấp ô. Kiểm dấu sửa đổi ô trước khi bỏ qua metadata, để sửa E4 không mở rộng E3. Giữ đối chứng phần tử thực sự lạ ở hàng và ô. [Đi vào ô](../scripts/tl_core/llm_route.py#L746) · [Guard trước Điều](../scripts/tl_core/llm_route.py#L918) · [Ví dụ thuộc tính ô trong fixture repo](../scripts/tl_selftest.py#L15809)

### E5 [P2] Suite DOCX bỏ sót hai hồi quy lọc markup của r5 — `scripts/tl_core/llm_route_test.py:1396`

Hai bản sao sửa riêng từng chốt đều trả rc 0, 59/59 ca và 155/155 đột biến có sẵn. Một bản đưa `strip_markup` trở lại ngay trước khi duyệt body, sau chốt dấu đoạn trên XML gốc. Bản kia đọc chữ của `w:moveFrom` như chữ còn hiệu lực. Hai chỉnh sửa vô hiệu hóa hai yêu cầu riêng ở D3. Ca gạch ngang hiện có chỉ chứng minh lọc các mẫu đã đo, còn đột biến gạch đơn/kép không khóa riêng đường đọc XML gốc và đường xóa chữ di chuyển. Hạng P2 vì thiếu cặp đo độc lập tại §3. Bằng chứng hai đột biến sống không đồng nghĩa head hiện tại chạy hai đường đột biến ấy.

Đề xuất khóa lại chữ và ranh giới trên trường hợp regex cũ từng nuốt đoạn. Đo riêng phần chữ chuyển đi bị bỏ và phần chữ chuyển đến được giữ ở đường `doc_dieu_cau_truc`. Mỗi thay đổi đích phải đỏ bằng `TinHieuChotCa` trong khi đối chứng gốc đạt. [Đọc XML và body](../scripts/tl_core/llm_route.py#L863) · [Duyệt markup](../scripts/tl_core/llm_route.py#L805) · [Runner đột biến](../scripts/tl_core/llm_route_test.py#L1717)

### E6 [P2] Cấp danh sách ngoài miền OOXML có thể làm bộ đọc cạn tài nguyên — `scripts/tl_core/llm_route.py:898`

`_doc_danh_so` và `_phan_tich_doan` nhận `ilvl` dưới dạng số nguyên mà thiếu chốt miền hợp lệ. Khi đoạn và định nghĩa đều tham chiếu một cấp ngoài miền, vòng lặp khởi tạo một mục bộ đếm cho mỗi cấp thấp hơn. Việc này xảy ra trước khâu chọn Điều, kể cả với danh sách không liên quan đến Điều đích. Trần kích thước thành phần ZIP vẫn cho qua XML nhỏ có số cấp sai miền. Hạng P2 vì có thể làm lệnh cục bộ treo hoặc hết bộ nhớ thay vì trả lỗi đầu vào, với hậu quả trên phiên xử lý tệp.

Đề xuất chặn cấp ngoài miền Word tại lúc nạp định nghĩa, override và đoạn, trước khi dùng cấp để khởi tạo bộ đếm. Tiêu chí đóng lớp là trả lỗi có kiểm soát và giữ nguyên ca dương nhiều cấp. [Định nghĩa cấp](../scripts/tl_core/llm_route.py#L593) · [Cấp trên đoạn](../scripts/tl_core/llm_route.py#L829) · [Khởi tạo bộ đếm](../scripts/tl_core/llm_route.py#L891)

### Lịch sử theo lớp

| Lớp | Biểu hiện mở và tiêu chí đóng |
| --- | --- |
| `ranh-gioi-khoan` | E1 (P1), tiếp A1/B1/C1/D1. D6/C3 và K1 thô đóng ở biểu hiện đã báo. Cần bằng chứng điểm cắt phân biệt tiêu đề với văn bản trước khi bỏ phần sau. |
| `docx-so-hien-thi` | E3 (P1), tiếp A2/B2/C2/D2 ở phạm vi đầu vào bộ đếm. Reset section D2 đã đóng. Cần chỉ đếm cấu trúc còn hiệu lực trước Điều. |
| `docx-markup-du-thao` | E2 (P1), tiếp A4/B3/C4/D3. Lỗi regex cũ đã đóng trong sản phẩm. Cần kiểm kết quả toggle trước khi xóa chữ. |
| `docx-chu-hien-thi` | E4 (P2), cùng lớp danh sách phần tử cho phép của B4/B6/C5. Cần đi qua metadata ô chuẩn và giữ từ chối khối chưa hiểu. |
| `do-phu-chot-docx` | E5 (P2), tiếp A7/B7/C6/D4. Hai đột biến cụ thể của D4 đã đóng. Cần phép đo riêng cho hai hồi quy markup đã đo. |
| `docx-gioi-han-bo-dem` | E6 (P2), lớp mới về giới hạn tài nguyên. Cần chặn cấp ngoài miền trước khi tạo bộ đếm. |
| `docx-namespace` | Đã đóng D5 qua giới hạn, thông báo và đột biến. |

Có 6 lớp mở và 6 finding mở, gồm 0 P0, 3 P1, 3 P2, 0 P3. Trong 5 lớp mở của lượt 4, đóng 1 lớp (20%) và 4 lớp tiếp tục mở. `docx-chu-hien-thi` mở lại với E4. `docx-gioi-han-bo-dem` là lớp mới. Cùng lớp lặp và trần 5/5 đưa packet tới Review Rescue Checkpoint. [Protocol §8.3](../docs/PROTOCOL_DA_PHIEN.md#L812) · [Protocol §12](../docs/PROTOCOL_DA_PHIEN.md#L1097) · [ADR-0060 M1/M2](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32)

## Kết quả test và đột biến

Linux x86_64, Python 3.13.18, Git 2.43.0. Checkout head đặt `core.abbrev=7`. Bản sao base không kế thừa tùy chọn đó. Tắt ghi bytecode, đặt log và bản sao ngoài checkout tại `/tmp/wp1525-r5-review.BhJZ2g/`. Các đột biến bổ sung chỉ sửa `llm_route.py` trong bản sao. Test dùng dữ liệu và runner có sẵn.

| Lệnh | Trạng thái | Mã thoát và bằng chứng |
| --- | --- | --- |
| `python scripts/tl_core/llm_route_test.py` | `passed` | rc 0, 59/59 ca và 155/155 đột biến có sẵn, gồm 58/58 `wp1525_*`. Runner chỉ tính giết khi ca đích trả `TinHieuChotCa`. `llm-route.stdout`. |
| Cùng lệnh trên từng bản sao `old-regex` và `keep-moved` | `failed` về tiêu chí độ phủ bổ sung | Mỗi lượt rc 0, 59/59 ca và 155/155 đột biến có sẵn. Giết 0/2 đột biến bổ sung. `old-regex.diff`, `old-regex.stdout`, `keep-moved.diff`, `keep-moved.stdout`. |
| `python scripts/tl.py --deterministic workflow-audit --strict --json` | `passed` | rc 0, `ok=true`, 26 cards, 60 tasks, 194 lệnh khả dụng, 0 lỗi, 0 cảnh báo. `workflow.stdout`. |
| `python scripts/tl.py --deterministic golden-test --json` | `passed` | rc 0, `ok=true`, 20/20. `golden.stdout`. |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` trên checkout có verdict | `failed` | rc 2, `ok=false`, 187/187 tệp manifest khớp. Tệp thừa duy nhất là `.review/VERDICT.md` theo yêu cầu tạo sớm. `release.stdout`. |
| Cùng lệnh `release-verify` trên bản sao sạch cùng exact head/tree | `passed` | rc 0, `ok=true`, 187/187 tệp, 0 tệp thừa, `package_hash_match=true`. Checkout ban đầu sạch. `release-clean.stdout`, `release-clean.oid`. |
| `python ops/lease_publish.py check --root . ops/leases/llm-khoan-docx-r5-g1-claude.yaml` | `passed` cục bộ | rc 0, thông báo “ĐĂNG ĐƯỢC”, Issue #1525, neo base `64b7f2c14776` và hạn 18:06 UTC. Hai lớp GitHub ngoài phạm vi của lệnh. `lease.stdout`. |
| `python scripts/tl.py --selftest` trên head | `failed` | rc 1, 1774/1790. `[OK] r1525_llm_khai_niem_tep_docx_cau_truc`, ca CLI dùng model giả kiểm rc 0/5/2. `selftest.stdout`, `selftest.stderr`. |
| Cùng lệnh trên bản sao sạch của base | `failed` | rc 1, 1771/1789. Base tree `0cc14e79cecd2ce44bc4dc6cff92cadb31fd7ee4`. Cả 16 ca đỏ ở head đều đỏ ở base. Hai ca chỉ đỏ ở bản sao base là `r218_docclaims_l2_sha_khong_ton_tai` và `r264_doc_claims_phu_docs`. So danh sách bằng `diff -u` trả rc 1 vì hai ca chỉ có ở base. `selftest-base.stdout`, `selftest-base.stderr`, `selftest-failed.txt`, `selftest-base-failed.txt`. |
| `git diff --check fcb12b3 HEAD` | `passed` | rc 0. |
| `git diff --check 64b7f2c HEAD` | `failed` | rc 2, 3 dòng Markdown hard break có từ hồ sơ #1514 lượt 8. [Hồ sơ](../ops/acceptance/llm-ranh-gioi-khoan/r1/review-8-codex/VERDICT.md#L3) |

`/tmp/.git` rỗng có mặt ở cả hai lượt selftest. 14 ca thuộc các nhóm `r973_bootstrap_*`, `wp433_*` và `wp727_tl_gws_refresh` đỏ như prompt dự báo. Cả hai lượt còn đỏ `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` và `r268_l2_trichotomy_theo_trang_thai_object`. Tập ca đỏ của head nằm trọn trong tập ca đỏ của base. Bản sao base thiếu `core.abbrev=7`, có thể giải thích hai ca doc-claims chỉ đỏ ở base, vốn phụ thuộc vào nhận diện SHA ngắn. N/N ở head vẫn đỏ trong môi trường này. [Ca r218](../scripts/tl_selftest.py#L26393) · [Ca r226](../scripts/tl_selftest.py#L27758) · [Ca r264](../scripts/tl_selftest.py#L29232) · [Ca r268](../scripts/tl_selftest.py#L29416)

Selftest trên head sinh hai thư mục ignored `references/golden/fixtures/` và `scripts/.tl_state/`. Đã chuyển cả hai vào `head-generated/` trong scratch. Snapshot đầu/cuối khớp exact HEAD/tree, diff tracked, index, status untracked/ignored và băm tệp thường dưới đường dẫn ignored có sẵn. Checkout cuối giữ tệp verdict theo yêu cầu. Hai snapshot chỉ xác nhận trạng thái ở hai mốc. Không có lệnh nào trong sáu lệnh được báo `skipped`.

## Không đo được

- E1–E4 và E6 dựa trên luồng đọc mã. Hành vi hiển thị Word sau toggle, số khoản sau khi accept tracked deletion, điểm cắt trên bố cục mới, tỷ lệ gặp `tcPr` theo từng exporter và trần tài nguyên thực tế chưa được chạy bằng fixture mới. Các phần tử định dạng khác của Word/Google Docs cần tệp xuất thực tế để kết luận chặn oan. E5 có hai phản chứng bằng đột biến mã và suite có sẵn.
- Bằng chứng Windows là `required` cho toàn PR theo ADR-0060 M3 do diff từ base thêm mã test Python chứa `encoding=`. Windows bản địa, Windows CI, các check GitHub, và hai lớp xác minh lease qua GitHub đều `not_run`. Model/effort phục vụ và mã thoát terminal của chính lượt launcher chưa có trong metadata đọc được trong phiên.
- `determinism-audit --strict`, `doc-claims-check --strict` và Ruff F delta thuộc nghiệm thu đặc tả §5, nằm ngoài sáu phép đo của prompt lượt này, trạng thái `not_run`. Đường model thật không chạy. Tập kết quả cục bộ trên không đủ gate merge.

ADR-0060 M1 yêu cầu 0 finding P0/P1/P2. Head này còn 3 P1 và 3 P2. Lượt 5/5 chạm trần review.

P2_mo: 3

VERDICT: REQUEST_CHANGES
