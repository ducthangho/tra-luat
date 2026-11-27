# Verdict packet #1525 r34 lượt 34 — Codex
reviewed_sha: a3ef89a344d4483f30ea4be898fb397fd5358553
tree: 9c3649ff1ae92ce17ef578fc7ffe875b10f2c35b
VERDICT: APPROVE

## Preflight

- Checkout rời của `ducthangho/tra-luat`, detached tại đúng ứng viên nhánh `ccr-89c0d2e2-inanqb`. Base nghiệm thu `64b7f2c14776d5d0e1d34a6be4725490956f5bec`, tree `0cc14e79cecd2ce44bc4dc6cff92cadb31fd7ee4`. `git merge-base` trả đúng base. Mốc nối #1514 `fcb12b3873c3bec2c339029136243ed2c804ce05`, mốc bản vá `7042aa14f705e6d3b2b21315a530c48d0862918c`.
- Nguồn đặc tả là blob `b0a31d2ab835cc19fd8df3b9a1ea324c83da502a` tại exact head. SHA-256 `5e1a03d77ccf6609a310fdfccee81025a66c16497dbe596d9db5cf96bb158ed6` khớp bản cục bộ và lease #1525 r34/g1. Review Class khai báo và hiệu lực đều là `sensitive`. Lease hết hạn 22:29 UTC, 26-11-2026. Dòng đầu prompt và §5 của đặc tả ghi trần 34. Lease tại `a3ef89a` ghi trần 35 cho lần chạy lại lượt 34 theo chỉ thị chủ kho, sau 33 lời gọi trước lượt và một lần chạy dở `e535bd34`. Review này dựa vào lease đã cập nhật tại exact head. [Đặc tả r34](../ops/specs/llm-khoan-docx-r34.md) · [Lease r34](../ops/leases/llm-khoan-docx-r34-g1-claude.yaml)
- Write set có 181 path, SHA-256 tính lại `71b055774fbfe1d011bc5610866f67a61eaacb44eda4ec79a6ebeaf3feed5ba0`. Diff bản vá khớp 8/8. Diff packet khớp 177/177 sau khi trừ bốn hồ sơ #1514 được prompt loại. Toàn PR có 225 path, 48 path ngoài lease r34 thuộc hồ sơ/spec/lease #1514. SHA-256 của `git diff --binary <mốc> HEAD` theo thứ tự bản vá, packet, PR là `d6dc9216da8fc858ebdfb82365a803318d7c484138efe7f5c53f8b7347f5d042`, `7b53b2417aba1c79869892cab8241bdc330923bd565785a91e096695bc909e76`, `7e51ca858b6e02f7aa3166a4d3f52313a0dcb9b77f5c549255e3baa0c7d16fd6`. Bia mộ kiểm đúng 34/34 cặp hai chiều từ #1514 r9 đến #1525 r34. Hash đặc tả và bytes lease đối chiếu Git/đĩa đúng 35/35.
- Executor `anthropic_claude / claude_code / machine/local` theo lease, phiên ghi quyền `session_015GtxrZQYT3Vt8PJdXrjEKg`. Reviewer `openai_codex / codex_cli / machine` theo launcher run `dbfdd78c1c3b49c18eafd7960819cb1c` trong context và checkout riêng. SHA-256 prompt snapshot `cd886bc8af252c7ba3e1dc4b078bce1288b6b7372544a230ab27889a829d589b` và checkpoint `5018cbaff72521904d80dee29a7a4db2bcee86f1332b2a948a885601884ef4ca` khớp run. Sandbox `workspace-write`, mạng bị giới hạn, dùng bản sao cục bộ ngoài checkout để chạy gate. Model và effort phục vụ `KHONG_DO_DUOC` từ metadata launcher đã cấp. Phiên ghi verdict chưa thể quan sát mã thoát terminal và hash stdout của chính launcher trước khi kết thúc.

## Đối chiếu lượt 33 và đặc tả r34

