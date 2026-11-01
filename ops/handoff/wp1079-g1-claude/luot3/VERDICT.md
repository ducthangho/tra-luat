verdict: changes_requested
reviewed_sha: 7df242e83cfa416cae78d3d8f04c3e323b4cf922
spec_sha256: 81070fa2c5a00bc0bb63867c7173f310cba9002001b68a26d62726ec904cbf5b
Ket qua: 0 P0, 1 P1, 0 P2, 0 P3.

Các phản chứng F01/F05/F06/F07 lượt 2 và F01–F03 lượt 1 đã đóng trên HEAD này. Có một lỗi mới **F08**: hai ca đăng ký khác nhau nhưng sinh từ cùng hàm mẫu bị coi là gọi sang ca khác. Cả ba điểm chấm đều loại assertion thực sự của chính ca đích dù ca kia chưa chạy. Đây là chặn nhầm của bộ chấm, không phải tín dụng giả hoặc lỗi môi trường. `r13`/`t70` dùng helper mới đã giết được mutant thật; không gán lỗi ấy cho bản sửa r13 hiện tại.

provider: openai_codex
model_family: openai
execution_surface: codex_service
transport: machine
exact_model_id: runtime không cung cấp định danh endpoint để kiểm chứng độc lập
reviewer_role: reviewer độc lập với executor Claude
reviewed_tree: a2ec7650f3dc5dff34a8833631f16de8b365b7d7
packet_id: wp1079
revision: r1
generation: 4
lease: wp1079-r1-g4-claude
review_class: sensitive
review_call: 3/3 (cuối, theo PROMPT)

## Phạm vi, cách tìm và giới hạn

Đã đọc PROMPT, SPEC, hai verdict trước, hai finding nguồn #484, diff tổng và diff từ lượt 2; kiểm kê toàn bộ 31 thông điệp commit trong BASE..HEAD. Băm SPEC được tự tính bằng `sha256sum ../SPEC.md`. `python3 -B ../review3/audit.py` xác nhận `DIFF_MATCH True`: diff thực khớp byte với `diff.patch`, đúng hai tệp, **623 dòng thêm / 118 dòng xóa**. 623 nằm trong trần 640 đã cho phép. Phần ngoài `.claude/` giống exact master đã merge (`767a68d^2`): `OUTSIDE_MASTER_DELTA ''`. Không tính trần dòng hoặc nợ #1117 thành finding.

Cách tìm lời khai: duyệt máy từng dòng thêm trong diff, không chỉ tìm từ khóa; ghi đủ 623 dòng và số dòng tại HEAD vào [claims-all-added-lines.tsv](review3/claims-all-added-lines.tsv). Đọc các hunk có dòng xóa cùng ngữ cảnh để tìm thay đổi ngữ nghĩa; quét AST để đếm ca/mutant, lần theo lời gọi giữa các ca đã đăng ký và nhóm `__code__`. Lưu toàn bộ message bằng `git log --format='%H%n%B' BASE..HEAD` vào [commits.txt](review3/commits.txt); phân loại 7 commit của nhánh packet và 24 commit kế thừa master trong [commit-inventory.json](review3/commit-inventory.json). BANG DO bên dưới nhóm các lời khai có cùng phép đo; danh sách nhóm không được coi là chứng cứ rằng mọi lời khai lịch sử đã được xác minh.

Các lệnh trong bảng được trình bày để chạy từ **`cay-kho/`**. Các script đã được gọi từ thư mục packet và tự định vị target; ba suite bên trong chạy với cwd đúng HEAD/base ghi trong JSON. Tên script rút gọn ở BANG DO nghĩa là `python3 -B ../review3/<tên script>`. Script tự tìm cây theo `__file__`, lưu log ở `review3/` và tạo mọi bản sao/đột biến ngoài `cay-kho/`. Bộ suite được gọi đúng ba command yêu cầu; command, cwd, rc, thời lượng lưu riêng trong `review3/{head,base}-{launcher,mutation,credential}.json`. Môi trường phép đo dùng HOME tạm, PATH hiện có, UTF-8, `PYTHONDONTWRITEBYTECODE=1`, `PIP_NO_INDEX=1`, cấu hình Git trơ; không kế thừa credential hoặc init shell của phiên. Các probe dùng dữ liệu trơ và shim. Không gọi mạng, credential thật, push hoặc sửa cây executor. Tool `environment_status` của skill môi trường không có trong phiên này; không suy đoán trạng thái mạng/credential từ đó.

