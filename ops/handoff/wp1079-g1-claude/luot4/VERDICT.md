verdict: changes_requested
reviewed_sha: 5368c34b77f07a820ca38a7db4d85aa1fe5624e2
spec_sha256: 81070fa2c5a00bc0bb63867c7173f310cba9002001b68a26d62726ec904cbf5b
Ket qua: 0 P0, 2 P1, 0 P2, 0 P3.

F08 đã hết chặn nhầm đối chứng cũ, nhưng chính bản vá mở lại **F05 ở cả ba đường chấm** khi target gọi thật sang ca khác cùng factory. Ngoài ra, thông điệp commit `5548919` khai sai số mutant mới (5 thay vì 4); mức P1 của lời khai sai đo được áp theo thang PROMPT. Không tách lời khai “F05 vẫn bị loại” của commit cuối thành finding thứ ba: nó là cùng biểu hiện của F05.

provider: openai_codex
model_family: openai
execution_surface: codex_service
transport: machine
exact_model_id: runtime không cung cấp định danh endpoint để kiểm chứng độc lập
reviewer_role: độc lập với executor Claude; không dùng context executor
review_axes: spec, standards_security
reviewed_tree: ea90b2dff1a75301b09d2f2ad85d6d7c7b70beb3
packet_id: wp1079
revision: r1
generation: 5
lease: wp1079-r1-g5-claude
review_class: sensitive
review_call: 4/4 (cuối)

Chỉ đọc và đo; không sửa `cay-kho/`, không push, không gọi mạng hoặc dùng credential thật. Trần 720 dòng thêm do chủ kho cho phép không là finding. F04 đã chuyển thành nợ #1117 theo PROMPT; không đưa lại vào finding. AST của phần thực thi `cham_lap_ca` so với `d929ee2` không đổi, nên không thấy bản vá này làm nợ ấy tệ hơn.

## Cách chạy và cách tìm lời khai

Mọi lệnh `python3 -B ../review4/<script>.py` dưới đây chạy được từ `cay-kho/`. `common.py` xác định đường dẫn theo vị trí script. Script suite thật sự gọi ba lệnh được yêu cầu bằng `/usr/bin/python3`; môi trường tối thiểu chỉ giữ PATH, locale và HOME tạm tuyệt đối, thêm `PYTHONDONTWRITEBYTECODE=1`, `PIP_NO_INDEX=1`, `PIP_DISABLE_PIP_VERSION_CHECK=1`, cấu hình Git trơ. Credential/secret của cha không được truyền. Không đọc giá trị credential. Các bản sao BASE/HEAD cũ được tạo bằng `git archive` đúng OID, ngoài cây review.

Các script phản chứng từ lượt 3 được chép vào `review4/`, cập nhật root/HEAD, đọc lại mã rồi **chạy lại trong lượt này**; không lấy log cũ làm kết quả mới. Hai phép mới là `probe_shared_call.py` và ba ca trong `make_hint.py`. Các HINT cũ dùng đối chiếu provenance được chép nguyên byte vào `review4/previous-hints/`.

Để không chỉ lập danh sách theo trí nhớ, `audit.py` duyệt **toàn diff** bằng các hunk `@@`, ghi đủ **704 dòng thêm**, kèm tệp và số dòng vào [claims-all-added-lines.tsv](review4/claims-all-added-lines.tsv), xác nhận diff cung cấp khớp Git. Đã đọc các hunk sửa assertion, helper, fixture, các khóa, bảng mutant, runner/reporter/kênh. `inventory_commits.py` dùng `rev-list BASE..HEAD`, lấy toàn `%B` và đường dẫn từng commit: **32 commit = 7 commit sửa packet + 25 master/merge**, không chỉ `-- .claude`. Toàn văn ở [commits.txt](review4/commits.txt), phân loại ở [commit-inventory.json](review4/commit-inventory.json). `claim_history.py` dùng AST so tên/nội dung từng mutant giữa mỗi commit packet và cha trực tiếp; vì vậy phát hiện cả sai lệch số lượng mà danh sách lời khai tự chọn dễ bỏ sót.

BANG DO nhóm lời khai theo phép kiểm chung, không có nghĩa đã chứng minh mọi mệnh đề phổ quát hoặc lịch sử. Số CI, review comment, quyền chủ kho và kết quả trên máy executor không có check-run/log độc lập trong môi trường này được ghi **KHÔNG ĐO ĐƯỢC**. Chúng không trở thành “khớp” chỉ vì xuất hiện trong Git message.

