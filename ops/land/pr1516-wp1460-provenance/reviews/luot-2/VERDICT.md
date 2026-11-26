VERDICT: changes_requested
reviewed_sha: 1c31f5a88ba125af708a9609085c0edd2f8dc3ee
reviewed_tree: d316445a44465cd563ce72b64a65b4893e63ad0c
spec_sha256: 33d433b018d6eb74048fe27f2cc517b01276a28b76edbe50ffea387a0614dd0c

**Còn 1 finding P2, thuộc lớp F02 `v1-not-fully-specified`.** F01, F03, F04 đã sửa đúng lớp trong phạm vi đo. F02 sửa được các biểu hiện đã báo và bốn đường sập executor bổ sung, nhưng bỏ sót parser YAML của kiểm kê workflow: dữ liệu lồng sâu làm lệnh thu thoát do `RecursionError`, không ghi biên nhận. Không xác nhận P0/P1. Không có lớp nguyên nhân mới; đây là một biểu hiện mới của lớp cũ, có ở cả H1 và H2.

## Hai trục và phạm vi

- **Spec: KHÔNG ĐẠT** — F02-R2 vi phạm tính toàn phần của lệnh thu tại §3 và quy tắc X2 “hình khác ⇒ không xanh”. Suite xanh không đóng đường này.
- **Standards/Security: ĐẠT trong phạm vi đã đo** — đường context chứa ref của F03 đã đi qua `env` và giữ nguyên dữ liệu khi chạy Bash; không xác nhận finding an ninh mới. Kết luận này không thay phép đo trên runner thật.

Reviewer độc lập, chỉ đọc `src/`; mọi bản sao và fixture ngoài `src/`. Metadata `runs/6e53f3d5/run.json`: provider `openai_codex`, execution_surface `codex_cli`, transport `machine`, run `6e53f3d5ac854dcab3d5e7e912c320ba`; sandbox thực tế `workspace-write`. Model/effort thực sự phục vụ từng request: **KHÔNG ĐO ĐƯỢC**; không lấy model trong prompt làm chứng cứ. Trích metadata ở [review-runtime.json](review-runtime.json). Agent `tl_auditor` chỉ đối soát output dài theo `src/CLAUDE.md:32`; finding, phép đo và phán phạm vi do reviewer chính thực hiện. Không dùng agent ấy làm lượt cross-review riêng.

HEAD/tree/cha khớp chỉ thị; cha đúng H1 `4cad0e1c140ced47030b5c2834ae000d9670671f`. Băm SPEC đo **trước khi đọc**; lease từ ref đã giao đúng wp1460/r8/g2, base `5259239d763c9ffc1677f033bd9a9cf23ede9299`, trần 6 tệp/1600 dòng thêm. Không gọi GitHub, không commit/push/dispatch. Verdict không cấp quyền land và không thay owner exact-H audit.

## Đối chiếu lượt 1 và danh sách đường vào

Danh sách độc lập được ghi **trước khi đọc HANDOFF.yaml** tại [inventory-before-handoff.md](inventory-before-handoff.md), từ verdict H1 và mã H2. Sau đó mới đối chiếu bảng `findings_closed` của executor. Các nhãn dưới áp dụng cho cả lớp, không chỉ biểu hiện đầu tiên.

