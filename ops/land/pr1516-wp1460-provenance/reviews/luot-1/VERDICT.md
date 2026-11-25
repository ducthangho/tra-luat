VERDICT: changes_requested
reviewed_sha: 4cad0e1c140ced47030b5c2834ae000d9670671f
reviewed_tree: 5ecfc5454dc486b2554365d0ed06ccb641168ea6
spec_sha256: 33d433b018d6eb74048fe27f2cc517b01276a28b76edbe50ffea387a0614dd0c

Kết luận cuối: **changes_requested — 4 finding P2 thuộc 4 lớp nguyên nhân; không có P0/P1 đã xác nhận.** Bộ test đã commit xanh không đủ đóng các bằng chứng phản chứng độc lập bên dưới.

## Phạm vi và định danh

Reviewer độc lập. `runs/db869399/run.json` ghi provider **openai_codex**, execution_surface **codex_cli**, transport **machine**, run_id **db8693993581490a8f8133c0cc7a37bc**, executable `/opt/node22/lib/node_modules/@openai/codex/bin/codex.js`; sandbox quan sát trong phiên **workspace-write**. Model/effort thực sự phục vụ: **KHÔNG ĐO ĐƯỢC**; không dùng tên model trong prompt làm chứng cứ. Trích metadata không chứa bí mật lưu ở `review-runtime.json`. Chỉ đọc `src/`, chạy phép thử trên bản sao ngoài `src/`; không commit, push hay ghi GitHub.

Đã đo `git -C src rev-parse HEAD HEAD^{tree}` khớp H/tree được giao; `git status --short` rỗng. Băm đặc tả đo trước khi đọc khớp 33d433b0…dd0c. Tree H khớp `head_tree` trong HANDOFF.yaml, dù handoff còn ghi head trước squash.

Write set đo bằng `git -C src diff --numstat 5259239d763c9ffc1677f033bd9a9cf23ede9299 4cad0e1c140ced47030b5c2834ae000d9670671f`: đúng 4 tệp, +1411/−20 (Python +1130/−20; workflow +86; schema +34; fixture +161), dưới trần 6 tệp/1600 dòng của lease.

## Hai trục

- **Spec: không đạt** — còn F01/F02 về hợp đồng nhận dữ liệu và biên nhận; F04 về độ phủ bằng chứng mới.
- **Standards/Security: không đạt** — F03 trộn context chứa ref với cú pháp shell; F01 bỏ qua dấu lỗi nguồn. Không phát hiện P0/P1 trong phạm vi đã đo.

## Đo lại lời khai — phần đã hoàn tất

Các lệnh dưới chạy offline; bản sao A/B đều `core.abbrev=7`. Log giữ ở `out/`.

| Phép đo | Lệnh / bằng chứng dương | Kết quả |
|---|---|---|
| A/B nghiệm thu 5 | `PYTHONDONTWRITEBYTECODE=1 bash ab.sh "$PWD/src" 5259239d763c9ffc1677f033bd9a9cf23ede9299 4cad0e1c140ced47030b5c2834ae000d9670671f "$PWD/review-scratch/ab"` | `A/B --kiem-bien-nhan-du: 32/32 trung byte` (stdout, stderr, rc, cây chọn); fixture tự dựng của executor, không tuyên bố là toàn bộ fixture nội bộ |
| Registry base | `python .claude/dev/ci_dang_ky_test.py` trong clone `nen` | rc 0; `PHẢN CHỨNG: 1226/1226 đỏ đúng`; `TỔNG: ĐẠT`; 8 s |
| Registry H | cùng lệnh trong clone `sau` | rc 0; `PHẢN CHỨNG: 1556/1556 đỏ đúng`; `TỔNG: ĐẠT`; 220 s; delta +212 s trên máy này |
| Đột biến wp1460 chạy riêng | `python3 -B out/executor_mutants.py` (wrapper gọi `dot_bien_wp1460()`); từng hàng ở `dot-bien-executor.log` và `executor-mutants-repro.log` | rc 0; `ĐỘT BIẾN wp1460: giết đúng lý do 61/61 · tự kiểm phân hạng 5/5`; 9,01 s |
| Nghiệm thu 1 độc lập | `python3 -B out/lenh_kiem_spec.py src/ops/specs/wp1460-r1/hop_dong --dot-bien` | rc 0; đúng ba dòng: `FIXTURE: 480/480 phep kiem dung ky vong · hinh 120 · ngu nghia 118 · tu vung 79 · doi tuong 163 · luat duoc phu 12/12`; `DOT BIEN: giet 249/249 · vi tu 57 · noi long schema 192`; `TONG: DAT` |
| Ruff F | `python3 -m ruff check --select F .claude/dev/ci_dang_ky_test.py` trên cả base và H | rc 0/0; `All checks passed!`; delta 0; ruff 0.15.15 |
| actionlint | `actionlint -no-color .github/workflows/ci-dot-bien-du.yml` trên cả base và H | rc 0/0; 0 finding cả hai; shellcheck có mặt; actionlint 1.7.7, ShellCheck 0.9.0 |

Log: `ab.log`, `nghiem-thu-1.log`, `dot-bien-executor.log`. Khối Python trích từ SPEC có sha256 `d9c78e708e18a211b7d8c7309638ffd1c73200578cf3128f9f0fc4275430f24e`; jsonschema 4.26.0.

## Đột biến độc lập — kết quả ban đầu

`python3 -B out/reviewer_mutants.py`: 41 biến thể, nền từng ca đích đều đạt; 37 GIẾT bằng đúng lớp `TinHieuChotCa` và đúng tên ca; 3 SỐNG; 1 `TIN_DUNG_GIA (KeyError)` cố ý tự kiểm, không tính là giết. Ba biến thể sống thay lần lượt `dinh_danh_definition.blob_oid`, `dinh_danh_definition.sha256`, `cong_cu.sha256` bằng chuỗi 0 đúng độ dài. Đã đo rộng hơn: mutant ghép cả ba vẫn vượt qua toàn suite 1556/1556; nhân chứng riêng xác nhận cả ba là thay đổi không tương đương. Chi tiết mỏ neo/thay thế/tên ca ở `reviewer-mutants.json`.

## Dò độc lập — bằng chứng cần xử lý

