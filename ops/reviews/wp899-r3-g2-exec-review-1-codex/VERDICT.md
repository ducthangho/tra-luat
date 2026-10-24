verdict: changes_requested
reviewed_sha: 29d641cbd4a38504eb30d87f0fc7eaa82a185f24
base_sha: dc657149941f9db3ab2afc6fb6462ba4827bf18f
Reviewed commit: 29d641cbd4a38504eb30d87f0fc7eaa82a185f24
reviewed_tree: cfa8b759780898f845d4e91bbd114153b9a09ec4
packet: wp899-r3-g2
review_round: 1
role: reviewer
provider: openai_codex
model_family: openai
model: gpt-6.1-sol (CLI-published)
effort: xhigh (CLI-published)
session_id: 01a16da4-4e87-7ec2-90e5-c3c0827f7192
model_reviewer_identity: openai_codex/gpt-6.1-sol/01a16da4-4e87-7ec2-90e5-c3c0827f7192 (CLI-published)
execution_surface: codex_cli
transport: machine
independent_from_executor_session: true
review_axes: [spec, standards_security]
github_submitter_identity: null
assurance: review_deferred

**Chưa đạt V2: hai lớp mở — P0=1, P1=1, P2=0, P3=0.** F02 `nhac-ten-script-thanh-thuc-thi` vẫn mở: hai phản chứng lượt 4 đã được chặn riêng lẻ, nhưng khối mất một phần màu có thể khớp lệnh của một bước/job khác trong cùng workflow và tạo marker/Gate `passed` cho test không chạy. Một lớp mới, F08 `nguon-workflow-git-khong-duoc-kiem-thu`, có hai mutant sống qua cả 33 ca. Khối thiếu dấu đóng còn được xác thực và tạo `failed`/rc12; biểu hiện này được nối vào F02, không tách slug để xóa lịch sử.

Đây là **lượt 1 của r3**, lời gọi thứ **5/8 theo assignment**, không tự xác minh được sổ chi remote. Không áp điều kiện dừng r2 để phủ nhận authority mở r3. Giữ nguyên V5: nếu F02 hoặc lớp mới F08 lặp ở lượt 2 r3 thì **DỪNG HẲN**. Verdict không cấp approval, quyền đẩy, merge, land, LIVE hoặc chuyển state.

**Preflight và phạm vi.** Đã đọc toàn bộ `.review-input/prompt.md`, hai đặc tả, bốn verdict r2 (lượt 4 trước), các tài liệu bắt buộc và adapter cross-review. Nguồn spec đóng băng của assignment là `.review-input/wp899-r3.md`, **18.402 byte**, SHA-256 `dd1a997d1f3682e23bb4b5577264076b7d9a12aeff5d9823f491cdda05e4f36f`; r2 **23.189 byte**, SHA-256 `d858c7c65a38a7f0fadda1cabf839c98ce70a881372d847c8979165925971707`. Cả hai khớp. Revision 3/generation 2, Review Class sensitive; áp Q1–Q8 và quyết định nâng trần **≤8 tệp/≤1050 dòng thêm** được prompt dẫn từ issuecomment-6383572422. Effective write set vẫn chỉ ba tệp, không được suy thành tám tệp có quyền ghi.

Origin `https://github.com/ducthangho/tra-luat.git`; detached HEAD/tree đúng các OID đầu verdict. Base tồn tại; `git merge-base --is-ancestor dc657149941f9db3ab2afc6fb6462ba4827bf18f HEAD` **rc0**; `--is-shallow-repository` trả **false**. Baseline nghiệm thu là `dc657149941f9db3ab2afc6fb6462ba4827bf18f`; điểm xuất phát `9e5019ef2e3b8d59345fff2165569c3281cba3b5` là parent trực tiếp của candidate. Đối chiếu **blob OID của từng tệp trong cả ba tệp** với `19b114867fbcad4c3b580bcbe4367bc78a890773` đều bằng nhau (`startpoint.json`). Không dời baseline theo điểm xuất phát. Lease/state/ref freshness, authority trên GitHub và terminal receipt của launcher **KHÔNG ĐO ĐƯỢC**; áp assignment offline được giao, không khai đã readback remote.

