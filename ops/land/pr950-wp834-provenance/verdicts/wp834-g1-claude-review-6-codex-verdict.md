Verdict: request_changes
Reviewed commit: 394d24787aaa5b4e4638b0820b42fe25b6f0432c
Spec sha256: c57ef4d86592218729b811efede7909803d75b6d18ca0d0c3e5059848b44a9d2; Chung sha256: 4e3d1e1b3f6a0b60b96ad7b70f0ece97eca4bb3d6d10defeab1cd24ac6d1cbf0

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn lượt 5: `tham-chieu/VERDICT-luot5.md`, sha256 `982379835f0318a8a1bce8ff839957ff6f315a53cec411835b141563016bde2e`, reviewed commit `19a862bb7cedb7c880532f818661162ff04fde97`. Đã đọc toàn văn prompt.snapshot, đặc tả con/phần chung, verdict trước và đầu vào thiết kế #812; review toàn diff base→head và diff riêng lượt 6.

| lớp/biểu hiện lượt 5 | kết luận lượt 6 | phép đo độc lập |
|---|---|---|
| F6 `ci-attempt-provenance-missing`: run attempt 1 xanh nhưng jobs đã có attempt 2 | **đóng — ĐÃ VÁ THẬT** trong phạm vi lỗi trước | `PROBES2.jsonl`: sáu biến thể (một/hai file × job mới in_progress/failure/success) đều rc=12, “jobs có attempt mới hơn”, state nguyên byte. Attempt 2 đủ/xanh, attempt 2 kèm jobs cũ, và attempt mới thuộc run khác đều rc=0. Mutant gỡ chốt mới chết đúng ở `r834_jobs_attempt_moi_hon`. |
| F2: cho phép `connector_refs` lặp | **đóng biểu hiện — ĐÃ VÁ THẬT** | `r834_refs_lap` giết mutant tập hoá refs: AssertionError đòi 11, được 0. Probe A/B: candidate 11/phủ ĐÚNG, mutant 0/accepted; ref lặp giữa hai slug cũng bị candidate bác. |
| F2: quyết định P3 thiếu trường | **đóng biểu hiện — ĐÃ VÁ THẬT** | `r834_qd_thieu_truong` giết mutant nới tập trường: AssertionError đòi 2, được 0. Probe A/B với đúng phép bỏ kiểm cũ cũng phân biệt candidate 2 và mutant 0 khi thiếu owner. |
| F2 ở cấp lớp | **còn mở — vá một phần** | Cả ba mutant tự thêm `ignore_job_run_id`, `ignore_invalid_ref_entries`, `ignore_p3_value_types` đều sống **60/60 mỗi mutant**; A/B chứng minh tác động thực. Hai biểu hiện cũ đã đóng, nhưng chưa đóng toàn lớp F2. |

F4 `connector-parser-mutant-false-credit` không tái mở: control chủ ý phá capture group của parser được `r834_sach_accepted` phân loại **TIN_DUNG_GIA / CliSapDo / IndexError**, không tính kill. F5 `stop-validation-order` không tái mở trong các phép đo: JSON hỏng, biên nhận H sai, quyết định P3 thiếu hoặc không mã hoá được đều bị bác trước sentinel `_xet_dung`, giữ nguyên byte.

**Kết luận: 0 P0, 0 P1, 1 P2, 0 P3 còn mở ⇒ request_changes.** Không có lớp nguyên nhân mới so với tập còn mở lượt 5; có ba biểu hiện độ phủ mới thuộc F2 kế thừa. Trong hai lớp còn mở lượt 5, F6 đóng hoàn toàn trong phạm vi đã đo, F2 còn mở: đóng 1/2 lớp. Không đếm các biểu hiện thành nhiều finding.

## Bảng lớp còn mở

`pl` = `.claude/dev/packet_loop.py`; `test` = `.claude/dev/packet_loop_test.py`. Các dòng neo exact head ở dòng 2. Đây là thiếu nghiệm thu, **không phải candidate hiện tại đang nhận các đầu vào sai được nêu**.

