verdict: changes_requested
reviewed_sha: 5ab75a4ca5b237f881a5be9ea97047d3f9395115
base_sha: 76cf4c51a6b1a5a0f30621c73f9a6f03e7e68138
Reviewed commit: 5ab75a4ca5b237f881a5be9ea97047d3f9395115
reviewed_tree: 2c32262ae078c008d9156bb44dbbe7716d92feb6
packet: wp899-r2-g1
review_round: 3
role: reviewer
provider: openai_codex
model_family: openai
model: gpt-6.1-sol
effort: xhigh
session_id: 01a16c5f-9c4a-7d32-9ac6-3df086949dbf
model_reviewer_identity: openai_codex/gpt-6.1-sol/01a16c5f-9c4a-7d32-9ac6-3df086949dbf (CLI-published; per-request not_measured)
execution_surface: codex_cli
transport: machine
independent_from_executor_session: true
review_axes: [spec, standards_security]
github_submitter_identity: null
assurance: review_deferred

Chưa đạt V2: **3 lớp mở, 8 nhóm biểu hiện; P0=2, P1=1, P2=0, P3=0**. F01/F02 vẫn tạo `passed` sai; F05 còn lỗi thu dữ liệu thoát mà không in dòng đếm. **F03 đã vá thật** trong phạm vi kiểm độc lập; F04/F06 giữ đóng; F07 giữ disposition authority. Suite ứng viên đạt **24/24 ca, 46/46 mutant**, nhưng 11 phản chứng đặc tả bổ sung đều làm candidate hiện tại đỏ đúng chốt, với một đối chứng hợp lệ xanh.

**Điều kiện dừng đã chạm:** F01, F02, F05 xuất hiện ở cả lượt 1, 2, 3. Đây là **LẶP LỚP**, không phải slug mới. Theo `dieu_kien_dung` của wp899-r2, Executor phải **DỪNG và đưa checkpoint cho chủ kho**, kèm verdict/bằng chứng này; không tự mở vòng vá/lượt gọi tiếp. Kết quả không cấp approval, `cross_approved`, quyền đẩy/merge/land hoặc chuyển state. HINT bên dưới là dữ liệu để quyết định/tái dẫn xuất, không cấp authority tiếp tục.

Review này thực hiện toàn bộ `.review-input/prompt.md`, không dùng subagent, không đăng GitHub, không push hoặc sửa mã ứng viên. Mọi tệp tạo ra nằm trong `.review/`. Không dùng mạng để thu CI/LIVE. Lệnh registry có tiến trình ký commit của fixture thử socket loopback và bị sandbox từ chối; ghi riêng ở A9, không coi là phép đo GitHub.

**Preflight và authority.** Đã đọc trọn spec được giao `.review-input/wp899-r2.md`: **23.189 byte**, SHA-256 **d858c7c65a38a7f0fadda1cabf839c98ce70a881372d847c8979165925971707**, khớp assignment, revision 2/generation 1. Origin `https://github.com/ducthangho/tra-luat.git`; detached HEAD đúng OID/tree nêu trên. Immutable acceptance baseline là `76cf4c51a6b1a5a0f30621c73f9a6f03e7e68138`; phép ancestor rc0. SHA lượt 2 `7c5742c3bf46a427b1525a86247c7448a6149948` chỉ dùng đo delta, không dời baseline; không có continuation base riêng được giao.

Áp quyết định chủ kho issuecomment-6380183334 **theo authority trong prompt**: trần **3 tệp/900 dòng thêm**, A10 là **13 checkout + chuan-bi not_measured**. Không dùng trần 700/kỳ vọng 14 checkout cũ để tạo finding. Remote authority/lease/state/budget hiện hành **KHÔNG ĐO ĐƯỢC** trong lượt offline, không tự nhận đã xác minh từ GitHub.

