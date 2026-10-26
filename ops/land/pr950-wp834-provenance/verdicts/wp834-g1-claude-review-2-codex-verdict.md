Verdict: request_changes
Reviewed commit: 0b8d48c5e221edcedcf3a2c31b444ed33a1619d8
Spec sha256: c57ef4d86592218729b811efede7909803d75b6d18ca0d0c3e5059848b44a9d2; Chung sha256: 4e3d1e1b3f6a0b60b96ad7b70f0ece97eca4bb3d6d10defeab1cd24ac6d1cbf0

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn: `tham-chieu/VERDICT-luot1.md`, SHA-256 `cc5621187bccd6e8e63e37ee660d7eb92c26eb88d6090122e3892cfa501b5e0e`, review commit `17a3714fc8d150bd49a8dd26af29364c1a0bbe4c`. Đã đọc cả diff base→head và diff bản vá 17a3714→0b8d48c. Script cũ không được cung cấp; các probe sau được dựng lại từ mô tả, chạy trên bản sao riêng. Không nhận lời khai executor làm bằng chứng đóng lớp.

| slug lượt 1 | kết luận lượt 2 | phép đo đã chạy và giới hạn |
|---|---|---|
| `ci-attempt-provenance-missing` | **đóng — ĐÃ VÁ THẬT** đối với cơ chế check khác che check được job nối | `PROBES.jsonl`: 3 control check đỏ/sai head/queued và 9 biến thể thêm check 999 xanh cùng suite nhưng khác app/kho hoặc cùng app đều rc=12. Chốt mới buộc chính check được nối là ID mới nhất trước khi gọi gate; gate kiểm head/status/conclusion của chính bản đó. Run mới đỏ và attempt mới với jobs cũ cũng bị bác. Lỗi kiểu dữ liệu jobs mới phát hiện được đếm riêng bên dưới, không phải cơ chế chọn lại check đã vá. |
| `conflicting-evidence-overwrite` | **đóng — ĐÃ VÁ THẬT** | Cùng check ID nhưng khác app, URL kho, status hoặc conclusion đều rc=12; cùng comment ID khác body và cùng run ID khác path đều rc=12. Bản lặp giống hệt được nhận; cùng ID ở hai endpoint vẫn được nhận với H đúng. Không còn ghi đè bản mâu thuẫn trong phạm vi đã đo. |
| `connector-verdict-incomplete` | **đóng — ĐÃ VÁ THẬT** | P0/P1/P2, Q1, `P 1`, PX, hai badge khác hạng ở cả ba endpoint đều bị bác; CHANGES_REQUESTED không hạng bị bác; review PENDING đơn độc không được tính là xong. Baseline sạch/no finding vẫn accepted. Vấn đề neo head được giữ ở slug riêng của lượt 1. |
| `connector-head-binding-incomplete` | **còn mở — VÁ HỜ, P1** | Probe cũ thiếu/sai commit_id, hậu tố `-invalid`, hai khai báo hiện hành/cũ mâu thuẫn nay rc=12; issue P1 có SHA cũ hợp lệ nay không chặn head mới. Tuy nhiên `EXTRA.jsonl` và `AMBIGUITY.jsonl` chứng minh parser còn nhận code span chứa SHA + nội dung thừa, và tiền tố có hai SHA phù hợp ngay trong readback vẫn được tính là review head hiện hành. Xem lớp F1. |
| `workflow-jobs-pagination-cross-run` | **đóng — ĐÃ VÁ THẬT** | `two_workflow_job_files` và `two_required_workflows`: 5 jobs của run 100 + 1 job của run 101, total_count 5/1 riêng, rc=0/accepted. Trường hợp workflow thứ hai thật sự nằm trong required_checks cũng xanh. Phân trang hai trang trong một tệp jobs/check-runs đều xanh; không sửa total_count thành tổng giả. |
| `accept-state-schema-incomplete` | **đóng — ĐÃ VÁ THẬT** | required_checks=[] cùng ba readback CI rỗng bị rc=8; receipt summary `{}`, p3 rỗng sai kiểu/string/null/dict/int/bad slug đều rc=8 và nguyên byte. `empty_ci` khi state hợp lệ bị rc=12. Không còn hai traceback state được mô tả ở lượt 1. |
| `required-mutation-coverage-missing` | **còn mở — VÁ HỜ, P2** | Đo đủ tám mutant sống cũ, mỗi bản chạy tất cả 38 ca r834: 7 bị giết, `omit_stop_call` vẫn 38/38. Các mutant bổ sung kiểm repo/head run, head job, tính duy nhất quyết định P3 và generation H đều SỐNG 38/38, ghi ở bảng riêng. Không suy mutant sống thành lỗi sản phẩm đang xảy ra. |

