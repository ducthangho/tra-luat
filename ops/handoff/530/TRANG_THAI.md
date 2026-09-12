# `wp530` — TRẠNG THÁI, `17:1xZ 12-09-2026`

> Nhánh này là **hồ sơ**, không phải packet. Write set của `wp530` là **MỘT** đường
> (`ops/lease_publish_test.py`) và nó nằm ở nhánh `claude/cham-dot-bien-mien-nhiem-lease-suite`
> / PR **#532**. Đặt hồ sơ ở đây để write set giữ đúng một đường — tiền lệ `ops/handoff-512-luot7`.

## Vị trí (viết sao cho đúng ở CẢ HAI trạng thái của lần merge)

- **Bản vá**: tìm ở `master` trước; chưa thấy thì `git fetch origin claude/cham-dot-bien-mien-nhiem-lease-suite`.
  Thứ định danh là **BĂM** `a1c7d7ffbac710346400650b94e2d2a8035f62b5`, không phải tên nhánh —
  tên nhánh là thứ trôi và bị xoá.
- **Lease**: `ops/leases/cham-dot-bien-mien-nhiem-lease-suite-exec-1-claude-20260912.yaml`, nhánh
  `ops/cap-lease-530` commit `a119295`. Đã ĐĂNG — dấu `**Lease …**` ở #530 comment `5647137036`
  (`16:22:20Z`, `github-actions[bot]`), lượt `ops-publish-lease` `34704879950` = **success**.
- **Spec đóng băng rev 3**: `ops/specs/CHAM-DOT-BIEN-MIEN-NHIEM-LEASE-SUITE.md`, sha256
  `47c3b1fe70da6976cf802436fa8883c2ba48ac8f706b3d9ec103deaeb5f37778`, hiện ở nhánh
  `ops/handoff-512-luot7` (CHƯA trên `master`).

## Đang chờ gì

**`S2`.** `ADR-0044` cho packet `sensitive`: ≤ 3 tệp và ≤ **300** dòng thêm. Đo được **1 tệp / +802 −61**.
`ADR-0044` nói *"vượt ngưỡng thì dừng TRƯỚC review"*, nên PR #532 đứng ở **draft** và **chưa mở vòng
cross-review nào** (`review_rounds_used = 0`). Xin trần như tiền lệ `#504` (`nang_tran` `S2=1500`).

Phân rã, để quyết được bằng số thay vì cảm tính:

| loại dòng THÊM | số |
|---|---|
| chú thích (`#`) | 148 |
| trống | 67 |
| docstring (đo thô) | ~90 |
| **MÃ THUẦN** | **~497** |
| tổng | **802** |

⇒ Gỡ sạch mọi dòng văn thì **vẫn còn ~497**. Trần 300 **không đạt được bằng cách cắt văn**; nó là
kích cỡ **cấu trúc** của bản port. Cắt văn để lọt trần cũng là tối ưu hoá thước đo chống lại mục
đích của nó — mọi khối chú thích ở đây là bản ghi của một phép đo đã trả giá.

## Nghiệm thu — đo được, có tệp log kèm

| # | tiêu chí | kết quả | log |
|---|---|---|---|
| `A1` | 10 control | **10/10**, `rc=0` (bộ đo cũ `7/10`, `rc=1`) | `A5-wrapper-a1c7d7f.log`; lượt ĐẦU `8/10` ở `A1-t162-control-luot-DAU-8-tren-10.log` |
| `A2` | bất biến phân hạng ở ranh giới KÊNH | `XANH_DUNG`, `rc=[0,0]` · **chiều ngược**: `XANH_SAI`, `rc=[1,1]` ⇒ CÓ RĂNG | `A2-A3-A8-t163-tu-kiem.log` · `do-rang-cua-muc-A2.txt` |
| `A3` | gỡ chốt ⇒ ca đích ĐỎ | **6/6** mục `DO` | `A2-A3-A8-t163-tu-kiem.log` |
| `A4` | catalogue 16 mutant | mẫu số 16 · **giết 16** · không giết 0 · KDD 0 | `A4-t161-catalog-16.log` |
| `A5` | suite đầy đủ, CHA + `[A]` + `[B]` | **158/158** đạt, bỏ qua 0 — đúng **3** dòng; 0 dòng `ĐỎ`; `WRAPPER_RC=0` | `A5-wrapper-a1c7d7f.log` |
| `A6` | `doctrine-scan` · `adr-song` | `rc=0` (7 tệp, 0 chỗ chép) · `rc=0` (48/48) | — |
| `A7` | dòng thêm ≤ trần | **KHÔNG ĐẠT** — xem trên | — |
| `A8` | `rc` kênh lệch rc thật ⇒ KDD | `dong-luot-ghi-rc-0-cung` ⇒ `GIET` | `A2-A3-A8-t163-tu-kiem.log` |

**Điều kiện đo, nói ra vì một con số không ghi điều kiện thì sẽ trôi mà không ai biết:**
`shellcheck 0.9.0` **CÓ MẶT** và `actionlint 1.7.7` ghim trên PATH (`AL_GOI=/tmp/actionlint/goi.gz`).
Thiếu `shellcheck` thì `t137`/`t159` fail-close `KHÔNG ĐO ĐƯỢC` — đó là nền đo, không phải hồi quy.

