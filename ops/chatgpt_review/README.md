# ChatGPT Pro Web Review — Local Bundle Contract

> Provider: `openai_chatgpt`
>
> Execution surface: `chatgpt_web`
>
> Transport: `human_mediated`
>
> Assurance: `advisory_review`

## 1. Mục đích

Sử dụng ChatGPT Pro qua giao diện Web để:

- review exact diff;
- phản biện Packet Spec;
- đề xuất finding và test;
- sinh patch hoặc remediation plan cho tác vụ nhỏ.

Không sử dụng cookie, session token, unofficial ChatGPT CLI hoặc endpoint nội bộ.

## 2. Tạo bundle

```bash
python ops/chatgpt_review/build_bundle.py \
  --packet-spec ops/specs/<packet>.md \
  --base-sha <base-sha> \
  --head-sha <head-sha> \
  --test-evidence <test-evidence.json> \
  --out work/reviews/<packet>-<head-short>
```

Builder phải:

- fail nếu worktree bẩn ngoài Packet;
- fail nếu SHA không đủ 40 ký tự;
- fail nếu changed path ngoài declared write set;
- sinh tree hash;
- hash mọi file;
- không đọc `.env`, credential hoặc home;
- không gọi mạng;
- không sửa repository.

## 3. Gửi ChatGPT

1. Tạo một conversation mới.
2. Tải lên:
   - `00_BUNDLE_MANIFEST.json`
   - `01_PACKET_SPEC.md`
   - `02_REVIEW_INSTRUCTIONS.md`
   - `03_DIFF.patch.txt`
   - `04_CHANGED_PATHS.txt`
   - `05_NUMSTAT.txt`
   - `06_TEST_EVIDENCE.json`
   - `07_REVIEW_NOTE_TEMPLATE.yaml`

GitHub App có thể được dùng để tham khảo repository, nhưng review phải dựa vào
bundle exact-SHA; dữ liệu GitHub live có thể thay đổi sau khi bundle được tạo.

## 4. Prompt

Dùng nội dung `REVIEW_PROMPT.md`.

Yêu cầu ChatGPT:

- chỉ review SHA trong bundle;
- không suy rằng đã chạy test;
- kiểm hai trục Spec và Standards/Security;
- không đề xuất ngoài write set nếu không đánh dấu successor;
- trả đúng YAML theo template;
- dùng stable finding ID;
- không thêm lời dẫn ngoài YAML.

## 5. Validate note

Lưu output thành:

`chatgpt_review_note.yaml`

Chạy:

```bash
python ops/chatgpt_review/validate_note.py \
  --bundle work/reviews/<bundle>/00_BUNDLE_MANIFEST.json \
  --note chatgpt_review_note.yaml \
  --repo . \
  --receipt-out chatgpt_review_validation_receipt.yaml
```

Có thể bổ sung:

`--pr 123`

để validator đọc PR head qua GitHub route đã được chứng minh.

## 6. Publish

Chỉ publish khi validator rc=0.

```bash
gh pr comment <pr-number> \
  --body-file work/reviews/<bundle>/RENDERED_REVIEW_NOTE.md
```

Nếu `gh` không được chứng minh, dùng GitHub connector hoặc route hợp lệ khác.

Đọc ngược comment sau khi đăng và đối chiếu hash/nội dung.

## 7. Giới hạn

Validator không chứng minh:

- model nào trong ChatGPT đã trả lời;
- ChatGPT session ID;
- người dùng có thực sự gửi đủ tệp;
- model đã đọc toàn bộ nội dung;
- model đã chạy test.

Vì vậy review luôn là advisory.
