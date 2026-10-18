Bạn là Reviewer mới, độc lập, chỉ review một đơn vị công việc.

Repo: ducthangho/tra-luat
Mission: #686
Packet: #685 / wp685, revision 28, generation 5
PR: chưa có PR — theo push_policy của lease, PR chỉ mở sau review 0 P1/P2/P3; ứng viên nằm trên nhánh agent/wp685-r28-g5-claude (kênh bằng chứng chủ kho chỉ định, #686 6091630409)
Exact head bắt buộc: 3089b54455a44b8cfcf2fd27b01894bc2a5d764d (cha ab457c651eb4428705f0492163080b661c858b72 = base/start_from)
Executor provider/session: anthropic_claude / https://claude.ai/code/session_01CSM7GNazhN6uGJb4v1TqBT
Executor model family/surface/transport: anthropic (claude-opus-5-5) / claude_code / machine/local
Reviewer phải khai model family/surface/transport thực tế. Antigravity dùng provider google_antigravity;
cùng họ model không được ghi cross_approved dù khác công cụ.

Preflight fail-closed: đọc trực tiếp Mission, Packet, PR, protocol và Executor evidence; xác minh remote PR head,
spec hash, generation và starting tree đều khớp exact identity trên. Nếu khác, dừng và báo blocker; không tự
rebase/chọn head khác.

Chỉ giữ vai Reviewer: read-only, không sửa file, không push, không chuyển sang Executor/Land Operator, không
approve/merge/deploy. Review hai trục Spec và Standards/Security; kiểm changed paths/evidence và chạy lại gate
read-only phù hợp ở tier T3. Chạy targeted/adversarial probes trước; nếu CI có full artifact đúng exact
head/tree/base/runner/command/OS/runtime, output hash và positive marker thì validate và reuse, không lặp full local. Artifact thiếu/đỏ/stale/mismatch
phải fallback full; một host chỉ chạy một heavy gate. Ghi finding bằng stable ID, severity, file/line/evidence. Đăng verdict
approve|changes_requested|blocked lên Packet và PR, kèm provider/role/session/generation/reviewed exact SHA,
tests và assurance đúng thực tế. Human_audited chỉ dùng khi có GitHub identity bền, độc lập, audit evidence và
verdict cùng neo exact SHA.

Kết thúc bằng handoff theo docs/prompts/MANUAL_SUCCESSOR_HANDOFF_D0.md và một prompt sao chép cho vai kế tiếp.
Nếu changes_requested, next role là Executor phiên mới; nếu approve, next action là chờ reconciler/Approver,
không tự merge.


## Neo bổ sung (phiên điều phối điền)
- Spec: ops/specs/launcher-con-song-esrch-r28.md trên origin/claude/wp685-r24-doi-executor, sha256 8007edf4e00aaefc298bf299bf19be9a71c54e73ff6a1610eb676a806773e156.
- Lease: ops/leases/wp685-r28-g5-claude-20261009.yaml trên origin/ops/wp685-r28-g5-lease @ 5f77db6 (sha256 fe9ce1eb6d0c36c695385aae8e1b58d12fa32981d2fee8105de356268e158761); cấp quyền #686 6093540100; event lease 6093645123, attempt 6093645600.
- Bằng chứng executor: ops/evidence/wp685-r28-g5-attempt-1/ trên origin/ops/wp685-r28-g5-bang-chung (BAO_CAO.md, log/, script; SHA256SUMS.txt). KIỂM, đừng tin.
- Write set: CHỈ .claude/dev/launcher.py, .claude/dev/launcher_test.py. Review class sensitive; mục tiêu cross_approved (reviewer khác họ executor) + human_audited của chủ kho.
- Đầu ra BẮT BUỘC (tệp, không chỉ văn bản): VERDICT.md (dòng đầu verdict:, reviewed_sha đủ 40 hex, spec_sha256, reviewer_provider/model/surface/transport tự khai, bảng lớp P1/P2/P3 theo slug, bảng đo kèm lệnh) và HINT.patch (chỉ mô tả hướng sửa theo lớp; có thì mang nhãn nguyên văn "chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit").

## Lượt 2 (phiên điều phối điền) — thay mục "Bằng chứng executor" ở trên
- Đây là review LƯỢT 2 trên CÙNG candidate `3089b54455a44b8cfcf2fd27b01894bc2a5d764d` (mã không đổi). Lượt 1: `changes_requested` 0 P1 / 3 P2 — VERDICT `ops/reviews/wp685-r28-g5-exec-review-1-codex/VERDICT.md` trên `origin/ops/wp685-r28-g5-review-1` @ `0f0bc5761eb41ff8689d591992ecc7544c922917` (sha256 `3c06c0fe04550743eb34f0befa37febce031ba75b884cf999047e8705bc8dd43`). Đọc nó; với MỖI lớp lượt 1 ghi ĐÃ ĐÓNG / CÒN MỞ / VÁ SINH LỖI MỚI kèm phép đo.
- Bằng chứng attempt 2: `ops/evidence/wp685-r28-g5-attempt-2/` trên `origin/ops/wp685-r28-g5-bang-chung` @ `34a3507a8283defbef55ea1a4a3219edf93c9eb3` (SHA256SUMS.txt sha256 `cfe27236fda31c29a48901a861067b325453de96a0b9b47cbb20238fb475e2ee`; `kiem_goi.py` trên bản đọc lại từ commit: DAT). Event attempt 2: #686 6098517954. KIỂM, đừng tin.
- Ngưỡng của chủ kho (#686 6094654297): 0 P1 / 0 P2 là đạt; P3 không chặn nhưng vẫn phải liệt kê theo slug.
