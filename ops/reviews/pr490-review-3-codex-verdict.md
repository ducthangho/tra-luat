verdict: changes_requested
reviewed_sha: f7872ac6876b0675ae549dfac279ef238b24d58d
luot: 3
so_lan_luot_nay_bi_chet_va_phong_lai: 0

0 finding P1 · 0 finding P2 · 1 finding P3

Finding lượt trước vẫn **VÁ HỜ**: phép so gói gợi ý đã được giới hạn đúng, nhưng câu Windows vẫn trộn cấu hình với lịch sử sự kiện không có nguồn. Quét toàn tệp còn tìm thấy lời suy ra sai rằng squash PR #489 sẽ phá cả các neo vốn đã nằm trong base. Giữ chung slug của lớp lỗi văn xuôi vượt nguồn, không tách mỗi câu thành finding riêng.

Reviewer: Codex/OpenAI, GPT-6 theo cấu hình phiên; execution surface: agent API có shell cục bộ; transport: `machine`; phiên độc lập với executor Claude. Authority/phạm vi là `PROMPT.md`: review offline, chỉ đọc `cay-kho/`, ghi verdict và hiện vật đo ngoài cây. Tree: `68b98d1174918994be8646d721d5dadff23f1176`. Không phải phiên land.

**L** là `cay-kho/ops/land/pr489-land-evidence.yaml`, nguyên byte với `BAN-DANG-REVIEW.yaml`. Đã ghi verdict ngay khi xác định vế Windows còn lỗi, rồi hoàn thiện bảng đo trong cùng lượt. Mọi cặp `N/N` dưới đây đếm một tập có đơn vị; tập đạt, đỏ và bỏ qua được tách riêng. SHA, PR/ADR/run/review ID, số dòng, schema/generation, mã thoát, phiên bản và timestamp là định danh/giá trị kỹ thuật; thời lượng là đại lượng liên tục, không phải số ca.

## ĐỐI CHIẾU LƯỢT 2

| slug | nhãn duy nhất | đối chứng chạy được |
|---|---|---|
| `van-xuoi-do-duoc-van-vuot-nguon` | **VÁ HỜ** | Vế gợi ý tại L:116–136: `git diff --numstat 98ef1f1..efa397e` xác nhận **8/8 tệp**, **2.189/2.189 dòng thêm**, **4/4 dòng bớt**. Phép so với `GOI-VA.md`/`cay/` đã sang `_ATTESTATION`, nói rõ thiếu đầu vào. Vế Windows tại L:303–314: parse workflow xác nhận ma trận, nhưng không cung cấp nhãn của PR, lịch sử dispatch hay lần đầu lên lịch. Các tiền đề ấy vẫn nằm ngay sau “ĐO ĐƯỢC”. [diffs](phep-do/diffs.json), [source boundaries](phep-do/source-boundaries.json), [coverage](phep-do/coverage.json). |

**Câu hỏi ngược — tách khóa có làm mất gì không?** Không mất số diff Git hoặc thông tin chính của lời khai gợi ý. `_do_duoc` có đủ cặp commit và lệnh, tái lập đúng. Nội dung so sánh vẫn còn trong `_ATTESTATION`; mức khẳng định đổi đúng theo nguồn. Đổi tên `ba_loi` thành `bon_loi` trong bản áp cũng đọc được, với **4/4 phần tử**; điều đó không xác nhận bản gợi ý trùng bản áp. `phan_them_la_gi` giữ mô tả xuất xứ và được mục kế bên giới hạn là lời khai. Không có khóa `_do_duoc` mới thiếu đầu vào Git.

**Câu Windows có hạ quá tay không?** Không. L:306–307 vẫn giữ phần cấu hình đo được: PR thông thường chọn **1/1 hệ điều hành** (`ubuntu-latest`); `push` trên master chọn **2/2 hệ điều hành** (`ubuntu-latest`, `windows-latest`). Cấu hình còn cho phép Windows qua `workflow_dispatch` hoặc nhãn `windows`. Phần chưa sửa là chuyển “lần đo đầu tiên” thành “lần đầu tiên lên lịch” nhưng vẫn cần lịch sử event/label để biết thứ tự. Điều kiện “không ai dispatch” không nằm trong `ci.yml`. Câu “không phải không biết” cũng không có bằng chứng bảo đảm một phiên nào sẽ đọc kết quả sau đó.

