# Prompt BẤT BIẾN — Reviewer chéo `DONREF-XOA-AN-TOAN` (#217), lượt **2/2**, provider `claude`

Executor `codex`, reviewer `claude` ⇒ cross-provider.

**Review DELTA**: `fa4b0dd..5f2ff857` — **một tệp** `ops/nhanh_don_duoc_test.py`, `+41/−18`.
Mã sản phẩm `ops/nhanh_don_duoc.py` **KHÔNG đổi một byte** (kiểm blob, đừng tin câu này).

Lượt 1 (chính bạn) đã trả **`approve`** trên `fa4b0dd` và nêu ba finding. Delta này vá cả ba.
**Đây là vòng CUỐI trong trần** — `changes_requested` ở đây đẩy packet lên checkpoint chủ kho.

Read-only với KHO: **không commit, không push, không đổi HEAD.** Đột biến chạy trên **BẢN SAO
TẠM** (`git -C kho archive <sha> | tar -x`).

```
./nhiem_vu.txt          prompt này
./DAC_TA.md             đặc tả ĐÓNG BĂNG — băm 1add3edf165faa2b53d6b52212ea34d7a73934367fd73bbca91e5518a9a664de
./VERDICT_LUOT_1.md     verdict lượt 1 của chính bạn (approve + 3 finding)
./diff_delta.patch      fa4b0dd..5f2ff857 — ĐÚNG phần phải soi
./kho/                  bản sao kho tại exact head, GHI ĐƯỢC
```

## 1. Mỏ neo

| trường | giá trị |
|---|---|
| exact head | `5f2ff8573ed259c1a4df3030428a4ec9b0f99e2e` — ĐO LẠI |
| head lượt 1 | `fa4b0dd879f0cf7ae589989863670d2a8200839c` |
| write set | `ops/nhanh_don_duoc_test.py` — **một tệp** |
| số ca | 7 → **8** · số mutant 7 → **10** |

**Việc đầu tiên: đối chiếu băm `DAC_TA.md`.** Lệch ⇒ DỪNG. Đặc tả **không đổi** ở lượt này.

## 2. Ba finding của bạn đã được vá thế nào

| finding | vá bằng |
|---|---|
| **P2** — ba nhánh rẽ cấp TOÀN KHO (`fetch` lỗi · kho nông · `base_oid != remote_oid`) không có đột biến nào nhắm vào | thêm **`T8`** (kho bare thật, ref cục bộ CŨ + fetch lần này hỏng) và **ba mutant** `bo-chan-fetch-loi` · `go-nhanh-kho-nong` · `dao-khop-base-remote` |
| **P3** — `T3` chưa đo phép lọc C trong lô TRỘN thật | thêm khẳng định `"ops/c-mot" not in lenh` vào `T3` |
| **P3** — prompt lượt 1 khai sai `rc=1` | **KHÔNG sửa prompt** (đã đóng băng, băm đã công bố). Executor khai: tệp test **không hề** ám chỉ `rc=1`; `return 1` còn lại là mã thất bại của **chính test runner**. **Kiểm lời khai ấy.** |

## 3. Trục phải soi

### 3.1 `T8` có ĐO THẬT không, hay chỉ CÓ MẶT

Đây là ca sinh ra để đóng P2 — nếu nó rỗng thì P2 chưa đóng, chỉ trông như đã đóng.

- Kho trong `T8` có **bare thật** không (`git init --bare`, `core.bare=true`), hay chỉ là thư mục?
- Ref cục bộ cũ có **thật sự đủ điều kiện A** trước khi phá remote không — kiểm bằng git **độc
  lập**, đừng tin phép phân loại của chính tool.
- Sau khi phá remote: nhánh vào **C kèm lý do**, và **không** lọt lệnh. Cả hai, không chỉ một.
- `T8` có nhánh "không thấy thì bỏ qua" nào không? Harness tính ĐẠT khi hàm không ném — một
  `return` sớm vẫn thành ĐẠT. Đây là bệnh `t24` kho đã trả giá.

