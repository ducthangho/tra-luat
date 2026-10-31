# Handoff wp1021 g1 — executor `claude` (phiên cloud), 30-10-2026

- Packet #1021 `BIEN-NHAN-V2-GLOB-HOA-THUONG` r2 · lease `ops/leases/wp1021-r2-g1-claude.yaml` @ `c91c1c1` (nhánh
  `ops/wp1021-r2-g1-lease`) · đặc tả `ops/specs/BIEN-NHAN-V2-GLOB-HOA-THUONG-r2.md` sha256
  `d5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d`.
- Nhánh code `agent/wp1021-g1-claude`, head cuối **`e9e0048b48ab610fee1246368b4f134c1ac4ae76`** (base `757bde5`). PR draft #1040.
- Không merge/land/deploy (`uy_quyen_merge: false`). Không force-push, không rebase, không xoá ref.
- Tệp này nằm trên nhánh lease, KHÔNG trên nhánh code, để head mà Codex đã duyệt không đổi.

## Lịch sử nhánh code
| commit | nội dung |
|---|---|
| `99c463d` | M1/M2: helper `_chon_bien_nhan` (iterdir + so đuôi `.lower()`, không lọc `is_file`) thay hai chỗ glob ở `kiem()`/`_sinh_no()`; ca `c98`; đột biến `m142`, `m143` |
| `5efa311` | vá Codex lượt 1: lỗi liệt kê ⇒ `KhongDoDuoc` (rc=2); ca `c99`; đột biến `m144`–`m147` |
| `8d9e3e3` | vá Codex lượt 2: `_hoi_trang_thai` (lỗi `stat` của `is_dir`/`.git exists` ⇒ rc=2, chỉ `OSError`); ca `c100`; đột biến `m148`–`m153` |
| `e9e0048` | vá Codex lượt 3 (chỉ tệp test): tiêm thêm `OSError(EIO)` cạnh `PermissionError`; đột biến `m154`, `m155` |

Diff so base: `ops/bien_nhan_v2.py` +40/−5 · `ops/bien_nhan_v2_test.py` +283/−0. Đúng hai tệp write set.

## Tiêu chí — đo trên đúng `e9e0048`
- **Suite Linux (phiên này)** `python ops/bien_nhan_v2_test.py`: `97/97 ca đạt · 151/151 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM
  đạt` · `TỔNG: ĐẠT` · rc=0.
- **C6** `python ops/bien_nhan_v2.py --root .`: `tổng 306` · `TỔNG: ĐẠT` (nền lease = 306). `--sinh-no`: `# 42 tệp`.
- **C1a/C1b/C2/C3/C9**: Codex lượt 4 đo độc lập, ĐẠT (C3 = hoàn nguyên glob ⇒ `c98` giết thật trên Linux; không vào bảng thường vì
  sống trên Windows). `rg 'glob\("\*\.receipt\.yaml"\)' ops/bien_nhan_v2.py` ⇒ 0 dòng. ruff `--select F` delta 0 (F541 sẵn có ở
  test, dời 1677 → 1678 vì thêm một dòng import). `doctrine-scan` sạch. `git diff --check` rc0.
