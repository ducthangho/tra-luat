verdict: changes_requested
reviewed_sha: 7c5742c3bf46a427b1525a86247c7448a6149948
base_sha: 76cf4c51a6b1a5a0f30621c73f9a6f03e7e68138
Reviewed commit: 7c5742c3bf46a427b1525a86247c7448a6149948
reviewed_tree: 994e22e0d6333a9cb9d422a6030dee24a647ee37
packet: wp899-r2-g1
review_round: 2
role: reviewer
provider: openai_codex
model_family: openai
execution_surface: codex_cli
transport: machine
independent_from_executor_session: true
review_axes: [spec, standards_security]
github_submitter_identity: null
assurance: review_deferred

Chưa đạt V2: **4 lớp mở, 10 nhóm biểu hiện; P0=2, P1=2, P2=0, P3=0**. F01 và F02 vẫn có thể tạo `passed` sai; F03 thiếu răng cho chốt total đổi; F05 còn đường lỗi không in dòng đếm. Suite ứng viên xanh **24/24 ca, 32/32 mutant**, nhưng hai mutant bổ sung sống qua **toàn bộ 24 ca**. Không coi suite xanh là đóng các lớp này.

Đây là review offline độc lập theo toàn bộ `.review-input/prompt.md`. Không gọi subagent, mạng/LIVE, GitHub, push, commit hoặc sửa mã ứng viên. Mọi hiện vật tạo ra nằm trong `.review/`. HINT là hướng để Executor tự tái dẫn xuất, không là patch sản phẩm hoặc authorization. Kết quả này không cấp `cross_approved`, quyền push/merge/land hoặc chuyển state.

**Preflight và phạm vi.** Đặc tả của assignment là `.review-input/wp899-r2.md`, đã đọc trọn và xác minh SHA-256 `d858c7c65a38a7f0fadda1cabf839c98ce70a881372d847c8979165925971707` (23.189 byte), revision 2/generation 1. Nguồn authority của lượt này là prompt được giao, gồm quyết định chủ kho issuecomment-6380183334: trần **3 tệp/900 dòng thêm** và đính chính A10 thành **13 checkout + chuan-bi not_measured**. Không báo hai quyết định ấy là finding; không dùng trần 700/kỳ vọng 14 checkout của bản spec cũ để chặn lượt này. Không xác minh lại GitHub authority/lease/state/budget từ xa trong phiên offline.

Origin `https://github.com/ducthangho/tra-luat.git`; detached HEAD đúng SHA/tree trên. Immutable acceptance baseline là `76cf4c51a6b1a5a0f30621c73f9a6f03e7e68138`; `merge-base --is-ancestor <base> HEAD` rc0. SHA lượt trước `f43ea20fafaee9596d8a5847534cb8489217df02` chỉ dùng đo delta sửa review, không thay baseline. Không có continuation base riêng được chỉ định. Đã đọc toàn mã mới và delta lượt trước; lưu `full.patch`, `delta.patch`, `numstat.txt`, `preflight.json`. Numstat rc0: `.claude/dev/ci_dang_ky_test.py` **1/0**, `ops/ci_provenance.py` **336/0**, `ops/ci_provenance_test.py` **468/0**, tổng **805 dòng thêm**, đúng write set. Mục MOI thêm đúng một dòng và dùng regex bằng tiền lệ `ops/land_evidence_nguon_test.py`.

**Môi trường/identity.** Linux, Python 3.13.17 (`/usr/bin/python`), PyYAML 6.0.3, Ruff 0.15.15, Git 2.43.0, codex-cli 0.164.0. Thread `01a16c4e-89f2-7e41-918e-c447bd91d87b`; `session_meta.id` khớp thread, `originator=codex_exec`, `model_provider=openai`. `turn_context` trong rollout của thread công bố **gpt-6.1-sol / effort xhigh**. Trích metadata ở `readback.json`/`readback.stdout.txt`, từ `/root/.codex/sessions/2026/10/24/rollout-2026-10-24T05-07-30-01a16c4e-89f2-7e41-918e-c447bd91d87b.jsonl`. Đây chỉ là **model do CLI công bố**; model phục vụ từng request **KHÔNG ĐO ĐƯỢC**. Không băm rollout còn đang ghi rồi dùng làm receipt cuối A13. Executor Claude/cloud/model_family=claude là thông tin trong spec, không phải runtime receipt độc lập do reviewer đo.

