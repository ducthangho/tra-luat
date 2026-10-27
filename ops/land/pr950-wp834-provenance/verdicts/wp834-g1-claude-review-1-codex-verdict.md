Verdict: request_changes
Reviewed commit: 17a3714fc8d150bd49a8dd26af29364c1a0bbe4c
Spec sha256: c57ef4d86592218729b811efede7909803d75b6d18ca0d0c3e5059848b44a9d2; Chung sha256: 4e3d1e1b3f6a0b60b96ad7b70f0ece97eca4bb3d6d10defeab1cd24ac6d1cbf0

Nhật ký mở đầu (đã hoàn tất; kết luận và bằng chứng đầy đủ ở dưới) — chưa cấp approve. Reviewer độc lập: Codex / openai, giao diện công cụ cục bộ, transport machine. Không truy cập mạng; chỉ ghi dưới out/. Không cấp quyền push/merge/land.

Đã xác minh: head và origin/master đúng OID yêu cầu; clone không shallow, .git là thư mục; base là tổ tiên head; worktree sạch. Hai băm đặc tả khớp. Diff chỉ có .claude/dev/packet_loop.py, .claude/dev/packet_loop_test.py và docs/PROTOCOL_DA_PHIEN.md (§4): 258 dòng thêm, 2 dòng xoá, đúng giới hạn 450.

Đo bước 1: `R834.log` ghi 19/19 ca xanh, 18 mutant khai báo bị giết (19 quan hệ mutant→ca); đọc tên ca, AssertionError và lý do. Không thấy traceback/CLI sập. `doctrine-scan`: rc=0, 10 tệp/0 chỗ chép doctrine. `adr-song`: rc=0, 55 ADR/55 dòng.

Nhật ký bước 2 — phản chứng đã xác nhận trong `REPRO.jsonl`: check-run do job trỏ tới đỏ/sai head/queued nhưng có bản ID lớn hơn xanh từ app khác vẫn rc=0, state=accepted; cùng check ID mang app hoặc URL kho mâu thuẫn cũng accepted; hai tệp jobs hợp lệ của hai run bị rc=12 do so total_count toàn cục; badge ngoài miền không bắt đầu bằng P bị bỏ qua tại reviews/issue_comments. Các lớp và bảng nghiệm thu sẽ được ghi đầy đủ sau khi xong phép đo.

**Kết luận review độc lập**

`request_changes`: **7 lớp — 0 P0, 4 P1, 3 P2; không có P3 riêng**. Ngưỡng của prompt là hết P0/P1/P2 mới approve. Không dùng kết quả suite xanh để thay phép đo các bất biến. Các mục dưới đây là kết luận trên đúng commit ở dòng 2, không phải yêu cầu triển khai #813–#816.

Reviewer: Codex, họ `openai`, công cụ thực thi cục bộ qua transport machine; độc lập với executor Claude. Assurance mục tiêu `cross_approved`, Review Class `sensitive`; verdict âm này không cấp assurance approve hay quyền push/merge/land. Không xác thực danh tính model bằng tài khoản GitHub hay tự khai đã có receipt runtime. Không gọi mạng/GitHub; các lệnh Git fetch/push trong fixture chỉ trao đổi giữa các kho cục bộ dưới `out/`.

**Định danh và phạm vi**

`PREFLIGHT.jsonl` ghi từng command/rc. HEAD là `17a3714fc8d150bd49a8dd26af29364c1a0bbe4c`, tree `1af6c1e48478a9de817259a934a9f420d579ed18`; `origin/master` là `ab344da5f07cce673d97056b70b002911c4d5082`. `merge-base --is-ancestor` rc=0; `symbolic-ref -q HEAD` rc=1 đúng trạng thái detached; `--is-shallow-repository` trả `false`; `.git` là thư mục. SHA-256 của hai đặc tả khớp dòng 3. Worktree nguồn sạch.

