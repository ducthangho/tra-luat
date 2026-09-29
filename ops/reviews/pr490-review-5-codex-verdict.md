verdict: approve
reviewed_sha: dccce0a54efdd687c20e128b64de1e355089c261
luot: 5
so_lan_luot_nay_bi_chet_va_phong_lai: 0

0 finding P1 · 0 finding P2 · 0 finding P3

Reviewer: Codex/OpenAI, GPT-6 theo cấu hình phiên; provider `openai_codex`, execution surface agent API có shell cục bộ, transport `machine`. Phiên độc lập với executor Claude; không có GitHub submitter vì không đăng gì lên mạng. Authority là yêu cầu đọc `PROMPT.md` và thực hiện review offline của gói này. Phạm vi ghi chỉ là `VERDICT.md` và `phep-do/` ngoài cây được review; không commit hoặc cấp quyền land. Tree được review: `c57aaf5a2e19271d128c005cbfab8c3f44d11590`.

**L** là `cay-kho/ops/land/pr489-land-evidence.yaml`, khớp nguyên byte `BAN-DANG-REVIEW.yaml`. **Approve áp cho hồ sơ tại exact SHA trên.** Không hồi tố thành cross-review cho `efa397e`, không xóa nợ đã khai, không chứng nhận CI/GitHub hoặc việc #490 đã merge/land.

Các phép đếm dưới đây dùng cặp bằng nhau và ghi đơn vị; tập đạt, tập đỏ, tập thiếu được đếm riêng. SHA, số dòng, ID PR/run/ADR, phiên bản, mã thoát và timestamp là định danh/giá trị kỹ thuật. JSON giữ số và kiểu dữ liệu để máy đọc được; lời trích lịch sử không được biến thành số đo mới. Đã ghi kết luận ngay khi hoàn tất đối chiếu và các phép tái chạy, rồi hoàn thiện hiện vật cùng lượt.

## ĐỐI CHIẾU LƯỢT 4

| Finding lượt trước | Nhãn duy nhất cho cả lớp | Kết luận |
|---|---|---|
| `van-xuoi-do-duoc-van-vuot-nguon` | **ĐÃ VÁ THẬT** | Đã kiểm đủ **3/3 vị trí** cùng các bản lặp trong ledger. Tiền kiểm Windows không còn kết luận lịch sử CI; kết quả bảng cũ đã thành attestation có giới hạn đầu vào; kết luận cổng đã giới hạn vào phép quét cụ thể. Không thấy phần sửa tái tạo lỗi ở nơi khác trong L. |

**Windows — L:251–266.** Đây là đóng lỗi về chứng cứ, không chỉ đổi nhãn né lỗi. Trước đây, tên mục là “CI Windows trên head”, `not_run` được suy từ không nhãn/không dispatch, trong khi hậu kiểm nói chưa biết chính lịch sử ấy. Nay **tên mục, trường giải thích đối tượng và lời đính chính cùng đổi**: `not_run` nói bước đọc kết quả của hồ sơ chưa được thực hiện; tiền đề không nhãn/không dispatch chỉ còn trong phần trích lời sai đã rút. Điều đó nhất quán với L:335–339. Lời khai điều phối không đọc thực tế vẫn không được kiểm chứng độc lập; nó khai khoảng trống chứng cứ của hồ sơ, không xác nhận trạng thái runner. [Đối tượng và giới hạn nguồn](phep-do/source-boundaries-current.json)

**Có nên bỏ mục đó khỏi `pre_merge_checks`? Không bắt buộc.** Mục này còn nghĩa là một bước thu thập/đọc bằng chứng tiền kiểm chưa làm. Nó không có `ket_qua` hay trạng thái đạt và không thay thế một lượt Windows đạt. Mẫu tại `PROTOCOL:466–488` chỉ quy định danh sách, không quy định mỗi phần tử phải là job CI hoặc một enum tên cổng đóng. Các hồ sơ ngang hàng cũng chứa việc kiểm quan hệ Git, lời khai và kiểm quy trình. Có thể chuyển nó sang `khong_do_duoc` để gọn hơn, nhưng việc đó không mua thêm độ đúng cần thiết cho finding này. Không tìm thấy consumer thực thi đọc các khóa tiền/hậu kiểm trong phạm vi literal đã ghi; không dựng giả một bộ đọc chỉ xét tên cổng để buộc sửa schema. [Schema và nội dung tiền kiểm ngang hàng](phep-do/schema.json), [phạm vi tìm consumer](phep-do/details.json)

