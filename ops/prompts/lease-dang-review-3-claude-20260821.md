# Prompt REVIEWER — `LEASE-DANG-DUNG-MOT-LAN` (#227), lượt **3** — REVIEW DELTA

Bạn là **reviewer** lượt 3. Lease `lease-dang-review-3-claude-20260821`.
**CHỈ ĐỌC.** Không sửa mã, không push, không commit.

**Đây là review DELTA, không phải review lại từ đầu.** Lượt 2 đã duyệt phần lớn; chỉ còn một P1
và ba P3, và lượt vá 3 nhắm đúng bốn thứ đó.

## Neo

- Exact head: **`9f5b08e81a131a1c22d15b6d5809885eae11413f`**.
- Nền delta (head lượt 2): **`90015a53c7407400f87c9f5a018067849fa1e842`**.
- Nền packet: `cfaccff9bb373274552042e01edb4bfee81dc0ed`.
- Delta lượt này **chỉ chạm `ops/lease_publish_test.py`**: **+37/−12** so với `90015a53`. Mười
  hai dòng BỊ XOÁ trong một tệp phản chứng là thứ phải soi — xem mục 4.
- Đặc tả **r3 (delta)** `c65d5dbd9d2b398978226f6863cf7cd4e4ddb219a7086be0005e65804a0f47da`,
  trên nền **r2** `3f310582de59dce7c109717dbab13ef9467b80c67ffeafc0ac8e1484309e0093`.
- Verdict lượt 2 `f21069548bf0e0ff507822a246283fe47417bc334fa1e231b2e71dc88d52b4c0`.

Lấy từ `origin/ops/lease-dang-227`. **KIỂM BĂM; lệch ⇒ DỪNG.**

## Đã đo lại độc lập — đừng tiêu thời gian chứng minh lại

Phiên điều phối, trên `9f5b08e8`:

| phép đo | kết quả |
|---|---|
| `git diff --numstat cfaccff9..HEAD` | 3 tệp, **+523/−19** (trần 550) |
| suite thường | `rc=0`, **61/61** |
| suite, `GITHUB_ACTIONS`+`GITHUB_REPOSITORY`+`GITHUB_ACTOR` đặt, `gh` **vắng** | `rc=0`, **61/61** |
| `actionlint` | `rc=0`, 5 tệp |
| **D10** xoá khối gọi `kiem-github` khỏi YAML | **59/61** — `t59` + `t60` ĐỎ (lượt 2: sống sót `58/58`) |
| **D11** gọi nhưng nuốt mã thoát | **60/61** — chỉ `t60` ĐỎ (lượt 2: sống sót `58/58`) |

## Việc của bạn — **đo, đừng đọc**

### 1. `t59`/`t60` có thật sự canh THỨ THẬT không?

P1 lượt 2 là *"phản chứng bắt buộc còn thiếu"*. Bản vá thêm hai ca. Câu hỏi đúng **không** phải
"chúng có xanh không" mà là **"chúng đo cái gì"**:
- Chúng đọc **chính `.github/workflows/ops-publish-lease.yml`** hay một bản chép/hằng số trong
  test? Nếu là bản chép thì hai bản sẽ trôi lệch và ca này chết âm thầm — đúng bài học của kho.
- `t59` đòi thứ tự `kiem-github` **trước** `check`. Có đột biến nào **đảo thứ tự** mà nó vẫn xanh
  không? Dựng và chạy.
- `t60` đòi `kiem-github` rc≠0 ⇒ không POST **và** bước rc≠0. Đo **cả hai vế** riêng: một đột
  biến chỉ phá vế "không POST", một đột biến chỉ phá vế "rc≠0".
- Có đường nào **gọi `kiem-github` sau `check`**, hoặc gọi nó cho lease này mà bỏ lease kia, mà
  `t59` vẫn xanh không?

### 2. `T53` — executor chọn đường (b): HẠ LỜI KHAI

r3 cho hai đường và đòi khai rõ. Executor chọn **(b)**: đổi mô tả `t53` từ *"toàn suite"* thành
*"một lệnh `check` trong Actions không có `gh`"*.

Đo xem lời khai mới có **khớp đúng** thứ `t53` làm không — không rộng hơn, và cũng **không hẹp
hơn** tới mức mất ý nghĩa. Và kiểm rằng việc hạ lời khai **không** làm ca ấy mất răng: đột biến
"cho `kiem()` gọi mạng trở lại" vẫn phải giết nó.

Nhắc: nợ nền (`chay()` truyền `env=None`, `GITHUB_ACTOR=nguoi-la` ⇒ suite đỏ) có **delta = 0** so
với `cfaccff9` — lượt 2 đã đo. Đó **không** phải finding của packet này.

### 3. `t55a`/`t55b` — tách thật hay tách hình thức?

D6 (dấu ở bất kỳ vị trí) phải giết **chỉ** `t55b`; D7 (thiếu `user.login` ⇒ cho qua) phải giết
**chỉ** `t55a`. Chạy cả hai. Rồi thử một đột biến thứ ba phá **cả hai** tính chất — nó phải giết
cả hai ca.

### 4. Hồi quy

Delta chỉ chạm tệp test, nhưng hãy xác nhận: có ca nào **cũ** bị nới lỏng để nhường chỗ không?
So `ops/lease_publish_test.py` giữa `90015a53` và `9f5b08e8`; mọi dòng **bị xoá hoặc bị sửa**
phải có lý do. (`git diff 90015a53..9f5b08e8 -- ops/lease_publish_test.py`)

### 5. Hình dạng **C** — *phản chứng bắt buộc còn thiếu*

Đây là hình dạng packet vừa mắc, bộ đếm **1**. Với **mỗi** chốt an ninh trong bản vá, hỏi:
**"phép đo nào ĐỎ nếu ai đó gỡ nó?"** Không trả lời được cái nào thì đó là **C lần thứ 2** ⇒
verdict phải nêu thẳng.

## Ngoài phạm vi — ĐỪNG báo

Bảy finding lượt 1 (đã đóng, lượt 2 xác nhận) · `ngoai_pham_vi` và `chua_do_duoc` của r2/r3 ·
khe race hai nhánh `ops/**` (chỉ **thu hẹp**) · nợ nền `GITHUB_ACTOR` (delta = 0) · chưa có lượt
Actions thật · chưa có Windows · ruleset/branch protection ngoài kho.

## Verdict

```
KET_LUAN: <cross_approved | can_sua | dung_lai>
reviewed_sha: 9f5b08e81a131a1c22d15b6d5809885eae11413f
```
Từng finding: **P1/P2/P3** · một câu · **lệnh + đầu ra thật** · đề xuất vá.

Kèm bảng: **P1 + ba P3 của lượt 2** — từng cái **ĐÓNG** (kèm phép đo của bạn) hay **KHÔNG ĐÓNG**.

Cuối: **`da_do_gi`** và **`khong_do_duoc`**. **"Thu hẹp"** khi chỉ thu hẹp; **"đóng"** chỉ khi có
phép đo.

Nếu `cross_approved`, **nói thẳng cái vẫn còn hở** — `approve` không nghĩa là không còn gì.

Nguồn sự thật là **tệp có băm trong kho**; prompt này chỉ là bản chiếu.
