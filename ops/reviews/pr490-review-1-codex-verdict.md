verdict: changes_requested
reviewed_sha: 9238606b21344fedae8d9c191834193b4bbee582
luot: 1
so_lan_luot_nay_bi_chet_va_phong_lai: 0

0 finding P1 · 1 finding P2 · 3 finding P3

Đã rút thật việc dùng review stale và CI PR làm bằng chứng exact head. `bookkeeping` đủ trường và phân biệt `merged` với `landed`. Còn thiếu trạng thái kết quả, một tham chiếu khóa sai, lý do đệ quy chưa đồng bộ và lời văn tiếp tục nhận phần chưa đối chứng là “ĐO ĐƯỢC”. Các số Git và kết quả cổng cục bộ tái lập được đều khớp; không dùng chúng chứng nhận lịch sử chạy hoặc GitHub CI.

Verdict được ghi ngay khi xác định finding P2, rồi hoàn thiện bằng chứng trong cùng lượt. Reviewer: Codex/OpenAI, agent API có shell cục bộ, transport `machine`; phiên độc lập với executor Claude theo nhiệm vụ được giao. Không suy danh tính reviewer từ tài khoản GitHub; chưa đăng ra GitHub. Tree: `9b434a38f69b63f75ee7bf145119ec8a75694a60`. Authority/phạm vi là `PROMPT.md`: review offline, chỉ đọc kho, ghi verdict và phép đo ngoài `cay-kho/`; không phải thao tác land.

Quy ước: cặp bằng chứng `N/N` luôn có hai số bằng nhau, kèm đơn vị. Với lượt thất bại, tách tập đạt, tập đỏ và tổng đã chạy. SHA, PR/ADR, số dòng, schema version, ID, phiên bản công cụ và rc là định danh/giá trị kỹ thuật, không phải phép đếm. **L** dưới đây là `cay-kho/ops/land/pr489-land-evidence.yaml`; dòng nguồn thuộc reviewed SHA.

## ĐỐI CHIẾU 5 FINDING

| slug nguyên văn | nhãn | đối chứng độc lập |
|---|---|---|
| `Do not count the stale cross-review toward landing` | **ĐÃ VÁ THẬT** | L:129–135 có `KHONG_THOA`; L:180–184 là `not_run`; L:263–269 không tuyên `landed`. Verdict thật approve tại `98ef1f1…`; Git xác nhận **2/2 commit** tới `efa397e…`, tree khác. So SHA trả false, trạng thái hồ sơ đúng. Không còn câu trong chính L nhận cross-review cho head merge đã thỏa. Đây là sửa lời khai, chưa trả nợ review hay thêm validator vận hành. |
| `Do not treat the PR check as an exact-head gate` | **ĐÃ VÁ THẬT** | L:142–157 dùng `ket_qua_tho`, `KHONG_XAC_THUC_EXACT_HEAD`, cấm đếm vào cổng đạt cho authorized head; L:122–128 rút câu CI xanh trên chính head. Workflow có **1/1 bước checkout**, không `with.ref`; selftest PR không sinh evidence exact identity. Không có log/run JSON để chứng minh runner thật. |
| `Mark the unmeasured post-merge CI as not_run` | **ĐÃ VÁ THẬT** | L:233–245 có `trang_thai: not_run`, giải thích ở `ly_do`, không còn `ket_qua` tại mục bị chấm. Phân loại chưa phủ các mục khác: P2 bên dưới. Lời “vẫn chạy tự động” trong `ly_do` còn vượt nguồn: P3 riêng. |
| `Restore the required bookkeeping field` | **VÁ SINH LỖI MỚI** | Đã thêm đúng list, **5/5 phần tử**; phân biệt merged, hậu kiểm tại chỗ, nợ, không tuyên landed/complete. L có **16/16 khóa mẫu**; **6/6 hồ sơ đối chiếu** đều có bookkeeping. Nhưng L:269 mới thêm đường dẫn khóa thiếu cấp `no_review_head_da_merge`; P3 này không phủ nhận việc khôi phục schema đã thành công. |
| `Remove the invented recursive-PR requirement` | **VÁ HỜ** | L:305–311,347–357 rút luật tưởng tượng; quét độc lập docs không thấy luật đòi PR kế nhiệm. Nhưng L:117–121 vẫn nhận hậu kiểm `efa397e` sẽ lại đổi head/sinh mắt xích và “chuỗi này chưa có điều kiện dừng”. Lý do treo nợ giữ tiền đề đệ quy mà đoạn mới vừa bác. Cần ghi đúng đây là cách làm/quyết định lịch sử, không phải hệ quả bắt buộc của hậu kiểm; P3 bên dưới. |

