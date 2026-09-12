# EVIDENCE — vòng review 10, PR #512 / packet #504. **Vòng CUỐI trong trần.**

Mọi con số là **lời khai**; việc của bạn là **ĐO LẠI**. Vòng 9 bác bốn lời khai của tôi và **đúng cả
bốn** — nên đừng nhân nhượng với tệp này.

## Neo — write set KHÔNG đổi một byte kể từ vòng 7

| | |
|---|---|
| `reviewed_sha` | `36f68c7e95e0de1fcf8e2311db33a164816db20f` — y hệt vòng 7, 8, 9 |
| base / `merge-base` | `bb7013c7669da19304a8769e5b25f8c1f8951e9c` |
| write set exact | `ops/lease_publish_test.py` · `ops/chay_lease_publish_test.sh` |
| lease | `windows-lease-suite-exec-2-claude-20260912`, gen 2, hết `2026-09-13T14:22:00Z` |
| vòng | **10** — **trần**. Hết vòng này mà còn `P1`/`P2` thì packet DỪNG và hỏi chủ kho. |

**Không có thay đổi mã nào trong PR** kể từ vòng 7. Kiểm điều đó trước.

## Vòng 9 kết gì — và tôi đã sửa gì

Vòng 9: `so_p1_trong_write_set: 0`, `so_p2_trong_write_set: 0`; full suite **độc lập** `155/155` ở
**CHA · `[A]` · `[B]`**; `F1 F2 F3 F4 F5 F7` giữ `ĐÃ VÁ THẬT`. Bốn finding **đều ngoài write set** và đều
nhắm vào **hồ sơ / luận cứ** của tôi. Tất cả đã đính chính **bằng hồ sơ**, không sửa byte hiện vật lịch sử.

| ID vòng 9 | tôi từng khai | nay ghi |
|---|---|---|
| `F6.11` | `main()` in **hai** hình dạng; `v6` lọt `4/4`, `v8` bắt `4/4` | `main()` có **BA** nhánh `except`; `BoQuaNen` đi nhánh riêng in chuỗi **cố định** ⇒ **lọt cả hai bản**; `TinHieuChotCa` là con `AssertionError` ⇒ cũng lọt cả hai, **và đếm nó vốn đã SAI vì nó LÀ lớp tín hiệu**. `v8` loại **2/4**. Trên **ba** lớp vô can thật: `v6` lọt `3/3`, `v8` lọt `1/3`. |
| `F6.12` | hồi quy `v8` **có biên** `8/454`, 4 ca | Mẫu số **493**; `454` là tập tiền tố **TĨNH**. Trong **39** lời gọi tiền tố ĐỘNG bị bỏ có **21** mang hình dạng va chạm `f"{x}: …"` trên **7 ca nữa** (`t23 t26 t27 t126 t127 t131 t133`) ⇒ **≥29 / ≥10 ca**. **RÚT** lời khai "có biên": cả hai bản đều **không có biên**, chỉ ngược chiều. |
| `N40` | vòng 8 dài `813 s` | **`812 s`** |
| `N42` | exclusion `#513` là *"`#504` giữ"* | tệp spec ghi **`#503`**, lease `m9-fetch-auth-exec-1-claude-20260911`. Kèm: **thân Issue `#513` ghi `#504` còn tệp spec ghi `#503`** — hai hiện vật lệch nhau, đã khai ở #530 |
| `F9.1` | `A2` của spec `#530` đòi *"va chạm chuỗi về 0"* | **đo sai đại lượng**; `A2` nay đòi **phân hạng không đổi khi mọi thông điệp chốt thành RỖNG** |

**Nguyên nhân gốc của `F6.11` + `F6.12` là MỘT, và tôi khai thẳng:** tôi khớp regex với một **chuỗi TỰ
GHÉP** (`f"{ten}: m"`) thay vì **chạy lớp ngoại lệ thật qua `main()`**. Đúng lỗi *"nghĩ ra được phép thử
mà KHÔNG CHẠY nó thì phép thử ấy không tồn tại"*, mắc ngay trong một packet mà toàn bộ nội dung là về
việc bộ đo nói dối. Spec `#530` **revision 2** nay đặt thành ràng buộc: **mọi tiêu chí nghiệm thu phải
chạy qua `main()` THẬT**.

