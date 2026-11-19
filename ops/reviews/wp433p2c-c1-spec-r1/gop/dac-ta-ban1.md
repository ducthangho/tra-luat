tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# GWS-CRED-DICH-NGOAI-KHO-C r1 — trên Windows, `credentials.json` của gws (W4, W5 trong `tl_gws.py`) chỉ ghi tới đường nằm trong danh sách cho phép, ngoài kho git (UNC đối chiếu bằng định danh tệp), không xuyên liên kết hay reparse point, ghi nguyên tử

- packet_id: GWS-CRED-DICH-NGOAI-KHO-C; revision: 1;

| trường | giá trị |
|---|---|
| `packet_issue` | #433 |
| `nguon_cap_viec` | Issue #433; đặc tả P2a `GWS-CRED-DICH-NGOAI-KHO-A-r1.md` (sha256 `b0065947…`, nhánh `ops/wp433-p2a-spec`, chưa vào master lúc soạn) §2 "Để P2c" mục (1)–(3) và §9 Q1 tầng hai, Q2, Q4. Quyết định chủ kho 2026-11-19 (phiên điều phối #1206) cho P2c: cho phép UNC; UNC nhận diện bằng định danh tệp, không so chuỗi; reparse point (junction, symlink, mount point) thuộc P2c; danh sách cho phép đường Windows chạy mọi nền qua `ntpath`, kèm gạch trộn, hoa/thường ổ, `..` kiểu Windows, mỗi namespace thiết bị một nhãn. |
| `phu_thuoc` | P2a ĐÃ LAND (PR #1415, merge `417b593`, tổ tiên của `11bd033`). P2c thay nhánh `os.name != "posix"` của `_dich_cred_gws` mà P2a để nguyên, gọi lại `_kiem_dich_ghi`, `_ghi_nguyen_tu_0600`, `_trong_kho_git`, `_safe_exc` và hợp đồng lỗi sáu cụm của P2a (M3 P2a). P2b không là tiền đề. |
| `review_class` | `sensitive` (`scripts/tl_gws.py` là đường ghi credential). Đối chiếu `lease_publish check` khi cấp lease. |
| `base` | `11bd0336d00b4a9544e70dcbbe049d372053a3ec` lúc soạn (2026-11-19T10:0xZ); blob `scripts/tl_gws.py` `9ec027c2808868a05b67adc3d93ea68a574d6ec0`, 2649 dòng (= blob tại merge P2a). Lease ghi base thật; phiên thi hành đo lại §0 trước khi sửa. |
| `tach_de_xuat` | Dự báo P2c trọn gói vượt trần 450 (§8). Đặc tả viết sẵn hai phần: mọi mục, ca, đột biến mang thẻ **[C1]** (danh sách cho phép thuần `ntpath`, nối nhánh Windows, vế reparse) hoặc **[C2]** (định danh tệp qua Win32, mở UNC). Chủ kho chọn tách hay nâng trần ở §9 Q1 (**E2**); tách thì C1 land trước, C2 sau, mỗi phần một lease. |

## 0. Hiện trạng (đo trên `11bd033`, Linux, CPython 3.11.18 / 3.12.3 / 3.13.18, `python -I`, không mạng; giờ máy `date -u`)

### 0.1 Nhánh Windows hiện tại

| chỗ | dòng | hành vi |
|---|---|---|
| `_dich_cred_gws` | 1201–1210 | nhánh `if os.name != "posix": return os.path.join(cfgdir_tho, "credentials.json"), None` (1204–1205): KHÔNG chuẩn hoá, KHÔNG chốt kho, KHÔNG chốt liên kết. |
| `_kiem_dich_ghi` | 1173–1187 | luật (b) chỉ `stat.S_ISLNK(os.lstat(tien_to).st_mode)` (1183); docstring tự khai "junction/reparse Windows chưa chặn". Người gọi: W4/W5 (qua `_dich_cred_gws`), W1–W3 (`_dich_jar_nlm` 1233), W6 (1784). |
| W4 | `cmd_bootstrap` 1803–1823 | gọi `_dich_cred_gws(cfgdir)` (1813) rồi `_ghi_nguyen_tu_0600` trong một `try … except OSError`. |
| W5 | `_gws_auth_load` 1961–1968 | như W4 (1963). |
| `_trong_kho_git` | 1119–1139 | đi lên trên `abspath` và `realpath` tìm mục `.git` bằng `lstat`. Không so chuỗi nên hoa/thường, 8.3 không ảnh hưởng; nhưng gốc share UNC là trần: share bắt đầu ở thư mục CON của một kho thì `.git` nằm trên trần ấy, không thấy (finding P1 lượt 1 của P2a). |

### 0.2 Phép đo `ntpath` (2026-11-19T10:04:39Z; tệp `ntpath-3.1x.txt` của lượt soạn)

`splitdrive` cho kết quả GIỐNG NHAU trên 3.11/3.12/3.13 cho 28 đầu vào: `C:\x`→(`C:`,`\x`); `C:`→(`C:`,``); `D:fake`→(`D:`,`fake`);
`\fake`→(``,`\fake`); `\\server\share\x`→(`\\server\share`,`\x`); `\\server`→(`\\server`,``); `\\server\`→(`\\server\`,``);
`\\?\C:\x`→(`\\?\C:`,`\x`); `\\.\pipe\x`→(`\\.\pipe`,`\x`); `\\?\UNC\s\sh`→(`\\?\UNC\s\sh`,``); `//server/share/x`→(`//server/share`,`/x`);
`\\\server\share`→(`\\\server`,`\share`); `\\server\\share`→(`\\server\`,`\share`); `1:\x`→(`1:`,`\x`); `D:\Quốc hội\tra-luat`→(`D:`, phần còn lại).
`isabs` LỆCH theo phiên bản: `\fake`, `/fake` ⇒ True trên 3.11/3.12, False trên 3.13 ⇒ M1 KHÔNG được gọi `isabs`. `splitroot` chỉ có
từ 3.12, kho khai Python ≥ 3.11 (`SKILL.md:161`) ⇒ không dùng. `stat.FILE_ATTRIBUTE_REPARSE_POINT` = 1024 có trên Linux cả ba bản;
`stat.IO_REPARSE_TAG_*` và `ctypes.WinDLL` KHÔNG có trên Linux ⇒ mã C2 nạp Win32 lười, chỉ khi `os.name == "nt"`.

### 0.3 Nguyên mẫu bộ phân loại (lượt soạn, KHÔNG phải mã thi công; `nguyen_mau_c1b.py`, 3.11 và 3.13 cho cùng đầu ra)

Nguyên mẫu (`nguyen_mau_c1_r1.py`, 2026-11-19T10:2xZ) theo đúng thứ tự kiểm của M1 cho ra đúng mã/gốc/thành phần của 37 lượt N1 (thứ tự
bảng N1) và 9 lượt N2 không có tham số `unc` (`q01`–`q09`). 16 đột biến §4b dòng 1–16 chạy trên nguyên mẫu: cả 16 đổi màu, lượt đầu
đổi màu đúng như cột "ca · lượt" §4b (`dich-dot-bien-nguyen-mau-r1.txt`). Tham số `unc` (M2) và mọi thứ ngoài M1/M2 chưa có nguyên mẫu.

### 0.4 Ràng buộc kề bên

- **Neo của fragment P2a** (`scripts/test_fragments/wp433_gws_cred_dich_ngoai_kho.py`, blob `2783e20c…`, 389 dòng, 37 đột biến) phải
  khớp ĐÚNG MỘT lần sau P2c, đặc biệt: `_kiem_dich_ghi(dest, "/", (*chuan[1], "credentials.json"))`, `"\ndef _dich_cred_gws("`,
  `return ly if not tp or ".." in tp else`, `if "\x00" in p or p.strip() == "":`, `ly = f"đường không hợp lệ: {repr(p)[:200]}"`,
  `{repr(kho_dich)[:200]}`, `for i in range(len(thanh_phan) + 1):`, `dest, ly_gws = _dich_cred_gws(cfgdir)`,
  `dest, ly_do = _dich_cred_gws(cfgdir)`, `else (True, dest)`. Fragment packet 1 neo `for i in range(len(thanh_phan) + 1):` và
  `ly_cfg = _kiem_dich_ghi(cfgp, cfgp, ())`. Mã mới KHÔNG được chứa lại nguyên văn các chuỗi ấy; `_duong_dich_chuan` (POSIX) giữ nguyên.
- Fragment P2a trên nt đòi `(w, t, v) == (7, 27, 21)` và chạy 4 ca `mọi` qua `_dich_cred_gws` — sau P2c, các ca ấy đi nhánh nt mới.
  Hồ sơ land P2a ghi "Windows native 0/1 (tuỳ chọn)": fragment P2a và fragment packet 1 CHƯA từng chạy trên Windows thật.
- Backend Win32 có sẵn: `.claude/dev/packet_loop.py:6408–6500` (#1174/#1342: `CreateFileW`, `GetFileInformationByHandle` — bố cục 13
  DWORD, `[7]` serial, `[11:13]` FileIndex — `GetFileInformationByHandleEx`, `FILE_FLAG_OPEN_REPARSE_POINT` `0x00200000`,
  `FILE_FLAG_BACKUP_SEMANTICS` `0x02000000`) và `.claude/dev/launcher.py:4030–4100`. `.claude/` bị loại khỏi gói phát hành nên
  `scripts/tl_gws.py` KHÔNG import được; C2 chép MẪU (argtypes/restype tường minh, `use_last_error=True`, `ctypes.WinError`, đóng
  handle trong `finally`), không chép hàm. Mã #1174 chỉ nhận ổ cố định NTFS; C2 cố ý nhận cả UNC (quyết định chủ kho).
- Bước CI `bundled-fragment check` kiểm bundled committed trên PR; manifest committed chỉ kiểm trên master. Fragment in ra STDERR.
- Không có CI Windows bắt buộc. Đo native Windows: Desktop `DESKTOP-T9R33P2` (Developer Mode bật 19-11 ⇒ tạo symlink không cần admin;
  `core.symlinks=true`); VM `tra-luat-win` dự phòng. Phiên soạn KHÔNG truy cập được máy ấy (§4c, §8).

## 1. `write_set`

Trọn P2c (khi chủ kho chọn KHÔNG tách):

```
scripts/tl_gws.py
scripts/test_fragments/wp433_gws_cred_win_duong.py
scripts/test_fragments/wp433_gws_cred_win_dinh_danh.py
scripts/tl_test_fragments_bundled.py
```

Khi tách: **C1** = `scripts/tl_gws.py`, `scripts/test_fragments/wp433_gws_cred_win_duong.py`, `scripts/tl_test_fragments_bundled.py`;
**C2** = `scripts/tl_gws.py`, `scripts/test_fragments/wp433_gws_cred_win_dinh_danh.py`, `scripts/tl_test_fragments_bundled.py`.
KHÔNG `RELEASE_MANIFEST.json`. `scripts/tl_test_fragments_bundled.py` theo tiền lệ phương án B (chủ kho 18-11-2026; P2a §1): chỉ sinh
bằng `generate_bundled_module_bytes(scripts/test_fragments)`, không sửa tay. **Điều kiện trước khi cấp lease (E2, §9 Q8):** comment của
chủ kho trên Issue #433 cấp ngoại lệ ấy nêu đúng `packet_id` (`GWS-CRED-DICH-NGOAI-KHO-C`, hoặc `-C1`/`-C2` khi tách), đúng một tệp
`scripts/tl_test_fragments_bundled.py` và sha256 đặc tả đã đóng băng; lease trỏ URL comment. Comment `7002145681` (P2a) không phủ.
Phiên land tái sinh `RELEASE_MANIFEST.json` trong commit land.

## 2. `ngoai_pham_vi`

- POSIX: không đổi hành vi nào của nhánh `posix` (P2a). `_duong_dich_chuan` (POSIX) không sửa.
- Phân loại đường cho W1–W3, W6: không (chúng không đọc biến môi trường đường). Riêng vế reparse M4 sửa THÂN `_kiem_dich_ghi` nên áp
  cho MỌI người gọi — đúng như P2a §2 mục (3) đã giao ("M6 cũ … trong `_kiem_dich_ghi` … đi cùng P2c").
- Kho git KHÁC kho tra-luat truy cập qua share hay ổ ánh xạ mà chuỗi `.git` không thấy: KHÔNG bảo vệ (chủ kho Q2 thu hẹp, P2a §9).
- ReFS và định danh 128 bit (`FILE_ID_INFO`): không; C2 dùng FileIndex 64 bit của `GetFileInformationByHandle` (§8).
- Reparse point không phải name-surrogate (placeholder đám mây OneDrive, dedup): M4 từ chối MỌI tag nếu `lstat` báo bit; hành vi
  `os.lstat` của CPython với các tag ấy chưa đo (§8, §9 Q7).
- TOCTOU: như P2a §2 — kiểm theo TÊN rồi ghi theo TÊN; định danh C2 là phép đo tại một thời điểm, không khoá. Thư mục cha hay share ghi
  được bởi principal khác, đổi giữa lúc kiểm và lúc `os.replace`, nằm ngoài bảo đảm; không ca nào đo khe này.
- Không sửa `ops/**`, `.github/**`, `scripts/tl_selftest.py`, fragment P2a, fragment packet 1, `RELEASE_MANIFEST.json`, `changelog.d/*`,
  `VERSION`, `CHANGELOG.md`, `SKILL.md`. Không thêm CI Windows.
- P2b (kiểm dữ liệu W6): packet riêng.

## 3. `muc_tieu`

| # | phần | mục tiêu | tệp |
|---|---|---|---|
| M1 | C1 | Hàm thuần `_phan_loai_duong_nt(p)` dùng `ntpath` import tường minh (không `os.path`, không `isabs`, `splitroot`, `abspath`, `normpath`, `realpath`) trả tuple mà phần tử đầu là MÃ. Kiểm THEO THỨ TỰ, mã đầu tiên khớp thắng: (1) `"\x00" in p` ⇒ `nul`; (2) `p.strip() == ""` ⇒ `trang`; (3) `re.match(r"[\\/]{2}\?[\\/]", p)` ⇒ `thiet_bi_win32`; (4) `re.match(r"[\\/]{2}\.[\\/]", p)` ⇒ `thiet_bi_dos`; (5) `re.match(r"[\\/]\?\?[\\/]", p)` ⇒ `nt_doi_tuong`; (6) `d, r = ntpath.splitdrive(p)`: `d` `fullmatch` `[A-Za-z]:` thì `r == ""` ⇒ `o_tran`, `r[0]` không phải `\`/`/` ⇒ `o_tuong_doi`, còn lại loại `o_tuyet_doi` với gốc `d.upper() + "\\"`; `d` bắt đầu bằng hai phân cách thì `fullmatch(r"[\\/]{2}([^\\/]+)[\\/]([^\\/]+)", d)` ⇒ loại `unc` với gốc `\\<máy>\<share>\` (phân cách chuẩn về `\`, giữ nguyên hoa/thường máy và share), không khớp ⇒ `unc_thieu_share`; `d == ""` thì `p[0]` là phân cách ⇒ `goc_o`, còn lại loại `tuong_doi` (gốc `None`); `d` khác ⇒ `o_khac`; (7) tách `r` theo `\` và `/`, bỏ thành phần rỗng và `.`; còn `..` ⇒ `hai_cham`; (8) từng thành phần: chứa một ký tự trong `<>:"|?*` hay mã `\x01`–`\x1f` ⇒ `ky_tu_cam`; kết thúc bằng `.` hay khoảng trắng ⇒ `cuoi_cham_cach`; `fullmatch` không phân biệt hoa/thường `(CON\|PRN\|AUX\|NUL\|COM[0-9¹²³]\|LPT[0-9¹²³])(\..*)?` ⇒ `ten_thiet_bi`; (9) hết ⇒ `(loại, gốc, thành_phần)`. Ký tự Unicode và khoảng trắng GIỮA tên được nhận (`D:\Quốc hội\tra-luat`). | `scripts/tl_gws.py` |
| M2 | C1 | `_duong_dich_chuan_nt(p, cwd, unc=False)` trả `(gốc, thành_phần)` hoặc lý do MỘT dòng `đường không hợp lệ: <repr(x)[:200]>` (x là `p`, hoặc `cwd` khi lỗi nằm ở `cwd`). Loại `tuong_doi`: phân loại `cwd` bằng M1, `cwd` phải là `o_tuyet_doi` hoặc `unc`, rồi ghép thành phần `cwd + p` (không ghép chuỗi rồi chuẩn hoá). Loại khác `o_tuyet_doi`/`unc` ⇒ từ chối. Không còn thành phần nào (`C:\`, `\\server\share`) ⇒ từ chối (`goc_rong`, như `/` của P2a). `unc` khi `unc=False` ⇒ từ chối (C1 đóng UNC tới khi C2 land, §9 Q5); C2 đổi lời gọi thành `unc=True`. | `scripts/tl_gws.py` |
| M3 | C1 | Nhánh `os.name != "posix"` của `_dich_cred_gws` thành `return _dich_cred_gws_nt(cfgdir_tho)`. `_dich_cred_gws_nt(cfgdir_tho)` (KHÔNG tạo/ghi gì): đọc `os.getcwd()` MỘT lần; M2; `dest = gốc + "\\".join((*tp, "credentials.json"))`; lý do = `_kiem_dich_ghi(dest, gốc, (*tp, "credentials.json"))` (luật (a) kho trên `abspath`/`realpath`, luật (b) liên kết/reparse ở MỌI tiền tố từ gốc ổ/share); [C2] rồi `_kiem_dinh_danh_nt(dest)`. Trả `(dest, lý_do)`; `dest` là đường DUY NHẤT được kiểm, được ghi và (W5) được trả về. W4, W5 không đổi (đã gọi `_dich_cred_gws` trong `try … except OSError`). Văn bản mới không chứa lại neo §0.4. | `scripts/tl_gws.py` |
| M4 | C1 | Thân `_kiem_dich_ghi`: thay ĐÚNG biểu thức nhận diện ở 1183 bằng `st = os.lstat(tien_to)` và điều kiện `stat.S_ISLNK(st.st_mode) or getattr(st, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT`; cụm giữ `là liên kết tượng trưng`; dòng `for i in range(len(thanh_phan) + 1):`, chữ ký, thứ tự luật, bắt `FileNotFoundError`/`NotADirectoryError` giữ nguyên; sửa docstring bỏ câu "junction/reparse Windows chưa chặn". Áp cho W1–W3, W4–W5, W6. | `scripts/tl_gws.py` |
| M5 | C2 | Backend Win32 trong `tl_gws.py`, nạp lười chỉ khi `os.name == "nt"`: `_dinh_danh_nt(duong)` mở bằng `CreateFileW(duong, FILE_READ_ATTRIBUTES 0x80, share 7, None, OPEN_EXISTING 3, 0x02000000 \| 0x00200000, None)`, `GetFileInformationByHandle` ⇒ `(serial, FileIndex64)`; `_duong_theo_dinh_danh_nt(goi_y, chi_so)` mở `goi_y` như trên làm handle gợi ý volume, `OpenFileById` (FILE_ID_DESCRIPTOR kiểu 0, `FileId` = chỉ số) rồi `GetFinalPathNameByHandleW(…, VOLUME_NAME_DOS 0)`, bỏ tiền tố `\\?\` (và `\\?\UNC\` ⇒ `\\`), trả đường; mọi thất bại Win32 ⇒ `ctypes.WinError(ctypes.get_last_error())` (một `OSError`); handle đóng trong `finally`. Gom ba hàm vào namespace `_BE_DD_NT` (`ton_tai` = `os.path.lexists`, `dinh_danh`, `theo_dinh_danh`) — đường thay được cho fragment. | `scripts/tl_gws.py` |
| M6 | C2 | `_kiem_dinh_danh_nt(dest, goc_kho=None, be=None)` (logic thuần trên `ntpath` + `be`, mặc định `_BE_DD_NT` và `_goc_kho_tra_luat()`): `goc_kho` rỗng ⇒ `None` TRƯỚC mọi lời gọi `be`; đi lên từ `ntpath.dirname(dest)` tới tổ tiên GẦN NHẤT mà `be.ton_tai` đúng (gốc ổ/share là trần); `(s, i) = be.dinh_danh(tổ_tiên)`; với MỖI `R` trong `goc_kho`: `(sR, _) = be.dinh_danh(R)`, `sR == s` ⇒ `L = be.theo_dinh_danh(R, i)`; `L is None` ⇒ ném `OSError` (fail-closed, §9 Q4); `_trong_kho_git(L)` khác `None` ⇒ trả `nằm trong kho git: <repr(kho)[:200]>`. Hết ⇒ `None`. `_goc_kho_tra_luat()` = các giá trị khác `None`, không lặp, của `_trong_kho_git(os.path.dirname(os.path.abspath(__file__)))` và `_trong_kho_git(os.getcwd())` (§9 Q3). M2 được gọi với `unc=True`. | `scripts/tl_gws.py` |
| M7 | C1+C2 | Hợp đồng lỗi: GIỮ sáu cụm của P2a, không thêm cụm. Mọi từ chối của M1/M2 ⇒ `đường không hợp lệ`; liên kết/reparse ⇒ `là liên kết tượng trưng`; định danh trùng kho ⇒ `nằm trong kho git`; lỗi Win32 hay `OSError` khác ⇒ `ghi lỗi: <_safe_exc(e)>` (chỉ tên lớp). W4: một dòng `[bootstrap] ✗ <cụm>: .+`, rc 1, `degraded`; W5: `(False, "<cụm>: …")`; `cmd_gws_auth_load` một dòng, rc 2 — như M3 của P2a. | `scripts/tl_gws.py` |
| M8 | C1 / C2 | Fragment C1 `wp433_gws_cred_win_duong.py` (`TEST_ID = "wp433_gws_cred_win_duong"`), fragment C2 `wp433_gws_cred_win_dinh_danh.py` (`TEST_ID = "wp433_gws_cred_win_dinh_danh"`): khuôn fragment P2a, tự chứa (không import fragment khác), nạp `tl_gws` vào bộ nhớ, đột biến trên bản sao, neo khớp đúng 1 lần, phân hạng `TinHieuChotCa(AssertionError)` theo (ca, lượt, nhãn), sổ lượt `_LUOT_DU_KIEN` và `_DU_KIEN` viết riêng, trạng thái lượt `đạt`·`đỏ`·`bỏ_qua`·`chỉ_nt`, mọi đầu ra ra STDERR, khôi phục mọi thứ đã thay trong `finally`. Tái sinh bundled bằng `generate_bundled_module_bytes`. | fragment, bundled |

## 4. `nghiem_thu`

Ký hiệu như P2a §4 (K = kho git tạm, T = thư mục tạm ngoài kho, gốc rig = `realpath(mkdtemp())`). Cột nền: `mọi` hoặc `nt`; ca `nt`
trên nền khác: mọi lượt `chỉ_nt` (không phải `bỏ_qua`). Mỗi lượt thu đủ hậu điều rồi so nhãn theo thứ tự ghi; nhãn đỏ đầu tiên là tín
hiệu. "W5 đúng" = `(False, s)`, `s` `fullmatch` `<cụm>: .+`, một dòng.

| # | phần · ca (nền) | lượt và tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|---|
| N1 | C1 · `phan_loai_nt` (mọi), gọi thẳng `_phan_loai_duong_nt` | 35 lượt `p01`–`p35`, mỗi lượt hai nhãn theo thứ tự [`ma`] mã đúng, rồi (loại nhận) [`goc_tp`] gốc và thành phần đúng. Nhận: p01 `C:\x`⇒`o_tuyet_doi`,`C:\`,(`x`); p02 `C:/x`⇒ như p01; p03 `c:\x`⇒ như p01 (ổ chuẩn hoa); p04 `C:\a/b\c`⇒(`a`,`b`,`c`); p05 `\\server\share\x`⇒`unc`,`\\server\share\`,(`x`); p06 `//server/share/x`⇒ như p05; p07 `/\server\share\x`⇒ như p05; p08 `fake`⇒`tuong_doi`,`None`,(`fake`); p09 `C:\x\.\y\\`⇒(`x`,`y`); p10 `D:\Quốc hội\tra-luat`⇒`o_tuyet_doi`,`D:\`,(`Quốc hội`,`tra-luat`). Từ chối (mã): p11 `a\x00b` `nul`; p12 `   ` `trang`; p13 `\\?\C:\x`, p14 `//?/C:/x`, p15 `\\?\UNC\s\sh` `thiet_bi_win32`; p16 `\\.\pipe\x`, p17 `//./C:/x` `thiet_bi_dos`; p18 `\??\C:\x` `nt_doi_tuong`; p19 `C:` `o_tran`; p20 `D:fake` `o_tuong_doi`; p21 `\fake`, p22 `/fake` `goc_o`; p23 `\\server`, p24 `\\server\`, p25 `\\\server\share`, p26 `\\server\\share` `unc_thieu_share`; p27 `1:\x` `o_khac`; p28 `C:\a\..\b`, p29 `a/../b`, p30 `..` `hai_cham`; p31 `C:\x:ads`, p32 `C:\a\|b` `ky_tu_cam`; p33 `C:\a.\b`, p34 `C:\a ` `cuoi_cham_cach`; p35 `C:\CON`, p36 `C:\nul.txt`, p37 `C:\com1\x` `ten_thiet_bi` (37 lượt). Vế âm base: không có hàm (lượt nào cũng đỏ trên base vì `AttributeError` — xem N7(e)). | Đột biến §4b dòng 1–15; lượt đích đo trên nguyên mẫu (§0.3). |
| N2 | C1 · `chuan_nt` (mọi), gọi thẳng `_duong_dich_chuan_nt` | `q01` (`fake`, `C:\cwd`) ⇒ [`ket_qua`] (`C:\`, (`cwd`,`fake`)); `q02` (`a\b`, `c:/cwd`) ⇒ (`C:\`, (`cwd`,`a`,`b`)); `q03` (`fake`, `\\s\sh\d`, `unc=True`) ⇒ (`\\s\sh\`, (`d`,`fake`)); `q04` (`fake`, `D:rel`) ⇒ [`ly_do`] lý do `fullmatch` `đường không hợp lệ: .+` chứa `repr('D:rel')`; `q05` (`fake`, `\\?\C:\cwd`) ⇒ [`ly_do`] như trên; `q06` (`C:\`) và `q07` (`\\server\share`, `unc=True`) ⇒ [`goc_rong`] lý do; `q08` (`x\n\..`) ⇒ [`mot_dong`] lý do không chứa `\n`; `q09` (`x`, `C:\`) ⇒ [`ket_qua`] (`C:\`, (`x`,)); `q10` (`\\server\share\x`, `unc=False`) ⇒ [`unc_dong`] lý do. (Giá trị mặc định `unc=False` không đổi ở C2; C2 chỉ đổi lời gọi trong `_dich_cred_gws_nt`, nên lượt này còn đúng sau C2.) | 16 `db_nt_goc_rong` ⇒ `q06`. 17 `db_nt_cwd_khong_kiem` (bỏ kiểm loại `cwd`, ghép thẳng) ⇒ `q04`. 18 `db_nt_khong_repr` ⇒ `q08`. 19 `db_nt_unc_mo_som` (mặc định `unc=True`) ⇒ `q10` (chỉ C1). |
| N3 | C1 · `reparse_gia_lap` (mọi) — bọc `os.lstat` trong cửa sổ gọi: với ĐÚNG đường `cfgdir` của lượt (so sau `normcase(normpath)`) trả `SimpleNamespace(st_mode=stat.S_IFDIR \| 0o700, st_file_attributes=<a>)`, đường khác đi hàm thật | `W5.bit` (`a = 1024`) ⇒ [`reparse`] W5 đúng với `là liên kết tượng trưng`, chi tiết `repr(cfgdir)`, không `credentials.json` dưới `cfgdir` thật; `truc_tiep` — gọi thẳng `_kiem_dich_ghi(<T>/x/credentials.json, <T>, ("x", "credentials.json"))` với `a = 1024` cho `<T>/x` ⇒ [`reparse_truc_tiep`] lý do như trên (vế áp cho mọi người gọi); `W5.khong_bit` (`a = 16`, FILE_ATTRIBUTE_DIRECTORY) ⇒ [`khong_bit`] `(True, d)`, tệp đúng byte. Trên POSIX W5 đi nhánh P2a; trên nt đi nhánh M3 — cùng một `_kiem_dich_ghi`. | 20 `db_bo_reparse` ⇒ `W5.bit`. 21 `db_reparse_moi_thu` (mọi thuộc tính khác 0) ⇒ `W5.khong_bit`. |
| N4 | C1 · `tich_hop_nt` (nt) — W4 fixture gws chuẩn của P2a, W5 với `_public_curl_bytes` giả; junction bằng `_winapi.CreateJunction` (thiếu thì `cmd /c mklink /J` ngoài cửa sổ chặn), symlink bằng `os.symlink` | `W5.trong_kho` `cfgdir = <K>\gwscfg` ⇒ [`ly_do`] W5 đúng `nằm trong kho git`, sạch(K); `W4.trong_kho` cùng `cfgdir` ⇒ [`w4`] rc 1, một dòng `[bootstrap] ✗ nằm trong kho git: …`; `W5.jn_to_tien` `<T>\jn\a\b` (`jn` junction → `<T>\that`) ⇒ [`lien_ket`] chi tiết `repr(<T>\jn)`, `<T>\that` không có tệp mới; `W5.jn_cfg` `cfgdir` là junction ⇒ [`lien_ket`]; `W5.sl_dir` `cfgdir` là symlink thư mục ⇒ [`lien_ket`]; `W5.sl_tep` `credentials.json` là symlink tệp tới `<T>\dich.json` (`CU`) ⇒ [`lien_ket`], `dich.json` còn `CU`; `W5.tuong_doi` cwd `<T>`, `cfgdir = cfg` ⇒ [`ket_qua`] `(True, d)`, `d == <T chuẩn>\cfg\credentials.json`, tệp đúng byte; `W5.o_thuong` `cfgdir` = `<T>` viết ổ thường, gạch `/` ⇒ [`ket_qua`] `d` có ổ hoa, chỉ `\`; `W5.o_tuong_doi` `<ổ của T>:cfg` ⇒ [`ly_do`] `đường không hợp lệ`; `W5.hai_cham` `<T>\x\..\cfg` ⇒ [`ly_do`] `đường không hợp lệ` (10 lượt; việc C1 đóng UNC ở lời gọi đo bằng D10, không đặt trong fragment vì C2 mở lại). Danh sách cho phép `bỏ_qua`: ĐÚNG hai lượt `W5.sl_dir`, `W5.sl_tep`, chỉ khi `os.symlink` trên CHÍNH thư mục fixture ném `OSError` có `winerror == 1314` (ERROR_PRIVILEGE_NOT_HELD); lỗi khác ⇒ `đỏ` với chẩn đoán `probe symlink: <repr(lớp, errno, winerror)>`. | 22 `db_nt_bo_chot` (nhánh nt về base: `return os.path.join(cfgdir_tho, "credentials.json"), None`) ⇒ `W5.trong_kho`. 23 `db_nt_goc_cfg` (gọi `_kiem_dich_ghi(dest, <cfgdir chuẩn>, ("credentials.json",))`) ⇒ `W5.jn_to_tien`. 24 `db_bo_reparse_nt` (cùng phép thay với 20, ca này) ⇒ `W5.jn_cfg` (junction không cho `S_ISLNK` — chưa đo, §4c D2). 25 `db_nt_ghi_duong_tho` (`_dich_cred_gws_nt` trả `ntpath.join(cfgdir_tho, "credentials.json")` làm `dest`, vẫn kiểm đường chuẩn) ⇒ `W5.tuong_doi`. `W5.sl_dir`, `W5.sl_tep` đỏ dưới 22 (lập luận, không là lượt đích). |
| N5 | C2 · `dinh_danh_gia_lap` (mọi), gọi thẳng `_kiem_dinh_danh_nt(dest, goc_kho, be)`; `be` giả GIỮ trạng thái: tập đường tồn tại, bảng định danh, bảng `theo_dinh_danh` trỏ tới đường THẬT của rig (K có `.git`, T không), nhật ký lời gọi; `dinh_danh` trên đường không có trong bảng ném `FileNotFoundError("wp433-dd-thieu")` | `trong_kho` (serial trùng, `theo_dinh_danh` ⇒ `<K>/sub`) ⇒ [`ket_qua`] `nằm trong kho git: ` + `repr(K)`; `ngoai_kho` (⇒ `<T>/out`) ⇒ [`ket_qua`] `None`; `khac_vol` (serial khác; bảng vẫn có ánh xạ ⇒ `<K>/sub`) ⇒ [`ket_qua`] `None`, [`khong_goi`] 0 lời gọi `theo_dinh_danh`; `to_tien` (`dest` = `\\s\sh\a\b\credentials.json`, chỉ `\\s\sh\a` tồn tại) ⇒ [`to_tien`] `dinh_danh` gọi trên ĐÚNG `\\s\sh\a`, kết quả đúng; `khong_tim_thay` (`theo_dinh_danh` ⇒ `None`) ⇒ [`nem`] `OSError`; `hai_goc` (`goc_kho` = (`R1` khác serial, `R2` trùng ⇒ `<K>/sub`)) ⇒ [`ket_qua`] lý do kho; `khong_goc` (`goc_kho = ()`) ⇒ [`ket_qua`] `None`, 0 lời gọi `be`. | 26 `db_dd_bo_kiem` (trả `None` ngay đầu) ⇒ `trong_kho`. 27 `db_dd_bo_so_serial` (bỏ điều kiện `sR == s`) ⇒ `khac_vol` `ket_qua`. 28 `db_dd_to_tien_la_cha` (dùng `ntpath.dirname(dest)` không đi lên) ⇒ `to_tien` (E: `FileNotFoundError` chứa `wp433-dd-thieu`). 29 `db_dd_khong_tim_thay_cho_qua` (`None` ⇒ bỏ qua) ⇒ `khong_tim_thay`. 30 `db_dd_mot_goc` (chỉ xét phần tử đầu) ⇒ `hai_goc`. |
| N6 | C2 · `dinh_danh_that` (nt) | `on_dinh` — `_dinh_danh_nt(<T>)` hai lần bằng nhau, `_dinh_danh_nt(<T>\sub)` cùng serial khác chỉ số ⇒ [`on_dinh`]; `theo_id` — `_duong_theo_dinh_danh_nt(<T>, chi_so(<T>\sub))` so `normcase` bằng `realpath(<T>\sub)` ⇒ [`theo_id`]; `noi_day` — W5 với `cfgdir = <T>\cfg` (ngoài kho, lexical qua), `_BE_DD_NT` thay bằng `be` giả ánh xạ định danh của `<T>` sang `<K>\sub`, `goc_kho` thật chứa K qua `_goc_kho_tra_luat` giả ⇒ [`noi_day`] W5 đúng `nằm trong kho git`; `ngoai` — cùng nhưng `be` thật ⇒ [`ngoai`] `(True, d)`, không dương tính giả. | 31 `db_dd_bo_noi_day` (`_dich_cred_gws_nt` bỏ lời gọi `_kiem_dinh_danh_nt`) ⇒ `noi_day`. 32 `db_dd_sai_chi_so` (đọc FileIndex từ `[10:12]` thay `[11:13]`) ⇒ `theo_id`. `on_dinh` đỏ khi backend trả hằng — lập luận. |
| N7 | C1, C2 · tự kiểm của mỗi fragment | (a) `_DU_KIEN` == tập ID `_DB`; mỗi mục giết đúng (ca, lượt, nhãn). (b) `_LUOT_DU_KIEN` riêng khỏi bảng ca: C1 4 ca / 37+10+3+10 = **60** lượt (`phan_loai_nt` 37, `chuan_nt` 10, `reparse_gia_lap` 3, `tich_hop_nt` 10); C2 2 ca / 7+4 = **11** lượt. Fragment C2 không sửa fragment C1 (write set riêng). Tập (ca, lượt) đã ghi trạng thái phải BẰNG sổ; trên POSIX mọi lượt ca `nt` là `chỉ_nt`, `bỏ_qua` chỉ trong danh sách cho phép N4. (c) MỘT dòng tổng kết ra STDERR dạng P2a (`CA`, `LUOT`, `DOT BIEN`, `HONG`, `TU_KIEM`, thêm `chỉ_nt`); `run` True chỉ khi các đẳng thức của P2a N9(c) đổi `chỉ_posix` thành `chỉ_nt`; trên POSIX: C1 `chỉ_nt` = 10 lượt, đột biến `chỉ_nt` = 4 (22–25); C2 = 4 lượt, 2 đột biến (31, 32); trên nt: `chỉ_nt` = 0, `bỏ_qua` ≤ 2. (d) Tự kiểm phân hạng như P2a N9(d): `tu_kiem_doi_kieu` (⇒ `TIN_DUNG_GIA`, `__context__` là `AttributeError`), `tu_kiem_chu_thich` (⇒ `SONG_SOT`), `tu_kiem_sai_luot` (CHÍNH đột biến 1, chỉ khai lượt `p14` thay `p13` ⇒ `TIN_DUNG_GIA`). (e) Base: chạy fragment trên nguồn base ⇒ `run` False (hàm M1/M2/M5/M6 chưa có). (f) stdout của `run` rỗng. | Trên bản sao fragment: thêm ID vào `_DU_KIEN` ⇒ (a) False; gỡ một lượt khỏi bảng ca ⇒ (b) False; ép `bỏ_qua` cho `W5.trong_kho` ⇒ (b) False; ép `bỏ_qua` symlink khi probe thành công ⇒ False; cố định `os.name == "nt"` cho bộ phân loại bỏ qua và cho probe ném `PermissionError` `winerror == 5` ⇒ lượt `đỏ`, False; bộ phân hạng bỏ so lượt ⇒ `tu_kiem_sai_luot` ra `GIET` ⇒ False; in tổng kết ra stdout ⇒ (f) đỏ. |
| N8 | C1, C2 · gate kế thừa | Exact head: `--selftest` N/N hai số bằng nhau, N = N_base + 1 (mỗi phần thêm một fragment), DELTA 0 ca đỏ mới (base và head dựng trong CÙNG một lệnh); `test-fragments-check --json` ⇒ `ok: true`; `bundle_fragment_check.py --json` ⇒ `ok: true`, `failed: []`; fragment P2a và fragment packet 1 vẫn ĐẠT (neo §0.4 khớp đúng 1 lần); `python3 ops/cloud_agent_creds_test.py` `TONG: DAT`, từng ca bằng base; lane worker `release-manifest` tạm + `release-verify --strict` ⇒ `ok: true`, `expected_file_count == checked_file_count`; `ruff check --select F` delta 0 trên `tl_gws.py`, 0 trên fragment và bundled; `git diff --check` rc 0; `doctrine-scan`, `adr-song` rc 0; numstat dưới `set -o pipefail`: đúng số dòng bằng số tệp write set của phần, mỗi dòng `^[0-9]+\t[0-9]+\t<đường>$`, tập đường == §1 của phần, tổng cột thêm ≤ 450. | Như P2a N8, N10–N12: sửa một ký tự neo P2a ⇒ fragment P2a `HONG ≥ 1`; chuyển fragment mới ra khỏi `scripts/test_fragments` trên bản sao ⇒ N = N_base; `run` ⇒ `return False` ⇒ `N−1/N`; không tái sinh bundled ⇒ `TEST_ID_SET_MISMATCH`; sửa byte sau manifest tạm ⇒ `ok: false`; numstat dựng tay tổng 451 ⇒ đỏ, đường ngoài §1 ⇒ đỏ, cột `-` ⇒ đỏ, `<base>` sai ⇒ rc 128. |
| N9 | C1, C2 · đo native (§4c) | Hồ sơ PR ghi lệnh, đầu ra thô và kết luận của từng phép D1–D10 áp cho phần ấy; phép nào không dựng được ghi `KHÔNG ĐO ĐƯỢC` kèm lý do, KHÔNG tính đạt. Điều kiện chặn: D2 (C1) và D6 (C2) là TIỀN ĐỀ — kết quả trái kỳ vọng ⇒ dừng, đi revision (§6). | Kết quả D2/D6 trái kỳ vọng ⇒ đỏ theo §6; thiếu hồ sơ native cho phép đã khai ⇒ đỏ. |

### 4b. Bảng đột biến — NGUỒN DUY NHẤT

Luật như P2a §4b (lượt gọi, `ngoai_le_la`, mỗi đột biến chỉ chạy ca đích, lượt đích = lượt ĐẦU TIÊN nó làm đỏ). Đột biến neo trên NGUỒN
CANDIDATE. Cột nền `nt` ⇒ đếm `chỉ_nt` trên nền khác. Cột "đo" = mọi lượt đổi màu trên nguyên mẫu §0.3, lượt đầu là đích; "lập
luận" = chưa chạy.

| # | phần | đột biến (phép thay) | ca · lượt | nhãn | cơ chế | nền | đo (nguyên mẫu §0.3; lượt đổi màu) |
|---|---|---|---|---|---|---|---|
| 1 | C1 | `db_nt_bo_win32` (bỏ kiểm (3)) | `phan_loai_nt` · `p13` | `ma` | H | mọi | đo: `p13`,`p14`,`p15`,`q05` |
| 2 | C1 | `db_nt_bo_dos` (bỏ (4)) | · `p16` | `ma` | H | mọi | đo: `p16`,`p17` |
| 3 | C1 | `db_nt_bo_nt` (bỏ (5)) | · `p18` | `ma` | H | mọi | đo: `p18` ⇒ `goc_o` |
| 4 | C1 | `db_nt_o_tran` (`r == ""` ⇒ coi như `\`) | · `p19` | `ma` | H | mọi | đo: `p19` |
| 5 | C1 | `db_nt_o_tuong_doi` (bỏ kiểm phân cách sau ổ) | · `p20` | `ma` | H | mọi | đo: `p20`,`q04` |
| 6 | C1 | `db_nt_o_chi_hoa` (`[A-Z]:`) | · `p03` | `ma` | H | mọi | đo: `p03` ⇒ `o_khac`, `q02` |
| 7 | C1 | `db_nt_khong_hoa_o` (bỏ `.upper()`) | · `p03` | `goc_tp` | H | mọi | đo: `p03`,`q02` |
| 8 | C1 | `db_nt_goc_o_tuyet_doi` (bỏ `goc_o`) | · `p21` | `ma` | H | mọi | đo: `p21`,`p22` |
| 9 | C1 | `db_nt_unc_share_rong` (regex nhận share rỗng) | · `p23` | `ma` | H | mọi | đo: `p23`,`p24`,`p26` |
| 10 | C1 | `db_nt_chi_gach_nguoc` (tách chỉ theo `\`) | · `p02` | `goc_tp` | H | mọi | đo: `p02`,`p04`,`p06`,`p29`,`q02` |
| 11 | C1 | `db_nt_bo_hai_cham` | · `p28` | `ma` | H | mọi | đo: `p28`–`p30`,`q08` |
| 12 | C1 | `db_nt_bo_ky_tu_cam` | · `p31` | `ma` | H | mọi | đo: `p31`,`p32` |
| 13 | C1 | `db_nt_bo_cuoi_cham` | · `p33` | `ma` | H | mọi | đo: `p33`,`p34` |
| 14 | C1 | `db_nt_bo_ten_tb` | · `p35` | `ma` | H | mọi | đo: `p35`–`p37` |
| 15 | C1 | `db_nt_o_khac_nhan` (`d` khác ⇒ nhận như ổ) | · `p27` | `ma` | H | mọi | đo: `p27` |
| 16 | C1 | `db_nt_goc_rong` | `chuan_nt` · `q06` | `goc_rong` | H | mọi | đo: `q06`,`q07` |
| 17 | C1 | `db_nt_cwd_khong_kiem` | · `q04` | `ly_do` | H | mọi | lập luận |
| 18 | C1 | `db_nt_khong_repr` | · `q08` | `mot_dong` | H | mọi | lập luận |
| 19 | C1 | `db_nt_unc_mo_som` | · `q10` | `unc_dong` | H | mọi | lập luận |
| 20 | C1 | `db_bo_reparse` (bỏ vế thuộc tính M4) | `reparse_gia_lap` · `W5.bit` | `reparse` | H | mọi | lập luận |
| 21 | C1 | `db_reparse_moi_thu` | · `W5.khong_bit` | `khong_bit` | H | mọi | lập luận |
| 22 | C1 | `db_nt_bo_chot` | `tich_hop_nt` · `W5.trong_kho` | `ly_do` | H | nt | lập luận |
| 23 | C1 | `db_nt_goc_cfg` | · `W5.jn_to_tien` | `lien_ket` | H | nt | lập luận (tương tự P2a 33) |
| 24 | C1 | `db_bo_reparse_nt` | · `W5.jn_cfg` | `lien_ket` | H | nt | chưa đo (D2) |
| 25 | C1 | `db_nt_ghi_duong_tho` | · `W5.tuong_doi` | `ket_qua` | H | nt | lập luận |
| 26 | C2 | `db_dd_bo_kiem` | `dinh_danh_gia_lap` · `trong_kho` | `ket_qua` | H | mọi | lập luận |
| 27 | C2 | `db_dd_bo_so_serial` | · `khac_vol` | `ket_qua` | H | mọi | lập luận |
| 28 | C2 | `db_dd_to_tien_la_cha` | · `to_tien` | `to_tien` | E — `FileNotFoundError` chứa `wp433-dd-thieu` | mọi | lập luận |
| 29 | C2 | `db_dd_khong_tim_thay_cho_qua` | · `khong_tim_thay` | `nem` | H | mọi | lập luận |
| 30 | C2 | `db_dd_mot_goc` | · `hai_goc` | `ket_qua` | H | mọi | lập luận |
| 31 | C2 | `db_dd_bo_noi_day` | `dinh_danh_that` · `noi_day` | `noi_day` | H | nt | lập luận |
| 32 | C2 | `db_dd_sai_chi_so` | · `theo_id` | `theo_id` | H | nt | lập luận |

Tổng: **32** (C1 **25**: 1–25, nền `mọi` 21, `nt` 4; C2 **7**: 26–32, `mọi` 5, `nt` 2). E: 1 (28). Không hai đột biến chung (ca, lượt,
nhãn): 6/7 cùng `p03` khác nhãn (6 đỏ ở `ma`, 7 qua `ma` rồi đỏ ở `goc_tp`); 20/24 cùng phép thay, khác ca (giả lập/native).

### 4c. Đo native Windows (phiên điều phối chạy trên `DESKTOP-T9R33P2`, dự phòng VM `tra-luat-win`)

Chung: `chcp 65001` và `set PYTHONIOENCODING=utf-8` trước mọi lệnh (console cp1258 giết `print` có dấu); gọi `python` (không giả định
`python3`); PowerShell: `Get-ChildItem -Force`, không đặt biến tên `$Args`; mọi thư mục thử nằm dưới `%TEMP%\wp433c-<giờ>` (một kho git
tạm `K` = `git init`, một thư mục ngoài kho `T`), dọn trong cùng phiên; ghi `python -VV`, `ver`, giờ `date -u` tương đương, nguyên văn đầu ra.

| # | phần | dựng / lệnh | kỳ vọng | không dựng được |
|---|---|---|---|---|
| D1 | C1 | Môi trường: `python -VV`; `reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\AppModelUnlock /v AllowDevelopmentWithoutDevLicense`; `git config --get core.symlinks`; hệ tệp volume của `%TEMP%` và của kho thật (`D:\Quốc hội\tra-luat`) qua `GetVolumeInformationW`; `fsutil 8dot3name query C:` | ghi lại, không có kỳ vọng | ghi KHÔNG ĐO ĐƯỢC từng mục |
| D2 | C1 (tiền đề) | `os.lstat` trên thư mục thường, junction (`mklink /J`), symlink thư mục (`mklink /D`), symlink tệp (`mklink`), và (nếu `mountvol` dùng được, cần admin) mount point: in `stat.S_ISLNK(st.st_mode)`, `st.st_file_attributes & 1024`, `hex(st.st_reparse_tag)` | thường: `False, 0`; junction, mount point: bit 1024 bật; symlink: bit bật. Junction cho `S_ISLNK` True thì đột biến 24 không còn là phép đỏ riêng — ghi lại, sửa revision. Bit KHÔNG bật cho junction ⇒ M4 không chặn được ⇒ DỪNG, revision | mount point không admin ⇒ KHÔNG ĐO ĐƯỢC |
| D3 | C1 | `os.lstat` trên `C:\`, `D:\`, `\\localhost\C$\`, `\\localhost\C$` | ổ có gạch cuối: thành công; UNC: ghi lại dạng nào thành công — gốc M1 (`\\máy\share\`) phải `lstat` được, sai ⇒ revision | `C$` cần quyền admin ⇒ KHÔNG ĐO ĐƯỢC |
| D4 | C1 | `os.getcwd()` trong `cmd` ở thư mục thường; trong PowerShell sau `Set-Location \\localhost\C$\Windows`; trên ổ `subst S: <T>` | dạng ổ hoa `X:\…` hoặc `\\máy\share\…`, không tiền tố `\\?\` | ghi KHÔNG ĐO ĐƯỢC từng vế |
| D5 | C1, C2 | Trên head: chạy fragment mới, fragment P2a, fragment packet 1 bằng bộ chạy fragment của kho (`python scripts/tl.py test-fragments-check --json` và chạy riêng từng fragment); thêm `python scripts/tl.py --selftest` nếu thời gian cho phép | mọi fragment `run` True; dòng tổng kết có `chỉ_nt=0`; fragment P2a `(w, t, v) == (7, 27, 21)`; `bỏ_qua` chỉ trong danh sách cho phép | không có |
| D6 | C2 (tiền đề) | Kho tạm `K\sub`. Đo `(serial, FileIndex64)` của `K\sub` qua (a) `K\sub`; (b) `\\localhost\C$\…\K\sub` (nếu `C$` dùng được); (c) share tạo trong shell ADMIN `net share tl433sub=<K\sub> /grant:%USERNAME%,FULL` rồi `\\localhost\tl433sub`; rồi `OpenFileById` với handle gợi ý `K` + chỉ số đo qua (c) ⇒ `GetFinalPathNameByHandleW` | (a)=(b)=(c); đường cuối == `K\sub` (normcase). Khác ⇒ cơ chế M6 không đứng ⇒ DỪNG, revision (§6) | không có admin để tạo share ⇒ KHÔNG ĐO ĐƯỢC; C2 KHÔNG được land khi D6(c) chưa đo (§6) |
| D7 | C2 | W5 thật (`python -c` gọi `_gws_auth_load` với Drive giả như fragment, hoặc `tl gws-auth-load` với `GOOGLE_WORKSPACE_CLI_CONFIG_DIR`): `\\localhost\tl433sub\gws` ⇒ `nằm trong kho git`; share `tl433out` của `<T>` ⇒ ghi được, tệp đúng; `net use Z: \\localhost\tl433sub` rồi `Z:\gws` ⇒ `nằm trong kho git`; `subst S: <K>\sub` rồi `S:\gws` ⇒ `nằm trong kho git`. Dọn: `net share tl433sub /delete`, `net share tl433out /delete`, `net use Z: /delete`, `subst S: /d` | như cột lệnh | thiếu admin ⇒ KHÔNG ĐO ĐƯỢC vế share/ổ ánh xạ |
| D8 | C1 | Tên 8.3: `dir /x` lấy tên ngắn của `K`; W5 với `<tên ngắn K>\gws` | `nằm trong kho git` | 8.3 tắt trên volume ⇒ KHÔNG ĐO ĐƯỢC |
| D9 | C1 | W5 với `cfgdir` dưới một thư mục tên có dấu và khoảng trắng (`<T>\Quốc hội\gws`), và trong kho thật `D:\Quốc hội\tra-luat\gwscfg` (dọn ngay) | ngoài kho: ghi được; trong kho: `nằm trong kho git` | không có |
| D10 | C1 | W5 với `cfgdir = \\localhost\C$\Windows\Temp\wp433c` (chỉ khi C1 land TRƯỚC C2) | `đường không hợp lệ`, không tệp nào được tạo | không có |

## 5. `pham_vi_e`

Không chạm E4, E5: chỉ sửa mã đường ghi; ca fragment dùng giá trị giả, HOME/cfgdir tạm, đồ giả thay tải Drive; không LIVE, không đẩy
Package. Phép đo native D6/D7 tạo/xoá share và ổ ánh xạ TẠM trên máy chủ kho bằng tay chủ kho (shell admin) — thao tác cục bộ, không
chạm dữ liệu kho hay credential thật.

## 6. `luat_dung`

- Trần lời gọi Codex theo dòng khai `ADR-0055`; chạm trần ⇒ Review Rescue Checkpoint; xin tăng mang **E2**.
- Trần kích thước theo dòng khai `ADR-0053` (≤ 6 tệp, ≤ 450 dòng thêm) đo bằng numstat thật (N8) TRƯỚC khi công bố; vượt ⇒ DỪNG, không
  push, không cắt ca. Tách hay nâng trần là quyết định của chủ kho — **E2** (§9 Q1).
- `_kiem_dich_ghi`, `_ghi_nguyen_tu_0600`, `_trong_kho_git`, `_dich_cred_gws` trên base thật khác §0.1, hoặc cần sửa thân ngoài M3/M4 ⇒ dừng, revision.
- Một neo §0.4 không còn khớp đúng 1 lần ⇒ dừng, revision (fragment P2a/packet 1 nằm ngoài write set).
- D2 (C1) hoặc D6 (C2) trái kỳ vọng ⇒ dừng, revision. D6(c) `KHÔNG ĐO ĐƯỢC` ⇒ C2 không được land; mở lại cần chủ kho quyết — **E2**.
- Chưa có comment cấp ngoại lệ bundled cho đúng `packet_id` trên #433 ⇒ không cấp lease (**E2**, §9 Q8).
- Đặc tả không thuộc Mission ⇒ chờ chủ kho duyệt băm theo `ADR-0067` — **E2**.

## 7. `hinh_dang_ke_thua`

Bộ đếm dùng chung với P2a/packet 1 (P2a §7): hình dạng "chốt nhìn THIẾU một phần của đường" đã bắt ba lớp (S5, L1, tổ tiên `cfgdir`).
P2c đáp hai lớp mới cùng hình dạng: (i) lớp TÊN — `ntpath` có nhiều cách viết một đường (gạch trộn, hoa/thường, `\\?\`, `\??\`, 8.3) ⇒
danh sách cho phép trên mã phân loại, mỗi nhánh một đột biến; (ii) lớp TRẦN của share — chuỗi tổ tiên UNC dừng ở gốc share ⇒ C2 đối
chiếu định danh. Mức đặc tả của P2c: 0 lượt review lúc soạn.

## 8. `chua_do_duoc`

- Mọi hành vi native Windows (§4c D1–D10) — phiên soạn không có Windows. Cụ thể chưa đo: junction có `S_ISLNK` hay không; bit reparse cho
  placeholder OneDrive/dedup qua `os.lstat` (CPython đi xuyên reparse không phải name-surrogate); `lstat` trên gốc UNC; định danh qua
  SMB loopback có bằng định danh cục bộ (D6 — tiền đề cả thiết kế C2); hành vi `OpenFileById` khi serial trùng tình cờ với volume máy khác.
- Nguyên mẫu chỉ phủ M1 và phần không-`unc` của M2; đột biến 17–32 là lập luận. Lời gọi `unc=True` của C2 trong `_dich_cred_gws_nt`
  không có đột biến trong fragment (đường UNC thật cần share) — chỉ D7 đo.
- ReFS (FileIndex 64 bit không đủ định danh); tên tệp ADS trên `credentials.json` (M1 đã chặn `:` trong thành phần, chưa đo hệ tệp).
- TOCTOU (§2).
- Kích thước (ước lượng tĩnh, chưa đo; mốc P2a thật: `tl_gws.py` +48/−19, fragment +389 cho 11 ca/46 lượt/37 đột biến, bundled +1, tổng
  +438):
  **C1** `tl_gws.py` +42–56 (M1 ~22–28, M2 ~10–13, M3 ~6–8, M4 +3, docstring/nhánh ~2); fragment +300–370 (khung, tự kiểm, đếm `chỉ_nt`
  ~110–125; rig W4/W5 + bọc `lstat` + dựng junction/symlink + probe ~70–85; bảng N1 37 lượt và N2 10 lượt dạng dữ liệu ~45–55; N3, N4
  ~45–60; `_DB` 25 mục ~28–32); bundled +1 ⇒ **343–427**, giữa ~385.
  **C2** `tl_gws.py` +45–62 (bindings ctypes ~16–20, `_dinh_danh_nt` ~8–10, `_duong_theo_dinh_danh_nt` ~12–15, `_kiem_dinh_danh_nt` ~10–13,
  `_goc_kho_tra_luat` ~3–4, nối dây ~2); fragment +190–250 (khung ~105–115, `be` giả giữ trạng thái ~30–40, N5/N6 ~35–55, `_DB` 7 mục
  ~8–10); bundled +1 ⇒ **236–313**, giữa ~275.
  **Trọn P2c** ⇒ **579–740**, vượt trần 450 ngay ở cận dưới ⇒ đề xuất TÁCH (§9 Q1). Biên trên C1 sát trần (427/450).

## 9. Câu hỏi cho chủ kho (mỗi câu **E2**: quyền quyết thuộc chủ kho; phiên soạn ĐÃ DỪNG ở đây)

- **Q1 — Kích thước.** Trọn P2c ~579–740 dòng > 450. (A) Tách C1 (đường + reparse, ~343–427) rồi C2 (định danh + mở UNC, ~236–313), mỗi
  phần một lease, ngân sách review riêng; (B) nâng trần cho P2c một lần (≥ 750). Khuyến nghị **A**: C1 tự đứng (đóng lỗ junction và
  dạng đường ngay), C2 phụ thuộc phép đo D6 cần shell admin.
- **Q2 — Cơ chế định danh cho UNC.** Văn bản quyết định 19-11: "so định danh của thư mục đích với gốc kho tra-luat và các tổ tiên của đích".
  Đọc theo chữ (A) — định danh từng tổ tiên của đích so với định danh gốc kho — KHÔNG bắt được share có gốc là thư mục CON của kho
  (`net share x=<kho>\sub`): chuỗi tổ tiên dừng ở `\\máy\x`, không bao giờ chạm gốc kho; đây đúng là finding P1 lượt 1 của P2a. (B) Đảo
  chiều (M6 của đặc tả này): lấy định danh tổ tiên gần nhất của đích; cùng serial volume với gốc kho thì mở theo định danh trên volume ấy
  (`OpenFileById`) để ra đường CỤC BỘ rồi chạy `_trong_kho_git` trên đường ấy — bắt được cả share gốc trong kho, ổ ánh xạ. (B') như B
  nhưng gợi ý volume bằng MỌI ổ cố định cục bộ thay vì gốc kho — bảo vệ mọi kho trên máy, rộng hơn quyết định thu hẹp. Khuyến nghị **B**.
- **Q3 — "Gốc kho tra-luat" là gì lúc chạy.** Ở Cowork, `tl_gws.py` chạy từ gói đã giải nén, không nằm trong kho git. Khuyến nghị: tập
  {kho chứa `tl_gws.py`, kho chứa `cwd`}, rỗng thì C2 không kiểm thêm (chỉ còn luật kho theo tên của `_kiem_dich_ghi`).
- **Q4 — Cùng serial mà `OpenFileById` không tìm thấy** (volume máy khác trùng serial 32 bit tình cờ, hoặc lỗi SMB). Khuyến nghị
  fail-closed: `ghi lỗi: OSError`. Phương án khác: coi là ngoài kho.
- **Q5 — UNC trong khoảng giữa C1 và C2.** Base hiện nhận UNC không kiểm gì. Khuyến nghị C1 TỪ CHỐI UNC (`đường không hợp lệ`) cho tới khi
  C2 land — quyết định 19-11 cho phép UNC gắn với điều kiện nhận diện bằng định danh. Phương án khác: C1 nhận UNC với luật kho theo tên.
- **Q6 — Mở rộng ngoài danh sách 19-11.** Đặc tả thêm: từ chối thành phần có `<>:"|?*`/ký tự điều khiển (chặn ADS), kết thúc bằng `.` hay
  khoảng trắng, tên thiết bị DOS (`CON`, `NUL.txt`, `COM1`…), `o_khac` (`1:`), và từ chối gốc trần `C:\`, `\\máy\share` (như `/` ở P2a; bản
  ban1 của P2a từng NHẬN gốc share). Khuyến nghị giữ cả (fail-closed, mỗi luật một đột biến).
- **Q7 — Reparse point.** M4 từ chối MỌI reparse point mà `lstat` báo bit (cả placeholder đám mây, dedup, AppExecLink), không chỉ
  junction/symlink/mount point. Hệ quả: `cfgdir` nằm trong thư mục OneDrive "chỉ trực tuyến" bị từ chối. Khuyến nghị giữ (fail-closed);
  phương án khác: chỉ từ chối tag name-surrogate (cần `st_reparse_tag`, chỉ có trên Windows).
- **Q8 — Ngoại lệ bundled** cho đúng `packet_id` (C, hoặc C1 và C2 riêng) — comment mới trên #433 sau khi duyệt băm; chặn lease, không chặn review.
- **Q9 — Phép đo admin.** D6(c), D7 cần chủ kho mở shell ADMIN trên Desktop để `net share`/`net use`. Đồng ý chạy (hoặc giao VM) không?
  Không ⇒ C2 dừng ở `KHÔNG ĐO ĐƯỢC` theo §6.

## 10. Nhật ký revision

- 2026-11-19T10:xxZ (phiên con của điều phối, soạn r1): đo §0 trên `11bd033`; nguyên mẫu M1/M2 và 16 đột biến trên Linux 3.11/3.13;
  bản lượt 1 đưa review Codex.