`ls -ld /tmp/.git` trả `dr-xr-xr-x`; `/var/tmp` từ chối ghi với `Errno 30 Read-only file system`. Không xóa `.git`, đổi backend hoặc làm giả điều kiện A1 để lấy gate xanh. HEAD/base có **cùng 23 tên ca lỗi**, cùng 10 cặp tên/lý do bỏ qua; [summary.json](review3/summary.json) giữ danh sách đầy đủ. Những lỗi storage/home và lỗi tiếp theo như không có run.json cũng xuất hiện trên base; không tính thành hồi quy. Windows thật, A1 với tiền đề `/tmp/.git` vắng và check-run CI exact HEAD là **KHÔNG ĐO ĐƯỢC** tại đây.

## Đóng finding cũ trước

| Finding | Lệnh chạy lại | Output thật | Kết luận |
|---|---|---|---|
| F01 lượt 1 + F01 lượt 2: tên lớp/qualname và stdout giả | `python3 -B ../review3/probe_oracles.py` | RuntimeError và AssertionError có cùng qualname → `loi`; stdout giả → `loi (...khong co ket qua kenh, rc=1)`; own assertion → `giet` | Đóng trên các phản chứng cũ; không nhận tên lớp làm identity |
| F02 lượt 1: bước dò Bash còn BASH_ENV/HOME cha | `python3 -B ../review3/probe_fixture.py` | Base: 7 installer, 2 init. HEAD: 0/0; cả hai probe Bash và hook dùng HOME fixture, không BASH_ENV/ENV/BASH_FUNC_* | Đóng trên POSIX đã đo |
| F03 lượt 1: khóa credential chỉ kiểm văn bản điểm nối | `python3 -B ../review3/probe_registered_mutations.py` | `wp1079_cc_chay_suite_bo_ten_do` giữ lời gọi cũ trong comment → `r1079_cc_chay_suite_phai_do_hanh_vi RIGHT_SIGNAL` | Đóng; đỏ bằng tín hiệu của chính ca |
| F05 lượt 2: assertion từ ca đăng ký khác | `python3 -B ../review3/probe_oracles.py` | Product/harness → `loi`; credential → `t2...(chot cua ca khac)`; own/helper vẫn `giet` | Phản chứng cấp nhầm tín dụng đã đóng; bản sửa sinh chặn nhầm mới F08 |
| F06 lượt 2: target thiếu/trùng rơi khỏi mẫu số | Cùng script | `missing`, `partial`, `duplicate` đều `(1,0)`, in `SAI - ca dich khong tim thay/trung` | Đóng; không coi target thiếu là skip |
| F07 lượt 2: khóa neutral sống khi chỉ giữ literal | Cùng script; `python3 -B ../review3/audit_debt_history.py` | HEAD khóa hành vi PASS; cùng phản chứng trên d929ee2 → `RIGHT_SIGNAL`; hai mutant bỏ neutral hiện tại đều giết đúng khóa | Đóng phản chứng cũ |

`probe_oracles.py` chạy riêng cả **15 ca r1079** trên HEAD: 15 PASS. `audit_debt_history.py` dựng bản sao d929ee2 và chạy lại sáu ca HINT lượt 2 đã được nhận: **6/6 RIGHT_SIGNAL**; các ca ấy PASS trên HEAD. Không tái nêu finding đã được chủ kho chuyển thành nợ #1117. Kiểm AST phần thực thi receiver xác nhận bản sửa này không đổi phần đó.

## BANG NGHIEM THU

