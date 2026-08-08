---
name: cross-review
description: Review chéo khác provider một PR packet của protocol đa phiên (tra-luat) trên nền Claude Code. Chỉ chứa cú pháp và công cụ của nền; quy tắc review nằm ở docs/PROTOCOL_DA_PHIEN.md.
argument-hint: "[so-issue-packet] [so-PR]"
---

# Adapter `cross-review` — Claude Code

**Đọc trước:** `docs/PROTOCOL_DA_PHIEN.md` §8 (mức review, quyền của reviewer, xử lý quota) và §13
(trigger, hai trục, dạng verdict, nơi ghi verdict, định nghĩa hoàn tất).

Tệp này **không tóm tắt** những mục trên — đợt đầu của chính adapter này chép §13 rồi ghi sai nơi
đăng verdict. Dưới đây chỉ có cú pháp của nền.

## Chạy provider kia trong sandbox

```bash
codex exec -s workspace-write --skip-git-repo-check --cd <sandbox> - < PROMPT.md
```

Sandbox là một thư mục ngoài kho, chứa sẵn: `SPEC.md` · `diff.patch` · `numstat.txt` · trích protocol ·
`EVIDENCE.md` (số đo gate — thiếu nó reviewer sẽ kết luận "KHÔNG ĐO ĐƯỢC") · bản sao cây sau sửa.
Trong prompt phải **cấm reviewer đọc ra ngoài thư mục đó**: lượt chạy với phạm vi mở đã quét ra ngoài
kho, đọc nhầm transcript phiên, 40 phút không ra kết luận. `workspace-write` để nó tự đột biến bản
sao mà không chạm kho thật.

## Ghi lại lượt review

```bash
python .claude/dev/packet_loop.py record-review --packet <n> --provider <claude|codex> \
    --verdict <approve|changes_requested|blocked> [--finding "<mô tả>" ...]
python .claude/dev/packet_loop.py next-comment  --packet <n>
python .claude/dev/packet_loop.py mark-posted   --packet <n> --url <url comment thật>
```

`--help` cho mã thoát. Vân tay finding bỏ hoa/thường, khoảng trắng và dấu câu **nhưng giữ toán tử**,
nên `state == blocked` và `state != blocked` vẫn là hai finding khác nhau.

## Đọc log CI

```bash
gh api repos/ducthangho/tra-luat/actions/jobs/<id>/logs
```