`python3 -B out/review_probe.py` (script rc 0; rc lệnh thu được ghi riêng từng ca):

- REST `.loi` cùng tồn tại với JSON hợp lệ: cả run/jobs/artifacts vẫn rc 0, `ok=true`; definition vẫn `measured`.
- `schedule`, `run.created_at=0001-01-01T00:00:00Z`: CLI rc 1 do `OverflowError`, không có biên nhận.
- `schedule`, `run.created_at=0999-11-21T19:31:12Z`: CLI rc 1, đã ghi biên nhận nhưng `schema_valid=false` vì khung năm được định dạng thiếu chữ số.
- Ref chứa dấu nháy kép vẫn được `git check-ref-format` chấp nhận; nội suy vào thân bước thu làm `shlex` không còn thấy đối số `--ref` riêng. Chỉ dùng tên nhánh làm dữ liệu và phân tích đối số, không dựng payload thực thi.

Các đối chứng: lượt khỏe xanh đúng schema; attempt 1→3 giữ job cũ hợp lệ; ba lỗi REST đơn lẻ cho biên nhận đỏ đúng schema; trang lặp/thiếu/sai kiểu bị từ chối; dấu job cũ sai run_id bị X4; ngày không tồn tại cho mốc null; đúng mốc cron và trước mốc một giây cho khung đúng. Dữ liệu từng ca: `reviewer-probes.json`.

## Findings

Các finding dưới áp lên đúng H ở đầu tệp; không có bản vá sản phẩm nào được ghi vào `src/`. Đường dẫn trong bảng tương đối với gốc kho `src/`. Những hướng vá chỉ là gợi ý cho executor tự hiện thực và tự đo.

| ID | Severity | Lớp nguyên nhân | Tệp:dòng | Mô tả và bằng chứng tái chạy | Gợi ý vá |
|---|---|---|---|---|---|
| F01 | P2 | `rest-error-sidecar-ignored` | `.claude/dev/ci_dang_ky_test.py:1663`, `:1751` | Bộ đọc chỉ nhìn `.json`, không đọc `.loi`. `python3 -B out/review_probe.py`: `run-json-and-loi`, `jobs-json-and-loi`, `artifacts-json-and-loi` đều **rc=0, ok=true, schema_valid=true**; `definition-json-and-loi` vẫn **measured**. Các đối chứng chỉ có `.loi` cho ba điểm lõi đều rc=1, biên nhận hợp lệ; definition chỉ có `.loi` là not_measured. Trái §4: không quan sát được do tệp `.loi` phải không xanh; đối với definition không được nhận đã đo từ dữ liệu có dấu lỗi. | Một bộ đọc trạng thái REST thống nhất phải coi dấu lỗi là kết quả không đo được, kể cả còn JSON. Ba điểm lõi hạ đỏ; definition hạ not_measured. |
| F02 | P2 | `v1-not-fully-specified` | `.claude/dev/ci_dang_ky_test.py:1636`, `:1676`, `:1769` | Hợp đồng “đối số hợp lệ ⇒ luôn có biên nhận hợp lệ” chưa toàn phần. Cùng lệnh probe: `schedule-0001-01-01T00:00:00Z` **CLI rc=1, OverflowError, receipt=false**; `schedule-0999-11-21T19:31:12Z` **CLI rc=1, receipt=true, schema_valid=false**. Phép trừ ngày có thể tràn; `%Y` trên nền đo không đệm năm dưới 1000; hình đỏ giữ khung sai mà không kiểm lại schema. Đây là dữ liệu ngày biên, không payload thực thi. | Tính/định dạng thời gian trong miền xử lý lỗi có kiểm chứng; khung không tính/biểu diễn được phải trở thành chưa biết trong hình đỏ, kèm lý do. Kiểm hình cuối cho cả hai nhánh trước khi ghi. Không tự sửa byte schema/oracle đóng băng. |
| F03 | P2 | `workflow-context-interpreted-as-shell` | `.github/workflows/ci-dot-bien-du.yml:225`; `.claude/dev/ci_dang_ky_test.py:1005` | `github.workflow_ref` và `github.ref` được nội suy thẳng vào thân shell trong dấu nháy kép. Tên nhánh dữ liệu chứa dấu nháy kép được `git check-ref-format` chấp nhận nhưng sau nội suy, `shlex` không còn nhận được cờ `--ref` riêng (`literal_ref_preserved=false`). Ca đối chứng tên nhánh thường giữ nguyên. Đây là lỗi ở tầng vận chuyển trước `doi_so_thu`; nháy kép không giữ một giá trị nội suy thành dữ liệu shell. Chỉ phân tích tên nhánh/đối số; **không** soạn hoặc chạy payload tấn công. | Truyền context qua `env`, lấy bằng biến shell được quote hoặc lập argv trong Python; cập nhật hình ghim tương ứng. Giữ nguyên giá trị ref/workflow_ref khi đi tới CLI. |
| F04 | P2 | `collector-derived-evidence-unasserted` | `.claude/dev/ci_dang_ky_test.py:2040`, `:2054`, `:2287` | Ba đột biến riêng thay `dinh_danh_definition.blob_oid`, `.sha256`, `cong_cu.sha256` bằng số 0 đúng độ dài đều **SỐNG** ở ca dương đã commit. `python3 -B out/hash_evidence.py` chứng minh mỗi bản vẫn **rc=0, ok=true, schema_valid=true** nhưng băm tương ứng sai; bản H không đổi khớp cả ba. Test chỉ so trạng thái definition/workflow_sha, không so ba giá trị đã đo với byte nguồn độc lập. Bộ 61/61 vì vậy chưa khóa toàn bộ bằng chứng định danh mới. | Thêm so băm độc lập từ byte workflow REST đã giải mã và byte công cụ đang chạy; thêm từng mutant thay một băm bằng giá trị sai nhưng đúng hình. Không đổi oracle đóng băng chỉ để che thiếu assertion phía producer. |

### Phạm vi lớp và phép kiểm đóng lớp (§8.3)

