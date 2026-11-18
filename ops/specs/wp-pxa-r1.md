# WP-PXA r1 — Chốt kích hoạt Proxima (đặc tả đóng băng)

- **Packet:** #1401 (con của #1319). Revision 1, generation 1. Review Class `sensitive`.
- **Căn cứ:**
  - Finding P1-1, P1-2 và P1-3 trong `ops/acceptance/wp1319/r4/VERDICT-run.md`.
  - Quyết định của chủ kho ngày 18/11 trong phiên `session_015GtxrapMSm976JLC7Fp1HM`:
    - P1-2: module mới trong repo.
    - P1-3: chốt ở operator.
    - §11 #8: xử lý luôn.
    - Gateway: không inference.
- **Ranh giới:**
  - Không sửa `scripts/ProximaControl.psm1`, `scripts/ProximaConfig.psm1`, `scripts/ProximaControl.psd1`, `scripts/Run-Px.ps1`, `config.example.json` hay các test cũ.
  - Không đụng mã P4 đã đóng băng hay binary Proxima.
  - Không có LIVE, không inference, không đăng nhập.

## 1. Mã mới
Tệp `.agents/skills/proxima-control/scripts/ProximaActivation.psm1`:
- Chạy được trên Windows PowerShell 5.1 và PowerShell 7.
- `Set-StrictMode -Version 3.0`. Chỉ dùng .NET/BCL và cmdlet có sẵn; không phụ thuộc module ngoài.
- Không import ProximaControl/ProximaConfig.
- Export **đúng** ba hàm (đôi khoá profile tính là một): `Test-ProximaArtifactTree`, `Enter-ProximaProfileGuard` cùng `Exit-ProximaProfileGuard`, và `Test-ProximaPromotionFence`. Tổng cộng 4 tên.
- Mỗi hàm trả một object có `ok` (bool) và `code` (string). Không ném lỗi ra ngoài: lỗi bất ngờ trả `ok=$false`, `code='NOT_MEASURED'`, kèm `error`.

### 1.1 `Test-ProximaArtifactTree -Root <dir> -ManifestPath <json> [-MutableRelative <string[]>] [-Override <hashtable rel→@{bytes;sha256}>]`
- **Manifest:** JSON có dạng `{ "<rel posix>": {"bytes": int, "sha256": hex} }`, cùng dạng `variant-manifests.json[variant]` của P4. Ngoài ra nhận dạng `{"files": {...}}`.
- **Duyệt cây:**
  - Đi toàn bộ cây dưới `Root` mà **không đi theo** reparse point. Bất kỳ thư mục hay tệp nào là reparse point (gồm cả `Root`) đều cho `REPARSE_POINT`.
  - Tên tương đối so **không phân biệt hoa thường** (Ordinal IgnoreCase). Hai đường dẫn chỉ khác hoa thường cho `DUPLICATE_CASE`.
- **So tập:** thực tế so với kỳ vọng (`manifest ∪ Override`).
  - Thiếu một tệp cho `ARTIFACT_MISSING`. Tệp trong `MutableRelative` được phép vắng mặt.
  - **Thừa một tệp cho `ARTIFACT_EXTRA`.** Đây là sửa P1-2: tệp thừa bị từ chối kể cả khi nó không nằm trong manifest.
  - Khác `bytes` hoặc `sha256` cho `ARTIFACT_CHANGED`. Tệp trong `MutableRelative` không bị kiểm nội dung.
- **Thứ tự mã lỗi khi gặp nhiều lỗi cùng lúc:** `REPARSE_POINT` > `DUPLICATE_CASE` > `ARTIFACT_EXTRA` > `ARTIFACT_MISSING` > `ARTIFACT_CHANGED`. Danh sách đầy đủ vẫn trả trong `extra`, `missing`, `changed` (tối đa 100 mỗi loại).
- Thư mục rỗng không có trong manifest chỉ được báo ở `extra_dirs`, không làm hàm fail.
- Trả thêm `verified_files` và `root`.

