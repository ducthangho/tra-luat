Verdict: request_changes
Reviewed commit: 7436fe3b1ee0fc54190c7cd50d3be06c41790ee5
Spec sha256: c57ef4d86592218729b811efede7909803d75b6d18ca0d0c3e5059848b44a9d2; Chung sha256: 4e3d1e1b3f6a0b60b96ad7b70f0ece97eca4bb3d6d10defeab1cd24ac6d1cbf0

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn đối chiếu: `tham-chieu/VERDICT-luot2.md`, SHA-256 `cb53cee193fa89c7b0c593e660fe183514a86b42a164f2bdd4be5e69935621be`, reviewed commit `0b8d48c5e221edcedcf3a2c31b444ed33a1619d8`. Đã đọc toàn bộ diff base→head và diff vá 0b8d48c→7436fe3; không lấy lời khai executor làm bằng chứng đóng lớp.

| slug còn mở lượt 2 | kết luận lượt 3 | phép đo độc lập |
|---|---|---|
| `connector-head-binding-incomplete` (F1, P1) | **đóng — ĐÃ VÁ THẬT**, trong phạm vi parser/nhất quán R đã đo | `PROBES.jsonl`: tiền tố 7/10/40 ký tự dạng trần, backtick, nhãn in đậm hợp lệ đều rc=0; nội dung thừa/SHA thứ hai trong code span hoặc thiếu backtick đóng đều rc=12. `EXTRA.jsonl`: hai SHA cùng tiền tố 10 ký tự trong readback: claim tiền tố → 12, exact head hiện hành → 0, exact head cũ → 12 vì chưa có kết luận head hiện hành. Dạng hai comment thật của #889 (summary + receipt), chỉ thay tuple repo/PR/head cho fixture, rc=0. Không tìm thấy hồi quy từ chối dạng thật đã cấp. Mutant parser hỏng được ghi là lỗi nghiệm thu **mới**, không đánh tráo thành lỗi parser sản phẩm. |
| `required-mutation-coverage-missing` (F2, P2) | **còn mở — VÁ HỜ / đã vá một phần** | Sáu mutant còn sống lượt 2 nay đều bị ca mới giết đúng lý do (bảng bên dưới). Tuy nhiên ba mutant tự dựng khác vẫn **50/50** ca r834 xanh: gọi dừng trước H/P3, bỏ điều kiện job completed/success, bỏ finding P0–P2 tại review_comments. Các probe độc lập phân biệt được cả ba. Không coi mutant sống là lỗi hành vi đang tồn tại trên bản gốc. |
| `ci-job-input-schema-incomplete` (F3, P2) | **đóng — ĐÃ VÁ THẬT** đối với các biểu hiện lượt 2 | `PROBES.jsonl`: job attempt true/1.0/string/null và run_id float/bool/string/null đều rc=12 có thông điệp kiểm kiểu; URL ID 5.000 chữ số rc=12 có kiểm soát, không traceback. Control integer và URL chuẩn accepted. Mutant bỏ kiểm kiểu và mutant join sai URL bị giết đúng assertion; mọi reject giữ nguyên byte. |

**Tổng còn mở: 3 lớp — 0 P0, 0 P1, 3 P2, 0 P3.** Một lớp cũ còn mở; hai lớp mới được đếm riêng: `connector-parser-mutant-false-credit` (bản vá sinh ra) và `stop-validation-order` (mới đo tại cửa accept). Không đạt ngưỡng approve: không còn P0/P1/P2.

## Bảng lớp còn mở

`pl` = `.claude/dev/packet_loop.py`; `test` = `.claude/dev/packet_loop_test.py`. Dòng theo exact head trên. Đếm theo nguyên nhân, không theo số biến thể.

