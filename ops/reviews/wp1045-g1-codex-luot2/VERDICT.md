Verdict: request_changes
Reviewed commit: b07adcc2c37215fcb152c94890b9c43f7032bd18
Spec sha256: 8e187b9130e18a757f4f24dfcea6761f688a5f69e21d17356b198b8cc5bd508e

**request_changes: còn 1 finding P3 về thiếu test khoá lỗi kiểm cuối trong lượt source.** Ba finding lượt 1 đã được đo lại và đóng. Hai mutant mới vẫn sống khi chạy toàn suite so với nền head; head hiện dừng đúng. Không phát hiện P0/P1/P2 trong phạm vi đã đo. Lệnh, output và giới hạn của từng kết luận ở các mục dưới.

Preflight: `git -C cay-kho rev-parse HEAD`, `sha256sum SPEC.md`, `git -C cay-kho diff --name-only 5e458f4 HEAD`, `git diff --check`: exact SHA/spec khớp; đúng hai tệp, diff-check rc=0. Chi tiết: [evidence/preflight.json](evidence/preflight.json). `/tmp/.git` tồn tại và rỗng; giữ nguyên để so tập ca đỏ head/base.

## ĐỐI CHIẾU LƯỢT TRƯỚC — cập nhật 1

Lệnh `env PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null python3 evidence/probe_behavior.py` chạy trên bản sao đủ cây head/base/daedfb7, xoá từng bản sau đo. [Log](evidence/behavior.log), [JSON](evidence/behavior.json).

- P2 `m2-bi-errexit-cat-truoc-thong-bao`: head DO tuỳ chọn, DO bắt buộc, bắt buộc vắng đều rc=3, stderr nêu đúng tên và `chua DAT sau khi cai`; round1 DO rc=2/stderr rỗng, vắng bắt buộc rc=3/stderr rỗng. Đã vá ở các phản chứng cũ.
- P3 `recipe-bat-errexit-bi-vo-hieu`: head/base recipe `set -e; false; echo CONTINUED` dừng rc=1, không ghi marker; round1 rc=0, ghi `CONTINUED`. Đã vá.
- Nhánh source sau lượt đầu thành công: công cụ kế tiếp DO (tuỳ chọn hoặc bắt buộc) head/base rc=2; bắt buộc vắng rc=3; recipe exit47 rc=47; recipe tự bật errexit rc=1. Cả head/base đều không chạy recipe thứ ba (`trace` rỗng). Chưa thấy lệch errexit trên head.
- Kết quả hai mutant từng sống được ghi ở cập nhật 2 bên dưới.

## ĐỐI CHIẾU LƯỢT TRƯỚC — cập nhật 2

`python3 evidence/run_mutants.py extra_source_no_cleanup extra_rc1_preserve_shape` (hai phép sửa được chạy trong lượt đầy đủ `python3 evidence/run_mutants.py`): cả hai nay **CHẾT đúng chốt hành vi**, mỗi mutant 11 PASS, 1 KILLED, 0 ERROR, 0 SKIP trong 12 ca r868/r1045.

- `extra_source_no_cleanup`: `r1045_bat_buoc_cong_cu_tuy_chon_thieu_khong_chan_cong_cu_sau` → `--bat-buoc (bo-chon-hong): bo lai thu muc tam sau hai luot source: ['cai_cong_cu.8SiCZZ']`.
- `extra_rc1_preserve_shape`: `r1045_bat_buoc_cong_cu_bat_buoc_hong_van_dung` → `--bat-buoc: cong cu bat buoc hong ma van di tiep: rc=1 GITHUB_PATH=[] `.

P3 `source-thieu-khoa-don-tam-va-ma-goc` đã đóng ở đúng hai mutant lượt trước. Head không còn thư mục tạm sau hai lượt source và batch recipe `exit 47` giữ rc=47 ([behavior.json](evidence/behavior.json)).

## Finding

