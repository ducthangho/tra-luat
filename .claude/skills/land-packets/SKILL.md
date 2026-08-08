---
name: land-packets
description: Client do NGƯỜI gọi để chuẩn bị land các packet đã accepted của một mission (tra-luat) — mặc định chỉ chạy `land prepare` dạng dry-run. Không tự trigger, không chứa quyền merge, không deploy.
argument-hint: "[so-issue-mission]"
disable-model-invocation: true
---

# Adapter `land-packets` — Claude Code

**Skill này KHÔNG tự trigger** (§13: "user-invoked client. Không tự trigger"). Nhãn
`disable-model-invocation: true` ở trên là cách Claude Code cưỡng chế điều đó — đừng gỡ.

**Đây là ADAPTER, không phải nguồn quy tắc.** Quy tắc ở `docs/PROTOCOL_DA_PHIEN.md` §12 (mission
không được `complete` khi còn packet chưa xong) và §13.

## Mặc định: `land prepare` — DRY, không ghi

1. **Freeze mission** — không nhận packet mới trong lúc chuẩn bị.
2. **Kiểm packet/review/override**: mọi packet phải `accepted`; review phải `cross_approved`
   (hoặc `same_provider_approved` có lý do ghi rõ). Workflow, security paths, credential boundary,
   dispatcher, migration dữ liệu và LIVE adapter **không được** `review_deferred` (§8).
3. **Rebase integration** — mọi branch phải nằm trên EOL base canonical.
4. **Release metadata** + **land gate**.

Báo cáo ra số, không ra cảm nhận: `N/N` hai số BẰNG NHAU, `"ok": true`, `release-verify --strict`
0 failed / 0 extra, `release-bundle` hai lần cùng SHA-256.

## `--apply` và deploy — KHÔNG thuộc skill này

`--apply` gửi mission/head SHA tới cùng operation `land apply` mà nền tảng dùng; **skill không chứa
quyền hay logic merge riêng**. Deploy là lệnh RIÊNG và cần quyền LIVE — xem `## Quy ước deploy` trong
`CLAUDE.md` (chốt chống thụt lùi: đọc version Package đang có trên Drive TRƯỚC khi push; Drive ≥ bản
sắp đẩy ⇒ DỪNG, hỏi người).

Trước mọi thao tác trong nhóm này, chạy:

```bash
python .claude/dev/packet_loop.py guard --action merge     # hoặc deploy | live
```

Nó **luôn** thoát mã 3 và không có cờ nới. Đó là điểm: quyết định land/deploy là của người, không phải
của vòng lặp.

## Cạm bẫy đã trả giá trong kho này

- `gh pr merge --auto` **land NGAY** — kho private + free plan nên không có required checks
  (branch protection/ruleset trả 403). "Auto" ở đây thoái hoá thành "merge now". Muốn chờ xanh thì
  tự đợi `gh pr checks`.
- **Không squash** khi packet nhiều commit — lịch sử tách trách nhiệm là một phần của nghiệm thu.
- `release-check --full` **rc=0 dù manifest lệch**; chỉ `release-verify --strict` bắt được.
- Thêm/xoá tệp trong cây ⇒ tái sinh `RELEASE_MANIFEST.json`, và ghi lại golden NẾU số đếm kiểm kê đổi.
  Bỏ bước này thì phiên land KẾ TIẾP ăn gate đỏ không phải do nó.
