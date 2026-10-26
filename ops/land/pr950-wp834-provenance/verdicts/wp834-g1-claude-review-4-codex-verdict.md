Verdict: request_changes
Reviewed commit: dcb77e78113ed66641771a82f404b713c9602d4d
Spec sha256: c57ef4d86592218729b811efede7909803d75b6d18ca0d0c3e5059848b44a9d2; Chung sha256: 4e3d1e1b3f6a0b60b96ad7b70f0ece97eca4bb3d6d10defeab1cd24ac6d1cbf0

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn: `tham-chieu/VERDICT-luot3.md`, sha256 `d452fd8bd7898faa4a905714fcc016336211a46e9b60684be578f0550d3bca72`, reviewed commit `7436fe3b1ee0fc54190c7cd50d3be06c41790ee5`. Đã đọc toàn văn prompt snapshot, hai đặc tả, toàn bộ diff base→head và diff vá 7436fe3→dcb77e7. Không dùng lời khai executor làm bằng chứng đóng lớp.

| slug còn mở lượt 3 | kết luận lượt 4 | phép đo độc lập |
|---|---|---|
| `required-mutation-coverage-missing` (F2, P2) | **còn mở — đã vá một phần / VÁ HỜ ở cấp lớp** | Ba mutant sống lượt 3 nay đều bị ca mới giết đúng lý do. Tuy nhiên ba mutant bổ sung vẫn sống **54/54 ca mỗi mutant**: bỏ check bổ sung trong lease; so chéo ID giữa endpoint; bỏ nhánh nhận review hoàn tất. Các probe A/B phân biệt cả ba; chi tiết bên dưới. |
| `connector-parser-mutant-false-credit` (F4, P2) | **đóng — ĐÃ VÁ THẬT** | `CONFIRM.jsonl`: parser mutant hiện hành giữ capture group; control sạch qua và hai ca parser đỏ bằng AssertionError đòi 12, được 0. Dựng lại mutant thiếu group của lượt 3: control sạch và hai ca parser trả CLI rc=1/IndexError, nay đều được phân loại **TIN_DUNG_GIA/CliSapDo**, không cấp kill. |
| `stop-validation-order` (F5, P2) | **đóng — ĐÃ VÁ THẬT** | `PROBES.jsonl`: surrogate đơn trong từng trường ten_no/owner/huong/ly_do đều rc=2, thông điệp UnicodeEncodeError, state nguyên byte và **không** tới hook `_xet_dung`. Hook in marker rồi gọi tiếp hàm gốc; Unicode Việt/emoji hợp lệ tới hook và accepted/0. Mutant bỏ tiền kiểm encode bị `r834_qd_khong_ma_hoa` giết: đòi 2, được sentinel 3. |

**Còn mở: 1 lớp — 0 P0, 0 P1, 1 P2, 0 P3.** Lớp cũ F2 có ba biểu hiện mới về độ phủ; **0 lớp mới** được tách riêng và chưa thấy lỗi hành vi mới do bản vá sinh ra trong phạm vi đã đo. Không đạt ngưỡng approve vì còn P2.

### Đo lại ba mutant sống lượt 3

Đã dựng lại đúng phép biến đổi trên head mới, kiểm neo duy nhất, compile, chạy ca đích mới của candidate; kết quả ghi riêng trong `CONFIRM.jsonl`. Không khai đã chạy cả 54 ca trên mỗi mutant cũ: một ca giết đúng đã chứng minh nó không còn sống.

| mutant lượt 3 | ca giết trên head này | ngoại lệ và lý do |
|---|---|---|
| stop_before_H_and_P3 | r834_xet_dung_sau_h | AssertionError: đòi rc=11/generation, được rc=3/COC_XET_DUNG |
| omit_job_completed_success | r834_job_chua_xanh | AssertionError: đòi rc=12/chưa xanh, được rc=0/accepted |
| accept_p1_review_comment | r834_review_comment_p1 | AssertionError: đòi rc=12/còn P1, được rc=0/accepted |

## Bảng lớp còn mở

