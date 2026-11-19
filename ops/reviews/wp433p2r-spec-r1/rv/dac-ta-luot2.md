tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# GWS-CRED-DICH-NGOAI-KHO-R r1 — `_kiem_dich_ghi` coi reparse point (junction, mount point, symlink) là liên kết, cho mọi chỗ ghi credential gọi nó

- packet_id: GWS-CRED-DICH-NGOAI-KHO-R; revision: 1;

| trường | giá trị |
|---|---|
| `packet_issue` | #433 |
| `nguon_cap_viec` | Issue #433; P2a `GWS-CRED-DICH-NGOAI-KHO-A-r1.md` (sha256 `b0065947…`) §2 "Để P2c" mục (3) ("vế reparse point — M6 cũ: `st_file_attributes & FILE_ATTRIBUTE_REPARSE_POINT` trong `_kiem_dich_ghi`, N3c giả lập, N4 junction native — đi cùng P2c", chủ kho Q4 19-11). Tách từ đặc tả gộp `GWS-CRED-DICH-NGOAI-KHO-C-r1.md` bản 4 (sha256 `b477d23e…`) theo quyết định chủ kho 2026-11-19 ~10:50Z (phiên điều phối #1206): Q1 hai packet riêng, land C1 → R; Q7 R chỉ cam kết các entry mà `os.lstat` báo bit 1024. |
| `phu_thuoc` | **C1 `GWS-CRED-DICH-NGOAI-KHO-C1` phải ĐÃ LAND** (các lượt native của R đi qua nhánh nt `_dich_cred_gws_nt` của C1). Không cấp lease cho R trước khi C1 merge vào nhánh mặc định. Gọi lại hợp đồng lỗi sáu cụm của P2a. |
| `review_class` | `sensitive` (`scripts/tl_gws.py` là đường ghi credential). Đối chiếu `lease_publish check` khi cấp lease. |
| `base` | Commit land của C1 (chưa có lúc soạn). §0 dưới đây đo `_kiem_dich_ghi` trên `96b6a33d770f7539a3eacbebdc215f87ded4ea7f` (blob `tl_gws.py` `9ec027c2…`); C1 không sửa thân hàm ấy, nên phiên thi hành đo lại §0 trên base thật và DỪNG nếu thân lệch. |

## 0. Hiện trạng (đo trên `96b6a33`, Linux, CPython 3.11.18 / 3.12.3 / 3.13.18)

- `_kiem_dich_ghi(dich, goc, thanh_phan)` ở `scripts/tl_gws.py:1173–1187`: luật (a) `_trong_kho_git(dirname(dich))`; luật (b) với
  `i` trong `range(len(thanh_phan) + 1)`, `tien_to = os.path.join(goc, *thanh_phan[:i])`, `if stat.S_ISLNK(os.lstat(tien_to).st_mode):`
  (1183) ⇒ `là liên kết tượng trưng: <repr(tien_to)[:200]>`; `FileNotFoundError`/`NotADirectoryError` bỏ qua. Docstring 1175–1176 tự khai
  "junction/reparse Windows chưa chặn".
- Người gọi: W4/W5 qua `_dich_cred_gws` (POSIX 1210; nhánh nt do C1 viết), W1–W3 qua `_dich_jar_nlm` (1233), W6 (1784). R áp cho cả bốn,
  trên đúng các tiền tố mỗi người gọi truyền.
- `stat.FILE_ATTRIBUTE_REPARSE_POINT` = 1024 có trên Linux cả ba bản (đo 2026-11-19T10:08:01Z); `os.stat_result` trên Linux không có
  `st_file_attributes` ⇒ `getattr(st, "st_file_attributes", 0)` = 0 ⇒ R không đổi hành vi POSIX.
