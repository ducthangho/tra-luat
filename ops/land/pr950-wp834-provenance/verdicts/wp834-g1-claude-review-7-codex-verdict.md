Verdict: approve
Reviewed commit: 8ac10ce47d2587c91637d74d299e3c781025be1e
Spec sha256: c57ef4d86592218729b811efede7909803d75b6d18ca0d0c3e5059848b44a9d2; Chung sha256: 4e3d1e1b3f6a0b60b96ad7b70f0ece97eca4bb3d6d10defeab1cd24ac6d1cbf0

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn lượt 6: `tham-chieu/VERDICT-luot6.md`, SHA-256 `61c33076c9ea9f3ab6e02530241304fd30671081819a059ef560ac4e949a73a9`, head `394d24787aaa5b4e4638b0820b42fe25b6f0432c`. Finding duy nhất còn mở lúc đó là P2 `required-mutation-coverage-missing`. Đã đọc toàn văn prompt.snapshot được chỉ định, hai đặc tả, verdict lượt 6, đầu vào thiết kế #812; đối chiếu lịch sử mutant các lượt 1–5, review toàn diff PR và riêng phần vá lượt 7.

| biểu hiện/mutant sống lượt 6 | kết luận lượt 7 | phép đo độc lập trên head hiện hành |
|---|---|---|
| `ignore_job_run_id` | **đóng — ĐÃ VÁ THẬT** | Bỏ riêng run_id khỏi phép nối job. `r834_job_run_id_khac`: GIET, AssertionError đòi rc=12, được 0. A/B chỉ đổi job.run_id=90: candidate 12/“VẮNG”, nguyên byte; mutant 0/accepted. |
| `ignore_invalid_ref_entries` | **đóng — ĐÃ VÁ THẬT** | Bỏ riêng kiểm số phần tử refs được lọc. `r834_refs_phan_tu_hong`: GIET, AssertionError đòi 11, được 0. A/B thêm ref sai endpoint cạnh ref đúng: candidate 11/“phủ ĐÚNG”, nguyên byte; mutant 0/accepted. |
| `ignore_p3_value_types` | **đóng — ĐÃ VÁ THẬT** | Bỏ kiểm các giá trị quyết định là chuỗi không trắng. `r834_qd_gia_tri_khong_chuoi`: GIET, AssertionError đòi 2, được 0. A/B đổi riêng owner=123: candidate 2/“P3 còn mở”, nguyên byte; mutant 0/accepted. |

`PROBES.jsonl` ghi A/B và ba nhóm `confirm_*`; `DECLARED.jsonl` đo lại ba mutant executor thêm. Cặp neo/thay đúng ba phép bỏ chốt lượt 6, được kiểm duy nhất và compile trước chạy. Chỉ cần ca đích giết đúng để đóng mutant cũ; không khai đã chạy 63 ca trên từng mutant cũ.

Diff `394d247..742ba39` chỉ thêm ba ca/ba mutant trong tệp test; sản phẩm không đổi. Merge `8ac10ce` giữ nguyên cả ba tệp write set so với `742ba39` (diff rỗng, rc=0). Không thấy bản vá lượt 7 gây lỗi hành vi mới trong phạm vi đã đo.

**Kết luận: 0 P0, 0 P1, 0 P2, 1 lớp P3 còn mở ⇒ approve.** Toàn bộ biểu hiện P2 lượt 6 đã đóng. Hai đột biến tự dựng mới dưới đây là nợ P3 theo đúng luật phân hạng lượt 7; không dùng chúng để giữ hoặc tái mở P2 cũ. Ngưỡng áp dụng: không còn P0/P1/P2. Đây là verdict nội dung trên exact commit, không cấp quyền push/merge/land.

## Bảng lớp còn mở

`pl` = `.claude/dev/packet_loop.py`; `test` = `.claude/dev/packet_loop_test.py`. Đếm theo nguyên nhân, không đếm hai biểu hiện thành hai finding.

| slug | hạng | biểu hiện file:dòng | phép đo/tái hiện đã chạy | hướng vá |
|---|---|---|---|---|
| `required-mutation-coverage-missing` | **P3** — chỉ hai biểu hiện mới | test:8616, test:8808; chốt pl:2820 và pl:2771 | `omit_unanchored_issue_finding` và `allow_noninteger_page_ids` đều **63/63 r834 PASS**. A/B: candidate đều rc=12, nguyên byte; mutant đều rc=0/accepted. Không có traceback hoặc lỗi setup. | Thêm hai ca đổi một yếu tố và mutant đúng chốt: thêm issue comment P1 không có Reviewed commit bên cạnh kết luận sạch; đổi ID issue comment từ int thành float. Giữ chốt sản phẩm. Parameter hoá/gộp test để giữ trần 450 dòng. |

