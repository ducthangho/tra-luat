verdict: approve
reviewed_head: 99b354ca7bcc40ce0c4f7d9db445b852510b5809
reviewed_sha: 99b354ca7bcc40ce0c4f7d9db445b852510b5809
reviewed_tree: a247775817d0bf1bec9a327a6a350975ca72e754
review_class: sensitive
provider: openai_codex
model: gpt-6.1-sol
model_family: openai
reasoning_effort: xhigh
execution_surface: codex_cli
transport: machine
review_round: 3/5

## Kết luận

**Approve trên exact head nêu trên.** Không phát hiện P0/P1/P2/P3 còn mở trong 6 tệp PR. H06/H07 lượt 2 đã được chốt bằng ca đúng và đột biến chết đúng `TinHieuChotCa`; tự đếm AST có 11 `wp886_cc_*`, cả 11 bị giết, đủ 16/16 lượt ca đích. N7 tự chạy đạt. Readback CI đã cung cấp đủ bằng chứng N8 và phần CI của M-3/M-5 theo yêu cầu lượt này, khắc phục lý do `pending` lượt 2.

**Tôi KHÔNG tự chạy được Windows.** Kết quả Windows bên dưới là đọc dữ liệu jobs/log đã lưu trong `evidence/ci-readback/`, có kiểm SHA, runner, checkout và marker dương; không phải phép đo Windows tại sandbox Linux. Không đổi `skipped` thành pass. Full launcher Linux có/không auth giả, toàn bộ launcher mutations và toàn bộ bán kính ops không được chạy lại tại chỗ trong lượt này: **KHÔNG ĐO ĐƯỢC**, xem bảng giới hạn. Approval review mã không cấp quyền merge/land/deploy và không xác nhận M-2 (thread remote) hoặc authority live.

## Neo

| Mục | Bằng chứng |
|---|---|
| Candidate HEAD | `99b354ca7bcc40ce0c4f7d9db445b852510b5809` |
| Candidate tree | `a247775817d0bf1bec9a327a6a350975ca72e754` |
| Base HEAD | `33e6d4c32d26663a87bbdd6f1350890fa6042cc5` |
| Base tree | `86c2596c9d80577601dd37891958e58be7ace11f` |
| Ancestry | `git -C cay-kho merge-base --is-ancestor <base> <head>` rc=0; base là cha của merge `a155182f0fd7ab5560b1e1438393714e5242eef8` |
| SHA-256 spec r1, tự băm đầu/cuối | `28d1bb708621c6d410aa2f22ba11f295a5a9407d74d7aa736ddd30421e4f96a6`, khớp |
| SHA-256 spec r2, tự băm đầu/cuối | `c019dbbacf838cddac40da8b360a0564c9383a10a07821735a7f3366ef72d68b`, khớp |
| Identity CLI công bố | `runs/a94adf40/stderr.log`: Codex v0.163.0, `gpt-6.1-sol`, effort `xhigh`, session `01a16bd3-28a8-7ba3-bd20-0310a43fbbd0` |
| Lease offline | wp886-r2-g2-claude, revision 2 / generation 2, hạn 2026-10-26T00:05:00Z; reviewer theo prompt lượt 3/5, không dùng quyền executor để sửa cây |
| Phạm vi thực đo | **6 tệp / 298 thêm / 33 xóa**, đạt trần 6/450 (M-4) |
| So bundle | Git diff base..head bằng byte `evidence/diff.patch`; diff từ `1c138c714f9c192ea730b65c5d18ff5eda1ca660` bằng byte `evidence/delta-tu-luot2.patch`; `git diff --check` rc=0 |
| Runtime | Linux x86_64, Python 3.13.16, Ruff 0.16.9; `cmd.exe`, `wine`, `pwsh` đều không có |

Model/effort là giá trị header CLI công bố, không suy từ tài khoản chuyển bằng chứng. Spec r1 giữ baseline lịch sử `e63961f27b53e66db8e6600009f97d5706743063`; base so PR của lượt này là master đã merge `33e6d4c...`, đúng chỉ định prompt. Không tự chuyển base theo master mới hơn. Bản sao lease/spec là authority offline được giao, không khẳng định đã kiểm lại trạng thái remote.

`git status --porcelain=v1` đầu lượt rỗng trên cả hai cây; cuối lượt chạy thêm `--untracked-files=all --ignored=matching`, rc=0, stdout/stderr rỗng. Snapshot nội dung, quyền tệp và đích symlink, kể cả `.git`, của head **5307/5307**, base **5306/5306**, mirror **539/539** mục đều giống đầu/cuối. SHA/tree không đổi. Chứng cứ [integrity/summary.json](integrity/summary.json) và `integrity/start-*.json`, `end-*.json` chỉ chứng minh hai mốc quan sát, không chứng minh mọi ghi trung gian. Sandbox thực tế là workspace-write; kỷ luật reviewer giữ nguồn read-only và mọi tệp tạo trong `out/`.

Hai bản sao thường `out/head`, `out/base` dựng trong **một lệnh** `PYTHONDONTWRITEBYTECODE=1 python3 -B out/setup_and_target.py`; chép test head (launcher + ops) sang bản base, giữ mã sản phẩm base. Không dùng worktree/hardlink tới nguồn. Các lệnh Python dùng `-B`, `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR=<sandbox>/out/tmp/`, `PIP_NO_INDEX=1`; Git dùng `GIT_OPTIONAL_LOCKS=0`. Fixture Git chỉ tắt ký commit qua env, không ép `core.abbrev` qua env (bản sao vốn ghim 7). Ruff dùng `--no-cache`. Không gọi mạng/GitHub, không sửa branch/sản phẩm.

