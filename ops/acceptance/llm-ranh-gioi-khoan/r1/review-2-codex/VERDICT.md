# Verdict packet #1514 r1 lượt 2 — Codex
reviewed_sha: 53c49ab125290b0a937c60aefe5481201b42cd4e

- HEAD detached, tree `60c69ec622d97f9458bec739623235b06a3aa6ba`. Base `64b7f2c14776d5d0e1d34a6be4725490956f5bec`, tree `0cc14e79cecd2ce44bc4dc6cff92cadb31fd7ee4`. Base là tổ tiên của HEAD (`git merge-base --is-ancestor`, rc `0`). Hai ref cục bộ `refs/heads/ccr-89c0d2e2-inanqb` và `refs/remotes/origin/ccr-89c0d2e2-inanqb` đều trỏ exact HEAD. Checkout được giao là clone nông.
- Packet revision 1, generation 1, Review Class `sensitive`. Lease có hiệu lực đến `2026-11-25T11:40:00Z`. SHA-256 của spec trên đĩa và của blob ở commit đóng băng `2d32ef1` lẫn HEAD cùng khớp lease, `a85ee727788a93021f5258b7f50dea3a9dd70d3f502f6abf40f74b947af7740a`. `lease_publish.py check` xác nhận write set, còn `git diff --name-status` cho thấy đủ 10/10 đường dẫn thay đổi nằm trong lease.
- Run `fd39754a13e24dd09f35801f61ea0017`, `openai_codex / codex_cli / machine`. `run.json` ghi đường thực thi Codex CLI. Checkpoint và `run.json` cùng neo HEAD và SHA-256 của prompt `6676cc4d215952bfad25684d9286a76f93c8238327ab4a179fa35b28925605a7`, khớp bản đọc lại. Cặp thực thi được giao là Claude Code (`anthropic_claude / claude_code / machine/local` theo lease) và Codex CLI. Sandbox `workspace-write` theo môi trường phiên. Linux x86_64, Python 3.13.18, Git 2.43.0, `core.abbrev=7` đặt cho tiến trình cổng.

## Đối chiếu lượt trước

| Lượt và finding | Trạng thái | Bằng chứng |
| --- | --- | --- |
| #1514 lượt 1, B1 (`89c60dc55718d7f76e73c8402ea38d006eaf9487`) | ĐÃ VÁ THẬT | Lease tại exact HEAD khai `reviewer_execution_surface: codex_cli`, khớp biên nhận của lượt 2. Lượt 1 dừng ở preflight. |
| #1503 lượt 11, X2 | ĐÃ VÁ THẬT với hình dạng nháy thẳng lồng đã nêu | Kiểm số dấu chạy trước bộ quét trạng thái. Mẫu bốn dấu đỏ khi bỏ chốt. |
| #1503 lượt 11, X3 (`ranh-gioi-khoan`) | CÒN MỞ | Các mẫu gãy trước dấu câu kết bị chặn. X3 sinh đường bỏ khoản ở A1. Các dạng tách hoặc bỏ khoản ở A2 vẫn còn. |
| #1503 lượt 11, X4 | ĐÃ VÁ THẬT với gộp dòng điểm | Đối chứng giữ xuống dòng đạt. Đột biến gộp khoảng trắng làm ca đích đỏ tại khẳng định X4. |

## Đối chiếu đặc tả