Nợ có tên: **bảo vệ neo head của finding issue comment và kiểu ID trang**. Owner gợi ý: **executor Packet #834 (Claude), chủ kho theo dõi**. Lý do cho phép tồn tại ở P3: đây là các mutant reviewer mới dựng, sản phẩm hiện hành từ chối đúng ở A/B; không thiếu ca bắt buộc của danh sách nghiệm thu và không có mutant đã nêu ở lượt trước còn sống. Giữ slug ổn định của lớp độ phủ, không đổi tên để xoá lịch sử. Đây là phân hạng theo chỉ thị lượt 7, không phải quyết định P3 thay mặt chủ kho trong state máy.

### Phản chứng độ phủ mới

Baseline thật: init → lease H/Đ/R qua kho Git cục bộ → receipt approve → approved_pending; đủ năm jobs/check-runs xanh, run 100/attempt 1/suite 500, connector sạch trên head. Mỗi bản mutant chỉ đổi chốt sản phẩm, giữ nguyên test candidate.

| mutant | phép đổi duy nhất | A/B trên cùng đầu vào |
|---|---|---|
| `omit_unanchored_issue_finding` | `if n is None and hang:` → `if False:` tại pl:2820 | Giữ kết luận sạch có head; thêm issue comment của bot, đúng kho/PR, badge P1, không khai Reviewed commit. Candidate rc=12/“có finding mà không neo head”, state nguyên byte. Mutant rc=0/accepted, bỏ qua finding không neo. |
| `allow_noninteger_page_ids` | `type(x.get("id")) is int` → `isinstance(x.get("id"), (int, float))` tại pl:2771 | Chỉ đổi ID kết luận sạch từ 20 thành 20.0. Candidate rc=12/“id int”, state nguyên byte. Mutant rc=0/accepted. |

Phép chạy toàn bộ 63 ca của từng mutant: `OMIT_UNANCHORED_ISSUE_FINDING.jsonl`, `ALLOW_NONINTEGER_PAGE_IDS.jsonl`; A/B: `PROBES.jsonl`. Script và cặp neo/thay: `audit_review.py`, `probe_review.py`; bản mutant ở `mutants/`. Các mutant này không trùng các phép bỏ chốt đã báo sống ở lượt 1–6.

Control `crashing_parser_control` cố ý phá capture group được `r834_sach_accepted` xếp **TIN_DUNG_GIA / CliSapDo / IndexError: no such group**. Không tính control này vào 64 kill hợp lệ. Lớp cũ `connector-parser-mutant-false-credit` không tái mở. Các probe H/P3 với sentinel `_xet_dung` xác nhận lỗi đầu vào muộn bị từ chối trước sentinel; `stop-validation-order` không tái mở.

## Định danh và phạm vi

- Thư mục làm việc thực là thư mục chứa `src/`, `out/`, `tham-chieu/`; snapshot prompt ở `scratchpad/runs/945ef0f9/prompt.snapshot` là nguồn chỉ dẫn, không phải gốc repo.
- HEAD `8ac10ce47d2587c91637d74d299e3c781025be1e`, tree `d2437881a06f791da8e88ae74e8873d06092123f`. Hai cha: `742ba39bdd8747944714c6e41c4f1272790d1f5c` và `356eb262cbd491b9599b56d5f7c41c93dd9a28a1`. `origin/master` trỏ đúng cha thứ hai.
- Lease base `ab344da5f07cce673d97056b70b002911c4d5082` là tổ tiên head (rc=0). `.git` là thư mục; clone không shallow; detached (`symbolic-ref` rc=1 đúng kỳ vọng). Băm worktree **và blob exact head** của hai đặc tả đều khớp dòng 3. `IDENTITY.json`, `CHECKS.json` lưu bằng chứng.
- Lease bản chép: packet 834/revision 1/generation 1, sensitive, executor Claude/họ claude, reviewer Codex/họ openai, assurance_target cross_approved. Lease có thêm handoff chỉ trên nhánh lease; diff PR thực chỉ ba tệp đặc tả cho phép. Chỉ thị lượt 7 cung cấp ngoại lệ same_failure_limit riêng lớp độ phủ và luật P3; review offline không xác minh comment ấy qua GitHub.
- Reviewer phiên này là Codex/OpenAI; thực thi shell bằng công cụ, transport machine, context độc lập với executor. Không có telemetry độc lập xác nhận exact model/effort/session ID hoặc nhãn surface `codex_cli`; không suy chúng từ người đăng và không tạo receipt assurance thay launcher.
- Không truy cập mạng/GitHub; mọi fetch/push/ls-remote thử nghiệm chỉ tới bare repository cục bộ dưới OUT. Các phép thử dùng `out/copy`, `out/mutants`, fixture/temp dưới OUT, `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR=OUT/tmp`, Git global/system cô lập. Không sửa source packet.

