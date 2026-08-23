# Prompt REVIEWER — `LEASE-DANG-WINDOWS` (#238), lượt **3**. Neo exact head `7f91ea1`.

Bạn review chéo lượt 4 của packet `#238`, kho `ducthangho/tra-luat`.
**Chỉ đọc; không sửa kho.** Bản sao ghi được là của bạn.

## ĐỌC ĐIỀU NÀY TRƯỚC MỌI THỨ KHÁC — bạn đang review MÃ DO CHÍNH NHÀ CUNG CẤP CỦA BẠN VIẾT

Bản vá của lượt 4 **không do executor nghĩ ra**. Nó do **reviewer lượt 2 (`claude`)** viết và chạy
trong cây review của họ; `r4/Q13` bắt executor (`codex`) **chép nguyên văn, cấm sửa**.

Nghĩa là: phần **cross-provider** của lượt này rất mỏng — `codex` chỉ làm động tác chép. Nội dung
bản vá là **của `claude`**, tức của nhà cung cấp mà bạn thuộc về.

**Đừng nể nó.** Đừng đọc "reviewer trước đã đo rồi" thành "đã đúng rồi". Hãy đối xử với ca `t73`
đúng như với mã của một executor: tìm cách làm nó **xanh mà không đo gì**, tìm cách nó **đỏ sai
lý do**, tìm ca nó **bỏ sót**. Nếu kết luận của bạn là "ĐẠT", hãy nói rõ bạn đã tấn công nó bằng
những gì.

## Nguồn sự thật — KIỂM BĂM, lệch ⇒ DỪNG

| gì | ở đâu | sha256 |
|---|---|---|
| đặc tả **r4** | `ops/specs/LEASE-DANG-WINDOWS-r4.md` | `11972e8ce5d543304b35b7239128af5130d11feaef378465461c3b2b649cc613` |
| verdict lượt 2 | `ops/reviews/lease-dang-windows-review-2-claude-verdict.md` | `e5dd9584d2e01172f71a0308c1d90eb0918d5b971af56cbb664d91438cf3c4a7` |
| r3 · r2 · r1 | `-r3.md` · `-r2.md` · `.md` | `130b6d29…` · `d9da7705…` · `f555cbe1…` |

Hồ sơ ở nhánh `ops/pkg-windows` (tìm ở `master` trước, chưa thấy thì
`git fetch origin ops/pkg-windows`). **Thứ định danh tệp là BĂM, không phải tên nhánh.**
Handoff lượt 4 nằm **TRONG** reviewed commit `7f91ea1` (khác lượt 3 — xem mục "sai khác nếp").

Mã: `codex/lease-dang-windows-1` @ **`7f91ea1cffe17af391362a91b83907c32b16f3b2`**.
Nền đo ngân sách: `ba82b06f9df81fc2f13786fec590ec2110d046b7`.

## Toàn bộ diff của lượt 4

```python
+@ca
+def t73_nen_posix_khong_duoc_bo_qua_ca_nao():
+    def bo(): raise BoQuaNen(WORKFLOW_DANG, "dang")
+    rc, out = _chay_main_meta(bo, "posix")
+    bang(rc == 1 and "ĐỎ" in out and "bỏ qua=0" in out,
+         f"nền posix mà vẫn bỏ qua được: rc={rc}, {out!r}")
```

Tám dòng thêm (`git diff --numstat`), chèn trước `def main()`. Không gì khác.

## Đã đo, KIỂM LẠI TÔI — tôi có thể sai

```
ban va khop TUNG BYTE voi ban reviewer luot 2 da chay: sha256 ca tep = c378e6b0f934aa02...
ngan sach write-set ba82b06f..7f91ea1  = +124/-20, 2 tep      (tran 125, du 1)
ops/lease_publish.py                    = KHONG doi mot byte  (vang khoi diff)
ban va nguyen ven                       73/73 dat; da chay=73, bo qua=0 ; rc=0
ban va + X1                             64/65 dat; da chay=65, bo qua=8 ; rc=1 ; DO t73
X1 KHONG kem ban va (doi chung)         64/64 dat; da chay=64, bo qua=8 ; rc=0  XANH
```

`X1` = bỏ mệnh đề `(nen or os.name) == "nt"` khỏi `_ly_do_bo_qua_workflow`.

