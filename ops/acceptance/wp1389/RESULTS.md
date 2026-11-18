# WP1389 r1 — kết quả đo (executor: Claude Code, phiên `session_015GtxrazyAyLwN5BiEB52Sq`)

Spec: `ops/specs/wp1389-r1.md` (sha256 `12257fa8…10bc`). Lease: `ops/leases/wp1389-r1-g1-claude.yaml`.
Base `eca1d125b8`. SKILL tại base: blob `678ba2f0`, sha256 `1799c2bd…faadb`.

**Head mã đã đo: `6896f164db73a16c6c4f92d02cd556dad1c1b3c4`** (tree `0fad4a51…`).
- SKILL blob `a85fc945`, sha256 `c3b07090ba6352e65792eeaaa93bd2f408acc0f37f3407b28db4f4975bcdef34`.
- `residue_matrix.sh` `8644d91d…614e`, `residue_matrix.ps1` `249db000…83e9`.
- Commit sau `6896f16` chỉ đổi tệp này, `VERDICT.md`, `REVIEW-PROMPT.md` và nhịp tim/ngân sách trong lease.

Lịch sử head:
- `045c913` (bản đầu) → `bcc239c` (W1) → `783e219` (W2).
- Review Codex lượt 1 ở `4aae991`: `request_changes`.
- `5c01f39`: sửa theo lượt 1. `6896f16`: sửa W3, W4 (§6).

Bằng chứng thô nằm NGOÀI Git:
- Linux: `/tmp/claude-0/` trong container của phiên. Container tạm, nên mọi số cần giữ đều chép vào tệp này.
- Windows: `F:\tl-win\session_015GtxrazyAyLwN5BiEB52Sq\wp1389\evidence\` trên Desktop `DESKTOP-T9R33P2`.

## 0. Nguồn CLI đã ghim (căn cứ chọn phương án b)

- `npm pack` lấy `@playwright/cli@0.1.23` và `playwright-core@1.65.0-alpha-2026-10-30`. SRI sha512 khớp `integrity`
  trong `package-lock.json`. Reviewer lượt 1 kiểm lại độc lập, kèm `playwright`.
- `playwright-core/lib/tools/cli-client/registry.js:119-131` `computeBaseDaemonDir`: `PWTEST_DAEMON_SESSION_DIR`, hoặc
  Linux `XDG_CACHE_HOME || ~/.cache`, Windows `LOCALAPPDATA || ~\AppData\Local`, rồi nối `ms-playwright/daemon`.
- `:137-148` `createClientInfo`: hash = `sha1(workspaceDir || packageRoot).slice(0,16)`.
  Đo: SHA-1 của `/tmp/claude-0/tlpw-base/install/0.1.0/node_modules/playwright-core` ⇒ `3815e4e10d63867a`, trùng thư mục
  CLI tạo.
- `session.js:121-126` `startDaemon`: tạo `<name>.err` bằng `openSync(errLog, "w")`.
- `session.js:73-97` `deleteData`: chỉ lọc `<name>.session` và `ud-<name>-*`.
- `serverRegistry.js:1847-1848,1927-1928`: `ms-playwright/b` = `PWTEST_SERVER_REGISTRY` hoặc cache mặc định.
- README và `references/session-management.md`: không có tuỳ chọn dời sổ phiên ⇒ (a) không khả dụng. Reviewer lượt 1
  đồng ý.

## 1. Tái hiện F1 trên Linux tại base (trước sửa)

- Container Linux x64, Node `v24.19.0` (SHASUMS256 khớp), npm `11.9.0`.
- Khối bash của SKILL được trích nguyên byte, chỉ thay placeholder; chạy trong môi trường sạch (`env -i`, giữ proxy/CA).
- `SETUP OK` / `PIN OK` / Capture `https://example.com/` / IDX=1 / `CLEANUP OK`.
- Sau đó còn `daemon/3815e4e10d63867a/tl-pw-cedba9810ed1.err` (0 byte), cùng các thư mục `b`, `daemon`, `daemon/<hash>`.
  Tệp này để nguyên, làm "tệp cũ" cho các lượt sau.

## 2. N1 — ma trận bash (Linux)

