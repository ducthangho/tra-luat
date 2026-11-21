# WP1488 r1 — kết quả đo (executor: phiên `session_015GtxrazyAyLwN5BiEB52Sq`, Linux, 21-11-2026)

Base `8656dc0176ed108e12c209ba55c91a1f6f9d612f`. Mã đo lượt 1: `ab298a8`. Sau Codex lượt 1:
`b7a280eebb49fb16bf0b226e1f407eca191db097`; các commit sau nó chỉ đổi tệp hồ sơ. Đặc tả `ops/specs/wp1488-r1.md` sha256 `1661834f…c0c8`.

## 1. Tái hiện lỗi trên base (spec §1)

Bằng `_wp868_chay` (stub, không mạng), script của `8656dc0`:
- A: lượt đầu `apt-get install … && chon_thu_muc_chay_duoc rg <tot2> && false`, lượt thử lại qua stdout ⇒ rc 0, `DAT`,
  `$GITHUB_PATH` = `[<tot2>]`.
- B: `chon_thu_muc_chay_duoc rg <tot> && false` ⇒ rc 1, `$GITHUB_PATH` = `[<tot>]`.

## 2. Thay đổi

- `ops/cai_cong_cu.sh`:
  - Bộ chọn ghi dòng vào tệp chờ `"$KENH_KQ.github_path"`, không ghi thẳng `$GITHUB_PATH` (B1).
  - Sau vòng thử lại của #1479 và trước nhánh lỗi: nếu `RC_CAI = 0`, tệp chờ của `KENH_KQ` hiện hành khác rỗng,
    `$GITHUB_PATH` khác rỗng, và kênh CUỐI là `DICH` (`_tl1488_kenh_la_dich`, thêm sau Codex lượt 1), thì `cat` tệp chờ
    sang `$GITHUB_PATH`. Chép lỗi thì in dòng báo và đặt `RC_CAI=1` (B2/B3).
- `.claude/dev/launcher_test.py`:
  - Ca `r1488_github_path_chi_ghi_khi_thanh_cong`.
  - 10 đột biến `wp1488_sh_*` (6 ban đầu, 4 thêm sau Codex lượt 1).
  - `wp858_sh_nuot_loi_ghi_github_path` dời neo sang dòng chép (nuốt lỗi bằng `|| :`).
  - `r858_hinh_dang_cong_thuc_cai` neo dòng tệp chờ, chốt bộ chọn không còn `>> "$GITHUB_PATH"`, chốt nguyên khối chép.

## 3. Ca `r1488_github_path_chi_ghi_khi_thanh_cong` (N1)

Mỗi kịch bản chốt NGUYÊN BYTE của tệp `$GITHUB_PATH` (sau Codex lượt 1; trước đó so dòng sau khi strip).

| Kịch bản | Chốt |
|---|---|
| A: lượt đầu chọn `tot2` rồi lỗi, lượt thử lại qua stdout | rc 0, `DAT`, đã update, tệp = `""` |
| A': như A, lượt thử lại gọi bộ chọn tới thư mục tốt | tệp = `"<thư mục tốt>\n"` |
| B: công thức không apt gọi bộ chọn rồi `false` | rc khác 0, tệp = `""` |
| C: tiến trình nền của lượt đầu gọi bộ chọn tới `muon/`; `cat` giả đầu PATH phát dấu lúc script đọc kênh `kq-thu-lai-*` (sau khi lượt thử lại đã thoát, trước bước chép) và chờ writer ghi xong | fixture chốt `di` và `xong` đều có; rc 0, tệp = `"<thư mục tốt>\n"` |
| D: `--bat-buoc` thật, công cụ tuỳ chọn gọi bộ chọn rồi `false`, công cụ bắt buộc sau nó | rc 0, tệp = `"<thư mục công cụ bắt buộc>\n"` |
| E: `$GITHUB_PATH` trỏ vào một thư mục | rc khác 0, stderr có `khong ghi duoc $GITHUB_PATH` |
| F: tệp chờ là thư mục (`mkdir` trước bộ chọn) | rc khác 0, tệp = `""`, stderr có `khong ghi duoc tep cho cua $GITHUB_PATH` |
| G: bộ chọn ra `DICH`, công thức sửa `rg` đầu PATH rồi gọi lại ⇒ kết quả cuối `GIU_PATH` | rc 0, `DAT`, tệp = `""` |
| H: bộ chọn ra `DICH`, công thức làm rỗng kênh rồi in thư mục ⇒ rơi về stdout | rc 0, `DAT`, tệp = `""` |
| I: `--bat-buoc`, `$GITHUB_PATH` là thư mục, công cụ tuỳ chọn trước công cụ bắt buộc | rc khác 0; công cụ tuỳ chọn báo `--bat-buoc di tiep`; đúng hai dòng `khong ghi duoc $GITHUB_PATH` |

