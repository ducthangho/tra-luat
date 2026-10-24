verdict: changes_requested
reviewed_sha: 19b114867fbcad4c3b580bcbe4367bc78a890773
base_sha: 76cf4c51a6b1a5a0f30621c73f9a6f03e7e68138
Reviewed commit: 19b114867fbcad4c3b580bcbe4367bc78a890773
reviewed_tree: 89972d84767c1ca112f6d3d4bfd2f0a315db9658
packet: wp899-r2-g1
review_round: 4
role: reviewer
provider: openai_codex
model_family: openai
model: gpt-6.1-sol (CLI-published)
effort: xhigh (CLI-published)
session_id: 01a16ca2-73a5-78f0-a227-626249ad6cf2
model_reviewer_identity: openai_codex/gpt-6.1-sol/01a16ca2-73a5-78f0-a227-626249ad6cf2
execution_surface: codex_cli
transport: machine
independent_from_executor_session: true
review_axes: [spec, standards_security]
github_submitter_identity: null
assurance: review_deferred

**Chưa đạt V2: 1 lớp còn mở, 2 nhóm biểu hiện; P0=1, P1=0, P2=0, P3=0.** F01 và F05 đã vá thật trong phạm vi kiểm độc lập. F02 vá được bốn biểu hiện của lượt 3 nhưng vẫn sinh bằng chứng `passed` từ dòng không được thực thi: bộ tách kịch bản tin mã ANSI trong metadata và bỏ qua các dòng không mang màu. Đây là **F02 `nhac-ten-script-thanh-thuc-thi` LẶP LỚP ở lượt 4**, không phải lớp mới. F03/F04/F06 giữ đóng; F07 giữ disposition authority.

**Điều kiện dừng của chủ kho đã chạm.** Áp nguyên quyết định issuecomment-6380890740 được giao trong prompt: “lặp lớp ở lượt 4 thì dừng hẳn”. Không tự mở vòng vá/review tiếp. Kết quả này không cấp approval, assurance `cross_approved`, quyền đẩy, merge, land hay chuyển state. HINT chỉ phục vụ checkpoint/xem lại thiết kế nếu chủ kho quyết định sau đó.

Đã đọc toàn bộ `.review-input/prompt.md` và spec được giao. Phiên chỉ review offline, không gọi subagent, không đăng GitHub, không push và không sửa code ứng viên. Mọi script, log, bản sao và kết quả do reviewer tạo đều trong `.review/`. Các fixture log có phần dựng để phản chứng được ghi rõ dưới đây; không khai chúng là log mới tải từ Actions.

**Preflight, authority và ba mốc.** `.review-input/wp899-r2.md` có **23.189 byte**, SHA-256 **d858c7c65a38a7f0fadda1cabf839c98ce70a881372d847c8979165925971707**, khớp assignment; revision 2/generation 1. Đây là bản spec đóng băng authoritative của review offline; không thay bằng r1 trong product tree. Immutable acceptance baseline là `76cf4c51a6b1a5a0f30621c73f9a6f03e7e68138`; candidate là HEAD/tree ở đầu verdict. Lượt 3 `5ab75a4ca5b237f881a5be9ea97047d3f9395115` chỉ dùng đo delta/đối chiếu, không dời baseline. Không có continuation base riêng được giao.

Origin là `https://github.com/ducthangho/tra-luat.git`; detached HEAD đúng assignment. Baseline tồn tại và phép `git merge-base --is-ancestor <base> HEAD` trả **rc0**. Checkout là **shallow=true**; các object baseline/candidate/lượt 3 và object checkout A10 dùng trong phép đo đều đọc được. Không suy có đầy đủ lịch sử/ref toàn kho từ bản sao này. Lease/state/ref freshness và ngân sách remote **KHÔNG ĐO ĐƯỢC**; áp authority offline được prompt chỉ định, không khai đã xác minh GitHub live.

Áp hai đính chính của chủ kho từ prompt: trần **3 tệp/900 dòng thêm** (issuecomment-6380183334), và A10 là **13 checkout + chuan-bi not_measured**. Quyết định checkpoint cho phép riêng lượt 4 không xóa lịch sử F01/F02/F05. Không dùng trần 700 hoặc kỳ vọng 14 checkout cũ để tạo finding.

