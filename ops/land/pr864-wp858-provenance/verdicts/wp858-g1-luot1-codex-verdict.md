verdict: changes_requested
reviewed_head: bfbd2732a0e5359cbeb2a4d5336fc3dc7d2a7121
reviewed_sha: bfbd2732a0e5359cbeb2a4d5336fc3dc7d2a7121
reviewed_tree: 454f7c3fcc024938c048271ffe8c10c38ce34eba
review_class: sensitive
provider: openai_codex
model: gpt-6.1-sol
model_family: openai
reasoning_effort: xhigh
execution_surface: codex_cli
transport: machine
review_run: b229621980404e3f8cf35c5807dd2bed

# Kết luận

Yêu cầu sửa 3 finding P2 dưới đây. N4 nguyên bản và L3 đã có bằng chứng nền/head; bản vá vẫn còn lỗ hổng ở hợp đồng stdout của N4, xử lý lỗi ghi PATH cho bước CI sau, và độ phủ Windows. Không có P0/P1 được phát hiện trong phạm vi đã đo. Chưa đủ điều kiện approve lớp sensitive vì chưa có quyết định chủ kho cho các finding này.

HEAD và băm spec đúng assignment. Nền thực tế `git merge-base HEAD origin/master` là `637f78029f5a5fe56d35199dd0f75c50274f2c0f`; master là ancestor của HEAD. Nền lease `3a3a3caca5de4934ff53851feb6994c2c7b84ad5` không bị dùng thay nền thực tế. Spec từ `origin/ops/wp858-spec:ops/specs/wp858.md` có SHA-256 `5a61e959281f852592b2a5420b4618718d2364db8fa6320934d2651bbb7d4c54`. Lease r1/g1 khai 7 đường dẫn; diff PR có 6 tệp, 353 dòng thêm/28 dòng xoá, nằm trong write set và trần 450.

Danh tính thực thi lấy từ [header của chính run](evidence/model-header.txt) và `runs/b2296219/run.json`; không suy từ actor GitHub. Cây `kho/` chỉ được đọc; chạy mã trên bản sao `out/head/`, phản chứng và mọi đột biến dưới `out/`, với `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR=<out>/tmp`. Không push, không gọi GitHub. `PIP_NO_INDEX=1` được đặt để các ca cần tải dependency không gọi mạng; các ca bỏ qua được khai riêng.

# Finding

| ID | Mức | Tệp:dòng | Phép đo tái hiện → kết quả thật | Đề xuất vá |
|---|---|---|---|---|
| F858-01 | P2 | `ops/cai_cong_cu.sh:53` | `python out/edges.py` → dòng `fail-w`: stub `cygpath -w` thoát 37, installer vẫn **rc=0**, checker `DAT`, `$GITHUB_PATH` rỗng. Dòng `bad-github-path`: đích ghi là thư mục → lỗi `Is a directory`, installer vẫn **rc=0/DAT**. `python out/edges.py followup` cho cùng hiện tượng trên Linux. Đối chứng `fail-w-direct` chạy công thức bằng `eval` trực tiếp → **rc=37**, khác đường installer thật. [Log](evidence/edges.log), [Linux](evidence/edges-followup.log). | Kiểm mã thoát của phép chuyển đổi và phép ghi, trả lỗi tường minh trước khi in thư mục đã chọn. Thêm ca âm qua **installer thật** cho cả Linux/Windows; chỉ chạy `eval` trực tiếp không bắt được việc `errexit` bị tắt trong command substitution. |
| F858-02 | P2 | `.claude/dev/launcher_test.py:8476`, `:8479`, `:8631`; `ops/cai_cong_cu.sh:47`, `:48` | `python out/mutate.py guards` → bỏ `cygpath -u` vẫn **11/11 ca đích qua**, không `TinHieuChotCa`; bỏ `-f` tên thường hoặc bỏ cả nhánh `.exe` cũng sống. Phép độc lập `bo_exe` cũng **11/11 qua**. Stub hiện trả nguyên đường POSIX và chỉ tạo tên không đuôi. `python out/edges.py followup` với ánh xạ `V:/Program Files/...` → head **rc=0/DAT**, bản bỏ `-u` **rc=1**, chứng minh đột biến chuyển đổi không tương đương. [Đột biến](mutants/bo_cygpath_u.json), [.exe](mutants/bo_exe.json), [đối chứng](evidence/edges-followup.log). | Dùng fixture mà đường Windows thực sự phải đổi mới tới ứng viên, thêm ca `.exe` và ca loại tệp/quyền phù hợp nền; đăng ký các mutant này và đòi `TinHieuChotCa` của ca đích. Với `-f` tên thường, xác định chốt có hợp đồng riêng hay tương đương do checker; không gọi nó là đã được kiểm khi chỉ thấy `-x` trong chuỗi. |
| F858-03 | P2 | `ops/cai_cong_cu.sh:44` (tương tác bộ đọc stdout ở `:115`) | `python out/edges.py installer-stdout` → cùng fixture N4, chỉ đổi stdout của stub apt-get lúc cài bash: im lặng **rc=0**, dòng chữ **rc=0**, dòng cuối là thư mục ban đầu có bash tốt/rg hỏng **rc=2**, tổng cuối **rg=DO, bash=DAT**. stderr vẫn nói `ten tran da DAT, giu nguyen PATH`. [Log](evidence/installer-stdout.log). | Bảo đảm nhánh tên trần DAT cung cấp tín hiệu cuối rõ ràng để caller không nhận dòng log installer làm thư mục chọn. Có thể dùng sentinel không phải thư mục trong hợp đồng hiện tại hoặc tách kênh kết quả; thêm biến thể N4 có stdout installer là thư mục. Giữ Q3 và xin mở write set nếu phải sửa ngoài hàm. |

F858-01: checker cuối chỉ chứng minh PATH của **tiến trình hiện tại** đã dùng được. Khi phép ghi thất bại, bước CI tiếp theo chưa nhận đường dẫn ấy. Bash thường xoá `errexit` trong `$(eval ...)`, nên `echo "$dich"` sau lệnh thất bại làm hàm quay về 0; `set -euo pipefail` ở đầu tệp không tự bảo vệ hậu điều này. Hai lỗi chuyển đổi/ghi là hai biểu hiện của cùng một lớp.

F858-02 là finding về độ phủ theo yêu cầu assignment. Chưa chứng minh lỗi runtime ở **head nguyên vẹn** đối với chuyển đổi hoặc `.exe`; bằng chứng là các hồi quy quan trọng sống qua mọi ca đích đã chỉ định. Đột biến chỉ bỏ `-f` tên thường có thể tương đương trong một số môi trường vì checker kiểm lại; không suy từ survivor đó thành lỗ an ninh. Hai mutant `bo_f_ca_hai` và `bo_exe` chồng phạm vi, không được tính thành hai lỗi độc lập.

