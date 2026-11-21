# WP1488 — kết quả đo (executor: phiên `session_015GtxrazyAyLwN5BiEB52Sq`, Linux, 21-11-2026)

Base `8656dc0176ed108e12c209ba55c91a1f6f9d612f`. Đặc tả hiện hành: `ops/specs/wp1488-r3.md` (sha256 `691a710c…16d7`),
lease `wp1488-r3-g3-claude`. Mã r1 đã đo: `ab298a8`, `b7a280e`; mã r2: `42b5386`; mã r3: `f8747c4`. Mã r3 sau Codex
lượt 4 (hai P3): `7a8823b890ff09f8eb98c75e7bc10fc9f963b37a`; các commit sau nó chỉ đổi tệp hồ sơ.

## 1. Tái hiện lỗi trên base

Bằng `_wp868_chay` (stub, không mạng), script của `8656dc0`:
- A: lượt đầu `apt-get install … && chon_thu_muc_chay_duoc rg <tot2> && false`, lượt thử lại qua stdout ⇒ rc 0, `DAT`,
  `$GITHUB_PATH` = `[<tot2>]`.
- B: `chon_thu_muc_chay_duoc rg <tot> && false` ⇒ rc 1, `$GITHUB_PATH` = `[<tot>]`.

## 2. Thay đổi (r3)

- `ops/cai_cong_cu.sh`:
  - Bộ chọn chỉ ghi kênh kết quả: không ghi `$GITHUB_PATH`, không tệp chờ, không `cygpath -w` (B1).
  - Sau vòng thử lại của #1479, khi `RC_CAI = 0`: đọc kênh ĐÚNG MỘT LẦN (lỗi ⇒ 7), `export -n KQ`. Nếu kết quả là `DICH`,
    `_tl1488_ghi_github_path` dựng dòng từ chính `DICH` ấy (đổi `cygpath -w` khi `LENH` gọi `chon_thu_muc_chay_duoc --win`),
    từ chối khi có `\n`/`\r` hoặc dòng rỗng, rồi thêm đúng một lần. Đầu ra `cygpath -w` đọc qua sentinel `x` và chỉ bỏ
    đúng một LF kết thúc dòng (Codex lượt 4), nên LF thừa ở đuôi không bị `$( )` ăn mất trước chốt. Từ chối/`cygpath -w` lỗi/ghi lỗi ⇒ `RC_CAI=1`, đi nhánh
    lỗi cũ (B2/B3). Hàm được `export -nf`. Phân nhánh PATH bên dưới dùng chính `KQ` ấy; `cat -- "$KENH_KQ"` và
    `>> "$GITHUB_PATH"` mỗi thứ chỉ còn một chỗ.
- `.claude/dev/launcher_test.py`:
  - Ca `r1488_github_path_chi_ghi_khi_thanh_cong` (A, A', B, C, D, E, G, H, I, J, L-LF, L-CR, M, W-rong, W-du-lf, W-cr,
    K1, K2, K3).
  - 16 đột biến `wp1488_sh_*`. Ba đột biến `wp858_sh_*` (`nuot_loi_cygpath_w`, `github_path_khong_qua_cygpath`,
    `github_path_vang_khong_mac_dinh`) và `wp858_sh_nuot_loi_ghi_github_path` dời neo sang `_tl1488_ghi_github_path`.
  - `cygpath` giả: khi `CYGPATH_W_HONG` thì IN đường rồi mới thoát 37 (đo việc xét mã thoát); thêm `CYGPATH_W_RONG`
    (rc 0, không in gì) và `CYGPATH_W_KIEU=du_lf|cr` (rc 0, thừa một LF ở đuôi / CR trước LF).
  - `r858_hinh_dang_cong_thuc_cai`: phần mã (bỏ chú thích) của bộ chọn không chứa `GITHUB_PATH`/`github_path`/`cygpath -w`;
    hàm mới có đủ các chốt; khối đọc kênh duy nhất; đúng một `cat -- "$KENH_KQ"` và một `>> "$GITHUB_PATH"`.