`git diff --numstat <base> HEAD` **rc0**: `.claude/dev/ci_dang_ky_test.py` **1/0**, `ops/ci_provenance.py` **359/0**, `ops/ci_provenance_test.py` **539/0**; tổng **899 dòng thêm**, đúng ba tệp write set. Đã đọc toàn bộ hai tệp mới, diff toàn bộ và delta lượt 3. Sổ đăng ký chỉ thêm một mục MOI. `git diff --check <base> HEAD` **rc0**. Bằng chứng: `preflight.json`, `full.txt`, `delta.txt`, `numstat.txt`.

**Runtime và giới hạn identity.** Linux x86_64; Python **3.13.17**, `/usr/bin/python`; PyYAML **6.0.3**; Git **2.43.0**; Ruff **0.15.15**; codex-cli **0.164.0**. `preflight.json` trích metadata của đúng thread từ `/root/.codex/sessions/2026/10/24/rollout-2026-10-24T06-39-10-01a16ca2-73a5-78f0-a227-626249ad6cf2.jsonl`: `session_meta.id` khớp thread môi trường, `originator=codex_exec`, `model_provider=openai`; `turn_context` công bố `gpt-6.1-sol`, effort `xhigh`. Đây là **model/effort do CLI công bố**; model phục vụ từng request **KHÔNG ĐO ĐƯỢC**. Không băm rollout đang ghi rồi gọi đó là receipt A13 cuối. Executor Claude/cloud/model_family=claude là thông tin spec; không có runtime receipt Executor độc lập trong assignment.

Sandbox thực tế `workspace-write`, network_access=false. Read-only đối với candidate là ràng buộc assignment và được đối chiếu snapshot; không tuyên bố OS khóa ghi toàn checkout. `core.abbrev` chưa đặt (**rc1**); không đổi config/trust/bootstrap và không chạy golden/doc-claims phụ thuộc cấu hình ấy. `codex --version` rc0 có cảnh báo không tạo được PATH aliases do filesystem read-only; không sửa quyền. Catalog không có `environment_status`. `doctor/chuan-bi`, mạng, cài dependency và phóng agent khác **not_run** trong assignment offline này.

**Cách tái hiện và receipt.** Từ gốc workspace: `python -B .review/run.py <nhãn> <command...>`. Wrapper đặt `PYTHONDONTWRITEBYTECODE=1`, TMPDIR/cache trong `.review/`; `<nhãn>.receipt.json` giữ command, **rc con thật**, thời gian, size/hash stdout/stderr. Output nguyên văn nằm ở `<nhãn>.stdout.txt/.stderr.txt`. Rc0 của driver chỉ nói thu thập hoàn tất; rc và trạng thái của từng phép thử nằm trong JSON chi tiết. Không đồng nhất fixture Windows, REST mock hoặc replay frozen với Windows/CI/LIVE thật.

**ĐỐI CHIẾU LƯỢT TRƯỚC — F01–F07.** Nguồn chính là `.review-input/VERDICT-luot3.md` trên SHA `5ab75a4ca5b237f881a5be9ea97047d3f9395115`; lịch sử lượt 1/2 cũng được đọc để giữ slug. Script lượt 3 không được giao; đã dựng lại đúng hình dạng phép đo từ mô tả.

