verdict: changes_requested
reviewed_sha: c5acb701ead28ecea076d3f278a71c40ddd894e6
spec_sha256: 81070fa2c5a00bc0bb63867c7173f310cba9002001b68a26d62726ec904cbf5b
Ket qua: 0 P0, 1 P1, 0 P2, 0 P3.

F08 chưa đóng ở đường gán trực tiếp `CA` của launcher: ca trùng mã vẫn chạy và chốt của chính target bị loại. F09 đã được đính chính. Các lỗi gate do môi trường được tách khỏi finding này.

Reviewer: Codex, provider `openai_codex`, execution_surface `codex_service`, transport `machine` (công cụ shell cục bộ trong môi trường quản lý; không gọi CLI Codex để suy danh tính). Model ID cụ thể và lịch sử identity/authority bên ngoài: KHÔNG ĐO ĐƯỢC độc lập. Executor theo assignment là Claude; lease được chỉ định `wp1079-r1-g6-claude`, review_class sensitive, lượt 5/5. Không nâng trần hoặc phát sinh lượt reviewer khác.

## Nhật ký tăng dần

Các đoạn sau được ghi trong khi đo; các bảng bên dưới là kết luận cuối.

Đang đo. HEAD/tree: c5acb701ead28ecea076d3f278a71c40ddd894e6 / 44179f7d5bcd7de5b53f859eda942a6fa8bb2f69; worktree ban đầu sạch. `/tmp/.git` hiện hữu (thư mục read-only), sẽ đối chiếu BASE cùng điều kiện, không coi lỗi storage do môi trường là hồi quy.

Đã chạy trước: `python3 -B ../review5/common.py prior.py` từ `cay-kho/` (script nằm ngoài kho; khi chạy từ gốc dùng `python3 -B review5/common.py prior.py`). 17/17 ca r1079 hiện có PASS. Launcher 347 ca / 347 code object riêng; credential 18/18, tổng 365. Không có ca hợp lệ hiện có bị cấm trùng mã. F09 đã được đính chính trong commit HEAD, AST xác nhận 4 tên mutant mới của 5548919. Log: `review5/prior.log`.

Đang kiểm thêm: gán trực tiếp CA=[target, alias] cùng factory không bị từ chối; runner chạy neutral rồi nhận chính assertion target thành `chot cua ca khac`, in `SAI giet 0/1`, trả `(1,0)`. Cần kiểm đường harness và đối chứng gán CA của credential trước khi chốt finding.

Cập nhật phản chứng độc lập (`review5/oracles.log`): nhánh a/b đều loại AttributeError, AssertionError đổi kiểu, bare AssertionError, chốt từ ca khác và lớp giả cùng qualname; own assertion được tính 1/1, neutral đỏ làm cổng đỏ, all-skip `(0,1)`, mixed `(0,0)`. Cache a chạy neutral đúng một lần với hai mutant. Harness gán CA trực tiếp cùng factory: neutral `('qua','review_target')`, mutant own assertion `('loi','review_target(khac:TinHieuChotCa)')`. Credential CA trực tiếp cùng code bị ValueError trước thực thi. Vì thế đường gán CA của launcher là lỗ hổng chưa đóng F08, không chỉ là thiếu test.

F02 A/B (`review5/fixture.log`): cùng cha thù địch, BASE ca PASS nhưng có 7 lời gọi installer shim + 2 lần init dùng HOME cha; HEAD ca PASS với 0 installer/init môi trường, cả hai probe Bash và hook dùng HOME fixture, không BASH_ENV/ENV/BASH_FUNC. Npm giả vẫn đứng trước chuan-bi. Không gọi installer thật.

Khóa hiện có: 23 mutant wp1079 / 26 target đều chết bằng TinHieuChotCa của đúng target (`review5/locks.json`); đã kiểm traceback độc lập, không lấy headline làm nguyên nhân. Audit diff: 697 dòng thêm, đúng 2 tệp; 33 commit trong BASE..HEAD gồm 8 packet và 25 master/merge. Ruff F 5→5 (đều F841), delta 0; doctrine-scan rc0 cả hai; diff-check rc0. Receiver/main của nợ #1117 có AST thực thi không đổi so 5548919, không tính lại finding đã nhận nợ.

## Cách chạy, phạm vi và cách tìm lời khai

