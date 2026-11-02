Verdict: request_changes
Reviewed commit: cd8ecb60032076acc5976b779102a465d2e62e65
Spec sha256: 67b448acc825fdd29f118c3b9082583773b4ad218a7c83ab4db496daa8f26d81

**request_changes — còn bốn finding P2 (F09–F12).** Các suite đăng ký xanh, nhưng phản chứng bổ sung xác nhận lỗ kiểm ranh giới argv, nhận sai token phiên bản, báo sai hậu điều nhóm tiến trình khi kill lỗi, và mất log bootstrap khi quá hạn. F01–F07 đều đã chặn được tái hiện cũ; F05 còn hở cùng hình dạng qua ranh giới đối số (F09). F08/D2 đạt cách hiểu đã duyệt. Lệnh và output cho từng kết luận nằm trong các bảng dưới.

Base: `97120d3c76ebb7c3eda4b585ff46f1c51e30c91b`; tree head: `eec2270ced7eae5012ac6ac0d760ad9f83475925`. Không có thay đổi mã trên `cay-kho/`; `ENV python3 evidence/final_audit.py` xác nhận cuối lượt `status=""`, `copy_bytes_equal=true`, `diff_packet_equal=true`, đúng head/base/hash và `core_abbrev="7"`.

Đo đầu vào: `git -C cay-kho rev-parse HEAD 'HEAD^{tree}'`, `sha256sum SPEC.md` cho đúng các giá trị trên; `git -C cay-kho status --short` không có output. `git -C cay-kho diff --numstat 97120d3c HEAD`: đúng 8 tệp write set, tổng +612/-7, dưới trần +700 đã duyệt trong prompt.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Các lệnh dưới đây chạy từ sandbox, với `env -i PATH=/usr/local/bin:/usr/bin:/bin HOME="$PWD/evidence/home" PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null LANG=C.UTF-8` (viết tắt **ENV**). Bản sao `evidence/head/` giữ `.git`; `evidence/base/` checkout đúng base. Script phản chứng: `evidence/probes.py`; log JSONL ghi từng ca và output, không dùng lời khai executor làm kết quả.

| Finding cũ | Lệnh / nhãn trong log | Kết quả đo trên head |
|---|---|---|
| F01 | `ENV python3 evidence/probes.py processes` → `F01_version_real_15s_group`; `mutations` → `B4_qua_han_chi_giet_cha` | Probe giả có cha, con, cháu: 15.02 s, rc 0, `alive=[false,false,false]`, tải 1, thay tệp. Mutant chỉ giết cha: `GIET`, `DO:b10_version_treo_giet_ca_nhom:...còn sống...`. Đã đóng tái hiện cũ; kiểm lại khi kill lỗi còn hở, xem F11. |
| F02 | `ENV python3 evidence/probes.py quick` → `F02_timeout`; `mutations` → `A5_bo_tran_tren` | `2147484` và `1e300` đều được đọc thành 180; bootstrap giả có đợi trước khi thoát: nap rc 0, một dòng ĐÃ NẠP, `alive=[false]`. Bỏ trần: `GIET`, `DO:a5_doc_timeout:doc_timeout('1e300') = 1e+300`. Đã đóng. |
| F03 | `processes` → `A4_group`; `mutations` → `A4_chi_giet_cha` | Timeout 2 s: cả cha, con, cháu chết; rc 0, dòng đúng. Mutant chỉ giết cha: `GIET`, `DO:a4_qua_han_giet_ca_nhom:...còn sống [con,cháu]`. Đã đóng lỗ fixture cũ. |
| F04 | `quick` → `F04_channels`; `mutations` → `A7_stderr_ke_thua` | Thử riêng stdout và stderr, mỗi kênh có dòng thường và dòng agent chứa sentinel giả: `redacted=true`, stderr helper rỗng, một dòng agent. Mutant stderr kế thừa: `GIET`, `DO:a7_che_master_key:loi: TL_MASTER_KEY lọt / không che / dòng agent...`. Đã đóng. |
| F05 | `mutations` → `F05_H_skip_nap`, `F05_H_wrong_path`, `F05_E_comment_nap`, `F05_E_wrong_path` | Hai mutant hook chết ở H2 bằng đúng `DO:h2_khoi_song_sot_set_e`; comment setup chết cả E1/E2 bằng `ChotCa`; sai path setup bị E2 bắt (`PY nhận ['missing/cloud_agent_creds.py nap']`). Các tái hiện cũ đã đóng, nhưng argv vẫn bị làm phẳng: **chưa đóng hết hình dạng F05**, xem F09. |
| F06 | `quick` → `F06_no_bash_POSIX` | Mock resolver bash trả None, `LA_WINDOWS=false`: rc 3, `DO:h2_khoi_song_sot_set_e:POSIX mà không có bash dùng được — không được bỏ qua (F06)`. Không còn rc 5/BoQua trong nhánh này. Đã đóng tái hiện cũ. |
| F07 | `quick` → `version_tokens` với `\\0377` | agy giả in byte không phải UTF-8: rc 0, `downloads=1`, `replaced=true`; không bỏ qua bước tải nữa. Đã đóng tái hiện cũ. |
| F08 / D2 | `quick` → `D2`; `mutations` → `D2_ghi_cwd_khi_khong_dat_bien` | Khi không đặt CLAUDE_ENV_FILE, cwd/HOME fixture chỉ có `home/.gemini/antigravity-cli/settings.json`, rc 0. Mutant tạo env.sh bị `DO:d2_khong_env_file_khong_tao_tep` bắt. **Đạt cách hiểu đã duyệt; không nêu lại F08.** |