`pl` = `.claude/dev/packet_loop.py`; `test` = `.claude/dev/packet_loop_test.py`; dòng theo exact head. Đếm theo nguyên nhân, không theo số biểu hiện.

| slug | hạng | biểu hiện file:dòng | phép đo/tái hiện đã chạy | hướng vá |
|---|---|---|---|---|
| `required-mutation-coverage-missing` (F2, kế thừa) | P2 | test:8560 (fixture `_r834`); test:8694 (hai file jobs nhưng workflow thứ hai không bắt buộc); pl:2843, pl:2804, pl:2814 (chốt chưa được suite bảo vệ) | `AUDIT.jsonl`: cả `ignore_lease_required_checks`, `cross_endpoint_id_space`, `omit_completed_review` sống 54/54. `CONFIRM.jsonl`: lease Git thật yêu cầu thêm workflow, candidate rc=12/VẮNG nhưng mutant thứ nhất accepted/0. `PROBES.jsonl` và `EXTRA.jsonl`: candidate nhận ID bằng nhau ở hai endpoint và nhận review hoàn tất đơn độc; hai mutant sau từ chối sai rc=12. | Bổ sung/đổi fixture r834 để đo check ngoài hằng, hai endpoint chung ID, review hoàn tất không issue comment; mỗi ca có mutant đúng tính chất. Tái dùng helper/parameter hoá trong 18 dòng dư hoặc giảm phần lặp hiện có; không cần đổi logic sản phẩm cho các phản chứng này. |

Đây là lỗi **nghiệm thu/độ phủ**, không phải kết luận bản gốc đang bỏ check, trộn không gian ID hoặc bỏ review. Bản gốc xử lý đúng các probe. Các bất biến bị bỏ lọt được đặc tả nói trực tiếp: M1 là hằng **hợp** required_checks của lease; M3/I7 đếm ID riêng theo endpoint và cho review hoàn tất làm bằng chứng xong. Cả ba vẫn có thể bị phá mà toàn bộ r834 xanh, nên không thể đóng F2 chỉ bằng tổng 54/54 và các mutant được liệt kê sẵn.

### Phản chứng và ca khoá F2

| mutant tự dựng | phép biến đổi trên bản sao | suite candidate | probe candidate / mutant |
|---|---|---|---|
| ignore_lease_required_checks | Tại đầu `_kiem_ci`, bản chiếu nc chỉ còn CHECK_BAT_BUOC | 54/54 PASS ⇒ **SỐNG** | Lease thật thêm `(.github/workflows/extra.yml, extra)` qua record-lease + receipt approve: 12/VẮNG, nguyên byte / 0/accepted. Đối chứng cung cấp đủ run/job/check của workflow thứ hai và hai file jobs: 0/accepted. |
| cross_endpoint_id_space | Thêm phép so số ID toàn cục với tổng số phần tử các endpoint trước vòng kiểm URL | 54/54 PASS ⇒ **SỐNG** | P3 review_comment ID=11 và kết luận sạch issue_comment ID=11, H/qd đầy đủ: 0/accepted / 12/id trùng xuyên endpoint, nguyên byte. |
| omit_completed_review | Thay nhánh `or any(... reviews ...)` của bằng chứng xong bằng False | 54/54 PASS ⇒ **SỐNG** | Chỉ một APPROVED review sạch, đúng head, không issue comment: 0/accepted / 12/connector chưa xong, nguyên byte. |

`run_review.py` nhánh `audit` chứa cặp neo/thay đầy đủ; `AUDIT.jsonl` lưu các định nghĩa và kết quả từng ca, bao gồm lệnh CLI/rc/stdout/stderr. Các mutant là dữ liệu thử trên bản sao, không phải patch sản phẩm. `CONFIRM.jsonl` còn lưu ngữ cảnh required_checks lấy từ lease Git thật, tránh suy chỉ từ state tự dựng. `probe_review.py` dùng bản sao trạng thái cho ma trận CLI; phần lease thật được kiểm riêng bởi `run_review.py confirm`.

