verdict: pending
reviewed_head: 1c138c714f9c192ea730b65c5d18ff5eda1ca660
reviewed_sha: 1c138c714f9c192ea730b65c5d18ff5eda1ca660
reviewed_tree: 19bf06bad9748818a9aa6ed7d7ed4a88199d7cdf
review_class: sensitive
provider: openai_codex
model: gpt-6.1-sol
model_family: openai
reasoning_effort: xhigh
execution_surface: codex_cli
transport: machine
review_round: 2/5

## Kết luận

**Pending về nghiệm thu đầy đủ**: chưa phát hiện P0/P1/P2/P3 mới trong 6 tệp bản vá, nhưng N8 đòi bằng chứng `windows-latest` thật trên exact head; gói offline này không có log/check-run độc lập để xác minh. Chạy `.cmd`, `%*`, quoting và cổng Windows thật là **KHÔNG ĐO ĐƯỢC**. Những lượt launcher toàn bộ hết hạn cũng không được tính N/N. Không suy pass từ lời khai executor hay phép mô phỏng Linux.

Phần đã chứng minh: phạm vi r2 hợp lệ, H01 lượt 1 đã đóng, mọi `r886_*` chạy qua trên Linux; 9 mutant có sẵn bị giết đúng chốt; 3 mutant reviewer bổ sung được giết bằng các ca độc lập. Đây không phải yêu cầu sửa sản phẩm khi chưa có lỗi đo được. Cần readback CI Windows đúng SHA và các cổng còn thiếu trước khi cấp approval nghiệm thu đầy đủ. Không merge/land/deploy hoặc gọi mạng/GitHub.

## Neo và môi trường

| Mục | Bằng chứng tự đo |
|---|---|
| Head / tree | `1c138c714f9c192ea730b65c5d18ff5eda1ca660` / `19bf06bad9748818a9aa6ed7d7ed4a88199d7cdf` |
| Base / tree | `33e6d4c32d26663a87bbdd6f1350890fa6042cc5` / `86c2596c9d80577601dd37891958e58be7ace11f` |
| Ancestry | `git merge-base --is-ancestor <base> <head>` rc=0; merge master `a155182` là cha head, manifest nằm trong commit cuối `1c138c7` |
| Spec r1 SHA-256 đầu/cuối | `28d1bb708621c6d410aa2f22ba11f295a5a9407d74d7aa736ddd30421e4f96a6` — khớp |
| Spec r2 SHA-256 đầu/cuối | `c019dbbacf838cddac40da8b360a0564c9383a10a07821735a7f3366ef72d68b` — khớp |
| Cây nguồn head/base sạch cuối | `True` / `True`; đầu lượt status rc=0, output rỗng, gồm tracked/untracked/ignored |
| Nội dung head/base/mirror đầu=cuối | `True` / `True` / `True`; gồm .git, quyền tệp và đích symlink |
| Số tệp snapshot head/base/mirror | 5307 / 5306 / 538 |
| Runtime | Linux x86_64; Python 3.13.16; Ruff 0.16.9; không có cmd.exe/wine/pwsh |
| Identity CLI | `runs/cd636453/stderr.log`: OpenAI Codex v0.163.0, `gpt-6.1-sol`, effort `xhigh`, session `01a16b7c-46dc-7b23-adbf-70e68982c778` |

Header CLI chứng minh model/effort CLI công bố, không chứng minh mọi request phía dịch vụ. Lease r2/offline còn hạn theo timestamp trong bản sao; không kiểm authority live. `evidence/EXECUTOR_GATES.md` chỉ dùng để đặt giả thuyết. Không suy CI xanh từ đó, cũng không báo lỗi cài shellcheck trên Windows là regression của PR.

