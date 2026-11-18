# WP1389 r1 — kết quả đo (executor: Claude Code, phiên `session_015GtxrazyAyLwN5BiEB52Sq`)

Spec: `ops/specs/wp1389-r1.md` (sha256 `12257fa8…10bc`). Lease: `ops/leases/wp1389-r1-g1-claude.yaml`.
Base `eca1d125b8`. SKILL tại base: blob `678ba2f0`, sha256 `1799c2bd…faadb`.
**Head mã đã đo: `783e219db3bf2985eb601b26f546d27d6bd99c1b`** (tree `decaa0df…`). Tại head này:
- SKILL: blob `daba88a1`, sha256 `92d1bde3a0c34f5a178b4c87e775555893017ee4b2c4a1dd820329f43f5c34b4`.
- `residue_matrix.sh`: sha256 `cc5f864c…4617e`. `residue_matrix.ps1`: sha256 `d4099282…60ef`.

Commit sau đó chỉ thêm tệp này và `REVIEW-PROMPT.md`. Hai head trước bị local Windows bắt lỗi (§6) rồi được vá:
- `045c913a5d77` (bản đầu);
- `bcc239ca2b88`.

Bằng chứng thô nằm NGOÀI Git:
- Linux: `/tmp/claude-0/` trong container của phiên. Container tạm, nên mọi số cần giữ đều chép vào tệp này.
- Windows: `F:\tl-win\session_015GtxrazyAyLwN5BiEB52Sq\wp1389\evidence\` trên Desktop.

## 0. Nguồn CLI đã ghim (căn cứ chọn phương án b)

- `npm pack` lấy `@playwright/cli@0.1.23` và `playwright-core@1.65.0-alpha-2026-10-30`. SRI sha512 của hai tarball bằng
  đúng `integrity` trong `package-lock.json`.
- `playwright-core/lib/tools/cli-client/registry.js:119-131` `computeBaseDaemonDir`: `PWTEST_DAEMON_SESSION_DIR`, hoặc
  Linux `XDG_CACHE_HOME || ~/.cache`, Windows `LOCALAPPDATA || ~\AppData\Local`, rồi nối `ms-playwright/daemon`.
- `:137-148` `createClientInfo`: hash = `sha1(workspaceDir || packageRoot).slice(0,16)`. Đo: `printf %s
  /tmp/claude-0/tlpw-base/install/0.1.0/node_modules/playwright-core | sha1sum` ⇒ `3815e4e10d63867a`. Bằng đúng thư mục
  con mà CLI đã tạo.
- `session.js:121-126` `startDaemon`: tạo `<name>.err` bằng `openSync(errLog, "w")`. `session.js:73-97` `deleteData`:
  chỉ lọc `<name>.session` và `ud-<name>-*`.
- `serverRegistry.js:1847-1848,1927-1928`: `ms-playwright/b` = `PWTEST_SERVER_REGISTRY` hoặc cache mặc định.
- `@playwright/cli` README và `references/session-management.md`: không có tuỳ chọn nào để dời sổ phiên.
  ⇒ (a) không khả dụng.

## 1. Tái hiện F1 trên Linux tại base (trước sửa)

- Container Linux x64, Node `v24.19.0` (SHASUMS256 nodejs.org khớp), npm `11.9.0` (`npm pack npm@11.9.0`).
- Các khối bash của SKILL được trích nguyên byte; chỉ thay placeholder. Môi trường sạch (`env -i`, giữ proxy/CA).
- `SETUP OK`, `PIN OK`, Capture `https://example.com/`, IDX=1, `CLEANUP OK`.
- Sau Cleanup, `~/.cache/ms-playwright` còn tệp `daemon/3815e4e10d63867a/tl-pw-cedba9810ed1.err` (0 byte), cùng các thư
  mục `b`, `daemon`, `daemon/3815e4e10d63867a`. Tệp `.err` này để nguyên làm "tệp cũ" cho các lượt sau.

## 2. N1 — ma trận bash (Linux)

`bash ops/acceptance/wp1389/residue_matrix.sh .agents/skills/playwright-browser/SKILL.md <scratch rỗng>` tại `783e219`.
Kết quả giống hệt ở `045c913` và `bcc239c`: hai commit vá chỉ đụng khối PowerShell, đoạn bash có cùng sha256.

```
SOURCE 92d1bde3a0c34f5a178b4c87e775555893017ee4b2c4a1dd820329f43f5c34b4 cleanup_frag ee956fa4b3e439ab43a777ef47ba0288e0d9ce9c1c24d9b51bb7837c57b6073c pre_frag c459af715dcd2a39f2f8a8787f317a47ed7e28aa3f2805ff47a5508488f72ca0
TONG: 30 dat / 30        rc=0
```

