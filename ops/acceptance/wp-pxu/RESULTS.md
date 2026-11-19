# WP-PXU r1 — Kết quả đo native trên Desktop (#1409)

Gói bằng chứng trên Desktop: `F:\tl-win\session_015GtxrapMSm976JLC7Fp1HM\wp-pxa\freeze-pxu\wp-pxu-n1-evidence.zip`
- sha256 `cdb2d062f3c4330e577e69492197fbf067d9ca671d55f15f343da2bbdd8b1eb0`, 63 tệp, MANIFEST `508ab7b1…`.
- Quét secret rc 0; `argv` và đích quét được ghi trong `secret-scan.json`.

Cây đo là bản clone sạch (không dùng worktree):
- `tree3` @ `b0ce2443b` cho N1;
- `tree4` @ `22865d8dc` cho N1b.

Giữa hai commit chỉ harness Install đổi; module `ProximaInstall.psm1` giữ nguyên `7b364dc3…`.

## N1 (lượt native 1/1) @ `b0ce2443b`, 02:19–02:37Z
| Harness | PS 5.1 (Desktop) | PS 7 (Core) |
|---|---|---|
| Install mặc định (en-AU) | 29/30, `setup_error_ids=[PU13]` | 29/30, `[PU13]` |
| Install + phản chứng (`tr-TR`) | 29/39: PU13 + CU01..CU09 đều `setup_error` | như PS 5.1 |
| Activation mặc định / phản chứng `tr-TR` | **30/30 · 36/36** | **30/30 · 36/36** |
| Manifest / Config / Control (phản chứng, `tr-TR`) | **12/12 · 46/46 · 38/38** | **12/12 · 46/46 · 38/38** |

- **Hồi quy: không có.** Số đếm bốn harness cũ trùng hoàn toàn WP-PXA N2.
- **PU13 = `setup_error` do môi trường:** tạo symlink tệp cần quyền admin hoặc Developer Mode (`CreateSymbolicLinkW error 1314`). Harness đúng thiết kế: không tính ca này là đạt. *(Sửa theo review 2, P2: các phép kiểm hardlink của PU13 **đã chạy xong** trước bước symlink; chỉ kết quả riêng của nó không được ghi thành một dòng, vì cả ca chuyển sang `setup_error`.)*
- **CU01..CU09 = `setup_error`: lỗi dựng của harness.** Tiến trình con cũng gặp PU13 nên trả rc 2, mà tiến trình cha chỉ nhận rc 0/1.

## N1b (lần chạy lại duy nhất, chỉ harness Install) @ `22865d8dc`, 02:39–02:40Z
- Bản vá của phiên điều phối (`22865d8dc`) cho phép tiến trình con trả rc 2 khi mọi `setup_error` của nó đã được tiến trình cha đo là `setup_error`.
- **Bản vá có lỗi:** nó đọc `$report.cases`, mà biến này chỉ được gán ở cuối lượt chạy. Dưới StrictMode, cả 9 CU ném lỗi `The property 'outcome' cannot be found`. *(Sửa theo review 2, P2: tiến trình con **có chạy**; lỗi xảy ra sau đó, lúc tiến trình cha xử lý kết quả. Câu cũ "trước khi tiến trình con nào kịp chạy" là sai.)* Kết quả: 29/39, cùng tập `setup_error`.
- Tôi không thử bản vá trên Windows trước khi dùng lần chạy lại duy nhất, vì container không có PowerShell.
- Đã sửa ở `42fb4743a` (đọc từ `$cases`, danh sách các case đã xong). Tại thời điểm N1b, bản sửa này chưa chạy native. *(Đã được thay thế: bản sửa chạy native ở **N2** (lease g2) và cấp tín dụng đúng cho 10/10 CU. Xem mục N2.)*

## Phản chứng: phân loại tay từ report của tiến trình con N1 (dữ liệu thật, không phải harness tự cấp tín dụng)
Ở N1 các tiến trình con **đã chạy trọn** và ghi report; chỉ tiến trình cha từ chối nhận chúng. Cả 18 report đã được chép nguyên văn vào `evidence-pxu/children-N1/` (`pxu-collect.ps1`). Bảng dưới là đối chiếu tay (`N1-children-analysis.txt`).