Sandbox thực tế `workspace-write`; read-only với mã ứng viên được giữ bằng assignment và snapshot, không tuyên bố toàn checkout bị OS khóa ghi. `core.abbrev` chưa cấu hình (rc1); không đổi bootstrap config, không chạy golden/doc-claims gate phụ thuộc nó. `codex --version` rc0 có cảnh báo không tạo được PATH aliases do filesystem read-only; không sửa quyền hoặc trust. Không có tool `environment_status` trong catalog của phiên; không suy readiness môi trường/mạng từ đó.

**Cách đọc bằng chứng.** Các lệnh bên dưới chạy từ gốc workspace qua `python -B .review/run.py <nhãn> <command...>`. Wrapper đặt `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR=<workspace>/.review/tmp`, cache ngoài mã ứng viên; mỗi `<nhãn>.receipt.json` ghi **command và rc con thật**, thời gian, hash stdout/stderr, kèm hai tệp output. Rc0 của script thu thập probe chỉ nói script hoàn tất; phải đọc rc/trạng thái con trong JSON. Phép đo là offline với REST/mock và fixture được ghi rõ, không giả thành CI/LIVE hoặc Windows thật.

ĐỐI CHIẾU LƯỢT TRƯỚC — nguồn `.review-input/VERDICT-luot1.md`, exact SHA `f43ea20fafaee9596d8a5847534cb8489217df02`. Đã dựng lại các phép đo từ mô tả vì script lượt 1 không được giao. Các nhãn “vá một phần” dưới đây là **VÁ HỜ ở cấp đóng lớp**, không phủ nhận các ca cũ đã được sửa thật.

