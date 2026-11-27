# Verdict packet #1525 r27 lượt 27 — Codex
reviewed_sha: 9972282f3adf0b1f6b8827178130482248df0cb3
tree: 555615a2ad3bb7ebec811cc8b0388b1c8a828e7b
base_sha: 64b7f2c14776d5d0e1d34a6be4725490956f5bec
VERDICT: APPROVE
> Kết luận nội dung. Còn một P2 chặn merge theo ADR-0060 M1.

## Phạm vi và preflight

- Reviewer `openai_codex / codex_cli / machine`, run `9dc5a1fe1a39497a942fa32266f08cfe` do launcher ghi. Executor theo lease `claude / claude_code / machine/local`. Review class khai báo và hiệu lực đều là `sensitive`. Sandbox quan sát là `workspace-write`, quyền ghi ngoài checkout giới hạn ở thư mục tạm được cấp. Model và effort phục vụ của reviewer `KHONG_DO_DUOC` từ metadata hiện có.
- Checkout giao để review ở trạng thái detached, sạch phần tracked, có sẵn thư mục ignored `.codex/`. Ba mốc base, điểm tách #1514 `fcb12b3873c3bec2c339029136243ed2c804ce05` và cha bản vá `8a69d6a7fd7283847eea6feca1e88455e1dc64e0` đều là tổ tiên của head. Đã đọc diff bản vá, đối chiếu phạm vi diff packet và PR từ ba mốc này.
- Lease r27 g1, giới hạn 27, đã dùng 26 trước lượt này. SHA-256 spec `5a1afe0e66485decc37b15e6b328d3d9bcb79cc5e9545ffa3d99c9f5f70bd13d`. Băm lại 146 đường dẫn write set có thứ tự cho `13536abd2be315a0ddeecb2b4cdef6d3deddca4a4868443be68536b68760c51b`. Cả 8 đường dẫn của diff r27 và cả 142 đường dẫn của diff packet sau khi loại hồ sơ #1514 đều thuộc write set. Đã so hai trường `da_bi_thay_the` và `thay_the_cho` trên đủ 27 cặp từ #1514 r9 đến #1525 r27. Lease r27 chưa có mốc bị thay thế trong checkout. [Đặc tả](../ops/specs/llm-khoan-docx-r27.md) · [Lease](../ops/leases/llm-khoan-docx-r27-g1-claude.yaml)

## Đối chiếu lượt 26 và đặc tả r27

