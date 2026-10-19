Reviewed commit: 701f41c686cef8456d43528ab9556a6b867cd7d6

verdict: approve
P1=0 P2=0 P3=0

## Phạm vi và danh tính

- Base: `e0273d31aba78b014aa89297f32ff86f9daf0277`.
- Head tree: `861df62ee0c17abf423908c5f41ba59b2604fdb4`.
- Spec SHA-256: `da3095b47567dc8cb94137d0cc675d722eb256a77c8e06ddb90a216e7f148666`, đã đối chiếu trước khi dùng.
- Diff: đúng 2 tệp trong write set, **77 dòng thêm / 8 dòng xoá**, dưới trần 300 dòng thêm. Blob `launcher.py` giống hệt base.
- Reviewer độc lập với executor theo chỉ thị phiên: Codex, họ GPT-6 theo thông tin hệ thống; provider `openai_codex`, execution surface `codex_service`, transport `machine`. Không có phép đo độc lập exact serving model/effort hoặc receipt xác thực họ model. Không tự nhận Human Audit hay đã hoàn tất assurance `human_audited`.
- Môi trường đo: Linux x86_64, Python **3.12.3 / 3.13.16**, Ruff **0.16.8**, Git **2.43.0**, ngày 16-10-2026 UTC.
- Kho nguồn được giữ read-only; mọi test thực thi trên clone ngoài kho nguồn; mọi thay đổi mutant nằm trong clone riêng `/tmp/wp766-mutants-…/repo`. Không dùng worktree. Các script/log review nằm trong thư mục ra.

Áp ngưỡng được giao: approve khi P1=0 và P2=0. Approval này là kết luận review mã trên exact SHA; các mục hồ sơ GitHub/assurance chưa xác minh được ghi riêng ở cuối.

## Findings

Không phát hiện lỗi P1/P2/P3 cần sửa trong diff. Lỗi PID của **base** đã tái hiện và được head khắc phục; không tính lỗi đã sửa thành finding mở. `r351` trên Python 3.12 và 5 lỗi Ruff F841 đều tồn tại nguyên vẹn ở base.

## Hướng thử độc lập

Các script dưới đây ở thư mục ra; chúng lưu lệnh con, cwd, rc và stdout/stderr vào `evidence/`. Ký hiệu `B313/H313/B312/H312` được khai trong mục Đã đo.