| lớp lượt 1 | phân loại trên SHA hiện tại | phép đo độc lập và răng |
|---|---|---|
| F01 `thieu-dinh-danh-van-passed` | **VÁ HỜ — vá một phần, còn P0** | `probes.py`: bỏ lần lượt 6 trường Run/5 trường Gate nay ra `not_measured`; Run tối giản/jobs rỗng cũng vậy. Ba mutant F01 hiện có đều GIET đúng `c22`. Nhưng `run_attempt=true`, `check_suite_id=true`, metadata Gate rỗng, total sai kiểu vẫn được nhận; xem F01a–c. |
| F02 `nhac-ten-script-thanh-thuc-thi` | **VÁ HỜ — vá một phần, còn P0** | `printf` chỉ nhắc tên, comment và hậu tố `.py.bak/.other` nay không tạo marker. `real_moi.py` chạy shell thật với tên MOI thật chỉ ở comment: Gate `not_measured`. Ba mutant F02 GIET đúng `c23`. Nhưng toán tử trong nháy, operand `-W/-X` và dòng nối vẫn tạo lời gọi giả; xem F02a–c. |
| F03 `phan-trang-dem-thay-vi-chung-minh-du` | **VÁ HỜ ở evidence — sản phẩm sửa các ca cũ, còn P1 ở răng** | `probes.py`: jobs đủ có job failure ⇒ rc12; trang sớm rỗng/ID lặp ⇒ dedup, `tap_jobs=not_measured`, rc0, không còn khai đầy đủ. Artifacts cũng lưu total/so_id/trạng thái thiếu. Mutant bỏ completeness và bỏ dedup GIET đúng `c20`. Tuy nhiên gỡ riêng chốt total đổi sống **24/24** ca; baseline→mutant trên probe riêng đổi `not_measured→passed`, xem F03a. |
| F04 `rest-gia-khong-neo-run` | **ĐÃ VÁ THẬT trong phạm vi đo** | Run 6, jobs run 6, artifacts run 6 đều HTTP404; log ID không có cũng 404. Hai mutant sửa URL jobs/artifacts thành run+1 đều **rc3, GIET đúng c20**, baseline0. RestGia nay giữ ID nguồn riêng, không lấy ID trong response làm nguồn thẩm quyền. |
| F05 `duong-loi-bo-dong-dem-bat-buoc` | **VÁ HỜ — vá một phần, còn P1** | 403 tại cả run/jobs/log/artifacts: rc3, HTTP403, đúng một `NOT_MEASURED: 4`, không provenance. Đối số sai: rc2, dòng đếm hiện có. Mutant gỡ summary REST GIET đúng `c19`. Nhưng Run JSON sai dạng/lỗi ghi vẫn thoát rc1 và stdout rỗng; mutant gỡ summary lỗi đối số sống 24/24; xem F05a–c. |
| F06 `redirect-loi-thoat-ngoai-bo-boc` | **ĐÃ VÁ THẬT trong phạm vi đo** | `probes.py`: URLError/OSError trực tiếp và sau302 đều thành LoiRest; sau302→403/307 giữ mã HTTP; 302→200 giữ byte. Request lượt blob là chuỗi URL, không có Request mang header token. Hai mutant F06 ứng viên và mutant reviewer chỉ bỏ bọc lỗi **lượt redirect** đều GIET đúng `c24`. Không suy kiểm mạng thật từ mock. |
| F07 `a10-doi-sha-khi-checkout-skipped` | **ĐÓNG BẰNG AUTHORITY, không phải sửa mã** | Áp đính chính trong prompt. Tự băm frozen provenance, đọc lại 14 job, replay excerpt bằng parser và `git cat-file` cục bộ: **13 passed, chuan-bi 118368688427 not_measured**. SHA/parents/tree khớp; LIVE độc lập vẫn KHÔNG ĐO ĐƯỢC. Không yêu cầu công cụ dựng checkout SHA cho bước skipped. |

Giữ nguyên bảy slug nguồn, không đổi khóa để reset lịch sử. **Không có slug nguyên nhân mới**; biểu hiện mới được nối vào F01/F02/F03/F05. Bốn lớp mở có 10 nhóm dưới đây (F01a–c, F02a–c, F03a, F05a–c). F04/F06 được đóng bằng phép đo; F07 là disposition authority và không được tính là sửa sản phẩm. Nếu dùng tỷ lệ §12 trên U=7 lớp lượt trước, F={F04,F06}, tỷ lệ sửa thật **2/7=28,6%**, F07 báo riêng. Đây mới là một chuyển tiếp; không tự suy hai chuyển tiếp thấp hoặc chạm trần review. Bộ đếm calls/rounds từ xa KHÔNG ĐO ĐƯỢC.

BẢNG LỚP HIỆN TẠI — mỗi dòng một lớp, không tách biểu hiện thành lượt finding mới.

