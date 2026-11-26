# Verdict packet #1525 r25 lượt 25 — Codex
reviewed_sha: 659d9f2997e553de7b6e2ed5da4db69df6add6f2
reviewed_tree: 90c60aa52040b16a1f88a41266fa7d50a3cfce5d
base_sha: 64b7f2c14776d5d0e1d34a6be4725490956f5bec

provider: openai_codex
execution_surface: codex_cli
transport: machine

## Đối chiếu lượt 24 và đặc tả r25

- Checkout độc lập, detached, origin `ducthangho/tra-luat`. Ref cục bộ `origin/ccr-89c0d2e2-inanqb` trỏ đúng reviewed SHA. Merge base với nền đóng băng trùng `base_sha`, tree nền `0cc14e79cecd2ce44bc4dc6cff92cadb31fd7ee4`. Mốc tiếp nối #1514 là `fcb12b3873c3bec2c339029136243ed2c804ce05`, mốc trước bản vá r25 là `cc05cb673859cf680fb8c8954d05efe65b2b5e08`.
- Lease #1525 r25/g1, class `sensitive`, lượt 25/25, hạn 19:35 UTC ngày 26-11-2026. Hash SHA-256 đặc tả trên đĩa và trong Git đều khớp lease `b0f72a4b5dec5df221d74bda9eef9daddbc0c0546f2d45800f53ed6293760a94`. Đã đối chiếu **25/25** cặp bia mộ hai chiều và **26/26** hash từ #1514 r9 qua #1525 r1 đến r25. Quyền đứng về tăng trần và ngoại lệ M5 được ghi trong đặc tả. [Lease r25](../ops/leases/llm-khoan-docx-r25-g1-claude.yaml) · [Đặc tả r25](../ops/specs/llm-khoan-docx-r25.md)
- Write set 136 đường dẫn, hash LF `dfdae2b996a6a83b510494b5c187deaaa6699bc87392991e298ac824cdfffdef`. Bản vá r25 **7/7** và phạm vi #1525 **132/132** đường dẫn khớp lease sau khi loại bốn tệp hồ sơ #1514 theo prompt. Toàn PR có 180 đường dẫn, gồm phần kế thừa #1514. Ba diff nguyên byte của PR, packet và r25 được giữ trong thư mục log.
- Codex CLI 0.172.0, run `70a547e31db24dc7a975a8e635ba84a4` qua launcher. SHA-256 prompt `c157142344e205fe85b6420cc37314502fcfb9baedae63fa28a729f6db45aa69` khớp run. Executor theo lease là `anthropic_claude / claude_code / machine/local`, phiên `session_015GtxrZQYT3Vt8PJdXrjEKg`. Linux, Python 3.13.18, Git 2.43.0, checkout shallow, `core.abbrev=7`, sandbox `workspace-write` với metadata Git checkout gốc chỉ đọc. Model cụ thể và effort phục vụ `KHONG_DO_DUOC` theo biên nhận hiện có. [Protocol §8.1](../docs/PROTOCOL_DA_PHIEN.md#L770)

| Mục | Trạng thái | Bằng chứng |
| --- | --- | --- |
| A1 lượt 24 · §2.27 | **ĐÃ VÁ THẬT** cho các biểu hiện đọc tuần tự đã báo | Một hàm `_chu_t` áp khoảng trắng XML ở hai biên cho chữ giữ lại, `delText` lạc và ruột bị bỏ. Duyệt tổ tiên nhận `preserve` và cho `default` thay giá trị kế thừa. `cap40` và `cap41` phân biệt không `preserve` với `preserve` kế thừa ở run thường. Xem kết quả đột biến về phần kiểm chưa đủ. [Mã](../scripts/tl_core/llm_route.py#L991) · [Ca](../scripts/tl_core/llm_route_test.py#L1460) |
| A2 lượt 24 · §2.27 | **ĐÃ VÁ THẬT** cho hai nhãn đa cấp kết gạch trong ca hiện có. **VÁ MỘT PHẦN** ở lớp `ranh-gioi-khoan` | Hai loại gạch đều được bổ sung vào nhánh thập phân nhiều cấp. Đột biến hồi quy `wp1525_thap_phan_bo_gach` bị giết. Chốt vẫn lệch miền nhãn do `_nhan` dựng, xem B1. [Chốt](../scripts/tl_core/llm_route.py#L502) · [Ca](../scripts/tl_core/llm_route_test.py#L690) |
| §1–§2.3 · A8 lượt 1 · K1 #1514 | **ĐÃ VÁ THẬT** cho hai biểu hiện K1 gốc | Điểm đi vào nhánh `_RE_DIEM` bị từ chối dù nguồn có số hay mất số. Dòng tiếp mở bằng “là” ở nguồn có số rơi vào nhánh dòng không số. Ở nguồn mất số, `lech_nguyen_van` đòi hai vế đều có chữ. Fixture Điều 3 và ba kết quả lưu đạt 8/8. Diff giữ giao diện, đường model, `can_nguoi_duyet: true` và chọn `pham_vi_kiem` đúng theo nguồn ranh giới. [Tách khoản](../scripts/tl_core/llm_route.py#L1364) · [CLI](../scripts/tl_core/ops_misc.py#L3120) |
| §2.1–§2.9 · A1/B1/C1/D1/E1/F1 và bảng B2/C2/E3/E4 | **HẾT ĐỐI TƯỢNG do hợp đồng r7** với việc tìm điểm cắt giữa tệp và duyệt ô. **ĐÃ VÁ THẬT** với việc bỏ fallback | Đoạn có nội dung đầu là tiêu đề đúng số, khớp toàn dòng. Vùng chạy hết body, phần còn lại có tiêu đề Điều/Chương/Mục/Phần sẽ bị chặn, bảng hoặc khối lạ ở đâu cũng bị chặn. DOCX thiếu số tự động ném `ValueError`, handler trả 2. Cả hàm đọc lẫn CLI đã bỏ `KhongCauTruc`; chỉ đầu vào TXT hoặc qua extract vào đường thô. [Vùng Điều](../scripts/tl_core/llm_route.py#L1254) · [Handler](../scripts/tl_core/ops_misc.py#L3037) |
| §2.4–§2.13 · A2/A5, B2, C2, D2, E6, F3–F5, G1–G3, H2/H4, J1, K3 | **ĐÃ VÁ THẬT** cho các biểu hiện lịch sử đã đo | Dãy được đếm riêng theo `numId` chuẩn hóa. `start` vắng dùng 0, `startOverride` đè cấp tương ứng, khi cấp cha tăng thì các cấp con được xóa khỏi bộ đếm. Ca có override khác start và reset điểm ở khoản sau. Cấp tổ tiên vắng, số >999, nhiều danh sách thực dùng, dãy khoản lệch 1…N, quy tắc restart chưa giải và số hiệu lực qua style bị chặn. Kiểu không dùng có đối chứng A5. [Numbering](../scripts/tl_core/llm_route.py#L749) · [Bộ đếm](../scripts/tl_core/llm_route.py#L1237) · [Ca override](../scripts/tl_core/llm_route_test.py#L1309) |
| §2.4–§2.13 · A3/A4, B3/B4/B6, C3–C5, D3–D6, E2/E5, F6, G4, H5, J2/J5, K1 lượt 10 | **ĐÃ VÁ THẬT** cho các biểu hiện lịch sử đã đo | XML gốc được lọc theo cây, tính riêng gạch đơn và kép, chỉ áp trực tiếp khi có thuộc tính trên run. Toggle nhiều tầng không giải được, sửa dấu đoạn và move không cân đều chặn. Content control, metadata được biết, tab và ngắt trang/cột cuối đoạn có ca dương. Chốt `mc:` áp toàn part. Từ nối cấu trúc chỉ dò trong chữ của đoạn mở khoản. [Phân tích đoạn](../scripts/tl_core/llm_route.py#L1049) · [Phép so](../scripts/tl_core/llm_route.py#L1523) |
| §2.5, §2.9, §2.18 · A6/B5/F2/R2 và câu dẫn | **HẾT ĐỐI TƯỢNG do hợp đồng r7** với việc nhận điểm gõ tay ở đoạn riêng. **ĐÃ VÁ THẬT** cho số gõ tay và câu dẫn đã báo | Đoạn không số sau khoản đầu dừng. Số gõ tay ở đoạn đã đánh số tự động kiểm theo mẫu riêng, giữ đối chứng số thập phân và chặn ngoặc kín. Trước khoản đầu chỉ nhận một câu dẫn nguyên đoạn đúng mẫu hoặc vắng. [Giới hạn số gõ tay](../scripts/tl_core/llm_route.py#L614) · [Câu dẫn](../scripts/tl_core/llm_route.py#L1344) |
| §2.10–§2.21 · G6/H1/J3/K2, L1–L5, M1/M2, N1–N3, Q1/Q2, R1/R3, S1–S3, T1/T2, U1/U2 | **ĐÃ VÁ THẬT** trong miền nhập liệu do packet đọc. U2 là giới hạn đã duyệt | Tiền tố thân được dò sau chốt ký tự, số mũ bị loại, bỏ một BOM ở đường thô. Kiểm namespace của khối và URI quan hệ đầy đủ, part chính đọc bằng bytes. So tiêu đề DOCX không phân biệt hoa thường. Không còn hướng dẫn sửa chữ nguồn để qua chốt dẫn chiếu. [Tiền tố và ký tự](../scripts/tl_core/llm_route.py#L540) · [Quan hệ](../scripts/tl_core/llm_route.py#L708) · [Hướng dẫn](../docs/GOI_AGENT_DA_NEN.md#L385) |
| §2.22–§2.26 · V1–V4, W1–W5, X1–X3, Y1–Y3, Z1–Z4 | **ĐÃ VÁ THẬT** cho các biểu hiện lịch sử qua ca đã có, **VÁ MỘT PHẦN** cho miền nhãn thô | `--markup-strict` được chuyển tiếp, extract lỗi dừng trước model. Kiểm mặc định đoạn, cấp trùng, trường đơn trị, wrapper, khóa style và tên part trùng còn hiệu lực. Mẩu run gạch, `del` và `moveFrom` dùng chung phép đọc. V3/W1/W3 và phần số hiệu của W2 là giới hạn đã duyệt. Miền nhãn điểm còn B1. [Đơn trị](../scripts/tl_core/llm_route.py#L630) · [Markup](../scripts/tl_core/llm_route.py#L1019) · [Extract](../scripts/tl_core/llm_route.py#L1628) |
| §3 · A7/B7/C6/D4/E5/F5/G5/H3/J4/Z4 và A8/B8/C7/K4/L6 | **ĐÃ VÁ THẬT** đối với các biểu hiện test và hướng dẫn lịch sử trong miền đã đo | Harness đòi neo duy nhất và `TinHieuChotCa` từ đúng ca đích. Có ca cho metadata riêng, quan hệ part chính đổi tên, số và nhãn Word, và selftest CLI model giả kiểm 0/5/2. §3 cần thêm bằng chứng cho các nhánh mới của A1 lượt 24. [Harness](../scripts/tl_core/llm_route_test.py#L2178) · [Selftest CLI](../scripts/tl_selftest.py#L32285) |

Với bản trích đúng, phép so buộc số khoản theo vị trí và đủ số lượng, rồi so riêng toàn bộ hai vế. Việc model bỏ, cắt, gộp hay tráo khoản bị bắt ở bước này. Đường thô vẫn có trường hợp hai bố cục mất phân cấp nhưng có cùng hình dạng chữ, chẳng hạn số tiểu mục trùng dãy khoản, hoặc hai dòng mỗi dòng tự đứng được như một định nghĩa. Phạm vi thô và biên bản #1514 đã khai giới hạn ấy. B1 xét riêng những hình dạng nhãn mà đặc tả #1525 cam kết nhận diện. [Phép so](../scripts/tl_core/llm_route.py#L1523) · [Verdict #1514 lượt 10](../ops/acceptance/llm-ranh-gioi-khoan/r1/review-10-codex/VERDICT.md)

## Findings

### B1 [P2] Bộ nhận nhãn điểm thô vẫn hẹp hơn bộ dựng nhãn Word — `scripts/tl_core/llm_route.py:502`

**Kịch bản.** Nguồn `--tep` văn bản thô mất số khoản và còn một nhãn điểm thập phân kết gạch. Nếu chữ của thuật ngữ bắt đầu ngay sau nhãn bằng một dấu mở ngoặc kép, lookahead của regex không nhận dòng ấy là điểm. Kết quả tương tự với nhãn thập phân có gạch giữa các cấp thay cho dấu chấm, một dạng có thể dựng từ `lvlText`. Khi dấu ngoặc/trích dẫn khép đúng trên dòng và dòng có từ nối “là” bên ngoài cùng dấu kết câu, một điểm có thể trở thành khoản mới trong bản trích. Đây là hai biểu hiện của cùng độ lệch miền nhãn. [Regex thô](../scripts/tl_core/llm_route.py#L490) · [Dựng nhãn](../scripts/tl_core/llm_route.py#L929)

**Căn cứ và hạng.** `_RE_DIEM` đòi dấu chấm giữa các số và sau nhãn đòi khoảng trắng hoặc chữ cái. `_RE_SO_KHOAN` và `_RE_SO_NOI_DONG` không bù được các dạng trên. Khi các chốt khác đều qua, `tach_khoan` giữ nguyên dòng và phép so có thể chấp nhận đầu ra chép nó như một khoản, kể cả phần nhãn. Đây là P2 vì cần bố cục thô có điều kiện, khớp lớp K1/W4/X3/Y3/Z3/A2 và vẫn có `can_nguoi_duyet` cùng cảnh báo ranh giới thô. Nhận định từ mã, áp dụng ngay tại đường `--tep` văn bản thô. [Tách khoản](../scripts/tl_core/llm_route.py#L1392) · [So và ghi](../scripts/tl_core/ops_misc.py#L3133) · [Verdict lượt 24](../ops/acceptance/llm-khoan-docx/r1/review-24-codex/VERDICT.md)

**Đề xuất.** Định nghĩa miền nhãn điểm được hỗ trợ ở một chỗ rồi kiểm cả các khoảng đệm, dấu phân cấp và ký tự đầu thân. Khi một tiền tố có thể vừa là nhãn điểm vừa là số khoản, cần bằng chứng đủ mạnh để phân vai hoặc từ chối trường hợp mơ hồ. Khóa cả âm và dương cho nhãn hợp lệ, số khoản đơn, số thập phân thực, từ ghép và viết tắt. Nếu thu hẹp miền thay cho nhận diện, ghi rõ miền được chọn trong đặc tả. [§2.25–2.27](../ops/specs/llm-khoan-docx-r25.md#L307)

### B2 [P2] Test r25 chưa khóa đặt lại `xml:space` và phần chữ đã bỏ — `scripts/tl_core/llm_route_test.py:1890`

**Bằng chứng và hạng.** Suite có đối chứng riêng cho chữ giữ lại thiếu `preserve` và cho `preserve` kế thừa. Ba phép sửa độc lập trên bản sao tạm đều chạy rc 0, 63/63 ca, 238/238 đột biến sẵn có. Chúng lần lượt biến `xml:space="default"` thành `preserve`, trả `_ruot_bi_bo` về đọc `e.text` trực tiếp và khôi phục việc giữ trắng XML đã bị cắt ở `delText` lạc. Mỗi phép bỏ một tính chất được §2.27 yêu cầu và vẫn qua suite. P2 vì đây là thiếu phép kiểm §3 cho chốt bảo vệ nguyên văn. Đọc mã hiện hành cho thấy cả ba tính chất vẫn được thực thi khi chạy tuần tự. [Ca r25](../scripts/tl_core/llm_route_test.py#L1460) · [§2.27 và §3](../ops/specs/llm-khoan-docx-r25.md#L326)

**Đề xuất.** Đo riêng nhánh `default` đặt lại giá trị kế thừa và nhánh mẩu bị bỏ trước khi quyết định giữ phân cách. Đối chứng dấu cách có hiệu lực với ký tự XML ở biên đã bị bỏ. Dùng ca đích và đột biến riêng cho nhánh `delText` lạc khi kiểm `xml:space`, vì đột biến hiện có chỉ đo việc giữ khoảng trắng thuần. [Các đột biến](../scripts/tl_core/llm_route_test.py#L1889)

### B3 [P2] Dấu ngắt trong run gạch đã bỏ vẫn có thể làm cả Điều bị từ chối — `scripts/tl_core/llm_route.py:1095`

**Kịch bản và căn cứ.** Một mẩu trong dự thảo gồm chữ bị gạch và ngắt mềm nằm trong cùng run. §2.25 Y1 yêu cầu bỏ trọn mẩu có nội dung, kể cả phân cách của mẩu. Vòng đọc run cập nhật `kq["ngat"]` trước khi xét nhánh run gạch. Nhánh bỏ run không hoàn tác cờ ấy. Với ngắt trang/cột, cờ `sau_ngat_trang` cũng còn và chữ hợp lệ ở run tiếp có thể làm đoạn bị đánh dấu ngắt mềm. Đường `w:del` hoặc `w:moveFrom` gọi `_ruot_bi_bo` mà không cập nhật hai cờ này. P2 vì hậu quả quan sát được từ mã là rc 2 oan đối với đoạn hợp lệ sau lọc. Chốt ngắt còn hiệu lực của §2.5 vẫn đúng. [Đọc run](../scripts/tl_core/llm_route.py#L1087) · [Đường wrapper](../scripts/tl_core/llm_route.py#L1138) · [Chốt đoạn](../scripts/tl_core/llm_route.py#L1285)

**Đề xuất.** Chỉ cập nhật trạng thái ngắt của đoạn sau khi biết phần nào của run còn hiệu lực. Giữ chính sách phân cách trắng của Y1 và đối chứng ngắt thật còn hiệu lực. Cần đo riêng ngắt mềm và ngắt trang/cột nằm trong mẩu bị bỏ, bên cạnh ca J5 đã có cho chữ bị bỏ nằm sau một ngắt. [Ca J5](../scripts/tl_core/llm_route_test.py#L1498)

| Lớp nguyên nhân | Hạng còn mở | Lịch sử và phép đóng |
| --- | --- | --- |
| `ranh-gioi-khoan` | P2 · B1 | K1 #1514 → V4/W4 → X3 → Y3 → Z3 → A2 lượt 24 → B1. Hai biểu hiện K1 gốc đã đóng. Cần khớp miền nhãn điểm hoặc công bố và cưỡng chế miền hẹp hơn. |
| `docx-test-doc-lap` | P2 · B2 | A7/B7/C6/D4/E5/F5/G5/H3/J4 → Z4 → B2. Z4 đã đóng với kiểm metadata. Ba đột biến độc lập r25 còn sống. |
| `docx-khoang-trang-sau-loc` | P2 · B3 | W2 → X1 → Y1 → Z1 → A1 lượt 24. Bản vá r25 sửa khoảng trắng biên với lời gọi tuần tự. Còn tác dụng phụ của dấu ngắt trong run bị loại, nối cả lịch sử H5/J5. |
| `docx-so-hien-thi` | Các biểu hiện đã báo đóng trong miền đã đo | A2/B2/G1/J1/V2/W5 → X2 → Y2 → Z2. Kiểm một giá trị mỗi cấp, nguồn style, tên member trùng và đối chứng override/reset vẫn qua. |

Có **0 P0, 0 P1, 3 P2, 0 P3**, ba lớp và ba finding mở. B1 có hai hình dạng nhãn còn lọt. B2 có ba nhánh thiếu phép đo. B3 có hai nhóm dấu ngắt còn tác dụng sau khi run bị loại. Theo ngưỡng verdict trong prompt, kết luận nội dung là `APPROVE`. Điều kiện merge ADR-0060 M1 vẫn thiếu do còn ba P2. [Protocol §8.3](../docs/PROTOCOL_DA_PHIEN.md#L812) · [ADR-0060 M1–M2](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32) · [ADR-0062](../docs/adr/0062-adr-0060-mac-dinh-va-dong-bang-adr-0054.md#L13)

## Kết quả test và đột biến

Thư mục `/tmp/wp1525-r25-review.NnQUVNke/` giữ log, mã thoát, diff kiểm và bản sao tạm. Dùng Python 3.13.18 trên Linux, tắt ghi bytecode và ghim `core.abbrev=7`. Bản sao `head` và `base` là hai checkout Git cục bộ detached, cùng object store đọc từ bản sao reviewer.

| Lệnh | Trạng thái | Mã thoát và bằng chứng |
| --- | --- | --- |
| `python scripts/tl_core/llm_route_test.py` | `passed` | rc 0, **63/63** ca, **238/238** đột biến bị giết, gồm **141/141** `wp1525_*`. `route.log`. |
| `python scripts/tl.py --deterministic workflow-audit --strict --json` | `passed` | rc 0, `ok=true`, 194 lệnh, 26 card, 11 nhóm, 60 task, 0 lỗi, 0 cảnh báo. `workflow.log`. |
| `python scripts/tl.py --deterministic golden-test --json` | `passed` | rc 0, `ok=true`, **20/20** ca, **20/20** bản chiếu ổn định, **20/20** byte thô ổn định ở lượt chạy này. `golden.log`. |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` · head sạch | `passed` | rc 0, `ok=true`, **187/187** tệp, sai/thiếu/thừa đều 0. Hash gói khớp `73610e7a3c45745bc44a2df03685953d202069d4528a3a74d5a21532c017dc51`. `clean-release.log`. |
| Cùng lệnh release-verify · checkout có verdict | `failed` | rc 2, đúng 187 tệp theo manifest và một tệp thừa `.review/VERDICT.md`. `release.log`. |
| `python ops/lease_publish.py check --root . ops/leases/llm-khoan-docx-r25-g1-claude.yaml` | `passed` cục bộ | rc 0, “ĐĂNG ĐƯỢC”, #1525, neo `64b7f2c14776`, hạn 19:35 UTC. `lease.log`. |
| `python scripts/tl.py --selftest` · checkout có verdict | `failed` | rc 1, **1773/1790**, transport **12/12**. Ca CLI `r1525_llm_khai_niem_tep_docx_cau_truc` đạt. Ngoài 16 ID đỏ ở base, có thêm `wp44_release_bundle_topology_under_200`. `selftest.log`. |
| `python scripts/tl.py --selftest` · base sạch | `failed` | rc 1, **1773/1789**, transport **12/12**, 16 ID đỏ. `base-selftest.log`. |
| `python scripts/tl.py --selftest` · head sạch | `failed` | rc 1, **1774/1790**, transport **12/12**. Ca CLI của packet và `wp44_release_bundle_topology_under_200` đều đạt. Cùng 16 ID đỏ với base. `clean-selftest.log`. |
| `git diff --check cc05cb6 HEAD` và `git diff --check fcb12b3 HEAD` | `passed` | Cả hai rc 0. `patch-diff-check.log`, `packet-diff-check.log`. |
| `git diff --check 64b7f2c HEAD` | `failed` | rc 2, ba dấu khoảng trắng cuối dòng trong hồ sơ #1514 lượt 8. `pr-diff-check.log`. |

16 ID đỏ chung gồm 14 ca `r973_bootstrap_*` (8), `wp433_*` (5) và `wp727_tl_gws_refresh` trong môi trường có `/tmp/.git` rỗng. Hai ca còn lại là `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` và `r268_l2_trichotomy_theo_trang_thai_object`. So danh sách ID đỏ giữa head sạch và base bằng `cmp` được rc 0. Delta đỏ bằng 0, ca CLI mới đạt. Ca kiểm cấu trúc gói trở lại đạt khi dùng checkout sạch. Tiêu chí selftest N/N của §5 vẫn thiếu. SHA-256 log head sạch `eb21d773c73c4a1f9647cb5ef9b31788e9929f03e53b36bb1bed771dd808f75b`, log base `efbf93308fadd51a6d75f7d855239725b142f7594b50968b4c0f02410e28e111`.

Theo dõi `DOT_BIEN` sẵn có bằng `python -B -m pdb scripts/tl_core/llm_route_test.py`, với breakpoint có điều kiện tại dòng 2203. Trình gỡ lỗi và suite đều rc 0. `target-mutants.log` ghi tín hiệu `TinHieuChotCa` cho từng trường hợp dưới đây, sau khi module đột biến đã nạp được. [Harness](../scripts/tl_core/llm_route_test.py#L2183)

| Đột biến | Kết quả và nguyên nhân |
| --- | --- |
| `wp1525_bo_xml_space` | Bị giết tại `cap40`. Giữ trắng biên dù không có `preserve`. |
| `wp1525_xml_space_khong_ke_thua` | Bị giết tại `cap41`. Mất trắng biên kế thừa từ đoạn và làm dính chữ. |
| `wp1525_thap_phan_bo_gach` | Bị giết tại `ca_khoan_mat_so_co_diem_dat`. Dòng điểm có nhãn thập phân kết gạch được nhận vào nguồn mất số. |
| `wp1525_tho_nhan_diem` | Bị giết tại `ca_wp1514_luot9`. Bỏ chốt làm nguồn có các dòng điểm được phân thành khoản. |
| Đổi `xml:space="default"` thành `preserve` trên bản sao | Còn sống, rc 0, **63/63**, **238/238**. `mutant-default-reset.diff` và `.log`. |
| `_ruot_bi_bo` đọc lại `e.text` trực tiếp trên bản sao | Còn sống, rc 0, **63/63**, **238/238**. `mutant-deleted-body.diff` và `.log`. |
| `delText` lạc giữ lại trắng XML đã bị `_chu_t` cắt trên bản sao | Còn sống, rc 0, **63/63**, **238/238**. `mutant-loose-deltext.diff` và `.log`. |

Ba đột biến bổ sung chỉ thay mã ở bản sao `mutant-space` rồi chạy lại chính suite hiện có. Cả ba log có cùng SHA-256 `2f759ff9b09455ccf5a9bf3e1af105fdbc786f02a09923449647752f89bc96fc` với `route.log`. Log breakpoint SHA-256 `5a62888f043d7163870072c9790414fe2a4b30d0ccd4fe3e429d8f4c2071fb5c`. Log manifest sạch SHA-256 `754317174d78dc93dc41202b413bb8497830bb58c3ec8705ceae70b9d25d7660`.

## Không đo được

- B1 và B3 là kết luận đọc mã. Chưa có bằng chứng end-to-end cho hai kịch bản bằng bộ ca sẵn có. Với phần tử XML của bản xuất Word/Google Docs, chưa xác lập thêm trường hợp phổ biến ngoài B3 và các giới hạn đã khai. Danh sách cho phép nhận các dạng đã có ca, gồm bookmark/comment/perm, content control, hyperlink, proofing marker, tab và ngắt trang/cột cuối đoạn. Tần suất hình dạng theo exporter và cách Word hiển thị cần bản xuất thực để đo. [Danh sách phần tử](../scripts/tl_core/llm_route.py#L615) · [Hướng dẫn](../docs/GOI_AGENT_DA_NEN.md#L385)
- `_GIU_TRANG` dùng trạng thái chung cấp module. Hai lần đọc đồng thời trong cùng tiến trình có thể thay tập ID của nhau và làm mất trắng `preserve`. Tìm tham chiếu trong repo chỉ thấy handler đọc tuần tự và các ca test. Chưa có đường gọi đồng thời thuộc CLI được giao hoặc phép đo runtime cho dạng dùng trực tiếp module. [Trạng thái](../scripts/tl_core/llm_route.py#L1009) · [Lần gán](../scripts/tl_core/llm_route.py#L1205)
- `skipped`: hai lớp GitHub của kiểm lease ngoại tuyến, gồm Issue/PR và comment. `not_run`: GitHub/CI từ xa, model thật và Windows native. Windows là `required` theo M3 vì toàn PR có thay đổi dòng Python chứa `encoding=`. `determinism-audit --strict`, `doc-claims-check --strict` và Ruff delta thuộc nghiệm thu §5, nằm ngoài danh sách phép đo của prompt lượt 25. [ADR-0060 M3](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L43) · [Đặc tả §5](../ops/specs/llm-khoan-docx-r25.md#L345)
- Chưa đo ref GitHub thực, repo nguồn Executor, model/effort phục vụ và receipt terminal của launcher. Checkpoint và run cục bộ cùng neo exact head và hash prompt. Mã thoát launcher và hash đầu ra ổn định do launcher ghi sau khi tiến trình reviewer kết thúc. [Protocol §8.1](../docs/PROTOCOL_DA_PHIEN.md#L770)

## Đọc lại checkout và kết luận

HEAD và tree trùng ở đầu và cuối. Diff binary worktree và index đều rỗng. Các thư mục ignored do golden và selftest sinh được chuyển sang scratch. Readback cuối chỉ thấy `.codex/` ignored đã có từ đầu và `.review/VERDICT.md` mới. Đây là snapshot tại hai mốc. [Protocol §8.2](../docs/PROTOCOL_DA_PHIEN.md#L797)

Lượt 25 đạt ngưỡng verdict do prompt đặt. ADR-0060 M1 vẫn chặn merge do ba P2 mở. Gate selftest N/N chưa đạt trên Linux này và bằng chứng Windows/CI chưa được đo. Lượt 25 đã dùng đến trần hiện hành của lease r25. [ADR-0060](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32) · [Lease r25](../ops/leases/llm-khoan-docx-r25-g1-claude.yaml)

P2_mo: 3
VERDICT: APPROVE