| Tệp | Thêm / xóa | Đối chiếu scope |
|---|---:|---|
| `.claude/dev/launcher_test.py` | 226 / 16 | Ca r886, nâng r858 python, seam đột biến cong_cu và hoàn nguyên con trỏ; delta lượt 2 chỉ thêm test/mutant |
| `RELEASE_MANIFEST.json` | 11 / 6 | Verify strict đạt trên head; thay đổi lượt 3 chỉ ở test ngoài gói |
| `changelog.d/wp-886.md` | 9 / 0 | Fragment packet |
| `ops/cong_cu.py` | 39 / 5 | Giải tên theo PATH và lý do thiếu tên N4; không đổi từ lượt 2 |
| `ops/cong_cu_test.py` | 7 / 2 | Chỉ docstring/fixture `python_alias_behavior_test`, giữ chốt kỳ vọng; POSIX symlink, Windows `.cmd` có đuôi PATHEXT |
| `scripts/tl_selftest.py` | 6 / 4 | Ratchet 191→192 và chú thích slot |

AST ops test sau khi loại riêng fixture alias **giống hệt base** (`ci/summary.json:ops_scope`). Không có thay đổi ca khác, expectation khác hoặc skip mới trong ops test.

## Đối chiếu lượt 2

Nguồn `evidence/verdict-luot2.md`: verdict pending trên `1c138c714f9c192ea730b65c5d18ff5eda1ca660`, không có finding F886-NN mở. H06/H07 là đề nghị tăng răng, không phải lỗi chọn interpreter của bản sản phẩm. Không kế thừa approval cũ thành kết quả lần này.

| Mục lượt trước | Phân loại | Tự đo trên head này |
|---|---|---|
| H06 — bỏ qua tệp không thực thi | **ĐÃ VÁ THẬT ở test** | Baseline `r886_n1_bo_qua_tep_khong_thuc_thi` qua. `wp886_cc_bo_X_OK` chết đúng lớp `TinHieuChotCa`, stack `classify → r886_n1_bo_qua_tep_khong_thuc_thi → bang`, dòng test 8788, message `nhan tep khong thuc thi duoc: [.../d/python]` |
| H07 — cùng tên, thư mục đầu PATH thắng | **ĐÃ VÁ THẬT ở test** | Baseline N6 qua. `wp886_cc_dao_thu_tu_PATH` chết đúng `TinHieuChotCa`, stack `classify → r886_n6_giai_ten_tinh_windows_va_posix → bang`, dòng 8771, message `cung ten o hai thu muc ma khong lay thu muc dau PATH: [.../e/python]` |
| H01 lượt 1 (đã đóng ở lượt 2) | **Vẫn đóng** | `wp886_cc_bo_muc_PATH_rong` tiếp tục chết đúng N6, không chỉ kiểm tồn tại assertion |
| N8 chưa có CI Windows | **Đã có bằng chứng đọc lại** | `gate-cong-cu (windows-latest, 0)` job 120742924486 success trên đúng SHA; 59/59, 0 tiền kiểm bỏ qua; launcher Windows cũng success, chi tiết dưới |

Lệnh `python3 -B out/run_mutations.py` rc=0. Mỗi neo đột biến khớp đúng một chỗ, compile trước chạy, tên tệp mutant riêng. Chỉ đúng lớp `TinHieuChotCa`, frame ca đích và không có ca đăng ký khác trong stack được tính kill. Bộ phân loại tự kiểm **6/6**: chốt đúng, AttributeError, AssertionError trần, chốt ca khác, pass, skip. Chi tiết [mutations/all.json](mutations/all.json), [mutations/classifier-controls.json](mutations/classifier-controls.json).

Đo thêm **chính phần test mới**: bỏ riêng assertion thứ tự mới trong N6 thì mutant đảo PATH sống (`hunts/delta_n6_assertion_ablation.json`). Sau đó đổi điều kiện `bang` mới của từng ca X_OK/N6 thành True trên bản sao test: cả 2 bị `review_delta_test_teeth` giết bằng `TinHieuChotCa` với message `delta assertion has no teeth`; baseline meta-test trước đó xác minh sản phẩm tốt qua, mutant sản phẩm chết đúng ca. Lệnh `python3 -B out/check_delta_teeth.py` rc=0; [hunts/delta-test-meta-mutations.json](hunts/delta-test-meta-mutations.json). Không viết patch sản phẩm.

## Bảng finding

| ID | Mức P0–P3 | Tệp:dòng | Bằng chứng | Hướng sửa bằng lời |
|---|---|---|---|---|
| — | — | — | Không có finding P0/P1/P2/P3 mới được chứng minh trong phạm vi bản vá. | Không yêu cầu sửa sản phẩm. |

Không cấp F886-NN cho hạn chế nền, ca chưa đo trọn, đột biến reviewer cố ý tạo, hoặc job vốn chỉ dành Ubuntu bị skipped khi chạy windows-only.

## Bảng N1–N8

