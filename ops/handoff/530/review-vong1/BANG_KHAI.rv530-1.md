# Bảng LỜI KHAI của phiên thi công — mọi con số tôi đã công bố, để reviewer ĐO LẠI

> **Bảng này CHẮC CHẮN THIẾU.** Nó do tôi tự liệt kê, cộng `trich_so.py` (bộ lọc theo một **danh
> sách đơn vị đoán trước**). Ở PR #250 đúng kiểu bộ lọc này bỏ sót bốn con số vì chúng **không mang
> đơn vị nào**. Nên: **mỗi con số bạn tìm ra mà bảng này bỏ sót được TÍNH LÀ MỘT FINDING.**

Nguồn của các lời khai: thân PR **#532**, comment **#530 `5647445521`**, hai thông điệp commit
`540b6f1` và `a1c7d7f`, và `ops/handoff/530/TRANG_THAI.md` trên nhánh `ops/handoff-530`.

| # | lời khai | giá trị khai | đo lại bằng |
|---|---|---|---|
| 1 | `bang()`→`chot()` trong 9 ca `#504` | **59** (t125 3 · t153 5 · t154 10 · t155 4 · t156 11 · t157 6 · t158 7 · t159 4 · t160 9) | đếm trên hai blob `dc02c9b` và `a1c7d7f` |
| 2 | `bang()` còn lại trong 9 ca sau khi đổi | **0** | như trên |
| 3 | A1 — control đúng phân hạng | **10/10**, `rc=0` | `--chi-ca=t162` |
| 4 | A1 — bộ đo CŨ (`ops/handoff/512-luot7/dotbien512.py`, nhánh `ops/handoff-512-luot7`) | **7/10**, `rc=1` | không có trong cây `a1c7d7f`; nhánh ấy có trong gương |
| 5 | A1 — lượt chạy ĐẦU trước khi có phép cắt bảng | **8/10** (2 control ĐỎ vì `neo khớp 3 lần` / `2 lần`) | log trong hồ sơ; tái lập bằng cách gỡ `_dot_bien_nguon_512` |
| 6 | A4 — catalogue | mẫu số **16** · giết **16** · không giết **0** · KHÔNG ĐO ĐƯỢC **0** | `--chi-ca=t161` |
| 7 | A4 — trước khi vá thừa kế kênh | giết **15**, KHÔNG ĐO ĐƯỢC **1** | tái lập bằng cách gỡ vòng `os.environ.pop` trong `_mo_kenh` |
| 8 | A3+A8+A2 — tự kiểm bộ chấm | **7/7** (6 mục `DO` + 1 mục `XANH`) | `--chi-ca=t163` |
| 9 | A3 — trước khi ghim cột cho neo `except` | **5/6** | tái lập bằng cách bỏ `\n` dẫn đầu của neo |
| 10 | A2 chiều NGƯỢC | mục A2 → `XANH_SAI`, `rc=[1,1]`, `t163` ĐỎ | bơm một nhánh ĐỌC `chi_tiet` vào `_doc_kenh_xac_thuc` |
| 11 | A5 — wrapper | **158/158** đạt, bỏ qua **0**, đúng **3** dòng tổng kết, **0** dòng `^  ĐỎ  `, `rc=0` | `AL_VER=1.7.7 AL_GOI=... bash ops/chay_lease_publish_test.sh` |
| 12 | số ca: nền → sau | **155** → **158** | `grep -c '^<<< ra '` hai vế |
| 13 | A6 | `doctrine-scan` `rc=0` (**7** tệp, **0** chỗ chép) · `adr-song` `rc=0` (**48/48**) | `packet_loop.py` |
| 14 | A7 numstat | **1** tệp, **+802 / −61** | `git diff --numstat dc02c9b -- ops/lease_publish_test.py` |
| 15 | phân rã dòng THÊM | chú thích **148** · trống **67** · docstring **~90** (đo thô) · MÃ THUẦN **~497** | `git diff -U0` + phân loại |
| 16 | trần `S2` | cũ **300** (`ADR-0044`) → mới **1000**; **dư 198** | lease `…exec-1r2…` |
| 17 | trần `S6` | cũ **2** (`ADR-0043`) → mới **10**; đã dùng **0** | như trên |
| 18 | delta chi phí | nền **104,4s**/155 ca → sau **319,4s**/158 ca ⇒ **+214,9s**, **×3,06** | `do-delta-chi-phi-hai-ve.sh` trên nhánh `ops/handoff-530` |
| 19 | `t125` | **53,0s** → **160,4s** ⇒ **+107,4s** | như trên |
| 20 | thời lượng ba ca mới | `t161` **49,4s** · `t162` **2,2s** · `t163` **53,7s** | lượt CHA của wrapper |
| 21 | chốt fail-close CHƯA có control phân biệt | **9** | `CHOT_CHUA_CO_CONTROL_512` |
| 22 | hai điểm vật hoá `dich` | bộ **TƯƠNG ĐƯƠNG**, không phải 2 chốt độc lập: gỡ riêng nửa nào cũng `rc=0` + **0** control lệch; gỡ cả hai ⇒ `rc=1`, `GIET → KHONG_GIET` | gỡ từng nửa rồi chạy `t162` |
| 23 | cổng đọc `nang_tran` / canh trần vòng | **0** dòng trong `ops/lease_publish.py`, **0** dòng trong `.claude/dev/packet_loop.py` | `grep -nE` |
| 24 | số ref so hai nguồn lúc cấp `r2` | **365/365**, `comm` RỖNG hai chiều | `ls-remote` so `for-each-ref` |
| 25 | `mẫu số 493` lời gọi `bang()`/`chot()` (khai ở spec rev 3) | **493** trên blob `13a2af8c…` của `36f68c7` | blob ấy có trong gương |

## Điều kiện đo — một con số không ghi điều kiện thì sẽ trôi mà không ai biết

- `shellcheck` **CÓ MẶT** (`0.9.0`) và `actionlint` **1.7.7** ghim trên PATH. **Thiếu `shellcheck` thì
  `t137`/`t159` fail-close `KHÔNG ĐO ĐƯỢC`** và bạn sẽ thấy một "hồi quy" không tồn tại. Hai nhị phân
  nằm ở `cong-cu/`, cộng gói offline `cong-cu/actionlint-1.7.7-goi.gz` cho `AL_GOI`.
- Mọi số ở trên đo trên Linux. **`full CI` và `CI Windows` CHƯA TỒN TẠI cho mã này** — chúng chỉ chạy
  khi merge. Mọi kết luận về Windows đứng ở `KHÔNG ĐO ĐƯỢC`; đừng đọc `158/158` thành một kết luận
  về Windows.
