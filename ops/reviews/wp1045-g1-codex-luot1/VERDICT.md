Verdict: request_changes
Reviewed commit: daedfb75e524fa6adc3d68db63b500c2d6c53730
Spec sha256: 8e187b9130e18a757f4f24dfcea6761f688a5f69e21d17356b198b8cc5bd508e

Có 1 finding P2 và 2 finding P3. Bản vá sửa được phản chứng công cụ tuỳ chọn vắng PATH, nhưng chưa thực hiện đủ M2, thay đổi ngữ nghĩa recipe tự bật errexit, và còn hai đột biến hành vi sống ở nhánh source. Mười đột biến đăng ký được yêu cầu đều giết đúng ca đích. Không cấp quyền merge/land.

Các lệnh Python trong báo cáo dùng tiền tố `env PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null`. Cwd mặc định là sandbox; lệnh suite/lint chạy trong bản sao đủ cây `copies/head` hoặc `copies/base`. `git config core.abbrev 7` đã đặt trước phép đo. Kết quả từng lần chạy và script tái hiện ở [evidence](evidence/); không dùng lời khai executor làm bằng chứng. Bản ghi tăng dần trước khi tổng hợp ở [VERDICT-progress.md](evidence/VERDICT-progress.md).

**Findings**

- [P2] m2-bi-errexit-cat-truoc-thong-bao: `ops/cai_cong_cu.sh:176` — `python3 evidence/probe_behavior.py` (các nhãn `head_final_DO_optional1045review`, `head_final_DO_required1045review`, `head_final_missing_required1045review`) — với công thức cài `true`, binary trả `exit 1`: JSON của chính công cụ là `DO`, script **rc=2, stderr rỗng**; công cụ bắt buộc vắng: JSON `KHONG_DO_DUOC`, **rc=3, stderr rỗng**. Lệnh kiểm cuối đứng trần dưới `set -e`, nên thoát trước chốt dòng 180. M2 đóng băng yêu cầu gọi trực tiếp, công cụ chưa DAT sau kiểm cuối phải thoát 3 và có dòng stderr nêu tên. Head chỉ đạt điều này với tuỳ chọn vắng, vì checker khi ấy trả 0. — Hướng vá: thu kết quả kiểm cuối để chốt trực tiếp thực sự chạy; giữ hành vi/mã kiểm cho lượt source; thêm test DO và bắt buộc vắng. [Log](evidence/behavior.log).

- [P3] recipe-bat-errexit-bi-vo-hieu: `ops/cai_cong_cu.sh:152` — `python3 evidence/probe_shell.py` và `python3 evidence/probe_behavior.py` (nhãn `head_recipe_sete`, `base_recipe_sete`) — recipe `set -e; false; echo CONTINUED`: dạng base **rc=1, stdout_file rỗng**; dạng head **rc=0, stdout_file="CONTINUED\n"**. Qua script đầy đủ với công cụ tốt sẵn: base rc=1, head rc=0 và JSON DAT. `|| RC_CAI=$?` làm toàn subshell nằm trong ngữ cảnh bỏ qua errexit, kể cả khi recipe bật lại `set -e`. `set +e` trước eval không bảo toàn trường hợp này. Phạm vi tác động hiện đo được là recipe tự bật `-e`; `rg -n 'set -e' cay-kho/ops/cong_cu.yaml` không có kết quả, nên không quy đây là hồi quy đã xảy ra ở recipe hiện hành. — Hướng vá: thu rc bằng cách tạm tắt errexit ở shell cha, chạy subshell ở vị trí không bị điều kiện hoá, lấy `$?`, rồi khôi phục; thêm ca bật lại `-e`. [Log shell](evidence/shell.log), [log script đầy đủ](evidence/behavior.log).

