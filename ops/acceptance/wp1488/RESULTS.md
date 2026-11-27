# WP1488 — kết quả đo (executor: phiên `session_015GtxrazyAyLwN5BiEB52Sq`, Linux, 21-11-2026)

Base gốc `8656dc0176ed108e12c209ba55c91a1f6f9d612f` (g1–g5); g6/g7 dựng trên master `b1db69429d272cfde43681b4a9de1184c452c0f1`.
Đặc tả hiện hành: `ops/specs/wp1488-r6.md` (sha256 `e33176d2…aecf`), lease `wp1488-r6-g7-claude` (thay g6, bia mộ hai chiều;
g6 thay g5). §10 cho r5, §11 cho g6/g7 (r6). Mã r1 đã đo: `ab298a8`, `b7a280e`; mã r2: `42b5386`; mã r3:
`f8747c4`, `7a8823b` (sau Codex lượt 4). Mã r4 (trả nợ `WP1488-WIN-THEO-LENH`):
`ab83dd363` (40 hex ở §9); sau Codex lượt 5 (P3, chỉ đổi ca test): `22a7ad1`; các commit sau nó chỉ đổi tệp hồ sơ.

## 1. Tái hiện lỗi trên base

Bằng `_wp868_chay` (stub, không mạng), script của `8656dc0`:
- A: lượt đầu `apt-get install … && chon_thu_muc_chay_duoc rg <tot2> && false`, lượt thử lại qua stdout ⇒ rc 0, `DAT`,
  `$GITHUB_PATH` = `[<tot2>]`.
- B: `chon_thu_muc_chay_duoc rg <tot> && false` ⇒ rc 1, `$GITHUB_PATH` = `[<tot>]`.

## 2. Thay đổi (r3; r4 ở §9)

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

## 7. Nợ có tên

- ĐÃ TRẢ ở r5 (§10). `WP1488-NUL-KENH` (Codex lượt 5 P2; chủ kho chọn ghi nợ ở Review Rescue Checkpoint, 21-11-2026 ~14:10Z). Lần đọc
  kênh `KQ="$(cat -- "$KENH_KQ" && printf x)"` để Bash bỏ byte NUL (chỉ in cảnh báo `ignored null byte`), nên kênh
  `<nhãn>\0\n<dir>` được nhận như `<nhãn>\n<dir>`. Đo (VERDICT lượt 5): `DICH\0` được nhận ở base `8656dc0`, r3 và r4
  (lớp có từ wp868); `DICH_WIN\0` trả 7 ở base/r3 chỉ vì nhãn chưa tồn tại, r4 nhận và ghi `W:<dir>`. Chỉ chạm tới khi
  chính công thức trong `ops/cong_cu.yaml` ghi NUL vào kênh. Chữa đúng là đổi cách đọc kênh (phát hiện NUL ngay trong lần
  đọc duy nhất), mà dòng ấy là neo của nhiều ca/đột biến wp868 — việc của packet riêng.

- ĐÃ TRẢ ở r4 (§9). `WP1488-WIN-THEO-LENH` (Codex lượt 4 P2; chủ kho chọn ghi nợ ở Review Rescue Checkpoint, 21-11-2026 ~12:10Z): chế độ
  Windows nhận bằng chuỗi `chon_thu_muc_chay_duoc --win ` trong `LENH`. Năm công thức Windows trong `ops/cong_cu.yaml` viết
  đúng literal nên chạy đúng (`r858_cai_windows…` đạt). Sai khi `"--win"` có nháy, tab thay dấu cách, chuỗi nằm trong dữ
  liệu hay ở nhánh không chạy. Sửa tận gốc phải mang chế độ `--win` qua kênh kết quả (đổi định dạng kênh đã đóng băng ở B5).

## 8. Không đo được

- Runner CI thật với `$GITHUB_PATH` của GitHub Actions: chỉ đo bằng tệp giả.
- macOS/Windows thật: `cygpath -w` nay chạy ở script chính, chế độ lấy từ nhãn kênh `DICH_WIN` (r4); ca
  `r858_cai_windows…`, (W), (N), (I-win) dùng cygpath giả trên Linux, chưa chạy trên Windows thật.

## 9. Revision 4 — trả nợ `WP1488-WIN-THEO-LENH` (đặc tả `ops/specs/wp1488-r4.md`)

