# WP1389 r1 — kết quả đo (executor: Claude Code, phiên `session_015GtxrazyAyLwN5BiEB52Sq`)

Spec: `ops/specs/wp1389-r1.md` (sha256 `12257fa8…10bc`). Lease: `ops/leases/wp1389-r1-g1-claude.yaml`.
Base `eca1d125b8`. SKILL tại base: blob `678ba2f0`, sha256 `1799c2bd…faadb`.

**Head mã đã đo: `07efca6e9ba23a159d149ab766b39f005cff06f9`** (tree `84f4e5b7…`).
- SKILL: blob `1ea39702`, sha256 `d7954c30772a954da44a5fa50c08713ebc8cd3a001faeb9618c17e1094a0a0be`. Trùng byte từ
  `4d8e9a7`; `2875afc` và `07efca6` chỉ đổi harness PS.
- `residue_matrix.sh` `d1bd9934…`, `residue_matrix.ps1` `99adc9e2…`.
- Commit sau `07efca6` chỉ đổi tệp này, `VERDICT.md`, `REVIEW-PROMPT.md` và lease.

## Lịch sử (rút gọn; chi tiết từng lượt trong git log và `VERDICT.md`)

| head | việc | kết quả |
|---|---|---|
| `045c913` → `783e219` | bản đầu; vá W1, W2 do local Windows bắt | Codex lượt 1 ở `4aae991`: `request_changes` (4 P1, 3 P2, 1 P3) |
| `5c01f39` → `6896f16` | sửa theo lượt 1; vá W3, W4 | Codex lượt 2 ở `f2654b2`: `request_changes` (3 P1, 4 P2, 1 P3) |
| `4d8e9a7` | **thiết kế lại** theo quyết định của chủ kho tại Review Rescue Checkpoint (AskUserQuestion: "Redesign: ask the CLI") | — |
| `2875afc`, `07efca6` | hai lỗi harness PS do local Windows bắt (W5, W6) | đo cuối ở `07efca6` (§2–§5) |

## 0. Thiết kế (vì sao (b), và cách lấy sổ phiên)

- Nguồn ghim (`npm pack`, SRI sha512 khớp lockfile; reviewer kiểm lại độc lập):
  - `registry.js:119-131`: sổ phiên = `PWTEST_DAEMON_SESSION_DIR` (hook test, bị cấm), hoặc
    `XDG_CACHE_HOME||~/.cache` (Linux), `LOCALAPPDATA||~\AppData\Local` (Windows), nối `ms-playwright/daemon`.
  - `:137-148`: thư mục con = `sha1(workspaceDir||packageRoot)[:16]`.
  - `session.js:121-126`: daemon tạo `.err` bằng `openSync(…, "w")`.
  - `session.js:73-97`: `deleteData` không xoá `.err`.
  - README và session-management của gói không có tuỳ chọn dời ⇒ (a) không khả dụng.
- **Từ `4d8e9a7`, skill không tự suy đường dẫn.**
  - Capture hỏi chính mã ghim bằng `node -e`, từ `work` như CLI. Lệnh nạp
    `playwright-core/lib/tools/cli-client/registry.js`, in `baseDaemonDir()` và `createClientInfo().daemonProfilesDir`.
    Chuỗi JS không có dấu nháy, vì đường dẫn mô-đun đi qua `argv`.
  - Capture kiểm kết quả: tuyệt đối, dạng `<base>/<16 hex>`, không liên kết; bash ≥ 4.4. Đạt thì ghi `00-sophien.txt`.
    Lỗi thì in `STOP trước open: phiên CHƯA tạo — KHÔNG chạy Cleanup`, không qua trap ERR.
  - Cleanup hỏi lại **trước `close`** và đòi kết quả trùng `00-sophien.txt`. Như vậy có neo xuất xứ: không có hoặc khác
    bản ghi thì không đóng, không dọn.
  - Bước dọn đòi đúng một mục mang nonce, và mục ấy phải là `<dòng 2>/<nonce>.err`. Thứ tự theo B4: ghi đường dẫn →
    chép → so → xoá.
  - Gỡ bản cài hỏi lại sổ phiên của bản cài bị loại TRƯỚC khi xoá `install`, đối chiếu `00-sophien.txt`, rồi xoá thư mục
    không đệ quy.