- Ca dương:
  - P1: tệp gốc bị xoá; `11-daemon.err` trùng byte; `11-daemon-path.txt` đúng đường dẫn.
  - P2: `.err` 0 byte.
- Ca phản chứng, đều rc≠0, có `STOP`, không `RESIDUE_OK`:
  - N1 0 mục · N2 hai thư mục hash · N3 `.session` sót · N4 `ud-` sót · N5 `.err` là symlink · N6 thư mục hash là
    symlink · N7 sổ phiên là symlink · N8 output cũ · N9 tên hash sai dạng · N10 `PWTEST_DAEMON_SESSION_DIR` ·
    N11 `.err` là thư mục · N12 chưa có sổ phiên.
  - Mỗi ca đều kiểm "mồi" của phiên khác và `.err` cũ vẫn giữ nguyên tên/kích thước/mtime/sha256. Tệp gốc cũng còn
    nguyên khi lẽ ra phải còn.
- Kiểm trước open: C1 sạch ⇒ qua · C2 nonce đã có ⇒ dừng · C3 chưa có `ms-playwright` ⇒ qua.
- 7 đột biến, mỗi đột biến làm ca đích của nó LỌT (`RESIDUE_OK`):
  - exact-one→N2 · name-glob→N3 · no-symlink-check→N5 · daemon-symlink→N7 · stale-output→N8 · hash-shape→N9 ·
    pwtest-hook→N10.
  - Không có đột biến đích riêng: N1, N4, N6, N11, N12, C1–C3.
- Chạy với SKILL tại base (chưa sửa) ⇒ `FAIL: can 2 cap danh dau (bash+ps), thay 0`, rc 1.

## 3. N2 — ma trận PowerShell (Desktop `DESKTOP-T9R33P2`, local, ADR-0057)

`residue_matrix.ps1` chạy từ bản clone tại head trên Desktop, scratch rỗng riêng cho mỗi shell.
- Mỗi ca chạy trong tiến trình con của chính shell đang đo, với `LOCALAPPDATA` trỏ vào scratch.
- PS 5.1 được gọi với `PSModulePath` bằng giá trị Machine. Không có nó thì thiếu `Get-FileHash`; đây là lỗi dựng
  harness, lần đầu đã làm hỏng lượt ps51 ở `045c913`.

| head | shell | kết quả | rc |
|---|---|---|---|
| `045c913` | pwsh 7.6.10 | `TONG: 28 dat / 29 (bo qua khong do duoc: 1)`: **FAIL N12** (§6) | 1 |
| `bcc239c` | PS 5.1 / pwsh 7 | `TONG: 29 dat / 29 (bo qua: 1)` cả hai | 0 / 0 |
| `783e219` | PS 5.1 (`5.1.26100`) | `TONG: 33 dat / 33 (bo qua khong do duoc: 1)` | 0 |
| `783e219` | pwsh 7.6.10 | `TONG: 33 dat / 33 (bo qua khong do duoc: 1)` | 0 |

- `SOURCE` ở `783e219` (cả hai shell): SKILL `92d1bde3…`, cleanup_frag (PS) `a0b9b62c46ef5492…`, pre_frag (PS) `14542fe69cb25ce0…`. Các băm này tính trên tệp có BOM UTF-8 do harness PS ghi ra. Trích lại trên Linux, thêm BOM rồi băm thì ra đúng hai giá trị ấy.
- Ca giống bản bash: P1, P2, N1–N4, N6, N7 (dùng junction thay symlink), N8–N12 và C1–C3.
- Ca riêng Windows:
  - N13: bản viết hoa `TL-PW-…ERR` ở thư mục hash khác. NTFS không phân biệt hoa thường, nên đó là mục thứ hai ⇒ STOP.
  - L1: một tiến trình khác giữ `.err` với `FileShare.None` trong 2 s ⇒ chờ rồi qua, bản sao trùng sha256.
  - L2: giữ 12 s ⇒ STOP, tệp gốc còn.
- Đột biến (7):
  - Làm ca đích LỌT: exact-one→N2 · name-filter→N3 · daemon-reparse→N7 · stale-output→N8 · hash-shape→N9 ·
    pwtest-hook→N10.
  - no-copy-retry (vòng chờ còn 1 lần) làm L1 ĐỎ.
- **KHÔNG ĐO ĐƯỢC: N5** (`.err` là symlink tệp). Máy không cấp `SeCreateSymbolicLink` và không bật Developer Mode, nên
  ghi `SKIP`, không tính đạt. Chốt tương ứng (cấm reparse point trên tệp) vì thế chỉ được đo ở bản bash.
