# Verdict packet #1525 r7 lượt 7 — Codex
reviewed_sha: 4badb3d603e2d5b7bf6670798255cd38bc1003e8
VERDICT: REQUEST_CHANGES

reviewed_tree: 28dea9ec21126d97e484cd3fb044cb30f43ee936

base_sha: 64b7f2c14776d5d0e1d34a6be4725490956f5bec

## Preflight

- Checkout rời của `ducthangho/tra-luat`, HEAD detached, `core.abbrev=7`. Merge-base khớp base. Đối chiếu 8 tệp thay đổi từ `60b5c32` (bản vá r7), 46 tệp từ `fcb12b3873c3bec2c339029136243ed2c804ce05` (mốc #1514) và 90 tệp từ base (toàn PR). Bỏ 4 hồ sơ acceptance #1514 theo prompt, 42/42 đường dẫn thuộc write set 46 mục. SHA-256 của write set sắp xếp, nối LF và kết thúc LF là `8b14d91156fb7e5b1ca31fc5f03bb349ba40d7792d41cca5f7a0a3a4dc9af6f9`.
- Spec r7 có blob `fc18cdd6eb7a54f44e54b5052184a63f709bf691`. SHA-256 của blob và tệp local cùng là `dd89b33f189e6b5ac70252a9f388e0a68bc243427c84eb03d44e372a2bb5c278`, khớp lease revision 7, generation 1, class và effective class `sensitive`. Lease còn hạn tới 21:31 UTC ngày 25-11-2026. Đã kiểm 7/7 cặp `thay_the_cho`/ `da_bi_thay_the` từ #1514 r9 ↔ #1525 r1 đến r6 ↔ r7. Lượt hiện tại dùng suất cuối 7/7. [Đặc tả](../ops/specs/llm-khoan-docx-r7.md) · [Lease r7](../ops/leases/llm-khoan-docx-r7-g1-claude.yaml) · [Lease #1514 r9](../ops/leases/llm-ranh-gioi-khoan-r9-g1-claude.yaml#L97)
- Executor theo lease là `claude / claude_code / machine/local`, phiên `session_015GtxrZQYT3Vt8PJdXrjEKg`. Reviewer `openai_codex / codex_cli / machine`, run launcher `639f7a6443764b6781152c266e9b9df9`, `codex-cli 0.172.0`, sandbox `workspace-write`, approval `never`. SHA-256 của prompt `36ec44233634d996549378e0a9e6580e14e0cf1b7309eb949a04a159d5295489` khớp metadata run. Checkout độc lập với phiên Executor.

## Đối chiếu lượt 6 và đặc tả r7

Lượt 6 neo `6781d1187c1a500b530e56017e4e2625a7dc990e`. Các đối chiếu dưới đây dùng quy tắc thay thế tuần tự của §2.4–§2.9. Thay đổi hợp đồng r7 về tệp một Điều có chỉ thị chủ kho ghi trong spec và lease. [Verdict lượt 6](../ops/acceptance/llm-khoan-docx/r1/review-6-codex/VERDICT.md) · [§2.9](../ops/specs/llm-khoan-docx-r7.md#L118)

| Mục | Trạng thái | Bằng chứng |
| --- | --- | --- |
| F1 · A1/B1/C1/D1/E1 · §2.9 | **HẾT ĐỐI TƯỢNG do hợp đồng r7** với lỗi cắt đuôi cũ | Tiêu đề đích là đoạn có nội dung đầu tiên. Vùng là tất cả đoạn sau đó. Đoạn giống tiêu đề khớp regex làm dừng, kể cả có số tự động. Bảng/khối lạ làm dừng ở mọi vị trí. Đột biến bỏ kiểm số Điều đầu và đột biến nhận thêm tiêu đề đều bị bắt. Cửa kiểm tiêu đề hiện còn một chặn oan riêng ở G6. [Mã](../scripts/tl_core/llm_route.py#L917) · [Ca F1](../scripts/tl_core/llm_route_test.py#L1363) |
| F2 · A6/C3/D6 · §2.9 | **ĐÃ VÁ THẬT** ở hành vi | Đoạn có chữ nhưng không có số sau khoản đầu trả `ValueError` chung cho điểm tay, tiếp dòng và khoản mất số. Đoạn cấp con tự động cùng danh sách vẫn được ghép. Dấu phân cách kiểm trên nguyên chữ của đoạn. Phép đột biến chung hiện bị ca đoạn thường bắt trước ca điểm tay, xem G5. [Ghép cấp](../scripts/tl_core/llm_route.py#L972) · [Chốt dấu](../scripts/tl_core/llm_route.py#L1006) · [Ca điểm tay](../scripts/tl_core/llm_route_test.py#L1355) |
| F3 · §2.9 | **VÁ MỘT PHẦN** | Định nghĩa, tham chiếu abstract, style và đoạn đều qua `_so_id`. Ca khác dạng số và ca trùng `numId` chết khi bỏ chốt. Cơ chế đếm phần trước Điều mà lượt 6 nêu hết đối tượng. Cặp khóa không phải số vẫn có thể tự khớp, xem G1. [Chuẩn hóa](../scripts/tl_core/llm_route.py#L574) · [Định nghĩa trùng](../scripts/tl_core/llm_route.py#L620) · [Ca dương](../scripts/tl_core/llm_route_test.py#L1316) |
| F4 · §2.9 | **VÁ MỘT PHẦN** | Giá trị chạy ở cấp hiện tại trên 999 bị chặn. Ca có `start` lớn, `startOverride` lớn và vượt trần do tăng số đều có mặt. Đột biến bỏ trần chết trên ca tăng số. Giá trị cấp tổ tiên được điền trực tiếp từ `start` hoặc override còn lách chốt, xem G3. [Bộ đếm](../scripts/tl_core/llm_route.py#L902) · [Ca F4](../scripts/tl_core/llm_route_test.py#L1404) |
| F5 · E6 · §2.9 | **ĐÃ VÁ THẬT** | `lvlOverride` ngoài 0–8 có ca riêng. `wp1525_ilvl_override_ngoai_mien` chết đúng tín hiệu ca ấy. Đoạn trỏ cấp ngoài miền dừng ở xác thực cấp không có định nghĩa trước khi dựng nhãn. [Override](../scripts/tl_core/llm_route.py#L636) · [Xác thực cấp đoạn](../scripts/tl_core/llm_route.py#L957) · [Ca F5](../scripts/tl_core/llm_route_test.py#L1400) |
| F6 · B4/B6/C5 · §2.5–§2.9 | **ĐÃ VÁ THẬT** với các phần tử đã báo | `ptab` đổi thành khoảng trắng. Mốc move cân theo số lần xuất hiện của từng khóa trong mỗi họ move, mốc lẻ trả `ValueError`. Ca dương đồng thời bỏ chữ `moveFrom`. Đột biến bỏ `ptab`, bỏ chốt cân và từ chối mốc nội dòng chết riêng. So sánh danh sách đã sắp xếp chưa xác nhận thứ tự hoặc ngữ nghĩa của các mốc, xem phần chưa đo. [Danh sách phần tử](../scripts/tl_core/llm_route.py#L529) · [Chốt cân](../scripts/tl_core/llm_route.py#L882) |
| A2/B2/C2/D2 · §2.4–§2.7 | **VÁ MỘT PHẦN** ở lớp số Word | Mặc định `start=0`, override 5→1, reset cấp con trực tiếp, nhãn sau Z và chốt restart section có đối chứng. Tách bộ đếm theo `numId`, từ chối danh sách khác và chặn cấp gắn style hoặc số chỉ qua style trong Điều. Nhảy cấp chưa được xác thực, xem G1/G3. Duyệt và đếm trong bảng của B2/C2 hết đối tượng. [Định nghĩa](../scripts/tl_core/llm_route.py#L586) · [Đếm và phân vai](../scripts/tl_core/llm_route.py#L902) · [Ca dương](../scripts/tl_core/llm_route_test.py#L1250) |
| A3/C3/D6 · §2.4/§2.6/§2.7 | **ĐÃ VÁ THẬT** cho các biểu hiện cũ | Chốt dấu phân cách chạy trên chữ mỗi đoạn. Lấy “là” từ đoạn mở khoản, kiểm định nghĩa tới hết các điểm. Ca có “là” chỉ ở điểm nhãn chữ hoa bắt đột biến quay về quét cả khoản. Phân vai điểm tay cũ của D6 hết đối tượng. [Phép so](../scripts/tl_core/llm_route.py#L1190) · [Ca A3](../scripts/tl_core/llm_route_test.py#L1280) |
| A4/B3/C4/D3/E2/E5 · §2.4–§2.8 | **ĐÃ VÁ THẬT** cho các biểu hiện cũ, lớp markup còn G2 | XML gốc giữ ranh giới. Gạch đơn và kép tính độc lập, nhiều tầng bật trả lỗi và tắt trực tiếp có đối chứng. Chốt revision dấu đoạn còn trên XML gốc. Đột biến regex cũ và đọc lại chữ `moveFrom` bị bắt. Nợ ở `docx_markup.py` đã khai trong E5. [Lọc run](../scripts/tl_core/llm_route.py#L778) · [Dấu đoạn](../scripts/tl_core/llm_route.py#L877) · [Ca E5](../scripts/tl_core/llm_route_test.py#L1306) |
| A5 / E3 / E4 | **HẾT ĐỐI TƯỢNG do hợp đồng r7** cho nội dung ngoài Điều và xử lý trong ô | Tệp một Điều chặn mọi bảng, nên hàng/ô bị sửa và metadata ô đều hết đường chạy. Định nghĩa danh sách không dùng vẫn có ca dương khi tồn tại cùng tệp. [Chốt toàn tệp](../scripts/tl_core/llm_route.py#L920) · [Ca A5](../scripts/tl_core/llm_route_test.py#L1276) |
| B5/B6/C5/D5 | **ĐÃ VÁ THẬT** cho các biểu hiện cũ | Thân mở bằng số thập phân đi qua. Duyệt wrapper hợp lệ cấp khối/nội dòng và bỏ metadata của chúng. Strict được chặn với chẩn đoán theo giới hạn đã khai. [Ca dương và Strict](../scripts/tl_core/llm_route_test.py#L1289) |
| A7/B7/C6/D4/E5/F5 · §3 | **VÁ MỘT PHẦN** khi xét chốt hiện hành | Các ca riêng cho override, bảng, tiêu đề lạ/ngắt, markup nguồn và cấp override còn có tín hiệu. Bảng-trước-fallback và các trường hợp ranh giới theo tiền tố cũ hết đối tượng. Mô tả “dừng ở Điều kế tiếp” ở §3 thuộc hợp đồng trước F1, phép đo r7 kiểm từ chối thêm tiêu đề. Điểm tay và định danh abstract còn lỗ bằng chứng ở G5. [Ca chặn](../scripts/tl_core/llm_route_test.py#L1344) · [DOT_BIEN](../scripts/tl_core/llm_route_test.py#L1464) |
| A8/B8/C7 · §1–§2.3 | **ĐÃ VÁ THẬT** cho hướng dẫn cũ | Hướng dẫn đường thô một dòng, DOCX dùng số trực tiếp, nhãn cấp khoản `%N.` hoặc `%N)`, tệp một Điều và điểm tự động. [Hướng dẫn](../docs/GOI_AGENT_DA_NEN.md#L369) |
| §1 và §2.2 · CLI | **ĐẠT** trên dạng đã đo | ZIP được nhận theo chữ ký, cần `--dieu` và nguồn tệp riêng. Lỗi cấu trúc phổ biến trả rc 2. D1 đã bỏ `KhongCauTruc`, Điều không có numbering báo lỗi thay cho fallback. Cờ `can_nguoi_duyet: true`, phạm vi kiểm theo tuyến, giao diện cờ và định tuyến model vẫn theo hợp đồng. Fixture Điều 3 và ba đầu ra lưu đạt 8/8 từng bản. [Handler](../scripts/tl_core/ops_misc.py#L3017) · [Đầu ra](../scripts/tl_core/ops_misc.py#L3123) · [Đối chứng](../scripts/tl_core/llm_route_test.py#L1034) |
| K1 (#1514 r9) · §2.3 | **ĐÃ VÁ THẬT** cho cả hai nhánh ghép thô | `_RE_DIEM` trả `None` trên cả nguồn có số và mất số. Dòng tiếp mở bằng “là” ở nguồn có số đi vào nhánh từ chối dòng không số. Ở nguồn mất số dòng ấy không có vế thuật ngữ để phép so chấp nhận. Hai đột biến điểm và bỏ qua dòng không số đều bị bắt. [Đường thô](../scripts/tl_core/llm_route.py#L1046) · [Ca điểm](../scripts/tl_core/llm_route_test.py#L1170) · [Ca “là”](../scripts/tl_core/llm_route_test.py#L808) |
| §2.1–§2.9 · Câu dẫn và so nguyên văn | **ĐẠT** khi đầu vào phép so phản ánh đúng nguồn | Đường cấu trúc nhận tối đa một câu dẫn chuẩn trước khoản đầu. Đường thô chỉ bỏ dòng đầu khớp toàn mẫu. Kiểm số và vị trí, đủ số mục và toàn bộ hai vế nên loại được đầu ra tự bỏ, cắt, gộp hoặc tráo khoản. Mã vẫn gộp khoảng trắng trong dòng như quy ước, giữ ranh giới dòng giữa các điểm. [Câu dẫn DOCX](../scripts/tl_core/llm_route.py#L1003) · [Câu dẫn thô](../scripts/tl_core/llm_route.py#L1059) · [Phép so](../scripts/tl_core/llm_route.py#L1177) |

**Lớp `ranh-gioi-khoan` trên đường thô.** Vẫn có thể tách lời dẫn nhóm hoặc đoạn tiếp mà mỗi dòng mang đủ hai vế và dấu kết như một định nghĩa độc lập sau khi mất bố cục. Nguồn có số cũng có thể đánh đồng tiểu mục với khoản kế nếu các số nhìn thấy liên tục và các dòng đều có hình dạng định nghĩa. Đây là giới hạn đã công bố của đường thô. TXT đã làm phẳng markup không giữ bằng chứng về chữ đã bỏ. Với số hiệu, `tl extract` vẫn có thể trả văn bản kèm cảnh báo markup. Handler chuyển tiếp cảnh báo và có thể xác minh trên bản đó khi extract trả rc 0 và nguồn không chạm CAP. Đây là đường kế thừa đã ghi ở lượt 6. [Phạm vi đường thô](../docs/GOI_AGENT_DA_NEN.md#L369) · [Cảnh báo fallback extract](../scripts/tl_core/extract_cache.py#L255) · [Chuyển tiếp cảnh báo](../scripts/tl_core/ops_misc.py#L3083)

## Findings

### G1 [P1] Bộ đếm có thể dựng số hoặc nhãn từ định danh hay cấp chưa hợp lệ — `scripts/tl_core/llm_route.py:574`, `:908`

**Kịch bản và căn cứ.** Có hai đường cùng làm sai dữ liệu đánh số trước phép so.

- `_so_id` trả lại giá trị gốc khi đổi sang số thất bại. Nếu cùng một khóa phi số xuất hiện ở định nghĩa và tham chiếu, tra từ điển vẫn thành công. Một khóa abstract phi số cũng được nối như vậy. Mã có thể dựng dãy khoản liên tục từ một định nghĩa vi phạm điều kiện ID số nguyên của F3. Cùng đường này còn nhận một số dạng mà `int()` hiểu ngoài cách viết số nguyên thập phân của OOXML.
- Dưới một khoản cấp gốc, có một điểm nhảy đến cấp sâu khi cấp trung gian chưa có đoạn. Vòng `setdefault` đánh dấu cấp trung gian bằng đúng `start` hoặc override, dù chưa có mục nào ở cấp đó. Khi điểm đầu tiên của chính cấp trung gian xuất hiện, giá trị bị tăng tới `start + 1`. Trạng thái giữ giá trị để dựng nhãn cấp tổ tiên và trạng thái đã thực sự đánh số dùng chung một từ điển. Mã không từ chối bước nhảy cấp và cũng không kiểm liên tục số ở cấp điểm. Ca dương hiện có chỉ đo reset cấp con trực tiếp.

**Hạng P1.** Bộ đọc dùng chính số và nhãn vừa dựng làm nguồn để so. Đầu ra chép lại nhãn sai có thể qua kiểm theo cấu trúc. Đây là suy luận luồng mã và hợp đồng `start`. Cách Word hiển thị chuỗi nhảy cấp cụ thể chưa được đo. [Chuẩn hóa ID](../scripts/tl_core/llm_route.py#L574) · [Ghép định nghĩa](../scripts/tl_core/llm_route.py#L620) · [Bộ đếm](../scripts/tl_core/llm_route.py#L902) · [Dựng nhãn](../scripts/tl_core/llm_route.py#L716)

**Đề xuất.** Xác thực ID theo miền số nguyên tại cả nơi khai báo và nơi tham chiếu. Tại bộ đếm, giữ riêng cấp đã có mục khỏi giá trị dùng để thay nhãn tổ tiên, hoặc báo cấu trúc không hỗ trợ khi nhảy qua cấp chưa diễn giải được. Phép kiểm đóng lớp cần đối chứng các cách viết hợp lệ của cùng ID, ID không hợp lệ, hai danh sách riêng, và điểm đầu tiên ở cấp trung gian sau bước nhảy với `start`/override. Chốt từ chối nhảy cấp có thể chặn danh sách hợp lệ được chỉnh thụt lề trong Word, nên đối chiếu số Word trước khi hỗ trợ dạng đó.

### G2 [P1] Kiểu dùng để gạch bỏ chữ có thể bị bỏ qua khi chỉ đọc tên part mặc định — `scripts/tl_core/llm_route.py:650`, `:783`

**Kịch bản và căn cứ.** Phần chính và numbering ở tên mặc định, còn tài liệu liên kết styles part bằng một target nội bộ khác. Run thừa kế gạch ngang từ character style trong part đó và không có gạch trực tiếp. `_doc_kieu` chỉ mở `word/styles.xml`; thiếu tệp thì dùng bảng kiểu rỗng. `_dem_bat_trong_chuoi` gặp `rStyle` chưa biết trả 0, và bộ đọc giữ chữ. Tệp vì vậy có thể cho một khoản đủ dãy số và đủ hai vế, nhưng chứa chữ gạch bỏ. Repository cũng dùng quan hệ `relationships/styles` khi dựng DOCX, với target mặc định do bộ dựng chọn. Nơi đọc hiện chưa xác nhận tên cố định chính là target đang liên kết. [Đọc kiểu](../scripts/tl_core/llm_route.py#L650) · [Tính gạch theo chuỗi kiểu](../scripts/tl_core/llm_route.py#L696) · [Nạp chữ run](../scripts/tl_core/llm_route.py#L778) · [Quan hệ styles của bộ dựng trong kho](../scripts/tl_core/the_thuc.py#L1804)

**Hạng P1.** Chữ đã bỏ có thể xuất hiện trong chính chuỗi được dùng để xác minh và đi vào đầu ra rc 0. Các ca gạch kiểu hiện có đều đưa styles vào tên mặc định. Mức độ xuất hiện của tên part khác mặc định trong Word hoặc Google Docs chưa đo.

**Đề xuất.** Giải quan hệ part nội bộ đang hiệu lực và đọc qua cùng chốt giới hạn ZIP, hoặc báo không hỗ trợ khi quan hệ styles trỏ ngoài dạng đã triển khai. Phép kiểm đóng lớp cần so cùng nội dung và style có gạch qua target mặc định và target khác tên, đồng thời giữ đối chứng trực tiếp và khi tài liệu thật sự không cần styles. Nếu áp chốt cho mọi `rStyle` thiếu, có thể từ chối tệp Word có tham chiếu dư, nên xác định lỗi quan hệ riêng với lỗi tham chiếu không phân giải được.

### G3 [P2] Giá trị khởi tạo của cấp tổ tiên đi vòng qua trần 999 — `scripts/tl_core/llm_route.py:908`, `:727`

**Kịch bản và căn cứ.** Khi gặp điểm sâu hơn, đoạn mã kiểm trần cho `dem[il]`, rồi sao `start` của các cấp tổ tiên chưa có vào cùng bảng mà không kiểm trần. `_nhan` đọc những giá trị đó khi `lvlText` tham chiếu cấp tổ tiên. Nếu tổ tiên trung gian có định dạng chữ, đường nhân chuỗi trong `_chu_cai` dùng giá trị trên trần. Cả nguồn `start` và `startOverride` đều tới được chỗ khởi tạo này. [Trần và khởi tạo cấp tổ tiên](../scripts/tl_core/llm_route.py#L902) · [Thay nhãn](../scripts/tl_core/llm_route.py#L716)

**Hạng P2.** Vi phạm F4 và có thể tạo nhãn quá dài hoặc làm cạn tài nguyên tiến trình. Ca bỏ trần hiện có chỉ đi qua bộ đếm cấp hiện hành.

**Đề xuất.** Kiểm miền khi tạo mọi giá trị mà nhãn có thể tham chiếu, gồm giá trị khởi tạo, trước khi dựng chuỗi. Phép kiểm đóng lớp cần bao phủ cấp trung gian chưa có đoạn với cả hai nguồn giá trị bắt đầu và giữ đối chứng giới hạn hợp lệ. Nếu áp trần ngay lúc khai báo, chỉ chặn định nghĩa đang được dùng để giữ hành vi A5 với định nghĩa dư.

### G4 [P2] Ngắt trang hoặc ngắt cột chủ động bị coi là ngắt dòng mềm — `scripts/tl_core/llm_route.py:804`

**Kịch bản và căn cứ.** Ngắt trang hoặc ngắt cột chủ động trong Word được lưu dưới dạng `w:br` có loại. Handler đặt `ngat=True` cho mọi `w:br`. Ngay cả ngắt trang nằm riêng giữa hai đoạn đã rõ số cũng làm rc 2, trong khi chốt và hướng dẫn chỉ công bố chặn ngắt dòng mềm. Mốc phân trang tự động `lastRenderedPageBreak` được bỏ qua. [Các loại phần tử run](../scripts/tl_core/llm_route.py#L538) · [Chốt ngắt](../scripts/tl_core/llm_route.py#L804) · [Hướng dẫn DOCX](../docs/GOI_AGENT_DA_NEN.md#L383)

**Hạng P2.** Đây là chặn oan một thao tác phân trang thường dùng trong Word. Chặn tệp nhiều Điều, bảng, ngắt dòng mềm, trường và Strict đều là giới hạn đã công bố.

**Đề xuất.** Phân biệt ngắt trang/cột thuần trình bày ở ranh giới đoạn với ngắt mềm, rồi đo cả dạng nằm giữa chữ để tránh nuốt ranh giới. Thử trên export thực trước khi khẳng định tập biến thể của Google Docs.

### G5 [P2] Đột biến có sẵn chưa khóa riêng điểm gõ tay và chuẩn hóa abstract ID — `scripts/tl_core/llm_route_test.py:1355`, `:1316`

**Bằng chứng.** `wp1525_gop_doan_khong_so` chết ở đoạn thường giữa hai khoản. Ca điểm tay gộp hai loại dấu trong cùng một mẫu. Dấu đóng ngoặc lẻ của điểm chữ có thể chặn mẫu ngay cả khi dạng dấu gạch lọt. Ca dương khác dạng số và ca âm trùng ID hiện đo `numId` ở tầng danh sách. Chúng không độc lập đo `abstractNumId`. Kết quả hai đột biến bổ sung trên bản sao tạm được ghi dưới đây. [Ca âm F2](../scripts/tl_core/llm_route_test.py#L1355) · [Ca dương F3](../scripts/tl_core/llm_route_test.py#L1316) · [Các đột biến](../scripts/tl_core/llm_route_test.py#L1464)

**Hạng P2.** Đây là lỗ trong bằng chứng đột biến theo §3, kể cả khi các hành vi đã nêu trong F2 và chuẩn hóa abstract ID hiện có trong runtime.

**Đề xuất.** Đo từng điểm tay độc lập, nhất là dấu gạch, và đo các cách viết tương đương của abstract ID qua tham chiếu tách biệt với `numId`. Giữ ca dương điểm tự động cùng danh sách. Khi kiểm chẩn đoán, khóa loại lỗi hoặc tính chất đầu ra để tránh bắt cứng câu chữ.

### G6 [P2] Chốt số Điều từ chối tiêu đề DOCX viết hoa dù tiêu đề khớp mẫu F1 — `scripts/tl_core/llm_route.py:926`

**Kịch bản và căn cứ.** Cửa tiêu đề đích dùng biểu thức phân biệt hoa thường trước `_RE_TIEU_DE_TRON`, vốn có `re.IGNORECASE`. Tiêu đề DOCX viết hoa hoàn toàn, có số Điều và dấu câu đúng hình dạng, dừng trước chốt được F1 chỉ định. Hướng dẫn nêu giới hạn viết hoa cho đường thô. [Mẫu F1](../ops/specs/llm-khoan-docx-r7.md#L119) · [Chốt số Điều](../scripts/tl_core/llm_route.py#L925) · [Mẫu tiêu đề](../scripts/tl_core/llm_route.py#L74) · [Hướng dẫn](../docs/GOI_AGENT_DA_NEN.md#L369)

**Hạng P2.** Chặn oan tiêu đề đích có số Điều xác định. Tiêu đề có nội dung dư hoặc tên Điều ngoài mẫu vẫn thuộc giới hạn đã khai.

**Đề xuất.** Dùng một mẫu cho tiêu đề DOCX và lấy số Điều từ chính lần khớp để so với `--dieu`. Đo ca viết hoa và giữ đối chứng sai số, dính nội dung hoặc có số tự động. Giữ riêng quy tắc đường thô nhằm tránh nới phạm vi của #1514.

### Lịch sử theo lớp

| Lớp | Finding và trạng thái | Phép kiểm đóng lớp |
| --- | --- | --- |
| `ranh-gioi-khoan` | F1 hết đối tượng theo quyết định r7, F2 và K1 đóng ở hành vi đã báo. G6 P2 còn ở cửa tiêu đề đích. | Xác nhận đúng số Điều, tiêu đề viết hoa hợp lệ, sai số, khối sau tiêu đề và điểm tay độc lập. |
| `docx-so-hien-thi` | A2/B2/C2/D2/F3 → G1 P1. | So ID hợp lệ/không hợp lệ và số/nhãn Word khi cấp con nhảy cấp hoặc khi cấp cha tăng. |
| `docx-markup-du-thao` | A4/B3/C4/D3/E2/E5 còn đối chứng dương, có biểu hiện khác ở G2 P1. | Giữ loại chữ đã bỏ với cùng kiểu ở hai tên part hợp lệ và kiểm hành vi khi thiếu quan hệ/part. |
| `docx-gioi-han-bo-dem` | E6/F4 → G3 P2. | Đo trần tại cấp mục hiện tại và cấp chỉ được tham chiếu trong nhãn. |
| `docx-chu-hien-thi` | Hai biểu hiện F6 đã sửa, G4 P2 còn ở dấu ngắt trang/cột. | Đo ngắt chủ động ở biên đoạn, giữ từ chối ngắt mềm. |
| `do-phu-chot-docx` | A7/B7/C6/D4/E5/F5 → G5 P2. | Đột biến hẹp chết đúng từng ca đích và giữ đối chứng dương. |

Tập F1–F6 có 5 lớp mở ở lượt 6. Lượt 7 có 6 finding trên 6 lớp mở, gồm 5 lớp còn mở từ tập đó và 1 lớp tái mở về markup. Tỷ lệ đóng lớp trên tập 5 lớp là 0/5. Việc bỏ cơ chế cắt Điều theo tiền tố có quyết định thay hợp đồng ở §2.9. [Lịch sử lượt 6](../ops/acceptance/llm-khoan-docx/r1/review-6-codex/VERDICT.md#L79) · [Protocol §8.3](../docs/PROTOCOL_DA_PHIEN.md#L812) · [Điều kiện checkpoint](../docs/PROTOCOL_DA_PHIEN.md#L1129)

## Kết quả test và đột biến

Linux x86_64, Python 3.13.18, Git 2.43.0, Ruff 0.15.15. Tắt ghi bytecode Python. Log, mã thoát, hash và bản sao detached của head/base nằm trong `/tmp/wp1525-r7-review.xCqtHZzW/`. Hai clone đo dùng object Git local và cùng `core.abbrev=7`. Tree của base là `0cc14e79cecd2ce44bc4dc6cff92cadb31fd7ee4`.

| Lệnh | Trạng thái | Mã thoát và bằng chứng |
| --- | --- | --- |
| `python scripts/tl_core/llm_route_test.py` | `passed` | Rc 0, **59/59 ca**, **157/157 đột biến có sẵn bị giết**, trong đó 59/59 mang tên `wp1525_*`. `route.log`. |
| `python scripts/tl.py --deterministic workflow-audit --strict --json` | `passed` | Rc 0, `ok=true`, 26 card, 11 nhóm, 60 task, 194 lệnh hiện diện, 0 lỗi và 0 cảnh báo. `clean-workflow.log`. |
| `python scripts/tl.py --deterministic golden-test --json` | `passed` | Rc 0, `ok=true`, **20/20** ca đạt, 20/20 bản chiếu và 20/20 byte thô ổn định ở lượt đo này. `clean-golden.log`. |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | `passed` trên head sạch | Rc 0, `ok=true`, **187/187** tệp, 0 thừa/sai/thiếu, hash gói khớp `5ce5ef385f72c243945efab940294722e8c80de76149fe5dd715c5674c9071e8`. Lượt đầu ở checkout đã có verdict trả rc 2, tệp thừa duy nhất là `.review/VERDICT.md`. `clean-manifest.log`, `manifest.log`. |
| `python ops/lease_publish.py check --root . ops/leases/llm-khoan-docx-r7-g1-claude.yaml` | `passed` cục bộ | Rc 0, “ĐĂNG ĐƯỢC”, #1525, neo base `64b7f2c14776`, hết hạn 21:31 UTC. Lệnh báo hai lớp kiểm GitHub nằm ngoài phép kiểm cục bộ. `lease.log`. |
| `python scripts/tl.py --selftest` | `failed` trên head và base | Rc 1 cả hai. Head **1.774/1.790**, base **1.773/1.789**, transport **12/12** cả hai. Tập 16 ca đỏ trùng hoàn toàn. Ca mới `r1525_llm_khai_niem_tep_docx_cau_truc` đạt, xác nhận rc 0/5/2 qua model giả. `clean-head-selftest.log`, `base-selftest.log`. |
| `python scripts/tl.py --deterministic determinism-audit --strict --json` | `passed` | Rc 0, `ok=true`, **15/15**. `head-determinism.log`. |
| `python scripts/tl.py --deterministic doc-claims-check --strict --json` | `failed` trên head và base | Rc 2 cả hai, 131 tệp quét và cùng một cờ cứng `SHA_NOT_A_COMMIT` cho `9941d8af52aeede1c78ea4e232fbe9a8d5272033` ở protocol dòng 1680. Object thiếu trong checkout shallow được giao. Delta cờ cứng 0. `head-doc-claims.log`, `base-doc-claims.log`. |
| `python -B -c 'import runpy,sys; m=runpy.run_path(".claude/dev/ci_dang_ky_test.py"); errors,count=m["loi_ruff_ci"](); print("RUFF_CONTRACT",count,errors); sys.exit(bool(errors) or count == 0)'` | `passed` ở phạm vi hợp đồng pin/probe Ruff | Rc 0, `RUFF_CONTRACT 3 []`. `head-ruff-contract.log`. |
| `python -m ruff check --no-cache --select F --output-format json scripts/tl.py` | `failed` trên head và base, tiêu chí delta đạt | Rc 1 cả hai, cùng 12 F821 và 0 F401. Hai JSON trùng sau bỏ đường dẫn tuyệt đối, SHA-256 `21c815da4003322df846c056fcf86db63f24ca02900da7142a6e1a2cc992dd7e`. `head-ruff-tl.log`, `base-ruff-tl.log`. |
| `python -m ruff check --no-cache --select F --output-format json scripts/tl_core/llm_route.py scripts/tl_core/llm_route_test.py` | `passed` | Rc 0, 0 chẩn đoán. `head-ruff-modules.log`. |
| `git diff --check 60b5c32 HEAD`, `git diff --check fcb12b3 HEAD` | `passed` | Rc 0 cả hai. Phép bổ sung `git diff --check 64b7f2c HEAD` rc 2 do ba dấu xuống dòng cứng Markdown bằng khoảng trắng ở hồ sơ #1514 lượt 8, nằm trước packet này. |

Tập 16 ca selftest đỏ gồm 8 ca `r973_bootstrap_*`, 5 ca `wp433_*` và `wp727_tl_gws_refresh` khi `/tmp/.git` rỗng hiện diện. Hai ca còn lại là `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` và `r268_l2_trichotomy_theo_trang_thai_object`, cùng đỏ ở base. `cmp` tập ca đỏ đã sắp xếp trả rc 0. So tập ca đạt chỉ thêm test DOCX mới trên head. Do đó delta ca đỏ bằng 0. Điều kiện selftest N/N của §5 vẫn thiếu. SHA-256 log head `70a1579ce4855585e83c678377cb6d20b24478e6a1e941d62832aa961576eef0`, log base `7a9e5af22678be34dd71e6800fc68eb95958c53d0b62025206c5ccf8f1754d81`.

Chạy thêm chính suite bằng `python -B -m pdb scripts/tl_core/llm_route_test.py`, đặt điểm dừng ở dòng 1735 khi ca đích bắt `TinHieuChotCa`. Rc trình gỡ lỗi 0 và suite vẫn 59/59, 157/157. SHA-256 `mutations.log` là `ce43c4488dd3031f050162c6f503bf7c43872e3d08774cbe59bde95bd09c2978`. Runner chỉ tính bị giết khi áp đúng một neo, nạp được module tạm và ca đích ném tín hiệu. [Harness](../scripts/tl_core/llm_route_test.py#L1715)

| Đột biến trong suite | Tín hiệu quan sát |
| --- | --- |
| `wp1525_noi_dung_truoc_tieu_de`, `wp1525_nhan_them_tieu_de` | Bắt vì sai số Điều hoặc nhận thêm đoạn tiêu đề Điều có số tự động. |
| `wp1525_gop_doan_khong_so` | Bắt trước ở mẫu đoạn thường giữa hai khoản. Phép đo riêng dấu gạch bên dưới xác định giới hạn này. |
| `wp1525_id_khong_chuan_hoa`, `wp1525_numid_trung` | Bắt vì chặn oan ID khác cách viết hoặc vì nhận hai định nghĩa trùng `numId`. |
| `wp1525_dem_vuot_tran`, `wp1525_ilvl_override_ngoai_mien` | Bắt ở ca tăng vượt 999 và ca override cấp ngoài miền. |
| `wp1525_moc_move_khong_can`, `wp1525_moc_move_la`, `wp1525_mat_ptab` | Bắt vì chấp nhận mốc lẻ hoặc chặn oan mốc nội dòng và tab căn lề. |
| `wp1525_tho_nhan_diem`, `dong_la_trong_nguon_co_so_bi_bo_qua` | Bắt vì nhận điểm ở đường thô hoặc bỏ qua dòng mất số trong nguồn có số. |

Hai phép bổ sung chỉ đổi `llm_route.py` trong clone tạm cùng head, mỗi lần chạy nguyên lệnh `python scripts/tl_core/llm_route_test.py` rồi khôi phục blob gốc. Cả hai đột biến **sống**, 0/2 bị giết. Không có thay đổi ở test có sẵn.

| Đột biến bổ sung | Kết quả |
| --- | --- |
| Cho đúng nhánh điểm tay mở bằng dấu gạch nhập vào khoản đang mở | Rc 0, 59/59 ca, 157/157 đột biến có sẵn. `mutant-dash.log`. SHA-256 của diff `c591bda934bd4e0aef968f1ee3741a3ec823d221e3b9bb0741d80d87705bd52a`. |
| Tắt chuẩn hóa riêng ở định nghĩa và tham chiếu `abstractNumId` | Rc 0, 59/59 ca, 157/157 đột biến có sẵn. `mutant-abstract.log`. SHA-256 của diff `5f4e1a26ce62ec60a2b7df182b19266888d7b4f5454b6ea9068b5076bc7179f8`. |

## Không đo được

- G1–G4 và G6 là đối chiếu mã. Bản Word/Google Docs thật, tần suất các dạng này, nhãn Word ở chuỗi nhảy cấp và hành vi mở target style khác tên chưa được đo. So mốc move hiện chỉ đo mốc cân/lẻ ở mẫu có sẵn. Chưa đo cách Word xử lý thứ tự mốc, ID cùng giá trị với cách viết khác nhau, hoặc mốc bọc qua nhiều cấp/dòng.
- Windows là `required` theo ADR-0060 M3. Diff toàn PR thêm dòng selftest dùng `encoding=`, thuộc dấu hiệu bắt buộc. Phép đo Windows native và CI ở exact head là `not_run`, kết quả `not_measured` trong lượt offline. [ADR-0060 M3](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L43)
- Kiểm GitHub, CI từ xa và model thật là `not_run`. Model và effort phục vụ báo `KHONG_DO_DUOC` từ run đang thực thi. Trạng thái terminal, rc con và hash stdout của chính lượt review cần đọc lại ở run `639f7a64` sau khi launcher kết thúc. Trong sáu lệnh prompt có **0** lệnh `skipped`.
- Test đầu tiên chạy ở checkout được giao đã sinh fixture golden và state tự kiểm trong hai thư mục ignored. Hai thư mục mới đó đã được chuyển vào scratch sau khi test dừng. Các gate cần cây sạch đã được chạy lại trên hai clone. Đầu/cuối checkout review khớp SHA/tree, diff tracked và index rc 0. Trong trạng thái cuối chỉ có verdict mới và thư mục ignored `.codex/` có từ đầu. Hai mốc này xác minh delta quan sát được. Repo nguồn của Executor nằm ngoài phạm vi quan sát.

## Kết luận

**0 P0, 2 P1, 4 P2, 0 P3** mở. Hai P1 liên quan nhãn số và chữ gạch bỏ có thể đi vào dữ liệu đối chiếu nguyên văn. **PR #1517 chưa đủ điều kiện merge** theo ADR-0060 M1. Lượt này đã dùng 7/7 lời gọi #1525 và chạm Review Rescue Checkpoint, cần giữ nguyên finding cùng exact SHA trong handoff. [ADR-0060 M1](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32) · [Protocol §12](../docs/PROTOCOL_DA_PHIEN.md#L1097)

P2_mo: 4

VERDICT: REQUEST_CHANGES
