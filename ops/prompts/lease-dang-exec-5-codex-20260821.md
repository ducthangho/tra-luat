# Prompt EXECUTOR — `LEASE-DANG-DUNG-MOT-LAN` (#227), lượt **5**

Bạn là **executor** lượt 5. Lease `lease-dang-exec-5-codex-20260821`.

**ĐỌC ĐOẠN NÀY TRƯỚC.** Lượt 4 bạn giao **đủ** `T62`/`T63`/`Q23` — đã đo lại độc lập và khớp
từng con số. Rồi bạn **TỰ DỪNG** ở chốt `C lần 2` thay vì vá tiếp, và **bạn đúng**: gỡ guard
`mark rc≠0` sống sót `63/63`, phiên điều phối đo lại và xác nhận. **Chốt đăng ký trước đã chạy
thật, nhờ bạn tôn trọng nó.** Đó là kết quả tốt nhất của cả packet cho tới giờ.

Bảng `Q24` của bạn còn lộ ra thứ lớn hơn: **không phải một nhánh mà một LỚP** — sáu guard thiếu
phản chứng. Và thủ phạm là **đặc tả**, không phải bạn: `r2`/Q11 đặt hàng *"bọc `set +e` quanh mọi
lệnh"* ở mức **khối** mà không đặt hàng phản chứng cho **từng guard**.

## Nguồn sự thật

1. **`ops/specs/LEASE-DANG-DUNG-MOT-LAN-r5.md`** — DELTA, sha256
   `2c8fb5c68e45dbdcd3e21c316169623d4dcab33459934b575ae8c626b08cb796`
2. r4 `abe7c292…` · r3 `c65d5dbd…` · r2 `3f310582…` — nguyên hiệu lực cho mọi thứ r5 không nêu.
3. **Handoff lượt 4 của chính bạn** — `ops/handoff/lease-dang-exec-4-codex-handoff.md`, sha256
   `dfada28511f0b63e4922b98fa08b55cb03d57f28faccfb9709b227e316c291b7`. **Bảng `Q24` trong đó là
   đầu vào chính của lượt này.**
4. `CLAUDE.md`.

Lấy từ `origin/ops/lease-dang-227`. **KIỂM BĂM; lệch ⇒ DỪNG.**

## Việc — một ý tưởng, ba ca

**KHÔNG liệt kê nhánh nữa.** Cách liệt kê đã thất bại **hai lượt liên tiếp** (hình dạng D, bộ đếm
2, cả hai lần do phiên điều phối). Lượt này **đổi kiến trúc**:

### `T64` — ca META: DẪN XUẤT danh sách guard TỪ YAML

Trích thân bước `đăng` **từ chính `.github/workflows/ops-publish-lease.yml`** (tiền lệ
`t32`/`t51`/`t59`), tìm **mọi** lệnh được bọc `set +e … rc=$? … set -e`, rồi đối chiếu tập ấy với
một **sổ đăng ký** trong tệp test. **Lệch ⇒ ĐỎ.**

Hai đột biến, **hai hướng ngược nhau**, cả hai phải chết:
- **M1** — thêm một lệnh bọc `set +e` vào **YAML** mà **không** đăng ký ⇒ ĐỎ.
- **M2** — xoá một mục khỏi **sổ đăng ký** ⇒ ĐỎ.

**M1 là phép thử quyết định.** Thêm guard vào YAML mà suite vẫn xanh ⇒ bộ trích đang đọc **bản
chép**, không đọc YAML thật. Nếu vậy thì chính bản vá kiến trúc cho D lại mắc D ⇒ **DỪNG** (chốt
đăng ký trong r5).

### `T65` — `T64` phải FAIL-CLOSE

Bộ trích trả **rỗng** hoặc **không phân tích được** ⇒ **ĐỎ**, không phải *"không có guard nào"*.
Ba trạng thái: `N>0` · `không phân tích được` · `N=0` — **hai trạng thái sau đều ĐỎ**.
**M3** — làm bộ trích trả `[]` ⇒ phải ĐỎ.

### `T66` — mỗi guard trong sổ có ca THẬT

