# Verdict packet #1525 r40 lượt 40 — Codex

reviewed_sha: f63028ad85b3ba4a37b10c0d9f6795eba78690e8
tree: 5fb9aa27580e8d14b30d683580d707bb9a5fbd35
base_sha: 64b7f2c14776d5d0e1d34a6be4725490956f5bec


## Preflight

- Repository `ducthangho/tra-luat`, detached HEAD, base nghiệm thu `64b7f2c14776d5d0e1d34a6be4725490956f5bec` là tổ tiên của ứng viên. So tiếp nối từ `9e2f419d90e4e38b58c54ee7e44592c7ae763b59`; tách toàn PR từ mốc master đã nhập `695916ea3bfffdd7b2e8fcb94b0740b3c421fe70`.
- Packet #1525 r40/g1, `sensitive`, lời gọi 41/45. Lease còn hạn lúc preflight, tới `2026-11-27T03:09:00Z`. SHA-256 đặc tả `f14c2046cfdcd48420acfc42d4e29bf467a5bab53314ddb193e758b7f214a5c8` khớp lease. Write set 212 path, hash `900f85eb793a088d1e819114449e5df05af437855cd94196eb36c81a21b988c5`. 11/11 path của bản vá từ r39 thuộc lease. Trong 256 path toàn PR từ master đã nhập, 208 thuộc lease, 48 là hồ sơ/spec/lease của #1514, gồm 4 tệp đóng lượt #1514 đã nêu trong prompt, thêm tại `fb3a492` và `2c91832`. 40/40 cặp bia mộ #1514 r9 → #1525 r1 → r40 khớp hai chiều và 41/41 hash đặc tả trong chuỗi khớp. [Lease r40](../ops/leases/llm-khoan-docx-r40-g1-claude.yaml) · [Đặc tả r40](../ops/specs/llm-khoan-docx-r40.md)
- Assignment Executor `claude / claude_code / machine/local`, theo lease. Reviewer `openai_codex / codex_cli / machine`, run `a18e92a20f6f429e9ff627f7ff07dcc0`, nguồn `../run/a18e92a2/run.json`. SHA-256 prompt `90df09e1642482191e77cadc283b37502100229dfbb4cae3c5d235f89e4f93d5` khớp run. Linux, Python 3.13.18, sandbox `workspace-write`, approval `never`, `core.abbrev=7`. Checkout reviewer có diff tracked/index rỗng, chỉ `.codex/` ignored tại mốc bàn giao. Các lệnh gate dùng clone cục bộ exact SHA bên ngoài checkout, với `PYTHONDONTWRITEBYTECODE=1`. [Protocol §8.1](../docs/PROTOCOL_DA_PHIEN.md#L770)

## Đối chiếu lượt 39 và đặc tả r40

| Mục | Trạng thái | Bằng chứng |
| --- | --- | --- |
| Lượt 39 `ranh-gioi-khoan`, §2.38–§2.42 | **ĐÃ VÁ THẬT** các ca cụ thể của lượt 39. **VÁ MỘT PHẦN** toàn lớp. | Bỏ giới hạn số vế/độ dài, thêm gạch em, chặn `là` trong dấu mở hoặc dính dấu kết ở các ca đích. Hai phía miền vẫn có trong `PHAM_VI_KIEM`; xem finding về chốt kết vế và trạng thái dấu phân cách. [Mã](../scripts/tl_core/llm_route.py#L587) · [Ca](../scripts/tl_core/llm_route_test.py#L1941) |
| Lượt 39 `can-tai-nguyen-doc-nguon`, §2.37–§2.42 | **ĐÃ VÁ THẬT** locator tuyệt đối và chốt deadline cuối về mặt mã. **VÁ MỘT PHẦN** theo tiêu chí khóa cả lớp. | Cùng handle đọc `EOCD−20` và vẫn đếm CD trước `ZipFile`. `con_lai()` kẹp join/wait, kiểm thời gian sau wait. Lỗi reader, kích thước mỗi lần đọc và `wait(timeout=5)` có ca mới. Xem phản chứng về độ phủ và thu hồi reader bên dưới. [ZIP](../scripts/tl_core/llm_route.py#L1396) · [Extract](../scripts/tl_core/llm_route.py#L1915) · [Ca](../scripts/tl_core/llm_route_test.py#L1977) |
| Lượt 39 `huong-dan-docx` | **ĐÃ VÁ THẬT** biểu hiện style | `pStyle` vắng/sai loại chặn, `rStyle` vắng bỏ qua và sai loại chặn, `basedOn` vắng dừng chuỗi và khác loại chặn. So độc lập với bộ phân giải tại ba điểm dùng. [Hướng dẫn](../docs/GOI_AGENT_DA_NEN.md#L428) · [Đặc tả](../ops/specs/llm-khoan-docx-r40.md#L385) · [Mã](../scripts/tl_core/llm_route.py#L1049) |
| Lượt 39 `ghi-chu-write-set` | **ĐÃ VÁ THẬT** | Ghi chú lease hiện hành bỏ trần 30 lượt và chỉ dẫn danh sách đã băm. Lease r39 còn câu cũ trong hồ sơ lịch sử với bia mộ trỏ r40. [Lease](../ops/leases/llm-khoan-docx-r40-g1-claude.yaml#L236) |
| #1514 K1, §2.3 và §2.38–§2.40 | **ĐÃ VÁ THẬT** hai đường ghép gốc | Dòng điểm dạng K1 gặp allowlist rồi trả `None` cho cả Điều. Sau khoản có số, dòng tiếp mở bằng `là` đi tới nhánh từ chối dòng không số. Ở nguồn mất số, `lech_nguyen_van` đòi hai vế khác rỗng. Số khoản liên tục từ 1, dấu kết và chốt số nội dòng giữ nguyên. Nhãn số trùng số khoản đã công bố và khóa ở tín hiệu. [Mã](../scripts/tl_core/llm_route.py#L1673) · [K1 nguồn](../ops/acceptance/llm-ranh-gioi-khoan/r1/review-10-codex/VERDICT.md) |
| §1 và §2.1–§2.15, §3 | **ĐÃ VÁ THẬT** các biểu hiện cũ còn thuộc hợp đồng. **HẾT ĐỐI TƯỢNG** điểm cắt/bảng/fallback cũ. | Word: `start` vắng thành 0, `startOverride` thay cấp tương ứng, bộ đếm theo numId đặt lại mọi cấp con khi tăng cấp cha. Nhảy cấp, cấp không định nghĩa, nhiều danh sách và dãy khoản khác 1..N bị chặn. DOCX nhận đúng tiêu đề đầu và đọc đến EOF, từ chối bảng, thêm tiêu đề, điểm gõ tay và câu dẫn ngoài mẫu. `KhongCauTruc` đã bị bỏ từ r5; DOCX lỗi đi thẳng rc 2. `lech_nguyen_van` so theo vị trí, số và hai vế của cả khoản; ở DOCX chỉ dò `là` trong đoạn đầu khoản. `can_nguoi_duyet` luôn true. [Đếm](../scripts/tl_core/llm_route.py#L1490) · [Vùng](../scripts/tl_core/llm_route.py#L1509) · [CLI](../scripts/tl_core/ops_misc.py#L3044) |
| §2.16–§2.26 | **ĐÃ VÁ THẬT** các chốt đã báo. Các ngoại lệ số hiệu giữ nguyên giới hạn. | Kiểm chữ gốc trước bỏ đoạn rỗng, allowlist Unicode, BOM/biên dòng, tiền tố Điều/Chương/Mục/Phần. Đọc XML gốc, đánh dấu `xml:space`, lọc gạch đơn/kép và del/moveFrom; mốc move thiếu/lệch ID bị chặn. `--markup-strict`, CAP và cờ cấu hình/profile còn ở đường số hiệu. U2, V3, W1/W3 và phần số hiệu W2 có khai giới hạn. [Markup](../scripts/tl_core/llm_route.py#L1226) · [Biên](../scripts/tl_core/llm_route.py#L1514) · [Extract](../scripts/tl_core/llm_route.py#L1975) |
| §2.27–§2.37 | **ĐÃ VÁ THẬT** các hình dạng đã khóa, riêng lớp nhãn và ngân sách xem trên. | Tra style trên tập ID xác thực; kiểm loại, khóa nội bộ, vòng `basedOn`; ngắt trong run đã bỏ và ký hiệu trong mẩu đã bỏ theo đúng thứ tự. Các mẫu nhãn r27–r35 được thay bằng allowlist §2.38 và bổ sung §2.40–§2.42; ca dương cũ phải đọc theo quyết định thu hẹp miền. [Style](../scripts/tl_core/llm_route.py#L1034) · [Allowlist](../scripts/tl_core/llm_route.py#L620) |

### Đối chiếu các finding lịch sử

Các nhóm dưới đây theo ID từng lượt trong hồ sơ và các mục thay thế. Kết quả động áp cho các fixture/đột biến còn trong suite, còn đối chiếu thiết kế áp cho mã hiện hành.

| Lượt và nguồn | Trạng thái trên r40 |
| --- | --- |
| 1–3 · `3d24751`, `38c481f`, `b0f3cb9` | **ĐÃ VÁ THẬT** A1 phần tiêu đề/khối, A2–A4, A5 phần xác thực danh sách dùng, A7–A8, B1 phần tiêu đề nguyên đoạn, B2 phần style, B3–B8, C1 phần ngắt tiêu đề, C2 phần nhãn sau Z, C3–C7. **HẾT ĐỐI TƯỢNG** A1/B1/C1 phần cắt, A5 phần ngoài Điều, A6 và B2/C2 phần bảng. |
| 4–6 · `fa3a8e2`, `3c1e143`, `6781d11` | **HẾT ĐỐI TƯỢNG** D1 phần điểm cắt, E1/E3/E4 và F1 do r7. **ĐÃ VÁ THẬT** D1 phần bỏ fallback, D2–D4, D6, E2/E5/E6, F2–F6. D5 là giới hạn Strict có chẩn đoán. |
| 7–9 · `4badb3d`, `6d28f34`, `4c647c8` | **ĐÃ VÁ THẬT** G1/G2/G4–G6, H1–H5 và J1–J5, với J2 thực hiện bằng chốt `mc:` toàn part §2.13. **HẾT ĐỐI TƯỢNG** G3 vì chặn nhảy cấp. |
| 10–12 · `674a28c`, `e1ed11f`, `f305663` | **ĐÃ VÁ THẬT** K1–K4 của #1525, L1–L6, M1–M2 theo miền hiện hành. Chốt tiền tố thay hình dạng tiêu đề của L2/M1. |
| 13–15 · `069b734`, `0447395`, `b5cff42` | **ĐÃ VÁ THẬT** N1–N3, Q1–Q2, R1–R3. Kiểm ký tự trước bỏ đoạn khóa lại R1/R3, giữ nguyên chữ nguồn theo Q2. |
| 16–18 · `7a913aa`, `8f31901`, `5ed4386` | **ĐÃ VÁ THẬT** S1–S3, T1–T2 trong write set, U1. U2 thuộc giới hạn của bộ đọc chung trên đường số hiệu. |
| 19–21 · `7c4abd7`, `8a685fe`, `3d21bd1` | **ĐÃ VÁ THẬT** V1/V2/V4, W2 DOCX, W4/W5, X1–X3 ở hình dạng gốc. V3/W1/W3 và W2 phần số hiệu đã công bố. |
| 22–24 · `fbddd47`, `30e3e07`, `b755fef` | **ĐÃ VÁ THẬT** Y1–Y3, Z1–Z4, A1–A2 ở hình dạng gốc. Hậu kiểm tên ZIP trùng vẫn chạy sau tiền kiểm số lượng. |
| 25–28 · `659d9f2`, `475fee9`, `9972282`, `0e1c112` | **ĐÃ VÁ THẬT** B2–B3, hình dạng gốc B1, C1/C2, D1 và E1. Ca dương theo miền §2.38. |
| 29–33 · `291919e`, `749e6ac`, `7e9cde7`, `571e83f`, `3278bfe` | **ĐÃ VÁ THẬT** F1/F2, G1/G2, H1–H3, I1, I2 phần nhãn có dấu đã báo, J1 và J2 với regex đã gỡ. I2 phần nhãn thiếu dấu phân biệt đã công bố. |
| 34–36 · `a3ef89a`, `8b67826`, `7b839ba` | **ĐÃ VÁ THẬT** lớp `ranh-gioi-ky-tu` và hình dạng nhãn một vế/dấu đầu dòng đã báo. Nhãn số trùng được khóa theo quyết định chủ kho. **VÁ MỘT PHẦN** với hai lớp còn mở. |
| 37–38 · `af071ea`, `418aa6a` | **ĐÃ VÁ THẬT** các hình dạng đã khóa của nhãn chữ Việt một vế, span kiểm ngoặc, số âm và ca trừ chữ trước ghép. Các ca nhãn và ngân sách lượt 38 đã chuyển thành chốt §2.41–§2.42, còn các giới hạn phép đo và biểu hiện cùng cơ chế bên dưới. |
| 39 · `9e2f419` | Hai P3 đóng theo biểu hiện gốc. Hai lớp P2 đối chiếu tại bảng trên và finding bên dưới. |

[Hồ sơ các lượt](../ops/acceptance/llm-khoan-docx/r1) · [Verdict lượt 39](../ops/acceptance/llm-khoan-docx/r1/review-39-codex/VERDICT.md)

## Findings THEO LỚP

### Lớp `ranh-gioi-khoan` [P2] — `scripts/tl_core/llm_route.py:594`, `:607`, `:613`

- **Bất biến.** Với văn bản thô, dấu hiệu phân biệt còn nhìn thấy giữa nhãn nhiều vế và thân phải dẫn tới từ chối cả Điều trong miền đã chọn. Chỉ được kết thúc việc dò nhãn khi thật sự sang vế định nghĩa hoặc gặp một trường hợp giao miền đã công bố.
- **Miền và bằng chứng đọc mã.** Cùng bộ quét nhận đầu dòng có hoặc không có số khoản. Nó dừng ở ký tự phi chữ/số đầu tiên sau các vế, kiểm ngay ký tự ấy rồi trả kết quả. Một cụm nhãn nhiều vế bọc nháy kép cân, với dấu kết nhãn ở **sau** nháy đóng, dừng tại nháy đóng nên không thấy dấu kết. Tương tự, khi một thành phần cuối được bọc ngoặc cân sau các vế trước rồi mới đến dấu kết nhãn, bộ quét dừng tại ngoặc mở. Cả nháy kép thẳng/cong và ngoặc cân đều thuộc miền mà `_dong_mo_ho` cho qua. Nếu thân sau nhãn có từ nối và dấu kết câu, `lech_nguyen_van` có thể chứng nhận nhãn là một phần thuật ngữ. Ngoài ra, nhánh thoát tại từ `là` chỉ kiểm có đệm theo sau, kể cả đệm trước chính dấu kết; `_tu_noi` cũng chưa loại vế phải mở bằng dấu phân cách như vậy. Với ca dính ngay dấu kết, mutant hiện có bị giết; hai cách đặt đệm cho cùng vai trò chưa được phân biệt. Các hình dạng này còn dấu phân biệt, nằm ngoài ba giới hạn về nhãn dính thân, nhãn chỉ ngăn bằng khoảng trắng và nhãn số trùng số khoản. [Chốt đầu dòng](../scripts/tl_core/llm_route.py#L620) · [Chốt dấu cân](../scripts/tl_core/llm_route.py#L1737) · [Phép so](../scripts/tl_core/llm_route.py#L1810)
- **Hạng P2.** Ranh giới sai có thể được nhận ở đường thô sau khi mất cấp danh sách; kết quả vẫn có tín hiệu cần duyệt. Hai P2 lượt 38–39 dùng cùng cách phân hạng. Chưa thấy bản vá này kéo cơ chế đó sang đường cấu trúc.
- **Hint patch.** Ở `dau_dong_cho_phep`, gọi một bộ phân loại trên span thân duy nhất. Bộ này giữ vị trí các vế, độ sâu ngoặc và ký tự đóng nháy, xét dấu kết trên span sau một cụm đóng cân và chỉ xác nhận `là` là từ nối nếu vế phải đã bắt đầu. Dùng cùng quyết định từ nối khi so nguyên văn đường thô. Trả trạng thái nhãn/mơ hồ trước khi dựng khoản. Một lượt quét từ trái qua phải phủ cả nhãn trần, nhãn bọc, thành phần có ngoặc và đệm trước dấu kết, không cần nhánh riêng theo số vế hay độ dài.
- **Hint test.** Ca âm cho dấu trong và sau cụm đóng cân, cả nháy thẳng/cong, thành phần bọc ngoặc, đệm trước dấu kết và hai cách lấy nguồn. Ca dương giữ thuật ngữ bọc nháy đóng rồi tới từ nối thật, chú thích nội bộ trong thuật ngữ, và dấu câu thuộc định nghĩa sau từ nối. Khi đột biến bỏ trạng thái của cụm đóng hoặc trả sớm ở mọi `là` có đệm, ca tương ứng phải đỏ. Khóa luôn thông điệp của cả hai phía trong `pham_vi_kiem`.
- **Phần giao miền.** Nếu chủ kho muốn giữ các mở đầu có dấu kết ngay sau phần bọc cân hoặc coi `là` + đệm + dấu kết là từ nối hợp lệ, cần ghi đúng hai điều này ở đặc tả và tín hiệu; người duyệt xác minh ranh giới bằng DOCX có cấp danh sách.

### Lớp `can-tai-nguyen-doc-nguon` [P2] — `scripts/tl_core/llm_route.py:1396`, `:1941`, `scripts/tl_core/llm_route_test.py:2089`

- **Bất biến.** Chốt đọc đo đúng miền và áp trước cấp phát; lỗi nguồn kết thúc có kiểm soát; ngân sách chờ, dừng đọc và thu hồi có giới hạn. Từng chốt phải có phản chứng đích để khóa bước sớm nhất áp dụng nó.
- **Miền và bằng chứng.** (1) ZIP64 dùng locator tuyệt đối như hint lượt 39. Ca mới chôn locator trong comment **member CD**, vẫn nằm trong cửa sổ tail, còn điều kiện lỗi cũ là locator nằm ngoài cửa sổ khi **archive comment EOCD** dài. Mutant có sẵn bỏ cả việc nhận locator nên bị giết; khôi phục chốt cửa sổ r39 vẫn đạt cả 64 ca. (2) Bộ chạy extract từ chối kết quả sau hạn, nhưng khôi phục `t.join(0.05)` vẫn qua cả bộ ca và 276 đột biến. Stub đo lỗi reader chỉ dùng stdout. Nhánh thu hồi `kill` và `wait(timeout=5)` thu hồi tiến trình trực tiếp. Trên các lối ra vượt trần, quá hạn và lỗi đọc, nó không có bước đóng/cancel hai reader hoặc thu hồi tiến trình con giữ bản sao handle ống. Reader là daemon, nên quá hạn có thể trả lỗi đúng nhưng vẫn để việc đọc/handle tồn tại nếu nhánh con giữ ống; chưa đo động tình huống này. `tl extract` có đường gọi transport/gws. (3) Gói qua tiền kiểm vẫn có thể lỗi ở bước mở gói hoặc member. CPython 3.13.18 ném `NotImplementedError` cho version ZIP, kiểu nén hoặc cờ ZIP không hỗ trợ; member mã hóa không có mật khẩu ném `RuntimeError`. Cả hai thoát danh sách bắt lỗi ở nhánh DOCX của `cmd_llm_khai_niem`, thành traceback thay cho rc 2 có chẩn đoán. Đây là lỗi biên đọc, được xác định khi đối chiếu với stdlib cục bộ. [Chốt ZIP](../scripts/tl_core/llm_route.py#L1409) · [Thu hồi](../scripts/tl_core/llm_route.py#L1941) · [Extract](../scripts/tl_core/extract_cache.py#L214) · [CLI](../scripts/tl_core/ops_misc.py#L3044)
- **Hạng P2.** Liên quan tính sẵn sàng của đường đọc và yêu cầu khóa chốt theo §2.41–§2.42. Các phản chứng chỉ ra lỗ độ phủ dù lệnh gate trên exact head xanh. Không suy ra sai nguyên văn từ các biểu hiện này.
- **Hint patch.** Giữ locus ZIP tại `doc_dieu_docx`: chuẩn hóa lỗi từ thao tác mở ZIP/member qua một ranh giới đọc hẹp thành `ValueError` có nguyên nhân, và giữ chốt byte/entry/locator trước mở. Trong `_chay_gioi_han`, gom mọi lối thoát vào một đường kết thúc cùng deadline đọc và ngân sách thu hồi riêng. Bảo đảm đường lỗi thu hồi cây tiến trình/endpoint thuộc sở hữu lời gọi và hoàn tất hoặc hủy reader trong ngân sách theo nền. Tránh gọi đóng ống từ luồng chính khi có thể đợi vô hạn vì reader đang giữ khóa. ZIP và I/O tiến trình cần hai vị trí vì có hai tài nguyên khác nhau; chính sách CLI vẫn quy về một lỗi nguồn có chẩn đoán.
- **Hint test.** ZIP thường tại biên số member, ZIP64 có archive comment ở cả hai phía ranh cửa sổ, sentinel và số khai lệch; stub xác nhận từ chối trước `ZipFile`. Mutant khôi phục điều kiện `i >= 20` phải đỏ. Với extract, đo hai ống đối xứng tại dưới/đúng/vượt trần, lỗi reader, EOF rồi treo, descendant giữ ống và thời hạn từng `join` bằng đồng hồ/luồng giả; bỏ phần kẹp join hoặc bỏ thu hồi phải đỏ đúng ca. Đối với lỗi I/O DOCX, ca âm ở cả mở gói và mở member phải kết thúc rc 2 trước model giả; ca dương giữ định dạng Word được hỗ trợ. Hint cần chạy lại trên Linux và Windows theo M3.

### Lớp `ve-sinh-diff-ho-so-review` [P3] — `ops/acceptance/llm-khoan-docx/r1/review-39-codex/VERDICT.md:118`

- **Bất biến.** Diff bổ sung hồ sơ review đạt cổng whitespace và byte hồ sơ vẫn đối chiếu được với bản giao đã neo.
- **Miền và bằng chứng.** `git diff --check 9e2f419 HEAD` rc 2 vì tệp mới của lượt 39 có một dòng trống thừa cuối tệp. Diff ngoài `ops` rc 0. Toàn PR cũng chứa cảnh báo lịch sử ở lượt #1525/35 và #1514/8. Đây là P3 về whitespace của hồ sơ, riêng với hai P3 style và ghi chú write set đã sửa. [Tệp mới](../ops/acceptance/llm-khoan-docx/r1/review-39-codex/VERDICT.md#L118) · [Cổng](../docs/PROTOCOL_DA_PHIEN.md#L1122)
- **Hint patch và test.** Chuẩn hóa kết tệp tại bước ghi markdown trước khi băm, rồi dùng `git diff --check` cho phần hồ sơ chưa đóng băng. Nếu byte hiện tại đã neo receipt, xử lý tại bước lưu hồ sơ để giữ bản gốc và dùng bản trình bày dẫn chiếu hash hoặc quyết định được audit. So lại hash của bản gốc và chạy diff check trên artifact mới; thêm lại dòng trống phải làm cổng đỏ.

Các hint ở trên là phương án văn bản cho Executor. Chưa áp dụng vào cây ứng viên.

## Kết quả test và đột biến

Các lệnh chạy trong clone sạch của exact head, riêng selftest đối chứng chạy trên base. Bản sao hai đột biến tách riêng và chỉ đổi một dòng mỗi bản. Log, mã thoát và diff bytes được lưu tại [scratch lượt 40](/tmp/wp1525-r40-review.xY0mYZ).

| Lệnh | Trạng thái và rc | Bằng chứng dương hoặc lỗi quan sát |
| --- | --- | --- |
| `python scripts/tl_core/llm_route_test.py` | `passed`, rc 0 | **64/64** ca và **276/276** đột biến bị giết, gồm **179/179** `wp1525_*`. Ca Điều 3 với ba kết quả lưu vẫn đạt 8/8 theo assertion có sẵn. Bộ chạy chỉ tính đột biến bị giết khi ca đích báo `TinHieuChotCa`. [Log](/tmp/wp1525-r40-review.xY0mYZ/head-llm-route.log) · [Ca 8/8](../scripts/tl_core/llm_route_test.py#L1159) · [Harness](../scripts/tl_core/llm_route_test.py#L2554) |
| `python scripts/tl.py --deterministic workflow-audit --strict --json` | `passed`, rc 0 | `ok=true`, 26 card, 11 nhóm, 60 task, 194 lệnh khả dụng, 0 lỗi/cảnh báo. Registry có **201/201** leaf được đăng ký. [Log](/tmp/wp1525-r40-review.xY0mYZ/head-workflow.log) |
| `python scripts/tl.py --deterministic golden-test --json` | `passed`, rc 0 | `ok=true`, **20/20** ca và **20/20** projection ổn định. Raw ổn định **19/20**, ca `hygiene_sweep_fixture` qua theo projection. [Log](/tmp/wp1525-r40-review.xY0mYZ/head-golden.log) |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | `passed`, rc 0 | `ok=true`, **187/187** tệp, 0 thừa/thiếu/lệch. Hash gói khớp `361a09d7cdcffdff40165dd9436e9d0c9fc3ad6b11ac1cb1fd6cbc63d35f6994`. [Log](/tmp/wp1525-r40-review.xY0mYZ/head-release.log) |
| `python ops/lease_publish.py check --root . ops/leases/llm-khoan-docx-r40-g1-claude.yaml` | `passed` cục bộ, rc 0. Hai phép đo GitHub `skipped`. | “ĐĂNG ĐƯỢC”, Issue #1525, neo `64b7f2c14776` và hạn lease đúng. Hai phép đo được công cụ ghi bỏ qua là Issue/PR và dò comment. [Log](/tmp/wp1525-r40-review.xY0mYZ/head-lease.log) |
| `python scripts/tl.py --selftest` | `failed`, rc 1 ở cả hai | Head **1774/1790**, base **1773/1789**, transport **12/12** trên cả hai. Head có `[OK] r1525_llm_khai_niem_tep_docx_cau_truc` và `[OK] r380_llm_khai_niem_bien_dau_vao`. [Log head](/tmp/wp1525-r40-review.xY0mYZ/head-selftest.log) · [Log base](/tmp/wp1525-r40-review.xY0mYZ/base-selftest.log) |
| `git diff --check 9e2f419 HEAD`; `git diff --check 9e2f419 HEAD -- . ':!ops'`; `git diff --check 695916e HEAD` | `failed` rc 2; `passed` rc 0; `failed` rc 2 | Lỗi whitespace mới ở verdict lượt 39; toàn PR còn lỗi lịch sử như finding P3. [Diff check r40](/tmp/wp1525-r40-review.xY0mYZ/diff-check-r40.log) · [Diff check PR](/tmp/wp1525-r40-review.xY0mYZ/diff-check-pr.log) |

So sánh 16 ID đỏ đã sắp bằng `cmp` ra rc 0; SHA-256 cả hai danh sách là `6c344d8f8a71b854460d8d4badd425904bdd116177ea8b3e14bd2387a2a14505`. Gồm 14 ca môi trường đã khai trong prompt, với `/tmp/.git` hiện diện và rỗng, cùng hai ca doc-claims `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` và `r268_l2_trichotomy_theo_trang_thai_object`. Delta ID đỏ bằng 0. Gate N/N vẫn đỏ. [ID head](/tmp/wp1525-r40-review.xY0mYZ/head-selftest-fail.ids) · [ID base](/tmp/wp1525-r40-review.xY0mYZ/base-selftest-fail.ids)

Hai phản chứng bổ sung dùng chính lệnh `python scripts/tl_core/llm_route_test.py` trên bản sao tạm.

| Thay đổi duy nhất | Trạng thái của đột biến và rc thật | Bằng chứng |
| --- | --- | --- |
| Khôi phục dò locator trong cửa sổ tail bằng `i >= 20` và lát cắt trước EOCD | Đột biến **sống ở ca đích**, lệnh rc 1 | **64/64** ca qua. **275/276** đột biến có sẵn bị giết, riêng neo chuỗi `wp1525_zip64_loc_trong_cua_so` biến mất nên harness ghi `KHONG AP DUOC`. Rc 1 xuất phát từ neo, không phải fixture phát hiện hồi quy. [Diff](/tmp/wp1525-r40-review.xY0mYZ/mutant-zip-locator.diff) · [Log](/tmp/wp1525-r40-review.xY0mYZ/mutant-zip-locator.log) |
| Khôi phục `t.join(0.05)`, giữ nguyên `con_lai()` ở wait và chốt deadline cuối | Đột biến **sống**, rc 0 | **64/64** ca và **276/276** đột biến có sẵn vẫn đạt. [Diff](/tmp/wp1525-r40-review.xY0mYZ/mutant-extract-join.diff) · [Log](/tmp/wp1525-r40-review.xY0mYZ/mutant-extract-join.log) |

SHA-256 log suite `9d49ee8bf33d8db949b384fd84ccd94bfb2302617df7512d8703205a5fa1f792`. Selftest head `cf1746646f1e91cfa0fafd929b08cadadc8ec8c1aad95344e75a7a402a73163e`, base `bd06de5f65b604d1cd3c11c22da59c1c71be3fb59b30bdc256da9acfdb1ebf2c`. Diff bytes từ base nghiệm thu `9d97cdb8e7a252f97874f910c1abc919c9ee46323bf9efbd74fdc5b011c3467d`, từ master đã nhập `cd02e9999182b84a6265ba843d5aa42e1b82491b622c40aa7fb96e332b73f0de`, từ r39 `fb41ba32244315befb8b22504de928e0cd2b5c8a5ec1b32fa9a5725fa92a577f`. [Diff r40](/tmp/wp1525-r40-review.xY0mYZ/r40.patch) · [Numstat r40](/tmp/wp1525-r40-review.xY0mYZ/r40.numstat)

## Không đo được

- Các hình dạng nhãn ngoài bộ ca hiện hành, việc thu hồi khi nhánh con giữ ống, và các lỗi ZIP kiểu nén/mã hóa trong findings dựa trên đọc mã. Không dựng thêm fixture hay chạy model thật. Chưa đo cửa sổ ZIP64 trên gói đại diện đúng biên mới; đột biến trên fixture có sẵn chỉ xác nhận thiếu độ phủ.
- Không có số đo tần suất export Word/Google Doc thật. Đối chiếu §2.5–§2.13 cho thấy con đoạn/run thông dụng trong bộ ca có sẵn đi đúng allowlist, gồm `t`, tab, dấu nối, bookmark, comment, ngắt trang cuối và content control. Các chặn đã công bố gồm bảng, hình, field, chú thích, ngắt mềm, đánh số kế thừa style, định dạng không hỗ trợ và Strict. Chưa xác nhận thêm dạng phổ biến bị chặn oan ngoài hợp đồng.
- `not_run` trong lượt reviewer gồm Windows bản địa, CI/provenance GitHub, `determinism-audit --strict`, `doc-claims-check --strict` độc lập và Ruff contract/lint. Các lệnh gate chạy theo mục “Cách đo” của prompt. Windows cần bằng chứng vì diff chạm `subprocess`. [ADR-0060 M3](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L41) · [Đặc tả §5](../ops/specs/llm-khoan-docx-r40.md#L548)
- Model và effort phục vụ `KHONG_DO_DUOC` trong metadata launcher đang chạy. Terminal rc và hash stdout của chính lượt này cần đọc lại sau khi launcher kết thúc. Cây làm việc Executor và PR head ngoài phạm vi quan sát offline. [Protocol §8.1](../docs/PROTOCOL_DA_PHIEN.md#L770)

## Kết luận

Readback cuối khớp exact HEAD và tree đầu tệp. Diff tracked và index rc 0 ở hai mốc. Checkout reviewer có `.review/VERDICT.md` untracked theo yêu cầu và `.codex/` ignored từ bootstrap. Hai clone chạy gate có output ignored trong `references/golden/fixtures/` và `scripts/.tl_state/` ở scratch. Snapshot chỉ chứng minh trạng thái quan sát ở hai mốc.

K1 của #1514 vẫn đóng ở hai cơ chế ghép gốc. Kết quả là **0 P0, 0 P1, 2 P2, 1 P3**. Hai lớp P3 của lượt 39 đóng, hai lớp P2 còn mở. Lượt 41/45. Verdict offline theo ngưỡng prompt là **APPROVE**. Ứng viên **chưa đủ điều kiện push/merge** theo ngưỡng 0 P1/P2/P3, cổng N/N và whitespace, cùng yêu cầu bằng chứng Windows. [Protocol §8.3](../docs/PROTOCOL_DA_PHIEN.md#L812) · [ADR-0060 M1/M3](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32)

P2_mo: 2
P3_mo: 1
VERDICT: APPROVE