| Lớp | Biểu hiện / số lượng | Còn ở đâu trong bản vá? | Phép kiểm đóng lớp và rủi ro của hướng vá |
|---|---|---|---|
| `rest-error-sidecar-ignored` | F01: 4 điểm REST | Cùng cơ chế ở run, jobs, artifacts và definition; không chỉ jobs. Các bước REST thật có dọn tệp ở nhánh thông thường, nên phép đo này nhắm vào hợp đồng hàm thu offline khi hai hiện vật cùng tồn tại, không tuyên bố đã gặp lỗi runner thật. | Với từng điểm: JSON tốt, lỗi đơn lẻ, cả hai, cả hai vắng. Ba điểm lõi không được xanh nếu có lỗi; definition vẫn cho audit xanh nhưng phải not_measured. Mutant bỏ kiểm `.loi` phải chết bằng ca tương ứng. Tránh vô tình biến lỗi definition thành lỗi lõi. |
| `v1-not-fully-specified` | F02: 2 biểu hiện thời gian | Quét từ `_doc_moc_du` → `khung_cron_du` → hình xanh/đỏ: chỉ hình xanh được validate, hình đỏ giữ khung tính lỗi. Helper cron trong khối oracle đóng băng cũng dùng phép trừ/`strftime` tương tự; không tuyên bố đã sửa lớp bằng việc sửa riêng một năm. Các biểu hiện chẩn đoán/A+3 của r4 vẫn thuộc B1b. | Các năm biên, ngày không tồn tại, đúng mốc, trước mốc 1 giây, dispatch, schedule và REST lỗi: luôn có rc 0/1 với schema hợp lệ, không bịa thời gian. Giữ mốc REST có thật; chỉ khung chưa biết mới null. Rủi ro: đổi oracle cần revision đặc tả; nới schema xanh để cho lọt dữ liệu thiếu là sai hướng. |
| `workflow-context-interpreted-as-shell` | F03: 2 context chứa ref trong cùng lệnh | `BUOC_THU_DU` tái tạo đúng cách nội suy nguy hiểm; shape test đang ghim nó. Đã quét các bước thêm: dấu job và REST dùng env, không có cùng lỗi ở đó. Các context SHA/ID có miền ký tự khác; không gộp chúng thành ref tùy ý. | Ca giữ nguyên argv với tên nhánh hợp lệ có ký tự cần quote; đối chứng thường. Mutant quay lại nội suy thân shell phải bị bắt trước khi gọi collector. Rủi ro vá: thiếu env, đổi tên cờ, bỏ `always()` hoặc nuốt rc; giữ test 11 bước và ca thực thi CLI. |
| `collector-derived-evidence-unasserted` | F04: 3 trường băm | Không chỉ checksum definition: cả blob OID và checksum công cụ đều không có oracle dương độc lập. Đột biến băm nội dung artifact của reviewer **bị giết**, vì C8 đối chiếu byte; không báo chung rằng mọi băm đều thiếu test. | Bản chuẩn khớp 3/3; thay riêng từng trường phải chết đúng lớp/tên ca; giữ mẫu definition not_measured hợp lệ. `hash-evidence.log` đã chứng minh 3 đột biến không tương đương và đều chết bởi `IdentityMismatch` của phép kiểm độc lập. Tránh tính kỳ vọng từ chính giá trị trong biên nhận hoặc khóa nhầm hash của H thay vì công cụ thực chạy trong bản sao. |

Nguồn F01/F03/F04: review mã lượt này trên H. F02 nối stable slug B1-04 từ review đặc tả 4–5; không đổi slug để che tái diễn. Tổng hiện ghi: **4 lớp, 11 biểu hiện**, mức cao nhất mỗi lớp P2. Hướng vá chỉ là mô tả; không có patch của reviewer vào workflow/gate.

## Đối chiếu lượt trước — áp các lớp đặc tả 4–6 vào mã

Đây là lượt review **mã nguồn đầu tiên**. Nguồn lịch sử đọc trực tiếp bằng `git -C src show origin/ops/wp1460-r1:ops/specs/wp1460-r1/reviews/wp1460-spec-review-{4,5,6}.json`; bản đọc giữ trong `out/`. SHA lượt 4 = `9f09a12a53fb0fc032c4496728b49feef09d5c5e`; lượt 5 = `f18abde3c05e15659a9c8ccfe8aa28e67e36d789`; lượt 6 = `2e93730ff2451353086964e78d0bcff7e9bb5ac5`. Mỗi lớp nhận đúng một nhãn; chuyển phạm vi không được tính là sửa.

