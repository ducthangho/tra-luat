tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# GWS-CRED-DICH-NGOAI-KHO-C r1 — trên Windows, `credentials.json` của gws (W4, W5 trong `tl_gws.py`) chỉ ghi tới đường nằm trong danh sách cho phép, ngoài kho git (đích qua mạng đối chiếu bằng định danh tệp), không xuyên liên kết hay reparse point, ghi nguyên tử

- packet_id: GWS-CRED-DICH-NGOAI-KHO-C; revision: 1;

| trường | giá trị |
|---|---|
| `packet_issue` | #433 |
| `nguon_cap_viec` | Issue #433; đặc tả P2a `GWS-CRED-DICH-NGOAI-KHO-A-r1.md` (sha256 `b0065947…`, nhánh `ops/wp433-p2a-spec`, chưa vào master lúc soạn) §2 "Để P2c" mục (1)–(3), §9 Q1 tầng hai, Q2, Q4. Quyết định chủ kho 2026-11-19 (phiên điều phối #1206): cho phép UNC; UNC nhận diện bằng định danh tệp, không so chuỗi; reparse point (junction, symlink, mount point) thuộc P2c; danh sách cho phép đường Windows chạy mọi nền qua `ntpath`, kèm gạch trộn, hoa/thường ổ, `..` kiểu Windows, mỗi namespace thiết bị một nhãn. |
| `phu_thuoc` | P2a ĐÃ LAND (PR #1415; `git diff --numstat 417b593^1 417b593` = fragment +389, `tl_gws.py` +48/−19, bundled +1; tổng +438; `417b593` là tổ tiên của `11bd033`). P2c thay nhánh `os.name != "posix"` của `_dich_cred_gws`, gọi lại `_kiem_dich_ghi`, `_ghi_nguyen_tu_0600`, `_trong_kho_git`, `_safe_exc` và hợp đồng lỗi sáu cụm của P2a. P2b không là tiền đề. |
| `review_class` | `sensitive` (`scripts/tl_gws.py` là đường ghi credential). Đối chiếu `lease_publish check` khi cấp lease. |
| `base` | `11bd0336d00b4a9544e70dcbbe049d372053a3ec` lúc soạn (đo 2026-11-19T10:08:01Z); blob `scripts/tl_gws.py` `9ec027c2808868a05b67adc3d93ea68a574d6ec0`, 2649 dòng (= blob tại `417b593`). Lease ghi base thật; phiên thi hành đo lại §0 trước khi sửa. |
| `tach_de_xuat` | Trọn gói vượt trần 450 (§8). Mọi mục, ca, đột biến mang một thẻ: **[C1]** danh sách cho phép đường + nối nhánh Windows + loại ổ; **[R]** vế reparse trong `_kiem_dich_ghi`; **[C2]** định danh tệp Win32 cho đích qua mạng (UNC, ổ mạng). Thứ tự land: C1 → R → C2 (R và C2 cần nhánh nt của C1). Chủ kho chọn cách gộp ở §9 Q1 (**E2**). |

## 0. Hiện trạng (đo trên `11bd033`, Linux, CPython 3.11.18 / 3.12.3 / 3.13.18, `python -I`, không mạng)

### 0.1 Nhánh Windows hiện tại

| chỗ | dòng | hành vi |
|---|---|---|
| `_dich_cred_gws` | 1201–1210 | nhánh `if os.name != "posix": return os.path.join(cfgdir_tho, "credentials.json"), None` (1204–1205): không chuẩn hoá, không chốt kho, không chốt liên kết. |
| `_kiem_dich_ghi` | 1173–1187 | luật (b) chỉ `stat.S_ISLNK(os.lstat(tien_to).st_mode)` (1183); docstring tự khai "junction/reparse Windows chưa chặn". Người gọi: W4/W5 qua `_dich_cred_gws`, W1–W3 (`_dich_jar_nlm` 1233), W6 (1784). |
| W4 / W5 | 1803–1823 / 1961–1968 | gọi `_dich_cred_gws(cfgdir)` (1813 / 1963) rồi `_ghi_nguyen_tu_0600` trong một `try … except OSError`. |
| `_trong_kho_git` | 1119–1139 | đi lên trên `abspath` và `realpath` tìm `.git` bằng `lstat`, nuốt mọi `OSError`. Gốc share UNC là trần của chuỗi: share có gốc là thư mục CON của một kho thì `.git` nằm trên trần, không thấy (finding P1 lượt 1 của P2a). Ổ mạng (`net use`) có cùng trần. |

### 0.2 Phép đo `ntpath` (2026-11-19T10:04:39Z; `nguyen-mau/do_ntpath.py`, `ntpath-3.1x.txt`)

28 đầu vào của `do_ntpath.py`: `splitdrive` GIỐNG NHAU trên 3.11/3.12/3.13, ví dụ `\\server\share\x`→(`\\server\share`,`\x`);
`\\server`→(`\\server`,``); `\\?\C:\x`→(`\\?\C:`,`\x`); `\\\server\share`→(`\\\server`,`\share`); `\\server\\share`→(`\\server\`,`\share`);
`1:\x`→(`1:`,`\x`). `isabs` LỆCH: `\fake`, `/fake` ⇒ True trên 3.11/3.12, False trên 3.13 ⇒ không gọi `isabs`. `splitroot` chỉ có từ 3.12
(kho khai Python ≥ 3.11) ⇒ không dùng. `ntpath.isreserved` chỉ có từ 3.13 ⇒ không dùng. `stat.FILE_ATTRIBUTE_REPARSE_POINT` = 1024 có
trên Linux cả ba bản; `stat.IO_REPARSE_TAG_*`, `ctypes.WinDLL` không có ⇒ mã Win32 nạp lười, chỉ khi `os.name == "nt"`.

### 0.3 Nguyên mẫu M1/M2 (KHÔNG phải mã thi công; `nguyen-mau/nguyen_mau_c1_r2.py`, `do_dot_bien_r2.py`)

Đo 2026-11-19T10:22:55Z trên 3.11, 3.12, 3.13, cùng đầu ra: nguyên mẫu cho đúng mã/gốc/thành phần của 43 lượt N1 và 13 lượt N2 `q01`–`q13`
(phần chưa có loại ổ, mã công khai và `repr`). Bộ chạy đột biến kiểm neo khớp đúng 1 lần, so lượt đầu đổi màu với lượt đích khai, trả
rc ≠ 0 khi lệch: **25/25 khớp, rc 0** trên cả ba bản (`dot-bien-r2-3.1x.txt`). Đó là các dòng §4b có cột "đo".

### 0.4 Ràng buộc kề bên

- **Neo của fragment P2a** (`wp433_gws_cred_dich_ngoai_kho.py`, blob `2783e20c…`, 389 dòng, 37 mục `_DB`) và **fragment packet 1**
  (`wp433_nlm_gws_dich_ngoai_kho.py`, 30 mục `_DB`) phải khớp ĐÚNG MỘT lần trên candidate. Đếm trên base (review lượt 1): mọi neo đúng
  1 lần. Neo dễ chạm: `_kiem_dich_ghi(dest, "/", (*chuan[1], "credentials.json"))`, `"\ndef _dich_cred_gws("`, `return ly if not tp or
  ".." in tp else`, `if "\x00" in p or p.strip() == "":`, `ly = f"đường không hợp lệ: {repr(p)[:200]}"`, `{repr(kho_dich)[:200]}`,
  `for i in range(len(thanh_phan) + 1):` (cả hai fragment), `ly_cfg = _kiem_dich_ghi(cfgp, cfgp, ())`. Mã mới không chứa lại nguyên văn
  các chuỗi ấy; R GIỮ nguyên dòng vòng `for i …`.
- Fragment P2a trên nt đòi `(w, t, v) == (7, 27, 21)` (`chỉ_posix`); ba trong bốn ca `mọi` của nó đi qua W4/W5 nên sau C1 đi nhánh nt
  mới; `m1_bien` gọi `_duong_dich_chuan` (POSIX) trực tiếp. Fragment P2a và packet 1 chưa có biên nhận chạy trên Windows thật trong kho
  lúc soạn (hồ sơ land P2a nhánh `ops/land-1414-1415` ghi "Windows native 0/1 (tuỳ chọn)").
- Backend Win32 có sẵn ở `.claude/dev/packet_loop.py:6408–6500` (#1174/#1342) và `.claude/dev/launcher.py:4030–4100`: bindings
  argtypes/restype tường minh, `use_last_error=True`, `BY_HANDLE_FILE_INFORMATION` 13 DWORD (`[0]` thuộc tính, `[7]` serial, `[11]`/`[12]`
  chỉ số cao/thấp), cờ `0x02000000` (BACKUP_SEMANTICS) và `0x00200000` (OPEN_REPARSE_POINT), đóng handle trong `finally`. `.claude/` bị
  loại khỏi gói nên `scripts/tl_gws.py` không import được: C1/C2 chép MẪU, không chép hàm.
- Bước CI `bundled-fragment check` kiểm bundled committed; manifest committed chỉ kiểm trên master. Fragment in ra STDERR. Không có CI
  Windows bắt buộc. Đo native: Desktop `DESKTOP-T9R33P2` (Developer Mode bật 19-11; `core.symlinks=true`), VM `tra-luat-win` dự phòng.
  Phiên soạn không truy cập được máy ấy (§4c).

## 1. `write_set`

Mỗi phần một packet (khi tách), mỗi phần ba tệp:

```
C1: scripts/tl_gws.py
    scripts/test_fragments/wp433_gws_cred_win_duong.py
    scripts/tl_test_fragments_bundled.py
R:  scripts/tl_gws.py
    scripts/test_fragments/wp433_gws_cred_win_reparse.py
    scripts/tl_test_fragments_bundled.py
C2: scripts/tl_gws.py
    scripts/test_fragments/wp433_gws_cred_win_dinh_danh.py
    scripts/tl_test_fragments_bundled.py
```

Gộp phần nào thì write set là hợp các dòng của phần ấy. KHÔNG `RELEASE_MANIFEST.json`. `scripts/tl_test_fragments_bundled.py` theo tiền
lệ phương án B (chủ kho 18-11-2026; P2a §1): chỉ sinh bằng `generate_bundled_module_bytes(scripts/test_fragments)`. **Điều kiện trước
khi cấp lease (E2, §9 Q8):** comment của chủ kho trên #433 cấp ngoại lệ ấy nêu đúng `packet_id` của phần, đúng một tệp
`scripts/tl_test_fragments_bundled.py` và sha256 đặc tả đã đóng băng; lease trỏ URL comment. Comment `7002145681` (P2a) không phủ.
Phiên land tái sinh `RELEASE_MANIFEST.json` trong commit land.

## 2. `ngoai_pham_vi`

- POSIX: không đổi hành vi nhánh `posix`; `_duong_dich_chuan` (POSIX) không sửa.
- Phân loại đường cho W1–W3, W6: không. Riêng R sửa THÂN `_kiem_dich_ghi` nên áp cho mọi người gọi, trên đúng các tiền tố mà người gọi
  truyền (`goc` + `thanh_phan`); không mở rộng chuỗi tiền tố của W1–W3/W6 lên trên `goc` của họ (P2a §2 mục (3) đã giao M6 cũ cho P2c).
- C2 bảo vệ mọi kho git trên các ổ CỤC BỘ có ký tự ổ (§3 M6); volume không có ký tự ổ (gắn vào thư mục) không được duyệt (§8).
- Định danh 128 bit (`FILE_ID_INFO`, ReFS): không.
- Reparse tag không phải name-surrogate (placeholder đám mây, dedup): CPython `os.lstat` có thể đi xuyên chúng (chưa đo, §8). R chỉ cam
  kết các entry mà `os.lstat` trả bit 1024.
- TOCTOU: như P2a §2 — kiểm theo TÊN rồi ghi theo TÊN; định danh C2 là phép đo tại một thời điểm. Thư mục cha, share hay ánh xạ ổ đổi
  giữa lúc kiểm và `os.replace` nằm ngoài bảo đảm; không ca nào đo khe này.
- Không sửa `ops/**`, `.github/**`, `scripts/tl_selftest.py`, fragment P2a, fragment packet 1, `RELEASE_MANIFEST.json`, `changelog.d/*`,
  `VERSION`, `CHANGELOG.md`, `SKILL.md`. Không thêm CI Windows. P2b là packet riêng.

## 3. `muc_tieu`

| # | phần | mục tiêu | tệp |
|---|---|---|---|
| M1 | C1 | Hàm thuần `_phan_loai_duong_nt(p)` trên `ntpath` import tường minh (không `os.path`, `isabs`, `splitroot`, `isreserved`, `abspath`, `normpath`, `realpath`), trả tuple mà phần tử đầu là MÃ. Kiểm THEO THỨ TỰ, mã đầu tiên khớp thắng: (1) `"\x00" in p` ⇒ `nul`; (2) `p.strip() == ""` ⇒ `trang`; (3) `re.match(r"[\\/]{2}\?[\\/]", p)` ⇒ `thiet_bi_win32`; (4) `re.match(r"[\\/]{2}\.[\\/]", p)` ⇒ `thiet_bi_dos`; (5) `re.match(r"[\\/]\?\?[\\/]", p)` ⇒ `nt_doi_tuong`; (6) `d, r = ntpath.splitdrive(p)`. `d` `fullmatch` `[A-Za-z]:`: `r == ""` ⇒ `o_tran`; `r[0]` không phải `\`/`/` ⇒ `o_tuong_doi`; còn lại loại `o_tuyet_doi`, gốc `d.upper() + "\\"`. `d` mở bằng hai phân cách: không `fullmatch` `[\\/]{2}([^\\/]+)[\\/]([^\\/]+)` ⇒ `unc_thieu_share`; máy hoặc share vi phạm luật thành phần (8) ⇒ mã của luật ấy; share là `IPC$` (không phân biệt hoa/thường) ⇒ `unc_ipc`; còn lại loại `unc`, gốc `\\<máy>\<share>\` (phân cách chuẩn `\`, giữ hoa/thường). `d == ""`: `p[0]` là phân cách ⇒ `goc_o`; còn lại loại `tuong_doi`, gốc `None`. `d` khác ⇒ `o_khac`. (7) tách `r` theo `\`/`/`, bỏ thành phần rỗng (gạch lặp, gạch cuối) và `.`; còn `..` ⇒ `hai_cham`. (8) Luật thành phần, áp cho từng thành phần và cho máy/share: chứa một ký tự trong `<>:"\|?*` hay mã `\x01`–`\x1f` ⇒ `ky_tu_cam`; `t.endswith((".", " "))` ⇒ `cuoi_cham_cach`; `fullmatch` không phân biệt hoa/thường `(CON\|PRN\|AUX\|NUL\|COM[0-9¹²³]\|LPT[0-9¹²³]\|CONIN\$\|CONOUT\$) *(\..*)?` ⇒ `ten_thiet_bi`. (9) Hết ⇒ `(loại, gốc, thành_phần)`. Unicode và khoảng trắng GIỮA tên được nhận. | `scripts/tl_gws.py` |
| M2 | C1 | `_duong_dich_chuan_nt(p, cwd, unc=False, loai_o=None)` trả `(kieu, gốc, thành_phần)` với `kieu` ∈ {`cuc_bo`, `mang`}, hoặc lý do MỘT dòng `đường không hợp lệ: <repr(x)[:200]>` (x = `cwd` khi lỗi ở `cwd`, ngược lại `p`). Loại `tuong_doi`: phân loại `cwd` bằng M1; `cwd` phải là `o_tuyet_doi` hoặc `unc`; ghép THÀNH PHẦN `cwd + p` (không ghép chuỗi). Loại khác `o_tuyet_doi`/`unc` ⇒ từ chối. Không còn thành phần nào (`C:\`, `\\máy\share`, `.` khi `cwd` là gốc) ⇒ từ chối. Loại `o_tuyet_doi`: `loai_o(gốc)` (mặc định `_loai_o_nt`, `GetDriveTypeW`) ∈ {2 REMOVABLE, 3 FIXED} ⇒ `cuc_bo`; = 4 REMOTE ⇒ `mang`; khác ⇒ từ chối. Loại `unc` ⇒ `mang`. `kieu == "mang"` và `unc` sai ⇒ từ chối (C1 đóng đích qua mạng tới khi C2 land, §9 Q5). | `scripts/tl_gws.py` |
| M3 | C1 | Nhánh `os.name != "posix"` của `_dich_cred_gws` thành `return _dich_cred_gws_nt(cfgdir_tho)`. `_dich_cred_gws_nt(cfgdir_tho)` (KHÔNG tạo/ghi gì): `os.getcwd()` MỘT lần; M2; `dest = gốc + "\\".join((*tp, "credentials.json"))`; lý do = `_kiem_dich_ghi(dest, gốc, (*tp, "credentials.json"))`; [C2] rồi `_kiem_dinh_danh_nt(dest, kieu)`. Trả `(dest, lý_do)`; `dest` là đường DUY NHẤT được kiểm, ghi và (W5) trả về. W4, W5 không đổi. Văn bản mới không chứa lại neo §0.4. | `scripts/tl_gws.py` |
| M4 | R | Thân `_kiem_dich_ghi`: thay ĐÚNG biểu thức nhận diện ở 1183 bằng `st = os.lstat(tien_to)` và điều kiện `stat.S_ISLNK(st.st_mode) or getattr(st, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT`; cụm giữ `là liên kết tượng trưng`; dòng vòng, chữ ký, thứ tự luật, nhánh `FileNotFoundError`/`NotADirectoryError` giữ nguyên; docstring bỏ câu "junction/reparse Windows chưa chặn". | `scripts/tl_gws.py` |
| M5 | C2 | Backend Win32 (nạp lười khi `os.name == "nt"`, gom vào namespace `_BE_DD_NT` để fragment thay được): (a) `dinh_danh(duong)` — `CreateFileW(duong, 0x80 FILE_READ_ATTRIBUTES, 7, None, 3, 0x02000000 \| 0x00200000, None)`, `GetFileInformationByHandle` ⇒ `(serial, (cao << 32) \| thấp, la_thu_muc = bool([0] & 0x10))`; (b) `o_cuc_bo()` — `GetLogicalDrives`, với mỗi `X:\` có `GetDriveTypeW` ∈ {2, 3}: `GetVolumeInformationW` ⇒ `(gốc, serial)`; lỗi `ERROR_NOT_READY` (21) thì bỏ ổ ấy, lỗi khác ném; (c) `theo_dinh_danh(goc_o, serial, chi_so)` — mở `goc_o` như (a) làm handle gợi ý; `FILE_ID_DESCRIPTOR` = {`dwSize` = `ctypes.sizeof` của chính cấu trúc (DWORD + enum + union 16 byte gồm `LARGE_INTEGER FileId`), `Type = 0` FileIdType, `FileId = chi_so`}; `OpenFileById(gợi_ý, byref(desc), 0x80, 7, None, 0x02000000 \| 0x00200000)`; thất bại với `ERROR_INVALID_PARAMETER` (87) hoặc `ERROR_FILE_NOT_FOUND` (2) ⇒ `None` (không có trên volume này), lỗi khác ném; mở được thì đọc lại `GetFileInformationByHandle` trên handle mới, đòi serial == `serial`, chỉ số == `chi_so`, là thư mục — lệch ⇒ ném `OSError`; `GetFinalPathNameByHandleW(h, buf, 32768, 0)`: trả 0 ⇒ `WinError`, ≥ 32768 ⇒ ném; chỉ nhận dạng `\\?\X:\…` (bỏ đúng 4 ký tự đầu), dạng khác ⇒ ném. Mọi lỗi Win32 ⇒ `ctypes.WinError(ctypes.get_last_error())`; mọi handle đóng trong `finally`. `_loai_o_nt` (C1, M2) cũng nằm ở đây khi C2 land; ở C1 là một hàm `GetDriveTypeW` lười riêng. | `scripts/tl_gws.py` |
| M6 | C2 | `_kiem_dinh_danh_nt(dest, kieu, be=None)` (logic thuần trên `ntpath` + `be`, mặc định `_BE_DD_NT`): `kieu == "cuc_bo"` ⇒ `None` TRƯỚC mọi lời gọi `be` (đích cục bộ đã được `_kiem_dich_ghi` kiểm qua `realpath`). Ngược lại: `a = ntpath.dirname(dest)`; lặp `be.dinh_danh(a)`: `FileNotFoundError` ⇒ nếu `a` là gốc (`ntpath.dirname(a) == a`) thì ném lại, không thì `a = ntpath.dirname(a)`; lỗi khác ném. Có `(s, i, _)`: với MỖI `(g, sg)` trong `be.o_cuc_bo()` mà `sg == s`: `L = be.theo_dinh_danh(g, s, i)`; `L is None` ⇒ xét ổ kế; `_trong_kho_git(L)` khác `None` ⇒ trả `nằm trong kho git: <repr(kho)[:200]>`. Hết ⇒ `None`. M3 gọi M2 với `unc=True`. Ý nghĩa: đích qua mạng mà đối tượng thật nằm trên một ổ cục bộ ⇒ quy về đường cục bộ rồi chốt kho như đường cục bộ; không ổ cục bộ nào cùng serial ⇒ đích ở máy khác ⇒ ngoài mọi kho cục bộ. | `scripts/tl_gws.py` |
| M7 | C1+R+C2 | Hợp đồng lỗi: GIỮ sáu cụm của P2a, không thêm cụm. Từ chối của M1/M2 ⇒ `đường không hợp lệ`; liên kết/reparse ⇒ `là liên kết tượng trưng`; định danh quy về kho ⇒ `nằm trong kho git`; lỗi Win32/`OSError` khác ⇒ `ghi lỗi: <_safe_exc(e)>` (tên lớp). W4 một dòng `[bootstrap] ✗ <cụm>: .+`, rc 1, `degraded`; W5 `(False, "<cụm>: …")`; `cmd_gws_auth_load` một dòng, rc 2 — như P2a M3. Mọi từ chối/lỗi xảy ra TRƯỚC writer: không tệp mới, không tệp tạm. | `scripts/tl_gws.py` |
| M8 | mỗi phần | Fragment của phần (`TEST_ID` = tên tệp không đuôi): khuôn fragment P2a, tự chứa, nạp `tl_gws` vào bộ nhớ, đột biến trên bản sao, neo khớp đúng 1 lần, phân hạng `TinHieuChotCa(AssertionError)` theo (ca, lượt, nhãn), sổ `_LUOT_DU_KIEN` và `_DU_KIEN` viết riêng, trạng thái lượt `đạt`·`đỏ`·`bỏ_qua`·`chỉ_nt`, mọi đầu ra ra STDERR, khôi phục trong `finally`. Tái sinh bundled bằng `generate_bundled_module_bytes`. | fragment, bundled |

## 4. `nghiem_thu`

Ký hiệu như P2a §4 (K = kho git tạm, T = thư mục tạm ngoài kho, gốc rig = `realpath(mkdtemp())`). Nền `mọi` hoặc `nt`; ca `nt` trên
nền khác: mọi lượt `chỉ_nt`. Mỗi lượt thu đủ hậu điều rồi so nhãn theo thứ tự ghi; nhãn đỏ đầu tiên là tín hiệu; ca dừng ở lượt đỏ đầu.
"W5 đúng" = `(False, s)`, `s` `fullmatch` `<cụm>: .+`, một dòng. Lý do M2 "đúng" = `fullmatch` `đường không hợp lệ: .+`, không `\n`,
chứa `repr` của đúng `x` (M2).

| # | phần · ca (nền) | lượt và tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|---|
| N1 | C1 · `phan_loai_nt` (mọi), gọi thẳng `_phan_loai_duong_nt` | 43 lượt, mỗi lượt nhãn [`ma`] rồi (loại nhận) [`goc_tp`]. Nhận: `p01` `C:\x`⇒`o_tuyet_doi`,`C:\`,(`x`); `p02` `C:/x`, `p03` `c:\x` ⇒ như `p01`; `p04` `C:\a/b\c`⇒(`a`,`b`,`c`); `p05` `\\server\share\x`, `p06` `//server/share/x`, `p07` `/\server\share\x` ⇒ `unc`,`\\server\share\`,(`x`); `p08` `fake`⇒`tuong_doi`,`None`,(`fake`); `p09` `C:\x\.\y\\`⇒(`x`,`y`); `p10` `D:\Quốc hội\tra-luat`⇒`D:\`,(`Quốc hội`,`tra-luat`); `p43` `\\server\share\\x`⇒ như `p05`. Từ chối: `p11` `a\x00b` `nul`; `p12` `   ` `trang`; `p13` `\\?\C:\x`, `p14` `//?/C:/x`, `p15` `\\?\UNC\s\sh` `thiet_bi_win32`; `p16` `\\.\pipe\x`, `p17` `//./C:/x` `thiet_bi_dos`; `p18` `\??\C:\x` `nt_doi_tuong`; `p19` `C:` `o_tran`; `p20` `D:fake` `o_tuong_doi`; `p21` `\fake`, `p22` `/fake` `goc_o`; `p23` `\\server`, `p24` `\\server\`, `p25` `\\\server\share`, `p26` `\\server\\share` `unc_thieu_share`; `p27` `1:\x` `o_khac`; `p28` `C:\a\..\b`, `p29` `a/../b`, `p30` `..` `hai_cham`; `p31` `C:\x:ads`, `p32` `C:\a\|b` `ky_tu_cam`; `p33` `C:\a.\b`, `p34` `C:\a ` `cuoi_cham_cach`; `p35` `C:\CON`, `p36` `C:\nul.txt`, `p37` `C:\com1\x`, `p38` `C:\NUL .txt`, `p39` `C:\CONIN$` `ten_thiet_bi`; `p40` `\\server.\share\x` `cuoi_cham_cach`; `p41` `\\server\sh:a\x` `ky_tu_cam`; `p42` `\\server\IPC$\x` `unc_ipc`. Base: hàm chưa có ⇒ lượt đầu đỏ (`ngoai_le_la`). | §4b dòng 1–21 (đo trên nguyên mẫu §0.3). |
| N2 | C1 · `chuan_nt` (mọi), gọi thẳng `_duong_dich_chuan_nt` với `loai_o` giả (mặc định trả 3; ghi riêng khi khác) | `q01` (`fake`, `C:\cwd`) ⇒ [`ket_qua`] (`cuc_bo`, `C:\`, (`cwd`,`fake`)); `q02` (`a\b`, `c:/cwd`) ⇒ (`cuc_bo`, `C:\`, (`cwd`,`a`,`b`)); `q03` (`fake`, `\\s\sh\d`, `unc=True`) ⇒ (`mang`, `\\s\sh\`, (`d`,`fake`)); `q04` (`fake`, `D:rel`) ⇒ [`ly_do`] chứa `repr('D:rel')`; `q05` (`fake`, `\\?\C:\cwd`) ⇒ [`ly_do`] chứa `repr` của cwd; `q06` (`C:\`) và `q07` (`\\server\share`, `unc=True`) ⇒ [`goc_rong`] lý do đúng; `q08` (`x\n\..`) ⇒ [`mot_dong`] lý do đúng; `q09` (`x`, `C:\`) ⇒ [`ket_qua`] (`cuc_bo`, `C:\`, (`x`,)); `q10` (`fake`, `\\s\sh\d`, `unc=False`) ⇒ [`unc_dong`] lý do; `q11` (`\\server\share\x`, KHÔNG truyền `unc`) ⇒ [`unc_dong`] lý do; `q12` (`.`, `C:\cwd`) ⇒ [`ket_qua`] (`cuc_bo`, `C:\`, (`cwd`,)); `q13` (`.`, `C:\`) ⇒ [`goc_rong`]; `q14` (`Z:\x`, `loai_o` ⇒ 4, KHÔNG truyền `unc`) ⇒ [`unc_dong`]; `q15` (`Z:\x`, `loai_o` ⇒ 4, `unc=True`) ⇒ [`ket_qua`] (`mang`, `Z:\`, (`x`,)); `q16` (`E:\x`, `loai_o` ⇒ 5) ⇒ [`ly_do`]. | §4b dòng 22–28. |
| N3 | R · `reparse_gia_lap` (mọi) — bọc `os.lstat` trong cửa sổ gọi: với ĐÚNG đường `cfgdir` của lượt (so sau `normcase(normpath)`) trả `SimpleNamespace(st_mode=stat.S_IFDIR \| 0o700, st_file_attributes=<a>)`, đường khác đi hàm thật | `W5.bit` (`a = 1024`) ⇒ [`reparse`] W5 đúng với `là liên kết tượng trưng`, chi tiết `repr(cfgdir)`, không tệp dưới `cfgdir` thật; `truc_tiep` — gọi thẳng `_kiem_dich_ghi(<T>/x/credentials.json, <T>, ("x", "credentials.json"))`, `a = 1024` cho `<T>/x` ⇒ [`reparse_truc_tiep`] lý do như trên; `W5.khong_bit` (`a = 16`) ⇒ [`khong_bit`] `(True, d)`, tệp đúng byte. Trên POSIX W5 đi nhánh P2a, trên nt nhánh C1 — cùng một `_kiem_dich_ghi`. | §4b dòng 34–35. |
| N4 | C1 · `tich_hop_nt` (nt) — W4 fixture gws chuẩn của P2a, W5 với `_public_curl_bytes` giả | `W5.trong_kho` `cfgdir = <K>\gwscfg` ⇒ [`ly_do`] W5 đúng `nằm trong kho git`, sạch(K); `W4.trong_kho` cùng `cfgdir` ⇒ [`w4`] rc 1, đúng một dòng `[bootstrap] ✗ nằm trong kho git: …`; `W5.tuong_doi` cwd `<T>`, `cfgdir = cfg` ⇒ [`ket_qua`] `(True, d)`, `d == <gốc ổ hoa của T>…\cfg\credentials.json` (dạng M2), tệp đúng byte; `W5.o_thuong` `cfgdir` = `<T>` viết ổ thường, gạch `/` ⇒ [`ket_qua`] `d` ổ hoa, chỉ `\`; `W5.o_tuong_doi` `<ổ của T>:cfg` ⇒ [`ly_do`] `đường không hợp lệ`; `W5.hai_cham` `<T>\x\..\cfg` ⇒ [`ly_do`] `đường không hợp lệ`. Mọi lượt từ chối: không tệp mới dưới `cfgdir`, không `.auth.json.*`. | §4b dòng 29–30. |
| N4r | R · `lien_ket_nt` (nt) — junction bằng `_winapi.CreateJunction` (thiếu thì `cmd /c mklink /J` ngoài cửa sổ chặn), symlink bằng `os.symlink`; mọi fixture nằm dưới T (ngoài kho) | `W5.jn_to_tien` `<T>\jn\a\b` (`jn` junction → `<T>\that`) ⇒ [`lien_ket`] chi tiết `repr(<T>\jn)`, `<T>\that` không tệp mới; `W5.jn_cfg` `cfgdir` là junction ⇒ [`lien_ket`]; `W5.sl_dir` `cfgdir` là symlink thư mục ⇒ [`lien_ket`]; `W5.sl_tep` `credentials.json` là symlink tệp tới `<T>\dich.json` (`CU`) ⇒ [`lien_ket`], `dich.json` còn `CU`. Danh sách cho phép `bỏ_qua`: ĐÚNG hai lượt `W5.sl_dir`, `W5.sl_tep`, chỉ khi `os.symlink` trên CHÍNH thư mục fixture ném `OSError` có `winerror == 1314`; lỗi khác ⇒ `đỏ` với `probe symlink: <repr(lớp, errno, winerror)>`. | §4b dòng 36–37. `W5.sl_dir`, `W5.sl_tep`: CHƯA có phép đỏ riêng (đột biến bỏ cả hai vế của luật (b) dừng ở `W5.jn_to_tien`); khai, không làm tròn. |
| N5 | C2 · `dinh_danh_gia_lap` (mọi), gọi thẳng `_kiem_dinh_danh_nt(dest, kieu, be)`; `be` giả GIỮ trạng thái: tập đường tồn tại (`dinh_danh` trên đường vắng ném `FileNotFoundError("wp433-dd-thieu")`), bảng định danh, danh sách `o_cuc_bo`, bảng `theo_dinh_danh` trỏ tới đường THẬT của rig (K có `.git`, T không), nhật ký lời gọi; mọi `dest` có thư mục cha tồn tại trừ khi ghi khác | `cuc_bo` (`kieu = "cuc_bo"`; fixture vẫn có thư mục cha tồn tại, một ổ cùng serial ánh xạ ⇒ `<T>/out`, để bỏ nhánh tắt vẫn trả `None`) ⇒ [`ket_qua`] `None`, [`khong_goi`] 0 lời gọi `be`; `trong_kho` (`mang`, một ổ cùng serial ⇒ `<K>/sub`) ⇒ [`ket_qua`] `nằm trong kho git: ` + `repr(K)`; `ngoai_kho` (⇒ `<T>/out`) ⇒ [`ket_qua`] `None`; `khac_vol` (không ổ nào cùng serial; bảng vẫn có ánh xạ ⇒ `<K>/sub`) ⇒ [`ket_qua`] `None`, [`khong_goi`] 0 lời gọi `theo_dinh_danh`; `hai_vol` (hai ổ cùng serial: ổ đầu ⇒ `None`, ổ sau ⇒ `<K>/sub`) ⇒ [`ket_qua`] lý do kho; `to_tien` (chỉ `\\s\sh\a` tồn tại, `dest` = `\\s\sh\a\b\credentials.json`) ⇒ [`to_tien`] `dinh_danh` gọi lần lượt `\\s\sh\a\b` rồi `\\s\sh\a`, kết quả đúng; `quyen` (`dinh_danh` ném `PermissionError("wp433-dd-quyen")`) ⇒ [`nem`] ném đúng ngoại lệ ấy; `goc_thieu` (cả gốc `\\s\sh\` vắng) ⇒ [`nem`] `FileNotFoundError`. | §4b dòng 38–44. |
| N6 | C2 · `dinh_danh_that` (nt) | `on_dinh` — `be.dinh_danh(<T>)` hai lần bằng nhau, `<T>\sub` cùng serial khác chỉ số, `la_thu_muc` đúng ⇒ [`on_dinh`]; `o_cuc_bo` — danh sách chứa gốc ổ của T với serial == serial của T ⇒ [`o_cuc_bo`]; `theo_id` — `be.theo_dinh_danh(<gốc ổ T>, s, chi_so(<T>\sub))` so `normcase` bằng `realpath(<T>\sub)` ⇒ [`theo_id`]; `noi_day` — W5 với `cfgdir = <T>\cfg`, `_loai_o_nt` giả trả 4 cho ổ của T, `be` giả ánh xạ định danh của `<T>` sang `<K>\sub` ⇒ [`noi_day`] W5 đúng `nằm trong kho git`, không tệp mới; `ngoai` — cùng nhưng `be` thật ⇒ [`ngoai`] `(True, d)`. | §4b dòng 45–47. |
| N7 | mỗi phần · tự kiểm | (a) `_DU_KIEN` == tập ID `_DB` (đếm cả số lần xuất hiện); mỗi mục giết đúng (ca, lượt, nhãn). (b) `_LUOT_DU_KIEN` viết riêng; tập và số lần (ca, lượt) đã ghi trạng thái BẰNG sổ. Sổ: **C1** 3 ca / 43 + 16 + 6 = **65** lượt; **R** 2 ca / 3 + 4 = **7**; **C2** 2 ca / 8 + 5 = **13**. (c) MỘT dòng tổng kết ra STDERR dạng P2a (`CA`, `LUOT`, `DOT BIEN`, `HONG`, `TU_KIEM`, cột `chỉ_nt` thay `chỉ_posix`); `run` True chỉ khi: `b == c`, `y == z`, `f == g`, `i == 0`, `a == b + w`, `x == y + u + t`, `e == f + h + v`, `x` == sổ, `e == len(_DU_KIEN)`, `h == 0` (không đột biến nào nhắm lượt được phép bỏ qua), mọi tự kiểm đúng hạng; trên nền khác nt: C1 `t = 6`, `v = 2`; R `t = 4`, `v = 2`; C2 `t = 5`, `v = 3`; `u == 0`; trên nt: `t == v == 0`, `u ≤ 2` chỉ ở R. (d) Tự kiểm phân hạng của CHÍNH fragment: `tu_kiem_doi_kieu` (`except` đổi kiểu ⇒ `TIN_DUNG_GIA`, `__context__` là `AttributeError`), `tu_kiem_chu_thich` (⇒ `SONG_SOT`), `tu_kiem_sai_luot` — C1: đột biến dòng 3 khai lượt `p14`; R: dòng 34 khai `truc_tiep`; C2: dòng 39 khai `ngoai_kho` ⇒ `TIN_DUNG_GIA`. (e) stdout của `run` rỗng. | Trên bản sao fragment: thêm ID vào `_DU_KIEN` ⇒ (a) False; lặp một lượt trong bảng ca ⇒ (b) False; gỡ một lượt ⇒ (b) False; ép `bỏ_qua` cho `W5.trong_kho` ⇒ False; (R) ép `bỏ_qua` symlink khi probe thành công ⇒ False; (R) cố định `os.name == "nt"` cho bộ phân loại bỏ qua, probe ném `PermissionError` `winerror == 5` ⇒ lượt `đỏ`, False; bộ phân hạng bỏ so lượt ⇒ `tu_kiem_sai_luot` ra `GIET` ⇒ False; in tổng kết ra stdout ⇒ (e) đỏ. |
| N8 | mỗi phần · gate | Exact head: `--selftest` N/N hai số bằng nhau, N = N_base + số fragment mới của packet, DELTA 0 ca đỏ mới (base/head dựng trong CÙNG một lệnh); `test-fragments-check --json` ⇒ `ok: true`; `bundle_fragment_check.py --json` ⇒ `ok: true`, `failed: []`; mỗi neo trong `_DB` và `_TU_KIEM` của fragment P2a và fragment packet 1 khớp ĐÚNG 1 lần trên nguồn candidate (đếm bằng nạp hai fragment rồi đọc bảng), và hai fragment ấy `run` True trên Linux; `python3 ops/cloud_agent_creds_test.py` `TONG: DAT`, từng ca bằng base; lane worker `release-manifest` tạm + `release-verify --strict` ⇒ `ok: true`, `expected_file_count == checked_file_count`; `ruff check --select F` delta 0 trên `tl_gws.py`, 0 trên fragment và bundled; `git diff --check` rc 0; `doctrine-scan`, `adr-song` rc 0; numstat dưới `set -o pipefail`: đúng 3 dòng, mỗi dòng `^[0-9]+\t[0-9]+\t<đường>$`, tập đường == §1 của phần, tổng cột thêm ≤ trần của dòng khai đầu tệp (450 trừ khi revision khai `nang_tran`). | Neo: candidate chèn thêm một bản của một neo P2a/packet 1 ⇒ đếm 2 ⇒ đỏ (từng fragment một lần). Selftest/bundled/manifest/numstat: như P2a N10–N12 (chuyển fragment mới khỏi `scripts/test_fragments` trên bản sao ⇒ N = N_base; `run` ⇒ `False` ⇒ `N−1/N`; không tái sinh bundled ⇒ `TEST_ID_SET_MISMATCH`; sửa byte sau manifest tạm ⇒ `ok: false`; numstat tay tổng 451 ⇒ đỏ; đường ngoài §1 ⇒ đỏ; cột `-` ⇒ đỏ; base sai ⇒ rc 128). `cloud_agent_creds_test`, `doctrine-scan`, `adr-song`, `ruff`: gate kế thừa, phép đỏ thuộc suite của chính chúng (`ops/cloud_agent_creds_test.py` có `PD*`; `.claude/dev/packet_loop_test.py`); packet không thêm. |
| N9 | mỗi phần · đo native (§4c) | Hồ sơ PR của phần ghi lệnh, exact head/tree, đầu ra thô và kết luận của MỌI phép bắt buộc của phần (§4c cột "bắt buộc"). | Phép bắt buộc thiếu, trái kỳ vọng hoặc `KHÔNG ĐO ĐƯỢC` ⇒ phần ấy không land (§6). |

### 4b. Bảng đột biến — NGUỒN DUY NHẤT

Luật như P2a §4b (lượt gọi, `ngoai_le_la`, mỗi đột biến chỉ chạy ca đích, lượt đích = lượt ĐẦU TIÊN nó làm đỏ). Đột biến neo trên NGUỒN
CANDIDATE. Cột nền `nt` ⇒ đếm `chỉ_nt` trên nền khác. Cột "đo" = mọi lượt đổi màu trên nguyên mẫu §0.3, lượt đầu là đích; "lập luận" = chưa chạy.

| # | phần | đột biến (phép thay) | ca · lượt | nhãn | cơ chế | nền | đo |
|---|---|---|---|---|---|---|---|
| 1 | C1 | `db_nt_bo_nul` (bỏ kiểm (1)) | `phan_loai_nt` · `p11` | `ma` | H | mọi | `p11` |
| 2 | C1 | `db_nt_bo_trang` (bỏ (2)) | · `p12` | `ma` | H | mọi | `p12` |
| 3 | C1 | `db_nt_bo_win32` (bỏ (3)) | · `p13` | `ma` | H | mọi | `p13`–`p15` |
| 4 | C1 | `db_nt_bo_dos` (bỏ (4)) | · `p16` | `ma` | H | mọi | `p16`,`p17` |
| 5 | C1 | `db_nt_bo_nt` (bỏ (5)) | · `p18` | `ma` | H | mọi | `p18` |
| 6 | C1 | `db_nt_o_tran` (`r == ""` ⇒ coi như `\`) | · `p19` | `ma` | H | mọi | `p19` |
| 7 | C1 | `db_nt_o_tuong_doi` (bỏ kiểm phân cách sau ổ) | · `p20` | `ma` | H | mọi | `p20`,`q04` |
| 8 | C1 | `db_nt_o_chi_hoa` (`[A-Z]:`) | · `p03` | `ma` | H | mọi | `p03`,`q02` |
| 9 | C1 | `db_nt_khong_hoa_o` (bỏ `.upper()`) | · `p03` | `goc_tp` | H | mọi | `p03`,`q02` |
| 10 | C1 | `db_nt_goc_o_tuyet_doi` (bỏ `goc_o`) | · `p21` | `ma` | H | mọi | `p21`,`p22` |
| 11 | C1 | `db_nt_unc_share_rong` (regex nhận share rỗng) | · `p23` | `ma` | H | mọi | `p23`,`p24`,`p26` |
| 12 | C1 | `db_nt_chi_gach_nguoc` (tách chỉ theo `\`) | · `p02` | `goc_tp` | H | mọi | `p02`,`p04`,`p06`,`p29`,`q02` |
| 13 | C1 | `db_nt_bo_hai_cham` | · `p28` | `ma` | H | mọi | `p28`–`p30`,`q08` |
| 14 | C1 | `db_nt_bo_ky_tu_cam` | · `p31` | `ma` | H | mọi | `p31`,`p32`,`p41` |
| 15 | C1 | `db_nt_bo_cuoi_cham` | · `p33` | `ma` | H | mọi | `p33`,`p34`,`p40` |
| 16 | C1 | `db_nt_bo_ten_tb` | · `p35` | `ma` | H | mọi | `p35`–`p39` |
| 17 | C1 | `db_nt_ten_tb_khong_cach` (bỏ ` *` trong regex) | · `p38` | `ma` | H | mọi | `p38` |
| 18 | C1 | `db_nt_bo_conin` (bỏ `CONIN$`/`CONOUT$`) | · `p39` | `ma` | H | mọi | `p39` |
| 19 | C1 | `db_nt_unc_bo_kiem_ten` (không áp luật (8) cho máy/share) | · `p40` | `ma` | H | mọi | `p40`,`p41` |
| 20 | C1 | `db_nt_bo_ipc` | · `p42` | `ma` | H | mọi | `p42` |
| 21 | C1 | `db_nt_o_khac_nhan` (`d` khác ⇒ nhận như ổ) | · `p27` | `ma` | H | mọi | `p27` |
| 22 | C1 | `db_nt_cwd_khong_kiem` (cwd sai loại ⇒ ghép chuỗi `ntpath.join(cwd, p)` rồi phân loại lại) | `chuan_nt` · `q04` | `ly_do` | H | mọi | `q04`,`q05` |
| 23 | C1 | `db_nt_goc_rong` | · `q06` | `goc_rong` | H | mọi | `q06`,`q07`,`q13` |
| 24 | C1 | `db_nt_khong_repr` (lý do nội suy `x` thô) | · `q08` | `mot_dong` | H | mọi | lập luận |
| 25 | C1 | `db_nt_bo_kiem_unc` (bỏ chốt `mang` khi `unc` sai) | · `q10` | `unc_dong` | H | mọi | `q10`,`q11` |
| 26 | C1 | `db_nt_unc_mo_som` (mặc định `unc=True`) | · `q11` | `unc_dong` | H | mọi | `q11` |
| 27 | C1 | `db_nt_bo_loai_o` (`o_tuyet_doi` luôn `cuc_bo`) | · `q14` | `unc_dong` | H | mọi | lập luận |
| 28 | C1 | `db_nt_loai_o_moi_loai` (mọi loại ổ khác 4 là `cuc_bo`) | · `q16` | `ly_do` | H | mọi | lập luận |
| 29 | C1 | `db_nt_bo_chot` (nhánh nt về base) | `tich_hop_nt` · `W5.trong_kho` | `ly_do` | H | nt | lập luận |
| 30 | C1 | `db_nt_ghi_duong_tho` (`dest` trả về = `ntpath.join(cfgdir_tho, "credentials.json")`, vẫn kiểm đường chuẩn) | · `W5.tuong_doi` | `ket_qua` | H | nt | lập luận |
| 34 | R | `db_bo_reparse` (bỏ vế thuộc tính M4) | `reparse_gia_lap` · `W5.bit` | `reparse` | H | mọi | lập luận |
| 35 | R | `db_reparse_moi_thu` (mọi thuộc tính khác 0) | · `W5.khong_bit` | `khong_bit` | H | mọi | lập luận |
| 36 | R | `db_bo_reparse_nt` (cùng phép thay với 34) | `lien_ket_nt` · `W5.jn_to_tien` | `lien_ket` | H | nt | chưa đo (D2: junction không `S_ISLNK`) |
| 37 | R | `db_nt_goc_cfg` (`_kiem_dich_ghi(dest, <cfgdir chuẩn>, ("credentials.json",))`) | · `W5.jn_to_tien` | `lien_ket` | H | nt | lập luận (như P2a 33) |
| 38 | C2 | `db_dd_kiem_ca_cuc_bo` (bỏ nhánh `cuc_bo` ⇒ `None`) | `dinh_danh_gia_lap` · `cuc_bo` | `khong_goi` | H | mọi | lập luận |
| 39 | C2 | `db_dd_bo_kiem` (trả `None` sau nhánh `cuc_bo`) | · `trong_kho` | `ket_qua` | H | mọi | lập luận |
| 40 | C2 | `db_dd_bo_so_serial` | · `khac_vol` | `ket_qua` | H | mọi | lập luận |
| 41 | C2 | `db_dd_dung_vol_dau` (dừng sau ổ đầu cùng serial) | · `hai_vol` | `ket_qua` | H | mọi | lập luận |
| 42 | C2 | `db_dd_khong_di_len` (gọi `dinh_danh` trên cha trực tiếp, không đi lên) | · `to_tien` | `to_tien` | E — `FileNotFoundError` chứa `wp433-dd-thieu` | mọi | lập luận |
| 43 | C2 | `db_dd_nuot_quyen` (lỗi ngoài `FileNotFoundError` ⇒ đi lên tiếp) | · `quyen` | `nem` | H | mọi | lập luận |
| 44 | C2 | `db_dd_goc_thieu_cho_qua` (gốc vắng ⇒ `None`) | · `goc_thieu` | `nem` | H | mọi | lập luận |
| 45 | C2 | `db_dd_sai_chi_so` (chỉ số từ `[10]`/`[11]`) | `dinh_danh_that` · `on_dinh` | `on_dinh` | H | nt | lập luận (`[10]` là số liên kết ⇒ T và `T\sub` thường cùng giá trị) |
| 46 | C2 | `db_dd_bo_tien_to` (không bỏ `\\?\`) | · `theo_id` | `theo_id` | H | nt | lập luận |
| 47 | C2 | `db_dd_bo_noi_day` (`_dich_cred_gws_nt` bỏ lời gọi M6) | · `noi_day` | `noi_day` | H | nt | lập luận |

Số 31–33 bỏ trống (dành chỗ). Tổng: **44** đột biến — C1 **30** (1–30: `mọi` 28, `nt` 2), R **4** (34–37: `mọi` 2, `nt` 2), C2 **10**
(38–47: `mọi` 7, `nt` 3). E: 1 (42). Cặp chung (ca, lượt) có chủ ý: 8/9 (`p03`, khác nhãn `ma`/`goc_tp`); 25/26 khác lượt nhờ `q10` truyền
`unc=False` tường minh, `q11` dùng mặc định; 36/37 cùng (`W5.jn_to_tien`, `lien_ket`) là CHỦ Ý không phân biệt được bằng một lượt — 36 bỏ
nhận diện junction, 37 bỏ tổ tiên; lượt `W5.jn_cfg` (junction tại chính `cfgdir`) chỉ đỏ dưới 36 ⇒ đổi đích 36 sang `W5.jn_cfg` nếu D2
xác nhận junction không có `S_ISLNK` (khai ở §8; đột biến 37 giữ đích `W5.jn_to_tien`).

### 4c. Đo native Windows (phiên điều phối chạy trên `DESKTOP-T9R33P2`, dự phòng VM `tra-luat-win`)

Chung: ghim exact head/tree; `chcp 65001` và `set PYTHONIOENCODING=utf-8` trước mọi lệnh; gọi `python` (không giả định `python3`);
PowerShell: `Get-ChildItem -Force`, không đặt biến tên `$Args`; mọi fixture dưới `%TEMP%\wp433c-<giờ>` (kho tạm K = `git init`, thư mục
ngoài kho T), dọn trong `finally`/cuối phiên kể cả khi lỗi; KHÔNG ghi vào kho thật. Gọi `tl_gws` offline: nạp `scripts/tl_gws.py`,
`bind`, thay `_public_curl_bytes`/`_gas` bằng đồ giả như fragment P2a, rồi gọi `_dich_cred_gws`/`_gws_auth_load`. Chạy một fragment:
`python -B -c "import importlib.util, sys; sys.path.insert(0, 'scripts'); import tl; s = importlib.util.spec_from_file_location('frag', '<fragment>'); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); r = m.run(tl); print('run() ->', r); sys.exit(0 if r else 1)"`
(mẫu của `ops/land/pr1415-wp433-provenance/linux/nghiem_thu_1415.py`).

| # | phần | bắt buộc | dựng / lệnh | kỳ vọng | khi không dựng được |
|---|---|---|---|---|---|
| D1 | mọi | không | `python -VV`; `ver`; khoá Developer Mode `reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\AppModelUnlock /v AllowDevelopmentWithoutDevLicense`; `git config --get core.symlinks`; hệ tệp + `GetDriveTypeW` của ổ chứa `%TEMP%` và ổ chứa kho thật | ghi lại | KHÔNG ĐO ĐƯỢC từng mục |
| D2 | R | có (tiền đề) | Trên T: thư mục thường, junction, symlink thư mục, symlink tệp; in `S_ISLNK`, `st_file_attributes & 1024`, `hex(st_reparse_tag)`; rồi gọi `_kiem_dich_ghi` trên từng fixture bằng nguồn candidate và bằng bản sao trong bộ nhớ đã áp đột biến 36 | thường `False, 0` và `None`; junction bit bật, candidate trả `là liên kết tượng trưng`; symlink bit bật. Bit KHÔNG bật cho junction ⇒ DỪNG, revision. Junction `S_ISLNK` True ⇒ ghi lại (đích đột biến 36 giữ `W5.jn_to_tien`) | symlink thiếu quyền (`winerror` 1314) ⇒ vế symlink KHÔNG ĐO ĐƯỢC; junction luôn dựng được |
| D3 | C1 / C2 | C1: vế ổ; C2: vế UNC | `os.lstat` trên `C:\`, ổ chứa T, và (C2) `\\localhost\<share D6>\` cùng `\\localhost\<share D6>` | thành công trên dạng gốc M1 (`X:\`, `\\máy\share\`); dạng gốc M1 thất bại ⇒ revision | vế UNC chưa có share ⇒ KHÔNG ĐO ĐƯỢC ⇒ C2 không land |
| D4 | C1 | vế `cmd` | `os.getcwd()` in BỞI tiến trình Python: chạy từ `cmd` ở T; từ PowerShell sau `Set-Location` vào T; (tuỳ chọn) trên ổ `subst S: <T>` | dạng `X:\…` không tiền tố `\\?\`; khác ⇒ revision | vế PowerShell/subst KHÔNG ĐO ĐƯỢC không chặn |
| D5 | mỗi phần | có | Chạy `run(tl)` của fragment của phần, fragment P2a, fragment packet 1 (lệnh mẫu ở trên), mỗi cái riêng; ghi dòng tổng kết stderr | mỗi `run()` True; fragment của phần: `chỉ_nt = 0`, `bỏ_qua` chỉ trong danh sách cho phép; fragment P2a: `(w, t, v) == (7, 27, 21)` (`chỉ_posix` của nó); packet 1: theo luật bỏ qua của chính nó | không có |
| D6 | C2 | có (tiền đề) | Shell ADMIN (chủ kho): `net share tl433sub=<K>\sub /grant:%USERNAME%,FULL` và `net share tl433out=<T> /grant:%USERNAME%,FULL`. Shell THƯỜNG (tài khoản chạy thật): `be.dinh_danh` của `<K>\sub` qua `<K>\sub` và qua `\\localhost\tl433sub`; `be.o_cuc_bo()`; `be.theo_dinh_danh(<gốc ổ của K>, s, i)` với `(s, i)` đo qua share | serial và chỉ số qua share == qua đường cục bộ; ổ của K có trong `o_cuc_bo` với cùng serial; `theo_dinh_danh` trả `<K>\sub` (normcase). Khác ⇒ M6 không đứng ⇒ DỪNG, revision | không có admin ⇒ KHÔNG ĐO ĐƯỢC ⇒ C2 không land |
| D7 | C2 | có | Dùng share D6. `_dich_cred_gws` với `cfgdir`: `\\localhost\tl433sub\gws` ⇒ `nằm trong kho git`; `\\localhost\tl433out\gws` ⇒ `None` rồi `_ghi_nguyen_tu_0600` ghi được, tệp đúng byte; `net use Z: \\localhost\tl433sub` rồi `Z:\gws` ⇒ `nằm trong kho git`; `subst S: <K>\sub` rồi `S:\gws` ⇒ `nằm trong kho git`. Vế âm: lặp hai ca "trong kho" với bản sao áp đột biến 47 ⇒ KHÔNG còn `nằm trong kho git`. Dọn: `net share … /delete`, `net use Z: /delete`, `subst S: /d` | như cột lệnh | thiếu admin ⇒ KHÔNG ĐO ĐƯỢC ⇒ C2 không land |
| D8 | C1 | không | `dir /x` lấy tên 8.3 của K; `_dich_cred_gws(<tên ngắn K>\gws)` | `nằm trong kho git` | 8.3 tắt ⇒ KHÔNG ĐO ĐƯỢC |
| D9 | C1 | có | `_dich_cred_gws` rồi writer với `cfgdir` = `<T>\Quốc hội\gws` và `<K>\Quốc hội\gws` | T: ghi được, tệp đúng; K: `nằm trong kho git`, không tệp | không có |
| D10 | C1 | có | (chỉ khi C1 land trước C2) `_dich_cred_gws` với `\\localhost\<bất kỳ>\x` và với ổ `Z:` ánh xạ bằng `net use` (dùng share D6 nếu có) | `đường không hợp lệ`, không truy cập/ghi gì | vế ổ ánh xạ thiếu admin ⇒ KHÔNG ĐO ĐƯỢC ⇒ C1 không land (§9 Q9) |

## 5. `pham_vi_e`

Không chạm E4, E5: chỉ sửa mã đường ghi; ca fragment dùng giá trị giả, HOME/cfgdir tạm, đồ giả thay tải Drive; không LIVE, không đẩy
Package. D6/D7/D10 tạo/xoá share, ổ ánh xạ và `subst` TẠM trên máy chủ kho bằng shell admin của chủ kho — thao tác cục bộ, không chạm dữ
liệu kho hay credential thật.

## 6. `luat_dung`

- Trần lời gọi Codex theo dòng khai `ADR-0055`; chạm trần ⇒ Review Rescue Checkpoint; xin tăng mang **E2**.
- Trần kích thước theo dòng khai `ADR-0053` (≤ 6 tệp, ≤ 450 dòng thêm), đo bằng numstat thật (N8) TRƯỚC khi công bố; vượt ⇒ DỪNG, không
  push, không cắt ca. Tách hay nâng trần là quyết định của chủ kho — **E2** (§9 Q1); nâng thì revision mới khai `nang_tran` theo `ADR-0053`.
- `_kiem_dich_ghi`, `_ghi_nguyen_tu_0600`, `_trong_kho_git`, `_dich_cred_gws` trên base thật khác §0.1, hoặc cần sửa thân ngoài M3/M4 ⇒ dừng, revision.
- Một neo §0.4 không còn khớp đúng 1 lần ⇒ dừng, revision.
- Phép native bắt buộc (§4c) của một phần thiếu, trái kỳ vọng hoặc `KHÔNG ĐO ĐƯỢC` ⇒ phần ấy không land; D2 hoặc D6 trái kỳ vọng ⇒
  revision. Thiếu máy hay quyền admin để đo ⇒ hỏi chủ kho — **E2**, mang theo danh sách phép thiếu và lý do (§9 Q9).
- Chưa có comment cấp ngoại lệ bundled cho đúng `packet_id` trên #433 ⇒ không cấp lease (**E2**, §9 Q8).
- Đặc tả không thuộc Mission ⇒ chờ chủ kho duyệt băm theo `ADR-0067` — **E2**.

## 7. `hinh_dang_ke_thua`

Bộ đếm có chứng cứ kế thừa từ P2a §7 / packet 1: **mức đặc tả 3, mức mã 0** cho hình dạng "chốt nhìn THIẾU một phần của đường" (S5, L1,
tổ tiên `cfgdir`); số đếm của tiền nhiệm xa hơn KHÔNG ĐO ĐƯỢC. P2c đáp hai lớp mới cùng hình dạng: (i) lớp TÊN — `ntpath` có nhiều cách viết
một đường ⇒ danh sách cho phép trên mã phân loại, mỗi nhánh một đột biến; (ii) lớp TRẦN của share/ổ mạng ⇒ C2 quy về đường cục bộ bằng
định danh. Riêng P2c (khác bộ đếm kế thừa): review lượt 1 bắt thêm ba lớp cùng hình dạng — máy/share không qua luật thành phần, ổ mạng
mang mã ổ cục bộ, tập gốc kho rỗng làm C2 mù (bản 1) — đã đóng ở bản này; đếm mức đặc tả P2c: 1 lượt có finding cùng hình dạng.

## 8. `chua_do_duoc`

- Mọi hành vi native Windows (§4c). Cụ thể: junction có `S_ISLNK` hay không; `os.lstat` với tag không phải name-surrogate; `lstat` trên gốc
  UNC; định danh qua SMB loopback có bằng định danh cục bộ (D6, tiền đề C2); `GetDriveTypeW` cho ổ `subst` và ổ `net use`; `IPC$` là share
  không phải hệ tệp duy nhất cần chặn bằng tên (share máy in, `ADMIN$` chưa xét); volume không có ký tự ổ (C2 không duyệt); hai volume cục
  bộ trùng serial 32 bit có cùng chỉ số tệp (M6 kiểm mọi ổ trùng serial, nhưng không phân biệt được đối tượng nếu cả serial và chỉ số trùng).
- Nguyên mẫu chỉ phủ M1 và phần M2 không có loại ổ, `repr`, mã công khai; đột biến 24, 27–47 là lập luận.
- TOCTOU (§2).
- Kích thước (ước lượng tĩnh, chưa đo; mốc P2a: 11 ca/46 lượt/37 đột biến ⇒ fragment +389, `tl_gws.py` +48):

  | phần | `tl_gws.py` (hạng mục) | fragment (hạng mục) | bundled | tổng |
  |---|---|---|---|---|
  | C1 | M1 28–34, M2 14–18, `_loai_o_nt` 5–7, M3 6–8 ⇒ **53–67** | khung + tự kiểm + đếm `chỉ_nt` 110–125; rig W4/W5 nt 60–75; N1 43 lượt + N2 16 lượt dạng dữ liệu 60–72; N4 6 lượt 20–28; `_DB` 30 mục 33–38 ⇒ **283–338** | 1 | **337–406** |
  | R | M4 +3, docstring 1–2 ⇒ **4–5** | khung 95–105; rig W5 + bọc `lstat` + dựng junction/symlink + probe 50–62; N3/N4r 7 lượt 30–40; `_DB` 4 mục 5–6 ⇒ **180–213** | 1 | **185–219** |
  | C2 | bindings 22–28, `dinh_danh` 9–11, `o_cuc_bo` 8–10, `theo_dinh_danh` 16–20, M6 12–15, nối dây 2–3 ⇒ **69–87** | khung 105–115; `be` giả giữ trạng thái 35–45; N5/N6 13 lượt 45–60; `_DB` 10 mục 11–13 ⇒ **196–233** | 1 | **266–321** |

  Gộp C1+R ⇒ 522–625 > 450. Trọn P2c ⇒ 788–946. Ba packet riêng: mỗi phần dưới 450, biên trên C1 còn 44 dòng.

## 9. Câu hỏi cho chủ kho (mỗi câu **E2**: quyền quyết thuộc chủ kho; phiên soạn dừng ở đây sau review)

- **Q1 — Kích thước.** (A) Ba packet C1 → R → C2, mỗi phần trần 450 (khuyến nghị: mỗi phần đều dưới trần; R nhỏ và tự đứng). (B) Hai
  packet C1+R rồi C2 — cần nâng trần C1+R lên ~650. (C) Một packet, nâng trần ~950.
- **Q2 — Cơ chế định danh cho đích qua mạng.** Văn bản 19-11 đọc theo chữ (A: định danh từng tổ tiên của đích so với gốc kho) KHÔNG bắt
  được share có gốc là thư mục con của kho — chuỗi tổ tiên dừng ở gốc share, không chạm gốc kho (finding P1 lượt 1 của P2a). (B, bản 1 của
  đặc tả này) quy về đường cục bộ qua volume của gốc kho tra-luat: mù khi không xác định được gốc kho (chạy từ gói giải nén, cwd ngoài kho
  — finding P1 lượt 1 của P2c). (B', đặc tả này) quy về đường cục bộ qua MỌI ổ cục bộ cùng serial rồi `_trong_kho_git` ⇒ không cần biết gốc
  kho, nhưng bảo vệ MỌI kho git trên máy, rộng hơn quyết định "thu hẹp" 19-11. Khuyến nghị **B'**.
- **Q4 — Cùng serial mà `OpenFileById` không tìm thấy** ⇒ xét ổ kế, hết ổ ⇒ coi là ngoài kho (đặc tả này). Lỗi Win32 khác, quyền, gốc
  share vắng ⇒ fail-closed `ghi lỗi`. Khuyến nghị giữ.
- **Q5 — Đích qua mạng trong khoảng giữa C1 và C2.** Base hiện nhận mọi dạng không kiểm. Khuyến nghị C1 TỪ CHỐI UNC và ổ mạng
  (`đường không hợp lệ`) tới khi C2 land.
- **Q6 — Mở rộng ngoài danh sách 19-11.** Đặc tả thêm: ký tự cấm (chặn ADS), chấm/khoảng trắng cuối, tên thiết bị DOS (kể cả `CONIN$`,
  `NUL .txt`), cùng luật ấy cho máy/share, share `IPC$`, `o_khac` (`1:`), loại ổ (chỉ REMOVABLE/FIXED là cục bộ; REMOTE là mạng; CDROM,
  RAMDISK, không rõ ⇒ từ chối), từ chối gốc trần `C:\`, `\\máy\share`. Khuyến nghị giữ cả.
- **Q7 — Reparse point.** R từ chối mọi entry mà `os.lstat` báo bit 1024; tag không phải name-surrogate có thể không được báo (chưa đo).
  Khuyến nghị giữ phạm vi "những gì `lstat` báo" và đo D2; không mở rộng bằng API khác trong P2c.
- **Q8 — Ngoại lệ bundled** cho đúng `packet_id` từng phần — comment mới trên #433 sau khi duyệt băm; chặn lease, không chặn review.
- **Q9 — Phép đo cần admin.** D6, D7, D10 (vế ổ ánh xạ) cần chủ kho mở shell ADMIN trên Desktop (hoặc VM) để `net share`/`net use`.
  Không có ⇒ C1 và C2 không land (§6).
- (Q3 của bản 1 — "gốc kho tra-luat là gì" — không còn cần nếu Q2 chọn B'.)

## 10. Nhật ký revision

- 2026-11-19T10:08Z–10:16Z (phiên con của điều phối, soạn bản 1): đo §0 trên `11bd033`; nguyên mẫu M1/M2. Bản lượt 1: sha256
  `96893bdf…` (`rv/dac-ta-ban1.md`).
- 2026-11-19T10:23Z (sau review Codex lượt 1: request_changes, 0 P0, 4 P1, 5 P2, 1 P3): máy/share qua luật thành phần, `IPC$`, tên DOS
  mở rộng; loại ổ (ổ mạng đóng như UNC); C2 đổi sang B' (mọi ổ cục bộ), ABI `OpenFileById`/`GetFinalPathNameByHandleW`, đọc lại định danh,
  đi lên chỉ trên `FileNotFoundError`; tách R khỏi C1; sổ lượt/đẳng thức theo từng fragment, `h == 0`; tự kiểm sai lượt dùng đột biến
  của chính fragment; `q11` đo mặc định `unc`; đột biến cho `nul`, `trang`; nguyên mẫu r2 và bộ chạy kiểm lượt đích (25/25); §4c cột bắt
  buộc, lệnh chạy fragment, D9 không ghi kho thật, vế âm D7; §7 bộ đếm kế thừa; §8 bảng kích thước một nguồn.