### 3.2 Ba mutant mới có nhắm ĐÚNG chỗ không

`bo-chan-fetch-loi` · `go-nhanh-kho-nong` · `dao-khop-base-remote`. Với mỗi con: nó sửa **đúng
dòng** nào? Gỡ nó ra thì ca đích còn đỏ không? Có con nào **không bao giờ chạy tới** dòng nó sửa?

Kho này đã trả giá vì một runner đột biến ghi mọi bản sao vào **cùng một tệp tạm** và CPython
dùng lại `.pyc` cũ ⇒ mutant chạy mã của bản trước, báo `giet 0/1` suốt ba lượt review. **Kiểm
cơ chế cô lập của runner.**

### 3.3 Hai mutant giết NHIỀU ca — đúng hay là dấu hiệu ca chưa tách

Executor **tự khai**: `in-ca-C` → T3,T5,T8 (3/3) · `dao-khop-base-remote` → T1,T3,T6 (3/3).

Lease đòi "giết nhiều ca ⇒ nói ra", và executor đã nói. Câu hỏi của bạn: **có đúng không?**

- `in-ca-C` giết T3 là **hiệu quả của bản vá** (trước chỉ chết ở T5, kịch bản suy biến) — xác nhận.
- `dao-khop-base-remote` giết T1,T3,T6: đó là **một chốt phủ nhiều ca**, hay ba ca đang **đo
  chung một thứ**? Nếu là cái sau thì độ phủ mỏng hơn con số 8 gợi ra.

### 3.4 Lời khai có đúng bằng phép đo không

Hình dạng kho đã đếm **năm lần**. Bộ đếm **không tăng** qua hai lượt của `codex` — **kiểm lại
điều đó**, đừng nhận cho xong:

- Câu *"tệp test không hề khai hay ám chỉ `rc=1`"* — grep và xác nhận.
- Câu *"mã sản phẩm giữ nguyên blob"* — so băm blob, đừng đọc diff.
- Tên và thông điệp của ca/mutant mới có nói đúng thứ chúng đo không?

### 3.5 Hồi quy

`8/8`, `rc=0`, không tụt ca. Bảy ca cũ **vẫn đỏ đúng chỗ** dưới bảy mutant cũ. Chạy tool trên kho
thật, **đọc `rc` trực tiếp — KHÔNG qua ống** (`| head` đóng ống sớm ⇒ `BrokenPipeError` ⇒ thoát 1;
con số ấy đã từng đi vào một prompt).

## 4. NGOÀI phạm vi

P1 lượt 2 của `#213` (nhánh mặc định bị ép lùi) — đặc tả ghi **CỐ Ý ĐỂ MỞ**, công cụ **khai**,
không vá. Sửa `ops-don-ref.yml`, `CLAUDE.md`, dọn nhánh, rà 76 nhánh C — ngoài phạm vi.

## 5. Điều kiện DỪNG

- Cần sửa mã để chứng minh ⇒ bản sao tạm, KHÔNG sửa cây kho.
- Thấy một tiêu chí ở `§nghiem_thu` sai hoặc **không thể đỏ** ⇒ DỪNG và nói ra.
- Thứ đòi sửa ngoài write set ⇒ finding + đề xuất, không tự mở rộng.

## 6. Định dạng trả về

**IN RA STDOUT.** Kết thúc bằng **đúng hai dòng cuối**:

```
VERDICT: <approve|changes_requested|do_not_land>
Reviewed commit: <sha 40 ký tự đã ĐO>
```

Trước đó: finding · **"đã đo và sạch"** · **"chưa đo được — GIẢ THUYẾT"**.

**`approve` nghĩa là:** ba finding của bạn đã đóng **bằng đo**, `T8` thật sự đo, ba mutant mới có
răng, không hồi quy — và bạn vẫn **không tìm thấy** đường nào làm một nhánh còn commit riêng lọt
vào lệnh xoá. Đây là vòng cuối; `changes_requested` đẩy packet lên checkpoint chủ kho.