| Finding H1 / lớp | Nhãn duy nhất | Đối chiếu đường vào và bằng chứng chạy trên H2 |
|---|---|---|
| F01 / `rest-error-sidecar-ignored` | **ĐÃ SỬA ĐÚNG LỚP** | Cả hai danh sách có run/jobs/artifacts/definition. Bốn trạng thái JSON tốt/chỉ lỗi/cả hai/vắng được đo; thêm `.loi` rỗng, dạng thư mục không đọc thành tệp và mode000. Ba điểm lõi có dấu lỗi ⇒ rc1, receipt hợp lệ; definition ⇒ rc0, `not_measured`. Không bỏ sót caller REST trong collector. Gỡ riêng từng caller: 4/4 đúng `TinHieuChotCa`, đúng ca; thêm 4 mutant reviewer chọn bỏ qua riêng từng điểm cũng chết đúng. |
| F02 / `v1-not-fully-specified` | **VÁ HỜ** | T1–T11 của handoff được đối chiếu với parse mốc, tính khung, định dạng, schema xanh/đỏ, thời điểm tạo, schema vắng, JSON REST/artifact, matrix, attempt và UTF-8 argv. Các chốt được khai đã qua đo răng. **Danh sách executor thiếu đường `yaml.safe_load` trước kiểm độ dài matrix**, vốn đã có trong danh sách độc lập “workflow checkout YAML/matrix → chuyển int”. YAML lồng 512/900 tầng vẫn không có receipt; xem F02-R2. |
| F03 / `workflow-context-interpreted-as-shell` | **ĐÃ SỬA ĐÚNG LỚP** | Đủ 10 context ở bước thu, đúng ánh xạ env và quote; dấu job/REST đã dùng env. 10/10 mutant quay lại nội suy riêng từng context chết đúng ca. Reviewer thêm mutant bỏ so env REF/SHA_SU_KIEN/WORKFLOW_SHA/RUN_ATTEMPT và bỏ phân biệt quote: 5/5 chết đúng. Bash thật giữ cả 10 argv với ref thường, nháy kép, dấu dollar và Unicode; ca committed còn chạy collector thật. Bước đo HEAD PR0 được xét riêng ở câu hỏi 1. |
| F04 / `collector-derived-evidence-unasserted` | **ĐÃ SỬA ĐÚNG LỚP** | Danh sách độc lập gồm blob OID, sha256 definition từ REST khác checkout, sha256 công cụ ở hai hình, thời điểm tạo và băm artifact. Handoff có các đường này; code so nguyên receipt xanh với kỳ vọng từ nguồn độc lập và phần định danh chung của hình đỏ. 6 mutant mới F04 chết đúng ca; ba mutant từng sống ở H1 nay bị test đã commit giết. Nhân chứng hash độc lập vẫn chứng minh từng mutant làm sai đúng trường. |

**Đo răng:** [round2-mutants.json](round2-mutants.json) chứa 28 chốt mới đã commit được gọi lại bằng bộ phân hạng độc lập: kiểm `type(exc) is module.TinHieuChotCa` **và** `exc.args == (case,)`. Kết quả 28/28; không cấp tín dụng cho ngoại lệ khác. T1/T5/T7 đo bổ sung ở [round2-extra-mutants.json](round2-extra-mutants.json): gỡ kiểm lịch thật, gỡ schema xanh, gỡ lý do thiếu schema — 3/3 chết đúng ca. T4 là mutant thời điểm tạo của F04. T2/T2b/T3/T6/T8/T9/T10/T11 có hàng riêng trong nhóm 28. Bảng đầy đủ tên chốt, mỏ neo, thay thế và tên ca lưu trong JSON; không gộp nhiều chốt thành một mutant.

Tỷ lệ đóng lớp H1→H2: **3/4 = 75%**. Không đổi slug F02 để bỏ lịch sử B1-04 của các lượt đặc tả. Phần chẩn đoán/B1b đã chuyển phạm vi vẫn không được tính là sửa.

## Finding còn mở của lượt này

Đường dẫn/dòng trong bảng tính từ gốc `src/` tại H2.

| ID | Mức | Lớp nguyên nhân | Tệp:dòng | Mô tả / bằng chứng chạy được | Gợi ý |
|---|---|---|---|---|---|
| **F02-R2** (nối F02/B1-04) | **P2** | `v1-not-fully-specified` | `.claude/dev/ci_dang_ky_test.py:1594`, `:1696` | `yaml.safe_load` có thể ném `RecursionError`, trong khi biên X2 chỉ bắt `OSError`, `ValueError`, `yaml.YAMLError`. `python3 -B out/yaml_boundary_evidence.py`: giữ workflow H2 và chỉ thay giá trị matrix bằng dữ liệu danh sách lồng nhau trong cây tạm. 64 tầng ⇒ rc1 + receipt hợp lệ; 512 tầng ⇒ H1/H2 đều rc1 do ngoại lệ + **không receipt**. Bản sao chỉ thêm bắt lỗi tại biên X2 ⇒ receipt không xanh hợp lệ; gỡ chốt lại ⇒ đúng `TinHieuChotCa('reviewer-wp1460-workflow-yaml-long-sau-van-co-bien-nhan')`. 8/8 đối chứng đúng kỳ vọng. Phép đo mở rộng riêng còn tái hiện ở 900 tầng. | Xử lý lỗi parser do dữ liệu tại biên lập kiểm kê thành lý do X2 và tiếp tục dựng hình không xanh; thêm ca tiến trình con cùng đột biến riêng gỡ chốt. Không bắt chung mọi `Exception` để che lỗi lập trình. |