| slug | hạng | biểu hiện file:dòng | phép đo/tái hiện đã chạy | hướng vá |
|---|---|---|---|---|
| `required-mutation-coverage-missing` (F2, kế thừa) | **P2** | test:8605, test:8808; chốt pl:2852, pl:2881, pl:2904 | Ba mutant riêng: **60/60 r834 vẫn PASS trên từng mutant**. Các probe A/B có candidate rc=12/11/2 và mutant rc=0/accepted. `CONFIRM.jsonl`: ba ca reviewer đề xuất PASS trên candidate, GIẾT đúng mutant bằng AssertionError. | Thêm ca r834 đổi đúng một yếu tố và mutant: job có run_id int khác; refs có một phần tử sai bên cạnh ref đúng; giá trị owner là int hoặc trắng. Giữ các chốt sản phẩm; gộp/parameter hoá test để không vượt 450 dòng. |

### F2 — phạm vi và cách tái hiện

Baseline dựng thật init → lease H/Đ/R trong kho Git giả cục bộ → receipt approve → approved_pending, đủ năm job/check-run xanh, connector sạch hoặc một P3 có H và quyết định đủ. Chỉ thay một yếu tố:

1. `ignore_job_run_id`: job 200 đổi `run_id` từ 100 sang 90, giữ attempt/head/name/check URL. Candidate trả 12/“VẮNG”; mutant bỏ riêng cặp `run_id` khỏi phép nối pl:2852 nhận `accepted`. Đây là kiểm nhất quán R theo I7/M2; không yêu cầu xác thực GitHub ngoài mô hình tin cậy.
2. `ignore_invalid_ref_entries`: bên cạnh ref hợp lệ `['review_comments', 11]`, thêm `['invalid_endpoint', 11]`. Candidate trả 11/“phủ ĐÚNG”; mutant gỡ `len(refs) != sum(...)` bỏ qua phần tử không hợp lệ sau bước lọc và vẫn `accepted`. Ca `refs_thua` hiện hữu chỉ thêm ref đúng kiểu/endpoint nên không bảo vệ chốt này.
3. `ignore_p3_value_types`: quyết định đầy đủ khoá, chỉ đổi `owner` thành số 123. Candidate trả 2/“P3 còn mở”; mutant gỡ kiểm mọi giá trị là chuỗi không trắng ghi `accepted` với owner số. Ca thiếu owner và ca Unicode hiện có không bảo vệ kiểu/trắng của các giá trị hợp lệ về mã hoá.

Cặp neo/thay nguyên văn: `audit_review.py::definitions` và các bản ghi `kind=mutation`. Bản thử và ca đề xuất ở OUT, không áp lên executor. `confirm_review.py` dùng đúng `_r834_ca` để đo rc, thông điệp và byte-state; không tính setup/CLI sập làm kill.

Hướng vá ở test: dùng `_r834_ca(12, ..., 'VẮNG')` đổi run_id; `_r834_ca(11, ..., 'phủ ĐÚNG', p3_cn=True)` thêm ref hỏng mà vẫn giữ ref đúng; `_r834_ca(2, ..., 'P3 còn mở', lop=(('a-b','P3'),))` đổi owner sang int. Các ca này đã chạy ở `CONFIRM.jsonl`. Rủi ro: xoá cả ref hợp lệ sẽ chết ở chốt phủ tập thay vì chốt đang cần đo; thiếu quyết định hoặc biên nhận ở fixture sẽ chết sớm; biến run_id thành float chỉ đo chốt kiểu đã có. Không nới gate để tiết kiệm dòng; diff đang 447/450.

## Định danh và phạm vi đo