**Các sửa phụ và schema.** Phép duyệt đệ quy đúng khóa `ket_qua`/`ket_qua_tho` tái hiện **17/17 mapping thiếu trạng thái** tại `9238606`; hiện còn **0/0 mapping thiếu**. Đủ **17/17 mapping cũ** được bổ sung. Hiện có **21/21 mục cổng cấp ngoài** = **10/10 tiền kiểm** + **11/11 hậu kiểm**; **17/17 mapping cấp ngoài có kết quả**, thêm **1/1 mapping kết quả lồng** thành **18/18 mapping kết quả có trạng thái**; kể cả mục chỉ mang lý do/bỏ qua thì **22/22 mapping có trạng thái**. Câu L:76–80 nay gọi đúng tập đếm. Comment L:177–183 liệt kê **5/5 giá trị kết quả**, kèm **2/2 trạng thái** `not_run`/`skipped`, đúng cách chia nhóm đã công bố. Con trỏ bookkeeping resolve **1/1 lần** tới `KHONG_THOA`. Không tạo trạng thái mạnh thay cho CI hoặc review exact head chưa có. [schema](phep-do/schema.json), [status audit](phep-do/status-audit.json).

L đủ **16/16 khóa mẫu** của `docs/PROTOCOL_DA_PHIEN.md:466–488`; các trường pre/post/bookkeeping đều là list, bookkeeping có **5/5 phần tử**. Toàn bộ **7/7 YAML** parse được, **0/0 khóa trùng**. Đối chiếu các hồ sơ khác:

| hồ sơ trong `ops/land/` | khóa mẫu | bookkeeping |
|---|---|---|
| `plat-x8-land-evidence.yaml` | Đủ **16/16 khóa** | **3/3 phần tử** |
| `pr468-hoso-4-packet-land-evidence.yaml` | Đủ **16/16 khóa** | **5/5 phần tử** |
| `pr477-dung-goi-review-land-evidence.yaml` | Có **15/15 khóa**; thiếu **1/1 khóa**: `session_id` | **4/4 phần tử** |
| `pr478-land-evidence.yaml` | Đủ **16/16 khóa** | **6/6 phần tử** |
| `pr480-land-evidence.yaml` | Đủ **16/16 khóa** | **8/8 phần tử** |
| `pr487-land-evidence.yaml` | Đủ **16/16 khóa** | **7/7 phần tử** |

**Xác nhận lượt trước ghi đúng việc thiếu `session_id` ở hồ sơ #477.** Đây là thiếu sót có sẵn ở tệp khác, không phải finding mới của bản sửa này. Mẫu protocol không định nghĩa enum `trang_thai`, không bắt danh sách lịch sử review phải mang trạng thái cổng. Đủ schema không có nghĩa đã thỏa authority/evidence hoặc được land.

**Quét toàn tệp — danh mục mệnh đề tự nhận đo được.** Đã trích và đọc **208/208 lá scalar YAML**, kể cả các khối không thay đổi, cùng **27/27 dòng comment YAML**. Bảng dưới liệt kê phần nhận là phép đo, trạng thái mạnh, và các suy luận được gắn vào chúng; các mệnh đề lặp được dẫn chung vị trí. Câu phủ định “KHÔNG ĐO ĐƯỢC”, lời đính chính trích câu cũ rồi bác, và dự kiến tương lai không bị đếm nhầm thành kết quả đạt. Toàn bộ giá trị/đường khóa/dòng và phân loại theo phạm vi nằm trong [claim-audit.json](phep-do/claim-audit.json); đây là audit ngữ nghĩa của reviewer, không phải validator ngữ nghĩa tự động.