| Lớp / nguồn | Nhãn áp vào mã | Bằng chứng đo và giới hạn |
|---|---|---|
| `v1-not-fully-specified` — B1-04, r4/r5 | **VÁ HỜ** | Các ca r5 đã sửa: `class_evidence.py` xác nhận hình đỏ run lỗi/schedule thiếu khung/push hợp lệ; hình xanh dùng mốc null bị C1. `review_probe.py` cũng chạy collector thật cho các trạng thái ấy. Nhưng bảo đảm toàn phần vẫn hở ở hai ngày biên F02. Phần chẩn đoán/hash/A+3 của r4 chuyển B1b, không được tính là sửa. |
| `legacy-selector-equivalence-is-impossible` — B1-14, r4 | **KHÔNG ÁP DỤNG** | Đặc tả hiện hành bỏ lời khai hai bộ chọn tương đương; yêu cầu thay bằng hồi quy CLI cũ. Đã đo A/B 32/32 và **68/68** trên nguyên khối fixture đã commit, 75/75 ca gốc đạt. Không dùng những số này để khôi phục lời khai tương đương mọi đầu vào, đặc biệt không bao gồm tổ hợp cờ mới. |
| `consumer-records-not-bound-to-producers` — B1-15, r5/r6 | **ĐÃ SỬA ĐÚNG LỚP** | `python3 -B out/class_evidence.py`: 7 biến thể nội dung dấu có **ZIP và băm thật khớp** đều chỉ vi phạm C11; 2 biến thể nội dung mảnh chỉ vi phạm C12; đồng thời bỏ producer khỏi REST và biên nhận bị C4 vì kiểm kê ngoài độc lập. Đối chứng ZIP thật khỏe không vi phạm; hai ca rerun hợp lệ vẫn không vi phạm. Đây là kiểm hợp đồng C, chưa phải B2/B3 đã triển khai hay tải ZIP Actions thật. |
| `frozen-fixture-semantic-oracle-missing` — B1-16, r5/r6 | **ĐÃ SỬA ĐÚNG LỚP** | Lệnh đặc tả độc lập chạy đúng 480/480, **57/57 vị từ và 192/192 nới schema bị giết** bằng `LechDauTien`, tự kiểm lỗi vô can giữ nguyên. Đã kiểm cụ thể tên artifact/attempt của hai ca rerun và C11/C12/C4 ở trên. Phạm vi đóng là **oracle/fixture đóng băng** của lớp cũ; F04 là lỗ assertion của biên nhận producer mới, ba trường ngoài phạm vi xác minh C hiện hành, không được lấy 249/249 che nó. |
| `collector-stamp-order-conflict` — B1-17, r5 | **ĐÃ SỬA ĐÚNG LỚP** | YAML thật có 11 bước, cặp dấu ngay sau đo HEAD ở cả 4 job. Các ca `wp1460-doi-cap-dau-qua-setup-python-…-do` đạt; đột biến executor ở job cũ/job thu bị GIẾT; reviewer gỡ chốt vị trí ở job cũ cũng GIẾT đúng tên ca. Không còn hai thứ tự trái nhau. |
| `consumer-freshness-anchor-unverified` — B1-19, r6 | **ĐÃ SỬA ĐÚNG LỚP** | `class-evidence.log`: mốc khai 2099 trái REST, ngày không tồn tại, cron lệch, khung tương lai, khung tuần trước đều C9; rerun giữ mốc gốc. Reviewer đổi công thức khung → ca schedule đỏ đúng tín hiệu. F02 ghi riêng tính toàn phần khi ngày ngoài miền tính/định dạng được, không phải sự chấp nhận mốc giả của lớp r6. |
| `source-review-budget-not-activated` — B1-21, r6 | **KHÔNG ÁP DỤNG** | Lỗi metadata của spec cũ, không phải đường mã producer. Đặc tả r8 có dòng kích hoạt ADR-0055, lease cho 3 source review + 2 connector trong trần packet 10. `identity-checks.log` đo tệp ADR có ở OID, vắng ở cha (rc128), OID trên first-parent `origin/master`, kho không shallow. Không coi allocation Mission là quyền tăng trần; không xác minh ngân sách remote live. |
| `schema-patterns-accept-trailing-newline` — B1-18 P3, r5 (bổ sung) | **ĐÃ SỬA ĐÚNG LỚP** | Hiện vật ghim dùng kết thúc tuyệt đối; phần từ vựng đo 79 phép kiểm, bao gồm LF/CRLF/sai ký tự cùng độ dài/sai kiểu. Bộ nới schema bị giết. |
| `collector-early-failure-contract-contradiction` — B1-20 P3, r6 (bổ sung) | **ĐÃ SỬA ĐÚNG LỚP** | Câu đặc tả hiện hành chỉ nói không bảo đảm có biên nhận; YAML và `wp1460-buoc-truoc-hong-thi-buoc-7-11-van-chay` thống nhất. Ca REST thật dùng gh giả xác nhận một điểm lỗi không dừng điểm sau; mutate bỏ `if` bị giết. Không suy một receipt xanh thành job/run cuối cùng success. |

## BẢNG SĂN

| Hướng | Giả thuyết chủ động | Phép đo đã chạy | Kết quả |
|---|---|---|---|
| 1. REST lỗi lẫn dữ liệu | JSON còn lại có thể che dấu lỗi | `review_probe.py`: riêng từng `.loi`, rồi JSON + `.loi` trên 4 điểm | Tìm F01; 3 điểm lõi xanh sai, definition vẫn measured. |
| 2. Ngày và hình đỏ | Lỗi tính cron có thể thoát ngoài hợp đồng hoặc giữ trường sai schema | Cùng script, năm 0001/0999, ngày 30-02, mốc cron và trước mốc một giây | Tìm F02; hai đối chứng biên cron thông thường xanh đúng; ngày không tồn tại đỏ đúng. |
| 3. Tầng shell | Giá trị ref hợp lệ theo Git có thể bị diễn giải thành cú pháp | Trích bước 10 từ YAML, `git check-ref-format`, `shlex.split` sau nội suy dữ liệu tên nhánh | Tìm F03; mất cờ/ref ở tên chứa dấu nháy; không chạy payload. |
| 4. Băm definition/công cụ | Dòng dương và schema có thể không chứng minh băm đúng | `reviewer_mutants.py`, `hash_evidence.py` | Tìm F04: ba mutant SỐNG ở test commit; nhân chứng độc lập giết 3/3 đúng lớp riêng. |
| 5. Phân trang/kiểu dữ liệu | `total_count`, trang lặp hoặc bản ghi sai kiểu có thể lọt | `review_probe.py`: jobs/artifacts thiếu trang, trang lặp, total_count chuỗi; run.id null/list/dict/bool/số 10^40 | Các ca này đều đỏ và có receipt hợp lệ; trang lặp bị X2/X7 hoặc thiếu trang bị X1. Không phát hiện thêm ở miền đã đo. |
| 6. Producer theo attempt | Nhảy attempt hoặc dấu job cũ có thể bị kiểm sai | Lượt 1→3 chỉ chạy lại thu; dấu retained attempt1 sai run_id; mutant chọn mảnh attempt1 thay bản mới | Rerun nhảy cóc hợp lệ vẫn xanh; dấu sai bị X4; mutant chọn cũ bị GIẾT. |
| 7. Kiểm kê độc lập | Đồng thiếu producer trong REST và receipt có thể tự chứng minh đủ | `class_evidence.py` tạo ZIP thật, bỏ cùng job cả hai nguồn, giữ kiểm kê ngoài | C4 từ chối; đối chứng khỏe đạt. |
| 8. Nội dung artifact | Băm gói đúng có thể che nội dung dấu/mảnh khai khác | 7 biến thể dấu + 2 mảnh, tính lại băm ZIP/tệp từ byte thật | 9/9 bị C11/C12 đúng luật, không chỉ schema hoặc hash. |
| 9. Definition khác checkout | Code có thể lén thay workflow_sha bằng SHA sự kiện hoặc buộc hai SHA bằng nhau | Ca positive có workflow_sha d… khác event SHA a…; đổi byte definition và cập nhật blob thật; các ca not_measured và mutant definition | Giữ định danh riêng, measured với byte riêng; thiếu/sai definition hạ not_measured, audit còn xanh theo spec. Giới hạn băm assertion là F04. |
| 10. Hồi quy CLI cũ | Thêm collector có thể đổi cách chọn/mã thoát/cây output cũ | A/B một lệnh dựng hai clone; `ab_committed_fixtures.py` chạy nguyên fixture committed; thêm 3 tổ hợp cờ mới riêng | 32/32 + 68/68 trùng byte; các cờ mới đi kèm lệnh cũ bị bỏ qua trên H (phán ở lựa chọn 6). |
| 11. Hình workflow | Chốt có thể chấp nhận thiếu needs/quyền/always hoặc bước dấu sai vị trí | Ca committed + đột biến reviewer bỏ so if/permissions/needs/timeout/thứ tự/nuốt rc | Các mutant đích đỏ bằng đúng `TinHieuChotCa`; không cấp điểm cho KeyError tự kiểm. |
| 12. Write set và lịch sử CI | Có tệp thứ năm hoặc dấu tắt CI nằm ngoài hunk dễ nhìn | `git diff --name-only/--numstat/--check`; quét toàn byte 4 tệp và toàn commit message base..H | Đúng 4 tệp, trong trần; 0 dấu tắt CI; diff check rc0; hai hiện vật hợp đồng trùng byte spec. |

