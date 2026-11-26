tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
dieu_kien_merge: ADR-0060@36d7c5dcdcbbb27176b75135125b9009f9fe0587

# PX-TRIEN-KHAI-VM r1 — triển khai `proxima-control` 2.2.0 lên endpoint VM và chạy thật `gemini:auto` (đặc tả)

## packet_id · packet_issue
- `packet_id`: `px-trien-khai-vm`. Revision 1, generation 1. Role `operator` (Claude, phiên `session_015GtxraqxgU6x1GshxzYCF4`).
- `packet_issue`: #1562. Review Class `sensitive` (thao tác sống trên VM; cùng lớp với `px-ask`).

## nguon_cap_viec
- Kế nhiệm #1529 (`px-loc-markup` r4, merge `4f954fe`): đặc tả r4 để ngoài phạm vi "kiểm thật sau merge (Q7)" và "đồng bộ phiên bản
  module trên VM".
- Chủ kho chốt bốn điểm (ghi hộ `issuecomment-7198271855`): một packet; phiên triển khai qua Desktop Commander với tư cách
  `tlcommander`; đúng 2 lời gọi `gemini:auto`; chỉ triển khai khi không có hoạt động `px-active` trong 15 phút.
- Tiền lệ chạy thật: `ops/specs/px-ask-r2.md`, `ops/acceptance/px-ask/r5/RESULTS.md` (#1446).

## so_do_nen (đọc-chỉ, 26-11-2026 ~17:0xZ, máy `tra-luat-win`)
- Desktop Commander có hai thiết bị cùng tên: `f7281f27…` chạy `tra-luat-win\tlcommander`, `810f79bb…` chạy `tra-luat-win\tladmin`.
- `<base>` = `C:\Users\tlcommander\ProximaGateway`. `<base>\control\` chứa `ProximaControl.psd1` và `ProximaControl.psm1` bản **1.0.1**
  (03-11-2026), **không có** `ProximaConfig.psm1`. Endpoint Remote (`ProximaControl.psm1` 2.x) băm và nạp đúng hai tệp
  `<base>\control\ProximaControl.psm1` + `ProximaConfig.psm1` ở mỗi lời gọi, lệch thì `EndpointCodeMismatch` ⇒ client 2.x hiện không
  dùng được đường Remote. Đường Local nạp module từ bản clone kho, không qua `control\`.
- `<base>\results\px-active\`: 164 mục, mục mới nhất 11:12:28Z ⇒ gateway đang được phiên khác dùng.
- Tiền lệ `px-ask` r1: tài khoản Desktop Commander không đọc được `ExecutablePath` của tiến trình gateway ở session 0 ⇒ `RuntimeUnverified`;
  r2/r5 chạy thật được nhờ chủ kho chạy một lệnh trong PowerShell admin qua RDP.
- sha256 bản 2.2.0 trên master `4f954fe`: `ProximaControl.psm1` `d26bf828cf12578ca8e3eb54c58438244c1305bf428b5f551757ec98080f339f`,
  `ProximaConfig.psm1` `59abfa860e59af7c596a9e3f60829f8dc1af4a853c5d4ac197c00cc033d76e7d`, `ProximaControl.psd1`
  `a8af40d86325999f7266f8d5a6f954506c008d76b40d77597cc3873c23b2cb8d`, `Run-Px.ps1`
  `03f99881494329cea213714b5e603d83776a7fb57bb153e1a4431d4acc479354`.

## write_set
- `ops/specs/px-trien-khai-vm-r1.md`
- `ops/leases/px-trien-khai-vm-r1-g1-operator.yaml`
- `ops/acceptance/px-trien-khai-vm/r1/RESULTS.md`

Không tệp mã nào trong kho đổi. Thay đổi sống chỉ ở `<base>\control\` (thay 1.0.1 bằng 2.2.0, giữ bản sao lưu) và một bản nhật ký
`px.active.v1` mỗi lời gọi `ask` (do module tự ghi).

## ngoai_pham_vi
- Khởi động/dừng/cài dịch vụ, khởi động lại Proxima, `px start|stop|restart|connect`; đổi cấu hình gateway, tài khoản, ACL, WinRM,
  firewall. Cần một trong các thứ ấy ⇒ dừng, báo chủ kho (E2).
- Đọc profile, cookie, `byok.json`, `ipc-token.json`, kho thông tin đăng nhập; in `PROXIMA_API_KEY`. Chép log thô vào kho.
- Chạy thử đường Remote (cần thông tin đăng nhập WinRM): ngoài phạm vi; đường Remote chỉ được kiểm tĩnh bằng băm (N3).
- Sửa gateway Proxima; chặn model khác `auto`.

## cac_buoc (mỗi bước một lần; lỗi ở bước nào thì ghi và dừng, không tự sửa)
**B0 — đo trước (đọc-chỉ, `tlcommander`).** Ghi: không có mục `px-active` mới trong 15 phút gần nhất (so `LastWriteTimeUtc` lớn nhất
với giờ hiện tại); băm 2 tệp hiện có trong `control\`; danh sách tệp `control\`. Có mục mới trong 15 phút ⇒ chờ, báo chủ kho, không
triển khai.

**B1 — sao lưu.** Chép `control\` sang `<base>\control.bak-<UTC yyyyMMddTHHmmssZ>\` (thư mục mới, thất bại nếu đã tồn tại); so băm
từng tệp bản sao = bản gốc.

**B2 — triển khai.** Lấy `ProximaControl.psm1`, `ProximaConfig.psm1`, `ProximaControl.psd1` từ master `4f954fe` (chuyển bằng clone kho
public tại đúng commit, kiểm `HEAD` và băm), ghi đè đúng 3 tệp trong `control\`. Không xoá, không thêm tệp khác. Đo lại băm 3 tệp =
số ở `so_do_nen`. Lệch hoặc ghi lỗi ⇒ khôi phục từ `control.bak-*` (chép ngược, đo băm = B0), báo chủ kho.

**B3 — đường chạy thật.** Dựng thư mục làm việc `D` ngoài `<base>` (clone kho public tại `4f954fe`, kiểm 4 tệp module = `so_do_nen`),
cấu hình `D\px-trien-khai-vm.json` (`schemaVersion` 1, `targetId` `px-trien-khai-vm`, `mode` `Local`, `basePath` `<base>`), script
`D\R1.ps1`. Chạy thử từ Desktop Commander chỉ `px config` + `px status` (không inference):
- `status` ok ⇒ phiên chạy B4 từ Desktop Commander.
- `RuntimeUnverified` hoặc lỗi quyền ⇒ chủ kho chạy đúng một lệnh trong PowerShell admin qua RDP:
  `pwsh -NoProfile -ExecutionPolicy Bypass -File <D>\R1.ps1` (tiền lệ r2/r5), rồi dán kết quả.

**B4 — `R1.ps1` (theo thứ tự, mỗi bước một lần).** Ghi danh tính (admin hay không, session); nạp module từ `D`, ghi `ModuleVersion`
(phải `2.2.0`) và băm; `px config`, `px status`, `px models gemini` (không inference); `gemini:auto` phải có trong danh sách, không có ⇒
dừng trước ask; `px ask gemini <Q1> -Model gemini:auto -WhatIf`; đúng **1** lần `px ask gemini <Q1> -Model gemini:auto`; đúng **1** lần
`px ask gemini <Q2> -Model gemini:auto`. Không thử lại, không đổi model/provider khi lỗi. `Q1` = `Reply with exactly one word: OK`.
`Q2` = `Tóm tắt trong hai câu: Luật Ban hành văn bản quy phạm pháp luật quy định những gì?` (câu mở, dễ sinh gợi ý câu hỏi tiếp).
Ghi mọi `px.result.v1` (hoặc mã lỗi) vào `D\r1-vm.json`, in sha256 tệp.

## nghiem_thu
- **N1 (cửa sổ):** B0 ghi mục `px-active` mới nhất cách giờ triển khai ≥ 15 phút. ĐỎ khi triển khai mà thiếu phép đo này.
- **N2 (sao lưu):** `control.bak-*` tồn tại, băm từng tệp = bản 1.0.1 đo ở B0.
- **N3 (triển khai, kiểm tĩnh Remote):** băm `control\ProximaControl.psm1` và `control\ProximaConfig.psm1` = số 2.2.0 ở `so_do_nen` (chính
  là `moduleSha256`/`configModuleSha256` mà client 2.2.0 gửi trong envelope); `control\` không có tệp nào ngoài tệp đã có ở B0 cộng
  `ProximaConfig.psm1`.
- **N4 (chạy thật):** đúng 2 lời gọi `ask` không `-WhatIf`, mỗi lời gọi đúng một bản nhật ký `px.active.v1` mới; với mỗi lời gọi ghi
  `outcome`, `httpStatus`, `answerMarkup`, `answerMarkupRemoved`, `reportedModel`, độ dài `answer`. Kết luận mỗi lời gọi:
  `ask_ok` (outcome `ok`, HTTP 200), `ask_failed` (kèm mã), hoặc `blocked` (dừng trước ask, kèm mã). N4 không đòi `answerMarkup`
  = `removed`: gateway có sinh khối hay không là dữ kiện đo, không phải tiêu chí đạt.
- **N5 (ranh giới):** không bước nào chạm dịch vụ, cấu hình, profile, thông tin đăng nhập; `ModuleVersion` nạp ở B4 = `2.2.0`.
- **N6 (sổ sách, ADR-0060):** RESULTS chỉ ghi dữ kiện đã lược (không tên tài khoản ngoài hai tên thiết bị đã đo ở `so_do_nen`, không
  JSON thô); câu trả lời model gắn nhãn không tin cậy. RESULTS viết XONG trước review offline và trước lần push duy nhất; bằng chứng
  sinh sau approve (CI, connector, merge) chỉ ghi lên Issue và bản ghi M8, không commit thêm.

## luat_dung
- Trần lời gọi Codex theo dòng khai `ADR-0055`; mỗi lời gọi ghi `packet_loop.py record-codex-call` neo SHA. Chạm trần ⇒ **E2**.
- Inference: đúng 2. Lời gọi thứ ba bất kỳ ⇒ vi phạm; cần thêm ⇒ **E2**.
- Cần khởi động lại dịch vụ/gateway, quyền admin cho bước khác B4, hay đổi cấu hình ⇒ dừng, **E2**.
- Có hoạt động `px-active` trong 15 phút ở B0 ⇒ chờ; quá 24 giờ không có cửa sổ ⇒ báo chủ kho.
- PR theo ADR-0060: mở draft; push một lần sau review offline approve và gate; commit mới ⇒ về draft; push thêm cần checkpoint chủ kho.

## pham_vi_e
Không chạm E4, E5. Thao tác sống trên VM của chủ kho ⇒ đặc tả chờ chủ kho duyệt băm trước khi cấp lease.

## chua_do_duoc
- Đường Remote chạy thật (handshake qua WinRM): không đo trong r1.
- Gateway có sinh khối `ElicitationsGroup` cho Q2 hay không: không đoán trước; mẫu duy nhất là lời khai của #1457 r2.
- Bản sao lưu `control.bak-*` để lại trên VM; dọn là việc riêng khi chủ kho yêu cầu.