Tất cả lệnh `python3 -B ../review5/common.py <script>.py` trong các bảng chạy được từ `cay-kho/`. `common.py` chuyển sang môi trường tối thiểu do reviewer dựng: PATH công cụ cục bộ, HOME scratch, locale, `PYTHONDONTWRITEBYTECODE=1`, `PIP_NO_INDEX=1`, `PIP_DISABLE_PIP_VERSION_CHECK=1`, cấu hình Git trơ. Không truyền credential của cha; không đọc giá trị credential. Không gọi mạng, push, cài gói hoặc sửa cây review. Các script chỉ dùng assertion, marker trơ, installer shim và fixture có sẵn. Hướng cần nội dung credential hay payload nhạy cảm chỉ giới hạn mô tả, không tự soạn.

HEAD checkout detached, kho không shallow; HEAD/tree khớp assignment. `SPEC.md` tự băm được `81070fa2c5a00bc0bb63867c7173f310cba9002001b68a26d62726ec904cbf5b`. `diff.patch` khớp byte với `git diff BASE HEAD -- .claude`; numstat 49/7 ở credential và 648/111 ở launcher, tổng **697 dòng thêm**. Trần 720 và lượt 5 được assignment cho phép, không tính finding.

Cách tìm tránh chỉ lập danh sách theo trí nhớ: `audit.py` duyệt mọi hunk `@@` và ghi đủ 697 dòng thêm kèm tệp/số dòng vào [claims-all-added-lines.tsv](review5/claims-all-added-lines.tsv); đã đọc các hunk assertion/helper/fixture/khóa/mutant/runner/reporter. Đồng thời duyệt **toàn bộ** `git rev-list BASE..HEAD`, lấy toàn `%B` và đường dẫn mỗi commit: **33 commit = 8 packet + 25 master/merge**. Toàn văn ở [commits.txt](review5/commits.txt), phân loại ở [commit-inventory.json](review5/commit-inventory.json). `claim_history.py` dùng AST so tập tên ca, tên và nội dung từng mutant với cha trực tiếp của cả 8 commit packet. Bảng đo nhóm các khẳng định có cùng phép kiểm; inventory đầy đủ không tự chứng minh mọi lời khai lịch sử. Thẩm quyền chủ kho, provenance HINT gốc không có tệp gốc đi kèm, CI/check-run và số chạy trên máy executor được ghi KHÔNG ĐO ĐƯỢC, không coi lời khai trong Git là bằng chứng chạy độc lập.

Các log đều tạo mới trong lượt này. Không lấy kết quả của VERDICT các lượt trước làm kết quả hiện tại. BASE được xuất bằng `git archive` ra scratch; các phép phản chứng nội dung dùng bản sao ngoài `cay-kho/`. BASE archive không có `.git` ở gốc, nên đối chứng full suite chỉ là chẩn đoán môi trường; đã so tập lỗi/skip thực tế thay vì suy tương đương mọi trạng thái Git. Finding F08 dùng các ca trơ không cần repo hoặc storage, có neutral dương riêng.

`ls -ld /tmp/.git` xác nhận thư mục read-only hiện hữu; không xóa hoặc thay quyền. Hai ca khác không ghi được `/var/tmp`; `t53` thiếu CLI claude/codex trong môi trường tối thiểu. Các lỗi storage/materializer/run phụ thuộc chúng có ở cả BASE và HEAD. A1 đòi `/tmp/.git` vắng nên **không đo được dưới tiền đề nghiệm thu**. Không gọi những lỗi này là hồi quy.

## Đối chiếu findings cũ — đã chạy trước khi thử hướng mới