`bash ops/acceptance/wp1389/residue_matrix.sh .agents/skills/playwright-browser/SKILL.md <scratch rỗng>` tại `6896f16`:

```
SOURCE c3b07090ba6352e65792eeaaa93bd2f408acc0f37f3407b28db4f4975bcdef34 cleanup_frag 04aec5e00ca2cd17ebbdd5f8163c55a776433135dc436c4a6fa4b89dbba6a955 pre_frag 25375d548f85ce9a7b9270758a60e31fec47675ffdcff620df6f2725dcafa12a
TONG: 39 dat / 39        rc=0
```

- Đoạn trích là NỘI DUNG giữa cặp đánh dấu, không gồm dòng đánh dấu. Harness đòi đúng 2 cặp, không lồng nhau.
- Ca dương:
  - P1 (`.err` có nội dung) và P2 (`.err` 0 byte).
  - Tệp gốc mất; `11-daemon.err` trùng byte; `11-daemon-path.txt` đúng.
  - Mọi tệp mồi giữ nguyên **nội dung (sha256)**, kích thước và mtime.
- Ca phản chứng: rc≠0, có `STOP`, không `RESIDUE_OK`.
  - Mồi nguyên vẹn. Các tệp mang nonce trong ca giữ nguyên sha256.
  - Không sinh output `11-*` mới. Riêng N8 kiểm output cũ không bị ghi đè.
  - Danh sách:
    - N1 0 mục · N2 hai thư mục hash · N3 `.session` sót · N4 `ud-…/Prefs` sót.
    - N5 `.err` là symlink · N6 thư mục hash là symlink · N7 sổ phiên là symlink.
    - N8 `11-daemon.err` cũ · N8 `11-daemon-path.txt` cũ · N9 tên hash sai dạng · N10 hook `PWTEST_DAEMON_SESSION_DIR`.
    - N11 `.err` là thư mục · N12 chưa có sổ phiên.
  - Ca mới theo lượt 1:
    - N14 `<nonce>Xerr` (hậu tố sai).
    - N15: phép quét trả một mục hợp lệ rồi lỗi rc 1, dùng `find` giả (container chạy root nên không chặn bằng quyền
      được).
    - N16 tên có xuống dòng.
    - N17 `XDG_CACHE_HOME` tương đối, có sẵn một sổ phiên thật ở đường dẫn ấy, nên chỉ chốt tuyệt đối mới chặn được.
- Kiểm trước `open` (chạy dưới `set -Eeuo pipefail` như khối Capture):
  - C1 sạch ⇒ qua · C2 nonce có sẵn ⇒ dừng · C3 chưa có `ms-playwright` ⇒ qua.
  - C4 cache tương đối, trong khi sổ CLI nhìn từ CWD đã có `.err` cùng nonce ⇒ dừng.
  - C5 hook đặt sau Kiểm pin ⇒ dừng · C6 mục mang nonce ở độ sâu 1 ⇒ bỏ qua, như CLI.
  - C7 phép quét lỗi, không in gì ⇒ dừng.
- 13 đột biến, mỗi đột biến làm ca đích của nó LỌT:
  - exact-one→N2 · name-glob→N3 · no-symlink-check→N5 · daemon-symlink→N7 · stale-output→N8 · hash-shape→N9 ·
    pwtest-hook→N10.
  - dot-wildcard→N14 · no-scan-rc→N15 · relative-cache→N17 · pre-relative→C4 · pre-scan-rc→C7 · pre-hook→C5.
  - Không có đột biến đích: N1, N4, N6, N11, N12, N16, C1–C3, C6.
- Kiểm chính harness: một SKILL biến thể ghi thêm 1 byte vào mọi tệp mồi rồi trả lại mtime cũ.
  - Kết quả tại `5c01f39`: harness rc 1, P1/P2 FAIL, `35/37`.
  - ⇒ Harness phát hiện được nội dung mồi bị đổi kể cả khi mtime giữ nguyên.

## 3. N2 — ma trận PowerShell (Desktop, local, ADR-0057)