| # | Giả thuyết | Lệnh đã chạy | Output thật cắt gọn | Kết luận |
|---|---|---|---|---|
| 1 | Base t81 phụ thuộc PID thật của lượt chạy | `python3.13 -B pid_matrix.py` → shim trên base, Python 3.12/3.13 | `getpid=10: rc=1 … tien trinh mu NGOAI cay…`; `11: rc=1 … hau due…`; `12: rc=1 … NGOAI cay…` | **LỖI trên base; đã sửa ở head** |
| 2 | Head t81 hoặc r766 vẫn đỏ với PID cũ/PID mới | Cùng ma trận: cả hai ca trên head, ép `that,1,10,11,12,13,14,15,99999` | `MATRIX commands=54 unexpected=0`; cả 36 lượt head rc=0 | **KHÔNG PHẢI LỖI** |
| 3 | Helper đọc PID quá sớm hoặc va chạm PID cha | `python3.12 -B properties.py`; `python3.13 -B properties.py` | Mỗi phiên bản: `CROSS_PRODUCT t81=544 r766=64 allocations_checked=973 failures=0` | **KHÔNG PHẢI LỖI** |
| 4 | Đổi fixture làm đổi hình cây hoặc nghĩa hai vế | Cùng script `properties.py`, ghi cây từ `_than_t81` thật | `(a) root=13, {13:12,14:13} → null`; `(b) {13:12,15:13,14:12} → {13:win:123,15:win:456}` | **KHÔNG PHẢI LỖI** |
| 5 | Vế (a) không còn bắt việc bỏ fail-closed | `python3.13 -B mutants.py` trên clone riêng | `chup_cay_khong_fail_closed_trong_cay`: rc=1; `TinHieuChotCa: hau due khong lay duoc khoa bi bo qua im lang` | **KHÔNG PHẢI LỖI** |
| 6 | Vế (b) không còn bắt việc hỏi khoá toàn máy | Cùng script, mutant `chup_cay_fail_closed_ca_may` | rc=1; `TinHieuChotCa: tien trinh mu NGOAI cay khong duoc lam hong ca anh` | **KHÔNG PHẢI LỖI** |
| 7 | r766 xanh giả khi bỏ tránh PID | Cùng script, mutant `pid_gia_quay_ve_ghi_cung` | rc=1; `TinHieuChotCa: getpid=11: tien trinh mu NGOAI cay…`; `TARGETED_MUTANTS=3 assertion_kills=3 OK=True` | **KHÔNG PHẢI LỖI** |
| 8 | `os.getpid` rò khi ném lỗi giữa vòng, làm hỏng ca sau | Hai lượt `properties.py`, ném lỗi ở vòng thứ hai | `restored: true` với `TinHieuChotCa`, `RuntimeError`, `SystemExit`, `KeyboardInterrupt`; `HARNESS_AFTER_FAILURE passed=1 skipped=0 failed=1 next_case=PASS` | **KHÔNG PHẢI LỖI**; một failure là sentinel cố ý |
| 9 | M1 bỏ sót ca dùng PID giả ở hai điểm loại trừ | `python3.13 -B audit_base.py`; grep tĩnh các điểm tự nhận diện; ép PID trên t78/t83/t92 | `AUDIT_CASES=t156…,t157…,t160…,t161…,t81…`; PID giả chỉ ở t81; 4 lượt ca đã stub đều rc=0 | **KHÔNG PHẢI LỖI** trong phạm vi đo/đọc nêu dưới |
| 10 | Có điểm so PID với chính mình mà hai hook bỏ sót | `rg -n` các tên PID, `/proc/self`, Win32 current-process trong `launcher.py` | getpid chỉ tại 544, 626, 1490; getpgid tại 1007; không có getppid hoặc `/proc/self` | **KHÔNG PHẢI LỖI**; 1490 đặt tên tệp tạm, 1007 so pgid của mục tiêu với PID mục tiêu |
| 11 | Có hồi quy theo thứ tự/chạy toàn suite | `python3.13 -B full_delta.py 3.12`; cùng lệnh với `3.13` | Cả hai in `DELTA_EQUAL=True`; tổng 196→197; giữ nguyên tập hỏng/bỏ qua | **KHÔNG PHẢI LỖI**; có ca chưa đo, xem cuối |
| 12 | Có mutant sống mới | `python3.13 -B .claude/dev/launcher_test.py --dot-bien` trên B313 và H313 | Base `235/235 dat`; head `236/236 dat`; cùng 1 không đo được | **KHÔNG PHẢI LỖI** |
| 13 | Diff thêm lỗi lint | `ruff check --select F …` trên B313/H313; so multiset `(code,message)` bằng JSON | Cùng `Found 5 errors`; `DELTA_EQUAL True`; 5 tên biến giống nhau | **KHÔNG PHẢI LỖI** |
| 14 | Bảng M1 thiếu trong thân PR | `gh pr view 772 … --json headRefOid,baseRefOid,body,number,url`; web open PR/Issue | gh rc=1: `socket: operation not permitted`; web: `Cache miss` | **KHÔNG ĐO ĐƯỢC**, không suy ra bảng vắng mặt |

## Đối chiếu M1–M5 và nghiệm thu

**M1 — kiểm kê trước bản vá.** Sweep độc lập chạy trên exact base, giữ nguyên giá trị getpid và ghi ca/snapshot tại hai điểm loại trừ. Đã đọc thêm các điểm truy cập PID của launcher, các lệnh `stop`/sổ PID của test và mọi tham chiếu `_chup_cay`/`_giet_rieng`/`_giet_cay`. Các đường CLI dùng PID tiến trình con thật (t31 thay PID sổ bằng `moi.pid`); không tìm thấy fixture PID cứng mới lọt vào hai điểm loại trừ. Hook nằm trong tiến trình test, không tự truyền sang subprocess; kết luận cho các đường CLI còn dựa trên việc đọc nguồn. Chín ca bị skip không được tính là đã chạy.

| Ca trên base | PID hoặc ảnh quan sát | Phép ép/kết quả thực đo | Giải thích |
|---|---|---|---|
| t81, vế (a)/(b) | root 10; ảnh trước loại trừ `{10,11}` / `{10,12}` | Python 3.12 và 3.13: ép 10 → rc=1, vế (b) | Root bị loại khỏi ảnh (b) |
| t81 | Cùng fixture | Ép 11 → rc=1, vế (a) | Con mù bị loại, ảnh không còn fail-closed |
| t81 | Cùng fixture | Ép 12 → rc=1, vế (b) | Con thường bị loại khỏi ảnh (b) |
| t81, controls | Cùng fixture | `that,1,13,14,15,99999` đều rc=0 trên cả hai Python | Không loại PID đang cần trong fixture |
| t156 | `_giet_rieng`: PID **2371**, ảnh `{2371:k}` | Sweep base qua | Đây là con thật đã wait, từ `_cs_con_da_wait()`, không phải PID giả cứng |
| t157 | Root/ảnh **2378** | Sweep base qua ở cả hai điểm | PID thật từ `Popen.pid` |
| t160 | Root **2406**, ảnh `{2406,2407}` | Sweep base qua ở cả hai điểm | Mẹ/cháu thật; số PID chỉ là giá trị quan sát của lượt này |
| t161 | Root mẹ đã thoát **2408**, ảnh cháu **2409** | Sweep base qua ở cả hai điểm | Mẹ/cháu thật |
| t78, t83 | PID giả **12345** | Ép getpid=12345, từng ca rc=0 | `_chup_cay` được stub; không đưa PID giả vào phép loại trừ thật |
| t92 | PID giả **500,501** | Ép getpid=500 và 501, từng lượt rc=0 | Cả `_chup_cay` và `_giet_rieng` được stub; getpgid/killpg cũng được kiểm soát |