## Bảng đo

| Hạng mục | Lệnh | Output / kết luận |
|---|---|---|
| Suite helper head | `ENV python3 evidence/run_checks.py suites` → `head-cloud.log` | rc 0; `CA: 24/24 dat`; `DOT BIEN: 36/36 bi giet dung ly do`; `TU KIEM PHAN HANG: DAT (4 dot bien)`; `TONG: DAT`. |
| Suite setup head | Cùng lệnh → `head-setup.log` | rc 0; `DOT BIEN: 11/11 bi giet dung ly do`; `13/13`. |
| Suite setup base | Cùng lệnh → `base-setup.log` | rc 0; `DOT BIEN: 8/8 bi giet dung ly do`; `11/11`. Head tăng đúng hai ca E. |
| Mẫu đăng ký | `ENV python3 evidence/probes.py extended` → `registry_actual_completed_suite`; `quick` → các control `registry` | Log suite đã hoàn tất khớp chính `MOI["ops/cloud_agent_creds_test.py"]`: `accepted=true`. 0 ca, 0 mutant, 23/24 ca, 35/36 mutant và tự kiểm DO: đều `accepted=false`. |
| H1 siết vị trí | `ENV python3 evidence/probes.py mutations` → `H1_khoi_ngay_sau_tieu_de_truoc_pip` | Ca gốc xanh; chuyển khối sau tiêu đề nhưng trước pip thật: `GIET`, `DO:h1_vi_tri_khoi_trong_hook:khối ở dòng 237–241, phải sau 505 và trước 580` (chỉ số dòng của ca). |
| A4 siết nhóm | `processes` → `A4_group`; `mutations` → `A4_chi_giet_cha` | Fixture đã có đủ ba PID, head chết cả ba; mutant bị đúng `TinHieuChotCa` của A4 bắt. Chốt kiểm lại nhóm trong **helper** chưa đầy đủ khi có lỗi, F11. |
| agy siết 1.4.120 | `quick` → `version_tokens`; `mutations` → `B4_so_chuoi_con` | Head: 1.4.12 tải 0; 1.4.120 tải 1/thay tệp. Đổi regex về `AGY_VER in ra`: `GIET`, đúng ca `b34_dung_ban_khong_tai_lech_hoac_hong_thi_thay`, lý do 1.4.120 tải 0 thay vì 1. Các hậu tố chữ còn lọt, F10. |
| Diff / bash | `ENV python3 evidence/run_checks.py gates` → `diff-check.json`, `bash-hook.json`, `bash-setup.json` | `git diff --check 97120d3c HEAD`, `bash -n .claude/hooks/session-start.sh`, `bash -n ops/codex_cloud_setup.sh`: đều rc 0, output rỗng. |
| Ruff F | `ENV python3 evidence/run_checks.py lint` → `lint.jsonl` | Hai tệp mới rc 0, `All checks passed!`. Hai .py khác: head/base đều chỉ có F401 import `shutil` trong `ops/codex_cloud_setup_test.py` (dòng 13/12); delta 0. `python3 -m ruff` ban đầu thiếu module; đã đo lại bằng binary `/root/.local/bin/ruff`. |
| Doctrine | `ENV python3 evidence/run_checks.py gates` → `doctrine.log` | rc 0; `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine`. |
| J1 manifest | Cùng lệnh → `manifest.log`; `ENV python3 evidence/final_audit.py` → `manifest` | rc 0, `ok=true`, `expected_file_count=checked_file_count=195`, `errors=[]`. |
| R1/R2 đọc RUNBOOK | `ENV python3 evidence/final_audit.py` → `R1_R2` | Tiêu đề A0.4e: head 1, base 0; mục 22 dòng; đủ cả 10 cụm, đếm riêng trong log; mẫu credential 0 lần. Đây là quét nội dung hiện có, chưa phải đột biến R2. |