`git diff --numstat <base> HEAD` rc0: `.claude/dev/ci_dang_ky_test.py` **1/0**, `ops/ci_provenance.py` **352/0**, `ops/ci_provenance_test.py` **524/0**, tổng **877 dòng thêm**, đúng ba tệp write set. Đã đọc toàn bộ hai tệp mới, diff toàn bộ và delta lượt 2; mục MOI thêm đúng một dòng, regex bằng tiền lệ `ops/land_evidence_nguon_test.py`. `git diff --check <base> HEAD` rc0. Artifacts: `preflight.json`, `full.patch`, `delta.patch`, `numstat.txt`.

**Môi trường và identity.** Linux x86_64, Python **3.13.17** (`/usr/bin/python`), PyYAML **6.0.3**, Git **2.43.0**, Ruff **0.15.15**, codex-cli **0.164.0**. Thread từ môi trường run: `01a16c5f-9c4a-7d32-9ac6-3df086949dbf`; `session_meta.id` trùng, `originator=codex_exec`, `model_provider=openai`. `turn_context` công bố **gpt-6.1-sol / effort xhigh**, nguồn `/root/.codex/sessions/2026/10/24/rollout-2026-10-24T05-26-08-01a16c5f-9c4a-7d32-9ac6-3df086949dbf.jsonl`, chỉ trích metadata vào `preflight.json`. Đây là **model do CLI công bố**; model phục vụ từng request **KHÔNG ĐO ĐƯỢC**. Không băm rollout đang ghi rồi gọi đó là receipt cuối A13. Executor Claude/cloud/model_family=claude là thông tin spec, chưa có runtime receipt độc lập của Executor trong assignment.

Sandbox thực tế `workspace-write`; ràng buộc read-only với candidate được thực hiện bằng assignment và snapshot, không tuyên bố toàn checkout bị OS khóa ghi. `core.abbrev` chưa cấu hình (rc1); không đổi config/bootstrap, không chạy golden/doc-claims phụ thuộc nó. `codex --version` rc0 có cảnh báo không tạo được PATH aliases do filesystem read-only; không sửa quyền/trust. Catalog không có `environment_status`, không suy readiness từ sự vắng mặt ấy.

**Cách tái hiện.** Chạy từ gốc workspace bằng `python -B .review/run.py <nhãn> <command...>`. Wrapper đặt `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR=<workspace>/.review/tmp`, cache trong `.review/`; `<nhãn>.receipt.json` ghi command, **rc con thật**, thời gian, size/hash stdout/stderr. Mỗi output được giữ nguyên trong `<nhãn>.stdout.txt`/`.stderr.txt`. Rc0 của script thu thập chỉ nói thu thập xong; đọc trạng thái/rc con trong JSON để kết luận. Các thử nghiệm là offline; không giả fixture Windows hoặc mock REST thành Windows/CI/LIVE thật.

**ĐỐI CHIẾU F01–F07.** Nguồn gần nhất `.review-input/VERDICT-luot2.md`, SHA `7c5742c3bf46a427b1525a86247c7448a6149948`; lịch sử lượt 1 `.review-input/VERDICT-luot1.md`, SHA `f43ea20fafaee9596d8a5847534cb8489217df02`. Script cũ không được giao; đã dựng lại phép đo từ mô tả, giữ nguyên slug nguồn. “Vá một phần” bên dưới là **VÁ HỜ ở cấp đóng lớp**, không phủ nhận bản vá đúng ở những biểu hiện cũ.

