# WP541 WINDOWS-LEASE-PUBLISH — spec r3 (packet **revision 2 / generation 2**)

> ĐẶC TẢ ĐÓNG BĂNG. KHÔNG phải lease, KHÔNG cấp việc. Phải có lease còn hiệu lực
> (`docs/PROTOCOL_DA_PHIEN.md` §3.2, §4) thì mới được bắt tay.
>
> **`r3` thay `r2`** (`fc6e814d2bfacf74a00537a57bd33aca712d50eca5302b23780bfbeef1162075`, nhánh
> `claude/spec-541-r2-20260917`). `r2` KHÔNG sai — bản vá theo nó đã đạt N1–N4 trên Windows thật.
> `r3` **mở rộng phạm vi**, và `docs/PROTOCOL_DA_PHIEN.md:300` nói thẳng: *"Mở rộng phạm vi hay đổi
> closure là revision mới, generation mới và cấp lại lease."* Nên đây là **revision 2 / generation
> 2**, và lease `wp541-path-r1-g1-antigravity` phải bị thay thế HAI CHIỀU (`thay_the_cho` ở lease
> mới, `da_bi_thay_the` ở lease cũ) — `_phan_loai_lease` chỉ biết HẠN, chỉ `lenh_ai_dang_giu` đọc
> `da_bi_thay_the`.
>
> `r1` (`28ebf711…`) và `r2` giữ nguyên làm dấu vết, KHÔNG sửa đè.
>
> Mọi con số ghi kèm ĐƠN VỊ (L1) và THỜI ĐIỂM ĐO (L5).

## packet_id · packet_issue

| trường | giá trị |
|---|---|
| `packet_id` | `WP541-WINDOWS-LEASE-PUBLISH` |
| `packet_issue` | **541** |
| `revision` / `generation` | **2 / 2** — căn cứ `PROTOCOL:300`. `r1/g1` đã cấp lease, đã giao hàng (`2f70869a`), đã review bốn lượt. |
| `mission_issue` | `KHONG_CO` |
| `base_sha` | `eb15657dae7a5f0e494a1dca50fdd6d8a55ed7d3` (`origin/master`, đo `15:27Z 18-09-2026`) |
| `nhanh giao hang g1` | `fix_issue_541`, head `2f70869a0537843e9cae78618ee7ae8c261d972d`, PR **#554** (`open`, đo `15:40Z 18-09`) |

**Mỏ neo của g1 ĐÃ CŨ.** `merge-base(origin/master, fix_issue_541)` = `d705623162b7`, còn
`origin/master` nay là `eb15657dae7a` — **13 commit** ở giữa (đơn vị: commit, đo `15:27Z 18-09`).
g2 phải hoà `origin/master` vào nhánh **bằng merge**, không rebase: `2f70869a` là `reviewed_sha`
của bốn lượt review và rebase làm mọi verdict ấy trỏ vào SHA không tra được.

## nguon_cap_viec

Ba nguồn, cả ba neo được:

1. **Issue #541, thân issue** — cấp phép gốc, ràng buộc gốc (xem `ngoai_pham_vi`).
2. **Verdict lượt 4** — `ops/reviews/wp541-review-4-claude-verdict.md` trên nhánh
   `claude/review-541-luot4-20260918` (commit `074fd01`), PR **#560**: `changes_requested`,
   **1 P1 · 1 P2 · 2 P3**, neo `reviewed_sha 2f70869a`.
3. **Chỉ thị chủ kho, phiên điều phối 18-09-2026**, nguyên văn: *"t136 gộp vào #541 luôn"* ·
   *"soạn spec r3 đi"*.

**Lượt 3 đã RÚT verdict `approve` xuống `changes_requested`** (`ops/reviews/wp541-review-3-claude-verdict.md`,
commit `7cfd5ce` trên `claude/review-541-luot3-20260918`) sau khi đo lại độc lập và tái hiện cả ba
phát hiện đo được của lượt 4. Không phát hiện nào của lượt 4 được nhận bằng lời khai.

