VERDICT: approve
reviewed_sha: f5af7469c03e7fe421a3704c731f390842260304
reviewed_tree: 3f977dc24ae10e4d5007845584469ba3247b9c1d
spec_sha256: 280f6f8d0dc97f29a79ed8ef94d3070d8ae1fe0487b549054137bcdbc4acbb0c

**Approve review mã H4: không còn finding P0–P2 được xác nhận; không có finding P3 mới.** H4 bỏ được hồi quy do trần 64 và chặn các đường tràn validator đã tái hiện, đồng thời giữ các sửa F01/F03/F04. Đây là kết luận review mã offline, không thay owner audit exact-H, CI PR, K7, canary A3 hay quyền push/merge.

## Định danh, phạm vi và hai trục

Reviewer độc lập với executor. Metadata `runs/aaaf15c6/run.json`: provider `openai_codex`, execution surface `codex_cli`, transport `machine`, run ID `aaaf15c610244e30a33a748d6bc8b8a1`. Sandbox quan sát `workspace-write`, approval `never`. Model/effort thực sự phục vụ: **KHÔNG ĐO ĐƯỢC**; không lấy tên model trong prompt làm bằng chứng runtime. Xem [review-runtime.json](review-runtime.json).

Đã đo băm SPEC **trước khi đọc**; khối Python trích độc lập có băm `d9c78e708e18a211b7d8c7309638ffd1c73200578cf3128f9f0fc4275430f24e`. H4/tree/cha khớp chỉ thị. Base `5259239d763c9ffc1677f033bd9a9cf23ede9299`, base tree `f51dd6a68bd96bcf71a1fb351e652a3eee318a1b`. Chuỗi cha H3 `d1c28891acec4f861a9f26e092d92b71bd08af9d` → H2 `1c31f5a88ba125af708a9609085c0edd2f8dc3ee` → H1 `4cad0e1c140ced47030b5c2834ae000d9670671f`. Lease g4 từ ref đã giao khớp spec/write set/trần 6 tệp, 1700 dòng; có nợ phương án (b). Không suy nợ ấy thành miễn finding hay revision đặc tả đã làm.

| Trục | Kết luận trên H4 |
|---|---|
| **Spec** | Đạt phạm vi review mã: dữ liệu đọc được, trường dư hợp lệ được giữ xanh; đầu vào sai đã đo cho receipt đỏ hợp lệ; oracle đóng băng, các chốt và hồi quy cũ đạt. Các nghiệm thu online/sau merge vẫn `not_run`. |
| **Standards/Security** | Không phát hiện P0–P2: context qua env, dấu lỗi nguồn không bị JSON tốt che, định danh/băm có phép kiểm độc lập. Catch mới đặt tại consumer, không có catch toàn hàm thu. Không tuyên bố đã kiểm an toàn giải nén/runner thật. |

## Đối chiếu các lớp finding trước

Mỗi lớp chỉ mang một nhãn trên H4. Lớp `v1-not-fully-specified` giữ nguyên lịch sử B1-04/F02/F02-R2/F02-R3; kết luận dưới áp cho phần lệnh thu B1a, không nhận đã triển khai những phần chuyển sang B1b.

| Lớp / finding | Nhãn H4 | Bằng chứng chạy được |
|---|---|---|
| F01 — `rest-error-sidecar-ignored` | **ĐÃ SỬA ĐÚNG LỚP** | Probe R1/R2 chạy lại bốn endpoint: `.loi` cạnh JSON khiến ba điểm lõi đỏ, definition `not_measured`; `.loi` rỗng/thư mục cũng được nhận. Bốn mutant gỡ riêng reader tại từng endpoint GIẾT. [reviewer-probes.json](reviewer-probes.json), [round2-probes.json](round2-probes.json), [rerun-executor_mutants.log](rerun-executor_mutants.log). |
| F03 — `workflow-context-interpreted-as-shell` | **ĐÃ SỬA ĐÚNG LỚP** | Bash thật giữ đủ 10 context với bốn ref thường/nháy/dollar/Unicode; từng mutant đưa context trở lại thân lệnh bị đúng ca giết. Ba hàng shlex cũ không giải env không phải phép đo hồi quy hợp lệ. [round2-probes.json](round2-probes.json), [round2-mutants.json](round2-mutants.json). |
| F04 — `collector-derived-evidence-unasserted` | **ĐÃ SỬA ĐÚNG LỚP** | Ba mutant băm giả từng sống nay GIẾT; nguồn băm được so độc lập với blob REST/byte definition/byte công cụ, cả hình xanh và đỏ. Mutant băm checkout thay byte REST cũng GIẾT. [reviewer-mutants.json](reviewer-mutants.json), [hash-evidence.json](hash-evidence.json). |
| F02/F02-R2/F02-R3 — `v1-not-fully-specified` | **ĐÃ SỬA ĐÚNG LỚP** | Ngày 0001/0999, YAML 64/512/900 và sáu lớp lỗi parser đều có receipt hợp lệ; tám chốt còn lại từ H3 (sáu catch, UTF-8, I/O tên) có răng. 30 nhóm H2/H3/H4 khôi phục 14 ca xanh→đỏ và ba ca definition mất measured của H3; 1680 lượt độc lập mỗi Python 3.12/3.13 không sập/sai schema. Gỡ chốt validator tái hiện sập thực, H4 cùng dữ liệu luôn đỏ hợp lệ. [yaml-boundary-h4.json](yaml-boundary-h4.json), [depth-contract-h4.json](depth-contract-h4.json), [input-sweep-312.json](input-sweep-312.json), [input-sweep-313.json](input-sweep-313.json). |

