Verdict: request_changes
Reviewed commit: ad5712faddcaee4f45190e00d8faf75353430063
Spec sha256: 67b448acc825fdd29f118c3b9082583773b4ad218a7c83ab4db496daa8f26d81

**Còn một finding P2: F14 — chốt hồi quy chưa bảo vệ đủ thiết kế subreaper.** Ba mutant làm sai những điều chủ kho chốt vẫn vượt **26/26 ca hành vi**: đặt subreaper sau Popen, thu hồi child ngoài nhóm, và nhận lỗi `killpg(pg, 0)` khác ESRCH thành thành công. Đối chứng riêng phân biệt được cả ba với head. Lệnh, output và giới hạn phép đo nằm ở bảng F14 bên dưới; không suy kết quả này thành toàn bộ runner đột biến vẫn xanh khi thay source.

Các tái hiện cũ của **F09, F12 và hai biểu hiện F13 đã đóng trong tập thử**. Helper nguyên trạng tuân thủ thiết kế (B) trong các phép đo bổ sung: đặt subreaper trước Popen ở cả hai đường gọi; chỉ thu hồi nhóm đích; lỗi/thiếu prctl, lỗi probe và hết hạn trả trạng thái không xác minh; vẫn rc 0 và một dòng `agent_creds:` ở các nhánh `nap` đã thử. Hai suite đăng ký đều xanh, đúng số liệu executor khai, nhưng chưa khóa các sai lệch mà F14 chỉ ra.

Base dùng cho mọi delta: `97120d3c76ebb7c3eda4b585ff46f1c51e30c91b`. Tree head: `7d5a5a814394f01ca74ac0b74b690537a1e2c682`. Áp trần **8 tệp / 700 dòng thêm**, ngoại lệ D2/settings.json và thiết kế (B) theo `run/f16f80b7/prompt.snapshot`. Không đề xuất quay lại đọc `/proc`. Ngưỡng approve của lượt này: không còn P0/P1/P2/P3. Verdict không cấp quyền merge/land.

**Neo và cách tái chạy**

Các lệnh dưới chạy từ sandbox, trừ lệnh có ghi cwd. [common.py](evidence/common.py) tạo hai clone cục bộ detached `evidence/head` và `evidence/base`, đặt `git config core.abbrev 7` trước các phép kiểm. Khi đọc `cay-kho`, lệnh Git dùng `-c core.abbrev=7`. Môi trường phép thử được dựng từ danh sách cho phép trong `common.ENV`, có `PYTHONDONTWRITEBYTECODE=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_SYSTEM=/dev/null`, thư mục tạm và HOME đồ giả. Đột biến chỉ ghi vào sandbox/bản sao. Bootstrap, agy và tải mạng của các fixture đều là đồ giả.

`PYTHONDONTWRITEBYTECODE=1 python3 evidence/checks.py identity` → [identity.json](evidence/identity.json): head/base/tree/spec đúng các OID và băm trên; `write_set_exact=true`, `file_count=8`, `added=699`, `removed=7`; `diff_equal=true`, `diff4_equal=true`, `numstat_equal=true`, `copy_equal=true`, `status=""`. Cụ thể, bytes của hai patch bằng `git diff BASE HEAD` và `git diff b89bb17 HEAD`; các tệp write set trong bản sao bằng `cay-kho`. Phép kiểm lặp cuối vẫn cho cùng kết quả. `status` đến từ `git status --porcelain=v1 --untracked-files=all --ignored`, không phải lời khẳng định đã giám sát mọi syscall.

Đúng tám đường dẫn đo được: `.claude/dev/ci_dang_ky_test.py`, `.claude/hooks/session-start.sh`, `RELEASE_MANIFEST.json`, `ops/cloud_agent_creds.py`, `ops/cloud_agent_creds_test.py`, `ops/codex_cloud_setup.sh`, `ops/codex_cloud_setup_test.py`, `references/RUNBOOK.md`.

Các tệp `.json` trong `evidence/logs/` lưu command, cwd, rc, thời gian, stdout và stderr. Bản ghi verdict tăng dần trước khi tổng hợp được giữ ở [verdict-progress.md](evidence/verdict-progress.md).