| slug | hạng | biểu hiện file:dòng | phép đo/tái hiện đã chạy | hướng vá |
|---|---|---|---|---|
| `required-mutation-coverage-missing` (F2, cũ) | P2 | test:8749–8750, test:8613; pl:2824, pl:2858, pl:2907 | `AUDIT_MUTANTS.jsonl`: `stop_before_H_and_P3`, `omit_job_completed_success`, `accept_p1_review_comment` đều sống 50/50. `EXTRA.jsonl`: mutant thứ nhất trả sentinel rc=3 trước receipt sai generation; hai mutant sau accepted/rc=0 với job in_progress và review comment P1 tương ứng. Bản gốc từ chối đúng. | Thêm ca consumer r834 cho lỗi muộn H/P3 với cọc I5, job chưa xanh nhưng check xanh, và P1 review comment có commit_id đúng. Mỗi ca có mutant đúng chốt, đối chứng dương, kiểm rc/lý do/byte. |
| `connector-parser-mutant-false-credit` (F4, mới do bản vá) | P2 | test:8727–8728, test:8596; pl:2790 khi bị đột biến | `DECLARED.jsonl`: `r834_reviewed_commit_tim_dau` làm cả `r834_reviewed_commit_sai_dang` và `r834_reviewed_commit_mau_thuan` trả rc=1, traceback `IndexError: no such group`; runner vẫn ghi GIET. `CONFIRM.jsonl`: mutant còn làm control sạch rc=1. Chỉ sửa cấu trúc capture group trong bản mutant riêng thì hai ca mục tiêu đỏ đúng AssertionError đòi 12, được 0. | Giữ cấu trúc dữ liệu mà consumer đọc khi gỡ chốt parser; tách mutant kiểm trường trọn và kiểm mọi khai báo. Đường r834 phải phân biệt CLI sập với vi phạm assertion mục tiêu, dùng cơ chế báo tín dụng giả đã có của harness. |
| `stop-validation-order` (F5, mới trong packet này) | P2 | pl:2903–2910; `_save` pl:702–707 | `LATE_INPUT.jsonl`: chuỗi surrogate đơn U+D800 trong từng trường ten_no/owner/huong/ly_do qua kiểm qd; bản gốc rc=8 ở `_save`, state nguyên byte. Với cọc I5, cùng input trả 3 trước khi bị bác. `CONFIRM.jsonl` dùng hook **gọi tiếp hàm gốc**: stderr lần lượt `OBSERVED_STOP_CALL` rồi `state không mã hoá được: UnicodeEncodeError`, rc=8. | Xác thực khả năng tuần tự hoá/mã hoá các đầu vào sẽ ghi, hoặc dựng và encode trạng thái dự kiến, trước `_xet_dung`. Giữ chốt encode trước truncate trong `_save`; không thêm điều kiện dừng riêng cho accept. |

### F2 — phần đã vá và phần chưa được suite bảo vệ

Sáu mutant sống của lượt 2 được dựng lại bằng cùng phép biến đổi trên head mới và chạy ca đích của candidate trong `DECLARED.jsonl`. Một ca giết đúng đã đủ chứng minh mutant không còn sống; không khai đã chạy toàn bộ 50 ca trên mỗi mutant cũ.

| mutant sống lượt 2 | mutant tương ứng trên head này | ca giết / thông điệp thực |
|---|---|---|
| omit_stop_call | r834_bo_goi_xet_dung | r834_xet_dung_duoc_goi: AssertionError đòi rc=3, được 0 |
| omit_run_repository | r834_bo_kho_run | r834_run_kho_khac: AssertionError đòi rc=12, được 0 |
| omit_run_head | r834_bo_head_run | r834_run_head_khac: AssertionError đòi rc=12, được 0 |
| omit_job_head | r834_bo_head_job | r834_job_head_khac: AssertionError đòi rc=12, được 0 |
| omit_connector_p3_unique_decision | r834_qd_theo_tap | r834_qd_trung: AssertionError đòi rc=2, được 0. Chốt chung quyết định offline/connector nay được ca offline bảo vệ. |
| omit_receipt_generation | r812_bo_generation | r834_bnc_lech_generation: AssertionError đòi rc=11, được 0; ca r812_bien_nhan_lech_generation cũng giết. |

Bảy mutant đã chết lượt 2 (omit_kiem_gate, oldest_run, omit_job_attempt, omit_connector_envelope, omit_total_count, omit_ref_exact_cover, omit_job_check_url_repo) cũng được đo lại qua các mutant khai báo tương ứng; vẫn chết đúng mục tiêu. Không báo lại chúng là thiếu coverage.