| CU (đột biến) | Ca đỏ ở PS 5.1 và PS 7 (`tr-TR`) | Khớp đúng tập khai báo? |
|---|---|---|
| CU01 bỏ kiểm rỗng + xoá đệ quy | PU05, PU06, PU17, PU21b | khớp |
| CU02 bỏ kiểm băm | PU08, PU25 | khớp |
| CU03 bỏ kiểm số mục | PU07, PU10, PU21 | khớp |
| CU04 bỏ kiểm reparse ở InstallDir | PU11 | khớp |
| CU05 bỏ tiền điều kiện tiến trình | PU14 | khớp |
| CU06 xoá từng đích ngay khi kiểm xong | PU05, PU21, PU21b, PU25, PU28. PU21 và PU25 mang `DirectoryNotFoundException` cùng `present=False` | khớp |
| CU07 xoá updater đệ quy, không cô lập (lỗi driver N3) | PU21, PU25, PU28 | khớp |
| CU08 bỏ kiểm final path ở InstallDir | PU24 (`A directory behind the swapped Programs junction was removed`) | khớp |
| CU09 xoá theo đường dẫn thay vì qua handle | PU28 (`An unverified file planted at the installer path was deleted`) | khớp |

Ở mọi tiến trình con, ngoài các ca đích chỉ có PU13 là `setup_error`; culture là `tr-TR`/`tr-TR`. Mỗi con chạy một module đã đột biến có băm riêng.

## Kết luận tạm sau N1/N1b (lịch sử; review 2/2: `request_changes`, xem `VERDICT-run.md`; đã được thay thế bởi N2 + review g2 bên dưới)
- **Đạt trong phạm vi đã đo:** 29/30 ca hành vi trên PS 5.1 và PS 7. Có cả các ca tráo junction và tráo tệp: PU23, PU24, PU25, PU28, trong đó PU28 xác nhận `blocked_by=System.IO.IOException`, tức handle chặn được việc tráo.
- **Phản chứng:** 9/9 đột biến bị giết, đúng tập ca khai báo, trên cả hai runtime (phân loại tay).
- **Chưa đo (tính tới N1b):**
  - PU13 symlink (môi trường thiếu quyền). *Sửa theo review 3, P2: phần hardlink đã chạy ở N1; ở N2 nó có kết quả riêng `hardlink=CLEANED`.*
  - bản sửa harness. *Đã thay thế: chạy native ở N2.*
  - UNC thật (chỉ có bộ phân loại dạng đường dẫn).
- **Tiêu chí PASS §4 của đặc tả chưa đạt theo chữ** (`setup_error_ids` phải rỗng): cần quyết định của chủ kho, hoặc một lượt đo trên máy có Developer Mode hay quyền symlink.

## N2 (lease g2, lượt native 1/1) @ `9cdfeaf5b`, 03:24–03:25Z
Gói bằng chứng: `F:\tl-win\session_015GtxrapMSm976JLC7Fp1HM\wp-pxa\freeze-pxu2\wp-pxu-n2-evidence.zip`
- sha256 `64efd2de866ca6fcb015f32af464f966dfc5a7c9c2d0e48d6ff2fd54dd3e4aaa`, 13 tệp, MANIFEST `c03c1235…`, quét secret rc 0.
- Cây `tree5` là clone sạch. **Trước khi chạy**, cả module lẫn harness đã được kiểm cú pháp bằng parser của PS 5.1 và PS 7: 0 lỗi.
- Module `81c1164b…`, harness `b2627283…`.

| Harness Install | PS 5.1 (Desktop) | PS 7 (Core) |
|---|---|---|
| Mặc định (en-AU) | **31/32**, `setup_error_ids=[PU13s]` | **31/32**, `[PU13s]` |
| Phản chứng + `tr-TR` | **41/42**, `[PU13s]`; **CU01–CU10 đều `killed` do harness cấp** | **41/42**, như PS 5.1 |