| N | Kết quả | Bằng chứng và giới hạn |
|---|---|---|
| N1 | ĐẠT trong phép đo đã nêu | r886_n1 và ca X_OK mới qua Linux; mutant sys.executable, tên/PATH đảo, bỏ X_OK đều chết đúng ca. CI Windows thực có N1/mutant tương ứng; X_OK POSIX không suy sang Windows |
| N2 | ĐẠT | Head không DAT với python hỏng đứng trước python3 tốt; base+test-head đỏ đúng TinHieuChotCa tại N2, message base vẫn DAT phiên bản 3.13.16 (`targeted/base-n2-classification.json`) |
| N3 | ĐẠT Linux | Ca chỉ python3 qua; probe PyYAML ở interpreter `-S` thấy 9.9.9 giả, vắng thì không DAT; Windows ca POSIX này skipped, còn fixture chỉ-python3 N8 đã qua trên Windows |
| N4 | ĐẠT | Không có ba tên → rc=3, KHONG_DO_DUOC, chi tiết đủ python/python3/py; cả mutant fallback lẫn bỏ lý do bị giết |
| N5 | ĐẠT tập ca liên quan chạy được; ghi riêng lỗi nền | Mọi r858 ngoài gốc-tạm qua head; ca python đầy đủ mới đỏ trên base. Ops Linux 61/61 + 2/2 tiền kiểm cả hai bên. r858_goc_tam đỏ cả hai do /var/tmp read-only; không coi ca ấy xanh. Full launcher tại chỗ KHÔNG ĐO ĐƯỢC |
| N6 | ĐẠT phép tĩnh tại chỗ và đọc bằng chứng CI Windows | N6 qua, mutant PATHEXT/native/PATH/-3 chết đúng ca; launcher Windows thực 248/248 mutant đo được, sàn 248/325=76,31% ≥70%; 77 không đo được giữ riêng |
| N7 | ĐẠT tự chạy | `release-verify --strict --json` rc=0, ok=true, expected=checked=192; `tl.py --selftest` rc=0, 1731/1731 |
| N8 | ĐẠT theo CI readback + Linux tự chạy | Fixture alias Linux qua ở cả hai bên. Windows job success, đúng checkout/head/runner, tiền kiểm bỏ qua=0 chứng minh alias được thực thi và qua. Mutant tên không đuôi bị ca tĩnh reviewer giết. Windows tại chỗ KHÔNG ĐO ĐƯỢC |

## Ca đích và hai vế

Lệnh dựng/chạy cả hai vế: `PYTHONDONTWRITEBYTECODE=1 python3 -B out/setup_and_target.py` rc=0. Mỗi ca chạy qua CLI thật `python3 -B .claude/dev/launcher_test.py --lap-ca <TÊN> --lan 1`; command/cwd/rc/stdout/stderr riêng tại `targeted/<head|base>/<TÊN>.json`. Đã chạy tất cả r886, tất cả r858 (bao gồm mọi r858_cai_python_*), và r802 con trỏ.

| Ca | Head rc | Base + test head rc |
|---|---:|---:|
| `r858_goc_tam_tranh_to_tien_co_git` | 1 | 1 |
| `r802_runner_tra_lai_con_tro_nguoi_goi` | 0 | 0 |
| `r858_cai_linux_chon_ban_chay_duoc` | 0 | 0 |
| `r858_cai_macos_chon_ban_chay_duoc` | 0 | 0 |
| `r858_cai_windows_chon_ban_chay_duoc` | 0 | 0 |
| `r858_cai_python_khong_in_thu_muc_ban_hong` | 0 | 1 |
| `r886_n1_ten_tran_theo_path_moi_nen` | 0 | 1 |
| `r886_n2_python_hong_dau_path_khong_DAT` | 0 | 1 |
| `r886_n3_chi_python3_DAT_va_do_dung_interpreter` | 0 | 1 |
| `r886_n4_khong_ten_nao_noi_ro_thieu_gi` | 0 | 1 |
| `r886_n6_giai_ten_tinh_windows_va_posix` | 0 | 1 |
| `r886_n1_bo_qua_tep_khong_thuc_thi` | 0 | 1 |
| `r886_ten_python_khop_cai_cong_cu_sh` | 0 | 1 |
| `r858_bat_buoc_bash_khong_dua_rg_hong_len_dau` | 0 | 0 |
| `r858_hinh_dang_cong_thuc_cai` | 0 | 0 |
| `r858_selftest_editskill_thu_muc_rieng` | 0 | 0 |

Head **15/16 qua**, base **7/16 qua**; không có ca head đỏ mà base xanh. Lỗi head duy nhất là `r858_goc_tam_tranh_to_tien_co_git`: cả hai vế `[Errno 30] Read-only file system: '/var/tmp/lt_...'`. Ca cố tránh tổ tiên `/tmp/.git` vốn là mount rỗng read-only; không đổi quyền/mount hay vá test để ép qua. N6, ca X_OK và Q1 trên base thiếu helper/hằng mới (AttributeError): đó là đối chứng không tương thích API, **không cấp tín dụng kill**. N2 được phân loại độc lập, chết vì chốt hành vi thật.

Ops Linux hai vế cùng một lệnh `PYTHONDONTWRITEBYTECODE=1 python3 -B out/run_ops_baselines.py` rc=0: head rc=0 **61/61 CA + 2/2 tiền kiểm**, 57,802s; base+test-head rc=0 **61/61 + 2/2**, 58,260s; không skip/fail. Gọi nguyên thân ca và tiền kiểm trong module, không sửa expectation/CA; đây là **baseline 63 hàm**, không phải tuyên bố đã chạy trọn main ops hay bán kính 490. Dữ liệu từng ca và log ở [ops-baseline/summary.json](ops-baseline/summary.json), `ops-baseline/<head|base>/cases.json`.

## N8, M-3, M-5 — đọc bằng chứng CI

Lệnh kiểm offline `PYTHONDONTWRITEBYTECODE=1 python3 -B out/read_ci_and_scope.py` rc=0. Dữ liệu nguồn là ba jobs JSON và hai log đầy đủ do prompt xác định là readback API; không dùng lời kể executor làm kết quả chạy. [ci/summary.json](ci/summary.json) giữ từng job, phép so SHA/runner, số dòng log, băm bytes log và AST ca bỏ qua.