- Neo phải giữ: dòng `for i in range(len(thanh_phan) + 1):` (neo của fragment packet 1, P2a), `{repr(kho_dich)[:200]}` (P2a). Dòng 1183
  không phải neo của fragment nào trên base; neo của fragment C1 đo lại khi cấp lease. Mọi neo `_DB`/`_TU_KIEM` của fragment P2a, packet 1
  và C1: số lần khớp trên candidate BẰNG trên base (packet 1 `tu_kiem_neo_lap` = 2).
- Hành vi CPython trên Windows (chưa đo, §4c D2): `os.lstat` mở name-surrogate reparse point (symlink, junction, mount point) mà không đi
  xuyên và đặt `st_file_attributes`; với tag không phải name-surrogate (placeholder đám mây, dedup) có thể đi xuyên — R không cam kết các tag ấy.

## 1. `write_set`

```
scripts/tl_gws.py
scripts/test_fragments/wp433_gws_cred_win_reparse.py
scripts/tl_test_fragments_bundled.py
```

KHÔNG `RELEASE_MANIFEST.json`. Bundled theo tiền lệ phương án B (chủ kho 18-11-2026; P2a §1): chỉ sinh bằng
`generate_bundled_module_bytes(scripts/test_fragments)`. **Điều kiện trước khi cấp lease (E2):** comment của chủ kho trên #433 cấp ngoại lệ
ấy nêu đúng `packet_id` `GWS-CRED-DICH-NGOAI-KHO-R`, đúng một tệp `scripts/tl_test_fragments_bundled.py` và sha256 của đặc tả này đã đóng
băng; lease trỏ URL comment. Phiên land tái sinh `RELEASE_MANIFEST.json` trong commit land.

## 2. `ngoai_pham_vi`

- Mọi thứ của C1 (danh sách cho phép đường, loại ổ, từ chối UNC/ổ mạng).
- Mở rộng chuỗi tiền tố của W1–W3/W6 lên trên `goc` mà họ truyền: không.
- Reparse tag không phải name-surrogate mà `os.lstat` không báo bit: không cam kết (chủ kho Q7); không dùng API khác (`FindFirstFileW`,
  `st_reparse_tag`) để bắt chúng.
- TOCTOU: như P2a §2.
- Không sửa `ops/**`, `.github/**`, `scripts/tl_selftest.py`, fragment P2a, packet 1, C1, `RELEASE_MANIFEST.json`, `changelog.d/*`,
  `VERSION`, `CHANGELOG.md`, `SKILL.md`.

## 3. `muc_tieu`

| # | mục tiêu | tệp |
|---|---|---|
| M1 | Thân `_kiem_dich_ghi`: thay ĐÚNG dòng nhận diện 1183 bằng `st = os.lstat(tien_to)` và điều kiện `stat.S_ISLNK(st.st_mode) or getattr(st, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT`; cụm giữ `là liên kết tượng trưng`, chi tiết `repr(tien_to)[:200]`; dòng vòng, chữ ký, thứ tự luật, nhánh `FileNotFoundError`/`NotADirectoryError` giữ nguyên; docstring bỏ câu "junction/reparse Windows chưa chặn" và nêu vế mới. Không sửa gì khác trong `tl_gws.py`. | `scripts/tl_gws.py` |
| M2 | Fragment `wp433_gws_cred_win_reparse.py`, `TEST_ID = "wp433_gws_cred_win_reparse"`: khuôn fragment P2a, tự chứa, nạp `tl_gws` vào bộ nhớ, đột biến trên bản sao, neo khớp đúng 1 lần, phân hạng `TinHieuChotCa(AssertionError)` theo (loại tín hiệu, ca, lượt, nhãn), sổ `_LUOT_DU_KIEN` và `_DU_KIEN` viết riêng, trạng thái lượt `đạt`·`đỏ`·`bỏ_qua`·`chỉ_nt`, mọi đầu ra ra STDERR, khôi phục (kể cả `os.lstat` đã bọc) trong `finally`. | fragment |
| M3 | Tái sinh bundled bằng `generate_bundled_module_bytes(scripts/test_fragments)`; không sửa tay. | bundled |