`residue_matrix.ps1` chạy từ bản clone tại head, mỗi shell một scratch rỗng riêng.
- Mỗi ca chạy trong tiến trình con của chính shell đang đo; `LOCALAPPDATA` trỏ vào scratch; CWD = `<ca>\home`.
- PS 5.1 được gọi với `PSModulePath` bằng giá trị Machine.
- SOURCE/frag băm trên byte gốc (LF, không BOM). Bản chạy cho PS 5.1 là tệp wrapper có BOM.

| head | PS 5.1 (`5.1.26100`) | pwsh 7.6.10 |
|---|---|---|
| `045c913` | (lỗi dựng harness: thiếu `PSModulePath` Machine) | `28/29`, **FAIL N12** ⇒ W1 |
| `bcc239c` | `29/29` | `29/29` |
| `783e219` | `33/33` | `33/33` |
| `5c01f39` | `40/40`, nhưng P2 chưa thực sự đo (W4) | **rc 1 ở N15**: Cleanup XOÁ `.err` ⇒ W3 |
| **`6896f16`** | **`44/44` rc 0** | **`44/44` rc 0** |

- Mỗi lượt có 1 SKIP (N5, xem dưới).
- Tệp kết quả: `N2-6896f16-ps51.out` (sha256 `b7099820…f2b6`), `N2-6896f16-ps7.out` (`421ce677…d2f2`).
  Cả hai in `SOURCE c3b07090… cleanup_frag b62eaf6e… pre_frag f6cbe7b8…`.
- Ca giống bản bash: P1/P2 (kèm kiểm cỡ fixture), N1–N4, N6/N7 (bằng junction), N8 ×2, N9–N12, N14, N17, C1–C6.
- Ca riêng Windows:
  - N13: bản viết hoa `TL-PW-…ERR` ở thư mục hash khác ⇒ dừng, cả hai tệp nguyên.
  - N15: thư mục hash bị `icacls /deny (RD)` ⇒ dừng. C7: như N15 nhưng ở bước trước `open`.
  - L1: tiến trình khác giữ `.err` với `FileShare.None` 2 s ⇒ chờ rồi qua. L2: giữ 12 s ⇒ dừng, tệp gốc nguyên.
  - L3: `FileShare.Read` 2 s (đọc được, không xoá được) ⇒ vòng xoá chờ rồi qua.
- 15 đột biến:
  - 13 đột biến làm ca đích LỌT: exact-one→N2 · name-filter→N3 · daemon-reparse→N7 · stale-output→N8 · hash-shape→N9
    · pwtest-hook→N10 · exact-name→N14 · scan-silent→N15 · relative-cache→N17 · pre-relative→C4 ·
    pre-scan-silent→C7 · pre-hook→C5.
  - no-copy-retry làm L1 ĐỎ; no-delete-retry làm L3 ĐỎ.
- **KHÔNG ĐO ĐƯỢC: N5** (`.err` là symlink tệp). Máy không có quyền tạo symlink tệp, nên ca được ghi `SKIP`, không tính
  đạt. Chốt "tệp không phải reparse point" của bản PS chỉ được kiểm bằng đọc mã; bản bash thì đo được (N5 ở §2).

## 4. N3 — Linux native (SKILL tại từng head)

Mỗi lượt một `TL_PW_ROOT` mới, chạy đủ Setup → Kiểm pin → Capture `https://example.com/` → Cleanup → Gỡ bản cài. Bước Gỡ
làm theo đúng văn xuôi SKILL, bằng đường dẫn hằng.

| head | nonce | thư mục hash | Setup / Pin / Cleanup | `11-daemon.err` | Gỡ: `daemon/<hash>` |
|---|---|---|---|---|---|
| `045c913` | `tl-pw-24acb5c4b5ad` | `8dba0eb089d06357` | OK / OK / OK | 0 byte, gốc đã xoá | 0 mục ⇒ `rmdir` rc 0 |
| `bcc239c` | `tl-pw-9e7c3371d342` | `b9256d8802e4db86` | OK / OK / OK | 0 byte, gốc đã xoá | 0 mục ⇒ `rmdir` rc 0 |
| `783e219` | `tl-pw-685c1e70f409` | `bb22e618b9082199` | OK / OK / OK | 0 byte, gốc đã xoá | 0 mục ⇒ `rmdir` rc 0 |
| `5c01f39` | `tl-pw-ed1e9f54aca4` | `49a865cc19d4a015` | OK / OK / OK | 0 byte, gốc đã xoá | 0 mục ⇒ `rmdir` rc 0 |
| **`6896f16`** | `tl-pw-68d502917e06` | `51579324497e2ada` | OK / OK / OK | 0 byte, gốc đã xoá | 0 mục ⇒ `rmdir` rc 0 |

