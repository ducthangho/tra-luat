# Handoff wp802 g1 — RG-DA-NEN (executor claude)

Lease `wp802-r1-g1-claude` (`ops/wp802-r1-g1-lease` @ `f6159dc4`) · spec `ops/specs/wp802.md` sha256 `e4fd84e1…00e0` (đo lại khớp) · PR #823.
Preflight: `ops-publish-lease.yml` 39092181024 + 39092090057 `success`; `ai-dang-giu` 6/6 ⇒ `NGƯỜI_GIỮ 1: wp802-r1-g1-claude` (ref máy chủ 596 ↔ cục bộ 596).

- **M1** `launcher.py`: `_ten_tran_giai_ra` giải bản TÊN TRẦN như bash (PATH theo thứ tự, mục rỗng = cwd; không dùng `shutil.which` vì trên Windows nó tự chèn cwd), đặt bản ấy LÊN ĐẦU danh sách probe. Với `rg`/`git`: bản ấy hỏng mà bản khác chạy được ⇒ `trang_thai: BI_CHE` + `bi_che{ban_hong, loi, ban_tot, cach_chua}`, vào `thieu_bat_buoc` (thoát 12), `co` giữ True; quá hạn không tính. Tên trần không giải ra trên PATH ⇒ KHÔNG `BI_CHE` (ngoài phạm vi Q2).
- **M2/M5** Windows: `winget … -e --accept-source-agreements --accept-package-agreements --disable-interactivity || choco install ripgrep --yes --no-progress`. Đuôi YAML: thư mục ĐẦU TIÊN có `rg` chạy được (WinGet Links → choco\bin → `command -v`), không có ⇒ thoát ≠ 0; ghi vào `$GITHUB_PATH` khi có. Lý do: lượt 39093706610 (`db1ed4d`) cài `DAT` 15.2.0 bằng **winget** rồi bước sau (shell mới) mất `rg`.
- **M3/M4** hook: `co_chay rg` trước cargo; `MINGW*|MSYS*|CYGWIN*` ⇒ không installer, in đúng `$RG_CAI_WINDOWS`. Thêm `rg-windows-khong-tu-cai rg-co-chay-truoc-cargo` vào `hook-nang-luc`.
- **M6** 9 ca `r802_*` (tên `wp802_*` của spec vướng `t116` `^def [tr]\d+_`), 14 đột biến `wp802_*`: 9 trên `launcher.py`, 5 trong `DOT_BIEN_HOOK` (3 hook + 2 `ops/cong_cu.yaml`, bản sao tạm, chỉ `TinHieuChotCa` là giết, trả lại con trỏ của người gọi). N6 cắt ở ` && ` đầu tiên. `t106` đổi kỳ vọng theo Q2 (BI_CHE, rc 12), giữ phép lùi + thứ tự. Bốn neo đột biến cũ đổi theo dòng đã sửa.
- **Codex lượt 1** (`db1ed4d`, changes_requested): F1 mục PATH rỗng ⇒ đã sửa + 3 đột biến; F2 YAML chọn bản cũ hỏng ⇒ đã sửa + ca chạy nguyên `cai_cong_cu.sh` + 2 đột biến; F3 con trỏ ⇒ đã sửa; F4 ⇒ dòng dưới.

Đo Linux và Windows: xem bình luận PR #823 trên head cuối (không chép số vào đây kẻo trôi theo head).

Chưa đo: ca WindowsApps thật (spec). Trên Windows, N7/N8 và ca cài YAML chỉ POSIX ⇒ 4 đột biến `DOT_BIEN_HOOK` KHÔNG ĐO ĐƯỢC (2 hook + 2 yaml); `wp802_hook_lenh_windows_lech_yaml` vẫn đo qua N6. `||` không chạy trong Windows PowerShell 5.1 (theo Q6 nguyên văn).