- [P3] source-thieu-khoa-don-tam-va-ma-goc: `.claude/dev/launcher_test.py:10320`, `:10343` — `python3 evidence/run_mutants.py extra_source_no_cleanup` và `python3 evidence/run_mutants.py extra_rc1_preserve_shape` — mỗi mutant **12/12 ca r868/r1045 PASS, 0 ERROR, 0 SKIP**, tức SỐNG trong nhóm ca liên quan. Mutant thứ nhất gỡ `rm -rf -- "$TAM_CAI"` trước `return 0`; phép đo hành vi để lại một thư mục `cai_cong_cu.*` sau batch rc=0, trong khi head không để lại. Mutant thứ hai giữ dòng capture/chuỗi neo, thêm `RC_CAI=1` trong nhánh lỗi; batch bắt buộc có recipe `exit 47` trả **1**, head/base trả **47**, nhưng test chỉ kiểm `!= 0`. — Hướng vá: dùng TMPDIR riêng, assert hết thư mục tạm sau ít nhất hai lượt source; dùng mã lỗi khác 1 và assert mã chính xác; neo cả hai mutant vào bảng. [Cleanup mutant](evidence/extra_source_no_cleanup.log), [rc mutant](evidence/extra_rc1_preserve_shape.log), [đối chứng hành vi](evidence/behavior.log). Đây là lỗ test; head hiện dọn tạm và giữ rc=47 đúng ở các đối chứng này.

**Toàn suite và điều kiện đo**

| Lệnh | Head | Base |
|---|---|---|
| `python3 .claude/dev/launcher_test.py` | rc=1; **298/311** đã chạy qua; tổng 313, bỏ qua 2, hỏng 13 | rc=1; **294/307** đã chạy qua; tổng 309, bỏ qua 2, hỏng 13 |
| `CONG_CU_TEST_BAN_KINH=manh python3 ops/cong_cu_test.py` | rc=0; **61/61 đạt**; bỏ qua 0, tiền kiểm bỏ qua 0 | rc=0; **61/61 đạt**; bỏ qua 0, tiền kiểm bỏ qua 0 |

Nhật ký: [head launcher](evidence/head-launcher.log), [base launcher](evidence/base-launcher.log), [head công cụ](evidence/head-cong-cu.log), [base công cụ](evidence/base-cong-cu.log). Mã thoát thật trong các tệp `.rc` tương ứng; không lấy rc của lệnh `tail` làm rc suite.

Trước đo, `ls -ld /tmp/.git; ls -la /tmp/.git` cho thấy thư mục tồn tại, rỗng ngoài `.`/`..`, mode `dr-xr-xr-x`. Giữ nguyên. Tập tên 13 ca đỏ head/base bằng nhau, không có ca đỏ mới:

- 11 ca `r484_*`: `r484_g2_doctor_doc_dung_home_da_materialize`, `r484_g2_schema_truoc_freshness_va_home_materialize`, `r484_g2_child_khong_nhan_snapshot_va_rac_chan_truoc_probe`, `r484_g2_storage_kernel_guardrails`, `r484_g2_recovery_probe_rollback_va_snapshot_moi`, `r484_g2_probe_isolated_marker_va_refresh`, `r484_g2_hook_shell_scrub_truoc_probe`, `r484_g8_hook_scrub_kin_voi_bash_env`, `r484_g7_materializer_khong_ghi_duoc_trang_thai_noi_dung_ly_do`, `r484_g7_tu_choi_ghi_dung_ban_da_probe`, `r484_g7_auth_doi_truoc_khi_thay_thi_giu_ban_moi`. Nhiều ca báo `Codex home is inside a repository`; các ca khác báo materializer/probe không tới được chốt. Đây là phép đo trong điều kiện tổ tiên `.git` đã cảnh báo, chưa phải phép đo khi đã bỏ điều kiện ấy.
- `r858_goc_tam_tranh_to_tien_co_git`, `t86_chuan_bi_nhan_ca_base64_lan_json_tho_va_tu_choi_rac`: `[Errno 30] Read-only file system: '/var/tmp/...'` ở cả head/base.
- Hai ca BỎ QUA: `t62_qua_han_ma_khong_giet_het_cay_phai_tra_125` (fixture Windows), `r484_g4_windows_sid_alias_identity` (native Windows SID).