Đã đọc diff đầy đủ (`CANDIDATE.diff`), lease chép trong `tham-chieu/`, đặc tả con/phần chung và verdict thiết kế #812. Lease khai thêm handoff chỉ trên nhánh lease, nhưng diff ứng viên đúng ba tệp của đặc tả, sửa protocol chỉ §4:

| tệp | thêm | xoá |
|---|---:|---:|
| `.claude/dev/packet_loop.py` | 147 | 1 |
| `.claude/dev/packet_loop_test.py` | 107 | 0 |
| `docs/PROTOCOL_DA_PHIEN.md` | 4 | 1 |
| tổng | **258** | **2** |

258 ≤ 450, `git diff --check` rc=0. Không finding về write set, kích thước hay M5.

**Bảng lớp — đếm theo nguyên nhân**

`pl` = `.claude/dev/packet_loop.py`; `test` = `.claude/dev/packet_loop_test.py`. Dòng là dòng của exact head, không phải dòng bản đột biến. Mỗi tên probe bên dưới tìm được trong JSONL cùng thư mục; script và fixture nằm dưới `out/`.

| slug | hạng | biểu hiện file:dòng | phép đo/tái hiện đã chạy | hướng vá |
|---|---|---|---|---|
| `ci-attempt-provenance-missing` | P1 | pl:2833, pl:2839; bộ chọn lại tại pl:2369 | `REPRO.jsonl`: `linked_check_failure_control` rc=12. Giữ job trỏ check 300, check 300 đỏ; thêm check 999 xanh cùng tên/suite nhưng app/kho khác: `linked_check_failure_masked_other_app` rc=0, `accepted`. Sai head hoặc queued ở check 300 cũng được nhận. | Dùng cùng tập check-run đã nối chính xác với job của run/attempt được chọn cho phép kiểm xanh. Kiểm status/conclusion/head trên chính check được job trỏ tới; không cho lần gọi `kiem-gate` chọn lại bản ngoài tập đã xác minh app/kho/attempt. |
| `conflicting-evidence-overwrite` | P1 | pl:2817; bộ đọc cũ pl:2313 | `duplicate_check_conflicting_app`, `duplicate_check_conflicting_repo`: cùng ID 300, hai bản khác app hoặc URL kho; rc=0, `accepted`. | Kiểm nhất quán mọi trường mang provenance/nội dung của cùng check ID trước lọc và lập dict; dùng một bản chuẩn hoặc từ chối mâu thuẫn. Giữ hành vi legacy khi mở rộng cửa mới. |
| `connector-verdict-incomplete` | P1 | pl:2799, pl:2802 | Badge `PX` bị bác đúng; thay bằng `Q1` hoặc `P 1` ở `reviews`/`issue_comments` thì rc=0, `accepted`. Các probe `reviews_badge_Q1`, `issue_comments_badge_P_1` có neo head hiện hành. | Nhận diện trường badge độc lập với miền giá trị, sau đó kiểm miền đóng P0–P3 ở cả ba endpoint. Không biến badge sai định dạng/hạng thành “không finding”. Tách kết luận sạch khỏi nội dung finding không phân hạng. |
| `connector-head-binding-incomplete` | P1 | pl:2789, pl:2791, pl:2800, pl:2802 | Bỏ `commit_id` của review/review comment P1: `*_missing_commit_p1` đều rc=0. Chỉ còn issue comment có `Reviewed commit: <tiền tố đúng>-invalid` cũng rc=0; hai dòng Reviewed commit mâu thuẫn cũng rc=0. Chiều ngược: issue comment P1 có SHA cũ hợp lệ bị rc=12 dù có kết luận sạch head mới. | Xác thực neo theo endpoint trước khi lọc: phân biệt “neo head khác hợp lệ” với “thiếu/sai/mơ hồ”. Parse trọn token/dòng và tất cả khai báo; chỉ hỗ trợ tiền tố khi chứng minh được nó neo duy nhất head cần xét. Finding đã xác định thuộc head cũ không được chặn head mới. |
| `workflow-jobs-pagination-cross-run` | P2 | pl:2816; CLI pl:3109 | `two_workflow_job_files`: một run CI có 5 jobs, một run khác có 1 job; hai tệp từ hai endpoint khai total_count tương ứng 5 và 1. Tất cả xanh nhưng rc=12, state giữ nguyên. | Kiểm đủ trang theo từng endpoint run/attempt (và tính nhất quán nguồn từng tệp), rồi mới hợp nhất jobs. Không ép tổng toàn bộ jobs bằng total_count của từng run. |
| `accept-state-schema-incomplete` | P2 | pl:2818, pl:2862, pl:2872; lược đồ kế thừa pl:676, pl:2542 | `EXTRA.jsonl`: state có `required_checks=[]` + ba readback CI rỗng ⇒ rc=0, `accepted`, không có dòng gate XANH nào. `bien_nhan_approve.p3=""` cũng accepted; `{}`/`p3=null` làm CLI rc=1 với KeyError/TypeError. | Kiểm lược đồ đầu vào state mà accept sử dụng: tập required checks không rỗng, chứa hằng bắt buộc; receipt summary có danh sách slug P3 đúng kiểu/miền. Dữ liệu hỏng phải bị từ chối có kiểm soát trước ghi state; không coi falsy sai kiểu là tập finding sạch. |
| `required-mutation-coverage-missing` | P2 | test:8561, test:8615, test:8636; pl:2770, pl:2820, pl:2827, pl:2839, pl:2853, pl:2877 | `AUDIT_MUTANTS.jsonl`: nhiều mutant gỡ riêng chốt vẫn xanh 19/19: bỏ gate, chọn run cũ nhất, bỏ match attempt job, bỏ envelope connector, bỏ total_count, bỏ phủ refs. Các mutant khai báo vẫn bị giết; điều đó không bảo vệ các chốt này. | Bổ sung ca baseline dương rồi đổi đúng một yếu tố cho từng chốt và mutant riêng; đọc tên ca + lớp ngoại lệ + lý do. Thêm check-run thực sự vắng, check-run được nối đỏ/sai head, hai run, attempt mới đã hoàn tất nhưng jobs còn cũ, trang thiếu, mapping H sai, CI rỗng và lỗi state lồng. |

