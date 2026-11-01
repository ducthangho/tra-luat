verdict: changes_requested
reviewed_sha: d929ee2dfa93f079a98d7e577ef6061e8e894d3a
spec_sha256: 81070fa2c5a00bc0bb63867c7173f310cba9002001b68a26d62726ec904cbf5b
Ket qua: 0 P0, 4 P1, 1 P2, 0 P3.

F01 lượt 1 chưa đóng toàn bộ: đã chặn lớp lồng trong hàm và stdout giả, nhưng lớp khác có cùng `__qualname__` vẫn nhận tín dụng. F02 và F03 lượt 1 đã đóng trên các phản chứng đã chạy. Bản vá còn nhận kết quả kênh giả trước khi ca chạy, nhận assertion của ca khác, bỏ mất ca đích không tồn tại, và có ca khóa neutral chỉ kiểm văn bản.

provider: openai_codex
model_family: openai
execution_surface: codex_service
transport: machine
exact_model_id: runtime không cung cấp định danh endpoint để kiểm chứng độc lập
reviewer_role: reviewer độc lập với executor Claude
reviewed_tree: b561926d68a0271f8c13391ff3459f8bb3be04c3
packet_id: wp1079
revision: r1
generation: 3
lease: wp1079-r1-g3-claude
review_class: sensitive
review_call: 2/2 (cuối)

## Phạm vi, cách chạy lại và giới hạn

Đã đọc PROMPT, SPEC đóng băng, verdict lượt 1, hai finding nguồn #484, diff tổng, diff từ lượt 1, và thông điệp của 29 commit trong BASE..HEAD. Diff `.claude` khớp byte với `diff.patch`: 471 thêm, 117 xóa, hai tệp. Phần ngoài `.claude/` bằng exact master đã merge (`767a68d^2`), không gán cho packet. Trần thêm 480 đã được cho phép, không tính finding.

Các lệnh trong bảng chạy từ `cay-kho/`; script tự tìm thư mục theo `__file__`. `../evidence/run_suites.py` chạy đúng ba lệnh suite, ghi cả command, rc và log. Môi trường dùng HOME tạm tuyệt đối, `PYTHONDONTWRITEBYTECODE=1`, `PIP_NO_INDEX=1`, `PIP_DISABLE_PIP_VERSION_CHECK=1`; bỏ `CODEX_AUTH_JSON`, `CODEX_HOME`, `TL_CODEX_SNAPSHOT`, `OPENAI_API_KEY`, `GH_TOKEN`, `GITHUB_TOKEN`, `GITHUB_PAT`, init shell và hàm Bash kế thừa. Các fixture tự dựng dữ liệu trơ cần thiết. Không gọi mạng, không dùng credential thật, không sửa/push cây executor. Bản sao lấy bằng `git archive` exact HEAD, BASE và head lượt 1; mọi đột biến ở `evidence/` hoặc `/tmp`, ngoài `cay-kho/`.

`ls -ld /tmp/.git` trả thư mục chỉ đọc `dr-xr-xr-x`. Một số ca còn cần ghi `/var/tmp`, nơi sandbox từ chối. Không xóa `.git` hay đổi backend để làm xanh. HEAD/base có **cùng tập 23 tên ca lỗi**, cùng 10 ca bỏ qua; không phát hiện hồi quy suite qua phép so tên. A1 với tiền đề `/tmp/.git` vắng, Windows thật và check-run CI exact HEAD là **KHÔNG ĐO ĐƯỢC**, không quy thành finding. Thất bại của bộ chấm khi nhận tín dụng giả được đo riêng bằng ca trơ có neutral xanh.

Các script xây bản sao đã có cơ chế dọn thư mục riêng trước khi chạy lại. Log cố định có thể xem ngay, không cần chạy lại toàn bộ suite. `evidence/claims-all-lines.tsv` kiểm kê mọi dòng đổi; `evidence/commits.txt` giữ toàn bộ thông điệp commit.

## Đóng finding lượt 1 trước

| Finding cũ | Lệnh chạy lại | Output thật | Đóng? |
|---|---|---|---|
| F01/P1: lớp trùng tên và đuôi stdout giả | `python3 -B ../evidence/probe_oracles.py`; `python3 -B ../evidence/probe_runner.py` | Hai ca hồi quy cũ PASS; `spoof_stdout → loi`. Nhưng `same_name_top_runtime` và `same_name_top_assert → giet`; runner thật `OK giet 1/1`, accounting `(0,0)` | **Chưa đóng toàn lớp — F01 dưới đây** |
| F02/P1: tim_bash chạy BASH_ENV/HOME cha | `python3 -B ../evidence/probe_fixture.py` | Lượt 1 installer=0/BASH_ENV=2; HEAD installer=0/BASH_ENV=0. Hai phép dò Bash và hook cùng HOME fixture, không BASH_ENV/ENV/BASH_FUNC_* | **Đóng trên POSIX đã đo** |
| F03/P2: credential chỉ kiểm chuỗi điểm nối | `python3 -B ../evidence/probe_measurements.py` | Mutant đổi `do.add` nhưng giữ nguyên lời gọi cũ trong comment làm `r1079_cc_chay_suite_phai_do_hanh_vi` ném **TinHieuChotCa của chính ca** | **Đóng**; ca kiểm văn bản neutral khác còn yếu, F07 |