`git diff --numstat <base> HEAD` **rc0**: `.claude/dev/ci_dang_ky_test.py` **1/0**, `ops/ci_provenance.py` **388/0**, `ops/ci_provenance_test.py` **627/0**; tổng **1016 dòng thêm**, đúng ba tệp. `git diff --check <base> HEAD` **rc0**. Đã đọc toàn mã mới, diff đầy đủ và delta r3; mục MOI thêm đúng một dòng. Evidence: `preflight.json`, `full.patch`, `delta.patch`, `startpoint.json`.

**Môi trường và cách đọc evidence.** Linux x86_64, Python **3.13.17**, `/usr/bin/python`, PyYAML **6.0.3**, Git **2.43.0**, Ruff **0.15.15**, codex-cli **0.164.0**; `core.abbrev=7` đã có sẵn, probe **rc0**, không sửa config. `preflight.json` chỉ trích metadata của rollout đúng thread: `/root/.codex/sessions/2026/10/24/rollout-2026-10-24T11-20-48-01a16da4-4e87-7ec2-90e5-c3c0827f7192.jsonl`. `session_meta.id` khớp thread, `originator=codex_exec`, `model_provider=openai`; `turn_context` công bố model/effort ở đầu verdict. Đây là **model/effort do CLI công bố**; model phục vụ từng request **KHÔNG ĐO ĐƯỢC**. Executor Claude/cloud/họ Claude là thông tin spec, không có runtime receipt Executor độc lập trong bundle.

Sandbox thực tế `workspace-write`, mạng restricted; checkout được giữ read-only theo assignment và snapshot, không tuyên bố OS khóa ghi toàn checkout. `codex --version` rc0 có cảnh báo không tạo được PATH aliases vì read-only; không sửa quyền/trust. Catalog không có `environment_status`. Không chạy doctor/chuan-bi, cài dependency, gọi subagent, GitHub, push hoặc LIVE trong assignment này. Registry fixture tự gọi signer qua socket loopback và bị từ chối; không biến lỗi đó thành bằng chứng GitHub hay lỗi sản phẩm.

Lệnh tái hiện từ gốc workspace: `python -B .review/run.py <nhãn> <command...>`. Wrapper đặt `PYTHONDONTWRITEBYTECODE=1`, TMPDIR/TMP/TEMP và cache trong `.review/`; mỗi `<nhãn>.receipt.json` giữ **command, rc con thật, thời gian, size/hash stdout/stderr**. Rc0 của driver thu thập không thay rc của ca/công cụ ghi trong JSON. Bản sao mutant và mọi output reviewer đều nằm trong `.review/`; không có patch sản phẩm được áp vào checkout.

**ĐỐI CHIẾU F01–F07.** Nguồn gần nhất: `.review-input/r2/VERDICT-r2-luot4.md`, SHA `19b114867fbcad4c3b580bcbe4367bc78a890773`. Giữ stable slug và lịch sử cả bốn lượt. Các ca cũ được dựng lại từ mô tả; không khai đã nhận script reviewer cũ.