- HEAD `394d24787aaa5b4e4638b0820b42fe25b6f0432c`; tree `a26d0f2d75dc30de48ea63510c8fb12ee15aa999`; cha `19a862bb7cedb7c880532f818661162ff04fde97`. Base và origin/master đều `ab344da5f07cce673d97056b70b002911c4d5082`, là tổ tiên (rc=0). Detached (`symbolic-ref` rc=1), không shallow, `.git` là thư mục. Băm hai spec từ bytes worktree và blob exact head đều khớp dòng 3.
- Lease bản chép r1/g1, sensitive, executor Claude/họ claude, reviewer Codex/họ openai, mục tiêu cross_approved. Reviewer phiên này là Codex/OpenAI; thực thi shell cục bộ qua công cụ, transport machine. Không có telemetry độc lập xác nhận exact model/effort/session ID hoặc nhãn riêng codex_cli; không suy danh tính từ người đăng, không phát hành receipt assurance thay launcher.
- Offline, không GitHub/mạng, không push remote thật. Fetch/push trong fixture chỉ dùng bare repository dưới OUT, với `GIT_ALLOW_PROTOCOL=file`. Đặt `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR=OUT/tmp`, Git global/system cô lập; `core.abbrev=7` trên bản sao. SRC chỉ đọc; mọi code thử, fixture, mutant và log ở OUT. Sandbox thực tế workspace-write; ràng buộc chỉ ghi OUT được giữ trong các thao tác review.
- `CHECKS.json` ghi command/rc/runtime; log JSONL lưu cả CLI con, stdout, stderr, tên ca và loại ngoại lệ. Trạng thái thông qua kiểm hash và marker dương, không chỉ mã thoát runner.

| tệp đổi | thêm | xoá |
|---|---:|---:|
| `.claude/dev/packet_loop.py` | 181 | 1 |
| `.claude/dev/packet_loop_test.py` | 262 | 3 |
| `docs/PROTOCOL_DA_PHIEN.md` (chỉ §4) | 4 | 1 |
| **Tổng** | **447** | **5** |

Đúng write set, đúng ba đường dẫn, 447≤450. `diff --check` rc=0. `CANDIDATE.diff` và `PATCH.diff` giữ hai phạm vi diff đã review.

## Đối chiếu I1–I11 và M1–M5