## review_class

Giữ nguyên r2: `risk` = `review_class` = **`sensitive`** — `ops/lease_publish.py` trúng cả
*"review/land authority"* lẫn *"gate lifecycle"* của §8. Không hạ được.

Đo bổ sung (r2 chưa có, `#552` r2 §D7 đã ghi): `_tinh_lop_tu_write_set` trả `sensitive` cho **MỌI**
đầu vào đã thử — `_BANG_LOP` có **7** mục, **tất cả** `sensitive`, và mặc định của `next()` cũng là
`sensitive`, nên giá trị khởi tạo `"routine"` trong hàm **không bao giờ tới được**. Lớp này do CỔNG
tính, không do spec khai; khai lệch thì cổng bác (`rc=10`).

## write_set

**KHÔNG ĐỔI.** Hai đường dẫn, đúng chữ `only` của Issue #541:

1. `ops/lease_publish.py`
2. `ops/lease_publish_test.py`

## KÍCH THƯỚC — KHAI VƯỢT NGƯỠNG, theo đúng cửa ADR-0044 tự mở

**Đây là mục quan trọng nhất của r3. Đọc trước khi viết dòng mã nào.**

Đo `15:40Z 18-09-2026`, `git diff --numstat d705623 origin/fix_issue_541`:

```
  ops/lease_publish.py        +102   -4
  ops/lease_publish_test.py   +168   -0
  TONG: 2 tep, +270, -4
```

Ngưỡng `sensitive` của ADR-0044 là **≤ 3 tệp và ≤ 300 dòng thêm**. g1 đã dùng **+270/300**. Còn
**30 dòng**. Năm mục tiêu của r3 (bốn bản vá + năm ca mới + một sửa fixture) **không thể** nằm trong
30 dòng. Nói thẳng con số thay vì để executor đâm vào trần giữa chừng.

**Hai đường ra, và một trong hai bị CẤM:**

- **Tách packet nối tiếp** — ADR-0044 nguyên văn: *"nối tiếp chỉ hợp lệ khi slice sau mọc trên
  `mission/<issue>/integration` **đã nhận** slice trước, không mọc trên một PR chưa merge."*
  PR #554 **chưa merge** và lane này **không có** integration branch. Đường này **đóng**.
- **Khai lý do trong spec** — ADR-0044 nguyên văn: *"Vượt một trong hai ngưỡng thì dừng TRƯỚC
  review để revision thiết kế, **hoặc khai lý do trong spec**; không tự mở hai PR chồng lấn."*
  Đây là đường ADR tự mở, và r3 **chính là** cái revision thiết kế ấy.

**Trần mới: ≤ 2 tệp và ≤ 400 dòng thêm** (đơn vị: `git diff --numstat` so `d705623`).