| lớp nguồn | phân loại trên candidate | phép đo tự chạy / răng bản vá |
|---|---|---|
| F01 `thieu-dinh-danh-van-passed` | **ĐÃ VÁ THẬT trong phạm vi đo** | Replay `steps=[]`, `[{}]`, name rỗng, conclusion null; SHA có newline với jobs rỗng; check URL có newline: đều `not_measured`, đúng trường trong `thieu`, không `passed`. Ma trận mở rộng kiểu scalar/list/dict/bool/chuỗi rỗng không ném trong các trường đã đo (`probes.json`). `r4_F01_previous_shapes` rc0. Các mutant fullmatch SHA/URL đều GIET c22. Ba mutant riêng bỏ kiểm step name, conclusion, dict đều **baseline0→rc3/TinHieuChotCa đúng c22** (`extra-results.json`). Mutant bỏ nguyên cả kiểm phần tử gây KeyError là **TIN_DUNG_GIA**, không dùng nó để chứng minh răng; xem danh sách. |
| F02 `nhac-ten-script-thanh-thuc-thi` | **VÁ HỜ ở cấp đóng lớp — vá một phần; còn P0, LẶP LỚP lần 4** | Bốn script thật `if false`, hàm chưa gọi, chuỗi nhiều dòng, heredoc của lượt 3 được chạy lại bằng `bash -e -x`: candidate nay trả `not_measured`, không marker; `r4_F02_previous_contexts` rc0. Các mutant đổi về quét từng dòng/nhận metadata hoặc nới grammar đều GIET c23. Nhưng hai phản chứng mới cùng cơ chế vẫn tool rc0/Gate passed, trong khi shell không gọi test; hai ca reviewer **rc3 do TinHieuChotCa đúng tên**, chi tiết ở bảng lớp. |
| F03 `phan-trang-dem-thay-vi-chung-minh-du` | **GIỮ ĐÃ VÁ THẬT trong phạm vi đo** | Replay cho cả jobs/artifacts: TRANG=1, totals **2→3→3→3**, IDs **1/2/3/rỗng** ⇒ vẫn `du:false`, dù cuối đủ 3 ID. Đối chứng total cố định ⇒ `du:true`. Thêm total khai thấp, trùng ID, trang lặp đến trần, body sai dạng; không khai đủ sai (`page_*` trong `probes.json`). Mutant bỏ kiểm total đổi và các mutant phân trang/dedup/completeness đều GIET đúng c20. |
| F04 `rest-gia-khong-neo-run` | **GIỮ ĐÃ VÁ THẬT trong phạm vi đo** | Run6/jobs run6/artifacts run6/log ID lạ đều404; attempt khác chỉ thấy state tương ứng. Hai mutant URL jobs/artifacts sang run+1 đều **baseline0→rc3, GIET c20**. Không dùng ID tự khai trong response để chọn route. |
| F05 `duong-loi-bo-dong-dem-bat-buoc` | **ĐÃ VÁ THẬT trong phạm vi đo** | Replay subprocess thật: check URL int/list, steps string/list scalar nay rc0 + Gate not_measured + đúng một dòng summary2, không AttributeError. HTTP403 ở bốn endpoint ⇒ rc3/403/summary4; Run list/null/string ⇒ rc3/summary4; đối số sai ⇒ rc2/summary4; lỗi ghi và AttributeError được tiêm ở thu ⇒ giữ rc1/ngoại lệ, đúng một summary4, không provenance. **15 đường terminal** trong `terminal.json`. `r4_F05_previous_shapes`/`r4_F05_final_grid` rc0. Mutant bỏ projection an toàn, lưới cuối, summary thu/REST/ghi/đối số đều GIET đúng c22/c19/c01. |
| F06 `redirect-loi-thoat-ngoai-bo-boc` | **GIỮ ĐÃ VÁ THẬT trong phạm vi đo** | Mock trực tiếp và sau302: URLError/OSError ⇒ LoiRest; 302→403/307 giữ HTTP code, 302→200 giữ bytes; lượt blob nhận chuỗi URL. Hai mutant ứng viên và mutant reviewer chỉ bọc lượt đầu đều GIET c24. Không có mạng thật hoặc payload credential; không suy đã đo chính sách redirect LIVE. |
| F07 `a10-doi-sha-khi-checkout-skipped` | **GIỮ ĐÓNG BẰNG AUTHORITY** | Đọc/băm frozen A10 và replay excerpt bằng parser candidate + Git cục bộ: 13 checkout passed, chuan-bi118368688427 not_measured; SHA/parents/tree khớp đính chính prompt. Đây không phải sửa mã và không phải phép đo LIVE mới. |

Tập mở cuối lượt 3 **U={F01,F02,F05}**; tập sửa thật được xác minh ở lượt 4 **F={F01,F05}**, tỷ lệ **2/3 ≈ 66,7%**. **Không có slug mới** trong phạm vi phép đo; hai biểu hiện mới thuộc F02, không chuyển thành lớp mới để né lịch sử. Tỷ lệ này không vô hiệu hóa stop condition lặp F02 ở lượt 4.

**BẢNG LỚP CÒN MỞ.** Một lớp nguyên nhân, hai nhóm biểu hiện; hạng cao nhất P0. Các đường cùng cơ chế đã được quét trước khi báo.

