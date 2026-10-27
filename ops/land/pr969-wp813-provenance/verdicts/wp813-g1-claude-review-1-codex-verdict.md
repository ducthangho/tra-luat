Verdict: request_changes
Reviewed commit: d7893933b0e02d6cebd1d7f5e17df05ea2a8de04
Spec sha256: 9df36da1ef2be23c7519934bf6aee0dfecb6d2082cb8e485c7a6819c8a6154f3; Chung sha256: 4e3d1e1b3f6a0b60b96ad7b70f0ece97eca4bb3d6d10defeab1cd24ac6d1cbf0

**Kết luận:** request_changes — **4 lớp P2; không có P0/P1/P3 mới được phân hạng trong phạm vi này**. Ngưỡng của prompt là không còn P0/P1/P2. Verdict chỉ neo commit dòng 2, không cấp quyền push, merge hoặc land.

Reviewer độc lập: Codex/OpenAI, họ `openai`; executor theo lease bản chép: Claude, họ `claude`; Packet #813 revision 2 generation 1, review class `sensitive`, assurance target `cross_approved`. Phiên dùng shell công cụ trong Linux, transport machine. Nhãn model/effort/session phục vụ thực tế và launcher `codex_cli` không được attestation độc lập trong lần đo này; không tự tạo receipt assurance. Đã đọc toàn bộ `runs/4fc65684/prompt.snapshot`; gốc SRC/OUT/tham-chieu là thư mục rv1 theo chỉ dẫn trực tiếp của người dùng.

| slug | hạng P0–P3 | biểu hiện file:dòng | phép đo/tái hiện đã chạy | hướng vá |
|---|---|---|---|---|
| `ci-reopen-run-context-unbound` | P2 | `.claude/dev/packet_loop.py:2977`, `:2978`, `:3279` | Run 101 mới nhất xanh; run 100 cũ rerun đỏ có check ID lớn hơn ⇒ `mo-lai` rc=0, `running`. Check mới hơn thiếu app/url cũng bị lọc bỏ và check đỏ cũ được nhận. | Mang ngữ cảnh workflow/run/attempt vào cửa CI đỏ và nối đúng suite/check; kiểm các trường định phạm vi trước lọc. |
| `checkpoint-spec-context-unbound` | P2 | `.claude/dev/packet_loop.py:2934`, `:3018`, `:3023` | Checkpoint không có `spec_hash` ⇒ rc=0, rời `cho_chu_kho`; thêm hash đúng cũng bị rc=7 vì schema cấm trường đó. | Bổ sung hash đặc tả vào schema và so đủ tuple I10 đúng vai trò nguồn. |
| `checkpoint-nested-scope-unvalidated` | P2 | `.claude/dev/packet_loop.py:3018`, `:3025` | `pham_vi` chứa list/object ⇒ rc=1, `TypeError: unhashable type`; tái hiện ở cả cửa cấp quyền vá và quyền đẩy. | Kiểm kiểu và miền từng phần tử trước phép `set`; từ chối có kiểm soát, state nguyên byte. |
| `r813-mutation-evidence-incomplete` | P2 | `.claude/dev/packet_loop_test.py:8923`, `:8930`, `:8948`, `:8940` | Mutant slug chết do `thieu-lop-am`, còn chặn cả baseline hợp lệ. Bỏ ghi checkpoint_day, bỏ kiểm generation, bỏ cấm refs trùng đều sống 30/30 r813. Bỏ kiểm kiểu path M5 sống 93/93 r813+r834. | Sửa mutant đúng predicate; bổ sung ca âm/đối chứng và oracle nội dung quyền; đăng ký mutant cho hai nguyên nhân độc lập. |

**F1 — `ci-reopen-run-context-unbound`.** I7 vẫn áp cho R dù readback do người gọi thu thập. Cửa mới chỉ nhận tên job trong `check_refs` và một danh sách check-runs; `max(id)` tại dòng 2977–2978 gộp mọi suite/workflow cùng tên, không có ánh xạ đến run/attempt như `_kiem_ci` của `accept`.