Phần cấu hình vẫn hữu ích: workflow có **1/1 bước checkout**, **0/0 khai báo `with.ref`**, **0/0 khai báo `pull_request.types`**; biểu thức ma trận được suy giải trên **8/8 tổ hợp boolean**. Khi có dispatch, ref master hoặc nhãn Windows, nhánh rộng chứa **2/2 hệ điều hành**; còn lại **1/1 hệ điều hành**. Đây là đọc biểu thức, không chạy GitHub expression engine hoặc chứng minh event `labeled`/run đã xảy ra. Những câu về nhãn, dispatch, lịch sử Windows và thứ tự “đầu tiên” vẫn là **4/4 câu hỏi lịch sử KHÔNG ĐO ĐƯỢC**. [Workflow](phep-do/workflow.json)

**Bảng nguồn — L:394–404.** Tái đếm được **526/526 lá YAML nguồn**, **62/62 comment YAML**, **242/242 lá JSON** và **2/2 tệp Markdown** nằm ngoài đầu vào bảng cũ. L hiện chỉ gọi kết quả giữ đủ bảng/không cắt là lời khai của reviewer, nêu rõ thiếu TSV gốc. Các tệp `claim-ledger.tsv` mới nhập kho là ledger PR #490; chúng không phải TSV đã dùng để so bảng YAML của PR #489. Do đó bản vá giữ được thông tin lịch sử mà không tiếp tục bảo lãnh một phép so không tái lập được. [Đếm lại nguồn cũ](phep-do/old-coverage.json)

**Hệ quả đóng chuỗi — L:459–470.** Không hạ quá tay và không thành câu rỗng. Khối này vẫn cho một kết quả tái lập và có thể bị bác: phép tìm literal với loại trừ đã khai trả **2/2 tệp Markdown**; AST `packet_loop.py` cho **17/17 lệnh con** và **2/2 chuỗi mô tả** chứa `landed`. Các tệp khớp literal là `ops/DO_VI_SAO_LEASE_482_483_CHET_20260909.md` và `ops/prompts/handoff-264-review-1-claude-20260823.md`. Tập đó cung cấp điểm bắt đầu cụ thể khi tìm sự phụ thuộc trực tiếp vào hồ sơ; không tìm thấy cổng đọc hồ sơ land trong tập ấy. [Phạm vi quét và danh sách AST](phep-do/code-scope.json)

Giá trị thực hành còn lại là chỉ ra khoảng cách giữa nghĩa vụ bookkeeping cho người đọc và chỗ cưỡng chế trực tiếp đã tìm được. Nó không còn hứa việc dừng chuỗi sẽ giữ mọi cổng xanh. `pham_vi_cua_ket_luan` loại trừ rõ đường dẫn dựng động, consumer ngoài kho và CI/API; `thu_mat_la_gi` cũng mang cùng phạm vi. Đọc cụm “trong các tệp đã quét” cùng các giới hạn liền kề là kết luận hữu hạn, không phải kết luận toàn kho. Không cần tạo phản chứng đường dẫn thoát cây để chốt giới hạn logic này.

**Lớp lỗi lặp từ các lượt trước đã đóng:** phép kiểm quyết định là so đối tượng trạng thái tiền/hậu kiểm, đếm lại đúng đầu vào của bảng, kiểm tập literal/AST và rà lại **95/95 hàng audit**. Việc làm theo gợi ý reviewer cũ tự nó không được dùng làm bằng chứng đúng.

## CẬP NHẬT BẢNG KIỂM KÊ

