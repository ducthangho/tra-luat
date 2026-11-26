# Handoff §7 — wp1463 lượt 5/5 (lease `wp1463-r17-g5-claude`)

Việc gỡ đã xong và commit cục bộ, **chưa push**. H qua các Nghiệm thu 1, 2, 3, 5, 6, 7, 9 và phần tại chỗ của Nghiệm thu 8; phần CI của Nghiệm thu 8 chưa đo vì H chưa đẩy. Handoff này chưa đăng lên Issue #1463 (GitHub MCP không kết nối được, HTTP 401) — điều phối cần đăng hộ.

## Định danh và kích thước

| | |
|---|---|
| H | `d84f45c1b4a346d6c9c17da0ba9579a7d0fcc7c5` |
| cây H | `22b64e981758e5c7fb2e5cbd4ecfcb8be31d53b0` |
| base | `1260fa0cba89353911e2f97188b2c04dab8139d7` |
| nhánh | `agent/wp1463-r17-g5-fable`, từ `02ebcea` (cây `f15aac5…`, khớp `start_from_tree`) |
| commit | `95fc954` (do_pr2.py) → `d84f45c` (KET_QUA.md) |
| đặc tả | sha256 `2848e163…81d8` khớp; prompt sha256 `51ed6c90…` khớp lease |

`git diff --numstat 1260fa0 H`:

| tệp | thêm | bớt |
|---|---|---|
| `.claude/dev/ci_dang_ky_test.py` | 11 | 4 |
| `ops/ci_provenance_test.py` | 606 | 74 |
| `ops/specs/wp1463-r1/do/KET_QUA.md` | 161 | 0 |
| `ops/specs/wp1463-r1/do/do_pr2.py` | 372 | 0 |
| **tổng: 4 tệp** | **+1150** | **−78** |

Trong trần: 4 ≤ 6 tệp, 1150 ≤ 2100, và 1150 < 1905 của `02ebcea`. Diff chỉ gồm đúng bốn tệp của write set; cây làm việc sạch.

## Hai tệp test byte-identical với `02ebcea`

- `git diff --quiet 02ebcea H -- ops/ci_provenance_test.py` ⇒ rc 0; blob `89213e00…` ở cả hai; sha256 `8eaa12ea…db81f`.
- `git diff --quiet 02ebcea H -- .claude/dev/ci_dang_ky_test.py` ⇒ rc 0; blob `30ef8bd6…` ở cả hai; sha256 `92516f3f…834d2`.

## Nghiệm thu 4 "Gỡ sạch"

- **(a)** Phép grep của đặc tả trên `do_pr2.py` ra **0 dòng** (grep rc 1). `python3 -B do_pr2.py vung` in cách dùng, **rc 2**.
- **(b)** `ab` và `registry` chạy bộ bằng `chay_bo`, không đổi.
- **(c)** Đúng một dòng `GIOI_HAN_PR2: …` ngay trước `KET_LUAN_…` ở cả bốn đầu ra thật (`ab`, `registry`, `tu-kiem`, `tu-kiem --dot-bien`).
- **(d)** Chuỗi tài liệu đầu tệp chỉ còn ba lệnh con và nêu cùng giới hạn.
- **(e)** Giữ đúng sáu ca và bốn đột biến của bộ chạy, cùng toàn bộ phần bộ so (danh sách ở dưới).
- Không còn tên mức module nào không được dùng (đo bằng `ast`); ba import `select`, `shutil`, `signal` đã gỡ theo.

## Dòng kết luận từng Nghiệm thu

`ab` chạy trên `95fc954`; H chỉ khác commit ấy ở `KET_QUA.md`. Ba lệnh nhẹ chạy lại trên H cho đầu ra giống từng byte bản trong `KET_QUA.md`.