Phép đo `followup_probes/latest_run_green_older_rerun_red` dựng cùng kho `o/r`, PR 55, cùng head: run 100/suite 500 là run cũ được rerun; run 101/suite 501 là run mới nhất đã xanh. Check 300 thuộc run 101 xanh; check 301 thuộc lần rerun của run 100 đỏ. CLI nhận cả hai check, chọn 301, trả rc=0 và ghi quyền `ci-do`. `run_context.json` ghi đầy đủ quan hệ run/suite của fixture; CLI hiện không có đầu vào để đọc quan hệ đó. Đây là phép đo thiếu khả năng kiểm nhất quán I7, không phải đòi máy tự gọi GitHub hay chứng minh tính chân thực của R. Kịch bản workflow khác dùng cùng tên job cũng được nhận (`probes/ci_unrelated_workflow_same_job`).

Cùng lớp bỏ mất ngữ cảnh: `ci_newer_app_missing` và `ci_newer_url_missing` đặt check mới hơn xanh nhưng mất một trường phạm vi; cửa bỏ bản mới, chọn bản đỏ cũ và rc=0. Các đối chứng hiện tại vẫn từ chối đúng head khác, repo khác, app khác hợp lệ, check đang chạy và check mới hơn xanh đầy đủ trường.

Hướng vá tại `cmd_mo_lai` và hợp đồng CLI/`check_refs`: tái dùng phần chọn ngữ cảnh của `_kiem_ci` hoặc helper chung, định danh `(app, workflow, job)`, xác định run mới nhất/attempt mới nhất rồi nối job → check/suite; tách predicate kết luận đỏ khỏi predicate xanh. Không dùng check ID để suy run nào mới nhất. Test khóa: hai run cùng head, run cũ rerun sau run mới xanh; hai workflow cùng tên job; bản mới mất app/url. Mutant gỡ liên kết run/suite phải làm ca đỏ. Nguy cơ khi vá: vô tình đổi hợp đồng `accept`, chọn nhầm run mới nhất toàn kho thay vì từng workflow, hoặc chặn đỏ hợp lệ vì app/workflow không liên quan; giữ các đối chứng đó.

**F2 — `checkpoint-spec-context-unbound`.** I10 đòi mỗi hiện vật dùng ở cửa khớp `(packet, generation, sha, spec_hash)`. `KHOA_CHECKPOINT` chỉ có sáu trường, không có `spec_hash`; phép so dưới đó cũng không đọc hash. M3 không miễn I10. Đã merge checkpoint fixture vào master của bare repo cục bộ; fetch và ls-remote đều đi đường thật. `checkpoint_missing_spec_hash` trả rc=0 và `cho_chu_kho → running`. `checkpoint_with_correct_spec_hash` và `checkpoint_with_wrong_spec_hash` đều trả rc=7 ở schema, không phải phép so hash. Vì vậy không thể đưa hiện vật đủ tuple I10 vào cửa hiện hành, và không phân biệt được checkpoint của revision/spec khác nếu packet/generation/head giữ nguyên.

Vá trong schema, phép so của `cmd_chu_kho_duyet` và fixture `_ck813`: yêu cầu hash và so với ngữ cảnh nguồn đã ghi trong state; nếu quyền nguồn có thể đi qua revision thì lưu đủ ngữ cảnh nguồn để không so nhầm với ứng viên. Test khóa: đúng hash được nhận, thiếu/sai hash bị từ chối nguyên byte; mutant bỏ phép so hash phải bị giết. Nguy cơ: làm vỡ checkpoint cũ hoặc so hash ứng viên với quyền nguồn; phải lựa chọn tương thích tường minh, không tự mặc định hash từ state để hợp thức hóa hiện vật thiếu neo.

**F3 — `checkpoint-nested-scope-unvalidated`.** Schema chỉ xác nhận `pham_vi` là list. Khi list có một list hoặc object, `set(d['pham_vi'])` ném TypeError không được bắt. `checkpoint_scope_list`, `checkpoint_scope_dict` và `checkpoint_day_nested_scope` đều có rc=1, traceback, state giữ nguyên byte. Đây là lỗi từ chối đầu vào không có kiểm soát; **không** khẳng định đã làm hỏng state hay cấp quyền từ các đầu vào này. Đối chứng giá trị chuỗi ngoài miền trả đúng rc=7/`['pham_vi']`, checkpoint đúng được nhận.

