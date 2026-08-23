# Cross-review — PR #264 (hồ sơ `PLAT-X8` + `PLAT-X8b`)

Bạn là **REVIEWER**, phiên `claude` RIÊNG, read-only. PR này **KHÔNG có một dòng mã sản phẩm** — 15
tệp, `+1702/−0`, toàn hồ sơ: verdict, biên nhận, land evidence, prompt bất biến, đặc tả, mục lục.

Lớp hiệu lực: **`sensitive`**. Không phải "cho chắc" — đo bằng chính cổng `PLAT-X8` dựng: cả 15
đường dẫn đều KHÔNG nằm trong `_BANG_LOP`, nên rơi vào nhánh MẶC ĐỊNH fail-closed. Vì thế `PROTOCOL
§8` đòi cross-review trước land, dù nó chỉ là tài liệu.

## Thẩm quyền — tự kiểm trước

```bash
git ls-tree -r --name-only origin/ops/cap-lease-plat-x8-2 -- ops/leases/ | grep handoff-264
```
Không thấy ⇒ fetch đủ rồi đo lại; vẫn không thấy ⇒ **DỪNG, khai `blocked`**.

## Neo

exact head **`36b8ea39`** · base = `origin/master` lúc cấp.

## SANDBOX phải TÁI LẬP MÔI TRƯỜNG CỔNG (`PROTOCOL §8`)

`core.abbrev` **ghim = 7**, rồi chạy cổng NGAY TRONG sandbox và đối chiếu cây gốc cùng commit.
**Lệch là lỗi sandbox cho tới khi chứng minh ngược lại.** Điều phối khai đã đối chiếu: `87/87 rc=0`
hai bên.

## VIỆC — đây là PR TÀI LIỆU, nên soi thứ tài liệu có thể sai

Mã không chạy được thì không có test nào bắt lỗi. Thứ PR này có thể sai là **LỜI KHAI**. Với TỪNG
khẳng định kiểm được, hãy ĐO:

1. **Băm và số trong biên nhận có khớp tệp thật không?** `verdict_sha256`, `verdict_bytes`,
   `reviewed_sha`, `base_sha`, `evidence_url` trỏ đúng commit chứa verdict.
2. **`la_canonical: true` và `assurance_dat: cross_approved` có đúng điều kiện không?** Đọc
   `PROTOCOL §8.1` và `:454`. Đặc biệt: hai biên nhận v2 này là v2 ĐẦU TIÊN và THỨ HAI của kho —
   `t26` có thật sự validate lược đồ v2 không, hay chúng qua cổng vì hợp lệ theo v1? Biên nhận tự
   khai điều đó; **kiểm lời tự khai ấy có đúng không**.
3. **`review_rounds_used` cộng có đúng không?** `PLAT-X8` 0→1; `PLAT-X8b` 0→1 với ngân sách RIÊNG.
   Có chỗ nào cộng dồn nhầm hai packet không?
4. **Land evidence** `ops/land/plat-x8-land-evidence.yaml`: `merge_commit`, `authorized_head_sha`,
   `pre_merge_checks`, `post_merge_checks` có khớp thực tế trên `master` không? Nó khai
   `authorization_url: null` — có chỗ nào khác lại khai ngược không?
5. **Đính chính lý do non-canon của lượt 3** — biên nhận lượt 3 nói lý do CŨ của chính nó là SAI.
   Đọc `ADR-0040` và `PROTOCOL:424-440`: **đính chính ấy có đúng không**, hay nó sửa một cái sai
   thành một cái sai khác?
6. **Mục lục `ops/reviews/README.md`**: mọi verdict mới có hàng không (`t27`), mọi caveat trong biên
   nhận có được nâng lên mục lục không?
7. **Câu mô tả VỊ TRÍ artefact** — bài học `CLAUDE.md`: câu nào nói "tệp X nằm ở nhánh Y" phải đúng
   ở CẢ HAI phía của lần merge. Có câu nào sẽ chết đúng lúc PR này land không?

## Danh sách trên là TRẦN, không phải SÀN

Nó liệt kê theo hình dạng hiểu biết của người viết prompt — tức người đã viết chính các tệp này và
do đó mù đúng chỗ họ sai. **Tìm thứ không được giao.** Lượt review trước của chuỗi này tìm được
finding nặng nhất NGOÀI mọi hướng được giao.

## Bằng chứng CI do điều phối cung cấp — và giới hạn của nó

`B-CI-EVIDENCE.md` chứa số đo CI trên exact head. **Đó là lời khai của PHIÊN ĐIỀU PHỐI**, không phải
phép đo của bạn — bạn không có công cụ Actions. Khai đúng như vậy trong verdict, đừng nhận làm của
mình, và cũng đừng báo nó là khoảng trống (lượt trước báo nhầm vì điều phối quên cấp tệp này).

## CẤM

`git push` · `git commit` · sửa kho thật · sửa nhánh đang review. Vá thử làm trên bản sao `/tmp`.

## ĐẦU RA

`verdict` · `assurance` **thực sự đạt** · từng finding đủ **bốn phần** `§441` · bảng số đo (lệnh ·
kết quả · `rc` · thời điểm + head) · **giới hạn của chính lượt này**.
