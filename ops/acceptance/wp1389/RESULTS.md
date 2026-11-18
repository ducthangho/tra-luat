# WP1389 r1 — kết quả đo (executor: Claude Code, phiên `session_015GtxrazyAyLwN5BiEB52Sq`)

Spec: `ops/specs/wp1389-r1.md` (sha256 `12257fa8…10bc`). Lease: `ops/leases/wp1389-r1-g1-claude.yaml`.
Base `eca1d125b8`. SKILL tại base: blob `678ba2f0`, sha256 `1799c2bd…faadb`.

**Head mã đã đo (lượt 8): `511cf5f11e2179791f4ca988972efc6647e61aac`** (tree `38d0d484…`).
- SKILL: sha256 `5b965c597b07e2357fed072018edc8b8a5e7b608303405be81a1a8c649945879`.
- `residue_matrix.sh` `7fb35acb…`, `residue_matrix.ps1` `5b6ebe43…` (không đổi từ lượt 7).
- Số đo các lượt trước (lượt 5 `d7960ee`, 6 `1d7b9f4`, 7 `8be8070`) giữ nguyên ở §2–§5, §9, §10 để đối chiếu.
- Commit sau head này chỉ đổi tệp này, `REVIEW-PROMPT.md`, `VERDICT.md` và lease. **Chủ kho chấp nhận** (AskUserQuestion
  18-11-2026 ~14:05Z, ghi ở lease `exact_head_chap_nhan`) dùng phép đo N1–N4 trên head mã đã đo cho head cuối khi
  `git diff --exit-code 511cf5f <head> -- .agents ops/acceptance/wp1389/residue_matrix.sh ops/acceptance/wp1389/residue_matrix.ps1`
  trả 0 (lượt 5 áp với `d7960ee`, lượt 6 với `1d7b9f4`, lượt 7 với `8be8070`). Đây là quyết định của chủ kho cho finding P2 "exact H" của Codex lượt 4, không phải phép đo trên head cuối.

## Lịch sử (rút gọn; chi tiết từng lượt trong git log và `VERDICT.md`)

| head | việc | kết quả |
|---|---|---|
| `045c913` → `783e219` | bản đầu; vá W1, W2 do local Windows bắt | Codex lượt 1 ở `4aae991`: `request_changes` (4 P1, 3 P2, 1 P3) |
| `5c01f39` → `6896f16` | sửa theo lượt 1; vá W3, W4 | Codex lượt 2 ở `f2654b2`: `request_changes` (3 P1, 4 P2, 1 P3) |
| `4d8e9a7` | **thiết kế lại** theo quyết định của chủ kho tại Review Rescue Checkpoint (AskUserQuestion: "Redesign: ask the CLI") | — |
| `2875afc`, `07efca6` | hai lỗi harness PS do local Windows bắt (W5, W6) | Codex lượt 3 ở `86879e1`: `request_changes` (2 P1 + 2 P2 chặn merge; P3 là giới hạn đã khai) |
| `429fb5b` | chủ kho nâng trần Codex 3 → 4. Bản vá: neo nonce, kiểm liên kết trước `close`, kênh base64 UTF-8, ma trận TOÀN LUỒNG | Codex lượt 4 ở `999f5fc`: `request_changes` (1 P1 + 4 P2 chặn merge) |
| `ff34b2c` | sửa theo lượt 4 (§8) | local Windows bắt một lỗi đột biến PS (W7) |
| `d7960ee` | vá W7 | đo lượt 5 (§2–§5, §8). Codex lượt 5 ở `376e9c2` (mã trùng byte): `request_changes` (1 P1 + 2 P2 chặn merge) |
| `1d7b9f4` | chủ kho nâng trần Codex 5 → 6; sửa theo lượt 5 (§9) | đo lượt 6 (§9). Codex lượt 6 ở `d0d4879` (mã trùng byte): `request_changes` (1 P1 + 2 P2 chặn merge) |
| `8be8070` | chủ kho nâng trần Codex 6 → 7; sửa theo lượt 6 (§10) | đo lượt 7 (§10). Codex lượt 7 ở `3c524fc` (mã trùng byte): `request_changes` — 3 chốt lượt 6 **đã sửa**; 1 P1 MỚI (cache Linux casefold, lỗi có sẵn từ thiết kế preflight, chưa ai chạy) |
| **`511cf5f`** | chủ kho nâng trần Codex 7 → 8; sửa P1 lượt 7 (§11) | **đo cuối** (§11). **Codex lượt 8 ở `277db46` (mã trùng byte): `approve`**, không P0–P2; 1 P3 không chặn (C20 chưa chụp byte descriptor) |

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
  - Capture kiểm kết quả: tuyệt đối, dạng `<base>/<16 hex>`, KHÔNG thành phần nào của đường dẫn là liên kết (từ
    `ff34b2c`); bash ≥ 4.4. Đạt thì tạo mới (không ghi đè) `00-sophien.txt`, gồm 3 dòng: sổ phiên, thư mục hash và
    **nonce**.
    Lỗi thì in `STOP trước open: phiên CHƯA tạo — KHÔNG chạy Cleanup`, không qua trap ERR.
  - Cleanup hỏi lại **trước `close`** và đòi trùng cả ba dòng `00-sophien.txt`. Thêm điều kiện: hai thư mục là thư mục
    thường, không có hook, bash ≥ 4.4. Như vậy có neo xuất xứ: không có, khác hoặc nonce lạ thì không đóng, không dọn.
  - Bước dọn đòi đúng một mục mang nonce, và mục ấy phải là `<dòng 2>/<nonce>.err`. Thứ tự theo B4: ghi đường dẫn →
    chép → so → xoá.
  - Gỡ bản cài (khối mã từ `ff34b2c`) lấy thư mục từ `11-daemon-path.txt` của run (B7), đòi nó bằng
    `<dòng 2 của 00>/<nonce>.err` và câu trả lời CLI hỏi TRƯỚC khi xoá `install`, không liên kết; xoá không đệ quy.