| Finding/lớp | Lệnh và bằng chứng HEAD hiện tại | Trạng thái |
|---|---|---|
| Lượt 4 F05, lượt 2 F05: assertion ca khác | `prior.py`, `oracles.py`: other khác code bị loại ở a/b/c; ca cùng factory qua `ca` bị ValueError, credential CA trực tiếp cũng ValueError; ca product cùng factory gọi other qua CA trực tiếp trả `(1,0)` | Đã vá biểu hiện nhận tín dụng giả. Lời khai từ chối cấu trúc mọi đường chưa đúng, xem F08 |
| Lượt 4 F09: commit đếm 5 thay vì 4 | `prior.py`, `claim_history.py`: 5548919 thêm đúng 4 tên và sửa 3 hàng; `%B` HEAD đính chính rõ cả F09 và câu sai của 5368c34 | Đã đóng; không tính lại lịch sử đã đính chính |
| Lượt 3 F08: own assertion cùng factory | `prior.py`, `oracles.py`, `make_hint.py`: `ca` và credential runner từ chối; launcher CA trực tiếp vẫn chạy, own assertion bị coi là other | **Chưa đóng ở đường CA trực tiếp**, cùng slug F08 bên dưới |
| Lượt 2 F01 / lượt 1 F01: lớp giả, qualname, stdout | `oracles.py`: lớp RuntimeError cùng qualname → loi; stdout LOAI_HONG/headline rồi thoát → loi, không có kênh; `locks.py`: mutant bỏ tiền tố/nonce/identity chết đúng ca | Đã vá phần đã đo |
| Lượt 2 F06: target thiếu/trùng | `extra.py`: all-missing, partial-missing, duplicate-name đều `(1,0)` | Đã vá nhánh product; không đánh tráo việc kiểm tên thành kiểm code |
| Lượt 2 F07: khóa neutral chỉ đọc chuỗi | `prior.py`, `locks.py`: bỏ thực thi, giữ literal vẫn làm khóa đỏ bằng tín hiệu của chính ca; neutral a/b đỏ làm cổng đỏ | Đã vá |
| Lượt 1 F02: dò Bash kế thừa init/HOME | `fixture.py`: HEAD 0 init/installer; 2 probe Bash và hook cùng HOME fixture, không BASH_ENV/ENV/BASH_FUNC | Đã vá |
| Lượt 1 F03: khóa credential chỉ tìm chuỗi | `oracles.py`, `locks.py`: chạy chay_suite thật; thay câu thực thi, giữ lời gọi trong comment vẫn OWN_SIGNAL | Đã vá |
| Lượt 2 F04 | `audit.py`: AST thực thi `main` và `cham_lap_ca` không đổi so 5548919; docstring vẫn khai giới hạn module trước main | Nợ #1117 đã được chủ kho nhận theo assignment; không tính finding chặn và không thấy bản vá làm nợ tệ hơn |

Quét runtime **347/347** ca launcher và **18/18** ca credential có code object riêng. Con số 345 của prompt là số ở head cũ; HEAD thực tế có 347 ca launcher, trong đó 2 ca chỉ dành cho Windows. Không có bằng chứng cấm nhầm một trong các ca đăng ký hiện có. F08 là phản chứng đường CA trực tiếp, không lấy 24 lỗi nền làm chứng cứ.

## BANG NGHIEM THU

| Tiêu chí | Lệnh từ cay-kho/ | Output thật | Đạt? |
|---|---|---|---|
| M1: a chỉ nhận tín hiệu, lỗi khác có loại, giữ skip | `python3 -B ../review5/common.py oracles.py` | own `OK giet 1/1`; AttributeError/wrapped/bare AssertionError/other đều `SAI giet 0/1`, in loại; all-skip `(0,1)`, mixed `(0,0)` | Đạt phần phân loại đo được; F08 còn chặn nhầm registry trực tiếp |
| M2: neutral a/b, cache, đỏ đóng cổng | Cùng lệnh; `python3 -B ../review5/common.py extra.py` | a/b neutral đỏ `(1,0)`; cache a `[True,False,False]`, cache b `['0','1','1']` cho 2 mutant | Đạt các đối chứng |
| M3: b nhận nguyên nhân từ kênh | `oracles.py`, `legacy.py`, `locks.py` qua common.py | HEAD AttributeError `(1,0)`, fake stdout không kênh → loi; own `(0,0)`; mutant bỏ nonce/identity chết đúng chốt | Đạt đường hợp lệ đã đo; F08 raw CA, nợ #1117 tách riêng |
| M4: c đúng lớp/tệp/assert, không nhận lỗi đổi kiểu | `oracles.py`, `extra.py` qua common.py | own bare assert → `{t2}`; lỗi implementation/wrapped → `{t2(AssertionError)}`; other → suffix; tệp khác cùng dòng assert bị loại | Đạt phần cục bộ, kể cả từ chối CA trùng code trước chạy |
| M5: 11 mutant cũ bằng chốt đúng ca | `python3 -B ../review5/common.py historical.py` | Trên ca HEAD: **10 OK**, 1 neutral đỏ recovery storage; `(1,0)` | 10 đo được đạt; 1 KHÔNG ĐO ĐƯỢC do `/tmp/.git` |
| M6: fixture N13 kín, giữ npm trước materialize | `python3 -B ../review5/common.py fixture.py` | BASE PASS/7 installer + 2 init cha; HEAD PASS/0; npm trước chuan-bi ở cả hai; HOME/init/function được lọc ở toàn bộ bước Bash HEAD | Đạt cục bộ |
| M7: khóa hành vi + mutant từng chốt, own assertion, registry | `prior.py`, `locks.py`, `make_hint.py`, `prototype.py` qua common.py | 17/17 khóa hiện có PASS; 23 mutant/26 target OWN_SIGNAL; 2 khóa mới F08 OWN_SIGNAL trên HEAD | **Chưa đạt đầy đủ**: khóa mới phơi đường CA trực tiếp còn mở |
| A1: ba gate dưới `/tmp/.git` vắng | `python3 -B ../review5/common.py suites.py head` (thực gọi đúng 3 lệnh SPEC) | 313/337, 509/545, credential 13/18; cả 3 rc1. BASE 296/320, 522/522, 13/18 | KHÔNG ĐO ĐƯỢC dưới tiền đề chuẩn; không coi gate là xanh |
| A2: scorer HEAD trên ca BASE; khóa đỏ trên scorer/fixture BASE | `historical.py`, `legacy.py`, `fixture_base_lock.py` qua common.py | 446 hàng product BASE: 397 OK, 34 neutral đỏ, 11 SAI, 3 giới hạn nền, 1 all-skip. Legacy a/b AttributeError vẫn OK, c `{t2}`; khóa neutral/c và hậu điều N13 đỏ đúng tín hiệu | Đạt phản chứng đã đo; không xác nhận đúng toàn bộ 11 tên SPEC dưới tiền đề chuẩn |
| A3: A/B installer logging | `fixture.py` qua common.py | 7→0 installer môi trường; 2→0 init; tất cả installer đều shim thoát 97 | Đạt |
| A4: ruff delta, diff-check, doctrine, CI | `python3 -B ../review5/common.py audit.py` | Ruff 5 F841→5 F841, delta0 (hai rc1 nền); diff-check rc0; doctrine-scan rc0 hai phía/10 tệp/0 vi phạm | Gate local đạt; check-run CI exact HEAD KHÔNG ĐO ĐƯỢC vì cấm mạng |