Ca ấy làm lệnh đó hỏng và khẳng định **bốn vế**: lease đó **không** POST · lease khác **vẫn** được
xử · `BI_CHAN` đặt đúng · mã thoát bước đúng.

Bao đủ **sáu nhánh còn hở** mà bảng `Q24` của bạn đã liệt: `packet_issue` · `body` · dựng payload
· `case ID` phi-số · `mark` · ghi `$GITHUB_ENV`.

Gỡ **từng** guard ⇒ ca **của guard đó** ĐỎ. **Gỡ `mark`, `body`, `$GITHUB_ENV` hiện SỐNG SÓT
`63/63`** — cả ba phải chết.

## KHÔNG làm

- **Đừng vá `_doc_gh` / `_kiem_loai_so_hieu` / `_kiem_comment_da_co`** cho những nhánh bảng `Q24`
  xếp *"một phần"*. Chúng là **hàm Python**, không phải guard shell ⇒ ngoài đơn hàng `T64`–`T66`.
  Thấy nhánh nào đáng lo thì **KHAI vào `chua_do_duoc`**, đừng tự mở phạm vi. Đây đúng chỗ hai
  lượt trước đã trượt — lần này ranh giới được vẽ sẵn.
- Sửa `ops/specs/**` · đụng lại finding đã đóng · đóng khe race · vá nợ nền `chay(env=None)`.

## Ngân sách

**≤ 3 tệp, ≤ 620 dòng THÊM** so với `cfaccff9`. Head `b32b4241` đang **`+541`** ⇒ còn **~79 dòng**.
Vượt ⇒ **DỪNG, xuất handoff**. Dòng xoá không tính.

Gợi ý: một ca `T66` **tham số hoá** chạy qua sáu guard rẻ hơn nhiều so với sáu ca chép tay — và
nó cũng khớp tinh thần Q25 (đừng liệt kê thứ máy dẫn xuất được).

## Cổng bắt buộc

| cổng | tiêu chí |
|---|---|
| `python3 ops/lease_publish_test.py` | `rc=0`, `N/N` bằng nhau, **≥ 66 ca** |
| cùng suite, `GITHUB_ACTIONS`+`GITHUB_REPOSITORY`+`GITHUB_ACTOR` đặt, `gh` **vắng** | `N/N` y hệt |
| `actionlint .github/workflows/*.yml` | `rc=0` cả 5 |
| **M1** thêm guard vào YAML, không đăng ký | **PHẢI ĐỎ** — phép thử quyết định |
| **M2** xoá một mục khỏi sổ đăng ký | **PHẢI ĐỎ** |
| **M3** bộ trích trả `[]` | **PHẢI ĐỎ** |
| gỡ **từng** guard trong sáu guard | ca của guard đó **PHẢI ĐỎ** (`mark`/`body`/`$GITHUB_ENV` hiện sống sót `63/63`) |
| kích thước | ≤ 3 tệp, ≤ 620 dòng thêm — số THẬT |

## Điều kiện DỪNG

- Ngân sách sẽ vượt 620 ⇒ DỪNG + handoff.
- Chốt phải nằm ngoài `write_set` ⇒ DỪNG + handoff.
- **A** lần 7 · **B** lần 3 · **C** lần 2 · **D** lần **3** ⇒ DỪNG, không vá.
- **`M1` không giết được `T64`** ⇒ **DỪNG**. Khi ấy bản vá kiến trúc cho D lại mắc D, và câu hỏi
  đúng không còn là *"vá thế nào"*.

## Báo cáo cuối

1. `git diff --numstat cfaccff9..HEAD` — số thật.
2. `N/N`, hai lần chạy.
3. Bảng đột biến, nêu riêng **M1, M2, M3** và **sáu** đột biến gỡ guard. Kèm danh sách đa sát.
4. **Sổ đăng ký guard** — in ra tập **dẫn xuất từ YAML** và tập trong sổ, cạnh nhau, để người đọc
   thấy chúng bằng nhau bằng mắt chứ không chỉ tin một ca xanh.
5. `chua_do_duoc` của riêng bạn. **"Thu hẹp"** khi chỉ thu hẹp; **"đóng"** chỉ khi có phép đo.

Nguồn sự thật là **tệp có băm trong kho**; prompt này chỉ là bản chiếu.