- Đo đường thật: lượt N3/N4 dùng `registry.js` THẬT của bản ghim. Ở N3, `00-sophien.txt` dòng 2 bằng đúng
  `sha1("<install>/node_modules/playwright-core")[:16]` (`0804253c76c63b3f`).

## 1. Tái hiện F1 trên Linux tại base

- Môi trường: Node `v24.19.0`, npm `11.9.0`. Khối bash của SKILL được trích nguyên byte, chạy với `env -i`.
- Sau `CLEANUP OK` còn `daemon/3815e4e10d63867a/tl-pw-cedba9810ed1.err`. Tệp này được để nguyên làm "tệp cũ" cho mọi lượt
  sau.

## 2. N1 — ma trận bash (Linux) tại `d7960ee`

Lệnh: `bash ops/acceptance/wp1389/residue_matrix.sh <SKILL> <scratch rỗng> <node v24.19.0>`, chạy trên `git archive d7960ee`.

```
SOURCE 75e9be5ff358476de7405008955bf898f9186a02d34e1616c50e079f6826c94c pre_frag 972cff1823a754c92a63887429e71a90ae5233a6867c8eefbdb9fd4de31f1ffc dau_frag 385efe408f5d9c3eae8f7ffef8194b0c620d171229d749a5b2940694b618f938 cleanup_frag 29d8183b49ff76fca502885c7578299c531a26cfe87954f0cff16f0ce057bae8 go_frag 418a97a2aa1b0fc28fc30b372a7e7cd27166f4bbff2a9c5791b65699b5e51416 node v24.19.0
TONG: 99 dat / 99        rc=0
```

- Đoạn trích: năm cặp đánh dấu (thêm `…-go-truoc`, `…-go-sau` của bước Gỡ), mỗi cặp đúng 2 lần. Dòng `node -e` của SKILL
  chạy bằng node thật, trên một `registry.js` giả do từng ca chỉ định.
- Tệp phải giữ được chụp TRƯỚC khi chạy. Ca STOP không được sinh output `11-*` mới (trừ ca lỗi sau bước ghi đường dẫn).
- Cleanup:
  - Qua: P1, P2.
  - Phải dừng: N1–N12, N14–N19; **N20** thư mục tổ tiên (`ms-playwright`) là symlink, cả qua đoạn đầu lẫn chỉ đoạn dọn
    (N20R); **N21** `cp` lỗi, **N22** `cmp` lỗi, **N23** `rm` lỗi (tệp gốc còn nguyên); **N24** ghi `11-daemon-path.txt`
    lỗi (hàm `printf` hỏng tiêm qua `BASH_FUNC_printf%%`) ⇒ chưa chép, chưa xoá.