Ba mutant bổ sung chạy **đủ 50 ca r834 mỗi bản**, không sửa test candidate, nằm tại `audit_mutants/`; script lưu cặp neo/thay đầy đủ và kiểm neo duy nhất, compile trước chạy:

| mutant tự dựng | thay đổi | 50 ca candidate | probe phân biệt bản gốc / mutant |
|---|---|---|---|
| stop_before_H_and_P3 | chuyển nguyên lời gọi `_xet_dung` từ sau validation qd lên ngay trước `_slug_connector` | 50/50 | H sai generation + cọc: 11 / 3. Bản gốc không chạm sentinel; mutant chạm sentinel. |
| omit_job_completed_success | chỉ gỡ hạng tử kiểm `(job.status, job.conclusion)` | 50/50 | job in_progress, check vẫn xanh: 12 / 0 accepted |
| accept_p1_review_comment | bỏ chặn P0–P2 riêng endpoint review_comments, chỉ đưa P3 thật vào danh sách P3 | 50/50 | review comment P1, đúng commit_id và repo/PR: 12 / 0 accepted |

Mutant thứ ba cần hai hunk cùng một thay đổi ngữ nghĩa: nếu chỉ bỏ `die` nhưng vẫn biến P1 thành P3 thì lỗi thiếu receipt lại chặn, không đo được việc bỏ finding P1. Không dùng crash hay fixture hỏng để giết mutant.

Ca I5 hiện tại chỉ làm hỏng JSON connector và đặt sentinel cho ca đó; do vậy nó phân biệt gọi dừng trước connector, nhưng không phân biệt gọi dừng trước H/P3 sau connector. Thêm ít nhất hai ca muộn với `vo=True` và kiểm **không** có marker sentinel. Ca job cần giữ nguyên run/check xanh rồi chỉ đổi status hoặc conclusion của job. Ca review comment cần giữ đủ neo hợp lệ, không dùng thiếu commit_id hay duplicate ID làm chốt phụ. Rủi ro vá: thêm assertion mà fixture đã chết ở chốt khác sẽ tạo coverage giả; dùng probe dương và đọc toàn bộ stderr.

### F4 — tín dụng giả mới, tách khỏi thiếu ca F2

Bản vá mutant thay `re.fullmatch` có **hai** capture group bằng `re.search` có **một** group. Consumer vẫn đọc `t[2]`. Hai ca mục tiêu chết ở cơ chế nội bộ này; chúng chưa chứng minh mutant cho lọt dữ liệu cần cấm. `_r834_ca` gọi `_doi` trước kiểm thông điệp; `_doi` gói rc=1/traceback thành AssertionError thường. `_phan_loai_giet` chỉ nhận tín dụng giả nếu có `CliSapDo` trong chuỗi exception, nên hai dòng được báo sai GIET.

Bằng chứng kiểm toán giữ nguyên phân loại **do runner khai** trong `DECLARED.jsonl`; bảng cuối báo phân loại reviewer. Trong `CONFIRM.jsonl`, mutant này còn phá cả `r834_sach_accepted`: đòi 0, được 1 với cùng IndexError. Bản mutant riêng tại `mutant_repaired/` chỉ giữ thêm group rỗng để token SHA vẫn nằm ở group 2: hai ca mục tiêu khi ấy trả accepted/0, và chính assertion đòi 12 làm chúng đỏ. Đây là dữ liệu đo trên bản sao, không phải patch sửa sản phẩm.

Hướng vá ở test: bảo toàn giao diện kết quả regex trong mutant, thêm đường nhận dạng traceback/unexpected CLI crash vào nhóm r834 theo cơ chế của harness. Ca khoá phải phân biệt: CLI crash ⇒ TIN_DUNG_GIA, bypass semantic ⇒ GIET, control sạch vẫn chạy. Rủi ro vá: sửa chỉ regex mà bỏ phân loại crash sẽ tái diễn ở mutant kế tiếp; ngược lại đừng coi mọi AssertionError là crash, vì assertion đúng mục tiêu là tín dụng hợp lệ.

