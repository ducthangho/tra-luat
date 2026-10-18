# Handoff wp802 g1 — RG-DA-NEN (executor claude)

- packet: #802 · lease `wp802-r1-g1-claude` (nhánh `ops/wp802-r1-g1-lease` @ `f6159dc4`) · spec `ops/specs/wp802.md`
  sha256 `e4fd84e1…00e0` (đo lại khớp) · nhánh `agent/wp802-g1-claude` rẽ từ `de82ef74`.
- Trước khi sửa: lượt `ops-publish-lease.yml` 39092181024 (lease) và 39092090057 (bia mộ) đều `success`; `ai-dang-giu`
  cho cả 6 đường dẫn sau khi so tập ref (máy chủ 596 ↔ cục bộ 596, thiếu 0) ⇒ `NGƯỜI_GIỮ 1: wp802-r1-g1-claude`.

## Đã làm (M1–M8)

| M | tệp | việc |
|---|---|---|
| M1 | `launcher.py` | `_AP_DUNG_BI_CHE = {rg, git}`; phần tử 0 của `_cac_duong_dan` (bản tên trần) đo HỎNG mà có bản sau chạy được ⇒ `trang_thai: BI_CHE` + `bi_che{ban_hong, loi, ban_tot, cach_chua}`, vào `thieu_bat_buoc` (thoát 12), `co` giữ True. Quá hạn ở phần tử 0 KHÔNG tính (`None ≠ False`). Bản chữ in `BI_CHE`, hai đường dẫn, cách chữa. |
| M2 | `launcher.py` | gợi ý Windows = `winget … -e --accept-source-agreements --accept-package-agreements --disable-interactivity \|\| choco install ripgrep --yes --no-progress` |
| M3 | hook | `co rg` → `co_chay rg` trước nhánh cargo |
| M4 | hook | `uname -s` khớp `MINGW*\|MSYS*\|CYGWIN*` ⇒ không installer nào; in cảnh báo + ĐÚNG MỘT dòng `$RG_CAI_WINDOWS` |
| M5 | `ops/cong_cu.yaml` | `rg.cai.windows` = cùng lệnh; dòng cuối `dirname "$(command -v rg \|\| cygpath -u "$LOCALAPPDATA/Microsoft/WinGet/Links/rg.exe")"` vì shim winget chưa có trong PATH của bash đang chạy |
| M6 | `launcher_test.py` | 7 ca `r802_*` + 9 đột biến (6 `DOT_BIEN`, 3 `DOT_BIEN_HOOK` mới — bản sao tạm của hook, chỉ `TinHieuChotCa` mới tính giết) |

Cờ phi tương tác của winget (Q6): `--accept-source-agreements --accept-package-agreements --disable-interactivity`.
Đổi tên ca: spec đề xuất `wp802_*`; `t116` đòi `^def [tr]\d+_` ⇒ dùng `r802_*` (tên đột biến giữ `wp802_*`).
`t106` ghim ĐÚNG hành vi cũ mà Q2 đổi (rg đầu hỏng ⇒ rc 0) — nay đòi `BI_CHE` + rc 12, vẫn giữ phép lùi sang bản tốt và thứ tự probe.
Hook: thêm `rg-windows-khong-tu-cai rg-co-chay-truoc-cargo` vào dòng `hook-nang-luc`.
Bốn neo đột biến cũ đổi theo dòng đã sửa (`doctor_luon_xanh`, `doctor_bo_qua_auth_hong`, `doctor_chi_thu_binary_dau`, `doctor_text_gop_CHUA_DO_thanh_THIEU`) — cùng ý, neo mới.

## Phép đo (Linux, container phiên, `core.abbrev 7`)

| N | ca / phép đo | kết quả |
|---|---|---|
| N1 | `r802_doctor_rg_tran_hong_la_BI_CHE` (tệp thật) | qua; đột biến `wp802_bo_nhanh_BI_CHE`, `wp802_BI_CHE_khong_vao_thieu` giết 2/2 |
| N2 | `r802_doctor_rg_chi_ban_tot_khong_BI_CHE` | qua; `wp802_luon_BI_CHE_khi_co_ung_vien` giết 1/1 |
| N3 | `r802_doctor_git_tran_hong_la_BI_CHE` | qua; `wp802_bo_git_khoi_tap_ap_dung` giết 1/1 |
| N4 | `r802_doctor_bash_ngoai_pham_vi_BI_CHE` | qua; `wp802_BI_CHE_moi_cong_cu` giết 1/1 |
| N6 | `r802_bang_cai_rg_khop_cong_cu_yaml` (cắt ở ` && dirname `, đúng một lần; thiếu PyYAML ⇒ ĐỎ) | qua; `wp802_launcher_winget_thanh_choco` + `wp802_hook_lenh_windows_lech_yaml` giết |
| N7 | `r802_hook_linux_rg_hong_van_thu_cargo` (khối rg của hook, nhật ký từng lời gọi) | qua; `wp802_hook_co_thay_co_chay` giết 1/1 |
| N8 | `r802_hook_windows_khong_cai_in_dung_lenh` | qua; `wp802_hook_windows_roi_vao_apt` giết 1/1 |
| N10 | `launcher_test.py` không biến / với `CODEX_AUTH_JSON` giả | **228/228** cả hai (tổng 230, bỏ qua 2 — cùng hai ca bỏ qua với master `de82ef74`: 221/221) · `--dot-bien` **259/259** (4 không đo được trên nền này, như master) |
| N11 | ruff F | 5 F841 = master 5 ⇒ delta 0 · `bash_nen quet` ĐẠT · `doctrine-scan` rc 0 · `bash -n` ok |

Mọi giết của `wp802_*` ra tên ca TRẦN, tức `TinHieuChotCa` (runner sản phẩm in `(AssertionError:…)`/`(Kiểu)` cho các đường khác).

## Chưa đo / còn mở

- N5, N9: chờ lượt `workflow_dispatch` `launcher-windows.yml` + `ci.yml` trên exact head (ghi ở PR).
- Vế nào của `winget … || choco …` chạy trên `windows-latest`: đọc từ log N9 nếu có.
- Ca WindowsApps THẬT: `chua_do_duoc` (spec). N7/N8 chỉ POSIX ⇒ ba đột biến hook là KHÔNG ĐO ĐƯỢC trên Windows.
- `||` không chạy trong Windows PowerShell 5.1: gợi ý `doctor` dán vào PS 5.1 sẽ lỗi cú pháp (cmd/PS7/Git Bash chạy được). Theo Q6 nguyên văn; chưa sửa.
- N12 (`release-verify` lane WORKER): đọc trên CI của PR.