- `--lap-ca r1488_github_path_chi_ghi_khi_thanh_cong`: 3/3 trên `ab298a8`, 2/2 trên `b7a280e`.
- Phản chứng: với `ops/cai_cong_cu.sh` của master `8656dc0` ⇒ ĐỎ ở (A) (`'…/tot2\n'`); với script của `2847860`
  (head lượt 1) ⇒ ĐỎ ở (G) (`'…/goc/usr/bin\n'`).

## 4. Đột biến (N2)

Từng đột biến chạy riêng để đọc assertion. Mọi đột biến đều chết bằng `TinHieuChotCa`.

| Đột biến | Thay đổi | Chết ở |
|---|---|---|
| `wp1488_sh_bo_chon_ghi_thang` | bộ chọn ghi `>> "$GITHUB_PATH"` như cũ | (A) `[tot2]` |
| `wp1488_sh_chep_khong_xet_rc` | bỏ điều kiện `RC_CAI = 0` | (B) rc 1, `[tot]` |
| `wp1488_sh_tep_cho_luot_dau` | đọc tệp chờ của kênh lượt đầu `$TAM_CAI/kq.github_path` | (A') `tot2` |
| `wp1488_sh_chep_loi_khong_dat_rc` | chép lỗi mà không đặt `RC_CAI` | (E) rc 0 |
| `wp1488_sh_chep_hai_lan` | chép tệp chờ hai lần | (A') hai dòng |
| `wp1488_sh_bo_chon_nuot_loi_tep_cho` | bộ chọn nuốt lỗi ghi tệp chờ | (F) thiếu dòng báo đúng |
| `wp1488_sh_bo_xet_kenh_dich` | bỏ điều kiện kênh cuối là `DICH` | (G) |
| `wp1488_sh_tep_cho_dong_trang` | tệp chờ ghi `'%s\n\n'` | (A') dòng trắng thừa |
| `wp1488_sh_chep_loi_thoat_ngay` | chép lỗi ⇒ `exit 1` ngay (bỏ nhánh lỗi cũ) | (I) |
| `wp1488_sh_doc_tep_cho_cu_ghi_muon` | đọc thêm tệp chờ của lượt đầu CHỈ khi writer muộn đã ghi | (C) — chỉ ca C bắt được |
| `wp858_sh_nuot_loi_ghi_github_path` (neo mới) | chép lỗi bằng `\|\| :` | `r858_cai_linux…` (rc 0 khi `$GITHUB_PATH` hỏng) và `r858_hinh_dang…` |

`wp1488_sh_tep_cho_luot_dau` chết ở (A') trước khi tới (C): tệp chờ của lượt đầu cũng chứa thư mục hỏng. Bảng `cai_sh` (mọi
packet) chạy riêng trên `b7a280e`: 90/90.

## 5. Hồi quy (N3) — hai vế dựng cùng một lệnh (clone + checkout + `core.abbrev 7`)

`/tmp/.git` không tồn tại lúc đo.

| Phép đo | Base `8656dc0` | Head `ab298a8` |
|---|---|---|
| `launcher_test.py` | 452/452 (tổng 454, bỏ qua 2) | `ab298a8`, `b7a280e`: 453/453 (tổng 455, bỏ qua 2) |
| `launcher_test.py --dot-bien` | 782/782 (7 không đo được trên nền này) | `ab298a8`: 788/788 · `b7a280e`: 792/792 (cùng 7) |

Hai ca bỏ qua (`t62_…`, `r484_g4_windows_sid_alias_identity`) và 7 đột biến không đo được (nhánh Windows) giống hệt nhau
ở mọi vế. Delta trên `b7a280e` = +1 ca, +10 đột biến, 0 hồi quy.

Các ca `r831_* r858_* r868_* r1045_* r1404_* r1479_*` chạy riêng: base 34/34. Bản dựng thử, trước khi sửa ca hình dạng:
33/34; ca đỏ duy nhất là `r858_hinh_dang_cong_thuc_cai`.

## 6. Khác

- `python .claude/dev/packet_loop.py doctrine-scan --root .`: sạch (12 tệp), rc 0.
- CI của PR ducthangho/tra-luat#1489 và review Codex (N4, N5): `VERDICT.md`.

## 7. Không đo được

- Runner CI thật với `$GITHUB_PATH` của GitHub Actions: chỉ đo bằng tệp giả.
- macOS/Windows thật: bộ chọn `--win` đi qua `cygpath -w` như cũ trước khi ghi tệp chờ; ca `r858_cai_windows…` (cygpath
  giả trên Linux) đạt, nhưng chưa chạy trên Windows thật.