`N42` cùng thói: chép số từ **thân Issue** rồi **quy cho tệp spec**, không mở tệp spec ra đọc.

## Lựa chọn bộ đo — lý lẽ đã viết lại, và nó YẾU HƠN trước

`v8` **giữ** làm mặc định (vòng 9 **không** đòi lùi `v6`). Nhưng cơ sở còn lại chỉ là **một MẪU đã đo**:
trên ba lớp vô can thật, `v8` lọt `1/3` so `v6` lọt `3/3`. **Không** còn lập luận "có biên". Nếu bạn thấy
một chiều nào chưa ai đo mà `v8` tệ hơn `v6`, đó là finding.

Ba bản trong `do-cua-tac-gia/`: `dotbien512.py` (`v8`, MẶC ĐỊNH) · `dotbien512_VA_VONG6.py` (`v6`) ·
`dotbien512_REGEX_CU.py` (`v0`). **Bộ đo được giao ở trạng thái TỰ BÁO ĐỎ** — `--tu-kiem` ⇒ `7/10`,
`rc=1` — **cố ý**, vì bộ control kèm cả ba ca nó xử sai.

## Đã đo trên `36f68c7` — kèm ĐIỀU KIỆN ĐO

| phép đo | kết quả khai |
|---|---|
| suite đầy đủ | `155/155 đạt; đã chạy=155, bỏ qua=0` ở `[A]` (log 1055) · `[B]` (1060) · CHA (1156); **0** dòng `  ĐỎ  `; rc=0 |
| `t125` · `t158` · `t160` ở CHA | `55.445s` · `3.381s` · `0.066s`, QUA |
| catalogue 16 đột biến (bộ đo mặc định, 10 control) | `16/16 giết thật, 0 tín dụng giả, 0 sống sót`, rc=0, **không ca nào đổi phân hạng** |
| `doctrine-scan` · `adr-song` | rc=0 `7 tệp / 0 chỗ chép` · rc=0 `47 ADR / 47 dòng §20` |
| `numstat` 2 đường so `bb7013c` | **+1101 / −27** (`1095 + 6`) |

**ĐIỀU KIỆN ĐO của `155/155`:** `actionlint 1.7.7` + **`shellcheck 0.9.0`**, Linux, python 3.11.15.
Thiếu `shellcheck` ⇒ `t137`/`t159` ĐỎ với `KHÔNG ĐO ĐƯỢC` — **fail-close đúng thiết kế**. Log **cả hai**
lượt trong `do-cua-tac-gia/`.

## `KHÔNG ĐO ĐƯỢC` — đừng đọc thành ĐẠT

- **`A3`/`A4` Windows**: không lượt Windows nào chạy trên head này. Chỉ thị chủ kho: **không CI bằng
  tay**; `full CI` và `CI Windows` **chỉ đến khi merge**. Linux `155/155` **không** chứng nhận Windows.
  Mốc thời gian Windows trong docstring (`N07`, `N11`–`N15`, `N17`, `N18`, `N30`) **thiếu log nguồn**.
- **Chống giả mạo tín hiệu của bộ đo**: `KHÔNG ĐO ĐƯỢC` đầy đủ — đó là lý do packet `#530` tồn tại.
- **`S8-bo-deadline`**: gốc trong `ops/lease_publish.py`, ngoài write set (`S3`).
- **`A5`**: `KHÔNG ĐẠT` — `1101 > 300`; override `1500` **không** đổi nhãn nghiệm thu đóng băng.
- **Lượt workflow đăng lease gen 2 ĐỎ** (`run 34699156658`): workflow lặp qua **mọi** tệp lease đổi trong
  push; tệp gen 1 (chạm chỉ để mang bia mộ) bị từ chối **đúng** vì đã hết hạn. Nợ mới, đã khai;
  `.github/workflows/**` ngoài write set.
- **Thông điệp commit `a65415d`** mất một cụm vì heredoc **không trích dẫn** biến dấu nháy ngược thành
  thay thế lệnh. Đã đính chính bằng commit `02fd817`, **không sửa byte**.
