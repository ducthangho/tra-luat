# Cross-review lượt 4 — `PLAT-X8` (#225 / PR #248) — VÒNG CANON

Bạn là **REVIEWER**, phiên `claude` RIÊNG, read-only. Executor là `codex` ⇒ **cross-provider**
(`cross_approved` đạt được theo `PROTOCOL §8.1`). Đây là **VÒNG CANON**: packet còn đúng hai vòng
theo `ADR-0043`, lượt này tiêu một vòng. Ba lượt trước đều `la_canonical: false`.

## Thẩm quyền — có lease, kiểm nó trước

Lease reviewer của CHÍNH lượt này: `ops/leases/plat-x8-review-4-claude-20260822.yaml`, trên nhánh
`ops/cap-lease-plat-x8-2`. **Tự kiểm nó tồn tại** trước khi làm gì khác:

```bash
git ls-tree -r --name-only origin/ops/cap-lease-plat-x8-2 -- ops/leases/ | grep review-4
```

Không thấy ⇒ `git fetch origin '+refs/heads/*:refs/remotes/origin/*'` rồi đo lại; vẫn không thấy
thì **DỪNG và khai `blocked`**. Lượt trước của chính packet này chạy KHÔNG có lease vì phiên điều
phối quên cấp — nó tự phát hiện và tự khai, và đó là lý do có dòng này.

## Neo

- exact head **`28f32f7cfb393c759e73e8afbb566a54866fc4b4`** · base `08bb4ecd6dbdb87267cb8179f52ac28c151eb4b9`
- cây đọc: clone rời, detached đúng head trên. KHÔNG phải kho thật.
- đặc tả · diff · numstat · ba verdict trước · `A12-EVIDENCE.md`: đường dẫn cụ thể nằm trong
  tin nhắn khởi động của lượt chạy. Prompt này CỐ Ý không chép đường dẫn tuyệt đối — đường dẫn
  là thứ duy nhất không mang được sang máy khác, và prompt bị lease neo băm nên phải sống lâu
  hơn một sandbox.

## HAI LUẬT REVIEW (`PROTOCOL §8`) — luật, không phải cú pháp

### L-A. Reviewer phải ĐO ĐƯỢC, không chỉ ĐỌC

Mọi khẳng định phải kèm **lệnh đã chạy + kết quả thật + `rc` đọc TRỰC TIẾP** (`echo $?` ngay sau
lệnh; KHÔNG qua pipeline, KHÔNG `$( )` cùng chuỗi `echo` — cả hai đã nuốt mã thoát thật ở kho này).
Không đo được thì viết **`KHÔNG ĐO ĐƯỢC`** kèm lý do: đó là **trạng thái thứ ba**, không được gộp
vào "không có vấn đề". **Suy luận có căn cứ KHÔNG phải phép đo** — suy thì nói là suy.

### L-B. ĐỐI CHIẾU LƯỢT TRƯỚC — bắt buộc từ lượt 2

Trả lời tường minh ba câu: (1) finding nào còn MỞ, và đã đóng THẬT chưa — **ĐO**, đừng tin nhãn
`DA_DONG` trong biên nhận; (2) lượt trước có kết luận nào SAI không — lượt 3 đã chứng minh lượt 1
và 2 sai một chỗ nặng, nên lượt 3 cũng sai được, soi nó như soi mã; (3) bản vá đáp lại lượt trước
đẻ ra gì mới — diff bạn đang xem CHÍNH LÀ bản vá ấy, và một lượt review không bảo chứng được cho
bản vá của chính nó. Thiếu phần này ⇒ verdict **chưa hoàn chỉnh**.

### L-C. Mọi con số kèm THỜI ĐIỂM ĐO

Ghi rõ đo lúc nào, trên head/ref nào. Packet này sập vì chuyện đó bốn lần (265→313→328;
82/82→85/85→87/87). Trước khi công bố, **đo lại**, đừng chép.

## VIỆC RIÊNG LƯỢT NÀY — người giữ kho chỉ thị

Tìm ra vấn đề ⇒ **THỬ VÁ VÀ KIỂM CHỨNG**: dựng **bản sao cả cây** trong `/tmp` (KHÔNG đụng cây
review), vá ở đó, chạy `python3 ops/lease_publish_test.py` đọc `rc` trực tiếp, viết **ca test khoá
lỗi**, rồi **ĐỘT BIẾN gỡ vá ra để chứng minh ca ấy ĐỎ**. Gửi về dạng **GỢI Ý VÁ** kèm patch chạy
được và số đo thật. Gợi ý là gợi ý — người vá là executor.

