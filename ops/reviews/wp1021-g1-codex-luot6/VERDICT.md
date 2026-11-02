Verdict: request_changes
Reviewed commit: 691cb65388e71afb825aeba3b5cbc5359fc4dac5
Spec sha256: d5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d

Còn **1 finding P3** trong chú thích mới: khẳng định cả hai đột biến từng sống qua toàn suite không đúng với citation_drop_next. Vì ngưỡng yêu cầu hết mọi P0–P3, verdict là **request_changes**. P1 `bien-ngoai-cua-so-surface-chua-co-rang` lượt 5 **ĐÃ VÁ THẬT**: ba phản chứng cũ đều chết tại c88; no_clamp chết qua toàn suite. Head sạch đạt **98/98 · 153/153 · 2/2, TỔNG: ĐẠT**. F1/F2/F3 và phần giải xung đột #1037 không có hồi quy trong các phép đo dưới đây. Windows CI/local và Ubuntu CI exact head: **KHÔNG ĐO ĐƯỢC**. Verdict này không cấp quyền merge/land.

## Neo và cách tái hiện

Các lệnh Python dưới đây chạy từ gốc sandbox, với `PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null`; `measure.run` truyền cùng môi trường cho tiến trình con, thêm UTF-8 và lưu command/cwd/rc/thời gian/stdout/stderr. Các suite chạy lệnh `python3 ops/bien_nhan_v2_test.py` trong cây được ghi ở log. Mọi đột biến reviewer chạy trên cây đủ, mỗi đột biến một tiến trình, có đối chứng khi mutant còn hiệu lực và kiểm băm nguồn trước/sau. Không sửa nguồn trong `cay-kho`.

`python3 preflight.py` rc=0 ([log](evidence/preflight.json)): HEAD và cha đúng chỉ thị, tree `2bfc4623ba0ac56cee9a1766f1bee3ee2faa3a0e`; origin/master = `b29da0bfe3bfb7a7be69136a1c5c40f82c088a93`; không nông, `.git` là thư mục, core.abbrev=7, trạng thái sạch. SPEC khớp băm dòng 3; HINT khớp `994c283d58086efc070a51c6347aca928edae847da153e95cd10f73600340fa9`. DIFF.patch và DIFF-LUOT6.patch khớp byte với git diff tương ứng.

`git -C cay-kho diff --name-only b29da0b..HEAD` chỉ có `ops/bien_nhan_v2.py` và `ops/bien_nhan_v2_test.py`. `git diff --numstat b29da0b..HEAD`: **40/5** và **296/2** (thêm/xóa). `git diff --check b29da0b..HEAD` và `git diff --check` đều rc=0/không output; lệnh và kết quả lưu trong preflight.json.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Không dùng lời khai executor hay verdict cũ làm bằng chứng pass. `python3 run_mutants_l6.py`, `run_old_findings.py`, `run_focused_l6.py`, và `summarize_l6.py` đều hoàn tất rc=0; script cuối kiểm các kết quả con bằng assertion ([bảng máy](evidence/review-summary.json)).

| Lớp/biểu hiện | Phép đo trên head mới | Kết luận |
|---|---|---|
| P1, đầu tệp: no_clamp | `mutation_probe.py no_clamp --suite`: wrapper rc=0; suite con **rc=1**, 97/98 · 153/153 · 2/2, TỔNG: ĐỎ. Chỉ c88 `giet_that`, hàng ix đòi rc=1 được 0; c18 sạch, băm ổn định. | ĐÃ VÁ THẬT |
| P1, đầu tệp: skip_first | `mutation_probe.py skip_first`: c88 `giet_that`, hàng v đòi 1 được 0; c18 sạch. Oracle 63/71 xác nhận hành vi mutant sai. | ĐÃ VÁ THẬT |
| P1, citation dòng sau | `mutation_probe.py citation_drop_next`: c88 `giet_that`, hàng ii-b đòi 0 được 1, đúng L-SURFACE; c18 sạch. Oracle 65/71. | ĐÃ VÁ THẬT |
| F1/P2, lỗi liệt kê thoát traceback | `review_new.py error-child head <kiem\|sinh> <stat-os\|access\|late>`: 6 tiến trình có hit, rc=2, không traceback; iterator yield rồi lỗi cũng được bắt. m147 bị c99 giết thật. | Vẫn đóng |
| F2/P3, chốt ngoại lệ lập trình | `boundary_oracle.py head`: hai đường truyền đúng đối tượng RuntimeError, hit=1, restored=true; RuntimeError/ValueError qua CLI: rc=1, traceback. Focused m152/m153 bị c100 giết thật. | Vẫn đóng |
| F3/P3, OSError ngoài PermissionError | `errno_probe.py head <mode> <site> <EIO\|ESTALE>`: **12/12** có đúng 1 hit, rc=2, không traceback. Tracer c99/c100 thấy OSError thuần errno=5; m154/m155 bị c100/c99 giết thật, c18 sạch. | Vẫn đóng |

