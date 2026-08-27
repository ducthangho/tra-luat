# `MCP-GH-CUU-HO` (#319) — KIỂM ĐỘC LẬP bản vá lease r6

**Không phải verdict review.** Phép đo của phiên điều phối, chạy lại bằng tay thay vì chuyển tiếp
báo cáo của executor.

- Neo: `f461413a03b3a28ebdacde1fa17f49c894223682` (đã commit, đã đẩy).
- Base: `ac82ddc583f688d54bdc60e06922ec09bdab9f16`. Executor `codex xhigh`, run `ae038f02`, 1058s.
- Ngân sách: `230 + 670 = 900/900`. Thêm ròng **24/24**. Biên còn **0**.

## Kết luận một dòng

Bản vá **ĐÚNG HƯỚNG và đã đóng phần cốt lõi của P1**, nhưng **bàn giao ở trạng thái ĐỎ** và còn
**hai dòng không có phản chứng**. Cả hai điều kiện dừng `S1` và `S2` đã bắn.

## 1. Bản vá bàn giao ĐỎ — và vì sao executor không thấy

Chạy trên vỏ **bind được** (executor không có), bản vá như nó bàn giao cho:

    D8(a) đích nằm trong tập giết: ĐỎ ['d11_xoa_d8']
    D8(b) không tập giết rỗng:     ĐỎ ['d11_xoa_d8']
    TỔNG: ĐỎ      rc=1

Nguyên nhân đo được: mẫu đột biến của `d11_xoa_d8` là chuỗi
`"    lines += dong_d8(d8_errors, failed)"`, và chuỗi ấy xuất hiện **HAI lần** trong tệp — một lần
là mã thật (dòng 660), một lần là **dữ liệu trong chính bảng `MUTATIONS`** (dòng 597). Bộ chạy đột
biến dùng `src.replace(old, new, 1)` nên nó đánh vào lần xuất hiện ĐẦU, tức vào **BẢNG**, không vào
mã. Đột biến do đó không sửa gì trong đoạn nó khai là đích ⇒ không ca nào đỏ ⇒ tập giết RỖNG.

Executor không thấy vì sandbox của nó không `bind(127.0.0.1)` được, nên nền của nó ĐỎ và mọi ô đột
biến in `KHÔNG_ĐO_ĐƯỢC (nền đỏ)` — **đúng `D7b`, và nó khai thẳng**. Nhưng hệ quả là nó **chưa bao
giờ đo bộ đo của chính mình đầu–cuối**, và bản in cuối của nó khai sáu đột biến "BỊ GIẾT" dựa trên
một phép đo thu nhỏ (`CA 0/1`), không phải trên cổng thật.

**Đã sửa bởi phiên điều phối, net 0 dòng:** neo mẫu vào HAI dòng để nó duy nhất. Đo lại:
`CA 40/40 đạt · 0 đỏ · ĐẠT` · `ĐỘT BIẾN 48/48 · ĐẠT` · `D8(a)(b)(c) ĐẠT` · `TỔNG: ĐẠT` · `rc=0`.

### Khuyết tật NỀN mà việc này lộ ra — rộng hơn một đột biến

Bộ chạy đột biến **không có chốt duy-nhất**: nó chỉ kiểm `if old not in src`, không kiểm
`src.count(old) == 1`. Quét cả bảng: **14 trong 48** mẫu đột biến KHÔNG duy nhất. 13 cái còn lại
hiện đánh ĐÚNG chỗ **chỉ nhờ thứ tự tình cờ** — mã đích của chúng nằm TRƯỚC bảng `MUTATIONS`
(dòng 552–601), nên lần xuất hiện đầu là mã thật. Chuyển một hàm xuống dưới bảng là 13 đột biến ấy
lặng lẽ trở thành vô nghĩa, y hệt `d11_xoa_d8`.