Đã dùng lại **95/95 ID** từ `LEDGER-luot4.json`; không dựng bộ mệnh đề khác. JSON và verdict cũ được đưa vào kho khớp nguyên byte với bản cung cấp; TSV cũ có **95/95 hàng** khớp các trường tương ứng trong JSON. Đã so diff trực tiếp `c42fc74..dccce0a`, ánh xạ dòng và cập nhật các hàng sau. [Diff theo hàng](phep-do/ledger-delta.json), [ledger hiện tại có giữ nguyên từng hàng cũ](phep-do/claim-audit-current.json), [TSV hiện tại](phep-do/claim-ledger-current.tsv)

| ID | Dòng tại `c42fc74` → dòng tại head hiện tại | Hàng cũ nay còn đúng không? |
|---|---|---|
| C047 | 251–254 → 251–262 | **Không nếu áp cho head mới.** Mệnh đề “tiền kiểm CI Windows not_run vì không nhãn/dispatch” đã bị rút. Hàng cập nhật phân biệt bước đọc hồ sơ chưa làm với trạng thái CI chưa biết. |
| C048 | 255–257 → 263–267 | **Còn đúng về nội dung cấu hình.** Nay phần ấy tách thành `cau_hinh_thi_doc_duoc`; vị trí cũ không còn dùng được. Không coi đọc YAML là tái chạy semantics của GitHub. |
| C074 | 384–386 → 394–395 và 398–404 | **Không nếu giữ nguyên kết luận về head mới.** Nguồn vẫn đếm được; mệnh đề giữ nguyên bảng/không cắt nay được gắn attestation và thiếu TSV. Cập nhật nội dung, nguồn và phạm vi. |
| C075 | 386–387 → 395–397 | **Còn đúng.** Đề xuất packet, cổng và phản chứng vẫn giữ nguyên ý nghĩa; chỉ đổi vị trí/bao dòng. |
| C085 | 442–446 → 459–470 | **Không nếu áp cho head mới.** Số literal/AST giữ nguyên, nhưng kết luận “không cổng nào đỏ” đã rút và scalar đổi thành mapping có phạm vi. Hàng hiện tại ghi đúng cấu trúc và giới hạn mới. |
| C003 — ảnh hưởng gián tiếp | 7 → 7 | **Nhận xét bác lời giới thiệu đã lỗi thời với head mới.** Comment không đổi, nhưng các phản ví dụ C047/C074/C085 mà hàng này viện dẫn đã được sửa. Cập nhật nhận xét; không biến nó thành bảo đảm mọi attestation là sự thật. |

Tổng cộng **5/5 hàng** giao trực tiếp phần dòng bị thay; **1/1 hàng** cần đổi đánh giá vì phụ thuộc ngữ nghĩa. Có **4/4 hàng** không được chép nguyên kết luận sang head mới: **C003, C047, C074, C085**. Trong bản cập nhật, **51/51 hàng** có tọa độ dòng khác bản cũ, kể cả các hàng gộp nhiều vị trí như C010 và C029; **44/44 hàng** giữ tọa độ. Danh sách đầy đủ và cả nội dung trước/sau nằm trong JSON, không chỉ các ví dụ ở bảng này.

**Bảng nhập kho có lỗi thời không? Có, nếu dùng nó như ledger của head hiện tại; không, nếu dùng đúng là hiện vật lượt 4.** Trong kho, `pr490-review-4-codex-verdict.md` ghi exact `reviewed_sha: c42fc74…`; `source-boundaries.json` cũng neo SHA đó. Gói giao việc nói rõ ledger là của SHA cũ. Vì vậy việc nhập bản lịch sử nguyên trạng không phải finding mới và không nên sửa ngược bản lịch sử. Nhưng các giá trị coverage cũ **214/214 scalar**, **225/225 khóa** không còn là coverage hiện tại. Bản hiện tại có **219/219 scalar**, **231/231 khóa**, **27/27 comment** được ánh xạ; **0/0 phần tử** ngoài ánh xạ ở từng tập. [Coverage hiện tại](phep-do/coverage-current.json), [nguyên văn từng node](phep-do/syntax-current.json)

