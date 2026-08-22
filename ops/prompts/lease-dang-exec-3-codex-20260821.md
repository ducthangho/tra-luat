# Prompt EXECUTOR — `LEASE-DANG-DUNG-MOT-LAN` (#227), lượt **3** (cuối)

Bạn là **executor** lượt 3. Lease `lease-dang-exec-3-codex-20260821`.
Bạn đã làm lượt 1 và lượt 2 trên chính nhánh này.

**Lượt 2 gần như xong: BẢY TRÊN BẢY finding của lượt 1 đã đóng THẬT**, reviewer dựng lại đúng
phản chứng cũ trên head mới cho từng cái. Lượt này **chỉ vá phần còn lại**.

## Nguồn sự thật — theo thứ tự

1. **`ops/specs/LEASE-DANG-DUNG-MOT-LAN-r3.md`** — **bản sửa đổi 3, CHỈ GHI DELTA**, sha256
   `c65d5dbd9d2b398978226f6863cf7cd4e4ddb219a7086be0005e65804a0f47da`.
2. **`ops/specs/LEASE-DANG-DUNG-MOT-LAN-r2.md`** — vẫn nguyên hiệu lực cho mọi thứ r3 **không**
   nêu, sha256 `3f310582de59dce7c109717dbab13ef9467b80c67ffeafc0ac8e1484309e0093`.
3. **Verdict lượt 2** — `ops/reviews/lease-dang-review-2-claude-verdict.md`, sha256
   `f21069548bf0e0ff507822a246283fe47417bc334fa1e231b2e71dc88d52b4c0`. Nó có **lệnh chạy được**
   cho từng finding và **mô tả sẵn cách vá P1**. Đọc kỹ mục P1 và mục `da_do_gi`.
4. `CLAUDE.md`.

Lấy từ `origin/ops/lease-dang-227`. **KIỂM BĂM TRƯỚC KHI ĐỌC**; lệch ⇒ DỪNG.
**Thứ định danh tệp là BĂM, không phải tên nhánh.**

## Việc — đúng bốn thứ, không hơn

### 1. P1 — nối `kiem-github` vào phép đo (BẮT BUỘC)

Sau Q9, `kiem-github` là **thứ duy nhất** chạy hai lớp GitHub, và nó có **đúng một điểm gọi
trong toàn kho**: một dòng trong YAML. Không ca nào đo điểm gọi ấy. Đo hai chiều:

```
xoá khối gọi `kiem-github` khỏi YAML  ->  58/58, actionlint rc=0    <- KHÔNG ai bắt
xoá khối gọi `check`       khỏi YAML  ->  57/58, `t51` ĐỎ           <- có `t51` bắt
```

Bất đối xứng này là lỗ **do chính lượt 2 mở**. Vá theo `T59`/`T60` của r3 — reviewer đã viết sẵn
cách: trong `_chay_buoc_dang`, cho `lease_publish.py` giả **ghi nhật ký `argv`** thay vì
`raise SystemExit(0)` câm; rồi đòi (a) mỗi lease có một dòng `kiem-github <tệp>` **trước**
`check <tệp>`; (b) thêm tham số `kiem_github_hong=` để đột biến "kiem-github trả rc≠0" làm lease
**không** được POST và bước rc≠0.

**Hai đột biến này PHẢI CHẾT** (lượt 2 cả hai **sống sót `58/58`**):
- **D10** — xoá hẳn khối gọi `kiem-github` khỏi YAML.
- **D11** — vẫn gọi nhưng **nuốt mã thoát** (bỏ cả hai nhánh `if`).

### 2. `T53` — làm đúng chữ, hoặc hạ lời khai (Q18)

`T53` khai *"toàn suite"* nhưng `t53` chạy **một** lệnh `check`, với `GITHUB_ACTOR="ducthangho"`
— đúng giá trị duy nhất **không** kích hoạt được lớp actor. Đo: `GITHUB_ACTOR=nguoi-la` ⇒
**36/58**.

**Đây KHÔNG phải hồi quy của bạn** — reviewer đo nền `cfaccff9` ra **26/42**, delta = 0. Cơ chế
có sẵn (`chay()` truyền `env=None`). Cái sai là **lời khai mới**.

Hai đường, chọn một, **khai rõ chọn đường nào và vì sao**:
- (a) thêm một ca chạy **toàn suite** trong tiến trình con với `GITHUB_ACTOR` **ngoài**
  allowlist — khi ấy `chay()` phải dựng env sạch, kẻo chính ca ấy đỏ;
