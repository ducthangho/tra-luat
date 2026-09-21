# `DAU-PHIEN-TRUNG-LAM-DO-CONG` — revision 1

| trường | giá trị |
|---|---|
| `packet_id` | `DAU-PHIEN-TRUNG-LAM-DO-CONG` |
| `packet_issue` | #593 |
| `revision` | 1 |
| `executor` | `claude` |
| `assurance_target` | `human_audited` |
| `review_class` | `sensitive` — chạm CHÍNH bộ phân hạng đột biến |
| `base` | chốt lúc cấp lease, KHÔNG chốt sẵn ở đây — xem §7 |

## `nguon_cap_viec`

Đỏ thật trên `gate-registry` của PR #591, head `9361a47`, run `35562939228`. Chẩn đoán đầy đủ
đăng tại [pull/591#issuecomment-5755803616](https://github.com/ducthangho/tra-luat/pull/591#issuecomment-5755803616).
Chỉ thị chủ kho, nguyên văn: **"Mở packet riêng cho entropy đi"**.

## Bệnh — ĐÃ ĐO, có số

`gate-registry` là **required check**. Nó đỏ ~**1 trên 256** lượt chạy đầy đủ, trên **mọi** head,
**mọi** nhánh, không liên quan tới nội dung PR.

Đột biến `entropy-giu-mot-byte`:

```python
"    return secrets.token_hex(16)"  ->  "    return secrets.token_hex(16)[-2:] * 16"
```

ép không gian giá trị của `sinh_dau_phien()` xuống **256**.

`r508_ban_ghi_luot_TRUOC_chi_khac_dau_phien` mở đầu:

```python
    ph_that, ph_khac = sinh_dau_phien(), sinh_dau_phien()
```

**Hai dấu phiên khác nhau là TIỀN ĐỀ của ca, không phải thứ ca ấy đo.** Ca đo rằng `doc_kenh`
trả `KHONG_DO_DUOC` khi bản ghi mang dấu phiên KHÁC. Khi hai lần rút trùng — 1/256 — bản ghi
hoá ra *khớp* dấu phiên đang hỏi, `doc_kenh` trả thứ khác, và `r508` chết **vì một lý do VÔ CAN**.
Đúng hình dạng `TIN DUNG GIA` mà chính kho này đặt tên, lần này **nằm bên trong một ca test**.

Đo 200 000 cặp, hai lượt độc lập:

```
lượt 1:  768 / 200 000  =  0,3840 %
lượt 2:  723 / 200 000  =  0,3615 %
lý thuyết 1/256         =  0,3906 %
```

Khi `r508` chết thêm, `do_chot = {r508, r509}` ≠ `dich = ("r509",)`, nên `chay_dot_bien_tu_kiem`
xếp mutant vào `hong` và suite ĐỎ.

**Loại trừ mọi packet đang mở:**

```
entropy-giu-mot-byte + r508 có tại: origin/master, dc85dd0a, 45ea292, 9361a47
git diff 45ea292 9361a47 -- ops/nhanh_don_duoc_test.py
    | grep -E 'entropy-giu-mot-byte|r508|sinh_dau_phien|token_hex'   =>  RỖNG
lượt A12 trên NỀN eb4a9ab (20-09) đã đỏ y hệt, 79/80, cùng mutant
```

## §3 — MỘT ĐƯỜNG VÁ BỊ BÁC, ghi lại để không ai đi lại

Nới `dich` thành `("r508","r509")` là đường **sai theo chiều nguy hiểm**. Chạy thẳng vị từ phân
hạng ở `ops/nhanh_don_duoc_test.py:2936` (`elif do_chot == set(dich):`) trên cả hai tập đầu vào
có thật:

```
  dich hien tai              do_chot=['r509']          -> GIET
  dich nan thanh hai ten     do_chot=['r509']          -> HONG (suite DO)
  dich hien tai              do_chot=['r508','r509']   -> HONG (suite DO)
  dich nan thanh hai ten     do_chot=['r508','r509']   -> GIET
```

Nó **đảo** chỗ chập chờn: đỏ **255/256** thay vì 1/256. Executor đã nêu nhầm đường này ở
pull/591#issuecomment-5755803616 và đã đính chính tại #593.

## §4 — Mục tiêu

| | |
|---|---|
| **M1** | `r508` dựng hai dấu phiên **phân biệt được** bằng một vòng rút có **chặn trên**, không rút một lần rồi cầu may |
| **M2** | Cạn chặn trên ⇒ khai **`KHÔNG ĐO ĐƯỢC`**. Không lặng lẽ đi tiếp trên tiền đề đã vỡ, không làm tròn lên ĐẠT. Ba trạng thái, fail-close |
| **M3** | Một ca KHOÁ chứng minh chính điều đó, tất định, không dựa vào may rủi |

## §5 — Nghiệm thu

| | tiêu chí | đột biến phải giết |
|---|---|---|
| **A1** | Bộ sinh **hằng** (không gian = 1) ⇒ `r508` ra `KHÔNG ĐO ĐƯỢC`; **không** ĐẠT, **không** treo. Chặn trên phải có, và phải đo được bằng số lần gọi | Bỏ chặn trên ⇒ ca treo / hết giờ ⇒ ĐỎ |
| **A2** | Bộ sinh không gian 256 ⇒ `r508` vẫn ĐẠT, **tất định** trên ít nhất 1 000 lượt lặp trong ca | Bỏ vòng rút lại ⇒ ca ĐỎ theo xác suất — nên chốt phải lặp đủ để bắt chắc |
| **A3** | Cạn chặn trên khai `KHÔNG ĐO ĐƯỢC` chứ không `DO_CHOT` và cũng không `DO_KHAC` — ba trạng thái phân biệt được bằng đầu vào | Đổi nhánh cạn-chặn sang `chot(False, ...)` ⇒ ca ĐỎ |
| **A4** | `r509` **KHÔNG ĐỔI MỘT DÒNG**, và `entropy-giu-mot-byte` vẫn giết đúng `r509` với `dich = ("r509",)` | Sửa `r509` ⇒ ca khoá ĐỎ |
| **A5** | Phân hạng không đổi: cặp `(giet, hong)` của toàn bảng bằng đúng cặp của nền trên cùng đầu vào | Đổi một nhánh phân hạng ⇒ cặp lệch |
| **A6** | Ca mới nằm trong `NHOM_BAT_BUOC`, có **đột biến riêng**, `SAN_NHOM` cập nhật | Bỏ đột biến của ca mới ⇒ `thieu` khác rỗng |
| **A7** | Toàn bộ tệp ⇒ `rc=0`, `TU KIEM N/N` **hai số bằng nhau**, `dot bien giet M/M` **hai số bằng nhau** | Bất kỳ ca nào đỏ |
| **A8** | Delta so nền, hai vế dựng trong **MỘT** lệnh; ứng viên = nền + (số đột biến mới) | Hai vế dựng ở hai thời điểm ⇒ phép đo vô hiệu |
| **A9** | **Chập chờn đã hết**: chạy `r508` `N ≥ 100 000` lượt **dưới chính đột biến** `entropy-giu-mot-byte` (gọi thẳng, không qua suite) ⇒ **0** lần đỏ. Khai bằng hai số bằng nhau `N/N` | Bỏ vòng rút lại ⇒ ~`N/256` lần đỏ ⇒ ca ĐỎ |

**Lưu ý gắn vào A9.** Đây là chốt DUY NHẤT chứng minh bệnh đã hết, và nó phải chạy **dưới đột biến**
chứ không dưới mã thường — dưới mã thường không gian là 2^128 nên `0 lần đỏ` đúng một cách vô nghĩa.
Một phép đo không phân biệt được "đã chữa" với "chưa từng bệnh" là một phép đo rỗng.

## §6 — `ngoai_pham_vi`

- Mọi thứ của #568: `CASE T6`, nguyên nhân (A) của `r506`, M7–M9 của r3.
- Đổi `sinh_dau_phien()` hay `secrets.token_hex`. **Bộ sinh không sai**; chỗ sai là một ca coi
  tính phân biệt là chuyện đương nhiên.
- Sửa `r509` — xem A4. Nó là ca thật sự đo bộ sinh.
- Nới `dich` của `entropy-giu-mot-byte` — xem §3, đã bác bằng số.
- Bốn điểm cảnh báo `invalid escape sequence` còn lại của kho — nợ riêng, đã khai ở #568.
- Mọi tệp ngoài `write_set`, kể cả sửa tạm rồi hoàn nguyên.

## §7 — `write_set` và VẬT CẢN LỊCH

```yaml
write_set:
  - ops/nhanh_don_duoc_test.py
```

Một đường, nằm gọn trong trần `≤ 3 tệp` của `ADR-0044:5` cho class `sensitive`.

**Đường ấy hiện do `chan-doan-tin-dung-gia-r3-g1-claude` giữ** (#568, tới `2026-09-22T04:45:00Z`).
Hai packet không thể cùng giữ một đường: cấp lease cho packet này **ngay bây giờ** sẽ làm
`ai-dang-giu` trả `NGƯỜI_GIỮ 2` — tức **CỬA ĐÓNG cho CẢ HAI**, và #568 r3 sẽ mất quyền ghi
trong lúc PR #591 còn đang chờ audit.

Nên lease của packet này phải chờ một trong hai:
1. #591 được audit và land, rồi r3 nhả đường; **hoặc**
2. Chủ kho chỉ thị khác một cách tường minh.

`base` và `start_from_sha` chốt **lúc cấp lease**, không chốt sẵn ở đây — vì head của #591 còn
có thể đổi theo audit, và neo sẵn một sha rồi để nó lệch là đúng lỗi `lease neo base không thuộc
master` mà `ADR-0044` đã ghi.

## §8 — `hinh_dang_ke_thua`

Kế thừa bộ đếm của #568 tại thời điểm mở packet này:

| hình dạng | số |
|---|---|
| `LOI-KHAI-RONG-HON-PHEP-DO` | 4 |
| `TIN-HIEU-DO-CHINH-MA-TEST-GIA-MAO` | 3 |
| `VA-DUNG-CHO-DUOC-CHI-ROI-BO-SOT-DUONG-THU-BA` | 2 |

**Cơ hội tái phát đã biết, cho chính packet này:** A9 là chốt duy nhất chứng minh bệnh đã hết.
Nếu nó chạy dưới mã thường thay vì dưới đột biến, nó sẽ **xanh mà không đo gì** — đúng hình dạng
`TIN-HIEU-DO-CHINH-MA-TEST-GIA-MAO` lần thứ **tư**. Hình dạng ấy đã ở mức 3, tức đã vượt ngưỡng
*"lần thứ ba ⇒ DỪNG và hỏi"*. Executor phải đo và khai rõ A9 chạy dưới đột biến, và phải có một
đột biến riêng chứng minh A9 có răng.