Ledger mới khai `old_reviewed_sha`, `reviewed_sha`, `old_row`, vị trí mới và `source_current` để không vô tình dùng nguồn lịch sử như phép đo mới. Phép vét cú pháp bảo đảm có đọc mọi scalar/khóa/comment, không tự chứng minh chân lý của prose. **245/245 dòng** chứa số hoặc từ đếm theo regex phụ đều có ID audit; regex này không thay việc đọc ngữ nghĩa. [Đối chiếu dòng có số](phep-do/numeric-lines.json)

## BẢNG ĐO

Các cổng được tái chạy trong bản clone cục bộ `phep-do/replay/`, từ object của `cay-kho/`, tại đúng SHA lịch sử mà L dẫn. Đã ghim `core.abbrev=7`, `core.autocrlf=false`; Python không ghi bytecode. Dùng `actionlint` 1.7.7 sẵn trong gói và ShellCheck 0.9.0, không cài qua mạng. [Công cụ](phep-do/tools.json), [lệnh/mã thoát/log cổng](phep-do/gate-commands.json), [kết quả có bằng chứng dương](phep-do/gates.json)

| Đối tượng và nguồn | Kết quả tự đo cùng giới hạn |
|---|---|
| Toàn vẹn gói | **3.214/3.214 tệp** khớp manifest; **317/317 cặp tên–OID ref nhánh** khớp snapshot, **0/0 cặp lệch**; shallow=`false`. Snapshot không chứng minh trạng thái máy chủ hiện tại. [Preflight](phep-do/preflight.json), [hash từng tệp](phep-do/integrity.json) |
| Diff lượt này | **1/1 commit**, **7/7 tệp**, thêm **1.171/1.171 dòng**, bớt **13/13 dòng**. Riêng L thêm **37/37 dòng**, bớt **13/13 dòng**; phần còn lại là **6/6 tệp hiện vật lượt 4**. Patch cung cấp khớp Git. [Diff](phep-do/diffs.json) |
| `9a99dd8..efa397e` — L:34–43 | **5/5 commit**, **14/14 tệp**, thêm **3.135/3.135 dòng**, bớt **132/132 dòng**. Commit `08b4c0e` đổi **105/105 dòng** của hồ sơ #480 và **108/108 dòng** của #487. Numstat không tự chứng minh đã sửa đúng mọi finding. [Diff](phep-do/diffs.json) |
| `98ef1f1..efa397e` — L:129–137 | **2/2 commit**, **8/8 tệp**, thêm **2.189/2.189 dòng**, bớt **4/4 dòng**; commit verdict thêm **4/4 tệp hiện vật đo**. Khóa `bon_loi_lich_su_git_dieu_phoi_tu_kiem_lai` trong biên nhận có **4/4 phần tử**. [Diff](phep-do/diffs.json), [chi tiết](phep-do/details.json) |
| `9a99dd8..98ef1f1` — L:409–411 | **8/8 tệp**, thêm **950/950 dòng**, bớt **132/132 dòng**. Phép trừ số Git với giá trị prompt được thuật lại cho **390/390 dòng chênh**. Giá trị “560 dòng” của prompt cũ: **KHÔNG ĐO ĐƯỢC**, không có prompt gốc; đây là phép tính có đầu vào attestation. [Diff](phep-do/diffs.json), [giới hạn](phep-do/source-boundaries-current.json) |
| Neo receipt — L:62–83 | **5/5 receipt đổi**; **2/2 neo** đã thuộc base, **3/3 neo** chưa thuộc base; **5/5 neo** thuộc head và merge thật. Kiểm cả membership của tập `rev-list` lẫn `merge-base --is-ancestor`, không lấy số receipt đổi làm số neo mới. [Từng neo đầy đủ](phep-do/anchors.json) |
| Git hậu merge — L:273–289 | Master snapshot=`c0a5cbe`, có **1.879/1.879 commit reachable**, kể cả chính nó; merge có **2/2 cha** đúng `f4d74fe` và `efa397e`; head thuộc ancestry; **0/0 commit** nhánh `claude/land-480-20260909` ngoài master. Timestamp object Git khớp `2026-09-09T14:51:22Z`; API `merged_at` không đo độc lập. [Git](phep-do/anchors.json) |
| Inventory `ops/land/` — L:364–366 | Base **4/4 tệp**; head #489 **6/6 tệp**; merge #489 **6/6 tệp**; head review hiện tại **7/7 tệp**. Đây là tệp Git, không phải số lần land. [Danh sách](phep-do/land-inventory.json) |
| Review #489 — L:86–124 | **2/2 bản ghi review**. Tiêu đề lượt đầu: **1/1 finding P1**, **4/4 finding P2**, **6/6 finding P3**. Lượt sau: **0/0 finding P1**, **0/0 finding P2**, **4/4 finding P3**. Đối chiếu **11/11 slug**: **9/9 đã vá**, **0/0 vá hờ**, **1/1 sinh lỗi**, **1/1 chưa vá**. Danh tính model thực phục vụ và runtime: **KHÔNG ĐO ĐƯỢC**. [Regex trên verdict](phep-do/reviews.json) |
| Mapping trạng thái — L:88–97, 190–199 | Từ bản trước, **17/17 mapping kết quả** từng thiếu trạng thái. Hiện có **10/10 mục tiền kiểm**, **11/11 mục hậu kiểm**, tổng **21/21 mục ngoài**; **17/17 mapping kết quả ngoài** cộng **1/1 mapping lồng**, tổng **18/18 mapping kết quả**, **0/0 mapping kết quả thiếu trạng thái**. Đếm cả loại không có kết quả: **22/22 mapping trạng thái**. Comment định nghĩa **5/5 giá trị phân loại kết quả** và **2/2 giá trị không chạy** (`not_run`, `skipped`). [Các tập đếm](phep-do/statuses.json), [comment nguyên văn](phep-do/syntax-current.json) |
| Receipt gate tại mỗi SHA `efa397e`, `c0a5cbe` — L:236, 292, 368–371 | Mỗi SHA: **94/94 bản ghi** = **41/41 v2 đạt**, **11/11 legacy**, **42/42 nợ đóng băng**; **0/0 vi phạm**, **0/0 chưa đo**, `TỔNG: ĐẠT`, `rc=0`. Không chứng minh identity/approval thật. [Gates](phep-do/gates.json) |
| Doctrine scan tại mỗi SHA trên — L:239, 295 | Mỗi SHA: **7/7 tệp quét**, **0/0 chỗ chép doctrine**, marker sạch, `rc=0`. [Gates](phep-do/gates.json) |
| ADR tại mỗi SHA trên — L:242, 298 | Mỗi SHA: **46/46 ADR**, **46/46 hàng §20**, khớp theo cổng, `rc=0`; ngoại lệ thiếu trạng thái là **1/1 ADR**, ADR-0016. [Gates](phep-do/gates.json), [nguồn](phep-do/details.json) |
| Doc claims strict tại mỗi SHA trên — L:245, 301 | Mỗi SHA: `ok=true`, **106/106 tệp**, **0/0 cờ cứng**, **367/367 advisory**, `rc=0`. [Gates](phep-do/gates.json) |
| ShellCheck — L:302–304 | **1/1 tệp đầu vào** không rỗng, giữ hash; **0/0 diagnostic** trong JSON, `rc=0`, phiên bản 0.9.0. [Gates](phep-do/gates.json) |
| Lease đủ công cụ — L:305–319 | **121/121 ca đăng ký**, **121/121 ca thực thi**, **121/121 ca đạt**, **0/0 ca bỏ qua**, `rc=0`. AST giữ tên từng ca; stdout giữ phản chứng có sẵn. [Log đủ công cụ](phep-do/c0a5cbe-lease.stdout) |
| Lease thiếu `actionlint` — cùng khối | **121/121 ca thực thi**; tập đạt **120/120 ca**, tập đỏ **1/1 ca**, đúng `t33_workflow_dang_lease_phai_qua_actionlint`, với thông báo thiếu công cụ; **0/0 ca bỏ qua**, `rc=1`. Không coi đây là một lượt đạt toàn bộ. [Log thiếu công cụ](phep-do/c0a5cbe-lease-no-actionlint.stdout) |
| Cổng duyệt danh tính — L:453–458 | Suite có sẵn: **40/40 ca nền đạt**, **46/46 đột biến** giết đúng tập đích, `TONG: DAT`, `rc=0`. Đây là phép thử mã cổng, không xác nhận approval/run GitHub. [Log](phep-do/c0a5cbe-duyet.stdout) |
| Nguồn bảng cũ — L:394–404 | Tại `98ef1f1`: **5/5 YAML nguồn**, **526/526 lá**, **62/62 comment**; **242/242 lá JSON** và **2/2 Markdown** ngoài đầu vào bảng. Bảo toàn type/path/value trong TSV đích và “0 lá cắt”: **KHÔNG ĐO ĐƯỢC**. [Nguồn](phep-do/old-coverage.json) |
| Cấu trúc chuỗi/miễn — L:417–419, 444–452 | Scalar chứa **6/6 ID PR** và danh sách có **2/2 mục miễn**. Chỉ số `mat_xich_thu: 6` khớp scalar; `mat_xich_thu_7: KHONG_TON_TAI` là lời khai/dự kiến theo quyết định, không phải phép đếm PR live. [Cấu trúc](phep-do/structural-numbers.json) |
| Phạm vi quét — L:460–470 | **2/2 tệp literal**, đều Markdown; **17/17 lệnh con**; **2/2 chuỗi mô tả `landed`**. Giới hạn theo tập mã/SHA, không chứng minh mọi cổng. [AST và tên tệp](phep-do/code-scope.json) |
| §20 — L:5 | **1/1 hàng ADR-0034** chứa đúng giá trị bảng `lease_publish.py ×10` và `packet_loop.py ×11`. Xác nhận nội dung bảng, không biến các số thuật lại thành số gate đang cưỡng chế hoặc số literal hiện tại trong mã. [Hàng nguyên văn](phep-do/code-scope.json) |
| Số thiếu nguồn lịch sử — L:101–102, 140–142, 187–188, 205, 218, 223–225, 231, 409–411, 428–432, 503–506 | Runtime **1559.927**, **982.697**, **1411**, **1541**, **23 giây**; ước tính **~24**, **~16 phút**; số tệp/hunk/dòng hint, số review API, số lần tóm tắt sai, “560 dòng” prompt và HTTP `403`: **KHÔNG ĐO ĐƯỢC** sự kiện được thuật lại. Không thay đầu vào mất bằng lời nhắc trong receipt/verdict. [Giới hạn nguồn](phep-do/source-boundaries-current.json), [ledger](phep-do/claim-audit-current.json) |

