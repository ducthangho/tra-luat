# WP541 — PHÉP ĐO TRÊN WINDOWS THẬT của chủ kho (18-09-2026)

| | |
|---|---|
| nền | Windows, Python **3.13.1**, git **2.55.0.windows.5** (`C:\Program Files\Git\cmd\git.exe`) |
| quyền | **Administrator: CÓ** · tạo symlink được: **CÓ** |
| cây đo | clone riêng `D:\…\tl541-do`, `HEAD = 2f70869` (bản vá `fix_issue_541`), `core.abbrev=7` |
| bộ đo | `ops/reviews/wp541-do-n7-windows.py`, sha256 `0413b5b2…c24572d` |
| kết quả | `rc=0` — **mọi chốt đạt** |

Đây là phép đo Windows thật ĐẦU TIÊN của packet này. Trước đó mọi kết luận về Windows
đều suy từ log CI hoặc từ đọc mã; #548 đã gỡ Windows khỏi cổng master, nên không có
đường nào khác để đo.

## 1. Nghiệm thu THẬT (N1–N4) — ĐẠT

`t165` `t166` `t167` `t168` — **QUA cả bốn**. Đây là tiêu chí nghiệm thu duy nhất mà
spec r2 công nhận (§nghiem_thu, N0: *"14 ca PATH KHÔNG phải tiêu chí nghiệm thu… Tiêu
chí thật là N1–N4"*).

## 2. N7 — đột biến GIẾT ĐÚNG LÝ DO

```
TRUOC (chua dot bien) = 1   [mong 1]
SAU  (da dot bien)    = 0   [mong 0]
t165 : DO | Chan: KHÔNG_XÁC_ĐỊNH: không thấy `git` trong PATH tối thiểu
```

Tắt nhánh `if nen_thuc == "windows":` ⇒ `t165` rơi xuống đường POSIX và chết **đúng
bằng lỗi hằng số cũ**. Không phải tín dụng giả: lý do nguyên văn trỏ thẳng vào thứ
đang đo. Đột biến chạy trên **bản sao tạm**; cây thật không bị đụng tới.

## 3. Giải đường dẫn trên nền thật — đo HAI CHIỀU

```
_git_exe_toi_thieu()          -> 'C:\Program Files\Git\cmd\git.exe'
shim-only o PATH ngoai cwd    -> None          (mong None)
DOI CHUNG DUONG: them git.exe -> '…\shim\git.exe'
```

Chiều âm (từ chối `git.bat`/`git.cmd`/`git.py`) và chiều dương (thêm `git.exe` thì
tìm ra) đều đo được. Không có chiều dương thì "luôn trả None" cũng qua được chiều âm.

Ghi chú: `shutil.which("git")` trả `…\git.EXE` (hoa) còn bản vá trả `…\git.exe`
(thường) — vì bước 2 **dựng đường ứng viên tường minh** thay vì hỏi PATHEXT. Đó là
điểm mạnh, không phải lệch.

## 4. Bức tranh đỏ ĐẦY ĐỦ — 11 ca, số học tự khớp

`143/154 đạt`, bỏ qua 7. Đối chiếu: `154 − 143 = 11`, bộ đọc lấy được **11**;
`liet_ke_day_du: true`.

**15 ca từng đỏ trên CI: nay 11 XANH, 4 còn đỏ.** Bốn ca ấy đã đọc mã từng ca, và
**không ca nào** còn mang chữ ký PATH:

| ca | nguyên nhân ĐÃ ĐỌC MÃ | thuộc #541? |
|---|---|---|
| `t131` | chạy thẳng một fixture `.sh` ⇒ `WinError 193 %1 is not a valid Win32 application` | KHÔNG — fixture chỉ-POSIX |
| `t132` | `WinError 5 Access is denied` khi dọn `…\.git\objects\36\c0fe…` (object của git là chỉ-đọc trên Windows) | KHÔNG — dọn dẹp fixture |
| `t136` | xem §5 — **rc ĐÚNG (12), LÝ DO SAI** | KHÔNG — hằng đường dẫn chỉ-POSIX trong fixture |
| `t150` | packet **#552**, `rc=12` đúng nhưng đầu ra lệch | KHÔNG — đã tách packet riêng |

Bảy ca đỏ còn lại (`t35`–`t40`, `t125`) chưa từng nằm trong 15 ca đích, và thân hàm
của **cả bảy giống hệt `origin/master`** (đối chiếu băm từng thân hàm) — bản vá không
đụng tới chúng.

- `t35`–`t40`: `rc=127` + `/bin/bash: D:\Quốc hội\…\ops\cai_actionlint.sh: No such
  file or directory` + `cygpath: command not found`. Chữ ký này **khớp bash của WSL**
  chứ không phải Git-Bash (Git-Bash CÓ `cygpath` và hiểu đường dẫn ổ đĩa). Đây là
  **giả thuyết**, chưa đo: cần chạy `where bash` trên máy ấy mới kết luận được.
- `t125`: chính ca đó tự khai `LỆCH_CHƯA_RÕ_NGUYÊN_NHÂN` và **từ chối kết luận** —
  hai lượt A/B toàn suite cho `143/154` và `144/154`, ca lệch là `t156`. Chập chờn
  hoặc phụ thuộc thứ tự/tải, chưa ai biết. Ca này nằm trong vùng chồng lấn đã khai
  với lease `ci-windows-r2-g2-antigravity`.

## 5. `t136` — ĐÍNH CHÍNH MỘT LỜI KHAI CỦA CHÍNH SPEC r2

Bảng §hien_trang của spec r2 ghi `t136 | PATH | Chan: … PATH tối thiểu /usr/bin:/bin`.
Đó là **lý do TRỰC TIẾP đọc từ log**, và nó đúng — nhưng bảng ấy trình bày nó như
**nguyên nhân DUY NHẤT**. Không phải. Lỗi PATH **che** một lỗi thứ hai:

```python
# ca đòi rc=12 KÈM LÝ DO "không khớp executable"
rc, td = _ma_chan(mod, mod.kham_pha_nguon, ep,
                  hoso=dict(hoso, git_path="/khong/co/git"), …)
chot(rc == 12 and "không khớp executable" in td, …)
```

Hằng `"/khong/co/git"` là đường dẫn **chỉ-POSIX**. Đo được:

```
POSIX    is_absolute("/khong/co/git") = True
WINDOWS  is_absolute("/khong/co/git") = False
```

Nên trên Windows, `kiem_mien_ho_so` bắn TRƯỚC với *"git_path phải là đường tuyệt
đối"*, và ca chết vì **lý do sai** dù `rc` đúng. Đúng kỷ luật *"giết đúng lý do"* mà
kho này đã trả giá để học — lần này nó bắt được một ca thật.

Thân hàm `t136` **giống hệt `origin/master`**: bản vá không gây ra, cũng không che.
Nó nằm TRONG write set (`ops/lease_publish_test.py`) nên sửa được trong #541, nhưng
**đó là quyết định của người giữ**, không phải của reviewer: spec đã đóng băng bằng
`spec_hash`, nới phạm vi là phải ra revision mới.

## 6. Ba ca xanh thêm nhờ quyền Administrator

Lượt trước (không quyền) `141/154`; lượt này `143/154`. Trong 15 ca đích, `t133`
`t139` `t151` chuyển từ ĐỎ sang QUA. Đúng như dự đoán ở lượt trước: chúng đỏ vì
**thiếu quyền tạo symlink**, không vì bản vá. `symlink_duoc: true` đo thẳng bằng
`os.symlink`, không suy từ lỗi của ca test.

## 7. P3 MỚI — chẩn đoán N3b ghi ra stderr VÔ ĐIỀU KIỆN

`ops/lease_publish.py` (bản vá):

```python
if chan_doan is not None:
    chan_doan.append(thong_bao_pf)
sys.stderr.write(thong_bao_pf + "\n")   # <- vô điều kiện
```

Người gọi truyền `chan_doan=` đã tuyên bố *"tôi sẽ thu chẩn đoán"*, nên lần ghi
stderr kia là thừa. Không phải lỗi đúng-sai, nhưng **đã trả giá thật**: một lượt đo
trên máy chủ kho chết giữa chừng vì đúng 72 byte ấy — Windows PowerShell 5.1 với
`2>&1` + `$ErrorActionPreference='Stop'` biến mọi dòng stderr của tiến trình con
thành lỗi chí mạng. Bộ test đầy đủ chạy xong mà N7 không bao giờ chạy.

Đề xuất (P3, không chặn): `if chan_doan is None: sys.stderr.write(...)`.

## 8. CHƯA ĐO ĐƯỢC — nói thẳng

1. **Nguyên nhân của `t35`–`t40`.** Chữ ký khớp WSL bash, nhưng chưa chạy `where bash`
   trên máy ấy. Tương quan, chưa phải nhân quả.
2. **`t125` chập chờn.** Chính ca đó từ chối kết luận; tôi cũng không kết luận.
3. **Hành vi của Windows PowerShell 5.1** ở §7: container review chỉ có pwsh 7.4.6,
   và trên 7.4.6 dòng stderr ấy KHÔNG chí mạng. Nguyên nhân suy từ thông điệp khớp
   nguyên văn + vị trí trap báo lỗi, cộng phép đo cho thấy dòng ấy có rò rỉ thật
   (72 byte → 0 byte sau khi bắt).
4. **Nền đo trên máy chủ kho.** Vẫn chưa có lượt chạy `origin/master` (chưa vá) trên
   chính máy ấy, nên câu *"7 ca kia đỏ sẵn"* dựa vào **đối chiếu băm thân hàm với
   master**, không dựa vào một lượt nền.