**KHÔNG ĐO ĐƯỢC toàn suite launcher xanh** trong điều kiện này; không đổi 13 lỗi môi trường thành PASS. Delta tập ca lỗi = 0. Riêng `python3 evidence/run_cases.py copies/head r1045_` cho **4/4 PASS**, 0 skip/error ([log](evidence/head-r1045.log)).

Cả hai `cong_cu_test` còn in `cổng cây thật=ĐẠT`, `lỗi đột biến=0`, `TỰ KIỂM SONG SONG (N126): ĐẠT`. Dòng `490 đột biến: GIAO ... KHÔNG đo trong tiến trình này (CONG_CU_TEST_BAN_KINH=manh)` không phải bằng chứng đã chạy 490 bán kính; báo cáo không nhận công đó.

**Phản chứng trên script base**

Bản sao đủ cây `copies/counterfactual` giữ tests head, chỉ thay script bằng `git -C cay-kho show 059a4a5a080a98270973ef9ce23a38dad5aa2f38:ops/cai_cong_cu.sh`.

`python3 evidence/run_cases.py copies/counterfactual r1045_` → 2 PASS, 2 KILLED, 0 ERROR, 0 SKIP ([log](evidence/counterfactual.log)):

| Ca | Kết quả và chốt |
|---|---|
| `r1045_cong_cu_tuy_chon_vang_mat_khong_duoc_nhan_giu_path` | ĐỎ tại (a): `rc=0 GITHUB_PATH=[] ... ten tran da DAT, giu nguyen PATH` dù vắng PATH và có ứng viên tốt |
| `r1045_bat_buoc_cong_cu_tuy_chon_thieu_khong_chan_cong_cu_sau` | PASS |
| `r1045_bat_buoc_cong_cu_bat_buoc_hong_van_dung` | PASS |
| `r1045_hinh_dang_dat_theo_trang_thai` | ĐỎ: `cai_cong_cu.sh thieu ham cong_cu_json_dung` |

Ca gộp dừng tại (a), nên đã đo riêng (b) bằng `python3 evidence/probe_behavior.py`: `base_missing_no_candidates` → rc=0, JSON `KHONG_DO_DUOC`, stderr nhận tên trần DAT; `head_missing_no_candidates` → rc=1, `khong thu muc nao co 'optional1045review' chay duoc`, GITHUB_PATH rỗng. Đúng phản chứng (a) và (b); không suy (b) từ lỗi của (a).

**Mười đột biến đăng ký**

Lệnh: `python3 evidence/run_mutants.py` (hoặc thêm tên mutant để lặp riêng). Mỗi lần bắt đầu bằng script head, sửa trên `copies/mutant`, một bản sao đủ cây gồm `.git` dạng thư mục; các phép sửa chỉ ở sandbox. Script đọc neo/bảng từ head, đòi neo khớp đúng một lần, chạy từng ca đích và ghi tên + thông điệp của `TinHieuChotCa`. Không tính exception giàn giáo là giết. Toàn bộ [log](evidence/mutations.log).

Tên ca rút gọn trong bảng:

- A = `r1045_cong_cu_tuy_chon_vang_mat_khong_duoc_nhan_giu_path`.
- B = `r1045_bat_buoc_cong_cu_tuy_chon_thieu_khong_chan_cong_cu_sau`.
- C = `r1045_bat_buoc_cong_cu_bat_buoc_hong_van_dung`.
- H = `r1045_hinh_dang_dat_theo_trang_thai`.
- L = `r858_cai_linux_chon_ban_chay_duoc`; S = `r858_hinh_dang_cong_thuc_cai`.
- R = `r868_doc_kenh_hong_thi_dung`; K = `r868_hinh_dang_kenh_ket_qua`.