**Giải thích và giới hạn phản chứng**

`ci-attempt-provenance-missing`: `_kiem_ci` xác minh app/kho/suite của check được job trỏ tới nhưng không kiểm status/conclusion/head của chính check đó. Sau đó `cmd_kiem_gate` đọc lại toàn bộ readback và chọn ID lớn nhất theo tên/suite, không giữ ràng buộc app/kho/attempt đã xác minh. Phép đo kiểm soát chứng minh check 300 đỏ thực sự bị từ chối nếu đứng một mình; chỉ thêm check 999 làm cửa xanh. `CI_MATRIX.jsonl` còn đo bản che lấp cùng app/suite: kết quả vẫn accepted, trong khi check được job trỏ tới vẫn đỏ. Đây là kiểm nhất quán R, không giả định executor ác ý, không đòi máy tự tải GitHub.

`conflicting-evidence-overwrite`: chốt mới `_trang_du` xử lý tốt comment/run/job trùng ID mâu thuẫn, nhưng check-runs dùng `_doc_check_runs` cũ: danh tính nó so chỉ có tên, suite và head. Dict mới ở 2817 giữ bản cuối; gate không xét app/URL của các bản cùng ID. Vì thế lớp được giao từ verdict #812 mới đóng một phần. Không tính mỗi endpoint thành một finding riêng.

`connector-verdict-incomplete`: regex chỉ tìm badge bắt đầu bằng P và không có khoảng trắng trong phần hạng. Với `![Q1 Badge]` hoặc `![P 1 Badge]`, tập hạng thành rỗng. Nhánh reviews/issue_comments chỉ vào kiểm miền khi tập ấy không rỗng nên bỏ qua. Cùng nội dung ở review_comments bị từ chối đúng vì endpoint đó bắt buộc có hạng. Kết luận review sạch không có badge được phép; không coi mọi body không badge là finding. Tuy nhiên review CHANGES_REQUESTED có nội dung finding không phân hạng hiện cũng được nhận; cần hợp đồng rõ để phân biệt trường hợp này, không nhận mặc nhiên chỉ vì regex không tìm thấy.