## Findings còn mở

- [P2] F09 `argv-boundaries-still-unchecked`: `ops/cloud_agent_creds_test.py:261`, `:266`; `ops/codex_cloud_setup_test.py:246`, `:251` — `ENV python3 evidence/probes.py mutations` và `extended` — mutant hook gộp `"$GOC/ops/cloud_agent_creds.py" nap` thành `"$GOC/ops/cloud_agent_creds.py nap"` cho `H_argv_collapsed: SONG_SOT`; setup gộp tương tự cho **cả E1/E2 SONG_SOT**. Đồ giả ghi JSON độc lập chứng minh head nhận hai đối số `[path,"nap"]`, mutant chỉ nhận `["path nap"]`. `echo "$*"` làm mất ranh giới đối số, nên lời gọi mà Python thật không thể mở đúng tệp vẫn qua chốt mới. Hướng vá: PY giả ghi mỗi lần gọi bằng JSON array hoặc NUL với số argc; so nguyên danh sách argv và thứ tự các lần gọi, không so chuỗi nối. Thêm hai mutant gộp đối số ở H2/E2; phải đỏ bằng đúng lớp chốt/tên ca. Đây là phần còn hở của F05, không phải bằng chứng lời gọi head hiện tại đang sai.

- [P2] F10 `agy-version-is-not-an-exact-token`: `ops/cloud_agent_creds.py:98` — `ENV python3 evidence/probes.py quick`, các dòng `version_tokens` — agy giả trả `antigravity 1.4.12rc1` hoặc `antigravity 1.4.12beta`: đều `downloads=0`, `replaced=false`, in `agy: ✓ đã có 1.4.12 — không tải`. Quyết định mới yêu cầu token 1.4.12 chính xác; regex chỉ chặn số/dấu chấm nên nhận cả token có hậu tố chữ. Hướng vá: tách/kiểm toàn bộ token phiên bản theo định dạng output đã chấp thuận, hoặc ràng buộc hai biên đủ để không nhận hậu tố tiền phát hành. Giữ ca dương 1.4.12 và ca âm 1.4.120; thêm rc1/beta, đòi tải đúng một lần và thay byte; mutant nới biên chữ phải đỏ đúng B4. Không cần tải hay chạy agy thật để khoá lỗi này.

