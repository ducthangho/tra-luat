# WP1389 r1 — kết quả đo (executor: Claude Code, phiên `session_015GtxrazyAyLwN5BiEB52Sq`)

Spec: `ops/specs/wp1389-r1.md` (sha256 `12257fa8…10bc`). Lease: `ops/leases/wp1389-r1-g1-claude.yaml`.
Base `eca1d125b8`. SKILL tại base: blob `678ba2f0`, sha256 `1799c2bd…faadb`.

**Head mã đã đo: `429fb5b0d43b5298734142c8eafafb9a0804c40e`** (tree `f5706c9d…`).
- SKILL: blob `b5f8a237`, sha256 `2dcbb5d4fa8362df603999b299c481ba099a6b3e6e47763cb925d7f48c84e0e5`.
- `residue_matrix.sh` `7606f312…`, `residue_matrix.ps1` `4b6e3aad…`.
- Commit sau `429fb5b` chỉ đổi tệp này, `VERDICT.md`, `REVIEW-PROMPT.md` và lease.

## Lịch sử (rút gọn; chi tiết từng lượt trong git log và `VERDICT.md`)

| head | việc | kết quả |
|---|---|---|
| `045c913` → `783e219` | bản đầu; vá W1, W2 do local Windows bắt | Codex lượt 1 ở `4aae991`: `request_changes` (4 P1, 3 P2, 1 P3) |
| `5c01f39` → `6896f16` | sửa theo lượt 1; vá W3, W4 | Codex lượt 2 ở `f2654b2`: `request_changes` (3 P1, 4 P2, 1 P3) |
| `4d8e9a7` | **thiết kế lại** theo quyết định của chủ kho tại Review Rescue Checkpoint (AskUserQuestion: "Redesign: ask the CLI") | — |
| `2875afc`, `07efca6` | hai lỗi harness PS do local Windows bắt (W5, W6) | Codex lượt 3 ở `86879e1`: `request_changes` (2 P1 + 2 P2 chặn merge; P3 là giới hạn đã khai) |
| **`429fb5b`** | chủ kho nâng trần Codex 3 → 4. Bản vá: neo nonce, kiểm liên kết trước `close`, kênh base64 UTF-8, ma trận TOÀN LUỒNG | **đo cuối** (§2–§5) |

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
    Chuỗi JS không có dấu nháy, vì đường dẫn mô-đun đi qua `argv`. Từ `429fb5b`, lệnh in **base64 của UTF-8** và cả hai
    shell giải mã tường minh, nên code page của console không đổi được đường dẫn.
  - Capture kiểm kết quả: tuyệt đối, dạng `<base>/<16 hex>`, không liên kết; bash ≥ 4.4. Đạt thì ghi `00-sophien.txt`,
    gồm 3 dòng: sổ phiên, thư mục hash và **nonce**.
    Lỗi thì in `STOP trước open: phiên CHƯA tạo — KHÔNG chạy Cleanup`, không qua trap ERR.
  - Cleanup hỏi lại **trước `close`** và đòi trùng cả ba dòng `00-sophien.txt`. Thêm điều kiện: hai thư mục là thư mục
    thường, không có hook, bash ≥ 4.4. Như vậy có neo xuất xứ: không có, khác hoặc nonce lạ thì không đóng, không dọn.
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

## 2. N1 — ma trận bash (Linux) tại `429fb5b`

Lệnh: `bash ops/acceptance/wp1389/residue_matrix.sh <SKILL> <scratch rỗng> <node v24.19.0>`

```
SOURCE 2dcbb5d4fa8362df603999b299c481ba099a6b3e6e47763cb925d7f48c84e0e5 pre_frag 4b8bb645114af21f66422222cab295c1773fda0a25820c3790648f2f99dac488 dau_frag 6b163824fd0e886d4ae1fe921a7a2e65a2912d257c0fd0ab358b9e105d4f5640 cleanup_frag 52328848e4da336eef8c35aa539a728ed6118cc41b943c0ef46e0e79b666fdbd node v24.19.0
TONG: 66 dat / 66        rc=0
```

- Đoạn trích: ba cặp đánh dấu, mỗi cặp đúng 2 lần. Dòng `node -e` của SKILL chạy bằng node thật, trên một `registry.js`
  giả do từng ca chỉ định.
- Tệp phải giữ được chụp TRƯỚC khi chạy. Ca STOP không được sinh output `11-*` mới.
- Cleanup:
  - Qua: P1, P2.
  - Phải dừng: N1–N12, N14–N19 (N18: `.err` nằm ở thư mục hash của bản cài khác; N19: thư mục hash của chính bản cài là
    symlink).