Bẫy môi trường: `ls -ld /tmp/.git` → thư mục `dr-xr-xr-x` tồn tại. Không xóa hoặc đổi quyền. Các ca storage dưới `/tmp` bị `Codex home is inside a repository`; hai ca dùng `/var/tmp` còn bị read-only. Không giả lập điều kiện `/tmp/.git` vắng. Base chạy cùng môi trường để phân biệt lỗi nền; kết quả gate đầy đủ không được gọi là xanh.

## Đối chiếu findings các lượt trước

| Nguồn/lớp | Đo lại trên HEAD | Kết luận |
|---|---|---|
| Lượt 1 F01 tên lớp/stdout; lượt 2 F01 cùng qualname | `probe_oracles.py`: RuntimeError/AssertionError giả cùng qualname đều `loi`; stdout giả thiếu kênh → `loi`; nonce sai bị khóa | Đã vá biểu hiện cũ |
| Lượt 1 F02 bước dò Bash | `probe_fixture.py`: cả hai probe Bash và hook đều HOME tạm, BASH_ENV/ENV null, không BASH_FUNC; 0 init/installer | Đã vá |
| Lượt 1 F03 khóa credential chỉ tìm chuỗi | `probe_oracles.py`, `probe_registered_mutations.py`: gọi chay_suite thật, mutant giữ comment vẫn RIGHT_SIGNAL | Đã vá |
| Lượt 2 F04 kênh trước main | `audit_debt_history.py`: `DEBT1117_RECEIVER_RUNTIME_UNCHANGED True` | Nợ #1117 theo authority; không chặn lại |
| Lượt 2 F05 assertion ca khác | Ca khác code riêng bị loại; `probe_shared_call.py` cho cùng factory bị nhận ở a/b/c | **Mở lại bởi bản vá F08**, cùng slug F05 |
| Lượt 2 F06 thiếu/trùng target | `probe_oracles.py`: missing/partial/duplicate đều `(1,0)` | Đã vá |
| Lượt 2 F07 khóa neutral | `probe_oracles.py`, `audit_debt_history.py`: khóa PASS trên HEAD; bỏ thực thi giữ literal → RIGHT_SIGNAL; runner neutral đỏ `(1,0)` | Đã vá |
| Lượt 3 F08 own assertion cùng factory | `probe_alias.py`: chỉ target chạy, a/b `(0,0)`, c nhận đúng `review_target`; ba khóa nhận từ HINT lượt 3 PASS | Đã vá **biểu hiện chặn nhầm cũ**; lớp nguồn gốc ca chưa đóng vì hồi quy F05 |

Không đổi slug để giấu tái diễn. Lớp `F05-assertion-ca-khac-bi-ghi-thanh-ca-dich` có ba biểu hiện a/b/c, cùng nguyên nhân và cùng cách sửa; tính là một finding, không ba. Lớp sai số lịch sử F09 độc lập.

## BANG NGHIEM THU

