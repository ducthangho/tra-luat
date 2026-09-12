# F6 — bộ đo đột biến cấp TÍN DỤNG GIẢ: nguyên nhân gốc, bản vá, và phần KHÔNG đóng được

**Hiện vật:** `ops/handoff/512-luot7/dotbien512.py` (bản đã vá) · `dotbien512_REGEX_CU.py` (phản chứng,
khác đúng MỘT dòng) · `tukiem-cu.txt` / `tukiem-moi.txt` (đầu ra hai chiều).

**Vì sao đi hồ sơ riêng:** `dotbien512.py` là **bộ đo**, không phải sản phẩm. Nó nằm ngoài write set
exact của lease (`ops/lease_publish_test.py` · `ops/chay_lease_publish_test.sh`), nên vá nó trong PR #512
là chạm đường thứ ba ⇒ điều kiện dừng `S1`. Reviewer vòng 6 nói thẳng: *"Sửa công cụ ngoài write set
bằng hồ sơ riêng; không lén đưa nó vào HINT."*

## Nguyên nhân gốc — đo, không đọc code

Dòng phân hạng cũ:

    vo_can = re.match(r"^[A-Za-z_][A-Za-z0-9_.]*(Error|Exception)\s*:", chi_tiet_do)

`main()` của bộ test in lý do ĐỎ theo HAI đường khác nhau:

| ngoại lệ | `main()` in |
|---|---|
| `AssertionError` (chốt của ca đích, qua `bang()`) | `str(ex)` — **không** tiền tố kiểu |
| mọi ngoại lệ khác | `f"{type(ex).__name__}: {ex}"` — **có** tiền tố kiểu |

Nên "có tiền tố `<Kiểu>Error:`/`<Kiểu>Exception:`" đúng là dấu của một ngoại lệ VÔ CAN. Lỗ: regex đòi
**ít nhất một ký tự** (`[A-Za-z_]` bắt buộc) TRƯỚC `Error|Exception`, nên hai dạng **TRẦN** không khớp:

| chuỗi | regex cũ | hệ quả |
|---|---|---|
| `Exception: CONTROL vo can…` | **KHÔNG khớp** | cấp `GIET THAT` — thể hiện reviewer vòng 6 khai |
| `Error: …` (lớp tên đúng bằng `Error`) | **KHÔNG khớp** | cấp `GIET THAT` — **thể hiện THỨ HAI, vòng 6 không khai** |
| `RuntimeError: …` · `ValueError: …` | khớp | loại đúng |

Hai thể hiện, **một lỗ gốc**: tiền tố bắt buộc. Đây đúng hình dạng *"vá đúng chỗ được chỉ rồi bỏ sót
đường thứ ba"* của `CLAUDE.md` — nên vá theo LỖ, không vá theo danh sách thể hiện reviewer liệt kê.

## Bản vá

Chuyển tiền tố thành **tuỳ chọn**: `^(?:[A-Za-z_][A-Za-z0-9_.]*)?(?:Error|Exception)\s*:`

Hướng sai còn lại là **fail-close**: một thông điệp chốt THẬT vô tình bắt đầu bằng `<Từ>Error:` sẽ bị xếp
`TIN DUNG GIA`, tức **làm catalog ĐỎ** chứ không cấp tín dụng khống.

## Răng — phản chứng HAI CHIỀU, chạy được

Bốn `CONTROL` mà ta **biết trước đáp án**, mỗi cái là một đột biến THẬT đi qua đúng đường catalog dùng
(không phải phép thử regex trên chuỗi bịa). Chạy: `python3 dotbien512.py <gốc-kho> --tu-kiem`.

| bản | kết quả | rc |
|---|---|---|
| `dotbien512_REGEX_CU.py` (khác đúng 1 dòng) | **2/4** — `Exception` TRẦN và `Error` TRẦN cùng ra `GIET THAT` | **1** |
| `dotbien512.py` (đã vá) | **4/4 đúng phân hạng** | **0** |

Ca thứ tư là ca **DƯƠNG** (`CTRL-chet-DUNG-chot-ca-dich`, mutant `M15`), cố ý có mặt: thiếu nó thì một
bản vá "cho mọi thứ là TIN DUNG GIA" cũng qua được ba ca âm — một chốt LUÔN ĐỎ cũng là chốt hỏng.

## KHÔNG ĐÓNG ĐƯỢC — khai thẳng, đây là phần còn nợ

Bộ đo chạy **ngoài tiến trình** và chỉ đọc **CHUỖI** trên stdout. Một dòng trong chính tệp test dạng

    except Exception as e: raise AssertionError(f"... {type(e).__name__}")

vẫn **giả được** tín hiệu "đã chết bằng chốt của ca đích" — đúng bài học `#355`/`#359` của `CLAUDE.md`,
nơi bộ phân hạng bị lừa bởi một dòng viết với ý định TỐT. Bản vá này thu hẹp lỗ, **không đóng** nó.

Đóng hẳn đòi tín hiệu là thứ **mã triển khai không giả được**: một LỚP NGOẠI LỆ RIÊNG có danh tính đi tới
được bộ đo. Kho đã có sẵn `TinHieuChotCa(AssertionError)` (`ops/lease_publish_test.py:4328`) nhưng:
- nó chỉ dùng cho khối `A0`/`t139`, các ca `#504` (`t125`/`t158`/`t160`) khẳng định bằng `bang()` trần;
- và **danh tính lớp chết ở `main()`**: nhánh `except AssertionError` in `str(ex)`, mất tên lớp.

Nên đóng hẳn = sửa `main()` phát một dấu riêng cho `TinHieuChotCa` ⇒ **thay đổi write set**
(`ops/lease_publish_test.py`) giữa lúc dự đoán vòng 7 là vòng chốt. **Đề xuất cho chủ kho, KHÔNG tự làm.**

Trạng thái đúng của F6 sau lượt này: **ĐÃ VÁ THẬT phần đo được, CÒN NỢ phần chống giả mạo tín hiệu** —
không phải "F6 đã đóng".