Năm lớp cũ đã đóng; hai lớp cũ còn mở. Finding mới được đếm riêng: **một lớp P2**, `ci-job-input-schema-incomplete`. Tổng còn mở: **3 lớp — 0 P0, 1 P1, 2 P2, 0 P3**. Không đạt ngưỡng approve (không còn P0/P1/P2).

## Định danh, phương pháp và phạm vi

Reviewer độc lập: Codex / họ openai, thực thi shell cục bộ qua công cụ của phiên API, transport machine; executor theo lease là Claude. Không kế thừa context executor. Assurance **mục tiêu** cross_approved, review_class sensitive; verdict âm này không tự cấp assurance, quyền push, merge hoặc land. Model/effort/session identity cấp runtime chưa được đối chiếu bằng receipt máy độc lập; không suy danh tính từ tài khoản GitHub hay nhãn lease.

Đã đọc toàn văn prompt.snapshot. Thư mục làm việc thực là `rv2/` (chứa src/, out/, tham-chieu/), không phải thư mục `runs/` chứa snapshot. Nguồn được coi read-only; mọi script, mutation, Git fixture, cache và kết quả nằm trong out/. Không truy cập mạng/GitHub. Các fetch/push/ls-remote trong fixture chỉ dùng các kho Git cục bộ thuộc out/.

`CHECKS.jsonl`: HEAD đúng dòng 2; tree `8167195dc44fcbb40a01f40baaba180dff7833ae`; origin/master `ab344da5f07cce673d97056b70b002911c4d5082`; ancestor rc=0; detached (`symbolic-ref -q HEAD` rc=1 đúng mong đợi); clone không shallow; .git là thư mục; worktree sạch. Hai hash spec đúng dòng 3. `git diff --check` rc=0. `core.abbrev=7` ở nguồn và bản sao.

| tệp trong diff ab344da→0b8d48c | thêm | xoá |
|---|---:|---:|
| .claude/dev/packet_loop.py | 170 | 1 |
| .claude/dev/packet_loop_test.py | 184 | 3 |
| docs/PROTOCOL_DA_PHIEN.md (§4) | 4 | 1 |
| Tổng | **358** | **5** |

Đúng ba tệp, 358 ≤ 450. Lease có thêm handoff chỉ trên nhánh lease, không có trong diff ứng viên; không finding về write set, kích thước hay M5. `CANDIDATE.diff` và `PATCH.diff` giữ toàn bộ hai diff đã đọc.

Kiểm tra cuối `SOURCE_INTEGRITY.json`: 5.989 tệp/link (kể cả .git) khớp theo nội dung/đích link với bản sao tạo trước test; 0 delta. Status gồm untracked và ignored rỗng; HEAD/tree đúng; diff worktree/index rc=0. `SOURCE_FINAL.json` giữ từng hash. Đây là đối chiếu snapshot đầu/cuối quan sát được, không phải chứng minh lịch sử không từng ghi rồi hoàn nguyên; sandbox cho phép ghi trong workspace nhưng mọi thao tác của review chỉ nhắm out/.

## Bảng lớp còn mở

`pl` = `.claude/dev/packet_loop.py`; `test` = `.claude/dev/packet_loop_test.py`. Dòng theo head ứng viên. Đếm theo nguyên nhân, không theo số biểu hiện.

| slug | hạng | biểu hiện file:dòng | phép đo/tái hiện đã chạy | hướng vá |
|---|---|---|---|---|
| `connector-head-binding-incomplete` (F1, cũ) | P1 | pl:2786, pl:2789, pl:2806, pl:2809 | `prefix_invalid_inside_ticks_{7,10,40}`, `prefix_second_sha_inside_ticks_{7,10,40}`: code span có SHA rồi nội dung thừa hoặc SHA thứ hai vẫn rc=0/accepted. `AMBIGUITY.jsonl`: hai SHA khác nhau có chung tiền tố 10 ký tự trong readback; claim full head hiện hành → 0, full SHA cũ → 12/chưa xong, tiền tố chung → 0/accepted. | Phân tích trọn trường có/không backtick, kiểm cặp delimiter và phần còn lại; tiền tố chỉ thành bằng chứng hiện hành nếu phân giải duy nhất. Với dữ liệu mơ hồ, yêu cầu exact SHA hoặc nguồn bổ sung có neo đúng; không tự chọn head chỉ vì startswith. |
| `required-mutation-coverage-missing` (F2, cũ) | P2 | test:8556–8735; pl:2900 và các chốt ghi trong bảng audit | `omit_stop_call` vẫn xanh 38/38; bảy mutant cũ khác bị giết đúng ca. `I5_CONTRACT.jsonl`: phép kiểm hợp đồng độc lập giết đúng omission bằng AssertionError (đòi sentinel rc=3, được 0), trong khi đầu vào hỏng vẫn bị bác trước sentinel. Kết quả mutant bổ sung bên dưới. | Thêm ca/mutant r834 cho từng chốt còn sống. Riêng I5 dùng sentinel có kiểm soát ở helper trong bản sao thử để đo call/order; không sáng tác stop condition mới cho accept. |
| `ci-job-input-schema-incomplete` (F3, mới) | P2 | pl:2832, pl:2845, pl:2849, pl:2850 | `job_type_run_attempt_True`, `job_type_run_attempt_1.0`, `job_type_run_id_100.0`: rc=0/accepted; Python coi True==1, 1.0==1, 100.0==100. Chuỗi `"1"`/`"100"` lại rc=12. `job_check_url_5000_digits`: URL đúng kho, ID là 5.000 chữ số, rc=1/ValueError tại int(m[1]), state nguyên byte. | Xác thực lược đồ job trước join: run_id/run_attempt là int thật, dương; kiểm URL như chuỗi và xử lý ID không chuyển được thành số bằng từ chối RC_GATE có kiểm soát. Không để coercion/so sánh Python thay hợp đồng provenance. |

