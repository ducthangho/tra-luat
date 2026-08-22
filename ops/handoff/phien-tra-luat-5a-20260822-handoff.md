# Bàn giao — phiên `tra-luat-5a`, 22-08-2026

**Vai:** điều phối + soạn tài liệu. **KHÔNG** phải executor của packet nào ⇒ bản này **không** theo
schema §7 (`ops/handoff/wp55-r4g1-handoff.md` mới là bản §7 thật). Không có `generation`, không
`attempts_used`, không head để review.

**Tiếp nối:** `ops/handoff/phien-dieu-phoi-20260821-handoff.md` (đã trên master). Bản đó vẫn đúng cho
phần lịch sử; bản này chép tiếp từ chỗ nó dừng.

**Trạng thái:** không việc nào đang dở. Một hẹn tự động đang chạy (§5).

---

## 1. Neo

```yaml
# Đo cùng lúc, trên cùng một commit. Đừng vá lẻ từng trường.
do_luc: '2026-08-22'
master: 3f64167                    # = origin/master lúc bàn giao
nhanh_lam_viec: claude/opus-5-plan-steps-y5r6ci   # đã hết việc, reset về master
pr_da_merge: 230
pr_dang_mo_lien_quan: [233, 234, 229]
hen_dang_chay: trig_0171iMNPHfQSn58J4VmPm6h1     # 06:00Z, kiểm #227
```

## 2. Phiên này đã làm gì