| Tiêu chí | Lệnh | Output thực tế | Đạt? |
|---|---|---|---|
| M1: (a) chỉ tín hiệu riêng được tín dụng, lỗi khác có loại; giữ skip | `python3 -B ../review3/probe_oracles.py`; `python3 -B ../review3/probe_skips_and_b.py` | Own/helper `(0,0)`; AttributeError/bare/wrapped AssertionError `(1,0)` và `tin dung gia`; all-skip `(0,1)`, mixed `(0,0)`, khớp base | Đạt phân loại âm và skip; đối chứng dương còn F08 |
| M2: neutral a/b, fail-close và cache | Hai script trên | Cả a/b neutral lỗi hoặc chốt `(1,0)`, có `neutral do`; hai mutant cùng target: neutral=1, mutant=2 | Đạt hành vi đã đo |
| M3: (b) nhận tín hiệu thật, không dựa headline/rc | Hai script trên | Harness own `(0,0)`; lỗi thường, wrapped và stdout giả không được kill; same qualname → `khac:TinHieuChotCa` | Đạt chống tín dụng giả cũ; chặn nhầm dương F08 |
| M4: (c) lớp riêng hoặc bare assert đúng tệp | `python3 -B ../review3/probe_oracles.py`; `python3 -B ../review3/probe_credential_mutants.py` | Native t2 assert được nhận; implementation/wrapped AssertionError bị gắn loại; tệp khác cùng dòng assert bị loại; 13 mutant có neutral xanh giết đúng assertion | Đạt kiểm loại/tệp; không giữ mọi kill thật do F08 |
| M5: phục hồi 11 mutant bằng assertion ca đích | `python3 -B ../review3/probe_base.py` | HEAD: 10 OK bằng `giet`; `g2_rejected_refresh_khong_phu_thuoc_metadata` → `KHONG_DO_NEUTRAL ... OSError` | 10 đạt, 1 KHÔNG ĐO ĐƯỢC do home/storage của môi trường |
| M6: N13, 0 installer ngoài npm giả, HOME/env và thứ tự | `python3 -B ../review3/probe_fixture.py` | HEAD `PASS INSTALLERS 0 INIT 0`, OUTER `[]`; hai npm giả trước `LAUNCHER chuan-bi`, rồi doctor | Đạt trên POSIX đã đo |
| M7: khóa a/b/c và mutant đúng ca, giữ kill thật | `python3 -B ../review3/probe_registered_mutations.py`; `python3 -B ../review3/probe_alias.py`; `python3 -B ../review3/make_hint.py` | 21 mutant/24 target outcomes đều RIGHT_SIGNAL; nhưng ca đích sinh chung hàm mẫu bị loại ở a/b/c; 3 HINT đỏ đúng tín hiệu của chính ca | **Không — F08/P1**, thiếu đối chứng dương này |
| A1: N/N, M/M và TỔNG ĐẠT khi /tmp/.git vắng | `python3 -B ../review3/run_suites.py`; `python3 -B ../review3/summarize.py` | HEAD: 312/335, 10 skip, 23 lỗi; mutation 507/543, 4 không đo; credential 13/18, nền đỏ | **KHÔNG ĐO ĐƯỢC đúng tiền đề**; kết quả thật được ghi, không báo gate xanh |
| A2: scorer mới trên ca base, khóa đỏ trên scorer base; N13 đỏ với fixture base | `python3 -B ../review3/probe_base.py`; `python3 -B ../review3/probe_fixture_base_lock.py` | Base product: 397 OK, 34 neutral đỏ, 11 SAI, 1 all-skip, 3 giới hạn Windows không chạy. Các khóa base a/neutral/c RIGHT_SIGNAL. N13 base + hậu điều mới RIGHT_SIGNAL với 7 AMBIENT | Đạt các phản chứng đo được; **không tái hiện đúng toàn bộ danh sách 11 trong môi trường nghiệm thu**, giải thích dưới đây |
| A3: đo A/B installer, base >0, HEAD=0 | `python3 -B ../review3/probe_fixture.py` | 7 → 0 installer; 2 → 0 init; HOME cha → HOME fixture; không installer thật được gọi | Đạt |
| A4: lint delta, diff-check, doctrine, CI exact head | `python3 -B ../review3/audit.py`; `git diff --check 7eeb1d9a10aea8e1805b66fbf3d68549eb6778da HEAD -- .claude`; `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .` | Ruff F841 5→5, delta 0; packet diff rc=0; doctrine rc=0, 10 tệp/0 chỗ. Diff toàn BASE..HEAD rc=2, cùng whitespace ở master. CI không truy cập do cấm mạng | Phần local của packet đạt; toàn diff có lỗi kế thừa master; CI **KHÔNG ĐO ĐƯỢC** |

A2 không được đọc từ số đếm đơn thuần. Trong 11 `SAI` của ca base, có **10/11 tên đã nêu trong SPEC**, cộng `PROMPT_FILE_mo_coi_di_tiep`: r13 cũ gọi t70 đã đăng ký, nay bị chốt nguồn gốc F05 loại. Tên SPEC còn lại là `g2_rejected_refresh_khong_phu_thuoc_metadata`, chuyển sang neutral đỏ vì `Codex home is inside a repository`. Ngoài ra có 33 neutral đỏ khác và một target tự bỏ qua; không giấu chúng vào 11. Đây là lý do không xác nhận phép đo “đúng 11 SAI kể trên”. Trên ca HEAD, r13 đã chuyển sang `_t70_prompt_file_chan`: đo riêng cả r13 và t70 đều `OK giet 1/1`, runner `(0,0)`.