| Mục | Trạng thái | Bằng chứng |
| --- | --- | --- |
| C1 lượt 26 · §2.29 | **ĐÃ VÁ THẬT** hai hình dạng C1 đã báo. **VÁ MỘT PHẦN** lớp nhãn điểm | Chốt mới chạy trước `co_so`, từ chối cặp số–số có một dấu nối thuộc tập cho phép. Ca có đệm, ngoặc và nguồn có số đều qua bộ ca. Mutant `wp1525_bo_chan_nhieu_cap` và mutant thu hẹp dấu nối đều chết đúng ca. D1 ghi phần miền nhãn còn có thể đi vào nhánh nhận khoản. [Nhận nhãn](../scripts/tl_core/llm_route.py#L490) · [Ca](../scripts/tl_core/llm_route_test.py#L686) |
| C2 lượt 26 · §2.29 | **ĐÃ VÁ THẬT** | `la_run` không truyền lên đoạn nếu run đã gạch và bị bỏ. Ruột ký hiệu vẫn được tính là nội dung khi quyết định giữ khoảng trắng. Ba đối chứng sẵn có bao phủ ký hiệu trong run gạch, trong `w:del` và trong run còn hiệu lực. Hai mutant ghi cờ quá sớm và bỏ cờ của run sống đều chết đúng ca. Chốt tương thích, trường đơn trị và sửa dấu đoạn vẫn được áp ở cấp tài liệu theo đặc tả. [Cờ của run](../scripts/tl_core/llm_route.py#L1098) · [Ca dương](../scripts/tl_core/llm_route_test.py#L1475) · [Ca âm](../scripts/tl_core/llm_route_test.py#L1778) |
| §1, §2.2–§2.3 · K1 #1514 | **ĐÃ VÁ THẬT** cho hai biểu hiện K1 được báo | Dòng điểm của K1 bị từ chối trên cả nguồn có số và mất số. Tiếp dòng “là” ở nguồn có số rơi vào nhánh từ chối dòng không số. Ca Điều 3 và ba đầu ra đã lưu vẫn đạt 8/8. Giữ CLI, định tuyến model, `can_nguoi_duyet: true` và chỉ báo nguồn ranh giới. D1 là biểu hiện khác của cùng lớp. [Ca K1](../scripts/tl_core/llm_route_test.py#L1236) · [Đường CLI](../scripts/tl_core/ops_misc.py#L3017) · [Đầu ra](../scripts/tl_core/ops_misc.py#L3130) |
| §2.1, §2.4–§2.13 · phạm vi Điều, đánh số, câu dẫn | **ĐÃ VÁ THẬT** trong miền đã khai. **HẾT ĐỐI TƯỢNG** với dò điểm kết thúc, đếm ô bảng và nhận điểm gõ tay đứng riêng | Vùng từ tiêu đề đích nguyên đoạn tới hết body. Bảng, khối lạ, tiền tố Điều khác, tiêu đề nhầm, đoạn số rỗng và dòng không số sau khoản đầu đều chặn. Trước khoản đầu chỉ cho đúng một câu dẫn chuẩn nguyên đoạn hoặc vắng. Thiếu đánh số tự động ném lỗi và CLI trả 2, bỏ `KhongCauTruc`. Đếm theo `numId`, dùng `start` mặc định 0 hoặc `startOverride`, xóa đếm cấp con khi cấp cha tiến, và từ chối nhảy cấp. Bộ đọc cuối buộc một danh sách trong vùng và số khoản 1…N, đồng thời chặn cấp/ID không xác định, định dạng ngoài phạm vi và đánh số kế thừa qua style trong Điều. [Định nghĩa danh sách](../scripts/tl_core/llm_route.py#L758) · [Vùng và bộ đếm](../scripts/tl_core/llm_route.py#L1240) · [Câu dẫn](../scripts/tl_core/llm_route.py#L1361) |
| §2.5–§2.13, §2.23–§2.29 · chữ còn hiệu lực, dấu phân cách | **ĐÃ VÁ THẬT** cho các biểu hiện đã kiểm | Đọc XML gốc, tách gạch đơn/kép, lọc mẩu sửa đổi, kiểm dấu đoạn và cặp mốc move. Không giữ phân cách nằm trong mẩu đã bỏ có nội dung. `xml:space` hiệu lực được kiểm ở đường chữ giữ, `delText` lạc và ruột bị bỏ. Cờ ngắt và cờ phần tử lạ trong run gạch chỉ tác động khi run còn hiệu lực. Từ nối của khoản cấu trúc chỉ dò trong đoạn mở khoản. [Đọc đoạn](../scripts/tl_core/llm_route.py#L1003) · [So nguyên văn](../scripts/tl_core/llm_route.py#L1544) |
| §2.14–§2.21 · part, tiền tố cấu trúc, biên Unicode | **ĐÃ VÁ THẬT** trong miền đã khai | URI và QName đầy đủ, part chính đọc byte và quan hệ theo part thật. Tiền tố được dò từ chữ còn sau lọc, trên bản chiếu dấu câu. Chốt ký tự chạy trước tách dòng/gộp khoảng trắng, đường thô bỏ một BOM, hai đường đều chặn chữ số ngoài ASCII. Hướng dẫn dẫn chiếu đầu đoạn yêu cầu làm thủ công. [Part](../scripts/tl_core/llm_route.py#L716) · [Miền ký tự](../scripts/tl_core/llm_route.py#L569) · [Hướng dẫn](../docs/GOI_AGENT_DA_NEN.md#L390) |
| §2.22–§2.26 · `--markup-strict`, đơn trị và ZIP | **ĐÃ VÁ THẬT** cho chốt CLI và các khai báo mâu thuẫn đã báo. U2/V3/W1/W3 và phần số hiệu của W2 là giới hạn đã duyệt | `lay_dieu_qua_extract` truyền cờ strict, lỗi extract làm dừng trước model. Trùng part ZIP, trường đơn trị, khóa style và cấp danh sách đều bị chặn; định nghĩa danh sách lỗi không dùng vẫn có đối chứng qua. [Extract](../scripts/tl_core/llm_route.py#L1649) · [Đơn trị](../scripts/tl_core/llm_route.py#L638) · [Giới hạn số hiệu](../ops/specs/llm-khoan-docx-r27.md#L264) |
| §3 · ca, đột biến và CLI | **ĐÃ VÁ THẬT** cho các khoảng trống test đã báo. Miền nhãn còn thiếu ca cho D1 | Harness chỉ tính kill khi đúng ca đích phát `TinHieuChotCa`; neo không duy nhất, lỗi nạp và lỗi vô can làm suite đỏ. Ca CLI có sẵn dùng model giả và kiểm rc 0/5/2. [Harness](../scripts/tl_core/llm_route_test.py#L2218) · [Ca CLI](../scripts/tl_selftest.py#L32285) |

### Đối chiếu từng lượt trước

ID trong bảng gắn với lượt ở cột đầu. Bằng chứng lấy từ mã head và các ca/đột biến có sẵn, đối chiếu mô tả gốc trong thư mục review.

| Lượt | Findings và trạng thái | Bằng chứng trên head |
| --- | --- | --- |
| 1 | A1 phần cắt và A6 **HẾT ĐỐI TƯỢNG** theo r7. A2–A5, A7–A8 và phần bảo vệ vùng của A1 **ĐÃ VÁ THẬT** | Vùng tới hết body; bộ đếm/sổ lỗi theo danh sách; từ nối chỉ trong đoạn mở; lọc XML gốc; hướng dẫn một dòng và ca đích hiện có. [Lượt 1](../ops/acceptance/llm-khoan-docx/r1/review-1-codex/VERDICT.md) |
| 2 | B1/B2 phần điểm cắt và duyệt bảng **HẾT ĐỐI TƯỢNG**. Các biểu hiện còn lại của B1–B8 **ĐÃ VÁ THẬT** | Tiêu đề nguyên đoạn, chặn số qua style, hai cờ gạch riêng, no-break hyphen, số thập phân, metadata wrapper và ca đích. [Lượt 2](../ops/acceptance/llm-khoan-docx/r1/review-2-codex/VERDICT.md) |
| 3 | C1 phần điểm cắt và C2 phần đếm bảng **HẾT ĐỐI TƯỢNG**. C2 phần nhãn chữ, C3–C7 và chốt ngắt tiêu đề C1 **ĐÃ VÁ THẬT** | Nhãn chữ lặp, kiểm dấu phân cách, xử lý toggle, SDT nội dòng, mutant phần tử lạ và tài liệu nhãn khoản. [Lượt 3](../ops/acceptance/llm-khoan-docx/r1/review-3-codex/VERDICT.md) |
| 4 | D1 phần điểm cắt **HẾT ĐỐI TƯỢNG**, fallback **ĐÃ VÁ THẬT**. D2–D4 và D6 **ĐÃ VÁ THẬT**, D5 là giới hạn đã khai | Chặn reset section, đọc trực tiếp XML, chặn phần tử lạ và kiểm nguyên chữ đoạn. Chẩn đoán namespace Strict riêng. [Lượt 4](../ops/acceptance/llm-khoan-docx/r1/review-4-codex/VERDICT.md) |
| 5 | E1, E3, E4 **HẾT ĐỐI TƯỢNG**. E2, E5, E6 **ĐÃ VÁ THẬT** | Chặn toàn bộ bảng; nhiều tầng toggle bị từ chối; ca lọc regex và `moveFrom`; trần cấp 0–8. [Lượt 5](../ops/acceptance/llm-khoan-docx/r1/review-5-codex/VERDICT.md) |
| 6 | F1 phần cắt và F2 phần nhận điểm tay **HẾT ĐỐI TƯỢNG**. F3–F6 **ĐÃ VÁ THẬT** | Chuẩn hóa ID, trần số, ca cấp ngoài miền, `ptab`, mốc move đủ cặp. [Lượt 6](../ops/acceptance/llm-khoan-docx/r1/review-6-codex/VERDICT.md) |
| 7 | G1–G6 **ĐÃ VÁ THẬT** | ID ASCII, từ chối nhảy cấp, quan hệ styles, trần đếm, ngắt cuối đoạn, ca điểm tay/abstract ID và tiêu đề không phân biệt hoa thường. [Lượt 7](../ops/acceptance/llm-khoan-docx/r1/review-7-codex/VERDICT.md) |
| 8 | H1–H5 **ĐÃ VÁ THẬT** | Tiền tố Điều, quan hệ gốc, mutant part đổi tên, dấu riêng ID style lỗi, chỉ cho ngắt trang/cột đứng cuối chữ hiệu lực. [Lượt 8](../ops/acceptance/llm-khoan-docx/r1/review-8-codex/VERDICT.md) |
| 9 | J1–J5 **ĐÃ VÁ THẬT** | Style có thuộc tính đánh số cũng bị chặn; `mc:` bị chặn ở cấp part; danh sách cho phép `lvlText`; quan hệ theo part chính; chữ gạch sau ngắt không tính. [Lượt 9](../ops/acceptance/llm-khoan-docx/r1/review-9-codex/VERDICT.md) |
| 10 | K1–K4 **ĐÃ VÁ THẬT** | Chốt `mc:` ở ba part, tiền tố cấu trúc viết số bằng chữ, khớp trọn `lvlText`, §3 ghi đúng đọc hết tệp. [Lượt 10](../ops/acceptance/llm-khoan-docx/r1/review-10-codex/VERDICT.md) |
| 11 | L1–L6 **ĐÃ VÁ THẬT** cho các biểu hiện đã báo | URI đầy đủ, tiền tố Điều thay điều kiện cuối câu, phân biệt mẫu số thứ tự cấp lớn, lỗi `lvlText` có kiểm soát, parser nhận bytes, hướng dẫn dấu và bullet. [Lượt 11](../ops/acceptance/llm-khoan-docx/r1/review-11-codex/VERDICT.md) |
| 12 | M1–M2 **ĐÃ VÁ THẬT** | Chốt tiền tố trên bản chiếu thay hình dạng tên Điều, giá trị số hỏng và mốc move thiếu ID được chặn. [Lượt 12](../ops/acceptance/llm-khoan-docx/r1/review-12-codex/VERDICT.md) |
| 13 | N1–N3 **ĐÃ VÁ THẬT** | Dò tiền tố sau chiếu dấu câu, chuẩn hóa ID bằng chuỗi, khối so QName đầy đủ. [Lượt 13](../ops/acceptance/llm-khoan-docx/r1/review-13-codex/VERDICT.md) |
| 14 | Q1–Q2 **ĐÃ VÁ THẬT** | Dò đầu đoạn bằng bản chiếu sau kiểm ký tự; hướng dẫn giữ nguyên nguồn và làm thủ công khi gặp dẫn chiếu đầu đoạn. [Lượt 14](../ops/acceptance/llm-khoan-docx/r1/review-14-codex/VERDICT.md) |
| 15 | R1–R3 **ĐÃ VÁ THẬT** | Ký tự kiểm trước chuẩn hóa khoảng trắng; mẫu số gõ tay ngoặc kín; nguồn thô có ký tự định dạng bị từ chối. [Lượt 15](../ops/acceptance/llm-khoan-docx/r1/review-15-codex/VERDICT.md) |
| 16 | S1–S3 **ĐÃ VÁ THẬT** | Tập ký tự cho phép, chốt trước tách dòng, `permStart`/`permEnd` có đối chứng. [Lượt 16](../ops/acceptance/llm-khoan-docx/r1/review-16-codex/VERDICT.md) |
| 17 | T1–T2 **ĐÃ VÁ THẬT** ở hai đường kiểm; phần theo producer thuộc ngoại lệ U2 | Chặn số mũ, UTF-8 thường và một tầng bỏ BOM. [Lượt 17](../ops/acceptance/llm-khoan-docx/r1/review-17-codex/VERDICT.md) |
| 18 | U1 **ĐÃ VÁ THẬT**. U2 là giới hạn đã duyệt | Miền chữ số ASCII, ca số mũ đầu và trong dòng. Làm sạch đầu vào theo số hiệu được khai ở §2.21. [Lượt 18](../ops/acceptance/llm-khoan-docx/r1/review-18-codex/VERDICT.md) |
| 19 | V1/V2/V4 **ĐÃ VÁ THẬT** cho các biểu hiện gốc. V3 là giới hạn đã duyệt | Cờ strict và lỗi trước model, chặn số từ mặc định đoạn, nhãn chữ kết chấm bị từ chối. [Lượt 19](../ops/acceptance/llm-khoan-docx/r1/review-19-codex/VERDICT.md) |
| 20 | W1/W3 và phần số hiệu của W2 là giới hạn đã duyệt. W2 đường DOCX, W4/W5 **ĐÃ VÁ THẬT** cho các biểu hiện gốc | Giữ phân cách thuần, nhãn chữ hoa/lặp, từ chối cấp và override trùng. [Lượt 20](../ops/acceptance/llm-khoan-docx/r1/review-20-codex/VERDICT.md) |
| 21 | X1–X3 **ĐÃ VÁ THẬT** cho các biểu hiện gốc | Tab/ngắt trong mẩu bị bỏ, trường đơn trị, nhãn chữ nối gạch và đối chứng từ ghép. [Lượt 21](../ops/acceptance/llm-khoan-docx/r1/review-21-codex/VERDICT.md) |
| 22 | Y1–Y3 **ĐÃ VÁ THẬT** cho các biểu hiện gốc | Chung phép đọc ruột, chọn vùng và style đơn trị, ca khoảng đệm và dấu nhãn. [Lượt 22](../ops/acceptance/llm-khoan-docx/r1/review-22-codex/VERDICT.md) |
| 23 | Z1–Z4 **ĐÃ VÁ THẬT** cho các biểu hiện gốc | Ruột có ký hiệu tính là nội dung, ZIP trùng bị chặn, các nhãn số–số đã báo bị chặn, ca metadata tách riêng. [Lượt 23](../ops/acceptance/llm-khoan-docx/r1/review-23-codex/VERDICT.md) |
| 24 | A1/A2 **ĐÃ VÁ THẬT** cho các biểu hiện gốc | `xml:space` theo cây, hai mẫu số–số kết bằng gạch vẫn bị chặn. [Lượt 24](../ops/acceptance/llm-khoan-docx/r1/review-24-codex/VERDICT.md) |
| 25 | B1 **VÁ MỘT PHẦN**. B2/B3 **ĐÃ VÁ THẬT** | Chốt số–số được mở rộng, còn D1 ngoài chốt. Các mutant đặt lại `xml:space`, mẩu đã bỏ, `delText` lạc và hai cờ ngắt đều chết đúng ca. [Lượt 25](../ops/acceptance/llm-khoan-docx/r1/review-25-codex/VERDICT.md) |
| 26 | C1 **VÁ MỘT PHẦN**, C2 **ĐÃ VÁ THẬT** | Đối chiếu riêng ở đầu mục. [Lượt 26](../ops/acceptance/llm-khoan-docx/r1/review-26-codex/VERDICT.md) |

Với #1514, các biểu hiện A1/A2/D3/E2/F2 về bỏ nhầm câu dẫn hoặc chia khoản, C1 về tiêu đề dính thân, A3/C2/D1/E1/F1 về dấu kết và số nội dòng, A4 về fixture, và G1/H1/J1/K1 về ghép dòng điểm đều được kiểm bằng ca lịch sử còn chạy. Hai hình dạng tiêu đề của D2 và việc chặn dòng điểm của C2 thuộc giới hạn đường thô đã khai. Đối chứng của C2 cho số dẫn chiếu đứng cuối khoản một dòng vẫn đạt. [Ca lịch sử #1514](../scripts/tl_core/llm_route_test.py#L1065) · [Giới hạn tiêu đề](../docs/GOI_AGENT_DA_NEN.md#L373)

## Findings

### D1 [P2] Nhãn điểm nhiều thành phần vẫn có thể bị nhận làm khoản — `scripts/tl_core/llm_route.py:1409`

**Kịch bản.** Một danh sách Word có cấp cha định dạng số và cấp con định dạng chữ. Nhãn điểm in số cha, dấu chấm, chữ cấp con rồi dấu chấm. Khi nguồn thô mất quan hệ cấp, dòng điểm có thể là dòng duy nhất mang số, hoặc đứng cùng các dòng có phần số đầu tạo thành dãy liên tục. Nếu thân từng dòng đủ hai vế định nghĩa và dấu kết, bộ tách có thể nhận phần số đầu là số khoản và để phần nhãn chữ vào thuật ngữ. Một biến thể cùng lớp dùng hai cấp số nhưng có hơn một dấu nối liền giữa hai cấp, chẳng hạn ngoặc đóng ngay sau số cha rồi dấu chấm trước số con. Bộ dựng `_nhan` nhận dãy dấu này và cả họ số–chữ. [Bộ dựng Word](../scripts/tl_core/llm_route.py#L938) · [Miền r27](../ops/specs/llm-khoan-docx-r27.md#L345)

**Căn cứ.** `_RE_NHIEU_CAP` đòi chữ số sau đúng một dấu nối có đệm. Mẫu số–chữ không khớp chốt đó, dù dạng kết bằng chấm khớp `_RE_DIEM`. Cả khi kiểm dấu phân cách lẫn khi phân vai dòng, mã ưu tiên `_RE_SO_KHOAN`, nên nhánh điểm không được xét. Ở dạng nhiều dấu nối số–số nói trên, phần số con có thể đứng ngay sau một dấu chấm còn lại, nơi `_RE_SO_NOI_DONG` loại vị trí do ký tự đứng trước. Cùng độ lệch miền xuất hiện khi hai placeholder số và chữ liền nhau, nhãn kết bằng chấm. `_nhan` dựng được nhãn này, còn cả ba matcher đầu dòng đều bỏ qua. Nếu không có số khoản nào khác, cả dòng có thể vào nhánh khoản mất số. Với dấu câu cân và hai vế khớp cách phân đoạn này, `lech_nguyen_van` có thể trả rỗng và CLI có thể ghi `--out`. Lỗi nằm ở bộ tách thô sau khi nhận chữ và áp cả với `--tep`. Các ngoại lệ producer đường số hiệu không bao phủ lỗi này. [Các matcher](../scripts/tl_core/llm_route.py#L490) · [Thứ tự phân vai](../scripts/tl_core/llm_route.py#L1400) · [So và ghi](../scripts/tl_core/ops_misc.py#L3120)

**Hạng và đề xuất.** P2 theo tiền lệ C1 và K1. Cần bố cục thô cụ thể và kết quả khớp phân đoạn nhận nhầm, trong khi đầu ra vẫn yêu cầu duyệt ranh giới. Dùng chung ngữ pháp nhãn nhiều thành phần cho bước kiểm dấu phân cách và bước phân vai. Kiểm nhãn nhiều thành phần trước khi chấp nhận nhãn số đơn, bao phủ các kiểu placeholder và các dãy dấu thuộc miền đã khai. Khóa riêng ba biểu hiện ở trên và giữ ca dương cho khoản một dòng, kể cả nhãn số dính thân. [Protocol §8](../docs/PROTOCOL_DA_PHIEN.md#L646) · [ADR-0060 M1–M2](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32)

| Lớp | Lịch sử và kết quả | Phép kiểm đóng lớp |
| --- | --- | --- |
| `ranh-gioi-khoan` | K1 #1514 → V4/W4/X3/Y3/Z3/A2 lượt 24/B1/C1 → D1. Hai biểu hiện K1 gốc đã đóng. Còn **một lớp, một finding P2** ở bước phân vai nhãn thô. | Bao phủ nhãn nhiều cấp trong miền `_nhan` đã công bố, trước mọi cửa nhận số đơn. Đo đường có số, mất số và đối chứng một khoản một dòng. |
| `docx-khoang-trang-sau-loc` | W2/X1/Y1/Z1/A1 lượt 24/B3/C2. Đóng các biểu hiện đã báo trong miền đo. | Đối chứng giữ phân cách thuần, bỏ trọn phần có nội dung, phân biệt phần tử còn hiệu lực với phần tử nằm trong run bị loại. |
| `docx-so-hien-thi` | A2/B2/G1/J1/V2/W5/X2/Y2/Z2. Đóng các biểu hiện đã báo trong miền đo. | Kiểm số hiển thị, reset, khai báo mâu thuẫn khi dùng và đối chứng định nghĩa không dùng. |
| `docx-test-doc-lap` | A7/B7/C6/D4/E5/F5/G5/H3/J4/Z4/B2. Đóng các khoảng trống đã báo. Thiếu ca cho biểu hiện D1 nằm trong phép đóng `ranh-gioi-khoan`. | Mutant đúng neo, đúng ca và đúng tín hiệu từ chối. |

Đóng 1/2 lớp còn mở từ lượt 26. Từ hai finding ở lượt trước còn một finding P2, với ba biểu hiện cùng cơ chế trong D1.

Phép so vẫn buộc đủ mục, đúng vị trí, đúng hai vế và giữ xuống dòng của các điểm. Đọc mã bộ đếm, định vị, chốt điểm gõ tay, câu dẫn và lọc markup không cho thấy thêm đường sai nguyên văn có căn cứ trong miền DOCX đã khai. Đường thô vẫn có các bố cục đồng hình do mất cấu trúc nguồn như mô tả ở K1, ví dụ hai dòng có đủ hình dạng định nghĩa mà vai trò thật chỉ xác định được bằng định dạng tài liệu. D1 hẹp hơn vì nhãn còn dấu hiệu phân cấp thuộc miền được đặc tả.

Đã rà các phần tử bỏ qua/đi vào/chặn của §2.5 cùng các bổ sung và fixture hiện có. Chưa xác lập một dạng export Word/Google Docs thường gặp bị chặn oan ngoài giới hạn đã khai. Các chốt có thể gây từ chối như phần tử `mc:`, trường, chú thích, bảng, danh sách theo style và định dạng số chưa hỗ trợ đều được công bố. Việc một phần tử còn lại có phổ biến trong export thực tế chưa đo được ở lượt offline này.

## Kết quả test và đột biến

Linux x86_64, Python 3.13.18, Git 2.43.0, `core.abbrev=7`. Hai checkout shallow, detached, dựng từ object local dưới `/tmp/wp1525-r27-review.RjDhBXes/`. Head và tree như đầu báo cáo, tree của base là `0cc14e79cecd2ce44bc4dc6cff92cadb31fd7ee4`. Test dùng `PYTHONDONTWRITEBYTECODE=1`. Log, fixture và state sinh trong lúc chạy nằm trong các bản sao hoặc thư mục tạm ngoài checkout được giao.

| Lệnh | Trạng thái | Mã thoát và bằng chứng |
| --- | --- | --- |
| `python scripts/tl_core/llm_route_test.py` | `passed` | rc 0, **63/63** ca, **244/244** mutant bị giết. `route.log`. |
| `python scripts/tl.py --deterministic workflow-audit --strict --json` | `passed` | rc 0, `ok=true`, 194 lệnh, 26 card, 11 nhóm, 60 task, 0 lỗi, 0 cảnh báo. `workflow.log`. |
| `python scripts/tl.py --deterministic golden-test --json` | `passed` | rc 0, `ok=true`, **20/20** khớp fixture, **20/20** bản chiếu và **20/20** byte thô ổn định. `golden.log`. |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | `passed` | rc 0, `ok=true`, **187/187** tệp, sai/thiếu/thừa đều 0, hash gói `8c16d6ebb7dc3ac84512ca377d215bc418bf62adafc2d9e7435efda357deb7aa` khớp. `release.log`. |
| `python ops/lease_publish.py check --root . ops/leases/llm-khoan-docx-r27-g1-claude.yaml` | `passed` cục bộ | rc 0, “ĐĂNG ĐƯỢC”, issue #1525, neo `64b7f2c14776`, hết hạn 20:15 UTC. Hai kiểm GitHub nằm ngoài lệnh này. `lease.log`. |
| `python scripts/tl.py --selftest` · head | `failed` | rc 1, **1774/1790** tổng, transport **12/12**. Ca `r1525_llm_khai_niem_tep_docx_cau_truc` đạt. `selftest.log`. |
| Cùng lệnh selftest · base | `failed` | rc 1, **1773/1789** tổng, transport **12/12**. Trùng đủ 16 ID đỏ của head, `cmp` rc 0. `base-selftest.log`. |
| `python scripts/tl.py --deterministic determinism-audit --strict --json` | `passed` | rc 0, `ok=true`, **15/15** kiểm tra. `determinism.log`. |
| `python scripts/tl.py --deterministic doc-claims-check --strict --json` · head và base | `failed` | Cả hai rc 2. Cùng 410 advisory và một cờ cứng `SHA_NOT_A_COMMIT` cho `9941d8af52aeede1c78ea4e232fbe9a8d5272033` ở protocol dòng 1680. `doc-claims.log`, `base-doc-claims.log`. |
| Ruff 0.15.15 · `python -m ruff check --no-cache --select F --output-format json scripts/tl.py` · head và base | `failed` cho lint, delta 0 | Cả hai rc 1, cùng 12 F821, khớp vị trí và nội dung sau khi bỏ tiền tố checkout. `ruff-head.log`, `ruff-base.log`. |
| Hợp đồng Ruff của CI · `loi_ruff_ci()` qua `runpy.run_path(".claude/dev/ci_dang_ky_test.py")` | `passed` | rc 0, `RUFF_CONTRACT 3 []`. `ruff-contract.log`. |
| `git diff --check 8a69d6a HEAD` và `git diff --check fcb12b3 HEAD` | `passed` | Cả hai rc 0. Với toàn PR từ base, cùng lệnh rc 2 ở ba dòng Markdown có khoảng trắng cuối trong verdict lượt 8 #1514, phần kế thừa. |

Trong 16 ca đỏ selftest trên mỗi cây, 14 ca khớp nhóm lỗi môi trường `/tmp/.git` rỗng được prompt nêu (8 `r973_bootstrap_*`, 5 `wp433_*`, 1 `wp727_tl_gws_refresh`). Hai ca còn lại cùng tên trên hai cây, `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` và `r268_l2_trichotomy_theo_trang_thai_object`. Danh sách ID nằm trong `selftest.fail-ids` và `base-selftest.fail-ids`. SHA-256 log head `594a04671b4dd340154ec45c5457e742493fec30ecb6673323b7260b4a97a1dc`, base `7799579ab58abb816c1211cbbba9fdfd3814932ef779d72dc6027263ca317ba0`. Delta ID đỏ bằng 0. Điều kiện selftest N/N và doc-claims rc 0 của §5 vẫn thiếu.

Bảng `DOT_BIEN` sẵn có tự dựng từng bản đột biến trong thư mục tạm. Lượt chạy lại trên bản sao head bằng `python -B -m pdb scripts/tl_core/llm_route_test.py` dừng ở nhánh `TinHieuChotCa` dòng 2238 để ghi tên mutant và ca đích. Cả hai lượt pdb và suite đều rc 0. Log `target-mutants.log` ghi **147/147** mutant `wp1525_*` vào nhánh đúng tín hiệu. Log `target-reasons.log` ghi lý do của các đột biến dưới đây.

| Mutant | Tín hiệu của ca đích |
| --- | --- |
| `wp1525_bo_chan_nhieu_cap` | `ca_khoan_mat_so_co_diem_dat` bắt dòng mang nhãn số nối gạch lọt ở nguồn mất số. |
| `wp1525_diem_noi_chi_cham` | Cùng ca bắt dòng mang nhãn chữ nối gạch lọt. |
| `wp1525_la_ghi_truoc_gach` | `ca_cau_truc_docx_dat` bắt DOCX hợp lệ bị từ chối vì cờ phần tử lạ đi ra từ run gạch. |
| `wp1525_nhan_phan_tu_la` | `ca_cau_truc_docx_chan` bắt phần tử lạ còn hiệu lực thoát chốt tiêu đề. |
| `wp1525_tho_nhan_diem` | `ca_wp1514_luot9` bắt các dòng điểm bị nhận thành khoản riêng ở nguồn mất số. |
| `wp1525_khong_dat_lai_cap_con`, `wp1525_bo_qua_start_override` | `ca_cau_truc_docx_dat` bắt nhãn chữ không đặt lại ở khoản sau và số khoản bắt đầu sai do mất override. |

## Không đo được

- D1 được xác định bằng đọc mã. Chưa đo ca đầu-cuối cho các biến thể D1, hành vi lưu/hiển thị theo phiên bản Word hoặc tần suất gặp trong nguồn thật. Kho hiện có 0 tệp `.docx` được theo dõi để đối chứng độ phổ biến của phần tử export. Hiệu lực `xml:space` đã đo với CLI tuần tự, còn gọi bộ đọc đồng thời trong cùng tiến trình chưa đo.
- `skipped` ở cấp sáu lệnh prompt là 0. `not_run` gồm Windows native/CI và hai kiểm từ xa về Issue/PR và comment, CI/receipt từ xa, model thật và LIVE. ADR-0060 M3 yêu cầu Windows cho diff toàn PR vì có đổi dòng `encoding=` trong mã Python. Kết quả Linux không đáp ứng phần nghiệm thu Windows. Trạng thái kết thúc của launcher, mã thoát con và hash stdout thuộc biên nhận sau khi phiên review đóng.
- HEAD/tree đầu và cuối khớp. Checkout giao để review chỉ có thay đổi quan sát được là `.review/VERDICT.md`; `.codex/` đã hiện diện trước lượt. `git diff --exit-code` và `git diff --cached --exit-code` rc 0. Các tiến trình tạo fixture và state chạy ở bản sao tạm. Snapshot ghi delta quan sát được giữa hai mốc.

Theo quy tắc verdict nội dung của prompt, **0 P0, 0 P1, 1 P2 và 0 P3** cho kết luận APPROVE. D1 chặn merge theo ADR-0060 M1. Điều kiện gate và Windows còn thiếu như ghi trên. [ADR-0060](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32) · [ADR-0062](../docs/adr/0062-adr-0060-mac-dinh-va-dong-bang-adr-0054.md#L13)

P2_mo: 1
VERDICT: APPROVE
