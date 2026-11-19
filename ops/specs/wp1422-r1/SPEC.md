# wp1422 r1 — `mo-lai ci-do` cho lane target có reviewer `codex_service` (MO-LAI-TARGET-SERVICE)
packet_id: wp1422
revision: 1

Trạng thái: đặc tả cho Packet #1422 thuộc Mission #1172. Chạm mã cổng lifecycle nên thuộc **E5**: chủ kho duyệt băm đặc tả này và tự audit exact-H (`human_exact_head_audit.v1`). Đo ở PR0 #1166 g4 (19/11/2026); chi tiết ở #1422 và https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-7004832203 .

## Vấn đề

`cmd_mo_lai` trong `.claude/dev/packet_loop.py` (master `d89e000`) luôn kiểm biên nhận bằng `_du_dieu_kien_approve` (vị từ ADR-0054). Ở lane target WP1174 có executor `claude` và reviewer `codex` với `execution_surface: codex_service` (cặp khác họ), `_1174_native_review_assurance` trả `assurance_target` của lease (`human_audited`). Vị từ vì thế đòi biên nhận khai provider reviewer `codex` **và** assurance `human_audited`, trong khi `ops/bien_nhan_v2.py::_muc_cam_theo_provider` cấm mọi provider mô hình khai `human_audited`. Không biên nhận nào thoả cả hai, nên `mo-lai ci-do` không bao giờ qua được ở lane này: PR0 g4 phải vòng sang g5 bằng `adopt-state`.

`record-review` ở cùng lane đã có đường riêng (`_1174_review`, nhánh `service`): reviewer `codex_service` nộp biên nhận advisory `wp1174_service_advisory.v1`, so khớp đóng khoá với state, không qua vị từ ADR-0054.

## Hợp đồng

1. **Phạm vi đường mới — đúng một lane.** `cmd_mo_lai` dùng đường advisory khi và chỉ khi cả bốn điều kiện cùng đúng:
   - đang chạy trong giao dịch target WP1174 (`_1174_TRANSACTION` khác None, admission khớp target theo đúng phép `_1174_target_matches` mà `_1174_review` dùng);
   - `st["reviewer_identity"]["execution_surface"] == "codex_service"`;
   - `a.nguyen_nhan == "ci-do"`;
   - state đang `approved_pending` (đầu vào hiện có của `ci-do`).
   Mọi trường hợp khác (source/legacy, ngoài giao dịch target, reviewer không phải service, `--nguyen-nhan connector`, `running` mở lại) đi đường hiện có **không đổi một byte hành vi**.
2. **Biên nhận advisory mở lại.** Hàm module-level mới `_1174_advisory_reopen_receipt(st, a, h) -> dict` đọc `a.bien_nhan` (thiếu/không đọc được/không phải JSON ⇒ `_die(RC_BIEN_NHAN, ...)`, không đoán). Nó đòi bản ghi là dict có **đúng** tập khoá `{schema, head, identity, verdict, finding_ids, assurance, bang_lop}` và:
   - `schema == "wp1174_service_advisory.v1"`, `assurance == "advisory_review"`, `verdict == "changes_requested"`;
   - `head == h` (= `pending_sha`), `identity == st["reviewer_identity"]` (so cả dict);
   - `finding_ids == sorted(set(a.finding_id))`, mỗi phần tử khớp `SLUG_RE`, không rỗng;
   - `bang_lop` là list khác rỗng; mỗi phần tử là dict có đúng khoá `{slug, hang, check_refs}`, `slug` khớp `SLUG_RE`, `hang` thuộc `HANG_LOP`; tập `slug` không lặp và **bằng** tập `finding_ids`.
   Trả `{"tep": str(a.bien_nhan), "sha256": sha256(byte thô), "p3": [...], "lop": bang_lop}` — cùng hình dạng `_du_dieu_kien_approve` trả, để phần còn lại của `cmd_mo_lai` (kiểm `check_refs`, `_doc_connector`, `_kiem_ci` với `CI_DO_THAT`, bộ đếm same-failure, `_xet_dung`, ghi state) chạy **không đổi**. Vi phạm bất kỳ ⇒ `_die(RC_BIEN_NHAN, ...)` trước mọi ghi.
