# Verdict packet #1525 r28 lượt 28 — Codex

reviewed_sha: 0e1c1122bee44aef58347f585bdcb09ed48af7c6
reviewed_tree: de631b29c530f168408eea2b704d5b1a66c64d5f
base_sha: 64b7f2c14776d5d0e1d34a6be4725490956f5bec

**APPROVE** theo ngưỡng nội dung của prompt. Còn E1 [P2] chặn merge theo ADR-0060 M1. Selftest và doc-claims strict cùng đỏ ở head và base.

## Phạm vi và preflight

- Reviewer độc lập `openai_codex / codex_cli / machine`, run launcher `9e6557ba13ac4d4db938e303379b3467`. Executor khai trong lease `claude / claude_code / machine/local`. Review class khai báo và hiệu lực đều là `sensitive`. Sandbox quan sát `workspace-write`, áp chế độ read-only với cây giao review. Model và effort phục vụ `KHONG_DO_DUOC` từ metadata tại thời điểm đọc. SHA-256 của prompt khớp trường `prompt_sha256` trong `run.json`. [Run](../../run/9e6557ba/run.json)
- Checkout rời, detached. Origin khai `ducthangho/tra-luat`. Ref local của nhánh giao `ccr-89c0d2e2-inanqb` trỏ đúng head. Base chính xác, merge-base bằng base. Các mốc `fcb12b3873c3bec2c339029136243ed2c804ce05` và `cda9439b2ffdf93fe5c46b09e118267edfdcc971` là tổ tiên của head. Đã đối chiếu diff bản vá, diff packet và phạm vi toàn PR.
- Lease r28/g1 còn hiệu lực theo thời gian UTC của môi trường, lượt 28/28. SHA-256 của spec `fa7e44f7d58daabbee8ffaaa525cef295f7510dd8921bbc1f114e79a2f55ffde`. Hash 151 đường dẫn lease `e979ff06452fe7a3a685e228b1140aece24c86c36f2d9a69901cdcdb3901e0ed`. Tất cả 8 đường dẫn bản vá và 147 đường dẫn của packet (151 trừ 4 mục hồ sơ #1514 theo prompt) nằm trong write set. Đủ 28/28 cặp `da_bi_thay_the` và `thay_the_cho` từ #1514 r9 qua #1525 r1…r28. R28 chưa có mốc thay thế trong checkout. [Lease](../ops/leases/llm-khoan-docx-r28-g1-claude.yaml) · [Spec](../ops/specs/llm-khoan-docx-r28.md)

## Đối chiếu lượt 27 và đặc tả r28

| Mục | Trạng thái | Bằng chứng |
| --- | --- | --- |
| D1 lượt 27 · §2.28–§2.30 | **ĐÃ VÁ THẬT** ba hình dạng đã báo. **VÁ MỘT PHẦN** lớp `ranh-gioi-khoan` | Chốt đầu dòng chạy trước nhận số đơn. Các ca số–chữ có dấu, số–số có nhiều dấu nối, số và chữ dính nhau đạt trên các nguồn được đo. Bảy mutant mới chết đúng ca, các đối chứng mã hạng, khoản có thân mở bằng chữ cái, từ ghép và viết tắt vẫn qua. Miền dựng nhãn và miền nhận diện còn lệch, xem E1. [D1 gốc](../ops/acceptance/llm-khoan-docx/r1/review-27-codex/VERDICT.md#L64) · [Chốt](../scripts/tl_core/llm_route.py#L510) · [Ca](../scripts/tl_core/llm_route_test.py#L686) |
| §1, §2.2–§2.3 · K1 #1514 | **ĐÃ VÁ THẬT** hai biểu hiện K1 | Dòng điểm quen thuộc bị chặn ở cả nguồn có số và mất số. Dòng mở bằng “là” ở nguồn có số gặp nhánh từ chối dòng không số, còn ở nguồn mất số sẽ thiếu thuật ngữ trước từ nối. Các ca lịch sử và ba bản kết quả đã lưu của Điều 3 đạt 8/8. CLI giữ nguyên định tuyến, `can_nguoi_duyet: true` và ghi đúng `pham_vi_kiem` theo nguồn. [K1 gốc](../ops/acceptance/llm-ranh-gioi-khoan/r1/review-10-codex/VERDICT.md#L35) · [Tách thô](../scripts/tl_core/llm_route.py#L1398) · [CLI](../scripts/tl_core/ops_misc.py#L3130) |
| §2.1, §2.4–§2.13 · vùng Điều, số, điểm, câu dẫn | **ĐÃ VÁ THẬT** cho các biểu hiện còn thuộc hợp đồng. **HẾT ĐỐI TƯỢNG** với cắt cuối Điều, đếm qua bảng và nhận điểm gõ tay đứng riêng | Tiêu đề đúng Điều, nguyên đoạn, đứng đầu nội dung. Vùng tới hết body. Bảng, khối lạ, tiền tố Điều khác, đoạn số rỗng và đoạn không số sau khoản đầu đều chặn. Trước khoản đầu chỉ cho câu dẫn chuẩn nguyên đoạn hoặc vắng. Thiếu đánh số tự động ném `ValueError`, CLI trả 2. Đường DOCX đã bỏ `KhongCauTruc` và fallback. [Vùng](../scripts/tl_core/llm_route.py#L1288) · [Câu dẫn](../scripts/tl_core/llm_route.py#L1378) · [CLI](../scripts/tl_core/ops_misc.py#L3037) |
| §2.4–§2.15, §2.22–§2.26 · số Word và cấu trúc tệp | **ĐÃ VÁ THẬT** với các sai khác đã báo | `start` mặc định 0, `startOverride` thay giá trị cấp, đếm riêng `numId`, reset các cấp con khi cấp cha tăng. Kiểm cấp tổ tiên, trần 999, một danh sách và dãy khoản 1…N. Định nghĩa dùng phải có ID/cấp và kiểu/nhãn khoản khớp chính cấp. Chặn style mang số, reset/isLgl tùy biến, khai báo đơn trị trùng và member ZIP trùng. Định nghĩa lỗi không dùng có đối chứng dương. [Định nghĩa](../scripts/tl_core/llm_route.py#L775) · [Bộ đếm](../scripts/tl_core/llm_route.py#L1260) · [Dãy khoản](../scripts/tl_core/llm_route.py#L1329) |
| §2.5–§2.13, §2.23–§2.29 · chữ còn hiệu lực | **ĐÃ VÁ THẬT** cho các biểu hiện đã báo | Đọc XML gốc. Gạch đơn/kép tính riêng, trực tiếp đè style, nhiều tầng toggle chưa giải được thì chặn. Lọc `del`/`moveFrom`, giữ `ins`/`moveTo`, kiểm sửa dấu đoạn và cân mốc move. Ba đường chữ còn, chữ xóa lạc và ruột bị loại dùng cùng `xml:space` hiệu lực. Giữ phân cách thuần, bỏ trọn mẩu có nội dung. Cờ ngắt và phần tử lạ trong run gạch chỉ truyền khi run còn hiệu lực. [Đọc run](../scripts/tl_core/llm_route.py#L1020) · [Sửa dấu đoạn](../scripts/tl_core/llm_route.py#L1243) |
| §2.14–§2.21 · part, tiền tố, ký tự | **ĐÃ VÁ THẬT** trong miền đã khai | Quan hệ theo URI đầy đủ, từ package tới part chính rồi tới numbering/styles, parser nhận byte, tách namespace. Tiền tố dùng bản chiếu dấu sau khi kiểm chữ gốc. Cả hai đường kiểm miền ký tự trước khi gộp hoặc tách. Số chỉ dùng chữ số ASCII và đường thô bỏ một BOM. Chặn dẫn chiếu mở đoạn, ký tự ngoài danh sách và DOCX Strict theo các giới hạn đã khai. [Quan hệ](../scripts/tl_core/llm_route.py#L734) · [Tập ký tự](../scripts/tl_core/llm_route.py#L592) |
| §2.22–§2.23 · đường số hiệu | **ĐÃ VÁ THẬT** cho chốt strict ở CLI. U2/V3/W1/W3 và phần số hiệu W2 thuộc giới hạn đã duyệt | `tl extract --markup-strict` phải thành công và có mốc Điều. Cờ chạm trần dừng trước model. Các giới hạn cắt Điều, làm sạch cache, gạch qua style, tab/ngắt và chặn bản sạch của bộ đọc dùng chung vẫn được khai. E1 xảy ra sau khi nhận văn bản, áp cả với `--tep` thô. [Extract](../scripts/tl_core/llm_route.py#L1666) · [Giới hạn đã duyệt](../ops/specs/llm-khoan-docx-r28.md#L270) |
| §3 · ca, đột biến và so nguyên văn | **ĐÃ VÁ THẬT** cho các khoảng trống test trước đây. **VÁ MỘT PHẦN** đối với miền nhãn ở E1 | Dùng ca DOCX dương/âm, CLI giả lập rc 0/5/2 và bảng đột biến với tín hiệu của ca đích. Phép so buộc đủ mục, đúng vị trí/stt, đúng hai vế và giữ dòng điểm. Từ nối DOCX chỉ dò ở đầu khoản. Cơ chế so vẫn có thể xác nhận kết quả khớp phân đoạn thô sai ở E1. [So nguyên văn](../scripts/tl_core/llm_route.py#L1561) · [Harness](../scripts/tl_core/llm_route_test.py#L2233) · [Ca CLI](../scripts/tl_selftest.py#L32285) |

### Đối chiếu từng lượt trước

ID finding được đọc cùng số lượt. “Giới hạn đã duyệt” chỉ áp cho đúng đường và biểu hiện được nêu trong spec.

| Lượt | Trạng thái các finding | Đối chiếu trên head |
| --- | --- | --- |
| [1](../ops/acceptance/llm-khoan-docx/r1/review-1-codex/VERDICT.md) | A1 phần cắt, A6 **HẾT ĐỐI TƯỢNG**. Phần còn lại của A1, A2–A5, A7–A8 **ĐÃ VÁ THẬT** | Đọc hết body, kiểm tiêu đề, đếm theo danh sách, giới hạn từ nối ở đầu khoản, đọc XML gốc và giữ hướng dẫn một dòng. |
| [2](../ops/acceptance/llm-khoan-docx/r1/review-2-codex/VERDICT.md) | B1/B2 phần cắt và đếm bảng **HẾT ĐỐI TƯỢNG**. Các biểu hiện còn lại của B1–B8 **ĐÃ VÁ THẬT** | Chốt tiêu đề nguyên đoạn, style đánh số, gạch đơn/kép, no-break hyphen, số thập phân, metadata wrapper và ca đích. |
| [3](../ops/acceptance/llm-khoan-docx/r1/review-3-codex/VERDICT.md) | C1 phần cắt, C2 phần đếm bảng **HẾT ĐỐI TƯỢNG**. Các biểu hiện còn lại của C1–C7 **ĐÃ VÁ THẬT** | Chốt ngắt ở tiêu đề, nhãn chữ lặp kiểu Word, dấu phân cách, toggle, content control nội dòng và hướng dẫn nhãn khoản. |
| [4](../ops/acceptance/llm-khoan-docx/r1/review-4-codex/VERDICT.md) | D1 phần cắt **HẾT ĐỐI TƯỢNG**, phần fallback **ĐÃ VÁ THẬT**. D2–D4/D6 **ĐÃ VÁ THẬT**. D5 là giới hạn đã khai | Chặn restart qua section, đọc XML gốc, chẩn đoán namespace Strict và kiểm nguyên chữ đoạn. |
| [5](../ops/acceptance/llm-khoan-docx/r1/review-5-codex/VERDICT.md) | E1/E3/E4 **HẾT ĐỐI TƯỢNG**. E2/E5/E6 **ĐÃ VÁ THẬT** | Chặn cả bảng. Kiểm toggle nhiều tầng, đường đọc XML gốc và move, miền cấp 0–8. |
| [6](../ops/acceptance/llm-khoan-docx/r1/review-6-codex/VERDICT.md) | F1 phần cắt, F2 phần nhận điểm tay **HẾT ĐỐI TƯỢNG**. F3–F6 **ĐÃ VÁ THẬT** | Chuẩn hóa ID bằng chuỗi, trần số, ca cấp ngoài miền, `ptab` và mốc move đủ cặp. |
| [7](../ops/acceptance/llm-khoan-docx/r1/review-7-codex/VERDICT.md) | G1–G6 **ĐÃ VÁ THẬT** với các biểu hiện đã báo | ID ASCII, chặn nhảy cấp, quan hệ styles, trần số, ngắt trang cuối đoạn, đột biến điểm tay/abstract ID và tiêu đề khác hoa thường. |
| [8](../ops/acceptance/llm-khoan-docx/r1/review-8-codex/VERDICT.md) | H1–H5 **ĐÃ VÁ THẬT** | Tiền tố Điều, quan hệ package, mutant part đổi tên, ID style lỗi và kiểm chữ sau ngắt trang/cột. |
| [9](../ops/acceptance/llm-khoan-docx/r1/review-9-codex/VERDICT.md) | J1–J5 **ĐÃ VÁ THẬT** | Style có thuộc tính đánh số và `mc:` bị chặn, `lvlText` khớp danh sách cho phép, dùng rels của part chính và bỏ chữ gạch sau ngắt. |
| [10](../ops/acceptance/llm-khoan-docx/r1/review-10-codex/VERDICT.md) | K1–K4 **ĐÃ VÁ THẬT** | Chốt `mc:` ở ba part, số thứ tự cấp lớn viết bằng chữ, khớp trọn `lvlText` và ca đọc đến hết tệp. |
| [11](../ops/acceptance/llm-khoan-docx/r1/review-11-codex/VERDICT.md) | L1–L6 **ĐÃ VÁ THẬT** | URI đầy đủ, chốt tiền tố Điều, phân biệt mẫu số thứ tự cấp lớn, lỗi `lvlText` có kiểm soát, parser nhận bytes, tài liệu ghi đủ dấu và bullet. |
| [12](../ops/acceptance/llm-khoan-docx/r1/review-12-codex/VERDICT.md) | M1–M2 **ĐÃ VÁ THẬT** | Không phụ thuộc dấu câu cuối tiêu đề. Giá trị số sai và mốc move thiếu ID được xử lý. |
| [13](../ops/acceptance/llm-khoan-docx/r1/review-13-codex/VERDICT.md) | N1–N3 **ĐÃ VÁ THẬT** | Chiếu dấu câu trước dò tiền tố. ID chuẩn hóa bằng chuỗi. Khối so QName đầy đủ. |
| [14](../ops/acceptance/llm-khoan-docx/r1/review-14-codex/VERDICT.md) | Q1–Q2 **ĐÃ VÁ THẬT** | Thứ tự kiểm ký tự và dò đầu đoạn. Hướng dẫn giữ chữ nguồn và làm thủ công khi dẫn chiếu mở đoạn. |
| [15](../ops/acceptance/llm-khoan-docx/r1/review-15-codex/VERDICT.md) | R1–R3 **ĐÃ VÁ THẬT** | Chốt chữ trước gộp khoảng trắng, chặn số gõ tay ngoặc kín, chặn ký tự định dạng trên nguồn thô. |
| [16](../ops/acceptance/llm-khoan-docx/r1/review-16-codex/VERDICT.md) | S1–S3 **ĐÃ VÁ THẬT** | Danh sách ký tự cho phép, chốt trước tách dòng, đối chứng `permStart`/`permEnd`. |
| [17](../ops/acceptance/llm-khoan-docx/r1/review-17-codex/VERDICT.md) | T1–T2 **ĐÃ VÁ THẬT** ở hai cửa kiểm. Phần producer theo U2 | Chặn số mũ, đọc UTF-8 thường, bỏ một BOM tại tầng dùng chung. |
| [18](../ops/acceptance/llm-khoan-docx/r1/review-18-codex/VERDICT.md) | U1 **ĐÃ VÁ THẬT**. U2 là giới hạn đã duyệt | Chữ số ASCII ở mọi chốt. Việc làm sạch nguồn theo số hiệu được ghi tại §2.21. |
| [19](../ops/acceptance/llm-khoan-docx/r1/review-19-codex/VERDICT.md) | V1/V2/V4 **ĐÃ VÁ THẬT** cho biểu hiện gốc. V3 là giới hạn đã duyệt | Cờ strict, chặn số từ mặc định đoạn, chặn nhãn chữ kết chấm. |
| [20](../ops/acceptance/llm-khoan-docx/r1/review-20-codex/VERDICT.md) | W2 DOCX, W4/W5 **ĐÃ VÁ THẬT** cho biểu hiện gốc. W1/W3 và W2 số hiệu là giới hạn đã duyệt | Giữ phân cách thuần, chặn nhãn chữ hoa/lặp và cấp hoặc override trùng. |
| [21](../ops/acceptance/llm-khoan-docx/r1/review-21-codex/VERDICT.md) | X1–X3 **ĐÃ VÁ THẬT** cho biểu hiện gốc | Giữ tab/ngắt thuần trong mẩu đã bỏ, kiểm trường đơn trị, chặn nhãn chữ nối gạch và giữ đối chứng từ ghép. |
| [22](../ops/acceptance/llm-khoan-docx/r1/review-22-codex/VERDICT.md) | Y1–Y3 **ĐÃ VÁ THẬT** cho biểu hiện gốc | Chung phép đọc ruột, đơn trị ở nút chọn vùng và khóa style, đo nhãn có khoảng đệm và dấu. |
| [23](../ops/acceptance/llm-khoan-docx/r1/review-23-codex/VERDICT.md) | Z1–Z4 **ĐÃ VÁ THẬT** cho biểu hiện gốc | Nội dung lạ trong mẩu bị bỏ, member ZIP trùng, nhãn số–số có ngoặc và mutant riêng trường metadata. |
| [24](../ops/acceptance/llm-khoan-docx/r1/review-24-codex/VERDICT.md) | A1/A2 **ĐÃ VÁ THẬT** cho biểu hiện gốc | `xml:space` theo cây, nhãn số–số kết bằng gạch. |
| [25](../ops/acceptance/llm-khoan-docx/r1/review-25-codex/VERDICT.md) | B1 **VÁ MỘT PHẦN** theo miền còn sót ở E1. B2/B3 **ĐÃ VÁ THẬT** | Khoảng cách giữa bộ nhận và bộ dựng vẫn còn. Các mutant đặt lại `xml:space`, mẩu đã bỏ, `delText` lạc và cờ ngắt đều chết đúng ca. |
| [26](../ops/acceptance/llm-khoan-docx/r1/review-26-codex/VERDICT.md) | C1 **ĐÃ VÁ THẬT** với hai biểu hiện gốc, **VÁ MỘT PHẦN** với miền nhãn. C2 **ĐÃ VÁ THẬT** | Chặn đảo thứ tự số đơn và nhãn đa cấp ở các dạng có ca. Trì hoãn truyền cờ ký hiệu lạ tới sau lọc run. |
| [27](../ops/acceptance/llm-khoan-docx/r1/review-27-codex/VERDICT.md) | D1 **ĐÃ VÁ THẬT** ba biểu hiện gốc, **VÁ MỘT PHẦN** lớp | Bảy mutant r28 vào đúng tín hiệu. E1 giữ slug lớp cũ. |

Lịch sử #1514 còn ca A1/A2/D3/E2/F2 về câu dẫn và chia khoản, C1 về tiêu đề dính thân, A3/C2/D1/E1/F1 về dấu kết và số nội dòng, A4 về ba fixture, và G1/H1/J1/K1 về ghép dòng điểm. Các hình dạng tiêu đề bị chặn trong D2 và giới hạn điểm của C2 đã ghi trong hợp đồng thô. Dãy số ở cuối khoản một dòng vẫn có đối chứng dương. [Ca #1514](../scripts/tl_core/llm_route_test.py#L1073) · [Giới hạn đường thô](../docs/GOI_AGENT_DA_NEN.md#L368)

Finding B1 về bề mặt của #1514 lượt 1 đã được giải quyết cho lượt hiện hành. Lease r28 và launcher cùng ghi `codex_cli`. Lượt lịch sử vẫn giữ bằng chứng lệch bề mặt tại thời điểm đó. [Verdict #1514 lượt 1](../ops/acceptance/llm-ranh-gioi-khoan/r1/review-1-codex/VERDICT.md)

## Findings

### E1 [P2] Nhãn nhiều cấp mà Word dựng được vẫn có thể thành khoản thô — `scripts/tl_core/llm_route.py:522`

**Kịch bản.** Danh sách có khoản cấp cha và điểm số ở cấp con. Định dạng nhãn con đặt một dấu chấm đầu, sau đó in số cha, dấu chấm, số con và dấu chấm kết. Đây là một nhãn trong miền `lvlText` của bộ dựng, có dấu chấm giữa hai cấp. Khi bản văn bản giữ nhãn điểm kiểu này nhưng đã mất số đầu khoản, một dòng điểm có đầy đủ hai vế định nghĩa có thể trở thành khoản riêng. Điều kiện là nguồn không còn dòng khớp mẫu số khoản ở đầu và các dòng còn lại cũng có hình dạng khoản một dòng. [Miền nhãn §2.29–§2.30](../ops/specs/llm-khoan-docx-r28.md#L346) · [Bộ dựng nhãn](../scripts/tl_core/llm_route.py#L955)

**Căn cứ.** `_nhan` cho dấu chấm trước placeholder. Cả `_RE_NHIEU_CAP` và `_RE_DIEM` đều đòi placeholder ở đầu sau phần đệm và dấu ngoặc mở tùy chọn. Nhánh bullet cũng không có dấu chấm. `_RE_SO_KHOAN` không nhận số đứng sau dấu chấm đầu nhãn. Mỗi số trong nhãn đã có dấu chấm ngay trước nên `_RE_SO_NOI_DONG` cũng bỏ qua. Sau khi qua chốt dấu phân cách và dấu kết câu, `tach_khoan` đưa nguyên dòng vào dãy mất số. Nếu model lấy chính phần trước từ nối làm thuật ngữ và đánh số theo dãy sai này, `lech_nguyen_van` sẽ chấp nhận hai vế. CLI có thể ghi kết quả vào `--out`. Chuỗi quyết định này xảy ra với `--tep` thô, độc lập với các giới hạn producer của đường số hiệu. [Matcher và nội dòng](../scripts/tl_core/llm_route.py#L490) · [Tách dòng](../scripts/tl_core/llm_route.py#L1426) · [So](../scripts/tl_core/llm_route.py#L1561) · [Ghi kết quả](../scripts/tl_core/ops_misc.py#L3133)

**Hạng và đề xuất.** P2 theo tiền lệ D1 và K1. Để nhận sai cần văn bản đã mất cấp danh sách, bố cục thỏa các chốt còn lại và đầu ra model khớp phân đoạn đó. Kết quả vẫn mang cờ duyệt ranh giới. Đóng lớp bằng một quy tắc về vị trí dấu và placeholder dùng chung giữa miền dựng và miền nhận, hoặc công bố ranh giới hỗ trợ hẹp hơn bằng quyết định có thẩm quyền. Phép kiểm đóng lớp cần bao phủ dấu ở đầu, giữa và cuối nhãn, nhiều cấu phần, nguồn có số và mất số, cùng các đối chứng khoản một dòng đã có. [Protocol §8.3](../docs/PROTOCOL_DA_PHIEN.md#L812) · [ADR-0060 M1–M2](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32)

| Lớp | Lịch sử và trạng thái | Phép kiểm đóng lớp |
| --- | --- | --- |
| `ranh-gioi-khoan` | K1 #1514 → V4/W4/X3/Y3/Z3/A2 lượt 24/B1/C1/D1 → E1. Ba biểu hiện D1 gốc đã đóng. Còn **một lớp, một finding P2, một biểu hiện được xác lập bằng đọc mã**. | Đối chiếu miền nhãn trước mọi cửa nhận số đơn, đo cả nguồn có số, nguồn mất số và đối chứng khoản một dòng. |
| `docx-khoang-trang-sau-loc` | W2/X1/Y1/Z1/A1 lượt 24/B3/C2. Đã đóng các biểu hiện báo trước trong miền đo. | Giữ phân cách thuần, bỏ trọn mẩu có chữ và kiểm riêng phần tử còn hiệu lực. |
| `docx-so-hien-thi` | A2/B2/G1/J1/V2/W5/X2/Y2/Z2. Đã đóng các biểu hiện báo trước trong miền đo. | Kiểm bộ đếm, reset, các khai báo mâu thuẫn khi dùng và đối chứng định nghĩa không dùng. |
| `docx-test-doc-lap` | A7/B7/C6/D4/E5/F5/G5/H3/J4/Z4/B2. Đã đóng các khoảng trống báo trước. | Đối chiếu neo đột biến, ca đích và lý do từ chối. Phép đo còn thiếu của E1 thuộc lớp ranh giới. |

Lượt 28 đóng ba biểu hiện D1 đã báo. Số lớp mở của lượt 27 giữ 1 → 1. Trên đường DOCX, đọc mã và ca có sẵn chưa cho thấy đường bỏ/gộp/cắt/tráo khoản hoặc nhận chữ đã bỏ trong phạm vi cấu trúc đã khai. Với Word/Google Docs, các phần tử định dạng gặp trong ca sẵn có gồm mốc bookmark/comment/permission, content control, no-break hyphen, tab và ngắt trang cuối đoạn. Các đường loại trừ như field, hình, chú thích, bảng, `mc:` và số qua style đã có trong đặc tả hoặc hướng dẫn. Lượt offline chưa xác lập phần tử export phổ biến nào khác gây chặn oan ngoài phạm vi đã khai. [Danh sách đọc đoạn](../scripts/tl_core/llm_route.py#L640) · [Hướng dẫn DOCX](../docs/GOI_AGENT_DA_NEN.md#L390)

## Kết quả test và đột biến

Linux x86_64, Python 3.13.18, Git 2.43.0, Codex CLI 0.172.0, `core.abbrev=7`. Hai checkout shallow, detached, lấy object từ kho local và xác nhận đúng OID/tree. Base có tree `0cc14e79cecd2ce44bc4dc6cff92cadb31fd7ee4`. Các phép đo đặt `PYTHONDONTWRITEBYTECODE=1`. Selftest base dùng thư mục tạm riêng trong cùng cây scratch. Log và mã thoát của các phép đo ở `/tmp/wp1525-r28-measure.cLdfSb/`.

| Lệnh | Trạng thái | Mã thoát và bằng chứng |
| --- | --- | --- |
| `python scripts/tl_core/llm_route_test.py` | `passed` | rc 0, **63/63** ca, **250/250** mutant chết. `route.log`. |
| `python scripts/tl.py --deterministic workflow-audit --strict --json` | `passed` | rc 0, `ok=true`, 194 lệnh, 26 card, 11 nhóm, 60 task, 0 lỗi, 0 cảnh báo. `audit.log`. |
| `python scripts/tl.py --deterministic golden-test --json` | `passed` | rc 0, `ok=true`, **20/20** khớp fixture, **20/20** bản chiếu ổn định, **20/20** byte thô ổn định. `golden.log`. |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | `passed` | rc 0, `ok=true`, **187/187** tệp, sai/thiếu/thừa đều 0. Hash gói khớp `bdb1e6a478fa77c48438558f7e8cc580652c28ae26acdd3891cc6a57074c1f42`. `release.log`. |
| `python ops/lease_publish.py check --root . ops/leases/llm-khoan-docx-r28-g1-claude.yaml` | `passed` cục bộ | rc 0, “ĐĂNG ĐƯỢC”, #1525, neo `64b7f2c14776`, hết hạn 20:33 UTC. `lease.log`. Lệnh này có phạm vi local. |
| `python scripts/tl.py --selftest` · head | `failed` | rc 1, **1774/1790**, transport **12/12**, ca `r1525_llm_khai_niem_tep_docx_cau_truc` đạt. `selftest.log`. |
| Cùng lệnh selftest · base | `failed` | rc 1, **1773/1789**, transport **12/12**, trùng cả 16 ID đỏ trên head. `base-selftest.log`. |
| `python scripts/tl.py --deterministic determinism-audit --strict --json` | `passed` | rc 0, `ok=true`, **15/15** chốt. `determinism.log`. |
| `python scripts/tl.py --deterministic doc-claims-check --strict --json` · head và base | `failed` | Cả hai rc 2, 410 advisory và cùng một cờ cứng `SHA_NOT_A_COMMIT` cho `9941d8af52aeede1c78ea4e232fbe9a8d5272033` ở protocol dòng 1680. Object này vắng trong checkout test shallow. `doc-claims.log`, `base-doc-claims.log`. |
| `python -m ruff check --no-cache --select F --output-format json scripts/tl.py` · head và base | `failed` cho lint, delta 0 | Ruff 0.15.15, cả hai rc 1, cùng 12 F821. Vị trí và nội dung khớp sau khi loại tiền tố checkout. `ruff-head.log`, `ruff-base.log`. |
| `loi_ruff_ci()` trong `.claude/dev/ci_dang_ky_test.py` qua `runpy.run_path` | `passed` | rc 0, `RUFF_CONTRACT 3 []`. `ruff-contract.log`. |
| `git diff --check cda9439 HEAD` và `git diff --check fcb12b3 HEAD` | `passed` | Cả hai rc 0. Trên toàn PR từ base, lệnh tương ứng rc 2 ở ba dấu ngắt dòng Markdown của hồ sơ kế thừa #1514 lượt 8. |

`cmp selftest.fail-ids base-selftest.fail-ids` rc 0. Có 14 ca thuộc nhóm lỗi môi trường `/tmp/.git` rỗng trong prompt (8 `r973_bootstrap_*`, 5 `wp433_*`, 1 `wp727_tl_gws_refresh`). Hai ca còn lại cũng đỏ ở base, `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` và `r268_l2_trichotomy_theo_trang_thai_object`. SHA-256 log head `08ef1c5a659b7aeeae1d3d7c94f333e9c4efb791bd4019a47451ee41ba41ccb0`, log base `4f392094559de5b90da305e92452e223de4ad7ff459724ffe1aeab6731a8b65b`. Delta ID đỏ bằng 0. Hai tiêu chí selftest N/N và doc-claims strict rc 0 ở §5 còn thiếu bằng chứng dương.

Harness `DOT_BIEN` tạo bản đột biến trong thư mục tạm và chỉ tính kill ở nhánh `TinHieuChotCa` của ca đích. Đã chạy lại bộ ca sẵn có qua `python -B -m pdb scripts/tl_core/llm_route_test.py`, breakpoint ở dòng 2253, điều kiện tên `wp1525_*`. Tiến trình và suite đều rc 0, log `target-mutants.log` ghi **153/153** mutant của packet đi vào đúng nhánh kill. SHA-256 `0be738d8f05a112846a9dc314889056583e960ba6ac935e11f11a2b711735590`.

| Mutant có sẵn | Tín hiệu của ca đích |
| --- | --- |
| `wp1525_nhieu_cap_noi_chi_cham`, `wp1525_nhieu_cap_mot_dau` | `ca_khoan_mat_so_co_diem_dat` bắt số–số nối gạch và số–số có hai dấu nối, trong đó dạng hai dấu có ca nguồn có số. |
| `wp1525_nhieu_cap_bo_so_chu`, `wp1525_nhieu_cap_bo_chu_truoc` | Cùng ca bắt số–chữ trong nguồn có số và chữ–chữ nối gạch trong nguồn mất số. |
| `wp1525_nhieu_cap_bo_so_dinh_chu`, `wp1525_nhieu_cap_bo_chu_dinh_so` | Cùng ca bắt hai thứ tự liền nhau. |
| `wp1525_chu_rieng_dinh_chu` | Cùng ca bắt đối chứng viết tắt hoặc từ ghép bị chặn oan. |
| `wp1525_tho_nhan_diem` | `ca_wp1514_luot9` bắt dòng điểm thông thường bị nhận thành khoản mới. |
| `wp1525_khong_dat_lai_cap_con`, `wp1525_bo_qua_start_override` | `ca_cau_truc_docx_dat` bắt nhãn con tiếp số sai và dãy khoản bắt đầu sai do mất override. |

## Không đo được

- E1 được xác lập qua đọc mã. Chưa đo đầu-cuối cho dạng nhãn còn lọt hay tần suất giữ nhãn ấy trong bản xuất Word/Google Docs. Kho có 0 tệp DOCX được Git theo dõi. Bộ test dùng fixture có sẵn, và phép đo `xml:space` ở đây phản ánh CLI tuần tự.
- `skipped` ở cấp sáu lệnh prompt là 0. `not_run` gồm Windows bản địa, CI, hai phép kiểm GitHub của lease và các phép dùng model thật hoặc LIVE. M3 xếp Windows là `required` vì diff toàn PR có sửa dòng `encoding=` trong mã Python. Bằng chứng Windows cho exact head còn thiếu. [ADR-0060 M3](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L43)
- Metadata đang chạy chưa chứa trạng thái terminal, mã thoát con hoặc hash stdout. Các trường này thuộc biên nhận launcher sau khi phiên review kết thúc. Phạm vi quan sát GitHub chỉ là refs và object đã cấp cục bộ.
- HEAD và tree đầu/cuối khớp. `git diff --exit-code` và `git diff --cached --exit-code` đều rc 0. Snapshot status trước/sau ghi nhận `.codex/` đã tồn tại và `.review/VERDICT.md` là đường dẫn mới duy nhất. So sánh xác nhận chênh lệch quan sát được giữa hai mốc ở checkout giao review.

Theo quy tắc verdict nội dung của prompt, có **0 P0, 0 P1, 1 P2 và 0 P3** mở. E1 chặn merge theo ADR-0060 M1. Bằng chứng selftest N/N, doc-claims strict và Windows còn thiếu theo bảng trên. [ADR-0060](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32) · [ADR-0062](../docs/adr/0062-adr-0060-mac-dinh-va-dong-bang-adr-0054.md#L12)

P2_mo: 1
VERDICT: APPROVE