F4 khác F2: các ca kiểm parser đã tồn tại và phân biệt được một mutant hợp lệ; lỗi mới nằm ở mutant được tạo sai và việc cấp tín dụng cho crash. F2 cần thêm tình huống đầu vào chưa được test, không thể chữa bằng chỉ sửa mutant parser.

### F5 — đầu vào chưa xác thực hết khi vào hàm dừng

Phép đo dùng một file JSON hợp cú pháp, có escape cho surrogate đơn trong **giá trị** quyết định P3; không dùng đường dẫn thoát cây. Kiểm `type(v) is str and v.strip()` nhận nó. `_save` của chính sản phẩm gọi đây là lỗi đầu vào/encoding và từ chối trước truncate, nhưng nó chạy sau `_xet_dung`.

Ma trận `LATE_INPUT.jsonl` có control tiếng Việt hợp lệ → accepted và control sentinel → rc=3. Bốn biến thể ten_no/owner/huong/ly_do đều rc=8, nguyên byte ở bản gốc; cả bốn chạm sentinel trước lỗi encoding. Để tránh suy từ hành vi sentinel dừng sớm, `CONFIRM.jsonl` dùng hook chỉ in marker rồi gọi **hàm gốc với nguyên đối số**. Kết quả input hỏng: marker trước UnicodeEncodeError, rc=8, state nguyên byte. H sai generation và thiếu quyết định P3 không in marker; control hợp lệ in marker và accepted.

Đây là vi phạm thứ tự M1/I5 thực tế, không chỉ thiếu test. **Không kết luận sản phẩm đang làm hỏng state khi reject**: I4 vẫn giữ trong các phép đo; `_xet_dung` hiện không có nhánh dừng riêng cho `cua="accept"`. Cũng không yêu cầu sáng tác nhánh dừng mới. Hợp đồng cửa mới yêu cầu mọi validation input hoàn tất trước lời gọi shared helper, và lỗi encoding có sẵn xảy ra sau nó.

Vá ở ranh giới qd/candidate state trước pl:2907; có thể kiểm encode các chuỗi mới hoặc tiền kiểm serialization của trạng thái dự kiến. Ca khoá dùng hook gọi tiếp hàm gốc: chuỗi hợp lệ tới hook, chuỗi không mã hoá được bị bác trước hook và giữ byte; mutant gỡ preflight phải làm marker xuất hiện. Rủi ro vá: chuẩn hoá/lossy replacement có thể đổi quyết định của người dùng; giữ nguyên Unicode hợp lệ, không thay dữ liệu hỏng bằng ký tự thay thế và không bỏ bảo vệ encode-before-truncate hiện có.

## Định danh, phạm vi và tính toàn vẹn

Đã đọc toàn văn prompt snapshot được chỉ định. Thư mục làm việc thực là `rv3/`, chứa `src/`, `out/`, `tham-chieu/`; đường `runs/.../prompt.snapshot` chỉ là nguồn chỉ dẫn. Review độc lập, offline, không GitHub, không mạng, không push/merge/land bên ngoài. Fetch/push/ls-remote trong fixture chỉ tới kho Git cục bộ dưới `out/`, có `GIT_ALLOW_PROTOCOL=file`. Mọi script, bản sao, mutant, fixture, temp và output của review đều nằm dưới `out/`; dùng `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR=out/tmp`, cô lập Git system/global.

Reviewer: Codex, họ openai, có shell cục bộ qua công cụ phiên API, transport machine; không kế thừa context executor Claude. Không có receipt máy độc lập để chứng minh exact model/effort/session identity hay xác nhận bề mặt là `codex_cli` như lease yêu cầu; phần này **không đo được**, không tự nhận đã có `cross_approved`. `cross_approved` là mục tiêu của packet. Verdict âm này chỉ đánh giá nội dung trên exact SHA, không cấp assurance hoặc quyền land.

`CHECKS.json` và `SOURCE_INTEGRITY.json`:

