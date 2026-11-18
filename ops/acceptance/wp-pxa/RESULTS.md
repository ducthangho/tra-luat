# WP-PXA r1 — Kết quả (#1401)

**Kết luận: đạt trong phạm vi.** Review 2/2 kết luận `approve_scoped` (`VERDICT-run.md`). Review 1/2 là `approve_with_fixes` (`VERDICT-code.md`) và mọi mục đã được sửa.

## Mã
- `.agents/skills/proxima-control/scripts/ProximaActivation.psm1` `bb96cd58…`.
- `tests/ProximaActivation.Tests.ps1` `f539c32d…`, gồm PA01–PA30 và CX01–CX06.
- `SKILL.md` `cc970931…`.
- Commit cuối `be9ca02`.

**Lịch sử executor:**
- Codex: 2 lời gọi. Lời gọi đầu dừng ở preflight vì `base_sha` trong lease g1 sai (lỗi phía điều phối); lời gọi sau viết mã.
- Fable 5.2: 2 lời gọi.
  - Lượt 1: sửa theo 15 mục của review 1.
  - Lượt 2: thay bộ đọc JSON bằng bản tuyến tính.

## Đo native
| Lượt | Máy | Kết quả |
|---|---|---|
| N1 (`b8bb841`) | Desktop, PS5.1 + PS7 | Activation 28/28 và 33/33. Ba harness cũ không hồi quy |
| Perf probe | Desktop, PS7 | Parser cũ **chậm theo bình phương**: n=200/800/1600 mất 3,0/39,5/159,3 s |
| A1 (`b8bb841`) | ASUS, cây Proxima thật | **Treo hơn 31 phút** ở bước đọc manifest 3225 mục. Phiên điều phối dừng tiến trình của chính mình và tự nhả khoá; chưa tạo `version.dll` |
| N2 (`be9ca02`, chạy lại 1/1) | Desktop, PS5.1 + PS7 | Activation **30/30** và **36/36** (6 CX, tr-TR). PA29 đọc 4000 mục trong 95–399 ms. Manifest 12/12, Config 46/46, Control 38/38. Zip `9813dae0…`, quét secret rc 0 |
| A2 (`be9ca02`, chạy lại 1/1) | ASUS, cây Proxima thật 3226 tệp | sạch → **OK**; thêm `version.dll` → **ARTIFACT_EXTRA**; gỡ → **OK**. Mỗi lần kiểm 7–9 s |

## Phạm vi đạt
- **P1-2 (r4 B2):** tệp ngoài manifest bị từ chối trước khi spawn.
- **P1-3 (r4 D3):** chốt profile ở operator; ngăn được giữa các bên cùng dùng guard.
- **§11 #8:** promotion fence ở mức hàm và test.

**Không phủ:** mở Proxima bằng tay, cửa sổ race sau snapshot, tiến trình elevated (trả `NOT_MEASURED`), và việc tích hợp module này vào một luồng kích hoạt thật. Hiện chưa có luồng kích hoạt nào trong repo gọi module.
