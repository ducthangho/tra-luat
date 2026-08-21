# Prompt BẤT BIẾN — Executor `DONREF-XOA-AN-TOAN` (#217), lượt 1, provider `codex`

Bạn là executor. Reviewer là `claude` (cross-provider, §8 thoả).

## 0. ĐẶC TẢ LÀ THẨM QUYỀN, KHÔNG PHẢI PROMPT NÀY

Nguồn có thẩm quyền là **`ops/specs/DONREF-XOA-AN-TOAN.md`**, băm

```
1add3edf165faa2b53d6b52212ea34d7a73934367fd73bbca91e5518a9a664de
```

**Việc đầu tiên: tìm tệp ấy và ĐỐI CHIẾU BĂM.** Thứ định danh nó là **BĂM**, không phải tên
nhánh — tên nhánh là thứ trôi và bị xoá. Tìm ở `master` trước; **chưa thấy thì** fetch nhánh
`ops/spec-donref-xoa-an-toan`. Băm lệch ⇒ **DỪNG**, báo cáo, không đoán.

Prompt này chỉ nói **cách làm trên nền**; mọi ràng buộc nội dung nằm trong đặc tả. Chỗ nào prompt
lệch đặc tả thì **PROMPT SAI**.

## 1. Mỏ neo

| trường | giá trị |
|---|---|
| packet | `#217` |
| base | `master` — ĐO LẠI bằng `git -C kho rev-parse origin/master` |
| write set | **`ops/nhanh_don_duoc.py`** · **`ops/nhanh_don_duoc_test.py`** — hai tệp, cả hai đều MỚI |
| lớp review | `cross_approved` |

**Không** sửa tệp nào khác. Không `CLAUDE.md`. Không `.github/workflows/ops-don-ref.yml` —
đặc tả §Q3 nói rõ `master` đã đúng và đụng vào là mở lại đúng bề mặt vừa quyết bỏ.

## 2. Việc

Đặc tả §`muc_tieu` có năm mục và §`nghiem_thu` có bảy tiêu chí, mỗi tiêu chí kèm **đột biến nào
làm nó ĐỎ**. Đọc thẳng ở đó. Tóm tắt để định hướng, **không thay thế**:

Một công cụ **CHỈ ĐỌC** phân loại nhánh remote thành **A** (mọi commit đã trong nhánh mặc định) ·
**B** (chỉ còn đúng một commit đã bị thay) · **C** (còn commit riêng, **hoặc KHÔNG ĐO ĐƯỢC**), rồi
in một lệnh `git push origin --delete` chứa **đúng** A và B.

Ba chỗ đặc tả nhấn, và chúng là chỗ dễ trượt nhất:

- **Ba trạng thái, không phải hai.** Mọi thứ không đo được rơi vào **C kèm lý do in ra**, không
  bao giờ rơi vào A hay B. `git` lỗi, ref biến mất giữa chừng, kho nông — tất cả là **C**.
- **Lệnh in ra không bao giờ chứa nhánh mặc định**, kể cả khi nó trivially là tổ tiên của chính nó.
- **Đầu ra phải KHAI GIỚI HẠN**: phân loại chỉ đúng tại thời điểm đo, vì nhánh mặc định có thể bị
  ép lùi sau đó, và lệnh in ra **không** có phép kiểm nào lúc chạy. Đây là P1 lượt 2 của `#213`,
  **cố ý để mở** — bạn **khai** nó, **không** vá nó. Vá nó là quay lại hướng đã bị bỏ.

## 3. Bằng chứng bắt buộc

1. `python3 ops/nhanh_don_duoc_test.py` ⇒ `rc=0`, `N/N` **hai số bằng nhau**, phủ đủ bảy tiêu chí.
2. Phản chứng dựng **KHO BARE THẬT** (`git init --bare` + push), **không** đồ giả diễn kịch bản.
   Kho này đã trả giá đúng chỗ đó: một `gh` giả diễn kịch bản từng cho `40/40` trong khi đột biến
   **xoá hẳn** lệnh phá vẫn qua. Đồ giả phải **mô phỏng TRẠNG THÁI**.
3. **Mỗi đột biến giết ĐÚNG ca của nó.** Một đột biến giết nhiều ca là dấu hiệu ca chưa tách đủ —
   **nói ra**, đừng làm tròn thành đạt.
4. Mọi đột biến chạy trên **BẢN SAO TẠM** (`git archive … | tar -x`), không sửa cây rồi khôi phục:
   `finally` không chạy khi bị giết.
5. Chạy công cụ **trên chính kho này** và in kết quả. Đối chiếu với số đã đo 2026-08-21:
   **A = 13 · B = 4 · C = 70** tại `master = 03339486`. Số khác đi **không** đương nhiên là sai —
   master đã tiến — nhưng **lệch mà không giải thích được** thì là finding.
6. Cây sạch cuối lượt; commit, **KHÔNG push** (phiên điều phối đẩy).

## 4. Điều kiện DỪNG

- Cần sửa tệp **ngoài** hai tệp write set ⇒ **DỪNG**, báo cáo. Đặc tả hứa thứ write set không kham
  được là **lỗi của đặc tả**, và sửa nó là việc của người giữ kho, không phải của bạn.
- Thấy một tiêu chí ở §`nghiem_thu` là **sai** hoặc **không thể đỏ** ⇒ DỪNG, mở revision, đừng tự
  đổi tiêu chí giữa đường.
- **Gặp hình dạng lỗi "lời khai rộng hơn phép đo" lần thứ SÁU ⇒ DỪNG, không vá.** Đặc tả
  §`hinh_dang_ke_thua` đếm được **năm lần** đã xảy ra, cùng một executor. Bạn được chọn một phần
  vì lý do ấy: nếu bạn cũng mắc, giả thuyết *"hình dạng bám người viết"* **sai**, và vấn đề nằm ở
  đặc tả. Trường hợp ấy **có giá trị hơn** một bản vá — báo cáo, đừng che.

## 5. Báo cáo cuối

In ra: băm đặc tả đã đối chiếu · hai việc đã làm gì · **số đo thật với `rc` đọc trực tiếp** · bảng
đột biến (tên · ca bị giết · `N/N`) · kết quả chạy công cụ trên kho này · **phần còn hở đã khai
tên** · SHA commit · trạng thái cây. Nói thẳng thứ nào **không** đo được — im lặng sẽ bị đọc thành
đã kiểm.