Đủ **5/5 slug**: **3/3 slug ĐÃ VÁ THẬT**, **1/1 slug VÁ SINH LỖI MỚI**, **1/1 slug VÁ HỜ**, **0/0 slug CHƯA VÁ**. Severity hiện tại đếm riêng.

**Câu hỏi ngược:** không thấy bản vá hạ quá tay số Git, băm, nội dung verdict hoặc kết quả cổng cục bộ tái lập được xuống “không đo được”. Giới hạn mới áp đúng cho review khác SHA, cây runner lịch sử, CI không đọc, model phục vụ và byte comment ngoài kho. Đặc biệt, `efa397e` và `c0a5cbe` có cùng tree `f9897f6dba19484900776d7af7e9b042070d4ce1`; điều đó xác nhận nội dung Git, không biến review tại `98ef1f1` thành review cho `efa397e`, cũng không xác định synthetic tree của lượt CI. Lỗi còn lại vẫn là nhận quá mức, không phải phủ nhận bằng chứng đo được.

**Kiểm doctrine độc lập:** kiểm kê **76/76 tệp tracked dưới `docs/`**, quét `land evidence`, `bookkeeping`, `PR riêng`, `PR kế`, `PR tiếp`, `kế nhiệm`, `hậu.merge`, rồi đọc ngữ cảnh hit liên quan. `PROTOCOL:466–488` quy định bản ghi/evidence bền; `ADR-0034:17–21` đòi bookkeeping/hậu kiểm; `PROTOCOL:727–737` đòi kiểm từng mục lease. Không câu nào buộc chính hồ sơ sinh PR kế nhiệm. `ADR-0027:15` và `KE_HOACH_TRIEN_KHAI_PROTOCOL_DA_PHIEN.md:20,138` nói draft land PR **của Mission**, khác đối tượng với PR kế nhiệm **cho bản ghi evidence**. Không có căn cứ bác việc điều phối chấp nhận finding thứ năm, hoặc đòi ADR miễn trừ quy tắc chưa tìm thấy. Kết luận giới hạn ở snapshot được cấp.

## BẢNG ĐO

Lệnh/rc/dữ liệu ở [commands.json](phep-do/commands.json), [gates.json](phep-do/gates.json), cùng các tệp liên kết dưới đây. Cổng tái chạy từ clone dùng object cục bộ, ngoài cây review; setup ở [rig.json](phep-do/rig.json). `core.abbrev=7`, Python 3.11.15, Git 2.43.0, actionlint 1.7.7, ShellCheck 0.9.0. Git protocol của tiến trình cổng giới hạn `file`. Các lượt cổng dưới đây là tái đo hiện tại, không hồi tố thành log lịch sử của điều phối.