## 4. `nghiem_thu`

Ký hiệu như P2a §4. "W5 đúng" = `(False, s)`, `s` `fullmatch` `<cụm>: .+`, một dòng.

| # | ca (nền) | lượt và tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|---|
| N1 | `reparse_gia_lap` (mọi) — bọc `os.lstat` trong cửa sổ gọi: với ĐÚNG một đường của lượt (so sau `normcase(normpath)`) trả `SimpleNamespace(st_mode=stat.S_IFDIR \| 0o700, st_file_attributes=<a>)`, đường khác đi hàm thật; T thật ngoài kho | Theo thứ tự: `W5.bit` (`cfgdir = <T>\cfg` tồn tại, `a = 1024` cho `cfgdir`) ⇒ [`reparse`] W5 đúng `là liên kết tượng trưng`, chi tiết `repr(<cfgdir dạng người gọi truyền>)`, writer 0; `truc_tiep` — gọi thẳng `_kiem_dich_ghi(<T>/x/credentials.json, <T>, ("x", "credentials.json"))`, `a = 1024` cho `<T>/x` ⇒ [`reparse_truc_tiep`] lý do như trên (hình dạng lời gọi của W1–W3); `W5.khong_bit` (`a = 16`, FILE_ATTRIBUTE_DIRECTORY) ⇒ [`khong_bit`] `(True, d)`, tệp đúng byte. Trên POSIX W5 đi nhánh P2a, trên nt đi nhánh C1 — cùng một `_kiem_dich_ghi`. Vế âm base: trên base `W5.bit` cho `(True, …)`. | §4b dòng 1–2. |
| N2 | `lien_ket_nt` (nt) — junction bằng `_winapi.CreateJunction` (thiếu thì `cmd /c mklink /J` ngoài cửa sổ chặn), symlink bằng `os.symlink`; mọi fixture dưới T (ngoài kho); bộ đếm writer | Theo thứ tự: `W5.jn_cfg` `cfgdir` là junction → `<T>\that` ⇒ [`lien_ket`] chi tiết `repr(cfgdir)`, `that` không tệp mới, writer 0; `W5.jn_to_tien` `<T>\jn\a\b` (`jn` junction → `<T>\that2`) ⇒ [`lien_ket`] chi tiết `repr(<T>\jn)`; `W5.sl_dir` `cfgdir` là symlink thư mục ⇒ [`lien_ket`]; `W5.sl_tep` `credentials.json` là symlink tệp tới `<T>\dich.json` (`CU`) ⇒ [`lien_ket`], `dich.json` còn `CU`. Dựng junction thất bại ⇒ lượt `đỏ` (không bỏ qua). Danh sách cho phép `bỏ_qua`: ĐÚNG `W5.sl_dir`, `W5.sl_tep`, chỉ khi `os.symlink` trên CHÍNH thư mục fixture ném `OSError` có `winerror == 1314`; lỗi khác ⇒ `đỏ` với `probe symlink: <repr(lớp, errno, winerror)>`. Vế âm base: junction KHÔNG bị chặn (C1 §2) ⇒ `W5.jn_cfg` cho `(True, …)` nếu D2 xác nhận junction không có `S_ISLNK`. | §4b dòng 3. `W5.jn_to_tien`: phép đỏ là phản chứng bộ đo `pc_chi_kiem_cfgdir` (N3). `W5.sl_dir`, `W5.sl_tep`: hồi quy cho vế `S_ISLNK` sẵn có, KHÔNG có phép đỏ riêng — khai, không tính đột biến. |
| N3 | tự kiểm | (a) `_DU_KIEN` == tập ID `_DB` (đếm cả số lần); mỗi mục giết đúng (loại tín hiệu, ca, lượt, nhãn). (b) `_LUOT_DU_KIEN` viết riêng; tập và số lần (ca, lượt) đã ghi trạng thái BẰNG sổ: 2 ca / 3 + 4 = **7** lượt. (c) MỘT dòng tổng kết ra STDERR dạng P2a (cột `chỉ_nt`); `run` True chỉ khi các đẳng thức chung của P2a N9(c) (`b == c`, `y == z`, `f == g`, `i == 0`, `a == b + w`, `x == y + u + t`, `e == f + h + v`; `chỉ_posix` đổi thành `chỉ_nt`) cùng `x == 7`, `e == len(_DU_KIEN)`, `h == 0` (không đột biến nào nhắm hai lượt symlink) và `0 ≤ u ≤ 2`; trên nền khác nt: `(w, t, v, u) == (1, 4, 1, 0)`; trên nt: `w == t == v == 0`, mỗi lượt `bỏ_qua` phải mang lỗi `winerror == 1314` của CHÍNH fixture lượt ấy. (d) Tự kiểm phân hạng: `tu_kiem_doi_kieu` (⇒ `TIN_DUNG_GIA`, `__context__` là `AttributeError`), `tu_kiem_chu_thich` (⇒ `SONG_SOT`), `tu_kiem_sai_luot` (CHÍNH đột biến 1, chỉ khai lượt `truc_tiep` ⇒ `TIN_DUNG_GIA`). (e) stdout của `run` rỗng. | Trên bản sao fragment: thêm ID vào `_DU_KIEN` ⇒ (a) False; lặp/gỡ một lượt ⇒ (b) False; ép `bỏ_qua` lượt ngoài danh sách ⇒ False; ép `bỏ_qua` symlink khi probe thành công ⇒ False; cố định `os.name == "nt"` cho bộ phân loại bỏ qua, probe ném `PermissionError` `winerror == 5` ⇒ lượt `đỏ`, False; bộ phân hạng bỏ so lượt ⇒ `tu_kiem_sai_luot` ra `GIET` ⇒ False; bộ bọc `lstat` không khôi phục ⇒ phép kiểm sau `run` thấy `os.lstat` khác hàm gốc ⇒ False; in tổng kết ra stdout ⇒ đỏ. Đối chứng XANH bắt buộc (trên bản sao, cố định `os.name == "nt"` cho bộ đếm): một lượt symlink bỏ qua hợp lệ (`u = 1`) và cả hai (`u = 2`) ⇒ `run` vẫn True với `h == 0`. Phản chứng BỘ ĐO `pc_chi_kiem_cfgdir` (nt; không phải mục `_DB`, không vào tổng): bản sao RAM sửa lời gọi `_kiem_dich_ghi` của nhánh nt C1 thành chỉ kiểm từ `cfgdir` ⇒ `W5.jn_cfg` vẫn đạt và `W5.jn_to_tien` đỏ ở `lien_ket` — chứng minh lượt tổ tiên đo được chuỗi tiền tố do W5/C1 truyền. |
| N4 | gate | Exact head: `--selftest` N/N hai số bằng nhau, N = N_base + 1, DELTA 0 ca đỏ mới; `test-fragments-check --json` ⇒ `ok: true`; `bundle_fragment_check.py --json` ⇒ `ok: true`, `failed: []`; mọi neo `_DB`/`_TU_KIEM` của fragment P2a, packet 1, C1: số lần trên candidate BẰNG trên base; ba fragment ấy `run` True trên Linux (packet 1 và P2a có ca symlink chạy THẬT trên POSIX, nên vế `S_ISLNK` còn sống được đo lại); `python3 ops/cloud_agent_creds_test.py` `TONG: DAT`, từng ca bằng base; lane worker `release-manifest` tạm + `release-verify --strict` ⇒ `ok: true`, `expected == checked`; `ruff check --select F` delta 0; `git diff --check` rc 0; `doctrine-scan`, `adr-song` rc 0; numstat dưới `set -o pipefail`: đúng 3 dòng, `^[0-9]+\t[0-9]+\t<đường>$`, tập đường == §1, tổng thêm ≤ 450. Gate T3 theo protocol §10.1: full selftest + release gates trên CẢ Windows (D12) và Linux cho cùng frozen integration SHA. | Như C1 N5: chèn thêm bản một neo ⇒ đỏ; xoá một bản `tu_kiem_neo_lap` ⇒ đỏ; numstat tay 451 / đường lạ / thiếu đường / cột `-` / base sai ⇒ đỏ; selftest/bundled/manifest như P2a N10–N11. Gate kế thừa: phép đỏ thuộc suite của chúng. |
| N5 | đo native (§4c) | Hồ sơ PR ghi lệnh, shell, exact head/tree, đầu ra thô, rc và kết luận của MỌI phép bắt buộc ở §4c. | Phép bắt buộc thiếu, trái kỳ vọng hoặc `KHÔNG ĐO ĐƯỢC` ⇒ không land. |