| vị trí · mệnh đề | nguồn tái lập trong kho | kết luận về ranh giới nguồn |
|---|---|---|
| L:4–7, §20 ghi số lần “có nhắc” | Hàng ADR-0034 tại protocol:1136 | ĐO ĐƯỢC nội dung bảng; không phải số cổng cưỡng chế đang hoạt động |
| L:34,41–43, commit/diff/phân bố finding và dòng đổi | Git và tiêu đề verdict PR #489 lượt đầu | ĐO ĐƯỢC số; sự kiện dismiss, comment và khẳng định đã sửa đúng toàn bộ finding là đối tượng khác |
| L:53–56, Git object và các cha merge | Object `c0a5cbe` | ĐO ĐƯỢC; không xác minh ai bấm hoặc CAS |
| L:63–64, số receipt đổi và loại neo | Diff receipt, YAML tại `efa397e` | ĐO ĐƯỢC, khớp |
| L:65, “Squash sẽ làm cả năm neo hỏng” | Ancestry từng commit neo so với `f4d74fe` | **Suy luận SAI**: neo PR #487 lượt đầu và lượt sau đã có trong base; xem finding |
| L:70–103, số lượt, mapping, slug và finding | YAML và verdict/receipt trong kho | ĐO ĐƯỢC nội dung; runtime/identity lịch sử KHÔNG ĐO ĐƯỢC |
| L:114–121, phần thêm sau approve, `_do_duoc` | Diff/commit tại cặp SHA được khai | ĐO ĐƯỢC Git; xuất xứ hint vẫn chỉ là attestation |
| L:143–169, SHA khác nhau, nợ chưa thỏa, OID không tự đổi | Git, verdict hiện có và protocol | ĐO ĐƯỢC trong snapshot; không loại trừ hiện vật bên ngoài gói |
| L:159–160, có các cổng cục bộ trên `efa397e` | Chạy lại mã tại SHA đó | ĐO ĐƯỢC khả năng tái lập; “đã chạy trước khi xin duyệt” chỉ là thời điểm thuật lại |
| L:198–200,451, checkout dự kiến | Workflow có checkout và không `with.ref` | ĐO ĐƯỢC cấu hình; runner thật KHÔNG ĐO ĐƯỢC |
| L:218–229, tiền kiểm receipt/doctrine/ADR/doc-claims | Chạy lại các lệnh sẵn có tại `efa397e` | ĐO ĐƯỢC cục bộ, có bằng chứng dương |
| L:239–240, PR trigger không khai `types` | YAML workflow | ĐO ĐƯỢC phần khai báo; hành vi trigger GitHub/lịch sử nhãn không đo trực tiếp |
| L:244–263, độ sâu/lịch sử/ancestry/cha/nhánh dư | Git của snapshot | ĐO ĐƯỢC; ánh xạ namespace ref của gói được khai rõ bên dưới |
| L:264–292, hậu kiểm receipt/doctrine/ADR/doc-claims/ShellCheck/lease | Tái chạy tại `c0a5cbe`, với và không có actionlint | ĐO ĐƯỢC; không chứng nhận thời điểm chạy/cài công cụ cũ |
| L:298–307, push master và ma trận hệ điều hành | Trigger/matrix trong `ci.yml` | ĐO ĐƯỢC cấu hình |
| L:307–308, PR này không nhãn Windows, không ai dispatch | Không có event/label/run history thô | **KHÔNG ĐO ĐƯỢC**, đang bị gộp vào phần tự nhận ĐO ĐƯỢC |
| L:311–314, lần đầu lên lịch Windows, sẽ biết muộn hơn | Cấu hình không chứa thứ tự sự kiện hoặc việc đọc kết quả | **KHÔNG ĐO ĐƯỢC**, không được bảo lãnh bằng tiền tố “THEO CẤU HÌNH” |
| L:322–343, bookkeeping: inventory, Git merged và cổng tại chỗ | Git/schema/các lần tái chạy | ĐO ĐƯỢC phần đó; `landed` vẫn không được tuyên |
| L:360–361, số lá nguồn/comment/Markdown | Parse lại các nguồn được dẫn | ĐO ĐƯỢC số nguồn; **“0 lá cắt”, giữ nguyên bảng là KHÔNG ĐO ĐƯỢC** vì thiếu TSV gốc; `tables.json` chỉ thuật kết quả cũ |
| L:367–368, diff cũ và độ thiếu dòng | Git; phép trừ dùng scalar prompt được thuật lại | ĐO ĐƯỢC Git/phép tính; prompt lịch sử tự nó không có trong kho |
| L:375–385, số ID chuỗi, không có luật bắt PR kế nhiệm evidence | Chuỗi YAML, lịch sử Git, protocol/ADR và audit docs | ĐO ĐƯỢC nội dung/đồ thị trong phạm vi kho; quyết định dừng và PR vắng mặt trên GitHub không đo |
| L:398–401, hệ quả “sẽ đo được về sau” | Hiện chưa có merge #490 trong snapshot | Đúng là DỰ KIẾN, không phải phép đo hiện tại; sự vắng mặt PR trên máy chủ vẫn cần nguồn ngoài Git |
| L:414–415, mã kiểm duyệt đúng head/danh tính/thẩm quyền | Bộ phản chứng sẵn có | ĐO ĐƯỢC mã cục bộ; không chứng nhận check hay approval thật trên GitHub |
| L:418–420, tìm đường land, lệnh con và literal `landed` | `rg` kể cả tệp ẩn; AST `packet_loop.py` | ĐO ĐƯỢC tập tìm kiếm. Câu bao trùm “KHÔNG cổng nào đỏ” **không được xác minh cho CI/cổng bên ngoài phạm vi đó** |
| L:425–437, bookkeeping vẫn cần, không có yêu cầu PR kế nhiệm | Protocol và ADR-0034 | Có nguồn doctrine; không tự tạo yêu cầu miễn trừ hoặc ADR mới |

Những phần đã nói rõ không đo được tiếp tục được giữ đúng loại: so bản gợi ý, chi phí ước tính, chỉ thị của chủ kho, API/CI, model, comment byte và readback. Không dùng nội dung tự thuật để tự chứng thực chính sự kiện ấy. Các giới hạn TSV, dự kiến tương lai và cổng ngoài kho được liệt kê để không lọt vào tập đã xác minh; không biến mỗi giới hạn thành một finding riêng.