- Đầu Cleanup (trước `close`): phải dừng D1–D3, D5–D8, **D9** tổ tiên là symlink; qua D4.
- Trước `open`: C1–C13; **C14** tổ tiên là symlink ⇒ dừng; **C15** `00-sophien.txt` đã có ⇒ dừng, tệp cũ KHÔNG bị ghi đè.
- **Gỡ** (khối mã mới): G1 thư mục hash rỗng, 11/00/CLI khớp ⇒ xoá. Giữ nguyên, có biên nhận `GIỮ`: G2 thiếu
  `11-daemon-path.txt`, G3 `11` trỏ thư mục khác, G4 thư mục còn mục (`rmdir` từ chối), G5 tổ tiên là symlink, G6 `00`
  khác, G7 CLI trả khác.
- **TOÀN LUỒNG** (khối bash Capture 3 + Cleanup 5 của SKILL, CLI giả có nhật ký và trạng thái). CLI giả mô phỏng
  `session.js`: `close` xoá descriptor, `delete-data` trả `deleted` = descriptor CÓ tồn tại.
  - E1: nhật ký đúng `open goto tab-list requests close delete-data tab-list`; `deleted: false`; `11-daemon-path.txt` đúng;
    `SHA256SUMS` có dòng và băm KHỚP tệp thật cho `00-sophien.txt`, `11-daemon.err`, `11-daemon-path.txt`,
    `09-delete-data.json`; tệp cũ nguyên.
  - **E6**: descriptor còn sót sau `close` ⇒ `deleted: true`; Cleanup vẫn đạt với cùng các khẳng định E1.
  - E2: nhật ký ĐÚNG BẰNG `open goto tab-list requests open <B>`; byte `.err`/`.session` của B nguyên; trạng thái B vẫn
    `open`; không có output 08–11.
  - E3 (thư mục hash bị thay bằng symlink giữa hai bước) và **E5** (thư mục tổ tiên bị thay bằng symlink giữa hai bước):
    nhật ký chỉ có Capture; byte phiên ở đích nguyên; không output 08–11.
  - E4 dừng trước `open`. **E7** `open` lỗi trước khi daemon tạo gì ⇒ Cleanup dừng trước `close`, không xoá gì. **E8**
    `open` lỗi SAU khi daemon tạo `.err` ⇒ Cleanup gọi `close` cho nonce của chính nó, phản hồi sai ⇒ STOP, `.err` GIỮ.
- 33 đột biến (đếm `PASS MUT`), mỗi đột biến làm ca đích lọt hoặc đỏ. Mới ở lượt này: residue-ancestor→N20,
  no-cmp→N22, no-rm-check→N23, no-write-check→N24, dau-ancestor→D9, pre-ancestor→C14, pre-noclobber→C15, go-no-receipt→G2,
  go-receipt-parent→G3, go-link→G5, go-record→G6, **only-false→E6** (bỏ nhánh `deleted: true`), **hash-early→E1** (dọn sau
  khi băm). Chốt `realpath` cũng bắt đường dẫn tương đối, nên đột biến relative-cache/pre-relative gỡ CẢ HAI lớp.
- Không có đột biến riêng: kiểm `cp` (lỗi chép đã bị `cmp` bắt, hai lớp).

## 3. N2 — ma trận PowerShell (Desktop, local, ADR-0057) tại `d7960ee`

| shell | kết quả | tệp out (sha256) |
|---|---|---|
| PS 5.1 (`5.1.26100`) | **`TONG: 110 dat / 110`** (bỏ qua 3), rc 0 | `4f0f2fed…` |
| pwsh 7.6.10 | **`TONG: 110 dat / 110`** (bỏ qua 3), rc 0 | `375cdbe1…` |

- Cả hai shell chạy node `v26.13.0`, in `SOURCE 75e9be5f… pre_frag 34746a0a… dau_frag e8f8d307… cleanup_frag 6124a30b…
  go_frag 5a114c16…`. Bốn băm đoạn trích PS này tính lại trên Linux từ cùng SKILL ra trùng.
- Ca giống bản bash, cộng các ca riêng Windows: N13 biến thể viết hoa; N15/C7 `icacls /deny`; L1–L3 khoá tệp; **L4** khoá
  xoá 12 s ⇒ STOP, bản sao đã chép trùng byte, gốc còn; **W1** thư mục run cấm ghi ⇒ không chép, không xoá; junction cho
  D5/D6/N6/N7/N19 và tổ tiên (N20, N20R, D9, C14, E5, G5); U1 Unicode; TOÀN LUỒNG E1–E8 qua `Invoke-PwGhi` của SKILL,
  với E1/E6 đọc `SHA256SUMS.csv` và so băm từng tệp.