| mục | kết quả và giới hạn |
|---|---|
| I1 / M1 | Accept đo ls-remote hạng Đ, remote lệch bị rc=5. Fixture đi qua lease/receipt H thật. Dương ghi accepted_sha, quyết định P3, mốc từng endpoint và hash CI/connector đúng; probe kiểm lại các hash từ bytes. |
| I2 | Không sửa cửa lease. Regression r812 kiểm H/holder/readback; chỉ dùng remote file của fixture. Không khẳng định đã xác minh lease đang có trên dịch vụ thật. |
| I3 / M3 | `lop=[]` và connector sạch được nhận; thiếu bằng chứng hoàn tất bị bác. Ma trận P0/P1/P2, Q1/P 1/P4/p3 và hai hạng trên cả ba endpoint đều bị bác. Review comment thiếu badge và CHANGES_REQUESTED thiếu hạng bị bác. Check/run/job không success không đạt. |
| I4 | Tất cả probe từ chối của candidate kiểm byte-state; gồm từ chối muộn ở H, quyết định P3, Unicode, JSON hỏng/khóa trùng/NaN. Mutant ghi state sớm bị giết bằng assertion I4. Không khái quát thành chứng minh mọi đầu vào vô hạn. |
| I5 / M1 | Gọi helper chung sau xác thực CI/connector/H/P3 và tiền kiểm UTF-8. Mutant bỏ gọi, gọi sớm trước đầu vào/H/encoding đều chết đúng; các probe với sentinel cũng xác nhận thứ tự. |
| I6 | Không mở quyền checkpoint/generation/mở lại/ngoại lệ đẩy. Các packet sau ngoài phạm vi, không bị đòi triển khai ở đây. |
| I7 / M2 | Kiểm app/workflow/job, newest run và attempt, repo/head, job URL → check-run, suite, check mới nhất và gọi lại kiem-gate. F6 trước đã đóng cả một/hai file và failure. Ba đối chứng cho attempt 2 xanh, jobs cũ và run khác đạt. F2 còn thiếu test bảo vệ so run_id. |
| I7 / M3 | `_trang_du` kiểm tập ID riêng endpoint, cùng ID/nội dung được nhận, mâu thuẫn bị bác cả xuyên trang và xuyên file jobs. Prefix Reviewed commit 7/10/40, bare/backtick đều nhận; suffix thừa/mơ hồ bị bác. P1 neo head cũ được bỏ qua ở cả ba endpoint; phần tử khác repo bị bác. Review hoàn tất đơn độc đạt, PENDING/DISMISSED/ngoài miền đơn độc không được tính xong. |
| I8 | Connector H gọi lại `_du_dieu_kien_approve`, dùng chuẩn hoá canon. Regression r812 về identity/provider/family/surface/transport đạt. |
| I9 | 148 ca r812 và 10 ca r929 được chọn đều đạt; 2 ca stdout cp1252/cp1258 đạt, gồm chuỗi tới accept mới. Có đo init chưa lease và đường legacy. Full suite chưa chạy, không khai N/N toàn repository. |
| I10 / M4 | Biên nhận connector là ứng viên: sai packet/generation/sha/spec_hash/role đều rc=11, nguyên byte. Không lấy nguồn của generation khác thay ứng viên. |
| I11 / M4 | P3 ở cả ba endpoint được nối slug H và nhận khi quyết định đủ. Thiếu/thừa/lặp/sai kiểu refs và thiếu/trùng/thừa/sai kiểu/trắng quyết định bị candidate bác; F2 còn test chưa bảo vệ phần tử refs bị lọc và kiểu giá trị quyết định. |
| M5 | Protocol chỉ thêm cửa accept có điều kiện ADR-0054 ở §4, giữ đường cũ. Packet không kích hoạt ADR-0054. |

Đối chiếu bốn lớp thiết kế #812: `connector-verdict-incomplete`, `conflicting-evidence-overwrite`, phần connector của `findings-not-receipt-bound` và hành vi `ci-attempt-provenance-missing` đã bị chặn trong các phép đo tương ứng. F2 là thiếu nghiệm thu độc lập, không đổi tên thành lỗi sản phẩm của các lớp này.

#929 đã có ở base: `_che_do_0054` quét cụm khai, không ghim số tệp kích hoạt. Đặc tả con/phần chung không đòi số tệp cố định; I9 vẫn xác định chế độ ở đường record-lease mới. Không thấy mâu thuẫn cần dừng. Nợ `ls[0] == 0` ngoài phạm vi theo prompt.


## Đối chiếu từng ca bắt buộc `nghiem_thu`

Tên ca/mutant trong bảng lược tiền tố `r834_`. Mọi ca nền dưới đây PASS; mọi mutant đích chết vì assertion đúng hành vi, không vì traceback. Ca âm kiểm state nguyên byte.