F858-03 là phản chứng hợp đồng stdout bằng installer stub được kiểm soát. Chưa đo rằng apt-get/brew/choco thật in chính dòng thư mục đó. Tuy nhiên nhánh “không in gì” hiện không bảo đảm lời khai giữ nguyên PATH khi stdout installer còn dữ liệu; fixture im lặng đang che trường hợp này.

| Lớp nguyên nhân | Findings / biểu hiện | Mức cao nhất | Cách kiểm đóng lớp |
|---|---|---|---|
| `loi-ghi-path-bi-nuot-trong-command-substitution` | F858-01: lỗi `cygpath -w`, lỗi ghi tệp trên Windows và Linux | P2 | Các lỗi đó qua installer thật đều khác 0; phép dương vẫn DAT và ghi đúng PATH. |
| `fixture-windows-khong-phan-biet-chuyen-doi-va-duoi-exe` | F858-02: `-u`, `.exe`, kiểm loại tệp | P2 | Mutant không tương đương bị đúng ca đích giết bằng `TinHieuChotCa`; làm rõ trường hợp tương đương. |
| `stdout-installer-bi-nhan-lam-ket-qua-chon` | F858-03: N4 với log installer là thư mục có rg hỏng | P2 | Cả ba đối chứng stdout giữ rg/bash DAT; không đẩy thư mục log lên đầu PATH. |

3 lớp / 3 finding; lượt 1, không có finding lượt trước để đối chiếu. Không sinh patch mã sản phẩm.

# Đối chiếu lời khai executor

| Lời khai | Đã đo → kết luận có giới hạn |
|---|---|
| 1. N1–N3 | 7 ca `r858_*`, 2 ca `r831_*`, 2 ca `r802_*` được yêu cầu đều qua, không bỏ qua. git/shellcheck/bash × 3 nền mô phỏng qua cả chiều dương và âm; Python theo đúng phụ lục chủ kho, chỉ rc và không in thư mục hỏng. Chưa đo native Windows/macOS. |
| 2. N4 | Giữ test head, chỉ phục hồi YAML và shell của nền trong `out/n4-base/` → rc=1 của harness, child rc=2, `{'rg':'DO','bash':'DAT'}`. Head ca nguyên bản rc=0. F858-03 là biến thể mới chưa được đóng. |
| 3. N6 | Hai selftest tổng đầu đều `[OK] edit_skill_assert_count_gate_dry`, số ca 1731 không đổi; tổng 1729/1731 do Git signing. Tắt signing chỉ trong env con rồi chạy lại hai lượt song song: **1731/1731 cả hai**, rc=0. Script `l3_probe.py` chạy nguyên khối thực tế trong hai tiến trình, chỉ chèn lịch đồng bộ: nền 1/2 qua (một tiến trình xoá tệp chung trước tiến trình kia đọc); head 2/2 qua với hai thư mục riêng. |
| 4. Sàn Windows | Mô phỏng `LA_WINDOWS=True` cho 9 mutant wp858: 9/9 đo được và bị giết bởi ca thuần Python. Đây là kiểm đường shape/skip, **không** phải số đo native Windows hoặc bằng chứng sàn toàn bảng trên Windows. |
| 5. L2/t86 | **Không tái hiện** được lỗi đặc thù “chỉ đỏ khi hai suite song song”. Trong sandbox này t86 đã đỏ cả khi chạy riêng ở nền/head vì credential fixture nằm dưới ancestor có `.git`. Cặp 10 lượt song song đều 0/10 do cùng chốt môi trường; không suy thành race. Không xác nhận con số 15 lượt của executor. |
| 6. Toàn bảng đột biến | Một lượt trên head: **`DOT BIEN: 286/286 dat (4 khong do duoc tren nen nay)`**, rc=0. 9 mutant wp858 đều bị giết. Headline toàn bảng không chứng minh mọi kill hợp lệ: phần runner cũ còn ghi tín dụng cho OSError/AssertionError không phải `TinHieuChotCa` trong một số ca credential; chúng không được dùng làm bằng chứng đóng chốt mới. |

# Bảng lệnh → kết quả thật

Các lệnh trong bản sao có `cwd=out/head` trừ khi bảng nói khác. Từ thư mục gốc chạy `PYTHONDONTWRITEBYTECODE=1 python out/audit.py targeted`, `mutation`, `suites`, `baseline`, `gates` để thực hiện các nhóm tương ứng; [audit.py](audit.py) giữ argv, env và cách dựng bản sao. Mỗi log ghi cwd và argv thực tế, mỗi JSON cùng tên giữ rc/thời lượng. Chỉ rc không đủ để nhận pass: xem kết quả trong cột cuối.

## Preflight, ca sẵn có và gate