- **M-2 Ubuntu** — run PR [41053943431](https://github.com/ducthangho/tra-luat/actions/runs/41053943431) `success`, mọi job nhãn
  `ubuntu-latest`, runner_id ≠ 0. Job `gate-ops (ubuntu-latest)` 124056817696: `bien_nhan_v2_test: 97/97 ca đạt · 151/151 đột biến
  thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt` · `TỔNG: ĐẠT`; `lease_publish: 268/268 đạt; đã chạy=268, bỏ qua=0`.
- **M-2 Windows** — dispatch `runner_set=windows-only` [41053942887](https://github.com/ducthangho/tra-luat/actions/runs/41053942887)
  `success`. Job `gate-ops (windows-latest)` 124057167797 (nhãn `windows-latest`, runner_id 1000026012): `bien_nhan_v2_test: 97/97
  ca đạt · 151/151 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt` · `TỔNG: ĐẠT`; `lease_publish: 255/255 đạt; đã chạy=255, bỏ
  qua=13` (13 ca bỏ qua có khai báo, giống run Windows trên `dbbabf9` trước packet).
- **M-4 / C7 (Windows local)**: **ĐẠT, local** — ASUS-LAPTOP, theo ADR-0057/0058, đúng `e9e0048`.
  · Lượt 1: 14:04Z `list_devices` `Online`; `D:\tl-win\KHOA.txt` rỗng ⇒ ghi khoá `session_015GtxrZ1Tt93F4NLUUhKYQy` 14:05:00Z
    hạn 16:05:00Z; kiểm tải: 4 `python.exe` không phải test (2 `browser-use --cli-mcp`, 2 `proxima_agent.web`), không đụng tới.
    Clone riêng `D:\tl-win\session_015GtxrZ1Tt93F4NLUUhKYQy` ở `e9e0048`, sạch, không nông, `core.abbrev 7`. Máy rời mạng
    ~14:16Z (14:36Z `Offline`), lượt bị cắt ở ca `c13`, không còn tiến trình test.
  · Lượt 2: máy `Online` lại 15:25Z; khoá vẫn của phiên này ⇒ gia hạn 15:26:48Z → 17:26:48Z; chạy lại từ đầu trong tiến trình
    tách (`Start-Process`), lệnh `python -u ops\bien_nhan_v2_test.py` với `PYTHONUTF8=1 PYTHONIOENCODING=utf-8
    PYTHONDONTWRITEBYTECODE=1`, log `D:\tl-win\session_015GtxrZ1Tt93F4NLUUhKYQy-head2.log`. Kết quả nguyên văn:
    `bien_nhan_v2_test: 97/97 ca đạt · 151/151 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 133/151 đột biến thường khai đối
    chứng` · `TỔNG: ĐẠT` · `rc=0 s=2625`. `m142`–`m155` đều `CÓ RĂNG … giet_that` đúng ca đích.
  · Không có lỗi local ⇒ không có gì phải vá (ADR-0057 §2). Đã ghi một dòng `do-luong.csv` (16:13:56Z, `may=ASUS-LAPTOP`) và xoá
    nội dung khoá. Lượt local KHÔNG phải check run, không thay bằng chứng Windows CI ở trên.

## Cross-review Codex — 4/4 lời gọi (trần spec r2 / lease M-1)
Qua `.claude/dev/launcher.py run --require-clean --expected-head …`, lệnh `codex exec -m gpt-6-astra -c
model_reasoning_effort="xhigh" --sandbox workspace-write`. `stderr.log` của cả bốn lượt KHÔNG in header model/effort, nên model và
cường độ ở đây là GIÁ TRỊ YÊU CẦU, chưa có xác nhận từ phía chạy. Sandbox: clone thường detached + SPEC + diff + verdict lượt trước.

| lượt | run_id | prompt sha256 | head | thời lượng | verdict | VERDICT.md sha256 |
|---|---|---|---|---|---|---|
| 1 | `fe55b319aa1843f0a671fccdabc58f91` | `f333893e…4c093c` | `99c463d` | 1216,3 s, rc0 | request_changes (2 P2) | `2b624947…20fdf4` |
| 2 | `8032f63d163a457192419ffea4cdb81a` | `16e81a25…924d13` | `5efa311` | 831,5 s, rc0 | request_changes (1 P2, 1 P3) | `68b2cbe6…3827fd` |
| 3 | `af505919a7a94adba8804d9589b0339d` | `d7f60694…659e2e` | `8d9e3e3` | 899,0 s, rc0 | request_changes (1 P3) | `4c786b0d…b388b` |
| 4 | `970e84dbe41d44b2ab346259c53bc519` | `1006b62e…78ce159` | `e9e0048` | 602,5 s, rc0 | **approve**, 0 P0–P3 mở | `076ef6c8…af78482` |

Finding và cách xử lý (mọi finding mang HÌNH DẠNG `loi-do`; KHÔNG có finding `bo-chon-ung-vien` nào sau lượt 1):
- L1 P2 `loi-do-liet-ke-thu-muc-thoat-traceback`: `iterdir()` ném `EACCES` ⇒ rc=1 + traceback (glob cũ nuốt lỗi). Vá ở `5efa311`.
- L1 P2 `bo-chon-ung-vien-thieu-rang-hai-duong-goi`: ba đột biến (lọc đuôi chính xác ở `--sinh-no`, bỏ `sorted`, bỏ nhánh thư mục
  vắng) sống qua suite. Đây là hình dạng chốt dừng của spec ⇒ DỪNG hỏi chủ kho; chủ kho duyệt làm tiếp 30-10-2026. Vá ở `5efa311`.
- L2 P2 cùng slug, biểu hiện thứ hai: `Path.is_dir()` chỉ nuốt ENOENT/ENOTDIR, `EACCES` ở `stat` vẫn ném ⇒ `--sinh-no` rc=1 +
  traceback (base rc=0, tức hồi quy của packet). Vá ở `8d9e3e3`; Codex lượt 3 kiểm thêm toàn bộ bảng lời gọi hệ tệp trên hai đường.
- L2 P3 `loi-do-thieu-chot-ngoai-le-lap-trinh`: chưa ca nào đòi lỗi lập trình đi thẳng ra. Vá ở `8d9e3e3` (`c100` chốt 7).
- L3 P3 `loi-do-thieu-chot-oserror-ngoai-permissionerror`: thu hẹp phép bắt về `PermissionError` sống. Vá ở `e9e0048`.
- L4: cả ba lớp đóng; không finding mới. Hai đột biến sống mà Codex tự dựng ở lượt 4 được nó phân loại tương đương (đảo thứ tự
  factory) hoặc bị bảng đột biến bắt (đổi EIO → EACCES làm `m154`/`m155` mất răng).

**Nơi lưu verdict**: nguyên văn bốn tệp `VERDICT.md` nằm ở **Phụ lục A** cuối tệp này (chép byte-exact bằng script; băm
sha256 ở bảng trên là băm của tệp gốc, đo lại được bằng cách cắt phần giữa hai dấu `<!-- VERDICT-Ln-BAT-DAU -->` /
`<!-- VERDICT-Ln-KET-THUC -->` — phần ấy không gồm dòng trống bao quanh). Bằng chứng phụ của reviewer (log, script dò) KHÔNG được
lưu. `ops/reviews/**` không thuộc write set nên executor KHÔNG ghi biên nhận v2 vào kho; nếu cổng land cần biên nhận trong
`ops/reviews/`, việc ấy cần lease/thẩm quyền riêng.

## Quan sát khác (ghi, KHÔNG vá)
- Clone của container mở ra nông; phải `fetch --unshallow` trước khi chạy `bien_nhan_v2.py --root .` (nông ⇒ rc=2).
- Codex lượt 3 liệt kê hai lỗi `resolve` (đường dẫn module provider; `--root` trong `main`) thoát traceback khi tiêm `OSError` — có
  sẵn ở base, ngoài write set, không tính finding của packet.
- `gate lifecycle tests` trên Windows in `16/28 ca QUA (bo qua 12, hong 0) - KHONG DU` trong bước "nền không có cgroup"; job vẫn
  `success`. Không thuộc packet này, chưa đối chiếu với master.

## Việc còn lại (không phải của executor)
- Merge/land: chủ kho.
- Biên nhận review trong `ops/reviews/` (nếu cổng land đòi): ngoài write set.


## Cập nhật 31-10-2026 — Codex lượt 8 và 9 trên `356a27e`: APPROVE (đọc phần này TRƯỚC mọi mục khác)

Phiên `session_015GtxrbRjCRMMLRWHoUuZYj`. Head không đổi: **`356a27e1378b2162bbc0be2ec06ff08fdacbdead`**. Không sửa mã.
Trần Codex 9 (Issue #1021 issuecomment-6531357709). **ĐÍNH CHÍNH (05:40Z): thực tế đã dùng 10 lời gọi — VƯỢT trần một.**
Phiên điều phối cũng chạy một lượt "8/9" trên đúng `356a27e` (run `e8bb597dcf5c44cca3228093286661ed`, 549,5 s, approve, 0 P0–P3;
prompt `55fa2adb…829ada`, VERDICT.md `27cea768…85fbffe`, 20114 byte — số liệu chép từ PR #1040 issuecomment-6538420022, phiên này
KHÔNG tự đo). Phiên này (`session_015GtxrbRjCRMMLRWHoUuZYj`) chạy lượt 8 lúc 03:12Z mà không biết lượt kia, rồi lượt 9 sau khi lượt 8 của
mình bị chặn; không kiểm comment PR trước khi gọi. Hai phiên chạy song song, không phiên nào biết phiên kia ⇒ đúng ca "hai writer" mà
lease sinh ra để chặn, ở đây là hai người tiêu cùng một ngân sách lời gọi. Ba verdict trên `356a27e` đều 0 P0–P3 (hai approve).
Chốt cho lần sau: trước MỖI lời gọi Codex, đọc comment PR + Issue để đếm lời gọi của MỌI phiên, không chỉ của mình.

**PR #1040 và nhánh code (đo 05:40Z).** PR tự đóng lúc 03:22Z (không merge) vì nhánh `agent/wp1021-g1-claude` bị xoá; review connector
lúc 03:30Z neo `b29da0b` (head sau khi nhánh bị đặt lại), KHÔNG phải `356a27e`. Phiên `session_015GtxrZ1Tt93F4NLUUhKYQy` theo chỉ thị chủ
kho đã dựng lại nhánh = `356a27e` từ tag `luu-tru/wp1021-g1-claude` (không thêm commit), mở lại PR ~05:36Z, chuyển ready; `get` PR lúc
05:40Z: `open`, `draft=false`, head `356a27e`, `mergeable_state=blocked` (chờ CI/connector trên head mới mở lại).

Cả hai lượt qua `.claude/dev/launcher.py run --require-clean --expected-head 356a27e…`, lệnh `codex exec -m gpt-6-astra -c
model_reasoning_effort="xhigh" --sandbox workspace-write`; `run.json` ghi `model_phuc_vu_trang_thai=DO_DUOC` (mọi
`response.created` đều `gpt-6-astra`) và `effort_phuc_vu=["xhigh"]` `DO_DUOC` — lần này model/effort là ĐO ĐƯỢC, không chỉ yêu cầu.
Prompt lượt 8 soạn lại (bản `e6fdd2c0…` của phiên trước nằm trong container cũ, đã mất).

| lượt | run_id | prompt sha256 | head | thời lượng | verdict | VERDICT.md sha256 |
|---|---|---|---|---|---|---|
| 8 | `2bc4a8762172489490fcf1c8fd54b625` | `8cc4055e…e3e7cc7` | `356a27e` | 893,4 s, rc0 | request_changes — **0 P0–P3 mở**; chặn bởi trở ngại snapshot (dưới) | `bd891b29…8b6ece` |
| 9 | `629cf3361f294f8aa9eea40043e36a12` | `0fa9975d…4e9ba0` | `356a27e` | 563,5 s, rc0 | **approve**, 0 P0–P3 mở | `8af135fc…410252` |

**Lượt 8 — trở ngại do executor dựng sandbox sai, không phải lỗi mã.** Clone sandbox chỉ có `master` + nhánh code, thiếu commit
`4bc94325e647ee5e32373f3af30b8f83b98a90fa` mà `ops/reviews/lease-publish-windows-do-review-r1-codex.receipt.yaml` tham chiếu (commit
chỉ nằm trên tag `luu-tru/lease-publish-windows-do-r1-verdict` và nhánh `ops/do-lease-publish-windows-150`). Hệ quả: C6 rc=2
`3 KHÔNG ĐO ĐƯỢC`, suite 95/98 (c14, c40, c76). Codex chạy mã base trên cùng dữ liệu và ra đỏ y hệt, nên đây là lỗi của sandbox.
Ngoài trở ngại ấy: P3 lượt 7 ĐÃ VÁ THẬT, mọi lớp cũ vẫn đóng, 16/16 đột biến m142–m157 giết đúng ca đích.
Bài học (cùng họ "`for-each-ref` đọc bộ đệm cục bộ" trong CLAUDE.md): sandbox review cho `bien_nhan_v2` phải có **mọi nhánh + mọi tag**,
vì receipt tham chiếu commit chỉ còn sống trên ref lưu trữ.

**Lượt 9** — clone mới có đủ nhánh (so tập tên với `ls-remote`: thiếu 0) và 75 tag, cùng HEAD/tree `c1e160cf…`. Executor tự đo trước khi
gọi: C6 `0 KHÔNG ĐO ĐƯỢC · tổng 306 · TỔNG: ĐẠT` rc0; suite `98/98 · 153/153 · 2/2 · TỔNG: ĐẠT` rc0. Codex đo độc lập: C6 như trên,
đếm riêng 306; suite **98/98 · 153/153 · 2/2**, `TỔNG: ĐẠT` (339,8 s), c14/c40/c76 ĐẠT; 16/16 đột biến riêng `giet_that` đúng ca,
đối chứng sạch; ruff F delta 0 (F541 sẵn có); doctrine-scan sạch; snapshot nguồn đầu = cuối.
CI đọc độc lập qua API thô: Windows run 41113949578 / job 124263645262 — `workflow_dispatch`, head đúng, labels `windows-latest`,
runner_id 1000026867, `98/98 · 153/153 · 2/2`, lease 255/255 (bỏ qua 13); Ubuntu run 41113943723 / job 124264022785 — `pull_request`,
head_sha đúng, labels `ubuntu-latest`, runner_id 1000026883 (checkout merge thử `00c58bc`), `98/98 · 153/153 · 2/2`, lease 268/268.
Giới hạn Codex khai: input `runner_set` của dispatch không có trong JSON run (suy từ workflow + 16/16 job Windows); C7 không đo.

Nguyên văn hai verdict ở **Phụ lục A** (lượt 8, 9), cùng quy ước cắt giữa hai dấu như lượt 1–7 (phần giữa + một `\n` cuối = tệp gốc).

**C7 — CẬP NHẬT 31-10 ~10:03Z, SAU KHI CẤP QUYỀN SYMLINK (đọc trước đoạn "KẾT QUẢ" ngay dưới; đoạn ấy là lượt TRƯỚC khi cấp quyền).**
Chủ kho duyệt cấp quyền. Cách làm: `gcloud` trên ASUS-LAPTOP (tài khoản chủ kho) thêm TẠM khoá metadata `windows-startup-script-cmd` gọi
`C:\tl-win\cap-quyen-symlink.ps1` (sha256 `3F25C86F…2E5926`, `secedit` thêm `SeCreateSymbolicLinkPrivilege` cho `tra-luat-win\tlcommander`,
chạy dưới SYSTEM lúc khởi động); khoá `windows-startup-script-ps1` (bootstrap của chủ kho) KHÔNG đụng. Trước khi tắt VM: đợi gate của một phiên
khác (`C:\work\tra-luat-agent\gate-3dfb973`, 07:58Z→08:12:22Z, KHÔNG ghi `KHOA.txt`) xong, rồi ghi khoá 08:16:20Z. Tắt êm `stop`/`start` hai lần
(lần 1: chính sách đã áp — `SeCreateSymbolicLinkPrivilege = tlcommander,*S-1-5-32-544` — nhưng tiến trình Desktop Commander đăng nhập TRƯỚC khi
script chạy nên vẫn token cũ, `symlink_to` vẫn `WinError 1314`; lần 2, boot 08:22:02Z: `whoami /priv` có quyền, `symlink_to` ⇒ `symlink_ok True`).
Đã gỡ khoá `-cmd` (rc=0; còn `block-project-ssh-keys`, `windows-keys`, `windows-startup-script-ps1`). Quyền symlink của `tlcommander` GIỮ lâu dài.
- Toàn suite 08:24:43Z→09:45:28Z: `97/98 ca · 153/153 đột biến thường CÓ RĂNG · 2/2 TỰ KIỂM`, `TỔNG: ĐỎ`. Ca đỏ duy nhất là `c14_cli_ba_trang_thai`
  (cổng thật rc=2, `KHÔNG ĐO ĐƯỢC quan hệ tổ tiên của 669ba5866cf2… (git rc=127)`), KHÔNG phải `c91`.
- `c14` chạy ~08:45Z, CHỒNG với phép đo riêng `c91` + 8 đột biến của chính phiên này (08:36:28Z→08:56:25Z) — lỗi của executor, đúng bài học
  ADR-0057 D1. Phép đo riêng ấy: `c91` ĐẠT; m103 m105 m115 m116 m117 m118 m129 m130 đều `CÓ RĂNG … giet_that` đúng `c91` (assertion của chính
  `c91`, không còn `WinError 1314`).
- Chạy lại riêng trên VM RẢNH (09:56:43Z→~10:02Z, chỉ một tiến trình python): `669ba5866cf2` có trong clone (`cat-file` ⇒ `commit`);
  `c14` **ĐẠT**, `c91` **ĐẠT**.
- Kết luận đo được: mọi ca và mọi đột biến đều đã có lần ĐẠT trên `356a27e` ở VM có quyền symlink, nhưng **chưa có MỘT lượt toàn suite 98/98
  không chồng** — ghép hai phép đo, không phải một N/N. Muốn N/N một lượt thì chạy lại toàn suite (~80 phút trên VM) khi máy rảnh.
- Sổ đo `C:\tl-win\do-luong.csv` thêm dòng 10:02:58Z; khoá `C:\tl-win\KHOA.txt` xoá (0 byte).
- **Quyết định chủ kho (31-10, sau 10:03Z):** (a) KHÔNG cần lượt toàn suite 98/98 không chồng — chấp nhận ghép hai phép đo trên làm bằng chứng C7;
  (b) GIỮ LÂU DÀI quyền `SeCreateSymbolicLinkPrivilege` của `tra-luat-win\tlcommander` trên VM. Phiên sau dùng VM: ca cần symlink (`c91` và
  mọi ca tạo symlink) nay đo được; đừng gỡ quyền này, và đừng diễn giải `c91` đỏ trên VM thành "đỏ sẵn do môi trường" nữa.

**C7 Windows local trên `356a27e` — KẾT QUẢ (tra-luat-win): `97/98 ca · 145/153 đột biến thường CÓ RĂNG · 2/2 TỰ KIỂM`, `TỔNG: ĐỎ`.
Toàn bộ chỗ đỏ là MÔI TRƯỜNG VM, ĐỎ SẴN trên base, KHÔNG do diff #1021** (ADR-0057 §2: lỗi có sẵn trên base nêu tên kèm SHA đo nền):
- Ca đỏ duy nhất `c91_B2_MA_TRAN_nguon_hong_qua_CLI_co_va_khong_no` = `KHÔNG ĐO ĐƯỢC [tin_dung_gia]`: `OSError: [WinError 1314] A required
  privilege is not held by the client` tại `pathlib.py:1386 in symlink_to` (fixture `ops/reviews/v/run.json` → `khong-co.json`, test:3258).
  Tám đột biến đích `c91` mất răng vì cùng lỗi ấy: m103, m105, m115, m116, m117, m118, m129, m130 (đều `tin_dung_gia`, cùng `WinError 1314`).
- Nguyên nhân đo được: tài khoản chạy trên VM không có quyền tạo symlink — `whoami /priv` không liệt kê `SeCreateSymbolicLinkPrivilege`;
  `python -c "...symlink_to('x')"` trần ra cùng `WinError 1314`, rc=1.
- Đo nền: worktree `b29da0bfe3bfb7a7be69136a1c5c40f82c088a93` trên cùng VM, gọi thẳng `_chay_1(c91)` ⇒ `tin_dung_gia`, cùng `WinError 1314`.
  `c91` và m103–m130 có từ wp960 (`ae0d06c`), không nằm trong diff #1021. ASUS-LAPTOP lượt `e9e0048` và Windows CI đều cho `c91` ĐẠT
  (máy có quyền symlink) — tức đây là thuộc tính của VM `tra-luat-win`, không phải của mã.
- Mọi ca/đột biến của #1021 trên VM: `c88`, `c89`, `c99`, `c100`, `c101` ĐẠT; m142–m157 đều `CÓ RĂNG … giet_that` đúng ca đích.
- Thời lượng 3828 s (04:57:01Z → 06:00:48Z theo `LastWriteTime` của log; dòng `rc=` không được ghi vì lệnh nối của tiến trình tách hỏng —
  lỗi quoting của executor, không ảnh hưởng nội dung log). Sổ đo `C:\tl-win\do-luong.csv` đã thêm một dòng (06:06:24Z, `may=tra-luat-win`,
  `loi_that=khong`); khoá `C:\tl-win\KHOA.txt` đã xoá (0 byte, 06:07Z).
- Hệ quả cho điều kiện merge: VM `tra-luat-win` hiện KHÔNG đo được `c91` ⇒ muốn có N/N local đầy đủ trên `356a27e` cần máy có quyền symlink
  (ASUS-LAPTOP, hoặc bật Developer Mode / cấp `SeCreateSymbolicLinkPrivilege` cho tài khoản VM — việc của chủ kho).
Chi tiết lượt `tra-luat-win`:
`tra-luat-win`: `Online` trong `list_devices` (ADR-0058 §1); `C:\tl-win\KHOA.txt` rỗng, không `python.exe` nào ⇒ khoá
`session_015GtxrbRjCRMMLRWHoUuZYj` 04:54:46Z hạn 06:54:46Z; clone `C:\tl-win\session_015GtxrbRjCRMMLRWHoUuZYj` đúng `356a27e`, không nông,
có `4bc94325…`, sạch, `core.abbrev 7`; Python 3.12.10; tiến trình tách PID 6996 từ 04:57:01Z, log
`C:\tl-win\session_015GtxrbRjCRMMLRWHoUuZYj-356a27e.log`. Lượt ASUS-LAPTOP (bị cắt, KHÔNG phải bằng chứng): máy `Offline` từ ~04:28Z khi đã ~100/153 đột biến (6 dòng khớp `ĐỎ|KHÔNG RĂNG|Traceback`
đều là tên ca chứa chữ "traceback", không lỗi thật); khoá `D:\tl-win\KHOA.txt` không xoá được, tự hết hiệu lực 05:44:33Z (ADR-0058 §3a).
Chi tiết lượt ASUS-LAPTOP: ASUS-LAPTOP `Online` (03:44Z, `tra-luat-win` cũng `Online` nhưng không dùng);
`KHOA.txt` rỗng ⇒ ghi khoá `session_015GtxrbRjCRMMLRWHoUuZYj` 03:44:33Z hạn 05:44:33Z. Kiểm tải: 2 `python.exe` của `browser-use --cli-mcp`
(PID 19112, 14808), không đụng. Clone `D:\tl-win\session_015GtxrbRjCRMMLRWHoUuZYj` từ GitHub, đúng `356a27e`, không nông, có `4bc94325…`,
sạch, `core.abbrev 7`. Lệnh `python -u ops\bien_nhan_v2_test.py` (`PYTHONUTF8=1 PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1`),
tiến trình tách bắt đầu 03:46:14Z, log `D:\tl-win\session_015GtxrbRjCRMMLRWHoUuZYj-356a27e.log`.

**Còn lại:** C7 N/N đầy đủ trên máy có quyền symlink (tuỳ chủ kho). Không merge/land (`uy_quyen_merge: false`) — chờ chủ kho. Lease hết hạn 2026-10-31T08:57:00Z.

## Cập nhật 30→31-10-2026 — sau khi #1041 vào master (đọc phần này TRƯỚC các mục trên)

Head hiện hành **`356a27e1378b2162bbc0be2ec06ff08fdacbdead`** (các mục trên mô tả `e9e0048`, nay đã cũ).

**Vì sao đổi head.** Chủ kho chỉ thị thứ tự merge (#1037 issuecomment-6529010520): #1041 trước, #1040 sau. #1041 vào master ở
`b29da0b`; nhánh này merge master vào ở `3883b60` (một hunk xung đột trong `ops/bien_nhan_v2_test.py`: giữ cả hai khối, đổi ca
`c98_chon_…` của #1021 thành `c101_…`). Chủ kho chọn gộp vào review các ca biên cửa sổ M4 của `c88` (#1011).

**Trần Codex** (ghi ở Issue #1021): 4 → 6 (issuecomment-6529311540) → 7 (6530712225) → 9 (6531357709). Đã dùng **7**.

| lượt | run_id | prompt sha256 | head | thời lượng | verdict | VERDICT.md sha256 |
|---|---|---|---|---|---|---|
| 5 | `2559d018c8b84c4d9517f138689796c1` | `faddce17…9aedea` | `3883b60` | 1048,1 s | request_changes — 1 P1 `bien-ngoai-cua-so-surface-chua-co-rang` (c88: biên `j = 0`, trích dẫn dòng sau; HÌNH DẠNG `bo-chon-ung-vien`) | `d0bebd7f…3ef46f` |
| 6 | `529bc3d976b244eaaaadc7e134d05993` | `e81958dc…e07ebc` | `691cb65` | 1010,8 s | request_changes — P1 **đã vá thật**; 1 P3 chú thích | `7be99282…103173` |
| 7 | `fcb9cb37d2014088ac4292a38b353dc8` | `6011d33a…bf03f8` | `c8a493c` | 627,9 s | request_changes — P3 lượt 6 đã vá; 1 P3 docstring trỏ `c99` thay `c100` | `181946a7…a00d1a10` |

Lượt 5 cũng xác nhận giải xung đột đúng (không mất dòng của bên nào) và F1–F3 cũ vẫn đóng.

| commit | nội dung |
|---|---|
| `3883b60` | merge master `b29da0b` (#1041) |
| `691cb65` | áp `HINT.patch` lượt 5 (sha256 `994c283d…`): bỏ tiền tố fixture `c88`, hàng `ii-b`, `m156`, `m157` (chủ kho duyệt) |
| `c8a493c` | áp `HINT-LUOT6.patch` (sha256 `fc52cb29…`): một dòng chú thích |
| `6964930` | P3 lượt 7 + hai tham chiếu đã cũ executor tự rà (chỉ docstring) |
| `356a27e` | tự rà mọi docstring #1021 trước lượt 8 (chỉ docstring) |

**Đo trên `356a27e`:**
- Linux (phiên executor): `bien_nhan_v2_test: 98/98 ca đạt · 153/153 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt`, `TỔNG: ĐẠT`;
  `bien_nhan_v2 --root .` `tổng 306`, `TỔNG: ĐẠT`; ruff F delta 0; `doctrine-scan` sạch.
- Ubuntu PR run 41113943723 `success`.
- Windows dispatch `runner_set=windows-only` 41113949578 `success`; job `gate-ops (windows-latest)` (runner_id 1000026867):
  `98/98 · 153/153 · 2/2`, `TỔNG: ĐẠT`; `lease_publish: 255/255 đạt; bỏ qua=13`.
- Windows local (ASUS-LAPTOP) trên `356a27e`: **KHÔNG ĐO ĐƯỢC** — đã khởi chạy 19:17Z (khoá hạn 21:17Z) nhưng máy offline từ
  ~19:35Z; không đọc được log, không ghi được `do-luong.csv`, không xoá được khoá (khoá tự hết hiệu lực 21:17Z theo ADR-0058 §3a).
  Các head trung gian `3883b60`/`691cb65`/`c8a493c` từng được chạy rồi dừng tay khi head đổi — không có N/N local nào cho chúng.

**CHƯA XONG — việc còn lại:**
1. **Codex lời gọi 8/9 trên `356a27e` chưa chạy.** Đĩa container còn ~75 MB; xoá bản làm việc review cũ bị cơ chế quyền phiên chặn
   (chủ kho đã đồng ý xoá, nhưng phiên không vượt chốt). Prompt lượt 8 đã soạn (sha256 `e6fdd2c0…`), cần chạy ở phiên có đĩa.
2. Lease hết hạn **2026-10-31T08:57:00Z**.
3. Master đã tiến tới `ba1b10d` (30 commit sau `b29da0b`), KHÔNG chạm `ops/bien_nhan_v2*.py`; có biên nhận mới trong
   `ops/reviews/` nên `tổng` của cổng sau merge sẽ khác 306.

## Phụ lục A — nguyên văn verdict Codex

### Lượt 1 — sha256 `2b6249476820cfb79ca8137c0de8b8bcbd40c82ffb381aaa490b50ddfc20fdf4`

<!-- VERDICT-L1-BAT-DAU -->
Verdict: request_changes
Reviewed commit: 99c463d9288798cf7a011e16ce69c36b04520f66
Spec sha256: d5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d

**Kết luận cuối: request_changes — 2 finding P2 còn mở** (0 P0, 0 P1, 0 P3 trong phạm vi đã đo). Head và base đều qua toàn suite; C1a/C1b/C2/C3/C6/C9 đạt trong các phép đo Linux. Tuy nhiên, đổi sang `iterdir()` làm lỗi liệt kê thư mục thoát thành traceback, và ba đột biến phá hành vi M1 vẫn qua toàn suite. Ngưỡng packet đòi hết cả P0–P3 nên chưa đủ approve. Báo cáo không cấp quyền merge/land.

Reviewed tree: `b6e042a42845fa52a90d898fc43ff72619f26c80`. Base: `757bde561d09738858506aecf5de2f050a5f0d5e`, tree `ab4a284cd655e867fc0bf35d1580a59d28d348db`. `git rev-parse --is-shallow-repository` trả `false` cho cả hai bản sao.

Các lệnh dưới chạy từ thư mục sandbox trừ khi ghi cwd khác. `measure.py` và `mutate.py` tự đặt `PYTHONDONTWRITEBYTECODE=1`, `PYTHONUTF8=1`, `PYTHONIOENCODING=utf-8`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_SYSTEM=/dev/null` cho tiến trình con. Với `probe.py` chạy trực tiếp, dùng cùng các biến đó. `core.abbrev=7` trên các bản sao trước phép đo. Log stdout/stderr và rc riêng trong `evidence/`; không suy pass chỉ từ rc.

## Bảng tiêu chí

| Tiêu chí | Màu / kết luận | Lệnh hoặc công cụ; output đo được |
|---|---|---|
| C1a | 🟢 Linux; 🟡 Windows KHÔNG ĐO ĐƯỢC | `python3 probe.py head behaviors`: hai YAML hợp lệ sai schema ⇒ rc=1, tổng 2, có `x.RECEIPT.YAML`, không `TỔNG: ĐẠT`; chỉ-x ⇒ rc=1, tổng 1, không “không có tệp”. `python3 mutate.py exact`: c98 `giet_that`, tổng=1; đối chứng sạch. Base: tổng 1 và bỏ x. |
| C1b | 🟢 Linux; 🟡 Windows KHÔNG ĐO ĐƯỢC | Cùng lệnh `behaviors`: YAML hỏng ⇒ rc=2, stderr nêu x, không traceback, không dòng tổng. `python3 probe.py mut-exact behaviors`: rc=1, tổng 1, không x trong stderr. |
| C2 | 🟢 Linux; 🟡 Windows KHÔNG ĐO ĐƯỢC | `python3 probe.py head cases`: c89 `qua`; base suite cũng có c89 `ĐẠT`. `python3 mutate.py isfile`: c89 `giet_that`, c98 `qua`, đối chứng c18 sạch hoàn toàn. |
| C3 | 🟢 | `python3 mutate.py glob`: bản sao helper dùng `tm.glob("*.receipt.yaml")`; c98 `giet_that` vì tổng=1, c89 `qua`, đối chứng sạch. Bản sao và patch lưu riêng, không thêm mutant glob vào bảng thường. |
| C4 | 🟡 KHÔNG ĐO ĐƯỢC đầy đủ | GitHub GET `actions/runs?head_sha=<reviewed SHA>&event=workflow_dispatch&per_page=100` và `actions/runs/41031049365/jobs?per_page=100`: đúng head, `.github/workflows/ci.yml`, job `123980641358`, labels `["windows-latest"]`, runner_id `1000025693`; selftest biên nhận còn `in_progress`, lease-publish `pending`. Chưa có N/N, chưa xác minh input `runner_set`. |
| C5 | 🟡 KHÔNG ĐO ĐƯỢC đầy đủ | `github_fetch_commit_workflow_runs` theo đúng head và GET `actions/runs/41031052871/jobs?per_page=100`: job `123980706092`, đúng head, labels `["ubuntu-latest"]`, runner_id `1000025706`; hai bước cần thiết đều `completed/success`, không skipped. `github_fetch_workflow_job_logs(job_id=123980706092)` lỗi 404 `BlobNotFound`, nên chưa đọc được N/N và `TỔNG: ĐẠT` từ log CI. |
| C6 | 🟢 | `python3 measure.py head gate`: rc=0, `253 ĐẠT v2 · 11/11 miễn trừ · 42 NỢ · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 306`, `TỔNG: ĐẠT`. Đếm riêng `sum(p.name.lower().endswith(".receipt.yaml") for p in Path("work/head/ops/reviews").iterdir())` ⇒ 306. Base gate và phép đếm cũng 306. |
| C7 | 🟡 KHÔNG ĐO ĐƯỢC | `remote_desktop_commander_list_devices({})` trả ASUS-LAPTOP `Online`. Không chạy test local Windows và không ghi khoá/sổ đo: chỉ thị reviewer giới hạn ghi trong sandbox, prompt đã yêu cầu phần Windows ghi không đo được. Không suy máy offline hay lấy CI thay local. ADR-0057/0058 đã đọc. |
| C8 | 🔴 | Hai P2 ở bảng findings; verdict neo đúng head nhưng là `request_changes`. Chưa có cơ sở xác nhận mọi điều kiện merge; không suy ngân sách review từ lời khai lease. Chốt dừng `bo-chon-ung-vien` của SPEC đã kích hoạt. |
| C9 | 🟢 các phép đo tại chỗ | `python3 -m ruff check --no-cache --select F ops/bien_nhan_v2.py ops/bien_nhan_v2_test.py` ở head/base: cùng F541 `1677:19`, cùng rc=1, delta=0, Ruff 0.15.15. Doctrine scan rc=0, `10 tệp, 0 chỗ chép doctrine`; `git diff --check <base>..HEAD` rc=0; rg mẫu glob ở head 0 dòng/rc=1, base 2 dòng, mutant-glob 1 dòng; numstat đúng hai tệp `17/3`, `50/0`. Vế dương C1a/C1b đã đo ở trên. |

## Bảng findings

| Mức | Slug lớp | Vị trí | Tái hiện / output / hướng vá |
|---|---|---|---|
| P2 | `loi-do-liet-ke-thu-muc-thoat-traceback` | `ops/bien_nhan_v2.py:96–98` | `python3 listing_probe.py`: tiêm EACCES vào liệt kê, head kiểm và sinh nợ rc=1 + traceback; base kiểm rc=2 không traceback. Chuyển `OSError` thành `KhongDoDuoc`, giữ nghĩa thư mục vắng; chi tiết và rủi ro ở Đợt 3. |
| P2 | `bo-chon-ung-vien-thieu-rang-hai-duong-goi` | `ops/bien_nhan_v2_test.py:3637–3658,4467–4472` | `python3 mutate.py <sinh_exact\|nosort\|noguard> --suite --behaviors`: ba bản lỗi đều rc=0, 95/95, 139/139, 2/2, `TỔNG: ĐẠT`. Thêm oracle và mutant riêng cho sinh nợ, sorted và thư mục vắng; chi tiết ở Đợt 4. |

Hai lớp finding, năm biểu hiện đo được: lớp lỗi liệt kê có hai đường gọi; lớp thiếu oracle có ba đột biến sống. Các đoạn sau giữ nhật ký đã ghi tăng dần, bao gồm lệnh, đối chứng, giới hạn và hướng vá cho từng finding.

Đã đối chiếu đầu vào bằng `git -C cay-kho rev-parse HEAD origin/master`,
`git -C cay-kho status --short`, `sha256sum SPEC.md`: head và băm như trên;
base `757bde561d09738858506aecf5de2f050a5f0d5e`; status rỗng, rc=0.
Kho nguồn được giữ nguyên; phép đo và đột biến dùng bản sao đủ cây trong sandbox.
Ở mốc đầu, Windows CI/local và Linux CI chưa có phép đo độc lập; kết quả đọc CI về sau được ghi trong bảng trên và phần cuối.

## Nhật ký đo

### Đợt 1 — C1, C6, C9

`PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null python3 probe.py head behaviors` và bản `base`: log `evidence/{head,base}-behaviors.log`, JSON từng fixture trong `evidence/fixture-*.json`. Kho thử do reviewer dựng độc lập, có git thật và commit.

| Phép đo | Head | Base |
|---|---|---|
| c1a | rc=1; tổng=['2']; traceback=False | rc=1; tổng=['1']; traceback=False |
| only-x | rc=1; tổng=['1']; traceback=False | rc=2; tổng=[]; traceback=False |
| c1b | rc=2; tổng=[]; traceback=False | rc=1; tổng=['1']; traceback=False |
| directory | rc=2; tổng=[]; traceback=False | rc=1; tổng=['1']; traceback=False |
| sinh-upper | rc=0; tổng=[]; traceback=False | rc=0; tổng=[]; traceback=False |
| missing | rc=2; tổng=[]; traceback=False | rc=2; tổng=[]; traceback=False |
| sinh-missing | rc=0; tổng=[]; traceback=False | rc=0; tổng=[]; traceback=False |
| case-pair | rc=1; tổng=['2']; traceback=False | rc=1; tổng=['1']; traceback=False |

`python3 measure.py head gate`: rc=0; `253 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 306`; `TỔNG: ĐẠT`.

Đếm riêng bằng `sum(p.name.lower().endswith(".receipt.yaml") for p in Path("work/head/ops/reviews").iterdir())`: **306**, base cũng **306**.

`python3 measure.py head doctrine`: rc=0; `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine`. `python3 measure.py {head,base} ruff`: mỗi lệnh rc=1, cùng một F541 tại `ops/bien_nhan_v2_test.py:1677:19`, delta **0**; Ruff **0.15.15**. Không gọi bare lint này là sạch.

`git -C cay-kho diff --numstat 757bde561d09738858506aecf5de2f050a5f0d5e..HEAD`: `17 3 ops/bien_nhan_v2.py`, `50 0 ops/bien_nhan_v2_test.py`; `git diff --check` cùng dải: rc=0, stdout rỗng.

### Đợt 2 — suite và đột biến đích

`python3 measure.py head suite` → rc=0, 463.23 s; `bien_nhan_v2_test: 95/95 ca đạt · 139/139 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 121/139 đột biến thường khai đối chứng`; `TỔNG: ĐẠT`.

`python3 measure.py base suite` → rc=0, 460.25 s; `bien_nhan_v2_test: 94/94 ca đạt · 137/137 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 119/137 đột biến thường khai đối chứng`; `TỔNG: ĐẠT`.

Delta đo được: **+1 ca, +2 đột biến thường**, không đổi **2 ca tự kiểm**.

Mỗi đột biến sau được tạo trên bản sao đủ cây bằng `python3 mutate.py <tên>`; bản vá nguyên văn và stdout nằm ở `evidence/mut-<tên>.patch` / `evidence/mut-<tên>-cases.stdout`.

| Đột biến | c98 | c89 | Đối chứng c18 sạch hoàn toàn |
|---|---|---|---|
| glob | giet_that | qua | True |
| exact | giet_that | qua | True |
| isfile | qua | giet_that | True |
| kiem_exact | giet_that | qua | True |
| sinh_exact | qua | qua | True |
| nosort | qua | qua | True |
| noguard | qua | qua | True |

C3: `glob` ⇒ c98 `giet_that`, thông điệp `tổng=1`; c89 `qua`. C2: `isfile` ⇒ c89 `giet_that`, rc=1 không còn tên thư mục; c98 `qua`. Không tính lỗi rig là bằng chứng giết trong các phép này.

C9: `rg -n 'glob\("\*\.receipt\.yaml"\)' ops/bien_nhan_v2.py`: head **0 dòng, rc=1**; base **2 dòng (1442,1601), rc=0**; bản `mut-glob` **1 dòng (98), rc=0**. JSON lệnh và output trong `evidence/scope.json`.

Regex: `python3 probe.py head total20` ⇒ c98 `giet_that`, `tổng=20`; c89/đối chứng vẫn qua. Không có lỗi khớp nhầm 20 thành 2.

### Đợt 3 — hồi quy lỗi liệt kê thư mục

- [P2] `loi-do-liet-ke-thu-muc-thoat-traceback`: `ops/bien_nhan_v2.py:96–98` — `PYTHONDONTWRITEBYTECODE=1 python3 listing_probe.py` — head khi `scandir(ops/reviews)` ném `PermissionError(EACCES)` trả **rc=1 + Traceback** trên cả đường kiểm và `--sinh-no`; base cùng fault đã xác nhận vào điểm tiêm: kiểm **rc=2, KHÔNG ĐO ĐƯỢC, không Traceback**, sinh nợ **rc=0, # 0 tệp**. Hướng vá: bắt `OSError` của phép liệt kê trong helper và đổi thành `KhongDoDuoc` có tên thư mục; giữ nhánh thư mục vắng trả `[]`, không nuốt lỗi bằng danh sách rỗng và không thêm `is_file()`.

HÌNH DẠNG: `loi-do`. Phép đo chạy trên bản sao head/base đầy đủ, không thay nguồn sản phẩm; tiêm đúng lỗi OS ở điểm liệt kê. Python 3.13 giữ riêng `scandir` cho glob, nên script tiêm cả `os.scandir` và `pathlib._local._StringGlobber.scandir`; mỗi đường lỗi có dấu `REVIEW_ENUMERATION_FAULT` xác nhận đã tiêm. Đối chứng không tiêm dùng cùng fixture `y.receipt.yaml`: cả hai bản kiểm rc=1 không traceback (schema cố ý sai), sinh nợ rc=0 với `# 1 tệp`. Log đầy đủ: `evidence/listing-{head,base}-{kiem,sinh}-{control,fail}.{json,stdout,stderr}`.

Ca khóa đề nghị: ép lỗi liệt kê trên thư mục có thật; đòi CLI kiểm và sinh nợ rc=2, nêu `ops/reviews`, không traceback; chạy thêm thư mục vắng và `c89` để giữ nghĩa cũ. Rủi ro khi vá: trả `[]` cho mọi `OSError` sẽ biến lỗi đo thành danh sách nợ rỗng; bắt `Exception` quá rộng che lỗi lập trình.

Giới hạn: phép đo bằng quyền hệ thống thực ở `io_probe.py` **KHÔNG ĐO ĐƯỢC** vì sandbox từ chối `os.setgroups([])` (`PermissionError: Operation not permitted`) trước khi gọi cổng. Không dùng các traceback đó làm bằng chứng lỗi sản phẩm. Bằng chứng finding là phép tiêm lỗi riêng đã nêu ở trên.

RIG: `python3 probe.py head rig-setup` tiêm `LoiDungCa` ở `_kho_cau` ⇒ c98/c89 đều `gian_giao`, đối chứng sạch. `python3 probe.py head rig` cố ý thay riêng `bnv2.main` bằng hàm ném `LoiDungCa` ⇒ c98/c89 báo `giet_that`, do `except Exception` đổi thành `bang(False)`. Đây là hạn chế của bắt ngoại lệ nếu tín hiệu rig xuất hiện bên trong API sản phẩm; chưa chứng minh đường fixture/m142 thật phát tín hiệu đó. Không dùng phép giả lập này để tuyên bố m142 đang có tín dụng giả.

### Đợt 4 — ba đột biến sống qua toàn suite

- [P2] `bo-chon-ung-vien-thieu-rang-hai-duong-goi`: `ops/bien_nhan_v2_test.py:3637–3658,4467–4472` — `python3 mutate.py sinh_exact --suite --behaviors`, tương tự `nosort`, `noguard` — **cả ba** bản có lỗi vẫn `95/95 ca đạt · 139/139 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt`, **rc=0, TỔNG: ĐẠT**. Hướng vá: thêm chốt trực tiếp cho `--sinh-no`, thứ tự helper và thư mục vắng; thêm đột biến đích riêng, không dựa hoàn toàn vào một đột biến helper chung.

HÌNH DẠNG: `bo-chon-ung-vien`. Đây là **một lớp finding, ba biểu hiện** thiếu oracle cho hành vi M1; không báo ba finding rời. Mã sản phẩm trên head đang xử lý đúng ba hành vi; lỗi là bộ kiểm không phát hiện khi chúng bị phá.

| Bản sao / đột biến | Hành vi sai đo riêng | Kết quả suite |
|---|---|---|
| `sinh_exact` | Chỉ thêm lọc `p.name.endswith(".receipt.yaml")` tại vòng lặp `_sinh_no`. `X.RECEIPT.YAML` bị bỏ qua: head `# 1 tệp`, mutant `# 0 tệp`, cùng rc=0. C1a/C1b ở đường kiểm vẫn qua. | rc=0; 95/95,139/139,2/2; 438.8 s; `TỔNG: ĐẠT` |
| `nosort` | Đặt `sorted = list` cục bộ trong helper (giữ neo văn bản m142/m143 để không chết giả vì rig). Tổng vẫn 3 nhưng thứ tự lỗi và khối nợ đổi; lỗi YAML đầu tiên đổi tên a thành z. | rc=0; 95/95,139/139,2/2; 440.11 s; `TỔNG: ĐẠT` |
| `noguard` | Bỏ hai dòng `if not tm.is_dir(): return []` ở helper. `--sinh-no` với thư mục vắng đổi từ rc=0, khối rỗng sang rc=1 + FileNotFoundError/Traceback; đường `kiem` còn guard riêng nên không đổi. | rc=0; 95/95,139/139,2/2; 438.77 s; `TỔNG: ĐẠT` |

Tái chạy trên bản sao đã lưu: `python3 measure.py mut-sinh_exact suite`, `python3 measure.py mut-nosort suite`, `python3 measure.py mut-noguard suite`; hành vi: `python3 probe.py <tên-cây> behaviors`. Tạo mới từ head bằng `mutate.py` trong sandbox trống tương ứng. Mỗi bản là bản sao đủ cây, `.git` là thư mục; mỗi suite là tiến trình riêng.

Ca khóa đề nghị: fixture chỉ có `X.RECEIPT.YAML` hợp lệ YAML nhưng sai schema, gọi CLI `--sinh-no`, đòi đúng tên và đúng số 1; helper nhận danh sách thư mục bị đảo thứ tự nhưng phải trả sorted; fixture không có `ops/reviews` đòi đường kiểm rc=2 không traceback, sinh nợ giữ rc=0/khối rỗng. Mỗi đột biến phải giết đúng ca đích và đối chứng vẫn sạch. Rủi ro khi vá test: đừng so thứ tự Path xuyên nền bằng thứ tự Linux ghim cứng; hãy ép thứ tự đầu vào trong fixture và so theo hợp đồng sorted của nền, không dùng hai tệp chỉ khác case trong ca bắt buộc Windows.

**Chốt dừng của SPEC `hinh_dang_ke_thua` đã kích hoạt** bởi finding mới hình dạng `bo-chon-ung-vien` trên M1. Câu hỏi chuyển chủ kho: **“có nên làm tiếp theo cách này không”**. Review đã hoàn tất; không tiến hành vá/đổi thiết kế trước quyết định đó.

### Hành vi biên và giới hạn

- `probe.py head behaviors`: `--sinh-no` nhận `X.RECEIPT.YAML`, rc=0, `# 1 tệp`, băm `37b128c59f1f5097f73f82691cb519f1f568667faab5ced1b4ab979d36837eae`. Thư mục biên nhận vắng trong kho git thật: kiểm rc=2, `kho thật mà không có ... — không phải sạch`, không traceback; sinh nợ rc=0, `# 0 tệp`, giống base. Không gọi hành vi sinh nợ có sẵn này là lỗi mới.
- Hai tên `a.receipt.yaml` và `a.RECEIPT.YAML` cùng tồn tại: head tổng 2, rc=1, cả hai tên có trong lỗi; base tổng 1. Chỉ đo Linux.
- `evidence/order-summary.json`: head thứ tự a,m,z; nosort m,z,a ở cả dòng lỗi và khối sinh nợ. Cùng tổng 3 và rc tương ứng 1/0. Với hai YAML hỏng: head báo a trước, nosort báo z trước, cùng rc=2. Trong các fixture này không đổi kết luận nhưng có đổi đầu ra; chưa suy cho mọi dữ liệu hay thứ tự Windows.
- `probe.py mut-exact behaviors`: C1a rc=1/tổng 1/không x; chỉ-x rc=2/không tổng; C1b rc=1/tổng 1/không x trong stderr. Như vậy cả ba vế sai riêng, dù c98 dừng ở vế đầu khi chạy nguyên ca.

### Bằng chứng CI, Windows local và kiểm tra cuối

Các truy vấn chỉ đọc qua connector GitHub/Remote Desktop Commander; không phát workflow, không ghi ứng dụng ngoài sandbox. Payload gốc được lưu: `evidence/windows-runs.json`, `windows-jobs.json`, `linux-jobs.json`, `ci-log-error.json`, `desktop-devices.json`.

- C4: [run Windows 41031049365](https://github.com/ducthangho/tra-luat/actions/runs/41031049365), job `123980641358`: head đúng, nhãn/runner_id đã đọc từ JSON jobs, selftest biên nhận còn chạy, lease-publish pending. Kết quả cuối và N/N **KHÔNG ĐO ĐƯỢC**.
- C5: [run PR 41031052871](https://github.com/ducthangho/tra-luat/actions/runs/41031052871), job `123980706092`: hai bước cần thiết đã success; log job trả 404 BlobNotFound tại lần đọc. Không coi status success là thay cho N/N. Toàn suite đo tại chỗ cũng không thay CI.
- C7: danh sách thiết bị trả Online nhưng không có lượt local nào do reviewer chạy; test Windows local, so base và sổ đo **KHÔNG ĐO ĐƯỢC**.

`GIT_OPTIONAL_LOCKS=0 git -C cay-kho status --porcelain=v1 --untracked-files=all --ignored` ⇒ rc=0, rỗng; `git -C cay-kho diff --exit-code HEAD --` ⇒ rc=0, rỗng. HEAD/tree cuối khớp các neo đầu báo cáo; `DIFF.patch` byte-identical với `git diff <base>..HEAD`; sha256 SPEC vẫn khớp. Chi tiết lệnh/output: `evidence/final-integrity.json`. Trạng thái đầu/cuối chứng minh không có delta quan sát được; không dùng nó để khẳng định lịch sử mọi lần ghi.

**request_changes** trên exact head đã nêu. Không sửa mã nguồn kho được review; không cấp quyền merge/land. Finding `bo-chon-ung-vien` cần quyết định của chủ kho theo chốt dừng SPEC trước vòng vá tiếp.
<!-- VERDICT-L1-KET-THUC -->

### Lượt 2 — sha256 `68b2cbe6a1555f3af26702d737fd8c2c1f46a780baf76bc6f7021994fc3827fd`

<!-- VERDICT-L2-BAT-DAU -->
Verdict: request_changes
Reviewed commit: 5efa311fd857f7657a1c687e9ea37693070a37d3
Spec sha256: d5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d

Kết luận: **request_changes**, còn **1 P2 và 1 P3** (2 lớp, 2 biểu hiện mở). Head qua **96/96 ca · 143/143 đột biến thường · 2/2 tự kiểm**, `TỔNG: ĐẠT`. Ba đột biến sống ở lượt trước nay chết đúng chốt c99. Lỗi liệt kê cũ đã được vá ở iterdir, nhưng EACCES ở `is_dir()` vẫn thoát traceback qua đường `--sinh-no`. Đột biến tương đương bắt `Exception` sống qua toàn suite, cho thấy thiếu chốt phân biệt lỗi lập trình. Ngưỡng áp dụng theo packet: không còn P0/P1/P2/P3. Windows và CI trên head này không được đo độc lập; không suy kết quả từ báo cáo executor.

## Neo và phạm vi

`git -C cay-kho rev-parse HEAD HEAD^{tree} origin/master` (rc=0): head như trên; tree `84f05adc6dcaadd38590431d92b2bc5df4206b99`; base `757bde561d09738858506aecf5de2f050a5f0d5e`.
`git -C cay-kho rev-parse --is-shallow-repository` ⇒ `false`; status gồm ignored/untracked ⇒ rỗng; `sha256sum SPEC.md` khớp dòng 3.
Đã đặt `git -C cay-kho config core.abbrev 7` theo chỉ thị. Các bản sao `work/head`, `work/base` có đủ cây và `.git` là thư mục. Lệnh Python đo chạy với `PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1 PYTHONIOENCODING=utf-8 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null` qua `measure.py` hoặc tiền tố môi trường tương đương.

Các script lượt 1 được chép ra gốc sandbox: `measure.py`, `listing_probe.py` giữ nguyên; `probe.py` thêm c99 vào danh sách ca đích; `mutate.py` đổi mốc neo selector từ biểu thức return sang ds, nosort vẫn che sorted bằng list tại return. Không đổi cơ chế phép thử. Diff adapter nằm trong `evidence/adapter-*.patch`.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn: `VERDICT-LUOT1.md`, reviewed head `99c463d9288798cf7a011e16ce69c36b04520f66` (lượt trước); đối chiếu trên exact head dòng 2 bằng script đã chép kèm.

| Finding P2 lượt 1 | Phân loại | Bằng chứng độc lập trên head mới |
|---|---|---|
| `loi-do-liet-ke-thu-muc-thoat-traceback` | **VÁ HỜ ở cấp lớp; phép tái hiện gốc đã vá thật** | `python3 listing_probe.py`: lỗi scandir ở cả hai đường nay rc=2, không traceback, có marker xác nhận tiêm. Tuy nhiên `python3 review_new.py error-child head sinh access`: EACCES ở stat trước iterdir vẫn rc=1/Traceback tại helper:101. Cùng gốc là thao tác I/O chuẩn bị danh sách nằm ngoài nhánh đổi lỗi đo; xem finding F1. |
| `bo-chon-ung-vien-thieu-rang-hai-duong-goi` | **ĐÃ VÁ THẬT** | `python3 mutate.py sinh_exact --suite`, `nosort --suite`, `noguard --suite`: cả ba rc=1/95 trên 96 ca/TỔNG: ĐỎ. c99 chết đúng chốt sinh nợ, thứ tự, thư mục vắng; c98/c89/c18 đối chứng qua. Thông báo và N/N đầy đủ ở Đợt 1 và Đợt 4. |

Không coi traceback của guard `kiem` ở base là hồi quy mới; F1 khoanh hồi quy vào guard helper mà packet thêm cho `--sinh-no`. Không có finding mới hình dạng `bo-chon-ung-vien`; chốt dừng cũ đã được chủ kho cho làm tiếp theo packet giao lượt này.

## Nhật ký đo

### Đợt 1 — phép tái hiện cũ, C1/C2/C3/C6/C9

`PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null python3 listing_probe.py` giữ nguyên script lượt 1: head `kiem` và `--sinh-no` đều **rc=2**, stderr có `REVIEW_ENUMERATION_FAULT: scandir`, `KHÔNG ĐO ĐƯỢC: không liệt kê được … (PermissionError …)`, không traceback. Đối chứng không tiêm: `kiem` rc=1/tổng 1/sai schema, sinh nợ rc=0/# 1 tệp. Log và rc thật: `evidence/listing-head-{kiem,sinh}-{fail,control}.{json,stdout,stderr}`.

Ba đột biến cũ đã chết đúng chốt c99 trong lượt chạy ca đích (`python3 mutate.py <tên> --suite`; số đo toàn suite bổ sung ở Đợt 4):

| Đột biến | Phân loại của c99 | Thông báo thực đo |
|---|---|---|
| sinh_exact | giet_that | sinh-no: đòi rc=0, khối nợ nêu x.RECEIPT.YAML, # 1 tệp; được rc=0, khối rỗng, # 0 tệp |
| nosort | giet_that | thứ tự: đòi a,m,z khi iterdir trả ngược; được z,m,a |
| noguard | giet_that | vắng/sinh-no: đòi rc=0 # 0 tệp; được rc=2 … FileNotFoundError |

Cả ba: c98 và c89 `qua`, đối chứng c18 `[true, ""]`. Chi tiết nguyên văn: `evidence/mut-*-cases.stdout`; không coi rc của wrapper là bằng chứng giết.

`python3 mutate.py exact --behaviors` ⇒ c98 `giet_that`, C1a tổng 1; `python3 mutate.py isfile` ⇒ c89 `giet_that`, rc=1 thay rc=2; `python3 mutate.py glob` ⇒ c98 `giet_that`, tổng 1. Cả ba có đối chứng c18 sạch. Các đột biến được tạo trên bản sao đầy đủ, mỗi cái tiến trình riêng.

`PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null python3 probe.py head behaviors` dựng các kho git thật độc lập:

| Fixture | rc | tổng | Traceback |
|---|---:|---|---|
| bad-order | 2 | [] | False |
| c1a | 1 | ['2'] | False |
| c1b | 2 | [] | False |
| case-pair | 1 | ['2'] | False |
| directory | 2 | [] | False |
| empty | 2 | [] | False |
| missing | 2 | [] | False |
| only-x | 1 | ['1'] | False |
| order | 1 | ['3'] | False |
| sinh-missing | 0 | [] | False |
| sinh-order | 0 | [] | False |
| sinh-upper | 0 | [] | False |

C1a và chỉ-x đều nêu tên đuôi hoa, không `TỔNG: ĐẠT`; C1b stderr nêu `x.RECEIPT.YAML`. Nội dung từng stdout/stderr và lệnh CLI nằm trong `evidence/fixture-head-*.json`.

`python3 measure.py head gate` và `python3 measure.py base gate` ⇒ cùng rc=0, `253 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 306`, `TỔNG: ĐẠT`. Đếm độc lập bằng `sum(p.name.lower().endswith(".receipt.yaml") for p in Path("work/head/ops/reviews").iterdir())` ⇒ 306; base cũng 306.

`python3 measure.py head doctrine` ⇒ rc=0, `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine`.
`python3 measure.py {head,base} ruff` (Ruff 0.15.15, no-cache, --select F, đúng hai tệp) ⇒ cả hai rc=1 và cùng F541 tại `ops/bien_nhan_v2_test.py:1677:19`; delta 0. Không gọi bare lint là sạch.
`git -C cay-kho diff --numstat 757bde561d09738858506aecf5de2f050a5f0d5e..HEAD` ⇒ `26 3 ops/bien_nhan_v2.py`, `148 0 ops/bien_nhan_v2_test.py`; name-only đúng hai tệp write set; diff --check cùng dải ⇒ rc=0/rỗng.
`rg -n 'glob\("\*\.receipt\.yaml"\)' ops/bien_nhan_v2.py` ⇒ head 0 dòng/rc=1; base 2 dòng/rc=0; mut-glob 1 dòng/rc=0 (vế âm có đối chứng dương).

### Đợt 2 — độ nhạy của c99, lỗi giàn giáo và khôi phục toàn cục

`python3 new_mutate.py fault_noop`: vô hiệu điều kiện tiêm bằng `False and …` ⇒ c99 `giet_that`, thông báo `liệt kê hỏng [] … được rc=1`, không xanh giả. `python3 new_mutate.py fault_noop_sinh`: chỉ vô hiệu tiêm ở `--sinh-no` ⇒ c99 `giet_that`, thông báo `liệt kê hỏng ['--sinh-no'] … được rc=0: '# 1 tệp'`. Hai đối chứng c98/c89 qua, c18 sạch.
`python3 new_mutate.py order_noop`: fixture trả xuôi ⇒ c99 `gian_giao`, `fixture: iterdir ngược không có hiệu lực`; không được tính là giết thật. Cùng với mutant nosort chết bằng kết quả helper z,m,a, phép đo thứ tự kiểm cả giàn giáo lẫn đầu ra helper.
`python3 new_mutate.py no_os_catch` ⇒ c99 `giet_that`, `CLI chết bằng PermissionError … đòi mã thoát, không traceback`.
`python3 new_mutate.py catch_empty` ⇒ c99 `giet_that`, rc=2 nhưng chỉ báo `không có tệp`, thiếu `không liệt kê được`. Vậy chỉ rc=2 không đủ đánh lừa chốt (4).

`PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null python3 trace_probe.py` ⇒ c99 `qua`, hai lần PermissionError được tiêm đúng thư mục, modes `[]` và `['--sinh-no']` (`evidence/c99-trace.json`). Bản tracer đầu truy cập sai biến closure `co`, đã được phân loại là lỗi probe và lưu riêng `c99-trace-rig-error.json`; bản chạy đúng đọc mode từ frame c99.
`python3 review_new.py symlink` ⇒ c99 `qua` khi thư mục tạm đi qua symlink (`evidence/symlink-c99.stdout`). Đây chỉ là phép thử symlink trên hệ đang đo, KHÔNG phải bằng chứng Windows.

`python3 review_new.py cleanup <order|kiem|sinh> <runtime|rig>` (6 tiến trình riêng, môi trường chuẩn): cả 6 ghi `restored=true`, `finally_restored=true`, chạy lại c99 sau lỗi đều `['qua', null]`. Fault được tiêm khi Path.iterdir đang là `nguoc` hoặc `hong`, không phải trước khi patch. Với LoiDungCa cả 3 là `gian_giao`; RuntimeError ở order là `tin_dung_gia`, ở hai CLI là `giet_that`. Không quan sát rò Path.iterdir trong 6 nhánh lỗi này.
`python3 probe.py head rig` và `rig-setup` ⇒ c98/c99 đều `gian_giao`; nhánh `except LoiDungCa: raise` mới có hiệu lực. c89 cũ vẫn đổi lỗi rig do main thành `giet_that`; hành vi này ngoài phần sửa lượt 2, không dùng nó để chứng minh mutation mới chết.

### Đợt 3 — mở rộng lỗi I/O và ranh giới bắt ngoại lệ

`python3 review_new.py error-child head <kiem|sinh> late` ⇒ cả hai rc=2/không traceback khi iterator đã yield một mục rồi mới ném PermissionError; stderr có `REVIEW_FAULT_HIT: late` và `không liệt kê được`.
`python3 review_new.py error-child head <kiem|sinh> stat-os` ⇒ cả hai rc=1/Traceback, marker `REVIEW_FAULT_HIT: stat-os`. os.stat của đúng thư mục bị tiêm EACCES; Path.is_dir thật truyền lỗi ra ngoài try. Ở --sinh-no, traceback đi qua `_chon_bien_nhan` dòng 101; ở kiem là guard sẵn có dòng 1459.
`python3 review_new.py error-child <head|base> <kiem|sinh> access` tiêm cùng EACCES vào cả os.stat và scandir/glob của đúng thư mục. Head cả hai rc=1/Traceback; base kiem cũng rc=1/Traceback (lỗi đã có), base sinh rc=0/# 0 tệp, có marker `access-scandir`. Vì vậy hồi quy mới được khoanh ở nhánh `--sinh-no`; lỗi I/O trước iterdir vẫn chưa được chuẩn hoá. Log và mã thoát: `evidence/{head,base}-access-{kiem,sinh}.{json,stdout,stderr}`.

Đo bằng quyền thư mục thật: **KHÔNG ĐO ĐƯỢC**. `python3 actual_permissions.py` không hạ được quyền cho tiến trình con: `os.setgroups([])` trả EPERM ngay cả đối chứng; không có lệnh cổng nào chạy sau chốt đó. Không dùng các rc=1 ấy làm bằng chứng lỗi sản phẩm; finding ở trên chỉ dựa phép tiêm OS có marker trên Path.is_dir thật.

`python3 new_mutate.py broad_literal`: đổi `except OSError` thành `except Exception` ⇒ c98/c99/c89 đều `qua`, c18 sạch. Nếu giữ m147 nguyên văn thì mốc neo mất: `evidence/literal-anchor-check.json` ghi `gian_giao`, không phải oracle giết được lỗi bắt rộng.
`python3 new_mutate.py broad --suite`: đột biến tương đương về nghĩa bằng gán cục bộ `OSError = Exception` trong helper, giữ nguyên mốc neo của m147 để đo hành vi. Ca đích c98/c99/c89 vẫn qua, c18 sạch; toàn suite đã xong: rc=0, 96/96 ca, 143/143 đột biến thường, 2/2 tự kiểm, TỔNG: ĐẠT (463.72 s; xem chốt cuối).
`python3 review_new.py error-child <head|mut-broad> <kiem|sinh> <runtime|value>`: head phát RuntimeError/ValueError ra ngoài (rc=1/traceback); mutant biến chúng thành rc=2/`KHÔNG ĐO ĐƯỢC: không liệt kê được … (RuntimeError/ValueError …)`, không traceback. Tất cả có marker xác nhận lỗi đã tiêm. Đây là khác biệt hành vi thật; head hiện bắt đúng OSError, phần còn thiếu là test phân biệt lỗi lập trình.

### Đợt 4 — toàn suite và xác nhận ba đột biến cũ

| Lệnh (môi trường chuẩn ở đầu tệp) | rc thật của suite | Kết quả nguyên văn rút gọn | Thời gian |
|---|---:|---|---:|
| `python3 measure.py head suite` | 0 | bien_nhan_v2_test: 96/96 ca đạt · 143/143 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 125/143 đột biến thường khai đối chứng; TỔNG: ĐẠT | 483.28 s |
| `python3 mutate.py sinh_exact --suite` | 1 | bien_nhan_v2_test: 95/96 ca đạt · 142/143 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 125/143 đột biến thường khai đối chứng; TỔNG: ĐỎ | 476.41 s |
| `python3 mutate.py nosort --suite` | 1 | bien_nhan_v2_test: 95/96 ca đạt · 143/143 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 125/143 đột biến thường khai đối chứng; TỔNG: ĐỎ | 481.23 s |
| `python3 mutate.py noguard --suite` | 1 | bien_nhan_v2_test: 95/96 ca đạt · 142/143 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 125/143 đột biến thường khai đối chứng; TỔNG: ĐỎ | 481.72 s |

Trong full log, cả ba mutant có dòng `ĐỎ c99_… [giet_that]` với đúng thông báo đã trích ở Đợt 1. `sinh_exact` còn làm m144 mất neo, `noguard` làm m146 mất neo: hai dòng `gian_giao` ấy KHÔNG được dùng làm bằng chứng giết; bằng chứng là c99 tự đỏ khi chạy trên mutant, trước pha đột biến nội bộ. `nosort` giữ 143/143 đột biến nhưng vẫn đỏ vì c99, đúng kỳ vọng.

Phác thảo oracle đã chạy cho ranh giới ngoại lệ: `python3 boundary_oracle.py head` ⇒ rc=0; `python3 boundary_oracle.py mut-broad` và `mut-broad_literal` ⇒ rc=1. Tiêm một RuntimeError sentinel tại đúng thư mục rồi đòi đúng đối tượng ngoại lệ truyền ra ngoài trên cả hai đường; mỗi đường có hit=1 và Path.iterdir được khôi phục. Chi tiết: `evidence/*-boundary-oracle.{json,stdout,stderr}`. Đây là dữ liệu phản chứng trong sandbox, không phải bản vá giao áp tự động.

## Bảng tiêu chí

| Tiêu chí | Kết quả | Lệnh và bằng chứng |
|---|---|---|
| C1a | ĐẠT phần đã đo; Windows KHÔNG ĐO ĐƯỢC | `python3 probe.py head behaviors`: c1a rc=1/tổng 2/có x.RECEIPT.YAML/không ĐẠT; only-x rc=1/tổng 1/không "không có tệp". `mutate.py exact --behaviors`: C1a còn tổng 1, only-x không tổng; c98 giet_that. |
| C1b | ĐẠT phần đã đo; Windows KHÔNG ĐO ĐƯỢC | Cùng lệnh: YAML hỏng đuôi hoa rc=2/stderr nêu x/không traceback/không tổng. Mut-exact bỏ sót x, rc=1, tổng 1. |
| C2 | ĐẠT phần đã đo; Windows KHÔNG ĐO ĐƯỢC | Full suite có c89 ĐẠT; `python3 mutate.py isfile`: c89 giet_that, rc=1 thay rc=2, c98/c99 qua, c18 sạch. |
| C3 | ĐẠT trên Linux | `python3 mutate.py glob`: c98 giet_that/C1a tổng 1; đối chứng c18 sạch. Không cho mutant phụ thuộc nền này vào bảng thường. |
| C4 | KHÔNG ĐO ĐƯỢC | Không có phép đo Windows CI độc lập trên exact head trong lượt này; success trên 99c463d do executor cung cấp không thay bằng chứng 5efa311. |
| C5 | KHÔNG ĐO ĐƯỢC | Không có log Ubuntu CI độc lập trên exact head; full suite tại sandbox không được nhận là CI. |
| C6 | ĐẠT | `python3 measure.py head gate`: rc=0, tổng 306, TỔNG: ĐẠT; đếm riêng 306. Base thật cũng rc=0/tổng 306. `--sinh-no` trên head rc=0/# 42 tệp. |
| C7 | KHÔNG ĐO ĐƯỢC | Không chạy Windows local. |
| C8 | KHÔNG ĐẠT | Còn finding F1 (P2), F2 (P3); verdict request_changes trên exact head đã neo. Không cấp quyền merge/land. |
| C9 | ĐẠT | Ruff --select F delta 0 (cả hai bare lint rc=1/cùng F541); doctrine rc=0/10 tệp/0 chỗ; diff --check rc=0; rg 0 dòng, có đối chứng base 2/mut-glob 1; numstat +26/-3 và +148/-0, đúng hai tệp. |

## Finding

| ID | Mức | Slug lớp nguyên nhân | Nguồn/lý do giữ hoặc thêm | Phép đóng |
|---|---|---|---|---|
| F1 | P2 | `loi-do-liet-ke-thu-muc-thoat-traceback` | Giữ slug lượt 1; biểu hiện cũ ở scandir đã đóng, còn biểu hiện I/O trước liệt kê tại is_dir trên --sinh-no | Tiêm EACCES cả stat và liệt kê: hai đường rc=2/không traceback; vắng thật vẫn đúng hành vi cũ; fixture/c99 mới phải giết mutant bỏ bắt lỗi stat. |
| F2 | P3 | `loi-do-thieu-chot-ngoai-le-lap-trinh` | Mới trong phần test cho nhánh bắt OSError; hiện c99 chỉ tiêm PermissionError | Head qua oracle RuntimeError sentinel; mutant bắt Exception phải bị giết thật bởi ca đích, không phải mất neo m147. |

- [P2] `loi-do-liet-ke-thu-muc-thoat-traceback`: `ops/bien_nhan_v2.py:101` (gọi từ `_sinh_no` dòng 1624), khối try bắt đầu ở dòng 103 — `PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null python3 review_new.py error-child head sinh access` — rc=1, stderr có `REVIEW_FAULT_HIT: stat-os`, `Traceback`, `PermissionError: [Errno 13] review OS stat failure`; base cùng phép tiêm rc=0/# 0 tệp, marker access-scandir — đưa cả bước kiểm tra thư mục vào chính sách bắt **OSError** và đổi thành KhongDoDuoc, không đổi lỗi truy cập thành vắng/rỗng. Giữ hành vi thật sự thiếu thư mục (`kiem` rc=2, sinh nợ rc=0/# 0 tệp), bổ sung ca tiêm lỗi stat ở helper và đối chiếu guard kiem để hai đường cùng chuẩn lỗi I/O. Không bắt Exception để che lỗi lập trình.

HÌNH DẠNG: `loi-do`.

Bằng chứng chỉ rõ điều kiện lỗi: stat của thư mục biên nhận bị từ chối trước khi iterdir chạy, như lỗi quyền tra cứu đường dẫn. Guard mới nằm ngoài try nên lời khẳng định "lỗi I/O khi chọn biên nhận ⇒ rc=2 không traceback" chưa kín. Ở kiem, cùng lỗi đã có trên base và không được kê riêng thành hồi quy. Bản thử quyền thực tế bị chặn ở setup đã nêu ở Đợt 3; không suy rằng phép chmod thật đã được đo thành công.

- [P3] `loi-do-thieu-chot-ngoai-le-lap-trinh`: `ops/bien_nhan_v2_test.py:3731` (c99 chốt lỗi liệt kê), `ops/bien_nhan_v2_test.py:4568` (m147) — `PYTHONDONTWRITEBYTECODE=1 python3 new_mutate.py broad --suite` — **rc=0, 96/96 ca đạt · 143/143 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 125/143 đột biến thường khai đối chứng; TỔNG: ĐẠT**, 463.72 s; trong khi RuntimeError/ValueError ở iterdir bị chuyển thành KhongDoDuoc — thêm chốt tiêm lỗi lập trình ngoài OSError và đòi ngoại lệ nguyên gốc truyền ra trên cả hai đường, cùng mutant nới catch phải chết tại chốt đó. `boundary_oracle.py` đã đo head rc=0, cả hai mutant broad/broad_literal rc=1; có hit=1/đường và khôi phục Path.iterdir.

HÌNH DẠNG: `loi-do`.

Đây là thiếu chốt hồi quy, không khẳng định head hiện bắt Exception. Mutant `broad_literal` đổi trực tiếp tên catch, vượt qua c98/c99/c89 và đối chứng, nhưng phá mốc neo văn bản m147 nên không thể dùng lỗi rig để nhận tín dụng giết. Mutant `broad` đặt tên cục bộ `OSError = Exception` trong chính helper: cùng nghĩa bắt rộng, vẫn giữ mốc neo, và sống qua toàn suite. Vì chốt (4) chỉ đưa PermissionError (thuộc OSError), nó không phân biệt catch hẹp với catch rộng. Ảnh hưởng có giới hạn: mutant vẫn fail-closed rc=2, nhưng che nguyên nhân lỗi lập trình thành lỗi đo; do đó xếp P3, không xếp lỗi runtime P2 cho head đang đúng.

## Chốt bằng chứng và giới hạn

`python3 new_mutate.py broad --suite` đã hoàn tất: log `evidence/mut-broad-suite.stdout`, mã thoát và thời gian `evidence/mut-broad-suite.json`. Không đột biến nào còn đang chờ kết quả để lập verdict này.

`python3 probe.py base behaviors` được chạy lại qua `measure.run` trên đúng base: C1a rc=1/tổng 1/bỏ x; only-x rc=2/không tổng; C1b rc=1/tổng 1/bỏ x. `python3 probe.py base cases` ⇒ c89 qua, c18 sạch. `evidence/base-behaviors.*`, `fixture-base-*.json` và `base-cases.stdout` lưu phép đo mới, không tái dùng số của lượt 1.

`PYTHONDONTWRITEBYTECODE=1 python3 integrity.py` ⇒ rc=0. `evidence/final-integrity.json` ghi lệnh/output: head/tree/base vẫn đúng các neo ở đầu; detached, không nông, core.abbrev=7; status gồm tracked/untracked/ignored rỗng; diff worktree và index so HEAD rc=0/rỗng. Hai tệp write set byte-identical với blob HEAD; DIFF.patch và DIFF-LUOT2.patch byte-identical với git diff tương ứng; SPEC vẫn khớp SHA-256. Bản `work/head` chạy suite cũng sạch và cùng HEAD/tree. Snapshot đầu/cuối chứng minh không có delta nội dung quan sát được; không dùng nó để khẳng định toàn bộ lịch sử mọi lần ghi. Thay đổi cấu hình core.abbrev được thực hiện đúng yêu cầu trước đo.

Các phần **KHÔNG ĐO ĐƯỢC**: Windows CI/local, Ubuntu CI trên exact head, và tái hiện bằng quyền hệ điều hành thật sau hạ quyền (setup EPERM). Không dùng kết quả CI của head cũ hoặc lời khai executor để đánh dấu đạt. Những hướng liên quan nội dung nhạy cảm không được dựng thêm. Không có thay đổi mã nguồn trong checkout được review; các script và mutant là hiện vật thử trong sandbox. Verdict này không cấp quyền merge/land.
<!-- VERDICT-L2-KET-THUC -->

### Lượt 3 — sha256 `4c786b0dac87602e2cceda698dd4973891d546c7e6391b9f59d0bf1cbcba388b`

<!-- VERDICT-L3-BAT-DAU -->
Verdict: request_changes
Reviewed commit: 8d9e3e3b55897575b9e69a13f5d1a4f3ff6c9fde
Spec sha256: d5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d

Kết luận cuối: **request_changes** vì còn **một finding P3 về chốt hồi quy OSError** (F3 bên dưới). F1/P2 và F2/P3 của lượt 2 đều **ĐÃ VÁ THẬT**. Không tìm thấy lỗi runtime mới trong phần thay đổi qua các phép đo đã chạy. Head đạt toàn suite `97/97 · 149/149 · 2/2`, cổng thật rc=0/tổng 306. Mutant thu hẹp helper mới chỉ còn bắt PermissionError vẫn sống qua toàn suite, dù EIO/ESTALE trên mutant thoát traceback; đây là bằng chứng thiếu chốt, không phải lời khẳng định head đang bắt sai. Chi tiết, lệnh và output được ghi tăng dần dưới đây.

## Phạm vi

Review độc lập packet #1021 r2, lượt 3. Checkout `cay-kho/` chỉ đọc mã nguồn; bản sao đầy đủ cây, fixture và log đặt trong sandbox. Cấu hình `core.abbrev=7` theo chỉ thị. Mọi tiến trình đo dùng `PYTHONDONTWRITEBYTECODE=1`, fixture Git cô lập bằng `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null`.

Windows CI/local và Ubuntu CI exact head: chưa có phép đo độc lập; không nhận lời khai executor là kết quả đo. Không cấp quyền merge/land.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| Finding lượt 2 | Kết luận | Bằng chứng chạy lại trên head mới |
|---|---|---|
| F1/P2 `loi-do-liet-ke-thu-muc-thoat-traceback` | **ĐÃ VÁ THẬT** | `review_new.py error-child head {kiem,sinh} {stat-os,access}`: 4/4 rc=2/không traceback, có hit. Bản đồ I/O bên dưới kiểm cả guard, helper, `.git`, liệt kê và đọc/băm. |
| F2/P3 `loi-do-thieu-chot-ngoai-le-lap-trinh` | **ĐÃ VÁ THẬT** | `runtime`/`value` ở iterdir truyền ra; `boundary_oracle.py head` rc=0; `new_mutate.py broad`/`broad_literal`: c100 `giet_that`, c18 sạch. Tracer chốt (7) đủ 4 hit/đúng đối tượng. |

Không finding cũ nào bị giữ là VÁ HỜ hoặc CHƯA VÁ. F3 mới ở cuối là thiếu phép phân biệt các lớp con OSError, khác thiếu chốt lỗi lập trình của F2.


## Đợt 1 — neo và tái hiện lượt 2

`evidence/preflight.json`: `git rev-parse HEAD HEAD^{tree} origin/master` rc=0, lần lượt `8d9e3e3b55897575b9e69a13f5d1a4f3ff6c9fde`, `97e0d90fb6dcda86076272c951a44e1ff79ff554`, `757bde561d09738858506aecf5de2f050a5f0d5e`; detached (`symbolic-ref` rc=1/rỗng), không nông (`false`), `.git` là thư mục, status rỗng. SHA-256 SPEC khớp neo.

Script lượt 2 được chép ra gốc sandbox để `ROOT=parent(__file__)` trỏ đúng nơi. `review_new.py` và `boundary_oracle.py` giữ nguyên byte. `new_mutate.py`/`mutate.py` chỉ đổi mốc `if not tm.is_dir()` sang `if not _hoi_trang_thai(tm.is_dir, tm)`; `probe.py` thêm `c100_` vào danh sách ca; `integrity.py` đổi mốc diff lượt trước từ `99c463d`/`DIFF-LUOT2.patch` sang `5efa311`/`DIFF-LUOT3.patch`. Không chỉnh oracle để nhận kết quả mới.

- F1 **ĐÃ VÁ THẬT** ở phép tái hiện cũ: `python3 review_new.py error-child head {kiem,sinh} {stat-os,access}` — cả 4 tiến trình rc=2, có `REVIEW_FAULT_HIT: stat-os`, stderr `KHÔNG ĐO ĐƯỢC: không đọc được trạng thái .../ops/reviews (PermissionError...)`, không traceback. Log `evidence/rerun-head-*.{stdout,stderr,json}`. Lỗi liệt kê muộn (`late`) cũng rc=2 trên hai đường.
- F2 **ĐÃ VÁ THẬT** ở phép tái hiện cũ: `python3 review_new.py error-child head {kiem,sinh} {runtime,value}` — cả 4 tiến trình rc=1, traceback kết thúc bằng đúng `RuntimeError`/`ValueError: review programming fault`; lỗi lập trình không bị đổi thành KhongDoDuoc. `python3 boundary_oracle.py head` rc=0, hai đường `propagated_same_error=true, hit=1, restored=true`.
- `python3 new_mutate.py broad` và `broad_literal`: c98/c99/c89 `qua`, **c100 `giet_that`**: `lỗi lập trình ở iterdir [] bị nuốt/đổi ... được không ngoại lệ`, đối chứng c18 `[true, ""]`. `boundary_oracle.py mut-broad` và `mut-broad_literal` đều rc=1, có hit=1 nhưng bị đổi thành rc=2. Đây là chết đúng chốt c100, không lấy lỗi mất mốc m147 làm tín dụng.

Các lệnh đo dùng tiền tố môi trường đã nêu. Full suite và bản đồ I/O vẫn đang chạy; chưa kết luận cuối.


## Đợt 2 — tiêu chí và bản đồ hệ tệp

`python3 probe.py head behaviors` (log `head-behaviors` và từng `fixture-head-*`): C1a rc=1, `tổng 2`, nêu x đuôi hoa; only-x rc=1, `tổng 1`, không thông báo không có tệp; C1b rc=2, stderr nêu x, không traceback, không có dòng tổng. Base đo lại: C1a `tổng 1`, only-x rc=2/không có tệp, C1b rc=1/bỏ x. Cặp tên chỉ khác hoa thường đếm 2 ở head. Thư mục đuôi hoa tới bước băm và rc=2.

`python3 mutate.py exact --behaviors`: c98/c99 `giet_that`, đối chứng c18 sạch; mutant bỏ x ở C1a/C1b/only-x. `python3 mutate.py isfile --behaviors`: c89 `giet_that` (rc=1 thay rc=2), đối chứng c18 sạch. `python3 mutate.py glob --behaviors`: c98/c99 `giet_that`, đối chứng c18 sạch; c100 `gian_giao` vì không còn gọi iterdir, KHÔNG lấy tín dụng này làm chết mutant. C3 được chứng minh bởi c98.

C6: `python3 measure.py head gate` và `base gate`: rc=0, `253 ĐẠT v2 · 11/11 miễn trừ ... · 42 NỢ ... · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 306`, `TỔNG: ĐẠT`. Lệnh đếm riêng dùng `os.listdir` (log `count-head`, `count-base`) cho `casefold_suffix 306` và `exact_suffix 306`. `python3 ops/bien_nhan_v2.py --root . --sinh-no` trên head/base đều rc=0, `# 42 tệp`.

C9: `git diff --numstat 757bde5..HEAD` chỉ hai tệp: `40 5 ops/bien_nhan_v2.py`, `262 0 ops/bien_nhan_v2_test.py`; `git diff --check` rc=0/rỗng. Ruff `--no-cache --select F` head/base cùng rc=1/cùng F541 tại test:1677, output byte-identical nên delta 0. Doctrine-scan head/base rc=0, `đã quét 10 tệp, 0 chỗ chép doctrine`. `rg -n 'glob\("\*\.receipt\.yaml"\)' ops/bien_nhan_v2.py`: head rc=1/0 dòng; base 2 dòng (1442/1601); mut-glob 1 dòng (116). Dương tính đối chứng là C1a/C1b ở trên, không suy từ vế âm.

### Bản đồ đầy đủ các callsite I/O của mã sản phẩm

Liệt kê độc lập bằng AST (`evidence/fs-call-inventory.json`) và theo các lời gọi từ `main` → `kiem`/`_sinh_no`, gồm bước import nguồn provider và nhánh đọc bằng chứng sau receipt. Bảng dưới đo từng callsite; lệnh cho MỖI ô: `python3 fs_probe.py <head|base> <kiem|sinh> <site>`. Log đầy đủ `evidence/fs-<tree>-<mode>-<site>.{stdout,stderr,json,result.json}` ghi vị trí, hit và khôi phục. `python3 fs_matrix.py` chạy 52 tiến trình độc lập, tất cả có hit dương, khôi phục hàm gốc. Lỗi tiêm là PermissionError thuộc OSError. Không khẳng định đã tiêm mọi syscall bên trong thư viện/importer/Git; đã đo mọi callsite I/O tường minh của tệp sản phẩm trong hai luồng.

| Site và dòng head | Phạm vi / thao tác | Head đo mới | Base đo mới |
|---|---|---|---|
| `provider-resolve` (235) | Không đổi; resolve đường dẫn module trước import nguồn | kiem: rc=1, hit=1, traceback; sinh: rc=1, hit=1, traceback | kiem: rc=1, hit=1, traceback; sinh: rc=1, hit=1, traceback |
| `provider-launcher` (240) | Không đổi; đọc launcher.py | kiem: rc=2, hit=1, không traceback; sinh: rc=0, hit=1, không traceback | kiem: rc=2, hit=1, không traceback; sinh: rc=0, hit=1, không traceback |
| `provider-agents` (244) | Không đổi; đọc AGENTS.md | kiem: rc=2, hit=1, không traceback; sinh: rc=0, hit=1, không traceback | kiem: rc=2, hit=1, không traceback; sinh: rc=0, hit=1, không traceback |
| `provider-protocol` (244) | Không đổi; đọc PROTOCOL_DA_PHIEN.md | kiem: rc=2, hit=1, không traceback; sinh: rc=0, hit=1, không traceback | kiem: rc=2, hit=1, không traceback; sinh: rc=0, hit=1, không traceback |
| `main-resolve` (1581) | Không đổi; resolve --root trước try | kiem: rc=1, hit=1, traceback; sinh: rc=1, hit=1, traceback | kiem: rc=1, hit=1, traceback; sinh: rc=1, hit=1, traceback |
| `guard-isdir` (1471) | Đổi lượt 3; is_dir/stat ops/reviews ở guard kiem | kiem: rc=2, hit=1, không traceback | kiem: rc=1, hit=1, traceback |
| `helper-isdir` (113) | Helper thêm ở packet; bọc lỗi lượt 3; is_dir/stat ops/reviews ở selector (đo riêng cả lần thứ hai trong kiem) | kiem: rc=2, hit=1, không traceback; sinh: rc=2, hit=1, không traceback | Không có callsite này; đối chứng glob ở listing_probe |
| `git-exists` (1472) | Đổi lượt 3; exists/stat .git khi thiếu ops/reviews | kiem: rc=2, hit=1, không traceback | kiem: rc=1, hit=1, traceback |
| `listing` (116) | Đổi glob thành iterdir trong packet; liệt kê thư mục; lỗi ngay và lỗi giữa iterator | kiem: rc=2, hit=1, không traceback; sinh: rc=2, hit=1, không traceback | Không có callsite này; đối chứng glob ở listing_probe |
| `receipt-hash` (677 → 1496/1641) | Không đổi; read_bytes để băm receipt | kiem: rc=2, hit=1, không traceback; sinh: rc=2, hit=1, không traceback | kiem: rc=2, hit=1, không traceback; sinh: rc=2, hit=1, không traceback |
| `receipt-text-kiem` (1497) | Không đổi; read_text receipt ở kiem | kiem: rc=2, hit=1, không traceback | kiem: rc=2, hit=1, không traceback |
| `receipt-text-sinh` (1640) | Không đổi; read_text receipt ở --sinh-no | sinh: rc=2, hit=1, không traceback | sinh: rc=2, hit=1, không traceback |
| `grafts-exists` (1214) | Không đổi; exists/stat .git/info/grafts qua _kho_lanh | kiem: rc=2, hit=42, không traceback | kiem: rc=2, hit=42, không traceback |
| `run-lstat` (1279) | Không đổi; lstat run_json qua _vang | kiem: rc=0, hit=29, không traceback | kiem: rc=0, hit=29, không traceback |
| `run-text` (1434) | Không đổi; read_text run_json | kiem: rc=2, hit=29, không traceback | kiem: rc=2, hit=29, không traceback |
| `verdict-isfile` (1295) | Không đổi; is_file/stat verdict_path | kiem: rc=2, hit=29, không traceback | kiem: rc=2, hit=29, không traceback |
| `verdict-text` (1298) | Không đổi; read_text verdict_path | kiem: rc=2, hit=29, không traceback | kiem: rc=2, hit=29, không traceback |
| `git-run` (843) | Không đổi; subprocess.run trong _git | kiem: rc=2, hit=506, không traceback | kiem: rc=2, hit=506, không traceback |
| `blob-run` (970) | Không đổi; subprocess.run đọc blob Git | kiem: rc=2, hit=253, không traceback | kiem: rc=2, hit=253, không traceback |
| `history-run` (1176) | Không đổi; subprocess.run trong _chay_git | kiem: rc=2, hit=1, không traceback | kiem: rc=2, hit=1, không traceback |

Các thao tác `root / ...`, `p.name`, `.lower()`, `.endswith()`, `Path.parts`, `is_absolute()`, `sorted(ds)` chỉ xử lý đường dẫn/tên trong bộ nhớ; băm SHA-256 không có I/O ngoài `read_bytes` đã đo. Hai caller selector đổi ở 1476/1636; cả hai dùng một helper. `is_file` ở bảng là kiểm verdict sau receipt, KHÔNG phải lọc receipt.

Đối chứng liệt kê cấp OS: `python3 listing_probe.py` trên head/base, hai đường và control/fail, log `listing-*.json`. Head lỗi scandir rc=2 không traceback; base kiem rc=2/không có tệp, base sinh rc=0/`# 0 tệp` (nuốt lỗi). `review_new.py ... late` ở head cho rc=2 sau khi iterator đã yield một mục, không xuất kết quả nợ dở dang.

Hai lỗi resolve thoát traceback là **có sẵn tại base**, các callsite này không được packet sửa. Đọc nguồn provider lỗi khi sinh nợ vẫn rc=0/#42 ở CẢ head/base; không tính finding mới. `_vang.lstat` nuốt EACCES rồi vẫn thử đọc run_json: ở phép tiêm chỉ-lstat, 29 lần đọc thực còn thành công nên rc=0; phép tiêm `run-text` riêng cho rc=2. Không gọi fallback đọc thành công ấy là lỗi đo bị báo sạch. Các nhánh Git/đọc lịch sử bắt lỗi và rc=2 ở cả head/base. Không yêu cầu packet vá các hành vi có sẵn ngoài phần thay đổi.

## Đợt 3 — c100 và đột biến reviewer

`python3 c100_audit.py <1..7> <rig|runtime|value>`: **21/21 tiến trình rc=0**, mỗi lần tiêm dừng ở một trong bảy lần gọi main khi đang thay Path; sau lỗi `Path.is_dir`, `Path.exists`, `Path.iterdir` đều đúng đối tượng gốc; chạy lại c100 `qua`, đối chứng c18 `[true, ""]`. Không đo thấy rò sang ca sau.

Tracer độc lập (`python3 c100_audit.py trace`, log cuối `c100-trace-final`) ghi 7 lần tiêm; bốn lần RuntimeError của chốt (7) đều đúng đối tượng mốc, hit=1, đủ iterdir/is_dir × kiem/sinh. Bản tracer đầu lỗi KeyError vì tưởng closure giữ biến `ten`; log `c100-trace` được giữ và KHÔNG tính là lỗi sản phẩm. Tracer sửa đọc `goc.__name__`; lần đo trung gian gán cờ từ biến vòng lặp cũ làm nhãn .git sai, nên bản cuối lấy argv từ frame main. Chỉ dùng kết quả tracer cuối.

`python3 extra_mutate.py <tên>` (bản sao đủ cây, từng mutant một tiến trình):

| Mutant | Ca c100 | Ý nghĩa |
|---|---|---|
| helper_empty: lỗi trạng thái trả False | giet_that | Không biến lỗi I/O thành vắng |
| helper_pathless: bỏ đường dẫn và chi tiết lỗi | giet_that | Chốt .git còn kiểm thông báo |
| runtime_replaced: ném RuntimeError mới cùng lời | giet_that | Đo đồng nhất đối tượng, không chỉ kiểu/thông điệp |
| injection_noop | gian_giao | dừng do không tiêm trúng, không tính là bắt lỗi sản phẩm |
| injection_runtime_noop | gian_giao | riêng chốt (7) không thể xanh khi không tiêm trúng |
| runtime_same_message: fixture ném đối tượng khác cùng lời | giet_that | Oracle không nhận RuntimeError giả cùng thông điệp |
| narrow_helper: chỉ bắt PermissionError tại helper mới | qua | **SỐNG TOÀN SUITE**, rc=0/97/97 · 149/149 · 2/2; EIO/ESTALE ở guard/helper/.git thoát traceback trên mutant |
| narrow_listing: chỉ bắt PermissionError tại nhánh liệt kê | qua | **SỐNG Ở CÁC CA ĐÍCH** c98/c99/c100/c89; EIO/ESTALE ở scandir thoát traceback trên mutant. Không chạy toàn suite cho mutant này |

Mọi mutant trên có c18 sạch; log `mut-<tên>-cases.stdout` ghi đầy đủ. `python3 errno_probe.py head <mode> <guard|helper|git|listing> <EIO|ESTALE>`: head rc=2 không traceback tại cả sáu tổ hợp đường đi, hit=1; helper trong kiem tiêm vào lần stat THỨ HAI (attempts=2), phân biệt được với guard. Mutant narrow_helper trả rc=1/traceback cho cả bốn tổ hợp trạng thái; narrow_listing trả rc=1/traceback ở hai đường liệt kê. Đây là lỗi bị đưa vào mutant, chưa phải lỗi runtime của head.


## Đợt 4 — toàn suite trên head

`PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null python3 measure.py head suite` đã xong. Tiến trình thật `python3 ops/bien_nhan_v2_test.py` trong `work/head`: **rc=0, 406.32 s**, `97/97 ca đạt · 149/149 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 131/149 đột biến thường khai đối chứng`, `TỔNG: ĐẠT`. Log `evidence/head-suite.{stdout,stderr,json}`; stderr rỗng. Các m148–m153 đều `giet_that` tại c100, m146/m147 vẫn chết ở c99. Không suy pass chỉ từ rc=0.

Phép tiêm ValueError có hai tầng cần phân biệt: tiêm thẳng vào phương thức Path (`errno_probe.py ... value-method`) truyền ra khỏi helper; tiêm sâu hơn vào `os.stat` có thể bị chính `Path.is_dir`/`Path.exists` đổi thành False. Đối chứng `boundary-base-kiem-{guard,git}-value` có cùng hành vi sẵn ở base. Không coi hành vi của pathlib là helper bắt Exception. Log `boundary-head-*` và `boundary-base-*` lưu hai tầng; RuntimeError ở tầng phương thức vẫn truyền nguyên gốc. Điều này không thay kết luận F2 cũ đã vá thật.


## Bảng tiêu chí cuối

| Tiêu chí | Kết quả | Lệnh / output và giới hạn |
|---|---|---|
| Toàn suite head | **ĐẠT** | `python3 measure.py head suite`: rc=0, `97/97 ca đạt · 149/149 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt`, `TỔNG: ĐẠT`; 406.32 s. |
| C1a | **ĐẠT phần đã đo**; Windows **KHÔNG ĐO ĐƯỢC** | `python3 probe.py head behaviors`: C1a rc=1/tổng 2/nêu x; only-x rc=1/tổng 1; mut-exact giết thật c98. |
| C1b | **ĐẠT phần đã đo**; Windows **KHÔNG ĐO ĐƯỢC** | Cùng lệnh: YAML hỏng đuôi hoa rc=2/nêu x/không traceback/không tổng; mut-exact bỏ x và rc=1/tổng 1. |
| C2 | **ĐẠT phần đã đo**; Windows **KHÔNG ĐO ĐƯỢC** | Full suite c89 ĐẠT; `python3 mutate.py isfile --behaviors`: c89 `giet_that`, c18 sạch. |
| C3 | **ĐẠT trên Linux** | `python3 mutate.py glob --behaviors`: c98 `giet_that`, c18 sạch. Không thêm mutant phụ thuộc nền vào bảng thường. |
| C4 | **KHÔNG ĐO ĐƯỢC** | Không có phép đo/log Windows CI độc lập trên exact head; không dùng lời khai executor. |
| C5 | **KHÔNG ĐO ĐƯỢC** | Không có phép đo/log Ubuntu CI độc lập trên exact head; full suite sandbox không được gọi là CI. |
| C6 | **ĐẠT** | `python3 measure.py head gate`: rc=0/tổng 306/TỔNG: ĐẠT; đếm riêng `os.listdir` cho 306; base cũng 306. |
| C7 | **KHÔNG ĐO ĐƯỢC** | Không chạy Windows local. |
| C8 | **KHÔNG ĐẠT** | Còn F3/P3; verdict request_changes trên exact SHA đã neo. |
| C9 | **ĐẠT** | Ruff F delta 0 (cùng F541 đã có ở base); doctrine-scan rc=0/10 tệp/0 chỗ; diff --check rc=0; đúng hai tệp write set; rg glob 0 dòng với đối chứng base 2/mut-glob 1; numstat +40/−5 và +262/−0. |

## Finding còn mở

| ID | Mức | Slug | Phạm vi | Bằng chứng quyết định |
|---|---|---|---|---|
| F3 | P3 | `loi-do-thieu-chot-oserror-ngoai-permissionerror` | c100 mới và c99 nhánh liệt kê của packet | Mutant thu hẹp helper chỉ bắt PermissionError sống toàn suite; oracle độc lập EIO/ESTALE phân biệt head với cả hai mutant thu hẹp. |

- [P3] `loi-do-thieu-chot-oserror-ngoai-permissionerror`: `ops/bien_nhan_v2_test.py:3789` và `:3803` (c100, phép hỏi trạng thái), cùng `:3733` (c99, liệt kê), bảng đột biến `:4656`/`:4669` — `PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null python3 extra_mutate.py narrow_helper --suite` — tiến trình suite trên bản sao mutant **rc=0, 398.14 s**, `97/97 ca đạt · 149/149 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 131/149 đột biến thường khai đối chứng`, `TỔNG: ĐẠT`; nhưng `python3 errno_probe.py mut-narrow_helper sinh helper EIO` **rc=1**, hit=1, `Traceback ... OSError: [Errno 5] review EIO failure`, trong khi cùng lệnh với `head` rc=2, hit=1, `KHÔNG ĐO ĐƯỢC: không đọc được trạng thái ...`, không traceback — mở rộng test bằng OSError không phải PermissionError và thêm mutant thu hẹp catch phải chết đúng chốt.

HÌNH DẠNG: `loi-do`.

**Vì sao đây là thiếu chốt của phần mới:** `_hoi_trang_thai` tại sản phẩm:88–95 hứa và hiện thực đúng hợp đồng OSError. C100 chỉ tiêm PermissionError/EACCES ở cả is_dir và exists, nên không phân biệt bắt toàn OSError với chỉ bắt PermissionError. Mutant reviewer đặt `OSError = PermissionError` cục bộ trong helper trước `return hoi()`; nghĩa bắt lỗi thu hẹp, vẫn giữ nguyên các mốc văn bản m150/m153. Nó không phá rig, không phá import/parity, không bỏ test, và mọi mutant thường vẫn được báo CÓ RĂNG. Đây là chốt hồi quy thiếu răng cho một phần hợp đồng; xếp P3, **không** xếp P2 runtime vì head đang đúng.

**Đủ các đường của cùng lớp:** `errno_probe.py` đo guard kiem, helper trong kiem (stat lần hai), helper trong sinh nợ, `.git` khi thư mục receipt vắng, và scandir trên hai đường. EIO và ESTALE đều rc=2 ở head. `narrow_helper` phá bốn tổ hợp trạng thái; `narrow_listing` (cùng phép thu hẹp trong selector) còn qua c98/c99/c100/c89 và phá hai tổ hợp liệt kê. Mutant listing chưa chạy toàn suite; không suy rằng nó sống toàn suite. Hai mutant cùng một finding, không tách riêng từng biểu hiện để đẩy sang lượt sau.

**Vá ở đâu và thế nào:** thay đổi test `c100` cho các nhánh is_dir/exists và `c99` cho liệt kê, cùng bảng `_dot_bien`. Không cần đổi mã sản phẩm đang đúng. Giữ các ca PermissionError hiện có và thêm tối thiểu `OSError(errno.EIO, ...)`; kiểm hit dương, rc=2, đúng đường dẫn, không traceback trên tất cả đường liên quan. Thêm mutant `except PermissionError` thay `except OSError` ở mỗi helper, đòi chết tại đúng test trong khi c18 còn sạch. Nếu dùng mutant thay catch trực tiếp, cập nhật mốc rig cho đúng; không lấy lỗi mất neo làm tín dụng. Hai phép thu hẹp tương đương giữ neo đã chạy nằm ở `evidence/mut-narrow_helper.patch` và `evidence/mut-narrow_listing.patch`.

**Ca khóa đã chạy ngoài cây:** `python3 io_boundary_oracle.py head` → rc=0/**12/12**; `... mut-narrow_helper` → rc=1/**4/12** (8 phép lỗi trạng thái bị bỏ bắt); `... mut-narrow_listing` → rc=1/**8/12** (4 phép lỗi liệt kê bị bỏ bắt). Script `io_boundary_oracle.py` gọi mỗi phép tiêm bằng tiến trình riêng, đòi hit=1/rc=2/không traceback. Có thể dùng làm đặc tả phản chứng khi bổ sung c99/c100. Lệnh tạo mutant chỉ chạy lần đầu khi đích chưa có; để chạy lại suite trên hiện vật có sẵn: `cd work/mut-narrow_helper && python3 ops/bien_nhan_v2_test.py` với tiền tố môi trường đã nêu.

**Rủi ro khi vá test:** không chọn ENOENT/ENOTDIR làm lỗi bắt buộc rc=2, vì `Path.is_dir` có thể coi đó là vắng thật; không nới catch thành Exception để chữa test. Giữ chốt vắng thật (sinh nợ rc=0/#0), chốt lập trình đúng đối tượng và finally khôi phục monkeypatch. Tầng tiêm phải rõ: lỗi phát từ os.stat có thể được pathlib xử lý trước helper; EIO đã đo truyền qua thực thi Path thật, nên không dựa riêng vào monkeypatch phương thức để giả định điều đó. `ESTALE` là phép bổ sung đã đo, không bắt buộc làm test phụ thuộc nền này nếu bộ Windows thiếu hỗ trợ tương ứng.

## Tính toàn vẹn và giới hạn cuối

`PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null python3 integrity.py` (log `evidence/integrity-run.{stdout,stderr,json}`, dữ liệu chi tiết `evidence/final-integrity.json`) rc=0. Head/tree/base vẫn đúng các neo; `.git` thường, detached, không nông, core.abbrev=7. Status bao gồm tracked/untracked/ignored của `cay-kho` và bản sao head rỗng; diff worktree/index so HEAD rỗng. Hai tệp write set byte-identical với blob HEAD; DIFF.patch và DIFF-LUOT3.patch byte-identical với git diff tương ứng; SPEC SHA-256 đúng neo. Đây là đối chiếu nội dung đầu/cuối, không phải lời khẳng định quan sát toàn bộ lịch sử ghi.

Tất cả tiến trình đo dùng để kết luận đã hoàn tất, không còn phép thử đang chờ. Windows CI/local, Ubuntu CI exact head và lỗi quyền phần cứng/hệ tệp thật: **KHÔNG ĐO ĐƯỢC**; các lỗi I/O trong bảng là phép tiêm có hit kiểm chứng. Không tự dựng nội dung nhạy cảm, không sửa mã nguồn checkout được review, không cấp quyền merge/land.
<!-- VERDICT-L3-KET-THUC -->

### Lượt 4 — sha256 `076ef6c837d6d580b9697377c2f0311d4365a7ab8fc1f40cb4b76a2cdaf78482`

<!-- VERDICT-L4-BAT-DAU -->
Verdict: approve
Reviewed commit: e9e0048b48ab610fee1246368b4f134c1ac4ae76
Spec sha256: d5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d

Kết luận cuối: **approve** trên đúng commit dòng 2; **0 finding P0/P1/P2/P3 mở**. F3 lượt 3 **ĐÃ VÁ THẬT**, F1/F2 lượt 2 vẫn đóng. Head đạt `97/97 ca · 151/151 đột biến thường · 2/2 tự kiểm`, `TỔNG: ĐẠT`; mutant thu hẹp helper nay đỏ đúng c100 trong toàn suite, mutant thu hẹp liệt kê đỏ đúng c99 ở phép ca đích. Cổng thật rc=0/`tổng 306`, khớp phép đếm độc lập. Các lệnh, output và giới hạn được ghi dưới đây; Windows và CI exact head **KHÔNG ĐO ĐƯỢC**. Verdict này không cấp quyền merge/land.

Rà soát packet #1021 r2, lượt 4. Kết quả được ghi tăng dần. Các phép đột biến chỉ thực hiện trên bản sao đủ cây trong sandbox; mã nguồn `cay-kho/` được giữ nguyên. Mọi tiến trình đo dùng `PYTHONDONTWRITEBYTECODE=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_SYSTEM=/dev/null`; cấu hình `core.abbrev=7` theo chỉ thị.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn đối chiếu: `VERDICT-LUOT3.md` trên `8d9e3e3b55897575b9e69a13f5d1a4f3ff6c9fde` và `VERDICT-LUOT2.md` trên `5efa311fd857f7657a1c687e9ea37693070a37d3`. Không coi lời khai executor hoặc verdict cũ là phép đo trên head hiện tại.

| Finding / lớp cũ | Phân loại trên head mới | Bằng chứng độc lập |
|---|---|---|
| F3/P3 `loi-do-thieu-chot-oserror-ngoai-permissionerror` (lượt 3; hai biểu hiện helper/liệt kê) | **ĐÃ VÁ THẬT** | `extra_mutate.py narrow_helper --suite`: rc=1, 96/97, c100 `giet_that` đúng EIO; `extra_mutate.py narrow_listing`: c99 `giet_that` đúng EIO; c18 đều sạch. `errno_probe.py` đủ EIO/ESTALE, 12/12 ở head rc=2/hit=1/không traceback. Tracer đo đủ cả hai lớp và thử đột biến factory ở Đợt 3 chứng minh m154/m155 có răng riêng. |
| F1/P2 `loi-do-liet-ke-thu-muc-thoat-traceback` (lượt 2) | **ĐÃ VÁ THẬT**, không bị mở lại | `review_new.py error-child head <kiem\|sinh> <stat-os\|access>`: 4/4 rc=2/có hit/không traceback; lỗi liệt kê muộn cũng rc=2. |
| F2/P3 `loi-do-thieu-chot-ngoai-le-lap-trinh` (lượt 2) | **ĐÃ VÁ THẬT**, không bị mở lại | `boundary_oracle.py head` rc=0/2 trên 2 truyền đúng đối tượng; `new_mutate.py broad` và `broad_literal` chết đúng c100, c18 sạch; tracer có đủ bốn RuntimeError mốc. |

Ba lớp lịch sử trên mang HÌNH DẠNG: `loi-do`; 0 lớp/0 biểu hiện còn mở sau phép đối chiếu. Không có finding mới `bo-chon-ung-vien`.

## Nhật ký đo

### Đợt 1 — neo, phạm vi và phép tái hiện

`evidence/preflight.json`: `git -C cay-kho rev-parse HEAD HEAD^{tree} origin/master` rc=0 ⇒ head đúng dòng 2, tree `e1e840c06edf6d93d7ce0a527ca0d8c2d15dcd41`, base `757bde561d09738858506aecf5de2f050a5f0d5e`; `--is-shallow-repository` ⇒ `false`, `.git` là thư mục, HEAD detached, status tracked/untracked/ignored rỗng. SHA-256 SPEC khớp dòng 3. Hai patch được so byte với `git diff`: đều khớp.

`git diff 8d9e3e3..HEAD -- ops/bien_nhan_v2.py` rc=0/rỗng: mã sản phẩm không đổi từ lượt 3. `git diff --numstat 757bde5..HEAD` ⇒ `40 5 ops/bien_nhan_v2.py`, `283 0 ops/bien_nhan_v2_test.py`; đúng hai tệp write set. `git diff --check 757bde5..HEAD` rc=0/rỗng.

Các script `luot3-probe/*.py` được chép nguyên byte ra gốc sandbox để `ROOT=parent(__file__)` trỏ đúng nơi; chưa thay mốc neo/oracle trong `extra_mutate.py`, `errno_probe.py`, `probe.py`, `mutate.py`, `new_mutate.py`, `review_new.py`, `boundary_oracle.py`, `measure.py`. `work/head` và `work/base` là bản sao đủ cây, gồm `.git` thường; base checkout đúng SHA nêu trên. Các log lệnh chạy qua `measure.run` có ba tệp `.json` (lệnh/rc/thời gian), `.stdout`, `.stderr` trong `evidence/`.

`python3 extra_mutate.py narrow_helper --suite`: ca đích **c100 `giet_that`** với thông báo `[]: CLI chết bằng OSError: [Errno 5] I/O error (tiêm, #1021) — đòi mã thoát, không traceback`; c98/c99/c89 qua, c18 `[true, ""]`. Phần toàn suite đang chạy; chưa suy từ phép ca đích sang toàn suite.

`python3 extra_mutate.py narrow_listing`: ca đích **c99 `giet_that`** với thông báo `[]: CLI chết bằng OSError: [Errno 5] I/O error (tiêm, #1021): '…/ops/reviews' — đòi mã thoát, không traceback`; c98/c100/c89 qua, c18 `[true, ""]`. Script báo rc=0 vì ghi quan sát; trạng thái `giet_that` và thông báo trong `mut-narrow_listing-cases.stdout` mới là bằng chứng chết mutant.

`python3 measure.py head gate` (lệnh tương đương ghi trong `head-gate.json`) rc=0: `253 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 306`, `TỔNG: ĐẠT`. Lệnh riêng `python3 -c 'import os; n=os.listdir("ops/reviews");print("casefold_suffix",sum(x.lower().endswith(".receipt.yaml") for x in n));print("exact_suffix",sum(x.endswith(".receipt.yaml") for x in n))'` ⇒ `306`, `306`. Base cũng đạt và đếm 306.

### Đợt 2 — EIO/ESTALE, F1/F2 và khôi phục phương thức

`python3 errno_probe.py <head|mut-narrow_helper|mut-narrow_listing> <mode> <site> <EIO|ESTALE>` chạy đủ sáu tổ hợp: `kiem/guard`, `kiem/helper`, `sinh/helper`, `kiem/git`, `kiem/listing`, `sinh/listing`. Mỗi tổ hợp/mã lỗi là tiến trình riêng. `evidence/errno-summary.json` tổng hợp 36 log: **head 12/12 rc=2, hit=1, không traceback**; `mut-narrow_helper` **8/12 rc=1/traceback** ở bốn tổ hợp trạng thái, 4/12 liệt kê vẫn rc=2; `mut-narrow_listing` **4/12 rc=1/traceback** ở hai đường liệt kê, 8/12 trạng thái vẫn rc=2. Tất cả 36 phép có hit=1. `kiem/helper` có attempts=2, nên đo riêng lần hỏi trạng thái thứ hai, không nhầm với guard. Head lỗi nêu đúng `ops/reviews`/`.git`; mutant kết thúc `OSError: [Errno 5|116] review EIO|ESTALE failure`.

F1 lượt 2: `python3 review_new.py error-child head <kiem|sinh> <stat-os|access>` ⇒ **4/4 rc=2**, `REVIEW_FAULT_HIT: stat-os`, `KHÔNG ĐO ĐƯỢC: không đọc được trạng thái …/ops/reviews (PermissionError…)`, không traceback. Nhánh iterator đã yield rồi lỗi (`late`) cũng rc=2 trên cả hai đường.

F2 lượt 2: `python3 review_new.py error-child head <kiem|sinh> <runtime|value>` ⇒ **4/4 rc=1**, traceback đúng `RuntimeError|ValueError: review programming fault`; không bị đổi thành KhongDoDuoc. `python3 boundary_oracle.py head` rc=0, hai đường `propagated_same_error=true, hit=1, restored=true`. `python3 new_mutate.py broad` và `broad_literal` ⇒ c100 **giet_that**: `lỗi lập trình ở iterdir [] bị nuốt/đổi: đòi RuntimeError mốc đi thẳng ra, được không ngoại lệ`; c98/c99/c89 qua, c18 sạch.

Phép mới `python3 audit_l4.py head <c99|c100> trace` dùng `sys.settrace` quan sát ngoại lệ THỰC SỰ ném từ `hong`/`gia` trong test nguyên trạng, không đếm lần tạo đối tượng chỉ phục vụ thông báo:

| Chốt / phương thức | Đường | PermissionError(EACCES) thực ném | OSError(EIO) thực ném |
|---|---|---:|---:|
| c99 / iterdir | kiem | 1 | 1 |
| c99 / iterdir | sinh | 1 | 1 |
| c100 / is_dir | kiem | 1 | 1 |
| c100 / is_dir | sinh | 1 | 1 |
| c100 / exists(.git) | kiem | 1 | 1 |

Cả hai lệnh rc=0, ca `qua`, mọi `restored=true`. **5/5 lần EIO có `type(ex) is OSError`, `isinstance(ex, PermissionError)=false`, errno=5**; 5 lần EACCES là PermissionError/errno=13. Vì vậy chốt không qua do Python đổi EIO thành PermissionError. Tracer c100 còn đo bốn RuntimeError của chốt (7), đủ iterdir/is_dir × kiem/sinh, tất cả đúng đối tượng mốc.

`python3 audit_l4.py head <c99|c100> cleanup <stage> <rig|runtime|value>`: c99 stage 1..4, c100 stage 1..10, tổng **42/42 tiến trình rc=0**. Tiêm ngắt tại mỗi lần gọi main khi Path đang bị thay; sau ngắt `Path.is_dir`, `Path.exists`, `Path.iterdir` đều đúng đối tượng gốc; chạy lại chính ca `qua`, c18 sạch, kiểm cuối vẫn khôi phục. Có lỗi giàn giáo/ngoại lệ khi cố tình ngắt, không dùng chúng làm tín dụng giết mutant. Không phát hiện rò monkeypatch trong phạm vi các nhánh đã đo.

### Đợt 3 — đột biến mới của phần EIO

`python3 mutate_l4.py <tên>` tạo một bản sao đầy đủ `work/mut4-<tên>` và patch trong `evidence/`; mỗi đột biến chạy tiến trình riêng. `probe.py` chạy c98/c99/c100/c89 và đối chứng c18. Với đột biến tệp test, `focused_l4.py` lấy bằng AST đúng thân đăng ký m154/m155 cùng hàm `do`/các biến của `_dot_bien` hiện tại; giữ nguyên cơ chế giết thật/đối chứng/khôi phục, chỉ chọn hai đăng ký cần đo. Đây là phép đo chọn lọc, KHÔNG được gọi là toàn suite.

| Đột biến reviewer | Kết quả đo | Diễn giải |
|---|---|---|
| `eio_helper_empty`: EIO trong `_hoi_trang_thai` trả False | c100 **giet_that**, c18 sạch | Vẫn rc=2 nhưng thông báo thành “kho thật mà không có”; chốt bắt được SAI NGHĨA, không chỉ so rc. |
| `eio_git_escape`: chỉ EIO ở `.git` được ném lại | c100 **giet_that**, `CLI chết bằng OSError: [Errno 5]…`; c18 sạch | Phân biệt nhánh `.git` với is_dir, không chết ở phép PermissionError trước đó. |
| `eio_listing_empty`: EIO khi liệt kê trả danh sách rỗng | c99 **giet_that**, c18 sạch | Vẫn rc=2 nhưng thông báo thành “không có tệp”; chốt đòi “không liệt kê được”. |
| `c99_duplicate_permission`: đổi errno của factory mới EIO → EACCES | **SỐNG ở bốn ca thường**, nhưng phép m155 **KHÔNG RĂNG / qua**, focused rc=1; m154 còn CÓ RĂNG | Tracer ghi 4 PermissionError, 0 OSError thuần. Bảng đột biến phát hiện sự mất lớp EIO của c99. |
| `c100_duplicate_permission`: đổi errno của OS_LOI mới EIO → EACCES | **SỐNG ở bốn ca thường**, nhưng phép m154 **KHÔNG RĂNG / qua**, focused rc=1; m155 còn CÓ RĂNG | Tracer ghi 6 PermissionError, 0 OSError thuần, bốn RuntimeError; bảng đột biến phát hiện sự mất lớp EIO của c100. |
| `reverse_osloi`: đảo thứ tự hai factory tại cả hai vòng OS_LOI | **SỐNG** ở các ca thường và focused rc=0/2 trên 2 CÓ RĂNG | Đối chứng tương đương: vẫn đủ 3 EIO + 3 EACCES + 4 RuntimeError, Path khôi phục. Không phải lỗi cần giết; thứ tự factory không thuộc hợp đồng. |

Cả sáu mutant có c18 sạch. Hai mutant làm mất EIO chỉ sống ở tầng ca thường; không được mô tả là sống qua toàn suite. Không có mutant sai hành vi sản phẩm nào trong tập mới này sống ở ca đích. Log chi tiết `mut4-*-cases.stdout`, `mut4-*-focused.{stdout,json}`, `mut4-*-trace.stdout`; m154/m155 trên head đối chứng focused rc=0/cả hai `giet_that`.

### Đợt 4 — C1/C2/C3/C9

`python3 probe.py head behaviors` (`head-behaviors` và từng `fixture-head-*`) ⇒ C1a rc=1/`tổng 2`/nêu `x.RECEIPT.YAML`/không `TỔNG: ĐẠT`; chỉ-x rc=1/`tổng 1`/không “không có tệp”; C1b rc=2/stderr nêu x/không traceback/không dòng tổng. Thư mục `X.RECEIPT.YAML` tới bước băm rồi rc=2. Base được đo lại: C1a tổng 1/bỏ x, chỉ-x rc=2/không có tệp, C1b rc=1/bỏ x.

`python3 mutate.py exact --behaviors` ⇒ c98/c99 **giet_that**, c18 sạch; fixture C1a/C1b/chỉ-x bỏ x. `python3 mutate.py isfile --behaviors` ⇒ c89 **giet_that**, `đòi rc=2 nêu tệp hỏng, được rc=1`, c18 sạch. `python3 mutate.py glob --behaviors` ⇒ c98/c99 **giet_that** vì bỏ x, c18 sạch; c100 `gian_giao` vì không gọi iterdir KHÔNG được tính làm tín dụng chết. C3 dựa vào c98 và kết quả fixture, không dựa vào lỗi giàn giáo.

C9: Ruff **đỏ sẵn, delta=0**, không ghi “Ruff sạch”: `python3 -m ruff check --no-cache --select F --output-format json ops/bien_nhan_v2.py ops/bien_nhan_v2_test.py` head/base cùng rc=1, chỉ F541 `f-string without any placeholders`, cột 19 tại cùng dòng nội dung của test; vị trí dịch 1677 → 1678 do import. So chuẩn hóa theo tên tệp/rule/thông báo/cột/nội dung dòng cho delta 0 (`criteria-summary.json`); `python3 -m ruff --version` ⇒ `ruff 0.15.15`. Chỉ đo bare lint theo tiêu chí; không suy đã đo pin/probe CI.

`python3 .claude/dev/packet_loop.py doctrine-scan --root .` head/base rc=0: `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine`. `rg -n 'glob\("\*\.receipt\.yaml"\)' ops/bien_nhan_v2.py` head rc=1/0 dòng, base 2 dòng (1442/1601), mutant glob rc=0/1 dòng (116). Vế dương C1a/C1b đã đo riêng ở trên. `python3 summarize_l4.py` rc=0 đối chiếu các log criterion và cleanup bằng assertion; kết quả `evidence/criteria-summary.json`.

### Đợt 5 — toàn suite và chốt cuối

`PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null python3 measure.py head suite` chạy `python3 ops/bien_nhan_v2_test.py` trong `work/head`: **rc=0, 401.34 s**, stderr rỗng, output:

```text
bien_nhan_v2_test: 97/97 ca đạt · 151/151 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 133/151 đột biến thường khai đối chứng
TỔNG: ĐẠT
```

`python3 extra_mutate.py narrow_helper --suite` đã hoàn tất phần suite trên bản sao mutant: **rc=1, 403.08 s**, stderr rỗng, **96/97 ca đạt · 151/151 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt**, `TỔNG: ĐỎ`. Ca thường duy nhất đỏ:

```text
ĐỎ  c100_LOI_TRANG_THAI_thu_muc_la_rc2_va_LOI_LAP_TRINH_di_thang [giet_that]: []: CLI chết bằng OSError: [Errno 5] I/O error (tiêm, #1021) — đòi mã thoát, không traceback
```

Log `head-suite.{json,stdout,stderr}` và `mut-narrow_helper-suite.{json,stdout,stderr}`. m154/m155 trong head đều **CÓ RĂNG / giet_that** tại đúng c100/c99. Không lấy rc đơn lẻ hoặc việc giàn giáo hỏng làm bằng chứng đạt. Không chạy toàn suite cho narrow_listing vì phép tái hiện được yêu cầu ở mutant ấy là ca đích; không suy số liệu toàn suite cho nó.

## Bảng tiêu chí cuối

| Tiêu chí | Kết quả | Lệnh / output quyết định |
|---|---|---|
| Suite head | **ĐẠT** | `python3 measure.py head suite`: rc=0, 97/97 · 151/151 · 2/2, `TỔNG: ĐẠT`; Đợt 5. |
| C1a | **ĐẠT phần đã đo**; Windows **KHÔNG ĐO ĐƯỢC** | `probe.py head behaviors`: rc=1/tổng 2/nêu x; chỉ-x tổng 1/không “không có tệp”. `mutate.py exact --behaviors` giết thật c98, c18 sạch. |
| C1b | **ĐẠT phần đã đo**; Windows **KHÔNG ĐO ĐƯỢC** | Cùng phép behaviors: YAML hỏng đuôi hoa rc=2/nêu x/không traceback; mutant exact bỏ x. |
| C2 | **ĐẠT phần đã đo**; Windows **KHÔNG ĐO ĐƯỢC** | Suite head in `ĐẠT c89_B2_receipt_KHONG_DOC_DUOC_la_rc2_khong_traceback`; `mutate.py isfile --behaviors` ⇒ c89 `giet_that`, c18 sạch. |
| C3 | **ĐẠT phép hoàn nguyên glob được yêu cầu** | `mutate.py glob --behaviors` ⇒ c98 `giet_that` vì tổng 1/bỏ x, c18 sạch. Không đưa mutant glob phụ thuộc nền vào bảng thường. |
| C4 | **KHÔNG ĐO ĐƯỢC** | Không có phép đo độc lập job/runner/log Windows CI trên exact head trong lượt này. |
| C5 | **KHÔNG ĐO ĐƯỢC** | Không có phép đo độc lập job/runner/log Ubuntu CI trên exact head trong lượt này; suite vừa chạy không được nhận là CI. |
| C6 | **ĐẠT** | `measure.py head gate`: rc=0/`tổng 306`/`TỔNG: ĐẠT`; lệnh `os.listdir` riêng đếm 306. Base cũng 306. |
| C7 | **KHÔNG ĐO ĐƯỢC** | Không chạy Windows local; không suy kết quả từ ghi chú lease/ADR hay báo cáo executor. |
| C8 — phần review | **ĐẠT ngưỡng nội dung review** | 0 P0/P1/P2/P3 mở, exact reviewed SHA đúng dòng 2; lượt cuối theo assignment. Các cổng CI/Windows chưa đo không được coi đã đạt; không cấp quyền merge/land. |
| C9 | **ĐẠT** | Ruff F delta 0; doctrine rc=0/10 tệp/0 chỗ; diff-check rc=0; glob 0 dòng; numstat đúng hai tệp +40/−5 và +283/−0. Đợt 1/4 và `criteria-summary.json`. |

## Bảng finding cuối

| Mức | Số finding mở | Vị trí / tái hiện / hướng vá |
|---|---:|---|
| P0 / P1 / P2 / P3 | **0 / 0 / 0 / 0** | Không có finding mới cần vá trong phạm vi đã đo. Bằng chứng đóng ba lớp lịch sử nằm ở bảng đối chiếu và Đợt 1–5. |

Không tạo mục `[P0..P3]` hay gán `HÌNH DẠNG` cho một lỗi không tồn tại. Các mutant tương đương hoặc chỉ sống ở một tầng được phân biệt rõ tại Đợt 3; không che mutant sống, cũng không biến đối chứng tương đương thành finding.

## Toàn vẹn cuối và giới hạn

`python3 integrity.py` qua `measure.run('integrity-run', ...)`: **rc=0**; `evidence/final-integrity.json` ghi lại lệnh và kết quả. Head/tree/base không đổi so neo ban đầu, detached, không nông, `core.abbrev=7`. Status gồm tracked/untracked/ignored của `cay-kho` và `work/head` rỗng; diff worktree/index so HEAD rỗng. Hai tệp write set byte-identical với blob HEAD; DIFF.patch và DIFF-LUOT4.patch byte-identical với diff tương ứng; SPEC giữ đúng SHA-256 dòng 3. Đây là đối chiếu nội dung tại hai mốc, không phải lời khẳng định đã quan sát toàn bộ lịch sử ghi.

`integrity.py` là script cũ duy nhất được chỉnh: mốc `previous-head` từ `99c463d` thành `8d9e3e3`, diff lượt từ `5efa311`/`DIFF-LUOT3.patch` thành `8d9e3e3`/`DIFF-LUOT4.patch`, cùng tên khóa assert tương ứng. Không đổi oracle kiểm toàn vẹn. `evidence/adapter-integrity.patch` giữ diff; `probe-provenance.json` ghi SHA-256 và xác nhận **15/16 script cũ nguyên byte**. Các script mới là `audit_l4.py`, `focused_l4.py`, `mutate_l4.py`, `summarize_l4.py`.

Tất cả tiến trình đo dùng cho kết luận đã hoàn tất. Các lỗi I/O được nêu là phép tiêm có hit kiểm chứng, không phải đo sự cố phần cứng/quyền truy cập thật. Windows CI/local và Ubuntu CI exact head: **KHÔNG ĐO ĐƯỢC**. Không dùng lời khai executor thay số đo, không sửa mã nguồn checkout được review, không cấp quyền merge/land.
<!-- VERDICT-L4-KET-THUC -->
### Lượt 5 — sha256 `d0bebd7fff8951937823d2cbf00b94874a8c35792ebecd8abc98d60f9f3ef46f`

<!-- VERDICT-L5-BAT-DAU -->
Verdict: request_changes
Reviewed commit: 3883b607c2167758065e408f0fa6eeb580472015
Spec sha256: d5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d

Kết luận: **request_changes**. Merge giữ đủ thay đổi hai bên; suite head đạt **98/98 · 151/151 · 2/2**, F1/F2/F3 cũ vẫn đóng. Còn **1 lớp P1 ở kiểm thử cửa sổ M4 của c88**: mutant làm sai biên đầu tệp vẫn qua toàn suite; mutant bỏ citation liền sau cũng qua toàn bộ 98 ca thường. Chỉ ghi trong sandbox, không sửa mã nguồn checkout được review. Chi tiết, giới hạn và gợi ý vá có bằng chứng bên dưới.

## Nhật ký đo tăng dần

Quy ước tái hiện: chạy từ gốc sandbox; mọi tiến trình đo dùng `PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null` (wrapper `measure.py` còn đặt UTF-8). `git config core.abbrev 7` được đặt trước phép đo và được giữ trong các bản sao. Log `.json` cạnh `.stdout/.stderr` ghi lệnh, cwd, rc và thời gian thật. Rc=0 của script thu quan sát không tự có nghĩa mutant chết; verdict dùng trạng thái ca và đối chứng cụ thể.

Đợt 1: `evidence/preflight.json` lưu lệnh/rc/output. Reviewed tree: `c25e25dbcfbfd2a8f584199ec2d6e6dfc26c69a6`. Head, cha 1, cha 2 và origin/master đúng assignment; SPEC khớp băm. `git diff --name-only b29da0b..HEAD` đúng hai tệp write set; `git diff --check b29da0b..HEAD` rc=0.

## GIẢI XUNG ĐỘT

`PYTHONDONTWRITEBYTECODE=1 python3 audit_merge.py` rc=0 (`evidence/merge-audit.json`). Ba patch đầu vào khớp byte với các lệnh `git diff` tương ứng. `git merge-file -p <e9e0048> <merge-base> <b29da0b>` trên tệp test phát đúng **một** xung đột; giữ tuần tự cả hai thân, đổi tên định nghĩa/đích m142/docstring c99 ⇒ **byte-identical với HEAD**. Merge-base là `757bde561d09738858506aecf5de2f050a5f0d5e`.

- So cha 1: `ops/bien_nhan_v2.py` không đổi byte. Tệp test nhận ba import contextlib/io/traceback, ca c98 của #1037, các hàm in chi tiết/vị trí ngoại lệ, tham số `chi` và dây in của `_dot_bien`; thêm đúng ba thay tên đã nêu. Ngoài `_chay_1` và `_dot_bien`, mọi hàm cũ còn nguyên sau chuẩn hóa tên.
- So cha 2: nhận đúng thay đổi #1021 của `DIFF.patch`: mã sản phẩm +40/−5, test +281/−0. Mọi hàm #1037 nguyên byte; chỉ `_dot_bien` được bổ sung đăng ký m142–m155. Không mất hàm của bên nào.
- Đếm AST: cha 1 **97 ca / 153 đăng ký**, cha 2 **95 ca / 139 đăng ký**, HEAD **98 ca / 153 đăng ký**. Tên ca, số tiền tố ca và tên đột biến không trùng. 153 gồm 151 thường + 2 tự kiểm (đã đối chiếu bằng output suite bên dưới). Mọi đăng ký của từng cha khớp AST sau đổi tên; chuỗi `c98_chon_bien_nhan_` vắng hoàn toàn ở head.

`python3 run_checks.py` đã chạy riêng `_dot_bien(chi={tên})` cho **m140–m155**, mỗi tên một tiến trình: tất cả rc=0, đúng một hàng, `giet_that`, có đối chứng. m142 trỏ c101; m147/m155 trỏ c99; m154 trỏ c100. Bốn lượt tiêm AttributeError vào đúng ca đích của m142/m147/m154/m155 đều in `KHÔNG RĂNG`, `chi tiết [tin_dung_gia]`, `AttributeError: review_merge_trace_sentinel` và vị trí `focused_merge.py:11 in reviewer_throw`; không nhận tín dụng giết giả. Log `evidence/focused-*.{json,stdout,stderr}`; phép focused không được gọi là toàn suite.

## C88 CỬA SỔ M4 — phép đo hành vi head

`python3 window_probe.py head --gate` (qua `measure.run`, `evidence/window-head.*`) rc=0: **71/71 phép trực tiếp và 71/71 fixture git thật qua cổng đúng kỳ vọng**. Ma trận độc lập đặt provider/citation ở khoảng cách −3…+3, dòng giữa; đầu tệp j=0 và cuối tệp; một/hai/ba dòng; dòng trống, khoảng trắng/tab, nhiều khai báo cùng dòng và gần nhau. Expected được ghi riêng trong script theo hợp đồng ba dòng. Output: `SUMMARY {"total":71,"direct_pass":71,"gate_pass":71,"failed":[]}`. Chưa thấy lỗi hành vi sản phẩm ở head trên tập này. Kết quả đột biến bên dưới cho thấy ma trận head xanh chưa chứng minh c88 đủ răng.

## Tiêu chí đã đo

`python3 run_checks.py` ghi lệnh/rc/output vào `evidence/`:

- C1a/C1b: `probe.py head behaviors` chạy fixture thật; hai tệp hợp lệ YAML sai schema ⇒ rc=1/tổng 2/nêu x; chỉ x ⇒ rc=1/tổng 1; YAML hỏng đuôi hoa ⇒ rc=2/stderr nêu x/không traceback. Log `head-behaviors.*` và `fixture-head-*`.
- C6: head và base chạy `python3 ops/bien_nhan_v2.py --root .` đều rc=0, tổng 306, `TỔNG: ĐẠT`. `receipt-count.stdout` đếm riêng casefold=306/exact=306.
- C9: Ruff F **đỏ sẵn**, head/base cùng F541 ở cùng nội dung dòng; `ruff-delta.json` xác nhận delta=0. Doctrine head/base rc=0: 10 tệp, 0 chỗ chép doctrine. `no-glob` rc=1/0 dòng. Không gọi Ruff sạch.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn lịch sử: `VERDICT-LUOT4.md` trên `e9e0048b48ab610fee1246368b4f134c1ac4ae76`. Kết quả dưới đây đo lại trên head mới, không lấy verdict cũ làm bằng chứng pass.

| Lớp lịch sử | Kết quả trên head mới | Phép đo |
|---|---|---|
| F1/P2 `loi-do-liet-ke-thu-muc-thoat-traceback` | Vẫn đóng trong phạm vi đã đo | `run_old_findings.py`: PermissionError ở trạng thái/liệt kê và iterator yield rồi lỗi trên cả kiem/sinh ⇒ rc=2, không traceback; `mutation_probe.py m147` trên bản sao đầy đủ ⇒ c99 giet_that, c18 sạch. |
| F2/P3 `loi-do-thieu-chot-ngoai-le-lap-trinh` | Vẫn đóng trong phạm vi đã đo | `boundary_oracle.py head` ⇒ cả hai đường truyền đúng đối tượng RuntimeError, hit=1, restored=true; `review_new.py error-child head <kiem\|sinh> <runtime\|value>` ⇒ rc=1/traceback đúng lỗi lập trình; focused m152/m153 chết đúng c100. |
| F3/P3 `loi-do-thieu-chot-oserror-ngoai-permissionerror` | Vẫn đóng trong phạm vi đã đo | `errno_probe.py head <mode> <site> <EIO\|ESTALE>`: 12/12 tiến trình rc=2, hit=1, không traceback, đủ guard/helper/git/listing. `mutation_probe.py m154` ⇒ c100 giet_that vì OSError errno 5; m155 ⇒ c99 giet_that vì errno 5; c18 đều sạch. Tracer c99/c100 xác nhận thực sự ném OSError thuần, không chỉ PermissionError. |

Cả ba lớp F1/F2/F3 có hình dạng `loi-do`; không mở lại bởi merge. Log chi tiết `evidence/errno-*`, `old-*`, `boundary-head.*`, `trace-*`, `mut-m147*`, `mut-m154*`, `mut-m155*`. Các lỗi I/O là lỗi tiêm có hit kiểm chứng.

### C2/C3 và chạy lại đột biến trên bản sao đủ cây

`python3 run_mutants.py` chạy mỗi mutant một tiến trình. `work/mutation` là bản sao đủ cây gồm `.git`; mỗi tiến trình sửa đúng mẫu duy nhất trên bản sao, chạy ca/đối chứng khi mutant còn hiệu lực, băm lại, rồi phục hồi. Patch và kết quả giữ trong `evidence/mut-*.patch` và `mut-*-result.json`.

| Mutant | Ca đích / đối chứng |
|---|---|
| m142 — so đuôi chính xác | c101 **giet_that**; c99 cũng đỏ; c18 sạch |
| m143 — thêm is_file | c89 **giet_that**; c18 sạch; C2 đạt |
| m147 — bỏ bắt lỗi liệt kê | c99 **giet_that**; c18 sạch |
| m154 — chỉ bắt PermissionError ở trạng thái | c100 **giet_that** với EIO; c18 sạch |
| m155 — chỉ bắt PermissionError ở liệt kê | c99 **giet_that** với EIO; c18 sạch |
| glob — hoàn nguyên selector | c101/c99 **giet_that**, c18 sạch; C3 đạt. c100 là `gian_giao` do không gọi iterdir, **không tính** làm tín dụng giết. |

### Toàn suite head đã hoàn tất

`PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null python3 measure.py head suite` chạy lệnh `python3 ops/bien_nhan_v2_test.py` trong bản sao đủ cây `work/head`: **rc=0, 375.16 s**, stderr rỗng (`evidence/head-suite.*`):

```text
bien_nhan_v2_test: 98/98 ca đạt · 151/151 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 133/151 đột biến thường khai đối chứng
TỔNG: ĐẠT
```

So cha 2 chi tiết mã sản phẩm: thêm `_hoi_trang_thai` (chỉ đổi OSError thành KhongDoDuoc) và `_chon_bien_nhan` (iterdir/lower/endswith/sorted, không lọc is_file); kiem dùng helper cho hai câu hỏi trạng thái và selector, thông báo rỗng nêu phép so không phân biệt hoa thường; `_sinh_no` dùng cùng selector. Test thêm import errno, c101/c99/c100 và m142–m155. Đây là toàn bộ delta #1021; `audit_merge.py` đã chứng minh phần #1037 còn nguyên.

### C88 — 40 đột biến reviewer

`python3 run_mutants.py` / `python3 mutation_probe.py <tên>`; bảng máy `evidence/window-mutations-summary.json`. **40/40** mutant có đối chứng c18 sạch và băm nguồn không đổi suốt phép đo. Mỗi mutant chạy tiến trình riêng trên bản sao đủ cây. Không tuyên bố tập hữu hạn này vét cạn mọi biểu thức Python tương đương.

| Nhóm | Số | Kết quả ca c88 / oracle độc lập |
|---|---:|---|
| Cận trái L ∈ {−3,−2,−1,0,+1}, cận phải R ∈ {0,1,2,3,4}, `max(0,j+L):j+R`, trừ cặp đúng (−1,2) | 24 | Tất cả c88 **giet_that**; bao gồm nới/thu hẹp/lệch sang trước/sau và cửa sổ rỗng |
| Lấy mọi dòng trước / mọi dòng sau / toàn tệp / loại dòng trắng / bỏ dòng khai ở EOF | 5 | Tất cả c88 **giet_that** |
| Nới riêng provider hoặc riêng citation sang trước/sau hai dòng | 4 | Tất cả c88 **giet_that**; xác nhận cả bốn phản chứng cũ đã được khóa |
| Bỏ provider trên chính dòng khai; bỏ citation dòng trước | 2 | c88 **giet_that** |
| `no_clamp`: bỏ chặn chỉ số âm ở đầu tệp | 1 | **SỐNG** ở c88/c79/c83; oracle chỉ 66/71 đúng |
| `skip_first`: bỏ qua khai báo j=0 | 1 | **SỐNG** ở c88/c79/c83; oracle chỉ 63/71 đúng |
| `citation_drop_next`: bỏ citation dòng ngay sau | 1 | **SỐNG** ở c88/c79/c83; oracle chỉ 65/71 đúng |
| `citation_drop_self`: bỏ citation cùng dòng | 1 | SỐNG ở c88 nhưng **c79 giet_that**, nên không phải lỗ hổng không được bộ ca bắt |
| `reverse_equivalent`: đảo thứ tự ba dòng trong cửa sổ | 1 | SỐNG; oracle 71/71. Tương đương với hai phép `any`, không phải lỗi |

Tổng: c88 giết 35/40; 5 sống tại c88 gồm 1 tương đương, 1 được c79 bắt, 3 mutant sai hành vi cần kiểm tiếp toàn bộ ca. Kết quả xác nhận cuối: `no_clamp` sống qua toàn suite 98/98 · 151/151 · 2/2; `citation_drop_next` sống qua toàn bộ 98/98 ca thường. Chỉ mutant đầu đã được chạy cả bảng đột biến; không gán kết quả whole-suite đó cho mutant thứ hai.

## Bảng finding — cập nhật sau phép đo ma trận

- [P1] bien-ngoai-cua-so-surface-chua-co-rang: `ops/bien_nhan_v2_test.py:2981` (ma trận c88), `:3001` (prefix che j=0); chốt sản phẩm `ops/bien_nhan_v2.py:1310–1311` — `python3 mutation_probe.py no_clamp` và `python3 mutation_probe.py citation_drop_next` — c88/c79/c83 đều `qua`, c18 sạch, trong khi oracle độc lập lần lượt chỉ 66/71 và 65/71 — bổ sung fixture thật bắt đầu tại dòng 0, citation ở dòng ngay sau và đăng ký đột biến riêng; gợi ý đã đo trong `HINT.patch`.

  HÌNH DẠNG: `bo-chon-ung-vien`.

  **Một lớp, hai biểu hiện còn mở** (biên đầu tệp; citation phía sau). Giữ slug lịch sử để nối P1 lượt 7; không coi số dòng tăng hoặc m140/m141 xanh là đóng mọi biên của lớp này. Đây là thiếu răng kiểm thử; chưa thấy sản phẩm head sai trên 71 fixture độc lập.

  **Biểu hiện A — đầu tệp.** Tất cả nội dung c88 đều được thêm `verdict: approve` và một dòng trống, nên không có khai báo ở j=0. Mutant `no_clamp` chèn `max = lambda lower, value: value` ngay trước dòng cắt cửa sổ, giữ nguyên dòng neo đột biến cũ: ở j=0 nó lấy chỉ số âm, có thể bỏ lời tự khai sai hoặc đọc sai cửa sổ. `skip_first` là phản chứng cùng biểu hiện. Witness `edge-j0-n3-provider-+1`: dòng 0 là khai báo khác run.json, dòng 1 có provider, dòng 2 trung tính; head có L-SURFACE/rc=1, mutant bỏ qua/rc=0. `window_probe.py mutation --gate` trên bản `no_clamp` (`window-no-clamp.*`) xác nhận **67/71** fixture git thật đúng, bốn fixture ra sai mã; oracle trực tiếp **66/71** vì thêm một ca nhiều khai báo vẫn có một vi phạm khác nên rc chưa phân biệt được. Không dùng rc đơn lẻ để che mất một surface.

  **Biểu hiện B — citation phía sau.** c88 chỉ có citation liền trước, hoặc cách hai dòng; c79 có citation cùng dòng. Không ca nào trong ba ca này bắt việc bỏ riêng citation ở dòng kế tiếp. Mutant `citation_drop_next` chỉ đổi tập xét `_RE_TRICH_DAN`, giữ nguyên tập provider. Witness `text-citation-+1`: provider + khai báo sai ở cùng dòng, citation ở dòng ngay sau; head loại khỏi lời tự khai, mutant báo sai L-SURFACE. Ma trận trực tiếp bắt sáu ca sai, còn c88/c79/c83 đều qua.

  **Hướng vá đã thử trong sandbox.** `HINT.patch` bỏ prefix cố định khỏi các fixture c88 (nhờ đó các hàng sẵn có thực sự chạm j=0), thêm hàng citation liền sau, thêm m156/m157 để khóa hai chốt. `python3 hint_probe.py create` rc=0: c88 head qua; m140/m141/m156/m157 đều `giet_that`, có đối chứng. `hint_probe.py <tên>` thử lại 40 mutant: sau hint, 38 mutant sai bị c88 bắt, `citation_drop_self` bị c79 bắt, `reverse_equivalent` vẫn qua. Không yêu cầu mutant tương đương phải chết. Các log `hint-*` lưu bằng chứng; chưa chạy toàn suite cho HINT và chưa áp HINT vào checkout được review. Executor cần tự tái dẫn xuất, chạy toàn suite/CI trên head mới.

  Ghi nhận lỗi của script reviewer: lần đầu `hint_probe.py citation_drop_self` đòi c88 tự giết dù đã biết c79 bắt mutant này; assertion reviewer sai. Giữ log `initial-hint-citation_drop_self.*`, sửa phép kiểm để ghi và đòi c79 `giet_that`, chạy lại rc=0. Không tính lần lỗi oracle đó là lỗi sản phẩm hay tín dụng giết.

### Xác nhận survivor qua toàn suite

`python3 mutation_probe.py no_clamp --suite` (wrapper `confirm-no-clamp.json`) rc=0. Lệnh con `python3 ops/bien_nhan_v2_test.py` trong cây đầy đủ đang mang đột biến: **rc=0**, stderr rỗng, `evidence/mut-no_clamp-suite.*`:

```text
bien_nhan_v2_test: 98/98 ca đạt · 151/151 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 133/151 đột biến thường khai đối chứng
TỔNG: ĐẠT
```

`mut-no_clamp-result.json` xác nhận băm sản phẩm trước/sau suite giữ nguyên; c18 sạch khi mutant đang hiệu lực. Dòng `max = lambda lower, value: value` chỉ thay clipping cận trái; dòng cắt cửa sổ gốc được giữ để m113/m140/m141 vẫn áp đúng mẫu. Vì thế đây là **SỐNG QUA TOÀN SUITE**, không phải rc=0 do bỏ chạy bảng đột biến hoặc lỗi giàn giáo. Witness git thật ở `window-no-clamp.*` đã chứng minh mutant sai hành vi.

**Kết luận riêng P1 lượt 7:** xác nhận `fc73522` đã vá thật bốn phản chứng ngoài cửa sổ ở khoảng cách ±2 (provider và citation); m140/m141 chết đúng c88, kể cả phép reviewer đổi riêng từng bộ lọc. Tuy nhiên **bác kết luận đóng toàn bộ lớp cửa sổ M4**: biên đầu tệp và citation liền sau vẫn chưa được khóa. Một lớp P1 với hai biểu hiện còn mở; nối cùng slug lịch sử. Việc này thuộc phần c88 được chỉ thị bổ sung cho lượt 5, không phải lỗi giải xung đột #1021/#1037.

## Bảng tiêu chí

| Tiêu chí | Kết quả | Lệnh / output quyết định |
|---|---|---|
| Đúng head/spec/phạm vi | ĐẠT | `preflight.json`, `audit_merge.py`: OID 40 ký tự/băm đúng; hai tệp; diff-check rc=0 |
| Giải xung đột | ĐẠT | `audit_merge.py`: 1 conflict; giữ cả hai + 3 đổi tham chiếu ⇒ khớp byte; 98 ca, 151 thường + 2 tự kiểm; không trùng/tên cũ |
| Suite head | ĐẠT | `measure.py head suite`: rc=0, 98/98 · 151/151 · 2/2, TỔNG: ĐẠT |
| #1037 với m142–m155 | ĐẠT | `focused_merge.py <m142…m155> real` đúng một hàng `giet_that`; 4 phép fake ghi đủ chi tiết/vị trí, `tin_dung_gia`, không được nhận CÓ RĂNG |
| C1a | ĐẠT phần đo; Windows KHÔNG ĐO ĐƯỢC | `probe.py head behaviors`: tổng 2/nêu x/rc=1; chỉ x tổng 1/không “không có tệp”; `mutation_probe.py m142` giết c101 |
| C1b | ĐẠT phần đo; Windows KHÔNG ĐO ĐƯỢC | YAML hỏng đuôi hoa rc=2/stderr nêu x/không traceback; mutant exact chết c101 |
| C2 | ĐẠT phần đo; Windows KHÔNG ĐO ĐƯỢC | c89 qua trong suite; `mutation_probe.py m143` c89 giet_that, c18 sạch |
| C3 | ĐẠT phép hoàn nguyên được yêu cầu | `mutation_probe.py glob` c101/c99 giet_that; c18 sạch; không lấy c100 gian_giao làm tín dụng |
| C4 Windows CI | KHÔNG ĐO ĐƯỢC | Không có phép đo độc lập job/runner/log exact head trong lượt này |
| C5 Ubuntu CI | KHÔNG ĐO ĐƯỢC | Suite vừa chạy không chứng minh job CI; không có phép đo độc lập CI exact head |
| C6 | ĐẠT | Head/base gate rc=0, tổng 306/TỔNG: ĐẠT; os.listdir đếm riêng 306 |
| C7 Windows local | KHÔNG ĐO ĐƯỢC | Không chạy Windows local; không suy kết quả từ lời khai executor |
| C8 nội dung review | KHÔNG ĐẠT | 1 lớp P1 còn mở trong phần c88; request_changes |
| C9 | ĐẠT | Ruff F delta 0 (đỏ sẵn F541); doctrine rc=0/10 tệp/0 chỗ; diff-check rc=0; glob 0 dòng; numstat +40/−5 và +281/−0 |
| C88 hành vi head | ĐẠT tập đã đo | `window_probe.py head --gate`: 71/71 trực tiếp và 71/71 git thật |
| C88 răng kiểm thử | KHÔNG ĐẠT | `no_clamp` sai trên witness nhưng vẫn toàn suite xanh; P1 ở trên |

**Tổng finding mở: P0=0, P1=1 lớp (2 biểu hiện), P2=0, P3=0.** Không cấp quyền merge/land.


### Xác nhận biểu hiện citation và toàn vẹn cuối

`python3 mutation_probe.py citation_drop_next --all-cases` (`evidence/confirm-citation-drop-next.*`) **rc=0, 208.20 s**: `ALL_CASES {"total":98,"passed":98,"failed":[]}`. Băm sản phẩm giữ nguyên, c18 sạch. Đây là toàn bộ **ca thường**, không phải lượt toàn suite có 151 đột biến. `python3 witness_citation.py` dựng lại cùng mutant trên bản sao đầy đủ rồi chạy `window_probe.py focus --gate`: phép kiểm oracle rc=1, **65/71 trực tiếp và 65/71 git thật đúng**, sáu fixture phát hiện hành vi sai; mọi lỗi là L-SURFACE, không phải giàn giáo. Log `window-citation-drop-next.*`, bảng `citation-gate-summary.json`.

`python3 validate_review.py` **rc=0**, output `ALL REVIEW ASSERTIONS PASS; 5 trees clean; 20 inherited scripts unchanged`. `evidence/final-validation.json` đối chiếu tự động số đếm suite, ca đích mutant/đối chứng, 12 phép EIO/ESTALE, tracer, C1/C6/C9, 40 mutant, 40 phép hint, bốn đột biến hint chạy riêng từng tiến trình, cùng snapshot cuối:

- `cay-kho`, `work/head`, `work/focus`, `work/mutation` vẫn ở exact head dòng 2/tree `c25e25dbcfbfd2a8f584199ec2d6e6dfc26c69a6`; `work/base` ở `b29da0bfe3bfb7a7be69136a1c5c40f82c088a93`.
- Cả năm cây: tracked/untracked/ignored sạch, diff worktree/index rỗng, không nông, `core.abbrev=7`; hai tệp nguồn khớp từng byte với blob HEAD. Snapshot đầu ghi tracked/untracked; ignored ở đầu lượt không được ghi riêng. Snapshot cuối không chứng minh toàn bộ lịch sử ghi trong lúc chạy; các bản sao phục vụ đột biến đã được phục hồi sau phép đo.
- SPEC giữ đúng SHA-256 dòng 3; 20 script `luot4-probe` được chép ra gốc sandbox giữ nguyên byte. Các script mới và HINT chỉ nằm trong sandbox. `git apply --check HINT.patch` trên bản sao rc=0; không áp lên `cay-kho`.

Các tiến trình đo đã kết thúc. **Verdict cuối: request_changes**, vì một lớp P1 M4 còn mở; phần giải xung đột và F1/F2/F3 không phát hiện hồi quy. Windows CI/local, Ubuntu CI exact head và toàn suite của HINT: **KHÔNG ĐO ĐƯỢC / chưa chạy**, không được suy là pass. Không cấp quyền merge/land.
<!-- VERDICT-L5-KET-THUC -->

### Lượt 6 — sha256 `7be99282d09817bc318facbd7746ef33fdff70167f677c0107ee00ad18103173`

<!-- VERDICT-L6-BAT-DAU -->
Verdict: request_changes
Reviewed commit: 691cb65388e71afb825aeba3b5cbc5359fc4dac5
Spec sha256: d5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d

Còn **1 finding P3** trong chú thích mới: khẳng định cả hai đột biến từng sống qua toàn suite không đúng với citation_drop_next. Vì ngưỡng yêu cầu hết mọi P0–P3, verdict là **request_changes**. P1 `bien-ngoai-cua-so-surface-chua-co-rang` lượt 5 **ĐÃ VÁ THẬT**: ba phản chứng cũ đều chết tại c88; no_clamp chết qua toàn suite. Head sạch đạt **98/98 · 153/153 · 2/2, TỔNG: ĐẠT**. F1/F2/F3 và phần giải xung đột #1037 không có hồi quy trong các phép đo dưới đây. Windows CI/local và Ubuntu CI exact head: **KHÔNG ĐO ĐƯỢC**. Verdict này không cấp quyền merge/land.

## Neo và cách tái hiện

Các lệnh Python dưới đây chạy từ gốc sandbox, với `PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null`; `measure.run` truyền cùng môi trường cho tiến trình con, thêm UTF-8 và lưu command/cwd/rc/thời gian/stdout/stderr. Các suite chạy lệnh `python3 ops/bien_nhan_v2_test.py` trong cây được ghi ở log. Mọi đột biến reviewer chạy trên cây đủ, mỗi đột biến một tiến trình, có đối chứng khi mutant còn hiệu lực và kiểm băm nguồn trước/sau. Không sửa nguồn trong `cay-kho`.

`python3 preflight.py` rc=0 ([log](evidence/preflight.json)): HEAD và cha đúng chỉ thị, tree `2bfc4623ba0ac56cee9a1766f1bee3ee2faa3a0e`; origin/master = `b29da0bfe3bfb7a7be69136a1c5c40f82c088a93`; không nông, `.git` là thư mục, core.abbrev=7, trạng thái sạch. SPEC khớp băm dòng 3; HINT khớp `994c283d58086efc070a51c6347aca928edae847da153e95cd10f73600340fa9`. DIFF.patch và DIFF-LUOT6.patch khớp byte với git diff tương ứng.

`git -C cay-kho diff --name-only b29da0b..HEAD` chỉ có `ops/bien_nhan_v2.py` và `ops/bien_nhan_v2_test.py`. `git diff --numstat b29da0b..HEAD`: **40/5** và **296/2** (thêm/xóa). `git diff --check b29da0b..HEAD` và `git diff --check` đều rc=0/không output; lệnh và kết quả lưu trong preflight.json.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Không dùng lời khai executor hay verdict cũ làm bằng chứng pass. `python3 run_mutants_l6.py`, `run_old_findings.py`, `run_focused_l6.py`, và `summarize_l6.py` đều hoàn tất rc=0; script cuối kiểm các kết quả con bằng assertion ([bảng máy](evidence/review-summary.json)).

| Lớp/biểu hiện | Phép đo trên head mới | Kết luận |
|---|---|---|
| P1, đầu tệp: no_clamp | `mutation_probe.py no_clamp --suite`: wrapper rc=0; suite con **rc=1**, 97/98 · 153/153 · 2/2, TỔNG: ĐỎ. Chỉ c88 `giet_that`, hàng ix đòi rc=1 được 0; c18 sạch, băm ổn định. | ĐÃ VÁ THẬT |
| P1, đầu tệp: skip_first | `mutation_probe.py skip_first`: c88 `giet_that`, hàng v đòi 1 được 0; c18 sạch. Oracle 63/71 xác nhận hành vi mutant sai. | ĐÃ VÁ THẬT |
| P1, citation dòng sau | `mutation_probe.py citation_drop_next`: c88 `giet_that`, hàng ii-b đòi 0 được 1, đúng L-SURFACE; c18 sạch. Oracle 65/71. | ĐÃ VÁ THẬT |
| F1/P2, lỗi liệt kê thoát traceback | `review_new.py error-child head <kiem\|sinh> <stat-os\|access\|late>`: 6 tiến trình có hit, rc=2, không traceback; iterator yield rồi lỗi cũng được bắt. m147 bị c99 giết thật. | Vẫn đóng |
| F2/P3, chốt ngoại lệ lập trình | `boundary_oracle.py head`: hai đường truyền đúng đối tượng RuntimeError, hit=1, restored=true; RuntimeError/ValueError qua CLI: rc=1, traceback. Focused m152/m153 bị c100 giết thật. | Vẫn đóng |
| F3/P3, OSError ngoài PermissionError | `errno_probe.py head <mode> <site> <EIO\|ESTALE>`: **12/12** có đúng 1 hit, rc=2, không traceback. Tracer c99/c100 thấy OSError thuần errno=5; m154/m155 bị c100/c99 giết thật, c18 sạch. | Vẫn đóng |

Log P1: [suite no_clamp](evidence/mut-no_clamp-suite.stdout), [rc/thời gian](evidence/mut-no_clamp-suite.json), [băm/đối chứng](evidence/mut-no_clamp-result.json), `evidence/wm-{no_clamp,skip_first,citation_drop_next}-result.json`. Log F1/F2/F3: `evidence/old-*`, `errno-*`, `boundary-head.*`, `trace-*`, `wm-m147*`, `wm-m154*`, `wm-m155*`, `focused-*`. Không tính lỗi giàn giáo hay ngoại lệ lập trình thành tín dụng giết.

**Giới hạn lịch sử được làm rõ:** lượt 5 chỉ có bằng chứng toàn suite cho no_clamp; citation_drop_next khi ấy chỉ chạy toàn bộ 98 ca thường. Để kiểm câu chú thích mới “hai đột biến từng sống qua toàn suite”, lượt 6 chạy thêm `python3 historical_citation_suite.py` trên **3883b60** mang citation_drop_next: wrapper rc=0; suite con **rc=1, 98/98 · 150/151 · 2/2, TỔNG: ĐỎ**, băm mutant ổn định ([log](evidence/historical-citation-suite.stdout), [neo](evidence/historical-citation-integrity.json)). m85 báo **KHÔNG RĂNG / gian_giao**, mẫu ` or any(_RE_TRICH_DAN.search(x) for x in cua)` khớp 0 chỗ. Vì vậy citation_drop_next sống qua ca thường, nhưng không phải survivor của **toàn suite xanh**. Đây là lỗi giàn giáo m85, không phải bộ ca cũ bắt được hành vi citation; cũng không được đổi lỗi giàn giáo thành bằng chứng full-suite survivor. Phép đo bổ sung của lượt 6 không được gán ngược thành phép đo đã có ở lượt 5. Chú thích mới sai ở phạm vi bằng chứng này (P3 bên dưới).

## C88 CỬA SỔ M4

`python3 window_probe.py head --gate` qua measure.run: **rc=0**, `SUMMARY {"total":71,"direct_pass":71,"gate_pass":71,"failed":[]}` ([log](evidence/window-head.stdout)). Ma trận độc lập gồm khoảng cách −3…+3, đầu/cuối tệp, một/hai/ba dòng, dòng trắng/tab và nhiều khai báo. Chưa thấy sai hành vi sản phẩm trong tập này.

`python3 c88_rows.py` rc=0: **10/10 hàng đúng, 10/10 phản chứng đảo rc, 10/10 giữ cùng rc khi thử lại tiền tố cũ** ([chi tiết](evidence/c88-rows.json)). Mỗi hàng được đo trực tiếp và qua kho git thật; rc=1 chỉ có L-SURFACE, rc=0 không lỗi/không chua_do. Bỏ tiền tố không làm hàng cũ xanh tình cờ vì lỗi khác:

| Hàng | j (từ 0) | Điều kiện thực sự được đo | rc head → khi đổi riêng điều kiện |
|---|---:|---|---|
| i | 1 | provider dòng trước | 1 → 0 khi bỏ provider |
| ii | 1 | citation dòng trước | 0 → 1 khi bỏ citation |
| ii-b (mới) | 0 | citation dòng sau | 0 → 1 khi bỏ citation |
| iii | 0 | không provider | 0 → 1 khi thêm provider cùng dòng |
| iv | 1 | notprovider không khớp cả từ | 0 → 1 khi đổi thành provider |
| v | 0 | provider dòng sau | 1 → 0 khi bỏ provider |
| vi | 2 | provider trước hai dòng ở ngoài cửa sổ | 0 → 1 khi kéo về cách một dòng |
| vii | 0 | provider sau hai dòng ở ngoài cửa sổ | 0 → 1 khi kéo về cách một dòng |
| viii | 2 | citation trước hai dòng không miễn | 1 → 0 khi kéo về cách một dòng |
| ix | 0 | citation sau hai dòng không miễn | 1 → 0 khi kéo về cách một dòng |

`run_mutants_l6.py` chạy lại nguyên **40 cặp đột biến** lượt 5. Tất cả đối chứng c18 sạch, băm nguồn ổn định; [bảng đầy đủ](evidence/review-summary.json):

| Nhóm | Số | Kết quả |
|---|---:|---|
| 24 cặp cận trái/phải khác cửa sổ đúng | 24 | c88 giet_that |
| Mọi dòng trước/sau/toàn tệp, loại dòng trắng, bỏ dòng khai ở EOF | 5 | c88 giet_that |
| Nới riêng provider hoặc citation ra trước/sau hai dòng | 4 | c88 giet_that |
| Bỏ provider cùng dòng, bỏ citation dòng trước | 2 | c88 giet_that |
| no_clamp, skip_first, citation_drop_next | 3 | c88 giet_that |
| citation_drop_self | 1 | SỐNG tại c88, **c79 giet_that**; không phải lỗ hổng của cả bộ ca |
| reverse_equivalent | 1 | SỐNG, oracle 71/71; tương đương vì đảo thứ tự không đổi hai phép any |

Tổng: **38 bị c88 giết + 1 bị c79 giết + 1 tương đương**. Tập hữu hạn này không được tuyên bố là vét cạn mọi biểu thức hay mọi nội dung verdict.

## Đột biến mới của reviewer

`python3 new_probe_l6.py <tên>` qua run_mutants_l6, mỗi tên một tiến trình; cả **14 phép** hoàn tất rc=0, đối chứng sạch, băm ổn định. Patch và dữ liệu: `evidence/new-*.patch/.json`, lệnh/rc: `newrun-*.json`.

| Phần thử | Số | Kết quả và lý do survivor |
|---|---:|---|
| Chỉ số âm cuộn về EOF; clamp ở 1; đòi đủ ba dòng; bỏ citation cuối vô điều kiện; chỉ citation dòng sau/cùng dòng; bỏ provider dòng sau; chỉ provider cùng dòng | 8 | Đều c88 giet_that; oracle chỉ 56–69/71 |
| Chặn cận phải bằng min(len, j+2); loại dòng trùng trong cửa sổ | 2 | **SỐNG, tương đương**; ba ca qua, oracle 71/71. Slice vốn tự chặn cận phải; loại bản sao không đổi any |
| Khôi phục tiền tố cũ; thêm một dòng trắng trước fixture | 2 | c88 riêng vẫn qua, nhưng **m156 KHÔNG RĂNG**, m157 vẫn giet_that |
| Bỏ hàng ii-b; đổi ii-b thành citation dòng trước | 2 | c88 riêng vẫn qua, nhưng **m157 KHÔNG RĂNG**, m156 vẫn giet_that |

Bốn phép cuối là đột biến vào test: sống qua ca thường nhưng bị bảng đột biến bắt. Không gán kết quả focused đó thành kết quả toàn suite.

## Giải xung đột và áp HINT

`python3 audit_l6.py` **rc=0**, `AUDIT ASSERTIONS PASS` ([JSON](evidence/merge-audit-l6.json)):

- Merge-base e9e0048/b29da0b là `757bde561d09738858506aecf5de2f050a5f0d5e`. `git merge-file -p` phát đúng **một** conflict; giữ cả hai thân + chuẩn hóa tên ca/đích m142/docstring c99 cho kết quả **khớp byte 3883b60**.
- Áp nguyên HINT bằng `patch -p1` lên blob test của 3883b60: rc=0. So head chỉ còn docstring/chú thích; AST thực thi giống nhau ([delta](evidence/hint-vs-head.patch)). Sản phẩm nguyên byte qua e9e0048/3883b60/head.
- Ca/đăng ký đột biến: e9e0048 **97/153**, b29da0b **95/139**, 3883b60 **98/153**, head **98/155**. Không mất hàm/đăng ký từ hai cha, không trùng tên/số ca, tên c98_chon_bien_nhan cũ không còn. 155 ở head gồm 153 thường và 2 tự kiểm, được suite xác nhận.

`python3 run_focused_l6.py` **rc=0**: m140–m157 chạy riêng **18/18**, mỗi log có đúng một hàng `giet_that` và `ASSERTIONS PASS`; m156/m157 đích c88, có đối chứng. Bốn lượt tiêm AttributeError vào ca đích m142/m147/m154/m155 đều **KHÔNG RĂNG**, `tin_dung_gia`, có tên ngoại lệ và vị trí ném (`focused_merge.py ... in reviewer_throw`). Dây báo lỗi #1037 còn hoạt động ([log driver](evidence/run-focused-l6.stdout)).

## Bảng tiêu chí

| Tiêu chí | Kết quả | Lệnh / output quyết định |
|---|---|---|
| Neo/phạm vi | ĐẠT | preflight.py; exact head/spec/tree, hai tệp, diff-check rc=0 |
| C1a | ĐẠT phần đã đo; Windows KHÔNG ĐO ĐƯỢC | probe.py head behaviors: hai YAML hợp lệ sai schema rc=1/tổng 2/nêu x; chỉ x rc=1/tổng 1/không báo rỗng; m142 so đuôi chính xác bị c101 giết thật |
| C1b | ĐẠT phần đã đo; Windows KHÔNG ĐO ĐƯỢC | Cùng driver: YAML hỏng đuôi hoa rc=2, stderr nêu x.RECEIPT.YAML, không Traceback; m142 chết c101 |
| C2 | ĐẠT phần đã đo; Windows KHÔNG ĐO ĐƯỢC | c89 qua trong suite; mutation_probe.py m143 thêm is_file → c89 giet_that, c18 sạch |
| C3 | ĐẠT | mutation_probe.py glob: c101/c99 giet_that, c18 sạch. c100 gian_giao vì không gọi iterdir, KHÔNG tính làm tín dụng |
| C4 Windows CI | KHÔNG ĐO ĐƯỢC | Không có đo độc lập jobs/labels/runner/log trên exact head |
| C5 Ubuntu CI | KHÔNG ĐO ĐƯỢC | Suite trong sandbox không chứng minh job CI exact head |
| C6 | ĐẠT | head/base chạy python3 ops/bien_nhan_v2.py --root .: rc=0, tổng 306, TỔNG: ĐẠT; os.listdir đếm riêng casefold=306/exact=306 |
| C7 Windows local | KHÔNG ĐO ĐƯỢC | Không chạy Windows local; không suy pass từ lời khai executor |
| C8 nội dung review | KHÔNG ĐẠT | Còn 1 P3 ở chú thích mới; request_changes neo exact head. Không xác nhận các điều kiện CI/land chưa đo; trần lượt 6 theo chỉ thị hiện hành |
| C9 | ĐẠT | Ruff F head/base cùng một F541 cùng nội dung dòng: **đỏ sẵn, delta=0**; doctrine rc=0, 10 tệp/0 chỗ; diff-check rc=0; rg glob rc=1/0 dòng; numstat 40/5 và 296/2 |
| Toàn suite head | ĐẠT | head-suite-final: rc=0, 372.70s, **98/98 · 153/153 · 2/2**, TỔNG: ĐẠT; stderr rỗng |
| C88/M4 | ĐẠT tập đã đo | 71/71 trực tiếp và git thật; 40 mutant phân loại đủ; no_clamp chết qua toàn suite |

Log C1: `evidence/head-behaviors.*`, `fixture-head-{c1a,only-x,c1b}.*`. C6/C9: `head-gate.*`, `base-gate.*`, `receipt-count.*`, `head-ruff.*`, `base-ruff.*`, `ruff-delta.json`, `head-doctrine.*`, `base-doctrine.*`, `no-glob.*`. Lệnh Ruff là `python3 -m ruff check --no-cache --select F --output-format json ops/bien_nhan_v2.py ops/bien_nhan_v2_test.py`; doctrine là `python3 .claude/dev/packet_loop.py doctrine-scan --root .`. Không gọi Ruff sạch tuyệt đối. C9 vế âm dùng `rg -n 'glob\("\*\.receipt\.yaml"\)' ops/bien_nhan_v2.py`; vế dương là C1a/C1b ở trên.

## Bảng finding

**Finding mở: 1. Tổng P0=0, P1=0, P2=0, P3=1.**

- [P3] chu-thich-nang-ca-thuong-thanh-toan-suite: `ops/bien_nhan_v2_test.py:4760` — `python3 historical_citation_suite.py` — suite con rc=1, 98/98 · 150/151 · 2/2, TỔNG: ĐỎ; m85 gian_giao do mẫu khớp 0 chỗ — sửa chú thích để tách no_clamp (từng sống qua toàn suite) với citation_drop_next (từng qua đủ 98 ca thường). Đây là lỗi mô tả bằng chứng mới được thêm ngoài HINT, không phải lỗi runtime hay mở lại P1.

  HÌNH DẠNG: `khac`.

  **Hướng vá cụ thể:** [HINT-LUOT6.patch](HINT-LUOT6.patch) thay đúng một dòng chú thích bằng: `# #1021 Codex lượt 5: no_clamp từng SỐNG qua toàn suite; citation_drop_next từng qua đủ 98 ca thường.` `python3 comment_hint_l6.py` rc=0: git apply --check và git diff --check đều rc=0; AST thực thi không đổi, bản sao đã phục hồi ([bằng chứng](evidence/comment-hint.json)). Patch chỉ được thử trong sandbox, chưa áp vào checkout được review.

  **Cách kiểm và rủi ro vá:** không thêm test runtime cho một chú thích; đối chiếu N/N/cờ gian_giao với log lịch sử và kiểm patch/AST như trên. Giữ nguyên các ca và m156/m157 đã xanh. Chỉ sửa chữ thì không đổi hành vi; tránh chạm mẫu neo, target hoặc đăng ký đột biến khi áp.

- [P1 — ĐÃ ĐÓNG] bien-ngoai-cua-so-surface-chua-co-rang: `ops/bien_nhan_v2_test.py:2981`, hàng ii-b tại `:2994`, bỏ prefix tại `:3005`, đăng ký tại `:4761`/`:4765` — `mutation_probe.py no_clamp --suite`, `skip_first`, `citation_drop_next` — c88 giet_that; no_clamp toàn suite rc=1/97 trên 98 ca, chỉ c88 đỏ — hướng vá lượt 5 đã được áp và kiểm: fixture chạm j=0, citation ngay sau, m156/m157 khóa hai chốt. Không yêu cầu vá thêm.

  HÌNH DẠNG: `bo-chon-ung-vien` (lớp lịch sử đã đóng).

F1/F2/F3 lịch sử có hình dạng `loi-do`, vẫn đóng theo bảng đối chiếu. P3 mới chỉ là câu mô tả sai phạm vi bằng chứng; không tạo finding runtime cho lỗi giàn giáo m85, mutant tương đương, ENOSPC hay phần nền không đo được.

## Toàn vẹn và giới hạn bằng chứng

`python3 summarize_l6.py` rc=0: `PASS: 40 windows (38 c88, 1 c79, 1 equivalent); 6 selector mutations; 18 focused real + 4 fake; F1/F2/F3; C1/C6/C9; 14 new probes`.

`python3 validate_l6_final.py` rc=0: `FINAL ASSERTIONS PASS: 4 clean full trees; exact head/spec/hint; all suite counts; no_clamp killed by c88; historical citation NOT a full-suite survivor` ([snapshot](evidence/final-validation.json)). `cay-kho`, `work/head`, `work/mutation`, `work/focus` về exact head/tree dòng đầu, tracked/untracked/ignored sạch, worktree/index diff rỗng; hai tệp nguồn khớp blob HEAD; .git là thư mục, không nông, core.abbrev=7. Snapshot cuối không được dùng để tuyên bố toàn bộ lịch sử ghi trong lúc chạy.

Script kế thừa được chép ra gốc sandbox để ROOT neo đúng. Chỉ `mutation_probe.py` được chỉnh để nhận `REVIEW_MUTATION_TREE`/`REVIEW_MUTATION_PREFIX`, giữ nguyên byte toàn bộ 40 định nghĩa đột biến và oracle; dùng `run_mutants_l6.py` thay driver sao chép cũ. `audit_l6.py` tái dựng merge tại 3883b60 rồi áp HINT trước khi so head. Không chạy `hint_probe.py create` vì hint đã áp. Các script nguyên bản trong luot5-probe không sửa. `work/focus` là clone local đủ cây, object git bất biến hardlink theo clone local; nguồn có bản riêng. Đã ghim origin/master và origin/HEAD về b29da0b cho bản clone này.

Sự cố hạ tầng được giữ riêng: lần sao work/focus đầu và audit scratch gặp ENOSPC; suite head đầu ra 97/98 do **c42 OSError ENOSPC**; suite no_clamp đầu bị cắt ngang/log dở. Các log `infra-initial-*` không được tính làm kết quả sản phẩm. Đã bỏ bản sao dở và bản base sau khi lưu C6/C9; suite head và no_clamp chạy lại đầy đủ, cho kết quả dùng ở trên. Bằng chứng tăng dần trước bản tổng hợp được giữ tại `evidence/VERDICT-progress.md`.

Windows CI/local, Ubuntu CI exact head: **KHÔNG ĐO ĐƯỢC**. Không cấp quyền merge/land.
<!-- VERDICT-L6-KET-THUC -->

### Lượt 7 — sha256 `181946a7e31be93140bf45fa35fb3e207d2c8f263bddca24ec504acca00d1a10`

<!-- VERDICT-L7-BAT-DAU -->
Verdict: request_changes
Reviewed commit: c8a493c0bb8afe0cfb8448e9220b661ed0f6aaa8
Spec sha256: d5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d

P3 lượt 6 **ĐÃ VÁ THẬT**. Còn **1 P3 mới phát hiện trong diff tổng thể**: docstring `_hoi_trang_thai` trỏ sai ca kiểm tra lỗi lập trình (`c99` thay vì `c100`). Do ngưỡng yêu cầu không còn bất kỳ P0/P1/P2/P3 nào, verdict là **request_changes**. Không phát hiện lỗi runtime mới trong các phép đo dưới đây.

Suite: **98/98 ca đạt · 153/153 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt, TỔNG: ĐẠT**. Sáu đột biến chỉ định đều chết đúng ca đích. C6/C9 đạt theo tiêu chí delta. Windows CI/local và Ubuntu CI trên exact head: **KHÔNG ĐO ĐƯỢC**. Verdict này không cấp quyền merge/land.

## Neo và cách tái hiện

Từ gốc sandbox: `PYTHONDONTWRITEBYTECODE=1 python3 measure_l7.py preflight`, `python3 measure_l7.py history`, `python3 measure_l7.py pipeline`. Driver ghi command, cwd, rc, thời gian và băm stdout/stderr trong `evidence/<tên>.json`; stdout/stderr được lưu riêng. Mọi tiến trình đo con dùng `PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1 PYTHONIOENCODING=utf-8 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null`. Các lệnh suite, cổng, Ruff, doctrine và rg chạy tại `cay-kho/`. Các probe dùng cơ chế `_dot_bien_tep` của suite; không sao chép toàn cây kho.

`python3 measure_l7.py preflight` rc=0 ([kết quả](evidence/preflight.json)): HEAD `c8a493c0bb8afe0cfb8448e9220b661ed0f6aaa8`, cha `691cb65388e71afb825aeba3b5cbc5359fc4dac5`, base `b29da0bfe3bfb7a7be69136a1c5c40f82c088a93`, tree `5ea6194cbf993b93521a01f269f2b446f4b1cf2a`. `.git` là thư mục, `git rev-parse --is-shallow-repository` → `false`; trạng thái tracked/untracked/ignored sạch, nguồn khớp blob HEAD. SPEC khớp băm dòng 3; HINT sha256 `fc52cb294ec8eba18038ffa00f95626e4de45b74d79360c79f7282ece7c3e202`. Hai tệp DIFF đầu vào khớp byte với git diff tương ứng.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| Finding/phạm vi trước | Phép đo, output | Kết luận |
|---|---|---|
| P3 `chu-thich-nang-ca-thuong-thanh-toan-suite`, lượt 6 / 691cb65 | `measure_l7.py preflight`: thay đúng một dòng theo HINT trong blob cha cho kết quả khớp byte HEAD. `measure_l7.py history`: kiểm log gốc lượt 5–6 bằng assertion, rc=0. | **ĐÃ VÁ THẬT** |
| P1 `bien-ngoai-cua-so-surface-chua-co-rang` / c88 | AST hai tệp giống hệt 691cb65. Suite sạch; `_dot_bien(chi={m156})` và `chi={m157}` đều `giet_that` tại c88, đối chứng c18 sạch. | Giữ kết luận **ĐÃ VÁ THẬT** của lượt 6; không mở lại P1. |
| F1/P2 `loi-do-liet-ke-thu-muc-thoat-traceback` | AST không đổi; m147 chết tại c99; m154 chết tại c100; suite sạch. | Vẫn đóng trong phạm vi đã đo. |
| F2/P3 `loi-do-thieu-chot-ngoai-le-lap-trinh` | AST không đổi; c100 và m152/m153 đạt trong suite. Probe bổ sung m153 bị c100 giết thật vì RuntimeError bị nuốt, c18 sạch. | Vẫn đóng về hành vi; finding mới bên dưới chỉ là tham chiếu docstring sai. |
| F3/P3, bắt OSError ngoài PermissionError | AST không đổi; m154/m155 chết đúng c100/c99 với errno=5. | Vẫn đóng. |
| Giải xung đột #1037 | `git diff 691cb65..HEAD` chỉ đổi một dòng chú thích; AST hai tệp giống hệt; c98 và toàn suite qua, m142 vẫn nhắm c101. | Giữ kết luận hành vi của lượt 6. Không chạy lại riêng toàn bộ thí nghiệm tiêm lỗi báo cáo của lượt 6. |

Lệnh đối chiếu AST: driver gọi `ast.dump(ast.parse(git show <rev>:<file>), include_attributes=False)` cho cả hai tệp ở HEAD và 691cb65, so chuỗi bằng nhau, lưu băm AST trong [preflight.json](evidence/preflight.json). `git diff --numstat 691cb65..HEAD` tương ứng 1 thêm/1 xóa chỉ trong chú thích trên m156. Chú thích hiện tại tại `ops/bien_nhan_v2_test.py:4760` là: “no_clamp từng SỐNG qua toàn suite; citation_drop_next từng qua đủ 98 ca thường.”

`python3 measure_l7.py history` rc=0 ([audit và provenance](evidence/history-audit.json)): log lượt 5 của no_clamp có rc=0, **98/98 · 151/151 · 2/2, TỔNG: ĐẠT**; hiện vật citation_drop_next ghi **98/98 ca thường**, không lỗi. Phép đo bổ sung lượt 6 trên 3883b60 có rc=1, **98/98 · 150/151 · 2/2, TỔNG: ĐỎ**, m85=`gian_giao` vì mẫu không khớp. Câu mới tách đúng hai phạm vi. Đây là đối chiếu lại hiện vật lịch sử, không gán chúng thành lần chạy mới trên HEAD.

Kết quả 71/71 M4, 40 mutant biên, no_clamp toàn suite đỏ, và phép đo F1/F2/F3 sâu của [lượt 6](VERDICT-LUOT6.md) được **kế thừa theo chỉ thị**, dựa trên AST bất biến; không khai đã chạy lại chúng ở lượt 7. Tập lớp mở lượt 6 có 1, đóng được 1; thêm 1 lớp P3 được phát hiện lượt này.

## Bảng tiêu chí

| Tiêu chí | Kết quả | Lệnh / output quyết định |
|---|---|---|
| Neo và write set | ĐẠT | `git diff --name-only b29da0b..HEAD` → đúng `ops/bien_nhan_v2.py`, `ops/bien_nhan_v2_test.py`; `preflight` rc=0. |
| C1a/C1b | ĐẠT phần đã đo; Windows KHÔNG ĐO ĐƯỢC | c101 qua trong suite và đối chứng sạch của `probe_l7.py glob`; m142 chết đúng c101 với tổng 1 thay vì 2. Ba nhánh ca giữ nguyên AST so lượt 6. |
| C2 | ĐẠT phần đã đo; Windows KHÔNG ĐO ĐƯỢC | `suite.stdout`: c89 ĐẠT, m143 lọc is_file bị c89 `giet_that` / CÓ RĂNG. |
| C3 | ĐẠT | `python3 probe_l7.py glob` rc=0: c101 sạch=`qua`, mutant glob=`giet_that`, tổng=1; c18 sạch; nguồn ổn định, temp dọn sạch ([log](evidence/glob-probe.stdout)). |
| C4 Windows CI | KHÔNG ĐO ĐƯỢC | Không có phép đo độc lập jobs/labels/runner/log trên exact head; không suy pass từ lời khai đang chạy. |
| C5 Ubuntu CI | KHÔNG ĐO ĐƯỢC | Lần chạy suite tại đây không chứng minh job CI exact head. |
| C6 | ĐẠT | `python3 ops/bien_nhan_v2.py --root .` rc=0, tổng 306, TỔNG: ĐẠT; đếm riêng os.listdir/name.lower().endswith = 306. |
| C7 Windows local | KHÔNG ĐO ĐƯỢC | Theo chỉ thị lượt 7; không sử dụng lời khai executor làm bằng chứng. |
| C8 nội dung review | KHÔNG ĐẠT | Còn 1 P3 mới; exact reviewed SHA đúng. Trần lượt 7 theo chỉ thị hiện hành. Không xác nhận điều kiện land/CI còn thiếu. |
| C9 | ĐẠT | Đúng hai tệp; hai diff-check rc=0; Ruff F head/base delta=0; doctrine rc=0; rg glob rc=1/0 dòng. |
| Toàn suite | ĐẠT | rc=0, 396.308 giây, 98/98 · 153/153 · 2/2, TỔNG: ĐẠT; stderr rỗng. |
| Sáu đột biến chạy riêng | ĐẠT | `python3 probe_l7.py focused` rc=0; 6/6 `giet_that` đúng ca đích, 6/6 đối chứng sạch; chi tiết dưới đây. |

Log suite: [stdout](evidence/suite.stdout), [command/rc](evidence/suite.json). Output cuối nguyên văn:

```text
bien_nhan_v2_test: 98/98 ca đạt · 153/153 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 135/153 đột biến thường khai đối chứng
TỔNG: ĐẠT
```

C6: [stdout](evidence/gate.stdout), [command/rc](evidence/gate.json), [đếm độc lập](evidence/receipt-count.json):

```text
bien_nhan_v2: 253 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 306
câu lịch sử: nợ L-REVIEW 1 · L-ANCESTRY 60 · L-SURFACE 0 · L-SURFACE chua_do_duoc 0
TỔNG: ĐẠT
```

Lệnh đếm độc lập tương đương: `python3 -c 'import os; print(sum(n.lower().endswith(".receipt.yaml") for n in os.listdir("ops/reviews")))'` → **306**. Không lọc is_file.

C9: `git diff --numstat b29da0b..HEAD` → **40/5** ở sản phẩm, **296/2** ở test. `git diff --check` và `git diff --check b29da0b..HEAD` → rc=0, stdout/stderr rỗng. `rg -n 'glob\("\*\.receipt\.yaml"\)' ops/bien_nhan_v2.py` → rc=1, 0 dòng.

Ruff `ruff 0.15.15`: `python3 -m ruff check --no-cache --select F --output-format json ops/bien_nhan_v2.py ops/bien_nhan_v2_test.py` → rc=1, **1 lỗi**; base cũng **1 lỗi**. Base lấy từng blob bằng `git show b29da0b:<path>` và lint stdin bằng cùng config, cùng `--select F --stdin-filename <path>`. Chuẩn hóa theo path/code/message/nội dung dòng: thêm 0, mất 0 ([delta](evidence/ruff-delta.json)). Đây là **delta đạt**, không phải Ruff sạch tuyệt đối.

Doctrine: `python3 .claude/dev/packet_loop.py doctrine-scan --root .` rc=0 ([log](evidence/doctrine.stdout)):

```text
doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine
```

## Sáu đột biến yêu cầu

`python3 probe_l7.py focused` gọi riêng `_dot_bien(chi={tên_đầy_đủ})` cho từng tên, kiểm đúng một hàng kết quả, `dat=true`, `tt=giet_that`, có đối chứng và không phải ca tự kiểm. Mọi đối chứng chạy khi mutant còn hiệu lực theo cơ chế suite. Băm nguồn trước/sau không đổi, module/CONG phục hồi và danh sách temp rỗng. [Output](evidence/focused.stdout), [bảng máy](evidence/focused-results.json).

| Đột biến | Ca đích | Kết quả | Assertion đầu tiên |
|---|---|---|---|
| `m142_chon_bien_nhan_so_duoi_CHINH_XAC` | `c101_chon_bien_nhan_KHONG_phan_biet_hoa_thuong_tren_moi_nen` | `giet_that`; CÓ RĂNG; c18 sạch | `C1a: đòi tổng 2 nêu x.RECEIPT.YAML, không ĐẠT; được rc=1 tổng=1: 'òi 2 · thiếu/r` |
| `m147_bo_chon_bo_bat_OSError` | `c99_bo_chon_bien_nhan_co_rang_o_SINH_NO_THU_TU_THU_MUC_VANG_va_LOI_LIET_KE` | `giet_that`; CÓ RĂNG; c18 sạch | `[]: CLI chết bằng PermissionError: [Errno 13] Permission denied (tiêm, #1021): '` |
| `m154_hoi_trang_thai_chi_bat_PermissionError` | `c100_LOI_TRANG_THAI_thu_muc_la_rc2_va_LOI_LAP_TRINH_di_thang` | `giet_that`; CÓ RĂNG; c18 sạch | `[]: CLI chết bằng OSError: [Errno 5] I/O error (tiêm, #1021) — đòi mã thoát, khô` |
| `m155_bo_chon_chi_bat_PermissionError` | `c99_bo_chon_bien_nhan_co_rang_o_SINH_NO_THU_TU_THU_MUC_VANG_va_LOI_LIET_KE` | `giet_that`; CÓ RĂNG; c18 sạch | `[]: CLI chết bằng OSError: [Errno 5] I/O error (tiêm, #1021): '/tmp/tmpxd6vy39i/` |
| `m156_B4_bo_chan_bien_dau_tep` | `c88_B4_LOI_TU_KHAI_surface_can_provider_va_khong_trich_dan` | `giet_that`; CÓ RĂNG; c18 sạch | `ix-trich-dan-sau-hai-dong: đòi rc=1, được 0: loi=[] chua=[]` |
| `m157_B4_trich_dan_bo_dong_sau` | `c88_B4_LOI_TU_KHAI_surface_can_provider_va_khong_trich_dan` | `giet_that`; CÓ RĂNG; c18 sạch | `ii-b-trich-dan-dong-sau: đòi rc=0, được 1: loi=["[L-SURFACE] r.receipt.yaml: ver` |

## Bảng finding

**Finding mở: 1. P0=0, P1=0, P2=0, P3=1.**

| Slug lớp | Mức | Vị trí | Trạng thái |
|---|---|---|---|
| `chu-thich-nang-ca-thuong-thanh-toan-suite` | P3 lịch sử | test:4760 | ĐÃ VÁ THẬT |
| `chu-thich-tro-sai-ca-ngoai-le-lap-trinh` | P3 | sản phẩm:90 | MỚI PHÁT HIỆN, còn mở |

- [P3] chu-thich-tro-sai-ca-ngoai-le-lap-trinh: `ops/bien_nhan_v2.py:90` — `PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null python3 probe_l7.py comment-probe` — wrapper rc=0; c99/c100 trên nguồn sạch đều `qua`; cùng mutant m153 nới `_hoi_trang_thai` từ bắt OSError sang Exception: **c99 vẫn qua**, **c100 giet_that**, chi tiết “lỗi lập trình ở is_dir [] bị nuốt/đổi: đòi RuntimeError mốc đi thẳng ra, được không ngoại lệ”; c18 sạch — đổi đúng tham chiếu `c99` thành `c100` trong docstring.

  HÌNH DẠNG: `khac`.

  Docstring hiện gán thuộc tính “lỗi lập trình phải đi thẳng ra” cho “c99 chốt 7”, nhưng c99 không canh thuộc tính này. Người bảo trì chạy ca được chỉ dẫn có thể nhận xanh dù đã nuốt lỗi lập trình; probe trên đã tái hiện đúng tình huống đó. Chốt 7 nằm trong `c100_LOI_TRANG_THAI_thu_muc_la_rc2_va_LOI_LAP_TRINH_di_thang` tại test:3830 và mutant m153 đăng ký ca này tại test:4820. Đây là lỗi tham chiếu bằng chứng trong diff #1021 tổng thể, đã tồn tại trước commit lượt 7; không phải hồi quy do sửa chú thích m156 và không phủ nhận F2 đã được vá về hành vi. [Kết quả chi tiết](evidence/comment-probe-results.json), [lệnh/rc](evidence/comment-probe.json), [đối chiếu lịch sử](evidence/comment-rename-history.json).

  Gợi ý vá chỉ thay chữ `c99` bằng `c100` ở vị trí nêu trên. Không sửa kho trong lượt review này. Bản probe dùng bản sao tạm đúng tệp nguồn qua `_dot_bien_tep`; đã kiểm băm nguồn không đổi và dọn bản tạm.

## Kiểm tra cuối và giới hạn

`PYTHONDONTWRITEBYTECODE=1 python3 finalize_l7.py` kiểm các rc, mẫu số, đích mutant, delta Ruff, head/spec và snapshot bằng assertion; output **FINAL ASSERTIONS PASS** ([kết quả](evidence/final-validation.json)). Snapshot đầu/cuối giống nhau về HEAD/tree, index, nội dung hai tệp nguồn, diff staged/unstaged và trạng thái tracked/untracked/ignored. Điều này chứng minh không có delta quan sát được ở hai mốc, không dùng để suy toàn bộ lịch sử ghi. Các bản tạm do probe tạo đều được dọn; chỉ giữ script và log bằng chứng trong sandbox. Bản cập nhật tăng dần trước tổng hợp được giữ tại [VERDICT-progress.md](evidence/VERDICT-progress.md).

Windows CI/local, Ubuntu CI exact head: **KHÔNG ĐO ĐƯỢC**. Không cấp quyền merge/land.
<!-- VERDICT-L7-KET-THUC -->

### Lượt 8 — sha256 `bd891b299d189b83973db7cde3f184b9a17bcc1d3dd5ff7a0e6ee08b068b6ece`

<!-- VERDICT-L8-BAT-DAU -->
Verdict: request_changes
Reviewed commit: 356a27e1378b2162bbc0be2ec06ff08fdacbdead
Spec sha256: d5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d

P3 lượt 7 **ĐÃ VÁ THẬT**; không phát hiện P0/P1/P2/P3 còn mở trong diff tổng. Tuy nhiên **chưa chấp nhận hồ sơ nghiệm thu**: C6 trả rc=2, suite Linux chỉ **95/98**, do snapshot thiếu một Git object lịch sử. Mã base trên cùng dữ liệu cũng thất bại như HEAD. Đây là trở ngại snapshot/bằng chứng, **không phải finding hồi quy trong hai tệp write set**, không có căn cứ yêu cầu sửa mã để làm xanh.

Đã đọc độc lập log CI Windows/Ubuntu: bien-nhan **98/98 · 153/153 · 2/2**, hai bước selftest yêu cầu đều success. Chưa đọc được `labels`/`runner_id` từ API thô; chưa xác nhận đầy đủ C4/C5. Windows local **KHÔNG ĐO ĐƯỢC**. Verdict không cấp quyền merge/land.

## Neo và cách tái hiện

Reviewer: OpenAI/Codex, họ GPT, độc lập với executor họ Claude; đo bằng shell và API GitHub trong phiên sandbox này. Không suy danh tính model từ tài khoản kết nối GitHub, không tự khai một model ID cụ thể ngoài thông tin phiên được cung cấp.

- HEAD: `356a27e1378b2162bbc0be2ec06ff08fdacbdead`; tree: `c1e160cfd5ddf1a053c2e8413e62f5881badd052`.
- Base review: `b29da0bfe3bfb7a7be69136a1c5c40f82c088a93`; lượt trước: `c8a493c0bb8afe0cfb8448e9220b661ed0f6aaa8`. `origin/master=b653574…` không dùng làm base.
- SPEC khớp băm dòng 3; `VERDICT-LUOT7.md` khớp SHA-256 `181946a7e31be93140bf45fa35fb3e207d2c8f263bddca24ec504acca00d1a10`.
- Clone báo `--is-shallow-repository=false`, checkout sạch. Không nông không bảo đảm chứa mọi commit ngoài lịch sử nhánh đã lấy; object thiếu được đo bên dưới.
- Hai patch lượt 8/tổng khớp byte với git diff. Write set đúng hai tệp. Numstat tổng: sản phẩm **40 thêm/5 xóa**, test **300 thêm/2 xóa**.
- Linux x86_64; Python **3.13.18**, Git **2.43.0**, Ruff **0.16.9**.

[Preflight](evidence/preflight/stdout.txt), [lệnh/rc](evidence/preflight/run.json), [môi trường và lịch sử](evidence/additional-checks/stdout.txt). Hai commit lượt này đúng `69649309848e1e23cf22b236f8528f5e6b31670a` và HEAD.

Từ gốc sandbox, dùng [measure.py](measure.py), mỗi nhãn phải mới:

```sh
export PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1 PYTHONIOENCODING=utf-8
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
python3 measure.py suite-replay cay-kho python3 ops/bien_nhan_v2_test.py
python3 measure.py gate-replay cay-kho python3 ops/bien_nhan_v2.py --root .
python3 measure.py focused-replay . python3 probe.py focused
python3 measure.py c1-replay . python3 probe.py c1
python3 measure.py comments-replay . python3 probe.py comments
python3 measure.py listing-replay . python3 probe.py listing
python3 measure.py ruff-replay . python3 ruff_delta.py
```

Driver lưu command/cwd/rc/thời gian trong `evidence/<nhãn>/run.json`, stdout/stderr riêng. Mọi tiến trình đo do driver khởi chạy nhận đủ năm biến bắt buộc, thêm `GIT_OPTIONAL_LOCKS=0` và `TMPDIR=<sandbox>/tmp` để không làm mới index hoặc ghi fixture ngoài sandbox. Probe dùng `_dot_bien_tep` tạo bản sao, kiểm băm hai nguồn, phục hồi module/CONG và dọn temp. API được lưu nguyên kết quả cùng tên tool/đối số/thời gian trong `evidence/ci-*.json`.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| Lớp/phạm vi | Bằng chứng lượt 8 | Kết luận |
|---|---|---|
| P3 `chu-thich-tro-sai-ca-ngoai-le-lap-trinh`, sản phẩm:90 | Sạch c99/c100 đều qua; m153: c99 vẫn qua, **c100 giet_that**, lỗi “RuntimeError mốc … được không ngoại lệ”; c18 sạch. Docstring hiện trỏ c100 chốt 7. | **ĐÃ VÁ THẬT** |
| F1 `loi-do-liet-ke-thu-muc-thoat-traceback` | m147→c99; m148–m151/m154→c100 chết đúng ca. Probe CLI liệt kê HEAD rc2, không traceback, cả hai đường. | Vẫn đóng |
| F2 `loi-do-thieu-chot-ngoai-le-lap-trinh` | m152/m153 bị c100 giết vì nuốt RuntimeError; c18 sạch dưới mutant. | Vẫn đóng |
| F3, OSError ngoài PermissionError | m154→c100, m155→c99 chết vì **OSError errno=5**, không lấy tín dụng từ EACCES. | Vẫn đóng |
| P1 `bien-ngoai-cua-so-surface-chua-co-rang` / c88 | c88 sạch; m156 chết tại ix-trich-dan-sau-hai-dong; m157 tại ii-b-trich-dan-dong-sau; c18 sạch. | Vẫn đóng |
| P3 chú thích m156/m157 / `chu-thich-nang-ca-thuong-thanh-toan-suite` | Test:4764 vẫn tách “no_clamp … toàn suite” và “citation_drop_next … 98 ca thường”; không đổi so lượt 7. Kế thừa đối chiếu hiện vật lịch sử trong verdict lượt 7 đã kiểm băm. | Vẫn đóng |
| Giải xung đột #1037 | AST thực thi không đổi; c98 ĐẠT trong suite mới; m142 nhắm c101, không trùng c98. | Vẫn đóng |

[audit.py](audit.py) bỏ **riêng docstring** đầu module/hàm/lớp rồi so `ast.dump(..., include_attributes=False)` với c8a493c: AST thực thi hai tệp bằng nhau. AST nguyên có docstring khác; không khai chúng bằng nhau. Băm AST chuẩn hóa đầy đủ trong preflight: sản phẩm `8d2f6e76…`, test `adab78b4…`.

Theo quyền kế thừa trong prompt, giữ các phép đo sâu đã được verdict lượt 7 kế thừa: **71/71 M4, 40 mutant biên, no_clamp toàn suite đỏ, ma trận F1/F2/F3 sâu và thí nghiệm báo cáo #1037**. Không chạy lại những tập ấy. Không dùng suite 98/98 hoặc C6 xanh lượt trước thay cho kết quả Linux hiện tại.

## Diff lượt 8 và rà diff tổng

Diff lượt 8 chỉ đổi **bốn docstring**, mã thực thi không đổi. Đã đọc toàn diff `b29da0b..HEAD`, gồm các khối executor không sửa ở lượt 8, và đối chiếu ca/đột biến hiện hành.

| Vị trí | Nội dung kiểm | Phép đo |
|---|---|---|
| `ops/bien_nhan_v2.py:90` | c100 chốt 7 canh lỗi lập trình | c99/c100 sạch và cùng mutant m153 như trên |
| `ops/bien_nhan_v2.py:106` | glob cũ nuốt lỗi; kiem “không có tệp”, sinh-no #0; iterdir không bắt lỗi thoát traceback; HEAD rc2 | Source base thật trên bản sao, mutant bỏ bắt và HEAD; tiêm EACCES vào backend scandir; gọi main và subprocess CLI |
| `ops/bien_nhan_v2_test.py:3674` | Bốn chốt c99 tương ứng m144–m147; EIO bổ sung m155 chốt 4 | Chạy riêng cả năm mutant; chết đúng chốt và đối chứng sạch |
| `ops/bien_nhan_v2_test.py:3761` | Ba chốt 5–7, m148–m153 và m154; EACCES/EIO | c100 sạch; từng mutant chết đúng lỗi trạng thái hoặc lỗi lập trình |
| `ops/bien_nhan_v2_test.py:3631`, `:2987` | Ba fixture c101; m142 phân biệt được cả ba; c88 chạm biên và trích dẫn dòng sau | Đo 3×3 fixture sạch/exact/glob; m156/m157 chết đúng hàng |

[Đối chiếu c99/c100](evidence/comment-target-results.json), [liệt kê/CLI](evidence/listing-results.json), [ba fixture](evidence/c1-results.json), [đột biến](evidence/focused-results.json).

Lần tiêm liệt kê đầu không trúng binding scandir riêng của glob Python 3.13 và dừng bằng assertion giàn giáo. Giữ log ở `evidence/listing/`; sửa script reviewer rồi đo lại có hit counter. Lần cuối: glob base kiem rc2/“không có tệp”, sinh-no rc0/#0; mutant bỏ bắt rc1/PermissionError/Traceback trong cả hai subprocess; HEAD rc2/“không liệt kê được” cả hai. Không tính lỗi giàn giáo là lỗi sản phẩm.

Tham chiếu cùng chiều `_liet_ke_theo_duoi` của t27 cũng đã đối chiếu trực tiếp: helper trong lease_publish_test dùng `name.lower().endswith`; khác biệt is_file là chủ ý được SPEC nêu.

## Bảng tiêu chí

| Tiêu chí | Kết quả | Bằng chứng quyết định |
|---|---|---|
| C1a | **ĐẠT Linux** | Hai YAML hợp lệ sai schema: rc1, tổng2, nêu x; chỉ-x: rc1/tổng1, không “không có tệp”. |
| C1b | **ĐẠT Linux** | YAML x hỏng: rc2, stderr nêu x.RECEIPT.YAML, không Traceback; không đòi tổng. |
| C2 | **ĐẠT Linux** | c89 qua; m143 thêm is_file bị đúng c89 giết, đối chứng sạch. |
| C3 | **ĐẠT** | Glob trên bản sao bị c101 giet_that: tổng1 thay vì2; c18 sạch. Không thêm glob vào bảng mutant thường. |
| C4 Windows CI | **Đo được log/steps/SHA; metadata bắt buộc KHÔNG ĐO ĐƯỢC** | Run41113949578, job124263645262, Windows OS, checkout đúng HEAD; bien-nhan98/98·153/153·2/2, lease255/255; hai step success. Chưa xác minh labels/runner_id/dispatch input. |
| C5 Ubuntu CI | **Đo được log/steps và run gắn HEAD; labels KHÔNG ĐO ĐƯỢC** | Run41113943723, job124264022785, Ubuntu OS; bien-nhan98/98·153/153·2/2, lease268/268; checkout merge thử00c58bc…, không phải checkout trực tiếp HEAD. |
| C6 | **CHƯA ĐẠT snapshot bàn giao** | Cổng rc2, tổng306, 3 KHÔNG ĐO ĐƯỢC; đếm riêng306. Thiếu object lịch sử; source base tái hiện giống hệt. |
| C7 Windows local | **KHÔNG ĐO ĐƯỢC** | Không chạy test Windows từ xa, theo chỉ thị. |
| C8 | **CHƯA ĐỦ NGHIỆM THU** | P0–P3 mã nguồn mở=0, nhưng C6/suite Linux chưa đạt. Áp chỉ thị lượt8/9 hiện hành; không suy quyền land. |
| C9 | **ĐẠT theo delta** | Ruff thêm0/mất0; doctrine sạch10 tệp; diff-check working tree/tổng rc0; rg glob0 dòng, đối chứng bản sao1 dòng. |
| Toàn suite Linux | **KHÔNG ĐẠT** | rc1, **95/98 · 153/153 · 2/2**, TỔNG: ĐỎ; 248.642 giây, stderr rỗng. |
| Đột biến riêng | **ĐẠT** | **16/16** m142–m157 giet_that đúng ca, 16/16 đối chứng nghiêm sạch khi mutant còn hiệu lực. |

Ruff dùng executable có sẵn **0.16.9**; Python mặc định không có module cho `python3 -m ruff`. Không lấy version 0.15.15 lượt trước làm version lần này. [ruff_delta.py](ruff_delta.py) lint blob base/head qua stdin, cùng cwd/config/cờ `--no-cache --select F`, chuẩn hóa path/code/message/nội dung dòng để không đếm dịch dòng là lỗi mới. Hai phía cùng một **F541**, head tại test:1681: `dung(lam, f"KHÔNG ĐO ĐƯỢC: không có bề mặt nào của provider KHÁC để mượn thử")`. **Delta0, không phải Ruff sạch tuyệt đối.** [Delta](evidence/ruff-delta-results.json), [head trực tiếp](evidence/ruff-head/stdout.txt).

Doctrine: `python3 .claude/dev/packet_loop.py doctrine-scan --root .` → `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine` ([log](evidence/doctrine/stdout.txt)). Hai diff-check rc0. Grep glob trên source rc1/0 dòng; bản sao hoàn nguyên trả đúng1 dòng/rc0 ([đối chứng](evidence/additional-checks/stdout.txt)).

## Đột biến riêng và đối chứng

`probe.py focused` gọi riêng `_dot_bien(chi={tên_đầy_đủ})` 16 lần. Trước mỗi lần, ca đích sạch phải qua. Instrumentation ghi đầy đủ lỗi, xác nhận `_sach_hoan_toan(c18)` chạy **khi module mutant còn hiệu lực**, không có loi/chua_do. Không tính gian_giao, tín dụng giả hay ca tự kiểm thành giet_that.

| Mutant | Ca đích | Chốt làm đỏ |
|---|---|---|
| m142 | c101 | C1a tổng1 thay vì2 |
| m143 | c89 | Thư mục receipt bị lọc, mất đường lỗi băm |
| m144 | c99 | sinh-no mất x.RECEIPT.YAML |
| m145 | c99 | Trả z,m,a thay vì a,m,z |
| m146 | c99 | Thư mục vắng: sinh-no rc2 thay vì rc0/#0 |
| m147 | c99 | PermissionError errno13 thoát biên |
| m148 | c100 | is_dir trần đường sinh-no, PermissionError |
| m149 | c100 | guard kiem trần, PermissionError |
| m150 | c100 | Bỏ bắt trạng thái, PermissionError |
| m151 | c100 | exists của .git trần, PermissionError |
| m152 | c100 | RuntimeError ở iterdir bị nuốt |
| m153 | c100 | RuntimeError ở is_dir bị nuốt |
| m154 | c100 | **OSError errno5** ở trạng thái thoát biên |
| m155 | c99 | **OSError errno5** khi liệt kê thoát biên |
| m156 | c88 | ix-trich-dan-sau-hai-dong: đòi rc1, được0 |
| m157 | c88 | ii-b-trich-dan-dong-sau: đòi rc0, được1 |

Tất cả dat=true, tt=giet_that, không tự kiểm, có đối chứng. [Chi tiết](evidence/focused-results.json), [lệnh/thời gian](evidence/focused/run.json). Ba fixture C1 được đo riêng dưới mutant, không suy cả ba từ assertion đầu tiên của c101.

## Bảng finding và trở ngại nghiệm thu

**Finding mã nguồn mở: P0=0, P1=0, P2=0, P3=0.** Không có finding mới hình dạng `bo-chon-ung-vien`; không kích hoạt chốt dừng SPEC. P3 lượt7 đóng; các lớp cũ vẫn đóng trong phạm vi chứng minh ở trên.

| Loại | Slug | Vị trí | Trạng thái |
|---|---|---|---|
| P3 lịch sử | chu-thich-tro-sai-ca-ngoai-le-lap-trinh | ops/bien_nhan_v2.py:90 | ĐÃ VÁ THẬT |
| Trở ngại snapshot, không chấm P cho mã | snapshot-thieu-object-lich-su | ops/reviews/lease-publish-windows-do-review-r1-codex.receipt.yaml:47 tham chiếu object thiếu | Chặn C6 và suite Linux |

HÌNH DẠNG của trở ngại snapshot: `loi-do` (thiếu dữ liệu để đo; **không phải** `bo-chon-ung-vien`). Không đề xuất sửa receipt hay nới cổng.

Lệnh tái hiện tại cay-kho:

```text
git cat-file -t 4bc94325e647
fatal: Not a valid object name 4bc94325e647

python3 ops/bien_nhan_v2.py --root .
bien_nhan_v2: 253 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 3 KHÔNG ĐO ĐƯỢC · tổng 306
TỔNG: KHÔNG ĐO ĐƯỢC
```

Object đầy đủ: `4bc94325e647ee5e32373f3af30b8f83b98a90fa`. Ba thông báo chỉ vào reviewed_sha, reviewed_sha_to_tien và verdict_usage_caveats[1].mo_ta của cùng receipt. [Gate stdout](evidence/gate/stdout.txt), [stderr](evidence/gate/stderr.txt), [rc/thời gian](evidence/gate/run.json).

Output cuối suite nguyên văn:

```text
bien_nhan_v2_test: 95/98 ca đạt · 153/153 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 135/153 đột biến thường khai đối chứng
TỔNG: ĐỎ
```

Ba ca đỏ: c40 thiếu marker TỔNG: ĐẠT ở đối chứng; c14 đòi rc0, nhận2; c76 đòi rc1 không chua_do, nhận2 với ba lỗi trên. [Toàn log](evidence/suite/stdout.txt), [lệnh/cwd/rc/thời gian](evidence/suite/run.json). Giữ nguyên mẫu số98.

Đối chiếu nguyên nhân: `probe.py baseline_gate` dùng **source blob b29da0b** qua bản sao, cùng dữ liệu/Git cay-kho; rc2 và stdout/stderr **khớp byte** HEAD. `probe.py baseline_failures` xác nhận AST c40/c14/c76 giống base rồi chạy ba ca với source base: cùng đỏ, cùng object thiếu. Không khai chạy toàn suite base. [Gate base](evidence/baseline-gate-results.json), [ba ca base](evidence/baseline-failure-results.json).

GitHub độc lập xác nhận [commit lịch sử tồn tại](https://github.com/ducthangho/tra-luat/commit/4bc94325e647ee5e32373f3af30b8f83b98a90fa); [kết quả API](evidence/missing-commit.json). Không coi object là bịa. Hướng khắc phục: bên chuẩn bị bundle bổ sung object thật cùng closure cần thiết vào **bản sao review mới**, kiểm cat-file/ancestry rồi chạy lại C6 và toàn suite trên đúng HEAD này, giữ nguyên98 ca. Không cần đổi hai tệp write set; không thay receipt/hash/nợ, không dựng object giả hoặc giả kết quả Git. Rủi ro chuẩn bị lại là trôi HEAD/ref; cần kiểm lại SHA/hash nguồn/SPEC.

## CI độc lập

Đã gọi github_fetch_workflow_run_jobs và github_fetch_workflow_job_logs cho từng run. github_fetch_commit_workflow_runs với đúng HEAD trả run Ubuntu41113943723. [Tóm tắt máy](evidence/ci-summary.json).

- [Windows run41113949578 / job124263645262](https://github.com/ducthangho/tra-luat/actions/runs/41113949578/job/124263645262): gate-ops (windows-latest), completed/success; log OS Windows Server2025, git log -1 đúng HEAD. Bien-nhan98/98·153/153·2/2/TỔNG: ĐẠT. Lease-publish **255/255; đã chạy=255, bỏ qua=13**; không đổi thành268/268 hoặc nói không có bỏ qua. Hai **bước** đều success, không skipped. [Jobs](evidence/ci-41113949578.json), [log](evidence/ci-log-41113949578.txt).
- [Ubuntu run41113943723 / job124264022785](https://github.com/ducthangho/tra-luat/actions/runs/41113943723/job/124264022785): gate-ops (ubuntu-latest), completed/success; OS Ubuntu24.04.5. Checkout **00c58bc70286f622914f07e36d72691d192b3949**, merge thử HEAD vào 6db934145acf6e47d01db5b2dc8c9da417c2d8eb. Bien-nhan98/98·153/153·2/2/TỔNG: ĐẠT; lease-publish268/268, bỏ qua0; hai bước success. [Jobs](evidence/ci-41113943723.json), [log](evidence/ci-log-41113943723.txt), [run gắn HEAD](evidence/commit-runs.json).

Plugin chuẩn hóa bỏ labels/runner_id. Thử `gh api repos/ducthangho/tra-luat/actions/runs/<id>/jobs` cho cả hai đều rc1: `proxyconnect tcp … socket: operation not permitted` ([Windows](evidence/ci-raw-windows/stderr.txt), [Ubuntu](evidence/ci-raw-ubuntu/stderr.txt)). Không suy labels từ tên job/OS; runner_id1000026867 executor khai vẫn **KHÔNG ĐO ĐƯỢC**. Dispatch/input Windows chưa xác minh độc lập. Không gọi workflow hoặc chạy test Windows từ xa.

## Kiểm tra cuối và giới hạn

[finalize.py](finalize.py) kiểm rc thật, mẫu số, đúng ba ca đỏ, đối chứng mutant, delta Ruff và snapshot bằng assertion. [Kết quả](evidence/final-validation.json): **FINAL EVIDENCE ASSERTIONS PASS** xác nhận báo cáo khớp bằng chứng, không biến suite/C6 đỏ thành xanh.

Snapshot [đầu](evidence/snapshot-before.json) / [cuối](evidence/snapshot-after.json) **giống nhau**: HEAD/tree, index, nội dung **8.468 tệp tracked**, diff staged/unstaged, trạng thái tracked/untracked/ignored. Băm hai nguồn:

| Tệp | SHA-256 đầu = cuối |
|---|---|
| ops/bien_nhan_v2.py | 7f9a86f3fc07429877f2959ad2ecbe238ef145d08860b8f78197340a06e276a6 |
| ops/bien_nhan_v2_test.py | cac81d460abd280c461cf0acf938e412fc4b1c4cb477f36b55d2c5b1b0474b87 |

Không sửa checkout, không commit/push/fetch vào checkout, không ghi ngoài sandbox. Temp fixture đã dọn. Verdict tăng dần giữ ở [VERDICT-progress.md](evidence/VERDICT-progress.md). C7 và metadata CI nêu trên **KHÔNG ĐO ĐƯỢC**; C6/suite Linux **đã đo và chưa đạt trên snapshot này**. Cần khắc phục snapshot và bổ sung bằng chứng; không có HINT sửa mã vì không phát hiện lỗi mã mới.
<!-- VERDICT-L8-KET-THUC -->

### Lượt 9 — sha256 `8af135fcf798d7c07d85387c2cdbaed703cbb735ac101848023b377be1410252`

<!-- VERDICT-L9-BAT-DAU -->
Verdict: approve
Reviewed commit: 356a27e1378b2162bbc0be2ec06ff08fdacbdead
Spec sha256: d5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d

**P0=0, P1=0, P2=0, P3=0 mở.** Trở ngại `snapshot-thieu-object-lich-su` của lượt 8 đã được khắc phục trong bản sao review mới, không thay đổi cây mã được review. Tôi tự đo C6 **rc=0, 0 KHÔNG ĐO ĐƯỢC, tổng 306, TỔNG: ĐẠT** và toàn suite Linux **98/98 · 153/153 · 2/2, TỔNG: ĐẠT**. c14/c40/c76 đều ĐẠT; giữ nguyên mẫu số 98. Không dùng lời khai executor thay cho các phép đo này.

C4 còn giới hạn đọc trực tiếp input dispatch gốc; C7 Windows local KHÔNG ĐO ĐƯỢC. Theo chỉ thị lượt 9, các giới hạn này tự chúng không phải finding mã và không chặn verdict khi C6/suite Linux đạt, không còn P0–P3 mở. **Verdict không cấp quyền merge/land.** Đây là lượt 9/9 theo chỉ thị hiện hành; không khởi tạo lượt review tiếp theo.

## Neo và cách tái hiện

Reviewer: OpenAI/Codex, họ `openai`, phiên độc lập với executor họ Claude. Bề mặt thực tế quan sát được: agent gọi shell trong sandbox Linux và công cụ GitHub qua API, transport máy. Không suy model ID/effort đã phục vụ từ tài khoản GitHub hoặc tự nhận có attestation launcher; không đăng verdict/receipt lên GitHub trong lượt này.

| Neo | Kết quả độc lập |
|---|---|
| HEAD | `356a27e1378b2162bbc0be2ec06ff08fdacbdead`, detached |
| Tree | `c1e160cfd5ddf1a053c2e8413e62f5881badd052`, giống lượt 8 |
| Base diff tổng | `b29da0bfe3bfb7a7be69136a1c5c40f82c088a93`, là tổ tiên HEAD |
| SPEC | SHA-256 khớp dòng 3 |
| VERDICT-LUOT8.md | SHA-256 `bd891b299d189b83973db7cde3f184b9a17bcc1d3dd5ff7a0e6ee08b068b6ece` |
| Checkout | Không nông; tracked/untracked/ignored sạch; `core.abbrev=7` |
| Write set | Chỉ `ops/bien_nhan_v2.py` và `ops/bien_nhan_v2_test.py` |
| Numstat tổng | Sản phẩm +40/−5; test +300/−2 |
| Môi trường | Linux x86_64; Python 3.13.18; Git 2.43.0; Ruff 0.16.9 |

[Preflight và các lệnh Git](evidence/14-initial.stdout.txt), [command/cwd/rc/thời gian](evidence/14-initial.json), [tóm tắt neo](evidence/initial-summary.json). Hai patch đầu vào khớp byte với git diff. So với snapshot cuối lượt 8, HEAD/tree, **toàn bộ nội dung 8.468 tệp tracked**, trạng thái và diff staged/unstaged đều bằng nhau; không đòi index của hai clone khác nhau phải có cùng byte.

| Tệp | SHA-256 lượt 8 = đầu lượt 9 = cuối lượt 9 |
|---|---|
| `ops/bien_nhan_v2.py` | `7f9a86f3fc07429877f2959ad2ecbe238ef145d08860b8f78197340a06e276a6` |
| `ops/bien_nhan_v2_test.py` | `cac81d460abd280c461cf0acf938e412fc4b1c4cb477f36b55d2c5b1b0474b87` |

`git cat-file -t 4bc94325e647ee5e32373f3af30b8f83b98a90fa` trả **commit**, rc=0. `for-each-ref --contains` trả đúng hai ref, cả hai trỏ chính commit này:

- `refs/tags/luu-tru/lease-publish-windows-do-r1-verdict`.
- `refs/remotes/origin/ops/do-lease-publish-windows-150`.

`merge-base --is-ancestor` của object với mỗi ref trả 0. Với HEAD trả 1: object được giữ qua ref lưu trữ, **không là tổ tiên HEAD**. Điều này phù hợp nội dung receipt lịch sử; không biến commit thử CI thành commit đã land. [Receipt đã đọc](evidence/37-ancestry-context.stdout.txt). Không sửa receipt, tag hoặc ref.

Từ gốc sandbox, tái hiện bằng [review_run.py](review_run.py) với nhãn mới:

```sh
export PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1 PYTHONIOENCODING=utf-8
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null GIT_OPTIONAL_LOCKS=0
export TMPDIR="$PWD/evidence/tmp"
python3 review_run.py replay-c6 cay-kho python3 ops/bien_nhan_v2.py --root .
python3 review_run.py replay-suite cay-kho python3 ops/bien_nhan_v2_test.py
python3 review_run.py replay-count cay-kho python3 -c 'import os; print(sum(n.lower().endswith(".receipt.yaml") for n in os.listdir("ops/reviews")))'
python3 review_run.py replay-focused . python3 probe.py focused
python3 review_run.py replay-c1 . python3 probe.py c1
python3 review_run.py replay-comments . python3 probe.py comments
python3 review_run.py replay-ruff . python3 ruff_delta.py
```

Driver lưu command/cwd/rc/thời gian/môi trường trong `evidence/<nhãn>.json`, stdout/stderr trong hai tệp tương ứng. Các script `audit.py`, `probe.py`, `ruff_delta.py` được chép nguyên byte từ bằng chứng lượt 8 về gốc để `ROOT` trỏ đúng sandbox; [băm bản chép](evidence/13-prepare.stdout.txt). Đột biến dùng `_dot_bien_tep`, chỉ sửa bản sao trong TMPDIR, phục hồi module/CONG và dọn fixture. API GitHub lưu đầy đủ tên công cụ/đối số hoặc URL/thời gian/kết quả; trạng thái tool không được giả thành rc của tiến trình shell.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| Lớp/phạm vi | Đo lại hoặc kế thừa có căn cứ | Kết luận |
|---|---|---|
| `snapshot-thieu-object-lich-su` | Object thật có mặt, ref/ancestry như trên; C6 rc=0/tổng 306/0 KHÔNG ĐO ĐƯỢC; suite 98/98, riêng c14/c40/c76 ĐẠT. | **ĐÃ KHẮC PHỤC THẬT** trở ngại snapshot; không phải sửa mã. |
| P3 lượt 7 `chu-thich-tro-sai-ca-ngoai-le-lap-trinh` | Đo mới sạch c99/c100 đều qua; m153 làm c100 `giet_that` vì nuốt RuntimeError, c99 vẫn qua; c18 sạch. Docstring sản phẩm:90 trỏ c100 chốt 7. | **ĐÃ VÁ THẬT**, vẫn đóng. |
| F1 `loi-do-liet-ke-thu-muc-thoat-traceback` | Đo riêng m147→c99; m148–m151/m154→c100, đúng `giet_that` và đối chứng sạch. Kế thừa probe CLI liệt kê hai đường của lượt 8 vì toàn tree bằng nhau. | Vẫn đóng. |
| F2 `loi-do-thieu-chot-ngoai-le-lap-trinh` | m152/m153 bị c100 giết vì nuốt RuntimeError; đối chứng nghiêm sạch khi mutant còn hiệu lực. | Vẫn đóng. |
| F3: OSError ngoài PermissionError | m154→c100 và m155→c99 chết đúng **OSError errno=5**; không lấy tín dụng từ EACCES. | Vẫn đóng. |
| P1 `bien-ngoai-cua-so-surface-chua-co-rang` / c88 | c88 sạch; m156 chết tại `ix-trich-dan-sau-hai-dong`; m157 chết tại `ii-b-trich-dan-dong-sau`; c18 sạch. | Vẫn đóng. |
| P3 `chu-thich-nang-ca-thuong-thanh-toan-suite` / m156–m157 | Kế thừa đối chiếu hiện vật lịch sử lượt 7→8; chú thích test:4764 giữ nguyên: no_clamp qua toàn suite, citation_drop_next qua 98 ca thường. | Vẫn đóng; không khai đo lại hiện vật lịch sử. |
| Giải xung đột #1037 | c98 ĐẠT trong suite mới; m142 vẫn nhắm c101. Kế thừa phép tiêm lỗi báo cáo của lượt 8 và các lượt trước. | Vẫn đóng. |

[16 đột biến riêng](evidence/focused-results.json), [đối chiếu c99/c100](evidence/comment-target-results.json), [log suite](evidence/16-suite.stdout.txt), [verdict lượt 8](VERDICT-LUOT8.md), [verdict lượt 7](VERDICT-LUOT7.md).

Phần kế thừa rõ ràng: **71/71 M4, 40 mutant biên, no_clamp toàn suite đỏ, ma trận F1/F2/F3 sâu, probe CLI liệt kê và thí nghiệm báo cáo #1037** đã được lượt 8 chấp nhận. Không chạy lại các tập sâu ấy; cơ sở kế thừa là cùng HEAD/tree và byte mọi tệp tracked, theo quyền trong prompt. Không kế thừa kết quả C6/suite thay cho lần đo mới. Audit còn xác nhận AST thực thi hai nguồn so c8a493c không đổi khi bỏ riêng docstring; không khai AST có docstring bằng nhau.

## Rà diff tổng

Đã đọc toàn [diff b29da0b..HEAD](evidence/19-diff-review.stdout.txt). Helper dùng `iterdir()` + `name.lower().endswith`, không lọc `is_file`, trả `sorted`; cả `kiem` và `_sinh_no` dùng helper. `OSError` được chuyển thành `KhongDoDuoc`, lỗi lập trình đi thẳng. Các ca và đột biến kiểm hai đường gọi, thứ tự, thư mục vắng, EACCES/EIO và RuntimeError. Phần c88/m156/m157 được đo riêng; các thay đổi chú thích khớp ca đích. Không phát hiện P0–P3 mới trong phạm vi diff tổng.

## Bảng tiêu chí

| Tiêu chí | Kết quả | Bằng chứng quyết định |
|---|---|---|
| C1a | **ĐẠT Linux; Windows CI có bằng chứng ca đạt** | Đo mới: hai YAML sai schema rc=1/tổng 2/nêu x; chỉ-x rc=1/tổng 1, không “không có tệp”. c101 ĐẠT trong log Windows. |
| C1b | **ĐẠT Linux; Windows CI có bằng chứng ca đạt** | YAML x hỏng rc=2, stderr nêu x.RECEIPT.YAML, không traceback; không đòi tổng. m142/exact làm cả ba fixture mất tiêu chí. |
| C2 | **ĐẠT Linux; Windows CI có bằng chứng ca đạt** | c89 ĐẠT, m143 lọc is_file bị đúng c89 giết; đối chứng sạch. Log Windows cũng có c89 ĐẠT. |
| C3 | **ĐẠT Linux** | Bản sao hoàn nguyên glob bị c101 `giet_that`: tổng 1 thay 2; c18 sạch. Không thêm glob vào bảng mutant thường. |
| C4 Windows CI | **Đã xác minh SHA/event/workflow/labels/runner/steps/log; input gốc KHÔNG ĐO ĐƯỢC trực tiếp** | Run 41113949578, job 124263645262; workflow_dispatch ci.yml, HEAD đúng, labels windows-latest, runner_id=1000026867; bien-nhan 98/98 · 153/153 · 2/2, TỔNG: ĐẠT; lease 255/255. Chi tiết/giới hạn bên dưới. |
| C5 Ubuntu CI | **ĐẠT run PR gắn đúng HEAD** | Run 41113943723, job 124264022785; event pull_request, head_sha đúng, labels ubuntu-latest, runner_id=1000026883; bien-nhan 98/98 · 153/153 · 2/2, TỔNG: ĐẠT; lease 268/268. Checkout merge thử được phân biệt bên dưới. |
| C6 | **ĐẠT** | rc=0, tổng 306 khớp lệnh đếm riêng 306, 0 KHÔNG ĐO ĐƯỢC, TỔNG: ĐẠT. |
| C7 Windows local | **KHÔNG ĐO ĐƯỢC / không chạy** | Không chạy test Windows từ xa, đúng chỉ thị lượt 9; không nhận lời khai executor. |
| C8 nội dung review | **ĐẠT theo ngưỡng lượt 9** | P0/P1/P2/P3 mở đều 0; C6 và suite Linux đạt trên đúng HEAD. Áp chỉ thị 9/9 hiện hành, không tự sửa SPEC đóng băng và không suy quyền merge/land. |
| C9 | **ĐẠT theo delta** | Ruff thêm 0/mất 0; doctrine sạch 10 tệp; hai diff-check rc=0; rg glob 0 dòng, đối chứng bản sao 1 dòng; numstat đúng hai tệp. |
| Toàn suite Linux | **ĐẠT** | rc=0, **98/98 · 153/153 · 2/2**, TỔNG: ĐẠT; 339.767 giây; stderr rỗng; không có BỎ QUA. |
| Đột biến riêng | **ĐẠT** | 16/16 m142–m157 `giet_that` đúng ca; 16/16 đối chứng nghiêm sạch khi mutant còn hiệu lực. |

C6 nguyên văn:

```text
bien_nhan_v2: 253 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 306
câu lịch sử: nợ L-REVIEW 1 · L-ANCESTRY 60 · L-SURFACE 0 · L-SURFACE chua_do_duoc 0
TỔNG: ĐẠT
```

[C6 stdout](evidence/15-c6.stdout.txt), [lệnh/rc/thời gian](evidence/15-c6.json), [đếm độc lập bằng os.listdir, không lọc is_file](evidence/17-count.json).

Suite nguyên văn:

```text
bien_nhan_v2_test: 98/98 ca đạt · 153/153 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 135/153 đột biến thường khai đối chứng
TỔNG: ĐẠT
```

[Suite stdout](evidence/16-suite.stdout.txt), [lệnh/cwd/rc/thời gian](evidence/16-suite.json). Validator còn đếm riêng 98 tên ca ĐẠT, không trùng; xác nhận c14/c40/c76 và c88/c89/c98/c99/c100/c101. Ba ca từng đỏ do snapshot đều xanh, không bỏ hoặc giảm mẫu số.

C1a/C1b/C3: [ma trận 3×3 sạch/exact/glob](evidence/c1-results.json). C9: [delta Ruff](evidence/ruff-delta-results.json), [doctrine](evidence/25-doctrine.stdout.txt), [diff-check tổng](evidence/26-diff-check.json), [diff-check checkout](evidence/27-working-diff-check.json), [rg âm](evidence/28-glob-negative.json), [đối chứng rg dương](evidence/38-glob-positive.stdout.txt). Ruff dùng executable có sẵn với `--no-cache --select F`, lint blob base/head cùng cwd/config, chuẩn hóa path/code/message/nội dung dòng. Hai phía cùng một **F541** có sẵn ở test (HEAD:1681): **delta 0, không phải Ruff sạch tuyệt đối**.

## CI đọc độc lập và giới hạn

Đã đọc mới jobs/logs và API thô, không gọi workflow. Hai lần `gh api` rc=1 vì sandbox không cho mở socket được giữ ở [Windows](evidence/30-ci-raw-windows.stderr.txt), [Ubuntu](evidence/31-ci-raw-ubuntu.stderr.txt); sau đó GET qua plugin trả đầy đủ JSON gốc, giải quyết giới hạn labels/runner_id của lượt 8.

- [Windows run 41113949578 / job 124263645262](https://github.com/ducthangho/tra-luat/actions/runs/41113949578/job/124263645262): checkout đúng HEAD, OS Windows Server 2025; hai bước đều completed/success. Lease-publish **255/255; đã chạy=255, bỏ qua=13**; không viết thành 268/268 hoặc nói không có ca bỏ qua. Chính bước selftest không skipped. [Run thô](evidence/ci-raw-windows-run.json), [jobs thô](evidence/ci-raw-windows-jobs.json), [log](evidence/ci-windows-log.txt).
- [Ubuntu run 41113943723 / job 124264022785](https://github.com/ducthangho/tra-luat/actions/runs/41113943723/job/124264022785): run và job có head_sha đúng HEAD; OS Ubuntu 24.04.5; hai bước completed/success, lease 268/268, bỏ qua 0. Checkout thực tế **00c58bc70286f622914f07e36d72691d192b3949**, merge thử HEAD vào 6db934145acf6e47d01db5b2dc8c9da417c2d8eb. Đây là CI PR gắn HEAD, không khai checkout trực tiếp HEAD. [Run thô](evidence/ci-raw-ubuntu-run.json), [jobs thô](evidence/ci-raw-ubuntu-jobs.json), [log](evidence/ci-ubuntu-log.txt).

Input `runner_set` không có trong JSON run. Đã đọc đủ 16/16 job Windows, chỉ có các job ma trận Windows; [biểu thức workflow trên HEAD](evidence/33-workflow-input.stdout.txt) chỉ chọn ma trận đó cho dispatch windows-only. Đây là **suy luận từ workflow và đồ thị job độc lập**, không phải đọc được payload input gốc; vẫn giữ giới hạn ở C4. Labels/runner_id nêu trên là dữ liệu API thô, không suy từ tên job/OS. C7 không có phép đo local. Không biến các giới hạn này thành finding mã mới.

## Bảng finding

**Tổng finding mở: 0 — P0=0, P1=0, P2=0, P3=0.** Không có finding mới cần mục vị trí/tái hiện/HÌNH DẠNG/hướng vá.

| Mục | Loại | Trạng thái |
|---|---|---|
| `snapshot-thieu-object-lich-su` | Trở ngại snapshot/bằng chứng, không gán severity mã | Đã khắc phục; C6 và suite đo mới đạt |
| Các lớp P lịch sử | Finding đã đóng, chi tiết bảng đối chiếu | Giữ đóng bằng đo lại/kế thừa được phép |
| C4 input dispatch gốc; C7 local | Giới hạn phép đo | Khai rõ, không tính thành finding mã |

## Kiểm tra cuối và giới hạn

[validate_review.py](validate_review.py) kiểm rc thật, chuỗi tổng và mẫu số, 98 tên ca, riêng c14/c40/c76, từng đột biến/đối chứng, delta Ruff, dữ liệu CI thô và snapshot. Kết quả **FINAL EVIDENCE ASSERTIONS PASS** trong [final-validation.json](evidence/final-validation.json).

Snapshot [đầu](evidence/snapshot-before.json) / [cuối](evidence/snapshot-after.json) bằng nhau về HEAD/tree, index, băm 8.468 tệp tracked, diff staged/unstaged và trạng thái tracked/untracked/ignored. TMPDIR đã rỗng. Đây là so sánh hai mốc quan sát; không suy thành audit toàn bộ lịch sử ghi. Không sửa tệp trong cay-kho, không commit/push/fetch hay gọi workflow trên kho được review. Các kho fixture riêng trong sandbox do bộ test dựng không phải cây executor.

Verdict đã được tạo và cập nhật từ đầu lượt; bản tiến độ giữ ở [VERDICT-progress.md](evidence/VERDICT-progress.md). Kết luận approve chỉ áp cho exact HEAD trên và phạm vi review này; metadata/model attestation và thủ tục cấp quyền land thuộc bước giao nhận riêng, không được verdict tự cấp.
<!-- VERDICT-L9-KET-THUC -->
