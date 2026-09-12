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
PY="$(command -v python3 || command -v python || command -v py)"   # CLAUDE.md: nhận CẢ BA tên
"$PY"  .claude/dev/packet_loop.py doctrine-scan --root .
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
PY="$(command -v python3 || command -v python || command -v py)"   # CLAUDE.md: nhận CẢ BA tên
"$PY"  .claude/dev/packet_loop.py init          --packet 55 --mission 54 \
                                                --executor claude --reviewer codex
# `init` CHỈ tới `awaiting_lease`. Uỷ quyền là bước RIÊNG, và người cấp KHÔNG được
# là tên một provider — agent không tự cấp lease cho chính mình.
"$PY"  .claude/dev/packet_loop.py record-lease  --packet 55 \
                                --lease-id wp55-r2-review-2-codex-20260813 \
                                --granted-by ducthangho \
                                --evidence https://github.com/o/r/issues/55#issuecomment-5281636040 \
                                --expires-utc 2026-08-13T18:30:00Z
"$PY"  .claude/dev/packet_loop.py begin-attempt --packet 55 --provider claude
"$PY"  .claude/dev/packet_loop.py next-comment  --packet 55        # in văn bản → ĐĂNG lên Issue
"$PY"  .claude/dev/packet_loop.py record-post   --packet 55 --for reviewing --comment-id 5258163128
"$PY"  .claude/dev/packet_loop.py transition    --packet 55 --to reviewing --comment-id 5258163128 \
                                                --head-sha $(git rev-parse HEAD)
"$PY"  .claude/dev/packet_loop.py void-attempt  --packet 55 --reason quota
"$PY"  .claude/dev/packet_loop.py status        --packet 55
"$PY"  .claude/dev/packet_loop.py where
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

## Vòng lặp vá → review → dừng

`§8` và `§13` quy định mức review và định nghĩa hoàn tất; `§12` quy định điều kiện dừng và ngưỡng.
Mục này chỉ nói **phiên phải làm gì với BẢNG LỚP mà reviewer trả về** — không nhắc lại ngưỡng nào.

**Điều kiện dừng đọc theo `review_class` của lease, không theo cảm giác đã đủ.** Lớp cao nhất
(`sensitive`) đòi một `approve` **tường minh**; một lượt không tìm ra gì mà thiếu bảng săn thì `§8` xếp
là *chưa đo*, không phải *đã sạch*. Lặp vá → review cho tới khi hết lớp P1 và P2, hoặc có `approve`.

**Đơn vị là LỚP, không phải từng lỗi.** `cross-review` sinh ra bảng ấy; đây là bên ĐỌC nó:

| reviewer trả về | phiên làm gì |
|---|---|
| lớp P1 hoặc P2 còn mở | vá THEO LỚP rồi mở vòng mới |
| cùng một lớp nêu **lần thứ BA** | **CẤM vá lẻ lần nữa** — xem dưới |
| `approve` + bảng săn đủ | dừng vòng lặp; sang phần merge |
| `blocked` | dừng, xuất handoff, **hỏi chủ kho** |

**Một lớp nêu lần thứ BA nghĩa là hai bản vá trước KHÔNG trúng gốc.** Vá lẻ lần thứ ba là mua thêm một
lượt để thua theo cùng cách. Lúc ấy đổi CÁCH TIẾP CẬN: liệt kê HẾT đường vào của lớp TRƯỚC khi sửa, và
nếu lớp ấy không đóng được trong phạm vi packet thì nói thẳng — nó là một nợ, và nợ thuộc packet khác.

**Vá theo LỚP, đừng vá theo danh sách reviewer chỉ.** Reviewer nêu những thể hiện họ thấy; cơ chế sinh
ra chúng thường có đường vào mà không ai nêu. Tự liệt kê hết đường vào trước, đóng cả loạt, và cho mỗi
đường một chốt riêng — ba chốt không phân biệt được bằng đầu vào là bộ TƯƠNG ĐƯƠNG, tức chỉ đo một cái.

**KHÔNG hội tụ thì đo bằng PHÂN HẠNG, không bằng số lượt.** Dãy lớp P1/P2 qua các vòng phải đi xuống.
Số lỗi giảm mà hạng không giảm thì chưa hội tụ; hạng giảm mà cùng một slug vẫn còn thì cũng chưa.

