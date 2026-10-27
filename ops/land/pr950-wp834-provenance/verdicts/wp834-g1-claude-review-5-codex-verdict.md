Verdict: request_changes
Reviewed commit: 19a862bb7cedb7c880532f818661162ff04fde97
Spec sha256: c57ef4d86592218729b811efede7909803d75b6d18ca0d0c3e5059848b44a9d2; Chung sha256: 4e3d1e1b3f6a0b60b96ad7b70f0ece97eca4bb3d6d10defeab1cd24ac6d1cbf0

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn: `tham-chieu/VERDICT-luot4.md`, SHA-256 `7b44edac3dc6e4e5119941a8f5e22afeb911cc88cabcc65e3479b16275051400`, reviewed commit `dcb77e78113ed66641771a82f404b713c9602d4d`. Đã đọc toàn văn prompt.snapshot; đọc hai đặc tả, diff base→head và bản vá dcb77e7→19a862b. Bản vá lượt 5 chỉ thêm 11 dòng vào test; mã sản phẩm không đổi.

| lớp/biểu hiện lượt trước | kết luận lượt 5 | phép đo độc lập |
|---|---|---|
| F2 `required-mutation-coverage-missing`: bỏ required check bổ sung của lease | **đóng biểu hiện — ĐÃ VÁ THẬT** | Dựng lại `ignore_lease_required_checks` chiếu toàn bộ nc về CHECK_BAT_BUOC; ca mới `r834_check_lease_them` giết bằng AssertionError đòi rc=12, được 0. Lease Git thật cũng cho candidate 12/VẮNG, mutant 0; cung cấp đủ workflow thứ hai + hai file jobs thì candidate 0. |
| F2: so chéo ID giữa endpoint | **đóng biểu hiện — ĐÃ VÁ THẬT** | `cross_endpoint_id_space` bị `r834_id_trung_khac_endpoint` giết: đòi 0, được 12/“id trùng xuyên endpoint”. Candidate nhận hợp lệ ID 20 ở review và issue comment. |
| F2: bỏ review hoàn tất đơn độc | **đóng biểu hiện — ĐÃ VÁ THẬT** | `omit_completed_review` bị `r834_review_hoan_tat_don_doc` giết: đòi 0, được 12/“connector chưa xong”. |
| **F2 ở cấp lớp** | **còn mở — vá một phần** | Hai mutant khác không tương đương vẫn sống **57/57 mỗi mutant**: bỏ các trường P3 bắt buộc; biến connector_refs thành tập làm mất tính duy nhất. Probe A/B chứng minh tác động, không tính mutant tương đương là finding. |

`CONFIRM.jsonl` lưu đúng cặp neo/thay và ngoại lệ của ba mutant cũ. Chỉ chạy ca đích mới trên mỗi mutant cũ; không khai đã chạy toàn bộ 57 ca trên chúng. `DECLARED.jsonl` đo riêng ba mutant executor thêm, cũng giết đúng lý do.

**Còn mở: 2 lớp — 0 P0, 1 P1, 1 P2, 0 P3.** F2 kế thừa vẫn mở. **Một lớp phát hiện mới so với tập còn mở lượt 4:** `ci-attempt-provenance-missing`, là tái lộ lớp thiết kế #812 trên một biểu hiện khác (readback run cũ mâu thuẫn jobs mới). Không quy lỗi này cho 11 dòng test mới. Tập U lượt 4 có một lớp, F đóng hoàn toàn rỗng ⇒ tỷ lệ đóng lớp 0/1; ba biểu hiện vá đúng không được tính thành ba lớp đã đóng.

F4 `connector-parser-mutant-false-credit` vẫn đóng: parser mutant hỏng capture group được phân loại **TIN_DUNG_GIA/CliSapDo** ở control và hai ca parser (rc=1/IndexError); không lấy ba lỗi sập này làm kill. Parser mutant khai báo hiện hành giết bằng AssertionError đúng. F5 `stop-validation-order` không tái mở: ca Unicode giữ byte, mutant bỏ tiền kiểm encoding bị giết trước sentinel `_xet_dung`; probe quyết định chứa surrogate rc=2 có kiểm soát.

## Bảng lớp còn mở

`pl` = `.claude/dev/packet_loop.py`; `test` = `.claude/dev/packet_loop_test.py`. Dòng neo exact head. Hai biểu hiện độ phủ cùng một nguyên nhân, không tách thành hai finding.

