# Cross-review — PR #267 (hồ sơ hai lượt review của PR #264)

Bạn là **REVIEWER**, phiên `claude` RIÊNG, read-only. Bốn tệp, **không một dòng mã sản phẩm**: hai
verdict (nguyên văn, neo băm) + hai biên nhận `schema_version: 2`, cộng vài hàng `ops/reviews/README.md`.

Lớp hiệu lực **`sensitive`** — đo bằng chính cổng `PLAT-X8` dựng: `ops/reviews/**` không nằm trong
`_BANG_LOP` nên rơi nhánh MẶC ĐỊNH fail-closed. Tài liệu không được miễn vì nó là tài liệu.

## Thẩm quyền — tự kiểm trước mọi việc khác

```bash
git ls-tree -r --name-only origin/ops/cap-lease-plat-x8-2 -- ops/leases/ | grep handoff-267
```
Không thấy ⇒ `git fetch origin '+refs/heads/*:refs/remotes/origin/*'` rồi đo lại; vẫn không thấy ⇒
**DỪNG, khai `blocked`**.

## SANDBOX phải TÁI LẬP MÔI TRƯỜNG CỔNG (`PROTOCOL §8`)

`core.abbrev` ghim **= 7**, chạy cổng NGAY TRONG sandbox, đối chiếu cây gốc cùng commit.
**Lệch là lỗi sandbox cho tới khi chứng minh ngược lại.**

## BỐI CẢNH — PR này ghi hồ sơ về một PR ĐÃ MERGE

PR #264 (hồ sơ `PLAT-X8`/`PLAT-X8b`) đã merge `6541cade`. Hai lượt review của nó không thể ghi vào
chính nó — thêm verdict sẽ đổi head, làm verdict hết phủ, đòi lượt nữa, lặp vô hạn. Nên chúng ghi ở
PR #267 này, **sau** khi #264 đã land.

Chuỗi đệ quy **dừng ở đây bằng QUYẾT ĐỊNH của chủ kho**, không bằng cơ chế nào. Nghĩa là: verdict của
CHÍNH LƯỢT NÀY sẽ không được ghi vào một PR nào nữa. Bạn nên biết điều đó khi cân nhắc mức độ chi
tiết cần ghi — đây là mắt xích cuối, không có lượt sau đọc lại.

## VIỆC — soi thứ TÀI LIỆU có thể sai: LỜI KHAI

1. **Băm/số của hai biên nhận có khớp tệp thật không?** `verdict_sha256`, `verdict_bytes`,
   `reviewed_sha`, `base_sha`, `evidence_url` (commit có tồn tại? nội dung tại đó có khớp băm? có
   đúng là commit ADD đầu tiên?).
2. **`t27` có THẬT SỰ đọc được caveat của hai biên nhận mới không?** Đây là điểm nóng: ba biên nhận
   TRƯỚC dùng sai tên khoá nên `t27` mù hoàn toàn. **Tự chạy đột biến hai chiều** — xoá một hàng
   caveat khỏi `ops/reviews/README.md` ⇒ `t27` phải ĐỎ và trỏ đúng `id`; khôi phục ⇒ xanh.
   Rồi **tự liệt kê TOÀN BỘ** caveat của hai biên nhận và đối chiếu từng cặp (`id`, `tệp verdict`)
   với bảng README. Đếm ra con số, đừng nhìn lướt.
3. **Hai verdict có được chép NGUYÊN VĂN không?** Chúng là tệp neo băm; so với băm khai trong biên
   nhận. Có chỗ nào bị sửa, cắt, hay thêm không?
4. **Ba lời tự khai giới hạn có ĐÚNG không** — hay khai nhẹ hơn/nặng hơn sự thật?
   (a) *"KHÔNG tính canon, KHÔNG tiêu vòng nào của `PLAT-X8`/`PLAT-X8b`"* — kiểm `ADR-0043` và bộ
       đếm thật trong các biên nhận của hai packet ấy.
   (b) *"KHÔNG cross-provider"* — kiểm có đúng cả tác giả lẫn reviewer đều `claude` không.
   (c) *"bằng chứng CI của cả hai lượt đều do điều phối cấp và đều có lỗi"* — đọc hai verdict, xem
       mô tả ấy có khớp thứ verdict thật sự nói không.
5. **Câu mô tả VỊ TRÍ artefact** — bài học `CLAUDE.md`: câu nào nói "tệp X ở nhánh Y" phải đúng ở CẢ
   HAI phía lần merge. Có câu nào sẽ chết đúng lúc #267 land không?
6. **Nợ `DE-QUY-HO-SO-REVIEW-CHUA-CO-LUAT`** — nó khai đệ quy dừng bằng quyết định chứ không bằng
   cơ chế. Câu ấy có đúng không, hay có cơ chế nào trong kho đã ngầm chặn mà chưa ai nhận ra?

## Danh sách trên là TRẦN, không phải SÀN

Người viết prompt này cũng là người viết cả bốn tệp bị review — nó mù đúng chỗ mình sai. Ba lượt
review gần nhất của chuỗi này đều tìm được finding nặng nhất **NGOÀI** mọi hướng được giao, và cả ba
lần đều là lỗi của phiên điều phối. **Tìm thứ không được giao.**

Một hướng nghi cụ thể: **bộ bằng chứng do điều phối chuẩn bị đã hỏng BA lần liên tiếp** (thiếu hẳn ·
neo sai head · chụp run chưa xong). Lần này nó khai đã sửa. Kiểm xem có thật không.

## Bằng chứng CI

`B-CI-EVIDENCE.md` — **LỜI KHAI của phiên điều phối**, không phải phép đo của bạn. Nó phải in rõ
`head` mà nó đo và trạng thái run. **Nếu head ấy không khớp `reviewed_sha`, hoặc run chưa hoàn tất,
hãy khai `KHÔNG ĐO ĐƯỢC`** — đừng dùng số của head khác.

## Hợp đồng finding `§441` — bốn phần. CẤM `git push`/`commit`/sửa kho thật.

## ĐẦU RA

`verdict` · `assurance` **thực sự đạt** · từng finding đủ bốn phần · bảng số đo (lệnh · kết quả ·
`rc` · thời điểm + head) · **giới hạn của chính lượt này**.
