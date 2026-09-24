# Kế hoạch thi công đa provider — tra-luat

> **Trạng thái:** Active transition plan
>
> Tài liệu này không cấp authority. Authority nằm trong Packet Spec,
> GitHub facts và verified receipts.
>
> Các provider/bề mặt hiện được sử dụng:
>
> - Google Antigravity;
> - ChatGPT Pro qua Web;
> - Claude Code và Codex khi quota khả dụng;
> - Human Auditor.

## 1. Mục tiêu

Duy trì tiến độ phát triển khi một hoặc nhiều provider không khả dụng, nhưng:

- không tạo orchestrator mới;
- không hạ chuẩn exact-SHA review;
- không khai sai provider hoặc transport;
- không cho output model tự tạo quyền ghi;
- không làm trạng thái động trôi vào tài liệu kế hoạch tĩnh;
- không dùng provider tạm thời để tự hợp thức hóa thay đổi sensitive.

## 2. Nhận dạng provider và execution surface

| Công cụ/bề mặt | Provider | Execution surface | Transport |
|---|---|---|---|
| Google Antigravity | `google_antigravity` | `antigravity` | machine/local |
| ChatGPT Pro Web | `openai_chatgpt` | `chatgpt_web` | `human_mediated` |
| Claude Code | `anthropic_claude` | `claude_code` | machine/local |
| Codex CLI | `openai_codex` | `codex_cli` | machine |
| Codex Desktop | `openai_codex` | `codex_desktop` | machine |
| Codex service (GitHub App / cloud) | `openai_codex` | `codex_service` | machine |
| Human Auditor | `human` | `manual_audit` | human |

Tên công cụ không tự quyết định assurance.
Codex Desktop không được khai thành CLI. Bề mặt Desktop không chứng minh model/effort
đã phục vụ hoặc tính độc lập của session; khai giới hạn đo được và giữ mức advisory
khi chưa đủ evidence theo protocol.