Bằng chứng: [yaml-boundary-evidence.log](yaml-boundary-evidence.log), [script tái chạy](yaml_boundary_evidence.py), [additional-inputs.json](additional-inputs.json). Script kiểm cùng lớp/tên tín hiệu ở bên ngoài tiến trình collector; bản thân `RecursionError` **không** được tính làm tín dụng giết. Chỉ bản sao tạm mang chốt đối chứng, không có bản vá sản phẩm trong `src/`.

Đây là lỗi hợp đồng offline khi đọc workflow sai hình, **không phải lời khai workflow H2 hiện hành bị sập trên GitHub**, cũng không chứng minh khả năng thực thi mã hay thoát cây thư mục. Phép thử sử dụng đúng đầu vào workflow mà `job_ky_vong_du` đọc, cùng cơ chế `wf` của ca matrix đã commit. §3 hứa đối số context hợp lệ luôn có receipt; X2 hứa hình workflow khác bị hạ không xanh. `rc1` vì traceback và mất receipt không đáp ứng hai điều đó.

**Phạm vi cùng lớp (§8.3):** JSON REST bốn điểm và JSON dấu/mảnh dùng `_doc_json_du`, nay bắt được recursion; 28 probe cấu trúc sâu bên trong các trường REST cũng không làm vỡ. Parse số ở matrix/tên artifact và các mốc lịch đã được đo. Đường YAML lập kiểm kê là biểu hiện còn mở đã xác nhận. Loader schema/oracle đóng băng thuộc hiện vật mã đã ghim, không được biến phép sửa byte hợp đồng tùy ý thành đầu vào producer hợp lệ; lỗi oracle năm 0001 ghi riêng ở câu hỏi 2. Không coi hết bộ nhớ, mất khả năng ghi đĩa hay mất byte chính chương trình là đã được xử lý hoặc đã được đo.

## Đo lại lời khai

Mọi clone đều `core.abbrev=7`; không chạy test trong checkout `src/`. Python 3.13.18/Linux, jsonschema 4.26.0, PyYAML 6.0.3. Mã thoát được ghi riêng tại [command-results.json](command-results.json); không suy rc giàn đo thành sản phẩm đúng.