- [P3] source-thieu-khoa-loi-kiem-cuoi: `.claude/dev/launcher_test.py:10358` (ca source lỗi chỉ ép recipe `exit 47`, chưa ép lỗi checker sau recipe rc=0; nhánh sản phẩm `ops/cai_cong_cu.sh:184`) — `python3 evidence/run_mutants.py extra_source_errexit_off_preserve_shape extra_source_final_error_swallowed` — mỗi mutant **12/12 PASS**, 0 ERROR/SKIP ở nhóm r868/r1045; probe độc lập trong cùng lệnh cho batch rc=2 nhưng `trace="THIRD\n"`, tức chạy công cụ thứ ba sau khi công cụ thứ hai DO. Head/base cùng probe rc=2 và trace rỗng. Mutant thứ nhất thêm `set +e` ngay sau chỗ khôi phục `set -e`, giữ chuỗi shape; mutant thứ hai thêm `|| true` chỉ vào checker lượt source. — Hướng vá: thêm ca batch ba công cụ, lượt đầu thành công, lượt hai recipe rc=0 nhưng checker DO/bắt buộc vắng, lượt ba ghi marker; đòi rc checker gốc và marker vắng. Neo cả hai mutant vào ca ấy. Giữ đối chứng tuỳ chọn vắng được đi tiếp, tránh vá test bằng quy tắc chặn mọi rc/không-DAT tuỳ chọn. Đây là lỗ khoá hồi quy trong test, **không phải head đang bật sai errexit**. Đã xác minh trên toàn suite: cả hai vẫn sống so với nền, cùng 13 ca đỏ/10 ca bỏ qua; xem mục đối chiếu toàn suite bên dưới. [Chi tiết](evidence/mutations.json).

## Đột biến đăng ký

Lệnh `python3 evidence/run_mutants.py`: **14/14 mutant đăng ký giết đủ 26/26 ca đích**, 0 ERROR, 0 SKIP. Mỗi mutant áp trên một bản sao đầy đủ riêng (có thư mục `.git`), đòi neo duy nhất, xoá ngay sau chạy. `TinHieuChotCa` mới được tính KILLED. Các lệnh tái hiện từng hàng: `python3 evidence/run_mutants.py <tên>`. [JSON gồm neo/thay và từng chốt](evidence/mutations.json).

| Mutant | Số ca đích bị giết | Chốt hành vi |
|---|---:|---|
| `wp858_sh_bo_kiem_ten_tran` | 2/2 | linux/git: ten tran da DAT ma van ghi GITHUB_PATH: rc=0 GITHUB_PATH='/tmp/lt_3w7uoh9s/goc/usr/bin' |
| `wp858_sh_chon_theo_ma_thoat` | 2/2 | linux/git: khong ung vien nao chay duoc ma van chon ('exit 0'): rc=3 GITHUB_PATH='/tmp/lt_acegf_ff/goc/usr/bin' |
| `wp1045_sh_ten_tran_ve_rc` | 2/2 | (a) vang PATH + ung vien tot ma khong chon ung vien: rc=3 GITHUB_PATH=[] cai_cong_cu: 'tuychon1045x' ten tran da DAT, giu nguyen PATH cai_cong_cu: 'tuychon1045x' chua DAT sau khi cai (trang_thai cua chinh no khac DAT; kiem-tra rc=0)  |
| `wp1045_sh_ung_vien_ve_rc` | 2/2 | (a) vang PATH + ung vien tot ma khong chon ung vien: rc=3 GITHUB_PATH=['/tmp/lt_g6yjm9rs/uv_tuychon1045x_rong'] cai_cong_cu: 'tuychon1045x' chua DAT sau khi cai (trang_thai cua chinh no khac DAT; kiem-tra rc=0)  |
| `wp1045_sh_cong_cu_dat_bo_trang_thai` | 2/2 | (a) vang PATH + ung vien tot ma khong chon ung vien: rc=0 GITHUB_PATH=[] cai_cong_cu: 'tuychon1045x' ten tran da DAT, giu nguyen PATH  |
| `wp1045_sh_bo_thoat_3` | 2/2 | (e-DO) doi rc=3 kem dong neu ten, duoc rc=0 stderr="cai_cong_cu: 'tuychon1045x' chua DAT sau khi cai (trang_thai cua chinh no khac DAT; kiem-tra rc=2)\n" |
| `wp1045_sh_source_tuy_chon_hong_van_dung` | 2/2 | --bat-buoc (bo-chon-hong): cong cu tuy chon thieu chan cong cu bat buoc sau no: rc=1 GITHUB_PATH=[] cai_cong_cu: khong thu muc nao co 'tuychon1045x' chay duoc  |
| `wp1045_sh_source_bat_buoc_hong_van_di_tiep` | 2/2 | --bat-buoc: cong cu bat buoc hong ma van di tiep: rc=3 GITHUB_PATH=['/tmp/lt_xeqi95y1/uv_tuychon1045x'] cai_cong_cu: 'batbuoc1045x' (bat_buoc: false) khong cai duoc (rc=47); --bat-buoc di tiep  |
| `wp1045_sh_kiem_cuoi_tran_duoi_errexit` | 2/2 | (e-DO) doi rc=3 kem dong neu ten, duoc rc=2 stderr='' |
| `wp1045_sh_eval_trong_ngu_canh_dieu_kien` | 2/2 | (g) cong thuc tu bat set -e ma loi giua chung van di tiep: rc=0 'tuychon1045x",\n      "bat_buoc": false,\n      "ban_ghim": null,\n      "ban_thay": {\n        "mac_dinh": "1.2.3"\n      },\n      "trang_thai": "DAT",\n      "chi_tiet": "dat"\n    } |
| `wp1045_sh_source_khong_don_tam` | 1/1 | --bat-buoc (bo-chon-hong): bo lai thu muc tam sau hai luot source: ['cai_cong_cu.ONAcoN'] |
| `wp1045_sh_rc_cai_mat_ma` | 1/1 | --bat-buoc: cong cu bat buoc hong ma van di tiep: rc=1 GITHUB_PATH=[]  |
| `wp1045_sh_thoat_3_ca_luot_source` | 2/2 | --bat-buoc (cong-thuc-rc0): cong cu tuy chon thieu chan cong cu bat buoc sau no: rc=3 GITHUB_PATH=[] cai_cong_cu: 'tuychon1045x' chua DAT sau khi cai (trang_thai cua chinh no khac DAT; kiem-tra rc=0)  |
| `wp868_sh_go_trap_sau_eval` | 2/2 | kenh 'loi': thu muc kenh con sau khi thoat: rc=7 con=['cai_cong_cu.MU3q72'] |