Vá tại phép xác thực scope trước `set`, không bắt mọi ngoại lệ để che lỗi: mỗi phần tử phải là chuỗi thuộc miền đóng; sau đó mới xét quyền được yêu cầu. Test khóa hai kiểu lồng ở cả hai nhánh, đòi rc=7/lý do schema hoặc scope, không traceback, state nguyên byte; mutant bỏ kiểm phần tử phải chết bằng oracle đúng mã/lý do, không được ghi công traceback. Nguy cơ: coi list rỗng hoặc scope không biết là quyền hợp lệ, hoặc lẫn `cho_phep_va` với `cho_phep_day`.

**F4 — `r813-mutation-evidence-incomplete`.** Đây là lỗi của chứng cứ nghiệm thu mới #813, không mở lại nợ P3 ngoài phạm vi của #834.

- `r813_slug_tu_dat` đổi `finding_id=a.finding_id` thành `None`. Ca mục tiêu đỏ với **rc vẫn 11**, lý do `thieu-lop-am`; baseline `ci-do` hợp lệ cũng bị mutant từ chối vì lý do ấy. Harness gắn `GIET`, nhưng mutant không chỉ gỡ chốt slug ngoài bảng và không chứng minh lỗ hổng được mở. Mutant độc lập `omit_only_slug_membership` chỉ bỏ predicate đó mới làm đúng ca trả rc=0 thay vì 11.
- `r813_hai_slug_doc_lap` là đối chứng bắt buộc nhưng không có mutant khai báo trỏ tới. Mutant độc lập `collapse_independent_causes` đã đo làm đúng ca này bị blocked (rc=3 thay vì 0). Nên khai mutant này trong bộ nghiệm thu. Ba ca khác không có target khai báo là `r813_ci_do_running`, `r813_connector_cho_chu_kho`, `r813_checkpoint_day`; không suy từ việc thiếu target rằng chúng không giết gián tiếp mutant nào.
- Oracle `r813_checkpoint_day` chỉ kiểm state vẫn `approved_pending`. Mutant bỏ hẳn ghi `checkpoint_day` vẫn sống toàn bộ 30 ca #813. Counterexample độc lập xác nhận CLI rc=0 nhưng quyền không tồn tại.
- Mutant bỏ so generation ở điều kiện `running` và mutant bỏ tính duy nhất của refs cũng sống 30/30. Probe riêng cho thấy mutant thứ nhất nhận quyền `ci-do` thuộc generation khác, mutant thứ hai nhận `check_refs` trùng; candidate từ chối đúng. Đây là lỗ độ phủ, không phải khai candidate đang có hai lỗi ấy.
- M5 đang kiểm đúng kiểu path trên mọi run. Nhưng bỏ riêng kiểm này vẫn sống 30 ca #813 + 63 ca #834; counterexample run mới có `path` sai kiểu làm mutant `accept` rc=0, candidate rc=12/`KHÔNG ĐO ĐƯỢC`, byte state giữ nguyên. Điểm này chạm đúng M5, nên thuộc phạm vi review; không quy nợ neo head/kiểu ID trang cũ #834 vào đây.

Hướng vá tại test/`MUTANTS`: thêm đối chứng cùng họ cho mutant slug; kiểm đầy đủ tuple của quyền sau cấp/thay, không chỉ state; thêm ca generation sai, check_refs lặp, path sai kiểu (và schema repository/full_name), mỗi ca có baseline dương và mutant đúng chốt. Các cặp search/replace đã chạy nằm trong `extra_mutants/*/mutation.json`. Chúng là dữ liệu phản chứng trên bản riêng, không phải bản vá sản phẩm để áp vào packet. Nguy cơ: mutant chết ở bước dựng nền, rc chung, hoặc CLI sập; tiếp tục kiểm exception, thông điệp, đối chứng và state byte thay vì chỉ số tổng.

**Định danh, write set và phạm vi.** `IDENTITY.json` ghi argv, rc, stdout/stderr đầy đủ. HEAD = `d7893933b0e02d6cebd1d7f5e17df05ea2a8de04`, tree = `a067a8fafece51860c4957817f0cbc11e1106f23`, origin/master = base `f577ab5b467510f3fa7ed27107dc2eab539d3bef`. Base là tổ tiên (merge-base --is-ancestor rc=0); symbolic-ref rc=1 dự kiến chứng minh detached; is-shallow=false; `.git` là thư mục thật. Hai đặc tả băm lại khớp dòng 3; blob phần chung tại exact HEAD cũng khớp worktree. Sub-spec bản chép không có trong SRC là trạng thái đúng theo prompt.