Lệnh dựng hai vế duy nhất: `PYTHONDONTWRITEBYTECODE=1 python3 -B out/setup_and_target.py`. Hai bản sao thường `out/head`, `out/base` được dựng cùng vòng lặp trước khi đo; chỉ chép hai tệp test head sang bản base, giữ mã sản phẩm base. Không dùng worktree hay hardlink. Lệnh Python dùng `-B` và `PYTHONDONTWRITEBYTECODE=1`; TMPDIR dưới `out/tmp/`; Git nguồn dùng `GIT_OPTIONAL_LOCKS=0`; lint dùng `--no-cache`. PIP_NO_INDEX=1 ngăn cài qua mạng. Snapshot hai mốc chứng minh không có delta quan sát, không chứng minh lịch sử mọi lần ghi. Sandbox thực tế là workspace-write; kỷ luật review giữ cây nguồn read-only.

## Phạm vi r2

`git diff <base> <head>` tự đo trùng byte với `evidence/diff.patch`. Numstat: **6 tệp / 266 dòng thêm / 33 dòng xóa**, đạt trần 6/450.

| Tệp | Thêm / xóa | Đối chiếu |
|---|---:|---|
| `.claude/dev/launcher_test.py` | 194 / 16 | r886, N5 đầy đủ, định tuyến mutant cong_cu, trả con trỏ |
| `RELEASE_MANIFEST.json` | 11 / 6 | Sinh lại manifest, verify bên dưới |
| `changelog.d/wp-886.md` | 9 / 0 | Fragment packet |
| `ops/cong_cu.py` | 39 / 5 | Giải python theo PATH, chi tiết lỗi N4 |
| `ops/cong_cu_test.py` | 7 / 2 | Chỉ fixture/docstring `python_alias_behavior_test`; kỳ vọng giữ nguyên |
| `scripts/tl_selftest.py` | 6 / 4 | Chỉ ratchet 191→192 và chú thích slot |

AST sau khi bỏ riêng `python_alias_behavior_test` khỏi cả hai bên **giống hệt** (`scope/ops-ast-outside-fixture.json`). Vì vậy các thay đổi #895 trên master không bị quy nhầm vào PR. POSIX vẫn symlink; Windows tạo `.cmd`. Lựa chọn `.cmd` thay `.exe` được chỉ thị review hiện tại xác nhận thuộc r2.

## Đối chiếu lượt 1

Nguồn `evidence/verdict-luot1.md`, head `a9be5828fb7b937ec8c9f7f1dc6b5a48babbafa5`: không có finding F886-NN mở, chỉ H01 là gợi ý tăng răng cho PATH rỗng; approval cũ giới hạn N1–N5, không kế thừa thành approval N8.

**H01 — ĐÃ VÁ THẬT trong phạm vi chốt đã nêu**. Baseline `r886_n6_giai_ten_tinh_windows_va_posix` qua; `wp886_cc_bo_muc_PATH_rong` chết bằng chính `TinHieuChotCa`, traceback `classify → r886_n6_giai_ten_tinh_windows_va_posix → bang`, message `muc PATH rong khong la cwd`. Mutant chọn `c/py.EXE -3` và `c/python3` thay python trong cwd. Chi tiết `mutations/wp886_cc_bo_muc_PATH_rong.json`. Không chỉ grep sự có mặt của assertion.

## Bảng finding

| ID | Mức | Tệp:dòng | Bằng chứng | Hướng sửa bằng lời |
|---|---|---|---|---|
| — | — | — | Không có P0/P1/P2/P3 mới được chứng minh trong phạm vi 6 tệp. | Không viết patch sản phẩm. |

Không gán F886-NN cho hạn chế nền, CI chưa đọc được, mutant do reviewer tự tạo, hoặc lời đếm sai ngoài diff. Prompt và lời khai executor ghi 10 `wp886_cc_*`; tự đếm AST danh sách chỉ có **9**. Báo đúng 9/9, không tạo một mutant “có sẵn” thứ mười. N8 thiếu bằng chứng là lý do pending, không phải kết luận mã Windows hỏng.

