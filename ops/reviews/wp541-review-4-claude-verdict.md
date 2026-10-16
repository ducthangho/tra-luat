# Verdict lượt 4 — Packet #541 `WP541-PATH-TOI-THIEU-THEO-NEN` (r1/g1)

- **Kết luận:** `changes_requested` — **1 P1 · 1 P2 · 2 P3**
- **Neo `reviewed_sha`:** `2f70869a0537843e9cae78618ee7ae8c261d972d`
- **PR:** [#554](https://github.com/ducthangho/tra-luat/pull/554) · nhánh `fix_issue_541`
- **Lease:** `wp541-path-r1-g1-antigravity` (executor `agy`), hết hạn `2026-09-19T00:00:00Z`
- **Thời điểm đo:** `2026-09-18T15:21Z` (phép đo chạy `15:16Z`–`15:21Z`)

## 0. Lượt này ĐỨNG SAU một `approve` — nói rõ quan hệ

Lượt 3 (phiên khác, nhánh `claude/review-541-luot3-20260918`) đã ra **`approve`** trên đúng
`2f708690`, 0 P1 / 0 P2 / 2 P3. Lượt 4 **không lật** kết luận ấy ở phần nó đã đo: tôi **đo lại độc
lập** và xác nhận hai lớp của lượt 2 đóng thật. Các phát hiện dưới đây là **hướng lượt 3 không
săn**, không phải phản bác lượt 3.

Lượt này là một phiên `claude` chấm executor `agy`. Lease khai `assurance_target: human_audited`
và `reviewer_provider: human` ⇒ mức cao nhất lượt này mua được vẫn là **`advisory_review`**.

## 1. Bảng đo — kê CẢ cái khớp

Điểm khác lượt 1 và 2: lượt này gọi **THẲNG `_git_windows`** với `path=` / `cwd=` /
`program_files=` tiêm vào, nên đo được trên Linux **mà KHÔNG mô phỏng `sys.platform`**. Lượt 1–2
phải dựng lại hành vi `shutil.which`; rig ấy đã hỏng **hai lần**. Lần này không có bản dựng lại nào
— ta gọi chính hàm.

**Ca đối chứng biết trước đáp án** (kiểm rig trước khi tin bất cứ ca nào):

```
[phải NHẬN ] git.exe ở thư mục ngoài cwd   -> .../ngoai/git.exe      ✔
[phải TỪ CHỐI] git.exe nằm TRONG cwd        -> None                   ✔
```

| hướng | đo được | |
|---|---|---|
| `P1-2` lượt 2 — bước 3 nhận `.bat`/`.cmd`/`.py` | `git.bat` · `git.cmd` · `git.py` · `git` (không đuôi) ⇒ **TỪ CHỐI cả bốn** | **ĐÓNG THẬT** |
| `P2-MỚI` lượt 2 — ca bắt buộc không được thi công | `t166` nay có **"Cửa 2 (P2-MỚI)"** đo đúng PATH-ngoài-cwd-chỉ-có-`.bat/.cmd/.py` ⇒ phải `None` **và** `rc == 12` | **ĐÓNG THẬT** |
| thư mục tên `git.exe` | **TỪ CHỐI** | đạt |
| bộ test đầy đủ trên head | `161/161 đạt, đã chạy=161, bỏ qua=0`, **0 ca ĐỎ** | đạt |
| kích thước theo `ADR-0044` | **2 tệp, +270 / −4**; ngưỡng `sensitive` là **≤ 3 tệp và ≤ 300 dòng thêm** | **trong ngưỡng** |

**Cách đóng `P1-2` MẠNH hơn mức lượt 2 đòi, và đáng nói ra:** bước 3 **bỏ hẳn `shutil.which`**,
dựng `Path(d) / "git.exe"` tường minh. Tức nó không còn phụ thuộc vào việc `shutil.which` có kéo
`PATHEXT` hay không — cả một lớp rủi ro chết theo **kiến trúc**, không theo bản vá.

**Một đính chính của chính reviewer, ghi thành số:** tôi đã suýt báo "vượt trần" vì nhớ ngưỡng là
**250**. Đo lại `docs/adr/0044-…md:5` ⇒ `sensitive` là **≤ 3 tệp và ≤ 300 dòng thêm`. Con số 250 là
số **#551 tự đặt cho mình**, không phải ngưỡng chung. `+270` **không** vượt.

## 2. Phát hiện

### P1 — Bước 1 (`CONG_CU_GIT`) nhận **BẤT KỲ tệp nào**, kể cả `.bat` và `.txt`

Đo, cùng rig, cùng ca đối chứng:

```
CONG_CU_GIT=git.exe                        -> NHẬN
CONG_CU_GIT=git.bat                        -> NHẬN     ← .bat
CONG_CU_GIT=git.cmd                        -> NHẬN     ← .cmd
CONG_CU_GIT=git.py                         -> NHẬN     ← .py
CONG_CU_GIT=khong-phai-git-chut-nao.txt    -> NHẬN     ← không liên quan gì tới git
```

`hop_le()` chỉ kiểm **ba** điều: là tệp · không dưới `%SystemRoot%` · không trong `cwd`. **Không
kiểm đuôi.** Bước 2 đấm cứng `git.exe` trong đường dẫn ứng viên; bước 3 dựng `git.exe` tường minh.
Chỉ bước 1 là trống.

**Vì sao là P1 chứ không phải chi tiết:** trên Windows, trao một đường dẫn `.bat` cho
`CreateProcessW` thì nó chạy **qua `cmd.exe`** — đúng cái hiểm hoạ mà cả packet này sinh ra để
đóng. Và mô hình đe doạ đang **không nhất quán**: PATH bị coi là KHÔNG đáng tin (chỉ `git.exe`, loại
cwd, loại `%SystemRoot%`), trong khi `CONG_CU_GIT` — cũng là **một biến môi trường** — được tin về
KIỂU tệp, chỉ kiểm VỊ TRÍ. Ai đặt được biến môi trường thì đặt được cả hai.

**Nói cả vế giảm nhẹ, vì nó có thật:** `CONG_CU_GIT` là đường **operator chỉ định tường minh**,
nên có lập luận rằng người đặt nó đã chọn. Đặc tả r2 (`:192-199`) **im lặng về đuôi tệp** — nó chỉ
đòi loại `cwd` và `%SystemRoot%` ở "mọi bước". Nên đây **không phải executor làm sai đặc tả**; ràng
buộc `git.exe` là thứ sinh ra từ review lượt 1–2, và executor áp nó cho bước 3.

**Đề xuất:** áp cùng ràng buộc cho bước 1 (`Path(chi_dinh).name.lower() == "git.exe"` trên nhánh
Windows), **hoặc** — nếu chủ kho muốn giữ bước 1 là cửa thoát của operator — **khai thẳng ngoại lệ
ấy trong docstring và trong đặc tả**, vì câu *"chỉ chấp nhận git.exe, không qua PATHEXT"* hiện đọc
như một bất biến của cả hàm trong khi nó đúng cho **một trong ba** bước. Kèm một ca + một đột biến
riêng.

### P2 — Mục PATH **có dấu nháy kép** bị từ chối ⇒ máy Windows thật có thể không tìm ra git

```
PATH = C:\...\cmd            -> NHẬN
PATH = "C:\...\cmd"          -> **None (từ chối)**
```

Trên Windows, mục PATH đặt trong nháy kép là **hợp lệ và phổ biến** (đường dẫn có dấu cách, ví dụ
`"C:\Program Files\Git\cmd"`). `cmd.exe` bóc nháy; mã này **không**. Hệ quả: một bản Git cài đúng
chuẩn bị **bỏ qua im lặng**, rơi xuống hết bước 3 rồi `Chan(RC_KHONG_XAC_DINH)`.

Đây là **fail-closed** nên không phải lỗ an ninh — nhưng là một **lỗi khả dụng chỉ hiện trên
Windows thật**, đúng lớp mà `gate (windows-latest)` chưa từng chạy cho bản vá này (`manual_ci_budget:
0`). `shutil.which` cũ **cũng không** bóc nháy, nên đây không phải hồi quy do bản vá; nó là một lỗ
**có sẵn nay lộ ra** khi ta tự dựng vòng lặp PATH.

**Đề xuất:** `d = d.strip().strip('"')` trước khi dựng ứng viên, kèm một ca.

### P3-1 — Một dấu `;` trong TÊN thư mục làm hỏng **toàn bộ** phép tách PATH

`path_val.split(";" if ";" in path_val else os.pathsep)`. Đo trên posix:

```
hai mục, phân cách bằng os.pathsep (':'), MỘT mục chứa ';' trong tên
   -> None   (mục git.exe HỢP LỆ ở mục kia bị MẤT)
```

Vì chuỗi có `;`, hàm tách theo `;` thay vì `:` ⇒ cắt nát cả hai mục. Trên Windows `os.pathsep`
**chính là** `;` nên nhánh này vô hại; nó chỉ có nghĩa ở posix — tức ở **chính bộ test**, nơi ca N2
tiêm PATH kiểu Windows vào Linux. Nên hậu quả thực tế là **một ca test có thể im lặng đo sai**, chứ
không phải người dùng gặp.

**Đề xuất:** tách theo `os.pathsep` khi nền thật là posix, và cho ca test tiêm rõ dấu phân cách
thay vì đoán từ nội dung chuỗi.

### P3-2 — `sys.stderr.write` VÔ ĐIỀU KIỆN, trong khi đã có tham số `chan_doan`

Hàm nhận `chan_doan` (danh sách) để thu chẩn đoán **có cấu trúc**, nhưng vẫn ghi thẳng 73 ký tự ra
`stderr` mỗi lần bước 2 không phân giải — **người gọi không tắt được**.

Việc này **đã gây thiệt hại đo được**: nó làm hỏng một phép đo của lượt 3 (commit `7d25003` trên
nhánh lượt 3: *"một dòng stderr giết cả lượt đo"*), và làm hỏng một phép đo của **chính lượt 4 này**
ở vòng đầu — tôi phải thêm mốc cắt `===JSON-BAT-DAU===` mới lấy được kết quả. Hai phiên độc lập,
cùng một chỗ.

Lượt 3 kết luận đó là *"lỗi của BỘ ĐO, không phải bản vá"*. **Đúng một nửa**: bộ đo phải chịu được
stderr. Nhưng một hàm thư viện ghi chẩn đoán không tắt được, ở một nhánh **bình thường** (máy chưa
cài Git dưới `%ProgramFiles%`), là một khuyết tật của hàm — và bằng chứng là nó đã cắn **hai** người
đo khác nhau.

**Đề xuất:** chỉ ghi `stderr` khi `chan_doan is None`, hoặc thêm cờ tắt.

## 3. Việc NGOÀI bản vá (không tính vào số lớp)

**Base đã cũ.** `merge-base(origin/master, fix_issue_541)` = `d705623162b7`, còn `origin/master` nay
là `eb15657dae7a` (merge PR #553). `merge-base --is-ancestor origin/master HEAD` ⇒ **rc=1**. Cổng
`thu-hoi` đòi quan hệ ấy và sẽ `CHAN [12]` ở lượt chạy kế. Hoà `origin/master` vào nhánh (**merge**,
không rebase, không force-push) rồi neo verdict lượt sau vào head SAU hoà. Write set của #553 rời
hẳn write set của packet này nên không dự kiến xung đột.

**Hồ sơ lượt 3 sẽ làm CI ĐỎ khi land.** Nhánh `claude/review-541-luot3-20260918` có bốn tệp
(`wp541-review-3-claude-verdict.md` + ba script đo) nhưng **không có `.receipt.yaml`** và **không có
hàng Mục lục** trong `ops/reviews/README.md`. Hai cổng sẽ bắt: `t26` (*"thiếu/rỗng `evidence_url`"*
— thực ra là thiếu hẳn biên nhận) và `t27` (*verdict không có trong cột `tệp verdict` của bảng Mục
lục*). Cả hai đã bắt đúng phiên này **ba lần** trong ngày. Đây là việc của phiên viết lượt 3, không
phải của agy.

**Đặc tả r2 đã cũ ở một dòng.** `ops/specs/wp541-path-toi-thieu-theo-nen-r2.md:196` vẫn ghi bước 3
là `shutil.which("git")` — chính thứ lượt 2 chứng minh là sai (nó luôn kéo `PATHEXT` trên Windows).
Bản vá **cố ý đi khác đặc tả** và đi **đúng**. Đặc tả nên được sửa ở revision sau; ghi ra đây để
không ai đọc đặc tả rồi "sửa" mã ngược lại. Đây là khuyết tật của đặc tả — và lời khuyên sai ban
đầu là của **reviewer lượt 1**, tức của tôi.

## 4. Chưa đo được

- **`gate (windows-latest)`** — chủ kho đặt `manual_ci_budget: 0`. **KHÔNG DÙNG PHƯƠNG TIỆN**, không
  phải *"đã đo và xanh"*.
- **Hành vi spawn thật của `.bat` trên Windows.** `P1` lập luận từ cơ chế `CreateProcessW`; tôi
  **chưa** chạy được một lượt spawn thật. Bộ đo `do_551.py` đã giao cho chủ kho sẽ đo đúng chỗ này.
- **Mục PATH có nháy trên Windows thật** — `P2` đo trên Linux bằng chính hàm ấy; hành vi phân giải
  đường dẫn của Windows có thể khác. Cần một lượt chạy trên nền thật để nâng từ *suy luận có phép
  đo* lên *phép đo trên nền đích*.

---

**Nguồn có thẩm quyền là tệp có băm trong kho; mọi bản đăng lên GitHub chỉ là bản chiếu.**
