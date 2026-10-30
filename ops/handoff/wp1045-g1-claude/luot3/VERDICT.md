Verdict: approve
Reviewed commit: 201460203f42485f589add150896f2febc00c027
Spec sha256: 8e187b9130e18a757f4f24dfcea6761f688a5f69e21d17356b198b8cc5bd508e

**approve — không còn finding P0/P1/P2/P3 trong phạm vi đã đo.** Finding lượt 2 đã vá thật: hai mutant cũ chết đúng ca mới, ca mới đạt với script base. Bảng thực tế có 13 mutant `wp1045_*` + 3 mutant cũ: 16/16 chết, 28/28 ca đích đỏ; bốn mutant tự thêm cũng chết. [Bằng chứng đột biến](evidence/targets.json), [probe bổ sung](evidence/behavior.json). Launcher còn cùng 13 ca đỏ/10 bỏ qua ở head và base; bộ công cụ 61/61 cả hai; Ruff/ShellCheck delta 0; doctrine-scan rc0. [Đối chiếu toàn suite và gate](evidence/summary.json).

Preflight tự đo: `git rev-parse HEAD` khớp SHA trên; `sha256sum SPEC.md` khớp; `git diff --name-only 5e458f4 HEAD` chỉ `.claude/dev/launcher_test.py`, `ops/cai_cong_cu.sh`; `git diff --check 5e458f4 HEAD` rc0, output rỗng. `DIFF.patch` và `DIFF-LUOT3.patch` khớp byte với diff tự tính. [Lệnh/output](evidence/preflight.json).

Điều kiện đo: core.abbrev=7; PYTHONDONTWRITEBYTECODE=1; GIT_CONFIG_GLOBAL=/dev/null; GIT_CONFIG_SYSTEM=/dev/null. `/tmp/.git` tồn tại và rỗng, giữ nguyên khi so head/base. Mọi lượt đột biến dùng bản sao đủ cây có `.git`, xoá sau đo.

## ĐỐI CHIẾU LƯỢT TRƯỚC — cập nhật 1

`PYTHONDONTWRITEBYTECODE=1 python3 evidence/run_targets.py` (hoặc thêm tên từng mutant) tự áp đúng cặp neo/thay lượt 2 trên bản sao đủ cây. [Lệnh chạy](evidence/run_targets.py), [kết quả](evidence/targets.json), [log](evidence/targets.log).

- `base_newcase`: `PASS` — `ca mới đạt`
- `extra_source_errexit_off_preserve_shape`: `KILLED` — `--bat-buoc (giua bat_buoc=False): kiem cuoi DO cua luot source khong dung ca loat: rc=3 cong cu sau da chay=True `
- `extra_source_final_error_swallowed`: `KILLED` — `--bat-buoc (giua bat_buoc=False): kiem cuoi DO cua luot source khong dung ca loat: rc=3 cong cu sau da chay=True `

`base_newcase` dùng ca mới của head với riêng `ops/cai_cong_cu.sh` lấy từ blob base. Các probe head/base cũng so script cài theo cách này; toàn suite base ở dưới checkout toàn bộ cây base.

Finding P3 `source-thieu-khoa-loi-kiem-cuoi`: **ĐÃ VÁ THẬT** ở hai phản chứng đã nêu. Base đạt vì lỗi checker ở lượt source vẫn dừng cả loạt bằng errexit; đây là hành vi nền cần giữ. Mutant rc3 thay vì rc2 vì lượt ba chạy rồi checker thấy công cụ bắt buộc ấy vắng; marker True chứng minh sai hành vi, không chỉ khác mã thoát.

Kiểm kê độc lập bằng AST của bảng `DOT_BIEN_HOOK`: **13** tên `wp1045_*`, **3** tên cũ được yêu cầu, **16 tổng cộng**. Không có 16 tên `wp1045_*` riêng cộng thêm 3; sẽ đo hết mọi hàng tồn tại, không suy thêm hàng không có. [Danh sách/cặp neo/thay](evidence/inventory.json).

## Đột biến đăng ký — cập nhật 2

`PYTHONDONTWRITEBYTECODE=1 python3 evidence/run_targets.py` ⇒ **16/16 mutant đăng ký CHẾT, 28/28 ca đích ĐỎ đúng `TinHieuChotCa`, 0 ERROR, 0 SKIP**. Đối chứng head: 15/15 ca liên quan đạt. Mỗi hàng tái hiện bằng `python3 evidence/run_targets.py <tên>`; cặp neo/thay và toàn bộ output mỗi ca ở [targets.json](evidence/targets.json).