### 4b. Bảng đột biến — NGUỒN DUY NHẤT

Luật như P2a §4b. Neo trên NGUỒN CANDIDATE. Nền `nt` ⇒ `chỉ_nt` trên nền khác.

| # | đột biến (phép thay) | ca · lượt | nhãn | cơ chế | nền | đo |
|---|---|---|---|---|---|---|
| 1 | `db_bo_reparse` (điều kiện về `stat.S_ISLNK(st.st_mode)`) | `reparse_gia_lap` · `W5.bit` | `reparse` | H | mọi | lập luận (giả lập: `S_IFDIR` ⇒ `S_ISLNK` sai) |
| 2 | `db_reparse_moi_thu` (vế thuộc tính thành `getattr(st, "st_file_attributes", 0) != 0`) | · `W5.khong_bit` | `khong_bit` | H | mọi | lập luận (16 ≠ 0) |
| 3 | `db_bo_reparse_nt` (cùng phép thay với 1) | `lien_ket_nt` · `W5.jn_cfg` | `lien_ket` | H | nt | chưa đo (D2: đòi junction có `S_ISLNK` sai, bit 1024 bật) |

Tổng: **3** đột biến (`mọi` 2, `nt` 1), E: 0. 1 và 3 cùng phép thay, khác ca (giả lập / native). Nếu D2 cho junction `S_ISLNK` đúng, đột
biến 3 sống trên nt ⇒ `KHÔNG ĐO ĐƯỢC`, chặn land, revision (§6) — vế mới khi ấy không cần cho junction và giá trị của R phải được xét lại.

