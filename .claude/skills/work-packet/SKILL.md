---
name: work-packet
description: Thực thi MỘT work packet của protocol đa phiên (tra-luat) — preflight spec/lease/worktree, chỉ sửa trong write set, chạy worker gate, mở PR, handoff. Dùng khi nhận một Issue packet có lease hợp lệ.
argument-hint: "[so-issue-packet]"
---

# Adapter `work-packet` — Claude Code

**Đây là ADAPTER, không phải nguồn quy tắc.** Quy tắc, schema, completion criteria chỉ nằm ở
`docs/PROTOCOL_DA_PHIEN.md`. Nếu tệp này và protocol nói khác nhau thì **protocol đúng, tệp này sai** —
sửa tệp này, đừng sửa protocol để khớp với nó.

Đọc trước khi làm bất cứ gì: `docs/PROTOCOL_DA_PHIEN.md` §3.2 (schema packet), §5 (write set),
§12 (stop conditions), §13 (hợp đồng skill này). Và `CLAUDE.md` cho quy trình sửa code của kho.

## Trình tự bắt buộc (§13)

1. **Đọc protocol** — không làm theo trí nhớ.
2. **Preflight**: lấy body Issue qua GraphQL (KHÔNG `gh issue view -q .body`), tái lập `spec_hash`
   theo công thức ghi cuối Issue, đối chiếu với giá trị khai. **Lệch ⇒ DỪNG**, spec đã trôi.
3. **Worktree riêng**, cắt từ `origin/master`; ghi đường dẫn + branch + base SHA vào Issue.
   Ghim `core.autocrlf=false` `core.eol=lf` `core.abbrev=7`.
4. **Chỉ sửa đúng `write_set`.** Cần đụng path ngoài write-set ⇒ **không tự mở rộng**: mở revision
   mới hoặc packet mới, kèm bằng chứng đo được.
5. **Worker gate** — xem `/gate`. rc đọc TRỰC TIẾP từng tiến trình, không qua pipe. Bằng chứng dương:
   `N/N` hai số BẰNG NHAU, `"ok": true`. **rc=0 không phải bằng chứng.**
6. **PR + handoff** — báo cáo số đo lên Issue, rồi bàn cho reviewer khác provider.

## Cưỡng chế — không bỏ qua được

Mọi transition đi qua máy trạng thái; nó là thứ giữ trần, không phải thiện chí của agent:

```bash
python .claude/dev/packet_loop.py init --packet <n> --mission <m> --executor <claude|codex> --reviewer <bên kia>
python .claude/dev/packet_loop.py begin-attempt --packet <n> --provider <provider của mình>
python .claude/dev/packet_loop.py next-comment --packet <n>      # lấy văn bản, ĐĂNG lên Issue
python .claude/dev/packet_loop.py mark-posted  --packet <n> --url <url comment>
```

Mã thoát: `0` đi tiếp · `2` sai cú pháp · `3` **DỪNG theo chốt** · `4` vi phạm cross-provider ·
`5` còn comment chưa đăng. Gặp `3` hoặc `4` thì **báo người**, không tự gỡ.

Quota/rate-limit làm hỏng một lượt thì **trả lượt**, đừng để nó ăn vào trần nội dung (§8):
`void-attempt --packet <n> --reason quota`.

## Ranh giới cứng

Vòng lặp tự do tới **TRƯỚC merge**, không hơn. Trước khi làm bất cứ việc nào dưới đây, chạy
`python .claude/dev/packet_loop.py guard --action <merge|deploy|live|secrets|force-push|delete-branch|delete-worktree|edit-other-spec>`
— nó **luôn** thoát mã 3 và **không có cờ nới**. Có cờ nới là không có chốt.

Riêng kho này: `gh pr merge --auto` **land NGAY** (private + free plan ⇒ không có required checks),
nên nó nằm trong nhóm cấm, không phải "merge có chờ".

## Nghiệm thu

Hoàn tất khi handoff hợp lệ đã được nhận — **không phải** khi gate local xanh. Với packet đụng
parity Windows–Linux, nghiệm thu thật là **CI xanh trọn trên cả hai nền**; đọc log bằng
`gh api repos/.../actions/jobs/<id>/logs` (`gh run view --job … --log` rụng step).
