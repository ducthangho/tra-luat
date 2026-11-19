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

## r2 (19/11): finding P2 của connector Codex — culture của tiến trình con phản chứng
**Finding:** review `5972629197` (comment `4626897634`, PR #1378, head `953ba9d8`).
- Harness không truyền culture cho tiến trình con phản chứng, và không kiểm culture của con.
- Lời khai "6 CX, tr-TR" ở dòng N2 phía trên **không được chứng minh cho tiến trình con**.

**Đo lại bằng chứng cũ trên Desktop** (culture mặc định `en-AU`):
- Ở lượt N1 trên cả PS 7 và PS 5.1, report của tiến trình cha ghi `tr-TR`.
- Cả 10 report của tiến trình con CX01–CX05 đều ghi **`en-AU`**.
- Vậy ở các lượt trước, ca CX được ghi nhận dưới culture mặc định của máy, không phải dưới `tr-TR`.

**Sửa** (đặc tả `ops/specs/wp-pxa-r2.md`, chỉ đổi `tests/ProximaActivation.Tests.ps1`, theo đúng mẫu của `ProximaInstall.Tests.ps1`):
- thêm tham số `-Culture`, đặt culture cho tiến trình cha;
- report thêm `ui_culture` và `culture_at_end`;
- luôn truyền `-Culture` cho tiến trình con;
- trước khi cấp `killed`, kiểm `culture` và `culture_at_end` của con phải bằng culture của cha.

Harness mới có sha256 `e5cc81c1…`. Module không đổi (`bb96cd58…`).

**Đo trên Desktop** (19/11, 09:50:04–09:51:41Z):
- Có khoá host. Parse bằng parser PS 7 và PS 5.1 đều cho 0 lỗi. Chạy khô trước đó đạt.

| Lượt | Kết quả |
|---|---|
| PS 7.6.10, `-Culture tr-TR -Counterexamples` | **36/36**, rc 0. Cha `tr-TR`/`tr-TR`; CX01–CX06 `killed`, `child_culture=tr-TR` |
| PS 5.1.26100, cùng cờ | **36/36**, rc 0. Cha `tr-TR`/`tr-TR`; CX01–CX06 `killed`, `child_culture=tr-TR` |
| Phản chứng: bản sao tạm bỏ `-Culture` cho con (`cb0e231a…`), PS 7 | rc 2, 30/36. CX01–CX06 `not_credited`: *"child ran under culture 'en-AU'/'en-AU', parent under 'tr-TR'"* |

**Bằng chứng:**
- Zip: `F:\tl-win\session_015GtxrapMSm976JLC7Fp1HM\pxa-r2\freeze\wp-pxa-r2-evidence.zip`, sha256 `e1d6505bf6d4251f207e2ada20a67498e3a627d2aeed312d8fb1f8f670ee0b8e`, 16 tệp, MANIFEST `297d4093…`.
- Quét secret rc 0.
- Driver `R2.ps1`. Bản harness được dựng từ blob cũ cộng đúng các thay thế trong `build.py`; băm khớp commit vá.
