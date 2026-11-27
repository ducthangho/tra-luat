# Verdict packet #1514 r4 lượt 5 — Codex

reviewed_sha: 9541e023bc5c0df8d346f2e5caaa54993a0aa60a

reviewed_tree: ed33cd131c362b9287f95b0a8674e5b79e40b010

**APPROVE theo ngưỡng review nội dung của lượt 5.** Không phát hiện P0/P1. D1 và D3 đã đóng trên ca đích, D2 được khai đúng giới hạn, sửa selftest Windows đúng phạm vi. Hai P2 dưới đây là suy luận từ mã. Điều kiện merge theo ADR-0060 M1 vẫn còn hai P2 mở. Selftest và doc-claims-check cùng đỏ trên head và base, và Windows bản địa trên exact head chưa đo được.

## Đối chiếu lượt 4 và đặc tả r4

Packet #1514 revision 4, generation 1, `sensitive`. Lease còn hạn tại preflight lúc 05:24 UTC ngày 25-11-2026. Đây là lượt 5/5 của packet. Checkout detached trên bản sao riêng của `ducthangho/tra-luat`. Base `64b7f2c14776d5d0e1d34a6be4725490956f5bec` là tổ tiên của HEAD, tree `0cc14e79cecd2ce44bc4dc6cff92cadb31fd7ee4`. Bản vá lượt này tính từ `e9fc10cbbc34ed5326d6e350e6a7281587b0aacb`.

Đặc tả r4 lấy từ blob `62389932e1de0f58ee8c4626f101796903d10ab7` tại reviewed SHA. SHA-256 của blob và tệp trên đĩa đều là `088701e2e7f3847ec19f139d6972712dd6c386f5dfd7948b7e724775d4e52525`, khớp lease r4. Cả 26/26 đường dẫn từ base và 12/12 từ lượt 4 thuộc 30 đường dẫn lease. SHA-256 của danh sách write set đã sắp xếp và nối LF là `d1bd89326dbfc62ad702199c8b1c2cbf77da1f0b407200eff40442283726f8f2`. Ba cặp bia mộ r1↔r2, r2↔r3, r3↔r4 đều khớp `da_bi_thay_the` và `thay_the_cho`. Cả hai `git diff --check` đều rc 0.

Reviewer `openai_codex / codex_cli / machine`, launcher run `584eec0b442b40748223595ada36263a`. `run.json` và `checkpoint.json` neo HEAD và prompt SHA-256 `fb9318c2b863127827ffb037434729dbe88237f11ef315463173eea94e241600`, trùng bản đọc từ `prompt.snapshot`. Executor theo lease là `claude / claude_code / machine/local`. Môi trường Linux x86_64, Bash, Python 3.13.18, Git 2.43.0, Codex CLI 0.172.0, `core.abbrev=7`, sandbox `workspace-write`.