3. **Không có đường nào yếu hơn.** CI đỏ thật trên head vẫn được đo lại bằng `_kiem_ci` (readback run/job/check-run, `CI_DO_THAT`); connector vẫn phải không còn P0–P2 trên head (`ci-do`); `check_refs` vẫn phải đúng dạng, không lặp. Đường mới chỉ thay **lớp kiểm biên nhận phân loại**, không thay lớp đo CI. Không đổi `_du_dieu_kien_approve`, `ops/bien_nhan_v2.py`, `record-review`, `accept`, `chu-kho-duyet`, `adopt-state` hay schema state.
4. **Ca kiểm bắt buộc** (trong `.claude/dev/packet_loop_test.py`; ca dương đòi kết quả dương cụ thể; ca âm đòi state KHÔNG đổi từng byte so với ảnh trước bước bị từ chối):
   a. **Dương — lane khác họ service:** fixture target như các ca `_1174` hiện có nhưng executor `claude`/`claude_code`/`machine/local`, reviewer `codex`/`codex_service`/`machine`, lease `assurance_target: human_audited`, state `approved_pending`; `mo-lai --nguyen-nhan ci-do` với biên nhận advisory hợp lệ + CI đỏ thật ⇒ rc0, `state == "running"`, `mo_lai_tu == {"nguyen_nhan":"ci-do","generation":...,"sha":h}`, `finding_counts[slug] == 1`.
   b. **Âm — mỗi ca khác đúng một thứ so với (a):** `schema` khác; `assurance` khác; `verdict` khác (`approve`); `head` khác; `identity` khác (một trường); thừa một khoá; thiếu một khoá; `finding_ids` lệch `--finding-id`; tập slug của `bang_lop` lệch `finding_ids`; `hang` ngoài `HANG_LOP`; `bang_lop` rỗng; tệp không phải JSON; check-run không đỏ thật (đường `_kiem_ci` vẫn chặn).
   c. **Không hồi quy:** ca `mo-lai` cùng họ hiện có (`native_identity`, biên nhận v2 `_bn812`) giữ nguyên ID và xanh; `--nguyen-nhan connector` ở lane khác họ service vẫn đi đường cũ (biên nhận advisory bị từ chối như trước); lane reviewer không phải service vẫn đi đường cũ.
5. **Mutant bắt buộc** — mỗi mutant làm ca đích ĐỎ đúng assertion của chính ca ấy, và ca đích XANH trên mã chưa đột biến:
   - `m1422_head_unchecked` (bỏ so `head`) ⇒ đích: 4b `head`.
   - `m1422_identity_unchecked` (bỏ so `identity`) ⇒ đích: 4b `identity`.
   - `m1422_slugs_unbound` (bỏ phép bằng giữa slug `bang_lop` và `finding_ids`) ⇒ đích: 4b slug lệch.
   - `m1422_connector_widened` (cho `connector` vào đường mới) ⇒ đích: 4c connector.
   - `m1422_any_surface` (bỏ điều kiện `codex_service`) ⇒ đích: 4c reviewer không phải service.
   Đăng ký mọi ca mới vào inventory; giữ nhất quán literal đếm.
6. **Không hồi quy chung:** mọi ca `wp1174_*`, `r812*`, `#813` hiện có giữ ID và xanh; kiểm kê anchor product mutant khớp đúng một lần; Ruff F delta so base = 0.

## Write set

- `.claude/dev/packet_loop.py`
- `.claude/dev/packet_loop_test.py`

## Quy trình và quyền

- Executor: Claude Code (Fable 5.2). Reviewer: Codex service (gpt-6-astra), phiên độc lập, chỉ đọc. Trần: attempts 3, review 3, lời gọi Codex 3.
- E5: chủ kho duyệt băm đặc tả này trước khi cấp lease; chủ kho tự audit exact-H trước merge; điều phối không ký thay. Merge do chủ kho bấm. Không Windows CI.
- Ngoài phạm vi: sửa vị từ ADR-0054, `bien_nhan_v2`, đường `connector`, PR1–PR8, installation, LIVE.
