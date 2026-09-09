verdict: changes_requested
reviewed_sha: 13ba87d8e6054ec4e35a5a6ada1eec66afffb545
luot: 6
so_lan_luot_nay_bi_chet_va_phong_lai: 0

0 finding P1 · 0 finding P2 · 1 finding P3

**Các trường neo biên nhận đều đúng; phần tóm tắt mới vẫn có lời khai vượt nguồn.** Bản vá mục lục/biên nhận sửa được lỗi `t27` trên cây cục bộ. Tuy nhiên, mục lục bỏ giới hạn runtime đã có trong biên nhận, và lời “ĐỦ BỘ” trong commit hiện tại không được danh sách cổng đã khai hỗ trợ. Giữ cùng slug vì đây là cùng lớp lỗi, tái phát ngoài hồ sơ land đã được sửa ở lượt trước.

Reviewer: Codex/OpenAI, GPT-6 theo cấu hình phiên; provider `openai_codex`, execution surface agent API có shell Linux, transport `machine`. Phiên độc lập với executor Claude. Authority/phạm vi là `PROMPT.md`: review offline, chỉ ghi đầu ra ngoài `cay-kho/`. Tree được review: `de63dea60cf89f105078644639b6130e62539b43`. Không có GitHub submitter trong lượt này.

**L** = `cay-kho/ops/land/pr489-land-evidence.yaml`, khớp nguyên byte `BAN-DANG-REVIEW.yaml`. Các phép đếm dùng cặp bằng nhau và đơn vị; tập đạt, đỏ, bỏ qua tách riêng. SHA, số dòng, ID PR/run/lượt, version, timestamp, mã thoát và scalar trích nguyên văn là giá trị kỹ thuật. Runtime lịch sử không trở thành phép đo chỉ vì phép tính từ scalar khớp.

## KIỂM 5 BIÊN NHẬN

R1 = [`pr490-review-1-codex-verdict.receipt.yaml`](cay-kho/ops/reviews/pr490-review-1-codex-verdict.receipt.yaml).  
R2 = [`pr490-review-2-codex-verdict.receipt.yaml`](cay-kho/ops/reviews/pr490-review-2-codex-verdict.receipt.yaml).  
R3 = [`pr490-review-3-codex-verdict.receipt.yaml`](cay-kho/ops/reviews/pr490-review-3-codex-verdict.receipt.yaml).  
R4 = [`pr490-review-4-codex-verdict.receipt.yaml`](cay-kho/ops/reviews/pr490-review-4-codex-verdict.receipt.yaml).  
R5 = [`pr490-review-5-codex-verdict.receipt.yaml`](cay-kho/ops/reviews/pr490-review-5-codex-verdict.receipt.yaml).  

Đọc byte verdict từ cây; đếm tiêu đề bằng regex `^###\s+(\S+)\s+\[(P[123])\]`; đọc SHA/verdict từ header; tìm commit thêm tệp bằng `git log --all --diff-filter=A --format=%H -- <verdict_path>`. Mỗi đường dẫn trả **1/1 commit thêm tệp**; **5/5 blob** tại commit đó vẫn nguyên byte ở head. URL khớp cả SHA và đường dẫn, không gọi HTTP. [Đối chiếu đầy đủ](phep-do/receipts.json), [script](phep-do/do-static.py).

