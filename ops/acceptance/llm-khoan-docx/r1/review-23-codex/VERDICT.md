# Verdict packet #1525 r23 lượt 23 — Codex

reviewed_sha: 30e3e0747773d829b9f451f6d8ed476a0ac8d9dc

tree_sha: a08c83094a8c6d00abb15d5f680101d5fc3e4f46

base_sha: 64b7f2c14776d5d0e1d34a6be4725490956f5bec

provider: openai_codex

execution_surface: codex_cli

transport: machine

## Đối chiếu lượt 22 và đặc tả r23

- Checkout độc lập, detached tại đúng SHA của PR #1517 trong bản sao `ducthangho/tra-luat`. Ref đã cấp `origin/ccr-89c0d2e2-inanqb` trỏ cùng SHA. `git merge-base` xác nhận base, tree base `0cc14e79cecd2ce44bc4dc6cff92cadb31fd7ee4`. Diff binary của worktree và index rỗng khi bắt đầu. Mốc kế thừa #1514 là `fcb12b3873c3bec2c339029136243ed2c804ce05`, mốc trước bản vá r23 là `39f2f88bea2f07c29faa9cda28274c7f1361c5cc`.
- Lease #1525 r23/g1, class `sensitive`, 22 lượt đã dùng trên trần 23. Kiểm cục bộ ngày 26-11-2026 trong thời hạn 11:01–19:01 UTC. SHA-256 spec `8b47a74259c2457cabf2ef841a98cac885ebb03c2274b3b8facd22aa08b87c73` khớp lease. Đối chiếu YAML đạt **23/23** liên kết hai chiều `da_bi_thay_the` ↔ `thay_the_cho` và **24/24** hash spec, từ #1514 r9 đến #1525 r23. Quyền đứng và ngoại lệ M5 được ghi trong lịch sử đặc tả. [Lease](../ops/leases/llm-khoan-docx-r23-g1-claude.yaml) · [Spec](../ops/specs/llm-khoan-docx-r23.md)
- Write set **126** đường dẫn duy nhất. Hash theo quy tắc sắp xếp, nối LF và kết LF khớp `05cc2e713e8e57ac2547cae4426d9927a0bfb1a696877dc451886bfbbfc83b2e`. Bản vá r23 **8/8** trong write set. Packet **122/122** sau khi loại bốn tệp hồ sơ kết thúc #1514 theo prompt. Toàn PR có **170** đường dẫn, gồm 44 đường dẫn kế thừa ngoài write set và bốn tệp hồ sơ #1514 ở trên. SHA-256 của `git diff` theo thứ tự toàn PR, toàn packet, bản vá r23 lần lượt là `19f3c22e5ebaa8ec2a72755c4a0ea909f0415c7b23cc6fba2714a363e54a77a5`, `316f0f60bc223d5bcdd4065cfb88292426e9a9c2290cfa19e6caa5323aa0a7d2`, `c203858d6ba6e943b1e45617e70fd5d0f320a836436ff73d98973ab16ca10dcd`.
- Reviewer `openai_codex / codex_cli / machine`, Codex CLI 0.172.0, run `b128ea6b8bc944f7a5c7e250c9c90e4b` qua launcher. Bắt đầu lúc 11:08:02 UTC. SHA-256 prompt `c9559a52c4517d8424c630edaf874461024fce616b576170d3673fa1c2f8a54a` khớp run. Executor `anthropic_claude / claude_code / machine/local` theo lease, phiên `session_015GtxrZQYT3Vt8PJdXrjEKg`. Ubuntu 24.04.5, Python 3.13.18, Git 2.43.0, shallow, `core.abbrev=7`, sandbox `workspace-write` với metadata Git chỉ đọc. Model và effort phục vụ `KHONG_DO_DUOC` tại thời điểm ghi verdict. [Protocol §8.1](../docs/PROTOCOL_DA_PHIEN.md#L770)

| Mục | Trạng thái | Bằng chứng |
| --- | --- | --- |
| Y1 · lượt 22 `fbddd4771e7ac3359f19a88d13b841b8d23624fc` · §2.25 | **ĐÃ VÁ THẬT** với `delText` pha tab trong run gạch. **VÁ MỘT PHẦN** với lớp | Run gạch, `del` và `moveFrom` gọi chung `_ruot_bi_bo`. Ca 38 và mutant khôi phục cách đọc riêng phân biệt được hai bản. Phần tử hiển thị chưa hiểu trong wrapper bị bỏ vẫn có thể biến một mẩu hỗn hợp thành mẩu trắng, xem Z1. [Mã](../scripts/tl_core/llm_route.py#L990) · [Ca](../scripts/tl_core/llm_route_test.py#L1452) |
| Y2 · lượt 22 · §2.25 | **ĐÃ VÁ THẬT** với hai `body`, hai `sdtContent`, wrapper lạ/thiếu nội dung và khóa `styleId` trùng. **VÁ MỘT PHẦN** với lớp | Bảng đơn trị chạy trước chọn body, wrapper khối và inline dùng cùng kiểm QName, style ID trùng bị chặn. Còn ứng viên trùng ở mức ZIP trước khi vào XML, xem Z2. Có khoảng trống kiểm thử đơn trị metadata, xem Z4. [Mã XML](../scripts/tl_core/llm_route.py#L629) · [Ca](../scripts/tl_core/llm_route_test.py#L1642) |
| Y3 · lượt 22 · §2.25 | **ĐÃ VÁ THẬT** với các dạng có trong ca r23. **VÁ MỘT PHẦN** với lớp | Ca hiện có bao phủ ngoặc/chấm/gạch có khoảng đệm ngang, chữ hoa/lặp và nhãn thập phân kết thúc trước khoảng trắng. Giữ đối chứng từ ghép và chữ viết tắt. Ngữ pháp này chưa phủ nhãn đa cấp có dấu bao do chính `_nhan` cho phép, xem Z3. [Hai regex](../scripts/tl_core/llm_route.py#L490) · [Ca](../scripts/tl_core/llm_route_test.py#L686) |
| §1–§2.3 · K1 của #1514 | **ĐÃ VÁ THẬT** cho hai biểu hiện K1 | Dòng điểm đã nhận diện luôn trả `None`. Dòng tiếp “là” ở nguồn có số rơi vào nhánh từ chối dòng không số. Nguồn mất số mà một dòng chỉ có từ nối ở đầu không thể qua phép so với thuật ngữ rỗng. Fixture Điều 3 và ba đầu ra đã lưu vẫn khớp 8/8 trong suite. `can_nguoi_duyet` luôn true, `pham_vi_kiem` lấy theo nguồn ranh giới. Diff giữ giao diện cờ và đường gọi model. [Tách khoản](../scripts/tl_core/llm_route.py#L1334) · [Ca K1](../scripts/tl_core/llm_route_test.py#L1225) · [CLI](../scripts/tl_core/ops_misc.py#L3120) |
| §2.4–§2.9 · A1, C1, D1, E1, F1 và phần bảng của B2/C2/E3/E4 | **HẾT ĐỐI TƯỢNG do hợp đồng r7** với điểm cắt và duyệt ô bảng. **ĐÃ VÁ THẬT** về fallback | Đoạn đầu có nội dung phải là tiêu đề khớp Điều yêu cầu. Thân đọc đến hết body, từ chối bảng và khối lạ, cùng tiền tố Điều/Chương/Mục/Phần. DOCX thiếu đánh số tự động dừng bằng `ValueError` và CLI rc 2. Kiểm các hàm hiện hành không còn `KhongCauTruc`. Tính duy nhất ở cấp part xem Z2. [Vùng](../scripts/tl_core/llm_route.py#L1205) · [CLI](../scripts/tl_core/ops_misc.py#L3037) |
| §2.4–§2.13 · A2/A5, B2, C2, D2, E6, F3–F5, G1–G3, H2/H4, J1, K1/K3 | **ĐÃ VÁ THẬT** ở các biểu hiện lịch sử về ô/cấp/ID/khởi tạo và style. **VÁ MỘT PHẦN** với lớp chọn định nghĩa | Đếm từng `numId` theo thứ tự, khởi tạo từ `start` (vắng dùng 0), `startOverride` thay giá trị ở cấp tương ứng. Sau mục cấp cha, xóa bộ đếm các cấp con. Cấp nhảy và nhiều danh sách trong Điều dừng, số khoản liên tục từ 1. Chặn gắn cấp qua style và các quy tắc restart chưa hỗ trợ. Định nghĩa lỗi không dùng vẫn qua ở ca đối chứng. XML được lấy theo quan hệ của đúng part, xem Z2 cho trường hợp tên member trùng. [Định nghĩa](../scripts/tl_core/llm_route.py#L748) · [Bộ đếm](../scripts/tl_core/llm_route.py#L1188) · [Ranh giới](../scripts/tl_core/llm_route.py#L1256) |
| §2.4–§2.13 · A3/A4, B1/B3/B4/B6, C3–C5, D3–D6, E2/E5, F6, G4, H5, J2/J5 | **ĐÃ VÁ THẬT** ở các biểu hiện lịch sử đã đo. **VÁ MỘT PHẦN** với lớp lọc mẩu đã bỏ | Dò “là” chỉ trong đầu khoản cấu trúc, kiểm dấu phân cách theo đoạn, đọc XML gốc để xử lý sửa đổi. Gạch đơn/kép tính riêng theo style, từ chối toggle nhiều tầng khi thiếu định dạng trực tiếp. Chặn sửa đổi dấu đoạn và move range không cân. Cho phép metadata wrapper hợp lệ, tab và ngắt trang/cột cuối đoạn. Strict, `mc:` và phần tử hiển thị chưa hiểu vẫn bị chặn theo phạm vi công bố. Xem Z1 về điều kiện coi mẩu bị bỏ chỉ chứa khoảng trắng. [Phân tích đoạn](../scripts/tl_core/llm_route.py#L1005) · [Từ nối](../scripts/tl_core/llm_route.py#L1474) |
| §2.5, §2.9, §2.18 · A6, B5, F2, R2 và câu dẫn | **HẾT ĐỐI TƯỢNG do hợp đồng r7** với điểm gõ tay dưới dạng đoạn riêng. **ĐÃ VÁ THẬT** cho chốt số gõ tay và câu dẫn trong phạm vi đã đo | Đoạn không số sau khoản đầu bị chặn. Với đoạn đánh số tự động, số gõ tay dạng ngoặc kín bị phát hiện kể cả khi dính chữ số. Dạng thập phân có đối chứng. Trước khoản đầu chỉ được có đúng một câu dẫn chuẩn hoặc vắng. [Số gõ tay](../scripts/tl_core/llm_route.py#L609) · [Câu dẫn](../scripts/tl_core/llm_route.py#L1295) |
| §2.10–§2.21 · G6, H1, J3, K2, L1–L5, M1/M2, N1–N3, Q1/Q2, R1/R3, S1–S3, T1/T2, U1/U2 | **ĐÃ VÁ THẬT** cho các biểu hiện đã nêu ở đầu vào tới parser. U2 trong giới hạn đã duyệt | Tiêu đề đích không phân biệt hoa thường. Chốt cấm tiền tố trong thân xét bản chiếu chữ/số, quan hệ so URI đầy đủ, parser đọc byte XML. Chốt ký tự chạy trước gộp/tách, một tầng xử lý BOM và loại số mũ khỏi tập cho phép. ID không chuyển qua int, thuộc tính số lỗi bị chặn theo phạm vi dùng, khối so QName. Hướng dẫn giữ nguyên câu chữ khi chốt từ chối dẫn chiếu đầu đoạn. [Tiền tố và ký tự](../scripts/tl_core/llm_route.py#L539) · [Quan hệ](../scripts/tl_core/llm_route.py#L707) · [Hướng dẫn](../docs/GOI_AGENT_DA_NEN.md#L390) |
| §2.22–§2.24 · V1–V4, W1–W5, X1–X3 | **ĐÃ VÁ THẬT** cho từng biểu hiện lịch sử trong bộ đo. **VÁ MỘT PHẦN** ở ba lớp Y1–Y3 | Chuyển `--markup-strict`; lỗi producer làm CLI dừng; `docDefaults/pPrDefault/numPr` bị từ chối. Cấp trùng và trường đơn trị được xử lý, kể cả đối chứng A5. Phần số hiệu của V3/W1/W2/W3 là giới hạn đã duyệt của producer, cùng U2. Phần thô sau khi đọc chữ vẫn chịu Z3. [CLI](../scripts/tl_core/ops_misc.py#L3074) · [Đặc tả](../ops/specs/llm-khoan-docx-r23.md#L262) |
| §3 · A7/A8, B7/B8, C6/C7, D4, E5, F5, G5, H3, J4, K4, L6 | **ĐÃ VÁ THẬT** cho ca và hướng dẫn lịch sử. **VÁ MỘT PHẦN** với yêu cầu kiểm riêng từng chốt ở r23 | Suite và các mutant lịch sử đạt. Ca r23 dùng lại harness đúng cơ chế, song bỏ chốt đơn trị riêng cho hai nút metadata vẫn qua toàn suite, xem Z4. [Bảng mutant](../scripts/tl_core/llm_route_test.py#L1812) · [Harness](../scripts/tl_core/llm_route_test.py#L2145) |

Khi chuẩn nguồn được dựng đúng, `lech_nguyen_van` đối chiếu số thứ tự theo vị trí, số lượng, thuật ngữ và định nghĩa riêng, giữ xuống dòng của điểm. Đầu ra tự bỏ, cắt, gộp hoặc tráo khoản không qua được phép so này. Z1–Z3 xảy ra trước phép so, khi chuẩn nguồn đã đổi. Phép so thô vẫn có giới hạn đã công bố đối với dòng mất hết nhãn, tiểu mục trùng hình dạng số khoản hoặc các dòng đã mất quan hệ thụt lề. [Phép so](../scripts/tl_core/llm_route.py#L1474) · [Phạm vi thô](../scripts/tl_core/llm_route.py#L1311)

## Findings

### Z1 [P1] Mẩu sửa đổi chứa ký hiệu có thể bị đọc thành mẩu chỉ có khoảng trắng — `scripts/tl_core/llm_route.py:990`

**Kịch bản.** Trong một định nghĩa, một mẩu đã xóa hoặc chuyển đi chứa ký hiệu Word cùng tab. Khi bỏ trọn mẩu đó, hai phần chữ còn hiệu lực đứng liền nhau. Bộ đọc giữ tab như một dấu tách từ, nên bản dựng có thêm khoảng trắng so với chữ còn lại sau sửa đổi.

**Căn cứ và hạng.** `_ruot_bi_bo` bỏ qua `w:sym` nhưng đưa `w:tab` vào ruột. Nhánh `del`/`moveFrom` gọi helper rồi `continue`, vì vậy ký hiệu không tới chốt phần tử hiển thị chưa hiểu trong `run`. Kết quả chỉ còn khoảng trắng và được giữ. Nhánh run gạch ngoài các wrapper này có chốt `la` cho ký hiệu, nên đây là lỗ ở cách duyệt hai wrapper dùng chung. P1 như Y1 vì dấu phân cách sai nằm trong chuẩn nguồn của đường cấu trúc, có thể được phép so chấp nhận là nguyên văn. [Phân loại ruột](../scripts/tl_core/llm_route.py#L990) · [Chốt run](../scripts/tl_core/llm_route.py#L1044) · [Nhánh wrapper](../scripts/tl_core/llm_route.py#L1094) · [Verdict Y1](../ops/acceptance/llm-khoan-docx/r1/review-22-codex/VERDICT.md#L30)

**Đề xuất.** Chỉ giữ phân cách khi mọi phần tử có thể hiển thị trong mẩu đều được chứng minh là khoảng trắng. Phần tử mang chữ/ký hiệu làm bỏ trọn mẩu. Phần tử chưa hiểu nên làm parser dừng nếu có ảnh hưởng đến quyết định giữ trắng. Đối chứng cho cả ba nhánh với mẩu thuần phân cách và mẩu có nội dung cùng phân cách.

### Z2 [P1] Gói DOCX có nhiều member cùng tên vẫn có thể được chọn một bản ngầm — `scripts/tl_core/llm_route.py:669`

**Kịch bản.** Quan hệ `officeDocument` trỏ đến một tên part nhưng thư mục ZIP có hai member tại tên đó. Một bản có đủ khoản của Điều, bản kia chỉ có các khoản đầu, đánh số liên tục. Nếu bản bị cắt là bản được tra theo tên, tiêu đề và các kiểm tra XML đơn trị đều đạt và phép so dựng chuẩn từ bản bị cắt. Cùng cơ chế áp dụng nếu member quan hệ, styles hay numbering có nhiều bản.

**Căn cứ và hạng.** Cả nhánh bounded lẫn nhánh dự phòng mở theo chuỗi tên. Kiểm quan hệ dùng `ten in z.namelist()`, chỉ chứng minh có ít nhất một lần. Thư viện `zipfile` của môi trường thêm mọi entry vào `filelist` nhưng cập nhật `NameToInfo` theo tên, và `getinfo` lấy một giá trị từ bảng này. Chốt Y2 chỉ chạy sau khi đã chọn một entry. P1 theo Y2 vì đầu vào mâu thuẫn vẫn có thể xác nhận thiếu khoản, số khác hoặc chữ dự thảo chưa lọc trên tuyến cấu trúc. Cách Word xử lý gói mâu thuẫn này chưa được đo. [Đọc part](../scripts/tl_core/llm_route.py#L669) · [Quan hệ](../scripts/tl_core/llm_route.py#L707) · [Reader bounded](../scripts/tl_core/ingest_engine.py#L138) · [Chốt sau chọn](../scripts/tl_core/llm_route.py#L1154)

**Đề xuất.** Xác thực mỗi part dùng để diễn giải có đúng một ZIP entry trước khi đọc, gồm các part quan hệ và tên mặc định. Dùng đối tượng entry đã xác thực cho cả nhánh bounded và dự phòng. Tách kiểm này khỏi chính sách A5 dành cho định nghĩa danh sách không dùng bên trong một part.

### Z3 [P2] Nhãn điểm thập phân đa cấp có ngoặc vẫn có thể thành khoản ở đường thô — `scripts/tl_core/llm_route.py:502`

**Kịch bản.** Nguồn thô mất số khoản nhưng giữ nhãn của một điểm cấp con. Nhãn gồm số cấp cha và cấp con ngăn bằng dấu chấm, cả cặp đặt trong ngoặc tròn. Dòng điểm có đủ từ nối ngoài ngoặc và dấu kết, như dòng định nghĩa trước nó. Bộ tách có thể tạo thêm một khoản từ dòng điểm.

**Căn cứ và hạng.** `_nhan` chấp nhận hai placeholder thập phân, dấu chấm và ngoặc bao. Nhánh thập phân của `_RE_DIEM` yêu cầu dòng bắt đầu bằng chữ số, nhánh ngoặc của `_RE_SO_KHOAN` chỉ nhận một số nguyên, và `_dong_mo_ho` cho qua ngoặc cân. Chốt số nội dòng bỏ qua chấm có chữ số theo sau và vị trí bắt đầu số đứng ngay sau chấm. Do đó đường mất số giữ cả dòng, rồi `_tu_noi` có thể tìm từ nối sau ngoặc. Cùng độ lệch miền xảy ra với nhãn đa cấp không ngoặc có dấu chấm cuối dính thân, vì nhánh thập phân đòi khoảng trắng. P2 theo Y3/K1 vì cần nguồn thô giữ một nhãn phân biệt được và điều kiện từ nối/dấu kết. Kết quả mang cờ duyệt ranh giới, song vẫn có thể được ghi như một mục khớp nguyên văn theo phân đoạn sai. [Nhãn thô](../scripts/tl_core/llm_route.py#L490) · [Nhãn cấu trúc](../scripts/tl_core/llm_route.py#L928) · [Tách thô](../scripts/tl_core/llm_route.py#L1343) · [Từ nối](../scripts/tl_core/llm_route.py#L1453)

**Đề xuất.** Dùng ngữ pháp chung cho nhãn có thể phục hồi từ text hoặc giới hạn cú pháp nhãn cấu trúc theo ngữ pháp đó. Đo cả ngoặc bao, dạng dính thân sau dấu chấm cuối và các tổ hợp nhiều cấp được chấp nhận. Giữ đối chứng số thập phân thật, từ ghép, chữ viết tắt. Trường hợp mất hết nhãn vẫn cần duyệt ranh giới như đã công bố.

### Z4 [P2] Hai trường đơn trị metadata của content control thiếu ca khóa riêng — `scripts/tl_core/llm_route_test.py:1645`

**Kịch bản và căn cứ.** §2.25 Y2 yêu cầu `sdtPr` và `sdtEndPr` mỗi loại xuất hiện tối đa một lần. Ca r23 kiểm hai `sdtContent`, thiếu nội dung và có con lạ. Tôi bỏ đúng hai khóa metadata khỏi bảng đơn trị trong bản sao tạm, giữ `sdtContent` cùng nguyên trạng mọi ca sẵn có. Suite vẫn rc 0, **63/63** ca qua và **231/231** mutant trong bảng bị giết. Đây là khoảng trống kiểm thử §3, hạng P2 theo A7/B7, vì guard trên head có mặt nhưng bộ ca không phát hiện khi guard biến mất. [Bảng đơn trị](../scripts/tl_core/llm_route.py#L631) · [Ca r23](../scripts/tl_core/llm_route_test.py#L1645) · [Mutant r23](../scripts/tl_core/llm_route_test.py#L1859)

**Đề xuất.** Dùng ca chỉ vi phạm đúng một trường mỗi lần và đột biến bỏ đúng kiểm trường đó. Giữ đối chứng wrapper hợp lệ và ca hai `sdtContent` sẵn có.

| Lớp | Hạng cao nhất mở | Lịch sử và phép đóng |
| --- | --- | --- |
| `docx-khoang-trang-sau-loc` | P1 · Z1 | W2 → X1 → Y1 → Z1. Dùng một phép phân loại đủ miền cho run gạch/xóa/chuyển đi, với đối chứng giữ phân cách thuần và bỏ trọn mẩu có ký hiệu/chữ. |
| `docx-so-hien-thi` | P1 · Z2 | A2/B2/G1/J1/V2/W5 → X2 → Y2 → Z2. Đóng tính duy nhất từ chọn part tới XML trường đơn trị; giữ đối chứng A5. |
| `ranh-gioi-khoan` | P2 · Z3 | K1 #1514/V4/W4 → X3 → Y3 → Z3. Hai biểu hiện K1 đã đóng. Đo nhãn đa cấp còn đọc được cùng đối chứng khoản đúng một dòng. |
| `docx-test-doc-lap` | P2 · Z4 | A7/B7/C6/D4/E5/F5/G5/H3/J4 → Z4. Kế thừa nghĩa vụ từng chốt có ca đích và mutant riêng. Đóng bằng ca metadata riêng và đối chứng wrapper hợp lệ. |
| `docx-markup-du-thao` | Trong giới hạn đã duyệt | V1/W1/W3 và phần số hiệu W2. Strict được truyền. Các giới hạn của bộ đọc dùng chung được chủ kho chấp nhận trong §2.21–§2.23. |

Có **0 P0, 2 P1, 2 P2, 0 P3** trên bốn lớp còn mở. Ba lớp còn mở từ lượt 22 đã đóng các biểu hiện cụ thể được báo, nhưng vẫn có đường cùng nguyên nhân. Lớp kiểm thử có phép đột biến r23 cho thấy khoảng trống riêng. Giữ nguyên trần 23/23 của lượt này. Điều kiện merge theo ADR-0060 M1 chưa đạt. [Protocol §8.3](../docs/PROTOCOL_DA_PHIEN.md#L812) · [ADR-0060 M1–M2](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32) · [ADR-0062](../docs/adr/0062-adr-0060-mac-dinh-va-dong-bang-adr-0054.md#L13)

## Kết quả test và đột biến

Log và mã thoát ở `/tmp/wp1525-r23-codex.RuXr5VlP/`. `head-clean` và `base-clean` là clone cục bộ detached ở hai OID đã nêu, cùng `core.abbrev=7`. Các phép đo tắt bytecode Python. Đột biến bổ sung chạy trong bản sao tạm riêng.

| Lệnh | Trạng thái | Mã thoát và bằng chứng dương |
| --- | --- | --- |
| `python scripts/tl_core/llm_route_test.py` | `passed` | rc 0, **63/63** ca, **231/231** mutant bị giết, trong đó **134/134** mang tiền tố `wp1525_`. `route.log`. |
| `python scripts/tl.py --deterministic workflow-audit --strict --json` | `passed` | rc 0, `ok=true`, 194 lệnh, 26 card, 11 nhóm, 60 task, 0 lỗi và 0 cảnh báo. `audit.log`. |
| `python scripts/tl.py --deterministic golden-test --json` | `passed` | rc 0, **20/20** ca, **20/20** bản chiếu ổn định. **19/20** byte thô ổn định. `hygiene_sweep_fixture` chỉ biến động ở `snapshot_age_s`, `diff={}` và không có biến động thô ngoài khai báo. `golden.log`. |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | `passed` trên checkout head sạch | rc 0, `ok=true`, **187/187** tệp, danh sách sai/thiếu/thừa rỗng, hash gói kỳ vọng và thực tế cùng `e816e6f7122b7c103a3cc5717017863011f3fcd8bbded191aaef30f3685c7e38`. Checkout ghi verdict có rc 2, chỉ báo thừa `.review/VERDICT.md`. `clean-release.log`, `release.log`. |
| `python ops/lease_publish.py check --root . ops/leases/llm-khoan-docx-r23-g1-claude.yaml` | `passed` cục bộ | rc 0, “ĐĂNG ĐƯỢC”, Issue #1525, đúng base, hết hạn 19:01 UTC. Hai lớp GitHub của lệnh được báo riêng ở mục Không đo được. `lease.log`. |
| `python scripts/tl.py --deterministic determinism-audit --strict --json` | `passed` | rc 0, **15/15** phép với `ok=true`. `clean-determinism.log`. |
| `python scripts/tl.py --deterministic doc-claims-check --strict --json` | `failed` ở cả head và base | Mỗi bên rc 2, 131 tệp, 410 advisory, cùng một cờ cứng `SHA_NOT_A_COMMIT` ở protocol dòng 1680. OID `9941d8af52aeede1c78ea4e232fbe9a8d5272033` vắng trong bản sao shallow, `git cat-file -t` rc 128. Mảng `flags` giống nhau. `clean-doc-claims.log`, `base-doc-claims.log`. |
| Ghim/probe Ruff qua `loi_ruff_ci()` của `.claude/dev/ci_dang_ky_test.py` | `passed` | rc 0, `RUFF_CONTRACT 3 []`. `ruff-contract.log`. |
| `python -m ruff check --no-cache --select F --output-format json scripts/tl.py` | `failed` tuyệt đối, tiêu chí delta đạt | Ruff 0.15.15, rc 1 ở mỗi SHA. Hai bên cùng **12 F821, 0 F401**. Hai JSON sau chuẩn hóa đường dẫn trùng nhau. `clean-ruff.log`, `base-ruff.log`. |
| `git diff --check` cho bản vá r23 và toàn packet #1525 | `passed` | rc 0 trên cả `39f2f88..HEAD` và `fcb12b3..HEAD`. |
| `git diff --check` cho toàn PR và dải kế thừa #1514 | `failed` trên cả hai dải | rc 2, cùng ba khoảng trắng cuối dòng trong verdict #1514 lượt 8. |

Harness có sẵn chỉ đếm một mutant bị giết nếu neo thay khớp một lần và ca đích ném `TinHieuChotCa`. R23 có 11 khai báo mutant mới hoặc đổi neo thuộc Y1–Y3, tất cả bị giết. [Bảng mutant](../scripts/tl_core/llm_route_test.py#L1859) · [Harness](../scripts/tl_core/llm_route_test.py#L2145)

| Mục | Đối chứng và đột biến |
| --- | --- |
| Y1 | `wp1525_gach_doc_ruot_rieng` khôi phục phép đọc từ `chu_run`; ca dương phần ruột có `delText` và tab bắt việc giữ sai phân cách. |
| Y2 | `wp1525_sdt_nhan_con_la`, `wp1525_style_trung_ghi_de` và `wp1525_body_khong_don_tri` chết ở `ca_cau_truc_docx_chan`. Đột biến thêm trên bản sao tạm chỉ bỏ kiểm trùng `sdtPr`/`sdtEndPr`. Suite ở bản sao vẫn rc 0, 63/63 ca qua, 231/231 mutant trong bảng bị giết. `mutant-sdt-meta.patch`, `mutant-sdt-meta.log`. |
| Y3 | Bảy mutant chốt nhãn thô khóa nhánh ngoặc kín, chấm/ngoặc, gạch, thập phân đa cấp, đệm ngang, chữ hoa và chữ lặp. `ca_khoan_mat_so_co_diem_dat` giữ hai đối chứng từ ghép và chữ viết tắt. |
| K1 #1514 | `ca_wp1514_luot9` có nguồn có số/mất số với điểm, kể cả mọi dòng kết dấu chấm. `wp1525_tho_nhan_diem` bị giết ở đây. `ca_ranh_gioi_luot4` có ca tiếp dòng mở bằng “là” ở nguồn có số. [Điểm](../scripts/tl_core/llm_route_test.py#L1225) · [Tiếp dòng](../scripts/tl_core/llm_route_test.py#L827) |
| Số Word | `ca_cau_truc_docx_dat` đo khởi tạo từ `start`, `startOverride` khác `start` (5 → 1), cấp con đặt lại ở khoản sau và đối chứng nhiều cấp. Các ca âm đo danh sách khác, cấp nhảy và trần số. [Ca dương](../scripts/tl_core/llm_route_test.py#L1307) · [Ca âm](../scripts/tl_core/llm_route_test.py#L1553) |

### Selftest và đối chứng base

| Lệnh và cây | Trạng thái | Mã thoát và kết quả |
| --- | --- | --- |
| `python scripts/tl.py --selftest` · head trong checkout verdict | `failed` | rc 1, **1773/1790**, transport **12/12**. Ca CLI DOCX đạt. `selftest.log`. |
| `python scripts/tl.py --selftest` · head sạch | `failed` | rc 1, **1774/1790**, transport **12/12**. Ca CLI DOCX `r1525_llm_khai_niem_tep_docx_cau_truc` đạt. `clean-selftest.log`. |
| `python scripts/tl.py --selftest` · base sạch | `failed` | rc 1, **1773/1789**, transport **12/12**. `base-selftest.log`. |

So tập ID đỏ giữa hai cây sạch trả rc 0. Hai bên có cùng 16 ca đỏ, gồm 14 ca thuộc `r973_bootstrap_*`, `wp433_*`, `wp727_tl_gws_refresh` trong môi trường có `/tmp/.git` rỗng, và hai ca `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim`, `r268_l2_trichotomy_theo_trang_thai_object`. Ca DOCX là phần tăng duy nhất trong tập đạt. `wp44_release_bundle_topology_under_200` chỉ đỏ ở checkout có verdict và đạt trên head sạch. Delta lỗi tự kiểm giữa hai cây sạch là 0. Gate N/N của §5 vẫn đỏ trong môi trường này.

| Hiện vật | SHA-256 |
| --- | --- |
| `route.log` và `mutant-sdt-meta.log` | `bb7d0ec103266b33b19826c1aa23ed6b71bee6d5314c382115d2c115bba9d57e` |
| `clean-release.log` | `3715727945ba296b38d9eb2598852e58545a914baf3d1d15f082c6a0abeb45c1` |
| `clean-selftest.log` | `20d3d40db3e3d3724f540eb1d21a4147034062e7d3fbf2a8a500fc5ed47fb6f0` |
| `base-selftest.log` | `24bd1d6fe1958fbec9b7ce0b11e8b878c9251fd774c7802cda6846fbe0ba2935` |

## Không đo được

- Z1–Z3 là findings từ đọc mã và, với Z2, đọc cách tra tên trong `zipfile` trên máy. Ca đầu-cuối cho các hình dạng mới và cách Word sửa hoặc từ chối gói có part trùng vẫn chưa được đo. Z4 có đối chứng đột biến thực thi bằng suite sẵn có.
- Đối chiếu §2.5 thấy bộ đọc đã nhận bookmark, comment, perm, hyperlink, content control, tab và ngắt trang/cột cuối đoạn trong phạm vi nêu. Bảng, ngắt mềm, trường, ký hiệu, hình, chú thích và phần tử `mc:` nằm trong giới hạn đã công bố. Chưa có bằng chứng trong corpus/fixture sẵn có về một phần tử phổ biến của export Word/Google Docs bị chặn oan ngoài các giới hạn ấy. Tần suất trên bản export thực chưa được đo. [Danh sách trong mã](../scripts/tl_core/llm_route.py#L614) · [Hướng dẫn](../docs/GOI_AGENT_DA_NEN.md#L390)
- `skipped`: hai lớp GitHub của lệnh lease cục bộ, gồm đo Issue/PR và dò comment. `not_run`: GitHub/CI từ xa, model thật và Windows bản địa. Windows là `required` theo ADR-0060 M3 vì diff toàn PR đổi dòng Python chứa `encoding=`. Các phép kiểm ở trên là trên Linux. [ADR-0060 M3](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L43) · [Dòng đổi](../scripts/tl_core/ops_misc.py#L3061)
- Repo nguồn Executor và ref GitHub hiện tại nằm ngoài phạm vi quan sát. Biên nhận terminal của launcher, gồm mã thoát con và hash stdout/verdict ổn định, chỉ có thể chốt sau khi lượt review kết thúc. [Protocol §8.1](../docs/PROTOCOL_DA_PHIEN.md#L770)

## Đọc lại checkout và kết luận

`git rev-parse HEAD 'HEAD^{tree}'` trùng ở hai mốc. Diff binary worktree và index rỗng. Hai thư mục ignored do test sinh được chuyển ra scratch. Readback cuối chỉ có `.review/VERDICT.md` mới và `.codex/` ignore đã có từ đầu. Diff tracked và index trên hai clone đối chứng cũng rỗng. Đây là kết quả quan sát ở đầu và cuối lượt. [Protocol §8.2](../docs/PROTOCOL_DA_PHIEN.md#L797)

Điều kiện merge chưa đạt với hai P1 và hai P2 còn mở. Selftest N/N, doc-claims strict và CI/Windows exact head cũng chưa có bằng chứng đạt. Lượt này là lời gọi 23/23 theo lease r23. [Đặc tả §5](../ops/specs/llm-khoan-docx-r23.md#L329) · [ADR-0060](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32)

P2_mo: 2

VERDICT: REQUEST_CHANGES
