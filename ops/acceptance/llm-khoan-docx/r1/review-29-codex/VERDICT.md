# Verdict packet #1525 r29 lượt 29 — Codex

reviewed_sha: 291919e66d40e9b8d88af484956a1978417d6ad4
reviewed_tree: 8afcb9e65764f7fc36343a5370916652ec6b099f
base_sha: 64b7f2c14776d5d0e1d34a6be4725490956f5bec


## Phạm vi và preflight

- Reviewer độc lập `openai_codex / codex_cli / machine`, run launcher `a692d7b78f6c463783810a4214032701`. Executor theo lease `claude / claude_code / machine/local`. Class khai báo và hiệu lực đều `sensitive`. Sandbox `workspace-write`; checkout giao review được dùng ở chế độ chỉ đọc với tệp theo dõi. Metadata của run đang chạy chưa cho phép đo model hoặc effort phục vụ (`KHONG_DO_DUOC`). SHA-256 prompt `f60add8b9caf6c3a246d017662479cd2cdb31491c9da7ff75d5d6d02cb9ecd75` khớp receipt đang chạy. [Run](../../run/a692d7b7/run.json)
- Checkout detached đúng SHA/tree trên, origin trỏ `ducthangho/tra-luat`; ref local của nhánh được giao trỏ cùng head. Merge-base đúng base. Đã đối chiếu diff bản vá từ `599b90cd50d3ab7f99247eeb705f9a985b6baf4a`, diff packet từ `fcb12b3873c3bec2c339029136243ed2c804ce05` và diff toàn PR (200 đường dẫn).
- Lease #1525 r29/g1 còn hiệu lực tại lúc đo, hết hạn 20:52 UTC ngày 2026-11-26, lượt 29/29, inference budget 0. Base trong lease khớp base giao review. SHA-256 spec trên đĩa và blob head cùng `d53a4c5698cccca56595243901e5279e57e034d52423db90edf11f83856a166a`, khớp lease. Quyền đứng nâng trần và ngoại lệ M5 có ghi ở đầu spec. [Lease](../ops/leases/llm-khoan-docx-r29-g1-claude.yaml) · [Đặc tả](../ops/specs/llm-khoan-docx-r29.md)
- Write set 156 đường dẫn, hash sau sắp xếp `11d71e6d9b776d6a7aeaa1771f16cd7a3a06b19f4d03e93fa4b41dd636287168`. So `git diff --name-only` với lease bằng `comm -23` cho 8/8 đường dẫn của bản vá và 152/152 của packet sau khi trừ hồ sơ #1514 theo prompt. Kiểm 29/29 cặp bia mộ hai chiều từ #1514 r9 ⇄ #1525 r1 ⇄ … ⇄ r29 và 30/30 hash spec trên đĩa lẫn blob Git. Cả chuỗi cùng branch, base và generation. [Bia mộ #1514](../ops/leases/llm-ranh-gioi-khoan-r9-g1-claude.yaml#L97) · [Lease r29](../ops/leases/llm-khoan-docx-r29-g1-claude.yaml#L188)

## Đối chiếu lượt 28 và đặc tả r29

