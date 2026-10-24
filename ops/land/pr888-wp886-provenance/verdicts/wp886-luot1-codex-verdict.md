verdict: approve
reviewed_head: a9be5828fb7b937ec8c9f7f1dc6b5a48babbafa5
reviewed_sha: a9be5828fb7b937ec8c9f7f1dc6b5a48babbafa5
reviewed_tree: 7e83a2cf394a421bb76dd4208a40dc857fac3c52
review_class: sensitive
provider: openai_codex
model: gpt-6.1-sol
model_family: openai
reasoning_effort: xhigh
execution_surface: codex_cli
transport: machine
review_round: 1/5

## Kết luận

**Approve trong phạm vi lượt 1 đã được chỉ định**: N1–N5 độc lập với lỗi fixture Windows đã biết; không phát hiện P0/P1/P2/P3 mới trong 5 tệp bản vá. N6 được đối chiếu tĩnh; N7 có bằng chứng dương trên HEAD. Không sửa sản phẩm hoặc fixture.

Đây là kết luận review mã theo phạm vi trên, **không chứng nhận toàn bộ cổng packet/điều kiện merge đã xanh**. Full launcher có 13 ca đỏ sẵn trên base và 10 ca bỏ qua; Windows thực/CI/authority live không đo được. Lệnh cong_cu_test mặc định đã chạy nhưng timeout ở vòng bán kính 470 mutant; mode gate được hỗ trợ, test nguyên byte, đạt đủ 61/61 ca nền. Các giới hạn được ghi riêng dưới đây, không đổi thành pass.

## Neo và môi trường

| Mục | Giá trị tự đo |
|---|---|
| Head | `a9be5828fb7b937ec8c9f7f1dc6b5a48babbafa5` |
| Head tree | `7e83a2cf394a421bb76dd4208a40dc857fac3c52` |
| Base | `1ccc31498b7d37c12305e8f1b5bf2d1fc217b92e` |
| Base tree | `7bdb1060e9940596a480ceadd14cfbebf1e97423` |
| Spec SHA-256 | `28d1bb708621c6d410aa2f22ba11f295a5a9407d74d7aa736ddd30421e4f96a6` — khớp đầu/cuối |
| Hai cây nguồn | Sạch đầu/cuối; status rc=0, output rỗng, kể cả untracked/ignored |
| Đối chiếu nội dung | Head 5230 tệp, base 5229 tệp; băm mọi tệp, gồm .git, và đích symlink đầu/cuối giống hệt |
| Runtime | Linux x86_64; Python 3.13.16; Ruff 0.16.9; không có Windows runner/wine/pwsh |
| Identity CLI | `runs/883f685c/stderr.log`: OpenAI Codex v0.163.0, gpt-6.1-sol, reasoning effort xhigh, provider openai |
| Session | `01a1695f-7a98-7452-9f7b-3e06be2c0dfb`; header chỉ chứng minh model/effort CLI công bố |

Các lệnh neo: `git -C cay-kho rev-parse HEAD 'HEAD^{tree}'`, tương tự với `nen`; `sha256sum evidence/spec.md`; cuối lượt dùng `git status --porcelain=v1 --untracked-files=all --ignored=matching`. Log cuối ở `integrity/`; snapshot đầy đủ `source-content-start.json` và `source-content-end.json`. Snapshot chứng minh không có delta nội dung quan sát ở hai mốc; không chứng minh lịch sử mọi lần ghi. Không thay quyền/trust hoặc ghi vào cây nguồn/mirror.

Các lệnh Python review dùng `-B` và môi trường `PYTHONDONTWRITEBYTECODE=1`; TMPDIR riêng dưới `out/tmp/`, Git read-only dùng `GIT_OPTIONAL_LOCKS=0`. Các bản sao thường dựng **cùng một lệnh** (`python3 -B out/run_review.py`): copytree head/base cùng cơ chế, rồi chỉ chép launcher_test head vào bản base. Không dùng git worktree. `out/run_suites.py` dựng bản mutant từ chính cây head sạch trong out/.