`connector-head-binding-incomplete`: không kết luận rằng mọi SHA viết tắt đều sai — fixture và output connector có dùng tiền tố. Phản chứng cụ thể là regex `search` + `\b` chỉ ăn phần đầu token sai, hoặc chỉ ăn khai báo đầu trong hai khai báo mâu thuẫn. Đồng thời thiếu `commit_id` bị đối xử giống SHA cũ hợp lệ, nên P1 biến mất. Đã đo SHA cũ hợp lệ ở review/review_comment được bỏ qua; đó là hành vi hợp lý với kết luận sạch hiện hành. Issue comment cũ lại bị từ chối ở 2800 trước khi lọc head, khiến cùng một PR từng có finding không thể tiến tiếp dù head mới sạch. Hướng vá là một bộ phân tích neo có kết quả rõ “hiện hành / cũ hợp lệ / không đo được”, không thêm blacklist từng chuỗi.

`workflow-jobs-pagination-cross-run`: `--workflow-jobs` được khai `action=append`, help nói “lặp mỗi run”, nhưng flatten mọi tệp rồi kiểm một total_count duy nhất. Tệp 5 jobs cộng tệp 1 job cho tập 6 ID; tập total_count `{5,1}` không thể bằng `{6}`. Không phải thiếu trang hay CI đỏ. Thậm chí run thứ hai không bắt buộc cũng gây lỗi; lease có required check của workflow thứ hai sẽ gặp cùng vấn đề. Không đề nghị sửa total_count của readback thành tổng giả để đi qua.

`accept-state-schema-incomplete`: phép thử cố ý làm hỏng state cục bộ để đo hợp đồng lỗi đầu vào, không coi state là hàng rào chống executor chủ ý gian lận. Lược đồ hiện có chấp nhận các giá trị ấy, rồi cửa mới mở quyền hoặc traceback. Với `required_checks=[]`, vòng lặp xác minh CI không chạy và không có hằng bắt buộc nào được kiểm tại cửa accept. Với `{}` hoặc null, state giữ byte nhưng rc=1/traceback không phải từ chối lược đồ có kiểm soát. Finding không gán lỗi thay state cho hai trường hợp traceback; lỗi thay state thực sự xảy ra ở trường hợp rỗng/sai kiểu được nhận.

**Đối chiếu từng mục bắt buộc `nghiem_thu`**

Tên ca và mutant dưới đây đều có tiền tố `r834_` (lược tiền tố trong các ô cho gọn). 19 ca tổng cộng gồm 18 mục bắt buộc và một ca dương P3. Toàn bộ baseline 19/19 xanh. Có 18 mutant khai báo, 19 quan hệ mutant→ca vì một mutant đo hai ca ID mâu thuẫn. Tất cả chết đúng assertion, không có `TIN_DUNG_GIA` hay `SONG` trong nhóm khai báo.

