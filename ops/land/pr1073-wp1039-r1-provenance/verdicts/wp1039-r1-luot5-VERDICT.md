Verdict: request_changes
Reviewed commit: 164d0bfc47e9336c5440b11fc52b9c93a3e71221
Spec sha256: 67b448acc825fdd29f118c3b9082583773b4ad218a7c83ab4db496daa8f26d81

Còn **hai finding P2**: **F14** chưa đóng hoàn toàn vì chốt thu hồi child ngoài nhóm phụ thuộc thời điểm child thoát; **F15** là hồi quy trong phần nén `_song_roi_don`, có thể để ca A9 xanh dù chưa dọn con/cháu. Các phản chứng và đối chứng được ghi bên dưới. Đây là vấn đề của bộ kiểm; các phép thử runtime đã chạy không cho thấy helper head đặt subreaper muộn, thu hồi nhầm nhóm hay coi EPERM là ESRCH.

Hai suite đầy đủ đạt đúng số liệu executor khai: helper **26/26**, **49/49**, tự kiểm phân hạng **4**; setup **13/13**, **13/13**. Phạm vi đúng **8 tệp, +700/-7**, các cổng được yêu cầu đều đạt theo tiêu chí delta. Các kết quả này không thay thế phản chứng về độ tin cậy của test.

Base: `97120d3c76ebb7c3eda4b585ff46f1c51e30c91b`. Tree head: `b750d095948c36acfa32a0d2f02b75ea79e610b9`. Áp dụng trần **8 tệp / 700 dòng thêm**, ngoại lệ F08/D2 và thiết kế F13(B) theo [prompt.snapshot](run/49dc3031/prompt.snapshot). Không cấp quyền merge/land.

**Neo và cách tái chạy**

Các lệnh driver bên dưới chạy từ sandbox, với tiền tố `PYTHONDONTWRITEBYTECODE=1 python3 -B`; ví dụ `python3 -B evidence5/probes5.py f14`. [common.py](evidence5/common.py) tạo clone riêng head/base, đặt `git config core.abbrev 7`; Git đọc `cay-kho` dùng `-c core.abbrev=7`. Driver dựng môi trường thử từ danh sách cho phép, có `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_SYSTEM=/dev/null`, HOME/TMPDIR trong `evidence5`, không kế thừa credential của phiên. Đột biến chỉ đặt trong bản sao; bootstrap và agy trong fixture đều là đồ giả. Script thử mới: [probes5.py](evidence5/probes5.py). Các log suite/cổng lưu command, cwd, rc, thời gian và hai kênh trong [logs](evidence5/logs). Bản ghi tăng dần trước tổng hợp: [verdict-progress.md](evidence5/verdict-progress.md).

`python3 -B evidence5/checks.py identity` → [identity.json](evidence5/identity.json): `head`, `base`, `tree`, `spec_sha256` khớp các giá trị trên; `write_set_exact=true`, `file_count=8`, `added=700`, `removed=7`, `diff_equal=true`, `diff5_equal=true`, `numstat_equal=true`, `copy_equal=true`, `status=""`. Hai patch được so byte với `git diff BASE HEAD` và `git diff ad5712f HEAD`; các tệp trong bản sao head được so byte với `cay-kho`.

Tám đường dẫn đo được: `.claude/dev/ci_dang_ky_test.py`, `.claude/hooks/session-start.sh`, `RELEASE_MANIFEST.json`, `ops/cloud_agent_creds.py`, `ops/cloud_agent_creds_test.py`, `ops/codex_cloud_setup.sh`, `ops/codex_cloud_setup_test.py`, `references/RUNBOOK.md`.

**ĐỐI CHIẾU LƯỢT TRƯỚC**

Nguồn lượt 4: [VERDICT-LUOT4.md](VERDICT-LUOT4.md), commit `ad5712faddcaee4f45190e00d8faf75353430063`. Giữ slug **`subreaper-regression-oracle-incomplete`** của F14; không đổi ID để xóa lịch sử.

