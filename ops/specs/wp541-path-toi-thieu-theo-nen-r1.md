# WP541 PATH-TOI-THIEU-THEO-NEN — revision 1 / generation 1

> ĐẶC TẢ ĐÓNG BĂNG. Đây KHÔNG phải lease và KHÔNG phải lệnh khởi động.
> Phải có Packet Issue + lease còn hiệu lực (`docs/PROTOCOL_DA_PHIEN.md` §3.2, §4) thì mới được bắt tay.
> Mọi con số dưới đây ghi kèm ĐƠN VỊ (L1) và THỜI ĐIỂM ĐO (L5). Đo lại trước mỗi bước công bố.

## packet_id · packet_issue

| trường | giá trị |
|---|---|
| `packet_id` | `WP541-PATH-TOI-THIEU-THEO-NEN` |
| `packet_issue` | **CHƯA CÓ** — chưa mở Issue tại thời điểm đóng băng spec này |
| `revision` / `generation` | 1 / 1 |
| `base_sha` | `a612c70cbc56d0e3a8c580f4759eddf215af82fb` (`origin/master`, đo **16:41Z 17-09-2026**) |
| `target_branch_neu_land` | `master` |

## nguon_cap_viec

**KHÔNG có dòng kế hoạch nào cấp việc này.** Đo **16:44Z 17-09-2026**: `grep -rn '541'
ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md` ⇒ **0 dòng** (đơn vị: dòng khớp trong tệp kế hoạch thi công).

Nguồn duy nhất trong kho nhắc tới packet này:

```
origin/ops/cap-lease-548:ops/leases/ci-windows-r1-g1-antigravity.yaml:113
    related_packets:
    - 546
    - 541      <-- dòng 113
    - 538
```

Ngoài dòng ấy, căn cứ là **phép đo trực tiếp** ghi ở mục `hien_trang_da_do` bên dưới. Một mô tả lỗi
đến phiên soạn spec qua kênh nền tự động KHÔNG phải nguồn cấp việc; nó đã được đo lại từng khẳng
định trước khi dùng, và những khẳng định không đo được thì nằm ở `chua_do_duoc`.

**Không phải packet khắc phục** của packet nào — xem `hinh_dang_ke_thua`.

## review_class

`sensitive` — **không hạ được**.

`docs/PROTOCOL_DA_PHIEN.md` §8 liệt kê `sensitive` gồm *"review/land authority"* và *"launcher hoặc
gate lifecycle"*. `ops/lease_publish.py` là cổng đăng/đọc lease, trúng cả hai. §8 còn ghi: *"Executor
không được hạ lớp. Path không biết, classifier lỗi hoặc bằng chứng không đọc được đều thành
`sensitive`."*

| trường | giá trị | căn cứ |
|---|---|---|
| `review_class` | `sensitive` | §8, đường dẫn bị chạm |
| `assurance_target` | `human_audited` | **đo 16:37Z 17-09-2026**: `doctor --kiem-song` **rc=12**; `codex` = `THIEU` (chưa cài CLI), `claude` = `CHUA_XAC_THUC`. `cross_approved` không mua được từ phiên này. |
| `prohibited_actions` | `self_review`, `self_approve`, `merge` | §8 |

Ghi rõ vì nó đã trôi so với #548: `launcher.py chuan-bi` **rc=0** lúc 16:26Z ĐÃ ghi được
`~/.codex/auth.json`, nhưng **CLI `codex` không có trên máy**. Credential sẵn cho một công cụ không
tồn tại — `ĐÃ ĐẶT ≠ DÙNG ĐƯỢC`, lùi thêm một tầng. Nếu tới lúc thi công mà `codex` đã cài VÀ
`--kiem-song` cho bằng chứng dương, được nâng lên `cross_approved`; **không được suy từ `chuan-bi`
rc=0**.

## write_set

Ba đường dẫn, liệt kê tường minh, không ký tự đại diện:

1. `ops/cong_cu.py`
2. `ops/lease_publish.py`
3. `ops/lease_publish_test.py`