| lớp | hạng | biểu hiện (tệp:dòng) | phép đo tái hiện | HINT patch |
|---|---|---|---|---|
| **F01 `thieu-dinh-danh-van-passed`** | **P0** | **a.** `ops/ci_provenance.py:240`: `isinstance(True,int)` và `True==1` nhận `run_attempt=true`, `check_suite_id=true`; `head_sha="bad"` vẫn làm **Run passed** (Checkout riêng not_measured). **b.** `:224`: Gate nhận `runner_id=true`, `labels=[]/[false]`, `runner_name=""`, `conclusion=""/"unknown"`, `check_run_url=""/"wrong"`; thiếu `name`/`steps` cũng vẫn passed. `check_run_url=""` làm check_run_id=null. **c.** `:86`, `:88`, `:98`: total=true/1.0 hoặc id=true vẫn `du=True`, tập có thể passed; artifact chỉ có id được xuất metadata null với tập passed. | `python -B .review/probes.py`, rc0; `probes.json`: các `F01_run_value_*`, `F01_gate_value_*` cho **tool rc0 + Run/Gate passed** trên dữ liệu chưa đủ. `F03_shape_total_bool/total_float/id_bool` ghi nguyên kết quả `du=true`. Trường bị xóa/None đã được xử lý nhưng không khóa lớp dữ liệu không có định danh hợp lệ. | **Ở đâu:** validator dựng Run/Gate và helper collection, trước khi dùng marker/so đếm cấp passed. **Cách:** kiểm kiểu chính xác cho số (loại bool), giá trị có nghĩa của SHA/check-run ID, chuỗi/list bắt buộc không rỗng và phần tử đúng kiểu; ghi thiếu/sai dạng là chưa đo, giữ failed/skipped/not_run đã biết riêng. Không chỉ sửa c22 để khớp đầu ra hiện tại. **Khóa:** ma trận từng trường thiếu, bool, sai kiểu, rỗng; cả có/không jobs và artifacts; mutant nới từng predicate phải chết bởi ca đích. Giữ đối chứng metadata hợp lệ, skipped/runner0, M3 thiếu local object. **Rủi ro:** quá chặt với self-hosted labels hoặc null metadata hợp lệ của skipped; không hard-code danh sách runner, không coi thiếu thành failed. |
| **F02 `nhac-ten-script-thanh-thuc-thi`** | **P0** | **a.** `ops/ci_provenance.py:175`, `:182`: shlex bỏ dấu nháy; token literal `';'`/`'&&'` bị phân loại lại thành toán tử, `echo` thành gọi python. **b.** `:192`: chỉ bỏ token bắt đầu `-`, không biết arity; operand của `-W/-X` bị nhận là script, kể cả lệnh thật dùng `-c`. Ngược lại `python -W ignore <script>` không nhận script. **c.** `:202`: phân tích từng dòng thay vì khối/lệnh logic; `printf` nối dòng sang các đối số `python <script>` bị nhận thành thực thi. Python nối dòng và `.\ops\...` Windows bị bỏ/làm sai path trong probe parser. | `real_moi.py` rc0: shell thật **chỉ echo+cat** output suite đã lưu, không gọi Python; với `echo ';' python ops/ci_provenance_test.py; cat .review/suite.stdout.txt`, **shell_rc0, tool_rc0, Gate/marker passed** bằng MOI/regex thật. `probes.py` chạy shell thật với `-W/-X ... -c`: chỉ print marker, **không chạy script**, tool vẫn passed. Probe khối nhiều dòng xác nhận printf-continuation→passed. | **Ở đâu:** `loi_goi_python` và cách `do_dau_duong` đưa khối lệnh vào parser, vì lỗi xảy ra trước regex marker. **Cách:** giữ phân biệt literal/toán tử từ lexer, đọc lệnh logic sau nối dòng và phân biệt operand của tùy chọn interpreter; `-m/-c` không thành script. Grammar chưa chứng minh thì not_measured. Chọn grammar theo shell hoặc giới hạn hỗ trợ tường minh; không dùng POSIX shlex để khẳng định PowerShell. Cách rẻ là ngừng cấp bằng chứng cho cú pháp chưa được hiểu; cách đắt hơn là parser giữ quote/argv cho hai shell. **Khóa:** các ca âm ở phép đo với MOI thật, ca dương `python3 -B ./...`, `-W ignore script`, nối dòng, đường Windows; mutant mất quote provenance/bỏ operand/đọc từng dòng phải chết đúng ca. **Rủi ro:** sửa ngăn false positive nhưng bỏ luôn lời gọi hợp lệ; giữ fallback trung thực và không nhận chỉ vì có chuỗi marker. |
| **F03 `phan-trang-dem-thay-vi-chung-minh-du`** | **P1 — răng test** | `ops/ci_provenance_test.py:284`, `:377`; chốt sản phẩm `ops/ci_provenance.py:86` kiểm total ổn định nhưng c20 chỉ thử đủ/rỗng/lặp ID, không thử total đổi mà cuối cùng có đủ ID duy nhất theo total mới. Không mutant nào hiện có gỡ riêng chốt này. **a.** Vì thế không bảo vệ cả jobs và artifacts khỏi ghép hai snapshot. **Sản phẩm hiện tại xử lý đúng probe này**; finding là M8 thiếu phản chứng cho chốt bản vá. | `mutants.py`: `review_F03_bo_kiem_total_doi` **baseline0→mutant0, SONG_SOT c20 và 24/24 ca**. `targeted.py`: 3 trang với totals2→3→3, IDs1,2,3, TRANG1: baseline tap not_measured, mutant passed, cho cả hai collection. `review_cases.py review_total_changed_complete`: baseline0→mutant3, `DO:review_total_changed_complete:` do **TinHieuChotCa đúng ca**. | **Ở đâu:** mở rộng c20 hoặc thêm ca riêng và DOT_BIEN; không cần sửa logic sản phẩm đang đúng. **Cách:** fixture giữ trạng thái theo trang, total đổi nhưng số ID cuối vẫn đủ; đo đồng thời trạng thái collection và số lần đọc, áp jobs/artifacts. **Khóa:** thêm đúng mutant bỏ kiểm total; reviewer đã có ca chạy được tại `review_cases.py`, receipt `review-case-results.json`. Neo/thay ở `mutants.py` chỉ là dữ liệu test để Executor tự tái dẫn xuất. **Rủi ro:** ca chết vì thiếu trang/index hoặc vì count mismatch sẽ cấp tín dụng giả; phải đủ3ID và phân hạng đúng tín hiệu/tên ca. |
| **F05 `duong-loi-bo-dong-dem-bat-buoc`** | **P1** | **a.** `ops/ci_provenance.py:233`, `:237`, `:321`: REST HTTP200 nhưng JSON Run là list/null/string làm `.get` ném AttributeError ngoài LoiRest; không có dòng đếm. **b.** `:324`: lỗi ghi output OSError cũng thoát trước mọi báo cáo terminal. **c.** `ops/ci_provenance_test.py:143`: c01 chỉ kiểm rc2; gỡ summary của nhánh parse-args-error `ops/ci_provenance.py:314` không bị bộ ca/mutant bắt. | `targeted.py` chạy subprocess: Run `[]` ⇒ **rc1, stdout rỗng, AttributeError**; lỗi ghi được tiêm ⇒ **rc1, stdout rỗng, OSError**. `probes.py` thêm null/string. `review_F05_bo_dem_sai_doi_so` **SONG_SOT 24/24** ca. Ca bổ sung `review_arg_error_summary` baseline0→mutant3, đúng TinHieuChotCa/tên ca. Các nhánh REST403 hiện đã có summary và mutant c19 có răng. | **Ở đâu:** kiểm envelope REST trước khi dựng mốc và đường báo cáo terminal `main`, thay vì rải print ở vài except. **Cách:** chuyển body sai dạng sang hợp đồng lỗi dữ liệu hiện có; bảo đảm summary đúng một lần khi lỗi ghi/thu không tạo được provenance, giữ lỗi/rc và trạng thái không sinh hiện vật. Không đổi lỗi I/O thành HTTP403/rc3 hay pass để có summary; mã lỗi mới nếu cần phải được chủ kho chốt, không tự bịa ý nghĩa. **Khóa:** cả4 endpoint HTTP, đối số parse/semantic sai, JSON envelope sai và lỗi ghi có/không bản out cũ; kiểm stdout/rc/hiện vật riêng, thêm mutant gỡ summary riêng nhánh đối số/lỗi. Reviewer đã đo ca đối số đủ răng ở `review_cases.py`. **Rủi ro:** hai dòng đếm, nuốt lỗi lập trình bằng catch-all hoặc in0 khi bốn mốc chưa sinh; giữ M6 rollback và báo no-provenance rõ ràng. |