| Mục | Trạng thái | Bằng chứng |
| --- | --- | --- |
| §1 bất biến | Chưa đạt đủ | `can_nguoi_duyet` và `pham_vi_kiem` giữ nguyên. Đường gọi model giữ nguyên. X3 bỏ điều kiện cũ bảo vệ dòng có từ nối khoản (A1). Bằng chứng 8/8 của ba kết quả đã lưu chưa có trong checkout. |
| §2.1 X2 | Đạt theo đặc tả | `tach_khoan` gọi `_dong_mo_ho` sau `_bo_dau_dong` và trước khi bỏ bất kỳ dòng nào. Chốt từ chối từ ba dấu nháy thẳng. Một cặp hợp lệ vẫn qua ca đối chứng. |
| §2.2 X3b/X3c | Đạt trên các mẫu đặc tả, còn A2 và A3 | Chốt duyệt mọi khoản sau khi gom điểm và tiếp dòng. Hai chấm ở dòng mở hợp lệ nếu điểm cuối kết câu. Hàm bỏ dấu đóng cuối theo một lượt, nên bỏ sót dấu đóng xen khoảng trắng. |
| §2.3 X3 | Chưa đạt §1 | Hậu tố được kiểm sau khi gộp khoảng trắng và bỏ qua hoa thường. Ca không khớp hậu tố bị chặn, hai mẫu câu dẫn chuẩn đạt. Hậu tố trùng trong nội dung khoản cũng kích hoạt việc bỏ dòng và che luôn chốt dấu câu kết ở phía sau (A1). |
| §2.4 X4 | Đạt theo đặc tả | `_gon` gộp khoảng trắng từng dòng, bỏ dòng rỗng và giữ `\n` cho cả hai vế. Tiếp dòng mở bằng từ nối vẫn qua. |
| §4.1–§4.5 | Đạt các mẫu đã liệt kê, còn khoảng trống kiểm thử | `ca_wp1514` có ca dương và ca âm cho bốn chốt. Sáu đột biến của packet đỏ bằng `TinHieuChotCa` của ca đích. Mẫu X3 chưa bảo vệ điều kiện cũ ở A1. |
| §4.6 và nghiệm thu 8/8 | Thiếu bằng chứng | Fixture mang số hiệu `134/2025/QH15` kiểm dạng nguồn mất số với 2 khoản. Việc đối chiếu đủ 8 khoản theo §1 chưa được đo. Xem A4. |
| Effective write set | Đạt | 10/10 đường dẫn trong diff thuộc lease, không có thay đổi ở các đường dẫn đặc tả loại trừ. `git diff --check 64b7f2c 53c49ab` trả rc 0. |

## Findings

### A1 [P1] Dòng đầu có từ nối của khoản vẫn bị bỏ nếu trùng hậu tố câu dẫn — `scripts/tl_core/llm_route.py:535`

**Kịch bản.** Trong nguồn mất số, dòng đầu của một khoản dài chứa từ nối định nghĩa ở cấp khoản và kết thúc bằng chính cụm dẫn sang phần giải thích tiếp theo. Dòng sau là một mệnh đề diễn giải có từ nối riêng, có dấu kết câu và đã mất dấu phân cấp. Nếu model bỏ dòng đầu và trả phần sau với số liên tục theo cách quét, kết quả có thể được nhận dù mất phần đầu của khoản.

**Căn cứ.** Nhánh mới dùng `_RE_CAU_DAN.search` trên hậu tố và đã bỏ `_tu_noi(ln) is None`. `continue` chạy trước khi thêm khoản, nên phép kiểm dấu câu ở dòng 543 chỉ thấy những dòng còn lại. `lech_nguyen_van` so theo danh sách đã rút ngắn ở dòng 655–674. Khi danh sách lệch rỗng, handler có thể trả rc 0 và ghi `--out` (`scripts/tl_core/ops_misc.py:3107`, `:3122`, `:3137–3142`). Nếu phần sau có dấu điểm nhận diện được, parser lại từ chối ở dòng 527 vì chưa có khoản để gắn điểm. Cả hai hệ quả đến từ việc bỏ nhầm dòng mở đầu.

**Đề xuất.** Giữ điều kiện nhận diện từ nối cấp khoản khi xét câu dẫn. Với dòng có tín hiệu của cả khoản và câu dẫn, giữ dòng để xử lý theo cấu trúc hoặc từ chối nếu cấu trúc chưa rõ. Thêm ca đích bảo vệ điều kiện này.

### A2 [P1] Quét theo dòng vẫn có thể tách hoặc bỏ sai khoản — `scripts/tl_core/llm_route.py:513`

**Kịch bản và căn cứ.** Đây là các đường còn lại của X3 từ #1503. Chúng dùng chung danh sách khoản mà `lech_nguyen_van` lấy làm chuẩn.