| Tiêu chí | Lệnh chạy được từ cay-kho | Output thật | Đạt? |
|---|---|---|---|
| M1: a chỉ tín hiệu target, lỗi vô can là tín dụng giả, giữ skip | `python3 -B ../review4/probe_oracles.py`; `python3 -B ../review4/probe_shared_call.py` | attr/bare/wrapped → loi và runner SAI; own/helper → giet; same-factory other → `OK giet 1/1` | Kiểu lỗi đạt; **đúng ca không đạt: F05** |
| M2: neutral a/b trước mutant, cache, đỏ làm cổng đỏ | `python3 -B ../review4/probe_skips_and_b.py`; `python3 -B ../review4/probe_oracles.py` | a/b neutral error/chốt `(1,0)`, thông báo neutral do; hai mutant cùng target chỉ neutral 1 lần; a dùng LAUNCHER gốc, b dùng harness_goc | Đạt phần đo được |
| M3: b dùng tín hiệu đúng target, không lấy rc/headline làm nguyên nhân | `python3 -B ../review4/probe_oracles.py`; `python3 -B ../review4/probe_shared_call.py` | stdout giả → loi; khác qualname → loi; nhưng other cùng factory → `OK giet 1/1` | **Không: F05** |
| M4: c kiểm loại và bare assert đúng tệp; wrapped không giả được | `python3 -B ../review4/probe_oracles.py`; `python3 -B ../review4/probe_credential_mutants.py` | t2 bare assert thật nhận; implementation/wrapped có suffix loại; tệp khác cùng dòng bị loại; 13 mutant đo được RIGHT_ASSERTION | Đạt lọc kiểu/tệp; nguồn đúng ca còn F05/M7 |
| M5: 11 mutant SPEC chết bằng chốt ca | `python3 -B ../review4/probe_base.py` | Ca HEAD: 10 OK bằng `giet`; `g2_rejected_refresh_khong_phu_thuoc_metadata` neutral OSError | 10 đạt; 1 **KHÔNG ĐO ĐƯỢC** storage |
| M6: N13 cô lập rg/actionlint/installer/HOME/init, giữ thứ tự npm | `python3 -B ../review4/probe_fixture.py`; `python3 -B ../review4/probe_fixture_base_lock.py` | Base 7 installer/2 init; HEAD 0/0; nhật ký NPM codex → NPM claude → chuan-bi → doctor | Đạt |
| M7: khóa a/b/c và mutant đúng ca, không chặn nhầm kill thật | `python3 -B ../review4/probe_registered_mutations.py`; `python3 -B ../review4/probe_alias.py`; `python3 -B ../review4/probe_shared_call.py` | 18 khóa PASS, 23 mutant/27 target RIGHT_SIGNAL; own cùng factory được nhận, nhưng other cùng factory cũng được nhận | **Không: F05**; thiếu đối chứng âm bổ sung |
| A1: N/N, M/M, credential ĐẠT khi /tmp/.git vắng | `python3 -B ../review4/run_suites.py` | HEAD launcher 315/338, mutation 509/545, credential nền 13/18; base cùng điều kiện đối chiếu ở BANG TEST | **KHÔNG ĐO ĐƯỢC đúng tiền đề**; không approve từ số này |
| A2: scorer mới trên ca base; khóa đỏ với scorer/fixture base | `python3 -B ../review4/probe_base.py`; `python3 -B ../review4/probe_legacy_runners.py`; `python3 -B ../review4/probe_fixture_base_lock.py` | 397 OK, 34 neutral đỏ, 11 SAI, 1 all-skip; base runner thật cấp tín dụng AttributeError ở a/b, HEAD loại; khóa a/neutral/c RIGHT_SIGNAL; N13 base+hậu điều mới RIGHT_SIGNAL | Đạt phản chứng đo được; **không xác nhận đúng toàn bộ 11 tên SPEC** trong tiền đề chuẩn |
| A3: A/B installer ngoài npm giả | `python3 -B ../review4/probe_fixture.py` | 7 → 0 installer; 2 → 0 init; outer HEAD `[]` | Đạt |
| A4: Ruff F delta 0, diff-check, doctrine, CI head cuối | `ruff check --no-cache --select F --output-format json .claude/dev/launcher_test.py .claude/dev/codex_cred_test.py`; `git diff --check 7eeb1d9a10aea8e1805b66fbf3d68549eb6778da HEAD -- .claude`; `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .` | Ruff 5 F841 cả base/HEAD; delta0. Diff scope rc0; doctrine rc0 (10 tệp,0 chỗ). Toàn diff rc2 lỗi từ master. CI cấm mạng | Local packet đạt; CI **KHÔNG ĐO ĐƯỢC** |

A2: scorer HEAD chạy trên **443 mutant product của base** sau loại 3 giới hạn Windows. Trong 11 SAI có **10/11 tên SPEC**, cộng `PROMPT_FILE_mo_coi_di_tiep` vì r13 base gọi t70 đã đăng ký. Tên SPEC còn lại `g2_rejected_refresh_khong_phu_thuoc_metadata` chuyển sang neutral đỏ vì storage; cộng 33 neutral đỏ khác và 1 all-skip. Không lấy số 11 tổng để khẳng định “đúng 11 tên”. Trên HEAD, r13/t70 dùng helper riêng: đo mỗi ca đều kill thật `OK giet 1/1`. Từng neutral/mutant ở [base-strict.json](review4/base-strict.json).

## BANG DO