### F1 — giới hạn chính xác và ca khoá

Bản vá đã sửa phản chứng `prefix-invalid` liền nhau của lượt 1, nhưng regex mới chỉ lấy chuỗi không có whitespace rồi `strip` mọi backtick ở hai đầu. Với trường `Reviewed commit: ` + code span chứa `<head> invalid` hoặc `<head> <sha-khac>`, nó chỉ lấy phần đầu; phần còn lại trong cùng trường biến mất. Không kết luận rằng mọi prose đi sau SHA trần đều sai; phản chứng ở đây là **một trường được bao bằng backtick nhưng nội dung bên trong không phải một SHA**.

Ngoài ra, `_neo_connector` chỉ xét `head.startswith(token)` riêng từng item. Trong phép đo ambiguity, một review CHANGES_REQUESTED/P1 có commit_id khác nhưng chung tiền tố với head. Không có review hoàn tất mang exact head hiện hành. Issue summary chỉ khai tiền tố chung. Sản phẩm vẫn suy summary là kết luận của head hiện hành và bỏ review cũ. SHA thứ hai là dữ liệu R tổng hợp để kiểm nhất quán; không khai đã tìm collision trên Git thật. Đây là mơ hồ ngay trong R đã cấp; không yêu cầu máy tự tải GitHub, không giả định phải chống executor cố ý gian lận, và không yêu cầu P1 trên head cũ luôn chặn head mới. Control exact current SHA được nhận; control exact old SHA bị bác vì thiếu kết luận hiện hành.

Vá ở parser `_neo_connector` và bước tập hợp head trong `_doc_connector`; bảo vệ bằng baseline exact SHA, tiền tố duy nhất, code span đúng và head cũ hợp lệ, sau đó đổi riêng delimiter/nội dung hoặc thêm head có chung tiền tố. Mutant bỏ kiểm trọn trường/độ duy nhất phải làm ca âm rc=0 để bị giết đúng lý do. Rủi ro bản vá: siết quá mức có thể chặn output connector dùng tiền tố hợp lệ hoặc prose thông thường; giữ đối chứng dương cho các dạng thực sự được hợp đồng hỗ trợ. Không cung cấp patch sửa gate/authority.

### F2 — coverage khác lỗi hành vi

Helper hiện tại không có nhánh dừng riêng cho `cua="accept"`; lời gọi ở pl:2900 có thật và nằm sau validation. Vì vậy **không báo rằng sản phẩm hiện bỏ một stop condition cụ thể**. Lỗi là nghiệm thu I5 không được suite/mutant bảo vệ dù đã được nêu đích danh ở lượt 1.

`EXTRA.py` chỉ chèn sentinel `_die(RC_TRAN, "REVIEWER_I5_SENTINEL")` vào helper trên bản sao: input hợp lệ đến sentinel rc=3; connector/H/quyết định P3 hỏng bị rc=12/11/2 trước sentinel và giữ nguyên byte. `I5_CONTRACT.py` bỏ lời gọi trên bản sao đó: input hợp lệ trở thành accepted/rc=0 và assertion mục tiêu đỏ, các control input hỏng vẫn đúng. Đây là dữ liệu kiểm hợp đồng đã chạy, không phải patch sản phẩm hay quy tắc dừng mới.

Vá test tại nhóm r834; mỗi chốt thêm baseline đủ H/Đ, một yếu tố âm, một mutant duy nhất và kiểm rc + thông điệp + byte. Rủi ro: sentinel không đúng vị trí có thể tạo tín dụng giả, hoặc test âm chết trong fixture trước khi tới accept; giữ control hợp lệ và control lỗi muộn. Mutant sống bổ sung không tự động có hạng sản phẩm riêng: các probe riêng đã xác nhận chốt thật đang từ chối đúng.

### F3 — phạm vi mới, không nhập nhầm lớp cũ