Log P1: [suite no_clamp](evidence/mut-no_clamp-suite.stdout), [rc/thời gian](evidence/mut-no_clamp-suite.json), [băm/đối chứng](evidence/mut-no_clamp-result.json), `evidence/wm-{no_clamp,skip_first,citation_drop_next}-result.json`. Log F1/F2/F3: `evidence/old-*`, `errno-*`, `boundary-head.*`, `trace-*`, `wm-m147*`, `wm-m154*`, `wm-m155*`, `focused-*`. Không tính lỗi giàn giáo hay ngoại lệ lập trình thành tín dụng giết.

**Giới hạn lịch sử được làm rõ:** lượt 5 chỉ có bằng chứng toàn suite cho no_clamp; citation_drop_next khi ấy chỉ chạy toàn bộ 98 ca thường. Để kiểm câu chú thích mới “hai đột biến từng sống qua toàn suite”, lượt 6 chạy thêm `python3 historical_citation_suite.py` trên **3883b60** mang citation_drop_next: wrapper rc=0; suite con **rc=1, 98/98 · 150/151 · 2/2, TỔNG: ĐỎ**, băm mutant ổn định ([log](evidence/historical-citation-suite.stdout), [neo](evidence/historical-citation-integrity.json)). m85 báo **KHÔNG RĂNG / gian_giao**, mẫu ` or any(_RE_TRICH_DAN.search(x) for x in cua)` khớp 0 chỗ. Vì vậy citation_drop_next sống qua ca thường, nhưng không phải survivor của **toàn suite xanh**. Đây là lỗi giàn giáo m85, không phải bộ ca cũ bắt được hành vi citation; cũng không được đổi lỗi giàn giáo thành bằng chứng full-suite survivor. Phép đo bổ sung của lượt 6 không được gán ngược thành phép đo đã có ở lượt 5. Chú thích mới sai ở phạm vi bằng chứng này (P3 bên dưới).

## C88 CỬA SỔ M4

`python3 window_probe.py head --gate` qua measure.run: **rc=0**, `SUMMARY {"total":71,"direct_pass":71,"gate_pass":71,"failed":[]}` ([log](evidence/window-head.stdout)). Ma trận độc lập gồm khoảng cách −3…+3, đầu/cuối tệp, một/hai/ba dòng, dòng trắng/tab và nhiều khai báo. Chưa thấy sai hành vi sản phẩm trong tập này.

`python3 c88_rows.py` rc=0: **10/10 hàng đúng, 10/10 phản chứng đảo rc, 10/10 giữ cùng rc khi thử lại tiền tố cũ** ([chi tiết](evidence/c88-rows.json)). Mỗi hàng được đo trực tiếp và qua kho git thật; rc=1 chỉ có L-SURFACE, rc=0 không lỗi/không chua_do. Bỏ tiền tố không làm hàng cũ xanh tình cờ vì lỗi khác:

| Hàng | j (từ 0) | Điều kiện thực sự được đo | rc head → khi đổi riêng điều kiện |
|---|---:|---|---|
| i | 1 | provider dòng trước | 1 → 0 khi bỏ provider |
| ii | 1 | citation dòng trước | 0 → 1 khi bỏ citation |
| ii-b (mới) | 0 | citation dòng sau | 0 → 1 khi bỏ citation |
| iii | 0 | không provider | 0 → 1 khi thêm provider cùng dòng |
| iv | 1 | notprovider không khớp cả từ | 0 → 1 khi đổi thành provider |
| v | 0 | provider dòng sau | 1 → 0 khi bỏ provider |
| vi | 2 | provider trước hai dòng ở ngoài cửa sổ | 0 → 1 khi kéo về cách một dòng |
| vii | 0 | provider sau hai dòng ở ngoài cửa sổ | 0 → 1 khi kéo về cách một dòng |
| viii | 2 | citation trước hai dòng không miễn | 1 → 0 khi kéo về cách một dòng |
| ix | 0 | citation sau hai dòng không miễn | 1 → 0 khi kéo về cách một dòng |