| Biểu hiện F14 | Lệnh và output mới | Phân loại |
|---|---|---|
| Subreaper sau Popen | `evidence5/probes5.py f14`: chính mutant `late_subreaper_both` cũ → rc=3, `DO:a11_subreaper_va_esrch:thứ tự subreaper/Popen: ['popen']`. Hai mutant bổ sung chuyển lời gọi xuống sau Popen thành công, riêng nap và version, cũng rc=3 cùng tín hiệu. `evidence5/probes4.py controls`: head có `['subreaper','Popen']`, mutant `['Popen','subreaper']` ở cả hai đường. | **ĐÃ VÁ THẬT** trong tập thử này. |
| EPERM bị nhận là đã dừng | `evidence5/probes5.py f14`: mutant cũ → rc=3, `DO:a11_subreaper_va_esrch:EPERM của killpg(pg, 0) bị nhận là đã dừng`. `evidence5/probes4.py controls`: head `stopped=false`, mutant `true`. | **ĐÃ VÁ THẬT** trong tập thử này. |
| `waitpid(-1, …)` thu hồi ngoài nhóm | `evidence5/probes5.py f14`: mutant cũ → rc=3, `DO:a11_subreaper_va_esrch:sr=True: dừng=True, sống [], q=0`. `evidence5/probes4.py outside`: head giữ exit=23; mutant gây `ChildProcessError: status consumed by cleanup`. Nhưng `evidence5/probes5.py delayed_outside`, child khởi động chậm 0.8 s → head **rc=0**, mutant **rc=0/SỐNG**, child được đo còn sống trước cleanup. | **VÁ HỜ / mới khóa được lịch chạy nhanh**. Xem F14 bên dưới. |

Log: [f14](evidence5/p5-f14.jsonl), [controls](evidence5/p4-controls.jsonl), [outside](evidence5/p4-outside.jsonl), [delayed_outside](evidence5/p5-delayed_outside.jsonl).

`python3 -B evidence5/all_cases.py` chạy lại toàn bộ 26 ca hành vi cho head và đúng ba mutant lượt 4: head **26/26**, ba mutant **25/26**, đều đỏ A11. Tuy nhiên lượt mutant EPERM này đỏ sớm tại nhánh `sr=False` với `sống [131]`; **không dùng lần đỏ đó làm bằng chứng giết đúng lỗi EPERM**. Lần chạy riêng `probes5.py f14` ở bảng trên mới có đúng thông báo EPERM. `probes5.py repeated_a11` chạy head độc lập 12 lần → **12/12 rc=0**. Log gốc được giữ, không thay bằng kết quả chạy lại: [all-cases-killpg_error_success.json](evidence5/all-cases-killpg_error_success.json), [repeated_a11](evidence5/p5-repeated_a11.jsonl).

Kiểm nhanh F01–F13 dùng output mới của `evidence5/replays.py`, `evidence5/probes4.py argv`, `setup_regressions`, `previous_mutants`, `nap_faults`. Script tái hiện lượt 3 bằng byte bản được cấp: `evidence5/audit4.py` → `replay_source_equal=true`, SHA-256 `740f269b712d542335114e3bec8786c06fa0bed657b253044ba5e2ab9a8fe804`.

