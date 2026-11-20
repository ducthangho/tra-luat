# Bàn giao điều phối Mission #1172: PR1 (#1448) và các bước sau

Bàn giao từ phiên điều phối Claude Code `session_015GtxrYrYrjwBfHspZtYwc1`, ngày 2026-11-20. Chủ kho đã đồng ý chuyển trọn vai điều phối sang phiên mới. **Phiên cũ dừng hẳn sau bàn giao này. Chỉ một phiên được giữ vai điều phối.**

## 1. Quy tắc thường trực (giữ nguyên, không tự nới)
- Trả lời chủ kho bằng tiếng Việt, hỏi ít nhất có thể, và chạy tới khi việc land.
- Giữ nguyên lịch sử, bộ đếm và số nền. Không reset, không hoàn lại lượt đã dùng. Lượt gọi model bị mất do hạ tầng vẫn tính là đã dùng và ghi `lost_infrastructure`.
- Uỷ quyền rộng của chủ kho (#1172 comment `6916538696`) cho phép điều phối:
  - cấp, gia hạn và rút lease;
  - nâng trần khi chủ kho đã quyết;
  - đăng comment;
  - đăng dòng miễn K6/K7 theo tiền lệ.
  Bản ghi audit uỷ quyền mang nhãn `owner_delegated_audit`, không bao giờ `human_audited`.
- Executor là Fable 5.2 (`claude-fable-5-2`), gọi qua Agent tool với `model: fable`, `subagent_type: general-purpose`, `isolation: worktree`. Reviewer là Codex `gpt-6-astra`, `model_reasoning_effort=xhigh`, gọi qua `.claude/dev/launcher.py run`. Kiểm model đã phục vụ ở `run.json` → `model_phuc_vu`.
- Không chạy Windows CI. Sau mỗi lần merge, huỷ lượt Windows nếu có. Chủ kho tự bấm merge. Chủ kho tự audit exact-H; điều phối không ký thay.
- Không bao giờ viết nguyên văn dấu bỏ-qua-CI trong commit message. Đặt `core.abbrev 7` khi chạy gate.
- Không đọc hay in giá trị secret. `TL_MASTER_KEY` không đi qua phiên cloud ở dạng đọc được. Chưa xoá doc key cũ, hai tệp `NEW-MASTER-KEY.txt` và `rekey-backup`: chủ kho chưa chắc đã chuyển hết.
- Mọi Mission revision mới hoặc spec mới cần **chủ kho duyệt băm** trước khi cài hoặc cấp lease. Bản revision chỉ ghi sổ thì không cần duyệt.

## 2. Trạng thái tại lúc bàn giao
- **Mission đang hiệu lực: r82.** https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-7032189767, Plan SHA256 `24d089b02c3c6b7fb734b417de4be5a46577e1501ca63c7d848a9f3cdabbbc20`. JSON nằm ở `ops/specs/wp1448-r2/mission-r82.json`.
- **Kế hoạch nguồn r3** (thay cho r2 đã mất, KHÔNG phải bản gốc): `ops/specs/wp1172-source-plan-r3/KE_HOACH_NGUON_R3.md`, sha256 `2e9fb13f1ab3f299c2d2dc1e5a6e407ff0aadb8aee1f6ffd00d88fc02b146f89`, nhánh `ops/wp1172-plan-r3` @ `c032656`. Cài ở r81. Có một đính chính: khoảng tiết kiệm khi có PR6 là 3,4–5,6 triệu s, không phải 3,5. Câu hỏi Q1–Q5 để chủ kho quyết tại packet cần nó: Q1 trước PR3, Q2 trước PR5/PR6, Q3 trước PR2.
- **Số nền** (#1434, đã merge `5e5d2cc`): `ops/specs/wp1434-r3/do/BASELINE.json`, sha256 `6100c8e18907f59b1abbdc44195861cc2310c654ce8dcfa2e74ca4ffa155f54c`.
- **PR1 = Packet #1448**, https://github.com/ducthangho/tra-luat/issues/1448:
  - spec r2 `ops/specs/wp1448-r2/SPEC.md`, sha256 `5014de59a48aad517ae22d1b91a6ae8dc1b382fc4650fdddecffe9cc5927c53e`, nhánh `ops/wp1448-r1`;
  - chủ kho đã duyệt băm spec r2 và r82;
  - review spec lượt 1 (`codex-spec-review-1.json`) ra `changes_requested`; lượt 2 (`codex-spec-review-2.json`, sha256 `9c75efb4…`) ra **approve**, 0 phát hiện;
  - **CHƯA cấp lease, CHƯA giao executor.** Theo r82, phiên mới được cấp lease và giao executor ngay, không cần hỏi lại.
- **Trần của r82 cho PR1:**

  | Khoản | Trần | Đã dùng |
  |---|---|---|
  | review spec | 1 | 1 |
  | lượt thực thi | 3 | 0 |
  | Codex review mã | 3 | 0 |
  | lượt CI PR Ubuntu | 3 | 0 |
  | `ci-dot-bien-du.yml` trên H (K7) | 1 | 0 |
  | connector | 2 | 0 |
  | CI rerun | 1 | 0 |
  | Windows | 0 | — |
  | tổng lượt gọi model | 9 | — |

  Còn lỗi P0–P2 sau khi hết trần thì dừng và hỏi chủ kho.
- **Hạn chót:** ngoại lệ routing C1 hết hạn 2026-12-24T18:53Z.

## 3. Việc còn treo (không thuộc PR1)
- `/case2.log` (76 byte, ở gốc filesystem của container cũ): chủ kho cho xoá, nhưng bộ chặn an toàn từ chối. Container cũ sẽ bị thu hồi nên bỏ qua được.
- Thư mục enrollment PR0 trên Desktop (`/home/tlcanary/wp1166-r4-g4-20261119`): giữ làm bằng chứng.

## 4. Trình tự cho PR1 (đã chạy thật ở #1434, #1422; làm đúng thứ tự)
1. **Lease.** `ops/leases/wp1448-r2-g1-claude.yaml` trên nhánh `ops/wp1448-r1`. Đây là JSON trong tệp `.yaml`; khuôn theo `ops/leases/wp1434-r3-g1-claude.yaml` trên nhánh `ops/wp1434-r1`. Các trường chính:
   - `mission_revision: 82`, `revision: 2`, `generation: 1`;
   - `risk`, `review_class` và `effective_review_class` đều là `sensitive` (cổng tính ra `sensitive`);
   - `spec_ref`, `spec_hash`, cùng prompt executor và băm của nó;
   - `write_set` theo spec, `limits` theo r82;
   - `base_sha` = master hiện tại.

   Trước khi cấp: chạy `python3 ops/lease_publish.py ai-dang-giu <đường dẫn>` cho từng tệp trong write set, sau khi `git branch -f` mọi nhánh cục bộ cho khớp origin; nếu không, lệnh ra `rc12`. Rồi chạy `python3 ops/lease_publish.py check <lease>`. Đẩy lên và kiểm workflow `ops — đăng lease bằng git` đã chạy.
2. **Executor.** Fable 5.2 làm một commit cục bộ trên `agent/wp1448-r2-g1-claude` từ master, không push.
3. **Codex review mã** trên một clone độc lập, không dùng worktree (launcher chặn worktree với `CHAN [14]`):
   - `launcher.py run --workspace <clone> --expected-head <H> --require-clean --prompt-file … --expected-prompt-sha256 … -- $(which codex) exec -m gpt-6-astra -c model_reasoning_effort=xhigh -s workspace-write --skip-git-repo-check -o <last.txt> "$(cat prompt)"`;
   - đặt `REVIEW_OUT` ra tệp JSON;
   - nhớ ADR-0052: một lượt bị cắt vẫn tính là một lượt gọi.
4. **Bài học K4: chủ kho phải audit TRƯỚC lần đẩy đầu của H.**
   - Đẩy một commit bootstrap (commit trung gian hoặc vòng trước) lên `agent/…`, rồi mở PR **nháp** để có số PR.
   - Đưa chủ kho mẫu `human_exact_head_audit.v1`, gồm các trường `packet`, `revision`, `generation`, `pr`, `reviewed_sha`, `reviewed_tree`, `spec_sha256`, `verdict: approve`, `assurance: human_audited`, `review_axes: [spec, standards_security]`, `open_findings: []`, `audit_source`.
   - Chủ kho đăng comment trên PR, rồi sửa `audit_source` thành link của chính comment ấy.
   - Kiểm qua API: OWNER, đủ các trường, `updated_at` sớm hơn lượt CI đầu tiên của H. Sau đó mới đẩy H.
   - H đổi thì cần audit mới.
5. **Bài học #1439: trước khi đẩy H, merge hoặc rebase nhánh lên master mới nhất.** Bộ phân loại so với master hiện tại, nên master trôi có thể kéo PR sang làn `day_du`. PR1 vốn là `day_du` vì đụng mã, nhưng vẫn phải cập nhật.
6. **Connector.** Gọi bằng comment `@codex review` kèm head. Kết luận sạch là dòng `Reviewed commit:` của đúng H. Lưu ý: chuyển PR nháp sang sẵn sàng sẽ tự sinh một lượt connector, tính vào trần; nên chuyển sang sẵn sàng sau khi đã có connector sạch, hoặc ghi lại lượt ấy.
7. **K7.** Một lượt `ci-dot-bien-du.yml` `workflow_dispatch` trên ref của H, phải `success`. Truyền `--dot-bien-du-runs/--dot-bien-du-jobs` cho kiem-merge.
   **K6.** Dòng miễn `windows: <H> mien` do điều phối đăng theo tiền lệ #1427 (comment 7015889026) và #1439 (comment 7029699343).
8. **kiem-merge.** Chạy `python3 .claude/dev/packet_loop.py kiem-merge` trên kho không shallow, với `--human-audit-comment` (JSON comment lấy qua REST), `--human-remote-run` (lượt CI sớm nhất trên H), `--workflow-runs/--workflow-jobs/--check-runs/--connector`, `--chu-kho-comment` (miễn), `--lease`, `--spec`. Phải ra `rc=0`. Khuôn đầu vào nằm trong lịch sử #1439.
9. **Sau merge.**
   - Huỷ lượt Windows nếu có, theo dõi gate master.
   - Ghi M8 lên #1448 với `landed: false`; §10.2.2 không đo được vì GraphQL trả 403 từ phiên cloud.
   - Rút hạn lease: sửa `lease_until`/`lease_expires_at_utc` thành khoảng +4 phút, kèm khối `thu_hoi_bang_rut_han`.
   - Cài một Mission revision chỉ ghi sổ.
10. **Cài Mission revision.**
    - Comment tiêu đề `## Mission #1172 — Installed revision N`, chứa `Plan SHA256` là sha256 của khối JSON, gồm cả `\n` cuối.
    - Đăng bằng REST POST qua `json.dumps`, không qua MCP, vì kế hoạch có dấu chéo ngược.
    - Đọc lại và so băm.
    - JSON viết bằng `json.dumps(…, ensure_ascii=False, indent=2) + "\n"`.

## 5. Phụ thuộc vào container cũ
- **Ảnh chụp thô của #1434** (khoảng 576 MB) chỉ có ở container cũ. Nghiệm thu PR1 mục 5 đòi tái lập các khoá `[B: …]` trên ảnh chụp ấy.
  - Phiên mới tự thu lại: `python ops/specs/wp1434-r3/do/thu_thap.py --thu --ra <thư mục ngoài kho>`, với cùng T0 `2026-10-21T01:16:24Z` và T1 `2026-11-20T01:16:24Z`, rồi chạy bước `--chi-su-kien-kho`.
  - So với `ops/specs/wp1434-r3/do/COHORT.json`. Nguồn nào đã hết hạn hoặc lệch thì ghi rõ trong nghiệm thu; không làm giả.
- Clone reviewer cũ và các tệp nháp không cần mang sang.

## 6. Ngoài phạm vi PR1
- Mọi thay đổi quyết định cổng (PR2–PR8).
- Nới M9, lấy mẫu mutant.
- Route production, LIVE, đóng Mission.

## 7. Prompt để dán vào phiên mới
Xem `ops/specs/wp1448-r2/HANDOFF-PROMPT.txt` trên cùng nhánh.