| Tệp | Trường | Khai | Đo được | Khớp? |
|---|---|---|---|---|
| R1 | `verdict_sha256` | `e81e5e3198b6143e27b36e8ea4776e8420a40004982e76a7faba34a24ae73d97` | `e81e5e3198b6143e27b36e8ea4776e8420a40004982e76a7faba34a24ae73d97` | Có |
| R1 | `verdict_bytes` | 29710 byte | **29710/29710 byte** | Có |
| R1 | `reviewed_sha` | `9238606b21344fedae8d9c191834193b4bbee582` | `9238606b21344fedae8d9c191834193b4bbee582` | Có |
| R1 | `verdict` | `changes_requested` | `changes_requested` | Có |
| R1 | `evidence_url` | blob `63c639ac1604f7c6bb8b734a556bdf68891f8046` + verdict_path | Đúng commit thêm đầu tiên và đường dẫn | Có |
| R1 | `so_p1` | 0 | **0/0 tiêu đề P1** | Có |
| R1 | `so_p2` | 1 | **1/1 tiêu đề P2** | Có |
| R1 | `so_p3` | 3 | **3/3 tiêu đề P3** | Có |
| R2 | `verdict_sha256` | `7fe26df83c910738f954326ee8d9dd892fe6823aab6d68c8fcbd37d6fee4fffe` | `7fe26df83c910738f954326ee8d9dd892fe6823aab6d68c8fcbd37d6fee4fffe` | Có |
| R2 | `verdict_bytes` | 26633 byte | **26633/26633 byte** | Có |
| R2 | `reviewed_sha` | `63c639ac1604f7c6bb8b734a556bdf68891f8046` | `63c639ac1604f7c6bb8b734a556bdf68891f8046` | Có |
| R2 | `verdict` | `changes_requested` | `changes_requested` | Có |
| R2 | `evidence_url` | blob `f7872ac6876b0675ae549dfac279ef238b24d58d` + verdict_path | Đúng commit thêm đầu tiên và đường dẫn | Có |
| R2 | `so_p1` | 0 | **0/0 tiêu đề P1** | Có |
| R2 | `so_p2` | 0 | **0/0 tiêu đề P2** | Có |
| R2 | `so_p3` | 1 | **1/1 tiêu đề P3** | Có |
| R3 | `verdict_sha256` | `c198b7364ca3a63d95bcf2ec800cecd01774842f3720710ee7aa3a2f01fd1ad4` | `c198b7364ca3a63d95bcf2ec800cecd01774842f3720710ee7aa3a2f01fd1ad4` | Có |
| R3 | `verdict_bytes` | 31388 byte | **31388/31388 byte** | Có |
| R3 | `reviewed_sha` | `f7872ac6876b0675ae549dfac279ef238b24d58d` | `f7872ac6876b0675ae549dfac279ef238b24d58d` | Có |
| R3 | `verdict` | `changes_requested` | `changes_requested` | Có |
| R3 | `evidence_url` | blob `c42fc74cca04720627836e187f81a71ab44e9b76` + verdict_path | Đúng commit thêm đầu tiên và đường dẫn | Có |
| R3 | `so_p1` | 0 | **0/0 tiêu đề P1** | Có |
| R3 | `so_p2` | 0 | **0/0 tiêu đề P2** | Có |
| R3 | `so_p3` | 1 | **1/1 tiêu đề P3** | Có |
| R4 | `verdict_sha256` | `1538dd59491b6253379067cbca7eb84add6b441e1d688d09da481f6ee6a14fc9` | `1538dd59491b6253379067cbca7eb84add6b441e1d688d09da481f6ee6a14fc9` | Có |
| R4 | `verdict_bytes` | 56281 byte | **56281/56281 byte** | Có |
| R4 | `reviewed_sha` | `c42fc74cca04720627836e187f81a71ab44e9b76` | `c42fc74cca04720627836e187f81a71ab44e9b76` | Có |
| R4 | `verdict` | `changes_requested` | `changes_requested` | Có |
| R4 | `evidence_url` | blob `dccce0a54efdd687c20e128b64de1e355089c261` + verdict_path | Đúng commit thêm đầu tiên và đường dẫn | Có |
| R4 | `so_p1` | 0 | **0/0 tiêu đề P1** | Có |
| R4 | `so_p2` | 0 | **0/0 tiêu đề P2** | Có |
| R4 | `so_p3` | 1 | **1/1 tiêu đề P3** | Có |
| R5 | `verdict_sha256` | `87e285d221a10e2a914050101feff444b172bc507f8d2f51d401e16c276d4852` | `87e285d221a10e2a914050101feff444b172bc507f8d2f51d401e16c276d4852` | Có |
| R5 | `verdict_bytes` | 23633 byte | **23633/23633 byte** | Có |
| R5 | `reviewed_sha` | `dccce0a54efdd687c20e128b64de1e355089c261` | `dccce0a54efdd687c20e128b64de1e355089c261` | Có |
| R5 | `verdict` | `approve` | `approve` | Có |
| R5 | `evidence_url` | blob `16663cac4e81d3be31377faeb6e49899a357dd2a` + verdict_path | Đúng commit thêm đầu tiên và đường dẫn | Có |
| R5 | `so_p1` | 0 | **0/0 tiêu đề P1** | Có |
| R5 | `so_p2` | 0 | **0/0 tiêu đề P2** | Có |
| R5 | `so_p3` | 0 | **0/0 tiêu đề P3** | Có |

Tổng **40/40 trường** khớp; **5/5 verdict_path** trỏ đúng tệp tương ứng. Không có finding về hash, byte, SHA, commit neo hay phân bố severity.

Các scalar runtime dưới đây được **trích nguyên văn lời khai**, không nhận là phép đo runtime độc lập:

| Tệp | Trường | Khai | Đo được | Khớp? |
|---|---|---|---|---|
| R1 | `thoi_luong_giay`; `stdout_byte`; `stderr_byte` | `1212.7` giây; `269` byte; `1486780` byte | Runtime **KHÔNG ĐO ĐƯỢC**. Trừ timestamp được khai rồi làm tròn cho `1212.7` giây | Chỉ khớp số học |
| R2 | `thoi_luong_giay`; `stdout_byte`; `stderr_byte` | `953.529` giây; `275` byte; `1358140` byte | Runtime **KHÔNG ĐO ĐƯỢC**. Trừ timestamp được khai rồi làm tròn cho `953.529` giây | Chỉ khớp số học |
| R3 | `thoi_luong_giay`; `stdout_byte`; `stderr_byte` | `1128.266` giây; `292` byte; `1738059` byte | Runtime **KHÔNG ĐO ĐƯỢC**. Trừ timestamp được khai rồi làm tròn cho `1128.266` giây | Chỉ khớp số học |
| R4 | `thoi_luong_giay`; `stdout_byte`; `stderr_byte` | `1242.964` giây; `308` byte; `2052295` byte | Runtime **KHÔNG ĐO ĐƯỢC**. Trừ timestamp được khai rồi làm tròn cho `1242.964` giây | Chỉ khớp số học |
| R5 | `thoi_luong_giay`; `stdout_byte`; `stderr_byte` | `895.244` giây; `304` byte; `1439474` byte | Runtime **KHÔNG ĐO ĐƯỢC**. Trừ timestamp được khai rồi làm tròn cho `895.244` giây | Chỉ khớp số học |
| R1–R5 | Timestamp, exit/status, stdout/stderr SHA-256, prompt hash, run ID, launcher/model | Giá trị đầy đủ trong `receipts.json`; `ma_thoat: 0`, model chạy `KHONG_DO_DUOC` | **KHÔNG ĐO ĐƯỢC**: không có run/stdout/stderr/prompt gốc của các lượt trong cây/lịch sử đường dẫn đã tìm | Nhãn ATTESTATION đúng chỗ; không xác thực hash của đầu vào vắng mặt |
| R1–R5 | `so_lan_chet_truoc_khi_xong`; `cay_kho_sach`; `commit_them_ngoai_head` | `0`; `true`; `0` | Header/lời khai verdict phù hợp; trạng thái runtime/cây lịch sử **KHÔNG ĐO ĐƯỢC** độc lập | Chỉ khớp lời khai |
| R1–R5 | Ref gói; lệch; độ sâu | Lần lượt `314`, `315`, `316`, `317`, `317` ref; `0`; `false` | Khớp lời thuật của verdict. Manifest/ref snapshot gói cũ không vào kho | **KHÔNG ĐO ĐƯỢC** độc lập; không dùng ref hiện tại bảo lãnh ref lịch sử |
| R1–R5 | Schema/lượt/identity/authority | Schema `2`; lượt theo tên tệp; các identity trong YAML | Parse **5/5 YAML**, **0/0 khóa trùng**. Đọc được giá trị định danh; không xác thực ai cấp lease/identity hoặc actor GitHub | Cấu trúc đúng; authority **KHÔNG ĐO ĐƯỢC** |
| R1–R5 | Hiện vật nhập kho và `cmp` với gói nguồn | Danh sách `hien_vat_reviewer_vao_kho` | Lần lượt **3/3**, **5/5**, **2/2**, **5/5**, **4/4 tệp** liệt kê tồn tại. Không có toàn bộ gói gốc để chạy lại phép so byte lịch sử | Tồn tại: có; phép `cmp` gốc: **KHÔNG ĐO ĐƯỢC** |

**5/5 biên nhận** đặt câu `run.json … KHÔNG vào kho ⇒ ATTESTATION` ngay trong `model_reviewer_identity.nguon_cac_scalar_tren`, và nhắc lại dưới `khong_do_duoc`. Đây là vị trí đúng cho scalar runtime. Phép trừ timestamp khớp **5/5 cặp đầu–cuối**, nhưng cả hai đầu vào vẫn là lời khai. Câu mở đầu “mọi scalar … đọc từ run.json” không chứng minh script đã chạy: thiếu script sinh biên nhận/run gốc để kiểm chứng cách sinh. [Inventory số](phep-do/numeric-inventory.json), [tìm nguồn](phep-do/source-search.json), [topology](phep-do/topology.json).

## KIỂM HÀNG MỤC LỤC MỚI

Đối chiếu **5/5 hàng** tại `ops/reviews/README.md:269–273` với verdict tương ứng, không lấy receipt mới làm chứng cứ duy nhất. [Hàng nguyên văn](phep-do/index-rows.json), [audit mệnh đề mới](phep-do/delta-claims.json).