| Finding cũ | Output mới / nguồn đo | Kết luận có giới hạn |
|---|---|---|
| F01 | `replays.py`, `prior-processes`, ca `F01_version_15s`: **15.022 s**, rc=0, `alive=[false,false,false]`, tải giả 1, thay byte. | Timeout version dọn cha/con/cháu trong tái hiện cũ. |
| F02 | `prior-quick`: `2147484`, `1e300` → 180; chạy nap giả từng đầu vào → rc=0, một dòng ĐÃ NẠP. | Không tái phát. |
| F03 | `prior-quick`, `F12_timeout_normal`: đủ ba PID, `alive=[false,false,false]`. `previous_mutants`: chỉ giết cha → `DO:a4_qua_han_giet_ca_nhom:nap mất 22.1 s`. | Fixture cha/con/cháu có hoạt động; không diễn giải assertion thời gian thành assertion PID. |
| F04 | `prior-quick`, thử riêng `in`/`loi`: rc=0, `ordinary ***`, `ĐÃ NẠP — ***`, stderr rỗng. Mutant stderr kế thừa bị A7 giết đúng ca. | Không tái phát. |
| F05 | `previous_mutants`: bỏ nap/sai path hook bị H2 giết. `setup_regressions`: sai path bị E2 giết; comment lệnh bị E1/E2 giết. | Các tái hiện cũ đã chặn. |
| F06 | `prior-quick`: resolver Bash rỗng → rc=3, `DO:h2_khoi_song_sot_set_e:POSIX mà không có bash dùng được — không được bỏ qua (F06)`. | Không tính thiếu Bash là xanh. |
| F07 | `prior-quick`, version byte không UTF-8 → rc=0, tải giả 1, thay byte. | Không tái phát. |
| F08 / D2 | `prior-quick`: rc=0, chỉ có `home/.gemini/antigravity-cli/settings.json`. | Đạt ngoại lệ chủ kho duyệt. |
| F09 | `probes4.py argv`: va chạm `][` vẫn sống H1/E1 nhưng **bị H2/E2 giết**; E2 ghi `PY nhận [['ops/cloud_agent_creds.py][nap']]`. Đối chứng `prior-argv_control` phân biệt hai phần tử argv với một phần tử ghép. | Các chốt thực thi bắt tái hiện cũ. |
| F10 | `prior-quick`: `1.4.12`, `(1.4.12)`, `1.4.12,` tải 0; `1.4.120`, `1.4.12rc1`, `1.4.12beta`, `v1.4.12`, `x1.4.12`, `1.4.12-rc1`, `1.4.12+build`, `1.4.12.0` tải 1. | Khớp TOKEN trong bảng đầu vào đã thử. |
| F11 | `prior-processes`: tiêm lỗi khiến chỉ cha chết → `alive=[false,true,true]`, rc=0, một dòng **KHÔNG xác minh được việc dừng**. | Không báo dừng sai trong tái hiện cũ. |
| F12 | `prior-cleanup_log`: hai lần communicate đều TimeoutExpired; vẫn có stdout/stderr đã che, mỗi dòng một lần, một trạng thái không xác minh. `previous_mutants`: bỏ `e.output` → A9 đỏ vì mất log. | Không tái phát. |
| F13 | `prior-processes`: /proc bình thường/lỗi quyền/bị che đều không báo dừng sai khi con/cháu sống. `prior-encoding`: CLI với tên tiến trình chứa byte không UTF-8 → rc=0, một trạng thái “đã dừng”, ba PID chết. Probe phụ gọi `_nhom_song` báo AttributeError vì API đó đã bỏ; không tính thành lỗi CLI. | Hai biểu hiện runtime cũ đã đóng trong tập thử. |

Log đầy đủ: [quick](evidence5/logs/prior-quick.json), [processes](evidence5/logs/prior-processes.json), [cleanup_log](evidence5/logs/prior-cleanup_log.json), [encoding](evidence5/logs/prior-encoding.json), [previous_mutants](evidence5/p4-previous_mutants.jsonl), [argv](evidence5/p4-argv.jsonl), [setup_regressions](evidence5/p4-setup_regressions.jsonl).

**Bảng đo suite và cổng**