`probe_base.py` chạy scorer HEAD trên **443 mutant product của base** có thể chạy theo giới hạn nền, với đúng lớp tín hiệu và danh sách CA của module base, không nhận nhầm lớp do import khác module. Đầu ra và từng kết quả neutral/mutant lưu tại [base-strict.json](review3/base-strict.json). Không lấy lỗi vô can hoặc neutral đỏ làm tín dụng. Phép đo này không giả lập `/tmp/.git` vắng.

## BANG DO

| Khẳng định | Diff khai / vị trí | Đo được bằng lệnh | Khớp? |
|---|---|---|---|
| Tín hiệu ca khác bị loại theo traceback | `chot_tu_ca_khac`; `ten_do(..., ca)`; message 5548919 | `probe_oracles.py`: other-case không được tín dụng; `probe_alias.py`: own assertion dùng chung code cũng bị loại | **Khớp ca âm; sai ở ca dương F08**. `__code__` không phải identity duy nhất của callable |
| Chỉ TinHieuChotCa ở a; wrapped/bare lỗi được chẩn đoán | `cham_mot_ca` và comment runner | `probe_oracles.py`: attr/bare/wrapped → loi, đầy đủ tên target và loại; own/helper → giet | Khớp trên các ca code riêng; F08 là giới hạn đo được |
| Neutral không qua làm cổng đỏ; cache mỗi target | `ket_luan_mutant`, hai cache và nhánh runner | `probe_oracles.py`, `probe_skips_and_b.py`: a/b `(1,0)`; 1 neutral/2 mutant | Khớp |
| Mẫu số giữ skip nền, không mất ca vắng | `ket_luan_mutant`; kiểm F06 trước neutral a | Cùng hai script: all/mixed giống base; missing/partial/duplicate đỏ | Khớp |
| Bare assert ở ba ca được đổi thành chốt; r01/r10/t115 không còn chết do lỗi vô can | Các hunk M5, `_r1079_run_json`, catch hợp đồng `_doc_mcp_json` | `probe_base.py`: base bare/file/JSON/type errors mất tín dụng; HEAD 10 target xanh-neutral chết bằng chốt | Khớp 10 mutant đo được; recovery storage chưa đo được |
| r13/t70 dùng helper chung, sửa hai lỗi trên 5548919 | `_t70_prompt_file_chan`, message 7df242e | `probe_oracles.py`: cả hai kill thật OK; `audit_debt_history.py`: 5548919 kill 1/2, mỏ neo classifier count 0; HEAD neo count 1 và mutant RIGHT_SIGNAL | Khớp phần hành vi; số 541/543 lịch sử chưa xác minh trong môi trường cũ |
| N13 giả rg/actionlint, che installer, giữ npm trước materialize | Fixture và comment F02 | `probe_fixture.py`: nhật ký INNER có npm codex, npm Claude, chuan-bi, doctor; HEAD OUTER rỗng | Khớp phép đo hiện tại; không suy thành cô lập mọi công cụ/hook tương lai |
| Dò Bash cũng dùng env sạch, HOME tạm, bỏ hàm Bash export | N13 patch.dict(clear=True), env lọc | Cùng script: ba subprocess đều HOME fixture, BASH_ENV/ENV null, functions []; parent thù địch ở base sinh 2 init/7 installer | Khớp |
| Credential nhận bare assert đúng tệp, loại implementation/wrapped và tệp khác cùng dòng | `la_chot_cua_suite`, lớp riêng và các raise thay thế | `probe_oracles.py` chạy ca khóa thật; `probe_credential_mutants.py`: 13 RIGHT_ASSERTION/5 neutral đỏ | Khớp phần loại/tệp; không đủ identity target khi dùng chung code, F08 |
| `chay_suite` dùng `ten_do(..., ca)`, không chỉ còn chuỗi trong comment | Message ee23c44/5548919, chay_suite | `probe_oracles.py` chạy neutral/own/attr/wrapped/other; mutant giữ comment trong `probe_registered_mutations.py` đỏ đúng ca | Khớp điểm nối hành vi |
| Bản sao harness giữ bố cục kho và phụ thuộc đọc fixture | `_dung_cay_harness`, message c73dff3 | Các probe harness đều chạy child từ `.claude/dev`, có hooks và bash_nen; bộ mutation hiện tại chỉ còn neutral đỏ do môi trường đã nêu | Khớp các đường đang đo; không khẳng định đây là clone đầy đủ kho |
| Kết quả b lấy từ kênh riêng; tên lớp khác có tiền tố; env kênh gỡ trước ca | `cham_lap_ca`, `chay_bo_ca`, main; ee23c44 và 5548919 | `probe_oracles.py`: stdout/same-qualname bị loại, `env_removed` neutral/mutant đều qua; nonce sai bị khóa loại | Khớp phần đang được tuyên bố tại HEAD; không mở rộng bảo đảm vượt giới hạn đã ghi trong docstring |
| Mỗi chốt mới có mutant giết đúng ca | Các bảng #1079; chỉnh anchor d929ee2/7df242e | `probe_registered_mutations.py`: 21 mutant, 24 target outcomes, 24 RIGHT_SIGNAL; `head-mutation.out`: 21 mutant wp1079 OK | Khớp mutant hiện có; không chứng minh đầy đủ đối chứng dương, F08 |
| Đã nhận 6/7 HINT lượt 2, 4 HINT lượt 1 | Message 5548919/ee23c44 và tên ca | `audit.py`, `probe_oracles.py`, `audit_debt_history.py`: các ca hiện diện/chạy; sáu ca lượt 2 tái hiện trên d929ee2 | Khớp bố cục và hành vi. Không có HINT lượt 1/2 nguyên byte ở packet để tự băm provenance cũ: **KHÔNG ĐO ĐƯỢC băm đó** |
| Các số lịch sử WIP +356, 531/536, 538/539, 541/543; “10/10” ở phiên executor | d8f8998/c73dff3/d929ee2/7df242e messages | Git có thể đo numstat từng SHA; `audit_debt_history.py` đo lại hai lỗi 5548919 và những hồi quy cũ; log hiện tại có counts khác do môi trường | Chỉ xác nhận source/neo/hành vi hiện tại; không xác nhận số suite của môi trường lịch sử chưa có log độc lập |
| Merge master, các lời khai CI/land/spec trong 24 commit kế thừa | Toàn bộ `git log --format=%B BASE..HEAD` | `audit.py`: ngoài .claude bằng master; `commit-inventory.json` liệt kê đủ SHA/body, phân loại bằng merge-base | Xác minh nguồn kế thừa; các CI run, review comment, quyết định chủ kho lịch sử trong message **KHÔNG ĐO ĐƯỢC từ check-run** vì không mạng; không quy thành finding packet |
| Không sửa sản phẩm/hook hoặc cây executor | Toàn diff và lời khai runner | Diff đúng hai tệp; `python3 -B ../review3/verify_tree.py` → 10161 tệp, changed=[], git_status rỗng | Khớp toàn vẹn đo được |