- 5 khối bash ở `6896f16` trùng byte với `5c01f39`; `6896f16` chỉ đổi khối PowerShell.
- Ảnh chụp `~/.cache/ms-playwright` ghi loại, kích thước, sha256, mtime và đường dẫn. Ở cả 5 lượt, ảnh trước Setup và
  ảnh sau Gỡ **trùng byte** (sha256 tệp ảnh chụp `8c247ab02e544cb8…`).
  - ⇒ 0 tệp mới, 0 thư mục mới. Tệp `.err` cũ `tl-pw-cedba9810ed1.err` còn nguyên.
- Ngay sau `CLEANUP OK`, thay đổi duy nhất là thư mục rỗng `daemon/<hash>` của bản cài.
- `10-verify`: rc 1, đúng thông báo của nonce. `SHA256SUMS` có 30 dòng, gồm cả hai tệp `11-*`.
- Lúc gỡ, `pgrep -af <root>` không thấy tiến trình nào (rc 1).

## 5. N4 — Windows native (Desktop, pwsh 7.6.10, local)

- Khối PowerShell của SKILL được trích nguyên byte; chỉ thay placeholder và thêm dạng `*>&1 | Tee-Object` mà SKILL ghi
  cho Kiểm pin.
- Mỗi bước là một tiến trình pwsh riêng, stdout/stderr chuyển hướng ở mức tiến trình: Setup; Kiểm pin + Capture;
  Capture tiếp + Cleanup.
- Node `v26.13.0`, npm `11.20.0`. `TL_PW_ROOT` mới mỗi lượt, nằm ngoài Git.
- Bước Gỡ:
  - kiểm tiến trình bằng `Get-CimInstance`, chỉ đọc;
  - xoá `install\0.1.0` và `browsers\0.1.0`;
  - với thư mục cha trong `11-daemon-path.txt`: đếm mục = 0 rồi mới `Remove-Item`, không đệ quy.
  - Từ `5c01f39`, văn xuôi Gỡ đổi sang `[IO.Directory]::Delete(p, $false)`. Dạng mới này chưa chạy native (§7).

| head | nonce | `daemon\<hash>` | Pin / Cleanup | `ms-playwright` trước → sau Cleanup → sau Gỡ |
|---|---|---|---|---|
| `bcc239c` | `tl-pw-eab3a5404a52` | `d9a951d4e51ecd16` | OK / OK, stderr 0 | 28 → 29 (+ thư mục hash rỗng) → 28, **trùng byte** |
| `783e219` | `tl-pw-ea1a16a46157` | `36f56a26df82f0f5` | OK / OK, stderr 0 | 28 → 29 → 28, **trùng byte** |
| **`6896f16`** | `tl-pw-787d3e252328` | `0c8dd11994b962c3` | OK / OK, stderr 0 | 28 → 29 → 28, **trùng byte** |

- Ở cả ba head, ảnh trước và ảnh sau Gỡ có cùng sha256 `a36424f64d972ffd61a4428f6b30ae516c00bfae2ec492c63eb7c6a50febf1f5`.
  - 15 tệp `.err` có từ trước giữ nguyên tên, kích thước, sha256 và mtime: 13 tệp của P2/P3 (08–11/11, có hai tệp
    2 482 và 2 294 byte), và 2 tệp của #1319 r1/r3.
