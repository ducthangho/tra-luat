# Verdict packet #1525 r43 lượt 43 — Codex

reviewed_sha: b68bdeaff3c9de6768450f096def34f3be3da109
reviewed_tree: cf422b69355ef81407ee63aa2bd5f09f5d05cf96

Checkout detached đúng SHA do prompt giao. Blob và bản cục bộ của đặc tả r43 trùng `spec_hash` của lease g1.

## Xác minh đầu vào

- Packet #1525, r43/g1, Review Class `sensitive`. Executor theo lease là `claude / claude_code / machine/local`, họ `claude`. Reviewer là `openai_codex / codex_cli / machine`, họ `openai`, run `9fffd6c59aeb423fbee3ca8d05ca3fb7` theo hồ sơ launcher. Sandbox `workspace-write`, mạng hạn chế, Linux x86_64, Python 3.13.18, Git 2.43.0, CLI 0.172.0 và `core.abbrev=7`. [Lease r43](../../../../../ops/leases/llm-khoan-docx-r43-g1-claude.yaml) · [Run](run.json)
- Baseline nghiệm thu `64b7f2c14776d5d0e1d34a6be4725490956f5bec`, tree `0cc14e79cecd2ce44bc4dc6cff92cadb31fd7ee4`. Mốc bàn giao #1514 `fcb12b3873c3bec2c339029136243ed2c804ce05`, mốc diff toàn PR `695916ea3bfffdd7b2e8fcb94b0740b3c421fe70`, và đầu r42 để đo bản vá `7bd28c3c64cdd685334171c81976d12652cbb075`. Commit merge `8afb0c7` có hai cha `c671163` và `695916e`. Trạng thái chưa push lấy từ prompt. Ref tracking trong checkout được giao trỏ ứng viên cục bộ, vì vậy chỉ đủ chứng minh mốc local.
- Nguồn đặc tả theo bàn giao là `b68bdeaff3c9de6768450f096def34f3be3da109:ops/specs/llm-khoan-docx-r43.md`, blob `884b0d40dcc902d3eb860561cc7b6d83fae8dc2a`. Blob và tệp checkout cùng SHA-256 `11f31f1dcbf79a3b908a194e176608df019fffde556e064493933f21fbeebbe0`, khớp lease. SHA-256 của toàn bộ prompt `ca0c393d04216bdecd98f3e765d06cea21399a1e32d1b425eb96a90c15f9c72e` khớp run và checkpoint. Lease hết hạn `2026-11-27T07:46:00Z`. Theo hồ sơ giao việc, đây là lời gọi thứ 44/45, gồm lần gọi thêm ở r34 và lần bị ngắt ở r35. [Đặc tả r43](../../../../../ops/specs/llm-khoan-docx-r43.md) · [Prompt](PROMPT.md) · [Checkpoint](#nhat-ky-scratch)

## Đối chiếu lượt 42 và đặc tả r43

Lượt 42 review trên `7bd28c3c64cdd685334171c81976d12652cbb075`, tree `bdc44e79ff5940897a2dbe5c41ba54630cc018a1`. Các trạng thái dưới đây dựa vào diff, mã trên chính r43, số liệu Git và các ca có sẵn của ứng viên. [Verdict và hint lượt 42](../../../../../ops/acceptance/llm-khoan-docx/r1/review-42-codex/VERDICT.md)

| Mục | Trạng thái | Bằng chứng |
| --- | --- | --- |
| Lượt 42 `ranh-gioi-khoan`, §2.38–§2.45 | **ĐÃ VÁ THẬT** trong miền đã khai. | `_quet_trang_thai` phát trạng thái trước ký tự, sự kiện đóng lẻ/lồng và trạng thái cuối. `_dong_mo_ho` chỉ kiểm ký tự, sự kiện và trạng thái cuối. `_quet` chiếu sang `_tu_noi`. `_mo_dau_nhieu_ve` dùng cùng span và mốc từ nối, với phép đếm ngoặc nằm trong nháy đầu phục vụ nhận nhãn theo hint r42. Ca r43 khóa nháy thẳng trong ngoặc, trạng thái cuối và cả phân đoạn lẫn phép so cho `là` + đệm + dấu. Hai phía miền nhãn nhiều vế và cảnh báo nhãn số trùng số khoản xuất hiện trong `PHAM_VI_KIEM`. [Đầu dòng](https://github.com/ducthangho/tra-luat/blob/b68bdeaff3c9de6768450f096def34f3be3da109/scripts/tl_core/llm_route.py#L587) · [Bộ quét chung](https://github.com/ducthangho/tra-luat/blob/b68bdeaff3c9de6768450f096def34f3be3da109/scripts/tl_core/llm_route.py#L1785) · [Phạm vi](https://github.com/ducthangho/tra-luat/blob/b68bdeaff3c9de6768450f096def34f3be3da109/scripts/tl_core/llm_route.py#L1679) · [Ca có sẵn](https://github.com/ducthangho/tra-luat/blob/b68bdeaff3c9de6768450f096def34f3be3da109/scripts/tl_core/llm_route_test.py#L1954) |
| Lượt 42 `can-tai-nguyen-doc-nguon`, ZIP, §2.37–§2.45 | **ĐÃ VÁ THẬT** hai biểu hiện ZIP của lượt 42. | Tiền kiểm đếm entry thật trên cùng handle, từ chối ZIP64, codec ngoài stored/deflate và cờ mã hóa trước `ZipFile`. Lỗi mở gói và mở/đọc member ở biên `_bien_zip`, còn parser chạy bên ngoài. Ca có sẵn từ chối codec/cờ trước một `ZipFile` stub và đo deflate hỏng. [Tiền kiểm](https://github.com/ducthangho/tra-luat/blob/b68bdeaff3c9de6768450f096def34f3be3da109/scripts/tl_core/llm_route.py#L1401) · [Biên đọc](https://github.com/ducthangho/tra-luat/blob/b68bdeaff3c9de6768450f096def34f3be3da109/scripts/tl_core/llm_route.py#L852) · [Ca ZIP](https://github.com/ducthangho/tra-luat/blob/b68bdeaff3c9de6768450f096def34f3be3da109/scripts/tl_core/llm_route_test.py#L2217) |
| Lượt 42 `can-tai-nguyen-doc-nguon`, extract và oracle | **VÁ MỘT PHẦN** toàn lớp. | Đã chuyển khởi tạo bộ đệm/sổ lên trước spawn và sửa đúng trường hợp `start()` thứ hai thất bại trước khi tạo luồng. Ca r43 kiểm đúng ngoại lệ gốc và kill/wait. `ident` vẫn chưa chứng minh có thể join khi `start()` bị ngắt giữa chừng, và lỗi khởi tạo luồng vẫn thoát biên CLI. Probe `ps` đã có giới hạn thời gian và đo trên PID đang sống, còn mơ hồ khi đọc đích. [Thu hồi](https://github.com/ducthangho/tra-luat/blob/b68bdeaff3c9de6768450f096def34f3be3da109/scripts/tl_core/llm_route.py#L1982) · [Oracle](https://github.com/ducthangho/tra-luat/blob/b68bdeaff3c9de6768450f096def34f3be3da109/scripts/tl_core/llm_route_test.py#L2094) · [Biên CLI](https://github.com/ducthangho/tra-luat/blob/b68bdeaff3c9de6768450f096def34f3be3da109/scripts/tl_core/ops_misc.py#L3095) |
| Lượt 42 `lien-ket-bang-chung-review`, §2.45 | **VÁ MỘT PHẦN**. | Đường dẫn tệp có thật từ thư mục archive. Cả hai `run.json` có run ID và head đúng, hai `PROMPT.md` khớp băm trong run. Link mã lại mở checkout hiện tại ở số dòng của revision cũ và neo scratch chưa có đích trong hai verdict. [Chỉ mục](../../../../../ops/acceptance/llm-khoan-docx/r1/LIEN_KET.md) · [Lượt 41](../../../../../ops/acceptance/llm-khoan-docx/r1/review-41-codex/VERDICT.md#L50) · [Lượt 42](../../../../../ops/acceptance/llm-khoan-docx/r1/review-42-codex/VERDICT.md#L41) |
| §1, §2.2–§2.3, K1 của #1514 | **ĐÃ VÁ THẬT** cho hai ngả K1 đã giao. | Điểm có dấu đầu dòng kiểu K1 làm từ chối Điều. Ở nguồn có số, dòng tiếp mở bằng “là” không thể nhập vào khoản trước vì thiếu số. Ở nguồn mất số, một dòng chỉ còn từ nối ở đầu không thể qua đối chiếu hai vế. Mỗi khoản thô giữ một dòng, số buộc liên tục, kiểm nguyên văn theo vị trí và luôn trả `can_nguoi_duyet: true`. [K1](../../../../../ops/acceptance/llm-ranh-gioi-khoan/r1/review-10-codex/VERDICT.md#L35) · [Phân đoạn](https://github.com/ducthangho/tra-luat/blob/b68bdeaff3c9de6768450f096def34f3be3da109/scripts/tl_core/llm_route.py#L1689) · [Phép so](https://github.com/ducthangho/tra-luat/blob/b68bdeaff3c9de6768450f096def34f3be3da109/scripts/tl_core/llm_route.py#L1865) · [CLI](https://github.com/ducthangho/tra-luat/blob/b68bdeaff3c9de6768450f096def34f3be3da109/scripts/tl_core/ops_misc.py#L3140) |
| §2.1, §2.4–§2.18 về vùng Điều, điểm gõ tay, fallback và câu dẫn | **HẾT ĐỐI TƯỢNG** với các lỗi cắt vùng, đếm qua bảng và nhập điểm gõ tay của hợp đồng cũ. **ĐÃ VÁ THẬT** ở các cửa còn hiệu lực. | Tệp chỉ chứa một Điều, tiêu đề nguyên đoạn là nội dung đầu tiên, kiểm tới EOF. Bảng, khối lạ, tiêu đề cấu trúc trong thân và đoạn không số sau khoản đầu dừng. Trước khoản đầu, chỉ vắng câu dẫn hoặc một câu dẫn khớp toàn đoạn. DOCX thiếu số tự động trả lỗi, đường `KhongCauTruc` đã bỏ. [Vùng Điều](https://github.com/ducthangho/tra-luat/blob/b68bdeaff3c9de6768450f096def34f3be3da109/scripts/tl_core/llm_route.py#L1557) · [Câu dẫn](https://github.com/ducthangho/tra-luat/blob/b68bdeaff3c9de6768450f096def34f3be3da109/scripts/tl_core/llm_route.py#L1663) · [Định tuyến CLI](https://github.com/ducthangho/tra-luat/blob/b68bdeaff3c9de6768450f096def34f3be3da109/scripts/tl_core/ops_misc.py#L3037) |
| §2.4, §2.10–§2.15, §2.22–§2.27 về số Word và part | **ĐÃ VÁ THẬT** ở các biểu hiện lịch sử trong miền nhận. | Part lấy từ quan hệ đúng URI. `start` mặc định 0, `startOverride` áp đúng cấp, bộ đếm theo numId với chốt 0–999, chặn nhảy cấp và xóa các bộ đếm con khi có mục cha. Vùng hợp lệ dùng một numId cho khoản lẫn điểm. Giữ nhãn chữ Word lặp một chữ, khóa cú pháp nhãn, đòi đúng số liên tục từ 1. `lech_nguyen_van` chỉ tìm từ nối trong đoạn mở khoản và so trọn thân cùng dòng điểm. [Định nghĩa](https://github.com/ducthangho/tra-luat/blob/b68bdeaff3c9de6768450f096def34f3be3da109/scripts/tl_core/llm_route.py#L932) · [Nhãn](https://github.com/ducthangho/tra-luat/blob/b68bdeaff3c9de6768450f096def34f3be3da109/scripts/tl_core/llm_route.py#L1121) · [Bộ đếm](https://github.com/ducthangho/tra-luat/blob/b68bdeaff3c9de6768450f096def34f3be3da109/scripts/tl_core/llm_route.py#L1540) · [Đường so](https://github.com/ducthangho/tra-luat/blob/b68bdeaff3c9de6768450f096def34f3be3da109/scripts/tl_core/llm_route.py#L1881) |
| §2.5–§2.8, §2.13, §2.19–§2.35 về markup/style/ký tự | **ĐÃ VÁ THẬT** ở các biểu hiện lịch sử được khóa. | Đọc XML gốc, giữ `ins/moveTo`, bỏ `del/moveFrom` và gạch có hiệu lực. Có chốt mốc move không cân, sửa dấu đoạn, hai thuộc tính gạch riêng, kiểu style, đơn trị, mc, khoảng trắng hiệu lực và ký tự gốc mọi đoạn. [Style](https://github.com/ducthangho/tra-luat/blob/b68bdeaff3c9de6768450f096def34f3be3da109/scripts/tl_core/llm_route.py#L1033) · [Duyệt run](https://github.com/ducthangho/tra-luat/blob/b68bdeaff3c9de6768450f096def34f3be3da109/scripts/tl_core/llm_route.py#L1278) · [Mốc move](https://github.com/ducthangho/tra-luat/blob/b68bdeaff3c9de6768450f096def34f3be3da109/scripts/tl_core/llm_route.py#L1507) |
| Giới hạn §2.21 U2, §2.22 V3, §2.23 W1/W3 và W2 phần số hiệu | **GIỚI HẠN ĐÃ KHAI**. | Kiểm `--markup-strict`, cắt theo Điều của tầng extract, làm sạch trước cache, dự thảo qua style và tab/ngắt theo phạm vi đã cấp. Chốt CAP giữ nguyên. Giới hạn nhãn dính thân, nhãn chỉ có đệm và nhãn số trùng khoản được loại khỏi số finding theo quyết định đã ghi. [Đặc tả](../../../../../ops/specs/llm-khoan-docx-r43.md#L279) · [Extract](https://github.com/ducthangho/tra-luat/blob/b68bdeaff3c9de6768450f096def34f3be3da109/scripts/tl_core/llm_route.py#L2064) |
| Write set và bia mộ | **KHỚP**. | Tập 229 path băm `2027465b22a60b467696c3e4c70d49a502fa25d8e3d51d124e3eeed0056d62db`. Cả 13 path diff r43 nằm trong tập. Diff toàn PR có 272 path, 47 path ngoài tập đều là hồ sơ #1514, có từ mốc bàn giao `2c91832` và giữ nguyên từ mốc đó. Đối chiếu hai khóa cho 43 cặp #1514 r9 ↔ #1525 r1 ↔ … ↔ r43 cho đủ 86 dòng khớp. [Lease](../../../../../ops/leases/llm-khoan-docx-r43-g1-claude.yaml) · [Phép đo](#nhật-ký-scratch) |

### Đối chiếu các biểu hiện lịch sử

| Lượt #1525 | Đối chiếu trên r43 |
| --- | --- |
| 1–6, A1–A8, B1–B8, C1–C7, D1–D6, E1–E6, F1–F6 | **HẾT ĐỐI TƯỢNG** cho điểm cắt, duyệt bảng để đếm, nhánh lùi và yêu cầu nhận điểm gõ tay. **ĐÃ VÁ THẬT** ở đường đọc XML, từ nối, số Word, wrapper, chốt/ca và hướng dẫn trong miền hiện hành. Strict được công bố là giới hạn có chẩn đoán. Lỗi regex ở `docx_markup.strip_markup` hết đường chạy trong DOCX của Packet này. |
| 7–12, G1–G6, H1–H5, J1–J5, K1–K4, L1–L6, M1–M2 | **ĐÃ VÁ THẬT** các cửa còn chạy. Kiểm số/ID, part và rels, ngắt, trường đơn trị, cấp/style, nhãn, tiêu đề, hợp đồng ca và mã hóa được thực hiện ở nơi nêu trong bảng. G3 hết cơ chế cũ do từ chối nhảy cấp. J2 nay được chốt toàn part mc. L2/M1 dùng chốt tiền tố cả thân. |
| 13–21, N1–N3, Q1–Q2, R1–R3, S1–S3, T1–T2, U1–U2, V1–V4, W1–W5, X1–X3 | **ĐÃ VÁ THẬT** ở biểu hiện trong write set và miền mới đã khóa. U2, V3, W1/W3 và W2 phần số hiệu là giới hạn đã duyệt. Chốt ký tự và chốt đầu dòng áp trước khi công nhận phân đoạn. |
| 22–33, Y1–Y3, Z1–Z4, A1–A2, B1–B3, C1–C2, D1, E1, F1–F2, G1–G2, H1–H3, I1–I2, J1–J2 | **ĐÃ VÁ THẬT** ở các biểu hiện đã báo theo điều khoản thay thế. Giữ nguyên chốt markup, style, namespace và ngân sách. Ngữ pháp cấm nhãn cũ được thay bằng danh sách cho phép và miền đã khai. |
| 34–38 | **ĐÃ VÁ THẬT** lớp `ranh-gioi-ky-tu` và các biểu hiện nhãn một vế, nhãn điểm gõ tay và nhãn nhiều vế theo miền đã duyệt. §2.39 khóa cảnh báo số trùng. Bằng chứng lượt 35 là hồ sơ tạm của run bị ngắt. Lớp ngân sách còn phần extract/oracle theo finding dưới đây. |
| 39–41 | **ĐÃ VÁ THẬT** locator ZIP64 tuyệt đối, một hạn chót, biên codec ZIP, hai P3 `huong-dan-docx` và `ghi-chu-write-set`, cùng lớp `ve-sinh-diff-ho-so-review` (đã đo trên toàn PR). Chốt nhóm POSIX đã đo ở nhánh procfs. Oracle `ps` và đường lỗi vòng đời vẫn thuộc lớp đang mở. Lớp ranh giới dùng chung bộ chuyển theo §2.45. |

Chốt K1 nằm trong phép so đầu ra sau lời gọi model. Khi chốt từ chối, kết quả có lệch, CLI trả rc 5 và giữ tệp `--out` đã xác minh trước đó. [Thứ tự gọi và so](https://github.com/ducthangho/tra-luat/blob/b68bdeaff3c9de6768450f096def34f3be3da109/scripts/tl_core/llm_route.py#L2094) · [Ghi đầu ra](https://github.com/ducthangho/tra-luat/blob/b68bdeaff3c9de6768450f096def34f3be3da109/scripts/tl_core/ops_misc.py#L3146)

Mã và các ca sẵn có chưa xác lập cửa P1 để nhận bỏ, gộp, cắt, tráo khoản hay chữ bị bỏ trong miền hỗ trợ. Allowlist DOCX xử lý content control nội dòng/khối, hyperlink, bookmark/comment, tab, ngắt trang/cột và nối không ngắt. Trường, hình, bảng và chú thích thuộc dạng đã công bố từ chối. Wrapper hướng chữ `w:dir`/`w:bdo` rơi vào cửa phần tử lạ. Mức phổ biến của chúng trong bản export văn bản tiếng Việt chưa được đo, nên chưa xác lập P2 chặn oan ngoài miền đã công bố. [Danh sách phần tử](https://github.com/ducthangho/tra-luat/blob/b68bdeaff3c9de6768450f096def34f3be3da109/scripts/tl_core/llm_route.py#L797) · [Hướng dẫn DOCX](https://github.com/ducthangho/tra-luat/blob/b68bdeaff3c9de6768450f096def34f3be3da109/docs/GOI_AGENT_DA_NEN.md#L391)

## Findings THEO LỚP

### Lớp `can-tai-nguyen-doc-nguon` [P2] — `scripts/tl_core/llm_route.py:1987`

- **Bất biến.** Từ khi spawn thành công, mọi lỗi đọc nguồn phải thu hồi tiến trình, luồng và đầu ống trong ngân sách đã công bố, đồng thời giữ nguyên nguyên nhân gốc. CLI cần chẩn đoán có kiểm soát cho lỗi vận hành đã dự kiến. Oracle chỉ xác nhận PID đích đã chết khi nhận được bằng chứng đúng nghĩa.
- **Miền đã đối chiếu.** Đã đóng tiền kiểm gói/entry/ZIP64/codec và biên mở/đọc ZIP, lỗi start trước khi thread thứ hai được tạo, cùng các cửa giới hạn byte, quá hạn reader, wait và chấp nhận kết quả qua hạn đã có ca. Các cửa extract còn mở chung cơ chế sở hữu và nhận dạng trạng thái.
  1. `_cho_ket_qua` ghi thread trước `start()`. `_thu_hoi` dùng `ident is not None` làm điều kiện join, trong khi CPython 3.13.18 đặt `ident` trước khi bật `_started` và `join()` kiểm `_started`. Nếu ngắt vào khoảng `start()` đang chờ bootstrap, cleanup vẫn có thể gọi join quá sớm và thay ngoại lệ gốc. Chính cleanup cũng chưa có hàng rào riêng quanh join và kiểm trạng thái reader. Nếu thread còn bootstrap chưa có `ident`, trạng thái ấy lại bị ghi như chưa start. Phép đo hiện có gây lỗi trước khi thực sự khởi động thread thứ hai, nên qua được mà chưa khóa các trạng thái trung gian. [Ghi sổ và start](https://github.com/ducthangho/tra-luat/blob/b68bdeaff3c9de6768450f096def34f3be3da109/scripts/tl_core/llm_route.py#L2038) · [Thu hồi](https://github.com/ducthangho/tra-luat/blob/b68bdeaff3c9de6768450f096def34f3be3da109/scripts/tl_core/llm_route.py#L1996) · [Ca start](https://github.com/ducthangho/tra-luat/blob/b68bdeaff3c9de6768450f096def34f3be3da109/scripts/tl_core/llm_route_test.py#L2123)
  2. Khi một reader còn kẹt, `_thu_hoi` không đóng cả hai ống, kể cả ống chưa giao hay đã an toàn. Nếu lỗi được CLI bắt, dòng in `{e}` không hiện `__notes__` của `add_note`. Ngược lại, `RuntimeError` khi start thật không thuộc các loại lỗi CLI đang bắt, dù ca lớp đã kiểm đúng nguyên nhân. Các cửa này đều trước model và nằm ngoài các giới hạn đã duyệt về nội dung đầu ra `tl extract`. [Đầu ống](https://github.com/ducthangho/tra-luat/blob/b68bdeaff3c9de6768450f096def34f3be3da109/scripts/tl_core/llm_route.py#L2007) · [Chẩn đoán](https://github.com/ducthangho/tra-luat/blob/b68bdeaff3c9de6768450f096def34f3be3da109/scripts/tl_core/ops_misc.py#L3095)
  3. Oracle `ps` đã có probe và timeout. Với PID đích, `rc=0` nhưng không có trạng thái, hoặc `rc=1` kèm chẩn đoán và stdout rỗng, vẫn biến thành `X` và được tính là đã mất. Lỗi gọi `ps` hoặc timeout chưa được mô hình hóa cùng trạng thái chưa đo. Probe trên PID sống xác nhận lệnh dùng được lúc probe. Nó chưa xác nhận một lần truy vấn đích lỗi đã tìm thấy PID vắng. [Oracle](https://github.com/ducthangho/tra-luat/blob/b68bdeaff3c9de6768450f096def34f3be3da109/scripts/tl_core/llm_route_test.py#L2103)
- **Hạng P2.** Đây là cửa lỗi có kiểm soát và bằng chứng thu hồi trước model. Đọc mã cho thấy vẫn còn đường che nguyên nhân, rò đầu ống hoặc kết luận oracle xanh thiếu chứng cứ. Các biểu hiện không chứng minh đã nhận sai nguyên văn.
- **Hint patch.** Dùng một sổ sở hữu ở biên `_chay_gioi_han` cho mọi lối thoát sau spawn. Mỗi đầu ống mang trạng thái chưa giao, đang khởi động, reader đã nhận hoặc đã xong. Trả thông tin thu hồi qua cùng một điểm và giữ nguyên ngoại lệ gốc qua lỗi thứ cấp. Giới hạn đã khai trên Windows vẫn áp dụng.
  ```text
  _chay_gioi_han:
      tạo sổ đầu ống trước Popen
      try:
          _cho_ket_qua với sổ, xác nhận start/handoff riêng từng reader
      except BaseException as loi_goc:
          báo_cáo = _thu_hoi(process, sổ, ngân_sách)
          gắn báo_cáo và giữ nguyên loi_goc
          ánh xạ lỗi start/wait vận hành tại biên extract, giữ nguyên ngắt
  _thu_hoi:
      kill/reap trong hạn
      chờ handoff đang khởi động trong hạn, join reader đã sẵn sàng
      thu lỗi cleanup vào báo_cáo, tiếp tục thu hồi các mục khác
      đóng riêng từng ống đã an toàn, báo các đầu ống chưa thu hồi
  oracle:
      trả CÒN_SỐNG, ĐÃ_KẾT_THÚC, hoặc KHÔNG_ĐO_ĐƯỢC
      chỉ ĐÃ_KẾT_THÚC thoả ca thu hồi
  ```
  Sổ gắn với đầu ống phủ phần khởi tạo chưa xong, đang đọc và đã đọc xong. Biên CLI có thể in báo cáo cùng lỗi vận hành nguồn. Oracle dùng một tiêu chí cho probe/truy vấn, kiểm định dạng và quy ước PID vắng của nền.
- **Hint test.** Mở rộng ca sẵn theo trạng thái start lần đầu, lần thứ hai, ngắt trong bootstrap, lỗi join/wait và reader giữ ống. Đối chứng thu hồi thành công phải giữ nguyên lỗi gốc, đóng từng đầu ống an toàn, báo đầu còn giữ và giữ deadline. Oracle cần phủ PID sống, chết hoặc zombie, không có trạng thái, lỗi lệnh, rc kèm stderr và timeout. Mutant nhập lại các trạng thái, để cleanup che lỗi gốc hoặc đổi lỗi oracle thành PID vắng phải đỏ tại ca đích.
- **Giới hạn.** Hướng dẫn đã khai Windows chỉ thu hồi tiến trình trực tiếp. Oracle `ps` và pha ngắt bootstrap trên các nền là phần chưa đo động của lớp.

### Lớp `lien-ket-bang-chung-review` [P3] — `ops/acceptance/llm-khoan-docx/r1/LIEN_KET.md:7`

- **Bất biến.** Liên kết hồ sơ cần mở đúng source tại `reviewed_sha`, đúng run/prompt đồng gói, hoặc đích chú giải có thật cho bằng chứng chỉ tồn tại trong scratch.
- **Miền và bằng chứng.** `realpath -e` tìm được đích mã, `run.json` và `PROMPT.md` từ các thư mục lượt 41–42. Hash prompt và run ID khớp. Link mã vẫn động theo checkout. Link `llm_route.py#L1776` ở lượt 42 mở dòng rỗng trên ứng viên r43, trong khi `git show 7bd28c3:scripts/tl_core/llm_route.py` xác nhận dòng 1776 ở SHA được review là `def _dong_mo_ho(ln) -> bool:`. Link `#L604` của lượt 41 cũng dịch từ nhánh kiểm `trich` sang nhánh nhận ký tự mở ở HEAD. Các link `#nhat-ky-scratch` trong hai verdict cùng trỏ tới anchor không tồn tại. Đích nội bộ có thật nhưng lệch phiên bản và đích chú giải vắng thuộc cùng lớp lưu hồ sơ. Đường dẫn gốc cũ của các lượt trước đã có chỉ mục chuyển đổi. [Chỉ mục](../../../../../ops/acceptance/llm-khoan-docx/r1/LIEN_KET.md) · [Lượt 41](../../../../../ops/acceptance/llm-khoan-docx/r1/review-41-codex/VERDICT.md#L50) · [Lượt 42](../../../../../ops/acceptance/llm-khoan-docx/r1/review-42-codex/VERDICT.md#L16)
- **Hạng P3.** Người đọc vẫn đọc được SHA, trạng thái và số liệu trong verdict, nhưng việc mở hiện vật kiểm chứng dễ dẫn tới đoạn mã khác hoặc đích vắng.
- **Hint patch.** Chuẩn hóa tại bước lưu theo một hàm phân giải. `repo_path + dòng → blob tại reviewed_sha + dòng`, `run/prompt → tệp đồng gói + đối chiếu ID/băm`, `scratch → chú giải có anchor thật + đường dẫn + hash khi có`. Với bản gốc đã có mỏ neo byte, giữ nguyên blob và đưa ánh xạ vào chỉ mục đi kèm. Phép phân giải nhận cùng metadata nguồn cho mọi link, nên sửa từ gốc cả link lệch SHA và đích thiếu.
- **Hint test.** Kiểm từ đường dẫn archive, đối chiếu nội dung dòng với blob khi HEAD đã dịch dòng, xác minh run ID/prompt hash và anchor thực trong tệp. Đột biến bỏ SHA khỏi đích mã hoặc bỏ mục giải thích scratch phải đỏ. Đối chứng gồm link mã đúng blob, run/prompt đồng gói đúng và log scratch có chú giải.
- **Giới hạn.** Log lịch sử chỉ có ở scratch khi không được lưu kèm. Bản lưu cần diễn đạt điều đó ở đích chú giải để người đọc biết độ bền của bằng chứng.

### Bảng lớp mở

| Slug | Lượt/SHA gốc | Biểu hiện còn mở | Hạng cao nhất | Phép đóng lớp |
| --- | --- | ---: | --- | --- |
| `can-tai-nguyen-doc-nguon` | Lượt 42, `7bd28c3c64cdd685334171c81976d12652cbb075` | 3 | P2 | Oracle phủ trạng thái sở hữu/thu hồi và phép đo PID, giữ lỗi gốc qua biên CLI. |
| `lien-ket-bang-chung-review` | Lượt 42, `7bd28c3c64cdd685334171c81976d12652cbb075` | 2 | P3 | Readback từ archive khớp blob, run/prompt và anchor. |

Đóng **1/3** lớp mở ở lượt 42, còn **2 lớp** với **5 biểu hiện** nêu trên. Tỷ lệ hai chuyển tiếp gần nhất lần lượt là **1/3** và **1/3**, dưới ngưỡng Review Rescue Checkpoint. Lease r43 ghi dừng ở lượt 43 nếu còn P2. [Protocol §12](https://github.com/ducthangho/tra-luat/blob/b68bdeaff3c9de6768450f096def34f3be3da109/docs/PROTOCOL_DA_PHIEN.md#L1129) · [Lease](../../../../../ops/leases/llm-khoan-docx-r43-g1-claude.yaml)

## Kết quả test và đột biến

Đo trên exact SHA đã ghi ở đầu verdict. Selftest, golden và bare Ruff có đối chứng baseline. Lượt xác nhận strict release chạy trên bản sao sạch, cùng head/tree. Tệp bytecode và log đặt ở scratch hoặc tắt bằng `PYTHONDONTWRITEBYTECODE=1`. [Log và rc](#nhật-ký-scratch)

| Lệnh | Trạng thái và mã thoát | Bằng chứng |
| --- | --- | --- |
| `python scripts/tl_core/llm_route_test.py` | `passed`, rc 0 | **64/64** ca, **288/288** đột biến, gồm **191/191** `wp1525_*` trên POSIX. Harness chỉ đếm mutant khi ca đích ném `TinHieuChotCa`. Ca Điều 3 và ba đầu ra đã lưu giữ **8/8**. [Harness](https://github.com/ducthangho/tra-luat/blob/b68bdeaff3c9de6768450f096def34f3be3da109/scripts/tl_core/llm_route_test.py#L2728) · [Ca 8/8](https://github.com/ducthangho/tra-luat/blob/b68bdeaff3c9de6768450f096def34f3be3da109/scripts/tl_core/llm_route_test.py#L1160) |
| `python scripts/tl.py --deterministic workflow-audit --strict --json` | `passed`, rc 0 | `ok=true`, **201/201** leaf đăng ký, 26 card, 11 nhóm, 60 task, 194 lệnh khả dụng, 0 lỗi/cảnh báo. |
| `python scripts/tl.py --deterministic golden-test --json` | `passed`, rc 0 ở các lần chạy | `ok=true`, **20/20** ca và projection ở cả hai SHA. Lượt đầu raw **19/20** (`hygiene_sweep_fixture`). Chạy lại trong hai bản sao với TMPDIR riêng, head và base đều raw **20/20**. |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | Lượt sạch `passed`, rc 0 | `ok=true`, **187/187**, không tệp thừa, package hash `d28b0a57aae03afe8c1b33c9b32d76f0d393d9a9dd13675c2d370acfa96f74f0` khớp. Lần đầu `failed`, rc 2, extra duy nhất là `.review/VERDICT.md` đã tạo sớm theo prompt. |
| `python ops/lease_publish.py check --root . ops/leases/llm-khoan-docx-r43-g1-claude.yaml` | `passed` cục bộ, rc 0 | “ĐĂNG ĐƯỢC”, #1525, neo `64b7f2c14776`, hạn `2026-11-27T07:46:00Z`. Hai phép đọc Issue/PR và tìm comment GitHub là `skipped` theo công cụ. |
| `python scripts/tl.py --selftest` | `failed`, head rc 1, base rc 1 | Head **1774/1790**, base **1773/1789**, transport **12/12** mỗi bên. Tập 16 ID đỏ trùng byte (`cmp` rc 0), delta 0. Head lặp lại cùng số và cùng ID trong bản sao. `r1525_llm_khai_niem_tep_docx_cau_truc` và `r380_llm_khai_niem_bien_dau_vao` đều `[OK]`. |
| `python scripts/tl.py --deterministic determinism-audit --strict --json` | `passed`, rc 0 | `ok=true`, **15/15** phép kiểm. |
| `python scripts/tl.py doc-claims-check --strict --json` | `failed`, head rc 2, base rc 2 | Mỗi bên 131 tệp, 410 advisory, một cờ cứng L2 `SHA_NOT_A_COMMIT` cho `9941d8af52aeede1c78ea4e232fbe9a8d5272033`. Mảng `flags` trùng byte. `git cat-file -t` rc 128 trên kho shallow được giao. |
| Ruff pin/probe qua `loi_ruff_ci()` của `.claude/dev/ci_dang_ky_test.py` | `passed`, rc 0 | `RUFF_CONTRACT 3 []`, ba phép của hợp đồng, không lỗi. |
| `python -m ruff check --no-cache --select F scripts/tl.py` | Bare lint `failed`, head rc 1, base rc 1. Tiêu chí delta 0 đạt. | Ruff 0.15.15, **12 F821** mỗi bên, log trùng byte. |
| `python -m ruff check --no-cache --select F scripts/tl_core/llm_route.py scripts/tl_core/llm_route_test.py` | `passed`, rc 0 | Ruff 0.15.15, không có chẩn đoán ở hai tệp Python đổi trong r43. |
| `git diff --check 7bd28c3 HEAD` và `git diff --check 695916e HEAD` | `passed`, rc 0 ở cả hai | Diff r43 và toàn PR không có chẩn đoán khoảng trắng. |

Tập ID selftest đỏ có SHA-256 `6c344d8f8a71b854460d8d4badd425904bdd116177ea8b3e14bd2387a2a14505`. 14 ca thuộc các nhóm `r973_bootstrap_*`, `wp433_*` và `wp727_tl_gws_refresh` khớp các nhóm prompt nêu cho môi trường có `/tmp/.git` rỗng. Hai ca cùng đỏ còn lại là `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` và `r268_l2_trichotomy_theo_trang_thai_object`. Gate N/N vẫn đỏ.

Sáu mutant mới của r43 kiểm nháy thẳng trong ngoặc, trạng thái cuối, chính sách codec, cờ mã hóa riêng, biên lỗi đọc member và join luồng chưa start. Chúng đều bị giết. Mỗi đột biến chạy trong tệp tạm do harness hiện có tạo và phải chết bằng tín hiệu của ca đích. Ca khởi động luồng chứng minh giữ nguyên lỗi ở trạng thái được giả lập. Các trạng thái khác được ghi trong finding. [Bảng đột biến](https://github.com/ducthangho/tra-luat/blob/b68bdeaff3c9de6768450f096def34f3be3da109/scripts/tl_core/llm_route_test.py#L2321)

## Nhật ký scratch

Thư mục của lượt đo là `/tmp/wp1525-r43-review.ZpGHlUQa`. Mỗi gate có `*.log` và `*.rc`. Các tên `focused`, `workflow`, `determinism`, `lease`, `head-manifest`, `head-selftest`, `base-selftest`, `head-golden`, `base-golden`, `claims`, `base-claims` và `head-ruff*` tương ứng bảng trên. `*.paths`, `*.outside`, `lease-chain.log`, `pr.numstat` và `*-status.*` lưu phép đo phạm vi và trạng thái checkout.

- Diff r43 SHA-256 `8c8bcf687a9d50d95e3cb519cb31999ebd5408bdc01f5f45ddf4d73026b85436`.
- Diff toàn PR SHA-256 `e2e11667ffcc335842f29fdea21ca8f39c1aac384ea74392ead76e8402fe9c79`.

Các phép chạy đầu trên checkout reviewer sinh 20 tệp ignored ở thư mục fixture và trạng thái. Tôi đã chuyển đúng 20 hiện vật sinh ra sang scratch sau khi test kết thúc. Phép chạy lại sử dụng bản sao tạm. Readback checkout reviewer chỉ có `.review/VERDICT.md` untracked. HEAD/tree và diff tracked/index khớp hai mốc, SHA-256 hai diff rỗng cùng là `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. Hai bản sao thử nghiệm cũng giữ HEAD/tree và diff tracked/index rỗng. Snapshot này chứng minh trạng thái quan sát được tại hai mốc.

## Không đo được

- `not_run` với ca mới, DOCX export thực tế từ Word/Google Docs, ngắt giữa bootstrap luồng, POSIX qua nhánh dự phòng `ps`, model thật và CI/GitHub. Phần sửa đường chạy `subprocess`/nền làm native Windows thuộc `required` theo ADR-0060 M3, trạng thái `not_run` trong lượt Linux offline này. [ADR-0060 M3](https://github.com/ducthangho/tra-luat/blob/b68bdeaff3c9de6768450f096def34f3be3da109/docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L44)
- `not_measured` cho strict doc-claims trên kho object đầy đủ và tần suất phần tử Word/Google Docs ngoài allowlist. Hai lần đo strict thực tế trong kho shallow vẫn ghi `failed` theo bảng.
- Model/effort phục vụ là `KHONG_DO_DUOC` từ hồ sơ đang chạy. Mã thoát terminal của phiên review, hash stdout cuối và delivery receipt cần readback của launcher sau khi phiên kết thúc. [Hồ sơ launcher](run.json) · [Protocol §8.1](https://github.com/ducthangho/tra-luat/blob/b68bdeaff3c9de6768450f096def34f3be3da109/docs/PROTOCOL_DA_PHIEN.md#L770)

**Chưa đủ điều kiện merge.** Ngưỡng kết luận nội dung của prompt là 0 P0/P1. Ngưỡng merge của chủ kho là 0 P0–P3 và ứng viên hiện còn P2/P3. Selftest N/N và doc-claims strict còn đỏ trong môi trường đo. Bằng chứng Windows/CI trên exact head còn thiếu. Áp điều kiện dừng của lease r43 vì còn P2 ở lượt 43. [ADR-0060](https://github.com/ducthangho/tra-luat/blob/b68bdeaff3c9de6768450f096def34f3be3da109/docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32) · [Lease r43](../../../../../ops/leases/llm-khoan-docx-r43-g1-claude.yaml)

P0_mo: 0
P1_mo: 0
P2_mo: 1
P3_mo: 1
VERDICT: APPROVE

<a id="nhat-ky-scratch"></a>
## Nhật ký scratch (không lưu kèm)

Các đích sau chỉ có trong scratch của lượt review hoặc ngoài kho; bản lưu này KHÔNG mang theo chúng:

- `checkpoint.json của launcher`