Vá ở **test** vì chốt sản phẩm đang đúng. Hướng ít tăng diff nhất là nâng `r834_hai_tep_jobs` thành hai workflow thật sự bắt buộc, thêm biến thể thiếu/đỏ ở workflow thứ hai; parameter hoá ca connector dương cho review-only và ID bằng nhau giữa endpoint. Giữ mỗi fixture có control xanh trước khi đổi một yếu tố. Ca thêm phải giết đúng ba mutant trên bằng assertion về kết quả/lý do, không traceback; giữ các ca âm của attempt/app/URL và byte-state hiện có. Rủi ro của cách vá: fixture workflow thứ hai thiếu một liên kết khác có thể chết ở chốt phụ; ca ID trùng sai ngay trong cùng endpoint có thể vô tình đo điều khác; nhầm review PENDING thành control dương sẽ nới gate. Vì vậy giữ đầy đủ run/attempt/job/check/H và đọc stderr của từng ca. Có thể gộp sinh ca/mutant hoặc bỏ phần lặp để giữ ≤450; không đề xuất thêm production logic chỉ để làm mutant chết.

## Định danh và phạm vi đã đo

- Thư mục làm việc thực: `rv4/`, có `src/`, `out/`, `tham-chieu/`; prompt snapshot ở `runs/89a9c925/` là nguồn chỉ dẫn, không phải SRC.
- HEAD `dcb77e78113ed66641771a82f404b713c9602d4d`; tree `94384584359100dfe04db9ec3c36cba18cba3703`.
- `refs/remotes/origin/master` = base `ab344da5f07cce673d97056b70b002911c4d5082`; base ancestor rc=0; HEAD detached (`symbolic-ref -q HEAD` rc=1 đúng kỳ vọng); không shallow; `.git` là thư mục.
- Hai SHA-256 đặc tả đúng dòng 3. Băm verdict lượt 1/2/3 cũng khớp prompt. Lease bản chép ghi r1/g1, executor Claude, review class sensitive; review này không xác minh lại lease live.
- Reviewer Codex, họ openai, dùng shell cục bộ qua công cụ của phiên, transport machine; độc lập với context executor. Không có telemetry độc lập trong đầu vào để chứng minh exact model/effort/session identity hoặc xác nhận surface `codex_cli`; không tự cấp assurance `cross_approved`. Đây là mục tiêu assurance của packet, khác kết luận kỹ thuật theo SHA.
- Mọi bản sao, fixture, mutant, script, log và temp đều dưới `out/`. Không truy cập mạng/GitHub; `GIT_ALLOW_PROTOCOL=file` giới hạn Git fixture tới kho cục bộ. Dùng `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR=out/tmp`, Git global/system cô lập; `core.abbrev=7` giữ trong bản sao. Python 3.13.17; Git 2.43.0; Linux.
- Snapshot đầu/cuối gồm **6.006** tệp/link, kể cả `.git`: **0 delta**. HEAD/tree không đổi; status tracked/untracked/ignored rỗng; worktree/index diff rc=0. Bằng chứng: `SOURCE_INITIAL.json`, `SOURCE_FINAL.json`, `SOURCE_INTEGRITY.json`. Giới hạn: chứng minh hai mốc không đổi, không chứng minh toàn bộ lịch sử chưa từng ghi rồi hoàn nguyên. Sandbox thực tế workspace-write; tác vụ review chỉ ghi đường dưới out.

| tệp trong diff base→head | thêm | xoá |
|---|---:|---:|
| .claude/dev/packet_loop.py | 181 | 1 |
| .claude/dev/packet_loop_test.py | 247 | 3 |
| docs/PROTOCOL_DA_PHIEN.md (§4) | 4 | 1 |
| Tổng | **432** | **5** |

Đúng ba đường dẫn và 432≤450. `git diff --check` rc=0. Toàn bộ diff được lưu tại `CANDIDATE.diff`, bản vá lượt này tại `PATCH.diff`. Không sửa nguồn hoặc áp hint vào nhánh executor.

## Đối chiếu bất biến I1–I11 và M1–M5

