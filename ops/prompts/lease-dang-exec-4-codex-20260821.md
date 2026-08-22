# Prompt EXECUTOR — `LEASE-DANG-DUNG-MOT-LAN` (#227), lượt **4**

Bạn là **executor** lượt 4. Lease `lease-dang-exec-4-codex-20260821`.

**ĐỌC ĐOẠN NÀY TRƯỚC:** lượt 3 của bạn **giao đủ đơn hàng, còn vượt**. Review lượt 3 xác nhận
`T59`/`T60` đóng thật, và reviewer tự dựng thêm bốn hướng tấn công (đảo thứ tự · bỏ đúng một
lease · tách hai vế) — **tất cả đều bị bắt**. Cái còn thiếu **không nằm trong đơn hàng của r3**.
Người viết r3 là phiên điều phối, và **đó là lần thứ ba đặc tả của phiên ấy là mắt xích yếu**.
Nói ra để bạn khỏi tự bào mòn: việc còn lại là **hoàn tất một khối**, không phải sửa lỗi của bạn.

## Nguồn sự thật

1. **`ops/specs/LEASE-DANG-DUNG-MOT-LAN-r4.md`** — DELTA, sha256
   `abe7c292aba05aa772b77c246a570d72c9b8e97220247030ae15af8f750d0fce`
2. r3 `c65d5dbd9d2b398978226f6863cf7cd4e4ddb219a7086be0005e65804a0f47da` ·
   r2 `3f310582de59dce7c109717dbab13ef9467b80c67ffeafc0ac8e1484309e0093` — nguyên hiệu lực cho
   mọi thứ r4 không nêu.
3. **Verdict lượt 3** `79f8bb2a48e92f9081cd50ba0d6d24a8f4bd7246d92ab0cc2d500e26ecfe24a0` — có
   **lệnh chạy được** và **mô tả sẵn cách vá**.
4. `CLAUDE.md`.

Lấy từ `origin/ops/lease-dang-227`. **KIỂM BĂM; lệch ⇒ DỪNG.**

## Việc — đúng ba thứ

### 1. `T62` — nhánh `rc=9` của `kiem-github` (BẮT BUỘC)

Đây là chốt chống **đăng trùng xuyên nhánh**: lease đã đăng từ nhánh A, nhánh B chưa được ghi
ngược `posted_comment_id`, nên `check` ở B trả `0`. `kiem-github` trả `9` là **cửa duy nhất**
chặn POST lần hai. Nó **không có phản chứng nào**:

```
D24 (rc=9 không còn dừng, ĐI TIẾP)  ->  61/61, actionlint rc=0   SỐNG SÓT
hành vi thật, lease `giua` ĐÃ CÓ comment:  bản gốc 2 POST  ·  D24 3 POST (ĐĂNG TRÙNG)
```

Thêm tham số `kiem_github_rc9=` vào `_chay_buoc_dang` (đồ giả trả `9`), rồi ca `t62`: lease đó
**không** được POST · hai lease kia POST bình thường · bước **`rc=0`** (bỏ qua ≠ lỗi).

**Hai đột biến, hai hướng NGƯỢC NHAU, cả hai PHẢI CHẾT:**
- **D22** — `rc=9` bị coi là LỖI (bước đỏ oan).
- **D24** — `rc=9` ĐI TIẾP (đăng trùng). Hiện **sống sót `61/61`**.

### 2. `T63` — nhánh `rc=9` của `check`

Cùng lớp. Reviewer đo **D23 sống sót `61/61`**, nhưng **delta = 0** so `cfaccff9` nên họ **không**
báo là finding — đúng doctrine. **Người giữ kho cố ý mở rộng phạm vi** để vá một thể (Q22).
Ca `t63`: y hệt `t62` nhưng cho `check`. **D23 phải CHẾT.**

### 3. Sửa con số: **9**, không phải 8 (Q23)