| Khẳng định | Diff khai | Đo được (lệnh/script từ cay-kho) | Khớp? |
|---|---|---|---|
| Ca khác bị loại; “Loi goi THAT ... (F05) van bi loai” | launcher:165–175; credential:579–591; message 5368c34/5548919 | `probe_shared_call.py`: previous a/b `(1,0)`, HEAD `(0,0)`; credential previous có suffix, HEAD không | **Sai — F05**, không chỉ thiếu bằng chứng |
| Ca cùng factory có thể chung __code__; target tự assert không phải ca khác | Hai hunk F08 và ba ca HINT lượt 3 | `probe_alias.py`: shared_code True; calls chỉ target 2 lần; cả ba đường nhận own kill | Khớp đối chứng này |
| AssertionError trần/AttributeError/kể cả except đổi kiểu bị từ chối | cham_mot_ca; la_chot_cua_suite; chay_suite | `probe_oracles.py`: loi hoặc suffix AssertionError/AttributeError; actual runner a/b SAI | Khớp |
| Khác lớp cùng __qualname__ không giả tín hiệu | Reporter khac:, message sửa F01 | `probe_oracles.py`: lớp RuntimeError/AssertionError giả đều loi; mutant bỏ phân biệt đỏ đúng ca | Khớp |
| Neutral đỏ không được tín dụng, mỗi target một lần, bản nguyên | Hai cache/ket_luan_mutant; F07 message/khóa | `probe_oracles.py`, `probe_skips_and_b.py`: cache1/mutant2; neutral error/chốt `(1,0)`; meta-lock giữ literal RIGHT_SIGNAL | Khớp |
| Ca bỏ qua giữ luật cũ, missing/trùng không tự rơi mẫu số | ket_luan_mutant/F06 | `probe_skips_and_b.py`: base/HEAD all-skip `(0,1)`, mixed `(0,0)`; missing/partial/duplicate `(1,0)` | Khớp |
| 3 ca đổi assert; r01/r10 có chốt run.json; t115 kiểm hợp đồng trả kết quả | Các hunk M5 | `probe_base.py`: 10/11 mutant HEAD neutral xanh → giet, trước đó là bare/FileNotFound/JSON/type error | Khớp phần đo được; recovery storage chưa đo được |
| r13/t70 dùng helper; mỏ neo AssertionError đã sửa | Message 7df242e, _t70_prompt_file_chan | `probe_oracles.py`: cả hai OK riêng; `audit_debt_history.py`: 5548919 kill1/2, neo count0; HEAD t117 PASS và mutant RIGHT_SIGNAL | Khớp hiện tại; số541/543 lịch sử chưa đo lại trong môi trường gốc |
| N13 không chạm installer/init/HOME cha; npm trước materialize | Fixture/comment M6; message ee23c44 | `probe_fixture.py`: outer[], 0/0, cả 3 child HOME fixture, không init/hàm cha; thứ tự log đúng; gỡ từng shim/scrub RIGHT_SIGNAL | Khớp phạm vi hook hiện tại |
| Credential đúng lớp/tệp/dòng assert; chay_suite thật dùng ten_do | la_chot_cua_suite/ten_do; message ee23c44 | `probe_oracles.py`, `probe_registered_mutations.py`: same-line other-file bị loại; mutant giữ comment đỏ đúng chốt; 13 target đo được RIGHT_ASSERTION | Khớp lọc loại/tệp; không chứng minh đúng ca chung factory |
| Harness dùng kênh riêng và gỡ env trước ca, stdout không là bằng chứng | cham_lap_ca/main/reporter | `probe_oracles.py`: stdout → thiếu kênh/loi; env_removed → qua; khóa nonce PASS | Khớp bảo đảm đã thu hẹp; #1117 giữ nguyên |
| Mỗi chốt mới có mutant đúng target | Bảng wp1079; message cuối “2 dot bien moi ... OK” | `probe_registered_mutations.py`: **23 mutant,27 target,27 RIGHT_SIGNAL**; F08 hai mutant mới có 3 target đúng | Khớp các mutant đã đăng ký; không đủ chứng minh đầy đủ nguồn gốc F05 |
| “5 dot bien moi” ở 5548919 | Toàn %B commit5548919 | `claim_history.py`: ADDED_MUTANTS có **4** tên, CHANGED_MUTANTS có3; diff-tree đối chiếu cha trực tiếp | **Không — F09** |
| WIP +356 | Message d8f8998 | `git diff --numstat BASE d8f8998 -- .claude`: 36+320 dòng thêm | Khớp; không suy thành vượt trần hiện tại |
| Đã nhận4 HINT lượt1,6/7 lượt2,3 lượt3; hash hint1/3 | Các message hint_provenance | `inventory_commits.py`: HINT1_LOCAL/HINT3_LOCAL True; 4/6/3 ca hiện diện và chạy; `audit_debt_history.py` tái hiện6 phản chứng trên d929ee2 | Khớp byte/tên/phản chứng đo được; không tự chứng minh ai đã viết hay nhận hint |
| Các số531/536,538/539,541/543,10/10 và “codex_cred_test DAT” trên máy executor | Message các SHA trước/cuối | Git xác nhận source/neo; suite HEAD đo nền13/18, base cũng13/18. Không có môi trường/log executor độc lập | **KHÔNG ĐO ĐƯỢC lịch sử**; không lấy đỏ sandbox làm lời khai sai |
| CI/review/land/spec/hash/authority trong25 commit master/merge | Toàn git log BASE..HEAD | `inventory_commits.py` liệt kê32 body đầy đủ; `audit.py`: ngoài .claude bằng master767a68d^2; không gọi check-run | Nguồn kế thừa khớp; lịch sử CI/authority **KHÔNG ĐO ĐƯỢC**, ngoài scope packet |
| Không sửa launcher sản phẩm, hook, workflow hay cây executor | Scope diff và yêu cầu review | `audit.py`: đúng2 tệp, numstat704 dòng thêm; `verify_tree.py` kiểm blob cuối | Xác nhận ở kiểm toàn vẹn cuối |

