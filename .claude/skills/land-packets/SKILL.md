---
name: land-packets
description: Client do NGƯỜI gọi để chuẩn bị land các packet của một mission (tra-luat) trên nền Claude Code. Chỉ chứa cú pháp và công cụ của nền; mọi quy tắc land, điều kiện uỷ quyền và tiêu chí hoàn tất nằm ở docs/PROTOCOL_DA_PHIEN.md.
argument-hint: "[so-issue-mission]"
disable-model-invocation: true
---

# Adapter `land-packets` — Claude Code

**Skill này KHÔNG tự trigger.** `disable-model-invocation: true` ở frontmatter là cách nền này cưỡng
chế điều §13 quy định — đừng gỡ.

**Đọc trước:** `docs/PROTOCOL_DA_PHIEN.md` §13 (nội dung `land prepare`, ranh giới `--apply`, deploy
là cổng riêng) · §8 (mức review được chấp nhận) · §10.2 (các thuật ngữ trạng thái, không dùng thay
nhau) · §12 (khi nào mission được đóng). Quy ước deploy của kho: `CLAUDE.md`.

Tệp này **không tóm tắt** những mục trên. Chốt cơ học:

```bash
PY="$(command -v python3 || command -v python || command -v py)"   # CLAUDE.md: nhận CẢ BA tên
"$PY"  .claude/dev/packet_loop.py doctrine-scan --root .
```

Dưới đây chỉ có cú pháp của nền.

## `land prepare` — mặc định, DRY

```bash
gh issue view 54 --json labels,title
gh issue list --state open --label coord:packet --json number,labels
gh pr list --state open --json number,headRefName,headRefOid,statusCheckRollup
git -C <worktree> log --oneline origin/master..<branch>
/gate
```

Báo cáo ra **số**, không ra cảm nhận: hai số bằng nhau, `"ok": true`, `0 failed / 0 extra`, hai lượt
bundle cùng SHA-256. Ngưỡng cụ thể của từng gate nằm ở `CLAUDE.md` và ở chính đầu ra của lệnh.

## `--apply` và deploy — KHÔNG thực thi từ đây

Trước mọi thao tác trong nhóm này:

```bash
PY="$(command -v python3 || command -v python || command -v py)"   # CLAUDE.md: nhận CẢ BA tên
"$PY"  .claude/dev/packet_loop.py guard --action merge     # hoặc deploy | live
```

Lệnh này không có cờ nới, và không được thêm. Uỷ quyền cho một exact head SHA sống trên GitHub, không
sống trong ngữ cảnh phiên — đọc §13 để biết cái gì được coi là uỷ quyền hợp lệ.
