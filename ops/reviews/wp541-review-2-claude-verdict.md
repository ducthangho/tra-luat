verdict: changes_requested
reviewed_sha: e60c757aa535

# CROSS-REVIEW LƯỢT 2 — packet #541 `WP541-PATH-TOI-THIEU-THEO-NEN` **r1 / gen 1**

| | |
|---|---|
| `reviewed_sha` | `e60c757aa535` (PR #554, nhánh `fix_issue_541`) — đo `07:2xZ 18-09-2026` |
| `base_sha` | `d705623162b7` — **đã hoà master**, `merge-base --is-ancestor` ⇒ **CÓ** |
| lease | `wp541-path-r1-g1-antigravity`, `spec_hash fc6e814d…` |
| lượt trước | `2170a4a4ce93` → `changes_requested` (3 P1 · 3 P2 · 4 P3) |
| kết luận | **`changes_requested`** — **1 LỚP P1** · **1 LỚP P2** · 0 P3 mở |
| assurance | **`advisory_review`** — trần cứng, xem cuối tệp |

## ĐỌC CHECK RUN TRƯỚC — VÀ LƯỢT NÀY NÓ XANH THẬT

Nợ `REVIEW-KHONG-DOC-CHECK-RUN`: đọc `get_check_runs` trước mọi việc khác.

| check run | kết luận |
|---|---|
| `chuan-bi` | **success** |
| `gate (ubuntu-latest)` | **success** |
| `gate-registry (ubuntu-latest)` | **success** |
| `gate-packet-loop (ubuntu-latest)` | **success** |
| `thu-hoi` | **success** |

Run `35297254635` / `35297253065`. Khác hẳn lượt 1, nơi `gate` **chưa từng chạy** và `thu-hoi` đỏ.

## ĐỐI CHIẾU LƯỢT TRƯỚC — 8/9 LỚP ĐÓNG, ĐO TỪNG CÁI

| lớp lượt 1 | trạng thái | phép đo |
|---|---|---|
| `P1-1` `t168` ĐỎ | **ĐÃ VÁ THẬT** | `chmod(0o755)` ở `t165`/`t167`/`t168`; bộ đầy đủ **`161/161 đạt`**, `rc=0`, **0 ĐỎ** |
| `P1-2` bước 3 nhận `.bat`/`.py` | **VÁ SINH CƠ CHẾ MỚI — CÒN MỞ** | xem dưới |
| `P1-3` vi phạm `DIEU_KIEN_BAT_DAU` | **ĐÃ ĐÓNG** | ngoại lệ §5 của chủ kho, không do bản vá |
| `P2-1` nhánh khác tên | **ĐÃ ĐÓNG** | lease ghi `branch_thuc_te` (`fix_issue_541`), quyết định giữ tên |
| `P2-2` base lệch 8 commit | **ĐÃ VÁ THẬT** | hoà master; `thu-hoi` từ failure → **success** |
| `P2-3` `gate` chưa chạy | **ĐÃ ĐÓNG** | 5/5 check run success |
| `P3-1` bốn khối tautology | **ĐÃ VÁ THẬT** | `grep -c "def mutant_"` ⇒ **0** |
| `P3-2` thông điệp đấm cứng | **ĐÃ VÁ THẬT** | nay `f"… PATH tối thiểu {path_posix}"` |
| `P3-3` docstring mâu thuẫn · `P3-4` mã chết | **ĐÃ VÁ THẬT** | bước 3 nay thật sự gọi `shutil.which`; `grep -c ds_khao_sat` ⇒ **0** |

`N5` (delta ca đỏ so nền): nền `157/157` · head `161/161` = 157 + đúng 4 ca mới ⇒ **0 ca đỏ mới, ĐẠT**.
`N6`: **2 tệp, +239 / −4** so `d705623` ⇒ dưới trần 2 tệp / 300 dòng, **ĐẠT**, và lần này neo vào base THẬT.

## `P1-2` CÒN MỞ — VÀ ĐÂY LÀ ĐÍNH CHÍNH LỜI KHUYÊN CỦA CHÍNH TÔI

Bàn giao lượt 1 tôi đưa hai đường và **khuyên (A)**: *"dùng đúng `shutil.which("git", path=…)` ở bước 3"*. agy làm theo:

```python
cand = shutil.which(os.path.join(d, "git")) or shutil.which(os.path.join(d, "git.exe"))
if cand and hop_le(cand):
    return str(Path(cand).resolve())
```

**Lời khuyên ấy SAI, và nó sai theo cách tôi đáng lẽ phải đo trước khi đưa ra.** `shutil.which` trên Windows **luôn** kéo `PATHEXT` vào — nên `.bat`/`.cmd`/`.py` quay lại bằng cửa khác. Tệ hơn: hành vi **đổi theo phiên bản Python**, và kho ghim đúng bản có vấn đề.

**Đọc MÃ NGUỒN THẬT của từng bản** (`inspect.getsource(shutil.which)`):

| bản | nhánh khi `cmd` có thư mục |
|---|---|
| **3.11** | `if os.path.dirname(cmd): if _access_check(cmd): return cmd; return None` — **trả về sớm, KHÔNG chạm PATHEXT** |
| **3.12 / 3.13** | `dirname, cmd = os.path.split(cmd); if dirname: path = [dirname]` — **KHÔNG trả về sớm**, rơi xuống `if sys.platform == "win32"` ⇒ `files = [cmd] + [cmd + ext for ext in pathext]` |

**Phản chứng CHẠY ĐƯỢC** (mô phỏng: đặt `sys.platform = "win32"` trên Linux — xem phần giới hạn):

```
python 3.11.15 | thư mục chỉ có git.bat/git.cmd/git.py/git.exe => TỪ CHỐI cả bốn
python 3.12.3  | thư mục chỉ có git.bat  => CHẤP NHẬN -> git.bat
               | thư mục chỉ có git.cmd  => CHẤP NHẬN -> git.cmd
               | thư mục chỉ có git.py   => CHẤP NHẬN -> git.py
python 3.13.12 | y hệt 3.12
```

**`ci.yml` ghim `python-version: "3.12"`** (ba chỗ: dòng 93, 626, 685 trên `d705623`). Tức nền CI **đúng là nền có lỗ**.

Và `hop_le(cand)` không cứu được: nó chỉ kiểm *là tệp* · *không dưới `%SystemRoot%`* · *không trong cwd*. Một `git.bat` ở thư mục PATH bình thường qua cả ba.

⇒ **Kết luận đúng, và nó khác lời khuyên lượt 1 của tôi:** nếu ý định là *chỉ nhận `.exe`* thì **`shutil.which` là công cụ SAI** — mọi cách gọi nó trên Windows đều mở PATHEXT. Phải kiểm `git.exe` **tường minh**, ví dụ:

```python
for d in ds_thu_muc:
    if trong_cwd(d) or duoi_system_root(d):
        continue
    cand = Path(d) / "git.exe"          # TƯỜNG MINH, không qua PATHEXT
    if hop_le(cand):
        return str(cand.resolve())
```

**Nếu ngược lại, chấp nhận `.bat`/`.cmd` là CÓ CHỦ ĐÍCH** (vài bản Git bọc bằng shim), thì phải **khai thẳng** điều đó trong docstring và trong đặc tả, kèm lý do vì sao `N2` chỉ chặn ở cwd mà không chặn ở PATH. Tôi không quyết hộ — nhưng **im lặng thì không được**, vì hiện docstring vẫn hứa *"`shutil.which("git")` trên PATH thật"* mà không nói PATHEXT mở tới đâu.

### Giới hạn của phép đo này — khai, không lấp

Phép chạy trên là **MÔ PHỎNG**: `sys.platform` bị đặt thành `"win32"` trên Linux. Đó **không phải** Windows thật. Thứ nó chứng minh là **nhánh mã nào được chạy**, và nó **khớp** với phép đọc mã nguồn — hai đường độc lập cùng chỉ một chỗ. Hành vi trên Windows thật (gồm việc `subprocess.run([git.bat, …])` có spawn được không) vẫn **KHÔNG ĐO ĐƯỢC** từ đây.

**Rig của tôi hở HAI lần trước khi đo đúng, và cả hai đều suýt thành phát hiện giả ngược chiều** — lần đầu mọi ca trả `None` vì `PATHEXT` viết HOA (`git.EXE`) không khớp tệp `git.exe` trên hệ tệp phân biệt hoa thường; lần hai vẫn `None` vì `PATHEXT` tách bằng `os.pathsep`, trên Linux là `:` chứ không phải `;`. Nếu dừng ở một trong hai lần ấy tôi đã kết luận *"đã vá xong"*. Ghi ra vì đó đúng bài học *"bộ quét nháp của chính mình là thứ dễ tin nhất nên nguy nhất"*.

## `P2-MỚI` — CA BẮT BUỘC CỦA BÀN GIAO KHÔNG ĐƯỢC THI CÔNG

Bàn giao lượt 1 đòi, nguyên văn:

> **Chốt bắt buộc kèm theo:** thêm **một ca** (hoặc mở rộng `t166`) đo đúng điều này — `git.bat` ở một thư mục PATH **không phải cwd** phải bị **từ chối**.

Đo: số ca test **+4** (master 157 → head 161), đúng bằng `t165`–`t168` — **không ca thứ năm nào**. Và `t166` hiện chỉ chạy một hình dạng:

```python
kq = lp._git_windows(path=str(cwd_fake), program_files=str(pf_rong), cwd=str(cwd_fake))
```

`path` **bằng** `cwd` ⇒ nó chỉ đo cửa cwd. **Không** ca nào đặt `git.bat` vào một thư mục PATH khác cwd.

**Kèm một cảnh báo cho vòng sau, kẻo ca mới sinh ra vô nghĩa:** trên `ubuntu-latest`, `sys.platform != "win32"` nên `shutil.which` **không** chạm PATHEXT — một ca viết thẳng sẽ **XANH VÔ ĐIỀU KIỆN** mà chẳng đo gì, đúng hình dạng *"ca có MẶT khác ca có ĐO"*. Ca ấy phải **tiêm nền** (như `nen="windows"` đã làm) **và** tiêm `PATHEXT` + đặt `sys.platform`, hoặc khai thẳng là **KHÔNG ĐO ĐƯỢC** trên Linux.

## BẢNG ĐO ĐẦY ĐỦ — KỂ CẢ CÁI KHỚP

| phép đo | kết quả |
|---|---|
| head trôi trong lúc review? | **không** — `e60c757aa535` ở cả hai lần đo |
| `write_set` | **đúng 2** đường ✔ |
| bộ test đầy đủ | **`161/161 đạt`**, `rc=0`, bỏ qua **0**, **0 ĐỎ** ✔ |
| `N5` delta ca đỏ so nền | **0 ca đỏ mới** ✔ (nền `157/157`) |
| `N6` numstat so base THẬT | **2 tệp, +239 / −4** ✔ |
| `thu-hoi` | **success** ✔ (lượt 1: failure) |
| `gate` + hai job phụ | **success cả ba** ✔ (lượt 1: chưa từng chạy) |
| hàm `mutant_` cục bộ còn lại | **0** ✔ |
| `ds_khao_sat` (mã chết) | **0** ✔ |
| thông điệp `Chan` nội suy `path_posix` | **CÓ** ✔ |
| `shutil.which` + PATHEXT trên py≥3.12 | **nhận `.bat`/`.cmd`/`.py`** ✘ — `P1-2` |
| ca đo `git.bat` ở PATH ngoài cwd | **KHÔNG CÓ** ✘ — `P2-MỚI` |

## `KHÔNG ĐO ĐƯỢC` — khai, không lấp

1. **Hành vi trên Windows thật.** Cả `P1-2` lẫn hệ quả spawn `.bat`/`.py` đều dựa trên đọc mã + mô phỏng `sys.platform`. Không có Windows ở đây.
2. **`N7`** (*"Trước = 1, Sau = 0"*) — lượt 1 đã hỏi hai con số ấy **đếm gì** (luật `L1`); chưa thấy trả lời trong bản vá hay thân PR. Vẫn `KHÔNG ĐO ĐƯỢC`.
3. **`gate (windows-latest)`** — không chạy, và theo ràng buộc `manual_ci_budget: 0` thì sẽ không chạy. Packet sửa đường Windows mà không được chạy Windows để nghiệm thu; nghịch lý này đặc tả đã khai và chọn sống chung.

## KHAI XUNG ĐỘT LỢI ÍCH

Phiên này **không** soạn đặc tả r2 của #541. Nhưng lượt này **KHÔNG độc lập về hình dạng `P1-2`**: bản vá `P1-2` được viết **theo đúng lời khuyên (A) của tôi ở lượt 1**, nên phán quyết rằng nó chưa đủ là tôi đang chấm **hậu quả lời khuyên của chính mình**. Điều đó không làm phép đo sai — bằng chứng là mã nguồn `shutil.which` và hai lượt chạy — nhưng nó có nghĩa: **khuyết tật này là của reviewer trước, không phải của executor.** agy làm đúng thứ được bảo.

Và như lượt 1: phiên này ghi hộ lease `ci-windows-r2-g2-antigravity`, cái lease sinh ra `P1-3` — nay đã đóng bằng ngoại lệ chủ kho.

## ASSURANCE — trần cứng

**`advisory_review`**. Lease khai `assurance_target: human_audited`, `reviewer_provider: human`; phiên này là một phiên `claude`, không phải người audit theo §8. Không có `session_run_id`. `antigravity` vẫn 0 lần trong `docs/PROTOCOL_DA_PHIEN.md`; việc ấy thuộc packet riêng #551.

## NGUỒN CÓ THẨM QUYỀN

Tệp này trong kho, có băm. Bản đăng trên GitHub chỉ là **bản chiếu**.
Verdict lượt 1 (`eb73292a…`) giữ nguyên trên đĩa; lượt này **không** rút điều gì của nó — tám trong chín lớp đã đóng, lớp còn lại đổi cơ chế chứ không biến mất.