**`W3′` ĐÃ ĐẠT trên head này** — run `32567293842` @ `7f91ea1c`, attempt 1, 2 job, không job nào
đỏ: ubuntu `73/73 bỏ qua=0` · windows `65/65 bỏ qua=8`. **65+8=73**, và con số Windows đi
**64 → 65** ⇒ `t73` **chạy thật trên chân `windows-latest`** và xanh. Đừng dựng lại lượt Windows.

Mọi đột biến của bạn phải qua `ast.parse` **trước** khi tin con số — phiên điều phối đã một lần
đọc nhầm `SyntaxError` (`rc=1`) thành "đỏ đúng".

## Hướng tấn công — mỗi hướng đòi MỘT PHÉP CHẠY

1. **`t73` có thể xanh mà không đo gì không?** Nó khẳng định ba thứ: `rc == 1` · `"ĐỎ" in out` ·
   `"bỏ qua=0" in out`. Có tổ hợp nào thoả cả ba mà **không** phải vì nhánh `posix` bị chặn?
2. **`t73` có đỏ SAI lý do không?** Làm `_chay_main_meta` hỏng theo cách khác (nền không truyền
   được, `WORKFLOW_DANG` sai đường dẫn, `main()` ném) — `t73` đỏ với thông điệp nào?
3. **Chuỗi `"ĐỎ"` khớp ở đâu?** Nó là một token trong đầu ra tổng hợp. Có ca nào khác in `ĐỎ` làm
   `t73` xanh giả không? Đây đúng họ với `t64 đếm chuỗi` mà kho đã trả giá.
4. **`X1` có phải đột biến DUY NHẤT khoá được không?** Đột biến khác cùng lớp: đảo chiều so nền
   (`!= "nt"`), thay `os.name` bằng hằng, bỏ tham số `nen`, cho `_chay_main_meta` bỏ qua tham số
   nền. Cái nào `t73` bắt, cái nào không?
5. **Lượt 4 có làm nặng thêm mục nào ngoài phạm vi không?** `P2-5` (`except Exception: ly_do=""`)
   và bảy mục P2/P3 của lượt 1 **cố ý để ngoài** — đừng báo lại thành phát hiện mới, **nhưng** nếu
   lượt 4 làm nặng thêm mục nào thì đó là phát hiện MỚI.
6. **Sai khác nếp không khai:** lượt 3 để handoff **ngoài** reviewed commit (*"để không tự đổi
   exact SHA"*), lượt 4 **commit handoff vào chính `7f91ea1`**. Lease không cấm, tổng tệp vẫn ≤3.
   Có hệ quả gì không, hay chỉ là nếp?

Nghĩ ra thêm hướng nào thì **chạy nó**. Hướng nằm trong verdict dưới dạng câu chữ là hướng đi chết.

## Ngân sách

Đã dùng **124/125**, còn **1 dòng**. `can_sua` ⇒ **PHẢI nói bản vá đề xuất cần bao nhiêu dòng**,
đo bằng `git diff --numstat` (**không phải** dòng mã logic — verdict lượt 2 khai "5 dòng" trong
khi numstat là **8**, và `r4/Q14` đã đính chính).

## Điều kiện DỪNG

**A** lần 8 · **B** lần 3 · **C** lần 2 · **D** lần 4 · **E** lần **5** · **F** lần 3 ⇒ DỪNG.
Bộ đếm vào lượt này: A=7 · B=2 · C=1 · D=3 · **E=4** · F=2.

## Xuất

```
KET_LUAN: dat | can_sua | tu_choi
reviewed_sha: 7f91ea1cffe17af391362a91b83907c32b16f3b2
```

Mỗi phát hiện: **mức (P1/P2/P3) · phép đo đã CHẠY · số · vì sao quan trọng**. Không có phép chạy
thì không phải phát hiện. Kèm `chua_do_duoc` và bộ đếm `hinh_dang_ke_thua` sau lượt này.

Nếu `dat`: nói rõ **bạn đã tấn công ca `t73` bằng những gì** — vì bạn đang duyệt mã của chính nhà
cung cấp mình.

Nguồn sự thật là **tệp có băm trong kho**; prompt này chỉ là bản chiếu.