| Mutant | Ca đích chết | Chốt đầu tiên (output) |
|---|---:|---|
| `wp858_sh_bo_kiem_ten_tran` | 2/2 | linux/git: ten tran da DAT ma van ghi GITHUB_PATH: rc=0 GITHUB_PATH='/tmp/lt_b3m3fgn2/goc/usr/bin' |
| `wp858_sh_chon_theo_ma_thoat` | 2/2 | linux/git: khong ung vien nao chay duoc ma van chon ('exit 0'): rc=3 GITHUB_PATH='/tmp/lt_aya1ci9n/goc/usr/bin' |
| `wp1045_sh_ten_tran_ve_rc` | 2/2 | (a) vang PATH + ung vien tot ma khong chon ung vien: rc=3 GITHUB_PATH=[] cai_cong_cu: 'tuychon1045x' ten tran da DAT, giu nguyen PATH cai_cong_cu: 'tuychon1045x' chua DAT sau khi cai (trang_thai cua chinh no khac DAT; kiem-tra rc=0)  |
| `wp1045_sh_ung_vien_ve_rc` | 2/2 | (a) vang PATH + ung vien tot ma khong chon ung vien: rc=3 GITHUB_PATH=['/tmp/lt_x4mzwf2o/uv_tuychon1045x_rong'] cai_cong_cu: 'tuychon1045x' chua DAT sau khi cai (trang_thai cua chinh no khac DAT; kiem-tra rc=0)  |
| `wp1045_sh_cong_cu_dat_bo_trang_thai` | 2/2 | (a) vang PATH + ung vien tot ma khong chon ung vien: rc=0 GITHUB_PATH=[] cai_cong_cu: 'tuychon1045x' ten tran da DAT, giu nguyen PATH  |
| `wp1045_sh_bo_thoat_3` | 2/2 | (e-DO) doi rc=3 kem dong neu ten, duoc rc=0 stderr="cai_cong_cu: 'tuychon1045x' chua DAT sau khi cai (trang_thai cua chinh no khac DAT; kiem-tra rc=2)\n" |
| `wp1045_sh_source_tuy_chon_hong_van_dung` | 2/2 | --bat-buoc (bo-chon-hong): cong cu tuy chon thieu chan cong cu bat buoc sau no: rc=1 GITHUB_PATH=[] cai_cong_cu: khong thu muc nao co 'tuychon1045x' chay duoc  |
| `wp1045_sh_source_bat_buoc_hong_van_di_tiep` | 2/2 | --bat-buoc: cong cu bat buoc hong ma van di tiep: rc=3 GITHUB_PATH=['/tmp/lt_4x_3_p4u/uv_tuychon1045x'] cai_cong_cu: 'batbuoc1045x' (bat_buoc: false) khong cai duoc (rc=47); --bat-buoc di tiep  |
| `wp1045_sh_kiem_cuoi_tran_duoi_errexit` | 2/2 | (e-DO) doi rc=3 kem dong neu ten, duoc rc=2 stderr='' |
| `wp1045_sh_eval_trong_ngu_canh_dieu_kien` | 2/2 | (g) cong thuc tu bat set -e ma loi giua chung van di tiep: rc=0 'tuychon1045x",\n      "bat_buoc": false,\n      "ban_ghim": null,\n      "ban_thay": {\n        "mac_dinh": "1.2.3"\n      },\n      "trang_thai": "DAT",\n      "chi_tiet": "dat"\n    }\n  ],\n  "canary": []\n}\n' |
| `wp1045_sh_source_khong_don_tam` | 1/1 | --bat-buoc (bo-chon-hong): bo lai thu muc tam sau hai luot source: ['cai_cong_cu.3rkFbd'] |
| `wp1045_sh_rc_cai_mat_ma` | 1/1 | --bat-buoc: cong cu bat buoc hong ma van di tiep: rc=1 GITHUB_PATH=[]  |
| `wp1045_sh_errexit_tat_sau_eval` | 1/1 | --bat-buoc (giua bat_buoc=False): kiem cuoi DO cua luot source khong dung ca loat: rc=3 cong cu sau da chay=True  |
| `wp1045_sh_kiem_cuoi_source_nuot_loi` | 1/1 | --bat-buoc (giua bat_buoc=False): kiem cuoi DO cua luot source khong dung ca loat: rc=3 cong cu sau da chay=True  |
| `wp1045_sh_thoat_3_ca_luot_source` | 2/2 | --bat-buoc (cong-thuc-rc0): cong cu tuy chon thieu chan cong cu bat buoc sau no: rc=3 GITHUB_PATH=[] cai_cong_cu: 'tuychon1045x' chua DAT sau khi cai (trang_thai cua chinh no khac DAT; kiem-tra rc=0)  |
| `wp868_sh_go_trap_sau_eval` | 2/2 | kenh 'loi': thu muc kenh con sau khi thoat: rc=7 con=['cai_cong_cu.dFmH0V'] |