| Đột biến | Ca đích ĐỎ | Thông điệp xác nhận đúng chốt |
|---|---|---|
| `wp1045_sh_ten_tran_ve_rc` | A, H (2/2) | A: `(a) ... rc=3 GITHUB_PATH=[] ... ten tran da DAT`; H: thiếu `if cong_cu_dat "$ten"` |
| `wp1045_sh_ung_vien_ve_rc` | A, H (2/2) | A: chọn `uv_tuychon1045x_rong`, rc=3; H: thiếu `PATH="$d:$PATH" cong_cu_dat` |
| `wp1045_sh_cong_cu_dat_bo_trang_thai` | A, H (2/2) | A: `(a) ... rc=0 GITHUB_PATH=[]`; H: thiếu so sánh `c[0].get(sys.argv[2]) == json.loads(sys.argv[3])` |
| `wp1045_sh_bo_thoat_3` | A, H (2/2) | A: `(d) ... doi rc=3, duoc rc=0`; H: `dong kiem cuoi thieu thoat 3` |
| `wp1045_sh_source_tuy_chon_hong_van_dung` | B, H (2/2) | B: `(bo-chon-hong) ... rc=1 GITHUB_PATH=[]`; H: `luot source ... phai di tiep ...` |
| `wp1045_sh_source_bat_buoc_hong_van_di_tiep` | C, H (2/2) | C: công cụ bắt buộc hỏng nhưng ứng viên công cụ sau được ghi GITHUB_PATH, có `--bat-buoc di tiep`; H: sai chốt source |
| `wp1045_sh_thoat_3_ca_luot_source` | B, H (2/2) | B: `(cong-thuc-rc0) ... rc=3 GITHUB_PATH=[]`; H: sai chốt trực tiếp/source |
| `wp858_sh_bo_kiem_ten_tran` | L, S (2/2) | L: `ten tran da DAT ma van ghi GITHUB_PATH`; S: thiếu `if cong_cu_dat` |
| `wp858_sh_chon_theo_ma_thoat` | L, S (2/2) | L: `khong ung vien nao chay duoc ma van chon ('exit 0'): rc=2 GITHUB_PATH=...`; S: thiếu gọi cong_cu_dat trong vòng |
| `wp868_sh_go_trap_sau_eval` | R, K (2/2) | R: `kenh 'loi': thu muc kenh con sau khi thoat: rc=7 con=['cai_cong_cu....']`; K: trap EXIT không duy nhất/bị gỡ |

Tổng: **10/10 mutant giết đủ 20/20 ca đích**, 0 exception khác, 0 SKIP.

**Đột biến tự bổ sung**

Mỗi hàng chạy toàn nhóm 12 ca `r868_*`/`r1045_*` trên bản sao đủ cây. “Hành vi xanh” ở đây chỉ nói nhóm đã chạy; không nhận là đã chạy lại toàn suite trên từng mutant.

| Mutant / cách sửa | Kết quả trong 12 ca | Phép đo bổ sung |
|---|---|---|
| `extra_no_ten`: bỏ kiểm tên | 11 PASS, H ĐỎ `thieu c[0].get("ten") == sys.argv[1]` | Hàm nhận JSON sai tên khi bỏ chốt; head từ chối |
| `extra_no_len`: bỏ `len(c) == 1` | 11 PASS, H ĐỎ `thieu len(c) == 1` | Hàm nhận hai mục khi bỏ chốt; head từ chối |
| `extra_rc_always1`: thay capture `$?` bằng `1` | 11 PASS, K ĐỎ vì mất chuỗi `|| RC_CAI=$?` | Batch bắt buộc `exit 47` đổi thành rc=1; chưa có ca hành vi bắt mã |
| `extra_source_no_cleanup` | **12 PASS: SỐNG** | Sau batch rc=0 còn một thư mục tạm; head không còn |
| `extra_required_exit42`: `exit "$RC_CAI"` → `exit 42` | 11 PASS, H ĐỎ vì mất chuỗi exit gốc | Batch bắt buộc `exit 47` đổi thành rc=42; ca C vẫn xanh |
| `extra_rc1_preserve_shape`: giữ capture, thêm `RC_CAI=1` trong nhánh lỗi | **12 PASS: SỐNG** | Cùng lỗi mất mã gốc, giữ được mọi chuỗi hình dạng |