Lệnh tái lập mỗi ô t81: ở clone base, `PYTHONDONTWRITEBYTECODE=1 python3.12 -B $OUT/ep_pid.py <PID> --lap-ca t81_chup_cay_windows_thieu_creationdate_phai_fail_closed --lan 1`, rồi lặp bằng `python3.13`. Mọi argv/rc/stdout riêng trong [pid-matrix.json](evidence/pid-matrix.json). Lệnh t78/t83/t92 và output nằm trong [m1-stubbed-fakes.log](evidence/m1-stubbed-fakes.log). Bảng M1 trong **thân PR** và thứ tự executor lập bảng trước khi vá chưa kiểm chứng được do không truy cập được GitHub; bảng trên là kết quả của reviewer, không phải xác nhận hồ sơ PR.

**M2 — helper, hình cây và phạm vi.** `launcher_test.py:1931` đọc cả hai PID ngay khi gọi. Với `n=4, tu=10`, tối đa hai số bị loại nên mọi PID fixture nằm trong 10…15. Ma trận bên ngoài đã ép toàn bộ 10…15; kiểm tra tích chéo dùng self PID `1…64,4096,65535,99999,2147483647` × parent PID `1,10,11,12,13,14,15,99999`, gồm cả tình huống hai giá trị trùng nhau. Mỗi phiên bản kiểm 544 thân t81 và 64 r766, đồng thời khẳng định kết quả helper luôn có 4 số khác nhau và không chứa self/parent đang bị ép. Không có cache PID lúc import. Nếu self PID ngoài 10…15, nó không thể trùng một PID được helper chọn; đây là suy luận trực tiếp từ vòng lặp, không phải tuyên bố đã chạy mọi số nguyên.

`launcher_test.py:1954` vẫn dựng con mù dưới gốc; `:1958` vẫn dựng con mù làm anh em của gốc, cùng cha. Ghi ảnh thực trong `properties.py` xác nhận hai đồ thị đồng dạng với base. Chốt `mu not in da_hoi` vẫn chạy. Hai mutant sản phẩm vẫn chết bởi đúng chốt (a)/(b).

**M3 — hồi quy và hoàn nguyên.** `:1975` lấy tập ép gồm 1, PID cũ và cả bốn PID baseline, có PID cha giả. Mỗi lượt `_than_t81()` tính lại fixture theo PID đang ép. `finally` ở `:1983` hoàn nguyên đúng đối tượng hàm, kể cả khi ném tín hiệu chốt, lỗi thường hoặc tín hiệu thoát ở lượt thứ hai. Đã kiểm trực tiếp trước khi context harness hoàn nguyên và kiểm ca kế sau bằng `chay_bo_ca`. Cả bốn full-suite journal đều đi qua các ca sau r766 đến cuối; tổng tăng đúng một.

**M4 — đột biến.** Ba mutant trọng tâm được thay trên bản sao toàn kho, mỗi lần khôi phục nguồn sạch trước mutant kế. Cả CLI (`LAP …: 0/1 qua`, rc=1, stderr rỗng, không traceback) và lời gọi trực tiếp (đúng class `TinHieuChotCa`) cùng xác nhận chết vì assertion mong muốn. Mutant harness bỏ tập tránh tạo `(cha,goc,mu,con)=(10,11,12,13)`, nên r766 bắt ở `getpid=11`, vế (b), đúng lời khai changelog. Toàn bảng trên Python 3.13: base 235/235 đo được, head 236/236; không có mutant sống mới, cùng 1 không đo được.

**M5 — changelog/docstring.** Fragment tiếng Anh tồn tại, mô tả đúng lỗi, tránh self/parent khi gọi, ca mới và mutant mới. Các khẳng định getpid=10/11/12, mutant chết tại 11 và sweep chỉ t81 dùng PID giả tại hai điểm loại trừ được tái hiện trong phạm vi trên. Docstring nói rõ tránh parent là phòng thủ và không có mutant riêng; launcher không đọc getppid. Không tìm thấy phản ví dụ làm lời khai kỹ thuật sai. Tần suất va chạm thực ngoài CI chưa được đo.