- [P2] F11 `group-recheck-only-observes-parent`: `ops/cloud_agent_creds.py:36`, `:40`, `:61`, `:97` — `ENV python3 evidence/probes.py processes` và `extended` — lỗi kill được **tiêm bằng mock PermissionError**, cha thật đã thoát, con/cháu thật còn sống: `_giet_nhom` trả `reported_stopped=true`. Qua chính `nap`: rc 0, `agent_creds: KHÔNG ĐO ĐƯỢC — bootstrap quá 0.3 s, đã dừng`, nhưng `alive=[false,true,true]`. Không phải phép đo killpg tự nhiên thất bại trên hệ điều hành; đây là fault injection chứng minh nhánh lỗi nuốt ngoại lệ rồi chỉ poll cha. Mutant thay `return p.poll() is not None` bằng `return True` cũng **SONG_SOT** ở cả A4/B10. Hướng vá: kiểm hậu điều cả nhóm, có hạn chờ và quy ước zombie; lỗi gửi signal hoặc không xác minh được phải trả thất bại/không xác định, không in “đã dừng”. Thêm fixture cha thoát trước, con/cháu giữ pipe; tiêm lỗi kill và đòi không báo thành công. Giữ mutant chỉ giết cha và thêm mutant bỏ hậu kiểm để cả hai đỏ đúng ca.

- [P2] F12 `bootstrap-timeout-drops-diagnostics`: `ops/cloud_agent_creds.py:59`, `:62` — `ENV python3 evidence/probes.py extended` → `timeout_log_forwarding` — bootstrap giả ghi/flush một dòng chẩn đoán trên stdout và một dòng trên stderr rồi ngủ; nap timeout 0.2 s, rc 0, chỉ in dòng trạng thái quá hạn; `forwarded_stdout=false`, `forwarded_stderr=false`. Trái mục tiêu 1: gom stdout+stderr, chuyển tiếp mọi dòng không chứa `agent_creds:` và che TL_MASTER_KEY. Nhánh except trở về trước vòng lọc, bỏ luôn log có ích khi bootstrap treo. Hướng vá: thu output đã nhận sau khi dừng/thu hồi nhóm, dùng chung bộ che/lọc cho đường thường và đường timeout; giữ đúng một dòng trạng thái cuối cùng. Ca bổ sung phải có cả hai kênh, sentinel giả và dòng agent trước khi treo; đòi giữ chẩn đoán đã che, bỏ dòng agent cũ, rc 0 và nhóm chết. Mutant bỏ chuyển tiếp log timeout phải đỏ đúng ca đó.

## Đột biến bổ sung và phạm vi của kết luận

Lệnh: `ENV python3 evidence/probes.py mutations`; log: `evidence/mutations.jsonl`. Mỗi phép dùng `chay_dot_bien` đều chạy ca đích xanh trên bản nguyên trước khi chạy bản đột biến; `GIET` chỉ được trả khi rc 3 có đúng `DO:<tên ca>:` từ `TinHieuChotCa`. Setup dùng lớp riêng `ChotCa` của bộ E. Việc một ca cấu trúc sống nhưng ca hành vi bắt đúng không bị tính thành lỗi bao phủ cả bộ.

| Đột biến bổ sung | Output | Giải thích / đối chứng |
|---|---|---|
| `H_argv_collapsed` | `SONG_SOT` tại H2 | Chuỗi `echo "$*"` giống nhau dù khác argv; đối chứng JSON ở `extended.jsonl`, F09. |
| `E_argv_collapsed` | `SONG_SOT` tại E1 và E2 | Cùng lỗ ranh giới đối số, F09. |
| `F05_E_wrong_path` | E1 `SONG_SOT`, E2 `ChotCa` | E1 chỉ đo vị trí; E2 nay bắt được sai đường dẫn, nên tái hiện cũ đã đóng. |
| `A3_without_separator_check` | `SONG_SOT` | Sáu input A3 không có trạng thái hợp lệ nhưng thiếu dấu ` — `. Đối chứng `quick` trên head với `agent_creds: ĐÃ NẠP` trả KHÔNG ĐO ĐƯỢC; `mutations` → `A3_mutant_invalid_input` trả sai `agent_creds: ĐÃ NẠP —  (bootstrap rc=0)`. Đây là lỗ hồi quy được đo, không phải lỗi parser hiện tại trên input ấy. Nên thêm input thiếu dấu vào A3. |
| `B6_without_regular_file_check` | `SONG_SOT` | Đối chứng `ENV python3 evidence/tar_control.py` → `tar-control.json`: head in “tarball không đúng MỘT tệp thường”; bản bỏ `isreg` in `agy: ✗ lỗi KeyError`; cả hai rc 0, chỉ tạo settings.json. Đích symlink fixture không có trong archive làm `extractfile` lỗi, wrapper vẫn chặn theo hậu quả. **Không suy ra có khai thác đường dẫn trên head.** Chốt loại thành viên chưa bị thử độc lập khỏi nhánh lỗi đọc. |
| `B6_without_count_check` | `GIET` ở B6 | Tar hai member bị chấp nhận và tạo agy, assertion B6 bắt được. |
| `B6_without_name_check` | `GIET` ở B6 | Fixture tên khác đã có trong bộ test làm tạo agy trái điều kiện; assertion B6 bắt được. Chỉ tái dùng fixture có sẵn. |
| `A4_without_recheck` | `SONG_SOT` | Thay `return p.poll() is not None` bằng `return True`; happy path vẫn giết nhóm nên ca không phân biệt việc hậu kiểm có tồn tại. Fault injection độc lập làm lộ F11. |
| `B10_without_recheck` | `SONG_SOT` | Cùng mutant trên probe version; lý do tương tự A4. |

