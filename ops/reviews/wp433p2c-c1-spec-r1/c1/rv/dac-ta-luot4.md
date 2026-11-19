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
| `base` | `96b6a33d770f7539a3eacbebdc215f87ded4ea7f` (origin/master, đo 2026-11-19T10:4xZ); blob `scripts/tl_gws.py` `9ec027c2808868a05b67adc3d93ea68a574d6ec0`, 2649 dòng — BẰNG blob tại `417b593` và `11bd033`. Lease ghi base thật; phiên thi hành đo lại §0 trước khi sửa. |

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

### 0.3 Nguyên mẫu M1/M2 (KHÔNG phải mã thi công; `c1/nguyen-mau/nguyen_mau_c1.py`, `do_dot_bien_c1.py`)

Đo 2026-11-19T10:49:32Z trên 3.11, 3.12, 3.13, cùng đầu ra (`nm-out-3.1x.txt`): đúng mã/gốc/thành phần của 42 lượt N1 và đúng kết quả
14 lượt N2 (lý do ở nguyên mẫu là `repr(x)`, chưa có tiền tố cụm). Bộ chạy đột biến kiểm neo khớp đúng 1 lần, so lượt đầu đổi màu với lượt
đích khai, trả rc ≠ 0 khi lệch: **28/28 khớp, rc 0** cả ba bản (`dot-bien-3.1x.txt`). Bộ chạy so DÒNG đầu ra, chưa đo `TinHieuChotCa`,
nhãn hay hợp đồng cụm — các thứ ấy chỉ có trên mã thi công. Đó là các dòng §4b cột "đo".

### 0.4 Ràng buộc kề bên

- **Neo của fragment P2a** (`wp433_gws_cred_dich_ngoai_kho.py`, blob `2783e20c…`, 37 mục `_DB`) và **fragment packet 1**
  (`wp433_nlm_gws_dich_ngoai_kho.py`, 30 mục `_DB`): đo trên base (review lượt 2/3 của đặc tả gộp) — mọi neo `_DB` đúng 1 lần; neo `_TU_KIEM`
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
| M3 | Nhánh `os.name != "posix"` của `_dich_cred_gws` thành `return _dich_cred_gws_nt(cfgdir_tho)`. `_dich_cred_gws_nt(cfgdir_tho)` (KHÔNG tạo/ghi gì): `os.getcwd()` MỘT lần; M2 — lý do ⇒ `(None, lý_do)`; `dest = gốc + "\\".join((*tp, "credentials.json"))`; trả `(dest, _kiem_dich_ghi(dest, gốc, (*tp, "credentials.json")))` — luật (a) kho trên `abspath`/`realpath`, luật (b) liên kết ở MỌI tiền tố từ gốc ổ. `dest` là đường DUY NHẤT được kiểm, ghi và (W5) trả về. W4, W5 không đổi. Văn bản mới không chứa lại neo §0.4. | `scripts/tl_gws.py` |
| M4 | Hợp đồng lỗi: GIỮ sáu cụm của P2a, không thêm cụm. Từ chối của M1/M2 ⇒ `đường không hợp lệ`; kho ⇒ `nằm trong kho git`; liên kết ⇒ `là liên kết tượng trưng`; `OSError` (kể cả từ `GetDriveTypeW` lười hay `lstat`) ⇒ `ghi lỗi: <_safe_exc(e)>`. W4 một dòng `[bootstrap] ✗ <cụm>: .+`, rc 1, `degraded`; W5 `(False, "<cụm>: …")`; `cmd_gws_auth_load` một dòng, rc 2 — như P2a M3. Mọi từ chối xảy ra TRƯỚC writer: không tệp mới, không tệp tạm. | `scripts/tl_gws.py` |
| M5 | Fragment `scripts/test_fragments/wp433_gws_cred_win_duong.py`, `TEST_ID = "wp433_gws_cred_win_duong"`: khuôn fragment P2a, tự chứa, nạp `tl_gws` vào bộ nhớ, đột biến trên bản sao, neo khớp đúng 1 lần, phân hạng `TinHieuChotCa(AssertionError)` theo (loại tín hiệu, ca, lượt, nhãn), sổ `_LUOT_DU_KIEN` và `_DU_KIEN` viết riêng, trạng thái lượt `đạt`·`đỏ`·`bỏ_qua`·`chỉ_nt`, mọi đầu ra ra STDERR, khôi phục trong `finally`. Ca `nt` thay `_loai_o_nt` trên module ĐÃ NẠP; M2/M3 tra tên ấy LÚC GỌI. | fragment |
| M6 | Tái sinh `scripts/tl_test_fragments_bundled.py` bằng `generate_bundled_module_bytes(scripts/test_fragments)`; không sửa tay. | bundled |