Băm/check local không thay thế CI exact HEAD. `git diff --check 7eeb1d9a10aea8e1805b66fbf3d68549eb6778da HEAD` thật sự rc=2 tại `ops/specs/launcher-sandbox-lay-mau-r2.md:242: new blank line at EOF`; `git diff --check 7eeb1d9a10aea8e1805b66fbf3d68549eb6778da 767a68d^2` cũng đúng rc=2 và cùng output. Với write set `.claude`, rc=0. Bằng chứng ở [diff-checks.json](review3/diff-checks.json); không che lỗi toàn diff nhưng cũng không gán lỗi master cho packet.

## BANG TEST

| Bộ | N/M, rc | Bỏ qua / giới hạn |
|---|---|---|
| HEAD `python3 .claude/dev/launcher_test.py` | **312/335** ca đã chạy qua; tổng 345, lỗi 23; rc=1 | **10 BO QUA**: 1 fixture Windows, 8 venv/pip không dựng được offline, 1 native Windows SID |
| BASE cùng command | **297/320**; tổng 330, lỗi 23; rc=1 | Cùng 10 tên/lý do bỏ qua; cùng tập 23 lỗi |
| HEAD `python3 .claude/dev/launcher_test.py --dot-bien` | **507/543**; rc=1 | **4 KHÔNG ĐO ĐƯỢC theo nền**; 36 SAI đều neutral đỏ, không cấp tín dụng |
| BASE cùng command | **522/522**; rc=0 | Cùng 4 theo nền; headline xanh của scorer cũ không chứng minh neutral xanh |
| HEAD `python3 .claude/dev/codex_cred_test.py` | Nền **13/18**, `TỔNG: ĐỎ`; rc=1 | Không chạy mutation chính thức vì neutral đỏ, **không gọi 5 lỗi ấy là skip** |
| BASE cùng command | Nền **13/18**, cùng 5 tên lỗi, `TỔNG: ĐỎ`; rc=1 | Tương tự; scorer cũ chưa gắn suffix loại vào các tên lỗi |
| Credential đo từng mutant sau neutral đúng target | **13/13 RIGHT_ASSERTION** đo được | 5/18 KHÔNG ĐO NEUTRAL, ghi riêng trong `probe-credential-mutants.log`; không thay thế gate chính thức |
| Khóa #1079 trên HEAD | **15/15 PASS** | Chạy riêng, log `probe-oracles.log` |
| Mutant #1079 trên bản sao | **21/21**, **24/24 target outcomes RIGHT_SIGNAL** | Có xác minh tín hiệu không xuất phát từ ca đăng ký khác |
| Scorer hiện tại trên ca product base | **397 OK / 443** được xét theo nền; 11 SAI, 34 neutral đỏ, 1 all-skip | 3 giới hạn Windows loại trước; từng tên ở `base-strict.json` |
| 11 mutant SPEC trên ca HEAD | **10/10 OK** đo được | 1 neutral đỏ/OSError chưa đo được |
| Probe chặn nhầm F08 | a `(1,0)`, b `(1,0)`, c gắn `(chot cua ca khac)` | Neutral xanh; alias không chạy; đây là phản chứng bộ chấm |
| HINT bổ sung | **3/3 đỏ RIGHT_SIGNAL** trên bản sao HEAD; dry-run rc=0 | Chưa có runtime fix để xác nhận hậu vá; không áp lên cây thật |
| Ruff F trên hai tệp scope | **F841 5→5**, delta 0; cả hai ruff rc=1 do lỗi nền | `--no-cache`, không làm bẩn repo; so code/message/file, không so số dòng đã dịch |
| Doctrine / diff-check write set | rc=0 / rc=0 | CI exact HEAD chưa đo được |

