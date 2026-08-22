# Prompt EXECUTOR — `LEASE-DANG-DUNG-MOT-LAN` (#227), lượt **2**

Bạn là **executor** lượt 2. Lease `lease-dang-exec-2-codex-20260821`.
Bạn **đã làm lượt 1** trên nhánh này. Lượt 1 bị review kết luận **`can_sua`**.

## Nguồn sự thật — theo thứ tự

1. **`ops/specs/LEASE-DANG-DUNG-MOT-LAN-r2.md`** — **BẢN SỬA ĐỔI 2**, sha256
   `3f310582de59dce7c109717dbab13ef9467b80c67ffeafc0ac8e1484309e0093`.
   **KIỂM BĂM TRƯỚC KHI ĐỌC.** Lệch ⇒ DỪNG.
   Đây là authority. Nó **thay thế** bản 1 (`…-MOT-LAN.md`, `e1026adb…`) — bản 1 vẫn còn trong
   kho làm hồ sơ, **đừng làm theo nó**.
2. **Verdict lượt 1** — `ops/reviews/lease-dang-review-1-claude-verdict.md`, sha256
   `42b438ad15fc1a8978dcd3bef023aa1f41d0926b8b87dc9c4d521229c9d6ae41`. Bảy finding, mỗi cái có
   lệnh chạy được. **Đọc hết.**
3. `CLAUDE.md` — luật của kho.

Cả ba lấy từ `origin/ops/lease-dang-227` nếu chưa có trên `master`:
```
git fetch origin ops/lease-dang-227
git show origin/ops/lease-dang-227:ops/specs/LEASE-DANG-DUNG-MOT-LAN-r2.md
```
**Thứ định danh tệp là BĂM, không phải tên nhánh.**

## Điều quan trọng nhất — đọc kỹ đoạn này

**Lượt 1 KHÔNG sai vì bạn cẩu thả. Nó sai vì ĐẶC TẢ ghim sai cơ chế.** Mục tiêu 4 của bản 1 bảo
bạn dò `GITHUB_ACTIONS`, mượn tiền lệ lớp `GITHUB_ACTOR`. Tiền lệ ấy **không áp dụng được**:
`GITHUB_ACTOR` là so CHUỖI, còn hai lớp mới là **LỜI GỌI MẠNG**, và **bộ selftest của chính cổng
chạy BÊN TRONG Actions không có `GH_TOKEN`**. Đo được: `GITHUB_ACTIONS=true python3
ops/lease_publish_test.py` ⇒ **46/52, rc=1** ⇒ land nguyên trạng thì **cổng đăng lease tự khoá
vĩnh viễn**.

**Q9 là bản sửa đổi gốc: `kiem()` GIỮ THUẦN, hai lớp GitHub dời sang lệnh con `kiem-github` mà
CHỈ workflow gọi, và BỎ HẲN việc dò `GITHUB_ACTIONS`.** Cả P1-1 lẫn nửa sau của P1-2 chết theo
**kiến trúc**, không theo bản vá. Đừng vá quanh nó.

## Bắt đầu từ đâu

Nhánh `codex/lease-dang-exec-1`, head hiện tại `fefa15b6…`. Bạn **giữ nguyên nhánh**, commit
tiếp lên nó. Ngân sách đo so với **`cfaccff9`**, tức tính **cả** lượt 1.

## Ngân sách — MỚI, vẫn CỨNG

**≤ 3 tệp, ≤ 500 dòng THÊM** so với `cfaccff9` (`git diff --numstat`). Người giữ kho nới
300 → 500 có chủ đích. Lượt 1 đã tiêu **+298**.

**Tính ra sẽ vượt 500 ⇒ DỪNG, xuất handoff.** KHÔNG tự chia packet, KHÔNG tự nới trần (§2).

Gợi ý thật: Q9 cho phép **xoá** kha khá thứ lượt 1 đã thêm (lớp dò env, đường `body` gọi mạng).
Dòng **xoá** không tính vào trần — đừng ngại xoá lại chính mã của mình.

## Cổng bắt buộc

| cổng | tiêu chí |
|---|---|
| `python3 ops/lease_publish_test.py` | `rc=0`, `N/N` **hai số bằng nhau**, **≥ 58 ca** |
| **cùng suite, `GITHUB_ACTIONS=true GITHUB_REPOSITORY=… GITHUB_ACTOR=…`, `gh` VẮNG** | **`N/N` y hệt** — đây là ca `T53`, ca khoá P1-1 |
| `actionlint .github/workflows/*.yml` | `rc=0` cả 5; thiếu công cụ ⇒ in `KHÔNG ĐO ĐƯỢC` và **ĐỎ** |
| đột biến | mỗi chốt mới giết **đúng ca của nó**, `1/1`, trên **BẢN SAO TẠM** |
| kích thước | ≤ 3 tệp, ≤ 500 dòng thêm — **báo cáo SỐ THẬT** |

**Hai đột biến BẮT BUỘC phải chết ở lượt này** (lượt 1 chúng sống hoặc không tồn tại):
- `[os.environ.get("GH_PATH") or "gh", "api", …]` — lượt 1 **SỐNG SÓT 52/52**. Phải giết bằng `T49′`.
- cho `kiem()` gọi mạng trở lại — phải giết bằng `T53`.

**Tách `t46` và `t48`.** Lượt 1 một đột biến giết cả hai; đặc tả đòi tách.

## Điều kiện DỪNG

- Ngân sách sẽ vượt ⇒ DỪNG + handoff.
- Chốt phải nằm **ngoài** `write_set` ⇒ DỪNG + handoff.
- Thấy một tiêu chí trong `nghiem_thu` **sai** ⇒ DỪNG và báo cáo. Đặc tả đã đóng băng lần hai;
  **lần này thì đúng là được phép nghi ngờ nó** — bản 1 đã sai một mục. Nhưng nghi ngờ thì
  **BÁO CÁO**, đừng tự sửa giữa đường.
- Gặp hình dạng **A** (*lời khai rộng hơn phép đo*) lần thứ **7**, hoặc hình dạng **B** (*mượn
  tiền lệ mà không đo xem nó có áp dụng được không*) lần thứ **3** ⇒ **DỪNG, không vá**.
  Bạn đã mắc **A** một lần ở lượt 1 (Q5 khai rộng hơn `T52` đo). Nói thẳng: **kiểm lại từng lời
  khai của mình bằng một phép đo có thể ĐỎ**, đừng bằng một phép khớp chuỗi.

## Báo cáo cuối

1. `git diff --numstat cfaccff9..HEAD` — số thật.
2. `N/N` của suite, **hai lần chạy**: môi trường thường **và** môi trường Actions không `gh`.
3. Bảng đột biến: ca ↔ đột biến ↔ `giết 1/1`. Nêu riêng hai đột biến bắt buộc ở trên.
4. **Bảy finding của verdict lượt 1** — từng cái: **đã đóng** (kèm phép đo) hay **không đóng**
   (kèm lý do). Không được bỏ sót cái nào.
5. `chua_do_duoc` của riêng bạn. **"Thu hẹp"** khi nó chỉ thu hẹp; **"đóng"** chỉ khi có phép đo.

Nguồn sự thật là **tệp có băm trong kho**; prompt này chỉ là bản chiếu.
