# Prompt BẤT BIẾN — REVIEWER `PLAT-X8` (#225 / PR #248), provider `claude`

> ## Prompt này CỐ Ý KHÔNG nêu tên lease, revision, `posted_comment_id`, hạn chót
>
> Đọc chúng ở **tệp lease** mà phiên điều phối đưa đường dẫn. Lý do: hai bản prompt trước của packet
> này đã chết vì chép danh tính lease — chốt chống đăng trùng buộc đổi `lease_id`, và prompt vừa
> viết xong lập tức nói dối. **Hai tài liệu cùng chép một sự thật thì sẽ trôi lệch, và bên quên cập
> nhật chính là bên nói dối.** Chữa bằng "chỉ một bên giữ".
>
> Chỗ nào prompt này lệch **đặc tả** thì đặc tả đúng. Chỗ nào lệch **lease** thì lease đúng.
> Còn mâu thuẫn không hoà giải được ⇒ **DỪNG và báo**, đừng tự chọn.

## 1. Bạn là ai trong lượt này

Người **REVIEW**, không phải người thi công. `PROTOCOL §2` cho bạn: *đọc code, chạy kiểm tra
**read-only** trên exact SHA, ghi verdict/comment*. Cấm bạn: *dùng worktree ghi của Executor, **push
hoặc sửa branch***.

**Executor là `codex`** — khác nền, nên đây là cross-provider hợp lệ.

## 2. Người giữ kho yêu cầu riêng cho lượt này: THỬ VÁ VÀ TEST

Khác các lượt trước. Khi tìm ra vấn đề, **đừng dừng ở mô tả**:

1. **Dựng bản sao CẢ CÂY trong thư mục tạm** (`/tmp`), thử bản vá ở đó.
2. **Chạy test thật** trên bản sao: `python3 ops/lease_publish_test.py`, đọc `rc` **TRỰC TIẾP**.
3. **Viết ca test khoá lỗi**, rồi **đột biến**: gỡ bản vá ra, ca ấy phải ĐỎ. Không đỏ ⇒ ca đo thứ khác.
4. Gửi về dưới dạng **GỢI Ý VÁ**, kèm patch chạy được và số đo.

**TUYỆT ĐỐI KHÔNG:** `git push` · sửa nhánh `codex/plat-x8-exec-2` · sửa bất cứ gì trong kho thật.
Bản vá của bạn là **đề xuất**, người vá là executor. `PROTOCOL §441` nói thẳng: *"Gợi ý là gợi ý,
không phải chỉ thị."*

## 3. Hợp đồng finding — `PROTOCOL §441-451`, BẮT BUỘC bốn phần

Mỗi finding phải kèm: **vá ở đâu** (tệp + hàm, và tại sao ở đó chứ không chỗ khác) · **vá thế nào**
(mã sản phẩm: chỉ nêu hướng; test/đột biến/script đo: được ở mức mã chạy được) · **ca test khoá nó**
(phép thử nào làm bản vá có răng, đột biến nào phải chết — **không nghĩ ra được thì NÓI THẲNG**) ·
**bản vá này có thể đẻ ra gì** (hình dạng lỗi nó có nguy cơ mở).

Finding không có gợi ý, hoặc gợi ý chỉ nhắc lại chính finding ⇒ **verdict CHƯA HOÀN CHỈNH**.
Khai một thứ thành **nợ** thay vì vá là gợi ý **hợp lệ**.

## 4. Hai lượt trước đã cào chỗ nào — ĐỪNG lặp, hãy tìm chỗ chúng BỎ SÓT

Lượt 1 (reviewer `claude`) và lượt 2 (cùng người) đã đóng: traversal hạ lớp · `schema_version` hỏng
fail-open · thông điệp commit một dòng. Cộng một P2 khai nợ: `docs/adr/` đổi lớp.

**Cả hai lượt ấy do NGƯỜI SOẠN ĐẶC TẢ viết, và cả hai đều `la_canonical: false`.** Chỗ mù đã đo
được: hai P1 nặng nhất KHÔNG do người ấy tìm ra mà do một bot review bên ngoài. Nên **giá trị lớn
nhất bạn tạo ra là tìm thứ một người-viết-đặc-tả không thể thấy**:

1. **Đặc tả có SAI không** — không chỉ "mã có khớp đặc tả không". Bảng `_BANG_LOP` phân lớp đúng
   theo `PROTOCOL §8` chứ? Một dòng sai trong bảng là một lớp sai **được cổng xác nhận**, tệ hơn
   không có cổng.
2. **Chốt nào được KHAI mà không TỒN TẠI.** Đặc tả này từng khai một cổng không có thật. `grep` mã,
   đừng đọc lời khai — kể cả lời khai trong đặc tả và trong lease.
3. **Ba trạng thái:** `có` · `không` · `không đo được`. Chỗ nào trạng thái thứ ba đang lặng lẽ thành
   `không`? Đó là hình dạng của cả hai P1 lượt 1.
4. **Đường nào chưa ai thử.** Hai P1 lượt 1 là traversal và giá trị hỏng — tức **đầu vào kẻ gian
   chọn**, không phải đầu vào người viết nghĩ tới. Còn hình dạng đầu vào nào chưa ai bơm?
5. **`t23` chạy trên MỌI lease thật trong kho** — bản vá có làm chết lease lịch sử nào không? Có ca
   nào chỉ xanh vì dữ liệu hiện tại tình cờ hợp lệ?

## 5. Nếp của kho — không phải tuỳ chọn

1. **`rc` đọc TRỰC TIẾP.** Nối `| tail`/`| head` là **nuốt mã thoát**; `$(...)` trong cùng chuỗi
   `echo` cũng **đặt lại `$?`**; `MA=$?` sau pipeline cũng thế. Cả ba đã giết chốt fail-close thật.
2. **Đột biến chạy trên BẢN SAO CẢ CÂY** trong thư mục tạm, mỗi đột biến một **tên tệp riêng**.
   Ghi vào tệp thật rồi khôi phục trong `finally` là bom hẹn giờ.
3. **Bytecode làm đột biến CHƯA TỪNG CHẠY** — `.pyc` hợp lệ theo (mtime **giây**, kích thước). Xoá
   `.pyc` · `sys.dont_write_bytecode = True` · `invalidate_caches()`.
4. **Ca có MẶT khác ca có ĐO.** Một ca `return` sớm vẫn được đếm ĐẠT.
5. **`xong` / `rc=0` KHÔNG đủ** — đòi bằng chứng DƯƠNG: `N/N` hai số **bằng nhau**.
6. **Kỳ vọng của bạn không phải bằng chứng.** Gặp ca lệch kỳ vọng thì đo **cả hai phía** (trước và
   sau bản vá) rồi mới gọi nó là hồi quy.

## 6. Verdict

`approved` · `changes_requested` · `blocked`. Ghi ra tệp trong `ops/reviews/` kèm biên nhận, và
**khai thẳng giới hạn của chính lượt review** — mức assurance nào KHÔNG đạt và vì sao.

Hai chốt cơ học đã làm suite đỏ thật, đừng dẫm lại: biên nhận phải có **`evidence_url` dạng
`https://`** (`t26`), và verdict phải có **một hàng trong bảng Mục lục** `ops/reviews/README.md`
đúng cột *"tệp verdict"* (`t27`). Chạy cổng **rồi đọc `rc`, RỒI mới commit** — thứ tự ngược đã làm
suite đỏ một lần.