`git diff --check BASE HEAD` thật sự rc2 tại `ops/specs/launcher-sandbox-lay-mau-r2.md:242: new blank line at EOF.` `git diff --check BASE 767a68d^2` cùng rc2 và cùng output; ngoài `.claude` HEAD bằng master ấy. Không gán lỗi master này cho packet, cũng không khai toàn diff sạch. [diff-checks.json](review4/diff-checks.json) lưu cả ba lệnh/rc/output.

## BANG TEST

| Bộ/lệnh thực chạy | N/M và rc | Bỏ qua / giới hạn |
|---|---|---|
| HEAD `python3 .claude/dev/launcher_test.py` | **315/338** đã chạy qua; tổng348, lỗi23; rc1 | **10 BO QUA**: 1 fixture Windows,8 venv/pip offline,1 SID Windows |
| BASE cùng lệnh, cùng env | **297/320**; tổng330, lỗi23; rc1 | 10 BO QUA; tập tên lỗi và tên/lý do bỏ qua **trùng HEAD** |
| HEAD `python3 .claude/dev/launcher_test.py --dot-bien` | **509/545**; rc1 | 4 không đo theo nền;36 SAI đều neutral đỏ |
| BASE cùng lệnh | **522/522**, rc0;4 không đo theo nền | Không đọc headline scorer cũ thành bằng chứng neutral xanh |
| HEAD `python3 .claude/dev/codex_cred_test.py` | Nền **13/18**, `TỔNG: ĐỎ`; rc1 | 5 ca đỏ, không là skip; dừng trước mutation |
| BASE cùng lệnh | Nền **13/18**, `TỔNG: ĐỎ`; rc1 | Cùng5 tên (HEAD thêm suffix loại lỗi) |
| Credential đo riêng từng mutant với neutral target | **13/13 RIGHT_ASSERTION** đo được | 5/18 KHÔNG ĐO NEUTRAL; không thay thế gate chính thức |
| Khóa #1079 trên HEAD | **18/18 PASS** | Log probe_oracles.log |
| Mutant #1079 trên bản sao | **23/23**, **27/27 target RIGHT_SIGNAL** | Có kiểm nguồn không từ ca đăng ký khác |
| Scorer HEAD trên ca product BASE | **397 OK/443** xét theo giới hạn nền |11 SAI,34 neutral đỏ,1 all-skip;3 Windows loại trước |
| 11 mutant SPEC trên ca HEAD | **10 OK**,1 neutral đỏ | Recovery storage KHÔNG ĐO ĐƯỢC |
| F08 own chung factory | a/b `(0,0)`; c `{review_target}` | Only target called; không chặn nhầm phản chứng cũ |
| F05 gọi thật ca khác chung factory | a/b `(0,0)`; c `{review_target}` | **Cấp tín dụng giả**; previous7df242e loại cả3 |
| HINT mới | **3/3 RIGHT_SIGNAL**, dry-run rc0 | Chỉ trên bản sao; không áp cây thật |
| Ruff F / doctrine / diff-check scope | 5→5 delta0 / rc0 / rc0 | Ruff cả2 rc1 do5 F841 nền; CI chưa đo |

Credential5 ca đỏ: t6,t9,t15,t16,t18; log [head-credential.out](review4/head-credential.out) và [probe_credential_mutants.log](review4/probe_credential_mutants.log). Các ca này không được báo bỏ qua, cũng không được đưa vào13 kill dương.

