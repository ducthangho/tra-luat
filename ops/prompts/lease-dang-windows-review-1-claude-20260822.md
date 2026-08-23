# Prompt REVIEWER — `LEASE-DANG-WINDOWS` (#238), lượt 1

Lease `lease-dang-windows-review-1-claude-20260822`. **CHỈ ĐỌC.** Không sửa, không commit, không push.

## Neo

- Exact head: **`edc1906cf01fcceb15c646e1fdc4fcd8957644ed`**
- Nền packet: `2ab3560a` (`master`) · nền so cho `write_set`: **`ba82b06f`** (head của `#227` đã bị revert)
- Đặc tả **r2** `d9da7705617c95c8dc394d773de8456712d3cc2a2975e5903e8cb28c934c0d83`
  trên nền **r1** `f555cbe1a368c12040726dd706ce25ed8dd4041bd8a2f840590810a3c3908a26`
  (**`Q3` của r1 ĐÃ BỊ THAY bằng `Q3′`**)
- Lấy từ `origin/ops/pkg-windows`. **KIỂM BĂM; lệch ⇒ DỪNG.**

## Đã đo lại độc lập — đừng chứng minh lại

| phép đo | kết quả |
|---|---|
| `git diff --numstat ba82b06f..HEAD -- <write_set>` | **2 tệp, +90/−20** (trần 90) |
| `ops/lease_publish.py` vs `ba82b06f` | **khớp BYTE-FOR-BYTE** |
| suite thường · suite Actions + `gh` **vắng** | **`72/72` rc=0**, `đã chạy=72, bỏ qua=0` cả hai |
| `actionlint` trên `ops-publish-lease.yml` (thứ `t33` **thật sự** lint) | rc=0, `shellcheck 0.9.0` **có mặt** |
| **`workflow_dispatch` THẬT** run **`32558427472`** trên exact head | `conclusion: success`, `run_attempt: 1`, `total_jobs: 2`, `failed_jobs: 0` · **`gate (windows-latest)` success**, bước `lease-publish selftest` **success** · `gate (ubuntu-latest)` cùng vậy |

**`W3′` đã đạt.** Đây là lần đầu trong chuỗi `#227`→`#238` bản vá được đo trên cả hai nền **trước**
khi land.

## Bối cảnh — đọc kỹ, nó quyết định trọng tâm

`#227` land rồi CI master **ĐỎ trên Windows** (`59/68`), phải revert (`#237`). Chín ca đỏ đều là
ca **mới** của `#227` và **chưa ca nào từng chạy trên Windows**.

Chẩn đoán đã chốt: `ops-publish-lease.yml` khai **`runs-on: ubuntu-latest`**; tám ca đi qua
`_chay_buoc_dang` **trích thân bước từ workflow ấy** ⇒ trên Windows chúng đo **một thứ không bao
giờ chạy ở đó**. `r2/Q3′` cho phép bỏ qua theo nền **CHỈ KHI phạm vi nền DẪN XUẤT ĐƯỢC từ
`runs-on`** — **không danh sách viết tay**. `t49` **không** thuộc diện ấy (`Q6`): nó đo mối nối
`GOI_GH`, phải **vá thật**.

## Việc — tấn công CHÍNH phép dẫn xuất

`#227` đã hai lần bị bắt vì "khoá theo thứ liệt kê được thay vì thứ thật sự chặn". Câu hỏi đúng ở
đây **không** phải *"có xanh không"* mà **"phép dẫn xuất có THẬT không, hay là danh sách trá hình"*.

1. **Nó đọc `runs-on` TỪ ĐÂU?** Từ chính tệp YAML, hay từ một hằng số/bảng trong tệp test? Nếu ca
   nào đó ghi sẵn tên workflow hoặc tên nền thì đó là danh sách trá hình.
   - Đổi `runs-on` của `ops-publish-lease.yml` thành `windows-latest` **thuần** ⇒ tám ca phải chạy
     trên Windows và **bỏ qua trên Linux**. Có đảo đúng chiều không?
   - `runs-on` viết dạng **matrix** / **biểu thức `${{ }}`** / **danh sách YAML** / **tên job khác**
     ⇒ rơi vào trạng thái nào? **Ba trạng thái**: dẫn xuất được · không dẫn xuất được · rỗng. Hai
     cái sau **phải ĐỎ**, không được lặng lẽ "coi như chạy được ở mọi nền".
   - Đổi **tên bước** hoặc **tên job** ⇒ ĐỎ hay lặng lẽ bỏ qua?
2. **`W7` có thật chống cửa sau không?** Dựng một ca bỏ qua theo nền mà workflow của nó **không**
   ubuntu-only — có ĐỎ không? Và một ca bỏ qua **không** vì `runs-on` chút nào (vd theo biến môi
   trường) — có lọt không?
3. **`W8`**: ca bị bỏ qua có **in ra** lý do kèm `runs-on` không? Bỏ dòng in ⇒ ĐỎ? Tổng kết có
   khai **số đã chạy / số bỏ qua** không? *"Ca có MẶT khác ca có ĐO."*
4. **`t49` có thật được VÁ, không phải bỏ qua trá hình?** Nó phải **chạy** trên Windows. Kiểm rằng
   nó không rơi vào diện `Q3′` bằng bất kỳ đường nào.
5. **`W1`/`W2`**: gỡ riêng `rc`, `stdout`, `stderr` ⇒ ĐỏÍ từng cái? Còn chỗ nào đọc tệp do đồ giả
   sinh mà **chưa** được bọc không? Executor khai đã bọc *"mọi chỗ"* — **đo lời khai ấy**.
6. **Hồi quy**: `+90/−20`, trong đó **20 dòng bị xoá**. Từng dòng phải có lý do.
   `git diff ba82b06f..edc1906c -- ops/lease_publish_test.py .github/workflows/ops-publish-lease.yml`
   Và: toàn bộ đột biến quyết định của `#227` (`M1`–`M4` · `A5` · `D3`/`D4` · tám đột biến gỡ
   guard) **vẫn phải giết**. Executor khai `21/21`; chọn ít nhất **năm** cái chạy lại.

## Ngoài phạm vi — ĐỪNG báo

Hai finding của verdict `#227` lượt 5 (`bao_chan` khoá theo **cách viết** · mất bất biến
`set +e … rc=$? … set -e`) — chúng ở **#235**.
`ops-don-ref.yml:106 SC1003:info` — finding **nền**, ngoài write set, `t33` không lint tệp ấy.
Cộng mọi `ngoai_pham_vi`/`chua_do_duoc` của `#227` r2–r7 và của `#238` r1/r2.

## Verdict

```
KET_LUAN: <cross_approved | can_sua | dung_lai>
reviewed_sha: edc1906cf01fcceb15c646e1fdc4fcd8957644ed
```
Từng finding: **P1/P2/P3** · một câu · **lệnh + đầu ra thật** · đề xuất vá.
Cuối: **`da_do_gi`** · **`khong_do_duoc`**.

**Ngân sách đã CẠN** (`+90/90`). `can_sua` thì **phải** nói bản vá đề xuất cần bao nhiêu dòng —
người giữ kho cần con số ấy để quyết có nới trần không.

`cross_approved` thì **nói thẳng cái vẫn còn hở**. Chuỗi này đã có một lần land rồi phải revert;
một lời `approve` không kèm danh sách chỗ hở là thứ nguy hiểm hơn `can_sua`.

Nguồn sự thật là **tệp có băm trong kho**; prompt này chỉ là bản chiếu.