| tệp trong diff PR `356eb26..8ac10ce` | thêm | xoá |
|---|---:|---:|
| `.claude/dev/packet_loop.py` | 181 | 1 |
| `.claude/dev/packet_loop_test.py` | 262 | 3 |
| `docs/PROTOCOL_DA_PHIEN.md` (chỉ §4) | 4 | 1 |
| **Tổng** | **447** | **5** |

Đúng 3 đường dẫn, 447≤450. `git diff --check` rc=0. Toàn diff đã đọc được giữ tại `PR.diff`; diff vá lượt 7 tại `ROUND7.diff`.

## Đối chiếu I1–I11 và M1–M5

| mục | kết quả và giới hạn |
|---|---|
| I1 / M1 | Cửa accept có phép đo Đ ls-remote; remote lệch bị rc=5. Baseline đi qua lease/receipt H thật. Dương ghi đúng accepted_sha, quyết định P3, mốc từng endpoint và hash các tệp readback. |
| I2 | Không sửa cửa lease; 148 ca r812 được chọn kiểm đường H/holder/readback và hồi quy. Lease fixture có remote Git thật cục bộ. Không khẳng định đã đo lease trên dịch vụ thật. |
| I3 / M3 | `lop=[]` và connector sạch accepted. Bằng chứng hoàn tất/CI rỗng bị bác. P0/P1/P2, badge Q1/P 1 và hai hạng khác nhau trên cả ba endpoint đều bị bác. Review comment thiếu badge, CHANGES_REQUESTED thiếu hạng bị bác. Các kết luận CI khác success không mở cửa. |
| I4 | Các ca âm r834 và probe từ chối kiểm state nguyên byte; gồm JSON hỏng/khóa trùng/NaN, H sai, P3 sai kiểu/thiếu/thừa/trùng/trắng và Unicode không mã hoá. Mutant ghi state sớm chết bằng assertion I4, dù rc sản phẩm vẫn là 12. Không suy thành chứng minh mọi đầu vào vô hạn. |
| I5 / M1 | Gọi `_xet_dung` dùng chung sau CI/connector/H/P3 và tiền kiểm UTF-8. Mutant bỏ gọi hoặc gọi sớm đều chết đúng. Probe dương chạm sentinel; H/P3 hỏng bị bác trước sentinel. Không tự đặt thêm điều kiện dừng riêng cho accept. |
| I6 | Không mở quyền checkpoint/generation/mở lại/ngoại lệ đẩy; các cửa ấy ngoài phạm vi. |
| I7 / M2 | App/workflow/job, run mới nhất, attempt mới nhất, repo/head, URL job→check-run, suite, check mới nhất và lời gọi kiem-gate được kiểm. Attempt 2 đủ xanh accepted; run cũ với jobs attempt mới hơn bị bác cả một/hai tệp; attempt lớn của run khác không chặn sai. Extra lease H yêu cầu workflow thứ hai: đủ sáu check/hai file jobs accepted, thiếu run/job đỏ/check đỏ bị bác. |
| I7 / M3 | Prefix Reviewed commit 7/10/40, bare/backtick và nhãn lặp nhất quán accepted; hậu tố dư/mâu thuẫn/tiền tố mơ hồ bị bác bởi ca r834. P1 head cũ ở cả ba endpoint không chặn head hiện hành; head cũ đứng một mình không là hoàn tất. PENDING/DISMISSED/unknown không tính xong; review hoàn tất đơn độc accepted. |
| I7 / phân trang | Tập ID theo từng endpoint; ID trùng giữa endpoint được nhận. Bản lặp giống hệt accepted; khác nội dung bị bác trước lọc, gồm xuyên trang và xuyên file jobs. Trang rỗng, total_count sai/không nhất quán bị bác. Hai biểu hiện độ phủ mới được giữ ở P3 phía trên. |
| I8 | `_slug_connector` tái dùng `_du_dieu_kien_approve`; helper dùng chuẩn hoá canon. Nhóm r812 identity/provider/family/surface/transport đạt. |
| I9 | 148/148 r812 đã chọn + 10/10 r929 đạt; gồm init chưa lease và đường lease/review cũ. Hai ca stdout cp1252/cp1258 đạt qua accept mới. Full suite chưa chạy, không khai N/N toàn kho. |
| I10 / M4 | Connector receipt dùng vai ứng viên, đủ tuple packet/generation/pending_sha/spec_hash. Đổi riêng từng thành phần hoặc role: rc=11, nguyên byte, trước sentinel. Không dùng hiện vật nguồn generation cũ thay ứng viên. |
| I11 / M4 | P3 trên cả ba endpoint accepted với refs H và quyết định đủ. Refs thiếu/thừa/lặp/sai kiểu/sai endpoint, quyết định thiếu/thừa/trùng/sai kiểu/trắng đều bị bác. Slug từ bảng lớp H, không dùng ID số executor đặt. |
| M5 | Protocol §4 chỉ bổ sung cửa accept có điều kiện packet áp ADR-0054; không kích hoạt ADR-0054. |