| lớp nguồn | phân loại trên HEAD này | phép đo lượt 2 chạy lại và răng bản vá |
|---|---|---|
| F01 `thieu-dinh-danh-van-passed` | **VÁ HỜ — vá một phần; còn P0, LẶP LỚP lần 3** | `probes.json`: bỏ từng trường Run/Gate, bool-as-int, SHA `bad`, labels rỗng/sai phần tử, conclusion/check URL rỗng nay không còn passed; total bool/float, ID bool bị LoiRest. Run tối giản/jobs rỗng không còn passed. Các mutant predicate F01 đều GIET đúng c22. Nhưng `steps=[]/[{}]` vẫn Gate passed; SHA/check URL có newline cuối vẫn qua kiểm định danh; xem bảng lớp. |
| F02 `nhac-ten-script-thanh-thuc-thi` | **VÁ HỜ — vá một phần; còn P0, LẶP LỚP lần 3** | Chạy lại quoted operator, operand `-W/-X` bằng shell thật + MOI thật: nay Gate not_measured; comment, `.py.bak`, `-m/-c`, đường Windows và dòng nối printf cũng không sinh marker. Bỏ sót lời gọi hợp lệ ngoài allowlist là chủ ý, không báo thành lỗi. Bốn mutant F02 GIET đúng c23. Nhưng xử lý từng dòng trong khối nhiều dòng vẫn nhận dữ liệu/nhánh không chạy thành lời gọi, xem bảng lớp. |
| F03 `phan-trang-dem-thay-vi-chung-minh-du` | **ĐÃ VÁ THẬT trong phạm vi đo** | `round2_exact_total_changed_jobs/artifacts` dựng lại **TRANG=1, totals 2→3→3, IDs 1/2/3**: collection đích not_measured dù cuối đủ 3 ID; nay còn đọc trang 4 rỗng. Mutant bỏ riêng kiểm total đổi **baseline0→mutant3, GIET đúng c20**; không còn sống như lượt 2. Đã đo thêm đủ/rỗng/trùng, total khai thấp, exact multiple, lặp full page với trần 3, envelope sai dạng: không khai đủ sai. Các mutant phân trang/dedup/completeness đều GIET đúng c20. |
| F04 `rest-gia-khong-neo-run` | **GIỮ ĐÃ VÁ THẬT trong phạm vi đo** | Run6, jobs của run6, artifacts của run6 và log ID lạ đều404. Hai mutant chuyển URL jobs/artifacts sang run+1 **baseline0→3, GIET đúng c20**. RestGia vẫn neo ID nguồn riêng; không lấy ID trong response làm authority cho route. |
| F05 `duong-loi-bo-dong-dem-bat-buoc` | **VÁ HỜ — vá một phần; còn P1, LẶP LỚP lần 3** | Đo subprocess: HTTP403 ở cả4 endpoint ⇒ rc3 +403 + đúng một summary4; Run `[]/null/string` nay rc3 +summary4; lỗi ghi được tiêm ⇒ rc1 +LOI_GHI +summary4. Mutant gỡ summary lỗi đối số nay **GIET đúng c01**, hai mutant body/ghi GIET đúng c19. Nhưng metadata job sai dạng còn làm thu() ném trước summary, xem bảng lớp. |
| F06 `redirect-loi-thoat-ngoai-bo-boc` | **GIỮ ĐÃ VÁ THẬT trong phạm vi đo** | URLError/OSError trực tiếp và sau302 đều LoiRest; 302→403/307 giữ mã, 302→200 giữ bytes. Request lượt blob là chuỗi URL, không mang Request/Authorization. Hai mutant F06 ứng viên và mutant chỉ bỏ bọc lỗi lượt redirect đều **GIET đúng c24**. Đây là mock, không chứng minh đường mạng thật. |
| F07 `a10-doi-sha-khi-checkout-skipped` | **ĐÓNG BẰNG AUTHORITY, không phải sửa mã** | Áp đính chính prompt; tự băm và đọc frozen A10, replay excerpt bằng parser candidate + Git cục bộ:13passed, chuan-bi118368688427 not_measured; SHA/parents/tree đúng. LIVE độc lập vẫn KHÔNG ĐO ĐƯỢC. |

Tập mở cuối lượt2 U={F01,F02,F03,F05}; tập sửa thật đã kiểm ở lượt3 F={F03}, tỷ lệ **1/4=25%**. Không có slug nguyên nhân mới. Ba lớp mở có **8 nhóm biểu hiện**: F01a–b, F02a–d, F05a–b. F04/F06 không tái mở; F07 không được tính là sửa sản phẩm. Lượt2 ghi tỷ lệ chuyển tiếp trước là2/7; đó là evidence kế thừa, không phải phép đo mới của lượt3. Điều kiện dừng theo lớp lặp lần3 đã đủ độc lập với phép tính tỷ lệ hay số calls từ xa.