- Giữa lượt có thêm: `b\browser@…`, cùng `daemon\<hash>\` chứa `<nonce>.err` (**bị khoá đọc**, `locked`) và
  `<nonce>.session`.
- `commands.tsv`: `01`…`09` rc 0, `10-verify` rc 1. `CLEANUP OK` ở `6896f16` (sha256 tệp out `f7b98047…`).
- Setup ghi 209 byte stderr, chỉ là `npm notice` về npm 12.2.3.
- Khoá `C:\tl-win\KHOA.txt` và `F:\tl-win\KHOA.txt` (5 trường, ADR-0057/58/59):
  - lấy hai lần: 10:05:54Z → nhả ~10:22Z, và 10:40:31Z → nhả ~10:49Z;
  - lúc lấy, cả hai tệp rỗng;
  - có tiến trình của phiên khác (`session_015GtxrapMSm976JLC7Fp1HM`): đã ghi lại, không đụng tới.
- Đã ghi 7 dòng vào `C:\tl-win\do-luong.csv`. `F:\tl-win\do-luong.csv` không tồn tại.

## 6. Lỗi do local Windows bắt (ADR-0057: lỗi do diff gây ra phải vá trước merge)

| # | head lỗi | quan sát | vá ở | ca khoá |
|---|---|---|---|---|
| W1 | `045c913` | Chưa có sổ phiên: Cleanup PS dừng bằng ngoại lệ `Get-Item` thô, không có `STOP` như bash. | `bcc239c`: `Need (Test-Path … -PathType Container)` | N12 |
| W2 | `bcc239c` | Daemon còn sống thì khoá **đọc** `<nonce>.err`. Bản cũ chỉ thử lại bước xoá, nên bước CHÉP có thể hỏng nếu daemon nhả handle chậm. | `783e219`: bước chép cũng thử lại 5 × 1 s | L1, L2, no-copy-retry |
| W3 | `5c01f39` | **pwsh 7.6.10**: `Get-ChildItem -ErrorAction Stop` trên thư mục bị từ chối liệt kê trả **0 mục, không lỗi**; PS 5.1 thì ném `UnauthorizedAccess`. Hệ quả: một mục mang nonce trong thư mục không đọc được bị bỏ sót, và Cleanup **xoá** `.err` rồi báo thành công. Đây chính là finding P1 "quét thiếu" của Codex lượt 1, tái hiện trên Windows. Probe hai shell: `[IO.Directory]::GetFileSystemEntries` ném lỗi ở cả hai. | `6896f16`: Capture và Cleanup PS quét bằng `[IO.Directory]::GetDirectories`/`GetFileSystemEntries` | N15, C7, scan-silent, pre-scan-silent |
| W4 | `5c01f39` | Bẫy harness (không phải SKILL): PowerShell không phân biệt hoa thường nên biến vòng `$c` CHÍNH LÀ `$script:C`. `New-Case` ghi đè nó, khiến P2 (`.err` rỗng) thực ra chạy như P1. | `6896f16`: đổi tên biến, thêm ca kiểm cỡ fixture | P1/P2-fixture-size |

## 7. Chưa đo được / giới hạn

- N5 trên Windows (symlink tệp): KHÔNG ĐO ĐƯỢC (§3). Chỉ đo một máy Windows; ASUS và VM không chạy.
- Lệnh `[IO.Directory]::Delete(p, $false)` trong văn xuôi Gỡ (Windows) chưa chạy native. Cả ba lượt N4 dùng dạng đếm rồi
  `Remove-Item`; dạng đã chạy ở lượt cuối (`6896f16`) cũng vậy.
- Thời gian thật để daemon nhả handle sau `10-verify` chưa đo. Các lượt N4 không cần thử lại; L1–L3 chỉ đo cơ chế chờ.
- Không chống hai trường hợp, đã khai trong Limits (lượt 1, P1 thứ ba; xem `VERDICT.md`):
  - liên kết ở thư mục cha phía trên `daemon`;
  - một tiến trình cùng người dùng tráo thư mục giữa lúc kiểm và lúc xoá.
- Máy mới tinh, chưa có `ms-playwright\b`/`daemon`: suy từ mã thì sẽ còn hai thư mục rỗng dùng chung; chưa đo.
- Ma trận dùng fixture tệp, không có daemon thật. Chỉ các lượt native chạy với CLI và trình duyệt thật.
- Ngoài chữ của spec: thêm cặp đánh dấu `du-luong-daemon-truoc-open` (cho B1) để ma trận trích được bước kiểm trước
  `open`. Đây là đánh dấu bổ sung cùng kiểu B6, không đổi hành vi.
