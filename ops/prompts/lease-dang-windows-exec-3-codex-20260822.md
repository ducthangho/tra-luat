# Prompt EXECUTOR — `LEASE-DANG-WINDOWS` (#238), lượt **3** — neo đặc tả **r3**

Lease `lease-dang-windows-exec-3-codex-20260822`. **TIẾP TỤC** lượt 2 (không thay thế).

## Kết quả lượt 2 — đọc kỹ, vì nó quyết định phạm vi lượt này

Cross-review lượt 1 kết luận **`can_sua`** trên `edc1906cf01fcceb15c646e1fdc4fcd8957644ed`.

**`W3′` · `W4` · `W5` ĐẠT, có bằng chứng sơ cấp** — `W3′` là lượt `workflow_dispatch` thật
(`run 32558427472`, `run_attempt 1`, `total_jobs 2`, `failed_jobs 0`, job `windows-latest` XANH).
**Không làm lại ba tiêu chí ấy.**

**`W6` · `W7` · `W8` KHÔNG ĐẠT.** Cả ba đo **HÀM TRỢ GIÚP**, không đo **DÂY NỐI**:

```
P1-1  raise BoQuaNen("hom nay troi mua — khong lien quan runs-on")
      -> 72/72 đạt; đã chạy=72, bỏ qua=1 ; rc=0            <- cửa sau
P1-2  job = job or {"runs-on": "ubuntu-latest"}            # hằng số trá hình
      -> 72/72 đạt; đã chạy=72, bỏ qua=0 ; rc=0
      + YAML đổi sang matrix[ubuntu,windows] KÈM hằng số ấy: vẫn rc=0
        (đây đúng là phép thử mà `W6` tự khai làm chuẩn — nó không đỏ)
```

**Cái sai nằm ở ĐẶC TẢ r2, không ở bản vá của bạn.** `W6`/`W7`/`W8` mô tả *thứ cần đúng* mà
không viết *đột biến nào phải làm nó đỏ ở đâu*. Phiên điều phối viết r2; r3 là bản tự sửa.

Reviewer đếm **bốn** biểu hiện cùng một hình dạng trong một diff 90 dòng (P1-1, P1-2, P2-1, P2-4)
⇒ hình dạng **E** lần **3**: *khoá phần LIỆT KÊ ĐƯỢC (hàm thuần, gọi thẳng được) thay vì phần
THẬT SỰ CHẶN (dây nối trong `main()` / call site)*.

## Nguồn sự thật

1. `{PROMPT_FILE}`
2. **`ops/specs/LEASE-DANG-WINDOWS-r3.md`** — sha256
   `130b6d29919db327ccc2d9ad8d53910e5dd74b2eef0f607d3e59a707647de40d`
3. `ops/specs/LEASE-DANG-WINDOWS-r2.md` (`d9da7705…`) và `ops/specs/LEASE-DANG-WINDOWS.md`
   (`r1`, `f555cbe1…`) — nguyên hiệu lực cho mọi thứ `r3` không nêu.
4. `ops/reviews/lease-dang-windows-review-1-claude-verdict.md` — sha256
   `38b4986dac49c0207cd6c6ccf68e169491065552288169a790c0e7ba49589523`
5. `CLAUDE.md`

**KIỂM BĂM; lệch ⇒ DỪNG.** Cây bắt đầu: `edc1906cf01fcceb15c646e1fdc4fcd8957644ed` trên
`codex/lease-dang-windows-1`.

## Việc — đúng HAI P1, không hơn

### 1. `Q9` (P1-1) — `main()` phải **ĐO LẠI** lý do bỏ qua

Hiện `main()` **nhận lời khai của ca**: ca ném `BoQuaNen("<chuỗi bất kỳ>")` và `main()` tin. Nên
bất kỳ ca nào cũng bỏ qua được vì bất kỳ lý do gì, kể cả lý do không dính `runs-on` chút nào.

`BoQuaNen` phải mang **mỏ neo** `(tệp workflow, tên job)`. `main()` **tự gọi** phép dẫn xuất trên
mỏ neo ấy. Dẫn xuất trả **rỗng** ⇒ ca xếp vào **hỏng**, KHÔNG phải bỏ qua.

Reviewer đề xuất tách `_phan_loai_bo_qua` để ca meta gọi được — cách làm là của bạn, nhưng **ca
meta là bắt buộc**: bơm một `BoQuaNen` với mỏ neo trỏ job **không** ubuntu-only (hoặc không mỏ
neo) ⇒ suite **PHẢI ĐỎ**.

### 2. `Q10` (P1-2) — ca phải **TỰ SINH** chuỗi `runs-on` lúc chạy

`t70` truyền `job=` dựng sẵn nên **chưa từng chạm tệp**; `t72` có đọc tệp nhưng chỉ đòi chuỗi
literal `'ubuntu-latest'`, mà hằng số trá hình thoả luôn.

Ca mới: ghi YAML tạm với `runs-on` là **một chuỗi do chính ca dựng lúc chạy** — chuỗi ấy **không
được xuất hiện ở bất cứ đâu trong mã sản phẩm** — rồi đòi **đúng chuỗi ấy** có mặt trong lý do.
Kèm đối chứng: một nhãn **không** ubuntu-only ⇒ lý do **rỗng**.

Hằng số không thể đoán trước chuỗi mà ca vừa sinh ⇒ **mọi** bản "dọn gọn thành hằng số" đều đỏ,
không cần liệt kê trước các dạng hằng số.

### 3. `Q8` / `W9` — chốt chống tái phát hình dạng **E**, và nó CHẠY ĐƯỢC

Với **mỗi** tiêu chí trong `{W6′, W7′, W8}`:

1. áp **đúng đột biến của tiêu chí ấy** lên mã sản phẩm (bản sao tạm — **CẤM** sửa tệp thật rồi
   khôi phục trong `finally`);
2. **gỡ khỏi suite mọi ca gọi THẲNG hàm trợ giúp** của tiêu chí ấy;
3. chạy lại ⇒ **vẫn phải còn ≥ 1 ca đỏ**.

Không còn ca đỏ nào ⇒ tiêu chí ấy **KHÔNG ĐẠT**. **Khai thẳng và DỪNG** — cấm thay bằng một phép
đo dễ hơn. Đây chính là chỗ lượt trước trượt: `W6`/`W7`/`W8` đều có ca "đạt", và cả ba ca ấy đều
là ca gọi thẳng hàm.

`W8` là ứng viên rõ nhất cho `KHÔNG ĐẠT`: reviewer đo được bỏ vòng `for ten, ly in bo_qua:
print(...)` ⇒ 8 ca biến mất **im lặng**, `rc=0`. Nếu trong ngân sách không đóng nổi `W8` ở mức dây
nối thì **khai KHÔNG ĐẠT**, đừng vay chỗ của hai P1.

## Ngân sách — **cố ý chật**

**≤ 3 tệp, ≤ 120 dòng THÊM so với `ba82b06f`.** Đã dùng **90**; còn **30**. Reviewer định giá hai
P1 ≈ **29** dòng.

Vượt ⇒ **DỪNG**, báo **số dòng đo được** cần thiết và chỗ vượt. **CẤM thu nhỏ phép đo cho vừa
ngân sách** — đó đúng là cách `W6`/`W7` ra đời ở lượt trước.

## CẤM — bảy mục còn lại KHÔNG thuộc lượt này

`P2-1` `P2-2` `P2-3` `P2-4` `P3-1` `P3-2` `P3-3` của verdict lượt 1 **để ngoài có chủ đích**, vào
packet kế tiếp **có tên**. Chúng là lỗi thật, đã đo — nhặt thêm "vì tiện tay" nghĩa là mục ấy
không có ai review đúng phạm vi của nó.

Riêng **`P2-2`** (dẫn xuất MỘT CHIỀU: workflow windows-only vẫn chạy trên Linux) trông rất gần
`Q10`. **Vẫn CẤM** — nó đổi hành vi bỏ qua theo chiều ngược lại và cần phép đo riêng.

Cũng cấm: sửa `ops/specs/**`, `ops/reviews/**`; đụng hai finding của verdict `#227` lượt 5 (chúng
ở **#235**).

## Cổng

| cổng | tiêu chí |
|---|---|
| `python3 ops/lease_publish_test.py` | `rc=0`, `N/N` hai số **bằng nhau** |
| cùng suite, ba biến GitHub đặt, `gh` **vắng** | `N/N` y hệt |
| `actionlint .github/workflows/*.yml` | `rc=0` cả 5 |
| **`shellcheck` PHẢI có mặt** khi chạy `actionlint` | thiếu ⇒ in **KHÔNG ĐO ĐƯỢC** và **ĐỎ** |
| phản chứng P1-1 | `BoQuaNen` mỏ neo không-ubuntu ⇒ suite **ĐỎ** |
| phản chứng P1-2 | `job = job or {'runs-on': 'ubuntu-latest'}` ⇒ suite **ĐỎ** |
| phản chứng P1-2 (b) | hằng số trá hình **+** YAML matrix[ubuntu,windows] ⇒ suite **ĐỎ** |
| `W9` cho `W6′` · `W7′` · `W8` | mỗi cái **≥ 1 ca đỏ** sau khi gỡ ca gọi thẳng |
| đột biến quyết định của `#227` | `M1`–`M4` · `A5` · `D3`/`D4` · tám đột biến gỡ guard — **vẫn phải giết** |
| `git diff --numstat ba82b06f..HEAD` | ≤ 3 tệp, ≤ **120** dòng thêm |

## Bạn KHÔNG chạy được `workflow_dispatch`

`W3′` **đã đạt trên `edc1906c`** — nhưng head sẽ đổi, và **bằng chứng cũ không chuyển sang head
mới**. Phiên điều phối chạy lại Windows thật trên exact head của bạn trước khi land. Suite xanh
trong sandbox **chưa phải bằng chứng**: `#227` có bốn lượt xanh như thế rồi vẫn đỏ ở CI.

## Handoff — **bắt buộc**, và phải quy kết ĐÚNG

Ghi `ops/handoff/lease-dang-windows-exec-3-codex-handoff.md`.

Handoff lượt 2 khai **"W6 | 1/1 | t70"**. **Sai quy kết** — `t70` không đỏ ở **bất kỳ** đột biến
`runs-on` nào; ca duy nhất đỏ trong cả sáu đột biến YAML là `t72`. Reviewer bắt được vì chạy lại.

Với **mỗi** tiêu chí, handoff phải nêu: **đột biến · vị trí (tệp:dòng) · TÊN CA đã đỏ THẬT ·
`N/N`**. Tên ca phải là ca **đã quan sát thấy đỏ**, không phải ca bạn nghĩ sẽ đỏ.

## Báo cáo cuối

1. `git diff --numstat ba82b06f..HEAD` — số thật, và số còn lại trong trần 120.
2. `N/N` hai lần chạy. Kèm phiên bản `actionlint` và `shellcheck`.
3. Bảng `W9`: `tiêu chí · đột biến · ca đã gỡ · ca còn đỏ · N/N`.
4. Ba phản chứng P1-1/P1-2/P1-2(b) — mã thoát và ca đỏ.
5. Tiêu chí nào **KHÔNG ĐẠT** — khai thẳng, kèm lý do đo được.
6. `chua_do_duoc`.

Nguồn sự thật là **tệp có băm trong kho**; prompt này chỉ là bản chiếu.