## BẢNG ĐO

Có thể tái chạy từ gốc gói bằng `python3 -B phep-do/do-static.py`, `python3 -B phep-do/do-more.py`, `python3 -B phep-do/do-gates.py`, rồi `python3 -B phep-do/do-final.py`. Script cổng dùng clone cục bộ dưới `phep-do/rigs/`, `GIT_ALLOW_PROTOCOL=file`, `core.abbrev=7`, không ghi cây review. Lệnh, mã thoát thật và stdout/stderr: [static commands](phep-do/static-commands.json), [more commands](phep-do/more-commands.json), [gate commands](phep-do/gate-commands.json), [gate summary](phep-do/gate-summary.json). Môi trường: Python 3.11.15, Git 2.43.0, actionlint 1.7.7 của gói, ShellCheck 0.9.0; [environment](phep-do/environment.json).

| khẳng định · nguồn | hồ sơ khai | tôi đo được | ĐO ĐƯỢC hay KHÔNG | khớp? |
|---|---|---|---|---|
| Head/tree/độ sâu/sạch | Exact SHA, detached, không nông | SHA/tree nêu trên; branch rỗng; `shallow=false`; **0/0 byte porcelain**, **0/0 ref replace** | ĐO ĐƯỢC | Có |
| Toàn vẹn gói | Manifest; BAN và verdict lượt trước là bản trong kho | **3.201/3.201 hiện vật** khớp SHA-256; **1/1 cặp BAN/L**, **1/1 cặp verdict cũ/bản trong kho** nguyên byte | ĐO ĐƯỢC | Có; không xác thực người tạo |
| Ref | **316/316 ref nhánh** | Cây, mirror và **3/3 TSV** cùng **316/316 cặp tên–OID**, **0/0 cặp lệch** | Snapshot ĐO ĐƯỢC; máy chủ KHÔNG ĐO ĐƯỢC | Có sau chuẩn hóa namespace/thứ tự cột |
| Diff sau lượt trước | **7/7 tệp**, **2.206/2.206 dòng thêm**, **8/8 dòng bớt** | Git khớp; patch và numstat gói nguyên byte với Git | ĐO ĐƯỢC | Có |
| Toàn PR #490 so `c0a5cbe` | Kiểm phạm vi thực | **11/11 tệp thêm**, **3.366/3.366 dòng thêm**, **0/0 dòng bớt** | ĐO ĐƯỢC | Phạm vi hiện tại, gồm evidence các lượt |
| L:34–43, sau `9a99dd8` | **5/5 commit**, **14/14 tệp**, **3.135/3.135 dòng thêm**, **132/132 dòng bớt** | Đúng tập `08b4c0e`, `45bd80e`, `98ef1f1`, `f7fe802`, `efa397e` và numstat | ĐO ĐƯỢC | Có; không xác thực tự dismiss |
| L:42–43, `08b4c0e` | L480 **105/105 dòng đổi**; L487 **108/108 dòng đổi** | L480 **57/57 dòng thêm**, **48/48 dòng bớt**; L487 **62/62 dòng thêm**, **46/46 dòng bớt** | ĐO ĐƯỢC | Có; “đổi” là thêm+bớt |
| L:42,85–86, finding PR #489 | Lượt đầu **1/1 P1**, **4/4 P2**, **6/6 P3**; lượt sau **0/0 P1**, **0/0 P2**, **4/4 P3** | Regex tiêu đề: **11/11 finding** lượt đầu; **4/4 finding** lượt sau; đúng phân bố | ĐO ĐƯỢC nội dung | Có |
| L:70,84–97, lượt/kết luận/đối chiếu | **2/2 lượt**, lượt sau approve; **11/11 slug** = **9/9 vá thật**, **0/0 vá hờ**, **1/1 sinh lỗi**, **1/1 chưa vá** | Nội dung verdict đúng SHA và kết luận, regex dòng slug đúng tập/phân bố | ĐO ĐƯỢC hiện vật | Có; runtime không được chứng thực |
| L:76–80, tập trạng thái | **17/17 mapping từng thiếu**, **21/21 mục ngoài**, **18/18 mapping kết quả**, **22/22 mapping có trạng thái** | Duyệt đệ quy bản cũ và head khớp toàn bộ tập; **0/0 mapping kết quả còn thiếu** | ĐO ĐƯỢC | Có |
| L:85–86, thời lượng review | 1559,927 giây; 982,697 giây | Receipt chứa đúng scalar; **0/0 runtime log gốc PR #489** trong inventory được cấp | KHÔNG ĐO ĐƯỢC sự kiện | Chỉ khớp lời khai |
| L:114–121, chênh sau machine approve | **2/2 commit**, verdict + **4/4 tệp đo**; **8/8 tệp**, **2.189/2.189 dòng thêm**, **4/4 dòng bớt** | Git khớp tập commit/tệp và số; `_do_duoc` tái lập được | ĐO ĐƯỢC | Có |
| L:124–126, so hint/bản áp | Mỗi phía **2/2 tệp**; **1/1 hunk khác**, **0/0 dòng lệch** ở phần đổi tên | Không có đầu vào hint ở head hoặc lịch sử tên đường được tìm. Đo riêng bản áp có **4/4 phần tử** trong khóa `bon_loi...` | Phép so KHÔNG ĐO ĐƯỢC | Đã gắn đúng ATTESTATION |
| L:55–65, cha/receipt/neo | **2/2 cha**, **5/5 receipt đổi**, **5/5 neo canonical_ancestry** | Đúng cha; **5/5 receipt** khớp byte/hash/blob verdict và ancestry tới head/merge thật | ĐO ĐƯỢC | Có về số/neo hiện hữu |
| L:65, ảnh hưởng squash PR #489 | **5/5 neo** sẽ hỏng | **2/2 neo đã có trong base**, **3/3 neo chưa có trong base**. Squash lên base không xóa tổ tiên sẵn có | ĐO ĐƯỢC quan hệ Git; hệ quả suy từ đồ thị | **Không; “cả năm” sai** |
| L:22–61, approval/operator/merge/CAS | ID, actor/state, expected head, merge lúc `2026-09-09T14:51:22Z` | Committer time Git đổi UTC khớp; Git object và cha có thật. Không có API thô cho APPROVED/DISMISSED/quyền/merged_by/CAS/comment | Git ĐO ĐƯỢC; API KHÔNG ĐO ĐƯỢC | Chỉ xác thực Git |
| L:140–169, review head merge | `KHONG_THOA`, nợ chưa trả | **1/1 phép so SHA** cho khác nhau; **2/2 commit** sau review. `efa397e` và `c0a5cbe` cùng tree `f9897f6dba19484900776d7af7e9b042070d4ce1` | ĐO ĐƯỢC gói | Trạng thái phù hợp |
| L:189–202, CI PR | Success; 1411 giây; lượt trước 1541 giây | **1/1 bước checkout**, không `with.ref`; thiếu run JSON/checkout log | Cấu hình ĐO ĐƯỢC; CI KHÔNG ĐO ĐƯỢC | Giới hạn exact-head đúng |
| L:203–217, cổng duyệt/phản chứng/mo | Run IDs/success; **2/2 review** được kể trong log; 23 giây; skipped | Không có API/log gốc. Tái chạy phản chứng cục bộ: **40/40 ca nền**, **46/46 đột biến** giết đúng tập đích | Mã ĐO ĐƯỢC; CI KHÔNG ĐO ĐƯỢC | Không nâng sự kiện API thành phép đo |
| L:218–220,264–266,333–334, receipt gate | **94/94 bản ghi** = **41/41 ĐẠT v2** + **11/11 legacy** + **42/42 nợ**; **0/0 vi phạm**, **0/0 chưa đo** | Cả `efa397e` và `c0a5cbe` khớp, `TỔNG: ĐẠT`, `rc=0` | ĐO ĐƯỢC cục bộ | Có tại đúng SHA được khai |
| L:221–223,267–269,335, doctrine-scan | **7/7 tệp**, **0/0 chỗ chép doctrine** | Cả các SHA tiền/hậu kiểm khớp, stdout dương, `rc=0` | ĐO ĐƯỢC cục bộ | Có |
| L:224–226,270–272,336, adr-song | **46/46 ADR**, **46/46 dòng §20** | Cả các SHA khớp; có miễn thiếu trạng thái ADR-0016 như khai | ĐO ĐƯỢC cục bộ | Có |
| L:227–229,273–275,336, doc-claims | `ok: true`, **106/106 tệp**, **0/0 cờ cứng**, **367/367 advisory** | Cả các SHA khớp; `rc=0`. Roots mặc định không quét `ops/land` | ĐO ĐƯỢC cục bộ | Có; không chứng minh văn xuôi L đúng |
| L:276–278,336, ShellCheck | `rc=0`, phiên bản 0.9.0 | **1/1 script đầu vào** có **13.252/13.252 byte**, hash giữ trong kết quả; JSON **0/0 diagnostic**, `rc=0` | ĐO ĐƯỢC cục bộ | Có; không chỉ tin output rỗng |
| L:279–292,334–335, lease đủ công cụ | **121/121 ca đạt**, **121/121 ca chạy**, **0/0 ca bỏ qua** | Đúng tập đăng ký; `rc=0`; actionlint 1.7.7 và ShellCheck 0.9.0 có mặt | ĐO ĐƯỢC cục bộ | Có |
| Cùng mục, lần thiếu actionlint | **120/120 ca đạt**, **1/1 ca đỏ**, **121/121 ca chạy** | `rc=1`; đúng `t33_workflow_dang_lease_phai_qua_actionlint` đỏ vì thiếu actionlint; **0/0 ca bỏ qua** | ĐO ĐƯỢC cục bộ | Có; đỏ đúng thiết kế, không gọi là gate đạt |
| L:244–263, Git hậu merge | Không nông, **1.879/1.879 commit**; master `c0a5cbe`; **0/0 commit nhánh dư** | Ref snapshot cho đúng số, đúng ancestry; parents `f4d74fe` và `efa397e` | ĐO ĐƯỢC Git | Có qua namespace tương đương |
| L:298–314, Windows | PR thường Linux; master Linux+Windows; “lần đầu lên lịch” | Ma trận đúng **1/1 hệ điều hành** và **2/2 hệ điều hành** theo điều kiện. Nhãn/dispatch/đầu tiên/đã biết kết quả không có nguồn | Cấu hình ĐO ĐƯỢC; lịch sử KHÔNG ĐO ĐƯỢC | **Vế lịch sử chưa đóng** |
| L:329–330, inventory land | Base **4/4 tệp**, head merge **6/6 tệp**, sau thêm L **7/7 tệp** | `ls-tree` tại `f4d74fe`, `efa397e`, reviewed SHA đúng tập | ĐO ĐƯỢC | Có; không đếm số lần land |
| L:360–361, độ phủ nguồn cũ | **526/526 lá YAML**, **0/0 lá cắt**; thiếu **2/2 Markdown**, **242/242 lá JSON**, **62/62 dòng comment** | Đếm nguồn tại `98ef1f1`, `efa397e`, head đều khớp. Scanner comment loại dấu `#` trong scalar; **3/3 verdict** PR #487 lượt sau và PR #489 các lượt có cùng slug độ phủ | Số nguồn ĐO ĐƯỢC; phép so TSV KHÔNG ĐO ĐƯỢC | Không chứng thực “0 lá cắt” từ `tables.json` một mình |
| L:367–368, prompt cũ/diff | Prompt **560/560 dòng thêm**; Git **950/950 dòng thêm**, **132/132 dòng bớt**, **8/8 tệp**; thiếu **390/390 dòng thêm** | Git đúng; phép trừ đúng từ scalar khai; prompt gốc không có để đọc lại | Git/phép tính ĐO ĐƯỢC; prompt KHÔNG ĐO ĐƯỢC | Phần Git khớp |
| L:4–7, số §20 | **10/10 lần nhắc theo bảng** ở lease_publish; **11/11 lần nhắc theo bảng** ở packet_loop | Protocol:1136 có đúng scalar; đây là bảng lịch sử/proxy về khái niệm, không phải đếm literal ADR-ID trong mã | ĐO ĐƯỢC lời dẫn | Có; không suy enforcement |
| L:375–390, chuỗi/chi phí | **6/6 ID PR**, dừng trước mắt xích kế; khoảng 24 phút CI, 16 phút review | Chuỗi đúng số ID; **5/5 merge message** của PR trước #490, **0/0 merge message #490**. Từ lời khai: 1411 giây ≈ 23,52 phút; 982,697 giây ≈ 16,38 phút | Git/phép tính ĐO ĐƯỢC; chi phí thực KHÔNG ĐO ĐƯỢC | Ước tính đã đúng loại nguồn |
| L:402–416, miễn trừ/duyệt | **2/2 mục miễn**, duyệt vẫn giữ | YAML đủ mục; bộ phản chứng mã giữ head/danh tính/thẩm quyền | Nội dung/mã ĐO ĐƯỢC; authority KHÔNG ĐO ĐƯỢC | Không dùng lời khai cấp quyền |
| L:418–420, đường land/cổng | **2/2 tệp văn bản**, **17/17 lệnh con**, **2/2 literal landed** | `rg` thường và `--hidden` cho cùng tập; AST đúng parser/literal | ĐO ĐƯỢC phạm vi kho | Có về số; không bảo đảm mọi gate/CI đều xanh |
| L:171–172,357,386–390,445–462, lịch sử phiên/giới hạn | “lần thứ tư”, các lượt có cùng họ finding, chi phí/identity/HTTP 403/comment | Nội dung các verdict cũ có thể đọc; không có toàn transcript/API/runtime để đo tần suất phiên, hành vi proxy hoặc model lịch sử | KHÔNG ĐO ĐƯỢC sự kiện ngoài gói | Không coi lời thuật lại là quan sát độc lập |