| lớp kế thừa | trạng thái trên candidate | phép đo độc lập và răng |
|---|---|---|
| F01 `thieu-dinh-danh-van-passed` | **GIỮ ĐÃ VÁ THẬT trong phạm vi đo** | c22 và các mutant F01 đều xanh/giết đúng ca. `probes.json` kiểm lại steps rỗng, `[{}]`, string/scalar, check URL int/list/newline; Gate đều not_measured, không ném. Thiếu head/event ⇒ Checkout chưa đo và không đọc YAML; thiếu path ⇒ workflow chưa đo/không marker. Thiếu check_suite_id giữ Run not_measured; Gate riêng có thể đo được, không gọi đó là Run passed. Trường mới `kich_ban` không làm Gate vượt validator. |
| F02 `nhac-ten-script-thanh-thuc-thi` | **VÁ HỜ ở cấp đóng lớp — còn P0, LẶP LỚP** | Hai ca **đúng cơ chế lượt 4**, dùng emitter Python và stdout suite/MOI thật: trên source điểm xuất phát r2, cả hai Gate passed; r3 đều không marker/buoc_xac_thuc=0/Gate not_measured. Nhưng thêm ứng viên trùng ở bước/job khác làm cả hai cơ chế tái mở; đổi thứ tự ứng viên không chữa. Biến thể env bị chặn vẫn giữ not_measured đúng A19. `r4-comparison.json`, `review-cases.json`, `probes.json`; chi tiết bảng lớp. |
| F03 `phan-trang-dem-thay-vi-chung-minh-du` | **GIỮ ĐÃ VÁ THẬT trong phạm vi đo** | Tự đo jobs/artifacts với TRANG=1: total 2→3→3→3, ID1/2/3/rỗng ⇒ du=false; đối chứng total cố định ⇒ du=true. Trang thiếu, trùng ID, total khai thấp cũng không được khai đầy đủ. Mutant phân trang/completeness/dedup/total đổi GIET c20. |
| F04 `rest-gia-khong-neo-run` | **GIỮ ĐÃ VÁ THẬT trong phạm vi đo** | RestGia trả 404 cho run6, jobs run6, artifacts run6 và log ID lạ; attempt2 lấy state attempt2. Hai mutant URL jobs/artifacts run+1 GIET c20, baseline0→3 đúng TinHieuChotCa. |
| F05 `duong-loi-bo-dong-dem-bat-buoc` | **GIỮ ĐÃ VÁ THẬT trong phạm vi đo** | c01/c19 và mutant summary/projection/lưới cuối đều GIET. HTTP403 đủ bốn endpoint ⇒ rc3/summary4; Run list/null/string ⇒ rc3/summary4; lỗi ghi OSError và AttributeError ở thu giữ lỗi thật và summary4. Shapes job cũ không còn ném; YAML hỏng/rất sâu/không phải mapping của r3 không ném, summary còn đúng. Không suy từ đó rằng mọi ngoại lệ đều đã đo. |
| F06 `redirect-loi-thoat-ngoai-bo-boc` | **GIỮ ĐÃ VÁ THẬT trong phạm vi đo** | Tự chạy c24: URLError trực tiếp/sau302, OSError sau302, 302→200; lỗi thành LoiRest, thành công giữ bytes; request blob là chuỗi URL. Hai mutant F06 GIET c24. Đây là mock offline, không chứng minh redirect/credential policy mạng thật. |
| F07 `a10-doi-sha-khi-checkout-skipped` | **GIỮ ĐÓNG BẰNG AUTHORITY** | r3 đã đòi 13 checkout + chuan-bi not_measured. Tự băm/readback dữ liệu A10 và đối chiếu Git local, đúng 13+1; không yêu cầu bịa SHA cho job không checkout. LIVE độc lập vẫn KHÔNG ĐO ĐƯỢC. |

Tập mở cuối r2 lượt4 U={F02}; r3 lượt1 chưa xác minh F02 đóng, F=∅, tỷ lệ sửa thật **0/1**. F08 là lớp mới, không vào tử số; việc mở r3 không reset lịch sử F02. Không suy riêng tỷ lệ này thành điều kiện dừng V5 ngay lượt1.

**BẢNG LỚP CÒN MỞ.** Hai lớp, năm nhóm biểu hiện: F02 a/b/c; F08 a/b. Mỗi lớp lấy hạng cao nhất còn mở.

