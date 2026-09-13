# Bảng LỜI KHAI của phiên thi công — vòng 2, head `3f1cda1`

> **Bảng này CHẮC CHẮN THIẾU.** Vòng 1 chứng minh điều đó bằng số: bảng 25 dòng của tôi bỏ sót **39**
> đại lượng (`BO_SOT_SO.md` của lượt trước). **Mỗi con số bạn tìm ra mà bảng này bỏ sót vẫn được TÍNH
> LÀ MỘT FINDING**, và mỗi con số trong bảng mà bạn đo ra KHÁC cũng vậy.

Nguồn: thân PR #532, comment PR `5647635305` và `5648007043`, comment #530 `5647564991`, thông điệp
commit `d5e7e7d`, và `ops/handoff/530/**` trên nhánh `ops/handoff-530`.

| # | lời khai | giá trị | đo lại bằng |
|---|---|---|---|
| 1 | `numstat` so `dc02c9b` | **1** tệp, **+995 / −61** | `git diff --numstat` |
| 2 | trần `S2` / dư | **1000** / **5** dòng | lease `…exec-1r2…` |
| 3 | trần `S6` / đã dùng | **10** / **1** vòng (đếm TAY) | lease `…exec-1r2…` |
| 4 | wrapper `A5` | **159/159**, bỏ qua 0, **3** dòng, **0** dòng `^  ĐỎ  `, `rc=0` | `chay_lease_publish_test.sh` |
| 5 | số ca | `155` (nền `dc02c9b`) → **159** | `grep -c '^<<< ra '` |
| 6 | `t161` A4 | mẫu số **16** · giết **16** · không giết **0** · KDD **0** | `--chi-ca=t161` |
| 7 | `t162` A1 | **12/12** (10 đóng băng + **2** bổ sung) | `--chi-ca=t162` |
| 8 | `t163` M5 | **7/7** (6 `DO` + 1 `XANH`) | `--chi-ca=t163` |
| 9 | `t164` chốt bộ đọc | **13/13** đầu vào cho `KHONG_DO_DUOC` | `--chi-ca=t164` |
| 10 | chốt bộ đọc, phân hạng | **3** có đầu vào phân biệt · **4** bị chốt sau hấp thụ · **2** còn nợ tự kiểm | `CHOT_*_512`, `NO_CHUA_CO_TU_KIEM_512` |
| 11 | 7 chốt reviewer nêu, **trước** `t164` | **7/7 CHƯA AI CANH** (`t161` 16/16, `t162` 12/12, `t163` 7/7, `rc=0`) | `quet-7-chot-TRUOC-t164.log` |
| 12 | 7 chốt ấy, **sau** `t164` | **3/7** làm `t164` ĐỎ | `rang-t164-SAU.txt` |
| 13 | ba đột biến false-GREEN, trước → sau vá | `7/7 rc=0` → ĐỎ · `10/10 rc=0` → ĐỎ · `16/16 rc=0` → ĐỎ | hai tệp `do-lai-3-cua-*.txt` |
| 14 | bản vá ĐẦU của chính tôi cho `m5-…` | làm **4/7** mục `DO` ĐỎ (oracle bị chính mutant làm hỏng) | thông điệp `d5e7e7d` |
| 15 | `A6` | `doctrine-scan` `rc=0` (**7** tệp, **0** chỗ chép) · `adr-song` `rc=0` (**48/48**) | `packet_loop.py` |
| 16 | lượt review vòng 1 | `1801,441s` · `ma_thoat=0` · `stderr 677 628 B` · verdict `24 341 B` sha `4505cdce…` | `run.json`, `sha256sum` |
| 17 | vòng 1 | `0 P1 · 4 P2 · 2 P3 · 4 NỢ`; **39** đại lượng bị bỏ sót | `VERDICT.rv530-1.md` |
| 18 | `CONTROL_512` đóng băng | **10** (8 `KHONG_DO_DUOC` + 2 `GIET`) | bảng trong tệp |
| 19 | `CONTROL_BO_SUNG_512` | **2** | bảng trong tệp |
| 20 | `_VUNG_CAT_512` | **4** vùng cắt | bảng trong tệp |
| 21 | delta chi phí (head **cũ** `a1c7d7f`) | `104,4s`/155 → `319,4s`/158 ⇒ **+214,9s ×3,06**; `t125` **+107,4s** | `do-delta-chi-phi-hai-ve.sh` |
| 22 | `sys.executable` | **18** biểu thức, chỉ **5** là lệnh tự gọi | vòng 1 đo, tôi đã sửa văn |
| 23 | neo của 26 mục | **16** khớp 1 lần · **8** khớp 2 · **2** khớp 3 | vòng 1 đo, tôi đã sửa văn |
| 24 | kênh khi gỡ selector (`t155`) | **3** bản ghi ca (`t01`,`t01`,`t155`) + 4 đóng lượt; lượt con in `0/0` `rc=0` | vòng 1 đo, tôi đã sửa văn |

**Điều kiện đo:** `shellcheck 0.9.0` và `actionlint 1.7.7` — cả hai ở `cong-cu/`. Thiếu `shellcheck`
thì `t137`/`t159` fail-close `KHÔNG ĐO ĐƯỢC`. Mọi số đo trên Linux; **Windows và full CI CHƯA TỒN
TẠI** cho mã này (chỉ chạy khi merge) ⇒ `KHÔNG ĐO ĐƯỢC`.

## Đính chính so với bảng vòng 2 (lượt CHẾT GIỮA CHỪNG)

Vòng 2 trước chết lúc ~`19:09Z`, 8,5 phút sau khi phóng (phiên bị treo/khôi phục; `run.json`
vẫn ghi `dang_chay` vì launcher bị giết trước khi kịp ghi trạng thái kết thúc — **đo** bằng
`ps` rỗng, `os.kill(pid,0)` ⇒ `ProcessLookupError`, mtime cuối `19:08:56`). Nó KHÔNG phải một
vòng hoàn tất. Hai phát hiện nó kịp ghi là THẬT và **đã được vá** ở `3f1cda1`:

| câu khai cũ | sự thật đo được | trạng thái |
|---|---|---|
| `:7079` *"mẫu số mặc định vẫn là 10"* | `control 512: 12/12` | ĐÃ SỬA VĂN |
| `:7176` *"trần `S2` chỉ còn dư ~26 dòng"* | `numstat 995/61`, trần 1000 ⇒ dư **5** | ĐÃ BỎ số dư khỏi văn |

Hai NỢ nó nêu (mỏ neo blob của mẫu **493** sai OID; phân rã dòng thêm lịch sử lệch ±1–2) đều
**ngoài** write set và đã được khai làm đính chính, không sửa hiện vật lịch sử.