- 33 đột biến PS mỗi shell (đếm `PASS MUT`).
- **KHÔNG ĐO ĐƯỢC** (máy không có quyền tạo symlink TỆP, ghi `SKIP`): N5, **D10** (`00-sophien.txt` là symlink tới bản ghi
  của run khác) và đột biến record-reparse→D10. Chốt reparse của bản ghi vì thế chỉ được đọc mã, chưa đo trên Windows.

## 4. N3 — Linux native

| head | nonce | thư mục hash (từ CLI) | Setup / Pin / Cleanup | Gỡ |
|---|---|---|---|---|
| `045c913` … `6896f16` | (5 lượt, xem git log) | (mỗi lượt một) | OK / OK / OK | `rmdir` thư mục rỗng |
| `4d8e9a7` | `tl-pw-7b6df2b6198e` | `0804253c76c63b3f` | OK / OK / OK | hỏi CLI ⇒ trùng ⇒ `rmdir` |
| `429fb5b` | `tl-pw-f9a312651e84` | `56408881502008d7` | OK / OK / OK; `00-sophien.txt` có 3 dòng gồm nonce | hỏi CLI (base64): trùng, thư mục thường ⇒ xoá `install`/`browsers` ⇒ `rmdir` |
| **`ff34b2c`** (SKILL trùng byte `d7960ee`) | `tl-pw-4328fdb0c7a7` | `0b62672472ad0641` | OK / OK / OK; `deleted: false`; `11-daemon.err` 0 byte | **chính khối Gỡ của SKILL**: `GO_DH` = thư mục hash ⇒ xoá `install`/`browsers` ⇒ `rmdir`; `con_ton_tai=khong` |

- Ở cả 8 lượt, ảnh chụp `~/.cache/ms-playwright` trước Setup và sau Gỡ **trùng byte** (`8c247ab02e544cb8…`). Lượt
  `ff34b2c`: sau Cleanup, mọi mục ngoài thư mục hash của lượt này trùng ảnh chụp trước Setup.

## 5. N4 — Windows native (Desktop, pwsh 7.6.10, local)

| head | nonce | `daemon\<hash>` | Cleanup | Gỡ | `ms-playwright` trước → sau Gỡ |
|---|---|---|---|---|---|
| `bcc239c`, `783e219`, `6896f16` | (3 lượt) | (mỗi lượt một) | `CLEANUP OK` | đếm rồi `Remove-Item` | **trùng byte** |
| `07efca6` | `tl-pw-caf69393a0ce` | `dc4a3fa1ae37afc7` | `CLEANUP OK` | hỏi CLI ⇒ `[IO.Directory]::Delete(p, $false)` | **trùng byte** |
| `429fb5b` | `tl-pw-81711a4330cf` | `06605341ebe36b2d` | `CLEANUP OK`, stderr 0 | hỏi CLI (base64): trùng, thư mục thường ⇒ xoá `install`/`browsers` ⇒ `[IO.Directory]::Delete(p, $false)` | **trùng byte** `a36424f6…` |
| **`d7960ee`** | `tl-pw-8ad25bd9fbde` | `3809d38db5c43001` | `CLEANUP OK`, stderr 0; `deleted: false`; `11-daemon.err` 0 byte; `SHA256SUMS.csv` 31 dòng | **chính khối Gỡ của SKILL** (`C-uninstall.ps1` sinh từ khối 6): `GODH=[…\3809d38db5c43001]`, `exists_after=False` | **trùng byte** `a36424f6…` |

- Lượt `d7960ee`: `00-sophien.txt` = `…\ms-playwright\daemon` | `…\daemon\3809d38db5c43001` | `tl-pw-8ad25bd9fbde`, do
  `registry.js` thật trả về; chốt dò tổ tiên chạy trên đường dẫn thật `C:\Users\…\AppData\Local\…` và cho qua. Tệp
  out: Cleanup `3f4f56fc…`, Gỡ `36749f86…`. Setup lại gặp 502 từ cổng web và Playwright tự thử lại (`SETUP OK`).
- 15 tệp `.err` có từ trước giữ nguyên tên, kích thước, sha256 và mtime.
- Giữa lượt, `<nonce>.err` bị khoá đọc (`locked`). Sau Cleanup chỉ còn thư mục hash rỗng; Gỡ xoá nó.
- Phản chứng ở `07efca6`: `[IO.Directory]::Delete(p, $false)` trên thư mục có tệp ⇒ bị từ chối, tệp còn nguyên.
- Ở `07efca6` có một lần tải bị **502 từ "Skyhigh Secure Web Gateway"**. Playwright tự thử lại và vẫn `SETUP OK`; đây
  không phải lỗi skill. Lượt `429fb5b` không gặp lại (stderr 209 byte, chỉ `npm notice`).
