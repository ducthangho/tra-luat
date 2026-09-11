verdict: changes_requested
reviewed_sha: 01e7f77d707cb093b5ba6d9b9d8577f40d025488
luot: 7
so_lan_luot_nay_bi_chet_va_phong_lai: 0

0 finding P1 · 0 finding P2 · 1 finding P3

**Hai vế P3 lượt 6 đã đóng thật. Các kết quả của 8/8 lệnh được khai đều tái chạy khớp.** Finding còn lại là lỗi mới, hẹp hơn: phần nhập hiện vật giới thiệu script đo lượt 6 là “chạy lại được”, nhưng script trong kho thiếu đường chạy cùng đầu vào cần thiết. Không có finding về giá trị neo, hash, byte hay kết quả của các cổng đã khai.

Reviewer: Codex/OpenAI, GPT-6 theo cấu hình phiên; provider `openai_codex`, bề mặt agent API có shell Linux, transport `machine`, phiên độc lập với executor Claude. Không suy thêm model/effort từ tên gói. Authority/phạm vi: `PROMPT.md` do người dùng giao. Tree: `d9d4cc1f2edae522463899a86ebdbf0891531622`. Không có GitHub submitter trong lượt này.

**L** là `cay-kho/ops/land/pr489-land-evidence.yaml`, khớp nguyên byte `BAN-DANG-REVIEW.yaml`; **R1–R6** là các `ops/reviews/pr490-review-*-codex-verdict.receipt.yaml`. Các số đếm bên dưới ghi đơn vị và cặp bằng nhau. SHA, ID, số thứ tự bước/dòng/lượt, phiên bản, timestamp, rc và scalar trích lời khai là định danh/giá trị kỹ thuật. Tỉ lệ độ phủ ghi bằng phần trăm với tập tử và mẫu được định nghĩa riêng.

## ĐỐI CHIẾU LƯỢT 6

`van-xuoi-do-duoc-van-vuot-nguon`: **ĐÃ VÁ THẬT**.

| Vế được giao | Phép kiểm độc lập và kết luận |
|---|---|
| Runtime ở mục lục mất giới hạn nguồn | Diff thực có **9/9 hàng cũ được thay**; **9/9 hàng** nay có “ATTESTATION — toàn bộ khối runtime”, nói rõ thời lượng/lần đầu/model/effort từ `run.json` ngoài kho và thiếu log gốc. **5/5 hàng** thuộc #490, **4/4 hàng** thuộc #487/#489. Hàng R6 mới cũng có giới hạn này. **10/10 phép làm tròn giây** khớp scalar của receipt; đây chỉ là số học, không xác thực runtime. [Đối chiếu từng hàng](phep-do/index-audit.json). |
| Commit `13ba87d` nhận “ĐỦ BỘ” | R5 đã có đính chính bền, rút lời khai đủ bộ; phân biệt validator với selftest; ghi danh sách có/chưa có bằng chứng; mục lục thuật lại sự thiếu độ phủ. Tự đọc **40/40 bước YAML**, kiểm message cũ và chạy lại **8/8 lệnh** cho kết quả khớp. Chi tiết và tỉ lệ hiện tại ở mục sau. [CI](phep-do/ci-audit.json), [lệnh/log](phep-do/gates.json). |

Nhãn trên áp cho **2/2 vế cụ thể của lượt 6**, không phủ nhận lỗi tái lập mới được phát hiện trong hiện vật vừa nhập. Không tiếp tục giữ slug cũ mở chỉ vì có thể dùng tên lớp lỗi rộng để gộp thêm vấn đề khác.

**Về phạm vi chín hàng:** sửa là hợp lý. Mục lục là tài liệu tra cứu đang sống; cùng một lỗi giới hạn nguồn xuất hiện trong cùng tệp, và cùng một caveat sửa nó. **9/9 verdict lịch sử tương ứng giữ nguyên hash**. Các hàng thêm phạm vi chỉ sửa lời tóm tắt hiện tại, không viết lại kết luận reviewer của PR đã merge, không thay code/quyền land/doctrine. Đây là sửa đầy đủ các bản lặp của finding, không phải scope creep.