## Đã đo

Đường dẫn rig (được tạo theo cặp, checkout/config trong cùng một lệnh `full_delta.py`, cùng nguồn clone và `core.abbrev=7`):

- `B313` = `/tmp/wp766-py3.13-acqiixhk/base`.
- `H313` = `/tmp/wp766-py3.13-acqiixhk/head`.
- `B312` = `/tmp/wp766-py3.12-1rql23bi/base`.
- `H312` = `/tmp/wp766-py3.12-1rql23bi/head`.
- `$OUT` = `/tmp/claude-0/-home-user-tra-luat/4db0e1e9-e429-5947-8704-a56b7bbfbbd7/scratchpad/rv1-out`; `$KHO` = `/tmp/claude-0/-home-user-tra-luat/4db0e1e9-e429-5947-8704-a56b7bbfbbd7/scratchpad/rv1`.

| Python | Vế | Qua / đã chạy | Tổng | Bỏ qua | Hỏng | rc |
|---|---|---|---|---|---|---|
| 3.12 | base | 186/187 | 196 | 9 | 1 | 1 |
| 3.12 | head | 187/188 | 197 | 9 | 1 | 1 |
| 3.13 | base | 187/187 | 196 | 9 | 0 | 0 |
| 3.13 | head | 188/188 | 197 | 9 | 0 | 0 |

Hai driver delta đều rc=0 và `DELTA_EQUAL=True`: tên/lý do hỏng và bỏ qua giống hệt giữa base/head của cùng Python. Python 3.12 có đúng `r351_KHONG_co_chi_thi_thi_van_phai_dat_moc` đỏ sẵn: `khong co chi thi ma cung khong dat moc — hook se chay pip moi luot`. Không gọi Python 3.12 là toàn suite xanh. Python 3.13 không có ca hỏng, nhưng cả hai vế vẫn bỏ qua 9 ca.

Nhật ký lệnh chính có cwd, argv nguyên văn, thời gian, rc và đường output ở [commands.jsonl](evidence/commands.jsonl). Bảng dưới liệt kê **tất cả** các lệnh được ghi qua runner, gồm cả lần thử không thành công; lệnh `-c` dài được giữ nguyên trong phụ lục ngay dưới.

| Nhãn | Lệnh | rc | Kết quả / log |
|---|---|---|---|
| full-delta-313 | `python3.13 -B full_delta.py 3.13` | 0 | Suite base/head rc=0/0; tập skip giữ nguyên — [log](evidence/full-delta-313.log) |
| full-delta-312 | `python3.13 -B full_delta.py 3.12` | 0 | Suite base/head rc=1/1; cùng r351 đỏ sẵn — [log](evidence/full-delta-312.log) |
| pid-matrix | `python3.13 -B pid_matrix.py` | 0 | 54 lượt, đúng kỳ vọng; 6 lần đỏ trên base, 48 qua — [log](evidence/pid-matrix.log) |
| static-sites | `rg -n 'getpid\|getppid\|/proc/self\|/proc/thread-self\|GetCurrentProcessId\|GetCurrentProcess\|current_process\|os\.getpgrp\|os\.getpgid' .claude/dev/launcher.py` | 0 | Hai loại trừ self, thêm đặt tên tệp tạm và getpgid mục tiêu — [log](evidence/static-sites.log) |
| pr-evidence | `gh pr view 772 --repo ducthangho/tra-luat --json headRefOid,baseRefOid,body,number,url` | 1 | Không kết nối được proxy, chưa đọc thân PR — [log](evidence/pr-evidence.log) |
| targeted-mutants | `python3.13 -B mutants.py` | 1 | Script reviewer dừng do đếm cả chuỗi mô tả trong bảng mutant; không phải lỗi head — [log](evidence/targeted-mutants.log) |
| mutation-full | `python3.13 -B .claude/dev/launcher_test.py --dot-bien` | 0 | 236/236, 1 không đo được — [log](evidence/mutation-full.log) |
| base-audit | `python3.13 -B audit_base.py` | 0 | 187 qua, 9 skip; 5 ca chạm điểm loại trừ — [log](evidence/base-audit.log) |
| ruff-base | `python3.13 -m ruff check --select F .claude/dev/launcher_test.py` | 1 | Python không có module ruff — [log](evidence/ruff-base.log) |
| ruff-head | `python3.13 -m ruff check --select F .claude/dev/launcher_test.py` | 1 | Python không có module ruff — [log](evidence/ruff-head.log) |
| targeted-mutants-retry | `python3.13 -B mutants.py` | 0 | Đã sửa neo script reviewer bằng đầu dòng; 3/3 đúng TinHieuChotCa — [log](evidence/targeted-mutants-retry.log) |
| ruff-cli-head | `ruff check --select F .claude/dev/launcher_test.py` | 1 | 5 F841 giống base — [log](evidence/ruff-cli-head.log) |
| ruff-cli-base | `ruff check --select F .claude/dev/launcher_test.py` | 1 | 5 F841 có sẵn — [log](evidence/ruff-cli-base.log) |
| properties-313 | `python3.13 -B properties.py` | 0 | 544 t81 + 64 r766; cây và hoàn nguyên đạt — [log](evidence/properties-313.log) |
| properties-312 | `python3.12 -B properties.py` | 0 | 544 t81 + 64 r766; cây và hoàn nguyên đạt — [log](evidence/properties-312.log) |
| integrity | `python3.13 -B -c <nguyên văn ở phụ lục>` | 0 | Head/tree/spec đúng; status sạch; launcher không đổi — [log](evidence/integrity.log) |
| mutation-base | `python3.13 -B .claude/dev/launcher_test.py --dot-bien` | 0 | 235/235, 1 không đo được — [log](evidence/mutation-base.log) |
| m1-stubbed-fakes | `python3.13 -B -c <nguyên văn ở phụ lục>` | 0 | t78(12345), t83(12345), t92(500,501): 4 rc=0 — [log](evidence/m1-stubbed-fakes.log) |
| ruff-normalized | `python3.13 -B -c <nguyên văn ở phụ lục>` | 0 | Multiset code/message 5→5, delta=0 — [log](evidence/ruff-normalized.log) |
| environment | `python3.13 -B -c <nguyên văn ở phụ lục>` | 0 | Python 3.12.3/3.13.16; Ruff 0.16.8; Git 2.43.0 — [log](evidence/environment.log) |
| integrity-final | `python3.13 -B -c <nguyên văn ở phụ lục>` | 0 | Kiểm lại cuối phiên: head/tree/status và blob các tệp nguồn giữ nguyên — [log](evidence/integrity-final.log) |


