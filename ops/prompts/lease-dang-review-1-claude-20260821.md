# Prompt REVIEWER — `LEASE-DANG-DUNG-MOT-LAN` (#227), lượt 1

Bạn là **reviewer** của packet này. Lease `lease-dang-review-1-claude-20260821`.
**CHỈ ĐỌC.** Không sửa mã, không push, không commit. Đầu ra của bạn là một **verdict**.

## Neo — kiểm trước khi đọc

- Exact head phải review: **`fefa15b67a2691cf90ee8bfd0ab3880adc5f35d9`**
  (`origin/codex/lease-dang-exec-1`). Head khác ⇒ DỪNG, báo cáo.
- Đặc tả ĐÓNG BĂNG — **authority thật sự**, KHÔNG phải prompt này, KHÔNG phải thân Issue:
  ```
  git show origin/ops/lease-dang-227:ops/specs/LEASE-DANG-DUNG-MOT-LAN.md > /tmp/spec227.md
  sha256sum /tmp/spec227.md   # PHẢI = e1026adb569f5b4732197afac9c0f35cdd5a8945d46301b1d4cb062624e7c72c
  ```
  Lệch băm ⇒ DỪNG.
  Tìm ở `master` trước; chưa thấy thì `git fetch origin ops/lease-dang-227` rồi lấy ở đó.
  **Thứ định danh tệp là BĂM, không phải tên nhánh.**
- Nền so: `cfaccff9bb373274552042e01edb4bfee81dc0ed`.

## Bối cảnh, gọn

Cổng đăng lease đăng **trùng** comment (11 comment cho 4 lease) và **chết cả lượt** khi
`packet_issue` trỏ vào một PR (4/20 lượt chạy gần nhất ĐỎ, cùng một dòng 403). Đặc tả chốt tám
quyết định Q1–Q8. Bản vá: 3 tệp, +298/−11, suite `52/52`, `actionlint` 5/5 — **đã được phiên
điều phối chạy lại độc lập và khớp**, nên đừng tiêu thời gian chứng minh lại ba con số đó.

## Việc của bạn

**Đo, đừng đọc.** Mỗi phát hiện phải có một lệnh chạy được và đầu ra thật. Một phát hiện không
chạy được thì nó **không tồn tại** — đó là luật của kho này, không phải lời khuyên.

Bốn câu hỏi, xếp theo mức nguy hiểm:

1. **Bản vá có làm ĐÚNG thứ nó khai không — trên MỌI đường, hay chỉ trên đường có test?**
   Hình dạng lỗi mà kho này đã đếm **5 lần**: *lời khai rộng hơn phép đo*. Với mỗi lời khai
   trong `muc_tieu` (đặc biệt **Q4** "xử hết nhưng vẫn ĐỎ" và **Q5** "ghi ngược chạy kể cả khi
   bước đăng đỏ"), hãy liệt kê **mọi đường** mà bước đăng có thể chết, rồi **đo từng đường**.
   Đặc tả nói `T51`/`T52` đo **thân bước trích từ YAML** — thân bước ấy trích được và chạy được
   ngoài Actions (tiền lệ `t32`), nên bạn **chạy được** phép đo này. Hãy chạy.
2. **Ba trạng thái có thật là ba không?** `có` · `không` · `KHÔNG ĐO ĐƯỢC`. Với mỗi lớp mới, tìm
   một đầu vào làm trạng thái thứ ba **im lặng thành "không"**. `gh` vắng mặt, `gh` trả rc≠0,
   JSON méo, phân trang, `--slurp` không được hỗ trợ ở phiên bản `gh` của runner.
3. **Mối nối `GOI_GH` có thật sự là một, và có thật sự không chọn được từ ngoài?** Đầu vào do
   head kiểm soát mà chọn được nguồn dữ liệu của cổng là lỗ authority.
4. **Dấu `**Lease `<id>`**` có phải mỏ neo đủ chặt?** Nghĩ theo cả hai chiều: (a) dấu bị BỎ SÓT ⇒
   đăng trùng; (b) dấu bị TRÙNG NHẦM ⇒ một lease chính đáng **không bao giờ** đăng được. Ai có
   thể đặt chuỗi ấy vào một comment trên issue, và bằng cách nào?

Ngoài bốn câu trên, **cứ báo bất cứ thứ gì bạn ĐO được**. Đừng bó mình trong danh sách này —
danh sách do phiên đã cấp lease viết, và chính phiên ấy vừa mắc lỗi lần thứ 5 của hình dạng nói
trên (kết luận "#214 là ISSUE" từ một API tiện tay thay vì từ `html_url`).

## Ngoài phạm vi — ĐỪNG báo

Đặc tả có mục `ngoai_pham_vi` và `chua_do_duoc`. Thứ đã khai ở đó **không phải finding**:
không thêm `pull-requests: write` · không sửa R4 · không dọn 4 tệp lease thiếu
`posted_comment_id` · không dọn 7 comment trùng · không đăng lại lease lên #214 · không đổi
`dung_than()` · chưa có lượt chạy Actions thật · khe race giữa hai nhánh `ops/**` chỉ **thu hẹp**.
Thấy một mục trong `chua_do_duoc` khai **hẹp hơn thực tế** thì ĐÓ mới là finding.

## Verdict — định dạng

```
KET_LUAN: <cross_approved | can_sua | dung_lai>
reviewed_sha: fefa15b67a2691cf90ee8bfd0ab3880adc5f35d9
```
Rồi từng finding: **P1/P2/P3** · một câu nêu lỗi · **lệnh + đầu ra thật** làm nó hiện ra ·
đề xuất vá. Không finding nào được nêu mà thiếu phần "lệnh + đầu ra".

Cuối verdict, hai mục bắt buộc:
- **`da_do_gi`** — bạn đã chạy những gì. Ai đọc phải dựng lại được.
- **`khong_do_duoc`** — thứ bạn **không** đo được và **vì sao**. Nói **"thu hẹp"** khi nó chỉ thu
  hẹp; chữ **"đóng"** chỉ dùng khi có phép đo chứng minh đã đóng.

Nguồn sự thật là **tệp có băm trong kho**; prompt này chỉ là bản chiếu.