**Schema so protocol và các hồ sơ ngang hàng.** Đã parse **7/7 YAML**, **0/0 khóa trùng**. L đủ **16/16 khóa mẫu**, `pre_merge_checks`, `post_merge_checks`, `bookkeeping` đều là list. Mẫu không định nghĩa schema đóng cho trường bổ sung, tên `ten` hay nội dung các mục kiểm. `mission_id: pr-489` không bám tiền tố ví dụ `gh-<issue>`; các hồ sơ PR ngang hàng cũng dùng tiền tố `pr-`, và đoạn mẫu không khai regex cưỡng chế. Không bịa thêm enum/ràng buộc để tạo finding. [So schema](phep-do/schema.json)

| Tệp trong `ops/land/` | Khóa mẫu và phần thiếu | Bookkeeping |
|---|---|---|
| `plat-x8-land-evidence.yaml` | **16/16 khóa có**, **0/0 khóa thiếu** | **3/3 phần tử** |
| `pr468-hoso-4-packet-land-evidence.yaml` | **16/16 khóa có**, **0/0 khóa thiếu** | **5/5 phần tử** |
| `pr477-dung-goi-review-land-evidence.yaml` | **15/15 khóa có**, **1/1 khóa thiếu**: `session_id` | **4/4 phần tử** |
| `pr478-land-evidence.yaml` | **16/16 khóa có**, **0/0 khóa thiếu** | **6/6 phần tử** |
| `pr480-land-evidence.yaml` | **16/16 khóa có**, **0/0 khóa thiếu** | **8/8 phần tử** |
| `pr487-land-evidence.yaml` | **16/16 khóa có**, **0/0 khóa thiếu** | **7/7 phần tử** |
| L — `pr489-land-evidence.yaml` | **16/16 khóa có**, **0/0 khóa thiếu** | **5/5 phần tử** |