## Bảng N1–N8

| N | Kết quả | Bằng chứng và giới hạn |
|---|---|---|
| N1 | ĐẠT phần Linux đã đo | r886_n1; H05 argv/py -3, H06 bỏ nonexec, H07 giữ python đầu PATH; mutant sys.executable bị giết |
| N2 | ĐẠT | Head không DAT khi python hỏng đứng trước python3 tốt; base chết đúng TinHieuChotCa trong ca N2, không lỗi vô can |
| N3 | ĐẠT Linux | r886_n3 đo python3 -S với PyYAML giả/vắng; H04 đo thêm jsonschema và T7 khác interpreter |
| N4 | ĐẠT | r886_n4 giữ KHONG_DO_DUOC, rc=3 và đủ tên python/python3/py; hai mutant N4 chết đúng chốt |
| N5 | ĐẠT tập r858 chạy được và ca nền ops 61/61; gate chưa đo trọn | r858 python đầy đủ và r802 pointer qua; r858 chọn gốc tạm đỏ ở cả hai bên do /var/tmp read-only; ops không bỏ qua ca/tiền kiểm, nhưng timeout phần tự kiểm giàn giáo |
| N6 | ĐẠT phép tĩnh; Windows runtime KHÔNG ĐO ĐƯỢC | r886_n6 và 5/5 cấu hình PATHEXT khớp launcher native; không suy sàn Windows từ Linux |
| N7 | Release ĐẠT; selftest kết quả bên dưới | release rc=0, ok=True, expected=checked=192; selftest `['== tl selftest 1731/1731 ==']`, rc=0 |
| N8 | Fixture tĩnh và Linux ĐẠT; Windows thật KHÔNG ĐO ĐƯỢC | `.cmd` được `_python_theo_path(...,la_windows=True)` giải; tên không đuôi không được giải; mutant fixture chết đúng ca reviewer. Chưa đọc gate-cong-cu windows-latest exact head |

## Ca có sẵn và đối chứng

Mỗi ca dùng `python3 -B .claude/dev/launcher_test.py --lap-ca <TEN> --lan 1`; stdout/stderr/rc/cwd/command riêng tại `targeted/<head|base>/<TEN>.json`.

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

Head **14/15 qua**, base **7/15 qua**; tập ca head đỏ nhưng base xanh rỗng. Lỗi chung duy nhất trên head là `[Errno 30] Read-only file system: /var/tmp/lt_...`: `/tmp/.git` là mount rỗng read-only trong namespace, ca chuyển sang `/var/tmp`. Không đổi mount/quyền/test để ép xanh. N6/Q1 trên base thiếu helper/hằng mới (AttributeError), không cấp tín dụng giết cho lỗi đó. N2 base được phân loại độc lập tại `targeted/base-n2-classification.json`.

## Cổng và giới hạn