Các probe chỉ chứa dữ liệu/command vô hại cho parser, không tạo nội dung tấn công nhạy cảm. Hướng liên quan đường output/job-ID thoát phạm vi, symlink hoặc credential qua redirect chỉ được mô tả bằng lời; **không đo được** và không kết luận đã khai thác/đã an toàn. Đã quét đường mới theo prompt: shlex/quote/punctuation, -m/-c/-W/-X, nối dòng, Windows path; đủ/rỗng/trùng/total đổi/body sai dạng trong pagination; scalar bool/chuỗi/list rỗng; direct/redirect/nested HTTP; các đường terminal. Phạm vi là tập probe công bố, không là chứng minh parser hiểu mọi grammar shell.

ĐỐI CHIẾU A1–A11 (A12/A13 ghi thêm để không bỏ nghĩa vụ spec):

| tiêu chí | kết quả | bằng chứng / giới hạn |
|---|---|---|
| A1 | **passed** trong phạm vi | `python -B ops/ci_provenance.py thu --help` rc0, đủ4 cờ, `help.*`; tệp chưa có trên base (`cat-file -e` rc128). Mutant A1 GIET đúng c01. |
| A2/M2 | **A2 passed; M2 failed** | c02 và mutant bỏ so attempt đạt. F01 cho thấy trường sai kiểu/không định danh vẫn passed; không dùng ca attempt hẹp thay toàn M2. |
| A3 | **passed** phạm vi7 ca | c03–c09 Linux/Windows fixture, thiếu/two-SHA, push lệch, PR có/không parents đều qua. Các mutant tương ứng GIET đúng ca. Native Windows execution **not_run**, không suy từ fixture. |
| A4/M4 | **failed** | Năm ca nêu trong spec, import MOI động và marker đúng bước đều có răng. F01/F02 còn cấp passed sai. F03 thiếu regression cho total đổi. |
| A5 | **passed** | c16 và mutant path⇒passed GIET; workflow_definition vẫn not_measured, path chỉ là loi_khai_rest_path. Không nâng mốc workflow definition bằng REST. |
| A6 | **passed** phạm vi lỗi đã thử | c17 thử lỗi giữa chừng, giữ bản cũ/không tạo out; mutant ghi thẳng GIET đúng ca. Không đo crash/power loss, writer cạnh tranh hoặc native Windows. F05 lỗi I/O mất summary không có nghĩa rollback A6 sai. |
| A7/M7 | **A7 hẹp passed; M7 failed** | c18 ghi đúng NOT_MEASURED1/rc0; c19 đủ4 endpoint403, rc3+403+summary4. Mutant gỡ summary bình thường/gộp rcREST/gỡ summaryREST đều GIET. F05 còn nhánh không có dòng đếm và răng lỗi đối số thiếu. |
| A8/M8 | **suite passed; M8 failed** | `suite.receipt.json`: rc0, CA24/24, DOT BIEN32/32, TU KIEM DAT(3), TONG DAT. Phân hạng giữ2 tín dụng giả là TIN_DUNG_GIA và comment-only là SONG_SOT. Hai mutant reviewer thật vẫn sống24/24, nên “có đột biến cho từng chốt” chưa được chứng minh. Fixture hash qua c21; nguồn log thật Windows đầy đủ KHÔNG ĐO ĐƯỢC. |
| A9 | **lệnh failed rc1; full acceptance KHÔNG ĐO ĐƯỢC** | `python -B .claude/dev/ci_dang_ky_test.py --chay`: in ĐĂNG KÝ25/25, LAUNCHER WINDOWS4/4, RUFF CI3/3 rồi dừng ở lệnh **git commit kho tạm rc128**, trước chay_moi. Traceback không chứa stderr của git con; nguyên nhân sâu ở lượt này chưa đo, không tự suy là lỗi diff. `registry.*` giữ bằng chứng. Probe `kiem()` thật: errors=[],25/25; gỡ riêng mục bằng tham số registry:25/24, báo đúng `test sống chưa đăng ký: ops/ci_provenance_test.py`. Regex MOI thật nhận output suite. Phần nối/âm đạt, không thay full --chay hoặc khai đã thấy test được chạy trong lệnh ấy. |
| A10 | **frozen/readback phù hợp authority; LIVE độc lập KHÔNG ĐO ĐƯỢC** | `readback.py`:14/14jobs, mọi labels `[ubuntu-latest]`; checkout13passed+1not_measured, SHA b27fe85c9e9593ddbb059808fe4347fe1bd267be, parents5618020a67709ca6f2c93138905df0aa8d9c2df6+400589368e09ab2ee0e734b7af08b93478035503, tree857bc47e6bc5f0024e442b400819ac51286dfc55. Băm provenance **5bb3559772344875fe043b33cdd26f62e80e592826d75ea31f7edcd2bfd1c575** khớp stdout giao kèm. Parser replay excerpt và local Git khớp. Workflow_definition và14 Gate jobs not_measured; NOT_MEASURED16 khớp, không tự nâng chúng. Không có full logs/HTTP receipt độc lập để kiểm hash full log hoặc chứng minh nguồn LIVE mới trên candidate. |
| A11 | **passed** theo trần900 được giao | doctrine-scan rc0:10tệp,0chép doctrine; adr-song rc0:53/53,khớp1–1 (tha0016); bare Ruff trên đúng2tệp mới rc0, All checks passed; numstat3tệp/805. `git diff --check <base> HEAD` rc0. Ruff pin/probe contract đo riêng `loi_ruff_ci()=([],3)`, không dùng thay bare lint. |
| A12/V1–V4 | **KHÔNG ĐO ĐƯỢC remote/future** | Offline, không ls-remote, push hoặc connector receipt; bảng lớp còn P0/P1 nên V2 trước đẩy chưa đạt. Không tự gọi connector hoặc tạo state. |
| A13 | **KHÔNG ĐO ĐƯỢC hoàn chỉnh** | Có metadata CLI/tham chiếu rollout đúng thread, nhưng stdout thread.started, launcher run.json và bản rollout/hash sau khi writer kết thúc chưa được reviewer thu đầy đủ. Bên vận chuyển phải thu1–5 sau run và readback. Không lấy file đang ghi hay GitHub submitter làm model identity. |

