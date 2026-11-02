Verdict: approve
Reviewed commit: 901644d8f7d24562ee666591f3917b094c5f1426
Spec sha256: 67b448acc825fdd29f118c3b9082583773b4ad218a7c83ab4db496daa8f26d81

F14 và F15 **ĐÃ VÁ THẬT trong phạm vi đã đo**. Không còn finding P0/P1/P2/P3 được xác lập trong lượt này. Hai suite đầy đủ đạt: cloud **26/26 ca, 49/49 đột biến, 4 tự kiểm phân hạng**; setup **13/13 ca, 13/13 đột biến**. Phạm vi đúng **8 tệp, +700/-7**. Các bằng chứng, mutant sống và giới hạn được phân biệt bên dưới.

Base: `97120d3c76ebb7c3eda4b585ff46f1c51e30c91b`. Tree head: `a8b3fc283771cde60cd3d23e731cd26d4464ceaf`. Áp dụng [prompt.snapshot lượt 6](run/5ecbd5af/prompt.snapshot): ngưỡng không P0–P3, trần 8 tệp/+700, ngoại lệ F08/D2 và thiết kế F13(B). **Không cấp quyền merge/land.**

**Neo và cách tái chạy**

Các driver chạy từ thư mục chứa verdict, với tiền tố `PYTHONDONTWRITEBYTECODE=1 python3 -B`; ví dụ `python3 -B evidence6/probes5.py delayed_outside`. [common.py](evidence6/common.py) dựng clone head/base, đặt `git config core.abbrev 7`, dùng `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_SYSTEM=/dev/null`; HOME/TMPDIR thử trong `evidence6`. Tiến trình test nhận môi trường theo danh sách cho phép. Đột biến nằm trong bản sao hoặc hàm nạp vào bộ nhớ driver; bootstrap/agy là fixture giả. [Nhật ký tăng dần](evidence6/verdict-progress.md) được giữ trước khi tổng hợp.

`evidence6/checks.py identity` → [identity.json](evidence6/identity.json): head/base/tree/spec khớp các giá trị trên; `write_set_exact=true`, `file_count=8`, `added=700`, `removed=7`, `diff_equal=true`, `diff6_equal=true`, `numstat_equal=true`, `copy_equal=true`, `status=""`. Hai patch được so byte với `git diff BASE HEAD` và `git diff 164d0bf HEAD`.

Tám đường dẫn đo được: `.claude/dev/ci_dang_ky_test.py`, `.claude/hooks/session-start.sh`, `RELEASE_MANIFEST.json`, `ops/cloud_agent_creds.py`, `ops/cloud_agent_creds_test.py`, `ops/codex_cloud_setup.sh`, `ops/codex_cloud_setup_test.py`, `references/RUNBOOK.md`. `git diff --name-only 164d0bf HEAD` chỉ trả `ops/cloud_agent_creds_test.py`; [kiểm cuối](evidence6/final-state.json) lưu rc/output.

**ĐỐI CHIẾU LƯỢT TRƯỚC**

Nguồn: [VERDICT-LUOT5.md](VERDICT-LUOT5.md), commit `164d0bfc47e9336c5440b11fc52b9c93a3e71221`. Giữ ID và slug, không reset lịch sử F01/F03 → F11 → F13 → F14.

