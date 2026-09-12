# TIẾP TỤC lượt cross-review #512 vòng 6 — lần ngắt THỨ BA, và lần này bạn KHÔNG mất gì

Bạn bị cắt lần nữa lúc ~10:41Z, vẫn vì **container bị recycle** (uptime đo 11:10Z: **0,6 phút**), không
vì bất cứ điều gì trong việc bạn làm. Đây là lần ngắt thứ ba của lượt này.

**Chỉ thị ghi-sau-mỗi-phát-hiện đã có tác dụng đo được: `VERDICT.md` trên đĩa đi từ 1 089 lên 11 688
byte.** Giữ đúng nếp đó — nó là thứ duy nhất đang giữ lượt này sống.

## Thứ ĐÃ nằm trên đĩa và KHÔNG cần làm lại

`VERDICT.md` hiện có đủ `## ĐỐI CHIẾU LƯỢT TRƯỚC` (bảy lớp + năm thể hiện), `## BẢNG ĐO`,
`## Findings theo lớp` (F2, F6, F7), `## Mutant đã chạy` (N01–N18 + catalogue 16), `## chua_do_duoc`.
Đọc lại chính tệp ấy trước khi làm gì — đừng đo lại thứ đã đo.

Tóm tắt để bạn định hướng, không thay cho việc đọc tệp: F1 F3 F4 F5 = **ĐÃ VÁ THẬT**;
F2 F6 F7 = **VÁ HỜ**; mutant còn SỐNG: **N01 N02 N10 N12 N17 N18** (N09 là tương đương, không finding).

## Việc còn lại — đúng bốn việc, theo thứ tự này

1. **Chốt thứ hạng và số đếm.** Đổi `so_p1`/`so_p2`/`so_p3`/`so_the_hien` từ `pending_final_audit`
   thành SỐ THẬT (đếm theo **LỚP**), và đổi `verdict:` từ `in_progress` thành `changes_requested` hoặc
   `approve`. Ghi đĩa ngay sau khi đổi.
2. **Nộp `HINT.patch`.** Có `scratch/luot1/HINT.final-candidate.patch`; bạn đã ghi là chạy lại N01–N18
   trên nó cho 17 chết đúng chốt. Hãy `patch -p0 --dry-run --fuzz=0` từ gốc `cay-kho/`, báo **số hunk
   và số tệp** vào verdict, rồi copy ra `HINT.patch` ở thư mục gốc và điền `hint_sha256`. **Chỉ chạm hai
   tệp write set.** Đừng đưa bản vá cho `cong-cu/dotbien512.py` vào HINT — nó ngoài write set; khai bằng
   lời như bạn đã làm.
3. **Đọc khối `nang_tran` S2.** `git -C cay-kho show 2d0ee53:ops/leases/windows-lease-suite-exec-1-claude-20260911.yaml`
   — commit ấy nằm trên nhánh `ops/cap-lease-504`; nếu ref chưa có trong clone thì nói **KHÔNG ĐO ĐƯỢC**
   chứ đừng suy. Kiểm hai điều: phép đo `+1082 ≤ 1500` có tái lập được không, và khối có tự khai đúng
   rằng **`A5` của đặc tả đóng băng vẫn là 300 nên đây là OVERRIDE chứ không phải "A5 đạt"**. Khai rộng
   hơn phép đo ⇒ finding. Bạn **không** phán xử thẩm quyền nâng trần.
4. **Rà lại `## chua_do_duoc`** cho khớp trạng thái cuối.

Nếu lại bị cắt: mọi thứ đã ghi đĩa vẫn dùng được. Nếu hết thời gian mà chưa xong việc 1, hãy để
`verdict: in_progress` và nói rõ việc nào chưa chạy — một lượt khai thật phần dở vẫn dùng được; một lượt
khai `approve` khi chưa đo thì không.

`cay-kho/` vẫn detached **`353eae10120da2a1788dcaf7a906fe46261bd71b`**, `git status --porcelain` RỖNG.

Dòng cuối stdout: `XONG VERDICT sha256=<sha256 của VERDICT.md>`.