### 4c. Đo native Windows (`DESKTOP-T9R33P2`, dự phòng VM `tra-luat-win`)

Chung như C1 §4c: ghim exact head/tree; `cmd.exe` với `chcp 65001` và `set PYTHONIOENCODING=utf-8`; lệnh **[ADMIN]** chạy nguyên văn trong
PowerShell Run as Administrator do chủ kho thao tác; `python` (không `python3`); rig dựng `%TEMP%\wp433r-<giờ>` (K kho tạm, T ngoài kho),
dọn đúng thứ mình tạo trong `finally`; không ghi kho thật; gọi `tl_gws` offline với bộ đếm writer.

| # | bắt buộc | admin | dựng / lệnh | kỳ vọng | khi không dựng được |
|---|---|---|---|---|---|
| D1 | không | không | `ver`; khoá Developer Mode; `git config --get core.symlinks`; hệ tệp của ổ T | ghi lại | KHÔNG ĐO ĐƯỢC |
| D2 | có (tiền đề) | không | Trên T: thư mục thường; junction bằng `cmd /c mklink /J <T>\jn <T>\that` (ghi rc, khác 0 ⇒ KHÔNG ĐO ĐƯỢC); symlink thư mục và symlink tệp bằng `os.symlink` trong Python tại đúng T (chỉ `OSError` có `winerror == 1314` cho phép ghi KHÔNG ĐO ĐƯỢC ở vế ấy; lỗi dựng khác ⇒ D2 đỏ); in `stat.S_ISLNK(st.st_mode)`, `st.st_file_attributes & 1024`, `hex(st.st_reparse_tag)`; gọi `_kiem_dich_ghi(<fixture>\credentials.json, <T>, (<tên fixture>, "credentials.json"))` bằng nguồn candidate và bằng bản sao áp đột biến 1 | thường: `False, 0`, `None`; junction: `S_ISLNK` sai, bit bật, candidate `là liên kết tượng trưng`, bản đột biến `None`; symlink: bit bật, cả hai bản đều chặn (vế `S_ISLNK`). Trái ⇒ DỪNG, revision | junction không dựng được ⇒ KHÔNG ĐO ĐƯỢC ⇒ không land; symlink `winerror` 1314 ⇒ vế symlink KHÔNG ĐO ĐƯỢC, không chặn |
| D3 | không | **có** | Mount point. Trước khi gắn: `<T>\mp` là thư mục thường rỗng, `_kiem_dich_ghi(<T>\mp\x\credentials.json, <T>, ("mp", "x", "credentials.json"))` ⇒ `None`. **[ADMIN]** PowerShell nguyên văn: `mountvol` (liệt kê, chọn tên `\\?\Volume{…}\` của một ổ CÓ SẴN), rồi `mountvol "<T>\mp" "<tên volume>"` và `$LASTEXITCODE`. Shell thường: xác nhận gắn đúng (`mountvol "<T>\mp" /L` trả đúng tên volume), in `S_ISLNK`, bit 1024, `hex(st_reparse_tag)` của `<T>\mp`; gọi lại `_kiem_dich_ghi` bằng nguồn candidate và bằng bản sao áp đột biến 1 | candidate: `là liên kết tượng trưng` với chi tiết `repr(<T>\mp)`; bản đột biến: `None` (vế bit là vế chặn). Dọn **[ADMIN]** `mountvol "<T>\mp" /D` | thiếu admin, hoặc không xác nhận được điểm gắn ⇒ KHÔNG ĐO ĐƯỢC kèm lý do, không chặn |
| D4 | có | không | Người gọi khác W5: `_kiem_dich_ghi` theo hình dạng W1 (`nbase` = `<T>\nb` có junction `<T>\nb\profiles` → `<T>\x`, thành phần `("profiles", "default", "cookies.json")`) | `là liên kết tượng trưng` với chi tiết `repr(<T>\nb\profiles)` | không có |
| D5 | có | không | `run(tl)` của fragment R, C1, P2a, packet 1, mỗi cái một tiến trình (lệnh mẫu ở C1 §4c) | mỗi `run()` True; R: `chỉ_nt = 0`, `bỏ_qua` chỉ hai lượt symlink khi thiếu quyền | không có |
| D12 | có (T3) | không | Trên frozen integration SHA: `python scripts/tl.py --selftest` và `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` trên Windows; cùng hai lệnh trên Linux | cả hai nền xanh, cùng SHA | thiếu Windows ⇒ T3 chưa đạt ⇒ không land |

## 5. `pham_vi_e`

Không chạm E4, E5: một biểu thức trong đường ghi; ca dùng giá trị giả, thư mục tạm, đồ giả thay tải Drive; không LIVE, không đẩy Package.
D3 (tuỳ chọn) gắn/gỡ một mount point TẠM bằng shell admin của chủ kho.

## 6. `luat_dung`

- Trần lời gọi Codex theo dòng khai `ADR-0055`; chạm trần ⇒ Review Rescue Checkpoint; xin tăng mang **E2**.
- Trần kích thước `ADR-0053` (≤ 6 tệp, ≤ 450 dòng thêm) đo bằng numstat thật TRƯỚC khi công bố; vượt ⇒ DỪNG; nâng trần là quyết định chủ kho — **E2**.
- Trước khi đóng băng và trước mỗi bước công bố: chạy lại ba phép đo mục *Hiệu lực* của `ADR-0053`, `ADR-0055` cho hai OID ở dòng khai.
- C1 chưa land ⇒ không cấp lease. Thân `_kiem_dich_ghi` trên base thật khác §0, hoặc cần sửa ngoài M1 ⇒ dừng, revision.
- Một neo lệch số lần so với base ⇒ dừng, revision.
- D2 trái kỳ vọng ⇒ dừng, revision; phép native bắt buộc thiếu hoặc `KHÔNG ĐO ĐƯỢC` ⇒ không land; thiếu máy ⇒ hỏi chủ kho — **E2**, mang theo
  số lời gọi đã dùng/trần, tài nguyên thiếu và danh sách phép cần nó.
- Chưa có comment ngoại lệ bundled cho đúng `packet_id` trên #433 ⇒ không cấp lease (**E2**).
- Đặc tả không thuộc Mission ⇒ chờ chủ kho duyệt băm theo `ADR-0067` — **E2**.

## 7. `hinh_dang_ke_thua`

Bộ đếm kế thừa: P2a/packet 1 **mức đặc tả 3, mức mã 0**; đặc tả gộp P2c thêm 3 lượt cùng hình dạng (đều ở phần định danh, đã bỏ theo Q2 = D).
R là lớp "chốt nhìn THIẾU một LOẠI liên kết" của cùng hình dạng: `S_ISLNK` không thấy junction. Mức đặc tả R: 0 lượt lúc soạn.

## 8. `chua_do_duoc`

- Hành vi `os.lstat` trên Windows với junction, mount point, symlink (D2, D3); với tag không phải name-surrogate (không đo, Q7).
- Đột biến 1–3 là lập luận (không có nguyên mẫu: một biểu thức).
- TOCTOU (§2).
- Kích thước (ước lượng tĩnh, chưa đo; mốc P2a): `tl_gws.py` +4–6 (dòng `st =`, điều kiện, docstring 1–2; −1 dòng cũ); fragment: khung + tự
  kiểm + đếm `chỉ_nt` 95–105, rig W5 + bọc `lstat` có khôi phục + dựng junction/symlink + probe 50–62, N1/N2 7 lượt 30–40, `_DB` 3 mục 4–5
  ⇒ **179–212**; bundled 1 ⇒ **184–219**, giữa ~200.

## 9. Lịch sử và quyết định

- Vế này là M4 của đặc tả gộp P2c (bản 2–4) và M6 của P2a bản 1; review lượt 1–3 của đặc tả gộp đã bắt: phạm vi tiền tố người gọi (đóng
  ở §2), thứ tự lượt để đột biến 3 có đích riêng (`W5.jn_cfg` trước `W5.jn_to_tien`), hai lượt symlink không có phép đỏ riêng (khai ở N2).
- Chủ kho 2026-11-19 ~10:50Z: Q1 tách C1 → R; Q7 giữ phạm vi "những gì `lstat` báo".

## 10. Nhật ký revision

- 2026-11-19T10:5xZ (phiên con của điều phối #1206): tách từ đặc tả gộp bản 4; đo §0 trên `96b6a33`. Bản lượt 1 (ngân sách riêng của R),
  sha256 `a403764f…`.
- 2026-11-19T11:0xZ (sau review lượt 1: request_changes, 3 P2, 1 P3): N3(c) đẳng thức cho phép `0 ≤ u ≤ 2` với `h == 0` và đối chứng xanh
  một/hai lượt bỏ qua; phản chứng bộ đo `pc_chi_kiem_cfgdir` cho `W5.jn_to_tien`; D2 dựng symlink bằng `os.symlink`, junction kiểm rc; D3
  có trạng thái trước khi gắn, xác nhận điểm gắn, bản đột biến. Bản lượt 2.