## BANG NGHIEM THU

| Tiêu chí | Lệnh chạy được | Output/bằng chứng | Đạt? |
|---|---|---|---|
| M1: product phân biệt chốt/lỗi, giữ skip | `python3 -B ../evidence/probe_oracles.py`; `python3 -B ../evidence/probe_origin.py`; `python3 -B ../evidence/probe_wiring.py` | Own assertion → giet; bare/wrapped → loi. Assertion ca khác vẫn `OK giet 1/1`; target vắng bị bỏ khỏi mẫu số | Đạt phân loại lớp thông thường; **không đạt bảo đảm đúng ca và giữ semantics target — F05/F06** |
| M2: neutral (a)/(b), cache, fail-close | `python3 -B ../evidence/probe_neutral_runner.py`; suite mutation | Product neutral error/assert → `(1,0)`; harness neutral error → `(1,0)`; hai mutant cùng target có neutral=1/mutant=2. 36 neutral đỏ không nhận tín dụng | **Đạt hành vi đo được**; chốt chống hồi quy chưa đủ, F07; target vắng không được đo, F06 |
| M3: harness chỉ nhận chốt đích thật | `python3 -B ../evidence/probe_runner.py`; `python3 -B ../evidence/probe_oracles.py` | Stdout giả bị loại; real assertion được giữ. Lớp cùng qualname và kênh giả trước main vẫn `OK giet 1/1` | **Không — F01/F04/F05** |
| M4: credential chỉ nhận lớp riêng hoặc assert đúng tệp | `python3 -B ../evidence/probe_oracles.py`; `python3 -B ../evidence/probe_measurements.py`; `python3 -B ../evidence/probe_origin.py` | Wrapped/implementation AssertionError bị loại; tệp khác cùng dòng assert bị loại; 13/13 mutant có neutral xanh chết ở assertion suite | Đạt phép kiểm loại/tệp được SPEC cho phép; **chưa bảo đảm assertion đúng ca**, F05. 5 neutral bị môi trường chặn |
| M5: phục hồi đúng 11 mutant nguồn | `python3 -B ../evidence/probe_measurements.py` | HEAD 10 neutral xanh/10 TinHieuChotCa đúng target; base tương ứng 4 AssertionError + 2 FileNotFoundError + JSONDecodeError + 2 TypeError + AttributeError. Mutant recovery còn lại neutral OSError ở cả hai | **Đạt 10/10 đo được; KHÔNG ĐO ĐƯỢC 1/11** |
| M6: N13 cô lập installer/init/HOME và giữ thứ tự | `python3 -B ../evidence/probe_fixture.py` | Base installer=7/init=3; lượt 1 installer=0/init=2; HEAD installer=0/init=0. `NPM install -g @openai/codex` trước `LAUNCHER chuan-bi` | **Đạt POSIX đã đo** |
| M7: ca khóa và mutant đúng lý do | `python3 -B ../evidence/probe_measurements.py`; `python3 -B ../evidence/probe_wiring.py`; `python3 -B ../evidence/make_hint.py` | 9 ca khóa HEAD xanh; 17 mutant mới/18 target outcomes đều TinHieuChotCa đúng ca. Nhưng neutral lock sống khi câu cũ chỉ còn trong literal, rồi runner cấp tín dụng cho neutral đỏ. HINT 7/7 đỏ đúng tín hiệu trên HEAD | **Không đủ — F07 và các phản chứng F01/F04/F05/F06** |
| A1: ba suite xanh dưới nền sạch | Ba lệnh ở BANG TEST; `ls -ld /tmp/.git` | Tiền đề không thỏa; HEAD/base cùng tập lỗi nền; mutation HEAD 503/539, base 522/522 theo grader cũ | **KHÔNG ĐO ĐƯỢC** nền nghiệm thu sạch; không nhận các số này là A1 đạt |
| A2: grader mới trên ca base, ca khóa đỏ với grader/fixture cũ | `python3 -B ../evidence/build_counterfactual.py`; chạy `../evidence/counterfactual/.claude/dev/launcher_test.py --dot-bien`; `python3 -B ../evidence/probe_base_locks.py`; `python3 -B ../evidence/probe_base_fixture_lock.py` | Counterfactual 476/522: 10 SAI không-neutral đúng danh sách nguồn, 36 neutral đỏ trùng HEAD. Ca khóa product/wiring/credential/bash đỏ bằng chốt HEAD trên semantics/base thật. Base fixture + hậu điều HEAD đỏ sau 7 installer | Đạt phản chứng đo được; **đúng 11 SAI trên nền sạch KHÔNG ĐO ĐƯỢC** |
| A3: installer ngoài npm=0 và base>0 | `python3 -B ../evidence/probe_fixture.py` | Base 7 → HEAD 0, log ngoài fixture độc lập; base/HEAD nguyên ca đều PASS | **Đạt** |
| A4: ruff delta, diff-check, doctrine, CI | `python3 -B ../evidence/audit_static.py`; `git diff --check BASE HEAD -- .claude` | Ruff F 5→5, normalized delta rỗng; packet diff-check rc=0; doctrine rc=0, 10 tệp/0 chỗ. Toàn diff rc=2 tại `ops/specs/launcher-sandbox-lay-mau-r2.md:242`, là nội dung master bằng merge parent | Đạt cổng cục bộ của packet. Toàn diff có whitespace kế thừa; CI exact HEAD **KHÔNG ĐO ĐƯỢC** do cấm mạng/thiếu hiện vật |