## ĐỐI CHIẾU LƯỢT TRƯỚC — cập nhật 3: mã thoát không che marker

`PYTHONDONTWRITEBYTECODE=1 python3 evidence/probe_behavior.py` trên head/base và hai mutant. Lượt ba nay có binary tốt sẵn để tránh lỗi vắng công cụ ở cuối. [Script](evidence/probe_behavior.py), [stdout/stderr, marker, thư mục tạm](evidence/behavior.json).

| Checker ở lượt hai | Head | Base | Tắt errexit | Nuốt lỗi checker |
|---|---|---|---|---|
| optional_DO | rc2, marker=False | rc2, marker=False | rc2, marker=True | rc2, marker=True |
| required_DO | rc2, marker=False | rc2, marker=False | rc2, marker=True | rc2, marker=True |
| required_missing | rc3, marker=False | rc3, marker=False | rc3, marker=True | rc3, marker=True |
| optional_missing | rc0, marker=True | rc0, marker=True | rc0, marker=True | rc0, marker=True |

Hai mutant CHẾT ở cả DO tuỳ chọn, DO bắt buộc và bắt buộc vắng nhờ marker. Đối chứng tuỳ chọn vắng được đi tiếp vẫn đúng ở head/base. Mọi lượt trong bảng đều không để lại thư mục tạm.

## Phản chứng base và các finding cũ

Cùng lệnh `python3 evidence/probe_behavior.py` chạy riêng (a)/(b), không để chốt (a) ngăn đo (b):

| Ca | Head | Base |
|---|---|---|
| (a) tuỳ chọn vắng PATH, ứng viên tốt | rc0, DAT, ghi ứng viên tốt | rc0, KHONG_DO_DUOC, GITHUB_PATH rỗng, nhận nhầm tên trần DAT |
| (b) vắng PATH, không ứng viên | rc1, không ghi GITHUB_PATH, báo không có ứng viên chạy được | rc0, KHONG_DO_DUOC, nhận nhầm tên trần DAT |
| (c) tên trần tốt | rc0, giữ PATH | rc0, giữ PATH |
| (d) recipe true, công cụ tuỳ chọn vắng | rc3, stderr nêu tên | rc0 |
| DO trực tiếp | rc3, stderr nêu tên | rc2, stderr rỗng |
| Bắt buộc vắng trực tiếp | rc3, stderr nêu tên | rc3, stderr rỗng |
| Recipe `set -e; false; touch marker` | rc1, marker vắng | rc1, marker vắng |

Các chốt lượt 1 vẫn đóng: thông báo M2 ở stderr, recipe tự bật errexit dừng thật, dọn tạm nhánh optional thất bại, bảo toàn rc47. Hai chốt sau còn được phản chứng bởi `wp1045_sh_source_khong_don_tam`, `wp1045_sh_rc_cai_mat_ma` ở bảng trên.

## Đột biến bổ sung cho phần còn lại của bản vá

`python3 evidence/probe_behavior.py <tên>` (lượt đầy đủ đã chạy không truyền tên): mỗi mutant dùng bản sao đủ cây riêng, chạy cả 13 ca r868/r1045 và xoá bản sao. Chỉ `TinHieuChotCa` tính là chết. [Cặp neo/thay, từng ca và probe JSON](evidence/behavior.json).

| Mutant tự thêm | Kết quả trong 13 ca | Output chốt |
|---|---|---|
| `extra_direct_diagnostic_stdout` | 1 KILLED, 12 PASS, 0 ERROR/SKIP | (e-DO) doi rc=3 kem dong neu ten, duoc rc=3 stderr='' |
| `extra_optional_recipe_returns_error` | 2 KILLED, 11 PASS, 0 ERROR/SKIP | --bat-buoc (bo-chon-hong): cong cu tuy chon thieu chan cong cu bat buoc sau no: rc=1 GITHUB_PATH=[] cai_cong_cu: khong thu muc nao co 'tuychon1045x' chay duoc cai_cong_cu: 'tuychon1045x' (bat_buoc: false) khong cai duoc (rc=1); --bat-buoc di tiep ; luot source cua --bat-buoc phai di tiep khi cong cu tuy chon cai hong, con lai thoat dung ma cu |
| `extra_json_accepts_other_name` | 1 KILLED, 12 PASS, 0 ERROR/SKIP | cong_cu_json_dung thieu 'c[0].get("ten") == sys.argv[1]' |
| `extra_json_accepts_multiple_items` | 1 KILLED, 12 PASS, 0 ERROR/SKIP | cong_cu_json_dung thieu 'len(c) == 1' |

