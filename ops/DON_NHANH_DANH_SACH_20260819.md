# Dọn nhánh remote — danh sách đối chiếu, ảnh chụp 2026-08-19

> **Số lượng KHÔNG nằm trong tiêu đề, có chủ đích.** Bản đầu tên là `..._10_NHANH_...` và
> chỉ trong hơn một giờ nó đã thành lời khai sai: `agent/w0-m2-g1-claude` bị xoá mất, còn 9.
> Nhét một con số trôi được vào tên tệp là tự hẹn ngày nói dối, nên bỏ hẳn.

**Tệp này là BẢN ĐỐI CHIẾU, không phải danh sách để xoá mù.** Thứ có thẩm quyền vẫn là
`scripts/don-nhanh.ps1` chạy trên máy có `gh` đọc được PR. Dùng tệp này để **so** với thứ
script in ra — khớp thì chạy, lệch thì dừng lại tìm hiểu, đừng tin bên nào trước.

## Neo phép đo

| | |
|---|---|
| master lúc đo | `a4d0e93e86d25057bc8061eaf0929beb35595ead` |
| đo lúc | `2026-08-19T10:00:55Z` |
| tổng nhánh remote | 103 |
| PR đang mở lúc đo | 11 (#161 #151 #145 #137 #127 #123 #110 #95 #94 #91 #78) |

**Master kho này nhích rất nhanh** — trong lúc làm việc hôm nay nó đi ~70 commit, có lúc
5–8 phút một PR. Nên ảnh chụp này **hết hạn nhanh**. Nếu ông chạy sau đây vài ngày thì cứ
tin script, và đọc tệp này như bối cảnh chứ không phải chân lý.

## 9 nhánh — đã merge trọn vào master, KHÔNG phải head/base của PR nào đang mở

```
agent/cg-t0-01-bundle-builder    58a21f7
agent/cg-t0-02-note-validator    b90481c
agent/gls-d1-g1-claude           96b24d0
agent/mp-t0-01-chatgpt-docs      f926835
agent/w0-m1b-g1-claude           6c84064
agent/w0-t1-g1-claude            2515ef2
ops/don-nhanh-giu-base-pr        35c63d0
ops/so-no-vong-3                 2845669
ops/tin-hieu-chan-som            d9faa14
```

Mỗi dòng đã kiểm bằng `git merge-base --is-ancestor <tip> origin/master` ⇒ **9/9 merged**,
soát lại lần cuối trên master `4262de4` lúc `2026-08-19T11:45Z`.
Commit không mất đi đâu khi xoá nhánh: chúng nằm trong master.

**Bản đầu ghi 10.** Nhánh thứ 10 là `agent/w0-m2-g1-claude` (`c97d741`) — đã bị xoá bởi ai
đó/cái gì đó trong khoảng 10:00Z–11:40Z, tức **hơn một giờ sau khi chụp**. Không phải đo
sai: nó đúng ở thời điểm đo, và sai ở thời điểm đọc. Đó chính là thứ mục "Neo phép đo" cảnh
báo, chỉ là nó đến nhanh hơn dự tính — giữ lại đoạn này làm bằng chứng sống cho lời cảnh báo
ấy thay vì lặng lẽ xoá một dòng.

## Chạy trên Windows

```powershell
# 1. THỬ KHÔ trước — không có -Xoa thì không xoá gì
.\scripts\don-nhanh.cmd

# 2. Chỉ khi đọc đúng như mục "Cách đọc" bên dưới
.\scripts\don-nhanh.cmd -Xoa
```

### Cách đọc kết quả thử khô

| script in ra | nghĩa là | làm gì |
|---|---|---|
| **10** nhánh, **không** dòng `CANH BAO` | `gh` đọc được PR, danh sách tin được | so với bảng trên; khớp thì `-Xoa` |
| có dòng `CANH BAO: … CHUA loai base cua PR dang mo` | `gh` **không** đọc được PR | **dừng**, sửa `gh auth` trước |
| **11** nhánh | gần như chắc chắn là ca `CANH BAO` ở trên | xem mục dưới — có một nhánh phải giữ |
| số khác hẳn 10 | master đã trôi xa khỏi ảnh chụp này | tin script, tệp này đã cũ |

Nếu `gh` không đọc được PR thì `-Xoa` sẽ **tự từ chối, thoát 13** — fail-close, không xoá
liều. Đó là hành vi ĐÚNG, không phải hỏng.

## Vì sao có bảng này: một ca lệch THẬT, đo được

Chạy thử khô trong container Claude Code (nơi proxy chặn `gh` đọc repo) cho **11** nhánh.
Nhánh thứ 11 là:

```
agent/w0-d3-g1-claude    — ĐÃ merge vào master, NHƯNG là HEAD của PR #161 đang mở
```

Xoá head của một PR đang mở thì GitHub **đóng PR đó**. Nó lọt vào danh sách chỉ vì lượt chạy
ấy không đọc được PR — chính script đã in `CANH BAO` báo đúng chuyện này, nên nó không hề
nói dối; nó nói "tôi chưa lọc được".

Danh sách 10 ở trên loại được nó vì phép đo dùng **MCP github** để hỏi PR (đường ấy chạy
được), thay vì `gh` (đường bị chặn). Cùng một câu hỏi, hai kênh, một kênh chết.

Trên máy ông `gh` đọc được PR ⇒ script tự loại nhánh ấy: nó nạp **cả `headRefName` lẫn
`baseRefName`** vào danh sách giữ (`don-nhanh.ps1` dòng 225), không chỉ base.

## Nhánh TUYỆT ĐỐI không được xoá — và vì sao

`mission/76/integration` là **BASE của 5 PR đang mở** (#151 #137 #127 #91 #78). Xoá nó là
đóng sạch năm PR, và tạo lại nhánh **không** mở lại chúng.

Đây đúng là lỗ mà **PR #150 sinh ra để vá**, và bản vá ấy đã land hôm nay (`6d8fce5`). Trước
#150 script chỉ đọc `headRefName` ⇒ nó sẽ coi `mission/76/integration` là "đã merge, xoá
được" và im lặng xoá. Nay nó giữ, và khi không đọc được PR thì từ chối thay vì đoán.

Ngoài ra 11 head của các PR đang mở cũng nằm trong danh sách giữ, cùng `master`.

## Kiểm lại bằng tay nếu muốn (không cần `gh`)

```powershell
git fetch --prune origin
git branch -r --merged origin/master        # lop 1: da merge
```

Lệnh trên **không** biết gì về PR — nó chỉ thay được lớp 1. Lớp 2 (giữ head/base của PR
đang mở) bắt buộc phải có nguồn dữ liệu PR; không có thì đừng xoá.

## Đã kiểm: xoá các nhánh này không làm mất bằng chứng

`ops/reviews/don-nhanh-base-review-6|7-claude-verdict.receipt.yaml` neo `evidence_url` vào
hai commit `ef0f906` và `a8c1d1d` trên nhánh `ops/don-nhanh-giu-base-pr`. Đã kiểm **cả hai
đều nằm trong master** sau khi #150 merge ⇒ xoá nhánh không làm chúng thành SHA không tra
được. (Bất biến này là thứ `ops-don-ref.yml` bảo vệ cho `luu-tru/*`; ở đây nó thoả nhờ
dòng dõi master, không nhờ tag.)

## Vì sao phiên web không tự xoá được

Đã đo cả ba đường, cùng ngày:

| đường | kết quả |
|---|---|
| `git push origin --delete` | **HTTP 403** — proxy egress chặn xoá ref |
| MCP github | có `create_branch`, **không có** tool xoá nhánh/ref |
| `.github/workflows/ops-don-ref.yml` | **từ chối TẤT CẢ** — mọi nhánh trong danh sách đều là `agent/*` hoặc `ops/*` |

`ops-don-ref.yml` từ chối bằng câu viết sẵn trong chính nó (dòng 197–198): *"thuộc vùng làm
việc được bảo vệ (ops/ claude/ codex/ agent/ mission/ dispatcher/) — **xoá phải do người,
không qua workflow**"*. Ba lớp độc lập cùng một kết luận, nên việc này là của ông trên máy
Windows, đúng như bàn giao đã ghi.

Một bẫy nhỏ đáng nhớ từ lượt đo: đầu ra của `git push --delete` **kết thúc bằng
`Everything up-to-date`** — đọc lướt tưởng xong, sự thật là `rc=1`. Đừng đọc dòng cuối.