Không có số Git hay số cổng cục bộ bị trôi. Sai số có ý nghĩa nằm ở **số neo bị quy là mất khi squash**, còn các phép so thiếu đầu vào phải giữ KHÔNG ĐO ĐƯỢC. [numeric-lines.json](phep-do/numeric-lines.json) giữ mọi dòng chứa số/chữ đếm để đối chiếu, kể cả định danh và comment.

**Tổng kiểm thực thi:** **12/12 lần gọi cổng có bằng chứng dương để đối chiếu**, gồm **11/11 lần trả `rc=0`** và **1/1 lần `rc=1` đúng ca thiếu công cụ**. Mọi **10/10 mục `DAT_DO_LAI_CUC_BO`** đều có phép tái chạy tương ứng; **4/4 mục `DAT_DO_GIT`** có nguồn Git. Các **2/2 mục `DAT_THEO_LOI_KHAI_API`** vẫn không được coi là đã đo CI. Phản chứng chỉ dùng bộ có sẵn trong cây, chạy trên clone; không tự soạn nội dung dựng đường dẫn thoát khỏi cây.

### van-xuoi-do-duoc-van-vuot-nguon  [P3]  Văn xuôi vẫn vượt nguồn ở lịch sử Windows và số neo sẽ mất khi squash.