| Nhãn / scope | Lệnh thực tế | rc | Kết quả thật / log |
|---|---|---|---|
| actionlint (head) | `actionlint` | 0 | không có stdout/stderr · [log](evidence/actionlint.log) |
| actionlint-base (base-full) | `actionlint` | 0 | không có stdout/stderr · [log](evidence/actionlint-base.log) |
| base-checkout (base-full) | `git checkout --detach 637f78029f5a5fe56d35199dd0f75c50274f2c0f` | 0 | Previous HEAD position was bfbd273 wp858(#858): tai sinh RELEASE_MANIFEST.json (changelog.d/wp-858.md them) / HEAD is now at 637f780 Merge pull request #859 from ducthangho/claude/bookkeeping-744-land · [log](evidence/base-checkout.log) |
| base-suite-clean (base-full) | `/usr/bin/python .claude/dev/launcher_test.py --nhat-ky /tmp/claude-0/-home-user-tra-luat/8020da77-7294-54d3-ba3c-35424edfafe5/scratchpad/rv1/out/evidence/base-suite-clean.journal` | 1 | 214/226 ca DA CHAY QUA (tong 236, bo qua 10, hong 12) - KHONG DU: 10 ca BO QUA, chua do gi · [log](evidence/base-suite-clean.log) |
| bash-syntax (head) | `bash -n ops/cai_cong_cu.sh` | 0 | không có stdout/stderr · [log](evidence/bash-syntax.log) |
| doc-claims (head) | `/usr/bin/python scripts/tl.py doc-claims-check --strict --json` | 0 | { /   "ok": true, /   "schema": "doc_claims_check.v1", /   "roots": [ /     "CHANGELOG.md", /     "SKILL.md", /     "CLAUDE.md", /     "CONTEXT.md", /     "references", /     "docs" /   ], /   "files_scanned":  · [log](evidence/doc-claims.log) |
| doctrine (head) | `/usr/bin/python ops/doctrine_scan.py --root .` | 2 | /usr/bin/python: can't open file '/tmp/claude-0/-home-user-tra-luat/8020da77-7294-54d3-ba3c-35424edfafe5/scratchpad/rv1/out/head/ops/doctrine_scan.py': [Errno 2] No such file or directory · [log](evidence/doctrine.log) |
| doctrine-correct (head) | `/usr/bin/python scripts/tl.py doctrine-scan --root . --json` | 2 | usage: tl [-h] [--version] [--config CONFIG] [--profile PROFILE] [--timings] /           [--deterministic] [--selftest] /           {gws-ping,download,gws-bootstrap-cowork,drive-push,bootstrap,nlm-install,overl · [log](evidence/doctrine-correct.log) |
| doctrine-final (head) | `/usr/bin/python .claude/dev/packet_loop.py doctrine-scan --root .` | 0 | doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine · [log](evidence/doctrine-final.log) |
| git-base (head) | `git merge-base HEAD origin/master` | 0 | 637f78029f5a5fe56d35199dd0f75c50274f2c0f · [log](evidence/git-base.log) |
| git-diff-check (head) | `git diff --check origin/master HEAD` | 0 | không có stdout/stderr · [log](evidence/git-diff-check.log) |
| git-identity (head) | `git rev-parse HEAD 'HEAD^{tree}'` | 0 | bfbd2732a0e5359cbeb2a4d5336fc3dc7d2a7121 / 454f7c3fcc024938c048271ffe8c10c38ce34eba · [log](evidence/git-identity.log) |
| git-sign-config (head) | `git config --show-origin --get commit.gpgsign` | 0 | file:/root/.gitconfig	true · [log](evidence/git-sign-config.log) |
| git-status (head) | `git status --porcelain=v1 --untracked-files=all --ignored=matching` | 0 | !! .claude/.packet_state/ / !! references/golden/fixtures/ / !! scripts/.tl_state/ · [log](evidence/git-status.log) |
| golden (head) | `/usr/bin/python scripts/tl.py golden-test --json` | 0 | ok=True; 20 cases · [log](evidence/golden.log) |
| head-all-mutations (head) | `/usr/bin/python .claude/dev/launcher_test.py --dot-bien` | 0 | DOT BIEN: 286/286 dat  (4 khong do duoc tren nen nay) · [log](evidence/head-all-mutations.log) |
| head-suite-clean (head) | `/usr/bin/python .claude/dev/launcher_test.py --nhat-ky /tmp/claude-0/-home-user-tra-luat/8020da77-7294-54d3-ba3c-35424edfafe5/scratchpad/rv1/out/evidence/head-suite-clean.journal` | 1 | 221/233 ca DA CHAY QUA (tong 243, bo qua 10, hong 12) - KHONG DU: 10 ca BO QUA, chua do gi · [log](evidence/head-suite-clean.log) |
| head-suite-inert (head) | `CODEX_AUTH_JSON=<INERT-REVIEW-WP858> /usr/bin/python .claude/dev/launcher_test.py --nhat-ky /tmp/claude-0/-home-user-tra-luat/8020da77-7294-54d3-ba3c-35424edfafe5/scratchpad/rv1/out/evidence/head-suite-inert.journal` | 1 | 221/233 ca DA CHAY QUA (tong 243, bo qua 10, hong 12) - KHONG DU: 10 ca BO QUA, chua do gi · [log](evidence/head-suite-inert.log) |
| master-ancestor (head) | `git merge-base --is-ancestor origin/master HEAD` | 0 | không có stdout/stderr · [log](evidence/master-ancestor.log) |
| n4-base (n4-base) | `/usr/bin/python .claude/dev/launcher_test.py --lap-ca r858_bat_buoc_bash_khong_dua_rg_hong_len_dau --lan 1` | 1 | moi truong: pid=6 pgid=1 sid=1 truong_nhom=False chung_nhom_voi_cha=True job_control=? ns_pid=pid:[4026532542] init=codex / nhom tien trinh: da tach sang session moi (pgid=6) /   lan 1/1: HONG /   HONG r858_bat · [log](evidence/n4-base.log) |
| r802_bang_cai_rg_khop_cong_cu_yaml (head) | `/usr/bin/python .claude/dev/launcher_test.py --lap-ca r802_bang_cai_rg_khop_cong_cu_yaml --lan 1` | 0 | LAP r802_bang_cai_rg_khop_cong_cu_yaml: 1/1 qua, 0 bo qua, 0 hong · [log](evidence/r802_bang_cai_rg_khop_cong_cu_yaml.log) |
| r802_cai_rg_windows_chon_ban_chay_duoc (head) | `/usr/bin/python .claude/dev/launcher_test.py --lap-ca r802_cai_rg_windows_chon_ban_chay_duoc --lan 1` | 0 | LAP r802_cai_rg_windows_chon_ban_chay_duoc: 1/1 qua, 0 bo qua, 0 hong · [log](evidence/r802_cai_rg_windows_chon_ban_chay_duoc.log) |
| r831_cai_rg_linux_chon_ban_chay_duoc (head) | `/usr/bin/python .claude/dev/launcher_test.py --lap-ca r831_cai_rg_linux_chon_ban_chay_duoc --lan 1` | 0 | LAP r831_cai_rg_linux_chon_ban_chay_duoc: 1/1 qua, 0 bo qua, 0 hong · [log](evidence/r831_cai_rg_linux_chon_ban_chay_duoc.log) |
| r831_cai_rg_macos_chon_ban_chay_duoc (head) | `/usr/bin/python .claude/dev/launcher_test.py --lap-ca r831_cai_rg_macos_chon_ban_chay_duoc --lan 1` | 0 | LAP r831_cai_rg_macos_chon_ban_chay_duoc: 1/1 qua, 0 bo qua, 0 hong · [log](evidence/r831_cai_rg_macos_chon_ban_chay_duoc.log) |
| r858_bat_buoc_bash_khong_dua_rg_hong_len_dau (head) | `/usr/bin/python .claude/dev/launcher_test.py --lap-ca r858_bat_buoc_bash_khong_dua_rg_hong_len_dau --lan 1` | 0 | LAP r858_bat_buoc_bash_khong_dua_rg_hong_len_dau: 1/1 qua, 0 bo qua, 0 hong · [log](evidence/r858_bat_buoc_bash_khong_dua_rg_hong_len_dau.log) |
| r858_cai_linux_chon_ban_chay_duoc (head) | `/usr/bin/python .claude/dev/launcher_test.py --lap-ca r858_cai_linux_chon_ban_chay_duoc --lan 1` | 0 | LAP r858_cai_linux_chon_ban_chay_duoc: 1/1 qua, 0 bo qua, 0 hong · [log](evidence/r858_cai_linux_chon_ban_chay_duoc.log) |
| r858_cai_macos_chon_ban_chay_duoc (head) | `/usr/bin/python .claude/dev/launcher_test.py --lap-ca r858_cai_macos_chon_ban_chay_duoc --lan 1` | 0 | LAP r858_cai_macos_chon_ban_chay_duoc: 1/1 qua, 0 bo qua, 0 hong · [log](evidence/r858_cai_macos_chon_ban_chay_duoc.log) |
| r858_cai_python_khong_in_thu_muc_ban_hong (head) | `/usr/bin/python .claude/dev/launcher_test.py --lap-ca r858_cai_python_khong_in_thu_muc_ban_hong --lan 1` | 0 | LAP r858_cai_python_khong_in_thu_muc_ban_hong: 1/1 qua, 0 bo qua, 0 hong · [log](evidence/r858_cai_python_khong_in_thu_muc_ban_hong.log) |
| r858_cai_windows_chon_ban_chay_duoc (head) | `/usr/bin/python .claude/dev/launcher_test.py --lap-ca r858_cai_windows_chon_ban_chay_duoc --lan 1` | 0 | LAP r858_cai_windows_chon_ban_chay_duoc: 1/1 qua, 0 bo qua, 0 hong · [log](evidence/r858_cai_windows_chon_ban_chay_duoc.log) |
| r858_hinh_dang_cong_thuc_cai (head) | `/usr/bin/python .claude/dev/launcher_test.py --lap-ca r858_hinh_dang_cong_thuc_cai --lan 1` | 0 | LAP r858_hinh_dang_cong_thuc_cai: 1/1 qua, 0 bo qua, 0 hong · [log](evidence/r858_hinh_dang_cong_thuc_cai.log) |
| r858_selftest_editskill_thu_muc_rieng (head) | `/usr/bin/python .claude/dev/launcher_test.py --lap-ca r858_selftest_editskill_thu_muc_rieng --lan 1` | 0 | LAP r858_selftest_editskill_thu_muc_rieng: 1/1 qua, 0 bo qua, 0 hong · [log](evidence/r858_selftest_editskill_thu_muc_rieng.log) |
| release-verify (head) | `/usr/bin/python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | 0 | ok=true; expected_file_count=checked_file_count=190; failed=[] · [log](evidence/release-verify.log) |
| ruff-base (base-full) | `/usr/bin/python -m ruff check --no-cache --select F scripts/tl.py` | 1 | Found 12 errors (12 F821); delta head/base=0 · [log](evidence/ruff-base.log) |
| ruff-contract (head) | `/usr/bin/python -c 'import runpy,sys; m=runpy.run_path('"'"'.claude/dev/ci_dang_ky_test.py'"'"'); e,n=m['"'"'loi_ruff_ci'"'"'](); print('"'"'RUFF_CONTRACT'"'"',n,e); sys.exit(bool(e) or n==0)'` | 0 | RUFF_CONTRACT 3 [] · [log](evidence/ruff-contract.log) |
| ruff-head (head) | `/usr/bin/python -m ruff check --no-cache --select F scripts/tl.py` | 1 | Found 12 errors (12 F821); delta head/base=0 · [log](evidence/ruff-head.log) |
| ruff-version (head) | `/usr/bin/python -m ruff --version` | 0 | ruff 0.17.1 · [log](evidence/ruff-version.log) |
| runtime (head) | `/usr/bin/python -c 'import sys,platform,yaml;print(sys.version); print(platform.platform()); print('"'"'PyYAML'"'"',yaml.__version__)'` | 0 | 3.13.16 (main, Oct  1 2026, 15:40:24) [GCC 13.3.0] / Linux-6.18.44-fc-v140-x86_64-with-glibc2.39 / PyYAML 6.0.3 · [log](evidence/runtime.log) |
| selftest-a (head) | `/usr/bin/python scripts/tl.py --selftest` | 1 | == tl selftest 1729/1731 == · [log](evidence/selftest-a.log) |
| selftest-b (head) | `/usr/bin/python scripts/tl.py --selftest` | 1 | == tl selftest 1729/1731 == · [log](evidence/selftest-b.log) |
| selftest-unsigned-a (head) | `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false /usr/bin/python scripts/tl.py --selftest` | 0 | == tl selftest 1731/1731 == · [log](evidence/selftest-unsigned-a.log) |
| selftest-unsigned-b (head) | `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false /usr/bin/python scripts/tl.py --selftest` | 0 | == tl selftest 1731/1731 == · [log](evidence/selftest-unsigned-b.log) |
| t86-parallel-clean (head) | `/usr/bin/python .claude/dev/launcher_test.py --lap-ca t86_chuan_bi_nhan_ca_base64_lan_json_tho_va_tu_choi_rac --lan 10` | 1 | LAP t86_chuan_bi_nhan_ca_base64_lan_json_tho_va_tu_choi_rac: 0/10 qua, 0 bo qua, 10 hong · [log](evidence/t86-parallel-clean.log) |
| t86-parallel-inert (head) | `CODEX_AUTH_JSON=<INERT-REVIEW-WP858> /usr/bin/python .claude/dev/launcher_test.py --lap-ca t86_chuan_bi_nhan_ca_base64_lan_json_tho_va_tu_choi_rac --lan 10` | 1 | LAP t86_chuan_bi_nhan_ca_base64_lan_json_tho_va_tu_choi_rac: 0/10 qua, 0 bo qua, 10 hong · [log](evidence/t86-parallel-inert.log) |
| t86-solo-base (base-full) | `/usr/bin/python .claude/dev/launcher_test.py --lap-ca t86_chuan_bi_nhan_ca_base64_lan_json_tho_va_tu_choi_rac --lan 1` | 1 | LAP t86_chuan_bi_nhan_ca_base64_lan_json_tho_va_tu_choi_rac: 0/1 qua, 0 bo qua, 1 hong · [log](evidence/t86-solo-base.log) |
| t86-solo-head (head) | `/usr/bin/python .claude/dev/launcher_test.py --lap-ca t86_chuan_bi_nhan_ca_base64_lan_json_tho_va_tu_choi_rac --lan 1` | 1 | LAP t86_chuan_bi_nhan_ca_base64_lan_json_tho_va_tu_choi_rac: 0/1 qua, 0 bo qua, 1 hong · [log](evidence/t86-solo-head.log) |
| tools-gate (head) | `CONG_CU_TEST_BAN_KINH=manh /usr/bin/python ops/cong_cu_test.py` | 0 | cong_cu_test: 60/60 đạt; tổng=61, bỏ qua=1, tiền kiểm bỏ qua=0 / SỐ LIỆU: ca=61 · đột biến=470 (giao mảnh) · lỗi đột biến=0 · tiền kiểm bỏ qua=0 · cổng cây thật=ĐẠT · [log](evidence/tools-gate.log) |

`ops/cong_cu_test.py` mặc định đã được chạy nhưng bị reviewer ngắt sau khi sang vòng bán kính 470 mutant (wrapper rc=130, rc con cuối không đo được); không khai vòng đó là pass. Chạy lại chế độ gate được kho hỗ trợ (`CONG_CU_TEST_BAN_KINH=manh`), khai riêng kết quả và việc chuyển bán kính cho shard. Đây không thay lượt `launcher_test.py --dot-bien` bắt buộc, vốn đã chạy trọn một lần. [Log lượt ngắt](evidence/tools-suite.log), [biên nhận](evidence/tools-suite-interrupted.json).

Hai lệnh dò sai entry point doctrine cũng được giữ trong bảng: tệp `ops/doctrine_scan.py` không tồn tại và `tl.py` không có subcommand đó, đều rc=2. Lệnh đúng `.claude/dev/packet_loop.py doctrine-scan --root .` mới là phép nghiệm thu rc=0. Không biến lỗi thao tác đó thành finding sản phẩm.

Suite tổng: head sạch và head có `CODEX_AUTH_JSON` giả đều 221/233 đã chạy qua (243 tổng, 10 bỏ qua, 12 hỏng); nền sạch 214/226 (236 tổng, 10 bỏ qua, 12 hỏng). Tập 12 ca hỏng **giống nhau**, delta ca hỏng mới=0, 7 ca head thêm đều qua. Những ca hỏng credential do TMPDIR dưới cây Git được ghi trong journal. Không gọi suite là N/N. Các lượt tổng này không phải phép A/B dựng và chạy trong cùng một lệnh như cổng spec yêu cầu; đối chiếu là từ ba log cùng môi trường, hạn chế được khai ở mục cuối.

## Đột biến độc lập từng chốt

Lệnh nhóm: `PYTHONDONTWRITEBYTECODE=1 python out/mutate.py guards`; phép `.exe` riêng gọi `mutate.once('bo_exe', ...)` qua Python, cùng runner. Mỗi bản nằm trong `out/mutants/`. Mỗi hàng chạy đúng 11 ca nêu trên, kể cả shape và N6; **chỉ** `TinHieuChotCa` mới tính giết. Chi tiết cặp neo/thay và fixture có trong [mutate.py](mutate.py) và bản `.sh` tương ứng. Riêng `bo_f_ca_hai` bỏ `-f` tên thường **và** bỏ nhánh `.exe`, không phải chỉ thay một biểu thức bằng true.

| Mutant | Ca giết bằng TinHieuChotCa / 11 | Kết quả |
|---|---|---|
| `bo_checker` | 4/11: `r858_cai_linux_chon_ban_chay_duoc`, `r858_cai_macos_chon_ban_chay_duoc`, `r858_cai_windows_chon_ban_chay_duoc`, `r858_hinh_dang_cong_thuc_cai` | GIẾT; lỗi giàn giáo=0 · [chi tiết](mutants/bo_checker.json) |
| `bo_cygpath_u` | 0/11: không có | **SỐNG**; lỗi giàn giáo=0 · [chi tiết](mutants/bo_cygpath_u.json) |
| `bo_cygpath_w` | 2/11: `r858_cai_windows_chon_ban_chay_duoc`, `r858_hinh_dang_cong_thuc_cai` | GIẾT; lỗi giàn giáo=0 · [chi tiết](mutants/bo_cygpath_w.json) |
| `bo_exe` | 0/11: không có | **SỐNG**; lỗi giàn giáo=0 · [chi tiết](mutants/bo_exe.json) |
| `bo_f_ca_hai` | 0/11: không có | **SỐNG**; lỗi giàn giáo=0 · [chi tiết](mutants/bo_f_ca_hai.json) |
| `bo_f_ten_tran` | 0/11: không có | **SỐNG**; lỗi giàn giáo=0 · [chi tiết](mutants/bo_f_ten_tran.json) |
| `bo_ghi_github` | 3/11: `r858_cai_linux_chon_ban_chay_duoc`, `r858_cai_macos_chon_ban_chay_duoc`, `r858_cai_windows_chon_ban_chay_duoc` | GIẾT; lỗi giàn giáo=0 · [chi tiết](mutants/bo_ghi_github.json) |
| `bo_return_1` | 4/11: `r858_cai_linux_chon_ban_chay_duoc`, `r858_cai_macos_chon_ban_chay_duoc`, `r858_cai_windows_chon_ban_chay_duoc`, `r858_hinh_dang_cong_thuc_cai` | GIẾT; lỗi giàn giáo=0 · [chi tiết](mutants/bo_return_1.json) |
| `bo_ten_tran` | 5/11: `r858_cai_linux_chon_ban_chay_duoc`, `r858_cai_macos_chon_ban_chay_duoc`, `r858_cai_windows_chon_ban_chay_duoc`, `r858_bat_buoc_bash_khong_dua_rg_hong_len_dau`, `r858_hinh_dang_cong_thuc_cai` | GIẾT; lỗi giàn giáo=0 · [chi tiết](mutants/bo_ten_tran.json) |
| `bo_x` | 1/11: `r858_hinh_dang_cong_thuc_cai` | GIẾT; lỗi giàn giáo=0 · [chi tiết](mutants/bo_x.json) |

`bo_cygpath_u_doc_lap` được đo thêm một lần độc lập: vẫn 11/11 qua, không kill; không tính nó thành mutant mới. Bản ghi [ở đây](mutants/bo_cygpath_u_doc_lap.json). Tổng 10 mutant chốt khác nhau: 6 chết, 4 sống (có chồng phạm vi), 0 lỗi giàn giáo. Survivor được báo ở F858-02.

## Đột biến từng ứng viên Q2

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python out/mutate.py candidates`. Bỏ từng token của từng công thức, giữ nguyên prefix installer; 29/29 bị `r858_hinh_dang_cong_thuc_cai` giết bằng `TinHieuChotCa`, không lỗi khác. Đây là số đo **shape**, không chứng minh tất cả vị trí ứng viên đã được thử bằng hành vi.

| Mutant (mỗi hàng là một phép) | Kết quả thật |
|---|---|
| `ung_vien_git_linux_1` | TinHieuChotCa · GIẾT · [chi tiết](mutants/ung_vien_git_linux_1.json) |
| `ung_vien_git_linux_2` | TinHieuChotCa · GIẾT · [chi tiết](mutants/ung_vien_git_linux_2.json) |
| `ung_vien_git_macos_1` | TinHieuChotCa · GIẾT · [chi tiết](mutants/ung_vien_git_macos_1.json) |
| `ung_vien_git_macos_2` | TinHieuChotCa · GIẾT · [chi tiết](mutants/ung_vien_git_macos_2.json) |
| `ung_vien_git_windows_1` | TinHieuChotCa · GIẾT · [chi tiết](mutants/ung_vien_git_windows_1.json) |
| `ung_vien_git_windows_2` | TinHieuChotCa · GIẾT · [chi tiết](mutants/ung_vien_git_windows_2.json) |
| `ung_vien_git_windows_3` | TinHieuChotCa · GIẾT · [chi tiết](mutants/ung_vien_git_windows_3.json) |
| `ung_vien_git_windows_4` | TinHieuChotCa · GIẾT · [chi tiết](mutants/ung_vien_git_windows_4.json) |
| `ung_vien_python_linux_1` | TinHieuChotCa · GIẾT · [chi tiết](mutants/ung_vien_python_linux_1.json) |
| `ung_vien_python_linux_2` | TinHieuChotCa · GIẾT · [chi tiết](mutants/ung_vien_python_linux_2.json) |
| `ung_vien_python_macos_1` | TinHieuChotCa · GIẾT · [chi tiết](mutants/ung_vien_python_macos_1.json) |
| `ung_vien_python_macos_2` | TinHieuChotCa · GIẾT · [chi tiết](mutants/ung_vien_python_macos_2.json) |
| `ung_vien_python_windows_1` | TinHieuChotCa · GIẾT · [chi tiết](mutants/ung_vien_python_windows_1.json) |
| `ung_vien_python_windows_2` | TinHieuChotCa · GIẾT · [chi tiết](mutants/ung_vien_python_windows_2.json) |
| `ung_vien_python_windows_3` | TinHieuChotCa · GIẾT · [chi tiết](mutants/ung_vien_python_windows_3.json) |
| `ung_vien_shellcheck_linux_1` | TinHieuChotCa · GIẾT · [chi tiết](mutants/ung_vien_shellcheck_linux_1.json) |
| `ung_vien_shellcheck_linux_2` | TinHieuChotCa · GIẾT · [chi tiết](mutants/ung_vien_shellcheck_linux_2.json) |
| `ung_vien_shellcheck_macos_1` | TinHieuChotCa · GIẾT · [chi tiết](mutants/ung_vien_shellcheck_macos_1.json) |
| `ung_vien_shellcheck_macos_2` | TinHieuChotCa · GIẾT · [chi tiết](mutants/ung_vien_shellcheck_macos_2.json) |
| `ung_vien_shellcheck_windows_1` | TinHieuChotCa · GIẾT · [chi tiết](mutants/ung_vien_shellcheck_windows_1.json) |
| `ung_vien_shellcheck_windows_2` | TinHieuChotCa · GIẾT · [chi tiết](mutants/ung_vien_shellcheck_windows_2.json) |
| `ung_vien_bash_linux_1` | TinHieuChotCa · GIẾT · [chi tiết](mutants/ung_vien_bash_linux_1.json) |
| `ung_vien_bash_linux_2` | TinHieuChotCa · GIẾT · [chi tiết](mutants/ung_vien_bash_linux_2.json) |
| `ung_vien_bash_macos_1` | TinHieuChotCa · GIẾT · [chi tiết](mutants/ung_vien_bash_macos_1.json) |
| `ung_vien_bash_macos_2` | TinHieuChotCa · GIẾT · [chi tiết](mutants/ung_vien_bash_macos_2.json) |
| `ung_vien_bash_windows_1` | TinHieuChotCa · GIẾT · [chi tiết](mutants/ung_vien_bash_windows_1.json) |
| `ung_vien_bash_windows_2` | TinHieuChotCa · GIẾT · [chi tiết](mutants/ung_vien_bash_windows_2.json) |
| `ung_vien_bash_windows_3` | TinHieuChotCa · GIẾT · [chi tiết](mutants/ung_vien_bash_windows_3.json) |
| `ung_vien_bash_windows_4` | TinHieuChotCa · GIẾT · [chi tiết](mutants/ung_vien_bash_windows_4.json) |

Chỉ số token: Linux/macOS `1` = ứng viên `/usr/bin` hoặc brew, `2` = fallback `command -v`; Windows git/bash `1,2,3` = `cmd,bin,usr/bin`, `4` = fallback; Windows python `1` = choco, `2` = glob Python3*, `3` = fallback; shellcheck Windows `1` = choco, `2` = fallback.

## Đường biên và đối chứng

Lệnh `python out/edges.py`, `python out/edges.py followup`, `python out/edges.py installer-stdout`; driver ghi các rc con dưới đây, bản thân driver kết thúc 0 vì nhiệm vụ là thu số đo. Dữ liệu/argv dựng trong [edges.py](edges.py). Mọi fixture đều dưới `out/tmp`.

| Phép đo | rc con | Kết quả thật |
|---|---|---|
| spaces-linux-git | 0 | DAT; GITHUB_PATH=/tmp/claude-0/-home-user-tra-luat/8020da77-7294-54d3-ba3c-35424edfafe5/scratchpad/rv1/out/tmp/lt_7af_vx1o/candidate with spaces/goc/usr/bin · [log](evidence/edges.log) |
| spaces-linux-shellcheck | 0 | DAT; GITHUB_PATH=/tmp/claude-0/-home-user-tra-luat/8020da77-7294-54d3-ba3c-35424edfafe5/scratchpad/rv1/out/tmp/lt_k_3kctwb/candidate with spaces/goc/usr/bin · [log](evidence/edges.log) |
| spaces-linux-bash | 0 | DAT; GITHUB_PATH=/tmp/claude-0/-home-user-tra-luat/8020da77-7294-54d3-ba3c-35424edfafe5/scratchpad/rv1/out/tmp/lt_pbmrtk4q/candidate with spaces/goc/usr/bin · [log](evidence/edges.log) |
| spaces-linux-python | 3 | không DAT; GITHUB_PATH=rỗng; stderr=loi: ban hong<br>cai_cong_cu: 'python' khong co cong thuc cai tu dong cho nen nay · [log](evidence/edges.log) |
| spaces-macos-git | 0 | DAT; GITHUB_PATH=/tmp/claude-0/-home-user-tra-luat/8020da77-7294-54d3-ba3c-35424edfafe5/scratchpad/rv1/out/tmp/lt_35gb9joi/candidate with spaces/brew/bin · [log](evidence/edges.log) |
| spaces-macos-shellcheck | 0 | DAT; GITHUB_PATH=/tmp/claude-0/-home-user-tra-luat/8020da77-7294-54d3-ba3c-35424edfafe5/scratchpad/rv1/out/tmp/lt_11tqlchz/candidate with spaces/brew/bin · [log](evidence/edges.log) |
| spaces-macos-bash | 0 | DAT; GITHUB_PATH=/tmp/claude-0/-home-user-tra-luat/8020da77-7294-54d3-ba3c-35424edfafe5/scratchpad/rv1/out/tmp/lt_lrws6kzo/candidate with spaces/brew/bin · [log](evidence/edges.log) |
| spaces-macos-python | 3 | không DAT; GITHUB_PATH=rỗng; stderr=loi: ban hong<br>cai_cong_cu: 'python' khong co cong thuc cai tu dong cho nen nay · [log](evidence/edges.log) |
| spaces-windows-git | 0 | DAT; GITHUB_PATH=W:/tmp/claude-0/-home-user-tra-luat/8020da77-7294-54d3-ba3c-35424edfafe5/scratchpad/rv1/out/tmp/lt_8_5o_lrv/candidate with spaces/pf/Git/cmd · [log](evidence/edges.log) |
| spaces-windows-shellcheck | 0 | DAT; GITHUB_PATH=W:/tmp/claude-0/-home-user-tra-luat/8020da77-7294-54d3-ba3c-35424edfafe5/scratchpad/rv1/out/tmp/lt__xnpk2k5/candidate with spaces/choco/bin · [log](evidence/edges.log) |
| spaces-windows-bash | 0 | DAT; GITHUB_PATH=W:/tmp/claude-0/-home-user-tra-luat/8020da77-7294-54d3-ba3c-35424edfafe5/scratchpad/rv1/out/tmp/lt_57eq8xsl/candidate with spaces/pf/Git/bin · [log](evidence/edges.log) |
| spaces-windows-python | 3 | không DAT; GITHUB_PATH=rỗng; stderr=loi: ban hong<br>cai_cong_cu: 'python' khong co cong thuc cai tu dong cho nen nay · [log](evidence/edges.log) |
| mapped | 0 | DAT; GITHUB_PATH=W:/tmp/claude-0/-home-user-tra-luat/8020da77-7294-54d3-ba3c-35424edfafe5/scratchpad/rv1/out/tmp/lt_qlu620q7/pf/Git/cmd · [log](evidence/edges.log) |
| no-programfiles | 0 | DAT; GITHUB_PATH=W:/tmp/claude-0/-home-user-tra-luat/8020da77-7294-54d3-ba3c-35424edfafe5/scratchpad/rv1/out/tmp/lt_e7x_u_jo/pf/Git/cmd · [log](evidence/edges.log) |
| missing-cygpath | 1 | không DAT; GITHUB_PATH=rỗng; stderr=/tmp/claude-0/-home-user-tra-luat/8020da77-7294-54d3-ba3c-35424edfafe5/scratchpad/rv1/out/tmp/lt_c3ex2qcd/kho/ops/cai_cong_cu.sh: line 47: cygpath: command not found<br>/tmp/claude-0/-home-user-tra-luat/8020da77-7294-54d3-ba3c-35424e · [log](evidence/edges.log) |
| fail-w | 0 | DAT; GITHUB_PATH=rỗng; stderr=conversion-failed · [log](evidence/edges.log) |
| bad-github-path | 0 | DAT; GITHUB_PATH=rỗng; stderr=/tmp/claude-0/-home-user-tra-luat/8020da77-7294-54d3-ba3c-35424edfafe5/scratchpad/rv1/out/tmp/lt_n36h5vrr/kho/ops/cai_cong_cu.sh: line 53: /tmp/claude-0/-home-user-tra-luat/8020da77-7294-54d3-ba3c-35424edfafe5/scratchpad/rv1/out/t · [log](evidence/edges.log) |
| exe-only | 1 | không DAT; GITHUB_PATH=rỗng; stderr=cai_cong_cu: khong thu muc nao co 'git' chay duoc · [log](evidence/edges.log) |
| fail-w-direct | 37 | không DAT; GITHUB_PATH=rỗng; stderr=conversion-failed · [log](evidence/edges.log) |
| python-glob-matched | 0 | </tmp/claude-0/-home-user-tra-luat/8020da77-7294-54d3-ba3c-35424edfafe5/scratchpad/rv1/out/tmp/lt_gf_akdyz/drive with spaces/Python311><br></tmp/claude-0/-home-user-tra-luat/8020da77-7294-54d3-ba3c-35424edfafe5/scratchpad/rv1/out/tmp/lt_gf_akdyz/drive with spaces/Python313 custom> · [log](evidence/edges.log) |
| python-glob-unmatched | 0 | </tmp/claude-0/-home-user-tra-luat/8020da77-7294-54d3-ba3c-35424edfafe5/scratchpad/rv1/out/tmp/lt_gf_akdyz/empty drive/Python3*> · [log](evidence/edges.log) |
| python-spaces-fixed-linux | 0 | DAT; GITHUB_PATH=rỗng; stderr=cai_cong_cu: 'python' ten tran da DAT, giu nguyen PATH · [log](evidence/edges-followup.log) |
| python-spaces-fixed-macos | 0 | DAT; GITHUB_PATH=rỗng; stderr=cai_cong_cu: 'python' ten tran da DAT, giu nguyen PATH · [log](evidence/edges-followup.log) |
| python-spaces-fixed-windows | 0 | DAT; GITHUB_PATH=rỗng; stderr=cai_cong_cu: 'python' ten tran da DAT, giu nguyen PATH · [log](evidence/edges-followup.log) |
| mapped-control | 0 | DAT; GITHUB_PATH=W:/tmp/claude-0/-home-user-tra-luat/8020da77-7294-54d3-ba3c-35424edfafe5/scratchpad/rv1/out/tmp/lt_7tab37b1/pf/Git/cmd · [log](evidence/edges-followup.log) |
| mapped-without-cygpath-u | 1 | không DAT; GITHUB_PATH=rỗng; stderr=cai_cong_cu: khong thu muc nao co 'git' chay duoc · [log](evidence/edges-followup.log) |
| linux-bad-github-path | 0 | DAT; GITHUB_PATH=rỗng; stderr=/tmp/claude-0/-home-user-tra-luat/8020da77-7294-54d3-ba3c-35424edfafe5/scratchpad/rv1/out/tmp/lt_aim59jdk/kho/ops/cai_cong_cu.sh: line 53: /tmp/claude-0/-home-user-tra-luat/8020da77-7294-54d3-ba3c-35424edfafe5/scratchpad/rv1/out/t · [log](evidence/edges-followup.log) |
| installer-stdout-quiet | 0 | cuối {'rg': 'DAT', 'bash': 'DAT'}; cai_cong_cu: 'bash' ten tran da DAT, giu nguyen PATH · [log](evidence/installer-stdout.log) |
| installer-stdout-text | 0 | cuối {'rg': 'DAT', 'bash': 'DAT'}; cai_cong_cu: 'bash' ten tran da DAT, giu nguyen PATH · [log](evidence/installer-stdout.log) |
| installer-stdout-directory | 2 | cuối {'rg': 'DO', 'bash': 'DAT'}; cai_cong_cu: 'bash' ten tran da DAT, giu nguyen PATH · [log](evidence/installer-stdout.log) |

Ba dòng `spaces-*-python` ban đầu rc=3 là **fixture sai của reviewer**: nó làm python chết cả khi bootstrap chạy script, vượt phụ lục chủ kho. Ba dòng `python-spaces-fixed-*` dùng shim chỉ hỏng `--version`, chuyển script tới Python thật, đều rc=0/DAT, không ghi thư mục hỏng. Không dùng ba rc=3 để kết tội bản vá. Dòng `exe-only` trên Linux rc=1 cũng **không** là lỗi head Windows: Python POSIX không tự phân giải tên trần sang `.exe`.

Các phép khoảng trắng cho git/bash/shellcheck đều DAT trên 3 nền mô phỏng. `ProgramFiles` vắng vẫn DAT nhờ fallback mặc định và stub chuyển đổi thực sự. `cygpath` vắng với git chưa DAT thì khác 0, không báo xanh. Glob Python3* giữ nguyên tên có khoảng trắng và mở ra hai ứng viên khi có khớp; không khớp thì giữ token glob literal. Theo phụ lục, không suy từ glob sang lời khai probe Python ứng viên.

## L3, signing và đường Windows thuần Python

| Lệnh / phép | rc / kết quả thật |
|---|---|
| `python out/l3_probe.py` (một lệnh dựng cả nền/head) | Driver 0; tiến trình nền 0/1, head 0/0; giá trị ca nền true/false, head true/true. [Log](evidence/l3-probe.log). |
| `python out/sign_probe.py` | Driver 0; trích nguyên hai hàm r226/r268 bằng AST, chạy trên cả nền/head: cấu hình signing của máy → false/false; override `commit.gpgsign=false` chỉ trong env con → true/true. [Log](evidence/sign-probe.log). |
| Mô phỏng `LA_WINDOWS=True`, chỉ 9 `DOT_BIEN_HOOK` wp858, gọi chính `chay_dot_bien()` | rc=0; 9/9 giết, errors=0, unmeasured=0; kill bởi shape/N6 thuần Python. [Log](evidence/wp858-windows-shape.log). Không phải Windows thật. |

# Không đo được / chưa nghiệm thu

- Không gọi GitHub theo assignment: chưa readback CI/check run, workflow_dispatch Windows, threads, decision cho finding hoặc trạng thái lease server. Chỉ xác minh ref/spec/lease offline đã cấp; không tự nhận toàn bộ điều kiện merge.
- Không có native Windows/macOS; chưa đo sàn 70% của toàn bảng trên từng nền, hành vi `.exe`/MSYS/PATHEXT thật, choco/brew/apt-get thật. 9 mutant mới đo được trong đường thuần Python mô phỏng không thay các số đo đó.
- Không xác nhận tổng launcher suite N/N: 10 ca bị bỏ qua (8 ca cần venv/pypdf không có bản cài offline, một fixture chỉ dành cho Windows và một ca native Windows SID); 12 ca credential đỏ vì TMPDIR dưới ancestor có `.git`. Cả nền/head cùng tập đỏ; không xoá chốt credential hay dời fixture ra ngoài phạm vi được giao để ép xanh.
- L2/t86: **không tái hiện** cơ chế race của executor. Solo cũng đỏ vì môi trường; hai suite ×10 và bằng chứng nền đỏ do đúng race chưa đo được. N5 chưa được xác nhận, không tuyên bố đã đóng.
- Vòng bán kính 470 mutant của `ops/cong_cu_test.py` bị ngắt; chỉ kết quả chế độ gate và phạm vi nó thực sự chạy được công nhận. Phần shard bị giao đi không được gọi là đã chạy.
- Chế độ gate `cong_cu_test` rc=0 nhưng chỉ 60/60 ca đã chạy (61 tổng): `t47_INDEX_phai_duoc_doc_TRUNG_THUC_va_nguon_py_nhan_du_moi_cach_viet` bỏ qua vì fixture không dựng được INDEX chưa hoà giải (`stage={'0'}`). Không khai 61/61.
- Tổng headline 286/286 của runner đột biến có phần tín dụng generic exception của code cũ. Các lỗi đó không đáp ứng quy tắc “chỉ TinHieuChotCa”; chỉ các phép wp858/chốt độc lập đã khai loại tín hiệu được dùng để đánh giá chốt mới. Không thêm finding ngoài packet cho hành vi cũ này.
- Nợ `python-probe-khong-theo-PATH` vẫn mở đúng phụ lục #858/6312034981; không sửa/đòi sửa `ops/cong_cu.py`, không tuyên bố probe đã thấy Python ứng viên.
- Các hướng cần nội dung đường dẫn thoát cây không được soạn hoặc chạy. Cần review riêng quan hệ tin cậy giữa đường cài, PATH và ranh giới cây nếu muốn mở rộng phạm vi; không có kết luận kiểm thử cho chúng trong lượt này.
- Snapshot đầu/cuối của `kho/` so HEAD/tree, trạng thái tracked/untracked/ignored và SHA-256 nội dung 4.839 tệp tracked. Chúng trùng nhau; không có delta quan sát được. Snapshot hai mốc không chứng minh lịch sử chưa từng ghi rồi hoàn nguyên, và không thay cơ chế sandbox. [Đầu](evidence/before.json), [cuối](evidence/after-final.json).

Kiểm tra artifact cuối: băm spec khớp, snapshot đầu/cuối bằng nhau, mọi liên kết evidence trong verdict có đích tồn tại. Băm tệp được lưu ở [SHA256SUMS](SHA256SUMS).

Các log, bản sao và script là evidence review, không là thay đổi mã sản phẩm hay quyền merge/land/deploy.