- Release: `python3 -B scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json`; rc=0, `ok=True`, `expected_file_count=192`, `checked_file_count=192`, không extra/missing/hash lệch (`gates/release.json`).
- Selftest: `python3 -B scripts/tl.py --selftest`; lượt rig đúng rc=0, timeout=False, 262.436s; `['== tl selftest 1731/1731 ==']` (`gates/selftest-corrected.json`). Lượt đầu 1730/1731 do tôi ép core.abbrev qua env, đã giữ log riêng. Cùng ca r226 trên base/head: env ép=**false/false**, bỏ ép=**true/true** (`gates/abbrev-*.json`). Repo copies vốn ghim core.abbrev=7; không sửa expectation hoặc sản phẩm.
- Ops: `CONG_CU_TEST_BAN_KINH=manh python3 -B ops/cong_cu_test.py` trên head; rc=-9, timeout=True, `['cong_cu_test: 61/61 đạt; tổng=61, bỏ qua=0, tiền kiểm bỏ qua=0']`; `[]` (`gates/ops-gate.json`). Có bằng chứng dương **61/61, bỏ qua=0, tiền kiểm bỏ qua=0** và cổng cây thật ĐẠT. Tiến trình hết 300s giữa `TỰ KIỂM GIÀN GIÁO`, sau control và crash vô can; không xác nhận tự kiểm còn lại hay toàn bộ gate. Bán kính 490 mutant đầy đủ **KHÔNG ĐO ĐƯỢC** trong lượt này; không báo đã pass.
- Probe container thật: `python3 -B ops/cong_cu.py kiem-tra --chi <python|PyYAML|jsonschema> --json`; rc lần lượt 0/0/0, chi tiết tại `gates/real-*.json`.
- Doctrine: `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .`, rc=0. Doc claims: `python3 -B scripts/tl.py doc-claims-check --strict`, rc=0. Không coi hai cổng hình thức là chứng minh ngữ nghĩa.
- Ruff thật: `ruff check --no-cache --select F ops/cong_cu.py ops/cong_cu_test.py .claude/dev/launcher_test.py scripts/tl_selftest.py` trên cả hai bản sao. Base/head 4399/4399 diagnostic; delta mới=0, rc base/head=1/1. So code/message/multiplicity, không so số dòng đã dịch. Không gọi baseline lint đỏ là “Ruff xanh”.

Full launcher mở rộng: `python3 -B out/run_suites.py`, từng lệnh `python3 -B .claude/dev/launcher_test.py --nhat-ky <out/suites/*.journal>`, có/không CODEX_AUTH_JSON giả. Bảng đếm từ journal; “qua/bỏ qua/hỏng” chỉ tính ca đã có dòng ra. **Không có marker hoàn tất thì không gọi N/N và không suy delta toàn suite.** Lượt base-absent đầu bị lỗi thư mục cha journal của rig, đã lưu riêng `invalid-missing-journal-parent.json`; lượt hợp lệ thay thế được ghi trong bảng.

| Cây | Auth | rc | Timeout | Ca có dòng ra | Qua/bỏ qua/hỏng | Marker hoàn tất |
|---|---|---:|---|---:|---|---|
| base | absent | -9 | True | 240 | 210/10/20 | không |
| base | fake | -9 | True | 256 | 226/10/20 | không |
| head | absent | -9 | True | 233 | 210/10/13 | không |
| head | fake | -9 | True | 255 | 232/10/13 | không |

Phần giao các ca có dòng ra ở cả hai cây được phân tích riêng tại `suites/completed-intersection.json`: absent 233 ca và fake 255 ca, đều không có ca mới đỏ. Đây chỉ là tập đã đo xong ở cả hai phía; không thay marker hoàn tất hoặc chứng minh các ca bị cắt. Các lượt launcher mở rộng được khởi chạy trước khi sửa rig, nên vẫn mang env `GIT_CONFIG_COUNT=2`, khóa 0 `commit.gpgsign=false`, khóa 1 `core.abbrev=7` ở cả hai phía. Tự kiểm N7 chạy lại riêng với chỉ khóa 0; không ghi đè lịch sử của các lượt cũ thành rig mới.

Full launcher mutation: `python3 -B .claude/dev/launcher_test.py --dot-bien`, rc=0, timeout=False, `['DOT BIEN: 319/319 dat  (4 khong do duoc tren nen nay)']` (`suites/all-mutations.json`). Sàn Linux đo được 319/323 = 98,76%, vượt 70%; 4 mục còn lại vẫn KHÔNG ĐO ĐƯỢC. Headline runner legacy không tự chứng minh từng mutant legacy chết đúng lý do; 9 wp886 được reviewer phân loại riêng dưới đây. Không suy kết quả này thành kết quả Windows.

## Bảng đột biến