- Tệp: `F:\tl-win\session_015GtxrazyAyLwN5BiEB52Sq\wp1389\evidence\N2-<head>-<shell>.out`, `N2-rc.txt`.

## 4. N3 — Linux native (SKILL tại head)

Hai lượt, mỗi lượt một `TL_PW_ROOT` mới. Chạy đủ Setup → Kiểm pin → Capture `https://example.com/` → Cleanup → Gỡ bản cài
(làm theo đúng văn xuôi SKILL, bằng đường dẫn hằng).

| head | nonce | thư mục hash | Setup / Pin / Cleanup | `11-daemon.err` | Gỡ: `daemon/<hash>` |
|---|---|---|---|---|---|
| `045c913` | `tl-pw-24acb5c4b5ad` | `8dba0eb089d06357` | `SETUP OK` / `PIN OK` / `CLEANUP OK` | 0 byte, sổ phiên đã xoá | 0 mục ⇒ `rmdir` rc 0 |
| `bcc239c` | `tl-pw-9e7c3371d342` | `b9256d8802e4db86` | `SETUP OK` / `PIN OK` / `CLEANUP OK` | 0 byte, sổ phiên đã xoá | 0 mục ⇒ `rmdir` rc 0 |
| `783e219` | `tl-pw-685c1e70f409` | `bb22e618b9082199` | `SETUP OK` / `PIN OK` / `CLEANUP OK` | 0 byte, sổ phiên đã xoá | 0 mục ⇒ `rmdir` rc 0 |

- Ở `bcc239c` và `783e219`, 5 khối bash trùng byte với `045c913`. Các commit vá chỉ đụng khối PowerShell.
- Ảnh chụp `~/.cache/ms-playwright` gồm loại, kích thước, sha256, mtime và đường dẫn. Ở cả ba lượt, ảnh trước Setup
  và ảnh sau Gỡ **trùng byte**: sha256 tệp ảnh chụp `8c247ab02e544cb8…` cả sáu lần.
  - ⇒ 0 tệp mới, 0 thư mục mới.
  - `.err` cũ `tl-pw-cedba9810ed1.err` còn nguyên, cùng thư mục `cc317b6c0c1b6fcc` của lượt nguyên mẫu.
- Ngay sau `CLEANUP OK`, thay đổi duy nhất là thư mục rỗng `daemon/<hash>` của bản cài. Gỡ bản cài xoá nó.
- `ms-playwright/b`: tệp `browser@…` có trong lúc chạy và mất sau `close`. Thư mục `b` đã có sẵn từ lượt ở §1.
- `10-verify`: rc 1, `"The browser 'tl-pw-9e7c3371d342' is not open, please run open first"`.
  `SHA256SUMS` có 30 dòng, gồm cả `11-daemon.err` và `11-daemon-path.txt`.
- Tiến trình dùng bản cài lúc gỡ: `pgrep -af <root>` không thấy gì (rc 1).

## 5. N4 — Windows native (Desktop, pwsh 7.6.10, local)

Khối PowerShell của SKILL được trích nguyên byte; chỉ thay placeholder, cộng dạng `*>&1 | Tee-Object` mà chính SKILL
ghi cho Kiểm pin.
- Mỗi bước (Setup; Kiểm pin + Capture; Capture tiếp + Cleanup) là một tiến trình pwsh riêng. stdout/stderr chuyển hướng
  ở mức tiến trình.