**Không mutant bổ sung nào SỐNG** trong tập đo này. Hai mutant JSON chỉ bị ca hình dạng trong suite giết; probe hành vi độc lập của helper xác minh hậu quả thật: chấp nhận sai tên / nhiều mục đều đổi rc1→rc0. Head nhận đúng một mục DAT đúng tên (rc0), từ chối sai tên, hai mục, thiếu trạng thái, danh sách rỗng, JSON hỏng và checker rc2 (tất cả rc1). Không nhận các biến thể này là đã được ca hành vi gốc phủ.

`bash ops/cai_cong_cu.sh shellcheck` trên bản sao head/base, bản kê thật và shellcheck cục bộ: cả hai rc0, trạng thái DAT, GITHUB_PATH rỗng. `sudo` là fixture rc0 để không cài gói; **KHÔNG ĐO ĐƯỢC** apt/tải gói thật. [Lệnh, stdout, stderr](evidence/behavior.json).

## Toàn suite launcher — cập nhật 4

`PYTHONDONTWRITEBYTECODE=1 python3 evidence/run_full.py head` / `... base` thực thi `python3 .claude/dev/launcher_test.py --nhat-ky <tệp>` trên hai bản sao đủ cây; base checkout đúng `5e458f4751c83a3811642532c5705ba22d0711c0`.

| Bản | rc | Qua/đã chạy | Tổng | BỎ QUA | Đỏ |
|---|---:|---:|---:|---:|---:|
| head | 1 | 291/304 | 314 | 10 | 13 |
| base | 1 | 286/299 | 309 | 10 | 13 |

Tập đỏ và tập bỏ qua bằng nhau: chênh hai chiều đều `[]`. Head có thêm 5 ca, cả 5 đạt. **KHÔNG ĐO ĐƯỢC launcher N/N xanh**; không coi 10 ca bỏ qua là đạt. [So tập](evidence/launcher-summary.json), [head stdout](evidence/head-launcher.stdout), [base stdout](evidence/base-launcher.stdout), [lệnh/rc head](evidence/head-launcher.json), [lệnh/rc base](evidence/base-launcher.json).

Tập 13 ca đỏ chung:

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

Hai ca đầu báo `[Errno 30] Read-only file system: /var/tmp/...`. Các ca r484 báo tổ tiên repository (`Codex home is inside a repository`) hoặc không tới được chốt materializer; cùng lỗi ở head/base. `/tmp/.git` rỗng tồn tại trong cả hai lượt. Không quy các lỗi chung này thành hồi quy của diff.

Tập 10 ca BỎ QUA chung:

- `t62_qua_han_ma_khong_giet_het_cay_phai_tra_125`
- `r345_chan_socket_that_ma_than_hook_van_chay_dung`
- `r345_cac_phep_do_cuc_bo_van_dung`
- `r345_lop_tham_import_van_co_rang`
- `r345_dot_bien_ba_phep_do_cuc_bo_lam_ca_dich_DO`
- `r347_tham_import_van_song_tren_python_truoc_310`
- `r347_dot_bien_bo_duong_lui_310_lam_ca_dich_DO`
- `r348_goi_chi_co_CLI_khong_duoc_bao_dong_gia`
- `r348_dot_bien_bo_isidentifier_lam_ca_dich_DO`
- `r484_g4_windows_sid_alias_identity`

Hai ca t62/r484_g4 dành cho Windows; tám ca r345/r347/r348 báo `KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)`. Không tự suy thành phép đo mạng.

## Bộ công cụ, kiểm tra tĩnh và phạm vi — cập nhật 5

Lệnh tái hiện toàn lượt: `PYTHONDONTWRITEBYTECODE=1 python3 evidence/run_full.py head` / `... base`. Các lệnh dưới đây chạy trong bản sao của mỗi bản; biến Git và bán kính được runner đặt tường minh. [Lệnh và rc từng bước](evidence/summary.json); [script so delta](evidence/summarize.py).