Bản sao lease/EXECUTOR_GATES là dữ liệu offline, không phải authority live/bằng chứng chạy. Không gọi mạng/GitHub hoặc cài dependency. Một số fixture có lệnh commit tự chạm đường ký nội bộ bị sandbox chặn; không có kết nối thành công, đã tắt ký riêng trong môi trường fixture sau khi chẩn đoán.

## Bảng finding

| ID | Mức | Vị trí tệp:dòng | Bằng chứng | Hướng sửa bằng lời |
|---|---|---|---|---|
| — | — | — | Không có finding P0/P1/P2/P3 mới trong phạm vi lượt này. | Không đề xuất patch sản phẩm. |

Không cấp ID F886-NN cho lỗi fixture Windows đã biết, lỗi môi trường hoặc đột biến do reviewer tự tạo. Mutant bỏ mục PATH rỗng cho thấy khoảng trống kiểm thử; H01 chứng minh bản sản phẩm hiện tại xử lý đúng. Gợi ý cải thiện test: bổ sung ca cwd có python khác phiên bản với thư mục PATH tiếp theo, PATH bắt đầu bằng mục rỗng, và buộc mutant bỏ mục rỗng chết bằng chốt đúng ca.

## Bảng N1–N7

| N | Kết quả | Bằng chứng và giới hạn |
|---|---|---|
| N1 | ĐẠT phần đã đo | r886_n1 qua; sys.executable mutant chết đúng ca; H01/H02/H03/H07 đối chiếu PATH/cwd/quyền thực thi/py -3/installer |
| N2 | ĐẠT | Head không DAT với python hỏng trước python3 tốt; base đỏ bằng **TinHieuChotCa đúng ca N2** |
| N3 | ĐẠT Linux | r886_n3 qua; H09 đo thêm cả jsonschema trên python3 -S khác checker: có/vắng package đều đúng |
| N4 | ĐẠT | Không có ba tên → KHONG_DO_DUOC và nêu đủ python/python3/py; hai mutant N4 chết đúng ca |
| N5 | ĐẠT ca liên quan chạy được và 61/61 ops cases; full launcher chưa N/N | r858_python nâng về N1/N3 đầy đủ qua; các r858 installer/shape/selftest và r802 pointer qua. r858_goc_tam lỗi /var/tmp ở cả hai vế; full launcher không có ca đỏ mới |
| N6 | ĐẠT phép tĩnh; Windows thực KHÔNG ĐO ĐƯỢC | r886_n6 qua, mutant native/path-first/py thiếu -3 chết; H04 8/8 khớp bộ giải native launcher. Không suy runtime .cmd/.bat hay sàn Windows từ Linux |
| N7 | ĐẠT trên HEAD trong rig fixture unsigned | release verify rc=0, ok=true, expected=checked=192; tl selftest rc=0 **1731/1731**, transport 12/12; unsigned base cũng 1731/1731 |