**Đính chính riêng lời giao việc:** đếm tiêu đề thực cho thấy slug này xuất hiện ở các lượt **1, 2, 3, 4, 6**: **5/5 lượt có finding**, nhưng không phải chuỗi liên tiếp “2→6”. Lượt 5 có **0/0 tiêu đề finding** và ghi **ĐÃ VÁ THẬT** trên `dccce0a`. Đây là sai số lịch sử trong prompt gói, không tính thành finding của PR. [Tiêu đề và nhãn](phep-do/reviews.json).

## KIỂM LỜI ĐÍNH CHÍNH "ĐỦ BỘ"

Tôi parse trực tiếp `.github/workflows/ci.yml`, đọc thân `run`, `uses` và `if`, rồi mới đối chiếu JSON lượt 6. Kết quả: **40/40 bước** = **8/8 setup** (vị trí 1–7, 9) + **31/31 bước kiểm** + **1/1 upload** (vị trí 29). Hai hiện vật JSON giữ đúng **40/40 step object** và **40/40 phân loại**; tên `artifact` trong bản nhập và `upload` của phép đo này chỉ cùng một loại bước. MOI trong registry có **8/8 suite gián tiếp**, không cộng chúng thành bước top-level. [Bảng đầy đủ lệnh và điều kiện](phep-do/ci-audit.json), [MOI](phep-do/code-scope.json).

Message `b43d784` và `13ba87d` nêu **6/6 tên cổng**, nhưng chỉ **2/2 mục tương ứng** với bảng CI: vị trí 19 (lease suite) và 32 (doc-claims). Vì thế lời “hai bước được nêu trong tổng ba mươi mốt” đúng ở nghĩa **tên đích kiểm được khai**. Nó không chứng minh đã chạy trọn hai bước CI: vị trí 19 gọi wrapper cài actionlint rồi mới chạy suite. Bản đính chính đã giữ caveat ấy. Có **1/1 commit chen giữa** `b43d784` và `13ba87d`, là `16663ca`; không đọc câu “cách nhau một commit” thành hai commit liền nhau. [Message nguyên văn](phep-do/commit-messages.json), [diff](phep-do/diffs.json).

| Lệnh hiện được khai | Tái chạy tại exact head đang review; tất cả `rc=0` | Liên hệ với CI |
|---|---|---|
| `python3 ops/bien_nhan_v2.py --root .` | **100/100 bản ghi**: **47/47 v2 đạt**, **11/11 legacy**, **42/42 nợ**; **0/0 vi phạm**, **0/0 chưa đo**; `TỔNG: ĐẠT` | Validator này không thay bước selftest 14. |
| `python3 ops/bien_nhan_v2_test.py` | **48/48 ca đạt**, **63/63 đột biến thường CÓ RĂNG**, **2/2 ca tự kiểm đạt**; `TỔNG: ĐẠT` | Khớp thân `run` bước 14. Log còn tách **45/45 đột biến thường có khai đối chứng** trong tập **63/63 đột biến thường**; không nhận toàn bộ đều có đối chứng. |
| `python3 ops/lease_publish_test.py` | **121/121 ca đạt**, **121/121 ca chạy**, **0/0 ca bỏ qua**; actionlint `1.7.7`, ShellCheck `0.9.0` | Chỉ suite bên trong bước 19; không tái chạy wrapper tải/cài công cụ. |
| `python3 .claude/dev/packet_loop.py doctrine-scan` | **7/7 tệp quét**, **0/0 chỗ chép doctrine**, có marker sạch | Không thay bước selftest 13. |
| `python3 .claude/dev/packet_loop.py adr-song` | **46/46 ADR**, **46/46 hàng §20**, khớp; ngoại lệ trạng thái `0016` được nêu riêng | Không thay bước selftest 13. |
| `python3 .claude/dev/packet_loop_test.py` | **278/278 ca nền đạt**, **0/0 bỏ qua**; **81/81 đột biến có dòng kết quả dương**, **78/78 lớp lách**, **35/35 ca bắt oan**, **0/0 ngoại lệ AC18**; `TỔNG: ĐẠT` | Khớp thân `run` bước 13. |
| `python3 scripts/tl.py doc-claims-check --strict --json` | `ok=true`; **106/106 tệp**, **367/367 advisory**, **0/0 cờ cứng** | Khớp thân `run` bước 32. `--json` chỉ chọn đầu ra máy đọc. |
| `shellcheck --format=json ops/dung_goi_review.sh` | JSON là `[]`: **0/0 diagnostic**; binary/version đã kiểm | Kiểm script dựng gói, không thay các bước selftest khác của CI. Định dạng JSON dùng để kiểm bằng chứng dương của kết quả phân tích. |

