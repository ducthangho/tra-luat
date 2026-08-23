# Prompt REVIEWER — `LEASE-DANG-WINDOWS` (#238), lượt **2**. Neo exact head `b0c8fb3`.

Bạn review chéo bản vá của `codex` cho packet `#238`, kho `ducthangho/tra-luat`.
**Chỉ đọc; không sửa kho.** Bản sao ghi được là của bạn, muốn đột biến gì thì đột biến ở đó.

## Nguồn sự thật — KIỂM BĂM TRƯỚC, lệch ⇒ DỪNG

| gì | ở đâu | sha256 |
|---|---|---|
| đặc tả **r3** | `ops/specs/LEASE-DANG-WINDOWS-r3.md` | `130b6d29919db327ccc2d9ad8d53910e5dd74b2eef0f607d3e59a707647de40d` |
| đặc tả r2 | `ops/specs/LEASE-DANG-WINDOWS-r2.md` | `d9da7705617c95c8dc394d773de8456712d3cc2a2975e5903e8cb28c934c0d83` |
| đặc tả r1 | `ops/specs/LEASE-DANG-WINDOWS.md` | `f555cbe1a368c12040726dd706ce25ed8dd4041bd8a2f840590810a3c3908a26` |
| verdict lượt 1 | `ops/reviews/lease-dang-windows-review-1-claude-verdict.md` | `38b4986dac49c0207cd6c6ccf68e169491065552288169a790c0e7ba49589523` |
| handoff lượt 3 | `ops/handoff/lease-dang-windows-exec-3-codex-handoff.md` | `2d5302fc687ed9ffc8002bbef6c8f8647d1036cd0f688db0e3d85fcd83d122f4` |

Hồ sơ nằm trên nhánh `ops/pkg-windows` (chưa vào `master`): tìm ở `master` trước, chưa thấy thì
`git fetch origin ops/pkg-windows`. **Thứ định danh tệp là BĂM, không phải tên nhánh.**

Mã cần review: `codex/lease-dang-windows-1` @ **`b0c8fb368d70f17bce5eb7e3d1fe02d810db8e19`**.
Nền đo ngân sách: `ba82b06f9df81fc2f13786fec590ec2110d046b7`.

## Chuyện đã xảy ra, ngắn

Lượt 2 (`edc1906c`) bị verdict lượt 1 kết `can_sua`: `W6`/`W7`/`W8` **không có răng** — cả ba đo
HÀM TRỢ GIÚP chứ không đo DÂY NỐI. Bốn biểu hiện cùng hình dạng trong một diff 90 dòng ⇒ **E lần 3**.

Người giữ kho nới trần **90 → 120**, phạm vi **CHỈ hai P1**. Đặc tả **r3** thêm `Q8`–`Q11` và
`W6′`/`W7′`/`W9`.

## SOI ĐẶC TẢ r3 TRƯỚC, BẢN VÁ SAU

**Ba lượt của packet trước hỏng ở ĐẶC TẢ, không ở bản vá.** r3 do phiên điều phối viết — cùng bên
đã viết r2 hỏng. Câu hỏi sắc nhất, và nó là câu tôi tự nghi bản của mình:

> **`Q8` có răng không, hay nó cũng chỉ là văn xuôi?** `Q8` bảo: một tiêu chí chỉ ĐẠT khi, sau khi
> gỡ mọi ca gọi thẳng hàm trợ giúp, đột biến vẫn còn ≥1 ca đỏ. **Nhưng ai cưỡng chế việc đó đã
> được làm?** Hiện tại: **không ai** — nó là một dòng trong handoff. Nếu đúng vậy thì `Q8` là
> chính hình dạng **E** ở một tầng cao hơn: một luật sống trong tài liệu, không sống trong cổng.
> **Đo, rồi kết luận.** Nếu đúng là không có cổng nào giữ `Q8`, nói thẳng — kể cả khi bản vá đạt.

## Phải đóng, và phải đo bằng chạy

`P1-1` và `P1-2` của verdict lượt 1. Phiên điều phối **đã đo độc lập** — hãy kiểm lại tôi, tôi có
thể sai:

```
suite tren b0c8fb3                 72/72 đạt; đã chạy=72, bỏ qua=0 ; rc=0
P1-1  raise BoQuaNen()  khong mo neo   72/73; bỏ qua=0 ; rc=1     (verdict cu: 72/72; bỏ qua=1; rc=0)
P1-2  job = job or {"runs-on": "ubuntu-latest"}   70/72 ; rc=1
ngan sach write-set ba82b06f..b0c8fb3   +116/-20, 2 tep   (tran 120)
actionlint 5 workflow: origin/master rc=1 voi DUNG mot finding y het
  (ops-don-ref.yml:106 SC1003:info); b0c8fb3 cung vay  =>  DELTA = 0
```