**BẢNG LỚP HIỆN TẠI.** Mỗi dòng một slug nguyên nhân. Tất cả ba lớp đều là tái diễn từ lượt1/lượt2 trên các SHA nêu trên; không tách slug mới cho biểu hiện mới.

| lớp | hạng | biểu hiện (tệp:dòng) | phép đo tái hiện | HINT patch |
|---|---|---|---|---|
| **F01 `thieu-dinh-danh-van-passed`** | **P0** | **a.** `ops/ci_provenance.py:50`, `:227`, `:234`: chỉ kiểm steps là list; `[]`, `[{}]`, hoặc bước có name rỗng/conclusion null vẫn tạo **Gate passed**, `thieu=[]`, thiếu danh sách bước có định danh/conclusion M4. **b.** `:29`, `:33`, `:47`, `:50`: `match` với `$` nhận cả newline cuối. `head_sha=H+newline`, jobs rỗng ⇒ **Run passed, rc0**; check_run_url có newline ⇒ **Gate passed, rc0**, check_run_id mang newline. | `python -B .review/run.py probes python -B .review/probes.py` rc0, `probes.json` các `gate_value_steps_0/1/2`. `real-moi.json`: `empty_steps`, `empty_step_object`, `blank_step`, `check_url_newline`, `head_sha_newline_no_jobs` giữ stdout/provenance tương ứng. Các `review_steps_need_metadata`, `review_oid_full_string`, `review_check_run_full_string` đều **rc3 do TinHieuChotCa đúng tên**, đối chứng valid rc0. Không suy “rc0 là pass”: ở đây chính mốc Run/Gate ghi passed sai. | **Ở đâu:** validator Run/Job trước khi dựng mốc và trước projection steps, vì tính đúng của marker không bổ sung được định danh thiếu. **Cách:** kiểm cấu trúc/phần tử steps có name/conclusion hợp lệ, giữ riêng bước skipped/null thực sự chưa đo; dùng phép khớp toàn chuỗi cho các định danh cố định, không chuẩn hóa dữ liệu bẩn thành hợp lệ. Vá chung predicate, không chỉ thêm giá trị vào c22. **Khóa:** ma trận steps thiếu/rỗng/sai phần tử/name/conclusion, SHA/check URL có ký tự đuôi; giữ đối chứng hợp lệ và job skipped/runner0. Mutant nới mỗi predicate/neo phải chết đúng ca; mẫu `review_cases.py` hiện làm candidate đỏ đúng lỗi. **Rủi ro:** siết mọi conclusion của bước thành success sẽ nhận sai các bước skipped; không hard-code tên runner hoặc biến thiếu thành failed. |
| **F02 `nhac-ten-script-thanh-thuc-thi`** | **P0** | `ops/ci_provenance.py:193`, `:203`, đặc biệt `:212`: allowlist áp trên **từng dòng** sau nối backslash, không giữ ngữ cảnh toàn khối. Dòng `python <MOI>` nằm trong **a.** nhánh `if false`, **b.** hàm chưa gọi, **c.** chuỗi nháy nhiều dòng, **d.** dữ liệu heredoc đều được nhận là thực thi; marker ở phần output khác của cùng bước làm Gate passed. Không phải lỗi bỏ sót lời gọi hợp lệ ngoài allowlist. | `python -B .review/run.py real-moi python -B .review/real_moi.py` rc0. Bốn case `disabled_branch`, `uninvoked_function`, `quoted_text`, `heredoc` chạy **bash -e -x thật**, chỉ false/printf/cat hoặc định nghĩa hàm; trace không gọi Python. Dùng **MOI/regex thật của ops/ci_provenance_test.py**, cat stdout suite đã lưu: **shell_rc0, tool_rc0, Gate/marker passed** cả4. Đối chứng comment và ba biểu hiện lượt2 đều not_measured. Full log, trace, output/provenance ở `real-moi/<case>/`; bốn `review_context_*` rc3 đúng chốt. | **Ở đâu:** đường đưa khối từ `tach_buoc` qua `dong_logic` tới `do_dau_duong`, vì regex từng dòng không chứng minh dòng ấy là câu lệnh được thực thi. **Cách rẻ:** chỉ nhận khối đã được chứng minh thuộc grammar tối giản ở cấp **toàn khối**, từ chối sinh evidence khi còn cấu trúc/ngữ cảnh chưa hiểu; giữ metadata shell/env của Actions tách khỏi lệnh. **Cách đắt:** parser giữ quote, continuation và cấu trúc theo shell. Không vá bằng blacklist riêng if/function/heredoc. **Khóa:** bốn case thực chạy ở trên, ca nối dòng Python/printf và đối chứng simple call; mutant làm rơi trạng thái quote/control hoặc quay về quét từng dòng phải chết đúng ca. **Rủi ro:** từ chối cả khối hợp lệ hoặc coi shell metadata là lệnh; giữ not_measured trung thực và đo riêng PowerShell, không dùng parser Bash để khẳng định PowerShell. |
| **F05 `duong-loi-bo-dong-dem-bat-buoc`** | **P1** | **a.** `ops/ci_provenance.py:224`: check_run_url là int hoặc list khác rỗng ⇒ gọi `.rsplit` trước validator, AttributeError. **b.** `:227`: steps là string, hoặc list chứa scalar ⇒ `.get` trên phần tử sai dạng, AttributeError. Cả hai lọt qua `main` tại `:331`–`:340`: thu chỉ bọc LoiRest, summary cho lỗi ghi không bao phủ lỗi thu. Không có dòng NOT_MEASURED như M7 yêu cầu. | `terminal_child.py` chạy bằng subprocess thật qua `probes.py`: `check_url_int`, `check_url_list`, `steps_str`, `steps_list_scalar` đều **rc1, stdout rỗng, AttributeError**, không provenance. Output riêng `terminal-<case>.stdout.txt/.stderr.txt`, rc ở `probes.json`. Bốn `review_summary_*` **rc3 do đúng TinHieuChotCa**, đối chứng HTTP403/Run sai envelope/lỗi ghi đã có summary. | **Ở đâu:** xác thực dữ liệu trước projection trong moc_gate và đường báo cáo terminal main, vì thêm một except riêng cho Run/ghi chỉ đóng những cửa đã biết. **Cách:** dữ liệu REST sai dạng phải đi qua hợp đồng lỗi dữ liệu đang có, và đường thu kết thúc phải báo đúng một summary dù chưa sinh provenance; giữ lỗi/rc thật, không đổi lỗi lập trình thành HTTP403 hoặc pass. Không dùng catch-all nuốt mọi lỗi để làm suite xanh. **Khóa:** field shape theo bảng bắt buộc, cả steps lẫn check URL, cộng4 endpoint/đối số/ghi với có-không out cũ; kiểm rc, summary và không sinh hiện vật riêng. Mutant cho lỗi thu đi vòng qua báo cáo terminal phải chết đúng tên ca; đã có ca tái hiện chạy được. **Rủi ro:** in hai summary, che lỗi lập trình hoặc phá rollback M6; không in0 khi bốn mốc chưa được sinh. |

