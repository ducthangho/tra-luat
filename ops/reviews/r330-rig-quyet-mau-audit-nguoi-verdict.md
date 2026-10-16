> **CÁCH ĐĂNG — đọc trước, đừng bỏ qua.**
> Comment này do **PHIÊN AGENT đăng HỘ** chủ kho theo chỉ thị, **KHÔNG** phải chủ kho tự gõ.
> Chỉ thị nguyên văn, phiên điều phối 20-09-2026: *"Nhánh bookkeeping riêng đi, rồi đăng hộ
> tôi verdict"*, nối tiếp chuỗi *"Thi công #565 đi"* → *"Mở nợ MAX_PATH, sửa script rồi tôi
> chạy nốt tầng 4"* → các lượt gửi log đo trên máy chủ kho.
> Khuôn chuẩn đòi chủ kho **tự đăng**; lượt này **không** đạt điều đó và khai thẳng ra.
> `author_association: OWNER` ở comment này **KHÔNG** phân biệt được người với máy — phiên chạy
> bằng credential chủ kho, đã ĐO được ở #551 (nợ #566). Thẩm quyền của lượt này neo vào **chỉ
> thị trong phiên**, không vào tác giả comment.
> **ĐỪNG dùng lượt này làm tiền lệ cho việc phiên agent đăng hộ chữ ký người.**

## human_audited — R330-RIG-QUYET-MAU-VA-NGOAI-LE-BI-NUOT (#565), người audit: @ducthangho

Tôi tự đọc `git diff dc85dd0a..8c425b1` (**2 tệp, +154/−8**) và đặc tả đóng băng
`ops/specs/r330-rig-quyet-mau-va-ngoai-le-bi-nuot-r1.md` (`sha256 64a4d2f0eea7657c…`,
11 942 B). Lease `r330-rig-quyet-mau-r1-g1-claude`, hạn `2026-09-20T16:02Z`.

### Bằng chứng — bốn tầng, HAI lượt chạy đầy đủ trên máy tôi, `2026-09-20` `02:13Z` và `02:37Z`

Bộ đo dựng **cả hai vế trong MỘT lệnh** và kiểm AST của từng clone trước khi đo.

**S1 — máy này CÓ biểu hiện bệnh** (điều kiện để mọi kết luận sau có nghĩa):

| chỗ | b6 `02:13Z` | b7 `02:37Z` |
|---|---|---|
| `%TEMP%` | **17/20** (0,85) | **18/20** (0,90) |
| cạnh kho `D:\…\_do_565_tam` | **19/20** (0,95) | **16/20** (0,80) |

`bash` = `C:\Windows\system32\bash.EXE`, `uname` → `Linux`, `/mnt/c` ⇒ **alias WSL**, đúng cơ
chế đã chẩn đoán (WSL giữ handle trên cwd ⇒ `PermissionError [WinError 32]` trên THƯ MỤC).

**S4 — đúng thứ đang đo:** nền `_goi` hình dạng **CŨ** (`with TemporaryDirectory`), `_t110`
in vô điều kiện **False**; ứng viên hình dạng **MỚI** (`mkdtemp` + `finally` +
`ignore_errors`, `return` trong thân `try`), `_t110` in vô điều kiện **True**.

**Tầng 2 — chạy CHÍNH `_goi` trích từ từng clone, 20 lượt mỗi vế:**

| | NÉM (b6) | NÉM (b7) | trả False |
|---|---|---|---|
| nền `dc85dd0a` | **17/20** | **16/20** | 0 |
| ứng viên `8c425b1` | **0/20** | **0/20** | 0 |

Vế nền NÉM ở cả hai lượt ⇒ **đối chứng âm ĐẠT**: rig phơi được bệnh, nên ứng viên xanh có nghĩa.
Không lượt nào có `trả False` — tức bản vá không đổi KẾT QUẢ của phép đo, nó chỉ thôi làm phép
đo chết vì dọn dẹp.

**Tầng 4 — `tl --selftest` trọn vẹn, một lượt mỗi vế:**

Hai lượt độc lập, cùng cặp commit — b6 lúc `02:13Z`, b7 lúc `02:37Z`. Số dưới đây là **b7**,
lượt gom được TÊN mọi ca đỏ; b6 khớp từng con số ở mọi ô trừ thời lượng.