## Finding mới

| ID | P0–P3 | Lớp | Tệp:dòng | Mô tả | Bằng chứng chạy được | Gợi ý |
|---|---|---|---|---|---|---|
| — | — | — | — | Không có finding mới được xác nhận trên H4. | Các bảng đo, đột biến và câu hỏi cấu trúc dưới đây. | Giữ những ca reviewer bổ sung khi bảo trì; không coi mọi mutant sống ở một ca đích là lỗi sản phẩm. |

Không hạ severity vì đây là lượt cuối. Hai giới hạn cần tách rõ: ca UTF-8 cũ chưa phủ giá trị matrix; cổng độ sâu theo phiên bản có thể biến mất sau khi nâng Python. Đã đo cả hai và giải thích vì sao chúng không chứng minh H4 hiện hành vi phạm r9/CI ghim 3.12.

## Đo lại lời khai

Môi trường chính: Linux, Python **3.13.18**, PyYAML **6.0.3**, jsonschema **4.26.0**, Ruff **0.15.15**, actionlint **1.7.7**, ShellCheck **0.9.0**. Đo thêm Python **3.12.13**, **3.11.18**, **3.14.6** có sẵn, không tải/cài dependency. Hai clone A/B được dựng trong cùng vòng lặp, `core.abbrev=7`.

| Lời khai / phép đo | Kết quả lần này |
|---|---|
| Numstat base..H4; H3..H4 | Đúng **4 tệp +1693/−20**; Python +1411/−20, workflow +87, schema +34, fixture +161. H3..H4 chỉ Python **+119/−24**. |
| Hai tệp hợp đồng | Đúng băm ghim, trùng byte SPEC; bảng băm ở cuối. |
| Suite H4 Python 3.13.18 | **rc0; 1677/1677; TỔNG: ĐẠT; 268 s** trong A/B. Lời khai ~267 s khớp mức sai khác thời gian thường. Base **rc0; 1226/1226; 7 s**; delta tại máy này +261 s, không phải số đo runner. [ab.log](ab.log), [ab-suite-sau.out](ab-suite-sau.out). |
| Suite H4 Python 3.12.13 | **rc0; 1677/1677; TỔNG: ĐẠT; 278,216 s**. Đã bổ sung rc/thời gian bị mất trong handoff. [suite-python312-venv.result.json](suite-python312-venv.result.json), [log](suite-python312-venv.log). |
| Đột biến committed | **112/112 giết đúng lý do; 6/6 tự kiểm; nền 105/105** ở cả hai suite. Chạy riêng bảng: **rc0**, 118 hàng đúng phân hạng. [rerun-executor_mutants.log](rerun-executor_mutants.log). |
| Nghiệm thu 1 độc lập | **rc0; 480/480; 249/249 = 57 vị từ + 192 schema; TONG: DAT**, 195,478 s. Trích từ SPEC, không dùng bản oracle trong code làm nguồn. [nghiem-thu-1.log](nghiem-thu-1.log). |
| A/B nghiệm thu 5 | **32/32** trùng stdout/stderr/rc/cây chọn; A/B fixtures committed **68/68**, **75/75 ca wp1166 gốc đạt**. [ab.log](ab.log), [rerun-ab_committed_fixtures.log](rerun-ab_committed_fixtures.log). |
| actionlint/Ruff | Base/H4 đều rc0; actionlint **0/0 finding, delta0**, ShellCheck có mặt; bare Ruff F **delta0**. Không đánh đồng với marker `RUFF CI: 3/3 hợp đồng`. |
| Probe R3 nguyên bản | **rc1 đúng lý do dự kiến**: assertion yêu cầu cột ứng viên vẫn đỏ với ghi chú dư không còn đúng. 24 hàng đã được ghi trước assertion. Tên cột `H3` trong giàn gốc thực chất nạp clone ứng viên **H4**. [depth-original.log](depth-original.log). |
| Probe R3 thích nghi H2/H3/H4 | **rc0; 30 nhóm × 3 bản**, độ sâu 0/60/64/70/300: H4 khớp H2 về rc/ok/vi phạm consumer/definition; **25/25 xanh**, **5/5 dấu sai hình đỏ**, definition **5/5 measured**. Gồm 10 ca đỏ sai R3 + 4 ở tầng300; 3 downgrade definition ở H3 đã hết. [depth-contract-h4.json](depth-contract-h4.json). |
| Ca dương H4 mới | Năm vị trí run/jobs/artifacts/definition/mảnh × 60/64/70/500 đều đạt qua ca committed, có oracle consumer; năm mutant trả lại trần đều bị ca tương ứng giết. Không dùng deepcopy của giàn R3 để tuyên bố đã đo tầng500. |
| Probe YAML R2 nguyên bản | **rc0; 8/8**, nhưng chỉ đọc H1/H2 và bản catch tạm, không được lấy làm bằng chứng H4. |
| Probe YAML thích nghi | **rc0; 12/12** H1/H2/H3/H4 ×64/512/900. H4 cả ba `rc1 + receipt hợp lệ + X2`; H1/H2 còn sập ở512/900. Probe R3 lịch sử cũng chạy riêng. [yaml-boundary-h4.json](yaml-boundary-h4.json). |
| Mutant reviewer R1/R2 | Sau thích nghi mỏ neo: R1 **40 GIẾT + 1 tự kiểm lỗi vô can**, nền41/41; R2 **45 GIẾT + 2 tự kiểm sai lớp/tên**, nền47/47. [reviewer-mutants.json](reviewer-mutants.json), [round2-mutants.json](round2-mutants.json). |
| Probe dữ liệu/lớp/cấu trúc trước | R1 40 hàng (37 dữ liệu + 3 shlex hạn chế); R2 **78 hàng, 0 bất ngờ**; bổ sung **7 ca YAML/số lớn + 28 cấu trúc JSON sâu**; **26 phép class evidence** đạt. AST bốn hàm legacy không đổi, YAML trừ đúng phần thêm bằng base. |
| Sweep riêng reviewer | **35 vị trí ×2 kiểu ×24 độ sâu =1680 lượt/Python**, trên3.12 và3.13: **0 sập, 0 receipt sai**. Thêm **35 cặp H2/H4** và **99 cặp bỏ chốt/H4** mỗi nền. [sweep312.log](sweep312.log), [sweep313.log](sweep313.log). |
| Sweep executor đo lại | Giàn chép, chỉ đổi gốc checkout: **1452 lượt mỗi Python3.11/3.12/3.13**, **748 bổ sung mỗi3.12/3.13**, tất cả0 sập/sai schema. Python3.14 quét thô **1122 lượt ở17 độ sâu**, 0 lỗi; không suy thành chứng minh mọi độ sâu. [executor-sweeps.log](executor-sweeps.log), [executor-sweep314.log](executor-sweep314.log). |
| Ca/đột biến mới theo nền | Python3.11 và3.13: **15/15**, Python3.14: **12/12** vì ba hàng KHE không được tạo. Suite3.12 đã chạy đủ15. [platform-3.11.18.json](platform-3.11.18.json), [platform-3.13.18.json](platform-3.13.18.json), [platform-3.14.6.json](platform-3.14.6.json). |
| Dữ liệu thường bổ sung | **63/63** có receipt hợp lệ: base64/definition sai kiểu, digest/id/tên, total_count, JSON là thư mục, ghi chú YAML dùng chung alias và Unicode. Hai ghi chú không dùng giữ xanh. [ordinary-data.json](ordinary-data.json). |
| Fuzz a5/b5/c5: 571/392/6000 | **Không xác nhận lại nguyên bộ**; xem KHÔNG ĐO ĐƯỢC. Không lấy số của executor làm bằng chứng reviewer. Probe tên byte đặc biệt được đo độc lập bằng fixture thường ở [matrix-name.json](matrix-name.json). |