| mục bắt buộc | ca `r834_*` | mutant `r834_*` | kết quả và lý do chết đã đọc |
|---|---|---|---|
| sạch `lop=[]`, connector sạch → accepted | `sach_accepted` | `bo_ket_luan_issue_comment` | baseline rc=0/accepted; mutant AssertionError: đòi 0, được 12, “connector chưa xong”. |
| đầu remote khác pending | `dau_nhanh_lech` | `bo_dau_nhanh_remote` | baseline rc=5, “≠ pending_sha”; mutant đòi 5, được 0. |
| check bắt buộc vắng | `check_vang` | `job_vang_bo_qua` | baseline rc=12, “VẮNG”; mutant đòi 12, được 0. **Giới hạn:** ca xoá Actions job, vẫn giữ check-run; chưa phải ca xoá check-run. Probe riêng `required_check_run_missing` đã bác rc=12. |
| app khác | `check_app_khac` | `bo_app` | baseline rc=12, “không từ app”; mutant đòi 12, được 0. |
| workflow khác cùng app | `check_workflow_khac` | `bo_path_workflow` | baseline rc=12, “VẮNG”; mutant đòi 12, được 0. |
| attempt mới đang chạy, check cũ xanh | `rerun_dang_chay` | `bo_attempt_moi_nhat` | baseline rc=12, “chưa xanh”; mutant đòi 12, được 0. Mutant này gỡ **hai** chốt: run status và match attempt của job. Gỡ riêng match attempt vẫn 19/19. |
| check-run kho khác | `check_kho_khac` | `bo_kho_check_run` | baseline rc=12, “kho khác”; mutant đòi 12, được 0. |
| phần tử PR khác cùng head | `pr_khac_cung_head` | `bo_neo_pr_phan_tu` | baseline rc=12, “không thuộc”; mutant đòi 12, được 0. Không bảo vệ envelope: mutant bỏ envelope sống. |
| review PENDING chưa xong | `review_pending` | `pending_la_xong` | baseline rc=12, “chưa xong”; mutant đòi 12, được 0. |
| CHANGES_REQUESTED có P1 | `review_changes_p1` | `bo_finding_review` | baseline rc=12, “còn ['P1']”; mutant đòi 12, được 0. |
| issue comment P1 | `issue_comment_p1` | `bo_finding_issue_comment` | baseline rc=12, “còn ['P1']”; mutant đòi 12, được 0. |
| cùng comment ID: P1 rồi P3 | `cung_id_hai_noi_dung` | `bo_nhat_quan_id` | baseline rc=12, “hai nội dung”; mutant đòi 12, được 0. |
| cùng workflow run ID khác path | `run_cung_id_khac_path` | `bo_nhat_quan_id` | baseline rc=12, “hai nội dung”; mutant đòi 12, được 0. |
| offline P3 thiếu quyết định | `p3_offline_thieu_qd` | `bo_p3_offline` | baseline rc=2, “P3 còn mở”; mutant đòi 2, được 0. |
| connector P3 thiếu quyết định | `p3_connector_thieu_qd` | `bo_p3_connector` | baseline rc=2, “P3 còn mở”; mutant đòi 2, được 0. |
| connector P3 không slug H | `p3_connector_khong_slug` | `khoa_id_so` | baseline rc=11, đòi `--bien-nhan-connector`; mutant đòi 11, được 0. Ca này bỏ receipt, chưa kiểm receipt có mapping sai. |
| bằng chứng dương rỗng | `bang_chung_duong_rong` | `bo_bang_chung_duong` | baseline rc=12, “chưa xong”; mutant đòi 12, được 0. Chỉ đo connector rỗng; CI rỗng xem finding. |
| đầu vào hỏng giữ state | `dau_vao_hong_state_nguyen` | `ghi_truoc_khi_doc` | baseline JSON connector hỏng rc=12, “KHÔNG ĐO ĐƯỢC”, byte bất biến; mutant cùng rc/lý do nhưng AssertionError “I4: state đổi sau khi accept từ chối”. |
| bổ sung: P3 đủ quyết định | `p3_du_quyet_dinh` | `bo_ref_connector_h` | baseline rc=0/accepted; mutant đòi 0, được 11, “bảng lớp H phải phủ ĐÚNG”. |

Mutant âm được ghi giết chỉ khi ca tương ứng đổi từ rc từ chối sang rc=0 hoặc vi phạm byte đúng mục tiêu. Hai mutant làm mất bằng chứng dương bị giết bởi từ chối có kiểm soát đúng thông điệp, không do lỗi import/setup. `SyntaxWarning` có sẵn về escape `\d` không phải lỗi chạy và không được tính làm giết mutant.

**Các phần đã kiểm đúng và đối chiếu I1–I11 / M1–M5**