| Mục | Trạng thái | Bằng chứng |
| --- | --- | --- |
| J1 lượt 33 · §2.36 | **VÁ MỘT PHẦN** | Dải chữ có dấu kết `.` hoặc `)` đi qua nhánh mới dù có đệm hay dính số. Ca sẵn có giữ đối chứng `1. A là …`, `1. e-mail là …`, thân ASCII và cụm ngoặc. Nhóm nhãn còn lọt được ghi ở lớp `ranh-gioi-khoan`. |
| J2 lượt 33 · §2.36 | **ĐÃ VÁ THẬT** với cách quay lui cấp số nhân đã báo | Một lớp ký tự phẳng thay lặp lồng trên dải chữ. Dấu, chữ và đệm là các tập rời ở ranh giới của nhánh mới. Ca có sẵn với dải 4.001 chữ và thiếu dấu kết chạy dưới ngưỡng 2 giây của harness. Lớp tài nguyên còn các biểu hiện độc lập trong tuyến đọc. |
| §1, §2.2–§2.3, §2.19–§2.23 · K1 #1514 | **ĐÃ VÁ THẬT** với hai đường ghép gốc | Dòng điểm nhận dạng được làm `tach_khoan` trả `None`. Dòng tiếp mở “là” trong nguồn có số rơi vào nhánh từ chối dòng không số. Bản mất số tách theo dòng và vế thuật ngữ rỗng bị loại khi so. Fixture Điều 3 Luật 134/2025/QH15 và ba kết quả lưu được kiểm 8/8 trong suite. `goi`, `duong_api`, `duong_sub`, `_chay_co_moc` và CLI không đổi trong bản vá r34. Kết quả vẫn gắn cờ duyệt và dùng đúng phạm vi theo nguồn. |
| §2.1, §2.4–§2.18 · vị trí Điều, điểm gõ tay, câu dẫn | **ĐÃ VÁ THẬT** ở các chốt hiện hành cho biểu hiện đã báo. Cắt vùng, đếm trong bảng và tiếp nhận điểm gõ tay **HẾT ĐỐI TƯỢNG** theo r7 | Tiêu đề nguyên đoạn khớp Điều được yêu cầu, đứng đầu phần có nội dung, không đánh số và không ngắt mềm. Đọc tới hết tệp, chặn bảng/khối lạ và tiền tố Điều/Chương/Mục/Phần trong vùng. Sau khoản đầu mọi đoạn có chữ mà thiếu đánh số đều bị chặn. Trước khoản đầu nhận tối đa một câu dẫn khớp toàn mẫu. Kiểm trước tiêu đề còn khe ký tự ngoài miền tại lớp `ranh-gioi-ky-tu`. |
| §2.1, §2.4–§2.18, §2.22–§2.26 · số Word | **ĐÃ VÁ THẬT** với các biểu hiện lịch sử của miền hỗ trợ | `start` vắng mặc định 0. `startOverride` thay gốc của cấp, ca có gốc 5 và override 1. Đếm riêng theo `numId`, đặt lại cấp con khi cấp cha tăng. Kiểm cha đã xuất hiện, thuộc tính đơn trị, ID chuẩn hóa, cấp 0–8, số ≤999 và danh sách lỗi khi dùng. Khoản phải cùng danh sách, `decimal`, nhãn của chính cấp và dãy từ 1. Ca dương đo nhãn chữ sau Z và reset ở khoản kế. |
| §2.5–§2.13, §2.23–§2.29, §2.32–§2.35 · chữ còn hiệu lực và style | **ĐÃ VÁ THẬT** với các biểu hiện đã báo trong miền kiểm | Đọc XML gốc, chặn sửa dấu đoạn, lọc gạch đơn/kép, `del` và `moveFrom`, giữ chữ chèn/chuyển tới. Tính gạch trực tiếp sau các tầng style và phân giải trên ID đúng loại. `_chu_t` dùng `xml:space` hiệu lực cho chữ thường, chữ xóa lạc và ruột bị bỏ; chỉ giữ mẩu trắng. Cờ phần tử lạ và ngắt của run bị bỏ đi theo run đó. `_tu_noi` nhận chữ của đoạn mở khoản cấu trúc; kết quả phải khớp cả hai vế, thứ tự và số lượng theo các khoản đã đọc. |
| §2.7 D1, §2.9, §2.21 U2, §2.22 V3, §2.23 W1–W3 | **ĐẠT** theo hợp đồng hiện hành | `KhongCauTruc` đã bỏ. DOCX không có đánh số tự động trả rc 2 qua `ValueError`. Đường số hiệu gọi `tl extract --markup-strict`; giữ nguyên các giới hạn đã được duyệt đối với bộ đọc chung và đường văn bản thô. |
| §3 và §5 · bộ đo | **ĐẠT** ca và đột biến sẵn có. Gate đầy đủ xem bảng kết quả | Các mutant được tính khi neo xuất hiện đúng một lần và ca đích ném `TinHieuChotCa`. Ca CLI dùng model giả kiểm rc 0/5/2. Bộ đột biến r34 thay trực tiếp nhánh dải chữ, đệm, dấu gạch và số–số; phép đo thời gian J2 có sẵn là ca dương. |