Mã: `ab83dd363…` (`ab83dd3638ae0bc8a6f2aec35ae789c06dd7c66f`). Đổi so với `7a8823b`:
- `ops/cai_cong_cu.sh`: bộ chọn ghi nhãn `DICH_WIN` khi THẬT SỰ chạy với `--win`, ngược lại `DICH` (B1). Lần đọc kênh duy
  nhất chọn chế độ theo nhãn: `DICH` ⇒ `_tl1488_ghi_github_path "<dir>" ""`, `DICH_WIN` ⇒ `… win` (`cygpath -w`); hàm
  không còn đọc `$LENH` (B2). Phép đọc PATH nhận thêm `DICH_WIN` (B5). Chú thích đầu tệp nêu định dạng kênh mới.
- `.claude/dev/launcher_test.py`:
  - Ca r1488 thêm (N) bốn biến thể qua `_wp868_chay` với `cygpath` giả ở đầu PATH (`-w` ⇒ `W:<dir>`): `"--win"` có nháy
    và tab ⇒ tệp = `b"W:<dir>\n"`; chuỗi `--win` chỉ nằm trong dữ liệu (`: '…--win…'`) và nhánh `if false` có `--win` ⇒ tệp
    = `b"<dir>\n"`; cả bốn rc 0, `DAT`. Thêm (I-win): như (I) trên nhánh `DICH_WIN` — `--bat-buoc`, công cụ tuỳ chọn chạy
    bộ chọn `--win` với `cygpath -w` in rồi thoát 37, công cụ bắt buộc sau nó ⇒ rc 0, báo `cygpath -w hong`, công cụ tuỳ
    chọn `--bat-buoc di tiep`, tệp = đúng dòng của công cụ bắt buộc.
  - `r858_hinh_dang_cong_thuc_cai`: chốt dòng nhãn `nhan=DICH; if [ -n "$win" ]; then nhan=DICH_WIN; fi`, `case "$2" in win)`,
    hàm không chứa `LENH`, khối gọi hai nhánh. `r868_hinh_dang_kenh_ket_qua`: chốt nhánh `DICH_WIN` của phép đọc PATH.
    `printf` giả của `r868_ghi_kenh_hong_thi_dung` khớp định dạng mới (`'%s\n%s'` kèm nhãn ở `$2`); ca vẫn đòi dấu
    `printf: loi ghi gia` trong stderr nên không đạt suông.
  - Năm đột biến r4 (bảng dưới). Neo của `wp868_sh_ham_in_stdout_thay_kenh`, `wp868_sh_ghi_dich_nuot_loi`,
    `wp1488_sh_bo_chon_ghi_thang`, `wp1488_sh_chep_loi_khong_dat_rc`, `wp1488_sh_chep_loi_thoat_ngay`,
    `wp1488_sh_doc_kenh_rieng_truoc` đổi theo dòng ghi kênh và lời gọi mới; không xoá đột biến nào.

Phản chứng (bốn biến thể của (N), cùng fixture, chỉ đổi `ops/cai_cong_cu.sh`):

| Biến thể | Kỳ vọng | `7a8823b` (r3) | `ab83dd3` (r4) |
|---|---|---|---|
| `chon_thu_muc_chay_duoc "--win" rg <u>` | `W:<dir>` | `<dir>` — SAI | đúng |
| `chon_thu_muc_chay_duoc<TAB>--win rg <u>` | `W:<dir>` | `<dir>` — SAI | đúng |
| `: '…--win rg' && chon_thu_muc_chay_duoc rg <u>` | `<dir>` | `W:<dir>` — SAI | đúng |
| `if false; then …--win rg x; fi; chon_thu_muc_chay_duoc rg <u>` | `<dir>` | `W:<dir>` — SAI | đúng |

Chạy cả ca `r1488_…` với script `7a8823b` ⇒ ĐỎ ở (N-nhay). `--lap-ca r1488_github_path_chi_ghi_khi_thanh_cong`: 1/1 trên
`ab83dd3`.

Đột biến r4 (chạy riêng trên ca đích, mỗi cái chết bằng `TinHieuChotCa`):