| mục | bằng chứng / kết luận trong phạm vi đo |
|---|---|
| I1, M1 | Accept đo remote branch bằng ls-remote; khác pending rc=5. Baseline thật qua lease H/Đ/R, receipt approve và accepted. Required checks bổ sung hoạt động đúng nhưng thiếu ca chống hồi quy — F2. accepted_sha, mốc endpoint, quyết định và hash readback lưu đúng (`EXTRA.jsonl`). |
| I2 | Packet không đổi cửa lease. Fixture r834 qua cửa lease thật; 148 ca r812 được chọn kiểm thêm H/holder/readback hiện có. R không được xem là authority độc lập. |
| I3, M3 | Findings rỗng accepted; bằng chứng xong rỗng bị bác. P0/P1/P2, Q1/P 1/PX và hai hạng bị bác ở cả ba endpoint. CHANGES_REQUESTED không hạng và review_comment thiếu neo bị bác. Check conclusion ngoài success không đạt. |
| I4 | Mọi reject ở ma trận CLI và các ca nền đã đo giữ nguyên byte; gồm lỗi JSON, H muộn, P3 thiếu/trùng/thừa/sai kiểu và Unicode. Mutant ghi sớm chết bởi assertion I4. |
| I5, M1 | Có lời gọi helper chung; các mutant bỏ gọi/đổi thứ tự bị giết. Tiền kiểm encoding chạy trước helper, hook gọi tiếp hàm gốc chứng minh F5 đã đóng. Không yêu cầu thêm nhánh dừng mới cho accept. |
| I6 | Packet không tạo quyền mở lại/checkpoint/generation/ngoại lệ đẩy; không đòi triển khai packet sau. |
| I7, M2/M3 | App/workflow/job, run/attempt mới nhất, kho/head, URL job→check-run, suite, kiem-gate và phân trang được đọc mã/đo ca. Hai workflow bắt buộc với hai file jobs có đối chứng accepted. ID lặp giống nhau được nhận; mâu thuẫn bị bác; ID cùng số ở hai endpoint hợp lệ được nhận nhưng thiếu ca suite — F2. |
| I8 | `_slug_connector` tái dùng `_du_dieu_kien_approve`/validator canon và chuẩn hoá danh tính. Regression r812 có alias/family/surface/transport. Không thêm thuật toán identity khác. |
| I9 | 148/148 ca r812 được chọn đạt, gồm init chưa lease→awaiting_lease, đường lease cũ luôn false và đường review cũ. Hai ca stdout cp1252/cp1258 được đổi trong diff cũng đạt. Không khai full suite đã chạy. |
| I10, I11, M4 | H connector lệch packet/generation/sha/spec_hash/role bị rc=11 trước hook; connector_refs thiếu/trùng/thừa/sai kiểu/endpoint/id bị bác. P3 ở từng endpoint có H và qd hợp lệ được nhận. Quyết định thiếu/trùng/thừa/sai kiểu/blank/extra-key bị rc=2, nguyên byte. |
| M5 | Protocol §4 mô tả accept có điều kiện ADR-0054 và các điều kiện chính; diff chỉ ở §4. Không kích hoạt ADR-0054. |

Các lớp thiết kế #812 được giao cho packet — `connector-verdict-incomplete`, `ci-attempt-provenance-missing`, `conflicting-evidence-overwrite` và phần connector của `findings-not-receipt-bound` — không tái lộ lỗi hành vi cũ trong phạm vi đo: PENDING không làm xong; finding ở ba endpoint bị đọc; attempt/job/kho sai bị bác; cùng ID khác nội dung bị bác trước lọc/map; P3 cần slug H và quyết định. Đây không thay việc còn thiếu coverage F2.

Parser Reviewed commit nhận tiền tố 7/10/40 ký tự, dạng trần/backtick/in đậm hợp lệ; đuôi thừa hoặc code span hỏng bị bác. Tiền tố mơ hồ do full SHA khác cùng tiền tố trong readback bị bác; exact head hiện tại vẫn nhận; chỉ exact head cũ không đủ kết luận cho head hiện tại. Review/issue comment P1 ở head cũ hợp lệ không chặn kết luận sạch hiện tại. Mô hình tin cậy R chỉ kiểm nhất quán, không xác thực trực tiếp nội dung từ GitHub.