Các lệnh con full-suite thực thi là `PYTHONDONTWRITEBYTECODE=1 python3.12 -B .claude/dev/launcher_test.py --nhat-ky $OUT/evidence/full_3.12_base.journal` ở B312 và tương ứng head/H312; lặp với `python3.13` ở B313/H313. rc từng vế nằm trong bảng trên; lệnh setup clone/checkout/config cùng rc nằm trong log driver. Ba lượt gọi trực tiếp mutant đều bắt và xác nhận class ngoại lệ, không dùng traceback làm bằng chứng.

Các lệnh đọc/định danh ngoài runner đã chạy: `pwd`; `rg --files … -g AGENTS.md`; `cat` prompt/spec/shim/AGENTS và các đoạn liên quan trong `CONTEXT.md`, `CLAUDE.md`, protocol, kế hoạch provider, fragment wp-727; `sha256sum spec-wp766.md`; `git status --short`, `git rev-parse HEAD`, `git rev-parse HEAD^{tree}`, `git diff --stat/--numstat/diff e0273d3 701f41c`; `command -v python3.12 python3.13`, `command -v ruff python python3`, `python --version`; các lượt `rg -n`, `sed -n`, `nl -ba` đọc nguồn được nêu ở phần đối chiếu; `cat/tail/rg` đọc journal/log/rig JSON và `ls` để định vị tệp. Các nhóm đọc hoàn tất rc=0; một lượt `cat rig-3.12.json` khi clone chưa dựng xong báo chưa có tệp, sau đó rig được tạo và đo đủ. Lệnh thăm dò `python3 -m ruff --version` báo không có module; binary Ruff được dùng thay. Các lệnh đọc log không được tính thành phép thử mới.

## KHÔNG ĐO ĐƯỢC

1. **Hồ sơ ngoài kho:** thân PR #772, bảng M1/argv trong thân PR, mốc lập bảng trước khi vá, nội dung lease/Issue mới nhất, assurance/human audit và CI GitHub. `gh pr view` bị sandbox chặn socket proxy; web open [PR #772](https://github.com/ducthangho/tra-luat/pull/772) và [Issue #766](https://github.com/ducthangho/tra-luat/issues/766) đều trả `Failed to fetch … Cache miss`. Không khẳng định hồ sơ thiếu hay đã đạt. Review dùng exact OID và đặc tả đã băm theo chỉ thị phiên.
2. **Chín ca không chạy trên mỗi vế suite:** t62 chỉ Windows; tám ca sau tự báo `KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)` trong sandbox. Chúng không được coi là pass; tập skip giống nhau ở cả bốn lượt:

   - `r345_chan_socket_that_ma_than_hook_van_chay_dung`.
   - `r345_cac_phep_do_cuc_bo_van_dung`.
   - `r345_lop_tham_import_van_co_rang`.
   - `r345_dot_bien_ba_phep_do_cuc_bo_lam_ca_dich_DO`.
   - `r347_tham_import_van_song_tren_python_truoc_310`.
   - `r347_dot_bien_bo_duong_lui_310_lam_ca_dich_DO`.
   - `r348_goi_chi_co_CLI_khong_duoc_bao_dong_gia`.
   - `r348_dot_bien_bo_isidentifier_lam_ca_dich_DO`.