- **I1/I2:** baseline dùng lease validator H và kho Git cục bộ thật, remote head đo bằng `ls-remote`; không thay hàm đo authority bằng stub. Chốt remote lệch được ca/mutant mới bảo vệ. Các chốt cấp lease kế thừa được chạy lại trong 149 ca `r812_*`.
- **I3:** lớp offline rỗng được nhận đúng. P1/P3/PX và hai badge khác hạng được đo ở cả ba endpoint. P1 bị bác rc=12; P3 đòi H; PX/hai hạng bị bác rc=12. Review comment không badge bị bác. Còn sai ở hạng không được regex nhận diện và tập CI rỗng như bảng lớp.
- **I4:** 37 probe từ chối trong `REPRO.jsonl` và 35 trong `EXTRA.jsonl` đều giữ state nguyên byte, kể cả từ chối muộn ở H/refs/quyết định P3. Hai traceback được tách riêng, không khai là từ chối chuẩn. Trường hợp đầu vào state hỏng được accepted vi phạm yêu cầu từ chối/không ghi; đã phân lớp riêng.
- **I5:** `cmd_accept` gọi đúng `_xet_dung` sau remote/CI/connector/H/quyết định P3. Helper hiện không có nhánh dừng riêng cho tên cửa `accept`; không tự đặt thêm stop condition ngoài đặc tả. Có lần đọc lại connector để lấy digest ở 2879 sau helper; chưa có phép đo race và không tính một finding I4 mới từ suy đoán này. Mutant bỏ lời gọi helper kiểm mức bảo vệ của suite, không chứng minh một điều kiện dừng mới phải được thêm.
- **I6:** không mở quyền phái sinh mới thuộc #813–#815; ngoài phạm vi.
- **I7/M2/M3:** chọn run mới hơn đang chạy bị bác; run attempt 2 đã completed nhưng jobs vẫn attempt 1 bị bác; URL check_run của job sai kho, run_id/head job lệch, suite check lệch đều bị bác rc=12. Trang có total_count sai kiểu/thiếu/thừa/âm bị bác; bản lặp giống hệt được khử trùng; bản lặp run/job mâu thuẫn bị bác. Cùng ID 31 ở reviews và review_comments được nhận với mapping H đúng: không so chéo không gian ID. Còn các lỗi CI/connector/phân trang đã nêu.
- **I8/I10/M4:** connector receipt dùng lại validator canon đầy đủ; probe đổi riêng packet, generation, reviewed_sha, spec_hash, role, verdict đều rc=11, byte bất biến. Đó là vai ứng viên với `(packet, generation hiện hành, pending_sha, spec_hash)`; packet này chưa có hiện vật nguồn generation cũ để áp quyền mở lại.
- **I11:** `connector_refs` trùng/thiếu/thừa/sai endpoint, bool/string ID, scalar/nested/sai kiểu list đều bị bác rc=11; ánh xạ hợp lệ cho P3 được nhận. Quyết định P3 trùng/thiếu/thừa, sai kiểu container/phần tử/trường, thừa trường, lý do trắng đều rc=2. Slug lấy từ H, không dùng ID số tự đặt. Phần connector của lớp thiết kế `findings-not-receipt-bound` **đã đóng trong phạm vi đã đo**, không tái báo chỉ vì ca mapping còn thiếu.
- **I9:** diff không sửa các nhánh legacy; phần thay ở `_du_dieu_kien_approve` thêm `lop` vào summary của đường ADR-0054. Đã chạy 149/149 ca `r812_*`, gồm init/lease legacy và các ca không kích hoạt. Đây là bằng chứng hồi quy chọn lọc; **chưa chạy toàn bộ mọi ca cũ** nên không khai toàn suite N/N.
- **M1:** luồng dương sạch và P3 có H/quyết định đều đạt accepted, ghi accepted_sha/mốc theo endpoint. M1 tổng thể chưa đạt vì những đường nhận sai đầu vào và CI/connector ở bảng lớp.
- **M5:** protocol §4 nêu cửa accept và điều kiện chỉ packet áp ADR-0054; đúng phạm vi.

**Đối chiếu đầu vào thiết kế #812 và thay đổi #929**