Con số 400 **neo từ dữ liệu của chính ADR-0044**, không từ cảm tính: ADR ghi `PLAT-M4` = 2 tệp,
**+351/−25** ⇒ **một vòng, một finding**; còn `PLAT-X4` = 4 tệp, +721/−159 ⇒ ba vòng, tám finding.
Tức một packet **2 tệp quanh +350** đã được chính kho này đo là quản được. 400 nằm trong dải ấy và
vẫn cách xa +721. Dự toán của r3: `+270` hiện có `+` ~12 dòng bốn bản vá `+` ~125 dòng năm ca mới
`+` ~3 dòng sửa fixture ≈ **410**… **cao hơn trần 400 mười dòng**. Đó là CỐ Ý: dự toán sát trần để
executor phải đo thật chứ không ước lượng. **Vượt 400 ⇒ DỪNG, handoff, KHÔNG tự nới** (N6').

**Vì sao không đơn giản nâng trần cho khỏi vướng:** trần này là thứ duy nhất trong packet ngăn
"vá thêm một chút nữa" lặp lại tới khi bản vá quá lớn để review. ADR-0044 sinh ra từ đúng một phép
đo cho thấy điều đó xảy ra thật.

## hien_trang_da_do

### Nguồn đo

| nguồn | thời điểm |
|---|---|
| Windows thật của chủ kho, quyền **Administrator**, Python 3.13.1, git 2.55.0.windows.5 | `18-09-2026 20:35+07` |
| biên nhận | `ops/reviews/wp541-do-windows-that-20260918.md` (nhánh `claude/review-541-luot3-20260918`) |
| verdict lượt 4 | `claude/review-541-luot4-20260918`, `074fd01` |
| đo lại độc lập bốn phát hiện | `ops/reviews/wp541-kiem-lai-luot4.py`, cùng nhánh lượt 3 |

### CÁI ĐÃ ĐÓNG THẬT — không mở lại, ghi để khỏi đo lại

Đo trên Windows thật, `rc=0`, mọi chốt đạt:

- **N1–N4** (`t165` `t166` `t167` `t168`): **QUA cả bốn**. Đây là tiêu chí nghiệm thu duy nhất r2
  công nhận (N0).
- **N7 của reviewer** (đơn vị, không phải tiêu chí spec): số dòng khớp `if nen_thuc == "windows":`
  **trước = 1, sau = 0**; tắt nhánh ấy ⇒ `t165` ĐỎ với lý do `KHÔNG_XÁC_ĐỊNH: không thấy 'git'
  trong PATH tối thiểu` — **giết đúng lý do**, không phải tín dụng giả.
- Giải đường dẫn thật: `_git_exe_toi_thieu()` → `C:\Program Files\Git\cmd\git.exe`; shim
  `.bat/.cmd/.py` ở PATH ngoài cwd ⇒ `None`; **đối chứng dương** thêm `git.exe` ⇒ tìm ra.
- 15 ca từng đỏ trên CI: **11 xanh**. Bốn ca còn đỏ đã đọc mã từng ca, **không ca nào** còn chữ ký
  PATH (chi tiết ở §`ngoai_pham_vi` và M5).
- Kích thước: 2 tệp, +270/−4 — trong trần **cũ** (300).

### BỐN PHÁT HIỆN CỦA LƯỢT 4 — đã tái hiện độc lập

Rig chạy **cặp ca đối chứng trước** (biết trước đáp án) rồi mới tin ca nào:

```
=== CA DOI CHUNG ===
  git.exe ngoai cwd  -> NHAN   OK
  git.exe TRONG cwd  -> None   OK
```

| mã | đo được | hạng |
|---|---|---|
| **P1** | `CONG_CU_GIT` = `git.exe` · `git.bat` · `git.cmd` · `git.py` · `khong-phai-git-chut-nao.txt` ⇒ **NHẬN cả năm** | **P1** |
| **P2** | `PATH=C:\…\cmd` ⇒ NHẬN; `PATH="C:\…\cmd"` (có nháy kép) ⇒ **None** | **P2** |
| **P3-1** | `os.pathsep=':'`, một mục chứa `;` trong TÊN ⇒ **None** — mục `git.exe` hợp lệ ở mục kia bị MẤT | P3 |
| **P3-2** | `sys.stderr.write` **vô điều kiện** dù đã có tham số `chan_doan` | P3 |

**P1 vì sao là P1, không phải chi tiết.** `hop_le()` kiểm **ba** điều: là tệp · không dưới
`%SystemRoot%` · không trong `cwd`. **Không kiểm đuôi.** Bước 2 đấm cứng `git.exe` trong đường ứng
viên; bước 3 dựng `git.exe` tường minh; **chỉ bước 1 trống**. Trên Windows, trao một đường `.bat`
cho `CreateProcessW` là chạy **qua `cmd.exe`** — đúng hiểm hoạ packet này sinh ra để đóng. Và mô
hình đe doạ đang **không nhất quán**: PATH bị coi là KHÔNG đáng tin, còn `CONG_CU_GIT` — **cũng là
một biến môi trường** — chỉ bị kiểm VỊ TRÍ. Ai đặt được biến này thì đặt được biến kia.

**Nói cả vế giảm nhẹ, vì nó có thật:** `CONG_CU_GIT` là đường operator chỉ định tường minh, và
**r2 im lặng về đuôi tệp** (`:192-199` chỉ đòi loại `cwd` và `%SystemRoot%` ở "mọi bước"). Nên đây
**KHÔNG phải executor làm sai đặc tả** — ràng buộc `git.exe` sinh ra từ review lượt 1–2 và executor
áp nó cho bước 3. r3 tồn tại để **nói ra điều r2 đã bỏ sót**, không phải để bắt lỗi ai.

**P2 là lỗi khả dụng, không phải lỗ an ninh** — nó fail-**closed**. Nhưng trên Windows, mục PATH đặt
trong nháy kép là **hợp lệ và phổ biến** (`"C:\Program Files\Git\cmd"`), nên một bản Git cài đúng
chuẩn bị **bỏ qua im lặng** rồi rơi hết xuống `Chan(RC_KHONG_XAC_DINH)`. `shutil.which` cũ **cũng
không** bóc nháy ⇒ **không phải hồi quy do bản vá**; là lỗ có sẵn nay lộ ra khi ta tự dựng vòng lặp
PATH. Đây đúng lớp mà `gate (windows-latest)` chưa từng chạy cho bản vá này (`manual_ci_budget: 0`).

**P3-2 có thiệt hại ĐO ĐƯỢC, không phải lo xa.** Nó làm hỏng **hai phép đo của hai phiên độc lập**:
lượt 3 (`7d25003` — bộ test đầy đủ chạy xong mà N7 không bao giờ chạy) và vòng đầu của chính lượt 4.
Lượt 3 từng gọi đó là *"lỗi của BỘ ĐO, không phải bản vá"*; **đúng một nửa** — bộ đo phải chịu được
stderr, nhưng một hàm thư viện ghi chẩn đoán mà người gọi **không tắt được**, ở một nhánh **bình
thường** (máy chưa cài Git dưới `%ProgramFiles%`), là khuyết tật của hàm.

### `t136` — ĐÍNH CHÍNH bảng chẩn đoán của chính r2

r2 §`hien_trang_da_do` ghi `t136 | PATH | Chan: KHÔNG_XÁC_ĐỊNH: … PATH tối thiểu /usr/bin:/bin`.
Đó là **lý do TRỰC TIẾP đọc từ log**, và nó đúng — nhưng bảng ấy trình bày nó như nguyên nhân
**DUY NHẤT**. Không phải. Lỗi PATH **CHE** một lỗi thứ hai; vá xong lỗi PATH thì lỗi kia lộ ra.

Ca đòi `rc=12` **KÈM LÝ DO** `"không khớp executable"`:

```python
rc, td = _ma_chan(mod, mod.kham_pha_nguon, ep,
                  hoso=dict(hoso, git_path="/khong/co/git"), da_duyet=[digest], …)
chot(rc == 12 and "không khớp executable" in td, f"git_path lệch phải 12: {rc} {td}")
```

Hằng `"/khong/co/git"` là đường **chỉ-POSIX**. Đo được:

```
POSIX    is_absolute("/khong/co/git")                  = True
WINDOWS  is_absolute("/khong/co/git")                  = False
POSIX    is_absolute("C:/Program Files/Git/cmd/git.exe") = False
WINDOWS  is_absolute("C:/Program Files/Git/cmd/git.exe") = True
```

Nên trên Windows `kiem_mien_ho_so` bắn **TRƯỚC** với `"git_path phải là đường tuyệt đối"`: `rc`
ĐÚNG (12), **lý do SAI**. Đúng kỷ luật *"giết đúng lý do"* mà kho đã trả giá để học — lần này nó
bắt được một ca thật.

Thân hàm `t136` **giống hệt `origin/master`** (đối chiếu băm thân hàm, đo `15:13Z 18-09`): bản vá
g1 không gây ra, cũng không che. Nó nằm TRONG write set nên sửa được ở đây, và chủ kho đã chỉ thị
gộp vào — đó là lý do r3 là **revision**, không phải generation suông.

## muc_tieu

Mỗi mục chiếu vào ĐÚNG MỘT đường dẫn trong `write_set` (L2). M1/M2 của r2 **đã xong**, không làm lại.

| # | mục tiêu | đường dẫn |
|---|---|---|
| **M3** | Bước 1 (`CONG_CU_GIT`) của `_git_windows` **chỉ nhận `git.exe`** trên nhánh Windows: `Path(chi_dinh).name.lower() == "git.exe"`, cộng đúng hai phép loại trừ vị trí như hai bước kia. Docstring sửa cho khớp: câu *"chỉ chấp nhận git.exe, không qua PATHEXT"* hiện đọc như bất biến của **cả hàm** trong khi nó đúng cho **một trong ba** bước. | `ops/lease_publish.py` |
| **M4** | Bóc nháy kép và khoảng trắng thừa ở mỗi mục PATH trước khi dựng ứng viên: `d = d.strip().strip('"')`. Mục rỗng sau khi bóc thì bỏ qua. | `ops/lease_publish.py` |
| **M5** | Tách PATH theo **`os.pathsep` của nền đang chạy**, không đoán dấu phân cách từ NỘI DUNG chuỗi. Ca test cần tiêm PATH kiểu Windows trên Linux thì truyền **dấu phân cách tường minh** qua tham số, đừng để hàm suy. | `ops/lease_publish.py` |
| **M6** | Chỉ ghi `sys.stderr` khi `chan_doan is None`. Người gọi đã truyền `chan_doan=` tức đã nhận việc thu chẩn đoán. **KHÔNG được bỏ hẳn chẩn đoán** — N3b của r2 vẫn là tiêu chí; đây là đổi KÊNH, không phải bịt miệng. | `ops/lease_publish.py` |
| **M7** | Sửa hằng đường dẫn chỉ-POSIX trong fixture `t136` thành một đường **tuyệt đối trên CẢ HAI nền** và chắc chắn không tồn tại (dựng từ thư mục sandbox, ví dụ `str(Path(s) / "khong-co-git")`). Giữ nguyên ý định của ca: `rc == 12` **và** lý do chứa `"không khớp executable"`. | `ops/lease_publish_test.py` |
| **M8** | Thêm **5** ca `tNNN_` mới cho M3·M4·M5·M6·M7, chạy được trên `ubuntu-latest` bằng tham số tiêm, **mỗi ca kèm một đột biến đổi màu riêng**. | `ops/lease_publish_test.py` |

### Ràng buộc thiết kế cho M8 — đọc trước khi viết ca

Bài học đã trả giá của kho: *"nếu ba chốt không phân biệt được bằng đầu vào thì chúng là bộ TƯƠNG
ĐƯƠNG và bạn chỉ đang đo một cái."* Năm ca dưới đây **phân biệt được bằng đầu vào**, nên là năm chốt
thật, không phải một chốt đếm năm lần. Ca nào không dựng được đầu vào tách nó khỏi bốn ca kia thì
**khai thẳng là bộ tương đương**, đừng giả vờ có năm.

**Mỗi ca phải có ĐỐI CHỨNG DƯƠNG.** Một ca chỉ đo chiều "phải từ chối" thì `return None` vô điều
kiện cũng qua được. Đây là lỗi kho đã trả giá (`t24`: suite báo 24/24 trong khi ca ấy không đo gì).

## nghiem_thu

Mỗi tiêu chí nêu PHÉP ĐO LÀM NÓ ĐỎ (L3).

**N0 giữ nguyên từ r2:** 14 ca PATH **không** phải tiêu chí nghiệm thu, chỉ là chỉ báo hồi quy.
**N1–N4 giữ nguyên và ĐÃ ĐẠT** trên Windows thật — ở g2 chúng hạ xuống làm **chỉ báo hồi quy**:
ĐỎ ⇒ g2 làm vỡ g1.

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| **N8** | `CONG_CU_GIT` trỏ vào `git.bat` · `git.cmd` · `git.py` · một `.txt` bất kỳ ⇒ **`None`**; trỏ vào `git.exe` hợp lệ ngoài `cwd` và ngoài `%SystemRoot%` ⇒ **trả đúng đường ấy**, tuyệt đối, đã resolve. | **Đột biến:** gỡ phép kiểm tên ở bước 1 ⇒ ĐỎ. Chiều dương (`git.exe` vẫn NHẬN) là bắt buộc: thiếu nó thì "bước 1 luôn trả None" cũng qua. |
| **N9** | Mục PATH bọc nháy kép `"…"` ⇒ **NHẬN** như mục không bọc. Mục rỗng, và mục chỉ có khoảng trắng ⇒ bỏ qua, không ném. | **Đột biến:** bỏ `.strip().strip('"')` ⇒ ĐỎ. Đối chứng: mục KHÔNG bọc vẫn NHẬN (chặn bản vá "bóc mọi ký tự đầu/cuối"). |
| **N10** | PATH kiểu POSIX có **một mục mang `;` trong TÊN thư mục**, mục kia chứa `git.exe` hợp lệ ⇒ **tìm ra `git.exe`**. | **Đột biến:** quay lại `split(";" if ";" in path_val else os.pathsep)` ⇒ ĐỎ. Ca này chỉ có nghĩa trên posix — tức trong chính bộ test; nói thẳng phạm vi ấy trong docstring của ca. |
| **N11** | Gọi `_git_windows(..., chan_doan=ds)` ở nhánh `%ProgramFiles%` không phân giải ⇒ `ds` **có** thông báo `KHÔNG_ĐO_ĐƯỢC…` **và** `sys.stderr` thu được **0 byte**. Gọi **không** truyền `chan_doan` ⇒ stderr **vẫn có** thông báo ấy. | **Đột biến (a):** trả `sys.stderr.write` về vô điều kiện ⇒ vế "0 byte" ĐỎ. **Đột biến (b):** bỏ hẳn lệnh ghi ⇒ vế "không truyền `chan_doan` thì stderr vẫn có" ĐỎ. Hai cửa, hai đột biến — N3b của r2 không được chết theo. |
| **N12** | Mọi hằng đường dẫn sentinel dùng trong fixture schema hồ sơ adapter phải **tuyệt đối trên CẢ HAI nền**: `PurePosixPath(s).is_absolute() and PureWindowsPath(s).is_absolute()`. | **Đột biến:** trả hằng về `"/khong/co/git"` ⇒ ĐỎ **trên `ubuntu-latest`**. Đây là mấu chốt thiết kế: khuyết tật của `t136` chỉ hiện trên Windows, mà Windows đã bị #548 gỡ khỏi cổng master — nên phải biến nó thành **bất biến độc lập nền**, đo được ở nơi cổng thật sự chạy. Một tiêu chí chỉ đỏ trên nền không ai chạy là tiêu chí không tồn tại. |
| **N5'** | *(chỉ báo, KHÔNG phải tiêu chí)* `ops/lease_publish_test.py` trên `ubuntu-latest`: **0** ca đỏ (lượt 4 đo trên head g1: `161/161 đạt, đã chạy=161, bỏ qua=0`). | ĐỎ ⇒ hồi quy do g2. Xanh **không** chứng minh mục tiêu nào. |
| **N6'** | `git diff --numstat` so `d705623162b75b7340ee7cca54ac2d2abbddbb6f`: **≤ 2 tệp và ≤ 400 dòng thêm**. | Vượt ⇒ **DỪNG, handoff, KHÔNG tự nới**. Căn cứ trần mới: §KÍCH THƯỚC. |

### Vì sao nghiệm thu vẫn KHÔNG neo vào `gate (windows-latest)`

Giữ nguyên lý lẽ r2, và nay có thêm một phép đo củng cố: **#548 đã gỡ Windows khỏi cổng master**
(ADR-0049 ghi thẳng điều đó), và `manual_ci_budget: 0` cấm gọi tay. Nên đường đo Windows duy nhất
còn lại là **máy chủ kho chạy bằng tay** — đã làm một lượt (`18-09`, biên nhận ở trên) và lượt ấy
là thứ phát hiện ra `t136`. N8–N12 chạy trên `ubuntu-latest` bằng tham số tiêm, đo **hành vi giải
đường dẫn theo nền** mà không cần nền ấy.

## ngoai_pham_vi

| # | cố ý KHÔNG làm | lý do |
|---|---|---|
| 1 | **`t150`** | Packet **#552** sở hữu, lease `t150-do-r1-g1-antigravity` đã cấp — đẩy `15:33Z`, workflow `đăng lease bằng git` **success**, comment `5732323948` lúc `15:35:51Z 18-09`, body **khớp từng byte** với bản cục bộ (8412 byte). Write set rời hẳn. |
| 2 | **`t131`** — `OSError: [WinError 193] %1 is not a valid Win32 application` | Chạy thẳng một fixture `.sh`; fixture **chỉ-POSIX**. Thân hàm giống hệt `origin/master`. Không thuộc phép giải đường dẫn. |
| 3 | **`t132`** — `PermissionError: [WinError 5]` khi dọn `…\.git\objects\36\c0fe…` | Object của git là chỉ-đọc trên Windows nên dọn thư mục tạm thất bại. Fixture, không phải cổng. Thân hàm giống hệt master. |
| 4 | **`t35`–`t40`** — `rc=127`, `/bin/bash: …\ops\cai_actionlint.sh: No such file or directory`, `cygpath: command not found` | **CHƯA ĐO ĐƯỢC nguyên nhân** — xem `chua_do_duoc` mục 1. Thân hàm cả sáu giống hệt master. |
| 5 | **`t125`** — `LỆCH_CHƯA_RÕ_NGUYÊN_NHÂN`, A/B toàn suite `143/154` so `144/154`, ca lệch `t156` | **Chính ca ấy từ chối kết luận nguyên nhân.** Chập chờn hoặc phụ thuộc thứ tự/tải. Nó còn nằm trong vùng chồng lấn đã khai với lease `ci-windows-r2-g2-antigravity`. |
| 6 | `.github/workflows/**`, ruleset, manifest, credential | Issue #541 cấm nguyên văn |
| 7 | `ops/cong_cu.py` | Issue #541 khai write set `only` hai tệp |
| 8 | Bỏ hẳn bước 3 (PATH thật) | r2 đã khai đó là **quyết định của chủ kho**, không phải của executor. Chưa có chỉ thị đổi. |

## hinh_dang_ke_thua

**Packet khắc phục của chính mình** — g2 sửa những gì review tìm thấy ở g1. Ba doctrine đang áp,
khai ở đây để đừng tái phạm ngay trong bản vá sửa lỗi:

1. **"Vá đúng chỗ được chỉ rồi bỏ sót đường thứ ba."** Chính lượt 3 dính: đo bước 2 và bước 3 rất
   kỹ rồi kết luận cho **cả hàm**, trong khi bước 1 nằm ngay trên đó. `_git_windows` có **BA** bước
   = **BA** đường vào. M3–M6 phải được kiểm **trên cả ba bước**, không chỉ ở bước bị chỉ tên.
2. **"Đột biến bị giết không phải đột biến bị giết ĐÚNG LÝ DO."** N8–N12 mỗi ca neo **lý do**, không
   chỉ neo `rc`. `t136` là ca thật vừa bị bắt bằng đúng kỷ luật này.
3. **"Ghi một nguyên nhân sai vào doctrine còn tệ hơn không ghi gì."** §`t136` ở trên đính chính
   bảng chẩn đoán của r2 thay vì lặng lẽ sửa — vì người đọc r2 sẽ tưởng "14 ca PATH" là chuyện đã
   khép.

## chua_do_duoc

Nói thẳng, đừng làm tròn.

1. **Nguyên nhân `t35`–`t40`.** Chữ ký (`cygpath: command not found`, bash không hiểu `D:\…`) khớp
   **bash của WSL** chứ không phải Git-Bash. Giả thuyết ấy **chưa kiểm được**: lệnh kiểm đưa cho chủ
   kho là `where bash`, mà `where` trong PowerShell là **bí danh của `Where-Object`** nên nó trả 0
   dòng **kể cả trên máy chắc chắn có bash** (đã tái hiện trên pwsh 7.4.6). Phép đo hỏng, không phải
   kết quả. Lệnh đúng, và hỏi đúng thứ bộ test hỏi: `py -c "import shutil; print(shutil.which('bash'))"`.
2. **`t125` chập chờn.** Chưa ai biết nguyên nhân, kể cả chính ca ấy.
3. **Nền đo trên máy chủ kho.** Chưa có lượt chạy `origin/master` (chưa vá) trên chính máy ấy, nên
   câu *"bảy ca kia đỏ sẵn"* dựa vào **đối chiếu băm thân hàm với master**, không dựa vào một lượt
   nền. Đủ để loại trừ "do bản vá", **chưa đủ** để nói "chúng luôn đỏ ở đó".
4. **Hành vi Windows PowerShell 5.1 ở P3-2.** Container review chỉ có pwsh 7.4.6, và trên 7.4.6 dòng
   stderr ấy KHÔNG chí mạng. Nguyên nhân suy từ thông điệp khớp nguyên văn + vị trí trap, cộng phép
   đo cho thấy dòng ấy rò rỉ thật (72 byte → 0 byte sau khi bắt). M6 đóng cả hai khả năng nên không
   phụ thuộc vào việc suy ấy đúng hay sai.
5. **Registry Windows.** r2 nêu ở `muc_tieu` bước 2 *"và registry nếu đọc được"*; bản vá g1 **không**
   đọc registry. Chưa ai đo xem thiếu nó có làm hỏng máy nào không. Không mở phạm vi ở r3.
6. **`granted_on_instruction` của lease g1** trỏ vào Issue #541 chứ không vào một comment chỉ thị —
   chủ kho chưa đăng comment nào. Cổng **không cưỡng chế** trường này. Lease g2 thừa hưởng đúng chỗ
   trống ấy trừ khi chủ kho đăng comment trước khi cấp.

## Ràng buộc thi công

- **KHÔNG chạy CI Windows bằng tay** (`manual_ci_budget: 0`), không `workflow_dispatch`.
- **KHÔNG tự merge, tự approve, tự review.** Reviewer phải fresh-context, độc lập, khác phiên.
- **KHÔNG chạm tệp ngoài `write_set`**, kể cả sửa tạm rồi hoàn nguyên.
- **KHÔNG viết dấu bỏ-qua-CI nguyên văn trong thông điệp commit**, kể cả khi trích dẫn.
- **Đọc `rc` TRỰC TIẾP**, đừng qua pipe (`| tail` làm `rc` thành của `tail`).
- **`core.abbrev = 7`** khi chạy gate, kể cả trong sandbox reviewer.
- **Đột biến chạy trên BẢN SAO TẠM**, không bao giờ trên tệp thật.
- **Hoà `origin/master` bằng MERGE, không rebase** — `2f70869a` là `reviewed_sha` của bốn lượt.
- **Đo `--numstat` TRƯỚC khi mở review** (N6'). Vượt 400 ⇒ DỪNG và handoff.