Năm ca credential neutral đỏ là t6, t9, t15, t16, t18 (tên đầy đủ có trong log). Cả base và HEAD đều không qua nên không được lấy kết quả mutation của năm ca đó làm chứng cứ dương.

## BANG SAN

| Hướng độc lập | Lệnh chạy từ cay-kho | Output thật | Phân loại |
|---|---|---|---|
| 1. AttributeError đổi kiểu bằng except sang AssertionError | `python3 -B ../review3/probe_oracles.py` | a `wrapped → loi`; b `wrapped → khac:AssertionError`; c target mang `(AssertionError)` | KHÔNG PHẢI LỖI |
| 2. AssertionError trực tiếp từ triển khai | Cùng script | a/b không kill; c `t2...(AssertionError)` khác tên target | KHÔNG PHẢI LỖI |
| 3. RuntimeError/AssertionError trùng qualname tín hiệu | Cùng script | Hai loại đều loi; harness tiền tố `khac:TinHieuChotCa` | KHÔNG PHẢI LỖI; F01 đóng |
| 4. Assertion của ca đăng ký khác | Cùng script | a/b loi; c `(chot cua ca khac)`; own/helper vẫn giet | KHÔNG PHẢI LỖI trên ca code riêng; F05 cũ đóng |
| 5. Neutral đã lỗi hoặc đã ném chốt | `python3 -B ../review3/probe_skips_and_b.py`; `python3 -B ../review3/probe_oracles.py` | a/b `(1,0)` và neutral do cho cả hai kiểu | KHÔNG PHẢI LỖI |
| 6. Toàn skip và vừa skip vừa chạy | `python3 -B ../review3/probe_skips_and_b.py` | Base/head a all `(0,1)`, mixed `(0,0)`; HEAD b cũng `(0,1)`/`(0,0)` | KHÔNG PHẢI LỖI |
| 7. Child in LOAI_HONG/headline giả rồi exit | `python3 -B ../review3/probe_oracles.py` | `HARNESS_CLASSIFY stdout ... mutant ('loi', 'review_target(khong co ket qua kenh, rc=1)')` | KHÔNG PHẢI LỖI |
| 8. Tệp khác có assert cùng số dòng | Cùng script, khóa `r1079_cc_test_chi_chot_cua_suite_la_do` | Khóa PASS; mutant bỏ so tệp → RIGHT_SIGNAL trong `probe_registered_mutations.py` | KHÔNG PHẢI LỖI |
| 9. Target mất hết, mất một phần, hoặc trùng | `python3 -B ../review3/probe_oracles.py` | Ba trường hợp đều `(1,0)` | KHÔNG PHẢI LỖI; F06 đóng |
| 10. Giữ literal neutral nhưng bỏ hành vi | Cùng script; `python3 -B ../review3/audit_debt_history.py` | HEAD meta-lock PASS; d929ee2 cùng phản chứng RIGHT_SIGNAL | KHÔNG PHẢI LỖI; F07 đóng |
| 11. Cache neutral và bản gốc đúng | `python3 -B ../review3/probe_skips_and_b.py`; `python3 -B ../review3/probe_oracles.py` | Hai mutant/target: a neutral=1/mutant=2; b `harness_goc` 1 lần, mutant 2 lần | KHÔNG PHẢI LỖI |
| 12. PATH thù địch, rg hỏng, installer log, BASH_ENV/ENV/HOME/hàm Bash cha | `python3 -B ../review3/probe_fixture.py` | Base PASS nhưng 7 installer/2 init; HEAD PASS với 0/0, OUTER [] | KHÔNG PHẢI LỖI của HEAD |
| 13. Gỡ từng chốt mới và hồi phục fixture base | `python3 -B ../review3/probe_registered_mutations.py`; `python3 -B ../review3/probe_fixture_base_lock.py` | 24/24 RIGHT_SIGNAL; base N13 + hậu điều mới RIGHT_SIGNAL, AMBIENT_COUNT 7 | KHÔNG PHẢI LỖI với các mutant đã đăng ký |
| 14. Kill thật r13/t70 qua helper chung | `python3 -B ../review3/probe_oracles.py` | Mỗi ca riêng `(0,0)`, `OK giet 1/1` cho PROMPT_FILE_mo_coi_di_tiep | KHÔNG PHẢI LỖI; sửa r13 hiện tại có tác dụng |
| 15. Hai callable đăng ký chung hàm mẫu, chỉ chạy target | `python3 -B ../review3/probe_alias.py` | PRODUCT_FACTORY `(1,0)`, HARNESS_FACTORY `(1,0)`, CREDENTIAL_FACTORY mutant `review_target(chot cua ca khac)` | **LỖI — F08/P1** |
| 16. Gate đầy đủ dưới bẫy môi trường và CI không mạng | `python3 -B ../review3/run_suites.py`; `ls -ld /tmp/.git` | 23 lỗi launcher và 5 lỗi credential trùng base, .git chỉ đọc; không thể đọc check-run | **KHÔNG ĐO ĐƯỢC** A1 chuẩn/CI; không suy thành hồi quy |