**ĐỐI CHIẾU LƯỢT TRƯỚC**

`python3 evidence/replays.py` chạy lại các chế độ `quick`, `processes`, `cleanup_log`, `encoding`, `argv_control` của script lượt 3 trên head mới, trong môi trường đồ giả. [prior_probes.py](evidence/prior_probes.py) bằng byte script lượt 3: `python3 evidence/audit4.py` → `replay_source_equal=true`, sha256 `740f269b712d542335114e3bec8786c06fa0bed657b253044ba5e2ab9a8fe804`. Kết luận bên dưới dùng output mới, không dùng kết quả cũ.

Trong bảng, `P <mode>` viết tắt cho `PYTHONDONTWRITEBYTECODE=1 python3 evidence/probes4.py <mode>`; `R <mode>` chỉ lần gọi mode tương ứng bởi `evidence/replays.py`. Các dòng JSON trong log ghi tên từng ca.

| Finding trước | Lệnh / bằng chứng mới | Output đo được và kết luận |
|---|---|---|
| F09 — va chạm `][` | `P argv`; `R argv_control`; [p4-argv.jsonl](evidence/p4-argv.jsonl) | Dùng đúng mutant lượt 3: `set -- ... nap; "$PY" "$1][$2"`. Hook: H1 SỐNG, **H2 GIẾT**; setup: E1 SỐNG, **E2 GIẾT**, output `PY nhận [['ops/cloud_agent_creds.py][nap']]`. Đối chứng JSON: head nhận `[path,"nap"]`, mutant `["path][nap"]`. Chốt thực thi đã bắt va chạm; việc chốt vị trí H1/E1 không bắt riêng argv không phải finding. **Đóng tái hiện cũ.** |
| F12 — nhóm chưa dừng, log hai kênh | `R cleanup_log`; [prior-cleanup_log.json](evidence/logs/prior-cleanup_log.json); `P previous_mutants` | Cả hai `communicate` ném `TimeoutExpired` và `.output` đã chứa hai log + dòng agent cũ. Head: rc 0; `stdout ***` và `stderr ***` mỗi dòng một lần; đúng một dòng `agent_creds: KHÔNG ĐO ĐƯỢC — bootstrap quá 0.3 s, KHÔNG xác minh được việc dừng`; `alive=[false,true,true]`. Mutant xóa `e.output` **GIẾT** bởi A9 với lý do mất log. **Đóng tái hiện cũ.** |
| F13(a) — lỗi đọc / che `/proc` | `R processes`; [prior-processes.json](evidence/logs/prior-processes.json) | Cùng lỗi signal tiêm làm chỉ cha chết, thử `/proc` đọc bình thường, lỗi quyền và che danh sách: cả ba rc 0, giữ log đã che, đúng một trạng thái **KHÔNG xác minh được việc dừng**, `alive=[false,true,true]`. Không còn báo sai “đã dừng”. **Đóng biểu hiện cũ.** |
| F13(b) — tên tiến trình không UTF-8 | `R encoding`; [prior-encoding.json](evidence/logs/prior-encoding.json) | Tạo lại tiến trình ngoài nhóm tên có byte `0xff`, rồi chạy CLI `nap` trên tl giả: rc 0, stderr rỗng, `ready` và đúng một dòng timeout `đã dừng`, ba PID bootstrap đều chết. Script cũ còn thử trực tiếp `_nhom_song`; lời gọi đó báo `AttributeError` vì hàm đã bị bỏ. **Đây là probe phụ lỗi thời, không phải lỗi CLI**; phép tái hiện CLI thực vẫn chạy và đã đóng lỗi rc 1 cũ. |
| F01 — version timeout để lại con | `R processes`, dòng `F01_version_15s` | Probe `--version` giả dùng đúng hạn 15 s, có cha/con/cháu: 15.021 s; rc 0; `alive=[false,false,false]`; tải giả 1 lần, thay byte. **Đóng tái hiện cũ.** |
| F02 — timeout hữu hạn quá lớn | `R quick` | `2147484`, `1e300` đều về 180. Chạy bootstrap giả với từng cấu hình: rc 0, một dòng `ĐÃ NẠP`, PID đã chết. **Không tái phát.** |
| F03 — fixture thiếu con/cháu | `R quick`, dòng `F12_timeout_normal`; `P previous_mutants` | Head có đủ ba PID và `alive=[false,false,false]`. Mutant chỉ giết cha **GIẾT** tại A4: `nap mất 22.1 s`. Không diễn giải thông báo này thành assertion riêng về PID; bằng chứng ba PID đến từ probe head. **Tái hiện cũ đóng; lỗ chốt mới của cùng nhóm hành vi xem F14.** |
| F04 — bỏ che stderr | `R quick`, `F04_in` / `F04_loi`; `P previous_mutants` | Thử riêng từng kênh: rc 0, `ordinary ***`, trạng thái `ĐÃ NẠP — ***`, stderr helper rỗng. Mutant stderr kế thừa **GIẾT** đúng A7/kênh `loi`. **Không tái phát.** |
| F05 — bỏ gọi / sai đích | `P previous_mutants`; `P setup_regressions`; [p4-setup_regressions.jsonl](evidence/p4-setup_regressions.jsonl) | Bỏ gọi/sai path hook bị H2 giết. Comment setup bị E1/E2 giết (`nap 0 lần`); sai path sống E1 nhưng E2 giết (`missing/cloud_agent_creds.py`). **Các tái hiện cũ đã chặn; F09 cũng đóng như trên.** |
| F06 — thiếu Bash được tính xanh | `R quick`, `F06_no_bash` | Mock resolver không tìm được Bash trên nhánh POSIX: rc 3, `DO:h2_khoi_song_sot_set_e:POSIX mà không có bash dùng được — không được bỏ qua (F06)`. **Không tái phát.** |
| F07 — output version không UTF-8 | `R quick`, đầu vào `\0377` | rc 0; tải giả 1 lần; byte agy được thay. **Không tái phát.** |
| F08 / D2 | `R quick`, `D2`; suite head | rc 0; danh sách tệp đúng `home/.gemini/antigravity-cli/settings.json`. **Đạt ngoại lệ đã duyệt; không mở lại F08.** |
| F10 — token phiên bản | `R quick`, `F10_F07_version` | `1.4.12`, `(1.4.12)`, `1.4.12,`: tải 0. `1.4.120`, `1.4.12rc1`, `1.4.12beta`, `v1.4.12`, `x1.4.12`, `1.4.12-rc1`, `1.4.12+build`, `1.4.12.0`: tải 1, thay byte, rc 0. **Không tái phát trong bảng đầu vào này.** |
| F11 — chỉ kiểm cha | `R processes`, `nap_fault_readable`; `P mutations` | Cha chết, con/cháu sống → head in **KHÔNG xác minh được việc dừng**. Mutant báo thành công khi hết hạn bị A9 giết bằng đúng thông báo báo dừng sai. **Tái hiện cũ đóng.** |

