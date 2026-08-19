# Kế hoạch thi công đa provider — tra-luat

> Trạng thái: Active transition plan
>
> Providers hiện xét đến:
>
> - Google Antigravity;
> - OpenAI API qua `llm`;
> - Claude Code;
> - OpenAI Codex;
> - Human Auditor.
>
> Tài liệu này không cấp authority. Authority nằm trong Packet Spec, GitHub
> facts và verified receipts.

## 1. Mục tiêu

Duy trì tiến độ phát triển khi một hoặc nhiều provider không khả dụng, nhưng:

- không tạo orchestrator mới;
- không hạ chuẩn review;
- không khai sai provider;
- không phụ thuộc GUI;
- không cho model tự mở rộng write set;
- không cho semantic/model output tự tạo quyền ghi.

## 2. Nhận dạng provider

| Bề mặt gọi | Provider | Metadata bắt buộc |
|---|---|---|
| Antigravity | `google_antigravity` | model, session, worktree |
| `llm -m <OpenAI model>` | `openai_api` | `llm_cli`, exact model ID |
| Claude Code | `anthropic_claude` | model/session |
| Codex | `openai_codex` | model/session |
| ChatGPT web thủ công | không phải machine provider | human-mediated note |

`llm` không phải provider. Việc dùng `llm` để gọi Gemini hoặc Claude làm thay đổi provider dù command vẫn bắt đầu bằng `llm`.

## 3. Review Class

Dùng class canonical:

```text
routine
systemic
sensitive
```

### Routine

Có thể land bằng same-provider review nếu:

- exact full SHA;
- session/worktree độc lập;
- required CI đầy đủ;
- không path sensitive;
- evidence hợp lệ;
- human readback.

### Systemic

Có thể AG–AG hoặc OpenAI–OpenAI review để tiến hành tạm thời, nhưng phải có
review debt bởi provider khác hoặc Human Auditor.

### Sensitive

Không land bằng review cùng provider. Cần:

- cross-provider review đã được runtime/receipt công nhận; hoặc
- Human Audit exact SHA có bằng chứng bền.

## 4. Assurance tạm thời

Trước khi provider registry hỗ trợ AG và OpenAI API, sử dụng:

```yaml
authoritative_assurance: review_deferred
advisory_review:
  executor_provider: google_antigravity
  reviewer_provider: openai_api
  provider_pair_is_distinct: true
  verdict: approve
```

Không dùng `cross_approved` chỉ vì hai tên provider khác nhau. Cross approval
cần contract máy đọc, identity evidence và receipt validation.

## 5. Luồng thực thi

1. Tạo Packet Spec.
2. Khóa exact base SHA, write set, provider và model.
3. Chạy capability probe.
4. Executor làm trên session/worktree riêng.
5. Freeze exact head/tree.
6. Reviewer khác session/worktree đọc review bundle.
7. Xuất verdict structured.
8. Validate schema và exact SHA cục bộ.
9. Publish + readback.
10. CI chạy trên đúng reviewed head.
11. Human Approver land exact SHA.
12. Post-merge readback và cập nhật review debt.

## 6. Review bundle

Reviewer chỉ nhận:

- Packet Spec
- base SHA
- head SHA
- tree SHA
- git diff
- git diff --numstat
- changed paths
- test commands + rc + positive evidence
- relevant protocol excerpts
- known limitations

Không gửi:

- `.env`;
- token;
- credential;
- home directory;
- raw transcript Executor;
- unrelated repository files;
- toàn bộ legal corpus nếu Packet không cần.

## 7. Non-convergence

Mỗi PR tối đa hai lượt review model theo cùng review policy.

Sau lần hai chưa approve:

- dừng;
- human checkpoint;
- tách Stable Slice nếu độc lập;
- tạo Remediation Packet;
- revision Packet/Mission;
- hoặc chờ provider khác.

Không đổi model, prompt, session hoặc tên Packet để reset budget.

## 8. Review debt

Review debt được tính từ:

- Review Class
- provider pair
- exact SHA validity
- session independence
- schema validity
- identity evidence
- CI status
- head staleness

Không mặc định mọi Routine Packet bằng 0 debt.

## 9. Trạng thái động

Trạng thái PR, quota, CI và Packet không được duy trì thủ công lâu dài trong
file này.

Nguồn trạng thái:

- GitHub Mission Issue;
- PR;
- workflow run;
- commit;
- `STATUS.generated` khi đã triển khai.

## 10. Stop conditions

Dừng khi:

- provider/model không khớp Packet;
- model mặc định bị sử dụng;
- input bundle vượt budget;
- output không validate;
- model yêu cầu tool chưa cấp;
- reviewer ghi repository;
- exact SHA lệch;
- required CI skipped/missing;
- xuất hiện security/LIVE/credential path;
- review budget hết;
- review evidence bị transport làm thay đổi.