| Mục | Trạng thái | Bằng chứng |
| --- | --- | --- |
| D1 lượt 4, A2b và C2, §2.5–2.7 | **ĐÃ VÁ THẬT** cho khoảng trắng Unicode nội dòng | `[^\S\n]` ở cả hai mép nhận U+00A0 mà không khớp `\n`. Mẫu D1 qua trên head, phục hồi regex ASCII làm chính khẳng định D1 đỏ. Ca C2 vẫn nhận dẫn chiếu ở cuối dòng điểm. Ca A2b vẫn chặn số nội dòng ASCII và nhận số thập phân. E1 ghi nhận dạng dấu số khác với D1. [Mã](../scripts/tl_core/llm_route.py#L488) · [Ca D1](../scripts/tl_core/llm_route_test.py#L1068) |
| D2 lượt 4, §2.7 | **ĐÃ KHAI ĐÚNG GIỚI HẠN** | Cả đặc tả và tài liệu người dùng ghi tiền tố `ĐIỀU` viết hoa và tên điều xuống dòng riêng. Với hai hình thức tiêu đề đứng riêng đã nêu, regex tiền tố phân biệt hoa thường và bộ quét chỉ bỏ tối đa một dòng tiêu đề. [Đặc tả](../ops/specs/llm-ranh-gioi-khoan-r4.md#L59) · [Tài liệu](../docs/GOI_AGENT_DA_NEN.md#L379) |
| D3 lượt 4, §2.7 | **ĐÃ VÁ THẬT** cho câu dẫn lặp hoặc muộn | Sau khi bỏ tiêu đề, chỉ vị trí 0 trong các dòng có nội dung được qua nhánh bỏ câu dẫn. Với nguồn mất số, dòng thứ hai trùng hậu tố vẫn ở thân và dấu hai chấm cuối làm nguồn bị từ chối. Với nguồn có số, dòng lạ trước khoản đầu bị từ chối. Câu dẫn chuẩn duy nhất vẫn qua. Phục hồi điều kiện cũ làm ca D3 đỏ. E2 xem xét riêng dòng đầu duy nhất. [Mã](../scripts/tl_core/llm_route.py#L522) · [Ca D3](../scripts/tl_core/llm_route_test.py#L1071) |
| B1 lượt 1, bề mặt reviewer | **ĐÃ VÁ THẬT** | Lease r4 khai `codex_cli / machine`, khớp prompt, launcher và CLI của lượt này. [Lease](../ops/leases/llm-ranh-gioi-khoan-r4-g1-claude.yaml#L10) |
| X2, §2.1 và §4.1 | **ĐẠT** | Chốt kiểm từ ba nháy kép thẳng sau khi gỡ dấu đầu dòng. Mẫu bốn nháy đạt ca từ chối, đối chứng một cặp qua. Bỏ chốt làm đỏ mẫu bốn nháy. [Mã](../scripts/tl_core/llm_route.py#L583) · [Ca](../scripts/tl_core/llm_route_test.py#L981) |
| X3b/X3c, A2a và A3, §2.2 đã sửa theo §2.5, §4.2–4.3 | **ĐẠT** | Sau khi gom điểm và tiếp dòng, mỗi khoản phải có dấu kết `.`, `!` hoặc `?` sau khi tỉa cả dải đuôi. Ca đích chặn mảnh gãy, khoản còn mở và chấm phẩy cuối. Đối chứng khoản mở bằng hai chấm có điểm cuối kết câu, cùng mẫu dấu đóng xen khoảng trắng, vẫn qua. Các đột biến tương ứng đỏ đúng ca. [Mã](../scripts/tl_core/llm_route.py#L553) · [Ca](../scripts/tl_core/llm_route_test.py#L985) |
| X3 và A1, §2.3, §2.5, §4.4 | **ĐẠT** cho các ca gốc | Câu dẫn cần hậu tố chuẩn và thiếu từ nối cấp khoản. Cả hai câu dẫn chuẩn qua, dòng mở sai hậu tố và dòng mở đã có từ nối bị chặn. Bỏ từng điều kiện đều làm đỏ ca đích. [Mã](../scripts/tl_core/llm_route.py#L546) · [Ca](../scripts/tl_core/llm_route_test.py#L1007) |
| A2c và C1, §2.6 | **ĐÃ VÁ THẬT** cho tiêu đề dính khoản | Chỉ bỏ tiêu đề khớp cả dòng với mẫu cho phép. Đối chứng bốn hình thức tiêu đề hợp lệ qua. Khôi phục cách chỉ dò chữ “là” làm đỏ ca phần dư chứa khoản dùng từ nối khác. [Mã](../scripts/tl_core/llm_route.py#L67) · [Ca](../scripts/tl_core/llm_route_test.py#L1042) |
| X4, §2.4 và §4.5 | **ĐẠT** | So thuật ngữ và định nghĩa theo vị trí và giữ ranh giới dòng trong từng vế. Đối chứng giữ dòng qua. Đột biến gộp trắng xuyên dòng làm đỏ mẫu định nghĩa dồn hai điểm. [Mã](../scripts/tl_core/llm_route.py#L570) · [Ca](../scripts/tl_core/llm_route_test.py#L1000) |
| A4, §1 và §4.6 | **ĐẠT** offline | Fixture Điều 3 tách 8/8. Cả ba bản lưu `tl`, `sub`, `api` có 8 mục qua chuẩn hoá và so nguyên văn. [Ca](../scripts/tl_core/llm_route_test.py#L1035) |
| §1, phạm vi runtime | **ĐẠT** | Diff sản phẩm chỉ thay nhận diện và phép so khoản. Các hàm gọi model và `ops_misc.py` giữ nguyên. Handler chỉ ghi `--out` khi danh sách lệch rỗng, luôn gắn `can_nguoi_duyet: true` và `pham_vi_kiem`. [Phạm vi kiểm](../scripts/tl_core/llm_route.py#L504) · [Handler](../scripts/tl_core/ops_misc.py#L3100) |
| Selftest Windows, §2.7 và §3 | **ĐÚNG PHẠM VI khi đọc diff** | Chỉ phép so mode 0644 được bỏ qua khi `os.name == "nt"`. Mọi nền vẫn đòi ghi được JSON, đọc lại `dieu == "15"` và rc 0. Ngoài `nt` vẫn kiểm cả mode. Hàm ghi nguyên tử không đổi. Kết quả Windows trên exact head là `not_measured`. [Selftest](../scripts/tl_selftest.py#L32289) · [Điều kiện trả về](../scripts/tl_selftest.py#L32345) |

## Findings

### E1 [P2] Dấu số dính thân có thể lọt qua chốt đánh số nội dòng — `scripts/tl_core/llm_route.py:489`, `scripts/tl_core/llm_route.py:501`

**Kịch bản và căn cứ.** Đọc tĩnh cho thấy bộ nhận số ở đầu dòng cho phép số và dấu chấm dính với chữ tiếp theo, còn chốt nội dòng đòi khoảng trắng sau dấu số. Với văn bản thô đã dồn một tiểu mục vào dòng trước, mất khoảng cách giữa dấu số và nội dung, rồi để tiểu mục sau thành dòng riêng, chốt nội dòng có thể bỏ qua tín hiệu đầu. Nếu dòng sau bắt đầu đúng số khoản kế tiếp, cả hai mảnh đều có dấu kết và hai vế hợp lệ, nó có thể trở thành một khoản trong chuẩn so. Để lọt cần đồng thời làm mất ranh giới trình bày và khoảng cách trong nội dòng, có số trùng dãy khoản và có đủ hai vế. Chưa có bằng chứng đây là một hình thức soạn khoản thông dụng. P2 theo phạm vi dữ liệu thô và kết quả vẫn mang cờ cần duyệt.

**Đề xuất.** Nếu mở lại lớp này, đối chiếu cú pháp nhận số đầu dòng với tín hiệu ở nội dòng. Giữ đối chứng số thập phân và số dẫn chiếu cuối dòng điểm. [Tách khoản](../scripts/tl_core/llm_route.py#L533) · [Kiểm sau phân đoạn](../scripts/tl_core/llm_route.py#L553)

### E2 [P2] Dòng đầu có nội dung vẫn có thể bị bỏ khi trùng hậu tố câu dẫn — `scripts/tl_core/llm_route.py:546`

**Kịch bản và căn cứ.** Ở vị trí đầu sau tiêu đề, nhánh bỏ dòng vẫn kiểm hậu tố. Một dòng mở không có số mà chứa nội dung thực chất và kết thúc bằng hậu tố chuẩn có thể bị bỏ nếu bộ dò không thấy “là” cấp khoản. Chẳng hạn về cấu trúc, dấu hai chấm ở phần mở khiến `_tu_noi` dừng trước khi tới phần còn lại. Nếu dòng kế tiếp tự tạo được một định nghĩa và phần sau vẫn có cấu trúc hợp lệ thì phép so không còn đối chiếu dòng đã bỏ. Tình huống cần chính dòng thân đầu không số mang hình dạng câu dẫn và thân còn lại tự đứng được. Đây là suy luận trên nguồn mơ hồ, chưa có bằng chứng về một kiểu trình bày thông dụng. P2 vì kết quả vẫn kèm cờ cần duyệt ranh giới. Ca D3 đã đóng đường bỏ câu dẫn thứ hai.

**Đề xuất.** Nếu xử lý tiếp, xác thực cả hình dạng câu dẫn đầu điều hoặc lấy ranh giới từ nguồn có cấu trúc. [Mẫu hậu tố](../scripts/tl_core/llm_route.py#L493) · [Dò từ nối](../scripts/tl_core/llm_route.py#L642) · [So khoản](../scripts/tl_core/llm_route.py#L663)

| Lớp nguyên nhân | Biểu hiện và trạng thái |
| --- | --- |
| `ranh-gioi-khoan` | D1 và D3 đóng trên biểu hiện lượt 4 tại `e9fc10c`. E1 và E2 là hai biểu hiện còn mở theo đọc tĩnh, mức cao nhất P2, lần lượt ở cú pháp số và câu dẫn. Đóng bằng phép kiểm xác nhận tín hiệu số được xử lý nhất quán và rằng dòng nội dung đầu không bị bỏ. |
| `dan-chieu-cuoi-dong-diem` | C2 vẫn đóng. Đối chứng qua và đột biến cho quét qua dòng làm nó đỏ. |
| `nhan-dien-tieu-de` | D2 đã được khai ở §2.7 và tài liệu người dùng. |

Ngoài E1 và E2, với nguồn mất số, hai câu hoàn chỉnh của cùng khoản nằm trên hai dòng có thể bị nhận là hai khoản khi mỗi dòng tự có hai vế và dấu kết. Đây là hệ quả của quy tắc mỗi dòng một khoản và giới hạn ranh giới đã công bố. Khi phân đoạn nguồn đúng, phép so vị trí, số lượng và cả hai vế loại trường hợp thiếu khoản, tráo khoản, cắt nội dung và mất ranh giới dòng điểm. Trong phần đọc tĩnh, chưa xác lập một dạng “Giải thích từ ngữ” thông dụng bị từ chối oan ngoài các giới hạn đã khai. Từ nối “là” dính dấu hai chấm cũng có thể bị chặn do regex đòi khoảng trắng hoặc hết chuỗi. Tần suất và đầu ra trường hợp này chưa đo được. [Quy tắc nguồn thô](../docs/GOI_AGENT_DA_NEN.md#L368) · [Regex từ nối](../scripts/tl_core/llm_route.py#L488) · [Phép so](../scripts/tl_core/llm_route.py#L663)

## Kết quả test và đột biến

Log, stdout/stderr và mã thoát ở `/tmp/wp1514-r5-evidence.Jq2pGwZ0/`. Các bộ test chạy trên bản sao cục bộ sạch, detached trên SHA và tree tương ứng. Tắt ghi bytecode Python. Chạy release-verify trước các cổng khác để phép kiểm kiểm kê chỉ thấy cây giao review. Hai lượt selftest dùng cùng cấu hình tiến trình `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false` để fixture tạo commit không phụ thuộc cấu hình ký của máy. Phần này không sửa Git config toàn cục.

| Lệnh | Trạng thái | rc và bằng chứng |
| --- | --- | --- |
| `python scripts/tl_core/llm_route_test.py` | `passed` | 0. **52/52 ca đạt, 96/96 đột biến bị giết.** |
| `python scripts/tl.py --deterministic workflow-audit --strict --json` | `passed` | 0. `ok=true`, 26 card, 60 task, 194 lệnh khả dụng, 0 lỗi, 0 cảnh báo. |
| `python scripts/tl.py --deterministic golden-test --json` | `passed` | 0. `ok=true`, 20/20 ca và 20/20 bản chiếu ổn định. 19/20 ổn định byte thô. `hygiene_sweep_fixture` dao động ở lần so byte thô và khai `snapshot_age_s` là trường biến động. |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | `passed` | 0. `ok=true`, 187/187 tệp, danh sách thiếu/thừa/sai đều rỗng. Package hash khớp `edb97cef5bbb5f5a191b8aca947b522201fa36b089ddcc7da40b619999bd64ed`. |
| `python ops/lease_publish.py check --root . ops/leases/llm-ranh-gioi-khoan-r4-g1-claude.yaml` | `passed` offline | 0. `ĐĂNG ĐƯỢC` với Issue #1514, neo `64b7f2c14776`, hạn `2026-11-25T11:40:00Z`. Lệnh báo phạm vi đo chỉ gồm các chốt cục bộ. |
| `python scripts/tl.py --selftest` | `failed` trên head và base | 1 trên mỗi mốc. Cả hai **1775/1789**, dòng ID và trạng thái trùng byte (`cmp`, rc 0). Cùng 14 ca đỏ thuộc các nhóm `r973_bootstrap_*` (8), `wp433_*` (5) và `wp727_tl_gws_refresh` (1) trong sandbox có `/tmp/.git` rỗng như prompt đã nêu. Delta ca đỏ 0. Ca `r380_llm_khai_niem_bien_dau_vao` đều `[OK]` trên Linux. |
| `python scripts/tl.py --deterministic determinism-audit --strict --json` | `passed` | 0. `ok=true`, 15/15 phép kiểm đạt. |
| `python scripts/tl.py --deterministic doc-claims-check --strict --json` | `failed` trên head và base | 2 trên mỗi mốc. Cùng một cờ cứng `SHA_NOT_A_COMMIT` cho `9941d8af52aeede1c78ea4e232fbe9a8d5272033` tại dòng 1680 của protocol. Object vắng trong clone nông. Cờ cứng delta 0. |
| `python -B -c 'import runpy; m=runpy.run_path(".claude/dev/ci_dang_ky_test.py"); errors,count=m["loi_ruff_ci"](); print("RUFF_CONTRACT",count,errors); raise SystemExit(bool(errors) or count == 0)'` | `passed` | 0. `RUFF_CONTRACT 3 []`, pin workflow 0.15.15. |
| `python -m ruff check --no-cache --select F scripts/tl.py` | `failed` trên head và base, tiêu chí delta đạt | 1 trên mỗi mốc. Ruff 0.15.15, cùng 12 F821, hai log trùng byte, delta 0. |

### Đột biến có sẵn

`python -m pdb scripts/tl_core/llm_route_test.py` đo thêm nhánh bắt `TinHieuChotCa` tại dòng 1304 cho 14 đột biến tên `wp1514_*`. Log `head-llm-route-pdb.log` ghi thông báo của khẳng định đích, debugger rc 0 và chương trình rc 0. Bộ test tự tạo đột biến trong thư mục tạm, mỗi đột biến nạp được và chỉ tính bị giết khi ca đích phát tín hiệu đúng loại. [Harness](../scripts/tl_core/llm_route_test.py#L1284)

| Đột biến | Khẳng định đích đỏ |
| --- | --- |
| `wp1514_l4_chi_cach_ascii` | D1. Khôi phục bộ nhận khoảng trắng ASCII làm nguồn đánh số nội dòng kề U+00A0 bị nhận thành ba khoản. |
| `wp1514_l4_cau_dan_moi_vi_tri` | D3. Khôi phục điều kiện cũ làm dòng câu dẫn thứ hai bị bỏ. |
| `wp1514_l3_tieu_de_chi_do_la` | C1. Tiêu đề có phần dư dính khoản dùng từ nối khác bị bỏ. |
| `wp1514_l3_so_noi_dong_qua_dong` | C2. Dẫn chiếu số điều cuối dòng điểm bị chặn. |
| `wp1514_l2_cau_dan_bo_tu_noi` | A1. Dòng mở có từ nối bị bỏ như câu dẫn. |
| `wp1514_l2_cham_phay_ket_cau` | A2a. Hai mảnh sau ngắt dòng ở chấm phẩy bị nhận thành hai khoản. |
| `wp1514_l2_hai_cham_ket_cau` | X3c. Dòng mang số sau khoản còn mở bằng hai chấm bị nhận. |
| `wp1514_l2_bo_so_noi_dong` | A2b. Thân có số nội dòng đi qua. |
| `wp1514_l2_so_noi_dong_nhan_thap_phan` | A2b. Đối chứng số thập phân bị chặn. |
| `wp1514_l2_duoi_mot_luot` | A3. Khoản có khoảng trắng xen giữa dấu đóng bị chặn. |
| `wp1514_bo_x2` | X2. Dòng có bốn nháy kép thẳng đi qua. |
| `wp1514_bo_ket_cau` | X3b. Mảnh thiếu dấu kết bị nhận thành khoản. |
| `wp1514_cau_dan_moi_hai_cham` | X3. Dòng mở sai hậu tố bị bỏ như câu dẫn. |
| `wp1514_gon_gop_dong` | X4. Định nghĩa dồn hai dòng điểm đi qua phép so. |

## Không đo được

- Windows bản địa §3 trên exact head là `not_run` và `not_measured`. Đặc tả ghi run `45542712141` có ca `r380_llm_khai_niem_bien_dau_vao` đỏ trong `gate (windows-latest)`. Snapshot được giao chưa có log ghim exact head cho `gate-registry (windows-latest)` và dòng `CI_DANG_KY scripts/tl_core/llm_route_test.py`. Phép đo Linux và đọc diff chưa xác nhận kết quả trên Windows. [Đặc tả](../ops/specs/llm-ranh-gioi-khoan-r4.md#L64)
- E1, E2 và khả năng chặn dạng từ nối “là” sát dấu hai chấm mới được đọc tĩnh. Tần suất trong corpus, phản chứng bằng ca mới và đối chiếu corpus ngoài fixture Điều 3 chưa đo. Phép đo D1 và D3 dùng các ca và đột biến đã có.
- Claude/Anthropic thật, `tl llm-khai-niem` thật và GitHub/CI từ xa là `not_run`. Không có bộ test trong “Cách đo” báo `skipped`. Cổng không đạt §6 được ghi `failed` ở bảng trên.
- Model và effort phục vụ là `KHONG_DO_DUOC` từ metadata hiện có. Run vẫn đang ghi khi verdict được hoàn tất, nên mã thoát launcher và SHA-256 của stdout hoàn chỉnh cần đọc từ hiện vật terminal của chính run.

Đọc lại `git rev-parse HEAD 'HEAD^{tree}'` xác nhận đúng SHA và tree đã ghi. `git diff --exit-code` và `git diff --cached --exit-code` đều rc 0. Snapshot cuối của checkout review có `.codex/` ignored như mốc đầu và thêm `.review/VERDICT.md`. Các tệp sinh khi chạy test nằm trên bản sao tạm. Phép kiểm nói về trạng thái quan sát được tại hai mốc. Nội dung `.codex/` và checkout Executor ở ngoài phạm vi quan sát.

VERDICT: APPROVE