| yêu cầu | ca | mutant | phép đo nền → mutant |
|---|---|---|---|
| approve sạch lop=[] và connector sạch → accepted | sach_accepted | bo_ket_luan_issue_comment | 0/accepted → 12/chưa xong, AssertionError đòi 0 |
| remote khác pending_sha | dau_nhanh_lech | bo_dau_nhanh_remote | 5/≠pending → 0 |
| check bắt buộc vắng | check_vang | job_vang_bo_qua | 12/VẮNG → 0 |
| cùng tên từ app khác | check_app_khac | bo_app | 12/không từ app → 0 |
| cùng tên workflow khác, cùng app | check_workflow_khac | bo_path_workflow | 12/VẮNG → 0 |
| rerun đang chạy, check cũ xanh | rerun_dang_chay | bo_attempt_moi_nhat | 12/chưa xanh → 0; mutant phối hợp đã neo lại đúng sau vá |
| check-run kho khác | check_kho_khac | bo_kho_check_run | 12/kho khác → 0 |
| readback PR khác cùng head | pr_khac_cung_head | bo_neo_pr_phan_tu | 12/không thuộc → 0 |
| PENDING không là xong | review_pending | pending_la_xong | 12/chưa xong → 0 |
| CHANGES_REQUESTED có P1 | review_changes_p1 | bo_finding_review | 12/còn P1 → 0 |
| issue comment có P1 | issue_comment_p1 | bo_finding_issue_comment | 12/còn P1 → 0 |
| cùng ID, P1 rồi P3 | cung_id_hai_noi_dung | bo_nhat_quan_id | 12/hai nội dung → 0 |
| workflow run cùng ID, khác path | run_cung_id_khac_path | bo_nhat_quan_id | 12/hai nội dung → 0 |
| P3 offline thiếu quyết định | p3_offline_thieu_qd | bo_p3_offline | 2/P3 còn mở → 0 |
| P3 connector thiếu quyết định | p3_connector_thieu_qd | bo_p3_connector | 2/P3 còn mở → 0 |
| P3 connector thiếu slug từ H | p3_connector_khong_slug | khoa_id_so | 11/cần biên nhận → 0 |
| bằng chứng dương rỗng | bang_chung_duong_rong; state_required_checks_rong | bo_bang_chung_duong; bo_luoc_do_state | 12/chưa xong; 8/state hỏng → 0 |
| đầu vào hỏng giữ byte | dau_vao_hong_state_nguyen | ghi_truoc_khi_doc | nền 12/JSON hỏng; mutant cùng rc nhưng assertion I4: state đổi |

Đủ các ca liệt kê không thay phép tự đột biến: ba chốt chưa được ca nào bảo vệ vẫn là F2. Ca reviewer không được tính thay ca bắt buộc trong candidate.

## Đột biến khai báo — đo từng quan hệ mutant/ca

Đo thực tế **54 khóa r834 + r812_bo_generation = 55 mutant**, **61 quan hệ đích GIẾT đúng**, 0 SỐNG, 0 TÍN DỤNG GIẢ. Lời khai “55 r834 + r812” lớn hơn một khóa; báo số đo, không tính sai số đếm này thành lớp finding. Mỗi mỏ neo có đúng một chỗ khớp, mọi bản mutant compile được. `DECLARED.jsonl` giữ nguyên CLI rc/stdout/stderr và cặp neo/thay.

| mutant | ca đích | phân loại | ngoại lệ/lý do thực |
|---|---|---|---|
| r812_bo_generation | r812_bien_nhan_lech_generation | GIET | AssertionError: r812 review ['bn']: đòi rc=11, được rc=0; stderr='' |
| r812_bo_generation | r834_bnc_lech_generation | GIET | AssertionError: r834 accept: đòi rc=11, được rc=0; stderr='' |
| r834_bo_ket_luan_issue_comment | r834_sach_accepted | GIET | AssertionError: r834 accept: đòi rc=0, được rc=12; stderr='connector chưa xong trên a64d6c9155db16fbf3a30eca6ca70ab440803280: không review hoàn tất/kết luận nào của chatgpt-codex-connector[bot]' |
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
| r834_bo_review_xong | r834_review_hoan_tat_don_doc | GIET | AssertionError: r834 accept: đòi rc=0, được rc=12; stderr='connector chưa xong trên a64d6c9155db16fbf3a30eca6ca70ab440803280: không review hoàn tất/kết luận nào của chatgpt-codex-connector[bot]' |
| r834_bo_attempt_jobs_moi | r834_jobs_attempt_moi_hon | GIET | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_refs_theo_tap | r834_refs_lap | GIET | AssertionError: r834 accept: đòi rc=11, được rc=0; stderr='' |
| r834_qd_thieu_truong_lot | r834_qd_thieu_truong | GIET | AssertionError: r834 accept: đòi rc=2, được rc=0; stderr='' |