Đây là lược đồ dữ liệu job trước phép nối, khác cơ chế chọn lại check-run ngoài tập đã xác minh của `ci-attempt-provenance-missing` lượt trước (đã vá). `_trang_du` kiểm id của **phần tử**, nhưng không kiểm kiểu run_id/run_attempt. So tuple Python nhận boolean/float như số nguyên rồi cấp accepted và ghi state. Lỗi URL là cùng ranh giới đầu vào jobs chưa có parser/từ chối có kiểm soát: regex cho chuỗi chữ số không giới hạn, sau đó int() có thể ném ValueError. Không tính traceback là một mutant bị giết; không nói trường hợp traceback làm đổi state.

Ca khoá: baseline job run_attempt=1/run_id=100; đổi đúng run_attempt thành true hoặc 1.0, run_id thành 100.0, đòi rc=12 và state nguyên byte; đối chứng integer vẫn accepted. Thêm ca URL chuỗi số quá dài phải bị từ chối có kiểm soát và không traceback. Mutant gỡ chốt kiểu phải làm boolean/float trở lại accepted, không lấy crash làm tín dụng. Rủi ro bản vá: dùng isinstance(int) vẫn nhận bool; tự ép int() sẽ giữ lỗi nhận float; siết schema không nên yêu cầu các trường GitHub không nằm trong hợp đồng R.

## Tám đột biến sống lượt 1 đo lại trên head mới

Mỗi mutant nằm dưới `audit_mutants/`, neo xuất hiện đúng một lần, compile thành công, chạy **đủ 38 ca r834**. Cặp neo/thay và toàn bộ lỗi không cắt ngắn nằm trong `AUDIT_MUTANTS.jsonl`/script.

| mutant lượt 1 | kết quả lượt 2 | lý do/ca phân biệt |
|---|---|---|
| `omit_kiem_gate` | GIẾT; 37/38 ca còn xanh | `r834_check_noi_do`: AssertionError: r834 accept: đòi rc=12, được rc=0 |
| `oldest_run` | GIẾT; 37/38 ca còn xanh | `r834_run_moi_nhat_do`: AssertionError: r834 accept: đòi rc=12, được rc=0 |
| `omit_job_attempt` | GIẾT; 37/38 ca còn xanh | `r834_attempt_moi_job_cu`: AssertionError: r834 accept: đòi rc=12, được rc=0 |
| `omit_connector_envelope` | GIẾT; 37/38 ca còn xanh | `r834_envelope_head_khac`: AssertionError: r834 accept: đòi rc=12, được rc=0 |
| `omit_total_count` | GIẾT; 37/38 ca còn xanh | `r834_trang_thieu`: AssertionError: r834 accept: đòi rc=12, được rc=0 |
| `omit_ref_exact_cover` | GIẾT; 37/38 ca còn xanh | `r834_refs_thua`: AssertionError: r834 accept: đòi rc=11, được rc=0 |
| `omit_stop_call` | SỐNG 38/38 | Không ca nào phân biệt khi gỡ chốt. |
| `omit_job_check_url_repo` | GIẾT; 37/38 ca còn xanh | `r834_job_url_kho_khac`: AssertionError: r834 accept: đòi rc=12, được rc=0 |

## Đột biến bổ sung lượt 2

| mutant | chốt | kết quả trên đủ 38 ca |
|---|---|---|
| `omit_run_repository` | repo của workflow run | SỐNG 38/38 |
| `omit_run_head` | head của workflow run | SỐNG 38/38 |
| `omit_job_head` | head của job | SỐNG 38/38 |
| `omit_connector_p3_unique_decision` | một quyết định duy nhất cho mỗi nguồn/slug P3 | SỐNG 38/38 |
| `omit_receipt_generation` | generation receipt H | SỐNG 38/38 |

`PROBES.jsonl` có control bác run sai repo/head, job sai head, quyết định P3 trùng và H sai generation trên sản phẩm gốc. Việc nhóm r834 thiếu ca được ghi vào F2, không báo sai rằng chốt sản phẩm không tồn tại. Mutant generation sửa helper dùng chung; nhóm r812 có ca generation âm, nên kết quả 38/38 chỉ chứng minh thiếu ca ở consumer connector/r834, không khẳng định toàn suite legacy không kiểm generation.

## Đối chiếu từng ca bắt buộc nghiệm thu

38/38 baseline r834 xanh. 35 mutant khai báo tạo 38 quan hệ mutant→ca, đều GIET bằng AssertionError đúng mục tiêu, không SONG/TIN_DUNG_GIA. Tên trong bảng được lược tiền tố `r834_`; log giữ tên đầy đủ. Những mutant làm hỏng đường dương bị giết bằng từ chối có kiểm soát đúng thông điệp; không tính SyntaxWarning có sẵn hay lỗi setup.

