# wp728 — Phép đo Linux ĐỘC LẬP cho mã WP710 đã land (zombie/subreaper, suite PowerShell) — Spec r1

> Nguồn quyết định: chủ kho đồng ý khuyến nghị Q9, Q10 (và Q8) của bản nháp `ops/specs/wp710-ke-nhiem-nhap.md`
> (commit `24254793c369f836297e9776fa3b6e721a25eefb`, PR #724), 2026-10-09. Đây là một lượt **ĐO/AUDIT**, không phải
> packet code: không write set sản phẩm. KHÔNG cấp việc: cần Issue `wp728`, lease `role: reviewer` và comment cấp quyền.

## Định danh và thẩm quyền

- `packet_id`: `wp728` · `packet_issue`: 728 · `revision`: 1.
- Đối tượng: lớp `linux-subreaper-khong-thu-hoi-zombie` của WP710 (`ops/reviews/wp710-g5-luot-9/VERDICT.md` dòng 22:
  "CHƯA VÁ trong delta; việc đóng KHÔNG ĐO ĐƯỢC"; dòng 56: Linux "KHÔNG ĐO ĐƯỢC độc lập"), trong commit
  `2e53b19a9c86a06f8f67247f9d68d8933d780de0`.
- Mã đo: `scripts/nlm-credential-refresh.ps1` và `scripts/nlm-credential-refresh.Tests.ps1` tại một exact SHA của
  `master` chứa land `8b59185975a938504de5963d2310e574dd4858b2` (đo spec: `353da6b30f7e2f54a7bed92db97c0fe9ea70a21d`).
  Ghi `reviewed_sha` + blob sha256 của hai tệp trong biên nhận.
- **Bên đo phải khác Executor.** Executor g5 của WP710 là `claude` (`ops/leases/wp710-r4-g5-claude-windows.yaml`:
  `provider: anthropic_claude`) ⇒ phiên Claude nào đo cũng chỉ là `same_provider`. Bên đo: **`codex` trên phiên cloud
  Linux** (`cross_approved`, bằng chứng họ model `do_may` từ `run.json`); dự phòng **human audit**.
- Tiền điều kiện đo được 2026-10-09T16:53Z và 18:10Z: trong container cloud, `codex` `CHUA_XAC_THUC` — `access_token`
  hết hạn (−136 h), `last_refresh=2026-09-24T01:47:47Z`. Chủ kho phải làm mới `CODEX_AUTH_JSON` (chép base64 NGAY sau
  `codex login`; refresh token xoay vòng — CLAUDE.md) trước khi phát lượt.
- Phân công (bài học CLAUDE.md "REVIEWER BỊ CHẶN"): mọi rig cần dựng đã mô tả dưới đây bằng lời; phiên điều phối dựng
  sẵn script rig ở scratch rồi giao reviewer CHẠY và ĐỘT BIẾN, không bắt reviewer tự soạn nội dung điều khiển tiến
  trình. Gọi qua `.claude/dev/launcher.py run` để lượt chết vẫn để lại `run.json`; truyền prompt làm đối số
  (stdin là DEVNULL), dùng đường dẫn `codex` đã resolve.
- Không LIVE, không `nlm` thật, không credential, không Drive. Fake CLI của bộ test là đủ.

## Phép đo

- **M1 — suite.** `pwsh -NoProfile -File scripts/nlm-credential-refresh.Tests.ps1` trên Linux. Ghi `pwsh`
  `$PSVersionTable.PSVersion`, `python --version`, `python3 --version`, `uname -r`, rc, dòng tổng kết nguyên văn. Đạt khi
  `failed=0` VÀ `passed` bằng số ca thực chạy trên Linux (đếm `$cases++` đã thực thi — không tin con số 34 của
  Executor). Bẫy đã biết: `Tests.ps1:213` gọi `Get-Command python`; nền chỉ có `python3` ⇒ dựng shim `python` trong
  một thư mục PATH tạm và GHI LẠI đã làm thế.
- **M2 — zombie nhiều chu kỳ.** Ca `v` (`Tests.ps1:991–1027`) chỉ kiểm SAU CHU KỲ ĐẦU (`-MaxCycles 2`); con số
  "4 chu kỳ, 0 zombie" của `changelog.d/wp-710.md:38` đến từ rig KHÔNG có trong kho. Rig: chạy wrapper với fake CLI của
  bộ test, chế độ `daemon` (con mồ côi bị dừng mỗi chu kỳ), `-EnableKeepalive -MaxCycles ≥4 -IntervalSeconds` đủ
  ngắn; trong MỖI khoảng nghỉ đếm tiến trình con của wrapper ở trạng thái `Z` qua `/proc/*/stat` (trường ppid = pid
  wrapper). Đạt khi 0 ở MỌI khoảng.
  **Phản chứng bắt buộc:** cùng rig trên BẢN SAO TẠM của wrapper đã gỡ lời gọi `Invoke-ReapAdopted` phải cho số zombie
  TĂNG theo chu kỳ (changelog khai đầu cũ: 1, 2, 3). Không tăng ⇒ rig không có răng ⇒ M2 = `KHÔNG ĐO ĐƯỢC`, không phải đạt.
  Đột biến chạy trên bản sao, không bao giờ trên tệp trong checkout.
- **M3 — đồng hồ (ghi nhận, không đóng lớp).** Ghi độ lệch mốc khởi động tiến trình đọc từ một pwsh sống ≥250 s so với
  pwsh mới (để so với lời khai 2,9 s/130 s và 7,0 s/256 s trên WSL). Q8: không sửa; chỉ ghi.
- **Parity 101 dạng / 168 chuỗi byte — KHÔNG đo lại (Q10).** Script so của Executor không có trong kho (tìm 16:57Z) ⇒
  không tái lập nguyên văn được; lượt 9 đã đóng lớp `stage-canary-true-khi-than-rong-hoac-sai-id` bằng fixture offline.
  Biên nhận ghi đúng câu: "parity 101/168: KHÔNG TÁI LẬP ĐƯỢC từ kho; không đo".

## Đầu ra

- `ops/reviews/wp728-do-linux/`: `VERDICT.md` (bảng M1–M3: `passed`/`failed`/`not_measured` kèm lệnh, rc, đầu ra
  nguyên văn), `run.json`, `SHA256SUMS.txt`, `.gitattributes` với `* -text` (bài học hồ sơ g5: CRLF).
- Kết luận cho lớp `linux-subreaper-khong-thu-hoi-zombie`: `đóng` chỉ khi M1 đạt VÀ M2 đạt kèm phản chứng có răng;
  ngược lại giữ mở và nêu cái thiếu.
- Biên nhận được đẩy bởi phiên điều phối lên một nhánh `ops/**`, không phải bởi reviewer (reviewer read-only).

## chua_do_duoc

- Hành vi trên WSL của máy chủ kho (rig khác cloud Linux); kết quả cloud không chứng minh WSL và ngược lại.
- `nlm` CLI và browser thật.