| lớp | hạng | biểu hiện (tệp:dòng) | phép đo tái hiện | HINT patch |
|---|---|---|---|---|
| **F02 `nhac-ten-script-thanh-thuc-thi` — LẶP LỚP** | **P0** | **a.** `ops/ci_provenance.py:185–191`, `:217–219`: bất cứ dòng nào trong nhóm có chứa mã ANSI cyan đều được chọn làm kịch bản, kể cả dòng giá trị metadata sau `env:`. Một dòng metadata có nội dung nhắc `python ops/ci_provenance_test.py` được nhập vào tập lời gọi và nhận marker của output khác. **b.** Cũng selector ấy bỏ toàn bộ dòng không có màu: khối `if false` với riêng dòng Python còn màu được biến thành “toàn khối lời gọi tối giản”. Nhánh fallback `b["lenh"][:1]` ở217 còn bỏ các dòng sau khi cả khối không màu; nó cũng không chứng minh toàn khối. `:225–227`, `:247` nâng thành marker/Gate passed. | `python -B .review/run.py probes python -B .review/probes.py` rc0; `real/env_ansi_metadata/` và `real/mixed_color_control/` giữ script, trace, Actions-shaped log, provenance trong result.json. Cả hai **shell rc0, tool rc0, marker target passed, Gate passed**. Trace shell thứ nhất chỉ có `+ python -B .review/emit.py`; trace thứ hai chỉ false và emitter, không gọi test. Dùng **MOI/regex thật** và stdout suite thật đã lưu (CA24/24, DOT BIEN53/53); emitter chỉ đọc lại stdout ấy. `python -B .review/review_cases.py r4_F02_env_metadata` và `... r4_F02_mixed_color` đều **rc3/DO:<đúng-ca>** từ TinHieuChotCa; đối chứng đơn giản rc0. | **Ở đâu:** `tach_buoc` và hợp đồng đầu vào `do_dau_duong`, vì `all(goi)` chỉ chứng minh tập con đã lọc, không chứng minh toàn khối. **Cách:** xác định ranh giới script/shell/env bằng cấu trúc đã kiểm; giữ các dòng chưa phân loại, từ chối evidence cho nhóm mơ hồ/mất dữ liệu; không lấy màu làm authority và không fallback cắt một dòng. Đường rẻ là fail-closed trước mọi phần nhóm chưa chứng minh; parser shell đầy đủ đắt hơn chỉ mua thêm coverage. **Khóa:** hai ca reviewer trên + đối chứng đơn giản/nối dòng/hai lời gọi, có/không/mất một phần ANSI; bỏ từng chốt phân ranh giới hoặc completeness phải chết vì TinHieuChotCa đúng ca. **Rủi ro:** loại cả bước hợp lệ, nhầm metadata với code, hoặc áp grammar Bash lên PowerShell; giữ `not_measured`, không đổi thiếu thành failed/pass. **Ước lượng chưa áp:** thay khoảng10–20 dòng sản phẩm và bổ sung/đổi khoảng12–20 dòng test, net có thể +5–15; candidate chỉ còn **1 dòng** theo trần899/900. Không khẳng định HINT đã vừa trần; cần giảm lặp trong đúng write set hoặc authority mới. Stop condition hiện tại không cấp quyền vá tiếp. |

**Phạm vi chứng cứ F02.** Shell được thực chạy tại chỗ; log Actions-shaped được reviewer dựng từ script/output, gắn fixture checkout và metadata vô hại `DEMO_TEXT`. Biểu hiện a thêm dòng nhắc test trong giá trị metadata; biểu hiện b chủ động bỏ màu ở các dòng control/emitter. Các file ghi rõ nội dung để tái hiện parser. Đây là phản chứng về việc công cụ cấp bằng chứng khi đầu vào không chứng minh được thực thi, **không** phải lời khai đã thu được hai log này từ GitHub hoặc đã chạy chúng trên Actions. Cách runner thật render đúng trường hợp này **KHÔNG ĐO ĐƯỢC** trong review offline. Không có credential, LIVE hay nội dung tấn công nhạy cảm trong các script đó.