**Vị trí:** L:306–314; chỗ cùng lớp tìm được khi quét toàn tệp: L:63–65. Các cảnh báo phạm vi ở L:360–361,398–401,418–421 cũng cần được giữ như trong bảng audit, không nâng thành kết quả xác thực toàn thể.

**Vế Windows còn tồn tại.** Ngay sau “ĐO ĐƯỢC (đọc `.github/workflows/ci.yml`)”, L:307–308 khẳng định PR không có nhãn `windows` và không ai gọi `workflow_dispatch`. YAML chỉ chứa điều kiện xét các sự kiện ấy, không chứa lịch sử chúng. L:311–313 đổi tên sự kiện từ “đo” sang “lên lịch”, vẫn khẳng định thứ tự đầu tiên cho mã cụ thể. Việc chưa giữ run JSON và chưa quét lịch sử được chính L:309–310 thừa nhận. Vì vậy đây là vế chưa đóng của finding trước, không phải chỉ một lựa chọn câu chữ.

Đối chứng: `python3 -B phep-do/do-static.py` đọc trigger/matrix/checkout, inventory nguồn và scalar cũ/mới. [source-boundaries.json](phep-do/source-boundaries.json) giữ nguyên biểu thức với các nhánh dispatch/master/nhãn Windows, cùng các mệnh đề không có chứng cứ sự kiện. Mã/cấu hình đọc được không bị hạ xuống “không đo được”.

