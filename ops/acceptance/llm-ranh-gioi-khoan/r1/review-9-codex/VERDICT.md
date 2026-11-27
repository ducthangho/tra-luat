# Verdict packet #1514 r8 lượt 9 — Codex

reviewed_sha: 5aa5b34cf57a7c542491a7ff556012b629cf2a59
reviewed_tree: 9a3302246a9ce5d4621f2bd8ad413bd6835cdcbe
base_sha: 64b7f2c14776d5d0e1d34a6be4725490956f5bec

VERDICT: APPROVE

G1 và H1 đã vá đúng. Lớp `ranh-gioi-khoan` còn một P2 theo đọc mã, nên điều kiện merge của ADR-0060 M1 chưa đạt. Selftest candidate và baseline đỏ cùng 14 ca môi trường, với danh sách trạng thái trùng nhau.

## Preflight

- Checkout `ducthangho/tra-luat` detached đúng candidate. Ref nhánh cục bộ và ref theo dõi `ccr-89c0d2e2-inanqb` đều trỏ vào candidate. Baseline nghiệm thu là tổ tiên và khớp `git merge-base`. Mốc diff bản vá là cha trực tiếp `b6efff087634f5438a17f48ad12aef53f9feff2a`. Verdict lượt 8 chấm `4d357d1ad679d1a0aeea9795fe9777be8a32c1e5`.
- Đặc tả nguồn `5aa5b34cf57a7c542491a7ff556012b629cf2a59:ops/specs/llm-ranh-gioi-khoan-r8.md`, blob `ab6584ac13f3630f0ccead99b24d8aad3106c2b7`. Blob và bản local cùng SHA-256 `2c7fe5735b9557586466051b3d08200e68eb753f73e33d979450dc86bc7eebfe`, khớp lease r8/g1, blob `816b5c7d2f54321cd35eb0c63b5fefa2b685b2f6`. Lease còn hạn lúc kiểm, hết hạn `2026-11-25T15:28:00Z`. [Đặc tả](../ops/specs/llm-ranh-gioi-khoan-r8.md) · [Lease](../ops/leases/llm-ranh-gioi-khoan-r8-g1-claude.yaml)
- Cả 8 blob đặc tả khớp hash trong lease tương ứng. 7/7 cặp r1↔r2 đến r7↔r8 nối đúng `thay_the_cho` và `da_bi_thay_the`. Lease r8 ghi 8 lời gọi đã dùng trước lượt này và trần 9. SHA-256 write set 50 đường dẫn theo quy tắc LF là `8c7eeb08de6bc6a9b6ec2485c4bf942f96e80cb7af6cd74a8819aacd2d8863b4`. `git diff --name-only BASE HEAD` và `git diff --name-only b6efff0 HEAD` lần lượt cho 46 và 8 đường dẫn, đều nằm trong write set. `git diff --check b6efff0 HEAD` rc 0. `git diff --check BASE HEAD` rc 2, báo hai dấu cách cuối dòng tại ba dòng metadata tạo Markdown hard break trong hồ sơ verdict lượt 8.
- Review Class khai báo và hiệu lực đều `sensitive`. Executor `claude / claude_code / machine/local` theo lease. Reviewer `openai_codex / codex_cli / machine`, họ `openai` theo provider, run `2db0301f451b4acdb5b8268c9d680a8d`. `checkpoint.json` khớp candidate và cùng `run.json` xác nhận SHA-256 của `prompt.snapshot` là `2131046f9ab7306f4b5038e0007b08fabf2da53c7ff482b9b0f86b4a5fc6a403`. Môi trường Linux x86_64, Bash, Python 3.13.18, Git 2.43.0, Codex CLI 0.172.0, `core.abbrev=7`, sandbox `workspace-write`. Model và effort phục vụ `KHONG_DO_DUOC` từ biên nhận đang chạy. [Protocol §8.1](../docs/PROTOCOL_DA_PHIEN.md#L770)

## Đối chiếu lượt 8 và đặc tả r8

| Mục | Trạng thái | Bằng chứng |
| --- | --- | --- |
| H1 lượt 8, §2.11 | **ĐÃ VÁ THẬT** cho kịch bản H1 | Ở nguồn mất số chưa bỏ câu dẫn chuẩn, nhánh nhận điểm kiểm `len(khoan) == 1` trước thao tác nối. Điều kiện độc lập với dấu cuối dòng mở. `ca_wp1514_luot7` chặn U+FF1A, không có dấu và dấu chấm phẩy. Trên bản sao dùng mã r7, ca đỏ đúng H1 tại U+FF1A. [Mã](../scripts/tl_core/llm_route.py#L539) · [Ca](../scripts/tl_core/llm_route_test.py#L1122) |
| G1 lượt 7, §2.10 được thay bởi §2.11 | **ĐÃ VÁ THẬT** | Ca dấu hai chấm ASCII chặn cả phân đoạn và đầu ra ghép. Khi bỏ chốt vai trò, ca đỏ ở G1. Khi bỏ điều kiện về câu dẫn chuẩn, đối chứng khoản thật có điểm đỏ do bị chặn oan. Nếu dòng đầu kết `:` và đứng riêng, chốt dấu kết câu vẫn loại nó. [Mã](../scripts/tl_core/llm_route.py#L546) · [Ca](../scripts/tl_core/llm_route_test.py#L1126) |
| F2, X3, A1, D3, E2, §2.3–2.9, §4.4 | **ĐÃ VÁ THẬT** ở nhánh bỏ dòng | `fullmatch` trên toàn dòng đã gộp khoảng trắng, chỉ tại vị trí 0 sau tiêu đề. Ca sẵn có đo hậu tố giống câu dẫn nhưng có nội dung dư, câu dẫn lặp hoặc muộn, và ba mẫu câu dẫn chuẩn. Đột biến nới chủ ngữ đỏ đúng F2. Nhánh giữ rồi ghép còn J1. [Mã](../scripts/tl_core/llm_route.py#L560) · [Ca D3](../scripts/tl_core/llm_route_test.py#L1062) · [Ca F2](../scripts/tl_core/llm_route_test.py#L1112) |
| F1, A2b, C2, D1, E1, §2.5–2.9 | **ĐÃ VÁ THẬT** với các biểu hiện đã báo | Ca F1 chặn khoảng trắng trước dấu và dấu sát trích dẫn, các ca trước giữ đối chứng thập phân và dẫn chiếu cuối dòng, chặn U+00A0 và dấu dính chữ. Đột biến thu về regex r5 đỏ đúng F1. Phạm vi tập bao được đối chiếu bên dưới. [Hai mẫu](../scripts/tl_core/llm_route.py#L488) · [Ca F1](../scripts/tl_core/llm_route_test.py#L1102) |
| A2c, C1, D2, §2.5–2.7 | **ĐÃ VÁ THẬT** đối với tiêu đề dính nội dung | Bộ quét chỉ bỏ tiêu đề khớp toàn dòng. Ca C1 chặn phần dư và giữ bốn mẫu đối chứng. Tên điều khác, tiền tố viết hoa và tên xuống dòng riêng đã được khai là giới hạn. [Mã](../scripts/tl_core/llm_route.py#L530) · [Ca C1](../scripts/tl_core/llm_route_test.py#L1042) |
| X2, §2.1 và §4.1 | **ĐẠT** | Chặn từ ba nháy kép thẳng sau khi bỏ dấu đầu dòng. Ca bốn dấu bị chặn, đối chứng một cặp qua. [Mã](../scripts/tl_core/llm_route.py#L599) · [Ca X2](../scripts/tl_core/llm_route_test.py#L977) |
| X3b, X3c, A2a, A3, §2.2 và §2.5, §4.2–4.3 | **ĐẠT** | Chốt chạy sau ghép điểm, tỉa cả dải trắng và dấu đóng, chỉ nhận chấm, chấm than, chấm hỏi. Ca đích chặn mảnh thiếu dấu kết và khoản chưa khép trước số mới. Đối chứng điểm cuối kết câu và khoảng trắng xen dấu đóng đều qua. [Mã](../scripts/tl_core/llm_route.py#L569) · [Ca](../scripts/tl_core/llm_route_test.py#L985) · [Ca A3](../scripts/tl_core/llm_route_test.py#L1030) |
| X4, §2.4 và §4.5 | **ĐẠT** | Ca ghép các dòng điểm thành một dòng báo lệch, đối chứng giữ xuống dòng qua. Đường tiếp dòng mở bằng “là” ở nguồn có số giữ hành vi Q3. [Mã](../scripts/tl_core/llm_route.py#L555) · [Ca X4](../scripts/tl_core/llm_route_test.py#L1003) |
| A4, §1 và §4.6 | **ĐẠT** offline | Fixture Điều 3 tách đủ tám khoản. Ba kết quả lưu `tl`, `sub` và `api` đều khớp 8/8. [Ca A4](../scripts/tl_core/llm_route_test.py#L1035) |
| B1 lượt 1, §1, §2.7 và §5 | **ĐÃ VÁ THẬT** ở bề mặt reviewer | Lease và launcher khớp Codex CLI. Diff giữ đường gọi model, VERSION, `can_nguoi_duyet: true` và `pham_vi_kiem`. Thay đổi selftest chỉ miễn so mode POSIX trên Windows và giữ phép so dữ liệu JSON. [Đầu ra](../scripts/tl_core/ops_misc.py#L3104) · [Selftest](../scripts/tl_selftest.py#L32294) |

**Tập bao đánh số nội dòng.** Trên một dòng đã tách, cả hai regex có cùng dạng lõi, gồm số trong ngoặc hoặc số trần với khoảng trắng tùy ý trước chấm hay ngoặc đóng. Vì dòng đã được tách, `\s*` của mẫu đầu dòng và `[^\S\n]*` theo nghĩa khoảng trắng trong mẫu nội dòng dùng cùng miền khoảng trắng tại vị trí đó. Mẫu đầu dòng cho phép dấu số ở cuối dòng và nhánh ngoặc còn cho phép chữ số đứng sát sau ngoặc đóng. Mẫu nội dòng loại cả hai trường hợp, loại xuống dòng và kiểm thêm bên trái phải khác ký tự từ, chấm và phẩy. Do đó tập bao chỉ đúng trong miền còn lại sau các ngoại lệ §2.9. Ngoại lệ sau chữ số áp cả cho nhánh ngoặc, dù lý do tránh thập phân chỉ giải thích trực tiếp nhánh dấu chấm. Chốt bên trái áp ở vị trí bắt đầu của lần khớp. Với số trong ngoặc, nhánh số trần còn có thể bắt đầu sau ngoặc mở. [Hai regex](../scripts/tl_core/llm_route.py#L488) · [§2.9](../ops/specs/llm-ranh-gioi-khoan-r8.md#L83)

**Chặn oan.** Các đối chứng câu dẫn chuẩn, tiêu đề hợp lệ và khoản có điểm sau câu dẫn chuẩn đều qua. Biến thể khác mẫu cho phép của câu dẫn, tiêu đề tách dòng, từ nối khác “là”, ký hiệu mã trùng dấu số và khoản đầu mất số có điểm khi thiếu câu dẫn chuẩn đều thuộc giới hạn đã khai. Trong các nguồn và ca có sẵn, tôi chưa xác lập được dạng phổ biến nào bị chặn oan ngoài các giới hạn đó. [Giới hạn người dùng](../docs/GOI_AGENT_DA_NEN.md#L368)

## Findings

### J1 [P2] Câu dẫn phụ ngoài danh sách vẫn có thể bị giữ và ghép thành khoản — `scripts/tl_core/llm_route.py:549,560,566`

**Kịch bản.** Nguồn mất số mở đầu bằng câu dẫn chuẩn. Tiếp theo là lời dẫn cho một nhóm thuật ngữ, chứa từ “là” đứng riêng ngoài ngoặc trước dấu phân cách, rồi đến các dòng điểm mà vai trò thực là định nghĩa riêng. Dòng điểm cuối có dấu kết câu. Cùng đường xử lý mở khi nguồn không có câu dẫn chuẩn nhưng lời dẫn phụ xuất hiện sau một khoản thực.

**Căn cứ.** `bo_cau_dan` lưu việc đã bỏ câu dẫn chuẩn cho toàn nguồn. Khi cờ này bật, hoặc khi đã có hơn một khoản, chốt r8 cho nối điểm vào khối hiện tại. Lời dẫn phụ ngoài danh sách đã được nhánh mất số thêm như một khoản. Kiểm dấu kết dùng đuôi điểm cuối. `_tu_noi` vẫn có thể chọn từ nối ở lời dẫn phụ, còn `lech_nguyen_van` so đầu ra với khối đã ghép. Một đầu ra chép đủ hai vế, đúng số thứ tự do bộ quét gán và đúng xuống dòng có thể qua dưới dạng một định nghĩa. §2.11 đã đóng đúng vị trí nêu trong H1 nhưng đường này còn trái cam kết §2.9 rằng nguồn có câu dẫn ngoài danh sách bị chặn. Các ca D3/F2 kiểm việc bỏ dòng, các ca H1/G1 kiểm ghép ở khoản đầu khi chưa có câu dẫn chuẩn. Đối chứng H1/G1 xác nhận nhánh vẫn cho phép ghép sau câu dẫn chuẩn. Kịch bản J1 được suy ra từ luồng mã, chưa chạy với đầu vào riêng. [Phân đoạn](../scripts/tl_core/llm_route.py#L539) · [Chọn từ nối và so khoản](../scripts/tl_core/llm_route.py#L658) · [§2.9–2.11](../ops/specs/llm-ranh-gioi-khoan-r8.md#L78)

**Hạng P2.** Tác động là nhận sai nhóm định nghĩa trong một bố cục thô có điều kiện, tương tự H1. Cần đồng thời có nguồn mất số, lời dẫn phụ phân tích được thành hai vế, các dấu điểm được nhận và đầu ra chép khớp khối. Cờ duyệt ranh giới vẫn bắt buộc. ADR-0060 M1 yêu cầu đóng P2 trước merge. [Verdict lượt 8](../ops/acceptance/llm-ranh-gioi-khoan/r1/review-8-codex/VERDICT.md#L35) · [ADR-0060 M1–M2](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32)

**Đề xuất.** Quyết định có được nối điểm hay không dựa trên vai trò xác lập được của từng dòng mở khối. Nếu văn bản thô còn cho phép hiểu dòng mở là lời dẫn nhóm hoặc khoản thật, từ chối khối hoặc yêu cầu đầu vào có ranh giới cấu trúc. Phép kiểm đóng lớp cần giữ đối chứng khoản thật có điểm và đo lời dẫn phụ ở cả hai vị trí nói trên, cùng các ca hiện có kiểm bỏ nhầm dòng và đánh số nội dòng.

| Lớp | Lịch sử | Trạng thái và phép kiểm đóng lớp |
| --- | --- | --- |
| `ranh-gioi-khoan` | F1/F2 trên `aed16f390f4adf59dde5718bff170c5cddd44cbb`, G1 trên `0ec7ca05b8fb9cc2cfd32a299f6522d9cc473c63`, H1 trên `4d357d1ad679d1a0aeea9795fe9777be8a32c1e5`, J1 trên candidate | **VÁ MỘT PHẦN**, cao nhất P2. H1 đóng và J1 mở trong cùng nhánh giữ rồi ghép của lớp. Biểu hiện mở **1→1**, lớp đóng **0/1**. Kiểm đóng lớp gồm nhánh bỏ dòng, điều kiện nối điểm theo từng khối, và phạm vi đánh số nội dòng đã khai. |

**Các đường còn lại theo đọc mã.** Khi phân đoạn đã đúng, bộ so bắt đầu ra tự bỏ, tráo, cắt hoặc gộp khoản bằng kiểm số lượng, thứ tự và hai vế từng khoản, giữ xuống dòng ở bên trong mỗi vế. Với nguồn thô mất số, một khoản đã bị ngắt thành nhiều dòng đều có hai vế và dấu kết, hoặc một dấu điểm xuất sai tại ranh giới, vẫn có thể làm chính bộ phân đoạn cắt hoặc ghép sai. Lời dẫn lạ đứng thành dòng riêng cũng có thể được tính là một khoản nếu nó có đủ hình dạng của một định nghĩa hoàn chỉnh. Đây là các đường bản thân văn bản thô không đủ chứng minh ranh giới, thuộc phạm vi người dùng cần duyệt. J1 chỉ ra lỗ cụ thể trong chốt câu dẫn của packet. [Phân đoạn](../scripts/tl_core/llm_route.py#L516) · [Bộ so](../scripts/tl_core/llm_route.py#L679) · [Giới hạn](../docs/GOI_AGENT_DA_NEN.md#L368)

## Kết quả test và đột biến

Log và mã thoát nằm ở `/tmp/wp1514-review-Lo0zSd3f/`. Các lệnh chạy offline trên exact candidate trừ khi ghi rõ mốc khác. Cache bytecode đã tắt.

| Lệnh | Trạng thái | Mã thoát và bằng chứng dương |
| --- | --- | --- |
| `python scripts/tl_core/llm_route_test.py` | `passed` | 0. **55/55 ca qua, 103/103 đột biến bị giết**. `focused.log`. |
| `python scripts/tl.py --deterministic workflow-audit --strict --json` | `passed` | 0. `ok=true`, 26 card, 60 task, 194 lệnh hiện diện, 0 lỗi, 0 cảnh báo. `workflow.log`. |
| `python scripts/tl.py --deterministic golden-test --json` | `passed` | 0. `ok=true`, 20/20 ca đạt, 20/20 bản chiếu ổn định. Byte thô 19/20 ổn định, khác biệt duy nhất là `snapshot_age_s` đã khai ở `hygiene_sweep_fixture`, không có drift ngoài khai báo. `golden.log`. |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | `passed` trên bản sao sạch | 0. `ok=true`, 187/187 tệp, 0 sai, thiếu hoặc thừa. Package hash khớp `f94f3cf583a21a08c4e4d6a67cf6a174b18fd217239d56f765d468365454bcb1`. `release-clean.log`. Lần đầu trong checkout review rc 2 vì thêm `.review/VERDICT.md`, là tệp thừa duy nhất và được ghi sớm theo prompt. |
| `python ops/lease_publish.py check --root . ops/leases/llm-ranh-gioi-khoan-r8-g1-claude.yaml` | `passed` cục bộ | 0. `ĐĂNG ĐƯỢC`, Issue #1514, neo `64b7f2c14776`, hạn `2026-11-25T15:28:00Z`. `lease.log`. |
| `python scripts/tl.py --selftest` | `failed` trên candidate và baseline | 1 mỗi lượt. Cả hai **1.775/1.789**, transport **12/12**. `cmp` của 1.801 dòng trạng thái/mã ca rc 0. Cùng 14 ca đỏ khi `/tmp/.git` rỗng hiện diện như prompt nêu, gồm 8 `r973_bootstrap_*`, 5 `wp433_*` và `wp727_tl_gws_refresh`. `r380_llm_khai_niem_bien_dau_vao` qua ở cả hai. Delta 0. Điều kiện N/N của §6 chưa đạt. |

Selftest ban đầu ở checkout có verdict cho rc 1, **1.773/1.789**. Đo lại trên hai bản sao riêng, cùng `core.abbrev=7` và `GIT_CONFIG_GLOBAL=/dev/null`. Hai ca đỏ thêm của lượt đầu, `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` và `r268_l2_trichotomy_theo_trang_thai_object`, đều qua ở hai bản sao. `/tmp/.git` giữ nguyên. Baseline có tree `0cc14e79cecd2ce44bc4dc6cff92cadb31fd7ee4`.

- `selftest-clean-head.log` có SHA-256 `9335ae09a16a0b7d3fe295c07abdd054cdf00549ce1cac63062e331ee6da8821`.
- `selftest-clean-base.log` có SHA-256 `a39e85411ef1b5702e8bece1743a980cd3e46c537b24b89bee466b98fdfacbac`.
- Hai bản trích bằng `rg '^  \[(OK|FAIL)\]'` có cùng SHA-256 `4d9b0711e0fb5bf3946f9daaee37dd0d2ab93e79377dbe2ce465b60187422e4e`.
- `mutation-signals.log` có SHA-256 `be66a3e8addf50f52ef13d9455fccc0ae7b1951806f0c1e44c969a32864a69ed`. `guard-r7.log` có SHA-256 `62d253faab9cb85cd6c26fba2fc7efc6169b0e4e11daf2319c2c6024319be24c`.

`DOT_BIEN` dùng module sao trong thư mục tạm, đòi đúng một neo và chỉ đếm đột biến chết bởi `TinHieuChotCa` của ca đích. Đọc tín hiệu bằng `python -B -m pdb scripts/tl_core/llm_route_test.py`, dừng tại nhánh bắt `TinHieuChotCa` ở dòng 1378. Rc 0 và suite exit status 0 trong `mutation-signals.log`. [Harness](../scripts/tl_core/llm_route_test.py#L1358)

| Đột biến có sẵn | Ca và tín hiệu quan sát được |
| --- | --- |
| `wp1514_l8_bo_chot_vai_tro` | `ca_wp1514_luot7` đỏ G1. Khối ASCII `:` bị giữ và ghép. |
| `wp1514_l8_vai_tro_bo_qua_cau_dan` | `ca_wp1514_luot7` đỏ ở đối chứng. Khoản thật có điểm sau câu dẫn chuẩn bị chặn. |
| `wp1514_l6_so_lieu_ke_dang_sau` | `ca_wp1514_luot6` đỏ F1. Thay regex bằng mẫu r5 làm lọt số có khoảng trắng trước dấu. |
| `wp1514_l6_cau_dan_mo_rong_chu_ngu` | `ca_wp1514_luot6` đỏ F2. Mở rộng chủ ngữ làm dòng có nội dung dư bị bỏ như câu dẫn. |

Phản chứng riêng cho H1 dùng bản sao nguyên văn hai tệp đã có. Chép suite ở candidate, đặt bên cạnh blob `llm_route.py` của `b6efff0` rồi chạy `python -B /tmp/wp1514-review-Lo0zSd3f/guard-r7/llm_route_test.py`. Rc 1, 54/55 ca. Ca duy nhất đỏ là `ca_wp1514_luot7`, đúng assertion H1 tại U+FF1A sau khi hai assertion G1 đã qua. Bốn neo đột biến phụ thuộc cấu trúc r8 vắng ở bản r7, nên 99/103 ở lượt phản chứng này không phải kết quả kiểm `DOT_BIEN` của candidate. `guard-r7.log`.

## Không đo được

- J1, các dấu phân cách ngoài mẫu có sẵn và tần suất chặn oan trong corpus chưa có phép chạy riêng. Phạm vi trong prompt chỉ cho chạy ca có sẵn và mô tả đường mới bằng lời. Lượt này ghi rõ các suy luận từ luồng mã.
- Windows `required` theo §3 và ADR-0060 M3. Diff toàn packet có `_os380.name` chỉ vào tên alias của `os`, đổi đường chạy test theo hệ điều hành. Windows bản địa và Windows CI exact candidate `not_run` trong lượt này, bằng chứng `not_measured`. Run `45542712141` và `45553156011` là mốc lịch sử. [Đặc tả §3](../ops/specs/llm-ranh-gioi-khoan-r8.md#L105) · [ADR-0060 M3](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L43)
- `determinism-audit --strict`, `doc-claims-check --strict` và Ruff F delta trong §6 là `not_run` theo phạm vi phép đo của prompt. CI từ xa, xác minh GitHub và gọi model thật đều `not_run`. Đây là review offline theo checkout được giao. Không có lệnh nào trong sáu lệnh prompt bị `skipped`.
- Trạng thái terminal, rc launcher và SHA-256 stdout đã đóng của lượt review cần đọc từ hiện vật đúng run sau khi tiến trình thoát.

## Readback

`git rev-parse HEAD 'HEAD^{tree}'` xác nhận SHA/tree tại mốc đầu và cuối. `git diff --exit-code` và `git diff --cached --exit-code` đều rc 0 trong checkout được giao và hai bản sao selftest. Sau khi chuyển fixture golden và state tự sinh sang scratch, `git status --porcelain=v1 --untracked-files=all --ignored=matching` của checkout được giao chỉ còn `.codex/` rỗng có sẵn và `.review/VERDICT.md`. Phép kiểm xác nhận trạng thái quan sát được tại các mốc. Repository nguồn của Executor nằm ngoài checkout được giao.

## Kết luận nội dung và điều kiện merge

0 P0, 0 P1, 1 P2, 0 P3 mở. H1 và G1 đã đóng. J1 giữ lớp `ranh-gioi-khoan` mở, nên chưa đạt điều kiện merge theo ADR-0060 M1. Đây là lượt Codex 9/9 và chạm Review Rescue Checkpoint. [ADR-0060 M1](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32) · [Protocol §12](../docs/PROTOCOL_DA_PHIEN.md#L1097)

P2_mo: 1

VERDICT: APPROVE
