Verdict: request_changes
Reviewed commit: b89bb1716650960fb7280fb2f5d483b0bd8b325b
Spec sha256: 67b448acc825fdd29f118c3b9082583773b4ad218a7c83ab4db496daa8f26d81

**request_changes — còn 3 finding P2: F09, F12 và F13.** Hai suite đăng ký đều xanh; tái hiện F10 đã đóng. Bản vá F09 vẫn dùng biểu diễn argv có va chạm; F12 còn mất log khi lần thu output thứ hai quá hạn; bộ đọc `/proc` mới có thể báo nhóm chết khi không đọc đủ dữ liệu hoặc làm `nap` thoát rc 1. Các kết luận đều dựa trên phép chạy bên dưới, không dựa vào lời khai executor.

Base: `97120d3c76ebb7c3eda4b585ff46f1c51e30c91b`; tree head: `a7132532a3e424b5d5320969b997837cd4ce626c`. Trần áp dụng theo prompt: ≤8 tệp/≤700 dòng thêm; D2 áp dụng ngoại lệ settings.json đã duyệt. **F13 là LẦN THỨ TƯ của cùng hình dạng “giết/kiểm lại nhóm tiến trình” F01 → F03 → F11**, theo chỉ thị S5. Quyết định giữ cấu trúc hiện tại không loại bỏ yêu cầu hậu kiểm đúng.

## Cách chạy và neo bằng chứng

Các lệnh bắt đầu từ thư mục chứa `VERDICT.md`. **ENV** bên dưới là:

```sh
env -i PATH=/usr/local/bin:/usr/bin:/bin \
  HOME="$PWD/evidence/home" TMPDIR="$PWD/evidence/tmp" LANG=C.UTF-8 \
  PYTHONDONTWRITEBYTECODE=1 \
  GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
```

`ENV git -C cay-kho config core.abbrev 7` được thực hiện trước phép đo. Bản sao `evidence/head/` và `evidence/base/` được clone cục bộ, checkout detached đúng OID và cũng đặt `core.abbrev=7`. Đột biến chỉ ghi vào bản sao/tệp tạm. Các phép bootstrap/agy dùng đồ giả; HOME và môi trường được cô lập như trên.

`git -C cay-kho rev-parse HEAD 'HEAD^{tree}'`, phép băm `hashlib.sha256` của `SPEC.md`, và `git -C cay-kho diff --name-only 97120d3c HEAD` được ghi trong [identity.json](evidence/identity.json). `ENV python3 evidence/audit.py` → [audit.json](evidence/audit.json): head/tree/hash đúng; `write_set_exact=true`, `file_count=8`, `added=659`, `removed=7`; `copy_bytes_equal=true`, `diff_packet_equal=true`, `numstat_packet_equal=true`. Hai patch đầu vào đều bằng byte của phép đo Git tương ứng (`identity.json`).

Audit cuối còn chạy `git status --porcelain=v1 --untracked-files=all --ignored`, `git diff --stat`, `git diff --cached --stat` trên `cay-kho`: đều output rỗng; HEAD/tree giữ nguyên. Đây là đối chiếu trạng thái quan sát được, không phải giám sát mọi syscall. Bản ghi tăng dần trước khi tổng hợp được giữ tại [verdict-progress.md](evidence/verdict-progress.md).

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn đối chiếu: `VERDICT-LUOT2.md` trên `cd8ecb60032076acc5976b779102a465d2e62e65`; kiểm nhanh lượt 1 theo `VERDICT-LUOT1.md` trên `49eb161aad2945ef2de647cd8a4c5805c18e5ab0`. Trong bảng, `quick`, `processes`, `mutations`… viết tắt cho `ENV python3 evidence/probes.py <tên>`; mỗi lần chạy ghi JSONL cùng tên.