[Argv, tested SHA, rc, stdout/stderr](phep-do/gates.json); [kết quả dương](phep-do/positive-evidence.json). Các phép chạy này chứng minh kết quả **tái lập ở lượt 7**, không chứng minh executor đã chạy vào thời điểm nào trước khi commit.

**“Tám và ba mươi mốt trả lời hai câu khác nhau, đừng cộng trừ” đúng về đơn vị, nhưng không thay được phép tính độ phủ.** Ánh xạ hiện tại cho **3/3 thân `run` khớp** (13, 14, 32), **1/1 bước chỉ chạy suite bên trong** (19), và **27/27 bước còn lại chưa được tám lệnh này bao phủ**. Trên inventory **31/31 bước kiểm**, độ phủ thân lệnh đầy đủ là **9,68%**; nếu chỉ đếm bước có đích kiểm được chạm tới, kể cả bước 19 một phần, là **12,90%**. Không gọi chỉ số thứ hai là độ phủ trọn bước.

Đây là tỉ lệ trên **inventory các nhánh điều kiện**, không phải tỉ lệ một job CI thực tế. Với giả định PR/Linux, YAML chọn **28/28 bước kiểm**, cho độ phủ thân lệnh tương ứng **10,71%**, còn có chạm đích kiểm là **14,29%**. Môi trường/runner/checkout/CI lịch sử vẫn **KHÔNG ĐO ĐƯỢC**. Bảng JSON cũng giữ các trường hợp Windows/push để không trộn hai nhánh loại trừ nhau thành một lượt chạy.

Danh sách “chưa có bằng chứng” trong R5 là danh sách nhóm, không phải bảng vét cạn từng bước: nó không nêu riêng `py_compile`, EOL ancestry và `don-nhanh_test.ps1`. Tôi giữ cả chúng trong mẫu số; không suy “chưa từng chạy” từ sự vắng mặt. Bản đính chính đã rút lời “đủ bộ” và không tự nhận tỉ lệ đủ giả, nên các điểm phân biệt này không tạo thêm finding về vế đã đóng.

## BẢNG ĐO

