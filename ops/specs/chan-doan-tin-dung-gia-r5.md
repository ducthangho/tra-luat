# `CHAN-DOAN-TIN-DUNG-GIA` — revision 5

| trường | giá trị |
|---|---|
| `packet_id` | `CHAN-DOAN-TIN-DUNG-GIA` |
| `packet_issue` | #568 |
| `revision` | 5 |
| `revision tiền nhiệm` | 4 (spec `bbdbff5a…`, đã thi công ở PR #598) |
| `executor` | `claude` |
| `assurance_target` | `human_audited` |
| `review_class` | `sensitive` |
| `base` | head PR #598 |

## `nguon_cap_viec`

**Ba** lượt cross-review trên codex (reviewer cross-provider), chạy độc lập trên `eb4a9ab` (#572),
`45ea292` (#590), `9361a47` (#591). Cả ba trả `changes_requested`. Ba P1/P2 chính đã vá ở r4.
**Hai finding còn lại** là nội dung revision này; executor đã **tái hiện bằng phản chứng chạy
được** cả hai. Đăng tại [#568 issuecomment-5759499489](https://github.com/ducthangho/tra-luat/issues/568#issuecomment-5759499489).

Chỉ thị chủ kho, nguyên văn: **"1. Đồng ý"** (cho đề nghị cấp r5), kèm
**"Lặp quy trình: vá, cross-review, đăng verdict cho tới khi approve."**

## Hai bệnh — đều ĐÃ ĐO

### B4 — ranh giới nuốt thân nhiều dòng **mà không khai cắt**

`ranh = re.compile(r"^(?:TU KIEM|DOT BIEN|MUTANT|LOI:)")` đóng khối ở **bất kỳ** dòng nào mang
một trong bốn tiền tố — kể cả khi đó là **nội dung hợp lệ của ngoại lệ**. Phần bị bỏ **không bao
giờ tới** `_goi_chan_doan`, nên không có nhãn `CAT` và không có số ký tự mất.

```
stdout = "TU KIEM r506: DO_KHAC - AssertionError: first" + LF
         "LOI: root-cause" + LF + "more-details" + LF + "TU KIEM: 0/1" + LF

ket qua            : [('r506', 'AssertionError: first')]
'root-cause' co    : False
'more-details' co  : False
sau _goi_chan_doan : 'AssertionError: first'
co nhan CAT        : False
```

Mất hai dòng thân **mà không một dấu hiệu nào nói là đã mất**. Đúng lớp bệnh #568 tồn tại để
chữa, ở một tầng khác. M4 của r1 khai *"chuyển tiếp NGUYÊN chẩn đoán"* — **rộng hơn** thứ nó làm
được. Xảy ra **kể cả khi thông điệp ngắn hơn trần 400**, nên nó **không** phải trường hợp cắt đã
khai của `_goi_chan_doan`.

### B5 — `r525` cấm một thứ đặc tả KHÔNG đòi, và **khoá chết** một đường mất chẩn đoán

`r525` chốt `chot(MOC not in th, "r525")` ở ô `thuong`: **bắt buộc** cha **không** được in
`stderr` khi đã có `DO_CHOT`. A8 của r2 chỉ đòi: *"`rc=1`, `stdout` rỗng, `stderr` mang chuỗi mốc
⇒ dòng cha phải chứa chuỗi mốc ấy"*. **Không có vế cấm.**

Đường "con **đã báo** một chốt rồi **chết tiếp** vì một lẽ khác" là có thật:

```
stdout = "TU KIEM r511: DO_CHOT - chot cua ca r511 that bai" + LF   ·  rc=1
stderr = "SystemExit: NGUYEN_NHAN_SAU_CHOT" + LF

(giet, hong)                 = (0, 1)
co in "CHOT r511"            : True
co in "NGUYEN_NHAN_SAU_CHOT" : False     <- nguyen nhan BI VUT
```

Lẽ thật nằm trên `stderr` và bị vứt — **và `r525` còn chốt rằng nó PHẢI bị vứt**, tức khoá chết
đường ấy và **bác trước** một triển khai giữ cả hai chẩn đoán.

## §4 — Mục tiêu

| | |
|---|---|
| **M13** | Ranh giới bỏ dòng nào thì phải **khai** — số dòng bị bỏ đi kèm khối vừa đóng. Không mất im lặng |
| **M14** | Bỏ vế cấm khỏi `r525`; cha **được phép** in cả `CHOT` lẫn `stderr`. Đường "đã báo chốt rồi chết tiếp" có **một mục có tên** và một phép đo |

**M13 — hai đường đều chấp nhận được, chọn một và khai:** (a) thu hẹp nhận diện ranh giới, hoặc
(b) giữ ranh giới nhưng **đếm và khai** phần bị bỏ. Đường (b) an toàn hơn vì không đổi phân hạng.
Dù chọn đường nào, **điều bị cấm là mất im lặng**.

**M14 — ghi rõ một hệ quả:** sửa `r525` **đổi một ca đã thi công và đang chờ audit ở PR #590**.
Chủ kho đã được báo trước điều đó và vẫn đồng ý.

## §5 — Nghiệm thu

| | tiêu chí | đột biến phải giết |
|---|---|---|
| **A29** | Với `stdout` có thân nhiều dòng bị ranh giới cắt, dòng cha phải mang **số dòng bị bỏ**. Khai bằng số, không bằng "có/không" | Bỏ phép đếm ⇒ ca ĐỎ |
| **A30** | Thân **không** bị cắt ⇒ **không** có nhãn bỏ-qua. Ba trạng thái phân biệt được bằng đầu vào: không mất / mất n dòng / cắt theo trần | Luôn in nhãn ⇒ ca ĐỎ |
| **A31** | `r525` **không còn** vế cấm. Với `stdout` có `DO_CHOT` **và** `stderr` mang mốc, một triển khai in **cả hai** phải ĐẠT | Đưa lại vế cấm ⇒ ca ĐỎ |
| **A32** | Đường "đã báo chốt rồi chết tiếp" có **ca riêng** đo được: `stdout` có `DO_CHOT`, `stderr` mang mốc khác ⇒ hành vi hiện tại được **khai đúng**, không khai rộng | Đổi hành vi mà không đổi lời khai ⇒ ca ĐỎ |
| **A33** | Phân hạng **không đổi**: cặp `(giet, hong)` bằng đúng cặp của nền trên cùng bảng đầu vào | Đổi một nhánh phân hạng ⇒ cặp lệch |
| **A34** | Ca mới nằm trong `NHOM_BAT_BUOC`, có **đột biến riêng**, `SAN_NHOM` cập nhật | Bỏ đột biến của ca mới ⇒ `thieu` khác rỗng |
| **A35** | Toàn bộ tệp ⇒ `rc=0`, `TU KIEM N/N` **hai số bằng nhau**, `dot bien giet M/M` **hai số bằng nhau** | Bất kỳ ca nào đỏ |
| **A36** | Delta so nền: nền đã đo `rc=0 · 30/30 · 94/94`; ứng viên `rc=0` và `dot bien giet = 94 + (số đột biến mới)`, hai vế dựng trong **MỘT** lệnh | Hai vế dựng ở hai thời điểm ⇒ phép đo vô hiệu |

**Lưu ý gắn vào A32.** r5 **không** hứa chữa đường "đã báo chốt rồi chết tiếp" — nó chỉ **gỡ khoá**
và **khai đúng** hành vi hiện tại. Chữa nó (in cả hai chẩn đoán) là **mở rộng phạm vi**: nó đổi
định dạng đầu ra mà `r516`/`r524`/`r530` đang đo. Ai muốn chữa thì xin revision riêng.

## §6 — `ngoai_pham_vi`

- **P1 về `r508`** — closure **#593**, đang xử riêng. r5 không đụng.
- **Chữa** đường "đã báo chốt rồi chết tiếp" — xem lưu ý A32. r5 chỉ gỡ khoá và khai đúng.
- Đổi hướng cắt hoặc `TRAN_CHAN_DOAN`.
- `CASE T6`; nguyên nhân (A) của `r506`; bốn điểm cảnh báo còn lại.
- Cơ chế write-set / lease — nợ riêng, issue **#599**.
- Mọi tệp ngoài `write_set`.

## §7 — `write_set`

```yaml
write_set:
  - ops/nhanh_don_duoc_test.py
```

Một đường. `start_from_sha` neo vào head #598: r5 xây **trên** r1+r2+r3+#593+r4, và A36 phải đo
trong **đúng** bảng đột biến r4 để lại (94 mục).

## §8 — `hinh_dang_ke_thua`

| hình dạng | trước | **r5** | vì sao |
|---|---|---|---|
| `LOI-KHAI-RONG-HON-PHEP-DO` | 6 | **7** | B4: M4 của r1 khai *"chuyển tiếp NGUYÊN chẩn đoán"*; đo được là mất dòng mà không khai |
| `TIN-HIEU-DO-CHINH-MA-TEST-GIA-MAO` | 4 | 4 | không tái phát |
| `CHOT-CAM-THU-DAC-TA-KHONG-DOI` | — | **1** | B5: `r525` chốt một vế cấm không có trong A8, và **bác trước** một triển khai đúng. Hình dạng MỚI, đặt tên ở đây |

`CHOT-CAM-THU-DAC-TA-KHONG-DOI` là hình dạng **mới**: một chốt tự thêm điều kiện ngoài đặc tả
rồi biến điều kiện ấy thành luật. Nó nguy hơn một chốt yếu, vì nó **chặn** đường sửa đúng.

**Cơ hội tái phát đã biết, cho chính r5:** A30 đòi "không mất thì không có nhãn". Nếu ca chỉ kiểm
chiều "có mất thì có nhãn" mà bỏ chiều ngược, một triển khai **luôn** in nhãn sẽ xanh — và lời
khai "khai đúng phần bị bỏ" lại rộng hơn phép đo, tức `LOI-KHAI-RONG-HON-PHEP-DO` lần thứ **tám**.
Ba trạng thái của A30 phải **phân biệt được bằng đầu vào**, mỗi trạng thái một ô.