Bốn lớp thiết kế #812 được giao cho packet — `connector-verdict-incomplete`, `ci-attempt-provenance-missing`, `conflicting-evidence-overwrite`, phần connector của `findings-not-receipt-bound` — không còn tái hiện hành vi sai cũ trong các ca/probe tương ứng. Nợ độ phủ được phân lớp riêng, không gọi thành lỗi sản phẩm đang nhận sai.

`_che_do_0054` hiện quét cụm khai do #929, không ghim tên tệp kích hoạt 0055. Đặc tả wp834/phần chung không đòi số tệp cố định; I9 vẫn xác định chế độ tại record-lease đường ref mới. **Không thấy mâu thuẫn cần dừng** giữa đặc tả ràng buộc với thay đổi này. Nợ `ls[0] == 0` của #929 ngoài phạm vi theo prompt.

## Đối chiếu từng ca bắt buộc `nghiem_thu`

Tên ca/mutant bên dưới lược tiền tố `r834_`. Tất cả ca nền PASS; mọi quan hệ mutant nêu dưới đây GIET bằng AssertionError đúng hành vi, không vì CLI sập. Mỗi ca âm kiểm byte-state. Mục check vắng được đo cả job vắng và URL trỏ check không có; probe độc lập xoá hẳn check-run cũng bị bác.

| yêu cầu | ca | mutant | nền → mutant / lý do đỏ |
|---|---|---|---|
| Sạch lop=[] và connector không finding | sach_accepted | bo_ket_luan_issue_comment | 0/accepted → 12/chưa xong |
| Đầu remote khác pending | dau_nhanh_lech | bo_dau_nhanh_remote | 5/≠ pending_sha → 0 |
| Check bắt buộc vắng | check_vang; job_tro_check_khong_co | job_vang_bo_qua; noi_check_theo_ten | 12/VẮNG hoặc không trỏ check-run → 0 |
| Cùng tên app khác | check_app_khac | bo_app | 12/không từ app → 0 |
| Cùng tên workflow khác cùng app | check_workflow_khac | bo_path_workflow | 12/VẮNG → 0 |
| Rerun mới đang chạy, check cũ xanh | rerun_dang_chay | bo_attempt_moi_nhat | 12/chưa xanh → 0; phối hợp run-state và job-attempt vì hai chốt cùng chặn |
| Check-run kho khác | check_kho_khac | bo_kho_check_run | 12/kho khác → 0 |
| PR khác cùng head | pr_khac_cung_head | bo_neo_pr_phan_tu | 12/không thuộc → 0 |
| Review PENDING không xong | review_pending | pending_la_xong | 12/chưa xong → 0 |
| CHANGES_REQUESTED có P1 | review_changes_p1 | bo_finding_review | 12/còn ['P1'] → 0 |
| Issue comment P1 | issue_comment_p1 | bo_finding_issue_comment | 12/còn ['P1'] → 0 |
| Cùng ID hai nội dung P1 rồi P3 | cung_id_hai_noi_dung | bo_nhat_quan_id | 12/hai nội dung → 0 |
| Workflow run cùng ID khác path | run_cung_id_khac_path | bo_nhat_quan_id | 12/hai nội dung → 0 |
| P3 offline thiếu quyết định | p3_offline_thieu_qd | bo_p3_offline | 2/P3 còn mở → 0 |
| P3 connector thiếu quyết định | p3_connector_thieu_qd | bo_p3_connector | 2/P3 còn mở → 0 |
| P3 connector thiếu slug H | p3_connector_khong_slug | khoa_id_so | 11/cần biên nhận → 0 |
| Bằng chứng dương rỗng | bang_chung_duong_rong; state_required_checks_rong | bo_bang_chung_duong; bo_luoc_do_state | 12/chưa xong; 8/state hỏng → 0 |
| Đầu vào hỏng giữ byte | dau_vao_hong_state_nguyen | ghi_truoc_khi_doc | Nền 12/JSON hỏng; mutant cùng rc nhưng AssertionError: I4: state đổi sau khi accept từ chối |