A2: trong 11 SAI thực đo, **10 tên thuộc SPEC**, cộng `PROMPT_FILE_mo_coi_di_tiep`: r13 BASE gọi ca t70 đã đăng ký nên bị chốt nguồn gốc hiện tại loại. Tên SPEC còn lại `g2_rejected_refresh_khong_phu_thuoc_metadata` bị neutral storage đỏ, cùng 33 neutral đỏ khác. Không dùng số tổng 11 để khẳng định đủ đúng 11 tên. Trên HEAD, r13 và t70 đã dùng helper chung: `extra.py` đo mỗi ca giết mutant thật 1/1, đều `(0,0)`.

## BANG DO

| Khẳng định | Diff/commit khai | Đo được bằng lệnh qua common.py | Khớp? |
|---|---|---|---|
| Scope/dòng thêm | 2 tệp test, dưới trần đã nâng | `audit.py`: diff byte-equal, 697 dòng thêm; numstat 49/7 + 648/111 | Có |
| Chỉ TinHieuChotCa là kill a; converted AssertionError không qua | cham_mot_ca/docstring | `oracles.py`: own OK, AttributeError/converted/bare/other SAI kèm loại; `legacy.py` A/B | Có trong registry code riêng; F08 là false rejection raw CA |
| Neutral đúng bản gốc, một lần/target, fail-close | runner a/b và ket_luan_mutant | `oracles.py`, `extra.py`: 1 neutral + 2 mutant; neutral đỏ `(1,0)` | Có các đối chứng hành vi |
| Skip giữ all/mixed và giới hạn nền | runner/ket_luan_mutant | `oracles.py`, `extra.py`, `summarize.py`: a/b all `(0,1)`, mixed `(0,0)`; 4 mutant nền giống BASE | Có phần đã đo |
| Headline/LOAI_HONG stdout không làm chứng cứ | cham_lap_ca, ee23c44 | `oracles.py`: fake tail/SystemExit → không kết quả kênh, SAI; `locks.py`: restore stdout fallback bị khóa | Có; không suy thành chống module giả kênh |
| Identity thật và tiền tố khac | reporter, 5548919 và correction | `prior.py`, `oracles.py`, `locks.py`: cùng qualname không qua, bỏ tiền tố/identity làm đúng target đỏ | Có |
| Assertion của ca KHÁC không nhận | chot_tu_ca_khac/ten_do | `oracles.py`, `prior.py`: a/b/c loại other; CA code trùng ở credential từ chối | Có biểu hiện tín dụng giả cũ; chặn nhầm raw CA launcher còn F08 |
| Ca cùng code đã bị cấm từ cấu trúc | ca, khóa mới và `%B` HEAD | `prior.py`: decorator ValueError, raw CA runner vẫn thực thi target 2 lần; `oracles.py`: own assertion bị loại ở a/b | **Không**, F08; không tách lời khai này thành finding nữa |
| Không có ca hiện có dùng chung code | `%B` HEAD, quyết định cấm ca | `prior.py`: 347/347 launcher,18/18 credential riêng code | Có ở HEAD; không chứng minh mọi kiểu ca tương lai |
| Thiếu/trùng target làm cổng đỏ | F06/%B 5548919 | `extra.py`: all-missing/partial/duplicate-name `(1,0)` | Có ở a |
| Credential đúng tệp, dòng assert, kiểu lỗi | la_chot_cua_suite/docstring | `oracles.py`, `locks.py`: tệp khác cùng dòng assert bị loại; bỏ từng check làm khóa đỏ | Có trong các đối chứng |
| Credential runner dùng classifier thực | chay_suite + khóa behavior | `oracles.py`, `locks.py`: lỗi không khớp `{t2}`; giữ comment nhưng thay thực thi → OWN_SIGNAL | Có |
| 11 mutant được sửa fixture/assertion | r01/r10/t115 và 3 ca đổi assert | `historical.py`:10/11 tên OK đúng chốt, recovery neutral OSError | Khớp 10 đo được; 1 KHÔNG ĐO ĐƯỢC |
| r13 không gọi registered t70 | helper mới, 7df242e | `extra.py`: r13 và t70 mỗi ca riêng OK 1/1 | Có |
| Bản sao harness giữ bố cục/dependency | _dung_cay_harness và `%B` c73dff3/c5acb70 | `locks.py`:26/26 target đúng chốt; N13 và khóa nạp CC chạy được; full mutation không còn FileNotFound trung tính ở các target này | Có phần phụ thuộc được chạy; không suy thành sao toàn repo |
| Mọi installer trong fixture, không đọc init/HOME cha | N13 comment và env | `fixture.py`: HEAD0 so BASE7 installer+2init; 3 subprocess HEAD có HOME fixture và 3 cờ init/function false | Có hướng được đo |
| Mỗi chốt wp1079 có mutant giết đúng ca | bảng mutant/comment | `locks.py`:23 mutant/26 target OWN_SIGNAL, traceback có target, không có registered other | Có với các mutant đăng ký; chưa khóa raw CA |
| Khóa neutral không chỉ tìm source | khóa behavior/F07 | `prior.py`, `locks.py`: bỏ thực thi, giữ literal vẫn làm khóa đỏ đúng lý do | Có |
| 5368c34 bỏ phép trừ, F05/F08 đã giải quyết | lời khai lịch sử, correction HEAD | `claim_history.py`, `prior.py`: phép trừ đã bỏ, 3 khóa/2 mutant F08 cũ đã gỡ, 2 khóa/2 tên mutant mới được thêm; F05 bị nhận trước đây đã đính chính | Phần Git khớp; tuyên bố đóng toàn F08 chưa khớp raw CA |
| 5548919 thêm 5 mutant | message lịch sử | `claim_history.py`:4 tên mới,3 hàng sửa; HEAD đính chính đúng | Lời cũ sai nhưng đã correction, F09 đóng |
| 2 mutant mới c5acb70 giết đúng ca | `%B` HEAD | `claim_history.py`, `locks.py`: wp1079_ca_cho_trung_ma và wp1079_cc_cho_trung_ma đều OWN_SIGNAL | Có |
| Nonce chống ca giả, không chống initializer giả kênh | docstring giới hạn/nợ #1117 | `audit.py`: main/cham_lap_ca AST thực thi không đổi so5548919; kiểm stdout giả vẫn đỏ | Giới hạn còn nguyên, không đẩy thành finding đã nhận nợ |
| Kết quả lịch sử 531/536,538/539,541/543; HINT hash, identity, session/owner/CI | 8 packet messages | `claim_history.py` kiểm được tập ca/mutant và correction; không có rig/log/check-run lịch sử độc lập để chạy lại các số cũ | KHÔNG ĐO ĐƯỢC lịch sử, không tự chứng thực từ message |
| 25 commit master/merge, các claim spec/land/CI khác | toàn `%B BASE..HEAD` | `audit.py`: đủ OID/path/message trong inventory; nội dung ngoài `.claude` là master theo scope assignment; không gọi GitHub kiểm check-run/approval hoặc thực thi packet khác | Git inventory đo được; claim vận hành ngoài packet KHÔNG ĐO ĐƯỢC độc lập |