`connector-verdict-incomplete`: đã sửa PENDING, đọc finding ba endpoint; **chưa đóng hoàn toàn**, còn miền badge và neo head. `ci-attempt-provenance-missing`: đã nối run/attempt/jobs/check URL và kiểm run mới; **chưa đóng hoàn toàn** vì lần gọi gate chọn check khác. `conflicting-evidence-overwrite`: đã sửa comment/workflow/job, **còn check-run**. Phần connector của `findings-not-receipt-bound`: đã có mapping H đúng tuple và phủ đúng refs, phép đo âm/dương đạt; thiếu coverage được tính riêng, không báo lại lỗi sản phẩm đã đóng.

`_che_do_0054` trên head hiện hành quét các blob ADR theo cụm khai `kích hoạt ADR-0054`, không ghim số 0055; nó có kiểm `ls[0] == 0`. wp834 và phần chung không bắt buộc một số tệp kích hoạt cụ thể, nên **không thấy mâu thuẫn đặc tả ràng buộc với thay đổi #929**. Dữ liệu thiết kế g2 cũ không phải luật để quay lại tên tệp cũ. Nợ P3 về ca `ls[0] == 0` của #929 được loại khỏi phân hạng theo prompt. Packet này không kích hoạt ADR-0054 trong kho thật; fixture riêng dựng trạng thái đã kích hoạt để đo cửa mới.

**Đột biến bổ sung của reviewer — đã chạy xong**

Tất cả biến đổi chỉ nằm trong `out/audit_mutants/`. Cặp neo/thay nguyên văn nằm trong `AUDIT_MUTANTS.py` và từng dòng `AUDIT_MUTANTS.jsonl`; mỗi neo được kiểm xuất hiện đúng một lần, compile thành công trước chạy. Mỗi mutant chạy lại **toàn bộ 19 ca r834**, không chỉ một ca lựa chọn. Kết quả là **8/8 mutant sống, mỗi mutant 19/19 xanh**, không phải lỗi runner.

| mutant reviewer | chốt bị gỡ/đổi | kết quả |
|---|---|---|
| `omit_kiem_gate` | bỏ lời gọi gate ở 2839 | SỐNG 19/19 |
| `oldest_run` | max run ID → min run ID | SỐNG 19/19 |
| `omit_job_attempt` | bỏ riêng ràng buộc job.run_attempt, giữ run status | SỐNG 19/19 |
| `omit_connector_envelope` | bỏ so repo/PR/head envelope, giữ kiểm phần tử | SỐNG 19/19 |
| `omit_total_count` | bỏ so total_count với tập ID phân biệt | SỐNG 19/19 |
| `omit_ref_exact_cover` | bỏ kiểm phủ chính xác connector_refs | SỐNG 19/19 |
| `omit_stop_call` | bỏ `_xet_dung(..., "accept")` | SỐNG 19/19 |
| `omit_job_check_url_repo` | lấy ID cuối URL job mà không kiểm kho trong URL | SỐNG 19/19 |

Riêng mutant bỏ `_xet_dung`, helper hiện không có nhánh hành vi cho `accept`, nên đây là thiếu phép kiểm hợp đồng gọi hàm I5; không dùng nó để khẳng định có một stop hành vi bị lọt. Các mutant còn lại làm yếu chốt quan sát được với dữ liệu biên cụ thể. Ví dụ probe `latest_attempt_completed_old_jobs` và `latest_run_running_old_success` cho biết các chốt tồn tại và từ chối đúng trên sản phẩm, trong khi ca gốc không phân biệt khi gỡ chúng. Không suy 8 mutant sống thành 8 lớp lỗi sản phẩm.

**Lệnh, rc và bằng chứng dương**

Môi trường chạy: Linux, Python cục bộ; `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR` trỏ tuyệt đối vào `out/tmp`, cấu hình Git global/system cô lập qua `/dev/null`. Không ghi cache Python vào nguồn. Lệnh git cuối dùng `GIT_OPTIONAL_LOCKS=0`. Bản sao `out/review-copy` có `packet_loop.py` bằng byte với nguồn; các biến đổi sản phẩm chỉ ở thư mục mutant riêng.