| mục bắt buộc | ca | mutant | kết quả/lý do đã đọc |
|---|---|---|---|
| sạch lop=[] và connector sạch | sach_accepted | bo_ket_luan_issue_comment | baseline accepted; mutant đòi 0, được 12, connector chưa xong |
| đầu remote khác pending | dau_nhanh_lech | bo_dau_nhanh_remote | baseline 5/≠pending; mutant được 0 |
| check bắt buộc vắng | check_vang; job_tro_check_khong_co | job_vang_bo_qua; noi_check_theo_ten | baseline 12/VẮNG hoặc không trỏ check-run; mutant được 0. Ca đầu xoá job; ca sau trỏ ID check không có. Probe độc lập còn xoá hẳn check-run. |
| cùng tên từ app khác | check_app_khac | bo_app | 12/không từ app → 0 |
| cùng tên, workflow khác cùng app | check_workflow_khac | bo_path_workflow | 12/VẮNG → 0 |
| attempt mới đang chạy, check cũ xanh | rerun_dang_chay | bo_attempt_moi_nhat | 12/chưa xanh → 0. Mutant phối hợp hai chốt; bản vá còn thêm attempt_moi_job_cu + bo_khop_attempt_job để bảo vệ riêng job attempt. |
| check-run kho khác | check_kho_khac | bo_kho_check_run | 12/kho khác → 0 |
| PR khác cùng head | pr_khac_cung_head | bo_neo_pr_phan_tu | 12/không thuộc → 0; envelope có ca/mutant riêng |
| review PENDING không xong | review_pending | pending_la_xong | 12/chưa xong → 0 |
| review CHANGES_REQUESTED P1 | review_changes_p1 | bo_finding_review | 12/còn P1 → 0 |
| issue comment P1 | issue_comment_p1 | bo_finding_issue_comment | 12/còn P1 → 0 |
| cùng ID P1 rồi P3 | cung_id_hai_noi_dung | bo_nhat_quan_id | 12/hai nội dung → 0 |
| cùng run ID khác path | run_cung_id_khac_path | bo_nhat_quan_id | 12/hai nội dung → 0 |
| offline P3 thiếu quyết định | p3_offline_thieu_qd | bo_p3_offline | 2/P3 còn mở → 0 |
| connector P3 thiếu quyết định | p3_connector_thieu_qd | bo_p3_connector | 2/P3 còn mở → 0 |
| connector P3 thiếu slug H | p3_connector_khong_slug | khoa_id_so | 11/đòi --bien-nhan-connector → 0; refs sai có refs_thua/bo_phu_dung_refs bổ sung |
| bằng chứng dương rỗng | bang_chung_duong_rong; state_required_checks_rong | bo_bang_chung_duong; bo_luoc_do_state | connector rỗng: 12→0; state thiếu checks: 8→0. Probe CI rỗng nhưng state hợp lệ rc=12. |
| đầu vào hỏng giữ state | dau_vao_hong_state_nguyen | ghi_truoc_khi_doc | baseline JSON hỏng rc=12, byte bất biến; mutant đỏ chính AssertionError “I4: state đổi sau khi accept từ chối” |

Toàn bộ 35 kết quả khai báo (gồm các ca vá ngoài danh sách bắt buộc) giữ nguyên dưới đây để đối chiếu tên ca, lớp ngoại lệ và lý do. Tên ở bảng trên được lược tiền tố cho gọn; log ghi tên đầy đủ. Một thông điệp stderr dài bị runner tham chiếu cắt ở 200 ký tự; `oldest_run` trong audit giữ bản đầy đủ và xác nhận đúng assertion rc, không traceback.

