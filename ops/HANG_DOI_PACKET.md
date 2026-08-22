# HÀNG ĐỢI PACKET — nguồn duy nhất cho THỨ TỰ

**Cập nhật 22-08-2026.**

> **Đọc được tệp này KHÔNG phải là được giao việc.** Nó là DỮ LIỆU. Thứ giao việc là Packet Issue
> kèm lease còn hiệu lực (`docs/PROTOCOL_DA_PHIEN.md` §3.2 và §4). Phiên nào tự chọn một dòng ở đây
> rồi bắt tay làm là tự cấp việc cho mình.

## Vì sao có tệp này

Thứ tự packet trước nay sống trong **bản bàn giao phiên** (§5 của
`ops/handoff/phien-dieu-phoi-20260821-handoff.md`), trong **comment Issue**, và trong **thân PR**.
Cả ba đều là chỗ TRÔI: bản bàn giao chết theo phiên, comment bị đẩy xuống dưới, thân PR đóng lại
sau khi merge. Đo 22-08-2026 trước khi tạo tệp này: `PLAT-X8` xuất hiện trong **0** tệp
`KE_HOACH_*`, `#227` cũng **0**. Nghĩa là thứ tự đã chốt của bốn packet đang tranh nhau hai tệp
**không tra được ở đâu cả**.

Cùng hình dạng với `SO-LEASE-KHONG-NAM-MOT-CHO`: thứ ta cần tra không có MỘT chỗ để tra, nên ai
cũng hỏi chỗ tiện tay.

**Họ `PLAT-X*` không thuộc kế hoạch nào** — khác `PLAT-M*` (nằm ở
`ops/KE_HOACH_DIEU_CHINH_DA_NEN_TANG.md` §7) và khác `W0-*`/`W1-*` (nằm ở
`ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md` §6). Chúng sinh ra từ các phát hiện rời của cross-review và
human audit. Đó là lý do không thể "ghi vào kế hoạch sẵn có": không có kế hoạch nào chứa chúng.

## TRA BẰNG SỐ ISSUE, KHÔNG BẰNG `packet_id`

`PLAT-X6` từng trỏ **hai** Issue (#209 và #220) cho tới khi #220 được đổi thành `PLAT-X7` bằng đính
chính **nối thêm** ngày 21-08. Tài liệu cũ vẫn ghi `PLAT-X6` cho **cả hai nghĩa** — trong đó
`ops/prompts/plat-x5-review-2-claude-20260820.md`, `ops/KE_HOACH_THI_CONG_ANTIGRAVITY.md`, hai lease
`ag-t0-01b-exec-*`, và `ops/specs/ag-t0-01b-r*.md`. Số Issue là thứ không nhập nhằng.

## Hàng đợi — lane `ops/lease_publish*`

Bốn thứ cùng đòi `ops/lease_publish.py` và/hoặc `ops/lease_publish_test.py`. Xử bằng **THỨ TỰ**,
không bằng thu hồi.

```
#227  LEASE-DANG-DUNG-MOT-LAN   ← ĐANG CHẠY
  │
#225  PLAT-X8
  │
#209  PLAT-X6
  │
#220  PLAT-X7
  │
mục D  gói spec-gate            ← chưa mở Issue
```

| # | packet | trạng thái 22-08 | vì sao đứng sau cái trên |
|---|---|---|---|
| #227 | `LEASE-DANG-DUNG-MOT-LAN` | executor `codex`, đặc tả bản sửa đổi 2, review lượt 1 ra `can_sua` | đang giữ lease còn hiệu lực trên **cả hai** tệp tới `22-08T13:30Z`; nhánh `codex/lease-dang-exec-1` đã có mã thật |
| #225 | `PLAT-X8` | **chưa có lease** — bản cấp 21-08 đã RÚT (`ops/RUT_LEASE_PLAT_X8_20260821.md`) | va chạm nội dung với #227: cùng sửa `kiem()`, cùng khối hằng sau `RC_NEO`, cùng `BAT_BUOC` |
| #209 | `PLAT-X6` | `state:ready`, **0 lease** | đòi `ops/NO_KY_THUAT.md` + `ops/lease_publish_test.py` |
| #220 | `PLAT-X7` | `proposed`, chưa có đặc tả, **0 lease** | phải khai `depends_on: [PLAT-X8]` — hướng chốt *"với `review_class: sensitive`, cổng từ chối cặp cùng họ model"* **tiêu thụ** lớp review hiệu lực mà `PLAT-X8` **sản xuất** |
| mục D | gói spec-gate | chưa mở Issue | chốt `spec_path`/`spec_sha256`/timestamp — `ops/specs/plat-x8.md` §4.4 xếp ngoài phạm vi |

### Lane KHÁC, không va — đừng gộp vào hàng đợi trên

| # | packet | write set | ghi chú |
|---|---|---|---|
| #219 | `AG-T0-01B` | `.claude/dev/launcher.py` + `_test.py` | nền Google Antigravity; lease `ag-t0-01b-exec-1r2` hiệu lực tới `23-08T02:05Z`. Không chạm `ops/lease_publish*` |

## Việc BẮT BUỘC trước khi cấp lease cho bất kỳ dòng nào

1. **Quét lease trên MỌI nhánh `ops/**`, không chỉ `master`.** Lease sống trên nhánh `ops/**` và chỉ
   về master sau khi merge, nên master luôn thiếu đúng những lease mới nhất. Đã trả giá: lease
   `PLAT-X8` được ký với cửa sổ chồng lấn ~23,75h vì phép đo chỉ hỏi master. Chưa có công cụ —
   nợ `SO-LEASE-KHONG-NAM-MOT-CHO`.
2. **Phân biệt "chưa hết hạn" với "còn hiệu lực".** Không trường nào trong tệp lease nói nó đã tiêu,
   và trạng thái Issue **không** trả lời được: đo 22-08, `#206` `#215` `#225` `#227` đều còn `open`
   trong khi hai packet đầu đã land. Phải đi tìm **hiện vật** của packet trên master. Ba trạng thái,
   không phải hai: `còn hiệu lực` · `đã tiêu` · **`không xác định được`** — và cái thứ ba phải làm
   người cấp lease DỪNG LẠI.
3. **Va chạm NỘI DUNG có thể tồn tại ngay cả khi cửa sổ không chồng.** Dời hiệu lực chỉ chữa cửa sổ.
   Nếu packet đứng trước đang sửa cùng hàm / cùng vùng, packet sau vẫn phải rebase và đo lại — xem
   `ops/RUT_LEASE_PLAT_X8_20260821.md` để biết cách đo.

## Điều kiện rời hàng đợi

Một dòng chỉ được xoá khỏi đây khi **hiện vật của nó có trên `master`** — không phải khi PR merge
(merge có thể bị revert), không phải khi Issue đóng (đo được: Issue đóng/mở không phản ánh trạng
thái land), và không phải khi ai đó tuyên bố xong.

## Cập nhật tệp này khi nào

Mỗi lần thứ tự đổi, mỗi lần một packet land, mỗi lần một Issue đổi định danh. Nếu bạn đang viết thứ
tự packet vào một **bản bàn giao**, một **comment**, hay một **thân PR** — hãy viết vào đây TRƯỚC,
rồi trỏ về đây. Đó chính là lỗi tệp này sinh ra để sửa.