| lệnh / phép đo | rc | bằng chứng / hiện vật |
|---|---:|---|
| `python -B out/PREFLIGHT.py` | 0 | `PREFLIGHT.jsonl`: OID/tree/hash đúng, ancestor rc=0, detached rc=1 đúng mong đợi, status sạch, diff check rc=0. |
| `python -u -B tham-chieu/chay_ca_va_dot_bien.py src r834_ r834_` | 0 | `R834.log`: `CA 19/19`; 18 mutant, 19 quan hệ giết đúng assertion; 0 sống, 0 tín dụng giả. Fixture/temp/mutant của lệnh đều dưới out qua TMPDIR; mã nguồn chỉ được đọc/chạy. |
| `python -u -B tham-chieu/chay_ca_va_dot_bien.py out/review-copy r812_` | 0 | `R812.log`: `CA 149/149`; không chạy mutant r812 trong lượt này. |
| `python -B out/review-copy/.claude/dev/packet_loop.py doctrine-scan --root out/review-copy` | 0 | `DOCTRINE.log`: 10 tệp, 0 chỗ chép doctrine. |
| `python -B out/review-copy/.claude/dev/packet_loop.py adr-song --root out/review-copy` | 0 | `ADR.log`: 55 ADR, 55 dòng §20, khớp 1–1; ngoại lệ 0016 được khai sẵn. |
| `python -u -B out/REPRO.py` | 0 | `REPRO.jsonl`: 59 bản ghi, gồm hai baseline accepted bằng H/Đ thật; 37 probe từ chối đều nguyên byte; các probe nhận sai được phân lớp ở trên. |
| `python -u -B out/EXTRA.py` | 0 | `EXTRA.jsonl`: 45 bản ghi, gồm hai baseline; 35 probe từ chối/thoát lỗi giữ byte; 2 traceback input state tách riêng. |
| `python -u -B out/CI_MATRIX.py` | 0 | `CI_MATRIX.jsonl`: 5 bản ghi; baseline accepted, check-run vắng bị bác, check đỏ được bản khác che lấp vẫn accepted. |
| `python -u -B out/AUDIT_MUTANTS.py` | 0 | `AUDIT_MUTANTS.jsonl`: 8 mutant, 8 × 19 ca đều xanh, tức thiếu coverage được chứng minh. |

Các script probe là bộ thu kết quả: rc=0 của **script** không có nghĩa mọi hành vi sản phẩm đúng; rc, stdout, stderr và so byte của từng lần CLI nằm trong JSONL. Tổng 109 bản ghi probe gồm 5 baseline, không gọi đó là “109 test pass”. Hai traceback là hành vi sản phẩm trên input state hỏng, không dùng để giết mutant hay lấy tín dụng nghiệm thu.

**Chưa chạy / ngoài phạm vi**

Chưa chạy toàn suite `python .claude/dev/packet_loop_test.py` (~45 phút theo prompt), toàn bộ mutant legacy, CI GitHub hay Windows; không khai các phần đó đạt. Đã ưu tiên kiểm chọn lọc theo yêu cầu, chạy 168 ca baseline liên quan, mutant khai báo và mutant độc lập. Không viết patch sửa gate/authority; chỉ cung cấp hướng vá và phản chứng. Không soạn payload đường dẫn thoát cây. Các hướng cần kiểm đường dẫn receipt/lease thoát cây chỉ nên giao executor dùng fixture có sẵn và ghi lại phép đo; lượt này không chạy, không phân hạng từ suy đoán ấy.

`mo-lai`, `cho_chu_kho`, checkpoint #813, vòng P3 #814, generation kế #815, ghi đẩy/kích hoạt #816 và nợ P3 #929 đã nêu đều ngoài phạm vi. Kết luận cuối vẫn **request_changes**, chỉ neo commit `17a3714fc8d150bd49a8dd26af29364c1a0bbe4c`.