DANH SÁCH MUTANT VÀ HẠNG. Đã chạy riêng trên bản sao `.review/mutants/` qua **`python -B ... --mot-ca <tên>`**. Mỗi ca đích có baseline rc0; chỉ mutant rc3 và `DO:<đúng-ca>:` từ đường bắt **TinHieuChotCa** mới tính GIET. `mutants/results.json` ghi rc từng con, output riêng ở `mutants/<tên>.txt`, source mutant giữ nguyên để tái hiện. Tổng **38 mutant khác nhau:33 GIET,3 SONG_SOT,2 TIN_DUNG_GIA**; 1 SONG_SOT là đối chứng vô hại,2 là thiếu răng thật. Không cộng tín dụng giả vào số giết.

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
| `F03_tap_luon_du` | `c20_du_trang` | 0 → 3 | **GIET** |
| `F03_trung_id_van_them` | `c20_du_trang` | 0 → 3 | **GIET** |
| `F04_jobs_run_khac` | `c20_du_trang` | 0 → 3 | **GIET** |
| `F04_artifacts_run_khac` | `c20_du_trang` | 0 → 3 | **GIET** |
| `F01_run_thieu_van_passed` | `c22_thieu_dinh_danh_khong_passed` | 0 → 3 | **GIET** |
| `F01_gate_thieu_van_passed` | `c22_thieu_dinh_danh_khong_passed` | 0 → 3 | **GIET** |
| `F01_checkout_head_thieu` | `c22_thieu_dinh_danh_khong_passed` | 0 → 3 | **GIET** |
| `F02_bo_doi_token_python` | `c23_chi_loi_goi_that` | 0 → 3 | **GIET** |
| `F02_hau_to_py` | `c23_chi_loi_goi_that` | 0 → 3 | **GIET** |
| `F02_khong_tach_toan_tu` | `c23_chi_loi_goi_that` | 0 → 3 | **GIET** |
| `F05_rest_mat_dong_dem` | `c19_rest_loi` | 0 → 3 | **GIET** |
| `F06_redirect_lot_loi` | `c24_goi_that_loi_va_chuyen_huong` | 0 → 3 | **GIET** |
| `F06_redirect_mang_token` | `c24_goi_that_loi_va_chuyen_huong` | 0 → 3 | **GIET** |
| `vo_can_AttributeError_qua_except_doi_kieu` | `c03_checkout_linux` | 0 → 4 | **TIN_DUNG_GIA** |
| `vo_can_KeyError` | `c03_checkout_linux` | 0 → 4 | **TIN_DUNG_GIA** |
| `chi_them_chu_thich` | `c20_du_trang` | 0 → 0 | **SONG_SOT** |
| `review_F03_bo_kiem_total_doi` | `c20_du_trang` | 0 → 0 | **SONG_SOT** |
| `review_F05_bo_dem_sai_doi_so` | `c01_cli_du_co` | 0 → 0 | **SONG_SOT** |
| `review_F06_chi_boc_loi_luot_dau` | `c24_goi_that_loi_va_chuyen_huong` | 0 → 3 | **GIET** |