Mọi command/rc/thời gian ở [command-results.json](command-results.json), rc từng script cũ ở [previous-command-results.json](previous-command-results.json). Các lần rc1 do giàn cũ vẫn giữ: R1/R2 mutant mất mỏ neo `is_valid`; R1 thất bại khiến giàn hash R2 ban đầu thiếu JSON phụ thuộc; R3 mutant mất trần; giàn signal R3 đòi4 hàng trong khi chốt trần đã xóa. Bản thích nghi chỉ sửa mỏ neo/kỳ vọng giàn, không sửa `src/`. Lần gọi Python3.12 đầu tiên resolve tới interpreter nền thiếu PyYAML cũng được giữ log riêng, không tính pass.

## Đo răng từng chốt mới trên bản sao

[round4_mutants.py](round4_mutants.py) phân hạng độc lập với helper sản phẩm: **`type(exc) is mod.TinHieuChotCa` và `exc.args == (case,)`**. Mỗi lần chỉ áp các thay thế của một hàng lên bản mới, tên tệp riêng, tắt bytecode. Nền25/25 ca đích đạt. Không đếm ngoại lệ nạp module hoặc lỗi vô can là giết.

| Mutant gỡ chốt H4 / trả lại hồi quy | Tên ca đích đầy đủ | Kết quả |
|---|---|---|
| `f02r3-bien-nhan-khong-xanh-is-valid-khong-chot` | `wp1460-con-khong-vo-thu-hinh-khong-xanh-bo-kiem-tran-de-quy-van-ghi` | **GIẾT**, đúng lớp/tên |
| `f02r3-gia-tri-ly-do-repr-de-quy` | `wp1460-con-khong-vo-thu-gia-tri-ly-do-khong-de-quy` | **GIẾT**, đúng lớp/tên |
| `f02r3-ly-do-run-repr` | `wp1460-thu-am-x1-run-id-la-danh-sach` | **GIẾT**, đúng lớp/tên |
| `f02r3-ly-do-digest-repr` | `wp1460-thu-am-x7-digest-la-danh-sach` | **GIẾT**, đúng lớp/tên |
| `f02r3-ly-do-ket-luan-repr` | `wp1460-thu-am-x3-ket-luan-la-object` | **GIẾT**, đúng lớp/tên |
| `f02r3-ly-do-head-repr` | `wp1460-thu-am-x5-head-la-danh-sach` | **GIẾT**, đúng lớp/tên |
| `f02r3-ly-do-manh-repr` | `wp1460-thu-am-x5-manh-la-danh-sach` | **GIẾT**, đúng lớp/tên |
| `f02r3-tran-do-sau-64-tro-lai-run` | `wp1460-thu-duong-truong-du-long-sau-run` | **GIẾT**, đúng lớp/tên |
| `f02r3-tran-do-sau-64-tro-lai-jobs` | `wp1460-thu-duong-truong-du-long-sau-jobs` | **GIẾT**, đúng lớp/tên |
| `f02r3-tran-do-sau-64-tro-lai-artifacts` | `wp1460-thu-duong-truong-du-long-sau-artifacts` | **GIẾT**, đúng lớp/tên |
| `f02r3-tran-do-sau-64-tro-lai-definition` | `wp1460-thu-duong-truong-du-long-sau-definition` | **GIẾT**, đúng lớp/tên |
| `f02r3-tran-do-sau-64-tro-lai-manh` | `wp1460-thu-duong-truong-du-long-sau-manh` | **GIẾT**, đúng lớp/tên |
| `f02r3-dau-job-is-valid-khong-chot` | `wp1460-con-khong-vo-thu-quet-bien-de-quy-dau-job` | **GIẾT**, đúng lớp/tên |
| `f02r3-bien-nhan-xanh-is-valid-khong-chot` | `wp1460-con-khong-vo-thu-quet-bien-de-quy-bien-nhan-xanh` | **GIẾT**, đúng lớp/tên |
| `f02r3-quet-khong-cham-gioi-han-thi-ca-do` | `wp1460-con-khong-vo-thu-quet-bien-de-quy-dau-job` | **GIẾT**, đúng lớp/tên |