**Bảng đo suite và cổng**

| Phép đo | Lệnh | Output / rc |
|---|---|---|
| Suite helper đầy đủ | `python3 evidence/checks.py suites` → cwd `evidence/head`: `python3 -B ops/cloud_agent_creds_test.py` | rc 0; **212.457 s**; `CA: 26/26 dat`; `DOT BIEN: 45/45 bi giet dung ly do`; `TU KIEM PHAN HANG: DAT (4 dot bien)`; `TONG: DAT`. [Log](evidence/logs/suite-cloud.json). |
| Suite setup đầy đủ | Cùng driver: `python3 -B ops/codex_cloud_setup_test.py` | rc 0; `DOT BIEN: 13/13 bi giet dung ly do`; `13/13`; 3.700 s. [Log](evidence/logs/suite-setup.json). |
| Setup base, đối chiếu F3 | `common.run('base-setup', [sys.executable,'-B','ops/codex_cloud_setup_test.py'], cwd=BASE)` | rc 0; `DOT BIEN: 8/8 bi giet dung ly do`; `11/11`. Head tăng đúng 2 ca. [Lệnh đầy đủ](evidence/logs/base-setup.json). |
| Mẫu tổng kết đăng ký | `python3 evidence/checks.py registry` | Dùng chính `MOI[...]` và `bang_chung_xanh` của head: hai log thực đều `accepted=true`. Đối chứng helper 0/0 ca, 0/0 mutant, 25/26 ca, 44/45 mutant, selfcheck DO đều **false**. [registry.json](evidence/registry.json). |
| H1 sau pip thật | `P previous_mutants` | Dời khối ngay sau tiêu đề, trước pip thật: **GIẾT** đúng H1, `khối ở dòng 237–241, phải sau 505 và trước 580`. Ca gốc xanh trước mutant. [Log](evidence/p4-previous_mutants.jsonl). |
| Phạm vi / kích thước | `python3 evidence/checks.py identity` | Đúng 8 tệp, **+699/-7**, các patch/numstat đầu vào khớp Git. Trong trần +700. |
| Whitespace | `python3 evidence/checks.py gates` → `git diff --check 97120d3c76ebb7c3eda4b585ff46f1c51e30c91b HEAD` | rc 0; stdout/stderr rỗng. [Log](evidence/logs/diff-check.json). |
| Bash | Cùng driver → `bash -n .claude/hooks/session-start.sh`; `bash -n ops/codex_cloud_setup.sh` | Cả hai rc 0; output rỗng. [Hook](evidence/logs/bash-hook.json), [setup](evidence/logs/bash-setup.json). |
| Ruff F, hai tệp mới | Cùng driver → `/root/.local/bin/ruff check --no-cache --select F ops/cloud_agent_creds.py ops/cloud_agent_creds_test.py` | rc 0; `All checks passed!`. [Log](evidence/logs/ruff-new.json). |
| Ruff F, hai `.py` còn lại | Cùng driver → Ruff `--select F --output-format json` trên setup test và tệp đăng ký, ở head/base | Cả hai rc 1, cùng một F401 `shutil imported but unused` trong setup test (head dòng 14, base dòng 12); tệp đăng ký không có lỗi F. `python3 evidence/audit4.py` chuẩn hóa path/vị trí → `ruff_diagnostics_equal=true`: **delta 0**. [Head](evidence/logs/ruff-head.json), [base](evidence/logs/ruff-base.json). |
| Doctrine | Cùng driver → `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .` | rc 0; `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine`. [Log](evidence/logs/doctrine.json). |
| J1 manifest | Cùng driver → `python3 -B scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | rc 0; `ok=true`, expected/checked **195/195**, `failed=[]`, `extra_files=[]`, `package_hash_match=true`. [Log](evidence/logs/release.json). |
| R1/R2 nội dung hiện có | `python3 evidence/audit4.py` | Tiêu đề A0.4e head/base 1/0; mục 22 dòng, đủ từng cụm yêu cầu với số đếm trong JSON; mẫu credential khớp 0. [audit4.json](evidence/audit4.json). Lần đầu script audit nhận nhầm tiêu đề là Markdown heading nên assert lỗi; đã sửa bộ chọn theo tiêu đề `**A0.4e`, chạy lại ra kết quả này. Lỗi harness ban đầu không được tính thành finding hay giết mutant. |

**Thiết kế (B): phép đo bổ sung trên head**

| Hướng thử | Lệnh / output | Kết luận có giới hạn |
|---|---|---|
| Thứ tự subreaper / Popen, `nap` | `P order`: `set_subreaper: 0→1`, rồi `Popen` quan sát SR=1; sau timeout có `waitpid(-pg,1)`; rc 0; ba PID chết; một dòng `đã dừng`. | Head đặt subreaper trước khi mở child. [p4-order.jsonl](evidence/p4-order.jsonl). |
| Cùng đường trong `cai-agy` | `P order`: SR=1 tại Popen `agy --version`; ghi nhận thu hồi `-pg`; ba PID giả chết, rc 0, tải giả 1 lần. | Hành vi thiết kế có ở probe version. Hạn ở probe này rút xuống 0.3 s; phép 15 s riêng nằm trong đối chiếu F01. |
| Không thu hồi child ngoài nhóm | `P outside`: tạo child khác nhóm đã thoát mã 23 nhưng chưa wait. Sau cleanup head, caller lấy được đúng PID và exit 23. | Head giữ status của child ngoài nhóm. Mutant `waitpid(-1,...)` làm caller nhận `ChildProcessError: status consumed by cleanup`. [p4-outside.jsonl](evidence/p4-outside.jsonl). |
| Chỉ ESRCH là đã dừng | `P matrix`: `ESRCH → stopped=true`; `EPERM`, `EINVAL`, `EINTR → stopped=false`; trace có SIGKILL, waitpid âm PGID, rồi killpg 0. | Phép tiêm lỗi đơn vị, không phải lỗi tự nhiên của hệ điều hành. [p4-matrix.jsonl](evidence/p4-matrix.jsonl). |
| Nhóm còn sống hết hạn | `P matrix`: giả killpg 0 vẫn thành công, `HAN_DON=.15` → `stopped=false`, 0.151 s. `R processes`: con/cháu thật còn sống, `HAN_DON=.2` → không xác minh, khoảng 0.704 s kể cả timeout bootstrap. | Head không biến hết hạn thành thành công. Nếu cả communicate và hậu kiểm đều hết hạn, phép Slow cho 0.302 s với HAN_DON=.15: hai ngân sách nối tiếp. Không nâng riêng thành finding vì packet không chốt một deadline dọn tổng. |
| Thiếu / thất bại prctl | `P matrix`: không có thuộc tính `prctl`, hoặc prctl trả -1 → `_SUBREAPER=false`, `stopped=false` dù killpg được giả ESRCH. | Không được suy “đã dừng” nếu không đặt được subreaper. |
| Các nhánh lỗi qua `nap` | `P nap_faults`: thiếu prctl, prctl=-1, killpg0 EPERM, killpg0 EINVAL → **bốn ca rc 0, agent_lines=1**, hai log đã che, trạng thái `KHÔNG xác minh được việc dừng`. | Thử với nhóm thật/tiêm lỗi API; ba PID chết. Driver tự làm subreaper để thu dọn fixture; giá trị trả của prctl mà helper thấy vẫn bị tiêm lỗi. [p4-nap_faults.jsonl](evidence/p4-nap_faults.jsonl). |
| Test đã là subreaper từ trước | `P preexisting`: A11 head rc 0 ở SR ban đầu 0 và 1. Mutant bỏ prctl: SR=0 → rc 3/`DO:a11...không đặt được thật`; SR=1 → rc 0/**SỐNG**. | Precondition ảnh hưởng sức phân biệt của ca. Không tự coi đây là lỗi runtime: khi SR đã là 1, mutant có sẵn điều kiện thu hồi. Cần kiểm soát trạng thái ban đầu nếu mục tiêu là chứng minh chính helper đã gọi prctl. [p4-preexisting.jsonl](evidence/p4-preexisting.jsonl). |

**Đột biến bổ sung: cái nào SỐNG và vì sao**

`python3 evidence/all_cases.py` nạp cùng bộ `CA` của head, chạy **tất cả 26 ca hành vi** trên head và ba bản helper đột biến, mỗi biến thể trong tiến trình riêng. Cả bốn: `rc=0`, `passed=26`, `total=26`, `failures={}`. Không chạy bảng mutation lồng trên source đã sửa: mất neo văn bản của một mutant có sẵn không chứng minh ca hành vi bắt được lỗi mới. Log chứa kết quả từng ca: [head](evidence/all-cases-head.json), [late_subreaper_both](evidence/all-cases-late_subreaper_both.json), [wait_any_child](evidence/all-cases-wait_any_child.json), [killpg_error_success](evidence/all-cases-killpg_error_success.json).

| Mutant / ca đo | Output | Vì sao SỐNG / bằng chứng khác hành vi |
|---|---|---|
| Chuyển `_dat_subreaper()` xuống ngay sau Popen ở **cả nap và version** | **SỐNG, 26/26**. `P controls`: head `['subreaper','Popen']`, mutant `['Popen','subreaper']` ở cả hai đường; oracle head true / mutant false. | A11 tự gọi `_dat_subreaper()` trước khi tự Popen fixture, nên không kiểm thứ tự ở hai entrypoint thật. Các fixture hiện có không ép tình huống orphan xảy ra trước lúc đặt muộn. |
| `os.waitpid(-p.pid, os.WNOHANG)` → `os.waitpid(-1, os.WNOHANG)` | **SỐNG, 26/26**; thêm `P mutations`: sống A11, A4, A9. | Không có child ngoài nhóm để phát hiện thu hồi nhầm. `P outside` đo mutant lấy mất exit status 23 của child khác nhóm, head giữ được. |
| Nhánh `except OSError` của probe killpg 0 trả `True` thay `False` | **SỐNG, 26/26**; thêm `P mutations`: sống A11 và A9. | A9 tiêm lỗi SIGKILL nhưng killpg 0 thật vẫn thành công; A11 không tiêm lỗi probe. `P controls` với EPERM: head `stopped=false`, mutant **true**; oracle head true / mutant false. |
| Bỏ lời gọi subreaper trước Popen của nap, để cleanup mới gọi | `P mutations`: **SỐNG** ở A4 và A11. | Đây là biến thể xóa lời gọi, khác mutant chuyển lời gọi ngay sau Popen nói trên. Chưa chạy tất cả 26 ca cho biến thể xóa này; không suy rộng. |
| Bỏ lời gọi subreaper trước Popen của version | `P mutations`: **SỐNG** ở B10 và A11. | B10 đo PID chết/tải lại, A11 tự thiết lập subreaper cho fixture; chưa đo lời gọi thiết lập ở đường version. Chưa chạy tất cả 26 ca cho riêng biến thể này. |
| Hết HAN_DON trả `True` | `P mutations`: sống A11, nhưng **GIẾT ở A9** với `báo dừng khi nhóm còn sống`. | Có ca hậu kiểm nhóm thật giữ sống để khóa đường hết hạn. Không phải survivor của bộ ca liên quan. |
| Mutant đăng ký `A11_bo_subreaper` khi SR ban đầu 1 | `P preexisting`: **SỐNG** ở A11; cùng mutant khi SR=0 bị **GIẾT**. | Thuộc tính đã được cấp sẵn; không dùng kết quả này làm finding riêng hoặc khẳng định suite mặc định sai. |

Các neo/thay chính xác và cách dựng mutant được giữ trong [all_cases.py](evidence/all_cases.py), [probes4.py](evidence/probes4.py). `P mutations` chạy ca gốc trước từng mutant và chỉ nhận **GIẾT** theo `phan_hang` của head (rc 3 và đúng `DO:<ca>:`); đầy đủ ở [p4-mutations.jsonl](evidence/p4-mutations.jsonl). Các oracle riêng chỉ được gọi là phép phân biệt độc lập, không giả làm mutant đăng ký của executor.

**Bảng finding còn mở**

| ID / mức | Slug | Vị trí | Kết quả |
|---|---|---|---|
| F14 / P2 | `subreaper-regression-oracle-incomplete` | `ops/cloud_agent_creds_test.py:134`, `:139`, `:140`, `:144`, `:212`, `:331` | Ba vi phạm của thiết kế (B) sống qua 26/26 ca hành vi, có đối chứng head/mutant khác nhau. |

- [P2] **F14 `subreaper-regression-oracle-incomplete`**: `ops/cloud_agent_creds_test.py:134` (A11, nhất là tự gọi `_dat_subreaper` ở dòng 139 trước Popen fixture dòng 140), `:212` (B10), `:331` (bảng đột biến A11) — **Lệnh tái hiện:** `PYTHONDONTWRITEBYTECODE=1 python3 evidence/all_cases.py`, `python3 evidence/probes4.py controls`, `python3 evidence/probes4.py outside` — **Output:** head và cả ba mutant đều `rc=0, passed=26, total=26, failures={}`. Oracle thứ tự trả false cho mutant đặt muộn ở cả nap/version; caller mất status child khác nhóm khi waitpid dùng -1; probe EPERM được mutant báo `stopped=true`. Head cho kết quả đúng ở cả ba đối chứng. Đây là thiếu chốt hồi quy cho chính thiết kế được dùng để đóng lớp lỗi tiến trình đã lặp nhiều lượt; không phải khẳng định production head hiện đang đặt muộn, thu hồi sai nhóm hay nhận EPERM thành ESRCH. **Hướng vá:** mở rộng A11/ca liên quan để đo hai entrypoint thật và các hậu điều nhóm, rồi đăng ký ba mutant này với ca đích đỏ đúng lý do.

Gợi ý vá bốn phần cho F14:

1. **Vá ở đâu:** trong `ops/cloud_agent_creds_test.py`, quanh A11/B10 và `DOT_BIEN`; có thể tái bố trí ca hiện có để giữ write set 8 tệp và trần +700. Không cần đổi thiết kế (B) đã đo đúng trên helper.
2. **Vá thế nào:** quan sát trạng thái/thứ tự prctl ngay tại Popen của `nap` và `_ban_khop`; test không tự đặt subreaper hộ đường đang kiểm. Có một child thuộc nhóm khác đã thoát mã riêng nhưng chưa wait; sau cleanup caller phải vẫn lấy được status đó. Tiêm EPERM hoặc lỗi khác ESRCH **ở killpg 0**, giữ đối chứng ESRCH. Kiểm riêng trạng thái SR ban đầu 0/1; nếu đặt lại SR cho phép thử, chỉ làm trong worker riêng và xác nhận bằng PR_GET.
3. **Ca khóa lỗi:** head xanh; mutant đặt subreaper sau Popen ở từng đường phải đỏ do thứ tự; `waitpid(-1,...)` phải đỏ do mất status child ngoài nhóm; mutant coi lỗi probe là thành công phải đỏ do trạng thái `nap` sai. Đòi rc 0, đúng một dòng agent, log đã che ở đường lỗi; giữ ca hết hạn A9 đang bắt đúng. [controls](evidence/p4-controls.jsonl) và [outside](evidence/p4-outside.jsonl) là dữ liệu tái dẫn xuất đã chạy, không phải bản sửa áp vào kho.
4. **Rủi ro của bản vá test:** subreaper là trạng thái của tiến trình test, có thể làm xanh giả mutant nếu đã bật từ ca trước; thu hồi child ngoài nhóm có thể lấy mất status của harness; fixture lỗi dễ để lại orphan. Cô lập worker, đồng bộ fixture bằng tín hiệu sẵn sàng thay vì chỉ sleep, thu dọn PID của chính fixture trong finally và phân biệt lỗi harness với `TinHieuChotCa`. Không nâng số ca đỏ do mất neo hoặc lỗi vô can thành bằng chứng giết đúng.

**Lịch sử lớp và giới hạn**

Giữ nguyên chuỗi lịch sử **F01/F03 → F11 → F13**, với S5/đổi cấu trúc (B) đã được chủ kho chọn. Hai biểu hiện runtime F13 cũ đã đóng qua tái hiện ở bảng trên. F14 là phần thiếu chốt của thiết kế mới trong cùng họ quản lý nhóm tiến trình; đặt ID mới không reset lịch sử hay ngân sách. Không có phép đo trong lượt này cho thấy cần đổi lại cấu trúc.

**KHÔNG ĐO ĐƯỢC trong lượt này:** G1 toàn bộ `tl.py --selftest` so head/base; G2 toàn bộ `launcher.py doctor`; L1 required CI jobs trên exact SHA; M1/M2 LIVE; bootstrap/agy thật; enum `gemini` và hiệu lực tắt auto-update của agy thật; CLAUDE_ENV_FILE ở phiên cloud thật; việc gỡ secret Codex sau setup; thời gian bootstrap thật; tarball thật của sáu nền; Darwin/Windows thật. Các mục này không được tính là passed và không dùng đồ giả thay cho biên nhận LIVE.

R2 chỉ quét nội dung đang có. **KHÔNG ĐO ĐƯỢC** đột biến cần tự soạn nội dung nhạy cảm; hướng thử chỉ mô tả: bên có thẩm quyền cung cấp fixture phù hợp bộ quét trong bản sao và kiểm đúng ca R2 đỏ. Lượt này không tự dựng nội dung ấy.

Kết luận áp cho exact head nêu ở dòng 2: **request_changes vì F14/P2**. Không cấp quyền merge/land.