`run_mutants_l6.py` chạy lại nguyên **40 cặp đột biến** lượt 5. Tất cả đối chứng c18 sạch, băm nguồn ổn định; [bảng đầy đủ](evidence/review-summary.json):

| Nhóm | Số | Kết quả |
|---|---:|---|
| 24 cặp cận trái/phải khác cửa sổ đúng | 24 | c88 giet_that |
| Mọi dòng trước/sau/toàn tệp, loại dòng trắng, bỏ dòng khai ở EOF | 5 | c88 giet_that |
| Nới riêng provider hoặc citation ra trước/sau hai dòng | 4 | c88 giet_that |
| Bỏ provider cùng dòng, bỏ citation dòng trước | 2 | c88 giet_that |
| no_clamp, skip_first, citation_drop_next | 3 | c88 giet_that |
| citation_drop_self | 1 | SỐNG tại c88, **c79 giet_that**; không phải lỗ hổng của cả bộ ca |
| reverse_equivalent | 1 | SỐNG, oracle 71/71; tương đương vì đảo thứ tự không đổi hai phép any |

Tổng: **38 bị c88 giết + 1 bị c79 giết + 1 tương đương**. Tập hữu hạn này không được tuyên bố là vét cạn mọi biểu thức hay mọi nội dung verdict.

## Đột biến mới của reviewer

`python3 new_probe_l6.py <tên>` qua run_mutants_l6, mỗi tên một tiến trình; cả **14 phép** hoàn tất rc=0, đối chứng sạch, băm ổn định. Patch và dữ liệu: `evidence/new-*.patch/.json`, lệnh/rc: `newrun-*.json`.

| Phần thử | Số | Kết quả và lý do survivor |
|---|---:|---|
| Chỉ số âm cuộn về EOF; clamp ở 1; đòi đủ ba dòng; bỏ citation cuối vô điều kiện; chỉ citation dòng sau/cùng dòng; bỏ provider dòng sau; chỉ provider cùng dòng | 8 | Đều c88 giet_that; oracle chỉ 56–69/71 |
| Chặn cận phải bằng min(len, j+2); loại dòng trùng trong cửa sổ | 2 | **SỐNG, tương đương**; ba ca qua, oracle 71/71. Slice vốn tự chặn cận phải; loại bản sao không đổi any |
| Khôi phục tiền tố cũ; thêm một dòng trắng trước fixture | 2 | c88 riêng vẫn qua, nhưng **m156 KHÔNG RĂNG**, m157 vẫn giet_that |
| Bỏ hàng ii-b; đổi ii-b thành citation dòng trước | 2 | c88 riêng vẫn qua, nhưng **m157 KHÔNG RĂNG**, m156 vẫn giet_that |

Bốn phép cuối là đột biến vào test: sống qua ca thường nhưng bị bảng đột biến bắt. Không gán kết quả focused đó thành kết quả toàn suite.

## Giải xung đột và áp HINT

`python3 audit_l6.py` **rc=0**, `AUDIT ASSERTIONS PASS` ([JSON](evidence/merge-audit-l6.json)):

- Merge-base e9e0048/b29da0b là `757bde561d09738858506aecf5de2f050a5f0d5e`. `git merge-file -p` phát đúng **một** conflict; giữ cả hai thân + chuẩn hóa tên ca/đích m142/docstring c99 cho kết quả **khớp byte 3883b60**.
- Áp nguyên HINT bằng `patch -p1` lên blob test của 3883b60: rc=0. So head chỉ còn docstring/chú thích; AST thực thi giống nhau ([delta](evidence/hint-vs-head.patch)). Sản phẩm nguyên byte qua e9e0048/3883b60/head.
- Ca/đăng ký đột biến: e9e0048 **97/153**, b29da0b **95/139**, 3883b60 **98/153**, head **98/155**. Không mất hàm/đăng ký từ hai cha, không trùng tên/số ca, tên c98_chon_bien_nhan cũ không còn. 155 ở head gồm 153 thường và 2 tự kiểm, được suite xác nhận.

`python3 run_focused_l6.py` **rc=0**: m140–m157 chạy riêng **18/18**, mỗi log có đúng một hàng `giet_that` và `ASSERTIONS PASS`; m156/m157 đích c88, có đối chứng. Bốn lượt tiêm AttributeError vào ca đích m142/m147/m154/m155 đều **KHÔNG RĂNG**, `tin_dung_gia`, có tên ngoại lệ và vị trí ném (`focused_merge.py ... in reviewer_throw`). Dây báo lỗi #1037 còn hoạt động ([log driver](evidence/run-focused-l6.stdout)).