15/15 trên là kiểm lại chốt của executor, **không cộng vào số mutant reviewer tự chọn**. Với hai ca quét thực tế, [round4-signals.json](round4-signals.json) quan sát: bản H4 hoàn thành43/43 lượt/ca, mọi receipt đỏ hợp lệ; bỏ chốt dấu sập tại lượt40, bỏ chốt hình xanh sập tại lượt36 trong ngữ cảnh observer này. Ngoại lệ là `RecursionError`, không có receipt ở lượt sập. Wrapper tiến trình con chuyển đúng sự cố đích thành `TinHieuChotCa` như bảng trên.

## Đột biến reviewer tự chọn và ba mutant SỐNG R3

| Mutant riêng lượt4 | Kết quả ca đích | Ý nghĩa |
|---|---|---|
| Trả trần65 ở run; trả trần65 ở mảnh | **2 GIẾT** | Các ca dương mới không chỉ chống đúng con số64. |
| Trả trần64 chỉ đường đọc tệp; chỉ đường bytes | **2 GIẾT** | Ca run và mảnh bảo vệ cả hai họ caller của reader. |
| `_hop_le_du` trả True khi tràn | **GIẾT** | Không thể biến không xác nhận được hình thành xanh. |
| `_hop_le_du` luôn False | **GIẾT** | Đối chứng dương ngăn giải pháp luôn hạ đỏ. |
| Bỏ yêu cầu `tran > 0` đồng thời quét60–70 | **SỐNG** qua ca quét đích | Đây là sửa chính test để tự nhận đã đo; không phải lỗi collector H4. Mutant committed chỉ đổi độ sâu nhưng giữ `tran > 0` đã bị giết. Không khai biến thể hai sửa này sống toàn suite. |
| Chỉ encode UTF-8 khóa job, bỏ phần matrix | **SỐNG** qua ca committed cũ | Đúng lỗ độ phủ đã biết; probe matrix nhất quán riêng bên dưới GIẾT đúng tên tín hiệu. H4 có chốt đúng. |
| Ném KeyError vô can | **GIẾT SAI LÝ DO** | Tự kiểm, không cấp tín dụng. |
| Ném TinHieuChotCa tên khác | **GIẾT SAI LÝ DO** | Tự kiểm, không cấp tín dụng. |

Tổng **10 mutant tự chọn: 6 GIẾT, 2 SỐNG, 2 GIẾT SAI LÝ DO**. Cùng15 hàng kiểm lại chốt:25 hàng,21 GIẾT/2 SỐNG/2 sai lý do. Mỏ neo, tên ca, lớp/args cụ thể ở [round4-mutants.json](round4-mutants.json).

| Ba SỐNG của lượt3 | Trạng thái thực đo trên H4 |
|---|---|
| `depth-cap-file-only-bypasses-stamp-shard` | **KHÔNG ÁP DỤNG nguyên mutant**: trần và ca đích cũ đã bị xóa. Không báo giả là GIẾT. Biến thể trả lại trần chỉ tệp/chỉ bytes nay bị các ca dương mới GIẾT. |
| `depth-cap-off-by-one` | **KHÔNG ÁP DỤNG nguyên mutant**: không còn hằng64. Hai biến thể trả lại65 nay GIẾT. |
| `utf8-keys-only-bypasses-matrix-values` | **Vẫn SỐNG qua ca đích committed**, không khai đóng bằng tỷ lệ suite. [matrix_name.py](matrix_name.py) dựng thêm job matrix, YAML/REST/dấu/tên thư mục cùng dữ liệu: tên Unicode thường xanh ở cả H4/mutant; tên dùng surrogateescape khiến **H4 rc1 + receipt hợp lệ**, mutant **UnicodeEncodeError + không receipt**. Ca reviewer `reviewer-r4-matrix-expanded-name-must-preserve-valid-receipt` GIẾT đúng lớp/tên. [matrix-name-signals.json](matrix-name-signals.json). |

