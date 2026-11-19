tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# GWS-CRED-DICH-NGOAI-KHO-A r1 — trên POSIX, `credentials.json` của gws (W4, W5 trong `tl_gws.py`) phải nằm ngoài kho git, không ghi xuyên liên kết ở BẤT KỲ thành phần nào của đường, và ghi nguyên tử

- packet_id: GWS-CRED-DICH-NGOAI-KHO-A; revision: 1;

| trường | giá trị |
|---|---|
| `packet_issue` | #433 |
| `nguon_cap_viec` | Issue #433. Tách từ đặc tả `NLM-GWS-DICH-NGOAI-KHO-r1.md` theo quyết định của chủ kho ngày 18-11-2026: packet `NLM-GWS-DICH-NGOAI-KHO` giữ W1–W3, W6 (chốt đích) và điều kiện `.claude`; packet `GWS-CRED-DICH-NGOAI-KHO` giữ W4, W5. Chủ kho 2026-11-19 (phiên điều phối #1206, AskUserQuestion) tách tiếp hai tầng: (Q1) kiểm DỮ LIỆU W6 sang **P2b** `GWS-CRED-DICH-NGOAI-KHO-B`; (Q1 tầng hai, sau review lượt 1) danh sách cho phép đường Windows/UNC sang **P2c** `GWS-CRED-DICH-NGOAI-KHO-C`. Đặc tả này là **P2a**: W4/W5 trên POSIX cộng chốt thư mục tổ tiên của `cfgdir`. |
| `phu_thuoc` | Packet `NLM-GWS-DICH-NGOAI-KHO` ĐÃ LAND trên `master` (PR #1394, merge `700fbca`). Packet này gọi lại `_kiem_dich_ghi(dich, goc, thanh_phan)` và `_ghi_nguyen_tu_0600(path, data)` của packet ấy KHÔNG sửa thân, dùng chung hợp đồng lỗi của nó (M4: năm cụm cố định, một dòng stderr, `degraded`). P2b và P2c không là tiền đề của P2a. |
| `review_class` | `sensitive`: `scripts/tl_gws.py` là đường ghi credential. Đối chiếu bằng `lease_publish check` khi cấp lease; không rõ thì giữ `sensitive`. |
| `base` | `3b647461db7c8ded1bddd9aafc5c6aa5eead223f` lúc soạn (2026-11-19, SAU khi packet 1 land); blob `scripts/tl_gws.py` `12e04c03971861d96161b9c1cd55de9c59a5f371`, 2620 dòng. Lease ghi OID base thật lúc cấp; phiên thi hành đo lại §0 trên base ấy trước khi sửa. Số dòng `641108c` trong §0.2 là mốc lịch sử của phép đo E1/E2/S4/S5/L1/L2. |

## 0. Hiện trạng (§0.1, §0.4 đo trên `3b64746`; §0.2 đo trên `641108c` trước packet 1 — hành vi W4/W5 không đổi vì packet 1 không chạm hai chỗ ấy; Linux, Python 3.13.18, dữ liệu GIẢ, không mạng; mốc phút là lời khai của phiên soạn, trừ chỗ ghi giờ máy)

### 0.1 Hai chỗ ghi thuộc packet

| # | hàm | dòng (`3b64746`) | đích | cách ghi hiện tại |
|---|---|---|---|---|
| W4 | `cmd_bootstrap` (1717), nhánh `bundle.get("gws_cred")` | 1780–1790 | `cfgdir/credentials.json`, `cfgdir` = `$GOOGLE_WORKSPACE_CLI_CONFIG_DIR` hoặc `~/.config/gws` (1781; giá trị rỗng chọn mặc định vì `or`) | `os.makedirs(cfgdir)` (1782), `open("wb")` (1784) ghi `bundle["gws_cred"].encode("utf-8")` (1785) không nguyên tử, `chmod` sau (1787); không `try` |
| W5 | `_gws_auth_load` (định nghĩa 1911) | 1930–1939 | như W4 | cùng mẫu (1931–1934); dữ liệu là `bytes` từ `store.decrypt` (1927) |

Người gọi W5: `cmd_gws_auth_load` (1942–1953, nhánh lỗi in một dòng `[gws-auth-load] ✗ {msg}`, rc 2), `cmd_gws_bootstrap_cowork` (2317, 2374),
`tl_core/ops_misc.py` (592). Không ai ghi riêng. `cfgdir` đến THẲNG từ biến môi trường, có thể tương đối hoặc có hậu tố.
Nhánh `--require-agent-creds` của `cmd_bootstrap` (1836–1838) in dòng riêng `[bootstrap] ✗ --require-agent-creds: credential agent chưa nạp
được (rc 4).` rồi trả 4; dòng ấy không mang cụm nào của hợp đồng lỗi.

### 0.2 Phép đo

| phép | dựng | kết quả |
|---|---|---|
| E1 (04:51:21Z) | `_gws_auth_load`, `GOOGLE_WORKSPACE_CLI_CONFIG_DIR=<kho git tạm>/gwscfg` | `(True, …/kho/gwscfg/credentials.json)`; `git status --porcelain` = `?? gwscfg/credentials.json` |
| E2 (04:51:21Z) | `cmd_bootstrap --env code`, bundle có `gws_cred`, cùng biến | rc 0; porcelain = `?? gwscfg/credentials.json` |
| S4 (05:17:57Z) | `_ghi_nguyen_tu_0600` trên đích là symlink vào kho; trên đích là hardlink | tệp được trỏ tới giữ nguyên; hardlink còn lại giữ nội dung cũ |
| S5 (05:17:57Z) | `_ghi_nguyen_tu_0600` với thư mục cha là symlink ra ngoài | tệp được tạo ở thư mục đích của symlink ⇒ writer KHÔNG chặn thành phần thư mục là liên kết |
| L1 (05:31:18Z) | `alias` là symlink tới thư mục; `os.lstat` | symlink cho `alias`; thư mục THƯỜNG cho `alias/`, `alias/.`, `alias/./`, `alias//` |
| L2 (05:31:18Z) | `os.path.normpath("T/alias/../x")` | `T/x` — gộp `..` theo từ vựng, khác đường kernel đi khi `alias` là symlink |
| B1 (2026-11-19T05:32:50Z, giờ máy) | biên trên POSIX, `python3 -I`, thư mục tạm `realpath` | `makedirs(<tệp thường>, exist_ok=True)` ⇒ `FileExistsError`; `open(<thư mục>, "wb")` ⇒ `IsADirectoryError`; `os.replace(<tệp>, <thư mục>)` ⇒ `IsADirectoryError` (lớp con `OSError`); `lstat(<tệp>/x)` ⇒ `NotADirectoryError`; `lstat("a\x00b")` ⇒ `ValueError`; `os.getcwd() == realpath(os.getcwd())` |

Từ B1: trên base, `cfgdir` là tệp thường làm W4 ném `FileExistsError` ra khỏi `cmd_bootstrap` (1782 không có `try`), và NUL lọt xuống
API đường dẫn thành `ValueError` — ngoài mọi `except OSError`.

### 0.3 Ràng buộc kề bên

- Neo PD của `ops/cloud_agent_creds_test.py` (bảng 796–806) và chuỗi khoá của `wp727_tl_gws_refresh`: như §0.4 của đặc tả
  `NLM-GWS-DICH-NGOAI-KHO-r1.md`; mã mới không chứa nguyên văn chuỗi neo PD nào. Fragment packet 1
  (`wp433_nlm_gws_dich_ngoai_kho.py`) có đột biến neo vào `tl_gws.py`; packet này không được làm neo nào của nó khớp ≠ 1 lần.
- Bước CI `bundled-fragment check` kiểm bundled committed trên PR (`ci.yml:294`); manifest committed chỉ bị kiểm trên master.
- Driver `bundle_fragment_check.py` đọc stdout của tiến trình con làm JSON: fragment in ra stderr.
- Nền test: đo lại trên base thật — `--selftest`, `ops/cloud_agent_creds_test.py`, `ruff --select F` trên `scripts/tl_gws.py`; tiêu chí DELTA.

### 0.4 Trạng thái sau packet 1 (đo trên `3b64746`)

- `_kiem_dich_ghi(dich, goc, thanh_phan)` ở 1173–1187: luật (a) `_trong_kho_git(dirname(dich))`; luật (b) `lstat` `goc` và MỌI tiền tố
  `goc/thanh_phan[:i]` tới chính `dich`, đang tồn tại thì không được `S_ISLNK`; `FileNotFoundError`/`NotADirectoryError` bỏ qua, lỗi khác lan ra.
  Nên truyền `goc = "/"` và `thanh_phan` là MỌI thành phần từ gốc thì luật (b) phủ mọi tổ tiên — không cần sửa thân hàm.
- `_ghi_nguyen_tu_0600` (1158–1170): `makedirs(dirname, 0o700)` → `mkstemp(dir=dirname, prefix=".auth.json.")` → ghi/flush/`fsync` →
  `chmod(tmp, 0o600)` → `os.replace` → `except BaseException` xoá tệp tạm rồi ném lại.
- Hợp đồng lỗi packet 1: năm cụm `nằm trong kho git` (1179), `là liên kết tượng trưng` (1184), `dữ liệu không hợp lệ`, `ngoài danh sách
  cho phép` (1193–1202), `ghi lỗi` (1772, 1800); chi tiết `repr(...)[:200]`; dòng `[thẻ] ✗ <cụm>: <chi tiết>`.
- Fragment packet 1 `scripts/test_fragments/wp433_nlm_gws_dich_ngoai_kho.py` (đếm lại bằng AST, xác nhận ở review lượt 1): 353 dòng,
  **18** ca trong `_CA`, **30** mục `_DB`, **4** mục `_TU_KIEM`; khung + đồ nghề chung (dòng 1–54 và 292–353) ≈ 116 dòng, `_Rig` 74.
  Numstat packet 1 (`git show --numstat 700fbca^1..700fbca`, ba đường): `tl_gws.py` +94/−42, fragment +353, bundled +1 = **+448**.

## 1. `write_set`

```
scripts/tl_gws.py
scripts/test_fragments/wp433_gws_cred_dich_ngoai_kho.py
scripts/tl_test_fragments_bundled.py
```

`scripts/tl_test_fragments_bundled.py` theo **quyết định của chủ kho ngày 18-11-2026** (phương án B): worker mang riêng tệp
ấy, chỉ sinh bằng `generate_bundled_module_bytes(scripts/test_fragments)`, KHÔNG mang `RELEASE_MANIFEST.json` — ngoại lệ so với
`docs/PROTOCOL_DA_PHIEN.md` dòng 864–868. **Điều kiện trước khi cấp lease (E2 — Q3, chờ chủ kho):** comment của chủ kho trên Issue #433 cấp
ngoại lệ ấy nêu đúng `packet_id` `GWS-CRED-DICH-NGOAI-KHO-A`, đúng một tệp `scripts/tl_test_fragments_bundled.py` và sha256 của đặc tả
này đã đóng băng; lease trỏ tới URL comment. Comment cấp cho packet 1 không phủ packet này. Phiên land tái sinh
`RELEASE_MANIFEST.json` trong commit land.

## 2. `ngoai_pham_vi`

- **Để P2b** (`GWS-CRED-DICH-NGOAI-KHO-B`, chủ kho 2026-11-19 Q1): kiểm DỮ LIỆU W6 (M7 cũ), ca `w6_du_lieu` (N9w6 cũ), ca hồi quy
  `jar_rong_base` (N3d cũ), §4b dòng 24–29 cũ. Chủ kho xếp lịch P2b SAU khi P2a land (Q1); về mã, P2b chỉ chạm W6 nên không cần mã P2a.
- **Để P2c** (`GWS-CRED-DICH-NGOAI-KHO-C`, chủ kho 2026-11-19 Q1 tầng hai + Q2 thu hẹp, đặc tả riêng, làm sau P2a):
  (1) danh sách cho phép đường Windows (ổ `X:\…`, từ chối `C:`, `D:fake`, `\fake`, `\\?\…`, `\\.\…`, `\\server` thiếu share), chạy mọi nền
  qua `ntpath`, kèm ca riêng cho gạch trộn, chữ hoa/thường ổ, `..` kiểu Windows, mỗi namespace thiết bị một nhãn — các finding lượt 1
  về dạng đường M1 và đột biến dòng 32 cũ (`db_unc_khong_can_share` không thể đỏ: regex vẫn đòi phân cách trước share) chuyển sang đây;
  (2) UNC `\\server\share\…`: **chủ kho Q2 (thu hẹp)** — chốt bằng SO ĐỊNH DANH tệp (volume serial + file id) của thư mục đích với GỐC KHO
  TRA-LUAT và các tổ tiên của đích; định danh trùng ⇒ nằm trong kho ⇒ từ chối. Khai rõ: chốt ấy KHÔNG bảo vệ kho git KHÁC truy cập qua
  share cùng máy hoặc ổ ánh xạ; (3) vế reparse point (M6 cũ: `st_file_attributes & FILE_ATTRIBUTE_REPARSE_POINT` trong `_kiem_dich_ghi`,
  N3c giả lập, N4 junction native) — khái niệm chỉ có trên Windows, đi cùng P2c (§9 Q4).
- **Windows trong P2a:** khi `os.name != "posix"`, W4/W5 KHÔNG chốt đích (giữ như base) — chỉ đổi sang ghi nguyên tử bằng
  `_ghi_nguyen_tu_0600` và hợp đồng lỗi M3. P2c thay nhánh ấy. Không có CI Windows bắt buộc; quyền 0600 không đo bằng `stat` trên Windows.
- W1–W3, W6, điều kiện `.claude`, `_kiem_jar_nlm`: packet `NLM-GWS-DICH-NGOAI-KHO`. Chốt tổ tiên của P2a chỉ áp cho W4/W5 (bằng
  cách gọi); W6 hiện gọi `_kiem_dich_ghi(cfgp, cfgp, ())` nên chưa kiểm tổ tiên — không sửa ở đây.
- Không sửa THÂN `_kiem_dich_ghi`, `_trong_kho_git`, `_ghi_nguyen_tu_0600`; không sửa `ops/**`, `.github/**`, `scripts/tl_selftest.py`,
  `RELEASE_MANIFEST.json`, `changelog.d/*`, `VERSION`, `CHANGELOG.md`, `SKILL.md`.
- Mục 3, mục 8 của #433: chủ kho quyết định 18-11-2026 là lỗi thời / theo thiết kế. Không chốt binary gws, `bindir`,
  `_persist_local_bin_on_path`.
- **TOCTOU — giới hạn bảo đảm:** chốt kiểm theo TÊN rồi `makedirs`/`mkstemp`/`replace` theo TÊN; không dùng thao tác gắn định danh
  thư mục (`dir_fd`, `O_NOFOLLOW` theo từng cấp). Bảo đảm của P2a CHỈ đúng khi mọi thư mục từ `/` tới `cfgdir` không bị BẤT KỲ
  principal nào (cùng hay khác uid) thay hoặc đổi tên trong khoảng từ lúc kiểm tới lúc `os.replace` trả về. Thư mục cha ghi được bởi
  principal khác (ví dụ thư mục dùng chung không có sticky bit) nằm ngoài bảo đảm. Không ca nào đo khe này; đây là giới hạn được khai,
  không phải hành vi được hứa.

## 3. `muc_tieu`

| # | mục tiêu | tệp |
|---|---|---|
| M1 | `_duong_dich_chuan(p, cwd)` (POSIX) trả `(đường_tuyệt_đối, thanh_phan_tu_goc)` hoặc chuỗi lý do `đường không hợp lệ: <repr(p)[:200]>`. Danh sách CHO PHÉP: (P1) `p` bắt đầu bằng `/` ⇒ tuyệt đối; (P2) `p` không bắt đầu bằng `/` ⇒ tương đối, ghép `cwd + "/" + p` theo chuỗi — KHÔNG `abspath`, `normpath`, `realpath` (§0.2 L2). Từ chối TRƯỚC khi ghép: `p` chứa `"\x00"` (B1: `ValueError` ngoài `except OSError`); `p.strip() == ""` (chuỗi chỉ khoảng trắng — chuỗi rỗng không tới được đây vì `or` chọn mặc định, §0.1). Rồi tách theo `/`, bỏ thành phần rỗng (hậu tố `/`, `//`) và `.`; còn `..` ⇒ từ chối; còn ≥ 1 thành phần (không cho `cfgdir` = `/`). Đường trả về = `"/" + "/".join(thanh_phan)`; đó là đường DUY NHẤT được kiểm, được ghi và (W5) được trả về. `cwd` đọc bằng `os.getcwd()` MỘT lần ở người gọi (B1: đường vật lý). | `scripts/tl_gws.py` |
| M2 | Hàm chung `_dich_cred_gws(cfgdir_tho)` trả `(dest, lý_do)`, gọi ở W4 và W5 TRƯỚC mọi `makedirs`/ghi: trên POSIX — M1, rồi `_kiem_dich_ghi(dest, "/", (*thanh_phan, "credentials.json"))` với `dest = <đường M1> + "/credentials.json"`, nên luật (b) `lstat` MỌI tổ tiên từ `/`, chính `cfgdir` và tệp cuối (finding P1 lượt 1). Trên `os.name != "posix"` — trả `(os.path.join(cfgdir_tho, "credentials.json"), None)` (P2c thay). Được phép ⇒ ghi bằng `_ghi_nguyen_tu_0600(dest, data)` thay `makedirs` + `open("wb")` + `chmod`. W4 trước đó đòi `bundle["gws_cred"]` là `str` và `.encode("utf-8")` thành công, sai ⇒ `dữ liệu không hợp lệ: gws_cred`. Lời gọi `_dich_cred_gws` và writer nằm trong MỘT `try … except OSError` ở mỗi chỗ ⇒ `ghi lỗi: <_safe_exc(e)>`. Ngoài kho, không liên kết ⇒ nội dung tệp như base. | `scripts/tl_gws.py` |
| M3 | Hợp đồng lỗi: theo M4 packet 1, thêm cụm thứ sáu `đường không hợp lệ`. Mọi dòng lỗi W4 `fullmatch` `\[bootstrap\] ✗ (nằm trong kho git|là liên kết tượng trưng|dữ liệu không hợp lệ|đường không hợp lệ|ghi lỗi): .+`, mọi đường nội suy qua `repr` (một dòng). W4 bị từ chối hoặc lỗi ghi ⇒ ĐÚNG MỘT dòng mang cụm ra stderr, `degraded = True`, đúng một dòng `[bootstrap] agent_creds:` ra stdout, rc 1; dòng `✓ gws cred → …` KHÔNG in. Có `--require-agent-creds` mà agent chưa `ĐÃ NẠP` ⇒ rc 4 và THÊM đúng dòng §0.1 (đếm riêng, không mang cụm). W5 trả `(False, <lý do bắt đầu bằng "<cụm>: ">)`; `cmd_gws_auth_load` in đúng một dòng `fullmatch` `\[gws-auth-load\] ✗ (<sáu cụm>): .+`, rc 2. Không ngoại lệ thoát ra: kiểu/encode kiểm TRƯỚC; NUL bị M1 từ chối; lời ghi chỉ bắt `OSError`. Tập ngoại lệ khai gắn với từng LƯỢT gọi = cột "ngoại lệ khai" §4b; ngoài tập của lượt đang chạy ⇒ `ngoai_le_la`. | `scripts/tl_gws.py` |
| M4 | Fragment `scripts/test_fragments/wp433_gws_cred_dich_ngoai_kho.py`, `TEST_ID = "wp433_gws_cred_dich_ngoai_kho"`, `run(tl_module)`, cùng khuôn fragment packet 1 nhưng tự chứa (không import fragment khác): rig HOME/`USERPROFILE`/`CODEX_HOME`/`GOOGLE_WORKSPACE_CLI_CONFIG_DIR`/`TL_*`/cwd tạm, thư mục gốc rig = `realpath(mkdtemp())` (để không tổ tiên nào là symlink, như `/var` trên macOS), khôi phục trong `finally`; thay `AGENT_CREDS_FILEID`/`TL_AGENT_CREDS_FILEID`, `_public_curl_bytes`, `_gas`, `_secrets_fetch`, `load_creds`, `_ensure_nlm_installed`, `cmd_gws_bootstrap_cowork`, `gws_exe` bằng đồ giả có đếm; lớp chặn `subprocess`/`urlopen` (`MANG_BI_CHAN`) chỉ trong cửa sổ gọi `tl_gws`; bộ quan sát bọc `tempfile.mkstemp`, `os.fsync`, `os.chmod`, `os.replace` (ghi nhận + tiêm lỗi theo pha, §4 N7); mọi đầu ra ra STDERR; đột biến trên bản sao trong bộ nhớ, neo khớp đúng 1 lần, `compile` thành công, phân hạng `TinHieuChotCa(AssertionError)` theo (ca, lượt, nhãn). Ca, lượt và đột biến viết dạng bảng; danh sách ID đột biến dự kiến `_DU_KIEN` viết RIÊNG khỏi `_DB`. | fragment |
| M5 | Tái sinh `scripts/tl_test_fragments_bundled.py` bằng `generate_bundled_module_bytes(scripts/test_fragments)`; không sửa tay; không đụng `RELEASE_MANIFEST.json`. | bundled |

## 4. `nghiem_thu`

Ký hiệu như đặc tả packet 1 §4 (K = kho git tạm, SENT = `SENTINEL-wp433-gws-…`, sạch(K) = `git status --porcelain` rỗng). "Fixture gws
chuẩn" = `cmd_bootstrap --env code --no-nlm --no-gws`, HOME ngoài mọi kho, bundle có `token` và `gws_cred`, KHÔNG `nlm_auth`, agent giả
`KHÔNG CẤU HÌNH`, `gws_exe` giả trả có; với `cfgdir` ngoài kho nó trả rc 0 — nên mọi rc 1 trong ca dùng fixture này chỉ đến từ W4.
"stderr đúng (W4)" = trong stderr đúng MỘT dòng bắt đầu `[bootstrap] ✗ ` khác dòng §0.1, và dòng ấy `fullmatch` mẫu M3 với cụm nêu
trong nhãn; "W5 đúng" = `(False, s)` với `s` `fullmatch` `<cụm>: .+` một dòng. Cột "nền" = `mọi` hoặc `posix` (ca `posix` trên nền khác
được đếm `chỉ_posix`, không tính `bỏ_qua`, §N8).

| # | ca (nền) · lượt | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|---|
| N1 | `w4_trong_kho` (posix) · `w5_trong_kho` (posix) | `cfgdir = K/gwscfg` ⇒ [`ma`] W4 rc 1, W5 `(False, …)`; [`stderr`] stderr đúng/W5 đúng với `nằm trong kho git`; [`sach`] `K/gwscfg` không tồn tại, sạch(K); [`agent_creds`] W4 một dòng `agent_creds:`; SENT không trong đầu ra. Vế âm base: §0.2 E1, E2. | `db_w4_bo_chot`, `db_w5_bo_chot` ⇒ `sach` của đúng chỗ ấy. `db_w4_quen_degraded` ⇒ `w4_trong_kho` `ma`. |
| N2 | `w5_goc_bieu_dien` (posix): `that` thư mục thật ngoài kho, `alias` symlink tới `that`, cwd = thư mục cha | `cfgdir` = `<tuyệt đối>/alias`, `…/alias/`, `…/alias/.`, `alias`, `alias/`, `alias/.` ⇒ [`goc_<i>`] W5 đúng với `là liên kết tượng trưng`, `that` rỗng. `x/../that` (có sẵn thư mục `x`) ⇒ [`hai_cham`] W5 đúng với `đường không hợp lệ`. Vế dương [`tuong_doi_thuong`]: `cfgthuong` ⇒ `(True, d)`, `d == <cwd>/cfgthuong/credentials.json`, tệp đúng byte. `w4_goc_alias_cham` (posix): fixture gws chuẩn, `cfgdir` = `<tuyệt đối>/alias/.` ⇒ [`goc_w4`] rc 1, stderr đúng với `là liên kết tượng trưng`, `that` rỗng. | `db_lstat_tho` ⇒ `goc_1`. `db_w4_khong_chuan_hoa` ⇒ `goc_w4`. `db_bo_cam_hai_cham` ⇒ `hai_cham`. `db_ghi_duong_tho` (kiểm đường chuẩn nhưng ghi/trả `os.path.join(cfgdir_thô, …)`) ⇒ `tuong_doi_thuong`. |
| N3 | `to_tien` (posix) — MỌI cấp của đường, cả hai đường ngoài kho (finding P1 lượt 1). Dựng `R/thuc/a/b` thật và `R/lk` symlink tới `R/thuc`. Lượt `W4.ong` và `W5.ong`: `cfgdir = R/lk/a/b` (tổ tiên HAI cấp trên `cfgdir` là symlink); lượt `W5.cha`: `R/lk2` symlink tới `R/thuc/a`, `cfgdir = R/lk2/b` (cha trực tiếp); lượt `W5.goc_cfg`: `cfgdir` chính là symlink (`R/lk3` → `R/thuc/a/b`); lượt `W4.tep_cuoi` và `W5.tep_cuoi`: `cfgdir` thường ngoài kho, `credentials.json` là symlink tới `R/dich.json` (`CU`). | [`lien_ket`] W4 rc 1/stderr đúng, W5 đúng — cụm `là liên kết tượng trưng`, chi tiết là `repr` đúng thành phần là liên kết; [`khong_ghi`] không có `credentials.json` mới dưới `R/thuc`, `R/dich.json` còn `CU`. Vế âm base: §0.2 S5 (writer ghi xuyên cha liên kết). Lượt kho (N3b) giữ riêng xuất xứ lỗi `nằm trong kho git`. | `db_w4_goc_cfgdir`, `db_w5_goc_cfgdir` (truyền `goc = <cfgdir chuẩn>`, `thanh_phan = ("credentials.json",)` như bản lượt 1) ⇒ lượt `W4.ong`/`W5.ong`, `lien_ket`. `db_bo_symlink_cuoi` (luật (b) bỏ qua chính `dich`) ⇒ lượt `W4.tep_cuoi` (lượt đầu tiên nó chạm), `lien_ket`. Thứ tự lượt: `W4.ong`, `W5.ong`, `W5.cha`, `W5.goc_cfg`, `W4.tep_cuoi`, `W5.tep_cuoi`. |
| N3b | `w5_chuoi_realpath`, `w5_chuoi_tu_vung` (posix) | (1) `L` symlink NGOÀI kho trỏ vào `K/sub`, `cfgdir = L/gws` ⇒ [`kho_truoc`] W5 đúng với cụm `nằm trong kho git` (luật (a) chạy trước luật (b), dù `L` là liên kết), sạch(K); (2) `lk` symlink TRONG K trỏ ra T, `cfgdir = K/lk/gws` ⇒ [`tu_choi_tu_vung`] cụm `nằm trong kho git`, T rỗng. | `db_chi_tu_vung` (trong `_kiem_dich_ghi`, chỉ đi lên trên `abspath`) ⇒ (1) `kho_truoc` (khi ấy luật (b) bắt `L` với cụm khác). `db_chi_realpath` ⇒ (2). Neo trên thân `_kiem_dich_ghi` của base; KHÔNG sửa `_trong_kho_git`. |
| N3e | `w5_duong_xuong_dong` (posix): kho là thư mục `k\nho` (có `.git`), `cfgdir = k\nho/gws` | [`mot_dong`] `cmd_gws_auth_load` (với `_gws_auth_load` thật) in ĐÚNG một dòng `✗` `fullmatch` mẫu M3 với chi tiết `repr(<đường kho>)`, rc 2; lượt W4 cùng `cfgdir` ⇒ stderr đúng. Đo 2026-11-18T06:33:10Z: không `repr` ⇒ 2 dòng. | `db_khong_repr_gws` ⇒ `mot_dong`. |
| N4 | `bien_cfgdir` (posix, trừ lượt `M1.*` chạy mọi nền vì gọi thẳng `_duong_dich_chuan` với `cwd` giả) | Lượt `M1.nul`: `_duong_dich_chuan("a\x00b", "/c")` ⇒ [`nul`] lý do `đường không hợp lệ`. Lượt `M1.trang`: `"   "` ⇒ [`trang`] `đường không hợp lệ`. Lượt `M1.goc`: `"/"` và `"/./"` ⇒ [`goc_rong`] `đường không hợp lệ`. Lượt `W4.cfg_la_tep`, `W5.cfg_la_tep`: `cfgdir` là TỆP thường ⇒ [`hop_dong`] W4 rc 1/stderr đúng, W5 đúng — cụm `ghi lỗi`; [`nguyen_trang`] tệp giữ byte, không tệp tạm. Lượt `W4.dich_la_thu_muc`, `W5.dich_la_thu_muc`: `cfgdir/credentials.json` là THƯ MỤC ⇒ [`hop_dong`] cụm `ghi lỗi`; [`nguyen_trang`] thư mục còn, rỗng, không tệp tạm. Mỗi lượt ghi số lần writer được gọi (0 cho `M1.*`, 1 cho hai lượt `dich_la_thu_muc`). Vế âm base: B1 (`FileExistsError`/`IsADirectoryError` thoát khỏi W4; NUL ⇒ `ValueError`). | `db_nhan_nul` ⇒ `nul`. `db_nhan_khoang_trang` ⇒ `trang`. `db_nhan_goc` (bỏ điều kiện ≥ 1 thành phần) ⇒ `goc_rong`. `db_w4_oserror_hep` (except ở W4 chỉ bắt `FileNotFoundError`) ⇒ lượt `W4.cfg_la_tep`, `hop_dong`. |
| N5 | `nguyen_tu` (mọi): lượt `W4.thuong`, `W5.thuong` — `cfgdir` ngoài kho có sẵn `credentials.json` cũ; lượt `W5.hardlink` — `credentials.json` là hardlink của H (`CU`) | Nhãn theo THỨ TỰ: [`nguyen_tu`] đúng MỘT `os.replace` có đích `credentials.json`, nguồn cùng thư mục và là đường `mkstemp` trả; [`fsync`] trước `replace` ấy có `os.fsync(fd)` với `fd` chính là fd `mkstemp` của nguồn; [`quyen`] (chỉ POSIX) nguồn `0600` lúc thay, đích `0600` sau cùng; [`byte`] tệp đúng byte, W4 rc 0 và in `✓ gws cred → …`; lượt `W5.hardlink`: [`ban_kia_giu`] H còn `CU`. | `db_w4_khong_nguyen_tu`, `db_w5_khong_nguyen_tu` (về `makedirs` + `open("wb")` + `chmod`) ⇒ lượt `W4.thuong`/`W5.thuong`, `nguyen_tu`. `db_bo_fsync` (thân writer bỏ `os.fsync`) ⇒ `W4.thuong`, `fsync`. `db_ghi_xuyen_hardlink` (writer `open(path, "r+b")` ghi đè đích đang có trước `replace`; số `replace` vẫn 1) ⇒ `W5.hardlink`, `ban_kia_giu`. |
| N6 | `w4_du_lieu_sai_dang` (mọi): lượt `N6.kieu` — `gws_cred` là số; `N6.surrogate` — chứa surrogate đơn | [`kieu`], [`surrogate`] rc 1, stderr đúng với `dữ liệu không hợp lệ`, không `credentials.json`, không tệp tạm, writer 0 lần, không ngoại lệ. | `db_w4_bo_kiem_kieu` ⇒ `kieu`. `db_w4_bo_kiem_encode` ⇒ `surrogate`. |
| N7 | `ghi_loi_theo_pha` (mọi): bộ quan sát ném `OSError("wp433-oserror-<pha>")` ở ĐÚNG MỘT pha, chỉ khi thư mục đích là `cfgdir` của ca: `mkstemp`, `fsync`, `chmod`, `replace`. Tám lượt theo thứ tự `W4.mkstemp`, `W4.fsync`, `W4.chmod`, `W4.replace`, `W5.mkstemp`, `W5.fsync`, `W5.chmod`, `W5.replace`, mỗi lượt có sẵn `credentials.json` cũ; thêm lượt `W5.cli` (`cmd_gws_auth_load` với `_gws_auth_load` thật, pha `replace`). | [`hop_dong`] W4 rc 1/stderr đúng, W5 đúng — cụm `ghi lỗi`, chi tiết chứa `wp433-oserror-<pha>`; W4 không in `✓ gws cred`; `W5.cli` đúng một dòng `[gws-auth-load] ✗ ghi lỗi: …`, rc 2; [`ban_cu`] `credentials.json` giữ byte cũ; [`khong_tam`] không tệp `.auth.json.*` trong `cfgdir`. | `db_w4_oserror_lan`, `db_w5_oserror_lan` (bỏ `except OSError` ở đúng một chỗ) ⇒ lượt ĐẦU của chỗ ấy (`W4.mkstemp`, `W5.mkstemp`), `hop_dong`. `db_bo_don_tam` (thân writer bỏ nhánh xoá tệp tạm) ⇒ lượt `W4.fsync`, `khong_tam`. |
| N8 | `chung_hop_dong_loi` (posix), hai lượt theo thứ tự `W4.trong_kho` rồi `require` | (1) [`stderr`] lượt `W4.trong_kho` lặp lại N1 với kiểm `fullmatch` TOÀN BỘ dòng `✗` (không dòng `✗` thứ hai); (2) [`require`] lượt `require`: `w4_trong_kho` kèm `--require-agent-creds` ⇒ rc 4, đúng một dòng mang cụm `nằm trong kho git` cộng đúng dòng §0.1, một `agent_creds:`. Thêm: `python3 ops/cloud_agent_creds_test.py` trên head `TONG: DAT`, `PD*` vẫn `GIET`, từng ca bằng base; fragment packet 1 vẫn ĐẠT. | `db_w4_in_hai_dong` (thêm một dòng `[bootstrap] ✗ xem thêm` không cụm) ⇒ `stderr`. `db_w4_lap_dong` (in lại ĐÚNG dòng lỗi hợp lệ lần thứ hai) ⇒ `stderr` — vế "đúng MỘT dòng", tách khỏi `db_w4_in_hai_dong` (dòng thêm không khớp mẫu ⇒ vế `fullmatch`). `db_require_thua_rc1` ⇒ `require`. Gate PD/packet 1: trên cây tạm sửa một ký tự trong một chuỗi neo PD của `tl_gws.py` ⇒ `cloud_agent_creds_test` không `TONG: DAT`; sửa một ký tự trong một neo của fragment packet 1 ⇒ fragment ấy `HONG ≥ 1`, `run` False. |
| N9 | Tự kiểm của fragment | (a) mỗi ID trong `_DU_KIEN` có đúng một mục `_DB` và ngược lại (so TẬP ID); mỗi mục giết đúng (ca, lượt, nhãn) đã khai; (b) MỘT dòng tổng kết RA STDERR `[wp433_gws_cred_dich_ngoai_kho] CA: dự_kiến=a chạy=b đạt=c bỏ_qua=d chỉ_posix=w · DOT BIEN: dự_kiến=e chạy=f giết_đúng=g bỏ_qua=h chỉ_posix=v · HONG: i · TU_KIEM: k/k`; `run` True chỉ khi `b == c`, `f == g`, `i == 0`, `a == b + d + w`, `e == f + h + v`, `e == len(_DU_KIEN)`, mọi tự kiểm đúng hạng; trên POSIX `d == h == w == v == 0`; trên nền khác `w`/`v` bằng đúng số ca/đột biến có cột nền `posix`; (c) tự kiểm phân hạng, mỗi mục là (đột biến, ca, lượt, nhãn, hạng mong đợi): `tu_kiem_doi_kieu` — chèn vào W4 `try: raise AttributeError("wp433-tu-kiem") except Exception as e: raise AssertionError(f"wp433-tu-kiem {type(e).__name__}")`, nhắm (`w4_du_lieu_sai_dang`, `N6.kieu`, `kieu`) ⇒ `TIN_DUNG_GIA`, VÀ ngoại lệ bắt được có `__context__` kiểu `AttributeError` (chứng minh đã đi qua `except` đổi kiểu); `tu_kiem_chu_thich` — chỉ thêm chú thích ⇒ `SONG_SOT`; `tu_kiem_sai_luot` — CHÍNH đột biến `db_w4_oserror_lan`, cùng ca `ghi_loi_theo_pha`, cùng nhãn `hop_dong`, cùng kiểu `OSError`, cùng dấu `wp433-oserror`, CHỈ khai lượt `W4.fsync` thay `W4.mkstemp` ⇒ `TIN_DUNG_GIA`; (d) neo 0/2 lần hoặc không `compile` ⇒ `HONG`; (e) stdout của `run` rỗng. | Trên cây tạm: thêm một ID vào `_DU_KIEN` không có mục `_DB` ⇒ (a) False; đổi lượt đích của `db_w5_bo_chot` sang lượt W4 ⇒ False; TẮT nhãn `goc_1` ⇒ `db_lstat_tho` không giết đúng ⇒ False; neo khớp 2 lần ⇒ `HONG: 1`, False; ép một ca `posix` vào `bỏ_qua` trên POSIX ⇒ False; bộ phân hạng bỏ so lượt ⇒ `tu_kiem_sai_luot` ra `GIET` ⇒ False; in tổng kết ra stdout ⇒ (e) đỏ. |
| N10 | Exact head: `--selftest` ĐẠT N/N hai số bằng nhau trên clone thật, N = N_base + 1, DELTA = 0 ca đỏ mới (base và head dựng trong CÙNG một lệnh); `test-fragments-check --json` ⇒ `ok: true`; `bundle_fragment_check.py --json` ⇒ `ok: true`, `failed: []`. | Không tái sinh bundled ⇒ `TEST_ID_SET_MISMATCH`; sửa tay bundled ⇒ `GENERATED_BUNDLE_STALE`. Trên cây tạm: gỡ fragment khỏi bundled ⇒ selftest cho N = N_base ⇒ đỏ vế `N_base + 1`; cho `run` trả False ⇒ selftest `N−1/N` ⇒ đỏ vế N/N. |
| N11 | Lane worker `ci.yml` (521–532) tại chỗ: `release-manifest --root . --out <tạm>` rồi `release-verify <tạm> --root . --strict` ⇒ `ok: true`, `expected_file_count == checked_file_count`. Phiên land tái sinh manifest trong commit land, hồ sơ land ghi `release-verify RELEASE_MANIFEST.json --strict` `ok: true` trên commit ấy. | Trên bản sao: sửa một byte của một tệp trong gói sau khi sinh manifest tạm ⇒ `ok: false`; xoá một tệp trong gói ⇒ `ok: false` hoặc `checked_file_count < expected_file_count`. |
| N12 | Exact head, lệnh + rc + bằng chứng dương: `ruff check --select F` delta = 0 trên `scripts/tl_gws.py`, 0 trên fragment và bundled; `git diff --check <base>..<head>` rc 0; `doctrine-scan`, `adr-song` rc 0; dưới `set -o pipefail`: `git diff --numstat <base>..<head> > numstat.txt` (rc ≠ 0 ⇒ đỏ), (i) đúng 3 dòng, (ii) mỗi dòng khớp `^[0-9]+\t[0-9]+\t<đường>$`, tập đường == §1, (iii) tổng cột thêm ≤ 450. | Tên chưa định nghĩa ⇒ delta ≠ 0. Trên bản sao head thêm khoảng trắng cuối dòng ⇒ `git diff --check` rc ≠ 0. Numstat dựng tay: đúng 3 dòng, đúng tập đường, tổng 450 ⇒ XANH; đổi một cột cho tổng 451 ⇒ (iii) ĐỎ; giữ số, đổi một đường thành đường ngoài §1 ⇒ (ii) ĐỎ; đổi một cột thành `-` (tệp nhị phân) ⇒ (ii) ĐỎ; đầu vào rỗng ⇒ (i); `<base>` không tồn tại ⇒ rc 128 ⇒ đỏ. `doctrine-scan`/`adr-song`: gate kế thừa, phản chứng thuộc bộ test của chính lệnh ấy (`.claude/dev/packet_loop_test.py`); packet này không thêm (L3 khai). |

### 4b. Bảng đột biến — NGUỒN DUY NHẤT (thắng mọi mô tả đột biến rải trong §4)

Luật như §4b packet 1, gồm luật LƯỢT GỌI: tập ngoại lệ khai gắn với từng lượt; ngoại lệ ngoài tập của lượt đang chạy ⇒ ca dừng với nhãn
`ngoai_le_la` (không bao giờ là nhãn đích); đột biến chỉ GIẾT khi tín hiệu `TinHieuChotCa` mang đúng (ca, lượt, nhãn). Trong một lượt các
nhãn được kiểm theo thứ tự ghi ở §4 và các lượt chạy theo thứ tự ghi ở §4; nhãn đầu tiên đỏ là nhãn của tín hiệu, nên lượt đích của một đột biến là lượt ĐẦU TIÊN nó làm đỏ. Mọi hậu điều của lượt được THU trước khi so (không dừng giữa
lúc đo). Ràng buộc cài đặt: kiểu/encode của `gws_cred` kiểm TRƯỚC khi ghi; NUL/khoảng trắng bị M1 từ chối; lời ghi W4/W5 chỉ bắt `OSError`.
Đột biến neo trên NGUỒN CANDIDATE (đã áp M1–M3). Cột "nền": `posix` ⇒ đột biến đếm `chỉ_posix` trên nền khác.

| # | đột biến | ca · lượt | nhãn | cơ chế | ngoại lệ khai ở biên lượt | nền | tự kiểm |
|---|---|---|---|---|---|---|---|
| 1 | `db_w4_bo_chot` | `w4_trong_kho` · `-` | `sach` | H | — | posix | lập luận (§0.2 E2) |
| 2 | `db_w5_bo_chot` | `w5_trong_kho` · `-` | `sach` | H | — | posix | lập luận (§0.2 E1) |
| 3 | `db_w4_quen_degraded` | `w4_trong_kho` · `-` | `ma` | H | — | posix | lập luận |
| 4 | `db_lstat_tho` | `w5_goc_bieu_dien` · `goc_1` | `goc_1` | H | — | posix | đo L1: `lstat("alias/")` không phải symlink |
| 5 | `db_w4_khong_chuan_hoa` | `w4_goc_alias_cham` · `-` | `goc_w4` | H | — | posix | đo L1: `lstat("alias/.")` không phải symlink |
| 6 | `db_bo_cam_hai_cham` | `w5_goc_bieu_dien` · `hai_cham` | `hai_cham` | H | — | posix | đo 2026-11-18T06:42:22Z: `makedirs("x/../that")` không ném |
| 7 | `db_ghi_duong_tho` | `w5_goc_bieu_dien` · `tuong_doi_thuong` | `tuong_doi_thuong` | H | — | posix | lập luận |
| 10 | `db_chi_tu_vung` | `w5_chuoi_realpath` · `-` | `kho_truoc` | H | — | posix | lập luận |
| 11 | `db_chi_realpath` | `w5_chuoi_tu_vung` · `-` | `tu_choi_tu_vung` | H | — | posix | lập luận |
| 12 | `db_bo_symlink_cuoi` | `to_tien` · `W4.tep_cuoi` | `lien_ket` | H | — | posix | lập luận (§0.2 S4: replace giữ tệp được trỏ, nên chỉ lớp từ chối đỏ) |
| 15 | `db_w4_khong_nguyen_tu` | `nguyen_tu` · `W4.thuong` | `nguyen_tu` | H | — | mọi | lập luận |
| 16 | `db_w5_khong_nguyen_tu` | `nguyen_tu` · `W5.thuong` | `nguyen_tu` | H | — | mọi | lập luận |
| 17 | `db_w4_bo_kiem_kieu` | `w4_du_lieu_sai_dang` · `N6.kieu` | `kieu` | E — `.encode` trên số | `AttributeError` chứa `'int' object has no attribute 'encode'` | mọi | đo: `(5).encode` ⇒ đúng thông điệp |
| 18 | `db_w4_bo_kiem_encode` | `w4_du_lieu_sai_dang` · `N6.surrogate` | `surrogate` | E — `.encode` trước writer, ngoài `try` | `UnicodeEncodeError` chứa `surrogates not allowed` | mọi | đo: đúng thông điệp |
| 19 | `db_w4_in_hai_dong` | `chung_hop_dong_loi` · `W4.trong_kho` | `stderr` | H | — | posix | lập luận |
| 20 | `db_w4_oserror_lan` | `ghi_loi_theo_pha` · `W4.mkstemp` | `hop_dong` | E | `OSError` chứa `wp433-oserror` | mọi | lập luận (thông điệp do bộ quan sát đặt) |
| 21 | `db_w5_oserror_lan` | `ghi_loi_theo_pha` · `W5.mkstemp` | `hop_dong` | E | `OSError` chứa `wp433-oserror` | mọi | lập luận |
| 22 | `db_khong_repr_gws` | `w5_duong_xuong_dong` · `-` | `mot_dong` | H | — | posix | đo 2026-11-18T06:33:10Z: không `repr` ⇒ 2 dòng |
| 23 | `db_require_thua_rc1` | `chung_hop_dong_loi` · `require` | `require` | H | — | posix | lập luận |
| 33 | `db_w4_goc_cfgdir` | `to_tien` · `W4.ong` | `lien_ket` | H | — | posix | lập luận (§0.2 S5) |
| 34 | `db_w5_goc_cfgdir` | `to_tien` · `W5.ong` | `lien_ket` | H | — | posix | lập luận (§0.2 S5) |
| 35 | `db_bo_fsync` | `nguyen_tu` · `W4.thuong` | `fsync` | H | — | mọi | lập luận |
| 36 | `db_bo_don_tam` | `ghi_loi_theo_pha` · `W4.fsync` | `khong_tam` | H | — | mọi | lập luận (tệp tạm đã có từ `mkstemp`) |
| 37 | `db_ghi_xuyen_hardlink` | `nguyen_tu` · `W5.hardlink` | `ban_kia_giu` | H | — | mọi | lập luận (`W4.thuong`/`W5.thuong` vẫn đạt: 1 `replace`, đúng byte) |
| 38 | `db_nhan_nul` | `bien_cfgdir` · `M1.nul` | `nul` | H | — | mọi | lập luận (gọi thẳng, không chạm API đường dẫn) |
| 39 | `db_nhan_khoang_trang` | `bien_cfgdir` · `M1.trang` | `trang` | H | — | mọi | lập luận |
| 40 | `db_nhan_goc` | `bien_cfgdir` · `M1.goc` | `goc_rong` | H | — | mọi | lập luận |
| 41 | `db_w4_oserror_hep` | `bien_cfgdir` · `W4.cfg_la_tep` | `hop_dong` | E | `FileExistsError` (lớp con `OSError`) chứa `File exists` | posix | đo B1 |
| 42 | `db_w4_lap_dong` | `chung_hop_dong_loi` · `W4.trong_kho` | `stderr` | H | — | posix | lập luận |

Số dòng giữ như các lượt trước để đối chiếu: 8, 9, 13, 13b, 14, 30–32 chuyển P2c; 24–29 chuyển P2b. Dòng 20 và 21: cùng ca, cùng nhãn, cùng
(loại, dấu), khác lượt — nên N9(c) `tu_kiem_sai_luot` đổi ĐÚNG MỘT biến (lượt khai của dòng 20, sang `W4.fsync`, một lượt mà đột biến ấy
không bao giờ tới vì ca dừng ở lượt đầu `W4.mkstemp`). Hai lượt `W4.mkstemp`/`W5.mkstemp` đứng đầu khối của chỗ mình nên đột biến 20/21
dừng ở đúng lượt đích. Dòng 33/34 vs 12: cùng nhãn `lien_ket`, khác lượt. Dòng 15/16 vs 35 vs 37: khác nhãn hoặc khác lượt.
Tổng: **29** đột biến (dòng 1–7, 10–12, 15–23, 33–42); E: 5 dòng (17, 18, 20, 21, 41); H: 24 dòng. Nền `posix`: **17** dòng (1–7, 10–12, 19, 22, 23, 33, 34, 41, 42); nền `mọi`: **12** (15–18, 20, 21, 35–40). Tự kiểm bằng phép đo: 8 dòng (4, 5, 6, 12 qua S4, 17, 18, 22, 41); còn lại lập luận, xác nhận khi chạy bảng trên mã thật (N9(a)). Tự kiểm phân hạng: 3 mục (N9(c)).

## 5. `pham_vi_e`

Không chạm E4, không chạm E5: chỉ sửa mã đường ghi, mọi ca dùng giá trị giả, HOME/cfgdir tạm, đồ giả thay tải Drive (rig chặn cả hằng
baked), không LIVE, không đẩy Package. Ngoại lệ bundled ở §1 là quyết định của chủ kho cho đúng packet này.

## 6. `luat_dung`

- Trần lời gọi Codex theo dòng khai `ADR-0055`; chạm trần ⇒ Review Rescue Checkpoint; xin tăng mang **E2**.
- Trần kích thước `ADR-0053`: executor đo `git diff --numstat <base>..H` (N12, không lọc đường dẫn) TRƯỚC khi công bố; vượt 450 dòng
  thêm ⇒ DỪNG, không push, báo điều phối. Không được cắt ca/phép đo để lọt trần (cắt phép đo là đổi đặc tả, phải qua revision). Chủ kho
  đã chọn TÁCH thay vì nâng trần ba lần (18-11, 19-11 Q1, 19-11 Q1 tầng hai); xin `nang_tran` chỉ khi chủ kho đổi quyết định — **E2**.
- `_kiem_dich_ghi` hoặc `_ghi_nguyen_tu_0600` trên base thật khác chữ ký/hành vi ở §0.4, hoặc cần sửa THÂN một trong hai ⇒ dừng, đi revision.
- Chưa có comment cấp ngoại lệ bundled cho packet này trên Issue #433 (§1, Q3) ⇒ không cấp lease.
- Cần sửa ngoài write set, hoặc preflight (quét §0.1 của đặc tả packet 1 trên base thật) thấy chỗ ghi credential từ bundle khác W1–W6 ⇒
  dừng, đi revision.
- Neo PD, chuỗi khoá `wp727`, hoặc neo đột biến của fragment packet 1 không giữ được nguyên văn ⇒ dừng, đi revision.
- Đặc tả không thuộc Mission nên chờ chủ kho duyệt băm theo `ADR-0067` — **E2**.

## 7. `hinh_dang_ke_thua`

Như §7 của đặc tả packet 1: số đếm hình dạng lỗi của tiền nhiệm **KHÔNG ĐO ĐƯỢC**; bộ đếm có chứng cứ DÙNG CHUNG với packet
`NLM-GWS-DICH-NGOAI-KHO` (mức đặc tả 3, mức mã 0); không reset khi tách. Các lượt review của W4/W5 đã bắt ba lớp của cùng một hình dạng
"chốt nhìn THIẾU một phần của đường": thư mục cha là liên kết mà writer đi xuyên (S5), `lstat` chuỗi thô không thấy `alias/` (L1), và
lượt 1 của P2a — chốt chỉ nhìn `cfgdir` và tệp cuối, bỏ qua tổ tiên. M2 đáp lại bằng một chốt duy nhất trên MỌI thành phần từ `/`, mỗi
cấp (tổ tiên, cha, chính `cfgdir`, tệp cuối) một lượt riêng (N3) và đột biến riêng (12, 33, 34).

## 8. `chua_do_duoc`

- Hệ quả hành vi đã biết của chốt tổ tiên (P1 lượt 1, chủ kho chọn): máy có tổ tiên của `cfgdir` là symlink — ví dụ `/var`, `/tmp` trên
  macOS, `/home` liên kết trên vài bản Linux — sẽ bị từ chối với `là liên kết tượng trưng: <thành phần>` cả khi dùng mặc định
  `~/.config/gws`; cách chữa của người dùng là đặt `GOOGLE_WORKSPACE_CLI_CONFIG_DIR` tới đường vật lý. Chưa đo trên máy thật nào; chưa đo
  ảnh hưởng tới phiên Cowork/Code thật (phiên bootstrap ghi `~/.config/gws/credentials.json` — §0 của hook phiên).
- Windows: P2a không đổi chốt đích trên nt (§2); nhánh nt của `_dich_cred_gws` chỉ được đo gián tiếp qua các ca `mọi` nền khi fragment
  chạy trên Windows, không có CI Windows bắt buộc.
- TOCTOU: không đo (§2, giới hạn khai).
- Kích thước P2a (ước lượng tĩnh, chưa đo; tính 2026-11-19 sau tách tầng hai, theo mật độ packet 1 §0.4 — khung 116/353, `_Rig` 74,
  hàm ca trung bình ~6,3 dòng, mục `_DB` ~1,07 dòng):
  `tl_gws.py` +44–54 (M1 POSIX ~14–18; `_dich_cred_gws` ~8–10; W4 viết lại ~14–16 dòng thêm, thay 9 dòng; W5 ~8–10, thay 8 dòng);
  fragment +365–426 (khung + `_DU_KIEN` + đếm theo nền + 3 tự kiểm ~125–135; rig có W4/W5 và bộ quan sát bốn pha ~80–95;
  13 hàm ca ~130–160 — `to_tien` 6 lượt, `ghi_loi_theo_pha` 9 lượt và `bien_cfgdir` 7 lượt viết dạng bảng; bảng 29 mục ~31–37);
  bundled +1 ⇒ **410–481 dòng thêm, 3 tệp, điểm giữa ~446** — sát trần, đầu cao vượt 31. Packet 1 với 30 mục `_DB` và 18 ca đo được
  +448. Trần CƯỠNG CHẾ trên numstat thật (N12 (iii), §6): vượt ⇒ DỪNG trước khi công bố, không cắt ca.
- `review_class`, lease của ba đường, nền test: đo khi cấp lease trên base thật.

## 9. Lịch sử review và quyết định

Lịch sử của đặc tả gốc `GWS-CRED-DICH-NGOAI-KHO` (lượt 3–10 trên các bản trước khi tách) giữ ở bản lưu
`rv433p2a/dac-ta-ban0-truoc-tach.md` (`0d0f586b…`); các kết quả còn hiệu lực đã nằm trong §0, §4: tên `TEST_ID` khớp
`_PACKET_TEST_ID_PATTERN` (lượt 3), định dạng dòng cố định và `repr` (lượt 5–6), luật ngoại lệ theo lượt và bảng §4b là nguồn duy nhất
(lượt 8–9).

**Quyết định của chủ kho (2026-11-19, phiên điều phối #1206, AskUserQuestion):**
- **Q1 — Kích thước: TÁCH, hai tầng.** Tầng một: kiểm DỮ LIỆU W6 sang P2b `GWS-CRED-DICH-NGOAI-KHO-B`. Tầng hai (sau review lượt 1 của
  P2a, vì đóng hết finding vượt 450): P2a = W4/W5 trên POSIX + chốt thư mục tổ tiên của `cfgdir`; P2c `GWS-CRED-DICH-NGOAI-KHO-C` =
  danh sách cho phép đường Windows và UNC, đặc tả riêng, làm sau. M4/M5 và các gate N10–N12 áp cho P2a.
- **Q2 — UNC: thu hẹp, áp cho P2c.** Chốt UNC bằng so định danh tệp (volume + file id) của thư mục đích với gốc kho tra-luat và các tổ
  tiên của đích; trùng ⇒ từ chối. Khai rõ không bảo vệ kho git khác (§2 "Để P2c").
- **Q3 — Ngoại lệ bundled (E2, §1): CÒN MỞ.** Cần comment mới của chủ kho trên #433 nêu đúng `packet_id` `GWS-CRED-DICH-NGOAI-KHO-A`,
  đúng tệp `scripts/tl_test_fragments_bundled.py` và sha256 đặc tả đã đóng băng (comment 6973856830 chỉ phủ packet 1). Không chặn review,
  chặn cấp lease.
- **Q4 (MỞ, không chặn review — phiên soạn xếp, chủ kho có thể đảo):** vế reparse point (M6 cũ) xếp sang P2c vì là khái niệm chỉ có trên
  Windows và P2a giữ phạm vi POSIX; giữ ở P2a thì thêm ~15–25 dòng (một dòng mã, ca giả lập gọi thẳng `_kiem_dich_ghi`, ca junction native,
  hai đột biến), đẩy điểm giữa §8 lên ~461–471, vượt trần.

**Review Codex lượt 1 của P2a** (2026-11-19, bản `9ec552f1…`, `rv433p2a/luot1.verdict.txt`): request_changes, 0 P0, 2 P1, 7 P2, 2 P3.
Xử lý trong bản này:
- P1 tổ tiên `cfgdir` — ĐÃ SỬA: M2 truyền `goc = "/"` và mọi thành phần; N3 `to_tien` sáu lượt (tổ tiên hai cấp, cha, chính `cfgdir`,
  tệp cuối; W4 và W5), cả hai đường ngoài kho; đột biến 33, 34 (bản lượt 1) và 12. N3b giữ riêng xuất xứ lỗi kho (`kho_truoc`).
- P1 UNC ngoài kho — CHUYỂN P2c (Q1 tầng hai, Q2).
- P2 dạng đường M1, dòng 32 không thể đỏ, `isabs("\\fake")` — CHUYỂN P2c.
- P2 biên `cfgdir` — ĐÃ SỬA: M1 từ chối NUL, chỉ khoảng trắng, gốc `/`; N4 `bien_cfgdir` (tệp thay thư mục, thư mục thay tệp, W4/W5,
  số lần gọi writer, hậu điều); rỗng giữ chọn mặc định (§0.1); đích symlink ở N3 `tep_cuoi` cả W4/W5.
- P2 TOCTOU — ĐÃ SỬA bằng khai giới hạn ĐÚNG (§2: mọi principal, không chỉ cùng uid; không hứa, không đo).
- P2 fsync/tiêm lỗi theo pha — ĐÃ SỬA: N5 nhãn `fsync` gắn fd `mkstemp`; N7 bốn pha × W4/W5 với `hop_dong`/`ban_cu`/`khong_tam`; đột biến
  35 (bỏ fsync), 36 (bỏ dọn tạm), 37 (ghi xuyên hardlink, nhãn và lượt riêng khỏi `nguyen_tu`).
- P2 nhãn/fullmatch/đếm stderr — ĐÃ SỬA: §4 định nghĩa "stderr đúng" bằng `fullmatch`, dòng `--require-agent-creds` đếm riêng (§0.1, M3);
  §4b ghi (ca, lượt, nhãn), thứ tự nhãn và thu đủ hậu điều; tách W4/W5 theo lượt; đột biến 42 (lặp đúng dòng lỗi; 19 là dòng thêm không khớp mẫu); 17/18 ghi rõ thao tác ném.
- P2 N8 tự kiểm — ĐÃ SỬA (nay N9): `_DU_KIEN` độc lập, so tập ID, đếm theo nền (`chỉ_posix`), `tu_kiem_sai_luot` chỉ đổi lượt (cùng
  ca/nhãn/kiểu/dấu), `tu_kiem_doi_kieu` đòi `__context__` là `AttributeError`.
- P2 gate — ĐÃ SỬA: N8 phản chứng neo PD/packet 1; N10 phản chứng `N_base + 1` và ca mới đỏ; N11 xoá tệp; N12 `git diff --check`, đường
  sai, cột `-`; `doctrine-scan`/`adr-song` khai gate kế thừa.
- P3 §2 phụ thuộc P2b — ĐÃ SỬA (lịch theo Q1, mã độc lập). P3 căn cứ §8 — ĐÃ SỬA (§0.4 theo AST: 18 ca, 30 `_DB`, 4 tự kiểm, +448).

## 10. Nhật ký revision

- 2026-11-19T04:5xZ (phiên con của điều phối #1206): đo lại §0.1 trên `3b64746`; đóng bốn finding lượt 10 của đặc tả gốc. Bản trước:
  `6c654d64…` (`rv433p2/dac-ta-ban0-hoan.md`).
- 2026-11-19 (phiên con): theo Q1 tầng một — đổi `packet_id` thành `GWS-CRED-DICH-NGOAI-KHO-A`, gỡ phần W6 sang P2b. Bản trước tách:
  `0d0f586b…` (`rv433p2a/dac-ta-ban0-truoc-tach.md`). Bản review lượt 1: `9ec552f1…` (`rv433p2a/dac-ta-ban1.md`).
- 2026-11-19 (phiên con, sau lượt 1 và Q1 tầng hai/Q2 thu hẹp): thu phạm vi về POSIX; chuyển dạng đường Windows, UNC, M6 reparse sang
  P2c; đóng các finding lượt 1 thuộc P2a (§9); đánh số lại N (N4 mới = biên `cfgdir`, N7 = tiêm lỗi theo pha, N9 = tự kiểm, N10–N12 = gate);
  thêm đột biến 33–42 (29 tổng); §8 tính lại 410–481, giữa ~446.