Thiếu `session_id` ở hồ sơ #477 là hiện trạng ngoài tệp được sửa, đã được lượt trước ghi nhận. Không tạo finding mới cho diff này. Kiểm schema cũng không chứng nhận các giá trị là sự kiện thật.

**Không còn finding mới cần yêu cầu sửa ở lượt này.** Không tạo đề mục finding giả chỉ để có nội dung dưới `###`.

## GIỚI HẠN

- **Không mạng:** mọi khẳng định về GitHub API/CI là **KHÔNG ĐO ĐƯỢC**. Bao gồm approval/dismiss, actor thực, CAS đã gửi, label/dispatch/run/checkout, thời lượng runner, byte comment, quyết định miễn CI và việc chuỗi thực tế đã đóng. Git chỉ xác minh object, nội dung và snapshot ref trong gói.
- Tái chạy cổng trên Linux ở SHA được dẫn chỉ chứng minh khả năng tái lập hiện tại. Không chứng minh chúng đã chạy trước merge, không tái dựng thứ tự cài công cụ, không phải lượt Windows CI, full release gate hoặc deploy. Tổng **12/12 lần gọi cổng** có log và bằng chứng dương đúng kỳ vọng: **11/11 lần** `rc=0`, **1/1 lần** `rc=1` trong thử thiếu công cụ. [Gates](phep-do/gates.json)
- TSV gốc của bảng PR #489 và gói hint vẫn thiếu; ledger lịch sử PR #490 vừa nhập kho không bù được các đầu vào ấy. Nợ cross-review exact head #489 và các nợ đã khai vẫn còn. Approve này không xóa chúng.
- Ledger bảo toàn ID và văn bản cũ để kiểm tra delta; `source_current` mới là nơi chỉ hiện vật lượt này. Coverage cú pháp và regex không thay audit ngữ nghĩa; tìm literal không loại trừ consumer động hoặc ngoài phạm vi. Các phản chứng thực thi dùng suite có sẵn, không tự soạn nội dung dựng đường dẫn thoát cây.
- `cay-kho/` được giữ chỉ đọc. Kiểm cuối: head/tree không đổi, **1.876/1.876 tệp tracked** khớp hash trước khi đo, **697/697 ref cục bộ** giữ nguyên, **0/0 tệp thay đổi** trong porcelain và **0/0 ref thay đổi**. Tập ref cục bộ này rộng hơn tập `refs/heads` trong snapshot gói. [Tree cuối](phep-do/tree-after.json). Bản clone dùng để chạy cổng và toàn bộ hiện vật đều nằm ngoài cây được review.

Tái lập: chạy lần lượt `python3 -B phep-do/do-static.py`, `python3 -B phep-do/do-gates.py`, `python3 -B phep-do/do-details.py`, `python3 -B phep-do/do-final.py` từ gốc gói. `do-gates.py` dùng clone cục bộ sẵn ở `phep-do/replay/`; các lệnh dựng clone và giới hạn tái lập được ghi tại [README phép đo](phep-do/README.md). Các script không tự sinh kết luận ngữ nghĩa hoặc sửa cây được review.
