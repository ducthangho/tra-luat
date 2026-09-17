# WP541 WINDOWS-LEASE-PUBLISH — spec r2 (packet revision 1 / generation 1)

> ĐẶC TẢ ĐÓNG BĂNG. KHÔNG phải lease, KHÔNG cấp việc. Phải có lease còn hiệu lực
> (`docs/PROTOCOL_DA_PHIEN.md` §3.2, §4) thì mới được bắt tay.
>
> **`r2` thay `r1` (`28ebf711…`, nhánh `claude/spec-541-r1-20260917`).** `r1` soạn khi chưa đọc
> Issue #541 và lệch nó ba chỗ: write set 3 tệp thay vì 2; executor `human_audited` thay vì
> `gpt-6-astra`; và quy CẢ 15 ca đỏ về một nguyên nhân. Issue #541 cảnh báo đúng điều thứ ba và
> điểm danh đích danh `t150`. Đo lại từ log CI: **14 ca do PATH, 1 ca (`t150`) KHÁC**. `r1` sai,
> không phải chật. `r1` giữ nguyên làm dấu vết, không sửa đè (§5 skill `soan-spec`).
>
> Mọi con số ghi kèm ĐƠN VỊ (L1) và THỜI ĐIỂM ĐO (L5).

## packet_id · packet_issue

| trường | giá trị |
|---|---|
| `packet_id` | `WP541-WINDOWS-LEASE-PUBLISH` |
| `packet_issue` | **541** — `WINDOWS-LEASE-PUBLISH — Git cô lập native Windows, unblock #540/#538`, `open`, **0** comment (đơn vị: comment trên Issue), tạo `2026-09-15T05:23:19Z`, đo `17:02Z 17-09-2026` |
| `revision` / `generation` | **1 / 1** — Issue khai `Revision1/generation1`. Chưa lease nào từng cấp cho packet này, nên §3.2 không buộc tăng revision; `r1`→`r2` là revision của **tệp spec**, không phải của packet. |
| `mission_issue` | `KHONG_CO` |
| `base_sha` | `a612c70cbc56d0e3a8c580f4759eddf215af82fb` (`origin/master`, đo 16:41Z 17-09-2026) |
| `depends_on` | `#540` (`open`, đo 17:02Z) · `#538` (`open`, đo 17:02Z) |

## nguon_cap_viec

**Issue #541, thân issue** — chủ kho cấp phép tường minh, nguyên văn trong đó:

> *"Owner's explicit answer in the current Codex task: 'Cấp thêm packet/lease riêng; giữ review
> high → xhigh và các gate.'"*

`ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md` **không có dòng nào** cho packet này (đo 16:44Z, đơn vị:
dòng khớp `541`) — nguồn cấp việc là Issue, không phải bảng kế hoạch.

**Không phải packet khắc phục** — xem `hinh_dang_ke_thua`.

## review_class

| trường | giá trị | căn cứ |
|---|---|---|
| `risk` / `review_class` | `sensitive` | §8 liệt kê *"review/land authority"* và *"gate lifecycle"*; `ops/lease_publish.py` trúng cả hai. Không hạ được. |
| `executor` | **Codex `gpt-6-astra` / high** | Issue #541 chỉ định |
| `reviewer` | **`gpt-6-astra` / xhigh**, fresh-context độc lập | Issue #541 chỉ định |
| `assurance_target` | `cross_approved` theo Issue | — |
| `environment` | `local` (Windows) | Issue: *"native Windows"* |
| `prohibited_actions` | `self_review`, `self_approve`, `merge` | §8 |

**Phiên soạn spec này KHÔNG dựng được đường executor ấy** — đo `16:37Z 17-09-2026`:
`launcher.py doctor --kiem-song` **rc=12**; `codex` = `THIEU` (CLI chưa cài), `claude` =
`CHUA_XAC_THUC`. `launcher.py chuan-bi` rc=0 lúc 16:26Z ĐÃ ghi `~/.codex/auth.json`, nhưng
credential sẵn cho một công cụ không tồn tại. **Đừng suy "codex dùng được" từ `chuan-bi` rc=0.**
Người cấp lease phải tự đo lại trên máy sẽ chạy executor.