- Khoá `C:\tl-win\KHOA.txt` và `F:\tl-win\KHOA.txt` (ADR-0057/58/59) được giữ trong bốn đợt; lúc lấy, cả hai đều rỗng.
  Đợt cuối: 12:03:30Z → nhả ~12:07Z.
  - Có tiến trình của phiên khác; đã ghi lại, không đụng tới.
- Lượt 5: khoá lấy 13:09:40Z (cả hai rỗng), nhịp tim 13:40:45Z, nhả ~13:48Z (0 byte). Tổng cộng đã ghi 20 dòng vào
  `C:\tl-win\do-luong.csv`.

## 6. Lỗi do local Windows bắt (ADR-0057: lỗi do diff gây ra phải vá trước merge)

| # | head | quan sát | vá ở |
|---|---|---|---|
| W1 | `045c913` | Cleanup PS dừng bằng ngoại lệ thô khi chưa có sổ, không có `STOP`. | `bcc239c` |
| W2 | `bcc239c` | Daemon còn sống thì khoá ĐỌC `.err`. Bước chép không có vòng chờ. | `783e219` |
| W3 | `5c01f39` | **pwsh 7**: `Get-ChildItem -ErrorAction Stop` trên thư mục không liệt kê được trả 0 mục, im lặng. Cleanup vì thế XOÁ `.err` khi lẽ ra phải dừng. Đây là P1 "quét thiếu" của Codex lượt 1, tái hiện trên Windows. | `6896f16`: quét bằng `[IO.Directory]` |
| W4 | `5c01f39` | Harness: biến vòng `$c` chính là `$script:C` (PS không phân biệt hoa thường), nên P2 không thực sự đo. | `6896f16` |
| W5 | `4d8e9a7` | Harness: biến đường dẫn `$DAU` và biến nội dung `$dau` là MỘT biến. Băm `dau_frag` Windows (`76fa593e`) lệch Linux (`3b4431a8`), nên lượt bị huỷ. | `2875afc` |
| W7 | `ff34b2c` | Đột biến PS no-capture-record (`… -and` ⇒ `$true -or`) không còn lọt: chốt reparse mới của bản ghi đứng sau một `-and`, nên `-or` không ngắt được phần đọc tệp, và đột biến ném lỗi đọc thay vì lọt. Cả 5.1 lẫn 7: 109/110. Ca D1 thật vẫn STOP; lỗi ở đột biến. | `d7960ee`: đột biến gỡ cả cụm chốt bản ghi |
| W6 | `2875afc` | Đột biến chỉ gỡ chốt tuyệt đối ở N17 không làm ca lọt, vì `FullName` tuyệt đối vẫn không trùng đường dẫn tương đối: chặn hai lớp. Không phải lỗi skill; đột biến được đổi thành gỡ cả hai lớp. | `07efca6` |

Bài học W4/W5: bẫy PowerShell không phân biệt hoa thường đã cắn harness hai lần. Lượt W5 chỉ lộ ra nhờ đối chiếu băm đoạn
trích giữa hai nền.

## 7. Chưa đo được / giới hạn

- N5, D10 trên Windows (symlink tệp): KHÔNG ĐO ĐƯỢC. Chỉ đo một máy Windows; ASUS và VM không chạy.
- Phụ thuộc vào mô-đun NỘI BỘ `lib/tools/cli-client/registry.js` của bản ghim; Limits có khai điều này. Nâng ghim thì
  phải đo lại đường này. Codex lượt 3 xếp điều này là giới hạn đã khai, không chặn merge.
- Bash < 4.4: chốt có trong mã (dừng trước `open`) nhưng không có shell cũ để đo; KHÔNG ĐO ĐƯỢC.
- Từ `ff34b2c`, liên kết ở BẤT KỲ thành phần nào của đường dẫn tới thư mục hash ⇒ DỪNG (trước `open`, trước `close`,
  bước dọn, Gỡ). Liên kết tĩnh ở thư mục cha KHÔNG còn được chấp nhận; cache Linux sau symlink phải đặt `XDG_CACHE_HOME`
  về đường dẫn vật lý (Limits).
  - Bị bắt: đổi môi trường giữa các bước (D2); đổi sổ phiên, thư mục hash hoặc thư mục tổ tiên thành liên kết giữa các
    bước (D5, D6, D9, E3, E5).
  - Không chống được (Limits): tiến trình cùng người dùng tráo thư mục, hoặc thay `00-sophien.txt` bằng hard link, giữa lúc
    kiểm và lúc thao tác.
