# Prompt BẤT BIẾN — Reviewer chéo `DONREF-XOA-AN-TOAN` (#217), lượt 1, provider `claude`

Executor là `codex`, reviewer là `claude` ⇒ cross-provider, §8 thoả.

Read-only với KHO: **không commit, không push, không đổi HEAD.** Đột biến chạy trên **BẢN SAO
TẠM** (`git -C kho archive <sha> | tar -x`). Đã có tiền lệ trả giá: một lượt review dùng
`git --work-tree=… checkout -- .` và ghi vào INDEX của worktree.

```
./nhiem_vu.txt      prompt này
./DAC_TA.md         đặc tả ĐÓNG BĂNG — băm 1add3edf165faa2b53d6b52212ea34d7a73934367fd73bbca91e5518a9a664de
./diff.patch        master..fa4b0dd — 2 tệp, +380
./kho/              bản sao kho tại exact head, GHI ĐƯỢC
```

## 0. ĐẶC TẢ LÀ THẨM QUYỀN, KHÔNG PHẢI PROMPT NÀY

**Việc đầu tiên: đối chiếu băm `DAC_TA.md`.** Lệch ⇒ DỪNG. Mọi tiêu chí nghiệm thu nằm ở
`§nghiem_thu` của đặc tả — bảy cái, mỗi cái kèm **đột biến nào làm nó ĐỎ**. Chỗ nào prompt này
lệch đặc tả thì **PROMPT SAI**.

## 1. Mỏ neo

| trường | giá trị |
|---|---|
| packet | `#217` |
| exact head | `fa4b0dd879f0cf7ae589989863670d2a8200839c` — ĐO LẠI bằng `git -C kho rev-parse HEAD` |
| base | `master` |
| write set | `ops/nhanh_don_duoc.py` · `ops/nhanh_don_duoc_test.py` — hai tệp, cả hai MỚI |

## 2. Công cụ này làm gì, và vì sao nó CHỈ ĐỌC

Packet thay cho PR `#213` đã **đóng băng** sau hai lượt cross-review, hai P1. Quyết định gốc của
đặc tả: **KHÔNG tự động hoá việc xoá ref** — vì cả hai P1 đều sinh ra từ chỗ workflow **giữ quyền
phá**. Công cụ này phân loại nhánh thành **A** (mọi commit đã trong nhánh mặc định) · **B** (chỉ
còn đúng một commit đã bị thay) · **C** (còn commit riêng, **hoặc KHÔNG ĐO ĐƯỢC**), rồi **in** một
lệnh `git push origin --delete` cho người đọc tự chạy.

**Rủi ro nằm ở ĐẦU RA, không ở quyền ghi.** Công cụ không viết gì, nhưng một phân loại sai làm
mất commit y hệt tự tay xoá nhầm. Đó là lý do đặc tả đặt `review_class: cross_approved` dù packet
không chạm đường authority nào.

## 3. Trục phải soi — theo rủi ro GIẢM DẦN

### 3.1 Có đường nào một nhánh CÒN COMMIT RIÊNG lọt vào A hoặc B không?

Câu hỏi duy nhất thật sự quan trọng. Mọi thứ khác là phụ. Hướng, **đừng dừng ở đây**:

- Nhánh **rỗng**, nhánh **trùng hệt** nhánh mặc định, nhánh **đi trước**, lịch sử **rời** (không
  tổ tiên chung), ref trỏ **tag object** thay vì commit, tên nhánh có ký tự lạ.
- **Nhóm B là chỗ nguy hiểm nhất**: nó tha một commit. Điều kiện nhận B chặt tới đâu? Một commit
  **cùng tiêu đề** nhưng **khác nội dung** thì sao? Hai commit? Commit rỗng? Tiêu đề bị người
  khác đặt trùng?
- **Ba trạng thái, không phải hai.** `git` lỗi, ref biến mất giữa chừng, mạng đứt, **kho nông** —
  tất cả phải rơi vào **C kèm lý do**. Có đường nào một lỗi bị đọc thành "không có commit riêng"?

### 3.2 Lệnh in ra có đúng bằng A + B không

