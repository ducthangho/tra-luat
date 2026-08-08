---
name: work-packet
description: Thực thi MỘT work packet của protocol đa phiên (tra-luat) trên nền Claude Code — dựng worktree, gọi máy trạng thái cưỡng chế stop conditions, chạy gate, mở PR. Quy tắc nằm ở docs/PROTOCOL_DA_PHIEN.md, tệp này chỉ là cú pháp.
argument-hint: "[so-issue-packet]"
---

# Adapter `work-packet` — Claude Code

**ĐỌC `docs/PROTOCOL_DA_PHIEN.md` TRƯỚC.** Trình tự bắt buộc, điều kiện từ chối việc, và định
nghĩa hoàn tất của skill này nằm ở **§13**; schema packet ở **§3.2**; write set ở **§5**; stop
conditions ở **§12**. Tệp này **cố ý KHÔNG tóm tắt** chúng — một bản tóm tắt là một bản sao, và bản
sao thì trôi lệch rồi mâu thuẫn với bản gốc. Ở đây chỉ có **cú pháp và công cụ của nền này**.

Quy trình sửa code, ngưỡng ruff, quy ước deploy của kho: `CLAUDE.md`.

## Cú pháp của nền — phần duy nhất thuộc về tệp này

**Preflight spec.** Lấy body Issue qua GraphQL, KHÔNG `gh issue view -q .body`:

```bash
gh api graphql -f query='{repository(owner:"ducthangho",name:"tra-luat"){issue(number:<n>){body}}}'
```

Tái lập `spec_hash` theo công thức ghi ở cuối chính Issue đó, đối chiếu giá trị khai. **Lệch ⇒ DỪNG.**

**Worktree riêng**, cắt từ `origin/master`, ghim EOL để hash khớp manifest:

```bash
git config core.autocrlf false && git config core.eol lf && git config core.abbrev 7
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPYCACHEPREFIX=<ngoài cây>        # __pycache__ rơi vào scripts/test_fragments/ làm ĐỎ selftest
```

**Gate**: `/gate`. **Đọc mã thoát TRỰC TIẾP từng tiến trình, không qua pipe.**

**Máy trạng thái** — mọi transition đi qua đây, không có đường tắt:

```bash
python .claude/dev/packet_loop.py init          --packet <n> --mission <m> \
                                                --executor <claude|codex> --reviewer <bên kia>
python .claude/dev/packet_loop.py begin-attempt --packet <n> --provider <provider của mình>
python .claude/dev/packet_loop.py next-comment  --packet <n>     # lấy văn bản → ĐĂNG lên Issue
python .claude/dev/packet_loop.py mark-posted   --packet <n> --url <url comment THẬT của Issue đó>
python .claude/dev/packet_loop.py void-attempt  --packet <n> --reason quota   # xem §8
python .claude/dev/packet_loop.py status        --packet <n>
```

Mã thoát khác 0 nghĩa là **DỪNG và báo người** — script tự giải thích lý do trên stderr. Không tìm
đường vòng: `init` không dựng lại được lên state đã có, `void-attempt` không gỡ được `blocked`,
`mark-posted` không nhận URL bịa. Cả ba đều đã bị bịt sau khi cross-review vòng 1 lách qua được.

**Trước mọi việc ngoài ranh giới** (merge, deploy, LIVE, secrets, force-push, xoá branch/worktree,
sửa spec packet khác):

```bash
python .claude/dev/packet_loop.py guard --action merge
```

Nó **luôn** dừng và **không có cờ nới**. Riêng kho này: `gh pr merge --auto` **land NGAY** (private +
free plan ⇒ không có required checks), nên nó thuộc nhóm cấm chứ không phải "merge có chờ".

**Đọc log CI**: `gh api repos/ducthangho/tra-luat/actions/jobs/<id>/logs` — `gh run view --job … --log`
rụng step.
