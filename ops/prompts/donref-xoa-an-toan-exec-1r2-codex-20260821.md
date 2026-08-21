# Prompt BẤT BIẾN — Executor `DONREF-XOA-AN-TOAN` (#217), lease **r2**, provider `codex`

Bạn là executor. Reviewer là `claude` (cross-provider). Lượt 1 của bạn đã được **`approve`** —
đây **không** phải rework một bản vá hỏng. Reviewer nêu ba finding, cả ba là **khoảng trống RĂNG
kiểm chứng**, không phải lỗ đang mở, và nó **cố ý không tự sửa**.

## 0. Đặc tả vẫn là thẩm quyền

`ops/specs/DONREF-XOA-AN-TOAN.md`, băm

```
1add3edf165faa2b53d6b52212ea34d7a73934367fd73bbca91e5518a9a664de
```

**KHÔNG ĐỔI** — lượt này **không** sửa đặc tả. Tìm ở `master` trước; chưa thấy thì fetch
`ops/spec-donref-xoa-an-toan`. Băm lệch ⇒ DỪNG.

**Vì sao thêm ca test mà không cần bản sửa đổi đặc tả:** `§nghiem_thu` khai *tối thiểu* một tiêu
chí cho mỗi mục tiêu, và `T8` dưới đây phục vụ **đúng `muc_tieu` 3 đã có** ("ba trạng thái —
mọi thứ không đo được rơi vào **C kèm lý do**") ở **cấp toàn kho**, chỗ hiện chỉ có `T4` phủ ở
cấp từng ref. Đây là **làm đầy** một mục tiêu sẵn có, không phải thêm mục tiêu mới. Nếu bạn thấy
lập luận này **sai** ⇒ DỪNG và nói, đừng tự mở rộng đặc tả.

## 1. Mỏ neo

| trường | giá trị |
|---|---|
| packet | `#217` |
| head xuất phát | `fa4b0dd879f0cf7ae589989863670d2a8200839c` |
| write set | **`ops/nhanh_don_duoc_test.py` — ĐÚNG MỘT TỆP** |
| verdict lượt 1 | `approve` — `ops/reviews/…` (bản chiếu trên `#217`) |

`ops/nhanh_don_duoc.py` **KHÔNG** nằm trong write set lượt này. Cả ba finding đều sửa được trong
tệp test. Cần đụng tệp kia ⇒ **DỪNG**, báo cáo.

## 2. Ba việc

### Việc 1 — P2: cấp TOÀN KHO chưa có răng

Ba nhánh rẽ trong `main()` — `fetch` thất bại · kho **nông** · `loi_head or base_oid !=
remote_oid` — là cơ chế **duy nhất** hiện thực hoá `muc_tieu` 3 ở cấp toàn kho, và **không đột
biến nào trong `DOT_BIEN` nhắm vào chúng**. Hành vi hôm nay **đúng** (reviewer tự đo, xem việc 1b),
nhưng một sửa đổi tương lai làm yếu `if fetch.returncode:` sẽ **không ai bắt được**.

**Phải làm:**

- Thêm **`T8`** dựng kho thật với **ref theo dõi cục bộ đã có sẵn từ lần fetch trước**, rồi **phá
  remote** để `fetch` lần này thất bại. Khẳng định: nhánh ấy — dù dữ liệu cục bộ CŨ nói nó đủ
  điều kiện A — phải vào **C kèm lý do**, và lệnh in ra **không** chứa nó.
  Đây là repro reviewer đã dựng và đo được; **dựng lại, đừng chép kết luận**.
- Thêm **ba đột biến** nhắm đúng ba nhánh rẽ ấy: `if fetch.returncode:` → `if False:` ·
  gỡ nhánh `elif shallow:` · `!=` → `==` trong `base_oid != remote_oid`. **Mỗi con phải giết
  đúng ca của nó.**

### Việc 2 — P3: `T3` chưa đo phép lọc C trong lô TRỘN thật

`T3` có cả nhánh B lẫn C trong **cùng một** lần chạy `main()` không suy biến, nhưng chỉ khẳng định
nhóm, **không** khẳng định `"ops/c-mot" not in lenh`. Mutant `in-ca-C` hiện chỉ bị bắt qua `T5` —
vốn là kịch bản **suy biến** (mọi nhánh đều C). Tức phép lọc `nhom in {"A","B"}` **chưa từng được
đo** trong đúng ngữ cảnh thật của kho production, nơi A/B/C **cùng tồn tại**.

**Phải làm:** thêm khẳng định `"ops/c-mot" not in lenh` vào `T3`. Kiểm rằng `in-ca-C` **vẫn**
giết `T5` **và** nay giết cả `T3` — hoặc nếu bạn tách thành mutant riêng thì nói rõ.

### Việc 3 — P3: `nhiem_vu.txt` của lượt 1 khai SAI `rc=1`

Prompt lượt 1 (do phiên điều phối viết) nói *"trên kho nông… **rc=1**"*. Sai: tool chỉ có
`return 2` và `return 0`. Con số `1` là **tạo tác của `| head`** — ống đóng sớm ⇒ `BrokenPipeError`
⇒ thoát 1. Phiên điều phối đã đo lại và xác nhận: `RC_THAT=0`.

**KHÔNG sửa `nhiem_vu.txt`** — nó là prompt đã đóng băng, băm đã công bố trong lease; sửa nó là
làm băm ấy trỏ vào thứ không còn tồn tại. **Việc của bạn:** nếu tệp test có chỗ nào khai/ám chỉ
`rc=1`, sửa cho đúng. Nếu **không có**, nói thẳng là không có — im lặng sẽ bị đọc thành đã sửa.

## 3. Bằng chứng bắt buộc

1. `python3 ops/nhanh_don_duoc_test.py` ⇒ `rc=0`, `N/N` hai số bằng nhau, **không tụt dưới 8 ca**.
2. Bảng đột biến đầy đủ: **mỗi con giết đúng ca của nó**. Con nào giết nhiều ca ⇒ **nói ra**.
3. Kho thật trong `T8` là **kho bare thật**, không đồ giả diễn kịch bản.
4. Mọi đột biến chạy trên **BẢN SAO TẠM**.
5. Chạy tool trên kho này và in kết quả — **đọc `rc` TRỰC TIẾP, không qua ống**. Bài học vừa trả
   giá: `| head` làm rc thành 1 và con số ấy đã đi vào một prompt.
6. Cây sạch; commit, **KHÔNG push**.

## 4. Điều kiện DỪNG

- Cần sửa `ops/nhanh_don_duoc.py` hay bất kỳ tệp nào ngoài write set ⇒ **DỪNG**, báo cáo.
- Thấy lập luận "thêm ca test không cần sửa đặc tả" ở §0 là **sai** ⇒ DỪNG, mở revision.
- Gặp hình dạng **"lời khai rộng hơn phép đo"** lần thứ **sáu** ⇒ DỪNG, không vá, báo cáo. Bộ đếm
  đang ở **5**; lượt 1 của bạn **không** làm nó tăng.

## 5. Báo cáo cuối

Băm đặc tả đã đối chiếu · ba việc đã làm gì · số đo thật với `rc` **đọc trực tiếp** · bảng đột
biến (tên · ca bị giết · `N/N`) · phần còn hở đã khai tên · SHA commit · trạng thái cây. Nói thẳng
thứ nào **không** đo được.