#929 có sẵn ở base: `_che_do_0054` quét cụm khai, không ghim số ADR kích hoạt. wp834/phần chung không bắt số tệp kích hoạt cố định; I9 vẫn xác định chế độ tại đường lease mới. Không tìm thấy mâu thuẫn buộc dừng giữa hai đặc tả này với #929. Nợ riêng `ls[0] == 0` nằm ngoài phạm vi theo prompt.

## Đối chiếu từng ca bắt buộc của `nghiem_thu`

Tên ca/mutant trong bảng lược tiền tố `r834_`. Tất cả ca nền đều PASS. Lý do nền là thông điệp CLI thật; mutant phải đỏ bằng AssertionError đúng kết quả/lý do/byte. Log giữ đủ stderr không cắt.

| yêu cầu bắt buộc | ca tương ứng | mutant | nền / lý do mutant đỏ |
|---|---|---|---|
| sạch lop=[] + connector sạch → accepted | sach_accepted | bo_ket_luan_issue_comment | 0/accepted; mutant 12/chưa xong, assertion đòi 0 |
| đầu remote khác pending | dau_nhanh_lech | bo_dau_nhanh_remote | 5/≠pending; mutant 0 |
| check bắt buộc vắng | check_vang | job_vang_bo_qua | 12/VẮNG; mutant 0 |
| cùng tên từ app khác | check_app_khac | bo_app | 12/không từ app; mutant 0 |
| workflow khác cùng app/job | check_workflow_khac | bo_path_workflow | 12/VẮNG; mutant 0 |
| attempt mới đang chạy, check cũ xanh | rerun_dang_chay | bo_attempt_moi_nhat | 12/chưa xanh; mutant 0. Hai hunk cùng ngữ nghĩa nới run-state + join attempt; attempt_moi_job_cu đo riêng join. |
| check-run kho khác | check_kho_khac | bo_kho_check_run | 12/kho khác; mutant 0 |
| PR khác cùng head | pr_khac_cung_head | bo_neo_pr_phan_tu | 12/không thuộc PR; mutant 0 |
| review PENDING không xong | review_pending | pending_la_xong | 12/chưa xong; mutant 0 |
| CHANGES_REQUESTED có P1 | review_changes_p1 | bo_finding_review | 12/còn P1; mutant 0 |
| issue comment có P1 | issue_comment_p1 | bo_finding_issue_comment | 12/còn P1; mutant 0 |
| cùng ID hai nội dung P1 rồi P3 | cung_id_hai_noi_dung | bo_nhat_quan_id | 12/hai nội dung; mutant 0 |
| hai run cùng ID khác path | run_cung_id_khac_path | bo_nhat_quan_id | 12/hai nội dung; mutant 0 |
| P3 offline thiếu quyết định | p3_offline_thieu_qd | bo_p3_offline | 2/P3 còn mở; mutant 0 |
| P3 connector thiếu quyết định | p3_connector_thieu_qd | bo_p3_connector | 2/P3 còn mở; mutant 0 |
| P3 connector không slug H | p3_connector_khong_slug | khoa_id_so | 11/cần biên nhận; mutant 0 |
| bằng chứng dương rỗng | bang_chung_duong_rong; state_required_checks_rong | bo_bang_chung_duong; bo_luoc_do_state | 12/chưa xong và 8/state hỏng; mutant 0 |
| input hỏng giữ byte | dau_vao_hong_state_nguyen | ghi_truoc_khi_doc | 12/JSON hỏng, byte nguyên; mutant chết bởi `AssertionError: I4: state đổi sau khi accept từ chối` |

Danh sách tối thiểu có đủ ca/kill đúng; F2 nói các nghĩa vụ M1/M3 khác vẫn chưa được suite bảo vệ. Probe reviewer không được tính thành ca đã có trong candidate.