**Chỗ cùng lớp còn sót — “cả năm neo” là sai.** `git diff --name-only f4d74fe..efa397e -- '*.receipt.yaml'` cho **5/5 receipt đổi**. Nhưng đổi receipt không có nghĩa commit neo của receipt ấy mới được đưa vào canonical bởi PR #489:

| receipt | commit neo | quan hệ với base `f4d74fe` |
|---|---|---|
| `pr487-review-1-codex-verdict.receipt.yaml` | `a0b154d7c8e6491fb53825301ace2d6d4e97ac9f` | Đã là tổ tiên |
| `pr487-review-2-codex-verdict.receipt.yaml` | `edb288e4e95081b83661c94c88addea005d3f121` | Đã là tổ tiên |
| `pr487-hau-kiem-head-review-1-codex-verdict.receipt.yaml` | `e1fd0a333109a555af4823fd2b830521d86fafbd` | Chưa là tổ tiên |
| `pr489-review-1-codex-verdict.receipt.yaml` | `45bd80e08c5efdcb9d713e42fe0804f7d9fd3af1` | Chưa là tổ tiên |
| `pr489-review-2-codex-verdict.receipt.yaml` | `f7fe80261779b8d11bf55e9fedd55a6912e29b99` | Chưa là tổ tiên |

`python3 -B phep-do/do-more.py` tính tập `git rev-list f4d74fe`, kiểm từng OID và lưu đường ancestry dương trong [anchors.json](phep-do/anchors.json). **2/2 neo** đầu đã nằm trong base; **3/3 neo** còn lại chưa nằm trong base. Một squash commit có base đó làm cha vẫn giữ tổ tiên của cha, nên không thể làm mất cả các neo đầu chỉ vì squash PR này. Không cần tạo commit tổng hợp để chứng minh phản ví dụ ấy. Lý do chọn merge để giữ các neo còn lại có cơ sở; con số “cả năm” thì không. Chính `.anchor.gioi_han` được trích là lời cảnh báo chung, không phải phép đo tác động cho PR #489.