- Đầu Cleanup (trước `close`):
  - Phải dừng: D1 thiếu bản ghi · D2 CLI trả sổ khác · D3 workspace · **D5 sổ phiên là link** · **D6 thư mục hash là
    link** · **D7 bản ghi mang nonce khác** · **D8 hook**.
  - Qua: D4.
- Trước `open`: C1–C13; mọi ca dừng in `KHÔNG chạy Cleanup`, không ghi `00-sophien.txt`.
- **TOÀN LUỒNG**: chạy chính khối bash Capture (khối 3) và Cleanup (khối 5) của SKILL, với một CLI giả ghi nhật ký và giữ
  trạng thái. Định dạng phản hồi JSON của CLI giả trùng mẫu so byte của Cleanup.
  - E1 đường đúng: nhật ký đúng thứ tự `open goto tab-list requests close delete-data tab-list`; dư lượng đã dọn; hash gồm
    cả `00`/`11`.
  - **E2** run A nhưng nonce của phiên B đang mở cùng bản cài: KHÔNG gọi `close`/`delete-data`; phiên B nguyên vẹn.
  - **E3** thư mục hash bị thay bằng symlink giữa Capture và Cleanup: KHÔNG gọi `close`; đích nguyên vẹn.
  - **E4** kiểm trước `open` dừng: KHÔNG gọi `open`, không có `00-sophien.txt`, và Cleanup không gọi `close`.
- 20 đột biến (đếm `PASS MUT` trong log), mỗi đột biến làm ca đích lọt hoặc đỏ:
  - 17 đột biến cũ, cộng no-nonce-binding→D7 và dau-link→D5.
  - **dau-after-close**: đưa đoạn đầu-Cleanup ra SAU `10-verify` ⇒ E2 gọi `close` VÀ `delete-data` trên phiên B. Đột biến
    này cho thấy vị trí của chốt là thứ bảo vệ.
- Tự kiểm harness: cho SKILL biến thể đổi nội dung mồi rồi trả mtime cũ ⇒ harness rc 1.

## 3. N2 — ma trận PowerShell (Desktop, local, ADR-0057) tại `429fb5b`

| shell | kết quả | tệp out (sha256) |
|---|---|---|
| PS 5.1 (`5.1.26100`) | **`TONG: 80 dat / 80`**, rc 0 | `01fedecb…` |
| pwsh 7.6.10 | **`TONG: 80 dat / 80`**, rc 0 | `62ad0350…` |

- Cả hai shell chạy node `v26.13.0`, in `SOURCE 2dcbb5d4… pre_frag 78ce992d… dau_frag a86ff384… cleanup_frag ad52db3e…`.
  Ba băm này trùng byte với cùng đoạn trích trên Linux.
- Ca giống bản bash, thêm các ca riêng Windows:
  - N13 biến thể viết hoa.
  - N15/C7 `icacls /deny`.
  - L1–L3 khoá tệp.
  - D5/D6 bằng junction.
  - **U1**: cache có dấu cách và ký tự Unicode (`cache ộê`). Kiểm trước `open` ghi đúng bản ghi; nonce có sẵn ⇒ dừng;
    dọn đúng.
  - **TOÀN LUỒNG E1–E4** chạy chính khối PowerShell Capture/Cleanup của SKILL qua `Invoke-PwGhi`, với cùng CLI giả.
- 22 đột biến PS; mỗi đột biến làm ca đích lọt hoặc đỏ. Có thêm:
  - utf8-decode→U1: đổi giải mã sang ASCII làm U1 đỏ.
  - dau-after-close→E2.
- **KHÔNG ĐO ĐƯỢC: N5** (symlink tệp) vì máy không có quyền tạo; ghi `SKIP`.

## 4. N3 — Linux native

| head | nonce | thư mục hash (từ CLI) | Setup / Pin / Cleanup | Gỡ |
|---|---|---|---|---|
| `045c913` … `6896f16` | (5 lượt, xem git log) | (mỗi lượt một) | OK / OK / OK | `rmdir` thư mục rỗng |
| `4d8e9a7` | `tl-pw-7b6df2b6198e` | `0804253c76c63b3f` | OK / OK / OK | hỏi CLI ⇒ trùng ⇒ `rmdir` |
| **`429fb5b`** | `tl-pw-f9a312651e84` | `56408881502008d7` | OK / OK / OK; `00-sophien.txt` có 3 dòng gồm nonce | hỏi CLI (base64): trùng, thư mục thường ⇒ xoá `install`/`browsers` ⇒ `rmdir` |

