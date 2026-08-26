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

## Công cụ — nhánh packet KHÔNG mang công cụ của kho

`base_sha` thường cũ hơn công cụ trên nhánh chính, nên cây làm việc của packet có thể
thiếu cả bộ dựng công cụ lẫn hook phiên, và `settings.json` bản cũ có thể chưa đăng ký
`SessionStart`. Kho gắn giữa phiên thì hook cũng không chạy. Ba chuyện độc lập, mỗi
chuyện một mình đã đủ để phiên mở ra mà không có `codex`/`rg`.

Lấy công cụ TỪ NHÁNH CHÍNH, đừng chạy cả hook phiên chỉ để lấy một thứ — hook có bước
cài phụ thuộc Python và đã đo được một lần làm hỏng môi trường đang tốt:

```bash
D="$(mktemp -d)"
git show origin/master:.claude/dev/launcher.py > "$D/launcher.py"
PY="$(command -v python3 || command -v python || command -v py)"   # CLAUDE.md: nhận CẢ BA tên
"$PY" "$D/launcher.py" doctor              # bằng chứng DƯƠNG, chạy được từ mọi nhánh
```

**Vắng mặt là một QUAN SÁT; "môi trường không có" là một KẾT LUẬN.** Trước khi báo với
người điều phối rằng không gọi được một CLI, phải chạy `command -v <tool>` và
`<tool> login status` trong CHÍNH phiên này, rồi loại trừ xong hai khả năng còn lại: hook
chưa chạy, và nhánh đang checkout không mang hook. Tài liệu mô tả một lần đo trong quá
khứ trên một cây khác — nó không phải quan sát về phiên đang chạy. Đã trả giá:
một phiên báo cross-review không chạy được, trong khi CLI cài được và lượt review sau đó
tìm ra một P1 thật.

Kiểm biến bí mật bằng **sự tồn tại**, không bao giờ in nội dung — biến khôi phục đăng
nhập chứa refresh token, in một lần là phải thu hồi và cấp lại:

```bash
if [ -n "${TEN_BIEN:-}" ]; then echo "có, ${#TEN_BIEN} ký tự"; else echo "chưa đặt"; fi
```

Đừng nối `${VAR:+…}` với `${VAR:-…}` trong cùng một chuỗi: `:-` chỉ thay thế khi biến
**rỗng hoặc chưa đặt**, nên ở nhánh "đã đặt" — nhánh người ta thật sự chạy — nó bung ra
**chính giá trị**. Bản trước của dòng này in `có, 27 ký tự` rồi in luôn cả token.

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