| Mục | Trạng thái | Bằng chứng |
| --- | --- | --- |
| E1 lượt 28 (`0e1c1122bee44aef58347f585bdcb09ed48af7c6`) · §2.31 | **ĐÃ VÁ THẬT** ở các hình dạng tiền tố đã báo. **VÁ MỘT PHẦN** lớp `ranh-gioi-khoan` | Hai mutant tiền tố chết ở ca nguồn mất số. Ca đối chứng có từ sau ngoặc vẫn qua. Nhánh số đơn vẫn giành trước một dạng nằm trong miền nhãn hợp lệ của bộ dựng. Xem F1. [E1 gốc](../ops/acceptance/llm-khoan-docx/r1/review-28-codex/VERDICT.md#L68) · [Nhận nhãn](../scripts/tl_core/llm_route.py#L524) |
| §1, §2.2–§2.3 · K1 #1514 | **ĐÃ VÁ THẬT** hai cơ chế ghép dòng đã báo | Số khoản mở một dòng riêng. Dòng điểm thông dụng trả `None` ở nguồn có số hoặc mất số. Dòng mở bằng “là” ở nguồn có số bị từ chối vì thiếu số khoản. Ở nguồn mất số, dòng ấy thiếu vế thuật ngữ khi so. Ca lịch sử giữ ba đầu ra 8/8 của Điều 3 Luật 134/2025/QH15. Định tuyến model giữ nguyên, kết quả vẫn gắn `can_nguoi_duyet: true` và chọn `pham_vi_kiem` theo nguồn. [K1 gốc](../ops/acceptance/llm-ranh-gioi-khoan/r1/review-10-codex/VERDICT.md#L35) · [Tách dòng](../scripts/tl_core/llm_route.py#L1432) · [CLI](../scripts/tl_core/ops_misc.py#L3130) |
| §2.1, §2.4–§2.13 · vùng Điều, điểm và câu dẫn | **ĐÃ VÁ THẬT** với các biểu hiện còn thuộc hợp đồng. **HẾT ĐỐI TƯỢNG** với cắt cuối Điều, đếm qua bảng và nhận điểm gõ tay đứng riêng | Tiêu đề nguyên đoạn, đúng số Điều, đứng đầu nội dung. Vùng đến hết thân tệp. Bảng, khối lạ, tiền tố Điều khác, đoạn số rỗng và đoạn không số sau khoản đầu bị chặn. Trước khoản đầu chỉ nhận tối đa một câu dẫn chuẩn khớp nguyên đoạn. Thiếu đánh số tự động là `ValueError` → CLI rc 2, đường `KhongCauTruc` đã bỏ. [Vùng Điều](../scripts/tl_core/llm_route.py#L1294) · [Câu dẫn](../scripts/tl_core/llm_route.py#L1384) · [CLI](../scripts/tl_core/ops_misc.py#L3037) |
| §2.4–§2.15, §2.22–§2.26 · số Word | **ĐÃ VÁ THẬT** các lệch số đã báo | `start` mặc định 0, `startOverride` thay start của cấp tương ứng. Bộ đếm theo từng `numId`, cấp trên tăng thì xóa các cấp con đã đếm, cấp con trước tổ tiên bị chặn. Tại bước ghép khoản chỉ nhận chung một `numId`, cấp khoản `decimal` với nhãn chính cấp, số chạy từ 1. Chặn trùng ID/cấp, trường đơn trị mâu thuẫn, reset hoặc liên kết style không hỗ trợ và mức đếm trên 999. Ca dương giữ định nghĩa lỗi không dùng. [Định nghĩa](../scripts/tl_core/llm_route.py#L781) · [Bộ đếm](../scripts/tl_core/llm_route.py#L1266) · [Ghép khoản](../scripts/tl_core/llm_route.py#L1345) |
| §2.5–§2.13, §2.23–§2.29 · chữ còn hiệu lực | **ĐÃ VÁ THẬT** với các biểu hiện đã báo. **VÁ MỘT PHẦN** lớp gạch kế thừa | Đọc XML gốc, gạch đơn/kép tính riêng, trực tiếp đè style, nhiều tầng bật chưa giải được thì chặn. Lọc `del`/`moveFrom`, giữ `ins`/`moveTo`, kiểm sửa dấu đoạn và cân mốc move. Đọc chữ còn, chữ xóa lạc và ruột bị bỏ theo cùng `xml:space`; giữ phân cách thuần. Cờ ngắt và phần tử lạ xét sau lọc run. Trường hợp tham chiếu style đoạn không phân giải được còn ở F2. [Đọc style](../scripts/tl_core/llm_route.py#L882) · [Đọc run](../scripts/tl_core/llm_route.py#L1081) · [Sửa dấu đoạn](../scripts/tl_core/llm_route.py#L1249) |
| §2.14–§2.21 · part, tiền tố, ký tự | **ĐÃ VÁ THẬT** trong miền hợp đồng | Part theo URI đầy đủ từ package tới part chính rồi tới numbering/styles, parser nhận byte. Đoạn/khối theo QName. Kiểm tập ký tự trước khi quyết nhận chữ, đường thô kiểm trước tách dòng và chỉ bỏ một BOM. Dò tiền tố thân Điều theo bản chiếu dấu. Giới hạn dẫn chiếu mở đoạn, chữ ngoài tập và DOCX Strict đã khai. [Quan hệ](../scripts/tl_core/llm_route.py#L740) · [Ký tự](../scripts/tl_core/llm_route.py#L598) |
| §2.22–§2.23 · đường số hiệu | **ĐÃ VÁ THẬT** chốt strict ở CLI. U2, V3, W1/W3 và phần số hiệu W2 thuộc giới hạn đã duyệt | `tl extract --markup-strict` phải có rc 0 và mốc Điều; cờ chạm trần dừng trước model. Giới hạn về cắt Điều, làm sạch cache, gạch qua style, bỏ tab/ngắt và chặn bản sạch nằm ở bộ đọc dùng chung. F1 xảy ra sau khi nhận văn bản thô, gồm cả `--tep` văn bản. [Chốt extract](../scripts/tl_core/llm_route.py#L1672) · [Giới hạn](../ops/specs/llm-khoan-docx-r29.md#L270) |
| §3 · test và phép so nguyên văn | **ĐÃ VÁ THẬT** các lỗ test đã nêu. **VÁ MỘT PHẦN** với miền nhãn của E1 | Ca DOCX dương/âm, CLI giả lập rc 0/5/2 và mutant đúng ca đích. Phép so buộc đủ số mục, đúng vị trí/stt, đúng hai vế, giữ dòng điểm. Với DOCX từ nối chỉ được lấy ở đầu khoản. F1/F2 có thể qua vì phép so dùng chính biểu diễn nguồn đã dựng. [Phép so](../scripts/tl_core/llm_route.py#L1567) · [Harness](../scripts/tl_core/llm_route_test.py#L2241) |

### Các finding lịch sử #1525

ID đọc kèm số lượt. Cột cuối ghi hành vi trên head, đọc cùng các neo trong bảng trên.

| Lượt | Trạng thái | Đối chiếu |
| --- | --- | --- |
| [1](../ops/acceptance/llm-khoan-docx/r1/review-1-codex/VERDICT.md) | A1 phần cắt và A6 **HẾT ĐỐI TƯỢNG**. Phần còn lại A1, A2–A5, A7–A8 **ĐÃ VÁ THẬT** với các biểu hiện gốc. | Đọc hết body, chặn tiêu đề lạ, đếm theo danh sách, dò từ nối ở đầu khoản, đọc XML gốc và hướng dẫn một dòng. F2 thuộc phạm vi style gạch của A4. |
| [2](../ops/acceptance/llm-khoan-docx/r1/review-2-codex/VERDICT.md) | B1/B2 phần cắt và đếm bảng **HẾT ĐỐI TƯỢNG**. Phần còn lại B1–B8 **ĐÃ VÁ THẬT** với các biểu hiện gốc. | Tiêu đề nguyên đoạn, giới hạn style đánh số, gạch đơn/kép, no-break hyphen, số thập phân, metadata wrapper và ca đích. |
| [3](../ops/acceptance/llm-khoan-docx/r1/review-3-codex/VERDICT.md) | C1 phần cắt, C2 phần đếm bảng **HẾT ĐỐI TƯỢNG**. Các biểu hiện còn lại C1–C7 **ĐÃ VÁ THẬT**. | Kiểm ngắt ở tiêu đề, nhãn chữ lặp, dấu phân cách, toggle, content control nội dòng và nhãn khoản. |
| [4](../ops/acceptance/llm-khoan-docx/r1/review-4-codex/VERDICT.md) | D1 phần cắt **HẾT ĐỐI TƯỢNG**, phần fallback **ĐÃ VÁ THẬT**. D2–D4/D6 **ĐÃ VÁ THẬT**. D5 có giới hạn đã khai. | Chặn restart qua section, đọc XML gốc, chẩn đoán namespace Strict, kiểm nguyên chữ đoạn. |
| [5](../ops/acceptance/llm-khoan-docx/r1/review-5-codex/VERDICT.md) | E1/E3/E4 **HẾT ĐỐI TƯỢNG**. E2/E5/E6 **ĐÃ VÁ THẬT**. | Chặn cả bảng; kiểm toggle nhiều tầng, đọc XML gốc, lọc move và miền cấp 0–8. |
| [6](../ops/acceptance/llm-khoan-docx/r1/review-6-codex/VERDICT.md) | F1 phần cắt và F2 phần nhận điểm tay **HẾT ĐỐI TƯỢNG**. F3–F6 **ĐÃ VÁ THẬT**. | Chuẩn hóa ID, trần số, ca riêng miền cấp, `ptab` và mốc move đủ cặp. |
| [7](../ops/acceptance/llm-khoan-docx/r1/review-7-codex/VERDICT.md) | G1–G6 **ĐÃ VÁ THẬT** với các biểu hiện gốc. | ID ASCII, chặn nhảy cấp, quan hệ styles, trần số, ngắt trang cuối đoạn, mutant điểm tay/abstract ID và tiêu đề khác hoa thường. |
| [8](../ops/acceptance/llm-khoan-docx/r1/review-8-codex/VERDICT.md) | H1–H5 **ĐÃ VÁ THẬT**. | Tiền tố Điều, quan hệ package, mutant part đổi tên, ID style lỗi và chữ sau ngắt trang/cột. |
| [9](../ops/acceptance/llm-khoan-docx/r1/review-9-codex/VERDICT.md) | J1–J5 **ĐÃ VÁ THẬT**. | Chặn style mang số, chặn `mc:`, khớp trọn `lvlText`, đọc rels riêng của part chính, bỏ chữ gạch sau ngắt. |
| [10](../ops/acceptance/llm-khoan-docx/r1/review-10-codex/VERDICT.md) | K1–K4 **ĐÃ VÁ THẬT**. | Chốt `mc:` ở ba part, số thứ tự cấp lớn viết bằng chữ, miền `lvlText`, đọc tới hết tệp. |
| [11](../ops/acceptance/llm-khoan-docx/r1/review-11-codex/VERDICT.md) | L1–L6 **ĐÃ VÁ THẬT**. | URI đầy đủ, tiền tố Điều, dạng số thứ tự cấp lớn, lỗi `lvlText` có kiểm soát, parser nhận bytes và hướng dẫn nhãn. |
| [12](../ops/acceptance/llm-khoan-docx/r1/review-12-codex/VERDICT.md) | M1–M2 **ĐÃ VÁ THẬT**. | Tiền tố Điều đứng độc lập với dấu cuối. Giá trị số sai và mốc move thiếu ID có chẩn đoán. |
| [13](../ops/acceptance/llm-khoan-docx/r1/review-13-codex/VERDICT.md) | N1–N3 **ĐÃ VÁ THẬT**. | Chiếu dấu trước khi dò tiền tố, ID bằng chuỗi, khối theo QName. |
| [14](../ops/acceptance/llm-khoan-docx/r1/review-14-codex/VERDICT.md) | Q1–Q2 **ĐÃ VÁ THẬT**. | Chốt ký tự trước dò đầu đoạn, hướng dẫn giữ nguyên chữ nguồn. |
| [15](../ops/acceptance/llm-khoan-docx/r1/review-15-codex/VERDICT.md) | R1–R3 **ĐÃ VÁ THẬT**. | Chốt chữ trước gộp, số tay ngoặc kín và ký tự định dạng ở nguồn thô. |
| [16](../ops/acceptance/llm-khoan-docx/r1/review-16-codex/VERDICT.md) | S1–S3 **ĐÃ VÁ THẬT**. | Danh sách cho phép, kiểm trước tách dòng và ca `permStart`/`permEnd`. |
| [17](../ops/acceptance/llm-khoan-docx/r1/review-17-codex/VERDICT.md) | T1–T2 **ĐÃ VÁ THẬT** ở cửa kiểm thuộc packet. | Số mũ ngoài miền, UTF-8 thường, bỏ BOM ở lớp dùng chung. Producer thuộc U2. |
| [18](../ops/acceptance/llm-khoan-docx/r1/review-18-codex/VERDICT.md) | U1 **ĐÃ VÁ THẬT**. U2 có giới hạn đã duyệt. | Mọi chốt cú pháp dùng chữ số ASCII. Việc làm sạch nguồn theo số hiệu đã khai. |
| [19](../ops/acceptance/llm-khoan-docx/r1/review-19-codex/VERDICT.md) | V1/V2/V4 **ĐÃ VÁ THẬT** với các biểu hiện gốc. V3 có giới hạn đã duyệt. | Strict, chặn số ở mặc định đoạn, chặn nhãn chữ kết chấm. |
| [20](../ops/acceptance/llm-khoan-docx/r1/review-20-codex/VERDICT.md) | W2 DOCX và W4/W5 **ĐÃ VÁ THẬT**. W1/W3 và W2 số hiệu có giới hạn đã duyệt. | Giữ phân cách thuần, chặn nhãn chữ hoa/lặp, cấp và override trùng. |
| [21](../ops/acceptance/llm-khoan-docx/r1/review-21-codex/VERDICT.md) | X1–X3 **ĐÃ VÁ THẬT**. | Giữ tab/ngắt thuần trong mẩu đã bỏ, kiểm trường đơn trị, chặn nhãn chữ nối gạch. |
| [22](../ops/acceptance/llm-khoan-docx/r1/review-22-codex/VERDICT.md) | Y1–Y3 **ĐÃ VÁ THẬT** với các biểu hiện gốc. | Chung phép đọc ruột, đơn trị ở nút chọn vùng và khóa style, nhận đệm ngang trong nhãn. |
| [23](../ops/acceptance/llm-khoan-docx/r1/review-23-codex/VERDICT.md) | Z1–Z4 **ĐÃ VÁ THẬT**. | Nội dung lạ trong mẩu bị bỏ, member ZIP trùng, nhãn số–số có ngoặc, mutant riêng trường metadata. |
| [24](../ops/acceptance/llm-khoan-docx/r1/review-24-codex/VERDICT.md) | A1/A2 **ĐÃ VÁ THẬT** với các biểu hiện gốc. | `xml:space` theo cây, nhãn số–số kết bằng gạch. |
| [25](../ops/acceptance/llm-khoan-docx/r1/review-25-codex/VERDICT.md) | B1 **VÁ MỘT PHẦN** theo F1. B2/B3 **ĐÃ VÁ THẬT**. | Mutant đặt lại `xml:space`, ruột bị bỏ, `delText` lạc và cờ ngắt đều chết. |
| [26](../ops/acceptance/llm-khoan-docx/r1/review-26-codex/VERDICT.md) | C1 **ĐÃ VÁ THẬT** với dạng gốc, **VÁ MỘT PHẦN** theo F1. C2 **ĐÃ VÁ THẬT**. | Chốt nhãn nhiều cấp trước số đơn; ký hiệu lạ chỉ ảnh hưởng khi run còn hiệu lực. |
| [27](../ops/acceptance/llm-khoan-docx/r1/review-27-codex/VERDICT.md) | D1 **ĐÃ VÁ THẬT** với các dạng gốc, **VÁ MỘT PHẦN** lớp. | Các mutant nối nhiều dấu, số/chữ và đối chứng mã hạng, viết tắt vẫn qua harness. |
| [28](../ops/acceptance/llm-khoan-docx/r1/review-28-codex/VERDICT.md) | E1 **ĐÃ VÁ THẬT** với các dạng gốc, **VÁ MỘT PHẦN** lớp. | Hai mutant tiền tố chết đúng ca; F1 nằm ở hậu tố của nhãn sau số đơn. |

Với #1514, các biểu hiện A1/A2/D3/E2/F2 về câu dẫn, C1 về tiêu đề dính thân, A3/C2/D1/E1/F1 về dấu kết và đánh số nội dòng, A4 về fixture, G1/H1/J1/K1 về ghép dòng điểm được đối chiếu qua các chốt trên và bộ ca lịch sử. Các giới hạn của D2 và C2 đã khai trong hợp đồng thô. B1 lượt 1 của #1514 về bề mặt đã được giải quyết cho run hiện hành. [Ca lịch sử](../scripts/tl_core/llm_route_test.py#L1073) · [Lịch sử #1514](../ops/acceptance/llm-ranh-gioi-khoan/r1/review-10-codex/VERDICT.md)

## Findings

### F1 [P2] Số khoản nhận trước nhãn điểm có dấu ở cuối — `scripts/tl_core/llm_route.py:1432`

**Kịch bản.** Cấp con dùng nhãn có một placeholder thập phân và hai dấu chấm liền sau số. Cách định dạng này thuộc miền `lvlText` hiện tại. Bản văn bản thô giữ nhãn điểm nhưng mất dấu thụt lề và cấp danh sách. Nếu số trên nhãn điểm trùng số khoản kế, dòng điểm có đủ hai vế và các dòng khác thỏa chốt một dòng, bộ quét có thể dựng thêm một khoản từ điểm đó.

**Căn cứ.** `_nhan` chấp nhận nhiều dấu ở cuối nhãn. `_RE_NHIEU_CAP` kiểm trước nhưng cần thành phần nhãn thứ hai; phần thân mở bằng một từ thông thường không cung cấp thành phần đó. `_RE_SO_KHOAN` nhận số và dấu chấm thứ nhất, để dấu còn lại trong thân rồi chạy nhánh khoản trước `_RE_DIEM`. Kiểm ngoặc, dấu kết và số nội dòng cho phép dấu chấm còn lại; dãy liên tục cũng có thể đạt. Nếu model chép đúng hai vế của phân đoạn sai, phép so có thể trả `ok=true` và ghi `--out`. Mâu thuẫn nằm trong bộ tách thô sau khi đọc nguồn, kể cả `--tep` văn bản. [Bộ dựng](../scripts/tl_core/llm_route.py#L978) · [Nhận số](../scripts/tl_core/llm_route.py#L491) · [Thứ tự chốt](../scripts/tl_core/llm_route.py#L1432) · [Phép so](../scripts/tl_core/llm_route.py#L1567)

**Hạng P2 và đề xuất.** Cùng lớp và mức ảnh hưởng với K1/E1 trên văn bản mất cấu trúc. Nhận sai cần nhãn trùng số kế, bố cục qua các chốt còn lại và kết quả model khớp phân đoạn đó; cờ duyệt ranh giới vẫn xuất hiện. Đối chiếu miền nhãn dựng được với miền từ chối trước nhánh khoản đơn, gồm các chuỗi dấu ở mọi vị trí và cả nhãn một placeholder. Với phần giao còn nhập nhằng với khoản thật, chốt miền hỗ trợ và ca đối chứng trên cả hai dạng nguồn. [E1 lượt 28](../ops/acceptance/llm-khoan-docx/r1/review-28-codex/VERDICT.md#L68) · [ADR-0060 M1–M2](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32)

### F2 [P1] Tham chiếu style đoạn bị đứt có thể làm lọt chữ gạch bỏ trong DOCX — `scripts/tl_core/llm_route.py:1089`

**Kịch bản.** Tệp có một paragraph style mặc định đặt gạch ngang. Một đoạn đánh số trực tiếp giữ tham chiếu tới style đoạn đã vắng trong part styles, chẳng hạn sau khi chuyển tài liệu giữa các mẫu. Khi Word bỏ qua tham chiếu không phân giải được, style đoạn mặc định áp dụng. Bộ đọc lại xử lý run như thể thiếu cả định dạng gạch từ style mặc định.

**Căn cứ.** `_doc_kieu` đã lưu ID style đoạn mặc định. `_phan_tich_doan` chỉ dùng ID ấy nếu phần tử `pStyle` vắng. Khi phần tử có mặt mà ID không tồn tại, `_dem_bat_trong_chuoi` thoát ngay, đóng góp 0 tầng gạch. `_theo_kieu` cũng xem tham chiếu đó như hết chuỗi. Đoạn vẫn có thể qua các chốt nhờ số trực tiếp hợp lệ và chữ phù hợp. Chữ gạch do style mặc định bị đưa vào văn bản gửi model lẫn nguồn của phép so. Đây là đường `--tep .docx`, ngoài ngoại lệ của bộ đọc số hiệu. [Lưu style mặc định](../scripts/tl_core/llm_route.py#L912) · [Tra chuỗi](../scripts/tl_core/llm_route.py#L927) · [Chọn style](../scripts/tl_core/llm_route.py#L1087) · [Lọc gạch](../scripts/tl_core/llm_route.py#L1146)

**Hạng P1 và đề xuất.** Phép kiểm cấu trúc có thể xác nhận và xuất chữ đã bỏ của dự thảo. Cờ duyệt ranh giới không phát hiện chữ sai khi cả model và bộ so dùng một bản đã trích sai. Xử lý tham chiếu paragraph style không phân giải được tại chỗ chọn style hiệu lực, bằng fallback đã xác minh hoặc từ chối có chẩn đoán. Phép đo đóng lớp cần đối chiếu style mặc định với trường hợp vắng style và trường hợp ID không phân giải, giữ riêng gạch đơn và gạch kép. [A4 lượt 1](../ops/acceptance/llm-khoan-docx/r1/review-1-codex/VERDICT.md#L50) · [Protocol §8.3](../docs/PROTOCOL_DA_PHIEN.md#L812)

| Lớp | Lịch sử | Trạng thái và cách kiểm đóng |
| --- | --- | --- |
| `ranh-gioi-khoan` | K1 #1514 → V4/W4/X3/Y3/Z3/A2 lượt 24/B1/C1/D1 → E1 lượt 28 → F1 | **VÁ MỘT PHẦN**, 1 biểu hiện P2 mở. Đối chiếu miền nhãn trước nhận số đơn với miền nhãn dựng từ `lvlText`; ca nguồn có số và mất số, đối chứng khoản hợp lệ. |
| `docx-markup-du-thao` | A4 lượt 1 → B3/C4/E2 → F2. Lịch sử lớp dùng cùng slug từ lượt 1. | 1 biểu hiện P1 mở ở bước chọn style hiệu lực. Các biểu hiện giữ/mất khoảng trắng W2/X1/Y1/Z1/A1 lượt 24/B3/C2 đã đo trên bộ ca sẵn có. Phép kiểm cho F2 đi qua tra style và lọc, trước bước ghép khoảng trắng. |
| `docx-so-hien-thi` | A2/B2/G1/J1/V2/W5/X2/Y2/Z2 | Đã đóng các biểu hiện số đã báo trong miền đo. Kiểm start/override, reset, nhiều numId, định nghĩa lỗi dùng và không dùng. |
| `docx-test-doc-lap` | A7/B7/C6/D4/E5/F5/G5/H3/J4/Z4/B2 | Các mutant đích lịch sử vào nhánh kill. Phép đo đầu-cuối còn thiếu được ghi theo F1/F2. |

Có hai lớp mở và hai biểu hiện. Với phân đoạn đúng, cách so hiện tại bắt model tự bỏ, gộp, cắt hoặc tráo khoản. Hai nhánh ghép dòng của K1 đã bị bỏ. Nguồn thô mất mọi nhãn vẫn có thể đánh đồng hai dòng đã mất cấu trúc với hai khoản hoàn chỉnh nếu mỗi dòng tự có hai vế và dấu kết. Tiểu mục còn số nhưng mất cấp có thể trùng số khoản kế. Đây là giới hạn cùng hình dạng thô đã ghi ở verdict K1 và ở `pham_vi_kiem`; F1 là một trường hợp cụ thể nằm trong miền nhãn có dấu mà r29 cam kết nhận diện. [Giới hạn K1](../ops/acceptance/llm-ranh-gioi-khoan/r1/review-10-codex/VERDICT.md#L48) · [Phạm vi thô](../scripts/tl_core/llm_route.py#L1400)

Danh sách cho phép đã có các mốc bookmark/comment/permission, content control, hyperlink, tab và dấu nối không ngắt. Field, hình, chú thích, markup tương thích, bảng và đánh số qua style đã nêu trong hợp đồng hoặc hướng dẫn. Ca hiện có chưa xác lập phần tử Word/Google Docs phổ biến nào khác gây chặn oan ngoài danh sách giới hạn. [Danh sách phần tử](../scripts/tl_core/llm_route.py#L647) · [Hướng dẫn](../docs/GOI_AGENT_DA_NEN.md#L389)

## Kết quả test và đột biến

Linux x86_64, Python 3.13.18, Git 2.43.0, Codex CLI 0.172.0. Các phép Python tắt bytecode. `core.abbrev=7` trên checkout được giao và hai bản sao detached trong scratch. Base có tree `0cc14e79cecd2ce44bc4dc6cff92cadb31fd7ee4`. Log và mã thoát lưu tại `/tmp/wp1525-r29-review.KGawB3lj/`.

| Lệnh | Trạng thái | Mã thoát và bằng chứng |
| --- | --- | --- |
| `python scripts/tl_core/llm_route_test.py` | `passed` | rc 0, **63/63** ca, **252/252** đột biến chết. `route.log`. |
| `python scripts/tl.py --deterministic workflow-audit --strict --json` | `passed` | rc 0, `ok=true`, 194 lệnh, 26 card, 11 nhóm, 60 task, 0 lỗi, 0 cảnh báo. `audit.log`. |
| `python scripts/tl.py --deterministic golden-test --json` | `passed` | rc 0, `ok=true`, **20/20** khớp fixture, **20/20** bản chiếu ổn định, **19/20** byte thô ổn định. Biến động của `hygiene_sweep_fixture` ở trường đã khai `snapshot_age_s`. `golden.log`. |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | `passed` trên bản sao head sạch | rc 0, `ok=true`, **187/187** tệp, sai/thiếu/thừa đều 0, package hash khớp `999c9fac62eac8df8effd07240e767ac87aa1bb9720f12d6f4880eb66ef2e07b`. Lượt đầu ở checkout giao review rc 2 vì kiểm kê thêm chính `.review/VERDICT.md`; chạy lại cùng SHA/tree trong bản sao sạch. `release.log`, `clean-release.log`. |
| `python ops/lease_publish.py check --root . ops/leases/llm-khoan-docx-r29-g1-claude.yaml` | `passed` cục bộ | rc 0, “ĐĂNG ĐƯỢC”, #1525, neo `64b7f2c14776`, hết hạn 20:52 UTC. `lease.log`. |
| `python scripts/tl.py --deterministic determinism-audit --strict --json` | `passed` | rc 0, `ok=true`, **15/15** chốt. `determinism.log`. |
| `python scripts/tl.py --deterministic doc-claims-check --strict --json` · head/base | `failed` ở cả hai | rc 2 mỗi bản, cùng cờ cứng `SHA_NOT_A_COMMIT` cho `9941d8af52aeede1c78ea4e232fbe9a8d5272033` tại protocol dòng 1680, object vắng trong checkout shallow. Head có 410 advisory. `doc-claims.log`, `base-doc-claims.log`. |
| `ruff check --no-cache --select F --output-format json scripts/tl.py` · head/base | `failed` cho lint, tiêu chí delta đạt | Ruff 0.16.9, rc 1 mỗi bản, cùng 12 F821, 0 F401. Nội dung chẩn đoán khớp sau bỏ tiền tố checkout. `ruff-head.log`, `ruff-base.log`. |
| `loi_ruff_ci()` qua `runpy.run_path` với `.claude/dev/ci_dang_ky_test.py` | `passed` | rc 0, `RUFF_CONTRACT 3 []` kiểm hợp đồng pin/probe trong workflow. `ruff-contract.log`. |
| `git diff --check 599b90c HEAD` và `git diff --check fcb12b3 HEAD` | `passed` | Cả hai rc 0. Phép tương ứng với base toàn PR rc 2 cho ba dòng ngắt Markdown bằng khoảng trắng của verdict #1514 lượt 8. |

Harness gốc tạo đột biến trong thư mục tạm. Lượt đo lại bằng `python -B -m pdb scripts/tl_core/llm_route_test.py` đặt breakpoint tại dòng 2261 với điều kiện `ten.startswith("wp1525_")`. Harness và debugger cùng rc 0, **155/155** mutant `wp1525_*` vào nhánh `TinHieuChotCa` của ca đích. [Harness](../scripts/tl_core/llm_route_test.py#L2241) · [Bảng đột biến](../scripts/tl_core/llm_route_test.py#L1929)

| Mutant có sẵn | Tín hiệu ca đích trong `target-mutants.log` |
| --- | --- |
| `wp1525_tien_to_chi_ngoac` | `ca_khoan_mat_so_co_diem_dat`: chốt r29 bỏ lọt dạng nhãn nhiều cấp có dấu chấm đứng đầu của fixture. |
| `wp1525_bo_nhan_dau_dau` | Cùng ca: bỏ lọt dạng nhãn một số có dấu chấm đứng đầu của fixture. |
| `wp1525_tho_nhan_diem` | `ca_wp1514_luot9`: bộ tách nhận các dòng điểm thông thường thành mục trong nguồn mất số. |
| `wp1525_khong_dat_lai_cap_con` | `ca_cau_truc_docx_dat`: nhãn điểm ở khoản kế chạy tiếp tới c thay vì bắt đầu lại. |
| `wp1525_bo_qua_start_override` | `ca_cau_truc_docx_dat`: ca hợp lệ bị từ chối vì số khoản bắt đầu 5 thay vì 1. |

Selftest trên head và đối chứng base:

| Lệnh | Trạng thái | Mã thoát và bằng chứng |
| --- | --- | --- |
| `python scripts/tl.py --selftest` · head | `failed` | rc 1, **1774/1790**, transport **12/12**. `r1525_llm_khai_niem_tep_docx_cau_truc` đạt. Lượt chạy ở checkout giao review và lượt chạy trên bản sao head sạch có cùng 16 ID lỗi. `selftest.log`, `head-selftest.log`. |
| Cùng lệnh · base | `failed` | rc 1, **1773/1789**, transport **12/12**, cùng 16 ID lỗi. `base-selftest.log`. |

`cmp head-selftest.fail-ids base-selftest.fail-ids` rc 0. Có 14 ca thuộc nhóm `/tmp/.git` rỗng trong prompt (8 `r973_bootstrap_*`, 5 `wp433_*`, 1 `wp727_tl_gws_refresh`). Hai ca còn lại cũng đỏ ở base, `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` và `r268_l2_trichotomy_theo_trang_thai_object`. Delta ID lỗi bằng 0. SHA-256 log head `1cbef7d35730a7dca6132413059efc909ff5279f633657917a4d9663d110722b`, base `1fb08ad829494f6e24731582fe1d7cff1372478a7302ec4a57428b2f937a3acb`, mutant đích `ab2743a355a1be3d200993551841ac49cc047b353d8771601c11716f7cb2958d`.

## Không đo được

- F1 và F2 được xác lập qua đọc mã. Chưa đo đầu-cuối cho hai kịch bản hoặc tần suất xuất hiện của chúng trong bản Word/Google Docs thực tế. Repo không có DOCX được Git theo dõi; phép chạy dùng fixture sẵn có.
- `skipped` ở cấp sáu lệnh trong prompt là 0. `not_run` gồm Windows bản địa, CI, hai phép kiểm GitHub của lease, model thật và LIVE. M3 yêu cầu Windows vì diff toàn PR sửa dòng `encoding=` trong mã Python. Bằng chứng Windows trên exact head còn thiếu. [ADR-0060 M3](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L43)
- Metadata launcher đang chạy chưa có mã thoát con, hash stdout và marker terminal. Phạm vi quan sát trạng thái nhánh là refs và objects cục bộ.
- Gate ban đầu tạo hai thư mục ignored chứa fixture và trạng thái test. Đã chuyển chúng vào `checkout-test-artifacts/` trong scratch. HEAD/tree đầu và cuối khớp. `git diff --exit-code` và `git diff --cached --exit-code` đều rc 0. Snapshot cuối ghi `.codex/` đã có từ đầu và `.review/VERDICT.md` là đường dẫn mới duy nhất. Snapshot chỉ chứng minh chênh lệch quan sát được giữa hai mốc.

Có **0 P0, 1 P1, 1 P2 và 0 P3** mở. F2 dẫn tới yêu cầu sửa theo ngưỡng nội dung của prompt. Cả F1 lẫn F2 đều chặn merge theo ADR-0060 M1. Nghiệm thu §5 còn thiếu selftest N/N và doc-claims strict đạt trên exact head, với delta nền bằng 0 ở hai phép đo này. [ADR-0060](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32) · [ADR-0062](../docs/adr/0062-adr-0060-mac-dinh-va-dong-bang-adr-0054.md#L12)

P2_mo: 1
VERDICT: REQUEST_CHANGES