## BANG TEST

| Bộ/lệnh thực chạy | N/M, rc | Bỏ qua / không đo được |
|---|---|---|
| HEAD `python3 .claude/dev/launcher_test.py` | **313/337** ca đã chạy qua; tổng347,24 đỏ; rc1 | **10 BO QUA**:2 Windows-only +8 venv/pip offline |
| BASE cùng lệnh qua suites.py | **296/320**; tổng330,24 đỏ; rc1 | Cùng 10 tên/lý do skip; tập24 tên lỗi bằng HEAD |
| HEAD `python3 .claude/dev/launcher_test.py --dot-bien` | **509/545**, rc1; tổng549 | 4 KHÔNG ĐO theo nền;36 SAI đều neutral đỏ, không cấp tín dụng |
| BASE cùng lệnh | **522/522**, rc0; tổng526 | 4 không đo theo nền; đây là headline scorer cũ có tín dụng giả, không phải chứng cứ neutral xanh |
| HEAD `python3 .claude/dev/codex_cred_test.py` | Nền **13/18**, `TỔNG: ĐỎ`, rc1 | 5 đỏ,0 skip; dừng trước mutation |
| BASE credential | Nền **13/18**, `TỔNG: ĐỎ`, rc1 | Cùng5 tên, HEAD thêm loại lỗi |
| Credential từng target neutral/mutant, độc lập với main | **13/13 OWN_ASSERTION** đo được | 5/18 target NEUTRAL_BLOCKED; không thay thế gate chính thức |
| Khóa hiện có r1079 | **17/17 PASS** | Chạy trước; không lấy test mới của reviewer vào mẫu số này |
| Mutant wp1079 trên bản sao | **23/23 mutant,26/26 target OWN_SIGNAL** | Có kiểm traceback độc lập theo ca |
| Scorer HEAD + ca product BASE | 446 hàng: **397 OK,34 neutral đỏ,11 SAI,4 skip** |4 skip=3 giới hạn nền+1 target tự skip; không báo đủ11 tên SPEC |
| 11 mutant SPEC trên ca HEAD | **10 OK**,1 neutral đỏ | Recovery storage không đo được |
| Hai ca HINT mới trên HEAD | **2/2 OWN_SIGNAL** | Chính target test ném TinHieuChotCa, không chết do dependency/AttributeError |
| Prototype kiểm registry ở main/runner, chỉ ngoài cây |2/2 khóa mới PASS; bỏ mỗi guard →1/1 khóa tương ứng OWN_SIGNAL | Chỉ minh họa hướng sửa, không là full regression của một bản vá đã hoàn tất |
| Ruff F / doctrine / diff-check |5→5 F841 delta0 / rc0 hai phía / rc0 | CI exact HEAD không đo vì cấm mạng |