- HEAD `7436fe3b1ee0fc54190c7cd50d3be06c41790ee5`; tree `7112a1e0e20d1bb8d600f62e747bc87d9cdebf5c`.
- origin/master đúng base `ab344da5f07cce673d97056b70b002911c4d5082`; base ancestor rc=0; detached (`symbolic-ref -q HEAD` rc=1 đúng mong đợi); không shallow; `.git` là thư mục.
- Hai SHA-256 đặc tả đúng dòng 3; hai băm verdict trước cũng khớp prompt. Lease r1/g1 ghi đúng executor, write set và giới hạn packet; bản chép lease không được xác minh lại từ mạng.
- `git diff --check ab344da 7436fe3` rc=0; `core.abbrev=7` ở bản nguồn được giữ trong bản sao.
- Snapshot đầu/cuối gồm **6.001 tệp/link**, kể cả `.git`: **0 delta** nội dung/đích link. Status tracked/untracked/ignored rỗng; worktree/index diff rc=0. Giới hạn: snapshot chứng minh hai mốc không đổi, không chứng minh toàn bộ lịch sử chưa từng ghi rồi hoàn nguyên. Sandbox thực là workspace-write; các thao tác review được giới hạn bằng đường ghi vào out/.

| tệp trong diff base→head | thêm | xoá |
|---|---:|---:|
| .claude/dev/packet_loop.py | 177 | 1 |
| .claude/dev/packet_loop_test.py | 225 | 3 |
| docs/PROTOCOL_DA_PHIEN.md (§4) | 4 | 1 |
| Tổng | **406** | **5** |

Đúng ba đường dẫn, 406 ≤ 450. Không finding về M5/write set/kích thước. `CANDIDATE.diff` và `PATCH.diff` giữ toàn bộ diff đã đọc. Handoff được lease cho phép chỉ trên nhánh lease, không nằm trong diff ứng viên.

## Đối chiếu bất biến và lớp thiết kế #812 được giao cho packet

| mục | kết quả / phạm vi |
|---|---|
| I1, M1 | Cửa accept đo đầu remote bằng ls-remote; lệch pending bị rc=5. Baseline H/Đ/R thật của fixture tới approved_pending rồi accepted. |
| I2 | Không sửa cửa cấp lease; nền r834 đi qua validator/cửa lease thật. r812 hồi quy đo thêm các chốt authority hiện có. Không suy readback R thành authority độc lập. |
| I3, M3 | P0/P1/P2 và Q1/P 1/PX/hai hạng bị bác ở cả ba endpoint. Thiếu hạng ở review comment và CHANGES_REQUESTED bị bác. Tập finding rỗng vẫn accepted; tập kết luận rỗng không đạt. |
| I4 | Mọi reject trực tiếp đã đo giữ state nguyên byte, gồm lỗi muộn H/P3 và encoding. Mutant ghi sớm bị assertion byte giết. Không tìm thấy lỗi I4 thực tế mới. |
| I5, M1 | Có gọi helper chung, omission đã được test mới giết; vẫn còn F2 về coverage lỗi muộn và F5 về encoding sau helper. |
| I6 | Packet không tạo quyền mở lại/checkpoint/generation/ngoại lệ đẩy; không đòi triển khai các packet kế tiếp. |
| I7, M2/M3 | Run mới nhất/attempt mới nhất, app/kho/workflow, job→check URL/suite, head, gọi kiem-gate và số ID phân biệt đều được soi bằng diff và ca/probe. Nhiều file jobs, nhiều trang và hai workflow bắt buộc thật đều accepted khi hợp lệ. |
| I8 | `_slug_connector` tái dùng validator/chuẩn hoá của `_du_dieu_kien_approve`; không thay thuật toán identity. r812 hồi quy gồm identity/alias/family/surface/transport. |
| I9 | 148/148 ca r812 đã chọn đạt; init chưa lease giữ awaiting_lease, đường lease cũ false và review cũ accepted vẫn đạt. Không khai toàn bộ suite đã chạy. |
| I10, I11, M4 | Receipt connector lệch packet/generation/SHA/spec_hash/role đều rc=11; refs trùng/thiếu/thừa/sai kiểu cũng rc=11; quyết định P3 thiếu/trùng/thừa/sai kiểu/blank rc=2. Bản đủ slug H và quyết định đạt. |
| M5 | Protocol §4 nêu accept có điều kiện ADR-0054 và đủ điều kiện chính. Không kích hoạt ADR trong packet. |

