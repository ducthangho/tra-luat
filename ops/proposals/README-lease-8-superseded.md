# Đề xuất: đánh dấu lease lượt 8 là ĐÃ BỊ THAY THẾ

**Trạng thái:** CHƯA ÁP. Soạn để chủ kho duyệt. Tệp lease trên nhánh
`ops/wp55-r3-review-8` vẫn nguyên trạng.

**Áp bằng:**

```bash
git checkout -B ops/lease-8-superseded origin/ops/wp55-r3-review-8
git apply ops/proposals/lease-8-superseded.diff
python3 ops/lease_publish.py check ops/leases/wp55-r3-review-8-codex-20260815.yaml   # ĐÒI rc=9
git add ops/leases && git commit -m "ops: danh dau lease luot 8 superseded boi luot 9"
git push -u origin ops/lease-8-superseded
```

## Diff làm gì

Thêm vào `ops/leases/wp55-r3-review-8-codex-20260815.yaml`, **không xoá dòng nào**:

| | |
|---|---|
| khối chữ ở đầu tệp | biển báo "ĐÃ BỊ THAY THẾ — ĐỪNG NHẬN VIỆC THEO NÓ" |
| `active: false` · `status: superseded` | trường máy đọc |
| `superseded_by` | `wp55-r3-review-9-codex-20260815` |
| `superseded_by_decision_of` + `_basis` | `ducthangho`, chỉ thị trực tiếp trong phiên |
| `superseded_reason` | tip nhánh rời khỏi `reviewed_sha_required` |
| `superseded_work_done: false` + note | KHÔNG có verdict nào nộp theo lease này |

Đặt ngay sau `event`, **không** nhét cuối tệp: ai đọc lease để nhận việc thì đọc từ
trên xuống, và "còn hiệu lực hay không" phải đập vào mắt trước mọi trường khác.

## Ba điều phải biết trước khi duyệt — đã ĐO, không phải suy đoán

**1. Cổng KHÔNG biết khái niệm `superseded`.** Đã grep `ops/lease_publish.py` và
`ops/lease_publish_test.py`: không có `superseded`, `active`, `revoked`. Cổng chỉ chặn
theo `lease_expires_at_utc` và `posted_comment_id`. Nên `active: false` **tự thân không
chặn được gì** — nó là bản khai cho người đọc, và là mỏ neo sẵn cho lần cứng hoá sau.

Muốn cổng chặn thật thì phải sửa `lease_publish.py`. Đó là thay đổi RIÊNG, cố ý không
gộp vào đây: sửa cổng là sửa thứ đang canh mọi lease, phải có bộ test và lượt review
của riêng nó.

**2. Bản chiếu trên #55 SẼ KHÔNG tự cập nhật.** Đo được:

```
$ python3 ops/lease_publish.py check ops/leases/wp55-r3-review-8-codex-20260815.yaml
CHAN [9]: lease 'wp55-r3-review-8-codex-20260815' đã đăng (comment 5301410944) — bỏ qua
rc=9
```

Workflow thấy `rc=9` thì `continue`, không đăng lại. Comment `5301410944` vì thế vẫn
hiển thị lease như lúc mới cấp, **không** có biển báo. Đây là hệ quả đã biết của thiết
kế "đăng một lần", không phải lỗi của bản vá.

Muốn bản chiếu khớp thì phải làm THÊM một trong hai, và cả hai đều cần chủ kho:

- sửa tay comment `5301410944` trên #55; hoặc
- đăng một comment mới trỏ về tệp này.

Ghi ra đây để không ai tưởng push xong là xong.

**3. YAML vẫn phân tích được và bộ test cổng vẫn xanh.** Đo trên bản đã áp diff:

```
YAML phân tích được, 65 trường
  active                = False
  status                = 'superseded'
  superseded_by         = 'wp55-r3-review-9-codex-20260815'
lease_publish: 30/30 đạt
```

## Vì sao phiên executor không tự áp

Sửa một lease ĐÃ CẤP là thao tác thuộc thẩm quyền §2 (`start/pause/resume/reroute/
override/authorize`), không thuộc vai executor. Phiên này chỉ soạn và đo.

Thêm một lý do cụ thể của lượt này: chính phiên executor là bên gây ra tình huống —
đẩy `3c4fbc2` và `4270210` vào nhánh packet khi lease lượt 8 đang neo `91780cb`. Bên
gây ra sự việc không nên tự tay đóng hồ sơ về sự việc ấy.