| Đối tượng | Kết quả và nguồn tái lập |
|---|---|
| Gói/head/ref | Detached đúng SHA đầu verdict, `shallow=false`, root `394e93468fc8d84ec20938e6df8fb7ab72b2cc37`. **3.234/3.234 hiện vật** khớp manifest. **318/318 cặp tên–OID nhánh** khớp cây và **3/3 TSV**; **0/0 cặp lệch**. Đây là snapshot gói, không xác nhận máy chủ hiện tại. [Manifest](phep-do/manifest.json), [refs](phep-do/refs.json), [graph](phep-do/graph.json). |
| Chênh sau R6 | **2/2 commit**, **8/8 tệp**, **1.858/1.858 dòng thêm**, **9/9 dòng bớt**. Patch và numstat gói khớp Git; BAN/L và verdict R6 gói/kho khớp byte; L không đổi từ `dccce0a`. [Diff](phep-do/diffs.json), [copies](phep-do/copies.json). |
| L, lịch sử sau `9a99dd8` | Đến `efa397e`: **5/5 commit**, **14/14 tệp**, **3.135/3.135 dòng thêm**, **132/132 dòng bớt**. Riêng `08b4c0e`: hồ sơ #480 đổi **105/105 dòng**, #487 đổi **108/108 dòng**, đơn vị thêm+bớt. Không suy lần push hay nguyên nhân dismiss từ Git. [Diff](phep-do/diffs.json). |
| L, phần sau head approve `98ef1f1` | Đến `efa397e`: **2/2 commit**, **8/8 tệp**, **2.189/2.189 dòng thêm**, **4/4 dòng bớt**. Diff `9a99dd8..98ef1f1`: **8/8 tệp**, **950/950 dòng thêm**, **132/132 dòng bớt**. Trừ scalar prompt được thuật `560` cho **390/390 dòng chênh**; không có prompt cũ để chứng thực đầu vào. [Diff](phep-do/diffs.json). |
| L, review #489 | R1 có **11/11 heading**: **1/1 P1**, **4/4 P2**, **6/6 P3**. R2 có **4/4 heading P3**, **0/0 P1**, **0/0 P2**. **11/11 nhãn đối chiếu** phân thành **9/9 vá thật**, **1/1 sinh lỗi**, **1/1 chưa vá**, **0/0 vá hờ**. Runtime `1559.927` và `982.697` giây là lời khai. [Reviews](phep-do/reviews.json). |
| L, trạng thái | **17/17 mapping từng thiếu trạng thái** đã được bổ sung. **10/10 mục tiền kiểm** + **11/11 hậu kiểm** = **21/21 mục ngoài**; **17/17 mapping kết quả ngoài** + **1/1 lồng** = **18/18 mapping kết quả**; **22/22 mapping trạng thái**; **0/0 mapping kết quả thiếu trạng thái**. **10/10 mục cục bộ**, **4/4 mục Git**, **2/2 mục API** giữ nguồn riêng. [Status](phep-do/status.json). |
| L, merge/neo | Merge `c0a5cbe` có **2/2 cha**, `f4d74fe` và `efa397e`. **5/5 receipt đổi**, **5/5 hash blob đúng**, **5/5 neo thuộc lịch sử head/merge**. Base chứa **2/2 neo**, còn **3/3 neo** mới ngoài base. Timestamp object Git quy đổi UTC đúng `2026-09-09T14:51:22Z`; không xác thực `merged_at` API. [Anchors](phep-do/anchors.json), [graph](phep-do/graph.json). |
| L, hậu merge Git | `c0a5cbe` có **1.879/1.879 commit reachable**. Nhánh snapshot `claude/land-480-20260909` có **0/0 commit ngoài mốc đó**. Không coi ref snapshot là remote hiện hành. [Graph](phep-do/graph.json). |
| L, cổng trên `efa397e` và `c0a5cbe` | Cả **2/2 SHA** tái chạy: **94/94 receipt** = **41/41 v2** + **11/11 legacy** + **42/42 nợ**, **0/0 vi phạm**, **0/0 chưa đo**, `TỔNG: ĐẠT`; doctrine **7/7 tệp**, **0/0 chỗ chép**; ADR **46/46 tệp**, **46/46 hàng**; doc-claims `ok=true`, **106/106 tệp**, **367/367 advisory**, **0/0 cờ cứng**. [Gates](phep-do/gates.json), [positive evidence](phep-do/positive-evidence.json). |
| L, lease/ShellCheck | Trên `c0a5cbe`, có công cụ: **121/121 ca đạt**, **0/0 bỏ qua**. Không có actionlint, vẫn có ShellCheck: **120/120 ca đạt**, **1/1 ca đỏ t33**, **121/121 ca chạy**, **0/0 bỏ qua**, `rc=1`. ShellCheck JSON **0/0 diagnostic**. Chứng minh chế độ thiếu công cụ, không chứng thực thứ tự lần chạy lịch sử. [Extra gates](phep-do/extra-gates.json), [môi trường](phep-do/environment.json). |
| L, CI/Windows | **1/1 bước checkout**, **0/0 trường `with.ref`**, **0/0 khai báo `pull_request.types`**. Biểu thức OR kiểm **8/8 tổ hợp**; nhánh rộng **2/2 OS**, nhánh hẹp **1/1 OS**. `not_run` Windows nói bước đọc của hồ sơ. Nhãn/dispatch/runner/thứ tự đầu tiên là **KHÔNG ĐO ĐƯỢC**. [CI](phep-do/ci-audit.json). |
| L, schema/bookkeeping | Đủ **16/16 khóa mẫu**; **5/5 phần tử bookkeeping**; **6/6 hồ sơ ngang hàng** có bookkeeping. Inventory land: base **4/4 tệp**, head #489 **6/6 tệp**, head này **7/7 tệp**. Số tệp không chứng nhận số lần land. [Graph](phep-do/graph.json). |
| L, đầu vào bảng cũ | Tự lấy tập tệp đổi ở `9a99dd8..98ef1f1`, đọc blob `98ef1f1`: **526/526 lá YAML**, **62/62 comment YAML**, **242/242 lá JSON**, **2/2 tệp Markdown**. “Không cắt lá TSV” **KHÔNG ĐO ĐƯỢC**, vì TSV đích không có. [Old inputs](phep-do/old-inputs.json). |
| L, chuỗi/AST/doctrine | **6/6 ID PR** trong chuỗi, **2/2 mục miễn** trong YAML; authority và sự vắng PR kế nhiệm chưa xác thực. Literal `ops/land` ngoài land/reviews khớp **2/2 tệp Markdown**; AST có **17/17 lệnh con**, **2/2 chuỗi mô tả chứa `landed`**. **76/76 tệp docs** tại SHA R1. Hàng ADR-0034 ghi `lease_publish.py ×10`, `packet_loop.py ×11`; đó là số của bảng, không tự biến thành số cổng cưỡng chế. [Code scope](phep-do/code-scope.json), [graph](phep-do/graph.json). |
| L, số không có nguồn gốc | ID review/run/comment, HTTP `403`, thời lượng CI `1411`, `1541`, `23` giây, ước tính `~24`/`~16` phút, hint/hunk và chỉ thị: **KHÔNG ĐO ĐƯỢC** sự kiện được thuật. Đọc được ID/giá trị không xác thực sự kiện. [Ledger đầy đủ](phep-do/land-ledger.json), [inventory số](phep-do/numeric-inventory.json). |
| Hồi quy mà các receipt thuật lại | `c42fc74` thiếu **3/3 hàng** và **3/3 receipt** của verdict đã có; `dccce0a` thiếu **4/4 hàng** và **4/4 receipt**; `b43d784` thêm đủ. Chạy suite sẵn có trên `c42fc74`: **120/120 ca đạt**, **1/1 đỏ t27**, **121/121 ca chạy**, **0/0 bỏ qua**. t27 dừng ở assertion mục lục đầu tiên; số receipt thiếu được đếm riêng. [Inventory](phep-do/regression-static.json), [đối chứng](phep-do/extra-gates.json). |
| Số receipt trong message cũ | Tái chạy `b43d784`: **98/98 bản ghi**, **45/45 v2**; `13ba87d`: **99/99 bản ghi**, **46/46 v2**. Mỗi mốc có **11/11 legacy**, **42/42 nợ**, **0/0 vi phạm**, **0/0 chưa đo**, `TỔNG: ĐẠT`. [Extra gates](phep-do/extra-gates.json). |

