# Verdict packet #1525 r1 lượt 1 — Codex

reviewed_sha: 3d247516aaeb0ad3d836a2dc51dda13052fdbe47
reviewed_tree: 983d328568021e96819d86aecc152e17e1d57b76
base_sha: 64b7f2c14776d5d0e1d34a6be4725490956f5bec
base_tree: 0cc14e79cecd2ce44bc4dc6cff92cadb31fd7ee4
continuation_base: fcb12b3873c3bec2c339029136243ed2c804ce05

## Preflight

- PR #1517, revision 1, generation 1, lượt 1/5, Review Class `sensitive`. Bản sao detached có origin `ducthangho/tra-luat`, `core.abbrev=7`, merge base trùng `base_sha`. Kiểm lúc 08:41 UTC ngày 25-11-2026, lease có hạn tới 16:34 UTC.
- SHA-256 của blob đặc tả ở exact head và bản đọc tại checkout cùng là `cde6a98ac43f4be0817969efe2175bf568d8c911c43fe0030f480c14db3c3965`, khớp lease. Hash write set tính theo quy tắc trong lease là `ac1a6cf6c2b059bf35a2bca8a89466fd34805c51e3b4c33ef5409ddc8691d4b2`. Diff toàn PR có 60 đường dẫn. Diff từ `fcb12b3` có 11 đường dẫn sau khi loại 4 tệp hồ sơ #1514 theo prompt. Cả 11 đều thuộc write set #1525. Lease #1525 trỏ r9 bằng `thay_the_cho` và r9 trỏ lại #1525 bằng `da_bi_thay_the`, cùng nhánh `ccr-89c0d2e2-inanqb`. [Đặc tả](../ops/specs/llm-khoan-docx-r1.md) · [Lease #1525](../ops/leases/llm-khoan-docx-r1-g1-claude.yaml) · [Lease #1514 r9](../ops/leases/llm-ranh-gioi-khoan-r9-g1-claude.yaml)
- Reviewer `openai_codex / codex_cli / machine`, run `718da173d81c485c84f7f1f3a08f5492`. `run.json` ghi exact head và prompt hash `919e9d80336d0aa5f95d9ee1b378c043e8d0fae92cc58170b67b0fac65c575dd`, trùng bytes của `prompt.snapshot`. Executor theo lease là `claude / claude_code / machine/local`, phiên giao việc `session_015GtxrZQYT3Vt8PJdXrjEKg`. Môi trường reviewer Linux, Python 3.13.18, Git 2.43.0, Codex CLI 0.172.0, sandbox `workspace-write`.

## Đối chiếu đặc tả r1