| Finding | Lệnh / nhãn phép đo | Output trên head và kết luận |
|---|---|---|
| F09 | `mutations`: `H2_gop_doi_so`, `F09_E_old_collapsed` | Gộp path và `nap` bằng dấu cách như lượt 2: H2 `GIET`; E1 `SONG_SOT`, E2 `GIET` với `PY nhận ['[ops/cloud_agent_creds.py nap]']`. **Tái hiện cũ đã chặn**, nhưng đột biến va chạm `][` sống qua cả H1/H2 và E1/E2; **F09 chưa đóng lớp**, xem finding. |
| F10 | `quick`: `F10_F07_version`; `mutations`: `B4_bien_chi_chan_so` | `1.4.12`: tải 0. `1.4.120`, `1.4.12rc1`, `1.4.12beta`: tải 1, thay byte, rc 0. Khôi phục regex cũ: `GIET`, đúng ca B34, lý do rc1 tải 0 thay vì 1. **Đã đóng trong tập thử.** |
| F11 | `processes`: `nap_fault_readable`; `mutations`: `A9_bo_hau_kiem_nhom` | Tiêm killpg lỗi, chỉ cha chết, `/proc` đọc bình thường: `alive=[false,true,true]`, rc 0, dòng `KHÔNG dừng được`. Mutant trả thành công vô điều kiện bị A9 bắt với đúng `DO:a9_loi_gui_tin_hieu_khong_bao_da_dung`. **Tái hiện cũ đã chặn; lớp còn mở qua F13.** |
| F12 | `quick`: `F12_timeout_normal`; `mutations`: `A4_bo_chuyen_tiep_log_khi_qua_han`; `cleanup_log` | Đường dọn thành công: stdout `stdout ***`, `stderr ***`, đúng một dòng trạng thái; dòng agent cũ biến mất; ba PID chết. Mutant bỏ chuyển tiếp bị A4 bắt đúng lý do log mất. Tuy nhiên khi lần `communicate` thứ hai cũng quá hạn, `.output` đã chứa log nhưng output cuối mất log. **Chưa đóng hết F12.** |
| F01 | `processes`: `F01_version_15s`; `mutations`: `B4_qua_han_chi_giet_cha` | Probe version giả với cha/con/cháu, hạn thật 15 s: 15.020 s, rc 0, `alive=[false,false,false]`, tải 1, thay byte. Mutant chỉ giết cha: `GIET`, B10 báo con còn sống. **Tái hiện cũ đóng; lớp hậu kiểm vẫn có F13.** |
| F02 | `quick`: `F02_timeout_parse`, `F02_timeout_live_*`; `mutations`: `A5_bo_tran_tren` | `2147484` và `1e300` đều về 180. Bootstrap giả đợi rồi thoát: nap rc 0, một dòng ĐÃ NẠP, PID đã chết. Bỏ trần: `GIET`, A5 báo `doc_timeout('1e300') = 1e+300`. **Đóng tái hiện cũ.** |
| F03 | `quick`: `F12_timeout_normal`; suite A4; `mutations`: `A4_chi_giet_cha` | Có đủ cha/con/cháu: cả ba chết ở head. Mutant chỉ giết cha bị A4 bắt bằng `DO:a4_qua_han_giet_ca_nhom:nap mất 22.2 s`; không diễn giải output này thành assertion PID. **Lỗ fixture cũ đóng; lớp hậu kiểm vẫn có F13.** |
| F04 | `quick`: `F04_in`, `F04_loi`; `mutations`: `A7_stderr_ke_thua` | Thử riêng từng kênh: sentinel ở dòng thường/dòng agent đều thành `***`, stderr helper rỗng, một dòng agent. Mutant stderr kế thừa: `GIET`, đúng A7/kênh `loi`. **Đóng tái hiện cũ.** |
| F05 | `mutations`: `H2_bo_qua_nap`, `F05_H_wrong_path`, `F05_E_commented`, `F05_E_wrong_path` | Bỏ gọi/sai path hook bị H2 bắt; comment setup bị E1 và E2 bắt; sai path setup sống E1 nhưng bị E2 bắt. **Tái hiện cũ đóng; ranh giới argv còn F09.** |
| F06 | `quick`: `F06_no_bash` | Mock resolver trả None trên nhánh POSIX: rc 3, `DO:h2_khoi_song_sot_set_e:POSIX mà không có bash dùng được — không được bỏ qua (F06)`. **Đóng tái hiện cũ.** |
| F07 | `quick`: `F10_F07_version`, input `\0377` | Version giả có byte không phải UTF-8: rc 0, tải 1, thay byte. **Đóng tái hiện cũ của output agy**; lỗi giải mã `/proc` mới thuộc F13. |
| F08 / D2 | `quick`: `D2`; suite mutant D2 | Vắng CLAUDE_ENV_FILE: rc 0; danh sách tệp đúng `home/.gemini/antigravity-cli/settings.json`. Đạt ngoại lệ đã duyệt; không nêu lại F08. Suite 40/40 có mutant `D2_ghi_cwd_khi_khong_dat_bien`. |

