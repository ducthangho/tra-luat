# WP1488 — kết quả đo (executor: phiên `session_015GtxrazyAyLwN5BiEB52Sq`, Linux, 21-11-2026)

Base `8656dc0176ed108e12c209ba55c91a1f6f9d612f`. Đặc tả hiện hành: `ops/specs/wp1488-r2.md` (sha256 `692325c7…add0`),
lease `wp1488-r2-g2-claude`. Mã r1 đã đo: `ab298a8`, `b7a280e`. Mã r2: `42b5386dc519d6e0a49e98e301b08539e2be4e0a`; các commit
sau nó chỉ đổi tệp hồ sơ.

## 1. Tái hiện lỗi trên base

Bằng `_wp868_chay` (stub, không mạng), script của `8656dc0`:
- A: lượt đầu `apt-get install … && chon_thu_muc_chay_duoc rg <tot2> && false`, lượt thử lại qua stdout ⇒ rc 0, `DAT`,
  `$GITHUB_PATH` = `[<tot2>]`.
- B: `chon_thu_muc_chay_duoc rg <tot> && false` ⇒ rc 1, `$GITHUB_PATH` = `[<tot>]`.

## 2. Thay đổi (r2)

- `ops/cai_cong_cu.sh`:
  - Bộ chọn không ghi `$GITHUB_PATH`; nó ghi tệp chờ `"$KENH_KQ.github_path"` hai dòng: (1) đường dẫn POSIX đã chọn,
    (2) dòng sẽ thêm (đã `cygpath -w` trên Windows) (B1).
  - Sau vòng thử lại của #1479, khi `RC_CAI = 0`: đọc kênh ĐÚNG MỘT LẦN (lỗi ⇒ 7); nếu kết quả là `DICH`,
    `_tl1488_chep_github_path` đọc tệp chờ một lần và thêm dòng (2) vào `$GITHUB_PATH` chỉ khi dòng (1) bằng `DICH`; khác
    thì cảnh báo, không ghi. Lỗi đọc tệp chờ/ghi `$GITHUB_PATH` ⇒ `RC_CAI=1`, đi nhánh lỗi cũ (B2/B3). Phân nhánh PATH bên
    dưới dùng chính `KQ` ấy; lệnh `cat -- "$KENH_KQ"` chỉ còn một chỗ.