## BANG SAN

| Hướng độc lập | Lệnh từ cay-kho | Output thật | Phân loại |
|---|---|---|---|
| 1. AttributeError qua except đổi sang AssertionError | `python3 -B ../review4/probe_oracles.py` | a wrapped loi; b khac:AssertionError; c target(AssertionError); runner a `(1,0)` | KHÔNG PHẢI LỖI |
| 2. AssertionError trực tiếp từ triển khai | Cùng lệnh | a bare loi; b khac:AssertionError; c suffix AssertionError | KHÔNG PHẢI LỖI |
| 3. Lớp khác trùng __qualname__ tín hiệu | Cùng lệnh | same_runtime/same_assert đều loi, không kill | KHÔNG PHẢI LỖI |
| 4. Assertion ca khác code riêng | Cùng lệnh | a/b loi; c `(chot cua ca khac)` | KHÔNG PHẢI LỖI với code riêng |
| 5. Neutral đỏ do lỗi hoặc chốt | `python3 -B ../review4/probe_skips_and_b.py`; `python3 -B ../review4/probe_oracles.py` | a/b `(1,0)`, SAI KHONG DO DUOC(neutral do) | KHÔNG PHẢI LỖI |
| 6. Toàn skip và mixed | `python3 -B ../review4/probe_skips_and_b.py` | base/HEAD all `(0,1)`, mixed `(0,0)`; b cũng vậy | KHÔNG PHẢI LỖI |
| 7. Child in LOAI_HONG/headline giả rồi exit | `python3 -B ../review4/probe_oracles.py` | neutral qua; mutant loi(khong co ket qua kenh,rc1) | KHÔNG PHẢI LỖI |
| 8. Tệp khác có assert cùng số dòng | Cùng lệnh; `python3 -B ../review4/probe_registered_mutations.py` | khóa PASS; mutant bỏ kiểm tệp RIGHT_SIGNAL | KHÔNG PHẢI LỖI |
| 9. Missing/partial/duplicate targets | `python3 -B ../review4/probe_oracles.py` | Cả3 `(1,0)` | KHÔNG PHẢI LỖI |
| 10. Giữ literal neutral nhưng bỏ thực thi | Cùng lệnh; `python3 -B ../review4/audit_debt_history.py` | Meta-lock PASS; test cũ trên scorer trước vá RIGHT_SIGNAL | KHÔNG PHẢI LỖI |
| 11. Cache neutral / bản nguyên | `python3 -B ../review4/probe_skips_and_b.py`; `python3 -B ../review4/probe_oracles.py` | neutral1/mutant2 ở a/b; harness_goc được dùng | KHÔNG PHẢI LỖI |
| 12. PATH/rg hỏng/installer log/init/HOME/hàm Bash cha | `python3 -B ../review4/probe_fixture.py` | base PASS dù7 installer/2 init; HEAD PASS0/0, OUTER[] | KHÔNG PHẢI LỖI HEAD |
| 13. Gỡ từng chốt và dùng fixture base | `python3 -B ../review4/probe_registered_mutations.py`; `python3 -B ../review4/probe_fixture_base_lock.py` |27/27 RIGHT_SIGNAL; N13 base+hậu điều mới RIGHT_SIGNAL,7 AMBIENT | KHÔNG PHẢI LỖI với các mutant đo |
| 14. Kill thật helper r13/t70 | `python3 -B ../review4/probe_oracles.py` | Hai ca riêng `OK giet1/1`, `(0,0)` | KHÔNG PHẢI LỖI |
| 15. Factory: chỉ target chạy, alias không chạy | `python3 -B ../review4/probe_alias.py` | a/b `(0,0)`; c đúng tên; calls target,target | KHÔNG PHẢI LỖI; F08 cũ đóng |
| 16. Factory: target GỌI THẬT registered other | `python3 -B ../review4/probe_shared_call.py` | HEAD a/b OK; c nhận target; calls target,target,other. Previous loại cả3 | **LỖI — F05/P1 mở lại** |
| 17. Đếm mutant theo cha Git, không đếm lời khai | `python3 -B ../review4/claim_history.py` |5548919 ADDED_MUTANTS4; message5; current tổng23 | **LỖI — F09/P1 lời khai số sai** |
| 18. Toàn suite và CI đúng tiền đề | `python3 -B ../review4/run_suites.py`; `ls -ld /tmp/.git` | HEAD23 lỗi launcher/5 credential; /tmp/.git chỉ đọc; không gọi mạng | **KHÔNG ĐO ĐƯỢC** A1 chuẩn và CI |