**Quét lớp mới và giới hạn.** `probes.json` giữ **96 nhóm đo** (không phải 96 acceptance): grammar nhiều dòng/nối backslash, Python -m/-W/-X, path Windows, PowerShell backtick, comment và nhiều lời gọi; phân trang/completeness/body shape; predicate số/bool/chuỗi/list/dict; lỗi direct/redirect/nested. Dạng parser ngoài allowlist được `not_measured` là chủ ý, không báo thành finding. Không tìm được slug nguyên nhân mới trong tập này. Màu thiếu hoàn toàn vẫn làm fallback xét riêng header; đây là cùng cơ chế F02, không dùng ví dụ ấy để khẳng định target chắc chắn chưa chạy. Native PowerShell/Windows **not_run**. Các hướng cần dữ liệu nhạy cảm về output path, symlink/job-ID hoặc credential redirect chỉ được mô tả bằng lời, **KHÔNG ĐO ĐƯỢC**.

**ĐỐI CHIẾU A1–A11; giữ thêm A12/A13.**

| tiêu chí | kết quả | evidence / giới hạn |
|---|---|---|
| A1 | **passed** | `python -B ops/ci_provenance.py thu --help` rc0, đủ4 cờ (`cli-help.*`); `cat-file -e <base>:ops/ci_provenance.py` rc128 xác nhận base chưa có tệp. Mutant A1 GIET c01. |
| A2/M2 | **passed trong phạm vi đo** | c02 đối chiếu attempt, Run đủ metadata mới passed; ma trận field sai dạng không được nâng passed. Mutant bỏ so attempt và predicate Run đều GIET. |
| A3 | **passed phạm vi bảy ca** | c03–c09: hai fixture OS, thiếu/hai SHA, push lệch, PR có/không quan hệ parents; SHA không lấy từ REST. Mutant bắt buộc/neo nguyên dòng/quan hệ PR GIET đúng ca. Fixture Windows không chứng minh native Windows execution. |
| A4/M4 | **failed — F02 P0** | Năm ca hẹp/import MOI/marker đúng bước qua và có răng, nhưng các ca mới cho marker/Gate passed dù target không được thực thi. Không dùng53 mutant hoặc24 ca để đóng F02. |
| A5 | **passed** | c16 + mutant REST path⇒passed GIET; Workflow definition giữ not_measured, `path` chỉ ở `loi_khai_rest_path`. |
| A6 | **passed phạm vi đã thử** | c17 lỗi ghi giữa chừng, có/không out trước; không để out nửa vời; mutant ghi thẳng GIET c17. Không đo crash/power loss, writer cạnh tranh hoặc native Windows. |
| A7/M7 | **passed trong phạm vi đo** | c18 summary1/rc0;15 đường terminal giữ đúng một dòng đếm, mã/ngoại lệ thật và không sinh provenance khi lỗi. Mutant summary/projection/lưới cuối đều GIET đúng ca. |
| A8 | **passed định dạng/số ca/phân hạng; không chứng minh hết semantics** | Suite rc0: **CA24/24; DOT BIEN53/53; TU KIEM DAT(2); TONG DAT**. Audit riêng60 mutant ở dưới không cộng tín dụng giả. Đưa mutant AttributeError qua except đổi kiểu vào DOT_BIEN trong bộ nhớ ⇒ **CA24/24, DOT BIEN0/1, TIN_DUNG_GIA, TONG DO, main rc1** (`classifier-negative.json`). Hai fixture hash qua c21; tính xác thực nguồn full log độc lập KHÔNG ĐO ĐƯỢC. |
| A9 | **lệnh failed rc1; full acceptance KHÔNG ĐO ĐƯỢC vì môi trường** | `python -B .claude/dev/ci_dang_ky_test.py --chay`: ĐĂNG KÝ25/25, LAUNCHER WINDOWS4/4, RUFF CI3/3, rồi git commit fixture rc128 do signer gọi socket loopback bị `operation not permitted` (`registry-detail.json` giữ stderr con). Không bypass ký/trust. `kiem()` thật errors=[]/25/25; gỡ mục bằng registry trong bộ nhớ ⇒25/24 và đúng lỗi test sống chưa đăng ký. Regex MOI bằng tiền lệ, nhận stdout suite thật, từ chối tổng lệch/0mutant/đỏ. Các probe này không thay full --chay. |
| A10 | **frozen/readback phù hợp authority; LIVE độc lập KHÔNG ĐO ĐƯỢC** | `readback.py` rc0;14jobs/14 labels Ubuntu;13 checkout replay passed + chuan-bi118368688427 not_measured. SHA **b27fe85c9e9593ddbb059808fe4347fe1bd267be**, parents **5618020a67709ca6f2c93138905df0aa8d9c2df6** + **400589368e09ab2ee0e734b7af08b93478035503**, tree **857bc47e6bc5f0024e442b400819ac51286dfc55**. Frozen provenance SHA-256 **2b05a44934ffe91e6c23e89adf33ac171cc1ced80ea01edd06ecc5fcd96720e1** khớp stdout. NOT_MEASURED16=WD1+checkout1+Gate14. Không có full logs/HTTP receipt độc lập để xác thực full-log hash hoặc LIVE trên candidate. |
| A11 | **passed theo trần900 đã cấp** | doctrine-scan rc0:10tệp/0chép doctrine; adr-song rc0:53/53 khớp1–1, tha0016; bare Ruff0.15.15 `check --no-cache --select F` hai tệp mới rc0/All checks passed; đúng3tệp/899 dòng thêm, diff-check rc0. Ruff pin/probe contract đo riêng `loi_ruff_ci()=([],3)`; không dùng thay bare lint. |
| A12/V1–V4 | **KHÔNG ĐO ĐƯỢC remote/future; V2 failed** | Không ls-remote/push/connector trong assignment. Còn F02 P0 và đã chạm stop condition lượt4; không có quyền đẩy hoặc tự phóng connector từ verdict này. |
| A13 | **KHÔNG ĐO ĐƯỢC hoàn chỉnh** | Có metadata CLI đúng thread trong preflight.json; chưa có stdout thread.started, launcher run.json và rollout/hash đã ổn định sau khi writer kết thúc. Bên vận chuyển cần thu/readback đủ1–5 đúng run; file đang ghi hoặc actor đăng GitHub không thay receipt. |

