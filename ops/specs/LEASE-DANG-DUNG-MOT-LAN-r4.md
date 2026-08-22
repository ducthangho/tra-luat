# ĐẶC TẢ ĐÓNG BĂNG — `LEASE-DANG-DUNG-MOT-LAN`, **bản sửa đổi 4** (delta)

> **CHỈ ghi phần thay đổi** so với r3 (`c65d5dbd…`), trên nền r2 (`3f310582…`).
> Mọi thứ không nêu ở đây thì r3/r2 vẫn nguyên hiệu lực.
> Bản 1, 2, 3 **KHÔNG bị sửa, KHÔNG bị xoá**.

`packet_id`: `LEASE-DANG-DUNG-MOT-LAN` · `packet_issue`: `#227`
`ke_thua`: r3 (`c65d5dbd9d2b398978226f6863cf7cd4e4ddb219a7086be0005e65804a0f47da`)
→ r2 (`3f310582de59dce7c109717dbab13ef9467b80c67ffeafc0ac8e1484309e0093`)
→ r1 (`e1026adb569f5b4732197afac9c0f35cdd5a8945d46301b1d4cb062624e7c72c`)

## Vì sao có bản này

Review lượt 3 (verdict `79f8bb2a48e92f9081cd50ba0d6d24a8f4bd7246d92ab0cc2d500e26ecfe24a0`):
**`can_sua`**, và **P1 cùng cả ba P3 của lượt 2 đều ĐÓNG**. Còn một P2 + một P3.

**P2:** nhánh `rc=9` của `kiem-github` — chốt chống **đăng trùng xuyên nhánh**, tức đúng thứ
packet mang tên — **không có phản chứng nào**. Đo hai tầng, trên bản sao tạm dựng bằng
`git archive` head `9f5b08e8`:

```
đột biến D24 (rc=9 không còn dừng, ĐI TIẾP)   ->  suite 61/61, actionlint rc=0   SỐNG SÓT
hành vi thật (thân bước trích từ YAML, lease `giua` ĐÃ CÓ comment trên issue):
   bản gốc   rc=0   2 lần POST    (đúng — `giua` bị bỏ qua)
   D24       rc=0   3 lần POST    (ĐĂNG TRÙNG)
```

## PHÂN XỬ CỦA NGƯỜI GIỮ KHO — ghi thẳng, không làm tròn

**r3 đăng ký trước:** *"hình dạng C (phản chứng bắt buộc còn thiếu) lần thứ 2 ⇒ DỪNG, không vá,
xuất handoff."* P2 **đúng là hình dạng C**, ở đúng khối mà C lần 1 chỉ vào. Reviewer nêu hai cách
đọc và **từ chối tự quyết**, đẩy về người giữ kho (§2).

**Người giữ kho quyết (2026-08-21): đọc là *"C lần 1 CHƯA ĐÓNG HẾT"*, KHÔNG tăng bộ đếm C.**
Cấp lượt vá 4.

Đây là một **override có chủ đích** đối với một chốt DỪNG đã đăng ký trước — ghi ra nguyên trạng
để không ai đọc thành "chốt ấy không tồn tại" hay "chốt ấy tự động mềm". Căn cứ:

- `r3` **chỉ đặt hàng** `T59`/`T60`, tức nửa *"workflow CÓ gọi"* và *"tôn trọng `rc≠0`"*. Executor
  giao **đủ**, còn vượt: reviewer tự dựng D12 (đảo thứ tự), D13 (bỏ đúng một lease), D14/D15
  (tách hai vế của `t60`) — **tất cả đều bị bắt**. Nửa `rc=9` **không nằm trong đơn hàng**.
- Vì vậy đây là **đơn hàng thiếu**, không phải **executor bỏ sót**. Chốt DỪNG sinh ra để chặn
  "vá tiếp lần thứ n cùng một hình dạng do người thi công"; ở đây mắt xích yếu là **đặc tả**.

**Lần thứ BA đặc tả của phiên điều phối là mắt xích yếu của packet:** bản 1 gây P1 lượt 1 · prompt
lượt 2 chứa một tiền đề chưa đo · `r3` đặt hàng thiếu nửa nhánh. Ba lần cùng một chỗ ⇒ xem Q24.

## Quyết định MỚI — Q20…Q24