| Mục | Trạng thái | Bằng chứng |
| --- | --- | --- |
| §1, bất biến và đối chứng | Đạt trong phạm vi kiểm | Diff giữ `goi`, `duong_api`, `duong_sub`, `_chay_co_moc` và tập cờ CLI. JSON luôn có `can_nguoi_duyet: true` và chọn `pham_vi_kiem` theo việc có danh sách khoản cấu trúc. Ca A4 trong `ca_wp1514` đối chiếu tám khoản và ba kết quả đã lưu `tl/sub/api`, mỗi bản 8/8. [CLI](../scripts/tl_core/ops_misc.py#L3116) · [Ca A4](../scripts/tl_core/llm_route_test.py#L1038) |
| §2.1, đọc ZIP/markup | Đạt ca đã có, còn A4 | Cấu trúc dùng ZIP/ElementTree, ưu tiên `read_member_bounded` khi import được và gọi `strip_markup` trước parse. Đột biến bỏ lọc bị ca đích giết. A4 ghi các cách markup có thể lọt qua hoặc làm sai ranh giới. [Đọc ZIP](../scripts/tl_core/llm_route.py#L540) · [Ca dương](../scripts/tl_core/llm_route_test.py#L1229) |
| §2.1, vùng Điều, khoản, điểm, câu dẫn | Đạt ca đã có, còn A1–A3, A5–A6 | Ca có sẵn xác nhận dừng ở Điều kế, đủ khoản và điểm, từ chối hai tiêu đề trực tiếp, sai số, trộn danh sách, số gõ tay, style trực tiếp và câu dẫn không chuẩn hoặc lặp. Câu dẫn vắng hoặc đúng một đoạn chuẩn qua `fullmatch`. [Chọn vùng](../scripts/tl_core/llm_route.py#L708) · [Câu dẫn](../scripts/tl_core/llm_route.py#L762) · [Ca chặn](../scripts/tl_core/llm_route_test.py#L1253) |
| §2.1, bộ đếm và nhãn | Đạt với fixture chuẩn, còn A2 và A7 | `start` đi vào bộ đếm qua giá trị đầu cấp. `startOverride` thay giá trị đó theo `numId`. Ca có sẵn xác nhận reset mặc định, `startOverride=1` được chấp nhận, danh sách chạy tiếp từ Điều trước bị chặn và `numId` khác có bộ đếm riêng. Nhãn hiển thị và độ liên tục còn các lệch mô tả ở A2. [Bộ đếm](../scripts/tl_core/llm_route.py#L585) · [Ca đối chứng](../scripts/tl_core/llm_route_test.py#L1288) |
| §2.1–2.2, định tuyến và so nguyên văn | Đạt ca đã có, còn A1–A4 | Chữ ký ZIP bật đường `.docx`, cần `--dieu`, cấm số hiệu. `KhongCauTruc` mang văn bản sang đường thô. Lỗi cấu trúc được bắt và trả rc 2. `lech_nguyen_van` dùng danh sách khoản đã cấp, so thứ tự và toàn bộ hai vế. Với oracle đúng, bỏ, gộp, cắt hoặc tráo khoản đều lệch. [Định tuyến](../scripts/tl_core/ops_misc.py#L3027) · [Phép so](../scripts/tl_core/llm_route.py#L931) |
| §2.3, K1 trên đường thô | **ĐÃ VÁ THẬT** cho hai biểu hiện đã nêu | `_RE_DIEM` trả `None` ở cả nguồn có số và mất số, kể cả khi mọi dòng có dấu kết câu. Dòng mở bằng “là” ở nguồn có số rơi vào nhánh dòng không số và trả `None`. Ở nguồn mất số, phép so từ chối nếu thiếu vế thuật ngữ. Các ca cũ chuyển sang truyền khoản cấu trúc ở nơi cần so nội dung có điểm. [Mã](../scripts/tl_core/llm_route.py#L800) · [Ca điểm](../scripts/tl_core/llm_route_test.py#L1164) · [Ca tiếp dòng](../scripts/tl_core/llm_route_test.py#L808) |
| §3, test và đột biến | Đạt các phép đo đã chạy, còn A7 về độ phủ | Bộ ca sẵn có đạt 58/58, giết 112/112 đột biến. Theo dõi nhánh `TinHieuChotCa` ghi đủ 15/15 đột biến `wp1525_*`. Ca tích hợp gọi handler với model giả, kiểm rc 0/5/2 và metadata. [Bảng đột biến](../scripts/tl_core/llm_route_test.py#L1336) · [Ca tích hợp](../scripts/tl_selftest.py#L32230) |

**Biểu hiện còn lại trên đường thô.** Bộ quét vẫn có thể nhận lời dẫn nhóm hoặc hai dòng tách ra từ một khoản nếu mỗi dòng đứng riêng đều có đủ hai vế và dấu kết câu. Mất thụt lề cũng có thể làm số tiểu mục có cùng hình dạng với số khoản kế tiếp được nhận là khoản khi khoản trước đã đủ điều kiện kết thúc và dãy số nhìn thấy vẫn liên tục. Đây là giới hạn hình dạng đã ghi ở verdict #1514 và trong `pham_vi_kiem`. Hai nhánh nối dòng của K1 đã đóng. Các trường hợp cấu trúc dưới đây mở lại lớp `ranh-gioi-khoan` theo cơ chế khác. [Verdict #1514](../ops/acceptance/llm-ranh-gioi-khoan/r1/review-10-codex/VERDICT.md) · [Phạm vi đường thô](../scripts/tl_core/llm_route.py#L773)

## Findings

Các kịch bản dưới đây là kết luận từ luồng mã. P1 dành cho đường có thể cho rc 0 hoặc ghi `--out` với nội dung, số khoản hoặc ranh giới sai ở đầu vào thuộc phạm vi chức năng. P2 dành cho từ chối nguồn dùng được hoặc thiếu phép kiểm acceptance. P3 dưới đây ảnh hưởng hướng dẫn sử dụng. Ngưỡng verdict của prompt và điều kiện merge M1 được áp riêng. [Protocol §8](../docs/PROTOCOL_DA_PHIEN.md#L634) · [ADR-0060 M1–M2](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32) · [ADR-0062](../docs/adr/0062-adr-0060-mac-dinh-va-dong-bang-adr-0054.md)

### A1 [P1] Chọn vùng Điều có thể bỏ khoản trước khi đối chiếu — `scripts/tl_core/llm_route.py:678,709,725`

- **Kịch bản và căn cứ.** Tiêu đề thật có phần thân sau ngắt mềm trong cùng đoạn. `_van_ban_doan` gộp dấu ngắt thành khoảng trắng, regex nhận cả đoạn làm tiêu đề, rồi parser loại toàn bộ khỏi oracle. Nhánh đối xứng xảy ra khi một đoạn nội dung mở bằng chữ giống tiêu đề Điều/Chương/Mục/Phần. Vòng cắt vùng dừng ở đó kể cả đoạn ấy có `numPr` và dãy khoản trước đó hợp lệ. Một tiêu đề ở phần thân, mục lục hoặc trích dẫn có cùng tiền tố cũng có thể làm chọn nhầm vùng hoặc báo trùng.
- **Kịch bản và căn cứ.** Vòng duyệt chỉ giữ `w:p` và sentinel `w:tbl` là con trực tiếp của `w:body`. Khoản dưới content control cấp khối `w:sdt/w:sdtContent` bị bỏ cùng số của nó. Khoản trực tiếp sau đó có thể bị kéo số xuống và cả dãy rút gọn vẫn liên tục. Tại Điều có khoản gõ số tay hoặc mất số và một bảng, `vung` có sentinel nhưng nhánh `KhongCauTruc` chạy trước chốt bảng, chuyển sentinel thành một dòng rỗng. Đường thô bỏ dòng ấy rồi có thể nhận trọn phần văn bản còn lại. Điều này trái §2.1 yêu cầu dừng khi có bảng trong vùng.
- **Đề xuất.** Bảo toàn thứ tự và loại khối của nội dung Điều. Đọc hoặc chặn container chứa nội dung trước khi tạo oracle. Kiểm bảng trước fallback. Chỉ cắt tại tiêu đề đã nhận dạng đủ chắc và giữ bằng chứng về đuôi cùng đoạn hoặc ngắt mềm. Thước đóng lớp cần giữ hoặc chặn khối có khoản bị che, xác nhận bảng ở cả đường có và không có số tự động, và đối chứng với Điều kế thật.

### A2 [P1] Bộ đếm và nhãn tự động có thể khác số Word hiển thị — `scripts/tl_core/llm_route.py:585,613,631,699,745`

- **Kịch bản và căn cứ.** Mỗi `numId` có bộ đếm riêng, nhưng code xóa tất cả cấp sâu hơn mỗi khi cấp nông hơn xuất hiện. Danh sách có `w:lvlRestart` quy định cấp kích hoạt khác, đặc biệt `0` để tiếp tục điểm qua khoản sau, vẫn bị đặt lại. Oracle sẽ chứa nhãn điểm do bộ đọc đánh lại và đầu ra chép nhãn đó có thể qua kiểm. Nhãn ghép có `w:isLgl` cũng có thể bị định dạng sai vì `_nhan` luôn dùng `numFmt` của cấp được tham chiếu. Với khoản, parser dựng `_nhan` rồi dùng thẳng `dem[cap0]` và in lại dạng `N.` mà chưa kiểm nhãn khoản thực sự chứa số cấp đó. `lvlText` cố định hoặc chỉ tham chiếu cấp khác có thể được báo là dãy khoản liên tục.
- **Kịch bản và căn cứ.** Đếm trước vùng Điều chỉ thấy đoạn trực tiếp có `numId` trực tiếp. Mục cùng danh sách đã dùng trong bảng hoặc dưới wrapper trước Điều bị bỏ khỏi bộ đếm. Style kế thừa qua `basedOn`, hoặc đoạn chỉ ghi `ilvl` và thừa hưởng `numId`, cũng qua khe `ngam`. Nếu chỉ dùng style gián tiếp trong Điều, bộ đọc có thể rơi về đường thô và đánh số 1..N cho các định nghĩa dù số thật bắt đầu muộn. Nếu mục bị bỏ nằm trước Điều và mục đích có `numPr` trực tiếp, ứng viên có thể qua ngay đường cấu trúc với số đầu bị hạ xuống 1. Trường hợp style trực tiếp trong fixture đã bị chặn như đặc tả.
- **Đề xuất.** Chỉ khẳng định số Word khi đã tính đúng các đoạn ảnh hưởng đến danh sách đích, cách restart, style hiệu lực và dạng nhãn. Dừng khi thiếu dữ liệu để xác minh. Đo cả `start` khác 1, `startOverride` thay đổi giá trị cơ sở, cấp con tiếp số, nhiều `numId` và số thứ tự bị ảnh hưởng bởi nội dung trước vùng.

### A3 [P1] Phép so có thể lấy từ nối “là” của điểm làm từ nối cấp khoản — `scripts/tl_core/llm_route.py:747,910,951`

- **Kịch bản và căn cứ.** Một khoản mở nhóm không có từ nối cấp khoản hoặc dấu hai chấm ASCII, bên dưới là điểm có từ nối của chính điểm. Parser biết cấp của điểm, nhưng đưa điểm vào khoản dưới dạng chuỗi. `_tu_noi` chỉ dừng khi dòng kế bắt đầu bằng `_RE_DIEM`. Nhãn `upperLetter`, nhãn số kiểu `decimal`, nhãn nhiều chữ cái hoặc nhãn dùng dấu chấm do `lvlText` dựng có thể nằm ngoài mẫu một chữ thường kèm ngoặc đóng. Phép so có thể lấy từ nối trong điểm, coi phần đầu nhóm cộng nhãn và đầu điểm là thuật ngữ cấp khoản, và nhận hai vế đó nếu model trả khớp.
- **Đề xuất.** Truyền thân đoạn mở khoản riêng khỏi điểm vào bộ dò từ nối. So định nghĩa với toàn bộ thân và các điểm đã xác thực sau khi chốt được từ nối trên đoạn mở khoản. Dùng cùng phép kiểm với điểm gõ tay và mọi nhãn tự động được hỗ trợ.

### A4 [P1] Markup có thể để lại chữ gạch ngang hoặc giữ ranh giới đã xóa — `scripts/tl_core/llm_route.py:566,668` · `scripts/docx_markup.py:39,243`

- **Kịch bản và căn cứ.** Bộ lọc so tiền tố XML literal `w:`. WordprocessingML dùng tiền tố khác nhưng cùng namespace vẫn được ElementTree đọc. Run chứa strike theo tiền tố ấy có thể đi nguyên vẹn vào chuỗi `w:t` theo namespace mở rộng. Strike kế thừa từ style cũng không xuất hiện trong run để bộ lọc trực tiếp bắt được. Cả hai có thể để chữ đã bỏ làm oracle của phép so nguyên văn. Với Track Changes xóa dấu đoạn, bộ lọc bỏ dấu sửa đổi cấp `pPr/rPr` nhưng giữ hai `w:p`. Bộ đếm và phép cắt khoản sau đó vẫn dựa vào hai đoạn cũ.
- **Đề xuất.** Giữ luồng lọc chung với `tl extract` và kiểm namespace, định dạng hiệu lực cùng revision tác động đến ranh giới trước khi xác nhận cấu trúc. Từ chối dạng revision chưa thể diễn giải. Đối chứng với strike trực tiếp, chữ mới thêm và tài liệu sạch.

### A5 [P2] Kiểu đánh số ở ngoài Điều có thể chặn cả Điều hợp lệ — `scripts/tl_core/llm_route.py:602,669,705`

- **Kịch bản và căn cứ.** Khoản trong Điều đích dùng danh sách số kiểu `decimal` riêng. Phần khác trong cùng văn bản có chương dùng số La Mã tự động hoặc danh sách có `lvlOverride` tùy chỉnh. Parser gọi `_nhan` cho mọi đoạn số trong body trước khi định vị Điều, và `_doc_danh_so` có thể từ chối override của một `numId` thậm chí không dùng. Điều đúng phạm vi bị rc 2 dù danh sách khác độc lập. Văn bản luật có Chương đánh số La Mã là trường hợp thực tế đáng kiểm. Mức phổ biến của việc dùng numbering tự động cho dạng này chưa đo.
- **Đề xuất.** Định vị vùng trước, giải mã nhãn và xác thực các định nghĩa danh sách cần dùng ở phạm vi Điều, đồng thời tính bộ đếm của đúng các danh sách liên quan từ đầu tài liệu. Kiểm trường hợp danh sách độc lập ngoài Điều và đối chứng khi đưa cùng dạng đánh số vào Điều.

### A6 [P2] Điểm gõ tay dính chữ bị chặn dù có dấu điểm được hỗ trợ — `scripts/tl_core/llm_route.py:528,737`

- **Kịch bản và căn cứ.** Điểm gõ tay sau một khoản có số tự động bắt đầu bằng dấu điểm chữ hoặc dấu gạch được liệt kê, nhưng người soạn không chèn khoảng trắng giữa dấu và thân điểm. §2.1 chỉ yêu cầu đoạn mở bằng dấu điểm. Regex cấu trúc đòi `\s` sau dấu nên rơi vào lỗi đoạn không số. Phần này chỉ ảnh hưởng khả năng đọc đầu vào.
- **Đề xuất.** Chốt hợp đồng cho dấu điểm liền chữ và áp dụng nhất quán. Nếu cần phân biệt gạch điểm với gạch là một phần từ, khai rõ điều kiện trong đặc tả và hướng dẫn.

### A7 [P2] Bộ ca chưa đo độc lập một số hành vi §2.1 theo yêu cầu §3 — `scripts/tl_core/llm_route_test.py:1253,1288,1336`

- **Kịch bản và căn cứ.** Đối chứng `startOverride=1` đặt đè lên cùng giá trị `start=1`, nên kiểm được dạng override được nhận. Bỏ phép thay giá trị nhưng vẫn chấp nhận cú pháp sẽ cho cùng kết quả. Ca bảng chỉ đặt bảng giữa hai khoản đã có số tự động và dùng chung nhánh chặn đoạn không số. Ca định dạng ở cấp khoản dùng `lowerLetter`, một định dạng nói chung được hỗ trợ. Bảng `DOT_BIEN` thiếu mục riêng cho nhánh dựng nhãn từ định dạng không hỗ trợ ở cấp con và cho điều kiện bảng trước fallback. Ca dương dùng nhãn điểm tự động. Chưa thấy ca dương đi qua nhánh nhận điểm gõ tay thực của `doc_dieu_docx`.
- **Đề xuất.** Dùng giá trị override khác giá trị gốc, kiểm từng nhánh với đối chứng đạt và yêu cầu đột biến đúng ca đích. Các test mới thuộc lượt Executor. Lượt này đo bảng đột biến sẵn có.

### A8 [P3] Hướng dẫn đường thô chứa hai quy tắc trái nhau — `docs/GOI_AGENT_DA_NEN.md:373`

Gạch hướng dẫn bắt đầu bằng quy tắc cũ cho phép dòng điểm hoặc dòng nối “là” ở nguồn có số và phần sau của chính gạch công bố chặn cả hai kể từ #1525. Người đọc có thể chọn tệp thô nhiều dòng rồi gặp lỗi. Đề xuất đưa quy tắc một dòng vào câu mở đầu và dẫn tới đường `.docx` cho khoản có điểm. [Hướng dẫn](../docs/GOI_AGENT_DA_NEN.md#L373)

| Lớp | Biểu hiện và hạng cao nhất | Nguồn và phép kiểm đóng lớp |
| --- | --- | --- |
| `ranh-gioi-khoan` | K1 đường thô đã đóng. A1, A3 mở, P1. | K1 ở `fcb12b3873c3bec2c339029136243ed2c804ce05`. Dùng cấu trúc để giữ đủ nội dung đúng Điều và chốt từ nối cấp khoản trước khi ghép điểm. Kiểm vùng đầy đủ và ca từ nối chỉ có ở cấp điểm. |
| `docx-so-hien-thi` | A2, P1 | Head r1. Đối chiếu bộ đếm, style hiệu lực, restart và nhãn với số hiển thị. |
| `docx-markup-du-thao` | A4, P1 | Head r1. Kiểm chữ sau khi lọc và biên đoạn đã được sửa. |
| `docx-kiem-danh-sach-ngoai-vung` | A5, P2 | Head r1. So cùng một Điều khi có và khi bỏ danh sách độc lập bên ngoài. |
| `docx-dau-diem-go-tay` | A6, P2 | Head r1. Kiểm hợp đồng hình dạng điểm gõ tay, có đối chứng đoạn không số. |
| `do-phu-chot-docx` | A7, P2 | Head r1. Xác minh riêng các nhánh §2.1 bằng ca đích và đột biến. |
| `huong-dan-duong-tho` | A8, P3 | Head r1. Đối chiếu toàn bộ hướng dẫn với hành vi một dòng của §2.3. |

## Kết quả test và đột biến

Log JSON, stdout/stderr và mã thoát ở `/tmp/wp1525-review.IqcsYnNr/`. Tắt bytecode Python. Các checkout chính và bản sao có `core.abbrev=7` trong cấu hình Git cục bộ.

| Lệnh | Trạng thái | Mã thoát và bằng chứng dương |
| --- | --- | --- |
| `python scripts/tl_core/llm_route_test.py` | `passed` | rc 0, 58/58 ca, 112/112 đột biến bị giết. `llm_route.log` |
| `python scripts/tl.py --deterministic workflow-audit --strict --json` | `passed` | rc 0, `ok=true`, 26 card, 60 task, 194 lệnh, 0 lỗi và 0 cảnh báo. `workflow.log` |
| `python scripts/tl.py --deterministic golden-test --json` | `passed` | rc 0, `ok=true`, 20/20 ca đạt, 20/20 bản chiếu ổn định và 20/20 byte thô ổn định trong lần đo này. `golden.log` |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | `passed` trên bản sao sạch của exact head | rc 0, `ok=true`, 187/187 tệp, các danh sách sai, thiếu, thừa đều rỗng. Package hash khớp `2d88cc40e618ba63106ef992a1025877bfd14b0edabd22f563f8080e65dc9ad8`. Lượt đầu trên checkout review trả rc 2 vì kiểm kê thêm `.review/VERDICT.md` do reviewer ghi sớm. `release_clean.log` và `release.log` |
| `python ops/lease_publish.py check --root . ops/leases/llm-khoan-docx-r1-g1-claude.yaml` | `passed` cục bộ | rc 0, “ĐĂNG ĐƯỢC”, Issue #1525, neo `64b7f2c14776`, hạn 16:34 UTC. Hai lớp GitHub là `not_run` theo phạm vi của `check`. `lease.log` |
| `python scripts/tl.py --selftest` | `failed` trên head và base | Rc 1 mỗi cây, head **1.774/1.790**, base **1.773/1.789**, transport 12/12 ở cả hai. Cùng 16 ID đỏ. Ca mới `r1525_llm_khai_niem_tep_docx_cau_truc` qua và là khác biệt duy nhất trong danh sách trạng thái. `{rerun-head,rerun-base}.log` |
| `python scripts/tl.py --deterministic determinism-audit --strict --json` | `passed` | rc 0, `ok=true`, 15/15 phép đạt. `determinism.log` |
| `python scripts/tl.py doc-claims-check --strict --json` | `failed` trên head và base | rc 2 cả hai, 131 tệp mỗi lượt, cùng một cờ cứng L2 `SHA_NOT_A_COMMIT` ở `docs/PROTOCOL_DA_PHIEN.md:1680`, delta 0. `git cat-file -t` trên checkout shallow không tìm thấy object `9941d8af52aeede1c78ea4e232fbe9a8d5272033` (rc 128). `doc_claims.log`, `doc_claims_base.log` |
| Adapter `cross-review` gọi `loi_ruff_ci()` ở exact head | `passed` đối với hợp đồng pin/probe | rc 0, `RUFF_CONTRACT 3 []`. `ruff_contract.log` |
| `ruff check --no-cache --select F --output-format concise scripts/tl.py` | `failed` trên head và base, đạt delta 0 | Ruff 0.16.9, rc 1 cả hai, 12 F821, 0 F401 trên từng cây. `cmp` hai output rc 0. `ruff_head.log`, `ruff_base.log` |
| `ruff check --no-cache --select F --output-format concise scripts/tl_core/llm_route.py scripts/tl_core/llm_route_test.py` | `passed` | Ruff 0.16.9, rc 0, không có chẩn đoán F. `ruff_module.log` |

Harness ghi từng bản đột biến trong thư mục tạm, đòi đúng một neo và chỉ tăng bộ đếm khi ca đích ném `TinHieuChotCa`. Chạy lại chính harness bằng `python -B -m pdb scripts/tl_core/llm_route_test.py`, breakpoint có điều kiện `ten.startswith("wp1525_")` ở dòng tăng bộ đếm. Rc 0, 15/15 mục `wp1525_*` tới breakpoint, tổng vẫn 58/58 và 112/112. Trong đó có bỏ lọc strike, reset điểm, dừng ở Điều kế, chặn style, chặn câu dẫn và chặn dòng điểm ở đường thô. SHA-256 `mutation-trace.log` là `7ff8f4665a7962e38494e6cdcdfb94037f1500d8086ea5fa60bb60f020859c16`. [Harness](../scripts/tl_core/llm_route_test.py#L1524)

Lần selftest đầu có thêm biến môi trường ghim `core.abbrev=7`. Đã chạy lại cả hai bản sao detached chỉ với cấu hình Git cục bộ để phép đo `r226` có thể đổi cấu hình trong repo fixture. Kết quả hai lần giống nhau. `cmp` tập ID đỏ head/base rc 0. `cmp` toàn bộ trạng thái sau khi bỏ đúng dòng ca mới của head cũng rc 0. Có 14 ID đã báo trong prompt với `/tmp/.git` rỗng hiện diện, gồm 8 `r973_bootstrap_*`, 5 `wp433_*` và `wp727_tl_gws_refresh`. Hai ca `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` và `r268_l2_trichotomy_theo_trang_thai_object` cũng đỏ trên cả hai cây sau khi bỏ biến ghim. Delta số ca đỏ là 0. Điều kiện N/N còn thiếu. SHA-256 danh sách ID đỏ ở mỗi cây là `e941799aa91a5070e1a1967a78d7f795cb80c8566c98e6a724aedb217b1acd2d`.

Cả sáu lệnh trong prompt đã chạy. Không có lệnh nào mang trạng thái `skipped`.

## Không đo được

- Các dạng ở Findings cần mẫu ngoài bộ ca sẵn có để kiểm trực tiếp với Word và Google Docs. Tần suất gặp trên tài liệu thực và cách Word hiển thị một cấp thiếu `w:start` chưa đo. Bộ đọc dùng giá trị dự phòng 1. Lượt này dùng ca và fixture có sẵn.
- Windows `required` theo ADR-0060 M3. Diff toàn PR thêm dòng chứa `encoding=` trong `scripts/tl_selftest.py` và đặc tả r9 có yêu cầu Windows bản địa. Windows bản địa, CI exact head, GitHub và các phép gọi model thật đều `not_run` trong lượt offline. [ADR-0060 M3](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L43) · [Đặc tả r9 §3](../ops/specs/llm-ranh-gioi-khoan-r9.md#L117)
- Model và effort phục vụ là `KHONG_DO_DUOC` từ evidence hiện có. `run.json` còn `dang_chay` tại lần đọc. Launcher chỉ có thể xác nhận trạng thái terminal, rc con và SHA-256 stdout sau khi reviewer kết thúc.

## Readback và kết luận

`git rev-parse HEAD 'HEAD^{tree}'` khớp đầu và cuối ở checkout review. `git diff --exit-code HEAD` và `git diff --cached --exit-code` đều rc 0. Hai thư mục ignored do test sinh ở lần đầu đã được chuyển khỏi checkout sang scratch. Cuối lượt status checkout có `.codex/` từ đầu và `.review/VERDICT.md`. Phép kiểm trước/sau xác nhận delta quan sát được. Cây Executor ở ngoài phạm vi quan sát.

0 P0, 4 P1, 3 P2, 1 P3 mở trên 7 lớp. PR chưa đủ điều kiện merge theo ADR-0060 M1. Các P1 đều liên quan tới xác minh nguyên văn trên đường `.docx`. K1 đã đóng ở đường thuần văn bản.

P2_mo: 3
VERDICT: REQUEST_CHANGES