### F05-assertion-ca-khac-bi-ghi-thanh-ca-dich [P1] Bản vá F08 nhận lại assertion của ca khác nếu dùng chung factory

TEP/DONG: `.claude/dev/launcher_test.py:169` trừ `{fn.__code__}` khỏi tập nguồn bị loại; `cham_mot_ca:185` dùng kết quả, reporter harness dùng cùng helper. `.claude/dev/codex_cred_test.py:585` trừ `{ca.__code__}`, `ten_do:588` mất khả năng nhận ca khác. Thông điệp `5368c34` cũng khẳng định sai “Loi goi THAT ... (F05) van bi loai”.

VAN DE: Nếu hai callable đăng ký từ cùng factory, chúng khác identity nhưng có cùng code object. Sau phép trừ, code của **cả target lẫn other** biến mất khỏi `khac`. Target gọi thật sang other, other ném chốt của chính nó, traceback có cả hai lần gọi nhưng helper không còn phần tử nào để nhận ra ca other. a/b gắn kill vào tên target; c trả tập đỏ đúng tên target. Neutral target vẫn xanh. Đây là cấp tín dụng giả, không phải biểu hiện chặn nhầm F08 còn nguyên.

DA THU NGHIEM: `python3 -B ../review4/probe_shared_call.py`, ghi [probe-shared-call.log](review4/probe-shared-call.log). Cùng phản chứng trên `7df242e` và HEAD, qua runner thật ở a/b và chay_suite thật ở c:

```text
previous PRODUCT_OTHER_FACTORY (1, 0) calls ['review_target','review_target','review_other'] shared_code True
previous HARNESS_OTHER_FACTORY (1, 0)
previous CREDENTIAL_OTHER_FACTORY [[], ['review_target(chot cua ca khac)']]
head PRODUCT_OTHER_FACTORY (0, 0) calls ['review_target','review_target','review_other'] shared_code True
head HARNESS_OTHER_FACTORY (0, 0)
head CREDENTIAL_OTHER_FACTORY [[], ['review_target']]
```

Child thực sự in `CALLED review_target`, `CALLED review_other`, rồi HONG vì assertion chỉ ở other. Không giả stdout/kênh/nonce, không đổi lớp tín hiệu, không spoof filename/traceback. Đột biến là đổi cờ trơ hoặc comment trên bản sao; target chỉ gọi other khi mutant. Đối chứng không gọi other (`probe_alias.py`) nhận own assertion đúng cả3; code riêng vẫn loại other. AST/runtime hiện chưa có nhóm registered CA dùng chung code trong348/18 ca có sẵn; không khai full suite hiện có đã nhận kill giả vì cấu trúc này. Đây là phản chứng hành vi bộ chấm trên loại ca hợp lệ, được PROMPT yêu cầu thử trực tiếp.

DO TIN: cao, cả ba đường và A/B exact OID. P1 do sai hành vi có neutral xanh. Cùng slug F05 lượt2; bản vá F08 tạo hồi quy mới từ trạng thái lượt3 đã chặn đối chứng này.

Gợi ý vá: sửa hai helper nguồn gốc và đường reporter cùng một thiết kế. Chỉ code object không đủ làm identity. Ghi nhận identity ca thật khi vào/ra callable đăng ký (ví dụ wrapper ở ranh giới đăng ký/chạy, đánh dấu nguồn chốt) để phân biệt hai lần thực thi của cùng code; vẫn cho phép helper không đăng ký. Không hoàn nguyên đơn giản phép trừ vì sẽ mở lại chặn nhầm F08. Giữ bốn đối chứng: own cùng factory/không gọi alias được nhận; gọi registered other cùng factory bị loại; other code riêng bị loại; helper r13/t70 vẫn được nhận. Đồng thời giữ neutral/cache/skip/missing-target.

[HINT.patch](HINT.patch) thêm ba ca `r1079_review4_{product,harness,credential}_shared_template_call_other`. `make_hint.py` đã chạy trên bản sao HEAD: **3/3 đỏ bằng TinHieuChotCa của chính ca hồi quy**, thông điệp đều chỉ rõ cấp tín dụng other chung code. Không lấy lỗi thiếu fixture làm bằng chứng: bản sao credential được bổ sung đúng tệp suite trước khi đo. Không cung cấp runtime fix chưa đo; hướng sửa trên là bằng lời, executor tự dẫn xuất. Sau sửa ba ca phải xanh, gỡ cơ chế provenance mới phải làm chúng đỏ lại đúng nguyên nhân.