## Đầu vào thù địch — đường xử lý và độ phủ

Không dựng đường dẫn thoát cây, symlink thoát cây hay payload thực thi. Các nhận xét dưới phân biệt rõ phép đo bằng dữ liệu thường với hướng chỉ đọc mã.

| Hướng | Đường mã xử lý | Ca đã commit đã chạy / phép đo bổ sung và phần hở |
|---|---|---|
| Tên artifact/tệp có cấu phần đường dẫn lạ, ký tự điều khiển, Unicode tương đương | X7 tại khoảng 1699–1702 dùng fullmatch và đối chiếu khóa/chỉ số kỳ vọng; `lay` 1704–1722 dựng tên artifact từ run/attempt/key kỳ vọng và đòi danh sách tệp bằng đúng một tên cố định. Không lấy tên tệp từ JSON để ghép đường dẫn. | `wp1460-thu-am-x7-artifact-ten-la`, `…x7-ten-trung`, `…x4-dau-thu-muc-thua-tep-*`, `…x5-manh-thua-tep` và các ca wp1166 tên/mục lạ đã chạy. **Không có ca riêng** cho chuẩn hóa Unicode, ký tự điều khiển hay symlink/extractor; không tuyên bố đã chứng minh chống thoát cây của action giải nén. Tên kỳ vọng ASCII và so chính xác không tự chuẩn hóa Unicode. |
| JSON khóa trùng/kiểu sai/số rất lớn/trang lặp hoặc thiếu | `_doc_json_du` 1608 dùng `json.loads` mặc định (khóa trùng lấy giá trị cuối; chưa có kiểm trùng). `_gop_trang_du` 1616 kiểm trang và số lượng; record lọc type int chính xác; X2/X7 chặn bản ghi trùng. | Ca committed `…x1-rest-la-rac`, `…x1-jobs-thieu-trang`, `…x1-artifacts-thieu-trang` đạt. Dữ liệu thường của reviewer đã đo null/list/dict/bool, số 10^40, trang thiếu/lặp/sai type: đỏ đúng schema. Khóa trùng, độ sâu JSON và số vượt giới hạn parser chỉ mô tả/đọc mã, **không soạn payload** và không ghi là đã phủ. |
| Attempt nhảy cóc/giảm, run_id khác giữa nguồn, dấu lượt khác | X1 khớp run context; X2 chọn max attempt riêng từng tên, không yêu cầu liên tục; X4 ràng dấu vào run/attempt/key/SHA/tree; X6 quan hệ mảnh≤gom≤run. | Các ca committed `…run-id-lech`, `…run-attempt-lech`, `…x4-dau-sai-run-id-*`, `…x4-dau-sai-attempt-*`, `…x6-*` đạt; reviewer 1→3 xanh hợp lệ, dấu attempt1 sai run đỏ. **Trường `jobs[].run_id` riêng không được đối chiếu**: dữ liệu thường đổi trường ấy vẫn xanh. X1 của spec chỉ ràng định danh ở `run`, còn bước REST chọn endpoint theo run; không tuyên bố đã xác thực mọi khóa phụ của REST job. |
| Definition đổi giữa lúc chạy và đọc, workflow_sha khác SHA sự kiện | Bước REST 215–221 đọc contents tại WF_SHA từ context; collector 1750–1759 giữ workflow_sha độc lập, kiểm đúng path và blob của bytes, không so với checkout SHA/A4. | Ca definition missing/wrong-blob/wrong-path và context SHA vắng/sai đều đạt; `definition-change.log` có byte definition khác checkout, d… khác a…, **rc0, measured**, đúng chủ đích B1a. Chưa đo REST/GitHub thật; không chứng minh bytes REST giả thực sự thuộc OID ngoài đời. F01/F04 nêu giới hạn lỗi và assertion của đường này. |
| Cron sai khung hoặc sự kiện ngoài hai loại | X8 tại 1674–1676 và `khung_cron_du`; hình đỏ giữ tên sự kiện đã nhận; C9 consumer tính lại khung/mốc REST. | Ca `…x8-cron-lech`, `…x8-schedule-cron-rong`, `…x8-su-kien-push`, hai ca schedule dương và ca vòng kín đã chạy; reviewer kiểm đúng mốc/trước mốc, consumer future/cron/window bị C9. Ngày biên còn F02. |
| REST hỏng một phần, `.loi` xen với tệp hợp lệ | `lay()` trong bước shell xóa tệp đối ngẫu theo rc gh, tiếp tục các endpoint rồi exit0; collector đọc độc lập 3 lõi và definition. | `wp1460-buoc-rest-that-mot-diem-loi-khong-dung-giua-chung` chạy thân YAML bằng bash/gh giả, jobs lỗi nhưng artifacts/definition tiếp tục. Ca core `.loi` và definition `.loi` đều đạt. **Chưa có ca committed cho `.loi` cạnh JSON cùng endpoint**; reviewer đo lỗ đó ở F01. |