## Đột biến kiểm toán và đối chứng

| mutant tự thêm | toàn bộ r834 | A/B trên đầu vào chỉ đổi một yếu tố | ca đề xuất |
|---|---|---|---|
| ignore_job_run_id | 60/60 PASS — SỐNG | 12/VẮNG, nguyên byte → 0/accepted | reviewer_ignore_job_run_id: candidate PASS, mutant AssertionError đòi 12 được 0 |
| ignore_invalid_ref_entries | 60/60 PASS — SỐNG | 11/phủ ĐÚNG, nguyên byte → 0/accepted | reviewer_ignore_invalid_ref_entries: candidate PASS, mutant AssertionError đòi 11 được 0 |
| ignore_p3_value_types | 60/60 PASS — SỐNG | 2/P3 còn mở, nguyên byte → 0/accepted | reviewer_ignore_p3_value_types: candidate PASS, mutant AssertionError đòi 2 được 0 |

Hai mutant cũ được dựng lại bằng đúng phép gỡ chốt lượt 5: `old_allow_missing_p3_fields` và `old_allow_duplicate_connector_refs`. Ca mới tương ứng đều GIẾT đúng; không suy từ mutant nới tập trường thành kiểm bỏ hẳn tập trường. Control `crashing_parser_control` bị `CliSapDo: ... IndexError: no such group`, phân loại **TIN_DUNG_GIA**, tách khỏi 61 kill khai báo.

`PROBES2.jsonl` có 88/88 phép đo đạt rc/lý do/byte/accepted hashes; `EXTRA.jsonl` có 61/61; `AUTHENTIC.jsonl` có 4/4 cùng baseline lease Git thật. Tổng **153 probe** hoàn chỉnh; các rig dương được kiểm riêng, không gộp thêm vào số probe. Lần đầu `PROBES` dừng ở assertion của **script reviewer** do đòi chữ `packet_issue` trong thông điệp thực là `packet`; rc sản phẩm vẫn đúng 11. Đã sửa kỳ vọng, chạy lại trọn vẹn thành `PROBES2`, giữ nguyên log lỗi đầu; không tính nó thành finding hay mutant kill.

## Lệnh, rc và bằng chứng dương

Chạy từ thư mục có src/out/tham-chieu. Mọi script dùng `out/copy`, mutant hoặc kho giả dưới OUT; các runner đặt TMPDIR trong OUT. rc=0 của audit nghĩa thu thập hoàn tất, **không** có nghĩa nghiệm thu đạt khi mutant không tương đương còn sống.