- E8: `open` lỗi sau khi daemon đã tạo `.err` ⇒ Cleanup dừng ở `close` và `.err` ở lại (không xoá gì khi chưa chứng minh
  đóng đúng phiên). Đây là hành vi "lỗi ⇒ không dọn" của B5, không phải dư lượng mới của đường thành công.
- Thời gian thật để daemon nhả handle sau `10-verify` chưa đo. Các lượt N4 không cần thử lại.
- Máy mới tinh, chưa có `ms-playwright\b`/`daemon`: suy từ mã sẽ còn hai thư mục rỗng dùng chung; chưa đo.
- Ngoài chữ của spec: thêm hai cặp đánh dấu (`…-truoc-open`, `…-dau-cleanup`) và tệp `00-sophien.txt` (3 dòng). Đây là
  các chốt B1/B2 làm chặt thêm theo hướng chủ kho đã duyệt, không nới hành vi nào trong spec.
- Harness kiểm ca DỪNG bằng sự có mặt của `STOP`, chưa khớp ĐÚNG lý do dừng cho từng ca. Lý do của các chốt quan trọng
  được khẳng định bằng đột biến; N17, E2–E4 được kiểm lý do bằng tay. Một ca có thể dừng vì lý do khác mà vẫn xanh. Đây
  là chỗ yếu đã biết của ma trận.

## 8. Lượt 5 — sửa theo Codex lượt 4

| finding lượt 4 | sửa ở SKILL | ca đo |
|---|---|---|
| P1 liên kết cha đổi đích giữa hai bước | bash `[ "$(realpath -m/-e -- "$DH")" = "$DH" ]`; PS dò `Split-Path -Parent` tới gốc, từ chối ReparsePoint. Ở trước `open`, đầu Cleanup, bước dọn, Gỡ. Thay cho các chốt `-L`/reparse riêng lẻ. | C14, D9, N20, N20R, E5, G5 (+ đột biến) |
| P2 PS nhận bản ghi qua reparse point | kiểm thuộc tính `00-sophien.txt` trước khi đọc; tạo bản ghi bằng `FileMode.CreateNew` (PS) / `set -C` (bash) | D10 (Windows: KHÔNG ĐO ĐƯỢC), C15 |
| P2 Gỡ dùng bản ghi Capture thay cho biên nhận Cleanup (B7) | khối mã Gỡ (1)/(2): thư mục từ `11-daemon-path.txt`, phải bằng `<dòng 2 của 00>/<nonce>.err` và câu trả lời CLI; không liên kết; xoá không đệ quy | G1–G7 (+ đột biến), N3, N4 |
| P2 ma trận toàn luồng chưa chứng minh hết | CLI giả `deleted` = descriptor tồn tại; E1/E6 so băm; E2/E3 nhật ký chính xác + byte; lỗi ghi/chép/so/xoá; đột biến only-false, hash-early | E1–E8, N21–N24, L4, W1 |
| P2 N2–N4 chưa có trên exact H | đo lại N1–N4 trên `d7960ee` (N3 trên `ff34b2c`, SKILL trùng byte) | §2–§5 |

## 9. Lượt 6 — sửa theo Codex lượt 5, đo trên `1d7b9f4`

| finding lượt 5 | sửa ở SKILL | ca đo (+ đột biến) |
|---|---|---|
| P1 `$(…)` cắt MỌI LF cuối ⇒ symlink tới thư mục tên chỉ khác ở LF cuối qua phép so `realpath` | cả 4 phép so: `[ "$(realpath … -- "$DH"; echo .)" = "$DH"$'\n.' ]` | C18 (trước `open`, tệp ở đích không đổi), D11 (đầu Cleanup), N25, G8; đột biến pre-lf→C18, dau-lf→D11 |
| P2 Gỡ đọc biên nhận qua liên kết | `00`/`11` phải là tệp thường không liên kết TRƯỚC khi đọc; cấm hook; `00` trùng NGUYÊN câu trả lời CLI + nonce | G9–G12 bash (+ go-receipt-link, go-record-link, go-hook, go-record-line1); PS G11, G12 (+ đột biến); PS G9/G10 KHÔNG ĐO ĐƯỢC (symlink tệp) |
| P2 `set -C` vẫn mở FIFO | từ chối mọi mục có sẵn trước khi tạo | C16 FIFO ⇒ dừng ngay, FIFO nguyên; C17 symlink treo; đột biến pre-fifo ⇒ Capture TREO (`timeout` 124) |