| Finding / lớp | Lệnh và output đo mới | Phân loại |
|---|---|---|
| F14 / `subreaper-regression-oracle-incomplete`: child ngoài nhóm khởi động chậm | `evidence6/probes5.py delayed_outside` là driver lượt 5 đổi đích sang head mới: delay=0/0.8 s, head rc=0, mutant `waitpid(-1)` rc=3, `DO:a11_subreaper_va_esrch:sr=True: dừng=True, sống [], q=0`. `evidence6/delays6.py delayed_outside`: delay **0, 0.05, 0.29, 0.31, 0.8, 2, 5 s**, **7/7 head rc=0**, **7/7 mutant rc=3 đúng A11**. Mọi `outside_alive_before_cleanup` đều false. [Tái hiện](evidence6/p5-delayed_outside.jsonl), [mở rộng](evidence6/p6-extended-delayed_outside.jsonl). | **ĐÃ VÁ THẬT**: rào chờ xác định q đã thoát mà chưa tiêu thụ status. Đã đo bảy độ trễ; không tự nhận đã vét mọi lịch lập lịch. |
| F14: subreaper muộn / nhận EPERM là dừng | `evidence6/all_cases.py`: head **26/26**; mỗi mutant `late_subreaper_both`, `killpg_error_success`, `wait_any_child` **25/26**, đỏ đúng A11. Output lần lượt: `thứ tự subreaper/Popen: ['popen']`; `EPERM của killpg(pg, 0) bị nhận là đã dừng`; `q=0`. [Thứ tự](evidence6/all-cases-late_subreaper_both.json), [EPERM](evidence6/all-cases-killpg_error_success.json), [thu hồi toàn cục](evidence6/all-cases-wait_any_child.json). | **ĐÃ VÁ THẬT**, biểu hiện đã đóng ở lượt trước không tái phát. |
| F15 / `fixture-cleanup-external-command-unchecked` | `evidence6/probes5.py cleanup_case`: head ở **normal / missing_kill / kill_rc1** đều **A9 rc=0, `alive_after=[false,false]`**. Cleanup lấy từ `ad5712f` làm đối chứng cũng đạt cả ba. PATH chỉ thay tại bước dọn. [Log](evidence6/p5-cleanup_case.jsonl). | **ĐÃ VÁ THẬT**: thiếu tiện ích ngoài hoặc tiện ích trả lỗi không còn làm hỏng dọn con/cháu. |

Kiểm nhanh F01–F13 dùng kết quả mới của `evidence6/replays.py`, chạy `prior_probes.py` với các mode `quick`, `processes`, `cleanup_log`, `encoding`, `argv_control`; mỗi tiến trình rc=0. `evidence6/audit4.py` xác nhận byte script tái hiện khớp bản được cấp, SHA-256 `740f269b712d542335114e3bec8786c06fa0bed657b253044ba5e2ab9a8fe804`; không dùng lại output cũ.

| Finding | Lệnh / nhãn và output mới | Kết luận giới hạn |
|---|---|---|
| F01 | `prior_probes.py processes`, `F01_version_15s`: **15.021 s**, rc=0, cha/con/cháu `alive=[false,false,false]`, tải giả 1, thay byte=true. [Log](evidence6/logs/prior-processes.json). | Timeout version 15 s dọn đủ ba thế hệ fixture. |
| F02 | `prior_probes.py quick`: `2147484`, `1e300` →180; nap giả với cả hai giá trị rc=0, một dòng ĐÃ NẠP. [Log](evidence6/quick.jsonl). | Không tái phát tràn timeout. |
| F03 | `quick`, `F12_timeout_normal`: đủ ba PID, tất cả chết, rc=0. `probes4.py previous_mutants`: chỉ giết cha → `DO:a4_qua_han_giet_ca_nhom:nap mất 22.1 s`. [Log âm](evidence6/p4-previous_mutants.jsonl). | Fixture có con/cháu; mutant bị bắt bởi hạn thời gian, không diễn giải thành assertion PID. |
| F04 | `quick`, thử riêng stdout/stderr: `ordinary ***`, `ĐÃ NẠP — ***`, stderr helper rỗng. `previous_mutants`: stderr kế thừa → `DO:a7_che_master_key:loi: TL_MASTER_KEY lọt / không che...`. | Không tái phát trong hai kênh đã thử. |
| F05 | `probes4.py previous_mutants`: bỏ nap/sai path hook bị H2 giết. `probes4.py setup_regressions`: sai path bị E2 giết (`PY nhận [['missing/cloud_agent_creds.py','nap']]`); comment lệnh bị E1/E2 giết (`nap 0 lần`). [Log setup](evidence6/p4-setup_regressions.jsonl). | Các tái hiện gọi thiếu/sai đích đã chặn. |
| F06 | `quick`: resolver Bash trả None → rc=3, `DO:h2_khoi_song_sot_set_e:POSIX mà không có bash dùng được — không được bỏ qua (F06)`. | Không biến thiếu Bash thành bỏ qua xanh. |
| F07 | `quick`, version byte không UTF-8 (`\0377`) → rc=0, tải giả 1, thay byte=true. | Không tái phát lỗi giải mã version. |
| F08 / D2 | `quick`: không đặt CLAUDE_ENV_FILE, nền fixture ngoài bảng → rc=0; tệp duy nhất `home/.gemini/antigravity-cli/settings.json`. | Đạt ngoại lệ đã duyệt. |
| F09 | `probes4.py argv`: va chạm `][` sống H1/E1 nhưng **bị H2/E2 giết**; E2: `PY nhận [['ops/cloud_agent_creds.py][nap']]`. `prior_probes.py argv_control`: head hai phần tử, mutant một phần tử. [Chốt](evidence6/p4-argv.jsonl), [đối chứng](evidence6/argv_control.jsonl). | Không tái phát tại chốt thực thi; riêng H1/E1 không đủ. |
| F10 | `quick`: `1.4.12`, `(1.4.12)`, `1.4.12,` tải 0; `1.4.120`, `1.4.12rc1`, `1.4.12beta`, `v1.4.12`, `x1.4.12`, `1.4.12-rc1`, `1.4.12+build`, `1.4.12.0` tải 1/thay byte. | Khớp TOKEN trong bảng đã thử. |
| F11 | `processes`, tiêm lỗi signal để chỉ cha chết: `alive=[false,true,true]`, rc=0, một trạng thái **KHÔNG xác minh được việc dừng**. | Không báo dừng sai khi con/cháu sống. |
| F12 | `cleanup_log`: hai `communicate` đều TimeoutExpired; stdout/stderr đã che vẫn có đúng một lần, một trạng thái. `previous_mutants`: bỏ `e.output` đỏ đúng A9 vì mất log. [Log](evidence6/logs/prior-cleanup_log.json). | Không tái phát khi dọn thất bại; dọn thành công cũng đạt ở `quick`. |
| F13 | `processes`: `/proc` đọc được/lỗi quyền/bị che đều không báo dừng sai khi con/cháu sống. `encoding`: tên tiến trình fixture có byte không UTF-8 → CLI rc=0, một trạng thái “đã dừng”, ba PID chết. [Log](evidence6/logs/prior-encoding.json). | Không tái phát hai biểu hiện runtime. Probe phụ `_nhom_song` trả AttributeError vì API đã bỏ; không tính probe đó là passed hoặc lỗi CLI. |