## Mọi quan hệ mutant → ca đã chạy

Đo thực tế **48 mutant tên r834 + r812_bo_generation = 49 mutant**, **55 quan hệ** (54 đến ca r834, 1 đến r812). Tất cả 55 quan hệ GIẾT đúng; 0 SỐNG, 0 TÍN DỤNG GIẢ trong bảng mutant khai báo. Nếu lời khai “49 r834 + r812” hiểu là 50 mutant thì lệch một; đây chỉ là hiệu chỉnh số đo, không thêm lớp finding.

| mutant | ca | phân loại | ngoại lệ/lý do |
|---|---|---|---|
| r812_bo_generation | r812_bien_nhan_lech_generation | GIẾT | AssertionError: r812 review ['bn']: đòi rc=11, được rc=0; stderr='' |
| r812_bo_generation | r834_bnc_lech_generation | GIẾT | AssertionError: r834 accept: đòi rc=11, được rc=0; stderr='' |
| r834_bo_ket_luan_issue_comment | r834_sach_accepted | GIẾT | AssertionError: r834 accept: đòi rc=0, được rc=12; stderr='connector chưa xong trên 3b7cb580bc488d9adbf8940ff843084c6033e24d: không review hoàn tất/kết luận nào của chatgpt-codex-connector[bot]' |
| r834_bo_ref_connector_h | r834_p3_du_quyet_dinh | GIẾT | AssertionError: r834 accept: đòi rc=0, được rc=11; stderr="bảng lớp H phải phủ ĐÚNG từng (endpoint, id) P3 của connector [('review_comments', 11)], mỗi cặp một lần" |
| r834_bo_dau_nhanh_remote | r834_dau_nhanh_lech | GIẾT | AssertionError: r834 accept: đòi rc=5, được rc=0; stderr='' |
| r834_job_vang_bo_qua | r834_check_vang | GIẾT | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_bo_app | r834_check_app_khac | GIẾT | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_bo_path_workflow | r834_check_workflow_khac | GIẾT | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_bo_attempt_moi_nhat | r834_rerun_dang_chay | GIẾT | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_bo_kho_check_run | r834_check_kho_khac | GIẾT | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_bo_neo_pr_phan_tu | r834_pr_khac_cung_head | GIẾT | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_pending_la_xong | r834_review_pending | GIẾT | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_bo_finding_review | r834_review_changes_p1 | GIẾT | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_bo_finding_issue_comment | r834_issue_comment_p1 | GIẾT | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_bo_nhat_quan_id | r834_cung_id_hai_noi_dung | GIẾT | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_bo_nhat_quan_id | r834_run_cung_id_khac_path | GIẾT | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_bo_p3_offline | r834_p3_offline_thieu_qd | GIẾT | AssertionError: r834 accept: đòi rc=2, được rc=0; stderr='' |
| r834_bo_p3_connector | r834_p3_connector_thieu_qd | GIẾT | AssertionError: r834 accept: đòi rc=2, được rc=0; stderr='' |
| r834_khoa_id_so | r834_p3_connector_khong_slug | GIẾT | AssertionError: r834 accept: đòi rc=11, được rc=0; stderr='' |
| r834_bo_bang_chung_duong | r834_bang_chung_duong_rong | GIẾT | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_ghi_truoc_khi_doc | r834_dau_vao_hong_state_nguyen | GIẾT | AssertionError: I4: state đổi sau khi accept từ chối |
| r834_bo_kiem_gate | r834_check_noi_do | GIẾT | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_bo_check_moi_nhat | r834_check_noi_do_bi_che | GIẾT | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_check_run_khong_nhat_quan | r834_check_cung_id_khac_app | GIẾT | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_bo_khop_attempt_job | r834_attempt_moi_job_cu | GIẾT | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_run_cu_nhat | r834_run_moi_nhat_do | GIẾT | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr="CẢNH BÁO: 'gate (ubuntu-latest)' có 1 run ở suite khác (300) — bỏ qua\nCẢNH BÁO: 'gate-cong-cu-gop (ubuntu-latest)' có 1 run ở suite khác (301) — bỏ qua\nCẢNH BÁO: 'gate-ops (ubuntu-latest)' có 1 run ở suite khác (302) — bỏ qua\nCẢNH BÁO: 'gate-packet-loop (ubuntu-latest)' có 1 run ở suite … (đầy đủ trong DECLARED.jsonl) |
| r834_bo_kho_url_job | r834_job_url_kho_khac | GIẾT | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_noi_check_theo_ten | r834_job_tro_check_khong_co | GIẾT | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_noi_check_theo_ten | r834_job_url_qua_dai | GIẾT | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_jobs_total_toan_cuc | r834_hai_tep_jobs | GIẾT | AssertionError: r834 accept: đòi rc=0, được rc=12; stderr='KHÔNG ĐO ĐƯỢC: workflow_jobs: cần trang {`jobs`, `total_count`} cùng một lần lấy, id int, tập id phân biệt = total_count' |
| r834_badge_chi_P | r834_badge_ngoai_mien_review | GIẾT | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_changes_khong_hang_lot | r834_review_changes_khong_hang | GIẾT | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_commit_thieu_la_cu | r834_review_comment_thieu_commit | GIẾT | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_reviewed_commit_tim_dau | r834_reviewed_commit_sai_dang | GIẾT | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_reviewed_commit_tim_dau | r834_reviewed_commit_mau_thuan | GIẾT | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_head_cu_van_chan | r834_issue_comment_head_cu_khong_chan | GIẾT | AssertionError: r834 accept: đòi rc=0, được rc=12; stderr='connector issue comment 21 có finding mà không neo head' |
| r834_bo_envelope | r834_envelope_head_khac | GIẾT | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_bo_total_count | r834_trang_thieu | GIẾT | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_bo_phu_dung_refs | r834_refs_thua | GIẾT | AssertionError: r834 accept: đòi rc=11, được rc=0; stderr='' |
| r834_bo_luoc_do_state | r834_state_required_checks_rong | GIẾT | AssertionError: r834 accept: đòi rc=8, được rc=0; stderr='' |
| r834_bo_luoc_do_state | r834_state_p3_sai_kieu | GIẾT | AssertionError: r834 accept: đòi rc=8, được rc=0; stderr='' |
| r834_bo_dau_hang_tron | r834_reviewed_commit_span_thua | GIẾT | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_bo_tien_to_mo_ho | r834_tien_to_mo_ho | GIẾT | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_bo_goi_xet_dung | r834_xet_dung_duoc_goi | GIẾT | AssertionError: r834 accept: đòi rc=3, được rc=0; stderr='' |
| r834_xet_dung_truoc_dau_vao | r834_xet_dung_sau_dau_vao | GIẾT | AssertionError: r834 accept: đòi rc=12, được rc=3; stderr='COC_XET_DUNG' |
| r834_bo_kho_run | r834_run_kho_khac | GIẾT | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_bo_head_run | r834_run_head_khac | GIẾT | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_bo_head_job | r834_job_head_khac | GIẾT | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_qd_theo_tap | r834_qd_trung | GIẾT | AssertionError: r834 accept: đòi rc=2, được rc=0; stderr='' |
| r834_bo_kieu_job | r834_job_attempt_bool | GIẾT | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_bo_kieu_job | r834_job_run_id_float | GIẾT | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_xet_dung_truoc_h | r834_xet_dung_sau_h | GIẾT | AssertionError: r834 accept: đòi rc=11, được rc=3; stderr='COC_XET_DUNG' |
| r834_bo_job_xanh | r834_job_chua_xanh | GIẾT | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_bo_p1_review_comment | r834_review_comment_p1 | GIẾT | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_bo_ma_hoa_truoc | r834_qd_khong_ma_hoa | GIẾT | AssertionError: r834 accept: đòi rc=2, được rc=3; stderr='COC_XET_DUNG' |