| Run | Phạm vi theo bundle | Tự kiểm jobs JSON |
|---|---|---|
| 40050753537 | ci.yml pull_request, Ubuntu | **23/23 success**, tất cả head_sha đúng, runner_id dương, nhãn ubuntu-latest; đủ 8 gate-cong-cu (0..7) và gate-cong-cu-gop (ubuntu-latest) success |
| 40050767584 | ci.yml dispatch windows-only | **15 success, 1 skipped**; 15 job thực thi có runner_id dương; chuan-bi Ubuntu, 14 job Windows; cả 16 head_sha đúng |
| 40050769532 | launcher-windows.yml dispatch | **1/1 success**, launcher (windows-latest), runner_id=1000018848, head_sha đúng |

Đã so **40/40 `head_sha`** với `99b354ca7bcc40ce0c4f7d9db445b852510b5809`; **39/39 job thực thi** có `runner_id > 0`, nhãn phù hợp, conclusion success. Ngoại lệ phải ghi đúng: job **120743668248 `gate-cong-cu-gop`** là **skipped**, `runner_id=null`, `labels=[]`. Không nói mọi job đã có runner. Điều kiện `.github/workflows/ci.yml:594` và exclude Windows chỉ gom khi ma trận chứa Ubuntu, đã có ở base; do đó windows-only không có gì để gom, không phải ca bị né bởi PR. Job Windows cần cho N8 là **120742924486**, `gate-cong-cu (windows-latest, 0)`, **success**, runner_id **1000018870**, nhãn **windows-latest**.

Hai log Windows còn có `git log -1 --format=%H` sau checkout: ops dòng **823–824**, launcher dòng **161–162**, đều exact head này. Không chỉ tin trường head_sha của job. Runtime log: ops CPython 3.12, launcher CPython 3.13.16. Lượt này không tự truy API để kiểm run attempt/event hay workflow-definition OID độc lập; không suy run head thành synthetic merge hoặc workflow-definition provenance. Các giới hạn provenance ngoài trường/log bundle có sẵn vẫn **KHÔNG ĐO ĐƯỢC**.

### Ops Windows và alias

`log-gate-cong-cu-windows-120742924486.txt:1059`:

```text
cong_cu_test: 59/59 đạt; tổng=61, bỏ qua=2, tiền kiểm bỏ qua=0
```

`main()` (`ops/cong_cu_test.py:9058`) gọi hai tiền kiểm, trong đó có `python_alias_behavior_test`, trước vòng CA. `_chay_tien_kiem` (dòng 4905) chỉ bắt `BoQuaMoiTruong`, trả tên/lý do và đếm riêng; lỗi chốt nghiệp vụ không bị nuốt. Vì mã ngoài fixture AST giống base, log có **0 tiền kiểm bỏ qua**, job success và dòng tổng 59/59, có đủ bằng chứng **alias đã chạy và qua trên Windows**, không phải alias nằm trong số 59 CA hay bị silently skipped. Không có dòng pass riêng tên alias trong log; kết luận dựa cả đường gọi/lớp bắt lỗi và marker dương.

Hai dòng **BỎ QUA** thực tế của log ops, giữ lý do nguyên nội dung:

- Dòng 1056: `  BỎ QUA t51_cache_phai_HET_HIEU_LUC_khi_chinh_TEP_ung_vien_doi: nền này không có /bin/sh để dựng ứng viên giả — KHÔNG ĐO ĐƯỢC`
- Dòng 1057: `  BỎ QUA t48_khung_INDEX_giu_BYTES_va_anh_chup_ghim_BLOB: nền này không đặt được tên tệp có ký tự điều khiển: [Errno 22] Invalid argument: 'C:\\Users\\RUNNER~1\\AppData\\Local\\Temp\\tmps5k97q2c\\khung\\ops\\va\r.py'`

Đối chiếu base: `t51_cache_phai_HET_HIEU_LUC_khi_chinh_TEP_ung_vien_doi` base:6017/head:6022 có cùng AST, guard thiếu `/bin/sh` không đổi; `t48_khung_INDEX_giu_BYTES_va_anh_chup_ghim_BLOB` base:6536/head:6541 cùng AST, tên chứa CR không hợp lệ trên Windows. Phù hợp hạn chế nền và ghi chú wp879 trong base, không phải sửa để né N8. Giữ kết quả **59 ca thực thi qua / 2 ca không đo được**, không khai 61/61 Windows.

Log dòng 1061 còn nói rõ **490 đột biến ops KHÔNG ĐO TRÊN WINDOWS**, được giao Ubuntu 8 mảnh + job gom. Không trộn con số này với launcher mutants. Bằng chứng Linux baseline của reviewer ở trên; bằng chứng CI đủ 8 mảnh/gom success nằm ở jobs-40050753537.json. Không có raw log ops Ubuntu trong bundle nên không tự gán một headline Ubuntu N/M chưa đọc được.

N8 có thêm phản chứng tĩnh cho fixture: `python3.cmd` → `python3` trên bản sao, chạy **thân fixture nhánh Windows** với seam `os.name`, kiểm tên tệp trước khi thay lời gọi subprocess bằng stub. Baseline quan sát `['python3.cmd']`; mutant `TinHieuChotCa`, frame `review_n8_fixture_suffix`, message `N8 static fixture requires native suffix, got ['python3']`. Lệnh `python3 -B out/run_supplemental.py` rc=0; [hunts/n8-fixture-static-mutation.json](hunts/n8-fixture-static-mutation.json). Đây là ca tĩnh được N8 cho phép, **không phải chạy CMD hay original probe Windows**; Linux alias thực đã chạy riêng và bằng chứng runtime Windows đến từ CI.

### Launcher Windows

Log `log-launcher-windows-120742710896.txt:503`:

```text
210/210 ca DA CHAY QUA (tong 259, bo qua 49, hong 0) - KHONG DU: 49 ca BO QUA, chua do gi
```