- Đo đường thật: lượt N3/N4 dùng `registry.js` THẬT của bản ghim. Ở N3, `00-sophien.txt` dòng 2 bằng đúng
  `sha1("<install>/node_modules/playwright-core")[:16]` (`0804253c76c63b3f`).

## 1. Tái hiện F1 trên Linux tại base

- Môi trường: Node `v24.19.0`, npm `11.9.0`. Khối bash của SKILL được trích nguyên byte, chạy với `env -i`.
- Sau `CLEANUP OK` còn `daemon/3815e4e10d63867a/tl-pw-cedba9810ed1.err`. Tệp này được để nguyên làm "tệp cũ" cho mọi lượt
  sau.

## 2. N1 — ma trận bash (Linux) tại `07efca6`

Lệnh: `bash ops/acceptance/wp1389/residue_matrix.sh <SKILL> <scratch rỗng> <node v24.19.0>`

```
SOURCE d7954c30772a954da44a5fa50c08713ebc8cd3a001faeb9618c17e1094a0a0be pre_frag 78ffaccac4168eb0db9a251ce01a36e875c1efd73801298e8ded24dfb1c1161e dau_frag c7c7579a285723d56f4edef2f738d480d733e67fde897fa08f51f6ab5566da26 cleanup_frag 52328848e4da336eef8c35aa539a728ed6118cc41b943c0ef46e0e79b666fdbd node v24.19.0
TONG: 55 dat / 55        rc=0
```

- Cách trích: lấy nội dung giữa ba cặp đánh dấu, mỗi cặp đúng 2 lần. Dòng `node -e` của SKILL chạy bằng node thật, trên
  một `registry.js` giả do từng ca chỉ định.
- Tệp phải giữ được chụp TRƯỚC khi chạy (tồn tại, loại, sha256, mtime). Mồi được băm nội dung.
  - Mọi ca STOP đều kiểm: không có output `11-*` mới.
  - N8 kiểm thêm output đối ứng phải vắng.
- Cleanup:
  - P1, P2 (`.err` rỗng): qua.
  - Phải dừng:
    - N1 0 mục · N2 hai thư mục hash · N3 `.session` sót · N4 `ud-` sót · N5 `.err` symlink.
    - N6 thư mục hash khác là symlink · N7 sổ phiên symlink · N8 ×2 output cũ · N9 tên hash sai.
    - N10 hook · N11 `.err` là thư mục · N12 chưa có sổ · N14 hậu tố sai · N15 quét lỗi.
    - N16 tên có xuống dòng · N17 sổ tương đối · **N18 `.err` ở thư mục hash của bản cài khác** · **N19 thư mục hash
      của chính bản cài là symlink**.
- Đầu Cleanup (trước `close`):
  - D1 thiếu `00-sophien.txt` ⇒ dừng.
  - D2 CLI trả sổ khác bản ghi (môi trường đổi giữa các bước) ⇒ dừng.
  - D3 CLI ở chế độ workspace ⇒ dừng.
  - D4 trùng ⇒ qua.
- Trước `open`:
  - Qua: C1 sạch · C3 chưa có sổ · C6 độ sâu 1 bị bỏ qua.
  - Phải dừng: C2 nonce có sẵn · C4 tương đối · C5 hook · C7 quét lỗi · C8 workspace · C9 sổ symlink · C10 hash symlink
    · C11 hash sai dạng · C12 hash không nằm dưới sổ · C13 không có node.
  - Mọi ca dừng ở đây đều in `KHÔNG chạy Cleanup`, không có `— chạy Cleanup` từ trap ERR, và không ghi
    `00-sophien.txt`.
- 17 đột biến, mỗi đột biến làm ca đích LỌT:
  - Cleanup: exact-one (thử hai thứ tự tạo tệp) · name-glob · no-symlink-check · daemon-symlink · stale-output ·
    pwtest-hook · exact-path · no-scan-rc · relative-cache · install-dir-binding.
  - Đầu Cleanup: no-capture-record · no-registry-compare.
  - Trước `open`: pre-relative · pre-hook · pre-scan-rc · pre-link · pre-shape.
- Tự kiểm harness: cho SKILL biến thể đổi nội dung mồi rồi trả mtime cũ ⇒ harness rc 1, P1/P2 FAIL.