Lệnh `PYTHONDONTWRITEBYTECODE=1 python3 -B out/run_mutations.py`; chỉ sửa `out/mutations/*.py`. Mỗi neo xuất hiện đúng 1 lần, compile trước chạy, baseline đúng ca phải xanh, chỉ `type(ex) is TinHieuChotCa` cùng frame tên ca đích và không có ca đăng ký khác trong stack mới cấp giết; con trỏ được trả trong finally. Bộ phân loại tự kiểm **6/6**: chốt thật, AttributeError, đổi AttributeError thành AssertionError, chốt ca khác, pass, skip (`mutations/classifier-selfchecks.json`). Đã chạy lại toàn bộ 9 mutant có sẵn sau khi siết bộ phân loại; kết quả không đổi. JSON giữ neo/thay, exception, message, frames (`mutations/all.json`).

| Mutant | Giết đúng ca có sẵn | Ca vẫn qua | Lỗi vô can | Ghi chú |
|---|---:|---:|---:|---|
| `wp886_cc_ve_sys_executable` | 3/3 | 0 | 0 | Ca đích có sẵn. |
| `wp886_cc_python3_truoc_python` | 2/2 | 0 | 0 | Ca đích có sẵn. |
| `wp886_cc_bo_python3` | 2/2 | 0 | 0 | Ca đích có sẵn. |
| `wp886_cc_py_mat_tru_3` | 2/2 | 0 | 0 | Ca đích có sẵn. |
| `wp886_cc_khong_ten_roi_ve_sys_executable` | 1/1 | 0 | 0 | Ca đích có sẵn. |
| `wp886_cc_bo_ly_do_thieu_ten` | 1/1 | 0 | 0 | Ca đích có sẵn. |
| `wp886_cc_windows_nhan_ten_tran` | 1/1 | 0 | 0 | Ca đích có sẵn. |
| `wp886_cc_bo_muc_PATH_rong` | 1/1 | 0 | 0 | Ca đích có sẵn. |
| `wp886_cc_path_truoc_ten` | 1/1 | 0 | 0 | Ca đích có sẵn. |
| `review_cc_bo_X_OK` | 0/1 | 1 | 0 | Sống qua N6; ca reviewer H06/H07 giết riêng. |
| `review_cc_dao_thu_tu_PATH` | 0/1 | 1 | 0 | Sống qua N6; ca reviewer H06/H07 giết riêng. |

**9/9 có sẵn bị giết; 14/14 lượt ca đích chết đúng chốt; 0 tín dụng giả.** Hai mutant reviewer sống qua riêng N6 không được báo là đã chết ở đó: H06/H07 dựng đầu vào phân biệt và giết bằng `review_n1_skip_nonexec` / `review_n1_first_PATH`. Baseline sản phẩm đều xanh. Đây là gợi ý tăng răng, không phải phát hiện bản sản phẩm đang chọn sai.

Mutant thứ ba của reviewer đổi riêng nhánh Windows trong bản sao fixture `.cmd` về tên không đuôi: baseline `review_n8_fixture_native_suffix` qua; mutant chết `TinHieuChotCa`, frame `review_n8_fixture_native_suffix → bang`, message `fixture Windows khong co ten native PATHEXT: ['python3'], prefix=None`. Đây là **ca tĩnh reviewer**, không phải tuyên bố original preflight đã chạy trên Windows. Mã/đầu ra ở `hunts/fixture-extensionless-mutant.py`, `hunts/H01-n8-mutation.json`.

## Các hướng săn độc lập

Lệnh chung `PYTHONDONTWRITEBYTECODE=1 python3 -B out/run_hunts.py` rc=0; từng phép H01–H09 có đoạn mã nhãn rõ và JSON tại `hunts/`. H02 còn đối chiếu dịch newline từ bytes gốc qua TextIOWrapper để không làm mất CR do read_text; đó là mô phỏng lớp ghi, không phải CMD runtime. Không tạo payload thoát cây thư mục.