**DANH SÁCH MUTANT VÀ HẠNG.** Hai lệnh audit: `python -B .review/run.py mutants python -B .review/mutants.py` và `... extra-mutants python -B .review/extra_mutants.py`, driver đều rc0. `mutants/results.json` giữ57 mục của lệnh đầu; `mutants/extra-results.json` giữ3 mục bổ sung; `mutants/all-results.json` nối hai nguồn, không ghi đè receipt lượt đầu. Mỗi mục giữ neo/thay nguyên văn, hash mã gốc, command, bản sao, baseline/rc/output và phân hạng. Mọi ca đích đã có **baseline rc0 trên bản sao source gốc**. Chạy `python -B ops/ci_provenance_test.py --mot-ca <ca>` với `CI_PROVENANCE_MA=<bản sao>`, bytecode tắt; chỉ rc3 từ handler TinHieuChotCa **đúng tên ca** được tính GIET.

Tổng **60 mutant:57 GIET,2 TIN_DUNG_GIA,1 SONG_SOT,0 HONG**. Trong đó53 mutant ứng viên đều GIET; hai tự kiểm là TIN_DUNG_GIA/SONG_SOT; năm mutant reviewer là4 GIET +1 TIN_DUNG_GIA. Hai ca F02 đỏ trên candidate là **phản chứng**, không phải mutant và không cộng vào số này. Bộ phân hạng còn từ chối rc3 mang tên ca khác và AssertionError thông thường.