| Nghiệm thu | Kết quả |
|---|---|
| 1 | H đủ: `CA: 86/86 dat` · `DOT BIEN: 524/524 bi giet dung ly do` · `TU KIEM PHAN HANG: DAT (2 dot bien)` · `TONG: DAT`, rc 0. H nhẹ: `CA: 86/86 dat` · `DOT BIEN: 524 muc CHE DO NHE — do khi diff cham vung` · `TONG: DAT`, rc 0. Có `actionlint` 1.7.7 và `shellcheck` 0.9.0. |
| 2 | `KET_LUAN_AB: DAT (9/9 phep dung)`, rc 0; `RC_LUOT: base/day_du=0 · H/day_du=0 · H/nhe=0`; base 485 việc, H 524 việc, tên base ⊆ H. |
| 3 | `KET_LUAN_REGISTRY: DAT`, rc 0; bốn tổ hợp ra ĐẠT/ĐẠT/ĐỎ/ĐỎ đúng kỳ vọng. |
| 5 | base đủ 718,6 s · H đủ 655,7 s · H nhẹ 152,8 s · `TIEN TRINH: 4` · 4 CPU. |
| 6 | 524/524 việc `hoan_tat`/`giet` trong `KET_CUC_A3` của lượt đủ thật. T8, T18, T19 (đích `c66`) và T47, T48 (đích `c82`) đều `giet`. 42 mục `T*` và 13 mục `D*` (D01, D1–D12) đều `giet`. |
| 7 | Ca `c85_vung_va_env_registry_that` `passed` trong lượt thật; `--mot-ca` trên H rc 0. |
| 8 (tại chỗ) | `python3 .claude/dev/ci_dang_ky_test.py` trên H: `PHẢN CHỨNG: 1677/1677 đỏ đúng` · `TỔNG: ĐẠT`, rc 0. `git diff --check` rc 0. |
| 9 | `KET_QUA.md` viết lại: bốn khối đầu ra thật, 0 dòng khớp bốn chuỗi cấm, đúng một mục `## Giới hạn`, không ghi SHA hay cây của H. |
| `tu-kiem` | `TU_KIEM_SO: 26/26 dat` · `TU_KIEM_CHAY: 6/6 dat` · `KET_LUAN_TU_KIEM: DAT`, rc 0. |
| `tu-kiem --dot-bien` | `DOT_BIEN_TU_KIEM: 19/19 bi bat dung cho (15 cua bo so, 4 cua bo chay)` · `KET_LUAN_TU_KIEM: DAT`, rc 0. |

Không hồi quy ở phần giữ lại: 52 dòng `SO`, `TU_KIEM_SO`, `DB_SO`, `CHAY ab/registry`, `DB_CHAY ab/registry` giống hệt bản trong `KET_QUA.md` của `02ebcea`. Với bốn đột biến bộ chạy, tôi đo thêm bằng script nháp ngoài kho: dưới mỗi đột biến, ca lệch duy nhất là đúng ca đích.

## Ca và đột biến

**Còn giữ**
- Bộ so: 26 đầu vào (`nen_khoe`, 8 đầu vào a–c, 5 đầu vào d, 3 đầu vào e, 2 đầu vào dương, 7 đối chứng d).
- `DOT_BIEN_SO`: 15 (chín `go_<phép>` và sáu `d_…`).
- Bộ chạy, sáu ca: `ab_rc0_doi_chung`, `ab_rc42_base_day_du`, `ab_rc42_H_day_du`, `ab_rc42_H_nhe`, `registry_tu_rc0_doi_chung`, `registry_tu_rc42_luot_nhe`.
- `DOT_BIEN_CHAY`, bốn: `ab_bo_chot_rc_luot_base_day_du`, `ab_bo_chot_rc_luot_H_day_du`, `ab_bo_chot_rc_luot_H_nhe`, `registry_tu_mac_dinh_rc_0`.

**Đã gỡ**
- Toàn bộ `tu_kiem_vung` (155 đầu vào): các họ `thuan_*` và `that_*`, gồm cả các ca `la_python` và `lk_*`.
- `DOT_BIEN_VUNG`, 19 đột biến:
  - `probe_dung_rieng_dung_nhan_chung_cua_bo`, `hop_tap_luot_du_vao_quan_sat_rong_cua_probe`, `bo_chot_song`
  - `khong_lan_truyen_hook_sang_tien_trinh_con`, `giai_dir_fd_theo_cwd`, `chi_khop_duong_dan_theo_chu`, `bo_dem_python_con`, `bo_rc`
  - `tap_phep_chi_so_so_luong`, `chay_mot_phep_hai_lan_thay_cho_phep_khac`, `bo_so_mot_hang_nhung_van_dem`, `phep_go_chay_ban_nap_cua_phep_khac`, `go_khong_go_khoa`
  - `phan_loai_bo_realpath`, `phan_loai_nhan_moi_ten`, `hook_chi_cai_theo_ten_trinh_thong_dich`
  - `la_python_giai_lai_theo_cwd_bo_doc`, `hook_bo_qua_cwd_rieng_cua_loi_goi`, `hook_khong_do_PATH_cua_loi_goi`
- Tám ca của bộ quan sát, tiền tố `quan_sat_`:
  - `khoe_doi_chung`
  - `qua_han_con_va_chau_khong_de_dau`
  - `ngat_goc_da_thoat_chau_bo_qua_TERM_khong_de_dau`
  - `ngat_lan_nua_giua_luc_don_van_don_het`
  - `tra_binh_thuong_chau_cung_nhom_da_dong_ong_khong_de_dau`
  - `khong_xac_nhan_duoc_nhom_da_het_la_khong_do_duoc`
  - `mat_ghim_khong_ban_tin_hieu_va_khong_do_duoc`
  - `chau_tu_setsid_giu_ong_DON_KHONG_HET_chi_ghi_gioi_han`