## Bảng đo

`run_checks.py` tự đặt môi trường cô lập như ENV; mỗi log có JSON chứa argv, cwd, rc và thời gian.

| Hạng mục | Lệnh | Output / kết quả |
|---|---|---|
| Helper head | `ENV python3 evidence/run_checks.py suites` → `head-cloud.log` | rc 0; `CA: 25/25 dat`; `DOT BIEN: 40/40 bi giet dung ly do`; `TU KIEM PHAN HANG: DAT (4 dot bien)`; `TONG: DAT`; 180.838 s. |
| Setup head | Cùng lệnh → `head-setup.log` | rc 0; `DOT BIEN: 12/12 bi giet dung ly do`; `13/13`. |
| Setup base | Cùng lệnh → `base-setup.log` | rc 0; `DOT BIEN: 8/8 bi giet dung ly do`; `11/11`. Head tăng đúng 2 ca E. |
| Mẫu đăng ký F1 | `ENV python3 evidence/audit.py` → `registry_*` | Dùng chính `MOI["ops/cloud_agent_creds_test.py"]` và `bang_chung_xanh` của head: log suite thực `accepted=true`; 0/0 ca, 0/0 mutant, 24/25 ca, 39/40 mutant, tự kiểm DO đều `accepted=false`. |
| H1 sau pip thật | `ENV python3 evidence/probes.py mutations` → `H1_khoi_ngay_sau_tieu_de_truoc_pip` | `GIET`, `DO:h1_vi_tri_khoi_trong_hook:khối ở dòng 237–241, phải sau 505 và trước 580`. Ca gốc xanh trước đột biến. |
| Phạm vi / kích thước | `ENV python3 evidence/audit.py` → `final_identity` | Đúng 8 đường dẫn write set, +659/-7; dưới trần +700 của chỉ thị hiện hành. |
| Whitespace / Bash | `ENV python3 evidence/run_checks.py gates` → `diff-check.json`, `bash-hook.json`, `bash-setup.json` | `git diff --check 97120d3c HEAD`, `bash -n .claude/hooks/session-start.sh`, `bash -n ops/codex_cloud_setup.sh`: đều rc 0, output rỗng. |
| Ruff F, hai tệp mới | Cùng lệnh → `ruff-new.json` | `/root/.local/bin/ruff check --no-cache --select F ops/cloud_agent_creds.py ops/cloud_agent_creds_test.py`: rc 0, `All checks passed!`; `ruff --version` → `ruff 0.16.9`. Đây là phép lint, không phải kiểm contract pin CI. |
| Ruff F, hai `.py` còn lại | Cùng lệnh → `ruff-head.json`, `ruff-base.json` | Cả hai rc 1, cùng một F401 `shutil imported but unused` trong setup test, dòng head/base 13/12; delta 0. File đăng ký không có lỗi F. |
| Doctrine | Cùng lệnh → `doctrine.json` | `python3 .claude/dev/packet_loop.py doctrine-scan --root .`: rc 0, `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine`. |
| J1 | Cùng lệnh → `manifest.json`; `audit.py` → `J1` | `python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json`: rc 0, `ok=true`, expected/checked 195/195, `errors=[]`, `package_hash_match=true`. |
| R1 / R2 nội dung hiện có | `ENV python3 evidence/audit.py` → `R1_*`, `R1_R2` | Tiêu đề A0.4e head/base 1/0; mục 21 dòng (tính cả dòng trống cuối); đủ từng cụm yêu cầu theo bảng đếm; mẫu credential 0. Chưa đo đột biến cần dựng nội dung nhạy cảm. |

## Finding còn mở