| Hàng | Nội dung tóm tắt | Đối chiếu |
|---|---|---|
| R1 — dòng 273 | Severity, nhãn, thiếu trạng thái, doctrine | **5/5 slug**: **3/3 vá thật**, **1/1 sinh lỗi**, **1/1 vá hờ**; **17/17 mapping** từng thiếu trạng thái; **76/76 tệp docs** tại SHA review. Tóm tắt khớp verdict; phân biệt PR của Mission với PR kế nhiệm cho hồ sơ. |
| R2 — dòng 272 | Mapping và trạng thái mạnh | **21/21 mục ngoài**, **18/18 mapping kết quả**, **22/22 mapping trạng thái**; **10/10 mục cục bộ**, **4/4 mục Git** có đối chứng tại SHA được dẫn. Khớp kết luận reviewer về tập trạng thái mạnh, không chứng nhận CI/API. |
| R3 — dòng 271 | Neo squash và Windows | **2/2 neo đã có trong base**, **3/3 neo chưa có**, tổng **5/5 neo**. Đúng đối tượng đếm; vế Windows giữ giới hạn không đo được lịch sử. |
| R4 — dòng 270 | Kiểm kê, độ phủ và các chỗ sai | **95/95 hàng**, **214/214 scalar**, **225/225 khóa**, **27/27 comment**, **0/0 phần tử ngoài ánh xạ** tại `c42fc74`; giữ giới hạn cú pháp/ngữ nghĩa. **8/8 tổ hợp boolean**; các chỗ sai được thuật đúng. |
| R5 — dòng 269 | Approve và đóng lớp lỗi trên L | Khớp verdict `dccce0a`, **0/0 tiêu đề finding**; **3/3 vị trí** đánh giá đã sửa; literal **2/2 tệp**, AST **17/17 parser**, **2/2 chuỗi landed** khớp. Giữ cảnh báo approve không phủ head mới. |
| R1–R5 | Runtime và “chạy trọn ngay lần đầu” | Giây làm tròn khớp số học; nhưng chỉ giữ nhãn **“Model/effort là ATTESTATION”**. Giới hạn runtime bị bỏ khỏi **5/5 hàng**. Đây là phần tóm tắt vượt nguồn, xem finding. |

Lời “đã đóng” của R5 được đọc theo SHA/phạm vi L mà hàng đó dẫn; không bác kết luận cũ vì nội dung thêm sau đó có lỗi. `khong_phu_head_hien_tai` giữ đúng ranh giới approve. Câu “head lúc viết là b43d784” là lời khai thời điểm soạn nháp; Git chỉ biết commit cha khi đưa tệp vào kho, nên không dùng quan hệ cha để bịa finding về thời điểm soạn.

## BẢNG ĐO