**Cảnh báo về chính phép đo P1-1:** lần dựng đột biến đầu tiên của tôi chèn vào giữa dòng gạch
ngang ⇒ `SyntaxError` ⇒ `rc=1`. Dừng ở `rc` thì đã tính là "đỏ đúng". Mọi đột biến của bạn phải
qua `ast.parse` **trước** khi tin con số.

## Sáu chỗ tôi nghi — mỗi chỗ phải trả lời bằng MỘT PHÉP CHẠY, không bằng đọc mã

1. **`W9` cho `W7′` gỡ `t70`** — nhưng `t70` không phải ca gọi thẳng dây nối của `W7′` (dây nối
   của `W7′` nằm trong `main()`). Handoff tự gọi nó là *"ca gọi thẳng helper dùng chung"*. Thủ tục
   `W9` ở đây có đo gì không, hay chỉ gỡ một ca không liên quan rồi tuyên đạt?
2. **`W9` cho `W8` KHÔNG gỡ ca nào** (*"không có ca gọi thẳng `_dong_tong_ket`"*). Vậy `W9` cho
   `W8` **rỗng theo cấu tạo**. `W8` có răng thật không? Đột biến **riêng rẽ**: (a) bỏ vòng in lý do;
   (b) hạ tổng kết về dạng cũ `{qua}/{len(CA)}`. Verdict lượt 1 đo được cả hai đều `rc=0`.
3. **`except Exception: ly_do = ""`** trong `main()` nuốt lỗi dẫn xuất. Nó ngã về `hong` nên
   fail-close — nhưng nó **gộp "KHÔNG ĐO ĐƯỢC" vào "hỏng"**, đúng ranh giới `P2-3` đang mở, và nó
   sẽ nuốt luôn một lỗi thật (đường dẫn sai, YAML hỏng) mà không ai biết. Đo hậu quả.
4. **Chuỗi tự sinh của `Q10`**: `t72` dựng `"ubuntu-" + tên tạm ngẫu nhiên`. Tiền tố `ubuntu-` là
   **cố định trong mã**. Có hằng số nào thoả được phép đo ấy không? Thử.
5. **Tám ca `_chay_buoc_dang`** có thật sự đi qua phép dẫn xuất trên workflow THẬT không, hay chỉ
   hai ca meta mới chạm tệp? Đổi `runs-on` của `ops-publish-lease.yml` sang `windows-latest` thuần,
   sang matrix, sang `${{ env.X }}`, sang rỗng — mỗi dạng rơi vào trạng thái nào, trên nền nào?
6. **Ba trạng thái**: `có` · `không` · `KHÔNG ĐO ĐƯỢC`. Trạng thái thứ ba có tồn tại trong bản vá
   này không, hay vẫn bị gộp?

Nghĩ ra thêm hướng nào thì **chạy nó**, đừng để nó nằm trong verdict dưới dạng câu chữ — chỗ đó là
nơi các ca đi chết.

## NGOÀI PHẠM VI — đừng báo lại thành phát hiện mới

`P2-1` `P2-2` `P2-3` `P2-4` `P3-1` `P3-2` `P3-3` của verdict lượt 1 **cố ý để ngoài** vì ngân sách;
chúng vào packet kế tiếp có tên. **Nhưng:** nếu bản vá lượt 3 làm **nặng thêm** mục nào trong đó,
đó là phát hiện MỚI và phải báo.

## Ngân sách

Đã dùng **116/120**, còn **4 dòng**. `can_sua` ⇒ **PHẢI nói bản vá đề xuất cần bao nhiêu dòng** —
người giữ kho cần con số ấy để quyết có nới trần lần nữa không.

## Điều kiện DỪNG

Hình dạng **A** lần 8 · **B** lần 3 · **C** lần 2 · **D** lần 4 · **E** lần **4** · **F** lần 3
⇒ DỪNG, kết `can_sua`, không đề xuất vá tiếp.

## Xuất

```
KET_LUAN: dat | can_sua | tu_choi
reviewed_sha: b0c8fb368d70f17bce5eb7e3d1fe02d810db8e19
```

Mỗi phát hiện: **mức (P1/P2/P3) · phép đo đã CHẠY · số · vì sao nó quan trọng**. Không có phép
chạy thì không phải phát hiện. Kèm mục `chua_do_duoc` và bộ đếm `hinh_dang_ke_thua` sau lượt này.

Nguồn sự thật là **tệp có băm trong kho**; prompt này chỉ là bản chiếu.