Đối chứng cấu trúc F13(B): `evidence6/probes4.py order` ghi `set_subreaper(0→1)` trước `Popen` ở cả nap/version, ba PID mỗi nhóm chết. `matrix` chỉ trả `stopped=true` cho ESRCH; EPERM/EINVAL/EINTR/nhóm còn tồn tại/không có prctl/prctl trả -1 đều false. `nap_faults`: bốn nhánh không xác minh đều rc=0, đúng một trạng thái, log đã che. [Order](evidence6/p4-order.jsonl), [matrix](evidence6/p4-matrix.jsonl), [faults](evidence6/p4-nap_faults.jsonl). AST audit không có literal đường `/proc` trong helper; kiểm tĩnh này không thay đối chứng runtime.

**Bảng đo suite và cổng**

| Phép đo | Lệnh thực / driver | Output / rc |
|---|---|---|
| Suite cloud đầy đủ | `evidence6/checks.py suites` → cwd head: `python3 -B ops/cloud_agent_creds_test.py` | rc=0, **217.490 s**; `CA: 26/26 dat`, `DOT BIEN: 49/49 bi giet dung ly do`, `TU KIEM PHAN HANG: DAT (4 dot bien)`, `TONG: DAT`. [Log](evidence6/logs/suite-cloud.json). |
| Suite setup đầy đủ | Cùng driver → `python3 -B ops/codex_cloud_setup_test.py` | rc=0, **3.773 s**; `DOT BIEN: 13/13 bi giet dung ly do`, `13/13`. [Log](evidence6/logs/suite-setup.json). |
| Setup base / F3 | `common.run('base-setup', [sys.executable,'-B','ops/codex_cloud_setup_test.py'], cwd=BASE)` | rc=0; **11/11**, mutant **8/8**; head tăng đúng hai ca E. [Lệnh/output](evidence6/logs/base-setup.json). |
| Mẫu tổng kết CI | `evidence6/checks.py registry`, dùng chính `MOI[...]` và `bang_chung_xanh` của head | Hai log thực `accepted=true`. Thay log cloud thành 0/0 ca, 0/0 mutant, 25/26 ca, 48/49 mutant hoặc selfcheck DO → cả năm **false**. [Log](evidence6/registry.json). |
| Đối chiếu số ca/mutant | `evidence6/all_cases.py`; đếm phần tử AST `DOT_BIEN` | Head **26** kết quả, tất cả rc=0; đăng ký **49** mutant, bằng mẫu thực **49/49**, không hụt do skip. [Ca](evidence6/all-cases-head.json), [đếm](evidence6/counts.json). |
| H1 sau pip thật | `evidence6/probes4.py previous_mutants` | Dời khối lên ngay sau tiêu đề → `GIET`, `DO:h1_vi_tri_khoi_trong_hook:khối ở dòng 237–241, phải sau 505 và trước 580`. |
| K2 / write set | `evidence6/checks.py identity` → `git diff --name-only BASE HEAD`, `git diff --numstat BASE HEAD` | Đúng 8 tệp, **+700/-7**, khớp danh sách cho phép và numstat đầu vào. |
| Whitespace | `evidence6/checks.py gates` → `git diff --check BASE HEAD` | rc=0, output rỗng. [Log](evidence6/logs/diff-check.json). |
| Bash | Cùng driver → `bash -n .claude/hooks/session-start.sh`; `bash -n ops/codex_cloud_setup.sh` | Cả hai rc=0, output rỗng. [Hook](evidence6/logs/bash-hook.json), [setup](evidence6/logs/bash-setup.json). |
| Ruff F, hai tệp mới | `/root/.local/bin/ruff check --no-cache --select F ops/cloud_agent_creds.py ops/cloud_agent_creds_test.py` | rc=0, `All checks passed!`. Bare lint bằng **ruff 0.16.9**; không kết luận pin CI. [Lint](evidence6/logs/ruff-new.json), [version](evidence6/logs/ruff-version.json). |
| Ruff F, hai .py còn lại | Ruff `--select F --output-format json` trên setup test và tệp đăng ký ở head/base; `evidence6/audit4.py` chuẩn hóa vị trí | Head/base cùng rc=1, một F401 `shutil imported but unused` tại setup test dòng 14/12; tệp đăng ký không lỗi. `ruff_diagnostics_equal=true`: **delta 0**. [Audit](evidence6/audit4.json), [head](evidence6/logs/ruff-head.json), [base](evidence6/logs/ruff-base.json). |
| Doctrine | `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .` | rc=0; `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine`. [Log](evidence6/logs/doctrine.json). |
| J1 | `python3 -B scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | rc=0, `ok=true`, expected/checked **195/195**, failed/extra rỗng. [Log](evidence6/logs/release.json). |
| RUNBOOK R1/R2 | `evidence6/audit4.py` | A0.4e head/base **1/0**, **22 dòng**, mọi cụm bắt buộc có mặt; nội dung hiện có khớp mẫu R2 **0** lần. [Audit](evidence6/audit4.json). |

**Đột biến và tái hiện bổ sung riêng cho lượt 6**

Script mới: [new_probes.py](evidence6/new_probes.py). Các thay đổi nằm trong bản sao/hàm fixture của reviewer. “SỐNG” luôn kèm ca và điều kiện; không gộp vào số 49/49 của suite chính.

| Lệnh / thay đổi | Output | Diễn giải |
|---|---|---|
| `new_probes.py wait_scope`: thay `waitpid(-p.pid)` bằng `waitpid(0)` hoặc `waitpid(p.pid)` trong helper | Cả hai `GIET`, `DO:a11_subreaper_va_esrch:sr=True: dừng=False, sống [], q=None`. [Log](evidence6/new-wait_scope.jsonl). | A11 bắt cả thu hồi nhóm caller và chỉ thu hồi cha; head đối chứng xanh trước mỗi mutant. |
| `new_probes.py barriers`: bỏ waitid khỏi fixture, hoặc thêm WNOHANG mà không kiểm kết quả; q trễ 0.8 s | Với mỗi fixture suy yếu, cả head và mutant `waitpid(-1)` **SỐNG**, rc=0. Fixture nguyên vẹn: head rc=0, mutant rc=3 đúng A11/q=0. [Log](evidence6/new-barriers.jsonl). | Đối chứng âm xác nhận rào chờ mới đóng F14. Mutant sống khi chủ động tháo rào trong bản sao test, không sống với test head. |
| Cùng driver: bỏ WNOWAIT, làm waitid tiêu thụ status | Cả helper head và mutant rc=3/A11/q=0. | Fixture hỏng ngay ở đối chứng dương; **không tính là giết mutant đúng lý do**, dù bộ phân hạng cơ học in `GIET`. |
| `new_probes.py cleanup`: None/PID đã chết/hai PID sống, PATH rỗng; hai tiến trình sống bỏ qua SIGTERM | Head trả đúng hai PID sống trước dọn, `alive_after=[false,false]`, `oracle_pass=true`. Đổi SIGKILL→SIGTERM: `[true,true]`, false. Chỉ dọn PID đầu: `[false,true]`, false. [Log](evidence6/new-cleanup.jsonl). | Hậu điều độc lập bắt hai mutant của cleanup fixture; head dọn đủ hai PID khi PATH không có tiện ích ngoài. |
| `new_probes.py cleanup_a9`: SIGKILL→SIGTERM trong cleanup, chạy A9 nguyên | **SỐNG** ở A9, rc=0, `alive_after=[false,false]`. [Log](evidence6/new-cleanup_a9.jsonl). | Hai child A9 bình thường chịu SIGTERM nên không phân biệt tín hiệu. Probe độc lập phía trên dùng child bỏ qua SIGTERM và bắt mutant. Đây là mutant mã dọn test; head hiện dùng SIGKILL và đạt cả hai đối chứng. |

Không đưa survivor do cố ý làm suy yếu fixture, survivor tương đương trên đầu vào A9, hoặc survivor tại H1/E1 đã bị H2/E2 bắt thành finding của head. Các giới hạn này vẫn được ghi lại; không gọi tất cả mutant bổ sung là bị giết.

**Bảng finding còn mở**

| Mức | Slug / vị trí | Lệnh tái hiện / output / hướng vá |
|---|---|---|
| Không có | Không có finding P0/P1/P2/P3 được xác lập | F14/F15 đóng theo bảng đối chiếu; không đề nghị vá sản phẩm từ mutant fixture đối chứng. |

Hai lớp từ lượt 5 được theo dõi, **0 lớp / 0 biểu hiện còn mở trong phạm vi đo**. Không có mục `- [P0..P3]` vì không có finding yêu cầu sửa.

**Kiểm cuối và giới hạn**

`python3 -B evidence6/final_audit.py` → [final-state.json](evidence6/final-state.json): `candidate_head_unchanged=true`, `copies_at_expected_head=true`, `all_clean=true`; hash spec không đổi. Với `cay-kho`, clone head và clone base, `git status --porcelain=v1 --untracked-files=all --ignored`, `git diff --exit-code`, `git diff --cached --exit-code` đều rc=0/output rỗng; `core.abbrev=7`, HEAD detached. Đây là kiểm trạng thái ở các mốc đầu/cuối, không phải giám sát mọi syscall trong suốt lượt review.

**KHÔNG ĐO ĐƯỢC trong lượt này:** G1 toàn bộ `tl.py --selftest` so head/base; G2 toàn bộ launcher doctor; L1 các required CI job trên exact SHA `901644d…`; M1/M2 LIVE; bootstrap/agy thật; enum gemini và tác dụng tắt auto-update trên agy thật; CLAUDE_ENV_FILE của phiên cloud thật; việc gỡ secret sau setup; thời gian bootstrap thật; tarball thật sáu nền; Darwin/Windows thật. Lời executor khai CI trên `164d0bf` không được tính là bằng chứng CI trên head mới. Không tính các mục này là passed và không cấp quyền merge/land.

R2 chỉ quét nội dung hiện có. Đột biến cần soạn nội dung nhạy cảm: **KHÔNG ĐO ĐƯỢC**; hướng thử bằng lời là bên có thẩm quyền cung cấp fixture thích hợp trong bản sao rồi xác minh đúng ca R2 đỏ. Không tự dựng nội dung đó.