- `.claude/dev/launcher_test.py`:
  - Ca `r1488_github_path_chi_ghi_khi_thanh_cong` (A, A', B, C, D, E, F, G, H, I, J, K1, K2).
  - 12 đột biến `wp1488_sh_*`; `wp858_sh_nuot_loi_ghi_github_path` dời neo sang dòng ghi trong `_tl1488_chep_github_path`.
  - `r858_hinh_dang_cong_thuc_cai` chốt dòng tệp chờ mới, bộ chọn không còn `>> "$GITHUB_PATH"`, khối đọc kênh duy nhất
    và đúng một `cat -- "$KENH_KQ"`.

## 3. Ca `r1488_github_path_chi_ghi_khi_thanh_cong` (N1)

Kịch bản có tệp đích chốt NGUYÊN BYTE bằng `read_bytes()` (bắt CRLF, dòng trắng). E và I (đích là thư mục) chốt rc và stderr.

| Kịch bản | Chốt |
|---|---|
| A: lượt đầu chọn `tot2` rồi lỗi, lượt thử lại qua stdout | rc 0, `DAT`, đã update, tệp = `b""` |
| A': như A, lượt thử lại gọi bộ chọn tới thư mục tốt | tệp = `b"<thư mục tốt>\n"` |
| B: công thức không apt gọi bộ chọn rồi `false` | rc khác 0, tệp = `b""` |
| C: tiến trình nền của lượt đầu gọi bộ chọn tới `muon/`; `cat` giả đầu PATH khớp ĐÚNG `cat -- <…>/kq-thu-lai-1` (lần đọc kênh cuối, sau khi lượt thử lại đã thoát), phát dấu rồi chờ writer ghi xong | fixture chốt móc ĐÃ kích hoạt (không thì báo "điểm đồng bộ đã đổi") và writer ĐÃ ghi; rc 0, tệp = `b"<thư mục tốt>\n"` |
| D: `--bat-buoc` thật, công cụ tuỳ chọn gọi bộ chọn rồi `false`, công cụ bắt buộc sau nó | rc 0, tệp = `b"<thư mục công cụ bắt buộc>\n"` |
| E: `$GITHUB_PATH` trỏ vào một thư mục | rc khác 0, stderr có `khong ghi duoc $GITHUB_PATH` |
| F: tệp chờ là thư mục (`mkdir` trước bộ chọn) | rc khác 0, tệp = `b""`, stderr có `khong ghi duoc tep cho cua $GITHUB_PATH` |
| G: bộ chọn ra `DICH`, công thức sửa `rg` đầu PATH rồi gọi lại ⇒ kết quả cuối `GIU_PATH` | rc 0, `DAT`, tệp = `b""` |
| H: bộ chọn ra `DICH`, công thức làm rỗng kênh rồi in thư mục ⇒ rơi về stdout | rc 0, `DAT`, tệp = `b""` |
| I: `--bat-buoc`, `$GITHUB_PATH` là thư mục, công cụ tuỳ chọn trước công cụ bắt buộc | rc khác 0; công cụ tuỳ chọn báo `--bat-buoc di tiep`; đúng hai dòng `khong ghi duoc $GITHUB_PATH` |
| J: bộ chọn ghi tệp chờ cho X, công thức tự ghi `DICH` cho Y (rg 9.9.9) | rc 0, `DAT`, JSON có `9.9.9` (PATH nội bộ dùng Y), tệp = `b""`, có cảnh báo `khong khop DICH cuoi` |
| K1: `cat` của lần đọc kênh in đủ nội dung rồi trả 9 | rc 7, tệp = `b""`, stderr `khong doc duoc kenh ket qua` |
| K2: `cat` của lần đọc kênh đầu trả 9 không in gì (lần sau, nếu có, đọc được) | rc 7, tệp = `b""` |

- `--lap-ca r1488_github_path_chi_ghi_khi_thanh_cong`: 3/3 trên `ab298a8`, 2/2 trên `b7a280e`, 2/2 trên `42b5386`.
- Phản chứng: script của master `8656dc0` ⇒ ĐỎ ở (A); script `2847860` (head r1 lượt 1) ⇒ ĐỎ ở (G); script `b7a280e`
  (head r1 lượt 2) ⇒ ĐỎ ở (J).

## 4. Đột biến (N2)

Từng đột biến chạy riêng để đọc assertion. Mọi đột biến đều chết bằng `TinHieuChotCa`.

| Đột biến | Thay đổi | Chết ở |
|---|---|---|
| `wp1488_sh_bo_chon_ghi_thang` | bộ chọn ghi `>> "$GITHUB_PATH"` như cũ | (A) |
| `wp1488_sh_chep_khong_xet_rc` | đọc kênh và chép cả khi `RC_CAI ≠ 0` | (B) |
| `wp1488_sh_tep_cho_luot_dau` | đọc tệp chờ của kênh lượt đầu `$TAM_CAI/kq.github_path` | (A') |
| `wp1488_sh_chep_loi_khong_dat_rc` | bỏ `\|\| RC_CAI=1` ở lời gọi chép | (I) |
| `wp1488_sh_chep_hai_lan` | thêm dòng hai lần | (A') |
| `wp1488_sh_bo_so_danh_tinh` | bỏ so dòng (1) với `DICH` | (J) |
| `wp1488_sh_dong_trang` | thêm `'%s\n\n'` | (A') |
| `wp1488_sh_tep_cho_crlf` | tệp chờ ghi CRLF ở dòng (2) | (A') |
| `wp1488_sh_chep_loi_thoat_ngay` | lỗi chép ⇒ `exit 1` ngay (bỏ nhánh lỗi cũ) | (I) |
| `wp1488_sh_doc_tep_cho_cu_ghi_muon` | đọc tệp chờ của lượt đầu CHỈ khi writer muộn đã ghi | (C) — chỉ ca C bắt được |
| `wp1488_sh_doc_kenh_rieng_truoc` | dựng lại thứ tự r1: quyết định chép bằng một lần đọc kênh RIÊNG trước lần đọc có xét lỗi | (K1) |
| `wp1488_sh_bo_chon_nuot_loi_tep_cho` | bộ chọn nuốt lỗi ghi tệp chờ | (F) |
| `wp858_sh_nuot_loi_ghi_github_path` (neo mới) | lỗi ghi `$GITHUB_PATH` bị nuốt bằng `\|\| :` | `r858_cai_linux…` và `r858_hinh_dang…` |

Ghi chú đo được:
- `wp1488_sh_chep_loi_khong_dat_rc` chết ở (I), không ở (E). Ở lời gọi trực tiếp, hàm trả 1 không kèm `||` thì `set -e` cũng
  thoát 1, nên (E) không phân biệt được; chỉ lượt `source` (I) phân biệt đường `RC_CAI` với errexit.
- Giới hạn chỉ `DICH` mới gọi hàm chép và phép so dòng (1) với `DICH` chồng nhau: bỏ riêng giới hạn `DICH` là đột biến
  tương đương (với `GIU_PATH`/kênh rỗng, dòng (1) không bao giờ bằng giá trị truyền vào), nên bảng không có đột biến ấy.
- Bảng `cai_sh` (mọi packet) chạy riêng: 90/90 trên `b7a280e`, 92/92 trên `42b5386`.

## 5. Hồi quy (N3) — các vế dựng cùng cách (clone + checkout + `core.abbrev 7`)

`/tmp/.git` không tồn tại lúc đo.

| Phép đo | base `8656dc0` | head |
|---|---|---|
| `launcher_test.py` | 452/452 (tổng 454, bỏ qua 2) | `ab298a8`, `b7a280e`, `42b5386`: 453/453 (tổng 455, bỏ qua 2) |
| `launcher_test.py --dot-bien` | 782/782 (7 không đo được trên nền này) | `ab298a8`: 788/788 · `b7a280e`: 792/792 · `42b5386`: 794/794 (cùng 7) |

Hai ca bỏ qua (`t62_…`, `r484_g4_windows_sid_alias_identity`) và 7 đột biến không đo được (nhánh Windows) giống hệt nhau
ở mọi vế. Delta trên `42b5386` = +1 ca, +12 đột biến, 0 hồi quy.

Các ca `r831_* r858_* r868_* r1045_* r1404_* r1479_*` chạy riêng: base 34/34; bản dựng thử r1 và r2, trước khi sửa ca hình
dạng: 33/34, ca đỏ duy nhất là `r858_hinh_dang_cong_thuc_cai`.

## 6. Khác

- `python .claude/dev/packet_loop.py doctrine-scan --root .`: sạch (12 tệp), rc 0.
- CI của PR ducthangho/tra-luat#1489 và review Codex (N4, N5): `VERDICT.md`.

## 7. Không đo được

- Runner CI thật với `$GITHUB_PATH` của GitHub Actions: chỉ đo bằng tệp giả.
- macOS/Windows thật: bộ chọn `--win` đi qua `cygpath -w` như cũ trước khi ghi dòng (2) của tệp chờ; ca `r858_cai_windows…`
  (cygpath giả trên Linux) đạt, nhưng chưa chạy trên Windows thật.
