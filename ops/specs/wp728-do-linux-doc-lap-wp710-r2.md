# wp728 — Phép đo Linux ĐỘC LẬP cho mã WP710 đã land (zombie/subreaper, suite PowerShell) — Spec r2

> Thay thế r1 (`ops/specs/wp728-do-linux-doc-lap-wp710-r1.md`, blob `9f3dbc6d30be33c154f915c1a22ca2439ad057b8`,
> sha256 `86a20133bfe117402d1da4fb5cbbf4d5076c96b998e802890a535cdb257f8001`). r1 đã có băm nên KHÔNG sửa đè; mọi lease
> wp728 phải neo băm của tệp NÀY. Đây là một lượt **ĐO/AUDIT**, không phải packet code. KHÔNG cấp việc: cần Issue
> #728, lease `role: reviewer` và comment cấp quyền của chủ kho.

## Vì sao có r2

Codex Review trên PR #724 (merge `86e7858`, review trên `877e558`, 2026-10-11) nêu hai P2 trúng r1, cộng một P2 về định
tuyến áp cho cả nhóm wp725–wp728. Chủ kho quyết 2026-10-15 (phiên Claude
https://claude.ai/code/session_01EENkYtuRtrNS79zt6PTN7h):

| comment | P2 | quyết định | mục sửa ở r2 |
|---|---|---|---|
| `discussion_r4242170336` | đích đo chọn được lúc phát lượt | **neo blob OID** + luật tường minh cho SHA sau | §Đích đo, N0 |
| `discussion_r4242170331` | rig M2 không được lưu | **lưu rig + bộ sinh đột biến**, bắt chạy lại từ bản lưu | §Rig, N2, N4 |
| `discussion_r4242170329` | packet đi thẳng `master`, bỏ mission integration | **nhánh `ops/**` → PR master, khai rõ** (wp728 không có mã sản phẩm) | §Định tuyến |
| — (đo 09:09Z 15-10) | `pwsh` vắng trong container | **ghim PowerShell 7.4.6 tarball** | §Môi trường, N0 |

Trước khi đóng băng, r2 đã qua một lượt cross-review độc lập (Codex, trên `4c9981f`, 09:42Z 15-10: 4 P2 + 3 P3 về
chính văn bản này) và được sửa NGAY trong PR #755 vì băm r2 chưa neo vào lease nào: F01 byte thực thi phải là blob đã
neo; F02 ghim runtime `pwsh` chứ không chỉ archive; F03 hợp đồng quan sát của rig; F04 mức bằng chứng assurance; F05 số
lịch sử không có thời điểm đo; F06 lời khai "không commit nào chạm" quá rộng; F07 tập thành viên của `SHA256SUMS.txt`.

Sửa thêm một lời khai sai của r1: r1 trỏ `ops/reviews/wp710-g5-luot-9/VERDICT.md` — tệp ấy KHÔNG có trên master. Nguồn
đúng là `ops/reviews/wp710-exec-review-9-codex-verdict.md` dòng 22 và 56 (đo 09:12Z 15-10).

## Định danh

- `packet_id`: `wp728` · `packet_issue`: 728 · `revision`: 2.
- `nguon_cap_viec`: Issue #728; packet cha WP710 — `ops/reviews/wp710-exec-review-9-codex-verdict.md` dòng 22
  (`linux-subreaper-khong-thu-hoi-zombie` — "CHƯA VÁ trong delta; việc đóng KHÔNG ĐO ĐƯỢC") và dòng 56 (Linux "KHÔNG ĐO
  ĐƯỢC độc lập"; WSL `Wsl/Service/E_ACCESSDENIED`).
- `review_class`: **sensitive** — đo hành vi giết/thu hồi tiến trình của wrapper credential (§8: "launcher hoặc gate
  lifecycle", "credential boundary"). Không rõ ⇒ mức chặt nhất.
- **Bên đo phải khác Executor.** Executor g5 của WP710 khai `claude` (`ops/leases/wp710-r4-g5-claude-windows.yaml`,
  `provider: anthropic_claude`) ⇒ bên đo: **`codex` trên phiên cloud Linux**; dự phòng **human audit**.
- **Assurance — đích, không phải lời khai đã đạt.** Nhãn đích là `cross_approved`, nhưng bằng chứng họ model hiện có KHÔNG
  đạt mức `do_may`: `run.json` của `.claude/dev/launcher.py` ghi provider/transport suy từ tên tệp chạy và băm log, không
  đọc model thực phục vụ lượt (cross-review #755 F04, đo trên `4c9981f`); lease WP710 cũng chỉ là lời khai Executor. Vì
  vậy biên nhận phải ghi mức bằng chứng họ model đúng như có (`khai_co_audit` nếu chủ kho audit, ngược lại
  `khong_do_duoc`) và KHÔNG tự nâng thành `do_may`. Chủ kho đòi `do_may` ⇒ đi đường human audit độc lập.

## Đích đo — neo theo NỘI DUNG, không theo nhánh

Bất biến (đo 09:09Z 15-10, `git rev-parse <rev>:<path>`):

| tệp | blob OID đóng băng | sha256 bytes (đo trên `6f121a3`) |
|---|---|---|
| `scripts/nlm-credential-refresh.ps1` | `24240a31be4d51332f748d3fdadf3307cb6f1a88` | `33d32769897f97644985def693a6c54c70d2dc4048aed242b557cf4df1e8da5d` |
| `scripts/nlm-credential-refresh.Tests.ps1` | `4dc5994c363245219419fc0e2a20350761d6f7f1` | `7f6e56362e2bea7a2033a8995aa779f12e0141ca4e2c950401a962863a46f1a8` |

Hai OID trên **bằng nhau** tại land WP710 `8b59185975a938504de5963d2310e574dd4858b2`, tại base spec r1
`353da6b30f7e2f54a7bed92db97c0fe9ea70a21d` và tại master `6f121a3810045af27bf65eb723edf36b29e387f2`, và trên **mọi**
commit của `git rev-list --ancestry-path 8b59185..6f121a3` (104 commit, 0 lệch; so `git rev-parse <c>:<path>` từng
commit, đo 09:43Z 15-10). Bất biến này KHÔNG có nghĩa "không merge nào đưa hai tệp vào": `git log` mặc định rỗng là do
history simplification; một số merge (vd. `bcab7330`) có thêm hai blob ấy so với parent kia — tức chỉ truyền đúng nội
dung WP710, không sửa nó.

**Luật chấp nhận SHA đo (tường minh):** `reviewed_sha` hợp lệ khi và chỉ khi CẢ BA đúng —
(a) `git merge-base --is-ancestor 8b59185975a938504de5963d2310e574dd4858b2 <reviewed_sha>` rc 0;
(b) `git rev-parse <reviewed_sha>:scripts/nlm-credential-refresh.ps1` = `24240a31…`;
(c) `git rev-parse <reviewed_sha>:scripts/nlm-credential-refresh.Tests.ps1` = `4dc5994c…`.
Ba trạng thái: đạt · không đạt · **KHÔNG ĐO ĐƯỢC** (lệnh git lỗi, ref không có cục bộ, đường dẫn không có trong tree) —
hai trạng thái sau đều DỪNG lượt trước M1.

**Byte THỰC THI phải là chính hai blob ấy** (cross-review #755 F01 — kiểm object Git không ràng buộc tệp được mở để chạy;
smudge/attributes hay một bản sao lạc có thể khác blob). Quy trình bắt buộc: xuất bằng `git cat-file blob
<reviewed_sha>:<path>` (KHÔNG qua checkout/filter) vào MỘT thư mục scratch riêng, giữ đúng tên tệp cạnh nhau
(`Tests.ps1` chỉ tham chiếu `$PSScriptRoot/nlm-credential-refresh.ps1`); băm sha256 byte thô của hai tệp xuất ra và so
với cột sha256 ở bảng trên; M1, M2 và đầu vào của `mutate.py` đều dùng CHÍNH hai tệp đã băm ấy, không đường dẫn nào khác.
Lệch ⇒ DỪNG trước M1. Một commit sau đổi một trong hai blob thì lượt đo KHÔNG được chạy trên commit ấy: phải ra r3. `reviewed_sha`
được ghi vào lease TRƯỚC khi phát lượt và lặp lại trong biên nhận.

## Môi trường

- PowerShell: **7.4.6**, tarball `powershell-7.4.6-linux-x64.tar.gz` từ
  `https://github.com/PowerShell/PowerShell/releases/download/v7.4.6/`, **71645796 byte, sha256
  `6f6015203c47806c5cc444c19d8ed019695e610fbd948154264bf9ca8e157561`** (phiên điều phối tải và đo 09:15Z 15-10; đây là
  bản ĐÃ ĐẾN, chưa đối chiếu với giá trị nhà phát hành công bố — ghi đúng như thế). Giải nén vào thư mục tạm NGOÀI
  checkout; không cài vào hệ thống. Lệch sha256 ⇒ DỪNG.
- **Ghim runtime, không chỉ ghim archive** (cross-review #755 F02 — `Tests.ps1` gọi `pwsh` TRẦN ở dòng 226, 244 và
  `Get-Command pwsh` ở 294, 1003, nên tiến trình con có thể chọn `pwsh` khác). Thư mục giải nén đặt ĐẦU `PATH` cho toàn bộ
  suite và rig; preflight đòi: `command -v pwsh` trỏ vào chính thư mục ấy, `pwsh -NoProfile -c
  '$PSVersionTable.PSVersion.ToString()'` in đúng `7.4.6`, và `type -a pwsh` không còn `pwsh` nào khác đứng trước. Ghi đường
  dẫn đã resolve và phiên bản vào biên nhận và `REPLAY.md`.
- Container cloud Linux (đo 09:09Z 15-10): không có `pwsh`; có `python3` 3.13.16; `codex-cli` 0.162.1. Shim `python`
  (vì `Tests.ps1:213` gọi `Get-Command python`) đặt trong thư mục PATH tạm và ghi vào biên nhận.
- Tiền điều kiện credential: bản `CODEX_AUTH_JSON` trong container là ảnh chụp cũ **122,1 h** (`last_refresh`
  2026-10-10T07:00:29Z, `doctor` đo 09:05Z 15-10, nhãn `SAP_HET_HAN`) — refresh token có thể đã bị vô hiệu. Làm mới
  (`codex login --device-auth` hoặc chép lại base64 NGAY sau login) TRƯỚC khi phát lượt, rồi `doctor --kiem-song`.
- Không LIVE, không `nlm` thật, không credential thật, không Drive. Fake CLI của bộ test là đủ.

## Rig — do phiên điều phối dựng, LƯU vào kho, reviewer CHẠY LẠI

Phân công theo bài học CLAUDE.md "REVIEWER BỊ CHẶN": reviewer không tự soạn nội dung điều khiển tiến trình. Phiên điều
phối dựng ba tệp dưới đây TRƯỚC khi phát lượt; reviewer chỉ chạy và đột biến.

- `ops/reviews/wp728-do-linux/rig/zombie_rig.py` — chạy wrapper (đường dẫn truyền vào làm đối số) với fake CLI của bộ
  test ở chế độ `daemon`, `-EnableKeepalive -MaxCycles 5 -IntervalSeconds 10`. `-MaxCycles 5` cho **4 khoảng nghỉ**
  (wrapper chỉ ngủ khi `cycle > 0`, `nlm-credential-refresh.ps1:1016`; không có khoảng sau chu kỳ cuối) — "khoảng" ở
  đây đếm KHOẢNG NGHỈ, không đếm dòng kết quả. Hợp đồng quan sát (cross-review #755 F03):
  - mỗi khoảng chỉ lấy mẫu sau khi đọc được sự kiện `staged` của chu kỳ trước và xong trước nửa khoảng (≤ 5 s);
  - mỗi mẫu ghi: số thứ tự khoảng, thời điểm, pid + starttime của wrapper (đọc `/proc/<pid>/stat`, trường 22) và việc
    wrapper còn sống; pid + starttime của con fixture lấy từ `WP714_CHILD_PID_FILE` (cùng cơ chế ca `v`,
    `Tests.ps1:1011`); số tiến trình `Z` có ppid = pid wrapper VÀ starttime ≥ starttime wrapper; tách riêng số zombie
    là con fixture với tổng con `Z`;
  - một dòng JSON mỗi khoảng và một dòng tổng kết; thời hạn cứng cho cả lượt.
  Bất kỳ điều nào sau đây ⇒ lượt ấy là **KHÔNG ĐO ĐƯỢC** (không phải đạt): thiếu mẫu của một khoảng, mẫu rơi sang chu kỳ
  kế, wrapper thoát sớm hoặc đổi starttime (pid tái dùng), fixture không sinh con, `/proc` đọc lỗi, quá thời hạn.
  Chỉ đường dẫn TƯƠNG ĐỐI hoặc `$TMPDIR`; không đọc biến môi trường ngoài danh sách cho phép (`PATH`, `TMPDIR`,
  `HOME` tạm, `WP714_*` của fixture); không ghi đường dẫn máy vào đầu ra.
- `ops/reviews/wp728-do-linux/rig/mutate.py` — bộ sinh đột biến TẤT ĐỊNH: đọc wrapper, đòi dòng
  `        if ($inRun) { [void](Invoke-ReapAdopted $direct) }` xuất hiện **đúng 1 lần** (đo: dòng 494), thay bằng
  `        if ($inRun) { }`, ghi ra tệp tạm, in sha256 bản đột biến. Khớp ≠ 1 ⇒ rc ≠ 0, không ghi gì.
- `ops/reviews/wp728-do-linux/rig/REPLAY.md` — đúng chuỗi lệnh chạy lại nền và đột biến từ CHÍNH các tệp đã lưu.

## Phép đo

- **M1 — suite.** `pwsh -NoProfile -File scripts/nlm-credential-refresh.Tests.ps1` trên Linux. Ghi
  `$PSVersionTable.PSVersion`, `python --version`, `python3 --version`, `uname -r`, rc, dòng tổng kết nguyên văn.
- **M2 — zombie nhiều chu kỳ.** Ca `v` (`Tests.ps1:991–1027`) chỉ kiểm sau chu kỳ đầu; lời khai "4 chu kỳ, 0 zombie"
  (Executor WP710; thời điểm đo gốc: KHÔNG ĐO ĐƯỢC) của
  `changelog.d/wp-710.md:38` đến từ rig không có trong kho. Chạy `zombie_rig.py` trên wrapper NGUYÊN VẸN (byte đã băm
  ở N0), `-MaxCycles 5` ⇒ 4 khoảng nghỉ.
- **M2' — phản chứng bắt buộc.** `mutate.py` trên chính tệp đã băm ở N0 → bản sao tạm → cùng rig, cùng tham số.
- **M3 — đồng hồ (ghi nhận, không đóng lớp).** Hai pwsh (một sống ≥ 250 s, một mới) cùng đọc mốc khởi động của CÙNG
  một PID; ghi công thức, đơn vị, nguồn đồng hồ và tuổi pwsh sống; không lấy chênh starttime của hai tiến trình khác nhau
  làm độ lệch. Đối chiếu lời khai 2,9 s/130 s và 7,0 s/256 s trên WSL (lời khai Executor WP710; thời điểm đo gốc: KHÔNG
  ĐO ĐƯỢC). Không sửa.
- **Parity 101 dạng / 168 chuỗi byte (lời khai Executor WP710; thời điểm đo gốc: KHÔNG ĐO ĐƯỢC) — KHÔNG đo lại.** Script so không có trong kho; biên nhận ghi đúng câu: "parity
  101/168: KHÔNG TÁI LẬP ĐƯỢC từ kho; không đo".

## write_set (exact — chỉ biên nhận, KHÔNG mã sản phẩm)

| đường dẫn | ai ghi |
|---|---|
| `ops/reviews/wp728-do-linux/rig/zombie_rig.py` | phiên điều phối, TRƯỚC lượt đo |
| `ops/reviews/wp728-do-linux/rig/mutate.py` | phiên điều phối, TRƯỚC lượt đo |
| `ops/reviews/wp728-do-linux/rig/REPLAY.md` | phiên điều phối, TRƯỚC lượt đo |
| `ops/reviews/wp728-do-linux/VERDICT.md` | reviewer viết; phiên điều phối chép nguyên byte vào kho |
| `ops/reviews/wp728-do-linux/run.json` | launcher |
| `ops/reviews/wp728-do-linux/SHA256SUMS.txt` | phiên điều phối |
| `ops/reviews/wp728-do-linux/.gitattributes` | phiên điều phối (`* -text`, bài học CRLF hồ sơ g5) |

## ngoai_pham_vi

- Sửa `scripts/nlm-credential-refresh.ps1` / `.Tests.ps1` — lượt này chỉ đo. Phát hiện lỗi thì mở packet riêng.
- Parity 101/168 (lý do ở M-parity). Hành vi trên WSL của máy chủ kho (rig khác cloud Linux).
- `nlm` CLI và trình duyệt thật; LIVE; Drive; deploy.

## Định tuyến

wp728 không có mã sản phẩm nên **không** đi `mission/<issue>/integration`: biên nhận được phiên điều phối đẩy lên một
nhánh `ops/wp728-*` rồi mở PR bookkeeping vào `master`, theo tiền lệ `ops/reviews/**`. Reviewer read-only, không đẩy.
Đây là quyết định chủ kho 2026-10-15 cho riêng wp728; KHÔNG phải ngoại lệ hồi tố cho wp725–wp727 (câu hỏi định tuyến của
ba packet đã land ấy được trả lời riêng trên PR #724).

## muc_tieu

1. Rig + bộ sinh đột biến có trong kho trước lượt đo → `rig/zombie_rig.py`, `rig/mutate.py`, `rig/REPLAY.md`.
2. Kết quả M1/M2/M2'/M3 có lệnh, rc, đầu ra nguyên văn → `VERDICT.md`, `run.json`.
3. Bằng chứng toàn vẹn của mọi tệp đầu ra (trừ chính tệp băm) → `SHA256SUMS.txt`, `.gitattributes`.

## nghiem_thu (mỗi tiêu chí kèm phép đo làm nó ĐỎ)

- **N0 — preflight.** Đạt khi CẢ BỐN đúng: luật chấp nhận SHA (a)(b)(c); sha256 byte thô của hai tệp xuất bằng `git
  cat-file blob` khớp bảng; sha256 tarball khớp; runtime `pwsh` resolve đúng thư mục giải nén và in `7.4.6`. ĐỎ (dừng
  TRƯỚC M1) với từng phản chứng: (i) `reviewed_sha` hợp lệ nhưng tệp đem chạy khác một byte; (ii) ref không có cục bộ
  hoặc đường dẫn bị đổi tên ⇒ KHÔNG ĐO ĐƯỢC; (iii) tarball lệch một byte; (iv) `PATH` đặt một `pwsh` khác lên trước.
- **N1 — M1.** `failed=0` VÀ `passed` = số ca thực chạy trên Linux (đếm ca đã thực thi, không tin con số 34 của
  Executor — con số ấy cũng không có thời điểm đo gốc). ĐỎ khi bất kỳ ca nào fail, hoặc `passed` < số ca thực thi.
- **N2 — M2 có răng.** Nền: cả 4 khoảng nghỉ có mẫu hợp lệ theo hợp đồng quan sát VÀ 0 zombie fixture ở mọi khoảng.
  Đột biến M2': số zombie fixture TĂNG qua các khoảng. ĐỎ khi nền có ≥ 1 zombie fixture ở một khoảng bất kỳ. Thiếu mẫu /
  wrapper thoát sớm / pid tái dùng / fixture không sinh con / `/proc` lỗi ⇒ **KHÔNG ĐO ĐƯỢC**. M2' KHÔNG tăng ⇒ rig không
  có răng ⇒ M2 = **KHÔNG ĐO ĐƯỢC** (không phải đạt).
- **N3 — M3.** Có con số độ lệch đo trên CÙNG một PID, kèm công thức, đơn vị, nguồn đồng hồ, tuổi pwsh sống. Không
  đóng/không mở lớp nào; ĐỎ khi thiếu số hoặc thiếu một trong các điều kiện ấy.
- **N4 — tái lập.** `REPLAY.md` chạy lại từ chính các tệp trong `rig/` cho cùng kết luận nền/đột biến; sha256 bản đột
  biến do `mutate.py` in ra trùng giữa hai lần chạy. ĐỎ khi: kết luận đổi giữa hai lần, hoặc `mutate.py` khớp ≠ 1 dòng,
  hoặc `SHA256SUMS.txt` sai. Tập thành viên của `SHA256SUMS.txt` (cross-review #755 F07): MỌI tệp dưới
  `ops/reviews/wp728-do-linux/` (đệ quy, gồm `rig/`) TRỪ chính `SHA256SUMS.txt`; lập SAU KHI `VERDICT.md` và `run.json`
  đã ở bản cuối. ĐỎ khi một tệp trong danh sách lệch băm, hoặc có tệp trong thư mục không nằm trong danh sách.
- **Kết luận lớp** `linux-subreaper-khong-thu-hoi-zombie`: `đóng` chỉ khi N0, N1, N2, N4 cùng đạt; ngược lại giữ mở và
  nêu đúng cái thiếu.

## hinh_dang_ke_thua

Không phải packet khắc phục mã ⇒ không có bộ đếm hình dạng lỗi để chép. Ghi nhận từ WP710 lượt 9: lớp
`linux-subreaper-khong-thu-hoi-zombie` mang trạng thái "CHƯA VÁ trong delta; việc đóng KHÔNG ĐO ĐƯỢC" (P2 lịch sử thiếu
đo) — wp728 chỉ đổi được trạng thái "đo" của lớp, không đếm thêm hình dạng.

## chua_do_duoc

- Hành vi trên WSL của máy chủ kho; kết quả cloud Linux không chứng minh WSL và ngược lại.
- `nlm` CLI và trình duyệt thật.
- Giá trị sha256 nhà phát hành công bố cho tarball pwsh 7.4.6 (chỉ có sha256 bản đã đến).
- Credential codex: đã làm mới bằng `codex login --device-auth` lúc 09:28Z 15-10 trong container phiên điều phối,
  `doctor --kiem-song` rc=0 (09:29Z); container khác KHÔNG kế thừa — đo lại khi phát lượt.
- Họ model thực phục vụ lượt đo (xem mục Assurance): launcher không đo được.