| khẳng định · nguồn | hồ sơ khai | tôi đo được | ĐO ĐƯỢC hay KHÔNG ĐO ĐƯỢC | khớp? |
|---|---|---|---|---|
| Gói: head/tree/sạch/độ sâu | Exact head, không nông | Đúng SHA/tree trên; detached; shallow=false; **0/0 byte** porcelain, **0/0 ref replace**; root commit `394e93468fc8d84ec20938e6df8fb7ab72b2cc37`. [preflight](phep-do/preflight.json) | ĐO ĐƯỢC | Có |
| Bản sao và manifest | L tại head; hiện vật có băm | **1/1 cặp** BAN/L nguyên byte; **3.183/3.183 tệp** khớp manifest. [manifest](phep-do/manifest.json) | ĐO ĐƯỢC | Có; không xác thực người tạo |
| Ref gói | **314/314 ref nhánh** | **314/314 cặp tên–OID** khớp cây, mirror và từng TSV; so tập. [refs](phep-do/refs.json) | ĐO ĐƯỢC trong gói; máy chủ KHÔNG ĐO ĐƯỢC | Có với snapshot |
| Diff `a48f576..9238606` | **1/1 tệp**, **92/92 dòng thêm**, **24/24 dòng bớt** | Git numstat/shortstat khớp; patch **13.224/13.224 byte**, numstat **40/40 byte** khớp hiện vật. [diffs](phep-do/diffs.json), [additional](phep-do/additional.json) | ĐO ĐƯỢC | Có |
| Toàn PR #490 so `c0a5cbe` | Chỉ thêm L | **1/1 tệp thêm**, **382/382 dòng thêm**, **0/0 dòng bớt**. [diffs](phep-do/diffs.json) | ĐO ĐƯỢC | Có |
| L:33–45, sau `9a99dd8` | **5/5 commit**; **14/14 tệp**, **3.135/3.135 dòng thêm**, **132/132 dòng bớt** | Git liệt kê đúng `08b4c0e`, `45bd80e`, `98ef1f1`, `f7fe802`, `efa397e`; diff khớp. [diffs](phep-do/diffs.json) | ĐO ĐƯỢC | Có |
| L:43–44, `08b4c0e` sửa L480/L487 | **105/105 dòng đổi**; **108/108 dòng đổi** | L480 thêm **57/57 dòng**, bớt **48/48 dòng**; L487 thêm **62/62 dòng**, bớt **46/46 dòng**. “Dòng đổi” là tổng thêm+bớt. | ĐO ĐƯỢC | Có |
| L:43,76–77, finding lượt đầu | **1/1 P1**, **4/4 P2**, **6/6 P3** | **11/11 tiêu đề finding** trong verdict đúng phân bố. Việc vá hết từng finding là mệnh đề khác: lượt sau còn khai chưa đóng/phát sinh. [reviews](phep-do/reviews.json) | ĐO ĐƯỢC số finding | Có; không hiểu thành tất cả đã đóng |
| L:103–110, từ `98ef1f1` tới `efa397e` | **2/2 commit**, **8/8 tệp**, **2.189/2.189 dòng thêm**, **4/4 dòng bớt** | Đúng `f7fe802`, `efa397e` và các số diff. [diffs](phep-do/diffs.json) | ĐO ĐƯỢC | Có |
| L:103, hiện vật đo | **4/4 tệp đo** cộng verdict | Đúng `bo-sot.json`, `comments.json`, `tables.json`, `bang-chu-thich-do-lai.tsv`, cộng verdict. | ĐO ĐƯỢC | Có |
| L:107–110, so gói gợi ý | **2/2 tệp**, **1/1 hunk khác**, phần đổi tên **0/0 dòng lệch** | Đọc được diff thực của README/receipt; khóa `bon_loi…` chứa **4/4 phần tử**. Thiếu `GOI-VA.md` và tệp gợi ý gốc nên không tái lập so hunk/byte với gợi ý. [source-boundaries](phep-do/source-boundaries.json), [additional](phep-do/additional.json) | ĐO ĐƯỢC bản áp; phép so gợi ý KHÔNG ĐO ĐƯỢC | Chưa xác thực phép so |
| L:55–67, merge và receipt | **2/2 cha**, **5/5 receipt đổi**, **5/5 neo canonical_ancestry** | Cha đúng `f4d74fe…`, `efa397e…`; **5/5 receipt** đúng loại neo, blob/hash và ancestry trên head/merge. [anchors](phep-do/anchors.json), [graph](phep-do/graph.json) | ĐO ĐƯỢC | Có; không tuyên mọi ref giữ object đều mất khi squash |
| L:71–91, lượt review và verdict | **2/2 lượt**; lượt sau approve, **4/4 P3** | **2/2 verdict** đúng SHA/kết luận; lượt sau **0/0 P1**, **0/0 P2**, **4/4 P3**. [reviews](phep-do/reviews.json) | ĐO ĐƯỢC hiện vật; runtime KHÔNG ĐO ĐƯỢC | Có về nội dung |
| L:80–90, trạng thái slug | **11/11 slug**: **9/9 đã vá**, **0/0 vá hờ**, **1/1 sinh lỗi**, **1/1 chưa vá** | Regex dòng slug khớp tập/phân bố; regex tiêu đề finding riêng cho **4/4 tiêu đề**. [reviews](phep-do/reviews.json) | ĐO ĐƯỢC | Có |
| L:76–77, thời lượng | 1559,927 giây; 982,697 giây | Receipt có cùng scalar, tự ghi nguồn `run.json` ngoài kho. Không có runtime gốc để đo thời lượng hay số lời gọi API. | KHÔNG ĐO ĐƯỢC sự kiện | Chỉ khớp lời khai |
| L:129,180–184, review head merge | KHÔNG THỎA, not_run | **1/1 phép so SHA** cho false; trạng thái đúng `KHONG_THOA`. [source-boundaries](phep-do/source-boundaries.json) | ĐO ĐƯỢC từ gói | Có; không loại trừ review ngoài gói |
| L:143–158, checkout CI | Chưa xác thực exact head; cấu hình **1/1 checkout** không ref | Parse workflow xác nhận; selftest PR không sinh evidence exact identity. [source-boundaries](phep-do/source-boundaries.json) | ĐO ĐƯỢC cấu hình; runner KHÔNG ĐO ĐƯỢC | Có với giới hạn mới |
| L:145,158–169, run/timing GitHub | success; thời lượng lần lượt 1411 giây, 1541 giây, 23 giây; run IDs; **2/2 review** trong log được thuật lại | Thiếu API/run JSON. Không xác thực run `34366297752`/`34363322760`, timing, lần chạy lại, review count hoặc lý do đỏ. | KHÔNG ĐO ĐƯỢC | Không đủ để công nhận pass |
| L:21–39,49–61, approval/operator/CAS | Approval `5155979035` tại `efa397e`, dismissal `5154728489`, merge lúc `14:51:22Z` | Git xác nhận merge object, committer time đổi UTC đúng `2026-09-09T14:51:22Z`. Không xác thực APPROVED/DISMISSED/COLLABORATOR/merged_by/CAS hoặc nhân quả dismissal. | ĐO ĐƯỢC Git; API KHÔNG ĐO ĐƯỢC | Tách nguồn |
| L:173,211,259, receipt gate | **94/94 receipt** = **41/41 v2 đạt** + **11/11 legacy** + **42/42 nợ**; **0/0 vi phạm**, **0/0 chưa đo** | Tự chạy CLI trên **2/2 checkout** `efa397e`, `c0a5cbe`: đúng phân bố, `TỔNG: ĐẠT`, rc=0. [gates](phep-do/gates.json) | ĐO ĐƯỢC bằng tái chạy | Có; không phải tất cả đạt v2 |
| L:175,213,261, doctrine-scan | **7/7 tệp**, **0/0 chỗ chép** | **2/2 lượt tái chạy** head/merge có stdout sạch, đúng số. [gates](phep-do/gates.json) | ĐO ĐƯỢC | Có |
| L:177,215,262, adr-song | **46/46 ADR**, **46/46 dòng bảng**, ngoại lệ ADR-0016 | **2/2 lượt tái chạy** xác nhận cả số và ngoại lệ. [gates](phep-do/gates.json) | ĐO ĐƯỢC | Có |
| L:179,217,262, doc-claims | ok:true; **106/106 tệp**, **0/0 cờ cứng**, **367/367 advisory** | **2/2 lượt tái chạy** có cùng JSON summary, ok:true; roots không gồm ops/. [head](phep-do/efa397e-doc-claims.stdout), [merge](phep-do/c0a5cbe-doc-claims.stdout) | ĐO ĐƯỢC | Có; không chứng nhận prose L |
| L:196–209, Git sau merge | Không nông; **1.879/1.879 commit**; head vào master; **0/0 commit** nhánh ngoài master | Đo `c0a5cbe`/`refs/heads/master` khớp, tính cả chính commit; ancestry đúng; nhánh land-480 không còn commit ngoài master snapshot. [graph](phep-do/graph.json) | ĐO ĐƯỢC | Có |
| L:196–209, tên ref | origin/master | Gói chỉ cấp refs/heads/*; origin/master trả rc=128. Dùng `refs/heads/master=c0a5cbe…` đã đối chiếu TSV; không sửa ref cây review. | ĐO ĐƯỢC | Khác namespace rig, không phải sai lịch sử |
| L:219,262, ShellCheck | 0.9.0, rc=0 | Cùng script tại merge: JSON `[]`, **1/1 tệp kiểm**, **0/0 diagnostic**, rc=0. [stdout](phep-do/c0a5cbe-shellcheck.stdout) | ĐO ĐƯỢC | Có, không chỉ rc |
| L:221–232,260–262, lease_publish có công cụ | **121/121 ca đạt**, **121/121 ca chạy**, **0/0 ca bỏ qua** | Suite sẵn có tại c0a5cbe khớp marker; actionlint 1.7.7, shellcheck 0.9.0. [stdout](phep-do/c0a5cbe-lease-publish.stdout) | ĐO ĐƯỢC | Có |
| L:223–228,261, thiếu actionlint | **120/120 ca đạt**, **1/1 ca đỏ** trong **121/121 ca chạy** | Cùng suite không thêm actionlint vào PATH: chỉ t33 đỏ vì thiếu công cụ, rc=1, **0/0 ca bỏ qua**. [summary](phep-do/missing-tool-summary.json) | ĐO ĐƯỢC | Có; không phải hồi quy |
| L:227, installer | Thiếu AL_VER dạng X.Y.Z thì từ chối | Ca installer sẵn có trong suite đã chạy. Không gọi installer thật/tải công cụ; dùng binary có băm từ gói. | ĐO ĐƯỢC qua suite | Có trong phạm vi offline |
| L:171,185–190,233–245, Windows/CI bỏ chờ | skipped/not_run; master dự kiến có Windows | Đọc được trigger, matrix, pull_request thiếu types. Không xác thực label/event/run thực, “lần Windows đầu tiên” hoặc runner chắc chắn đã chạy. | ĐO ĐƯỢC cấu hình; CI KHÔNG ĐO ĐƯỢC | Trạng thái đúng; prose còn vượt nguồn |
| L:141–245, trạng thái kết quả | Sửa bằng trang_thai | Duyệt **21/21 mục top-level**: còn **6/6 tiền kiểm**, **10/10 hậu kiểm**, cộng **1/1 kết quả lồng** thiếu trạng thái. Tổng **17/17 mapping kết quả thiếu trạng thái**. [schema](phep-do/schema.json) | ĐO ĐƯỢC | Chưa phủ lớp lỗi |
| L:247–277, schema/bookkeeping | Khóa bắt buộc; **5/5 phần tử** | L có **16/16 khóa mẫu**; đúng list pre/post/bookkeeping; **7/7 YAML** không khóa trùng; **6/6 hồ sơ khác** có bookkeeping. Mẫu không quy định enum/trường con trang_thai. [schema](phep-do/schema.json), [duplicates](phep-do/yaml-duplicates.json) | ĐO ĐƯỢC | Có về top-level |
| Các hồ sơ đối chiếu | So với hồ sơ cũ | **5/5 hồ sơ** khác đủ khóa mẫu; **1/1 hồ sơ** pr477-dung-goi-review-land-evidence.yaml thiếu session_id. Không lấy lỗi cũ làm chuẩn, không gán cho PR #490. | ĐO ĐƯỢC | Tiền lệ không hoàn hảo |
| L:255–257, inventory land | Base **4/4 tệp**, head **6/6 tệp**, thêm L **7/7 tệp** | ls-tree tại f4d74fe, efa397e, reviewed SHA khớp đủ danh sách; không đổi thành số lần land thành công. [graph](phep-do/graph.json) | ĐO ĐƯỢC | Có |
| L:263–269, trạng thái và con trỏ | Merged đạt, chưa tuyên landed | Semantics đúng; con trỏ thiếu no_review_head_da_merge, **1/1 phép resolve** thất bại. [source-boundaries](phep-do/source-boundaries.json) | ĐO ĐƯỢC | Sai tham chiếu, P3 |
| L:283–288, phủ bảng | **526/526 lá YAML**, **2/2 Markdown**, **242/242 lá JSON**, **62/62 comment** | Tái đếm nguồn bằng parse/span scalar, số khớp ở 98ef1f1, efa397e, reviewed SHA. **3/3 verdict lịch sử** được dẫn cùng mang slug này. Thiếu TSV gốc nên chưa chứng nhận không lá bị cắt/khớp từng hàng chỉ từ tables.json. [coverage](phep-do/coverage.json), [additional](phep-do/additional.json) | ĐO ĐƯỢC nguồn; so bảng gốc KHÔNG ĐO ĐƯỢC | Số nguồn khớp |
| L:293–295, prompt cũ/diff | Prompt khai **560/560 dòng thêm**; Git **950/950 dòng thêm**, **132/132 dòng bớt**, **8/8 tệp**; thiếu **390/390 dòng** | Git tái đo đúng các số mới; phép trừ số được thuật lại đúng 390/390 dòng. Prompt gốc không có trong kho để xác thực số 560 đã in. Prompt hiện tại đúng. | ĐO ĐƯỢC Git/phép tính; prompt cũ KHÔNG ĐO ĐƯỢC | Có phần Git |
| L:4–5, §20 | lease_publish.py ×10; packet_loop.py ×11 | Hàng protocol:1136 ghi đúng **10/10 lần nhắc**, **11/11 lần nhắc** ở ô có nhắc. Đọc hàng lịch sử, không tái chứng minh độ phủ enforcement. [doctrine](phep-do/doctrine.json) | ĐO ĐƯỢC lời dẫn | Có |
| L:301–303, chuỗi | **6/6 ID PR**; không sinh mắt xích kế tiếp | Chuỗi đúng **6/6 ID**; local history có **5/5 merge message** của các PR trước #490. Không có merge #490 được định danh trong gói. Không đo được PR vắng mặt trên GitHub/tương lai. [additional](phep-do/additional.json) | ĐO ĐƯỢC chuỗi/Git; hệ quả KHÔNG ĐO ĐƯỢC | Quyết định khác hoàn tất |
| L:312–313, chi phí mỗi mắt xích | Khoảng 24 phút runner, 16 phút review, **1/1 lượt duyệt**, ít nhất **1/1 lượt review/API** | Thiếu log/usage/run JSON theo từng PR. 1411 giây ≈23,52 phút; 982,697 giây ≈16,38 phút chỉ là tính từ scalar tự khai. | KHÔNG ĐO ĐƯỢC chi phí thực | Khai vượt loại nguồn |
| L:317–330, miễn trừ | **2/2 mục miễn**; duyệt khác danh tính còn bắt buộc | YAML đủ **2/2 mục**; prompt xác nhận quyết định chủ kho. Miễn CI không miễn duyệt. Hệ quả merge/không PR kế tiếp chưa có bằng chứng trong gói. | ĐO ĐƯỢC nội dung/chỉ thị; hệ quả KHÔNG ĐO ĐƯỢC | Phạm vi đúng |
| L:332–335, cổng duyệt | Danh tính/thẩm quyền/exact head | duyet_danh_tinh.py:239–250 so commit_id; workflow:69–74 truyền PR head vào --head-sha. Không gọi API hoặc xác thực run cong cũ. | ĐO ĐƯỢC mã/cấu hình; run KHÔNG ĐO ĐƯỢC | Có về cơ chế |
| L:338–341, nơi đọc land evidence | **2/2 tệp văn bản**, **17/17 lệnh con**, **2/2 chuỗi mô tả landed** | rg --hidden ngoài land/reviews khớp; AST đếm parser và ngữ cảnh landed đúng. Tệp: DO_VI_SAO_LEASE_482_483_CHET_20260909.md, handoff-264-review-1-claude-20260823.md. [doctrine](phep-do/doctrine.json) | ĐO ĐƯỢC phạm vi quét | Có; không chứng minh mọi gate ngoài phạm vi |
| L:137–138, lần thứ tư; L:32–48, comment đính chính | Tần suất/diễn biến phiên | Có lời tự thuật và diff; thiếu toàn transcript/comment thô để độc lập đếm chuỗi sự kiện theo thời gian. | KHÔNG ĐO ĐƯỢC lịch sử phiên/API | Không xác nhận từ lời kể |
| L:365–382, model/comment/môi trường | Model chưa xác thực; HTTP 403; evidence kế tiếp cố ý không có | Không kiểm API, argv/modelUsage, proxy, byte comment. Không dùng thiếu nguồn ngoài kho để phủ định số Git/cổng tái đo. | KHÔNG ĐO ĐƯỢC sự kiện ngoài gói | Giữ giới hạn |

Các dòng số/định danh/chữ đếm của toàn L, kể cả comment/văn xuôi, được giữ trong [numeric-lines.json](phep-do/numeric-lines.json). Bảng phân biệt số nguồn tái đếm được, phép so thiếu đầu vào và sự kiện bên ngoài; đọc lại scalar tự khai không phải đo lại sự kiện.

### ket-qua-con-thieu-trang-thai  [P2]  Kết quả còn lại chưa phân biệt trạng thái và nguồn bằng trường cấu trúc.

**Vị trí:** L:159–179,194–223; đáng chú ý pre_merge_checks[1], [2] và post_merge_checks[9].do_lan_dau_thieu_cong_cu.

L:146–151,241–245 tự đặt lý do sửa là tránh mục mang ket_qua bị đọc thành đã hoàn tất. Nhưng **17/17 mapping kết quả** khác vẫn thiếu trang_thai: **6/6 tiền kiểm**, **10/10 hậu kiểm**, **1/1 kết quả lồng**. Run GitHub cong/phản chứng vẫn chứa success trong ket_qua, không có phân loại nguồn cùng cấp; lần thiếu actionlint có rc=1 nhưng không có failed. Bộ đọc theo chính quy ước vừa công bố không phân loại nhất quán được. Không khẳng định có consumer trong kho tự chuyển state theo khóa này: đây là lỗi hợp đồng evidence của L và yêu cầu rõ của prompt, không phải enum bịa thêm vào protocol.

**Vá ở đâu/thế nào:** duyệt mọi mapping kết quả trong hai danh sách L, thêm trạng thái/nguồn thích hợp. Giữ API ở ket_qua_tho với trạng thái chưa xác thực; phân biệt số tái lập tại commit với việc đã chạy ở thời điểm lịch sử. Giữ số Git/cổng cục bộ đã tái đo; không đổi tất cả thành not_run. Lần thiếu công cụ là failed; lần có công cụ có trạng thái/bằng chứng riêng.

**Ca khóa lỗi:** [do-git-schema.py](phep-do/do-git-schema.py) đã đi đệ quy, liệt kê toàn bộ mapping thiếu trạng thái trong [schema.json](phep-do/schema.json). Sau vá, kiểm mọi mapping mang kết quả phải có trạng thái cùng cấp; bỏ một trạng thái hoặc đưa success API vào tập đạt phải bị phát hiện. Chưa thêm/chạy validator sản phẩm mới.

**Rủi ro bản vá:** passed hàng loạt nâng lời khai API thành bằng chứng; not_run hàng loạt lại phủ nhận Git/cổng thật. Cần giữ riêng giá trị, nguồn và thời điểm.

### ly-do-hau-kiem-van-tu-sinh-chuoi  [P3]  Lý do treo hậu kiểm vẫn nhận cách ghi hiện vật là hệ quả bắt buộc.

**Vị trí:** L:117–121, đối chiếu L:305–311,347–357.

Đoạn giữ lại nói hậu kiểm efa397e sẽ sinh verdict/receipt, lại đổi head, lại thêm mắt xích, rồi gọi chuỗi chưa có điều kiện dừng. Đoạn mới nói không có luật PR kế nhiệm và chuỗi đã đóng. Hậu kiểm một OID cố định không thay OID ấy; ghi hiện vật ở commit khác không làm hậu kiểm cho efa397e stale. Chỉ lựa chọn vận chuyển tự buộc xét lại commit vận chuyển mới tạo vòng lặp. Người nhận nợ có thể hiểu rằng không thể hậu kiểm nếu không mở lại chuỗi. Nếu câu thuật lại quyết định trước đây, cần neo thời điểm và nhận đó là cách làm đã chọn.

**Vá ở đâu/thế nào:** sửa chính vi_sao_ghi_thay_vi_chay_ngay: nợ chưa trả do quyết định dừng/phạm vi phiên, hoặc ghi đây là lý do lịch sử đã được đính chính. Không cần mở PR khác, không yêu cầu trả nợ ở lượt này, không thay quyết định chủ kho.

**Ca khóa lỗi:** Git cho **2/2 OID** reviewed/authorized tách biệt, giữ cố định; quét doctrine không có luật PR kế nhiệm. Soát đồng thời lý do treo nợ và đoạn đóng chuỗi, không suy ghi evidence ở commit khác thành review OID cũ hết hiệu lực. Đây là kiểm quan hệ/ngữ nghĩa; chưa có ca máy đáng tin kiểm trọn lời văn, không tuyên grep là gate ngữ nghĩa.

**Rủi ro bản vá:** sửa quá tay thành review cũ phủ commit hiện vật mới sẽ tái mở P1. Giữ efa397e chưa có review trong gói; review 98ef1f1 chỉ phủ chính SHA ấy.

### bookkeeping-tro-sai-khoa-cross-review  [P3]  Con trỏ trạng thái trong bookkeeping thiếu một cấp YAML.

**Vị trí:** L:269, phần mới thêm trong bản vá.

Địa chỉ ghi là `head_da_cross_review_khac_head_merge.dieu_kien_cross_review_CHO_HEAD_DA_MERGE`. Parse/resolve không tìm thấy khóa. Địa chỉ thật là `head_da_cross_review_khac_head_merge.no_review_head_da_merge.dieu_kien_cross_review_CHO_HEAD_DA_MERGE`, giá trị KHONG_THOA. Người/công cụ theo con trỏ không tới được trạng thái vừa thêm.

**Vá ở đâu/thế nào:** thêm cấp no_review_head_da_merge vào L:269; không di chuyển trạng thái hoặc đổi giá trị để khớp con trỏ sai.

**Ca khóa lỗi:** **1/1 phép resolve** con trỏ đang dẫn đã thất bại; địa chỉ đủ cấp đọc được KHONG_THOA, lưu ở [source-boundaries.json](phep-do/source-boundaries.json). Sau vá resolve chính chuỗi trích từ bookkeeping; thiếu cấp phải thất bại. Không cần suite sản phẩm mới cho lỗi địa chỉ này.

**Rủi ro bản vá:** kéo khóa ra cấp khác có thể tạo trạng thái song song hoặc làm chỉ dẫn cũ sai. Sửa con trỏ là nhỏ nhất.

### van-xuoi-do-duoc-van-vuot-nguon  [P3]  Ngoài mục CI vẫn có đoạn nhận lời khai hoặc dự kiến là phép đo.

**Vị trí:** L:107–110,236–240,312–321.

L:312 gọi chi phí mỗi mắt xích là “ĐO ĐƯỢC thật”, nhưng runtime scalar ở receipt tự ghi thiếu run.json và CI thiếu JSON/log. L:320 gọi merge #490 và PR kế tiếp vắng mặt là hệ quả đo được trong gói trước merge; master còn c0a5cbe, không có merge #490 được định danh hay API PR. L:236–240 suy on:push thành runner vẫn chạy/lần Windows đầu tiên. L:107–110 nhận số hunk so gợi ý là đo được nhưng thiếu đầu vào gợi ý. Đây là kiểu mất giới hạn nguồn mà bản vá CI vừa sửa. Không phủ nhận số từng được điều phối quan sát; reviewer không có nguồn để đối chứng phần gọi là phép đo.

**Vá ở đâu/thế nào:** đánh dấu so gợi ý/runtime là attestation nếu không giữ đầu vào; ghi chi phí là ước tính từ scalar thuật lại, không tổng quát cho mỗi PR. Để hệ quả #490 ở thì dự kiến/cần đọc lại; phân biệt workflow được cấu hình chạy với runner đã chạy. Giữ số Git/cổng tái lập được. Muốn giữ chữ đo được thì bổ sung đúng nguồn gốc và phạm vi từng run/commit.

**Ca khóa lỗi:** đã parse trigger/matrix/checkout, kiểm inventory và lịch sử Git; lưu [source-boundaries.json](phep-do/source-boundaries.json), [additional.json](phep-do/additional.json). Soát cặp mệnh đề–nguồn: thiếu nguồn sự kiện thì không gọi đã quan sát. Chưa có ca máy kiểm trọn ngữ nghĩa văn xuôi; không bịa CI log làm đối chứng.

**Rủi ro bản vá:** hạ mọi thứ xuống không đo được tạo lỗi ngược. Chỉ hạ sự kiện/phép so thiếu nguồn; giữ SHA, cha, ancestry, numstat, số lá nguồn, kết quả tái chạy và nội dung cấu hình là ĐO ĐƯỢC.

## GIỚI HẠN

- **Không mạng.** Mọi khẳng định GitHub API/CI — approval/dismissal, run/timing/conclusion, event/label, runner checkout, merged_by, comment byte, quyền thật, CAS đã gửi — đều **KHÔNG ĐO ĐƯỢC** trong lượt này. Ref chỉ được đối chiếu nội bộ gói, không xác thực máy chủ hiện tại hoặc PR vắng mặt.
- Cổng đã chạy là tái đo commit cố định, không phải log tiền/hậu kiểm lịch sử, không chứng minh model/session identity. Thiếu run.json/argv/usage/log runtime của review cũ; thiếu gói gợi ý, TSV cấu trúc gốc và prompt cũ để so byte. Đọc kết quả cũ không thay phép so thiếu đầu vào.
- Đã chạy cổng ngắn được hồ sơ nêu, ShellCheck và suite lease_publish sẵn có trên Linux, gồm đối chứng thiếu/có actionlint. Không chạy full tl.py --selftest, Windows, CI hoặc deploy; không tuyên các cổng ấy pass. Doc-claims không quét prose ops/land; receipt gate không xác thực danh tính hoặc cấp quyền land.
- Kết luận không có luật PR kế nhiệm giới hạn ở docs của reviewed SHA và ngữ cảnh liên quan đã đọc. Không sửa doctrine, không thêm ngoại lệ, không yêu cầu mở lại chuỗi.
- Giữ cay-kho chỉ đọc; không commit/push/checkout/config trong cây ấy. Chạy thử có thể ghi nằm ở clone tạm ngoài cây. Cuối lượt head/tree giữ nguyên, **0/0 byte** porcelain, **0/0 hiện vật nguồn lệch băm**, **0/0 commit mới** trong cây review. [final-integrity.json](phep-do/final-integrity.json). Verdict không cấp quyền merge, không chứng nhận landed/complete cho #489/#490.