```text
MUT r834_bo_ket_luan_issue_comment: r834_sach_accepted=GIET:AssertionError: r834 accept: đòi rc=0, được rc=12; stderr='connector chưa xong trên f7510bca1bc4ed8d9a28ad907030192ea7404d35: không review hoàn tất/kết luận nào của chatgpt-codex-connector[bot]'
MUT r834_bo_ref_connector_h: r834_p3_du_quyet_dinh=GIET:AssertionError: r834 accept: đòi rc=0, được rc=11; stderr="bảng lớp H phải phủ ĐÚNG từng (endpoint, id) P3 của connector [('review_comments', 11)], mỗi cặp một lần"
MUT r834_bo_dau_nhanh_remote: r834_dau_nhanh_lech=GIET:AssertionError: r834 accept: đòi rc=5, được rc=0; stderr=''
MUT r834_job_vang_bo_qua: r834_check_vang=GIET:AssertionError: r834 accept: đòi rc=12, được rc=0; stderr=''
MUT r834_bo_app: r834_check_app_khac=GIET:AssertionError: r834 accept: đòi rc=12, được rc=0; stderr=''
MUT r834_bo_path_workflow: r834_check_workflow_khac=GIET:AssertionError: r834 accept: đòi rc=12, được rc=0; stderr=''
MUT r834_bo_attempt_moi_nhat: r834_rerun_dang_chay=GIET:AssertionError: r834 accept: đòi rc=12, được rc=0; stderr=''
MUT r834_bo_kho_check_run: r834_check_kho_khac=GIET:AssertionError: r834 accept: đòi rc=12, được rc=0; stderr=''
MUT r834_bo_neo_pr_phan_tu: r834_pr_khac_cung_head=GIET:AssertionError: r834 accept: đòi rc=12, được rc=0; stderr=''
MUT r834_pending_la_xong: r834_review_pending=GIET:AssertionError: r834 accept: đòi rc=12, được rc=0; stderr=''
MUT r834_bo_finding_review: r834_review_changes_p1=GIET:AssertionError: r834 accept: đòi rc=12, được rc=0; stderr=''
MUT r834_bo_finding_issue_comment: r834_issue_comment_p1=GIET:AssertionError: r834 accept: đòi rc=12, được rc=0; stderr=''
MUT r834_bo_nhat_quan_id: r834_cung_id_hai_noi_dung=GIET:AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' · r834_run_cung_id_khac_path=GIET:AssertionError: r834 accept: đòi rc=12, được rc=0; stderr=''
MUT r834_bo_p3_offline: r834_p3_offline_thieu_qd=GIET:AssertionError: r834 accept: đòi rc=2, được rc=0; stderr=''
MUT r834_bo_p3_connector: r834_p3_connector_thieu_qd=GIET:AssertionError: r834 accept: đòi rc=2, được rc=0; stderr=''
MUT r834_khoa_id_so: r834_p3_connector_khong_slug=GIET:AssertionError: r834 accept: đòi rc=11, được rc=0; stderr=''
MUT r834_bo_bang_chung_duong: r834_bang_chung_duong_rong=GIET:AssertionError: r834 accept: đòi rc=12, được rc=0; stderr=''
MUT r834_ghi_truoc_khi_doc: r834_dau_vao_hong_state_nguyen=GIET:AssertionError: I4: state đổi sau khi accept từ chối
MUT r834_bo_kiem_gate: r834_check_noi_do=GIET:AssertionError: r834 accept: đòi rc=12, được rc=0; stderr=''
MUT r834_bo_check_moi_nhat: r834_check_noi_do_bi_che=GIET:AssertionError: r834 accept: đòi rc=12, được rc=0; stderr=''
MUT r834_check_run_khong_nhat_quan: r834_check_cung_id_khac_app=GIET:AssertionError: r834 accept: đòi rc=12, được rc=0; stderr=''
MUT r834_bo_khop_attempt_job: r834_attempt_moi_job_cu=GIET:AssertionError: r834 accept: đòi rc=12, được rc=0; stderr=''
MUT r834_run_cu_nhat: r834_run_moi_nhat_do=GIET:AssertionError: r834 accept: đòi rc=12, được rc=0; stderr="CẢNH BÁO: 'gate (ubuntu-latest)' có 1 run ở suite khác (300) — bỏ qua\nCẢNH BÁO: 'gate-cong-cu-gop (ubuntu-latest)' có 1 run ở suite khác (30
MUT r834_bo_kho_url_job: r834_job_url_kho_khac=GIET:AssertionError: r834 accept: đòi rc=12, được rc=0; stderr=''
MUT r834_noi_check_theo_ten: r834_job_tro_check_khong_co=GIET:AssertionError: r834 accept: đòi rc=12, được rc=0; stderr=''
MUT r834_jobs_total_toan_cuc: r834_hai_tep_jobs=GIET:AssertionError: r834 accept: đòi rc=0, được rc=12; stderr='KHÔNG ĐO ĐƯỢC: workflow_jobs: cần trang {`jobs`, `total_count`} cùng một lần lấy, id int, tập id phân biệt = total_count'
MUT r834_badge_chi_P: r834_badge_ngoai_mien_review=GIET:AssertionError: r834 accept: đòi rc=12, được rc=0; stderr=''
MUT r834_changes_khong_hang_lot: r834_review_changes_khong_hang=GIET:AssertionError: r834 accept: đòi rc=12, được rc=0; stderr=''
MUT r834_commit_thieu_la_cu: r834_review_comment_thieu_commit=GIET:AssertionError: r834 accept: đòi rc=12, được rc=0; stderr=''
MUT r834_reviewed_commit_tim_dau: r834_reviewed_commit_sai_dang=GIET:AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' · r834_reviewed_commit_mau_thuan=GIET:AssertionError: r834 accept: đòi rc=12, được rc=0; stderr=''
MUT r834_head_cu_van_chan: r834_issue_comment_head_cu_khong_chan=GIET:AssertionError: r834 accept: đòi rc=0, được rc=12; stderr='connector issue comment 21 có finding mà không neo head'
MUT r834_bo_envelope: r834_envelope_head_khac=GIET:AssertionError: r834 accept: đòi rc=12, được rc=0; stderr=''
MUT r834_bo_total_count: r834_trang_thieu=GIET:AssertionError: r834 accept: đòi rc=12, được rc=0; stderr=''
MUT r834_bo_phu_dung_refs: r834_refs_thua=GIET:AssertionError: r834 accept: đòi rc=11, được rc=0; stderr=''
MUT r834_bo_luoc_do_state: r834_state_required_checks_rong=GIET:AssertionError: r834 accept: đòi rc=8, được rc=0; stderr='' · r834_state_p3_sai_kieu=GIET:AssertionError: r834 accept: đòi rc=8, được rc=0; stderr=''
```