| lớp | hạng | biểu hiện (tệp:dòng) | phép đo tái hiện | HINT patch | ước lượng dòng |
|---|---|---|---|---|---|
| **F02 `nhac-ten-script-thanh-thuc-thi` — LẶP LỚP** | **P0**; c riêng P1 | **a/b.** `ops/ci_provenance.py:166`, `:207`, `:218`, `:240`: bộ chọn ứng viên toàn workflow chỉ so phần mang màu; một phần khối của bước hiện tại có thể bằng nguyên một run ở bước/job khác. Header `if false; then` và dòng control không màu vẫn bị bỏ qua. Metadata mang màu cũng có thể hoàn thiện một ứng viên ở nơi khác. `:252`, `:273` nâng marker và Gate passed. **c.** `:216–219`, `:240`: nhóm chưa từng có dấu đóng vẫn được coi là khối in lại để xác thực, rồi marker thất bại giả. | `python -B .review/review_cases.py F02_collision_other_job`: **rc3/DO:F02_collision_other_job** do TinHieuChotCa đúng tên. Bash thật **rc0**, trace chỉ `+ false` và `+ python -B .review/emit.py`; không gọi `ops/ci_provenance_test.py`. Công cụ **rc0**, marker target/Gate **passed**, buoc_xac_thuc=1. `r4_compare.py`: cả mixed-color và env-metadata, ứng viên khác job trước/sau hoặc bước khác cùng job đều passed; ứng viên trùng có env ⇒ not_measured. `F02_missing_endgroup` cũng **rc3 đúng chốt**: bỏ dòng đóng khỏi đối chứng hợp lệ ⇒ công cụ **rc12/Gate failed**, buoc_xac_thuc=1; dữ liệu thiếu phải chưa xác thực/không marker. | **Ở đâu:** hợp đồng khối từ `tach_buoc` sang `do_dau_duong`, vì `git_blob` đọc đúng YAML không chứng minh tập con log thuộc đúng bước. **Cách rẻ:** trước phép khớp Q2, đòi khối đóng và cấu trúc echo/metadata/header nhất quán, đủ để không nhận tập con hoặc dòng env thành một khối khác; mơ hồ ⇒ không xác thực/not_measured. Giữ YAML là nguồn kịch bản, không quay về lấy script từ log. Chỉ giới hạn ứng viên theo job cũng chưa đóng biểu hiện cùng-job; chỉ so header cũng chưa đóng metadata. Nếu chưa chứng minh được completeness bằng grammar hẹp, cần fail-closed thay vì nhận khớp tình cờ. Parser/định danh bước giàu hơn là đường đắt, cần authority nếu đổi Q2. **Khóa:** hai ca r4 gốc, ma trận collision ở r4-comparison, missing-endgroup, đối chứng đơn giản/blank/CRLF và A19; mutant bỏ từng chốt phải chết đúng ca. **Rủi ro:** từ chối bước hợp lệ, nhầm output group với echo hoặc viết parser Bash áp lên pwsh; giữ fallback chưa đo và đo riêng nền. | Ước lượng **20–35 dòng thêm ròng**, gồm sản phẩm/test; chưa áp, không khẳng định vừa trần. |
| **F08 `nguon-workflow-git-khong-duoc-kiem-thu` — MỚI** | **P1** (M8/M11) | **a/b.** `ops/ci_provenance_test.py:139–152`, `:455`: mọi ca workflow mới tiêm hàm tra dictionary thay cho `git_blob`; nhãn “thiếu object/sai path” ở c32 không đi qua reader thật `ops/ci_provenance.py:145–151`. Không có ca/đột biến khóa source SHA của reader. Đổi toàn bộ reader sang HEAD, hoặc vô hiệu hóa việc đọc YAML, đều không bị ca nào bắt. | `python -B .review/extra_mutants.py`: `git_ignore_sha` đổi đúng neo `f"{sha}:{path}"` thành `f"HEAD:{path}"`; `git_always_unavailable` đổi nhánh giải mã thành `return None`. **Mỗi mutant 33/33 ca rc0, SONG_SOT**, gồm c32. Source/neo/thay/rc từng ca ở `extra-mutants/results.json`. Ca reviewer `git_workflow_source` đọc workflow thật tại b27fe85 và so bytes từ git: **baseline rc0**, cả hai mutant **rc3/DO:git_workflow_source**, GIET thật. Đây là thiếu răng, chưa khẳng định reader sản phẩm hiện sai. | **Ở đâu:** thêm ca vào bộ test hiện có và DOT_BIEN, vì `git_blob` hiện trả bytes đúng trong phép đo độc lập. **Cách:** gọi reader thật trên object cục bộ khác HEAD, đối chiếu exact bytes; khóa cả SHA/path hợp lệ và object/path thiếu, non-UTF8. Có thể dùng fixture Git riêng của test, hoặc mock subprocess giữ argv+byte state; không chép implementation để tự so. **Khóa:** hai mutant reviewer trên phải chết do TinHieuChotCa đúng ca; thêm mutant bỏ/chuyển path và decode guard nếu nhận các chốt ấy. **Rủi ro:** test phụ thuộc object lịch sử chưa có trong clone CI, hoặc fixture commit chết vì signer rồi cấp tín dụng giả; fixture phải tự đủ và phân hạng setup riêng. | Ước lượng **12–20 dòng thêm ròng** cho ca/đột biến, không cần sửa sản phẩm đang đúng. |

Ứng viên còn **34 dòng** theo trần 1050. Tổng HINT ước **32–55 dòng ròng**, chưa triển khai; không khẳng định hai lớp có thể đóng trong trần nếu không giảm lặp. Cần Executor tái dẫn xuất trong đúng write set hoặc xin authority thích hợp; reviewer không tự nâng trần.

