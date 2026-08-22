# Prompt REVIEWER — `LEASE-DANG-DUNG-MOT-LAN` (#227), lượt **5** — REVIEW DELTA

Lease `lease-dang-review-5-claude-20260822`. **CHỈ ĐỌC.** Không sửa, không commit, không push.

## Neo

- Exact head: **`ba82b06f9df81fc2f13786fec590ec2110d046b7`**
- Nền delta (head lượt trước): **`6eaa3755abd96ef6d8f820daaa6b9d96e2bdd7b5`**
- Nền packet: `cfaccff9bb373274552042e01edb4bfee81dc0ed`
- Đặc tả **r7** `623b23555a6fa43dad2d9badeaac3a6f852c0be6b9927d4593992f6e10310cb4`
  trên nền r6 `4ee67d54…` · r5 `2c8fb5c6…` · r4 `abe7c292…` · r3 `c65d5dbd…` · r2 `3f310582…`
- Verdict lượt 4 `0655b9d0caea1d49450b4b8013f79cd49af61adc62b261bdce2085b76b17614f`

Lấy từ `origin/ops/lease-dang-227`. **KIỂM BĂM; lệch ⇒ DỪNG.**

## Đã đo lại độc lập — đừng chứng minh lại

| phép đo | kết quả |
|---|---|
| `numstat cfaccff9..HEAD` | 3 tệp, **+645/−19** (trần 660) |
| suite thường · suite Actions + `gh` **vắng** | **`68/68` rc=0** cả hai |
| `actionlint` | rc=0, 5 tệp |
| **D3** `if ! cmd` · **D4** `cmd \|\| rc=$?` | mỗi cái **`67/68`** ĐỎ `t64` — ở head trước **cả hai sống sót `67/67`** |
| **A5** gỡ nhánh chặn của khối POST | **`64/68`** ĐỎ `t64 t66 t67 t68` — ở head trước **sống sót `67/67`** |
| **M4** dời `check` xuống sau POST | **`65/68`** ĐỎ `t51 t63 t67` — vẫn giết |
| đếm `bao_chan` | **9**, khớp sổ 9 mục, **không `+1`** |

## Việc — tấn công CHÍNH giả định của danh sách CHO PHÉP

`r7` đảo từ danh sách CẤM (liệt kê cách viết guard) sang danh sách CHO PHÉP (đếm `bao_chan`).
Nước đi ấy **chỉ đúng nếu `bao_chan` là dấu hiệu BẮT BUỘC** của mọi nhánh chặn. Đó là giả định
mới, và nó **chưa ai đo**.

### 1. `bao_chan` có thật là đường DUY NHẤT không?

Executor khai *"chín nhánh lỗi đều gọi `bao_chan`; bốn đường `continue` còn lại là hai bộ lọc đầu
vào và hai đường `rc=9` bỏ qua hợp lệ"*. **Đo, đừng tin.** Dựng những nhánh chặn **không** đi qua
`bao_chan` và xem có lọt không:
- `BI_CHAN=1; echo "::endgroup::"; continue` **viết thẳng**, không gọi `bao_chan`;
- `exit 1` thẳng trong vòng lặp;
- một nhánh **im lặng** `continue` (bỏ lease mà không đặt `BI_CHAN` — mất lease, cổng vẫn xanh);
- đổi tên hàm `bao_chan` thành tên khác rồi gọi tên mới.

Lọt cái nào ⇒ **E lần 2** ⇒ theo chốt `r7` thì verdict phải là `dung_lai`. **Nêu thẳng.**

### 2. Phép đếm có ba trạng thái không?

`t64` đếm `bao_chan` và so với sổ. Nếu thân bước **không trích được** (đổi tên bước, YAML hỏng,
`run` rỗng) thì nó rơi vào **ĐỎ** hay lặng lẽ so `0 == 0`? Ba trạng thái: đếm được · không đếm
được · **đếm ra 0**. Hai cái sau phải **ĐỎ**.

### 3. `t68` có thật đo bốn vế không?

`t68` khẳng định `rc` bước `=1` · `giua` POST **đúng một lần** · `marks["giua"]` là **False**.
Với **mỗi** vế, dựng một đột biến phá **đúng vế đó** và xem `t68` có ĐỎ không. Vế nào không có
đột biến giết được ⇒ vế ấy là trang trí.

Và: đồ giả cho `t68` có **giữ trạng thái** không, hay nó diễn kịch bản? (`gh` trả `rc=1` kèm id
số hợp lệ — kiểm xem comment có **thật sự** được thêm vào danh sách không.)

### 4. Hồi quy

Delta lượt 7 = **một tệp** `ops/lease_publish_test.py`, **+30/−18**. **Mười tám dòng BỊ XOÁ**
trong một tệp phản chứng là thứ phải soi từng dòng — đây là lượt có tỉ lệ xoá cao nhất packet.
`git diff 6eaa3755..ba82b06f -- ops/lease_publish_test.py`
Đặc biệt: việc đổi tên mục #6 thành `post_rc` và thêm `case_id` có làm **ca cũ** nào yếu đi không?

### 5. Bộ đếm hình dạng

**E** = *khoá theo thứ liệt kê được thay vì theo thứ thật sự chặn*, bộ đếm **1**.
`r7` đăng ký: **E lần 2 ⇒ DỪNG**. Mục 1 ở trên chính là phép thử cho nó.

**A** = 6 · **B** = 2 · **C** = 1 · **D** = 3 (người giữ kho quyết không tăng ở lượt trước, có ghi
cả hai cách đọc trong biên nhận lượt 4).

## Ngoài phạm vi — ĐỪNG báo

`ngoai_pham_vi` + `chua_do_duoc` của r2–r7: cửa sổ *"POST xong, `mark` hỏng"* (cấm vá) · khe race
hai nhánh `ops/**` · nợ nền `chay(env=None)` · nhánh *"một phần"* trong `_doc_gh`/
`_kiem_loai_so_hieu`/`_kiem_comment_da_co` · `t59` chỉ so `argv[0:2]` · chưa có Actions thật /
Windows / `gh` thật · ba lượt review đều là review **delta**, không rà toàn bộ diff · ruleset
ngoài kho.
Thấy một mục `chua_do_duoc` khai **hẹp hơn thực tế** thì ĐÓ mới là finding.

## Verdict

```
KET_LUAN: <cross_approved | can_sua | dung_lai>
reviewed_sha: ba82b06f9df81fc2f13786fec590ec2110d046b7
```
Từng finding: **P1/P2/P3** · một câu · **lệnh + đầu ra thật** · đề xuất vá.

Cuối: **`da_do_gi`** · **`khong_do_duoc`**. **"Thu hẹp"** khi chỉ thu hẹp; **"đóng"** chỉ khi có
phép đo.

**Ngân sách còn 15 dòng** (`+645/660`). `can_sua` thì **phải** nói bản vá đề xuất có lọt 15 dòng
không — người giữ kho cần con số ấy.

`cross_approved` thì **nói thẳng cái vẫn còn hở**. Packet đã qua **bảy** lượt vá; một lời
`approve` không kèm danh sách chỗ hở là thứ nguy hiểm hơn `can_sua`.

Nguồn sự thật là **tệp có băm trong kho**; prompt này chỉ là bản chiếu.
