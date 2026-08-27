# ĐẶC TẢ PACKET — `CONG-SAME-FAILURE-DEM-Y-DINH` (Issue #283)

```yaml
packet_id: CONG-SAME-FAILURE-DEM-Y-DINH
packet_issue: 283
revision: 1
generation: 1
review_class: sensitive          # `.claude/dev/packet_loop.py` nam trong _BANG_LOP sensitive
executor: claude
reviewer: codex
assurance_target: cross_approved
```

Issue #283 mang phần mô tả đầy đủ (phép đo, bảng 4 slug, `muc_tieu`, `nghiem_thu`). Tệp này
là bản **ĐÓNG BĂNG** để lease neo `sha256`; nó **không** nhắc lại Issue mà chỉ chốt những
điều kiện mà lease cưỡng chế được.

## 1. `write_set` — 2 đường dẫn

```
.claude/dev/packet_loop.py
.claude/dev/packet_loop_test.py
```

Đụng đường thứ ba ⇒ đòi revision mới.

## 2. `ngan_sach_kich_thuoc`

| | |
|---|---|
| tệp tối đa | **2** |
| dòng thêm tối đa | **200** |

Vượt ⇒ **DỪNG và NÉN**, không nới. Tiền lệ trong ngày: gen 1 của #262 nới hai lần rồi vẫn
`blocked`; gen 2 nén hai lần và về đúng `220/220`.

## 3. Bất biến KHÔNG được đổi

- **Fail-close giữ nguyên.** Thiếu nhãn, nhãn sai dạng, lease không đọc được ⇒ **TÍNH VÀO
  TRẦN**. Chốt này thà chặn oan còn hơn thả lọt; packet chỉ sửa **ĐẠI LƯỢNG ĐẾM**.
- **Trần `same_failure` giữ nguyên.** Nới trần là bỏ chốt, không phải sửa nó.
- **Người thi công KHÔNG tự dán nhãn hoãn.** Không có chốt này thì M1 là cửa hậu: mọi
  finding lặp đều được gọi là "cố ý hoãn".

## 4. Ba trạng thái, không phải hai

Mỗi finding lặp phải rơi vào đúng một: `va_truot` · `hoan_co_thoa_thuan` · **`KHONG_DO_DUOC`**.
Cái thứ ba **tính vào trần** (fail-close) và phải in ra **khác** hai cái kia — doctrine
`None ≠ False` của kho.

## 5. Phép đo BẮT BUỘC cho mọi đột biến

**Bán kính nổ đo trên TOÀN BỘ suite**, không dùng kết quả của bộ tự-chứng-minh.

Lý do đã đo được, không phải phòng xa: bộ ấy chỉ chạy `phai_chet` + **3 đối chứng KHÁC HỌ**,
nên một đột biến giết **37/231** ca vẫn báo *"giết 1 ca đích · 3 đối chứng còn sống"*. Đã trả
giá ở #262 (`mutant-siet-tuoi-giet-ba-muoi-bay-ca`), và cross-review bắt được vì **họ** chạy
toàn suite còn executor thì không.

```python
ket = T.chay_suite(mut_path, tmpdir)          # KHONG truyen chi_chay
chet = sorted(t for t, v in ket.items() if v is not None)
```

## 6. `dieu_kien_dung`

- Định **nới trần** thay vì sửa đại lượng đếm ⇒ DỪNG.
- Định cho **người thi công** tự dán nhãn hoãn ⇒ DỪNG.
- Vượt **200** dòng hoặc **2** tệp ⇒ DỪNG và NÉN.
- Định sửa `docs/PROTOCOL_DA_PHIEN.md` ⇒ DỪNG: ngoài write set, và §10 đang là write set
  tiềm năng của #284.

## 7. `chua_do_duoc` — khai trước

- **`packet_loop_test.py` KHÔNG có cổng CI nào** (#277). Mọi con số của packet này sẽ là
  **lượt chạy TAY, một nền**, trừ khi #277 land trước. Khai thẳng trong PR, đừng để `231/231`
  trông như đã được máy đo.
- **Không đo được nhãn "hoãn có thoả thuận" có bị lạm dụng trong thực tế không** — packet chỉ
  dựng được cơ chế và chốt thẩm quyền; tần suất lạm dụng chỉ lộ sau vài packet dùng thật.
- **Ca #262 dùng làm N1 là ca LỊCH SỬ**, dựng lại từ `finding_ids` trong handoff. Nó **không**
  chứng minh cơ chế đúng cho mọi hình dạng hoãn — chỉ cho hình dạng đã gặp.