Các ca mới ở `review_cases.py` là **phản chứng chạy trên candidate chưa sửa**, không phải mutant và không cộng vào số mutant. `review-cases.json` ghi **1 đối chứng rc0 +11 ca rc3**, mọi ca đỏ do chính `bang()`/TinHieuChotCa và đúng tên, không chết bởi setup/import/permission. Nhãn rank của helper chỉ dùng nhận dạng tín hiệu; không có lời khai đã vá sản phẩm. Không áp patch sản phẩm, không sinh product patch-as-hint.

**Quét các đường mới và giới hạn.** `probes.json` chứa107 nhóm đo (con số nhóm, không phải số acceptance hay số ca suite). Đã kiểm parser một/nhiều dòng, nối backslash, `python -m/-c`, `-W/-X`, toán tử trong nháy, PowerShell/Windows path; các dạng ngoài allowlist được bỏ là chủ ý. PowerShell backtick-continuation mô phỏng còn tạo marker, nhưng native PowerShell **not_run**; không dùng nó thay bốn phản chứng Bash thật. Phân trang được đo đủ/rỗng/lặp/total đổi/total khai thấp/exact multiple, body sai dạng và giới hạn vòng lặp; giữ F03 đóng trong tập đó. Vị từ số loại bool, chuỗi/list rỗng đã đo từng trường; `digest` hiện chỉ kiểm prefix và giữ null, không có phép đo xác thực nội dung artifact/hash nên không khai đã xác thực byte artifact. Redirect được đo trực tiếp/hai lượt/lỗi lồng bằng mock, không qua mạng thật. Đường help có trong receipt A1; các nhánh kết thúc khi thực thu dữ liệu, parse lỗi và ghi lỗi được đo riêng ở F05.

