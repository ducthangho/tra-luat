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
- **PU13 = `setup_error` do môi trường:** tạo symlink tệp cần quyền admin hoặc Developer Mode (`CreateSymbolicLinkW error 1314`). Harness đúng thiết kế: không tính ca này là đạt. Phần hardlink của PU13 vì thế cũng **chưa đo**.
- **CU01..CU09 = `setup_error`: lỗi dựng của harness.** Tiến trình con cũng gặp PU13 nên trả rc 2, mà tiến trình cha chỉ nhận rc 0/1.

## N1b (lần chạy lại duy nhất, chỉ harness Install) @ `22865d8dc`, 02:39–02:40Z
- Bản vá của phiên điều phối (`22865d8dc`) cho phép tiến trình con trả rc 2 khi mọi `setup_error` của nó đã được tiến trình cha đo là `setup_error`.
- **Bản vá có lỗi:** nó đọc `$report.cases`, mà biến này chỉ được gán ở cuối lượt chạy. Dưới StrictMode, cả 9 CU ném lỗi `The property 'outcome' cannot be found` **trước khi** tiến trình con nào kịp chạy. Kết quả: 29/39, cùng tập `setup_error`.
- Tôi không thử bản vá trên Windows trước khi dùng lần chạy lại duy nhất, vì container không có PowerShell.
- Đã sửa ở HEAD (đọc từ `$cases`, danh sách các case đã xong). **Bản sửa này CHƯA chạy native;** ngân sách chạy lại đã hết.

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

## Kết luận tạm (chờ review 2/2)
- **Đạt trong phạm vi đã đo:** 29/30 ca hành vi trên PS 5.1 và PS 7. Có cả các ca tráo junction và tráo tệp: PU23, PU24, PU25, PU28, trong đó PU28 xác nhận `blocked_by=System.IO.IOException`, tức handle chặn được việc tráo.
- **Phản chứng:** 9/9 đột biến bị giết, đúng tập ca khai báo, trên cả hai runtime (phân loại tay).
- **Chưa đo:**
  - PU13 symlink/hardlink (môi trường thiếu quyền);
  - bản sửa harness ở HEAD (để harness tự cấp tín dụng);
  - UNC thật (chỉ có bộ phân loại dạng đường dẫn).
- **Tiêu chí PASS §4 của đặc tả chưa đạt theo chữ** (`setup_error_ids` phải rỗng): cần quyết định của chủ kho, hoặc một lượt đo trên máy có Developer Mode hay quyền symlink.