| Nội dung | Kết quả tái đo và giới hạn |
|---|---|
| Head/cây/snapshot | Detached tại SHA đầu verdict; `shallow=false`; root `394e93468fc8d84ec20938e6df8fb7ab72b2cc37`. **3.224/3.224 hiện vật** khớp manifest gói; **0/0 hash lệch**. `PROMPT.md` không nằm trong manifest này. [Manifest](phep-do/manifest.json) |
| Bản sao/diff sau lượt trước | **3/3 cặp** BAN/L, verdict5, ledger4 khớp nguyên byte. `dccce0a..HEAD`: **11/11 tệp**, **929/929 dòng thêm**, **0/0 dòng bớt**; patch và numstat gói nguyên byte với Git. L không đổi. [Copies](phep-do/copies.json), [diff](phep-do/diffs.json) |
| Ref gói | **317/317 cặp tên–OID nhánh** khớp cây và **3/3 TSV**, sau chuẩn hóa namespace/thứ tự cột; **0/0 cặp lệch**. Snapshot gói, không phải GitHub hiện hành. [Ref](phep-do/refs-normalized.json) |
| L:34–43, `9a99dd8..efa397e` | **5/5 commit**, **14/14 tệp**, **3.135/3.135 dòng thêm**, **132/132 dòng bớt**. `08b4c0e` đổi **105/105 dòng** hồ sơ #480, **108/108 dòng** hồ sơ #487; đơn vị thêm+bớt. Không suy lần push/dismiss hoặc vá hết finding từ numstat. [Diff](phep-do/diffs.json) |
| L:101–113, review #489 | Lượt đầu **11/11 tiêu đề**: **1/1 P1**, **4/4 P2**, **6/6 P3**; lượt sau **4/4 tiêu đề P3**, **0/0 P1**, **0/0 P2**. **11/11 nhãn slug**: **9/9 vá thật**, **1/1 sinh lỗi**, **1/1 chưa vá**, **0/0 vá hờ**. Head/verdict đọc từ tệp tương ứng. [Reviews](phep-do/reviews.json) |
| L:88–97, tập cổng YAML | **17/17 mapping cũ** được thêm trạng thái; **10/10 mục tiền kiểm** + **11/11 hậu kiểm** = **21/21 mục ngoài**. **17/17 mapping kết quả ngoài** + **1/1 lồng** = **18/18 mapping kết quả**, **22/22 mapping trạng thái**, **0/0 mapping kết quả thiếu trạng thái**. [Status](phep-do/status.json) |
| L:129–137, `98ef1f1..efa397e` | **2/2 commit**, **8/8 tệp**, **2.189/2.189 dòng thêm**, **4/4 dòng bớt**; commit verdict thêm **4/4 tệp đo**. Khóa `bon_loi_lich_su_git_dieu_phoi_tu_kiem_lai` có **4/4 phần tử**. So với gói hint vẫn **KHÔNG ĐO ĐƯỢC**. [Diff](phep-do/diffs.json), [chi tiết](phep-do/extra.json) |
| L:54–83, merge/neo | `c0a5cbe` có **2/2 cha**: `f4d74fe`, `efa397e`. **5/5 receipt đổi**; **5/5 hash blob** và **5/5 quan hệ tổ tiên tới head/merge** đúng. Base đã chứa **2/2 neo**, chưa chứa **3/3 neo**. Timestamp object Git: `2026-09-09T14:51:22Z`; không chứng minh payload API `merged_at`. [Graph](phep-do/graph.json), [anchors](phep-do/anchors.json) |
| L:273–290, hậu merge Git | `c0a5cbe` có **1.879/1.879 commit** reachable; nhánh `claude/land-480-20260909` có **0/0 commit** ngoài mốc đó. `efa397e` thuộc lịch sử merge. Ref là snapshot, không phải GitHub hiện tại. [Graph](phep-do/graph.json) |
| L:234–245, 291–302; cổng tại `efa397e`/`c0a5cbe` | Cả **2/2 SHA**: receipt **94/94 bản ghi** = **41/41 v2 đạt** + **11/11 legacy** + **42/42 nợ**, **0/0 vi phạm**, **0/0 chưa đo**, `TỔNG: ĐẠT`; doctrine **7/7 tệp**, **0/0 chỗ chép**; ADR **46/46 tệp**, **46/46 hàng**; doc-claims `ok=true`, **106/106 tệp**, **367/367 advisory**, **0/0 cờ cứng**. Tất cả `rc=0`, có log dương. [Gates](phep-do/gates.json), [positive evidence](phep-do/positive-evidence.json) |
| L:303–320, ShellCheck/lease tại `c0a5cbe` | ShellCheck `0.9.0`: JSON **0/0 diagnostic**, `rc=0`. Có actionlint `1.7.7`: **121/121 ca đạt**, **121/121 ca chạy**, **0/0 ca bỏ qua**. Thiếu actionlint: **120/120 ca đạt**, **1/1 ca đỏ t33**, **121/121 ca chạy**, `rc=1`; không gọi là pass. [Positive evidence](phep-do/positive-evidence.json), [môi trường](phep-do/environment.json) |
| L:251–266, 323–346, Windows/CI | **1/1 bước checkout**, **0/0 trường with.ref**, **0/0 khai báo pull_request.types**. Biểu thức OR giải trên **8/8 tổ hợp**, nhánh rộng **2/2 OS**, nhánh hẹp **1/1 OS**. Không chạy GitHub expression engine; nhãn/dispatch/runner/thứ tự lịch sử **KHÔNG ĐO ĐƯỢC**. Trạng thái Windows hiện nói bước đọc của hồ sơ. [Workflow](phep-do/workflow.json) |
| L:367–386, schema/bookkeeping | Inventory land: base **4/4 tệp**, head #489 **6/6 tệp**, head này **7/7 tệp**. L đủ **16/16 khóa mẫu**, bookkeeping **5/5 phần tử**. **6/6 hồ sơ ngang hàng** có bookkeeping. Không áp enum tên cổng hoặc schema đóng không có trong mẫu. [Extra](phep-do/extra.json), [Graph](phep-do/graph.json) |
| L:394–404, đầu vào bảng cũ | Tại `98ef1f1`: **526/526 lá YAML nguồn**, **62/62 comment YAML**, **242/242 lá JSON**, **2/2 tệp Markdown** ngoài đầu vào YAML. Thiếu TSV gốc: “không cắt lá” **KHÔNG ĐO ĐƯỢC**; L giữ nó như ATTESTATION. [Đếm đúng đầu vào](phep-do/old-inputs.json) |
| L:409–411, diff/prompt cũ | `9a99dd8..98ef1f1`: **8/8 tệp**, **950/950 dòng thêm**, **132/132 dòng bớt**. Trừ scalar prompt được thuật `560` cho **390/390 dòng chênh**. Prompt gốc **KHÔNG ĐO ĐƯỢC**; phép trừ không chứng thực đầu vào. [Diff](phep-do/diffs.json) |
| L:418–456, chuỗi/miễn trừ | Chuỗi văn bản có **6/6 ID PR**, **2/2 mục miễn** trong YAML. Kiểm nội dung không xác thực quyết định chủ kho, PR kế nhiệm vắng mặt hay chuỗi đã đóng thật. [Extra](phep-do/extra.json) |
| L:459–470, literal/AST | **2/2 tệp Markdown** khớp `ops/land` trong tracked files ngoài `ops/land`/`ops/reviews`; **17/17 lệnh con** AST `packet_loop.py`; **2/2 chuỗi mô tả** chứa `landed`. Không suy không có consumer động hoặc mọi cổng xanh. [Code scope](phep-do/code-scope.json) |
| L:5, bảng ADR | **1/1 hàng ADR-0034** chứa `lease_publish.py ×10`, `packet_loop.py ×11`; là giá trị bảng thuật lại, không phải số cổng cưỡng chế hoặc phép đếm literal hiện tại. [Code scope](phep-do/code-scope.json) |
| L:101–102, 205–231, 428–432, 503–506; số thiếu nguồn | Runtime `1559.927`, `982.697`, `1411`, `1541`, `23` giây; ước tính `~24`, `~16` phút; số review/run/comment/HTTP `403`, hint, thời điểm cài công cụ và identity: **KHÔNG ĐO ĐƯỢC** sự kiện được thuật lại. ID/OID đúng dạng/tồn tại không chứng thực API. [Tìm nguồn](phep-do/source-search.json), [ledger](phep-do/claim-audit-current.json) |
| Mới: hồi quy mục lục/receipt | `c42fc74` có **3/3 verdict mồ côi**, thiếu **3/3 hàng**, **3/3 receipt**. Đến `dccce0a` mới có **4/4 verdict mồ côi**, thiếu **4/4 hàng**, **4/4 receipt**; `b43d784` bổ sung đủ. Không gán số ở mốc sau cho CI được thuật ở mốc trước. Có công cụ: trước vá **120/120 ca đạt**, **1/1 ca đỏ t27**, **121/121 ca chạy**; sau vá và head này **121/121 ca đạt**, **0/0 ca bỏ qua**, `rc=0`. `t27` dừng tại assertion mục lục đầu tiên; số receipt thiếu kiểm riêng bằng inventory, không nói stdout đã liệt kê hết lỗi. [Regression](phep-do/regression-static.json), [positive evidence](phep-do/positive-evidence.json) |
| Mới: cổng trong commit | `b43d784`: **98/98 receipt** = **45/45 v2** + **11/11 legacy** + **42/42 nợ**. `13ba87d`: **99/99 receipt** = **46/46 v2** + **11/11 legacy** + **42/42 nợ**. Cả hai **0/0 vi phạm**, **0/0 chưa đo**, `TỔNG: ĐẠT`; doctrine **7/7 tệp**, ADR **46/46 tệp**, doc-claims `ok=true` **106/106 tệp**, ShellCheck **0/0 diagnostic**. Số thành phần đúng không biến tập cổng thành đầy đủ CI. [Gates](phep-do/positive-evidence.json) |