Trần ADR-0044 cho `sensitive`: **≤ 3 tệp** và **≤ 300 dòng thêm** (`git diff --numstat`). Write set
này **kịch trần tệp** — phát sinh cần tệp thứ tư thì DỪNG, đi qua revision mới, không tự nới.

**Không cần ADR mới** (đo **16:41Z**): `docs/adr/0047-nguon-tin-cay-cho-cong-doc-lease.md` chỉ quy
định danh sách cấm biến `GIT_*` (`GIT_WORK_TREE`, `GIT_COMMON_DIR`, `GIT_EXEC_PATH`,
`GIT_SSL_NO_VERIFY`); nó **không** ghi cứng `/usr/bin:/bin` ở bất kỳ dòng nào. Hằng số ấy là lựa
chọn triển khai, không phải quyết định do ADR quản. `adr-song --root .` **rc=0** lúc 16:41Z.
`ADR-0049` đã bị #548 đặt chỗ — đừng dùng số ấy.

### Trạng thái lease của từng đường (đo 16:41Z 17-09-2026)

| đường dẫn | `ai-dang-giu` rc | người giữ |
|---|---|---|
| `ops/cong_cu.py` | 0 | **0** — rảnh |
| `ops/lease_publish.py` | 0 | **0** — rảnh |
| `ops/lease_publish_test.py` | 11 | **1: `ci-windows-r1-g1-antigravity`** (packet #548), `lease_expires_at_utc: 2026-09-17T18:55:00Z` |

Chốt so hai nguồn ref chạy TRƯỚC mọi phép quét lease trên (đo 16:12Z): `ls-remote --heads` **417**
tên nhánh, `for-each-ref refs/remotes/origin` **417** tên nhánh, `comm -23` **rỗng** ⇒ không mù.

### DIEU_KIEN_CAP_LEASE

- **Xếp SAU #548 trên `ops/lease_publish_test.py`.** Lease #548 đang giữ đúng tệp này, VÀ cấm tường
  minh `ops/lease_publish.py` trong `khong_duoc_cham` — hai packet cài răng lược, không trùng ngẫu
  nhiên. Cấp lease WP541 trước khi #548 nhả là tự tạo cửa sổ hai writer.
- **Quét lại `ai-dang-giu` cho CẢ BA đường ngay trước khi cấp**, và chốt `comm -23` phải rỗng. Các
  con số ở bảng trên sẽ trôi; chúng để đối chiếu, không để quyết định. **Không đo lại thì không cấp.**
- **"Hết hạn" KHÔNG phải "đã nhả"** — lease gia hạn được. Đọc `da_bi_thay_the` và tìm hiện vật của
  #548 trên master, đừng suy từ mốc 18:55Z.

## ngoai_pham_vi

Bốn mục CỐ Ý không làm:

1. **Không chạm `.github/workflows/ci.yml`.** #548 sở hữu đường này trong `write_set` của nó.
2. **Không sửa `_bash_windows` trong `ops/cong_cu.py`** dù cùng lớp lỗi (giải công cụ POSIX trên
   Windows). Nó đang chạy đúng; gộp vào đây là mở rộng diff của một packet `sensitive` kịch trần.
   Cần thì mở packet riêng.
3. **Không quét/sửa hằng số PATH kiểu POSIX ở tệp khác.** Đã ĐO, không phải giả định: **16:28Z
   17-09-2026**, `grep -rn '"/usr/bin:/bin"' --include='*.py' .` ⇒ **1 dòng** (đơn vị: dòng mã khớp
   chuỗi nguyên văn, toàn kho) — `ops/lease_publish.py:1106`. Ghi phép đo này ra đây để lượt sau
   không phải đoán lại.
4. **Không đổi 15 ca `t129…t151`.** Chúng là chỉ báo hồi quy, không phải tiêu chí nghiệm thu — lý do
   ở `nghiem_thu` mục N0.

## hien_trang_da_do

Mọi dòng dưới đây là phép đo của phiên soạn spec, trên `a612c70cbc56`.

**Mã (đo 16:28–16:29Z 17-09-2026):**

```python
# ops/lease_publish.py:1103-1110
def _git_exe_toi_thieu() -> str:
    """Executable `git` giải MỘT lần bằng đường tuyệt đối trong PATH tối thiểu (Q4.1)."""
    import shutil
    duong = shutil.which("git", path="/usr/bin:/bin")      # <-- 1106
    if not duong:
        raise Chan(RC_KHONG_XAC_DINH, "KHÔNG_XÁC_ĐỊNH: không thấy `git` trong PATH tối thiểu /usr/bin:/bin")
    return str(Path(duong).resolve())
```

- Nơi gọi `_git_exe_toi_thieu()`: **3** (đơn vị: dòng gọi trong `ops/lease_publish.py`) —
  `hoso_adapter_do:1156` · `kham_pha_nguon:1218` · `__init__:1298`. Cộng **1** trong tệp test (`:4998`).
- Hợp đồng hạ nguồn: `_env_rong(git_exe, …)` đặt `"PATH": str(Path(git_exe).parent)` — tức đường dẫn
  giải được ở 1106 trở thành **TOÀN BỘ PATH của tiến trình con**. Đây là lý do hàm phải trả đường
  TUYỆT ĐỐI và không được tin PATH của người gọi.
- Tổng ca trong `ops/lease_publish_test.py`: **150** (đơn vị: hàm `def tNNN_` ở mức module).

**Nền Windows thật của chủ kho (đo 17-09-2026, PowerShell 7, `D:\thu546`, Python 3):**

| chốt | kết quả |
|---|---|
| `shutil.which("git")` | `C:\Program Files\Git\cmd\git.EXE` — git CÓ mặt |
| `shutil.which("git", path="/usr/bin:/bin")` | **`None`** — cùng cái git ấy, PATH tối thiểu không thấy |
| `os.pathsep` | `';'` ⇒ `"/usr/bin:/bin".split(';')` cho **1** mục rác, không tách |
| `os.path.isdir("/usr/bin:/bin")` | `False` |
| `PATHEXT` | `.COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH;.MSC;.PY;.PYW;.CPL` ⇒ tên trần `git` KHÔNG bao giờ được probe |
| `os.defpath` | `'.;C:\bin'`; `which("git", path=os.defpath)` ⇒ **`None`** |

**Ba nguyên nhân ĐỘC LẬP, mỗi cái tự đủ** (đọc từ `shutil.which`, Python 3.11): dấu phân cách sai ·
thư mục không tồn tại · PATHEXT. Trên Windows thật chúng nổ CÙNG LÚC nên **không phân biệt được bằng
đầu vào** ⇒ chúng là một bộ TƯƠNG ĐƯƠNG, và spec này chỉ đặt **một** chốt cho cả ba (N1).

**`os.defpath` đã bị LOẠI khỏi danh sách ứng viên** — đo, không suy: nó dẫn đầu bằng `.` (cwd) và
`C:\bin` gần như không tồn tại trên runner. Dùng nó là đổi một cái đỏ ồn ào lấy một cái im lặng.

## muc_tieu

Mỗi mục chiếu vào ĐÚNG MỘT đường dẫn trong `write_set` (L2).

| # | mục tiêu | đường dẫn |
|---|---|---|
| **M1** | Thêm `_git_windows(path=None, system_root=None, program_files=None, cwd=None)` vào `ops/cong_cu.py`, đặt cạnh `_bash_windows` và theo ĐÚNG khuôn của nó: danh sách ứng viên có thứ tự, loại trừ theo VỊ TRÍ, tham số tiêm để test lái được. | `ops/cong_cu.py` |
| **M2** | Sửa `_git_exe_toi_thieu` tại `ops/lease_publish.py:1103-1110`: chọn PATH tối thiểu **THEO NỀN** thay cho hằng số, uỷ quyền nhánh Windows cho `M1`, giữ nguyên `Chan(RC_KHONG_XAC_DINH)` khi trượt hết, giữ nguyên hợp đồng "trả đường TUYỆT ĐỐI đã resolve". Nhận tham số tiêm (`*, nen=None, **tiem`) để test lái. | `ops/lease_publish.py` |
| **M3** | Thêm **≥3** ca `rXX_` mới đo thẳng phép giải đường dẫn, chạy được trên `ubuntu-latest`, cộng đột biến cho từng ca. | `ops/lease_publish_test.py` |

### Thứ tự ứng viên cho M1 (Windows)

1. `CONG_CU_GIT` — biến môi trường tường minh, nếu có.
2. **Thư mục cài Git phân giải từ `%ProgramFiles%`** (và registry nếu đọc được).
3. `shutil.which("git")` trên PATH thật — **đường CHÓT**, không phải đường đầu.

Ở **mọi** bước: loại ứng viên nằm trong **cwd**, loại ứng viên nằm dưới **`%SystemRoot%`**. Trượt hết
⇒ `Chan(RC_KHONG_XAC_DINH)`.

**Vì sao bước 3 xuống chót, nói thẳng cái đánh đổi:** PATH thật là đúng thứ hằng số gốc sinh ra để
KHÔNG tin. Để nó ở đầu là nới lỏng chính bất biến đang bảo vệ. Để nó ở chót vẫn là một cửa nới —
nên nó phải có chốt riêng (N3), và nếu bước 2 không phân giải được thì **không im lặng rơi xuống**:
ghi `KHÔNG_ĐO_ĐƯỢC` vào chẩn đoán rồi mới thử bước 3 (ba trạng thái, doctrine `None ≠ False`).

**POSIX giữ nguyên `/usr/bin:/bin`.** Nó đang đúng; đổi nó là mở rủi ro không mua được gì.

## nghiem_thu

Mỗi tiêu chí nêu PHÉP ĐO LÀM NÓ ĐỎ (L3). Tiêu chí không thể đỏ thì không phải tiêu chí.

**N0 — 15 ca `t129…t151` KHÔNG phải tiêu chí nghiệm thu.** Lý do, đã đo **16:33Z**: tên đầy đủ của
chúng là `t129_Q45_reader_object_store_bam_lai_va_canh_tu_bytes`,
`t130_S2_seam_bytes_lech_OID_12_va_parser_KHONG_nhan_byte`,
`t139_A12_catalog_mutant_A0_giet_dung_ly_do_va_ghi_SONG_kem_seam`, … — **không ca nào nói về PATH**.
Cả 15 là hạ nguồn của `_git_exe_toi_thieu` qua ba nơi gọi, chết vì `Chan` ném lên từ preflight TRƯỚC
khi ca kịp đo thứ nó sinh ra để đo. Vá hằng số ⇒ chúng xanh vì *"git tìm được"*, không vì *"PATH tối
thiểu đúng"*. Đó đúng là **tín dụng giả** mà kho đã trả giá hai lần — và `t139` mang sẵn tên
`mutant_A0_giet_dung_ly_do`, tức chính ca dựng lên để chống tín dụng giả đang là nạn nhân của nó.
Chúng vào spec với tư cách **chỉ báo hồi quy**, không phải tiêu chí.

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| **N1** | Nền Windows giả, KHÔNG ứng viên hợp lệ nào ⇒ `_git_exe_toi_thieu` ném `Chan(RC_KHONG_XAC_DINH)`; nền Windows giả CÓ `%ProgramFiles%\Git\cmd\git.exe` ⇒ trả đúng đường ấy, tuyệt đối, đã resolve. | **Đột biến:** quay bước giải Windows về hằng số `"/usr/bin:/bin"` ⇒ ca N1 phải ĐỎ. Đây là chốt cho bộ TƯƠNG ĐƯƠNG ba nguyên nhân (separator · thư mục vắng · PATHEXT) — chúng không tách được bằng đầu vào nên chỉ đặt MỘT chốt, và spec khai thẳng như vậy thay vì giả vờ có ba. |
| **N2** | Nền Windows giả, `cwd` chứa `git.bat` (và một biến thể `git.py`, vì `PATHEXT` đo được trên máy chủ kho có `.PY`) ⇒ kết quả **KHÔNG** trỏ vào cwd. | **Đột biến:** gỡ phép loại-trừ-cwd ⇒ ca N2 phải ĐỎ. Chốt này đo **chế độ hỏng THỨ HAI**: nhánh `win32` của `shutil.which` tự `path.insert(0, os.curdir)`, nên PATH "tối thiểu" tự nhận cwd — đúng cái nó sinh ra để chặn. Phân biệt được với N1 bằng đầu vào (cwd sạch ⇔ cwd có `git.*`) ⇒ **không** thuộc bộ tương đương của N1. |
| **N3** | Ứng viên nằm dưới `%SystemRoot%` bị loại; và khi bước `%ProgramFiles%` không phân giải, chẩn đoán ghi `KHÔNG_ĐO_ĐƯỢC` chứ không im lặng rơi xuống bước 3. | **Đột biến:** (a) gỡ phép loại `%SystemRoot%` ⇒ ĐỎ; (b) đổi nhánh "không phân giải được" thành rơi thẳng xuống bước 3 không ghi gì ⇒ ĐỎ. Hai đột biến vì đây là hai cửa khác nhau trên cùng một bước. |
| **N4** | POSIX không hồi quy: trên `ubuntu-latest`, `_git_exe_toi_thieu()` vẫn trả `/usr/bin/git`. | **Đột biến:** đổi nhánh POSIX sang một hằng số khác ⇒ ĐỎ. |
| **N5** | *(chỉ báo hồi quy, KHÔNG phải tiêu chí)* `ops/lease_publish_test.py` đạt **150/150** trên `ubuntu-latest` (đơn vị: ca `def tNNN_`, đo nền 16:29Z = 150 ca tồn tại). Delta so `origin/master` = 0. | Nếu đỏ thì đó là hồi quy do bản vá — nhưng N5 XANH **không** chứng minh mục tiêu nào. |
| **N6** | `git diff --numstat` so `a612c70cbc56`: ≤ **3** tệp và ≤ **300** dòng thêm (đơn vị: tệp / dòng thêm, theo ADR-0044 cho `sensitive`). | Vượt một trong hai ⇒ DỪNG, handoff, không tự nới. |

**N7 — xác nhận trên Windows thật, KHÔNG phải phép đo nghiệm thu.** Một lượt chạy trên máy Windows
của chủ kho, bằng script TỰ CHỨNG MINH đột biến đã áp (đếm dòng khớp hằng số: **trước = 1, sau = 0**)
và fail-close khi nền đo sai (không phải `win32`, hoặc `git` không có trong PATH thường ⇒
`KHÔNG_XÁC_ĐỊNH`, rc≠0, KHÔNG được đọc thành "đã chứng minh").

**Vì sao nghiệm thu KHÔNG neo vào `gate (windows-latest)`:** packet #548 làm `gate` thôi chạy Windows
khi push master. Nếu #548 land trước, cái đỏ của WP541 **biến mất khỏi CI** — không phải vì được
chữa, mà vì cổng không còn chạy. Kho có bài học riêng cho đúng chuyện này: *"cổng không nói dối — nó
VẮNG MẶT, và trên giao diện 'xanh' với 'không chạy' nhìn giống hệt nhau."* N1–N4 chạy trên
`ubuntu-latest` bằng tham số tiêm, nên chúng đo **hành vi giải đường dẫn theo nền** mà không cần nền
đó — WP541 vì thế miễn nhiễm với việc #548 land sớm hay muộn, và không phụ thuộc `manual_ci_budget`.

## hinh_dang_ke_thua

`khong_ap_dung` — WP541 **không phải packet khắc phục** của packet nào. Nó không kế thừa bộ đếm hình
dạng lỗi từ biên nhận tiền nhiệm vì không có tiền nhiệm: lỗi được phát hiện bằng phép đo trực tiếp
trên `a612c70cbc56`, không phải từ một lượt thi công trước đó bị bác.

Ghi kèm một doctrine ĐANG áp, không phải bộ đếm kế thừa: bài học **#513 lượt 10→13** (*"vá đúng chỗ
được chỉ rồi bỏ sót đường thứ ba"*) trực tiếp áp cho packet này, vì `_git_exe_toi_thieu` có **3** nơi
gọi và phép giải có **3** bước ứng viên. Vì thế `nghiem_thu` đã tự liệt kê HẾT các đường TRƯỚC và
cho mỗi đường một chốt riêng (N1 · N2 · N3a · N3b), và khai thẳng chỗ nào là bộ TƯƠNG ĐƯƠNG (ba
nguyên nhân trong N1) thay vì đếm chúng thành ba chốt.

## chua_do_duoc

Ghi thẳng, không giấu sau chữ "có thể":

1. **Hành vi `%ProgramFiles%` / registry trên runner `windows-latest` của GitHub.** Chưa ai đo.
   `manual_ci_budget: 0` nên phiên này không gọi được CI Windows, và **máy Windows của chủ kho KHÔNG
   thay thế được phép đo đó** — nó là máy khác, cấu hình khác. Đây là rủi ro đã biết của M1 bước 2;
   N3 fail-close chính là để nó hỏng ồn ào thay vì im lặng.
2. **Chế độ hỏng thứ hai (cwd chiếm quyền) chưa có phép đo trên Windows thật.** Nó suy từ mã nguồn
   `shutil.which` (nhánh `win32` `path.insert(0, os.curdir)`) — đã đọc, chưa chạy. Probe dựng sẵn để
   đo nó chưa chạy được (tệp bị lưu nhầm phần mở rộng `.bat`). N2 đo nó bằng nền GIẢ trên Linux, đủ
   để khoá hành vi, **không** đủ để khẳng định ca thật trên Windows.
3. **Kích thước diff thật.** Chưa có bản vá nên `--numstat` chưa chạy. Ước lượng ~20–30 dòng ở
   `lease_publish.py` + ~30–50 ở `cong_cu.py` + ~60–90 ở test — **là ước lượng, không phải phép đo**.
   N6 là chốt thật.
4. **Trạng thái PR #550 / packet #548 lúc đọc spec này.** Con số `18:55:00Z` đọc từ tệp lease lúc
   16:41Z; trạng thái PR đọc từ bản ghi phiên khác, KHÔNG phải phiên này đo. Phải đo lại trước khi
   cấp lease.
5. **`15` ca ĐỎ và `133/148 đạt; đã chạy=148, bỏ qua=7`** — những con số này đến từ log CI job
   `105238582317` (run `35232106589`), **phiên soạn spec KHÔNG đọc log ấy**. Thứ phiên này đo được là:
   cả 15 tên ca **tồn tại** trong tệp test (16:29Z), và tổng ca là **150** (16:29Z). Chênh `150` với
   `148` chưa được giải thích bằng phép đo — đừng dùng `148` như một con số đã kiểm.

## Ràng buộc thi công

- **KHÔNG chạy CI Windows bằng tay** (`manual_ci_budget: 0`): không `workflow_dispatch`, không gọi
  lane `windows`.
- **KHÔNG tự merge, tự approve, tự review.** Cross-review phải là phiên khác, checkout khác,
  context khác.
- **KHÔNG chạm tệp ngoài `write_set`.**
- **KHÔNG viết dấu bỏ-qua-CI nguyên văn trong thông điệp commit**, kể cả khi trích dẫn (viết tách
  chữ hoặc mô tả bằng lời — GitHub khớp CHUỖI trên toàn thông điệp, dấu nháy ngược không phải hàng rào).
- **Đọc `rc` TRỰC TIẾP**, đừng qua pipe.
- **`core.abbrev = 7`** khi chạy gate, kể cả trong sandbox reviewer.
