---
name: land-packets
description: Client do NGƯỜI gọi để chuẩn bị land các packet của một mission (tra-luat) trên nền Claude Code. Chỉ chứa cú pháp và công cụ của nền; quy tắc land nằm ở docs/PROTOCOL_DA_PHIEN.md.
argument-hint: "[so-issue-mission]"
disable-model-invocation: true
---

# Adapter `land-packets` — Claude Code

**Skill này KHÔNG tự trigger.** `disable-model-invocation: true` ở trên là cách nền này cưỡng chế
điều §13 quy định — đừng gỡ.

**Đọc trước:** `docs/PROTOCOL_DA_PHIEN.md` §13 (nội dung `land prepare`, ranh giới `--apply`, deploy
là lệnh riêng) · §8 (mức review được chấp nhận) · §12 (khi nào mission được `complete`).
Quy ước deploy của kho: `CLAUDE.md` §"Quy ước deploy".

Tệp này **không tóm tắt** những mục trên. Dưới đây chỉ có cú pháp của nền.

## `land prepare` — mặc định, DRY

```bash
gh issue view <mission> --json labels,title                    # mission còn packet chưa xong?
gh issue list --state open --label coord:packet --json number,labels
gh pr list --state open --json number,headRefName,statusCheckRollup
git -C <worktree> log --oneline origin/master..<branch>        # đã rebase trên EOL base chưa
/gate                                                          # land gate, rc trực tiếp từng lệnh
```

Báo cáo ra **số**, không ra cảm nhận: `N/N` hai số bằng nhau, `"ok": true`,
`release-verify --strict` 0 failed / 0 extra, `release-bundle` hai lần cùng SHA-256.

## `--apply` và deploy — KHÔNG thực thi từ đây

Trước mọi thao tác trong nhóm này:

```bash
python .claude/dev/packet_loop.py guard --action merge      # hoặc deploy | live
```

`--help` cho mã thoát. Lệnh này không có cờ nới.