## Bảng tiêu chí

| Tiêu chí | Kết quả | Lệnh / output quyết định |
|---|---|---|
| Neo/phạm vi | ĐẠT | preflight.py; exact head/spec/tree, hai tệp, diff-check rc=0 |
| C1a | ĐẠT phần đã đo; Windows KHÔNG ĐO ĐƯỢC | probe.py head behaviors: hai YAML hợp lệ sai schema rc=1/tổng 2/nêu x; chỉ x rc=1/tổng 1/không báo rỗng; m142 so đuôi chính xác bị c101 giết thật |
| C1b | ĐẠT phần đã đo; Windows KHÔNG ĐO ĐƯỢC | Cùng driver: YAML hỏng đuôi hoa rc=2, stderr nêu x.RECEIPT.YAML, không Traceback; m142 chết c101 |
| C2 | ĐẠT phần đã đo; Windows KHÔNG ĐO ĐƯỢC | c89 qua trong suite; mutation_probe.py m143 thêm is_file → c89 giet_that, c18 sạch |
| C3 | ĐẠT | mutation_probe.py glob: c101/c99 giet_that, c18 sạch. c100 gian_giao vì không gọi iterdir, KHÔNG tính làm tín dụng |
| C4 Windows CI | KHÔNG ĐO ĐƯỢC | Không có đo độc lập jobs/labels/runner/log trên exact head |
| C5 Ubuntu CI | KHÔNG ĐO ĐƯỢC | Suite trong sandbox không chứng minh job CI exact head |
| C6 | ĐẠT | head/base chạy python3 ops/bien_nhan_v2.py --root .: rc=0, tổng 306, TỔNG: ĐẠT; os.listdir đếm riêng casefold=306/exact=306 |
| C7 Windows local | KHÔNG ĐO ĐƯỢC | Không chạy Windows local; không suy pass từ lời khai executor |
| C8 nội dung review | KHÔNG ĐẠT | Còn 1 P3 ở chú thích mới; request_changes neo exact head. Không xác nhận các điều kiện CI/land chưa đo; trần lượt 6 theo chỉ thị hiện hành |
| C9 | ĐẠT | Ruff F head/base cùng một F541 cùng nội dung dòng: **đỏ sẵn, delta=0**; doctrine rc=0, 10 tệp/0 chỗ; diff-check rc=0; rg glob rc=1/0 dòng; numstat 40/5 và 296/2 |
| Toàn suite head | ĐẠT | head-suite-final: rc=0, 372.70s, **98/98 · 153/153 · 2/2**, TỔNG: ĐẠT; stderr rỗng |
| C88/M4 | ĐẠT tập đã đo | 71/71 trực tiếp và git thật; 40 mutant phân loại đủ; no_clamp chết qua toàn suite |

Log C1: `evidence/head-behaviors.*`, `fixture-head-{c1a,only-x,c1b}.*`. C6/C9: `head-gate.*`, `base-gate.*`, `receipt-count.*`, `head-ruff.*`, `base-ruff.*`, `ruff-delta.json`, `head-doctrine.*`, `base-doctrine.*`, `no-glob.*`. Lệnh Ruff là `python3 -m ruff check --no-cache --select F --output-format json ops/bien_nhan_v2.py ops/bien_nhan_v2_test.py`; doctrine là `python3 .claude/dev/packet_loop.py doctrine-scan --root .`. Không gọi Ruff sạch tuyệt đối. C9 vế âm dùng `rg -n 'glob\("\*\.receipt\.yaml"\)' ops/bien_nhan_v2.py`; vế dương là C1a/C1b ở trên.

## Bảng finding

**Finding mở: 1. Tổng P0=0, P1=0, P2=0, P3=1.**