- Nguồn mất số có khoản ngắt dòng sau dấu chấm phẩy ở giữa một định nghĩa dài. Hai mảnh đều có từ nối và hai vế đầy đủ, phần sau kết thúc bằng dấu câu được cho phép. Dòng 537–538 tạo hai khoản và dòng 543 nhận cả hai. `lech_nguyen_van` có thể nhận câu trả lời tách đôi cùng cách đó.
- Trong khoản cuối của nguồn có số, một tiểu mục đứng đầu dòng có thể trùng số khoản kế tiếp sau một thân hoặc điểm đã kết câu. Nếu số của các tiểu mục trước nằm trong cùng dòng với phần thân, chúng không phá dãy số mà parser nhận. Dòng 513 làm mất thụt lề, dòng 523–525 ưu tiên nhận số khoản, và cả dãy số lẫn dấu câu kết có thể qua. Nếu tiểu mục có cấu trúc giống một định nghĩa, phép so hai vế sẽ xác nhận nó như khoản độc lập. Ca X3c hiện tại bắt đầu từ phần trước còn mở nên chặn được hai mẫu đã định.
- Tiêu đề dùng dấu hai chấm bị dính vào khoản đầu trong bản text. `_RE_TIEU_DE_DIEU` nhận tiền tố ở dòng 69, nhưng `_tu_noi(dong[0])` dừng ở dấu hai chấm ngoài ngoặc (dòng 639–643) trước khi gặp từ nối của khoản. Dòng 519 vì thế bỏ nguyên dòng. Nếu khoản còn lại mất số, parser có thể đếm lại từ 1 và nhận một kết quả thiếu khoản đầu. Cơ chế này có từ base.

**Đề xuất.** Với tiêu đề dính nội dung, chỉ bỏ tiêu đề khi nhận chắc ranh giới tiêu đề. Với văn bản đã mất thụt lề hoặc cấp đánh số, cần bằng chứng cấu trúc hoặc từ chối những trường hợp ranh giới còn mơ hồ. Cập nhật mô tả giới hạn của dấu câu kết trong `docs/GOI_AGENT_DA_NEN.md` nếu các dạng này được chuyển sang packet kế tiếp.

### A3 [P2] Khoảng trắng xen giữa các dấu đóng làm khoản đã kết câu bị từ chối — `scripts/tl_core/llm_route.py:552`

**Kịch bản.** Một khoản kết thúc bằng nguyên câu trích dẫn trong ngoặc đơn. Bản text có khoảng trắng do dàn trang hoặc OCR giữa dấu đóng trích dẫn và dấu đóng ngoặc.

**Căn cứ.** `_dong_mo_ho` vẫn chấp nhận các cặp dấu cân bằng. Lượt xóa dấu đóng của `_ket_thuc_cau` dừng ở khoảng trắng xen giữa. Lượt xóa khoảng trắng cuối làm lộ dấu đóng trích dẫn còn lại, nên hàm từ chối dù trước đó có dấu kết hợp lệ. Giới hạn này chưa được khai trong mục script gọi Claude.

**Đề xuất.** Bỏ cả dải đuôi gồm khoảng trắng và các dấu đóng được liệt kê, rồi kiểm dấu câu cuối. Giữ ca đối chứng cho dấu đóng đơn và bổ sung đối chứng có khoảng trắng xen kẽ.

### A4 [P2] Fixture hiện tại chưa đo tương thích 8 khoản theo §4.6 — `scripts/tl_core/llm_route_test.py:30`

**Căn cứ.** `VAN_BAN` và `DUNG` có hai khoản. `chay_lenh` gắn số hiệu của luật vào lời gọi giả, và `ca_wp1514` dùng các mẫu nhỏ độc lập. Tổng 49/49 vì thế chưa xác nhận 8/8 của Điều 3 và ba kết quả đã lưu như §1 yêu cầu.

**Đề xuất.** Bổ sung fixture tám khoản cùng hình dạng theo §4.6 và chạy lại bộ so trên ba kết quả đã lưu, bằng dữ liệu offline.

| Lớp | Biểu hiện | Cao nhất | Điều kiện đóng |
| --- | --- | --- | --- |
| `ranh-gioi-khoan` | A1, A2, nối X3 của #1503 lượt 11 | P1 | Phản chứng độc lập cho bỏ dòng đầu, tách dòng có dấu kết và số tiểu mục trùng. Chốt nhận diện tiêu đề cần đo riêng vì chạy trước vòng phân khoản. |
| Dấu đóng cuối khoản | A3 | P2 | Đối chứng nhận khoản có khoảng trắng giữa dấu đóng theo §2.2. |
| Bằng chứng tương thích Điều 3 | A4 | P2 | 8/8 trên ba kết quả đã lưu hoặc hiện vật tương đương đủ theo đặc tả. |