| mẫu không duy nhất | số lần | lần đầu ở dòng | đánh trúng? |
|---|---:|---:|---|
| `b7_bo_invalidate` `b7_trung_ten` | 2 | 33 · 44 | đúng chỗ |
| `c1_cho_so_ca_rong` `c4_khong_goi_ca` `d7_cong_khong_xanh` | 4 | 364 | đúng chỗ |
| `c2_cho_so_db_rong` `c3_cho_ca_hai_rong` | 2 | 368 · 372 | đúng chỗ |
| `d10_main_luon_xanh` `d11_ep_rc_xanh` | 3 | 381 | đúng chỗ |
| `d8_bo_dieu_kien_a/b/c` | 2 | 462–464 | đúng chỗ |
| `d9_vuot_ngan_sach` | 2 | 500 | đúng chỗ |
| **`d11_xoa_d8`** | 2 | **597** | **SAI — vào bảng** |

Chốt đúng là fail-close: `src.count(old) != 1` ⇒ `KHÔNG_ĐO_ĐƯỢC`, đừng đoán. Tốn ~2 dòng, và
ngân sách còn **0**.

## 2. Cơ chế mới CÓ răng ở đâu, và KHÔNG ở đâu

Đột biến theo SỐ DÒNG, chạy trên một bản nền đã xanh:

| # | dòng | đột biến | phán định | bản in | mã thoát |
|---|---:|---|---|---|---|
| N1 | 381 | `return 0 if xanh else 1` → `return 0` | **SỐNG SÓT** | `CA 38/40 · 2 đỏ · ĐỎ` · `TỔNG: ĐỎ` | 0 |
| N2 | 377 | `phan_dinh` → `return True` | **SỐNG SÓT** | `CA 39/40 · 1 đỏ · ĐỎ` · `TỔNG: ĐẠT` | 0 |
| N3 | 609 | `fn()` → `pass` | BỊ GIẾT | `CA 40/40 · ĐẠT` · `TỔNG: ĐỎ` | 1 |
| N4 | 660 | bỏ các dòng `D8` | BỊ GIẾT | `TỔNG: ĐỎ` | 1 |
| N5 | 664 | bỏ dòng `TỔNG` | BỊ GIẾT | không có dòng `TỔNG` | 1 |
| N6 | 670 | `sys.exit(chay_cli())` → `sys.exit(0)` | **SỐNG SÓT** | **KHÔNG IN GÌ CẢ** | 0 |
| N7 | 657 | hậu tố dòng `CA` → luôn `"ĐẠT"` | **SỐNG SÓT** | `CA 40/40 · 0 đỏ · ĐẠT` · `TỔNG: ĐẠT` | 0 |
| N8 | 606 | bỏ một ca khỏi vòng lặp | BỊ GIẾT | `CA 39/40 · 0 đỏ · ĐỎ` | 1 |
| N9 | 606+657 | N8 cộng N7 | BỊ GIẾT | `CA 39/40 · 0 đỏ · ĐẠT` · `TỔNG: ĐỎ` | 1 |

**Đã tiến thật.** N1 và N2 vẫn cho tiến trình thoát 0, nhưng khác hẳn trước: bản in nay **NÓI RA**
rằng có ca đỏ (`CA … · ĐỎ`, kèm dòng ca đỏ có tên). Trước bản vá, cùng loại đột biến cho một bản
in TRÔNG SẠCH. Người đọc báo cáo nay thấy đỏ; chỉ mã thoát nói dối.

**Nhưng đừng đọc quá lời.** Với N2 hai dòng của CÙNG một bản in vẫn mâu thuẫn nhau: dòng `CA` nói
`ĐỎ` còn dòng `TỔNG` nói `ĐẠT`. Bất biến "mã thoát phản ánh báo cáo" **chưa** thành bất biến; nó
mới thành "mọi đường làm gãy nó đều để lại vết đỏ trong báo cáo".

## 3. Hai chỗ còn hở — cả hai đều vi phạm chính đặc tả r4

Đặc tả r4 viết: *"không được có dòng nào trong cơ chế mà xoá đi vẫn xanh."*