- [P3] chu-thich-nang-ca-thuong-thanh-toan-suite: `ops/bien_nhan_v2_test.py:4760` — `python3 historical_citation_suite.py` — suite con rc=1, 98/98 · 150/151 · 2/2, TỔNG: ĐỎ; m85 gian_giao do mẫu khớp 0 chỗ — sửa chú thích để tách no_clamp (từng sống qua toàn suite) với citation_drop_next (từng qua đủ 98 ca thường). Đây là lỗi mô tả bằng chứng mới được thêm ngoài HINT, không phải lỗi runtime hay mở lại P1.

  HÌNH DẠNG: `khac`.

  **Hướng vá cụ thể:** [HINT-LUOT6.patch](HINT-LUOT6.patch) thay đúng một dòng chú thích bằng: `# #1021 Codex lượt 5: no_clamp từng SỐNG qua toàn suite; citation_drop_next từng qua đủ 98 ca thường.` `python3 comment_hint_l6.py` rc=0: git apply --check và git diff --check đều rc=0; AST thực thi không đổi, bản sao đã phục hồi ([bằng chứng](evidence/comment-hint.json)). Patch chỉ được thử trong sandbox, chưa áp vào checkout được review.

  **Cách kiểm và rủi ro vá:** không thêm test runtime cho một chú thích; đối chiếu N/N/cờ gian_giao với log lịch sử và kiểm patch/AST như trên. Giữ nguyên các ca và m156/m157 đã xanh. Chỉ sửa chữ thì không đổi hành vi; tránh chạm mẫu neo, target hoặc đăng ký đột biến khi áp.

- [P1 — ĐÃ ĐÓNG] bien-ngoai-cua-so-surface-chua-co-rang: `ops/bien_nhan_v2_test.py:2981`, hàng ii-b tại `:2994`, bỏ prefix tại `:3005`, đăng ký tại `:4761`/`:4765` — `mutation_probe.py no_clamp --suite`, `skip_first`, `citation_drop_next` — c88 giet_that; no_clamp toàn suite rc=1/97 trên 98 ca, chỉ c88 đỏ — hướng vá lượt 5 đã được áp và kiểm: fixture chạm j=0, citation ngay sau, m156/m157 khóa hai chốt. Không yêu cầu vá thêm.

  HÌNH DẠNG: `bo-chon-ung-vien` (lớp lịch sử đã đóng).

F1/F2/F3 lịch sử có hình dạng `loi-do`, vẫn đóng theo bảng đối chiếu. P3 mới chỉ là câu mô tả sai phạm vi bằng chứng; không tạo finding runtime cho lỗi giàn giáo m85, mutant tương đương, ENOSPC hay phần nền không đo được.

## Toàn vẹn và giới hạn bằng chứng

`python3 summarize_l6.py` rc=0: `PASS: 40 windows (38 c88, 1 c79, 1 equivalent); 6 selector mutations; 18 focused real + 4 fake; F1/F2/F3; C1/C6/C9; 14 new probes`.

`python3 validate_l6_final.py` rc=0: `FINAL ASSERTIONS PASS: 4 clean full trees; exact head/spec/hint; all suite counts; no_clamp killed by c88; historical citation NOT a full-suite survivor` ([snapshot](evidence/final-validation.json)). `cay-kho`, `work/head`, `work/mutation`, `work/focus` về exact head/tree dòng đầu, tracked/untracked/ignored sạch, worktree/index diff rỗng; hai tệp nguồn khớp blob HEAD; .git là thư mục, không nông, core.abbrev=7. Snapshot cuối không được dùng để tuyên bố toàn bộ lịch sử ghi trong lúc chạy.

Script kế thừa được chép ra gốc sandbox để ROOT neo đúng. Chỉ `mutation_probe.py` được chỉnh để nhận `REVIEW_MUTATION_TREE`/`REVIEW_MUTATION_PREFIX`, giữ nguyên byte toàn bộ 40 định nghĩa đột biến và oracle; dùng `run_mutants_l6.py` thay driver sao chép cũ. `audit_l6.py` tái dựng merge tại 3883b60 rồi áp HINT trước khi so head. Không chạy `hint_probe.py create` vì hint đã áp. Các script nguyên bản trong luot5-probe không sửa. `work/focus` là clone local đủ cây, object git bất biến hardlink theo clone local; nguồn có bản riêng. Đã ghim origin/master và origin/HEAD về b29da0b cho bản clone này.

Sự cố hạ tầng được giữ riêng: lần sao work/focus đầu và audit scratch gặp ENOSPC; suite head đầu ra 97/98 do **c42 OSError ENOSPC**; suite no_clamp đầu bị cắt ngang/log dở. Các log `infra-initial-*` không được tính làm kết quả sản phẩm. Đã bỏ bản sao dở và bản base sau khi lưu C6/C9; suite head và no_clamp chạy lại đầy đủ, cho kết quả dùng ở trên. Bằng chứng tăng dần trước bản tổng hợp được giữ tại `evidence/VERDICT-progress.md`.

Windows CI/local, Ubuntu CI exact head: **KHÔNG ĐO ĐƯỢC**. Không cấp quyền merge/land.