## I1–I11, M1–M5 và đầu vào thiết kế #812

- **I1/I2:** baseline dựng Git local thật, lease qua validator H/canon + holder + comment R, pending qua review H; accept tự ls-remote local để đo đầu nhánh. Không stub authority. Remote lệch bị bác. Các chốt lease kế thừa được 149 ca r812 kiểm lại.
- **I3:** lớp rỗng và connector sạch được nhận; thiếu bằng chứng CI/connector, check không success, hạng ngoài miền bị bác. Miền kiểu dữ liệu job còn F3. Hai badge khác hạng bị bác; hai badge P3 giống nhau được quy về cùng hạng P3 và vẫn phải có H/quyết định. Spec không đòi đếm số lần cùng badge thành hai lớp, nên không tự báo thêm finding.
- **I4:** 112 lần từ chối trong PROBES đều nguyên byte; EXTRA cũng giữ byte ở mọi lần không rc=0, gồm lỗi muộn H/quyết định và traceback URL đã tách riêng. Các input bị nhận sai ở F1/F3 chuyển accepted, nên không thể coi hợp đồng input fail-closed đã đạt toàn bộ. Không dùng traceback làm tín dụng mutant.
- **I5:** lời gọi chung có thật sau remote/CI/connector/H/quyết định. Sentinel độc lập xác nhận thứ tự; suite candidate thiếu bảo vệ lời gọi (F2). Có đọc lại connector lấy hash ở pl:2902; chưa đo race/TOCTOU, không suy thành finding mới. Không gán stop condition #813–#816 cho cửa này.
- **I6:** không có quyền phái sinh mới thuộc các packet sau; ngoài phạm vi.
- **I7/M2/M3:** đã đo đúng repo/PR/head envelope và phần tử cả ba endpoint; đủ trang theo ID từng endpoint; duplicate nguyên byte được khử trùng; khác nội dung bị bác. Hai workflow/tệp jobs hợp lệ được nhận. Run/attempt mới và job→URL→check app/kho/suite cùng gate được kiểm. Neo issue summary vẫn còn F1, schema job còn F3.
- **I8/I10/M4:** `_slug_connector` dùng lại `_du_dieu_kien_approve`, validator canon và chuẩn hoá identity. Receipt vai reviewer/approve phải khớp packet, generation hiện hành, pending_sha, spec_hash, lease/assurance/identity. Probe đổi riêng packet/generation/SHA/spec/role/verdict đều rc=11, nguyên byte. Đây là hiện vật ứng viên; chưa có hiện vật nguồn generation cũ trong scope này.
- **I11:** refs trùng/thiếu/thừa/sai endpoint/bool hoặc string ID/scalar/nested/null đều rc=11; cùng ID ở hai endpoint với refs đúng được nhận. Quyết định P3 thiếu/trùng/thừa/sai kiểu/lý do trắng/thừa trường đều rc=2. Slug lấy từ H, không dùng ID số executor đặt. H có lớp P3 không mang connector_refs không tự biến thành finding connector nếu readback không có finding tương ứng; không tự đòi mapping cho lớp ngoài tập connector đã đo. Phần connector của lớp thiết kế `findings-not-receipt-bound` đã đóng trong phạm vi đo.
- **I9:** 149/149 ca r812 xanh (bao gồm init chưa lease, đường lease cũ false, trạng thái không kích hoạt và các chốt receipt); ba ca neo đột biến/codepage xanh; 10/10 ca r929 xanh. Không chạy toàn suite nên không khai “mọi ca cũ N/N”. Diff nhánh legacy không đổi; thay summary `lop` chỉ ở đường review ADR-0054.
- **M1:** baseline sạch và P3 đủ H/quyết định accepted, accepted_sha đúng pending, ghi mốc riêng từng endpoint và digest R. Tổng M1 chưa đạt vì F1/F3; nghiệm thu mutation chưa đạt vì F2.
- **M5:** protocol chỉ sửa §4, điều kiện accept chỉ packet áp ADR-0054 đúng phạm vi.