**(a) `N7` — dòng 657 không có đột biến canh.** Hậu tố `ĐẠT`/`ĐỎ` của dòng `CA` là dòng MỚI do bản
vá này thêm, và ép nó thành `"ĐẠT"` cho một bản chạy XANH HOÀN TOÀN, `rc=0`. Không đột biến nào
trong 48 nhắm vào nó. N9 cho thấy nó không phải chốt DUY NHẤT (bỏ một ca vẫn chết qua đường khác),
nhưng "có đường khác bắt hộ" không phải là có phản chứng.

**(b) `D10-main` bị hạ thành mệnh đề luôn đúng.** Thân ca nay là đúng một dòng:

    assert ma_thoat(False) == 1

Đặc tả r4 đòi `D10`: *"ca dựng cảnh sổ ca một phần tử có cờ ghi nhận, gọi điểm vào, và đòi CẢ HAI:
mã thoát khác 0 VÀ cờ đã được đặt."* Ca mới **không dựng cảnh, không gọi điểm vào, không có cờ**.
Bản CŨ mạnh hơn: nó khẳng định "có ca đăng ký mà không chạy ca nào ⇒ 1". Đây là **hồi quy**, và
theo `S1` (ghi dòng lệch đặc tả) thì đúng ra phải DỪNG trước khi commit. Khả năng ấy chưa mất hẳn
— nó chuyển sang ca `D11-gate` và sang `_du_ca` trong dòng `CA` — nhưng `D10` nay không còn tự đo
tiêu chí mang tên nó.

## 4. Một khuyết tật của ĐẶC TẢ r4, do phiên điều phối viết

Đặc tả r4 khai: *"`D11` thu hẹp bề mặt ấy xuống một dòng duy nhất."* **Đo được là SAI.** Có ít nhất
BA dòng mà đột biến làm tiến trình thoát 0: 381 (`ma_thoat`), 377 (`phan_dinh`), 670 (`sys.exit`).
Khác biệt thật — và đây mới là điều đáng khai — là hai dòng đầu **để lại vết đỏ trong bản in**, còn
dòng 670 thì **không in gì cả**. Câu đúng phải là: *`D11` không xoá được bề mặt, nhưng nó làm mọi
đường làm giả TRỪ dòng ngoài cùng nhất đều phải để lại vết trong báo cáo.*

Ghi vào đây vì phiên điều phối vừa soạn đặc tả, vừa soạn tiêu chí, vừa chấm — và một lời khai quá
mạnh của chính nó là thứ dễ trôi qua nhất.

## 5. Điều kiện dừng đã bắn

- **`S1`** — `D10-main` lệch đặc tả r4 (mục 3b).
- **`S2`** — 900/900, biên **0**. Ba việc còn lại đều cần thêm dòng: chốt duy-nhất cho bộ chạy đột
  biến (~2), đột biến canh dòng 657 (~1), khôi phục `D10` cho tử tế (~4). Tổng ~7 dòng > 0.
- Lease r6 **CẤM nâng trần**, và r5 đã chốt trước: *"MÃ chạm 900 ⇒ TÁCH. Không nâng lần bốn."*

## 6. Đề xuất cho người giữ kho

- **A (khuyến nghị)** — **TÁCH**, đúng như r5 đã hứa trước khi biết sẽ chạm. Packet mới nhận ba
  việc: chốt duy-nhất fail-close cho bộ chạy đột biến · đột biến canh dòng 657 · khôi phục `D10`.
  Packet #319 chạy review vòng 4 trên `f461413a` như hiện trạng, và verdict được đọc với BA finding
  trên đã khai sẵn — reviewer xác nhận hoặc bác chúng, chứ không phải tự tìm lại.
- **B** — nâng trần lần thứ tư. Không khuyến nghị: đây là lần thứ TƯ động vào cùng một con số của
  cùng một packet, và r5 đã ghi thẳng rằng khi ấy con số mất hết ý nghĩa.
- **C** — land `f461413a` với ba finding thành nợ có tên. Chỉ hợp lệ nếu người giữ kho xếp cả ba là
  P2; `luat_dung_LAND` cấm nợ hoá P1, và phiên điều phối **không tự xếp hạng** cho chúng.