| Hướng | Giả thuyết · lệnh/phép đo | Output thật | Kết luận |
|---|---|---|---|
| H01 | Chạy đúng thân fixture qua seam os.name; resolver thuần Python; mutant tên không đuôi | `.cmd` → prefix python3.cmd; không đuôi → None; mutant chết đúng ca tĩnh | Fixture đáp ứng luật tên tĩnh; runtime Windows KHÔNG ĐO ĐƯỢC. Trên Linux dùng PATHEXT lowercase và chmod để mô hình hóa điều kiện file, không mô phỏng toàn bộ Windows |
| H02 | sys.executable có space, &, ngoặc, %, !; xem bytes fixture, list2cmdline và TextIOWrapper newline Windows | 4 biến thể giữ đường dẫn trong cặp quote, `%*`; mô phỏng ghi Windows cho đuôi `[42,13,13,10]`; cmd.exe/wine/pwsh đều None | Có thể quan sát lớp sinh/quote; giải nghĩa `%*`, biến phần trăm, delayed expansion, quote và CRCRLF trên CMD **KHÔNG ĐO ĐƯỢC**; không suy lỗi hay pass runtime |
| H03 | POSIX symlink bị cấm, original preflight có nuốt đỏ thành xanh không? `_chay_tien_kiem` + patch symlink_to→EPERM | Bình thường None (qua); denied trả `[python_alias_behavior_test, ... KHONG_DO_DUOC]` qua BoQuaMoiTruong | Không regression; main đếm tiền kiểm riêng và kéo rc lỗi nếu bỏ qua. Không tính denied là pass |
| H04 | T7 khi module probe trỏ interpreter khác checker; `_chay/kiem_tra_1` thực | PyYAML bare=9.9.9, absolute=6.0.3; jsonschema bare=9.9.9, absolute=4.26.0; cả hai DO `cac duong goi khac ban` | Không lỗi; đo hai package riêng, không chỉ python --version |
| H05 | Chỉ có py; mất -3 hoặc hỏng argv chứa space/quote/&/ngoặc/Unicode | prefix py,-3; rc=0, argv_equal=true cho đủ 5 đối số | ĐẠT POSIX; không suy batch `%*` từ phép POSIX |
| H06 | Python không executable đứng trước bản tốt; đối chiếu bash command -v và mutant bỏ X_OK | Head/Bash chọn H06-good/python; mutant chọn H06-bad/python và chết đúng TinHieuChotCa | Không lỗi sản phẩm; ca reviewer phân biệt được mutant sống qua N6 |
| H07 | Hai thư mục đều có python khác phiên bản; đổi thứ tự PATH | Head 3.10.11; mutant đảo PATH 3.11.12, chết đúng review_n1_first_PATH | Không lỗi sản phẩm; độc lập với thứ tự tên python/python3 |
| H08 | PATHEXT mặc định/tùy biến/thứ tự đuôi/đuôi có dấu chấm; so launcher native | 5/5 cấu hình kết quả bằng nhau, gồm EXE, CMD và None | Khớp repository resolver trong phép tĩnh Linux; không khẳng định semantics Windows filesystem thực |
| H09 | Merge master mang sửa ops test ngoài fixture vào diff PR hoặc tạo regression r858/r886 | AST ngoài fixture equal=true; head 14/15, base 7/15, new_failures=[] | Không thấy regression trong tập chọn lọc; không suy full suite khi timeout |
| H10 | Selftest đỏ vì rig ép core.abbrev, không phải ratchet của PR; `python3 -B out/probe_abbrev.py <base/head> <bad/good>` | Base/head với env ép false/false, bỏ ép true/true; tất cả 4 lệnh rc=0 | Cô lập một biến của rig, giữ mã test nguyên byte; full rerun được báo riêng |

Các hiện vật lệnh/rc/output nằm dưới `out/` và được tổng hợp trong verdict này. Không sửa cây head/base/mirror; không viết patch sản phẩm. Giới hạn chưa đo được giữ nguyên, không chuyển thành xanh.