## Ca có sẵn và phản chứng hai vế

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 -B out/run_review.py` (rc=0); từng ca dùng `python3 -B .claude/dev/launcher_test.py --lap-ca <TEN> --lan 1`. Mỗi ca head/base có command, cwd, rc, stdout/stderr tại `targeted/<head|base>/<TEN>.json`.

| Ca | Head rc | Base+test-head rc |
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
| `r886_ten_python_khop_cai_cong_cu_sh` | 0 | 1 |
| `r858_bat_buoc_bash_khong_dua_rg_hong_len_dau` | 0 | 0 |
| `r858_hinh_dang_cong_thuc_cai` | 0 | 0 |
| `r858_selftest_editskill_thu_muc_rieng` | 0 | 0 |

Head **14/15 qua**, base **7/15 qua**. Ca chọn gốc tạm đỏ ở cả hai vì `[Errno 30] Read-only file system: /var/tmp/lt_...`; TMPDIR ở dưới tổ tiên `/tmp/.git`, nên ca tự chuyển sang /var/tmp không ghi được. Không đổi test, không nới quyền để làm xanh.

N2 base: `TinHieuChotCa`, frames `classify → r886_n2_python_hong_dau_path_khong_DAT → bang`, thông điệp `python hong dau PATH ma van DAT: rc=0`, thấy Python 3.13.16/DAT. **Đỏ đúng lý do**, không phải lỗi vô can (`targeted/n2-base-classification.json`). N6/Q1 trên base thiếu `_python_theo_path`/`TEN_PYTHON` (AttributeError), không được tính như mutant bị giết.

Full suite: `PYTHONDONTWRITEBYTECODE=1 python3 -B out/run_suites.py`; mỗi lượt gọi `python3 -B .claude/dev/launcher_test.py --nhat-ky <out/suites/*.journal>`. CÓ và KHÔNG CODEX_AUTH_JSON giả; module test tự bỏ biến trước ca. JSON từng lượt giữ output đầy đủ.

| Cây | Credential | Qua/đã chạy | Tổng | Bỏ qua | Hỏng | rc |
|---|---|---:|---:|---:|---:|---:|
| base | absent | 228/248 | 258 | 10 | 20 | 1 |
| base | fake | 228/248 | 258 | 10 | 20 | 1 |
| head | absent | 235/248 | 258 | 10 | 13 | 1 |
| head | fake | 235/248 | 258 | 10 | 13 | 1 |
| mutant | absent | 235/248 | 258 | 10 | 13 | 1 |

**Delta ca mới đỏ = 0** cho cả hai chế độ credential. Bảy ca được sửa: `r858_cai_python_khong_in_thu_muc_ban_hong`, `r886_n1_ten_tran_theo_path_moi_nen`, `r886_n2_python_hong_dau_path_khong_DAT`, `r886_n3_chi_python3_DAT_va_do_dung_interpreter`, `r886_n4_khong_ten_nao_noi_ro_thieu_gi`, `r886_n6_giai_ten_tinh_windows_va_posix`, `r886_ten_python_khop_cai_cong_cu_sh`.

Cùng 10 skip: 8 ca r345/r347/r348 không dựng được venv/pip; t62 và r484_g4_windows_sid_alias_identity cần Windows. Cùng 13 ca đỏ còn lại ở head/mutant đã đỏ trên base: 2 lỗi /var/tmp read-only; 6 lỗi trực tiếp `Codex home is inside a repository`; 5 ca r484 doctor/schema/credential/materializer khác chưa được quy nguyên nhân sâu. Đây là kết quả baseline chung, không tuyên bố toàn bộ nguyên nhân đã được chứng minh. Tập head_fail trừ base_fail rỗng; mutant_fail bằng head_fail. Không gọi full suite là N/N hoặc 13 ca này là regression của PR.

## Bảng đột biến

Lệnh độc lập: `PYTHONDONTWRITEBYTECODE=1 python3 -B out/run_mutations.py` (rc=0). Mọi sửa chỉ nằm ở bản sao `out/mutations/*.py`; con trỏ test được hoàn nguyên. Chỉ đếm `TinHieuChotCa` khi traceback có **đúng tên ca đích**, baseline ca đó xanh; mọi ngoại lệ khác là FALSE_CREDIT, không cấp giết. Neo/thay nguyên văn và từng exception/message/frames ở JSON từng mutant.

| Đột biến | Giết đúng ca | Ca qua | Lỗi vô can/tín dụng giả không cấp giết |
|---|---:|---:|---:|
| `wp886_cc_ve_sys_executable` | 3/3 | 0 | 0 |
| `wp886_cc_python3_truoc_python` | 2/2 | 0 | 0 |
| `wp886_cc_bo_python3` | 2/2 | 0 | 0 |
| `wp886_cc_py_mat_tru_3` | 2/2 | 0 | 0 |
| `wp886_cc_khong_ten_roi_ve_sys_executable` | 1/1 | 0 | 0 |
| `wp886_cc_bo_ly_do_thieu_ten` | 1/1 | 0 | 0 |
| `wp886_cc_windows_nhan_ten_tran` | 1/1 | 0 | 0 |
| `wp886_cc_path_truoc_ten` | 1/1 | 0 | 0 |
| `review_cc_bo_muc_PATH_rong` | 0/15 | 14 | 1 |

Tám mutant có sẵn: **8/8 bị giết, 13/13 lượt ca đích chết đúng chốt, 0 tín dụng giả**. Mutant mới `review_cc_bo_muc_PATH_rong` đổi vòng duyệt sang `filter(None,...)`: **sống qua cả suite launcher đầy đủ** (cùng 13 ca đỏ baseline, không có ca mới đỏ), đồng thời 14/15 ca liên quan qua; ca còn lại chỉ OSError môi trường, không phải giết. H01 cho thấy mutant đo sai 3.11.12 trong khi shell/head đo 3.10.11 với PATH=:rel: mutant không tương đương, bộ ca thiếu chốt cho mục rỗng.

Full `python3 -B .claude/dev/launcher_test.py --dot-bien` qua `out/run_all_mutations.py`: **rc=0**, `DOT BIEN: 318/318 dat (4 khong do duoc tren nen nay)`, 175.970 giây; `all-mutations/result.json`. Bốn không đo: g4_windows_sid_alias_not_normalized, g4_windows_LA_not_current_owner, g2_windows_directory_pin_access, 124_khi_chau_con_song. Sàn Linux 318/322>70%; không suy sàn Windows. 318/318 là kết quả runner legacy; reviewer chỉ chứng minh độc lập đúng lý do cho tám wp886, không tự xác nhận mọi legacy mutant từ headline.

## Các hướng săn độc lập

Lệnh chung: `PYTHONDONTWRITEBYTECODE=1 python3 -B out/run_hunts.py`, rc=0; từng đoạn H01–H09 được gắn nhãn trong script. Bên dưới trích output thật; toàn bộ JSON tại `hunts/Hxx.json`. Không dựng payload thoát cây/đường dẫn độc hại.

| Hướng | Giả thuyết và phép đo | Output thật | Kết luận |
|---|---|---|---|
| H01 | PATH rỗng/tương đối; đối chiếu Bash với `_python_theo_path/_chay` | `PATH=:rel`: head/Bash `Python 3.10.11`; mutant `3.11.12`; `PATH=rel:`/`rel`: head/Bash cùng `3.11.12`, rc=0 | KHÔNG PHẢI LỖI sản phẩm; mutant có đổi hành vi, không tương đương |
| H02 | Tệp không có X_OK và thư mục tên `python` đứng trước bản tốt | head chọn `.../nonexec_dir/c/python`, output `Python 3.12.9`, rc=0; Bash cùng đường và phiên bản | KHÔNG PHẢI LỖI |
| H03 | Chỉ có `py`; giữ `-3` và argv; py không hiểu `-3` | prefix `[...,py,-3]`, rc=0 `args-preserved`; py hỏng rc=19 → DO `mong [0]` | KHÔNG PHẢI LỖI |
| H04 | PATHEXT rỗng/lạ, thứ tự đuôi: so resolver với launcher native | 8/8 cấu hình khớp `_ten_tran_giai_ra(...,kieu_bash=False)` trên hệ tệp Linux | KHÔNG PHẢI LỖI trong phép tĩnh; Windows subprocess KHÔNG ĐO ĐƯỢC |
| H05 | T7: một probe tên trần, một probe interpreter tuyệt đối | `ban_thay={bare:0.0.1,absolute:3.13.16}`, DO, `cac duong goi khac ban` | KHÔNG PHẢI LỖI |
| H06 | N4 không tên nào / py không executable / py hỏng | KHONG_DO_DUOC có đủ `python, python3, py`; py không executable → None; py hỏng → DO rc=23 | KHÔNG PHẢI LỖI |
| H07 | `cai_cong_cu.sh --bat-buoc` end-to-end; python đầu PATH chỉ hỏng --version | rc=0, GITHUB_PATH bằng chính ứng viên tốt `.../mandatory/goc/usr/bin`; cổng công cụ và toàn bộ đều DAT | KHÔNG PHẢI LỖI; fixture manifest chỉ python, sudo/apt-get là stub offline |
| H08 | Canary dùng probe lenh[0]=python, PATH chỉ python3 | owner DAT `3.13.16`; canary DAT `canary bat dung SC1003 (rc=0)` | KHÔNG PHẢI LỖI |
| H09 | Cả PyYAML và jsonschema trên python3 khác checker (`-S`), metadata có/vắng | PyYAML có: rc=0/DAT/9.9.9; jsonschema có: rc=0/DAT/4.26.0; cả hai vắng: rc=2/DO, ban_thay=null | KHÔNG PHẢI LỖI |

## Cổng bổ sung và nhiễu môi trường

| Lệnh trên out/head | rc/kết quả thật | Diễn giải |
|---|---|---|
| `python3 -B ops/cong_cu_test.py` mặc định | TIMEOUT ở 900 giây; nền 60/60, 1 skip; cổng cây thật và tự kiểm phân hạng/giàn giáo/song song đạt | Vòng 470 mutant bán kính toàn bộ chưa đo xong; **KHÔNG ĐO ĐƯỢC toàn lệnh**, không khai pass |
| Cùng lệnh, `CONG_CU_TEST_BAN_KINH=manh` | rc=0; nền 60/60, tổng 61/skip 1 trong môi trường ban đầu | Mode gate được hỗ trợ; không chứng minh đủ 61 ca |
| Cùng mode gate, fixture unsigned | **rc=0; 61/61**, tổng 61/skip 0/tiền kiểm skip 0; cổng cây thật ĐẠT; lỗi đột biến 0 | 470 bán kính giao mảnh, không khẳng định đã đo đủ 470 |
| `python3 -B ops/cong_cu.py kiem-tra --json` | rc=2/tổng DO; python 3.13.16, PyYAML 6.0.3, jsonschema 4.26.0 đều DAT | shellcheck KHONG_DO_DUOC/FileNotFoundError; canary blocking DO/SUY_GIAM, rc actionlint 0 không thay pass canary |
| `python3 -B scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | **rc=0; ok=true; expected_file_count=checked_file_count=192** | failed/extra/missing/errors rỗng; package hash expected/current/full-tree cùng 355168a4bf63f8615f577229d280fc2ede0539799c40e8624241bc1940a32e9a |
| `python3 -B scripts/tl.py --selftest`, môi trường ban đầu | rc=1; 1729/1731 trên cả head và base | Cùng hai fail r226/r268; không quy thành regression |
| Cùng selftest, fixture unsigned | **rc=0; 1731/1731** trên cả head và base; transport 12/12 | Bằng chứng dương, không chỉ rc |
| `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .` | **rc=0**, sạch, quét 10 tệp, 0 chỗ chép doctrine | `doctrine-scan.raw`; lệnh thăm dò nhầm `tl.py doctrine-scan` trước đó rc=2/argparse, không phải lỗi PR |
| `python3 -B scripts/tl.py doc-claims-check --strict` | **rc=0; ok=true; 113 tệp; flags=0; 394 advisory** | Không đếm advisory thành lỗi chặn; `gates-fast/doc_claims.json` |

`ops/cong_cu_test.py` giữ nguyên SHA-256 **23dbdeada416cfa960ff4d2d4a85d7cb4bf29d84240a3fe6274edde7b1b5cf76** ở head/base/bản chạy. Không sửa fixture Windows.

Nhiễu ký commit: `/root/.gitconfig` có `commit.gpgsign=true`, `gpg.format=ssh`; commit fixture tối thiểu rc=128, `fatal: failed to write commit object`, dịch vụ ký bị sandbox từ chối socket (`git-commit-control.json`). Tắt ký **chỉ trong môi trường con** bằng `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false` (không sửa global config/source/trust/quyền); cả hai selftest chuyển 1729/1731→1731/1731, ops case INDEX không còn skip. Các lượt điều chỉnh đặt thêm PIP_NO_INDEX=1 để giữ offline. `unsigned-gates/*-selftest.json`, `cong-cu-unsigned-gate.raw` giữ bằng chứng; không dùng lời khai executor.

## Write set, M-4 và Ruff

Tự đo `git -C cay-kho diff BASE HEAD --numstat`: **5 tệp, 246 dòng thêm, 31 dòng xoá**, đúng write set và M-4 ≤5/≤450:

| Tệp | Thêm | Xoá |
|---|---:|---:|
| .claude/dev/launcher_test.py |183|16|
| RELEASE_MANIFEST.json |11|6|
| changelog.d/wp-886.md |7|0|
| ops/cong_cu.py |39|5|
| scripts/tl_selftest.py |6|4|

`ruff 0.16.9 check --select F --no-cache --output-format json ops/cong_cu.py .claude/dev/launcher_test.py scripts/tl_selftest.py scripts/tl.py` trên cả hai cây: rc=1 vì nợ nền; theo thứ tự tệp **1,5,4392,12** ở cả hai, tổng 4410=4410. So `(path,code,message,count)` không có diagnostic mới hoặc mất: **delta=0**, không gọi lint sạch tuyệt đối. `out/run_static.py`, `static/ruff-summary.json` và `static/numstat.json` chứa command/output thật; không tạo cache trong cây nguồn.

## Đánh giá Windows và phần không đo được

Fixture `ops/cong_cu_test.py:3126` tạo symlink **python3 không đuôi**. Native Windows của bản vá chỉ thử đuôi PATHEXT khi tên trần chưa mang đuôi, khớp `_ten_tran_giai_ra(...,kieu_bash=False)` tại launcher.py:2306. Vì vậy xung đột fixture đã biết có cơ sở khi đọc code; theo chỉ thị lượt 1, không tạo finding mới, không sửa tệp ngoài write set.

r886_n6 và H04 chứng minh luật tĩnh khớp; không chứng minh CreateProcess chạy .cmd/.bat trên Windows thật. **KHÔNG ĐO ĐƯỢC**: Windows runtime, launcher-windows workflow_dispatch, gate-cong-cu Windows, CI/check runs exact head, lease/authority live; sandbox không có mạng/GitHub. Còn 4 mutant legacy không đo được trên Linux, 10 launcher case bỏ qua, 13 ca đỏ baseline, và 470 bán kính ops chưa đo đầy đủ. Không điều kiện nào trong số này được ghi xanh hoặc suy từ EXECUTOR_GATES. Approval ở đây không thay M-2/M-3, không cấp quyền merge/land/deploy.

## Hiện vật và giới hạn bằng chứng

Tất cả script/log/bản sao nằm dưới out/. Không viết patch hoặc commit/push vào kho sản phẩm; các commit chỉ phục vụ fixture trong out/. Không gửi tin qua dịch vụ ngoài hoặc thay đổi cây nguồn/mirror. Auditor read-only theo CLAUDE.md bước 5 kiểm lại marker/đếm từ log, không sửa code; các kết luận chính được primary đối chiếu lại. Lệnh/scripts tái hiện: run_review.py, run_mutations.py, run_suites.py, run_hunts.py, run_static.py, run_all_mutations.py, run_unsigned_gates.py; các logs giữ cả rc khác 0, skip và timeout.

Neo cuối và băm nội dung hai cây khớp đầu; tệp verdict được chốt sau khi các tiến trình có thể ghi verdict đã hoàn tất. `VERDICT.sha256` là băm hiện vật cuối để readback.