Các lớp thiết kế `connector-verdict-incomplete`, `ci-attempt-provenance-missing`, `conflicting-evidence-overwrite` và phần connector của `findings-not-receipt-bound` không lộ lại lỗi hành vi cũ trong phạm vi đo: pending không hoàn tất; finding ở mọi endpoint bị đọc; attempt/jobs khác bị bác; duplicate ID mâu thuẫn bị bác trước lọc/map; P3 phải có H và quyết định. Bản lặp ID **giống hệt** được nhận; cùng ID ở **hai endpoint khác nhau** vẫn được nhận. Review/issue comment P1 ở head cũ hợp lệ không chặn head hiện hành đã có kết luận. Các chốt còn thiếu test được giữ ở F2, không báo sai rằng chốt sản phẩm đã biến mất.

#929 đã ở base: `_che_do_0054` quét đúng cụm khai trên các tệp ADR, không ghim số 0055. Hai đặc tả ràng buộc của review này không yêu cầu số tệp cố định; I9 vẫn xác định chế độ ở đường lease mới. Không tìm thấy mâu thuẫn cần dừng giữa wp834/chung với thay đổi #929. Nợ coverage `ls[0] == 0` của #929 nằm ngoài phạm vi theo prompt.

## Đối chiếu từng ca bắt buộc `nghiem_thu`

Tên dưới đây lược tiền tố `r834_` cho gọn. Mọi ca trong bảng có baseline xanh. Phân loại kill dựa tên ca, rc, exception và thông điệp đầy đủ; log không cắt stderr.

| mục bắt buộc | ca | mutant | phép đo / lý do đỏ |
|---|---|---|---|
| sạch lop=[] + connector sạch → accepted | sach_accepted | bo_ket_luan_issue_comment | nền 0/accepted; mutant AssertionError đòi 0 được 12, connector chưa xong |
| đầu remote khác pending | dau_nhanh_lech | bo_dau_nhanh_remote | nền 5/≠pending; mutant đòi 5 được 0 |
| check bắt buộc vắng | check_vang; job_tro_check_khong_co | job_vang_bo_qua; noi_check_theo_ten | nền 12/VẮNG hoặc không trỏ check-run; mutant đòi 12 được 0 |
| cùng tên từ app khác | check_app_khac | bo_app | nền 12/không từ app; mutant được 0 |
| cùng tên từ workflow khác cùng app | check_workflow_khac | bo_path_workflow | nền 12/VẮNG; mutant được 0 |
| attempt mới chạy, check cũ xanh | rerun_dang_chay | bo_attempt_moi_nhat | nền 12/chưa xanh; mutant được 0. Mutant phối hợp run-state và job-attempt vì hai chốt cùng chặn. attempt_moi_job_cu có mutant riêng. |
| check-run khác kho | check_kho_khac | bo_kho_check_run | nền 12/kho khác; mutant được 0 |
| PR khác cùng head | pr_khac_cung_head | bo_neo_pr_phan_tu | nền 12/không thuộc; mutant được 0 |
| review PENDING không xong | review_pending | pending_la_xong | nền 12/chưa xong; mutant được 0 |
| CHANGES_REQUESTED P1 | review_changes_p1 | bo_finding_review | nền 12/còn P1; mutant được 0 |
| issue comment P1 | issue_comment_p1 | bo_finding_issue_comment | nền 12/còn P1; mutant được 0 |
| cùng ID hai nội dung P1 rồi P3 | cung_id_hai_noi_dung | bo_nhat_quan_id | nền 12/hai nội dung; mutant được 0 |
| cùng run ID khác path | run_cung_id_khac_path | bo_nhat_quan_id | nền 12/hai nội dung; mutant được 0 |
| offline P3 thiếu quyết định | p3_offline_thieu_qd | bo_p3_offline | nền 2/P3 còn mở; mutant được 0 |
| connector P3 thiếu quyết định | p3_connector_thieu_qd | bo_p3_connector | nền 2/P3 còn mở; mutant được 0 |
| connector P3 không slug H | p3_connector_khong_slug | khoa_id_so | nền 11/cần biên nhận connector; mutant được 0 |
| bằng chứng dương rỗng | bang_chung_duong_rong; state_required_checks_rong | bo_bang_chung_duong; bo_luoc_do_state | nền 12/chưa xong và 8/state hỏng; mutant được 0 |
| input hỏng giữ byte | dau_vao_hong_state_nguyen | ghi_truoc_khi_doc | nền 12/JSON hỏng và byte nguyên; mutant chết bởi đúng `AssertionError: I4: state đổi sau khi accept từ chối` |