`git diff --numstat base head` rc=0: packet_loop.py 143 thêm/5 xoá; packet_loop_test.py 167 thêm/1 xoá ⇒ **2 đường dẫn, 310 dòng thêm ≤450**. `diff --check` rc=0. Đã đọc toàn bộ diff, lưu `PATCH.diff`. Lease bản chép có thêm đường handoff dành cho nhánh lease; không có thay đổi handoff trong candidate, đúng giới hạn diff hai tệp của spec. `wp834-g1-codex-luot8-VERDICT.md` chỉ được dùng làm đầu vào thiết kế/lịch sử nợ, không thay đặc tả hay bằng chứng chạy độc lập.

**Đối chiếu từng yêu cầu `nghiem_thu`.** Tất cả ca nền nêu dưới đã đạt. “Giết” trong bảng là lỗi assertion có lý do xác định, không phải CLI sập.

| ca bắt buộc | ca `r813_*` tương ứng | mutant khai báo và kết quả thực đo |
|---|---|---|
| Chạm trần qua mo-lai → blocked | `r813_cham_tran_mo_lai` | `r813_mo_lai_khong_xet`: AssertionError, đòi rc3 được0; giết đúng. |
| Cùng nguyên nhân dưới hai comment ID mới đếm chung | `r813_cung_slug_hai_id` | `r813_dem_theo_id`: bước cuối đòi rc3 được0; giết đúng. |
| Đối chứng hai nguyên nhân độc lập đếm riêng | `r813_hai_slug_doc_lap` | Không có target khai trong MUTANTS; mutant tự dựng `collapse_independent_causes` giết đúng bằng rc3 thay vì0. Thiếu nghiệm thu khai báo, F4. |
| Slug ngoài biên nhận bị từ chối | `r813_slug_ngoai_bien_nhan` | `r813_slug_tu_dat`: rc11 với `thieu-lop-am`, sai ngữ nghĩa; mutant đúng predicate tự dựng làm rc0. F4. |
| Begin-attempt khi đã chạm trần bị từ chối | `r813_begin_attempt_cham` | `r813_begin_khong_xet`: rc0 thay vì3; giết đúng. |
| Cửa khép lượt không bị chặn | `r813_cua_khep_khong_chan` | `r813_chan_cua_khep`: rc3/same-failure thay vì0; giết đúng. |
| Mo-lai không finding bị từ chối | `r813_khong_finding` | `r813_bo_tap_rong`: rc0 thay vì2; giết đúng. |
| Connector tập con P0–P2 bị từ chối | `r813_connector_tap_con` | `r813_tap_con_lot`: rc0 thay vì11; giết đúng. |
| CI đỏ và connector P1 cùng head | `r813_ci_va_p1_cung_head` | `r813_bo_ci_do`: rc0 thay vì12; giết đúng. |
| Connector đến sau CI | `r813_connector_sau_ci` | `r813_chi_tu_approved`: bước1 rc8 thay vì0; `r813_ci_do_doi_connector_xong`: bước0 rc12/connector chưa xong thay vì0. Cả hai đúng chốt. |
| Checkpoint chỉ ở nhánh khác bị từ chối | `r813_checkpoint_nhanh_khac` | `r813_checkpoint_ref_tuy_y`: rc0 thay vì7; giết đúng. |
| Checkpoint packet khác bị từ chối | `r813_checkpoint_packet_khac` | `r813_bo_packet_checkpoint`: rc0 thay vì7; giết đúng. |
| Không dùng cho_phep_va làm quyền đẩy | `r813_va_lam_quyen_day` | `r813_moi_pham_vi_la_du`: rc0 thay vì7; giết đúng. |
| M5 run mới in_progress thiếu repository | `r813_m5_run_moi_thieu_repository` | `r813_m5_bo_repository`: accept rc0 thay vì12; giết đúng, candidate byte state nguyên. |
| M5 path hoặc head_sha sai kiểu | `r813_m5_run_head_sai_kieu` | `r813_m5_bo_head_sha`: accept rc0 thay vì12; giết đúng. Đã có nhánh “head_sha” theo yêu cầu hoặc; chốt path riêng chưa được bảo vệ (F4). |
| Đối chứng mọi ca #834 hiện có vẫn đạt | Toàn bộ 63 `r834_*` | 63/63 PASS, không skipped; không suy thành full-suite N/N. |

**Bất biến I1–I11 và những chốt đã soi.**