**Đối chiếu đầy đủ các biên nhận:** **48/48 trường đo** khớp; **6/6 verdict_path đúng**; **6/6 đường dẫn trả đúng 1/1 commit thêm tệp**; **6/6 blob nguyên byte từ commit ấy tới head**. URL neo đúng SHA lẫn đường dẫn. [Giá trị khai và giá trị đo của từng trường](phep-do/receipts.json).

| Receipt | Byte verdict | P1 · P2 · P3, đơn vị heading | Timestamp được khai → giây tính lại | stdout/stderr byte được khai |
|---|---:|---|---|---|
| R1 | **29.710/29.710 byte** | **0/0 · 1/1 · 3/3** | `1212.700479` → `1212.7` | `269` / `1486780` |
| R2 | **26.633/26.633 byte** | **0/0 · 0/0 · 1/1** | `953.52854` → `953.529` | `275` / `1358140` |
| R3 | **31.388/31.388 byte** | **0/0 · 0/0 · 1/1** | `1128.265837` → `1128.266` | `292` / `1738059` |
| R4 | **56.281/56.281 byte** | **0/0 · 0/0 · 1/1** | `1242.964299` → `1242.964` | `308` / `2052295` |
| R5 | **23.633/23.633 byte** | **0/0 · 0/0 · 0/0** | `895.24447` → `895.244` | `304` / `1439474` |
| R6 | **31.520/31.520 byte** | **0/0 · 0/0 · 1/1** | `1442.025902` → `1442.026` | `182` / `931800` |