3. **Windows thật:** không chạy Windows CI/Toolhelp32 thật; t81 chạy nhánh Windows bằng fixture như thiết kế được giao. Mutant `124_khi_chau_con_song` cùng không đo được trên base/head vì t62 bỏ qua trên Linux. Không ngoại suy kết quả 236/236 thành phủ tất cả 237 mutant trên mọi nền.
4. **Đột biến riêng cho né PID cha:** chưa tạo/chạy; mã sản phẩm không loại PID cha, nên bỏ né parent không nhất thiết làm t81 đỏ. Reviewer đã kiểm hành vi helper né parent bằng tích chéo; điều này không thay thế một mutant riêng nếu sau này cần khoá yêu cầu phòng thủ ấy.
5. **Số đo executor khác rig:** không tái tạo headline 195/195→196/196 của executor vì rig này bỏ qua thêm tám ca venv/pip. Kết quả độc lập thực có ở bảng: 187/187→188/188 trên 3.13; 186/187→187/188 trên 3.12. Chỉ kết luận delta bằng 0 và ca mới qua trong phần đo được.
6. **Tần suất PID va chạm thực trên CI** và toàn bộ không gian PID thật chưa được chạy; phép đo dùng shim/property sweep, kèm lập luận về miền PID 10…15 của helper. Hai commit lịch sử `9fddb1d`/`80e0fac` được nhắc trong docstring không được chạy lại; lỗi đã được tái hiện trên exact base được giao.
7. `python3.13 -m ruff` không chạy được do không có module; binary Ruff cùng phiên bản đo cả hai vế đã xác nhận delta F=0. Đây là thay bề mặt gọi công cụ, không coi lệnh module thất bại là pass.

## Phụ lục lệnh nguyên văn và rc

Các phép đo sau được thực thi bằng `python3.13 measure.py <nhãn> <cwd> -- <argv>`, với `PYTHONDONTWRITEBYTECODE=1` và `PYTHONUNBUFFERED=1`. Phụ lục giữ nguyên cả những lần thử thất bại. Scripts `full_delta.py`, `pid_matrix.py`, `mutants.py`, `properties.py`, `audit_base.py` là artifact reviewer có thể đọc để tái lập; chúng không phải bản vá đưa cho executor.

<details>
<summary>Lệnh chính, cwd và mã thoát</summary>

**full-delta-313 — rc=0; cwd=.**

```sh
python3.13 -B full_delta.py 3.13
```

**full-delta-312 — rc=0; cwd=.**

```sh
python3.13 -B full_delta.py 3.12
```

**pid-matrix — rc=0; cwd=.**

```sh
python3.13 -B pid_matrix.py
```

**static-sites — rc=0; cwd=../rv1**

```sh
rg -n 'getpid|getppid|/proc/self|/proc/thread-self|GetCurrentProcessId|GetCurrentProcess|current_process|os\.getpgrp|os\.getpgid' .claude/dev/launcher.py
```

**pr-evidence — rc=1; cwd=../rv1**

```sh
gh pr view 772 --repo ducthangho/tra-luat --json headRefOid,baseRefOid,body,number,url
```

**targeted-mutants — rc=1; cwd=.**

```sh
python3.13 -B mutants.py
```

**mutation-full — rc=0; cwd=/tmp/wp766-py3.13-acqiixhk/head**

```sh
python3.13 -B .claude/dev/launcher_test.py --dot-bien
```

**base-audit — rc=0; cwd=.**

```sh
python3.13 -B audit_base.py
```

**ruff-base — rc=1; cwd=/tmp/wp766-py3.13-acqiixhk/base**

```sh
python3.13 -m ruff check --select F .claude/dev/launcher_test.py
```

**ruff-head — rc=1; cwd=/tmp/wp766-py3.13-acqiixhk/head**

```sh
python3.13 -m ruff check --select F .claude/dev/launcher_test.py
```

**targeted-mutants-retry — rc=0; cwd=.**

```sh
python3.13 -B mutants.py
```

**ruff-cli-head — rc=1; cwd=/tmp/wp766-py3.13-acqiixhk/head**