| Phép đo / lệnh | Kết quả đo lại |
|---|---|
| `git diff --numstat base H2` | **4 tệp, +1566/−20**: Python +1284/−20; workflow +87; schema +34; fixture +161. Khớp khai báo. |
| Schema/fixture so nguồn đóng băng | SHA-256 `844b5218b6f6844945f5c4c9440f09015d238fe09a60d64b3787c440787e4f46` và `ce8595739a1ab2f4a86c9c196255e5f91fb19a9f6d3865df6caa2d66f9970e6d`; **trùng byte** cả hai. |
| `python .claude/dev/ci_dang_ky_test.py`, trong A/B | Base **rc0, 1226/1226, TỔNG ĐẠT, 7 s**; H2 **rc0, 1619/1619, TỔNG ĐẠT, 237 s**. Khớp count, thời gian khác 221 s khai báo; đây là số đo máy này, có công việc kiểm độc lập chạy cùng thời gian. |
| Bảng mutant wp1460 đã commit | **89/89 giết đúng lý do; 6/6 tự kiểm; nền 83/83**. Chạy riêng wrapper cũng rc0, 95 hàng không lệch hạng mong đợi. |
| Khối lệnh kiểm trích độc lập từ SPEC, `--dot-bien` | **rc0; 480/480; 249/249 = 57 vị từ + 192 nới schema; TONG: DAT**. Khối trích sha256 `d9c78e708e18a211b7d8c7309638ffd1c73200578cf3128f9f0fc4275430f24e`. |
| `bash ab.sh … base H2 …` | rc0, **32/32** trùng stdout/stderr/rc/cây chọn. |
| `luot-1/ab_committed_fixtures.py` | rc0; **75/75 ca gốc**, **68/68** A/B CLI committed trùng byte. |
| actionlint + ShellCheck | Base/H2 đều rc0, 0 finding; actionlint **1.7.7**, ShellCheck **0.9.0** có mặt. |
| Bare Ruff F | `python3 -m ruff check --select F .claude/dev/ci_dang_ky_test.py`: base/H2 đều rc0, `All checks passed!`, delta0; Ruff **0.15.15**. Tách biệt Ruff CI contract 3/3 của suite. |
| `luot-1/reviewer_mutants.py` | rc0; **40 GIẾT + 1 KeyError tự kiểm**, nền 41/41; H1 là 37 GIẾT + 3 SỐNG + 1 tự kiểm. |
| Probe H1 chạy lại | 40 hàng, gồm 37 probe dữ liệu và 3 phép phân tích shell cũ; bốn JSON+`.loi` và hai năm biên đã đổi đúng hướng. Phần shell cũ cần thích nghi, giải thích bên dưới. |
| `hash_evidence_r2.py` | Bản chuẩn đúng 3/3 băm; cả ba mutant sai bị nhân chứng độc lập giết đúng `IdentityMismatch`. Chỉ đổi cách chọn mutant theo tên vì chúng không còn SỐNG. |
| `class_evidence.py` / `structure_checks.py` | rc0; **26** phép đối chiếu lớp; I1 sau bỏ đúng phần thêm bằng base; bốn hàm legacy nguyên nguồn. |
| `ops/ci_provenance_test.py` | rc0; **77/77 ca, 485/485 mutant, 2 tự kiểm, TONG DAT**. |
| `ops/gate_output_doi_chieu_test.py` | rc0; **51/51 ca, 158/158 mutant, 2 tự kiểm, TONG DAT**. |
| `ops/cong_cu.py kiem-tra --json`; doctrine-scan | Base/H2 rc0; JSON công cụ trùng byte; doctrine đều sạch, 12 tệp, 0 chỗ chép doctrine. |

Log chính: [ab.log](ab.log), [nghiem-thu-1.log](nghiem-thu-1.log), [executor-mutants.log](executor-mutants.log). Output suite đầy đủ giữ ở `ab-suite-nen.out`, `ab-suite-sau.out`; không chỉ giữ dòng tổng.

**Giới hạn giàn probe lượt 1:** đã chạy nguyên script `review_probe.py`. Ba hàng shell dùng `shlex` mà không giải biến môi trường nên nay đọc literal `$REF`; `literal_ref_preserved=false` trong ba hàng ấy là giàn cũ không mô phỏng giao diện mới, không phải F03 tái phát. `round2_probes.py` chạy Bash thật với env trích từ YAML, ghi argv: bốn loại ref đều giữ **cả 10/10 đối số**. Test committed `wp1460-buoc-thu-that-ref-can-quote-giu-nguyen-con-dang-noi-suy-cu-lam-mat` còn chạy collector thật và đối chứng hình nội suy cũ.

## Đột biến độc lập của reviewer

Gộp hai tệp `round2-mutants.json` và `round2-extra-mutants.json`: **47 nền đạt; 45 GIẾT đúng = 28 chốt committed kiểm lại + 17 mutant reviewer; 2 GIẾT SAI LÝ DO có chủ đích để tự kiểm; 0 SỐNG ngoài tự kiểm**. Không gọi hai tự kiểm sai lý do là giết thành công. Bộ lượt 1 chạy lại là phép đo riêng, không cộng vào con số này.