### 1.2 `Enter-ProximaProfileGuard -ProfileDir <dir> [-ProcessProvider <scriptblock>]` và `Exit-ProximaProfileGuard -Guard <obj>`
- `ProcessProvider` dùng để test; mặc định là `Get-CimInstance Win32_Process`. Nó trả các object có `ProcessId`, `Name`, `ExecutablePath`, `CommandLine`.
- **Thứ tự kiểm:**
  1. Lấy danh sách tiến trình. Không lấy được thì `NOT_MEASURED`, và **không** cấp khoá.
  2. Có tiến trình tên `Proxima*.exe` mà CommandLine chứa `--user-data-dir=<ProfileDir>` thì `PROFILE_BUSY`. So sau khi chuẩn hoá đường dẫn: đầy đủ, bỏ dấu `\` cuối, không phân biệt hoa thường, chấp nhận cả dạng có hoặc không có dấu ngoặc kép.
  3. Mỗi tệp `rest-port.json` và `ipc-port.json` có trong profile: nếu `pid` trỏ tới một tiến trình **còn sống** tên `Proxima*` thì `PROFILE_BUSY`. JSON hỏng thì `NOT_MEASURED`.
  4. Mở `<ProfileDir>\.proxima-activation.lock` với `FileMode.OpenOrCreate`, `FileAccess.ReadWrite`, `FileShare.None`. Không mở được vì đang có người giữ thì `PROFILE_LOCKED`.
  5. Khi đã giữ được khoá, ghi một dòng `pid<TAB>utc<TAB>host`.
- Kết quả thành công: `ok=$true`, `code='ACQUIRED'`, `guard` là object giữ stream. Người gọi phải giữ guard suốt thời gian app chạy rồi gọi `Exit-ProximaProfileGuard`. `Exit` đóng stream, idempotent, và **không** xoá tệp khoá.
- Đã biết và chấp nhận: chốt này không chặn được người tự mở Proxima bằng tay mà không qua guard. Ghi điều này trong SKILL.md.

### 1.3 `Test-ProximaPromotionFence -Plan <string[]> -TargetHost <id> -ArtifactSha256 <hex64> -ReceiptDir <dir>`
- Hàm thuần: chỉ đọc tệp, không ghi gì.
- Receipt là tệp `<ReceiptDir>\<host>.json` có dạng `{"schema":"proxima_activation_receipt.v1","host":...,"artifact_sha256":...,"passed":bool,"completed_at":iso}`.
- **Mã trả về:**

  | Mã | Khi nào |
  |---|---|
  | `FENCE_TARGET_UNKNOWN` | `TargetHost` không có trong `Plan` |
  | `ALLOWED` (`ok=$true`) | `TargetHost` là phần tử đầu của `Plan`; hoặc mọi host đứng trước đều có receipt hợp lệ, `passed=true`, `host` khớp tên tệp và `artifact_sha256` khớp (chữ thường) |
  | `FENCE_PRIOR_MISSING` | Thiếu receipt của một host đứng trước |
  | `FENCE_RECEIPT_INVALID` | Receipt hỏng hoặc sai schema |
  | `FENCE_PRIOR_FAILED` | Một host đứng trước có `passed=false` |
  | `FENCE_ARTIFACT_MISMATCH` | Một host đứng trước có `artifact_sha256` khác |

- Trả kèm `blocking_host`.

## 2. Test
Tệp `.agents/skills/proxima-control/tests/ProximaActivation.Tests.ps1`:
- Harness tự viết, **không dùng Pester**, cùng khuôn với `ProximaManifest.Tests.ps1`: `-AddonRoot -ScratchRoot -ReportPath [-Counterexamples]`; rc 0 khi đạt, rc 1 khi một thuộc tính sai, rc 2 khi lỗi dựng. Report JSON có `total`, `passed`, `failed_ids`, `harness_sha256` và `source_hashes`.
- **Các ca bắt buộc:**

  | Ca | Nội dung |
  |---|---|
  | PA01 | Cây đúng → `ok` |
  | PA02 | Sửa 1 byte → `ARTIFACT_CHANGED` |
  | PA03 | Đổi kích thước → `ARTIFACT_CHANGED` |
  | **PA04** | **Thêm `version.dll` cạnh exe → `ARTIFACT_EXTRA`** (hồi quy r4 B2) |
  | PA05 | Thiếu tệp → `ARTIFACT_MISSING` |
  | PA06 | Junction trong cây → `REPARSE_POINT`, tạo bằng `New-Item -ItemType Junction` hoặc `cmd /c mklink /J`, không cần quyền admin. Trên nền không tạo được junction thì ghi rõ `skipped` kèm lý do; trên Windows không được skip |
  | PA07 | Tệp mutable khác nội dung hoặc vắng mặt → `ok` |
  | PA08 | Manifest hỏng → `NOT_MEASURED` |
  | PA09 | Guard hai lần trên cùng profile → lần hai `PROFILE_LOCKED`; sau `Exit` thì lần ba `ACQUIRED` |
  | PA10 | ProcessProvider giả có `Proxima.exe` mang `--user-data-dir` của profile → `PROFILE_BUSY` |
  | PA11 | `rest-port.json` trỏ pid sống tên `Proxima.exe` (giả) → `PROFILE_BUSY` |
  | PA12 | ProcessProvider ném lỗi → `NOT_MEASURED` và không có tệp khoá bị giữ |
  | PA13–PA18 | Fence lần lượt: `ALLOWED` (host đầu), `ALLOWED` (đủ receipt), `FENCE_PRIOR_MISSING`, `FENCE_PRIOR_FAILED`, `FENCE_ARTIFACT_MISMATCH`, `FENCE_RECEIPT_INVALID`, và `FENCE_TARGET_UNKNOWN` |

- **`-Counterexamples` (đột biến chứng minh test có răng):**
  - Chép module ra scratch, bỏ phép so tập (chỉ duyệt manifest) → PA04 phải ĐỎ.
  - Bỏ kiểm CommandLine → PA10 phải ĐỎ.
  - Bỏ kiểm receipt `passed` → ca `FENCE_PRIOR_FAILED` phải ĐỎ.
  - Mỗi đột biến chạy trên **bản sao tạm**, không chạy trên tệp thật.

## 3. Tài liệu
Thêm vào `SKILL.md` một mục ngắn "Kích hoạt (Activation guard)": ba hàm, mã lỗi, và giới hạn của chốt profile. Bảo đảm `ProximaManifest.Tests.ps1` (PM01–PM07) vẫn đạt; mục này không được làm vỡ kiểm tag hay kiểm nội dung của nó.

## 4. Đo
- **Desktop `a5f7076e`:** chạy `ProximaActivation.Tests.ps1` trên PS5.1 và PS7, có và không có `-Counterexamples`. Chạy lại ba harness cũ (Manifest, Config, Control) có `-Counterexamples`, `tr-TR` như r3, để chứng minh không hồi quy. Dùng khoá `C:\tl-win\KHOA.txt` / `F:\tl-win\KHOA.txt`.
- **ASUS `7404cfba`, chỉ đọc, đối chứng thật:** chạy `Test-ProximaArtifactTree` trên `C:\Users\admin\tl-work\wp1319-r4\copy` với manifest `variant-manifests.json["baseline"]`. Override `resources/app-update.yml` bằng băm thực tế; `MutableRelative` = `resources/app.asar.unpacked/src/enabled-providers.json`.
  - Cây sạch → `ok`.
  - Thêm `version.dll` **vào một bản sao nhỏ trong thư mục tạm của wp1319-r4**, hoặc tạm thời vào `copy` rồi xoá và kiểm lại → `ARTIFACT_EXTRA`.
  - Dùng khoá `D:\tl-win\KHOA.txt`.

## 5. Vai, ngân sách, write set
- Executor Codex, ≤ 3 lời gọi.
- Reviewer Claude, độc lập, chỉ đọc, effort cao. Review mã trước khi đo; review kết quả sau khi đo. Tối đa 2 lượt.
- Native: Desktop 1 lượt và ASUS 1 lượt, mỗi máy được chạy lại 1 lần khi lỗi dựng.
- Write set (liệt kê từng tệp, không glob):
  - `.agents/skills/proxima-control/scripts/ProximaActivation.psm1`
  - `.agents/skills/proxima-control/tests/ProximaActivation.Tests.ps1`
  - `.agents/skills/proxima-control/SKILL.md`
  - `ops/specs/wp-pxa-r1.md`
  - `ops/leases/wp-pxa-r1-g1-executor.yaml`
  - `ops/acceptance/wp-pxa/RESULTS.md`
  - `ops/acceptance/wp-pxa/VERDICT-code.md`
  - `ops/acceptance/wp-pxa/VERDICT-run.md`
  - `ops/acceptance/wp1319/MATRIX.md`
