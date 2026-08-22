# Prompt EXECUTOR — `LEASE-DANG-DUNG-MOT-LAN` (#227), lượt **7**

Lease `lease-dang-exec-7-codex-20260822`.

**ĐỌC ĐOẠN NÀY TRƯỚC.** Phần **cốt lõi** của lượt 6 **ĐẠT**, và reviewer đo rất kỹ để khẳng định
điều đó: **tám** hướng tấn công vào chính phép dẫn xuất vị trí, **bảy ĐỎ**, cái thứ tám xanh
**đúng**. Bốn đột biến *"guard còn nhưng hành vi sai"* cũng chết — **không ca nào trống ruột**,
kể cả guard `$GITHUB_ENV` mà bạn tự khai là yếu. Bằng chứng đẹp nhất: `t66` **không** chết dưới
`M4` vì kỳ vọng của nó **trôi theo YAML**; chỉ `t67` chết.

Còn **hai** lỗ, và chúng **cùng một gốc**: *khoá theo thứ ta **liệt kê được**, thay vì theo thứ
**thật sự chặn***.

## Nguồn sự thật

1. **`ops/specs/LEASE-DANG-DUNG-MOT-LAN-r7.md`** — DELTA, sha256
   `623b23555a6fa43dad2d9badeaac3a6f852c0be6b9927d4593992f6e10310cb4`
2. r6 `4ee67d54…` · r5 `2c8fb5c6…` · r4 `abe7c292…` · r3 `c65d5dbd…` · r2 `3f310582…`
3. **Verdict lượt 4** `0655b9d0caea1d49450b4b8013f79cd49af61adc62b261bdce2085b76b17614f` — nó
   **nguyên mẫu sẵn** cả hai bản vá và **đã đo**. Đọc kỹ.
4. `CLAUDE.md`.

Lấy từ `origin/ops/lease-dang-227`. **KIỂM BĂM; lệch ⇒ DỪNG.**

## Việc — ba thứ, và thứ nhất là ĐẢO MỘT NGUYÊN TẮC

### `T64′` (Q32) — ĐẢO danh sách CẤM thành danh sách CHO PHÉP

`_guard_dan_xuat` hiện neo vào **đúng một** mẫu (`^set +e$` … `^rc=$?$` … `^set -e$`). Đo được:

```
them guard chan THAT kieu `if ! cmd`     ->  67/67  LOT
them guard chan THAT kieu `cmd || rc=$?` ->  67/67  LOT
them guard kieu chinh tac                ->  66/67  DO t64   (bat duoc)
```

Đây đúng bài học của kho: **danh sách CẤM phải đoán trước mọi cách viết nên thua từ trong thiết
kế; danh sách CHO PHÉP chỉ phải liệt kê một tập nhỏ và biết trước.** Chính `lease_publish.py` đã
trả giá ở `granted_by`.

**Đơn vị khoá đổi từ *"khối `set +e`"* sang *"NHÁNH CHẶN"***, và nhánh chặn có **một** dấu hiệu
bắt buộc: nó gọi **`bao_chan`** — thứ **duy nhất** đặt `BI_CHAN`. Đếm `bao_chan`, đòi **mọi** lời
gọi nằm trong tập đã đăng ký.

Reviewer đã nguyên mẫu và đo: `if ! cmd` · `cmd || rc=$?` · `set +e` một dòng — **cả ba chuyển
sang ĐỎ**. Bạn tự dựng lại, đừng chép mù.

### `T68` (Q33) — nhánh chặn của khối POST, và XOÁ dấu `+1`

```
go NHANH CHAN cua khoi POST (giu nguyen set +e/rc=$?/set -e)  ->  67/67 XANH TRON VEN
```

**Không** phải equivalent mutant: đồ giả `gh` trả `rc=1` **nhưng in một id SỐ hợp lệ** — đúng
tình huống nhánh ấy sinh ra để chặn — và khi gỡ, lease `giua` **được `mark` bằng id đến từ một
lời gọi hỏng**.

Gốc: mục #6 của sổ khoá **khối POST** nhưng **đặt tên `case_id`**, còn ca của nó bơm lỗi vào câu
`case "$ID"` — một nhánh nằm **ngoài mọi khối**. **Cái tên đã che chỗ hở.**

