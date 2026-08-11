---
name: cross-review
description: Review chéo khác nền một PR packet của protocol đa phiên (tra-luat) trên nền Claude Code. Chỉ chứa cú pháp và công cụ của nền; mọi quy tắc review, mức assurance và tiêu chí hoàn tất nằm ở docs/PROTOCOL_DA_PHIEN.md.
argument-hint: "[so-issue-packet] [so-PR]"
---

# Adapter `cross-review` — Claude Code

**Đọc trước:** `docs/PROTOCOL_DA_PHIEN.md` §8 (mức review, quyền của người review, xử lý quota) và
§13 (trigger, hai trục, dạng verdict, nơi ghi verdict, định nghĩa hoàn tất).

Tệp này **không tóm tắt** những mục trên — đợt đầu của chính adapter này chép §13 rồi ghi sai nơi
đăng verdict. Chốt cơ học:

```bash
python .claude/dev/packet_loop.py doctrine-scan --root .
```

Dưới đây chỉ có cú pháp của nền.

## Lấy diff của ĐÚNG head SHA

```bash
gh pr view 56 --json headRefOid,headRefName,state,statusCheckRollup
gh pr diff 56 > diff.patch
git diff --numstat <base_sha> <head_sha> > numstat.txt
```

Verdict neo `reviewed_sha`; head đổi thì làm lại, đừng review bản đã cũ.

## Chạy nền kia trong sandbox

```bash
codex exec -s workspace-write --skip-git-repo-check --cd <sandbox> - < PROMPT.md
```

Sandbox là thư mục ngoài kho, chứa sẵn: `SPEC.md` · `diff.patch` · `numstat.txt` · trích protocol ·
`EVIDENCE.md` (số đo gate — thiếu nó sẽ ra kết luận "KHÔNG ĐO ĐƯỢC") · bản sao cây sau sửa. Trong
prompt phải **cấm đọc ra ngoài thư mục đó**: một lượt chạy phạm vi mở đã quét ra ngoài kho, đọc nhầm
transcript phiên, 40 phút không ra kết luận. `workspace-write` để nó tự đột biến bản sao mà không
chạm kho thật.

## GHI VERDICT LÊN PR — bắt buộc, đây là nơi verdict sống

```bash
gh pr review 56 --request-changes --body-file verdict.md
gh pr review 56 --approve         --body-file verdict.md
gh pr comment 56 --body-file verdict.md          # verdict blocked, hoặc phần bằng chứng dài
```

Không có bước này thì lượt review **không tồn tại** với ai ngoài phiên đang chạy — prompt review
vòng 6 của đợt F2 đã bốc hơi đúng kiểu đó. Nếu `gh` không dùng được, đường tương đương trên nền này
là MCP GitHub (`pull_request_review_write` với `method: create` rồi `submit_pending`); ghi rõ đã dùng
đường nào trong chính verdict.

## Ghi lại lượt review

```bash
python .claude/dev/packet_loop.py record-review --packet 55 --provider codex \
    --verdict changes_requested \
    --finding-id url-alias      --finding-desc "mô tả tự do, KHÔNG tham gia phép đếm" \
    --finding-id van-tay-lach   --finding-desc "mỗi lỗi một slug ổn định"
```

`--finding-id` là **khoá đếm**: slug kebab-case do người review đặt và giữ NGUYÊN qua các lượt cho
cùng một lỗi. Mô tả đổi thoải mái. Đặt slug mới cho một lỗi cũ là làm hỏng phép đếm — đó là lý do
khoá không còn là văn xuôi. Slug sai dạng hoặc thiếu thì lệnh thoát khác 0 và không tự đoán từ mô tả.

`--help` cho ý nghĩa từng mã thoát.

## Đọc log CI

```bash
gh api repos/ducthangho/tra-luat/actions/jobs/<id>/logs
```