## Người gọi thật và mã thoát

`python3 evidence/probe_calls.py`: đọc 10 bước gọi trực tiếp trong `ci.yml` (5 job × shellcheck/rg), tất cả `shell: bash`, `continue-on-error: false`; `ops/codex_cloud_setup.sh:85` gọi actionlint dưới `set -euo pipefail`. Chạy đúng câu gọi với callee fixture trả 0/2/3/47: cả ba đường ở head/base cho rc tương ứng 0/2/3/47; chỉ rc0 chạy tới marker `AFTER_CALL`. Không có phân nhánh phụ thuộc riêng rc2 thay vì rc3 trong các callsite này. Vì vậy DO direct đổi 2→3 theo M2 vẫn làm bước/caller dừng, không đổi đỏ thành xanh. Đây là phép đo hợp đồng mã thoát ở caller, không phải chạy toàn bootstrap. [Log](evidence/calls.log), [cấu trúc callsite và kết quả](evidence/calls.json).

Cùng script đo gọi `bash ops/cai_cong_cu.sh shellcheck`, `... rg`, `... actionlint` với bản kê thật và nhị phân cục bộ: head/base đều rc0, JSON DAT; shellcheck/rg giữ GITHUB_PATH rỗng, actionlint ghi đúng thư mục cài. `sudo apt-get` là fixture rc0; actionlint dùng archive tạo từ binary cục bộ với băm tự đo qua AL_GOI/AL_SHA256, đích trong sandbox. **KHÔNG ĐO ĐƯỢC** apt/tải release thật, toàn bootstrap cloud, Windows native, CI PR hoặc workflow_dispatch/G5 của exact head.

## Chốt đề xuất đã đo

`python3 evidence/probe_source_guard.py`: ca batch ba lượt source với lỗi kiểm cuối ở lượt hai được đo trên đầy đủ bốn cây. Head/base **3/3 PASS** mỗi cây (DO tuỳ chọn rc2, DO bắt buộc rc2, bắt buộc vắng rc3; tất cả không chạy lượt ba). Hai mutant mới mỗi cây **3/3 KILLED** bởi marker `THIRD` xuất hiện, dù mã cuối vẫn 2/2/3. Chỉ kiểm `rc != 0` sẽ bỏ lọt lỗi này. Đây là bằng chứng cho ca khoá đề xuất, chưa phải sửa test trong kho. [Script](evidence/probe_source_guard.py), [kết quả](evidence/source-guard.json).

## Toàn suite launcher — kết quả đã xong

`python3 evidence/run_full.py head` / `python3 evidence/run_full.py base` thực thi `python3 .claude/dev/launcher_test.py` trên hai bản sao đầy đủ, với PYTHONDONTWRITEBYTECODE=1, GIT_CONFIG_GLOBAL=/dev/null, GIT_CONFIG_SYSTEM=/dev/null và core.abbrev=7.

| Bản | rc | Qua/đã chạy | Tổng | Bỏ qua | Hỏng |
|---|---:|---:|---:|---:|---:|
| Head | 1 | 290/303 | 313 | 10 | 13 |
| Base | 1 | 286/299 | 309 | 10 | 13 |