Hai hình dạng dễ tái phát được kiểm lại: **đầu ra bootstrap không đúng hợp đồng** (`A3_without_separator_check`) và **tarball độc** (`B6_without_regular_file_check`). Cả hai đã xuất hiện trong bảng đột biến bổ sung của `VERDICT-LUOT1.md`, và vẫn SỐNG ở phép chạy lượt này. Đây là **hai lần quan sát trong hồ sơ được cung cấp**, không có bằng chứng để gọi là “lần thứ ba”. F12 bổ sung lỗi chuyển tiếp log ở nhánh quá hạn, không phải lần thứ ba của cùng tái hiện thiếu dấu phân cách. Không tự kết luận stop condition lần ba từ số commit vá.

Đối chứng hợp đồng khác: `ENV python3 evidence/probes.py quick` → `contract_inputs`: trạng thái hợp lệ thiếu dấu phân cách và chi tiết rỗng đều bị head từ chối; dòng hợp lệ được chép trạng thái/chi tiết kèm rc. Hai dấu `agent_creds:` cùng nằm trong một dòng vẫn được giữ trong chi tiết; không coi riêng điều đó là vi phạm điều khoản đếm **số dòng**. Các output được lưu nguyên văn trong log.

## Giới hạn và bàn giao

Các mục **KHÔNG ĐO ĐƯỢC trong lượt này**: G1 (toàn bộ `tl.py --selftest` head/base), G2 (toàn `launcher.py doctor`), L1 (required CI jobs trên exact SHA; đầu vào không có biên nhận), M1/M2 LIVE, agy thật và enum `gemini`, hiệu lực biến tắt auto-update ở agy thật, CLAUDE_ENV_FILE trong phiên cloud thật, việc gỡ secret Codex sau setup, thời gian bootstrap thật, tarball thật sáu nền và Windows. Không dùng kết quả fixture để nhận các mục đó là đạt. H1/H3 và vế âm base đã được bộ helper đo, nhưng không thay thế G2.

R2 đã quét nội dung hiện có, nhưng **KHÔNG ĐO ĐƯỢC** phản chứng cần dựng chuỗi nhạy cảm; hướng thử chỉ mô tả: bên được phép cung cấp fixture tổng hợp phù hợp scanner, chạy trong bản sao và đòi đúng ca R2 đỏ. Không tạo nội dung đó trong review này. Các phép tarball dùng fixture sẵn có; kiểm kê tệp chỉ chứng minh trong cây fixture, không phải giám sát mọi đường ghi toàn hệ thống.

Artifact tái hiện: `evidence/run_checks.py`, `evidence/probes.py`, `evidence/final_audit.py`, `evidence/tar_control.py`, các `.log`/`.json`/`.jsonl` tương ứng. Mọi mutant chỉ nằm trong bản sao/tệp tạm. Các hướng vá trên là đề nghị cho executor, chưa áp vào kho.

Verdict này **không cấp quyền merge/land**.