**Ranh giới chứng cứ F02.** Hai script shell được chạy thật tại chỗ; emitter chỉ đọc lại stdout suite đã chạy, không gọi test target, không sửa script test. Workflow fixture giữ nguyên khi so các biến thể log; nó có một run thường và một run ở bước/job khác (job khác có `if: false`). Không có lệnh workflow nào in nhóm Run giả; lỗi không đòi thay script target hoặc workflow tại lúc thu log. Log có thiếu một phần ANSI/metadata được reviewer dựng theo đúng cơ chế phản chứng lượt4; **không khai đã thu được định dạng này từ Actions**. Workflow/REST/Git callback của phép replay là fixture, không giả là workflow thật của b27fe85. Bằng chứng chứng minh phép xác thực hiện tại có thể nhận đầu vào thiếu/mơ hồ thành passed, cùng miền phản chứng A14/A15; khả năng runner thật tạo từng biến thể **KHÔNG ĐO ĐƯỢC** offline. Giới hạn “không chống tác giả workflow” không đóng phản chứng này: test/workflow không cần đổi trong phép so, và không có group giả được phát từ workflow. Nếu muốn loại cả biến thể log thiếu/mất màu khỏi miền bảo đảm thì cần quyết định acceptance rõ ràng, không gọi F02 đã đóng bằng kiểm r4 đơn lẻ.

Q1–Q8 được giữ như authority, không ghi bản thân các lựa chọn đó thành finding. F02 chỉ ra điều kiện xác thực đầu vào còn thiếu trong triển khai. HINT đường rẻ giữ phép so nguyên văn Q2; đường đổi tập ứng viên/định danh bước cần chủ kho quyết định nếu làm đổi hợp đồng.

**Quét r3 ngoài ca đích.** `probes.json` giữ **85 nhóm đo**, không phải 85 acceptance: biên nhóm, thiếu/mất ANSI, CRLF, blank giữa run, khoảng trắng, nhiều newline cuối, continuation, `|-`/`>`; một/nhiều ứng viên; alias/anchor kể cả tự tham chiếu, khóa không phải chuỗi, `on` thành True, YAML sâu/hỏng; object/path thiếu, path REST có hậu tố ref, non-UTF8 qua mock; env step/job/workflow, biểu thức env, defaults, shell bash/pwsh/sh và shell template khác. Không có exception thoát ở tập này. Dạng ngoài grammar giữ not_measured là chủ ý, không yêu cầu hỗ trợ parser shell đầy đủ.

Sáu luật chặn executor thêm có răng bằng c31 và từng mutant riêng: VAR prefix, workflow env, defaults workflow/job, shell khác allowlist, GITHUB_ENV/PATH. Chúng giảm nhận nhầm các đường đổi chế độ đã nêu; không chứng minh mọi action/container có thể ảnh hưởng runtime đều đã được mô hình hóa. Luật defaults và quét mọi run trong mọi job khá bảo thủ: kể cả defaults giữ shell bash, hoặc tham chiếu GITHUB_ENV ở job độc lập, cũng từ chối đo. Đánh giá ở đây là **giới hạn độ phủ**, không coi từ chối đo ấy thành passed hoặc yêu cầu nới chốt chỉ để tăng tỷ lệ đo. Logic chế độ đầy đủ giữ ở P-B theo Q4. Native Windows/pwsh, reusable workflow/composite resolution và cách runner thật render các biên này **KHÔNG ĐO ĐƯỢC**; không tự soạn payload nhạy cảm về path/symlink/credential.

Trường mới `kich_ban.trang_thai=passed` hiện chỉ thể hiện đã đọc/parse được workflow: nó vẫn có thể kèm `buoc_xac_thuc=0`. Các phép đo ở đây dùng **count + marker + trạng thái Gate**, không lấy riêng chữ passed của trường đó làm chứng minh một bước đã được xác thực. Không nâng mốc Workflow definition bằng trường phụ này.

**ĐỐI CHIẾU A1–A19.** “Passed phạm vi hẹp” không thay mục tiêu M4/M8 đang có finding.