- Node `v26.13.0`, npm `11.20.0` (`C:\Program Files\nodejs`, như r3 của #1319). `TL_PW_ROOT` mới mỗi lượt, ngoài Git
  (`git rev-parse` rc 128 đúng thông báo).
- Gỡ bản cài làm theo văn xuôi SKILL:
  - kiểm tiến trình chỉ đọc, bằng `Get-CimInstance`;
  - xoá `install\0.1.0` và `browsers\0.1.0`;
  - đếm mục của thư mục cha trong `11-daemon-path.txt` = 0 rồi mới `Remove-Item` không đệ quy.

| head | nonce | `daemon\<hash>` | Pin / Cleanup | `ms-playwright` trước → sau Cleanup → sau Gỡ |
|---|---|---|---|---|
| `bcc239c` | `tl-pw-eab3a5404a52` | `d9a951d4e51ecd16` | `PIN OK` / `CLEANUP OK`, stderr 0 byte | 28 → 29 (+ thư mục hash rỗng) → 28, **trùng byte** |
| `783e219` | `tl-pw-ea1a16a46157` | `36f56a26df82f0f5` | `PIN OK` / `CLEANUP OK`, stderr 0 byte | 28 → 29 (+ thư mục hash rỗng) → 28, **trùng byte** |

- Ảnh chụp `%LOCALAPPDATA%\ms-playwright` gồm loại, kích thước, sha256, mtime (ticks) và đường dẫn. Ảnh trước và
  ảnh sau Gỡ đều có sha256 `a36424f64d972ffd61a4428f6b30ae516c00bfae2ec492c63eb7c6a50febf1f5`, ở cả hai head.
  - 15 tệp `.err` có từ trước giữ nguyên tên, kích thước, sha256 và mtime: 13 tệp của P2/P3 (08–11/11, trong đó hai tệp
    2 482 và 2 294 byte) và 2 tệp của #1319 r1/r3 ngày 18/11.
  - ⇒ 0 tệp mới, 0 tệp cũ bị đụng.
- Giữa lượt (sau Capture, trước Cleanup): thêm `b\browser@…`, cùng `daemon\<hash>\` chứa `<nonce>.err` (**khoá đọc**,
  `Get-FileHash` báo "being used by another process") và `<nonce>.session`.
  Sau Cleanup chỉ còn thư mục hash rỗng; `b\browser@…` đã mất.
- `commands.tsv`: `01`…`09` rc 0, `10-verify` rc 1, đúng mẫu.
  - `11-daemon-path.txt` = đường dẫn `.err` gốc. `11-daemon.err` 0 byte.
  - `SHA256SUMS.csv` có 30 dòng, gồm cả hai tệp `11-*`.
- Setup stderr 209 byte, chỉ là `npm notice New major version of npm available! 11.20.0 -> 12.2.3`. Bảng ghim không đổi.
- Khoá `C:\tl-win\KHOA.txt` và `F:\tl-win\KHOA.txt`:
  - lấy lúc 10:05:54Z khi cả hai rỗng; nhịp tim 10:11, 10:18, 10:20, 10:21Z; nhả (0 byte) sau lượt cuối.
  - Lúc lấy khoá có tiến trình của phiên khác (`session_015GtxrapMSm976JLC7Fp1HM`, nén bằng chứng wp1319-r3). Đã ghi
    lại, không đụng tới.
- Đã ghi 3 dòng vào `C:\tl-win\do-luong.csv`. `F:\tl-win\do-luong.csv` không tồn tại.

## 6. Lỗi do local Windows bắt (ADR-0057: lỗi do diff gây ra phải vá trước merge)

| # | head lỗi | quan sát | vá ở | ca khoá |
|---|---|---|---|---|
| W1 | `045c913` | Chưa có sổ phiên: Cleanup PS dừng (rc 1) bằng ngoại lệ `Get-Item` thô, không qua `Need`/`STOP` như bash. Vẫn đóng an toàn, nhưng thông báo lệch hợp đồng. | `bcc239c`: `Need (Test-Path … -PathType Container)` | N12 (PS) |
| W2 | `bcc239c` | Khi daemon còn sống, `<nonce>.err` bị khoá cả ĐỌC (đo giữa lượt N4). Bản trước chỉ thử lại bước XOÁ. Nếu daemon nhả handle chậm hơn `10-verify`, bước CHÉP sẽ hỏng và Cleanup thất bại (đóng an toàn, nhưng hỏng thật). Chưa gặp trong lượt chạy; lỗi được đo qua cơ chế khoá. | `783e219`: bước chép cũng thử lại 5 × 1 s | L1, L2, đột biến no-copy-retry |

## 7. Chưa đo được / giới hạn

- N5 trên Windows (symlink tệp): KHÔNG ĐO ĐƯỢC (§3).
- Chỉ đo một máy Windows (Desktop). ASUS và VM không được chạy trong packet này.
- `ms-playwright\b` và `ms-playwright\daemon` là thư mục dùng chung. Skill không xoá chúng; Limits khai điều này.
  Trên hai máy đã đo, chúng có từ trước nên không xuất hiện trong diff. Trên máy mới tinh, chúng sẽ là hai thư mục rỗng
  còn lại sau khi gỡ, kể cả `b`. Hệ quả này suy từ mã (§0), chưa đo trên máy sạch.
- Đã đo cửa sổ khoá L1/L2. Thời gian thật để daemon nhả handle sau `10-verify` thì chưa đo; hai lượt N4 không cần thử lại.
- Ma trận dùng fixture tệp, không có daemon thật. Lượt native là thứ duy nhất chạy với CLI và trình duyệt thật.
- CI của PR chưa chạy khi viết tệp này; xem PR.