Không tự soạn phản chứng nhạy cảm. Các hướng liên quan thoát phạm vi output/job-ID, symlink hoặc credential qua redirect chỉ được mô tả bằng lời, **KHÔNG ĐO ĐƯỢC**; không tuyên bố đã khai thác hoặc đã đóng chúng. Bảng probe không là chứng minh bao quát mọi grammar, kiểu dữ liệu, race hoặc giao thức mạng.

**ĐỐI CHIẾU A1–A11; ghi thêm A12/A13 để giữ nghĩa vụ spec.**

| tiêu chí | kết quả | evidence / phạm vi |
|---|---|---|
| A1 | **passed** phạm vi tiêu chí | `python -B ops/ci_provenance.py thu --help` rc0, đủ4 cờ; tệp chưa có trên base (`cat-file -e` rc128). Mutant A1 GIET đúng c01. |
| A2/M2 | **A2 passed; M2 chưa đạt toàn bộ** | c02 và mutant bỏ so attempt đạt. F01b vẫn làm Run passed với SHA sai định dạng; không dùng ca attempt hẹp để đóng M2. |
| A3 | **passed** phạm vi7 ca và mutant yêu cầu | c03–c09 đo fixture Linux/Windows, không SHA/hai SHA, push lệch, PR có/không parents và thiếu local object; các mutant tương ứng GIET đúng ca. Native Windows **not_run**, không suy execution Windows từ fixture. |
| A4/M4 | **failed** | Năm ca nguyên spec, import MOI động và marker đúng bước đều có răng. Nhưng F01/F02 còn sinh passed sai. Steps rỗng/không định danh và dòng Python thuộc dữ liệu/control context chưa được ca sẵn có khóa. |
| A5 | **passed** | c16 + mutant path⇒passed GIET; workflow_definition giữ not_measured, path chỉ là loi_khai_rest_path. |
| A6 | **passed** phạm vi lỗi đã thử | c17 lỗi giữa chừng, có/không bản out cũ, không để out nửa vời; mutant ghi thẳng GIET đúng c17. Chưa đo crash/power loss, writer cạnh tranh hay native Windows. |
| A7/M7 | **A7 hẹp passed; M7 failed** | c18 summary1/rc0; c19 cả4 endpoint403/rc3/summary4. Các mutant bỏ summary/gộp rc đều GIET. Các cửa F05a/b vẫn thoát rc1 và mất summary. |
| A8 | **passed** phần định dạng/số ca/đột biến; không đóng các lớp lỗi | `suite.receipt.json`: rc0, **CA24/24, DOT BIEN46/46, TU KIEM DAT(3), TONG DAT**. Liệt kê lại từng mutant ở bảng sau;2 tín dụng giả được giữ đúng hạng. Fixture hash qua c21; nguồn full log Windows độc lập KHÔNG ĐO ĐƯỢC. Suite xanh không chứng minh semantics F01/F02/F05. |
| A9 | **lệnh failed rc1 do môi trường; full acceptance KHÔNG ĐO ĐƯỢC** | `python -B .claude/dev/ci_dang_ky_test.py --chay`: ĐĂNG KÝ25/25, LAUNCHER WINDOWS4/4, RUFF CI3/3 rồi dừng trước chay_moi. `registry-detail.*` đo stderr child: **git commit fixture rc128**, signer gọi socket127.0.0.1 bị `operation not permitted`, không bypass ký/trust/quyền. Không phải finding của diff. `kiem()` thật errors=[],25/25; gỡ riêng mục khỏi registry trong bộ nhớ ⇒25/24, báo đúng `test sống chưa đăng ký: ops/ci_provenance_test.py`. Regex MOI thật nhận stdout suite; không thay full --chay bằng probe này. |
| A10 | **frozen/readback phù hợp authority; LIVE độc lập KHÔNG ĐO ĐƯỢC** | `readback.py` rc0:14/14jobs, mọi labels `[ubuntu-latest]`; checkout13passed+chuan-bi118368688427 not_measured. SHA **b27fe85c9e9593ddbb059808fe4347fe1bd267be**, parents **5618020a67709ca6f2c93138905df0aa8d9c2df6** + **400589368e09ab2ee0e734b7af08b93478035503**, tree **857bc47e6bc5f0024e442b400819ac51286dfc55**, replay excerpt + Git cục bộ khớp. Băm frozen provenance **ec8f5608d37934abdc3fe505e1f13b949ea78c51a7d19f3dc56127de02b06060** khớp stdout; NOT_MEASURED16 khớp:WD1+checkout1+Gate14. Không có full logs/HTTP receipt độc lập để kiểm hash log hoặc chứng minh LIVE trên candidate. |
| A11 | **passed** theo trần900 được giao | doctrine-scan rc0:10tệp/0chép doctrine; adr-song rc0:53/53 khớp1–1 (tha0016); bare Ruff trên2tệp mới rc0/All checks passed; diff3tệp/877dòng thêm, diff-check rc0. Ruff pin/probe contract đo riêng `loi_ruff_ci()=([],3)`, không dùng thay bare lint. |
| A12/V1–V4 | **KHÔNG ĐO ĐƯỢC remote/future; V2 chưa đạt** | Không ls-remote, push hoặc connector receipt trong assignment. Còn P0/P1 và đã chạm điều kiện dừng; không có quyền đẩy hay tự gọi connector từ verdict này. |
| A13 | **KHÔNG ĐO ĐƯỢC hoàn chỉnh** | Đã có metadata CLI của đúng thread trong preflight.json; không có đủ stdout thread.started, launcher run.json và bản rollout/hash sau khi writer kết thúc. Bên vận chuyển phải thu/readback1–5 sau run; không coi file còn ghi hoặc actor đăng GitHub là evidence hoàn chỉnh. |