## Kết quả lệnh và bằng chứng dương

Các lệnh dưới chạy từ `rv4/`; code được test là `out/copy` hoặc mutant riêng, không chạy test trên src. JSONL giữ rc của CLI con. rc=0 của script thu thập chỉ nghĩa thu thập hoàn tất; mutant sống vẫn là nghiệm thu failed.

| lệnh | rc | kết quả/hiện vật |
|---|---:|---|
| `python -B out/run_review.py declared` | 0 | 54/54 nền r834; 49 mutant/55 quan hệ GIẾT đúng; `DECLARED.jsonl`, `DECLARED.log`, `DECLARED.stderr` |
| `python -B out/run_review.py audit` | 0 | 3 mutant × 54 ca = 162 PASS trên mutant ⇒ **3 SỐNG, failed coverage**; `AUDIT.jsonl` |
| `python -B out/run_review.py r812` | 0 | 148/148 ca được chọn đạt; 1 not_run theo giới hạn nội dung đường dẫn; `R812.jsonl` |
| `python -B out/run_review.py confirm` | 0 | 2 ca encoding đạt; parser hỏng 3 TIN_DUNG_GIA đúng; parser sửa group control đạt + 2 kill; 3 mutant cũ chết; lease thật candidate 12/mutant 0; `CONFIRM.jsonl` |
| `python -B out/probe_review.py` | 0 | 93 phép đo khớp kỳ vọng rc/state, 0 traceback; gồm H/P3/Unicode/CI/parser/ID; `PROBES.jsonl` |
| `python -B out/extra_review.py` | 0 | 9 phép đo/kiểm tra đạt: review-only A/B, P3 ở reviews/issue_comments, ambiguity, accepted fields/hashes; `EXTRA.jsonl` |
| `python -B out/copy/.claude/dev/packet_loop.py doctrine-scan --root out/copy` | 0 | 10 tệp, 0 chỗ chép doctrine; `doctrine-scan.log` |
| `python -B out/copy/.claude/dev/packet_loop.py adr-song --root out/copy` | 0 | 55 ADR/55 dòng, khớp 1–1; ngoại lệ 0016 khai sẵn; `adr-song.log` |
| `git -C src diff --check ab344da dcb77e7` | 0 | không lỗi whitespace; `CHECKS.json` |
| `git -C src diff --numstat ab344da dcb77e7` | 0 | 3 tệp, 432 thêm/5 xoá; `CHECKS.json` |
| `python -B out/finalize_review.py` | 0 | kiểm tổng log + snapshot nguồn đầu/cuối + status/diff/index; 6.006 tệp/link, 0 delta; `SOURCE_INTEGRITY.json` |