- Ở cả 7 lượt, ảnh chụp `~/.cache/ms-playwright` trước Setup và sau Gỡ **trùng byte** (`8c247ab02e544cb8…`).

## 5. N4 — Windows native (Desktop, pwsh 7.6.10, local)

| head | nonce | `daemon\<hash>` | Cleanup | Gỡ | `ms-playwright` trước → sau Gỡ |
|---|---|---|---|---|---|
| `bcc239c`, `783e219`, `6896f16` | (3 lượt) | (mỗi lượt một) | `CLEANUP OK` | đếm rồi `Remove-Item` | **trùng byte** |
| `07efca6` | `tl-pw-caf69393a0ce` | `dc4a3fa1ae37afc7` | `CLEANUP OK` | hỏi CLI ⇒ `[IO.Directory]::Delete(p, $false)` | **trùng byte** |
| **`429fb5b`** | `tl-pw-81711a4330cf` | `06605341ebe36b2d` | `CLEANUP OK`, stderr 0 | hỏi CLI (base64): trùng, thư mục thường ⇒ xoá `install`/`browsers` ⇒ `[IO.Directory]::Delete(p, $false)` | **trùng byte** `a36424f6…` |

- `00-sophien.txt`: `…\ms-playwright\daemon` | `…\daemon\06605341ebe36b2d` | `tl-pw-81711a4330cf`, do `registry.js` thật
  trả về.
- 15 tệp `.err` có từ trước giữ nguyên tên, kích thước, sha256 và mtime.
- Giữa lượt, `<nonce>.err` bị khoá đọc (`locked`). Sau Cleanup chỉ còn thư mục hash rỗng; Gỡ xoá nó.
- Phản chứng ở `07efca6`: `[IO.Directory]::Delete(p, $false)` trên thư mục có tệp ⇒ bị từ chối, tệp còn nguyên.
- Ở `07efca6` có một lần tải bị **502 từ "Skyhigh Secure Web Gateway"**. Playwright tự thử lại và vẫn `SETUP OK`; đây
  không phải lỗi skill. Lượt `429fb5b` không gặp lại (stderr 209 byte, chỉ `npm notice`).
- Khoá `C:\tl-win\KHOA.txt` và `F:\tl-win\KHOA.txt` (ADR-0057/58/59) được giữ trong bốn đợt; lúc lấy, cả hai đều rỗng.
  Đợt cuối: 12:03:30Z → nhả ~12:07Z.
  - Có tiến trình của phiên khác; đã ghi lại, không đụng tới.
- Tổng cộng đã ghi 15 dòng vào `C:\tl-win\do-luong.csv`.

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
  phải đo lại đường này. Codex lượt 3 xếp điều này là giới hạn đã khai, không chặn merge.
- Bash < 4.4: chốt có trong mã (dừng trước `open`) nhưng không có shell cũ để đo; KHÔNG ĐO ĐƯỢC.
- Giả định cache TIN CẬY và ỔN ĐỊNH; đã khai trong Limits. Liên kết tĩnh ở thư mục cha được chấp nhận.
  - Bị bắt: đổi môi trường giữa các bước (D2); đổi sổ phiên hoặc thư mục hash thành liên kết giữa các bước (D5, D6, E3).
  - Không chống được: tiến trình cùng người dùng tráo thư mục giữa lúc kiểm và lúc xoá.
  - Codex lượt 3 xếp đây là giới hạn đã khai.
- Thời gian thật để daemon nhả handle sau `10-verify` chưa đo. Các lượt N4 không cần thử lại.
- Máy mới tinh, chưa có `ms-playwright\b`/`daemon`: suy từ mã sẽ còn hai thư mục rỗng dùng chung; chưa đo.
- Ngoài chữ của spec: thêm hai cặp đánh dấu (`…-truoc-open`, `…-dau-cleanup`) và tệp `00-sophien.txt` (3 dòng). Đây là
  các chốt B1/B2 làm chặt thêm theo hướng chủ kho đã duyệt, không nới hành vi nào trong spec.
- Harness kiểm ca DỪNG bằng sự có mặt của `STOP`, chưa khớp ĐÚNG lý do dừng cho từng ca. Lý do của các chốt quan trọng
  được khẳng định bằng đột biến; N17, E2–E4 được kiểm lý do bằng tay. Một ca có thể dừng vì lý do khác mà vẫn xanh. Đây
  là chỗ yếu đã biết của ma trận.