| Lệnh | Head | Base | Kết luận |
|---|---|---|---|
| `CONG_CU_TEST_BAN_KINH=manh python3 ops/cong_cu_test.py` | rc0, 61/61, bỏ qua 0, tiền kiểm bỏ qua 0 | rc0, 61/61, bỏ qua 0, tiền kiểm bỏ qua 0 | N/N không đổi |
| `ruff check --no-cache --select F --output-format json .claude/dev/launcher_test.py scripts/tl.py` | rc1: 5 F841 + 12 F821 | rc1: 5 F841 + 12 F821 | Delta 0 |
| `shellcheck --format=json ops/cai_cong_cu.sh` | rc1: 1 SC1090 | rc1: 1 SC1090 | Delta 0 |
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | rc0, sạch, 10 tệp, 0 chỗ chép doctrine | giống head | Đạt |
| `git -C cay-kho diff --check 5e458f4 HEAD` | rc0, output rỗng | — | Đạt |
| `bash -n cay-kho/ops/cai_cong_cu.sh` | rc0, output rỗng | — | Đạt |

Bộ công cụ còn báo `TỰ KIỂM SONG SONG (N126): ĐẠT`, `lỗi đột biến=0`, `cổng cây thật=ĐẠT` ở cả hai bản. Dòng 490 mutant nói rõ **giao mảnh, KHÔNG đo trong tiến trình này**; không nhận đã chạy cả 490 bán kính. [Head công cụ](evidence/head-cong-cu.stdout), [base công cụ](evidence/base-cong-cu.stdout), [head rc](evidence/head-cong-cu.json), [base rc](evidence/base-cong-cu.json).

Ruff/ShellCheck so đa tập đường dẫn tương đối + mã + thông điệp, bỏ dịch dòng; chênh hai chiều đều `[]`. Bare lint có nợ nền và rc1, không gọi là lint tuyệt đối sạch. Phiên bản đo: Ruff 0.16.9, ShellCheck 0.9.0, Python 3.13.17, Git 2.43.0; [lệnh/output phiên bản](evidence/tool-versions.json). [Head Ruff](evidence/head-ruff.stdout), [base Ruff](evidence/base-ruff.stdout), [head ShellCheck](evidence/head-shellcheck.stdout), [base ShellCheck](evidence/base-shellcheck.stdout), [head doctrine](evidence/head-doctrine.stdout), [base doctrine](evidence/base-doctrine.stdout).

`git diff --name-only 5e458f4 HEAD`: đúng `.claude/dev/launcher_test.py`, `ops/cai_cong_cu.sh`; stat 276 thêm/10 xoá. Kiểm cuối exact HEAD không đổi, tree `332aed0f6d2efa3a4a75856c6d66800e0ca258cb`; `git status --porcelain --ignored`, `git diff --exit-code`, `git diff --cached --exit-code` đều rc0/output rỗng. Hai tệp nội dung khớp blob HEAD; `core.abbrev=7`, SHA spec không đổi; `copies/` rỗng, `/tmp/.git` vẫn rỗng. [Preflight](evidence/preflight.json), [lệnh/output kiểm cuối](evidence/final-integrity.json).

## Finding

Không có finding P0/P1/P2/P3 còn mở trong phạm vi đã đo. Finding P3 `source-thieu-khoa-loi-kiem-cuoi` của lượt 2 **ĐÃ VÁ THẬT** theo hai mutant cũ, ca mới trên base và ma trận hành vi source ở trên; không mở lại các finding lượt 1.

## Giới hạn nghiệm thu

- **KHÔNG ĐO ĐƯỢC** launcher N/N xanh: đã chạy trọn vẹn, nhưng cả head/base cùng 13 ca đỏ và 10 ca bỏ qua như bảng trên.
- **KHÔNG ĐO ĐƯỢC** CI PR, Windows native/workflow_dispatch và G5 của exact head; ca giả lập Windows trong launcher không thay thế phép đo này.
- **KHÔNG ĐO ĐƯỢC** cài gói/tải release thật; phép gọi shellcheck dùng binary thật và fixture cho installer như đã khai.
- Chỉ có 13 tên `wp1045_*` trong bảng, cộng 3 tên cũ thành 16; đã đo toàn bộ 16 hàng hiện hữu. Không có bằng chứng cho ba tên `wp1045_*` bổ sung không được cung cấp.

Verdict **approve** theo ngưỡng không còn P0/P1/P2/P3 trong diff đã đo, với các giới hạn nghiệm thu nêu rõ. Không cấp quyền merge/land.