| # | quyết định | căn cứ ĐO ĐƯỢC |
|---|---|---|
| **Q20** | Bộ đếm **C giữ 1**. Không tăng. | Phân xử §2 ở trên. |
| **Q21** | Trần **550 → 570** dòng thêm; `attempts` **3 → 4**. | Head `+523`. Bản vá P2 ~15 dòng cộng ca thứ hai cho `check`. |
| **Q22** | Vá **CẢ HAI** nhánh `rc=9`: của `kiem-github` **và** của `check`. | Nhánh của `check` có **delta = 0** so `cfaccff9` (reviewer đo D23 sống sót `61/61` rồi **KHÔNG** báo là finding — đúng doctrine "đo nền trước"). Người giữ kho **cố ý mở rộng phạm vi**: vá một thể rẻ hơn, và hai nhánh cùng một lớp. Ghi ra vì đây là mở rộng phạm vi có chủ đích, không phải phạm vi trôi. |
| **Q23** | Sửa con số trong tiêu chí nghiệm thu: đột biến *"cho `kiem()` gọi mạng trở lại"* giết **9** ca, không phải 8. | Đo trên cả `9f5b08e8` (52/61) lẫn `90015a53` (49/58): `t01 t02c t02d t09 t14 t21 t50 t53 t58`. Sai số sinh ở verdict lượt 2 (gộp `t02c`/`t02d` thành `t02`), `r3` chép lại rồi biến thành **tiêu chí**. |
| **Q24** | **Đơn vị của câu hỏi "phép đo nào ĐỎ nếu ai đó gỡ nó?" là NHÁNH, không phải KHỐI.** | Đây là bài học thật của ba lượt: `r3` hỏi câu ấy ở mức **khối** (`kiem-github`), nên nửa `rc=9` **của cùng khối** lọt. Từ lượt 4, executor phải **liệt kê từng nhánh rẽ** của mã mới trong `write_set` và trả lời cho **từng nhánh**. Nhánh nào không có câu trả lời ⇒ hoặc thêm ca, hoặc **khai thẳng** vào `chua_do_duoc`. |

## `nghiem_thu` — HAI ca thêm

Giữ `T43`–`T61`. Đột biến chạy trên **BẢN SAO TẠM**.

| # | tiêu chí | đột biến làm nó ĐỎ |
|---|---|---|
| **T62** | `kiem-github` trả **`9`** ⇒ lease đó **KHÔNG** được POST, hai lease kia POST bình thường, và bước **`rc=0`** (bỏ qua ≠ lỗi). | **D22** — `rc=9` bị coi là LỖI (bước đỏ oan) · **D24** — `rc=9` ĐI TIẾP (đăng trùng). **Hai đột biến riêng, hai hướng ngược nhau.** D24 hiện **SỐNG SÓT `61/61`**. |
| **T63** | `check` trả **`9`** ⇒ y hệt `T62`. | **D23** — `rc=9` của `check` ĐI TIẾP. Hiện **SỐNG SÓT `61/61`** (delta = 0, vá theo Q22). |

Ngoài hai ca: suite `rc=0`, `N/N` hai số bằng nhau, **≥ 63 ca**; đột biến giết nhiều ca phải được
**KHAI**; con số cho *"cho `kiem()` gọi mạng trở lại"* là **9** (Q23).

## `ngoai_pham_vi` — không đổi

Giữ nguyên r2/r3. Nhấn lại: **`ops/specs/**` ngoài `write_set`** — đính chính `chua_do_duoc` của
r2/r3 thuộc **biên nhận**, phiên điều phối làm.

## `hinh_dang_ke_thua`

**A** *lời khai rộng hơn phép đo* = **6** · **B** *mượn tiền lệ mà không đo* = **2** ·
**C** *phản chứng bắt buộc còn thiếu* = **1** (Q20).

**Hình dạng MỚI — D: *đặt câu hỏi kiểm chứng ở SAI ĐỘ PHÂN GIẢI*.** Bộ đếm **1**:
`r3` hỏi *"phép đo nào ĐỎ nếu gỡ nó?"* ở mức **khối**, nên nửa `rc=9` **của cùng khối** lọt.
Cùng họ với *"đếm sự CÓ MẶT thay vì KHẢ NĂNG"* — chỉ khác trục: ở đây là **độ mịn** của câu hỏi.

**Chốt cho lượt 4:** **A** lần 7 · **B** lần 3 · **C** lần 2 · **D** lần **2** ⇒ **DỪNG, không
vá**, xuất handoff. **C lần 2 nay có định nghĩa chặt hơn** (kẻo lại phải phân xử lần nữa): một
chốt an ninh **KHÔNG nằm trong đơn hàng của `T62`/`T63`** mà thiếu phản chứng.

## `chua_do_duoc` — thêm

Giữ mọi mục của r2/r3, thêm bốn thứ lượt 3 đo được:

1. **`t59` chỉ so `argv[0:2]`** — đổi hoặc bỏ cờ phía sau (vd `--root .`) **vô hình** với nó.
   Reviewer đo: đột biến bỏ `--root .` sống sót `61/61`, **nhưng** chú thích YAML tự khai cờ ấy
   là dư (`_goc_kho` đi ngược tìm `.git` ra cùng chỗ) ⇒ lời khai ĐÚNG, **không** phải khuyết tật.
2. **Nợ nền `chay(env=None)`**: `GITHUB_ACTOR` ngoài allowlist ⇒ `39/61`. **Delta = 0** so
   `cfaccff9` ⇒ không phải finding của packet, nhưng vẫn là mìn cho `ci.yml` khi có actor khác đẩy.
3. **Báo cáo của executor không sống trong kho.** `r3` đòi khai đường Q18 và đột biến đa sát;
   executor **có** khai, nhưng kênh khai là **stdout của lượt chạy**, không phải một tệp có băm.
   Reviewer lượt 3 vì vậy **không đo được** lời khai ấy và nói thẳng *"không kết luận là chưa
   khai"*. Đây là **khoảng mù của quy trình**, không phải lỗi của ai — và nó chưa được vá.
4. **Vẫn chưa có lượt GitHub Actions THẬT nào** trên bất kỳ head nào của packet, và chưa có
   Windows. Mọi phép đo workflow là thân bước trích từ YAML chạy dưới `bash` tại chỗ.