Scripts review ghi log dạng JSONL tăng dần; mỗi bản mutant có mã riêng trong `mutants/`. Fixture chứa Git refs/receipts thật nhưng đều là kho giả cục bộ. Khi chạy lại, dùng thư mục fixture mới vì script giữ nguyên hiện vật đo để kiểm toán, không tự xoá kết quả cũ.

Full suite `python .claude/dev/packet_loop_test.py`: **not_run**, theo ưu tiên chạy chọn lọc trong prompt (~45 phút full suite). Không khai N/N toàn repository, CI online hoặc Windows execution. Bare Ruff lint và Ruff pin/probe contract: **not_run**; không gắn nhãn “Ruff passed”. SyntaxWarning tại test:3714 có sẵn và không được tính là kill hay finding.

Ca `r812_r4_own_parent` được loại trước khi chạy để không dựng nội dung đường dẫn đi lên cây. Hướng thử cần đường dẫn thoát cây chỉ mô tả: kiểm receipt/readback qua đường dẫn đi lên hoặc symlink đưa ra ngoài cây, yêu cầu từ chối có kiểm soát và state nguyên byte; không soạn/chạy payload cho hướng đó. Không suy an toàn đường dẫn từ phần không chạy.

Ngoài phạm vi, không phân hạng: mo-lai, cho_chu_kho, checkpoint #813, vòng P3 #814, generation #815, ghi đẩy/kích hoạt #816, nợ #929 đã nêu. Verdict chỉ neo commit dòng 2; không cấp quyền push/merge/land.