## 3. Ca `r1488_github_path_chi_ghi_khi_thanh_cong` (N1)

Kịch bản có tệp đích chốt NGUYÊN BYTE bằng `read_bytes()`. E và I (đích là thư mục) chốt rc và stderr.

| Kịch bản | Chốt |
|---|---|
| A: lượt đầu chọn `tot2` rồi lỗi, lượt thử lại qua stdout | rc 0, `DAT`, đã update, tệp = `b""` |
| A': như A, lượt thử lại gọi bộ chọn tới thư mục tốt | tệp = `b"<thư mục tốt>\n"` |
| B: công thức không apt gọi bộ chọn rồi `false` | rc khác 0, tệp = `b""` |
| C: tiến trình nền của lượt đầu gọi bộ chọn tới `muon/`; `cat` giả khớp ĐÚNG `cat -- <…>/kq-thu-lai-1` (lần đọc kênh cuối, sau khi lượt thử lại đã thoát), phát dấu rồi chờ writer ghi xong | fixture chốt móc ĐÃ kích hoạt và writer ĐÃ ghi; rc 0, tệp = `b"<thư mục tốt>\n"` |
| D: `--bat-buoc` thật, công cụ tuỳ chọn gọi bộ chọn rồi `false`, công cụ bắt buộc sau nó | rc 0, tệp = `b"<thư mục công cụ bắt buộc>\n"` |
| E: `$GITHUB_PATH` trỏ vào một thư mục | rc khác 0, stderr có `khong ghi duoc $GITHUB_PATH` |
| G: bộ chọn ra `DICH`, công thức sửa `rg` đầu PATH rồi gọi lại ⇒ kết quả cuối `GIU_PATH` | rc 0, `DAT`, tệp = `b""` |
| H: bộ chọn ra `DICH`, công thức làm rỗng kênh rồi in thư mục ⇒ rơi về stdout | rc 0, `DAT`, tệp = `b""` |
| I: `--bat-buoc`, `$GITHUB_PATH` là thư mục, công cụ tuỳ chọn trước công cụ bắt buộc | rc khác 0; công cụ tuỳ chọn báo `--bat-buoc di tiep`; đúng hai dòng `khong ghi duoc $GITHUB_PATH` |
| J: công thức tự ghi `DICH` cho Y (rg 9.9.9) sau bộ chọn | rc 0, `DAT`, JSON có `9.9.9` (PATH nội bộ dùng Y), tệp = `b"<Y>\n"` (một nguồn) |
| L-LF, L-CR: `DICH` (qua biến môi trường) chứa `\n` / `\r` | rc khác 0, tệp = `b""`, stderr `ky tu xuong dong` |
| M: `bash -a` + `--bat-buoc`; công cụ bắt buộc chụp `env` của tiến trình con ở lượt sau | rc 0; không có `KQ=` hay `_tl1488` trong `env`; tệp = hai dòng của hai công cụ |
| W-rong / W-du-lf / W-cr: Windows (`git`, cygpath giả): rc 0 mà rỗng / thừa LF đuôi / có CR | rc khác 0, tệp = `b""`, stderr có `rong` hoặc `xuong dong` |
| K1: `cat` của lần đọc kênh in đủ nội dung rồi trả 9 | rc 7, tệp = `b""`, stderr `khong doc duoc kenh ket qua` |
| K2: `cat` của lần đọc kênh đầu trả 9 không in gì (lần sau, nếu có, đọc được) | rc 7, tệp = `b""` |
| K3: đường thành công, `cat` giả đếm số lần mở kênh `*/kq` | rc 0, đúng 1 lần đọc, tệp = `b"<thư mục tốt>\n"` |