**Mốc ledger và mệnh đề mới.** Giữ **95/95 ID hàng** từ lượt trước, thêm nguồn hiện tại và ánh xạ dòng. Mô tả lịch sử của C047/C074/C085 không được coi là nội dung hiện tại. Trên đúng `c42fc74`: **214/214 scalar**, **225/225 khóa**, **27/27 comment**, **0/0 mục ngoài ánh xạ**. L tại head này có **219/219 scalar**, **231/231 khóa**, **27/27 comment**, không đổi từ `dccce0a`.

Audit phần mới theo **18/18 nhóm mệnh đề** trong [delta-claims](phep-do/delta-claims.json); **330/330 scalar giá trị**, **357/357 khóa** của các receipt có inventory trong [topology](phep-do/topology.json). Đây là kiểm cú pháp cộng audit ngữ nghĩa thủ công, không tuyên thuật toán chứng minh mọi câu đúng. Các khối source-boundaries/workflow nhập từ lượt trước khớp **8/8 phép đối chiếu** với nguồn hiện tại. [Ledger coverage](phep-do/ledger-coverage.json), [imported evidence](phep-do/imported-evidence.json).

**Câu hỏi ngược về CI.** Chẩn đoán `b43d784` đúng ở nghĩa hẹp: `t27` thuộc `lease_publish_test.py`; danh sách cổng tại chỗ trước đó không chứa suite canh lớp lỗi này. Tuy nhiên, CI thật đã đỏ ở đâu và điều phối thật sự chưa chạy cổng nào vẫn **KHÔNG ĐO ĐƯỢC** khi thiếu log lịch sử.

Bảng sau đối chiếu **31/31 bước kiểm/test**, gồm các biến thể có điều kiện, trong `ci.yml`. Cộng **8/8 bước setup** và **1/1 bước upload artifact** thành **40/40 bước workflow**. Số thứ tự là vị trí bước YAML, không phải số ca test. “Không khai” nghĩa là commit message không cung cấp bằng chứng cho bước đó, không có nghĩa chắc chắn chưa từng chạy. [Lệnh/điều kiện đầy đủ](phep-do/ci-comparison.json), [commit message](phep-do/commit-messages.json).