**DANH SÁCH MUTANT VÀ HẠNG.** `python -B .review/run.py mutants python -B .review/mutants.py` rc0; code mutant ở `.review/mutants/`, neo/thay nguyên văn, command, source, rc và output từng con trong `mutants/results.json` cùng stdout/stderr riêng. Mọi target đã chạy **baseline rc0** trên bản sao gốc; mỗi mutant chạy `python -B ops/ci_provenance_test.py --mot-ca <tên>` với `CI_PROVENANCE_MA=<bản sao>`, bytecode tắt. Chỉ **rc3 và DO:<đúng-ca>: do handler TinHieuChotCa** được tính GIET. Tổng **51 mutant:48 GIET,2 TIN_DUNG_GIA,1 SONG_SOT**; survivor là đối chứng chỉ thêm chú thích. Không cộng2 tín dụng giả hoặc11 phản chứng trên candidate vào số giết.

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
| `F02_khong_noi_dong` | `c23_chi_loi_goi_that` | 0 → 3 | **GIET** |
| `F02_cho_moi_co` | `c23_chi_loi_goi_that` | 0 → 3 | **GIET** |
| `F02_doi_so_tu_do` | `c23_chi_loi_goi_that` | 0 → 3 | **GIET** |
| `F01_bool_la_int` | `c22_thieu_dinh_danh_khong_passed` | 0 → 3 | **GIET** |
| `F01_chuoi_rong` | `c22_thieu_dinh_danh_khong_passed` | 0 → 3 | **GIET** |
| `F01_conclusion_bat_ky` | `c22_thieu_dinh_danh_khong_passed` | 0 → 3 | **GIET** |
| `F01_labels_rong` | `c22_thieu_dinh_danh_khong_passed` | 0 → 3 | **GIET** |
| `F01_check_run_bat_ky` | `c22_thieu_dinh_danh_khong_passed` | 0 → 3 | **GIET** |
| `F01_head_sha_bat_ky` | `c22_thieu_dinh_danh_khong_passed` | 0 → 3 | **GIET** |
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
| `vo_can_KeyError` | `c03_checkout_linux` | 0 → 4 | **TIN_DUNG_GIA** |
| `chi_them_chu_thich` | `c20_du_trang` | 0 → 0 | **SONG_SOT** |
| `review_F06_chi_boc_luot_dau` | `c24_goi_that_loi_va_chuyen_huong` | 0 → 3 | **GIET** |
| `review_F01_bo_kiem_steps` | `c22_thieu_dinh_danh_khong_passed` | 0 → 3 | **GIET** |