Giàn R3 thích nghi có18 hàng: tám chốt H3 còn áp dụng đều GIẾT; các mutant riêng4 GIẾT/1 SỐNG/2 sai lý do; ba mutant dựa trần ghi không áp dụng. Các kết quả SỐNG đều chỉ có nghĩa trong miền ca đích được nêu.

## Câu hỏi cấu trúc 1 — lớp nguyên nhân và mọi consumer

**Trong đường CLI với code/schema/thư viện ghim và khả năng đọc/ghi bình thường, đã đóng các biểu hiện dữ liệu của lớp này; không tìm thấy đường sập còn nằm ngoài chốt.** Không có cơ sở nhận là VÁ HỜ chỉ vì máy hữu hạn không có tính toàn phần toán học. Kết luận dựa cả dữ liệu dương, dữ liệu sai hình sát biên và độc lập kiểm các consumer, không dựa riêng số suite.

Danh sách độc lập đã được ghi **trước lần mở HANDOFF.yaml**, ở [inventory-before-handoff.md](inventory-before-handoff.md). Đối chiếu sau đó khớp C1–C6 của executor; còn bổ sung I/O, encoding, helper context, dependency và các đường không đệ quy. Bảng đầy đủ theo nhóm:

| Consumer / vị trí trong `.claude/dev/ci_dang_ky_test.py` | Vì sao không còn đường đệ quy dữ liệu chưa chốt / phép đo |
|---|---|
| `doi_so_thu`,1820; regex/int/encode/repr argv | CLI chỉ nhận chuỗi; số tối đa19 chữ số; UTF-8 được kiểm; lỗi đối số rc2/no receipt. Các ca cũ tiếp tục đạt. `workflow_sha` chỉ lọc40hex, không xuất container tùy ý. |
| `_doc_json_du`,1614; file/read_text/decode/json.loads | OSError/ValueError/RecursionError thành unreadable; một reader cho REST và bytes dấu/mảnh. Không còn trần riêng. Quét sâu cả sáu nguồn + mutant bỏ catch đã chạy. |
| `job_ky_vong_du`,1591; đọc UTF-8, YAML parser | Sáu ngoại lệ ngoài YAMLError/ValueError chỉ được chuẩn hóa quanh `safe_load`. Sáu ca thực + sáu mutant; lỗi traversal cố ý sau parser vẫn TypeError thoát, không bị nuốt. |
| Traversal YAML; `repr(k)`, `str(v)`, f-string matrix, encode tên, set | Chỉ hai hình job, khóa str, giá trị matrix str/int, giới hạn chuỗi64; danh sách tên đã được kiểm UTF-8. SafeLoader không cho khóa container không hashable đi qua như khóa job hợp lệ. Ca tên lạ, số lớn, alias ghi chú và matrix nhất quán đã đo. |
| `_gop_trang_du`,1638 | Duyệt hai tầng, không duyệt sâu nội dung; tổng chỉ vào set sau `type is int`. Trang/record sai kiểu và total_count container đều đỏ có receipt. |
| Run/repository comparisons,1693–1712 | So với scalar context và kiểm type trước `==`; không có phép so hai cây dữ liệu sâu. Regex/strptime mốc có kiểm kiểu; `_khung_du` bắt tràn ngày/định dạng. |
| Jobs/artifacts index,1719–1735; hash/set/sorted/count | Tên str, id/attempt int chính xác; set/tuple không mang container. Thông báo tập tên repr của danh sách chuỗi hữu hạn. Chi-so regex cố định, không regex do đầu vào cung cấp. |
| Năm vị trí lý do,1705/1745/1761/1768/1769 | `_gt_du` chỉ repr scalar; list/dict thành tên kiểu. Helper200000 tầng đo không đệ quy; năm caller có pin câu chữ. Không tuyên bố các pin này là năm ca sập thực. |
| `lay`,1739; Path/iterdir/read_bytes/hashlib | Tên được dựng từ kỳ vọng; phép đọc/list bắt OSError/ValueError. Ghi nhận hash từ bytes; không đi sâu JSON. Ca NUL/tệp là thư mục/thừa tệp đã đo. Không dựng đường thoát cây. |
| Dấu,1773 | `_hop_le_du` bắt RecursionError từ validator thật. Sau khi hợp schema chỉ lấy scalar để so/hash/dựng dòng. Cửa sổ sập thực đã tái hiện khi gỡ chốt. |
| Mảnh,1766–1770 | Object/head/manh kiểm riêng; so với scalar; head sai tạo lỗi trước khi đi xanh. Trường dư được bỏ qua đúng hợp đồng. Không đưa toàn cây mảnh vào receipt. |
| Definition,1786–1794; base64, hash blob, equality | Index/kiểu/base64 trong suppress(TypeError,KeyError,ValueError); lỗi decode thuộc miền này. Không mang nội dung sâu vào receipt. Băm/so chuỗi scalar;63 ca dữ liệu bổ sung và sweep có đường này. |
| Schema loader,1673 | Schema/code/dependency là hiện vật tin cậy ghim băm, không phải tệp thu tùy ý của CLI. Thiếu schema chuyển không xanh; schema test hook không được lấy làm chứng cứ đầu vào thực. |
| Validator receipt xanh/đỏ,1803/1807 | Cả hai qua `_hop_le_du`. started_at/completed_at chưa lọc kiểu được chặn ở hình xanh; hình đỏ chỉ context/chuỗi lý do/mốc scalar. Biến thể trả False mọi lúc bị ca dương GIẾT. |
| `json.dumps`,encode,write_bytes,1810 | Receipt xanh qua schema hữu hạn tầng; tất cả tên có thể xuất raw đã qua UTF-8/kết quả so bằng, mốc/SHA/digest có pattern. Hình đỏ không giữ cây đầu vào; repr chuỗi escape surrogate. Vì vậy không còn cây sâu cho serializer. Hai sweep1680 lượt không có receipt sai/mất; probe matrix phân biệt rõ bảo vệ encoding. |
| Băm `__file__`,clock và stdout | Byte chương trình/clock là dependency, không phải payload thu. Đầu module28–30 cấu hình UTF-8 + backslashreplace cho stdout/stderr. I/O thiết bị hỏng, mất chương trình, MemoryError là giới hạn thực thi, không được nhận đã xử lý. |