Danh sách bắt buộc cụ thể có đủ ca/kill hợp lệ; điều này không đóng các khoảng trống F2 và hai ca parser có tín dụng giả F4 ngoài danh sách tối thiểu.

## Toàn bộ quan hệ mutant → ca đã đo

44 mutant tên r834, cộng mutant r812_bo_generation được dùng cho ca connector mới: **45 mutant / 51 quan hệ**, trong đó 50 quan hệ tới 50 ca r834 và 1 tới ca r812. Reviewer xác nhận **49 quan hệ GIẾT đúng, 2 TÍN DỤNG GIẢ**; không mutant khai báo sống. Theo mutant: 44 có kill hợp lệ, 1 chỉ crash. Runner gốc khai cả 51 GIET, là sai ở đúng hai dòng F4.

| mutant | ca | phân loại reviewer | lý do/exception |
|---|---|---|---|
| r812_bo_generation | r812_bien_nhan_lech_generation | GIET | AssertionError: r812 review ['bn']: đòi rc=11, được rc=0; stderr='' |
| r812_bo_generation | r834_bnc_lech_generation | GIET | AssertionError: r834 accept: đòi rc=11, được rc=0; stderr='' |
| r834_bo_ket_luan_issue_comment | r834_sach_accepted | GIET | AssertionError: r834 accept: đòi rc=0, được rc=12; stderr='connector chưa xong trên fc2a38704723d87a08d6c351bf5f957f3d4eecf8: không review hoàn tất/kết luận nào của chatgpt-codex-connector[bot]' |
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
| r834_run_cu_nhat | r834_run_moi_nhat_do | GIET | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr="CẢNH BÁO: 'gate (ubuntu-latest)' có 1 run ở suite khác (300) — bỏ qua\nCẢNH BÁO: 'gate-cong-cu-gop (ubuntu-latest)' có 1 run ở suite khác (301) — bỏ qua\nCẢNH BÁO: 'gate-ops (ubuntu-latest)' có 1 run ở suite khác (302) — bỏ qua\nCẢNH BÁO: 'gate-packet-loop (ubuntu-latest)' có 1 run ở suite khác (303) — bỏ qua\nCẢNH BÁO:… (toàn bộ trong DECLARED.jsonl) |
| r834_bo_kho_url_job | r834_job_url_kho_khac | GIET | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_noi_check_theo_ten | r834_job_tro_check_khong_co | GIET | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_noi_check_theo_ten | r834_job_url_qua_dai | GIET | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_jobs_total_toan_cuc | r834_hai_tep_jobs | GIET | AssertionError: r834 accept: đòi rc=0, được rc=12; stderr='KHÔNG ĐO ĐƯỢC: workflow_jobs: cần trang {`jobs`, `total_count`} cùng một lần lấy, id int, tập id phân biệt = total_count' |
| r834_badge_chi_P | r834_badge_ngoai_mien_review | GIET | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_changes_khong_hang_lot | r834_review_changes_khong_hang | GIET | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_commit_thieu_la_cu | r834_review_comment_thieu_commit | GIET | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' |
| r834_reviewed_commit_tim_dau | r834_reviewed_commit_sai_dang | TIN_DUNG_GIA | AssertionError đòi 12, được 1; IndexError: no such group (CLI traceback) |
| r834_reviewed_commit_tim_dau | r834_reviewed_commit_mau_thuan | TIN_DUNG_GIA | AssertionError đòi 12, được 1; IndexError: no such group (CLI traceback) |
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

## Kết quả lệnh, rc và bằng chứng dương

Các đường dưới đây tương đối với thư mục làm việc `rv3`; mọi script đã chạy trên bản sao `out/copy`. Biến môi trường chung: `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR="$PWD/out/tmp"`; runner còn cô lập Git global/system, đặt `GIT_ALLOW_PROTOCOL=file`. File JSONL lưu rc của **CLI con**; rc=0 của script thu thập chỉ nói thu thập hoàn tất, không biến mutant sống/crash thành pass.