## Kết quả test và đột biến


Log và mã thoát của các bộ test nằm tại `/tmp/wp1514-review.KTIapP3S/`. Các cổng chạy trong môi trường tối giản, HOME và cache riêng, không sinh bytecode. Git chỉ cho phép transport cục bộ. Các phép đo dùng bộ giả có sẵn của repo và bản sao mã cho đột biến.

| Lệnh | Trạng thái | rc và bằng chứng |
| --- | --- | --- |
| `python scripts/tl_core/llm_route_test.py` | `passed` | `0`. 49/49 ca, 89/89 đột biến bị giết. |
| `python scripts/tl.py --deterministic workflow-audit --strict --json` | `passed` | `0`. `ok=true`, 26 card, 60 task, 194 lệnh khả dụng, 0 lỗi. |
| `python scripts/tl.py --deterministic golden-test --json` | `passed` | `0`. 20/20 ca đạt. 19/20 ổn định byte thô ở lượt này. Ca `hygiene_sweep_fixture` dao động ở `snapshot_age_s`, là trường biến động đã khai. Bản chiếu khớp và không có drift ngoài khai báo. |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | `passed` trên bản sao sạch | `0`, `ok=true`, 187/187 tệp, 0 thiếu/thừa/sai. Lần chạy ở checkout giao ban đầu trả `2` vì nhận `.review/VERDICT.md` là tệp thừa. |
| `python ops/lease_publish.py check --root . ops/leases/llm-ranh-gioi-khoan-r1-g1-claude.yaml` | `passed` offline | `0`, `ĐĂNG ĐƯỢC`, Issue 1514, neo `64b7f2c14776`, hạn `2026-11-25T11:40:00Z`. |
| `python scripts/tl.py --selftest` | `failed` trên cả HEAD và base | `1` cả hai. HEAD `1775/1789`, base `1775/1789`. Toàn bộ danh sách ca và trạng thái trùng nhau. Có đúng 14 ca đỏ trên cả hai ở các nhóm `r973_bootstrap_*` (8), `wp433_*` (5) và `wp727_tl_gws_refresh` (1), trong sandbox có `/tmp/.git` rỗng như ghi trong prompt. Delta bằng 0. |
| `python scripts/tl.py --deterministic determinism-audit --strict --json` | `passed` trên bản sao sạch | `0`, 15/15 phép kiểm, `ok=true`. Kiểm manifest trên 187 tệp đúng package hash `11b64b01c60ebb9a440ad699b4466538c4bf89be456d0325f4a1d1e313fd2532`. |
| `python scripts/tl.py --deterministic doc-claims-check --strict --json` | `failed` trên cả HEAD và base offline | `2` cả hai. Cùng một cờ cứng `SHA_NOT_A_COMMIT` cho `9941d8af52aeede1c78ea4e232fbe9a8d5272033` ở `docs/PROTOCOL_DA_PHIEN.md:1680`. Object vắng trong clone được giao. Delta cờ cứng bằng 0. |
| Phép kiểm `loi_ruff_ci()` trong `.claude/dev/ci_dang_ky_test.py` | `passed` | `0`, `RUFF_CONTRACT 3 []`. |
| `python -m ruff check --no-cache --select F scripts/tl.py` | `failed` cả hai, đạt tiêu chí delta | `1` cả hai. Ruff 0.15.15, cùng 12 lỗi, stdout trùng byte, delta 0. |
| Windows §3 | `not_run` | `not_measured`, lượt này là Linux offline. Phần giả lập Windows giữ đường kiểm riêng trong suite. |

Lần selftest đầu ở checkout có verdict trả `1`, `1773/1789`. Ca topology của gói đỏ ở checkout có tệp verdict. Ghim `core.abbrev` bằng biến môi trường cũng làm ca `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` đỏ vì override lấn thiết lập 7/8 của kho thử con. Hai bản sao sạch với Git config riêng loại được cả hai sai lệch. Không có bộ test bắt buộc nào báo `skipped` ở cấp bộ.