- [P2] **F09 `argv-boundaries-still-unchecked`**: `ops/cloud_agent_creds_test.py:282`, `:287`; `ops/codex_cloud_setup_test.py:246`, `:251` — **Lệnh:** `ENV python3 evidence/probes.py mutations` và `ENV python3 evidence/probes.py argv_control` — **Output:** `H_argv_bracket_collision` SỐNG tại H1/H2; `E_argv_bracket_collision` SỐNG tại E1/E2. Đối chứng JSON ghi bản nguyên nhận `["ops/cloud_agent_creds.py","nap"]`, mutant nhận `["ops/cloud_agent_creds.py][nap"]`. Bộ ghi `printf "[%s]" "$@"` biến cả `["a","b"]` và `["a][b"]` thành `[a][b]`, nên chưa so được nguyên danh sách argv. Mutant chạy thật Bash, không sửa assertion hay giả mạo tệp nhật ký. **Hướng vá:** ghi argv theo định dạng không va chạm, như JSON array hoặc NUL giữa các đối số và ranh giới lần gọi riêng; so cả argc, byte từng đối số và thứ tự lần gọi. Thêm ca va chạm `][` bên cạnh mutant gộp dấu cách hiện có. Đây là lỗ chốt hồi quy kế thừa F05/F09, không phải bằng chứng lời gọi hiện tại của head đang sai.

  Neo/thay đã chạy cho setup:

  ```sh
  # Gốc
  "$PY" ops/cloud_agent_creds.py nap || true
  # Đột biến
  set -- ops/cloud_agent_creds.py nap; "$PY" "$1][$2" || true
  ```

  Với hook, thay `"$PY" "$GOC/ops/cloud_agent_creds.py" nap` bằng `set -- "$GOC/ops/cloud_agent_creds.py" nap; "$PY" "$1][$2"`; giữ phần pipeline/guard. Hai ca cấu trúc vẫn thấy token ở `set --`, còn hai ca hành vi bị va chạm serialization. Phạm vi “SỐNG” là các ca đích đã ghi, không phải tuyên bố toàn bộ runner đột biến trên nguồn đã thay đều xanh.

- [P2] **F12 `bootstrap-timeout-drops-diagnostics`**: `ops/cloud_agent_creds.py:53`, `:56`, `:57`, `:82` — **Lệnh:** `ENV python3 evidence/probes.py cleanup_log` — **Output:** rc 0, chỉ `agent_creds: KHÔNG ĐO ĐƯỢC — bootstrap quá 0.3 s, KHÔNG dừng được`; `communicate_trace` cho thấy **cả hai** ngoại lệ `TimeoutExpired.output` chứa dòng stdout, dòng stderr có sentinel giả và dòng agent cũ. Parent chết, con/cháu giữ pipe: `alive=[false,true,true]`. Phép thử tiêm lỗi killpg và đặt `HAN_DON=0.2` để rút ngắn; không phải kết luận killpg thật tự nhiên lỗi. `_giet_nhom` nuốt ngoại lệ thu output, giữ `ra=b""`; `nap` cũng không lấy output từ ngoại lệ đầu tiên. **Hướng vá:** giữ phần output đã thu được khi lần communicate cuối quá hạn/lỗi; dùng ngoại lệ ban đầu làm phương án dự phòng khi cần. Đi qua cùng bộ che/lọc, tránh nối lặp hai bản tích luỹ. Ca hồi quy phải đòi hai dòng chẩn đoán đã che xuất hiện đúng một lần, dòng agent cũ biến mất, đúng một dòng trạng thái và rc 0 ngay cả khi hậu kiểm báo không dừng được. Nhánh timeout dọn thành công đã được vá; nhánh này vẫn là F12.