## Đột biến khai báo — từng quan hệ đã đo

**63/63 ca nền; 58 mutant (57 khóa r834 + r812_bo_generation), 64 quan hệ GIET đúng; 0 SỐNG, 0 TÍN DỤNG GIẢ trong nhóm khai báo.** Số thực đo là 58, không phải 59 như lời khai trong prompt; sai số đếm này không được tách thành một finding mới. `r812_bo_generation` có hai ca đích, một r812 và một r834. Các cặp neo/thay, command, rc/stdout/stderr CLI con giữ đầy đủ trong `DECLARED.jsonl`.

| mutant | ca đích | phân loại | ngoại lệ/lý do thực |
|---|---|---|---|
| r812_bo_generation | r812_bien_nhan_lech_generation | GIET | AssertionError: r812 review ['bn']: đòi rc=11, được rc=0; stderr='' |
| r812_bo_generation | r834_bnc_lech_generation | GIET | AssertionError: r834 accept: đòi rc=11, được rc=0; stderr='' |
| r834_bo_ket_luan_issue_comment | r834_sach_accepted | GIET | AssertionError: r834 accept: đòi rc=0, được rc=12; stderr='connector chưa xong trên 8e762cc2fc39015ba77213539f2ffd2e3991c240: không review hoàn tất/kết luận nào của chatgpt-codex-connector[bot]' |
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
| r834_bo_review_xong | r834_review_hoan_tat_don_doc | GIET | AssertionError: r834 accept: đòi rc=0, được rc=12; stderr='connector chưa xong trên 8e762cc2fc39015ba77213539f2ffd2e3991c240: không review hoàn tất/kết luận nào của chatgpt-codex-connector[bot]' |
| r834_bo_attempt_jobs_moi | r834_jobs_attempt_moi_hon | GIET | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_refs_theo_tap | r834_refs_lap | GIET | AssertionError: r834 accept: đòi rc=11, được rc=0; stderr='' |
| r834_qd_thieu_truong_lot | r834_qd_thieu_truong | GIET | AssertionError: r834 accept: đòi rc=2, được rc=0; stderr='' |
| r834_bo_run_id_job | r834_job_run_id_khac | GIET | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_bo_ref_hong | r834_refs_phan_tu_hong | GIET | AssertionError: r834 accept: đòi rc=11, được rc=0; stderr='' |
| r834_bo_kieu_gia_tri_qd | r834_qd_gia_tri_khong_chuoi | GIET | AssertionError: r834 accept: đòi rc=2, được rc=0; stderr='' |

## Lệnh, rc và bằng chứng dương

Chạy từ thư mục chứa src/out/tham-chieu. rc=0 của script audit chỉ nói hoàn thành thu thập; mutant sống vẫn là nợ độ phủ. Không cộng các phép kiểm lặp vào số ca suite candidate.