Counterfactual chỉ thay grader/reporter và phụ thuộc cần thiết; giữ nguyên CA, fixture, bảng mutation và launcher của BASE. Adapter trong phép ca khóa product gọi **chay_dot_bien BASE thật** với một mutant và một case, không tự giả kết quả phân loại. Phép fixture base chỉ thêm hậu điều HEAD, cho shim ghi đồng thời log ngoài và `ky.log` của fixture để hậu điều quan sát được installer; không thay hook hoặc cho installer thật chạy.

## BANG DO

Cách tìm lời khai: `setup.py` duyệt từng dòng thêm/xóa của diff; `inventory.py` gắn đường dẫn, phía old/new, số dòng và chủ thể AST vào **588 dòng đổi**, gồm cả dòng trắng/comment/bảng literal. Không chỉ tìm số hoặc tên hàm. Đọc toàn diff và `git log --format=%B BASE..HEAD`; lưu 29 thông điệp. Bảng sau gom từng nhóm hành vi/khẳng định; kiểm kê dòng đầy đủ là `claims-all-lines.tsv`. Dòng ngoài thân AST được ghi rõ là module/comment/table, không coi phép gắn chủ thể là chứng minh hành vi.

| Khẳng định | Diff/commit khai | Đo được bằng lệnh | Khớp? |
|---|---|---|---|
| Đúng HEAD/SPEC/diff/write set | PROMPT, diff hai tệp | `python3 -B ../evidence/setup.py`; `python3 -B ../evidence/inventory.py`; `sha256sum ../SPEC.md` | Đúng SHA/tree/hash; diff byte khớp; +471/-117; 339 tên CA duy nhất, không target thiếu trong bảng hiện tại |
| 356 dòng thêm ở WIP đầu; bố cục harness được sửa ở c73 | d8f8998, c73dff3 | `python3 -B ../evidence/audit_claims.py`; full mutation; N13 trên copied harness | d8 +356; c73 +374; HEAD +471. Copied N13 chạy qua, không thiếu hooks/bash_nen. Ca g8 còn bị storage chặn, không khai đã đo kernel |
| Recovery/checkpoint giữ điều kiện khi assert→bang | diff ba ca | `python3 -B ../evidence/audit_claims.py`; SOURCE11 trong `measurements.log` | 20 + 8 biểu thức assert của hai ca được giữ nguyên trong bang. t79 đổi raise riêng; 4 mutant đo được chết đúng target. Recovery runtime **KHÔNG ĐO ĐƯỢC** |
| run.json vắng là chốt r01/r10, MCP ném là vi phạm hợp đồng | `_r1079_run_json`, t115 | `python3 -B ../evidence/probe_measurements.py` | Hai FileNotFoundError và bốn lỗi MCP đổi thành TinHieuChotCa đúng ca, neutral xanh |
| Product loại bare/wrapped lỗi vô can, skip/neutral/cache đúng | helper và nhánh (a) | `python3 -B ../evidence/probe_oracles.py`; `python3 -B ../evidence/probe_neutral_runner.py` | Khớp các đối chứng này; assertion ca khác và target vắng còn lọt |
| N13 mọi subprocess dùng môi trường sạch, không installer | comment, env, ee23c44 | `python3 -B ../evidence/probe_fixture.py` | Khớp 7→0 installer và 3→0 init. HOME fixture ở cả hai bước dò và hook; thứ tự npm/chuan-bi đúng |
| Credential lớp riêng, 5 raise đổi loại, nhận assert đúng tệp | codex_cred_test diff | AST inventory; `python3 -B ../evidence/probe_measurements.py` | 5 raise đổi lớp; 13 mutant đo được có assertion suite thật. 5 neutral chặn bởi môi trường; nhận assertion ca KHÁC là giới hạn còn lại |
| Credential nối ten_do bằng hành vi, giữ comment không lừa được | ee23c44, ca mới và mutant cc | `python3 -B ../evidence/probe_measurements.py`; `python3 -B ../evidence/probe_base_locks.py` | Khớp; F03 cũ đóng, mutant đỏ đúng ca mới |
| “danh tính lớp THẬT”, lớp khác trùng tên không qua | comment :14618, ee23c44 | `python3 -B ../evidence/probe_runner.py` | **Sai với cùng qualname**, F01; chỉ trường hợp local qualname khác đã được chặn |
| Tệp+nonce, gỡ env trước ca, stdout không làm chứng cứ | cham_lap_ca/main, ee23c44 | `python3 -B ../evidence/probe_oracles.py`; `python3 -B ../evidence/probe_runner.py` | Gỡ khỏi os.environ khi vào case và loại stdout giả là đúng; **initializer trước main vẫn giả kênh được**, F04 |
| Mutant báo tên lớp trước đó chỉ đổi một nhánh nên sống, sửa cả hai nhánh giết đúng ca | d929ee2 | `python3 -B ../evidence/probe_base_locks.py`; `python3 -B ../evidence/probe_measurements.py` | Old one-branch mutant lock `qua`; current two-branch mutant TinHieuChotCa đúng target. Số lịch sử 538/539 trên môi trường executor **không xác nhận lại** ở sandbox này |
| Các con số lịch sử 531/536, 10/10; hint_provenance SHA | c73dff3, ee23c44 | `git show c73dff3`; `git show ee23c44`; log hiện tại | Đo lại bố cục/ca hồi quy và current mutants; không có log môi trường cũ hay HINT cũ nguyên byte để xác minh SHA provenance và toàn số lịch sử — **KHÔNG ĐO ĐƯỢC**, không giả nhận đã xác thực |
| 9 khóa, mỗi chốt có mutant đúng target | bảng mới và comment | `python3 -B ../evidence/probe_measurements.py`; `python3 -B ../evidence/probe_wiring.py` | 17 mutant/18 target outcomes đúng chốt thật; **không chứng minh đủ độ phủ**, F07 |
| 25 message khác và nội dung ngoài packet đến từ master | merge 767a68d và log BASE..HEAD | `python3 -B ../evidence/audit_claims.py`; `git log --format=%B BASE..HEAD` | Outside .claude bằng exact merge master. Các lời khai CI/GitHub/authority/run lịch sử trong message master không có dữ liệu kiểm lại offline, ghi **KHÔNG ĐO ĐƯỢC**, không gán là hồi quy packet |