- Tám đột biến của bộ quan sát, tiền tố `quan_sat_`: `bo_buoc_don`, `chi_ket_thuc_con_khong_ket_thuc_nhom`, `bo_don_o_duong_ngat`, `bo_buoc_KILL`, `bo_don_tiep_khi_bi_ngat_lan_nua`, `bo_don_o_duong_tra_binh_thuong`, `bo_nhanh_DON_KHONG_HET`, `ban_tin_hieu_khi_mat_ghim`.
- Mã đi kèm: lệnh con `vung`, mã hook và probe, bảng fixture cùng `Z`/`GOC`/`oracle`, bộ đọc nhật ký và bộ phân loại ba phép, bộ chạy có nhóm tiến trình riêng cùng các hàm dọn, cây giả của tự kiểm, và các dòng giới hạn/kết luận của vùng.

## Ruff

`python3 -m ruff check --no-cache --select F` (ruff 0.15.15):
- Trên H, ba tệp `.py`: 0 lỗi.
- Trên base, hai tệp test: 0 lỗi (`do_pr2.py` không có ở base).
- **Delta = 0.**

## Chưa đo được

- CI PR Ubuntu trên H, K7 (`ci-dot-bien-du.yml`), Windows / dòng miễn M3, Nghiệm thu 10 sau merge.
- Vùng của bộ trên H và việc dọn tiến trình con khi `ab`/`registry` bị ngắt hay hết giờ: PR2 không đo, chuyển `NO-PR2-DO-CAP-HDH`.
- `ab` trên đúng SHA H: chỉ đo trên `95fc954`, vì `KET_QUA.md` nằm trong H.
- `registry` không kèm `--tu` (tự chạy bộ): lượt này chỉ chạy dạng `--tu`.
- Với 15 đột biến bộ so, "đúng lý do" chỉ được đo theo tiêu chí của chính bộ chạy (lệch ở đúng phép bị gỡ hoặc bị đổi); tôi không đo thêm bằng thước độc lập.
- Đường gọi (api hay subscription) mà lease yêu cầu ghi: tôi chỉ quan sát được `ANTHROPIC_API_KEY` có đặt trong phiên (kiểm sự tồn tại, không đọc giá trị), không xác nhận được đường tính phí.

## Chỗ đặc tả chưa rõ và cách tôi đã hiểu

1. **Ghi chú trong `KET_QUA.md`.** Prompt nói "chỉ đầu ra thật", nhưng Nghiệm thu 2 giao cho tệp này ghi tập khai nhóm (a) "cùng lý do", và các bản lượt 2–4 chưa từng có phần lý do. Tôi giữ ba gạch đầu dòng lý do và hai dòng chú giải cách đọc. Nếu chủ kho muốn tệp chỉ có đầu ra thì xoá đúng các dòng ấy.
2. **Hai khối `tu-kiem`.** Tôi chép đầu ra của cả `tu-kiem` lẫn `tu-kiem --dot-bien` thành hai khối riêng, dù khối sau in lại trọn khối trước (bản cũ gộp làm một).
3. **`GIOI_HAN_PR2` ở đường lỗi của `ab`.** Khi clone hoặc checkout hỏng, lệnh vẫn in một dòng `KET_LUAN_AB: KHONG_DO_DUOC`, nên tôi in dòng giới hạn trước nó. Đã đo: rc 3, đúng một dòng.
4. **Kết quả cổng kho và ruff.** Mục "Ngoài năm lệnh con" của bản cũ không còn trong `KET_QUA.md`; hai kết quả ấy nằm ở handoff này, theo câu của Nghiệm thu 9 về bản ghi cần SHA của H.
5. **"T1–T48".** Lượt thật có 42 mục `T*` (số chạy tới 48, không liền) và 13 mục `D*`; tôi báo số đo được, không khẳng định có đủ 48 mục.

```yaml
schema_version: 1
packet_id: wp1463
generation: 5
spec_hash: 2848e163bed43cdc825eaa1fa8add2f2820ddc011cb4e95f258b5e0649ec81d8
provider: claude
model_family: claude
execution_surface: claude_code
transport: machine/local
role: executor
base_sha: 1260fa0cba89353911e2f97188b2c04dab8139d7
head_sha: d84f45c1b4a346d6c9c17da0ba9579a7d0fcc7c5
status: needs_followup
changed_paths: [.claude/dev/ci_dang_ky_test.py, ops/ci_provenance_test.py, ops/specs/wp1463-r1/do/KET_QUA.md, ops/specs/wp1463-r1/do/do_pr2.py]
next_role: human
manual_next_action: chủ kho audit exact-H d84f45c trước lần đẩy đầu; sau đó review mã Codex lượt 4/4
remaining_work: [CI PR Ubuntu, K7, dòng miễn Windows M3, Nghiệm thu 10]
```