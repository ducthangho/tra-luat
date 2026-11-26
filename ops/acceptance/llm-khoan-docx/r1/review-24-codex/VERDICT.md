# Verdict packet #1525 r24 lượt 24 — Codex

reviewed_sha: b755fef46e96492019fabcd8bcd13e370a6ce9c6

tree_sha: add492453053239ad37ed5e66b04b58037c13ac9

base_sha: 64b7f2c14776d5d0e1d34a6be4725490956f5bec

provider: openai_codex

execution_surface: codex_cli

transport: machine

## Đối chiếu lượt 23 và đặc tả r24

- Checkout độc lập, detached, origin cục bộ là `ducthangho/tra-luat`. Ref có sẵn `origin/ccr-89c0d2e2-inanqb` trỏ đúng head. Base là tổ tiên của head, tree base `0cc14e79cecd2ce44bc4dc6cff92cadb31fd7ee4`. Mốc tiếp nối #1514 là `fcb12b3873c3bec2c339029136243ed2c804ce05`, mốc trước bản vá r24 là `db06b9cd52db6407c01ac92d3b26991a7fdd38e5`.
- Lease #1525 r24/g1, class khai và effective đều `sensitive`, hiệu lực 11:18–19:18 UTC ngày 26-11-2026. Đây là lượt 24/24. SHA-256 của bytes đặc tả trong Git và bản trên đĩa cùng là `bbff4c150d3a29253442ad81172508b99b3494d062752fbdc95bb8390bad162b`, khớp lease. Blob đặc tả `f969ac265e9eb4c32fa72d3414530728cefc57b9`. Kiểm **24/24** cặp bia mộ hai chiều và **25/25** hash đặc tả từ #1514 r9 qua #1525 r1…r24. Quyền đứng và ngoại lệ M5 được ghi trong đặc tả. [Lease](../ops/leases/llm-khoan-docx-r24-g1-claude.yaml) · [Đặc tả](../ops/specs/llm-khoan-docx-r24.md)
- Write set 131 đường dẫn duy nhất, hash LF `0e88f366278e01a0e0b58e097d3e764465279e6bdd14e4f3a6c15d948760f9c8`. Bản vá r24 **8/8** và toàn packet **127/127** đường dẫn nằm trong lease sau khi loại bốn tệp hồ sơ #1514 theo giao việc. Toàn PR đổi 175 đường dẫn, gồm phần kế thừa #1514. SHA-256 của ba diff theo thứ tự toàn PR / packet / r24 là `9d92fecaaa74bff258d576a353ee3f766ff354c3a2804e19a7380d57958e371b` / `112ffe460df5be915ca4dbf61dc05c0ef544729359e07f55106920deb49a30f2` / `8c704fcc64d9a5578721de691ce7710e8d49bed3ea64eada30ee4ac3eb732ef9`.
- Codex CLI 0.172.0, run `636c334fe3644d17bc3a0fecc3cb1996` qua launcher. Hash prompt `2cb432cf043252c5baa9417d9d0866346a8784532ed15c19ef49e0b2c66fd039` khớp checkpoint cùng run. Executor theo lease là `anthropic_claude / claude_code / machine/local`, phiên `session_015GtxrZQYT3Vt8PJdXrjEKg`. Linux x86_64, Python 3.13.18, Git 2.43.0, checkout shallow, `core.abbrev=7`, sandbox `workspace-write` với metadata Git checkout gốc chỉ đọc. Tên model và effort phục vụ `KHONG_DO_DUOC` từ receipt đang chạy. [Protocol §8.1](../docs/PROTOCOL_DA_PHIEN.md#L770)

| Mục | Trạng thái | Bằng chứng |
| --- | --- | --- |
| Z1 · lượt 23 · §2.26 | **ĐÃ VÁ THẬT** cho ký hiệu kèm tab trong `w:del`. **VÁ MỘT PHẦN** cho lớp phân cách | `_ruot_bi_bo` dùng danh sách cho phép và cùng áp cho run gạch, xóa, chuyển đi. Ca 39 và mutant `wp1525_ruot_ky_hieu_la_trang` phân biệt được hành vi. Quyết định giữ phân cách vẫn bỏ qua `xml:space` và đường giữ chữ gặp cùng vấn đề, xem A1. [Mã](../scripts/tl_core/llm_route.py#L991) · [Ca](../scripts/tl_core/llm_route_test.py#L1458) |
| Z2 · lượt 23 · §2.26 | **ĐÃ VÁ THẬT** | Kiểm tên member trùng trên toàn thư mục ZIP trước khi đọc quan hệ hoặc part, nên document, styles, numbering và các part quan hệ cùng qua một chốt. Ca hiện có dùng hai bản document, bản sau thiếu khoản. `wp1525_zip_trung_ten` bị giết. [Mã](../scripts/tl_core/llm_route.py#L1163) · [Ca](../scripts/tl_core/llm_route_test.py#L1663) |
| Z3 · lượt 23 · §2.26 | **ĐÃ VÁ THẬT** cho ba hình dạng thêm vào suite. **VÁ MỘT PHẦN** cho lớp ranh giới | Mẫu ngoặc bao, dấu chấm cuối dính chữ, và ngoặc đóng cuối đều bị từ chối trong ca sẵn có. `wp1525_diem_bo_thap_phan` bị giết. Miền dấu phân cách/kết nhãn vẫn hẹp hơn miền nhãn cấu trúc, xem A2. [Mã](../scripts/tl_core/llm_route.py#L502) · [Ca](../scripts/tl_core/llm_route_test.py#L686) |
| Z4 · lượt 23 · §2.26 và §3 | **ĐÃ VÁ THẬT** | Hai ca vi phạm riêng một trường, cùng giữ `sdtContent` hợp lệ. Mutant bỏ kiểm `sdtPr` và mutant bỏ kiểm `sdtEndPr` đều bị giết ở ca đích. Ca dương control chứa khoản vẫn đạt. [Ca](../scripts/tl_core/llm_route_test.py#L1659) · [Đột biến](../scripts/tl_core/llm_route_test.py#L1881) |
| §1–§2.3, A8, K1 của #1514 | **ĐÃ VÁ THẬT** cho hai biểu hiện K1 | Dòng điểm đã nhận diện bị từ chối ở cả nguồn có số và mất số. Dòng tiếp mở bằng “là” của nguồn có số không thể nhập vào khoản trước. Với nguồn mất số, phần trước từ nối bị rỗng và phép so báo lệch. Fixture Điều 3 và ba kết quả lưu vẫn đạt 8/8. Không đổi giao diện cờ hay các hàm gọi model. CLI vẫn ghi `can_nguoi_duyet: true` và `pham_vi_kiem` tương ứng. [Ca K1](../scripts/tl_core/llm_route_test.py#L1225) · [Tách khoản](../scripts/tl_core/llm_route.py#L1335) · [CLI](../scripts/tl_core/ops_misc.py#L3120) |
| §2.4–§2.9, A1/B1/C1/D1/E1/F1 và phần bảng B2/C2/E3/E4 | **HẾT ĐỐI TƯỢNG do hợp đồng r7** đối với cắt giữa tệp và duyệt ô. **ĐÃ VÁ THẬT** về fallback | Đoạn có nội dung đầu phải là tiêu đề đúng số Điều, khớp cả đoạn. Vùng kéo tới hết body, bảng và khối lạ bị từ chối, tiền tố Điều/Chương/Mục/Phần trong thân bị chặn. Tệp ZIP nhận vào đường DOCX thiếu số tự động dừng bằng `ValueError` → CLI 2, không còn `KhongCauTruc`. [Vùng Điều](../scripts/tl_core/llm_route.py#L1225) · [CLI](../scripts/tl_core/ops_misc.py#L3028) |
| §2.4–§2.13, A2/A5, B2, C2, D2, E6, F3–F5, G1–G3, H2/H4, J1/K3 | **ĐÃ VÁ THẬT** cho các biểu hiện đã báo | Bộ đếm riêng từng `numId`, `start` vắng là 0, `startOverride` thay giá trị của cấp, cấp cha tăng xóa đếm cấp con. Ca dương đo override 5 → 1 và điểm đặt lại ở khoản sau. Cấp tổ tiên vắng, cấp ngoài miền, số >999, nhiều danh sách thực dùng, số khoản lệch dãy 1…N, số qua style và quy tắc restart chưa hiểu đều dừng. Kiểu danh sách lỗi không dùng có đối chứng A5. Phần nhận dạng part dùng tệp quan hệ của đúng part chính. [Numbering](../scripts/tl_core/llm_route.py#L749) · [Bộ đếm](../scripts/tl_core/llm_route.py#L1197) · [Ca dương](../scripts/tl_core/llm_route_test.py#L1309) |
| §2.4–§2.13, A3/A4, B3/B4/B6, C3–C5, D3–D6, E2/E5, F6, G4, H5, J2/J5, K1 | **ĐÃ VÁ THẬT** cho các biểu hiện lịch sử đã khóa. **VÁ MỘT PHẦN** cho lớp phân cách | Đọc XML gốc, lọc các run gạch đơn/kép độc lập, từ chối toggle nhiều tầng khi không có giá trị trực tiếp, kiểm sửa đổi dấu đoạn và mốc move, chặn `mc:` và dấu phân cách mơ hồ. Content control, metadata đã biết, tab và ngắt trang/cột cuối đoạn có ca dương. Từ nối chỉ dò trong đầu khoản cấu trúc. Hành vi về khoảng trắng biên run vẫn có A1. [Phân tích đoạn](../scripts/tl_core/llm_route.py#L1021) · [Phép so](../scripts/tl_core/llm_route.py#L1494) |
| §2.5, §2.9, §2.18, A6/B5/F2/R2 và câu dẫn | **HẾT ĐỐI TƯỢNG do hợp đồng r7** với việc nhận điểm gõ tay ở đoạn riêng. **ĐÃ VÁ THẬT** cho chốt số gõ tay và câu dẫn | Đoạn không số sau khoản đầu bị chặn. Chốt số gõ tay chạy trên đoạn đã đánh số tự động, phân biệt dạng ngoặc kín với số thập phân. Trước khoản đầu chỉ nhận một câu dẫn chuẩn nguyên đoạn hoặc không có câu dẫn. [Số gõ tay](../scripts/tl_core/llm_route.py#L614) · [Câu dẫn](../scripts/tl_core/llm_route.py#L1315) |
| §2.10–§2.21, G6/H1/J3/K2, L1–L5, M1/M2, N1–N3, Q1/Q2, R1/R3, S1–S3, T1/T2, U1/U2 | **ĐÃ VÁ THẬT** cho các biểu hiện lịch sử ở đầu vào do packet đọc. U2 thuộc giới hạn đã duyệt | Tiêu đề đích so không phân biệt hoa thường. Tiền tố thân dò trên bản chiếu chữ/số sau chốt ký tự. ID chuẩn hóa bằng chuỗi. Quan hệ so URI đầy đủ, QName khối phải đúng, parser nhận bytes XML. Tập ký tự loại số mũ, ký tự lạ bị chặn trước khi gộp hoặc tách dòng và đường thô chỉ gỡ một BOM cho chốt xác minh. Tài liệu hướng dẫn giữ nguyên chữ nguồn khi gặp dẫn chiếu bị chặn. [Tiền tố và ký tự](../scripts/tl_core/llm_route.py#L540) · [Quan hệ](../scripts/tl_core/llm_route.py#L708) · [Hướng dẫn](../docs/GOI_AGENT_DA_NEN.md#L385) |
| §2.22–§2.25, V1–V4, W1–W5, X1–X3, Y1–Y3 | **ĐÃ VÁ THẬT** cho các ca lịch sử chạy lại. **VÁ MỘT PHẦN** cho phân cách và nhãn thô | `--markup-strict` được chuyển tiếp và lỗi extract dừng trước model. Kiểm `numPr` ở mặc định đoạn, cấp trùng, trường đơn trị, wrapper và khóa style vẫn hoạt động. U2/V3/W1/W3 và phần số hiệu W2 là các giới hạn đã duyệt của `tl extract`/`docx_markup`. A2 xảy ra ngay cả khi tự đưa văn bản thô hoàn chỉnh qua `--tep`. [Extract](../scripts/tl_core/llm_route.py#L1599) · [Đơn trị](../scripts/tl_core/llm_route.py#L630) |
| §3, A7/B7/C6/D4/E5/F5/G5/H3/J4, A8/B8/C7/K4/L6 | **ĐÃ VÁ THẬT** cho ca và hướng dẫn lịch sử, trong miền đã đo | Harness chỉ đếm mutant khi neo khớp đúng một lần và ca đích ném `TinHieuChotCa`. Ca lịch sử giữ đối chứng Word override, ngữ pháp thô, dấu phân cách, và quan hệ part đổi tên. Ca CLI dùng model giả kiểm rc 0, 5 và 2. Các hình dạng A1/A2 chưa có ca đối chứng theo hợp đồng đúng. [Harness](../scripts/tl_core/llm_route_test.py#L2171) · [CLI selftest](../scripts/tl_selftest.py#L32285) |

Khi bản trích đầu vào đúng, phép so buộc số khoản theo vị trí, kiểm đủ mọi khoản và so riêng cả thuật ngữ lẫn định nghĩa. Việc bỏ, cắt, gộp hoặc tráo khoản chỉ ở đầu ra của model bị phát hiện. A1/A2 nằm trước bước đó, tại nơi dựng bản trích dùng làm chuẩn. [Phép so](../scripts/tl_core/llm_route.py#L1494) · [Ghi kết quả](../scripts/tl_core/ops_misc.py#L3133)

## Findings

### A1 [P1] DOCX giữ dấu cách biên run mà Word bỏ — `scripts/tl_core/llm_route.py:1063`

**Kịch bản.** Một từ trong định nghĩa được chia làm hai run vì đổi định dạng. Text của run đầu có khoảng trắng ở cuối dưới chế độ `xml:space="default"`. Word bỏ khoảng trắng biên này. Bộ đọc ghép hai run với dấu cách ở giữa và có thể xác nhận một định nghĩa khác nguyên văn. Cùng nguyên nhân trong đường lọc dự thảo, khoảng trắng biên không có hiệu lực ở `t`/`delText` vẫn có thể được tính là phân cách cần giữ nếu mẩu xóa/chuyển đi/run gạch chỉ có khoảng trắng.

**Căn cứ và hạng.** `_phan_tich_doan` dùng thẳng `c.text` ở run còn hiệu lực, và dùng `c.text` cho `delText` lạc thuần trắng. `_ruot_bi_bo` cũng dùng thẳng `e.text` cho `t`/`delText`. Khi đã nối mảnh, `_gon_doan` thu gọn các khoảng trắng còn một dấu cách, nên vẫn giữ biên từ sai. Quy tắc Word về `xml:space` đã được ghi trong selftest r222. Ca `cap27` hiện đòi giữ khoảng trắng đầu ở run không có thuộc tính này, dù mục đích của ca là kiểm URI quan hệ. Hạng P1 theo lớp W2/X1/Y1/Z1 vì bản trích cấu trúc có thể nhận sai chữ của nguồn, kể cả khi số và ranh giới khoản đều đúng. [Run còn hiệu lực](../scripts/tl_core/llm_route.py#L1059) · [Ruột bị bỏ](../scripts/tl_core/llm_route.py#L1005) · [Quy tắc r222](../scripts/tl_selftest.py#L17944) · [Ca cap27](../scripts/tl_core/llm_route_test.py#L1412)

**Đề xuất.** Dùng chung cách đọc khoảng trắng hiệu lực của `t`/`delText` trong `_phan_tich_doan` và `_ruot_bi_bo`, xét giá trị `xml:space` kế thừa và việc đặt lại `default` trước khi ghép. Sửa dữ liệu ca quan hệ để đánh dấu dấu cách có chủ ý. Khóa bằng đối chứng giữa preserve và default trong cả chữ còn hiệu lực và mẩu bị bỏ. Giữ các đối chứng tab, ngắt dòng, NBSP và dấu cách hiệu lực ở r222, vì cắt biên đồng loạt có thể làm dính chữ hợp lệ.

### A2 [P2] Nhãn điểm đa cấp kết bằng gạch ngang vẫn có thể thành khoản thô — `scripts/tl_core/llm_route.py:507`

**Kịch bản.** Văn bản thô đã mất số khoản nhưng còn nhãn của một điểm. Nhãn có hai số cấp phân cách bằng dấu chấm và kết thúc bằng gạch ngang. Dòng điểm có từ nối “là” ngoài ngoặc cùng dấu kết câu, và những dòng còn lại đều có hình dạng hợp lệ. Bộ tách có thể coi dòng điểm là một khoản mới, sau đó xác nhận nguyên văn theo phân đoạn sai.

**Căn cứ và hạng.** `_nhan` cho phép dấu gạch ngang ngắn và vừa ở cuối nhãn có nhiều placeholder. Nhánh số đa cấp của `_RE_DIEM` chỉ tiêu thụ dấu chấm hoặc ngoặc đóng sau cụm chữ số. Tại dấu gạch, lookahead cũng hụt. `_RE_SO_KHOAN` bỏ qua dấu chấm đầu vì ngay sau là chữ số, còn chốt số nội dòng không bắt phần số kế tiếp vì nó đứng ngay sau dấu chấm. Khi nguồn ở nhánh mất số, nguyên dòng đi vào `khoan`. Phép so sau đó có thể chấp nhận nếu model lấy cả nhãn không được nhận diện vào thuật ngữ. Hạng P2 theo K1/Z3 vì cần nhãn còn sót và hình dạng câu định nghĩa. Đây là sai phân đoạn của đường thô có cờ duyệt. [Nhãn thô và số nội dòng](../scripts/tl_core/llm_route.py#L490) · [Nhãn cấu trúc](../scripts/tl_core/llm_route.py#L929) · [Tách thô](../scripts/tl_core/llm_route.py#L1363)

**Đề xuất.** Đồng bộ miền nhãn điểm có thể xuất hiện dưới dạng text với miền mà `_nhan` cho phép, hoặc khai rõ và thu hẹp miền hỗ trợ cấu trúc. Khóa bằng ca nhãn đa cấp kết gạch ngang và các biến thể dấu kết/đệm, ở cả quyết định “đây là điểm” và thứ tự ưu tiên trước nhãn khoản khi hai mẫu chồng lấn. Đối chứng từ ghép, viết tắt và chữ số thập phân thực để tránh tăng chặn oan.

| Lớp nguyên nhân | Hạng còn mở | Lịch sử và phép đóng |
| --- | --- | --- |
| `docx-khoang-trang-sau-loc` | P1 · A1 | W2 → X1 → Y1 → Z1 → A1. Loại nội dung hiển thị lạ đã tiến bộ. Còn xác định dấu cách hiệu lực ở biên run cho cả chữ giữ lại và mẩu bị bỏ, với đối chứng preserve/default. |
| `docx-so-hien-thi` | Đã đóng biểu hiện Z2 | A2/B2/G1/J1/V2/W5 → X2 → Y2 → Z2. Chốt toàn gói chặn trùng tên member trước chọn part và giữ kiểm XML đơn trị cũng như đối chứng A5. |
| `ranh-gioi-khoan` | P2 · A2 | K1 #1514/V4/W4 → X3 → Y3 → Z3 → A2. Hai biểu hiện K1 cũ đã đóng. Còn độ lệch miền nhãn điểm giữa bộ dựng và bộ nhận chữ thô. |
| `docx-test-doc-lap` | Đã đóng biểu hiện Z4 | A7/B7/C6/D4/E5/F5/G5/H3/J4 → Z4. Hai kiểm metadata nay có ca đích và mutant riêng. |

Hai trong bốn lớp mở ở lượt 23 đóng trong phạm vi đã kiểm, hai lớp còn mở với một biểu hiện mỗi lớp. Có **0 P0, 1 P1, 1 P2, 0 P3**. Điều kiện merge ADR-0060 M1 chưa đạt. [Verdict lượt 23](../ops/acceptance/llm-khoan-docx/r1/review-23-codex/VERDICT.md) · [Protocol §8.3](../docs/PROTOCOL_DA_PHIEN.md#L812) · [ADR-0060 M1–M2](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32) · [ADR-0062](../docs/adr/0062-adr-0060-mac-dinh-va-dong-bang-adr-0054.md#L13)

## Kết quả test và đột biến

Log và mã thoát lưu tại `/tmp/wp1525-r24-review.FdBNftrZ/`. Hai bản sao Git cục bộ detached `head` và `base` được dùng cho selftest, kiểm delta và phép xác nhận release, cùng runtime Linux và `core.abbrev=7`. Bytecode Python bị tắt. Bản sao `mutant-space` dành cho đột biến bổ sung.

| Lệnh | Trạng thái | Mã thoát và bằng chứng |
| --- | --- | --- |
| `python scripts/tl_core/llm_route_test.py` | `passed` | rc 0, **63/63** ca đạt, **235/235** mutant được bắt. **138/138** có tiền tố `wp1525_`. `llm-route.log`. |
| `python scripts/tl.py --deterministic workflow-audit --strict --json` | `passed` | rc 0, `ok=true`, 194 lệnh có sẵn, 26 card, 11 nhóm, 60 task, 0 lỗi, 0 cảnh báo. `workflow.log`. |
| `python scripts/tl.py --deterministic golden-test --json` | `passed` | rc 0, `ok=true`, **20/20** ca, **20/20** bản chiếu ổn định, **19/20** byte thô ổn định. `hygiene_sweep_fixture` khai biến động `snapshot_age_s`, có `diff={}`. `golden.log`. |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` · head sạch | `passed` | rc 0, `ok=true`, **187/187** tệp, không sai/thiếu/thừa. Hash kỳ vọng và thực tế cùng `17a53133115891b0e196d318d4a468c488e954acfbf40c6931b5404e6d1ecee7`. Lần chạy ở checkout có verdict rc 2, chỉ thừa `.review/VERDICT.md`. `clean-release.log`, `release.log`. |
| `python ops/lease_publish.py check --root . ops/leases/llm-khoan-docx-r24-g1-claude.yaml` | `passed` cục bộ | rc 0, “ĐĂNG ĐƯỢC”, đúng #1525, neo base `64b7f2c14776`, hết 19:18 UTC. Hai lớp GitHub nằm ngoài phép đo. `lease.log`. |
| `python scripts/tl.py --selftest` · head | `failed` | rc 1, **1774/1790**, transport **12/12**. `r1525_llm_khai_niem_tep_docx_cau_truc` đạt. `selftest.log`. |
| `python scripts/tl.py --selftest` · base | `failed` | rc 1, **1773/1789**, transport **12/12**. Tập 16 ID đỏ trùng head. `base-selftest.log`. |
| `python scripts/tl.py --deterministic determinism-audit --strict --json` | `passed` | rc 0, `ok=true`, **15/15** phép. `determinism.log`. |
| `python scripts/tl.py --deterministic doc-claims-check --strict --json` · head và base | `failed` | Cả hai rc 2, 131 tệp và cùng 410 advisory, cùng một cờ cứng `SHA_NOT_A_COMMIT` ở protocol dòng 1680. `git cat-file -t 9941d8af52aeede1c78ea4e232fbe9a8d5272033` rc 128 trong lịch sử shallow. `doc-claims.log`, `base-doc-claims.log`. |
| Ghim/probe Ruff qua `loi_ruff_ci()` trong `.claude/dev/ci_dang_ky_test.py` | `passed` | rc 0, `RUFF_CONTRACT 3 []`. `ruff-contract.log`. |
| `python -m ruff check --no-cache --select F --output-format json scripts/tl.py` · head và base | `failed` tuyệt đối, tiêu chí delta đạt | Ruff 0.15.15, cả hai rc 1, cùng **12 F821, 0 F401**. Hai JSON giống nhau sau chuẩn hóa đường dẫn. `ruff.log`, `base-ruff.log`. |
| `git diff --check` · dải r24 và dải #1525 | `passed` | rc 0 ở `db06b9c..HEAD` và `fcb12b3..HEAD`. |
| `git diff --check` · toàn PR và dải #1514 | `failed` | Cả hai rc 2, cùng ba khoảng trắng cuối dòng trong verdict #1514 lượt 8. `pr-diff-check.log`, `inherited-diff-check.log`. |

Selftest có cùng 16 ID đỏ ở cả hai cây. Trong đó 14 ca thuộc `r973_bootstrap_*`, `wp433_*`, `wp727_tl_gws_refresh`, với `/tmp/.git` rỗng trong sandbox. Hai ca còn lại là `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` và `r268_l2_trichotomy_theo_trang_thai_object`. Ca CLI của packet là ID đạt tăng thêm duy nhất. Delta đỏ 0, tiêu chí N/N vẫn chưa đạt trên Linux này.

| Mục | Phép kiểm và kết quả |
| --- | --- |
| Z1 | `wp1525_ruot_ky_hieu_la_trang` làm đỏ ca `ca_cau_truc_docx_dat` khi ký hiệu trong mẩu bị bỏ không còn được tính là nội dung. Các ca khoảng trắng thuần, tab và mẩu có chữ vẫn khóa ba quyết định giữ/bỏ. |
| Z2 | `wp1525_zip_trung_ten` tắt chốt toàn ZIP, chết tại ca DOCX có hai member document trùng tên. |
| Z3 | `wp1525_diem_bo_thap_phan` tắt cả nhánh thập phân. Ca đích đã có đối chứng trước r24, nên mutant này một mình không cô lập ba dạng bổ sung. Cả ba dạng đều được assert từ chối trong ca chạy trên head. |
| Z4 | `wp1525_sdtpr_khong_don_tri` và `wp1525_sdtendpr_khong_don_tri` bỏ đúng một trường mỗi lần và đều bị bắt. |
| K1 | `wp1525_tho_nhan_diem` chết ở `ca_wp1514_luot9`. `ca_ranh_gioi_luot4` kiểm dòng tiếp mở bằng “là” ở nguồn có số. |
| A1 · đối chứng bổ sung | Trên bản sao, chỉ sửa nhánh đọc `w:t` trong `_phan_tich_doan` để cắt khoảng trắng ASCII ở biên khi node thiếu `preserve`. Chạy lại suite sẵn có rc 1, **62/63**, **235/235** mutant. Ca `ca_cau_truc_docx_dat` đỏ ở `cap13` với đúng tín hiệu `CHOT`: chữ đã dính sau khi bỏ dấu cách cuối của run thiếu `preserve`. Đây là bằng chứng ca cũ đang phụ thuộc dấu cách ấy. Phép sửa tạm chưa xử lý thuộc tính kế thừa hay đường `delText`. [Ca cap13](../scripts/tl_core/llm_route_test.py#L1356) |

| Hiện vật | SHA-256 |
| --- | --- |
| `llm-route.log` | `6b04be44471430c58640cf72de4769db6ea74d7103617bbc5a4cfbb183ed59e6` |
| `selftest.log` | `b52acb7a95bbcf189569dc110584f086aafa4f871d32deb9f9c14431809c8f38` |
| `base-selftest.log` | `6ace83cf90d1ca820065b12eda446d9e5055fd024ccae1a70b81d4360e7f8a3a` |
| `clean-release.log` | `4da1ef3b243aff81fb9850974641c928a0512234dbd3f352b19f5e9036f920e8` |
| `mutant-space.log` | `6880207eaaeb0566151247a6ff42e1e265feeb319560753ee41fdb5c3d4f0554` |
| `mutant-space.patch` | `f503152b4df373bbba6c9be5c75b80165b998802a78f37979d2d4656e3f07efc` |

## Không đo được

- Kịch bản đầu-cuối của A1 với Word/Google Docs, gồm cả `xml:space` kế thừa và mẩu bị bỏ, cùng kịch bản A2 với nhãn đa cấp kết gạch là kết quả đọc mã. Đột biến A1 đo phần phụ thuộc của ca sẵn có vào khoảng trắng biên. Phạm vi lượt này giữ nguyên dữ liệu thử sẵn có.
- §2.5 đã nhận bookmark, comment, perm, hyperlink, content control, proofing marker, tab và ngắt trang/cột cuối đoạn. Các giới hạn đã khai gồm bảng, ngắt mềm, trường, hình, ký hiệu, chú thích, `mc:` và ký tự ngoài tập cho phép. Chưa có bằng chứng từ ca sẵn có về một phần tử phổ biến của Word/Google Docs bị chặn oan ngoài các giới hạn này. Tần suất theo bản export thực chưa đo. [Danh sách phần tử](../scripts/tl_core/llm_route.py#L615) · [Hướng dẫn](../docs/GOI_AGENT_DA_NEN.md#L385)
- `skipped`: hai lớp GitHub của kiểm lease offline, gồm Issue/PR và comment. `not_run`: GitHub/CI từ xa, model thật, Windows bản địa. Windows là `required` theo M3 vì diff toàn PR đổi dòng Python có `encoding=`. [ADR-0060 M3](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L43) · [Dòng đổi](../scripts/tl_core/ops_misc.py#L3061)
- Ref GitHub hiện thời, repo nguồn Executor và receipt terminal của launcher nằm ngoài phép quan sát của verdict. Checkpoint cục bộ neo prompt và candidate. Mã thoát tiến trình reviewer và hash stdout ổn định do launcher ghi khi kết thúc. [Protocol §8.1](../docs/PROTOCOL_DA_PHIEN.md#L770)

## Đọc lại checkout và kết luận

HEAD/tree ở đầu và cuối đều trùng. Diff binary worktree và index rỗng. Checkout chính ban đầu chỉ có `.codex/` ignored. Golden tạo fixture ignored, đã chuyển các file mới ấy sang scratch. Readback cuối thấy `.codex/` và tệp mới `.review/VERDICT.md`. Hai bản sao đối chứng có diff tracked rỗng. Snapshot là quan sát ở hai mốc. [Protocol §8.2](../docs/PROTOCOL_DA_PHIEN.md#L797)

Lượt 24 đã dùng hết trần theo lease r24. A1 và A2 chặn merge theo ADR-0060 M1. Gate N/N và doc-claims strict chưa đạt trên bản sao Linux, còn bằng chứng Windows/CI chưa đo.

P2_mo: 1

VERDICT: REQUEST_CHANGES
