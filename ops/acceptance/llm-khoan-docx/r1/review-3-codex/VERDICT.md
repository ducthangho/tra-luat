# Verdict packet #1525 r3 lượt 3 — Codex

reviewed_sha: b0f3cb9ea1cca141f12eb462ced60f949d1ed0a4
tree_sha: d129d1e7a6a23617edb8df50c57bb588d6f5f5e8
base_sha: 64b7f2c14776d5d0e1d34a6be4725490956f5bec

VERDICT: REQUEST_CHANGES

## Xác minh đầu vào

- Checkout độc lập `rv`, detached HEAD. Origin khai `github.com/ducthangho/tra-luat`. Baseline nghiệm thu là `64b7f2c14776d5d0e1d34a6be4725490956f5bec`, mốc bàn giao #1514 là `fcb12b3873c3bec2c339029136243ed2c804ce05`, mốc đối chiếu bản vá r3 là `15801e48e77a2ddda7a46370428113bc55134bfa`. Cả ba là tổ tiên của head được review.
- Đặc tả r3 lấy từ `b0f3cb9ea1cca141f12eb462ced60f949d1ed0a4:ops/specs/llm-khoan-docx-r3.md`, blob `f7c6a41098750bc5a2c0ad2da317d23a5fd48aab`. SHA-256 của blob và bản checkout cùng là `8cda58b3504f240ae5d117902e48df67750c28191a02b8e3abb606716431a6e0`, khớp lease revision 3, generation 1, `sensitive`, hạn `2026-11-25T17:27:00Z`. [Đặc tả](../ops/specs/llm-khoan-docx-r3.md) · [Lease](../ops/leases/llm-khoan-docx-r3-g1-claude.yaml)
- `fcb12b3..HEAD` có 26 đường dẫn, gồm bốn hồ sơ #1514 mà prompt loại khỏi phép so. Cả 22 đường dẫn còn lại nằm trong 32 đường dẫn write set. SHA-256 danh sách đã sắp xếp là `d83bcf5f2ab77f97bc239ab6d4f19bc83c674c1209a88432a21f7afbd2107d8e`. `15801e4..HEAD` có tám đường dẫn, đều thuộc write set. Ba cặp bia mộ r9 ↔ r1 ↔ r2 ↔ r3 khớp `thay_the_cho` và `da_bi_thay_the`. 4/4 hash đặc tả tại head khớp lease.
- Executor khai trong lease `claude / claude_code / machine/local`. Reviewer thực tế `openai_codex / codex_cli / machine`, Codex CLI 0.172.0, sandbox `workspace-write` với `.git` và `.codex` chỉ đọc. `run.json` và `checkpoint.json` của launcher cùng neo SHA và SHA-256 prompt `23873d9c9cdcad54caba1e2144e2c07e6ead5172733311e179e1ffc5f2268172`. Run ID `c56a15e4c43644b0929ba2333c09f49c`, lời gọi 3/5. Model và effort phục vụ `KHONG_DO_DUOC` tại thời điểm ghi. [Hợp đồng receipt](../docs/PROTOCOL_DA_PHIEN.md#L770)

## Đối chiếu lượt 2 và đặc tả r3

Nguồn lịch sử là lượt 1 trên `3d247516aaeb0ad3d836a2dc51dda13052fdbe47`, lượt 2 trên `38c481f792b3f44d7500e93249153af63c0165db` và lượt 10 #1514 trên `fcb12b3873c3bec2c339029136243ed2c804ce05`. [A1–A8](../ops/acceptance/llm-khoan-docx/r1/review-1-codex/VERDICT.md) · [B1–B8](../ops/acceptance/llm-khoan-docx/r1/review-2-codex/VERDICT.md) · [K1](../ops/acceptance/llm-ranh-gioi-khoan/r1/review-10-codex/VERDICT.md#L35)

| Mục | Trạng thái | Bằng chứng |
| --- | --- | --- |
| §1 | Đạt trong phạm vi đo | Không đổi `goi`, `duong_api`, `duong_sub`, `_chay_co_moc` hay tập cờ CLI. Handler chọn `pham_vi_kiem` theo dữ liệu dùng để đối chiếu và luôn đặt `can_nguoi_duyet: true`. Ca `ca_wp1514_luot2` đo Điều 3 và ba kết quả đã lưu, mỗi bản 8/8. Diff thô giữ các chốt cũ và thay nhánh nhập nhiều dòng bằng nhánh chặn. [Handler](../scripts/tl_core/ops_misc.py#L3130) · [Ca 8/8](../scripts/tl_core/llm_route_test.py#L1060) |
| A1 | VÁ MỘT PHẦN | Wrapper cấp khối, bảng trong Điều trước fallback, tiêu đề trùng và đoạn giống tiêu đề có đánh số đều có chốt. Nhánh tiêu đề đích còn bỏ qua `ngat` khi chữ đã gộp khớp mẫu. Điểm cắt vẫn có thể nhận một đoạn thân làm tiêu đề. Xem C1. [Chọn vùng](../scripts/tl_core/llm_route.py#L855) |
| A2 | VÁ MỘT PHẦN | Nhãn cấp khoản phải là `decimal` cộng `%N.` hoặc `%N)`. Test đo `start=0`, `startOverride` đổi 5→1, đặt lại điểm ở khoản kế, danh sách tiếp từ Điều trước và hai `numId` trong Điều. `lvlRestart`, `isLgl` bật và liên kết style không hỗ trợ bị chặn. C2 còn sai số và sai nhãn điểm. [Định nghĩa](../scripts/tl_core/llm_route.py#L583) · [Bộ đếm](../scripts/tl_core/llm_route.py#L831) · [Ca dương](../scripts/tl_core/llm_route_test.py#L1247) |
| A3 | ĐÃ VÁ THẬT | Phép dò chỉ nhận chữ đoạn mở khoản. Đột biến dò cả khoản bị giết bởi ca có từ nối duy nhất trong điểm nhãn chữ hoa. C3 là một đường tách sai riêng ngay trong đoạn mở khoản. [So sánh](../scripts/tl_core/llm_route.py#L1133) · [Ca A3](../scripts/tl_core/llm_route_test.py#L1280) |
| A4 | VÁ MỘT PHẦN | Đã lọc gạch trực tiếp, chặn gạch còn sót qua namespace/style và sửa dấu đoạn trên XML gốc. C4 còn lọt định dạng gạch kế thừa. [Lọc markup](../scripts/tl_core/llm_route.py#L816) · [Ca A4](../scripts/tl_core/llm_route_test.py#L1350) |
| A5 | ĐÃ VÁ THẬT | Danh sách La Mã độc lập có override ngoài phạm vi vẫn để Điều đích đạt. Mã kiểm lỗi định nghĩa và dựng nhãn cho danh sách dùng trong Điều. [Ca A5](../scripts/tl_core/llm_route_test.py#L1276) · [Kiểm danh sách](../scripts/tl_core/llm_route.py#L901) |
| A6 | ĐÃ VÁ THẬT | Điểm gõ tay dấu chữ và dấu gạch liền thân giữ nguyên dấu và dòng. Đột biến buộc khoảng trắng bị giết. [Ca A6](../scripts/tl_core/llm_route_test.py#L1263) |
| A7 | VÁ MỘT PHẦN | Ca override khác `start` gốc, ca điểm gõ tay và chốt bảng trước fallback đã có đối chứng và đột biến đích. C6 còn khe độ phủ của tiêu đề và ranh giới. [Ca và đột biến](../scripts/tl_core/llm_route_test.py#L1304) |
| A8 | ĐÃ VÁ THẬT | Hướng dẫn đường thô nói nhất quán mỗi khoản một dòng và dẫn sang `.docx` khi có điểm. [Hướng dẫn](../docs/GOI_AGENT_DA_NEN.md#L373) |
| B1 | VÁ MỘT PHẦN | Tiêu đề dính thân ngoài mẫu, markup/phần tử lạ được phát hiện ở điểm cắt, ngắt mềm trong vùng và đoạn số rỗng đều có chốt trước fallback. Chốt `ngat` của tiêu đề đích và thứ tự xác thực điểm cắt còn hở. Xem C1 và C6. [Chọn vùng và fallback](../scripts/tl_core/llm_route.py#L861) |
| B2 | VÁ SINH LỖI MỚI | Đã chặn `w:lvl/w:pStyle`, numbering chỉ qua style trong Điều và khối lạ trước Điều. Bảng lồng có hàng/ô trực tiếp đạt, nhưng duyệt trực tiếp làm mất hàng/ô nằm dưới wrapper mà `iter(w:tc)` cũ nhìn thấy. Xem C2. [Duyệt bảng](../scripts/tl_core/llm_route.py#L710) · [Ca bảng lồng](../scripts/tl_core/llm_route_test.py#L1297) |
| B3 | VÁ MỘT PHẦN | Hai cờ gạch tách riêng. Tắt gạch đơn trực tiếp vẫn giữ gạch kép kế thừa. `docDefaults` có ca riêng và mã nạp style đoạn mặc định. C4 còn sai ở cách áp dụng thuộc tính bật/tắt trong style. [Style và run](../scripts/tl_core/llm_route.py#L631) · [Các ca B3](../scripts/tl_core/llm_route_test.py#L1369) |
| B4 | ĐÃ VÁ THẬT | `noBreakHyphen` sinh `-`. Ca dương so đúng ký tự. Phần tử run chưa hiểu, gồm trường, hình và ký hiệu, đặt `la`. Ca `w:sym` và đột biến đích xác nhận nhánh này trong vùng. C5 là chặn oan wrapper chứa chữ có thể đọc. [Đọc run](../scripts/tl_core/llm_route.py#L760) · [Ca dấu nối](../scripts/tl_core/llm_route_test.py#L1285) |
| B5 | ĐÃ VÁ THẬT | Regex số gõ tay có `(?!\d)`. Ca dương đầu thân là số thập phân, ca âm mang số tay và hai đột biến tương ứng đã chạy. [Regex](../scripts/tl_core/llm_route.py#L528) · [Ca dương](../scripts/tl_core/llm_route_test.py#L1290) |
| B6 | ĐÃ VÁ THẬT | Metadata `customXmlPr`, `sdtPr`, `sdtEndPr` được bỏ qua theo vị trí wrapper. Ca dương và đột biến kiểm `customXmlPr`. [Duyệt khối](../scripts/tl_core/llm_route.py#L710) · [Ca B6](../scripts/tl_core/llm_route_test.py#L1293) |
| B7 | VÁ MỘT PHẦN | Đã tách ca bảng trước fallback, thêm ca/đột biến tiêu đề đánh số tự động, `numFmt` cấp con và `numStyleLink`. Nhánh `la` của điểm cắt vẫn sống qua toàn bộ suite khi bị vô hiệu hóa. Các khe khác ở C6. [Bảng đột biến](../scripts/tl_core/llm_route_test.py#L1433) |
| B8 | ĐÃ VÁ THẬT | Hướng dẫn phân biệt numbering qua style trong và ngoài Điều theo r3. C7 ghi sai lệch khác về dấu cuối nhãn khoản. [Hướng dẫn DOCX](../docs/GOI_AGENT_DA_NEN.md#L390) |
| §2.1, §2.4 và §2.5 | Còn C1–C6 | Dùng thư viện chuẩn, dùng reader ZIP bounded khi nạp được và lọc markup trước khi đọc. Câu dẫn cấu trúc vắng hoặc đúng một đoạn khớp toàn câu chuẩn. Chỉ những đoạn mang marker điểm gõ tay đã khai mới được ghép vào khoản đang mở. Đối chiếu sau trích giữ số lượng, thứ tự, số mục và hai vế theo từng khoản đã đọc. [Đọc thành phần](../scripts/tl_core/llm_route.py#L552) · [Câu dẫn](../scripts/tl_core/llm_route.py#L947) · [Phép so](../scripts/tl_core/llm_route.py#L1116) |
| §2.2 | Đạt định tuyến, còn C1 ở dữ liệu trước fallback | ZIP magic chọn DOCX, yêu cầu `--dieu`, từ chối số hiệu đi kèm. `ValueError` và lỗi đọc nằm trong nhóm handler bắt được trả rc 2. Chỉ `KhongCauTruc` đi đường thô. `--out` chỉ ghi khi danh sách lệch rỗng. [Handler](../scripts/tl_core/ops_misc.py#L3027) · [Ghi đầu ra](../scripts/tl_core/ops_misc.py#L3133) |
| §2.3 và K1 | ĐÃ VÁ THẬT | `_RE_DIEM` trả `None` trên nguồn có và mất số. Dòng tiếp mở bằng “là” ở nguồn có số rơi vào nhánh từ chối dòng không số. Ở nguồn mất số, phép so từ chối vì vế thuật ngữ rỗng. Ca Q3 cũ, ca J1 có đủ dấu kết và đột biến bỏ chốt điểm đã chạy. [Bộ tách](../scripts/tl_core/llm_route.py#L976) · [Q3](../scripts/tl_core/llm_route_test.py#L808) · [J1](../scripts/tl_core/llm_route_test.py#L1170) |
| §3 | Còn C6 | Ca dương đo điểm, số và chữ sau lọc. Ca âm đo tách điểm, sai cấu trúc và fallback. Selftest có ca tích hợp handler với model giả, kiểm rc 0/5/2 và metadata. [Ca tích hợp](../scripts/tl_selftest.py#L32230) |

Trên đường thô, lớp `ranh-gioi-khoan` còn giới hạn đã công bố. Hai dòng đã mất bố cục vẫn có thể được hiểu là hai khoản nếu mỗi dòng trông như một định nghĩa hoàn chỉnh. Số tiểu mục mất thụt lề cũng có thể trùng số khoản tiếp theo. `pham_vi_kiem` báo rõ phạm vi đó. Với DOCX, `KhongCauTruc` chỉ được tạo sau các chốt vùng, nhưng điểm cắt ở C1 có thể làm phần đưa vào các chốt thiếu dữ liệu. [Phạm vi thô](../scripts/tl_core/llm_route.py#L958) · [Hướng dẫn](../docs/GOI_AGENT_DA_NEN.md#L368)

## Findings

P1 áp cho đường có thể báo đạt hoặc ghi `--out` với nguồn đối chiếu sai. P2 áp cho lỗi chặn oan và thiếu phép kiểm bắt buộc. P3 áp cho hướng dẫn sai mà hành vi chạy vẫn đúng hợp đồng ở điểm đó. [Protocol §8](../docs/PROTOCOL_DA_PHIEN.md#L634) · [ADR-0060 M1–M2](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32)

### C1 [P1] Điểm cắt dựa vào tiền tố có thể bỏ phần cuối Điều — `scripts/tl_core/llm_route.py:864,871`

**Kịch bản và căn cứ.** Một đoạn thân trong Điều, chẳng hạn đoạn trích hay đoạn không đánh số có chữ mở giống tiêu đề Điều khác, đến trước các khoản còn lại. Vòng đọc chỉ cần đoạn ngoài bảng, khớp tiền tố, không đánh số và hai cờ `con_bo`/`la` tắt để `break`. Đoạn ấy và phần sau bị loại trước các chốt đoạn không số và ngắt mềm. Một dãy đầu liên tục từ 1 vẫn qua và phép so chỉ đòi các khoản đã lọc ra, cả với DOCX số tự động và với DOCX số tay lùi qua `KhongCauTruc`. `ngat` cũng không được kiểm trên tiêu đề đích. Một ngắt mềm giữa số Điều và phần tên được phép có thể biến thành đúng mẫu sau `_gon_doan`, trái chốt tiêu đề của §2.4 A1.

**Đề xuất.** Xác thực vai trò của điểm cắt trước khi bỏ dữ liệu và trả lỗi khi đoạn có thể là thân. Kiểm ngắt ở tiêu đề đích và ứng viên điểm cắt trước khi gộp chữ hoặc lùi về đường thô. Giữ đối chứng Điều kế thật có tên riêng. [Nhánh cắt](../scripts/tl_core/llm_route.py#L870) · [Chốt vùng](../scripts/tl_core/llm_route.py#L881) · [§2.4 A1](../ops/specs/llm-khoan-docx-r3.md#L45)

### C2 [P1] Bộ đếm bỏ hàng hoặc ô có wrapper, nhãn chữ có thể sai sau Z — `scripts/tl_core/llm_route.py:677,710`

**Kịch bản và căn cứ.** Với bảng trước Điều, `findall(w:tr)` rồi `findall(w:tc)` chỉ thấy hàng và ô trực tiếp. Word có thể đặt content control hoặc `customXml` ở cấp hàng hay ô. Vòng lặp đó lặng lẽ bỏ cả nhánh được bọc. Marker bảng vẫn là `bang`, nên chốt khối `la` trước Điều không chặn. Nếu nhánh bị bỏ dùng cùng `numId` với Điều đích, mã có thể thấy khoản đầu là 1 trong khi Word đã dùng số 1 trước đó. Bộ đếm mỗi danh sách hoạt động độc lập nhưng vẫn dựa vào tập đoạn không đầy đủ. Ngoài ra, cho `lowerLetter` và `upperLetter`, `_chu_cai` dùng phép đổi cơ số kiểu cột bảng tính. Sau nhãn Z, Word lặp một chữ cho mỗi nhãn hai chữ. Từ nhãn thứ hai của vòng này, phép tăng kiểu cột cho chuỗi khác. Nhãn điểm sai đi vào cả văn bản gửi model và phép so.

**Đề xuất.** Duyệt container hàng/ô theo thứ tự, đếm đúng một lần hoặc đánh dấu nhánh chưa hiểu để chặn trước Điều. Đối chiếu định dạng chữ với quy ước Word hoặc thu hẹp miền hỗ trợ đến giới hạn đã xác minh. Giữ đối chứng `start`, `startOverride`, đặt lại cấp con, bảng lồng và `numId` độc lập. [Duyệt bảng](../scripts/tl_core/llm_route.py#L710) · [Bộ đếm](../scripts/tl_core/llm_route.py#L831) · [Dựng nhãn](../scripts/tl_core/llm_route.py#L677)

### C3 [P1] DOCX có thể tách thuật ngữ tại “là” nằm trong trích dẫn — `scripts/tl_core/llm_route.py:1043,1138`

**Kịch bản và căn cứ.** Tiêu đề khoản là một cụm có trích dẫn dùng dấu ngoài miền `_quet`, chẳng hạn ngoặc vuông hoặc dấu trích dẫn góc. Bên trong cặp dấu có “là”, và bên ngoài có từ nối thật của khoản. Đường thô chạy `_dong_mo_ho` và từ chối dấu chưa hiểu. Đường cấu trúc đi thẳng tới `_tu_noi` trên đầu khoản. `_quet` coi “là” bên trong cặp dấu đó như từ nối cấp khoản. Sau đó hai chuỗi sai ranh giới do phép so tự cắt có thể khớp đầu ra model và qua kiểm.

**Đề xuất.** Áp kiểm dấu phân cách cho đầu khoản cấu trúc trước khi tìm từ nối hoặc dùng bộ quét nhận diện được cặp dấu đó. Giữ kiểm từ nối cấp khoản độc lập với nội dung điểm. [Chốt đường thô](../scripts/tl_core/llm_route.py#L976) · [Bộ quét](../scripts/tl_core/llm_route.py#L1074) · [Phép so cấu trúc](../scripts/tl_core/llm_route.py#L1116)

### C4 [P1] Gạch kế thừa có thể mất khi áp style hậu duệ — `scripts/tl_core/llm_route.py:639,663,743`

**Kịch bản và căn cứ.** Word xử lý `w:strike` như thuộc tính toggle trong định nghĩa style. Nếu style cha bật gạch đơn, khai báo giá trị tắt trong style con giữ trạng thái đang có. Tắt trong định dạng trực tiếp của run mới đặt trạng thái tắt tuyệt đối. `_theo_kieu` dừng ở giá trị gần nhất, kể cả `False`, nên đánh mất trạng thái bật từ cha. Bộ lọc chung chỉ xem gạch trực tiếp trên run. Chữ đã gạch theo style có thể còn trong đoạn, đi vào dữ liệu cấu trúc hoặc vào `KhongCauTruc`, rồi được đối chiếu như chữ đang dùng.

**Đề xuất.** Tính thuộc tính toggle theo chuỗi style theo đúng thứ tự và tách quy tắc định dạng trực tiếp. Nếu chưa xác định được hiệu lực, chặn trước khi tạo dữ liệu so. Giữ đối chứng tắt trực tiếp hợp lệ, gạch kép, style kế thừa và `docDefaults`. [Đọc style](../scripts/tl_core/llm_route.py#L631) · [Áp định dạng run](../scripts/tl_core/llm_route.py#L747) · [Bộ lọc chung](../scripts/docx_markup.py#L74)

### C5 [P2] Content control nội dòng chứa văn bản thường bị từ chối — `scripts/tl_core/llm_route.py:535,778`

**Kịch bản và căn cứ.** Word có content control văn bản thường ở cấp run, dùng trong mẫu soạn thảo để bọc một cụm chữ chỉnh sửa được. Cùng `w:sdt` đã được hỗ trợ ở cấp khối, nhưng `w:sdt` đặt trong đoạn có nội dung `w:sdtContent` toàn run vẫn bị `duyet` biến thành `la`. Kết quả là rc 2, dù tiêu đề, khoản và số thứ tự có thể giữ nguyên. Hướng dẫn không nêu giới hạn riêng với content control nội dòng. Dạng này khác trường Word hay hình/chú thích đã công bố. Tần suất trong corpus pháp luật và bản xuất Google Docs chưa đo.

**Đề xuất.** Chỉ đi vào `w:sdtContent` nội dòng khi cấu trúc hợp lệ, áp tiếp danh sách con đang dùng và chặn nhánh hiển thị chưa hiểu. Nếu giới hạn này chủ ý, nêu rõ phạm vi hỗ trợ trong đặc tả và hướng dẫn. [Duyệt khối](../scripts/tl_core/llm_route.py#L710) · [Duyệt nội dòng](../scripts/tl_core/llm_route.py#L778) · [Hướng dẫn](../docs/GOI_AGENT_DA_NEN.md#L390)

### C6 [P2] Ca ranh giới chưa giết được đột biến vô hiệu hóa nhánh phần tử lạ — `scripts/tl_core/llm_route_test.py:1342,1366,1465`

**Kịch bản và căn cứ.** `wp1525_ranh_gioi_markup` bỏ chung `con_bo` và `la`. Ca đích có gạch ngang qua style, chỉ cần `con_bo` là đủ làm đỏ. Trên bản sao tạm, đặt riêng `la=False` ngay trước chốt ranh giới vẫn cho rc 0, 59/59 ca và 142/142 đột biến. Ca tiêu đề có ngắt mềm dùng helper luôn thêm chữ ngoài mẫu sau ngắt, nên chốt regex tự giết ca. Ca đó chưa xác nhận tiêu đề khớp mẫu nhưng có ngắt. Ca liên kết numbering có `numStyleLink`, còn đột biến bỏ chung `numStyleLink/styleLink` chưa chứng minh nửa `styleLink`. §2.5 B7 và §3 yêu cầu đo riêng từng chốt.

**Đề xuất.** Đối chứng từng nhánh bằng ca có nguyên nhân từ chối duy nhất và đột biến bỏ đúng nhánh đó. Giữ ca bảng trước fallback đã được tách ở r3. [Helper ngắt](../scripts/tl_core/llm_route_test.py#L1206) · [Ca gạch ngang ở điểm cắt](../scripts/tl_core/llm_route_test.py#L1366) · [Bảng đột biến](../scripts/tl_core/llm_route_test.py#L1452)

### C7 [P3] Hướng dẫn thiếu dạng nhãn khoản kết thúc bằng ngoặc đóng — `docs/GOI_AGENT_DA_NEN.md:395`

Hướng dẫn liệt kê nhãn khoản khác `%N.` trong nhóm rc 2. §2.4 A2 và `re.fullmatch` đều cho phép `%N)`. Cập nhật hướng dẫn để người đọc có thể chọn tệp với một trong hai dạng được hỗ trợ. [Hướng dẫn](../docs/GOI_AGENT_DA_NEN.md#L390) · [Chốt nhãn](../scripts/tl_core/llm_route.py#L908)

### Lịch sử theo lớp

| Lớp | Biểu hiện đang mở và mức cao nhất | Cách đóng lớp |
| --- | --- | --- |
| `ranh-gioi-khoan` | C1 tiếp A1/B1, C3 ở đầu khoản. P1. K1 thô và biểu hiện A3 lấy từ nối ở điểm đã đóng. | Xác minh vùng trước khi cắt, rồi xác minh dấu phân cách và từ nối của chính đầu khoản. |
| `docx-so-hien-thi` | C2 tiếp A2/B2. P1. | Đối chiếu số Word từ đúng chuỗi đoạn và nhãn của từng cấp. |
| `docx-markup-du-thao` | C4 tiếp A4/B3. P1. | Kiểm hiệu lực style và định dạng trực tiếp trước khi xác nhận chữ. |
| `do-phu-chot-docx` | C6 tiếp A7/B7. P2. | Kiểm từng nhánh độc lập với đối chứng và đột biến đích. |
| `docx-chu-hien-thi` | Biểu hiện B4 đã đóng. C5 là dạng wrapper bị từ chối, P2. | Đo nhận wrapper văn bản thường và chặn wrapper có nội dung chưa hỗ trợ. |
| `huong-dan-duong-docx` | B8 đã đóng ở phần style. Còn C7 về nhãn, P3. | Đối chiếu toàn bộ hướng dẫn với những dạng nhãn được nhận. |

Sáu lớp và bảy finding C1–C7 còn mở. B5 (`docx-nhan-dien-so-go-tay`) và B6 (`docx-khoi-customxml`) đóng lớp. Trong tám lớp mở từ lượt 2, 2/8 đóng toàn lớp. B4 và B8 đóng biểu hiện cũ nhưng lớp vẫn mở vì C5 và C7. Các lớp đã đóng từ trước `docx-kiem-danh-sach-ngoai-vung`, `docx-dau-diem-go-tay` và `huong-dan-duong-tho` tiếp tục qua đối chiếu. `ranh-gioi-khoan`, `docx-so-hien-thi`, `docx-markup-du-thao` và `do-phu-chot-docx` lặp qua ba lượt, đủ tín hiệu Review Rescue Checkpoint theo §12. [Lịch sử lượt 2](../ops/acceptance/llm-khoan-docx/r1/review-2-codex/VERDICT.md#L78) · [Protocol §8.3](../docs/PROTOCOL_DA_PHIEN.md#L812) · [Protocol §12](../docs/PROTOCOL_DA_PHIEN.md#L1097)

## Kết quả test và đột biến

Môi trường Linux x86_64, Python 3.13.18, Git `core.abbrev=7`, tắt Python bytecode. Mã thoát và log nằm trong `/tmp/wp1525-review3.YHRBqWD7/`. Các lệnh ở head dùng `b0f3cb9ea1cca141f12eb462ced60f949d1ed0a4`. Bản sao baseline detached có tree `0cc14e79cecd2ce44bc4dc6cff92cadb31fd7ee4`.

| Lệnh và phạm vi | Trạng thái | Mã thoát và bằng chứng |
| --- | --- | --- |
| `python scripts/tl_core/llm_route_test.py` | `passed` | rc 0, 59/59 ca và 142/142 đột biến. Có 45 tên `wp1525_*` trong `DOT_BIEN`. Runner áp từng neo đúng một lần trên bản sao tạm và chỉ tính giết khi ca đích ném `TinHieuChotCa`. `llm_route_test.log` |
| Cũng lệnh trên, trên bản sao tạm vô hiệu riêng `la` tại điểm cắt | `passed` theo runner, đột biến bổ sung **sống** | rc 0, 59/59 và 142/142. Chỉ thêm `d = {**d, "la": False}` ngay trước `if d["con_bo"] or d["la"]`, giữ nguyên mã test và các neo sẵn có. `mutant_boundary.diff`, `mutant_boundary.log`. Đây là bằng chứng cho C6. |
| `python scripts/tl.py --deterministic workflow-audit --strict --json` | `passed` | rc 0, `ok=true`, 26 cards, 60 tasks, 194 lệnh, 0 lỗi và 0 cảnh báo. `workflow.log` |
| `python scripts/tl.py --deterministic golden-test --json` | `passed` | rc 0, `ok=true`, 20/20 ca. `golden.log` |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` trên checkout chứa verdict | `failed` | rc 2, `ok=false`, 187/187 tệp khớp hash. Tệp thừa duy nhất là `.review/VERDICT.md` do yêu cầu ghi sớm. `manifest.log` |
| Cũng lệnh `release-verify` trên bản sao sạch cùng SHA/tree | `passed` | rc 0, `ok=true`, 187/187, 0 tệp thừa và package hash khớp. `candidate_manifest.log` |
| `python ops/lease_publish.py check --root . ops/leases/llm-khoan-docx-r3-g1-claude.yaml` | `passed` cục bộ | rc 0, “ĐĂNG ĐƯỢC”, Issue #1525, neo `64b7f2c14776`, hết hạn `2026-11-25T17:27:00Z`. `check` báo hai lớp GitHub ngoài phạm vi lệnh. |
| `python scripts/tl.py --selftest` trên head | `failed` | rc 1, 1774/1790, gồm `[OK] r1525_llm_khai_niem_tep_docx_cau_truc`. `selftest.log` |
| `python scripts/tl.py --selftest` trên baseline | `failed` | rc 1, 1773/1789. So danh sách `[FAIL]` đã sắp xếp trả rc 0 và không có delta. `base_selftest.log` |
| `python scripts/tl.py --deterministic determinism-audit --strict --json` | `passed` | rc 0, `ok=true`, 15/15 kiểm tra, mode mặc định `full=false`. `determinism.log` |
| `python scripts/tl.py --deterministic doc-claims-check --strict --json` trên head và baseline | `failed` trên cả hai | rc 2/2. Cùng một cờ cứng L2 `SHA_NOT_A_COMMIT` cho `9941d8af52aeede1c78ea4e232fbe9a8d5272033` tại `docs/PROTOCOL_DA_PHIEN.md:1680`. Object vắng trong kho được cấp. `doc_claims.log`, `base_doc_claims.log` |
| Ruff bare `python -m ruff check --no-cache --select F scripts/tl.py --output-format json` trên head và baseline | `failed` bare, **đạt delta 0** | Ruff 0.15.15, rc 1/1. Cùng 12 F821, 0 F401 và danh sách mã/thông điệp giống nhau. `ruff_head.log`, `ruff_base.log` |
| Ruff pin/probe contract qua `loi_ruff_ci()` của `.claude/dev/ci_dang_ky_test.py` | `passed` | rc 0, `RUFF_CONTRACT 3 []`. `ruff_contract.log` |
| `git diff --check fcb12b3 HEAD` và `git diff --check 64b7f2c HEAD` | `passed` phạm vi packet, `failed` toàn PR | rc 0 và rc 2. Toàn PR báo ba Markdown hard break đã có ở hồ sơ #1514 lượt 8, dòng 3–5. [Hồ sơ](../ops/acceptance/llm-ranh-gioi-khoan/r1/review-8-codex/VERDICT.md#L3) |

Cả hai selftest chạy khi `/tmp/.git` là thư mục rỗng. Ngoài 14 ca cảnh báo trong prompt thuộc nhóm `r973_bootstrap_*`, `wp433_*` và `wp727_tl_gws_refresh`, cả hai cùng đỏ ở `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` và `r268_l2_trichotomy_theo_trang_thai_object`. Hai ca đó dùng Git trong repo tạm. Phép đo xác nhận cùng 16 ID đỏ và thêm một ca #1525 đạt ở head. Gate N/N vẫn đỏ trong môi trường này. [Ca r226](../scripts/tl_selftest.py#L27758) · [Ca r268](../scripts/tl_selftest.py#L29379)

`skipped` trong sáu lệnh prompt là 0. Các gate bổ sung dùng để đối chiếu §5 và ADR-0062. Fixture kiểm tra và file state ignored mà các lệnh head tự sinh trong checkout đã được chuyển ra scratch sau khi tiến trình kết thúc. Readback giữ nguyên HEAD/tree, diff tracked và index đều rc 0. So với snapshot đầu, trạng thái còn `.review/VERDICT.md` và thư mục rỗng `.codex/` đã có sẵn.

## Không đo được

- C1–C5 và C7 dựa trên đọc mã và đối chiếu đặc tả. Lượt này dùng fixture và test sẵn có, cùng một đột biến mã trên bản sao tạm cho C6. Hành vi Word sau Z, hiệu lực toggle trên Word thực và tần suất content control nội dòng trong corpus luật hoặc Google Docs chưa có phép đo bản địa. Tài liệu khai `br`/`cr` là ngắt mềm. Trường, hình, chú thích và các phần tử hiển thị ngoài phạm vi đọc đã công bố được giữ như giới hạn khai báo.
- Windows `required` theo ADR-0060 M3 vì toàn PR thêm dòng Python chứa `encoding=`. Windows và GitHub CI trên exact head đều `not_run`. GitHub readback head, hai lớp check lease từ xa và receipt terminal của launcher chưa đo trong phiên offline. [ADR-0060 M3](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L43)
- Model/effort phục vụ chưa có trường `DO_DUOC` trong bản ghi launcher đang chạy. Snapshot đầu/cuối chỉ chứng minh tình trạng quan sát được tại hai mốc. Receipt terminal, mã thoát lượt Codex và stdout hash thuộc readback sau khi launcher kết thúc. [Protocol §8.1–§8.2](../docs/PROTOCOL_DA_PHIEN.md#L770)

Kết luận cho exact head có 0 P0, 4 P1, 2 P2 và 1 P3 mở. K1 đã đóng trên đường thô. Điều kiện merge ADR-0060 M1 chưa đạt. Hồ sơ lớp lặp được đưa tới Review Rescue Checkpoint theo §12. [ADR-0060 M1](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32) · [Protocol §12](../docs/PROTOCOL_DA_PHIEN.md#L1097)

P2_mo: 2
VERDICT: REQUEST_CHANGES
