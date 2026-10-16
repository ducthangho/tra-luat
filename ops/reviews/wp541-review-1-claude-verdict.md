verdict: changes_requested
reviewed_sha: 2170a4a4ce93

# CROSS-REVIEW LƯỢT 1 — packet #541 `WP541-PATH-TOI-THIEU-THEO-NEN` **r1 / gen 1**

| | |
|---|---|
| `reviewed_sha` | `2170a4a4ce93` (PR #554, nhánh `fix_issue_541`) — đo `01:10Z 18-09-2026` |
| `base_sha` lease khai | `d705623162b7` |
| `base_sha` THẬT của nhánh | **`a612c70cbc56`** — lệch, xem `P2-2` |
| lease | `wp541-path-r1-g1-antigravity`, `spec_hash fc6e814d2bfacf74a00537a57bd33aca712d50eca5302b23780bfbeef1162075` |
| kết luận | **`changes_requested`** — 3 LỚP P1 · 3 LỚP P2 · 4 P3 |
| assurance | **`advisory_review`** — trần cứng, xem cuối tệp |

## TÔI ĐỌC CHECK RUN TRƯỚC — VÀ NÓ KHÔNG PHẢI "XANH"

Nợ `REVIEW-KHONG-DOC-CHECK-RUN` do chính tôi đặt sau khi tự mắc ở lượt 2 của #548. Lượt này đọc
trước mọi việc khác. Trên `2170a4a4ce93` có **đúng một** check run:

| check run | kết luận |
|---|---|
| `thu-hoi` | **failure** (run `35290612007`) |
| `gate` | **KHÔNG TỒN TẠI** |

`gate` **chưa từng chạy** trên head này — `actions_list` trên `ci.yml` không có lượt nào cho
`fix_issue_541`. Nên **mọi ô `PASS` trong bảng của thân PR là lời khai tại chỗ, chưa cổng nào xác
nhận.** Đây là `KHÔNG ĐO ĐƯỢC`, không phải xanh; đúng bài học *"cổng không nói dối — nó VẮNG MẶT,
và trên giao diện xanh với chưa-chạy nhìn giống hệt nhau"*.

## `P1-1` — `t168` ĐỎ TRÊN CHÍNH CÂY CỦA BẢN VÁ, và nền KHÔNG phải nguyên nhân

Thân PR khai `N4 (t168) | 1/1 đạt | PASS` và `N5 (Hồi quy) | delta = 0 | PASS`. Đo lại:

```
nền  origin/master        rc=0   lease_publish: 157/157 đạt; đã chạy=157, bỏ qua=0
head origin/fix_issue_541 rc=1   lease_publish: 158/159 đạt; đã chạy=159, bỏ qua=0
```

Ca đỏ, xác nhận trên **cả ba làn** (CHA · `[A]` · `[B]`):

```
ĐỎ  t168_N4_posix_khong_hoi_quy_usr_bin_git: Chan: KHÔNG_XÁC_ĐỊNH:
    không thấy `git` trong PATH tối thiểu /usr/bin:/bin
```

**Nguyên nhân gốc, phản chứng MỘT BIẾN.** Fixture ghi tệp bằng `write_text` ⇒ chế độ **644**;
`shutil.which` đòi bit thực thi (`os.access(..., X_OK)`). Đo tách bạch:

```
chế độ tệp fixture      : 644
shutil.which TRƯỚC chmod: None
shutil.which SAU  chmod: /tmp/…/usr/bin/git
```

Chỉ thêm `os.chmod(fake_bin/"git", 0o755)` vào fixture, **không đụng gì khác**:

```
TRƯỚC khi sửa (cây agy nguyên bản): rc=1   0/1 đạt
SAU khi CHỈ thêm chmod +x         : rc=0   1/1 đạt
```

**Không phải lỗi môi trường** — đã đo nền trước khi nghi bản vá: container này CÓ
`/usr/bin/git`, `-rwxr-xr-x`. Bit thực thi là yêu cầu của POSIX nói chung, nên ca này sẽ đỏ y hệt
trên `ubuntu-latest`.

⇒ **`N5` KHÔNG ĐẠT**: `1` ca đỏ MỚI, và nó là một trong bốn ca do chính bản vá thêm vào.

## `P1-2` — BƯỚC 3 CHẤP NHẬN `git.bat` / `git.py` / `git` / `git.cmd` TỪ **MỌI** THƯ MỤC PATH

`N2` tồn tại vì nhánh `win32` của `shutil.which` tự chèn `os.curdir`, nên một `git.bat` cắm vào
cwd sẽ được chạy. Bản vá đóng cwd — rồi **mở lại đúng vector ấy ở mọi thư mục PATH khác**:

```python
for ten in ("git.exe", "git.cmd", "git.bat", "git.py", "git"):
```

Phản chứng đã chạy, **hai chiều**:

| đầu vào | kết quả |
|---|---|
| PATH chỉ có `git.bat` | **CHẤP NHẬN** `…/path_git_bat/git.bat` |
| PATH chỉ có `git.py` | **CHẤP NHẬN** `…/path_git_py/git.py` |
| PATH chỉ có `git` (không đuôi) | **CHẤP NHẬN** `…/path_git/git` |
| PATH chỉ có `git.cmd` | **CHẤP NHẬN** `…/path_git_cmd/git.cmd` |
| **cwd** chỉ có `git.bat` | từ chối (`None`) |
| **cwd** chỉ có `git.py` | từ chối (`None`) |
| `shutil.which("git")` trên thư mục chỉ có `git.py` | **`None`** |

Dòng cuối là chỗ đắt: phép quét tay **RỘNG HƠN** đúng thứ docstring của chính hàm hứa
(*"3. `shutil.which("git")` trên PATH thật"*). `shutil.which` tôn trọng `PATHEXT` và **không**
trả `git.py`; phép quét tay thì trả. Tức bản vá không chỉ chuyển cơ chế, nó **nới** tập tên được
chấp nhận, ở đúng bước được mô tả là "đường CHÓT".

Đây là hình dạng *"danh sách CẤM không bao giờ đủ"* nhìn từ mặt kia: phòng thủ dựng ở **một** thư
mục (cwd) trong khi cửa mở ở **mọi** thư mục còn lại.

**KHÔNG ĐO ĐƯỢC từ đây:** hệ quả spawn. `subprocess.run([git_exe, "--version"])` trên Windows đi
`CreateProcessW`, mà `CreateProcessW` không chạy được `.bat`/`.py` như một executable — bài học
`CreateProcessW chỉ tự thêm .exe` đã có trong `CLAUDE.md`. Nếu đúng vậy thì một `KHÔNG_XÁC_ĐỊNH`
sạch (`rc=12`) biến thành một lỗi spawn khó đọc. Tôi **không có Windows** để đo, nên ghi là
KHÔNG ĐO ĐƯỢC chứ không khai là đã chứng minh.

## `P1-3` — VI PHẠM `DIEU_KIEN_BAT_DAU` CỦA LEASE

Lease `wp541-path-r1-g1-antigravity` viết, nguyên văn:

> Executor **KHÔNG** được chạm `ops/lease_publish_test.py` cho tới khi `ai-dang-giu` cho đường ấy
> trả `rc=0` / `NGƯỜI_GIỮ 0`. Phải **ĐO** trước mỗi lần chạm, không suy từ mốc
> `2026-09-18T17:00:00Z`: *"hết hạn" KHÔNG phải "đã nhả"*.

và liệt kê trong `prohibited_actions`:

> `CHAM ops/lease_publish_test.py TRUOC khi lease #548 nha duong ay`

Đo lúc `01:0xZ 18-09-2026`, sau khi fetch đủ ref:

```
ai-dang-giu ops/lease_publish_test.py  →  rc=11
NGƯỜI_GIỮ 2: ci-windows-r2-g2-antigravity, wp541-path-r1-g1-antigravity
```

`ci-windows-r2-g2-antigravity` (#548) **vẫn giữ** đường ấy tới `17:00:00Z`. Bản vá thêm **172 dòng**
vào chính tệp đó.

Lease đã khai thẳng rằng chốt này là **kỷ luật, không phải cổng** — *"Không máy nào cưỡng chế nó.
`DIEU_KIEN_BAT_DAU` là thứ duy nhất đứng giữa lease này và cửa sổ hai writer"*. Nó vừa không được
giữ. Kho đã trả giá một lần cho đúng chuyện này (`#227`, cửa sổ hai writer ~23,75h).

**Đây KHÔNG phải lỗi kỹ thuật của mã** và tôi không đề nghị vứt công việc đi. Nhưng nó là quyết
định của **người giữ kho**, không của reviewer: hoặc chủ kho khai một ngoại lệ §5 có phạm vi (như
đã làm cho #551), hoặc phần `lease_publish_test.py` chờ tới khi `ai-dang-giu` trả `rc=0`.

## `P2-1` — NHÁNH SAI

| | |
|---|---|
| lease khai | `branch: agy/wp541-path-r1-g1`, `branch_ownership: exclusive` |
| tồn tại trên origin | **0** |
| agy đẩy | `fix_issue_541` |

`branch_ownership: exclusive` không còn nghĩa gì nếu công việc sống ở một nhánh khác tên. Tên nhánh
không phải định danh của lease, nhưng lease **khai** một tên và hiện vật **ở** tên khác thì mọi
phép tra theo hồ sơ đều trượt.

## `P2-2` — BASE SAI ⇒ `thu-hoi` ĐỎ, và hoà sẽ là hoà THẬT trên tệp test

| | |
|---|---|
| lease khai | `start_from_sha: d705623162b7` (master lúc cấp) |
| merge-base thật | **`a612c70cbc56`** — 8 commit trước |
| `master` là tổ tiên của head? | **KHÔNG** |

Đó chính là `thu-hoi` `failure`. Chữa bằng merge `origin/master` vào nhánh — nhưng phải biết trước
rằng **đây không phải hoà hình thức**: packet #548 đã sửa **chính** `ops/lease_publish_test.py`
(`+220` dòng, thêm `t161`/`t162`), còn nhánh này thêm `t165`–`t168` từ base cũ. Đo:

```
nhánh agy có t161/t162 (của #548) : 0
master  có t161/t162              : 2
```

Không va tên ca (master cao nhất là `t162`), nên xung đột sẽ là xung đột vị trí chứ không phải
trùng định danh — nhưng nó vẫn là hai bên cùng sửa một tệp, phải giải bằng tay và **đo lại** sau đó.

**Kèm một cảnh báo về con số chống đỡ THẨM QUYỀN.** `N6` (trần ADR-0044) trong thân PR đo bằng
`git diff` **ba chấm** so `a612c70`: `2 tệp, +271 / −3`. Cách đo ấy đúng với base cũ. Đo **hai
chấm** so master thật cho ra **7 tệp, +297 / −284** — con số ấy **không** có nghĩa "agy hoàn tác
#548" (hoà git sẽ giữ phía master cho 5 tệp agy không đụng), nên đừng đọc nó như một phát hiện.
Điều nó nói là: **`N6` phải được đo LẠI sau khi hoà**, vì nó là con số chống đỡ một câu về thẩm
quyền, và nó đang neo vào một base không còn là base.

## `P2-3` — `gate` CHƯA CHẠY (đã nêu ở đầu)

Không lượt `ci.yml` nào cho head này. `N1`–`N6` trong thân PR vì thế đều là lời khai tại chỗ.
Không gọi CI tay (`manual_ci_budget: 0`) — cách đúng là **đẩy một commit** (chính là commit hoà +
bản vá `t168`), lượt PR sẽ tự bắn.

## `P3` — bốn mục, và mục đầu SUÝT thành một phát hiện SAI của tôi

**`P3-1` — bốn khối "đột biến" trong test là TAUTOLOGY.** Cả bốn là **hàm cục bộ** định nghĩa
trong chính tệp test, không chạm mã sản phẩm. Nặng nhất là `t167` cửa (b):

```python
chan_doan_mut_b = []
chot(not any("KHÔNG_ĐO_ĐƯỢC" in str(msg) for msg in chan_doan_mut_b), ...)
```

`not any(...)` trên danh sách **rỗng** là `True` vô điều kiện. Phép kiểm ấy **không bao giờ đỏ
được**, nên nó không phải bằng chứng. `t165`/`t166`/`t167a` cùng hình dạng: một hàm trả `X` rồi
khẳng định nó trả `X`.

**NHƯNG PHẢI NÓI CHO ĐÚNG, và đây là chỗ tôi suýt sai.** Đọc mã xong tôi đã định kết luận *"bốn ca
không có răng"*. Chạy thì ngược lại. Đột biến vào **HÀM THẬT**, mỗi lần một biến, mỗi mutant một
thư mục riêng, tắt bytecode:

| đột biến vào mã sản phẩm | ca đích | kết quả |
|---|---|---|
| `MA` — bỏ hẳn nhánh `windows`, rơi về hằng số cũ | `N1` `t165` | **BỊ GIẾT** (`rc=1`) |
| `MB` — gỡ phép loại-trừ cwd trong `hop_le` | `N2` `t166` | **BỊ GIẾT** |
| `MC` — gỡ phép loại `%SystemRoot%` | `N3a` `t167` | **BỊ GIẾT** |
| `MD` — bỏ `chan_doan.append(...)` | `N3b` `t167` | **BỊ GIẾT** |
| `ME` — đổi hằng số nhánh POSIX | `N4` `t168` | **BỊ GIẾT** |

Mỗi đột biến tự chứng minh đã áp (`TRƯỚC=1 SAU=0`). ⇒ Kết luận đúng là: **các khối tautology ấy vô
giá trị, KHÔNG phải các CA vô giá trị.** Răng nằm ở những khẳng định thật bao quanh chúng. Bốn khối
kia nên **xoá** (chúng làm bảng nghiệm thu trông như đã đo đột biến trong khi không), hoặc viết lại
thành đột biến thật vào mã sản phẩm như bảng trên.

Ghi ra vì đó đúng bài học *"NGHĨ RA được phép thử mà KHÔNG CHẠY nó thì phép thử ấy KHÔNG TỒN TẠI"*,
áp theo chiều ngược: đọc mã rồi kết luận "không có răng" mà chưa chạy là cách sinh ra một phát hiện
giả.

**`P3-2` — thông điệp `Chan` đấm cứng `/usr/bin:/bin`.** `path` nay tiêm được, nhưng lỗi vẫn in
*"không thấy `git` trong PATH tối thiểu /usr/bin:/bin"* bất kể đã tìm ở đâu. Chính nó làm `P1-1`
khó đọc: thông điệp chỉ vào một đường dẫn mà phép chạy ấy không hề tìm.

**`P3-3` — docstring mâu thuẫn mã.** Docstring khai bước 3 là `shutil.which("git")`; mã quét tay
một danh sách tên. Đo được ở bảng `P1-2`: hai đường cho hai kết quả khác nhau.

**`P3-4` — `ds_khao_sat = [cw] + ds_thu_muc`.** Thêm cwd vào danh sách khảo sát rồi trông vào
`hop_le` loại nó ra. Mã chết, và nó làm người đọc tưởng cwd có được xét.

## BẢNG ĐO ĐẦY ĐỦ — KỂ CẢ CÁI KHỚP

| phép đo | kết quả |
|---|---|
| head trôi trong lúc review? | **không** — `2170a4a4ce93` ở cả hai lần đo |
| `write_set` (số tệp) | **đúng 2** — `ops/lease_publish.py`, `ops/lease_publish_test.py` ✔ |
| ca test mới có `@ca` (được đăng ký) | **4/4** ✔ — không ca nào "có MẶT mà không ĐO" |
| `N1` `t165` trên cây sạch | `rc=0` ✔ |
| `N2` `t166` trên cây sạch | `rc=0` ✔ |
| `N3` `t167` trên cây sạch | `rc=0` ✔ |
| `N4` `t168` trên cây sạch | **`rc=1`** ✘ — `P1-1` |
| đột biến thật vào mã sản phẩm | **5/5 bị giết** ✔ |
| `N5` delta ca đỏ so nền | **KHÔNG ĐẠT** — nền `157/157`, head `158/159` |
| `N6` numstat (ba chấm, base cũ) | `2 tệp, +271 / −3` — dưới trần, **nhưng neo vào base đã trôi** |
| `thu-hoi` | **failure** |
| `gate` | **KHÔNG TỒN TẠI** trên head |
| `ai-dang-giu ops/lease_publish.py` | `rc=11 · NGƯỜI_GIỮ 1` = chính lease này ✔ |
| `ai-dang-giu ops/lease_publish_test.py` | `rc=11 · **NGƯỜI_GIỮ 2**` ✘ — `P1-3` |

## `KHÔNG ĐO ĐƯỢC` — khai, không lấp

1. **Hành vi spawn `.bat`/`.py` trên Windows thật** — không có Windows ở đây. Hệ quả của `P1-2` vì
   thế nêu ở mức *"nếu"*, không khai là đã chứng minh.
2. **`N7`** (*"Trước = 1, Sau = 0"* trên Windows thật) — không tái lập được từ container này. Thêm
   nữa, hai con số ấy **không kèm đơn vị** và không khớp với *"14 ca PATH"* ở cùng dòng. Luật `L1`
   của kho: mọi con số phải khai **đếm gì**. Đề nghị executor nói rõ `1` và `0` đếm cái gì.
3. **`gate` trên head** — xem `P2-3`.

## KHAI XUNG ĐỘT LỢI ÍCH

Phiên này **không** soạn đặc tả r2 của #541 (phiên `session_015diBngheEgZLBopnn4K13P` soạn) và
**không** cấp HINT nào cho bản vá này, nên phán quyết về hình dạng bản vá là độc lập.

Nhưng có một chỗ **phải** khai: phiên này chính là phiên đã **ghi hộ lease
`ci-windows-r2-g2-antigravity`** — cái lease đang giữ `ops/lease_publish_test.py` và làm nên
`P1-3`. Tôi có lợi ích trong việc lease ấy được coi là chính đáng. Vì thế `P1-3` được viết dưới
dạng **phép đo** (`rc=11`, `NGƯỜI_GIỮ 2`) cộng **trích nguyên văn** điều khoản lease, và kết luận
để ngỏ cho chủ kho quyết, chứ tôi không tự phán là phải vứt phần việc ấy.

## ASSURANCE — trần cứng, không phải nhận xét về bản vá

**`advisory_review`**. Lease khai `assurance_target: human_audited` và `reviewer_provider: human`.
Tôi **không** phải người audit theo nghĩa §8 — tôi là một phiên `claude`, và `antigravity` vẫn
xuất hiện **0** lần trong `docs/PROTOCOL_DA_PHIEN.md`, nên cặp agy↔claude không mua được
`cross_approved`. Việc ấy thuộc packet riêng **#551**.

Lượt này cũng **không có `session_run_id`**: chạy trong phiên điều phối, checkout riêng có thật
(bản giải nén rời ngoài kho), context thì không.

## NGUỒN CÓ THẨM QUYỀN

Tệp này trong kho, có băm. Bản đăng trên GitHub chỉ là **bản chiếu**.