## 3. N2 — ma trận PowerShell (Desktop, local, ADR-0057) tại `07efca6`

| shell | kết quả | tệp out (sha256) |
|---|---|---|
| PS 5.1 (`5.1.26100`) | **`TONG: 65 dat / 65`**, rc 0 | `0df38f71…` |
| pwsh 7.6.10 | **`TONG: 65 dat / 65`**, rc 0 | `468e3310…` |

- Cả hai shell dùng node `v26.13.0` và in `SOURCE d7954c30… pre_frag 34cce6b8… dau_frag 3b4431a8… cleanup_frag ad52db3e…`.
  Ba băm đoạn trùng byte với cùng đoạn trích trên Linux.
- Các ca giống bản bash, cộng các ca riêng Windows:
  - N13: bản viết hoa của nonce.
  - N15/C7: `icacls /deny (RD)`; kiểm cả mục bị che vẫn nguyên.
  - L1/L2: `FileShare.None` 2 s / 12 s. L2 còn kiểm B4: đường dẫn đã được ghi trước khi chép.
  - L3: `FileShare.Read` 2 s.
- 18 đột biến:
  - 16 đột biến làm ca đích lọt. Trong đó `relative-cache-and-path` gỡ CẢ HAI lớp, vì N17 trong PS bị chặn hai lớp (W6).
  - no-copy-retry làm L1 đỏ; no-delete-retry làm L3 đỏ.
- **KHÔNG ĐO ĐƯỢC: N5** (symlink tệp), vì máy không có quyền tạo; ghi `SKIP`, không tính đạt.

## 4. N3 — Linux native

| head | nonce | thư mục hash (từ CLI) | Setup / Pin / Cleanup | Gỡ |
|---|---|---|---|---|
| `045c913`, `bcc239c`, `783e219`, `5c01f39`, `6896f16` | (xem git log) | (mỗi lượt một thư mục) | OK / OK / OK | `rmdir` thư mục rỗng |
| **`4d8e9a7`** (SKILL trùng byte `07efca6`) | `tl-pw-7b6df2b6198e` | `0804253c76c63b3f` | OK / OK / OK | hỏi CLI: dòng 2 trùng `00-sophien.txt` ⇒ xoá `install`/`browsers` ⇒ `rmdir` |

- Ở cả 6 lượt, ảnh chụp `~/.cache/ms-playwright` (loại, kích thước, sha256, mtime) trước Setup và sau Gỡ **trùng
  byte** (`8c247ab02e544cb8…`). Tệp `.err` cũ còn nguyên.
- Lượt `4d8e9a7`: `SHA256SUMS` có 31 dòng, gồm `00-sophien.txt`.

## 5. N4 — Windows native (Desktop, pwsh 7.6.10, local)

| head | nonce | `daemon\<hash>` | Cleanup | Gỡ | `ms-playwright` trước → sau Gỡ |
|---|---|---|---|---|---|
| `bcc239c`, `783e219`, `6896f16` | (3 lượt) | (mỗi lượt một) | `CLEANUP OK` | đếm rồi `Remove-Item` | **trùng byte** |
| **`07efca6`** | `tl-pw-caf69393a0ce` | `dc4a3fa1ae37afc7` | `CLEANUP OK`, stderr 0 | hỏi CLI: dòng 2 trùng ⇒ xoá `install`/`browsers` ⇒ `[IO.Directory]::Delete(p, $false)` ok | **trùng byte** `a36424f6…` |

- `00-sophien.txt`: `C:\Users\<user>\AppData\Local\ms-playwright\daemon` | `…\daemon\dc4a3fa1ae37afc7`, do `registry.js` thật
  của bản ghim trả về.
- 15 tệp `.err` có từ trước giữ nguyên tên, kích thước, sha256 và mtime: 13 tệp của P2/P3, 2 tệp của #1319.
- Giữa lượt, `<nonce>.err` bị **khoá đọc** (`locked`). Sau Cleanup chỉ còn thư mục hash rỗng; Gỡ xoá thư mục này.
- Phản chứng: gọi `[IO.Directory]::Delete(p, $false)` trên thư mục có tệp ⇒ bị từ chối
  (`MethodInvocationException`), tệp còn nguyên.
