# Đặc tả packet — VERDICT-KHONG-BOC-HOI (revision 1)

Đặc tả ĐÓNG BĂNG. Lease neo vào `spec_hash` = sha256 của chính tệp này.

## `nguon_cap_viec`

Chỉ thị chủ kho trong phiên `session_01C52eS8AgeiwTrDifXGDGYP` (2026-09-08): xử lý hai nội dung
phát hiện khi đo, mở PR ở phiên riêng, cấp lease và thực thi. Nội dung (b) là packet này.

## Bối cảnh đo được (mọi số kèm thời điểm và lệnh)

### Chính adapter đã khai hậu quả, mà không có gì cưỡng chế

`.claude/skills/cross-review/SKILL.md`, mục "GHI VERDICT LÊN PR", viết nguyên văn:

> Không có bước này thì lượt review **không tồn tại** với ai ngoài phiên đang chạy — prompt
> review vòng 6 của đợt F2 đã bốc hơi đúng kiểu đó.

Tức kho ĐÃ BIẾT lớp lỗi này và đã mất một lượt vì nó. Nhưng câu ấy là **lời dặn**, không phải
cổng: không bộ kiểm nào đòi một lượt review phải để lại hiện vật bền.

### Đo lại 2026-09-08 — nó vẫn đang xảy ra, và ở quy mô lớn hơn

**PR #478, lượt 1–3.** Ba lượt ấy CÓ XẢY RA — thông điệp commit chứng minh:

```
8f7becb ops/land: vá 7 P2 của cross-review #478 lượt 1 — trong đó 4 số SAI
260f7c6 ops: vá 4 P2 của cross-review #478 lượt 2 — trong đó bản vá lượt 1 làm ĐỎ cổng
5a4dd85 ops/reviews: vá P1 cổng receipt v2 + P2 provenance model (#478 lượt 3)
```

Hiện vật của ba lượt ấy: **KHÔNG CÓ, ở cả hai chỗ có thể có.**

- Trên PR: `pull_request_read(get_comments)` trên #478 ⇒ mảng **RỖNG** (0 comment).
- Trong kho: `git rev-list --objects --all | grep -iE 'pr478|478-.*verdict'` ⇒ **0** đường dẫn.

**PR #468 — cùng bệnh, đo được thành số.** Quét toàn kho (309 nhánh + 62 tag):

```
git rev-list --objects --all | grep -oE 'ops/reviews/pr468[^ ]*verdict\.md' | sort -u
```

⇒ **10** verdict, đánh số **6–15**. Lượt **1–4** không có hiện vật nào. Lượt **5** có hiện vật,
và hiện vật ấy TỰ PHỦ ĐỊNH: `ops/reviews/GHI-NHAN-CROSS-REVIEW-LUOT5-KHONG-HOAN-TAT.md:3` viết
*"Đây KHÔNG phải verdict và KHÔNG phải biên nhận"*, không có `*.receipt.yaml` đi kèm.