## write_set

Hai đường dẫn. Issue #541 nguyên văn: *"Planned product write set: `ops/lease_publish.py` and
`ops/lease_publish_test.py` **only**"*.

1. `ops/lease_publish.py`
2. `ops/lease_publish_test.py`

Trần ADR-0044 cho `sensitive`: **≤ 3 tệp**, **≤ 300 dòng thêm**. Write set này **2 tệp** — còn dư
một tệp so với trần, nhưng Issue nói `only`, nên **dư ấy không được tiêu**. Cần tệp thứ ba ⇒ DỪNG,
handoff, hỏi chủ kho.

**Hệ quả đã biết, ghi thẳng:** `ops/cong_cu.py` có sẵn `_bash_windows()` (dòng 63) — tiền lệ giải
công cụ POSIX trên Windows bằng danh sách ứng viên có thứ tự + loại trừ theo vị trí + bốn tham số
tiêm để test lái. `r1` định đặt `_git_windows` cạnh nó để dùng chung. Issue chặn đường đó. `r2`
đặt hàm mới **trong `ops/lease_publish.py`**, và chấp nhận **rủi ro hai bản trôi lệch** — cùng lớp
rủi ro mà CLAUDE.md ghi cho `pkg_secret_scan.py` (*"hai bản sẽ trôi lệch, và bên quên cập nhật
chính là bên đẩy lọt"*). Nợ này khai ở `chua_do_duoc` mục 4, không giấu.

**Không cần ADR mới** (đo 16:41Z): `docs/adr/0047-*.md` chỉ quy định danh sách cấm biến `GIT_*`,
không ghi cứng `/usr/bin:/bin` dòng nào. `adr-song --root .` rc=0. `ADR-0049` đã bị #548 đặt chỗ.

### Trạng thái lease (đo 16:41Z 17-09-2026 — SẼ TRÔI, phải quét lại)

| đường dẫn | `ai-dang-giu` rc | người giữ |
|---|---|---|
| `ops/lease_publish.py` | 0 | **0** — rảnh |
| `ops/lease_publish_test.py` | 11 | **1: `ci-windows-r1-g1-antigravity`** (#548), `lease_expires_at_utc: 2026-09-17T18:55:00Z` |

Chốt so hai nguồn ref chạy TRƯỚC (đo 16:12Z): máy chủ **417** tên nhánh, đệm cục bộ **417**,
`comm -23` **rỗng** ⇒ không mù.

### DIEU_KIEN_CAP_LEASE

- **Xếp SAU #548** trên `ops/lease_publish_test.py`. Lease #548 giữ đúng tệp này VÀ liệt
  `ops/lease_publish.py` trong `khong_duoc_cham` — hai packet cài răng lược, có chủ ý.
- Issue #541: *"spec+lease will be frozen against exact state after WP540's independent review,
  before this executor starts."* **#540 đang `open`** (đo 17:02Z) ⇒ điều kiện này **CHƯA THOẢ**.
- **Quét lại `ai-dang-giu` cả hai đường ngay trước khi cấp**, và `comm -23` phải rỗng. Số ở bảng
  trên để đối chiếu, không để quyết định. Không đo lại thì không cấp.
- **"Hết hạn" KHÔNG phải "đã nhả"** — lease gia hạn được; đọc `da_bi_thay_the` và tìm hiện vật của
  #548 trên master.

## hien_trang_da_do

### Nguồn đo

Log job CI tải qua REST lúc **17:00Z 17-09-2026**: run `35232106589`, job `105238582317`,
`gate (windows-latest)`, `conclusion: failure`. **296 402** byte, **2 546** dòng (đơn vị: byte /
dòng của log job). Metadata job xác nhận **đúng MỘT** bước đỏ (đơn vị: bước có
`conclusion != success|skipped`): **#18 `lease-publish selftest (đo lại setup sau G5)`**.

Dòng tổng kết trong log, nguyên văn: `lease_publish: 133/148 đạt; đã chạy=148, bỏ qua=7`.

> `r1` khai *"chênh giữa 150 ca đo được và 148 trong log chưa giải thích được"*. Vẫn CHƯA giải
> thích — xem `chua_do_duoc` mục 2. Đừng dùng `148` như con số đã kiểm.

### Mã (đo 16:28–16:29Z 17-09-2026)

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

- Hằng số `"/usr/bin:/bin"`: **1** lần xuất hiện toàn kho (đơn vị: dòng `*.py` khớp chuỗi nguyên văn).
- Nơi gọi `_git_exe_toi_thieu()`: **3** trong `ops/lease_publish.py` — `hoso_adapter_do:1156` ·
  `kham_pha_nguon:1218` · `__init__:1298`; cộng **1** trong tệp test (`:4998`).
- Hợp đồng hạ nguồn: `_env_rong(git_exe, …)` đặt `"PATH": str(Path(git_exe).parent)` — đường giải
  ở 1106 trở thành **TOÀN BỘ PATH của tiến trình con**. Đây là lý do hàm phải trả đường TUYỆT ĐỐI
  và **không được tin PATH của người gọi**.

### CHẨN ĐOÁN RIÊNG TỪNG CA — đo từ log, không suy từ đồ thị lời gọi

Issue #541: *"Preserve distinct case diagnoses, including t150, rather than declaring every failure
solved by that hypothesis."* Đã làm. **15/15** ca có dòng `!!! do` trong log (đơn vị: ca đỏ có dòng
chẩn đoán). Phân loại bằng máy, khớp mẫu `không thấy 'git' trong PATH tối thiểu` hoặc `/usr/bin`:

| ca | lớp | lý do nguyên văn trong log (rút gọn) |
|---|---|---|
| `t129` | **PATH** | `Chan: KHÔNG_XÁC_ĐỊNH: không thấy 'git' trong PATH tối thiểu /usr/bin:/bin` |
| `t130` | **PATH** | như trên |
| `t131` | **PATH** | như trên |
| `t132` | **PATH** | `kho shallow phải 12: 12 KHÔNG_XÁC_ĐỊNH: không thấy 'git' trong PATH tối thiểu…` |
| `t133` | **PATH** | `H sạch phải 0: 12 '' 'CHAN [12]: … không thấy 'git' trong PATH tối thiểu…'` |
| `t136` | **PATH** | `Chan: KHÔNG_XÁC_ĐỊNH: … PATH tối thiểu /usr/bin:/bin` |
| `t138` | **PATH** | `12 'CHAN [12]: … PATH tối thiểu /usr/bin:/bin\n'` |
| `t139` | **PATH** | `mutant chết vì lỗi VÔ CAN (tín dụng giả): ['S2-bo-bam-lai: Chan: … PATH tối thiểu…']` |
| `t144` | **PATH** | `Chan: KHÔNG_XÁC_ĐỊNH: … PATH tối thiểu /usr/bin:/bin` |
| `t145` | **PATH** | như trên |
| `t146` | **PATH** | như trên |
| `t147` | **PATH** | `ngày hỏng date-revoke: đợi 8, được 12: '' 'CHAN [12]: … PATH tối thiểu…'` |
| `t149` | **PATH** | `Chan: KHÔNG_XÁC_ĐỊNH: … PATH tối thiểu /usr/bin:/bin` |
| **`t150`** | **KHÁC** | `policy không phải UTF-8 phải 12, không traceback: 12 'e\nCHAN [12]: KHÔNG_XÁC_ĐỊNH: ops/thu-hoi/_ngoai-le-closure.retired.yaml có mặt tại refs/heads/meta-pol-hong mà policy .github/coordination/change-impact.v1.json vắng hoặc không phải JSON object (Q13)\n'` |
| `t151` | **PATH** | `M4: ops=blob phải 12, không được kết luận sổ rỗng: 12 '' 'CHAN [12]: … PATH tối thiểu…'` |

**Tổng: 14 PATH · 1 KHÁC.**

Chốt phủ định cho `t150`, đo riêng: hai dòng `!!! do t150_*` trong log, **`'PATH tối thiểu'` →
False**, **`'/usr/bin'` → False**. `t150` nhận đúng `rc=12` như nó đợi, nhưng **thông điệp khác**:
nó đợi nhánh "policy không phải UTF-8", thực tế nhận nhánh "policy vắng hoặc không phải JSON
object (Q13)". Đây là hỏng **độc lập**, không phải hạ nguồn của `_git_exe_toi_thieu`.

`t139` đáng đọc kỹ: nó tự khai `mutant chết vì lỗi VÔ CAN (tín dụng giả)` — tức chính ca kho dựng
lên để chống tín dụng giả đang BÁO CÁO rằng nó đang bị tín dụng giả. Nó làm đúng việc.

### Nền Windows thật của chủ kho (đo 17-09-2026, PowerShell 7, Python 3)

| chốt | kết quả |
|---|---|
| `shutil.which("git")` | `C:\Program Files\Git\cmd\git.EXE` — git CÓ mặt |
| `shutil.which("git", path="/usr/bin:/bin")` | **`None`** |
| `os.pathsep` | `';'` ⇒ chuỗi **không tách**, cho **1** mục rác |
| `os.path.isdir("/usr/bin:/bin")` | `False` |
| `PATHEXT` | `.COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH;.MSC;.PY;.PYW;.CPL` ⇒ tên trần `git` KHÔNG bao giờ được probe |
| `os.defpath` | `'.;C:\bin'`; `which("git", path=os.defpath)` ⇒ **`None`** |

**Ba nguyên nhân ĐỘC LẬP, mỗi cái tự đủ** (đọc từ `shutil.which`, CPython 3.11): dấu phân cách sai ·
thư mục không tồn tại · PATHEXT. Trên Windows thật chúng nổ CÙNG LÚC ⇒ **không phân biệt được bằng
đầu vào** ⇒ là một bộ TƯƠNG ĐƯƠNG, đặt **một** chốt (N1), không giả vờ có ba.

`os.defpath` **đã bị LOẠI** khỏi danh sách ứng viên — đo, không suy: nó dẫn đầu bằng `.` (cwd) và
`C:\bin` gần như không tồn tại trên runner.

## muc_tieu

Mỗi mục chiếu vào ĐÚNG MỘT đường dẫn trong `write_set` (L2).

| # | mục tiêu | đường dẫn |
|---|---|---|
| **M1** | Thay hằng số ở `ops/lease_publish.py:1106` bằng phép giải **THEO NỀN**. Thêm `_git_windows(path=None, system_root=None, program_files=None, cwd=None)` **trong chính tệp này**, theo khuôn `_bash_windows` của `ops/cong_cu.py` (danh sách ứng viên có thứ tự, loại trừ theo VỊ TRÍ, tham số tiêm để test lái). `_git_exe_toi_thieu(*, nen=None, **tiem)` nhận tham số tiêm. Giữ nguyên `Chan(RC_KHONG_XAC_DINH)` khi trượt hết và hợp đồng "trả đường TUYỆT ĐỐI đã resolve". | `ops/lease_publish.py` |
| **M2** | Thêm **≥4** ca `rXX_` mới đo thẳng phép giải, chạy được trên `ubuntu-latest`, mỗi ca kèm đột biến đổi màu riêng. | `ops/lease_publish_test.py` |

### Thứ tự ứng viên cho M1 (Windows)

1. `CONG_CU_GIT` — biến môi trường tường minh, nếu có.
2. Thư mục cài Git phân giải từ `%ProgramFiles%` (và registry nếu đọc được).
3. `shutil.which("git")` trên PATH thật — **đường CHÓT**.

Ở **mọi** bước: loại ứng viên nằm trong **cwd**, loại ứng viên nằm dưới **`%SystemRoot%`**. Trượt
hết ⇒ `Chan(RC_KHONG_XAC_DINH)`. **POSIX giữ nguyên `/usr/bin:/bin`** — nó đang đúng.

**Ràng buộc của Issue #541 áp thẳng vào đây**, nguyên văn: *"Do not replace fixed trusted resolution
with unrestricted inherited PATH"*. Bước 3 **KHÔNG phải** PATH thừa kế không giới hạn: nó đứng chót,
và bị lọc bởi cùng hai phép loại trừ (cwd, `%SystemRoot%`). Nói thẳng cái đánh đổi: nó **vẫn là một
cửa nới** so với hằng số cũ, nên nó phải có chốt riêng (N3). Nếu người giữ kho thấy bước 3 vi phạm
tinh thần câu trên thì **bỏ hẳn bước 3** và chấp nhận `RC_KHONG_XAC_DINH` khi Git cài ngoài
`%ProgramFiles%` — quyết định ấy là của chủ kho, không phải của executor.

Giữ nguyên, theo Issue: closed-world environment · absolute Git pinning · repository-config
distrust · object-store/ancestry/receipt checks · raw evidence · fail-closed distinctions.
Không disable mutant, không skip Windows, không weaken reason check, không relax security policy.
Không đụng workflow/ruleset/manifest/credential.

## ngoai_pham_vi

| # | cố ý KHÔNG làm | lý do |
|---|---|---|
| 1 | **`t150`** — không sửa, không tính vào nghiệm thu | **Đo được** (17:00Z): nguyên nhân KHÁC, không chứa `PATH tối thiểu` hay `/usr/bin`. Nó đợi nhánh "policy không phải UTF-8" mà nhận nhánh "policy vắng hoặc không phải JSON object (Q13)". Gộp vào WP541 là cấp **tín dụng giả** cho một ca không được chữa — đúng điều Issue #541 cấm. Cần packet riêng. |
| 2 | `.github/workflows/ci.yml` | #548 sở hữu trong `write_set` của nó; Issue #541 cũng cấm *"no workflow… changes"* |
| 3 | `ops/cong_cu.py`, gồm cả `_bash_windows` | Issue #541 khai write set `only` hai tệp |
| 4 | Không quét/sửa hằng số PATH kiểu POSIX ở tệp khác | **Đo 16:28Z**: hằng số xuất hiện **1** lần toàn kho (đơn vị: dòng `*.py` khớp chuỗi nguyên văn) |
| 5 | Không đổi 14 ca PATH hiện có | Chúng là chỉ báo hồi quy, không phải tiêu chí — xem N0 |

## nghiem_thu

Mỗi tiêu chí nêu PHÉP ĐO LÀM NÓ ĐỎ (L3).

**N0 — 14 ca PATH KHÔNG phải tiêu chí nghiệm thu.** Chúng chết vì `Chan` ném từ preflight TRƯỚC khi
kịp đo thứ chúng sinh ra để đo (đã đo: lý do nguyên văn của cả 14 chứa `PATH tối thiểu`). Vá hằng số
⇒ chúng xanh vì *"git tìm được"*, không vì *"PATH tối thiểu đúng"*. Vào spec với tư cách **chỉ báo
hồi quy**. Tiêu chí thật là N1–N4.

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| **N1** | Nền Windows giả, không ứng viên hợp lệ ⇒ `Chan(RC_KHONG_XAC_DINH)`; có `%ProgramFiles%\Git\cmd\git.exe` ⇒ trả đúng đường ấy, tuyệt đối, đã resolve. | **Đột biến:** quay bước giải Windows về hằng số `"/usr/bin:/bin"` ⇒ N1 ĐỎ. Một chốt cho bộ TƯƠNG ĐƯƠNG ba nguyên nhân — chúng không tách được bằng đầu vào, spec khai thẳng thay vì đếm thành ba. |
| **N2** | Nền Windows giả, `cwd` chứa `git.bat` **và** biến thể `git.py` (vì `PATHEXT` đo được có `.PY`) ⇒ kết quả **KHÔNG** trỏ vào cwd. | **Đột biến:** gỡ phép loại-trừ-cwd ⇒ N2 ĐỎ. Đo **chế độ hỏng THỨ HAI**: nhánh `win32` của `shutil.which` tự `path.insert(0, os.curdir)`, nên PATH "tối thiểu" tự nhận cwd — đúng cái nó sinh ra để chặn. Phân biệt được với N1 bằng đầu vào (cwd sạch ⇔ cwd có `git.*`) ⇒ **không** thuộc bộ tương đương N1. |
| **N3** | Ứng viên dưới `%SystemRoot%` bị loại; và khi bước `%ProgramFiles%` không phân giải, chẩn đoán ghi `KHÔNG_ĐO_ĐƯỢC` chứ không im lặng rơi xuống bước 3. | **Hai đột biến, hai cửa:** (a) gỡ phép loại `%SystemRoot%` ⇒ ĐỎ; (b) đổi nhánh "không phân giải được" thành rơi thẳng xuống bước 3 không ghi gì ⇒ ĐỎ. |
| **N4** | POSIX không hồi quy: trên `ubuntu-latest`, `_git_exe_toi_thieu()` vẫn trả `/usr/bin/git`. | **Đột biến:** đổi nhánh POSIX sang hằng số khác ⇒ ĐỎ. |
| **N5** | *(chỉ báo, KHÔNG phải tiêu chí)* `ops/lease_publish_test.py` trên `ubuntu-latest`: delta so `a612c70cbc56` = **0** ca đỏ (đơn vị: ca `def tNNN_` đỏ). | Đỏ ⇒ hồi quy do bản vá. Xanh **không** chứng minh mục tiêu nào. |
| **N6** | `git diff --numstat` so `a612c70cbc56`: ≤ **2** tệp và ≤ **300** dòng thêm. | Vượt ⇒ DỪNG, handoff, không tự nới. |

**N7 — xác nhận trên Windows thật, KHÔNG phải phép đo nghiệm thu.** Một lượt trên máy Windows của
chủ kho bằng script TỰ CHỨNG MINH đột biến đã áp (đếm dòng khớp hằng số: **trước = 1, sau = 0**) và
fail-close khi nền đo sai (không phải `win32`, hoặc `git` không có trong PATH thường ⇒
`KHÔNG_XÁC_ĐỊNH`, rc≠0, **không được đọc thành "đã chứng minh"**).

### Vì sao nghiệm thu KHÔNG neo vào `gate (windows-latest)` — hai lý do, cả hai đo được

1. **`t150` sẽ vẫn ĐỎ.** Nó nằm ngoài phạm vi và nguyên nhân khác. Nên `gate (windows-latest)` **không
   thể xanh** sau WP541 dù WP541 đúng hoàn toàn. Neo nghiệm thu vào nó là tự đặt một tiêu chí không
   bao giờ đạt. Đây là lý do ĐO ĐƯỢC, khác `r1` — `r1` chỉ nêu lý do thứ hai.
2. **Cổng có thể VẮNG MẶT.** #548 làm `gate` thôi chạy Windows khi push master. Nếu #548 land trước,
   cái đỏ biến mất khỏi CI — không phải vì được chữa. Kho có bài học riêng: *"cổng không nói dối —
   nó VẮNG MẶT, và trên giao diện 'xanh' với 'không chạy' nhìn giống hệt nhau."*

N1–N4 chạy trên `ubuntu-latest` bằng tham số tiêm, đo **hành vi giải đường dẫn theo nền** mà không
cần nền đó ⇒ WP541 miễn nhiễm với cả hai, và không tiêu `manual_ci_budget`.

## hinh_dang_ke_thua

`khong_ap_dung` — WP541 không phải packet khắc phục của packet nào; lỗi phát hiện bằng phép đo trực
tiếp, không phải từ một lượt thi công bị bác.

Hai doctrine ĐANG áp (không phải bộ đếm kế thừa):

- **#513 lượt 10→13** — *"vá đúng chỗ được chỉ rồi bỏ sót đường thứ ba"*. Áp thẳng: `_git_exe_toi_thieu`
  có **3** nơi gọi và phép giải có **3** bước ứng viên. Vì thế `nghiem_thu` tự liệt kê HẾT các đường
  TRƯỚC và cho mỗi đường một chốt riêng (N1 · N2 · N3a · N3b), và khai thẳng chỗ nào là bộ TƯƠNG
  ĐƯƠNG thay vì đếm thành ba chốt.
- **#355/#359** — *"đột biến bị giết không phải đột biến bị giết ĐÚNG LÝ DO"*. Áp thẳng: `t139` đang
  báo `tín dụng giả` trong chính log này. Mỗi ca mới ở M2 phải neo tín hiệu bằng lớp ngoại lệ riêng
  + tên ca, không bằng chuỗi `AssertionError` mà bất kỳ `except` nào cũng viết ra được.

## chua_do_duoc

1. **Hành vi `%ProgramFiles%` / registry trên runner `windows-latest` của GitHub.** Chưa ai đo.
   `manual_ci_budget: 0` nên phiên này không gọi CI Windows, và **máy Windows của chủ kho KHÔNG thay
   thế được phép đo đó** — máy khác, cấu hình khác. Rủi ro đã biết của M1 bước 2; N3 fail-close để nó
   hỏng ồn ào thay vì im lặng.
2. **Chênh `150` với `148`.** Đo 16:29Z: `ops/lease_publish_test.py` có **150** hàm `def tNNN_`. Log
   CI khai `đã chạy=148, bỏ qua=7`. Chênh **2** chưa giải thích được bằng phép đo — có thể là ca bỏ
   qua theo nền, có thể là log cũ hơn cây. **Đừng dùng `148` như con số đã kiểm.**
3. **Chế độ hỏng thứ hai (cwd chiếm quyền) chưa có phép đo trên Windows thật.** Suy từ mã nguồn
   `shutil.which` (nhánh `win32`: `path.insert(0, os.curdir)`) — đã đọc, chưa chạy. N2 đo nó bằng
   nền GIẢ trên Linux: đủ để khoá hành vi, **không** đủ để khẳng định ca thật trên Windows.
4. **Nợ trôi lệch giữa `_git_windows` (trong `lease_publish.py`) và `_bash_windows` (trong
   `cong_cu.py`).** Hai hàm cùng lớp bài toán, hai tệp, không cổng nào canh chúng đồng bộ. Do Issue
   #541 khai write set `only` hai tệp. Khai ra đây để lượt sau không phải phát hiện lại.
5. **Nguyên nhân gốc của `t150` trên Windows.** Đo được rằng nó KHÁC PATH; **chưa** đo được vì sao
   policy JSON bị đọc thành "vắng hoặc không phải JSON object". Cần packet riêng.
6. **Kích thước diff thật.** Chưa có bản vá nên `--numstat` chưa chạy. N6 là chốt thật.
7. **Trạng thái #540 / #548 / PR #550 lúc đọc spec này.** Đo 17:02Z: `#540 open`, `#538 open`,
   `#548 open`, `#550` là PR `open`. Phải đo lại trước khi cấp lease — Issue #541 buộc chờ WP540
   review xong.

## Ràng buộc thi công

- **KHÔNG chạy CI Windows bằng tay** (`manual_ci_budget: 0`).
- **KHÔNG tự merge, tự approve, tự review.** Reviewer phải fresh-context, độc lập, khác phiên.
- **KHÔNG chạm tệp ngoài `write_set`.**
- **KHÔNG viết dấu bỏ-qua-CI nguyên văn trong thông điệp commit**, kể cả khi trích dẫn.
- **Đọc `rc` TRỰC TIẾP**, đừng qua pipe.
- **`core.abbrev = 7`** khi chạy gate, kể cả trong sandbox reviewer.
