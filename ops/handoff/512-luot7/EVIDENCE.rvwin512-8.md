# EVIDENCE — vòng review 8, PR #512 / packet #504

Mọi con số là **lời khai**. Việc của bạn là **ĐO LẠI**.

## Neo — head KHÔNG đổi kể từ vòng 7

| | |
|---|---|
| `reviewed_sha` | `36f68c7e95e0de1fcf8e2311db33a164816db20f` — **y hệt vòng 7** |
| base | `bb7013c7669da19304a8769e5b25f8c1f8951e9c` |
| write set (2 đường) | `ops/lease_publish_test.py` · `ops/chay_lease_publish_test.sh` — **không đổi một byte** kể từ vòng 7 |
| vòng | **8**; đã dùng 7/10 |

**Không có thay đổi nào trong PR giữa vòng 7 và vòng 8.** Vòng 7 kết `F2` và `F7` là **ĐÃ VÁ THẬT**, và
lớp P1 duy nhất còn mở (`F6`) nằm **ngoài write set**. Nên lượt này tập trung vào `F6` — nhưng bạn vẫn
phải tự kiểm rằng PR thật sự không đổi, đừng nhận lời khai ấy.

## Việc đã làm sau vòng 7 — tất cả NGOÀI write set

### F6.5 — đã vá bằng ĐẢO CHIỀU phép đo

Vòng 7 bắt: `raise StopIteration(...)` vẫn được cấp `GIET THAT`. Nguyên nhân: bản vá vòng 6 nới regex
cho tiền tố thành tuỳ chọn nhưng **vẫn đoán TÊN ngoại lệ** qua hậu tố `Error|Exception`.

Bản vá mới **thôi đoán tên**, đo **hình dạng `main()` thật sự in ra**. `main()` có đúng hai nhánh:
`except AssertionError` ⇒ `str(ex)` (chốt, không tiền tố) · `except Exception` ⇒
`f"{type(ex).__name__}: {ex}"` (vô can, có tiền tố). Nên `_DANG_VO_CAN` khớp
"**định danh Python (có thể có chấm) rồi `: `**" — phủ toàn bộ nhánh thứ hai.

Kèm `_kiem_hop_dong_main()`: **fail-close** nếu `main()` không còn in theo hai hình dạng ấy.

| phép đo tôi khai | kết quả |
|---|---|
| `dotbien512.py --tu-kiem` (7 control) | `7/7`, rc=0 |
| `dotbien512_VA_VONG6.py --tu-kiem` (cùng 7 control, khác **một dòng**) | `5/7`, rc=1 — ĐỎ ở `StopIteration` **và** lớp tự định nghĩa `Bung` |
| đổi hợp đồng in của `main()` trong cây giả lập | bộ đo TỰ CHẶN, rc=1 |
| `dotbien512.py` (catalogue 16) | `16/16 giết thật`, rc=0, **không ca nào đổi phân hạng** so lần đo trước |

**Tự khai giới hạn:** `CTRL-GeneratorExit` ra `TIN DUNG GIA` qua **đường khác** — `GeneratorExit` là
`BaseException` nên `main()` không bắt, không sinh dòng `ĐỎ`, và ca rơi vào nhánh `ĐỎ=[]`. Nó **không**
chứng minh `_DANG_VO_CAN`. Đừng đọc `7/7` thành bảy phép đo cho cùng một chốt — và nếu tôi viết mạnh hơn
thế ở đâu, đó là finding.

### F6.6 — đính chính, không sửa mã

Vòng 7 đúng: `EVIDENCE` vòng 7 nói cả hai log ở trong gói nhưng gói chỉ có một. Log `153/155` **có thật**;
lỗi ở khâu **đóng gói**. Lượt này `do-cua-tac-gia/` có **đủ 16** hiện vật của nhánh `ops/handoff-512-luot7`.

### N31 / N32 — hai lỗi số thật của tôi, đã đính chính bằng hồ sơ

- `N31`: tiêu đề commit `36f68c7` ghi *"5 mutant sống"* — đúng là **SÁU**.
- `N32`: *"dư 386"* sai — đúng là **dư 399** (`1500 − 1101`). `418` là dư của head **cũ** `353eae1`.

Không sửa lịch sử để giấu. Nếu bạn thấy chỗ nào còn mang số cũ mà chưa được điểm danh, đó là finding.

## CÔNG CỤ — lượt này bạn CHẠY ĐƯỢC full suite

Vòng 7 không chạy được (`installer rc=4`, sandbox không ra mạng). Nay có gói **offline**:

```
AL_VER=1.7.7 AL_GOI=<sandbox>/goi-offline/actionlint_1.7.7_linux_amd64.tar.gz \
  AL_DICH=<thư mục tạm trong sandbox>/actionlint \
  bash ops/chay_lease_publish_test.sh
```

sha256 của gói: `023070a287cd8cccd71515fedc843f1985bf96c436b7effaecce67290e7e0757` — installer **vẫn tự đối
chiếu** với băm ghim của nó, `AL_GOI` không phải đường bỏ qua kiểm tra.

`shellcheck` phải có, kẻo `t137`/`t159` ĐỎ với `KHÔNG ĐO ĐƯỢC` — đó là **fail-close đúng thiết kế**,
không phải hồi quy.

## KHÔNG ĐO ĐƯỢC — vẫn nguyên, đừng đọc thành ĐẠT

- **`A3`/`A4` Windows**: không lượt Windows nào chạy. Các mốc thời gian Windows trong docstring
  (`N07`, `N11`–`N15`, `N17`, `N18`, `N30` của vòng 7) **thiếu log nguồn trong kho** — nợ hồ sơ có thật,
  chưa chữa.
- **Chống giả mạo tín hiệu của catalogue**: bộ đo chạy ngoài tiến trình và đọc **chuỗi**, nên một
  `except` trong tệp test vẫn giả được tín hiệu. Đóng hẳn đòi `main()` phát dấu riêng cho một lớp tín
  hiệu ⇒ **thay đổi write set** ⇒ đề xuất chủ kho, chưa làm.
- **`S8-bo-deadline`**: gốc ngoài write set (`S3`).
- **`A5`**: `KHÔNG ĐẠT` — `1101 > 300`, override 1500 không đổi nhãn đóng băng.
- **Trạng thái GitHub trực tiếp**: `KHÔNG ĐO ĐƯỢC` từ sandbox.