| Đột biến reviewer | Số | Ca đích / kết quả |
|---|---:|---|
| Bỏ qua dấu lỗi chỉ tại run/jobs/artifacts/definition | 4 | Ca JSON kèm `.loi` tương ứng; **4 GIẾT đúng**. |
| Tràn lịch nhưng bịa khung hiện đại | 1 | `wp1460-cli-schedule-nam-0001-khung-tran-van-ghi-bien-nhan-hop-le`; **GIẾT đúng**. |
| Tự đệm năm <1000 thành khung hợp lệ hình nhưng trái oracle | 1 | `…thu-am-x8-nam-999-khung-khong-bieu-dien-duoc-ghi-null-giu-moc-rest`; **GIẾT đúng**. |
| Hạ schema đỏ nhưng bịa `run_created_at` | 1 | `wp1460-thu-hinh-khong-xanh-kiem-schema-truoc-khi-ghi`; **GIẾT đúng**. |
| Bỏ so riêng env REF, SHA_SU_KIEN, WORKFLOW_SHA, RUN_ATTEMPT | 4 | Lần lượt ca bỏ env-ref / sha-la-ref-name / workflow-sha-tu-checkout / attempt-ghi-cung; **4 GIẾT đúng**. |
| Comparator coi biến ref có/không quote như nhau | 1 | `wp1460-job-thu-lenh-thu-bien-ref-khong-quote-do`; **GIẾT đúng**. |
| Băm đường dẫn công cụ thay byte công cụ | 1 | `wp1460-thu-duong-luot-dau`; **GIẾT đúng**. |
| Băm SHA sự kiện thay byte workflow REST | 1 | `wp1460-thu-definition-byte-rest-khac-tep-checkout-measured-bam-theo-byte-rest`; **GIẾT đúng**. |
| Gỡ riêng kiểm ngày có thật / schema xanh / lý do schema vắng | 3 | Ca created-at-ngay-khong-ton-tai / started-at-sai-dang / khong-nap-duoc-schema-dong-bang; **3 GIẾT đúng**. |
| Ném `TinHieuChotCa` nhưng tên ca khác | 1 | **GIẾT SAI LÝ DO**, tự kiểm, không cấp tín dụng. |
| Ném `TypeError` vô can | 1 | **GIẾT SAI LÝ DO**, tự kiểm, không cấp tín dụng. |

Riêng đường còn thiếu F02-R2: H2 chưa có chốt để gỡ. Vì vậy dùng đối chứng bản sao thêm đúng một chốt X2 rồi gỡ lại; kết quả 8/8 ở bảng finding, không nhập nhằng nó thành một chốt đã tồn tại trên H2.

## Hồi quy H1..H2

Diff thực chỉ có Python +185/−31 và workflow +2/−1. Không xác nhận hồi quy mới trong các lựa chọn 1–7 hay các lớp đặc tả từng được đóng:

| Phạm vi H1 đã chấp nhận | Kết quả trên H2 |
|---|---|
| 1. `--ref` thiếu/rỗng; 2. `--cron` phải có mặt | Ca committed và probe vẫn rc2/no receipt khi thiếu; dispatch có cron rỗng vẫn xanh. UTF-8 argv sai nay rc2. |
| 3. X5 đối chiếu chỉ số mảnh; 4. measured kiểm path + blob | Ca âm và mutant lượt 1 tiếp tục đạt. REST byte khác checkout vẫn measured, băm theo REST. |
| 5. Xanh sai schema hạ đỏ | Ca started_at sai dạng/sai kiểu và completed_at sai kiểu đều receipt đỏ hợp lệ; mutant gỡ schema xanh bị giết. Phần toàn phần rộng hơn vẫn hở F02-R2. |
| 6. CLI cũ bỏ qua cờ mới | `choices_evidence.py`: không cờ mới base/H2 rc0/0; kèm `--rest`, `--run-attempt`, `--workflow-ref` mới base/H2 rc2/0 như H1. Giữ phán phạm vi hẹp nghiệm thu 5, không tuyên bố tương đương mọi argv. |
| 7. Chạy đầy đủ oracle trong tiến trình con | Suite và phép trích độc lập đều đủ 480/249; không cắt bộ kiểm để giảm thời gian. |
| Producer ↔ consumer, C4/C11/C12 | 26 phép `class_evidence.py` giữ kết quả; nội dung dấu/mảnh sai dù băm ZIP thật khớp vẫn bị đúng luật từ chối. |
| Oracle đóng băng / từ vựng / freshness C9 | Hai tệp và khối kiểm giữ byte; 57 vị từ + 192 ràng buộc bị giết; các ca mốc giả/cron/khung cũ vẫn bị C9. Nợ năm biên tách ở câu hỏi 2. |
| Thứ tự dấu và early failure | Chốt 11 bước, dấu ngay sau đo HEAD, bước 7–11 `always()` vẫn đạt; mutant vị trí/if tiếp tục bị giết. |
| Reader REST chung, env và schema hai hình | `_doc_json_du` không dùng cho bốn hàm legacy; thêm catch đúng `RecursionError`. JSON definition lỗi chỉ hạ not_measured; lỗi lõi hạ đỏ. Env đủ đúng tên; không thấy lỗi đổi kết luận do bản vá trong các đối chứng đã chạy. |

