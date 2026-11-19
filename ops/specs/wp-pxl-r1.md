# WP-PXL r1 — LIVE promote hai module ProximaActivation + ProximaInstall lên Desktop rồi VM (đặc tả đóng băng)

- **Packet:** #1413 (con của #1319). Revision 1. Review Class `sensitive`.
- **Căn cứ:**
  - Quyết định của chủ kho ngày 19/11 khoảng 06:03Z: "Live Promote thì đẩy bản lên desktop và cả VM đi".
  - Câu trả lời xác nhận thao tác cụ thể (AskUserQuestion, cùng ngày): **"Chỉ 2 module mới"**.
  - Thiết kế D3 trong `ops/acceptance/wp1319/DESIGN.md`: hàng rào promote; mỗi máy kiểm digest; healthcheck không inference; gateway/service/account/endpoint không đổi; máy trước FAIL thì chặn máy sau.
  - WP-PXA (#1401, `approve_scoped`) và WP-PXU (#1409, `approve_scoped`, VM 42/42).
- **Ranh giới (cứng):**
  - **Không** sửa, thay, gỡ hay import lại `ProximaControl` 1.0.1 trên VM.
  - **Không** dừng, khởi động lại hay đổi cấu hình `ProximaGateway`/`Proxima` runtime.
  - Không đổi service, tác vụ lập lịch, tài khoản, ACL hay endpoint.
  - Không inference. Không cài/gỡ Proxima.
  - Chỉ **thêm** hai thư mục module mới; không ghi đè bất kỳ tệp có sẵn nào. Thư mục đích đã tồn tại thì DỪNG.

## 1. Artifact
Nguồn là commit `9cdfeaf5b1eb17d0d75eb4ce6defe5a29ba69e7a`, nhánh `ccr-8ee03d7f-vnmqk0`. Từ commit này tới HEAD, `.agents/` không đổi.

| Tệp đích (tương đối trong thư mục Modules) | Nguồn | Byte | sha256 |
|---|---|---|---|
| `ProximaActivation/ProximaActivation.psm1` | `.agents/skills/proxima-control/scripts/ProximaActivation.psm1` | 29 276 | `bb96cd5814752c66e84a44ed09b1e311772120413abf991e813d2ce9517a677d` |
| `ProximaInstall/ProximaInstall.psm1` | `.agents/skills/proxima-control/scripts/ProximaInstall.psm1` | 39 070 | `81c1164bf913b181ae5e8e88a04b4498abd592d1ff2e3a25f6cf24d7ed57a82a` |

- **`artifact_sha256`** = sha256 của hai dòng `<đích>\t<byte>\t<sha256>\n` theo thứ tự trên = `194de2661beac7804ff77aec7397ff652220a2a6f8cf30212d77baf9b3510b86`.
- Không thêm `.psd1`. Thư mục module chỉ chứa đúng một `.psm1` cùng tên, nên `Import-Module <tên>` nạp được.

## 2. Đích và thứ tự (hàng rào)
`Plan = [DESKTOP-T9R33P2, TRA-LUAT-WIN]`.

| Máy | Thư mục Modules (đúng chỗ đang chứa module của người dùng/commander) |
|---|---|
| DESKTOP-T9R33P2 | `C:\Users\ThangHD\OneDrive\Documents\PowerShell\Modules` (mục đầu của `PSModulePath`) |
| TRA-LUAT-WIN | `C:\Users\tlcommander\Documents\PowerShell\Modules` và `C:\ProgramData\TraLuatCommander\profile\Documents\PowerShell\Modules`. Cùng hai chỗ đang chứa `ProximaControl` 1.0.1 |

## 3. Bước trên mỗi máy
- **P0 tiền kiểm (chỉ đọc):**
  - lấy khoá host;
  - ghi tải máy;
  - xác nhận thư mục đích **chưa** tồn tại;
  - chụp trạng thái nền:
    - (VM) PID và thời điểm bắt đầu của `ProximaGateway.exe` và cây `Proxima.exe` của nó;
    - (VM) băm mọi tệp của `ProximaControl` 1.0.1 ở cả hai chỗ;
    - (VM) trạng thái các tác vụ lập lịch `TraLuat*`;
    - danh sách module con của mỗi thư mục Modules.
- **P1 hàng rào:**
  - Gọi `Test-ProximaPromotionFence -Plan … -TargetHost <máy> -ArtifactSha256 194de266… -ReceiptDir <dir>`. Hàm lấy từ cây mã đã kiểm băm ở commit trên, **nạp theo đường dẫn**, chưa phải bản vừa cài.
  - Chỉ được tiếp khi kết quả là `ALLOWED`. Máy VM cần receipt của Desktop với `passed=true` và đúng `artifact_sha256`.
- **P2 cài:**
  - Chép hai tệp từ cây mã đã kiểm (băm nguồn phải khớp bảng §1) vào thư mục đích mới.
  - Băm lại tệp đích: phải khớp.
- **P3 kiểm khói (không inference, không xoá gì):** trong tiến trình PowerShell mới, cả PS 7 và PS 5.1 nếu máy có:
  - `Import-Module ProximaActivation` → export đúng `Test-ProximaArtifactTree`, `Enter-ProximaProfileGuard`, `Exit-ProximaProfileGuard`, `Test-ProximaPromotionFence`;
  - `Import-Module ProximaInstall` → export đúng `Remove-ProximaUninstallResidue`;
  - `Remove-ProximaUninstallResidue -WhatIf -LocalAppData <thư mục tạm rỗng>` → `NOTHING_TO_DO`;
  - `Test-ProximaPromotionFence` cho chính máy → `ALLOWED`.

  Trên VM, việc nạp được thử cho thư mục Modules của commander bằng cách nạp theo đường dẫn đầy đủ (không đổi `PSModulePath`).
- **P4 hậu kiểm:**
  - (VM) PID, thời điểm bắt đầu gateway và cây `Proxima.exe` **giống P0**; băm `ProximaControl` 1.0.1 **giống P0**; tác vụ `TraLuat*` **giống P0**;
  - chỉ có thêm đúng hai thư mục module mới.
- **P5 receipt:** ghi `<ReceiptDir>\<host>.json` = `{"schema":"proxima_activation_receipt.v1","host":…,"artifact_sha256":"194de266…","passed":<P1..P4 đạt>,"completed_at":…}`. Nhả khoá. Đóng băng bằng chứng (zip + MANIFEST + quét secret).
- Receipt của Desktop được chuyển nguyên byte sang `ReceiptDir` của VM, kiểm băm trước khi chạy P1 trên VM.

## 4. Rollback
Xoá đúng hai thư mục `ProximaActivation` và `ProximaInstall` vừa tạo trên máy đó. Chỉ xoá khi nội dung còn đúng hai tệp có băm theo §1. Không có gì khác cần hoàn tác. Nếu P4 trên VM thấy gateway thay đổi: dừng, rollback, báo chủ kho; **không** tự khởi động lại gateway.

## 5. PASS
- Mỗi máy: P1 `ALLOWED`, P2 băm khớp, P3 đạt (export đúng, `NOTHING_TO_DO`, `ALLOWED`), P4 không thay đổi ngoài hai thư mục mới, receipt `passed=true`.
- VM chỉ được chạy khi Desktop có receipt `passed=true`.

## 6. Vai, ngân sách, write set
- Operator: phiên điều phối. Không có Executor (không viết mã sản phẩm).
- Reviewer: Codex `gpt-6-astra`, độc lập, chỉ đọc, 1 lượt sau khi xong cả hai máy.
- Native: mỗi máy 1 lượt, chạy lại 1 lần khi lỗi dựng (sau rollback).
- Write set (không glob):
  - `ops/specs/wp-pxl-r1.md`
  - `ops/leases/wp-pxl-r1-g1-operator.yaml`
  - `ops/acceptance/wp-pxl/RESULTS.md`
  - `ops/acceptance/wp-pxl/VERDICT.md`
  - `ops/acceptance/wp1319/MATRIX.md`