Dòng 865: `DOT BIEN: 248/248 dat  (77 khong do duoc tren nen nay)`. Tổng **325**, sàn đo được **248/325 = 76,31%**, vượt 70%. Không khai toàn bộ 259 ca hoặc 325 mutant đều đã đo được; headline legacy không tự xác minh stack của từng mutant ngoài wp886.

Các dòng wp886 thực tế (dòng 844–854):

```text
wp886_cc_ve_sys_executable   OK  giet 2/2: r886_n1_ten_tran_theo_path_moi_nen, r886_n2_python_hong_dau_path_khong_DAT
wp886_cc_python3_truoc_python OK  giet 2/2: r886_n2_python_hong_dau_path_khong_DAT, r886_ten_python_khop_cai_cong_cu_sh
wp886_cc_bo_python3          OK  giet 1/1: r886_ten_python_khop_cai_cong_cu_sh
wp886_cc_py_mat_tru_3        OK  giet 2/2: r886_n6_giai_ten_tinh_windows_va_posix, r886_ten_python_khop_cai_cong_cu_sh
wp886_cc_khong_ten_roi_ve_sys_executable OK  giet 1/1: r886_n4_khong_ten_nao_noi_ro_thieu_gi
wp886_cc_bo_ly_do_thieu_ten  OK  giet 1/1: r886_n4_khong_ten_nao_noi_ro_thieu_gi
wp886_cc_windows_nhan_ten_tran OK  giet 1/1: r886_n6_giai_ten_tinh_windows_va_posix
wp886_cc_bo_muc_PATH_rong    OK  giet 1/1: r886_n6_giai_ten_tinh_windows_va_posix
wp886_cc_bo_X_OK             KHONG DO DUOC tren nen nay (ca dich bo qua: r886_n1_bo_qua_tep_khong_thuc_thi)
wp886_cc_dao_thu_tu_PATH     OK  giet 1/1: r886_n6_giai_ten_tinh_windows_va_posix
wp886_cc_path_truoc_ten      OK  giet 1/1: r886_n6_giai_ten_tinh_windows_va_posix
```

10/11 wp886 đo được trên Windows có kill; riêng X_OK **KHÔNG ĐO ĐƯỢC** vì ca POSIX bỏ qua. Không lấy 11/11 Linux thay cho 11/11 Windows.

Đã liệt kê đủ 49 dòng skip launcher và đối chiếu AST với base ở bảng sau. **46/49** ca có AST nguyên vẹn trên base. Ca r858 python có sẵn guard POSIX từ base, PR chỉ tăng chốt dưới guard; r886_n3 cần shell POSIX (đã có từ lượt 2); ca X_OK mới chỉ đo POSIX, không thể phân biệt mutation đó trên Windows theo cơ chế nền dùng trong suite. Hai r886 mới/thuộc PR không phải skip làm né N8: chúng xanh và mutant chết trên Linux; Windows N8 được tiền kiểm native `.cmd` đo riêng. Đây là giới hạn phạm vi cần giữ, không gọi các ca đó pass Windows.