F02-R2 tái hiện trên H1 và H2, nên ghi **lỗ còn sót**, không gọi là “vá sinh lỗi mới”. Các lớp `legacy-selector-equivalence-is-impossible` và `source-review-budget-not-activated` vẫn **KHÔNG ÁP DỤNG** theo phán lượt 1, không được tính vào số lớp đã sửa của lượt này.

## BẢNG SĂN

| Hướng / giả thuyết | Phép đo | Kết quả |
|---|---|---|
| 1. Dấu lỗi bị JSON tốt che | 4 điểm × trạng thái; rỗng/thư mục/mode000; bỏ chốt từng caller | F01 đóng trong miền đo. Mode000 dưới root chưa chứng minh lỗi permission thật. |
| 2. Mốc lịch làm vỡ hoặc sinh hình đỏ sai | 0001/0999/1000/9999, leap day đúng/sai, dispatch/schedule; hai ca cron lượt 1 | Có receipt đúng schema; giữ mốc REST thật, khung không biểu diễn được null. |
| 3. JSON sâu/lớn còn thoát catch | 4 điểm, độ sâu 64–1500; 2 MiB dữ liệu phụ; JSON dấu/mảnh sâu; 28 cấu trúc sâu trong trường REST | Không tìm thêm lỗi ở JSON; sai hình hạ đỏ, definition lỗi vẫn not_measured. Không đo OOM. |
| 4. Parser YAML nằm trước chốt matrix | Matrix lồng sâu; số nguyên YAML 4301/5000 chữ số; đối chứng H1/H2/chốt scratch/gỡ chốt | **Tìm F02-R2** ở YAML 512/900 tầng; số nguyên quá dài đã hạ X2 có receipt. |
| 5. Số attempt/chỉ số lớn vượt chuyển int | Chuỗi dài 19/20/64/65/4301/5000; ca committed + mutant | Các phép đo có receipt đỏ hợp lệ; tên REST X7, workflow X2; không thử đường thoát cây. |
| 6. Ref qua env mất byte hoặc thiếu cờ | Bash thật, 4 tên ref hợp lệ Git; mutant từng context và env | Giữ 10/10 argv; F03 đóng. |
| 7. Băm từ nhầm nguồn vẫn qua test | Ba mutant H1, REST khác checkout, băm đường dẫn thay nội dung | Test committed nay giết; nhân chứng độc lập xác nhận băm sai thật. |
| 8. Hình xanh/đỏ đổi kết luận sau vá | Ca job-time sai, schema chặt hơn, schema vắng, lỗi REST từng điểm | Đúng kết quả kỳ vọng; không thấy hồi quy ở các ca này. |
| 9. Cờ cũ/I1 bị thay theo helper mới | A/B 32 + 68, AST bốn hàm cũ, YAML trừ đúng phần thêm | Đạt; cờ mới bị bỏ qua như H1 được ghi riêng, không che bằng A/B. |
| 10. Định danh REST jobs xuyên run | Probe đổi toàn bộ `jobs[].run_id`, giữ nguồn khác | Vẫn xanh như H1; ngoài ràng buộc X1 hiện hành, phán ở câu hỏi 3. |