| tiêu chí | kết quả | evidence / phạm vi |
|---|---|---|
| A1 | **passed** | c01/CLI help đủ bốn cờ, mutant xóa attempt GIET đúng c01; dòng summary khi sai đối số có răng. |
| A2 | **passed** | c02, run_attempt2 so yêu cầu1 ⇒ failed/rc12; mutant bỏ so GIET. |
| A3 | **passed trong phạm vi bảy ca** | c03–c09: Linux/Windows fixture, thiếu/hai SHA, push lệch, PR có/không parents; mutant bắt buộc và nguyên dòng đều GIET. Fixture không là execution Windows. |
| A4 / M4 | **năm ca hẹp passed; M4 failed — F02** | c10–c15 và mutant tương ứng có răng: runner0/not_run, skipped, marker lệch/khác bước, ngoài MOI, import động. Collision vẫn tạo passed sai; mất dấu đóng tạo failed sai. |
| A5 | **passed** | c16 + mutant path⇒passed GIET; Workflow definition luôn not_measured, path chỉ lời khai REST. |
| A6 | **passed phạm vi lỗi thử** | c17 và mutant ghi thẳng GIET; lỗi giữa chừng có/không bản out cũ không để thư mục nửa vời. Không đo crash/power loss/writer cạnh tranh/native Windows. |
| A7 / M7 | **passed phạm vi đo** | c18 rc0/NOT_MEASURED1, c19 HTTP403/rc3/summary4; mutant gỡ từng summary/lưới cuối GIET. Không dùng rc0 làm chứng nhận bốn mốc. |
| A8 / M8 | **định dạng và phân hạng passed; thiếu chốt mới F08** | Suite **rc0: CA33/33, DOT BIEN66/66, TU KIEM DAT(2), TONG DAT**. Audit riêng68 mutant khớp hạng. Tiêm một mutant vô can AttributeError qua except đổi kiểu vào DOT_BIEN trong bộ nhớ ⇒ **CA33/33, DOT BIEN0/1, TIN_DUNG_GIA, TONG DO, main rc1** (`classifier-negative.json`); wrapper rc0 chỉ thu evidence. Hai mutant Git mới còn sống. |
| A9 | **lệnh failed rc1; toàn bộ KHÔNG ĐO ĐƯỢC vì môi trường** | `python -B .claude/dev/ci_dang_ky_test.py --chay` in ĐĂNG KÝ25/25, LAUNCHER WINDOWS4/4, RUFF CI3/3, rồi git commit fixture rc128: signer gọi socket loopback bị `operation not permitted`. `readback.json` giữ stderr con; không bypass ký/trust. `kiem()` thật []/25/25; bỏ mục khỏi registry trong bộ nhớ ⇒ đúng lỗi test sống chưa đăng ký/25/24. Regex bằng tiền lệ, nhận stdout suite thật và từ chối tổng lệch/0mutant/đỏ. Không dùng probe thay full --chay. |
| A10 | **frozen readback phù hợp; LIVE độc lập KHÔNG ĐO ĐƯỢC** | Chi tiết ngay dưới; không có full log/HTTP receipt để chạy lại công cụ trên nguồn LIVE. |
| A11 | **passed theo trần đã cấp** | doctrine-scan rc0:10 tệp/0 chép; adr-song rc0:53/53 khớp1–1 (tha0016); Ruff `check --no-cache --select F` đúng hai tệp mới rc0/All checks passed; đúng3 tệp/1016 dòng, diff-check rc0. Ruff pin/probe contract đo riêng `loi_ruff_ci()=([],3)`, không dùng thay bare lint. |
| A12 | **KHÔNG ĐO ĐƯỢC remote/future; V2 chưa đạt** | Không ls-remote/push/connector trong assignment offline. Còn P0/P1 nên chưa đủ điều kiện đẩy. |
| A13 | **KHÔNG ĐO ĐƯỢC hoàn chỉnh** | Metadata CLI đúng thread đã trích; stdout thread.started, launcher run.json và rollout/hash sau khi writer kết thúc chưa được thu trọn. Bên vận chuyển phải thu/readback1–5 đúng run. Không băm rollout đang ghi để gọi receipt cuối. |
| A14 | **passed đúng ca; chưa đóng F02** | c25 + mutant dựng script từ dòng màu GIET đúng c25; phản chứng r4_env thực chạy r2 passed→r3 not_measured. Variant có ứng viên trùng còn lọt F02b. |
| A15 | **passed đúng ca; chưa đóng F02** | c26 + mutant tập con GIET đúng c26; r4_mixed r2 passed→r3 not_measured. Variant ứng viên trùng còn lọt F02a. |
| A16 | **passed tiêu chí ca/đột biến** | c27 âm whole-block không tối giản và đối chứng toàn minimal; bỏ all(goi) GIET c27; bỏ equality GIET c25. Không dùng nó thay kiểm completeness của khối log. |
| A17 | **passed ba vế và đối chứng** | c28/c29/c30; ba mutant gỡ env step/env job/cho đối số đều GIET đúng ca con. Sáu chốt phụ c31/mutant cũng GIET. |
| A18 | **ca và mutant chỉ định passed; reader thật thiếu răng F08** | c32 thiếu object/path/YAML/SHA qua fixture không ném; mutant dùng REST head thay checkout GIET c32, bỏ bắt YAML GIET c32. Probe gọi Git thật và decode non-UTF8 đúng; nhưng đổi git_blob sang HEAD/None sống33/33. Không khai A18 đã chứng minh toàn đường Q3. |
| A19 | **passed ca chặt nhất** | c33: ứng viên thứ hai có env ⇒ chặn; mutant lấy đầu GIET c33. Đo lại đảo vị trí/cùng-job vẫn giữ chặn khi có env. Ứng viên trùng không env trong một bước khác là phản chứng F02 riêng, không phủ nhận ca A19. |