| Đột biến | Thay đổi | Chết ở |
|---|---|---|
| `wp1488_sh_bo_chon_luon_dich` | bộ chọn luôn ghi nhãn `DICH` | (I-win) |
| `wp1488_sh_quyet_theo_lenh` | hàm quyết định theo `$LENH` (thiết kế r3) | (N-nhay) |
| `wp1488_sh_path_bo_nhanh_dich_win` | bỏ nhánh `DICH_WIN` của phép đọc PATH | (N-nhay) rc 7; `r858_cai_windows…` rc 7 |
| `wp1488_sh_dich_win_khong_doi` | nhánh `DICH_WIN` gọi hàm với chế độ rỗng | (I-win); `r858_cai_windows…` |
| `wp1488_sh_dich_win_loi_khong_dat_rc` | bỏ `\|\| RC_CAI=1` ở nhánh `DICH_WIN` | (I-win) |
| `wp1488_sh_path_nhan_hau_to` (Codex lượt 5) | phép đọc PATH nhận thêm `DICH_WINx*` | (Q-win-hau-to) rc 3 |
| `wp1488_sh_ghi_nhan_long` | phía ghi nhận `DICH_WIN*` (bỏ đòi LF ngay sau nhãn) | (Q-win-hau-to) rc 1, có gọi `cygpath` |

Bản đầu của bảng này (commit `377a0cb`) ghi (W-rong) cho hai dòng đầu vì đo TRƯỚC khi thêm (I-win), mà (I-win) chạy trước
(W); Codex lượt 5 (P3) bắt được, đo lại ở `22a7ad1` cho cột trên.

Kịch bản (Q) (Codex lượt 5 P3, thêm ở `22a7ad1`): công thức tự ghi kênh `DICH_WINx\n<dir>`, `DICHx\n<dir>`, `DICH_WIN\n`,
`DICH\n` ⇒ cả bốn rc 7, stderr `kenh ket qua hong`, tệp = `b""`, `cygpath` giả không được gọi (tệp log vắng).

Ghi chú đo được: `wp1488_sh_dich_win_loi_khong_dat_rc` SỐNG ở bản đầu của r4 (chưa có I-win) — cùng lý do như
`wp1488_sh_chep_loi_khong_dat_rc` ở §4: ngoài lượt `source`, hàm trả 1 không kèm `||` thì `set -e` cũng thoát. Thêm (I-win)
thì chết. Các đột biến r1–r3 đo lại trên `ab83dd3` (chạy riêng): chết ở đúng ca ghi trong §4.

Hồi quy (N3), hai vế dựng trong CÙNG một lệnh (clone + checkout + `core.abbrev 7`), `/tmp/.git` không tồn tại:

| Phép đo | `7a8823b` | `ab83dd3` |
|---|---|---|
| `launcher_test.py` | 453/453 (tổng 455, bỏ qua 2) | 453/453 (tổng 455, bỏ qua 2) |
| `launcher_test.py --dot-bien` | 798/798 (7 không đo được trên nền này) | 803/803 (cùng 7) |

Hai ca bỏ qua và 7 đột biến không đo được giống hệt nhau ở hai vế. Số ca không đổi vì (N), (I-win) là kịch bản trong ca
`r1488_…` sẵn có. Delta = +5 đột biến, 0 hồi quy. Hai vế chạy song song trong cùng một lệnh, 13:1xZ–13:4xZ.

Đo lại sau Codex lượt 5 (thêm Q và 2 đột biến), hai vế dựng lại trong CÙNG một lệnh, chạy 2026-11-21T14:11:58Z → 14:38:34Z,
`/tmp/.git` không tồn tại:

| Phép đo | `7a8823b` | `22a7ad1` |
|---|---|---|
| `launcher_test.py` | 453/453 (tổng 455, bỏ qua 2) | 453/453 (tổng 455, bỏ qua 2) |
| `launcher_test.py --dot-bien` | 798/798 (7 không đo được) | 805/805 (cùng 7) |

Delta = +7 đột biến (5 r4 + 2 sau lượt 5), 0 hồi quy. Ruff `--select F`: 5 F841 ở hai vế (delta 0).

Ruff `--select F` trên `launcher_test.py`: 5 F841 ở cả hai vế (delta 0). `shellcheck ops/cai_cong_cu.sh`: một SC1090 ở cả
hai vế (delta 0). `doctrine-scan`: rc 0.

## 10. Revision 5 — trả nợ `WP1488-NUL-KENH` (đặc tả `ops/specs/wp1488-r5.md`)

Lịch sử: `210ceff` → `9390529` (merge master `d0868db`, không xung đột; tác giả giữ chỗ `x` vì dựng trong clone đo — giữ
nguyên để không đổi SHA đã review) → `e9ac35b` (r5) → `4cd2ba2` (P3 lượt 6). Lease g5 cấp sau; nhánh fast-forward lên
`4cd2ba2`, các commit sau chỉ đổi hồ sơ.