| bất biến | kết quả trong phạm vi packet |
|---|---|
| I1 | mo-lai dùng H qua `_du_dieu_kien_approve`; chu-kho-duyet tự fetch/ls-remote Đ. Checkpoint vẫn thiếu tuple I10 (F2). Không yêu cầu R tự có thẩm quyền. |
| I2 | Đường lease không đổi; regression #812 qua baseline H/Đ/R bằng kho Git cục bộ. Không xác minh lease live/remote GitHub. |
| I3 | Finding rỗng, hạng connector, tập P0–P2 đúng bằng, kết luận CI allowlist có ca; nested scope checkpoint làm sập CLI (F3). |
| I4 | Các từ chối có kiểm soát đã đo giữ state nguyên byte; hai dạng nested scope cũng giữ byte nhưng traceback. Kết quả hợp lệ chạm trần ghi history/counter rồi blocked. Không thấy ghi state một phần. |
| I5 | Hai cửa mới gọi chung `_xet_dung` sau xác thực; mutant xét sớm bị giết đúng. Cửa begin chặn same-failure, cửa khép record-review vẫn chạy. Chưa miễn lỗi schema F3 vì nó xảy ra trước stop gate. |
| I6 | Candidate thay quyền mo_lai_tu khi có connector sau CI, tiêu thụ khi cấp vá; checkpoint_day mới thay quyền trước, cùng hash/phạm vi dùng lại bị chặn. Thiếu test bảo vệ nội dung quyền/generation (F4). Tiêu thụ quyền ở cửa đẩy thuộc #816, không tính thiếu ở đây. |
| I7 | Connector vẫn neo repo/PR/head và đủ trang bằng ID phân biệt; accept giữ mặc định `_doc_connector(..., p0p2=None)`, toàn bộ 63 ca #834 đạt. Nhánh ci-do mới thiếu run/workflow/attempt và kiểm đủ trường phạm vi (F1). |
| I8 | Reuse validator chuẩn của H; regression các danh tính #812 đạt. Không tạo chuẩn hóa riêng ở cửa mo-lai. |
| I9 | 149/149 ca #812 và 63/63 #834 đạt; state cũ không có hai trường mới vẫn qua chuỗi nền. Không chạy full suite, không khẳng định mọi ca còn lại đã được đo. |
| I10 | H changes_requested được probe lệch packet, generation, SHA thật khác, spec_hash, role: rc11, byte nguyên. Checkpoint không có spec_hash: F2. |
| I11 | Slug đếm từ bảng H, same-failure cộng cả history mo_lai, hai ID cùng nguyên nhân đếm chung và hai slug độc lập đếm riêng. Ref trùng/thiếu/thừa/sai kiểu được probe riêng; chốt sản phẩm đúng trong các phép đó, độ phủ mutant thiếu ở F4. |

`ci-do` nhận `failure`, `timed_out`, `startup_failure`; từ chối `success`, `cancelled`, `neutral`, `skipped`, `action_required`, `stale`, giá trị lạ và trạng thái chưa completed. Điều kiện vào `running` cần quyền ci-do hiện hành cùng generation: candidate từ chối quyền vắng/sai nguyên nhân/sai generation. Head được lấy từ state; không có cờ cho caller chọn head. Kiểm này không chữa việc chọn nhầm run trên cùng head trong F1.

Checkpoint chỉ trên nhánh khác bị từ chối; schema packet/generation/head/người quyết sai có ca riêng. Đã đọc phép đối chiếu ls-remote với ref sau fetch; không gây race mạng thật trong phiên offline. Probe `neo` trỏ issue kho khác vẫn được nhận, nhưng không phân hạng riêng: thẩm quyền M3 là hiện vật được merge ở master (Đ), spec không yêu cầu URL comment là nguồn cấp quyền thứ hai. Không nâng yêu cầu này thành finding suy diễn.