| lệnh | rc thật | kết quả / hiện vật |
|---|---:|---|
| python -B out/run_review.py declared | 0 | 50/50 nền r834; 45 mutant, 51 quan hệ. `DECLARED.jsonl`, `DECLARED.stderr`; 2 tín dụng giả như F4. |
| python -B out/audit_mutants.py | 0 | 3 mutant mới × đủ 50 ca: đều sống 50/50; `AUDIT_MUTANTS.jsonl`. Đây là nghiệm thu **failed**, không phải 150 ca chứng minh gate an toàn. |
| python -B out/run_review.py r812 | 0 | 148/148 ca được chọn đạt; 1 not_run theo giới hạn nội dung đường dẫn; `R812.jsonl`. |
| python -B out/probe_review.py | 0 | 86 probe; mọi rc khớp kỳ vọng và mọi reject giữ byte; `PROBES.jsonl`. |
| python -B out/extra_review.py | 0 sau sửa scratch reviewer | 21 phép đo; ambiguity/full SHA controls, dạng thật #889, head cũ, nhiều trang/nhiều workflow, các mutant có thay đổi hành vi; `EXTRA.jsonl`. Lần đầu script reviewer lỗi FileExistsError vì dùng lại thư mục fixture, chưa đo candidate; đã chuyển scratch riêng và chạy lại. |
| python -B out/late_input_review.py | 0 | 10 phép đo; 4 kỳ vọng từ chối trước stop bị vi phạm (8 mong đợi, 3 sentinel). `LATE_INPUT.jsonl`; đây là bằng chứng **failed I5**, không phải 10/10 pass. |
| python -B out/confirm_review.py | 0 | Hook gọi tiếp hàm gốc chứng minh thứ tự lỗi; mutant parser sửa cấu trúc bị hai ca gốc giết đúng lý do; mutant hỏng phá control sạch. `CONFIRM.jsonl`. |
| python -B out/copy/.claude/dev/packet_loop.py doctrine-scan --root out/copy | 0 | 10 tệp, 0 chỗ chép doctrine; `doctrine-scan.log` |
| python -B out/copy/.claude/dev/packet_loop.py adr-song --root out/copy | 0 | 55 ADR, 55 dòng, khớp 1–1; ngoại lệ 0016 được khai sẵn; `adr-song.log` |
| git -C src diff --check ab344da 7436fe3 | 0 | không lỗi whitespace; `CHECKS.json` |
| git -C src diff --numstat ab344da 7436fe3 | 0 | 3 tệp, 406 thêm / 5 xoá; `CHECKS.json` |
| snapshot đầu/cuối + git status/diff/index | 0 | 6.001 tệp/link, 0 delta; `SOURCE_INITIAL.json`, `SOURCE_FINAL.json`, `SOURCE_INTEGRITY.json` |

Suite đầy đủ `python .claude/dev/packet_loop_test.py`: **not_run**, theo ưu tiên chạy chọn lọc trong prompt (~45 phút cho full suite). Không khai N/N toàn repository, không xác minh CI online hay Windows. Bare Ruff lint và Ruff pin/probe contract: **not_run**, không gắn nhãn Ruff passed. SyntaxWarning tại test:3714 là có sẵn, không được tính là kill hay finding mới.

Ca r812_r4_own_parent được loại trước khi chạy để không dựng nội dung đường dẫn có thành phần đi lên cây. Hướng thử đường dẫn thoát cây chỉ mô tả: kiểm receipt/readback path qua thành phần đi lên hoặc liên kết đưa ra ngoài cây, yêu cầu từ chối có kiểm soát và state nguyên byte; không tạo payload hay chạy các hướng đó. Không suy an toàn đường dẫn từ việc không chạy.

Ngoài phạm vi, không phân hạng: mo-lai, cho_chu_kho, checkpoint #813, vòng P3 #814, generation #815, ghi đẩy/kích hoạt #816, và nợ coverage riêng #929 nêu trong prompt. Verdict chỉ neo commit dòng 2, không cấp quyền push/merge/land.