### F08-shared-code-khong-phai-ca-khac [P1] Bộ chấm loại assertion của chính ca khi một ca khác dùng chung hàm mẫu

TEP/DONG: `.claude/dev/launcher_test.py:168` đưa code của mọi callable khác identity vào `khac`, `:171` kiểm membership; ảnh hưởng `cham_mot_ca:185` và reporter `:14759`. `.claude/dev/codex_cred_test.py:584`/`:587` làm tương tự, được gọi thật từ `chay_suite:609`.

VAN DE: Hai function được tạo từ một factory có thể khác object, tên và closure nhưng **cùng `__code__`**. Đây là cách hợp lệ để đăng ký hai ca/bí danh có dữ liệu riêng; decorator `ca` không cấm nó. Khi chỉ chạy function đích và assertion của chính function ấy thất bại, tập `khac` vẫn chứa **chính code của target** thông qua callable còn lại. Thuật toán kết luận có assertion của ca khác dù callable kia chưa hề được gọi. Vì vậy một kill thật bị báo tín dụng giả ở a/b, hoặc không khớp `phai_chet` ở c. Vi phạm đối chứng dương M7 (“assertion của chính ca phải vẫn là một lần giết”) và yêu cầu kiểm chặn nhầm của PROMPT.

Đây khác với ca gọi thật sang một ca đăng ký khác của F05 cũ. Probe ghi dấu từng lần gọi: chỉ `review_target` chạy ở neutral và mutant; `review_alias` không chạy. Không đổi danh tính lớp tín hiệu, không giả traceback, nonce, stdout hoặc kết quả kênh.

DA THU NGHIEM: `python3 -B ../review3/probe_alias.py` tại exact HEAD, mọi mutant ở bản sao ngoài cây. Dựng hai ca bằng cùng factory, khác tên/closure. Product neutral dựa trên launcher gốc qua; mutant có đường dẫn riêng làm chính chốt target đỏ. Harness chạy neutral và mutant qua child/runner thật. Credential chạy `chay_suite` thật, `nap` trả module trơ; chính hàm target của suite ném lớp tín hiệu thật.

