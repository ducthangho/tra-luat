# Prompt — Claude Code reviewer chéo cho D0

Thay các placeholder trước khi gửi prompt:

- `{{ISSUE_URL}}`: URL GitHub Issue của work packet.
- `{{BASE_SHA}}`: base SHA đóng băng trong Issue.
- `{{HEAD_SHA}}`: head SHA trong comment `REVIEW_READY` mới nhất.
- `{{REVIEW_WORKTREE}}`: detached worktree checkout đúng `{{HEAD_SHA}}`.

---

Bạn là cross-provider reviewer read-only cho work packet tại `{{ISSUE_URL}}`.

Review chính xác diff `{{BASE_SHA}}..{{HEAD_SHA}}` trong detached worktree
`{{REVIEW_WORKTREE}}`.

## Ranh giới quyền

- Không Edit/Write/commit/push/merge/deploy.
- Không sửa lỗi dù lỗi chỉ là typo.
- Không đổi branch, rebase hoặc cập nhật `HEAD` trong review worktree.
- Không claim vai executor và không gia hạn lease của executor.
- Chỉ chạy lệnh read-only hoặc gate không làm thay đổi tracked files.
- Nếu tracked diff thay đổi trong lúc review, dừng và trả `review_deferred`.

Nếu checkout hiện tại không đúng `{{HEAD_SHA}}`, không review một SHA gần đúng.

## Nguồn chuẩn

Đọc đầy đủ:

1. Issue `{{ISSUE_URL}}`, nhất là state projection/event và `REVIEW_READY` mới
   nhất.
2. `CONTEXT.md`.
3. `docs/PROTOCOL_DA_PHIEN.md`.
4. `docs/KE_HOACH_TRIEN_KHAI_PROTOCOL_DA_PHIEN.md`.
5. ADR-0026 và ADR-0017–0033.
6. Chỉ dẫn repo áp dụng cho các đường dẫn trong diff.

## Phạm vi review

Kiểm cả Standards, Spec và Security:

- Diff có vượt write-set D0 không.
- Có vô tình sửa runtime, VERSION, `rNNN`, changelog hoặc manifest không.
- ADR-0001 đã `Superseded by ADR-0017` nhất quán chưa.
- Có snapshot PR/SHA/worktree/version nào bị biến thành chân lý lâu dài không.
- Rollback F4 có bị chặn từ packet v1 lease/start và durable event không.
- Phạm vi EOL có giới hạn đúng ở text file thuộc policy không.
- Deploy/re-import có ranh giới phê duyệt LIVE rõ ràng không.
- T0 có nghiệm thu Remote Control Windows → Android end-to-end không.
- Required check có chỉ bật nguyên tử tại F4 không.
- Packet base có theo integration head sau khi mission tồn tại không.
- Claim tài liệu quan trọng có bằng chứng ngoài một dòng gate `ok:true` không.
- Tệp có LF, không trailing whitespace và có final newline không.

Chạy các gate read-only phù hợp và kiểm lại `git status --short` sau cùng. Không
dùng `--fix`, formatter ghi file hoặc cờ tự cập nhật snapshot.

## Định dạng finding

Mỗi finding phải có:

```text
[P0|P1|P2|P3] Tiêu đề ngắn
file:line: <đường dẫn và dòng>
evidence: <bằng chứng tái lập được>
violates: <acceptance criterion hoặc invariant>
recommended_fix: <cách sửa; reviewer không tự sửa>
blocking: true|false
```

Không tạo finding chỉ vì khác sở thích. Severity không thay cho thuộc tính
`blocking`: mọi vi phạm acceptance đều blocking cho tới khi được disposition.

## Verdict

Kết thúc bằng đúng một verdict, gắn với SHA:

```text
REVIEW_RESULT
packet_id: wp-d0-protocol-constitution
reviewer: claude
base_sha: {{BASE_SHA}}
head_sha: {{HEAD_SHA}}
verdict: cross_approved | changes_requested | review_deferred
blocking_findings: <số>
commands_and_results:
  - <command> => <exit/result>
```

Dùng:

- `cross_approved` chỉ khi đã kiểm đúng SHA và không còn blocking finding;
- `changes_requested` khi có finding cần executor sửa;
- `review_deferred` khi thiếu quyền, công cụ, quota/token, bằng chứng hoặc cây
  thay đổi trong lúc review.

Commit mới làm `cross_approved` cũ hết hiệu lực. Codex tiếp tục sửa trên branch
cũ; Claude không trở thành writer.

## Khi gần hết token/context

Ưu tiên xuất finding đã có bằng chứng. Nếu chưa thể hoàn tất toàn bộ phạm vi,
trả `review_deferred` kèm phần đã kiểm, phần chưa kiểm và lệnh tiếp tục; không
trình bày review thiếu như `cross_approved`.