## 4. `nghiem_thu`

Ký hiệu như P2a §4 (K = kho git tạm, T = thư mục tạm ngoài kho, gốc rig = `realpath(mkdtemp())`). Nền `mọi` hoặc `nt`; ca `nt` trên
nền khác: mọi lượt `chỉ_nt`. Mỗi lượt thu đủ hậu điều rồi so nhãn theo thứ tự ghi; nhãn đỏ đầu tiên là tín hiệu; ca dừng ở lượt đỏ đầu.
"W5 đúng" = `(False, s)`, `s` `fullmatch` `<cụm>: .+`, một dòng. "Lý do M2 đúng(x)" = BẰNG nguyên văn `"đường không hợp lệ: " + repr(x)[:200]`.

| # | ca (nền) | lượt và tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|---|
| N1 | `phan_loai_nt` (mọi), gọi thẳng `_phan_loai_duong_nt` | 42 lượt, mỗi lượt nhãn [`ma`] rồi (loại nhận) [`goc_tp`]. Nhận: `p01` `C:\x`⇒`o_tuyet_doi`,`C:\`,(`x`); `p02` `C:/x`, `p03` `c:\x` ⇒ như `p01`; `p04` `C:\a/b\c`⇒(`a`,`b`,`c`); `p05` `fake`⇒`tuong_doi`,`None`,(`fake`); `p06` `C:\x\.\y\\`⇒(`x`,`y`); `p07` `D:\Quốc hội\tra-luat`⇒`D:\`,(`Quốc hội`,`tra-luat`); `p08` `C:\ a`⇒(` a`,). Từ chối (mã): `p09` `a\x00b` `nul`; `p10` `   ` `trang`; `p11` `\\?\C:\x`, `p12` `//?/C:/x`, `p13` `\\?\UNC\s\sh` `thiet_bi_win32`; `p14` `\\.\pipe\x`, `p15` `//./C:/x` `thiet_bi_dos`; `p16` `\??\C:\x` `nt_doi_tuong`; `p17` `C:` `o_tran`; `p18` `D:fake` `o_tuong_doi`; `p19` `\fake`, `p20` `/fake` `goc_o`; `p21` `\\server\share\x`, `p22` `//server/share/x`, `p23` `/\server\share\x`, `p24` `\\server`, `p25` `\\\server\share`, `p26` `\\server\\share` `unc`; `p27` `1:\x` `o_khac`; `p28` `C:\a\..\b`, `p29` `a/../b`, `p30` `..` `hai_cham`; `p31` `C:\x:ads`, `p32` `C:\a\|b`, `p33` `C:\a` + `\ud800` + `b`, `p34` `C:\a` + `\x01` + `b` `ky_tu_cam`; `p35` `C:\a.\b`, `p36` `C:\a ` `cuoi_cham_cach`; `p37` `C:\CON`, `p38` `C:\nul.txt`, `p39` `C:\com1\x`, `p40` `C:\NUL .txt`, `p41` `C:\CONIN$`, `p42` `C:\COM0` `ten_thiet_bi`. Base: hàm chưa có ⇒ lượt đầu đỏ (`ngoai_le_la`). | §4b dòng 1–22 (đo trên nguyên mẫu §0.3). |
| N2 | `chuan_nt` (mọi), gọi thẳng `_duong_dich_chuan_nt` với `loai_o` giả (trả 3 trừ khi ghi khác) | `q01` (`fake`, `C:\cwd`) ⇒ [`ket_qua`] (`C:\`, (`cwd`,`fake`)); `q02` (`a\b`, `c:/cwd`) ⇒ (`C:\`, (`cwd`,`a`,`b`)); `q03` (`fake`, `\\s\sh\d`) ⇒ [`ly_do`] đúng(`\\s\sh\d`); `q04` (`fake`, `D:rel`) ⇒ [`ly_do`] đúng(`D:rel`); `q05` (`fake`, `\\?\C:\cwd`) ⇒ [`ly_do`] đúng(cwd); `q06` (`C:\`) ⇒ [`goc_rong`] đúng(`C:\`); `q07` (`x\n\..`) ⇒ [`mot_dong`] đúng(p), không `\n`; `q08` (`x`, `C:\`) ⇒ [`ket_qua`] (`C:\`, (`x`,)); `q09` (`.`, `C:\cwd`) ⇒ (`C:\`, (`cwd`,)); `q10` (`.`, `C:\`) ⇒ [`goc_rong`] đúng(`C:\`); `q11` (`Z:\x`, `loai_o` ⇒ 4) ⇒ [`ly_do`] đúng(p); `q12` (`E:\x`, ⇒ 5) ⇒ [`ly_do`]; `q13` (`F:\x`, ⇒ 2) ⇒ [`ket_qua`] (`F:\`, (`x`,)); `q14` (`fake`, `Z:\cwd`, ⇒ 4) ⇒ [`ly_do`] đúng(cwd). | §4b dòng 23–29. |
| N3 | `tich_hop_nt` (nt) — W4 fixture gws chuẩn của P2a, W5 với `_public_curl_bytes` giả; bộ đếm lời gọi writer và `os.lstat` | `W5.trong_kho` `cfgdir = <K>\gwscfg` ⇒ [`ly_do`] W5 đúng `nằm trong kho git`, sạch(K); `W4.trong_kho` cùng `cfgdir` ⇒ [`w4`] rc 1, đúng một dòng `[bootstrap] ✗ nằm trong kho git: …`; `W5.tuong_doi` cwd `<T>`, `cfgdir = cfg` ⇒ [`ket_qua`] `(True, d)`, `d` = dạng M2 của `<T>\cfg\credentials.json`, tệp đúng byte; `W5.o_thuong` `cfgdir` = `<T>\o` viết ổ thường, gạch `/` ⇒ [`ket_qua`] `d` ổ hoa, chỉ `\`; `W5.o_tuong_doi` `<ổ của T>:cfg` ⇒ [`ly_do`] `đường không hợp lệ`; `W5.hai_cham` `<T>\x\..\cfg` ⇒ [`ly_do`] `đường không hợp lệ`; `W5.unc` `\\wp433-khong-ton-tai.invalid\s\x` ⇒ [`ly_do`] `đường không hợp lệ`, 0 lời gọi `lstat`/writer (không chạm mạng); `W5.sl_to_tien` `<T>\sl\a` (`sl` symlink thư mục → `<T>\that`) ⇒ [`lien_ket`] chi tiết `repr(<T>\sl)`, `that` không tệp mới. Mọi lượt từ chối: writer 0 lần, không `.auth.json.*`. Danh sách cho phép `bỏ_qua`: ĐÚNG lượt `W5.sl_to_tien`, chỉ khi `os.symlink` trên CHÍNH thư mục fixture ném `OSError` có `winerror == 1314`; lỗi khác ⇒ `đỏ` với `probe symlink: <repr(lớp, errno, winerror)>`. | §4b dòng 30–32. |
| N4 | tự kiểm | (a) `_DU_KIEN` == tập ID `_DB` (đếm cả số lần); mỗi mục giết đúng (loại tín hiệu, ca, lượt, nhãn). (b) `_LUOT_DU_KIEN` viết riêng; tập và số lần (ca, lượt) đã ghi trạng thái BẰNG sổ: 3 ca / 42 + 14 + 8 = **64** lượt. (c) MỘT dòng tổng kết ra STDERR dạng P2a (`CA`, `LUOT`, `DOT BIEN`, `HONG`, `TU_KIEM`, cột `chỉ_nt` thay `chỉ_posix`); `run` True chỉ khi: `b == c`, `y == z`, `f == g`, `i == 0`, `a == b + w`, `x == y + u + t`, `e == f + h + v`, `x == 64`, `e == len(_DU_KIEN)`, `h == u` và `h ≤ 1` (chỉ đột biến 32 theo lượt duy nhất được phép bỏ qua), mọi tự kiểm đúng hạng; trên nền khác nt: `t = 8`, `v = 3`, `u = h = 0`; trên nt: `t == v == 0`. (d) Tự kiểm phân hạng: `tu_kiem_doi_kieu` (`except` đổi kiểu ⇒ `TIN_DUNG_GIA`, `__context__` là `AttributeError`), `tu_kiem_chu_thich` (⇒ `SONG_SOT`), `tu_kiem_sai_luot` (CHÍNH đột biến 3, chỉ khai lượt `p12` ⇒ `TIN_DUNG_GIA`). (e) stdout của `run` rỗng. | Trên bản sao fragment: thêm ID vào `_DU_KIEN` ⇒ (a) False; lặp một lượt ⇒ (b) False; gỡ một lượt ⇒ (b) False; ép `bỏ_qua` lượt ngoài danh sách cho phép ⇒ False; ép `bỏ_qua` symlink khi probe thành công ⇒ False; cố định `os.name == "nt"` cho bộ phân loại bỏ qua, probe ném `PermissionError` `winerror == 5` ⇒ lượt `đỏ`, False; bộ phân hạng bỏ so lượt ⇒ `tu_kiem_sai_luot` ra `GIET` ⇒ False; in tổng kết ra stdout ⇒ (e) đỏ. |
| N5 | gate | Exact head: `--selftest` N/N hai số bằng nhau, N = N_base + 1, DELTA 0 ca đỏ mới (base/head dựng trong CÙNG một lệnh); `test-fragments-check --json` ⇒ `ok: true`; `bundle_fragment_check.py --json` ⇒ `ok: true`, `failed: []`; với MỌI neo trong `_DB` và `_TU_KIEM` của fragment P2a và fragment packet 1: số lần khớp trên candidate BẰNG trên base (`_DB` = 1; `tu_kiem_neo_lap` = 2), đếm bằng nạp hai fragment rồi đọc bảng; hai fragment ấy `run` True trên Linux; `python3 ops/cloud_agent_creds_test.py` `TONG: DAT`, từng ca bằng base; lane worker `release-manifest` tạm + `release-verify --strict` ⇒ `ok: true`, `expected_file_count == checked_file_count`; `ruff check --select F` delta 0 trên `tl_gws.py`, 0 trên fragment và bundled; `git diff --check` rc 0; `doctrine-scan`, `adr-song` rc 0; numstat dưới `set -o pipefail`: đúng 3 dòng, mỗi dòng `^[0-9]+\t[0-9]+\t<đường>$`, tập đường == §1, tổng cột thêm ≤ 450. Gate T3 theo protocol §10.1: full selftest + release gates trên CẢ Windows (D12) và Linux cho cùng frozen integration SHA; D5 không thay T3; T4 chỉ tái dùng T3 khi exact identity khớp. | Neo: chèn thêm một bản của một neo `_DB` (mỗi fragment một lần) ⇒ đỏ; xoá một bản neo `tu_kiem_neo_lap` ⇒ 1 ≠ 2 ⇒ đỏ. Selftest/bundled/manifest: như P2a N10–N11. Numstat dựng tay: tổng 451 ⇒ đỏ; đường ngoài §1 ⇒ đỏ; thiếu một đường ⇒ đỏ; cột `-` ⇒ đỏ; base sai ⇒ rc 128. `cloud_agent_creds_test`, `doctrine-scan`, `adr-song`, `ruff`: gate kế thừa, phép đỏ thuộc suite của chúng; packet không thêm. |
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
| 9 | `db_nt_o_tuong_doi` (bỏ kiểm phân cách sau ổ) | · `p18` | `ma` | H | mọi | `p18`,`q04` |
| 10 | `db_nt_o_chi_hoa` (`[A-Z]:`) | · `p03` | `ma` | H | mọi | `p03`,`q02` |
| 11 | `db_nt_khong_hoa_o` (bỏ `.upper()`) | · `p03` | `goc_tp` | H | mọi | `p03`,`q02` |
| 12 | `db_nt_goc_o_tuyet_doi` (bỏ `goc_o`) | · `p19` | `ma` | H | mọi | `p19`,`p20` |
| 13 | `db_nt_chi_gach_nguoc` (tách chỉ theo `\`) | · `p02` | `goc_tp` | H | mọi | `p02`,`p04`,`p29`,`q02` |
| 14 | `db_nt_bo_hai_cham` | · `p28` | `ma` | H | mọi | `p28`–`p30` |
| 15 | `db_nt_bo_ky_tu_cam` (bỏ dòng lớp ký tự cấm) | · `p31` | `ma` | H | mọi | `p31`,`p32`,`p34` |
| 16 | `db_nt_bo_surrogate` | · `p33` | `ma` | H | mọi | `p33` |
| 17 | `db_nt_bo_dieu_khien` (bỏ `\x01-\x1f` khỏi lớp) | · `p34` | `ma` | H | mọi | `p34` |
| 18 | `db_nt_bo_cuoi_cham` | · `p35` | `ma` | H | mọi | `p35`,`p36` |
| 19 | `db_nt_bo_ten_tb` | · `p37` | `ma` | H | mọi | `p37`–`p42` |
| 20 | `db_nt_ten_tb_khong_cach` (bỏ ` *` trong regex) | · `p40` | `ma` | H | mọi | `p40` |
| 21 | `db_nt_bo_conin` (bỏ `CONIN$`/`CONOUT$`) | · `p41` | `ma` | H | mọi | `p41` |
| 22 | `db_nt_o_khac_nhan` (`d` khác ⇒ nhận như ổ) | · `p27` | `ma` | H | mọi | `p27` |
| 23 | `db_nt_cwd_khong_kiem` (cwd sai loại ⇒ ghép chuỗi `ntpath.join(cwd, p)` rồi chuẩn hoá lại) | `chuan_nt` · `q03` | `ly_do` | H | mọi | `q03`–`q05` (lý do nêu đường ghép ≠ cwd) |
| 24 | `db_nt_goc_rong` (bỏ chốt không còn thành phần) | · `q06` | `goc_rong` | H | mọi | `q06`,`q10` |
| 25 | `db_nt_bo_loai_o` (bỏ chốt loại ổ) | · `q11` | `ly_do` | H | mọi | `q11`,`q12`,`q14` |
| 26 | `db_nt_loai_o_moi_loai` (chỉ từ chối loại 4) | · `q12` | `ly_do` | H | mọi | `q12` |
| 27 | `db_nt_bo_removable` (chỉ loại 3 là cục bộ) | · `q13` | `ket_qua` | H | mọi | `q13` |
| 28 | `db_nt_loai_o_chi_tuyet_doi` (chỉ kiểm loại ổ khi `p` tuyệt đối) | · `q14` | `ly_do` | H | mọi | `q14` |
| 29 | `db_nt_khong_repr` (lý do nội suy `x` thô) | · `q07` | `mot_dong` | H | mọi | lập luận |
| 30 | `db_nt_bo_chot` (nhánh nt về base) | `tich_hop_nt` · `W5.trong_kho` | `ly_do` | H | nt | lập luận (§0.1: base ghi vào kho) |
| 31 | `db_nt_ghi_duong_tho` (`dest` trả về = `ntpath.join(cfgdir_tho, "credentials.json")`, vẫn kiểm đường chuẩn) | · `W5.tuong_doi` | `ket_qua` | H | nt | lập luận |
| 32 | `db_nt_goc_cfg` (`_kiem_dich_ghi(dest, <cfgdir chuẩn>, ("credentials.json",))`, bỏ tổ tiên) | · `W5.sl_to_tien` | `lien_ket` | H | nt | lập luận (như P2a 33) |

Tổng: **32** đột biến (`mọi` 29, `nt` 3), E: 0. Cặp chung (ca, lượt) có chủ ý: 10/11 (`p03`, khác nhãn `ma`/`goc_tp`); 25/26/28 khác lượt
nhờ `q11`/`q12`/`q14`. `W5.o_thuong`, `W5.o_tuong_doi`, `W5.hai_cham`, `W5.unc`, `W4.trong_kho`: không có đột biến đích riêng — đỏ dưới 30
(lập luận); chúng là phép đo tích hợp của M1/M2 trên Windows thật, có răng từ N1/N2.

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
| D8 | có nếu 8.3 bật | không | `fsutil 8dot3name query <ổ T>:`; `dir /x` lấy tên 8.3 của K; `_dich_cred_gws(<tên ngắn K>\gws)` | `nằm trong kho git`, writer 0 | 8.3 tắt ⇒ KHÔNG ĐO ĐƯỢC, không chặn |
| D9 | có | không | Tên Unicode THÔNG THƯỜNG: `_dich_cred_gws` rồi writer với `cfgdir` = `<T>\Quốc hội\gws` và `<K>\Quốc hội\gws` | T: ghi được, tệp đúng; K: `nằm trong kho git`, writer 0 | không có |
| D10 | có | **có** (chỉ tạo/xoá share) | Shell THƯỜNG: `whoami` ⇒ `<P>`. **[ADMIN]** PowerShell nguyên văn: `net share wp433c1=<đường T> /grant:"<P>",FULL`. Shell THƯỜNG (KHÔNG phải admin — ổ ánh xạ của phiên admin không thấy được ở phiên thường): `net use <Z>: \\localhost\wp433c1`; kiểm `os.path.isdir("<Z>:\\")` đúng và `GetDriveTypeW("<Z>:\\") == 4` (đối chứng dương: ổ mạng hoạt động); rồi `_dich_cred_gws` với `\\localhost\wp433c1\x`, `<Z>:\x`, và (cwd = `<Z>:\`) `x` | cả ba `đường không hợp lệ`; 0 lời gọi `lstat` trên đường đích, writer 0. Dọn: shell thường `net use <Z>: /delete`; **[ADMIN]** `net share wp433c1 /delete` | thiếu admin ⇒ KHÔNG ĐO ĐƯỢC ⇒ không land |
| D11 | có | không | `subst <S>: <K>\sub` (rig tạo và kiểm `<K>\sub` trước) và `subst <S2>: <T>`; `_dich_cred_gws` với `<S>:\gws` khi `<K>\sub\gws` (a) đã có, (b) chưa có; và `<S2>:\gws`; ghi `GetDriveTypeW`, `os.path.realpath` | `<S>`: (a), (b) `nằm trong kho git`, writer 0; `<S2>`: `None`. `<S>` không bị chặn ⇒ DỪNG, revision (phương án: nhận diện `subst` bằng `QueryDosDeviceW`). Dọn `subst <S>: /d`, `subst <S2>: /d`, ghi rc từng lệnh | không có |
| D12 | có (T3) | không | Trên frozen integration SHA: `python scripts/tl.py --selftest` (N/N hai số bằng nhau) và `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` trên Windows; cùng hai lệnh trên Linux (CI) | cả hai nền xanh, cùng SHA | thiếu Windows ⇒ T3 chưa đạt ⇒ không land |

## 5. `pham_vi_e`

Không chạm E4, E5: chỉ sửa mã đường ghi; ca fragment dùng giá trị giả, HOME/cfgdir tạm, đồ giả thay tải Drive; không LIVE, không đẩy
Package. D10 tạo/xoá một share TẠM trỏ vào thư mục tạm bằng shell admin của chủ kho; D10/D11 tạo/xoá ổ ánh xạ và `subst` TẠM — thao tác cục
bộ, không chạm dữ liệu kho hay credential thật.

## 6. `luat_dung`

- Trần lời gọi Codex theo dòng khai `ADR-0055`; chạm trần ⇒ Review Rescue Checkpoint; xin tăng mang **E2**.
- Trần kích thước theo dòng khai `ADR-0053` (≤ 6 tệp, ≤ 450 dòng thêm), đo bằng numstat thật (N5) TRƯỚC khi công bố; vượt ⇒ DỪNG, không
  push, không cắt ca; nâng trần là quyết định của chủ kho — **E2**.
- Trước khi đóng băng và trước mỗi bước công bố: chạy lại ba phép đo mục *Hiệu lực* của `ADR-0053` và `ADR-0055` trên ref mới của nhánh
  mặc định cho hai OID ở dòng khai; một phép sai ⇒ dòng khai không hợp lệ ⇒ dừng, revision.
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
- Nguyên mẫu chỉ phủ M1/M2 (không có cụm lý do, `repr` cắt 200); đột biến 29–32 là lập luận.
- TOCTOU (§2).
- Kích thước (ước lượng tĩnh, chưa đo; mốc P2a: 11 ca/46 lượt/37 đột biến ⇒ fragment +389, `tl_gws.py` +48):
  `tl_gws.py`: M1 22–28, M2 12–15, `_loai_o_nt` 5–7, M3 6–8 ⇒ **45–58**; fragment: khung + tự kiểm + đếm `chỉ_nt` 110–125, rig W4/W5 nt + bộ
  đếm + dựng symlink + probe 62–77, N1 42 lượt + N2 14 lượt dạng dữ liệu 54–66, N3 8 lượt 24–32, `_DB` 32 mục 35–40 ⇒ **285–340**;
  bundled 1 ⇒ **331–399**, giữa ~365; biên trên còn 51 dòng dưới 450.

## 9. Lịch sử và quyết định

- Đặc tả gộp `GWS-CRED-DICH-NGOAI-KHO-C-r1.md` (bản 1–4) qua 3 lượt review Codex (`rv/luot1–3.verdict.txt`); các finding thuộc phần đường
  (luật thành phần, Unicode biên, thứ tự kiểm, `q11` mặc định, loại ổ, `subst`, D-rig, T3, numstat, neo `tu_kiem_neo_lap`) đã vào bản này.
- Chủ kho 2026-11-19 ~10:50Z: Q2 = D, Q1 tách C1 → R, Q4–Q7 mặc định, Q9 tự chạy shell admin, Q8 xin riêng từng `packet_id`.
- So với phần C1 của đặc tả gộp: UNC thành mã `unc` duy nhất (bỏ luật máy/share, `IPC$`, tham số `unc`); `mang` bị từ chối vĩnh viễn; thêm
  lượt `W5.unc`, `W5.sl_to_tien` và đột biến 32 (chọn gốc) vào C1 vì symlink đã bị luật (b) chặn, không cần R.

## 10. Nhật ký revision

- 2026-11-19T10:49Z (phiên con của điều phối #1206): tách từ đặc tả gộp bản 4 theo quyết định chủ kho; đo lại base `96b6a33` (blob
  `tl_gws.py` không đổi); nguyên mẫu C1 28/28. Bản lượt 4 (tiếp số lượt của đặc tả gộp).