## Đầu vào thù địch: mô tả đường xử lý và độ phủ

Không dựng payload thực thi shell, traversal hoặc hiện vật nhằm thoát cây thư mục. Các phép đo chỉ dùng dữ liệu JSON/YAML, tên ref và tệp trong cây tạm.

| Hướng | Đường mã xử lý / ca phủ |
|---|---|
| Context cần quote | Workflow dòng 225–226 → env → biến shell quote → `doi_so_thu`; ca Bash thật và `wp1460-buoc-thu-that-ref-can-quote-giu-nguyen-con-dang-noi-suy-cu-lam-mat`, cùng 10 ca nội suy riêng. |
| `.loi` rỗng/không đọc được cạnh JSON tốt | `doc(ten)` dòng 1674 dùng `lexists`, không cần đọc nội dung dấu. Ca JSON-kem-dau-loi bốn điểm; probe rỗng và dấu dạng thư mục xác nhận sự tồn tại quyết định. Không khẳng định chmod000 dưới root tạo được PermissionError. |
| JSON REST rất lớn/lồng sâu | `_doc_json_du` dòng 1609 bắt recursion rồi X1/not_measured; ca `wp1460-con-khong-vo-thu-am-x1-rest-la-rac`; probe hữu hạn 2 MiB và sâu tới 1500, cả artifact. Không đo mức cạn tài nguyên. YAML inventory là parser khác còn hở, xem finding. |
| Biên lịch | `_doc_moc_du` → `_khung_du` → schema xanh/đỏ; ca 0001, 0999 và các probe lịch. Không bịa mốc hiện tại thay REST. |
| Attempt/chỉ số mảnh rất lớn | `doi_so_thu` giới hạn số context; regex tên artifact dòng 1715 giới hạn attempt 19 chữ số; `job_ky_vong_du` giới hạn giá trị matrix 64 ký tự; ca `…5000-chu-so` và probe các ngưỡng. |
| Byte workflow REST khác checkout | `doc('definition')` → giải mã base64 → blob SHA-1 + SHA-256 từ byte trả về; ca `wp1460-thu-definition-byte-rest-khac-tep-checkout-measured-bam-theo-byte-rest`, mutant băm nhầm checkout và probe độc lập. |

## Phán câu hỏi 1–4

1. **Bước đo HEAD giữ nội suy SHA/run_id/run_attempt: không có P0–P2 được xác nhận.** `choices_evidence.py` đo bước này bằng đúng bước PR0 và chỉ chứa ba context đó. Theo miền định danh đã ghim trong đặc tả, chúng là SHA hex/số của lượt, không có miền ref tự do gây F03. Không yêu cầu thay hình PR0 để đóng F03. Đây là phán theo miền hợp đồng; chưa đo context thực trên GitHub.
2. **Hạ không xanh khi khung năm <1000 không biểu diễn được trên glibc là đúng hướng.** Năm 0999 và đầu năm 1000 có khung năm 0999 đều đỏ hợp lệ, giữ `run_created_at`, khung null. Dispatch không tính cron nên ngày cổ hợp lệ vẫn có thể xanh; không nên viết rộng rằng mọi sự kiện ở năm cổ đều đỏ. `choices_evidence.py` xác nhận oracle đóng băng: receipt xanh hình hợp lệ ở năm 0001 ném `OverflowError`; khung 0999 được đệm đúng bốn số vẫn bị C9 do `strftime`. Đây là **nợ đặc tả/oracle đóng băng**, cần revision riêng nếu muốn mở miền đó; không yêu cầu sửa byte hợp đồng trong PR này. Finding đang chặn là đường producer YAML, không phải đòi sửa oracle.
3. **`jobs[].run_id` chưa đối chiếu: giữ ghi chú, không nâng thành finding PR này.** Probe vẫn rc0/ok=true/schema-valid khi chỉ thay trường đó. X1 đóng băng đối chiếu `run` với context; X4 đối chiếu run_id nhúng trong dấu. Chưa có yêu cầu hiện hành đối chiếu thêm trường REST jobs này. Bổ sung là việc sửa hợp đồng sau, không được nhận là đã kiểm ở H2.
4. **Bốn đường executor tự bổ sung đều sửa đúng biểu hiện và có răng:** JSON recursion, chuỗi matrix >4300 chữ số, attempt quá dài trong tên REST, UTF-8 argv không mã hóa được. Bốn ca con đạt trên nền; gỡ riêng từng chốt tạo đúng tín hiệu/tên ca, lỗi vô can được bộ tự kiểm nhận riêng. **Lớp F02 chưa đóng**, vì YAML inventory còn ném recursion trước khi đến kiểm matrix. Không gộp parser JSON và YAML chỉ vì chúng đều đọc tệp.

