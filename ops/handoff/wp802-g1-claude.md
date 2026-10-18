# Handoff wp802 g1 — RG-DA-NEN (executor claude)

Lease `wp802-r1-g1-claude` (`ops/wp802-r1-g1-lease` @ `f6159dc4`) · spec `ops/specs/wp802.md` sha256 `e4fd84e1…00e0` (khớp) · PR #823. Preflight: `ops-publish-lease.yml` 39092181024 + 39092090057 `success`; `ai-dang-giu` 6/6 ⇒ chỉ `wp802-r1-g1-claude` (ref 596 ↔ 596).

- **M1** `launcher.py`: `_ten_tran_giai_ra` giải TÊN TRẦN như bash (PATH theo thứ tự, mục rỗng = cwd, đo bản ấy TRƯỚC. `_cac_duong_dan` dùng cùng hàm ở chế độ native (thứ tự PATHEXT của `which`, `x.CMD` hơn shim `x`, chỉ trong từng thư mục — `which` trên Windows tự chèn cwd). `rg`/`git`: bản ấy hỏng mà bản khác chạy ⇒ `trang_thai: BI_CHE` + `bi_che{ban_hong, loi, ban_tot, cach_chua}`, thiếu bắt buộc (thoát 12), `co` giữ True; quá hạn hoặc tên trần không giải ra ⇒ KHÔNG `BI_CHE`.
- **M2/M5** Windows: `winget … -e --accept-source-agreements --accept-package-agreements --disable-interactivity || choco install ripgrep --yes --no-progress`. Đuôi YAML: thư mục đầu tiên (WinGet Links → choco\bin → `command -v`) có `rg` in đúng regex probe `ripgrep X.Y.Z` (trọn token), không có ⇒ thoát ≠ 0; ghi `$GITHUB_PATH` khi có (lượt 39093706610: winget cài `DAT` 15.2.0 rồi bước sau mất `rg`).
- **M3/M4** hook: chọn nền TRƯỚC probe; Windows probe một lần, không installer, in đúng `$RG_CAI_WINDOWS`; Linux `co_chay rg` trước cargo. Thêm `rg-windows-khong-tu-cai rg-co-chay-truoc-cargo` vào `hook-nang-luc`.
- **M6** 11 ca `r802_*` (tên `wp802_*` vướng `t116`), 20 đột biến `wp802_*`: 11 `launcher.py` (2 chỉ đo trên Windows), 7 `DOT_BIEN_HOOK` (4 hook + 3 YAML, bản sao tạm, chỉ `TinHieuChotCa` là giết), 2 harness. `t106` theo Q2 (BI_CHE, rc 12), giữ phép lùi + thứ tự; bốn neo đột biến cũ đổi theo dòng đã sửa.
- **Codex** lượt 1 (`db1ed4d`) F1–F4, lượt 2 (`509dfa8`) F2 còn ứng viên rc 0 rỗng + F5 hook Windows probe hai lần, lượt 3 (`a0de1f9`) F2 glob lỏng + F6 resolver bỏ `x.CMD` + F3 con trỏ YAML ⇒ đều đã sửa, mỗi cái có ca + đột biến. Verdict: nhánh lease @ `539d086`.
- **N9 có răng**: `nhap/wp802-n9-do` @ `9b45585` hỏng `rg.cai.windows` ⇒ `launcher-windows` 39101164840 ĐỎ ở `Install and verify test tools`; đối chứng `abc16de` ⇒ 39101166158 XANH.
- **Trần ADR-0053**: vượt (473 dòng thêm / 6 tệp, đo `git diff --numstat de82ef74`) theo quyết định chủ kho "Chọn a" — https://github.com/ducthangho/tra-luat/issues/802#issuecomment-6246303988

Số đo Linux/Windows của head cuối: bình luận PR #823 (không chép vào đây kẻo trôi theo head).
Chưa đo: WindowsApps thật (spec). Trên Windows các ca shell POSIX tự bỏ qua ⇒ đột biến của chúng KHÔNG ĐO ĐƯỢC; `wp802_hook_lenh_windows_lech_yaml` vẫn đo qua N6. `||` không chạy trong Windows PowerShell 5.1 (Q6 nguyên văn).
`gate-cong-cu (windows-latest)`: `ops/cong_cu_test.py` t23/t49 đỏ (ngoài write set, không chạm công thức `rg`); master `fb490a7` đỏ sớm hơn ở bước cài `rg` (lượt 39095054115). `gate-ops (windows-latest)`: `ops/lease_publish_test.py` t217 `PermissionError` xoá object git — y hệt trên master (251/252), delta 0.