[Mã tách và so](../scripts/tl_core/llm_route.py#L1412) · [Chọn vùng và ghép](../scripts/tl_core/llm_route.py#L1322) · [Bộ đếm](../scripts/tl_core/llm_route.py#L1305) · [CLI](../scripts/tl_core/ops_misc.py#L3017) · [Suite](../scripts/tl_core/llm_route_test.py) · [Lượt 33](../ops/acceptance/llm-khoan-docx/r1/review-33-codex/VERDICT.md)

### Đối chiếu lịch sử

Mỗi dòng dưới đây giữ ID tại lượt nguồn. Trạng thái áp cho biểu hiện gốc và phạm vi đã đo. Trạng thái lớp hiện tại nằm trong phần Findings.

| Lượt và SHA nguồn | Đối chiếu trên r34 |
| --- | --- |
| 1 · `3d24751` | A1 chốt tiêu đề/bảng/khối, A2–A4, A5 phạm vi định nghĩa chưa dùng, A7–A8 đã vá. A1 phần cắt, A5 phần nội dung ngoài Điều và A6 hết đối tượng theo r7. |
| 2 · `38c481f` | B1 phần kiểm nguyên đoạn, B2 phần số và style, B3–B8 đã vá. Cắt vùng của B1 và duyệt bảng của B2 hết đối tượng theo r7. |
| 3 · `b0f3cb9` | C1 phần ngắt tiêu đề, C2 phần nhãn sau Z, C3–C7 đã vá. C1 cắt vùng và C2 đếm trong bảng hết đối tượng. |
| 4 · `fa3a8e2` | D1 quy tắc cắt và lùi thô hết đối tượng. D2–D4 và D6 đã vá. D5 có chẩn đoán và giới hạn Strict đã khai. |
| 5 · `3c1e143` | E2/E5/E6 đã vá. E1/E3/E4 hết đối tượng vì r7 bỏ điểm cắt và chặn toàn bộ bảng. |
| 6 · `6781d11` | F1 hết đối tượng. F2 đóng bằng chặn đoạn không số. F3/F4/F6 đã vá, F5 khóa riêng override và kiểm cấp đoạn qua định nghĩa đã xác thực. |
| 7 · `4badb3d` | G1/G2/G4–G6 đã vá. G3 hết đối tượng vì chặn nhảy cấp trước khi dựng nhãn tổ tiên. |
| 8 · `6d28f34` | H1–H5 đã vá. H5 chỉ tính chữ hiệu lực sau ngắt. |
| 9 · `4c647c8` | J1–J5 đã vá. Chốt J2 kiểm phần tử `mc:` toàn part. |
| 10 · `674a28c` | K1–K4 của #1525 đã vá. |
| 11 · `e1ed11f` | L1–L6 đã vá. Chốt tiền tố r14 bao hình dạng L2. |
| 12 · `f305663` | M1 đã vá theo chốt tiền tố. M2 đã vá theo kiểm kiểu và giá trị vắng. |
| 13 · `069b734` | N1/N2/N3 đã vá ở tiền tố, ID dài và QName. |
| 14 · `0447395` | Q1/Q2 đã vá bằng kiểm ký tự gốc và giữ nguyên chữ nguồn khi gặp dẫn chiếu. |
| 15 · `b5cff42` | R1–R3 đã vá cho các biểu hiện gốc. Phạm vi trước tiêu đề có biểu hiện mới được ghi ở lớp ký tự. |
| 16 · `7a913aa` | S1–S3 đã vá ở biểu hiện gốc. S2 và lớp ký tự chưa đóng toàn miền. |
| 17 · `8f31901` | T1/T2 đã vá cho phần thuộc packet. Hành vi bộ đọc chung nằm trong giới hạn U2. |
| 18 · `5ed4386` | U1 đã vá với miền chữ số ASCII. U2 là giới hạn số hiệu có quyết định chủ kho. |
| 19 · `7c4abd7` | V1/V2 và ca nhãn V4 đã vá. V3 là giới hạn có quyết định chủ kho. |
| 20 · `8a685fe` | W2 DOCX và W4/W5 đã vá ở các ca gốc. W1/W3 và W2 số hiệu là giới hạn có quyết định chủ kho. |
| 21 · `3d21bd1` | X1–X3 đã vá ở các ca gốc. |
| 22 · `fbddd47` | Y1–Y3 đã vá ở các ca gốc. I1 đóng thêm miền tra cứu khóa style của Y2. |
| 23 · `30e3e07` | Z1–Z4 đã vá ở các ca gốc. |
| 24 · `b755fef` | A1/A2 đã vá ở các ca gốc. |
| 25 · `659d9f2` | B1–B3 đã vá ở các ca gốc. Miền nhãn B1 vẫn hở theo lớp ranh giới. |
| 26 · `475fee9` | C1/C2 đã vá ở các ca gốc. C1 vẫn hở theo lớp ranh giới. |
| 27 · `9972282` | D1 đã vá ở ca gốc. Miền nhãn D1 vẫn hở theo lớp ranh giới. |
| 28 · `0e1c112` | E1 đã vá ở ca gốc. Miền nhãn E1 vẫn hở theo lớp ranh giới. |
| 29 · `291919e` | F1/F2 đã vá ở ca gốc. Miền nhãn F1 vẫn hở theo lớp ranh giới. |
| 30 · `749e6ac` | G1/G2 đã vá ở ca gốc. Miền nhãn G2 vẫn hở theo lớp ranh giới. |
| 31 · `7e9cde7` | H1–H3 đã vá ở ca gốc. Miền nhãn H2 vẫn hở theo lớp ranh giới. |
| 32 · `571e83f` | I1 đã vá. I2 vá một phần, các vị trí dấu còn hở được ghi cùng J1. Cơ chế backtracking sinh ở I2 được thay tại r34. |
| 33 · `3278bfe` | J1 vá một phần, J2 đóng ở biểu hiện quay lui cấp số nhân. |

Nguồn #1514 r9, review 10 trên `fcb12b3`. Các chốt tiêu đề/câu dẫn (C1, A1/A2/D3/E2/F2), dấu kết và số nội dòng (A3/C2/D1/E1/F1), ghép dòng (G1/H1/J1/K1) và so chữ/khoảng dòng (X2–X4) vẫn có trên r34. A4 giữ ba đầu ra lưu 8/8, B1 kiểm theo bề mặt launcher. D2 và ngoại lệ của C2 nằm trong giới hạn #1514. [Hồ sơ lượt 1–33](../ops/acceptance/llm-khoan-docx/r1) · [Lượt 10 #1514](../ops/acceptance/llm-ranh-gioi-khoan/r1/review-10-codex/VERDICT.md) · [Đặc tả #1514 r9](../ops/specs/llm-ranh-gioi-khoan-r9.md)

## Findings THEO LỚP

Các hint dưới đây là mã giả và mô tả ca để Executor tái dẫn xuất. Các biểu hiện mới được suy ra từ mã. Bảng đột biến sẵn có chỉ chứng minh các ca đã nêu trong phần kết quả.

### Lớp `ranh-gioi-khoan` [P2] — `scripts/tl_core/llm_route.py:526,540,1460`

- **Bất biến.** Trước khi tách số khoản hoặc nhận một dòng mất số làm khoản, phải từ chối mọi dòng còn nhận dạng được là nhãn điểm trong miền dấu và placeholder đã công bố.
- **Miền.** Cả `--tep` UTF-8 và chữ do `extract` trả dùng một bộ tách. Miền gồm dấu đầu/cuối và đệm ngang, placeholder số hoặc chữ, các thành phần dính nhau hoặc nối bởi dấu/khoảng đệm, nhãn thập phân nhiều cấp và bullet. R34 bao nhóm số–dải chữ kết bằng chấm, ngoặc đóng hoặc gạch có khoảng trắng. Còn ba hình dạng cùng cơ chế:
  1. Dải chữ sau số, kết bằng gạch sát ngoặc kép hợp lệ hoặc ngoặc tròn mở thân. Hậu tố này thuộc miền gạch của §2.28 B1. Nhánh r34 chỉ nhìn khoảng trắng sau gạch. Nhánh chữ lặp riêng cũng trượt khi dải gồm các chữ khác nhau. Khi số đầu có chấm/ngoặc đóng và khớp số kế tiếp, `_RE_SO_KHOAN` ăn số trước khi xét `_RE_DIEM`; phần còn lại của nhãn vào thuật ngữ. Dấu phân cách có thể cân bằng và từ nối nằm ngoài ngoặc, nên phép so chấp nhận đầu ra chép đúng phân đoạn sai.
  2. Ngoặc mở ở vị trí cuối nhãn số–chữ từng được nhận trong các nhánh r33. R34 bỏ nó khỏi điều kiện kết. Chốt cân ngoặc có thể chặn một số dòng, nhưng sau khi gỡ số khoản, dấu mở có thể khép trong thân. Cần quyết định chung về dấu mở của nhãn và dấu mở thân, kể cả dạng dính và có đệm.
  3. Dải chữ ghép từ nhiều placeholder trước dấu hoặc trước chữ số dính, kể cả nhãn không bắt đầu bằng số. `_nhan` dựng được dải ghép. Phía thô chỉ nhận dải chữ phẳng trong nhánh mở bằng số; các nhánh mở bằng chữ chỉ cho một chữ lặp đứng riêng. Nếu đầu dòng không được nhận dạng và toàn nguồn mất số, dòng đi nguyên vẹn vào khoản. Nếu có phần số mở khoản hợp lệ ở đầu, nhánh số có thể nhận một tiền tố của nhãn.
- **Hint patch.** Dùng một phép quét đầu dòng và một bảng dấu dùng chung với ngữ pháp nhãn của `_nhan`. Mã giả sát luồng hiện tại:

  ```text
  tach_khoan:
      cho mỗi dòng:
          ket_qua = quet_nhan_dau_dong(dòng)
          nếu ket_qua.la_diem_hoac_nhieu_thanh_phan: trả None
          nếu ket_qua.la_so_khoan_don: lưu số đã đọc và vị trí bắt đầu thân
          kiểm dấu phân cách của phần còn lại theo đúng vai trò vừa xác định
      kiểm câu dẫn, số liên tục, dấu kết và số nội dòng như hiện hành
  ```

  Bộ quét đọc tối đa từng dải số/chữ/đệm, giữ vị trí dấu đầu–giữa–cuối và phân loại dấu kết cùng ký tự đầu thân. Dấu gạch trước khoảng trắng và trước dấu mở thân dùng chung quyết định. Phân loại nhãn diễn ra trước số khoản đơn, nên đường có số và mất số dùng chung kết quả. Dải chữ ghép có dấu được nhận từ mọi vị trí placeholder cho phép. Bảng ngoại lệ giữ các đối chứng đã duyệt về chữ đầu thân, từ ghép, mã hạng và cụm ngoặc. [Chỗ dựng nhãn](../scripts/tl_core/llm_route.py#L982) · [Nhận nhãn thô](../scripts/tl_core/llm_route.py#L526) · [Chọn nhánh](../scripts/tl_core/llm_route.py#L1460) · [§2.28–§2.36](../ops/specs/llm-khoan-docx-r34.md#L339)
- **Hint test.** Xét song song nguồn có số và mất số, chạy bảng hình dạng theo vị trí dấu, loại placeholder, đệm, phần tử ghép và ký tự đầu thân. Đối chứng dương gồm các thân được duyệt ở r31/r34, fixture 8 khoản và đường DOCX giữ cấp con. Ca âm phải kiểm `tach_khoan` trả `None` và kết quả so không được xác minh. Đột biến đảo ưu tiên số khoản/nhãn, hoặc bỏ phân loại chung dấu kết, phải bị ca tương ứng bắt.
- **Vùng giao.** Hình dạng nguồn thô có thể làm mất cấp dù từng dòng riêng vẫn hợp lệ. Câu khai nếu cần sửa ranh giới miền là “Dấu mở của thân và dấu mở kết thúc nhãn chỉ được phân biệt khi còn ranh giới nhìn thấy giữa nhãn và thân; dạng trùng với một khoản hợp lệ và nhãn nhiều placeholder dính nhau mà không có dấu phân biệt thuộc bước duyệt ranh giới.” Hai trường hợp đã khai gồm dải chữ thiếu dấu kết và nhãn chỉ ngăn bằng khoảng trắng.
- **Lịch sử và hạng.** K1 #1514, V4/W4/X3/Y3/Z3, A2/B1/C1/D1/E1/F1, G2/H2/I2 → J1. P2 theo K1/J1. Để đầu ra sai vượt kiểm cần đúng bố cục mơ hồ, dấu và từ nối hợp lệ, số liên tục nếu còn số, cùng đầu ra khớp phân đoạn thô có cờ duyệt. Cơ chế ghép điểm mà K1 từng báo đã bị loại; lớp phân loại nhãn còn mở.

### Lớp `can-tai-nguyen-doc-nguon` [P2] — `scripts/tl_core/llm_route.py:1047,1467,1498`

- **Bất biến.** Chi phí đọc và tách nguồn bị giới hạn theo kích thước/cấu trúc được hỗ trợ. Vượt miền phải đi ra bằng lỗi nguồn có kiểm soát.
- **Miền.** J2 đã mất cơ chế quay lui cấp số nhân ở nhánh dải chữ r34. Các đường khác còn hở: (1) `_ket_thuc_cau` dùng tìm kiếm không neo đầu với dải trắng/dấu đóng tham lam trước neo cuối. Khi dải giữa dòng dài rồi mới gặp chữ, máy regex thử lại từ nhiều vị trí trong dải, dẫn tới số bước bậc hai. (2) `int` ở `tach_khoan` nhận số đầu dòng không giới hạn độ dài. Giá trị vượt trần chuyển đổi của Python ném `ValueError`; trên CLI, phép đo này nằm sau model và nằm ngoài các lỗi được bắt ở bước gọi. (3) DOCX giới hạn byte từng thành phần và số thứ tự Word, nhưng `_danh_dau_giu_trang` đệ quy cả vào cây sẽ bị bỏ. `_doan_trong` và `duyet` cũng đệ quy wrapper. `RecursionError` không thuộc nhóm lỗi nguồn mà CLI bắt. (4) Mỗi điểm mở rộng lại chuỗi `lvlText` rồi nối vào chuỗi khoản đã có. Trần số đếm không giới hạn độ dài nhãn hay tổng số byte sau khi mở rộng. Điểm nhiều đoạn còn khiến chuỗi khoản bị sao chép lặp lại.
- **Hint patch.** Đặt ngân sách ở đầu tuyến đọc nguồn và truyền kết quả phân tích nguồn đã giới hạn sang phép so. Trong `tach_khoan`, giữ số dưới dạng lát chuỗi, kiểm độ dài/miền trước `int` và xác định dấu kết bằng quét lùi một lần hoặc `rstrip` trên tập ký tự hiện có. Trong `doc_dieu_docx`, kiểm độ sâu/node của XML trước mọi phép duyệt đệ quy hoặc dùng duyệt tường minh có ngân sách, giới hạn kích thước nhãn/kết quả được mở rộng, gom các dòng của từng khoản rồi nối một lần. Bộ quét nhãn đầu dòng dùng thời gian tuyến tính trên phép đọc đã giới hạn. Trả lỗi nguồn rõ ràng và giữ ý nghĩa của kết quả chưa xác minh. Giới hạn kích thước đầu vào đơn lẻ chưa chặn được cả đệ quy, công việc regex và độ dài đầu ra. Dùng chung ngân sách ở ranh giới phân tích, với các phép tiêu thụ tại đúng chỗ phát sinh chi phí.
- **Hint test.** Đối chứng nguồn dài hợp lệ trong hạn, trường hợp thiếu dấu kết đã có của J2, dấu câu theo quy tắc hiện tại và điểm tự động. Ca âm lần lượt kiểm dải trắng giữa dòng, số quá dài, wrapper quá sâu, mở rộng nhãn/rất nhiều dòng điểm. Đo tăng theo kích thước với giới hạn thời gian tiến trình bên ngoài. Khi bỏ riêng mỗi chốt, ca đích phải báo vi phạm về công việc/tài nguyên hoặc loại lỗi nguồn. Việc phục hồi regex lồng của r33 cần phép đo có timeout. Bộ hiện có kiểm ngưỡng dương, bảng `DOT_BIEN` r34 chưa phục hồi trực tiếp cơ chế J2.
- **Hạng và lịch sử.** P2 theo E6/F4/J2 vì một lần đọc có thể đình trệ, thoát bằng traceback hoặc đã tiêu token trước khi lỗi. Dãy biểu hiện tài nguyên đang mở có nguyên nhân độc lập với regex lồng vừa bỏ. Policy cần ghi các giới hạn kích thước đã chọn để người dùng biết khi phải chuyển sang đọc thủ công. [Quét XML](../scripts/tl_core/llm_route.py#L1047) · [Ghép nhãn](../scripts/tl_core/llm_route.py#L1397) · [Đường gọi rồi so](../scripts/tl_core/llm_route.py#L1730) · [Các lỗi CLI bắt](../scripts/tl_core/ops_misc.py#L3120)

### Lớp `ranh-gioi-ky-tu` [P2] — `scripts/tl_core/llm_route.py:1242,1327,1345`

- **Bất biến.** Chữ còn hiệu lực trong mọi đoạn DOCX phải qua danh sách ký tự trên chữ gốc trước khi gộp khoảng trắng, quyết định đoạn rỗng hay tìm tiêu đề.
- **Miền.** `_phan_tich_doan` trả cả chữ đã gộp và lỗi ký tự của chữ gốc. `doc_dieu_docx` chọn `i0` chỉ từ chữ đã gộp, số và cờ phần tử lạ; vòng kiểm lỗi ký tự bắt đầu từ `i0`. Một đoạn không số trước tiêu đề chỉ chứa khoảng trắng Unicode ngoài tập, hoặc ký tự xuống dòng thực nằm bên trong text node, có thể gộp thành rỗng nhưng vẫn mang `ky_tu_la`. Đoạn đó biến mất ở cả hai bước. Cùng đường vào ở đoạn trực tiếp, content control, `customXml` và chữ từ mẩu bỏ được giữ dưới chính sách “chỉ khoảng trắng”. Đoạn có chữ nhìn thấy hoặc lỗi cấu trúc vẫn được xét. Hợp đồng r7 bỏ qua đoạn rỗng hợp lệ, §2.19 S2 buộc xét ký tự trên chữ gốc trước khi gộp.
- **Hint patch.** Sau khi `_doan_trong` và `_phan_tich_doan` tạo danh sách đoạn, kiểm `ky_tu_la` trên toàn bộ danh sách ngay trước `co_nd`. Mọi chỗ tạo đoạn dùng cùng giá trị lỗi đã tính từ chữ gốc. Bước bỏ đoạn rỗng, chọn tiêu đề và ghép khoản chỉ nhận danh sách đã kiểm.
- **Hint test.** Chặn riêng một đoạn chỉ chứa khoảng trắng ngoài miền ở trước tiêu đề, trong vùng và cuối tệp. Giữ đối chứng đoạn rỗng chỉ có phân cách được phép và chữ ngoài miền nằm trọn trong một mẩu đã bỏ. Đột biến dời vòng kiểm về sau `i0` phải làm đỏ ca trước tiêu đề.
- **Hạng và lịch sử.** P2 vì đây là vi phạm chốt đầu vào đã công bố với một vị trí cụ thể. Từ đọc mã chưa có bằng chứng đoạn trắng trước tiêu đề làm thay đổi hai vế của khoản. Nối R1/R3 lượt 15, S1/S2 lượt 16 và các phép đo ký tự ASCII/Unicode lượt 17–18. [Chữ gốc và chỉ số đầu](../scripts/tl_core/llm_route.py#L1242) · [Vòng kiểm hiện tại](../scripts/tl_core/llm_route.py#L1345) · [§2.19](../ops/specs/llm-khoan-docx-r34.md#L249)

| Lớp | Biểu hiện hiện tại | Đối chiếu |
| --- | --- | --- |
| `ranh-gioi-khoan` | 3 nhóm hình dạng · P2 | J1 vá ca đích, lớp chưa đóng. |
| `can-tai-nguyen-doc-nguon` | 4 đường chi phí · P2 | J2 đóng ở nhánh đã báo. Lớp E6/F4/J2 chưa đóng ở đường đọc còn lại. |
| `ranh-gioi-ky-tu` | 1 vị trí kiểm bị bỏ qua · P2 | Nhánh kiểm chữ gốc của `ranh-gioi-khoan` tại R1/R3/S1/S2. |
| `docx-markup-du-thao`, `docx-khoa-bang-style`, `docx-so-hien-thi`, `docx-test-doc-lap` | 0 biểu hiện cũ còn mở trong miền đã kiểm | Xem bảng lịch sử và phần chưa đo. |

Đối chiếu slug lịch sử: `ranh-gioi-khoan` giữ nhánh phân loại nhãn và J1. `ranh-gioi-ky-tu` nối riêng các biểu hiện kiểm chữ gốc R1/R3/S1/S2 của cùng slug nguồn theo hồ sơ lượt 18–19. Chốt thứ nhất cần quét nhãn không mất cấp, chốt thứ hai cần kiểm chữ gốc trước khi bỏ đoạn. Mỗi biểu hiện hiện tại chỉ thuộc một lớp, lịch sử và mẫu số lớp mở của lượt 33 được giữ. [Lượt 18](../ops/acceptance/llm-khoan-docx/r1/review-18-codex/VERDICT.md#L55) · [Lượt 19](../ops/acceptance/llm-khoan-docx/r1/review-19-codex/VERDICT.md#L57)

Hai lớp mở ở lượt 33 vẫn còn biểu hiện trên r34, dù J2 gốc đã đóng. Theo phép đếm lớp của §8.3, 0/2 lớp cũ đủ bằng chứng đóng toàn miền. Báo 3 lớp với 8 nhóm biểu hiện. Lịch sử `ranh-gioi-khoan` đã vượt ngưỡng lặp một lớp tại §12. Phép kiểm đóng lớp cần đối chiếu cả bộ sinh nhãn, bộ quét tuyến thô và các đối chứng đã duyệt. [Protocol §8.3 và §12](../docs/PROTOCOL_DA_PHIEN.md#L812) · [ADR-0060 M2](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L40)

**Word và Google Docs.** Mã có nhánh cho bookmark, perm, proof, comment, dấu ngắt do render, hyperlink, content control, tab/ptab và dấu nối không ngắt. Trường, hình, chú thích, ký hiệu, bảng, ngắt mềm, `mc:`, đánh số qua style và dạng Strict thuộc giới hạn đã công bố. Hồ sơ và fixture hiện có chưa xác lập phần tử export thường gặp ngoài danh sách công bố gây chặn oan. [Danh sách phần tử](../scripts/tl_core/llm_route.py#L655) · [Các giới hạn hướng dẫn](../docs/GOI_AGENT_DA_NEN.md#L390)

## Kết quả test và đột biến

Thư mục bằng chứng `/tmp/wp1525-r34-evidence.0ArjEHTl`. Linux x86_64, Python 3.13.18, Git 2.43.0, Codex CLI 0.172.0, Ruff 0.15.15. Bản sao detached cục bộ dùng object store của checkout shallow, với `core.abbrev=7`, bytecode bị tắt và cache ngoài checkout. Các lệnh mặc định đo head đã nêu ở đầu. Bản sao base chỉ dùng đối chứng. Golden và selftest tạo fixture/state trong chính bản sao tạm. Release verify chạy khi bản sao head còn sạch.

| Lệnh | Trạng thái | Mã thoát và bằng chứng |
| --- | --- | --- |
| `python scripts/tl_core/llm_route_test.py` | `passed` | Rc 0, **63/63** ca đạt, **265/265** đột biến bị giết. `llm.log`. |
| `python scripts/tl.py --deterministic workflow-audit --strict --json` | `passed` | Rc 0, `ok=true`, 26 card, 60 task, 194 lệnh, 0 lỗi/cảnh báo. `workflow.log`. |
| `python scripts/tl.py --deterministic golden-test --json` | `passed` | Rc 0, `ok=true`, **20/20** ca và projection ổn định. Lần đầu **19/20** stdout trùng byte. `hygiene_sweep_fixture` chỉ đổi khóa volatile đã khai `snapshot_age_s`, 0 khóa lệch chưa khai. `golden.log`. |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | `passed` | Rc 0, `ok=true`, **187/187** tệp, 0 thiếu/thừa/sai. Package hash `867188712883ac9b4a4600e30bf680c1776424484bf41eb66c4e077b354035d0` khớp manifest. `release.log`. |
| `python ops/lease_publish.py check --root . ops/leases/llm-khoan-docx-r34-g1-claude.yaml` | `passed` cục bộ | Rc 0, “ĐĂNG ĐƯỢC”, Issue #1525, neo `64b7f2c14776`, hạn 22:29 UTC. Hai lớp GitHub của lệnh nằm ngoài phép đo local. `lease.log`. |
| `python scripts/tl.py --selftest` | `failed` | Head rc 1, **1774/1790**, ca tích hợp `r1525_llm_khai_niem_tep_docx_cau_truc` đạt. `selftest-head.log`. So với base ở dưới. |
| `python scripts/tl.py --deterministic determinism-audit --strict --json` | `passed` | Rc 0, `ok=true`, **15/15**. `determinism.log`. |
| `python scripts/tl.py --deterministic doc-claims-check --strict --json` | `failed` trên head và base | Rc 2 mỗi bản. 131 tệp mỗi bản, cùng cờ cứng `SHA_NOT_A_COMMIT` cho `9941d8af52aeede1c78ea4e232fbe9a8d5272033` tại protocol dòng 1680. `git cat-file -t` rc 128 trong checkout shallow. `claims-head.log`, `claims-base.log`. |
| `python -m ruff check --no-cache --select F scripts/tl.py` | `failed` lint, đạt delta | Rc 1 trên head và base, cùng 12 F821 và 0 F401. `cmp` hai log rc 0. `ruff-head.log`, `ruff-base.log`. |
| `python -m ruff check --no-cache --select F scripts/tl_core/llm_route.py scripts/tl_core/llm_route_test.py` | `passed` | Rc 0, “All checks passed!”. `ruff-modules.log`. |
| `loi_ruff_ci()` qua `runpy.run_path(".claude/dev/ci_dang_ky_test.py")` theo adapter | `passed` | Rc 0, `RUFF_CONTRACT 3 []` cho hợp đồng pin/probe. `ruff-contract.log`. |
| `git diff --check <mốc> HEAD` | `passed` cho bản vá và packet, `failed` cho toàn PR | Rc lần lượt 0, 0, 2. Toàn PR có 3 dấu xuống dòng Markdown ở hồ sơ lượt 8 #1514, dòng 3–5, đã có tại mốc giao #1514. |

Chạy `python -B -m pdb scripts/tl_core/llm_route_test.py`, breakpoint dòng 2335 ở nhánh `except TinHieuChotCa` với `ten.startswith("wp1525_")`. Rc của tiến trình và suite đều 0. **168/168** mục mang tiền tố vào đúng nhánh tín hiệu của ca đích. Harness tạo mã đột biến trong thư mục tạm. `mutation-trace.log` SHA-256 `bd0bc909d81dc20c36c19ed1552150cc728cba4c3b55d47ec5be5f8ddde2fb6f`. [Harness](../scripts/tl_core/llm_route_test.py#L2316)

| Mutant có sẵn | Tín hiệu đo được |
| --- | --- |
| `wp1525_dai_chu_bo` | `ca_khoan_mat_so_co_diem_dat` phát hiện mở lại nhãn số dính chữ có dấu kết. |
| `wp1525_dai_chu_khong_dem` | Cùng ca, phát hiện nhận nhãn số–chữ có đệm vào phân đoạn. |
| `wp1525_dai_chu_gach_khong_doi_trang` | Cùng ca, đối chứng thân khoản mở bằng `e-mail` hoặc từ ASCII bị chặn. |
| `wp1525_so_so_bo` | Cùng ca, phát hiện nhận nhãn số–số có dấu gạch. |
| `wp1525_tho_nhan_diem` | `ca_wp1514_luot9` phát hiện dòng điểm trở thành khoản thô. |
| `wp1525_khong_dat_lai_cap_con` | `ca_cau_truc_docx_dat` phát hiện nhãn điểm ở khoản thứ hai tiếp số của khoản trước. |
| `wp1525_bo_qua_start_override` | Cùng ca, đối chứng hợp lệ bị chặn do danh sách bắt đầu từ 5 thay vì 1. |

Lần chạy lại golden trên head sau khi selftest head kết thúc vẫn rc 0, 20/20 ca, 20/20 projection ổn định và 19/20 stdout trùng byte. Chênh lệch raw vẫn thuộc đúng `snapshot_age_s` ở `hygiene_sweep_fixture`. `golden-rerun.log`.

Selftest base rc 1, **1773/1789**. Transport đạt **12/12** trên mỗi cây. Lọc ID `[FAIL]`, sắp theo `LC_ALL=C` và so bằng `cmp` trả rc 0. Cùng **16** ID đỏ, gồm 14 ca thuộc nhóm `/tmp/.git` rỗng đã báo (8 `r973_bootstrap_*`, 5 `wp433_*`, `wp727_tl_gws_refresh`) và hai ca `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim`, `r268_l2_trichotomy_theo_trang_thai_object`. Delta tập lỗi bằng 0 và tiêu chí selftest N/N vẫn đỏ. SHA-256 log head `a4f618212a1497030a3ab085d146bf665b64dff350df777ac25bf1457b1891cf`, log base `178146b59e8944662170acabd7ae45240b0eb1ba8f8f93f024bc5801a4629310`, danh sách lỗi hai bên `6c344d8f8a71b854460d8d4badd425904bdd116177ea8b3e14bd2387a2a14505`.

## Không đo được

- Các nhóm biểu hiện mới và hint test dựa trên đường thực thi đọc được từ mã. Không có phép thử mới cho nhãn còn lọt, ngân sách theo kích thước/độ sâu hoặc ký tự ngoài miền trước tiêu đề. Ca J2 sẵn có kiểm ngưỡng dương của nhánh dải chữ. Hệ số tăng và tác động CLI chưa được đo với các đường chi phí còn lại.
- Chưa có corpus DOCX do Word/Google Docs xuất để xác định tần suất chặn oan ngoài giới hạn, hay để đối chiếu hành vi Word với biến thể thuộc tính đánh số. Cặp mốc move hiện chỉ được đo cân theo ID, chưa có phép đo thứ tự/lồng phạm vi hay văn bản Word render trong biến thể khác ca sẵn có. Các thuộc tính ẩn chữ hoặc dấu đoạn và style ký tự mặc định cần đối chứng render trước khi kết luận ảnh hưởng với bản dự thảo thực.
- `skipped` trong sáu lệnh của prompt là 0. `not_run` gồm Windows bản địa, CI từ xa, hai lớp GitHub của lease, model/API thật và LIVE. Windows là `required` theo M3 vì diff toàn PR có dòng Python thêm/sửa chứa `encoding=`. Tập ID đỏ đối chứng Linux chỉ có giá trị cho môi trường đã đo. [ADR-0060 M3](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L43)
- `not_measured` gồm provenance CI, mốc remote hiện hành, model/effort và kết quả terminal của launcher đang chạy. `codex --version` trả 0 cùng cảnh báo không tạo được PATH alias trên filesystem read-only. Phiên bản binary và định danh provider/surface/transport trong run là phần đo được.

## Readback và kết luận

Head và tree khớp đầu/cuối. `git diff --exit-code` và `git diff --cached --exit-code` rc 0. Snapshot `git status --porcelain=v1 --untracked-files=all --ignored` từ rỗng đến đúng dòng `?? .review/VERDICT.md`. Snapshot xác nhận delta quan sát được giữa hai mốc. Repo làm việc của Executor nằm ngoài phạm vi quan sát.

**0 P0, 0 P1, 3 P2, 0 P3.** Verdict APPROVE theo ngưỡng P0/P1 của prompt. Điều kiện merge của ADR-0060 M1 chưa đạt vì còn ba lớp P2. Full selftest, doc-claims strict và bằng chứng Windows exact head cũng chưa đạt hoặc còn thiếu. [ADR-0060 M1](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32) · [ADR-0062](../docs/adr/0062-adr-0060-mac-dinh-va-dong-bang-adr-0054.md#L12)

P2_mo: 3
VERDICT: APPROVE