**6/6 phép tính thời lượng khớp**, nhưng timestamp, stdout/stderr byte/hash, prompt hash, run ID, rc lịch sử, restart, model, cách sinh bằng script và trạng thái sạch của cây lịch sử đều **KHÔNG ĐO ĐƯỢC độc lập**. Dấu `/` ở cột cuối chỉ ngăn hai scalar stdout/stderr được trích, không phải tỉ lệ đạt. Ref gói cũ được khai lần lượt `314, 315, 316, 317, 317, 317`; không dùng snapshot hiện tại để xác nhận chúng. Inventory hiện vật nhập của R1–R6 lần lượt **3/3, 5/5, 2/2, 5/5, 4/4, 4/4 tệp** tồn tại; các phép `cmp` với gói gốc không được tái chứng thực khi thiếu gói gốc.

R1 đối chiếu **5/5 slug** với **3/3 vá thật**, **1/1 sinh lỗi**, **1/1 vá hờ**; R2 đối chiếu **4/4 slug** với **3/3 vá thật**, **1/1 vá hờ**; R3/R4 mỗi lượt **1/1 nhãn vá hờ**; R5 **1/1 nhãn vá thật**. Các con số diễn giải riêng của R1–R5 về trạng thái, docs, neo và ledger đều đối chiếu các phép đo ở bảng trên, không chỉ chép đoạn tóm tắt.

**Phủ đầu vào kiểm toán:** đã ghi **518/518 dòng có chữ số** của L và R1–R6; **646/646 scalar**, **679/679 khóa**, **93/93 comment YAML** với giá trị/nguyên văn, vị trí và giới hạn nguồn; **0/0 khóa YAML trùng**. Riêng L có **219/219 scalar**, **231/231 khóa**, **27/27 comment**. Giữ **95/95 ID ledger** cũ, gắn nội dung hiện tại và nguồn; C047/C074/C085 được cập nhật cách hiểu theo phần đã sửa, không dùng mô tả cũ kết tội văn hiện tại. Tại `c42fc74` tự đếm lại **214/214 scalar**, **225/225 khóa**, **27/27 comment**; R1–R5 tại `13ba87d` có **330/330 scalar**, **357/357 khóa**. [Inventory](phep-do/numeric-inventory.json), [nguồn từng node](phep-do/node-source-audit.json), [ledger](phep-do/land-ledger.json), [đếm theo SHA](phep-do/historical-receipt-topology.json).

