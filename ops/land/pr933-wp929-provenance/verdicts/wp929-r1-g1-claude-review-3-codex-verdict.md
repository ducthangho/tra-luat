Verdict: request_changes
Reviewed commit: f3b54d260bcdecf5b6d2348730a958e168bf7330
Spec sha256: 79251bee45fc39003d13438d741c4e6319dc80ea6b480dc1b931c93d0c6a7ae6
Reviewed tree: 4318f11054c40f10dfb9abc9b2592a8b5a1de186
Base origin/master: 36057e8292bcb3b27ceb64b461d7cf29057a8ba3

Một P2 còn mở: fixture mới làm gate Windows thất bại. Giữ một P3 kế thừa về độ phủ lỗi ls-tree. Áp ngưỡng của prompt: còn P0/P1/P2 thì không approve. Lỗi Windows đã có ở 227dcde; merge master không sinh ra nó và approval lượt 2 đã bỏ sót nó.

## Trạng thái finding lượt trước

ĐỐI CHIẾU LƯỢT TRƯỚC: `VERDICT-luot2.md`, reviewed SHA `227dcdebc62c9275f9df09056f66e2124ed5f14c`, SHA256 `40d42d53d7b30f7e703eced0376803907aa3b3a57d1d62dd697adcac25c30e49`. Nối lịch sử về `VERDICT-luot1.md`, reviewed SHA `8a6d795c982fc7e9da2fbfd28a75ca25d5f3eb95`, SHA256 `8a392561044c0ae6b9d504260149ff441fb8ec81cfe828fd8e06bd8f27c80bbf`.

| Finding/lớp kế thừa | Kết quả tự đo trên f3b54d2 |
| --- | --- |
| `wp929-tree-is-not-activation-file` (P2 lượt 1, đóng lượt 2) | **ĐÃ VÁ THẬT** trong phạm vi tree/symlink: hai ca tương ứng PASS; `r929_bo_kiem_loai_doi_tuong` giết cả hai, `r929_nhan_symlink` giết ca symlink tại `_kiem`, cần False nhưng được True. Chốt mode/type còn nguyên. Không dựng lại probe gitlink riêng của lượt 2. |
| `wp929-filename-boundaries-unmeasured` (P3 lượt 1, đóng lượt 2) | **ĐÃ VÁ THẬT** cho hai biên đã báo: ca ba chữ số và đuôi khác `.md` PASS; mutant `r929_so_chu_so_tuy_y`, `r929_bo_duoi_md` đều chết tại so sánh False/True. |
| `wp929-nfc-unmeasured` (P3 lượt 1, đóng lượt 2) | **ĐÃ VÁ THẬT**: `r929_nfd_van_tinh` PASS; `r929_bo_nfc` chết tại so sánh True/False. Fixture ghi bytes NFD vào Git blob. |
| `wp929-git-error-guards-unmeasured` (P3 còn mở một phần lượt 2) | **CHƯA VÁ** nhánh ls-tree; xem P3 dưới. Nhánh show có phép đo đúng trên Linux (ca PASS, mutant chết đúng khẳng định), nhưng fixture thêm để đo nhánh này **VÁ SINH LỖI MỚI** về tính đa nền: lỗi Windows P2 dưới. Đây là lỗi của bản vá đã có từ lượt 2, không hàm ý có thay đổi giữa 227dcde và f3b54d2. |

Lệnh cho bảng trên: `python3 -B evidence/review_runner.py baseline` và `python3 -B evidence/review_runner.py mutants`, cả hai rc=0. Output: `BASELINE: passed=159/159; skipped=0`; `MUTANTS: valid=11/11`. Log `evidence/mutants.log` có traceback, xác nhận chết tại khẳng định `luat_adr0054`. Mỗi mutant giữ 3/3 đối chứng khác họ xanh.

## Findings mới