| mutant | ca đích | rc baseline → mutant | hạng |
|---|---|---|---|
| `A1_xoa_co_attempt` | `c01_cli_du_co` | 0 → 3 | **GIET** |
| `A2_bo_so_attempt` | `c02_attempt_lech` | 0 → 3 | **GIET** |
| `A3d_lay_sha_dau_tien` | `c06_checkout_hai_sha` | 0 → 3 | **GIET** |
| `A3c_thieu_la_do_duoc` | `c05_checkout_khong_sha` | 0 → 3 | **GIET** |
| `A3e_lay_head_sha_rest` | `c07_checkout_push_lech` | 0 → 3 | **GIET** |
| `A3b_chi_nhan_linux` | `c04_checkout_windows` | 0 → 3 | **GIET** |
| `A3g_pr_nhan_moi_sha` | `c09_checkout_pr_lech` | 0 → 3 | **GIET** |
| `A3_sha_khong_nguyen_dong` | `c05_checkout_khong_sha` | 0 → 3 | **GIET** |
| `A4d_regex_ca_log_job` | `c13_marker_buoc_khac` | 0 → 3 | **GIET** |
| `A4b_skipped_la_passed` | `c11_job_skipped` | 0 → 3 | **GIET** |
| `A4a_runner_0_la_passed` | `c10_runner_id_0` | 0 → 3 | **GIET** |
| `A4c_khong_khop_la_not_measured` | `c12_marker_khong_khop` | 0 → 3 | **GIET** |
| `A4_chep_cung_MOI` | `c15_moi_mot_nguon` | 0 → 3 | **GIET** |
| `A4_job_failure_bo_qua` | `c14_ngoai_moi` | 0 → 3 | **GIET** |
| `A5_passed_khi_co_path` | `c16_workflow_def_luon_not_measured` | 0 → 3 | **GIET** |
| `A6_ghi_thang_vao_out` | `c17_ghi_nguyen_tu` | 0 → 3 | **GIET** |
| `A7_bo_dong_dem` | `c18_dem_not_measured` | 0 → 3 | **GIET** |
| `A7_gop_rest_vao_12` | `c19_rest_loi` | 0 → 3 | **GIET** |
| `M1_chi_doc_trang_dau` | `c20_du_trang` | 0 → 3 | **GIET** |
| `F03_dung_khi_du_total` | `c20_du_trang` | 0 → 3 | **GIET** |
| `F03_tap_luon_du` | `c20_du_trang` | 0 → 3 | **GIET** |
| `F03_trung_id_van_them` | `c20_du_trang` | 0 → 3 | **GIET** |
| `F04_jobs_run_khac` | `c20_du_trang` | 0 → 3 | **GIET** |
| `F04_artifacts_run_khac` | `c20_du_trang` | 0 → 3 | **GIET** |
| `F01_run_thieu_van_passed` | `c22_thieu_dinh_danh_khong_passed` | 0 → 3 | **GIET** |
| `F01_gate_thieu_van_passed` | `c22_thieu_dinh_danh_khong_passed` | 0 → 3 | **GIET** |
| `F01_checkout_head_thieu` | `c22_thieu_dinh_danh_khong_passed` | 0 → 3 | **GIET** |
| `F02_search_thay_match` | `c23_chi_loi_goi_that` | 0 → 3 | **GIET** |
| `F02_quet_tung_dong` | `c23_chi_loi_goi_that` | 0 → 3 | **GIET** |
| `F02_kich_ban_gom_metadata` | `c23_chi_loi_goi_that` | 0 → 3 | **GIET** |
| `F01_steps_chi_la_list` | `c22_thieu_dinh_danh_khong_passed` | 0 → 3 | **GIET** |
| `F05_chieu_khong_an_toan` | `c22_thieu_dinh_danh_khong_passed` | 0 → 3 | **GIET** |
| `F05_luoi_cuoi` | `c19_rest_loi` | 0 → 3 | **GIET** |
| `F02_khong_noi_dong` | `c23_chi_loi_goi_that` | 0 → 3 | **GIET** |
| `F02_cho_moi_co` | `c23_chi_loi_goi_that` | 0 → 3 | **GIET** |
| `F02_doi_so_tu_do` | `c23_chi_loi_goi_that` | 0 → 3 | **GIET** |
| `F01_bool_la_int` | `c22_thieu_dinh_danh_khong_passed` | 0 → 3 | **GIET** |
| `F01_chuoi_rong` | `c22_thieu_dinh_danh_khong_passed` | 0 → 3 | **GIET** |
| `F01_conclusion_bat_ky` | `c22_thieu_dinh_danh_khong_passed` | 0 → 3 | **GIET** |
| `F01_labels_rong` | `c22_thieu_dinh_danh_khong_passed` | 0 → 3 | **GIET** |
| `F01_check_run_bat_ky` | `c22_thieu_dinh_danh_khong_passed` | 0 → 3 | **GIET** |
| `F01_head_sha_bat_ky` | `c22_thieu_dinh_danh_khong_passed` | 0 → 3 | **GIET** |
| `F01_head_sha_nhan_newline` | `c22_thieu_dinh_danh_khong_passed` | 0 → 3 | **GIET** |
| `F01_check_run_nhan_newline` | `c22_thieu_dinh_danh_khong_passed` | 0 → 3 | **GIET** |
| `F01_artifact_khong_kiem` | `c22_thieu_dinh_danh_khong_passed` | 0 → 3 | **GIET** |
| `F01_phong_bi_khong_kiem` | `c22_thieu_dinh_danh_khong_passed` | 0 → 3 | **GIET** |
| `F03_bo_kiem_total_doi` | `c20_du_trang` | 0 → 3 | **GIET** |
| `F05_than_run_sai_dang` | `c19_rest_loi` | 0 → 3 | **GIET** |
| `F05_loi_ghi_mat_dong_dem` | `c19_rest_loi` | 0 → 3 | **GIET** |
| `F05_sai_doi_so_mat_dong_dem` | `c01_cli_du_co` | 0 → 3 | **GIET** |
| `F05_rest_mat_dong_dem` | `c19_rest_loi` | 0 → 3 | **GIET** |
| `F06_redirect_lot_loi` | `c24_goi_that_loi_va_chuyen_huong` | 0 → 3 | **GIET** |
| `F06_redirect_mang_token` | `c24_goi_that_loi_va_chuyen_huong` | 0 → 3 | **GIET** |
| `vo_can_AttributeError_qua_except_doi_kieu` | `c03_checkout_linux` | 0 → 4 | **TIN_DUNG_GIA** |
| `chi_them_chu_thich` | `c20_du_trang` | 0 → 0 | **SONG_SOT** |
| `review_F01_skip_step_elements` | `c22_thieu_dinh_danh_khong_passed` | 0 → 4 | **TIN_DUNG_GIA** |
| `review_F06_only_wrap_first` | `c24_goi_that_loi_va_chuyen_huong` | 0 → 3 | **GIET** |
| `review_F01_step_name` | `c22_thieu_dinh_danh_khong_passed` | 0 → 3 | **GIET** |
| `review_F01_step_conclusion` | `c22_thieu_dinh_danh_khong_passed` | 0 → 3 | **GIET** |
| `review_F01_step_dict` | `c22_thieu_dinh_danh_khong_passed` | 0 → 3 | **GIET** |