```sh
ruff check --select F .claude/dev/launcher_test.py
```

**ruff-cli-base — rc=1; cwd=/tmp/wp766-py3.13-acqiixhk/base**

```sh
ruff check --select F .claude/dev/launcher_test.py
```

**properties-313 — rc=0; cwd=.**

```sh
python3.13 -B properties.py
```

**properties-312 — rc=0; cwd=.**

```sh
python3.12 -B properties.py
```

**integrity — rc=0; cwd=../rv1**

```sh
python3.13 -B -c 'import hashlib,json,pathlib,subprocess; base="e0273d31aba78b014aa89297f32ff86f9daf0277"; head="701f41c686cef8456d43528ab9556a6b867cd7d6"; run=lambda *a: subprocess.check_output(["git","--no-optional-locks",*a],text=True).strip(); print("HEAD",run("rev-parse","HEAD")); print("TREE",run("rev-parse","HEAD^{tree}")); print("STATUS",repr(run("status","--porcelain"))); print("DIFF",run("diff","--numstat",base,head)); f=".claude/dev/launcher.py"; print("LAUNCHER_UNCHANGED",run("rev-parse",base+":"+f)==run("rev-parse",head+":"+f)); p=pathlib.Path("../rv1-out/spec-wp766.md"); print("SPEC_SHA256",hashlib.sha256(p.read_bytes()).hexdigest())'
```

**mutation-base — rc=0; cwd=/tmp/wp766-py3.13-acqiixhk/base**

```sh
python3.13 -B .claude/dev/launcher_test.py --dot-bien
```

**m1-stubbed-fakes — rc=0; cwd=/tmp/wp766-py3.13-acqiixhk/base**

```sh
python3.13 -B -c 'import json,os,pathlib,subprocess,sys; shim=str(pathlib.Path("/tmp/claude-0/-home-user-tra-luat/4db0e1e9-e429-5947-8704-a56b7bbfbbd7/scratchpad/rv1-out/ep_pid.py")); failures=0
for case,pids in [("t78",[12345]),("t83",[12345]),("t92",[500,501])]:
 for pid in pids:
  args=[sys.executable,"-B",shim,str(pid),"--lap-ca",case,"--lan","1"]; p=subprocess.run(args,capture_output=True,text=True,start_new_session=True); print(json.dumps({"argv":args,"rc":p.returncode,"stdout":p.stdout,"stderr":p.stderr})); failures+=p.returncode!=0
sys.exit(bool(failures))'
```

**ruff-normalized — rc=0; cwd=.**

```sh
python3.13 -B -c 'import collections,json,pathlib,subprocess,sys; paths=json.loads(pathlib.Path("rig-3.13.json").read_text()); seen={}
for side,path in paths.items():
 args=["ruff","check","--select","F","--output-format","json",".claude/dev/launcher_test.py"]; p=subprocess.run(args,cwd=path,capture_output=True,text=True); rows=json.loads(p.stdout); seen[side]=collections.Counter((r["code"],r["message"]) for r in rows); print(side,"rc",p.returncode,"diagnostics",len(rows),"messages",sorted(seen[side].items()))
print("DELTA_EQUAL",seen["base"]==seen["head"]); sys.exit(seen["base"]!=seen["head"])'
```

**environment — rc=0; cwd=.**

```sh
python3.13 -B -c 'import platform,subprocess,sys; print(platform.platform()); print("executable",sys.executable); print("python313",sys.version); print(subprocess.check_output(["python3.12","--version"],text=True).strip()); print(subprocess.check_output(["ruff","--version"],text=True).strip()); print(subprocess.check_output(["git","--version"],text=True).strip())'
```

**integrity-final — rc=0; cwd=../rv1**

```sh
python3.13 -B -c 'import hashlib,pathlib,subprocess; run=lambda *a: subprocess.check_output(["git","--no-optional-locks",*a],text=True).strip(); head=run("rev-parse","HEAD"); print("HEAD",head); assert head=="701f41c686cef8456d43528ab9556a6b867cd7d6"; print("TREE",run("rev-parse","HEAD^{tree}")); status=run("status","--porcelain"); print("STATUS",repr(status)); assert not status
for f in [".claude/dev/launcher.py",".claude/dev/launcher_test.py","changelog.d/wp-766.md"]:
 raw=pathlib.Path(f).read_bytes(); committed=subprocess.check_output(["git","show",head+":"+f]); assert raw==committed; print("UNCHANGED",f,hashlib.sha256(raw).hexdigest())'
```

</details>

<details>
<summary>54 lệnh shim PID và kết quả riêng</summary>