- `--lap-ca r1488_github_path_chi_ghi_khi_thanh_cong`: 3/3 (`ab298a8`), 2/2 (`b7a280e`, `42b5386`, `f8747c4`, `7a8823b`).
- Phản chứng (ca chạy với `ops/cai_cong_cu.sh` của commit cũ): master `8656dc0` ⇒ ĐỎ ở (A); `2847860` (r1 lượt 1) ⇒ (G);
  `b7a280e` (r1 lượt 2) ⇒ (J, kỳ vọng r2); `42b5386` (r2) ⇒ (J, kỳ vọng r3: tệp rỗng thay vì `<Y>`); `f8747c4` (r3 trước
  Codex lượt 4) ⇒ (W-du-lf).

## 4. Đột biến (N2)

Từng đột biến chạy riêng trên đúng ca đích để đọc assertion. Mọi đột biến đều chết bằng `TinHieuChotCa`.

| Đột biến | Thay đổi | Chết ở |
|---|---|---|
| `wp1488_sh_bo_chon_ghi_thang` | bộ chọn ghi `>> "$GITHUB_PATH"` | (A) |
| `wp1488_sh_chep_khong_xet_rc` | đọc kênh và ghi cả khi `RC_CAI ≠ 0` | (B) |
| `wp1488_sh_chep_loi_khong_dat_rc` | bỏ `\|\| RC_CAI=1` | (I) |
| `wp1488_sh_chep_hai_lan` | ghi hai lần | (A') |
| `wp1488_sh_dong_trang` | `'%s\n\n'` | (A') |
| `wp1488_sh_crlf` | `'%s\r\n'` | (A') |
| `wp1488_sh_chep_loi_thoat_ngay` | lỗi ghi ⇒ `exit 1` ngay | (I) |
| `wp1488_sh_doc_kenh_cu_ghi_muon` | đọc kênh một lần (móc C kích hoạt), RỒI đọc kênh của lượt đầu nếu writer muộn đã ghi | (C) |
| `wp1488_sh_doc_kenh_rieng_truoc` | dựng lại thứ tự r1: quyết định ghi bằng một lần đọc kênh riêng, không xét lỗi, trước lần đọc có xét lỗi | (L-LF) |
| `wp1488_sh_bo_tu_choi_xuong_dong` | bỏ từ chối `\n`/`\r` | (L-LF) |
| `wp1488_sh_kq_lo_export` | bỏ `export -n KQ` | (M) |
| `wp1488_sh_ham_lo_export` | bỏ `export -nf` hàm | (M) |
| `wp1488_sh_bo_tu_choi_dong_rong` | bỏ từ chối dòng rỗng | (W-rong) |
| `wp1488_sh_cygpath_an_lf` | đọc `cygpath -w` không sentinel (`$( )` ăn LF đuôi) | (W-du-lf) |
| `wp1488_sh_chi_xet_dich` | chỉ xét `\n`/`\r` trong `DICH`, bỏ xét dòng đã đổi | (W-du-lf) |
| `wp1488_sh_doc_kenh_hai_lan` | đọc kênh thêm một lần sau lần đầu thành công | (K3) |
| `wp858_sh_nuot_loi_cygpath_w` (neo mới) | bỏ xét mã thoát `cygpath -w` | `r858_cai_windows…` và `r858_hinh_dang…` |
| `wp858_sh_github_path_khong_qua_cygpath` (neo mới) | dòng không qua `cygpath -w` | `r858_cai_windows…` và `r858_hinh_dang…` |
| `wp858_sh_github_path_vang_khong_mac_dinh` (neo mới) | `${GITHUB_PATH}` không mặc định dưới `set -u` | `r858_cai_linux…` và `r858_hinh_dang…` |
| `wp858_sh_nuot_loi_ghi_github_path` (neo mới) | lỗi ghi bị nuốt bằng `\|\| :` | (E) của r1488; `r858_cai_linux…`, `r858_hinh_dang…` |

Ghi chú đo được:
- `wp1488_sh_chep_loi_khong_dat_rc` chết ở (I), không ở (E): ở lời gọi trực tiếp, hàm trả 1 không kèm `||` thì `set -e` cũng
  thoát 1; chỉ lượt `source` (I) phân biệt đường `RC_CAI` với errexit.
- `wp1488_sh_doc_kenh_rieng_truoc` chết ở (L-LF) trước khi tới (K1): lần đọc riêng lấy dòng 2 của kênh, bỏ qua phần sau
  ký tự xuống dòng, nên ghi một dòng mà lần đọc chính thì từ chối.
- `wp1488_sh_doc_kenh_cu_ghi_muon`: bản đầu chọn tệp TRƯỚC lúc móc của C kích hoạt nên sống; viết lại để đọc sau khi móc
  kích hoạt, nay chết ở (C).
- Bảng `cai_sh` (mọi packet) chạy riêng: 90/90 (`b7a280e`), 92/92 (`42b5386`), 93/93 (`f8747c4`), 96/96 (`7a8823b`).

## 5. Hồi quy (N3) — các vế dựng cùng cách (clone + checkout + `core.abbrev 7`)

`/tmp/.git` không tồn tại lúc đo (lượt đo `f8747c4`: một `/tmp/.git` RỖNG do lượt Codex 3 tạo lúc 10:20:59Z được gỡ bằng
`rmdir` trước khi chạy).

| Phép đo | base `8656dc0` | head |
|---|---|---|
| `launcher_test.py` | 452/452 (tổng 454, bỏ qua 2) | `ab298a8`, `b7a280e`, `42b5386`, `f8747c4`, `7a8823b`: 453/453 (tổng 455, bỏ qua 2) |
| `launcher_test.py --dot-bien` | 782/782 (7 không đo được trên nền này) | `ab298a8` 788/788 · `b7a280e` 792/792 · `42b5386` 794/794 · `f8747c4` 795/795 · `7a8823b` 798/798 (cùng 7) |

Hai ca bỏ qua (`t62_…`, `r484_g4_windows_sid_alias_identity`) và 7 đột biến không đo được (nhánh Windows) giống hệt nhau
ở mọi vế. Delta trên `7a8823b` = +1 ca, +16 đột biến, 0 hồi quy.

Các ca `r831_* r858_* r868_* r1045_* r1404_* r1479_*` chạy riêng: base 34/34; bản dựng thử r1, r2, r3 trước khi sửa ca hình
dạng: 33/34, ca đỏ duy nhất là `r858_hinh_dang_cong_thuc_cai`.

## 6. Khác

- `python .claude/dev/packet_loop.py doctrine-scan --root .`: sạch (12 tệp), rc 0.
- Commit message của `f8747c4` ghi "15 đột biến wp1488_sh_*"; số đúng là 13 (bảng trên; 782 + 13 = 795).
- CI của PR ducthangho/tra-luat#1489 và review Codex (N4, N5): `VERDICT.md`.

## 7. Nợ có tên còn mở

- `WP1488-WIN-THEO-LENH` (Codex lượt 4 P2; chủ kho chọn ghi nợ ở Review Rescue Checkpoint, 21-11-2026 ~12:10Z): chế độ
  Windows nhận bằng chuỗi `chon_thu_muc_chay_duoc --win ` trong `LENH`. Năm công thức Windows trong `ops/cong_cu.yaml` viết
  đúng literal nên chạy đúng (`r858_cai_windows…` đạt). Sai khi `"--win"` có nháy, tab thay dấu cách, chuỗi nằm trong dữ
  liệu hay ở nhánh không chạy. Sửa tận gốc phải mang chế độ `--win` qua kênh kết quả (đổi định dạng kênh đã đóng băng ở B5).

## 8. Không đo được

- Runner CI thật với `$GITHUB_PATH` của GitHub Actions: chỉ đo bằng tệp giả.
- macOS/Windows thật: `cygpath -w` nay chạy ở script chính, nhận biết bằng `LENH` có `chon_thu_muc_chay_duoc --win`; ca
  `r858_cai_windows…` và (W) dùng cygpath giả trên Linux, chưa chạy trên Windows thật.
