verdict: changes_requested
reviewed_sha: c73dff39c0d50622ab26812ee88476ef884aa8fb
spec_sha256: 81070fa2c5a00bc0bb63867c7173f310cba9002001b68a26d62726ec904cbf5b
Ket qua: 0 P0, 2 P1, 1 P2, 0 P3.

Cần sửa F01 (harness vẫn cấp tín dụng giả), F02 (N13 chưa cô lập bước dò Bash) và F03 (ca khóa credential chỉ kiểm văn bản tại điểm nối). Các thất bại do môi trường được ghi riêng, không tính thành finding của packet.

provider: openai_codex
model_family: openai
execution_surface: codex_service
transport: machine
exact_model_id: runtime không cung cấp định danh endpoint để kiểm chứng độc lập
reviewer_role: reviewer độc lập với executor Claude; không dùng context executor
review_axes: spec, standards_security
reviewed_tree: b9d3458c612968fec3b326da640829c6a58a0aec
packet_id: wp1079
revision: r1
generation: 2
lease: wp1079-r1-g2-claude
review_class: sensitive
review_call: 1/2

Đã đọc PROMPT, SPEC đóng băng, hai mục nguồn F01/F02, diff và toàn bộ thông điệp hai commit trong phạm vi 7eeb1d9a10aea8e1805b66fbf3d68549eb6778da..HEAD. Không sửa `cay-kho/`, không push, không dùng credential thật, không gọi web/GitHub API. Các phép đo chạy cục bộ trong sandbox không có mạng. Những ca suite cần dựng venv/pip tự bỏ qua; không coi chúng là đã kiểm được. Các bản sao, script và log ở `evidence/`, ngoài cây được review. Trần dòng thêm 380 đã được chủ kho cho phép, không phải finding.

## Cách chạy lại và giới hạn môi trường

Các lệnh suite dưới đây chạy từ `cay-kho/`. Bỏ các biến `CODEX_AUTH_JSON`, `CODEX_HOME`, `TL_CODEX_SNAPSHOT`, `OPENAI_API_KEY`, `GH_TOKEN`, `GITHUB_TOKEN`, `GITHUB_PAT`; đặt `PYTHONDONTWRITEBYTECODE=1`, dùng HOME tạm **tuyệt đối, đã chuẩn hóa**. Khi chạy lại offline có thể thêm `PIP_NO_INDEX=1 PIP_DISABLE_PIP_VERSION_CHECK=1`. Các script `../evidence/*.py` tự tìm dữ liệu theo vị trí script, nên chạy được cả từ `cay-kho/` lẫn thư mục chứa verdict. Archive `evidence/head/` khớp exact HEAD; `evidence/base/` lấy bằng `git archive` từ exact BASE, không lấy master hiện hành.

Lệnh kiểm bẫy: `ls -ld /tmp/.git`; output thật: thư mục tồn tại, mode `dr-xr-xr-x`. Backend từ chối home dưới `/tmp` bằng `Codex home is inside a repository`. Hai ca chọn `/var/tmp` còn gặp `OSError: [Errno 30] Read-only file system`. Không xóa `.git`, không ghi ra `/var/tmp` hay `/dev/shm` để né sandbox. Base được đo cùng điều kiện. A1 với tiền đề `/tmp/.git` vắng và CI check-run trên GitHub vì vậy ghi **KHÔNG ĐO ĐƯỢC**, không đọc thành hồi quy.

Lượt HEAD đầu có HOME chứa `..`, tạo thêm lý do chặn đường dẫn trong log. Đã loại lượt đó khỏi kết luận chính, lưu `*-initial.log`, và chạy lại cả hai suite launcher với HOME chuẩn hóa. Số lỗi giữ nguyên; đối chiếu theo tên ca và neutral được lưu riêng.

## BANG NGHIEM THU