**Thu hẹp phạm vi để lấy `approve` là LÁCH, không phải hội tụ.** Bỏ một đường dẫn khỏi diff cho lớp
biến mất thì lớp vẫn sống, chỉ là ngoài tầm nhìn của lượt sau. Đổi write set là **revision mới** theo
`§3.2`/`§5`, không phải một quyết định trong vòng lặp.

**Rescue Checkpoint: DỪNG và HỎI.** Chạm checkpoint thì phiên không tự chọn đường đi tiếp — nó xuất
handoff kèm phép đo rồi chờ chủ kho quyết. Điều kiện chạm và các đường ra ở `ADR-0037`.

## Sau khi đã QUYẾT MERGE — ba mệnh đề TÁCH RỜI

Đọc đủ ba, đừng gộp; bỏ mệnh đề nào cũng đổi nghĩa cả mục:

1. Head đổi tiếp **KHÔNG** kéo theo một vòng cross-review mới.
2. Nghĩa vụ còn lại **VẪN CÓ**: phải có **CI hậu merge**. Đây KHÔNG phải *"merge rồi khỏi đo"*.
3. Ngoại lệ duy nhất là **PHÁT HIỆN LỖI** — lúc ấy mở vòng mới và **khai lý do**.

Mệnh đề 2 tồn tại vì viết yếu đi là mở đường merge rồi không ai đo gì. Mệnh đề 3 tồn tại vì bỏ nó là
khai *"merge rồi không review nữa bất kể gì"*.

**Bẫy đã đo khi đọc CI hậu merge:** huỷ một job trong lượt hậu merge làm kết luận **mức RUN** thành
`cancelled` dù job kia `success` — nền không có đường huỷ MỘT job. Nên đọc CI hậu merge ở **mức JOB**,
đừng đọc `conclusion` của run: một job xanh nằm trong một run bị huỷ trông y hệt một lượt chưa bao giờ
xanh.

## Ba loại chi CI — và `N = 0` cho giai đoạn TRƯỚC merge

| loại | là gì | ngân sách |
|---|---|---|
| **(a)** | CI gác cổng do nền **tự bắn** theo push/PR, cộng lượt **CI hậu merge** | không tính vào `N` |
| **(b)** | lượt CI **gọi tay** trong lúc lặp vá → review | **`N = 0` TRƯỚC merge** |
| **(c)** | CI thăm dò: gọi tay `workflow_dispatch`, lane nền-khác, hay full CI **trước merge** | **CẤM** |

`N = 0` là điểm khác bản trước của mục này. Để `N` mở kèm câu *"đóng băng trong đặc tả"* thì một phiên
vẫn tự cấp cho mình vài lượt full CI mà vẫn đúng chữ — đúng hình dạng *"ngoại lệ thành thường lệ"*.

**Ca đối chiếu, đo được:** chuỗi `#512` ba vòng cuối **không** gọi `workflow_dispatch` lượt nào và chỉ
nhận lượt tự động ⇒ luật này cho ra **ĐẠT** trên chuỗi ấy. Một luật làm một chuỗi đã tuân thủ thành
*vi phạm* là luật viết sai, không phải chuỗi sai.

Nhắc một điều đã đo và dễ đọc ngược: gắn nhãn để xin một lane khác **không tự sinh lượt chạy nào** khi
workflow không khai loại sự kiện gắn nhãn. Nhãn chỉ được đọc ở lượt bắn KẾ TIẾP — nên "đã gắn nhãn"
không phải "đã có lượt đo".

**KHÔNG CỔNG NÀO CƯỠNG CHẾ MỤC NÀY.** Cả phần vòng lặp, phần hậu-merge và ba loại chi CI ở trên đều là
**chữ**, tức kỷ luật đọc — y như các mục khác của skill này. Cưỡng chế chi CI bằng máy là packet riêng
(`CONG-CHAN-CHI-CI-SOM`); cổng đọc một hằng số trần duy nhất là nợ `SO-CANON-CHUA-TON-TAI`. Ai tin ở
đây đã có cơ chế sẽ bỏ đúng bước kiểm bằng tay mà mục này đang đòi.

## Chặn cứng

```bash
PY="$(command -v python3 || command -v python || command -v py)"   # CLAUDE.md: nhận CẢ BA tên
"$PY"  .claude/dev/packet_loop.py guard --action merge
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
