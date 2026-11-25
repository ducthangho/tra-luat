# Verdict packet #1514 r9 lượt 10 — Codex

reviewed_sha: fcb12b3873c3bec2c339029136243ed2c804ce05
reviewed_tree: addd6a844c311dbbb34b1b02ee4e91f7788f8de0
base_sha: 64b7f2c14776d5d0e1d34a6be4725490956f5bec
base_tree: 0cc14e79cecd2ce44bc4dc6cff92cadb31fd7ee4

## Phạm vi và preflight

- PR #1517, revision 9, generation 1, class `sensitive`. Checkout detached, origin `ducthangho/tra-luat`, `core.abbrev=7`. Merge base của hai SHA là đúng `base_sha`. Lease còn hiệu lực lúc preflight, hạn `2026-11-25T15:46:00Z`. Hash SHA-256 của đặc tả khớp `9b5e02ad6cd703561b2e177aee75aae88c5bf0b8fa4230a1dc85f4edb51d120a`. Lượt 10/10 theo lease với 9 lời gọi trước đó.
- `git diff --name-status 64b7f2c HEAD` có 51 đường dẫn, tất cả thuộc 55 đường dẫn trong write set r9. Bốn đường dẫn còn lại là verdict tổng và ba tệp hồ sơ lượt 10. Hash write set đã sắp xếp khớp lease và cả 9 hash đặc tả đều khớp lease tương ứng. Diff `acedac5..fcb12b3` có tám đường dẫn, cũng đều thuộc lease r9. Tám cặp lease kề nhau đều khớp hai chiều `thay_the_cho` / `da_bi_thay_the`; r1 có tiền nhiệm rỗng, r9 là đầu chuỗi hiện hành. [Lease r9](../ops/leases/llm-ranh-gioi-khoan-r9-g1-claude.yaml) · [Đặc tả r9](../ops/specs/llm-ranh-gioi-khoan-r9.md)
- Reviewer `openai_codex / codex_cli / machine`, run `5bff6270a6b7479d940e543e2b3a9d59`. `run/5bff6270/run.json` và checkpoint cùng neo exact head và prompt hash `bb72d3a3e6899a90bf0160746ee4241ddc86ee3e4ddb4a5b89b9de10a9357602`. Executor ghi trong lease là `claude / claude_code / machine/local`, tương ứng `anthropic_claude` trong bảng provider. Lease nêu phiên giao việc `session_015GtxrZQYT3Vt8PJdXrjEKg`. Môi trường reviewer là Linux, Python 3.13.18, Git 2.43.0, Codex CLI 0.172.0, sandbox `workspace-write`. [Nhận dạng provider](../ops/KE_HOACH_THI_CONG_DA_PROVIDER.md#L26)

## Đối chiếu lượt 9 và đặc tả r9

| Mục | Trạng thái | Bằng chứng |
| --- | --- | --- |
| J1 lượt 9, §2.12 | **ĐÃ VÁ THẬT** đối với kịch bản đã báo | Ở nguồn mất số, điểm trước khoản đầu trả `None` ở chốt khoản đang mở. Mọi điểm sau đó trả `None` ở chốt r9, kể cả sau câu dẫn chuẩn và giữa nguồn. Tiếp dòng mở bằng “là” chỉ chạy ở nguồn có số. `ca_wp1514_luot9` đo ba vị trí và giữ đối chứng mỗi khoản một dòng. Khoản có số kèm điểm vẫn qua. [Mã](../scripts/tl_core/llm_route.py#L539) · [Ca J1](../scripts/tl_core/llm_route_test.py#L1145) |
| H1 lượt 8, G1 lượt 7, §2.10–2.11 đã được §2.12 thay thế | **ĐÃ VÁ THẬT** đối với các kịch bản đã báo | Chốt điểm ở nguồn mất số áp dụng ở mọi vị trí và độc lập với ký tự cuối dòng mở. Ca có ASCII `:`, U+FF1A, dấu chấm phẩy và câu dẫn thiếu dấu phân cách đều đỏ ở phép kiểm nguồn như mong đợi. Đối chứng khoản có số mang điểm qua. [Ca G1/H1](../scripts/tl_core/llm_route_test.py#L1125) |
| F2, E2, D3, A1, X3, §2.9 và §4.4 | **ĐÃ VÁ THẬT** ở nhánh bỏ dòng | Gộp khoảng trắng rồi `fullmatch` cả dòng ở vị trí 0 sau khi xử lý tiêu đề. Dòng giống hậu tố câu dẫn nhưng có nội dung dư, câu dẫn lặp hoặc đến muộn không được bỏ. Ca dương kiểm các câu dẫn trong danh sách. Cách giữ dòng vẫn còn K1 ở nguồn có số. [Chốt câu dẫn](../scripts/tl_core/llm_route.py#L559) · [Ca F2](../scripts/tl_core/llm_route_test.py#L1105) |
| F1, E1, D1, C2, A2b, §2.9 | **ĐÃ VÁ THẬT** đối với các biểu hiện đã báo | Các ca sẵn có kiểm dấu số dính chữ, U+00A0, khoảng trắng trước dấu, dấu sát nháy và giữ đối chứng số thập phân, số cuối dòng. Tập bao theo nghĩa đen vẫn có các ngoại lệ đã ghi ở dưới. [Regex](../scripts/tl_core/llm_route.py#L488) · [Ca E1/F1](../scripts/tl_core/llm_route_test.py#L1084) |
| C1, A2c, D2, §2.5–2.7 | **ĐÃ VÁ THẬT** đối với tiêu đề dính nội dung | Tiêu đề có tiền tố hợp lệ chỉ được bỏ khi cả dòng thuộc hình dạng được phép. Ca C1 có phản chứng dư nội dung và bốn tiêu đề đối chứng. Tiền tố viết hoa, tên khác và tên đứng dòng riêng thuộc giới hạn đã khai. [Chốt tiêu đề](../scripts/tl_core/llm_route.py#L533) · [Ca C1](../scripts/tl_core/llm_route_test.py#L1045) |
| X2, §2.1 và §4.1 | **ĐẠT** | Từ ba dấu nháy kép thẳng trong nội dung sau khi gỡ dấu đầu dòng bị chặn. Ca có bốn dấu bị từ chối, đối chứng một cặp qua. [Chốt nháy](../scripts/tl_core/llm_route.py#L604) · [Ca X2](../scripts/tl_core/llm_route_test.py#L977) |
| X3b/X3c, A2a, A3, §2.2, §2.5, §4.2–4.3 | **ĐẠT** theo các ca đặc tả | Sau khi ghép, tỉa cả dải khoảng trắng và dấu đóng rồi yêu cầu `.`, `!` hoặc `?`. Ca dòng gãy chưa kết thúc, dấu chấm phẩy và khoản mở ngay trước số kế bị từ chối. Đối chứng điểm cuối đúng dấu và đuôi xen khoảng trắng qua. [Chốt dấu câu](../scripts/tl_core/llm_route.py#L569) · [Ca A2/A3](../scripts/tl_core/llm_route_test.py#L1012) |
| X4, §2.4 và §4.5 | **ĐẠT** | Ca ghép các dòng điểm báo lệch. Đối chứng giữ xuống dòng và ca Q3 tách trước tiếp dòng “là” đều qua. [So hai vế](../scripts/tl_core/llm_route.py#L677) · [Ca X4](../scripts/tl_core/llm_route_test.py#L1003) |
| A4, §1 và §4.6 | **ĐẠT** offline | Fixture Điều 3 tách đủ tám khoản. Ba đầu ra đã lưu `tl`, `sub`, `api` cùng khớp 8/8. [Ca A4](../scripts/tl_core/llm_route_test.py#L1038) |
| B1 lượt 1, §1, §2.7 và §5 | **ĐÃ VÁ THẬT** ở bề mặt được giao | Launcher và lease cùng khai `codex_cli`. Diff giữ định tuyến model, VERSION, `can_nguoi_duyet: true` và `pham_vi_kiem`. Selftest vẫn so dữ liệu và chỉ so mode 0644 trên POSIX. [Đầu ra](../scripts/tl_core/ops_misc.py#L3100) · [Selftest](../scripts/tl_selftest.py#L32294) |

**Tập bao đánh số.** Trên một dòng đã tách, hai mẫu cùng có số trong ngoặc hoặc số trần kèm chấm/ngoặc đóng. Khoảng trắng giữa số trần và dấu có cùng miền trên dòng. Mẫu đầu dòng nhận dấu số ở cuối dòng và nhánh ngoặc vẫn nhận chữ số sát ngay sau ngoặc đóng. Mẫu nội dòng loại cả hai, loại vị trí ngay trước xuống dòng và thêm điều kiện bên trái trước lần khớp, gồm ký tự từ, chấm và phẩy. Nhánh số trần có thể bắt số trong ngoặc từ sau ngoặc mở nếu hậu tố cho phép. Tuyên bố “tập bao” chỉ đúng trong miền còn lại sau các ngoại lệ §2.9. Lý do tránh số thập phân giải thích trực tiếp nhánh dùng chấm. Trong nhánh ngoặc, hậu tố chữ số còn có thể là đầu nội dung. [Hai mẫu](../scripts/tl_core/llm_route.py#L488) · [§2.9](../ops/specs/llm-ranh-gioi-khoan-r9.md#L83)

**Chặn oan.** Dạng câu dẫn khác về loại văn bản, cách diễn đạt, chữ hoa/thường hoặc dấu câu đều nằm trong giới hạn “mọi câu dẫn khác” của §2.9. Chuỗi tiêu đề, dấu ngoặc/trích dẫn, dấu kết, từ nối khác “là”, đánh số nội dòng và điểm ở nguồn mất số có giới hạn được ghi trong đặc tả hoặc tài liệu người dùng. Trong nguồn có sẵn chưa xác lập được một dạng phổ biến bị chặn oan ngoài các giới hạn đó. [§2 của đặc tả](../ops/specs/llm-ranh-gioi-khoan-r9.md#L20) · [Tài liệu người dùng](../docs/GOI_AGENT_DA_NEN.md#L368)

## Findings

### K1 [P2] Số khoản liên tục vẫn cho lời dẫn nhóm hoặc dòng mất số nhập vào một khoản — `scripts/tl_core/llm_route.py:539`

**Kịch bản.** Sau câu dẫn chuẩn, một dòng mang số thực tế mở một nhóm định nghĩa, có chữ “là” đứng ngoài ngoặc trước dấu phân cách. Các điểm sau đó mang định nghĩa riêng. Điểm cuối kết câu. Nếu các số đầu dòng nhìn thấy vẫn liên tục, dòng mở nhóm trở thành thuật ngữ và toàn bộ các điểm thành định nghĩa của nó. Một đường ghép khác xuất hiện khi một dòng định nghĩa mất dấu số giữa các mục còn số. Nếu dòng ấy mở bằng “là” và mục ngay trước chưa có từ nối, bộ quét có thể ghép nó như tiếp dòng. Điều kiện tương tự áp dụng khi dòng mở bằng “là” là lời nối của một nhóm đứng sau dòng mang số chỉ nêu nhãn nhóm, rồi các định nghĩa riêng xuất hiện ở các điểm.

**Căn cứ.** Chỉ một kết quả khớp `_RE_SO_KHOAN` đã bật `co_so` cho cả nguồn. Kiểm số liên tục chỉ quan sát các marker đã nhận, nên không phát hiện dòng mất số ở cuối hoặc giữa các marker vẫn liên tục, hay điểm là định nghĩa riêng nằm trong một mục có số. Nhánh điểm nối mọi điểm vào khoản đang mở. Nhánh tiếp dòng chỉ đòi đầu dòng “là” và khoản cũ chưa có từ nối. Dấu kết được kiểm sau ghép. `_tu_noi` tìm từ nối trước điểm đầu, kể cả trên dòng ghép, và phép so sử dụng chính khối đã ghép. Đầu ra chép đúng hai vế, giữ xuống dòng và có số mục đúng theo bộ quét có thể nhận `ok=true` và được ghi `--out`. Số liên tục và khớp nguyên văn của các khối đó chưa phân biệt được vai trò định nghĩa riêng của dòng bị nhập. Đây là suy luận đọc mã, trên cùng cơ chế giữ rồi ghép của J1. [Hai nhánh ghép](../scripts/tl_core/llm_route.py#L539) · [Chọn từ nối](../scripts/tl_core/llm_route.py#L656) · [So kết quả](../scripts/tl_core/llm_route.py#L683) · [Đầu ra](../scripts/tl_core/ops_misc.py#L3103)

**Hạng P2.** Hậu quả là gán sai nhóm thuật ngữ trong bố cục thô có điều kiện. Để vượt kiểm, nguồn cần đồng thời qua chốt số, dấu câu và từ nối, đầu ra phải khớp khối đã ghép. Cờ duyệt ranh giới vẫn xuất hiện. Mức ảnh hưởng tương ứng J1/H1 và M1 yêu cầu đóng P2 trước merge. [Verdict lượt 9](../ops/acceptance/llm-ranh-gioi-khoan/r1/review-9-codex/VERDICT.md#L39) · [Protocol §8](../docs/PROTOCOL_DA_PHIEN.md#L645) · [ADR-0060 M1–M2](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32)

**Đề xuất.** Kiểm vai trò của từng dòng trước khi nối, dùng cấu trúc nguồn khi có và từ chối các khối có hai cách phân đoạn khi chỉ có văn bản thô. Tiêu chí đóng lớp cần đo cả định nghĩa riêng mang dấu điểm và dòng mở “là” trong nguồn có số, cùng đối chứng khoản có điểm và tiếp dòng Q3 hợp lệ.

| Lớp | Lịch sử | Trạng thái và phép kiểm đóng lớp |
| --- | --- | --- |
| `ranh-gioi-khoan` | F1/F2 trên `aed16f390f4adf59dde5718bff170c5cddd44cbb`, G1 trên `0ec7ca05b8fb9cc2cfd32a299f6522d9cc473c63`, H1 trên `4d357d1ad679d1a0aeea9795fe9777be8a32c1e5`, J1 trên `5aa5b34cf57a7c542491a7ff556012b629cf2a59` và K1 trên `fcb12b3873c3bec2c339029136243ed2c804ce05` | **VÁ MỘT PHẦN**, hạng cao nhất P2. J1, H1 và G1 đã đóng ở nguồn mất số. K1 còn hai đường nhập dòng ở nguồn có số. Số finding đang mở 1→1, số lớp đóng 0/1. Đóng lớp cần phân biệt vai trò trước khi ghép và giữ bằng chứng dương các chốt bỏ dòng, đánh số nội dòng. |

**Các đường phân đoạn khác theo đọc mã.** Với phân đoạn đúng, kiểm đủ số lượng, thứ tự và hai vế chặn đầu ra tự bỏ, cắt hoặc gộp. Nếu nguồn mất số chứa một dòng lời dẫn lạ có đủ hai vế và dấu kết như định nghĩa hoàn chỉnh, bộ quét có thể giữ nó thành một khoản riêng. Tương tự, một khoản đã bị ngắt thành nhiều dòng mà mỗi dòng đều đủ hai vế và dấu kết có thể bị tách thành nhiều khoản. Ở nguồn có số, mất quan hệ thụt lề có thể biến một dấu số tiểu mục trùng số khoản kế thành marker cấp khoản nếu mục trước đã kết câu. Những trường hợp cùng hình dạng thô này thuộc phạm vi người dùng phải xác nhận ranh giới. Các lỗi cắt vế do một cụm nối chứa chính chữ “là” cũng thuộc phép quy ước dùng chữ “là” đầu tiên ngoài ngoặc. [Phân đoạn](../scripts/tl_core/llm_route.py#L516) · [Quy tắc từ nối](../scripts/tl_core/llm_route.py#L655) · [Phạm vi đã công bố](../scripts/tl_core/llm_route.py#L512)

## Kết quả test và đột biến

Log và mã thoát của các lệnh đo nằm tại `/tmp/wp1514-review10.iXDLoMLz/`. Dùng hai clone cục bộ detached ở exact head và base, cùng Git `core.abbrev=7`. Tắt bytecode Python. Release verify đo trên bản sao sạch để verdict được ghi sớm không đi vào kiểm kê gói.

| Lệnh | Trạng thái | Mã thoát và bằng chứng dương |
| --- | --- | --- |
| `python scripts/tl_core/llm_route_test.py` | `passed` | rc 0, **56/56 ca**, **102/102 đột biến bị giết**. `head-llm-route.log` |
| `python scripts/tl.py --deterministic workflow-audit --strict --json` | `passed` | rc 0, `ok=true`, 26 card, 60 task, 194 lệnh hiện diện, 0 lỗi và 0 cảnh báo. `head-workflow.log` |
| `python scripts/tl.py --deterministic golden-test --json` | `passed` | rc 0, `ok=true`, **20/20** ca đạt, 20/20 bản chiếu ổn định. Byte thô 19/20 ổn định. Ca `hygiene_sweep_fixture` khai phần biến động `snapshot_age_s` và có `diff={}` sau chiếu. `head-golden.log` |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | `passed` | rc 0, `ok=true`, **187/187** tệp, các danh sách sai, thiếu và thừa đều rỗng. Package hash khớp `af442cf14e0a773dbd471569f79c7d9c2be0a476cf7d4ec3c549f41391cabd9b`. `head-manifest.log` |
| `python ops/lease_publish.py check --root . ops/leases/llm-ranh-gioi-khoan-r9-g1-claude.yaml` | `passed` cục bộ | rc 0, “ĐĂNG ĐƯỢC”, Issue #1514, neo `64b7f2c14776`, hạn `2026-11-25T15:46:00Z`. Lệnh báo hai lớp kiểm GitHub nằm ngoài phạm vi của `check`. |
| `python scripts/tl.py --deterministic determinism-audit --strict --json` | `passed` | rc 0, `ok=true`, **15/15** phép đạt. `head-determinism.log` |
| `python scripts/tl.py --deterministic doc-claims-check --strict --json` | `failed` trên head và base | rc 2 mỗi lượt, 131 tệp quét mỗi lượt, cùng một cờ cứng `SHA_NOT_A_COMMIT` cho `9941d8af52aeede1c78ea4e232fbe9a8d5272033` ở `docs/PROTOCOL_DA_PHIEN.md:1680`. Object vắng trong checkout shallow được giao. Delta cờ cứng bằng 0. `{head,base}-doc-claims.log` |
| `python -B -c …` gọi `loi_ruff_ci()` trong `.claude/dev/ci_dang_ky_test.py` theo adapter | `passed` | rc 0, `RUFF_CONTRACT 3 []`. Phép kiểm pin/probe workflow. `head-ruff-contract.log` |
| `python -m ruff check --no-cache --select F --output-format json scripts/tl.py` | `failed` trên head và base, tiêu chí delta đạt | Ruff 0.15.15, rc 1 mỗi lượt, cùng 12 F821 và 0 F401. Output JSON sau bỏ tiền tố đường dẫn tuyệt đối có cùng SHA-256 `1d22192d3432b5a7d4fe204392569505d679bf63d2ea4d578b0f27bcaecc51fe`. `{head,base}-ruff-tl.log` |
| `python -m ruff check --no-cache --select F --output-format json scripts/tl_core/llm_route.py scripts/tl_core/llm_route_test.py` | `passed` | Ruff 0.15.15, rc 0, danh sách chẩn đoán rỗng. `head-ruff-module.log` |
| `git diff --check` và `git diff --check acedac5 HEAD` | `passed` | rc 0 cho cả hai. Phép bổ sung `git diff --check 64b7f2c HEAD` rc 2, ba dấu ngắt dòng cứng Markdown bằng khoảng trắng ở verdict lượt 8, dòng 3–5. |
| `python scripts/tl.py --selftest` | `failed` trên head và base | rc 1 mỗi lượt, **1.773/1.789** trên cả hai. Transport **12/12**. Cùng 16 ca đỏ, tập ID và trạng thái trùng nhau. `{head,base}-selftest.log` |

`DOT_BIEN` ghi từng bản đột biến vào thư mục tạm, yêu cầu đúng một neo và chỉ tính bị giết khi ca đích ném `TinHieuChotCa`. Chạy lại bằng `python -B -m pdb scripts/tl_core/llm_route_test.py`, đặt điểm dừng tại dòng 1392 cho ba đột biến dưới đây. Rc trình gỡ lỗi 0, rc suite 0 và tổng vẫn 56/56, 102/102. SHA-256 log `head-mutation-breakpoints.log` là `5987b3c434b68634fd1d72e2f6a9dc569c7eda427f8f3fe2f96f55d9224a115e`. [Harness](../scripts/tl_core/llm_route_test.py#L1372)

| Đột biến có sẵn | Ca đích và bằng chứng |
| --- | --- |
| `wp1514_l9_cho_diem_nguon_mat_so` | `ca_wp1514_luot9` chạm assertion J1. Bỏ chốt mới làm lời dẫn sau câu dẫn chuẩn và hai điểm được ghép thành một khoản. |
| `wp1514_l6_so_lieu_ke_dang_sau` | `ca_wp1514_luot6` chạm assertion F1. Thay bằng mẫu r5 làm lọt số có khoảng trắng trước dấu. |
| `wp1514_l6_cau_dan_mo_rong_chu_ngu` | `ca_wp1514_luot6` chạm assertion F2. Mở rộng phần chủ ngữ làm dòng có nội dung dư bị bỏ. |

Đối chiếu 1.801 dòng trạng thái ca của hai lượt bằng `cmp` sau khi lọc `[OK]` và `[FAIL]`, rc 0. Cùng 14 ca đã nêu trong prompt với `/tmp/.git` rỗng hiện diện, gồm 8 `r973_bootstrap_*`, 5 `wp433_*`, `wp727_tl_gws_refresh`. Hai ca đỏ thêm là `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` và `r268_l2_trichotomy_theo_trang_thai_object`, đều đỏ trên base. Delta ca đỏ bằng 0. `r380_llm_khai_niem_bien_dau_vao` qua trên cả hai. Điều kiện selftest N/N của §6 vẫn thiếu. SHA-256 của bản đối chiếu trạng thái là `dc0321b2fcd600bdba7566a467c1d699b39d5e171f17b0b0082664d6c815454d`.

## Không đo được

- K1 và các dạng ngoài ca sẵn có là suy luận từ luồng mã. Tần suất của các dạng đó và tỷ lệ chặn oan trên corpus chưa đo trong lượt này.
- Windows là `required` theo §3 và ADR-0060 M3 vì diff đổi hành vi selftest theo `os.name`. Windows CI và phép đối chứng Windows bản địa trên exact head là `not_run`, kết quả `not_measured`. Run `45542712141` và `45553156011` là bằng chứng lịch sử trên các SHA trước. [Đặc tả §3](../ops/specs/llm-ranh-gioi-khoan-r9.md#L116) · [ADR-0060 M3](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L43)
- Xác minh GitHub, CI từ xa và gọi model thật là `not_run` theo phạm vi offline. Model và effort phục vụ ở launcher là `KHONG_DO_DUOC` tại thời điểm reviewer ghi verdict. Trạng thái terminal, rc con và SHA-256 stdout của lượt reviewer đọc từ đúng run sau khi tiến trình kết thúc.

## Readback và kết luận

`git rev-parse HEAD 'HEAD^{tree}'` khớp đầu và cuối phiên, rc 0. `git diff --exit-code` và `git diff --cached --exit-code` rc 0. Status checkout review chỉ có `.codex/` rỗng từ đầu và `.review/VERDICT.md` mới. Hai clone đo giữ nguyên HEAD/tree và tracked/index. Fixture golden và state phát sinh của test nằm ở hai clone trong scratch. Repo nguồn Executor nằm ngoài phạm vi quan sát.

Không có lệnh nào trong sáu lệnh của prompt được báo `skipped`. Kết luận nội dung theo ngưỡng của prompt có 0 P0, 0 P1, 1 P2 và 0 P3 mở. **CHƯA ĐỦ ĐIỀU KIỆN MERGE** vì K1 còn mở theo ADR-0060 M1. Selftest N/N, doc-claims strict, bằng chứng Windows và CI trên exact head cũng chưa đạt hoặc chưa được đo theo bảng. Lượt này chạm trần 10/10. Lớp `ranh-gioi-khoan` còn mở tại Review Rescue Checkpoint. [ADR-0060 M1](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32) · [Protocol §12](../docs/PROTOCOL_DA_PHIEN.md#L1097)

P2_mo: 1

VERDICT: APPROVE