## Chi phí thời gian — đo DELTA hai vế trong MỘT lệnh

`do-delta-chi-phi-hai-ve.sh` dựng **cả hai** vế trong một lệnh, hai vòng lặp, cùng các bước, chạy
liền nhau (`clone` + `checkout --detach` + `core.abbrev 7`), vì dựng hai vế ở hai thời điểm là mở cửa
cho môi trường trôi giữa chừng.

| vế | sha | ca | tổng giây | `t125` |
|---|---|---|---|---|
| nền | `dc02c9b` | 155/155 | **104.4** | 53.0s |
| sau | `a1c7d7f` | 158/158 | **319.4** | 160.4s |

⇒ **+214.9s (×3.06)**, trong đó `t125` một mình **+107.4s** vì hai lượt con LỒNG của nó cũng chạy
ba ca mới. Đặc tả khai chi phí kênh là `chưa đo`; nay đã đo, và khai thẳng vì `#463` đang cắt chi phí
CI. Có một đường giảm rõ (đừng chạy ba ca mới trong hai lượt con của `t125`) nhưng nó **đổi phạm vi
`t125`** ⇒ là câu hỏi thiết kế cho reviewer/chủ kho, phiên thi công **không tự quyết**.

**Bản đầu của phép đo này không đo gì và vẫn trông như thành công**: nó gọi
`/usr/bin/env time -f` mà container KHÔNG có GNU `time`, nên mỗi vế chết ngay, log còn **1** dòng,
script in ra bình thường và báo `so ca chay: 0`. Đúng bệnh *"rc=0 + output rỗng"*. Bản hiện tại có
**chốt DƯƠNG**: thiếu dòng tổng kết thì in `KHÔNG_DO_DUOC` và thoát khác 0.

## Ba chốt phải dựng, mỗi chốt do một phép đo bắt được — không do đọc code

1. **Phép cắt bảng (ba vùng).** Catalogue nay NẰM TRONG tệp bị đột biến nên mỗi neo xuất hiện ít nhất
   hai lần. Lượt chạy ĐẦU: **2/10** control ĐỎ vì `neo khớp 3 lần` / `2 lần`. Cắt RIÊNG từng bảng
   (cắt rộng tạo vùng mù thật) + tự kiểm CẤU TRÚC.
2. **Neo phải ghim CỘT.** `"        except TinHieuChotCa as ex:"` (8 dấu cách) là **chuỗi con** của
   bản 12-dấu-cách trong `t159`. **5/6 → 6/6** sau khi ghim bằng một ký tự xuống dòng dẫn đầu.
3. **Kênh không được thừa kế xuống CHÁU.** Với mutant `bo-chot-selector-khong-khop`, lượt con của
   `t155` chạy trọn 157 ca và ghi tiếp vào đúng tệp kênh của cha — sau cả bản ghi đóng lượt ⇒
   `KHÔNG ĐO ĐƯỢC` cho một mutant ĐÃ BỊ GIẾT THẬT (`giết=15, KDD=1`). Sau khi vá: **16/16**.

## Hai lời khai của chính phiên này bị chỉnh, ghi cả câu SAI

1. **"hai chốt vật hoá `dich` là ĐỘC LẬP"** — SAI. Đo riêng từng nửa (`do-vat-hoa-tung-nua.txt`):
   gỡ nửa nào cũng `rc=0`, **0** control lệch (nửa còn lại HẤP THỤ); chỉ gỡ **cả hai** mới `rc=1` và
   control dương lệch `GIET → KHONG_GIET`. ⇒ một bộ **TƯƠNG ĐƯƠNG**, mục `M5` ấy đo **đúng một** thứ.
2. **`A2` ở commit `540b6f1` chỉ nằm trong docstring** — tức nó **KHÔNG TỒN TẠI**. Commit `a1c7d7f`
   biến nó thành ca chạy thật **và** đo chiều ngược. Đúng lỗi *"nghĩ ra được phép thử mà KHÔNG CHẠY
   nó thì phép thử ấy không tồn tại"* — mắc ngay trong một packet mà toàn bộ nội dung là về việc bộ
   đo nói dối.

## Chưa đo được — khai, không lấp

1. **Chống giả mạo tín hiệu bởi mã CÙNG interpreter** — kênh bảo vệ khỏi một **tập lỗi khai tường
   minh**, không khỏi mã sửa thẳng trạng thái khung. Kế thừa **nguyên** giới hạn của `#513`.
2. **Windows** — `full CI` và `CI Windows` chỉ đến khi merge; trước đó chúng **không tồn tại** cho
   mã này. Đừng đọc Linux `158/158` thành một kết luận về Windows.
3. **9 chốt fail-close của bộ chấm chưa có control phân biệt** — khai trong
   `CHOT_CHUA_CO_CONTROL_512`, **không** đếm là đã đo. Đặc tả đóng băng mẫu số control ở 10, nên
   thêm control là việc của một revision, không phải của phiên thi công.
4. **`review_rounds_used`** vẫn là đếm TAY — nợ `SO-CANON-CHUA-TON-TAI`, `0` tệp canh trần vòng.