Các log cùng tên mutant trong `evidence/`; bản biến thể cuối ở [log riêng](evidence/extra_rc1_preserve_shape_run.log). Kết quả chứng minh ca hình dạng có bắt các cách sửa trực tiếp, nhưng không thay thế phép đo mã gốc/dọn tạm.

`python3 evidence/probe_json.py` kiểm hàm tách từ script của bản sao đầy đủ với đầu ra JSON kiểm soát: head nhận một mục đúng tên và CRLF (rc=0); sai tên, hai mục, danh sách rỗng đều rc=1. Bỏ kiểm tên làm sai tên rc=0; bỏ kiểm len làm hai mục rc=0 ([log](evidence/json.log)). Đây là phép đo bổ sung, không phải bằng chứng Windows native.

**Shell, source và CRLF**

`python3 evidence/probe_shell.py`:

| Recipe | Base rc | Head rc |
|---|---:|---:|
| `false` | 1 | 1 |
| `exit 47` | 47 | 47 |
| `false; true` | 0 | 0 |
| `set -e; false; echo CONTINUED` | 1 | 0, có `CONTINUED` |

Vì vậy, mã cuối vẫn là mã recipe hỏng khi recipe thực sự kết thúc hỏng; không phải luôn là mã của mọi lệnh hỏng bên trong. `false; true` vốn đã rc=0 ở base vì `set +e`. Khác biệt mới là vô hiệu hoá cả lần bật lại `-e` trong eval (finding P3).

`python3 evidence/probe_behavior.py`: direct `exit 47` cho cả công cụ tuỳ chọn/bắt buộc và batch bắt buộc `exit 47` đều head/base rc=47. Với head, nhánh tuỳ chọn hỏng trong `--bat-buoc` trả 0, đi tới công cụ bắt buộc tiếp theo và kiểm toàn bộ; kết quả cuối gồm tuỳ chọn `KHONG_DO_DUOC`, bắt buộc `DAT`. `return 0` đúng ở lượt source có marker nội bộ; lỗi direct và lỗi bắt buộc dùng exit đúng ở các đối chứng đã đo. Head không để sót thư mục tạm; vấn đề cleanup ở đây là thiếu test bảo vệ, không phải head đang rò.

`t23_batch_chiu_duoc_stdout_CRLF_cua_python_windows` nằm trong bộ `cong_cu_test` 61/61. Đo thêm wrapper Python chuyển stdout thành CRLF qua **hàm mới**: `head_CRLF_selector` → rc=0, DAT, 19 CRLF; `head_CRLF_batch` → rc=0, 48 CRLF, vẫn đi tiếp qua công cụ bắt buộc. [Log byte/count](evidence/behavior.log), [JSON cuối batch](evidence/batch-json-summary.log). Không thấy vỡ CRLF trong mô phỏng này.

**Các đường gọi và giới hạn hồi quy**

`rg -n 'cai_cong_cu\.sh|cai_actionlint\.sh|kiem-tra --chi'` trên năm tệp được yêu cầu → [callsites.log](evidence/callsites.log):

- `ci.yml`, `ci-dot-bien-du.yml`: gọi trực tiếp shellcheck và rg; actionlint qua `cai_actionlint.sh` riêng.
- `launcher-windows.yml:92`: lặp shellcheck, rg, actionlint qua `cai_cong_cu.sh`.
- `ops/codex_cloud_setup.sh:85`: gọi trực tiếp actionlint, nhận GITHUB_PATH rồi kiểm các công cụ.
- `.claude/hooks/session-start.sh:218`: gọi `cai_actionlint.sh` riêng, không gọi `cai_cong_cu.sh`.