### Đột biến

Quan sát breakpoint ở nhánh bắt `TinHieuChotCa` của bộ test có sẵn (`python -m pdb`, rc `0`). Mỗi dòng sau là lý do ca đích đỏ khi bộ test áp đột biến trên tệp tạm.

| Đột biến | Khẳng định đỏ |
| --- | --- |
| `wp1514_bo_x2` | X2, dòng có bốn nháy kép thẳng phải bị coi là mơ hồ. |
| `wp1514_bo_ket_cau` | X3b, không nhận hai mảnh gãy của một khoản mất số. |
| `wp1514_hai_cham_ket_cau` | X3c, khoản kết thúc bằng hai chấm trước dòng có số phải bị chặn. |
| `wp1514_cau_dan_moi_hai_cham` | X3, không được bỏ dòng đầu kết thúc bằng hai chấm khi sai mẫu. |
| `wp1514_gon_gop_dong` | X4, định nghĩa gộp điểm thành một dòng phải lệch. |
| `wp1514_khong_bo_dau_dong_cuoi` | Đối chứng X3b/X3c, điểm và dấu đóng sau dấu chấm vẫn phải qua. |

Hai phép bổ sung sửa riêng `llm_route.py` trên bản sao tạm và chạy lại tệp test với dữ liệu sẵn có.

- Cho nguồn có số bỏ qua lỗi thiếu dấu kết, đồng thời giữ nhánh chặn hai chấm. `ca_wp1514` đỏ bằng `TinHieuChotCa` đúng ở mẫu X3c thiếu dấu kết, 48/49 ca. Suite trả rc `1`, trong đó một neo đột biến gốc mất vì chính dòng đó đã bị đổi. X3b và mẫu hai chấm X3c không che mẫu này.
- Đổi ngưỡng X2 từ `>= 3` thành `>= 4`. Cả 49/49 ca vẫn xanh. Rc `1` chỉ do đột biến gốc `wp1514_bo_x2` mất neo, nên ca hiện có chứng minh được mẫu bốn dấu, chưa phân biệt ngưỡng đúng ở đúng ba dấu.

Hai mẫu hồi quy cũ về từ nối trên dòng điểm và ghép dòng mở bằng từ nối (`llm_route_test.py:634`, `:668`) đã được chỉnh đầu ra giả để giữ xuống dòng. Nhờ đó phép so mới của X4 không tự chặn hai mẫu trước khi chúng kiểm hành vi cũ.

## Không đo được

- A1–A3 là kết luận từ đường đi của mã. Chưa chạy ca tái hiện mới và chưa đo tần suất các dạng này trong corpus. Các đột biến đã chạy chỉ dùng mẫu có sẵn của repo.
- Cổng Windows bản địa §3 và 8/8 trên ba kết quả `tl`/`sub`/`api` lưu sẵn là `not_measured`. Checkout thiếu hiện vật cho phép đo 8/8, còn lượt này giới hạn ở Linux offline.
- CI, trạng thái remote của PR và nguồn gốc object thiếu trong doc-claims là `not_run` theo ràng buộc offline.
- Model và effort thực tế của reviewer là `KHONG_DO_DUOC`. Khi ghi verdict, `run.json` đang ở `dang_chay`. Trạng thái terminal, rc của runner và hash stdout cần được launcher ghi nhận sau khi lượt kết thúc. Receipt chưa đủ dữ liệu để suy ra bằng chứng ngoài checkout được giao.

Kiểm cuối bằng `git rev-parse HEAD 'HEAD^{tree}'`, `git diff --exit-code` và `git diff --cached --exit-code`, đều rc `0`. SHA/tree của HEAD và base khớp preflight. Selftest lần đầu sinh hai thư mục ignored `references/golden/fixtures/` và `scripts/.tl_state/` trong checkout được giao. Hai thư mục được dọn sau khi suite dừng. Snapshot cuối chỉ thêm `.review/VERDICT.md` so với snapshot đầu có `.codex/` ignored. Phép so này đo trạng thái tại các mốc. Nội dung `.codex/` và repo nguồn không thuộc phạm vi kiểm.

VERDICT: REQUEST_CHANGES