| | nền `dc85dd0a` | ứng viên `8c425b1` |
|---|---|---|
| tổng kết | `rc=1` · **1708/1710** | `rc=1` · **1710/1711** |
| ca ĐỎ **có tên** | **2**: `r330_deploy_msg_khong_chay_lenh`, `r378_l7_resolve_phai_o_trong_kho` | **1**: `r378_l7_resolve_phai_o_trong_kho` |
| `r330_deploy_msg_khong_chay_lenh` | **`[FAIL]`** | **`[OK]`** |
| `r379_rig_khong_quyet_mau…` | (chưa có ca này) | **`[OK]`** |
| `[LOI-VO-CAN?]` | 0 | 1 (`r378…: OSError [WinError 1314]`) |
| tệp `tl_selftest.py` trong lúc chạy | 355 ảnh chụp · **1 trạng thái** (2 145 309 B, `e8a31e8b1b429b1b`) | 374 ảnh chụp · **1 trạng thái** (2 156 120 B, `8c34fb0d6c9050ae`) |
| worktree | `rc=0`, 36,6 MiB | `rc=0`, 36,6 MiB |

Phân định tầng 4: **ĐẠT**. Tiêu chí là **DELTA**, không phải `rc` tuyệt đối — nền tự nó cũng
không xanh (`CLAUDE.md` §Quy trình sửa code: *"tiêu chí là DELTA so master = 0, KHÔNG phải 0
tuyệt đối"*). Và phép trừ phải chặt hơn "không tăng": r330 nằm TRONG số đỏ của nền, nên đỏ
phải **giảm ≥ 1**. Đo được **2 → 1**.

Quan trọng hơn con số: **ngoài `r330`, tập ca đỏ của hai vế BẰNG NHAU — đúng `{r378}`**. Đây là
phép so TẬP TÊN chứ không phải so số đếm, nên nó loại hẳn ca "mất một ca đỏ cũ, thêm một ca đỏ
mới, tổng không đổi". v2 phải suy luận chỗ này; v3 thì đo được.

### Cổng trên Linux (container agent, đo lại `2026-09-20` ~02:5xZ, `core.abbrev=7`)

| cổng | kết quả |
|---|---|
| `tl.py --selftest` | `rc=0` · **1711/1711** · 0 dòng `[LOI-VO-CAN?]` |
| `release-verify … --strict --json` (lệnh của **lane LAND**) | `ok=true` · `expected_file_count 180 == checked_file_count 180` · 0 failed · 0 extra |
| `adr-song` · `doctrine-scan` · `doc-claims-check --strict` · `git diff --check` | `rc=0` cả bốn |

Trần `ADR-0044:5` cho class `sensitive`: **2 tệp ≤ 3** · **+154 dòng ≤ 300**. Không xin ngoại lệ.

### Bốn chỗ tôi soi trực tiếp trong diff

1. `_goi` — dọn dẹp đã **ra khỏi đường quyết định**: `mkdtemp()` → `try: … return` →
   `finally: rmtree(ignore_errors=True)`. Không còn context manager nào có quyền NÉM sau khi
   phép đo đã có kết quả. Chữa bằng **kiến trúc**, đúng yêu cầu của lease vì hình dạng
   `RIG-QUYET-MAU-CUA-PHEP-DO` đã chạm mức NĂM.
2. `_t110` — in kiểu ngoại lệ **vô điều kiện**, không chờ `TL_SELFTEST_DEBUG`; vẫn
   `cases.append((name, False))` nên **không** đổi hành vi phân loại (M3 giữ nguyên). Cắt ở
   400 ký tự và **khai thẳng số ký tự đã cắt**.
3. `r379` — ca mới, bốn nhánh vị từ độc lập. **Răng đo được, không tả:** ba đột biến, mỗi
   nhánh vế A một cái, chạy trong ba bản sao cây riêng — `mA1` (thêm một
   `with TemporaryDirectory()` vào `_goi`) · `mA1b` (`ignore_errors=True→False`) · `mA2`
   (đưa `return` ra ngoài `try`) — **cả ba làm `r379` ĐỎ** (`1710/1711`) trong khi nền xanh
   (`1711/1711`), và **cả ba giữ `[OK] r330`** ⇒ r379 đo HÌNH DẠNG độc lập với kết quả chạy
   của r330.
4. Chính `r378` trong bảng trên **là vế B đang làm việc trên dữ liệu thật**: trước bản vá nó
   đỏ mà không để lại một dòng nào; nay nó nói thẳng `OSError [WinError 1314] A required
   privilege is not held by the client`. Đó là bằng chứng Đ2 hoạt động, không phải hồi quy.

### Tôi chấp nhận tường minh — năm khuyết tật ĐÃ BIẾT

1. **`r379` đã ĐỎ MỘT LẦN, và nguyên nhân tới giờ CHƯA BIẾT.** Lúc 01:35Z 20-09 trên
   `dbaf3a7`, `r379` ném `SyntaxError: invalid syntax (<unknown>, line 1602)` khi nó
   `ast.parse` nguyên `scripts/tl_selftest.py` — trong khi CHÍNH tệp ấy đang chạy. Cùng
   commit, cùng máy, cùng python, lượt 00:55Z thì xanh.
   · Đã **loại trừ** ở tầng tĩnh: blob git, cây làm việc, worktree mới — parse **0/30 NÉM**
   mỗi nguồn, băm khớp, không CRLF / CR lẻ / BOM / NUL, `core.autocrlf=false`, `eol=lf`.
   · Bản vá `8c425b1` **thu hẹp bề mặt PARSE** từ 30 374 dòng xuống thân một hàm (~30 dòng),
   và bắt chẩn đoán phải nêu tên tệp + số byte + băm.
   · **Nói cho đúng, kẻo lại khai rộng hơn phép đo:** bề mặt **ĐỌC** thì **KHÔNG** thu hẹp —
   `inspect.getsource` đi qua `linecache`, mà `linecache` vẫn nạp cả tệp. Nếu nguyên nhân là
   một lần đọc hỏng thì bản vá chỉ **giảm xác suất trúng**, không loại bỏ nó.
   · Đã **loại trừ thêm** bằng b7: tệp `tl_selftest.py` được chụp băm mỗi 2 giây trong suốt lượt
   selftest — **355 ảnh chụp ở vế nền và 374 ở vế ứng viên, mỗi vế đúng MỘT trạng thái**. Tệp
   trên ĐĨA không đổi giữa chừng. Nói hẹp cho đúng: điều đó loại giả thuyết "tệp bị ghi đè", chứ
   **không** loại giả thuyết "một lần ĐỌC trả về byte hỏng" — đọc hỏng là sự kiện từng-lần-đọc.
   · **Bằng chứng nay là 2/2 xanh, vẫn CHƯA đủ để khai đã chữa.** Trên `dbaf3a7`: 2 lượt, 1 xanh
   1 đỏ. Trên `8c425b1`: 2 lượt đầy đủ (b6 `02:13Z`, b7 `02:37Z`), **cả hai xanh**. Với một lỗi
   tần suất chưa biết, hai lượt xanh chỉ làm bằng chứng mạnh hơn, không làm nó thành chứng minh.
   · **Hiệu ứng người quan sát, tôi khai chứ không giấu:** phép canh của b7 tự nó đọc tệp 2 MB
   hàng trăm lần trong lúc chạy, và tầng 4 của b7 chậm hơn b6 rõ rệt (nền 345,6s → 720,7s; ứng
   viên 235,4s → 763,6s). Hai việc **trùng thời điểm**; tôi **chưa tách được** đấy là do phép
   canh hay do máy bận. Nghĩa là lượt xanh của b7 chạy dưới điều kiện I/O khác lượt đã đỏ.
2. ~~**Ca đỏ THỨ HAI của vế nền chưa có tên.**~~ **ĐÃ ĐÓNG bằng phép đo** (b7, `02:37Z`): ca ấy
   là **`r378_l7_resolve_phai_o_trong_kho`**, đúng ca đang đỏ ở vế ứng viên. Tôi giữ mục này
   trong danh sách để lưu rằng v2 của bản nháp đã phải SUY LUẬN chỗ này, và cái phải suy luận
   ấy sinh ra chỉ vì bộ gom của phiên agent bỏ sót — dữ liệu vẫn luôn nằm trong log.
3. **`r378` đỏ vì MÔI TRƯỜNG, không vì bản vá** — `OSError [WinError 1314] A required privilege
   is not held by the client`, tức máy tôi thiếu quyền tạo symlink. Nó đỏ ở **CẢ HAI** vế, đã
   đo bằng tên. Bản vá làm nó HIỆN RA (trước đó nó đỏ câm), không chữa nó.
4. **Công cụ đo của phiên agent đã sai BA lần trong chính packet này**, cả ba do phiên ấy tự
   khai chứ không phải tôi bắt: (a) bản 4 đòi `rc == 0` tuyệt đối nên in
   *"r330 vẫn hỏng trong suite"* trong khi r330 đã `[OK]` — một câu SAI VỀ SỰ VIỆC; (b) bản
   vá cho (a) hụt một bậc (`>` đáng ra `>=`), suýt cấp ĐẠT cho một lượt có ca mới đỏ; (c) bộ
   gom chỉ bắt tên `r330` nên tự làm mù mình về các ca đỏ khác, rồi khai với tôi rằng chúng
   "không nêu tên được". **Công cụ đo KHÔNG nằm trong write set và KHÔNG vào kho** — chữ ký
   của tôi không bảo chứng cho nó, chỉ cho bản vá.
5. **Không có reviewer máy.** `cross_approved` KHÔNG ĐẠT ĐƯỢC chứ không phải "chưa đo": codex
   hết quota review (`chatgpt-codex-connector[bot]`: *"You have reached your Codex usage
   limits for code reviews"*, PR #567), agy hết quota, claude LÀ executor. Nghĩa là người viết
   bản vá cũng là người viết bộ đo ra kết luận cho bản vá. Chữ ký của tôi là thứ duy nhất
   đứng ngoài vòng ấy.

### Đếm hình dạng lỗi (chép sang packet kế thừa)

| hình dạng | lúc cấp lease | sau lượt này |
|---|---|---|
| `RIG-QUYET-MAU-CUA-PHEP-DO` | 5 | 5 (đây là thứ packet chữa) |
| `NGOAI-LE-BI-NUOT-LANG` | 2 | 2 |
| `LOI-KHAI-RONG-HON-PHEP-DO` | 3 | **6** (+3: mục 4a/4b/4c trên) |
| `GIA-THUYET-CHUA-KIEM-VIET-NHU-DA-KIEM` | 1 | 1 |

`LOI-KHAI-RONG-HON-PHEP-DO` **đã quá ngưỡng ba lần** — và cả ba lần mới đều nằm trong CÔNG CỤ
ĐO, không trong sản phẩm. Đó là một nợ riêng, không phải việc của packet này.

### Lời khai tôi cho phép, và lời khai tôi KHÔNG cho phép

Lease đóng băng ghi `loi_khai_dung` là *"Nguyên nhân đã xác định; bản vá **CHƯA** được xác
nhận trên nền thật"* — đúng ở thời điểm cấp, vì chưa có lượt Windows nào. Nay đã có. Tôi
**nâng** lời khai đó thành:

> Nguyên nhân của `r330` đã xác định và bản vá ĐÃ được xác nhận trên nền thật — **hai lượt
> độc lập**, trên một máy Windows 11 + WSL, ngày 2026-09-20, với đối chứng âm ĐẠT ở cả hai
> (nền NÉM 17/20 rồi 16/20; ứng viên 0/20 cả hai lượt).

**KHÔNG** cho phép khai: *"suite đã xanh trên Windows"* (không xanh — `r378` còn đỏ ở cả hai
vế) · *"đã chữa r330 trên mọi cấu hình Windows"* (một máy) · *"`r379` đã hết chập chờn"*
(**chưa chứng minh** — 2/2 xanh không phải chứng minh; xem mục 1) · *"`r378` là lỗi của môi
trường nên không cần xử"* (nó là nợ riêng, chưa ai mở).

VERDICT: approve
Reviewed commit: 8c425b1934ec416dc9001da19b5f30eedcebd7d5

---
_Generated by [Claude Code](https://claude.ai/code)_
