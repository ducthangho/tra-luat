# PROMPT REVIEWER — `SLICE-B-C` (#215 / PR "#216"). Neo exact head `181bd7f8`.

Reviewer khác nền (codex) cho packet do `claude` vá. **Read-only.** Kho ở `./kho`; mọi tệp
bạn tạo phải nằm NGOÀI cây ấy. Chốt: `git -C kho status --short` RỖNG ở cuối lượt, HEAD vẫn
`181bd7f822f84a528da4cfde810d240bcc726dbf`.

## Packet làm gì

Phần còn lại DUY NHẤT của Slice B. Ba việc, write set **đúng hai tệp**
(`ops/NO_KY_THUAT.md`, `ops/lease_publish_test.py`), `+100/−0`:

1. Hai mục sổ nợ (§9, §10). Tiêu chí là một phép **ĐẾM**: `.github/workflows/ci.yml` khai
   **2** chuỗi `NỢ CÓ TÊN`, sổ nợ phải có **2** mục tương ứng.
2. Docstring `t34` nay nói phạm vi bằng SỐ: che **3/8 = 37,5%** dạng gọi đã biết.
3. Ca mới **`t42`** đòi docstring `t34` chứa đủ **năm dạng gọi đã ĐO là lọt** + con số `3/8`,
   với bảng `_DANG_DA_DO_LA_LOT` làm NGUỒN.

## Việc — soi bốn trục, mỗi trục một câu hỏi sắc

**1. `t42` có RĂNG THẬT không, hay chỉ trông có răng?** Phiên vá khai ba đột biến giết đúng
`t42` (bỏ một dạng khỏi docstring · bỏ `3/8` · đổi bảng mà không đổi docstring). **Đo lại**,
đừng đọc. Rồi tự nghĩ đột biến THỨ TƯ mà `t42` **không** giết được.
Cảnh báo phương pháp, phiên vá đã ăn một lần: chạy đột biến bằng cách copy **một tệp** ra thư
mục tạm làm `HERE` lệch và cho `9/42` **vô nghĩa** — phải copy **cả cây**.

**2. `t42` đo LỜI KHAI hay đo HÀNH VI, và docstring của nó có khai đúng điều đó không?**
Đây là chỗ packet dễ tự mâu thuẫn nhất: một ca sinh ra để chặn "lời khai trôi" mà chính lời
khai của nó trôi thì vô nghĩa. Kiểm cả hai chiều.

**3. Hai mục sổ nợ có nói QUÁ phạm vi đo được không?** §9 khai `PLAT-X5-required-status-check`
là nợ **THƯỜNG TRỰC** (vì Q7 đã quyết KHÔNG BẬT) và khai *"thứ mất là DETECTION, không phải
PROTECTION"* kèm con số *"vẫn còn 8 ca đỏ"*. **Kiểm con số 8 ấy có đo được không.** Nếu không
kiểm được từ cây này thì khai `KHÔNG ĐO ĐƯỢC` — đừng đoán.

**4. Phép ĐẾM `2 = 2` có bị lách được không?** Nó đếm chuỗi `NỢ CÓ TÊN` trong `ci.yml` và mục
trong sổ nợ. Ai đó thêm một marker thứ ba mà quên mục thì có gì đỏ không? Có ca máy nào canh
phép đếm ấy không, hay nó chỉ là câu chữ trong Issue?

## Bốn chốt của kho
1. Bằng chứng DƯƠNG: `N/N` hai số bằng nhau, đừng dừng ở `rc=0`.
2. Đột biến chạy trên BẢN SAO CẢ CÂY, không ghi vào tệp thật.
3. Ba trạng thái: `có` · `không` · **`KHÔNG ĐO ĐƯỢC`**. Cái thứ ba phải được KHAI.
4. Khai thẳng thứ bạn không đo được.

## Đầu ra
Mỗi finding: bằng chứng chạy được · mức (P0..P3) · bất biến bị cắt · gợi ý vá.
Kết thúc bằng đúng hai dòng, mỗi dòng ĐÚNG MỘT LẦN:

```
VERDICT: approve | changes_requested | blocked
Reviewed commit: 181bd7f822f84a528da4cfde810d240bcc726dbf
```