- `ops/cai_cong_cu.sh`: lần đọc kênh duy nhất `KQ="$(cat -- "$KENH_KQ" | tr '\000' '\001' && printf x)"` (dưới
  `pipefail`, lỗi `cat` hay `tr` vẫn là lỗi đọc ⇒ 7); ngay sau `export -n KQ`, kết quả có `0x01` ⇒
  `cai_cong_cu: kenh ket qua co byte NUL hoac 0x01 — tu choi`, thoát 7 TRƯỚC mọi phân nhánh.
- `.claude/dev/launcher_test.py`: ca r1488 thêm (R) 7 biến thể — NUL ở nhãn `DICH`/`DICH_WIN`/`GIU_PATH`; NUL, `0x01` giữa
  đường dẫn với nhãn `DICH` và với nhãn `DICH_WIN` hợp lệ ⇒ rc 7, đúng NGUYÊN dòng báo, tệp rỗng, không gọi `cygpath`;
  (R-gp-vang) vắng `$GITHUB_PATH` ⇒ vẫn 7, không tới hậu kiểm. Neo của các ca/đột biến đọc kênh dời theo dòng mới
  (`r858_hinh_dang…`, `r868_hinh_dang…`, `wp868_sh_doc_kenh_nuot_loi`, `wp1488_sh_doc_kenh_*`, `wp1488_sh_chep_khong_xet_rc`),
  không xoá đột biến nào.

Phản chứng (cùng fixture, công thức tự ghi kênh, đo 25-11-2026): script `210ceff` ⇒ `DICH\0` rc 0 ghi `<dir>`;
`DICH_WIN\0` rc 0 ghi `W:<dir>`; NUL giữa đường dẫn ghi `<dir>x` rồi rc 3; `0x01` giữa đường dẫn ghi `<dir>\x01x` rồi rc 3.
Ca r1488 với script `210ceff` ĐỎ ở (R-dich-nul). Ứng viên r5: cả năm dạng rc 7, tệp rỗng; kênh đúng vẫn rc 0.

Đột biến r5 (chạy riêng trên ca đích, chết bằng `TinHieuChotCa`):

| Đột biến | Thay đổi | Chết ở |
|---|---|---|
| `wp1488_sh_bo_tr_nul` | bỏ `\| tr` (Bash lại bỏ NUL) | (R-dich-nul) rc 0, có dòng ghi |
| `wp1488_sh_bo_chot_nul` | chốt `0x01` không bao giờ khớp | (R-dich-nul) rc 7 nhưng thiếu dòng báo riêng |
| `wp1488_sh_pipeline_nuot_loi_cat` | `{ cat … \|\| :; } \| tr` | (K1) rc 0 sau lỗi đọc |
| `wp1488_sh_chot_nul_sau_ghi` | chốt đặt SAU bước ghi | (R-nul-giua) tệp đích đã bị ghi |
| `wp1488_sh_chot_nul_chi_khi_co_dich` (Codex lượt 6) | chốt chỉ khi có `$GITHUB_PATH` | (R-gp-vang) rc 3 |
| `wp1488_sh_cygpath_truoc_chot_nul` (Codex lượt 6) | gọi `cygpath -w` trước chốt khi nhãn `DICH_WIN` | (R-win-nul-giua) có log `cygpath` |

Các đột biến đổi neo đo lại: `wp1488_sh_doc_kenh_cu_ghi_muon` (C) · `wp1488_sh_doc_kenh_rieng_truoc` (L-LF) ·
`wp1488_sh_doc_kenh_hai_lan` (K3) · `wp1488_sh_chep_khong_xet_rc` (B) · `wp1488_sh_kq_lo_export` (M) ·
`wp868_sh_doc_kenh_nuot_loi` (`r868_doc_kenh_hong_thi_dung` và `r868_hinh_dang_kenh_ket_qua`). Reviewer lượt 7 đo lại
độc lập 12 đột biến + 1 đột biến riêng: cùng ca chết.

Hồi quy (N3), hai vế dựng trong CÙNG một lệnh (clone + checkout + `core.abbrev 7`), `/tmp/.git` không tồn tại:

| Phép đo | master `d0868db` | `e9ac35b` (19:02Z–19:26Z) | `4cd2ba2` (20:58Z–21:21Z) |
|---|---|---|---|
| `launcher_test.py` | 455/455 (tổng 457, bỏ qua 2) | 456/456 | 456/456 (tổng 458, bỏ qua 2) |
| `launcher_test.py --dot-bien` | 801/801 (7 không đo được) | 828/828 | 830/830 (cùng 7) |

Merge `210ceff` vào master `d0868db` TRƯỚC r5 (đo 18:38Z–19:02Z): 456/456, 824/824. Delta của `4cd2ba2` so master = +1 ca
(r1488), +29 đột biến (23 `wp1488_sh_*` r1–r4 + 6 r5), 0 hồi quy. Ruff `--select F` 5 F841 và shellcheck 1 SC1090 giống
hệt master (delta 0). `doctrine-scan` rc 0. Windows thật: chưa đo (cygpath giả trên Linux).

## 11. Generation g6/g7 — áp ADR-0060, review và vá THEO LỚP (đặc tả r6)

Chủ kho chỉ thị 2026-11-26 áp ADR-0060 và vá/review theo lớp. Đối chiếu (Issue #1488, issuecomment-7198141773): PR #1489 đã
push 26 head (vượt M5) ⇒ đóng, mở g6; 7 verdict g1–g5 không review theo lớp; Issue chưa có hồ sơ; Windows, `full_mutant_audit`,
connector chưa chạy. Chủ kho nâng trần Codex 8→12 (E2).

- g6 (`d5688ac`, master `b1db694` + mã g5 trong một commit): Codex lượt 8 qua `launcher.py run` (`run_id` `cf204383…`,
  `gpt-6-astra`/`xhigh` đo được), TOÀN diff theo lớp ⇒ `changes_requested`, 0 P0–P2, P3 mở ở hai lớp:
  `thay-the-lenh-lam-mat-du-lieu` (F1488-L8-01 A/B/C: `cygpath -w`, `cygpath -u`, stdout rơi về) và
  `phep-do-khong-do-dieu-khai` (F1488-L8-02 A/B: JSON stdout Windows, PATH nguyên văn khi đích rỗng/vắng). Verdict nguyên văn:
  issuecomment-7199395981; mục sổ xét lại cách làm: issuecomment-7199403050.
- r6 (chủ kho duyệt băm `e33176d2`, issuecomment-7199661828), g7 (`agent/wp1488-g7-claude`):
  - `ops/cai_cong_cu.sh`: MỘT hàm `_tl1488_doc` (B7) đọc nguồn qua `tr '\000' '\001'` dưới `pipefail` kèm sentinel, dùng
    chung cho kênh, `cygpath -u` (bộ chọn), `cygpath -w` (bước ghi), stdout rơi về; mỗi nơi gọi từ chối 0x01 trước side
    effect rồi mới bỏ delimiter của giao thức mình (`cygpath`: đúng một LF; stdout: các LF cuối như cũ). `export -nf`.
  - `.claude/dev/launcher_test.py`: ca r1488 thêm S (`cygpath -w` NUL đầu/giữa/cuối), U (`cygpath -u` NUL/LF thừa/rỗng),
    U-cap (cặp `<x>`/`<x>LF`), V (stdout có NUL ⇒ 7), Y (PATH nguyên văn, DICH/DICH_WIN × rỗng/vắng); X: `_r1488_json` — mọi
    lượt gọi trực tiếp thành công của r1488 và bộ chọn r858 phải có TOÀN stdout là một JSON. Bộ dò (M) siết sang đúng
    `KQ=` và `BASH_FUNC__tl1488*` (thân `chon_thu_muc_chay_duoc`, export sẵn từ base dưới allexport, nay nhắc tên
    `_tl1488_doc`). 8 đột biến r6; neo cũ dời theo dòng mới, không xoá đột biến nào.
  - Lượt `--dot-bien` đầu trên `b407791` ra 836/838: `wp858_sh_cygpath_u_hong_khong_tra_loi` và `wp868_sh_doc_kenh_nuot_loi`
    mất răng vì B7 (hàm không gán đầu ra khi lệnh lỗi; ca hình dạng chưa chốt thân hàm). Sửa ở `bcd23b3`: ca bộ chọn đòi DỪNG
    ngay ở lời gọi `cygpath -u` hỏng; ca hình dạng r868 chốt thân `_tl1488_doc` trên cả tệp. Cả hai chết đủ 4 ca đích.

Phản chứng: ca r1488 với script g6 `d5688ac` ĐỎ ở (S-nul_dau) (rc 0, ghi `W:<dir>`).

Đột biến r6 (chạy riêng, chết bằng `TinHieuChotCa`):

| Đột biến | Chết ở |
|---|---|
| `wp1488_sh_u_bo_chot_byte` | (U-nul) |
| `wp1488_sh_u_bo_chot_rong` | (U-rong) |
| `wp1488_sh_u_cat_moi_lf` | (U-du_lf) |
| `wp1488_sh_w_bo_chot_byte` | (S-nul_dau) |
| `wp1488_sh_stdout_bo_chot_byte` | (V) rc 3 |
| `wp1488_sh_doc_lo_export` | (M) `BASH_FUNC__tl1488_doc` |
| `wp1488_sh_win_in_rac_stdout` (reviewer lượt 8) | (N-nhay) qua `_r1488_json`; `r858_cai_windows…` |
| `wp1488_sh_path_cat_lf_cuoi` (reviewer lượt 8) | (Y-DICH-rong) |

Cổng trên `bcd23b312082708ff1de89d6472313cfda7a5bb4` (mã cuối g7; commit sau chỉ đổi tệp này):

| Phép đo | master `b1db694` | `bcd23b3` |
|---|---|---|
| `launcher_test.py` | 455/455 (tổng 457, bỏ qua 2) | 456/456 (tổng 458, bỏ qua 2) |
| `launcher_test.py --dot-bien` | 801/801 (7 không đo được) | 838/838 (cùng 7) |
| `tl.py --selftest` | — | 1789/1789, rc 0 |

Hai vế dựng trong CÙNG một lệnh (clone + checkout + `core.abbrev 7`, `core.autocrlf false`, `core.eol lf`), 18:34Z–19:03Z,
`/tmp/.git` không tồn tại. `git diff --check b1db694..HEAD` rc 0; ruff `--select F` 5 F841 và shellcheck 1 SC1090 giống master;
`doctrine-scan` rc 0. Windows thật (M3 `required`): chưa đo tại thời điểm ghi mục này.

### 11.1 Sau Codex lượt 9 (F1488-L9-01, checkpoint M1)

Codex lượt 9 (`c6b7092`, `run_id` `c2dbbeb8…`) `changes_requested`, 0 P0–P2: F1488-L9-01 (lớp `phep-do-khong-do-dieu-khai`)
và phần lịch sử stdout-LF của F1488-L8-01 C. Số lớp P3 chưa đóng 2 → 2 ⇒ checkpoint M1; chủ kho chọn "Vá L9-01, miễn
stdout-LF" (issuecomment-7205822618). Bản vá `02ddc74` chỉ đổi `.claude/dev/launcher_test.py`:

- (T) lỗi vế `tr` của `_tl1488_doc` ở bốn điểm gọi × hai kiểu (không in / chuyển đủ rồi thoát 45); `tr` giả chỉ hỏng ở điểm
  đang thử; ca đòi dấu `TR_LOI_GIA`, đúng mã (kênh 7, stdout 1, `cygpath` khác 0), dòng báo của điểm ấy, tệp đích rỗng.
- (V-path) stdout chỉ tới thư mục có 0x01 trong tên chứa `rm` giả ghi dấu ⇒ rc 7 và `rm` giả KHÔNG được gọi.
- (X) C và K3 dùng `_r1488_json`.
- Đột biến: `wp1488_sh_tr_nuot_loi` chết ở (T-kenh-rong); `wp1488_sh_chot_stdout_sau_path` (dời chốt qua `export PATH`)
  chết ở (V-path) — rc 7 nhưng `rm` giả đã gọi. Bản đầu của (V-path) đặt `rm` giả sai chỗ (khoá `ung_vien` ngoài `dau/` là
  thư mục + `/rg`) nên đột biến dời chốt sống; sửa trước khi commit.

Cổng trên `02ddc74da4cb6af2c7527b280dd04e61bdea5e6e` (mã cuối; commit sau chỉ đổi tệp này), hai vế cùng một lệnh
23:49Z–00:17Z: master `b1db694` 455/455 · 801/801; `02ddc74` 456/456 · **840/840** (cùng 7 không đo được); `tl.py --selftest`
1789/1789 rc 0; `git diff --check` rc 0; ruff/shellcheck/doctrine-scan như master.