Bằng chứng độc lập về **sập đúng biên** khi bỏ catch, không có wrapper validator trong giàn này: Python3.13 — dấu checkout_tree sâu9997, job started_at/completed_at sâu9993/9994; Python3.12 — dấu9996, thời điểm9992/9993. Bản bỏ chốt ném `RecursionError`, không receipt; **H4 tại mọi điểm đó rc1, schema hợp lệ**. Mỗi nền còn99 cặp quanh biên,35 cặp H2/H4 và1680 phép kiểm khác. Không dùng các con số này như hằng portable; độ sâu phụ thuộc stack và parser.

## Câu hỏi cấu trúc 2 — giới hạn parser tự thân

**Không xếp giới hạn parser thành P0–P2 của PR này.** X1 yêu cầu REST “đọc được”; X5 yêu cầu tệp mảnh “đọc được”; mục3 quy định dữ liệu không đọc được cho receipt không xanh. Khi JSON parser tự từ chối tài liệu, các luật này không chứng minh đủ điều kiện xanh. `_doc_json_du` xử lý nó bằng cùng đường unreadable và vẫn ghi receipt hợp lệ. Definition không đọc được thì `not_measured`, vẫn có thể xanh như đặc tả cho phép.

Khác biệt đã đo với H3: trần64 tự loại tài liệu parser **đã đọc được** và oracle chấp nhận, nên H3 sai. H4 chỉ giữ giới hạn của chính parser. 35 cặp H2/H4 trên năm điểm dư, gồm sát biên, vượt biên và20000 tầng, **không có kết luận H2 xanh nào bị H4 đổi đỏ**; definition cũng khớp. 30 nhóm kiểm oracle ở độ sâu0–300 và các ca committed tới500 đều phục hồi xanh cần có. Dấu có trường dư vẫn đỏ vì schema cấm, không phải hồi quy.

Quyết định phương án(b) vẫn là nợ chuẩn hóa lời hứa toàn phần, nhất là OOM/I/O/schema môi trường. Đây không phải nhận đã sửa đặc tả hoặc miễn một phản chứng hợp đồng còn sống. Không đòi PR phải có parser phi đệ quy mới để nâng miền tài nguyên so với H2.

## Câu hỏi cấu trúc 3 — `KHE_1460` và CI

`gate-registry` của `.github/workflows/ci.yml:1064` ghim **Python3.12**, cài PyYAML6.0.3/jsonschema4.26.0. Job thu cũng ghim3.12. Với cấu hình hiện tại, cập nhật patch3.12 không tự trở thành3.14, nên **cổng không tự tắt im lặng trên CI được ghim này**. Đã chạy suite3.12.13 đầy đủ, có112/112 và hai ca biên thật.

**Có tắt im lặng nếu người bảo trì đổi interpreter sang≥3.14**: code không in skip/reason riêng. Thực nghiệm trên cùng3.13, chỉ đặt KHE=False trong bản sao:314→310 ca,118→115 mutant; đúng hai ca quét + hai wrapper và ba mutant biến mất. Trên3.14.6 thật KHE=False,12/12 hàng H4 còn lại đạt. Tổng309/114 ở3.14 còn giảm thêm một ca/mutant năm999 do `%Y` đã đệm bốn chữ số, là điều kiện có sẵn từ trước, không quy cả chênh lệch cho KHE.

Đây là điểm phải kiểm lại **khi nâng Python**, không phải bằng chứng cổng H4 hiện tại không chạy. Số đo3.14 chỉ là17 độ sâu/1122 lượt và12 mutant, chưa chứng minh mệnh đề “không tồn tại đầu vào parse được gây tràn” trên mọi patch/platform. Không dùng kinh nghiệm3.14.6 để miễn kiểm lại phiên bản tương lai.

## Câu hỏi cấu trúc 4 — ca có MẶT hay có ĐO

**Các ca thực sự chạy, nhưng mỗi ca chỉ chứng minh đúng tính chất nó đo.**