- **[P2] wp929-windows-readonly-object-delete** — `cay-kho/.claude/dev/packet_loop_test.py:8482–8483`: callback `sau` của `r929_show_loi_la_false` gọi `Path.unlink()` trực tiếp trên loose object chỉ đọc. Windows từ chối xoá. Callback chạy sau push nhưng trước `_r812_r7_cmd`, nên ca chưa tới lần `record-lease` cần đo, chưa kiểm tra nhánh lỗi `git show`.

  **Tác động/xếp hạng:** `gate-packet-loop (windows-latest)` trả mã 1. Workflow đưa Windows vào ma trận cho `workflow_dispatch` hoặc PR có nhãn `windows` (`ci.yml:65–70`); bước selftest gọi toàn bộ suite (`ci.yml:1075–1077`). Đây là hồi quy gate trên nền được hỗ trợ của chính PR: **P2, chặn approve**. Việc nằm trong test không làm nó thành P3; không suy rằng mọi PR Ubuntu cũng bị chặn.

  **Lệnh đọc bằng chứng native đã giao:**

  ```text
  rg -n 'HEAD is now at ab94c4f|ĐỎ  r929_show_loi_la_false|nền: 871/872|TỔNG: 1 lỗi|Process completed with exit code 1' windows-gate-packet-loop-40476173630.log
  L908: HEAD is now at ab94c4f Merge pull request #933 ...
  L1193: ĐỎ  r929_show_loi_la_false: PermissionError: [WinError 5] Access is denied: '...\.git\objects\56\5656b85a2ca1758ccd6cf6feaff364416f5c96'
  L1194: nền: 871/872 đạt · BỎ QUA: 4
  L2509: TỔNG: 1 lỗi
  L2510: ##[error]Process completed with exit code 1.
  ```

  Log chạy trên merge `ab94c4fb01d0d122d2f00a1f2c386c6a191349c5`, không phải check run mới trên f3b54d2. `python3 -B evidence/audit.py before` chứng minh hai tệp write set giống từng byte ở ab94c4f, f3b54d2 và 227dcde, nên lỗi thuộc đúng mã review.

  **Probe độc lập:** `python3 -B evidence/windows_probe.py > evidence/windows-probe.log 2>&1`, rc=0. Đây là **Linux có bơm mô hình lỗi xoá tệp chỉ đọc**, không phải chạy lại Windows:

  ```text
  OBJECT_UNLINK mode=0o444 writable=False
  HEAD_WITH_READONLY_MODEL: PermissionError: ... INJECTED Windows read-only deletion model; WinError 5 ...
  OBJECT_UNLINK mode=0o644 writable=True
  WRITE_BIT_FIX_WITH_READONLY_MODEL: PASS
  WRITE_BIT_FIX_SHOW_RC_MUTANT: AssertionError: wp929 ['docs/adr/0100-ghi-chu.md']: đòi {'luat_adr0054': False}, được {'luat_adr0054': True}
  ```

  **Vá tối thiểu:** tại nhóm helper r929 trong tệp test, tách callback thành helper: lấy đúng OID blob ghi chú như hiện tại, dựng đúng đường dẫn object trong fixture, thêm quyền ghi bằng `p.chmod(p.stat().st_mode | stat.S_IWRITE)` (import `stat`), rồi `p.unlink()`. Probe dùng helper tương đương qua callback trong bộ nhớ; không ghi bản vá vào checkout. Giữ nguyên ca lỗi show và khẳng định False.

  **Phép kiểm đóng:** baseline `r929_show_loi_la_false` PASS trên Windows thật; mutant `r929_bo_rc_show` chết bằng `AssertionError` False/True ở `_kiem`; đối chứng xanh; gate Windows kết thúc rc=0 với số ca đạt bằng số ca thực chạy. Không skip Windows hoặc nuốt PermissionError. Log native còn in `ok r929_bo_rc_show`; dòng đó không chứng minh chết đúng chốt khi baseline của chính ca đã lỗi fixture. Phải kiểm lớp ngoại lệ và vị trí chết.

  **Rủi ro bản vá:** helper trỏ nhầm object hoặc xử lý lỗi quá rộng có thể phá fixture hoặc che lỗi thật. Giới hạn thao tác vào đúng blob ghi chú trong kho tạm, để lỗi I/O khác nổi lên. Hướng sửa đã qua probe mô hình; **native Windows sau vá chưa chạy**. Owner đề xuất: executor/maintainer `packet_loop_test.py`.

Finding kế thừa dưới đây không được đếm là finding mới:

- **[P3] wp929-git-error-guards-unmeasured** — suite PR chưa khoá riêng `ls[0] == 0` tại `packet_loop.py:2576`. Lượt này tự kiểm chốt sản phẩm và mutant trên **12 ca bắt buộc** (10 r929, một ca `r812_r7_activation_*` hiện có, cùng `r812_khong_kich_hoat_la_false`). Không nhận kết quả mutant 159 ca của lượt 2 làm phép đo mới.

  **Lệnh:** `python3 -B evidence/ls_probe.py > evidence/ls-probe.log 2>&1`, rc=0. Output:

  ```text
  DROP_LS_RC_REQUIRED_CASES: passed=12/12; skipped=0
  HEAD_LS_ERROR: PASS; injection=[{'args': ['ls-tree', '-z', 'refs/remotes/origin/master', 'docs/adr/'], 'original_rc': 0, 'injected_rc': 128, 'stdout_bytes': 287}]
  DROP_GUARD_LS_ERROR: AssertionError: wp929 ['docs/adr/0100-ghi-chu.md']: đòi {'luat_adr0054': False}, được {'luat_adr0054': True}; injection=[... 'original_rc': 0, 'injected_rc': 128, 'stdout_bytes': 287}]
  ```

  Probe dựng baseline dương bằng fixture sẵn có rồi chạy lại CLI `record-lease` trong subprocess. Wrapper chỉ đổi rc của đúng lệnh ls-tree thành 128, giữ stdout Git thật; kiểm wrapper được gọi đúng một lần. HEAD đóng về False, bỏ chốt thì True. Sản phẩm xử lý đúng: giữ **nợ độ phủ P3**, độc lập với lỗi gate Windows P2.

  **Vá ở đâu/cách vá/phép kiểm:** thêm ca lỗi ls-tree có stdout hợp lệ vào nhóm r929 và mutant bỏ riêng chốt rc vào `MUTANTS`. Baseline True, ca lỗi False, bỏ chốt phải chết tại so sánh state, đối chứng xanh. Rủi ro: instrumentation quá rộng làm fetch/validator chết trước chỗ đo. Owner đề xuất: executor/maintainer tệp test. Quyết định: giữ mở dưới dạng nợ P3; không cần sửa chốt sản phẩm đang đúng.

## Phép đo đã chạy

Lệnh tính từ `rv3`, trừ khi ghi chạy trong `tmp/k`. Tạo bản sao bằng `cp -a cay-kho tmp/k`; chỉ ghim `core.abbrev=7` trên bản sao. Runner nạp module test từ bản sao và gọi `chay_suite(..., chi_chay={...})`; fixture/mutant nằm ngoài `cay-kho/`. Script chạy lại sẽ chọn scratch mới nếu thư mục kết quả đã tồn tại. Git system/global bị cô lập bằng `/dev/null`; không sửa cấu hình nguồn.

| Lệnh/phạm vi | Kết quả thực đo |
| --- | --- |
| `git -C cay-kho rev-parse HEAD refs/remotes/origin/master HEAD^1 HEAD^2` | rc=0; lần lượt f3b54d2…, 36057e8…, 227dcde…, 36057e8…; OID đầy đủ trong audit log |
| `git -C cay-kho diff --stat 227dcde f3b54d2 -- .claude/dev/packet_loop.py .claude/dev/packet_loop_test.py` | rc=0, output rỗng |
| `git -C cay-kho diff --name-status f3b54d2^1 f3b54d2` | rc=0; bảy đường dẫn merge, không có write set |
| `python3 -B evidence/audit.py before` | rc=0; HEAD/tree/base/SPEC đúng; `diff.patch` khớp byte với `git diff 36057e8..f3b54d2`; nguồn khớp Git blob và bản sao |
| `python3 -B evidence/review_runner.py baseline > evidence/baseline.log 2>&1` | rc=0; **159/159 PASS**, gồm 149 r812 + 10 r929; failed=0, skipped=0; đủ 12 ca prompt yêu cầu |
| `python3 -B evidence/review_runner.py mutants > evidence/mutants.log 2>&1` | rc=0; **11/11 valid_kill=True**: toàn bộ 10 mutant r929 và mutant r812 tên ADR; tổng 12 khẳng định đích đỏ đúng, 33/33 lượt đối chứng xanh, skipped=0 |
| `python3 -B evidence/windows_probe.py` | rc=0; bằng chứng native đã giao và mô hình Linux như P2; native Windows sau vá: **not_run** |
| `python3 -B evidence/ls_probe.py` | rc=0; 12/12 ca hiện có sống khi bỏ chốt; probe CLI bổ sung phân biệt HEAD/mutant |
| `python3 -B -m ruff check --no-cache --select F --output-format json <hai blob base hoặc head>` qua `audit.py before` | Ruff **0.17.2**; base/head cùng rc=1, cùng 1 F841 + 2 F541, delta=0; không tuyên bố lint sạch hoặc đã đo Ruff 0.15.15 của CI |
| Trong `tmp/k`: `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null PYTHONDONTWRITEBYTECODE=1 python3 -B .claude/dev/packet_loop.py doctrine-scan --root .` | rc=0; sạch, 10 tệp |
| Trong `tmp/k`: cùng env, `python3 -B .claude/dev/packet_loop.py adr-song --root .` | rc=0; 55 ADR/55 dòng §20, khớp 1–1 |
| Trong `tmp/k`: cùng env, `python3 -B .claude/dev/ci_dang_ky_test.py` (không `--chay`) | rc=0; `PHẢN CHỨNG: 1070/1070 đỏ đúng`; `TỔNG: ĐẠT`; log `evidence/ci-dang-ky.log` |
| `git -C cay-kho diff --check 36057e8 f3b54d2` (trong audit) | rc=0 |
| `python3 -B evidence/audit.py after` | rc=0; `SOURCE_DELTA [] files=6064`, tracked/untracked/ignored sạch; HEAD/tree và hai tệp đã kiểm thử khớp nguồn |