**Tổng: ít nhất 8 lượt review (5 của #468 + 3 của #478) không để lại verdict bền nào.**
Con số ấy là cận DƯỚI: chỉ đếm được các lượt mà commit hoặc tài liệu khác còn nhắc tới. Lượt nào
chạy rồi biến mất hoàn toàn thì theo định nghĩa không đếm được.

### Cổng hiện có KHÔNG chặn

`.claude/dev/packet_loop.py record-review --help` (đo 2026-09-08) nhận:

```
--packet --provider --verdict {approve,changes_requested,blocked}
--reviewed-sha --finding-id --finding-desc
```

**Không có trường nào trỏ tới hiện vật verdict.** Nên `record-review` ghi nhận một lượt review
là ĐÃ XẢY RA mà không đòi bất kỳ bằng chứng bền nào rằng verdict ấy tồn tại ở đâu đó. Một lượt
được đếm vào `assurance` trong khi nội dung của nó có thể đã bốc hơi.

Đây đúng họ bài học của kho: **đếm SỰ CÓ MẶT của một lượt thay vì KHẢ NĂNG TRA LẠI nó.**

## `review_class`

`sensitive` — chạm `.claude/dev/packet_loop.py`, tệp cưỡng chế điều kiện dừng của `PROTOCOL §12`.

## `write_set`

```
.claude/dev/packet_loop.py
.claude/dev/packet_loop_test.py
.claude/skills/cross-review/SKILL.md
```

Đo `ai-dang-giu` trên cả ba đường, 2026-09-08: **`NGƯỜI_GIỮ 0`**.

## `ngoai_pham_vi`

- KHÔNG sửa `CLAUDE.md` — thuộc write set packet `MU-REF-KHONG-PHU-TAG` chạy song song.
- KHÔNG dựng lại verdict đã mất của 8 lượt nói trên. Chúng KHÔNG khôi phục được; packet này
  chặn lần sau, không vá lịch sử. Bịa lại một verdict cũ là làm hỏng hồ sơ.
- KHÔNG đổi ba giá trị canonical của `--verdict` (`approve`/`changes_requested`/`blocked`).
- KHÔNG tự đăng comment lên GitHub từ `packet_loop.py`. Nó là bộ ghi sổ cục bộ; thêm đường ghi
  ra mạng là mở một bề mặt mới và trái kiến trúc "không thêm đường ghi thứ ba".

## `muc_tieu`

1. `record-review` ĐÒI một **con trỏ verdict bền** và fail-close khi thiếu. Con trỏ hợp lệ là
   một trong hai, và phải KIỂM ĐƯỢC chứ không chỉ khai:
   - đường dẫn hiện vật **có trong git** tại `reviewed_sha` (hoặc trong cây làm việc), hoặc
   - định danh comment đã đăng trên PR (id số + URL).
2. Ba trạng thái: `có con trỏ kiểm được` · `thiếu` · `có khai mà KHÔNG kiểm được`. Trạng thái
   thứ ba fail-close, mã thoát RIÊNG — không gộp vào `thiếu`.
3. `SKILL.md` nêu đúng cú pháp mới, và **đồng bộ nợ `SKILL-MD-COMM-CHI-PHU-HEADS`**: đoạn `comm`
   trong tệp ấy chỉ phủ `--heads`; sửa để trỏ sang bộ kiểm của packet `MU-REF-KHONG-PHU-TAG`
   thay vì chép lại doctrine (chép sẽ làm `doctrine-scan` đỏ).
4. Phản chứng chạy được cho từng chốt.

## `nghiem_thu` — mọi tiêu chí NÊU ĐƠN VỊ

| # | tiêu chí | đơn vị / ngưỡng |
|---|---|---|
| B1 | `python3 -B .claude/dev/packet_loop_test.py` | `N/N đạt` hai số **BẰNG NHAU**, `bỏ qua = 0`, `rc = 0` |
| B2 | DELTA số ca so `origin/master` | **≥ +6** ca mới |
| B3 | ca "thiếu con trỏ ⇒ CHẶN" | mã thoát **≠ 0** |
| B4 | ca "con trỏ là đường dẫn CÓ trong git ⇒ QUA" | mã thoát **= 0** |
| B5 | ca "con trỏ trỏ đường dẫn KHÔNG tồn tại ⇒ CHẶN" | mã thoát **≠ 0**, **≠** mã của B3 |
| B6 | ca "con trỏ là comment id hợp lệ ⇒ QUA" | mã thoát **= 0** |
| B7 | ca "comment id sai dạng ⇒ CHẶN" | mã thoát **≠ 0** |
| B8 | ca "hiện vật RỖNG (0 byte) ⇒ CHẶN" | mã thoát **≠ 0** — có tệp ≠ có nội dung |
| B9 | đột biến: bỏ chốt đòi con trỏ | ca B3 phải **ĐỎ** |
| B10 | đột biến: chấp nhận con trỏ mà không kiểm tồn tại | ca B5 phải **ĐỎ** |
| B11 | đột biến: coi tệp rỗng là hợp lệ | ca B8 phải **ĐỎ** |
| B12 | tương thích ngược | mọi lời gọi `record-review` HIỆN CÓ trong kho phải còn chạy được, hoặc packet phải liệt kê ĐỦ chỗ cần sửa (đếm bằng `rg`, ghi SỐ) |
| B13 | `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | `rc = 0` |
| B14 | `python3 .claude/dev/packet_loop.py adr-song --root .` | `rc = 0` |
| B15 | `python3 -B ops/lease_publish_test.py` | `121/121 đạt; đã chạy=121, bỏ qua=0`, `rc = 0` |
| B16 | `python3 -B ops/bien_nhan_v2.py` | `0 vi phạm`, `TỔNG: ĐẠT`, `rc = 0` |
| B17 | `python3 scripts/tl.py doc-claims-check --strict` | `rc = 0`, `ok: true` |
| B18 | cột THÊM của `git diff --numstat` | **≤ 500** dòng |

**B9–B11 là chốt răng.** Đột biến chết vì lỗi VÔ CAN là **TÍN DỤNG GIẢ**, không tính — phải phân
hạng bằng tín hiệu mã triển khai KHÔNG GIẢ ĐƯỢC (lớp ngoại lệ riêng + neo TÊN CA), theo bài học
`#355`/`#359`. Một `except Exception ... raise AssertionError` trên đường đi sẽ giả mạo được tín
hiệu "ca đích đỏ"; đừng phân hạng bằng chuỗi `AssertionError`.

## `dieu_kien_dung`

- Cho `packet_loop.py` gọi mạng để xác minh comment id. Nó là bộ ghi sổ CỤC BỘ; kiểm dạng và
  kiểm sự có mặt trong sổ là đủ. Gọi mạng ⇒ cổng phụ thuộc mạng ⇒ tự tắt khi mất mạng.
- Nới chốt để các lời gọi cũ khỏi sửa. Nếu tương thích ngược đắt thì **khai số chỗ phải sửa**
  (B12) và báo chủ kho, đừng hạ chốt.
- Dựng lại verdict đã mất — xem `ngoai_pham_vi`.
- Sửa `CLAUDE.md` — chồng lấn write set.
- Đếm một lượt review là hợp lệ chỉ vì `record-review` chạy `rc=0`. Chính packet này tồn tại vì
  `rc=0` từng không đảm bảo gì.

## `chua_do_duoc`

- **Tổng số lượt cross-review từng chạy trong kho**: KHÔNG ĐO ĐƯỢC. Con số 8 ở trên là cận DƯỚI,
  chỉ gồm lượt còn được commit hoặc tài liệu khác nhắc tới.
- Lượt 1–3 của #478 có từng được đăng lên PR rồi bị xoá hay chưa bao giờ được đăng: KHÔNG ĐO
  ĐƯỢC — API chỉ trả trạng thái hiện tại, không trả lịch sử xoá.
- Liệu `assurance` của các packet cũ có bị tính sai vì đếm cả lượt không hiện vật: chưa đo.
  Ghi làm câu hỏi mở; packet này KHÔNG hồi tố.