| Dòng log | Ca và lý do BO QUA thực tế | Đối chiếu base |
|---|---|---|
| 452 | BO QUA t03_git_gia_thoat_0_im_lang_van_bi_chan: bo qua tren Windows (can shim .cmd) | AST giống base |
| 453 | BO QUA t28_qua_han_giet_ca_CON_CHAU: bo qua tren Windows (can kiem bang cay tien trinh that) | AST giống base |
| 454 | BO QUA t33_stop_giet_that: bo qua tren Windows | AST giống base |
| 455 | BO QUA t50_stop_roi_runner_KHONG_duoc_de_len_so: bo qua tren Windows (can kiem rieng) | AST giống base |
| 456 | BO QUA t51_ma_thoat_ngoai_khoang_khong_bi_cat_cut: bo qua tren Windows (can tin hieu POSIX) | AST giống base |
| 457 | BO QUA t55_doctor_nhan_python_khong_can_ten_python3: bo qua tren Windows (can shim khong duoi .exe) | AST giống base |
| 458 | BO QUA t60_doctor_KHONG_tin_which_khi_cong_cu_khong_chay_duoc: bo qua tren Windows (can .exe rong) | AST giống base |
| 459 | BO QUA t63_chau_phot_lo_SIGTERM_ma_bao_da_giet_ca_cay_la_noi_doi: ca nay dung SIG_IGN cua POSIX; duong Windows la t62 | AST giống base |
| 460 | BO QUA t67_chau_sinh_SAU_luc_chup_van_phai_bi_dem: dua tren SIGTERM cua POSIX; duong Windows la t62 | AST giống base |
| 461 | BO QUA t66_chau_setsid_roi_khoi_nhom_van_phai_bi_giet: setsid la khai niem POSIX; duong Windows la t62 | AST giống base |
| 462 | BO QUA t76_wrapper_thoat_khong_duoc_xoa_prompt_cua_chau: ca nhom tien trinh POSIX; Windows can fixture that rieng | AST giống base |
| 463 | BO QUA t72_bi_ngat_KHONG_duoc_ghi_thanh_xong: SIGINT tren Windows khong cung ngu nghia; can ca rieng | AST giống base |
| 464 | BO QUA t108_hook_phai_probe_CHAY_DUOC_khong_chi_CO_MAT: bo qua tren Windows (can shim .cmd cho fixture) | AST giống base |
| 465 | BO QUA t125_bridge_bo_bash_hong_dau_PATH_va_truyen_rc_hook_ve_nguyen_ven: bo qua tren Windows (can fake bash .exe chay duoc; duong POSIX do o CI ubuntu) | AST giống base |
| 466 | BO QUA t126_bridge_hook_vuot_han_phai_rc124_khong_phai_treo_hay_0: bo qua tren Windows (can fake bash .exe chay duoc; duong POSIX do o CI ubuntu) | AST giống base |
| 467 | BO QUA r351_co_chi_thi_thi_KHONG_duoc_dat_moc: bo qua: khoi dat moc la shell POSIX | AST giống base |
| 468 | BO QUA r351_KHONG_co_chi_thi_thi_van_phai_dat_moc: bo qua: khoi dat moc la shell POSIX | AST giống base |
| 469 | BO QUA r484_g2_hook_shell_scrub_truoc_probe: BO QUA shell POSIX; verified on WSL Linux | AST giống base |
| 470 | BO QUA r484_g8_hook_scrub_kin_voi_bash_env: BO QUA shell POSIX; verified on WSL Linux | AST giống base |
| 472 | BO QUA r484_g6_trust_posix_backslash_is_not_separator: POSIX literal backslash semantics measured on Linux | AST giống base |
| 473 | BO QUA r484_g7_bridge_codex_co_mat_nhung_hong_van_hoan: BO QUA shim POSIX | AST giống base |
| 474 | BO QUA r484_g7_hook_vang_codex_cai_cli_truoc_materialize: BO QUA shell POSIX | AST giống base |
| 475 | BO QUA r484_g7_auth_doi_truoc_khi_thay_thi_giu_ban_moi: đo trên POSIX; nhánh Windows dùng cùng phép đọc lại trước os.replace | AST giống base |
| 476 | BO QUA r802_cai_rg_windows_chon_ban_chay_duoc: BO QUA shell POSIX | AST giống base |
| 477 | BO QUA r802_hook_linux_rg_hong_van_thu_cargo: BO QUA shell POSIX | AST giống base |
| 478 | BO QUA r802_hook_windows_khong_cai_in_dung_lenh: BO QUA shell POSIX | AST giống base |
| 479 | BO QUA r831_cai_rg_linux_chon_ban_chay_duoc: BO QUA shell POSIX | AST giống base |
| 480 | BO QUA r831_cai_rg_macos_chon_ban_chay_duoc: BO QUA shell POSIX | AST giống base |
| 481 | BO QUA r858_cai_linux_chon_ban_chay_duoc: BO QUA shell POSIX | AST giống base |
| 482 | BO QUA r858_cai_macos_chon_ban_chay_duoc: BO QUA shell POSIX | AST giống base |
| 483 | BO QUA r858_cai_windows_chon_ban_chay_duoc: BO QUA shell POSIX | AST giống base |
| 484 | BO QUA r858_cai_python_khong_in_thu_muc_ban_hong: BO QUA shell POSIX | Guard POSIX có sẵn; tăng chốt dưới guard |
| 485 | BO QUA r886_n3_chi_python3_DAT_va_do_dung_interpreter: BO QUA shell POSIX | Ca POSIX từ lượt 2; Linux đã đo |
| 486 | BO QUA r886_n1_bo_qua_tep_khong_thuc_thi: BO QUA X_OK khong co nghia tren Windows | Ca X_OK POSIX mới; Linux đã đo |
| 487 | BO QUA r858_bat_buoc_bash_khong_dua_rg_hong_len_dau: BO QUA shell POSIX | AST giống base |
| 488 | BO QUA r868_kenh_rieng_khong_doc_stdout_trinh_cai: BO QUA shell POSIX | AST giống base |
| 489 | BO QUA r868_writer_muon_khong_lam_treo: BO QUA shell POSIX | AST giống base |
| 490 | BO QUA r868_khong_bo_chon_doc_dong_cuoi: BO QUA shell POSIX | AST giống base |
| 491 | BO QUA r868_doc_kenh_hong_thi_dung: BO QUA shell POSIX | AST giống base |
| 492 | BO QUA r868_ghi_kenh_hong_thi_dung: BO QUA shell POSIX | AST giống base |
| 493 | BO QUA r868_don_kenh_khi_loi: BO QUA shell POSIX | AST giống base |
| 494 | BO QUA r868_vong_duyet_ung_vien: BO QUA shell POSIX | AST giống base |
| 495 | BO QUA t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan: bo qua: nhanh /proc chi co tren Linux | AST giống base |
| 496 | BO QUA t157_giet_cay_khi_stat_EACCES_van_tron_ven: bo qua: nhanh /proc chi co tren Linux | AST giống base |
| 497 | BO QUA r743_con_song_tham_do_bang_stat_giu_errno_moi_phien_ban: bo qua: nhanh /proc chi co tren Linux | AST giống base |
| 498 | BO QUA t158_comm_hong_SAU_luc_sinh_qua_han_khong_duoc_124_khi_con_song: bo qua: comm/prctl/proc chi co tren Linux | AST giống base |
| 499 | BO QUA t159_chuong_trinh_ten_tieng_Viet_qua_han_phai_giet_duoc: bo qua: comm/proc chi co tren Linux | AST giống base |
| 500 | BO QUA t160_giet_cay_chau_setsid_comm_hong_phot_lo_SIGTERM: bo qua: setsid/proc chi co tren Linux | AST giống base |
| 501 | BO QUA t161_giet_cay_me_da_thoat_chau_cung_nhom_comm_hong: bo qua: nhom tien trinh/proc chi co tren Linux | AST giống base |

## Bảng đột biến

Đếm bằng AST chính danh sách `DOT_BIEN_HOOK`, không grep comment/chuỗi: **11** tên bắt đầu `wp886_cc_` ([mutations/ast-count.json](mutations/ast-count.json)). Lượt 2 có 9; hai mục mới đúng là X_OK và đảo thứ tự PATH. Các bản sao mutant tại `mutations/*.py`; không đụng `cay-kho/`, `nen/` hay mirror. Baseline mọi ca đích đều qua trước khi cấp tín dụng.

