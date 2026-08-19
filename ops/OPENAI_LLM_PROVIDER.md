# OpenAI API qua `llm` — Provider Contract

> Provider: `openai_api`
>
> Execution surface: `llm_cli`
>
> Trạng thái ban đầu: reviewer read-only, executor patch-only
>
> Không dùng ChatGPT subscription làm API authority.

## 1. Cài đặt

Khuyến nghị dùng môi trường công cụ riêng:

```bash
pipx install llm
# hoặc uv tool install llm
```

Không cài trực tiếp vào Python runtime chính của tra-luat nếu không cần.

Sau khi cài:

```bash
llm --version
llm models
llm logs status
```

## 2. Credential

Cho sử dụng thủ công cá nhân:

```bash
llm keys set openai
```

Đối với launcher hoặc automation, ưu tiên:

`OPENAI_API_KEY` được inject vào riêng tiến trình con từ OS secret store hoặc CI secret.

Cấm:

- commit key;
- ghi key vào prompt;
- in key vào log;
- đưa key cho Reviewer tool;
- copy keys.json giữa thiết bị qua Git hoặc Drive.

## 3. Model

Mọi invocation phải có:

`-m <exact-model-id>`

Cấm:

- bỏ `-m`;
- dùng default model;
- dùng alias ngắn;
- tự đổi model sau preflight;
- dùng model không nằm trong allowlist Packet.

Capability probe phải ghi:

```yaml
provider: openai_api
surface: llm_cli
model_id: <exact>
llm_version: <exact>
model_present: true
schema_supported: true | false | unknown
checked_at: <iso-timestamp>
```

## 4. Logging

Mỗi invocation bắt buộc dùng:

`--no-log`

Ngoài ra nên chạy:

`llm logs off`

như defense-in-depth.

Controller phải đặt một `LLM_USER_PATH` tạm thời cho từng run để cô lập template, model option và local history khỏi cấu hình người dùng khác.

## 5. Reviewer mode

Reviewer mode phải:

- `--no-log`;
- `--no-stream`;
- exact model;
- JSON Schema;
- không tools;
- không conversation continuation;
- không truy cập filesystem ngoài review bundle;
- không đọc Executor transcript.

Lời gọi logic:

```bash
llm \
  -m <exact-model-id> \
  --no-log \
  --no-stream \
  --schema <review-schema.json> \
  --system <review-system-prompt>
```

Review bundle được truyền qua stdin bởi Python bridge, không dựng pipeline shell khác nhau cho Windows và POSIX.

Output phải được local controller:

- parse JSON;
- validate JSON Schema;
- kiểm `reviewed_sha`;
- kiểm provider/model;
- tính output hash;
- ghi immutable evidence;
- sau đó mới cho phép publish.

## 6. Executor mode — giai đoạn đầu

Executor không được cấp shell hoặc filesystem tools.

Model chỉ sinh:

`openai_patch_plan.v0`

gồm:

```yaml
base_sha: <exact-base-sha>
expected_head_sha: <exact-head-sha>
files:
  - path: <relative-path>
    operation: create | replace | patch
    content_or_patch: <content>
test_plan: <commands>
risks: <notes>
```

Controller:

- kiểm path nằm trong write set;
- từ chối symlink/path traversal;
- áp patch;
- chạy test;
- đọc lại diff;
- tạo commit bằng executor controller, không phải model.

## 7. Tool-enabled executor — bị hoãn

`llm` hỗ trợ tool calling, nhưng không được dùng ngay cho tra-luat.

Chỉ mở sau khi có:

- closed toolbox;
- path allowlist;
- no-network test sandbox;
- secret redaction;
- prompt-injection negative matrix;
- tool-call budget;
- event log;
- rollback;
- Human Audit hoặc cross-provider review.

## 8. Lỗi và review budget

Nếu transport không cung cấp event máy đọc chứng minh model đã bắt đầu generation:

`generation_start: unproven`

Timeout hoặc crash không được tự động retry. Chuyển sang human/review-rescue checkpoint.

Không suy `model_generation_started` từ:

- byte đầu tiên;
- banner CLI;
- stderr;
- exit code;
- dòng log wrapper.

## 9. Retention

Lưu dài hạn:

- prompt hash;
- response hash;
- exact model;
- exact SHA;
- verdict;
- finding IDs;
- token/cost summary nếu có;
- artifact references.

Không lưu dài hạn:

- raw API key;
- raw prompt chứa nội dung nhạy cảm;
- toàn bộ source không liên quan;
- raw tool payload;
- conversation SQLite mặc định.