| lệnh | rc | kết quả / hiện vật |
|---|---:|---|
| python -B out/run_review.py declared | 0 | 60/60 nền; 55 mutant/61 quan hệ GIẾT đúng; DECLARED.jsonl/log/stderr |
| python -B out/run_review.py regression | 0 | 148/148 r812 + 10/10 r929; REGRESSION.jsonl/log/stderr |
| python -B out/audit_review.py ignore_job_run_id | 0 | 60/60 PASS trên mutant — nghiệm thu FAILED; IGNORE_JOB_RUN_ID.jsonl/log |
| python -B out/audit_review.py ignore_invalid_ref_entries | 0 | 60/60 PASS trên mutant — nghiệm thu FAILED; IGNORE_INVALID_REF_ENTRIES.jsonl/log |
| python -B out/audit_review.py ignore_p3_value_types | 0 | 60/60 PASS trên mutant — nghiệm thu FAILED; IGNORE_P3_VALUE_TYPES.jsonl/log |
| python -B out/audit_review.py old_allow_missing_p3_fields | 0 | ca mới GIẾT đúng mutant cũ; OLD_ALLOW_MISSING_P3_FIELDS.jsonl/log |
| python -B out/audit_review.py old_allow_duplicate_connector_refs | 0 | ca mới GIẾT đúng mutant cũ; OLD_ALLOW_DUPLICATE_CONNECTOR_REFS.jsonl/log |
| python -B out/probe_review.py probes | 1 | script reviewer sai kỳ vọng từ khóa, không lỗi candidate; PROBES.jsonl/log/stderr |
| python -B out/probe_review.py probes2 | 0 | 88/88 probe; PROBES2.jsonl/log/stderr |
| python -B out/extra_review.py extra | 0 | 61/61 probe bổ sung; EXTRA.jsonl/log/stderr |
| python -B out/authentic_lease_review.py authentic | 0 | lease thật thêm required check → đủ 6 check đạt, thiếu workflow/jobs hoặc job đỏ bị bác; AUTHENTIC.jsonl/log |
| python -B out/confirm_review.py confirm | 0 | 3 baseline đề xuất PASS, 3 mutant GIẾT đúng, 1 control TÍN DỤNG GIẢ; CONFIRM.jsonl/log |
| python -B out/checks_review.py checks | 0 | 2/2 stdout cp1252/cp1258; CHECKS.json/jsonl/log |
| python -B out/copy/.claude/dev/packet_loop.py doctrine-scan --root out/copy | 0 | 10 tệp, 0 chỗ chép doctrine; doctrine-scan.log |
| python -B out/copy/.claude/dev/packet_loop.py adr-song --root out/copy | 0 | 55 ADR / 55 dòng khớp 1–1, ngoại lệ 0016 khai sẵn; adr-song.log |
| git -C src diff --check ab344da 394d247 | 0 | không lỗi whitespace |
| git -C src diff --numstat ab344da 394d247 | 0 | 3 tệp, 447 thêm / 5 xoá |
| python -B out/finalize_review.py finalize | 0 | kiểm số đo, snapshot cuối, bảng đối chiếu và SUMMARY.json |

Snapshot đầu/cuối **6017 tệp/link** kể cả .git, **0 delta**; HEAD/tree và tracked/untracked/ignored sạch, worktree/index diff rc=0. `SOURCE_INITIAL.json`, `SOURCE_FINAL.json`, `SOURCE_INTEGRITY.json`. Chỉ chứng minh hai mốc không có delta, không chứng minh toàn lịch sử chưa từng ghi rồi hoàn nguyên. `ARTIFACTS.json` băm các báo cáo/log/script/diff sau khi các writer hoàn tất.

Các runner giữ fixture để kiểm tra lại, không tự xoá. Muốn chạy lại, dùng OUT mới với bản sao `copy/` tương ứng hoặc đổi tên nhóm fixture; không chạy đè các kho giả đã có. Manifest ghi phạm vi hiện vật cấp OUT và mã mutant, không băm toàn bộ mọi kho fixture.

**not_run:** full suite `python .claude/dev/packet_loop_test.py` (~45 phút), theo ưu tiên chọn lọc của prompt; không xác nhận lời khai 932/932 trên head cũ và không khai N/N toàn kho trên head mới. CI online, Windows execution, bare Ruff lint và Ruff pin/probe contract chưa chạy; không gộp thành “Ruff passed”. SyntaxWarning sẵn có tại test:3714 không được tính kill hoặc finding. Các ca đã chọn không có skipped; một ca r812 chủ động not_run theo giới hạn bên dưới.

`r812_r4_own_parent` không chạy. Hướng đòi soạn đường dẫn thoát cây chỉ mô tả bằng lời: receipt/readback qua đường dẫn đi lên hoặc symlink dẫn ra ngoài gốc phải bị từ chối có kiểm soát, giữ state nguyên byte. Không dựng payload và không suy an toàn đường dẫn từ phép chưa chạy.

Ngoài phạm vi, không phân hạng: mo-lai, cho_chu_kho, checkpoint #813, vòng P3 #814, generation #815, ghi đẩy/kích hoạt #816 và nợ #929 nêu trong prompt. Verdict chỉ neo commit dòng 2, **không cấp quyền push/merge/land**.
