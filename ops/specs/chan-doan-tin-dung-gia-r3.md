# `CHAN-DOAN-TIN-DUNG-GIA` — revision 3

| trường | giá trị |
|---|---|
| `packet_id` | `CHAN-DOAN-TIN-DUNG-GIA` |
| `packet_issue` | #568 |
| `revision` | 3 |
| `revision tiền nhiệm` | 2 (spec `43cb42b908ae72c8…`, đã thi công ở PR #590) |
| `executor` | `claude` |
| `assurance_target` | `human_audited` — không đổi |
| `review_class` | `sensitive` — vẫn chạm CHÍNH bộ phân hạng đột biến |
| `base` | `45ea2921bb14de1eeb2bf0063fda95b63f1f0f7e` (head PR #590) |

## `nguon_cap_viec`

Đo từ kết quả chạy `do-568-windows.ps1` của chủ kho (gói `do-568-windows-20260920-174002.zip`),
đối chiếu log runner PR #590 và một phép tái hiện đầu-cuối. Đăng đầy đủ tại
[#568 issuecomment-5755428171](https://github.com/ducthangho/tra-luat/issues/568#issuecomment-5755428171).

Chỉ thị chủ kho, nguyên văn, hai lượt:
1. Trả lời ba câu hỏi của executor: **"1. r3 / 2. gộp / 3. Đăng lên đi"**.
2. Sau khi executor khai vật cản của "gộp" (hai người giữ khác trên
   `ops/lease_publish_test.py`, và trần `≤3 tệp` của `ADR-0044:5`): **"Hình A, cấp r3 đi"**.

## Vì sao đây là REVISION chứ không phải generation

`PROTOCOL_DA_PHIEN.md:300`: *"Mở rộng phạm vi hay đổi closure là revision mới, generation mới và cấp lại lease."*

r2 đóng băng ở `43cb42b9…` với A8–A12. Bản vá này **thêm tiêu chí nghiệm thu mới** (mô-đun phải
biên dịch với 0 cảnh báo escape-sequence) và **sửa kích thích của ca `r525` đã thi công trong r2**.
Cả hai đều là đổi closure ⇒ revision.

Executor có lập luận rằng bản vá này *"cần để chính A8 của r2 đúng ngoài đời"* nên có thể đi dưới r2.
Chủ kho **bác**. Ghi lại vì sao lời bác ấy đúng: hình dạng `LOI-KHAI-RONG-HON-PHEP-DO` vừa tái diễn
**lần thứ tư**, và tự nới closure trong đúng tình huống này là đúng cái cơ chế sinh ra nó.

## Bệnh — đã ĐO, có phản chứng chạy được

Hai docstring `"""…"""` **không raw** chứa `\d` — dòng **2213** và **2723** của
`ops/nhanh_don_duoc_test.py`, do chính `18d6519` (bản vá r1) đưa vào.

Quy trách nhiệm, biên dịch từng mốc rồi đếm cảnh báo escape-sequence:

```
dc85dd0a : 0      ← nền trước r1
18d6519  : 2      ← BẢN VÁ r1 ĐƯA VÀO
eb4a9ab  : 2      ← head PR #572
45ea292  : 2      ← head PR #590
```

Khớp với phép đo trên máy chủ kho: `nen-*.err.txt` = 0 B / 0 cảnh báo; `ung-vien-*.err.txt`
= 17 222 B / 80 cảnh báo mỗi lượt.

Hậu quả đo được:

```
TRAN_CHAN_DOAN                            = 400 ký tự
khối cảnh báo của MỘT tiến trình con      = 425 ký tự
⇒ % ngân sách 400 bị cảnh báo chiếm       = 100 %
```

`_goi_chan_doan` cắt **từ đầu** (giữ 400 ký tự ĐẦU), nên nguyên nhân thật nằm sau bị cắt sạch.

Hai nhánh đọc `p.stderr` là `ops/nhanh_don_duoc_test.py:2844` (**M2**, r1) và `:2869` (**M6**, r2)
— đúng hai nhánh dành cho *"con chết trước khi in được gì"*, tức đúng lúc `stderr` là chỗ **duy nhất**
còn nguyên nhân.

Vô hình trên Python 3.11 (`DeprecationWarning`, im lặng mặc định); hiện từ 3.12 (`SyntaxWarning`).
`.github/workflows/ci.yml` ghim `python-version: "3.12"` (dòng 93, 626, 685); runner chạy **3.12.14**;
job `gate-registry` của PR #590 có **259** dòng `SyntaxWarning`, trong đó **152** thuộc
`nhanh_don_duoc_test.py` và các bản sao đột biến của nó.

**Phản chứng chạy được** — bản sao tạm, tiêm lỗi mức module, tiến trình thật, đưa `stderr` thật
qua đúng `_goi_chan_doan`:

```
python3.11   rc=1 · stdout=0B · stderr=256B  →  "… | NameError: name 'NGUYEN_NHAN_THAT_KHONG_TON_TAI'…"  → CÓ nguyên nhân
python3.12   rc=1 · stdout=0B · stderr=698B  →  "…:2215: SyntaxWarning: invalid escape sequence '\d' | …"  → KHÔNG
```

**A8 của r2 ĐẠT trong test nhưng SAI ngoài đời.** `r525` giả lập `run` trả `stderr` ngắn nên chuỗi
mốc lọt; `stderr` thật có 425 ký tự cảnh báo đứng trước.

**Đây là khuyết tật NGỦ.** Trên các lượt xanh, số dòng `    stderr: ` in ra là **0** ở cả log CI #590
lẫn cả 13 tệp `.out.txt` của chủ kho. Nó chỉ nổ đúng lúc có sự cố.

## §4 — Mục tiêu

| | |
|---|---|
| **M7** | Hai docstring thành raw (`r"""`). Mô-đun biên dịch với **0** cảnh báo escape-sequence dưới Python ≥3.12 |
| **M8** | Chốt KHOÁ: một ca tự kiểm dựng lại phép đo ấy trên **chính tệp mã nguồn** (`Path(__file__)`), không phải trên một hằng chép tay |
| **M9** | Sửa kích thích của `r525`: `stderr` giả lập phải **dài hơn `TRAN_CHAN_DOAN`** và mang nguyên nhân ở **cuối**, đúng hình dạng thật |

## §5 — Nghiệm thu

| | tiêu chí | đột biến phải giết |
|---|---|---|
| **A13** | `compile()` trên `ops/nhanh_don_duoc_test.py` dưới Python ≥3.12 ⇒ **0** cảnh báo escape-sequence. Khai bằng hai số bằng nhau (`0 == 0`), KHÔNG đọc `rc` | Đổi một `r"""` về `"""` ⇒ ca ĐỎ |
| **A14** | Ca M8 đọc **tệp thật** qua `Path(__file__)`. Đột biến trỏ nguồn đọc sang chuỗi rỗng ⇒ ca ĐỎ | Thay nguồn đọc ⇒ ca ĐỎ |
| **A15** | `r525` với `stderr` dài `> TRAN_CHAN_DOAN` và nguyên nhân ở **cuối**: ca phải khai **đúng** rằng dòng cha KHÔNG chứa nguyên nhân với `TRAN_CHAN_DOAN` hiện tại — **không** được khai ĐẠT | Nới `TRAN_CHAN_DOAN` mà không đổi hướng cắt ⇒ ca ĐỎ |
| **A16** | Phân hạng **không đổi**: cặp `(giet, hong)` bằng đúng cặp của r2 trên cùng bảng đầu vào có đủ bốn nhãn | Đổi một nhánh phân hạng ⇒ cặp lệch |
| **A17** | Ca mới nằm trong `NHOM_BAT_BUOC`, có **đột biến riêng**, `SAN_NHOM` cập nhật | Bỏ đột biến của ca mới ⇒ `thieu` khác rỗng ⇒ suite ĐỎ |
| **A18** | Toàn bộ `ops/nhanh_don_duoc_test.py` ⇒ `rc=0`, `TU KIEM N/N` **hai số bằng nhau**, `dot bien giet M/M` **hai số bằng nhau** | Bất kỳ ca nào đỏ |
| **A19** | Delta so nền `45ea292`: nền đã đo `rc=0 · 82/82`; ứng viên phải `rc=0` và `dot bien giet = 82 + (số đột biến mới)`, hai vế dựng trong **MỘT** lệnh | Hai vế dựng ở hai thời điểm ⇒ phép đo vô hiệu, **không phải** ĐẠT |

**Lưu ý gắn vào A15.** Hướng cắt của `_goi_chan_doan` (cắt từ đầu) là câu hỏi **thiết kế còn mở** và
**KHÔNG thuộc closure r3**. Sửa nó — cắt từ giữa, ưu tiên đuôi, hay lọc cảnh báo khỏi `stderr` —
là **mở rộng phạm vi**. r3 chỉ **khoá hành vi hiện tại thành một lời khai trung thực**, để không ai
đọc "M2/M6 chuyển tiếp được chẩn đoán" thành một lời hứa vô điều kiện.

## §6 — `ngoai_pham_vi`

- `CASE T6` (`OSError: [Errno 39] Directory not empty`) — nợ mở, chưa có chủ
- Nguyên nhân (A) của `r506` — nợ mở, chưa có chủ
- `entropy-giu-mot-byte` làm suite ĐỎ ~1/256 lượt — nợ mở, chưa có chủ
- Đổi hướng cắt hoặc giá trị `TRAN_CHAN_DOAN` — xem lưu ý A15
- **Bốn điểm cảnh báo còn lại của kho** — xem §7
- Mọi tệp ngoài `write_set`, kể cả sửa tạm rồi hoàn nguyên

## §7 — `write_set` MỘT ĐƯỜNG, và vì sao KHÔNG gộp

```yaml
write_set:
  - ops/nhanh_don_duoc_test.py
```

Chủ kho ban đầu chỉ thị **"gộp"**. Executor đo rồi khai vật cản, chủ kho chốt lại **"Hình A"**.
Ghi cả hai lượt để không ai đọc §7 này thành executor tự thu hẹp.

Quét toàn kho tại `origin/master` bằng Python 3.12, đếm **ĐIỂM** (site) chứ không đếm dòng log:

```
  2  ops/lease_publish_test.py                                     (2220 '\s' · 4178 '\d')
  1  .claude/dev/packet_loop_test.py
  1  ops/reviews/goi-va-lease-hoi-toan-kho-1/lease_publish_test.py
  1  ops/reviews/goi-va-lease-hoi-toan-kho-2/lease_publish_test.py
  0  ops/nhanh_don_duoc_test.py        ← master sạch; r1 chưa land
  0  ops/lease_publish.py
```

5 điểm có sẵn + 2 điểm #568 thêm = 7 điểm / 5 tệp.

Đo `ai-dang-giu` lúc 2026-09-21T04:2xZ, đọc `rc` trực tiếp:

```
ops/nhanh_don_duoc_test.py                                     rc=11  NGƯỜI_GIỮ 1: chan-doan-tin-dung-gia-r2-g1-claude
ops/lease_publish_test.py                                      rc=11  NGƯỜI_GIỮ 2: dang-lease-dau-truoc-kiem-sau-r1-g1-claude (#579, tới 19:48Z)
                                                                                    windows-fixture-posix-r1-g1-claude      (#578, tới 10:30Z)
.claude/dev/packet_loop_test.py                                rc=0   NGƯỜI_GIỮ 0
ops/reviews/goi-va-lease-hoi-toan-kho-1/lease_publish_test.py  rc=0   NGƯỜI_GIỮ 0
ops/reviews/goi-va-lease-hoi-toan-kho-2/lease_publish_test.py  rc=0   NGƯỜI_GIỮ 0
```

Hai lý do gộp không đi được:
1. `ops/lease_publish_test.py` có **hai người giữ khác**. Lease r3 hết hạn trước `#579` (19:48Z).
2. 5 tệp > trần **≤ 3 tệp** của `ADR-0044:5` cho class `sensitive`.

Bốn điểm còn lại chuyển sang một packet vệ sinh riêng. **Chúng KHÔNG có răng**: không tệp nào
trong số đó có nhánh chẩn đoán bị cảnh báo ăn mất ngân sách — đó là lý do tách được mà không
bỏ sót thứ gì đang chảy máu.

## §8 — `hinh_dang_ke_thua`

| hình dạng | r2 | **r3** | vì sao nâng |
|---|---|---|---|
| `LOI-KHAI-RONG-HON-PHEP-DO` | 3 | **4** | r1 khai "chẩn đoán của con được chuyển tiếp" trong khi chỉ đo trên Python 3.11, nơi khuyết tật vô hình |
| `TIN-HIEU-DO-CHINH-MA-TEST-GIA-MAO` | 2 | **3** | `r525` xanh nhờ kích thích (`stderr` giả lập ngắn) hẹp hơn hiện thực |
| `VA-DUNG-CHO-DUOC-CHI-ROI-BO-SOT-DUONG-THU-BA` | 2 | 2 | không tái phát ở lượt này |

Cả hai hình dạng được nâng đều **đã vượt ngưỡng "lần thứ ba ⇒ DỪNG và hỏi"**. Executor đã dừng
và hỏi trước khi chạm tệp; r3 tồn tại là **kết quả** của lần dừng ấy, không phải một lần tự đi tiếp.

**Cơ hội tái phát đã biết, cho chính r3:** A13 đo "0 cảnh báo" bằng `compile()` trong tiến trình
đang chạy. Nếu ca ấy đọc một **bản chép** thay vì tệp thật, nó sẽ xanh trong khi tệp thật bẩn —
đúng hình dạng `TIN-HIEU-DO-CHINH-MA-TEST-GIA-MAO` lần thứ tư. A14 tồn tại để chặn đúng chỗ đó,
và phải có đột biến riêng chứng minh nó chặn được.