| phép đo | kết quả |
|---|---|
| N1 bash (Linux, node v24.19.0) | `TONG: 116 dat / 116`, 40 đột biến; `SOURCE a435d082… pre_frag 5dd27467… dau_frag 7c01d316…` |
| N2 PS 5.1 | `TONG: 114 dat / 114 (bỏ qua 6)`, out `87ffd7d4…` |
| N2 pwsh 7.6.10 | `TONG: 114 dat / 114 (bỏ qua 6)`, out `dfe05ce5…` |
| N3 Linux native | `tl-pw-ca46b0664823`, hash `06b465beb0a36c28`: Setup/Pin/Cleanup OK, `deleted: false`; khối Gỡ: `GO_DH` đúng, `con_ton_tai=khong`; `~/.cache/ms-playwright` trước = sau **trùng byte** `8c247ab0…` |
| N4 Windows native (pwsh 7) | `tl-pw-98669eb93778`, hash `590917233a1cbc79`: `CLEANUP OK`, `deleted: false`; khối Gỡ (`C-uninstall.ps1` sinh từ khối 6): `GODH` đúng, `exists_after=False`; `ms-playwright` trước = sau **trùng byte** `a36424f6…`; 15 `.err` cũ nguyên. Out Cleanup `e2ab6e16…`, Gỡ `0ea55d9b…` |

- KHÔNG ĐO ĐƯỢC trên Windows (không tạo được symlink tệp): N5, D10, G9, G10 và các đột biến record-reparse, go-record-reparse.
- Khoá Windows: lấy 14:18:59Z (cả hai rỗng), nhả 14:27:39Z (0 byte); thêm 3 dòng `do-luong.csv` (tổng 23).

## 10. Lượt 7 — sửa theo Codex lượt 6, đo trên `8be8070`

| finding lượt 6 | sửa ở SKILL | ca đo (+ đột biến) |
|---|---|---|
| P1 PowerShell `-ceq` so theo văn hoá, có thể bỏ qua U+00AD ⇒ xoá tệp sai tên | đường dẫn đích (bước dọn) và thư mục hash (trước `open`) so bằng `[string]::Equals(…, Ordinal)` | N26 (`<nonce>` + U+00AD + `.err`) ⇒ dừng, tệp nguyên. **Đột biến `ceq-path` trở về `-ceq` ⇒ LỌT trên CẢ PS 5.1 LẪN pwsh 7: bản cũ CHÉP rồi XOÁ tệp sai tên. P1 là lỗi THẬT, tái hiện trên Windows.** |
| P2 so biên nhận qua chuỗi (bash `$(…)` bỏ NUL, PS `ReadAllText` bỏ BOM) | đầu Cleanup và Gỡ so TỪNG BYTE: bash `printf … \| cmp -s -- - <tệp>`, PS `ReadAllBytes` → base64 → ordinal | D12 (00 thêm NUL/BOM ⇒ dừng trước `close`), G13 (00), G14 (11) ⇒ GIỮ; đột biến trở về so chuỗi: record-bytes→D12, go-record-bytes→G13, go-receipt-bytes→G14, đều lọt trên cả bash lẫn PS |
| P3 (gợi ý) `echo .` che rc của `realpath` | `realpath … && echo .` | các ca liên kết cũ vẫn đạt |

- N22 (giả `cmp` lỗi) chuyển sang chạy riêng đoạn dọn: đầu Cleanup nay cũng dùng `cmp`, nên `cmp` giả dừng nó trước; ca
  đòi thông báo đúng bước so bản sao.

| phép đo | kết quả |
|---|---|
| N1 bash (Linux, node v24.19.0) | `TONG: 123 dat / 123`, 43 đột biến; `SOURCE 01b08e95… pre_frag 79d485ba… dau_frag 84a893f5…` |
| N2 PS 5.1 | `TONG: 122 dat / 122 (bỏ qua 6)`, out `dad6670c…` |
| N2 pwsh 7.6.10 | `TONG: 122 dat / 122 (bỏ qua 6)`, out `0bed7e20…` |
| N3 Linux native | `tl-pw-6f15921bd285`, hash `049d9731e692b377`: Setup/Pin/Cleanup OK, `deleted: false`; khối Gỡ: `GO_DH` đúng, `con_ton_tai=khong`; `~/.cache/ms-playwright` trước = sau **trùng byte** `8c247ab0…` |
| N4 Windows native (pwsh 7) | `tl-pw-bc2e29b9f19d`, hash `3a0502c1880c81ec`: `CLEANUP OK`, `deleted: false`; khối Gỡ: `GODH` đúng, `exists_after=False`; `ms-playwright` trước = sau **trùng byte** `a36424f6…`; 15 `.err` cũ nguyên. Out Cleanup `3208135d…`, Gỡ `e1735e64…` |