- [P2] **F13 `group-recheck-incomplete-proc`**: `ops/cloud_agent_creds.py:44`, `:47`, `:48`, `:49`, `:50`, `:61` — **Lệnh:** `ENV python3 evidence/probes.py processes`, `proc_matrix`, `encoding` — **Output và hai biểu hiện:** (a) `nap_fault_permission` và `nap_fault_hidden`: rc 0, in `đã dừng` dù `alive=[false,true,true]`. Lỗi signal được tiêm để chỉ cha chết; sau đó tiêm PermissionError khi đọc stat của con/cháu hoặc ẩn chúng khỏi danh sách `/proc`. `_nhom_song` biến “không thấy/không đọc được” thành False. Đối chứng cùng lỗi signal nhưng `/proc` đọc đầy đủ cho `KHÔNG dừng được`. (b) Không cần mock lỗi đọc: một tiến trình fixture **khác nhóm bootstrap** có tên chứa byte không phải UTF-8 làm `_nhom_song` ném `UnicodeDecodeError`; CLI `nap` trên bootstrap giả thoát **rc 1, stdout rỗng**, không có dòng trạng thái dù ba PID bootstrap đã chết. Stack trace kết thúc tại `f.read_text()` dòng 49 trong [encoding.jsonl](evidence/encoding.jsonl). **Hướng vá:** giữ thiết kế `/proc` đã được chủ kho chọn nhưng làm kết quả ba trạng thái đáng tin: phân biệt tiến trình biến mất với quyền/lỗi đọc/dữ liệu không đủ, chỉ xác nhận chết khi có bằng chứng đủ; không coi danh sách rỗng sau `killpg(...,0)` thành bằng chứng cả nhóm chết. Đọc stat theo byte để tên tiến trình không phụ thuộc UTF-8; mọi nhánh không xác minh được phải trả trạng thái không xác định, không phá hợp đồng rc 0/một dòng của `nap`. Bổ sung đối chứng live/zombie, lỗi quyền, danh sách bị che/không đầy đủ, không có `/proc`, tên không UTF-8 và các mutant nới chốt. **LẦN THỨ TƯ của cùng hình dạng F01/F03/F11**, không reset lịch sử bằng ID F13.

### Bảng nối lớp

| Lớp nguyên nhân | Lịch sử / nguồn | Biểu hiện còn mở | Cách kiểm đóng lớp |
|---|---|---|---|
| Ranh giới argv không được so đầy đủ | F05 lượt 1 → F09 lượt 2 → F09 lượt 3 | Va chạm `[a][b]` | Đối chứng argv độc lập + H2/E2 giết cả gộp dấu cách và va chạm delimiter. |
| Giết/kiểm lại nhóm tiến trình | F01/F03 lượt 1 → F11 lượt 2 → F13 lượt 3; S5 đã ghi nhận ba lần trước | Xác nhận sai khi `/proc` không đầy đủ; ngoại lệ giải mã phá `nap` | Giữ đo cả nhóm; các lỗi đọc/ẩn/không có proc không được báo thành công; ca tên byte lạ vẫn rc 0, một trạng thái. |
| Mất log ở nhánh timeout | F12 lượt 2 → F12 lượt 3 | Lần thu output thứ hai quá hạn | So log đầu vào/đầu ra có che, đúng số lần và đúng một trạng thái trên cả hai đường dọn. |

Có 3 lớp còn mở, 4 biểu hiện (hai biểu hiện trong F13); mức cao nhất mỗi lớp là P2. Không nâng “suite xanh” thành “đã vá thật” cho các lớp còn phản chứng.

## Đột biến và biên bổ sung

Lệnh `ENV python3 evidence/probes.py mutations` ghi [mutations.jsonl](evidence/mutations.jsonl). Với helper, `chay_dot_bien` chạy ca gốc trước; chỉ xếp `GIET` khi rc 3 và có đúng `DO:<ca đích>:`. Với setup, script cũng chạy ca gốc rồi chỉ nhận lớp `ChotCa`. Lỗi harness/vô can không được tính là giết.