Tên lịch sử “Codex service” có tên máy `codex_service` từ wp461 r3 (Mission
[#470](https://github.com/ducthangho/tra-luat/issues/470) Q1; nợ mở ở
[#461](https://github.com/ducthangho/tra-luat/issues/461) theo mục `no_khai_ra` của
[biên nhận review #460 lượt 9](reviews/pr460-bien-nhan-v2-review-9-gpt6astra-verdict.receipt.yaml)).
`codex_service` là mọi đường chạy Codex không qua lệnh `codex` (CLI) và không qua Codex
Desktop — gồm GitHub App `chatgpt-codex-connector[bot]` review trên PR và Codex cloud nói
chung. Nó không chứng minh model/effort đã phục vụ hay tính độc lập của phiên; receipt phải
khai `KHONG_do_duoc` cho phần không đo được. Các biên nhận lịch sử khai `codex_cli` giữ
nguyên (Q2 #470): chúng đi qua `codex exec`, không được ánh xạ lại.

## 3. Vai trò ChatGPT Pro Web

ChatGPT Pro Web được dùng theo hai chế độ.

### 3.1 Advisory Reviewer

ChatGPT nhận một review bundle đóng băng và trả review note có cấu trúc. Nó không được xem là authoritative reviewer vì local controller không thể machine-verify model identity, session identity hoặc toàn bộ transport.

### 3.2 Patch Planner

ChatGPT có thể sinh:

- unified diff;
- patch plan;
- test plan;
- remediation plan.

AG hoặc local controller phải:

1. kiểm write set;
2. kiểm path traversal và symlink;
3. áp patch;
4. chạy test;
5. đọc lại diff;
6. commit và push.

ChatGPT Web không phải Executor-of-record.

## 4. Review Class

Dùng Review Class canonical:

```text
routine
systemic
sensitive
```

### Routine

Có thể land khi:

- AG Executor hoặc human-controlled patch application;
- AG Reviewer độc lập hoặc reviewer theo protocol;
- ChatGPT advisory review tùy chọn;
- exact SHA hợp lệ;
- required CI đầy đủ;
- human readback.

ChatGPT advisory review không thay thế các điều kiện khác.

### Systemic

- AG–AG review có thể dùng tạm thời nhưng bắt buộc review debt bởi Claude, Codex hoặc Human Auditor.
- ChatGPT advisory review là lớp soi bổ sung, không tự xóa review debt.

### Sensitive

Không land bằng AG–AG và ChatGPT advisory alone.

Cần:

- cross-provider review được runtime/receipt công nhận; hoặc
- Human Audit exact SHA có evidence bền.

## 5. Review bundle

Review bundle phải gắn với một exact head và tree.

Nội dung tối thiểu:

```text
00_BUNDLE_MANIFEST.json
01_PACKET_SPEC.md
02_REVIEW_INSTRUCTIONS.md
03_DIFF.patch.txt
04_CHANGED_PATHS.txt
05_NUMSTAT.txt
06_TEST_EVIDENCE.json
07_REVIEW_NOTE_TEMPLATE.yaml
```

`00_BUNDLE_MANIFEST.json` phải chứa:

```json
{
  "schema": "chatgpt_review_bundle.v1",
  "bundle_id": "<stable-id>",
  "packet_id": "<packet-id>",
  "base_sha": "<40-char-git-oid>",
  "head_sha": "<40-char-git-oid>",
  "tree_sha": "<40-char-tree-oid>",
  "write_set": [],
  "review_class": "routine|systemic|sensitive",
  "files": [
    {
      "path": "01_PACKET_SPEC.md",
      "sha256": "<hash>",
      "size": 0
    }
  ],
  "created_at_utc": "<iso8601>",
  "builder_version": "<version>"
}
```

Mọi file phải được hash. Bundle thay một byte phải sinh bundle hash mới.

## 6. Quy trình review ChatGPT

1. Local builder tạo bundle từ clean worktree và exact SHA.
2. Human tải các file bundle lên một conversation ChatGPT mới.
3. Không tái sử dụng conversation Executor.
4. ChatGPT chỉ review dữ liệu trong bundle.
5. ChatGPT trả đúng một review note theo template.
6. Human lưu note về local.
7. Local validator:
   - parse note;
   - validate schema;
   - kiểm full SHA;
   - kiểm bundle hash;
   - kiểm verdict/finding ID;
   - so local head và tùy chọn GitHub PR head;
   - sinh validation receipt.
8. Chỉ note có receipt hợp lệ mới được đăng lên PR.
9. Note vẫn mang assurance `advisory_review`.

## 7. Quy trình Patch Planner

1. Tạo Packet Spec và patch request bundle.
2. ChatGPT sinh patch hoặc patch plan.
3. Local controller kiểm:
   - path thuộc write set;
   - không path traversal;
   - không symlink escape;
   - không binary/secret không được phép.
4. AG hoặc human áp patch.
5. Test, review và CI chạy như Packet bình thường.
6. ChatGPT không được khai là Executor-of-record.

## 8. Review note

Review note dùng format:

```yaml
format: temporary_chatgpt_review_note.v0
provider: openai_chatgpt
execution_surface: chatgpt_web
transport: human_mediated
account_plan: pro
bundle_id: <bundle-id>
bundle_sha256: <sha256>
reviewed_sha: <40-char-git-oid>
reviewed_tree: <40-char-tree-oid>
verdict: approve | changes_requested | blocked
review_axes:
  - spec
  - standards_security
findings:
  - finding_id: <stable-kebab-slug>
    severity: P0 | P1 | P2 | P3
    path: <repo-relative-path-or-null>
    line: <integer-or-null>
    evidence: <text>
    recommendation: <text>
tests:
  independently_run: false
  evidence_reviewed: []
limitations:
  - human_mediated_transport
  - model_identity_not_machine_verified
  - tests_not_run_by_chatgpt
assurance: advisory_review
```

ChatGPT không được tự đặt `machine_validated: true`.

## 9. Validation receipt

Local validator sinh:

```yaml
format: chatgpt_review_validation_receipt.v1
review_note_sha256: <sha256>
bundle_id: <bundle-id>
bundle_sha256: <sha256>
schema_valid: true
bundle_valid: true
reviewed_sha_matches_bundle: true
reviewed_tree_matches_bundle: true
local_head_matches: true
github_pr_head_matches: true | false | unavailable
provider_claim_valid: true
transport_claim_valid: true
finding_ids_valid: true
model_identity_verified: false
session_identity_verified: false
authoritative_assurance: review_deferred
advisory_assurance: advisory_review
validator_version: <version>
validated_at_utc: <iso8601>
```

Receipt không được nâng review thành `cross_approved`.

## 10. Non-convergence

> **ĐÃ CHỐT (quyết định của người giữ kho).** Điều khoản này là **trần review CANON
> của cả kho**, áp cho mọi lane và mọi provider — không riêng luồng ChatGPT. Nó thay
> thế trần của `ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md` §8 (2 lời gọi *hoặc* ba vòng
> code/review tổng). Khi hai tài liệu lệch nhau, **điều khoản này thắng**.

Mỗi PR tối đa:

`2 model review rounds`

**Đếm theo VÒNG, không theo LỜI GỌI.** Hai đại lượng này khác nhau và đã bị lẫn một
lần: một vòng có thể tốn nhiều lời gọi (reviewer bị void vì quota/hạ tầng rồi gọi lại
vẫn là **một** vòng). Ánh xạ sang bộ đếm trong `.claude/dev/packet_loop.py`:

| đại lượng | bộ đếm | trạng thái cưỡng chế |
|---|---|---|
| **vòng** — thứ điều khoản này chốt | `review_rounds_used` | **CHƯA CÓ TRẦN** — xem nợ bên dưới |
| lời gọi — trục chi phí, khác trục này | `codex_review_calls_used` / `..._limit` | có trần (mặc định 2), cạn thì `checkpoint` + `RC_TRAN` |

Một **vòng** = một lượt reviewer trả verdict trên một exact head, cộng lượt executor
sửa theo verdict đó. Lượt reviewer bị `void` vì lý do thuộc `LY_DO_VOID`
(quota · rate_limit · infrastructure · permission) **không tính** vào trần vòng.

**NỢ CƯỠNG CHẾ — trần này hiện là TỰ NGUYỆN.** Đo được trên
`.claude/dev/packet_loop.py`: `review_rounds_used` chỉ được khởi tạo và **tăng**, không
có `review_rounds_limit` và không nơi nào đọc nó để chặn. Bằng chứng lịch sử: packet
`W0-R1` đã chạy **4 vòng** review — vượt cả trần 3 vòng của kế hoạch cũ lẫn trần 2 vòng
ở đây — và không có gì dừng nó lại. Cho tới khi trần được dệt vào đường bắt buộc,
**đừng đọc con số này như một cổng**; nó là kỷ luật của người vận hành.

Sau vòng hai chưa approve:

- dừng;
- human checkpoint;
- Stable Slice nếu độc lập;
- Remediation Packet;
- revision Packet/Mission;
- hoặc chờ provider khác.

Không đổi conversation, prompt hoặc tên Packet để lách review budget.

## 10b. Master drift sau khi gate đã xanh — merge thẳng

> **ĐÃ CHỐT (quyết định của người giữ kho).** Luật nằm ở `docs/PROTOCOL_DA_PHIEN.md`
> §5.1. Mục này **không chép lại** — chỉ nêu điều kiện áp và điều cần nhớ.

Áp khi đủ cả ba: reviewer đã `approve`; required gate đã xanh trên **exact head của
nhánh**; và thứ đổi kể từ đó là **master**, không phải head nhánh. Khi ấy **không chạy
lại gate** — merge thẳng, sạch là xong.

Hai điều dễ đọc sai:

1. Điều này **không** hạ chuẩn exact-SHA. Head nhánh không đổi, nên review và gate cũ
   vẫn neo đúng thứ chúng đã đo. Quy tắc `head đổi ⇒ stale` nói về head NHÁNH.
2. "Nghi ngờ" **không phải cảm tính** — §5.1 có danh sách **sáu kích hoạt đo được**.
   Trúng bất kỳ dòng nào ⇒ chạy lại gate SAU merge. Đọc danh sách ở đó, đừng đoán.

## 10c. Reviewer bắt buộc kèm gợi ý cách vá

> **ĐÃ CHỐT (quyết định của người giữ kho).** Luật nằm ở `docs/PROTOCOL_DA_PHIEN.md`,
> ngay dưới verdict contract. Nâng từ một yêu cầu ad-hoc trong prompt lease lượt 5 của
> `#150` lên thành luật thường trực, áp mọi reviewer và mọi provider.

Bốn phần bắt buộc cho **mỗi** finding: vá ở đâu · vá thế nào · ca test khoá nó · bản vá
này có thể đẻ ra gì. Chi tiết và lý do từng phần: xem protocol.

**Ánh xạ sang schema của tài liệu này:** trường `recommendation` trong
`temporary_chatgpt_review_note.v0` (§8) là **nơi chứa bốn phần đó**, không phải một câu
khuyến nghị trần. Note có finding mà `recommendation` rỗng, hoặc chỉ nhắc lại chính
finding, là note **chưa hoàn chỉnh** — validator trả lại, không đăng lên PR.

## 11. Review debt

Review debt được tính từ:

- Review Class;
- authoritative assurance;
- exact SHA validity;
- identity evidence;
- required CI;
- head staleness.

ChatGPT advisory review:

- không tự tạo debt;
- không tự xóa debt;
- chỉ bổ sung evidence để reviewer/maintainer quyết định nhanh hơn.

## 12. Trạng thái động

Không lưu thủ công trong file này:

- quota hiện tại;
- PR đang mở;
- CI xanh/đỏ;
- head SHA hiện hành;
- Packet đã merge hay chưa.

Đọc các trạng thái này từ GitHub facts hoặc `STATUS.generated`.

## 13. Stop conditions

Dừng khi:

- bundle không tái lập được;
- bundle hash sai;
- reviewed SHA không đủ 40 ký tự;
- reviewed SHA không khớp current head;
- ChatGPT note có field ngoài contract nguy hiểm;
- ChatGPT khai đã chạy test;
- note chứa secret hoặc nội dung ngoài bundle;
- required CI skipped/missing;
- cần ghi ngoài write set;
- xuất hiện security, credential, workflow hoặc LIVE path;
- review budget hết.