| lệnh | rc | kết quả/hiện vật |
|---|---:|---|
| `python -B out/run_review.py declared` | 0 | 63 nền PASS; 58 mutant/64 quan hệ GIET; DECLARED.jsonl/log/stderr |
| `python -B out/run_review.py regression` | 0 | 148 r812 + 10 r929 PASS; REGRESSION.jsonl/log/stderr |
| `python -B out/audit_review.py omit_unanchored_issue_finding` | 0 | 63/63 trên mutant — SỐNG; OMIT_UNANCHORED_ISSUE_FINDING.jsonl/log |
| `python -B out/audit_review.py allow_noninteger_page_ids` | 0 | 63/63 trên mutant — SỐNG; ALLOW_NONINTEGER_PAGE_IDS.jsonl/log |
| `python -B out/probe_review.py probes` | 0 | 99 probe đạt; ba ca đích GIET mutant lượt 6; một control TIN_DUNG_GIA; PROBES.jsonl/log |
| `python -B out/extra_review.py extra` | 0 | 41 probe đạt, gồm lease H thật thêm workflow, hai jobs files, mốc/hash state; EXTRA.jsonl/log |
| Python heredoc gọi `suite(..., ['stdout_cp1252','stdout_cp1258'])` từ out/run_review.py | 0 | 2/2 PASS; CODEPAGES.jsonl/log/stderr |
| `python -B out/copy/.claude/dev/ci_dang_ky_test.py` | 0 | PHẢN CHỨNG: 1070/1070 đỏ đúng; TỔNG: ĐẠT; CI_DANG_KY.log/stderr. Đây là kiểm registry/hợp đồng, không phải đã chạy toàn CI. |
| `python -B out/copy/.claude/dev/packet_loop.py doctrine-scan --root out/copy` | 0 | 10 tệp, 0 chỗ chép doctrine; doctrine-scan.log |
| `python -B out/copy/.claude/dev/packet_loop.py adr-song --root out/copy` | 0 | 55 ADR / 55 dòng, khớp 1–1; ngoại lệ 0016 khai sẵn; adr-song.log |
| `git -C src diff --check 356eb26 8ac10ce` | 0 | sạch whitespace |
| `git -C src diff --numstat 356eb26 8ac10ce` | 0 | 3 tệp, 447 thêm / 5 xoá |
| `git -C src diff 742ba39 8ac10ce -- <ba tệp write set>` | 0 | output rỗng; merge không đổi write set |
| `python -B out/finalize_review.py` | 0 | đối chiếu số đo, snapshot source cuối, VERDICT và SUMMARY/ARTIFACTS |

Tổng **140 probe A/B/hành vi** hoàn tất, không tính các rig setup vào số này. Các probe âm kiểm rc, thông điệp và byte-state; các probe dương kiểm accepted_sha/hash readback, nhóm EXTRA kiểm thêm mốc endpoint. Script probe được bổ sung assertion mốc khi lượt PROBES đang chạy; lượt EXTRA chạy phiên bản có assertion đó và đo lại các baseline sạch/offline/connector cùng các trường hợp phân trang. Không coi assertion chưa chạy là bằng chứng của lượt PROBES.

Snapshot đầu/cuối **6356 tệp thường** kể cả .git: **0 delta**; không có symlink trong snapshot cuối. HEAD/tree không đổi; tracked/untracked sạch; diff worktree/index đều rc=0. `SOURCE_INITIAL.json`, `SOURCE_FINAL.json`, `SOURCE_INTEGRITY.json`. Phép này chứng minh tính toàn vẹn tại hai mốc, không khẳng định đã giám sát mọi write lịch sử.

Các artifact cấp OUT (báo cáo, script, log, diff) được băm trong `ARTIFACTS.json`. Fixture và mutant giữ lại để kiểm tra; muốn chạy lại toàn bộ, dùng OUT mới hoặc đổi tên nhóm fixture. Manifest không băm toàn bộ kho fixture.

**not_run:** full suite `python .claude/dev/packet_loop_test.py` (~45 phút), theo ưu tiên chọn lọc của prompt; không xác nhận lời khai 935/935 hoặc 1303 mutant của head cũ, không khai N/N toàn repository trên head mới. CI online, thực thi Windows, bare Ruff lint chưa chạy; dòng RUFF CI trong registry không đồng nghĩa lint đã chạy. SyntaxWarning sẵn có tại test:3714 không được tính kill/finding. Các ca được chọn không skipped.

`r812_r4_own_parent` chủ động không chạy. Hướng thử đòi soạn đường dẫn thoát cây chỉ mô tả bằng lời: tham chiếu receipt/readback đi lên hoặc symlink dẫn ngoài gốc cần được từ chối có kiểm soát và giữ nguyên state. Không tự soạn payload, không suy kết luận an toàn đường dẫn từ phép chưa chạy.

Ngoài phạm vi, không phân hạng: mo-lai, cho_chu_kho, checkpoint #813, vòng P3 #814, generation #815, ghi đẩy/kích hoạt #816 và nợ #929 nêu trong prompt. Verdict chỉ neo commit dòng 2, **không cấp quyền push/merge/land**.