- KHÔNG ĐO ĐƯỢC trên Windows (không tạo được symlink tệp): N5, D10, G9, G10 và đột biến record-reparse, go-record-reparse.
- Khoá Windows: lấy 14:42:01Z (cả hai rỗng), nhả 14:48:14Z (0 byte); thêm 3 dòng `do-luong.csv` (tổng 26).

## 11. Lượt 8 — sửa P1 của Codex lượt 7, đo trên `511cf5f`

- P1 (cache Linux không phân biệt hoa thường, ext4 casefold): `find -name` phân biệt hoa thường có thể bỏ sót tệp `.err`
  khác hoa thường, rồi `startDaemon` mở chính tệp đó bằng `w` và cắt rỗng. Sửa: trước `open`, tra ĐÚNG đường dẫn
  `<thư mục hash>/<nonce>.err` và `.session` mà Node sẽ mở (bash `-e`/`-L`; PS `Test-Path`), có thì dừng.
- Ca C19 (`.err`), C20 (`.session`): `find` giả trả rỗng rc 0 trong khi tệp đúng tên đã có ⇒ dừng trước `open`, tệp nguyên;
  đột biến pre-exact-err→C19, pre-exact-session→C20 đều lọt. **Casefold thật KHÔNG ĐO ĐƯỢC** (container không mount
  được ext4 casefold); đây là mô phỏng hành vi phép quét.
- Windows: `GetFileSystemEntries` vốn không phân biệt hoa thường, nên chốt mới là lớp thứ hai sau phép quét, không đo
  tách được; harness PS không đổi.

| phép đo | kết quả |
|---|---|
| N1 bash (Linux, node v24.19.0) | `TONG: 127 dat / 127`, 45 đột biến |
| N2 PS 5.1 | `TONG: 122 dat / 122 (bỏ qua 6)`, out `d51ce2c8…` |
| N2 pwsh 7.6.10 | `TONG: 122 dat / 122 (bỏ qua 6)`, out `741aba3b…` |
| N3 Linux native | `tl-pw-f0be0486b58f`, hash `d42179c0ffb62de8`: Setup/Pin/Cleanup OK, `deleted: false`; khối Gỡ: `GO_DH` đúng, `con_ton_tai=khong`; `~/.cache/ms-playwright` trước = sau **trùng byte** `8c247ab0…` |
| N4 Windows native (pwsh 7) | `tl-pw-d70f778ed015`, hash `e7f0337db6e10a57`: chốt tra đúng tên chạy trên đường dẫn thật và cho qua; `CLEANUP OK`, `deleted: false`; khối Gỡ: `GODH` đúng, `exists_after=False`; `ms-playwright` trước = sau **trùng byte** `a36424f6…`; 15 `.err` cũ nguyên. Out Cleanup `fda190e6…`, Gỡ `6a05598f…` |

- Khoá Windows: lấy 14:58:15Z (cả hai rỗng), nhả 15:07:28Z (0 byte); thêm 3 dòng `do-luong.csv` (tổng 29).

## 12. Trạng thái review

- **Codex lượt 8: `approve`** ở `277db46263883c05d6d3e839d0c4661d7b95597f` (SKILL + hai harness trùng byte `511cf5f`, nơi đo
  N1–N4). Nguyên văn trong `VERDICT.md`.
- P3 còn mở (không chặn): C20 chỉ đo việc dừng, chưa chụp tồn tại/byte/mtime của descriptor như C19. Chưa sửa để giữ
  nguyên byte đã được review; nếu sửa thì harness đổi và cần đo/review lại.
- Gợi ý chưa làm (reviewer nêu, không chặn): Limits có thể ghi thêm fallback Windows khi `LOCALAPPDATA` thiếu/rỗng.
- Merge/land do chủ kho duyệt đúng SHA (lease `uy_quyen_merge: false`). CI trên các head mang mã (`511cf5f`) báo xong,
  không suite nào lỗi theo thông báo GitHub; cổng merge vẫn phải xác nhận lại trên head cuối.
