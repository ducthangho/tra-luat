tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# GWS-CRED-DICH-NGOAI-KHO-C1 r1 — trên Windows, `credentials.json` của gws (W4, W5 trong `tl_gws.py`) chỉ ghi tới đường ổ CỤC BỘ nằm trong danh sách cho phép, ngoài kho git, không xuyên liên kết; UNC và ổ mạng luôn bị từ chối

- packet_id: GWS-CRED-DICH-NGOAI-KHO-C1; revision: 1;

| trường | giá trị |
|---|---|
| `packet_issue` | #433 |
| `nguon_cap_viec` | Issue #433; P2a `GWS-CRED-DICH-NGOAI-KHO-A-r1.md` (sha256 `b0065947…`) §2 "Để P2c". Đặc tả gộp P2c `GWS-CRED-DICH-NGOAI-KHO-C-r1.md` bản 4 (sha256 `b477d23e…`, 3 lượt review Codex, chưa approve) được TÁCH theo quyết định chủ kho 2026-11-19 ~10:50Z (phiên điều phối #1206, AskUserQuestion): **Q2 = D** — KHÔNG nhận đích qua mạng cho `credentials.json` (UNC và ổ mạng từ chối hẳn; đảo quyết định "cho phép UNC" sáng 19-11), BỎ hẳn phần định danh tệp; **Q1** — hai packet riêng, land C1 → R; **Q4–Q7** — đồng ý mặc định đề xuất (Q5 thành vĩnh viễn); **Q9** — chủ kho tự chạy lệnh shell ADMIN trên Desktop khi tới bước đo; **Q8** — ngoại lệ bundled xin riêng cho đúng `packet_id` khi cấp lease. Đặc tả này là **C1**; vế reparse point là packet **R** `GWS-CRED-DICH-NGOAI-KHO-R` (đặc tả riêng, land sau C1). |
| `phu_thuoc` | P2a ĐÃ LAND (PR #1415, merge `417b593`; `git diff --numstat 417b593^1 417b593` = fragment +389, `tl_gws.py` +48/−19, bundled +1, tổng +438). C1 thay nhánh `os.name != "posix"` của `_dich_cred_gws`, gọi lại `_kiem_dich_ghi`, `_ghi_nguyen_tu_0600`, `_safe_exc` và hợp đồng lỗi sáu cụm của P2a; KHÔNG sửa thân hàm nào trong số đó. R phụ thuộc C1, C1 không phụ thuộc R. |
| `review_class` | `sensitive` (`scripts/tl_gws.py` là đường ghi credential). Đối chiếu `lease_publish check` khi cấp lease. |
| `base` | `96b6a33d770f7539a3eacbebdc215f87ded4ea7f` (origin/master, `git ls-remote` đo 2026-11-19T10:59:03Z); blob `scripts/tl_gws.py` `9ec027c2808868a05b67adc3d93ea68a574d6ec0`, 2649 dòng — BẰNG blob tại `417b593` và `11bd033`. Lease ghi base thật; phiên thi hành đo lại §0 trước khi sửa. |

## 0. Hiện trạng (đo trên `96b6a33`, Linux, CPython 3.11.18 / 3.12.3 / 3.13.18, `python -I`, không mạng)

### 0.1 Nhánh Windows hiện tại

| chỗ | dòng | hành vi |
|---|---|---|
| `_dich_cred_gws` | 1201–1210 | nhánh `if os.name != "posix": return os.path.join(cfgdir_tho, "credentials.json"), None` (1204–1205): không chuẩn hoá, không chốt kho, không chốt liên kết; nhận mọi dạng đường kể cả UNC, `\\?\`, `D:fake`. |
| `_kiem_dich_ghi` | 1173–1187 | luật (a) `_trong_kho_git(dirname(dich))`; luật (b) `lstat` `goc` và mọi tiền tố tới `dich`, `S_ISLNK` ⇒ `là liên kết tượng trưng` (1183). Thân giữ nguyên ở C1. |
| W4 / W5 | 1803–1823 / 1961–1968 | gọi `_dich_cred_gws(cfgdir)` (1813 / 1963) rồi `_ghi_nguyen_tu_0600` trong một `try … except OSError`. Không đổi. |
| `_trong_kho_git` | 1119–1139 | đi lên trên `abspath` và `realpath` tìm `.git` bằng `lstat`. Trên Windows `realpath` giải symlink/junction và (lời khai, đo ở D11) ổ `subst`. Gốc share UNC là trần của chuỗi nên share gốc dưới một kho không thấy `.git` — lý do UNC và ổ mạng bị từ chối hẳn. |

### 0.2 Phép đo `ntpath` (2026-11-19T10:04:39Z; `c1/nguyen-mau/do_ntpath.py`, `ntpath-3.1x.txt`)

28 đầu vào: `splitdrive` GIỐNG NHAU trên 3.11/3.12/3.13 (ví dụ `\\server\share\x`→(`\\server\share`,`\x`); `\\?\C:\x`→(`\\?\C:`,`\x`);
`1:\x`→(`1:`,`\x`); `D:fake`→(`D:`,`fake`)). `isabs` LỆCH: `\fake`, `/fake` ⇒ True trên 3.11/3.12, False trên 3.13 ⇒ không gọi `isabs`.
`splitroot` (≥ 3.12) và `isreserved` (≥ 3.13) vắng trên 3.11 — kho khai Python ≥ 3.11 ⇒ không dùng. `ctypes.WinDLL` vắng trên Linux ⇒
`GetDriveTypeW` nạp lười, chỉ khi `os.name == "nt"`.

### 0.3 Nguyên mẫu M1/M2 (KHÔNG phải mã thi công; `c1/nguyen-mau/nguyen_mau_c1_r3.py`, `do_dot_bien_c1_r3.py`)

Đo 2026-11-19T11:05:43Z trên 3.11, 3.12, 3.13, cùng đầu ra (`nm-r3-out-3.1x.txt`): đúng mã/gốc/thành phần của 45 lượt N1 và đúng kết quả
18 lượt N2 (nguyên mẫu dùng tiền tố thử `ly_do:` và đã cắt `repr(x)[:200]`; tiền tố công khai chờ mã thi công). Bộ chạy đột biến kiểm neo khớp đúng 1 lần, so lượt đầu đổi màu với lượt
đích khai, trả rc ≠ 0 khi lệch: **36/36 khớp, rc 0** cả ba bản (`dot-bien-r3-3.1x.txt`). Một đột biến thử thêm — kiểm luật thành phần TRƯỚC `..` — đã bị LOẠI vì tương đương với đột biến 14: `..` cũng trượt luật `cuoi_cham_cach`, nên thứ tự ấy không đổi kết quả nào (phòng thủ hai lớp, không phải vùng mù). Bộ chạy so DÒNG đầu ra, chưa đo `TinHieuChotCa`,
nhãn hay hợp đồng cụm — các thứ ấy chỉ có trên mã thi công. Đó là các dòng §4b cột "đo".

### 0.4 Ràng buộc kề bên

- **Neo của fragment P2a** (`wp433_gws_cred_dich_ngoai_kho.py`, blob `2783e20c…`, 37 mục `_DB`) và **fragment packet 1**
  (`wp433_nlm_gws_dich_ngoai_kho.py`, 30 mục `_DB`): đo trên base bởi review lượt 4 (trên `96b6a33`, blob `tl_gws.py` `9ec027c2…`; giờ
  chính xác của lượt ấy không ghi — phiên thi hành đếm lại và ghi UTC theo §6) — mọi neo `_DB` đúng 1 lần; neo `_TU_KIEM`
  đúng 1 lần trừ đối chứng `tu_kiem_neo_lap` của packet 1 CỐ Ý khớp 2 lần (`_ghi_jar_nlm(nbase, nlm)`). Neo dễ chạm: `_kiem_dich_ghi(dest,
  "/", (*chuan[1], "credentials.json"))`, `"\ndef _dich_cred_gws("`, `return ly if not tp or ".." in tp else`, `if "\x00" in p or
  p.strip() == "":`, `ly = f"đường không hợp lệ: {repr(p)[:200]}"`, `for i in range(len(thanh_phan) + 1):`. Mã mới không chứa lại nguyên
  văn các chuỗi ấy; `_duong_dich_chuan` (POSIX) giữ nguyên.
- Fragment P2a trên nt đòi `(w, t, v) == (7, 27, 21)`; ba ca `mọi` của nó đi qua W4/W5 nên sau C1 đi nhánh nt mới (thư mục tạm cục bộ ⇒
  phải vẫn đạt). Fragment P2a và packet 1 chưa có biên nhận chạy trên Windows thật trong master lúc soạn.
- `.claude/dev/packet_loop.py:6408–6440` có mẫu bindings kernel32 (argtypes/restype tường minh, `use_last_error=True`, `GetDriveTypeW`).
  `.claude/` bị loại khỏi gói ⇒ C1 chép MẪU, không import.
- CI: `bundled-fragment check` kiểm bundled committed; manifest committed chỉ kiểm trên master; không có CI Windows bắt buộc; protocol
  §10.1 đòi T3 trên Windows + Linux cho integration SHA. Đo native: Desktop `DESKTOP-T9R33P2` (Developer Mode bật 19-11, `core.symlinks=true`),
  VM `tra-luat-win` dự phòng (§4c).

## 1. `write_set`

```
scripts/tl_gws.py
scripts/test_fragments/wp433_gws_cred_win_duong.py
scripts/tl_test_fragments_bundled.py
```

KHÔNG `RELEASE_MANIFEST.json`. `scripts/tl_test_fragments_bundled.py` theo tiền lệ phương án B (chủ kho 18-11-2026; P2a §1): chỉ sinh bằng
`generate_bundled_module_bytes(scripts/test_fragments)`. **Điều kiện trước khi cấp lease (E2):** comment của chủ kho trên #433 cấp ngoại lệ
ấy nêu đúng `packet_id` `GWS-CRED-DICH-NGOAI-KHO-C1`, đúng một tệp `scripts/tl_test_fragments_bundled.py` và sha256 của đặc tả này đã đóng
băng; lease trỏ URL comment. Comment `7002145681` (P2a) không phủ. Phiên land tái sinh `RELEASE_MANIFEST.json` trong commit land.

## 2. `ngoai_pham_vi`

- POSIX: không đổi hành vi nhánh `posix`; `_duong_dich_chuan` (POSIX) không sửa.
- Junction, mount point, reparse point khác: packet R (chốt reparse trong thân `_kiem_dich_ghi`). Trước khi R land, junction ở tổ tiên hay tại
  `cfgdir` CHƯA bị chặn trên Windows (symlink thì đã bị luật (b) `S_ISLNK` chặn).
- Đích qua mạng: UNC (mọi dạng mở bằng hai phân cách) và ổ có `GetDriveTypeW` khác REMOVABLE/FIXED bị TỪ CHỐI, không có ngoại lệ (chủ kho
  Q2 = D). Không định danh tệp, không `OpenFileById`.
- Phân loại đường cho W1–W3, W6: không.
- TOCTOU: như P2a §2 — kiểm theo TÊN rồi ghi theo TÊN; ánh xạ ổ (`subst`, `net use`) đổi giữa lúc kiểm và `os.replace` nằm ngoài bảo đảm;
  không ca nào đo khe này.
- Không sửa `ops/**`, `.github/**`, `scripts/tl_selftest.py`, fragment P2a, fragment packet 1, `RELEASE_MANIFEST.json`, `changelog.d/*`,
  `VERSION`, `CHANGELOG.md`, `SKILL.md`. Không thêm CI Windows.

## 3. `muc_tieu`

| # | mục tiêu | tệp |
|---|---|---|
| M1 | Hàm thuần `_phan_loai_duong_nt(p)` trên `ntpath` import tường minh (không `os.path`, `isabs`, `splitroot`, `isreserved`, `abspath`, `normpath`, `realpath`), trả tuple mà phần tử đầu là MÃ. Kiểm THEO THỨ TỰ, mã đầu tiên khớp thắng: (1) `"\x00" in p` ⇒ `nul`; (2) `p.strip() == ""` ⇒ `trang`; (3) `re.match(r"[\\/]{2}\?[\\/]", p)` ⇒ `thiet_bi_win32`; (4) `re.match(r"[\\/]{2}\.[\\/]", p)` ⇒ `thiet_bi_dos`; (5) `re.match(r"[\\/]\?\?[\\/]", p)` ⇒ `nt_doi_tuong`; (6) hai ký tự đầu đều là phân cách (`\` hoặc `/`, trộn được) ⇒ `unc`; (7) `d, r = ntpath.splitdrive(p)`: `d` `fullmatch` `[A-Za-z]:` thì `r == ""` ⇒ `o_tran`, `r[0]` không phải phân cách ⇒ `o_tuong_doi`, còn lại loại `o_tuyet_doi` với gốc `d.upper() + "\\"`; `d == ""` thì `p[0]` là phân cách ⇒ `goc_o`, còn lại loại `tuong_doi` (gốc `None`); `d` khác ⇒ `o_khac`; (8) tách `r` theo `\`/`/`, bỏ thành phần rỗng và `.`; còn `..` ⇒ `hai_cham`; (9) từng thành phần: chứa ký tự trong `<>:"\|?*` hoặc mã `\x01`–`\x1f` ⇒ `ky_tu_cam`; chứa surrogate đơn `\ud800`–`\udfff` ⇒ `ky_tu_cam`; `t.endswith((".", " "))` ⇒ `cuoi_cham_cach`; `fullmatch` không phân biệt hoa/thường `(CON\|PRN\|AUX\|NUL\|COM[0-9¹²³]\|LPT[0-9¹²³]\|CONIN\$\|CONOUT\$) *(\..*)?` ⇒ `ten_thiet_bi` (chặt hơn `isreserved` 3.13 ở `COM0`/`LPT0`, cố ý — chủ kho Q6); (10) hết ⇒ `(loại, gốc, thành_phần)`. Khoảng trắng ĐẦU tên, khoảng trắng GIỮA tên, Unicode thường (kể cả NBSP, DEL) được nhận. | `scripts/tl_gws.py` |
| M2 | `_duong_dich_chuan_nt(p, cwd, loai_o=None)` trả `(gốc, thành_phần)` hoặc lý do MỘT dòng đúng nguyên văn `"đường không hợp lệ: " + repr(x)[:200]`. Loại `tuong_doi`: phân loại `cwd` bằng M1; `cwd` khác `o_tuyet_doi` ⇒ lý do với `x = cwd`; ngược lại ghép THÀNH PHẦN `cwd + p` (không ghép chuỗi), gốc của `cwd`, và từ đây `x = cwd`. Loại khác `o_tuyet_doi` ⇒ lý do với `x = p`. Không còn thành phần nào (`C:\`, `.` khi `cwd` là gốc) ⇒ lý do với `x` hiện hành. `loai_o(gốc)` (mặc định `_loai_o_nt` = `GetDriveTypeW` nạp lười) không thuộc {2 REMOVABLE, 3 FIXED} ⇒ lý do với `x` hiện hành — tức ổ mạng (4), CD (5), RAM (6), không rõ (0, 1) đều bị từ chối, kể cả khi ổ ấy đến từ `cwd`. | `scripts/tl_gws.py` |
| M3 | Nhánh `os.name != "posix"` của `_dich_cred_gws` thành `return _dich_cred_gws_nt(cfgdir_tho)`. `_dich_cred_gws_nt(cfgdir_tho)` (KHÔNG tạo/ghi gì): `os.getcwd()` MỘT lần; M2 — lý do ⇒ `(None, lý_do)`; `dest = gốc + "\\".join((*tp, "credentials.json"))`; rồi dò `.git` BA trạng thái từ `ntpath.dirname(dest)` lên gốc trên hai chuỗi như `_trong_kho_git` (`abspath` và `realpath`): `os.lstat(<d>\.git)` thành công ⇒ `(dest, "nằm trong kho git: " + repr(d)[:200])`; `FileNotFoundError`/`NotADirectoryError` ⇒ chưa có, đi tiếp; `OSError` khác LAN RA (W4/W5 báo `ghi lỗi`) — vì `_trong_kho_git` nuốt mọi `OSError` (`tl_gws.py:1133–1134`, review lượt 6 đo bằng probe RAM: `PermissionError` khi dò marker ⇒ `_kiem_dich_ghi` trả `None`); sau đó trả `(dest, _kiem_dich_ghi(dest, gốc, (*tp, "credentials.json")))` — luật (b) liên kết ở MỌI tiền tố từ gốc ổ. Không sửa thân `_trong_kho_git`. `dest` là đường DUY NHẤT được kiểm, ghi và (W5) trả về. W4, W5 không đổi. Văn bản mới không chứa lại neo §0.4. | `scripts/tl_gws.py` |
| M4 | Hợp đồng lỗi: GIỮ sáu cụm của P2a, không thêm cụm. Từ chối của M1/M2 ⇒ `đường không hợp lệ`; kho ⇒ `nằm trong kho git`; liên kết ⇒ `là liên kết tượng trưng`; `OSError` (kể cả từ `GetDriveTypeW` lười hay `lstat`) ⇒ `ghi lỗi: <_safe_exc(e)>`. W4 một dòng `[bootstrap] ✗ <cụm>: .+`, rc 1, `degraded`; W5 `(False, "<cụm>: …")`; `cmd_gws_auth_load` một dòng, rc 2 — như P2a M3. Mọi từ chối xảy ra TRƯỚC writer: không tệp mới, không tệp tạm. | `scripts/tl_gws.py` |
| M5 | Fragment `scripts/test_fragments/wp433_gws_cred_win_duong.py`, `TEST_ID = "wp433_gws_cred_win_duong"`: khuôn fragment P2a, tự chứa, nạp `tl_gws` vào bộ nhớ, đột biến trên bản sao, neo khớp đúng 1 lần, phân hạng `TinHieuChotCa(AssertionError)` theo (loại tín hiệu, ca, lượt, nhãn), sổ `_LUOT_DU_KIEN` và `_DU_KIEN` viết riêng, trạng thái lượt `đạt`·`đỏ`·`bỏ_qua`·`chỉ_nt`, mọi đầu ra ra STDERR, khôi phục trong `finally`. Ca `nt` thay `_loai_o_nt` trên module ĐÃ NẠP; M2/M3 tra tên ấy LÚC GỌI. | fragment |
| M6 | Tái sinh `scripts/tl_test_fragments_bundled.py` bằng `generate_bundled_module_bytes(scripts/test_fragments)`; không sửa tay. | bundled |

## 4. `nghiem_thu`

Ký hiệu như P2a §4 (K = kho git tạm, T = thư mục tạm ngoài kho, gốc rig = `realpath(mkdtemp())`). Nền `mọi` hoặc `nt`; ca `nt` trên
nền khác: mọi lượt `chỉ_nt`. Mỗi lượt thu đủ hậu điều rồi so nhãn theo thứ tự ghi; nhãn đỏ đầu tiên là tín hiệu; ca dừng ở lượt đỏ đầu.
"W5 đúng" = `(False, s)`, `s` `fullmatch` `<cụm>: .+`, một dòng. "Lý do M2 đúng(x)" = BẰNG nguyên văn `"đường không hợp lệ: " + repr(x)[:200]`.

| # | ca (nền) | lượt và tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|---|
| N1 | `phan_loai_nt` (mọi), gọi thẳng `_phan_loai_duong_nt` | 45 lượt, mỗi lượt nhãn [`ma`] rồi (loại nhận) [`goc_tp`]. Nhận: `p01` `C:\x`⇒`o_tuyet_doi`,`C:\`,(`x`); `p02` `C:/x`, `p03` `c:\x` ⇒ như `p01`; `p04` `C:\a/b\c`⇒(`a`,`b`,`c`); `p05` `fake`⇒`tuong_doi`,`None`,(`fake`); `p06` `C:\x\.\y\\`⇒(`x`,`y`); `p07` `D:\Quốc hội\tra-luat`⇒`D:\`,(`Quốc hội`,`tra-luat`); `p08` `C:\ a`⇒(` a`,). Từ chối (mã): `p09` `a\x00b` `nul`; `p10` `   ` `trang`; `p11` `\\?\C:\x`, `p12` `//?/C:/x`, `p13` `\\?\UNC\s\sh` `thiet_bi_win32`; `p14` `\\.\pipe\x`, `p15` `//./C:/x` `thiet_bi_dos`; `p16` `\??\C:\x` `nt_doi_tuong`; `p17` `C:` `o_tran`; `p18` `D:fake` `o_tuong_doi`; `p19` `\fake`, `p20` `/fake` `goc_o`; `p21` `\\server\share\x`, `p22` `//server/share/x`, `p23` `/\server\share\x`, `p24` `\\server`, `p25` `\\\server\share`, `p26` `\\server\\share` `unc`; `p27` `1:\x` `o_khac`; `p28` `C:\a\..\b`, `p29` `a/../b`, `p30` `..` `hai_cham`; `p31` `C:\x:ads`, `p32` `C:\a\|b`, `p33` `C:\a` + `\ud800` + `b`, `p34` `C:\a` + `\x01` + `b` `ky_tu_cam`; `p35` `C:\a.\b`, `p36` `C:\a ` `cuoi_cham_cach`; `p37` `C:\CON`, `p38` `C:\nul.txt`, `p39` `C:\com1\x`, `p40` `C:\NUL .txt`, `p41` `C:\CONIN$`, `p42` `C:\COM0` `ten_thiet_bi`; thứ tự luật thành phần khi hai luật cùng khớp: `p43` `C:\a<.` ⇒ `ky_tu_cam` (trước `cuoi_cham_cach`), `p44` `C:\CON.x ` ⇒ `cuoi_cham_cach` (trước `ten_thiet_bi`); nhận: `p45` `C:\a` + `\x7f` + `b` + `\u00a0` ⇒ `o_tuyet_doi`,`C:\`,(nguyên tên) (DEL, NBSP cuối được nhận). Base: hàm chưa có ⇒ lượt đầu đỏ (`ngoai_le_la`). | §4b dòng 1–22, 33–35, 40 (đo trên nguyên mẫu §0.3). |
| N2 | `chuan_nt` (mọi), gọi thẳng `_duong_dich_chuan_nt` với `loai_o` giả (trả 3 trừ khi ghi khác) | `q01` (`fake`, `C:\cwd`) ⇒ [`ket_qua`] (`C:\`, (`cwd`,`fake`)); `q02` (`a\b`, `c:/cwd`) ⇒ (`C:\`, (`cwd`,`a`,`b`)); `q03` (`fake`, `\\s\sh\d`) ⇒ [`ly_do`] đúng(`\\s\sh\d`); `q04` (`fake`, `D:rel`) ⇒ [`ly_do`] đúng(`D:rel`); `q05` (`fake`, `\\?\C:\cwd`) ⇒ [`ly_do`] đúng(cwd); `q06` (`C:\`) ⇒ [`goc_rong`] đúng(`C:\`); `q07` (`x\n\..`) ⇒ [`mot_dong`] đúng(p), không `\n`; `q08` (`x`, `C:\`) ⇒ [`ket_qua`] (`C:\`, (`x`,)); `q09` (`.`, `C:\cwd`) ⇒ (`C:\`, (`cwd`,)); `q10` (`.`, `C:\`) ⇒ [`goc_rong`] đúng(`C:\`); `q11` (`Z:\x`, `loai_o` ⇒ 4) ⇒ [`ly_do`] đúng(p); `q12` (`E:\x`, ⇒ 5) ⇒ [`ly_do`]; `q13` (`F:\x`, ⇒ 2) ⇒ [`ket_qua`] (`F:\`, (`x`,)); `q14` (`fake`, `Z:\cwd`, ⇒ 4) ⇒ [`ly_do`] đúng(cwd); `q15` (`G:\x`, ⇒ 0), `q16` (`H:\x`, ⇒ 1), `q17` (`R:\x`, ⇒ 6) ⇒ [`ly_do`] đúng(p); `q18` (`D:` + 300 × `a`, loại `o_tuong_doi`) ⇒ [`cat_200`] lý do BẰNG `"đường không hợp lệ: " + repr(p)[:200]` (`len(repr(p)) = 305`). | §4b dòng 23–29, 36–38, 41. |
| N3 | `tich_hop_nt` (nt) — W4 fixture gws chuẩn của P2a, W5 với `_public_curl_bytes` giả; bộ đếm lời gọi writer và `os.lstat` | `W5.trong_kho` `cfgdir = <K>\gwscfg` ⇒ [`ly_do`] W5 đúng `nằm trong kho git`, sạch(K); `W4.trong_kho` cùng `cfgdir` ⇒ [`w4`] rc 1, đúng một dòng `[bootstrap] ✗ nằm trong kho git: …`; `W5.tuong_doi` cwd `<T>`, `cfgdir = cfg` ⇒ [`ket_qua`] `(True, d)`, `d` = dạng M2 của `<T>\cfg\credentials.json`, tệp đúng byte; `W5.o_thuong` `cfgdir` = `<T>\o` viết ổ thường, gạch `/` ⇒ [`ket_qua`] `d` ổ hoa, chỉ `\`; `W5.o_tuong_doi` `<ổ của T>:cfg` ⇒ [`ly_do`] `đường không hợp lệ`; `W5.hai_cham` `<T>\x\..\cfg` ⇒ [`ly_do`] `đường không hợp lệ`; `W5.unc` `\\wp433-khong-ton-tai.invalid\s\x` ⇒ [`ly_do`] `đường không hợp lệ`, 0 lời gọi `lstat`/writer (không chạm mạng); `W5.sl_to_tien` `<T>\sl\a` (`sl` symlink thư mục → `<T>\that`) ⇒ [`lien_ket`] chi tiết `repr(<T>\sl)`, `that` không tệp mới; `W5.loai_o_loi` `cfgdir = <T>\c2`, `_loai_o_nt` giả (thay trên module đã nạp) ném `OSError("wp433-c1-loai-o")` ⇒ [`hop_dong`] W5 `(False, "ghi lỗi: OSError")`, writer 0, không `.auth.json.*`; `W4.loai_o_loi` cùng đồ giả, fixture gws chuẩn ⇒ [`hop_dong`] rc 1, đúng một dòng `[bootstrap] ✗ ghi lỗi: OSError`, không in `✓ gws cred`, writer 0; `W5.git_loi` `cfgdir = <T>\pk\gws` với `<T>\pk\.git` có thật, bọc `os.lstat` ném `PermissionError("wp433-c1-git")` cho ĐÚNG `<T>\pk\.git` ⇒ [`hop_dong`] W5 `(False, "ghi lỗi: PermissionError")`, writer 0, không `.auth.json.*`; `W5.realpath_loi` `cfgdir = <T>\rp\gws` (`<T>\rp` có thật, không có `.git`), bọc `os.path.realpath` của module đã nạp: gọi với `strict=True` trên `<T>\rp` ném `PermissionError("wp433-c1-rp")`, gọi khác đi hàm thật ⇒ [`hop_dong`] W5 `(False, "ghi lỗi: PermissionError")`, writer 0, không `.auth.json.*`. Mọi lượt từ chối: writer 0 lần, không `.auth.json.*`. Danh sách cho phép `bỏ_qua`: ĐÚNG lượt `W5.sl_to_tien`, chỉ khi `os.symlink` trên CHÍNH thư mục fixture ném `OSError` có `winerror == 1314`; lỗi khác ⇒ `đỏ` với `probe symlink: <repr(lớp, errno, winerror)>`. | §4b dòng 30–32, 39, 42–44. |
| N4 | tự kiểm | (a) `_DU_KIEN` == tập ID `_DB` (đếm cả số lần); mỗi mục giết đúng (loại tín hiệu, ca, lượt, nhãn). (b) `_LUOT_DU_KIEN` viết riêng; tập và số lần (ca, lượt) đã ghi trạng thái BẰNG sổ: 3 ca / 45 + 18 + 12 = **75** lượt. (c) MỘT dòng tổng kết ra STDERR dạng P2a (`CA`, `LUOT`, `DOT BIEN`, `HONG`, `TU_KIEM`, cột `chỉ_nt` thay `chỉ_posix`); `run` True chỉ khi: `b == c`, `y == z`, `f == g`, `i == 0`, `a == b + w`, `x == y + u + t`, `e == f + h + v`, `x == 75`, `e == len(_DU_KIEN)`, `h == u` và `h ≤ 1` (chỉ đột biến 32 theo lượt duy nhất được phép bỏ qua), mọi tự kiểm đúng hạng; trên nền khác nt: `t = 12`, `v = 7`, `u = h = 0`; trên nt: `t == v == 0`. (d) Tự kiểm phân hạng: `tu_kiem_doi_kieu` — trên bản RAM chèn vào đầu thân `_phan_loai_duong_nt` một lớp `TinGia(AssertionError)` định nghĩa tại chỗ, mang ĐÚNG thuộc tính `ca = "phan_loai_nt"`, `luot = "p01"`, `nhan = "ma"`, và `try: raise AttributeError("wp433-c1-tu-kiem")` / `except Exception: raise TinGia(...)`; đường đi tới bộ phân hạng giữ nguyên (fragment không bọc lại ngoại lệ ấy) ⇒ bộ phân hạng chuẩn trả `TIN_DUNG_GIA` (lớp không phải `TinHieuChotCa` dù tuple khớp) và ngoại lệ có `__context__` kiểu `AttributeError`; đối chứng: bộ phân hạng bỏ RIÊNG phép so lớp, giữ so tuple ⇒ `GIET` ⇒ `run` False, `tu_kiem_chu_thich` (⇒ `SONG_SOT`), `tu_kiem_sai_luot` (CHÍNH đột biến 3, chỉ khai lượt `p12` ⇒ `TIN_DUNG_GIA`). (e) stdout của `run` rỗng. | Trên bản sao fragment: thêm ID vào `_DU_KIEN` ⇒ (a) False; lặp một lượt ⇒ (b) False; gỡ một lượt ⇒ (b) False; ép `bỏ_qua` lượt ngoài danh sách cho phép ⇒ False; ép `bỏ_qua` symlink khi probe thành công ⇒ False; cố định `os.name == "nt"` cho bộ phân loại bỏ qua, probe ném `PermissionError` `winerror == 5` ⇒ lượt `đỏ`, False; bộ phân hạng bỏ so lượt ⇒ `tu_kiem_sai_luot` ra `GIET` ⇒ False; in tổng kết ra stdout ⇒ (e) đỏ. |
| N5 | gate | Exact head: `--selftest` N/N hai số bằng nhau, N = N_base + 1, DELTA 0 ca đỏ mới (base/head dựng trong CÙNG một lệnh); `test-fragments-check --json` ⇒ `ok: true`; `bundle_fragment_check.py --json` ⇒ `ok: true`, `failed: []`; với MỌI neo trong `_DB` và `_TU_KIEM` của fragment P2a và fragment packet 1: số lần khớp trên candidate BẰNG trên base (`_DB` = 1; `tu_kiem_neo_lap` = 2), đếm bằng nạp hai fragment rồi đọc bảng; hai fragment ấy `run` True trên Linux; `python3 ops/cloud_agent_creds_test.py` `TONG: DAT`, từng ca bằng base; lane worker `release-manifest` tạm + `release-verify --strict` ⇒ `ok: true`, `expected_file_count == checked_file_count`; `ruff check --select F` delta 0 trên `tl_gws.py`, 0 trên fragment và bundled; `git diff --check` rc 0; `doctrine-scan`, `adr-song` rc 0; numstat dưới `set -o pipefail`: TRƯỚC numstat, `git rev-parse` base và head rồi so exact OID với base của lease và head đã ghim; numstat đúng 3 dòng, mỗi dòng `^[0-9]+\t[0-9]+\t<đường>$`, tập đường == §1, tổng cột thêm ≤ 450. Gate T3 theo protocol §10.1: phiên land tái sinh `RELEASE_MANIFEST.json` rồi ghim integration SHA/tree; trên CHÍNH SHA/tree ấy, full selftest + TOÀN BỘ release gates của lane LAND (D12) trên CẢ Windows và Linux; D5 không thay T3; T4 chỉ tái dùng T3 khi exact identity khớp. | Neo: chèn thêm một bản của một neo `_DB` (mỗi fragment một lần) ⇒ đỏ; xoá một bản neo `tu_kiem_neo_lap` ⇒ 1 ≠ 2 ⇒ đỏ. Selftest/bundled/manifest: như P2a N10–N11. Numstat dựng tay: tổng 451 ⇒ đỏ; đường ngoài §1 ⇒ đỏ; thiếu một đường ⇒ đỏ; cột `-` ⇒ đỏ. OID: base CÓ THẬT nhưng sai (vd. `11bd033`) ⇒ đỏ ở bước so OID (numstat của nó vẫn rc 0 — đo lượt 4 review); ref không tồn tại ⇒ `git` rc ≠ 0 và pipeline giữ lỗi. `cloud_agent_creds_test`, `doctrine-scan`, `adr-song`, `ruff`: gate kế thừa, phép đỏ thuộc suite của chúng; packet không thêm. |
| N6 | đo native (§4c) | Hồ sơ PR ghi lệnh, shell, exact head/tree, đầu ra thô, rc và kết luận của MỌI phép bắt buộc ở §4c. | Phép bắt buộc thiếu, trái kỳ vọng hoặc `KHÔNG ĐO ĐƯỢC` ⇒ không land (§6). |

### 4b. Bảng đột biến — NGUỒN DUY NHẤT

Luật như P2a §4b (lượt gọi, `ngoai_le_la`, mỗi đột biến chỉ chạy ca đích, lượt đích = lượt ĐẦU TIÊN nó làm đỏ, giết chỉ khi khớp loại tín
hiệu + ca + lượt + nhãn). Neo trên NGUỒN CANDIDATE. Nền `nt` ⇒ đếm `chỉ_nt` trên nền khác. Cột "đo" = mọi lượt đổi màu trên nguyên mẫu
§0.3, lượt đầu là đích; "lập luận" = chưa chạy.

| # | đột biến (phép thay) | ca · lượt | nhãn | cơ chế | nền | đo |
|---|---|---|---|---|---|---|
| 1 | `db_nt_bo_nul` (bỏ (1)) | `phan_loai_nt` · `p09` | `ma` | H | mọi | `p09` |
| 2 | `db_nt_bo_trang` (bỏ (2)) | · `p10` | `ma` | H | mọi | `p10` |
| 3 | `db_nt_bo_win32` (bỏ (3)) | · `p11` | `ma` | H | mọi | `p11`–`p13` (⇒ `unc`) |
| 4 | `db_nt_bo_dos` (bỏ (4)) | · `p14` | `ma` | H | mọi | `p14`,`p15` |
| 5 | `db_nt_bo_nt` (bỏ (5)) | · `p16` | `ma` | H | mọi | `p16` (⇒ `goc_o`) |
| 6 | `db_nt_bo_unc` (bỏ (6)) | · `p21` | `ma` | H | mọi | `p21`–`p26` (⇒ `o_khac`) |
| 7 | `db_nt_unc_chi_gach_nguoc` ((6) chỉ nhận `\\`) | · `p22` | `ma` | H | mọi | `p22`,`p23` |
| 8 | `db_nt_o_tran` (`r == ""` ⇒ coi như `\`) | · `p17` | `ma` | H | mọi | `p17` |
| 9 | `db_nt_o_tuong_doi` (bỏ kiểm phân cách sau ổ) | · `p18` | `ma` | H | mọi | `p18`,`q04`,`q18` |
| 10 | `db_nt_o_chi_hoa` (`[A-Z]:`) | · `p03` | `ma` | H | mọi | `p03`,`q02` |
| 11 | `db_nt_khong_hoa_o` (bỏ `.upper()`) | · `p03` | `goc_tp` | H | mọi | `p03`,`q02` |
| 12 | `db_nt_goc_o_tuyet_doi` (bỏ `goc_o`) | · `p19` | `ma` | H | mọi | `p19`,`p20` |
| 13 | `db_nt_chi_gach_nguoc` (tách chỉ theo `\`) | · `p02` | `goc_tp` | H | mọi | `p02`,`p04`,`p29`,`q02` |
| 14 | `db_nt_bo_hai_cham` | · `p28` | `ma` | H | mọi | `p28`–`p30` |
| 15 | `db_nt_bo_ky_tu_cam` (bỏ dòng lớp ký tự cấm) | · `p31` | `ma` | H | mọi | `p31`,`p32`,`p34`,`p43` |
| 16 | `db_nt_bo_surrogate` | · `p33` | `ma` | H | mọi | `p33` |
| 17 | `db_nt_bo_dieu_khien` (bỏ `\x01-\x1f` khỏi lớp) | · `p34` | `ma` | H | mọi | `p34` |
| 18 | `db_nt_bo_cuoi_cham` | · `p35` | `ma` | H | mọi | `p35`,`p36`,`p44` |
| 19 | `db_nt_bo_ten_tb` | · `p37` | `ma` | H | mọi | `p37`–`p42` |
| 20 | `db_nt_ten_tb_khong_cach` (bỏ ` *` trong regex) | · `p40` | `ma` | H | mọi | `p40` |
| 21 | `db_nt_bo_conin` (bỏ `CONIN$`/`CONOUT$`) | · `p41` | `ma` | H | mọi | `p41` |
| 22 | `db_nt_o_khac_nhan` (`d` khác ⇒ nhận như ổ) | · `p27` | `ma` | H | mọi | `p27` |
| 23 | `db_nt_cwd_khong_kiem` (cwd sai loại ⇒ ghép chuỗi `ntpath.join(cwd, p)` rồi chuẩn hoá lại) | `chuan_nt` · `q03` | `ly_do` | H | mọi | `q03`–`q05` (lý do nêu đường ghép ≠ cwd) |
| 24 | `db_nt_goc_rong` (bỏ chốt không còn thành phần) | · `q06` | `goc_rong` | H | mọi | `q06`,`q10` |
| 25 | `db_nt_bo_loai_o` (bỏ chốt loại ổ) | · `q11` | `ly_do` | H | mọi | `q11`,`q12`,`q14`–`q17` |
| 26 | `db_nt_loai_o_moi_loai` (chỉ từ chối loại 4) | · `q12` | `ly_do` | H | mọi | `q12`,`q15`–`q17` |
| 27 | `db_nt_bo_removable` (chỉ loại 3 là cục bộ) | · `q13` | `ket_qua` | H | mọi | `q13` |
| 28 | `db_nt_loai_o_chi_tuyet_doi` (chỉ kiểm loại ổ khi `p` tuyệt đối) | · `q14` | `ly_do` | H | mọi | `q14` |
| 29 | `db_nt_khong_repr` (lý do nội suy `x` thô) | · `q07` | `mot_dong` | H | mọi | lập luận |
| 30 | `db_nt_bo_chot` (nhánh nt về base) | `tich_hop_nt` · `W5.trong_kho` | `ly_do` | H | nt | lập luận (§0.1: base ghi vào kho) |
| 31 | `db_nt_ghi_duong_tho` (`dest` trả về = `ntpath.join(cfgdir_tho, "credentials.json")`, vẫn kiểm đường chuẩn) | · `W5.tuong_doi` | `ket_qua` | H | nt | lập luận |
| 32 | `db_nt_goc_cfg` (`_kiem_dich_ghi(dest, <cfgdir chuẩn>, ("credentials.json",))`, bỏ tổ tiên) | · `W5.sl_to_tien` | `lien_ket` | H | nt | lập luận (như P2a 33) |
| 33 | `db_nt_dao_ky_tu_cuoi` (kiểm `cuoi_cham_cach` trước `ky_tu_cam`) | `phan_loai_nt` · `p43` | `ma` | H | mọi | `p43` |
| 34 | `db_nt_dao_cuoi_ten_tb` (kiểm `ten_thiet_bi` trước `cuoi_cham_cach`) | · `p44` | `ma` | H | mọi | `p44` |
| 35 | `db_nt_cam_nbsp_del` (thêm `\x7f`, `\u00a0` vào lớp ký tự cấm) | · `p45` | `ma` | H | mọi | `p45` |
| 36 | `db_nt_loai_o_nhan_0` (nhận loại 0) | `chuan_nt` · `q15` | `ly_do` | H | mọi | `q15` |
| 37 | `db_nt_loai_o_nhan_1` (nhận loại 1) | · `q16` | `ly_do` | H | mọi | `q16` |
| 38 | `db_nt_loai_o_nhan_6` (nhận loại 6) | · `q17` | `ly_do` | H | mọi | `q17` |
| 39 | `db_nt_nuot_loi_loai_o` (`_dich_cred_gws_nt` bọc `loai_o` trong `try … except OSError` coi như 3) | `tich_hop_nt` · `W5.loai_o_loi` | `hop_dong` | H | nt | lập luận |
| 40 | `db_nt_thanh_phan_truoc_namespace` (ngay sau (1), áp luật (9) cho mọi đoạn tách theo `\`/`/` của `p` trừ đoạn đầu và `""`, `.`, `..`) | `phan_loai_nt` · `p11` | `ma` | H | mọi | `p11`–`p13`,`p15`,`p16` (⇒ `ky_tu_cam`) |
| 41 | `db_nt_bo_cat_200` (lý do dùng `repr(p)` không cắt) | `chuan_nt` · `q18` | `cat_200` | H | mọi | `q18` |
| 42 | `db_nt_w4_nuot_loi_dich` (CHỈ ở W4: tách lời gọi `_dich_cred_gws` ra `try` riêng, `except OSError` đặt `ly_gws = "ghi lỗi"` không chi tiết; nhánh lỗi writer giữ nguyên) | `tich_hop_nt` · `W4.loai_o_loi` | `hop_dong` | H | nt | lập luận (dòng lỗi không `fullmatch` `: .+`) |
| 43 | `db_nt_git_nuot_loi` (dò `.git` của M3 coi mọi `OSError` là "chưa có") | `tich_hop_nt` · `W5.git_loi` | `hop_dong` | H | nt | lập luận (probe RAM lượt 6: nuốt ⇒ `None`) |
| 44 | `db_nt_realpath_khong_strict` (chuỗi thật gọi `os.path.realpath(a)` non-strict) | `tich_hop_nt` · `W5.realpath_loi` | `hop_dong` | H | nt | lập luận (đồ giả chỉ ném khi `strict=True` ⇒ bản non-strict trả đường và W5 ghi) |

Tổng: **44** đột biến (`mọi` 37, `nt` 7), E: 0. Cặp chung (ca, lượt, nhãn) CÓ CHỦ Ý, duy nhất: 3/40 (`p11`, `ma`) — mọi đầu vào thiết bị đều
thuộc đúng một trong ba chốt (3)–(5), nên lượt đầu đỏ của phép đảo thứ tự 40 luôn trùng lượt đầu đỏ của đột biến bỏ chốt sở hữu nó; hai đột
biến cho hai mã khác nhau (`unc` / `ky_tu_cam`), cả hai bị giết đúng đích. Cặp chung (ca, lượt) khác nhãn: 10/11 (`p03`, `ma`/`goc_tp`); 25/26/28/36–38 khác
lượt nhờ `q11`/`q12`/`q14`–`q17`. Đột biến 30 chỉ cấp bằng chứng tại `W5.trong_kho` (ca dừng ở đó). `W4.trong_kho`, `W5.o_thuong`,
`W5.o_tuong_doi`, `W5.hai_cham`, `W5.unc`: KHÔNG có đột biến đích — là phép đo tích hợp trực tiếp của M1/M2/M4 trên Windows
thật (đúng/sai đọc thẳng từ hậu điều), răng của luật đến từ N1/N2 (`W4.loai_o_loi` có đột biến 42); không khai chúng "đổi màu dưới" đột biến nào.

### 4c. Đo native Windows (`DESKTOP-T9R33P2`, dự phòng VM `tra-luat-win`)

Chung: ghim exact head/tree; lệnh thường chạy trong `cmd.exe`, mở đầu `chcp 65001` và `set PYTHONIOENCODING=utf-8`; lệnh **[ADMIN]** chạy
nguyên văn trong **PowerShell mở bằng Run as Administrator** do chủ kho thao tác; gọi `python` (không giả định `python3`); ghi `python -VV`,
rc và đầu ra thô từng bước. Rig (một script Python dùng một lần, không vào kho) dựng `%TEMP%\wp433c1-<giờ>` với kho tạm K (`git init`) và
thư mục ngoài kho T; chọn ký tự ổ CÒN TRỐNG (kiểm trước khi dùng); dọn đúng tài nguyên mình tạo trong `finally`; KHÔNG ghi vào kho thật.
Gọi `tl_gws` offline: nạp `scripts/tl_gws.py`, `bind`, thay `_public_curl_bytes`/`_gas` bằng đồ giả như fragment P2a, bọc
`_ghi_nguyen_tu_0600` và `os.lstat` bằng bộ đếm, rồi gọi `_dich_cred_gws` hoặc `_gws_auth_load`. Chạy một fragment:
`python -B -c "import importlib.util, sys; sys.path.insert(0, 'scripts'); import tl; s = importlib.util.spec_from_file_location('frag', '<fragment>'); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); r = m.run(tl); print('run() ->', r); sys.exit(0 if r else 1)"`.

| # | bắt buộc | admin | dựng / lệnh | kỳ vọng | khi không dựng được |
|---|---|---|---|---|---|
| D1 | không | không | `ver`; `reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\AppModelUnlock /v AllowDevelopmentWithoutDevLicense`; `git config --get core.symlinks`; hệ tệp và `GetDriveTypeW` của ổ chứa `%TEMP%` và ổ chứa kho thật | ghi lại | KHÔNG ĐO ĐƯỢC từng mục |
| D3 | có | không | `os.lstat` trên gốc ổ chứa T (`X:\`) | thành công (gốc M2 `lstat` được) | thất bại ⇒ revision |
| D4 | có (vế `cmd`) | không | `os.getcwd()` in BỞI tiến trình Python chạy từ `cmd` ở T; (tuỳ chọn) từ PowerShell sau `Set-Location` vào T | dạng `X:\…` mà M1 nhận `o_tuyet_doi`, không tiền tố `\\?\`; khác ⇒ revision | vế PowerShell KHÔNG ĐO ĐƯỢC không chặn |
| D5 | có | không | `run(tl)` của fragment C1, fragment P2a, fragment packet 1 (lệnh mẫu trên), mỗi cái một tiến trình; ghi dòng tổng kết stderr | mỗi `run()` True; C1: `chỉ_nt = 0`, `bỏ_qua` chỉ `W5.sl_to_tien` khi thiếu quyền symlink; P2a `(w, t, v) == (7, 27, 21)`; packet 1 theo luật bỏ qua của nó | không có |
| D8 | có nếu K có alias 8.3 hoặc 8.3 bật | không (trừ nhánh dự phòng) | Rig đặt tên K dài > 8 ký tự; LUÔN chạy `fsutil 8dot3name query <ổ T>:` VÀ `dir /x` trên THƯ MỤC CHA của K; có tên ngắn thực tế thì đo (bất kể chính sách); `_dich_cred_gws(<cha>\<tên ngắn K>\gws)`; ghi riêng `_trong_kho_git` chỉ trên chuỗi `abspath` và chỉ trên `realpath` của cha `dest`; rồi chạy cùng `cfgdir` qua `_gws_auth_load` (tải giả, backend thật, bộ đếm writer) | helper: `nằm trong kho git`; `_gws_auth_load`: `(False, s)` cụm `nằm trong kho git`, writer 0, không tệp mới hay `.auth.json.*` trong K. Phép này đo việc CHẶN tên ngắn, không quy công cho `realpath` (chuỗi từ vựng có thể tự thấy `.git` qua tên ngắn) | chính sách tắt VÀ `dir /x` xác nhận K không có tên ngắn ⇒ KHÔNG ĐO ĐƯỢC, không chặn. Chính sách bật mà K không có tên ngắn ⇒ dự phòng **[ADMIN]** PowerShell `fsutil file setshortname "<K>" WP433K~1` rồi đo lại; vẫn không có ⇒ chuyển rig sang VM `tra-luat-win`; không đo được ở đâu ⇒ KHÔNG ĐO ĐƯỢC và CHẶN land |
| D9 | có | không | Tên Unicode THÔNG THƯỜNG: `_dich_cred_gws` rồi writer với `cfgdir` = `<T>\Quốc hội\gws` và `<K>\Quốc hội\gws` | T: ghi được, tệp đúng; K: `nằm trong kho git`, writer 0 | không có |
| D10 | có | **có** (chỉ tạo/xoá share) | Shell THƯỜNG: `whoami` ⇒ `<P>`; `net share wp433c1` phải báo KHÔNG tồn tại (rc ≠ 0) trước khi tạo. **[ADMIN]** PowerShell nguyên văn (một dòng, đã trích dẫn): `net share "wp433c1=<đường T>" '/grant:<P>,FULL'` rồi `$LASTEXITCODE`. Shell THƯỜNG (KHÔNG phải admin — ổ ánh xạ của phiên admin không thấy ở phiên thường): `net use <Z>: \\localhost\wp433c1`; đối chứng dương: `os.path.isdir("<Z>:\\")` đúng và `GetDriveTypeW("<Z>:\\") == 4`. Rồi qua `_gws_auth_load` (tải giả, `_loai_o_nt` THẬT bọc bộ quan sát gọi xuyên, bộ đếm `lstat`/writer) với `cfgdir` = `\\localhost\wp433c1\x`, = `<Z>:\x`, và = `x` khi cwd là `<Z>:\` (ghi `repr(os.getcwd())` trong CHÍNH tiến trình gọi W5; M1 phải phân loại nó `o_tuyet_doi` gốc `<Z>:\`) | cả ba `(False, "đường không hợp lệ: …")` đúng `repr` của `x` theo M2; lượt UNC: 0 lời gọi `_loai_o_nt`; hai lượt `<Z>:`: ĐÚNG một lời gọi `_loai_o_nt("<Z>:\\")` trả 4; 0 lời gọi `lstat` trên đường đích, writer 0, không tệp mới dưới T. Rời cwd `<Z>:` trước khi dọn. Dọn: shell thường `net use <Z>: /delete`; **[ADMIN]** `net share wp433c1 /delete` CHỈ khi chính lượt này đã tạo share | thiếu admin hoặc đối chứng dương thất bại ⇒ KHÔNG ĐO ĐƯỢC ⇒ không land |
| D11 | có | không | `subst <S>: <K>\sub` (rig tạo và kiểm `<K>\sub` trước) và `subst <S2>: <T>`, kiểm cả hai ánh xạ (`subst` liệt kê, `os.path.isdir`); `_dich_cred_gws` với `<S>:\gws` khi `<K>\sub\gws` (a) đã có, (b) chưa có; và `<S2>:\gws`; ghi `GetDriveTypeW("<S>:\\")` và `os.path.realpath` của CHÍNH cha `dest` (`<S>:\gws`) ở cả (a), (b), so `normcase` với `<K>\sub\gws` | `<S>`: (a), (b) `nằm trong kho git`, writer 0, `realpath` = `<K>\sub\gws`; `<S2>`: `("<S2>:\\gws\\credentials.json", None)`. Rồi chạy (a), (b) qua `_gws_auth_load` (tải giả, backend thật, bộ đếm writer): `(False, s)` cụm `nằm trong kho git`, writer 0, không tệp mới hay `.auth.json.*` dưới `<K>\sub`; và `<S2>` qua `_gws_auth_load`: `(True, d)`, tệp đúng byte (đối chứng ngoài kho). `<S>` không bị chặn ⇒ DỪNG, revision (phương án: nhận diện `subst` bằng `QueryDosDeviceW`). Dọn `subst <S>: /d`, `subst <S2>: /d`, ghi rc từng lệnh | không có |
| D12 | có (T3) | không | Phiên land tái sinh `RELEASE_MANIFEST.json` trong commit land rồi ghim integration SHA/tree. Trên CHÍNH SHA/tree ấy, cả Windows và Linux: `python scripts/tl.py --selftest` (N/N hai số bằng nhau) và MỌI bước release gate của lane LAND trong `.github/workflows/ci.yml` đọc TẠI SHA ấy (gồm `release-verify RELEASE_MANIFEST.json --strict --json` với rc 0, `ok: true`, hai trường số nguyên `expected_file_count` và `checked_file_count` CÓ MẶT và bằng nhau — thiếu trường là đỏ — và `release-bundle` hai lần cùng sha256); hồ sơ liệt kê từng lệnh, rc, đầu ra | mọi bước xanh trên cả hai nền, cùng SHA/tree | thiếu một bước, một nền hoặc sai identity ⇒ T3 chưa đạt ⇒ không land |

## 5. `pham_vi_e`

Không chạm E4, E5: chỉ sửa mã đường ghi; ca fragment dùng giá trị giả, HOME/cfgdir tạm, đồ giả thay tải Drive; không LIVE, không đẩy
Package. D10 tạo/xoá một share TẠM trỏ vào thư mục tạm bằng shell admin của chủ kho; D10/D11 tạo/xoá ổ ánh xạ và `subst` TẠM — thao tác cục
bộ, không chạm dữ liệu kho hay credential thật.

## 6. `luat_dung`

- Trần lời gọi Codex theo dòng khai `ADR-0055`; chạm trần ⇒ Review Rescue Checkpoint; xin tăng mang **E2**.
- Trần kích thước theo dòng khai `ADR-0053` (≤ 6 tệp, ≤ 450 dòng thêm), đo bằng numstat thật (N5) TRƯỚC khi công bố; vượt ⇒ DỪNG, không
  push, không cắt ca; nâng trần là quyết định của chủ kho — **E2**.
- Trước khi đóng băng và trước mỗi bước công bố: chạy lại ba phép đo mục *Hiệu lực* của `ADR-0053` và `ADR-0055` trên ref mới của nhánh
  mặc định cho hai OID ở dòng khai, và đo lại các dữ kiện thay đổi được của §0 (OID base, blob `tl_gws.py`, đếm neo §0.4), ghi exact OID,
  giờ UTC và rc; một phép sai ⇒ dừng, revision.
- `_kiem_dich_ghi`, `_ghi_nguyen_tu_0600`, `_trong_kho_git`, `_dich_cred_gws` trên base thật khác §0.1, hoặc cần sửa thân ngoài M3 ⇒ dừng, revision.
- Một neo §0.4 lệch số lần so với base ⇒ dừng, revision.
- Phép native bắt buộc (§4c) thiếu, trái kỳ vọng hoặc `KHÔNG ĐO ĐƯỢC` ⇒ không land; D3, D4 hoặc D11 trái kỳ vọng ⇒ revision. Thiếu máy ⇒ hỏi
  chủ kho — **E2**, mang theo số lời gọi Codex đã dùng/trần, tài nguyên còn thiếu và danh sách phép cần nó. Lệnh **[ADMIN]** do chủ kho tự
  chạy (Q9 đã quyết), không phải điểm hỏi mới.
- Chưa có comment cấp ngoại lệ bundled cho đúng `packet_id` trên #433 ⇒ không cấp lease (**E2**).
- Đặc tả không thuộc Mission ⇒ chờ chủ kho duyệt băm theo `ADR-0067` — **E2**.

## 7. `hinh_dang_ke_thua`

Bộ đếm kế thừa từ P2a §7 / packet 1: **mức đặc tả 3, mức mã 0** cho hình dạng "chốt nhìn THIẾU một phần của đường". Đặc tả gộp P2c thêm
**3** lượt liên tiếp cùng hình dạng (máy/share ngoài luật thành phần, ổ mạng mang mã ổ cục bộ, gốc kho rỗng; `subst` và miền định danh SMB;
lại miền định danh và dò `.git` nuốt lỗi) — chạm ngưỡng ba lần, nên chủ kho chọn D: bỏ đích qua mạng, cả lớp lỗi định danh chết theo kiến trúc.
C1 đáp lớp TÊN bằng danh sách cho phép trên mã phân loại, mỗi nhánh một đột biến; lớp alias cục bộ (`subst`, 8.3) dựa vào `realpath` và được đo
bắt buộc (D8, D11). Mức đặc tả của C1: 0 lượt riêng lúc soạn (lượt review tiếp nối số của đặc tả gộp: lượt 4 trở đi).

## 8. `chua_do_duoc`

- Mọi hành vi native (§4c): `GetDriveTypeW` và `realpath` cho ổ `subst`/`net use`; dạng `os.getcwd()`; `lstat` gốc ổ; tên 8.3.
- Junction (chưa chặn tới khi R land, §2).
- Nguyên mẫu chỉ phủ M1/M2 (tiền tố thử `ly_do:` thay cụm công khai); đột biến 29–32, 39, 42, 43 là lập luận.
- `_trong_kho_git` (P2a/packet 1) vẫn nuốt mọi `OSError` khi dò `.git` trên nhánh POSIX và ở W1–W3/W6; C1 chỉ đóng khe ấy cho W4/W5 trên
  nt (M3 bước dò ba trạng thái). Khe POSIX là nợ kế thừa, ngoài write set hành vi của C1 — báo điều phối để mở việc riêng.
- TOCTOU (§2).
- Kích thước (ước lượng tĩnh, chưa đo; mốc P2a: 11 ca/46 lượt/37 đột biến ⇒ fragment +389, `tl_gws.py` +48):
  `tl_gws.py`: M1 22–28, M2 12–15, `_loai_o_nt` 5–7, M3 kèm chuỗi thật `strict` và dò `.git` ba trạng thái 18–23 ⇒ **57–73**; fragment: khung + tự kiểm + đếm `chỉ_nt` 110–125, rig W4/W5 nt + bộ
  đếm + dựng symlink + probe 62–77, N1 45 lượt + N2 18 lượt dạng dữ liệu 59–71, N3 12 lượt 36–45, `_DB` 44 mục 47–54 ⇒ **314–372**;
  bundled 1 ⇒ **372–446**, giữa ~409; biên trên còn 4 dòng dưới 450 — SÁT TRẦN: vượt khi thi công ⇒ dừng theo §6 (E2), không cắt ca.

## 9. Lịch sử và quyết định

- Đặc tả gộp `GWS-CRED-DICH-NGOAI-KHO-C-r1.md` (bản 1–4) qua 3 lượt review Codex (`rv/luot1–3.verdict.txt`); các finding thuộc phần đường
  (luật thành phần, Unicode biên, thứ tự kiểm, `q11` mặc định, loại ổ, `subst`, D-rig, T3, numstat, neo `tu_kiem_neo_lap`) đã vào bản này.
- Chủ kho 2026-11-19 ~10:50Z: Q2 = D, Q1 tách C1 → R, Q4–Q7 mặc định, Q9 tự chạy shell admin, Q8 xin riêng từng `packet_id`.
- So với phần C1 của đặc tả gộp: UNC thành mã `unc` duy nhất (bỏ luật máy/share, `IPC$`, tham số `unc`); `mang` bị từ chối vĩnh viễn; thêm
  lượt `W5.unc`, `W5.sl_to_tien` và đột biến 32 (chọn gốc) vào C1 vì symlink đã bị luật (b) chặn, không cần R.

## 10. Nhật ký revision

- 2026-11-19T10:49Z (phiên con của điều phối #1206): tách từ đặc tả gộp bản 4 theo quyết định chủ kho; đo lại base `96b6a33` (blob
  `tl_gws.py` không đổi); nguyên mẫu C1 28/28. Bản lượt 4 (tiếp số lượt của đặc tả gộp).
- 2026-11-19T11:01Z (sau review lượt 4 trên `51a7a4fb…`: request_changes, 6 P2, 1 P3): thứ tự luật thành phần (`p43`, `p44`, đột biến
  33–34), NBSP/DEL được nhận (`p45`, 35), loại ổ 0/1/6 (`q15`–`q17`, 36–38), lỗi `GetDriveTypeW` qua W4/W5 (`W5/W4.loai_o_loi`, 39); bỏ lời
  khai "đỏ dưới 30" cho các lượt tích hợp; D8 tên ngắn thực tế + KHÔNG ĐO ĐƯỢC rõ; D10 trích dẫn PowerShell, kiểm tên share trống, đi qua
  `_gws_auth_load`; D11 `realpath` của cha `dest` và đối chứng tuple; D12 = tái sinh manifest + mọi gate lane LAND trên hai nền; numstat so
  exact OID; giờ đo cụ thể. Nguyên mẫu r2 34/34. Bản lượt 5.
- 2026-11-19T11:06Z (sau review lượt 5 trên `36905860…`: request_changes, 6 P2, 2 P3): đột biến 40 (thứ tự namespace trước luật thành
  phần; cặp 3/40 có chủ ý), `q18` + 41 (cắt `repr` 200), 42 (lỗi chọn đích ở W4); D8 không còn đường xanh khi 8.3 bật mà thiếu tên ngắn
  (dự phòng `fsutil file setshortname` ADMIN, rồi VM, rồi chặn); D10 ghi cwd trong tiến trình và đếm lời gọi `_loai_o_nt`; D12 tên trường
  `expected_file_count`/`checked_file_count`; cột đo 15/18/25/26; giờ UTC. Nguyên mẫu r3 36/36. Bản lượt 6.
- 2026-11-19T11:15Z (sau review lượt 6 trên `a4d929df…`: request_changes, 1 P1, 2 P2, 1 P3; 8/8 finding lượt 5 đóng hoặc đóng một
  phần): M3 dò `.git` ba trạng thái riêng cho nhánh nt (lỗi quyền ⇒ `ghi lỗi`), lượt `W5.git_loi`, đột biến 43; D8 luôn đọc `dir /x`, chỉ bỏ
  qua khi chính sách tắt VÀ không có alias; `tu_kiem_doi_kieu` cụ thể; sửa lời khai nguyên mẫu và ô đo dòng 9. Bản lượt 7.
- 2026-11-19T11:17Z (sau review lượt 7 trên `83dd4ceb…`: request_changes, 3 P2, 1 P3; 4/4 finding lượt 6 đóng hoặc một phần): chuỗi thật
  dùng `realpath(strict=True)` của tổ tiên tồn tại gần nhất (lỗi phân giải ⇒ `ghi lỗi`), lượt `W5.realpath_loi`, đột biến 44;
  `tu_kiem_doi_kieu` dùng lớp giả mang đủ tuple; D8/D11 chạy thêm qua `_gws_auth_load`; §0.4 đếm neo lại có UTC. Bản lượt 8 (lượt cuối trong
  ngân sách dừng của C1).