Mutant `review_F01_skip_step_elements` bỏ nguyên predicate phần tử làm projection ném **KeyError(name), rc4**; ca đích không chết bởi TinHieuChotCa nên giữ **TIN_DUNG_GIA**. Không dùng tín hiệu này để đóng F01. Các mutant riêng name/conclusion/dict mới là phép đo răng của từng chốt: đều rc3 đúng c22. Mutant chỉ thêm chú thích là đối chứng sống sót có chủ ý. Không áp patch sản phẩm hoặc phát product patch-as-hint.

**Giới hạn nghiệm thu và bàn giao.** Native Windows/PowerShell, CI/required checks trên candidate, HTTP/full-log authenticity, redirect thật, remote lease/ref freshness, review-call budget và receipt terminal/delivery cuối **KHÔNG ĐO ĐƯỢC**. Full runtime/release gates **not_run**; đây là review targeted công cụ dev-side, không chứng nhận worker/land/release gate hoàn chỉnh. Không nâng `skipped`, `not_run`, rc1 môi trường hoặc dữ liệu thiếu thành passed. Bộ fixture giữ đúng skipped/not_run ở c10/c11; không dùng chúng làm execution OS thật.

**Snapshot cuối.** `snapshot-start.json`, `snapshot-end.json`, `snapshot-comparison.json` đối chiếu hash/size **5.266 tệp** ngoài `.git/` và `.review/`, gồm ignored/untracked, `.review-input/` và `.codex/`: **0 delta**. HEAD/tree không đổi; tracked diff, cached diff và untracked không ignored rỗng, các lệnh rc0. Ignored chỉ là các vùng đã có `.codex/`, `.review-input/`, `.review/`; danh sách ignored ngoài `.review/` không đổi. `.git/` không băm toàn metadata, được kiểm qua HEAD/tree/index/diff/status. Hai snapshot chứng minh không có delta quan sát ở hai mốc, không chứng minh lịch sử chưa từng ghi rồi hoàn nguyên. Không có repo nguồn bên ngoài nào được cấp/quan sát trong lượt này.

Verdict **changes_requested** giữ trên exact SHA đầu tệp. F02 còn P0 và lặp lượt4; bước tiếp theo là **dừng hẳn theo authority checkpoint**, bàn giao chủ kho, không tự động vá hoặc mở lượt review kế tiếp. A9/A10/A12/A13 vẫn cần evidence phù hợp ở môi trường/thời điểm được cấp; verdict này không chứng nhận các nghĩa vụ ấy đã hoàn thành.