| Python | Vế / cwd | PID | Ca | rc |
|---|---|---|---|---|
| 3.12 | base B313/H313 tương ứng | that | t81 | 0 |
| 3.12 | base B313/H313 tương ứng | 1 | t81 | 0 |
| 3.12 | base B313/H313 tương ứng | 10 | t81 | 1 |
| 3.12 | base B313/H313 tương ứng | 11 | t81 | 1 |
| 3.12 | base B313/H313 tương ứng | 12 | t81 | 1 |
| 3.12 | base B313/H313 tương ứng | 13 | t81 | 0 |
| 3.12 | base B313/H313 tương ứng | 14 | t81 | 0 |
| 3.12 | base B313/H313 tương ứng | 15 | t81 | 0 |
| 3.12 | base B313/H313 tương ứng | 99999 | t81 | 0 |
| 3.12 | head B313/H313 tương ứng | that | t81 | 0 |
| 3.12 | head B313/H313 tương ứng | 1 | t81 | 0 |
| 3.12 | head B313/H313 tương ứng | 10 | t81 | 0 |
| 3.12 | head B313/H313 tương ứng | 11 | t81 | 0 |
| 3.12 | head B313/H313 tương ứng | 12 | t81 | 0 |
| 3.12 | head B313/H313 tương ứng | 13 | t81 | 0 |
| 3.12 | head B313/H313 tương ứng | 14 | t81 | 0 |
| 3.12 | head B313/H313 tương ứng | 15 | t81 | 0 |
| 3.12 | head B313/H313 tương ứng | 99999 | t81 | 0 |
| 3.12 | head B313/H313 tương ứng | that | r766 | 0 |
| 3.12 | head B313/H313 tương ứng | 1 | r766 | 0 |
| 3.12 | head B313/H313 tương ứng | 10 | r766 | 0 |
| 3.12 | head B313/H313 tương ứng | 11 | r766 | 0 |
| 3.12 | head B313/H313 tương ứng | 12 | r766 | 0 |
| 3.12 | head B313/H313 tương ứng | 13 | r766 | 0 |
| 3.12 | head B313/H313 tương ứng | 14 | r766 | 0 |
| 3.12 | head B313/H313 tương ứng | 15 | r766 | 0 |
| 3.12 | head B313/H313 tương ứng | 99999 | r766 | 0 |
| 3.13 | base B313/H313 tương ứng | that | t81 | 0 |
| 3.13 | base B313/H313 tương ứng | 1 | t81 | 0 |
| 3.13 | base B313/H313 tương ứng | 10 | t81 | 1 |
| 3.13 | base B313/H313 tương ứng | 11 | t81 | 1 |
| 3.13 | base B313/H313 tương ứng | 12 | t81 | 1 |
| 3.13 | base B313/H313 tương ứng | 13 | t81 | 0 |
| 3.13 | base B313/H313 tương ứng | 14 | t81 | 0 |
| 3.13 | base B313/H313 tương ứng | 15 | t81 | 0 |
| 3.13 | base B313/H313 tương ứng | 99999 | t81 | 0 |
| 3.13 | head B313/H313 tương ứng | that | t81 | 0 |
| 3.13 | head B313/H313 tương ứng | 1 | t81 | 0 |
| 3.13 | head B313/H313 tương ứng | 10 | t81 | 0 |
| 3.13 | head B313/H313 tương ứng | 11 | t81 | 0 |
| 3.13 | head B313/H313 tương ứng | 12 | t81 | 0 |
| 3.13 | head B313/H313 tương ứng | 13 | t81 | 0 |
| 3.13 | head B313/H313 tương ứng | 14 | t81 | 0 |
| 3.13 | head B313/H313 tương ứng | 15 | t81 | 0 |
| 3.13 | head B313/H313 tương ứng | 99999 | t81 | 0 |
| 3.13 | head B313/H313 tương ứng | that | r766 | 0 |
| 3.13 | head B313/H313 tương ứng | 1 | r766 | 0 |
| 3.13 | head B313/H313 tương ứng | 10 | r766 | 0 |
| 3.13 | head B313/H313 tương ứng | 11 | r766 | 0 |
| 3.13 | head B313/H313 tương ứng | 12 | r766 | 0 |
| 3.13 | head B313/H313 tương ứng | 13 | r766 | 0 |
| 3.13 | head B313/H313 tương ứng | 14 | r766 | 0 |
| 3.13 | head B313/H313 tương ứng | 15 | r766 | 0 |
| 3.13 | head B313/H313 tương ứng | 99999 | r766 | 0 |

Mỗi dòng dùng đúng argv sau (thay các giá trị trong dòng; JSON lưu argv cụ thể, không có placeholder):

```sh
python<Python> -B $OUT/ep_pid.py <PID> --lap-ca <tên đầy đủ của t81 hoặc r766> --lan 1
```

</details>