| Tiêu chí | Lệnh chạy được | Output/bằng chứng thật | Đạt? |
|---|---|---|---|
| M1: product chỉ nhận tín hiệu suite; giữ bỏ qua | `python3 -B ../evidence/probe_oracles.py`; `python3 -B ../evidence/probe_neutral_runner.py` | `bare`, `unrelated`, `wrapped` → `loi`; assertion đích → `giet`; runner converted AssertionError → `SAI`, accounting `(1,0)` | ĐẠT phần đo được |
| M2: neutral trước mutant, đỏ làm cổng đỏ | `python3 -B ../evidence/probe_neutral_runner.py`; `python3 .claude/dev/launcher_test.py --dot-bien` | Product neutral error/assertion → `(1,0)`; harness neutral AttributeError → `(1,0)`; lượt product có gọi neutral trước mutant; hai mutant cùng đích: neutral=1, mutant=2. Full suite không cho 36 neutral đỏ nhận tín dụng | ĐẠT; ca khóa điểm nối còn giới hạn kiểm văn bản |
| M3: harness chỉ nhận đúng TinHieuChotCa | `python3 -B ../evidence/probe_runner_spoof.py` | `review_same-name OK giet 1/1`, `review_fake-suffix OK giet 1/1`; cả hai accounting `(0,0)` dù không có assertion của suite | **KHÔNG — F01/P1** |
| M4: credential phân biệt assertion suite và lỗi khác | `python3 -B ../evidence/probe_oracles.py`; `python3 -B ../evidence/probe_cred_measured.py` | AssertionError triển khai/đổi kiểu/tệp khác → không phải chốt; 13/13 mutant đo được chết đúng assertion suite; 5 neutral không xanh | ĐẠT trong phạm vi đo được; không xác nhận 5 ca bị môi trường chặn |
| M5: phục hồi 11 mutant nguồn bằng chốt đích | `python3 -B ../evidence/probe_11.py` | HEAD: 10 OK bằng TinHieuChotCa, 1 KHONG_DO_NEUTRAL/OSError; base: 10 SAI đúng các loại cũ, cùng 1 neutral lỗi | ĐẠT 10/10 đo được; **KHÔNG ĐO ĐƯỢC 1/11**, không khai 11/11 |
| M6: fixture N13 kín với installer, init shell, HOME cha | `python3 -B ../evidence/probe_fixture.py`; `python3 -B ../evidence/validate_hint.py` | Installer base=7, HEAD=0; NPM trước chuan-bi. Tuy nhiên HEAD PASS với **2 BASH_ENV** chạy dưới HOME cha trong tim_bash | **KHÔNG — F02/P1** |
| M7: ca khóa và mutant đúng ca/đúng lý do | `python3 -B ../evidence/probe_new_mutations.py`; `python3 -B ../evidence/probe_cc_wiring.py` | 14/14 mutant đăng ký chết đúng TinHieuChotCa ca đích; mutant đổi `do.add` nhưng giữ lời gọi cũ trong comment **SURVIVED**, rồi cấp tín dụng cho AttributeError | **KHÔNG đủ — F03/P2**, đồng thời thiếu hai phản chứng F01 |
| A1: ba suite xanh khi /tmp/.git vắng | Ba lệnh suite ở BANG TEST; `ls -ld /tmp/.git` | Tiền đề không thỏa. HEAD/base cùng 23 lỗi launcher; credential cùng 13/18. Đột biến HEAD 500/536, 4 bỏ qua nền, 36 neutral đỏ | **KHÔNG ĐO ĐƯỢC** điều kiện nghiệm thu; không quy thành hồi quy |
| A2: grader mới trên ca base; ca khóa đỏ khi bỏ chốt; N13 mới đỏ với fixture base | `python3 -B ../evidence/build_counterfactual.py`; `python3 -B ../evidence/counterfactual/.claude/dev/launcher_test.py --dot-bien`; `python3 -B ../evidence/probe_base_fixture_lock.py`; script M7 | Counterfactual giữ CA/fixture/bảng base, chỉ chuyển grader và reporter HEAD. Kết quả đầy đủ ở BANG TEST; đúng 10 SAI không do neutral thuộc danh sách 11, mục thứ 11 bị /tmp/.git. Base fixture + hậu điều N13 mới → TinHieuChotCa sau 7 shim installer | ĐẠT phản chứng đo được; số đúng 11 SAI dưới nền sạch **KHÔNG ĐO ĐƯỢC** |
| A3: 0 installer ngoài npm; A/B base > 0 | `python3 -B ../evidence/probe_fixture.py` | `base INSTALLERS 7`; `head INSTALLERS 0`; cả hai nguyên ca PASS. Log riêng phân biệt INSTALL và BASH_ENV | ĐẠT phép đo installer; không suy thành cô lập toàn ca |
| A4: ruff delta, diff-check, doctrine, CI exact head | `python3 -B ../evidence/audit_static.py`; `git diff --check 7eeb1d9a10aea8e1805b66fbf3d68549eb6778da HEAD`; `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | Ruff 0.16.8: F 5→5, delta=0; diff-check rc=0; doctrine rc=0, quét 10 tệp/0 chỗ. Không có check-run offline cho exact HEAD | ĐẠT ba cổng cục bộ; CI **KHÔNG ĐO ĐƯỢC** do cấm mạng/không có hiện vật check-run |

## BANG DO

Cách tìm lời khai: không chỉ tìm số hay tên hàm. `python3 -B evidence/inventory_claims.py` duyệt **mọi dòng thêm và xóa** trong unified diff, giữ phía old/new, đường dẫn, số dòng và chủ thể AST; đọc cả comment/docstring lẫn câu lệnh. Có **490 dòng đổi = 374 thêm + 116 xóa**, gồm dòng trắng; bảng toàn bộ ở `evidence/diff-claims-all-lines.tsv`. `audit_static.py` còn lập `diff-additions.tsv`: 345 dòng thêm không trắng, 145 dòng chứa chữ số. Sau đó đọc `git log --format=%B 7eeb1d9a10aea8e1805b66fbf3d68549eb6778da..HEAD`, lưu nguyên văn ở `evidence/commits.txt`. Bảng dưới gom theo hành vi để tránh nhắc 490 dòng riêng rẽ; không gán nhãn “đã đo hết” cho lịch sử, Windows hay những nhánh neutral bị chặn. Việc gán chủ thể cho dòng trắng/comment biên dùng AST gần nhất, không phải một chứng minh hành vi.

| Khẳng định | Diff khai ở đâu | Đo được (lệnh/script) | Khớp? |
|---|---|---|---|
| Đúng đối tượng và diff hai tệp | SHA/spec/write set | `sha256sum ../SPEC.md`; `git rev-parse HEAD HEAD^{tree}`; so byte `git diff 7eeb1d9a10aea8e1805b66fbf3d68549eb6778da HEAD` với diff.patch | Khớp cả SHA/tree/SPEC/diff/numstat |
| 338+36 dòng thêm; mở trần được cho phép | numstat; commit WIP khai +356 ở commit đầu | `git diff --numstat 7eeb1d9a10aea8e1805b66fbf3d68549eb6778da HEAD`; `git diff --numstat 7eeb1d9a10aea8e1805b66fbf3d68549eb6778da HEAD^` | HEAD +374/-116; HEAD^ +356, đúng lời khai lịch sử về diff; không finding trần |
| TinHieuChotCa riêng ở credential; 5 raise đổi kiểu | class, t6/t11/t12/t13 | AST đếm 5 raise mới; `probe_cred_measured.py` | 5 vị trí đúng; t11/12/13 đo bằng mutant; t6 bị neutral storage chặn |
| AssertionError trần chỉ nhận nếu frame trong cùng đúng tệp/assert | la_chot_cua_suite | `probe_oracles.py`; 5 mutant cc trong `probe_new_mutations.py` | Khớp loại/tệp/dòng; tệp khác có cùng số dòng assert bị loại |
| ten_do thêm loại ngoại lệ và chay_suite dùng nó | ten_do, chay_suite | `probe_cc_wiring.py`; `probe_cred_measured.py` | HEAD đúng; ca khóa điểm nối không đủ răng: F03 |
| Product phân loại AttributeError, AssertionError, đổi kiểu | cham_mot_ca | `probe_oracles.py`; `probe_neutral_runner.py` | Khớp; own assertion vẫn được tính giết |
| Neutral đỏ không cấp tín dụng, nền skip giữ kết quả cũ | ket_luan_mutant, chay_dot_bien | `probe_neutral_runner.py`, full --dot-bien | Khớp accounting `(1,0)` / all-skip `(0,1)` / mixed `(0,0)` |
| t79 và checkpoint bỏ assert trần, MCP bắt hợp đồng trả kết quả, r01/r10 chốt run.json | t79/t115/_r1079_run_json/r01/r10/checkpoint | `probe_11.py` trên base/HEAD | 10/10 đo được đổi từ lỗi cũ sang TinHieuChotCa ca đích, đúng tên mutant |
| Recovery/snapshot cũng giết lại bằng bang | r484_g2_recovery_probe_rollback_va_snapshot_moi | `probe_11.py`, neutral base/HEAD | KHÔNG ĐO ĐƯỢC: OSError trước assertion do /tmp/.git; không chỉ đọc mã rồi khai pass |
| rg/actionlint giả, installer về shim, npm trước materialize | N13 và bảng mutant N13 | `probe_fixture.py`; 3 mutant N13 trong `probe_new_mutations.py` | Khớp cho hook child: 7→0 installer, thứ tự giữ; mutant đỏ đúng chốt |
| “mọi lối … nằm TRONG fixture”, môi trường cha bị lọc | comment và env N13 | `probe_fixture.py`, `validate_hint.py` | **Không khớp toàn ca:** bước tim_bash còn 2 BASH_ENV/HOME cha, F02 |
| Năm ca khóa tự kiểm và 14 mutant mới | r1079_*; DOT_BIEN_HOOK/HARNESS; CC_TEST_DANG_DUNG | `audit_static.py`; `probe_new_mutations.py`; `probe_cc_wiring.py` | 5 ca neutral xanh, 14 mutant hiện có chết đúng chốt; chưa khóa được F01/F03 |
| Bản sao cc_test riêng, con trỏ được đưa vào ca khóa | nhánh hook loại cc_test và hoàn nguyên | 5 cc mutant độc lập, mỗi namespace mới | Đo được 5/5; không thay nhánh chấm hook sang cơ chế khác |
| Neutral product dùng LAUNCHER gốc, harness dùng bản sao nguyên; giữ bố cục hooks/ops | chay_dot_bien, _dung_cay_harness | `probe_neutral_runner.py`; `probe_runner_spoof.py`; full --dot-bien | Đúng về bố cục/neutral; neutral g8 vẫn đỏ do storage, không còn lấy FileNotFound làm tín dụng |
| “giet CHỈ khi … TinHieuChotCa”, không tin rc/headline riêng | cham_lap_ca, LOAI_HONG, chay_bo_ca, main | `probe_runner_spoof.py` qua runner đầy đủ | **Không đúng về loại thật:** tên lớp và đuôi stdout đủ để nhận tín dụng, F01 |
| Commit đầu: F01(a)(b)(c) sửa; F02 installer shim | `git log --format=%B 7eeb1d9a10aea8e1805b66fbf3d68549eb6778da..HEAD` | Các phép đo oracle/fixture ở trên | Đúng một phần; F01/F02 còn lỗ đo được; commit tự khai WIP/chưa nghiệm thu |
| Commit cuối: d8f8998 từng 531/536, sau sửa “10/10” | thông điệp c73dff3 | `commits.txt`; chạy toàn bộ HEAD và 14 mutant mới | Mẫu số d8f có thể đếm lại; số 531/536 là kết quả lịch sử khác môi trường, không có log cũ hoặc danh tính cụ thể cả 10 ca: **KHÔNG ĐO ĐƯỢC** nguyên lời khai. Không thay bằng số của sandbox hiện tại |
| Mã sản phẩm/hook/CI và cô lập process mỗi product mutant ngoài phạm vi | SPEC ngoài phạm vi | so Git blob launcher.py, session-start.sh, ci.yml BASE/HEAD; đọc runner | Ba blob không đổi. Product còn chạy chung process đúng phạm vi đã chấp nhận; không mở lại #824/#825/#826 |

Các trailer Co-Authored-By/Claude-Session trong commit là metadata được đọc lại, không tự chứng minh model identity hay CI. Bảng lời khai này do reviewer tự lập và có thể chưa bao hết mọi suy luận ngầm từ mã; không coi sự vắng mặt trong bảng là bằng chứng đúng. Các lớp đo trực tiếp bổ sung trong BANG SAN được dùng để tìm phần bảng có thể bỏ sót.

## BANG TEST

| Bộ | Lệnh | N/M, rc | Bỏ qua / giới hạn |
|---|---|---|---|
| Launcher HEAD | `python3 .claude/dev/launcher_test.py` | **302/325** ca chạy qua; tổng 335, đỏ 23, rc=1 | 10 BO QUA; log `evidence/launcher-head.log` |
| Launcher base | `python3 evidence/base/.claude/dev/launcher_test.py` từ thư mục verdict | **297/320**; tổng 330, đỏ 23, rc=1 | Cùng 10 BO QUA, cùng chính xác 23 tên đỏ; HEAD có thêm 5 ca khóa xanh |
| Mutation HEAD | `python3 .claude/dev/launcher_test.py --dot-bien` | **500/536**, rc=1; 540 mutant đăng ký | 4 không đo được theo nền; 36 SAI đều `neutral do`, không có SAI loại khác |
| Grader/report HEAD trên ca/bảng/fixture base | `python3 evidence/build_counterfactual.py` rồi `python3 evidence/counterfactual/.claude/dev/launcher_test.py --dot-bien` từ thư mục verdict | **476/522**, rc=1 | 4 bỏ qua; 36 neutral đỏ **cùng tên với HEAD**; 10 SAI khác là đúng 10 mục đo được trong danh sách 11 |
| Credential HEAD | `python3 .claude/dev/codex_cred_test.py` | Neutral **13/18**, rc=1; main chạy **0/18** mutant | Main dừng trước mutation; t6/t9/t15/t16/t18 đỏ do điều kiện home/storage |
| Credential base | `python3 evidence/base/.claude/dev/codex_cred_test.py` từ thư mục verdict | Neutral **13/18**, rc=1; main chạy **0/18** mutant | Cùng 5 ca đỏ, không phải hồi quy |
| Credential đo độc lập theo neutral đích | `python3 -B evidence/probe_cred_measured.py` | **13/13** mutant đo được chết đúng assertion suite | 5/18 chưa đo được vì neutral không xanh; t11/t12/t13 thuộc 13 ca đã đo |
| 11 mutant nguồn | `python3 -B evidence/probe_11.py` | HEAD **10/10** đo được chết bằng TinHieuChotCa; base 10 SAI đúng loại cũ | 1/11 neutral OSError ở cả hai, g2 recovery |
| 14 mutant mới | `python3 -B evidence/probe_new_mutations.py` | **14/14** chết đúng TinHieuChotCa của ca đích | 0 bỏ qua; `guard-mutations.json` ghi mutant/target/lý do |
| HINT regression | `python3 -B evidence/validate_hint.py` | 3 ca bắt F01/F02 đỏ đúng TinHieuChotCa trên HEAD; ca (c) xanh trên HEAD, đỏ đúng chốt trên mutant F03 | Đây là kiểm chứng phản chứng của hint, không phải gate xanh của một bản vá |

Sai lệch A2 so với “đúng 11 SAI” được phân rã: 10 SAI do lỗi oracle cũ đã xác nhận; mục thứ 11 `g2_rejected_refresh_khong_phu_thuoc_metadata` nằm trong 36 neutral đỏ; còn 35 neutral đỏ khác là nền đỏ sẵn trong sandbox. HEAD phục hồi đúng 10 mục đo được và thêm 14 mutant khóa xanh: **476 + 10 + 14 = 500**. Không gọi 36 neutral đỏ là kill hay hồi quy. Danh sách đủ, rc và so sánh tập tên: `evidence/results-summary.json`, tạo bằng `python3 -B evidence/summarize_results.py`.

Mười ca BO QUA của launcher được giữ nguyên theo tên ở `evidence/launcher-head.log` và `launcher-base.log`: t62 (Windows), bốn ca r345, hai ca r347, hai ca r348 (venv/pip không dựng được), r484_g4_windows_sid_alias_identity (Windows). Bốn mutant không đo được: ba Windows SID/pin và `124_khi_chau_con_song` vì ca Windows tự bỏ qua. Không cộng BO QUA vào tử số đã qua.

Credential CLI dừng đúng trước bảng mutant khi neutral chưa xanh, nên 13/13 mutant ở phép chạy độc lập **không phải** “main đã chạy 18/18”. Năm mutant chưa đo được có đích t6/t9/t15/t16/t18. Launcher HEAD có 540 mutant đăng ký, mẫu số 536 sau 4 bỏ qua; base/counterfactual có 526, mẫu số 522. Các mẫu số không lấy từ comment.

## BANG SAN

Các hướng sau dùng dữ liệu trơ và bản sao. Mỗi dòng có lệnh đã chạy và output thật; không dựng credential giống thật hoặc nội dung nhạy cảm mới.

| Hướng độc lập | Lệnh | Output thật | Phân loại |
|---|---|---|---|
| 1. Product: lỗi vô can, assert triển khai, except đổi kiểu | `python3 -B evidence/probe_oracles.py` | `a bare ('loi','bare(AssertionError)')`; `a unrelated ...AttributeError`; `a wrapped ...AssertionError`; `a own ('giet','own')` | KHÔNG PHẢI LỖI ở (a) |
| 2. Neutral đỏ qua runner đầy đủ, cả (a)/(b) | `python3 -B evidence/probe_neutral_runner.py` | HEAD neutral error/assert `(1,0)`, harness neutral `(1,0)`; base nhận `(0,0)` và không chạy neutral | KHÔNG PHẢI LỖI ở cơ chế mới |
| 3. All-skip/mixed, đối chiếu base | Cùng script neutral runner | Base/HEAD all-skip `(0,1)`; mixed `(0,0)`; HEAD own `(0,0)` | KHÔNG PHẢI LỖI; không chặn nhầm assertion đích đã đo |
| 4. Lớp RuntimeError chỉ trùng tên tín hiệu | `python3 -B evidence/probe_runner_spoof.py` | `review_same-name OK giet 1/1: review_target`, accounting `(0,0)` | **LỖI — F01** |
| 5. Child chỉ in đuôi LOAI_HONG/headline rồi SystemExit | Cùng script spoof; `probe_oracles.py` kiểm thêm giả ở giữa | Đuôi giả → `OK giet 1/1`, `(0,0)`; giả ở giữa rồi AttributeError thật → `loi` | **LỖI — F01**, anchoring chỉ chặn giả ở giữa |
| 6. Credential: AssertionError triển khai/đổi kiểu và tệp khác cùng dòng assert | `python3 -B evidence/probe_oracles.py`; `probe_new_mutations.py` | `c implementation False`, `c wrapped False`, `c other-file False`; bỏ kiểm tệp làm ca khóa chết bằng TinHieuChotCa | KHÔNG PHẢI LỖI ở classifier (c) |
| 7. Assertion từ ca khác/shared helper | `python3 -B evidence/probe_oracles.py` | Product/harness gọi ca khác ném cùng tín hiệu → `giet`; assert t1 trong suite credential có thể được ten_do gán tên t2 | Giới hạn provenance đã đo. M4 cho phép assert của cùng suite/helper; chưa có mutant sản phẩm thật nhảy sang ca khác. Không mở finding riêng chỉ từ việc gọi helper; không dùng phép này chứng minh “assertion riêng của ca” |
| 8. Comment giữ hình dạng điểm nối, bỏ thật ten_do | `python3 -B evidence/probe_cc_wiring.py` | `LOCK mutated-chay_suite SURVIVED`; HEAD unrelated không cấp kill, mutant unrelated cấp kill | **LỖI chốt thiếu răng — F03** |
| 9. Installer A/B trong cha thù địch, rg hỏng | `python3 -B evidence/probe_fixture.py` | Base nguyên ca PASS, INSTALLERS=7; HEAD nguyên ca PASS, INSTALLERS=0; nhật ký NPM trước LAUNCHER chuan-bi | KHÔNG PHẢI LỖI ở phép chắn installer của hook child |
| 10. BASH_ENV và HOME cha ở bước dò Bash | Cùng script fixture; `python3 -B evidence/validate_hint.py` | HEAD PASS nhưng OUTER có 2 `BASH_ENV HOME=<ambient-home>`; ca hồi quy đỏ bằng TinHieuChotCa với hai AMBIENT_INIT | **LỖI — F02** |
| 11. 11 mutant nguồn và phản chứng ca base | `python3 -B evidence/probe_11.py`; chạy counterfactual | 10 base SAI đúng loại → 10 HEAD giết đúng chốt; một g2 recovery neutral OSError ở cả hai | KHÔNG PHẢI LỖI phần đo được / KHÔNG ĐO ĐƯỢC storage |
| 12. Gỡ từng chốt mới; fixture base dưới hậu điều mới | `python3 -B evidence/probe_new_mutations.py`; `python3 -B evidence/probe_base_fixture_lock.py` | `TOTAL 14 RIGHT_REASON 14`; base fixture + new postcondition TARGET TinHieuChotCa, installer calls 7 | KHÔNG PHẢI LỖI với 14 mutant hiện có; không phủ định F03 |
| 13. Nền môi trường, cổng tĩnh, bất biến cây | Ba suite; `python3 -B evidence/audit_static.py`; `python3 -B evidence/verify_tree.py` | Cùng 23 lỗi/10 bỏ qua; ruff delta0, diff/doctrine rc0; 10120 tệp, changed=[], git status rỗng | KHÔNG PHẢI LỖI mới; A1/CI chưa đo được |

Không thấy bộ chấm mới chặn nhầm lần giết thật trong 10 mutant nguồn, 13 mutant credential và 14 mutant khóa đo được, cùng đối chứng own assertion của (a)/(b). Những lần gate đỏ vì neutral đỏ được tách riêng; không diễn giải chúng thành test yếu hoặc assertion bị bộ chấm bỏ sót.

### F01-harness-tin-ten-loai-va-duoi-stdout [P1] Harness nhận lỗi khác tên giống tín hiệu và output giả là giết hợp lệ

TEP/DONG: `.claude/dev/launcher_test.py:14525`, `:14529` (LOAI_HONG dùng `type(e).__name__`), `:14492`–14494 (so chuỗi suffix); ca khóa `:9981`–10000 chỉ thử giả ở giữa output.

VAN DE: Reporter không ghi việc `isinstance(e, TinHieuChotCa)` có thật hay không; chỉ ghi tên lớp. Một lớp RuntimeError độc lập tên TinHieuChotCa vì thế đi qua cùng giao thức với chốt suite. Ngoài ra ca có thể in đúng hai dòng cuối và thoát bằng SystemExit(1), vượt khỏi catch Exception, nên không có báo cáo chính thức của runner nhưng suffix vẫn được tin. Cả hai cho tín dụng giả khi neutral trước đó qua. Đây là sai hành vi M3/F01, độc lập với bẫy storage; không chỉ là thiếu bài test.

DA THU NGHIEM: `PYTHONDONTWRITEBYTECODE=1 python3 -B evidence/probe_runner_spoof.py`. Hai mutant harness trên bản sao, neutral `review_target` qua, mutant lần lượt chỉ ném lớp RuntimeError trùng tên hoặc in đuôi rồi SystemExit. Runner HEAD thật in:

```text
review_same-name             OK  giet 1/1: review_target
same-name accounting (0, 0)
review_fake-suffix           OK  giet 1/1: review_target
fake-suffix accounting (0, 0)
```

Đối chứng `probe_oracles.py`: bare AssertionError và except AttributeError→AssertionError đều bị loại; assertion suite thật vẫn nhận giết; marker giả ở giữa output rồi AttributeError thật bị loại. Vì vậy finding nhắm chính xác vào danh tính lớp và nguồn suffix, không bác việc chặn headline cũ đã có ích.

DO TIN: cao — qua `chay_dot_bien` đầy đủ, có neutral, không mock CompletedProcess, không dùng API/mạng/credential.

Gợi ý vá ở reporter và `cham_lap_ca`: phân loại bằng danh tính lớp thật trong tiến trình con, truyền kết quả qua kênh kết quả riêng có định danh lượt/ca, không lấy stdout của ca làm nguồn chứng cứ. Khi child thoát trước báo cáo đáng tin thì xếp lỗi runner, không giết. Giữ loại ngoại lệ cụ thể để chẩn đoán. Chỉ mô tả hướng sửa bộ chấm; HINT đính kèm chỉ thêm ca hồi quy.

Ca khóa: hai ca đầu HINT phải đỏ trên HEAD hiện tại bằng TinHieuChotCa của chính ca; sau sửa phải qua. Mutant quay lại chấm theo tên lớp hoặc chỉ suffix phải giết đúng hai ca tương ứng. Rủi ro vá: làm mất kết quả hợp lệ hoặc biến skip Windows thành lỗi; giữ đối chứng own assertion, wrapped error và all-skip/mixed, đồng bộ writer/reader của giao thức.

### F02-n13-do-bash-ke-thua-init-va-home-cha [P1] N13 lọc môi trường cho hook nhưng để bước tim_bash chạy BASH_ENV của cha

TEP/DONG: `.claude/dev/launcher_test.py:8998`–9002 tạo env sạch/HOME tạm, nhưng `:9007` gọi `tim_bash()` ngoài env ấy; kiểm cuối `:9017` chỉ nhìn ky.log của fixture.

VAN DE: `tim_bash()` thực hiện hai subprocess năng lực Bash. Chúng thừa hưởng `os.environ` thật của ca, nên đọc BASH_ENV và chạy dưới HOME cha trước khi hook child được gọi với env sạch. Script init có thể chạm installer/HOME của runner trong giai đoạn này; phép đo chỉ ghi marker trơ để chứng minh đường đi, không dựng hành động nhạy cảm. Cả hai lần thực thi nằm ngoài ky.log mà chốt N13 kiểm, nên nguyên ca vẫn PASS. M6 yêu cầu cô lập fixture, không chỉ child cuối.

DA THU NGHIEM: `PYTHONDONTWRITEBYTECODE=1 python3 -B evidence/probe_fixture.py`. Cha có rg hỏng, installer shim chỉ ghi log/thoát 97, BASH_ENV chỉ ghi marker và HOME trỏ thư mục trơ của reviewer. Output:

```text
base fixture PASS None
base INSTALLERS 7 BASH_ENV 3
head fixture PASS None
head INSTALLERS 0 BASH_ENV 2
```

Hai dòng OUTER của HEAD đều ghi HOME cha, không phải `s/home`. INNER vẫn có `NPM install -g @openai/codex` trước `LAUNCHER chuan-bi`, không có installer ngoài npm. Do đó công nhận phần chắn installer đã vá, nhưng không công nhận tuyên bố môi trường fixture đã kín. HINT case `r1079_n13_do_bash_cung_phai_loc_env_cha` đỏ đúng TinHieuChotCa: `['AMBIENT_INIT', 'AMBIENT_INIT']`.

DO TIN: cao — nguyên ca HEAD, công cụ/marker trơ, có A/B base, không phụ thuộc /tmp/.git.

Gợi ý vá tại N13: dùng cùng môi trường đã lọc BASH_ENV/ENV/BASH_FUNC_* và HOME tạm cho **mọi** subprocess của ca, gồm tim_bash; có thể đặt context môi trường sạch quanh bước dò và luôn hoàn nguyên sau ca, hoặc dò trong subprocess với env tường minh. Ghi nhận từ môi trường cha độc lập với ky.log để phát hiện thoát fixture. Không sửa hook sản phẩm để tránh nhánh cần thử.

Ca khóa: BASH_ENV cha chỉ ghi marker không được chạy, trong khi NPM vẫn trước chuan-bi. Mutant bỏ môi trường sạch quanh bước dò phải làm chính ca mới đỏ. Rủi ro vá: làm mất ứng viên Bash cần thiết trên Windows, thay PATH quá rộng hoặc không hoàn nguyên os.environ; giữ đối chứng tìm Bash và nguyên N13/N14.

### F03-cc-ca-khoa-chi-tim-chuoi-diem-noi [P2] Ca khóa credential không đo hành vi chay_suite và sống khi khôi phục bộ chấm sai

TEP/DONG: `.claude/dev/launcher_test.py:10040`–10043, nhất là `inspect.getsource(ns["chay_suite"])`; mutant đăng ký `:14145`–14146.

VAN DE: Ca khóa thử helper `la_chot_cua_suite`/`ten_do`, rồi chỉ tìm chuỗi `do.add(ten_do(...))` để kết luận runner thật dùng classifier. Nó không chạy `chay_suite` trên một ca ném lỗi vô can. Giữ chuỗi đó trong comment trong khi đổi câu thực thi thành `do.add(ca.__name__)` là đủ để ca khóa xanh dù khôi phục nguyên lỗi cấp tín dụng giả. Grader HEAD hiện tại ở (c) xử lý đúng; finding này là **chốt thiếu răng** theo M7, không nhận vơ rằng production HEAD đã sai ở (c).

DA THU NGHIEM: `PYTHONDONTWRITEBYTECODE=1 python3 -B evidence/probe_cc_wiring.py` trên bản sao. Thay đúng một câu trong credential test, giữ lời gọi cũ ở comment. Output:

```text
LOCK mutated-chay_suite SURVIVED
head neutral [] would_grant_kill False
head unrelated ['t2_chua_thay_thi_tra_None_khong_doan(AttributeError)'] would_grant_kill False
mutant neutral [] would_grant_kill False
mutant unrelated ['t2_chua_thay_thi_tra_None_khong_doan'] would_grant_kill True
```

DO TIN: cao — ca khóa hiện có xanh trên mutant sai, sau đó gọi runner thật xác nhận lỗi được nhận tín dụng.

Gợi ý vá ngay ca khóa (c): gọi `chay_suite` thật với ca thật trong suite và module trơ, kiểm neutral, assertion suite thật, AttributeError và AttributeError đổi sang AssertionError; không dùng comment/source text làm chứng cứ điểm nối. HINT bổ sung ca hành vi theo hướng này: xanh trên HEAD và đỏ đúng TinHieuChotCa trên mutant giữ comment. Có thể giữ kiểm hình dạng như một lớp phụ.

Ca khóa: thêm mutant đổi do.add đồng thời giữ lời gọi trong comment; nó phải giết đúng ca hành vi mới. Rủi ro vá: mock cả classifier/runner sẽ làm test tự chứng minh chính nó; giữ runner, classifier và assertion ca thật, chỉ thay nguồn module triển khai trơ, tránh phụ thuộc credential storage đang không đo được.

## HINT và bảo toàn cây

`HINT.patch` dùng `patch -p0` từ gốc `cay-kho/`, nhưng chỉ đã dry-run và chạy trên bản sao. Nhãn bắt buộc: **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Patch chỉ thêm bốn ca test, không sửa bộ chấm hoặc mã sản phẩm nhạy cảm. Hướng vá bộ chấm được mô tả bằng lời ở từng finding. Executor cần tự dẫn xuất và khai hint_provenance nếu dùng.

`patch --dry-run -p0 -d evidence/head < HINT.patch`: rc=0. `python3 -B evidence/validate_hint.py`: ba ca hồi quy F01/F02 đỏ bằng đúng TinHieuChotCa trên HEAD; ca hành vi credential xanh trên HEAD, đỏ bằng đúng TinHieuChotCa trên mutant F03. Không xem patch test đỏ này là bản vá hoàn chỉnh có thể áp rồi merge.

Kiểm cuối: `python3 -B evidence/verify_tree.py` đối chiếu **10120 tệp** với Git blob, `changed=[]`; `git status --porcelain` rỗng; HEAD/tree vẫn giữ đúng OID ban đầu. Ba tệp .cmd có CRLF theo `.gitattributes`; chuẩn hóa đúng thuộc tính Git thì khớp blob, không phải thay đổi do review. Chi tiết ở `evidence/final-integrity.json`. Băm HINT: `e37a6dd591ad377b63841f96394e1bc6d7b587ec649e71ca18a2ac4666bdf21a`.

Ruff dùng bản có sẵn **0.16.8** ở cả hai phía; CI ghim 0.15.15, không cài hoặc tải bản khác trong sandbox. Kết luận delta F=0 là phép A/B cùng binary hiện có, không thay bằng chứng CI exact HEAD.

Nhật ký tiến độ đã ghi trong lúc làm được lưu ở `evidence/progress.log`. Các log `*-initial.log` bị thay thế bởi lượt HOME chuẩn hóa, không dùng để tính bảng nghiệm thu.

Các số lịch sử CI/Windows không được đo bằng đọc comment. Không thực hiện land/merge, không đăng verdict lên dịch vụ ngoài, không nhận thay vai approver. Verdict này neo duy nhất exact SHA nêu ở đầu.