**Mệnh đề sự kiện mới:** danh mục đầy đủ nằm trong [delta-claims.json](phep-do/delta-claims.json), chia **27/27 nhóm ngữ nghĩa**, kèm nguồn và trạng thái cho từng nhóm; [delta-lines.json](phep-do/delta-lines.json) giữ **1.858/1.858 dòng thêm**, **0/0 dòng ngoài ánh xạ**. Các nhóm gồm: caveat/số hàng/phạm vi/runtime của mục lục; lời cũ/danh sách có–chưa có/CI/tám lệnh của R5; neo/kết quả/tóm tắt/runtime/ref/cmp/anchor của R6; toàn bộ bảng định lượng và giới hạn của verdict R6; từng bản ghi JSON receipt, từng step/điều kiện/phân loại JSON CI; script và hai commit message. **35/35 phép đối chiếu nhóm trường của JSON receipt nhập khớp** với đúng nguồn lịch sử; các JSON CI đã đối chiếu trực tiếp YAML như trên. Không phát hiện giá trị đo sai mới trong các bảng ấy.

Các tổng riêng của **gói R6** trong verdict được nhập — manifest, ref, các lần thử PATH, số lần gọi cổng và snapshot cuối — chỉ còn là lời khai reviewer lịch sử khi thiếu manifest/log/snapshot gốc. Bản verdict nhập khớp byte không thay bằng chứng gốc cho các tổng ấy. Bảng audit phân biệt rõ trường hợp này; không lấy số của gói R7 lấp vào.

Liệt kê đủ node/dòng là bảo đảm **cú pháp**; việc tách mệnh đề và gắn nguồn là audit ngữ nghĩa của reviewer. Không tuyên một regex chứng minh mọi câu đúng.

### script-do-luot6-khong-co-duong-tai-lap-trong-kho  [P3]  Hiện vật đo được giới thiệu là chạy lại được nhưng phụ thuộc gói cũ không được cung cấp.

**Vị trí và phản chứng.** Commit `2f783bc` viết về `do-static.py`: “script sinh ra nó — chạy lại được”. R6:85–100 giới thiệu hiện vật khóa phép đo và hướng người đọc chạy lại trước khi nhận đủ cổng. Nhưng `ops/reviews/pr490-review-6-phep-do/do-static.py:6` đặt `P` theo thư mục script rồi lấy `R=P.parent/'cay-kho'`. Với vị trí được lưu trong kho, nó trỏ tới `ops/reviews/cay-kho`, thư mục không tồn tại. Script còn đọc bắt buộc manifest/ref TSV của gói cũ, và dòng 55 đọc `VERDICT-luot5.md` cùng `LEDGER-luot4.json`; chúng không nằm trong bộ hiện vật được nhập. Đổi working directory không sửa được đường dẫn tính từ `__file__`.

Tôi chép **1/1 script nguyên byte** cùng thư mục hiện vật sang scratch ngoài kho, giữ bố cục tương ứng và chạy bằng `python3`. Kết quả **1/1 lần thử bị lỗi**, `rc=1`, stdout rỗng, traceback `FileNotFoundError` tại thư mục `ops/reviews/cay-kho` trước phép đo đầu tiên. Hash bản nguồn/bản chạy cùng là `5414a19d947849af4671543c8f80a4fd7eda198e5e0c01078f8a1d882d7272bf`. [Phản chứng máy đọc được](phep-do/script-replay.json), [stderr](phep-do/logs/imported-script.stderr).

Ngay cả chuyển nguyên script về bố cục `phep-do/` của một gói mới cũng chưa cung cấp các đầu vào lịch sử nêu trên. Ngoài ra, script chỉ xuất `ci-steps.json`; không có đoạn sinh bảng phân loại `ci-comparison.json`. JSON đó kiểm lại được bằng đọc YAML và message như lượt này đã làm, nhưng không phải một phép chạy của script đang được giao.