**M1–M4 trên đúng head:**

- M1: `ls-tree -z` đọc metadata/tên tách bằng NUL/TAB; chỉ nhận mode 100644/100755, type blob, tên con trực tiếp đúng regex; loại ADR-0054; đọc từng ứng viên và chuẩn hoá NFC; đòi đúng một cụm khai và rc đọc đều 0. Metadata thay `--name-only` để tránh lỗi nhận tree/symlink lượt 1. Các chốt shallow, land-OID, first-parent, §20 giữ nguyên. Lỗi show/ls có phép đo riêng ở trên.
- M2/phạm vi: bỏ `ADR0055_TEP`, không thêm hằng runtime ghim số ADR kích hoạt, không đổi `ADR0054_TEP`, `LUAT_0054_RE` hay chữ ký. AST sản phẩm ngoài hàm/hằng được phép giống base. Diff đúng hai tệp: sản phẩm +7/−3, test +71/−4, tổng **78 dòng thêm ≤ 300**. PR không đổi docs, manifest, VERSION hoặc frozen spec. Docs/ADR-0056 đi vào qua merge master.
- M3: (a)–(d) và (e) đổi ADR đích đều PASS qua CLI `record-lease` trên Linux. Không thay các ca ấy bằng gọi hàm nội bộ.
- M4: cả bốn mutant bắt buộc giết đúng ca, đọc được `AssertionError` của state. Bảng đủ 11 mutant đã chạy:

| Mutant | Ca đích | Khẳng định đỏ |
| --- | --- | --- |
| `r929_duong_dan_co_dinh_0055` | (a) `r929_kich_hoat_so_bat_ky` | cần True, được False |
| `r929_hai_chuoi_roi` | (b) `r929_hai_chuoi_roi_khong_tinh` | cần False, được True |
| `r929_mot_tro_len` | (c) `r929_hai_tep_kich_hoat` | cần False, được True |
| `r929_bo_loai_tru_adr0054` | (d) `r929_chi_adr0054_tu_neu_cum` | cần False, được True |
| `r812_r7_activation_adr_name` | (e) `r812_r7_activation_adr_name` | cần False, được True |
| `r929_bo_kiem_loai_doi_tuong` | tree và symlink | cả hai cần False, được True |
| `r929_nhan_symlink` | symlink | cần False, được True |
| `r929_so_chu_so_tuy_y` | ba chữ số | cần False, được True |
| `r929_bo_duoi_md` | đuôi khác .md | cần False, được True |
| `r929_bo_nfc` | NFD | cần True, được False |
| `r929_bo_rc_show` | lỗi show | cần False, được True |

**Kho thật:** `audit.py before` gọi mã từ bản sao với root đọc là `cay-kho`: cả SPEC được giao và dòng khai hợp lệ neo land-OID `7cc384ec9e02ed79b429ac6ee2455d3bfbb75b16` đều trả False. Có 55 ADR thường; chỉ chính ADR-0054 chứa cụm và bị loại, nên số tệp kích hoạt hợp lệ bằng 0. Không kích hoạt ADR-0054 trong kho thật.

**Giới hạn:** không chạy toàn bộ N1 gồm 876 ca/1249 mutant; không suy full-suite xanh từ 159 ca đích. N6 check run mới trên head chưa truy vấn vì bundle offline. Bằng chứng Windows đã giao là FAILED trên ab94c4f với hai tệp giống byte. Ubuntu xanh cùng run là thông tin từ prompt, không có log Ubuntu để tự xác minh. Các probe parser/gitlink riêng ở lượt 2 không được tuyên bố đã chạy lại.

Review do phiên Codex/OpenAI có shell/tools thực hiện, execution surface service/cloud, transport machine. Không có phép đo độc lập về model/effort thực phục vụ, launcher receipt hoặc session identity của executor; không tự xác nhận assurance `cross_approved`. Sandbox thực tế workspace-write; giữ `cay-kho/` read-only theo nhiệm vụ, không tuyên bố OS cưỡng chế read-only. Snapshot đầu/cuối gồm nội dung, mode và metadata Git chứng minh không có delta quan sát được, không chứng minh toàn bộ lịch sử ghi. Không mạng, không sửa/push/merge nguồn, không gửi thông điệp ngoài; commit/push fixture chỉ tới bare repo tạm. Không tự soạn nội dung thoát cây. Script/log/JSON nằm trong `evidence/`; `VERDICT.md` đã được tạo ngay từ đầu và cập nhật theo phép đo.