| Đột biến / biên | Output | Diễn giải |
|---|---|---|
| Va chạm argv `][` | H1/H2/E1/E2 `SONG_SOT` | Hai danh sách argv khác nhau có cùng chuỗi ghi; F09. |
| `_nhom_song` luôn False | A4 `SONG_SOT`, A9 `GIET`, B10 `SONG_SOT` | A9 mới đã bắt được bỏ hậu kiểm trên nhóm còn sống, khi `/proc` đọc được. Không tuyên bố mutant này sống qua toàn bộ bộ ca. |
| Tính zombie là còn sống | A4/A9/B10 đều `SONG_SOT` | Các ca thực tế không giữ một trạng thái zombie ổn định để phân biệt chốt này. Đối chứng `proc_matrix` riêng: live → True, zombie → False trên head. Không suy rằng head xử lý zombie sai. |
| Bỏ vòng chờ hậu kiểm (`and False`) | A9 `SONG_SOT` | A9 chỉ đòi kết luận “không dừng được” khi con còn sống liên tục, không kiểm khoảng chờ. Không tự coi bỏ thời gian chờ là lỗi sản phẩm khi kết luận vẫn thận trọng. |
| Bỏ kiểm dấu phân cách A3 | `SONG_SOT` | Sáu ca A3 chưa có trạng thái hợp lệ nhưng thiếu ` — `. Đây là mutant kế thừa từ hồ sơ hai lượt trước; không phải lỗi parser mới được chứng minh trên head. |
| Bỏ `isreg` B6 | `SONG_SOT` | Các fixture B6 hiện có vẫn không tạo agy; assertion đo hậu quả không tách được điều kiện loại member khỏi lỗi của thao tác đọc tar. Chỉ tái dùng fixture có sẵn; không suy ra khai thác tar trên head. |
| Token phiên bản bổ sung (`quick`) | `v1.4.12`, `x1.4.12`, `1.4.12-rc1`, `1.4.12+build`, `1.4.12.0`: tải 1/thay tệp; `(1.4.12)` và `1.4.12,`: tải 0 | Đúng quy tắc token/dấu phân cách hiện tại trong các input đã đo. Không dùng kết quả giả để xác nhận định dạng agy thật. |
| Không có `/proc`, lỗi quyền `killpg(...,0)` (`proc_matrix`) | Trả None | Nhánh này giữ trạng thái không xác định, không xác nhận chết. Khác lỗi quyền đọc từng stat đang bị nuốt, F13. |
| Stat bị lỗi quyền, OSError, danh sách rỗng, stat cụt (`proc_matrix`) | Trả False; byte không UTF-8 → `UnicodeDecodeError` | Bằng chứng đơn vị cho F13. Fixture biến mất trả False cũng được ghi; không coi riêng ENOENT do tiến trình biến mất là lỗi. |
| Thứ tự dọn (`proc_matrix`) | `killpg(123,9)` → `communicate(10)` → `poll` → `recheck`; `stopped=true`, output `output` | Thứ tự giết/thu/hậu kiểm đúng trên đối chứng. |
| Hạn `HAN_DON` (`proc_matrix`) | Đặt 0.2 s: elapsed 0.401 s, `stopped=false`, output rỗng | Thu pipe và vòng hậu kiểm có hai ngân sách nối tiếp, không phải một deadline chung 0.2 s. Ghi rõ giới hạn đo; chưa nâng riêng thành finding vì đặc tả không chốt tổng hạn dọn 10 s. Phần mất output thuộc F12. |

## Giới hạn và bàn giao

**KHÔNG ĐO ĐƯỢC trong lượt này:** G1 (toàn bộ `tl.py --selftest` head/base), G2 (toàn `launcher.py doctor`), L1 (required CI jobs trên exact SHA, không có biên nhận được cung cấp), M1/M2 LIVE, agy thật/enum `gemini`/hiệu lực tắt auto-update, CLAUDE_ENV_FILE trong phiên cloud thật, việc gỡ secret Codex sau setup, thời gian bootstrap thật, tarball thật sáu nền, Darwin/Windows thật. Kết quả đồ giả không thay cho các mục này. G3/J1 và các cổng được yêu cầu rõ trong prompt đã có phép đo ở bảng trên.

R2 đã quét văn bản hiện có; **KHÔNG ĐO ĐƯỢC** phản chứng cần dựng nội dung nhạy cảm. Hướng thử chỉ mô tả: bên được phép cung cấp fixture phù hợp scanner trong bản sao, đòi đúng ca R2 đỏ. Không tự dựng nội dung ấy trong lượt này. Phép B6 chỉ dùng fixture sẵn trong bộ test; việc đếm tệp trong fixture không chứng minh mọi đường ghi ngoài fixture.

Artifact tái hiện: [run_checks.py](evidence/run_checks.py), [probes.py](evidence/probes.py), [audit.py](evidence/audit.py), các log/JSON/JSONL được dẫn ở trên. Hướng vá là bàn giao cho executor; không áp bản sửa vào kho được review.

Ngưỡng theo prompt: approve chỉ khi không còn P0/P1/P2/P3. Ba P2 trên chặn approve. Verdict này **không cấp quyền merge/land**.