**Tác động và mức.** Người clone kho không có đường tái chạy đã được giới thiệu để sinh lại chứng cứ. Đây là lỗi phạm vi của lời khai khả năng tái lập trong một PR hồ sơ, xếp P3. Không suy số trong `receipts.json` hoặc kết quả tám cổng là sai: chúng đã được tôi đo độc lập và khớp. Không yêu cầu biến script lịch sử thành một công cụ sản phẩm chỉ để đạt approve.

**Vá ở đâu và thế nào.** Cách nhỏ nhất là đính chính bền trong R6, cạnh `hien_vat_reviewer_vao_kho`: script giữ nguyên của gói lượt 6, **chưa chạy lại trực tiếp từ checkout này**, liệt kê đầu vào/bố cục còn thiếu; sửa hướng dẫn “chạy lại” để phân biệt đọc/đối chiếu bảng JSON với chạy script. Nâng caveat cần thiết lên hàng mục lục theo cơ chế của kho. Không viết lại commit/verdict gốc. Nếu muốn giữ lời khai tái chạy, bổ sung runner riêng nhận `--repo`, `--out`, exact SHA và đầu vào cần thiết, kèm cách xử lý nguồn không có; phần tạo phân loại CI cần được cung cấp nếu vẫn giới thiệu nó như đầu ra được sinh lại.

**Ca khóa bản vá.** Nếu chọn sửa lời khai: đối chiếu receipt → mục lục → đường chạy, bảo đảm không chỗ nào còn nhận script tự đủ đầu vào. Nếu chọn runner: chạy từ bản sao checkout sạch, output ngoài kho, đòi kết quả dương cho các trường đã đo và step object; đầu vào lịch sử thiếu phải báo riêng **KHÔNG ĐO ĐƯỢC**, không âm thầm bỏ qua rồi tuyên đủ. Phản chứng nguyên byte ở trên phải được giải quyết bằng đường chạy có tài liệu, không bằng việc reviewer tự đoán cách dựng lại gói.

**Nguy cơ bản vá.** Đừng sửa `__file__` rồi cho script ghi vào `ops/reviews`; đừng lấy head mới thay exact SHA lịch sử, lấy manifest gói mới chứng thực gói cũ, hoặc gọi so giá trị JSON là so nguyên byte gói nguồn. Giữ riêng trường đo được với runtime/ref/API thiếu nguồn.

## GIỚI HẠN

- **Không mạng.** Mọi GitHub API/CI, approval/dismiss, actor, CAS, nhãn/dispatch, byte comment, quyết định miễn CI, sự vắng PR kế nhiệm và chuỗi đã đóng thật là **KHÔNG ĐO ĐƯỢC**. Git chỉ chứng minh object/nội dung/ref snapshot được cấp. Không duyệt merge/land/deploy.
- Môi trường tái chạy: Linux, Python `3.11.15`, PyYAML `6.0.1`, Git `2.43.0`, actionlint `1.7.7`, ShellCheck `0.9.0`; `core.abbrev=7` trên bản sao. CI khai Python `3.12`/PyYAML `6.0.3`. Không đồng nhất môi trường này với GitHub runner hay Windows. Không tải/cài công cụ qua mạng.
- **22/22 lần gọi cổng** có argv, tested SHA, rc và log: **20/20 lần rc=0**, **2/2 lần rc=1** là các đối chứng có chủ đích cho thiếu công cụ/t27. Phép chạy script nhập là **1/1 lần thử riêng**, `rc=1`, không trộn vào số cổng đạt. Full CI/full release/Windows/API **not_run trong lượt này**. Chỉ chạy phản chứng có sẵn trong cây; không tự soạn nội dung dựng đường dẫn thoát cây.
- `cay-kho/` giữ sạch, head/tree/ref/nội dung không đổi; kiểm cuối và băm trước/sau ở [tree-final.json](phep-do/tree-final.json). Các phép chạy và fixture của suite nằm ngoài kho được review. Hướng dẫn tái lập và giới hạn các script của lượt này ở [README phép đo](phep-do/README.md).