**A10 — readback lời khai executor, không phải LIVE mới.** `python -B .review/run.py readback python -B .review/readback.py` **rc0**. Hai hash provenance bằng hash trong stdout được giao:

- Run **39342960764**, attempt1: SHA-256 `87b8be84f479d0b17b214a4d3b0983d2fd46b89089602f3e55f118bfaef206b4`; Run passed, **14 job**, mọi labels `[ubuntu-latest]`; **13 Checkout passed + chuan-bi chưa đo**, SHA `b27fe85c9e9593ddbb059808fe4347fe1bd267be`, parents `5618020a67709ca6f2c93138905df0aa8d9c2df6` + `400589368e09ab2ee0e734b7af08b93478035503`, tree `857bc47e6bc5f0024e442b400819ac51286dfc55`, khớp Git local. Workflow tại SHA có **71 run, 0 run nhắc MOI**. Không có marker cho đường dẫn trong MOI; các mục ngoài MOI đều `not_measured/khong_co_trong_MOI`, phù hợp M4(e), không coi là vi phạm câu “không có mục marker” theo diễn giải assignment. Gate14 not_measured, WD not_measured; summary **16** khớp.
- Run **40074551995**, attempt1: SHA-256 `d2e5247ff36f512428b2e82a004f53cc8bfc59b7d584e7d3835aafbe7aa73c6a`; **23 job**, 22 Checkout passed + chuan-bi chưa đo, SHA `dc657149941f9db3ab2afc6fb6462ba4827bf18f`, parents/tree khớp Git local; mọi labels Ubuntu. Tám job gate-nhanh-manh có marker `nhanh_don_duoc_test.py` **not_measured/che_do_khong_xac_dinh**; gate-nhanh-gop không có marker cho lời gọi có đối số. Không Gate failed; summary **25** khớp.

Nguồn chỉ gồm stdout/provenance frozen, không có full log để kiểm full-log hashes hoặc replay parser cho từng job; không suy hash tự khớp là xác thực nguồn LIVE. WD luôn chưa đo, không dùng YAML tại SHA checkout thay cho mốc định nghĩa workflow theo §10.2.2.