### F09-commit-dem-sai-so-dot-bien-moi [P1] Commit 5548919 khai 5 mutant mới nhưng chỉ thêm 4

TEP/DONG: `%B` của commit `55489195d303013333a2302a2652ae62164fdc94`, đoạn “5 dot bien moi”. Nội dung gắn với bảng mutant ở hai tệp trong scope; xem [claim-history.log](review4/claim-history.log).

VAN DE: Lời khai ghi5 nhưng ngay danh sách chỉ nêu4 tên. So bảng AST giữa commit và cha trực tiếp xác nhận đúng4 tên mới;3 hàng khác là sửa nội dung đã có, không có tên mới thứ5. Không phải số dòng thêm/trần review đã được miễn; cũng không phải khác biệt môi trường. Đây là khẳng định số lượng sai đo được; P1 áp đúng định nghĩa PROMPT, không suy rằng bộ chạy hiện tại có thêm lỗi hành vi từ sai số này.

DA THU NGHIEM: `python3 -B ../review4/claim_history.py` →

```text
5548919 ADDED_MUTANTS ['wp1079_bo_kiem_ca_dich_vang', 'wp1079_bo_kiem_ca_khac',
'wp1079_bo_tien_to_khac', 'wp1079_cc_bo_kiem_ca_khac']
CHANGED_MUTANTS ['wp1079_bao_cao_theo_ten_lop', 'wp1079_cc_chay_suite_bo_ten_do',
'wp1079_cc_ten_do_bo_loai']
```

`git show -s --format=%B 5548919` xác nhận nguyên văn “5 dot bien moi”; kiểm AST ba bảng độc lập với dòng in hoặc số mutant PASS. Commit cuối thêm đúng2 tên và bảng hiện tại có23 mutant wp1079; không khai sai số lịch sử làm mất tên trong HEAD.

DO TIN: cao, phép set-difference tên theo object Git. Gợi ý: ghi correction bền trong handoff rằng `5548919` thêm4 tên mới và sửa3 hàng đã có, cùng lệnh/OID đối chứng; không cần đổi logic scorer hoặc sửa commit cũ chỉ để làm biến mất lịch sử. HINT runtime chỉ dành F05; F09 là đính chính lời khai, không tạo chốt runtime giả để canh văn bản commit.

## HINT và kiểm toàn vẹn cuối

`patch --dry-run -p0 -d cay-kho < HINT.patch` → rc0, `checking file .claude/dev/launcher_test.py`. **Chưa áp/chạy trên cây thật; executor tự dẫn xuất, tự đo, tự chịu trách nhiệm commit/hint_provenance.** SHA-256 HINT: `1fb51923063ac20b9fbad4d63a892b5d45dee329006dc18fab434bb7edb2af07`.

`python3 -B ../review4/verify_tree.py` so **10.161 blob theo HEAD**: `changed=[]`, `git_status=""`, HEAD/tree vẫn đúng OID ở đầu verdict. Ba tệp `.cmd` có CRLF, nội dung chuẩn hóa khớp Git và thuộc tính EOL. Bằng chứng: [final-integrity.json](review4/final-integrity.json).

`python3 -B ../review4/summarize.py` → `LAUNCHER_FAIL_SETS_EQUAL True`, `LAUNCHER_SKIP_SETS_EQUAL True`, `HEAD_MUTANT_RED_COUNT 36 ALL_NEUTRAL_RED True`, `NEW_MUTANTS 23`. [summary.log](review4/summary.log), [summary.json](review4/summary.json) và sáu bộ `*-*.out/.err/.json` lưu lệnh, rc, thời gian và output nguyên. Launcher base/HEAD cùng23 tên lỗi và10 skip; credential cùng5 tên đỏ. Đây là đối chứng nền trong sandbox, không thay thế gate A1/CI trên môi trường đúng tiền đề.

Mọi script đo và HINT mới ở ngoài `cay-kho/`. Không có phát sinh `.pyc` hoặc sửa cây executor.

Đây là lời gọi4/4 cuối theo PROMPT. Không yêu cầu thêm vòng review, không tự gia hạn lease, không coi nợ #1117 hoặc giới hạn sandbox là finding mới.