5 ca credential đỏ: `t6_khong_in_gia_tri_khi_khong_co_co`, `t9_cmd_lay_GHI_tep_huong_dan_dan`, `t15_home_chua_tao_la_KHONG_DO_DUOC`, `t16_khong_ghi_duoc_trang_thai_tu_choi_phai_noi_ra`, `t18_kiem_ghi_dung_ban_da_probe`. Không gọi chúng là skip hoặc kill.

10 tên skip đầy đủ,24 tên lỗi và36 mutant neutral đỏ được lưu ở [summary.json](review5/summary.json). Log các gate: [head-launcher.log](review5/head-launcher.log), [head-mutants.log](review5/head-mutants.log), [head-credential.log](review5/head-credential.log), cùng các tệp `base-*.log`. Những lỗi /tmp, /var/tmp, thiếu tool hay con không được materialize không thành finding mới khi BASE cho cùng hiện tượng.

## BANG SAN

| Hướng độc lập | Lệnh từ cay-kho/ | Output thật | Phân loại |
|---|---|---|---|
| 1. Toàn vẹn spec/head/diff và scope | `python3 -B ../review5/common.py audit.py` | DIFF_MATCH True;697 dòng; HEAD đúng;STATUS rỗng | KHÔNG PHẢI LỖI |
| 2. Các đường đăng ký/code identity | `python3 -B ../review5/common.py prior.py` | decorator rejected; direct registry `(1,0)` sau2 lần target;347/347 code riêng | **LỖI F08** ở đường CA trực tiếp, không cấm nhầm ca hiện có |
| 3. Oracle product và đổi kiểu exception | `python3 -B ../review5/common.py oracles.py` | AttributeError/wrapped/implementation assert SAI; own OK | KHÔNG PHẢI LỖI các đối chứng đó |
| 4. Harness channel/stdout/qualname | Cùng lệnh | fake class → khac; stdout tail/SystemExit → không có kênh, SAI; own OK | KHÔNG PHẢI LỖI phần đã đo |
| 5. Credential nguồn tệp/assertion | Cùng lệnh; `extra.py` qua common.py | same-line other file bị loại; own13/13; lỗi implementation và other không khớp target | KHÔNG PHẢI LỖI phần đo được;5 neutral KHÔNG ĐO ĐƯỢC |
| 6. Own assertion bị chặn nhầm | `oracles.py`, `make_hint.py` qua common.py | raw CA harness neutral qua nhưng own mutant loi;2 khóa mới OWN_SIGNAL | **LỖI F08**, không phải neutral đỏ môi trường |
| 7. Neutral/cache và skip a/b | `oracles.py`, `extra.py` qua common.py | neutral đỏ `(1,0)`;1 neutral/2 mutant; all `(0,1)`,mixed `(0,0)` | KHÔNG PHẢI LỖI |
| 8. Target thiếu/trùng tên | `python3 -B ../review5/common.py extra.py` | all/partial/duplicate đều `(1,0)` | KHÔNG PHẢI LỖI F06 cũ |
| 9. N13/installer/init/HOME cha thù địch | `python3 -B ../review5/common.py fixture.py` | BASE7 installer+2init;HEAD0; npm trước chuan-bi | KHÔNG PHẢI LỖI F02 hiện tại |
| 10. Khóa M6 trên fixture BASE | `python3 -B ../review5/common.py fixture_base_lock.py` | OWN_SIGNAL, frames có đúng N13;9 marker ambient | KHÔNG PHẢI LỖI: phản chứng dương cho hậu điều mới |
| 11. Gỡ từng chốt đăng ký | `python3 -B ../review5/common.py locks.py` | TOTAL26 OWN_SIGNAL26,23 mutant | KHÔNG PHẢI LỖI các chốt đăng ký; chưa bao raw CA |
| 12. Legacy runner/11 mutant SPEC | `legacy.py`, `historical.py` qua common.py | BASE a/b lỗi vô can OK,c `{t2}`;HEAD loại;10 SPEC OK/1 neutral đỏ | Lỗi gốc F01 được tái hiện BASE và vá ở HEAD; phần storage KHÔNG ĐO ĐƯỢC |
| 13. Kill thật qua helper r13/t70 | `python3 -B ../review5/common.py extra.py` | Hai ca riêng OK1/1, `(0,0)` | KHÔNG PHẢI LỖI |
| 14. F09/counts/lời khai lịch sử | `python3 -B ../review5/common.py claim_history.py` |5548919 thêm4/sửa3;c5acb70 correction;2 mutant mới | KHÔNG PHẢI LỖI còn mở; lịch sử CI/identity KHÔNG ĐO ĐƯỢC |
| 15. Gate/môi trường và integrity | `suites.py head`, `suites.py base`, `summarize.py` qua common.py |24 lỗi/10skip cùng tập;3 gate HEAD đỏ;10161 tracked files không đổi | Gate đầy đủ KHÔNG ĐO ĐƯỢC theo tiền đề A1; cây review KHÔNG PHẢI LỖI |

