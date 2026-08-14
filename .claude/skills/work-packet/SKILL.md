---
name: work-packet
description: Thực thi MỘT work packet của protocol đa phiên (tra-luat) trên nền Claude Code. Chỉ chứa cú pháp và công cụ của nền; mọi quy tắc, schema và tiêu chí hoàn tất nằm ở docs/PROTOCOL_DA_PHIEN.md.
argument-hint: "[so-issue-packet]"
---

# Adapter `work-packet` — Claude Code

**Đọc trước, không làm theo trí nhớ:** `docs/PROTOCOL_DA_PHIEN.md` §13 (trình tự bắt buộc, điều kiện
từ chối việc, định nghĩa hoàn tất) · §3.2 (schema packet) · §5 (write set) · §7 (handoff) ·
§12 (điều kiện dừng). Quy trình sửa code và quy ước deploy của kho: `CLAUDE.md`.

Tệp này **không tóm tắt** những mục trên. Tóm tắt là bản sao, và bản sao thì trôi lệch — ba lượt
review liên tiếp đã bắt được đúng lỗi đó ở chính adapter này. Nay có chốt cơ học:

```bash
python .claude/dev/packet_loop.py doctrine-scan --root .
```

Dưới đây chỉ có cú pháp của nền.

## Lấy spec

```bash
gh api graphql -f query='{repository(owner:"ducthangho",name:"tra-luat"){issue(number:55){body}}}'
```

Không dùng `gh issue view -q .body`. Tái lập `spec_hash` theo công thức ghi ở cuối chính Issue đó.

## Dựng worktree

```bash
git rev-parse --is-shallow-repository        # đòi false trước khi tin bất kỳ phép so lịch sử nào
git config core.autocrlf false && git config core.eol lf && git config core.abbrev 7
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPYCACHEPREFIX=<ngoài cây>
```

## Gate

`/gate`. Đọc mã thoát trực tiếp từng tiến trình, không qua pipe — `rc` của pipe là `rc` của lệnh cuối.

## Máy trạng thái — mọi chuyển động đi qua đây

```bash
python .claude/dev/packet_loop.py init          --packet 55 --mission 54 \
                                                --executor claude --reviewer codex
# `init` CHỈ tới `awaiting_lease`. Uỷ quyền là bước RIÊNG, và người cấp KHÔNG được
# là tên một provider — agent không tự cấp lease cho chính mình.
python .claude/dev/packet_loop.py record-lease  --packet 55 \
                                --lease-id wp55-r2-review-2-codex-20260813 \
                                --granted-by ducthangho \
                                --evidence https://github.com/o/r/issues/55#issuecomment-5281636040 \
                                --expires-utc 2026-08-13T18:30:00Z
python .claude/dev/packet_loop.py begin-attempt --packet 55 --provider claude
python .claude/dev/packet_loop.py next-comment  --packet 55        # in văn bản → ĐĂNG lên Issue
python .claude/dev/packet_loop.py record-post   --packet 55 --for reviewing --comment-id 5258163128
python .claude/dev/packet_loop.py transition    --packet 55 --to reviewing --comment-id 5258163128 \
                                                --head-sha $(git rev-parse HEAD)
python .claude/dev/packet_loop.py void-attempt  --packet 55 --reason quota
python .claude/dev/packet_loop.py status        --packet 55
python .claude/dev/packet_loop.py where
```

**Lease không tự có.** `init` chỉ khai *hình dạng* của packet và dừng ở `awaiting_lease`; `leased`
chỉ đạt được qua `record-lease`, và lệnh đó chỉ **ghi hộ** một quyết định đã có ở nơi khác — nó đòi
người cấp (không được là `claude`/`codex`), dấu vết bền để đối chiếu, và hạn. Hạn được cưỡng chế
**cả lúc ghi lẫn mỗi lần mở lượt**: lease hết hạn thì `begin-attempt` thoát 8. Bản trước ghi thẳng
`leased` ngay trong `init`, nên ai gõ được `init` là tự có lease — review cross-provider tái hiện
bằng `init --packet 999999 --mission 888888` rồi `begin-attempt`, cả hai `rc=0`.

`--comment-id` là **ID GitHub trả về lúc đăng**, không phải URL. Ghi sổ bằng `record-post` trước, rồi
`transition` mới tiêu thụ được; mỗi ID dùng đúng một lần cho đúng một chuyển động. Tiến trình này
không gọi mạng nên **không xác minh** ID có thật — đọc `--help` để thấy nó bảo đảm đúng những gì.

Vào `reviewing` phải khai `--head-sha` là **exact head** đưa ra review. Bản duyệt sau đó phải neo
đúng SHA ấy, và mở lượt mới sẽ xoá mỏ neo — nên có commit mới thì bản duyệt cũ hết hiệu lực.

`--help` cho danh sách đầy đủ và ý nghĩa từng mã thoát. Mã thoát khác 0 ⇒ dừng và báo người; script
tự nói lý do trên stderr.

## Chặn cứng

```bash
python .claude/dev/packet_loop.py guard --action merge
# merge | deploy | live | secrets | force-push | delete-branch | delete-worktree | edit-other-spec
```

Lệnh này không có cờ nới, và không được thêm.

## Đăng heartbeat

```bash
gh issue comment 55 --body-file heartbeat.md
```

Nhịp và nội dung tối thiểu do lease của đợt khai; đọc chính comment cấp lease, đừng nhớ theo lần trước.

## Đọc log CI

```bash
gh api repos/ducthangho/tra-luat/actions/jobs/<id>/logs
```
