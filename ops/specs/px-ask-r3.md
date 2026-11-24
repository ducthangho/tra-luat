# PX-ASK-SONG r3 — module proxima-control nhận model id thật của Proxima (đặc tả đóng băng)

- **Packet:** #1446. Revision 3, generation 1. Role `executor` (Claude), Review Class `sensitive`.
- **Căn cứ:**
  - r2 (`ops/acceptance/px-ask/r2/RESULTS.md`): `GET /v1/models` của Proxima trên VM quảng bá 13 id dạng `<provider>` hoặc
    `<provider>:<variant>`, ví dụ `chatgpt`, `gemini:auto`, `chatgpt:thinking`, `auto`. Không id nào có `/`.
  - Module 2.0.0 (`Test-PxcModel`, bộ lọc `px models <provider>`) chỉ nhận `<provider>/<model>`, nên `px ask` luôn gặp
    `ModelNotAdvertised`.
  - Chủ kho 20/11 chọn: *"Mở packet sửa module"*.

## 1. Thay đổi hành vi
1. **Model thuộc provider `P`** khi id **bằng đúng** `P`, **hoặc** bắt đầu bằng `P:`, **hoặc** bắt đầu bằng `P/`. Mọi phép so dùng Ordinal.
   Dạng `/` được giữ để tương thích ngược.
2. Mọi chỗ dùng quan hệ "thuộc provider" đều theo luật này qua **một** hàm chung:
   - `Test-PxcModel` (chặn ở `use`, ở `ask` phía local, và ở `Invoke-PxcAsk` phía endpoint);
   - bộ lọc `px models <provider>`.
3. Id vẫn phải khớp **đúng nguyên văn** (Ordinal) một id được quảng bá; giữ nguyên câu so trong vòng lặp hiện có.
4. `Test-PxcProvider` từ chối thêm ký tự `:`, như đã từ chối `/`. Ví dụ provider `gw:fast` ⇒ `ArgumentInvalid`, để một id có biến thể
   không thể tự đóng vai provider.
5. Không đổi gì khác: không đổi HTTP, nhật ký, WhatIf, kiểm runtime, Remote, dịch vụ.

## 2. Phiên bản và tài liệu
- `ModuleVersion` `2.0.0` → `2.1.0` trong `ProximaControl.psd1`, kéo theo frontmatter và mục *Phiên bản* của `SKILL.md`, cùng
  `$Want`/CX04 của `ProximaManifest.Tests.ps1`.
- `SKILL.md` và help của `px` thay `<provider>/<model>` bằng mô tả đúng luật §1.
- Hệ quả Remote (ghi rõ, không xử lý): băm module đổi nên handshake với endpoint chạy bản cũ sẽ lệch. VM hiện chạy 1.0.1, vốn đã lệch.

## 3. Test (Windows tập trung, không CI Windows)
- `ProximaControl.Tests.ps1`:
  - thêm ca bắt buộc **`X5-10`** (26 → 27 id);
  - thêm counterexample **`CX12`**: bỏ dấu `:` khỏi luật tiền tố, phải làm `X5-10` đỏ với token có tên.
- `X5-10` phải đo:
  - nhận: `gw`, `gw:fast`, `prov/m1` (dạng cũ), `auto`;
  - từ chối: `gwz` với provider `gw` (tiền tố thiếu dấu phân cách), `gw:FAST` (sai hoa thường), `gw:slow` (không quảng bá),
    `gw:fast` với provider `g`; với `ask` thì không có POST nào;
  - provider `gw:fast` ⇒ `ArgumentInvalid`;
  - `px models gw` ⇒ đúng `gw,gw:fast`;
  - `ask` với `gw:fast` ⇒ đúng 1 POST, body có `model` = `gw:fast`.
- Chạy trên ASUS từ một clone sạch của kho công khai, tại SHA ứng viên:
  - `ProximaControl.Tests.ps1` với PS 7 và PS 5.1, cả `en-US` lẫn `tr-TR`, kèm `-Counterexamples` ở PS 7 `en-US`;
  - `ProximaManifest.Tests.ps1` với PS 7 và PS 5.1.
  - Đạt khi rc 0, `passed == total`, và mọi CX được ghi có (`credited`).
- `ProximaConfig/Activation/Install.Tests.ps1` không đổi mã nên không chạy lại.

## 4. Review
Codex offline qua `.claude/dev/launcher.py run` trên bundle của SHA ứng viên, **tối đa 2 lời gọi**. Thêm connector Codex trên PR.
P0–P2 chặn merge.

## 5. Sau merge (r4, đặc tả riêng)
Chủ kho chạy lại một lệnh admin trên VM với module 2.1.0, để có **đúng 1** lời gọi `px ask` thật. r3 **không** gọi model.

## 6. Write set (không glob)
- `.agents/skills/proxima-control/scripts/ProximaControl.psm1`
- `.agents/skills/proxima-control/scripts/ProximaControl.psd1`
- `.agents/skills/proxima-control/SKILL.md`
- `.agents/skills/proxima-control/tests/ProximaControl.Tests.ps1`
- `.agents/skills/proxima-control/tests/ProximaManifest.Tests.ps1`
- `ops/specs/px-ask-r3.md`
- `ops/leases/px-ask-r3-g1-claude.yaml`
- `ops/acceptance/px-ask/r3/RESULTS.md`
- `ops/acceptance/px-ask/r3/VERDICT.md`