| Mutant có sẵn | Giết đúng ca / số ca | Ca đích thực chạy | Lỗi vô can |
|---|---:|---|---:|
| `wp886_cc_ve_sys_executable` | 3/3 | `r886_n1_ten_tran_theo_path_moi_nen`, `r886_n2_python_hong_dau_path_khong_DAT`, `r858_cai_python_khong_in_thu_muc_ban_hong` | 0 |
| `wp886_cc_python3_truoc_python` | 2/2 | `r886_n2_python_hong_dau_path_khong_DAT`, `r886_ten_python_khop_cai_cong_cu_sh` | 0 |
| `wp886_cc_bo_python3` | 2/2 | `r886_n3_chi_python3_DAT_va_do_dung_interpreter`, `r886_ten_python_khop_cai_cong_cu_sh` | 0 |
| `wp886_cc_py_mat_tru_3` | 2/2 | `r886_n6_giai_ten_tinh_windows_va_posix`, `r886_ten_python_khop_cai_cong_cu_sh` | 0 |
| `wp886_cc_khong_ten_roi_ve_sys_executable` | 1/1 | `r886_n4_khong_ten_nao_noi_ro_thieu_gi` | 0 |
| `wp886_cc_bo_ly_do_thieu_ten` | 1/1 | `r886_n4_khong_ten_nao_noi_ro_thieu_gi` | 0 |
| `wp886_cc_windows_nhan_ten_tran` | 1/1 | `r886_n6_giai_ten_tinh_windows_va_posix` | 0 |
| `wp886_cc_bo_muc_PATH_rong` | 1/1 | `r886_n6_giai_ten_tinh_windows_va_posix` | 0 |
| `wp886_cc_bo_X_OK` | 1/1 | `r886_n1_bo_qua_tep_khong_thuc_thi` | 0 |
| `wp886_cc_dao_thu_tu_PATH` | 1/1 | `r886_n6_giai_ten_tinh_windows_va_posix` | 0 |
| `wp886_cc_path_truoc_ten` | 1/1 | `r886_n6_giai_ten_tinh_windows_va_posix` | 0 |

**11/11 mutant bị giết, 16/16 lượt đúng chốt, 0 skip, 0 lỗi vô can được tính kill.** Chi tiết message/type/frame và cặp neo/thay nguyên văn trong từng JSON. Không dùng rc của runner legacy thay chứng minh đúng lớp tín hiệu.

Mutant reviewer bổ sung, tất cả baseline qua rồi mới đo âm:

| Mutant reviewer trên bản sao | Ca giết bằng TinHieuChotCa | Kết quả |
|---|---|---|
| Chấp nhận directory thay regular file | `review_h11_file_types` | kill, `file type confused: [.../directory/python]` |
| Đổi trạng thái lỗi timeout từ DO sang KHONG_DO_DUOC | `review_h13_timeout` | kill, `timeout misclassified` |
| Đổi exact tên python thành prefix startswith | `review_h14_dispatch` | kill, `dispatch rewrote python3: (0, 'one\n', None)` |
| Bỏ hoàn nguyên CONG_CU_DANG_DUNG trong finally | `review_h15_restore` | kill, `cong_cu pointer not restored on assertion` |
| Làm điều kiện bang X_OK mới luôn True | `review_delta_test_teeth` | kill; mutant sản phẩm bỏ X_OK sống qua test đã yếu đi |
| Làm điều kiện bang thứ tự N6 mới luôn True | `review_delta_test_teeth` | kill; mutant sản phẩm đảo PATH sống qua test đã yếu đi |
| Fixture Windows bỏ .cmd | `review_n8_fixture_suffix` (tĩnh) | kill; không gọi đây là đo CMD runtime |

**7/7** phản chứng reviewer bị chặn đúng chốt của reviewer. Các mutant này là công cụ đánh giá, không phải finding về head sạch. Cặp neo/thay hoặc AST edit và đầu ra nằm trong `run_hunts.py`, `check_delta_teeth.py`, `run_supplemental.py` cùng `hunts/*.json`.

## Hướng săn độc lập mới

Các hướng sau là H11–H15, khác H01–H10 lượt 2 (không đếm lại PATHEXT, quoting, symlink privilege, T7/module interpreter, argv py -3, X_OK, thứ tự PATH, scope merge hay core.abbrev). Lệnh chung **`PYTHONDONTWRITEBYTECODE=1 python3 -B out/run_hunts.py`**, rc=0, mỗi hàm/phép dưới đây có JSON cùng tên trong `hunts/` và output thật trong `logs/hunts.log`.

