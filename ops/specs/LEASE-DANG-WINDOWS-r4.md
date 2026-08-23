# ĐẶC TẢ ĐÓNG BĂNG — `LEASE-DANG-WINDOWS`, **bản sửa đổi 4** (delta)

> **CHỈ ghi phần thay đổi** so với r3 (`130b6d29919db327ccc2d9ad8d53910e5dd74b2eef0f607d3e59a707647de40d`).
> r1 · r2 · r3 **KHÔNG bị sửa, KHÔNG bị xoá**.

`packet_id`: `LEASE-DANG-WINDOWS` · `packet_issue`: `#238`

## Bản này CỐ Ý KHÔNG ĐẶC TẢ GÌ MỚI

Ba lượt liên tiếp hỏng ở **đặc tả**, không ở bản vá. Mỗi lần phiên điều phối mô tả *thứ cần đúng*
thì lại sinh thêm một biểu hiện hình dạng **E**. Nên r4 **không mô tả một phép dẫn xuất nào**: nó
**chép lại một bản vá ĐÃ CHẠY** và đăng ký phản chứng của chính bản vá ấy.

## Vì sao có bản này

Cross-review lượt 2 (`e5dd9584d2e01172f71a0308c1d90eb0918d5b971af56cbb664d91438cf3c4a7`, đo trên
`b0c8fb368d70f17bce5eb7e3d1fe02d810db8e19`) kết `can_sua`. **`P1-1` và `P1-2` của lượt 1 ĐÃ ĐÓNG**
— reviewer kiểm lại năm phép đo của phiên điều phối, 5/5 khớp. Còn một lỗ MỚI:

**`P1-3` — cổng NỀN không có phản chứng nào.** Một đột biến MỘT MỆNH ĐỀ (`X1`), bỏ
`(nen or os.name) == "nt"` khỏi `_ly_do_bo_qua_workflow`:

```
b0c8fb3 + X1  (chưa vá)      lease_publish: 64/64 đạt; đã chạy=64, bỏ qua=8 ; rc=0   XANH
```

Tám ca `_chay_buoc_dang` biến mất **IM LẶNG trên chân Ubuntu — chân LUÔN chạy**. Cả ba ca mới của
lượt 3 (`t70` `t71` `t72`) đều ép `nen="nt"`, nên **không ca nào đo nhánh `posix`** — đúng nhánh
quyết định *"có được bỏ qua hay không"*. `Q9` khoá phần LIỆT KÊ ĐƯỢC (chuỗi lý do) chứ không khoá
phần THẬT SỰ CHẶN (nền) ⇒ **hình dạng E lần 4**.

Reviewer **không dừng ở mô tả**: đã viết và CHẠY ca vá, rồi giao lại số. Người giữ kho quyết
in-session 22-08-2026: **nới trần, đóng `P1-3` bằng đúng ca ấy**.

## Quyết định MỚI

| # | quyết định | căn cứ |
|---|---|---|
| **Q12** | Ngân sách nới **120 → 125 dòng thêm**. | Bản vá đo được **8** dòng thêm (xem Q14) ⇒ `116 + 8 = 124`, lọt với đúng **1** dòng dư. Trần vẫn chật có chủ đích. |
| **Q13** | **Executor CHÉP ca vá dưới đây, KHÔNG tự nghĩ lại.** Đây là mã đã chạy trong cây review của lượt 2, không phải đề xuất trên giấy. | Điều kiện dừng `E lần 4` **đã kêu**. Người giữ kho cho đi tiếp với lý do nêu rõ: lượt này **không đặc tả phép dẫn xuất nào mới**, nên nó không tái tạo hình dạng E. Cho executor tự nghĩ lại chính là mở đường cho lần thứ năm. |
| **Q14** | **Đơn vị đếm là `git diff --numstat`, và con số là 8 — KHÔNG phải 5.** | Verdict khai *"5 dòng"* = dòng **mã logic**. Phiên điều phối đo bằng `git diff --numstat`: **8** (kể 2 dòng trống ngăn cách và 1 dòng `f"..."` bị ngắt). Ghi thẳng để người sau không lấy số 5 làm chuẩn rồi tưởng vượt trần. |
| **Q15** | Phạm vi lượt này **CHỈ `P1-3`**. `P2-5` và bảy mục P2/P3 của lượt 1 **để ngoài**. | Trần 125 chỉ đủ cho `P1-3`. `P2-5` (≈3 dòng) là fail-close nên không mất an toàn, chỉ sai chẩn đoán — nó vào packet kế tiếp cùng `P2-3` mà nó làm nặng thêm. |

