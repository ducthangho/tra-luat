# Prompt — Codex executor cho D0

Thay các placeholder trước khi gửi prompt:

- `{{ISSUE_URL}}`: URL GitHub Issue của work packet.
- `{{BASE_SHA}}`: SHA cố định ghi trong Issue.
- `{{PACKET_ID}}`: mặc định `wp-d0-protocol-constitution`.
- `{{GENERATION}}`: generation hiện hành.
- `{{BRANCH}}`: branch executor được cấp.
- `{{WORKTREE}}`: worktree sạch của executor.

---

Bạn là executor duy nhất của work packet `{{PACKET_ID}}`, generation
`{{GENERATION}}`, tại `{{ISSUE_URL}}`.

## Nguồn chuẩn

Đọc đầy đủ trước khi sửa:

1. GitHub Issue `{{ISSUE_URL}}`, gồm mọi state/event comment mới nhất.
2. `CONTEXT.md`.
3. `docs/PROTOCOL_DA_PHIEN.md`.
4. `docs/KE_HOACH_TRIEN_KHAI_PROTOCOL_DA_PHIEN.md`.
5. ADR-0026 và ADR-0017–0033.
6. `AGENTS.md` hoặc chỉ dẫn repo tương đương nếu tồn tại.

Issue và protocol quyết định phạm vi. Nếu chúng mâu thuẫn, chuyển `PAUSE`, nêu
bằng chứng và không tự chọn một cách hiểu thuận tiện.

## Preflight và claim

Trước lần ghi đầu tiên:

1. Xác nhận trạng thái packet là `ready_for_claim`, không phải `PAUSE`,
   `leased`, `running`, `reviewing` hoặc trạng thái kết thúc.
2. Fetch remote và xác nhận `{{BASE_SHA}}` vẫn là base được Issue chỉ định.
3. Xác nhận worktree `{{WORKTREE}}` sạch và branch là `{{BRANCH}}`.
4. Khai triển write-set D0 thành danh sách đường dẫn chính xác.
5. Kiểm không có writer/PR đang giữ write-set giao nhau.
6. Comment `CLAIM` vào Issue với packet, generation, executor, base SHA,
   branch, worktree, write-set, thời điểm và lease expiry.

Nếu không kiểm được GitHub hoặc base/write-set đã đổi, dừng ở `PAUSE`; không
giả định trạng thái cũ vẫn đúng và không âm thầm rebase.

## Phạm vi triển khai

Thực hiện đúng D0 docs-only và acceptance criteria trong Issue.

- Chỉ sửa write-set đã claim.
- Không mang tệp bẩn từ worktree khác.
- Không sửa `VERSION`, `CHANGELOG.md`, `SKILL.md`, manifest hoặc runtime.
- Không cấp số `rNNN`/version và không sinh release metadata.
- Không sửa security path ngoài phạm vi.
- Không merge hoặc deploy.
- Không re-import Capabilities.

Đặc biệt kiểm đủ các điểm:

- ADR-0001 chuyển thành `Superseded by ADR-0017` nhất quán.
- PR/SHA/worktree/version chỉ là snapshot có `observed_at`.
- Rollback F4 bị chặn ngay khi có packet v1 lease/start hoặc durable event hậu
  cutover; sau đó chỉ `PAUSE` và fix-forward.
- EOL chỉ nói về text file thuộc policy đang mang CRLF.
- Deploy/re-import luôn cần phê duyệt LIVE rõ ràng.
- T0 nghiệm thu Claude Remote Control Windows → Android end-to-end.
- Required check chỉ bật nguyên tử tại F4.
- Packet sau khi mission tồn tại lấy base từ integration head.

## Kiểm chứng

Chạy các gate phù hợp trên đúng cây sẽ commit, tối thiểu:

- `doc-claims-check --strict`;
- kiểm liên kết và trạng thái ADR;
- `git diff --check`;
- kiểm LF, trailing whitespace và final newline;
- kiểm diff không vượt write-set;
- kiểm không có VERSION/r/manifest/runtime diff.

Không coi một dòng `ok:true` là đủ nếu claim quan trọng chưa được kiểm trực
tiếp. Ghi nguyên lệnh, exit code và kết quả cần thiết.

## Bàn giao review

Khi toàn bộ acceptance criteria đạt:

1. Commit đúng các tệp thuộc packet.
2. Push branch nếu được protocol và quyền hiện hành cho phép.
3. Không merge hoặc deploy.
4. Comment `REVIEW_READY` vào Issue theo mẫu:

```text
REVIEW_READY
packet_id: {{PACKET_ID}}
generation: {{GENERATION}}
executor: codex
base_sha: {{BASE_SHA}}
head_sha: <HEAD_SHA_THỰC>
branch: {{BRANCH}}
changed_files:
  - <path>
commands_and_results:
  - <command> => <exit/result>
residual_risks:
  - <risk hoặc none>
```

Claude chỉ review đúng `head_sha` này. Mọi commit mới làm approval cũ hết hiệu
lực và cần `REVIEW_READY` mới.

## Khi gần hết token/context

Không tự sinh executor thứ hai. Ghi comment `HANDOFF_REQUIRED` gồm packet,
generation, base/head SHA, việc đã làm, việc còn lại, lệnh tiếp tục, blocker và
evidence. Đặt `PAUSE` hoặc `handoff_required`; không nhận là hoàn thành.