`BASE` trong lệnh Git là `7eeb1d9a10aea8e1805b66fbf3d68549eb6778da`, không phải ref chuyển động. Các script dùng đầy đủ OID này.

## BANG TEST

| Bộ | Lệnh thực chạy | N/M, rc | Bỏ qua/không đo được |
|---|---|---|---|
| HEAD launcher | `python3 .claude/dev/launcher_test.py` | **306/329** ca đã chạy qua; tổng 339; hỏng 23; rc=1 | **10**: 1 Windows timeout, 1 Windows SID, 8 venv/pip offline |
| BASE launcher | Cùng lệnh, archive exact BASE | **297/320**; tổng 330; hỏng 23; rc=1 | **10**, cùng tập tên/lý do HEAD; cùng 23 tên hỏng |
| HEAD mutation | `python3 .claude/dev/launcher_test.py --dot-bien` | **503/539**; tổng 543; rc=1 | **4** nền; 36 neutral đỏ tính hỏng, không gộp vào skip |
| BASE mutation | Cùng lệnh, archive exact BASE | **522/522**; tổng 526; rc=0 | **4** nền; grader cũ cấp tín dụng giả, không chứng minh đúng nguyên nhân |
| HEAD credential | `python3 .claude/dev/codex_cred_test.py` | Nền **13/18**; `TỔNG: ĐỎ`; rc=1 | Không có skip hợp lệ; 5 neutral đỏ, không chạy mutation toàn suite |
| BASE credential | Cùng lệnh, archive exact BASE | Nền **13/18**; `TỔNG: ĐỎ`; rc=1 | Cùng 5 tên lỗi |
| Grader HEAD trên ca/bảng BASE | `python3 ../evidence/counterfactual/.claude/dev/launcher_test.py --dot-bien` | **476/522**; 46 SAI=36 neutral+10 lỗi vô can; rc=1 | 4 nền; đúng 1/11 source mutant bị neutral storage chặn |
| Credential target riêng | `python3 -B ../evidence/probe_measurements.py` | **13/13** target có neutral xanh đều chết bằng assertion suite thật | **5/18** neutral không xanh, không nhận là kill |
| Khóa/mutant mới đăng ký | Cùng script | **9/9** khóa neutral xanh; **17/17** mutant mới, **18/18** target outcomes là TinHieuChotCa đúng ca | 0 |
| HINT bổ sung | `python3 -B ../evidence/make_hint.py` | **7/7 ĐỎ trên HEAD**, đều TinHieuChotCa của chính ca mới | Đây là phản chứng, chưa có bản vá runtime để xác nhận hậu vá |
| Cổng tĩnh | `python3 -B ../evidence/audit_static.py` | Ruff F 5→5/delta=0; doctrine rc=0; packet diff-check rc=0 | CI exact HEAD, Windows và A1 nền sạch chưa đo |