- Năm pin `_gt_du`: quan sát10 lần trước/sau gỡ caller, tất cả vẫn rc1 + receipt đỏ hợp lệ. Mutant làm câu lý do đổi nên `TinHieuChotCa` đúng lớp/tên; chúng **đo wiring và định dạng**, không tự chứng minh chống sập. Tính không đệ quy của helper được đo riêng bằng list200000 tầng và mutant trả lại repr. Nguồn dữ liệu parse được không tái hiện sập repr ở năm vị trí trong các sweep này; không bịa năm ca sập để hợp thức hóa bảng mutant. `ly_do` là văn bản cho người đọc, không mang nghĩa máy theo r9; đổi sang `<list>/<dict>` không đổi kết luận.
- Ca hình không xanh dùng schema tự tham chiếu: thực sự làm validator ném; H4 rc1 + receipt hợp lệ theo **schema đóng băng** và hai mốc null, bỏ chốt thì RecursionError/no receipt. Đây là **test đơn vị lỗi dependency qua hook**, không phải tệp thu khiến schema đóng băng tràn. Hình đỏ không giữ dữ liệu lồng, nên không lấy ca này làm chứng cứ một đường sập thực có thể tới từ REST/artifact.
- Hai ca dấu/hình xanh: đã quan sát43 lượt mỗi ca, đánh dấu `is_valid` thật sự không trả về ít nhất một lần; mutant quét xa biên nhưng vẫn giữ yêu cầu `tran > 0` bị GIẾT. Đây mới là bằng chứng hành vi chống sập trực tiếp. Giàn reviewer độc lập còn tái hiện thiếu receipt khi bỏ chốt mà không cần schema giả.

Vì vậy không coi năm pin và ca schema giả là “không làm gì”, cũng không dùng chúng để tuyên bố mạnh hơn phép đo. Phần chịu trách nhiệm chống lỗi dữ liệu thực đã có bằng chứng trực tiếp bổ sung.

## Hồi quy H3..H4 và bảy lựa chọn H1

| Lựa chọn / chốt đã chấp nhận | Kết quả H4 |
|---|---|
| 1. Ref bắt buộc | Giữ nguyên: thiếu/sai context rc2, không receipt. |
| 2. Cron phải có tham số; dispatch nhận chuỗi rỗng | Giữ nguyên trong CLI/ca dương và đối số. |
| 3. X5 kiểm chỉ số mảnh | Giữ chốt; mutant bỏ chỉ số vẫn GIẾT. Ghi chú dư được đọc và không ảnh hưởng chọn mảnh. |
| 4. Definition measured theo path/blob REST | Giữ băm/nguồn REST, không ép bằng checkout; khôi phục measured ở ghi chú dư sâu. |
| 5. Xanh sai schema phải đỏ | Giữ nguyên; bổ sung bắt tràn ở validator. Dữ liệu ordinary sai kiểu và thời điểm sâu đều đỏ hợp lệ. |
| 6. CLI cũ bỏ qua cờ mới trong phạm vi hẹp | A/B32+68 trùng byte; probe cờ mới vẫn base/head rc2/0 như lựa chọn đã nhận. Không tuyên bố tương đương mọi argv. |
| 7. Chạy đầy đủ oracle ở tiến trình con | Vẫn480/249, băm khối không đổi, suite hai Python đã chạy đầy đủ. |
| F01/F03/F04 | Các ca/mutant cũ còn đạt; ba tệp workflow/schema/fixture không đổi byte H3..H4. |
| P1 lượt executor5: sáu lớp lỗi YAML | Gỡ từng catch vẫn GIẾT đúng tên; TypeError traversal ngoài parser vẫn thoát, không bị catch che. |
| P2 lượt executor5: UTF-8 tên mở rộng | Giữ đúng `join(ra)`; fixture matrix nhất quán mới chứng minh H4 chống mất receipt, không chỉ ghim câu lỗi. |
| P4 lượt executor5: ValueError tên đường dẫn | Chốt riêng còn răng, NUL cho receipt đỏ hợp lệ. |
| Đổi `ly_do` thành `<list>/<dict>` | Mười phép quan sát trước/sau chỉ khác lý do; rc/ok/schema giữ nguyên. Consumer C1–C12 không dùng nội dung `ly_do`. |

## BẢNG SĂN

| Hướng / giả thuyết | Phép đo | Kết quả |
|---|---|---|
| 1. Bỏ trần64 có mở lại sập validator | Gỡ catch trên bản sao;99 cặp quanh biên mỗi3.12/3.13 | Sập đúng chỗ ở bản bỏ chốt, H4 không sập và receipt hợp lệ. |
| 2. Trường dư hợp lệ vẫn bị hạ đỏ |30 nhóm H2/H3/H4 +5 ca committed tới500 +35 cặp quanh/vượt biên | Không còn hồi quy H3; H4=H2, oracle rỗng ở các ca dương. |
| 3. Serializer/encode vẫn giữ cây sâu |35 vị trí ×2×24; matrix tên nhất quán |0 lỗi H4; mutant UTF-8 keys-only thiếu receipt bị ca reviewer giết. |
| 4. YAML catch quá hẹp hoặc che lỗi mã | Sáu mutant parser;64/512/900; alias ghi chú; TypeError traversal | Đóng lỗi parser cũ, không nuốt lỗi ngoài parser. |
| 5. Ca chống sập chỉ đo câu chữ |18 hàng observer baseline/gỡ chốt | Phân tách rõ5 pin text,1 dependency schema và2 biên dữ liệu thật. |
| 6. KHE tự mất trong CI hiện tại | Đọc pin CI; suite3.12; inventory False/True; interpreter3.14 | Pin3.12 giữ cổng; nâng3.14 sẽ bỏ4 ca/3 mutant, cần tái đánh giá. |
| 7. Base64/gộp trang/regex còn ngoại lệ |63 dữ liệu thường +sweep bổ sung17 điểm |0 sập/sai receipt; không dùng regex do đầu vào cung cấp. |
| 8. REST lỗi bị JSON che, shell mất context | Probe R1/R2 và mutant từng endpoint/context | F01/F03 giữ đóng. |
| 9. Hash/identity có tín dụng giả | Ba băm giả, băm tên/checkout sai nguồn, self-check lỗi vô can | Hash mutant GIẾT; tín dụng giả không tính. |
| 10. Hồi quy bộ chọn/hình workflow |32+68 A/B,75 ca gốc, AST/YAML | Trùng byte trong miền nghiệm thu5; I1 được giữ. |
| 11. Nới phép kiểm thành luôn đỏ/xanh | Mutant `_hop_le_du` trả False/True sai | Cả hai GIẾT; đối chứng dương có răng. |
| 12. Write set/CI marker/read-only | Băm/schema, numstat,4 commit messages,17994 file snapshots | Đúng4 tệp, trong trần,0 marker,0 đổi nguồn. |