## Ca vá — CHÉP NGUYÊN VĂN

Chèn ngay **trước** `def main() -> int:` trong `ops/lease_publish_test.py`:

```python
@ca
def t73_nen_posix_khong_duoc_bo_qua_ca_nao():
    def bo(): raise BoQuaNen(WORKFLOW_DANG, "dang")
    rc, out = _chay_main_meta(bo, "posix")
    bang(rc == 1 and "ĐỎ" in out and "bỏ qua=0" in out,
         f"nền posix mà vẫn bỏ qua được: rc={rc}, {out!r}")
```

Nó đi qua `main()`, **không gọi thẳng** `_ly_do_bo_qua_workflow` ⇒ tuân `Q8`.

## `nghiem_thu` — thêm `W10`

Giữ `W1` `W2` `W4` `W5` (r1) · `W3′` (r2) · `W6′` `W7′` `W8` `W9` (r3). **`W3′` phải chạy LẠI trên
head mới** — bằng chứng của `b0c8fb3` (run `32563904221`) KHÔNG chuyển sang head khác.

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| **W10** | Nhánh `posix` của cổng nền có ca canh. | Ba số phải khớp CHÍNH XÁC, đã đo sẵn trong cây review lượt 2: bản vá nguyên vẹn ⇒ `73/73 đạt; đã chạy=73, bỏ qua=0`, `rc=0` · bản vá **+** `X1` ⇒ `64/65 đạt; đã chạy=65, bỏ qua=8`, `rc=1`, ĐỎ `t73_nen_posix_khong_duoc_bo_qua_ca_nao` · **và đối chứng** `X1` **không** kèm bản vá ⇒ `64/64`, `rc=0` (XANH — đây là lỗ, phải tái hiện được thì mới biết ca vá đo đúng thứ ấy). |

Lệch bất kỳ số nào trong ba số ⇒ **DỪNG**, báo số đo được. Không sửa ca cho vừa số.

## `hinh_dang_ke_thua`

**E = 4** (verdict lượt 2 tuyên, với `P1-3` là biểu hiện thứ tư). Bộ đếm khác giữ nguyên:
**A** = 7 · **B** = 2 · **C** = 1 · **D** = 3 · **F** = 2.

Ghi cho hồ sơ, vì đây là lần **thứ tư** liên tiếp lỗi nằm ở đặc tả chứ không ở bản vá: `r3/Q9` tự
khai *"Ca không còn khai được lý do thì không còn cửa sau nào"*. Câu ấy **rộng hơn phép đo** — nó
đúng về **chuỗi lý do** và sai về **nền**. Đó là hình dạng **A** trong một câu của hình dạng **E**.
Phiên điều phối **không tự tăng A**; nêu ra để người giữ kho quyết.

## `chua_do_duoc`

Giữ r3. Thêm:
- Hành vi của `P1-3` trên chân `windows-latest` THẬT — reviewer chỉ **suy** được (`64/64 bỏ qua=8`
  y hệt bản đúng ⇒ không chân CI nào đỏ), chưa chạy Windows thật. `W3′` của lượt này sẽ đo.
- `shellcheck` có/vắng trên runner `windows-latest`: **KHÔNG ĐO ĐƯỢC** từ log. Thứ đo được là dù
  thế nào `t33` cũng không cho biết — và đó là nợ của packet kế tiếp, không phải của lượt này.