| Phép đo | Lệnh thực / driver | Output / rc |
|---|---|---|
| Suite helper đầy đủ | `evidence5/checks.py suites` → cwd head: `python3 -B ops/cloud_agent_creds_test.py` | rc=0, **220.385 s**; `CA: 26/26 dat`, `DOT BIEN: 49/49 bi giet dung ly do`, `TU KIEM PHAN HANG: DAT (4 dot bien)`, `TONG: DAT`. [Log](evidence5/logs/suite-cloud.json). |
| Suite setup đầy đủ | Cùng driver → `python3 -B ops/codex_cloud_setup_test.py` | rc=0, **4.724 s**; `DOT BIEN: 13/13 bi giet dung ly do`, `13/13`. [Log](evidence5/logs/suite-setup.json). |
| Setup base / F3 | `common.run('base-setup', [sys.executable,'-B','ops/codex_cloud_setup_test.py'], cwd=BASE)` | rc=0; `11/11`, mutant `8/8`. Head tăng đúng 2 ca. [Command/output](evidence5/logs/base-setup.json). |
| Mẫu đăng ký | `evidence5/checks.py registry`, dùng chính `MOI[...]` và `bang_chung_xanh` của head | Hai log thực `accepted=true`; log helper thay thành 0/0 ca, 0/0 mutant, 25/26 ca, 48/49 mutant, selfcheck DO đều **false**. [Log](evidence5/registry.json). |
| H1 sau pip thật | `evidence5/probes4.py previous_mutants` | Mutant dời khối ngay sau tiêu đề bị H1 giết: `khối ở dòng 237–241, phải sau 505 và trước 580`. |
| K2 / write set | `evidence5/checks.py identity` → `git diff --name-only BASE HEAD`, `git diff --numstat BASE HEAD` | Đúng 8 tệp, **+700/-7**, trong trần; patch/numstat đầu vào khớp Git. |
| Whitespace | `evidence5/checks.py gates` → `git diff --check BASE HEAD` | rc=0, output rỗng. [Log](evidence5/logs/diff-check.json). |
| Bash | Cùng driver → `bash -n .claude/hooks/session-start.sh`; `bash -n ops/codex_cloud_setup.sh` | Hai lệnh rc=0, output rỗng. [Hook](evidence5/logs/bash-hook.json), [setup](evidence5/logs/bash-setup.json). |
| Ruff F, hai tệp mới | `/root/.local/bin/ruff check --no-cache --select F ops/cloud_agent_creds.py ops/cloud_agent_creds_test.py` | rc=0; `All checks passed!`. [Log](evidence5/logs/ruff-new.json). |
| Ruff F, hai .py còn lại | Ruff `--select F --output-format json` trên setup test và tệp đăng ký ở head/base; `evidence5/audit4.py` chuẩn hóa path/vị trí | Head/base cùng rc=1, một F401 `shutil imported but unused` ở setup test, dòng 14/12; đăng ký không có lỗi. `ruff_diagnostics_equal=true`: **delta 0**. [Audit](evidence5/audit4.json). |
| Doctrine | `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .` | rc=0; `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine`. [Log](evidence5/logs/doctrine.json). |
| J1 | `python3 -B scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | rc=0; `ok=true`, expected/checked **195/195**, failed/extra rỗng. [Log](evidence5/logs/release.json). |
| R1/R2, nội dung hiện có | `evidence5/audit4.py` | A0.4e head/base **1/0**, mục **22 dòng**, đủ từng cụm yêu cầu; mẫu credential khớp **0**. [Số đếm từng cụm](evidence5/audit4.json). |
| Thiết kế B, lỗi probe | `evidence5/probes4.py matrix`; `nap_faults` | Chỉ ESRCH → stopped=true; EPERM/EINVAL/EINTR/nhóm còn tồn tại/thiếu prctl/prctl=-1 → false. Các nap fault thử có rc=0, một dòng agent, log đã che, trạng thái không xác minh. [Matrix](evidence5/p4-matrix.jsonl), [nap](evidence5/p4-nap_faults.jsonl). |

**Phần nén mã và đột biến bổ sung: cái nào SỐNG, vì sao**

So sánh với `ad5712f` dùng source lấy trực tiếp bằng `git show`, không dùng lời khai. `git diff --stat ad5712f HEAD` → chỉ hai tệp helper/test thay đổi, **+25/-24**.

| Hướng thử | Lệnh / output | Nhận định |
|---|---|---|
| `_nem` | `evidence5/probes5.py compression`: `same_object=true`, `error=PermissionError`. A9 với cleanup bình thường vẫn rc=0 ở `cleanup_case`. | Helper ném đúng đối tượng ngoại lệ; chưa thấy hồi quy ở phép đo này. |
| `_song_roi_don` | `compression`: cleanup cũ dọn được khi PATH thiếu kill hoặc kill giả rc=1; head thiếu kill → FileNotFoundError, child sống; head kill rc=1 → trả danh sách PID nhưng child sống. `cleanup_case` xác nhận trên **A9 thật**, chi tiết F15. | **Có đổi hành vi ngoài F14, sinh F15.** |
| `_co_musl`, năm đầu vào thường | `evidence5/probes5.py musl`: prior/head giống nhau: có thư viện thứ nhất/thứ hai → true, không gọi ldd; ldd chứa musl → true; glibc/ldd thiếu → false. | Chưa thấy hồi quy ở năm đầu vào này. |
| `_co_musl`, Path.exists lỗi quyền | Cùng lệnh: prior `PermissionError`, head `result=false`, cả hai không gọi ldd. | **Có đổi hành vi ngoài F14** vì kiểm file được đưa vào phạm vi except. Phép đo này xác nhận sự khác nhau, không chứng minh một nền musl thật có lỗi quyền hoặc đã cài sai nhị phân. |
| Mutant `_co_musl` luôn False | `musl`: **SỐNG B9**, rồi toàn bộ ca hành vi **26/26**, rc=0. Đối chứng giả Linux/x86_64 có thư viện musl: head `linux_amd64_musl`, mutant `linux_amd64`. | Có khoảng trống độ phủ: B9 truyền boolean musl trực tiếp cho hàm ánh xạ; fixture cai-agy thay cả `khoa_nen_hien_tai`. Không suy 26/26 này thành toàn bộ runner đột biến vẫn xanh; không gán lỗi runtime cho head chỉ vì mutant sống. |
| `main` | `compression`: prior/head cùng reconfigure hai kênh UTF-8/backslashreplace; nap/cai-agy gọi đúng hàm một lần, rc=0; argv rỗng/`nap --bad` rc=2, cùng usage trên stderr. Hai hàm tác vụ được mock để không chạy thật. | Không thấy đổi hành vi ở bốn argv này. |
| Subreaper muộn riêng từng đường | `evidence5/probes5.py f14`: cả nap và version → rc=3, đúng `DO:a11_subreaper_va_esrch:thứ tự…`. | **GIẾT đúng lý do**, kể cả mutant đặt lời gọi sau Popen thành công. |
| Thu hồi toàn cục + child chậm | `evidence5/probes5.py delayed_outside`: delay=0 mutant bị giết; delay=0.8 mutant **SỐNG**, A11 rc=0; child vẫn sống trước cleanup. | Chốt chưa chuẩn bị đúng tiền điều “child ngoài nhóm đã thoát nhưng chưa wait”; F14 còn mở. |
| Bỏ prctl khi trạng thái có sẵn | `evidence5/probes4.py preexisting`: SR=0 mutant bị giết, SR=1 **SỐNG**; head xanh cả hai. | Thuộc tính đã được cấp sẵn ở vế SR=1. Không dùng survivor này làm finding riêng hay kết luận runner mặc định sai. |

Log: [compression](evidence5/p5-compression.jsonl), [musl](evidence5/p5-musl.jsonl), [toàn bộ CA dưới mutant musl](evidence5/logs/musl-disabled-all-cases.json), [preexisting](evidence5/p4-preexisting.jsonl).

**Bảng finding còn mở**

| ID / mức | Slug lớp | Vị trí | Hậu quả đo được |
|---|---|---|---|
| F14 / P2 | `subreaper-regression-oracle-incomplete` | `ops/cloud_agent_creds_test.py:136`–140 | Khi child ngoài nhóm khởi động chậm, mutant thu hồi toàn cục sống qua A11. |
| F15 / P2 | `fixture-cleanup-external-command-unchecked` | `ops/cloud_agent_creds_test.py:76`, caller `:121` | Phụ thuộc mới vào kill trong PATH; thiếu lệnh làm A9 hỏng và để con/cháu sống, lệnh rc=1 còn cho A9 xanh dù con/cháu sống. |

- [P2] **F14 `subreaper-regression-oracle-incomplete`**: `ops/cloud_agent_creds_test.py:136`–140 — **Lệnh tái hiện:** `PYTHONDONTWRITEBYTECODE=1 python3 -B evidence5/probes5.py delayed_outside` — **Output:** delay=0: head rc=0, mutant `waitpid(-1, …)` rc=3, `DO:a11_subreaper_va_esrch:sr=True: dừng=True, sống [], q=0`; delay=0.8: cả head và mutant rc=0, mutant `SONG_SOT`, `outside_alive_before_cleanup=[true]` tại lần cleanup đầu. Probe chỉ trì hoãn khởi động child rồi vẫn thoát 7; không đổi assertion hoặc production helper. `sleep(0.3)` không bảo đảm q đã thoát. Nếu q chưa thoát, waitpid toàn cục chưa thể thu q và lời q.wait sau đó vẫn trả 7, nên ca không thử hành vi thu hồi nhầm. **Hướng vá:** chờ xác định q đã thoát **mà chưa tiêu thụ status**, rồi mới gọi cleanup; dùng đồng bộ có hạn và finally dọn fixture. Đối chứng đã chạy trên bản test trong bộ nhớ: `probes5.py delayed_ready` thêm rào `waitid(..., WEXITED | WNOWAIT)` trước cleanup → delay=0 và 0.8 đều head rc=0, mutant rc=3/DO A11, `outside_alive_before_cleanup=[false]`. [Log hướng vá](evidence5/p5-delayed_ready.jsonl). Bản thử này chưa áp vào kho; executor tự áp và tự đo. Không cần đổi thiết kế B của production helper.

- [P2] **F15 `fixture-cleanup-external-command-unchecked`**: `ops/cloud_agent_creds_test.py:76`, dùng bởi A9 ở `:121` — **Lệnh tái hiện:** `PYTHONDONTWRITEBYTECODE=1 python3 -B evidence5/probes5.py cleanup_case` — **Output:** cleanup lấy từ `ad5712f`, cả ba kịch bản bình thường/không có kill/kill trả 1 đều A9 rc=0, `alive_after=[false,false]`. Cleanup head bình thường đạt tương tự; thiếu kill → `rc=4`, `HONG:a9_loi_gui_tin_hieu_khong_bao_da_dung:FileNotFoundError: … 'kill'`, `alive_after=[true,true]`; kill trả 1 → **A9 rc=0**, `alive_after=[true,true]`. PATH chỉ thay trong lời gọi cleanup; bootstrap vẫn là fixture, tín hiệu kill trực tiếp vẫn được phép như đối chứng cũ chứng minh. Đây là lỗi mới của việc thay syscall bằng tiện ích ngoài mà không kiểm rc, không phải lỗi production `_giet_nhom`. **Hướng vá:** phục hồi dọn từng PID bằng `os.kill` như bản trước hoặc cơ chế tương đương không phụ thuộc tiện ích ngoài; giữ danh sách PID sống *trước* dọn cho assertion nhưng bảo đảm dọn trong finally và quan sát hậu điều. Probe dùng lại cleanup cũ đã xác nhận cả ba kịch bản dọn được. [Log](evidence5/p5-cleanup_case.jsonl). Giữ trần +700 bằng điều chỉnh trong write set hiện có.

Hai finding là **hai lớp / hai biểu hiện còn mở**. F14 giữ lịch sử F01/F03 → F11 → F13 → F14; sửa thứ tự/EPERM không đóng phần fixture ngoài nhóm. F15 phát sinh từ phần nén mã lượt 5, không phải yêu cầu đổi lại kiến trúc subreaper.

**Kiểm cuối và giới hạn**

Lặp `evidence5/checks.py identity` cuối lượt vẫn cho cùng head/tree/spec, đúng 8 tệp/+700, `copy_equal=true`, `status=""`. Với `cay-kho`, clone head và clone base: `git -c core.abbrev=7 -C <path> status --porcelain=v1 --untracked-files=all --ignored`, `git diff --exit-code`, `git diff --cached --exit-code` đều rc=0/output rỗng; OID/head/tree ghi trong [final-state.json](evidence5/final-state.json). Đây là quan sát tại các mốc kiểm, không phải giám sát mọi syscall giữa hai mốc.

**KHÔNG ĐO ĐƯỢC trong lượt này:** G1 toàn bộ `tl.py --selftest` so head/base; G2 toàn bộ launcher doctor; L1 required CI jobs trên exact SHA; M1/M2 LIVE; bootstrap/agy thật; enum `gemini` và tác dụng tắt auto-update trên agy thật; CLAUDE_ENV_FILE của phiên cloud thật; việc gỡ secret sau setup; thời gian bootstrap thật; tarball thật sáu nền; Darwin/Windows thật. Không tính các mục này là passed.

R2 chỉ quét nội dung đang có. **KHÔNG ĐO ĐƯỢC** đột biến cần tự soạn nội dung nhạy cảm; hướng thử bằng lời: bên có thẩm quyền cung cấp fixture thích hợp trong bản sao, rồi xác minh đúng ca R2 đỏ. Không tự dựng nội dung đó trong lượt này.