Đăng ký nhánh `case "$ID"` **tường minh**, đặt lại tên mục #6 cho khớp thứ nó khoá. Sau đó
**không còn dấu `+1`**: số `bao_chan` phải **BẰNG** số mục trong sổ. Đo nền hôm nay: **9**
`bao_chan` vs **8** khối — chênh đúng 1, chính là nhánh ấy.

`T68` khẳng định: `rc` bước `=1` · `giua` POST **đúng một lần** · `marks["giua"]` là **False**.
Đột biến **A5** (gỡ nhánh ấy) hiện **sống sót `67/67`** — phải chết.

### `T65′` (Q34) + Q35 — hai hạt nhỏ

- `_ve_dan_xuat` fail-close phải có **ca riêng**, không sống nhờ `except Exception` của `main()`.
  Bọc `try` quanh nó, hoặc `next(…, mặc_định)` ⇒ phải ĐỎ.
- `ghe.exists()` → kiểm **tệp**, kẻo `IsADirectoryError` biến một lỗi sản phẩm tương lai thành
  cú crash khó đọc.

## Ngân sách — KHÔNG nới, lần đầu trong packet này

**≤ 3 tệp, ≤ 660 dòng THÊM.** Head `6eaa3755` đang **`+633`** ⇒ còn **27 dòng**.
Reviewer đo ba bản vá ≈ **15 dòng** (9 + 2 + 4) ⇒ **lọt**.

Vượt 660 ⇒ **DỪNG, xuất handoff**. Dòng xoá không tính.

## Cổng bắt buộc

| cổng | tiêu chí |
|---|---|
| `python3 ops/lease_publish_test.py` | `rc=0`, `N/N` bằng nhau, **≥ 68 ca** |
| cùng suite, ba biến GitHub đặt, `gh` **vắng** | `N/N` y hệt |
| `actionlint .github/workflows/*.yml` | `rc=0` cả 5 |
| **D2** `set +e` một dòng · **D3** `if ! cmd` · **D4** `cmd \|\| rc=$?` | **cả ba PHẢI ĐỎ** — hiện sống sót `67/67` |
| **A5** gỡ nhánh chặn của khối POST | **PHẢI ĐỎ** — hiện sống sót `67/67` |
| `M1` `M2` `M3` `M4` và tám đột biến gỡ guard | **vẫn phải ĐỎ** (đừng làm hỏng thứ đang chạy) |
| số `bao_chan` == số mục trong sổ | **không còn dấu `+1`** |
| kích thước | ≤ 3 tệp, ≤ 660 dòng thêm — số THẬT |

## KHÔNG làm

`ops/specs/**` · đổi thứ tự lệnh trong thân bước `đăng` · rollback · preflight · finding đã đóng ·
khe race · nợ nền `chay(env=None)` · `_doc_gh`/`_kiem_loai_so_hieu`/`_kiem_comment_da_co` (nhánh
*"một phần"*).

## Điều kiện DỪNG

- Ngân sách sẽ vượt 660 ⇒ DỪNG + handoff. **Không tự nới** (§2).
- **A** lần 7 · **B** lần 3 · **C** lần 2 · **D** lần 4 · **E** lần **2** ⇒ DỪNG.
  **E** = *khoá theo thứ liệt kê được thay vì theo thứ thật sự chặn*, bộ đếm **1**.
  **E lần 2** = sau khi đảo sang `bao_chan`, **lại** tìm được một nhánh chặn **không** gọi
  `bao_chan`. Khi ấy dấu hiệu nhận dạng vẫn sai, và câu hỏi đúng không còn là *"vá thế nào"*.
  **Trước khi báo xong: tự đi tìm một nhánh như vậy.** Không tìm được thì nói là không tìm được.

## Báo cáo cuối

1. `git diff --numstat cfaccff9..HEAD` — số thật.
2. `N/N`, hai lần chạy.
3. Bảng đột biến: **D2 D3 D4 A5** và **M1 M2 M3 M4** + tám đột biến gỡ guard. Danh sách đa sát.
4. **Sổ đăng ký sau Q33** — in số `bao_chan` và số mục trong sổ **cạnh nhau**, chứng minh bằng
   nhau, **không `+1`**.
5. `chua_do_duoc` của riêng bạn, kèm kết quả cuộc đi tìm *"nhánh chặn không gọi `bao_chan`"*.

Nguồn sự thật là **tệp có băm trong kho**; prompt này chỉ là bản chiếu.