| Bước YAML | Cổng/lệnh CI | b43d784 / 13ba87d khai gì? |
|---|---|---|
| 8 | `cong_cu.py kiem-tra --json` + `cong_cu_test.py` | Không khai |
| 10 | PR head chứa EOL base: `cat-file` + `merge-base --is-ancestor` | Không khai; chỉ PR |
| 11 | `py_compile` các module đã liệt kê | Không khai |
| 12 | `codex_cred_test.py` | Không khai |
| 13 | `packet_loop_test.py` | Chỉ khai `doctrine-scan`/`adr-song`; không tương đương selftest |
| 14 | `bien_nhan_v2_test.py` | Chỉ khai validator `bien_nhan_v2`; không tương đương selftest |
| 15 | `ci_dang_ky_test.py --chay` | Không khai; còn gọi các suite trong MOI |
| 16 | `idiom_py_test.py` | Không khai |
| 17 | `eol_policy_test.py` | Không khai |
| 18 | `pre_push_test.py` | Không khai |
| 19 | `chay_lease_publish_test.sh`: cài actionlint rồi lease suite | Có khai suite; không có log chứng thực đường wrapper/setup lịch sử |
| 20 | `don-nhanh_test.ps1` | Không khai; khác Windows |
| 21 | Kiểm cấp cgroup + `gate_lifecycle_test.py` | Không khai; Linux |
| 22 | `gate_lifecycle_test.py` không cgroup | Không khai; khác Linux |
| 23 | `eol_policy.py --all --json` | Không khai |
| 24 | `bundle_fragment_check.py --json` | Không khai |
| 25 | `gen_instructions.py --selftest` | Không khai |
| 26 | `command_registry_test.py` | Không khai |
| 27 | `tl.py --selftest` | Không khai; PR |
| 28 | `gate_lifecycle.py run … -- tl.py --selftest`, evidence exact identity | Không khai; không phải PR |
| 30 | `workflow-audit --strict --json` | Không khai |
| 31 | `golden-test --json` | Không khai |
| 32 | `doc-claims-check --strict --json` | Có khai cổng tương ứng |
| 33 | `determinism-audit --strict --json` | Không khai |
| 34 | `ci_phamvi.py --kiem-bam` | Không khai |
| 35 | `ci_phamvi_test.py` | Không khai; khác Windows |
| 36 | `release-check --full --json` | Không khai |
| 37 | `release-verify` manifest committed | Không khai; ref master |
| 38 | Sinh/verify manifest tạm + kiểm mọi tệp được Git theo dõi | Không khai; ref khác master |
| 39 | Build bundle, so SHA-256 của **2/2 lần build** | Không khai |
| 40 | `tl_boot.py --version` | Không khai |

MOI còn có **8/8 suite**: `chon_reviewer_test`, `gh_readback_test`, `mcp_gh_test`, `mcp_github_doc_test`, `probe_mang_test`, `pretooluse_guard_test`, `subagent_ghi_detect_test`, `nhanh_don_duoc_test`. [Tập tên nguyên đường dẫn](phep-do/ci-registry-indirect.json). Không lấy số bước top-level làm số suite/ca chạy thực tế.

Danh sách commit sau vá có **6/6 tên cổng**: lease suite, validator receipt, doctrine-scan, adr-song, doc-claims, ShellCheck. Nó chỉ nêu trực tiếp **2/2 mục tương ứng** với bước lease/doc-claims trong bảng CI; các tên còn lại không thay toàn bộ selftest tương ứng. Lời **“Cổng tại chỗ, ĐỦ BỘ”** tại `13ba87d` cần đính chính phạm vi. Không buộc chạy full CI chỉ để chữa câu chữ; phải khai đúng tập đã đo và phần chưa có bằng chứng.

### van-xuoi-do-duoc-van-vuot-nguon  [P3]  Bản tóm tắt mới lại bỏ giới hạn runtime và nhận tập cổng con là đủ bộ.

**Vị trí và phản chứng.** `ops/reviews/README.md:269–273` đưa thời lượng và “chạy trọn ngay lần đầu” vào các hàng mới, nhưng chỉ giữ câu “Model/effort là ATTESTATION”. Receipt tương ứng, trường `model_reviewer_identity.nguon_cac_scalar_tren` và `khong_do_duoc`, nói rõ runtime đến từ `run.json` ngoài kho. Thiếu log gốc để xác thực thời lượng, stdout/stderr hoặc lịch sử attempt. Tóm tắt làm mất giới hạn nguồn ngay tại chỗ người đọc dùng mục lục. **5/5 giá trị giây làm tròn** đúng số học không giải quyết lỗi này.

Cùng hình dạng ở commit `13ba87d`: sau bài học “chạy bộ cổng của CI” trong `b43d784`, nó khai **“Cổng tại chỗ, ĐỦ BỘ”** rồi liệt kê tập cổng hẹp. Bảng CI trên chỉ rõ các đường kiểm chưa được khai, kể cả full selftest, registry, workflow/golden/determinism và release. `bien_nhan_v2.py` xanh không chứng minh `bien_nhan_v2_test.py` đã chạy; `doctrine-scan`/`adr-song` không thay `packet_loop_test.py`. Đây là lỗi phạm vi báo cáo; không kết luận các cổng vắng mặt chắc chắn chưa chạy hoặc sẽ đỏ.

