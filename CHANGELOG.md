# ★ v1.35.86 — r249: báo cáo lượt rà ra khỏi GÓI, vào thư mục `rasoat/` (2026-07-30)

5 tệp sản phẩm-phiên đang chiếm slot trong gói mà runtime Cowork không bao giờ đọc:
`KETQUA_DON_DU_LIEU_BHXH_2026-07-29.md` · `RASOAT_PROFILE_LUAT_BHXH_2026-07-29.md` ·
`RASOAT_BLLD_18-VBHN-VPQH.md` · `RASOAT_BLLD_2026-06-27.md` · `BANGIAO_NGUON_CONGBAO_BHXH_2026-07-29.md`.
Đã `git mv` cả 5 vào `rasoat/` và thêm `rasoat` vào `_RELEASE_EXCLUDE_DIRS`. Gói 198 → 193 tệp.

**Chọn THƯ MỤC, không liệt kê từng tên** — đây là điểm thiết kế, không phải tiện tay: báo cáo sinh
liên tục theo ngày, nên bảng tên sẽ trôi lệch ngay lượt rà sau và lại chiếm slot mà không ai nhớ vá.
Thư mục thì bao được mọi báo cáo tương lai với zero bảo trì.

**KHÔNG dùng `reports/` sẵn có** dù nó đã nằm trong `_RELEASE_EXCLUDE_DIRS`: `.gitignore` dòng 20 bỏ
qua `reports/`, nên chuyển vào đó là MẤT tệp khỏi git — trái yêu cầu (giữ trong repo, chỉ loại khỏi
gói). `rasoat/` là thư mục CÓ commit mà không vào gói, cùng khuôn `changelog_archive`.

Test **r249** đo qua CHÍNH hàm quyết định `_release_should_include` chứ không chỉ đọc bảng, và có
phản chứng: `rasoat/X.md` → loại · **`SKILL.md` ở gốc → VẪN nhận** (thiếu vế này thì một luật quét
quá tay vẫn xanh) · 4 báo cáo phải CÒN trên đĩa (loại khỏi gói ≠ xoá tệp).

Đã kiểm không tài liệu nào trỏ tới 5 tệp này nên `doc_pointers` không sinh con trỏ chết — khác với
bẫy r246, nơi một đường dẫn trong §10 trỏ tới tệp cố ý ngoài gói và `release-verify` bắt đỏ.

# ★ v1.35.85 — r248: script deploy phải NÓI RÕ khi bị đặt sai chỗ (2026-07-30)

**Sự cố người dùng báo:** copy `deploy-package.ps1` + `.cmd` sang `D:\Quốc hội\` rồi chạy ⇒ chết ở bước 0
với `Cannot find path 'D:\VERSION' because it does not exist.` Người đọc KHÔNG THỂ suy ra nguyên nhân
thật là SAI CHỖ ĐẶT: script tính gốc repo bằng "lên HAI cấp từ vị trí của nó" (vì vốn nằm ở
`<repo>/scripts/`), nên ở `D:\Quốc hội\` thì lên hai cấp ra `D:\`.

Lỗi kép: (1) người dùng đặt sai chỗ, (2) **script báo lỗi mù mờ** — và (2) mới là khiếm khuyết của ta.
Một thông báo chỉ đúng-về-mặt-kỹ-thuật mà không dẫn tới cách chữa thì vẫn là hỏng.

Nay CẢ HAI bản thử nhiều ứng viên rồi KIỂM dấu hiệu repo (`VERSION` + `scripts/tl.py`):
`-Repo`/`TL_REPO` → lên-2-cấp → thư-mục-script → cwd. Không đạt ⇒ in ĐÃ THỬ NHỮNG ĐÂU (từng đường dẫn,
kèm nhãn vì sao thử) + hai cách chữa, `rc=2`. Thêm tham số `-Repo` (ps1) và biến `TL_REPO` (sh) để ai
muốn giữ script ngoài repo vẫn chạy được.

Vá cả bản `sh` dù chỉ bản `ps1` sập — cùng một giả định "lên hai cấp", parity là doctrine.

**Test hai chiều, chạy thật (tải PowerShell 7.4.6, xong xoá):**
| tình huống | ps1 | sh |
|---|---|---|
| đặt đúng `<repo>/scripts/` | chạy | chạy |
| script NGOÀI repo, cwd cũng ngoài (đúng ca của user) | **rc=2 + chỉ rõ 3 đường đã thử** | **rc=2** |
| script ngoài repo + `-Repo`/`TL_REPO` | chạy | chạy |
| script ngoài repo nhưng cwd Ở TRONG repo | chạy (cwd cứu) | chạy |

Ca cuối đáng ghi: lượt test đầu tôi chạy từ trong repo nên `cwd` cứu, phép thử KHÔNG chạm đường đỏ —
phải dựng lại cwd trung tính mới tái hiện được. Fixture sai làm test xanh oan.

Kèm bộ khởi chạy mỏng `deploy-tra-luat.cmd` (KHÔNG vào repo — người dùng tự đặt ở `D:\Quốc hội\`): chỉ
`call` bản trong repo, sửa MỘT dòng `TL_REPO`. Cố ý không phải bản copy — hai bản song song sẽ trôi lệch,
đúng cái bệnh vừa chữa xong ở r246 khi bỏ `upload-skill-to-Package.ps1`.

# ★ v1.35.84 — r247: vỏ `.cmd` để double-click deploy (2026-07-30)

Bỏ `upload-skill-to-Package.ps1` ở r246 làm mất luôn đường **double-click** — Windows KHÔNG chạy `.ps1`
khi double-click (mở trong editor), và ExecutionPolicy mặc định có thể chặn. Đó chính là lý do đường cũ
có vỏ `.cmd`. Trả lại: `scripts/deploy-package.cmd`.

- Ưu tiên `pwsh` (7+, bản đã kiểm); chỉ có `powershell` 5.1 thì VẪN chạy nhưng NÓI RÕ 5.1 chưa kiểm và
  gợi ý `winget install`. Không im lặng giả định tương thích.
- `-ExecutionPolicy Bypass` chỉ cho TIẾN TRÌNH này, không đổi cài đặt máy.
- `pause` CHỈ khi không có đối số (đường double-click, để cửa sổ không biến mất); gọi từ terminal/CI có
  đối số thì trả rc ngay, không treo chờ.
- Truyền thẳng mọi đối số cho `.ps1` và **giữ nguyên rc** (0/1/2/3) — vỏ bọc không được nuốt mã lỗi.

Cũng thêm `deploy-package.cmd` vào `_RELEASE_EXCLUDE_NAMES_ANYWHERE` (dev-side, gói giữ 197 tệp) và mở
test **r244** lên 5 tên.

**Giới hạn phải nói rõ: `.cmd` KHÔNG được test hành vi.** Container này là Linux, không có `cmd.exe`, và
batch không có bản thay thế như PowerShell 7 trên Linux. Nên chỉ soi tĩnh, và bù bằng cách giảm bề mặt
rủi ro theo đúng các bẫy batch đã biết:
- **ASCII thuần + CRLF** cho cả hai tệp `.cmd` (kiểm bằng số: 0 ký tự >127, 0 LF lẻ). `cmd.exe` khó tính
  với LF-only và với ký tự ngoài code page.
- **KHÔNG nhúng đường dẫn có dấu** (`D:\Quốc hội`) vào `.cmd` — mời gọi lỗi code page. Tệp dọn lấy
  `%~dp0` (thư mục của chính nó) nên Windows tự đưa đúng đường dẫn, không qua bước giải mã nào.
- Không đọc biến được `set` TRONG cùng khối ngoặc (cần delayed expansion) — đã soi từng chỗ; các bộ đếm
  chỉ đọc SAU vòng lặp. `if defined` thì an toàn trong khối vì nó xét lúc chạy.
- Mốc thời gian lấy từ `wmic os get localdatetime`, KHÔNG dùng `%DATE%` (đổi định dạng theo locale máy).
- Ngoặc trong `echo` nằm trong khối đều escape `^(` `^)`.

# ★ v1.35.83 — r246: BỎ `upload-skill-to-Package.ps1`, một đường deploy cho mỗi nền (2026-07-30)

Người giữ chốt: chuyển sang `deploy-package.ps1`, bỏ script cũ. Kể từ đây **không còn đường deploy nào
thiếu chốt** — trước đó `upload-skill-to-Package.ps1` nằm ngoài repo nên (a) trôi lệch theo từng máy,
(b) không có chốt chống thụt lùi, (c) phiên Claude không đọc/sửa được.

Đường chính thức, hai nền, cùng quy trình — cả hai TRONG repo nên `git pull` là có bản mới nhất:
`.\scripts\deploy-package.ps1 -Pull -Push` · `./scripts/deploy-package.sh --push`.

**GỠ `scripts/wire_deploy_guard.py` (thêm ở r245, sống đúng một phiên bản).** Nó sinh ra CHỈ để vá
`upload-skill-to-Package.ps1`; bỏ script đó thì bộ vá mất đối tượng. Giữ lại là dead tooling mà tài liệu
vẫn trỏ tới — đúng loại doc-rot mà `doc-claims-check` sinh ra để bắt. Cần lại thì `git revert`.
Test **r244** thu về 4 tên (bỏ tên thứ 5), vẫn đo hai vế.

**Bẫy phát sinh, và repo tự dạy cách chữa đúng.** §10 viết lại có dòng `./scripts/deploy-package.sh` —
`release-verify` ĐỎ ngay: `doc_pointers` bắt con trỏ đó CHẾT TRONG GÓI, vì chính 4 script deploy đã bị
loại khỏi gói ở r244/r245. Cổng đúng, tài liệu sai.

Lượt chữa ĐẦU đi sai đường: khoanh cặp vào `_POINTER_BASELINE` (tiền lệ `GOTCHAS.md → scripts/.tl_state`,
"cố ý ngoài gói"). Test `r209_baseline_ratchet` ĐỎ ngay — baseline **khoá SỐ ĐẾM**, phình lên là phải sửa
test có chủ đích. Đọc chú thích của chính test đó mới thấy nếp đã chốt: r218 hạ 10→4, r226 hạ 4→3 và ghi rõ
*"sửa lời tài liệu thay vì khoanh nợ tiếp"* — cho ĐÚNG trường hợp tệp không có trong kho/gói. Nên đã GỠ
mục baseline vừa thêm (giữ ratchet ở 3) và sửa LỜI: §10 gọi TÊN tệp, dòng chạy đổi thành `cd scripts` rồi
`./deploy-package.sh --push` (cả hai script tự `cd` về gốc repo nên vẫn chạy đúng và vẫn copy-paste được),
kèm một khối `>` nói thẳng 4 script này ở trong repo nhưng CỐ Ý ngoài gói. Cũng cân phương án loại luôn
DEV_TOOLING_GUIDE khỏi gói rồi BỎ: `gen_instructions.py` có trỏ tới nó ⇒ sẽ sinh con trỏ chết MỚI.

Viết lại DEV_TOOLING_GUIDE §10 quanh `deploy-package.ps1`: bảng 5 bước kèm rc khi hỏng, nêu rõ "luôn
đóng gói bản mới nhất" được bảo đảm bằng CHẶN ở bước 0 chứ không bằng nhắc, và "chưa byte-match thì coi
như CHƯA deploy" ở bước 5. Dọn nốt 3 chỗ còn trỏ script cũ: §Quy trình sửa code bước 7 (cả hai tệp),
CLAUDE.md bước 7, và mục 1 §Quy ước deploy.

# ★ v1.35.82 — r245: nối chốt vào script deploy NGOÀI repo, tự động và fail-safe (2026-07-30)

`upload-skill-to-Package.ps1` ở `D:\Quốc hội\`, KHÔNG có trong repo (đã kiểm: không trên đĩa, chưa từng
vào git) nên phiên Claude không đọc/sửa được. Bảo người dùng tự chèn tay thì dễ chèn SAU lệnh
`drive-push` — lúc đó chốt vô nghĩa vì đã ghi đè rồi.

`scripts/wire_deploy_guard.py` — vá tự động, DRY mặc định, `--apply` mới ghi (sao lưu `.bak`):
- Tự tìm lệnh `drive-push` (regex biên từ, bỏ dòng chú thích) và chèn **NGAY TRƯỚC** nó, giữ đúng thụt lề.
- **KHÔNG thấy `drive-push` ⇒ TỪ CHỐI rc=2 và KHÔNG sửa tệp**, in khối để tự chèn. Không đoán chỗ:
  đoán sai ở đây tệ hơn không làm gì.
- **Idempotent** bằng marker — chạy lại không chèn lần 2.
- **Giữ nguyên vỏ tệp: CRLF + BOM.** Chính bài học v1.35.68 (viết lại text-mode nuốt CRLF, mất 1
  byte/dòng); script deploy Windows gần như chắc chắn CRLF, có thể có BOM.
- Khối chèn **TỰ ĐỌC `VERSION`** từ `--repo`, KHÔNG dựa vào tên biến trong script người dùng — không
  đoán được `$ver`/`$version`, đoán sai thì chốt chạy với version rỗng và mất tác dụng im lặng.
- `--repo` bị kiểm ngay (phải có `VERSION` + `scripts/deploy-guard.ps1`), sai thì chết TẠI ĐÂY chứ không
  để chết lúc deploy — lúc đó khó lần ra nguyên nhân.

**Test 6 vế trên fixture giống thật (CRLF + BOM + `drive-push` thụt trong khối `if`):** DRY chỉ đúng dòng ·
apply chèn + `.bak` · chạy lại idempotent (marker đếm 1) · BOM giữ và 0 LF lẻ · **chốt ở dòng 15 TRƯỚC
`drive-push` dòng 19** · fixture không có `drive-push` → rc=2 và md5 KHÔNG đổi.

**Kiểm CÚ PHÁP bằng chính `Parser` của PowerShell** (tải PowerShell 7.4.6 vào container, chạy rồi xoá):
tệp đã vá parse 0 lỗi, bản `.bak` cũng parse 0 lỗi (chắc fixture vốn đúng), và `deploy-guard.ps1` +
`deploy-package.ps1` cũng parse sạch. Chèn code vào script deploy của người khác mà chỉ "đọc thấy đúng"
là không đủ — cú pháp sai ở đó làm hỏng đường release của họ.

`wire_deploy_guard.py` cũng là dev-side (chỉ chạy ở máy dev để vá tệp ngoài repo) ⇒ vào
`_RELEASE_EXCLUDE_NAMES_ANYWHERE`, gói giữ 198 tệp. Test **r244** mở rộng lên 5 tên, vẫn đo hai vế.

# ★ v1.35.81 — r244: bản deploy PowerShell ĐẦY ĐỦ, quét bí mật dùng chung, và trần 200 tệp của gói (2026-07-30)

**`scripts/deploy-package.ps1`** — song sinh đầy đủ của `deploy-package.sh` cho Windows, thay hẳn
`upload-skill-to-Package.ps1` (ngoài repo). Nằm TRONG repo nên `git pull` là có bản mới nhất, hết cảnh
script deploy trôi lệch ở máy riêng. Cùng quy trình, cùng chốt, cùng mã lỗi (0/1/2/3).

"Luôn đóng gói ra bản mới nhất" làm bằng CHẶN chứ không bằng nhắc: bước 0 tự `git fetch` và DỪNG nếu
cây tụt sau `origin/master` (mục 2 quy ước) — build từ cây tụt sau chính là cách Package thụt lùi.
`-Pull` thì tự fast-forward rồi ĐỌC LẠI VERSION; KHÔNG bao giờ tự merge/rebase.

**`scripts/pkg_secret_scan.py`** — tách bảng mẫu bí mật thành NGUỒN SỰ THẬT DUY NHẤT cho cả hai đường.
Nhét inline vào mỗi script = hai bảng mẫu, và chúng SẼ trôi lệch: thêm mẫu bên sh mà quên bên ps1 thì
đường Windows đẩy lọt secret mà không ai biết.

**Trần 200 tệp — đụng THẬT, không phải đề phòng.** Thêm 3 script làm entries 199 → 202 ⇒ `release-bundle`
chết `IMPORT_LIMIT_EXCEEDED`. Bốn script deploy (`deploy-package.sh` · `deploy-package.ps1` ·
`deploy-guard.ps1` · `pkg_secret_scan.py`) là dev-side thuần — phiên Cowork LIVE bootstrap TỪ zip thì
không bao giờ tự deploy — nên vào `_RELEASE_EXCLUDE_NAMES_ANYWHERE`. GIỮ trong repo/git, CHỈ loại khỏi
GÓI, cùng tiền lệ `CLAUDE.md`/`.claude/`. Khoá bằng test **r244** đo BA VẾ, có phản chứng cho vế (b):
tệp phải VẪN CÒN trong repo — nếu thiếu vế đó thì "loại khỏi gói" biến thành "mất tệp" mà test vẫn xanh.

**Hai bẫy PowerShell sập ở lượt chạy đầu, đã vá và ghi lại trong chú thích code:**
- `param([string[]]$Args)` — `$Args` là BIẾN TỰ ĐỘNG trong hàm PS, nên `@Args` nở ra mảng tự động RỖNG
  thay vì đối số truyền vào ⇒ python chạy KHÔNG đối số, đọc stdin, EOF, **rc=0 và output rỗng**: gate
  báo "rc=0" mà chẳng chạy gì. Đây là kiểu xanh-oan nguy hiểm nhất. Đổi thành `$Argv`.
- `Get-Content -Raw` trên tệp RỖNG trả `$null` ⇒ `[regex]::Match` ném "Value cannot be null". Ép `[string]`.

Cả hai chỉ lộ ra vì CHẠY THẬT: đã tải PowerShell 7.4.6 vào container để chạy chứ không đọc code suy diễn.

**Thêm hai lỗi nữa cùng một họ — `-Force`, và nó không chỉ là chuyện đếm:**
- Đặt tên zip probe bắt đầu bằng dấu `.` ⇒ trên Unix là tệp ẨN, `Test-Path` thấy có mà `Get-Item`
  KHÔNG trả tệp ẩn khi thiếu `-Force` ⇒ ném "Could not find item". Đổi tên probe + thêm `-Force`.
- `Get-ChildItem` cũng bỏ tệp ẩn khi thiếu `-Force`. Phát hiện nhờ ĐỐI CHIẾU PARITY: cùng zip
  (sha `a69d3192…`) mà ps1 đếm 196 còn sh đếm 198 — hai tệp lệch là `.gitattributes`/`.gitignore`.
  Nhưng cùng lệnh đó CHÍNH LÀ bộ tìm tệp secrets ⇒ đường Windows đang MÙ với `.env`, `.netrc`,
  `.tl_secrets`. Đếm lệch chỉ là triệu chứng; lỗ an ninh là bệnh. Đã `-Force` mọi chỗ.

**Và một lỗ trong chính `pkg_secret_scan.py` vừa viết:** lọc theo phần mở rộng nên MÙ với tệp KHÔNG có
mở rộng — `pathlib` cho `Path('.env').suffix == ''`. Bơm `GOCSPX-…` vào `.env` thì bộ quét trả rc=0.
Nay quét cả tệp không mở rộng, tự tránh nhị phân bằng NUL-check 8KB + trần 2MB. Phản chứng 3 vế:
`.env` có secret → bắt · `credentials` (không mở rộng) → bắt · tệp nhị phân → bỏ đúng · cây sạch → rc=0.

Ba lỗi này đều KHÔNG thể bắt bằng đọc code — chúng lộ ra vì chạy thật rồi ĐỐI CHIẾU HAI BẢN với nhau.
Parity không phải nghi lễ: nó là cái duy nhất phát hiện đường Windows mù secrets.

# ★ v1.35.80 — r243: port chốt chống thụt lùi sang PowerShell (2026-07-30)

v1.35.79 cưỡng chế chốt cho đường Linux, nhưng đường Windows (`upload-skill-to-Package.ps1`) vẫn ghi đè
im lặng — hai đường vào CÙNG một fileId nên chốt một bên là chốt nửa vời.

Thêm `scripts/deploy-guard.ps1`: dạng DROP-IN, nối vào script ngoài repo bằng ĐÚNG 1 DÒNG đặt ngay
trước `drive-push` (khuôn ở DEV_TOOLING_GUIDE §10), cũng chạy tay được để kiểm trước khi đẩy. Làm kiểu
drop-in vì `upload-skill-to-Package.ps1` ở `D:\Quốc hội\`, KHÔNG có trong repo ⇒ không sửa mù nội dung
tệp mình chưa đọc.

**So sánh theo [version] chứ KHÔNG theo chuỗi** — đây là cạm bẫy thật, không phải đề phòng suông:
so chuỗi thì `'1.35.9' -gt '1.35.78'` ra ĐÚNG nhưng SAI về nghĩa. Cùng lý do bản sh dùng `sort -V`.

**Đã TEST HÀNH VI bằng PowerShell 7.4.6 thật** (tải vào container để chạy, không đọc code suy diễn):
| Drive | sắp đẩy | cờ | rc |
|---|---|---|---|
| 1.35.78 | 1.35.79 | — | 0 qua |
| 1.35.79 | 1.35.79 | — | **3 chặn** (bằng số) |
| 1.35.80 | 1.35.79 | — | **3 chặn** |
| 1.35.80 | 1.35.79 | `-ForceOlder` | 0 qua (đã WARN) |
| 1.35.78 | 1.35.9 | — | **3 chặn** (bẫy so chuỗi) |
| 1.35.9 | 1.35.78 | — | 0 qua (bẫy so chuỗi, chiều ngược) |
| tên người đặt tay | 1.35.79 | — | 0 qua + WARN (không chặn oan) |
| tên rỗng | 1.35.79 | — | **4 fail-closed** |

8/8 đúng. Đường sản xuất (gọi `gws` thật, Drive đang v1.35.79) cũng đã chạy: qua với 1.35.80, chặn với
1.35.79. **PARITY** với bản sh kiểm riêng trên 5 ca so sánh — hai bản cho cùng phán quyết, gồm cả bẫy.

Phân biệt hai loại lỗi, có chủ đích: KHÔNG ĐỌC ĐƯỢC Drive (gws chết/thiếu quyền/JSON hỏng) ⇒ `exit 4`
**fail-closed**, không đoán là an toàn. Đọc được nhưng KHÔNG RÚT ĐƯỢC version từ tên ⇒ WARN và đi tiếp,
vì tên file có thể do người đặt tay và ta ĐÃ biết trạng thái Drive.

# ★ v1.35.79 — r242: cưỡng chế chốt CHỐNG THỤT LÙI khi đẩy Package (2026-07-30)

v1.35.78 chốt quy ước deploy vào CLAUDE.md, nhưng mục 3 ("Drive ≥ version sắp đẩy ⇒ DỪNG") chỉ là
VĂN BẢN — `deploy-package.sh` đọc tên Package trên Drive rồi chỉ IN ra, không so, không chặn. Chính
quy ước đó viết "không có nó thì mục 1-2 chỉ là lời hứa", nên để nguyên là tự mâu thuẫn.

Nay bước 4 rút version từ tên file Drive và so bằng `sort -V`:
- Drive **>** bản sắp đẩy ⇒ `rc=3`, chặn **TRƯỚC** `drive-push` (không chạm Drive), in cách chữa.
- Drive **=** bản sắp đẩy ⇒ CŨNG CHẶN. Cùng số mà khác cây là đúng cái sai "một số version = một cây"
  đã cấm ở mục v1.35.68; muốn đẩy lại y nguyên thì cũng phải nói rõ ý định.
- Cố ý ghi đè ⇒ `--force-older` (WARN rồi đi tiếp).
- Không rút được version từ tên ⇒ WARN và đi tiếp, KHÔNG chặn oan (tên file có thể do người đặt tay).

**Phản chứng end-to-end, không dùng test hook** — nhân bản cây rồi hạ số hiệu, Drive thật đang v1.35.78:
| cây | cờ | rc | `drive-push` có được gọi? |
|---|---|---|---|
| v1.35.70 | — | **3** | KHÔNG |
| v1.35.78 (bằng số) | — | **3** | KHÔNG |
| v1.35.78 | `--force-older` | — | CÓ (đã WARN) |

Đã kiểm Drive NGUYÊN VẸN sau hai lượt bị chặn: `md5=7cd1aacd…` và `modifiedTime` không đổi — chốt
nằm trước đường ghi, không phải rollback sau khi đã đẩy. Vế `--force-older` đo bằng cách thay
`drive-push` bằng bản giả CHỈ trong cây thử, nên chứng minh được nhánh đó xuyên qua mà không đụng
Drive thật.

Giới hạn còn lại, đã ghi vào CLAUDE.md mục 3: đường `upload-skill-to-Package.ps1` bên Windows CHƯA có
chốt này ⇒ deploy từ đó phải tự kiểm bằng tay.

# ★ v1.35.78 — r241: `core.abbrev` là ĐIỀU KIỆN TẤT ĐỊNH của gate, không phải tuỳ chọn (2026-07-29)

Truy ra từ việc `git fetch --unshallow` để dứt điểm 2 cờ `SHA_NOT_A_COMMIT` của doc-claims-check
trong container remote. Unshallow ĐÚNG là cách chữa (79 → 304 commit, `ad413e7`/`78d6bfe` resolve
được, 2 cờ về 0) — nhưng nó LỘ RA trôi dạt nguy hiểm hơn: `doc-claims-check` suy tập
độ-dài-SHA-ứng-viên từ `git rev-parse --short HEAD`, mà git trả độ dài TỐI THIỂU-DUY-NHẤT — trôi
theo cả SỐ COMMIT lẫn COMMIT ĐANG Ở HEAD. Repo phình ⇒ ngưỡng 7 → 8 ⇒ mọi chuỗi 8 hex thành SHA.

ĐO trên cây này (không suy diễn):
| ngưỡng | golden | docclaims | determinism | selftest |
|---|---|---|---|---|
| **7** | ✓ | ✓ 0 cờ | ✓ | N/N |
| 8 | ✗ case `doc_claims_check_fixture` | ✗ **18 cờ TOÀN FALSE POSITIVE** | ✗ | N-1/N |

18 cờ giả là tiền tố UUID bị nhận nhầm thành SHA: notebook id `59e8d0de`, `45739ff7`, `743ed200`,
`dbe706a0`… Phạm vi ảnh hưởng RỘNG HƠN chú thích cũ: không chỉ L2 của docclaims mà kéo đỏ cả
**golden và determinism** — golden được ghi ở ngưỡng 7.

`scripts/deploy-package.sh` (thêm ở v1.35.69/r232) nay tự ghim `core.abbrev=7` REPO-LOCAL ở bước 0
và cảnh báo khi repo còn shallow. CI ghim `--global`; repo-local hẹp hơn, không đụng config global
của người dùng. `.git/config` KHÔNG được commit nên mỗi clone mới phải đặt lại ⇒ script tự đặt.

**Cách ghim SAI đã thử và bị chính test bắt:** ban đầu tiêm qua env `GIT_CONFIG_*`. Env đó thắng cả
config của repo CON, nên nó đè luôn repo tạm mà `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` tự dựng
để đo chênh 7-vs-8 ⇒ đúng cái test khoá hành vi này ĐỎ. Config repo-local không có tật đó vì repo tạm
mang config riêng. Ghi lại để đừng ai "tối giản" nó về env.

# ★ v1.35.77 — r240: NLM chạy được từ điện thoại — jar phải LIST giữ domain, KHÔNG `nlm login --manual` (2026-07-29)

## THÀNH CÔNG: cookie từ điện thoại nạp được, 139 notebook

Chốt cả chuỗi r233–r239. User export bằng **Cookie Quick Manager** (đọc cookie MỌI domain) từ
Firefox Android → bộ ĐỦ: có LSID/__Host-GAPS/__Host-1PLSID/3PLSID (accounts.google.com). Nạp →
`nlm login --check` = **✓ Authentication valid! Notebooks found: 139**.

## Bug CUỐI (đo LIVE): `nlm login --manual -f` LÀM PHẲNG jar → mất domain

Bộ cookie ĐỦ vẫn ĐỎ khi nạp bằng `nlm login --manual`. Truy: nó lưu cookies.json DẠNG DICT phẳng
(name→value). `_get_httpx_cookies` (nlm core/base.py) khi gặp dict phẳng đặt MỌI cookie vào
`.google.com` ⇒ cookie host-scoped `LSID`/`__Host-GAPS` (accounts.google.com) sai host ⇒
RotateCookies tới accounts.google.com không nhận đủ ⇒ Google đẩy signin. Bản CDP-harvest
(`nlm login` thật) lưu cookies.json DẠNG LIST có `domain` nên `_get_httpx_cookies` giữ đúng host.

Bằng chứng phân tách: replay httpx set ĐÚNG domain từng cookie ⇒ KHÔNG bị đẩy signin; cùng bộ đó
qua `nlm login --manual` (phẳng) ⇒ bị đẩy signin. Khác biệt DUY NHẤT = domain.

## Vá

- Thêm `scripts/nlm_auth_convert.py`: nhận CQM `{"cookies":[…]}` / list thô / dict phẳng / header
  → ghi cookies.json **LIST giữ domain** (schema CDP: domain/expires/httpOnly/…). Với input phẳng
  gán domain theo TÊN (LSID/__Host-*/ACCOUNT_CHOOSER/SMSV→accounts.google.com, OSID→notebooklm,
  còn lại→.google.com). VALIDATE identity 7 + LSID TRƯỚC khi ghi (thiếu ⇒ rc2, không đụng jar).
- `nlm-auth-import.sh`: bỏ `nlm login --manual -f` (làm phẳng), gọi convert. Sửa 1 bug bash:
  backtick trong chuỗi `ok "...\`tl …\`"` bị thực thi như command-substitution (`tl: not found`).

Đã kiểm end-to-end: `./scripts/nlm-auth-import.sh --file <CQM export>` ⇒ jar LIST 35 cookie giữ
domain, probe 139 notebook, stage bundle Drive (verify LIVE 300 nguồn). rc=0.

## Cẩm nang phone (chốt): Firefox Android + **Cookie Quick Manager** (KHÔNG Cookie-Editor — chỉ
tab hiện tại, hụt LSID) → export toàn bộ cookie google → Drive `ducthangho@gmail.com` → ở sandbox
`./scripts/nlm-auth-import.sh`. Mọi thứ CÙNG account ducthangho@gmail.com (browser + Drive + gws).
# ★ v1.35.76 — r239: nút thắt cookie NLM là LSID/đăng-nhập, KHÔNG phải PSIDTS (đo LIVE) (2026-07-29)

Tiếp r238. User export lại nhưng vẫn 19 cookie thiếu nhóm phiên. Truy tới gốc bằng ĐO LIVE
(không đoán tiếp):

1. Tra mã nlm: `REQUIRED_COOKIES = [SID,HSID,SSID,APISID,SAPISID]` — chỉ 5, bản 19-cookie CÓ đủ
   ⇒ nlm báo "đăng nhập thành công". Nhưng đó chỉ là sanity-check của nlm, KHÔNG phải điều Google đòi.
2. Tái hiện request thật (httpx GET notebooklm.google.com): BỊ ĐẨY VỀ accounts.google.com/signin
   ⇒ Google TỪ CHỐI bộ cookie. (Chữ "region" trong HTML chỉ là footer trang signin — URL là
   /signin = lỗi AUTH, không phải chặn vùng; sandbox từng chạy 139 notebook nên vùng không chặn.)
3. Thử `rotate_google_cookies` (endpoint accounts.google.com/RotateCookies của nlm): MINT THÀNH CÔNG
   __Secure-1PSIDTS/3PSIDTS — nhưng VẪN bị đẩy signin ⇒ PSIDTS KHÔNG phải nút thắt (nlm tự mint).

Nút thắt THẬT = cookie ĐĂNG NHẬP (LSID/__Host-GAPS, chỉ ở accounts.google.com) + ROTATION
(__Secure-*PSIDRTS). Bản upload lấy từ myaccount.google.com (có 3 cookie myaccount: OSID/OTZ) nên
hụt nhóm này; Google không chấp nhận replay session thiếu cookie đăng nhập từ IP sandbox. Bộ
54-cookie hồi đầu chạy được vì có đủ.

Vá validation (r239): LSID là CỔNG (thiếu ⇒ chặn, chỉ thẳng accounts.google.com/AccountChooser —
trang "chọn tài khoản" ở đúng host accounts, đừng bấm vào tài khoản); *PSIDTS HẠ xuống chỉ ghi chú
(nlm tự mint qua RotateCookies, không chặn); *PSIDRTS vẫn cảnh báo. Đã test: bản 19-cookie ĐỎ ở
bước 2 với thông điệp đúng nút thắt.

Đường chắc ăn khi phone không đủ: `nlm login` trên máy có browser (CDP lấy đủ jar) → nlm-auth-stage.
# ★ v1.35.75 — r238: nlm-auth-import — 3 lỗi thật khi user upload cookie từ điện thoại (2026-07-29)

Chạy import thật lần đầu với file user upload từ điện thoại (Firefox+Cookie-Editor), lộ 3 lỗi:

## 1. Upload .json bị Google chuyển thành Google Docs
`mimeType = application/vnd.google-apps.document` ⇒ `alt=media` KHÔNG tải được. Vá: dò
mimeType trước; nếu là `vnd.google-apps.*` thì `files export mimeType=text/plain` rồi cắt BOM
(Docs export chèn ﻿ đầu file ⇒ json.loads nổ "Unexpected UTF-8 BOM"). JSON THÂN sống sót qua
Docs (không bị smart-quote) — chỉ BOM+CRLF, cắt BOM là đọc được.

## 2. gws chặn --output ra ngoài cwd
"--output resolves to ... outside the current directory". Script tải vào /tmp ⇒ chết. Vá: tải
vào scripts/.tl_state/ (trong repo) rồi xoá qua trap. (Bug này che bởi `>/dev/null 2>&1` ban đầu.)

## 3. Export THIẾU cookie ⇒ probe network_error (không phải lỗi mạng)
Bản upload có 19/54 cookie: đủ 7 cookie ĐỊNH-DANH (SID/*PSID/HSID/SSID/APISID/SAPISID) nên nlm
"đăng nhập thành công" — NHƯNG thiếu `__Secure-*PSIDTS` (dấu thời gian phiên) và `LSID`/
`__Host-GAPS` (cookie đăng nhập, chỉ sống ở accounts.google.com) ⇒ API NotebookLM TỪ CHỐI, nlm
báo "network_error: ValueError". Đó là vì export từ Gmail/myaccount HỤT nhóm __Host-*/LSID.

Vá validation 3 TẦNG (chặn TRƯỚC khi nạp, thay vì để probe LIVE mới lộ): định-danh → *PSIDTS →
LSID; thiếu bất kỳ ⇒ exit 2 + chỉ thẳng "export từ tab accounts.google.com" (nơi DUY NHẤT mang
LSID/__Host-GAPS và thấy cả cookie .google.com). *PSIDRTS vẫn chỉ WARN (thiếu thì phiên ngắn).

Đã kiểm: bản 19-cookie nay ĐỎ ở bước 2 (rc=2) với thông điệp đúng, KHÔNG đụng jar.
# ★ v1.35.74 — r237: cookie harvest KHÔNG cần notebooklm.google.com (vá cho vùng bị chặn web) (2026-07-29)

User đã cài Firefox + Cookie-Editor nhưng notebooklm.google.com bị chặn theo vùng ⇒ không mở
được trang web để "đứng trên tab đó" mà export. App NotebookLM thì chạy.

Đo trên jar TỪNG CHẠY ĐƯỢC (139 notebook): 7 cookie nlm bắt buộc (SID · __Secure-1PSID ·
__Secure-3PSID · HSID · SSID · APISID · SAPISID) đều nằm trên .google.com / .google.com.hk —
KHÔNG cái nào trên notebooklm.google.com (trang đó chỉ có _ga/OSID, không phải thứ nlm dùng).
Tức chúng là cookie ĐĂNG NHẬP GOOGLE CHUNG. Bằng chứng mạnh nhất: jar cũ lấy SID/__Secure-1PSID
từ .google.com.HK (một trang Google vùng khác) mà vẫn chạy 139 notebook từ sandbox.

Hệ quả: harvest cookie từ Gmail / myaccount.google.com (KHÔNG bị chặn) là ĐỦ; không cần mở
notebooklm web. Truy cập API NotebookLM xảy ra Ở SANDBOX (vùng của nó), không ở trình duyệt
người dùng — nên vùng của điện thoại không liên quan.

App NotebookLM chạy được KHÔNG dùng làm nguồn cookie: app lưu auth ở storage riêng, không root
thì không lấy ra được. Nó chỉ XÁC NHẬN tài khoản có quyền NotebookLM (khớp: sandbox chạy được).

Vá hướng dẫn trong nlm-auth-import.sh (header + thông điệp thiếu-cookie): trỏ Gmail/myaccount
thay vì notebooklm; nêu rõ vùng web bị chặn không ảnh hưởng.
# ★ v1.35.73 — r236: nlm-auth-import --watch (tự phát hiện file mới) + đính chính "script cài trên điện thoại" (2026-07-29)

## Yêu cầu & giới hạn thật

User muốn "script tự cài Firefox Android + addon + chạy lấy cookie tự động". Phần TRÊN ĐIỆN
THOẠI KHÔNG script hoá được — ba rào cản độc lập: (1) container không có đường vào máy người
dùng (chỉ egress qua proxy); (2) Android chưa root không cho script cài APK / lái GUI trình
duyệt (cần chạm tay — tính năng bảo mật); (3) đăng nhập Google không tự động hoá an toàn được,
và extension tự moi cả session Google là anti-pattern bảo mật. Bước "browser đã đăng nhập →
sinh JSON session" BẮT BUỘC là hành động người-thật.

## Cái tự động hoá ĐƯỢC: --watch

Thêm `--watch <phút>` (mặc định 15): ghi mốc modifiedTime của bản mới nhất lúc bắt đầu, poll
Drive mỗi 20s, khi có file khớp mới HƠN mốc thì tự nạp → probe LIVE → stage. Nhờ vậy luồng còn:
[điện thoại] export JSON + lưu Drive · [sandbox] bật 1 lệnh, phần còn lại tự chạy.

## Bug đã bắt trong lúc làm (ghi lại — lớp lỗi ĐO ĐƯỢC)

`_pick_newest` bản đầu in bằng f-string có `\t` trong biểu thức — Python **3.11 CẤM backslash
trong f-string** (chỉ 3.12+ mới cho). `2>/dev/null` NUỐT SyntaxError ⇒ hàm lặng lẽ trả rỗng ⇒
`--watch` sẽ KHÔNG BAO GIỜ thấy file dù có thật. `bash -n` không bắt được (lỗi nằm trong Python
nhúng). Sửa: bỏ f-string, dùng `%`-format. Bài học: inline Python trong .sh phải test HÀNH VI,
không tin `bash -n`; và đừng để `2>/dev/null` che lỗi cú pháp của chính mình.
# ★ v1.35.72 — r235: nlm-auth-import TỰ TÌM file trên Drive (bỏ bước tra fileId) (2026-07-29)

Mục tiêu vận hành: người dùng chỉ có ĐIỆN THOẠI, muốn "cơ bản chỉ chạy script". Bản r233 bắt
phải nêu `--drive-id <fileId>` — mà lấy fileId trên điện thoại là bước thủ công khó chịu nhất
của cả luồng (mở Drive, chia sẻ, cắt id khỏi URL).

Nay chạy `./scripts/nlm-auth-import.sh` KHÔNG tham số: tự truy vấn Drive qua gws
(`name contains 'nlm-auth' and trashed = false`, `orderBy modifiedTime desc`), in tối đa 5 bản
tìm được, ĐÁNH DẤU bản mới nhất bằng mũi tên rồi dùng nó. `--drive-find <chuỗi>` để đổi chuỗi
tìm; `--drive-id` và `--file` giữ nguyên.

Không tìm thấy ⇒ nói thẳng phải làm gì (đặt tên file có `nlm-auth`), không để người dùng đoán.

Luồng điện thoại rút còn: export cookie JSON → lưu vào Drive → ở đây gõ 1 lệnh.
# ★ v1.35.71 — r234: chính env-reimport.sh in lời khuyên đã bị bác (2026-07-29)

Ngay lượt chạy đầu sau khi deploy r233, `env-reimport.sh` in ở nhánh NLM-chết:
«Trong lúc chờ: dùng NotebookLM MCP (mcp__notebooklm-*) — không cần cookie CLI.»

Câu đó SAI, và r233 đã đo ra chính điều ngược lại trong cùng một lượt: phiên này KHÔNG có
NotebookLM MCP nào (`ListMcpResourcesTool` chỉ trả `github`), còn MCP của chính gói nlm thì
dùng CHUNG `get_client()`→`load_cached_tokens()` nên cũng chết theo cookie. Tức script vừa
viết đã mang sẵn lời khuyên mà CHANGELOG cùng bản vá tuyên bố là sai — đúng lớp bug r232 vừa
sửa cho `doctor`, lần này tôi tự mắc lại.

Thay bằng hai đường THẬT: (A) máy có trình duyệt → `nlm login` + `nlm-auth-stage`; (B) chỉ có
điện thoại → trình duyệt CÓ extension (Quetta/Edge Canary/Firefox+add-on) → export JSON →
Drive → `nlm-auth-import.sh --drive-id`. Kèm câu chốt: Chrome Android KHÔNG dùng được (không
extension, 9/13 cookie httpOnly) và KHÔNG tồn tại đường fallback MCP ở phiên này.

# ★ v1.35.70 — r233: hai script vận hành sandbox headless + đo lại đường NLM (2026-07-29)

## `scripts/env-reimport.sh` — dựng lại môi trường

Idempotent, chỉ cần `TL_TOKEN` (KHÔNG cần `TL_MASTER_KEY`). Ba điểm thiết kế có chủ đích:
- smoke **THẬT** bằng `gws drive files list`, không dừng ở `gws-ping` (ping chỉ đọc config, không
  chứng minh `refresh_token` còn đổi được access token);
- phán quyết NLM **chỉ** bằng probe LIVE — tuổi cookie và cờ rotation KHÔNG kết luận thay được;
- khi chốt chống hạ cấp (r229) chặn thì **KHÔNG tự `--force`**: jar cục bộ chết thì bundle càng
  chết, ép ghi chỉ mất bản tươi hơn. `rc=3` = gws sống / NLM chết ⇒ deploy vẫn chạy.

## `scripts/nlm-auth-import.sh` — nạp cookie từ trình duyệt KHÁC

Cho đường "lấy cookie ở điện thoại → nạp vào sandbox". Kiểm ĐỦ cookie phiên TRƯỚC khi đụng jar,
sao lưu jar và KHÔI PHỤC nếu nạp hỏng hoặc probe LIVE đỏ, rồi `nlm-auth-stage` để phiên sau khỏi
làm lại. Tên tệp cố ý KHÔNG chứa `cookie`: mẫu đó nằm trong danh sách secret của `CLAUDE.md` nên
secret_guard chặn cả đọc lẫn ghi — bản đầu đặt tên `nlm-cookie-import.sh` và bị chặn ngay.

## Đo lại đường NLM (thay cho suy đoán trước đó)

| Câu hỏi | Kết luận | Bằng chứng |
|---|---|---|
| NotebookLM MCP có trong phiên Cowork/web này? | **KHÔNG** | `ListMcpResourcesTool` chỉ trả server `github`; ToolSearch không có tool notebooklm nào |
| MCP của gói nlm chạy được khi chưa `nlm login`? | **KHÔNG** | `notebooklm-mcp = notebooklm_tools.mcp.server:main` dùng chung `get_client()`→`load_cached_tokens()`; docstring server tự ghi "run `nlm login`" |
| Lấy cookie từ Chrome trên điện thoại? | **KHÔNG** | 9/13 cookie phiên là `httpOnly` (đo trên jar thật) ⇒ JS/bookmarklet mù; Chrome Android không có extension |
| `nlm login` chạy trong sandbox? | **KHÔNG** | cần CDP tới browser đã đăng nhập; container chỉ có egress qua proxy, không với tới máy người dùng |
| Có đường nào từ điện thoại? | **CÓ** | trình duyệt Android có extension (Quetta/Edge Canary/Firefox+add-on) → export JSON → Drive → `nlm-auth-import.sh` |

Sửa lại một khẳng định sai ở lượt trước: tài liệu và câu trả lời từng nói "thiếu nlm/auth thì
fallback NotebookLM MCP". Điều đó KHÔNG đúng cho phiên này — không có server nào để fallback.

`nlm login --manual -f` nhận JSON list / JSON dict / chuỗi header (`extract_cookies_from_chrome_export`),
KHÔNG nhận Netscape `.txt` — script bắt riêng ca đó và in lệnh `awk` chuyển đổi, vì extension phổ
biến nhất lại xuất đúng định dạng không dùng được.

# ★ v1.35.69 — r232: gợi ý khắc phục của `doctor` chỉ tới lệnh KHÔNG chữa được (2026-07-29)

> Phát hiện khi làm theo chính gợi ý của `doctor` sau r229: chạy `nlm-reconcile --apply` cho 53 mục
> lệch thì DRY cho thấy nó ghi ĐÚNG 0 DÒNG. Dừng trước khi ghi, đo lại, hoá ra gợi ý sai.

## Gốc — sai theo CẤU TRÚC, không phải theo dữ liệu

`doctor` in MỘT câu cho MỌI kiểu drift: «đồng bộ 1 bước: `tl nlm-reconcile <nb> --apply`». Nhưng
reconcile CHỈ ghi cho dòng **THIẾU** `nlm_notebook_id`/`nlm_source_id` (tập backfill/link).

| Cờ | reconcile `--apply` chữa được? | Vì sao |
|---|---|---|
| `NLM_NOTEBOOK_ID_MISSING` | ✅ | đúng định nghĩa backfill |
| `NLM_STATUS_MISMATCH` | ✅ | link/settle |
| `CORPUS_TRUE_NOT_ON_NLM` | ❌ | **NỢ PHỦ** — nguồn CHƯA CÓ MẶT trên NLM; không lệnh registry nào tạo ra nguồn |
| `row_kind` topology (71 dòng) | ❌ | reconcile ghi `row_kind` **kèm** dòng backfill/link, mà `_topology_row_kind_findings` chỉ nhận dòng **ĐÃ CÓ** `nlm_notebook_id` (`if not nb: continue`) ⇒ **hai tập RỜI NHAU** |

Đo 29-07-2026 trên kho thật: breakdown `NLM_STATUS_MISMATCH=0 · CORPUS_TRUE_NOT_ON_NLM=53 ·
NLM_NOTEBOOK_ID_MISSING=0`; DRY reconcile trên **cả** notebook nền `743ed200…` **lẫn** notebook
overflow `2d8c2fef…` (nơi mang đủ 71 dòng lệch) đều cho `backfill=0 · link=0 · desync=0 ·
settle=0 · unregistered=0`. Grep toàn kho: `OVERFLOW_ROW_NOT_MARKED_OVERFLOW` chỉ xuất hiện ở
ĐÚNG MỘT chỗ — hàm phát hiện; không có đường ghi nào.

Đây là lớp bẫy nguy hiểm nhất, cùng họ với «`nlm login` là đủ» đã bị bác ở GOTCHAS §9: câu sai
**đọc như hướng dẫn vận hành**, nên người làm đúng theo nó sẽ tin đã sửa xong trong khi không có
gì đổi.

## Vá

`_drift_hint_lines(bd, nb)` — PURE, tách khỏi chỗ in để test được; gợi ý theo TỪNG cờ:
- có `NLM_NOTEBOOK_ID_MISSING`/`NLM_STATUS_MISMATCH` ⇒ vẫn mời `--apply`, nhưng đếm ĐÚNG số mục
  chữa được (không phải tổng drift);
- có `CORPUS_TRUE_NOT_ON_NLM` ⇒ nói thẳng là NỢ PHỦ, `--apply` KHÔNG chạm tới, trỏ `slot-audit` +
  `ingest-missing`;
- sạch ⇒ im.

Tên mới PHẢI khai trong `_STUB_MAP["ops_misc"]`: `cmd_doctor` re-home `__globals__` về namespace
`tl`, quên khai thì NameError đúng lúc in cảnh báo (bẫy I11). Ca test khoá luôn điều này.

Gợi ý `row_kind` đổi thành REPORT-ONLY kèm lý do cấu trúc. Sửa 2 chú thích đã lỗi thời trong
`ops_misc.py` (§F-06) và docstring `_topology_row_kind_findings` (`nlm_ops.py`) — cả hai đang nói
`--apply` chữa được.

## Test khoá (2 ca) + phản chứng hai chiều

| Ca | Khẳng định | Gỡ vá |
|---|---|---|
| `r232_goi_y_doctor_khop_thu_reconcile_ghi_duoc` | chỉ NỢ PHỦ ⇒ không mời `--apply`; có cờ chữa được ⇒ mời và đếm đúng (7=3+4); cả hai ⇒ 2 dòng; sạch ⇒ rỗng; `_drift_hint_lines` resolve được từ namespace tl | **ĐỎ** |
| `r232_row_kind_va_backfill_la_hai_tap_roi_nhau` | mọi finding đều mang `notebook_id` khác rỗng; dòng THIẾU `notebook_id` (ứng viên backfill duy nhất) không bao giờ lọt vào findings dù `row_kind` sai; kèm chốt UX chuỗi gợi ý cũ đã biến mất | **ĐỎ** |

Selftest **1393/1393** (sau merge origin/master mang r230/r231). Trước merge: 1386/1386; gỡ 3 tệp logic (giữ test) ⇒ 1384/1386, cả 2 ca đỏ.

Ruff `--select F` DELTA so master = **0** cả 4 tệp. Ghi chú: bản test đầu dùng `_TL_MODULE` làm
delta **+3** (`F821 Undefined name '_TL_MODULE'` — đúng lớp sẵn có 1992 lần, nhưng tiêu chí là
delta 0) ⇒ đổi sang `importlib.import_module("tl")` gán biến cục bộ. Đã thử `_mod215` (nạp thẳng
tl_core) và BÁC: `_resolve_shard_topology` gọi `_profiles_from_config`, `_topology_row_kind_findings`
gọi `_shard_row_kind` (nlm_admin_ops) — cả hai chỉ resolve qua namespace tl, nạp thẳng ⇒ NameError.

## Hiệu lực (doctor LIVE, cùng dữ liệu từng sinh ra gợi ý sai)

```
⚠ registry↔NLM lệch: 53 mục → NLM_STATUS_MISMATCH=0 · CORPUS_TRUE_NOT_ON_NLM=53 · NLM_NOTEBOOK_ID_MISSING=0
   53 mục CORPUS_TRUE_NOT_ON_NLM = NỢ PHỦ (nguồn CHƯA có mặt trên NLM) — `nlm-reconcile --apply`
   KHÔNG chạm tới: nó chỉ điền trường cho dòng ĐÃ có nguồn. Soi bằng `tl slot-audit --notebook-id
   743ed200-…`; đẩy nguồn bằng `tl ingest-missing`.
```

Câu «đồng bộ 1 bước … --apply» đã biến mất khỏi ca này.

## KHÔNG làm

Không tự sửa 53 mục lẫn 71 dòng — đó là DATA-ops, cần user chốt phạm vi. r232 chỉ sửa việc
**công cụ nói sai sự thật**.

## Va chạm số hiệu khi merge (ghi lại để lượt sau khỏi vấp)

Bản vá này làm ở nhánh tách từ v1.35.65 và tự đánh **r230/v1.35.66**. Trong lúc đó `master` đã tiêu
thụ ĐÚNG hai số đó cho việc khác (`r230` = chunk NLM nuốt khối đầu văn bản, `r231` = 4 vá dọn hồ sơ
BHXH) và đi tới **v1.35.68**. Khi merge phải đánh lại toàn bộ thành **r232/v1.35.69** — đổi bằng
token CHÍNH XÁC, không thay chuỗi hàng loạt, vì `tl_selftest.py` chứa CẢ `r230` của master (3 chỗ,
gồm `r230_chunk_khong_nuot_khoi_dau_va_dieu_1`) lẫn của mình (5 chỗ); `ops_misc.py`/`nlm_ops.py`
master không đụng nên thay cả tệp được. Sau đổi: còn đúng 3 chỗ `r230` — của master.

# ★ v1.35.68 — merge r229 vào nhánh r230/r231 (2026-07-29)

**Thêm `scripts/deploy-package.sh` — đóng gói + deploy TỪ LINUX/Cowork.** Trước đây deploy chỉ có
đường Windows (`upload-skill-to-Package.ps1` ở `D:\Quốc hội\`, user double-click), nên trong container
remote KHÔNG deploy được. Script này chạy cùng quy trình §10 DEV_TOOLING_GUIDE + §6 bước 7-8:
VERSION khớp 3 chỗ → gate 8 bước → bundle ×2 đòi same-SHA → verify trong gói → (tuỳ chọn) drive-push
→ tải lại đối chiếu BYTE + VERSION.

MẶC ĐỊNH KHÔNG ĐẨY: phải nêu `--push`. Ba điểm học từ chính lần chạy đầu:
- `release-bundle` TỪ CHỐI ghi zip trong skill root (`OUT_INSIDE_SKILL_ROOT`, kẻo zip nuốt chính nó)
  và tự chuyển ra thư mục cha ⇒ script phải đọc đường dẫn THẬT từ khoá `out` của JSON. Bản đầu tin
  vào tham số mình truyền nên `sha256sum` chết trên tệp không tồn tại, hai chuỗi RỖNG so nhau lại
  BẰNG NHAU ⇒ cổng same-SHA báo ✓ oan. Nay chặn rỗng trước khi so.
- `release-verify` chạy trong gói sinh `__pycache__` ⇒ đếm tệp phải loại, nếu không 195 đọc thành 224.
- `doc-claims-check` đỏ trên clone SHALLOW vì SHA cũ trong `changelog_archive` không resolve được.
  Script chỉ hạ thành WARN khi repo THẬT SỰ shallow VÀ mọi cờ đều là `SHA_NOT_A_COMMIT`; cờ khác ⇒
  đỏ như thường. Đã ĐO NỀN trên origin/master: y hệt 2 cờ, delta = 0.

Phản chứng đã chạy (không tin cổng chặn chỉ vì nó tồn tại): VERSION lệch 3 chỗ ⇒ rc=1 chặn ở bước 0;
bơm token dạng `AKfycb…` vào `references/` ⇒ quét bắt đúng tệp/dòng, rc=2, KHÔNG đẩy.

Nhánh `claude/review-bhxh-law-profile-2m08hz` tách ra TRƯỚC khi r229 lên master nên phân kỳ thật:
master có r229 (v1.35.65), nhánh có r230 (v1.35.66) + r231 (v1.35.67). Merge gộp cả hai ⇒ cây kết quả
KHÁC mọi bản 1.35.67 phát hành trước đó, nên bump số mới thay vì giữ 1.35.67 (một số version = một cây).
Xung đột chỉ ở 4 chỗ mang số version (VERSION · hằng `VERSION` tl.py · header SKILL.md · CHANGELOG);
KHÔNG có xung đột logic — r229 chạm `nlm_ops`/`tl_gws`, r230/r231 chạm chunk + registry/enum.

**Bẫy đã sập và gỡ được — GIẢI XUNG ĐỘT PHẢI GIỮ LINE ENDING.** Lượt gỡ đầu viết lại `SKILL.md` và
`scripts/tl.py` bằng Python text-mode (`open(...,'w')`), nuốt CRLF→LF: SKILL.md 47966→47659 byte
(đúng 307 byte = 307 dòng), tl.py 223463→221776 (1687 dòng). Nội dung ĐÚNG, chỉ line ending sai.
Gate bắt: `golden-test` case `workflow_audit` lệch `kernel.size_bytes` 47966≠47659, kéo theo
`determinism-audit` + test `r219_gotchas_nhan_trang_thai`. ⇒ Hai tệp này là CRLF TOÀN BỘ; sửa bằng
script phải mở nhị phân hoặc `newline=''`. Đây là lý do golden 0-diff là GATE, không phải nghi lễ.

# ★ v1.35.67 — r231: 4 vá bắt được khi dọn hồ sơ Luật BHXH (2026-07-29)

## Ca 1 — rổ 46 nuốt Nghị định và cả CÔNG VĂN

Rổ 46 = «LUẬT sửa đổi ≥2 luật» ⇒ theo định nghĩa chỉ Luật/Bộ luật vào được. Guard cũ **chỉ chặn VBHN**,
nên phần CĂN CỨ của một Nghị định (trích ≥8 số hiệu luật) đủ kích `_distinct_target_luat_subjects >= 2`
⇒ `corpus-audit` đề xuất đẩy `ND_233-2025-ND-CP`, `ND_212-2025-ND-CP` và `CV_10593-NHNo-ALCO` vào 46.
Nhánh omnibus lại chạy TRƯỚC nhánh BHXH→02 nên nuốt luôn cả ca đúng.
**Vá:** tên mang tiền tố doctype khác luật (`ND_/TT_/QD_/NQ_/CT_/CV_/BC_/TTr_/PL_/VBT_/DUTHAO_/CU_/SCAN_`)
KHÔNG BAO GIỜ ép 46. Test giữ cả ca ĐÚNG (Luật omnibus thật vẫn → 46) lẫn guard VBHN cũ.

## Ca 2 — `NAME_TRICH_YEU` đổi tên phá bundle nhiều phần

Header của tệp bundle là header của tài liệu ĐẦU TIÊN trong đó, nên `_doc_subject_for_name` trích chủ đề
của một phần rồi đặt cho CẢ bundle: `VBT_Y_kien_gop_y_Luat_BHXH_16-7_phan_6_cua_8` →
`Luat_Cong_ngan_hang_nha_nuoc` (mất chỉ số phần, gắn tiền tố `Luat_` cho thứ không phải luật).
**Vá:** bỏ qua NAME_TRICH_YEU khi tên khớp `phan_N_cua_M` / `part_N_of_M` / `__partNN__`.

## Ca 3 — pipeline chunk ĐỨT ở chính khớp nối của nó

`chunk-apply` ghi `.md`, `profile-ingest` chỉ nhận doc/docx/odt/pdf/rtf/xls/xlsx ⇒
`profile-ingest-chunks` gọi con luôn `rc=2 UNSUPPORTED_EXTENSION`. Nới allowlist là SAI hướng (mở cửa cho
`.md` bất kỳ vào corpus). **Vá:** cầu nối tự vật chất hoá chunk thành `.docx` bằng **`zipfile` + XML thuần**
— KHÔNG thêm phụ thuộc (requirements.txt: stdlib-only). Front-matter giữ thành đoạn đầu (dấu vết + sha256),
thân giữ NGUYÊN VĂN; test đọc ngược `word/document.xml` khẳng định còn đủ, kể cả ký tự phải escape XML.

## Ca 4 — `loai_noncanonical` thiếu rổ cho TÀI LIỆU LÀM VIỆC

Điền `loai` cho 12 dòng đang RỖNG (bản so sánh ×3, ý kiến góp ý ×8, mục lục) làm `loai_noncanonical`
nhảy **4 → 16** dù dữ liệu TỐT LÊN — thước đo thiếu rổ, không phải dữ liệu sai. Cùng bệnh đã chữa 3 lần
trước (Hướng dẫn v1.34.31 · Công điện v1.30.1 · Điều ước v1.32.0).
**Vá:** thêm 6 loại vào enum — `Bản so sánh` · `Ý kiến góp ý` · `Bản thuyết minh` · `Bản đánh giá` ·
`Bản tổng hợp` · `Tài liệu làm việc` (kèm alias không dấu). Test có vế phản chứng: giá trị rác vẫn phải bị bắt.

`python scripts/tl.py --selftest` ⇒ **1387/1387** (thêm 3 ca r231).

# ★ v1.35.66 — r230: chunk NLM NUỐT khối đầu văn bản + Điều 1, `warnings` vẫn rỗng (2026-07-29)

> Bắt được khi đẩy Luật BHXH 41/2024 (bản Công báo 987+988, 183k ký tự) lên NotebookLM.

`_chunk_records_from_text` chỉ sinh chunk **TỪ tiêu đề Điều đầu tiên trở đi**, nên toàn bộ phần đứng
trước nó — cơ quan ban hành, **SỐ HIỆU**, tên luật, căn cứ Hiến pháp, `Chương I` — **biến mất không dấu
vết**. Cộng thêm guard `_is_heading` (PH2-08, vốn sinh ra để loại dẫn chiếu) **loại oan `Điều 1.`** vì
dòng ngay trước là `NHỮNG QUY ĐỊNH CHUNG` — tiêu đề cơ cấu, không kết bằng dấu câu.

| Đo trên Luật BHXH 41/2024 | trước | sau |
|---|---|---|
| `total_chars` | 183.428 | 183.428 |
| tổng ký tự các chunk | **182.678** (hụt **750**) | **183.428** (hụt 0) |
| `warnings` | `[]` — im lặng | `[]` (không còn gì để báo) |
| ranh giới | `part1 Điều 2..65` · `part2 66..141` | `part1 Điều 1..64` · `part2 65..141` |

Hậu quả nếu không bắt: nguồn NLM của luật gốc **thiếu cả số hiệu lẫn Điều 1** — hỏi "Điều 1 Luật BHXH
quy định gì" sẽ không có căn cứ, mà không chỗ nào báo lỗi. Ranh giới mới cũng **khớp** `_split_by_dieu_chunks`
(đã vá r229), hết cảnh hai bộ cắt cho hai kết quả.

**Vá:** (1) `_is_heading` chấp nhận thêm khi dòng trước là dòng cơ cấu (`Chương/Mục/Phần/Tiểu mục`
hoặc dòng TOÀN HOA ≤120 ký tự); (2) **bất biến bảo toàn** — phần đầu được gắn vào chunk 1, tổng ký tự
các chunk luôn == tổng ký tự nguồn.

Test `r230_chunk_khong_nuot_khoi_dau_va_dieu_1` khẳng định cả hai, kèm vế **phản chứng** (guard cũ loại
`Điều 1.` trên đúng fixture đó) để fixture hết tái hiện bug là ĐỎ chứ không xanh oan.

`python scripts/tl.py --selftest` ⇒ **1384/1384**.

# ★ v1.35.65 — r229: dẫn chiếu "Điều N" đầu dòng bị đếm thành TIÊU ĐỀ ⇒ split_plan cắt sai; registry-doctor nói rõ CƠ SỞ ĐẾM (2026-07-29)

> Phát hiện khi rà hồ sơ **Luật BHXH** và nạp bản **Công báo số 987+988 ngày 25-8-2024** của Luật BHXH
> 41/2024/QH15. Cả hai lỗi đều thuộc lớp «con số trông đúng nên không ai kiểm».

## Ca 1 — `_dieu_sequence_stats` đếm 161 Điều cho luật CÓ 141 Điều

Regex cũ `^\s*Điều\s+(\d+)\b` neo đầu dòng nhưng **không đòi dấu kết tiêu đề**. Bản `pdftotext` của
Công báo ngắt dòng giữa câu, đẩy **dẫn chiếu** lên đầu dòng — 20 mục thừa đều dạng
`Điều 109 của Luật này…`, `Điều 2 của Luật này bao gồm:`.

| Đo trên bản Công báo 41/2024 | count | monotonic | split_plan |
|---|---|---|---|
| luật CŨ | 161 | **False** | part 2 = **Điều 2**..141 (SAI, phải là 65..141) |
| luật MỚI | **141** | True | ranh giới đúng |

**Cùng một regex lỏng nằm ở HAI nơi** — và nơi thứ hai nặng hơn: `_split_by_dieu_chunks` dùng nó để **CẮT**,
nên chunk part 2 mở đầu ngay tại dẫn chiếu «Điều 2 của Luật này» nằm GIỮA THÂN Điều 64 ⇒ nguồn NLM bị
**xẻ giữa câu**, không chỉ sai nhãn.

| chunk_plan (Công báo 41/2024, 190k ký tự > ngưỡng NLM) | trước | sau |
|---|---|---|
| part 1 | Điều 1..64 | Điều 1..63 |
| part 2 | **Điều 2**..141 (cắt giữa thân Điều 64) | Điều **64**..141 |

**Vá:** một hàm `_dieu_head_marks` dùng chung cho ĐẾM lẫn CẮT — tiêu đề phải kết bằng `.`/`:` hoặc hết
dòng; **giữ fallback** luật cũ khi thể thức không có dấu (`Điều 5 Quy định chung`) ⇒ không văn bản nào tệ đi.

**Bẫy kiến trúc đã trả giá (đỏ 2 lượt):** hàm mới trong `tl_core` KHÔNG tự thấy nhau — 1646 hàm được
re-home `__globals__` về `tl.py`. Hàm phải khai thêm vào `_STUB_MAP["ingest_ops"]`; **hằng cấp module thì
KHÔNG có đường nào** (`_DIEU_HEAD_RE` NameError) ⇒ regex phải để TRONG thân hàm.

**Đo 2 chiều (bắt buộc theo CLAUDE.md):** bản GDoc sạch 141→141 (KHÔNG hồi quy) · bản PDF 161→141
monotonic. Test `r229_dieu_dan_chieu_dau_dong_khong_thanh_tieu_de` có **vế phản chứng**: khẳng định luật
CŨ trên đúng fixture đó ra 5 & không monotonic — fixture hết tái hiện bug là ca test ĐỎ, không xanh oan.

## Ca 2 — `registry-doctor`: `count` là TỔNG, mọi bucket lại tính trên phần ĐÃ LỌC

`analyze()` bỏ qua `row_kind='ref'` và bản gốc `loai='thuong'`, nhưng vẫn trả `count = len(rows)`.
Trên hồ sơ Luật BHXH: `count=90, missing_sohieu=19` ⇒ người đọc hiểu «19/90», thật ra là **19 trên 25
dòng được quét** (27 ref + 38 thuong bị loại); đếm thẳng registry có **56** dòng sohieu rỗng.
Tương tự `duplicate_sohieu_groups=0` trong khi dữ liệu có 2 nhóm trùng — đều rơi vào phần bị loại.

**Vá:** thêm `scanned` / `skipped_ref` / `skipped_own_thuong` / `basis` — đúng khuôn `sweep.corpus_basis`.
`scanned` vào `_DOCTOR_SUMMARY_KEYS` nên **text và JSON vẫn 1-1** (giữ bất biến H2).

## Kết quả
`python scripts/tl.py --selftest` ⇒ **1383/1383** (thêm 3 ca r229: đếm · cắt-chunk · cơ-sở-đếm).
# ★ v1.35.65 — r229: tuổi cookie NLM ra số ÂM vì mốc `last_validated` naive lệch múi giờ (2026-07-29)

> Phát hiện khi bootstrap gws/nlm trong sandbox Claude Code on the web (UTC) từ bundle stage ở máy
> UTC+7. `tl nlm-auth-load` in `~-0 ngày tuổi` — số âm, vô nghĩa. Không phải nhiễu hiển thị.

## Gốc

`profiles/default/metadata.json.last_validated` do nlm ghi theo **giờ của máy ghi nó** và là ISO
**NAIVE** (`2026-07-29T18:04:42`, không tzinfo). `_nlm_auth_age_days` trừ thẳng `datetime.now()` của
máy ĐỌC ⇒ trộn hai múi giờ. Đo được: lệch **465,6 phút** ⇒ tuổi = **−0,3 ngày**.

Sai số bị chặn bởi biên múi giờ thực (UTC-12..UTC+14 ⇒ ≤14h ≈ 0,58 ngày) nên KHÔNG lật nổi ngưỡng
14 ngày ở giữa dải — đừng thổi phồng. Cái đắt nằm ở ba chỗ khác:

| # | Hệ quả | Mức |
|---|---|---|
| a | In tuổi ÂM — sai hiển nhiên, làm mất tin vào mọi cảnh báo cạnh nó | hiển thị |
| b | SÁT ngưỡng 14 ngày thì nuốt mất cảnh báo re-stage | cảnh báo |
| c | **`_nlm_auth_load_downgrade` so tuổi bundle (mốc máy STAGE) với tuổi jar cục bộ (mốc máy NÀY)** — hai gốc thời gian khác nhau ⇒ bundle từ máy đi trước LUÔN ra tuổi âm ⇒ luôn `_b <= _l` ⇒ chốt phán "bundle tươi hơn" và CHO GHI ĐÈ | **NẶNG** — mở toang chốt chống hạ cấp r208c 3.1 |

(c) là thứ chốt r208c 3.1 sinh ra để chặn: nạp bản cũ đè lên jar tươi = tự giết phiên đang sống.

## Vá — `_nlm_lv_age_seconds` (PURE, tl_gws)

| Nhánh | Xử lý | Vì sao |
|---|---|---|
| có tzinfo | so tuyệt đối | đúng ở mọi máy |
| naive, tuổi ≥ 0 | DÙNG | cùng máy: chính xác. Khác múi: chỉ ĐỘI LÊN ≤14h — lệch về phía cảnh báo SỚM, an toàn ⇒ giữ nguyên mốc 2026-07-05 «ưu tiên last_validated» |
| naive, tương lai ≤ 120s | 0 | dung sai đồng hồ NTP |
| naive, tương lai > 120s | **None** | mốc vô nghĩa với đồng hồ máy này ⇒ rơi xuống `extracted_at` (epoch — tz-safe), KHÔNG bịa số âm |

Bản MIRROR `_nlm_auth_age_minutes` (tl_core/nlm_ops — nuôi cảnh báo trước lô
`NLM_COOKIE_BATCH_WARN_MIN`) mang y hệt bug, vá cùng quy tắc nhưng viết **INLINE**: hàm này re-home
`__globals__` về namespace tl (bẫy I11), thêm tên module-level ở đó sẽ NameError sau bind.

## Test khoá (4 ca) + phản chứng HAI CHIỀU

| Ca | Khẳng định | Gỡ vá |
|---|---|---|
| `r229_tuoi_cookie_khong_ra_so_am` | mốc tương lai ⇒ rơi xuống epoch, tuổi ≥ 0 và ĐÚNG (14,2′); kèm 3 nhánh aware/jitter/None | **ĐỎ** |
| `r229_chot_chong_ha_cap_khong_lat_vi_lech_mui_gio` | bundle cũ 3 ngày + mốc naive tương lai vs jar cục bộ 10′ ⇒ PHẢI kết luận HẠ CẤP | **ĐỎ** |
| `r229_mirror_nlm_ops_cung_quy_tac` | bản mirror trên HOME giả ⇒ 20 ngày theo epoch, không phải −466′ | **ĐỎ** |
| `r229_van_uu_tien_last_validated_khi_dung_duoc` | PHẢN CHỨNG: last_validated dùng được thì vẫn ƯU TIÊN (epoch stale 19 ngày không được thắng) | XANH (đúng vai: guard hồi quy, không phải ca bắt bug) |

Selftest **1384/1384**. Gỡ đúng 2 tệp logic (giữ test) ⇒ **1381/1384**, 3 ca trên đỏ.

Ruff `--select F` DELTA so master = **0** cả 4 tệp: tl.py 12/0 · tl_gws.py 91/4 · nlm_ops.py 176/0 ·
tl_selftest.py 3931/1. (Nền tl_selftest trong CLAUDE.md ghi 3914 đo ở v1.35.60 — đã trôi tự nhiên tới
v1.35.64; tiêu chí là DELTA, không phải con số tuyệt đối.)

## Không đổi

Cờ `BUNDLE_ROTATION_TOKEN_EXPIRED` giữ nguyên — nó ĐÚNG và độc lập với bug này. Đo cùng phiên: jar
tươi 14 phút vẫn có `__Secure-3PSIDRTS` hết hạn 4 phút (TTL loại cookie xoay ~10 phút) ⇒ cờ gần như
luôn bật sau mỗi lần nạp; `nlm login --check` LIVE xanh (139 notebook) và `nlm-auth-status`
`alive:true`. Cờ không phải phán quyết phiên chết, mà là cảnh báo ĐỘ BỀN: phiên không gia hạn được
nữa, có thể chết đột ngột ⇒ đừng mở lô dài. Phán quyết vẫn thuộc về probe LIVE.

# ★ v1.35.64 — r228: trả nốt nợ r227 — r218/r219 đỏ TỪ GÓI ĐÃ BUNG; mỗi bối cảnh một khẳng định + vá DỮ LIỆU mồ côi (2026-07-29)

> Món nợ r227 ghi rõ ở mục «Còn nợ»: `r218_docclaims_sach_khong_bao_gia` và
> `r219_docclaims_l9_tu_tat_khi_quet_hep` đỏ khi chạy từ gói bung (LIVE 1377/1379), đã đỏ y hệt trên
> 1.35.61 ⇒ CÓ SẴN. Cùng lớp bệnh r226/c: khẳng định của test/lớp guard ngầm giả định đang đứng trong
> CÂY GIT (có `.git`, có lịch sử, có `references/changelog_archive/`).

## Gốc — hai bệnh KHÁC NHAU dưới một triệu chứng

| Ca | Gốc thật | Vá |
|---|---|---|
| `r218_sach_khong_bao_gia` | Chính TEST gọi `git rev-parse` để dựng SHA đối chứng — gói bung không có `.git` ⇒ `returncode != 0` ⇒ đỏ vì CHỖ CHẠY | Khuôn r227: mỗi bối cảnh một khẳng định (bảng dưới) |
| `r219_l9_tu_tat_khi_quet_hep` | Ratchet `by_layer.L9 == 0` ĐỎ ĐÚNG: `CHECKPOINT_TEST_PLAN.md` + `COWORK_PROJECT.md` chỉ được `changelog_archive` (loại khỏi gói, `_RELEASE_EXCLUDE_DIRS`) trỏ ⇒ trong gói chúng MỒ CÔI THẬT, `DOC_NO_INBOUND_POINTER` ×2 | Vá DỮ LIỆU, KHÔNG nới guard: cấp con trỏ SỐNG trong `references/RUNBOOK.md` (header) — L9 phán đúng ở cả hai bối cảnh, giữ nguyên |

## r218 — mỗi bối cảnh một khẳng định (không nhánh nào xanh vì im lặng)

| Bối cảnh | Khẳng định |
|---|---|
| CÂY GIT (`.git` tồn tại) | như cũ: `git rev-parse` PHẢI chạy được, tài liệu đối chứng CÓ vế SHA thật, mọi lớp im |
| GÓI CÀI | tài liệu đối chứng BỎ vế SHA (không SHA nào chứng minh đúng được khi không có `.git`), các lớp L1/L3/L5/L6/L7 vẫn phải im; kèm khẳng định RIÊNG: gói KHÔNG được mang `references/changelog_archive/` (có = tệp dev lọt bundle) |

Xoá `.git` trong KHO ⇒ rơi vào nhánh gói, nhánh đó đòi archive phải VẮNG mà kho thật có archive ⇒ vẫn ĐỎ
— không tồn tại đường «thiếu dữ kiện thì cho qua» (hướng «guard tự tắt» đã THỬ VÀ BÁC từ r227: L2 tắt khi
clone nông làm chính ca test của nó đỏ trên runner).

## Test khoá mới `r228_docclaims_goi_khong_mang_tai_lieu_mo_coi`

Bắt NGAY TRONG CÂY GIT điều trước đây chỉ lộ khi bung gói: mọi phát hiện L9 (cờ LẪN advisory
`DOC_POINTED_ONLY_BY_HISTORICAL`) phải rơi vào tệp KHÔNG được đóng gói (`_release_should_include` false).
Tài liệu «chỉ lịch sử trỏ» trong cây git trông vô hại (advisory) nhưng vào gói là mồ côi thật — chính cái
lỗ r218/r219 lọt. Một khẳng định chạy được ở CẢ HAI bối cảnh, dùng chung lượt quét memo r223.

## Kèm đợt (trả nợ đúng dịp bump)

- `.gitignore` + `dist/` — sản phẩm build cục bộ, đã nằm trong `_RELEASE_EXCLUDE_DIRS`, có/không có nó
  làm đổi SHA cây làm việc so manifest.

## Nghiệm thu

- `tl --selftest` trong CÂY GIT: **1380/1380** (+1 ca r228).
- `tl --selftest` **TỪ GÓI BUNG** v1.35.64 (bung ra thư mục tạm ngoài kho, output ghi file rồi mới
  parse): **1380/1380** — món «Còn nợ» LIVE 1377/1379 của r227 đã trả.
- Phản chứng chạy được, mỗi bối cảnh một chiều, cả ba lượt ĐỎ ĐÚNG CA (worktree `--detach` + bản gói
  riêng, chạy xong dọn):
  · CÂY GIT, gỡ 2 dòng con trỏ trong RUNBOOK.md → đúng MỘT ca đỏ `r228_docclaims_goi_khong_mang_tai_lieu_mo_coi`
    (1379/1380; r219 VẪN XANH ở đó — chính cái lỗ chỉ-lộ-khi-bung-gói, nay có ca bắt ngay trong cây git);
  · GÓI BUNG, bơm `references/MO_COI_R228.md` mồ côi + xoá `references/GOTCHAS.md` → r218_sach + r219_l9
    + r228 cùng ĐỎ (xoá tệp trong gói bị bắt, không có nhánh «thiếu thì cho qua»);
  · GÓI BUNG, bơm `references/changelog_archive/` vào gói → đúng MỘT ca đỏ r218_sach (khẳng định riêng
    của nhánh gói không rỗng nghĩa).
- Bẫy TỰ CẤP CON TRỎ, cắn ngay khi chạy phản chứng lượt đầu (ghi lại vì sẽ cắn tiếp): docstring ca r228
  viết TRẦN tên hai tệp đủ đuôi ⇒ `scripts/*.py` là nguồn con trỏ sống của L9 ⇒ chính ca test tự cấp con
  trỏ, phản chứng gỡ-RUNBOOK xanh oan 1380/1380. Sửa cách viết (không tên trần đủ đuôi trong scripts/).
- `ruff check --select F` delta so master = **0**, đo CÙNG ruff 0.16.0 trên cả hai bản: tl.py 12 F821 +
  0 F401 (y nền); tl_selftest.py 3931 F821 + 1 F401 = master y hệt (nền «3914» trong CLAUDE.md là số
  của ruff đời cũ — đúng bài «thấy số lạ thì đo lại master trước khi nghi bản vá»).
- 8 bước gate offline: đều rc=0.

# ★ v1.35.63 — r227: ca r226/c đỏ khi chạy TỪ GÓI ĐÃ CÀI — test khẳng định về kho, chạy ở nơi không phải kho (2026-07-29)

> Bắt được bằng phép thử chưa từng làm: bung bundle v1.35.62 vào `~/.claude/skills/tra-luat/` rồi chạy
> `tl --selftest` **từ đó**. CI chạy trong CÂY GIT; LIVE chạy trong GÓI ĐÃ BUNG. Hai hình dạng khác nhau,
> và r225/r226 mới chỉ soi được hình dạng thứ nhất.

## Đo: cùng một gói, hai chỗ chạy

| Ca | 1.35.61 từ gói | 1.35.62 từ gói | Phán |
|---|---|---|---|
| `r216_merge_fail_closed_tren_duong_san_xuat` | ĐỎ | **XANH** | r226 chữa đúng cả ở hình dạng LIVE, không riêng CI |
| `r218_docclaims_sach_khong_bao_gia` | ĐỎ | ĐỎ | **có sẵn**, không phải hồi quy của r226 |
| `r219_docclaims_l9_tu_tat_khi_quet_hep` | ĐỎ | ĐỎ | **có sẵn** |
| `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` | — | **ĐỎ** | **do r226 gây ra** — vá ở đây |

## Gốc và cách vá

Vế (b) của r226/c đọc `.github/workflows/ci.yml` để khoá thứ tự hai dòng trong CI. Nhưng `.github/`
**cố ý không đóng gói**, nên ở gói cài tệp đó không tồn tại ⇒ ca đỏ vì CHỖ CHẠY, không vì drift.

Đã **BÁC** cách chữa hiển nhiên «thiếu tệp thì cho qua»: như thế thì xoá hẳn `ci.yml` trong kho cũng lọt
lưới — vá một báo giả bằng cách mở một lỗ thật. Thay vào đó mỗi bối cảnh gánh một khẳng định riêng, không
bối cảnh nào xanh vì im lặng:

| Bối cảnh | Khẳng định |
|---|---|
| trong CÂY GIT (`.git` tồn tại) | `ci.yml` PHẢI có, và dòng ghim `core.abbrev` + `fetch-depth: 0` phải đứng TRƯỚC bước `doc-claims-check` |
| trong GÓI CÀI | `.github/` PHẢI KHÔNG có — nếu có tức tệp dev lọt vào bundle, cũng là lỗi |

## Nghiệm thu

- `tl --selftest` trong CÂY GIT (Python 3.12): **1379/1379**.
- `tl --selftest` **TỪ GÓI ĐÃ BUNG**: ca r226/c nay XANH; còn đúng 2 ca đỏ `r218`/`r219` — **cả hai có sẵn
  từ trước r226**, đã đo trên chính bản 1.35.61.
- Gói lành: `tl_boot --version` → `tl 1.35.63`; 192 tệp; không lọt `.git`/`CLAUDE.md`/`.claude`/
  `.githooks`/`tra_luat_config.v2.json`.
- Phản chứng 2 chiều, **mỗi nhánh một chiều** (không nhánh nào xanh vì im lặng):
  · bơm `.github/workflows/ci.yml` VÀO GÓI → ca ĐỎ (khẳng định phía gói không rỗng nghĩa);
  · gỡ dòng ghim `core.abbrev` khỏi `ci.yml` TRONG CÂY GIT → ca ĐỎ (drift-lock cũ còn nguyên hiệu lực).
- 9 bước gate chạy tay trong cây git: đều rc=0.

## Còn nợ (đo được, cố ý chưa sửa)

`r218_docclaims_sach_khong_bao_gia` và `r219_docclaims_l9_tu_tat_khi_quet_hep` đỏ khi chạy từ gói cài, và
đã đỏ như thế từ TRƯỚC r226 (đo trên 1.35.61). Cùng lớp với ca vừa vá — lớp `doc-claims-check` giả định
đang đứng trong cây git — nhưng chữa chúng phải đụng thiết kế hai lớp guard, rộng hơn hẳn một dòng điều
kiện, nên tách ra đợt riêng. Hệ quả đang chịu: `tl --selftest` ở LIVE ra 1377/1379 chứ không N/N.

# ★ v1.35.62 — r226: CI đỏ ≥9 run KHÔNG phải lỗi test — lệnh cục bộ thuần chết ở cổng creds (2026-07-29)

> Việc đặt ra: CI đỏ liên tiếp từ 27-07 (r217) trên CẢ ubuntu lẫn windows, luôn đúng một ca
> `r216_merge_fail_closed_tren_duong_san_xuat`, trong khi cây dev 1376/1376 và worktree `--detach` cùng
> HEAD cũng 1376/1376. Giả thuyết đang treo là «CI ghim Python 3.12, dev 3.13». **Đo xong: sai giả thuyết.**

## Phân xử giả thuyết Python — bằng cách chạy CẢ HAI bản trên cùng một máy

| Bản Python | Máy KHÔNG config | Máy CÓ creds (`TL_WEBAPP`+`TL_TOKEN`) |
|---|---|---|
| 3.12.3 | **1375/1376** (đỏ đúng ca r216) | ca r216 xanh |
| 3.13.12 | **1375/1376** (đỏ đúng ca r216) | ca r216 xanh |

Cùng bản Python mà đổi kết quả theo *chỗ chạy*, còn đổi bản Python thì không đổi gì ⇒ biến thật KHÔNG phải
Python, cũng không phải OS. Biến thật là **máy có config hay không**.

## Nguyên nhân gốc: `rasoat-merge` thiếu ở `_CREDS_LAZY_CMDS`

`main()` gọi `load_creds` cho MỌI lệnh ngoài `_CREDS_LAZY_CMDS`. `rasoat-merge` không có trong tập đó, nên
trên máy trống nó `sys.exit` rc=1 **TRƯỚC handler** — dù handler tự khai «Không gọi mạng, không NLM». Ca
r216 chạy đúng đường sản xuất (subprocess) rồi parse `stdout`, mà stdout RỖNG ⇒ `JSONDecodeError` ⇒ FAIL.
Máy dev xanh chỉ vì có `tra_luat_config.v2.json` (`.gitignore` dòng 7) — runner clone sạch thì không.

Đây đúng LỚP bug đã cắn hai lần: `doc-text` (bug CI 16-07, khoá ở `r121`) và `doc-claims-check` (r218). Vá
lần này gom cả họ hàng r213, mỗi tên một bằng chứng riêng:

| Lệnh | Bằng chứng nó KHÔNG được chết ở cổng |
|---|---|
| `rasoat-merge` | handler thuần cục bộ, không có đường dùng creds |
| `state-get` | handler CÓ `except SystemExit → CAN_WEBAPP_LIVE` (rc=2 + JSON) — là **code chết** khi `main()` thoát trước |
| `state-put` | nhánh `--dry-run` return TRƯỚC `load_creds`; cùng nhánh `CAN_WEBAPP_LIVE` chết như trên |

Đo sau vá (máy trống): cả ba tới được handler, trả JSON schema của chính nó thay vì tường creds ở stderr.

## Blocker THỨ HAI, chỉ lộ ra khi selftest hết chặn: `doc-claims-check --strict` đỏ trên clone runner

r225 nối guard vào CI nhưng bước selftest đỏ đứng TRƯỚC nên guard **chưa từng chạy trên runner**. Chạy tay
trên clone `--depth 1` (đúng hình dạng `actions/checkout@v4` mặc định) ra **4 cờ cứng**:

| Cờ | Phân xử | Vá |
|---|---|---|
| L1 ×2 — `SKILL_KERNEL_DRAFT.md` | Guard bắt **ĐÚNG**: tệp chưa bao giờ có trong lịch sử git (`git log --all` = rỗng), chỉ tồn tại cục bộ trên máy dev. | Sửa TÀI LIỆU (`CONTEXT.md`, `references/SKILL_KERNEL_MAPPING.md`) nói đúng rằng đây là bản nháp không commit; **trả nợ** cặp tương ứng trong `_POINTER_BASELINE` (ratchet 4 → 3). |
| L2 ×2 — `ad413e7`, `78d6bfe` | Guard hô **SAI**: cả hai là commit THẬT (09-07 và 07-07); clone nông không có lịch sử để tra nên `cat-file -e` trượt. | `fetch-depth: 0` — cấp cho guard cái lịch sử nó cần để kết luận. |

## Ngưỡng L2 trôi theo KÍCH THƯỚC KHO — dòng ghim `core.abbrev` là dòng gánh việc

`sha_lens` lấy từ `git rev-parse --short`, mà git tự nới độ dài viết tắt theo số object. Cùng một kho:

| Hình dạng clone | `core.abbrev` | Hậu quả cho L2 |
|---|---|---|
| `--depth 1` | 7 | ngưỡng đúng như mọi phép đo r218 giả định |
| đủ lịch sử (281 commit, 17.783 object) | **8** | 8 = độ dài tiền tố UUID notebook (`743ed200`, `45739ff7`, `dbe706a0`…) ⇒ **18 cờ GIẢ**, và ca `r218_docclaims_l2_sha_khong_ton_tai` (mồi `deadbee`, 7 ký tự) **cũng đỏ theo** |

Nghĩa là bật `fetch-depth: 0` một mình sẽ đổi 4 cờ lấy 18 cờ. Nên CI ghim `core.abbrev 7` — **giữ đúng
ngưỡng mà r218 đã đo và thiết kế theo, không phải nới lỏng guard**. Đo sau khi ghim, trên clone ĐỦ lịch sử:
`doc-claims-check --strict` rc=0, **0 cờ cứng**, L2 vẫn BẬT hoàn toàn.

> Đã cân nhắc và BÁC hướng «L2 tự tắt khi clone nông»: nó làm chính ca
> `r218_docclaims_l2_sha_khong_ton_tai` đỏ trên runner (lớp tắt thì mồi `deadbee` không còn được bắt) —
> tức là chữa cờ giả bằng cách tắt guard ở đúng nơi guard cần chạy.

## Nghiệm thu

- `tl --selftest` trên Python **3.12**, container clone sạch KHÔNG config: **1379/1379** (+3 ca r226).
- 11/11 bước CI chạy tay trên chính container đó: đều rc=0; `release-bundle` ×2 cùng SHA-256, 192 entry.
- Phản chứng, hai lượt trong worktree `--detach` riêng (đã dọn):
  · gỡ 3 tên khỏi `_CREDS_LAZY_CMDS` → **3/3 đỏ đúng ca** (`r216_merge_fail_closed_tren_duong_san_xuat`,
  `r226_lenh_cuc_bo_khong_chet_o_cong_creds`, `r226_r216_khong_phu_thuoc_config_may_chay`), 1376/1379;
  · gỡ dòng ghim `core.abbrev` khỏi `ci.yml` → **1/1 đỏ đúng ca**
  (`r226_nguong_l2_troi_theo_abbrev_va_ci_ghim`), 1378/1379.
- Ca `r226_lenh_cuc_bo_khong_chet_o_cong_creds` chặn thẳng `load_creds` cho ném `SystemExit` rồi chạy
  `main()` THẬT ⇒ tất định trên MỌI máy, kể cả máy CÓ config (tước env không đủ: `_config_candidates` còn
  dò cwd/gốc-skill/`~`). Kèm NEGATIVE control: lệnh ngoài danh sách phải VẪN chết ở cổng.
- `doc-claims-check --strict`: **4 cờ → 0** (clone `--depth 1` trước vá; clone đủ + ghim abbrev sau vá).
- Ca `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` phản chứng 2 chiều trên kho git THẬT: cùng tài liệu, đổi
  mỗi `core.abbrev` mà kết luận L2 lật (7 ⇒ cờ cứng · 8 ⇒ advisory) + drift-lock hai dòng trong `ci.yml`.

## Còn nợ (đo được, cố ý chưa sửa)

Ngưỡng L2 vẫn tự hiệu chỉnh theo `core.abbrev` — CI nay ghim nên tất định, nhưng **máy dev không được
ghim**: khi kho lớn thêm và git nới viết tắt lên 8, `/gate` sẽ đỏ bằng đúng 18 cờ giả nói trên. Chưa sửa
trong lõi vì cần thiết kế riêng để phân biệt «tiền tố UUID» với «SHA viết tắt» — sửa kèm đợt nào đụng lớp
L2. Chữa tạm tại chỗ: `git config core.abbrev 7`.

# ★ v1.35.61 — r225: guard r218/r219 chỉ đóng ở đường TAY — nối `doc-claims-check` + `release-check` vào CI (2026-07-29)

> Việc đặt ra: đối chiếu con số «gate 8 bước» (prompt bàn giao) với «gate 9 bước» (ghi chép cũ). Đối chiếu
> cho ra: **không mâu thuẫn** — có HAI bộ gate khác tên gọi trùng, và đúng chỗ tiếp giáp giữa chúng là một
> lỗ hổng chưa ai thấy.

## Hai bộ gate — không cái nào là tập con của cái kia

| | `/gate` — 8 bước | CI — 9 bước |
|---|---|---|
| Nguồn | `.claude/commands/gate.md` | `.github/workflows/ci.yml` (job tên `gate`) |
| Chạy khi | người gõ TAY trong phiên | TỰ ĐỘNG: push master + PR, ubuntu × windows |
| Chỉ nó có | `doc-claims-check --strict` · `release-check --full` · `release-verify --strict` | `py_compile` · `release-bundle` ×2 same-SHA · `tl_boot --version` |

Cả hai con số đều đúng, khác đối tượng. Nhưng r218 dựng cổng kiểm trích dẫn, r219 nối nó vào `/gate` —
**đường TAY** — mà quên CI, **đường TỰ ĐỘNG**. Đúng câu r219 tự viết ở mục v1.35.55: «guard không nối vào
đường chạy tự động thì guard chỉ là tài liệu». Vá một reader chưa phải vá xong bẫy.

## Phản chứng 2 chiều CHẠY THẬT (worktree `--detach` riêng, đã dọn)

| Bước nối vào CI | Chiều XANH (checkout sạch) | Chiều ĐỎ (đột biến đúng ca) |
|---|---|---|
| `doc-claims-check --strict` | rc=0 | trích dẫn chết vào `references/GOTCHAS.md` → **rc=2** |
| `release-check --full` | rc=0 | `SyntaxError` ở `tl_core/the_thuc.py` → **rc=3** |
| `release-verify --strict` | rc=0 | file thừa `tl_core/rac_pc225.py` → **rc=2**, `extra_files` liệt kê đúng |

Chiều xanh đo trên worktree checkout sạch — **cùng hình dạng cây với CI runner**, không phải cây dev có rác.

## Hai ca LỌT LƯỚI, đã phân xử (không ca nào là chốt yếu)

1. **VERSION lệch → `release-check` vẫn xanh.** Đột biến SAI CA: `release-check --full` là bộ py_compile +
   `instruction_project_audit`/`instruction_nlm_audit` + `workflow_audit` in-process, nó không hề kiểm VERSION.
2. **File `.py` lỗi cú pháp MỚI trong `tl_core/` → `release-check` vẫn xanh.** Vì bước py_compile của nó chạy
   **danh sách tường minh 11 module**, trong khi `detail` lại ghi `"scripts/tl_core/*.py"` — nhãn nói glob,
   việc làm là danh sách. Đo tiếp: `tl_core/` nay **29 file .py**, tức **18 module** (`the_thuc`, `ingest_engine`,
   `classify`, `profile_mgmt`, `resolve`…) không nằm trong danh sách py_compile nào — cả `release.py` lẫn `ci.yml`.

★ **18 module đó KHÔNG hở**: bơm `SyntaxError` vào `the_thuc.py` → `release-check` **rc=3** và `tl --selftest`
**rc=3**, chỉ riêng `py_compile` danh-sách-tường-minh xanh. Nghĩa là danh sách kia **dư thừa và lệch nhãn, không
phải lỗ hổng** ⇒ CỐ Ý KHÔNG sửa trong r225: sửa nhãn `detail` là đụng `release.py` cho một lợi ích chữ nghĩa,
kéo theo trọn chu trình bump/gate/manifest/bundle. Ghi vào sổ để đợt nào đụng `release.py` thì sửa kèm.

★ Cùng phản chứng này cho thấy **giá trị gia tăng thật** của `release-check --full` trong CI: nó ĐỎ đúng ca mà
`py_compile` của CI xanh.

## Chốt

CI 9 → **11 bước**: `doc-claims-check --strict` chèn sau `golden-test` (đúng vị trí nó đứng trong `/gate`),
`release-check --full` trước `release-verify`, và `release-verify` nay mang `--strict`. Thứ tự giữ nguyên
`release-verify` TRƯỚC `release-bundle` — đảo lại thì `dist/a.zip`/`dist/b.zip` thành `extra_files` và `--strict`
đỏ oan. `.github/` cố ý nằm ngoài manifest/zip (từ v1.33.59) nên thay đổi này không đụng gói skill; bump version
là do CHANGELOG.md — file CÓ trong manifest.

# ★ v1.35.60 — r224: 5 «import thừa» F401 ở tl.py KHÔNG thừa — chúng là MẶT NAMESPACE của 1646 hàm re-home (2026-07-29)

> Việc đặt ra: dọn 5 F401 đầu `scripts/tl.py` (`base64` `datetime` `hashlib` `unicodedata` `zipfile`),
> tiền đề «import thừa THẬT vì thân tl.py đã tách sang tl_core». **Đo 29-07 BÁC tiền đề đó**: 4/5 tên có
> hàm gọi thật, và cơ chế giữ chúng sống không phải cái grep nhìn ra được.

## Vì sao cả grep lẫn phép kiểm «module có tự import chưa» đều phân xử NGƯỢC

| Phép đo | Số |
|---|---|
| Hàm tl_core có `__globals__` **IS** namespace tl.py | **1646** |
| Hàm re-home tra `unicodedata` | 19 |
| Hàm re-home tra `base64` | 9 |
| Hàm re-home tra `hashlib` | 3 |
| Hàm re-home tra `datetime` | 2 |
| Hàm re-home tra `zipfile` | 0 |

Hàm tách sang `tl_core` được **re-home** về globals của tl.py nên tra tên toàn cục ở **tl.py**, không ở tệp
gốc. Vì thế `tl_core/profile_mgmt.py` **có** `import datetime` mức module mà vẫn `NameError` khi tl.py
thiếu tên — mọi phép kiểm dựa trên «tệp gốc đã tự import chưa» đều cho kết luận ngược.

## Phản chứng 2 chiều (bắt buộc theo CLAUDE.md)

| Lượt | Thay đổi | Kết quả |
|---|---|---|
| 1 | bỏ cả 5 tên | selftest **ĐỎ** — `NameError: unicodedata` ở `tl_core/classify.py` |
| 2 | giữ `base64`+`unicodedata`, bỏ 3 tên còn lại | gate **ĐỎ** — `NameError: datetime` ở `tl_core/profile_mgmt.py` |
| 3 | giữ cả 5 + `# noqa: F401` | gate **XANH** |

Lượt 1–2 chứng minh khung đo CÓ lực phát hiện (không phải xanh giả) — đúng bài học r223.

## Chốt

Giữ nguyên 5 tên, tách sang dòng riêng mang `# noqa: F401` kèm số đo, để `noqa` **không** che import thừa
mới ở dòng trên. Mặt import lúc chạy **y hệt** master (14 tên, không thêm/bớt) ⇒ hành vi không đổi.
`ruff --select F scripts/tl.py`: **12 F821 + 0 F401**, delta F821 so master = 0.

# ★ v1.35.59 — r223: khung test NUỐT LỖI — «quét không chạy được» hoá trang thành «quét chạy rồi bất đồng» (+1 test, 1376/1376) (2026-07-29)

> Hồ sơ bàn giao ghi hai ca `r219_docclaims_l9_tu_tat_khi_quet_hep` và `…l10_l11_bi_bac` «đỏ chập
> chờn khi chạy nối nhiều lượt selftest», quy cho `_r218_run` dùng `subprocess timeout=300`.
> **Đo 29-07 BÁC chú thích đó**, và cái đo được ra lại là một khuyết nặng hơn.

## Vì sao `timeout=300` là nghi phạm sai

| Phép đo | Số |
|---|---|
| `doc-claims-check --json` toàn kho (35 tệp, JSON 58.386 B), đo đơn | **3,88 s** |
| Cùng lệnh, ép 6 luồng song song + selftest chạy nền | **8,5–10,2 s** |
| Trần `timeout` | 300 s |
| **Biên** | **30–77 lần** |

Chạy **4 lượt selftest nối** (109/118/173/134 s, lượt 3 đè lên phép ép tải): **4/4 đều 1375/1375**,
hai ca xanh cả 4 lượt, kho sạch cả 4 lượt. **Không dựng lại được hiện tượng.** Quá hạn chỉ là nghi
phạm đứng gần hiện trường.

## Khuyết thật

`_r218_run` phân xử báo cáo bằng `j = loads(...) if "{" in out else {}` — lượt quét sập, quá hạn hay
trả JSON hỏng đều quy về **`{}` lặng lẽ**. Mà đúng **hai ca gọi TRẦN** ấy là hai ca duy nhất **không
kiểm `rc`** (mọi ca `--path` đều kiểm `rc==0`/`rc==1`). Nên `{}` hoá trang thành BẤT ĐỒNG NỘI DUNG:
cả hai đỏ cùng lúc, **không ghi lý do**, không phân biệt nổi với một hồi quy thật.

★Trớ trêu: đó đúng là giáo lý mà chính ca `_l9_tu_tat` áp cho **sản phẩm** — «0 cờ vì sạch» ≠ «0 cờ
vì không chạy», nên lớp tự tắt phải khai báo qua `layers_skipped`. Giáo lý ấy bị vi phạm ngay ở tầng
**khung test**. Một khung test không nói nổi «tôi đã không chạy» thì mọi ca nó gác đều là báo cáo có
điều kiện.

## Vá

- **`_r218_phanxu()` tách riêng** — phân xử một lượt quét, nổ `_R218ScanChet` **kèm mã lý do**
  (`STDOUT_KHONG_CO_JSON` / `JSON_HONG` / `QUA_HAN_300s` / `BAO_CAO_THIEU_KHOA`) và ngữ cảnh lượt
  quét, thay vì trả `{}`. Tách rời để phản chứng bơm được đầu vào hỏng mà **vẫn là đường sản xuất**
  (`_r218_run` gọi đúng hàm này — không bind, theo doctrine `false-green-test-qua-bind`).
- **`_r218_run_toankho()` memo hoá** lượt quét toàn kho, chốt hình dạng báo cáo MỘT chỗ
  (`basis` + `layers` phải có). Hai ca gọi trần nay dùng **đúng một** lượt quét thay vì hai:
  selftest 1376 ca chạy **107,5 s** so với nền 109–134 s.
- **+1 ca `r223_khung_test_khong_duoc_nuot_loi`** — phản chứng 2 chiều: chiều xuôi đọc được báo cáo
  thật có rác đứng trước JSON; chiều ngược ba dạng hỏng phải nổ ĐÚNG mã lý do; ca thứ tư khoá memo
  (hai lần gọi phải trả về CÙNG một đối tượng).

★Không đụng `timeout=300`: đo cho thấy nó không phải cơ chế, và hạ trần xuống chỉ đổi một ca đỏ
không lý do thành một ca đỏ không lý do khác.

# ★ v1.35.58 — r222: dấu cách bị gạch trong .docx — bộ lọc markup ĐẺ RA chữ không có trong văn bản (+3 test, 1375/1375) (2026-07-28)

> Lượt rà hồ sơ đo ra `scripts/docx_markup.py` bỏ TRỌN run bị gạch **kể cả khi nội dung bị gạch chỉ
> là MỘT DẤU CÁCH** ⇒ hai từ dính liền. Đo trên `19-2026-VBHN-VPQH` (VBHN Luật BHXH — căn cứ đối
> chiếu Luật mẹ của cả hồ sơ) @121.553: `raw` = 187.401 ký tự, văn bản «hủy bỏ quyết định»;
> `strip`/`mark`/`auto` = 187.399 (**−2**, đúng 2 dấu cách bị gạch) ⇒ **«hủy bỏquyết định»**.
> **Nguồn viết ĐÚNG, công cụ làm hỏng.**

## Vì sao đây là lỗi nặng chứ không phải lỗi trình bày

Bỏ nhầm **chữ** = MẤT nội dung — dễ thấy, dễ bắt. Bỏ nhầm **dấu cách** = SINH nội dung mới: câu vẫn
đọc trôi, không ai soi, và chữ lạ ấy đi thẳng vào bản trích dẫn quy phạm. Dấu cách bị gạch là **tàn
dư định dạng**, không phải «chữ đã bỏ» theo nghĩa nghiệp vụ.

★Lỗi này **lật một bằng chứng của đợt rà trước**: «Điều 80 bản kho dính chữ *bỏquyết*» từng được
dùng để kết luận «bản Công báo đúng hơn» ở Luật 41/2024. Thực ra bản kho không sai — **bộ lọc sai**;
lỗi biến mất khi đổi nguồn chỉ vì bản mới không mang markup, tức **gỡ được tình cờ**. ⇒ *Một «lỗi
của dữ liệu» có thể là lỗi của ĐƯỜNG ĐỌC dữ liệu; đối chiếu `--markup raw` trước khi quy lỗi cho
nguồn.*

## Chỗ hỏng

`_cut_block`/`_cut_inline` xoá mẩu markup rồi mới hỏi có nhãn không, mà nhãn dựng bằng
`xml_chunk_text` — hàm này nén `\s+` rồi `.strip()`, nên trả `""` cho **CẢ** mẩu rỗng hẳn **LẪN**
mẩu chỉ-khoảng-trắng. Hai thứ đó phải xử lý **ngược nhau**, nhưng đường cũ không phân biệt được.
★Chế độ `mark` dính y hệt, dù nó đáng lẽ chỉ ĐÁNH DẤU chứ không xoá.

## Cách vá

- `scripts/docx_markup.py:76` — thêm `chunk_payload()`: chữ THÔ, **chỉ ruột `w:t`/`w:delText`**
  (`scripts/docx_markup.py:48`), giữ nguyên khoảng trắng, softbreak (`w:tab`/`w:br`/`w:cr`) tính là
  một dấu cách. Chỉ đọc trong phần tử text — **không** lấy mọi text lọt giữa tag, để docx bị in đẹp
  (xuống dòng giữa các tag) không bị hiểu nhầm là có khoảng trắng nội dung.
- `scripts/docx_markup.py:150` — `_keep_space()`: mẩu bị bỏ mà ruột **chỉ có khoảng trắng** thì trả
  **chính khoảng trắng đó** (không quy về một dấu cách), ngược lại trả `None` = bỏ như cũ. Áp ở **cả
  ba** chế độ: nhãn `⟦BỎ: ⟧` vừa là rác vừa không phải nội dung bị bỏ.
- Phủ đủ thể: `w:del` · `w:moveFrom` · run `w:strike`/`w:dstrike` · `delText` lạc
  (`scripts/docx_markup.py:177`, chỉ được thay bằng `w:t` vì đang nằm SẴN trong `w:r`).
- Thẻ sinh ra mang `xml:space="preserve"` — bắt buộc theo OOXML cho khoảng trắng đầu/cuối `w:t`.

Một chỗ vá phủ **mọi** reader: đo trước khi sửa — `strip_markup` là đường DUY NHẤT, 4 nơi gọi
(`scripts/normalize_document.py`, `scripts/tl_core/ingest_ops.py`, `scripts/tl_core/lookup_ops.py`),
**0 bản sao chép logic**. Đây đúng là chỗ r182 từng trả giá (vá một reader, còn hai reader kia sai
tiếp), nên lần này kiểm trước bằng phép đo chứ không bằng trí nhớ.

## Phản chứng — và đột biến lọt lưới là phát hiện đáng giá nhất

**8 đột biến THẬT vào mã sản xuất, chạy bộ test ĐÓNG GÓI (không phải harness rời): 8/8 đỏ đúng ca.**
Riêng M5 («nới thành giữ tất») đỏ thêm **11 ca r182** — đúng, vì nó phá luôn bất biến cũ.

★**Lượt đầu M2 LỌT LƯỚI, và nó lật chính lời chú thích vừa viết.** M2 = bỏ vế `pay and` trong
`pay and not pay.strip()`. Chú thích ban đầu bảo vế ấy chống «đẻ dấu cách ma ở mọi ranh giới đoạn» —
**sai**: mẩu rỗng trả `""`, mà `"" is not None`, nên cái sinh ra là `<w:t></w:t>` **RỖNG**, tức VĂN
BẢN không đổi. Khác biệt thật nằm ở mức **XML**: `<w:del …/>` tự đóng (đánh dấu xoá dấu-đoạn) có
trong MỌI docx track-changes, nên bỏ vế này là chèn một run rỗng vào **mọi ranh giới đoạn** — phá
bất biến thiết kế «chỉ CẮT/BÓC tag markup, KHÔNG đụng gì khác» (cùng họ `r182_no_markup_is_noop`).
⇒ ca khoá đổi sang **so ở mức XML** (`_o == _x` trừ đúng cái tag) rồi M2 mới chết.

*Bài học giữ lại:* chốt đúng việc mà **chú thích sai lý do** còn nguy hơn chốt thừa — phiên sau đọc
chú thích rồi gỡ nhầm. Đột biến là thứ duy nhất phân xử được điều đó.

## Hai lỗi của chính đợt này, ghi để khỏi lặp

1. **Phép kiểm toàn vẹn lấy MẪU không phải là phép kiểm toàn vẹn.** Harness phản chứng bị giết giữa
   chừng ⇒ `finally` không chạy ⇒ đột biến M3 **nằm lại trên mã canonical**. Tôi kiểm bằng
   `git diff --numstat` (36/2) + `grep` **một dòng** ⇒ cả hai đều xanh, vì M3 thay 2 dòng bằng 2
   dòng và không đụng dòng được grep. Lượt chạy sau lấy chính file bẩn làm «bản pristine» ⇒ bản sao
   lưu cũng nhiễm. **Toàn vẹn phải đo bằng hash CẢ TỆP; bản gốc phải lấy từ trạng thái đã xác minh.**
2. **Chốt chống rỗng, lần thứ hai trong hai đợt liên tiếp.** Harness in `?/?` khi không parse được
   kết quả, mà chốt `base_ok != base_tot` vẫn xanh vì **so hai dấu `?` với nhau**. Nay nền phải là
   **số thật** và phải **đúng bằng** số ca mong đợi mới được chạy tiếp.

## Ranh giới — r222 vá CÔNG CỤ, không tự sửa DỮ LIỆU

Record cache `19-2026-VBHN-VPQH` **vẫn còn** «bỏquyết» (đúng 1 chỗ trên toàn cache 11 record; 10
record kia `markup=null` nên không dính). Cờ `markup strike=2` treo trên record ấy **vẫn báo** sau
r222: `scan()` đếm theo THỂ, không phân biệt gạch-chữ với gạch-khoảng-trắng — cố ý không đổi, vì
thêm trường vào `stats` là đổi lược đồ đã ghi vào record. Người thẩm tra quyết **không nạp lại**
lượt này.

*Đây là lần thứ tư một đợt phải nhắc lại cùng một câu: **vá công cụ không tự sửa dữ liệu công cụ đã
làm hỏng.***

# ★ v1.35.57 — r221: cổng T1 số hiệu của `verify_deep` — sửa một phép so CHƯA TỪNG khớp đúng lần nào (+2 test, 1372/1372) (2026-07-28)

> Lượt rà hồ sơ đo ra `verify_deep.py:287` sai ở **11/11** record cache: nó gắn cờ «không thấy số
> hiệu» cho **cả những bản in đúng chuẩn**. Không phải hồi quy — cổng này chưa bao giờ khớp đúng
> một lần nào. Và lại đúng khuôn r219/r220: **phép đo bác chính đề xuất đầu tiên**, lần này là đề
> xuất của phiên đang làm.

## Chỗ hỏng

`re.escape(so_hieu.split("/")[0])` chỉ có nghĩa với dạng IN trên văn bản («41/2024/QH15»), nhưng
đường nạp truyền **khoá registry** gạch ngang («41-2024-QH15») — không có `/` nào để tách, nên
`split("/")[0]` trả về nguyên khoá rồi đem so nguyên chuỗi với văn bản dùng gạch chéo. Cùng họ lỗi
mà r219 đã bác ở L11: **lẫn khoá registry với trích dẫn văn xuôi**.

Phải xử lý **cả ba** khác biệt, cả ba đã có sẵn ở `scripts/tl_core/classify.py:64-94` mà
`verify_deep` chưa mượn (`scripts/build_cache.py:65-66` mới làm một phần ba):

1. gạch ngang (khoá) vs gạch chéo (bản in);
2. **`Đ`/`đ` (U+0110/U+0111) KHÔNG phân rã bằng NFKD** — phải thay TRƯỚC khi bỏ dấu, nếu không
   `[^a-z0-9]` xoá thẳng và «158/2025/NĐ-CP» nén thành `1582025ncp`;
3. VBHN in **không có năm** («19/VBHN-VPQH» vs khoá «19-2026-VBHN-VPQH»).

## Phạm vi tìm — đo theo bậc, không chọn theo cảm giác

Layout VPQH in «Số: NN/VBHN-XXX» **chỉ ở khối XÁC THỰC cuối bài** (đo: `54/VBHN-VPQH` ở vị trí
105.362/108.650) ⇒ chỉ soi head-2000 là bỏ sót. Nhưng **quét toàn văn thì nới quá tay** — khối CĂN
CỨ dẫn số hiệu văn bản KHÁC:

| phạm vi | tự-khớp | lọt NHẦM |
|---|---|---|
| phép cũ | **0/11** | — |
| head-2000 | 9/11 | 3/110 |
| toàn văn | 10/11 | **6/110** ✗ |
| **head-2000 + tail-4000** | **10/11** | **3/110** ✓ |

Chọn head+tail: nhạy hơn head-thuần một bậc mà mức lọt nhầm **đúng bằng** nó. Tail 3000 còn sót
(hit cách cuối 3.288), 6000 không đổi, 10000 bắt đầu ăn vào thân (4/110). Cờ duy nhất còn lại sau
khi vá là `89-2026-VBHN-VPQH` — **báo đúng**: số hiệu vắng mặt trên toàn bộ 127.359 ký tự.

★Chốt `if not fold: return False` đặt trên **số hiệu đã nén**, không trên phạm vi: số hiệu rác
(«///») nén ra chuỗi RỖNG, mà `"" in x` đúng với mọi `x` ⇒ chốt theo phạm vi rỗng như bản nháp đầu
chỉ đỡ được khi văn bản CŨNG rỗng.

## Nghiệm thu

* Selftest **1370 → 1372** (+2 ca `r221_*`), nạp THẲNG `verify_deep.py` không qua bind (bẫy r212).
* **Phản chứng CHẠY THẬT 8/8 đỏ đúng ca.** ★M8 (bỏ `.replace("đ","d")` chữ thường) ban đầu **KHÔNG**
  làm test đỏ ⇒ theo luật kho đó là mã chết; đã bổ sung ca nguồn-viết-thường thay vì gỡ chốt, vì
  chốt là bản mượn nguyên của `classify.py` và phá tính đối xứng mới là chỗ hỏng sau này.
* Ca đối chứng **bắt buộc chứa chữ Đ** — ca QH15/VBHN (vốn không có Đ) để phép sai **vẫn xanh**;
  phiên trước đã tự sa vào đúng bẫy này hai lần.
* Test đi qua `t1_structure` chứ không chỉ gọi hàm con — bài học r219: guard không nối vào đường
  chạy thì guard chỉ là tài liệu.
* ruff F delta **0**. Không đụng dữ liệu cache/registry/corpus.

# ★ v1.35.56 — r220: doc-claims-check trả nốt L4 (giàn giáo nháp) — và phép đo cắt `XXX` trần khỏi đề bài (+2 test, 1370/1370) (2026-07-28)

> Nợ CỐ Ý cuối cùng của kế hoạch r218. Vẫn đúng bài học r219 — ĐO TRƯỚC KHI THIẾT KẾ: phép đo lần
> này cắt hẳn một phần đề bài (`XXX` trần) trước khi nó kịp thành ~100% báo giả, và cho sẵn ranh
> giới cờ-vs-advisory đúng ngay từ dòng code đầu tiên.

## L4 — giàn giáo nháp còn sót trong văn xuôi

`{{...}}` (reason `DRAFT_PLACEHOLDER`) và `TODO`/`TBD`/`FIXME`/`XXX` (reason `DRAFT_MARKER`) trong
VĂN XUÔI: tài liệu sống trình bày như đã xong mà còn chỗ-điền thì không hoàn cảnh nào đúng ⇒ **cờ**;
tài liệu lịch sử nhắc lại là ghi chép ⇒ advisory (cùng khuôn L1/L8). Quét trên bản đã che CẢ fence
LẪN span backtick — marker nằm trong fence/span là ví dụ hay ký pháp đang được MÔ TẢ, không phải
trạng thái của chính tài liệu.

★Đo 2026-07-28 TRƯỚC khi viết dòng code nào (đúng khuôn đã bác L10/L11 ở r219):

* `{{...}}` / `<TODO>` / `TBD` / `FIXME` = **0 hit toàn kho** — bốn khuôn vào là xanh sẵn.
* **12/12 hit `XXX` toàn kho là placeholder cơ-quan-ban-hành trong ký pháp số hiệu
  `NN-YYYY-VBHN-XXX`** — tất cả kề dấu `-`. Bắt `XXX` trần như kế hoạch r218 đặt hàng thì lớp này
  khai trương bằng ~100% báo giả. Giữ `XXX` nhưng **loại hit kề `-`** (đúng phép loại trừ mà L2
  dùng cho khúc UUID notebook) ⇒ 0 báo giả mà vẫn bắt được `XXX` đứng rời.
* Hit `TODO` DUY NHẤT toàn kho nằm ở `references/DOCTRINE_APPENDIX.md` (tài liệu lịch sử) ⇒ vào kho
  đúng **0 cờ + 1 advisory** — gate `--strict` không đổi màu, cùng khuôn "vào kho là xanh sẵn" của
  L8/L9.

## Nghiệm thu

* Selftest **1368 → 1370** (+2 ca `r220_*`): ca cờ với BA đối chứng trong CÙNG tài liệu (`XXX` kề
  `-`, marker trong span, marker trong fence — cả ba phải IM); ca PURE lịch-sử-hạ-advisory nạp
  thẳng `workflow.py` không bind + ratchet 0 cờ L4 trên kho thật.
* **Phản chứng 2 chiều CHẠY THẬT trên bãi cách ly, 7 đột biến: 7/7 đỏ đúng ca** — M1 bỏ loại trừ kề
  `-` · M2 quét thiếu che span · M3 bỏ hạ advisory lịch sử · M4 bỏ L4 khỏi danh sách lớp · M5 hỏng
  regex placeholder · M6 mask thôi che fence (đỏ CẢ guard che-nhiễu `r218_*` = đúng, mask là của
  chung) · M7 bỏ `TBD` khỏi họ marker. Không đột biến nào lọt lưới ⇒ không giữ chốt chưa chứng minh.
* Golden `doc_claims_check_fixture` regen CÓ CHỦ ĐÍCH: fixture (SINH TỪ MÃ trong
  `_golden_ensure_fixtures`) thêm cặp nổ/im trên cùng một dòng + marker trong fence; `by_layer`
  thêm `L4: 2`, `claims_flagged` 10→12, `layers` thêm L4. `workflow_audit` KHÔNG đổi (card không
  bị hash). Card `doc_claims_check.json` thêm dòng plan L4.
* ruff F delta **+1 và là `F821 Undefined name Path`** ở `tl_selftest.py` (194→195 — đúng lớp báo
  giả GOTCHAS §11: tên bơm động vào `globals()` qua `_STUB_MAP`; test mới dùng `Path(td)` đúng
  khuôn các ca `r219_*`). Gate 8/8 xanh trọn, gen_instructions 38/38, bundle dựng ×2 trùng byte.

# ★ v1.35.55 — r219: doc-claims-check thêm L8/L9, BÁC L10/L11 bằng đo, và vá 3 sự thật sai trong chính GOTCHAS.md (+7 test, 1368/1368) (2026-07-28)

> Đợt này trả nốt nợ CỐ Ý của r218. Kết quả đáng ghi nhất **không phải hai lớp mới**, mà là ba lần
> phép đo bác thẳng thiết kế đã đặt hàng: hai lớp bị loại vì đo ra ~100% báo giả, một lớp phải đổi
> hẳn định nghĩa vì định nghĩa gốc **bất khả thi hành**. Xây theo kế hoạch mà không đo trước thì cả
> ba đều đã lọt vào kho và làm hỏng đúng cái khiến báo cáo dùng được: ranh giới cờ-vs-advisory.

## (a) L8 — tên lệnh `tl <cmd>` không tồn tại

Lớp đúng trọng tâm của cả lệnh: tài liệu bảo phiên sau chạy một lệnh KHÔNG CÓ thì phiên đó đi thẳng
vào ngõ cụt — không cách nào đúng ⇒ **cờ**, không phải advisory. Nguồn sự thật là golden
`references/golden/parser_surface.json` (191 lệnh, repo-local, tất định, đã bị `golden-test` khoá byte)
chứ KHÔNG import `build_parser` — import tl.py trong handler kéo theo `load_creds`, thứ mà lệnh
READ-ONLY offline này cố ý không đụng. Thiếu golden ⇒ lớp **tự tắt và khai báo**, không đoán.

Chỉ quét TRONG span backtick. Đo 28-07: quét trần bắt 8 hit và **cả 8 đều là báo giả tiếng Việt** —
`tl cho` (từ "…hằng trong tl cho"), `tl selftest` (từ "**tl selftest 338/338**"), `tl rebase` (từ
"globals tl rebase → NameError"). Trong-span còn 4, cả 4 nằm ở sổ lưu trữ ⇒ **0 cờ trên tài liệu sống**.

## (b) L9 — tài liệu mồ côi. ★Định nghĩa của kế hoạch BỊ BÁC

Kế hoạch r218 định nghĩa mồ côi = «vắng trong mục DANH MỤC REFERENCES của SKILL.md». **Đo: 20/29 tệp
`references/*.md` vắng** ⇒ lớp này hô 69% cây tài liệu. Tệ hơn — cách "sửa" duy nhất là thêm 20 dòng
vào SKILL.md, trong khi kernel chỉ còn **162 B** đệm tới trần WARN ⇒ **lớp BẤT KHẢ THI HÀNH**. Danh
mục kernel là bản CHỌN LỌC có chủ đích (9 mục + 2 glob), đọc nó thành chỉ mục là đọc sai chức năng.

Định nghĩa dùng được, đo ra **0 cờ + 2 advisory** (vào kho là xanh sẵn):
* cờ `DOC_NO_INBOUND_POINTER` — KHÔNG nguồn nào trong kho nhắc tới (md đã quét + mọi `.py` + workflow
  card + `docs/adr`). Tệp nằm trong gói mà không đường nào dẫn tới = BẤT KHẢ đúng.
* advisory `DOC_POINTED_ONLY_BY_HISTORICAL` — chỉ CHANGELOG/sổ lưu trữ nhắc.

L9 chạy MỘT LẦN cuối lượt và **chỉ khi lượt quét đủ rộng** (có `SKILL.md` + ≥1 tệp `references/`);
quét hẹp thì mọi tệp khác đều "không ai trỏ tới" — kết luận vô nghĩa sinh 28 cờ rác.

## (c) L10 và L11 — CỐ Ý KHÔNG LÀM, lý do đi THEO SẢN PHẨM

Kế hoạch xếp L11 vào "hai lớp đáng nhất". Đo bác cả hai; lý do nằm ở `basis.layers_bac` của mọi lượt
chạy (và có test khoá) để phiên sau khỏi "bổ sung nốt" rồi tự đổ rác vào báo cáo mình cần đọc:

* **L11 số hiệu VBQPPL thiếu NĂM** — 20 hit/5 tệp, 18 ở tài liệu lịch sử, **đúng 2 ở tài liệu sống và
  cả 2 viết ĐÚNG**: `62/VBHN-VPQH` (SKILL.md) là số hiệu CHÍNH THỨC in trên văn bản; `88/VBHN-VPQH`
  (COMMANDS.md) nằm trong câu đang MÔ TẢ việc v1.33.47 cố ý chấp nhận dạng bare. Bất biến
  `NN-YYYY-VBHN-XXX` áp cho **khoá registry**, không áp cho trích dẫn văn xuôi — và mặt registry đã có
  cổng riêng (`vbhn-year-fix`). Bản thu hẹp "bare number ĐA NGHĨA" thì cần tra registry cache ⇒
  máy-phụ-thuộc, phá tính tất định của golden.
* **L10 GAS version thiếu `Code.<ver>.gs`** — 30 version được dẫn, chỉ 6 có tệp ⇒ 24 cờ. Kho giữ 6 bản
  gần nhất là CÓ CHỦ ĐÍCH; và chính việc viết `Code.<ver>.gs` vào tài liệu đã làm guard con trỏ r209 đỏ.

## (d) Việc B — nhãn trạng thái GOTCHAS.md, và 3 sự thật SAI trong chính nó

Ràng buộc đo trước khi gõ: test `r127_gotchas_doc_pointer_driftlock` khoá 4KB ≤ file ≤ 12KB; file đang
**11.784 B ⇒ đệm 504 B**, không phải "~10KB còn ~2KB" như kế hoạch ghi. Dán nhãn cho cả ~42 bẫy tốn
~588 B ⇒ không vừa. **Không nới trần** (nới ratchet cho code mình xanh chính là "vá quá tay") mà cắt
chữ chỗ khác — đúng nếp file này tự dặn. Kết: **12.276 B, còn đệm 12 B.**

Nhãn chỉ dán ở chỗ trạng thái ĐÃ ĐỔI (`[B]` = tiền đề BỊ BÁC); không nhãn = còn hiệu lực. "Còn hiệu
lực" là mặc định nên nhãn cho nó không mang tin — dán tất cả vừa hết byte vừa loãng tín hiệu.

Ba mục sửa, cả ba đều là **số/kết luận sai đang nằm trong tài liệu bẫy**:
1. **§9 cookie NLM** — «cookie DBSC đời ~1h, `nlm login` là đủ» BỊ BÁC (đo 26+27-07): không cookie nào
   TTL 1h; chết do token XOAY `__Secure-1PSIDRTS`; **`nlm login` trần là NO-OP** (probe homepage → xanh
   giả, rc=0) ⇒ phải `--force`. Đây là mục nguy hiểm nhất vì câu gốc đọc như hướng dẫn vận hành.
2. **§1 trần kernel** — ghi "hiện ~49.145B, đệm 7B" (số TRƯỚC KERNEL-DIET r128), đo thật **47.966 B,
   đệm 162 B tới WARN 48.128** ⇒ lệch ~1,2 KB.
3. **§3 kiểu xuống dòng** — ghi "repo ghi LF, riêng COMMANDS.md CRLF". Đo: **8 tệp CRLF TOÀN PHẦN**
   (gồm `SKILL.md`, `tl.py`, `tl_selftest.py`), 200 tệp LF, 0 hỗn hợp. Chính đợt này trả giá: bump
   version bằng `write_text` nuốt sạch CR của SKILL.md (307 dòng) — `git diff --numstat` bắt được ngay,
   đã hoàn tác và làm lại ở mức BYTE.

## (e) Hiện vật manifest restricted-egress (F16c)

`references/PATCH_v2.21.1.gs.md` khuyến nghị bản **restricted-egress** làm MẶC ĐỊNH nhưng tệp không có
trong kho — chỉ ghi cách tự dựng ⇒ người vận hành theo đúng khuyến nghị thì không có gì để copy. Nay có
`references/APPSSCRIPT_MANIFEST.restricted-egress.json`, và test khoá bất biến thật sự nguy hiểm: hai
manifest chỉ được khác nhau ĐÚNG khoá `urlFetchWhitelist` — lệch thêm khoá nào khác nghĩa là đổi policy
egress đã âm thầm kéo theo đổi oauthScope/quyền webapp.

## (f) ★r218 làm ra cái cổng nhưng QUÊN nối vào gate

`doc-claims-check` **không hề có trong `.claude/commands/gate.md`** (7 bước, sửa lần cuối ở `cece035`,
từ trước r218). Nghĩa là suốt r218 cái lỗ hổng nó sinh ra để bịt vẫn chỉ đóng khi có người NHỚ chạy tay
— đúng loại hỏng mà chính nó đi bắt. r219 nối vào: gate nay **8 bước**, `doc-claims-check --strict` đứng
sau `golden`. Guard không nối vào đường chạy tự động thì guard chỉ là tài liệu.

## Nghiệm thu

* Selftest **1361 → 1368** (+7 ca `r219_*`), **gate 8/8 xanh trọn** (kể cả bước mới), gen_instructions
  38/38, ruff F delta **0 thực chất** (+1 và là `F821 Undefined name Path` ở `tl_selftest.py` 193→194 —
  đúng lớp báo giả GOTCHAS §11 đã ghi: tên bơm động vào `globals()` qua `_STUB_MAP`).
* **Phản chứng 2 chiều CHẠY THẬT trên bãi cách ly, 2 lượt / 18 đột biến.** Lượt 1: 9/11 đỏ đúng ca —
  và **2 ca lọt lưới đều là phát hiện thật**, không phải trục trặc harness:
  * M2 lọt ⇒ ca đối chứng thiếu tên profile CHỮ THƯỜNG (bản viết hoa rơi ngoài `[a-z]` của `CMD_RE`
    nên im lặng kể cả khi guard bị tắt) ⇒ đã bổ sung dòng đo được.
  * M3 lọt ⇒ **`_doc_claims_noisy` trong `_doc_claims_tl_cmd` là MÃ CHẾT** (`CMD_RE` chỉ nhận
    `[a-z][a-z0-9-]{2,}` nên mọi ký tự nhiễu đã rụng trước) ⇒ **gỡ**. Một chốt không đột biến nào giết
    được là chốt CHƯA ĐƯỢC CHỨNG MINH; giữ lại chỉ tạo cảm giác an toàn giả.
* Golden `doc_claims_check_fixture` regen CÓ CHỦ ĐÍCH: `by_layer` thêm L8/L9, `layers` thêm L8/L9,
  `layers_skipped.L9` (bằng chứng lớp tự tắt đúng lúc), và ca L8 mới khoá byte (`tl sweep` KHÔNG nổ,
  `tl khong-co-lenh-nay` nổ đúng dòng 7). ★Bẫy trả giá một lượt: fixture dưới `references/golden/
  fixtures/` **SINH TỪ MÃ** (`_golden_ensure_fixtures`) — sửa tay bị ghi đè lặng lẽ ở `golden-test` kế
  tiếp, phải sửa trong `workflow.py`. (`workflow_audit` KHÔNG đổi: nó không đếm `references/*.json`.)

# ★ v1.35.54 — r218: `tl doc-claims-check` — cổng kiểm TRÍCH DẪN trong văn xuôi, và 8 con trỏ chết nó bắt được ngay lần chạy đầu (+9 test, 1361/1361) (2026-07-28)

> Lỗ hổng đã ĐO, không phải phỏng đoán: gate 9 bước kiểm mã nguồn + manifest + bundle, **không bước nào
> kiểm tính đúng của trích dẫn trong tài liệu**. Trong khi `CHANGELOG.md`, `GOTCHAS.md`, `RUNBOOK.md`,
> `DOCTRINE_APPENDIX.md` dày đặc `r216`, `9279426`, `tl.py:1504`, `references/X.md`, `v1.35.52`.
> Khuôn hỏng đã trả giá nhiều lần: tài liệu dẫn tệp–cờ–số hiệu đã đổi chỗ, không ai phát hiện cho tới
> khi một phiên sau đi theo con trỏ và lạc. Đúng loại lỗi máy bắt rẻ hơn người.

## (a) Lệnh mới `tl doc-claims-check` — READ-ONLY, sáu lớp, fail-CLOSED khi `--strict`

```
tl doc-claims-check [--path <file|dir> ...] [--strict] [--json] [--out <file>]
```

Không ghi (trừ `--out` do người gọi khai), không mạng, không GAS/NLM, **không có `--apply`/`--fix`**.
`rc` 0 sạch · 1 có cờ · 2 lỗi dùng lệnh; `--strict` đẩy 1→2 (khuôn `workflow-audit --strict`).

| Lớp | Bắt gì | Xác minh bằng |
|---|---|---|
| L1 | đường dẫn trong span backtick có `/` | tồn tại trong cây (hoặc cạnh tài liệu) |
| L2 | commit SHA | `git cat-file` + `merge-base --is-ancestor` CỤC BỘ |
| L3 | link markdown tương đối | resolve TỪ VỊ TRÍ TÀI LIỆU |
| L5 | `v1.NN.NN` | ≤ VERSION hiện hành + có trong sổ |
| L6 | `rNNN` (chấp hậu tố `r208d`) | ≤ đợt mới nhất + có trong sổ |
| L7 | `<file>.py:<dòng>` | tệp tồn tại **và** đủ số dòng |

Che nhiễu (§2.4) giữ nguyên offset nên số dòng báo cáo vẫn đúng: khối fence ```` ``` ````/`~~~` che cho
mọi lớp; span backtick che THÊM cho L2/L5/L6 (SHA/version trong ví dụ lệnh là minh hoạ), nhưng **không**
che cho L1/L7 — đường dẫn và con trỏ mã vốn luôn nằm trong backtick, che đi là mù.

## (b) Ranh giới CỜ vs ADVISORY — thứ quyết định báo cáo dùng được hay thành rác

Bản đầu tiên hô **213 cờ**. Đọc kỹ thì phần lớn là lỗi của chính công cụ, và mỗi lần sửa đều phải ĐO:

- **56 cờ `VERSION_AHEAD_OF_CURRENT` đều là `v2.x`** — version **webapp GAS** (`2.21.2p`), hệ đánh số
  KHÁC hẳn VERSION skill. Kế hoạch viết `v1.NN.NN` là có lý do; siết regex về nhánh `v1.*`.
- **18 cờ `SHA_NOT_A_COMMIT` đều dài ĐÚNG 8 và đều là khúc đầu UUID notebook** («query notebook
  `fec6c125`»), trong khi git ở kho này viết tắt **7**. Ngưỡng nay lấy từ chính git
  (`rev-parse --short`) + 40; hình dạng khác mà không tra ra commit ⇒ advisory, không hô sai.
- **`CHANGELOG.md` không phải sổ đầy đủ** — nó bị cắt còn 50 mục, sổ cũ nằm ở
  `references/changelog_archive/`. Đọc thiếu chỗ đó thì 184 version bị hô sai. Và **quét toàn văn chứ
  không chỉ dòng tiêu đề**: số hiệu đợt phần lớn nằm trong thân bài, headings-only chỉ thấy 4/191.
- Gộp đủ archive rồi dải `v1.9–v1.22` **vẫn thủng** (46/420) ⇒ đó là khuyết của SỔ, không phải bằng
  chứng trích dẫn sai ⇒ `VERSION_NOT_IN_CHANGELOG` xuống advisory. L6 đối xứng: `r160` không tra được
  nhưng sổ cũng vắng r158/159/161/163/165. **Chỉ khẳng định BẤT KHẢ mới là cờ** (vượt VERSION/đợt mới nhất).
- §2.2 nói thẳng «tài liệu lịch sử được phép dẫn tệp đã xoá»: `CHANGELOG.md`,
  `references/changelog_archive/`, `references/DOCTRINE_APPENDIX.md` (tự khai là thân SKILL.md trước
  v1.16.0, giữ nguyên để tra bối cảnh) ⇒ L1 ở đó là advisory. Phân định theo **loại tài liệu**, không
  theo tuổi tệp: git kho này chỉ 265 commit trong khi skill già hơn thế, `--diff-filter=D` không phân
  định nổi (nó chỉ nhận ra 3/134).

Kết quả: **213 → 8 cờ**, 275 advisory. Kế hoạch §2.3 và §2.7 **tự mâu thuẫn** ở L2 (§2.3 đòi SHA phải có
chữ số, §2.7 lấy `deadbeef` — không chữ số nào — làm phản chứng); đo ra kho có **0** token hex toàn chữ
cái nên bỏ vế «phải có chữ số», giữ vế «phải có chữ a-f» (vế này mới gánh việc: loại token toàn số).

## (c) Tám con trỏ chết bắt được ngay lần chạy đầu — đã vá cả tám

| Vị trí | Trích dẫn | Sự thật |
|---|---|---|
| `references/API_CONTRACT.md:266` | `scripts/manifest_build.py` | bản thật ở `scripts/_fallback/` |
| `references/DELTA_v1.19.md:6,31` | `references/Code.2.21.2h.gs` | snapshot `.gs` chỉ giữ từ `2.21.2k` |
| `references/DEV_TOOLING_GUIDE.md:56` | `references/Code.2.21.2i.gs` | nay trỏ `Code.2.21.2p.gs` hiện hành |
| `references/PATCH_v2.21.1.gs.md:378` | `APPSSCRIPT_MANIFEST.restricted-egress.json` | **không có trong kho — mà đó là phương án được KHUYẾN NGHỊ MẶC ĐỊNH** |
| `references/QUY_TRINH_RA_SOAT_3_TANG.md:92` | `references/BANG_PHAN_TANG_RUI_RO.md` | không tồn tại; quy tắc nằm ngay dưới cùng trang |
| `references/SKILL_KERNEL_MAPPING.md:25` | `changelog_archive/CHANGELOG-2026H1.md` | tên thật là `CHANGELOG-den-1.33.53.md` + `CHANGELOG-1.33.54-den-1.34.99.md` |
| `references/THE_THUC_TRINH_BAY.md:333` | `r160` | không tra được, nhưng dải sổ thưa ⇒ giữ ở advisory, KHÔNG vá |

## (d) ★Đối chứng ngoài dự kiến: r209 đã khoanh đúng 6 mục này từ trước — nay TRẢ NỢ

`tl_core/release.py` có sẵn guard con trỏ r209 với `_POINTER_BASELINE` **10 cặp nợ đã khoanh**.
`doc-claims-check` quét bằng đường hoàn toàn khác và dựng lại **đúng 6 cặp trong số đó** từ con số 0 —
tức danh sách khoanh nợ ấy chính xác, chỉ là chưa ai trả. Đã sửa thân tài liệu ⇒ baseline **10 → 4**
(ratchet chặn chiều THÊM miễn trừ; trả nợ làm số nhỏ đi là chiều đúng, hạ mốc có chủ đích). Bốn cặp còn
lại không phải nợ: placeholder trong văn xuôi, thư mục runtime cố ý ngoài gói, đường Drive `_meta/templates/…`.

Hai guard **bổ sung nhau chứ không trùng**: r209 đối chiếu PACKAGE-SET (nguồn sự thật = manifest) cho
`references/*.md` + `SKILL.md`; r218 đối chiếu CÂY THẬT, thêm link/SHA/version/đợt/`py:dòng`, có đệ quy
thư mục con và có phép che fence/backtick.

## (e) Bẫy tự gây, ghi lại để khỏi mắc lần hai

- Fixture golden nằm DƯỚI `references/` và **cố tình** chứa trích dẫn chết (đó là nội dung test). Quét
  mặc định mà nuốt chúng thì `--strict` không bao giờ xanh và 8 phát hiện thật lẫn với dữ liệu test ⇒
  bỏ qua `references/golden/fixtures/` khi ĐI NGANG, vẫn quét khi trỏ THẲNG (chính là cách golden chạy).
- Sửa `DEV_TOOLING_GUIDE.md` thành `references/Code.<ver>.gs` làm **r209 đỏ**: regex con trỏ của nó cắt
  ở `<` và sinh ra `references/Code` không tồn tại. Bộ lọc nhiễu của r218 nuốt token đó, r209 thì không
  — vá một reader chưa phải vá xong bẫy (bài học `ke-hoach-khung-tham-tra`).
- Lệnh mới thiếu dòng trong `_CREDS_LAZY_CMDS` ⇒ `main()` `load_creds` sys.exit TRƯỚC handler trên máy
  không config (GOTCHAS §4). Đã thêm.
- `r218` trong dòng doctrine mới bị CHÍNH nó hô `R_AHEAD_OF_LATEST` khi CHANGELOG chưa có mục r218 —
  đúng hành vi mong muốn, tự hết khi mục này tồn tại.

## (f) Việc C — doctrine «một bài học một lượt ghi»

`references/RASOAT_HOSO_LOOP.md` §9bis: không gộp nhiều phát hiện vào một lần ghi — cách đánh số lúc nháp
(«phát hiện 3», «mục trên») rò rỉ vào bản đã ghi và thành trích dẫn chết. Nhắc lại quy ước sao lưu:
mọi `*.bak.*.json` để Ở GỐC out-dir, KHÔNG trong `master/`.

## Nghiệm thu

selftest **1361/1361** (+9 ca r218, mỗi lớp ≥1 phản chứng «đỏ đúng ca», đều chạy qua đường sản xuất
`python scripts/tl.py …` chứ không qua bind) · gate 9/9 · `doc-claims-check --strict` rc=0 trên kho thật ·
chạy 2 lượt cho stdout byte-identical · golden thêm case `doc_claims_check_fixture`, regen `workflow_audit`
CÓ CHỦ ĐÍCH (đổi kích thước SKILL.md + 2 tệp runtime mới) · **0 lệnh ghi Drive, 0 call NLM**.

# ★ v1.35.53 — r217: sửa-theo-điểm thay cho thay-trọn-gói, bộ lọc nguồn Công báo, và một đường nạp chưa từng chạy nổi trên máy tiếng Việt (+6 test, 1352/1352) (2026-07-28)

> Nguồn: kết luận lượt rà 6 (`THAY_BAN_TRON_GOI_BI_BAC`) + `BAN_CONG_BAO_BOC_RA_CON_RAC_KHONG_CO_BUOC_LAM_SACH_CHUAN`.
> Đây là hai mục vá người giao việc đã chọn ở lượt 7 nhưng để lại vì lớn hơn hẳn phần còn lại.
> Mục (c) thì không ai đặt hàng — nó lộ ra ngay lần đầu chạy thật đường nạp offline.

## (a) `tl doc-patch <số hiệu> --diem <file>` — sửa ĐÚNG những điểm đã chứng minh

Lượt rà 6 đối chiếu bản kho với bản đăng Công báo: ND 159 lệch 17 điểm, ND 158 lệch 111 điểm. Nhưng
kết luận đắt hơn con số là **không bản nào trùm bản nào** — bản Công báo mang lỗi riêng («ngưởi» ở
khoản 2 Điều 8 ND 158 chính là phát hiện VD-34), còn bản kho mất hai công thức tính vì công thức là
ảnh/equation trong Google Doc. Thay trọn gói vì thế là **đánh đổi mù**: sửa được vài điểm thì rước
vào lỗi khác. Việc đúng là sửa từng điểm, có bằng chứng, có đường lùi — mà công cụ chưa có.

| | |
|---|---|
| cổng ghi | DRY mặc định · `--apply --confirm yes` · không có chế độ ghi ngầm |
| phạm vi | `vung` BẮT BUỘC: `khoi_dau` \| `dieu:<N>` \| `phu_luc` — không có "tìm khắp văn bản" |
| khớp | mỗi điểm phải khớp **ĐÚNG 1 lần**; 0 lần ⇒ `KHONG_KHOP`, >1 ⇒ `KHOP_NHIEU_LAN` |
| fail-closed | **toàn lô**: một điểm hỏng ⇒ KHÔNG áp điểm nào |
| nhầm văn bản | `so_hieu` trong file điểm lệch số hiệu đang sửa ⇒ chặn |
| đường lùi | tự sao lưu `docs/_doc_patch_bak/` + nhật ký; `doc-patch --undo <run_id>` |
| cổng undo | chỉ hoàn tác khi file còn ĐÚNG sha256 lượt patch đã ghi — khác ⇒ từ chối |

`KHOP_NHIEU_LAN` là chỗ cố ý không "thông minh": một chuỗi chính tả sai thường có mặt ở nhiều Điều,
và máy không được chọn hộ sửa cái nào. Người dùng thu hẹp bằng cách đưa thêm chữ hai bên vào `tim`.

**Không mượn `tl undo`**: nhật ký undo hiện có phục vụ registry qua GAS, hoàn tác của nó là ghi lại
giá trị ô. Ở đây đối tượng là FILE record cache, hoàn tác là chép lại nguyên bản. Trộn hai thứ vào
một lệnh là mời một lớp lỗi mới.

`text_hash` **cố ý KHÔNG tính lại** — record không giữ bố cục dòng của bản gốc nên mọi cách tính lại
đều ra một con số không đối chiếu được với gì cả; thay vào đó record mang cờ `DOC_PATCH:` nói thẳng
rằng hash đang là của bản nguồn TRƯỚC khi sửa, kèm `doc_patch.lich_su` đủ để dựng lại đường đi.

## (b) Bộ lọc nguồn Công báo ở đường nạp — `--loc-congbao`

Văn bản bóc từ PDF Công báo mang rác trình bày chen vào giữa thân. Bỏ ĐÚNG BA loại có khuôn chắc,
mỗi loại phải khớp **toàn dòng** (dính chữ khác ⇒ không bỏ, chỉ khai báo):

- `dong_chay` — dòng chạy đầu trang `[số] CÔNG BÁO/Số …/Ngày d-m-yyyy [số]`;
- `so_trang` — dòng chỉ có số **và kề một dòng chạy**. Điều kiện kề là bắt buộc: trong phụ lục/biểu
  mẫu có vô số dòng chỉ-một-số là dữ liệu thật;
- `chu_ky_so` — khối chữ ký số đủ 4 dòng liên tiếp, **quét toàn văn chứ không neo ở đầu bản**.

★Đo 27-07 trên ba văn bản thật: khối chữ ký số **không chỉ nằm ở đầu** — ND 159 có HAI khối nằm giữa
thân (sau khoản 6 Điều 1), Luật 41/2024 có một khối. Bản làm sạch **bằng tay** ở lượt 6 chỉ bắt khối
ở đầu nên còn sót 12 dòng; bộ lọc bắt đủ.

★**Cố ý KHÔNG tự bỏ nhãn mục Công báo** ở đầu bản (`VĂN BẢN QUY PHẠM PHÁP LUẬT`, tên cơ quan in một
mình) — chỉ khai báo `DAU_MUC_CONG_BAO_CON_LAI`. Công báo in tên cơ quan HAI lần (nhãn mục + cơ quan
ban hành), và neo «CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM» nằm SAU dòng số hiệu ở cả Luật 41/2024
(`Luật số: 41/2024/QH15`) lẫn ND 159 (`Số: 159/2025/NĐ-CP`) ⇒ mọi quy tắc cắt tự động đều ăn mất
chính danh tính văn bản. Người quyết, không máy.

Không bật cờ thì **khai báo mà vẫn nạp** (`NGUON_CONG_BAO_CON_RAC` vào `verify_flags`) — cùng họ với
`khoi_dau_missing` của r215: bản Công báo còn rác vẫn là bản chính thức, chặn nạp là phá đúng ca dùng
chính đáng. Cờ khai báo cũng không làm văn bản thành `partial` vì nó không phải khiếm khuyết cấu trúc.

## (c) Đường nạp `--method file` chưa từng chạy nổi trên máy tiếng Việt — và báo hỏng SAU KHI đã ghi

Lần đầu chạy thật `ingest_to_cache.py --method file` (đường `cache-build` offline, không đụng Drive):

```
{"ok": false, "reason": "ingest_failed",
 "error": "UnicodeDecodeError: 'charmap' codec can't decode byte 0x90 in position 46"}
```

`ingest_to_cache.py:724` đọc lại record cache bằng `open(target)` **không khai encoding** ⇒ Python
dùng codec locale (cp1258 trên Windows tiếng Việt) và nổ. Chỗ đó nằm **SAU** `patch_cache_metadata`,
nên lệnh in `ok:false` rc=2 **trong khi cache đã được ghi 49.758 B** — đúng lớp bẫy "rc≠0 không có
nghĩa là chưa ghi gì". Lượt 6 kết luận đường này "chạy được" bằng cách ĐỌC CODE; nó chưa từng chạy.

Khoá bằng **hành vi, máy-độc-lập**: chạy đường nạp dưới `-W error::EncodingWarning` +
`PYTHONWARNDEFAULTENCODING=1` ⇒ mọi `open()` thiếu encoding nổ bất kể locale của máy chạy test. Grep
chuỗi `encoding=` sẽ xanh giả ngay khi ai đó thêm một `open()` trần ở dòng khác.

## (d) `rasoat_phuluc.py`: Mục F thành Phụ lục VI, thêm Phụ lục VII

Bộ hồ sơ trình không khớp tên với chính nó: Báo cáo rà soát hứa một "Phụ lục" cho danh mục nội dung
chưa đủ căn cứ kết luận, còn tệp sinh ra đặt nhãn "Mục F — KHÔNG vào phụ lục"; và bảng tổng hợp theo
mã thì chỉ tồn tại dưới dạng dữ liệu JSON, không có bản trình bày để đính kèm.

★Số **VI/VII** chứ không phải III/IV: III/IV/V đã thuộc về Mẫu 05/06/07-BN. Chiếm lại số của chúng là
đổi nghĩa một bộ biểu mẫu chuẩn chỉ vì trong một hồ sơ cụ thể chúng tình cờ rỗng. Tên Phụ lục VI cũng
nói đủ hai thứ `route()` dồn vào đó ("nghiên cứu, rút kinh nghiệm" **và** "chưa đủ căn cứ kết luận") —
gọi tắt theo vế sau sẽ mô tả sai phần lớn số dòng.

## Nghiệm thu

- selftest **1346 → 1352** (+6 `r217_*`: 2 PURE nạp `verify_deep.py` thẳng từ file không qua bind,
  1 PURE nạp `lookup_ops.py` thẳng, 3 chạy **đường sản xuất thật** bằng subprocess).
- **Phản chứng 2 chiều CHẠY THẬT 11 đột biến trên bãi cách ly: 11/11 đỏ đúng ca, 0 lọt lưới** — cả
  hướng tắt guard (bỏ fail-closed toàn lô, bỏ cổng `--confirm`, bỏ cổng sha undo, bỏ cổng số hiệu,
  chỉ quét chữ ký số ở đầu, thôi khai báo, trả lại `open()` trần) lẫn hướng vá quá tay (nới khớp
  đúng-1-lần thành ≥1, bỏ dòng-chỉ-có-số không cần kề dòng chạy, bỏ luôn nhãn mục, chặn nạp khi còn
  rác). Bốn đột biến còn làm đỏ thêm test khác — guard phủ chéo.
- `ruff --select F` **delta 0 thực chất**: `tl.py` +0, `verify_deep.py` +0 (0 lỗi), ba script đường
  nạp +0; `lookup_ops.py` +26 và `tl_selftest.py` +11 đều là tên đã bind — đúng 2 tên mới
  (`_journal_read`, `_journal_new_run_id`) và cả hai đều có trong danh sách bind của `tl.py`.
- `parser_surface` regen **chủ đích 1 dòng** (thêm `doc-patch`). SKILL.md **byte-đẳng-dài 47.924**
  ⇒ re-import Capabilities KHÔNG bắt buộc. GAS **vẫn 2.21.2p**, không đụng.

# ★ v1.35.52 — r216: `rasoat-merge` đếm hai lần mà không ai biết, và đơn vị rà xuyên văn bản lọt vào danh mục VBQPPL (+5 test, 1346/1346) (2026-07-27)

> Nguồn: `rasoat_bugs.md` lượt rà 7 (27-07) — `RASOAT_MERGE_AN_CA_FILE_BAK_TRONG_THU_MUC_MASTER` +
> `RASOAT_MERGE_KHONG_CO_KHAI_NIEM_DON_VI_XUYEN_VAN_BAN`, và mục treo từ lượt 6
> `BANG_MASTER_DI_TRUOC_MASTER_UNIT_KHONG_CONG_NAO_BAT`. Cùng lớp **hỏng IM LẶNG** với r214/r215:
> rc=0, không cảnh báo, chỉ SỐ LIỆU là sai — mà đây là số liệu đi thẳng vào biểu mẫu trình Uỷ ban.

## (a) Bản sao lưu để lẫn trong `master/` ⇒ bảng master phồng 40 → 53 phát hiện, `_bo_qua` RỖNG, rc=0

`rasoat-merge --in <thư mục>` quét MỌI `*.json`. Đo thật 27-07 khi một bản sao lưu bị đặt nhầm vào
`master/`:

| | trước vá | sau vá |
|---|---|---|
| số phát hiện | **53** (13 mã VD trùng) | **40** |
| số văn bản | 5 | 4 |
| cảnh báo | **không có** (`_bo_qua: []`, rc=0) | `bo_qua_ban_sao` + rc=0 |

Hai nguồn mang **cùng `unit_id`** vẫn được gộp, không cổng nào đối chiếu. Phụ lục sinh ra từ bảng đó
đếm một phát hiện HAI lần, và người đọc bản phụ lục không có cách nào biết là trùng.

- **`_rasoat_la_ban_sao` (PURE)** — CỐ Ý HẸP: chỉ thành phần (ngăn bằng dấu chấm, KHÔNG tính thành
  phần đầu) bắt đầu bằng `bak`/`backup`. Không đoán theo `old`/`copy`/`cu`; `bakery-2025.json` vẫn là
  phiếu thật. Bản sao bị bỏ qua **được KHAI BÁO** ở `bo_qua_ban_sao` — bỏ qua im lặng chỉ là đổi sang
  một cái bẫy khác. ★Ghi chú giữ lại trong docstring: `backup` KHÔNG bắt đầu bằng `bak` (b-a-c ≠
  b-a-k) — bản đầu gộp làm một tiền tố và test đỏ ngay.
- **`_rasoat_trung_lap` (PURE)** — bắt trùng `key` (`phat_hien` lẫn `noi_dung`) và trùng `unit_id`,
  nêu rõ nguồn nào mang giá trị trùng. Cổng **fail-CLOSED**: có trùng ⇒ rc=2 và **KHÔNG ghi**. Ghi đè
  bằng bảng đã đếm hai lần là mất luôn bản đúng để đối chiếu ở lượt sau.

## (b) `--check`: bảng master ĐI TRƯỚC tầng unit thì merge lật ngược âm thầm

Khe hở đo được ở lượt 6: bản cập nhật VD-12 chỉ nằm ở `BANG_MASTER.json`, chưa chép về
`master/unit-003.json`. `rasoat-merge` lấy unit làm NGUỒN và bảng master làm ĐÍCH ⇒ chạy lại là mất
trắng một lượt làm việc, không báo gì. Lượt 6 phải xử bằng luật miệng "CẤM chạy `rasoat-merge`".

**`tl rasoat-merge --check`** = đối chiếu bảng master đang có với kết quả merge, **KHÔNG ghi đè**;
lệch ⇒ rc=2 kèm danh sách (`CHI_CO_O_BANG_MASTER` / `CHI_CO_O_KET_QUA_MERGE` / `KHAC_NOI_DUNG` +
ô lệch / hai loại cho `van_ban`). `_rasoat_check_lech` CỐ Ý bỏ qua `_nguon`/`_thieu_o_metadata`/
`_bo_qua` — chúng mang tên file, đổi theo chỗ chạy chứ không theo dữ liệu.

## (c) Đơn vị rà XUYÊN VĂN BẢN bị đẩy vào Mẫu 03-BN thành "văn bản" không tồn tại

`_rasoat_unit_to_bang` lấy `van_ban` của đơn vị làm SỐ HIỆU một dòng trong Mẫu 03-BN = *Danh mục
VBQPPL thuộc đối tượng, phạm vi rà soát*. `unit-006` (rà khối Căn cứ ban hành của CẢ 4 nghị định)
không phải một VBQPPL, nhưng nhãn mô tả của nó — `158/159/212/233-2025-ND-CP (KHOI CAN CU BAN HANH)`
— thành **dòng thứ 5** của một biểu mẫu chính thức trình Uỷ ban.

★`unit-004` (đơn vị đối chiếu 159×158) thoát được **CHỈ VÌ** tình cờ đặt `van_ban` trùng số hiệu thật
nên bị dedup nuốt đi — may, không phải do công cụ biết phân biệt.

Khoá mới **`loai_don_vi: van_ban|doi_chieu|xuyen_van_ban`** trong khuôn §6: `doi_chieu`/`xuyen_van_ban`
⇒ KHÔNG sinh dòng Mẫu 03-BN (và cũng không đòi điền ô metadata — đơn vị này không phải văn bản), phát
hiện vẫn gộp bình thường. **Mặc định (thiếu khoá) = GIỮ NGUYÊN hành vi cũ**: chỉ đơn vị tự khai mới
đổi cách xử lý.

## Nghiệm thu

- Selftest **1341 → 1346** (+5 `r216_*`). Bốn test PURE nạp `lookup_ops.py` THẲNG từ file (không
  bind) — đúng đường `rasoat_phuluc.py` đi; một test chạy **đường sản xuất thật** bằng subprocess
  `tl rasoat-merge`, vì cái đã cắn 27-07 là hành vi của LỆNH (rc=0 + ghi đè), không phải của hàm.
- **Phản chứng 2 chiều CHẠY THẬT 8 đột biến trên bãi cách ly: 8/8 đỏ đúng ca** — gồm cả hai hướng
  "tắt guard" (M1/M3/M5/M7) và "vá quá tay" (M2 coi mọi file là bản sao, M6 đơn vị nào cũng không
  sinh dòng), cùng hai hướng fail-open của cổng ghi (M4 thấy trùng vẫn ghi, M8 `--check` ghi đè).
- `ruff --select F` delta **0 thực chất**: +4 dòng đều là `_print_json_or_text` — tên do `bind()` cấp,
  đúng nhóm nợ sẵn của `lookup_ops.py`; `tl.py` giữ nguyên 17.
- `parser_surface` regen **chủ đích 1 dòng** (`rasoat-merge`, do thêm `--check`). SKILL.md
  **byte-đẳng-dài 47.924** ⇒ re-import Capabilities KHÔNG bắt buộc. GAS vẫn **2.21.2p**, không đụng.

# ★ v1.35.51 — r215: khối đầu văn bản bị đánh rơi trên đường cache, và nguồn DỰ THẢO phục vụ RAG lặng lẽ (+6 test, 1341/1341) (2026-07-27)

> Nguồn: `rasoat_bugs.md` lượt rà 4 (27-07) — `CACHE_BUILD_DANH_ROI_KHOI_DAU_VAN_BAN` (mục đáng vá nhất)
> + `DU_THAO_ND_BHXH_DE_CORPUS_TRUE_VA_DA_DAY_LEN_NLM`. Cùng lớp **hỏng IM LẶNG** với r214: rc=0, chỉ
> nội dung là thiếu. Khác ở chỗ cái thiếu lần này là **danh tính của chính văn bản**.

## (a) Đường cache trả về văn bản KHÔNG TỰ CHỨNG MINH ĐƯỢC DANH TÍNH — hai lỗ hổng, không phải một

**Đo trên ND 158/2025 (27-07), record `158-2025-nd-cp--consolidated.json` khai `chars=115.600`:**

| đường đọc | ký tự | bắt đầu bằng | phụ lục |
|---|---|---|---|
| `doc-text <id>` (mặc định → cache) | **108.823** | `Điều 1. Phạm vi điều chỉnh` | **không** |
| `doc-text <id> --markup mark` (gdoc-docx) | 115.414 | `CHÍNH PHỦ / Số: 158/2025/NĐ-CP` | có |

Bóc ra **hai** khiếm khuyết ĐỘC LẬP, trước đây bị gộp làm một và đổ nhầm cho "bản nguồn thiếu":

- **(a1) MẤT KHI DỰNG CACHE — `normalize_document.py` không hề lưu khối đầu.** `split_articles` bỏ
  `parts[0]` của `ART_SPLIT`; record chỉ có `articles` + `phu_luc`. Toàn bộ Quốc hiệu · cơ quan ban
  hành · `Số: 158/2025/NĐ-CP` · địa danh-ngày tháng · tên loại + trích yếu · khối `Căn cứ…` · tiêu đề
  Chương I **không nằm ở đâu cả** trong cache. Không cứu được bằng đọc lại cache — phải nạp lại.
- **(a2) MẤT KHI DỰNG LẠI — `cmd_extract` nối CHỈ `articles`.** `phu_luc` **CÓ trong record**
  (6.030 ký tự) nhưng đường dựng lại bỏ qua. Rồi bản thiếu đó **được ghi đè vào khoá cache CHUẨN**
  `extract_<id>.txt` ⇒ `doc-text` phục vụ nó làm bản mặc định. Đây mới là chỗ nhân bản thiệt hại.

**Vá:**
- `verify_deep.preamble_of(raw)` — PURE, dùng **CHUNG `ART_SPLIT`** với `split_articles` để hai bên
  không bao giờ lệch định nghĩa "chỗ Điều đầu tiên bắt đầu".
- `normalize_document` lưu `khoi_dau` + `structure.has_khoi_dau/khoi_dau_chars`. Khoá MỚI ⇒ record cũ
  đọc vẫn chạy; văn bản nạp dạng `--as-appendix` để rỗng (cả văn bản LÀ phụ lục, không có khối đầu riêng).
- `_consolidated_text(doc)` — PURE, dựng lại **khối đầu + Điều + phụ lục**. Đo lại trên chính record ND
  158 **chưa nạp lại**: 108.823 → **114.855** ký tự ⇒ **6.032 ký tự phụ lục được cứu ngay, không cần
  re-ingest**. Phần khối đầu thì cache cũ không có gì để cứu — nên nó phải **nói ra** (dưới).

## (b) Máy đoán thì phải nói là đang đoán — 3 cổng KHAI BÁO, không cổng nào chặn

Hỏng thật sự không phải "thiếu chữ" mà là **thiếu chữ mà không ai biết**. Ca đã trả giá: VBHN Luật NSNN
`89-2026` — text không có khối đầu ⇒ `_classify_doc_header` hết chỗ đọc trong vùng tiêu đề, đi quét sâu
16k và **nhặt số hiệu từ THÂN**, trả về `145/2025/QH15` (số của luật SỬA ĐỔI được liệt kê trong thân).
Lượt 3 đọc kết quả đó thành "bản nguồn thiếu khối đầu"; đo 27-07 cho thấy **nguồn CÓ đủ**.

- `_text_thieu_khoi_dau(text)` — PURE, bắt text **vào thẳng mốc cấu trúc thân** (`Điều N.` / `Chương
  <La Mã>` / `Mục N`). **CỐ Ý hẹp và tất định**: văn bản có letterhead, phụ lục độc lập mở đầu `PHỤ
  LỤC`, văn xuôi nhắc chữ "Điều" đều KHÔNG bị bắt — cổng này chạy trên mọi lượt đọc nên báo động giả
  đắt hơn im lặng.
- `_doc_text_any`: **mọi** đường trả text (cache · gdoc · gdoc-docx · docx · pdf) đi qua `_kd_gate` ⇒
  cảnh báo `[khoi-dau] ⚠` + `khoi_dau_missing` trong `doc-text --json`. Nhánh `return _ct, "cache"` —
  đúng đường đã phục vụ ND 158 — được nối riêng, không dựa vào đường chung phía dưới.
- `_classify_doc_header` trả thêm `khoi_dau_missing`. **KHÔNG đổi cách đoán**: đường quét sâu 16k vẫn
  cần cho layout VPQH in số VBHN ở **khối ký CUỐI** (v1.34.6 #1) — bịt nó là vá quá tay, làm hỏng một ca
  đúng để chữa một ca sai. Chỉ thôi im lặng.
- `cmd_extract`: record dựng TRƯỚC r215 (không có khoá `khoi_dau`) ⇒ cảnh báo tại chỗ kèm đúng hai lối
  ra (`cache-build` lại, hoặc `doc-text --markup mark`). `rep` phân biệt **`thieu_khoa`** (lỗi công cụ:
  cache cũ) với **`rong`** (dữ kiện: văn bản thật sự không có khối đầu) — gộp hai cái đó chính là cách
  lượt 3 đọc sai địa chỉ.

## (c) `DU_THAO_ND_BHXH_DE_CORPUS_TRUE_VA_DA_DAY_LEN_NLM` — cảnh báo hai đầu, **CỐ Ý KHÔNG CHẶN**

- **Đo:** hai dự thảo nghị định (`DUTHAO_ND_…`) mang `corpus=true`, `nlm_status=pushed` trong chính
  notebook hồ sơ. Cờ `DRAFT_NOT_EFFECTIVE` **có** bắn ở đường phân loại — nhưng không đường nào nói ra
  **vào lúc hỏi** ⇒ câu trả lời RAG có thể trộn chữ dự thảo với luật đang có hiệu lực.
- **★Đã cân nhắc và BÁC hướng fail-closed** mà sổ lỗi đề xuất đầu tiên ("loại các dòng có cờ
  DRAFT_NOT_EFFECTIVE khi đẩy"): dự thảo nằm trong notebook **hồ sơ trình** là **đúng chỗ** — chúng
  chính là đối tượng rà. Chặn đẩy sẽ phá đúng ca dùng chính đáng. Cái sai là phục vụ chúng LẶNG LẼ, nên
  vá đúng chỗ đó — trùng với phương án thứ hai mà chính sổ lỗi nêu ("ít nhất cảnh báo").
- `_nlm_draft_sources(entries, source_ids=, notebook_id=)` — PURE, đọc **registry**, không đoán từ
  envelope NLM (cùng doctrine với `_nlm_scope_shortfall` r214). Ghim `--source-id` → xét đúng nguồn được
  hỏi; không ghim → cả notebook. Dòng dự thảo **chưa** lên NLM không tính (chưa thành rủi ro RAG).
- Cảnh báo ở **hai** đầu: `nlm-add` (lúc đẩy) và `nlm-query` (lúc hỏi — in TRƯỚC câu trả lời).

## Kiểm chứng

- Selftest **1335 → 1341** (+6 `r215_*`). Ba test PURE nạp module **THẲNG từ file, KHÔNG bind** —
  bẫy [[false-green-test-qua-bind]] đã trả giá ở r213.
- **Phản chứng 2 chiều CHẠY THẬT 9 đột biến trên bãi cách ly** (vá thiếu ×5 / vá quá tay ×4): xem
  báo cáo phiên. Hai chiều đối xứng cho cùng một cổng (`M5` báo động tuốt ↔ `M6` guard chết hẳn).
- `_consolidated_text` đo lại trên record ND 158 THẬT (chưa nạp lại) — số ở bảng trên là đo, không ước.

# ★ v1.35.50 — r214: hai lỗi công cụ lượt rà 2 đo được — env profile ăn mất export, và `-s` LẶP làm NLM rụng nguồn (+6 test, 1335/1335) (2026-07-26)

> Nguồn: `rasoat_bugs.md` mục 8 + mục 9 (lượt rà 2, 26-07, cả hai `workaround`). Cả hai đều thuộc lớp
> **hỏng IM LẶNG**: lệnh vẫn rc=0, chỉ kết quả là sai — đúng lớp nguy hiểm nhất cho một lượt rà soát,
> vì nó đẻ ra kết luận ÂM TÍNH GIẢ mà không để lại dấu vết nào cho người rà.

## (a) `TL_META_FOLDER_ID_BI_PROFILE_OVERLAY_XOA` → `_apply_profile_env` thôi ăn env người dùng export

- **Lỗi:** `state-get`/`state-put` (r213) và `RASOAT_HOSO_LOOP` §7 bảo người dùng `export
  TL_META_FOLDER_ID`. Nhưng `_apply_profile_env` **pop VÔ ĐIỀU KIỆN** cả 6 khoá overlay rồi chỉ set lại
  khi block profile có ô tương ứng ⇒ profile thiếu `metaFolderId` (đúng ca config Cowork bootstrap, cờ
  `MARKER_CONFIG_DRIFT`) thì env bị **xoá trắng**, lệnh báo `META_FOLDER_ID_TRONG` và chuỗi `fix` chỉ lại
  **đúng cái đường nó vừa phá**. Lượt rà 2 phải đi vòng `--folder-id` tường minh cả lượt.
- **Vá:** vòng xoá chỉ còn xoá **đúng khoá do CHÍNH overlay trước đó ghi** (dấu vết để ở env
  `TL_PROFILE_ENV_OVERLAY` — **KHÔNG** dùng biến module: bẫy I11, mutable/hằng ở `tl_core` phải re-export
  sang `tl.py` mới sống qua rebase globals; env lại đi theo cả process con, đúng ngữ nghĩa "overlay đã
  ghi"). Mục đích GỐC của vòng xoá (đổi profile trong cùng process không dính scope cũ) giữ nguyên.
- **★NGOẠI LỆ GIỮ NGUYÊN — không nới:** `PROFILE_NOT_FOUND` vẫn xoá **SẠCH** bất kể ai ghi, để guard hạ
  nguồn (`NO_NOTEBOOK_ID`, `PROFILE_CATEGORIES_OWN_REQUIRED`, registry-id-empty) fail-closed thay vì mượn
  scope nền còn sót trong env — nới chỗ này là mở lại đúng lớp sự cố 1.23.21 mà v1.33.48 sinh ra để chặn.
- **Giới hạn đã biết (nói thẳng, không giấu):** nếu người dùng export env RỒI đổi profile **trong cùng
  một process** qua một profile CÓ ô đó rồi sang profile KHÔNG có, giá trị export ban đầu vẫn mất — bằng
  hành vi cũ. Khoá chính (lần overlay ĐẦU TIÊN không được ăn env) đã đóng; phần còn lại là mép hiếm.

## (b) `NLM_QUERY_LOAI_NGUON_KHONG_BAO` → **nguyên nhân gốc nằm ở argv của chính skill**, không phải NLM

- **Đo lại lật chẩn đoán cũ:** sổ lỗi ghi "NLM im lặng loại bớt nguồn". Đọc `nlm notebook query --help`
  của CLI ĐANG CÀI: `--source-ids/-s <str>` là **MỘT chuỗi «Comma-separated source IDs»**, KHÔNG phải
  option lặp. `nlm_cli.notebook_query` lại phát `-s <id>` **lặp lại** ⇒ giá trị sau **ĐÈ** giá trị trước,
  chỉ nguồn **CUỐI** sống sót. Khớp đúng số đo 26-07: truyền `212` rồi `233` → `sources_used` chỉ còn
  `233` = cái cuối. `cross_query` **trong chính file đó** vốn đã đúng khuôn `-n ",".join(...)`.
- **Vá tầng 1 (gốc):** tách `_query_args` PURE (khuôn `_add_args`), gộp **một** `-s` bằng dấu phẩy.
- **Vá tầng 2 (không tin server):** `_nlm_scope_shortfall` đối chiếu `sources_used` ↔ `--source-id`;
  thiếu → `NLM_SCOPE_SHORTFALL` cảnh báo stderr (rc vẫn 0, không chặn việc đang chạy). Cờ mới
  **`--strict-scope`**: thiếu → rc=2 **và KHÔNG in câu trả lời ra stdout** (agent hạ nguồn sẽ tưởng đủ
  nguồn); envelope không khai `sources_used` mà đã đòi `--strict-scope` → rc=2 `SCOPE_UNVERIFIABLE`
  (fail-CLOSED: đòi bảo đảm mà không chứng minh được thì không phát).
- **CỐ Ý KHÔNG đoán:** chỉ nhận đúng khoá `sources_used`. `sources`/`citations` là nguồn được **TRÍCH
  DẪN** — tập con HỢP LỆ của nguồn được **QUÉT** — đoán sang đó chỉ đẻ báo động giả (đã khoá bằng test).

## Nghiệm thu

- Selftest **1329 → 1335** (+6 `r214_*`). **Phản chứng 2 chiều CHẠY THẬT 7 đột biến** trên bãi cách ly
  (bản sao cây, không đụng canonical): 7/7 làm ĐỎ đúng ca kỳ vọng, khôi phục lại 1335/1335. Đáng chú ý:
  hai đột biến "vá quá tay" (M2 bỏ xoá khi `PROFILE_NOT_FOUND`, M3 thôi pop) còn làm ĐỎ **cả guard cũ**
  `r6_base_also_not_set_unknown_profile` / `r106_empty_profile_never_inherits_base` ⇒ xác nhận độc lập
  rằng bản vá không đụng vào tính chất mà v1.30.0/v1.33.48 đang giữ.
- `ruff --select F` **delta = +1** và là `DEFAULT_PROFILE` — tên vốn đã bind sẵn 14 lần trong chính file
  đó (nợ F821 by-design của khuôn bind), **không phải lớp lỗi mới**.
- `parser_surface.json` regen **CHỦ ĐÍCH** (đúng 1 dòng: `nlm-query`, do thêm `--strict-scope`).
- `SKILL.md` **byte-đẳng-dài 47.924** (chỉ đổi dòng version) ⇒ re-import Capabilities KHÔNG bắt buộc.
- **GAS KHÔNG đụng — vẫn 2.21.2p, không cần deploy GAS.**

# ★ v1.35.49 — r213: ĐỢT 5 — vá HAI mắt xích lớp điều phối mà lượt rà LIVE 26-07 phơi ra (+6 test, 1329/1329) (2026-07-26)

> Nguồn: sổ lỗi H7/H8 (`rasoat_bugs.md`, 7 mục, TẤT CẢ `workaround`). Hai mục vá ở đây là hai mắt xích
> **BẮT BUỘC** của lớp điều phối mà **không cổng máy nào phủ** — cả hai chỉ lộ ra khi chạy thật, vì Đợt
> 1–3 tả chúng bằng prose chứ không cài thành lệnh.

## (a) `STATE_DRIVE_KHONG_CO_DUONG_GHI` → `tl state-get` / `tl state-put`

- **Lỗi:** `WRITE_PATHS_v1` bắt state ở Drive `_meta/rasoat_state.json` làm nguồn sự thật resume, nhưng
  gói LIVE **không có lệnh nào ghi một JSON tuỳ ý vào `_meta/`**. Mặt ghi Drive duy nhất là
  `profile-file-add --apply --confirm yes` (cổng tài liệu corpus — cần người duyệt) và `drive-push`
  (đòi file ĐÃ tồn tại). Theo đúng chữ của doc thì **mỗi lần chốt state phải xen người 1 lần** — phá
  nghiệm thu ≤2 lần xen của H7. Lượt rà 26-07 phải giữ state local, KHÔNG sống nổi ca §7 (sandbox xoá
  trắng / đổi máy).
- **Đo lại trước khi vá — và phép đo lật đề bài:** mặt ghi **ĐÃ CÓ** và đang chạy THẬT trong sản xuất
  (`_create_profile_manifest_json`, `profile-index`): `g.post("upload", mime="application/json",
  folderId=<_meta>, convert/register/share="false", force="true")` rồi MỚI dọn bản cũ. **Thiếu là thiếu
  LỆNH, không thiếu năng lực** ⇒ **KHÔNG đổi GAS, KHÔNG thêm action `files_put`** (đề xuất ban đầu),
  GAS giữ nguyên `2.21.2p`, Đợt 5 **không cần deploy GAS**.
- **Vá:** cặp lệnh client-only. `state-put` **CỐ Ý không có `--confirm`** — mượn cổng duyệt là tái tạo
  đúng thứ đã phá H7. Đổi lại khoá bằng **ba chốt máy**: (1) `_rasoat_state_scope` fail-CLOSED — danh
  sách tên ĐÓNG (`rasoat_state.json`/`rasoat_approvals.json`), từ chối mọi tên khác/có đường dẫn;
  (2) folder đích BẮT BUỘC `_meta/` (không có mặc định root); (3) `--expect-claim` từ chối ghi khi
  `session_claim.id` trên Drive đã khác (single-writer §9), và **fail-CLOSED khi không đọc nổi bản trên
  Drive** thay vì đoán là khớp.
- `register="false" share="false"` là **bắt buộc, không phải tuỳ chọn**: `upload` mặc định
  `ANYONE_WITH_LINK` + ghi registry ⇒ để mặc định thì state hồ sơ vừa RÒ RỈ qua link vừa bẩn registry.
  Ba tham số này bị test khoá ở NGUỒN.
- **Thứ tự an toàn:** tạo bản MỚI trước → dọn bản cũ sau. Chết giữa chừng = tồn 2 bản, `state-get` lấy
  bản mới nhất và lượt sau dọn nốt; đảo thứ tự thì chết giữa chừng = MẤT state.
- Tiện thể trả nợ mục `PROFILE_META_FOLDER_KHONG_CO_TRONG_CONFIG`: `metaFolderId` rỗng nay báo lỗi **chỉ
  thẳng đường vòng ĐỌC-ONLY** (`profile-sync --json`, KHÔNG `--apply`) thay vì cụt lủn — đường vòng đó
  26-07 phải tự nghĩ ra.

## (b) `THIEU_BUOC_GOP_MASTER_UNIT_SANG_BANG_MASTER` → `tl rasoat-merge`

- **Lỗi:** PHA 4 **SẬP thật** (`AttributeError: 'str' object has no attribute 'get'`). Khuôn §6
  `master/<unit>.json` và khuôn bảng master khớp ở tầng **item** (cùng 10 trường + `anchor`) nhưng lệch
  ở tầng **container**. QUY_TRINH chỉ viết "dồn phát hiện vào bảng master" — Đợt 1–3 **không định nghĩa
  và không cài** bước "dồn", cũng không test nào chạy chuỗi §6 → phụ lục.
- **Hỏng IM LẶNG trước, báo sai chỗ sau:** `van_ban += d.get("van_ban", [])` gặp CHUỖI số hiệu thì `+=`
  **trải chuỗi thành TỪNG KÝ TỰ** (`["1","5","9","-",…]`), mãi sau mới chết ở nơi khác.
- **Vá:** `tl rasoat-merge --in <master/> [--out] [--state]`; và `rasoat_phuluc.py` **tự nhận khuôn §6**
  qua ĐÚNG hàm quy đổi đó (một nguồn chân lý) nên `--in <out-dir>/master` chạy thẳng — điều mà thẻ
  `rasoat_hoso.json` đã **khẳng định trong mục `verify` từ Đợt 2 mà chưa ai kiểm**; nay mới thành thật.
  Khuôn không nhận ra ⇒ **rc≠0 nói rõ file nào**; file có CẢ `phat_hien` lẫn `noi_dung` cũng bị từ chối,
  không đoán — đoán sai ở đây là nuốt mất phát hiện mà không ai biết.
- **KHÔNG BỊA metadata:** đơn vị rà chỉ biết số hiệu + tên; `ngay`/`hieu_luc_tu`/`tinh_trang` nằm ở
  registry. Các ô đó để **RỖNG** + nổi lên `_thieu_o_metadata` + ghi chú ngay trong ô Ghi chú, thay vì
  lấp cho đầy bảng. (Đợt 4 dựng tay các ô này từ registry; **CỐ Ý chưa tự động hoá** ở r213 — registry
  không có `ngay`/`hieu_luc_tu` nên cũng chỉ lấp được 3/6 ô, mà đánh đổi là biến một lệnh thuần/tất định
  thành lệnh phụ thuộc cache. Ghi nhận là việc riêng.)
- **Khe hở H8** (phiên kế nhiệm chết SAU khi ghi master nhưng TRƯỚC khi cập nhật state ⇒ state còn
  `doing` dù việc đã xong): `--state` chạy `_rasoat_state_reconcile` — `doing` + CÓ master ⇒ `done`;
  `doing` + KHÔNG master ⇒ `pending`; `done` KHÔNG BAO GIỜ bị hạ. Luật cũ của thẻ ("doing mồ côi →
  pending") áp thẳng sẽ **rà lại đơn vị đã xong và đẻ phát hiện trùng số**.

## (c) Chốt MÂU THUẪN DOCTRINE `nlm-auth-load` (câu trừ ngữ cảnh, không đảo/không nới)

- Chuỗi khắc phục của `nlm-auth-status` xếp `tl nlm-auth-load` ở **(1)** trong khi §4b + PHA 0 **CẤM tự
  chạy** nó. **Cả hai đều đúng, khác NGỮ CẢNH:** (1) là đường bootstrap Cowork/headless — ở đó máy chưa
  có jar nào và đấy là đường duy nhất chạy được không cần browser; trong lượt rà thì nạp bundle đè lên
  jar đang sống/vừa chết là quay vòng vô ích.
- ⇒ **Không đảo thứ tự** (đảo là phá nghiệm thu r208b) và **không nới §4b** (nới là mở lại vòng lặp
  r208c đã đóng). Thay vào đó **cả 5 chuỗi** thông báo auth mang sẵn **câu trừ** trỏ §4b, vì agent đọc
  thông báo lỗi thường không đọc doctrine. Chốt chặn hạ cấp `_nlm_auth_load_downgrade` (r208c) vẫn giữ —
  nó chặn bản CŨ hơn nhưng **KHÔNG chặn được bản mới-hơn-mà-cũng-chết**, nên câu trừ là lớp còn thiếu.

## Test 1323 → **1329** (+6 `r213_*`), tất cả phản chứng 2 chiều

- `r213_rasoat_ops_chay_duoc_khong_can_bind` — **bẫy trả giá NGAY khi viết r213**: bản đầu của
  `_rasoat_merge_units` gọi `_norm_compare_text`, chạy tốt qua `tl` (đã bind) nhưng `NameError
  unicodedata` khi `rasoat_phuluc.py` import trần. Đúng khuôn false-green mà r212 vừa dạy. Test nạp
  `lookup_ops` THẲNG từ file (không ai gọi `bind`) + khoá NGUỒN cấm nối lại helper đó.
- `r213_gop_master_s6_chay_tron_chuoi_den_phu_luc` — chạy **subprocess đường sản xuất thật**
  `python scripts/rasoat_phuluc.py --in <thư mục master>`; phản chứng 1: file khuôn lạ phải rc≠0 (không
  nuốt thành "0 phát hiện"); phản chứng 2: tái hiện thuật toán CŨ trên đúng dữ liệu ⇒ khẳng định
  `+=` trải 14 ký tự — test bắt được nếu ai revert.
- `r213_merge_khuon_nhan_dien_2_chieu` · `r213_state_put_scope_fail_closed` (11 tên xấu đều bị chặn,
  khoá `share/register/force` + THỨ TỰ upload-trước-trash ở nguồn) · `r213_state_hoa_giai_don_vi_doing`
  (6 chiều, gồm "master rỗng ⇒ không đơn vị nào tự lên done") · `r213_auth_carve_out_khong_pha_thu_tu`
  (thứ tự r208b KHÔNG vỡ ∧ câu trừ có mặt ∧ doctrine ở 2 tài liệu vẫn CẤM).
- **Đo trên dữ liệu THẬT của Đợt 4** (`p14_h7h8_rasoat_2026-07-26/master`): 2 file → 2 văn bản, 9 phát
  hiện; chuỗi tiếp `rasoat_phuluc` ra 04:5 · Mục F:4 · dedup **9** — khớp đúng kết quả đường vòng 26-07.
  Hồi quy khuôn bảng cũ giữ nguyên 03:4 · 04:5 · F:4 · dedup 9.
- `parser_surface.json` regen CHỦ ĐÍCH: **+3 dòng, 0 sửa** — chứng minh không lệnh cũ nào đổi mặt.

## Kiểm LIVE đường ghi (user duyệt chạy thật, đã dọn sạch sau đó)

`state-get` đường ĐỌC đã chạy LIVE ngay khi viết. Đường GHI thì chạy trọn một lượt trên Drive thật
rồi trash file kiểm thử — vì **ship một đường mà chưa ai chạy đúng là cái Đợt 5 tồn tại để tránh**
(thẻ `rasoat_hoso.json` từng khẳng định `rasoat_phuluc.py --in master/` chạy được, suốt 3 đợt không ai
kiểm, và nó sập thật).

- PUT lần 1 → `fileId` mới, `don_ban_cu: []`. GET đọc lại: **JSON khớp TUYỆT ĐỐI**, dấu tiếng Việt
  nguyên vẹn (`Điều 1 khoản 2.`).
- `--expect-claim` **lệch** ⇒ `CLAIM_LECH` **rc=2**, nói rõ claim trên Drive vs kỳ vọng. **khớp** ⇒ cho
  ghi, và **dọn đúng bản cũ** (`don_ban_cu` 1 mục, `don_sach: true`).
- GET sau ghi đè: đúng **1 bản**, `canh_bao` rỗng, nội dung là bản B. Trash xong → `state-get` trở lại
  **rc=3** "chưa có state trên Drive". Không để lại rác.
- **★ Lượt kiểm LIVE bắt được 1 lỗi mà test thuần không thấy:** `state-get` đếm **KÝ TỰ** trong khi
  `state-put` đếm **BYTE**, cùng nhãn `"bytes"` ⇒ CÙNG một file báo **478 vs 471** (7 ký tự có dấu),
  nhìn hệt như mất dữ liệu khi đối chiếu round-trip. Đã sửa `state-get` sang byte utf-8 + khoá bằng
  `r213_state_put_scope_fail_closed` (ok6). Đây đúng là loại lỗi chỉ lộ ra khi chạy thật.

## ★ Bẫy đã trả giá trong chính lượt này (ghi để không lặp)

- **`contract_check.py --bump <ver>` là bump CONTRACT GAS, KHÔNG phải version skill.** Gọi nhầm nó với
  `1.35.49` đã ghi đè `2.21.2p` ở 5 chỗ trong `SKILL.md`/`API_CONTRACT.md` (sinh ra cả `Code.1.35.49.gs`
  không tồn tại). Đã `git checkout` hai file và bump 3 chỗ version skill BẰNG TAY. Bump skill =
  `VERSION` + hằng `VERSION` trong `tl.py` + header `SKILL.md`; KHÔNG có công cụ tự động cho việc đó.
- `tl_selftest.py` là **CRLF toàn bộ** trong khi `tl_core/*.py` là **LF** — nối test phải chuyển đổi,
  không thì lẫn dòng.

# ★ v1.35.48 — r212: GUARD ADR-0001 ĐANG FAIL-OPEN — `tl_gws` thiếu `import Path` (+1 test, 1323/1323) (2026-07-26)

> Phát hiện khi truy một `[FAIL] r65` người dùng gặp 26-07 (lần đỏ ĐÓ là thoáng qua — chạy selftest đúng
> lúc merge fast-forward đang viết lại 10 file). Truy tiếp thì lòi ra lỗi THẬT, không liên quan lần đỏ đó.

- **Lỗi:** `scripts/tl_gws.py` **không hề import `pathlib`** — `Path` là tên stdlib DUY NHẤT trong nhóm còn
  chờ `bind(tl_module)` chép từ namespace tl. Nên `_bundle_meta_blocks_push` (guard ADR-0001: cây có
  `BUNDLE_META.json` = giải nén từ bundle nhánh song song ⇒ CẤM publish) ném `NameError`, bị
  `except → return False` nuốt, và **luôn báo "không có gì chặn cả"**. Đo tươi: `import tl_gws` trần rồi gọi
  trên thư mục CÓ `BUNDLE_META.json` → `False`. Mọi đường dispatch không qua `build_parser` — đúng cái bẫy
  mà chú thích đầu file đã cảnh báo — biến guard cấm-publish thành cho-phép-publish.
- **Vì sao r65 không bắt:** nó gọi qua `_imp("tl_gws")` — instance ĐÃ bind nên `Path` có sẵn. Test xanh
  trong khi đường sản xuất hỏng: false-green kinh điển.
- **Vá:** (a) `from pathlib import Path` vào nhóm stdlib TƯỜNG MINH ở top (đúng doctrine sẵn có của file);
  (b) guard đổi sang **FAIL-CLOSED** — đọc không được thì CHẶN (`return True`), vì guard cấm-publish mà hỏng
  theo hướng "cứ publish đi" là hỏng sai chiều; người vẫn có `--force`.
- Test 1322 → **1323** (`r212_guard_bundle_meta_khong_phu_thuoc_bind`): nạp tl_gws THẲNG từ file (không ai
  gọi bind — khẳng định `_BOUND is False`) rồi đòi guard phân biệt đúng 2 thư mục; **phản chứng** gỡ `Path`
  khỏi globals ⇒ tái hiện đúng sự cố nhưng nay CHẶN thay vì cho qua; khoá luôn nguồn (xoá dòng import =
  test đỏ). **Chạy 2 chiều thật:** code CŨ → `1322/1323` (r212 đỏ, r65 vẫn xanh — chứng minh r65 chưa bao
  giờ phủ chỗ này); code ĐÃ VÁ → `1323/1323`.
- **Ruff đã tố cáo từ lâu mà không ai đọc:** delta trên `tl_gws.py` đúng **−2 `F821 Undefined name Path`**
  (99 → 97), không thêm phát hiện mới. Hai dòng đó nằm lẫn trong ~97 F821 "cố ý" của thiết kế `bind()` nên
  chìm nghỉm — bài học: nợ F821 diện rộng che mất F821 THẬT.

# ★ v1.35.47 — r211: ĐỢT 3 LỚP ĐIỀU PHỐI — H5 degrade-and-continue + sổ lỗi · H6 kickoff contract + PHA 0 tiền kiểm (+6 test, 1322/1322) (2026-07-26)

> Tiếp r210 (Đợt 2 đã merge). Đợt 3 **không viết code lõi**: hai hạng mục đều là ĐẶC TẢ — nhưng đặc tả
> viết dưới dạng **khối máy-đọc** (`BUG_LEDGER_v1` · `PHA0_GATE_v1` · `KICKOFF_CONTRACT_v1`, cùng idiom
> `WRITE_PATHS_v1` của r210) để guard bắt được drift, thay vì prose mà không cổng nào gác.

- **H5 — làn lỗi & sổ lỗi (`references/QUY_TRINH_RA_SOAT_3_TANG.md`, mục MỚI "LÀN LỖI"):** 4 bước
  (thử đường vòng CÓ SẴN → `workaround` đơn vị vẫn tới `done` → `blocker` đánh `blocked` **không giả
  `done`** rồi đi tiếp → chỉ dừng khi **chặn đứng toàn cục**). Chốt: **đúng HAI hạng lỗi**; "chặn đứng"
  KHÔNG phải hạng lỗi mà là **trạng thái hồ sơ** suy ra từ hàng đợi (mọi đơn vị còn lại cùng một `ma`) —
  nên một `blocker` lẻ không bao giờ đọc được thành lý do dừng. **Sửa nóng CHỈ khi chặn đứng**, lỗi lẻ
  **gom vá sau lượt rà**, và không nhánh nào vá tại LIVE (deploy là bước tay ⇒ vá tại chỗ bị đè lần
  deploy sau). Khuôn sổ `rasoat_bugs.md` **8 trường bắt buộc**, thiếu/rỗng một trường = coi như CHƯA ghi
  sổ; `version_do_duoc` bắt buộc vì báo lỗi đo trên bản trễ là vô giá trị (LIVE drift). Tên sổ dùng đúng
  `rasoat_bugs.md` đã khoá trong `WRITE_PATHS_v1` — kế hoạch gọi `BUGS_FOUND.md` là CÙNG một sổ, không đẻ
  tên file thứ hai.
- **H6 — PHA 0 tiền kiểm (cùng tài liệu) + kickoff contract (`references/RASOAT_HOSO_LOOP.md` §1):**
  PHA 0 mở rộng thành cổng **6 bước** — b1 `doctor` · b2 `ping`/contract · b3 `precheck` ·
  b4 `profile-doctor` · b5 `nlm-auth-status` · b6 **canary probe LIVE**. Ba verdict thay vì hai:
  `chan_dung` (dừng sớm, báo 1 dòng) · **`chan_lan_ghi`** (Loop B đứng, **Loop A vẫn rà trên cache** —
  không giết cái còn chạy được) · `co_fallback` (tụt chế độ không-NLM). **b5/b6 CHỈ chạy khi lượt sắp cần
  NLM**, và **chi phí trước cổng = 0 call truy vấn** (canary là `notebook_get`, ngoài ngân sách 60).
  Verdict đọc theo đo 26-07: `alive=false` ⇒ chế độ không-NLM · `alive=null` ⇒ KHÔNG chặn · `alive=true`
  + `rotation_token_expired` ⇒ chạy tiếp nhưng không mở lô dài. Kickoff nâng 6 → **8 mục** (thêm *môi
  trường & đường ghi* và *nghiệm thu & điểm dừng*), mỗi mục có mặc định trừ **phạm vi hồ sơ = bắt buộc
  hỏi**; bộ hằng số trong hợp đồng phải khớp `RASOAT_PLAN_SCHEMA.md` §4, không đẻ bộ thứ hai.
- **Thẻ `references/workflows/rasoat_hoso.json`:** `plan[A1]` trỏ `PHA0_GATE_v1` b1–b6; +2 `rules`
  (degrade-and-continue; luật sửa nóng); +3 `recommended_commands` (`doctor`/`precheck`/`nlm-auth-status`)
  — mọi lệnh đều CÓ THẬT trong parser và được kịch bản gọi tên (drift-guard r210 vẫn gác).
- Test 1316 → **1322** (+6 `r211_*`), tất cả PURE, không chạm mạng: `so_loi_dung_khuon` ·
  `degrade_khong_dung_vong` (bơm lỗi giữa lượt drain 6 đơn vị → ghi sổ 1 mục ĐỦ trường, PLAN vẫn tiến
  5/6, vòng không dừng) · `sua_nong_chi_khi_chan_dung` · `pha0_chan_som_truoc_khi_tieu_nlm` (chặn đứng ở
  b1 ⇒ chưa hề chạm b5/b6) · `kickoff_du_muc_va_hang_so` · `the_khop_luat_moi`.
  **Phản chứng 2 CHIỀU chạy thật (6 đột biến tài liệu, mỗi lần chạy lại cả suite):** hạ b6 xuống
  `chan_dung` → đỏ đúng test PHA 0 · bỏ `version_do_duoc` → đỏ khuôn sổ · cắt 1 mục kickoff → đỏ hợp đồng ·
  lệch hằng `nlm=60→40` → đỏ hợp đồng · gỡ luật sửa nóng khỏi thẻ → đỏ drift-guard thẻ · xoá hẳn khối
  `BUG_LEDGER_v1` → đỏ 3 test (fail-closed, không im lặng cho qua). Không đột biến nào làm đỏ lây.
- Không đụng `scripts/tl.py` (ngoài bump VERSION) — **ruff delta 0**; GAS **KHÔNG đổi, vẫn 2.21.2p**.

# ★ v1.35.46 — r210: ĐỢT 2 LỚP ĐIỀU PHỐI — H3 kịch bản vòng lặp rà hồ sơ + H4 agent rà đơn vị read-only (+5 test, 1316/1316) (2026-07-26)

> Tiếp r209 (Đợt 1 đã merge). Đợt 2 KHÔNG xây engine mới: vòng lặp **BỌC** `tl rasoat-loop` +
> `tl frontier-expand` sẵn có và dùng nguyên bộ từ vựng hội tụ `dry_rounds`/`max_iter`/`PAUSE` — phần
> PLAN chỉ thêm cái chúng không có (trạng thái theo đơn vị, lưu bền, `session_claim`).

- **H3 — `references/RASOAT_HOSO_LOOP.md` (MỚI, vào `_RELEASE_REQUIRED_FILES` cùng `RASOAT_PLAN_SCHEMA.md`):**
  kịch bản vận hành đầy đủ — §0 ranh giới vai (phiên chính = BÊN GHI DUY NHẤT; agent read-only; worker
  Q-NLM không đụng state/registry) · §1 hợp đồng giao việc 6 mục · §2 Loop A A1–A8 kèm lệnh CÓ THẬT ·
  §3 Loop B B0–B6 (dò trùng `--refresh` TRƯỚC, chuẩn-bị-trước-duyệt-sau, bậc thang nguồn tải, tách kênh
  cache/NLM, đơn vị `doi_chieu_bo_sung` + bất biến done-không-reset) · §4 Loop C + §4b chế độ chạy-không-NLM
  (canary probe LIVE, CẤM tự `nlm-auth-load`) · §5 làn lỗi · §7 **khối máy-đọc `WRITE_PATHS_v1`** ·
  §8 đóng gói chủ động 40%/60% đo tại RANH GIỚI đơn vị · §9 nhịp registry cấm chen ngang.
- **H4 — agent `tl-rasoat`:** prompt mẫu đầy đủ trong §6 (dùng được ở LIVE nơi KHÔNG có file agent) +
  wrapper dev `.claude/agents/tl-rasoat.md` **ép cứng bằng frontmatter** (`tools` không có Write/Edit,
  `disallowedTools`, `maxTurns` — theo kho best-practice `claude-subagents.md`); prompt-only chỉ là lớp 2,
  LIVE phải hậu kiểm `verify-integrity` + `git status`. Kèm wrapper lệnh `.claude/commands/rasoat-hoso.md`.
  (`.claude/` bị release-exclude ⇒ wrapper là dev-side, không vào gói.)
- **SKILL.md (+58B ròng, 47.924B — vẫn dưới WARN):** thêm 1 dòng vocab nhóm lệnh + 1 dòng danh mục
  references trỏ kịch bản; **dọn mục GAS `2.21.2m`** (bản .gs dev-only, lịch sử đã ở CHANGELOG/DOCTRINE) và
  **sửa 2 chỉ dẫn SAI version**: `tl ping` phải ra `2.21.2p` (không phải `2.21.2m`), dòng đồng bộ tài liệu
  cũng về `2.21.2p` — LIVE là 2.21.2p từ r208-gas.
- Test 1311 → **1316** (+5 `r210_*`): `loop_khong_ghi_trong_cay` (bóc khối `WRITE_PATHS_v1`, PHẢN CHỨNG
  2 chiều: bơm đường ghi trong cây → bắt; thiếu khối → fail-closed) · `loop_doc_khop_the` (drift-guard
  prose ↔ thẻ máy: A1–A8, từ vựng hội tụ, MỌI `recommended_commands` phải được kịch bản gọi tên — test này
  đã bắt THẬT một drift: thiếu `profile-ingest --staged`, đã vá) · `agent_prompt_dung_schema` (schema JSON
  của agent khớp ĐÚNG bộ trường mẫu master + anchor) · `agent_wrapper_ep_cung` (frontmatter khoá cứng;
  vắng `.claude/` = LIVE → bỏ qua) · `skill_tro_kich_ban_va_gas_dung_ban` (khoá luôn việc hết `2.21.2m`).
- Golden regen CÓ CHỦ ĐÍCH 1 fixture (`workflow_audit`: `links_checked` 13→15 do 2 con trỏ mới trong SKILL.md).
  **GAS KHÔNG đổi — vẫn 2.21.2p.**

# ★ v1.35.45 — r209: ĐỢT 1 LỚP ĐIỀU PHỐI RÀ HỒ SƠ — H9 guard ratchet con trỏ + H0 vá đường cấp cứu LÕI + H1/H1b template master + H2 thẻ quy trình (+7 test, 1311/1311) (2026-07-26)

> Thi hành Đợt 1 kế hoạch `docs/KE_HOACH_RASOAT_HOSO_ORCHESTRATION.md` (nhánh kiến trúc 2al46n, grill
> 25→26-07 chốt 8/8 quyết định). Đo 26-07 trên v1.35.44: **80 cặp (tài_liệu, con_trỏ) đứt** trong
> SKILL.md + references/*.md — 65 ở DOCTRINE_APPENDIX (lưu trữ), **2 nằm ngay trong chỉ dẫn CẤP CỨU của
> LÕI** (`scripts/build_parts.py`/`scripts/tl_rebuild.sh` — đặc tả chi tiết rồi KHÔNG BAO GIỜ được viết;
> cơ chế `_parts/` đã bỏ từ khi Cowork bootstrap qua `tl_fetch.sh`, xem `tl_boot.py:4`).

- **H9 — guard RATCHET `_doc_pointer_findings` (release.py):** mở rộng REL-01 từ «references/ trong
  SKILL.md» ra «references/|templates/|scripts/ trong SKILL.md + references/*.md», đối chiếu PACKAGE-SET.
  Phân hạng: `_POINTER_ARCHIVE_DOCS` (DOCTRINE_APPENDIX → advisory, không sửa thân tài liệu lịch sử);
  `_POINTER_BASELINE` = **10 nợ cũ khoanh theo CẶP** (miễn trừ không lan giữa tài liệu) — hằng số trong
  code, sửa baseline = qua ruff→selftest→CHANGELOG→review; cặp MỚI đứt ở tài liệu sống ⇒ fail-closed
  (`DOC_POINTERS_NOT_IN_PACKAGE`, khóa `doc_pointers` trong release-verify).
- **H0 — vá đường cấp cứu LÕI (hướng (ii) SỬA LÕI, user chốt):** SKILL.md bỏ 4 vùng trỏ
  `build_parts`/`tl_rebuild`/`_parts` (−223B → 47.866B, thoát vùng WARN 47K); `COWORK_EDIT_SAFETY.md`
  viết lại lớp PHÁT HIỆN/KHÔI PHỤC theo sự thật: thang cứu hộ = `tl_boot.py` (strip NUL) →
  `verify-integrity` (chỉ mặt file hỏng) → **bước 0 `tl_fetch.sh` zip SẠCH** → RE-SYNC; hết đường ghép
  local, hết quy trình 5-bước chết.
- **H1 — `templates/MAU_BANG_TONG_HOP_PHAT_HIEN.json` (MỚI, vào `_RELEASE_REQUIRED_FILES`):** schema suy
  từ BÊN ĐỌC (`rasoat_phuluc.py:load_master` — thư mục *.json gộp, append-only mức thư mục), kèm
  `_vocab_hinh_thuc` 10 giá trị CÓ DẤU (route() khớp chuỗi cố định — không dấu rơi ÂM THẦM về 04, bẫy
  KHOÁ bằng test làm bằng chứng), `anchor` (neo phụ thuộc: doc_deps.text_hash + cite + ttl_ngay=90) +
  `muc_chac_chan` enum `chac_chan|can_kiem_tra|cho_verify_nlm` nhập từ đầu — KHÔNG có bước merge (local
  chưa từng có template). **Q2 (user chốt): XOÁ đặc tả `nlm_log.py`** khỏi `QUY_TRINH_RA_SOAT_3_TANG.md:91`
  → thay bằng `NHAT_KY_NLM_<sh>.csv` (khung sẵn của `rasoat_worksheet.py`) + quota đếm trong state.
- **H1b — `rasoat_phuluc.py` mở rộng TỐI THIỂU:** kết xuất phụ lục 04–07 nối `muc_chac_chan` +
  `anchor.cite` vào cột Ghi chú (bảng C không rơi mất mức chắc chắn/cite; master vẫn là nguồn sự thật).
- **H2 — thẻ `references/workflows/rasoat_hoso.json`** (`workflow_card.v1`, risk medium, đủ 12 trường,
  recommended_commands đều CÓ THẬT trong parser; vào `_RELEASE_REQUIRED_WORKFLOWS`) + đặc tả phần biến
  động `references/RASOAT_PLAN_SCHEMA.md` (`rasoat_plan.v1`: 4 hàng đợi + Q-VERIFY, claim/takeover 30′,
  hằng số vận hành chốt 26-07, nghi thức đóng gói A8).
- **ADR-0016** (state LAI · single-writer theo claim · anchor · guard ratchet) — trade-off + hệ quả.
- Test 1304 → **1311** (+7 `r209_*`): `pointer_findings_pure` (fail-closed manifest rỗng · archive
  advisory · baseline im · cặp mới đỏ) · `baseline_ratchet` (khoá số đếm 10 + miễn-trừ-không-lan) ·
  `cay_that_va_phan_chung` (cây thật 0 fail + PHẢN CHỨNG bơm dòng SKILL.md trước-H0 → đỏ đúng 2 con trỏ)
  · `skill_md_khong_tro_file_ma` (H0, prefix thư mục) · `master_template_va_vocab` (10/10 vocab + bẫy
  không-dấu + chuẩn NN-YYYY-VBHN-XXX) · `bang_c_du_truong` (H1b) · `the_rasoat_hoso_hop_le` (H2 +
  workflow-audit sạch). **GAS KHÔNG đổi — vẫn 2.21.2p.**
- Tồn đọng ghi nhận (KHÔNG sửa đợt này): `QUY_TRINH:81` nhắc `nlm_qa.py` (bare — đã hợp nhất vào tl) ·
  `QUY_TRINH:99` nhắc `manifest_build.py` (bản thật ở `scripts/_fallback/`) · SKILL.md §7 bản đồ script
  còn vài tên bare đời cũ — nằm ngoài vùng phủ guard (chỉ bắt con trỏ CÓ tiền tố), gỡ dần theo baseline.

# ★ v1.35.44 — r208d: van F7 ĐỔI TỪ CHẶN-THEO-TUỔI SANG CANARY LIVE trước lô (user duyệt 26-07; +1 test/1 đổi kỳ vọng, 1304/1304) (2026-07-26)

> Tiếp r208c. Ngưỡng F7 (`NLM_COOKIE_BATCH_MAX_MIN = 50`) dựng trên «đời cookie ~60′» mà r208c đo được là
> SAI: cookie phiên hạn **380 ngày**, chết là do token xoay `__Secure-1PSIDRTS` hết hạn mà CLI `nlm` không
> gia hạn. Hệ quả đo được: tuổi **vừa CHẶN OAN** phiên còn tốt, **vừa CHO QUA** phiên đã chết — phiên chết
> thật lúc `age_min` mới **5,2′** trong khi công cụ hứa «còn 54,8′».

- **Chốt chặn lô = verdict probe LIVE**, không còn là tuổi. Điểm khéo: `_rep54` ngay phía trên trong
  `cmd_ingest_missing` **đã probe rồi** (`probe=not _thr_over`, mà tới được cổng lô nghĩa là
  `_thr_over=False`) ⇒ canary **KHÔNG tốn round-trip mới**.
  - `alive=False` → **DỪNG rc=2 trước mọi side-effect**, reason `NLM_AUTH_DEAD_BEFORE_BATCH`, kèm `why`,
    `cookie_age_min`, `rotation_token_expired` và `fix` (chuỗi khắc phục r208b). Chỉ tới được nhánh này khi
    fallback TẮT (có fallback thì `_dead54` đã rẽ `BATCH_LINKS` phía trên). Trước r208d nhánh đó đi tiếp
    đường API rồi mới fail giữa chừng — dừng sớm vẫn fail-closed mà không để lại chuỗi dở dang.
  - `alive=None` → **KHÔNG chặn** (bài học M2 v1.33.35: không kết luận ≠ chết).
  - tuổi cao / token xoay hết hạn → **CẢNH BÁO** trước lô, không chặn.
- **Hằng đổi tên `NLM_COOKIE_BATCH_MAX_MIN` → `NLM_COOKIE_BATCH_WARN_MIN`** (vẫn 50) — tên cũ nói dối vì
  nó không còn là ngưỡng chặn. Re-export I11 cập nhật cùng đợt.
- `--force-api-add` GIỮ NGUYÊN là cửa ép chủ đích (không mở rộng cổng sang nhánh đó — hành vi có test
  `r115_ingest_missing_force_api_add_wins` khoá từ trước).
- Test 1303 → **1304** (+1 `r208d_canary_truoc_lo`: chết→rc=2 0 add + có đường ra · sống-nhưng-tuổi-99′→
  KHÔNG chặn, vẫn cảnh báo · `alive=None`→không chặn · token xoay hết hạn→cảnh báo). `r192_f7_cookie_50p_chan_lo`
  đổi tên/kỳ vọng CÓ CHỦ ĐÍCH → `r208d_f7_canary_thay_chan_theo_tuoi` (khoá cả việc tên hằng cũ đã BIẾN MẤT).
  Harness `_run_im110` thêm tham số `force_api_add` (mặc định True = hành vi cũ của mọi caller sẵn có).
  **GAS KHÔNG đổi — vẫn 2.21.2p.**

# ★ v1.35.43 — r208c mục 3.1: ĐO TRƯỚC RỒI MỚI VÁ — lật tiền đề «cookie chết sau ~1 giờ», bỏ `est_remaining_min` bịa, chống hạ cấp `nlm-auth-load` (+1 test/1 đổi kỳ vọng, 1303/1303) (2026-07-26)

> **Đo tươi trên jar THẬT (25-07 khuya), bắt đúng lúc phiên chết:**
> 1. **KHÔNG cookie nào có TTL ~1 giờ.** `SID`/`__Secure-1PSID`/`HSID`/`SSID`/`APISID`/`OSID` hết hạn
>    **2027-08-09 = 380 ngày**; `__Secure-1PSIDTS`/`SIDCC`/`__Secure-1PSIDCC` **365 ngày**. Hằng
>    `_NLM_COOKIE_LIFE_MIN = 60` (ghi chú «hồ sơ DBSC 2026-07-12») KHÔNG có gì trong dữ liệu đỡ.
> 2. **Credential ngắn hạn DUY NHẤT = `__Secure-1PSIDRTS`/`3PSIDRTS`** (token xoay phiên DBSC). Trong jar
>    nó **đã hết hạn 110 phút TRƯỚC** khi phiên chết.
> 3. **CLI `nlm` KHÔNG xoay cookie**: qua 2 lần gọi live, **không một giá trị nào đổi** (kể cả `1PSIDTS`,
>    `SIDCC`, csrf). Phiên không tự lành được — chỉ có thể THAY.
> 4. **Số đo đắt nhất:** `nlm-auth-status` trên phiên ĐÃ CHẾT in `alive:false` · `age_min:5.2` ·
>    **`est_remaining_min: 54.8`** · **`warn: []`**. Đầu phiên thì ngược lại: `alive:true` mà báo còn
>    `0.0'`. Sai CẢ HAI CHIỀU — không phải ước lượng kém, mà là **trấn an giả trên xác chết**.
> 5. `auth.json` (thứ `secrets-stage` đem gói) trễ hơn profile sống **127′**, `extracted_at` **415′**,
>    token xoay trong đó hết hạn **7,2 giờ** trước.
>
> **Kết luận:** nửa «không tự làm mới» của báo cáo ĐÚNG (số đo 3); nửa «chết sau ~1 giờ» KHÔNG đứng được —
> chết là do xoay phiên phía server mà client không theo được ⇒ **thời điểm chết không đoán trước được**
> (25-07 sống 68,1′; lần này chết khi `age_min` mới 5,2′). ⇒ **BÁC đề xuất gốc «tự gọi `nlm-auth-load`
> rồi thử lại»**: nó ghi đè profile bằng bản bundle, mà bundle đo được là CŨ HƠN.

- **BỎ HẲN `est_remaining_min`** khỏi `_nlm_preflight_report`/`nlm-auth-status` (schema → **`nlm_auth_status.v2`**).
  Thay bằng thứ ĐO ĐƯỢC: `rotation_token_expired` + `rotation_token_min` (hạn thật trong jar) và verdict
  probe LIVE. `age_min` GIỮ nhưng nói đúng nghĩa — thời gian từ **lần xác thực thành công gần nhất**,
  KHÔNG phải tuổi cookie, KHÔNG dự đoán được cái chết.
- **`_nlm_rotation_token_state()`** (PURE, jar tiêm được) + cờ **`ROTATION_TOKEN_EXPIRED`**: token xoay hết
  hạn ⇒ «phiên KHÔNG gia hạn được nữa, chỉ có thể thay bằng `nlm login`; vẫn có thể sống thêm rồi chết
  ĐỘT NGỘT — đừng mở lô dài». Tín hiệu có thật, kiểm offline, **0 round-trip**. `found=False` ⇒ không kết
  luận gì (tuyệt đối không suy ra «còn sống»).
- **`alive:false` nay LUÔN kèm đường ra** (`fix` + `warn[AUTH_DEAD]`) — trước đó `nlm-auth-status` báo chết
  với `warn: []`, đúng thứ báo cáo mục 3.2 phàn nàn. Vá nốt chỗ sót cuối còn hô `nlm login` trần (cảnh báo
  *overflow liveness* của doctor).
- **`nlm-auth-load` CHỐNG HẠ CẤP**: `_nlm_auth_load_downgrade` (PURE) so mốc `last_validated` bundle ↔ jar
  cục bộ TRƯỚC khi ghi đè; bundle cũ hơn ⇒ **TỪ CHỐI** kèm lý do + số phút, có `--force` để cố ý. Không đọc
  được một trong hai phía ⇒ KHÔNG chặn (máy chưa từng login vẫn nạp được).
- **Van F7 (`NLM_COOKIE_BATCH_MAX_MIN = 50`) và ngưỡng cảnh báo 45′ GIỮ NGUYÊN** — cả hai dựng trên TTL 60′
  vừa đo là sai, nhưng nới một chốt an toàn là quyết định của người vận hành, không phải của đợt vá này.
  Thông điệp đã nói rõ con số đó không dự đoán được cái chết để không ai bị ru ngủ.
- Test 1302 → **1303** (+1 `r208c_cookie_do_thay_vi_doan`: hạn token xoay · cờ · chống hạ cấp · re-export I11).
  `r115_preflight_report_two_tiers` đổi kỳ vọng CÓ CHỦ ĐÍCH (`est_remaining_min` không còn; chết phải có `fix`).
  **GAS KHÔNG đổi — vẫn 2.21.2p.**

# ★ v1.35.42 — r208b BƯỚC 3 (báo cáo 25-07): `register` tự điền/cảnh báo name+cat · thông báo auth chỉ ĐÚNG đường · `nlm-reconcile` LUÔN cho xem plan (+3 test, 1302/1302) (2026-07-25)

> Ba mục còn lại của báo cáo `BAO_CAO_van_de_skill_tra-luat_2026-07-25.md` sau r208 (2.2 slot-audit) và
> r208-gas (1.1 khoá ghi registry). **Không mục nào nới lỏng một chốt chặn nào** — 2.4 giữ NGUYÊN ngưỡng
> chặn r201/r206 và CỐ Ý **không** thêm `--trust-live`/`--after-restore`: registry có thể bị đua về rỗng
> bất cứ lúc nào, nên không lời khẳng định nào của người vận hành cứu được ca đó.

**2.1 — `register` không còn trả `ok:true` im lặng với `name:""`/`cat:""`** (`tl_core/source_ops.py`)
- Ca thật 25-07: 17 dòng ghép bằng `register --drive-id --nlm-source-id …` ra name/cat rỗng ⇒ corpus-audit
  gắn `NLM_GHOST_SOURCE`/`ORPHAN_CAT`/`MISSING_SOHIEU` trong khi file vẫn đúng folder cat 23 và nguồn vẫn
  SỐNG trên NLM. Cờ báo động giả kiểu đó khiến người vận hành dễ đi **XOÁ nhầm nguồn còn tốt**.
- **`_register_infer_name_cat`** (PURE, tiêm được bảng taxonomy): `name` = tên file Drive bỏ đuôi;
  `cat` = nhãn canonical `NN_Ten` tra theo (1) folder cha trong `config.categories` — **0 round-trip**,
  (2) TÊN folder cha khớp taxonomy 45+2 (kể cả folder trơ `23`), QUARANTINE giữ nguyên.
- **`_register_autofill`**: chỉ chạm cột trống ở **CẢ** lệnh **LẪN** dòng registry hiện có (không bao giờ
  đè giá trị đã ghi), TRÁNH cột đang `--clear-cols` (điền lại giữa lệnh xoá là chống ý định), bỏ qua lệnh
  thuần-xoá. Tốn ≤2 round-trip Drive và chỉ khi thật sự thiếu; **tái dùng chính `reg_get` của
  `_reg_row_present`** (tách `_reg_row_get`) nên KHÔNG thêm call GAS nào.
- Output mới: `autofilled` · `complete:false` + `incomplete_cols` + `warn[REGISTER_ROW_INCOMPLETE]` kèm
  lệnh chữa sẵn và nói thẳng hậu quả nếu để trống. Cờ `--no-autofill` để tắt.

**3.2 — mọi thông báo auth nêu ĐỦ chuỗi đúng thứ tự** (`nlm_cli.py` = nguồn sự thật)
- `nlm-auth-load` (headless, KHÔNG cần master key) → `nlm-auth-pull` (**nói rõ lấy `TL_MASTER_KEY` ở đâu**)
  → `nlm login` (**ghi rõ là TƯƠNG TÁC**, không chạy được ở Cowork/headless). Trước đây mọi thông báo chỉ
  hô `nlm login`, và `nlm-auth-load` — đường đúng — không chỗ nào nhắc.
- Hằng `AUTH_FIX_HINT`/`AUTH_FIX_HINT_SHORT` ở `nlm_cli` (3 nơi sinh `auth_hint`); `nlm_auth_fix_hint()`
  (`tl_core/nlm_ops.py`, re-export `_STUB_MAP`) cho slot-audit/`_live_source_count`/doctor; `tl_gws` và
  playbook `LISTING_CHANNEL_SUSPECT` dùng chung. **Drift-lock**: selftest bắt CẢ 7 biến thể (kể cả 2 bản
  dự phòng) phải nêu đủ 3 lệnh ĐÚNG THỨ TỰ — thông báo auth mới sau này không rơi lại về `nlm login` trần.

**2.4 — `nlm-reconcile` chặn thì vẫn phải CHO XEM** (`tl_core/nlm_admin_ops.py`)
- `--apply` bị guard chặn: rc=2 và **0 dòng registry được ghi** như cũ, nhưng nay in **plan đầy đủ ra
  stdout** (`mode:APPLY_BLOCKED`, `blocked_by`) + **ghi file JSON** để soát; error vẫn ở stderr (giữ kỷ
  luật «parse JSON đừng gộp `2>&1`»). Trước đây chỉ có error rc=2 ⇒ phải làm tay 17 dòng.
- DRY **LUÔN** ghi plan-artifact (mặc định `.tl_state/reconcile_plan_<nb>.json` — đúng đường
  `--from-plan auto`). Trước r208b chỉ nhánh `--all-notebooks` nội bộ mới đặt được `plan_out`; cờ
  `--plan-out` nay có trên CLI.
- **Chốt cửa hậu**: plan sinh lúc guard đang nghi mang dấu `verdict` và ghi tên `.BLOCKED.json` riêng;
  `--apply --from-plan` **TỪ CHỐI** (`PLAN_VERDICT_SUSPECT`) — đường from-plan không re-scan live nên guard
  bất hoạt ở đó, thiếu chốt này thì «luôn ghi plan» vô tình mở lối đi vòng qua chính cái chặn vừa giữ.
  `--force-unsafe` vẫn là cửa DUY NHẤT để đi tiếp.
- Helper tách để hai nhánh dùng chung: `_reconcile_plan_path` · `_reconcile_plan_artifact` (PURE) ·
  `_reconcile_write_artifact`.

Test 1299 → **1302** (+3: `r208b_auth_fix_chain_dung_thu_tu` · `r208b_register_tu_dien_name_cat` ·
`r208b_reconcile_luon_in_plan`). `parser_surface.json` regen (2 lệnh đổi: `register`, `nlm-reconcile`).
**GAS KHÔNG đổi** — vẫn 2.21.2p, không cần deploy.

# ★ v1.35.37 — r206: guard reconcile PHÂN ĐỊNH registry-mỏng vs kênh-liệt-kê (`REGISTRY_SCOPE_SUSPECT`) — ca thật 25-07 registry nền bị xoá còn 2 dòng (+2 test, 1297/1297) (2026-07-25)

> Sự cố thực địa 25-07: registry nền rơi còn **2 dòng** → `nlm-reconcile` thấy 300/300 nguồn live thành
> `unregistered`. Guard r201 chặn `--apply` ĐÚNG (rc=2, 0 ghi — cứu một vụ link/clear bậy 300 nguồn đè lên
> bản đã hỏng), NHƯNG hô sai bệnh: `LISTING_CHANNEL_SUSPECT` + playbook `nlm login`, trong khi
> `tl nlm-auth-status` báo `alive:true`/cookie 6,6′. Lời chẩn sai đẩy người vận hành đi chữa nhầm giữa lúc
> đang là CẤP CỨU MẤT DỮ LIỆU. **Ngưỡng CHẶN giữ NGUYÊN — đợt này chỉ sửa LỜI CHẨN.**
- **`_reconcile_suspect_kind(live_n, unreg_n, registry_n)`** (PURE, `tl_core/nlm_admin_ops.py`): chỉ chạy khi
  guard r201 ĐÃ bật; `registry_n < live_n * _RECONCILE_REGISTRY_THIN_RATIO` (20%) ⇒ `REGISTRY_SCOPE_SUSPECT`,
  ngược lại giữ `LISTING_CHANNEL_SUSPECT`; guard không bật ⇒ `""` (không chẩn bừa). Re-export I11 CÙNG ĐỢT
  (`_STUB_MAP` + hằng `_RECONCILE_REGISTRY_THIN_RATIO` trực tiếp).
- **Hai playbook tách hẳn**: nhánh registry-mỏng trỏ `counts --refresh` → `profile-info --json` (kiểm
  `registryDocId`) → **version history Sheet** → `journal`/Executions, và ghi rõ **⛔ ĐỪNG `--force-unsafe`
  khi registry đang mỏng**; nhánh kênh-liệt-kê giữ nguyên văn r201 (đổi kênh / `nlm login` / đo máy khỏe).
  JSON `--apply` nay trả `error` = đúng verdict + `registry_rows_seen`.
- **`registry_rows_seen` vào output MỌI lần** (kể cả không có verdict) — số dòng registry lúc đối soát, để
  đọc report là thấy ngay registry dày/mỏng.
- Test: 1295 → **1297** (+2: `r206_suspect_kind_pure` biên 20% · `r206_reconcile_registry_thin_verdict`
  khoá verdict/playbook/`--apply` rc=2 KHÔNG ghi + vế registry-dày vẫn ra `LISTING_CHANNEL_SUSPECT`).
  Fixture `r201_reconcile_listing_channel_guard` đổi CÓ CHỦ ĐÍCH 1→30 dòng registry: bệnh kênh-liệt-kê
  THẬT thì registry vẫn dày, kỳ vọng `LISTING_CHANNEL_SUSPECT` GIỮ NGUYÊN.
- `references/GOTCHAS.md` **§11 mới**: đọc verdict reconcile · `counts` không `--refresh` là snapshot cũ ·
  **`tl journal` là file CỤC BỘ theo clone** (truy nguyên phải dùng version history Sheet + Apps Script
  Executions) · `profile-delete-assets` đã kiểm là xoá đúng scope · phiên REMOTE bị egress chặn Google
  (bẫy `script.googleusercontent.com`) · 12 `F821` trên clone tươi là GIẢ.

# ★ v1.35.36 — r205 WP7 R-c TRỌN GÓI: GỠ FALLBACK organize 12-call (guard SERVER_TOO_OLD fail-closed) + DI TRÚ resume LÊN PIPELINE + LOCK ingest_to_cache chỉ-cache (grill nhỏ 25-07 user duyệt (a) hẹp/(b) khuyến nghị/(c) CÓ làm; +3 test/−1 đổi kỳ vọng, 1295/1295) (2026-07-25)

> Đợt R-c khép chuỗi WP7 R-a→R-b→R-c (ADR-0004). GAS 2.21.2o KHÔNG đổi; SKILL.md CHỈ đổi header.
- **(b) GỠ fallback organize** ở CẢ HAI `_pi_stage_write` + `_il_stage_write`: `_ingest_commit_supported`
  nay là GUARD fail-closed — server <2.21.2o (hoặc ping lỗi/transient) ⇒ rc=2
  `SERVER_TOO_OLD_FOR_INGEST_COMMIT` TRƯỚC khi ghi (charact: fallback lane dừng ngay sau ping, 0 write),
  KHÔNG lặng lẽ đi đường 12-call không ai soak; upload đã journal → chạy lại + `--resume` tái dùng.
  Nhánh sheet (copy_convert) + nhánh resume-skip GIỮ NGUYÊN. 6 harness selftest cũ nâng fake gas
  (ping 2.21.2o + nhận `ingest_commit` trả envelope thiếu `file` → readback đi `_verify_convert_readback`
  như cũ — flow test giữ nguyên); 2 lock commit-vs-fallback (r198/r204) đổi kỳ vọng CÓ CHỦ ĐÍCH thành
  `r205_*_commit_only_server_guard`.
- **(c) `cmd_profile_ingest_resume` = adapter run_pipeline**: bảng 5 stage `_pr_stage_*`
  `plan→confirm→stage→write→commit` (KHÔNG stage readback riêng — `_verified_reg_write` vốn fused
  write+verify, thêm readback rời = đổi số call trái parity), thân bê NGUYÊN VĂN (identity gate
  r184/ADR-0011-D5 nguyên vị trí ở confirm; DRY_REPAIR = outcome stop); re-export I11 cùng đợt.
  **Parity: charact resume pre ≡ post BYTE-EQUAL cả 3 lane** (dry name-only / apply single / apply
  chunks — `.tl_state/charact_{pre,post}_resume.json`); r116×4 + r184×2 resume tests pass NGUYÊN TRẠNG.
- **(a) lock `ingest_to_cache` chỉ đọc/ghi cache** (ADR-0004 Đ3, phạm vi hẹp): sweep xác nhận action
  Drive chỉ còn {exportdocx, exporttext, vb_status} (đọc) + `fetch_drive_convert_docx` = stub raise
  `CACHE_ONLY_NO_DRIVE_CONVERSION` (đã vá từ trước); test khóa `r205_ingest_to_cache_chi_doc_ghi_cache`
  chặn mọi mutation thêm sau này.
- Parity tổng R-c: il/zip happy lanes ≡ R-b byte-equal; PI call-seq/rc/output ≡ R-a (khác duy nhất
  hash fixture do bed đổi đường dẫn phiên — artifact, không phải drift); K1 plan DRY bất biến kể cả
  lane fallback. Sổ drift R-c: TRỐNG (thay đổi hành vi duy nhất = guard (b) đã duyệt).
- Test: 1293 → **1295** (+3: `r205_resume_via_pipeline` · `r205_ingest_to_cache_chi_doc_ghi_cache` ·
  guard il; 2 lock cũ đổi kỳ vọng, wiring r204 il thêm vế cấm organize). WP7 LÕI: **R-a+R-b+R-c XONG
  TRỌN** — còn theo dõi soak thực địa + đo NLM lô khi cookie sống.

# ★ v1.35.35 — r204 WP7 R-b: DI TRÚ ingest-local LÊN PIPELINE **GỘP** CHUYỂN GAS ingest_commit + ZIP ADAPTER (p11 mục 2 + quyết định 1(b)/α; bench 33,1 s/file −58%; +3 test/−1, 1293/1293) (2026-07-25)

> Thi hành đợt R-b của KE_HOACH WP7 lõi (grill 25-07 — KHÔNG re-litigate; chuỗi tăng tốc theo lệnh user,
> không chờ soak 30-07): MỘT lần đổi trên hàm ~700 dòng — di trú `cmd_ingest_local` lên `run_pipeline`
> ĐỒNG THỜI chuyển stage write sang GAS `ingest_commit` (khuôn r198 profile-ingest). GAS 2.21.2o KHÔNG đổi
> (`doIngestCommit_` vốn nhận đủ tham số nhánh ingest-local: cat NN/sohieu/goc/loai/reg_cat — ghi chú
> APP_VERSION 2.21.2o «client r198 chỉ dùng nhánh profile» nay hết treo).
- **`cmd_ingest_local` = adapter run_pipeline**: bảng 6 stage `_il_stage_*` chuỗi ADR `plan→confirm→stage→
  write→readback→commit` (re-export I11 CÙNG ĐỢT — bài học NameError 24-07), thân stage BÊ NGUYÊN VĂN code
  cũ (cat/recat gate, F1 dedup sohieu live, F4 PDF-ảnh, F5 van kích thước, S1 OCR gate, claim F-04, resume
  N6 — giữ trọn vị trí/thứ tự); đếm write/readback ADR-0004 đủ 6 stage.
- **Điểm đổi CÓ CHỦ ĐÍCH duy nhất (stage write)**: feature-detect `_ingest_commit_supported` ≥2.21.2o →
  MỘT call `ingest_commit` thay `organize` + convert-readback từ CHÍNH response (0 call thêm —
  `_ingest_commit_readback`, expected_folder_id="" như đường cũ); server cũ → organize GIỮ NGUYÊN
  (fallback — R-c gỡ = xóa 1 nhánh). Backfill sohieu/title_vn + registry readback (reg_get refresh)
  GIỮ NGUYÊN (doctrine verified-write).
- **Parity K1/K2/K3 ĐẠT** (bed `.tl_state/charact_{pre,post}_ingestlocal.json`, 4 lane main/no-nlm-add/
  drive-id/fallback): K1 plan DRY **byte-equal kể cả plan_hash** cả 4 lane · K2 output apply + rc y hệt,
  chuỗi call chỉ lệch TRONG stage write đúng khuôn duyệt (organize→ping+ingest_commit, okw BẰNG TUYỆT ĐỐI;
  lane fallback = cũ + đúng 1 ping) · K3 selftest cũ pass nguyên trạng (4 source-lock r55/r95/r192×2 chỉ
  đổi CHỖ TRỎ getsource sang ghép 6 stage — kỳ vọng giữ nguyên). Sổ drift R-b: TRỐNG.
- **ZIP adapter (phần 2)**: child ingest-zip/profile-ingest-zip chạy in-process qua build_parser (r187) =
  CHÍNH cmd đã di trú → TỰ đi pipeline + ingest_commit, `zip_ingest.py` 0 diff; charact 1 ca zip-1-docx
  DRY+apply (`.tl_state/charact_{pre,post}_zip.json`, pre chụp từ git worktree HEAD r203): bundle plan
  byte-equal, output y hệt, lệch duy nhất = khuôn write-stage.
- **Benchmark sống** (3 docx ~60k ký tự khác chủ đề, profile thử BenchRb204 tạo-đo-dọn, lane --no-nlm-add —
  phần NLM R-b không đổi): 33,3/30,5/33,1 s → **median 33,1 s/file ≤ trần 56,7 s**, so ~78 s/file đường
  organize cũ (baseline 24-07) ≈ **−58%**; profile-delete --trash-assets dọn sạch, config 0 vết.
- Test: 1291 → **1293** (+3 `r204_*`: wiring pipeline ingest-local · call-count commit-vs-fallback ·
  wiring child ZIP; −1 `r198_ingest_local_giu_duong_cu` — lock «giữ đường cũ chờ soak» hết hiệu lực CÓ
  CHỦ ĐÍCH theo quyết định 1(b)). CÒN: **R-c** (ingest_to_cache + gỡ fallback + cân nhắc di trú resume —
  grill nhỏ 3 quyết định với user trước khi code).

# ★ v1.35.34 — r203 WP7 R-a: STATE MACHINE `run_pipeline` + DI TRÚ profile-ingest (ADR-0004 Đ1; parity K1/K2/K3 ĐẠT; +3 test, 1291/1291) (2026-07-25)

> Thi hành đợt R-a của KE_HOACH WP7 lõi (`C:\qh\p13_wp7_2026-07-25\KE_HOACH_WP7_LOI_R-a.md` — grill 25-07,
> 8 quyết định user duyệt từng câu). Refactor BẢO TOÀN HÀNH VI nghiêm ngặt — Sổ drift: TRỐNG.
- **Engine** (`tl_core/ingest_engine.py`, stdlib thuần không bind): +`run_pipeline(stages, ctx)` — engine sở
  hữu TRÌNH TỰ + FAIL-CLOSED (`{"rc":n}` dừng, `{"stop":X}` outcome hợp lệ DRY_PLAN/STAGED_STOP/DONE) +
  ĐẾM write/readback (`_counts`; mỗi resource ≤1 write/stage — vượt = `PIPELINE_WRITE_BOUND`; xuyên-stage
  hợp lệ cho ca late-draft rename) + `ctx._trace`; I/O tiêm qua ctx (fake-ctx test offline 100%).
- **`cmd_profile_ingest` = adapter**: MỘT bảng stage chuỗi ADR `plan→confirm→stage→write→readback→commit`;
  thân stage (`_pi_stage_*` ×6, re-export I11 CÙNG ĐỢT — bài học NameError 24-07) bê NGUYÊN VĂN code cũ;
  feature-detect ingest_commit NHỐT trong stage `write` (quyết định α — R-c gỡ fallback = xóa 1 nhánh);
  `--staged` = outcome `STAGED_STOP` (ADR-0015 nguyên vẹn); resume/OCR-bridge/chunks/ZIP NGOÀI khuôn R-a.
- **Parity 3 lớp ĐẠT** (`.tl_state/charact_{pre,post}_wp7.json`, bed cố định 3 lane main-NLM/no-nlm-add/staged):
  K1 plan DRY **byte-equal kể cả plan_hash** · K2 chuỗi call trùng khớp 18/18 phép so · K3 toàn bộ selftest
  cũ pass nguyên trạng (r116/r184/r198/r200 không đổi một ca).
- **Benchmark sống** (3 docx 60k ký tự, profile thử BenchWP7 tạo-đo-dọn): 44,0/45,5/43,1 s → **median
  44,0 s/file ≤ trần 56,7 s** (baseline 49,3+15%) — overhead khung ≈ 0.
- Test: 1288 → **1291** (+3 `r203_*`: run_pipeline halt/merge/stop · write-bound ADR-0004 · wiring khung).
  CÒN theo kế hoạch: **R-b** ingest-local (GỘP chuyển ingest_commit p11) + ZIP · **R-c** cache + gỡ fallback
  + cân nhắc resume (chuỗi TĂNG TỐC theo lệnh user 25-07 — không chờ soak 30-07).

# ★ v1.35.33 — r202 BACKUP CONFIG PROFILE-DELETE RA NGOÀI CÂY SKILL (doctrine r193; +1 test, 1288/1288) (2026-07-25)

> Gốc: Tầng-3 smoke 25-07 phát hiện `profile-delete --trash-assets --apply` để lại
> `tra_luat_config.v2.<profile>.bak.json` (CHỨA token webapp) ở GỐC cây skill — vi phạm doctrine r193
> «backup config KHÔNG BAO GIỜ nằm trong cây skill» (bundle đã có guard TOKEN_IN_BUNDLE + exclude `.bak`
> nên KHÔNG lọt zip, nhưng file vẫn nằm trên đĩa trong cây). Sweep toàn scripts: đây là điểm ghi DUY NHẤT
> (profile-rename/use/config-pin-registry đều ghi config qua `_write_json_atomic`, không tạo `.bak`).
- **Helper mới** `profile_env._config_backup_dir()` (re-export I11 vào tl.py): đích cho MỌI backup config —
  `TL_CONFIG_BACKUP_DIR` (test/override) → `D:\Quốc hội\_config_backups` (máy chuẩn, chỉ khi ĐÃ tồn tại)
  → `%LOCALAPPDATA%\tra-luat\_config_backups` (máy lạ); mkdir tự động.
- **`cmd_profile_delete`**: backup đổi từ `Path(path).with_suffix(….bak.json)` (= CẠNH config, tức gốc cây)
  sang `_config_backup_dir()/<tên-cũ-giữ-nguyên>`; tên file + nội dung + trường `config_backup` trong output
  GIỮ NGUYÊN — chỉ đổi thư mục.
- Test: 1287 → **1288** (`r202_profile_delete_backup_ngoai_cay` — chỉ-nó-chặn: apply xong thư mục config
  SẠCH `.bak`, backup tròn nội dung nằm đúng TL_CONFIG_BACKUP_DIR, env unset ⇒ đích mặc định vẫn NGOÀI
  cây skill). Selftest xanh CẢ HAI trạng thái env; gate release-check 39/39; GAS 2.21.2o KHÔNG đổi.
  SKILL.md CHỈ đổi header version (đẳng dài) ⇒ re-import KHÔNG bắt buộc (nợ re-import r200 vẫn còn nếu chưa làm).

# ★ v1.35.32 — r201 GÓI 4 FIX VẬN HÀNH ĐẢNG/NLM (grill 7 vấn đề 24-07 đêm; +5 test, 1287/1287) (2026-07-24)

> Nguồn: báo cáo 7 vấn đề phiên vận hành Chat (nạp 342/348-QĐ/BTCTW) → grill chốt 3 quyết định C1-C3.
> FIX-A/B vá ở phiên trước (commit WIP `15dcf70`), FIX-C/D + test tier-3 phiên này — release gộp 1 gói.
- **FIX-A** `tl.py:_looks_like_sohieu_query`: +nhánh `_dang_bare_key` (fullmatch khóa chuẩn hóa toàn truy
  vấn — KHÔNG substring) — `exists "342-QD-BTCTW"`/`"342-QĐ/BTCTW"`/`"04-CT-TW"` hết not-found OAN
  (trước: cổng đòi năm/VBHN nên tier sohieu bỏ đói phép nới D5).
- **FIX-B** `tl_core/classify.py:_profile_title_from_header` — 3 defect: (a) stop-tại-«Căn cứ» CẢ 2 vòng;
  (b) loại Đảng đứng riêng (QUY ĐỊNH/QUY CHẾ/…) ghép dòng «VỀ …», bỏ dòng kẻ; (c) strip zero-width/BOM
  per-line. Ca sống 342: title = «QUY ĐỊNH VỀ HỆ THỐNG THÔNG TIN LĨNH VỰC TỔ CHỨC XÂY DỰNG ĐẢNG».
- **FIX-C** `nlm-reconcile` guard nghi-kênh (quyết định C2): live ≥ 20 VÀ unregistered/live > 50% →
  verdict **`LISTING_CHANNEL_SUSPECT`** (hằng `_RECONCILE_SUSPECT_*`, re-export I11): DRY vẫn in report
  + banner LOUD + playbook (đổi kênh / `nlm login` / đo máy khỏe); `--apply` **DỪNG rc=2 TRƯỚC mọi ghi**
  (trước preflight/gate/journal); override tường minh `--force-unsafe`; verdict nổi lên per_notebook của
  `--all-notebooks`. Gốc: ca «300 unregistered» phiên Chat = kênh liệt kê suy hoá trả id lạc namespace,
  tool IM LẶNG suýt link/clear bậy hàng loạt (máy khỏe đo 2/300 = 0,7%).
- **FIX-D** `_ingest_perf_hint` +1 câu: thêm cờ SAU dry-run ⇒ plan_hash đổi ⇒ phải DRY lại (by design —
  tránh PLAN_HASH_MISMATCH oan; hint vẫn im khi đã dùng cờ nhanh).
- **Đóng KHÔNG vá** (verdict grill): **#3** «ingest không regen manifest» = FALSE ALARM (GAS
  `doManifestExport_` gọi `regReadAll_(true)` dựng tươi mỗi refresh — cú miss là hệ quả bug #2/FIX-A);
  **#7** DUP_DIEU 348 = HỢP LỆ (doc = Quy định Đ1-8 + Quy chế «kèm theo» đánh lại Điều — đúng doctrine
  L6, info-only là hành vi đúng).
- Test: 1282 → **1287** (+2 phiên trước `r201_exists_sohieu_dang_bare`, `r201_title_dang_quydinh_cancu_bom`;
  +3 phiên này: `r201_reconcile_listing_channel_guard` (5 ca: DRY banner · apply rc=2 0-ghi · force-unsafe
  đi tiếp · 2/300 lành · 5/5 live<20 không kích) · `r201_reconcile_title_bridge_tier3_lock` (khóa tier-3:
  link title duy nhất / ownership guard / không re-point sid — thay golden fixture vì golden không chạy
  offline với NLM live) · `r201_perf_hint_plan_hash_note`). Selftest xanh CẢ HAI trạng thái env; GAS
  2.21.2o KHÔNG đổi. SKILL.md CHỈ đổi header version (đẳng dài 48089 B) ⇒ re-import KHÔNG bắt buộc
  (nợ re-import r200 vẫn còn nếu chưa làm).

# ★ v1.35.31 — r200 LANE STAGED: `profile-ingest --staged` + `verify-staged` PARITY → BULK-FLIP (ADR-0015; +4 test, 1282/1282) (2026-07-24)

> Grill 24-07 phần 2 (C2-C6): «corpus trước, verify sau» NHƯNG không đảo doctrine — staged (corpus=false)
> → verify parity → bulk-flip r197. Poison window = 0; ADR-0004 giữ nguyên (hoãn ≠ bỏ hậu điều).
- **`profile-ingest --staged`** (v1 CHỈ profile-ingest — tiền lệ r198): GIỮ cổng AN TOÀN lúc nạp (dup-name
  registry + claim đường commit + convert-readback trong `ingest_commit`, 0 call thêm); DỪNG ngay sau
  readback — HOÃN iv đọc-toàn-văn + v verify_gate + vi quét Điều/chunk + NLM. Registry `corpus=false`,
  note **`staged:pending;sq=<q>`** (marker = cột note, KHÔNG thêm cột schema). **TỪ CHỐI pdf/ocr/sheet**
  rc=2 `STAGED_LANE_REFUSES_SOURCE` TRƯỚC mọi side-effect. Plan/options chỉ thêm key `staged` KHI staged
  (plan_hash cũ giữ nguyên — 0 churn golden).
- **`tl verify-staged`** (generated, contract `verify_staged`, high/confirm/dry-run): dò note `staged:*`
  trên manifest refresh LIVE (bài học reg-query 24-07) → chạy ĐÚNG bộ iv+v+vi (PARITY — đổi thời điểm,
  KHÔNG đổi tiêu chuẩn). DRY = báo cáo; `--apply --confirm yes`: PASS → **bulk-flip corpus=true + note
  thật** (1 `reg_bulk` journaled trước-ảnh từng dòng — `tl undo <run>` cả lô); FAIL → Ở LẠI staged
  (note `staged:fail:<FLAG>`), KHÔNG auto-xóa/KHÔNG NLM; file vượt chunk_max vẫn flip + flag
  `needs_chunk_pipeline`. NLM nạp SAU flip (van 1 + bảng tay khối ≤4 r199, `nlm_status` theo ADR-0010).
- Docs: **ADR-0015** (Accepted — 5 quyết định, có phân loại cổng AN TOÀN/CHẤT LƯỢNG theo ADR-0004);
  CONTEXT.md +«Staged ingest (lane trì hoãn)» +«Verify parity» + vá «Ingest thành công» (ngoại lệ duy nhất
  vế corpus); SKILL.md +vế STAGED dòng BA VAN (+254 B) − diet 2 vế lịch sử/trivia mục #15 (−246 B)
  ⇒ 48081→48089 B (trần 48128). **SKILL.md ĐỔI NỘI DUNG ⇒ RE-IMPORT Capabilities.**
- Test: 1278 → **1282** (+4 `r200_*`: từ-chối pdf/ocr/sheet trước side-effect · staged apply bỏ iv/v/vi
  (0 read_doc_text, 0 nlm_add, note đúng marker) · verify-staged parity + flip đúng lô (dòng không-staged
  không bị đụng, before-image đủ) · needs_chunk_pipeline). Selftest xanh CẢ HAI trạng thái env;
  parser_surface regen chủ đích (`--staged` + verify-staged); golden re-bless workflow_audit (+1 lệnh,
  size_bytes SKILL) + tool_inventory (154 lệnh, 28 high-risk).

# ★ v1.35.30 — r199 BẢNG TAY NLM CHIA KHỐI ≤4 URL (grill 24-07 C1; +1 test, 1278/1278) (2026-07-24)

> Grill 24-07 (6 quyết định, C1 chốt «giữ van 1, chỉ sửa bảng tay»): NLM hay chết khi người dùng dán cả lô
> dài một lượt lên UI — bảng tay nay CHIA KHỐI để sự cố khoanh vùng theo khối, không mất cả lô.
- `_nlm_links_md` (PURE, `tl_core/nlm_ops.py`): lô >`NLM_BATCH_LINKS_THRESHOLD`(=4, tái dùng hằng r192 —
  KHÔNG đẻ hằng mới) → chia `## Khối k/N — [mở notebook](url)` mỗi khối ≤4 link + dặn CHỜ NLM nhận xong
  khối trước rồi mới dán khối kế; lô ≤4 giữ dạng phẳng r192 Y HỆT (byte-level). Hưởng chung cả 2 caller:
  `nlm-links --md-out` + nhánh BATCH_LINKS của `ingest-missing`.
- Van 1/2/3 GIỮ NGUYÊN ngữ nghĩa (không re-litigate r192): auto-add vẫn chỉ lô ≤4; vế «auto bulk tách cụm»
  của đề xuất gốc tự tan vì đường auto không bao giờ vượt 1 cụm.
- Test: 1277 → **1278** (+1 `r199_van1_bang_tay_chia_khoi_4`: 9 nguồn → đúng 3 khối 4+4+1, khối 1 có Doc_3
  KHÔNG có Doc_4, link notebook tại header khối, chữ «chờ», hẹn reconcile; 3 nguồn → KHÔNG chia khối).
  Selftest xanh CẢ HAI trạng thái env (trần + TL_WEBAPP/TL_TOKEN export). SKILL.md CHỈ đổi header version
  (đẳng dài 48081 B) ⇒ re-import KHÔNG bắt buộc.
- CONTEXT.md: mục «Bảng tay (nạp NLM)» ghi nhận thể thức chia khối.

# ★ v1.35.29 — r198 INGEST_COMMIT: GỘP 4 BƯỚC INGEST THÀNH 1 ROUND-TRIP GAS (ADR-0014 Accepted + GAS 2.21.2o; +6 test, 1277/1277) (2026-07-24)

> KE_HOACH p11 §5 (quyết định #4/#5/#6 duyệt 24-07). ADR-0014 viết TRƯỚC khi code, trạng thái **Accepted**
> — supersede mục HOÃN `ingest_pipeline` (KE_HOACH_VA_SKILL_r191_r192 §3); lý do bỏ cổng-1-tuần ghi rõ trong
> ADR (số đo 24-07 trên đường sản xuất thật, khuôn r192 đã áp đủ, ingest vẫn đồng-nút-cổ-chai; ~2s/call cố
> định ⇒ giảm SỐ CALL là đòn bẩy duy nhất). Baseline: 12 call ≈ 68s/file, trong đó reg_get×3+info×3 = 14s
> CHỈ ĐỂ ĐỌC LẠI.
- **GAS 2.21.2o** (deploy clasp GIỮ deployment ID `AKfycbzNrsxGYjFkzT…` @79; ping xác nhận 2.21.2o + đo lại
  sau 25s ổn định; ADDITIVE — client cũ không đổi hành vi): action **`ingest_commit`** = organize(+rename)+
  register+READBACK (row snapshot `reg_get refresh=true` + file/src info) MỘT round-trip; **sub-step marker**
  `organize_done/rename_done/upsert_done` — lỗi giữa chừng trả PARTIAL (đã-xong-gì) cho journal/`--resume`
  (ADR-0011/D5) map điểm đứt; tham số đủ cho CẢ ingest-local (cat NN) lẫn profile (cat=folderId flat).
  Smoke sống 0-mutation (fileId bundle, convert/register=false): ok, marker đủ, elapsed 1,5s server.
- **Client r198 — CHỈ `cmd_profile_ingest` chuyển đường** (quyết định #6; `ingest-local` giữ 12-call, chuyển
  sau soak — ca guard ghim source): helper `_gas_version_at_least` (PURE, tuple số+đuôi chữ; parse hỏng →
  False fail-safe) · `_ingest_commit_supported` (feature-detect ping ≥2.21.2o, cache 1 ping/process qua
  `_GAS_VER_CACHE` — mutable sống ở tl.py, bẫy I11) · `_ingest_commit_call` (partial → step
  `ingest_commit:<điểm đứt ĐẦU TIÊN>`; transport/shape tường minh) · `_ingest_commit_readback` (dựng
  `convert_readback.v1` từ file/src_file TRONG response — 0 call thêm, CÙNG BỘ phép kiểm
  `_verify_convert_readback`). Server cũ → nhánh organize GIỮ NGUYÊN (fallback 2 code path = nợ bảo trì có
  chủ đích, gỡ sau soak — ADR). Journal giữ nguyên số bước intent/commit; resume contract không đổi.
- Đồng bộ contract: `EXPECT_VERSION` 2.21.2n→**2.21.2o** (drift-lock r119) + pin `expect_version` đổi CÓ CHỦ
  ĐÍCH; API_CONTRACT.md đóng dấu 2.21.2o + row `ingest_commit`; SKILL.md target 2.21.2n→2.21.2o byte-đẳng-dài
  (48081B KHÔNG đổi — không đụng golden size); repo +`references/Code.2.21.2o.gs`, bundle exclude 2.21.2n
  (tiền lệ r194; ca r130 cập nhật theo).
- Test: 1271 → **1277** (+6 `r198_*`: version-compare PURE · feature-detect cache 1 ping + fail-safe ·
  partial marker → step đứt · readback từ response cùng bộ phép kiểm · call-site 2.21.2o = ĐÚNG 1
  ingest_commit/0 organize/0 info vs 2.21.2n = fallback y cũ · guard ingest-local giữ đường cũ).

# ★ v1.35.28 — r197 BULK CORPUS-FLIP CLIENT-ONLY (KE_HOACH p11 §4, quyết định #3 duyệt 24-07; +3 test, 1271/1271) (2026-07-24)

> Gốc số đo: `source-update-corpus` ~15 s/Ô × 26 lượt ≈ 400 s (baseline §3 KE_HOACH). Server KHÔNG đụng —
> `reg_bulk` (v2.13.7) + `reg_get_bulk` (v2.21.2l) có sẵn. Số release trượt +1 so kế hoạch gốc (r196 đã bị
> phiên vá TRINH 3.9/3.11 dùng — ghi chú hồi tố đầu KE_HOACH).
- **`source-update-corpus` nhận N target** (parser `target` nargs='+', positional `status` giữ cuối; 1 target
  = hành vi CŨ Y HỆT — hồi quy 0, ca r180 S5/r52 giữ nguyên). N>1 → lane bulk `_source_update_corpus_bulk`:
  - Phạm vi **registry-thuần**: `true` hoặc `false --as-ref`; `false` trần → rc=2 `BULK_PLAIN_FALSE_REFUSED`
    (gỡ NLM là chuỗi side-effect per-row — đi từng dòng như cũ; khớp từ vựng «Hạ ref» CONTEXT.md).
  - **Auto-refresh manifest TRƯỚC plan** (bài học 24-07 nạp chồng 9 tài liệu vì cache cũ); DRY in bảng N dòng
    before/after (name, drive_id, corpus cũ→mới, row_kind cũ→mới, nlm_status); fail-closed CẢ LÔ khi có
    target lỗi (`BULK_TARGETS_NOT_OK`) hoặc 2 target trỏ cùng dòng (`BULK_DUPLICATE_ROWS`).
  - Ghi = **1 `reg_bulk`** (qua `_journaled_reg_write`: intent{before}/commit per-row, bust cache đúng 1 lần)
    + **1 `reg_get_bulk`** verify AUTHORITATIVE per-row (lệch dòng nào báo dòng đó — không tin patched trần).
  - Journal **1 run/N before-image** → `tl undo <run>` khôi phục CẢ LÔ. Trần payload: tiền lệ L4 22-07 ghi
    118 dòng/1 reg_bulk OK — lô 26 trong biên, không cần chunk.
- SKILL.md: +vế N target=LÔ ở dòng cổng OCR/corpus (+67 B) − diet vế diễn giải lịch sử PROFILE_NOT_FOUND
  (−81 B) ⇒ 48095→48081 B (trần 48128); golden re-bless đúng trường (`workflow_audit.size_bytes` +
  `parser_surface` nargs) — sửa SKILL.md bằng byte-replace, KHÔNG write_text (bẫy CRLF §0).
- Test: 1268 → **1271** (+3 `r197_*`: parser N/1 target; plain-false rc=2 trước mọi đọc/ghi; lô 4 = DRY bảng
  4 dòng + auto-refresh + đúng 1 reg_bulk + 1 reg_get_bulk + journal 4 before + undo đủ 4 restore). Selftest
  xanh CẢ HAI trạng thái env (trần + TL_WEBAPP/TL_TOKEN export).

# ★ v1.35.27 — r196 VÁ 2 BẪY PHIÊN 24-07: BRIDGE OCR TỰ CHẾ CAM KẾT + NLM-ADD 404 RẼ NHẦM «OFFLINE» (TRINH 3.9/3.11; +6 test, 1268/1268) (2026-07-24)

> Gói việc TRINH_CONG2_DELTA mục 3.8/3.9/3.11. Mục 3.8 (fixture golden `workflow_audit` links_checked
> 14→13) XÁC NHẬN ĐÃ ĐÓNG từ r195 (đo tươi golden-test 19/19 ok:true) — không làm lại.
- **3.11 — bridge `ingest-ocr`/`profile-ingest-ocr` HẾT tự truyền `--ocr-verified`** (ca thật A-8 VCB 10838:
  verify_gate child in `ocr_verified=true` mà không ai cam kết; máy-đo-xanh ≠ người-đã-đối-chiếu — chính
  `ocr-verify` XANH vẫn dặn «nếu đã đối chiếu bổ sung bằng mắt/nguồn gốc»; đường VBQPPL thủng cổng S1 r180).
  Nay: 2 spec bridge nhận cờ `--ocr-verified` tường minh và CHỈ forward khi có; thiếu → rc=2
  `OCR_VERIFIED_ATTESTATION_REQUIRED` TRƯỚC child (fail trước side-effect) + hint đối chiếu neo ≥6
  từ/trang/Điều/phụ lục; verify máy đỏ vẫn chặn như cũ (HAI TẦNG độc lập: máy đo ∧ người cam kết). Docs
  đồng bộ: khối `van_ban_lon` gen_instructions + workflow card `ocr_ingest.json` (plan/apply/stop_conditions)
  — re-bless golden `route_task_ocr_ingest` + regen `parser_surface.json` CÓ CHỦ ĐÍCH.
- **3.9 — `nlm-add` 404 NOT_FOUND ×2 (ca KL 137-KL/TW)**: gốc = probe `notebook_get` trả NOT_FOUND THOÁNG QUA
  (flake backend ngay sau đợt gỡ 6 nguồn — eventual consistency; MCP cùng notebook OK cùng lúc, tối cùng
  ngày nlm-cli add OK «BUG 404 KHÔNG tái hiện») nhưng `_nlm_verdict` retry TỨC THÌ 1 nhịp (vẫn trong cửa sổ
  flake) rồi `_nlm_or_corpus` kết luận «NLM OFFLINE» rẽ deferred — SAI BẢN CHẤT: NOT_FOUND trên MỘT notebook
  = đích-không-nhìn-thấy (id sai/flake), KHÔNG phải NLM chết (auth alive); đường `--url` còn chết
  `NLM_OFFLINE_NO_DEFER_FOR_URL` khó hiểu ×2 (khớp hồ sơ: không journal nào trong cửa sổ lỗi). Vá 3 tầng:
  (1) `_nlm_not_found` PURE + retry backoff **5s/15s** riêng lớp NOT_FOUND (mirror F6 r192 «retry kể cả
  404»; transient khác giữ 1 nhịp tức thì — hợp đồng ADR-7 r121 nguyên vẹn; hook `_nlm_verdict_sleep` cho
  test); (2) route mới **`not_found`** fail-closed + banner playbook (kiểm `--notebook-id` UUID ĐẦY ĐỦ theo
  config topology / chờ ≥60s thử lại / lane thay thế MCP source_add + `tl register` nối sổ) — KHÔNG defer
  (defer ghi nlm_status=deferred trỏ notebook không nhìn thấy = poison registry nếu id sai); lệnh không xử
  route này rơi về đường cũ (gate live tự fail với lỗi thật); (3) `cmd_nlm_add` rc=2 `NOTEBOOK_NOT_FOUND`
  TRƯỚC mọi side-effect. ★Bẫy I11: 2 tên hàm + 1 hằng mới re-export vào tl.py (hàm rebase đọc globals tl).
- Test: 1262 → **1268** (+3 `r196_bridge_*`: thiếu-attest chặn profile/vbqppl + positive control forward;
  +3 `r196_nlm_*`: backoff 404 → sống, route not_found + banner, cmd rc=2 không side-effect); harness
  `_run_bridge114` thêm tham số `attested` (mặc định True — giữ nguyên hợp đồng ca r114).

# ★ v1.35.26 — r195 VÁ BUG CLAIM CREDS gas.py + 2 vá HERMETIC selftest (+2 test, 1262/1262) (2026-07-24 — BỔ SUNG HỒI TỐ ở phiên r196: r195 sót CHANGELOG; nguồn = commit `4680a8e`)

> Bug (đo 24-07, lô ATVSLĐ): `_fallback/gas.py` chụp WEBAPP/TOKEN từ env LÚC IMPORT (`_ensure_creds`
> không đọc lại os.environ) và DEFAULT_CONFIGS không biết `tra_luat_config.v2.json` ở cwd/gốc skill ⇒
> nlm-add (gas import trước, load_creds chạy sau) chết INGEST_CLAIM_FAILED «Thiếu TL_WEBAPP/TL_TOKEN» dù
> config v2 ngay cwd, kể cả `--config` tường minh; 13 lượt nlm-add giữa lô phải vòng bằng export env tay.
- Vá kép (TDD 2 ca chỉ-nó-chặn): `_ensure_creds` đọc lại env TẠI-LÚC-GỌI (env > globals cache > config
  file); `_default_configs()` candidates ĐỘNG cwd → gốc skill → scripts/ (v2 trước .json) — đồng bộ
  `_config_candidates` của profile_env (một cửa).
- Kèm 2 vá hermetic selftest họ r181 (`ingest_target` ghim `_manifest_entries`; r96 ghim
  `_resolve_overflow_shards`) + re-bless golden `workflow_audit` (nợ r194, links_checked 14→13).
- Test: 1260 → **1262**. SKILL.md chỉ đổi header ⇒ không cần re-import Capabilities.

# ★ v1.35.25 — r194 HẠ KÍCH THƯỚC BUNDLE 6,4MB → ~1,5MB (amend ADR-0007; +1 test, 1260/1260) (2026-07-24)

> User yêu cầu hạ size. Đo cấu phần: code 4MB (giữ) · 3 bản GAS 623KB · CHANGELOG 327KB · toàn bộ ZIP_STORED.
- **Nén DEFLATED mức 9 CỐ ĐỊNH** (amend ADR-0007, có mục riêng trong ADR): mọi phép so archive-hash của quy
  trình đều là build ×2 CÙNG MÔI TRƯỜNG (gate ×2, CI tự so 2 bản của nó, deploy so build↔pullback cùng
  artifact) — không có so-hash-cố-định xuyên máy nên DEFLATE không phá tính tất định ĐO ĐƯỢC; per-file
  sha256 trong manifest tính trên nội dung GIẢI NÉN, `release-verify` không đổi ngữ nghĩa. Verifier archive
  chấp nhận {STORED (gói cũ), DEFLATED}; check size-equality chỉ áp cho STORED.
- **Trim GAS cũ khỏi GÓI** (giữ trong repo/git — tiền lệ 2.21.2k v1.34.69): current nay 2.21.2n ⇒
  `Code.2.21.2l.gs` + `Code.2.21.2m.gs` (412KB) vào `_RELEASE_EXCLUDE_NAMES_ANYWHERE`; ca r130 cập nhật
  theo (2.21.2n phải CÒN trong gói).
- **CHANGELOG archive**: lịch sử 1.33.54→1.34.99 (246KB) chuyển NGUYÊN VĂN sang
  `references/changelog_archive/CHANGELOG-1.33.54-den-1.34.99.md` (dir vốn bị loại khỏi bundle); CHANGELOG
  còn ~84KB (v1.35.0+) + con trỏ.
- Test: 1259 → **1260** (+`r194_bundle_deflate_tat_dinh`: member DEFLATED ×2 cùng byte + metadata đóng băng
  + giải nén tròn). ★Bẫy phiên: chuỗi bash double-quote nuốt BACKTICK (command substitution) khi sinh text
  có `code` — dòng con trỏ CHANGELOG phải vá lại bằng Edit.

# ★ v1.35.24 — r193 HOTFIX SỰ CỐ TOKEN TRONG BUNDLE (SEC; +2 test, 1259/1259) (2026-07-23)

> **Sự cố:** `tra_luat_config.v2.json.bak_truoc_shard3_2026-07-23` (backup config do phiên shard-3 tạo ở
> ROOT cây skill, chứa **token webapp THẬT + webappUrl**) LỌT vào release-bundle → nằm trong zip LIVE trên
> Drive từ deploy r191/r192 cùng ngày (và có thể các bản deploy 23-07 trước đó, tuỳ thời điểm file sinh ra
> 20:21). Phát hiện bởi bước quét token trong SCRIPT SHIP của user — gate 9 bước KHÔNG có bước này.
> **Gốc:** luật exclude chỉ bắt suffix `.bak` CHÍNH XÁC + tên `tra_luat_config.v2.json` CHÍNH XÁC — đuôi
> backup BIẾN THỂ (`.bak_truoc_*`) lọt cả hai lưới; và pipeline KHÔNG có tầng quét nội dung.
- **Vá dữ liệu**: file backup DI CHUYỂN (không xoá) ra `D:\Quốc hội\_config_backups\` — ngoài cây đóng gói.
- **Vá code 2 tầng** (`release.py`): (a) `_release_should_include` — tên trong `_RELEASE_EXCLUDE_NAMES_ANYWHERE`
  nay chặn CẢ biến thể có hậu tố (`<tên>.bak_*`, `<tên>.old`…) + MỌI tên chứa `.bak`/`.tmp`; (b) cổng
  **`TOKEN_IN_BUNDLE`** ngay trong `cmd_release_bundle`: quét từng member (khuôn `tl_[A-Za-z0-9]{20,}`,
  helper PURE `_release_secret_findings` — finding CẮT token, không in trọn) → thấy là XOÁ zip tạm, rc=2,
  KHÔNG phát hành. Quét token giờ là tầng vệ CỦA SKILL, không phụ thuộc script ship ngoài.
- **Khắc phục hậu quả**: rebuild sạch + deploy ĐÈ bản lộ trên Drive cùng ngày. **KHUYẾN NGHỊ BẮT BUỘC:
  XOAY TOKEN webapp** (token đã nằm trong zip tải được trong nhiều giờ) + user re-import Capabilities
  (bản import v1.35.23 cũng chứa file token).
- Test: 1257 → **1259** (+2 `r193_*`: exclude biến thể chỉ-nó-chặn + quét token PURE/shape).

# ★ v1.35.23 — r192 ĐỢT HIỆU NĂNG/UX NLM F5–F9 + SỬA CHỮ SKILL.md (kế hoạch r191/r192; +10 test, 1257/1257) (2026-07-23)

> Đợt 2/2 của kế hoạch chốt qua grilling 23-07 (đợt 1 = r191/v1.35.22 cùng ngày). SKILL.md sửa NỘI DUNG
> một lượt (F1/F2/F3/F4/F5/F6/F7/F9 + khuôn lô chuẩn) ⇒ **RE-IMPORT Capabilities MỘT lần sau r192**.
> HOÃN ADR `ingest_pipeline` server-side (đã quyết); ĐO LẠI hiệu năng sau ~1 tuần theo bảng baseline 23-07.

- **F5 (đề xuất #1) — BA VAN NLM** (con số người thẩm tra duyệt): ① **van TRƯỚC LÔ** —
  `NLM_BATCH_LINKS_THRESHOLD` 2→**4**; lô >4 nguồn → KHÔNG auto-add API, nhánh BATCH_LINKS của
  `ingest-missing` nay GHI **BẢNG TAY** markdown (`hand_sheet` — `_nlm_links_md`: link bấm-được + notebook
  + hẹn reconcile) vào `.tl_state/nlm_bang_tay_<key>.md`; `nlm-links` +`--drive-ids` (bảng tay lô cụ thể,
  không đòi chưa-trên-NLM) +`--md-out`. ② **van KÍCH THƯỚC** — `_NLM_SIZE_VAN_CHARS=150k`: `ingest-local`
  đo text local lúc lập plan, >150k ký tự → TỰ chuyển `--nlm-no-wait` (plan ghi `nlm_size_van`; đo 23-07:
  343k >10′ client-timeout, <100k 30-90s). ③ **van RUNTIME** — `nlm_cli.source_add` mặc định chờ settle
  **120s** (trước 600s); CLI rc≠0 nhưng ĐÃ có Source ID ⇒ ok + `settle_timeout` (THÔI CHỜ, KHÔNG huỷ —
  nguồn đang index); `nlm-add` route sang lane deferred (F3), `ingest-local` bước link cuối ghi
  `nlm_status=deferred` + KHÔNG corpus (mirror khuôn ADD-TAY: reconcile nâng pushed → register corpus);
  rc=124 (hard-kill timeout+30) → note «ĐỪNG add lại mù — reconcile là đường vét».
- **F6 (đề xuất #8) — retry GAS chọn lọc**: `_gas_get_retry` +`_schedule` tường minh; `ingest_claim`
  (3 call-site) + `reg-query --live` đi lịch **5s/15s**; **GAS 404 chập chờn** ('HTTPError: 404' hạ tầng,
  KHÁC NOT_FOUND nghiệp vụ JSON) nay coi transient; KHÔNG auto-retry đường ghi. `CLAIMED_ELSEWHERE`
  (cả 3 nơi) in kèm `claim_ttl_hint` = giờ hết hạn muộn nhất (now+TTL 5′ — worst-case client-tính).
- **F7 (đề xuất #7) — preflight-lô auth NLM**: `NLM_COOKIE_BATCH_MAX_MIN=50`; `ingest-missing` sắp add API
  >1 nguồn mà cookie >50′ → CHẶN rc=2 `NLM_COOKIE_TOO_OLD_FOR_BATCH` «chạy nlm login trước lô» (trước chỉ
  WARN COOKIE_AGE_HIGH → chết giữa lô).
- **F8 (đề xuất #6) — `ingest_claim` đọc config**: helper một-cửa `_ingest_claim_get` — tự `load_creds`
  từ config như mọi bước khác (env TL_WEBAPP/TL_TOKEN vẫn ưu tiên — hết cảnh export tay/tlenv.sh) + gộp
  retry F6; cả 3 call-site claim đi qua cửa này.
- **F9 (đề xuất #9) — fetch hỏi-trước mặc định**: «phê duyệt nạp theo skill ≠ phê duyệt TỰ TẢI nguồn
  gated» — `fetch-route` MẶC ĐỊNH `mode=ask_first_links` (link bấm-được + link _HOP_NAP, KHÔNG fetch_plan);
  recipe tự tải CHỈ xuất với cờ tường minh **`--auto-download-approved`** (gõ SAU khi người dùng đồng ý
  trong phiên).
- **SKILL.md (một lượt — re-import 1 lần)**: F1 dedup lỏng-năm + `--replace-sohieu` (mục 18 CORPUS-FIRST);
  F2 đọc-tự-refresh; F4 PDF_IMAGE (10a); F9 khuôn 10b nổi hơn; khối **BA VAN NLM + KHUÔN LÔ CHUẨN MỚI**
  (lô ≥3 file → ingest song song 2–3 tiến trình + `--nlm-no-wait` + MỘT reconcile cuối lô) + F3/F6/F7.
- Test: **1247 → 1257** (+10 `r192_*`: van1 ×3, van2, van3 ×2, F6, F7, F8, F9); 3 ca cũ CẬP NHẬT THEO
  NGƯỠNG MỚI (r118/r122 lô 5>4; r72a fetch-route thêm cờ approved); parser_surface regen chủ đích
  (fetch-route + nlm-links). CONTEXT.md +2 từ vựng (ba van NLM, bảng tay).
- Ghi chú nhất quán: `ingest-local --nlm-no-wait` chủ động GIỮ khuôn S4 (pushed+corpus=true tại link,
  reconcile cuối lô là lưới — khuôn lô chuẩn dựa vào đây); `deferred` CHỈ dùng cho nlm-add --no-wait và
  ca settle-timeout van 3 (chưa xác minh settle, corpus chưa set).

# ★ v1.35.22 — r191 ĐỢT AN TOÀN DỮ LIỆU F1–F4 (kế hoạch r191/r192 chốt qua grilling 23-07; +11 test, 1247/1247) (2026-07-23)

> Nguồn: `SKILL_FIX_DE_XUAT_23-7.md` (đo thật phiên Cổng 1 + nạp 23-07 trên v1.35.21). Mỗi fix một ca
> TDD chỉ-nó-chặn (tiền lệ r181); các bẫy thật 23-07 nay bị chặn máy. KHÔNG fix nào đổi cách ĐỌC nội
> dung văn bản ⇒ không kích hoạt nghĩa vụ rà-lại Phần VI mục F. SKILL.md CHỈ bump header (không
> re-import); mọi sửa nội dung dồn r192.

- **F1 (đề xuất #4) — dedup số hiệu LIVE ngay tại DRY `ingest-local`**: bẫy 158/159 — dedup cache nguội
  che dòng có sẵn → DRY "đi lọt", apply tạo dòng + GDoc TRÙNG. Nay DRY (và apply) đo dedup trên registry
  LIVE (`_manifest_entries(refresh=True)`, +5–10s/DRY chấp nhận); khoá LỎNG-NĂM dùng bộ chuẩn hoá SẴN CÓ
  `_sohieu_loose` (so BẰNG-KHOÁ — '29-2025' không bắt oan '129-2025'); trùng dòng corpus-effective
  (`_entry_is_corpus_effective`, kể cả overflow) ⇒ CHẶN rc=2 `SOHIEU_ALREADY_IN_CORPUS`. Thay bản có
  chủ đích: cờ mới **`--replace-sohieu`** — plan in dòng cũ + `post_steps` chuỗi hạ bản sau nạp.
  LIVE không đọc được → fail-closed rc=2 (mirror S13); `--resume` bỏ qua (identity-gate đã giữ);
  `--skip-live-check` bỏ qua có chủ đích. Helper mới `_ingest_dedup_sohieu_live` (PURE).
- **F2 (đề xuất #5) — đường ĐỌC tự refresh khi manifest BẨN**: bẫy extract 164-2025 ngay sau hoán đổi
  canonical vẫn trả bản CŨ, phải `boot --refresh` tay. Nay `_invalidate_manifest_cache` (mọi lệnh GHI)
  để lại marker `manifest.dirty`; `_manifest_entries` thấy marker + có creds env (main() đã nạp cho mọi
  lệnh ngoài _CREDS_LAZY_CMDS) ⇒ ÉP refresh LIVE rồi xoá marker — vá MỘT chỗ phủ mọi lệnh resolve theo
  số hiệu (extract/locate/xref/doc-text). Đường đọc ADVISORY (discovery overflow trong `_ingest_target`)
  dùng `heal_dirty=False` — ngoài phạm vi resolve, không ép refresh. Phía ghi không cộng giá.
- **F3 (đề xuất #2) — `nlm-add --no-wait` tự reg_link với `deferred`**: bẫy 3 nguồn add no-wait có
  source_id trả về mà registry nlm=''/nb='-', phải register tay. Nay no-wait reg_link NGAY sid THẬT +
  `nlm_status='deferred'` (ngữ nghĩa MỞ RỘNG: «đã gửi NLM, chưa xác minh settle» — không claim có mặt
  vật lý nên không vi phạm VERIFY-THEN-LINK A-#1); chỉ link dòng đã tồn tại + chưa có pointer khác
  (stale-an-toàn, không row xương); corpus KHÔNG đụng. `nlm-reconcile` thêm nhóm **`settle_confirm`**
  (deferred + sid CÓ MẶT live đúng notebook) → `--apply` nâng `deferred→pushed` CHỈ cột nlm_status
  (corpus không auto-true); deferred VẮNG live giữ nguyên desync_real. Ca client-timeout-mất-source_id:
  reconcile vẫn là đường vét duy nhất. Helper mới `_nlm_no_wait_reg_link`. (Ca cũ
  `r117_nlm_add_no_wait_skips_reg_link` khoá hành vi bỏ-link → THAY bằng
  `r191_nlm_add_no_wait_links_deferred`.)
- **F4 (đề xuất #3) — cổng PDF-ảnh trong `ingest-local` lúc lập plan**: bẫy 4 PDF «ký số»
  datafiles.chinhphu.vn/hue.gov.vn đều PDF ẢNH (text layer 149 ký tự metadata chữ ký) suýt convert mù.
  Nay mọi nguồn .pdf đo text-layer local ngay lúc lập plan (`_pdf_text_layer_stats`: pdftotext + đếm
  trang qua form-feed, fallback đếm `/Type /Page`); **< 100 ký tự/trang ⇒ cờ `PDF_IMAGE`** → coi
  `source_quality=ocr` chưa verify → rơi vào ocr_gate r180 S1 SẴN CÓ (apply chặn corpus rc=2, đi tiếp
  đường OCR-verify) — không đẻ nhánh mới; chỉ override khi user để `auto` (đường `ingest-ocr` tường
  minh đi qua như cũ); không đo được (thiếu pdftotext) → cảnh báo, KHÔNG đoán. Plan DRY thêm khối
  `pdf_image` (verdict + chars_per_page). Helper mới `_pdf_image_verdict` (PURE) + hằng
  `_PDF_IMAGE_CHARS_PER_PAGE=100`.
- Test: **1236 → 1247** (+11: F1 ×4 `r191_dedup_sohieu_*`/`r191_ingest_local_sohieu_dup_dry_rc2`/
  `r191_ingest_local_replace_sohieu_di_tiep`, F2 ×2 `r191_manifest_dirty_*`, F3 ×2
  `r191_reconcile_settle_confirm_*` + 1 thay, F4 ×3 `r191_pdf_*`/`r191_ingest_local_pdf_*`).
  parser_surface regen CHỦ ĐÍCH (1 lệnh `ingest-local` — thêm `--replace-sohieu`). Bẫy selftest bắt
  được khi vá: mock `_manifest_entries` RÒ từ ca trước trong namespace tl → ca F2 gọi thẳng hàm module
  `tl_core.regio` + heal đòi TL_WEBAPP env (bare selftest trơ với marker — hermetic kép).

# ★ v1.35.21 — r190 DỨT ĐIỂM PHA D THEO P10 GỐC: via TELEMETRY + DOCS SYNC COMMANDS/RUNBOOK + CAP TỔNG REPACK (2026-07-23)

> Đối chiếu bản thi hành với P10_PROMPT gốc (user cung cấp sau) lộ 3 thiếu sót Pha D — vá nốt:
> +2 test r190 (1236/1236).

- **`via` propagation**: P10 đòi propagate CẢ `via` lẫn `degraded_reason` — r188 mới làm vế sau.
  Nay `profile-list --discover` + `profile-sync` LUÔN nổi `via` (profile_catalog/list_loop) khi scan
  có — biết đang đi bulk hay fallback ngay cả khi không degraded.
- **Docs sync đúng nghĩa (COMMANDS.md/RUNBOOK.md)**: profile-doctor +`--plan-marker-migration`
  (canary, tên đã quote r189); profile-ingest --resume ghi rõ identity gate r184 (`--journal`/
  `--drive-id`, name-only=DRY_REPAIR); ingest-zip sửa mô tả worker lỗi thời ("trần cứng 8" →
  ngân sách RAM D7 trần 4) + bundle hash r184 + in-process r187; RUNBOOK +B7 (resume định danh,
  marker v2 đã migrate, `TL_INGEST_MEMORY_BUDGET_MB`/`TL_DOCX_XML_MAX_MB`, đường bulk 2.21.2n).
- **SEC-01 cap TỔNG**: engine +`read_all_members_bounded` (trần member + trần TỔNG mặc định 4×) —
  đường repack the_thuc normalize đọc mọi member vào RAM, N member vừa-dưới-trần cộng lại hết
  nuốt RAM (`ZIP_TOTAL_BOUND_EXCEEDED`).
- Còn lại theo P10 (KHÔNG thuộc release này, đã ghi nhận): Pha A 5 ca bắt buộc chạy bù trên
  profile thử (kịch bản giao user); phần lõi WP7 (state machine + di trú 4 entrypoint +
  benchmark ≤+15%) → kế hoạch P11.

# ★ v1.35.20 — r189 QUOTE TÊN PROFILE TRONG ACTION PLAN MIGRATION (2026-07-23)

> Bug thực chiến migration 23-07: `marker_migration_plan[].action` in tên profile TRẦN — tên có dấu
> cách («Biểu mẫu DMVB», «Pháp lệnh NCC»…) dán nguyên văn vào shell bị vỡ tham số. Vá:
> `_migration_plan_finalize` bọc ngoặc kép (chạy được cả cmd lẫn bash). TDD r186_migration_plan_canary
> siết kỳ vọng sang bản quoted với tên có dấu cách. (Migration 15/15 profile đã xong bằng lệnh
> quote tay — vá này cho lần dùng sau.)

# ★ v1.35.19 — r188 SEC-01 BOUNDED-READ DOCX/XML + TELEMETRY degraded_reason + DOCS SYNC ADR (2026-07-23)

> MERGE phiên song song: master v1.35.16 = r186-extract (Opus) đánh TRÙNG số v1.35.16/r186 với
> r186-marker nhánh review — theo ADR-0001 số canonical thắng: 3 release nhánh này dồn lên
> v1.35.17/18/19 khi merge (test prefix r186_marker_*/r186_extract_* đã khác tên, giữ nguyên).

> Pha D (chốt) kế hoạch review p9 phần-còn-lại. +3 test r188 (1231/1231).

- **SEC-01 — chống zip-bomb DOCX/XML:** engine thêm `read_member_bounded(zf, member)` — đọc member
  STREAMING với TRẦN bytes giải nén (env `TL_DOCX_XML_MAX_MB`, mặc định 50, clamp [1,500]); vượt ⇒
  `ZIP_MEMBER_BOUND_EXCEEDED` (ValueError), member thiếu GIỮ ngữ nghĩa KeyError. Wire 9 điểm đọc:
  `_docx_unzip_text` (doc-text/extract), probe profile-ingest, `docx_markup.scan_file`,
  `normalize_document._docx_zip_text`, the_thuc (check/wrap-scan/landscape + normalize đọc
  TOÀN BỘ member khi repack). Các đường catch-all sẵn có fail-safe "" / scan(0) — không OOM,
  không traceback giữa pipeline.
- **Telemetry degraded_reason (WP5 dứt điểm):** `profile-list --discover` + `profile-sync` nay NỔI
  `degraded_reason` từ scan (SERVER_NO_PROFILE_CATALOG…) lên output JSON như doctor r185 —
  perf gate chỉ được coi xanh trên đường bulk, fallback phải tự khai.
- **Docs sync:** bổ sung 3 ADR bị tham chiếu từ r184 mà chưa có file trong cây:
  `0011-source-revision-tach-khoi-content-identity` (SourceRevision/claim-key/resume gate),
  `0012-marker-transaction-schema-v2` (state machine + v2 + rollout R1/R2 — R2 đã thi hành r186),
  `0013-zip-immutable-plan-bundle` (bundle hash, 1-extract r185, subprocess=0 r187).

# ★ v1.35.18 — r187 WP7 TRACER-BULLET: ENGINE INGEST CHUNG — SUBPROCESS=0 (ZIP) + STAGE SCHEDULER + HASH-ONCE (2026-07-23)

> Pha C kế hoạch review p9 phần-còn-lại (ADR-0004, ticket WP7/R3 ở r185). Module MỚI
> `tl_core/ingest_engine.py` — primitive engine ĐỘC LẬP stdlib (không bind, không import ngược
> tl_core): stage scheduler + hash-once run-scope + child runner in-process. +5 test r187 (1228).

- **Subprocess=0 cho ZIP apply:** `_zip_child_apply_one` chạy child APPLY **in-process** qua
  `run_child_inprocess` (một runner cho cả DRY lẫn apply — `_zip_child_plan_one` cũng ủy quyền);
  stdout/stderr route THEO THREAD (`_ThreadRouteProxy` refcount) — redirect_stdout process-global
  không thread-safe khi N child chạy trong ThreadPool. Giới hạn ghi nhận: (1) không còn timeout
  900s kiểu subprocess — child treo = run treo (GAS client tự timeout tầng dưới); (2) chunking/OCR
  vẫn `_run_child_tl` subprocess — NGOÀI scope ticket (ticket chỉ định child ingest-zip).
- **Stage scheduler (upload≤2, NLM≤2):** `stage_slot(stage)` BoundedSemaphore per-process; wire
  6 call-site: 2 upload (`profile-ingest`, `ingest-local`) + 4 `source_add` (profile-ingest,
  chunks, resume, ingest-local). Stage lạ = không giới hạn. Registry đã một lane từ r185/ING-05.
- **Hash nguồn ĐÚNG 1 lần/run (kể cả child plan):** `ingest_contract.sha256_file` ủy quyền
  `hash_file_once` — trong `run_scope()` (nest được) memo theo realpath; `_zip_plan_bundle` +
  `_zip_apply` mở scope trọn invocation → archive+member+child-plan hash 1 lượt (test đo:
  bundle = 1 compute, extract-verify memo-hit). Ghi nhận trade-off: re-hash archive giữa
  plan↔extract trong CÙNG run thành memo-hit — guard thẩm quyền là so sha256 TỪNG member lúc
  extract (GIỮ NGUYÊN, test ZIP_MEMBER_CHANGED_OR_CORRUPT còn đỏ đúng). Ngoài scope: hành vi cũ.
- Test r184/r185 zip apply chuyển patch funnel `_run_child_tl` → `_zip_child_apply_one` (đúng
  đường mới); +r187: cap concurrency đo bằng thread, hash-once trong/ngoài scope, routed-io 2
  thread song song bắt đúng stdout riêng, apply không đụng subprocess (fake raise nếu gọi).
- Golden regen CÓ CHỦ ĐÍCH (user duyệt): workflow_audit `py_size.files_scanned` 66→67 — đúng 1
  dòng, do file module MỚI `tl_core/ingest_engine.py` (không phải diff hành vi).

# ★ v1.35.17 — r186-marker R2 MARKER WRITER v2 + FAIL-CLOSED BODY + MIGRATION CANARY (2026-07-23, đổi số khi merge — v1.35.16 thuộc r186-extract canonical)

> Pha B kế hoạch review p9 phần-còn-lại (P10). Reader v1/v2 đã LIVE từ r184 ⇒ flip WRITER an toàn
> (client cũ 1 phiên bản vẫn đọc v1; marker mới phát v2). +5 test r186 (1223). Offline-only — mọi
> migration LIVE trên profile thật vẫn chờ user duyệt plan.

- **Writer v2 (ADR-0012 R2):** `_marker_body` phát `schema=tra_luat_profile.v2` + `fingerprint`
  (sha256 canonical-JSON, đóng dấu CUỐI sau mọi trường); tham số mới `meta_id` = fallback
  `metaFolderId` khi prof thiếu (marker luôn nằm trong chính `_meta` được ghi) — rename/set-meta
  truyền `mr.meta_folder_id`.
- **Fail-closed TRƯỚC upload:** `_marker_write` validate body (`_marker_validate`) trước mutation —
  v2 thiếu trường bắt buộc theo `manifestScope` / fingerprint lệch ⇒ `status=REJECTED`, 0 call Drive,
  journal ghi errors + repair (own-scope cần notebookId/registryDocId/manifestId). Hết cửa tạo
  marker hỏng rồi mới phát hiện qua doctor.
- **Migration canary:** `profile-doctor --plan-marker-migration` chốt plan qua
  `_migration_plan_finalize` (PURE) — sort tất định, phần tử ĐẦU `canary=true`, action chạy được
  per-profile `tl profile-backfill-markers --profile-name <p> --apply --force` (canary trước →
  verify doctor sạch → mới đại trà; --apply do user duyệt). Note doctor MARKER_SCHEMA_V1 cập nhật.
- Fixture selftest vá-trường-sau-`_marker_body` re-mint fingerprint (`_remint186`) — marker giả lập
  không thành "v2 fingerprint lệch" bị validate chặn oan; r86 defaults đổi kỳ vọng schema→v2;
  fixture minimal thêm `metaFolderId` (v2 bắt buộc).
# ★ v1.35.16 — r186 `tl extract` TRÊN GOOGLE DOC: ĐÓNG NỐT BẪY r183 BỎ LẠI (2026-07-23)

> r183 vá `doc-text` nhưng **`tl extract` vẫn dính NGUYÊN bẫy** — và đây mới là đường nguy hiểm hơn:
> extract **ghi thẳng vào cache chuẩn `extract_<id>.txt`**, tức NGUỒN NUÔI CORPUS/NLM ⇒ chữ đã bỏ chảy
> vào kho, rồi `doc-text` đọc lại chính cache đó.
>
> **Đo tươi 23-07-2026** (dự thảo BHXH 16/7, sau khi r183 đã LIVE): `tl extract <gdoc>` → **25.338 ký tự
> = BẢN THÔ**, đủ cả ba câu ĐÃ BỎ («tối đa là 12 tháng», «phải được chứng thực», «là cơ quan nhà nước»),
> **0 nhãn, 0 cảnh báo**. Gốc: `cmd_extract` đọc bằng transport `read`/webapp `exporttext` = export
> **text/plain**, và **không hề có cờ `--markup`**. **Sau vá, cùng lệnh: 21.128 ký tự, nguồn
> `gdoc-docx (markup strip)`, ba câu trên VẮNG MẶT.**
>
> **Vá — cùng khuôn r183, dùng CHUNG code (không chép lại logic):**
> · 4 helper tách ra `lookup_ops`: `_markup_warn` (một câu cảnh báo DUY NHẤT cho cả hai lệnh — lệch chữ
> giữa hai đường là mầm nhầm lẫn) + `_markup_cert_path/_write/_read` (sidecar chứng nhận).
> · `cmd_extract` +`--markup {strip,mark,raw}` (mặc định `strip`) và +`--markup-strict`.
> · (a) chế độ lọc ⇒ **export `.docx`** qua `_gdoc_docx_text` TRƯỚC, lọc bằng `docx_markup`.
> · (b) không lọc được (export .docx fail → rơi text/plain, kể cả nhánh resolve-lại canonical) ⇒
> **CẢNH BÁO `[markup] ⚠`**; `--markup-strict` ⇒ **rc=3 và KHÔNG ghi file** (ở extract điều này nặng hơn
> doc-text: thà thiếu file còn hơn bơm bản thô vào corpus).
> · (c) **bản `cache-build` consolidated cũng cảnh báo** — nó dựng bởi `normalize_document` mà
> `--markup-mode auto` cho DỰ THẢO ra bản **`mark`**, không ai chứng nhận được nó ở chế độ nào.
> · (d) **`mark`/`raw` KHÔNG ghi vào khoá cache chuẩn** nữa mà ra `extract_<id>.<mode>.txt` (nói rõ ở
> stderr) — trước đây `extract --markup mark` sẽ bơm thẳng ⟦BỎ:…⟧ vào khoá chuẩn.
> · (e) ghi khoá chuẩn ⇒ ghi kèm **sidecar chứng nhận** ⇒ `doc-text` đọc lại cache đó **hết cảnh báo**:
> vòng poison `extract → cache → doc-text → corpus` **đóng ở cả hai đầu**.
>
> **TDD 3 ca ĐỎ→XANH** (đo trước vá: 3/3 FAIL, nền 1218 không đổi): `r186_extract_gdoc_qua_docx_markup` ·
> `r186_extract_canh_bao_va_markup_strict` · `r186_extract_ghi_sidecar_dong_vong_poison` (ca (e) kiểm
> LIÊN THÔNG hai lệnh, không chỉ kiểm từng lệnh rời).
>
> ★ **BÀI HỌC PHẠM VI:** r183 ghi "còn mở: `tl extract`" rồi vẫn deploy — bẫy im lặng sống thêm một
> vòng trên chính đường nuôi corpus. Vá bug đọc-sai-văn-bản thì phải quét **MỌI reader của cùng nguồn**
> ngay trong một đợt (r182 quét 4 reader .docx; r183/r186 mới quét đủ 2 reader Google Doc).

# ★ v1.35.15 — r185 WP5-WP6 PERF: BULK PROFILE (GAS 2.21.2n) + ZIP 1-PASS + D7 RAM BUDGET + REGISTRY LANE (2026-07-23)

> Thi hành WP5-WP6 kế hoạch review p9 (D3/D6/D7). GAS **2.21.2n** = 2.21.2m ⊕ 2 endpoint CỘNG THÊM
> CHỈ ĐỌC: `profile_catalog` (snapshot Van_ban_thuong 1 call — items + _meta + NỘI DUNG mọi marker)
> và `drive_info_bulk` (metadata ≤200 fileId 1 call, giữ thứ tự input). Client try-first + fallback
> tương thích server cũ (`degraded_reason` — perf gate chỉ xanh trên đường bulk). +9 test r185 (1218).

- **WP5 — call budget D6 (đo bằng test đếm call trên fake GAS):**
  · `profile-list --discover` / `profile-sync`: scan = **1 call** `profile_catalog` (tổng ≤2 kể bootstrap),
    KHÔNG tăng theo 1/10/50 profile (trước: ~3×N call list/list/download-marker).
  · `profile-doctor` shallow 50 profile: **≤3 GAS** (bootstrap + catalog + info_bulk; marker đọc từ
    catalog, asset info từ bulk — 0 call `info`/`list`/`download` trong vòng lặp).
  · `profile-doctor --deep` 1 profile, 300 nguồn + 50 template: **≤4 GAS + 1 NLM** — `reg_get_bulk`
    lô 300 (0 `reg_get` lẻ; ghi nhận: bulk 1 row/sid — sid nhiều row chỉ thấy row cuối, ca hiếm);
    template probe từ info-bulk prefetch (0 download-để-kiểm-tồn-tại; location theo parents,
    'shared' resolve LƯỜI ≤1 lần/run).
  · `profile-sync --apply`: `_persist_profiles_config_bulk` — TOÀN BỘ diff ghi config NGUYÊN TỬ
    **1 lần** + 1 journal run (trước: N lần read-modify-write + N run).
- **WP6 — I/O/RAM (ING-03/ING-05/D7):**
  · ZIP apply: **1 extract + 1 lượt hash member/invocation** — bundle lập từ CHÍNH lần extract của
    apply; bỏ pre-pass recompute trùng lặp (drift do authorize bắt: `PLAN_HASH_MISMATCH` + note
    `PLAN_DRIFT_REPLAN_REQUIRED`). Trước r185: 2 extract + hash member ×3.
  · D7: `TL_INGEST_MEMORY_BUDGET_MB` (mặc định 256, clamp 64-4096); `workers_effective =
    min(requested, 4, floor(budget / (32MiB + 2,5×size_max)))` — hard cap 4 (trước cap 8 không đếm
    RAM); plan/apply CÔNG KHAI `resources{workers_requested/effective, peak_memory_estimate}`;
    không đủ 1 worker ⇒ `INSUFFICIENT_MEMORY_BUDGET` DỪNG TRƯỚC mutation.
  · ING-05: `_verified_reg_write`/`_journaled_reg_write`/`_verified_reg_upsert` đi **một lane RLock**
    trong process (8 thread không chồng nhau — test đo max-concurrency=1). GIỚI HẠN GHI NHẬN: chưa
    phủ child SUBPROCESS ingest-zip (row khác nhau + claim F-04 che; lane xuyên-process = WP7).
- **Còn lại WP6 (ticket WP7/R3):** subprocess child ingest-zip → in-process engine (subprocess=0,
  member hash đúng 1 lần kể cả child plan); stage scheduler upload≤2/NLM≤2; GWS streaming upload;
  SEC-01 bounded-read DOCX/XML.
- EXPECT_VERSION → **2.21.2n**; API_CONTRACT đóng dấu 2.21.2n + 2 action mới; GAS deploy qua clasp
  giữ URL NGAY SAU deploy skill (thứ tự an toàn: client-có-fallback lên trước server).

# ★ v1.35.14 — r184 REVIEW P0: GATE ARTIFACT + MARKER TRANSACTION + IDENTITY/RESUME + ZIP BUNDLE (2026-07-23)

> Bốn vá P0 từ review hiệu năng/đúng đắn Profile+ingest (kế hoạch grill-with-docs 23-07, workspace
> `C:\qh\p9_review_v13512_2026-07-23` — evidence register 11/12 CONFIRMED). Fork v1.35.12, merge 3-way
> lên r183 (giữ nguyên vá gdoc --markup); +23 test r184 (1209/1209).

- **REL-01 — gate xanh giả trên artifact**: v1.35.12 deploy-zip fail 4 selftest (r67/r125/r127/r128) vì
  SKILL.md trỏ `references/changelog_archive/` (release-exclude) — cây dev xanh (exists() trên đĩa),
  artifact đỏ. Vá: `_skill_links_findings` (PURE) đối chiếu link SKILL.md với PACKAGE-SET của manifest,
  wire fail-closed vào `_verify_release_manifest` (`SKILL_LINKS_NOT_IN_PACKAGE` + `skill_links` trong
  release-verify); gỡ con trỏ dev-only khỏi kernel (không nới auditor).
- **PRO-01 — marker false-success (ADR-0012)**: `_marker_write` thành state machine journaled
  upload → FULL readback (so TRỌN payload — hết so 3 trường) → enumerate (HẾT nuốt `except: pass`) →
  cleanup → PROVE-ONE (re-list chứng minh 0 marker dư) → commit; trả `status COMMITTED/PARTIAL/FAILED`
  + `phases` + repair action trong journal. 6 caller (rename/adopt/create/backfill/promote/set-meta)
  chuyển `verified&&cleanup_ok` → `ok` trọn chuỗi. Reader hiểu marker v1/v2 (`tra_luat_profile.v2`,
  bộ trường bắt buộc theo manifestScope, fingerprint) — R1 writer GIỮ v1; `_marker_mutation_guard`
  chung; `profile-doctor --plan-marker-migration` (DRY, migration ghi ở R2).
- **ING-02 — identity đội lốt + resume mù nguồn (ADR-0011/D4-D5)**: `identity_hash_for_drive_source`
  hết nhét sha256(drive_id) vào slot content_hash — retype thành `build_source_revision`
  (identity_strength revision/metadata) + `claim_key_for_source` (payload KHÔNG có content_hash;
  observed_at CỐ Ý ngoài khóa). ⚠ giá trị claim key ĐỔI — 2 host lệch version không khóa chéo trong
  cửa sổ rollout (TTL 5'). `profile-ingest` apply NAY CÓ JOURNAL (name/sha256/identity_hash/plan_hash/
  drive_id + run_end). Resume: name-only = DRY REPAIR (mode `DRY_REPAIR`, 0 mutation, 1 phiên bản
  chuyển tiếp); `--apply` đòi `--journal <run_id>` HOẶC `--drive-id` + fingerprint khớp registry
  (`_resume_identity_gate` PURE); journal legacy → `LEGACY_JOURNAL_REPLAN_REQUIRED`; lệch →
  `RESUME_IDENTITY_MISMATCH`. CLI profile-ingest/profile-file-add + `--journal`.
- **ING-01 — ZIP self-confirm (ADR-0013)**: DRY (`ingest-zip`/`profile-ingest-zip` có --cat) lập ĐỦ
  child plan IN-PROCESS (`_zip_child_plan_one`, 0 subprocess DRY) → `plan_hash` = fingerprint TOÀN
  bundle (archive+member+mọi child plan, `ingest_zip_bundle.v1`). Apply: authorize trên bundle hash;
  pre-pass tuần tự recompute từng child — khác bundle đã duyệt ⇒ `PLAN_DRIFT_REPLAN_REQUIRED`,
  0 mutation; `--confirm yes` cho child CHỈ với hash NẰM TRONG bundle user duyệt (hết tự-phê-duyệt);
  journal record `plan` bundle + intent per-member. ⚠ plan hash ZIP cũ (chỉ parent) hết hợp lệ — DRY
  lại lấy bundle hash. DRY vbqppl KHÔNG --cat giữ DRY phân loại (note_bundle).
- Bẫy merge: msys sed text-mode TƯỚC 
 → 3 file CRLF (tl.py/tl_selftest/command_registry) thành
  whole-file-diff giả 19k dòng; khôi phục CRLF trước merge. Kernel 48.190B > 47K warn sau merge —
  rút gọn dòng bảng CHANGELOG-sâu về 48.121B. Golden regen CÓ CHỦ ĐÍCH: parser_surface (cờ CLI mới),
  workflow_audit (links 15→14).

# ★ v1.35.13 — r183 NGUỒN GOOGLE DOC: `--markup` HẾT LÀ NO-OP IM LẶNG (2026-07-23)

> **BẪY IM LẶNG — nguy hiểm hơn bug thường vì công cụ báo THÀNH CÔNG.** r182 vá 3 reader `.docx`, nhưng
> **nhánh Google Doc của `_doc_text_any` không hề đụng `docx_markup`**: nó đi `_read_doc_text` (export
> **text/plain**) — đường này san phẳng mọi định dạng, GIỮ CHỮ mà MẤT gạch-bỏ. Cờ `--markup` bị bỏ qua
> HOÀN TOÀN, vẫn rc=0, không một dòng cảnh báo.
>
> **Đo tươi 23-07-2026** (Dự thảo Luật BHXH 16/7, `1ltPv6AwO72wglCpEitkT7tmu-GZ3zPEGhTObiKF8p4s`): qua
> `drive_id` **mọi chế độ = 25.339 ký tự** (≈ bản thô), **0 nhãn ⟦BỎ⟧**; từ `.docx` gốc: strip **21.131** /
> mark **25.503** (60 nhãn) / raw 25.032, `docx_markup.scan_file` = **63 khối `w:strike`** ⇒ **4.405 ký tự
> chữ ĐÃ BỎ bị đọc như quy phạm hiện hành**. Tác hại đã xảy ra: **6 phát hiện SAI** trong một đợt rà soát
> («tối đa là 12 tháng», «phải được chứng thực», «là cơ quan nhà nước», «trước liền kề tháng»), phải chạy
> trọn một đợt sửa hơn 60 chỗ trên 10 file.
>
> **Vá — đi CẢ HAI hướng, vì không hướng nào đủ một mình:**
> (a) **LẤY CHO ĐƯỢC MARKUP** — `_gdoc_docx_text`: Google Doc + chế độ lọc ⇒ **export `.docx`**
> (`_doc_text_fetch_binary(..., export_mime=…wordprocessingml.document)`; `alt=media` KHÔNG tải được
> Docs-native) rồi qua CHÍNH bộ lọc `docx_markup` như nhánh .docx — source mới `gdoc-docx`. Hướng này cứu
> được các bản Google Doc CÒN giữ dấu vết (gạch-bỏ thủ công/suggestion), nhưng KHÔNG cứu được bản đã mất
> markup lúc convert ⇒ phải có (b).
> (b) **KHÔNG LẤY ĐƯỢC THÌ NÓI THẲNG** — export .docx fail, hoặc bản convert không còn dấu vết nào
> (del=0/strike=0/ins=0), hoặc text lấy từ **cache không kèm chứng nhận đã-lọc** ⇒ **CẢNH BÁO stderr**
> `[markup] ⚠ …` + khai vào `meta`/JSON (`markup_filter_ran`, `markup_found`, `markup_warning`).
> `--markup raw` = đối chứng CÓ CHỦ ĐÍCH ⇒ không cảnh báo. **IM LẶNG LÀ HÀNH VI ĐÃ LOẠI BỎ.**
>
> **`--markup-strict`** (mới): có cảnh báo ⇒ **TỪ CHỐI in văn bản, rc=3** (`MARKUP_UNVERIFIED`). Dành cho
> pipeline thẩm tra: thà thiếu văn bản còn hơn có văn bản mà người đọc tưởng đã lọc.
>
> **SIDECAR chứng nhận cache** `extract_<id>.txt.markup.json` (`{v, filter_ran, found, source}`): cache cũ —
> nhất là do `tl extract` ghi từ export text/plain — KHÔNG có sidecar ⇒ lần đọc sau **cảnh báo + gợi ý
> `--refresh`** thay vì im lặng tái diễn đúng bẫy cũ. Thêm `_read_doc_text(..., use_cache=False)` cho
> mark/raw (cache là bản CHUẨN strip — trả nó cho chế độ khác cũng là một kiểu im lặng).
>
> **CẮT STDOUT PHẢI BÁO** — `--max` cắt làm hai chế độ về CÙNG số ký tự và trông y hệt nhau (đúng cái bẫy
> suýt làm chẩn sai hôm 23-07): nay in `⚠ ĐẦU RA BỊ CẮT: x/y ký tự … dùng --max 0 --out <file>`.
>
> **TDD 5 ca ĐỎ→XANH** (đo trước vá: 5/5 FAIL, không ca nào khác đổi): `r183_gdoc_strip_qua_docx_export` ·
> `r183_gdoc_mat_markup_canh_bao` · `r183_markup_strict_tu_choi_rc3` · `r183_canh_bao_cat_stdout` ·
> `r183_cache_cu_khong_chung_nhan_canh_bao`. Selftest **1186/1186**.
>
> ★ **ĐO ĐƯỢC KHI DỰNG CA:** hai test double cũ của `r121` (`_read_doc_text` lambda không nhận `**kw`) làm
> ca ĐỎ vì `TypeError` bị `except Exception` của `_doc_text_any` NUỐT — đúng lớp lỗi âm-tính-giả mà chính
> r183 đang vá; đã nới double.
>
> ★ **DOCTRINE:** bản TRONG KHO không đương nhiên là bản dùng được làm căn cứ; với tài liệu có markup,
> **file `.docx` GỐC mới là nguồn chuẩn**. Công cụ không chứng minh được đã lọc thì PHẢI NÓI — không được
> để người dùng tự suy ra từ rc=0.
>
> **Còn mở:** `tl extract` trên Google Doc vẫn đọc bằng export text/plain (chưa có cờ `--markup`) — nay
> cache do nó ghi bị doc-text cảnh báo là CHƯA CHỨNG NHẬN; để vòng sau.

# ★ v1.35.12 — r182 ĐỌC ĐÚNG .docx CÓ MARKUP SỬA ĐỔI (cả 3 reader sản xuất đọc SAI dự thảo) (2026-07-22)

> Lỗi ĐÚNG-SAI về NỘI DUNG PHÁP LUẬT (không phải lỗi hình thức): mọi đường đọc .docx đều lấy chữ ĐÃ BỎ làm
> quy phạm CÒN HIỆU LỰC. **Đo TƯƠI qua ĐÚNG hàm sản xuất TRƯỚC khi vá — 20 sai / 4 đường đọc:** nhánh
> python-docx của `normalize_document._docx_to_text` GIỮ chữ `w:strike` và MẤT chữ `w:ins` (python-docx bỏ
> run không phải con TRỰC TIẾP của `w:p`); hai nhánh strip-tag — `lookup_ops._docx_unzip_text`
> (`tl doc-text`; doc-compare/dedup/nlm qua `_doc_text_any`) và `ingest_ops._profile_read_probe_text` (cổng
> nạp, DRY phân loại) — giữ CẢ `w:delText`. Bảng (`c.text`) CÙNG LỖI.
>
> ★ **TỰ KIỂM BÁC BỎ GIẢ ĐỊNH BAN ĐẦU:** `tl doc-text`/`tl extract` **KHÔNG** đi qua `_docx_to_text` ⇒ vá mỗi
> `normalize_document` là CHƯA chạm đường tra cứu (P6 vẫn sai). `_docx_to_text` chỉ phục vụ đường NẠP;
> `tl extract` đọc GDoc bằng export GAS. Bài học: xác minh call-graph trước khi tin phạm vi một bug.
>
> **Vá:** module dùng chung `scripts/docx_markup.py` (zero-dep) — bỏ `w:del`/`w:moveFrom`/`w:delText`, BÓC VỎ
> `w:ins`/`w:moveTo`, bỏ run `w:strike`/`w:dstrike` (tôn trọng `w:val="false"` = đè TẮT), quét
> `w:rPrChange`/`w:pPrChange` TRƯỚC khi dò strike (rPrChange lưu ĐỊNH DẠNG CŨ ⇒ dễ tưởng run hiện tại bị gạch).
> Cả 4 đường đọc + CẢ BẢNG dùng CHUNG bộ lọc; phát hiện markup → CẢNH BÁO stderr. Chế độ: `strip` (mặc định —
> bản chuẩn vào cache) · `mark` ⟦BỎ:…⟧ · `raw` (đối chứng). CLI: `tl doc-text --markup`,
> `normalize_document --markup-mode auto` (auto = **mark cho DỰ THẢO / strip cho VBQPPL đã ban hành**).
> mark/raw KHÔNG đọc/ghi cache `extract_<id>.txt` (giữ corpus sạch nhãn).
>
> ★ **ĐO ĐƯỢC KHI DỰNG CA TDD (giả thuyết ban đầu SAI):** bản `mark` KHÔNG an toàn cho parser — `ART_SPLIT`
> đòi CHỮ HOA ngay sau "Điều N." nên nhãn `⟦` CHẶN Điều THẬT, còn `:` trong `⟦BỎ:` lại THOẢ lookbehind
> `[\s.;:]` nên tiêu đề ĐÃ GẠCH BỎ đẻ ra "Điều ma" (đo: `split_articles(mark)` = `[5]`, MẤT `[1]`).
> Không nhãn nào chữa được cả hai chiều ⇒ **CẤU TRÚC LUÔN phân tích trên bản `strip`**; mark/raw chỉ đi vào
> `text_markup` (bản XEM). Nhãn phải là phần tử `w:t` THẬT — python-docx CHỈ nối `w:t`, chèn text trần thì
> nhánh lib nuốt nhãn còn nhánh strip-tag giữ ⇒ hai đường đọc lệch nhau.
>
> **BÁN KÍNH HỒI QUY = 0 (đo trên kho THẬT):** quét 210 .docx — **200 file sạch markup cho text `strip` ≡ `raw`
> (bytes y hệt) 200/200**; 10 file có markup đều là DỰ THẢO (`strike`, cao nhất 102 và 63). Đối chứng dự thảo
> 16/7/2026: `"là cơ quan nhà nước"` 1→0, `"12 tháng"` 1→0, `"chứng thực"` 3→0 — **đúng nguồn gốc 3 "phát hiện"
> sai của GĐ5–GĐ7** (4.098 ký tự đã gạch bỏ từng bị đọc như quy phạm sống).
>
> **Gate:** selftest **1181/1181** (+9 ca r182; nền 1172 GIỮ NGUYÊN) + gen_instructions 38/38; golden regen
> ĐÚNG 2 khoá có chủ đích (`doc-text` parser surface do thêm `--markup`; `workflow_audit.files_scanned`
> 65→66 do thêm 1 module). **Đối chứng bằng revert 7 chốt:** mỗi chốt có ca VÂN-TAY RIÊNG
> (N1→lib · N2→zip · N3→doc-text · N4→cổng nạp · N5→chỉ điều-ma · N6→chỉ cache · N7→nhãn), "FAIL khác = 0" mọi lượt.
>
> **KERNEL:** thêm bất biến **19** — (a) rà dự thảo PHẢI ĐỌC KÈM TỜ TRÌNH (tách MỤC TIÊU CHÍNH SÁCH khỏi CÂU
> CHỮ QUY PHẠM; phần lớn "vênh" là KHÁC TẦNG) · (b) markup = ĐÃ BỎ / MỚI THÊM, không kết luận trên bản chưa
> lọc · (c) MỌI KHẲNG ĐỊNH PHÁP LÝ verify NGUYÊN VĂN qua `get_legal_article`/`tl extract`, **CẤM nêu theo trí
> nhớ**. Bù byte theo khuôn kernel-diet: khối ADR-0003 trích NGUYÊN VĂN sang `references/KERNEL_APPENDIX.md`
> §D ⇒ SKILL.md 48.115 → **48.061 B** (dưới trần 47K, biên 67 B).

# ★ v1.35.11 — r181 HERMETIC SELFTEST+GOLDEN + CHECKPOINT MKDIR (nền+gate xanh dưới defaultProfile «Luật BHXH») (2026-07-22)

> Nối r180: cổng khởi động phát hiện selftest nền LỆCH **1167/1169** trên ĐÚNG commit `e45571a` (cây sạch,
> HEAD/VERSION khớp) → dừng đúng luật, chẩn gốc READ-ONLY. Hai ca resume/checkpoint (`r20`/`r30`) đỏ do
> **selftest KHÔNG hermetic w.r.t. defaultProfile máy**: S10 lật default `vbqppl`→«Luật BHXH» (config gitignored
> nên cây git vẫn sạch) + một ca sớm gọi `apply_profile_offline(config THẬT)` **leak** `TL_PROFILE=«Luật BHXH»`
> tới r20/r30 (cleanup env ở sau). Đo TƯƠI bằng probe-file: ckpt rơi vào `…\Luật BHXH\corpus_audit_ckpt_all.json`
> — mà `_ckpt_save` **NUỐT OSError** khi thư mục cha thiếu → checkpoint resume ghi HỤT im lặng → không hội tụ.
> Vá cả 2 (user duyệt P1); **gate bước 5/6 (golden-test, determinism-audit) cũng đỏ TIỀN TỒN cùng gốc** (kiểm
> `git stash` về r180: rc=2 y hệt; `TL_PROFILE=vbqppl golden-test` → xanh 100% ⇒ goldens ĐÚNG, chỉ non-hermetic)
> → thêm **Fix3**. Mỗi vá 1 ca **CHỈ-NÓ-CHẶN** (đối chứng revert đủ 3). selftest **1172/1172** (+3 ca r181; nền
> 1169 GIỮ NGUYÊN) + gen_instructions **38/38** + gate 9 bước TOÀN XANH.

- **Fix1 (production) — `_ckpt_save` mkdir thư mục cha** (`hygiene.py` `cmd_corpus_audit`): thêm
  `_ckpt.parent.mkdir(parents=True, exist_ok=True)` trước `write_text`. Bịt lỗ THẬT: profile mới toanh / phiên
  đầu, cache-subdir chưa tồn tại → `FileNotFoundError` bị `except OSError: pass` nuốt → mất tiến độ resume im
  lặng (nghịch ý checkpoint chống-hỏng-dữ-liệu). Ca `r181_ckpt_save_mkdirs_missing_parent` (ép
  `_profile_cache_dir()`→subdir chưa có; đo checkpoint GHI ĐƯỢC + resume 2 lượt hội tụ + tự dọn). Cô lập:
  revert mkdir → **CHỈ** ca này đỏ (1170/1171), r20/r30 vẫn xanh (Fix2 pin cứu về base cache).
- **Fix2 (harness) — `selftest()` ghim `TL_PROFILE=DEFAULT_PROFILE`** (`tl.py` `_selftest_pin_profile`/
  `_selftest_restore_profile` + wrap bare selftest, restore ở finally ngoài): hermetic w.r.t. defaultProfile
  máy, miễn nhiễm mọi leak env giữa suite (đúng doctrine "bare selftest must be hermetic"). Ca
  `r181_selftest_pin_profile_hermetic` (env non-default giả lập → pin đưa `active==DEFAULT` &
  `_profile_cache_dir()==CACHE`, `restore` trả nguyên env). Cô lập: neuter thân pin → **CHỈ** ca này đỏ
  (1170/1171), r20/r30 vẫn xanh (Fix1 mkdir cứu). Call-site xác nhận bởi nền-xanh-dưới-«Luật BHXH».
- **Fix3 (gate) — golden-test tự-hermetic** (`workflow.py` `_golden_env`): LUÔN tiêm `TL_PROFILE=DEFAULT_PROFILE`
  vào env mỗi subprocess golden (goldens là artifact NỀN; subprocess kế thừa defaultProfile máy — nếu ≠ nền thì
  `reg-query` trả `base_also` / corpus·đếm theo overlay → golden ĐỎ GIẢ; determinism-audit đỏ ăn theo vì gọi
  `_golden_test` in-process). Case tự khai `TL_PROFILE` thì tôn trọng (setdefault); đường `--write` nhờ đó regen
  dưới ĐÚNG nền. Ca `r181_golden_env_pins_base_profile` (máy-độc-lập). Cô lập: revert `_golden_env` → **CHỈ** ca
  này đỏ (1171/1172). 6 ca golden đỏ (`hygiene_*` + `doc_text_cache_fixture`) là TIỀN TỒN r180, r181 thêm 0 đỏ.
- **Doctrine:** nền/gate có thể LỆCH mà cây git SẠCH khi trạng thái sống (defaultProfile) ở config **gitignored**
  → cổng khởi động PHẢI đo selftest **VÀ gate** TƯƠI, không tin "cây sạch = xanh". Mọi lệnh hermetic-CI (selftest,
  golden-test/determinism) phải trung hoà active-profile về DEFAULT (thêm cache-dir với selftest).

# ★ v1.35.10 — r180 THĂNG FAIL 8 Ô TT-DT (ADR-0009 Đ3) + 7 FIX GĐ2/CỔNG-1 (2026-07-22)

> Phiên grill-with-docs 22-07: xử lý log vận hành GĐ2+Cổng-1 «Luật BHXH» (S1-S10/D1-D7 — mỗi quyết
> định user duyệt từng câu) + việc mở #1 của bàn giao: thăng FAIL từng ô lớp TT-DT theo chuẩn
> zero-oan tuyệt đối. selftest **1169/1169** (+18 ca r180; nền 1151 GIỮ NGUYÊN).
> Hồ sơ đo tươi + đối chiếu tay: `D:\Quốc hội\thang-o-2026-07-22\` (ket_luan_doi_chieu.md).

- **THĂNG FAIL 8 (hệ·ô·trục) — user duyệt từng ô 22-07** (the_thuc.py `_THANG_FAIL` inline — bẫy I11):
  `hanh_chinh·noi_nhan_ds·co` · `hanh_chinh·noi_nhan_tu·co` · `hanh_chinh·ten_loai·co` ·
  `hanh_chinh·dia_danh·kieu` · `dang·the_loai·co` · `dang·dia_danh·co` · `dang·so_ky_hieu·co` ·
  `dang·dia_danh·kieu`. Đo TƯƠI production v1.35.9 trên 159 file (129 corpus ngâm + 30 mới), lớp A
  191 WARN đối chiếu tay TỪNG finding; chỉ thăng vi phạm ĐO ĐƯỢC (nhánh «cỡ không khai báo» giữ WARN
  — guard `chua_do`); B3/tin-cậy-thấp giữ INFO vĩnh viễn (Đ1); trục chưa duyệt giữ WARN. Ô CÓ oan ở
  lại WARN kèm hồ sơ: `dieu·kieu` (neo ăn câu trích dẫn Điều trong báo cáo 9/9), `de_muc_than` (ăn
  khối ký/đuôi tiêu đề), mọi ô canh both≈left, cụm dàn-trang-bằng-indent (TB_20), gach=đường-kẻ
  (tieu_de Đảng/tiêu ngữ), thut lệch <3mm (thut='0' không dung sai). Khoá 10 ca selftest ba chiều
  (FAIL thuận · WARN nghịch · INFO bất khả xâm); fixture r136/r143 nắn ĐÚNG thể thức (địa danh
  nghiêng, «Nơi nhận:» 12pt — sửa fixture, KHÔNG nới bộ kiểm) + biến thể `_VN136_NOSZ`.
- **S1 — cổng OCR đường corpus NỀN** (`_ingest_local_ocr_gate` PURE + nối `cmd_ingest_local`):
  `--source-quality ocr` ∧ ¬`--ocr-verified` ⇒ ép đường no-nlm-add, registry corpus=false + note
  `OCR_UNVERIFIED_NOT_CORPUS`, rc=2 kèm next_steps ocr-verify/ingest-ocr; DRY plan mang `ocr_gate`.
  (Hố 21-07: Hiệp định VN–Hàn scan vẫn corpus=true — ingest-local coi cặp cờ là trang trí trong khi
  profile-ingest gate cứng; nay MỘT cổng MỘT luật.)
- **S2 — `source-update-corpus false --as-ref` (HẠ REF một bước):** corpus=false + row_kind=ref,
  GIỮ nguồn NLM + nlm_status họ sống (ca ILO C102 hết 3 bước xoá-rồi-add-lại); shared_source_id
  KHÔNG chặn nhánh này (không đụng NLM); journal ghi before row_kind thật. CONTEXT.md +«Hạ ref».
- **S3 — extract resolve --sohieu ĐỌC CỘNG NỀN dưới --profile** (`_extract_resolve_entries` mirror
  base-also reg-query, hit nền scope='vbqppl'). Chẩn đoán log SAI HƯỚNG nhưng bệnh thật: không phải
  thiếu pattern VPQH mà là thiếu base-also (đo 22-07: `52-2025-VPQH` resolve ngon KHÔNG profile,
  fail DƯỚI profile). Ghi nhận data: sohieu Hiến pháp `52-2025-VPQH` thiếu token VBHN — sổ hygiene.
- **S4 — DRY .doc cũ hết phán chắc** (`_profile_dry_gate_soften` PURE): NO_TEXT_FOR_VERIFY trên
  .doc binary (không --text-file) → info `OLD_DOC_VERIFY_AT_APPLY` + `verify_at_apply=true` +
  plan registry.corpus=null (quyết ở apply sau convert server-side — hố dry/apply lệch 21-07).
- **S5 — source-update-corpus NOT_FOUND tự refresh MỘT lần** trước khi kết luận (hố: gọi ngay sau
  apply dính cache cũ, phải --refresh tay).
- **S7 — reg-query positional = lọc mờ theo tên** (alias --name; trước rc=2 unrecognized).
- **S8 — nlm-add --row-kind** (`_nlm_link_row_kind` PURE): cờ tường minh thắng suy-topology F-06,
  kind bảo hộ giữ luật cũ khi không cờ — hết phải register --row-kind riêng sau nlm-add.
- **Vận hành trong phiên (data, journaled):** D1 xoá dòng own mồ côi profile «Luật BHXH» của Luật
  DN VBHN_67 (hai-scope-hai-ảnh đóng; dòng nền `67-2025-VBHN-VPQH` canonical khoẻ — căn cứ Đ122/88
  thông) · D4 đóng bằng đo: 382/BC-BTC là RIA định mức chi NSNN 2027-2030, KHÔNG phải RIA BHXH
  (giữ cat; RIA BHXH vào sổ chờ-nạp) · D3 sổ chờ-nạp 6 tài liệu · D2/D5/D6/D7 + tồn dư mới → phiên
  hygiene riêng · S6 xref deferred (cần đo tái hiện riêng) · S9 không làm (cookie phía Google).
- Golden regen CHỦ ĐÍCH: `parser_surface.json` (+3 bề mặt cờ mới: --as-ref · reg-query positional ·
  nlm-add --row-kind). SKILL.md: header + §184 cổng OCR máy-chặn + lối hạ ref → **re-import Capabilities**.

# ★ v1.35.9 — r179 BẢY FIX LOG PHIÊN VẬN HÀNH + ADR-0010 TỪ VỰNG NLM (2026-07-21)

> Thi công `BAN_GIAO_r179_2026-07-21.md` — 7 quyết định đã grill 21-07, mỗi cái đo trước phán sau.
> selftest **1151/1151** (+20 ca r179; 1131 cũ GIỮ NGUYÊN — added-fire 936/1118 là hành vi đúng).
> ADR-0010 mới: `docs/adr/0010-tu-vung-nlm-status-dong-va-tach-claim-due.md`.

- **T1 — `register --nlm-status` TỪ VỰNG ĐÓNG (ADR-0010 Q1):** `_nlm_status_write_ok` (classify.py)
  = họ `pushed*/synced*/active/removed_<lý do>` + rỗng (route clear); giá trị lạ (added/live/ready/
  typo) → `NLM_STATUS_UNKNOWN` **rc=2 TRƯỚC mọi round-trip** (test khoá: fake-gas 0 call). Cửa ĐỌC
  `_nlm_status_known` GIỮ NGUYÊN khoan dung (trash*/deleted/removed-trần) — bất đối xứng CÓ CHỦ ĐÍCH,
  selftest khoá cả hai chiều.
- **T2 — lệnh MỚI `backfill-nlm-status --dry/--apply`:** nắn MỘT LẦN added→pushed, live→active
  (map tất định, case-insens; map INLINE trong hàm — bẫy I11 hằng module-level không sống sót
  bind-REBASE, dính thật khi smoke). Per-row `reg_upsert` journaled + before → undo được; giá trị
  ngoài map KHÔNG đụng (stray `OUTSIDE_MAP`/`NO_DRIVE_ID`). Đo DRY trên «Luật BHXH»: **25 map
  (23 added + 2 live), 1 stray `ready`**. ⚠ CHẠY SAU DEPLOY (xem mục vận hành cuối).
- **T3 — guard `sua_doi` TỰ TRỎ chặn cứng:** `_sua_doi_self_ref` (PURE) — token trong sua_doi
  (tách `;`/`,`) sau `norm_sohieu` trùng số hiệu CHÍNH dòng (từ `--sohieu` cùng lệnh, fallback
  manifest theo drive_id) → `SUA_DOI_SELF_REFERENCE` rc=2, **KHÔNG có --force** (không tồn tại ca
  hợp lệ). Bắt biến thể `142/2025/QH15 ≡ 142-2025-QH15`. Xác minh bề mặt: cờ `--sua-doi` SINH ĐỘNG
  từ dest ở cli.py:437-439 (literal không có trong repo — log ghi đúng, grep sai chỗ).
- **T4 — draft theo BẬC BẰNG CHỨNG (mọi hệ) + vá title BOM/letterhead.** Đo 6 docx thật lô BNV
  16/7 trước khi sửa: sohieu classify nhiễm UUID tên file (`7_2026_e7c88c81`), issue_date nhiễm
  trích dẫn thân («Căn cứ NĐ… 2018») ⇒ veto official KHÔNG dùng được sohieu/issue_date thô.
  - Bậc: banner «DỰ THẢO» dòng riêng (`_draft_banner_line`, chịu artifact toạ độ docx
    `-44005514605Dự thảo…`) HOẶC Số-line KHUYẾT («Số:  /TTr-BNV», `_sohieu_line_khuyet`) ⇒ draft
    MẠNH; Số-line letterhead CÓ SỐ trong TEXT (`_sohieu_from_title_zone(strict_letterhead=True)` —
    KHÔNG best-fallback/filename) **AND** dateline đủ số (`_issue_dateline_complete`) ⇒ official
    PHỦ QUYẾT marker yếu («lấy ý kiến»/«góp ý»/«dự thảo» trong trích yếu); không bằng chứng ⇒ giữ
    hành vi cũ. Nghiệm thu: QĐ-TW ký + «lấy ý kiến» → draft:false (hết oan, ca log vận hành);
    6/6 file thật lô BNV GIỮ draft:true đúng (3 khuyết/banner + 3 weak-không-bằng-chứng).
  - Title (`_profile_title_from_header`): bỏ BOM đầu file (đường .txt/.html utf-8 — quốc hiệu hết
    thành title); bỏ dòng LETTERHEAD tên cơ quan (IN HOA ≤60, pattern agency BOUNDED — `bo\s+(?!luat)`
    né «BỘ LUẬT», không nhận `so|vu|ban` trần nên «SO SÁNH…»/«BAN HÀNH…» vẫn là title) + strip
    artifact toạ độ docx («598805267335BỘ NỘI VỤ»).
- **T5 — scope MỘT TỪ VỰNG ở 3 lệnh đọc (CONTEXT «Scope (dòng kết quả)»):** khoá `_scope` riêng
  của reg-query BỎ HẲN — dòng nền base-also mang `scope:'vbqppl'` + cờ `BASE_SCOPE_HIT` per-row
  Y HỆT source-map/exists ở CẢ reg-query (JSON rows + text `[nền]`) LẪN locate (text `[nền]` từng
  dòng + JSON). Selftest r6 cập nhật khoá `_scope` tuyệt chủng.
- **T6 — `vbhn-check --sohieu`:** alias MỎNG của positional (định tuyến y hệt: số hiệu → goc,
  trích yếu → subject; positional thắng nếu cả hai) — tay quen `--sohieu` hết usage-error.
- **T7 — `locate --json` JSON THẬT (`locate.v1`):** envelope cả 3 nhánh (offline_index /
  offline_manifest / webapp_find): `query/mode/count/shown/truncated/low_confidence/rows[]`
  (+`profile_hits/base_hits`, warnings token máy-đọc `OFFLINE_CACHE_*`); stdout sạch (narration
  tắt); row nền scope+BASE_SCOPE_HIT (T5). rc giữ nguyên ngữ nghĩa cũ.
- **T8 — tách nhãn claim/due (ADR-0010 Q2), sự cố «51/40/51» đóng bằng SỐ ĐO:** đo lại tươi trên
  «Luật BHXH»: vật lý 51 = claim 40 (24 own + 16 ref) + **11 dòng `removed_from_drive` nguồn CÒN
  SỐNG** (lô PDF dự thảo 16.6 — file Drive xoá, nguồn NLM giữ); reconcile desync_real=0; 10 dòng
  blank đều corpus=false (không thuộc diện). → Helper chung `_nlm_due_rows` (corpus∪ref − removed_*,
  blank-nb fold về base); **slot-audit**: khoá `gap` trần BỎ → `desync_estimate` (đếm) +
  `nlm_due_rows`/`coverage_gap`(+sample) + `removed_family_still_pointing` + `note_removed_live`
  khi giải thích TRỌN (hết lời khuyên backfill sai) + `labels_note`; **nlm-reconcile**: +`nlm_due_rows`/
  `coverage_gap` per-source (có live-set) + `removed_family_still_live`(+sample 11 file đúng tên) +
  `labels_note` (chỉ khi KHÔNG --from-plan — không có live ground-truth thì không phán). Hai lệnh
  nay kể CÙNG một câu chuyện với tên tường minh; «Hai phép đo ≠ nhau, lệch số KHÔNG phải mâu thuẫn».
- **Bề mặt/gate:** GENERATED_SPECS + COMMAND_META +`backfill-nlm-status` (medium/registry/dry-run,
  module nlm_ops); _STUB_MAP +7 tên (`_nlm_status_write_ok`/`_sua_doi_self_ref`/`_draft_banner_line`/
  `_sohieu_line_khuyet`/`_issue_dateline_complete`/`_nlm_due_rows`/`cmd_backfill_nlm_status`+
  `_backfill_nlm_status_candidates`); parser_surface regen CHỦ ĐÍCH (locate --json · vbhn-check
  --sohieu · lệnh mới). Selftest +20 ca `r179_t*` — kỷ luật đột biến r178: mỗi chốt có ca CHỈ nó
  chặn (vd `r179_t4_official_veto_requires_both_evidences` giết mutant nới strict→best-fallback;
  `r179_t1_register_gate_rc2_before_server` chứng minh gate đứng trước server bằng fake-gas 0 call).
- **Vận hành SAU deploy (một lần):** `tl --profile "Luật BHXH" backfill-nlm-status` DRY → `--apply`
  (25 dòng; stray `ready` trên VBHN_14 ATVSLĐ sửa tay sau khi hiểu nguồn gốc) — cờ
  `NLM_STATUS_MISMATCH` trên dòng added sẽ tự hết. Cân nhắc chạy thêm trên scope nền vbqppl.
- **CONTEXT.md** +5 mục từ vựng (Draft (ingest) · nlm_status · Scope (dòng kết quả) · nlm_claim ·
  nlm_due) — sản phẩm phiên grill 21-07, commit CÙNG release này.

# ★ v1.35.8 — r178 TIÊU CHÍ MÁY NHẬN DIỆN CÔNG VĂN HỆ ĐẢNG + ô mới `kinh_gui` (2026-07-21)

> Đóng việc-mở treo từ r175: biến thể `dang.cong_van` ĐÃ CÓ Ô từ lâu nhưng **chưa bao giờ kích
> hoạt được** — code chỉ bật cong_van cho `hanh_chinh` qua regex «V/v», mà HD05 không dùng «V/v».
> Đối soát nguyên văn HD05 27/5/2026 (GDoc `1Lko21mO…`). selftest **1131/1131** + gen_instructions 38/38.

- **Tiêu chí máy (2 vế, neo vào Ô):** ô `so_ky_hieu` khớp «Số N-CV/…» **∧** KHÔNG có ô `the_loai`.
  - Vế 1 — HD05 **3.1.2.b ví dụ 3**: *«Công văn của ban tuyên giáo và dân vận tỉnh uỷ — Số
    138-CV/BTGDVTU»*; bảng thống nhất viết tắt khi TRÙNG chữ cái đầu (**3.1.2.a**: QĐ, CT, CTr,
    TT, TTr) **không chứa CV** ⇒ không thể loại nào khác chiếm ký hiệu này. Khai **B2** (suy từ ví
    dụ + vắng mặt, không phải bảng liệt kê đóng) — cố ý KHÔNG khai B1.
  - Vế 2 — phản đảo **5.1.1** *«Văn bản ban hành đều ghi tên loại văn bản, **trừ công văn**»* ⇒
    CÓ tên loại ⇒ KHÔNG phải công văn (**B1**).
- **⚠ PHẢI neo vào Ô, KHÔNG dò head-blob như nhánh «V/v».** Đo 21-07 trên 190 docx thật: chuỗi
  «-CV/» khớp đúng **1 file — và là DƯƠNG TÍNH GIẢ**: `02_Bao-cao-tiep-thu-chi-dao.docx` là BÁO
  CÁO, chuỗi nằm ở **đoạn thân số 8** (*«Công văn số 3152-CV/VPTW, ngày 19/6/2026»*), **offset
  1040 < 3000** nên `_head[:3000]` CHẠM. Viết theo khuôn cũ là hỏng ngay trên dữ liệu đang có.
- **«Kính gửi» BỊ BÁC làm tiêu chí** (từng là ứng viên): khớp **35/190** file thật — báo cáo, tờ
  trình, phiếu trình. HD05 9.2.3 chỉ cho chiều *công văn ⇒ có Kính gửi*, KHÔNG cho chiều đảo.
- **Ô MỚI `dang.kinh_gui`** (trong bảng biến thể, chỉ sống khi cong_van bật) — HD05 **PL2 mục 5**:
  *«Từ "Kính gửi" đối với thể loại công văn … | In thường | **14** | **Nghiêng**»* + **9.2.3** (ô
  5a), **B1**. `canh`/`thut` = **"na"**: PL2 chỉ pin cỡ+kiểu, còn 9.2.3 *«ở chính giữa, trang đầu
  văn bản»* nhập nhằng giữa canh-giữa và vị-trí-giữa-trang ⇒ không kiểm (khuôn "na" r175).
- **Classifier hệ Đảng:** HD05 không có neo KÝ TỰ cho trích yếu công văn (PL2 nêu ví dụ *«về việc
  chuẩn bị hội nghị…»*, chữ thường) ⇒ neo VỊ TRÍ theo **5.2.3** *«trình bày cân đối dưới số và ký
  hiệu văn bản (ô số 5b)»* — đoạn chưa gán đầu tiên SAU `so_ky_hieu`, khai **B3** (user duyệt
  21-07). Nhánh tự phòng vệ 2 chốt (ô `so_ky_hieu` phải mang «-CV/»; ứng viên không in hoa) vì gán
  vô điều kiện sẽ **cướp đúng đoạn `the_loai`** của báo cáo (bước 3+4 chạy sau, `_set` không ghi đè).
- **⚠ Hồi quy tự bắt được và đã vá:** đặt nhánh `kinh_gui` ngoài cổng «-CV/» làm
  `01_To-trinh_Bo-Chinh-tri.docx` **rụng 1 `TT-DT-THAN-THUT`** (4170→4169) — ô `kinh_gui` không vào
  bảng khi biến thể tắt, nên đoạn bị nuốt thành **mất kiểm âm thầm**. Siết vào trong cổng ⇒
  **190/190 docx thật khớp r177 từng finding một** (183 file thật + 7 file khoá `~$` của Word;
  6 docx mới xuất hiện dưới `C:qh` sau mốc baseline đều hệ hành chính, không ca nào nhận nhầm).
- **Test r176 ca (f), f1-f10:** công văn Đảng chuẩn = 0 TT-DT · trích yếu 14 đứng →
  `TRICH-YEU-CV-{CO,KIEU}` · ô `kinh_gui` sai → `KINH-GUI-{CO,KIEU}` · ô đã `bo`
  (`the_loai`/`trich_yeu`) hết bị kiểm · **chiều nghịch**: BÁO CÁO (có tên loại + «Kính gửi:» +
  «-CV/» ở thân) không bị nhận nhầm và `the_loai` VẪN được kiểm · «Kính gửi» một mình không bật
  được biến thể · «-CV/» + CÓ tên loại không bật được biến thể (f7/f8) · không «-CV/» thì biến
  thể tắt (f9) · BÁO CÁO Đảng có «Kính gửi:» dài vẫn giữ `TT-DT-THAN-THUT` (f10).
- **⚠ Bộ đột biến 7 chốt — bắt được 3 CHỐT CHẾT mà selftest 1131/1131 vẫn xanh.** Vế «vắng
  the_loai», vế «-CV/» tầng check, cổng «-CV/» tầng classifier: gỡ từng cái ra, test vẫn XANH, vì
  mọi ca đều đã bị một chốt KHÁC chặn trước khi chạm tới. Thêm f7/f9/f10 mới đỏ đúng. Hai bẫy phụ
  lộ ra khi dựng ca: (i) dòng «Kính gửi» 23 ký tự rơi **dưới ngưỡng giỏ `than`** ⇒ ca rỗng nghĩa,
  phải kéo dài; (ii) `SK_PAT["dang"]` = `^\s*Số\s+\d+\s*-\s*[A-ZĐ]+/` **không khớp `TTr`** (chữ
  `r` thường) ⇒ `i_sk = None` ⇒ nhánh không chạy ⇒ ca đậu rỗng nghĩa, phải đổi sang «-BC/».
  **Trạng thái cuối:** 6/7 chốt SỐNG (có ca đỏ đúng). Vế «-CV/» ở **tầng check vẫn là CHỐT CHẾT**
  — cổng classifier đã chặn từ trước nên hạ nó xuống `True` không đổi finding nào. **Giữ lại như
  phòng vệ thừa CÓ CHỦ Ý và ghi thẳng vào code** (hai tầng cùng đọc một căn cứ 3.1.2.b), KHÔNG
  tuyên bố là đã được test khoá.
- **Sổ `_BAT_DUOC` giữ nguyên 53 ô** (KHÔNG bump): sổ r173 dựng `_tat_ca` từ bảng CHÍNH
  `_tt_dac_ta()`, còn `trich_yeu_cv`/`kinh_gui` thuộc bảng BIẾN THỂ — không đột biến được trên văn
  bản mẫu chung, nên khoá ở r176 (e)/(f) thay thế. Phạm vi này đã ghi vào comment sổ để khỏi tưởng thiếu.
- **Còn cách ly:** nhóm «văn bản/phụ lục ban hành kèm theo» (NQ351 Mẫu 6b/11b/14) — không đổi.

# ★ v1.35.7 — r177 PHÂN XỬ HAI CA CÁCH LY: trich_yeu·kieu GIỮ «đậm» (gỡ Đ5) · viết tắt Quy định = QĐ (2026-07-21)

> Đóng giỏ «chờ nguyên văn B1» treo từ r176, đúng trình tự «không đoán»: đối soát nguyên văn
> corpus NĐ30 PL I (GDoc `1YgArj3U…`) + HD05 27/5/2026 (GDoc `1Lko21mO…`). selftest **1131/1131**
> + gen_instructions 38/38.

- **Ca 1 — viết tắt "Quy định" hệ Đảng: `QĐ` THẮNG, `QĐi` bác.** HD05 mục 3.1.2.a nguyên văn:
  *«Trường hợp chữ cái đầu các âm tiết của tên loại văn bản trùng nhau thì thống nhất ký hiệu
  một số tên loại văn bản như sau: **Quyết định, Quy định: QĐ**; Chỉ thị: CT; Chương trình: CTr;
  Thông tri: TT; Tờ trình: TTr»*; ví dụ 3.1.2.b(ii): *«Quy định của Uỷ ban Kiểm tra Trung ương —
  Số 23-QĐ/UBKTTW»*. Chuỗi `QĐi` KHÔNG xuất hiện trong toàn văn HD05. `ABBR_DANG` + §5.3 vốn đã
  đúng — sửa phía SẢN PHẨM: `mau-dang-hd05/Mau_Dang_05_Quy_dinh.docx` `Số   -QĐi/ĐU` →
  `Số   -QĐ/ĐU` (readback sạch; quét cả 15 docx chỉ mẫu 05 dính) + bảng GHI_CHU.md kèm nguyên văn.
  ⚠ **ĐÍNH CHÍNH HỒ SƠ**: bảng viết tắt nằm ở HD05 **mục 3.1.2**, KHÔNG phải 3.2 như ghi chú r176
  (3.2 = kỹ thuật trình bày số-ký-hiệu) — cite cờ `TT-VIET-TAT` sửa `HD05 3.2` → `HD05 3.1.2`.
- **Ca 2 — `(hanh_chinh|dang)·trich_yeu·kieu` «đậm,nghiêng vs đậm»: «đậm» THẮNG, GỠ CÁCH LY Đ5.**
  NĐ30 PL I II.5.b nguyên văn: *«Trích yếu nội dung văn bản được đặt ngay dưới tên loại văn bản,
  trình bày bằng chữ in thường, cỡ chữ từ 13 đến 14, kiểu chữ **đứng, đậm**»*; HD05 PL2 mục 5:
  *«Trích yếu nội dung văn bản | In thường | 14-15 | **Đứng, đậm**»* (công văn: 12 nghiêng — khớp
  biến thể TT-5 sẵn có). Bảng đặc tả («dam», B1) vốn đúng ⇒ «đậm,nghiêng» đo được trong thực chiến
  là LỆCH CHUẨN THẬT, không oan. Gỡ khối `_bo_kiem` Đ5 trong `_the_thuc_check_dac_ta`; mức vẫn
  **INFO** (trich_yeu thuộc nhóm tin-cậy-thấp Đ1 — không FAIL, chưa thăng, không cần duyệt zero-oan).
- **Test:** r176 (d) LẬT CHIỀU — trich_yeu đậm+nghiêng nay PHẢI ra `TT-DT-TRICH-YEU-KIEU` mức INFO;
  sổ r173 `_BAT_DUOC` **51→53 ô** (thêm `(hanh_chinh|dang).trich_yeu`), gap ledger 8→6 (hồ sơ
  comment cập nhật). Docstring Đ1-Đ5 + baseline ghi lại theo trạng thái r177.
- **Nghiệm thu:** tầng 1 đo lại @r177 trên 34 file sản phẩm còn trên đĩa (15 docx Đảng + 19 NQ351):
  **0 TT-DT tuyệt đối**; `_TEST_dien_that` giữ **0/0/0**; mẫu trống giữ đúng 2 FAIL số-KH/địa-danh;
  mẫu 05 sau sửa không phát sinh finding mới. Corpus đo-lũ 129 file KHÔNG đo lại được (bản tạm đã
  xoá, `t2_corpus.json` chỉ lưu tên+findings) — theo bảng nghiệm thu r176 (`tong_hop_sau_va.md`
  dòng `trich_yeu·kieu 7/7`), lớp A số học 856 → **863** (+7 INFO, toàn bộ là ca đậm+nghiêng thật).
- **Reference đồng bộ:** §6.34 (Đ5 → phân xử xong kèm nguyên văn; sổ 53 ô; test d lật) · §5.3 hàng
  số-ký-hiệu đóng dấu «không có `QĐi`». ADR-0009 thêm mục «Hậu kiểm 2026-07-21 (r177)». Comment
  `ABBR_DANG` ghi căn cứ 3.1.2.a.
- **Việc mở KHÔNG đổi:** cong_van hệ Đảng chưa có tiêu chí máy · nhóm «kèm theo» (Mẫu 6b/11b/14)
  VẪN cách ly (chưa đối soát đủ căn cứ từng ô) · builder trục kiểu/canh/thụt còn inline · thăng
  FAIL từng ô = vòng sau.

# ★ v1.35.6 — r176 ADR-0009 BƯỚC 5 «NỐI BỘ KIỂM»: lớp đặc tả TT-DT đọc bảng vào production (2026-07-21)

> Hoàn tất trình tự 5 bước ADR-0009. `the-thuc-check` nay có LỚP ĐẶC TẢ đọc bảng `_tt_dac_ta()`
> (+ biến thể r175): finding `TT-DT-<Ô>-<CO|KIEU|CANH|THUT>` theo đúng gói Đ1-Đ5 user duyệt 21-07.
> selftest **1131/1131** (+1: r176) + gen_instructions 38/38.

- **Parser mở rộng** (`_the_thuc_parse_docx`): kênh `p["dt"]` per-đoạn — cỡ (mode), tỉ lệ
  đậm/nghiêng/gạch, `dam_dau` (run đầu — văn phạm `:tien_to`), jc/firstLine/left KẾ THỪA STYLE
  đủ tầng run → pPr/rPr → pStyle → Normal → docDefaults (1 cấp basedOn; thiếu tầng style từng đẻ
  701 finding oan ở đo lũ). Khoá cũ ind/jc/dam/szs GIỮ NGUYÊN ngữ nghĩa — cờ tay r143-r171 không đổi.
- **Classifier `_tt_dt_phan_loai`** port NGUYÊN TRẠNG từ bộ kiểm nháp đo-lũ (6 bẫy oan đã vá giữ
  đủ) + **vá oan mới lộ khi quét sổ**: neo `thong_qua` siết theo công thức Đ36 k1 «<loại> này được
  Quốc hội … thông qua» — thân Lệnh công bố («Luật X đã được Quốc hội thông qua») hết bị gán nhầm.
- **Lớp kiểm `_the_thuc_check_dac_ta`** nối sau T3: Đ1 B1/B2→WARN · B3→INFO · ô tin-cậy-thấp
  (than/ten_cq/ten_cq_tren/trich_yeu/tieu_de_pc/ho_ten_ky)→INFO, KHÔNG BAO GIỜ FAIL; Đ3 chỉ chạy
  khi nhận diện được khối đầu (quoc_hieu/tieu_de), nhóm «kèm theo»/phụ lục bỏ; Đ4 nhường cờ tay
  (TT-BAC-CO-CHU↔(quoc_hieu|tieu_ngu|tieu_de)·co mọi hệ · TT-CHUC-VU-DAM↔dang chuc_vu_ky·kieu ·
  TT-CHUONG-CANH-GIUA↔dang (phan_chuong|muc)·canh — một hiện tượng một finding); Đ5 cách ly
  (hanh_chinh|dang)·trich_yeu·kieu chờ nguyên văn NĐ30 PL I II.5. Biến thể resolve trước khi so:
  «/QĐ-CTN»→qd_ctn · «V/v» đầu dòng→cong_van hanh_chinh (cong_van hệ Đảng CHƯA có tiêu chí máy —
  để sau, không đoán).
- **Sổ `_BAT_DUOC` r173: 1 ô → 51 ô** (test tự cưỡng chế đúng thiết kế — nối xong là sổ buộc phải
  mở). 8 gap còn lại có hồ sơ trong comment r173: 2 Đ5 cách ly · 3 neo-bằng-chính-thuộc-tính-lật
  (de_muc_than ×2, co_quan_ban_hanh) · 2 đoạn văn bản test <25 ký tự · 1 biên quét 2n/3 văn bản ngắn.
- **r176 MỚI** khoá 6 hành vi: (a) tầng-1 builder 3 hệ + Lệnh/QĐ-CTN = 0 TT-DT; (b) Đ3 mất khối
  đầu → lớp im hẳn kể cả khi có lỗi thật; (c) Đ4 chuc_vu_ky Đảng đậm → chỉ TT-CHUC-VU-DAM;
  (d) Đ5 trich_yeu đậm+nghiêng → im; (e) công văn V/v chuẩn 12-13 đứng → 0, V/v 14 nghiêng →
  TT-DT-TRICH-YEU-CV-CO+KIEU, ô đã `bo` không kiểm; (f) `dam:tien_to` «Điều 3.» đậm + nội dung
  Đứng → không TT-DT-DIEU-KIEU, không giẫm TT-KHOAN-DAM.
- **NGHIỆM THU trên corpus đo-lũ** (129 file, baseline `t2_corpus.json` @v1.35.5): tầng 1 —
  19 mẫu NQ351 + 15 mẫu HD05 + builder qua PRODUCTION = **0 TT-DT tuyệt đối**; lớp A 876 → **856**,
  diff per-ô ĐÚNG 5 dòng giải trình 100% theo quyết định đã duyệt (−9 Đ4 nhường TT-BAC-CO-CHU:
  tieu_de 7 + quoc_hieu 1 + tieu_ngu 1 · −4 Đ4 nhường TT-CHUC-VU-DAM · −7 Đ5 cách ly trich_yeu);
  lớp B phụ lục 3.905 → **0** (Đ3); lớp C 46 → 42 (−4 cùng lý do Đ4/Đ5). Chống-trùng kiểm tay
  2 file đại diện: mỗi hiện tượng đúng 1 finding cờ tay, 0 TT-DT trùng.
- tl.py: +2 tên `_STUB_MAP["the_thuc"]` (`_tt_dt_phan_loai`, `_the_thuc_check_dac_ta`).

# ★ v1.35.5 — r175 ADR-0009 BƯỚC 4 ĐO LŨ xong + vòng-2 BƯỚC 1 vá bảng theo 5 quyết định Đ1-Đ5 (2026-07-21)

> BƯỚC 4 "đo lũ" chạy NGOÀI repo (bộ kiểm nháp đọc bảng, `D:\Quốc hội\do-lu-2026-07-21`), user duyệt
> cả gói Đ1-Đ5, rồi quay bước 1 vá bảng ngay trong release này. selftest **1130/1130** (+1: r175) + 38/38.

- **Số liệu bước 4** (skill v1.35.4): tầng 1 — builder tự dựng 0 finding; 33 mẫu chuẩn 15 finding,
  đối chiếu tay **100% là khiếm khuyết của BẢNG, không phải lỗi mẫu**. Tầng 2 — 129 file thật
  (khớp 105/111 dòng nền 19-07): lớp A 49 VB hoàn chỉnh **1.214 finding**, hai VB nền "đạt chuẩn
  hoàn toàn" ăn 85/57 ⇒ **Đ1: chưa ô nào thăng FAIL** (zero-oan chưa ai đạt). Phiên đo tự bắt
  6 nguồn cảnh báo oan của chính bản nháp (7.779 → 5.842) — "đo trước, phán sau" trả lãi.
- **5 quyết định Đ1-Đ5** (ADR-0009, user duyệt 21-07): Đ1 không thăng FAIL; Đ2 vá bảng trước khi
  nối; Đ3 chỉ áp lớp đặc tả cho file có khối đầu; Đ4 chống báo trùng cờ tay; Đ5 cách ly
  `trich_yeu·kieu` chờ nguyên văn NĐ30 PL I II.5.
- **Bảng 54 → 59 ô** (thi hành Đ2): vbqppl_qh +3 ô B1 đo từ sơ đồ mẫu (`cau_ban_hanh` «Quốc hội
  ban hành Luật … .» 14 nghiêng; `co_quan_ban_hanh` dòng chủ thể «CHỦ TỊCH / NƯỚC CHXHCNVN» 14 đậm
  giữa — tầng 1 lộ: 3 finding chuc_vu_ky 14pt là bản nháp GÁN NHẦM dòng này, chữ ký thật 13pt khớp
  bảng; `tu_lenh` «QUYẾT NGHỊ:»/«NAY …:» 14 đậm giữa); ô `can_cu` QH mở nghĩa gồm «Xét/Theo đề
  nghị»; `de_muc_than` hanh_chinh (B3→INFO vĩnh viễn) + dang (B2* — reference TT-6 «đề mục: đậm»).
- **Văn phạm ô mới**: kiểu `dam:tien_to` (ô `dieu` cả 3 hệ — đậm áp TIỀN TỐ «Điều N.»+tên, nội dung
  inline Đứng, khớp `dam_dau` r171); giá trị `na` cho canh/thụt = luật không ấn định + thực tiễn đa
  dạng ⇒ KHÔNG kiểm (đề mục tự do: kho mẫu HD05 canh giữa, corpus dàn đều thụt 1cm — hai kiểu cùng sống).
- **`_tt_dac_ta_bien_the()` MỚI** — trục thứ ba BIẾN THỂ THEO MẪU: override Mẫu 16 QĐ-CTN (quốc hiệu
  13, B1 sơ đồ); biến thể công văn hanh_chinh (ô 5b NĐ30: trích yếu «V/v» 12-13 đứng, B2*) và dang
  (TT-5: 12 nghiêng, B2*) kèm `bo` tên loại/trích yếu; nhóm «kèm theo» (6b/11b/14) VẪN CÁCH LY.
- **Test**: r170 mở rộng 59/59 ô (+spec Lệnh CTN thứ 5; parse `:tien_to`; skip `na`) · r173 đột biến
  phủ 59/59 (spec Lệnh CTN + câu ban hành + đề mục; sổ `_BAT_DUOC` KHÔNG đổi — đúng: bộ kiểm chưa
  nối) · **r175 MỚI** khoá cấu trúc bảng biến thể (override phải KHÁC gốc + đủ căn cứ/bậc; ô `them`
  tuple-6 không trùng bảng chính; `bo` trỏ ô có thật).
- **Builder BYTE-IDENTICAL** — không ô mới nào chảy vào `_tt_co_build`/`_CHON`; bundle ×2 cùng SHA.
- **Đo lại sau vá** (bộ kiểm nháp): tầng 1 **0/0/0 TUYỆT ĐỐI** (builder · 19 mẫu NQ351 · 15 mẫu
  HD05 — đạt chuẩn ADR "mẫu chuẩn 0 finding lệch bảng"); lũ lớp A 1.214 → **876**.
- Hồ sơ: `docs/adr/0009` cập nhật bước 4 + Đ1-Đ5 + nội dung r175 · reference §6.34 (59 ô, `:tien_to`,
  `na`, biến thể) · CONTEXT.md +«Biến thể mẫu», +«na».
- Còn lại bước 5 (nối bộ kiểm theo Đ3/Đ4/Đ5, cập nhật sổ `_BAT_DUOC` từng ô) — phiên sau.

# ★ v1.35.4 — r174 ADR-0009 BƯỚC 3a: cỡ chữ builder DẪN XUẤT từ bảng đặc tả — byte-identical (2026-07-21)

> BƯỚC 3 (phần a — cỡ chữ, thứ dễ trôi nhất vì là con số). selftest **1129/1129** + 38/38 giữ nguyên.

- **`_tt_co_build(he)` MỚI**: dict `S` của `the_thuc_build` không còn hard-code — dẫn xuất từ
  `_tt_dac_ta()`: ô đơn trị dùng thẳng; ô khai DẢI tra `_CHON` (lựa chọn nội bộ **bậc B3** trong dải
  luật, đặt CẠNH bảng, lệch dải là ValueError ngay lúc build — thà nổ sớm còn hơn lặng lẽ hard-code
  trở lại). Từ nay **sửa cỡ trong bảng là builder đổi theo** — đúng nghĩa nguồn sự thật cho trục cỡ chữ.
- **Bằng chứng an toàn**: đối chiếu tay 33 giá trị × 3 hệ khớp 100% S cũ; build lại 4 văn bản chuẩn
  (dang · Luật QH · NQ UBTVQH · hành chính) **BYTE-MATCH sha256 `word/document.xml`** trước/sau.
  Đăng ký `_tt_co_build` vào bảng re-export `tl.py` (bẫy #6).
- **Phạm vi trung thực**: kiểu/canh/thụt trong builder VẪN inline tại từng chỗ render — nhưng bị
  r170 (54/54 ô) + r173 (đột biến) khoá từ ngoài: builder lệch bảng là đỏ ngay. Nối nốt trục
  kiểu/canh vào lúc nối bộ kiểm (bước 5) nếu thực tế cho thấy cần — ghi chú trong ADR-0009.

# ★ v1.35.3 — r173 ADR-0009 BƯỚC 2: khoá test 100% (54/54 ô) + selftest đột biến sổ-hai-chiều (2026-07-21)

> BƯỚC 2/5 của ADR-0009. selftest 1128→**1129** (thêm r173), gate GIỮ 9 bước — đột biến là NỘI DUNG
> của bước selftest, không phải bước gate mới (Q7 user chốt).

- **r170 chiều thuận 28→54/54 ô**: thêm văn bản dựng thứ 3 (NQ UBTVQH — phủ `dia_danh/muc/quyen_han_ky/
  noi_nhan_*` hệ QH mà mẫu Luật không có) + thứ 4 (**hành chính 18/18 ô — trước đây hệ này 0 test**);
  dang bổ `muc` + `noi_nhan_tu`; qh-Luật bổ `thong_qua`. **KHOÁ ĐỦ-PHỦ tự cưỡng chế**: r170 đối chiếu
  tập (hệ, ô) đã test với toàn bảng — thêm ô vào bảng mà quên viết test là ĐỎ ngay, độ phủ không thể
  trôi ngầm lần nữa (bài học 28/48=58% âm thầm của r170 cũ).
- **r173 chiều nghịch — đột biến LẬT ĐẬM từng ô (54 đột biến) + SỔ HAI CHIỀU**: `_BAT_DUOC` ghi ô bộ
  kiểm HÔM NAY bắt được (duy nhất `dang.chuc_vu_ky` → TT-CHUC-VU-DAM, cờ viết tay — khớp thực nghiệm
  1/5 ngày 20-07); tụt lùi = đỏ · ô gap bật cờ mới (bước 5 nối dần) = đỏ buộc ghi sổ. Máy-canh-cho-
  máy-canh: bằng chứng sống rằng dây nối bảng→bộ kiểm hoạt động, sống sót qua refactor.
- **Bẫy mới ghi nhận**: `the_thuc_check()` gọi thẳng cấp module KHÔNG normalize `-`→`_` của tham số
  `he` (chỉ CLI normalize) — `he="vbqppl-qh"` nổ KeyError câm trong test. r173 dùng dạng gạch dưới.
- **Vá lệch version 3 nơi**: v1.35.2 commit trước bump file `VERSION` nhưng SÓT hằng `tl.py:94` và
  header SKILL.md ⇒ r65 (guard ADR-0001 `version_forked == VERSION`) đỏ đúng chức năng. v1.35.3 đồng
  bộ cả ba. Bài học: bump version = **3 chỗ** (VERSION · tl.py · SKILL.md header).
- Kernel chỉ đổi header ⇒ re-import Capabilities KHÔNG bắt buộc.

# ★ v1.35.2 — r172 ADR-0009 BƯỚC 1: vá bảng đặc tả (+bậc thẩm quyền) · normalize idempotent với build (2026-07-21)

> Grilling 20→21-07 chốt ADR-0009 (8 quyết định, user duyệt từng cái): `_tt_dac_ta()` sẽ thành nguồn
> sự thật DUY NHẤT (nối 5 bước); thang thẩm quyền B1>B2>B3; severity buộc vào bậc (B3→INFO vĩnh viễn);
> chuẩn thăng FAIL zero-oan; selftest đột biến hai chiều (gate GIỮ 9 bước). Đây là BƯỚC 1.
> Cứ liệu mở màn: đo 5 đột biến vi phạm bảng → bộ kiểm bắt 1/5; bảng không được hàm nào đọc (kể cả
> builder — chỉ selftest); file "0 finding" theo GHI_CHU thực chất 2 WARN thật. selftest **1128/1128** giữ.

- **`_tt_dac_ta()` 48→54 ô, tuple 5→6 trường (+`bac`)**: mỗi ô tự khai bậc thẩm quyền B1/B2/B3
  (hậu tố `*` = giá trị đơn chọn trong dải luật). `hanh_chinh` 13→18 ô: TÁCH `ten_cq_tren` (chủ quản
  KHÔNG đậm — hết mâu thuẫn §6.16) + 4 ô bố cục `phan_chuong/tieu_de_pc/muc/dieu` (NĐ30 PL I II.6);
  `vbqppl_qh` 18→19: bổ khuyết `quyen_han_ky` (Đ37 k1, Mẫu 10-13); 5 ô dẫn chiếu mơ hồ "PL I sơ đồ"
  → đích danh **Đ30/Đ31/Đ33**. Hai hệ `vbqppl`/`vbhn` **khai trắng tường minh** `__khai_trang__`
  (ADR-0009: cấm giả vờ kiểm). r170 unpack `[:5]`.
- **M5 CHẾT — normalize idempotent với build**: `_fix_sect` lề phải THEO HỆ (`he_eff`): nhà nước
  **1134=20mm** (= builder; NĐ30 dải 15-20, chọn 20 là B3 — Q4 user chốt), Đảng giữ **850=15mm** HD05
  đơn trị. Trước đây normalize ép 850 toàn cục ⇒ âm thầm đổi lề mọi file nhà nước đã build. Đã chứng
  minh: build→normalize giữ nguyên 4 lề (hành chính) · Đảng vẫn 850. `criteria["normalize"]` tách
  `le_nha_nuoc`/`le_dang` — NEO dòng 415 + r135 anchor + r138 fixture sửa cùng release (đúng quy trình
  drift-lock). **Lưu ý vận hành:** file NHÀ NƯỚC normalize từ nguồn lề 15mm nay ra 20mm (khác bản .35.1).
- **Comment nhánh WARN dải-hợp sửa đúng sự thật**: nhánh `rng is None` KHÔNG chết — chỉ còn `vbhn`
  chạm (ke_thua chưa materialize, không khai khoá lề); nhãn cũ "vbqppl_qh" sai từ v1.34.76.
- **Reference đồng bộ**: §6.34 viết lại (54 ô = 18+19+17, 22 khoá — hết cách đọc nhầm "48 × 3 hệ");
  §6.25 đệm ô 6pt→**4pt** theo r164 (nhãn B3); §6.17 làm rõ "Mẫu 1-16 = 19 sơ đồ" (mẫu 6/11/15 tách
  a/b) — hết vênh 16-vs-19; §8 normalize mô tả lề theo hệ.
- **Hồ sơ**: `docs/adr/0009` (8 quyết định + trình tự 5 bước + zero-oan) · `CONTEXT.md` cụm "Thể thức"
  (Đặc tả thể thức · Bậc thẩm quyền · Cách ly). **CÁCH LY chờ B1**: viết tắt `QĐi` (Mẫu Đảng 05) vs
  `QĐ` (`ABBR_DANG` + §5.3) — cần nguyên văn HD05 mục 3.2 mới phân xử, KHÔNG đoán.
- Ngoài repo: `mau-dang-hd05/_TEST_dien_that` điền lại đúng (0/0/0 thật @v1.35.1, dấu `;`, hết tổ chức
  KL121, một kiểu dấu) · GHI_CHU đóng dấu kiểm chạy-lại-được + sử liệu vụ trôi.

# ★ v1.35.1 — khoản/điểm không in đậm · công thức ban hành VB Đảng (§6.35-6.36) (2026-07-20)

> User rà mẫu Quyết định: *"đoạn BAN THƯỜNG VỤ QUYẾT ĐỊNH có căn giữa không · nội dung Điều 3 tại
> sao phải in đậm · kiểm tra tương tự với các mẫu khác"*. selftest 1127→**1128**.

- **§6.35 KHOẢN/ĐIỂM KHÔNG IN ĐẬM.** HD05 PL2 mục 6 tách ba dòng: *"Từ 'Điều', số thứ tự và tên
  điều"* = đậm · *"Khoản"* = Đứng · *"Điểm"* = Đứng. Minh hoạ ở cấp RUN xác nhận
  `1. Quy định về…`[đậm=0]. Điều KHÔNG có tên (6.2.4.c cho phép *"tên điều hoặc nội dung của
  điều"*) ⇒ chỉ tiền tố `Điều N.` đậm, nội dung in thường — HAI RUN trong cùng đoạn
  (`spec.body[].dam_dau`). Cờ mới **`TT-KHOAN-DAM`**; thêm `spec.body[].nghieng`.
  ★Bẫy: hàm phân loại đề mục dùng `t.upper() == t`, mà `"1- …"`/`"…"` không có chữ cái nào nên cũng
  thoả ⇒ **34 đoạn nội dung khoản bị in đậm** khắp bộ mẫu Đảng. Điều kiện đúng: in hoa **và ≥2 chữ cái**.
- **§6.36 CÔNG THỨC BAN HÀNH VB ĐẢNG LÀ CÂU THƯỜNG.** HD05 không quy định; cứ liệu là chính
  QĐ 399-QĐ/TW: *"Ban Bí thư quy định về … như sau:"* — in thường, không in hoa/đậm/canh giữa.
  NGƯỢC với VBQPPL (`QUYẾT NGHỊ:` in hoa đậm canh giữa). Mẫu Quyết định sửa
  `BAN THƯỜNG VỤ QUYẾT ĐỊNH` → `Ban Thường vụ quyết định:`.
- *"Kính trình"* chuyển sang **nghiêng** (HD05 PL2 mục 9), trước bị in đậm.
- **ĐÍNH CHÍNH CĂN CỨ**: quy tắc bố cục Phần/Chương/Mục/Điều của HD05 là **mục 6.2.4**, không phải
  6.2.3 (6.2.3 = phần căn cứ ban hành). Sửa trong reference §6.33 và bảng `_tt_dac_ta()`.

# ★★ v1.35.0 — TẤT ĐỊNH HOÁ quy tắc thể thức 3 hệ (§6.34) + thụt Điều NQ351 (2026-07-20)

> User: *"kiểm lại mẫu NQ351 có lỗi Chương/Điều tương tự không"* + *"nghiên cứu cách tất định hoá
> các quy tắc thể thức của Đảng, Quốc hội và hành chính"*. selftest 1126→**1127**.

**Kết quả rà 19 mẫu NQ351**: KHÔNG có lỗi như mẫu Quy chế Đảng — Phần/Chương/Mục đã `center` không
thụt, Điều đã có dấu chấm sau số. Nhưng lộ **một khác biệt tinh vi giữa hai hệ** đang bị làm giống
nhau: NQ351 Đ35 k2 c ghi Điều **"cách lề trái 1cm đến 1,27cm"** (thụt TRÁI cả khối) trong khi HD05
6.2.2 ghi **"khi xuống dòng thì chữ đầu dòng lùi vào"** (thụt DÒNG ĐẦU). Một dòng thì nhìn giống
nhau, chỉ lộ khi tiêu đề điều xuống dòng. Đã tách: `kieu="dieu"` ở hệ `vbqppl_qh` dùng `w:ind
w:left`, hệ `dang` giữ `w:firstLine`. `_tt_p` nhận thêm tham số `left`.

**TẤT ĐỊNH HOÁ — `_tt_dac_ta()`**: bảng đặc tả `(cỡ, kiểu, canh, thụt, căn_cứ)` cho **48 thành phần
× 3 hệ**. Bổ khuyết cho `_the_thuc_criteria()` vốn chỉ khoá ngưỡng SỐ, trong khi mọi lỗi thực chiến
đều ở kiểu chữ / canh lề / loại thụt. **`r170` đối soát HAI CHIỀU**: dựng văn bản thật cho từng hệ
rồi kiểm từng thành phần khớp bảng ⇒ builder và bảng không thể trôi khỏi nhau.

Bảng làm hiện rõ **ba chỗ ba hệ thực sự khác nhau — đúng ba lỗi đã mắc trong phiên**:
`chuc_vu_ky` (Đảng in thường, hai hệ kia đậm) · `noi_nhan_tu` (Đảng gạch chân, hai hệ kia đậm+
nghiêng) · `dieu` (QH thụt trái, Đảng thụt dòng đầu).

★Bẫy lặp lại: hàm module-level mới (`_tt_dac_ta`) phải đăng ký bảng re-export trong `tl.py`, nếu
không `_TL_MODULE._tt_dac_ta` không resolve và test đỏ **không kèm chẩn đoán**. ★Bẫy regex: đổi thẻ
`<w:ind>` thêm `w:left` làm `r'<w:ind w:firstLine="…"'` hết khớp — đừng neo vào thứ tự thuộc tính.


> **[r194] Lịch sử 1.33.54 → 1.34.99 đã chuyển NGUYÊN VĂN sang `references/changelog_archive/CHANGELOG-1.33.54-den-1.34.99.md`** (dev-only, không vào bundle — tiền lệ v1.34.69; bản 1.33.53 trở về trước ở `CHANGELOG-den-1.33.53.md`).