Hai mutant `review_F03_bo_kiem_total_doi` và `review_F05_bo_dem_sai_doi_so` được chạy thêm qua **mọi ca hiện có**, mỗi mutant24/24rc0 (`mutants/*.all-cases.json`). Sau đó reviewer viết ca đặc tả độc lập trong `.review/review_cases.py`: `review_total_changed_complete` và `review_arg_error_summary`; **cả hai baseline0→mutant3, đúng TinHieuChotCa/tên ca**, xem `review-case-results.json` và `review-cases.*`. Đây là bằng chứng test có thể khóa tính chất, chưa phải test được tích hợp vào ứng viên. Không áp patch sản phẩm vào cây review.

`review_total_changed_complete` chạy jobs rồi artifacts; tín hiệu mutant chết ở jobs là đủ chứng minh đường chung sai, còn `targeted.json` đo A/B từng collection độc lập và xác nhận cả hai. Ca hiện có32mutant được chạy lại qua cả suite và bộ đo liệt kê; lần liệt kê để giữ receipt từng mutant, không dùng một số tổng thay việc phân hạng.

**Tình trạng cuối và giới hạn.** Snapshot đầu/cuối `snapshot-start.json`, `snapshot-end.json` băm/đo kích thước **5264 tệp ngoài .git/ và .review/**, gồm ignored/untracked, `.review-input/` và `.codex/`: **0 delta**. HEAD/tree không đổi; status tracked/untracked (không ignored), diff và cached diff đều rỗng rc0. Ignored vẫn là `.codex/`, `.review-input/`, `.review/`. `.git/` không băm toàn bộ metadata; được đối chiếu qua HEAD/tree/index/diff/status. Hai snapshot chỉ chứng minh không có delta quan sát tại hai mốc, không chứng minh lịch sử chưa từng ghi rồi hoàn nguyên.

Native Windows, CI candidate, mạng/redirect thật, full log authenticity, remote lease/ref freshness, review call budget, launcher terminal receipt và delivery receipt **KHÔNG ĐO ĐƯỢC**. Full runtime/release gates **not_run** vì phạm vi là công cụ dev-side/acceptance A1–A13, không sửa runtime/release. Không có required check skipped nào được coi passed; fixture/test mô phỏng skipped vẫn giữ nguyên ý nghĩa skipped/not_run. Cần Executor khép F01/F02/F03/F05 trong write set và đưa exact SHA mới ra review; A9/A10/A12/A13 vẫn cần evidence đúng môi trường/thời điểm. Không dùng verdict này làm approval hoặc quyền land.