| slug | hạng | biểu hiện file:dòng | phép đo/tái hiện đã chạy | hướng vá |
|---|---|---|---|---|
| `ci-attempt-provenance-missing` (F6, phát hiện mới lượt 5; kế thừa slug thiết kế #812) | **P1** | pl:2845, pl:2852 | `EXTRA_CONFIRM.jsonl`: run 100/attempt 1 và checks cũ xanh; tệp jobs thứ hai có cùng run/head, attempt 2/in_progress ⇒ **rc=0, accepted**. `CI_CONSISTENCY.jsonl`: xảy ra cả khi cùng một file jobs và khi job attempt 2 đã failure. | Trước lọc jobs theo attempt của run, đối chiếu attempt lớn nhất đã biết cho cùng run/head; jobs chứng minh attempt mới hơn thì từ chối readback cũ/mâu thuẫn, giữ state. Thêm ca r834 đo cả run cũ + jobs mới, có đối chứng attempt 2 đủ/xanh và jobs attempt cũ hợp lệ. |
| `required-mutation-coverage-missing` (F2, kế thừa) | **P2** | test:8560, test:8800; chốt chưa có ca giết tại pl:2881, pl:2904 | `AUDIT.jsonl`: `allow_duplicate_connector_refs` và `allow_missing_p3_fields` đều **57/57 PASS**. A/B candidate 11/2, mutant 0/accepted; cùng một endpoint/id còn có thể được mutant gán vào hai slug H khác nhau. | Bổ sung ca r834 đổi một yếu tố (quyết định thiếu owner; ref lặp trong/giữa lớp) và mutant đúng chốt. Giữ code chốt hiện hành; giảm phần test lặp/parameter hoá để giữ trần 450. |

### F6 — job đã chứng minh có attempt mới hơn nhưng bị bỏ qua

Baseline dương đi qua init → lease H/Đ/R thật trong kho giả cục bộ → receipt approve → approved_pending. Run `id=100`, workflow `.github/workflows/ci.yml`, head H, attempt 1 completed/success; đủ năm jobs/check-runs xanh, suite 500; connector sạch. Chỉ thêm readback job cùng run/head, tên `gate (ubuntu-latest)`, `id=250`, `run_attempt=2`, `status=in_progress`, `conclusion=null`, URL check-run 350 đúng kho. Run/check readback vẫn là snapshot attempt 1. Mỗi file khai total_count đúng tập ID của chính nó.

`_kiem_ci` lấy attempt 1 từ run rồi lọc mất job attempt 2 tại pl:2852; không kiểm mâu thuẫn đã có giữa hai readback. Các check cũ vẫn đủ cho `cmd_kiem_gate`, nên ghi accepted. Check-run 350 chưa có trong snapshot check-runs cũ cũng bị bỏ qua cùng job mới. Đây là **thiếu kiểm nhất quán I7/M2 của đầu vào R**, không phải yêu cầu máy xác thực GitHub hoặc chống executor gian lận. Chính dữ liệu đã nộp chứng minh không thể gọi attempt 1 là mới nhất. Mẫu này có thể xảy ra khi lấy các endpoint ở hai phía của một rerun.

| phép đo | candidate | bản thử hướng vá riêng |
|---|---|---|
| attempt 1 đủ/xanh, không job mới | 0/accepted | 0/accepted |
| run/check attempt 1 xanh, jobs có attempt 2 đang chạy, hai file | **0/accepted** | 12/mâu thuẫn, nguyên byte |
| cùng tình huống, một file jobs | **0/accepted** | 12/mâu thuẫn, nguyên byte |
| job attempt 2 completed/failure | **0/accepted** | 12/mâu thuẫn, nguyên byte |
| đổi run thành attempt 2/in_progress | 12/chưa xanh, nguyên byte | không cần đo thêm cho lỗi này |
| run/jobs attempt 2 khớp, đủ check xanh | 0/accepted | 0/accepted |
| run/jobs mới attempt 2 xanh + job cũ attempt 1 | 0/accepted | 0/accepted |

Đã chạy hướng vá bằng bản sao `mutants/reject_newer_job_attempt_hint/packet_loop.py`; cặp neo/thay trong `EXTRA_CONFIRM.jsonl`, script `extra_confirm.py`. Đây là dữ liệu phản chứng, **không phải patch đã áp vào packet**. Chỉ kiểm các đối chứng trong bảng trên trên bản thử; không khai full suite của bản thử. Rủi ro khi vá: cấm mọi attempt khác nhau sẽ chặn sai jobs lịch sử; so attempt xuyên run sẽ chặn workflow khác. Vì vậy chỉ xét mâu thuẫn “job cùng run/head có attempt lớn hơn run đã chọn”, giữ test lower-attempt và nhiều workflow. Không được tự nâng run lên attempt mới rồi dùng lại check cũ.

### F2 — hai mutant có tác động thực nhưng không ca candidate nào bảo vệ

| mutant | phép đổi trên bản sao | suite r834 | probe candidate / mutant |
|---|---|---|---|
| allow_missing_p3_fields | Bỏ `set(q) == truong` trong kiểm từng quyết định | **57/57 PASS ⇒ SỐNG** | P3 hợp lệ chỉ bỏ `owner`: 2/P3 còn mở, byte nguyên / 0/accepted với quyết định thiếu owner. |
| allow_duplicate_connector_refs | `sorted(refs) != sorted(p3)` → `set(refs) != set(p3)` | **57/57 PASS ⇒ SỐNG** | Lặp ref `[review_comments,11]`: 11/phủ ĐÚNG / 0. Thêm lớp slug `e-f` cùng ref, kèm quyết định tương ứng: candidate 11, mutant 0/accepted với cùng finding gán vào cả `c-d` và `e-f`. |

Đây là thiếu nghiệm thu, **không phải bản gốc đang nhận quyết định thiếu hoặc ref trùng**. M1 bắt buộc đủ trường + lý do; M4/I11 yêu cầu ánh xạ finding → slug từ H. Các probe của reviewer không thay ca r834 đã có trong candidate. `audit_definitions.json`, `run_review.py audit`, `probe_review.py` và `extra_confirm.py` chứa cặp neo/thay và ca khoá có thể tái dẫn xuất.

Không tính `ignore_job_check_name` là finding dù 57/57 vẫn xanh: phép so ID check-run mới nhất ở pl:2864 và kiểm nhất quán ID đã bảo vệ tên tương đương. Probe đổi job sang check-run tên khác bị **cả candidate và mutant** từ chối rc=12. Đây là đối chứng chống báo sai “mutant sống = lỗi” chỉ từ số đếm.

Hướng vá F2 ở test: dùng `_r834_ca(2, ...)` xoá owner trên quyết định P3 hợp lệ; dùng `_r834_ca(11, ..., p3_cn=True)` tạo ref lặp, giữ biên nhận H/qd đủ. Mỗi ca phải giết mutant bằng AssertionError về rc/lý do, không setup/traceback. Rủi ro: ca thiếu owner nhưng thiếu cả H hoặc qd khác sẽ chết sớm ở chốt phụ; ca hai slug phải cung cấp đủ hai quyết định để mutant không bị chặn vì thiếu qd. Diff còn 7 dòng theo trần hiện tại; cần gộp helper/giảm lặp khi bổ sung sửa F6 và test, không nới gate để tiết kiệm dòng.

## Định danh, môi trường và phạm vi

- CWD thực có `src/`, `out/`, `tham-chieu/`; snapshot prompt nằm ngoài ba thư mục đó và đã được đọc toàn văn. SRC được đối xử read-only; mọi script, fixture, clone, mutant, temp và log ở OUT.
- HEAD `19a862bb7cedb7c880532f818661162ff04fde97`; tree `3eaf451e17fdb30afa609929fcb48e2b3ca7ffb2`. Base/origin/master `ab344da5f07cce673d97056b70b002911c4d5082`, tổ tiên rc=0; detached (`symbolic-ref` rc=1), không shallow, `.git` là thư mục. Hai spec hash đúng dòng 3.
- Lease bản chép r1/g1, sensitive, executor Claude; review mục tiêu cross_approved. Reviewer là Codex/họ openai, shell cục bộ qua công cụ phiên, transport machine; không dùng context executor. Không có telemetry độc lập để xác nhận exact model/effort/session ID hoặc riêng nhãn surface `codex_cli`; không suy danh tính từ tài khoản submitter và không tự phát hành receipt assurance.
- Không mạng/GitHub hoặc push remote thật. Git fixture giới hạn `GIT_ALLOW_PROTOCOL=file`; các push trong fixture chỉ tới bare repository dưới OUT. `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR=out/tmp`, Git global/system cô lập. Python 3.13.17, Git 2.43.0, Linux.
- Snapshot đầu/cuối **6011 tệp/link** kể cả `.git`, **0 delta**; tracked/untracked/ignored sạch, worktree/index diff rc=0. `SOURCE_INITIAL.json`, `SOURCE_FINAL.json`, `SOURCE_INTEGRITY.json`, `CHECKS.json`. Chỉ chứng minh hai mốc không đổi, không chứng minh toàn bộ lịch sử chưa từng ghi rồi hoàn nguyên. Sandbox workspace-write; phạm vi thực ghi của review chỉ OUT.

| tệp | thêm | xoá |
|---|---:|---:|
| .claude/dev/packet_loop.py | 181 | 1 |
| .claude/dev/packet_loop_test.py | 258 | 3 |
| docs/PROTOCOL_DA_PHIEN.md (§4) | 4 | 1 |
| Tổng | **443** | **5** |

Đúng 3 đường dẫn, 443≤450; diff-check rc=0. Bản vá riêng dcb77e7→19a862b chỉ test, 11 dòng thêm. Hiện vật `CANDIDATE.diff`, `PATCH.diff`.

## Đối chiếu I1–I11 và M1–M5

| mục | kết quả trong phạm vi đo |
|---|---|
| I1/M1 | Accept có ls-remote hạng Đ; baseline qua lease/receipt; lệch remote bị rc=5. Ghi accepted_sha, mốc endpoint, qd và các hash đúng trên probe dương. F6 làm điều kiện CI chưa đủ. |
| I2 | Không sửa cửa lease. r834 dựng lease thật, r812 kiểm H/holder/readback; authentic extra lease xác nhận union required_checks. Không kiểm authority lease live qua mạng. |
| I3/M3 | Finding rỗng được nhận; không bằng chứng xong bị bác. P0/P1/P2, badge Q1/P 1/P4/p3 và hai hạng bị bác ở cả ba endpoint. Review comment thiếu badge/neo bị bác. Check status/conclusion không success bị bác. |
| I4 | Mọi từ chối đã đo giữ byte, gồm H/P3 muộn, malformed JSON/Unicode. Mutant ghi sớm chết bằng assertion I4. Riêng đầu vào CI mâu thuẫn ở F6 lại được nhận: chưa thể tuyên bố mọi đầu vào hỏng đều bị bác. |
| I5/M1 | Gọi helper chung sau JSON/CI/connector/H/qd/encoding. Mutant bỏ gọi, gọi sớm trước đầu vào/H/encoding đều giết đúng. Không đặt thêm điều kiện dừng ngoài packet. |
| I6 | Không thêm quyền mở lại/checkpoint/generation/ngoại lệ đẩy; không đòi triển khai packet sau. |
| I7/M2 | App/workflow/job, URL kho, suite, head, newest run, attempt join và kiem-gate có kiểm. **F6 còn mở** ở nhất quán attempt giữa readbacks. Hai workflow bắt buộc, hai file jobs dương đạt. |
| I7/M3 | Trang theo tập ID riêng endpoint; ID lặp giống nhau nhận, mâu thuẫn bác. ID chung số xuyên endpoint nhận. Review hoàn tất đơn độc nhận; PENDING đơn độc bác. Reviewed commit tiền tố 7/10/40 và bare/backtick nhận; mơ hồ/đuôi thừa bị bác; finding ở head cũ hợp lệ được bỏ qua. |
| I8 | Connector H tái dùng _du_dieu_kien_approve và chuẩn hoá validator canon; regression r812 về identity/alias/family/surface/transport đạt. |
| I9 | 148/148 r812 được chọn và 2/2 stdout cp1252/cp1258 đạt, gồm đường cũ và init chưa lease. Không khai toàn suite đã chạy. |
| I10/M4 | Biên nhận connector ứng viên lệch packet/generation/sha/spec_hash/role bị rc=11, byte nguyên. Không dùng vai trò nguồn cho candidate. |
| I11/M4 | Slug từ H; refs thiếu/thừa/trùng/sai kiểu/endpoint/id bị bác ở candidate. Quyết định thiếu/trùng/thừa/sai kiểu/blank/Unicode bị bác. F2 còn thiếu ca r834 khoá hai tính chất cụ thể nêu trên. |
| M5 | Protocol chỉ đổi §4, cửa accept có điều kiện ADR-0054 và nêu remote/CI/connector/P3. Không kích hoạt ADR-0054. |

Đối chiếu lớp thiết kế #812: `connector-verdict-incomplete`, `conflicting-evidence-overwrite`, phần connector của `findings-not-receipt-bound` không tái lộ hành vi cũ trong các phép đo; riêng `ci-attempt-provenance-missing` **chưa đóng hoàn toàn**, theo F6. Không lấy R làm authority độc lập; R vẫn phải nhất quán theo I7.

#929 đã có ở base: `_che_do_0054` quét cụm khai trong ADR, không ghim số tệp kích hoạt. Hai đặc tả wp834/phần chung không bắt số tệp kích hoạt cố định; I9 vẫn đặt xác định chế độ ở đường record-lease mới. Không phát hiện mâu thuẫn buộc dừng với #929. Nợ `ls[0] == 0` ngoài phạm vi theo prompt.

## Đối chiếu từng ca bắt buộc mục nghiêm_thu

Tên trong bảng lược tiền tố `r834_`. Mỗi ca nền đã PASS, rc/lý do kiểm bởi helper; ca âm kiểm byte-state. Cột cuối đọc từ ngoại lệ và stderr CLI thật trong `DECLARED.jsonl`.

| yêu cầu | ca | mutant | nền / mutant đỏ đúng lý do |
|---|---|---|---|
| sạch lop=[] và connector không finding | sach_accepted | bo_ket_luan_issue_comment | 0/accepted; mutant 12/chưa xong, AssertionError đòi 0 |
| remote khác pending | dau_nhanh_lech | bo_dau_nhanh_remote | 5/≠pending; mutant 0 |
| check bắt buộc vắng | check_vang | job_vang_bo_qua | 12/VẮNG; mutant 0 |
| cùng tên từ app khác | check_app_khac | bo_app | 12/không từ app; mutant 0 |
| cùng tên workflow khác cùng app | check_workflow_khac | bo_path_workflow | 12/VẮNG; mutant 0 |
| attempt mới chạy, check cũ xanh | rerun_dang_chay | bo_attempt_moi_nhat | 12/chưa xanh; mutant 0; hai hunk nới run-state và join attempt, ca attempt_moi_job_cu đo riêng join |
| check-run kho khác | check_kho_khac | bo_kho_check_run | 12/kho khác; mutant 0 |
| PR khác cùng head | pr_khac_cung_head | bo_neo_pr_phan_tu | 12/không thuộc; mutant 0 |
| PENDING không xong | review_pending | pending_la_xong | 12/chưa xong; mutant 0 |
| CHANGES_REQUESTED có P1 | review_changes_p1 | bo_finding_review | 12/còn P1; mutant 0 |
| issue comment có P1 | issue_comment_p1 | bo_finding_issue_comment | 12/còn P1; mutant 0 |
| cùng ID hai nội dung P1 rồi P3 | cung_id_hai_noi_dung | bo_nhat_quan_id | 12/hai nội dung; mutant 0 |
| run cùng ID khác path | run_cung_id_khac_path | bo_nhat_quan_id | 12/hai nội dung; mutant 0 |
| P3 offline thiếu quyết định | p3_offline_thieu_qd | bo_p3_offline | 2/P3 còn mở; mutant 0 |
| P3 connector thiếu quyết định | p3_connector_thieu_qd | bo_p3_connector | 2/P3 còn mở; mutant 0 |
| P3 connector thiếu slug H | p3_connector_khong_slug | khoa_id_so | 11/cần biên nhận; mutant 0 |
| bằng chứng dương rỗng | bang_chung_duong_rong; state_required_checks_rong | bo_bang_chung_duong; bo_luoc_do_state | 12/chưa xong và 8/state hỏng; mutant 0 |
| đầu vào hỏng giữ byte | dau_vao_hong_state_nguyen | ghi_truoc_khi_doc | 12/JSON hỏng; mutant AssertionError “I4: state đổi sau khi accept từ chối” |

Đủ danh sách tối thiểu và mutant khai báo giết đúng không phủ hết nghĩa vụ M1/M2/M4; F2/F6 vẫn có phản chứng độc lập.

## Toàn bộ quan hệ mutant khai báo đã đo

**57/57 nền; 52 mutant** (51 tên r834 và một r812_bo_generation), **58 quan hệ GIẾT đúng** (57 tới r834, một tới r812). 0 SỐNG/0 TÍN DỤNG GIẢ trong nhóm mutant khai báo này. Các lỗi sập có chủ ý trong CONFIRM được thống kê riêng, không cộng kill.

| mutant | ca đích | phân loại | ngoại lệ/lý do |
|---|---|---|---|
| r812_bo_generation | r812_bien_nhan_lech_generation | GIET | AssertionError: r812 review ['bn']: đòi rc=11, được rc=0; stderr='' |
| r812_bo_generation | r834_bnc_lech_generation | GIET | AssertionError: r834 accept: đòi rc=11, được rc=0; stderr='' |
| r834_bo_ket_luan_issue_comment | r834_sach_accepted | GIET | AssertionError: r834 accept: đòi rc=0, được rc=12; stderr='connector chưa xong trên 49f909fdf9c818601e73a5fd39bf7478a5957953: không review hoàn tất/kết luận nào của chatgpt-codex-connector[bot]' |
| r834_bo_ref_connector_h | r834_p3_du_quyet_dinh | GIET | AssertionError: r834 accept: đòi rc=0, được rc=11; stderr="bảng lớp H phải phủ ĐÚNG từng (endpoint, id) P3 của connector [('review_comments', 11)], mỗi cặp một lần" |
| r834_bo_dau_nhanh_remote | r834_dau_nhanh_lech | GIET | AssertionError: r834 accept: đòi rc=5, được rc=0; stderr='' |
| r834_job_vang_bo_qua | r834_check_vang | GIET | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_bo_app | r834_check_app_khac | GIET | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_bo_path_workflow | r834_check_workflow_khac | GIET | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_bo_attempt_moi_nhat | r834_rerun_dang_chay | GIET | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_bo_kho_check_run | r834_check_kho_khac | GIET | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_bo_neo_pr_phan_tu | r834_pr_khac_cung_head | GIET | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_pending_la_xong | r834_review_pending | GIET | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_bo_finding_review | r834_review_changes_p1 | GIET | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_bo_finding_issue_comment | r834_issue_comment_p1 | GIET | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_bo_nhat_quan_id | r834_cung_id_hai_noi_dung | GIET | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_bo_nhat_quan_id | r834_run_cung_id_khac_path | GIET | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_bo_p3_offline | r834_p3_offline_thieu_qd | GIET | AssertionError: r834 accept: đòi rc=2, được rc=0; stderr='' |
| r834_bo_p3_connector | r834_p3_connector_thieu_qd | GIET | AssertionError: r834 accept: đòi rc=2, được rc=0; stderr='' |
| r834_khoa_id_so | r834_p3_connector_khong_slug | GIET | AssertionError: r834 accept: đòi rc=11, được rc=0; stderr='' |
| r834_bo_bang_chung_duong | r834_bang_chung_duong_rong | GIET | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_ghi_truoc_khi_doc | r834_dau_vao_hong_state_nguyen | GIET | AssertionError: I4: state đổi sau khi accept từ chối |
| r834_bo_kiem_gate | r834_check_noi_do | GIET | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_bo_check_moi_nhat | r834_check_noi_do_bi_che | GIET | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_check_run_khong_nhat_quan | r834_check_cung_id_khac_app | GIET | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_bo_khop_attempt_job | r834_attempt_moi_job_cu | GIET | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_run_cu_nhat | r834_run_moi_nhat_do | GIET | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr="CẢNH BÁO: 'gate (ubuntu-latest)' có 1 run ở suite khác (300) — bỏ qua\nCẢNH BÁO: 'gate-cong-cu-gop (ubuntu-latest)' có 1 run ở suite khác (301) — bỏ qua\nCẢNH BÁO: 'gate-ops (ubuntu-latest)' có 1 run ở suite khác (302) — bỏ qua\nCẢNH BÁO: 'gate-packet-loop (ubuntu-latest)' có 1 run ở suite khác (303) — bỏ qua\nCẢNH BÁO: 'gate-registry (ubuntu-latest)' có 1 run ở suite khác (304) — bỏ qua" |
| r834_bo_kho_url_job | r834_job_url_kho_khac | GIET | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_noi_check_theo_ten | r834_job_tro_check_khong_co | GIET | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_noi_check_theo_ten | r834_job_url_qua_dai | GIET | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_jobs_total_toan_cuc | r834_hai_tep_jobs | GIET | AssertionError: r834 accept: đòi rc=0, được rc=12; stderr='KHÔNG ĐO ĐƯỢC: workflow_jobs: cần trang {`jobs`, `total_count`} cùng một lần lấy, id int, tập id phân biệt = total_count' |
| r834_badge_chi_P | r834_badge_ngoai_mien_review | GIET | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_changes_khong_hang_lot | r834_review_changes_khong_hang | GIET | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_commit_thieu_la_cu | r834_review_comment_thieu_commit | GIET | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_reviewed_commit_tim_dau | r834_reviewed_commit_sai_dang | GIET | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_reviewed_commit_tim_dau | r834_reviewed_commit_mau_thuan | GIET | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_head_cu_van_chan | r834_issue_comment_head_cu_khong_chan | GIET | AssertionError: r834 accept: đòi rc=0, được rc=12; stderr='connector issue comment 21 có finding mà không neo head' |
| r834_bo_envelope | r834_envelope_head_khac | GIET | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_bo_total_count | r834_trang_thieu | GIET | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_bo_phu_dung_refs | r834_refs_thua | GIET | AssertionError: r834 accept: đòi rc=11, được rc=0; stderr='' |
| r834_bo_luoc_do_state | r834_state_required_checks_rong | GIET | AssertionError: r834 accept: đòi rc=8, được rc=0; stderr='' |
| r834_bo_luoc_do_state | r834_state_p3_sai_kieu | GIET | AssertionError: r834 accept: đòi rc=8, được rc=0; stderr='' |
| r834_bo_dau_hang_tron | r834_reviewed_commit_span_thua | GIET | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_bo_tien_to_mo_ho | r834_tien_to_mo_ho | GIET | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_bo_goi_xet_dung | r834_xet_dung_duoc_goi | GIET | AssertionError: r834 accept: đòi rc=3, được rc=0; stderr='' |
| r834_xet_dung_truoc_dau_vao | r834_xet_dung_sau_dau_vao | GIET | AssertionError: r834 accept: đòi rc=12, được rc=3; stderr='COC_XET_DUNG' |
| r834_bo_kho_run | r834_run_kho_khac | GIET | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_bo_head_run | r834_run_head_khac | GIET | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_bo_head_job | r834_job_head_khac | GIET | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_qd_theo_tap | r834_qd_trung | GIET | AssertionError: r834 accept: đòi rc=2, được rc=0; stderr='' |
| r834_bo_kieu_job | r834_job_attempt_bool | GIET | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_bo_kieu_job | r834_job_run_id_float | GIET | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_xet_dung_truoc_h | r834_xet_dung_sau_h | GIET | AssertionError: r834 accept: đòi rc=11, được rc=3; stderr='COC_XET_DUNG' |
| r834_bo_job_xanh | r834_job_chua_xanh | GIET | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_bo_p1_review_comment | r834_review_comment_p1 | GIET | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_bo_ma_hoa_truoc | r834_qd_khong_ma_hoa | GIET | AssertionError: r834 accept: đòi rc=2, được rc=3; stderr='COC_XET_DUNG' |
| r834_bo_check_lease | r834_check_lease_them | GIET | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_id_so_cheo_endpoint | r834_id_trung_khac_endpoint | GIET | AssertionError: r834 accept: đòi rc=0, được rc=12; stderr='KHÔNG ĐO ĐƯỢC: gop: cần trang {`items`, `total_count`} cùng một lần lấy, id int, tập id phân biệt = total_count' |
| r834_bo_review_xong | r834_review_hoan_tat_don_doc | GIET | AssertionError: r834 accept: đòi rc=0, được rc=12; stderr='connector chưa xong trên 49f909fdf9c818601e73a5fd39bf7478a5957953: không review hoàn tất/kết luận nào của chatgpt-codex-connector[bot]' |

## Lệnh, rc và bằng chứng dương

Chạy từ thư mục rv5; script test luôn dùng `out/copy` hoặc mutant riêng. Runner ghi JSONL tăng dần, giữ đầy đủ command/rc/stdout/stderr của CLI con. rc=0 của runner AUDIT chỉ nghĩa thu thập hoàn tất; các mutant không tương đương còn sống vẫn là **nghiệm thu failed**.

| lệnh | rc | kết quả/hiện vật |
|---|---:|---|
| `python -B out/run_review.py declared` | 0 | 57 nền PASS; 52 mutant/58 quan hệ GIẾT đúng; DECLARED.jsonl/log/stderr |
| `python -B out/run_review.py regression` | 0 | 148/148 r812 PASS, 2/2 encoding PASS; 1 ca not_run theo giới hạn đường dẫn; REGRESSION.jsonl/log/stderr |
| `python -B out/run_review.py audit` | 0 | 3×57 ca PASS trên mutant; 2 mutant có tác động thực SỐNG, 1 tương đương loại khỏi finding; AUDIT.jsonl/log/stderr |
| `python -B out/probe_review.py` | 0 | 94/94 phép đo khớp rc/lý do/byte và accepted hashes; PROBES.jsonl/log/stderr |
| `python -B out/confirm_review.py` | 0 | 3 mutant cũ GIẾT đúng; 3 ca parser sập TIN_DUNG_GIA đúng; 3 phép lease Git thật; CONFIRM.jsonl/log/stderr |
| `python -B out/extra_review.py` (bản đầu trước khi thêm hướng vá) | 0 | 5 phép đo, tái hiện F6 + hai slug cùng ref; EXTRA.jsonl/log/stderr. Bản nguồn hoàn chỉnh tương đương chạy ở lệnh tiếp. |
| `python -B out/extra_confirm.py` | 0 | 9 phép đo, F6 candidate/hint và đối chứng sạch/attempt 2; EXTRA_CONFIRM.jsonl/log/stderr |
| `python -B out/ci_consistency.py` | 0 | 6 phép đo: một file, attempt mới failure, jobs lịch sử; CI_CONSISTENCY.jsonl/log/stderr |
| `python -B out/copy/.claude/dev/packet_loop.py doctrine-scan --root out/copy` | 0 | 10 tệp, 0 chỗ chép doctrine; doctrine-scan.log |
| `python -B out/copy/.claude/dev/packet_loop.py adr-song --root out/copy` | 0 | 55 ADR/55 dòng khớp 1–1; ngoại lệ 0016 khai sẵn; adr-song.log |
| `git -C src diff --check ab344da 19a862b` | 0 | không lỗi whitespace; CHECKS.json |
| `git -C src diff --numstat ab344da 19a862b` | 0 | 3 tệp, 443 thêm/5 xoá; CHECKS.json |
| `python -B out/finalize_review.py` | 0 | kiểm số đo/manifest nguồn; SUMMARY.json, SOURCE_INTEGRITY.json, ARTIFACTS.json |

Để chạy lại, dùng thư mục OUT mới hoặc đổi tên nhóm fixture vì script giữ hiện vật thay vì xoá. Các bản mutant/hint và fixture là dữ liệu review, không áp vào executor. `ARTIFACTS.json` băm các log/script/verdict/diff sau khi writer hoàn tất.

**not_run:** full suite `python .claude/dev/packet_loop_test.py` (~45 phút), theo ưu tiên chạy chọn lọc trong prompt; không khai N/N toàn repository hoặc xác nhận lời khai 929/929 của executor. CI online và Windows execution chưa đo. Bare Ruff lint và Ruff pin/probe contract not_run, không dùng nhãn “Ruff passed”. SyntaxWarning sẵn có tại test:3714 không được tính kill hoặc finding.

`r812_r4_own_parent` không chạy: tuân thủ yêu cầu không soạn nội dung đường dẫn thoát cây. Hướng thử này chỉ mô tả bằng lời: receipt/readback qua đường dẫn đi lên hoặc symlink dẫn ra ngoài gốc phải bị từ chối có kiểm soát, state nguyên byte. Không dựng payload, không suy an toàn đường dẫn từ phần không chạy.

Ngoài phạm vi, không phân hạng: mo-lai, cho_chu_kho, checkpoint #813, vòng P3 #814, generation #815, ghi đẩy/kích hoạt #816, nợ #929 nêu trong prompt. Verdict chỉ neo commit dòng 2, **không cấp quyền push/merge/land**.
