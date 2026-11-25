# Verdict packet #1514 r7 lượt 8 — Codex

reviewed_sha: 4d357d1ad679d1a0aeea9795fe9777be8a32c1e5  
reviewed_tree: 72c86bbe1f1b67d9e6955e680a5fd561bec4b268  
base_sha: 64b7f2c14776d5d0e1d34a6be4725490956f5bec  
base_tree: 0cc14e79cecd2ce44bc4dc6cff92cadb31fd7ee4

**APPROVE theo ngưỡng nội dung của prompt.** G1 đã được vá. Lớp `ranh-gioi-khoan` còn một biểu hiện P2 nên chưa đạt điều kiện severity để merge.

## Preflight

- Checkout `ducthangho/tra-luat` detached đúng SHA. Lease r7/g1 chỉ định `sensitive`, khai Codex lượt 8/8. Blob đặc tả `2be1d6861e4ca62e22ce5ea548917ccc2f348dd9` và bản local cùng SHA-256 `20209949c953ab6c0a1e5f0cc56e0b82265e47c7968c1bb9b980d5c7bd06344c`, khớp lease.
- Hai ref nhánh lưu cục bộ `ccr-89c0d2e2-inanqb` cùng trỏ vào SHA ứng viên. Baseline là tổ tiên (rc 0). Mốc diff bản vá `a1e5022353732d6999a9f24589fc6b91478f3f74` khác mốc review lượt 7 `0ec7ca05b8fb9cc2cfd32a299f6522d9cc473c63`. Cả hai diff qua `git diff --check` (rc 0).
- Đối chiếu danh sách đường dẫn trên cả diff toàn packet (41 tệp) và diff bản vá (8 tệp) với lease r7: 0 đường dẫn ngoài write set. SHA-256 danh sách theo quy tắc LF của lease là `e6dedafad749e011a38c608dfdc9c9a36a30b08cc0657b0994fd65047a5cc98b`. Sáu cặp r1↔r2 đến r6↔r7 trỏ đúng theo cả `thay_the_cho` và `da_bi_thay_the`. Cả bảy blob đặc tả tại HEAD khớp hash của lease tương ứng. Lease r7 hết hạn lúc `2026-11-25T14:56:00Z`, còn hạn tại preflight.
- Executor `claude / claude_code / machine/local` theo lease. Reviewer `openai_codex / codex_cli / machine` theo launcher run `625259b31a4141ef9997d0580c1abcf4`. `run.json` và `checkpoint.json` cùng khớp SHA ứng viên và băm prompt `5bda61e80096063ca26438aa8e9eb2fabf8c16ee366f0a9c1f468cb08104341f`. Linux x86_64, Bash, Python 3.13.18, Git 2.43.0, Codex CLI 0.172.0, `core.abbrev=7`, sandbox `workspace-write` theo quyền phiên. Model và effort phục vụ: `KHONG_DO_DUOC` từ receipt đang chạy.

## Đối chiếu lượt 7 và đặc tả r7