[Head stdout](evidence/head-launcher.stdout), [head rc](evidence/head-launcher.json), [base stdout](evidence/base-launcher.stdout), [base rc](evidence/base-launcher.json). `python3 evidence/summarize.py` cho chênh tập ca đỏ hai chiều `[]`, chênh tập ca bỏ qua hai chiều `[]`. Tập 13 ca đỏ cũng đúng 13 tên đã ghi ở VERDICT-LUOT1.md. Hai lỗi /var/tmp trả EROFS; 11 lỗi r484 gồm thông báo tổ tiên repository hoặc chốt materializer không tới được. `/tmp/.git` rỗng còn nguyên trong suốt phép đo; không quy 13 lỗi chung thành hồi quy của head. **KHÔNG ĐO ĐƯỢC launcher N/N xanh**.

Tập đỏ:

- `r858_goc_tam_tranh_to_tien_co_git`
- `t86_chuan_bi_nhan_ca_base64_lan_json_tho_va_tu_choi_rac`
- `r484_g2_doctor_doc_dung_home_da_materialize`
- `r484_g2_schema_truoc_freshness_va_home_materialize`
- `r484_g2_child_khong_nhan_snapshot_va_rac_chan_truoc_probe`
- `r484_g2_storage_kernel_guardrails`
- `r484_g2_recovery_probe_rollback_va_snapshot_moi`
- `r484_g2_probe_isolated_marker_va_refresh`
- `r484_g2_hook_shell_scrub_truoc_probe`
- `r484_g8_hook_scrub_kin_voi_bash_env`
- `r484_g7_materializer_khong_ghi_duoc_trang_thai_noi_dung_ly_do`
- `r484_g7_tu_choi_ghi_dung_ban_da_probe`
- `r484_g7_auth_doi_truoc_khi_thay_thi_giu_ban_moi`

Tập bỏ qua (10; lượt 1 ghi 2, lần này thêm 8 ca không dựng được venv/pip):

- `t62_qua_han_ma_khong_giet_het_cay_phai_tra_125`: fixture nay danh cho Windows; ban POSIX la t63 (chay duoc, khong bo qua)
- `r345_chan_socket_that_ma_than_hook_van_chay_dung`: KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)
- `r345_cac_phep_do_cuc_bo_van_dung`: KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)
- `r345_lop_tham_import_van_co_rang`: KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)
- `r345_dot_bien_ba_phep_do_cuc_bo_lam_ca_dich_DO`: KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)
- `r347_tham_import_van_song_tren_python_truoc_310`: KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)
- `r347_dot_bien_bo_duong_lui_310_lam_ca_dich_DO`: KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)
- `r348_goi_chi_co_CLI_khong_duoc_bao_dong_gia`: KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)
- `r348_dot_bien_bo_isidentifier_lam_ca_dich_DO`: KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)
- `r484_g4_windows_sid_alias_identity`: BO QUA native Windows SID conversion

## Phản chứng nền và recipe

`python3 evidence/probe_behavior.py` đo riêng từng ca để lỗi (a) không che lỗi (b):

| Ca | Head | Base |
|---|---|---|
| (a) tuỳ chọn vắng PATH, ứng viên tốt | rc0, DAT, GITHUB_PATH ghi ứng viên | rc0, KHONG_DO_DUOC, GITHUB_PATH rỗng, nhận nhầm tên trần DAT |
| (b) tuỳ chọn vắng, không ứng viên | rc1, stderr không có ứng viên chạy được, GITHUB_PATH rỗng | rc0, KHONG_DO_DUOC, nhận nhầm tên trần DAT |

`python3 evidence/probe_shell.py` tái hiện đúng recipe `set -e; false; echo CONTINUED` trên ba cấu trúc eval: base rc1/stdout_file rỗng; round1 rc0/stdout_file `CONTINUED\n`; head rc1/stdout_file rỗng. Đối chứng `false`, `exit 47`, `false; true` lần lượt 1,47,0 ở cả ba cấu trúc. [Log](evidence/shell.log). Phép đo script đầy đủ trong `probe_behavior.py` xác nhận cùng khác biệt, không chỉ đoạn shell tách rời.

## Đột biến mới — đối chiếu toàn suite đã xong

Lệnh `python3 evidence/run_survivor_suite.py <tên>` chạy `python3 .claude/dev/launcher_test.py --nhat-ky <tệp>` trên bản sao đủ cây cho từng mutant, rồi xoá bản sao. Cả hai đều **SỐNG so với nền head**: rc1, **290/303**, tổng 313, bỏ qua 10, hỏng 13; tập ca đỏ trùng head, không có ca đỏ mới, không mất ca đỏ nền. Không gọi suite này xanh; kết luận sống dựa trên delta ca đỏ bằng 0.