- Setup ở lượt này có một lần tải bị **502 từ "Skyhigh Secure Web Gateway"** của mạng máy chủ. Playwright tự thử lại và
  vẫn ra `SETUP OK` (stderr `34da8dcc…`, 6 651 byte). Ghi lại để biết; không phải lỗi của skill.
- Khoá `C:\tl-win\KHOA.txt` và `F:\tl-win\KHOA.txt` (5 trường, ADR-0057/58/59) được giữ trong ba đợt:
  10:05:54Z → ~10:22Z, 10:40:31Z → ~10:49Z, 11:31:04Z → ~11:50Z.
  - Lúc lấy khoá, cả hai tệp đều rỗng.
  - Có tiến trình của phiên khác; đã ghi lại, không đụng tới.
- Đã ghi tổng cộng 12 dòng vào `C:\tl-win\do-luong.csv`.

## 6. Lỗi do local Windows bắt (ADR-0057: lỗi do diff gây ra phải vá trước merge)

| # | head | quan sát | vá ở |
|---|---|---|---|
| W1 | `045c913` | Cleanup PS dừng bằng ngoại lệ thô khi chưa có sổ, không có `STOP`. | `bcc239c` |
| W2 | `bcc239c` | Daemon còn sống thì khoá ĐỌC `.err`. Bước chép không có vòng chờ. | `783e219` |
| W3 | `5c01f39` | **pwsh 7**: `Get-ChildItem -ErrorAction Stop` trên thư mục không liệt kê được trả 0 mục, im lặng. Cleanup vì thế XOÁ `.err` khi lẽ ra phải dừng. Đây là P1 "quét thiếu" của Codex lượt 1, tái hiện trên Windows. | `6896f16`: quét bằng `[IO.Directory]` |
| W4 | `5c01f39` | Harness: biến vòng `$c` chính là `$script:C` (PS không phân biệt hoa thường), nên P2 không thực sự đo. | `6896f16` |
| W5 | `4d8e9a7` | Harness: biến đường dẫn `$DAU` và biến nội dung `$dau` là MỘT biến. Băm `dau_frag` Windows (`76fa593e`) lệch Linux (`3b4431a8`), nên lượt bị huỷ. | `2875afc` |
| W6 | `2875afc` | Đột biến chỉ gỡ chốt tuyệt đối ở N17 không làm ca lọt, vì `FullName` tuyệt đối vẫn không trùng đường dẫn tương đối: chặn hai lớp. Không phải lỗi skill; đột biến được đổi thành gỡ cả hai lớp. | `07efca6` |

Bài học W4/W5: bẫy PowerShell không phân biệt hoa thường đã cắn harness hai lần. Lượt W5 chỉ lộ ra nhờ đối chiếu băm đoạn
trích giữa hai nền.

## 7. Chưa đo được / giới hạn

- N5 trên Windows (symlink tệp): KHÔNG ĐO ĐƯỢC. Chỉ đo một máy Windows; ASUS và VM không chạy.
- Phụ thuộc vào mô-đun NỘI BỘ `lib/tools/cli-client/registry.js` của bản ghim; Limits có khai điều này. Nâng ghim thì
  phải đo lại đường này.
- Bash < 4.4: chốt có trong mã (dừng trước `open`) nhưng không có shell cũ để đo; KHÔNG ĐO ĐƯỢC.
- Giả định cache TIN CẬY và ỔN ĐỊNH; đã khai trong Limits. Liên kết tĩnh ở thư mục cha được chấp nhận. Đổi môi trường
  giữa các bước bị bắt (D2). Không chống được tiến trình cùng người dùng tráo thư mục giữa lúc kiểm và lúc xoá.
- Thời gian thật để daemon nhả handle sau `10-verify` chưa đo. Các lượt N4 không cần thử lại.
- Máy mới tinh, chưa có `ms-playwright\b`/`daemon`: suy từ mã sẽ còn hai thư mục rỗng dùng chung; chưa đo.
- Ngoài chữ của spec: thêm hai cặp đánh dấu (`…-truoc-open`, `…-dau-cleanup`) và tệp `00-sophien.txt`. Đây là các
  chốt B1/B2 làm chặt thêm theo hướng chủ kho đã duyệt, không nới hành vi nào trong spec.