Đột biến *"cho `kiem()` gọi mạng trở lại"* giết **9** ca: `t01 t02c t02d t09 t14 t21 t50 t53 t58`.
Đo trên cả `9f5b08e8` (52/61) lẫn `90015a53` (49/58). Sai số sinh ở verdict lượt 2 (gộp
`t02c`/`t02d` thành `t02`), r3 chép lại rồi biến thành **tiêu chí nghiệm thu**. Sửa mọi chỗ khai
"8 ca" trong `write_set` nếu có.

## Q24 — BẮT BUỘC, và nó là bài học của cả packet

**Đơn vị của câu hỏi *"phép đo nào ĐỎ nếu ai đó gỡ nó?"* là NHÁNH, không phải KHỐI.**

r3 hỏi câu ấy ở mức **khối** (`kiem-github`), nên nửa `rc=9` **của cùng khối** lọt. Từ lượt này:
**liệt kê TỪNG NHÁNH RẼ** của mã mới trong `write_set` — mỗi `if`, mỗi `case`, mỗi mã thoát được
phân biệt — và trả lời cho **từng nhánh**. Nhánh nào không có câu trả lời thì **hoặc thêm ca,
hoặc KHAI THẲNG vào `chua_do_duoc`**. Bảng ấy là **mục bắt buộc của báo cáo cuối**.

## Ngân sách

**≤ 3 tệp, ≤ 570 dòng THÊM** so với `cfaccff9`. Head `9f5b08e8` đang **`+523`** ⇒ còn **~47 dòng**.
Vượt ⇒ **DỪNG, xuất handoff**. Dòng xoá không tính.

## Cổng bắt buộc

| cổng | tiêu chí |
|---|---|
| `python3 ops/lease_publish_test.py` | `rc=0`, `N/N` bằng nhau, **≥ 63 ca** |
| cùng suite, `GITHUB_ACTIONS`+`GITHUB_REPOSITORY`+`GITHUB_ACTOR` đặt, `gh` **vắng** | `N/N` y hệt |
| `actionlint .github/workflows/*.yml` | `rc=0` cả 5 |
| **D22** `rc=9` của `kiem-github` thành LỖI | **PHẢI ĐỎ** |
| **D24** `rc=9` của `kiem-github` ĐI TIẾP | **PHẢI ĐỎ** — hiện sống sót `61/61` |
| **D23** `rc=9` của `check` ĐI TIẾP | **PHẢI ĐỎ** — hiện sống sót `61/61` |
| kích thước | ≤ 3 tệp, ≤ 570 dòng thêm — số THẬT |

## KHÔNG làm

Sửa `ops/specs/**` · đụng lại các finding đã đóng · đóng khe race hai nhánh `ops/**` ·
vá nợ nền `chay(env=None)` (delta = 0, ngoài phạm vi).

## Điều kiện DỪNG

- Ngân sách sẽ vượt 570 ⇒ DỪNG + handoff.
- Chốt phải nằm ngoài `write_set` ⇒ DỪNG + handoff.
- **A** lần 7 · **B** lần 3 · **C** lần 2 · **D** lần 2 ⇒ DỪNG, không vá.
  **C lần 2** = một chốt an ninh **KHÔNG thuộc đơn hàng `T62`/`T63`** mà thiếu phản chứng — và
  **bảng Q24 chính là thứ phát hiện ra nó**. Làm bảng ấy TRƯỚC khi tuyên bố xong.

## Báo cáo cuối

1. `git diff --numstat cfaccff9..HEAD` — số thật.
2. `N/N`, hai lần chạy (thường · Actions không `gh`).
3. Bảng đột biến, nêu riêng **D22, D23, D24**. Kèm danh sách đột biến giết **nhiều** ca (con số
   cho *"kiem() gọi mạng lại"* là **9**).
4. **Bảng Q24** — từng nhánh rẽ của mã mới ↔ phép đo nào ĐỎ nếu gỡ nó ↔ (nếu không có) đã khai
   vào `chua_do_duoc` chưa.
5. `chua_do_duoc` của riêng bạn. **"Thu hẹp"** khi chỉ thu hẹp; **"đóng"** chỉ khi có phép đo.

Nguồn sự thật là **tệp có băm trong kho**; prompt này chỉ là bản chiếu.