| # | việc | kết quả |
|---|---|---|
| 1 | Vá bốn con trỏ chết trong tài liệu có thẩm quyền | **PR #230 MERGE**, master `3f64167`, 8 tệp |
| 2 | Dán hộp ⛔ lên đầu `ops/specs/plat-x8.md` | bản **3b**, băm `308d0cf4…` |
| 3 | Ghi nợ mục **12** `PLAT-X4-721-dong-chua-verdict-nao-phu` | sổ nợ nay **12** mục |
| 4 | Đính chính append-only câu *"vòng 3 đã lấp chỗ ấy"* | trong `ops/THAM_DINH_KE_HOACH_20260821.md` |
| 5 | Viết bản giao việc hoàn thiện kế hoạch | `ops/prompts/phien-hoan-thien-ke-hoach-20260822.md` |
| 6 | Điều phối với phiên `session_018YdsqSNdxorwxVYW2d2PkH` (PR #233) | đã hồi âm, đã cam kết phạm vi |

Lượt master sau merge (`32552166181`) **xanh cả hai nền**, đo tới từng bước: `gate (windows-latest)`
28 bước chạy thật ~8 phút; `gate (ubuntu-latest)` 5m47s. Bốn bước `skipped` đều có điều kiện, ba cặp
skip **ngược nhau** giữa hai nền. **Việc Windows không còn treo.**

## 3. BỐN LẦN PHIÊN NÀY ĐO SAI — chép ra vì cả bốn cùng một họ

Cross-review (auto-review connector, 4 lượt trên #230) ra **chín** finding thật. Sáu cái là số trôi
theo thời gian. **Bốn cái dưới đây là phép đo SAI của chính phiên**, và đều đã được báo cho người
giữ kho **trước khi** bị bác — nên đính chính nằm trong chính các tệp đã land, không chỉ trong hội thoại.

| # | tôi khai | sự thật đo được |
|---|---|---|
| 1 | *"protocol KHÔNG có canon 2 vòng"* | **SAI.** `docs/PROTOCOL_DA_PHIEN.md:543` và `:561` có sẵn trần 2 lượt Codex/PR |
| 2 | *"`spec_sha256` 11/49 lease"* | **SAI.** Đếm chuỗi con, gộp hai lược đồ: `spec_sha256:` = **5**, `spec_sha256_required:` = **6** |
| 3 | *"X4 cấp HAI lượt review, không verdict ở đâu"* | **SAI.** **BA** lượt; kết quả lượt 1+2 là `changes_requested`, ghi trong **thân lease của lượt kế tiếp** |
| 4 | *"nhánh #227 đứng yên ⇒ executor có thể đã dừng"* | **SAI.** Họ đẩy sang nhánh **khác tên** (`land/227`) và đã mở **PR #234** |

**Họ chung:** cả bốn đều là *hỏi chỗ tiện tay thay vì hỏi chỗ kết luận được ghi*. (1) và (2) là grep
lỏng; (3) đọc `ops/reviews/` rồi kết luận về lịch sử review; (4) neo vào một **tên nhánh tự suy ra**.

**Chốt rút ra, đã áp:** đo bằng **hiện vật** và **khoá chính xác**, không bằng tên/chuỗi con/tín hiệu
gần nhất. Và trong tài liệu thì **bỏ số ghi cứng, thay bằng lệnh đo sống** — PR #230 ăn ba finding
chỉ vì số ghi cứng chết ở commit kế tiếp, ba lần trong cùng một PR.

## 4. Hai con số tôi đã báo người giữ kho mà sau đó bị bác — đọc kỹ

- **"Mục D là hai field"** — hụt **hai bậc**. Đo lại: **49** lease dùng **230** tên trường mức gốc,
  `ops/lease_publish.py` nhắc **8**, còn **222** không ai kiểm. Phiên #233 đo ra 215/8/**207** —
  cột giữa **khớp tuyệt đối**, tổng lệch **15**, chưa ai phân định. Kết luận chịu tải không đổi: mục D
  là một **quyết định phạm vi**, không phải bản vá hai dòng. Phiên #233 đã cắt thành D1–D4.
- **"Protocol im lặng về trần review"** — sai (xem §3.1). Chỗ hở thật, do phiên #233 tìm ra và
  **mạnh hơn** cách tôi đóng khung: protocol mang **HAI** con số mà không nói cái nào thắng —
  `:750` *"hai lượt Codex"* ↔ `:751` *"BA vòng code/review tổng cộng"*. Cộng dòng 7 trỏ ADR bằng một
  **phạm vi đã chết** (`ADR-0017 đến ADR-0035`, trong khi có 45 ADR).

## 5. Việc duy nhất còn treo — `PLAT-X8` bản 4

Chờ **#227** land. Đo 05:07Z: **chưa** (master `0` hàm mới · `RC_` = 6 · 39 ca). Đường land là
**PR #234** (`land/227`, head `86788eb4`, mở 04:59Z) — `gate (ubuntu-latest)` **FAILURE**, chết ở
**bước 10 `lease-publish selftest`**, 18 bước sau `skipped`.

**Không vá hộ:** không có lease trên `ops/lease_publish*`, và lease `#227` còn hiệu lực tới
**23-08T01:00Z**. Đó là việc của executor `#227`.

Hẹn `trig_0171iMNPHfQSn58J4VmPm6h1` (06:00Z) mang **tiêu chí đã sửa**: đo hiện vật trên master +
quét **tập PR đang mở** theo NỘI DUNG; **không canh tên nhánh**. Kèm ba đường thoát để không hẹn vô hạn.

Khi #227 land: sáu chỗ phải sửa cho bản 4 nằm sẵn trong **hộp ⛔ ở đầu `ops/specs/plat-x8.md`**.
Kèm gỡ hộp, thêm hàng `4` vào bảng phiên bản, và cập nhật **cả bốn** chỗ trích băm còn sống. **Hai
bảng LỊCH SỬ giữ nguyên băm cũ.** Trước khi đổi băm: `grep -rl plat-x8 ops/leases/` phải RỖNG.

## 6. Cam kết phạm vi với phiên #233 — GIỮ ĐÚNG

Phiên `session_018YdsqSNdxorwxVYW2d2PkH` (PR #233) đang làm protocol §20 (bảng **định tuyến** ADR, do
máy canh) và `ops/HOAN_THIEN_KE_HOACH_20260822.md`. Tôi đã hồi âm và cam kết **không đụng**:

- `ops/NO_KY_THUAT.md` — họ dùng §13/§14, cố ý chừa §12 cho tôi (đã land ở #230, ráp sạch)
- `docs/PROTOCOL_DA_PHIEN.md`
- `docs/adr/**`

**#233 CHƯA sắp merge:** codex ra 2 P2 chưa vá (`ADR-NNNN` trong khối mã có rào / comment HTML vẫn bị
tính là metadata sống ⇒ `adr-song` trả `rc=0` sai; và regex tên tệp siết hơn văn bản mô tả).

## 7. Còn mở, không ai đang làm

| thứ | trạng thái |
|---|---|
| `PLAT-X8` (#225) | `state:proposed`, **0 lease**. Lease cũ đã cấp rồi **RÚT** (`c7bb945`), chưa từng đăng |
| `PLAT-X6` (#209) | `state:ready`, **0 lease** — sổ nợ `required-status-check` + đảo `t34` |
| `PLAT-X7` (#220) | `proposed`, chưa spec — đo danh tính model, `depends_on: [PLAT-X8]` |
| PR #229 | `ops/HANG_DOI_PACKET.md` — một chỗ duy nhất cho THỨ TỰ packet, chưa merge |
| nợ `SO-LEASE-KHONG-NAM-MOT-CHO` | chưa có lệnh `ai-dang-giu` |
| nợ mục 12 | verdict lượt 3 của X4 **không có hiện vật ở đâu**; và lease lượt 3 khai sai rằng lượt 1+2 *"có verdict trong `ops/reviews/`"* (ở đó có **0** tệp X4) |

**Một manh mối chưa phân định, đừng đọc thành kết luận:** `mergeable_state` của PR #230 đổi
`clean` → `blocked` đúng lúc cổng chuyển `success` → `in_progress`, rồi về `clean` khi cổng xanh lại.
GitHub trả `blocked` khi **branch protection** chặn, `unstable` khi check **không bắt buộc** đang chờ.
Ta nhận `blocked`. Đó là bằng chứng gián tiếp rằng branch protection **có đòi một thứ gì đó** — nếu
thứ ấy là job `gate` thì nó đụng **Q7** (đã trả lời *"KHÔNG BẬT"*) và nợ thường trực `§9`. **Chưa đo
được** vì REST tới `/repos/<kho>` bị proxy chặn 403 từ container này. Cách phân định: so
`mergeable_state` trên một PR **không có review nào** khi cổng đỏ.

---

**Đọc được bản này KHÔNG phải là được giao việc.** Handoff không phải lease (`docs/PROTOCOL_DA_PHIEN.md` §7).