- Có nhánh **mặc định** lọt vào lệnh không, kể cả khi nó trivially là tổ tiên của chính nó?
- Có nhánh **C** nào lọt không?
- Tên nhánh có ký tự đặc biệt: lệnh in ra còn **an toàn để dán** không, hay có đường tiêm lệnh?
- Phạm vi khai là `ops/**` — nhánh **ngoài** phạm vi có lọt vào lệnh không?

### 3.3 Bộ phản chứng có RĂNG hay chỉ CÓ MẶT

Bảy ca, bảy đột biến, executor khai mỗi con giết **đúng ca của nó**. **XÁC NHẬN, đừng tin** — rồi
tự nghĩ đột biến mới, nhất là cho 3.1.

- Đồ giả có **mô phỏng TRẠNG THÁI** không, hay **diễn KỊCH BẢN**? Executor khai dựng **kho bare
  thật**; kiểm lời khai ấy.
- Có ca nào **CÓ MẶT mà KHÔNG ĐO** — `return` sớm, nhánh "không thấy thì bỏ qua" không chốt?
- Một đột biến giết **nhiều** ca là dấu hiệu ca chưa tách đủ. Executor khai không con nào như vậy.

### 3.4 Lời khai có đúng bằng phép đo không

Đây là hình dạng lỗi kho đã đếm **NĂM lần** (đặc tả `§hinh_dang_ke_thua`). Đọc **từng câu** khai
trong mã và đầu ra, rồi **đo lại từng câu**:

- Dòng `GIOI HAN` có nói đúng thứ công cụ thật sự không bảo đảm không?
- Docstring/chú thích có hứa rộng hơn thứ mã làm không?
- Nhãn nhóm C (`kho nong`, …) có đúng nguyên nhân không, hay gộp nhiều nguyên nhân vào một chữ?

### 3.5 Phép đo trên kho thật

Executor chạy trên kho đầy đủ: `A=15 · B=3 · C=72` @ `master a7a45119`. Trên kho **nông** thì
**mọi nhánh vào C**, lệnh rỗng, `rc=1` — phiên điều phối đã đo lại và xác nhận. **Kiểm cả hai.**
`rc=1` khi không có gì để xoá: đó là lựa chọn đúng hay là một mã thoát gây hiểu nhầm?

## 4. NGOÀI phạm vi — nêu lại là sai phạm vi

- **P1 lượt 2 của `#213`** (nhánh mặc định bị ép lùi sau phép đo): đặc tả `§ngoai_pham_vi` ghi
  **CỐ Ý ĐỂ MỞ**. Công cụ **khai** nó, không vá. Nêu như finding CHẶN là sai phạm vi.
- Sửa `.github/workflows/ops-don-ref.yml`, `CLAUDE.md`; dọn nhánh; rà nội dung 72 nhánh C; bảy
  trục cũ của `#213` — tất cả ngoài phạm vi theo đặc tả.

## 5. Điều kiện DỪNG

- Cần sửa mã để chứng minh ⇒ **bản sao tạm**, KHÔNG sửa cây kho.
- Thấy một tiêu chí ở `§nghiem_thu` **sai** hoặc **không thể đỏ** ⇒ DỪNG và nói ra.
- Thứ đòi sửa ngoài hai tệp write set ⇒ finding + đề xuất, không tự mở rộng.

## 6. Định dạng trả về

**IN RA STDOUT** — có lượt đã mất trắng verdict vì ghi vào tệp trong sandbox rồi sandbox bị xoá.

Kết thúc bằng **đúng hai dòng cuối**, không có gì sau chúng:

```
VERDICT: <approve|changes_requested|do_not_land>
Reviewed commit: <sha 40 ký tự đã ĐO>
```

Trước đó: finding (mức P1/P2/P3, **bằng chứng đo được**, invariant bị cắt, gợi ý vá) · **"đã đo và
sạch"** · **"chưa đo được — GIẢ THUYẾT"**.

**`approve` nghĩa là:** bạn đã TÌM và KHÔNG THẤY đường nào làm một nhánh còn commit riêng lọt vào
lệnh xoá. Không phải "đọc thấy hợp lý". Đầu ra của công cụ này là một lệnh phá mà người ta sẽ dán
vào terminal.