- (b) sửa mô tả `t53` cho khớp đúng thứ nó đo.

### 3. `t55` tách đôi (Q19)

`t55a` = thiếu `user.login` ⇒ CHẶN · `t55b` = dấu không ở đầu thân ⇒ không tính.
**D6** (dấu chỉ cần `in body`) phải giết **chỉ** `t55b`; **D7** (thiếu `user.login` ⇒ cho qua)
phải giết **chỉ** `t55a`.

### 4. KHAI đột biến giết nhiều ca

`nghiem_thu` r2 đã đòi, đòi ấy chưa được thực hiện. Ít nhất hai cái đã biết:
`bo lop do loai so hieu` → `t43`+`t44` · `cho kiem() goi mang tro lai` → 8 ca.

## KHÔNG làm

- **Đừng sửa `ops/specs/**`** — không nằm trong `write_set`, và đặc tả có băm thì không sửa đè.
  Mục `chua_do_duoc` của r2 khai hẹp hơn thực tế; việc đính chính thuộc **biên nhận**, phiên
  điều phối làm.
- Đừng đụng bảy finding lượt 1 — chúng đã đóng, có phản chứng. Đừng "cải thiện" chúng.
- Đừng đóng khe race hai nhánh `ops/**`.

## Ngân sách — nới, vẫn CỨNG

**≤ 3 tệp, ≤ 550 dòng THÊM** so với `cfaccff9`. Head hiện tại **`+498`**, tức bạn còn **~52
dòng**. Người giữ kho nới 500 → 550 có chủ đích, vì trần cũ đã cạn sạch.

**Tính ra sẽ vượt 550 ⇒ DỪNG, xuất handoff.** Dòng **xoá** không tính vào trần.

## Cổng bắt buộc

| cổng | tiêu chí |
|---|---|
| `python3 ops/lease_publish_test.py` | `rc=0`, `N/N` hai số bằng nhau, **≥ 61 ca** |
| cùng suite, `GITHUB_ACTIONS`+`GITHUB_REPOSITORY`+`GITHUB_ACTOR` đặt, `gh` **vắng** | `N/N` y hệt |
| `actionlint .github/workflows/*.yml` | `rc=0` cả 5; thiếu công cụ ⇒ `KHÔNG ĐO ĐƯỢC` và **ĐỎ** |
| **D10** xoá khối gọi `kiem-github` khỏi YAML | **PHẢI ĐỎ** — lượt 2 sống sót `58/58` |
| **D11** gọi `kiem-github` nhưng nuốt rc | **PHẢI ĐỎ** — lượt 2 sống sót `58/58` |
| **D6/D7** | giết **hai ca khác nhau** (`t55b`/`t55a`) |
| kích thước | ≤ 3 tệp, ≤ 550 dòng thêm — **số THẬT** |

## Điều kiện DỪNG

- Ngân sách sẽ vượt ⇒ DỪNG + handoff. KHÔNG tự nới trần (§2).
- Chốt phải nằm **ngoài** `write_set` ⇒ DỪNG + handoff.
- Hình dạng **A** (*lời khai rộng hơn phép đo*) lần thứ **7**, **B** (*mượn tiền lệ mà không đo*)
  lần thứ **3**, hoặc **C** (*phản chứng bắt buộc còn thiếu*) lần thứ **2** ⇒ **DỪNG, không vá**.
  Hình dạng **C** là hình dạng bạn vừa mắc ở lượt 2. Trước khi báo xong: với **mỗi** chốt an
  ninh trong bản vá, hỏi **"phép đo nào ĐỎ nếu ai đó gỡ nó?"** — và nếu không trả lời được thì
  đó chính là C lần thứ hai.

## Báo cáo cuối

1. `git diff --numstat cfaccff9..HEAD` — số thật.
2. `N/N`, **hai lần chạy** (thường · môi trường Actions không `gh`).
3. Bảng đột biến, **nêu riêng D10, D11, D6, D7**. Kèm **danh sách đột biến giết NHIỀU ca**.
4. `T53`: chọn đường (a) hay (b), và **vì sao**.
5. `chua_do_duoc` của riêng bạn. **"Thu hẹp"** khi chỉ thu hẹp; **"đóng"** chỉ khi có phép đo.

Nguồn sự thật là **tệp có băm trong kho**; prompt này chỉ là bản chiếu.