Bốn mutation skip: `g4_windows_sid_alias_not_normalized`, `g4_windows_LA_not_current_owner`, `g2_windows_directory_pin_access`, `124_khi_chau_con_song`. Hai tập 23 ca hỏng ở `head-failed-names.json` và `base-failed-names.json`; skip giữ nguyên văn trong log launcher. Không chỉ so tổng số.

## BANG SAN

| Hướng độc lập | Lệnh | Output thật | Kết luận |
|---|---|---|---|
| 1. AttributeError đổi kiểu qua except | `python3 -B ../evidence/probe_runner.py` | `review_wrapped SAI giet 0/1 … review_target(AssertionError)`, accounting `(1,0)` | KHÔNG PHẢI LỖI ở đối chứng này |
| 2. AssertionError trực tiếp từ triển khai | `python3 -B ../evidence/probe_oracles.py` | Harness bare→loi; product bare→loi; credential behavioral lock PASS | KHÔNG PHẢI LỖI ở đối chứng này |
| 3. Lớp khác cùng tên đầy đủ | `python3 -B ../evidence/probe_runner.py` | RuntimeError/AssertionError cùng qualname đều `OK giet 1/1`, `(0,0)` | **LỖI — F01** |
| 4. Stdout giả LOAI_HONG/headline rồi exit | `python3 -B ../evidence/probe_oracles.py` | `spoof_stdout ('loi', 'review_target(khong co ket qua kenh, rc=1)')` | KHÔNG PHẢI LỖI; phần này F01 cũ đã vá |
| 5. Giả kết quả qua env lúc khởi tạo module | `python3 -B ../evidence/probe_runner.py` | `review_forged_channel OK giet 1/1`, `(0,0)`, target chưa chạy | **LỖI — F04** |
| 6. Assertion của ca khác | `python3 -B ../evidence/probe_origin.py`; `python3 -B ../evidence/probe_oracles.py` | Product/harness `giet review_target`; credential assertion t1 ghi thành tên đỏ t2, `credited_target True` | **LỖI — F05** |
| 7. Neutral đã đỏ, cache, all-skip/mixed | `python3 -B ../evidence/probe_neutral_runner.py` | Neutral đỏ `(1,0)`; skip `(0,1)`; mixed `(0,0)`; hai mutant neutral=1/mutant=2 | KHÔNG PHẢI LỖI hành vi HEAD ở dữ liệu hợp lệ |
| 8. Target không tồn tại/thiếu một phần | `python3 -B ../evidence/probe_wiring.py` | HEAD all-missing `(0,1)`; partial-missing `OK giet 1/1` `(0,0)`; base tương ứng SAI 0/1 và SAI 1/2 | **LỖI — F06** |
| 9. Neutral lock giữ chuỗi cũ trong literal | Cùng script | `NEUTRAL WIRING LOCK SURVIVED`; runner mutant neutral đỏ lại `OK giet 1/1` | **LỖI chốt thiếu răng — F07** |
| 10. Credential tệp khác cùng dòng assert | `python3 -B ../evidence/probe_oracles.py`; `python3 -B ../evidence/probe_measurements.py` | Khóa classifier PASS; mutant bỏ so tệp TinHieuChotCa đúng ca | KHÔNG PHẢI LỖI ở kiểm tệp |
| 11. N13 trong cha thù địch | `python3 -B ../evidence/probe_fixture.py` | Base 7 installer/3 init, lượt 1 0/2, HEAD 0/0; npm trước chuan-bi | KHÔNG PHẢI LỖI; F02 cũ đã đóng |
| 12. Kênh nonce sai, target sai, cấu trúc hỏng | `python3 -B ../evidence/probe_oracles.py` | Nonce/target sai→loi; JSON list→AttributeError chưa bắt; record thiếu counts→qua; record hong=1 nhưng rc=0→giet | Loại nonce/target đúng. Record không kiểm schema/rc là giới hạn liên quan F04; crash JSON list làm cổng đỏ, không đếm thành finding cấp tín dụng độc lập |
| 13. Chặn nhầm kill thật | `python3 -B ../evidence/probe_runner.py`; `python3 -B ../evidence/probe_measurements.py` | Real assertion `OK giet 1/1`; 10/10 source mutant đo được, 13/13 credential, 17/17 mutant mới đều đúng chốt | KHÔNG thấy chặn nhầm trong phạm vi đo được; không nhận vơ 1 source mutant bị storage chặn |
| 14. Nền storage/Windows/CI | Ba suite + base; `ls -ld /tmp/.git` | Cùng 23 ca lỗi; /tmp/.git có mặt; /var/tmp read-only; không có check-run offline | KHÔNG ĐO ĐƯỢC, không quy hồi quy |

