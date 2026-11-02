Verdict: request_changes
Reviewed commit: 49eb161aad2945ef2de647cd8a4c5805c18e5ab0
Spec sha256: 67b448acc825fdd29f118c3b9082583773b4ad218a7c83ab4db496daa8f26d81

**Kết luận:** request_changes. Hai bộ test khai trong prompt đều xanh với đúng số lượng, nhưng có 8 finding còn mở: 6 P2 và 2 P3. Helper hiện tại để sót tiến trình con ở đường kiểm phiên bản agy; một timeout hữu hạn quá lớn làm `nap` rc 1 và để bootstrap còn sống; đầu ra phiên bản không giải mã được khiến agy hỏng không được cài lại. Các phản chứng còn xác nhận thiếu phép đo nhóm tiến trình, stderr và lời gọi thật trong test. D2 không đạt nguyên văn và mâu thuẫn với yêu cầu tạo settings. Bằng chứng chi tiết ở các bảng và finding bên dưới.

**Neo và điều kiện đo.** Base `97120d3c76ebb7c3eda4b585ff46f1c51e30c91b`; tree head `24121aac5944ea573100fd07f5901d558a789ebb`. `sha256sum SPEC.md cay-kho/ops/specs/cloud-setup-p2b-wire-r1.md` trả cùng băm ở dòng 3. `/tmp/.git` tồn tại và rỗng (`list(Path('/tmp/.git').iterdir())` ⇒ `[]`). Đã đặt `git -C cay-kho config core.abbrev 7` trước test; các lệnh đo qua [run.py](evidence/run.py) đặt `PYTHONDONTWRITEBYTECODE=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_SYSTEM=/dev/null`, HOME tạm và môi trường không mang credential. Bootstrap/agy trong các phản chứng đều là đồ giả; tarball do fixture tạo. Không tải hoặc chạy agy thật, không chạy bootstrap thật.

Head/base phục vụ selftest nằm trong `evidence/head-copy` và `evidence/base`, clone cục bộ bằng `git clone --quiet --shared cay-kho <đích>`; base checkout detached đúng OID trên. Đột biến chỉ ghi trên bản sao/tệp tạm ngoài `cay-kho`. Cây được review sạch ở đầu và cuối: lệnh `git -C cay-kho status --porcelain=v1 --untracked-files=all --ignored`, `git diff --stat` và `git diff --cached --stat` đều không có output; HEAD/tree không đổi (`final_identity` trong [final-checks.log](evidence/final-checks.log)). Đây là đối chiếu hai thời điểm, không phải khẳng định giám sát mọi syscall.

**Bảng đo cổng.** Lệnh bắt đầu tại thư mục chứa `VERDICT.md`; mỗi `evidence/<tên>.json` ghi argv, cwd, rc và thời gian thật, `evidence/<tên>.log` giữ output.