## Hai hình dạng suy luận đã cắn kho này

- **BẤT BIẾN ĐÚNG CHE SỐ HẠNG SAI.** Đã xảy ra ở chính packet này: `write_set` thật ra `sensitive`
  ĐÚNG, nhưng chỉ vì `max()` lấy tệp ĐẦU; tệp THỨ HAI phân sai lớp, bị che suốt hai lượt. Thấy một
  tổng đúng thì hỏi: **từng số hạng có đúng không, hay chỉ phép gộp cứu nó?**
- **DANH SÁCH GIAO CHO REVIEWER LÀ TRẦN, KHÔNG PHẢI SÀN.** Mọi thứ liệt kê dưới đây là mức TỐI
  THIỂU, và nó giới hạn tầm nhìn theo đúng hình dạng hiểu biết của người VIẾT prompt — tức người
  đã bỏ sót. P1 của lượt 3 **không nằm trong hướng nào** được giao; nó lộ ra vì reviewer hỏi một
  câu không ai giao. **Tìm thứ không được giao.**

## Diff đang review

Bản vá P1 của lượt 3: xoá 4 mục `systemic` khỏi `_BANG_LOP`, sửa `t77`, thêm `t86`/`t87`.
Điều phối khai: suite `87/87` `rc=0`; đột biến khôi phục 4 mục ⇒ `85/87` `rc=1`, `t86`+`t87` ĐỎ.
**ĐỪNG nhận — chạy lại.** Lời khai của điều phối cũng là lời khai.

Vài chỗ đáng hỏi (TRẦN, không phải sàn):
- `t86` đòi MỌI mục `_BANG_LOP` là `sensitive`. Nếu sau này kho **được phép** nới bảng đúng quy
  trình §8 thì ca này ĐỎ. Ý định hay giòn quá tay?
- `t77` bơm mục `routine` TẠM vào `mod._BANG_LOP`. Có rò sang ca khác không?
- Bảng seed nay chỉ còn `sensitive`. Vậy `_THU_TU_LOP` và nhánh `routine`/`systemic` của
  `_tinh_lop_tu_write_set` còn ca nào phủ **vế DƯƠNG** không, hay đã thành mã chết không ai đo?

## `A12` — ĐÃ CÓ BẰNG CHỨNG, việc của bạn là KIỂM nó, không phải báo thiếu

Lượt trước khai `A12` chưa đo lại trên head mới. Sai — nó đã chạy, reviewer khi ấy không có công cụ
để thấy. Bằng chứng: `workflow_dispatch` **run `32592693727`** trên `28f32f7c`, cả hai job
`gate (ubuntu-latest)` và `gate (windows-latest)` = `success`, **0 bước hỏng**. Số đo đầy đủ ở
`A12-EVIDENCE.md`. Bạn **không có** công cụ Actions; nên với `A12`, việc của bạn là đọc tệp bằng
chứng ấy và khai đúng rằng đó là **lời khai của phiên điều phối**, không phải phép đo của bạn —
đúng như `plat-x5-review-2` đã làm. Đừng báo nó là khoảng trống.

## Hợp đồng finding (`PROTOCOL:436-451`) — BỐN phần bắt buộc

**vá ở đâu** · **vá thế nào** · **ca test khoá nó + đột biến nào phải chết** · **bản vá đẻ ra gì**.
Không nghĩ ra phần nào thì nói thẳng. Finding không có gợi ý, hoặc gợi ý chỉ nhắc lại chính
finding, ⇒ verdict **chưa hoàn chỉnh**.

## CẤM

`git push` · `git commit` · sửa kho thật · sửa nhánh `codex/plat-x8-exec-2`. Vá thử làm trên **bản
sao trong `/tmp`**.

## ĐẦU RA

`verdict` (`approve`/`changes_requested`/`blocked`) · `assurance` **thực sự đạt** (đừng khai theo
mục tiêu; nếu thiếu điều kiện nào thì khai thiếu) · phần **ĐỐI CHIẾU LƯỢT TRƯỚC** · từng finding đủ
bốn phần · bảng số đo (lệnh · kết quả · `rc` · thời điểm + head) · **giới hạn của chính lượt này**.
