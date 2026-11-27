# Verdict packet #1514 r3 lượt 4 — Codex

reviewed_sha: e9fc10cbbc34ed5326d6e350e6a7281587b0aacb
tree_sha: 28f41ccae4db6013c310367cbc3e287864146d2a
base_sha: 64b7f2c14776d5d0e1d34a6be4725490956f5bec

VERDICT: REQUEST_CHANGES

C1 đã đóng. C2 sửa đúng ca dẫn chiếu ở cuối dòng, đồng thời mở lại một đường tách sai khoản khi dấu đánh số nội dòng kề khoảng trắng Unicode (D1, P1, kết luận đọc mã).

## Đối chiếu lượt 3 và đặc tả r3

- Checkout độc lập, detached, origin `ducthangho/tra-luat`. Base là tổ tiên của HEAD (`git merge-base --is-ancestor`, rc 0), tree base `0cc14e79cecd2ce44bc4dc6cff92cadb31fd7ee4`. Ref nhánh packet và ref origin trong bản sao cùng trỏ đúng HEAD. Lượt 3 neo `64153dbfb402bcf1d0ac7ecd614b7aa23bb57d8f`.
- Packet #1514, revision 3, generation 1, Review Class `sensitive`, lượt 4/5 tính chung. Nguồn đặc tả là blob `fb5f91dc1fec84c459b77f472156b9f954a21ee2` tại reviewed SHA. SHA-256 blob và bản trên đĩa cùng là `c3af3b110d2880a26aed97411192328e8788f5cc1b613a424a65e5d66c8b17ad`, khớp [lease r3](../ops/leases/llm-ranh-gioi-khoan-r3-g1-claude.yaml#L21). Lease còn hạn đến 11:40 UTC ngày 25-11-2026.
- Cả 20/20 đường dẫn thay đổi từ base và 11/11 từ lượt 3 thuộc 27 đường dẫn lease. Hash danh sách sắp xếp, nối và kết thúc bằng LF là `c0eef20a24e6221f63a2883b4962a2d66d3a304291c49638ab4101b06a5b39fb`, khớp lease. `git diff --check` rc 0 ở cả hai phạm vi. Bia mộ đúng hai chiều qua `da_bi_thay_the` và `thay_the_cho` cho từng cặp r1↔r2 và r2↔r3. [Lease r1](../ops/leases/llm-ranh-gioi-khoan-r1-g1-claude.yaml#L63) · [Lease r2](../ops/leases/llm-ranh-gioi-khoan-r2-g1-claude.yaml#L58) · [Lease r3](../ops/leases/llm-ranh-gioi-khoan-r3-g1-claude.yaml#L60)
- Reviewer `openai_codex / codex_cli / machine`, run `59a6d2d290ae41c4a79f186353a9e146`. `run.json` và `checkpoint.json` neo cùng HEAD và SHA-256 `8136783bbe21378ce3758b3d71f9f69ab5f0b0f6996a5b02101a7a59f88b8ada`, khớp bản đọc từ `prompt.snapshot`. Executor theo lease là Claude Code, `claude / claude_code / machine/local`. Môi trường Linux x86_64, Bash, Python 3.13.18, Git 2.43.0, Codex CLI 0.172.0, `core.abbrev=7` và sandbox `workspace-write` theo môi trường lượt chạy.

| Mục | Trạng thái | Bằng chứng |
| --- | --- | --- |
| C1 lượt 3, A2c lượt 2 và luật tiêu đề §2.6 | **ĐÃ VÁ THẬT** cho đường bỏ khoản dính tiêu đề | Sau khi chuẩn hóa khoảng trắng, dòng có tiền tố chỉ bị bỏ nếu toàn dòng khớp mẫu cho phép. Ca C1 chặn phần dư dùng từ nối khác và “là” sát nháy, đồng thời chấp nhận bốn dạng tiêu đề hợp lệ có sẵn. Trả lại kiểm tra chữ “là” làm đỏ mẫu đầu đúng lý do. D2 ghi nhận giới hạn về nhận diện tiêu đề cùng tên. [Mã](../scripts/tl_core/llm_route.py#L67) · [Ca C1](../scripts/tl_core/llm_route_test.py#L1042) |
| C2 lượt 3 và luật đánh số §2.6 | **VÁ SINH LỖI MỚI** | Regex khớp đúng biểu thức trong r3. Ca C2 đi qua và đỏ đúng lý do khi khôi phục mẫu dùng khoảng trắng qua dòng. D1 mô tả tác động của cùng thay đổi lên khoảng trắng trên chính dòng. [Mã](../scripts/tl_core/llm_route.py#L497) · [Ca C2](../scripts/tl_core/llm_route_test.py#L1056) |
| A1 lượt 2, §2.3 và §4.4 | **ĐÃ VÁ THẬT** cho biểu hiện đã đo | Nhánh câu dẫn đòi hậu tố chuẩn và `_tu_noi(ln) is None`. Đối chứng với hai câu dẫn chuẩn và dòng mở đầu kết hai chấm sai hậu tố đều đạt. Bỏ điều kiện từ nối làm ca A1 đỏ. D3 giữ lại biến thể khác đã nêu ở lượt 3. [Mã](../scripts/tl_core/llm_route.py#L540) · [Ca A1](../scripts/tl_core/llm_route_test.py#L1016) |
| A2 lượt 2, X3 của #1503 | **VÁ MỘT PHẦN** | A2a và A2c đóng trên phạm vi đã kiểm. A2b còn D1 cùng lớp tách sai khoản. [Hồ sơ lượt 2](../ops/acceptance/llm-ranh-gioi-khoan/r1/review-2-codex/VERDICT.md#L40) |
| A2a, X3b/X3c, §2.2, §2.5 và §4.2–4.3 | **ĐÃ VÁ THẬT** cho các mẫu đã nêu | Sau khi gom điểm, tập dấu kết là `.`, `!`, `?` theo §2.5. Ba đột biến phục hồi chấm phẩy, cho phép hai chấm hoặc bỏ cả chốt đều bị giết. Đối chứng khoản mở bằng hai chấm và kết bằng dòng điểm hợp lệ vẫn qua. [Mã](../scripts/tl_core/llm_route.py#L553) · [Ca X3b/X3c](../scripts/tl_core/llm_route_test.py#L985) |
| A2b, §2.5 được sửa theo §2.6 | **VÁ MỘT PHẦN** | Chốt chạy trên thân đã bỏ số khoản. Mẫu số nội dòng ASCII vẫn bị chặn, mẫu số thập phân vẫn đạt và hai đột biến tương ứng bị giết. Bản vá thu hẹp thêm tập khoảng trắng nội dòng, xem D1. [Mã](../scripts/tl_core/llm_route.py#L555) · [Ca A2b](../scripts/tl_core/llm_route_test.py#L1022) |
| A3 lượt 2, dải dấu đóng §2.2 | **ĐÃ VÁ THẬT** | Xóa cả dải dấu đóng và khoảng trắng cuối. Khôi phục cách tỉa từng bước làm đối chứng có khoảng trắng xen giữa dấu đóng bị từ chối. [Mã](../scripts/tl_core/llm_route.py#L560) · [Ca A3](../scripts/tl_core/llm_route_test.py#L1031) |
| A4 lượt 2, §1 và §4.6 | **ĐÃ VÁ THẬT** trong fixture offline | Nguồn trong fixture tách 8/8. Cả ba bản lưu `tl`, `sub`, `api` đủ 8 mục và qua bước chuẩn hóa cùng bộ so runtime. [Ca A4](../scripts/tl_core/llm_route_test.py#L1035) |
| X2, §2.1 và §4.1 | **ĐẠT** | Chốt từ ba nháy kép thẳng chạy trên dòng đã bỏ dấu đầu. Mẫu bốn nháy đỏ khi bỏ chốt, đối chứng một cặp vẫn qua. [Mã](../scripts/tl_core/llm_route.py#L581) · [Ca X2](../scripts/tl_core/llm_route_test.py#L981) |
| X4, §2.4 và §4.5 | **ĐẠT** | Ca giữ xuống dòng đạt, ca dồn hai điểm báo lệch khoản 1. Đột biến gộp khoảng trắng qua dòng làm đỏ đúng ca X4. [Mã](../scripts/tl_core/llm_route.py#L568) · [Ca X4](../scripts/tl_core/llm_route_test.py#L1003) |
| §1, phạm vi gọi model và công bố kết quả | **GIỮ NGUYÊN** cho đường gọi và cờ | Diff từ base giữ các hàm định tuyến và gọi model. Handler vẫn gắn `can_nguoi_duyet: true` và `pham_vi_kiem`, chỉ ghi kết quả qua phép so. D1 ảnh hưởng danh sách khoản dùng làm chuẩn cho chính phép so này. [Phạm vi kiểm](../scripts/tl_core/llm_route.py#L503) · [Handler](../scripts/tl_core/ops_misc.py#L3100) |

## Findings

### D1 [P1] Khoảng trắng Unicode nội dòng mở lại đường nhận tiểu mục thành khoản — `scripts/tl_core/llm_route.py:500`

**Kịch bản.** Xét lớp A2b của lượt 2, trong đó một khoản định nghĩa dài chứa tiểu mục đánh số. Tiểu mục được giữ nội dòng trong bản text và kết câu, còn một tiểu mục sau bắt đầu dòng riêng với số trùng số khoản kế tiếp. Khi dấu số nội dòng kề khoảng trắng không ngắt (U+00A0), chẳng hạn khoảng trắng dùng để giữ số và nội dung đi cùng nhau khi dàn trang, chốt r3 bỏ qua tín hiệu từng làm r2 từ chối cả nguồn. Điều kiện bổ sung để sai được nhận là tiểu mục đầu dòng có từ nối và hai vế mà phép so hiểu được.

**Căn cứ.** `ln.strip()` giữ khoảng trắng nằm giữa dòng. Bộ kiểm dấu phân cách cho qua U+00A0. Regex cũ dùng `\s` ở cả hai mép, regex r3 chỉ nhận dấu cách ASCII và tab, dù đang dò trong một dòng. Nhánh nhận số ở đầu dòng vẫn đọc số tiểu mục tiếp theo như số khoản, kiểm dãy từ 1 và dấu câu kết đều có thể qua. Đột biến bỏ chốt nội dòng trên ca A2b có sẵn đã cho thấy bộ quét trả ba khoản. `lech_nguyen_van` lấy danh sách đã tách này làm chuẩn, nên phản hồi tách cùng cách có thể ra `ok=true` và được ghi với cờ cần người duyệt. Đây là hồi quy ngay trên lớp A2b đã được xếp P1. Dấu cách không ngắt là biến thể dàn trang của hình dạng đã xét ở lượt 2, không đòi sửa nội dung định nghĩa. Độ phổ biến của tổ hợp trong corpus chưa đo được. [Tách dòng và khoản](../scripts/tl_core/llm_route.py#L521) · [Chốt nội dòng](../scripts/tl_core/llm_route.py#L555) · [Ca A2b](../scripts/tl_core/llm_route_test.py#L1022) · [So khoản](../scripts/tl_core/llm_route.py#L661) · [Ghi kết quả](../scripts/tl_core/ops_misc.py#L3103)

**Đề xuất.** Sửa §2.6 và áp quy tắc nhận diện khoảng trắng trên từng dòng vật lý của thân khoản trước khi ghép, để giữ tập khoảng trắng Unicode của r2 và vẫn không so xuyên dòng. Điều kiện đóng là cùng bắt được số thứ tự có dấu cách ASCII hoặc khoảng trắng không ngắt, chấp nhận dẫn chiếu ở cuối dòng điểm và giữ đối chứng số thập phân.

### D2 [P2] Cùng tên “Giải thích từ ngữ” có thể bị chặn vì kiểu trình bày tiêu đề — `scripts/tl_core/llm_route.py:524`

**Kịch bản và căn cứ.** Tiêu đề một dòng được trình bày toàn chữ hoa có thể khớp mẫu toàn dòng không phân biệt hoa thường, nhưng không vào nhánh đó vì tiền tố `_RE_TIEU_DE_DIEU` phân biệt hoa thường. Tiêu đề ngắt thành dòng số Điều và dòng tên riêng cũng rơi vào nhánh từ chối, vì chỉ dòng đầu được bỏ và dòng tên được xử lý như thân khoản. Khi nguồn có số, dòng tên trở thành dòng lạ trước khoản đầu. Khi mất số, nó thành một khoản thiếu dấu kết hoặc thiếu từ nối. Đây là các biến thể của chính tên điều được hỗ trợ. Đặc tả mô tả tên tiêu đề khác và giới hạn đường văn bản thô, chưa nói trực tiếp tới chữ hoa ở tiền tố hay tên tiêu đề bị xuống dòng. Phép kiểm hiện có chỉ đổi hoa thường ở phần tên sau tiền tố. [Hai regex](../scripts/tl_core/llm_route.py#L67) · [Rẽ nhánh](../scripts/tl_core/llm_route.py#L524) · [Đối chứng](../scripts/tl_core/llm_route_test.py#L1053) · [Giới hạn đã công bố](../docs/GOI_AGENT_DA_NEN.md#L373)

**Đề xuất.** Nếu mở rộng hỗ trợ, đồng bộ điều kiện hoa thường giữa hai regex và chỉ nhận dòng tên kế tiếp khi toàn dòng đúng tên cho phép. Giữ đối chứng từ chối phần dư dính khoản đầu. Nếu giữ giới hạn, ghi hai hình thức này vào tài liệu.

### D3 [P2] Hậu tố câu dẫn vẫn có thể che mất phần mở đầu của khoản không số — `scripts/tl_core/llm_route.py:545`

**Kịch bản và căn cứ.** Đây là biến thể đã nêu cuối lượt 3. Dòng mở của khoản đầu kết bằng hậu tố câu dẫn và không có từ nối cấp khoản theo bộ quét. Dòng tiếp theo tự có dạng một định nghĩa và không có dấu điểm. Chừng nào danh sách khoản còn rỗng, câu lệnh `continue` có thể bỏ dòng mở, kể cả khi trước đó đã bỏ một câu dẫn. Dòng tiếp theo trở thành khoản đầu và phép so có thể chấp nhận kết quả thiếu phần mở. Xếp P2 vì cần bản text mất số và cấu trúc trùng cả hai dấu hiệu, chưa có bằng chứng đây là hình thức khoản thông dụng. [Ghi nhận lượt 3](../ops/acceptance/llm-ranh-gioi-khoan/r1/review-3-codex/VERDICT.md#L53) · [Nhánh câu dẫn](../scripts/tl_core/llm_route.py#L545)

**Đề xuất.** Giới hạn vị trí và hình dạng của câu dẫn đầu điều. Từ chối luồng có thêm một dòng nhập nhằng cùng hậu tố trước khoản đầu.

| Lớp nguyên nhân | Biểu hiện | Hạng còn mở và điều kiện đóng |
| --- | --- | --- |
| `ranh-gioi-khoan` | X3 → A1/A2 → C1; D1, D3 | P1. C1 và mẫu A1 đã đóng. Chặn D1 với tiểu mục nội dòng có dấu cách Unicode, giữ đối chứng C2 và xác nhận điều kiện bỏ câu dẫn cho D3. |
| `dan-chieu-cuoi-dong-diem` | C2 | Đóng biểu hiện gốc tại SHA hiện tại bằng ca đích và đột biến. Tác động phụ của bản vá thuộc D1. |
| `nhan-dien-tieu-de` | D2 | P2. Xác nhận cùng tên được xử lý đúng khi đổi hoa thường hoặc ngắt dòng, hoặc khai rõ giới hạn. |

Hai lớp còn mở, gồm ba biểu hiện được nêu ở D1–D3. Giới hạn đã khai vẫn cho phép hai câu hoàn chỉnh của cùng một khoản bị coi là hai khoản nếu số bị mất và mỗi câu nằm một dòng, đều có hai vế và dấu kết hợp lệ. Khi bộ quét phân đoạn đúng, phép so theo vị trí, số lượng và hai vế giữ xuống dòng vẫn từ chối kết quả cắt ngắn định nghĩa, bỏ khoản đã nhận diện hoặc gộp mất ranh giới dòng điểm. [Quy tắc nguồn mất số](../docs/GOI_AGENT_DA_NEN.md#L368) · [Phép so](../scripts/tl_core/llm_route.py#L661)

## Kết quả test và đột biến

Log và mã thoát nằm trong `/tmp/wp1514-r4-evidence.YxpJ4UDH/`. Bytecode Python tắt. Các bản sao sạch giữ nguyên Git SHA và tree của mốc tương ứng. Phép đo tạo fixture, trạng thái và bộ đệm của công cụ nằm trong bản sao hoặc đã được chuyển ra thư mục log sau khi lệnh kết thúc.

| Lệnh | Trạng thái | rc và bằng chứng |
| --- | --- | --- |
| `python scripts/tl_core/llm_route_test.py` | `passed` | 0. **51/51 ca đạt, 94/94 đột biến bị giết**. |
| `python scripts/tl.py --deterministic workflow-audit --strict --json` | `passed` | 0. `ok=true`, 26 card, 60 task, 194 lệnh khả dụng, 0 lỗi và 0 cảnh báo. |
| `python scripts/tl.py --deterministic golden-test --json` | `passed` | 0. `ok=true`, 20/20 ca và 20/20 bản chiếu ổn định. 19/20 ca ổn định byte thô. `hygiene_sweep_fixture` có dao động byte thô, bản chiếu ổn định và fixture khai `snapshot_age_s` là trường biến động. |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | `passed` trên bản sao sạch | 0. `ok=true`, **187/187** tệp, 0 thiếu/thừa/sai, package hash khớp `d3f9a28c2e10e6e473a1e9a89214a173ec8bf429bb84e2e9f3ab9458ca11f7e6`. Lần chạy trong checkout review trả 2 và chỉ báo thêm `.review/VERDICT.md`. |
| `python ops/lease_publish.py check --root . ops/leases/llm-ranh-gioi-khoan-r3-g1-claude.yaml` | `passed` offline | 0. `ĐĂNG ĐƯỢC`, Issue #1514, neo `64b7f2c14776`, hạn 11:40 UTC. Gate offline tự khai ngoài phạm vi hai lớp đo Issue/PR và dò comment. |
| `python scripts/tl.py --deterministic determinism-audit --strict --json` | `passed` | 0. `ok=true`, 15/15 phép kiểm đạt. |
| `python scripts/tl.py --deterministic doc-claims-check --strict --json` | `failed` trên head và base | 2 trên mỗi mốc. Cùng một cờ cứng `SHA_NOT_A_COMMIT` cho `9941d8af52aeede1c78ea4e232fbe9a8d5272033` ở [protocol](../docs/PROTOCOL_DA_PHIEN.md#L1680) trong clone nông. Delta cờ cứng 0. |
| `python -B -c 'import runpy; m=runpy.run_path(".claude/dev/ci_dang_ky_test.py"); errors,count=m["loi_ruff_ci"](); print("RUFF_CONTRACT",count,errors); raise SystemExit(bool(errors) or count == 0)'` | `passed` | 0. `RUFF_CONTRACT 3 []`. Phép đọc hợp đồng pin/probe workflow, pin 0.15.15. |
| `python -m ruff check --no-cache --select F scripts/tl.py` | `failed` trên head và base, đạt tiêu chí delta | 1 trên mỗi mốc. Ruff 0.16.9 có sẵn, cùng 12 lỗi F821, stdout trùng byte, delta 0. |
| `python scripts/tl.py --selftest` | `failed` trên head và base | 1 trên mỗi mốc. **1775/1789** trên hai bản sao sạch sau khi cô lập cấu hình ký commit. Dòng ID và trạng thái ca của hai mốc trùng byte (`cmp`, rc 0). Có 14 ca đỏ ở cả hai mốc, delta 0. |

Sandbox chứa thư mục rỗng `/tmp/.git`, ứng với 8 ca `r973_bootstrap_*`, 5 ca `wp433_*` và 1 ca `wp727_tl_gws_refresh` đã nêu trong prompt. Lần đầu chạy trên bản sao sạch có cùng 1773/1789 ở head và base (rc 1). Hai ca đỏ thêm là `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` và `r268_l2_trichotomy_theo_trang_thai_object`, đều tạo commit trong repo thử. Môi trường có `commit.gpgsign=true` trong cấu hình Git toàn cục. Hai ca này qua trên cả hai mốc khi đặt `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false` riêng cho tiến trình selftest offline. Lần chạy trực tiếp trong checkout review trả rc 1, 1772/1789, thêm ca đỏ `wp44_release_bundle_topology_under_200` do tệp verdict.

### Đột biến có sẵn

Chạy `python -m pdb scripts/tl_core/llm_route_test.py` trên bản sao head. Breakpoint tại nhánh bắt `TinHieuChotCa` dòng 1285 ghi khẳng định đầu tiên đỏ cho 12 đột biến của packet. Debugger và chương trình đều rc 0. Bộ test tạo và đóng tệp đột biến trong thư mục tạm. [Harness](../scripts/tl_core/llm_route_test.py#L1265)

| Đột biến | Khẳng định đích thực sự đỏ |
| --- | --- |
| `wp1514_l3_tieu_de_chi_do_la` | C1. Tiêu đề dính khoản có từ nối khác được bỏ, nguồn không bị đánh mơ hồ. |
| `wp1514_l3_so_noi_dong_qua_dong` | C2. Số điều ở cuối dòng điểm bị chặn oan. |
| `wp1514_l2_cau_dan_bo_tu_noi` | A1. Dòng mở có từ nối lại bị bỏ như câu dẫn. |
| `wp1514_l2_cham_phay_ket_cau` | A2a. Hai mảnh sau khi xuống dòng ở chấm phẩy bị nhận là hai khoản. |
| `wp1514_l2_hai_cham_ket_cau` | X3c. Dòng mang số sau thân còn mở bằng hai chấm được nhận. |
| `wp1514_l2_bo_so_noi_dong` | A2b. Thân có số nội dòng vẫn được nhận theo dãy số khoản liên tục. |
| `wp1514_l2_so_noi_dong_nhan_thap_phan` | A2b. Đối chứng số thập phân bị từ chối. |
| `wp1514_l2_duoi_mot_luot` | A3. Khoản có khoảng trắng xen giữa dấu đóng bị từ chối. |
| `wp1514_bo_x2` | X2. Dòng có bốn nháy kép thẳng qua chốt mơ hồ. |
| `wp1514_bo_ket_cau` | X3b. Mảnh thiếu dấu câu kết bị nhận là khoản. |
| `wp1514_cau_dan_moi_hai_cham` | X3. Dòng mở sai hậu tố bị bỏ như câu dẫn. |
| `wp1514_gon_gop_dong` | X4. Kết quả dồn hai dòng điểm thành một dòng vẫn qua bộ so. |

## Không đo được

- D1–D3 là phân tích tĩnh. Chưa đo tần suất trong corpus, tổ hợp khoảng trắng Unicode và tiểu mục của D1, hay các dạng trình bày của D2 và D3 bằng ca mới. Chưa đo riêng dạng số trong ngoặc bằng ca đích. Phép thử 8/8 dùng ba bản lưu trong fixture của candidate.
- Windows bản địa §3 là `not_run` và `not_measured` trong lượt Linux offline. Suite có ca cho nhánh Windows mô phỏng. Claude/Anthropic thật, lệnh `tl llm-khai-niem` thật và GitHub/CI từ xa là `not_run`. Không có bộ test trong “Cách đo” báo `skipped`.
- Model và effort phục vụ là `KHONG_DO_DUOC` từ hiện vật khả dụng của run. Mã thoát launcher và hash stdout hoàn chỉnh cần được đọc lại khi run kết thúc.

Đọc lại `git rev-parse HEAD 'HEAD^{tree}'` cho đúng SHA và tree đã ghi. `git diff --exit-code` và `git diff --cached --exit-code` đều rc 0. `git status --porcelain=v1 --untracked-files=all --ignored=matching` ở mốc cuối vẫn có `.codex/` ignored từ đầu và có thêm `.review/VERDICT.md`. Phép so quan sát trạng thái checkout review ở hai mốc. Nội dung `.codex/` và repo của Executor ngoài phạm vi quan sát.

VERDICT: REQUEST_CHANGES