### F01-harness-cung-qualname-van-cap-tin-dung [P1] F01 cũ chưa đóng: tên đầy đủ vẫn được dùng như danh tính lớp

TEP/DONG: `.claude/dev/launcher_test.py:14619`, `:14623` ghi `type(e).__qualname__`; `:14584`–14586 coi chuỗi `TinHieuChotCa` là giết. Ca hồi quy `:10047` chỉ dùng lớp local có qualname dài.

VAN DE: Khi `isinstance` sai, reporter vẫn ghi qualname vào cùng trường semantic với tín hiệu thật. Một lớp độc lập ở module scope hoặc sinh bằng `type` có qualname đúng `TinHieuChotCa` được receiver nhận là chốt. Lỗi có thể là RuntimeError hay AssertionError không thuộc lớp suite. Comment “danh tính lớp THẬT … lớp khác trùng tên không qua” và lời khai ee23c44 vì vậy rộng hơn hành vi. Neutral xanh và sửa cả hai nhánh __name__ trong mutant mới chưa khóa được đường này.

DA THU NGHIEM: `python3 -B ../evidence/probe_runner.py`, runner HEAD thật, chỉ đột biến bản sao và có neutral target PASS:

```text
review_same_name_runtime     OK  giet 1/1: review_target
same_name_runtime accounting (0, 0)
review_same_name_assert      OK  giet 1/1: review_target
same_name_assert accounting (0, 0)
review_real_assert           OK  giet 1/1: review_target
```

Không đổi lớp thật của suite. Hai exception giả chỉ cùng tên; real assertion vẫn là đối chứng dương. HINT `r1079_review_lop_khac_cung_qualname_khong_la_chot` đỏ bằng TinHieuChotCa của chính ca.

DO TIN: cao. Hướng vá: truyền kết quả `isinstance` bằng trường semantic riêng; tên/qualname chỉ dùng chẩn đoán, không được chuyển ngược thành kết luận identity. Khóa cả lớp module-scope/dynamic và lớp local, giữ own assertion và unrelated exception. Không cung cấp bản vá runtime trong hint.

### F04-kenh-ket-qua-gia-truoc-main [P1] Module đang bị đột biến biết cả đường kênh và nonce trước khi runner gỡ env

TEP/DONG: `.claude/dev/launcher_test.py:14573`–14586; `main:14757` chỉ pop hai biến sau khi module đã khởi tạo.

VAN DE: Nonce được truyền cho chính tệp harness đang bị đột biến ngay từ lúc interpreter khởi chạy. Mã module-level chạy trước main có cả nonce và đường ghi, nên có thể tạo record đúng tên, `hong=1`, `loai=TinHieuChotCa`, rồi thoát. Receiver chỉ kiểm hai chuỗi định danh và trường loại; target không cần chạy hay ném assertion. Đây là đường giả kết quả trong mutation harness, không phải giả định attacker ngoài máy hoặc đọc credential.

DA THU NGHIEM: `python3 -B ../evidence/probe_runner.py`. Neutral cùng tệp có `review_target: pass` qua; mutant thêm initializer đọc **chỉ hai biến LT của fixture**, ghi record trơ rồi `SystemExit(1)` trước main. Full chay_dot_bien HEAD báo:

```text
review_forged_channel        OK  giet 1/1: review_target
forged_channel accounting (0, 0)
```