`python3 evidence/probe_linux_calls.py` chạy đúng script head/base với binary thật sẵn (rg 15.2.0, ShellCheck 0.9.0, actionlint 1.7.7). Để chỉ ghi trong sandbox, phần `sudo apt-get install` là fixture rc=0; actionlint cài từ archive đóng bằng binary cục bộ, hash tự đo qua AL_GOI/AL_SHA256, đích trong sandbox. Đây không phải phép cài apt/tải release thật.

| `bash ops/cai_cong_cu.sh <tên>` trong điều kiện trên | Head | Base |
|---|---|---|
| rg | rc=0, DAT, GITHUB_PATH rỗng, `ten tran da DAT` | giống head |
| shellcheck | rc=0, DAT, GITHUB_PATH rỗng, `ten tran da DAT` | giống head |
| actionlint | rc=0, DAT, GITHUB_PATH là đích cài | cùng hành vi, chỉ khác thư mục fixture |

[Log](evidence/linux-calls.log). Lần đầu archive giữ uid/gid 65534 gây tar rc=5 ở **cả hai bản**; đã lưu [log ban đầu](evidence/linux-calls-initial.log), sửa metadata fixture về uid/gid 0 rồi đo lại. Không quy lỗi giàn giáo ấy cho bản vá.

Không thấy đổi đỏ/xanh ngoài dự kiến trong ba đường gọi Linux đã đo. Phép gọi vắng tuỳ chọn đổi base xanh → head đỏ là thay đổi dự kiến. **KHÔNG ĐO ĐƯỢC** apt thật, lượt Windows native, CI PR và Windows workflow_dispatch/G5 của exact head trong các phép đo này; không dùng mô phỏng CRLF/Linux để nhận CI xanh. Các đường cloud setup/hook được đối chiếu callsite và suite, chưa chạy nguyên cả quy trình bootstrap có tác dụng ngoài sandbox.

**Phạm vi và kiểm tra tĩnh**

| Lệnh / bằng chứng | Output |
|---|---|
| `git -C cay-kho rev-parse HEAD` | `daedfb75e524fa6adc3d68db63b500c2d6c53730` |
| `sha256sum SPEC.md` | `8e187b9130e18a757f4f24dfcea6761f688a5f69e21d17356b198b8cc5bd508e` |
| `git diff --stat 059a4a5a080a98270973ef9ce23a38dad5aa2f38 HEAD` | đúng `.claude/dev/launcher_test.py`, `ops/cai_cong_cu.sh`; 199 thêm, 12 xoá; không chạm `ops/cong_cu.py`, `ops/cong_cu.yaml`, `ci.yml` |
| `git diff --check 059a4a5a080a98270973ef9ce23a38dad5aa2f38 HEAD` | head/base rc=0, output rỗng |
| `ruff check --no-cache --select F --output-format json .claude/dev/launcher_test.py scripts/tl.py` | head/base rc=1: 5 F841 ở launcher_test, 12 F821 ở tl.py; **delta=0** |
| `shellcheck ops/cai_cong_cu.sh` | head/base rc=1, đúng một SC1090 tại source; head dòng 118, base dòng 104; **delta=0** |
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | head/base rc=0: `sạch — đã quét 10 tệp, 0 chỗ chép doctrine` |
| `python3 evidence/summarize_static.py` | ruff đa tập (file tương đối, code, message) chênh hai chiều `{}`; DIFF.patch khớp byte với diff tự đo; source status rỗng |

[Static summary](evidence/static-summary.log), các log `head/base-ruff`, `head/base-shellcheck`, `head/base-doctrine` kèm `.rc` ở evidence. Tree head `4343526b981e50b0765fd7dfc1a31197463d969d`; tree base `3407b8ef9531fd9e15e273c9cc5870022860cedc`. Kho ứng viên không có thay đổi tracked/untracked sau phép đo; chỉ cấu hình core.abbrev được đặt theo yêu cầu.