**Vá ở đâu và thế nào.** Sửa chính khối Windows trong `post_merge_checks`: tách mô tả ma trận khỏi lời khai lịch sử nhãn/dispatch; bỏ tính “đầu tiên” và lời bảo đảm sẽ biết kết quả, hoặc viết rõ là suy luận có điều kiện với các tiền đề chưa xác minh. Giữ cấu hình đọc được ở lớp ĐO ĐƯỢC. Sửa `land_operator_neo.vi_sao_MERGE_chu_khong_SQUASH`: đếm neo chưa nằm trong base thay cho đếm receipt đổi; ghi riêng tập neo đã tồn tại trong base. Với các kết quả cũ thiếu TSV và khẳng định mọi cổng, gắn phạm vi/attestation rõ như bảng audit. Đường rẻ nhất là sửa ranh giới lời khai; đường giữ khẳng định sự kiện mạnh phải bổ sung đầu vào gốc có SHA/phạm vi/thời gian.

**Ca khóa lỗi.** Đã chạy các phép đo Git, nguồn và cấu hình nêu trên; không chỉ đề xuất rồi bỏ đó. Ca kiểm cho lần vá: một câu chỉ thay “đo Windows đầu tiên” bằng “lên lịch Windows đầu tiên” vẫn phải bị loại nếu không có event history. Kiểm neo trên **5/5 receipt** phải cho đúng tập OID tổ tiên của base; cách đếm đồng nhất “receipt đổi” với “neo mới” phải bị bác bởi các neo PR #487 có sẵn. Với thiếu TSV, chỉ bảng tổng số không được chứng minh giữ nguyên mọi lá. Chưa có validator máy đủ để bảo đảm toàn bộ ngữ nghĩa văn xuôi; không nhận regex hay `rc=0` của script inventory là loại bảo đảm ấy.

**Rủi ro khi vá.** Hạ chung cả đoạn sẽ làm mất phần cấu hình, Git và cổng cục bộ thực sự tái lập được. Hướng ngược lại là dùng một số có nguồn để bảo lãnh mệnh đề bên cạnh, hoặc nhầm điều kiện xảy ra với lịch sử đã xảy ra. Giữ riêng đối tượng, SHA/base, thời điểm và nguồn của từng mệnh đề; không cần sửa doctrine, mở PR kế nhiệm hoặc cấp quyền land để đóng finding này.

## GIỚI HẠN

- **Không mạng.** Mọi sự kiện GitHub API/CI — approval/dismissal/quyền/merged_by/CAS, nhãn/event/run/conclusion/timing, checkout runner, comment byte và sự vắng mặt của PR — đều **KHÔNG ĐO ĐƯỢC**. Số ref chỉ xác minh trong snapshot được cấp.
- Gói cung cấp `refs/heads/*`, không có `refs/remotes/origin/*`. Lệnh gọi nguyên tên `origin/master` trên cây review thất bại `rc=128`; đã lưu trong [static-attempt1-commands.json](phep-do/static-attempt1-commands.json). Các phép đo tương ứng dùng `refs/heads/master` và `refs/heads/claude/land-480-20260909`, đối chiếu tập tên–OID của mirror/TSV, không tạo ref trong cây. Lỗi đường dẫn ở script đo đã được sửa trong cùng phiên; không có reviewer chết/phóng lại.
- Cổng tái chạy chứng minh hành vi cục bộ ở đúng commit, không hồi tố thời điểm tiền/hậu kiểm hay biến nó thành CI thật. Không chạy Windows, full selftest sản phẩm, merge, deploy hoặc đọc API. Bộ phản chứng danh tính cũng tự báo chưa đo ngữ nghĩa trigger GitHub bằng PR đối kháng.
- Thiếu hint gốc, TSV cấu trúc gốc, prompt lịch sử và runtime/API log. Có báo cáo kết quả cũ không đồng nghĩa đủ đầu vào để chạy lại phép so. Dự kiến về #490 không được biến thành sự kiện quan sát, và số grep/AST không chứng minh mọi check bên ngoài kho đều xanh.
- Cây review giữ nguyên: **1.867/1.867 tệp tracked** khớp blob sau clean filter của Git; **3/3 tệp `.cmd`** có CRLF trong worktree theo `.gitattributes` và LF trong blob, đã có sẵn trong manifest, không phải sửa của reviewer. **3.201/3.201 hiện vật gốc** vẫn nguyên băm, **0/0 hiện vật lệch**, **0/0 byte porcelain**, head/tree/ref không đổi. Các **2/2 clone** phục vụ đo cũng sạch. [final-integrity.json](phep-do/final-integrity.json).

Verdict không cấp quyền merge và không chứng nhận `landed` hoặc `complete` cho #489/#490.