| Hướng | Giả thuyết và lệnh/phép chạy | Output thật | Kết luận |
|---|---|---|---|
| H11 — loại đối tượng hệ tệp | `review_h11_file_types`: directory tên python và symlink đứt phía trước python3 hợp lệ có thể được nhận nhầm chỉ vì X_OK | resolved=`good/python3`; `_chay`=`[0,"Python 8.8.8\n",null]`; mutant isfile→exists chết `TinHieuChotCa` | Không lỗi trên Linux; guard regular-file có tác dụng, độc lập quyền thực thi/thứ tự PATH |
| H12 — tìm thấy nhưng không exec được | `review_h12_exec_format`: python có quyền exec nhưng sai định dạng, python3 tốt cạnh đó; có thể fallthrough làm DAT giả | `_chay`=`[null,"","khong_khoi_chay:OSError"]`; state=`KHONG_DO_DUOC`; chi tiết giữ OSError | Không fallback sang python3 để che bản python đã chọn hỏng; không ném ra ngoài |
| H13 — timeout của interpreter đã chọn | `review_h13_timeout`: python ngủ 5s, python3 tốt; timeout=0.15s qua `_chay` thật, rồi kiem_tra_1 cùng seam timeout | `[null,"","qua_han"]`; state=`DO`; detail=`probe 'mac_dinh' da chay nhung qua han`; mutant đổi trạng thái chết | Giữ khác biệt đã chạy nhưng quá hạn với không khởi chạy, không tìm interpreter khác |
| H14 — biên dispatch exact tên | `review_h14_dispatch`: đổi resolver có thể lan sang python3/python-tool/đường tuyệt đối | python→`one`, python3→`three`, python-tool→`tool`, absolute python3→`three`, đều rc=0; mutant startswith chết đúng ca | Chỉ bare python được viết lại; tên khác và đường tuyệt đối giữ hành vi |
| H15 — hoàn nguyên đích mới của runner | `review_h15_restore`: con trỏ cong_cu người gọi cấp có thể rò sau chốt đúng hoặc lỗi ValueError; r802 chỉ canh hook/yaml | Chốt đúng: `counts=[0,0]`, `restored=true`, `OK giet 1/1`; ValueError: `counts=[1,0]`, `restored=true`, `SAI giet 0/1`; tệp caller nguyên byte; mutant bỏ restore chết | Đích cong_cu mới được định tuyến/hoàn nguyên đúng và lỗi vô can không bị tính kill; kiểm riêng phần harness của bản vá |

Đo bổ sung cho delta test (không tính vào số hướng mới ở trên): hạ riêng hai assertion mới và phép bỏ assertion N6, bằng chứng meta-test đã ghi ở mục đối chiếu. Đo bổ sung N8 fixture là nghĩa vụ nghiệm thu, không đếm lại H01 lượt trước thành hướng mới.

## Cổng đã chạy và giới hạn

| Cổng / lệnh | rc và bằng chứng dương | Phạm vi |
|---|---|---|
| `python3 -B scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | rc=0; ok=true; expected=checked=192; failed/extra/missing/errors rỗng; hash expected=current=full_tree `e280f452ad090a874c90f35c6310476e02cb32b400e3a7a6e569d7b4959b2929` | Head copy đúng bytes; `gates/release.json` |
| `python3 -B scripts/tl.py --selftest` | rc=0; **1731/1731**; timeout=false; 239,492s | Head; `gates/selftest.json`. Dòng retry `TL_SELFTEST_NO_NET` là fixture selftest, không coi log stderr rỗng là điều kiện pass |
| `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .` | rc=0; `sạch — đã quét 10 tệp, 0 chỗ chép doctrine` | `gates/doctrine.json`; không thay review ngữ nghĩa |
| `python3 -B scripts/tl.py doc-claims-check --strict` | rc=0; ok=true | `gates/doc-claims.json` |
| `python3 -B ops/cong_cu.py kiem-tra --chi <python/PyYAML/jsonschema> --json` | rc=0/0/0; DAT, phiên bản 3.13.16 / 6.0.3 / 4.26.0 | Container thật, riêng từng công cụ; không khai đã quét canary toàn bộ; `gates/real-*.json` |
| `ruff check --no-cache --select F --output-format json ops/cong_cu.py ops/cong_cu_test.py .claude/dev/launcher_test.py scripts/tl_selftest.py scripts/tl.py` | rc base/head=1/1; **4411/4411 diagnostics**, delta mới=0 | Bare Ruff 0.16.9 thực chạy trên hai bản sao; so path tương đối/code/message/multiplicity, không so số dòng dịch; không gọi lint tuyệt đối xanh; `gates/ruff-*.json` |
| Targeted launcher / 11 wp886 mutants | Hoàn tất, kết quả đúng ca ở bảng riêng | Không thay full launcher |
| Ops baseline 61 CA + 2 tiền kiểm | Head/base cùng 63/63 hàm qua, rc=0/0; không skip | Không thay toàn bộ main hoặc bán kính |
| Full launcher Linux có/không CODEX_AUTH_JSON giả | **KHÔNG ĐO ĐƯỢC trong lượt này (not_run)** | Không chạy suite rất lâu; theo prompt ưu tiên ca đích. Không suy N/N từ ca chọn lọc hoặc từ verdict cũ |
| Full `launcher_test.py --dot-bien` Linux | **KHÔNG ĐO ĐƯỢC trong lượt này (not_run)** | 11 wp886 được tự đo đầy đủ; headline Windows 248/248 là CI readback, không thay full Linux |
| Full main `ops/cong_cu_test.py`, bán kính 490 tại chỗ | **KHÔNG ĐO ĐƯỢC trong lượt này (not_run)** | Tự chạy toàn bộ 61 CA + tiền kiểm; CI Ubuntu 8 mảnh và gom đều success, không khai 490 đã đo tại sandbox |
| Windows runtime tại chỗ | **KHÔNG ĐO ĐƯỢC** | Không có Windows/cmd/wine/pwsh. Bằng chứng Windows chỉ đọc CI có đúng SHA/runner/checkout và output |
| CI workflow-definition OID, run attempt/event độc lập, M-2/authority live | **KHÔNG ĐO ĐƯỢC** | Gói có jobs và hai log, không gọi mạng; không dùng approval mã để xác nhận các mục ngoài phép kiểm được giao |

M-3 (Ubuntu CI + launcher Windows) và M-5 (gate-cong-cu Windows N8 + N7) có bằng chứng dương theo yêu cầu review lượt này; M-4 đạt 6/450. Không biến job skipped, ca bỏ qua hoặc giới hạn chưa chạy thành màu xanh. Không merge, land, deploy, push hay viết patch sản phẩm.