Các hướng thù địch chỉ được mô tả/phân tích; fixture mới là dữ liệu JSON/YAML hữu hạn, trường ghi chú, kiểu sai, tên lạ dưới cây tạm. Không dựng payload thực thi, đường/symlink thoát cây. Không suy phép đo này thành bảo đảm an toàn của action giải nén hoặc mọi nguồn dữ liệu ngoài đời.

## Write set, P3 và KHÔNG ĐO ĐƯỢC

[identity-checks.json](identity-checks.json): đúng bốn đường lease, **1693≤1700**, còn7 dòng; `git diff --check` rc0. Quét toàn byte bốn tệp và toàn thông điệp bốn commit H1..H4 đối với các dạng đánh dấu bỏ-qua-CI chuẩn: **0 hit**.

| Hiện vật | SHA-256 |
|---|---|
| `bien_nhan_audit.v1.schema.json` | `844b5218b6f6844945f5c4c9440f09015d238fe09a60d64b3787c440787e4f46` |
| `fixture.json` | `ce8595739a1ab2f4a86c9c196255e5f91fb19a9f6d3865df6caa2d66f9970e6d` |

**Danh sách P3 còn mở dạng `{slug kebab-case, severity}`: `[]`.** Nợ phương án(b) vẫn được giữ như lease đã ghi; không gắn một P3 giả hay tự khai đã đóng nợ. Rủi ro khi nâng interpreter là điều kiện bảo trì được mô tả ở câu3, không có bằng chứng lỗi CI hiện tại.

**KHÔNG ĐO ĐƯỢC / not_run:**

- GitHub/REST/context/runner thật, CI PR Ubuntu, K7, canary A3, lịch/chạy lại/push sau merge; không tiêu quota M9, không cấp miễn Windows exact-H. Không kiểm live ref/lease ngoài snapshot được giao.
- Windows/macOS, runner hai nhân, Python/dependency khác các phiên bản nêu trên. Suite đầy đủ chỉ3.13.18 và3.12.13;3.11/3.14 là các sweep/ca/mutant đã ghi, không phải full suite.
- Toàn bộ các fuzz ngẫu nhiên `fuzz_a5.py`, `fuzz_b5.py`, `fuzz_c5.py` và số571/392/6000 từ handoff không được nhận là đã tái đo nguyên bộ. Khi kiểm giàn thấy chúng có các nhánh/tokens tạo dữ liệu thù địch vượt giới hạn fixture thường của chỉ thị lượt này (thẻ kiểu thực thi, expansion alias, tên đường tương đối); không chạy nguyên bộ. Đã thay bằng phép quét ordinary độc lập,63 ca bổ sung và probe matrix nhất quán; không gọi các tập thay thế là cùng phép đo. Không kết luận fuzz cũ sai.
- OOM/MemoryError, hết đĩa, output không ghi được, BrokenPipe/thiết bị I/O hỏng, mất byte chính chương trình; lỗi quyền thật dưới tài khoản không đặc quyền. Quyền000 dưới root không đo PermissionError thật.
- Tính toàn phần với schema/dependency tùy ý; schema tự tham chiếu chỉ là unit test qua hook. Không tuyên bố coarse sweep3.14 chứng minh không còn cửa sổ tràn ở mọi nền.
- Runtime model/effort thực sự phục vụ; receipt cuối của launcher đang bao phiên chưa có tại thời điểm viết.

## Kiểm cuối và hiện vật bàn giao

[read-only-check.json](read-only-check.json): **17994/17994 tệp** tracked/untracked/ignored của `src/` ở hai mốc, **0 thêm,0 xóa,0 đổi byte**; Git status/working diff/index diff rỗng; HEAD/tree/cha cuối giữ nguyên. Snapshot nội dung đầu lấy sau khi khởi động các giàn chỉ chạy trên bản sao; Git sạch đã kiểm trước đó. Đây là đối chiếu hai mốc, không phải giám sát syscall.

Không sửa branch nguồn, không commit/push sản phẩm hoặc ghi GitHub. Chỉ clone/mutant/fixture ở ngoài `src/`. Giữ `out/` gồm verdict, log, JSON, giàn tái chạy và băm; clone A/B do reviewer tạo được dọn sau khi chép log. Hướng tái chạy: [REPRODUCE.md](REPRODUCE.md). Nhật ký kết luận tạm được giữ ở [review-progress.md](review-progress.md).
