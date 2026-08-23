# Cross-review lượt 1 — `PLAT-X8b` (#255 / PR #263) — VÒNG CANON

Bạn là **REVIEWER**, phiên `claude` RIÊNG, read-only. Executor là `codex` ⇒ **cross-provider**
(`cross_approved` đạt được theo `PROTOCOL §8.1`). Packet còn **2/2** vòng canon; lượt này tiêu một.

## Thẩm quyền — tự kiểm TRƯỚC khi làm gì khác

Lease của chính lượt này: `ops/leases/plat-x8b-review-1-claude-20260823.yaml` trên nhánh
`ops/cap-lease-plat-x8-2`.

```bash
git ls-tree -r --name-only origin/ops/cap-lease-plat-x8-2 -- ops/leases/ | grep x8b-review
```

Không thấy ⇒ `git fetch origin '+refs/heads/*:refs/remotes/origin/*'` rồi đo lại; vẫn không thấy thì
**DỪNG và khai `blocked`**. Packet mẹ đã có một lượt chạy KHÔNG lease vì phiên điều phối quên cấp —
chính reviewer phát hiện, và đó là lý do dòng này đứng đầu prompt.

## Neo

- exact head **`135adf78c1f6175c977ae3439ce27619202dff08`** · base `1ef928db2a409ea73de5a30f8bd14023c0aca3b1`
- diff: **1 tệp, 10 dòng thêm** — `ops/lease_publish_test.py`, thêm đúng một ca `t88`.

## BẮT BUỘC TRƯỚC KHI REVIEW — đối chiếu cổng sandbox vs cây gốc (`PROTOCOL §8`)

Sandbox phải **TÁI LẬP MÔI TRƯỜNG CỔNG**, không chỉ tái lập nội dung. Cụ thể, đã đo được ở PR #252:
`core.abbrev` **phải ghim = 7** trong sandbox, nếu không `git rev-parse --short` trả 8 ký tự và
`doc-claims-check --strict` đổi SHA dài 8 từ *advisory* thành **cờ cứng** ⇒ `rc=2` giả.

```bash
git config core.abbrev            # phải là 7
python3 ops/lease_publish_test.py ; echo $?
```

**Lệch với cây gốc là LỖI SANDBOX cho tới khi chứng minh ngược lại.** Phiên điều phối khai: trên cây
gốc cùng commit, suite = `88/88` `rc=0`. Sandbox ra số khác ⇒ điều tra sandbox TRƯỚC, đừng báo
finding.

## HAI LUẬT REVIEW — `PROTOCOL §8`, luật chứ không phải cú pháp

**Reviewer phải ĐO ĐƯỢC, không chỉ ĐỌC.** Mọi khẳng định kèm lệnh đã chạy + kết quả + `rc` đọc TRỰC
TIẾP (`echo $?` ngay sau lệnh; KHÔNG pipeline, KHÔNG `$( )` cùng chuỗi `echo`). Không đo được thì
viết **`KHÔNG ĐO ĐƯỢC`** kèm lý do — trạng thái THỨ BA, không gộp vào "không có vấn đề". Suy luận có
căn cứ KHÔNG phải phép đo.

**Đối chiếu nguồn gốc.** Đây là lượt 1 của `PLAT-X8b` nên chưa có "lượt trước" của chính packet.
Nhưng packet này SINH RA từ một finding của vòng canon `PLAT-X8` lượt 4. Hãy tự kiểm finding gốc ấy
trên cây hiện tại và phân loại theo đúng bốn nhãn `§8`: **`ĐÃ VÁ THẬT` · `VÁ HỜ` · `VÁ SINH LỖI MỚI`
· `CHƯA VÁ`**, kèm bằng chứng bạn TỰ ĐO — không nhận lời khai của executor lẫn của điều phối.

## Bảng bằng chứng của điều phối — và GIỚI HẠN của nó (`PROTOCOL §8`)

Điều phối khai đã đo bốn trạng thái trên cây `git archive` sạch:

| trạng thái | khai |
|---|---|
| nền (chưa có `t88`) | `87/87` `rc=0` |
| xoá `posixpath.normpath`, **chưa** có `t88` | `87/87` `rc=0` — 0 ca ĐỎ |
| có `t88`, mã nguyên vẹn | `88/88` `rc=0` |
| có `t88` + xoá `normpath` | `87/88` `rc=1`, CHỈ `t88` ĐỎ; `t83` XANH |

**Lệnh đã dùng để trích bảng này:** chạy `python3 ops/lease_publish_test.py` trên bốn cây, mỗi cây
dựng bằng `git archive <sha> | tar -x`, đột biến bằng cách xoá đúng dòng chứa `posixpath.normpath`.
**Nó lọc theo:** đúng MỘT đột biến, đúng MỘT hàm. **Do đó nó bỏ sót:** mọi đột biến khác trong
`_tinh_lop_tu_write_set`, mọi tương tác của `t88` với ca khác ngoài `t83`, mọi đầu vào đối kháng
không đi qua `tam/lop-thap/`, và toàn bộ câu hỏi `t88` có đo ĐÚNG THỨ nó tự nhận hay không.
**Mỗi mục bảng này bỏ sót mà bạn tìm ra được tính là FINDING.**

**ĐỪNG nhận bốn con số trên — chạy lại.** Lời khai của điều phối cũng là lời khai.

## Danh sách dưới đây là TRẦN, không phải SÀN

Nó giới hạn tầm nhìn theo đúng hình dạng hiểu biết của người viết prompt — tức người đã bỏ sót.
Finding nặng nhất của packet mẹ **không nằm trong hướng nào** được giao. **Tìm thứ không được giao.**

- `t88` bơm `("tam/lop-thap/", "routine")` vào `mod._BANG_LOP`. Có rò sang ca khác không? `_nap_cong()`
  dựng module mới mỗi lần — kiểm, đừng tin.
- `t88` có thật sự đo `normpath` không, hay đo một thứ khác tình cờ cùng chết theo đột biến ấy?
- Đột biến của điều phối xoá CẢ DÒNG. Còn đột biến TINH VI hơn thì sao — ví dụ đổi `normpath` thành
  một phép chuẩn hoá SAI nhưng vẫn chuẩn hoá? `t88` có bắt được không?
- Bảng seed nay chỉ còn `sensitive`. Nhánh `routine`/`systemic` của `_tinh_lop_tu_write_set` còn ca
  nào phủ **vế DƯƠNG** không, hay đã thành mã chết?
- `t88` dùng prefix tổng hợp `tam/lop-thap/`. Tên ấy có thể trùng đường thật nào trong kho không?

## VIỆC RIÊNG LƯỢT NÀY — người giữ kho chỉ thị

Tìm ra vấn đề ⇒ **THỬ VÁ VÀ KIỂM CHỨNG** trên **bản sao cả cây** trong `/tmp` (KHÔNG đụng cây
review): vá, chạy suite đọc `rc` trực tiếp, viết ca test khoá lỗi, rồi **ĐỘT BIẾN gỡ vá để chứng
minh ca ấy ĐỎ**. Gửi về dạng **GỢI Ý VÁ** kèm patch chạy được. Gợi ý là gợi ý — người vá là executor.

## Hợp đồng finding (`PROTOCOL:436-451`) — BỐN phần bắt buộc

**vá ở đâu** · **vá thế nào** · **ca test khoá nó + đột biến nào phải chết** · **bản vá đẻ ra gì**.
Không nghĩ ra phần nào thì nói thẳng. Gợi ý chỉ nhắc lại chính finding ⇒ verdict **chưa hoàn chỉnh**.

## CẤM

`git push` · `git commit` · sửa kho thật · sửa nhánh `codex/plat-x8b-exec-1`.

## ĐẦU RA

`verdict` (`approve`/`changes_requested`/`blocked`) · `assurance` **thực sự đạt**, đừng khai theo mục
tiêu · phần đối chiếu finding gốc theo bốn nhãn · từng finding đủ bốn phần · bảng số đo (lệnh · kết
quả · `rc` · **thời điểm + head**) · **giới hạn của chính lượt này**, nói thẳng.