### F08-shared-code-khong-phai-ca-khac [P1] Cấm trùng code chưa bao đường gán CA trực tiếp, nên vẫn loại assertion của chính target

TEP/DONG: `.claude/dev/launcher_test.py:58` (`ca` chỉ kiểm khi gọi decorator); `:172` (tập code của other vẫn chứa code của target qua alias); `:14581` (runner chỉ kiểm tên target); `:14805` và `:14829` (consumer/reporter không từ chối registry trùng code). `%B` của `c5acb701ead28ecea076d3f278a71c40ddd894e6` khẳng định F05/F08 đã đóng theo cấu trúc; khóa `r1079_ca_trung_ma_bi_tu_choi_luc_dang_ky` chỉ đo decorator launcher và CA credential, bỏ cửa gán CA launcher.

VAN DE: Hai hàm từ cùng factory, khác tên và closure, gán `CA=[target,alias]` không đi qua `ca`. Đây là một đường sử dụng thật của harness: chính ca mới `r1079_review4_product_shared_template_call_other` thay CA trực tiếp; các ca meta khác cũng dùng pattern này. `chay_dot_bien` vẫn chạy neutral và mutant, không có ValueError/diagnostic registry. Khi chỉ target ném chốt của **chính nó**, `khac` chứa cùng code qua alias nên bị gọi là “chốt của ca khác”. Product báo tín dụng giả/SAI; harness báo `khac:TinHieuChotCa`. Alias không cần được gọi. Quyết định mới của chủ kho là cấm registry này trước chạy; hiện tại chỉ decorator và credential enforce được, vì vậy lời khai “đóng theo cấu trúc” chưa đúng. Không đề nghị khôi phục phép trừ gây F05, không đòi hỗ trợ lại ca bị chủ kho cấm. Yêu cầu là từ chối nhất quán mọi đường trước thực thi, tránh chạy rồi gán sai nguồn chốt.