**Tác động/mức.** Phần mới khiến người đọc đánh giá chứng cứ mạnh hơn nguồn, cùng lớp lỗi các lượt trước. Xếp P3 vì trường neo/hash/severity đúng, bản vá t27 hoạt động và chưa có chứng cứ lỗi runtime sản phẩm hoặc quyền land bị cấp bởi những câu này. Lỗi được xác định là độ chính xác của hồ sơ review, không phải một lỗi kỹ thuật nặng hơn bị hạ mức để đạt approve.

**Vá ở đâu và thế nào.** Sửa ngay **5/5 hàng mục lục** để nêu thời lượng/số lần chạy là attestation của điều phối từ run gốc không lưu trong kho; giữ riêng số Git/hash/byte/heading đã tái lập được. Không sửa verdict gốc. Đính chính commit “ĐỦ BỘ” bằng caveat bền trong receipt R5, đồng thời nâng cảnh báo lên mục lục theo cơ chế hiện có; ghi danh sách cổng thật sự có evidence và phần chưa có evidence. Comment CI đầu receipt R1–R4 cũng nên gắn rõ ATTESTATION cho sự kiện CI, tách khỏi kết quả tái lập cục bộ. Không viết lại lịch sử commit.

**Ca khóa bản vá.** Đối chiếu nguồn → receipt → mục lục: mỗi scalar runtime đưa ra mục lục phải giữ cùng giới hạn nguồn; bỏ giới hạn chỉ ở hàng mục lục phải làm phép đối chiếu không đạt. Với “đủ cổng”, so tập **lệnh + điều kiện** của CI với tập có evidence exact SHA, không so từ khóa gần giống; bỏ mục selftest nhưng vẫn nhận validator là selftest phải bị phát hiện. `t27` hiện canh tên/liên kết/caveat ID, nên suite có sẵn xanh không chứng minh prose đúng. Không cần thêm validator ngữ nghĩa vào PR hồ sơ này; bảng audit và caveat rõ phạm vi là cách vá nhỏ nhất, cổng tự động tổng quát là việc riêng.

**Nguy cơ bản vá.** Đừng đổi “chưa có bằng chứng đã chạy” thành “đã không chạy”; đừng hạ hash/byte/ancestry đo được thành attestation chung; đừng gọi timestamp tự khai là log runtime; đừng bỏ cổng chưa có evidence khỏi tập CI để tạo số đủ giả. Gắn nhãn runtime ở receipt nhưng tiếp tục bỏ nhãn ở mục lục vẫn chưa đóng lỗi.

## GIỚI HẠN

- **Không mạng:** mọi khẳng định GitHub API/CI, approval/dismiss, actor, CAS, label/dispatch, byte comment, quyết định miễn CI và chuỗi đã đóng thật là **KHÔNG ĐO ĐƯỢC**. Git chỉ chứng minh object, nội dung và snapshot ref đã cấp.
- Tái chạy trên clone Linux, Python `3.11.15`, PyYAML `6.0.1`, Git `2.43.0`, actionlint `1.7.7`, ShellCheck `0.9.0`. CI khai Python `3.12`, PyYAML `6.0.3`; đây không phải tái dựng môi trường CI hoặc lượt Windows. Không tải/cài công cụ qua mạng. [Môi trường](phep-do/environment.json).
- Các lần lease đầu có PATH trỏ nhầm thư mục công cụ của giàn đo nên thiếu actionlint. Đã giữ nguyên log, phân loại riêng, chạy lại với binary được cấp. Không quy lỗi `t33` đó cho PR. Mốc trước vá có thêm lỗi `t27`; từng tập đỏ/đạt được đối chiếu tên ca. [Positive evidence](phep-do/positive-evidence.json).
- Tổng **27/27 lần gọi cổng** có log, rc và bằng chứng dương đúng kỳ vọng: **22/22 lần rc=0**, **5/5 lần rc=1** ở đối chứng lỗi mục lục/thiếu công cụ. **Không** gọi các lượt đỏ là cổng đạt. Full CI/full release gate, Windows, API, merge, deploy: **not_run trong lượt review này**. Chỉ chạy các bộ có sẵn, không tự soạn nội dung dựng đường dẫn thoát cây.
- Nợ cross-review exact head #489, TSV gốc/hint và các nợ hồ sơ đã khai vẫn còn. Kết luận này không hồi tố một review cho `efa397e` hoặc cấp quyền land. Phép tái chạy không chứng minh thời điểm chạy trước merge.
- Cây được review giữ sạch: **1.886/1.886 tệp tracked** giữ hash, **697/697 ref cục bộ** giữ nguyên; **0/0 tệp thay đổi**, **0/0 ref thay đổi**; head/tree không đổi. [Kiểm cuối](phep-do/tree-after.json).

Tái lập và giới hạn các script ở [README phép đo](phep-do/README.md). JSON giữ số/kiểu nguyên gốc cho máy đọc. Các nguồn thiếu không được lấp bằng lời khai chép lại từ verdict/receipt.
