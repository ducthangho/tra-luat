# Cross-review LƯỢT 2 — PR #264 (hồ sơ `PLAT-X8` + `PLAT-X8b`)

Bạn là **REVIEWER**, phiên `claude` RIÊNG, read-only. PR thuần tài liệu, lớp **`sensitive`** (đo bằng
chính cổng `PLAT-X8`: mọi đường dẫn rơi mặc định fail-closed).

**LƯỢT 2.** Lượt 1 trả `changes_requested` với **ba** finding; tác giả đã vá cả ba và head đổi. Việc
chính của bạn là mục `ĐỐI CHIẾU LƯỢT TRƯỚC` — nó là **bắt buộc từ lượt 2** theo `PROTOCOL §8`.

## Thẩm quyền — tự kiểm trước

```bash
git ls-tree -r --name-only origin/ops/cap-lease-plat-x8-2 -- ops/leases/ | grep handoff-264-review-2
```
Không thấy ⇒ fetch đủ rồi đo lại; vẫn không thấy ⇒ **DỪNG, khai `blocked`**.

## SANDBOX phải TÁI LẬP MÔI TRƯỜNG CỔNG (`PROTOCOL §8`)

`core.abbrev` ghim **= 7**, chạy cổng NGAY TRONG sandbox, đối chiếu cây gốc cùng commit.
**Lệch là lỗi sandbox cho tới khi chứng minh ngược lại.**

## ĐỐI CHIẾU LƯỢT TRƯỚC — bắt buộc, bốn nhãn `§8`

Với **TỪNG** finding của lượt 1, tự kiểm trên cây HIỆN TẠI và phân loại:
**`ĐÃ VÁ THẬT` · `VÁ HỜ` · `VÁ SINH LỖI MỚI` · `CHƯA VÁ`** — kèm bằng chứng bạn TỰ ĐO.
**Không nhận lời khai của tác giả.** Mục này rẻ và bắt được thứ không lượt nào khác nhìn tới: bản vá
**tự sinh lỗi**.

**F1 [P2] — `t27` mù vì sai tên trường.** Ba biên nhận v2 dùng khoá `canh_bao_da_nang_len_muc_luc`;
`t27` đọc `verdict_usage_caveats`. Cổng lặp trên danh sách RỖNG ⇒ 12 caveat chưa từng được kiểm.
Bản vá khai: đổi tên khoá ở cả ba tệp.
**Đừng tin — tự chạy đột biến HAI CHIỀU**: xoá một hàng caveat khỏi `ops/reviews/README.md` ⇒ `t27`
phải **ĐỎ** và trỏ đúng tên caveat; khôi phục ⇒ xanh. Nếu nó vẫn xanh khi thiếu hàng thì bản vá là
`VÁ HỜ`.

**F2 [P2] — caveat `mo-neo-TRUNG-BINH-khong-phai-manh` của `plat-x8b-review-1` thiếu hàng README.**
Bản vá khai: đã thêm. Tự liệt kê **TOÀN BỘ** caveat của cả ba biên nhận và đối chiếu từng cặp
(`id`, `tệp verdict`) với bảng README — đếm ra con số, đừng nhìn lướt.

**F3 [P3] — dòng bookkeeping `land-evidence` sẽ sai sau khi #264 merge.** Bản vá khai: viết lại cho
đúng ở CẢ HAI phía. Tự đọc câu mới và hỏi: nó còn đúng sau merge không? Có câu NÀO KHÁC trong diff
cùng bệnh mà lượt 1 bỏ sót không?

## Danh sách trên là TRẦN, không phải SÀN

Lượt 1 tìm được finding nặng nhất **NGOÀI** mọi hướng nó được giao. Người viết prompt này cũng là
người viết các tệp bị review và là người vừa vá — nên nó mù đúng chỗ vừa sửa. **Tìm thứ không được giao.**

Vài chỗ đáng nghi mà lượt 1 CHƯA soi (gợi ý, không giới hạn):
- Bản vá F1 đổi tên khoá ở ba tệp. Có tệp thứ tư nào trong kho cũng dùng tên sai không? Có chỗ nào
  còn NHẮC tên cũ (tài liệu, commit, README) làm người sau chép lại không?
- `t27` nay đọc được 12 caveat. Cả 12 có thật sự có hàng đúng không, hay chỉ cái bị đột biến mới có?
- Bản vá F3 thêm một câu dài vào `no_mang_theo_khi_land`. Nó có làm YAML sai kiểu, hay nói quá điều
  đo được không?

## Bằng chứng CI

`B-CI-EVIDENCE.md` — **LỜI KHAI của phiên điều phối**, không phải phép đo của bạn. Đọc phần giới hạn
trong đó và khai đúng nguồn.

## Hợp đồng finding `§441` — bốn phần. CẤM `git push`/`commit`/sửa kho thật.

## ĐẦU RA

`verdict` · `assurance` **thực sự đạt** · **mục `ĐỐI CHIẾU LƯỢT TRƯỚC` với bốn nhãn** · finding mới
(nếu có) đủ bốn phần · bảng số đo (lệnh · kết quả · `rc` · thời điểm + head) · **giới hạn của chính
lượt này**.
