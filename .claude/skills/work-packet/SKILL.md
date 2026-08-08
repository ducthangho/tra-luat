---
name: work-packet
description: Thực thi MỘT work packet của protocol đa phiên (tra-luat) trên nền Claude Code. Chỉ chứa cú pháp và công cụ của nền; quy tắc nằm ở docs/PROTOCOL_DA_PHIEN.md.
argument-hint: "[so-issue-packet]"
---

# Adapter `work-packet` — Claude Code

**Đọc trước, không làm theo trí nhớ:** `docs/PROTOCOL_DA_PHIEN.md` §13 (trình tự bắt buộc, điều kiện
từ chối việc, định nghĩa hoàn tất) · §3.2 (schema packet) · §5 (write set) · §12 (stop conditions).
Quy trình sửa code và quy ước deploy của kho: `CLAUDE.md`.

Tệp này **không tóm tắt** những mục trên. Tóm tắt là bản sao, và bản sao thì trôi lệch — đợt đầu của
chính adapter này đã chép §13 mà làm rơi mất heartbeat. Dưới đây chỉ có cú pháp của nền.

## Lấy spec

```bash
gh api graphql -f query='{repository(owner:"ducthangho",name:"tra-luat"){issue(number:<n>){body}}}'
```

Không dùng `gh issue view -q .body`. Tái lập `spec_hash` theo công thức ghi ở cuối chính Issue đó.

## Dựng worktree

```bash
git config core.autocrlf false && git config core.eol lf && git config core.abbrev 7
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPYCACHEPREFIX=<ngoài cây>
```

## Gate

`/gate`. Đọc mã thoát trực tiếp từng tiến trình, không qua pipe.

## Máy trạng thái — mọi transition đi qua đây

```bash
python .claude/dev/packet_loop.py init          --packet <n> --mission <m> \
                                                --executor <claude|codex> --reviewer <bên kia>
python .claude/dev/packet_loop.py begin-attempt --packet <n> --provider <của mình>
python .claude/dev/packet_loop.py next-comment  --packet <n>     # lấy văn bản → ĐĂNG lên Issue
python .claude/dev/packet_loop.py mark-posted   --packet <n> --url <url comment thật, mỗi URL một lần>
python .claude/dev/packet_loop.py void-attempt  --packet <n> --reason quota
python .claude/dev/packet_loop.py status        --packet <n>
python .claude/dev/packet_loop.py where
```

`--help` cho danh sách đầy đủ và ý nghĩa từng mã thoát. Mã thoát khác 0 ⇒ **dừng và báo người**;
script tự nói lý do trên stderr. Đừng tìm đường vòng — mọi lối đã thử đều đã bị bịt và có test khoá.

## Chặn cứng

```bash
python .claude/dev/packet_loop.py guard --action <merge|deploy|live|secrets|force-push|delete-branch|delete-worktree|edit-other-spec>
```

## Đọc log CI

```bash
gh api repos/ducthangho/tra-luat/actions/jobs/<id>/logs
```