DA THU NGHIEM:

- `python3 -B ../review5/common.py prior.py` → decorator `ValueError`, nhưng direct CA in `SAI giet 0/1 ... review_target(chot cua ca khac)`, trả `(1,0)`; target được chạy neutral rồi mutant, alias không chạy.
- `python3 -B ../review5/common.py oracles.py` → harness neutral `('qua','review_target')`; chỉ đổi cờ để chính target assert → mutant `('loi','review_target(khac:TinHieuChotCa)')`. Credential cùng kiểu CA bị ValueError trước chạy, chứng minh chỗ khác đã có đúng policy.
- `python3 -B ../review5/common.py make_hint.py` → hai khóa test-only trong `HINT.patch` đều **OWN_SIGNAL** trên HEAD. Khóa product ghi đúng hai lần `review_target`, không alias. Khóa subprocess kiểm cả default/`--lap-ca`/`--dot-bien`; cả ba không từ chối registry trước chạy. Traceback của lỗi khóa gồm chính hàm khóa và `bang`, không có registered other, không phải FileNotFound/AttributeError.
- `python3 -B ../review5/common.py prototype.py` → prototype thêm validator ở main và runner trực tiếp làm **2/2 khóa PASS**; gỡ từng guard làm khóa tương ứng chết **OWN_SIGNAL**, thông điệp đúng đường raw CA. Prototype chỉ nằm ngoài cây; chưa tuyên bố một fix hoàn chỉnh đã qua toàn regression.

DO TIN: cao — có neutral dương, runner thực/subprocess thực và đối chứng credential. Không cần /tmp storage, mạng, credential hay Windows. Không thấy duplicate code trong 347 ca hiện tại; finding là sai hành vi trên đường vào được user yêu cầu kiểm, kèm lời khai đóng cấu trúc sai đo được. Cùng slug F08 của lượt3, không tách thành finding mới để đổi tên lớp.

Gợi ý vá — **ở đâu:** helper kiểm registry dùng chung cho launcher, gọi ở các consumer trước khi chạy ca, bao main/default/lap/harness và lời gọi trực tiếp `chay_dot_bien`; cân nhắc helper trực tiếp nhận CA nếu tiếp tục dùng như API. **Cách vá:** giữ cấm code trùng theo authority, kiểm toàn bộ CA trước neutral/mutant, từ chối có diagnostic code trùng; decorator vẫn kiểm sớm. Không chỉ kiểm danh sách đã lọc target, vì alias không được chọn vẫn gây nhận sai nguồn. Đồng bộ policy với credential runner đang kiểm toàn CA. Cập nhật `r1079_review4_product_shared_template_call_other` để chờ từ chối trước chạy thay vì cố thực thi một registry nay bị cấm. **Ca khóa:** hai ca trong [HINT.patch](HINT.patch); giữ own code riêng/helper r13/t70 dương, registered-other âm, duplicate-name/missing-target, neutral/cache/skip. Mỗi điểm nối validator phải có mutant gỡ chính lời gọi, làm khóa đích đỏ bằng TinHieuChotCa. **Rủi ro:** chỉ vá main sẽ bỏ direct runner; chỉ vá decorator lặp lỗi hiện tại; kiểm mỗi target bỏ alias; kiểm quá rộng vào danh sách lặp của cùng một ca có thể làm hỏng `--lap-ca`; đổi về phép trừ code mở lại F05. Cần chạy lại các meta-test cố ý thay CA và các gate hợp lệ sau sửa.

## HINT và toàn vẹn cuối

[HINT.patch](HINT.patch) là **patch test-only**, `patch -p0` từ `cay-kho/`, gồm hai ca hồi quy ở trên; hướng runtime đã nêu trong finding. Patch chưa áp cây review. `make_hint.py` đã dry-run trên bản sao exact HEAD rc0 và chạy chứng minh cả hai khóa đỏ đúng nguyên nhân. SHA256 patch: `ef61ed87fa61e5c7716d3b91a4047f05d56092cac3f2016a7f7ac2e7a7916c20`.

`integrity-final.json`: **10161/10161 tệp tracked giữ nguyên**, added=[],removed=[],changed=[]; `git status --porcelain` rỗng; HEAD/tree vẫn `c5acb701ead28ecea076d3f278a71c40ddd894e6` / `44179f7d5bcd7de5b53f859eda942a6fa8bb2f69`. Tất cả bản sao, hint, script và log ở ngoài `cay-kho/`. Không push hoặc ghi ứng dụng ngoài. Kết luận chặn là F08 raw CA; không lấy lỗi môi trường, nợ #1117 hay trần đã được cho phép thành finding.