| Mutant | Delta đỏ so head | Probe hành vi bổ sung |
|---|---|---|
| `extra_source_errexit_off_preserve_shape` | `[]` hai chiều | lượt thứ ba chạy sau checker DO/KHONG_DO_DUOC; chốt đề xuất 3/3 KILLED |
| `extra_source_final_error_swallowed` | `[]` hai chiều | cùng hành vi; chốt đề xuất 3/3 KILLED |

Vì test source hiện chỉ phủ recipe thất bại và tuỳ chọn vắng (checker rc0), còn các lỗi kênh có `exit` tường minh, cả hai biến thể lọt. Ca shape vẫn thấy các chuỗi yêu cầu. Đây xác nhận finding **P3 source-thieu-khoa-loi-kiem-cuoi**; không mở lại ba finding cũ đã đóng. [Toàn suite mutant tắt errexit](evidence/extra_source_errexit_off_preserve_shape-full.stdout), [toàn suite mutant nuốt checker](evidence/extra_source_final_error_swallowed-full.stdout), [delta](evidence/summary.json).

## Bộ công cụ, phạm vi và kiểm tra tĩnh

Các lệnh dưới đây chạy trong bản sao head/base bằng `python3 evidence/run_full.py head` và `... base`; mã thoát thật được lưu riêng trong `evidence/<bản>-<tên>.json`, stdout/stderr riêng.

| Lệnh | Head | Base | Kết luận |
|---|---|---|---|
| `CONG_CU_TEST_BAN_KINH=manh python3 ops/cong_cu_test.py` | rc0, 61/61, bỏ qua 0, tiền kiểm bỏ qua 0 | giống head | Không đổi N/N |
| `ruff check --no-cache --select F --output-format json .claude/dev/launcher_test.py scripts/tl.py` | rc1: 5 F841 + 12 F821 | giống head | Delta 0 |
| `shellcheck --format=json ops/cai_cong_cu.sh` | rc1: 1 SC1090 | giống head | Delta 0 |
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | rc0: sạch, 10 tệp, 0 chỗ chép doctrine | giống head | Đạt |
| `git -C cay-kho diff --check 5e458f4 HEAD` | rc0, output rỗng | — | Đạt |

Bộ công cụ còn ghi `TỰ KIỂM SONG SONG (N126): ĐẠT`, `lỗi đột biến=0`, `cổng cây thật=ĐẠT` ở cả hai bản. Dòng 490 đột biến ghi rõ **giao mảnh, không đo trong tiến trình này**; không nhận đã chạy cả 490 bán kính. [Head công cụ](evidence/head-cong-cu.stdout), [base công cụ](evidence/base-cong-cu.stdout), [summary lệnh/rc/delta](evidence/summary.json), [head ruff](evidence/head-ruff.stdout), [base ruff](evidence/base-ruff.stdout), [head shellcheck](evidence/head-shellcheck.stdout), [base shellcheck](evidence/base-shellcheck.stdout), [head doctrine](evidence/head-doctrine.stdout), [base doctrine](evidence/base-doctrine.stdout). Ruff/shellcheck delta được so bằng đa tập file tương đối + mã + thông điệp, không coi dịch dòng là finding mới.

`git diff --name-only 5e458f4 HEAD` chỉ có `.claude/dev/launcher_test.py` và `ops/cai_cong_cu.sh`; stat 247 thêm/10 xoá. `git diff 059a4a5 5e458f4 -- <hai tệp>` output rỗng. DIFF.patch và DIFF-LUOT2.patch khớp byte với diff tự tính. [Preflight](evidence/preflight.json), [diff lượt 2](evidence/round2-integrity.json).

Kiểm cuối: exact head không đổi, tree `ea67ffac538583be856d1884e2b176e41f26b173`; `git status --porcelain` output rỗng; core.abbrev=7; danh sách `copies/` rỗng; `/tmp/.git` vẫn rỗng; spec sha256 không đổi. [Lệnh và output kiểm cuối](evidence/final-integrity.json).

## Kết luận

**request_changes — 1 P3 `source-thieu-khoa-loi-kiem-cuoi`; không còn ba finding lượt 1.** Head giữ đúng hành vi source trong các phép đo, nhưng hai mutant làm tiếp tục sau lỗi kiểm cuối vẫn sống cả nhóm ca liên quan lẫn toàn suite so với tập đỏ nền. Chốt đề xuất đã đo giết được cả hai. Ngưỡng yêu cầu không còn P0/P1/P2/P3 chưa đạt. Không cấp quyền merge/land; đây là verdict cuối của lượt review theo trần packet.