`probe_oracles.py` còn đo record có hong=1/rc=0 hoặc counts mâu thuẫn vẫn nhận giet, record chỉ đúng nonce+tên nhưng thiếu counts nhận qua. Việc gỡ env **trong ca** đã được đối chứng là có thật; nó không bảo vệ giai đoạn khởi tạo module. HINT tương ứng đỏ đúng TinHieuChotCa.

DO TIN: cao đối với đường initializer đã chạy. Hướng vá: đặt phần nắm nonce, chạy ca và ghi kết quả trong runner tin cậy không nằm trong nguồn đang mutation; gỡ dữ liệu kênh trước khi tải nguồn đó. Kiểm schema, số ca/kết quả và rc nhất quán, nhưng không coi chỉ kiểm schema/rc là đã chặn được record giả hợp lệ. Không tuyên bố cô lập an ninh hoàn toàn Python cùng process; cần chốt ranh giới nguồn nào được mutation và nguồn nào làm chứng cứ.

### F05-assertion-ca-khac-bi-ghi-thanh-ca-dich [P1] Cả ba điểm chấm thiếu nguồn gốc assertion theo ca

TEP/DONG: `.claude/dev/launcher_test.py:172`–173 (`cham_mot_ca`), `:14619`/`:14774` (reporter gán tên target); `.claude/dev/codex_cred_test.py:38`–48, `:580`, `:600`.

VAN DE: Product nhận mọi TinHieuChotCa lan tới target; harness gắn tên target vào kết quả tương tự. Credential kiểm tệp/dòng assert nhưng không kiểm assertion thuộc ca nào. Khi mã gọi của target đi vào **một ca khác đã đăng ký**, assertion của ca ấy vẫn được ghi thành kill target. Kiểm tên target ở kênh chỉ kiểm nhãn reporter tự đặt, không kiểm nguồn chốt. SPEC M4 cho phép cách kiểm tệp hiện tại; phép đo này cho thấy nó chưa đáp ứng bảo đảm đúng ca của M7, yêu cầu phản chứng ca KHÁC trong PROMPT và doctrine tại CLAUDE.md. Không đề nghị loại bỏ helper `bang` dùng chung.

DA THU NGHIEM: `python3 -B ../evidence/probe_origin.py`; `python3 -B ../evidence/probe_oracles.py`:

```text
PRODUCT origin accounting (0, 0) ... OK giet 1/1: review_target
HARNESS other_case_assert ('giet', 'review_target')
CREDENTIAL origin neutral [] credited_target False
CREDENTIAL origin other_assert ['t2_chua_thay_thi_tra_None_khong_doan'] credited_target True
OTHER assertion trace ['wrong', 't1_doc_duoc_url_va_ma_tu_dau_ra_that']
```

Product/harness có neutral target xanh; mutant chuyển sang gọi ca khác. Credential dùng chay_suite và **t2 thật**, callback triển khai gọi **t1 thật** với dữ liệu trơ; assertion nằm ở t1, tập đỏ vẫn đúng tên t2. Ba ca HINT tương ứng đều đỏ đúng TinHieuChotCa của chính ca mới.

DO TIN: cao. Hướng vá: neo tín hiệu vào identity ca đang được đo, kiểm nguồn phát/traceback và không nhận chốt từ ca đã đăng ký khác. Giữ khả năng dùng helper chung và đo đối chứng kill thật để không chặn oan. Cách kiểm đúng tệp/loại hiện tại vẫn có giá trị nhưng chưa đủ để suy đúng target.

### F06-ca-dich-vang-bi-xoa-khoi-mau-so [P1] Nhánh product bỏ mất target chưa chạy rồi vẫn có thể báo OK

TEP/DONG: `.claude/dev/launcher_test.py:14378`, `:14386`–14390; `ket_luan_mutant:191`–195.

VAN DE: Runner lọc phai_chet thành các fn tìm thấy, rồi truyền **danh sách đã lọc** vào ket_luan_mutant. Target mất/đổi tên không còn được tính vào mẫu số. Nếu mất hết, runner khai skip theo nền dù không ca nào chạy hoặc tự skip; nếu chỉ mất một phần, những target còn lại đủ làm mutant OK. Base giữ mẫu số từ phai_chet nên báo SAI. Đây là thay đổi ngoài luật bỏ qua theo nền phải giữ của M1/M2. Bảng HEAD hiện tại không có target thiếu; finding là hành vi fail-open của bộ chấm mới khi danh sách ca và metadata lệch.

DA THU NGHIEM: `python3 -B ../evidence/probe_wiring.py`, một mutant hợp lệ và target trơ; cùng dữ liệu trên base/HEAD:

```text
HEAD MISSING TARGET accounting (0, 1) ... KHONG DO DUOC tren nen nay (ca dich bo qua: )
BASE MISSING TARGET accounting (1, 0) ... SAI giet 0/1
HEAD PARTIAL MISSING accounting (0, 0) ... OK giet 1/1: real_target
BASE PARTIAL MISSING accounting (1, 0) ... SAI giet 1/2: real_target
```

Ca còn lại thực sự ném chốt của mình, không dùng unrelated error. HINT missing-target đỏ bằng TinHieuChotCa của chính ca mới.

DO TIN: cao. Hướng vá: kiểm tập target yêu cầu khớp tập tìm thấy trước neutral/mutant; thiếu hoặc trùng phải tính hỏng, in rõ tên. Chỉ tạo skip khi có chứng cứ ca tự bỏ qua hoặc gioi_han nền đã khai. Giữ phai_chet làm nguồn mẫu số và đối chứng partial/all-missing riêng với all-skip/mixed thật.

### F07-khoa-neutral-chi-do-chuoi-nguon [P2] Ca khóa neutral vẫn sống khi hành vi bị gỡ nhưng văn bản được giữ

TEP/DONG: `.claude/dev/launcher_test.py:10004`–10013; hai mutant neutral `:14296`–14303.

VAN DE: F03 cũ đã được sửa thành ca credential đo hành vi. Tuy nhiên ca khóa điểm nối neutral (a)/(b) vẫn dùng inspect.getsource/count. Nó không đo neutral được gọi, module gốc được dùng, cache hay accounting khi neutral đỏ. Bỏ câu thực thi rồi giữ chính chuỗi ấy trong literal không thực thi của runner đủ để khóa này xanh. Hai mutant đang đăng ký xóa luôn văn bản nên không bộc lộ giới hạn. HEAD hiện tại thực thi neutral đúng; finding này là chốt M7 chưa đủ răng, không nói HEAD đã bỏ neutral.

DA THU NGHIEM: `python3 -B ../evidence/probe_wiring.py`, bản sao ngoài cây:

```text
NEUTRAL WIRING LOCK SURVIVED
MUTANT RED NEUTRAL accounting (0, 0) ... OK giet 1/1: review_target
```

Đã đổi neutral thành kết quả qua giả, giữ đoạn cũ trong literal ngay trong chay_dot_bien; khóa hiện có không đỏ, sau đó runner thật trên mutant cấp kill dù target đã đỏ từ neutral. HINT meta-regression `r1079_review_khoa_neutral_phai_do_hanh_vi` đỏ đúng TinHieuChotCa của chính ca.

DO TIN: cao. Hướng vá: chuyển khóa sang gọi runner thật với ca trơ có dấu đếm, hai mutant cùng target, neutral lỗi/chốt, và kiểm `(hong,khong_do)`; làm tương tự cho (b). `probe_neutral_runner.py` cung cấp phép đo hành vi đã chạy. Có thể giữ kiểm văn bản làm lớp phụ, không dùng nó thay chứng cứ thực thi.

## HINT và kiểm toàn vẹn cuối

`HINT.patch` dùng `patch -p0` từ gốc `cay-kho/`. **Chưa áp/chạy trên cây thật — executor tự dẫn xuất, tự đo và chịu trách nhiệm commit.** Patch chỉ thêm 7 ca phản chứng; hướng thay bộ chấm mô tả bằng lời ở findings. Đã dry-run rc=0 và chạy trên bản sao: **7/7 ca đỏ bằng TinHieuChotCa của chính ca**, không lấy FileNotFoundError/AttributeError vô can làm răng. Chưa có triển khai hậu vá để khẳng định các ca này xanh hay có mutant hồi quy đầy đủ sau vá.

`python3 -B ../evidence/summarize.py` xác nhận: counterfactual 46 SAI=36 neutral+10 tín dụng giả; 36 tên neutral trùng HEAD; 18/18 outcomes của 17 mutant mới đúng lớp chốt. Final integrity kiểm **10.161 tracked blobs**: không có khác biệt chưa giải thích; ba `.cmd` dùng CRLF đúng `.gitattributes`, nội dung chuẩn hóa khớp HEAD. `git status --porcelain` rỗng, exact HEAD không đổi. Bằng chứng ở `evidence/final-integrity.json`, `summary.log`, cùng log lệnh tương ứng. Không có thay đổi vào `cay-kho/`.

Đây là review 2/2 cuối. Không kết luận approve từ CI chưa đo được hoặc từ con số base 522/522 vốn dùng bộ chấm đang bị thay. Các finding nêu trên là phản chứng cục bộ có neutral/đối chứng rõ ràng, tách khỏi bẫy môi trường.