- **PU29 đạt** (kịch bản P1 của review 2: `Programs` bị tráo sang thư mục ngoài có junction `Proxima` → `RESIDUE_CHANGED`, 0 hành động, junction ngoài và tệp đánh dấu còn nguyên). PU23 và PU24 đạt; PU28 `blocked_by=System.IO.IOException`.
- **PU13 (hardlink) đo được:** `hardlink=CLEANED`; bản gốc của hardlink còn nguyên.
- **PU13s (symlink):** `setup_error`, lỗi 1314, vì máy thiếu quyền. Đây là ca duy nhất không đo được.
- **Phản chứng:** mỗi CU làm đỏ đúng tập ca khai báo, `env_limited=[PU13s]`, tiến trình con chạy `tr-TR`. CU08 → PU24, PU29 · CU10 → PU29. Các CU còn lại khớp bảng N1. Bản vá rc-2 của phiên điều phối nay **đã chạy native** và cấp đúng.
- 4 harness cũ không chạy lại: module `ProximaInstall` không được chúng nạp, và số đếm N1 giữ nguyên.

## Kết luận (review g2 1/1: **`approve_scoped`**, xem `VERDICT-run.md` mục g2)
- **Đạt (scoped, Desktop, PS 5.1 + PS 7):** 31/32 ca hành vi; 41/42 khi có phản chứng `tr-TR`; harness tự cấp 10/10 CU. P1 của review 2 đã đóng: PU29 đạt, CU10 bị giết.
- **Giới hạn phải ghi:**
  - PU13s (symlink) `setup_error` 1314, nên PASS §4 **theo chữ chưa đạt**. Quyết định H.7 giữ "chưa đo", không miễn tiêu chí.
  - 4 harness cũ không chạy lại ở `9cdfeaf5b`. Việc mang số đếm N1 sang là suy luận tĩnh, vì chỉ module và harness Install đổi.
  - UNC: chỉ có bộ phân loại.
  - Chưa chạy bộ cài/bộ gỡ thật cùng hàm này. Hàng "quy trình gỡ" của NSIS (MATRIX H.7) vẫn chờ một lần gỡ thật.

## V1: đo trên VM (lease g3; chủ kho "Symlink đo ở VM", 19/11 khoảng 04:35Z) @ `9cdfeaf5b`, 04:37–04:41Z
- **Máy:** `tra-luat-win`, user `tlcommander`, Medium integrity, có `SeCreateSymbolicLinkPrivilege`. Thử tạo và xoá một symlink trong `%TEMP%`: thành công.
- **Phạm vi trên gateway LIVE:** chỉ chạy harness Install với LocalAppData giả trong scratch. Không cài, không gỡ, không đụng Proxima, gateway hay dịch vụ. Khoá `C:\tl-win\KHOA.txt` được lấy rồi nhả. Scratch đã xoá; cây sạch.
- **Cây mã:** fetch nông kèm sparse checkout `.agents/skills/proxima-control` @ `9cdfeaf5b`. Module `81c1164b…`, harness `b2627283…`.
- **Gói bằng chứng trên VM:** `C:\tl-win\session_015GtxrapMSm976JLC7Fp1HM\pxu-vm\freeze\wp-pxu-v1-evidence.zip`, sha256 `eba83af7ea828c04b93224bacd01002a87c198161f90635fdd9e29d62094d819`, 12 tệp, MANIFEST `4604b1a8…`, quét secret rc 0 (bộ quét `fbf9392b…`).

| Harness Install | PS 5.1 (Desktop edition) | PS 7 (Core) |
|---|---|---|
| Mặc định (en-US) | **32/32**, `setup_error_ids=[]` | **32/32**, `[]` |
| Phản chứng + `tr-TR` | **42/42**, `[]`; CU01–CU10 `killed` (con rc 1) | **42/42**, `[]`; CU01–CU10 `killed` (con rc 1) |

- **PU13s (symlink) đạt**; PU13 `hardlink=CLEANED`.
- **Tiêu chí PASS §4 theo chữ (`passed == total`, `setup_error_ids` rỗng) đạt trên VM**, ở cả hai runtime.
- Desktop vẫn là nơi đo 31/32 (chỉ thiếu PU13s), đúng như mục N2.