## Write set, ngân sách và phần chưa đo

[identity-checks.json](identity-checks.json) xác nhận đúng bốn tệp của lease; +1566 ≤1600, còn **34 dòng**; không tệp thứ năm. Hai commit H1/H2 và toàn bộ bốn tệp có **0** chuỗi đánh dấu bỏ qua CI theo phép quét các dạng chuẩn; `git diff --check` rc0. H1..H2 không đổi hai tệp hợp đồng.

Handoff ghi executor đã dùng **4/4** lượt. Finding P2 không được hạ mức vì hết lượt hay gần trần dòng; verdict này không cấp thêm attempt. Điều phối xử lý tiếp theo authority/budget hiện hành, giữ lịch sử lớp F02.

**KHÔNG ĐO ĐƯỢC / not_run:**

- Workflow/REST GitHub thật, các giá trị context thật, tải artifact/rerun nhiều attempt thật, PR Ubuntu CI, K7, canary A3, nghiệm thu 8/10/11 và schedule sau merge; không tiêu quota M9 và không thực hiện các hành động đó.
- Python 3.12 có executable nhưng `import jsonschema` thất bại `ModuleNotFoundError`, rc1. Không nhận phép chạy Python 3.13 là đã đo 3.12. Không chạy Windows; `LAUNCHER WINDOWS 4/4` là kiểm hợp đồng, không phải chạy nền Windows.
- MemoryError/OOM, hết đĩa, output không ghi được, lỗi đọc byte chính công cụ; không tuyên bố toàn phần trong điều kiện tiến trình/môi trường không còn khả năng ghi. PermissionError thật trên `.loi` dưới UID không có quyền chưa đo; mode000 dưới root không đủ chứng minh.
- Không chạy registry `--chay` toàn bộ hoặc `ops/ci_duong_nhanh_test.py`; không đo hiệu năng runner 2 nhân. Nguồn ref/lease là snapshot đã giao, không xác minh ngân sách remote live.
- Model/effort phục vụ từng request, rc và băm stdout cuối của launcher đang bao phiên: chưa có receipt kết thúc tại thời điểm viết; điều phối phải hoàn tất sau khi phiên dừng. Không dùng cấu hình yêu cầu thay bằng chứng runtime.

Cách tái chạy và toàn bộ hiện vật ở [REPRODUCE.md](REPRODUCE.md). Cổng lân cận cuối đã hoàn tất; kết quả được bổ sung vào bảng đo lại phía trên.

## Kiểm cuối và bàn giao

Đã đối chiếu **17.994/17.994 tệp worktree** trước/sau: **0 thêm, 0 xóa, 0 đổi byte**, gồm hidden/ignored. Git status, working diff và index diff rỗng; HEAD/tree/cha cuối giữ nguyên. Bằng chứng ở [read-only-check.json](read-only-check.json). So hai mốc không chứng minh lịch sử mọi syscall; sandbox workspace-write không được khai thành cơ chế chặn ghi riêng cho src. `/tmp/.git` có sẵn ở cả hai mốc, không xóa.

Giữ `out/` với script, log, JSON, băm và hướng dẫn tái chạy; dọn các clone/tệp tạm do reviewer dựng. Kết luận cuối vẫn **changes_requested: F02-R2 P2 còn mở**, dù mọi cổng đã commit được chạy trong phiên đều đạt.