**DANH SÁCH MUTANT VÀ HẠNG.** `mutants/results.json` giữ đầy đủ neo/thay, source, command, baseline/rc/output của **66 mutant ứng viên +2 tự kiểm**. Từng ca đích đã xanh trên bản sao source gốc; chỉ **rc3 + DO:<đúng-ca>: do TinHieuChotCa** tính GIET. `extra-mutants/results.json` giữ hai mutant Git, mỗi con chạy toàn33 ca. Tổng **70 mutant khác nhau đối với bộ ca ứng viên: 66 GIET, 3 SONG_SOT, 1 TIN_DUNG_GIA, 0 HONG**; một survivor là comment-only chủ ý, hai survivor thật là F08. Khi thêm ca reviewer, hai mutant F08 được đo lại và GIET; không đổi hạng SONG_SOT của chúng đối với bộ ca ứng viên. Các phản chứng đỏ trên candidate không được cộng vào số mutant.

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
| `A14_kich_ban_tu_dong_mau` | `c25_f02_env_mang_mau` | 0 → 3 | **GIET** |
| `A15_khoi_la_tap_con` | `c26_f02_dong_khong_mau` | 0 → 3 | **GIET** |
| `A16_bo_luat_toan_khoi` | `c27_f02_yaml_khong_toi_gian` | 0 → 3 | **GIET** |
| `A16_bo_khop_nguyen_van` | `c25_f02_env_mang_mau` | 0 → 3 | **GIET** |
| `A17i_cho_env_buoc` | `c28_che_do_env_buoc` | 0 → 3 | **GIET** |
| `A17ii_bo_env_job` | `c29_che_do_env_job` | 0 → 3 | **GIET** |
| `A17iii_cho_doi_so` | `c30_che_do_doi_so` | 0 → 3 | **GIET** |
| `che_do_bo_tien_to_VAR` | `c31_che_do_duong_khac` | 0 → 3 | **GIET** |
| `che_do_bo_env_workflow` | `c31_che_do_duong_khac` | 0 → 3 | **GIET** |
| `che_do_bo_defaults_workflow` | `c31_che_do_duong_khac` | 0 → 3 | **GIET** |
| `che_do_bo_defaults_job` | `c31_che_do_duong_khac` | 0 → 3 | **GIET** |
| `che_do_moi_shell` | `c31_che_do_duong_khac` | 0 → 3 | **GIET** |
| `che_do_bo_GITHUB_ENV` | `c31_che_do_duong_khac` | 0 → 3 | **GIET** |
| `A18_head_sha_thay_sha_checkout` | `c32_workflow_khong_doc_duoc` | 0 → 3 | **GIET** |
| `A18_yaml_hong_nem` | `c32_workflow_khong_doc_duoc` | 0 → 3 | **GIET** |
| `A19_lay_ung_vien_dau` | `c33_nhieu_ung_vien` | 0 → 3 | **GIET** |
| `F01_steps_chi_la_list` | `c22_thieu_dinh_danh_khong_passed` | 0 → 3 | **GIET** |
| `F05_chieu_khong_an_toan` | `c22_thieu_dinh_danh_khong_passed` | 0 → 3 | **GIET** |
| `F05_luoi_cuoi` | `c19_rest_loi` | 0 → 3 | **GIET** |
| `F02_khong_noi_dong` | `c23_chi_loi_goi_that` | 0 → 3 | **GIET** |
| `F02_cho_moi_co` | `c23_chi_loi_goi_that` | 0 → 3 | **GIET** |
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
| `git_ignore_sha` | toàn 33 ca ứng viên | 33/33 rc0 → 33/33 rc0 | **SONG_SOT** |
| `git_always_unavailable` | toàn 33 ca ứng viên | 33/33 rc0 → 33/33 rc0 | **SONG_SOT** |

Ca reviewer `git_workflow_source`: baseline **rc0**, `git_ignore_sha` và `git_always_unavailable` đều **rc3/DO:git_workflow_source**, GIET thật (`review-cases.json`). Đối chứng `control_simple` rc0; hai ca r4 gốc rc0 trên candidate. Hai ca `F02_collision_other_job` và `F02_missing_endgroup` đỏ bằng TinHieuChotCa đúng tên, không chết do setup/import/permission.

**Giới hạn và bàn giao.** A9 còn thiếu full acceptance trong runtime có khả năng ký fixture; A10 chưa có LIVE độc lập; A12/A13 và CI/required checks trên candidate chưa được đo. Native Windows/pwsh, release/full runtime gates, mạng/redirect thật, xác thực full logs và receipt vận chuyển cuối **not_run/KHÔNG ĐO ĐƯỢC** theo từng scope đã nêu; không coi skipped, dữ liệu thiếu hoặc lỗi môi trường là passed. Kết quả nội dung là **changes_requested** trên exact SHA đầu tệp, với F02 còn P0 và F08 P1. Executor/điều phối cần giữ hai slug này cho lượt kế tiếp và áp V5; reviewer không tự sửa sản phẩm hay tự mở lượt review khác.

**Snapshot cuối.** `snapshot-start.json`, `snapshot-end.json`, `snapshot-comparison.json` đối chiếu hash/size **5.376 tệp** ngoài `.git/` và `.review/`, gồm ignored/untracked và toàn `.review-input/`: **0 delta**. HEAD/tree không đổi; tracked diff, cached diff và untracked không ignored rỗng; các lệnh Git **rc0**. Ignored ngoài output review vẫn chỉ `.review-input/`. `.git/` không băm toàn metadata, được kiểm qua HEAD/tree/index/diff/status. Hai snapshot chỉ chứng minh không có delta quan sát tại hai mốc, không chứng minh chưa từng ghi rồi hoàn nguyên trong toàn lịch sử. Không có repository nguồn bên ngoài nào được cấp/quan sát.