## Bảng đột biến độc lập đầy đủ

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 -B out/reviewer_mutants.py`, rc **0** của giàn đo. **40 đột biến chức năng: 37 GIẾT đúng lý do, 3 SỐNG**; thêm 1 đột biến tự kiểm lỗi vô can bị phân loại TÍN DỤNG GIẢ. 41/41 ca đích đạt trên bản không đổi. Mỏ neo/thay thế nguyên văn: [reviewer-mutants.json](reviewer-mutants.json); không sửa test trong mutant. Tệp Python đột biến có tên riêng, tắt bytecode, nằm ngoài `src/`.

| Mã | Đột biến | Ca đích đã commit | Kết quả đo |
|---|---|---|---|
| M01 | `X1-context-identity-only-id` | `wp1460-thu-am-x1-run-id-lech` | GIẾT đúng lớp/tên ca |
| M02 | `X1-missing-artifact-page` | `wp1460-thu-am-x1-artifacts-thieu-trang` | GIẾT đúng lớp/tên ca |
| M03 | `X2-inventory-missing-job` | `wp1460-thu-am-x2-thieu-job` | GIẾT đúng lớp/tên ca |
| M04 | `X2-duplicate-producer` | `wp1460-thu-am-x2-trung-job` | GIẾT đúng lớp/tên ca |
| M05 | `X3-allow-skipped` | `wp1460-thu-am-x3-job-truoc-skipped` | GIẾT đúng lớp/tên ca |
| M06 | `X4-exact-one-file` | `wp1460-thu-am-x4-dau-thu-muc-thua-tep-hien-tai` | GIẾT đúng lớp/tên ca |
| M07 | `X4-old-stamp-run-id` | `wp1460-thu-am-x4-dau-sai-run-id-attempt-1-cua-job-khong-chay-lai` | GIẾT đúng lớp/tên ca |
| M08 | `X4-old-stamp-attempt` | `wp1460-thu-am-x4-dau-sai-attempt-attempt-1-cua-job-khong-chay-lai` | GIẾT đúng lớp/tên ca |
| M09 | `X4-old-stamp-key` | `wp1460-thu-am-x4-dau-sai-khoa-job-attempt-1-cua-job-khong-chay-lai` | GIẾT đúng lớp/tên ca |
| M10 | `X4-old-stamp-event-sha` | `wp1460-thu-am-x4-dau-sai-su-kien-sha-attempt-1-cua-job-khong-chay-lai` | GIẾT đúng lớp/tên ca |
| M11 | `X4-old-stamp-checkout-sha` | `wp1460-thu-am-x4-dau-sai-checkout-sha-attempt-1-cua-job-khong-chay-lai` | GIẾT đúng lớp/tên ca |
| M12 | `X4-checkout-tree` | `wp1460-thu-am-x4-dau-tree-lech-hien-tai` | GIẾT đúng lớp/tên ca |
| M13 | `X4-bypass-stamp-schema` | `wp1460-thu-am-x4-dau-sai-schema-hien-tai` | GIẾT đúng lớp/tên ca |
| M14 | `X5-select-old-shard` | `wp1460-thu-am-x5-manh-vang-o-attempt-moi-nhat-du-co-ban-attempt-cu` | GIẾT đúng lớp/tên ca |
| M15 | `X5-shard-head` | `wp1460-thu-am-x5-manh-head-sai` | GIẾT đúng lớp/tên ca |
| M16 | `X5-shard-index` | `wp1460-thu-am-x5-manh-khai-chi-so-khac` | GIẾT đúng lớp/tên ca |
| M17 | `X6-aggregator-attempt` | `wp1460-thu-am-x6-gom-cu-hon-manh` | GIẾT đúng lớp/tên ca |
| M18 | `X6-run-attempt` | `wp1460-thu-am-x6-job-vuot-attempt-cua-luot` | GIẾT đúng lớp/tên ca |
| M19 | `X7-no-duplicate-names` | `wp1460-thu-am-x7-ten-trung` | GIẾT đúng lớp/tên ca |
| M20 | `X7-allow-current-receipt` | `wp1460-thu-am-x7-bien-nhan-cua-attempt-hien-tai` | GIẾT đúng lớp/tên ca |
| M21 | `X7-content-hash-forged` | `wp1460-thu-duong-luot-dau` | GIẾT đúng lớp/tên ca |
| M22 | `X8-schedule-cron` | `wp1460-thu-am-x8-schedule-cron-rong` | GIẾT đúng lớp/tên ca |
| M23 | `X8-window-offset` | `wp1460-thu-duong-schedule-khung-cung-ngay` | GIẾT đúng lớp/tên ca |
| M24 | `self-completion-fabricated` | `wp1460-thu-duong-luot-dau` | GIẾT đúng lớp/tên ca |
| M25 | `non-green-exit-zero` | `wp1460-thu-am-x3-job-truoc-failure` | GIẾT đúng lớp/tên ca |
| M26 | `non-green-null-time-invented` | `wp1460-thu-vong-kin-run-loi` | GIẾT đúng lớp/tên ca |
| M27 | `non-green-extra-field` | `wp1460-thu-am-x3-job-truoc-failure` | GIẾT đúng lớp/tên ca |
| M28 | `arguments-ignore-wrong-workflow` | `wp1460-thu-doi-so-workflow-ref-tro-tep-khac-thoat-2-khong-ghi` | GIẾT đúng lớp/tên ca |
| M29 | `arguments-write-on-error` | `wp1460-thu-doi-so-ref-vang-thoat-2-khong-ghi` | GIẾT đúng lớp/tên ca |
| M30 | `definition-path-unbound` | `wp1460-thu-definition-tep-khac-not-measured-van-xanh` | GIẾT đúng lớp/tên ca |
| M31 | `definition-replace-workflow-sha` | `wp1460-thu-duong-luot-dau` | GIẾT đúng lớp/tên ca |
| M32 | `definition-blob-record-forged` | `wp1460-thu-duong-luot-dau` | **SỐNG** |
| M33 | `definition-sha256-record-forged` | `wp1460-thu-duong-luot-dau` | **SỐNG** |
| M34 | `tool-sha256-record-forged` | `wp1460-thu-duong-luot-dau` | **SỐNG** |
| M35 | `shape-ignore-if` | `wp1460-job-thu-buoc-8-bo-if-do` | GIẾT đúng lớp/tên ca |
| M36 | `shape-ignore-permissions` | `wp1460-job-thu-quyen-ghi-actions-do` | GIẾT đúng lớp/tên ca |
| M37 | `shape-ignore-needs` | `wp1460-job-thu-bo-needs-dot-bien-gop-do` | GIẾT đúng lớp/tên ca |
| M38 | `shape-ignore-timeout-minutes` | `wp1460-job-thu-timeout-do` | GIẾT đúng lớp/tên ca |
| M39 | `shape-ignore-stamp-order` | `wp1460-doi-cap-dau-qua-setup-python-dot-bien-du-do` | GIẾT đúng lớp/tên ca |
| M40 | `shape-collector-command-swallows-exit` | `wp1460-job-thu-lenh-thu-nuot-ma-do` | GIẾT đúng lớp/tên ca |
| M41 | `classifier-unrelated-keyerror` | `wp1460-thu-duong-luot-dau` | TÍN DỤNG GIẢ — KeyError tự kiểm, không tính giết |

Không có đột biến chức năng nào trong bảng bị nhận nhầm là GIẾT do AttributeError/KeyError/TypeError hoặc tín hiệu ca khác. M41 cố ý chết bằng KeyError và đã bị loại đúng. Ba mutant sống có nhân chứng độc lập trong `hash-evidence.log`: bản gốc PASS, từng bản sai bị `IdentityMismatch` đúng tên.

## Phán từng lựa chọn 1–7

| Lựa chọn | Phán | Căn cứ và phép đo |
|---|---|---|
| 1. Thiếu/rỗng `--ref` → rc2, không receipt | **Chấp nhận cách giải quyết chỗ im lặng** | `su_kien.ref` khác rỗng ở cả hai hình máy đóng băng; không có giá trị này thì không thể dựng receipt hợp lệ mà không tự bịa/đoán. Xem nó là đối số context bắt buộc hợp lý, không phải dữ liệu REST hỏng. Các ca committed và probe `new-ref-absent` đo rc2/no receipt. Nên làm rõ điều kiện này ở mô tả CLI; không coi mệnh đề “đối số hợp lệ” là cho phép thiếu định danh bắt buộc của schema. |
| 2. `--cron` bắt buộc xuất hiện; rỗng cho dispatch | **Chấp nhận trong giao diện workflow này** | Bước YAML luôn truyền cờ, dù dispatch đưa chuỗi rỗng. Dispatch rỗng xanh; vắng cờ rc2; schedule rỗng/lệch đỏ và có receipt hợp lệ. Phân biệt bắt buộc có tham số với bắt buộc có lịch: code không yêu cầu dispatch có cron khác rỗng. Không có yêu cầu nghiệm thu buộc CLI chấp nhận bỏ hẳn cờ ở dispatch. |
| 3. X5 kiểm thêm `manh` bằng chỉ số | **Chấp nhận; đúng hiện vật máy ưu tiên** | C12 đòi `type(manh) is int` và chỉ số khớp. Nếu bỏ, producer có thể xanh nhưng consumer chuẩn từ chối. Ca `…x5-manh-khai-chi-so-khac` và M16 bị GIẾT; probe C12 nội dung có băm thật cũng từ chối. Không tái kiểm kết quả từng mutant/mục của B1b. |
| 4. measured chỉ khi path đúng và git-blob hash đúng byte | **Chấp nhận** | Đây là kiểm “đọc được chính tệp tại OID” trước khi khai measured; thất bại chỉ hạ not_measured và không làm audit đỏ. Ca path/blob sai, SHA vắng đều đạt. Khác SHA sự kiện vẫn được measured, đúng tách biệt definition/checkout. F01/F04 là thiếu sót khác của đường này. |
| 5. Receipt xanh trượt schema bị hạ đỏ | **Chấp nhận nguyên tắc, hiện thực chưa đủ toàn phần** | Probe `job-time-invalid` cho rc1/receipt hợp lệ; đúng tránh “xanh thiếu dữ liệu”. Nhưng nhánh đỏ chưa được validate và giữ khung sai ở F02. Phải bảo đảm cả kết quả hạ cấp cũng hợp lệ. |
| 6. Lệnh cũ bỏ qua các cờ mới truyền kèm | **Chấp nhận theo miền hồi quy hẹp đã đóng băng; không tương đương toàn CLI** | Đã đo: không cờ mới base/H đều rc0; kèm `--rest`, `--run-attempt` sai hoặc `--workflow-ref` sai: base rc2, H rc0 (`legacy-new-flags.log`). Đây là tổ hợp có cờ vừa được giới thiệu, không thuộc miền fixture cũ của nghiệm thu 5; r5 đã bỏ yêu cầu tương đương phổ quát. I1 của M9 vẫn giữ các lệnh cũ trong workflow nguyên trạng, đo bằng `structure_checks.py`, và 68/68 fixture cũ trùng byte. Không ghi “CLI không đổi trên mọi đối số”, không coi cờ bị bỏ qua là đã được kiểm. |
| 7. Chạy đầy đủ `--dot-bien` hợp đồng trong tiến trình con song song | **Chấp nhận; đúng nghiệm thu 1** | Nghiệm thu bắt bộ test PR chạy lại phép kiểm đầy đủ. Đã đo base 8 s, H 220 s, delta +212 s; executor ước +210 s được tái lập gần đúng. Chạy con sớm chỉ chồng thời gian các ca, không giảm số phép kiểm. Timeout của tiến trình con là 3600 s; thời gian runner 2 nhân chưa đo, nên không suy con số tại chỗ thành chi phí runner. |

Lựa chọn 6 không xóa dữ kiện base rc2 → H rc0 trên các cờ mới. Phán này dựa vào phạm vi nghiệm thu 5 hiện hành và câu I1 nói về M9/ba job cũ; nếu bên điều phối muốn hợp đồng CLI cấm mọi tổ hợp chế độ thì phải ghi điều đó tường minh, không phục hồi ngầm lời khai tương đương đã bị bỏ sau review r4.

## Phép đo bổ sung đã hoàn tất

- **A/B fixture committed:** `python3 -B out/ab_committed_fixtures.py`, rc0; `COMMITTED WP1166: 75/75 ca goc dat`; `A/B CLI COMMITTED FIXTURES: 68/68 trung byte (stdout, stderr, rc, cay chon)`. Script trích nguyên khối ca wp1166 của H, giữ các assertion gốc, chặn tại lời gọi selector để gọi hai CLI trên cùng cây input; các đối số Python sai kiểu không bị giả làm CLI. Hai clone dùng chung lần dựng của `ab.sh`.
- **Mutant băm ghép:** trên clone `review-scratch/dot`, áp đồng thời 3 phép gán băm sai đã chứng minh độc lập rồi chạy `python3 -B .claude/dev/ci_dang_ky_test.py`: **rc0; `PHẢN CHỨNG: 1556/1556 đỏ đúng`; `TỔNG: ĐẠT`**. Đây là bằng chứng độ phủ thiếu; không phải kết quả candidate H không đổi. Log `survivors-full-suite.log`. Một lần chuẩn bị giàn trước đó có mỏ neo chồng nhau, đã bị hủy và **không** được tính là phép đo mutant (`survivors-setup-aborted.log`).
- **I1 và đường cũ:** `python3 -B out/structure_checks.py`, rc0: bỏ đúng hai bước dấu ở từng job cũ và job thu mới thì YAML parsed bằng base; bốn hàm legacy `chon_bien_nhan_du`, `kiem_bien_nhan_du`, `loi_bien_nhan_du`, `_loi_mot_bien_nhan` giống nguyên nguồn giữa base/H. Probe ban đầu xóa theo chỉ số cố định sai vì job đầu có bước Force LF trước checkout; đã sửa giàn sang nhận diện đúng cặp bước thêm, không báo false-positive đó thành finding.
- **Hợp đồng file:** schema sha256 `844b5218b6f6844945f5c4c9440f09015d238fe09a60d64b3787c440787e4f46`; fixture `ce8595739a1ab2f4a86c9c196255e5f91fb19a9f6d3865df6caa2d66f9970e6d`; cả hai byte-identical với `d26c8ae8…`. `git diff --check` rc0. Quét toàn 4 tệp và toàn thông điệp commit base..H: **0 dấu bỏ qua CI**. Không tệp thứ năm.
- **Môi trường:** Linux, Python **3.13.18**, jsonschema **4.26.0**, Ruff **0.15.15**, actionlint **1.7.7**, ShellCheck **0.9.0**. Workflow sẽ dùng Python 3.12; chưa đo trên runner thật. Ruff bare F tách biệt với contract Ruff CI 3/3 của suite.

Các lời khai cổng lân cận trong handoff cũng đã đo lại, không chỉ đọc log executor:

| Phép đo | Lệnh trong clone H | rc / bằng chứng dương |
|---|---|---|
| Provenance | `python3 -B ops/ci_provenance_test.py` | **0**; `CA: 77/77 dat`; `DOT BIEN: 485/485 bi giet dung ly do`; `TU KIEM PHAN HANG: DAT (2 dot bien)`; `TONG: DAT`; 619,34 s |
| Gate-output | `python3 -B ops/gate_output_doi_chieu_test.py` | **0**; `CA: 51/51 dat`; `DOT BIEN: 158/158 bi giet dung ly do`; tự kiểm 2/2; `TONG: DAT`; 247,48 s |
| Công cụ, base và H | `python3 -B ops/cong_cu.py kiem-tra --json` | **0/0**; JSON trùng byte, 1.944 ký tự mỗi bản |
| Doctrine, base và H | `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .` | **0/0**; `doctrine-scan: sạch — đã quét 12 tệp, 0 chỗ chép doctrine` |

## KHÔNG ĐO ĐƯỢC / không chạy

- **not_run:** workflow/REST GitHub thật, PR Ubuntu CI, K7, hai canary A3, rerun attempt thật, quan sát push đồng thời, schedule sau merge; nghiệm thu 8/10/11 và các mốc land do điều phối/người có quyền thực hiện. Không gọi dispatch, không push/commit/merge, không dùng quota M9 của GitHub. Verdict này không cho phép land hoặc thay owner exact-H audit.
- **not_run:** Windows và Python 3.12/runner Ubuntu thật; các số thời gian là máy Linux hiện tại. Toàn bộ registry `--chay` và `ops/ci_duong_nhanh_test.py` không nằm trong những lệnh đã chạy ở lượt này.
- **not_measured:** giá trị context thật của GitHub; hình REST jobs khi rerun qua nhiều attempt; hành vi download-artifact thực đối với artifact attempt cũ; quan hệ byte REST với OID trên máy chủ. Gh giả và fixture offline không chứng minh những điều đó.
- **not_measured:** các hướng payload đường dẫn/ký tự điều khiển/Unicode/khóa JSON trùng ngoài ca đã commit như bảng trên. Không viết payload tấn công để lấp ô độ phủ.
- **not_measured:** model/effort thực sự phục vụ từng request và mã thoát cuối/stdout hash ổn định của launcher đang bao phiên này. Metadata launcher đo được đã ghi riêng; coordinator cần hoàn tất receipt sau khi phiên kết thúc. Hash các output test và verdict bàn giao nằm trong `SHA256SUMS`.
- `/tmp/.git` **có tồn tại** khi reviewer kiểm và ở cuối; không phải “vắng” như môi trường executor từng khai. Không xóa vì không có bằng chứng nó do reviewer tạo. Không biến khác biệt môi trường này thành lỗi mã; các gate báo đạt ở điều kiện đã ghi.

## Toàn vẹn checkout và bàn giao

Đã băm nội dung toàn bộ **17.994 tệp worktree** quan sát được trước/sau, gồm tệp ẩn/ignored: **0 thêm, 0 xóa, 0 đổi byte**; `git status --porcelain` rỗng, diff/index rỗng. HEAD/tree cuối vẫn đúng H/tree đầu báo cáo. Bằng chứng `read-only-check.json`, `src-before.json`, `src-after.json`. Phép so hai mốc chứng minh không có delta quan sát được; không phải chứng minh lịch sử mọi syscall, cũng không gán sandbox write protection riêng cho `src/`.

Các script, dữ liệu kết quả và log dương/âm được giữ trong `out/`; chỉ các clone và tệp nháp do reviewer dựng được dọn. Cách tái dựng phép đo ở [REPRODUCE.md](REPRODUCE.md). Không sửa code để chữa finding trong lượt review này.