| Mục | Trạng thái | Bằng chứng |
| --- | --- | --- |
| G1 lượt 7, §2.10 | **ĐÃ VÁ THẬT** cho dòng đầu kết dấu hai chấm ASCII | Ở nguồn mất số, dòng ở vị trí 0 ngoài danh sách bị chặn trước khi thêm khoản. Đoạn tỉa đuôi dùng đúng dải ký tự của §2.10. `ca_wp1514_luot7` chặn nguồn và kết quả ghép trong ca G1. Khoản đối chứng mở bằng hai chấm và có điểm sau câu dẫn chuẩn, vẫn qua. Đột biến bỏ chốt đỏ đúng G1. [Mã](../scripts/tl_core/llm_route.py#L554) · [Ca G1](../scripts/tl_core/llm_route_test.py#L1122) |
| F2 lượt 6, X3, A1, D3, E2, §2.3 và §2.5–2.9, §4.4 | **ĐÃ VÁ THẬT** đối với việc bỏ nhầm dòng | `fullmatch` trên dòng đầu sau tiêu đề và chuẩn hóa khoảng trắng. Fixture có ba biến thể câu dẫn chuẩn, hai động từ và các mẫu nội dung dư hoặc câu dẫn lặp. Đột biến nới chủ ngữ đỏ F2. Đường giữ rồi ghép còn H1. [Mã](../scripts/tl_core/llm_route.py#L493) · [Ca F2](../scripts/tl_core/llm_route_test.py#L1112) |
| F1 lượt 6, A2b, C2, D1, E1, §2.5–2.9 | **ĐÃ VÁ THẬT** cho các biểu hiện đã báo | Ca F1 chặn khoảng trắng trước dấu và dấu dính trích dẫn. Các ca trước giữ đối chứng số thập phân và dẫn chiếu cuối dòng điểm, chặn khoảng trắng ASCII/U+00A0 và dấu dính chữ. Đột biến phục hồi regex r5 đỏ đúng F1. Đây là tập bao có điều kiện, đối chiếu bên dưới. [Mã](../scripts/tl_core/llm_route.py#L489) · [Ca F1](../scripts/tl_core/llm_route_test.py#L1107) |
| A2c, C1, D2, §2.6–2.7 | **ĐÃ VÁ THẬT** đối với tiêu đề dính nội dung | Chỉ bỏ tiêu đề khớp cả dòng. Ca C1 chặn phần dư và giữ bốn mẫu tiêu đề đối chứng. Tên điều khác, tiền tố viết hoa và tên điều xuống dòng riêng là giới hạn đã khai. [Mã](../scripts/tl_core/llm_route.py#L533) · [Ca C1](../scripts/tl_core/llm_route_test.py#L1042) |
| X2, §2.1 và §4.1 | **ĐẠT** | Chặn từ ba nháy kép thẳng sau khi bỏ dấu đầu dòng. Mẫu bốn dấu bị chặn và đối chứng một cặp qua. [Mã](../scripts/tl_core/llm_route.py#L603) · [Ca X2](../scripts/tl_core/llm_route_test.py#L981) |
| X3b, X3c, A2a, A3, §2.2 đã sửa theo §2.5, §4.2–4.3 | **ĐẠT** trên các ca đích | Chốt dấu kết chạy sau khi gom điểm và chỉ nhận chấm, chấm than, chấm hỏi. Mảnh thiếu dấu kết và khoản chưa khép trước dòng số bị chặn. Đối chứng điểm cuối kết câu và đuôi dấu đóng xen trắng vẫn đạt. [Ca dấu kết](../scripts/tl_core/llm_route_test.py#L985) · [Ca A3](../scripts/tl_core/llm_route_test.py#L1031) |
| X4, §2.4 và §4.5 | **ĐẠT** | Ghép dòng điểm thành một dòng báo lệch, bản giữ xuống dòng qua. Đối chứng tiếp dòng mở bằng “là” giữ hành vi cũ. [Mã](../scripts/tl_core/llm_route.py#L583) · [Ca X4](../scripts/tl_core/llm_route_test.py#L1003) |
| A4, §1 và §4.6 | **ĐẠT** offline | Fixture Điều 3 tách đủ tám khoản. Ba kết quả lưu `tl`, `sub`, `api` đều khớp 8/8 sau chuẩn hóa. [Ca A4](../scripts/tl_core/llm_route_test.py#L1035) |
| B1 lượt 1, §1 và §5 | **ĐÃ VÁ THẬT** đối với bề mặt reviewer | Lease và launcher cùng nhận dạng Codex CLI. Diff giữ `can_nguoi_duyet: true`, `pham_vi_kiem`, các hàm gọi model và VERSION. Selftest chỉ miễn so mode 0644 cho Windows, vẫn so nội dung JSON. [Đầu ra](../scripts/tl_core/ops_misc.py#L3104) · [Selftest](../scripts/tl_selftest.py#L32294) |

**Hai regex số khoản.** Trên từng dòng đã được tách và tỉa trắng, hai mẫu cùng nhận lõi số trong ngoặc hoặc số trần với khoảng trắng tùy ý trước chấm hay ngoặc đóng. `_RE_SO_KHOAN` áp điều kiện ký tự kế tiếp khác chữ số ở nhánh số trần, còn nhận số trong ngoặc sát chữ số và dấu số nằm ở cuối dòng. `_RE_SO_NOI_DONG` áp ngoại lệ chữ số, xuống dòng và cuối chuỗi cho cả hai nhánh, đồng thời bỏ qua dấu số sát ký tự từ, chấm hoặc phẩy ở bên trái. Vì vậy nó bao các mẫu trong miền còn lại sau ngoại lệ §2.9. Tập bao này phụ thuộc các ngoại lệ trên. Lý do số thập phân giải thích trực tiếp trường hợp số trần có dấu chấm, còn trường hợp số trong ngoặc sát chữ số cũng bị loại bởi cùng lookahead. [Hai mẫu](../scripts/tl_core/llm_route.py#L488) · [Đặc tả F1](../ops/specs/llm-ranh-gioi-khoan-r7.md#L88)

**Khả năng chặn oan.** Các biến thể thiếu cụm mở đầu, khác từ ngữ hay kiểu chữ của câu dẫn, tiêu đề khác tên hoặc xuống dòng riêng, khoản dùng từ nối khác “là”, dòng gãy và ký hiệu mã trùng dấu số đều nằm trong giới hạn đã khai. Các ca có sẵn không xác lập một dạng “Giải thích từ ngữ” thường gặp khác bị chặn ngoài danh sách giới hạn. Chưa đo độ phổ biến trên corpus. [Giới hạn người dùng](../docs/GOI_AGENT_DA_NEN.md#L368) · [Ca đối chứng F2](../scripts/tl_core/llm_route_test.py#L1117)

## Findings

### H1 [P2] Dòng dẫn với dấu phân cách ngoài chốt vẫn có thể bị ghép với điểm thành một khoản — `scripts/tl_core/llm_route.py:545,559`

**Kịch bản.** Nguồn mất số bắt đầu bằng lời dẫn liệt kê ngoài danh sách, có từ “là” đứng riêng giữa hai vế, tiếp sau là các mục mang dấu điểm và điểm cuối có dấu kết câu. Nếu dấu hai chấm cuối dòng dẫn xuất hiện ở dạng toàn chiều rộng (fullwidth, U+FF1A), chốt r7 bỏ qua dòng này.

**Căn cứ.** `_dong_mo_ho` không loại U+FF1A. `endswith(":")` chỉ nhận U+003A, nên nhánh nguồn mất số vẫn thêm dòng dẫn như một khoản. Nhánh `_RE_DIEM` nối các mục vào khoản đó rồi phép kiểm dấu kết dùng đuôi của điểm cuối. `_tu_noi` chỉ dò trước điểm đầu và có thể tìm được “là” trong dòng dẫn. Nếu đầu ra có một mục đúng thứ tự và chép đúng hai vế cùng xuống dòng của cả khối, `lech_nguyen_van` chấp nhận phân đoạn ấy. §2.10 chặn đúng biểu hiện G1 đã báo. §2.9 và tài liệu người dùng vẫn cam kết từ chối nguồn có câu dẫn ngoài danh sách. Đây là kết luận đọc mã, chưa có phép chạy riêng cho H1. [Kiểm dấu](../scripts/tl_core/llm_route.py#L603) · [Ghép điểm và chốt r7](../scripts/tl_core/llm_route.py#L539) · [Tách và so hai vế](../scripts/tl_core/llm_route.py#L655) · [Cam kết F2](../ops/specs/llm-ranh-gioi-khoan-r7.md#L84)

**Hạng P2.** Bộ so có thể nhận nhầm một khối gồm lời dẫn và các mục thành một định nghĩa. Ca này cần nguồn mất số, lời dẫn có từ nối ở vị trí phù hợp, dấu điểm tương thích và đầu ra chép khớp cả khối. `can_nguoi_duyet` vẫn bắt buộc. ADR-0060 M1 chặn merge khi còn một P2 mở. [ADR-0060 M1](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32)

**Đề xuất.** Xử lý sự mơ hồ trước khi nối điểm vào dòng mở của nguồn mất số khi chưa thấy câu dẫn đã xác thực. Nếu không đủ tín hiệu về vai trò dòng mở, yêu cầu ranh giới có cấu trúc hoặc từ chối khối. Giữ đối chứng khoản thật có điểm sau câu dẫn chuẩn. Phép kiểm đóng lớp cần đo nhánh bỏ dòng và nhánh giữ rồi ghép qua nhiều kiểu dấu phân cách.

| Lớp | Biểu hiện và nguồn | Trạng thái |
| --- | --- | --- |
| `ranh-gioi-khoan` | F1/F2 trên `aed16f390f4adf59dde5718bff170c5cddd44cbb`, G1 trên `0ec7ca05b8fb9cc2cfd32a299f6522d9cc473c63`, H1 trên SHA lượt 8 | **VÁ MỘT PHẦN**, hạng cao nhất còn mở P2. G1 đã đóng, H1 còn cùng cơ chế giữ và ghép của lớp. Số biểu hiện mở **1→1**, tỷ lệ đóng lớp **0/1**. |

**Các đường còn lại trong giới hạn văn bản thô.** Một khoản mất số gồm nhiều câu trọn trên các dòng riêng vẫn có thể bị tách nếu mỗi dòng có hai vế và dấu kết. Dấu điểm xuất sai tại một ranh giới có thể khiến bộ quét gộp dòng vào khoản trước. Chấm viết tắt cũng có thể thỏa phép thử dấu kết. Khi phân đoạn nguồn đúng, bộ so kiểm số lượng, thứ tự và hai vế theo từng khoản, nên các đầu ra tự bỏ, tráo, gộp hoặc cắt nội dung bị phát hiện. Giới hạn văn bản thô và bước duyệt ranh giới đã được công bố. [Phân đoạn](../scripts/tl_core/llm_route.py#L516) · [Bộ so](../scripts/tl_core/llm_route.py#L676) · [Phạm vi](../docs/GOI_AGENT_DA_NEN.md#L368)

## Kết quả test và đột biến

Log gốc và mã thoát ở `/tmp/wp1514-r8-evidence.4D6OlC/`. Các lệnh dưới đây chạy với `PYTHONDONTWRITEBYTECODE=1` và `python -B`. SHA ứng viên là SHA nêu ở đầu verdict.

| Lệnh | Trạng thái | rc và bằng chứng |
| --- | --- | --- |
| `python scripts/tl_core/llm_route_test.py` | `passed` | 0. **55/55 ca qua, 102/102 đột biến bị giết.** `component.log`, SHA-256 `edc9ee7ba26f1f195d2aa5b192f2419cf8a5ee74e5194dcc7e95891fbd0d822c`. |
| `python scripts/tl.py --deterministic workflow-audit --strict --json` | `passed` | 0. `ok=true`, 26 card, 60 task, 194 lệnh có mặt, 0 lỗi, 0 cảnh báo. `audit.log`, SHA-256 `160e385a7bea43c5deafef786ddd344be86f1bfb3d58883b2ebbba7aa8bc70f6`. |
| `python scripts/tl.py --deterministic golden-test --json` | `passed` | 0. `ok=true`, 20/20 ca đạt, 20/20 bản chiếu và 20/20 byte thô ổn định giữa hai lần chạy. `golden.log`, SHA-256 `e2a34e5c341a18fe3a0b4e2843fbae5628df6724f7bb763894d83b8da2f565f8`. |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | `passed` trên clone sạch | 0. `ok=true`, 187/187 tệp, 0 sai, thiếu hoặc thừa. Package hash khớp `11098882e201994d27394380a1b39040874723eb4abc20ae6b30bebe73ce1003`. `release-clean.log`, SHA-256 `e452606f4fa8c47fb612ae20cf071a059e8890dec8518109d5fe049f0a5ffa8d`. |
| `python ops/lease_publish.py check --root . ops/leases/llm-ranh-gioi-khoan-r7-g1-claude.yaml` | `passed` cục bộ | 0. `ĐĂNG ĐƯỢC`, Issue #1514, neo `64b7f2c14776`, hạn `2026-11-25T14:56:00Z`. `lease.log`, SHA-256 `78dc56f607bc75400077aff7e7a6d23c6813e4348f658ce290452a6f6e6a3e36`. |
| `python scripts/tl.py --selftest` | `failed` trên ứng viên và baseline | 1 trên mỗi SHA. Cả hai **1.775/1.789**, transport **12/12**. `cmp` của 1.801 dòng mã ca và trạng thái trả rc 0. Cùng 14 ca đỏ trong môi trường có `/tmp/.git` rỗng như prompt đã nêu, gồm 8 `r973_bootstrap_*`, 5 `wp433_*` và `wp727_tl_gws_refresh`. `r380_llm_khai_niem_bien_dau_vao` đạt trên cả hai. Delta 0. Gate N/N §6 chưa đạt. |

Lần chạy release-verify ban đầu trong checkout review có `rc=2` và `ok=false`, với duy nhất tệp thừa `.review/VERDICT.md` đã được tạo sớm theo prompt. Đã chạy lại trên clone sạch có cùng SHA/tree. Log lần đầu `release.log`, SHA-256 `17628eab06ac9062ba0d21deee7b340e953e246460090cd1fd4a0a0fefd08873`.

Full selftest lần đầu trong checkout review trả rc 1, 1.772/1.789. Lượt chạy lại tách bản sao ứng viên và baseline khỏi thư mục chứa verdict, bỏ cấu hình ký commit toàn cục trong tiến trình chạy fixture Git (`GIT_CONFIG_GLOBAL=/dev/null`) và giữ `core.abbrev=7`. Lượt đầu trên clone được ngắt trước khi áp cấu hình này (rc 130). Ba ca đỏ thêm ở lần đầu, `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim`, `r268_l2_trichotomy_theo_trang_thai_object` và `wp44_release_bundle_topology_under_200`, đều đạt sau khi cô lập. `/tmp/.git` của sandbox vẫn hiện diện. Log ứng viên `selftest-clean-head.log`, SHA-256 `fb656bf8598981eed9ad55f25ae2010893c306c3bf4b6fbc0f03d426cbfdf38c`.

Log baseline `selftest-clean-base.log`, SHA-256 `e74cfa7e21deeafb536a591c008014e5b8e0320eb13e5c9ff953476ee856875e`. Hai bản trích xuất dòng trạng thái bằng `rg '^  \[(OK|FAIL)\]'` cùng SHA-256 `4d9b0711e0fb5bf3946f9daaee37dd0d2ab93e79377dbe2ce465b60187422e4e`. Exact SHA/tree và diff tracked/index của cả hai clone được kiểm lại sau khi chạy.

Harness tạo bản sao đột biến trong thư mục tạm. Quan sát lại các ca có sẵn bằng `python -B -m pdb` trên clone đúng SHA, breakpoint ở nhánh bắt `TinHieuChotCa` dòng 1372, lọc tên `wp1514_l6_*` và `wp1514_l7_*`. Rc 0 của debugger và exit status 0 của suite được ghi trong `mutation-pdb.log` (SHA-256 `31d5cf2b72dc46101d2db1ff8fff26de6e4a173d05132f7682761bbb9e6abd5f`). [Harness](../scripts/tl_core/llm_route_test.py#L1354)

| Đột biến đã có | Tín hiệu đích quan sát được |
| --- | --- |
| `wp1514_l7_bo_chot_dong_dau_hai_cham` | `ca_wp1514_luot7` báo G1. Bỏ guard làm khối nguồn được phân đoạn thành một khoản gồm dòng dẫn và các điểm. |
| `wp1514_l6_so_lieu_ke_dang_sau` | `ca_wp1514_luot6` báo F1. Khôi phục mẫu r5 làm nguồn có đánh số nội dòng với khoảng trắng trước dấu được nhận. |
| `wp1514_l6_cau_dan_mo_rong_chu_ngu` | `ca_wp1514_luot6` báo F2. Nới chủ ngữ làm dòng đầu có nội dung dư bị bỏ như câu dẫn. |

## Không đo được

- H1 được xác định từ luồng mã. Chưa có ca chạy riêng cho biến thể dấu phân cách, số liệu tần suất hoặc khảo sát corpus trong lượt này. Ca và đột biến G1 đo đúng dấu hai chấm ASCII của §2.10.
- Windows là `required` theo ADR-0060 M3 vì diff có dòng `os.name` trong selftest. Windows CI và Windows bản địa trên exact SHA là `not_run` trong lượt này và `not_measured` về bằng chứng. Các run `45542712141` và `45553156011` thuộc các mốc lịch sử. [Đặc tả §3](../ops/specs/llm-ranh-gioi-khoan-r7.md#L101) · [ADR-0060 M3](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L43)
- `determinism-audit --strict`, `doc-claims-check --strict` và Ruff F delta của §6 là `not_run` trong phạm vi lệnh của prompt. GitHub/CI từ xa, API Claude/Anthropic thật, `claude -p` thật và `tl llm-khai-niem` thật là `not_run`. Chưa đo live head và trạng thái PR. Không có lệnh nào trong sáu lệnh prompt được đánh dấu `skipped`.
- Trạng thái terminal, rc launcher và băm stdout đã đóng của lượt 8 cần đọc lại từ hiện vật terminal của đúng run sau khi phiên kết thúc.

Các fixture golden và state tự sinh trong checkout review đã được chuyển ra scratch sau khi lần chạy đầu kết thúc. `git diff --exit-code` và `git diff --cached --exit-code` đều rc 0. HEAD/tree khớp hai mốc, mục ignored `.codex/` có sẵn và rỗng, tệp mới duy nhất trong checkout là verdict được giao. Phép kiểm Git xác nhận trạng thái quan sát tại các mốc.

## Kết luận nội dung và điều kiện merge

0 P0, 0 P1, 1 P2, 0 P3 mở. Lớp `ranh-gioi-khoan` còn mở qua các lượt 6, 7 và 8. Đây là lượt Codex 8/8 theo lease, đã chạm Review Rescue Checkpoint. Điều kiện severity để merge theo ADR-0060 M1 chưa đạt. [Protocol §12](../docs/PROTOCOL_DA_PHIEN.md#L1097) · [ADR-0060 M1](../docs/adr/0060-dieu-kien-merge-va-moc-ready.md#L32)

P2_mo: 1

VERDICT: APPROVE