| Phép đo | Lệnh | Output / kết luận |
|---|---|---|
| Helper head | `python3 evidence/run.py head-cloud cay-kho python3 ops/cloud_agent_creds_test.py` | rc 0; `CA: 22/22 dat`; `DOT BIEN: 27/27 bi giet dung ly do`; `TU KIEM PHAN HANG: DAT (4 dot bien)`; `TONG: DAT`; không có ca bỏ qua |
| Setup head | `python3 evidence/run.py head-setup cay-kho python3 ops/codex_cloud_setup_test.py` | rc 0; `DOT BIEN: 10/10 bi giet dung ly do`; `13/13` |
| Setup base | `python3 evidence/run.py base-setup evidence/base python3 ops/codex_cloud_setup_test.py` | rc 0; `DOT BIEN: 8/8 bi giet dung ly do`; `11/11`; head tăng đúng 2 ca |
| Release J1 | `python3 evidence/run.py release cay-kho python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | rc 0; `ok=true`, `expected_file_count=195`, `checked_file_count=195` |
| J1 phản chứng | `python3 evidence/final_checks.py` | Thêm một byte newline vào RUNBOOK ở bản sao rồi verify: rc 2, `ok=false`, `package_hash_match=false`; hoàn nguyên bản sao trong `finally` |
| Đăng ký CI đối chứng | `python3 evidence/run.py registry-control evidence/head-copy python3 .claude/dev/ci_dang_ky_test.py` | rc 0; `PHẢN CHỨNG: 1070/1070 đỏ đúng`; `TỔNG: ĐẠT` |
| Xoá dòng đăng ký | Trên bản sao, xoá duy nhất dòng bắt đầu `"ops/cloud_agent_creds_test.py":`, rồi `python3 evidence/run.py registry-removed evidence/head-copy python3 .claude/dev/ci_dang_ky_test.py` | rc 1; `ĐỎ: test sống chưa đăng ký: ops/cloud_agent_creds_test.py`; `ĐĂNG KÝ: 29/28`; `TỔNG: ĐỎ`; đã hoàn nguyên bản sao |
| G1 head | `python3 evidence/run.py head-selftest evidence/head-copy python3 scripts/tl.py --selftest` | rc 0; `== tl selftest 1774/1774 ==` |
| G1 base | `python3 evidence/run.py base-selftest evidence/base python3 scripts/tl.py --selftest` | rc 0; `== tl selftest 1774/1774 ==`; `final_checks.py` đối chiếu danh sách kết quả: 0 ca đỏ mới |
| G2 | `python3 evidence/run.py doctor-head cay-kho python3 .claude/dev/launcher.py doctor` | rc 0; `DUNG_DUOC hook-phien du nang luc so voi master (+agent-creds-bootstrap,agy-ghim moi hon)` |
| G3 | `python3 evidence/run.py doctrine cay-kho python3 .claude/dev/packet_loop.py doctrine-scan --root .` | rc 0; `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine` |
| K1 hai tệp mới | `python3 evidence/run.py ruff-new cay-kho ruff check --no-cache --select F ops/cloud_agent_creds.py ops/cloud_agent_creds_test.py` | Ruff 0.16.9; rc 0; `All checks passed!` |
| K1 các Python còn lại | `python3 evidence/run.py ruff-head cay-kho ruff check --no-cache --select F ops/codex_cloud_setup_test.py .claude/dev/ci_dang_ky_test.py`; lặp với `ruff-base evidence/base` | Cả hai rc 1, cùng một F401 `shutil imported but unused` trong setup test; delta lỗi F = 0. Không gọi kết quả này là lint sạch tuyệt đối |
| K2 và hiện vật | `python3 evidence/audit.py` / `git -C cay-kho diff --numstat 97120d3c HEAD` | `exact_write_set=true`, 8 tệp, +599/-7; DIFF.patch và numstat.txt bằng byte của phép đo git |
| Whitespace | `python3 evidence/run.py diff-check cay-kho git diff --check 97120d3c76ebb7c3eda4b585ff46f1c51e30c91b HEAD` | rc 0; output rỗng |
| Cú pháp hook | `python3 evidence/run.py bash-hook-check cay-kho bash -n .claude/hooks/session-start.sh` | rc 0; output rỗng |
| Cú pháp setup | `python3 evidence/run.py bash-setup-check cay-kho bash -n ops/codex_cloud_setup.sh` | rc 0; output rỗng |

Lần doctor đầu trên bản sao thiếu ref `origin/master` chỉ trả `KHONG_DO_DUOC hook-phien`; không dùng nó làm bằng chứng đạt. Dòng G2 trên được đo lại trên đúng `cay-kho`, có ref base đã xác minh.

**Đối chiếu từng tiêu chí.** Ký hiệu lệnh để bảng ngắn: **Q** = `python3 evidence/audit.py` ([log](evidence/audit.log)); **X** = `python3 evidence/edge_counts.py` ([log](evidence/edge-counts.log)); **M** = `python3 evidence/probes.py` ([log](evidence/probes.log)); **S** = `python3 evidence/safety.py` ([log](evidence/safety.log)); **Z** = `python3 evidence/final_checks.py` ([log](evidence/final-checks.log)). Các script tự cô lập môi trường như runner. `Q / tên_ca` nghĩa là Q thực sự gọi hàm đó và ghi rc, không chỉ tìm tên trong mã.

| Tiêu chí | Mã / phép đo | Output và giới hạn |
|---|---|---|
| A1 | Q `a1_thieu_khoa_khong_goi_tl`; X hai biến thể | Vắng và rỗng: từng ca rc 0, bootstrap 0 lần, đúng 1 dòng `BỎ QUA — thiếu TL_MASTER_KEY` |
| A2 | Q `a2_loc_dong_agent_cua_bootstrap` | rc 0; một dòng chuẩn với `rev=7`, dòng thường giữ lại, dòng `[bootstrap] agent_creds:` gốc bị lọc |
| A3 | Q `a3_bang_sau_ca_hop_dong`; X | Sáu ca đều rc 0, đúng 1 dòng; lần lượt lý do `rc=2`, `rc=3`, hợp đồng/2 dòng, hợp đồng/trạng thái lạ, `FileNotFoundError`, `KHÔNG CẤU HÌNH ... rc=1`. Ngoài bảng, mutant bỏ kiểm dấu phân cách còn sống (M) |
| A4 | Q `a4_qua_han_giet_ca_nhom`; M | Ca gốc rc 0. Đối chứng riêng có cha+con: head chết cả hai; mutant chỉ giết cha sống qua ca A4, để con sống. `_con_song` coi trạng thái `/proc/.../stat` `Z` là chết. F03 |
| A5 | Q `a5_doc_timeout` | `abc`, `-5`, `0`, `inf` đều về 180; rc 0. Số hữu hạn vượt giới hạn hệ thống chưa được xử lý: F02 |
| A6 | Q `a6_argv_va_trinh_thong_dich` | rc 0; so nguyên argv `bootstrap --env code --no-nlm` và realpath interpreter với `sys.executable` |
| A7 | Q `a7_che_master_key`; M | Ca hiện tại rc 0 nhưng fixture chỉ in stdout. M phát hiện mutant stderr đi thẳng vẫn sống và làm lộ sentinel. Head che được cả hai kênh khi bổ sung fixture stderr. F04 |
| A8 | Q `a8_nap_luon_rc0`; S | rc bootstrap 0–4 và timeout thường cho nap rc 0; `nap --la` rc 2, không gọi tl. S đo `2147484` ⇒ nap rc 1, không có dòng chuẩn, bootstrap còn sống. F02 |
| B1 | Q `b1_chua_co_thi_tai_va_ghi` | rc 0; tải 1, nội dung agy bằng payload giả, có bit thực thi |
| B2 | Q `b2_sha512_lech_khong_ghi` | rc 0; không tạo bản mới khi băm lệch, bản cũ giữ nguyên byte; có `agy: ✗ sha512 lệch` |
| B3 | Q `b34_dung_ban_khong_tai_lech_hoac_hong_thi_thay` | Bản giả 1.4.12 rc 0 ⇒ tải 0 |
| B4 | Cùng ca b34; S | Lệch 1.4.13 và version rc 1 ⇒ tải 1, thay tệp. S cho version output không phải UTF-8 ⇒ tải 0, không thay; timeout version để con sống. F01, F07 |
| B5 | Q `b5_nen_ngoai_bang_va_d2_khong_env_file` | rc 0; `CHƯA HỖ TRỢ freebsd_amd64`; tải 0 |
| B6 | Q `b6_tarball_doc_tu_choi`; X ba ca riêng | `../x`, hai member, symlink: từng ca rc 0, không tạo agy; dưới fixture chỉ có settings. M bỏ kiểm số member / tên ⇒ `GIET`; bỏ `isreg` ⇒ `SONG_SOT` vì thư viện tự lỗi và wrapper giữ không ghi agy. Giới hạn: `s.tep()` chỉ quét trong fixture, không giám sát mọi đường ghi bên ngoài |
| B7 | Q `b7_khong_goi_agy_install` | rc 0; log không rỗng và mọi lời gọi đều `--version`, không có `install` |
| B8 | Q `b8_hang_ghim_dung_spec`; X | rc 0; SHA spec đúng; đúng 6 khoá; từng tuple URL/sha512 bằng bảng đọc trực tiếp từ spec đã ghim; `AGY_VER=1.4.12` |
| B9 | Q `b9_luat_chon_nen` | rc 0; bốn vế Linux x86_64, Linux aarch64 musl, Darwin arm64, Linux i686 ngoài bảng được kiểm riêng |
| C1 | Q `c13_gop_model_provider_khong_ghi_khoa` | rc 0; dict có `a=1` giữ `a`; chưa có settings thì tạo đúng provider |
| C2 | Q `c2_settings_khong_phai_object_khong_dung` | `[1,2]` và JSON lỗi: từng ca rc 0, sha256 trước/sau bằng nhau, có cảnh báo |
| C3 | Q `c13_gop_model_provider_khong_ghi_khoa` | rc 0; đặt sentinel cho cả GEMINI_API_KEY/GOOGLE_API_KEY, settings không chứa sentinel; so dict toàn bộ |
| D1 | Q `d1_env_file_dung_mot_dong` | rc 0; chạy hai lần, đúng 1 export mới, giữ `export FOO=1` |
| D2 | Q ca b5; X `D2_literal` | Ca test rc 0 nhưng `CLAUDE_ENV_FILE` vắng vẫn tạo `home/.gemini/antigravity-cli/settings.json`; không đạt nguyên văn “không tạo tệp nào ở cwd/HOME”. F08 |
| H1 | Q `h1_vi_tri_khoi_trong_hook`; S | Head đủ marker, vị trí, thứ tự, số chuỗi trong/ngoài; base 0. S xác nhận thực gọi nap rồi cai-agy. M chứng minh test H không bắt được bỏ gọi/sai path. F05 |
| H2 | Q `h2_khoi_song_sot_set_e`; S; M | Block thật với PY giả rc 3 vẫn rc 0; mọi dòng S có prefix, stderr helper được gom. Bỏ guard cai-agy ⇒ ca đỏ đúng. Thiếu bash trên POSIX lại BoQua: F06 |
| H3 | Q `h3_ten_nang_luc` | rc 0; hai tên mới có mặt, tập tên cũ là tập con |
| E1 | Setup head/base và S | Head 1 nap trong main sau pip, không cai-agy; base 0; S ghi đúng argv. Comment lời gọi / sai đường dẫn vẫn qua E1, E2: F05 |
| E2 | Setup head; S | Dòng thật, PY giả rc 3, `set -euo pipefail`: rc 0. Không có chốt đếm lời gọi trong ca hiện tại: F05 |
| F1 | Q `F1_pattern`; registry-control/removed | Log thật khớp MOI qua `bang_chung_xanh=true`; 0 ca, 0 mutant, lệch số ca, 1 mutant sống và selfcheck DO đều false. Xoá đăng ký làm rc 1. Mẫu vẫn nhận số tổng đã trừ ca POSIX bị skip: F06 |
| F2 | Z `F2` | AttributeError qua except đổi thành AssertionError ⇒ `TIN_DUNG_GIA`; assertion ca khác ⇒ `TIN_DUNG_GIA`; assertion trần ⇒ `TIN_DUNG_GIA`; chỉ thêm chú thích ⇒ `SONG_SOT` |
| F3 | head-setup/base-setup | 13/13 so 11/11, tăng đúng E1/E2; mutant 10/10 so 8/8 |
| R1 | Q | Tiêu đề head 1, base 0; mục 22 dòng ≤60. Từng cụm sau chuẩn hoá đoạn: TL_MASTER_KEY 5; agent-creds-exec --gemini 1; agent_creds: 2; bốn trạng thái mỗi thứ 1; secrets-keygen 1; agent-creds-set 2; Codex Cloud 4. Xoá trạng thái trên bản văn tạm ⇒ phép kiểm false |
| R2 | Q | 0 chuỗi khớp ba mẫu cấm. Không tự dựng nội dung giống credential để đột biến; vế đột biến R2: KHÔNG ĐO ĐƯỢC |
| J1 | release; Z | ok true, 195/195; thêm một byte trên bản sao ⇒ rc 2, ok false |
| G1 | Hai selftest; Z | head/base 1774/1774, delta ca đỏ mới 0 |
| G2 | doctor-head | `hook-phien` đủ năng lực so với master |
| G3 | doctrine | rc 0, 10 tệp, 0 vi phạm |
| K1 | Ba phép lint ở bảng cổng | Hai tệp mới 0; hai tệp Python khác cùng 1 F401 ở base/head, delta 0 |
| K2 | Q | Chính xác 8 đường dẫn của write_set; +599/-7 |

**Finding còn mở.** Mỗi finding có slug riêng; đây là lượt 1, không có finding lượt trước để đối chiếu. Hướng vá là đề nghị cho executor, chưa được áp vào kho.

- [P2] F01 `agy-version-child-lifetime`: `ops/cloud_agent_creds.py:94–99` — tái hiện `python3 evidence/safety.py`, dòng `B4_version_timeout_children` — output `rc=0`, khoảng `15.02` giây, `downloads=1`, `alive=[false,true]`. `_ban_khop()` dùng `subprocess.run(timeout=15)` chỉ dừng tiến trình trực tiếp; agy giả sinh một tiến trình con cùng nhóm rồi ngủ, và tiến trình con còn sống khi `cai-agy` trả về. Đây là lỗi trên helper nguyên trạng. Hướng vá: chạy probe version trong nhóm riêng, khi quá hạn giết/thu hồi cả nhóm và kiểm trạng thái các PID; thêm fixture có tiến trình con, dọn nhóm trong finally. Không chỉ kiểm lại PID cha.

- [P3] F02 `finite-timeout-overflow`: `ops/cloud_agent_creds.py:22–27,62–67` — tái hiện `python3 evidence/safety.py`, dòng `A8_timeout_overflow_leaves_child` — `TL_CLOUD_BOOTSTRAP_TIMEOUT_GIAY=2147484` được chấp nhận là hữu hạn/dương nhưng output `rc=1`, `stdout=""`, `OverflowError: timeout is too large`, `child_alive=true`. `1e300` cũng cho rc 1 trong M. Nhánh communicate chỉ bắt TimeoutExpired, nên mất bảo đảm luôn rc 0/đúng một dòng và không dọn tiến trình đã mở. Hướng vá: xử lý giá trị ngoài khả năng timeout của hệ thống bằng mặc định 180 hoặc cơ chế đợi chia khoảng phù hợp hợp đồng, đồng thời dọn nhóm ở mọi đường lỗi sau Popen rồi in một trạng thái không đo được. Bổ sung ca timeout hữu hạn quá lớn; mức P3 vì cần cấu hình bất thường.

- [P2] F03 `group-kill-oracle-missing`: `ops/cloud_agent_creds_test.py:92–102` — tái hiện `python3 evidence/probes.py`, dòng `A4_kill_parent_only` — thay `os.killpg(p.pid, signal.SIGKILL)` bằng `p.kill()` được `SONG_SOT`. Ca A4 chỉ tạo một tiến trình rồi kiểm PID ấy. Đối chứng riêng trong cùng script tạo cha+con: head `alive=[false,false]`; mutant `alive=[false,true]`, cả hai vẫn in “đã dừng”. Hướng vá: để tl giả sinh con cùng nhóm, ghi cả hai PID, đo cả hai với zombie tính chết; đăng ký mutant chỉ giết cha và bảo đảm nó chết đúng ở chốt tiến trình con. Đây là thiếu phép đo của test; head giết nhóm đúng trong đối chứng timeout bình thường.

- [P2] F04 `stderr-redaction-oracle-missing`: `ops/cloud_agent_creds_test.py:46–53,111–114` — tái hiện `python3 evidence/probes.py`, `A7_stderr_direct` — thay `stderr=subprocess.STDOUT` bằng `stderr=None` vẫn `SONG_SOT`. TL_GIA chỉ ghi stdout nên điều kiện kiểm `k.loi` không thực sự thử kênh stderr. Fixture độc lập ghi sentinel và dòng trạng thái vào stderr cho head `master_leaked=false`, mutant `master_leaked=true`, `agent_lines=2`. Hướng vá: fixture có đầu ra riêng trên stdout và stderr; đo cả dòng thường lẫn agent trên từng kênh, gộp output của helper khi đếm/redact; thêm mutant để stderr kế thừa thẳng. Không có bằng chứng head hiện tại làm lộ master trong fixture đúng hai kênh.

- [P2] F05 `wire-call-positive-evidence-missing`: `ops/cloud_agent_creds_test.py:237–263`; `ops/codex_cloud_setup_test.py:230–251` — tái hiện `python3 evidence/probes.py` — `H_skip_nap` (thêm `:` trước lời gọi) và `H_wrong_path` đều H1/H2/H3 rc 0; `E_comment_nap` và `E_wrong_path` đều E1/E2 PASS. Regex tính cả chữ trong comment/đối số, PY giả không ghi argv, còn echo cuối vẫn tạo dấu thành công. Do đó lời gọi có thể mất hoặc sai đích mà các ca nghiệm thu mới vẫn xanh. Hướng vá: PY giả ghi nhật ký argv, kiểm đích helper, số lần và thứ tự nap/cai-agy; phải có bằng chứng cả khi fake rc 3. Dùng thực thi đoạn trích để phân biệt comment/lệnh rỗng; giữ kiểm vị trí riêng. Kết quả này nói về các ca H/E, không khẳng định toàn bộ runner đột biến vẫn xanh khi thay mất neo văn bản.

- [P2] F06 `posix-hook-skip-counted-green`: `ops/cloud_agent_creds_test.py:254–256,344–356`; mẫu MOI ở `.claude/dev/ci_dang_ky_test.py:59` — tái hiện `python3 evidence/audit.py` — với resolver bash trả None trên `LA_WINDOWS=false`, H2 trả `5, BO QUA ... không có bash dùng được`; `bang_chung_xanh` nhận bản tổng kết `CA: 21/21`, `DOT BIEN: 26/26`, `TONG: DAT` kèm dòng bỏ qua. Đây là phép đo nhánh skip và bộ nhận output, không phải lời khai đã chạy cả suite trên máy thiếu bash. SPEC H2 chỉ cho bỏ qua khi LA_WINDOWS. Hướng vá: thiếu bash trên POSIX phải là lỗi làm suite đỏ, không trừ khỏi mẫu; chặn skip không được phép trước tổng kết, giữ ngoại lệ Windows rõ ràng. Lượt head thực tế có bash và không bỏ qua.

- [P2] F07 `unreadable-version-does-not-reinstall`: `ops/cloud_agent_creds.py:94–99,152–159` — tái hiện `python3 evidence/safety.py`, `B4_invalid_utf8_version` — agy giả in một byte không giải mã UTF-8 được: `rc=0`, `downloads=0`, `replaced=false`, `agy: ✗ lỗi UnicodeDecodeError`. Lỗi giải mã không thuộc OSError/SubprocessError nên thoát khỏi `_ban_khop`, bị wrapper nuốt và bỏ luôn bước cài; trái yêu cầu version hỏng thì tải/thay. Hướng vá: bắt lỗi decode như kết quả kiểm phiên bản không hợp lệ, hoặc nhận bytes và giải mã với chính sách rõ ràng; trả False để đi tiếp tải có kiểm băm; thêm ca stdout/stderr không giải mã được.

- [P3] F08 `d2-acceptance-narrowed`: `ops/cloud_agent_creds_test.py:173–177` và SPEC dòng D2 — tái hiện `python3 evidence/edge_counts.py`, `D2_literal` — `claude_env_file_present=false`, `rc=0`, `files=["home/.gemini/antigravity-cli/settings.json"]`. Test gọi đây là D2 nhưng cho phép settings trong danh sách; SPEC nguyên văn cấm tạo mọi tệp ở cwd/HOME. Đồng thời C1/mục tiêu 3 yêu cầu tạo settings nên không thể sửa bằng cách ngừng tạo settings một cách máy móc. Hướng vá: làm rõ/điều chỉnh tiêu chí D2 qua revision được chấp thuận (ví dụ đo riêng `dat_env_file` không có biến, hoặc ghi rõ ngoại lệ agy/settings), rồi đo đúng tiêu chí đó. Không tự coi cách hiểu hẹp của executor là đặc tả đóng băng.

**Đột biến bổ sung ngoài DOT_BIEN.** Lệnh M; mỗi mutant helper chạy trên bản sao và ca gốc phải xanh trước khi phân hạng. Các mutant hook/setup chạy các ca mục tiêu với đường dẫn bản sao.

| Đột biến / ca đích | Output | Vì sao / nhận định |
|---|---|---|
| A4 chỉ giết PID cha / A4 | `SONG_SOT` | Không tạo/đo tiến trình con; F03 |
| A7 stderr đi thẳng / A7 | `SONG_SOT` | Fixture không ghi stderr; F04 |
| A3 bỏ `not sep` / A3 | `SONG_SOT` | Sáu input A3 không có trạng thái hợp lệ nhưng thiếu dấu ` — `. Head từ chối input thiếu dấu trong đối chứng; nên bổ sung dạng này vào phép đo hợp đồng |
| B6 bỏ điều kiện số member / B6 | `GIET` | Ca hai member tạo agy trái điều kiện, chốt B6 bắt được |
| B6 bỏ điều kiện tên / B6 | `GIET` | Ca `../x` bị ghi vào agy, chốt B6 bắt được |
| B6 bỏ `isreg` / B6 | `SONG_SOT` | Symlink fixture không có đích trong tar: extractfile lỗi, wrapper vẫn từ chối theo hậu quả không ghi. Không suy đây là chứng cứ khai thác thoát đường dẫn |
| Hook thêm `:` trước nap / H1–H3 | cả ba rc 0 | Không đo lời gọi; F05 |
| Hook sai đường dẫn helper / H1–H3 | cả ba rc 0 | PY giả bỏ qua argv; F05 |
| Hook bỏ guard cai-agy / H2 | `DO:h2... rc=3` | Bị giết đúng chốt sống sót set -e |
| Setup comment nap / E1–E2 | cả hai PASS | Regex đọc comment, echo XONG vẫn chạy; F05 |
| Setup sai đường dẫn / E1–E2 | cả hai PASS | Không kiểm argv; F05 |

M còn thử tên member `antigravity/`, `./antigravity`, `antigravity/../x`: từng ca rc 0, agy không tồn tại, có thông báo từ chối tarball. Hai dấu `agent_creds:` trong cùng một dòng chi tiết được head giữ như chi tiết của một dòng; không kết luận vi phạm điều khoản đếm số dòng chỉ từ số lần xuất hiện dấu này.

**Hành vi an toàn và giới hạn.** S đo lỗi tải và lỗi ghi giả: `cai-agy` rc 0, chỉ log lớp OSError; đo khối hook thật với fake rc 3: rc 0, log argv nap rồi cai-agy, `all_prefixed=true`, stderr rỗng. S chạy toàn hook với `CLAUDE_CODE_REMOTE` rỗng và `false`, project tạm: rc 0, `khong phai moi truong remote — bo qua`; helper không được gọi. Hook có ghi dấu vết cục bộ sẵn từ base, nên không suy “không ghi gì” khi remote khác true.

Trong ca stderr mở rộng của M, head không lộ TL_MASTER_KEY; C3 xác nhận không ghi sentinel Gemini/Google vào settings. Tuy nhiên **helper chỉ che TL_MASTER_KEY**: Z dùng bootstrap giả cố ý in sentinel Gemini cho `sentinel_forwarded=true`. Không có phép đo bootstrap thật in khoá Gemini, nên đây là giới hạn của cơ chế lọc, chưa phải bằng chứng rò khoá thật. Không khẳng định mọi output bootstrap đều được lọc secret. Các phép B6/X/M không quan sát thấy ghi lạ trong cây fixture; kiểm mọi đường ghi ngoài cây bằng giám sát hệ thống: KHÔNG ĐO ĐƯỢC. Không nhận phép quét `rglob` trong fixture là chứng minh toàn hệ thống không bị ghi.

Các phần sau **KHÔNG ĐO ĐƯỢC**: L1 (không có biên nhận required jobs trên exact SHA trong đầu vào được kiểm); M1/M2 LIVE; enum gemini được agy thật chấp nhận; hiệu lực AGY_CLI_DISABLE_AUTO_UPDATE của agy thật; CLAUDE_ENV_FILE trong phiên cloud thật; bí mật Codex được gỡ ở giai đoạn agent; thời gian bootstrap thật; tarball thật sáu nền; Windows. Các phần LIVE không được thay bằng đồ giả rồi nhận là đạt. Không tự dựng nội dung nhạy cảm cho phản chứng R2; hướng thử là chèn dữ liệu tổng hợp do executor được phép cung cấp rồi kiểm scanner đỏ.

Verdict này không cấp quyền merge/land. Các script/log trong `evidence/` là dữ liệu phản chứng để executor tái hiện, không phải bản vá đã áp vào kho.