```text
review_own_alias             SAI giet 0/1: ... [tin dung gia: review_target(chot cua ca khac)]
PRODUCT_FACTORY (1, 0) calls ['review_target', 'review_target'] same_code True
review_factory_alias        SAI giet 0/1: ... [tin dung gia: review_target(khac:TinHieuChotCa)]
HARNESS_FACTORY (1, 0)
CREDENTIAL_FACTORY neutral [] calls ['review_target']
CREDENTIAL_FACTORY mutant ['review_target(chot cua ca khac)'] calls ['review_target', 'review_target']
```

Đối chứng: cùng probe/scorer với một ca code riêng hoặc helper chưa đăng ký nhận `giet`; gọi thật sang ca đã đăng ký khác bị loại đúng. `probe_oracles.py` đo mutant sản phẩm thật giết riêng r13 và t70 bằng helper mới, cả hai `(0,0)`. Quét AST/runtime trong `audit.py` thấy **chưa có nhóm CA nào dùng chung code ở 345/18 ca hiện tại**; do đó không khai rằng F08 đã làm một ca sẵn có đỏ trong full suite. Finding là sai hành vi có thể tái hiện của bộ chấm trên kiểu ca hợp lệ, không lấy 23 lỗi môi trường làm bằng chứng.

DO TIN: cao về cả ba đường và nguyên nhân tập `khac`; khả năng gặp trong các ca sẵn có hiện tại được giới hạn rõ như trên. P1 theo thang PROMPT vì là sai hành vi đo được.

Gợi ý vá ở `chot_tu_ca_khac` và `ten_do`: đừng dùng việc một code object xuất hiện trong registry của callable khác như bằng chứng callable ấy đã chạy. Cần phân biệt identity/nguồn chốt của ca đang đo với mã dùng chung; ít nhất phải tránh đưa code của chính target vào tập loại chỉ vì có bí danh/hàm mẫu. Đồng thời giữ việc loại lời gọi thực sự sang ca đăng ký khác. Nếu bộ chấm cần identity ở thời điểm vào ca, ghi nhận identity tại ranh giới đăng ký/chạy ca thay vì suy duy nhất từ `f_code`. Đây là hướng sửa bằng lời; không cung cấp/áp runtime fix vào cây review.

Ca khóa trong `HINT.patch`: ba ca product/harness/credential đều có neutral xanh, target tự ném chốt thật, callable chung mẫu không chạy; mong đợi lần lượt `(0,0)`, `giet`, tập đỏ đúng tên target. `make_hint.py` đã chạy cả ba trên bản sao HEAD: **3/3 đỏ bằng TinHieuChotCa của chính ca hồi quy**, với thông điệp xác nhận chặn nhầm chứ không phải lỗi fixture/mỏ neo. Sau sửa phải qua ba ca; đưa lại phép suy `__code__` hiện tại phải làm chúng đỏ lại đúng lý do. Giữ 21 mutant đang có, nhất là hai đường other-case và credential-origin, để tránh đổi chặn nhầm thành tín dụng giả.

Rủi ro sửa: xóa toàn bộ kiểm nguồn gốc sẽ mở lại F05; xử lý alias bằng cách gộp theo tên có thể mở lại F06 hoặc mất cache/skip. Cần giữ đối chứng other-case âm, helper/r13/t70 dương, target thiếu/trùng, neutral đỏ và all-skip/mixed. Chưa có runtime fix nên chưa khẳng định hậu vá đã xanh.

## HINT và bảo toàn cây

[HINT.patch](HINT.patch) chỉ thêm ba ca hồi quy F08, áp bằng `patch -p0` từ `cay-kho/`. **Chưa áp/chạy trên cây thật — executor tự dẫn xuất, tự đo, tự chịu trách nhiệm commit và khai hint_provenance nếu dùng.** Đã `patch --dry-run -p0 -d cay-kho < HINT.patch`: rc=0, `checking file .claude/dev/launcher_test.py`. Thử ca trên bản sao, không lấy ngoại lệ vô can làm răng. Băm SHA-256 hiện tại: `813270e9c3fd6ab40740ec0c1c12d75293d2f7422a2bf8e107bece900505eef5`.

`python3 -B ../review3/verify_tree.py`: so nội dung **10161 tệp** với Git blob ở exact HEAD; `changed=[]`; `git status --porcelain` rỗng; HEAD/tree vẫn như đầu verdict. Ba tệp `.cmd` có CRLF khớp thuộc tính `eol=crlf`; chuẩn hóa theo Git thì khớp blob. Không tạo `.pyc`, không đổi cây executor. Bằng chứng cuối ở [final-integrity.json](review3/final-integrity.json).