Các lớp thiết kế #812 `connector-verdict-incomplete`, `ci-attempt-provenance-missing`, `conflicting-evidence-overwrite` đã được khép ở cơ chế được giao và đo; giới hạn neo head tách theo slug đã có lượt 1, lỗi schema job mới đếm riêng. Không dùng kết quả này để khép các packet ngoài scope.

`_che_do_0054` của #929 nhận diện ADR kích hoạt bằng cụm khai trong blob ADR, không ghim số 0055. Đặc tả wp834/phần chung không bắt buộc tên tệp kích hoạt cố định: **không thấy mâu thuẫn đặc tả ràng buộc với code hiện hành**. 10 ca r929 đo số bất kỳ, NFC, blob/tệp, đúng một khai và lỗi đọc; không dùng thiết kế g2 cũ làm luật để quay lại số 0055. Nợ P3 `ls[0] == 0` của #929 ngoài phạm vi, không phân hạng. Packet này không kích hoạt ADR-0054 trên kho thật; chỉ fixture local dựng trạng thái kích hoạt.

## Lệnh, rc và bằng chứng dương

Môi trường: Linux/Python cục bộ; `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR=<rv2>/out/tmp`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_SYSTEM=/dev/null`; runner còn cô lập config Git phạm vi lệnh. Không bytecode vào nguồn. Tất cả các lệnh sau chạy từ rv2; root test là out/review-copy.

| lệnh/phép đo | rc | bằng chứng |
|---|---:|---|
| `python -u -B tham-chieu/chay_ca_va_dot_bien.py out/review-copy r834_ r834_` | 0 | R834.log: CA 38/38, 35 mutant, 38 quan hệ GIET, không SONG/TIN_DUNG_GIA |
| `python -u -B tham-chieu/chay_ca_va_dot_bien.py out/review-copy r812_` | 0 | R812.log: CA 149/149; không chạy mutant r812 |
| `python -u -B tham-chieu/chay_ca_va_dot_bien.py out/review-copy r929_` | 0 | R929.log: CA 10/10; không chạy mutant r929 |
| `python -u -B out/CHECKS.py` | 0 | CHECKS.jsonl: OID/hash/ancestor/diff check; doctrine-scan 10/0 rc0; adr-song 55/55 rc0; neo mutant, stdout_cp1252/cp1258 đều xanh |
| `python -u -B out/PROBES.py` | 0 | 131 bản ghi, gồm 2 baseline accepted; 112 từ chối nguyên byte, không traceback; kết quả chi tiết từng input trong PROBES.jsonl |
| `python -u -B out/EXTRA.py` | 0 | 26 bản ghi; có 1 CLI rc1/ValueError được phân loại F3, 4 ca sentinel I5; không gọi tất cả là “pass” |
| `python -B out/AMBIGUITY.py` | 0 | full current rc0, full old rc12, shared prefix rc0; hai SHA và claim giữ trong AMBIGUITY.jsonl |
| `python -B out/I5_CONTRACT.py` | 0 | 4 control trên omission mutant; chỉ ca hợp lệ đổi rc3→0 làm assertion mục tiêu đỏ, 3 input hỏng vẫn từ chối trước stop |
| `python -u -B out/AUDIT_MUTANTS.py` | 0 | 13 mutant × 38 ca; 7 GIẾT đúng assertion, 6 SỐNG (1 cũ + 5 mới); không lỗi neo/compile/TIN_DUNG_GIA |

Script probe thu kết quả có thể rc=0 dù hành vi sản phẩm sai; rc/stdout/stderr/state-before/state-after của từng lần CLI được giữ riêng. Đây không phải tuyên bố mọi probe pass. Ca stdout codepage chạy trên Linux bằng encoding môi trường, không phải chứng nhận thực thi Windows.

## Giới hạn và ngoài phạm vi

Chưa chạy full suite `python .claude/dev/packet_loop_test.py` (~45 phút theo prompt), toàn bộ mutant legacy, bare Ruff, CI GitHub hoặc Windows. Các phần đó là **not_run**, không nhận N/N toàn suite từ lời khai executor. Ưu tiên selective suite, toàn bộ mutant r834, tám mutant cũ và phản chứng độc lập theo chỉ thị.

Không soạn payload đường dẫn thoát cây. Hướng thử receipt/lease qua đường dẫn vượt cây hoặc symlink ra ngoài chỉ mô tả bằng lời tại đây; không tạo fixture mới dạng đó và không phân hạng từ suy đoán. Nhóm r812 chạy nguyên các ca có sẵn của repository theo chỉ thị hồi quy, trên bản sao riêng.

`mo-lai`, `cho_chu_kho`, checkpoint #813, vòng P3 #814, generation kế #815, ghi đẩy/kích hoạt #816 và nợ P3 #929 nêu trong prompt đều ngoài scope. Không sửa mã nguồn packet, không commit/push/merge/land. Verdict chỉ neo exact commit ở dòng 2.
