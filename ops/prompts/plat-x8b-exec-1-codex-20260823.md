# Nhiệm vụ executor — `PLAT-X8b` (#255), attempt 1

Bạn là **EXECUTOR `codex`**. Packet nhỏ, đóng, một tệp. Đọc đặc tả `ops/specs/plat-x8b.md` trước —
lease neo băm nó, và nó có đủ số nền + bốn trạng thái đã đo.

## Việc — đúng một tệp: `ops/lease_publish_test.py`

Thêm **một** ca test khoá lại `posixpath.normpath` trong `_tinh_lop_tu_write_set`.

Vì sao cần: bảng `_BANG_LOP` nay chỉ còn mục `sensitive`, nên traversal không còn đích nào để hạ
lớp xuống — xoá hẳn dòng `normpath` mà suite vẫn `87/87 rc=0`, **0 ca ĐỎ**. Mã ĐÚNG, phép đo MẤT.

Cách: bơm một mục **thấp hơn `sensitive` TẠM** vào `mod._BANG_LOP` trong phạm vi ca (cùng nếp
`t77`/`t81`/`A14` — `_nap_cong()` dựng module MỚI mỗi lần gọi nên không rò sang ca khác, đã kiểm),
rồi đòi traversal qua đúng mục ấy vẫn ra `sensitive`, cho **cả** `""` lẫn `"planned:"`.

## CẤM

- **KHÔNG sửa `ops/lease_publish.py`** — mã sản phẩm đúng, sửa là chữa nhầm bệnh.
- **KHÔNG nới `_BANG_LOP` thật** — giữ đúng 7 mục theo `§8:572`. Mục thấp hơn CHỈ trong ca test.
- **KHÔNG sửa/xoá `t83`** — ca mới bổ sung, không thay.
- **KHÔNG `git push`** — phiên điều phối đẩy sau khi kiểm.

## Nghiệm thu — chạy thật, đừng mô tả

1. `python3 ops/lease_publish_test.py`, đọc `rc` **TRỰC TIẾP** (`echo $?` ngay sau lệnh; KHÔNG qua
   pipeline, KHÔNG `$( )` trong cùng chuỗi `echo` — cả hai đã nuốt mã thoát thật ở kho này).
   Đích: **88/88**, hai số BẰNG NHAU, `bỏ qua=0`, `rc=0`.
2. **ĐỘT BIẾN BẮT BUỘC** — trên **bản sao cả cây** trong `/tmp`, không đụng cây chính: xoá dòng
   `duong = posixpath.normpath(duong)` khỏi `_tinh_lop_tu_write_set`, giữ nguyên phần còn lại, chạy
   lại suite ⇒ ca mới phải **ĐỎ**, `87/88` `rc=1`. Nghĩ ra được ca nào thì phải CHẠY nó — kho này
   đã trả giá vì để phép thử nằm trong tài liệu.
3. **Vế DƯƠNG**: xác nhận ca mới XANH khi mã nguyên vẹn (bước 1 đã cho điều này).
4. Xác nhận `t83` XANH ở **cả hai** chiều — nếu `t83` cũng đỏ theo đột biến thì ca mới đang đo trùng
   `t83`, không phải đo thứ `t83` bỏ sót.
5. `git diff --check` ⇒ `rc=0`.
6. **Commit** bằng `git commit -F <tệp>`, KHÔNG `-m` một dòng. Nêu **LÝ DO + bằng chứng đo được**.
   **ĐỪNG viết chuỗi bỏ-qua-CI nguyên văn** trong thông điệp, kể cả khi trích dẫn.

## Báo cáo

Ghi `BAO-CAO-PLAT-X8B.md` ở gốc workspace: sửa gì · số đo thật kèm `rc` · kết quả đột biến cả hai
chiều · `git diff --numstat` so với master.