Bộ phân hạng còn được đối chứng bằng tín hiệu rc3 mang tên ca khác và lỗi AssertionError thông thường: cả hai **TIN_DUNG_GIA** (`mutants/results.json:selfcheck`). Hai mutant kiểm toán bổ sung `review_F06_chi_boc_luot_dau` và `review_F01_bo_kiem_steps` đều GIET đúng ca;48 GIET gồm46 mutant ứng viên +2 bổ sung. Các hunk mutant chỉ là dữ liệu kiểm thử trên bản sao; Executor phải tái dẫn xuất nếu dùng sau quyết định checkpoint.

**Snapshot cuối và giới hạn bàn giao.** `snapshot-start.json`, `snapshot-end.json`, `snapshot-comparison.json` băm/kích thước **5.265 tệp ngoài .git/ và .review/**, gồm ignored/untracked và `.review-input/`, `.codex/`: **0 delta**. HEAD/tree không đổi; git diff, cached diff và untracked không ignored đều rỗng, rc0. Ignored vẫn là `.codex/`, `.review-input/`, `.review/`. `.git/` không băm toàn metadata; được đối chiếu qua HEAD/tree/index/diff/status. Hai snapshot chứng minh không có delta quan sát ở hai mốc, không chứng minh lịch sử chưa từng ghi rồi hoàn nguyên. Mọi scratch, log và bản sao mutant thuộc `.review/` được loại khỏi phép so source.

Native Windows, CI candidate/required checks, mạng/redirect thật, full-log authenticity, remote lease/ref freshness, review-call budget, launcher terminal receipt và delivery receipt **KHÔNG ĐO ĐƯỢC**. Full runtime/release gates **not_run**; review này đo targeted acceptance của công cụ dev-side, không chứng nhận worker/land/release gate hoàn chỉnh. Không có `skipped`, `not_run` hoặc dữ liệu không đo được nào được nâng thành passed. A9 cần môi trường có khả năng ký fixture; A10 cần receipt LIVE độc lập thích hợp; A12/A13 cần evidence đúng thời điểm và bên vận chuyển.

Kết luận giữ **changes_requested** trên exact SHA nêu đầu. F03 đóng bằng phép đo và răng; F01/F02/F05 còn mở lần3 nên bước kế tiếp là **checkpoint của chủ kho theo đặc tả**, không tự động vá tiếp hoặc xin review lượt4.