**Lệnh, mã thoát và bằng chứng.** Mọi lệnh dưới chạy trên `out/copy` hoặc mutant/fixture bên dưới OUT, với `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR=OUT/tmp`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_SYSTEM=/dev/null`, `GIT_OPTIONAL_LOCKS=0`, `GIT_ALLOW_PROTOCOL=file`. Bản sao có `core.abbrev=7`. Python 3.13.17, Git 2.43.0, PyYAML 6.0.3, Linux x86_64. Các fetch/push/ls-remote trong test dùng bare repo cục bộ; không fetch/push kho packet, không mạng, không GitHub.

| lệnh thực thi | rc | bằng chứng dương / log |
|---|---:|---|
| `python -B -W ignore out/run_review.py baseline r813_` | 0 | 30/30 PASS; `R813.log`, `baseline_r813/results.json` |
| `python -B -W ignore out/run_review.py mutants r813_` | 0 | 27 mutant/27 quan hệ mục tiêu bị harness gắn GIET, 81 đối chứng khác họ PASS; sau đọc nghĩa chỉ 26 đúng chốt, 1 sai nghĩa. `M813.log`, `mutants_r813/results.json` |
| `python -B -W ignore out/run_review.py baseline r834_` | 0 | 63/63 PASS; `R834.log`, `baseline_r834/results.json` |
| `python -B -W ignore out/run_review.py baseline r812_` | 0 | 149/149 PASS; `R812.log`, `baseline_r812/results.json` |
| `python -B -W ignore out/extra_mutants.py omit_checkpoint_day_authority omit_reopen_generation_guard omit_ref_uniqueness omit_only_slug_membership collapse_independent_causes` | 0 | Driver hoàn tất; ba mutant sống 30/30 mỗi mutant, hai mutant đúng chốt giết đúng ca đích. `EXTRA.log` và JSON từng mutant |
| `python -B -W ignore out/extra_mutants.py omit_m5_path_type` | 0 | Mutant sống 93/93; `M5_MUTANT.log` và JSON. rc0 nghĩa driver hoàn tất, không phải mutant bị giết. |
| `python -B -W ignore out/probes.py` | 0 | Ghi từng argv/rc/stdout/stderr/hash state trong `probes/results.json`; có 4 lỗi setup M5 FileExistsError, không tính kết quả sản phẩm; đã đo lại bằng followup bên dưới. |
| `python -B -W ignore out/followup_probes.py` | 0 | M5 thiếu/sai kiểu được từ chối rc12; tuple quyền/checkpoint và CI trong `followup_probes/results.json`. Probe `running_authority_missing` không xóa được key vì helper merge state: loại khỏi bằng chứng; đã thay bằng ca last bên dưới. |
| `python -B -W ignore out/last_probes.py` | 0 | Thiếu key quyền thật → rc8; nested scope quyền đẩy → rc1; H dùng SHA khác thật → rc11. `last_probes/results.json` |
| `python -B -W ignore out/mutant_counterexamples.py` | 0 | CLI trên mutant: không ghi quyền vẫn rc0; path sai kiểu được accepted; mutant slug chặn baseline đúng. `mutant_counterexamples/results.json` |
| `python -B -W ignore out/boundary_mutant_probes.py` | 0 | Mutant generation/refs nhận đầu vào sai rc0; `boundary_mutant_probes/results.json` |
| `python -B out/copy/.claude/dev/packet_loop.py doctrine-scan --root out/copy` | 0 | 10 tệp, 0 chỗ chép doctrine; `DOCTRINE.log`, `.rc`, `.stderr` |
| `python -B out/copy/.claude/dev/packet_loop.py adr-song --root out/copy` | 0 | 55 ADR, 55 dòng §20 khớp 1–1; ngoại lệ 0016 có sẵn; `ADR.log`, `.rc`, `.stderr` |

Đã đọc mã hai helper được cung cấp: `chon.py` in ca đỏ nhưng không đặt exit code theo kết quả; `dotbien.py` in số lỗi nhưng cũng không `sys.exit(loi)`, và cắt ngắn thông điệp. Vì vậy dùng `run_review.py` với cùng `chay_suite`, `_phan_loai_dot_bien`, `_doi_chung_khac_ho`, `_phan_loai_giet`, thêm kiểm mỏ neo duy nhất và giữ nguyên toàn văn exception. Không gọi một rc0 của helper là bằng chứng đạt. Tất cả nhóm chọn lọc có inventory và số ca khớp; tổng **242/242 ca nền PASS**, không skipped trong tập này.

**Giới hạn và ngoài phạm vi.** Không chạy full suite 45–60 phút; không đo CI online, Windows hoặc bare Ruff lint; không chạy bộ mutant cũ #812/#834 ngoài các ca regression đã nêu. M4/protocol §4/§12 đã tách; không xem việc đồ thị protocol chưa có cho_chu_kho là finding. #814, #815, tiêu thụ quyền ở cửa đẩy #816 và kích hoạt ADR-0054 ngoài phạm vi. Nợ P3 cũ `required-mutation-coverage-missing` của #834 về neo head issue comment/kiểu ID trang không được xét lại hay khai đã đóng.

Các hướng thử đòi soạn đường dẫn thoát cây chỉ được mô tả: kiểm checkpoint/receipt có đường dẫn điều hướng ra ngoài gốc hoặc liên kết trỏ ra ngoài cây; đòi từ chối trước đọc/ghi ngoài phạm vi và state nguyên byte. Không tự tạo payload đường dẫn thoát cây, không chạy các probe ấy. Liên kết của các fixture regression được đọc trước khi chạy và nằm trong cây fixture dưới OUT.

**Toàn vẹn nguồn.** `python -B -W ignore out/finalize_review.py` rc=0. Snapshot nguồn sau preflight và cuối phiên: **6989 → 6989 tệp thường, 0 delta byte/mode**, bao gồm `.git`, tracked/untracked/ignored; 0 symlink. HEAD/tree/ref và status/diff/index được kiểm lại sạch; hai tệp mã trong bản sao nền vẫn giống SRC từng byte. Xem `SOURCE_INITIAL.json`, `SOURCE_FINAL.json`, `SOURCE_INTEGRITY.json`, `FINAL_CHECKS.json`, `CHECKS.json`. Đây là đối chiếu hai mốc, không phải giám sát mọi write trong lịch sử phiên. Sandbox thực tế workspace-write; nguồn được đối xử chỉ đọc, artifact và fixture do reviewer tạo nằm dưới OUT.

**Phụ lục: audit đầy đủ 27 mutant khai báo.** Mọi exception trong bảng là `AssertionError`, không có `CliSapDo`/traceback được tính điểm. Toàn văn không cắt ngắn nằm trong JSON; các path fixture được viết gọn thành `OUT` ở đây.

| mutant | ca đích | exception/lý do thực đo | kết luận ngữ nghĩa |
|---|---|---|---|
| `r813_bo_ci_do` | `r813_ci_va_p1_cung_head` | AssertionError: r813 bước 0: đòi rc=12, được rc=0; stderr='' | Giết đúng chốt |
| `r813_ci_do_nhan_xanh` | `r813_ci_khong_do` | AssertionError: r813 bước 0: đòi rc=12, được rc=0; stderr='' | Giết đúng chốt |
| `r813_bo_tap_rong` | `r813_khong_finding` | AssertionError: r813 bước 0: đòi rc=2, được rc=0; stderr='' | Giết đúng chốt |
| `r813_slug_tu_dat` | `r813_slug_ngoai_bien_nhan` | AssertionError: r813: rc đúng mà lý do khác — đòi 'slug-ngoai-bang', stderr="biên nhận OUT/mutants_r813/r813_slug_tu_dat/fixtures/r813_slug_ngoai_bien_nhan/3bn.yaml không đủ điều kiện changes_requested: ['thieu-lop-am']" | KHÔNG ghi công: đổi sang lỗi thiếu lớp âm |
| `r813_tap_con_lot` | `r813_connector_tap_con` | AssertionError: r813 bước 0: đòi rc=11, được rc=0; stderr='' | Giết đúng chốt |
| `r813_chi_tu_approved` | `r813_connector_sau_ci` | AssertionError: r813 bước 1: đòi rc=0, được rc=8; stderr="mo-lai connector không chạy từ 'running' (đòi approved_pending của packet áp ADR-0054, hoặc running mở lại bằng ci-do cùng generation)" | Giết đúng chốt |
| `r813_ci_do_doi_connector_xong` | `r813_connector_sau_ci` | AssertionError: r813 bước 0: đòi rc=0, được rc=12; stderr='connector chưa xong trên 12b42b272c30ce026982f6decf4a7c1c8c3ef5b5: không review hoàn tất/kết luận nào của chatgpt-codex-connector[bot]' | Giết đúng chốt |
| `r813_dem_theo_id` | `r813_cung_slug_hai_id` | AssertionError: r813 bước 4: đòi rc=3, được rc=0; stderr='' | Giết đúng chốt |
| `r813_mo_lai_khong_xet` | `r813_cham_tran_mo_lai` | AssertionError: r813 bước 1: đòi rc=3, được rc=0; stderr='' | Giết đúng chốt |
| `r813_begin_khong_xet` | `r813_begin_attempt_cham` | AssertionError: r813 bước 2: đòi rc=3, được rc=0; stderr='' | Giết đúng chốt |
| `r813_chu_kho_khong_xet` | `r813_chu_kho_cham_tran` | AssertionError: r813 bước 2: đòi rc=3, được rc=0; stderr='' | Giết đúng chốt |
| `r813_chan_cua_khep` | `r813_cua_khep_khong_chan` | AssertionError: r813 bước 3: đòi rc=0, được rc=3; stderr='cùng finding-id lặp tới trần (ci-gate×1; trần 1) — packet về blocked. Lặp lại nghĩa là bản vá không trúng gốc; ghi failure evidence + handoff rồi dừng.' | Giết đúng chốt |
| `r813_xet_truoc_dau_vao` | `r813_xet_dung_sau_dau_vao` | AssertionError: r813 bước 2: đòi rc=11, được rc=3; stderr='cùng finding-id lặp tới trần (ci-gate×1; trần 1) — packet về blocked. Lặp lại nghĩa là bản vá không trúng gốc; ghi failure evidence + handoff rồi dừng.' | Giết đúng chốt |
| `r813_checkpoint_ref_tuy_y` | `r813_checkpoint_nhanh_khac` | AssertionError: r813 bước 1: đòi rc=7, được rc=0; stderr='' | Giết đúng chốt |
| `r813_bo_packet_checkpoint` | `r813_checkpoint_packet_khac` | AssertionError: r813 bước 1: đòi rc=7, được rc=0; stderr='' | Giết đúng chốt |
| `r813_moi_pham_vi_la_du` | `r813_va_lam_quyen_day` | AssertionError: r813 bước 0: đòi rc=7, được rc=0; stderr='' | Giết đúng chốt |
| `r813_checkpoint_dung_lai` | `r813_checkpoint_day_dung_lai` | AssertionError: r813 bước 1: đòi rc=7, được rc=0; stderr='' | Giết đúng chốt |
| `r813_va_ve_running_khong_tieu` | `r813_checkpoint_va` | AssertionError: r813: đòi {'state': 'running', 'mo_lai_tu': None}, được {'state': 'running', 'mo_lai_tu': {'generation': 1, 'nguyen_nhan': 'connector', 'sha': '12b42b272c30ce026982f6decf4a7c1c8c3ef5b5'}} | Giết đúng chốt |
| `r813_m5_bo_repository` | `r813_m5_run_moi_thieu_repository` | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' | Giết đúng chốt |
| `r813_ci_do_bo_app` | `r813_ci_do_app_khac` | AssertionError: r813 bước 0: đòi rc=12, được rc=0; stderr='' | Giết đúng chốt |
| `r813_ci_do_luot_cu` | `r813_ci_do_chay_lai_xanh` | AssertionError: r813 bước 0: đòi rc=12, được rc=0; stderr='' | Giết đúng chốt |
| `r813_lop_bo_hang` | `r813_connector_lop_p3` | AssertionError: r813 bước 0: đòi rc=11, được rc=0; stderr='' | Giết đúng chốt |
| `r813_bo_head_checkpoint` | `r813_checkpoint_head_lech` | AssertionError: r813 bước 1: đòi rc=7, được rc=0; stderr='' | Giết đúng chốt |
| `r813_bo_generation_checkpoint` | `r813_checkpoint_generation` | AssertionError: r813 bước 1: đòi rc=7, được rc=0; stderr='' | Giết đúng chốt |
| `r813_bo_nguoi_quyet` | `r813_checkpoint_nguoi_quyet` | AssertionError: r813 bước 1: đòi rc=7, được rc=0; stderr='' | Giết đúng chốt |
| `r813_cho_chu_kho_khong_quyen` | `r813_state_cho_chu_kho_mat_quyen` | AssertionError: r813 bước 2: đòi rc=8, được rc=0; stderr='' | Giết đúng chốt |
| `r813_m5_bo_head_sha` | `r813_m5_run_head_sai_kieu` | AssertionError: r834 accept: đòi rc=12, được rc=0; stderr='' | Giết đúng chốt |

Các phép đo trên đủ để request_changes; không lấy việc ca nền xanh để bác bỏ phản chứng độc lập hoặc coi packet đã nghiệm thu toàn phần.
