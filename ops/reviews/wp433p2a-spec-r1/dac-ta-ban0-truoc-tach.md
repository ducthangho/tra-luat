tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# GWS-CRED-DICH-NGOAI-KHO r1 — `credentials.json` của gws (W4, W5 trong `tl_gws.py`) phải nằm ngoài kho git, không ghi xuyên liên kết và ghi nguyên tử

- packet_id: GWS-CRED-DICH-NGOAI-KHO; revision: 1;

| trường | giá trị |
|---|---|
| `packet_issue` | #433 |
| `nguon_cap_viec` | Issue #433. Tách từ đặc tả `NLM-GWS-DICH-NGOAI-KHO-r1.md` theo quyết định của chủ kho ngày 18-11-2026 (qua phiên điều phối): packet `NLM-GWS-DICH-NGOAI-KHO` giữ W1–W3 (jar NLM), W6 (config) và điều kiện `.claude`; packet này giữ W4, W5 (`credentials.json` của gws). |
| `phu_thuoc` | Packet `NLM-GWS-DICH-NGOAI-KHO` ĐÃ LAND trên `master` (PR #1394, merge `700fbca`; hồ sơ land `ops/land/pr1394-wp433-*`). Packet này gọi lại `_kiem_dich_ghi(dich, goc, thanh_phan)` do packet ấy thêm (M1 của nó) và dùng chung hợp đồng lỗi của nó (M4: năm cụm cố định, một dòng stderr, `degraded`). Không cấp lease trước khi packet ấy land. |
| `review_class` | `sensitive`: `scripts/tl_gws.py` là đường ghi credential (`credentials.json` của gws). Đối chiếu bằng `lease_publish check` khi cấp lease; không rõ thì giữ `sensitive`. |
| `base` | `3b647461db7c8ded1bddd9aafc5c6aa5eead223f` lúc soạn lại (2026-11-19, SAU khi packet 1 land); blob `scripts/tl_gws.py` `12e04c03971861d96161b9c1cd55de9c59a5f371`, 2620 dòng. Lease ghi OID base thật lúc cấp; phiên thi hành đo lại §0 trên base ấy trước khi sửa. Số dòng `641108c` cũ trong §0.2 là mốc lịch sử của phép đo E1/E2/S4/S5/L1/L2, không phải neo sửa. |

## 0. Hiện trạng (§0.1 đo lại trên `3b64746` lúc 2026-11-19T04:5xZ; §0.2 đo trên `641108c` trước packet 1, hành vi W4/W5 không đổi vì packet 1 không chạm hai chỗ ấy — §0.1; Linux, Python 3.13.18, dữ liệu GIẢ, không mạng; mốc phút là lời khai của phiên soạn, trừ chỗ ghi giờ máy)

### 0.1 Hai chỗ ghi thuộc packet

| # | hàm | dòng (`3b64746`) | đích | cách ghi hiện tại |
|---|---|---|---|---|
| W4 | `cmd_bootstrap` (1717), nhánh `bundle.get("gws_cred")` | 1780–1790 | `cfgdir/credentials.json`, `cfgdir` = `$GOOGLE_WORKSPACE_CLI_CONFIG_DIR` hoặc `~/.config/gws` (1781) | `os.makedirs(cfgdir)` (1782), `open("wb")` (1784) ghi `bundle["gws_cred"].encode("utf-8")` (1785) không nguyên tử, `chmod` sau (1787) — packet 1 KHÔNG chạm |
| W5 | `_gws_auth_load` (định nghĩa 1911) | 1930–1939 | như W4 | cùng mẫu (1931–1934); dữ liệu là `bytes` từ `store.decrypt` (1927) — packet 1 KHÔNG chạm |

Người gọi W5: `cmd_gws_auth_load` (1942–1953, nhánh lỗi in `✗`, rc 2), `cmd_gws_bootstrap_cowork` (2317, 2374), `tl_core/ops_misc.py`
(592). Không ai trong số đó ghi riêng. `cfgdir` đến THẲNG từ biến môi trường, có thể tương đối hoặc có hậu tố.

### 0.2 Phép đo

| phép | dựng | kết quả |
|---|---|---|
| E1 (04:51:21Z) | `_gws_auth_load`, `GOOGLE_WORKSPACE_CLI_CONFIG_DIR=<kho git tạm>/gwscfg` | `(True, …/kho/gwscfg/credentials.json)`; `git status --porcelain` = `?? gwscfg/credentials.json` |
| E2 (04:51:21Z) | `cmd_bootstrap --env code`, bundle có `gws_cred`, cùng biến | rc 0; porcelain = `?? gwscfg/credentials.json` |
| S4 (05:17:57Z) | `_ghi_nguyen_tu_0600` trên đích là symlink vào kho; trên đích là hardlink | tệp được trỏ tới giữ nguyên; hardlink còn lại giữ nội dung cũ ⇒ thay nguyên tử không ghi xuyên tệp cuối |
| S5 (05:17:57Z) | `_ghi_nguyen_tu_0600` với thư mục cha là symlink ra ngoài | tệp được tạo ở thư mục đích của symlink ⇒ thay nguyên tử KHÔNG chặn thành phần thư mục là liên kết |
| L1 (05:31:18Z, `scratchpad/rig433/do_luot2.py`) | `alias` là symlink tới thư mục; `os.lstat` | symlink cho `alias` (tuyệt đối, tương đối); thư mục THƯỜNG cho `alias/`, `alias/.`, `alias/./`, `alias//` (tuyệt đối) và `alias/`, `alias/.` (tương đối) |
| L2 (05:31:18Z) | `os.path.normpath("T/alias/../x")` | `T/x` — gộp `..` theo từ vựng, khác đường kernel đi khi `alias` là symlink |

Review Codex lượt 2 của đặc tả gốc (05:30:13Z) đo độc lập E1/E2/S4/S5 và đặt yêu cầu cho L1: kiểm thành phần bằng đường tuyệt
đối dựng từ cwd cố định, chính sách `.`/`..`, đường kiểm == đường ghi, ca root symlink tuyệt đối/tương đối/`/`/`/.`, ca dương
cfgdir tương đối, và vế Windows không dựa `os.path.isjunction` (chỉ có từ Python 3.12; tài liệu kho khai Python ≥ 3.11,
`SKILL.md:161`). `stat.FILE_ATTRIBUTE_REPARSE_POINT` và `st_file_attributes` có trên Windows từ Python 3.5.

### 0.3 Ràng buộc kề bên

- Neo PD của `ops/cloud_agent_creds_test.py` (bảng 796–806) và chuỗi khoá của `wp727_tl_gws_refresh`: như §0.4 của đặc tả
  `NLM-GWS-DICH-NGOAI-KHO-r1.md`; mã mới không chứa nguyên văn chuỗi neo PD nào. Fragment của packet 1
  (`wp433_nlm_gws_dich_ngoai_kho.py`) có đột biến neo vào `tl_gws.py`; packet này không được làm neo nào của nó khớp ≠ 1 lần.
- Bước CI `bundled-fragment check` kiểm bundled committed trên PR; tái sinh riêng bundled là đủ cho bước ấy xanh, manifest
  committed chỉ bị kiểm trên master (đo trong đặc tả packet 1, §0.4, 05:31:35Z–05:31:48Z).
- Driver `bundle_fragment_check.py` đọc stdout của tiến trình con làm JSON: fragment in ra stderr.
- Nền test: đo lại trên base thật (sau packet 1) — `--selftest`, `ops/cloud_agent_creds_test.py`, `ruff --select F` trên
  `scripts/tl_gws.py`; tiêu chí là DELTA.

### 0.4 Trạng thái sau packet 1 (đo trên `3b64746`)

- `_kiem_dich_ghi(dich, goc, thanh_phan)` có ở 1173–1187: luật (a) `_trong_kho_git(dirname(dich))`, luật (b) chỉ `stat.S_ISLNK` (1183);
  docstring 1175–1176 ghi rõ "junction/reparse Windows chưa chặn". Vế reparse CHƯA có ⇒ điều kiện §6 về M6 thoả.
- Hợp đồng lỗi packet 1: năm cụm `nằm trong kho git` (1179), `là liên kết tượng trưng` (1184), `dữ liệu không hợp lệ`, `ngoài danh sách
  cho phép` (1193–1202), `ghi lỗi` (1772, 1800); chi tiết `repr(...)[:200]`.
- W6 (1754–1774): packet 1 thêm chốt đích (1761) và ghi nguyên tử (1769), CHƯA có kiểm DỮ LIỆU: `os.environ["TL_TOKEN"]` gán thẳng (1755)
  trước `TL_WEBAPP` (1757); `existing.update` (1768) trên giá trị parse được bất kỳ; `json.dumps(...).encode` (1769) chỉ nằm trong
  `except OSError` (1771) ⇒ `UnicodeEncodeError` lan ra. Đúng tiền đề của M7.
- Fragment packet 1 `scripts/test_fragments/wp433_nlm_gws_dich_ngoai_kho.py`: 353 dòng, 31 mục `db_*`, rig `_Rig` (55–128) tự chứa.
  Mốc kích thước packet 1 (numstat `641108c..3b64746`): `tl_gws.py` +94/−42, fragment +353, bundled +1.
- Phép đo M1 mới (2026-11-19T04:52:30Z, `python3 -I`, `ntpath` trên Python 3.11.18 / 3.12.3 / 3.13.18, ba bản cùng kết quả trừ `\fake`):
  `splitdrive("\\\\server\\share")` = (`\\server\share`, `""`), `isabs` True; `\\server\share\x` ⇒ (`\\server\share`, `\x`);
  `//server/share/x` ⇒ (`//server/share`, `/x`); `\\?\C:\x` ⇒ (`\\?\C:`, `\x`); `\\.\pipe\x` ⇒ (`\\.\pipe`, `\x`); `\\server` ⇒
  (`\\server`, `""`); `C:` ⇒ (`C:`, `""`), `isabs` False; `\fake` ⇒ `isabs` True trên 3.11/3.12, False trên 3.13.
- Phép đo env (cùng lúc, Linux, ba bản Python): `os.environ[...] = "\udc80"` THÀNH CÔNG (`os.environb` = `b"\x80"`, surrogateescape);
  `"\ud800"` ⇒ `UnicodeEncodeError … surrogates not allowed`; `"a\x00b"` ⇒ `ValueError: embedded null byte`. `"\udc80".encode("utf-8")` và
  `"\ud800".encode("utf-8")` đều ⇒ `UnicodeEncodeError … surrogates not allowed`. Windows chưa đo.

## 1. `write_set`

```
scripts/tl_gws.py
scripts/test_fragments/wp433_gws_cred_dich_ngoai_kho.py
scripts/tl_test_fragments_bundled.py
```

`scripts/tl_test_fragments_bundled.py` theo **quyết định của chủ kho ngày 18-11-2026** (phương án B): worker mang riêng tệp
ấy, chỉ sinh bằng `generate_bundled_module_bytes(scripts/test_fragments)`, KHÔNG mang `RELEASE_MANIFEST.json` — ngoại lệ so với
`docs/PROTOCOL_DA_PHIEN.md` dòng 864–868. **Điều kiện trước khi cấp lease (E2 — chờ chủ kho):** comment của chủ kho trên Issue #433 cấp ngoại lệ
ấy nêu đúng `packet_id` `GWS-CRED-DICH-NGOAI-KHO`, đúng một tệp `scripts/tl_test_fragments_bundled.py` và sha256 của đặc tả
này đã đóng băng; lease trỏ tới URL comment. Comment cấp cho packet 1 không phủ packet này. Phiên land tái sinh
`RELEASE_MANIFEST.json` trong commit land.

## 2. `ngoai_pham_vi`

- W1–W3, W6 (trừ phần kiểm DỮ LIỆU W6 — M7 của packet này, chuyển 2026-11-18T06:53:23Z để giữ trần packet 1), điều kiện `.claude`,
  `_kiem_jar_nlm`: packet `NLM-GWS-DICH-NGOAI-KHO`. Thân `_kiem_dich_ghi` chỉ được sửa ĐÚNG MỘT
  chỗ: thêm vế reparse point vào phép nhận diện liên kết (M6). Mọi sửa khác của thân hàm ⇒ luật dừng §6.
- Mục 3, mục 8 của #433: chủ kho quyết định 18-11-2026 là lỗi thời / theo thiết kế. Không làm.
- Không chốt binary gws, `bindir`, `_persist_local_bin_on_path` (không ghi credential từ bundle).
- Không sửa THÂN `_trong_kho_git`/`_ghi_nguyen_tu_0600`; không sửa `ops/**`, `.github/**`, `scripts/tl_selftest.py`,
  `RELEASE_MANIFEST.json`, `changelog.d/*`, `VERSION`, `CHANGELOG.md`, `SKILL.md`.
- Không chống đối thủ ĐỒNG THỜI cùng uid (đổi cwd/thư mục giữa lúc kiểm và lúc ghi).
- Windows: không có CI Windows bắt buộc; quyền 0600 không đo bằng `stat` trên Windows.

## 3. `muc_tieu`

| # | mục tiêu | tệp |
|---|---|---|
| M1 | `_duong_dich_chuan(p)` trả `(đường_tuyệt_đối, thanh_phan_tu_goc)` hoặc lý do. Từ đường thô `p`: (1) đọc `cwd = os.getcwd()` MỘT lần ở đầu lệnh; `p` tương đối thì ghép `os.path.join(cwd, p)` — KHÔNG `abspath`, `normpath`, `realpath` (§0.2 L2); (2) tách ổ đĩa (`splitdrive`), tách thành phần theo `sep` và `altsep` của mô-đun đường đang dùng; dạng được NHẬN là DANH SÁCH CHO PHÉP, mọi dạng khác bị từ chối `đường không hợp lệ`. Với `_path` là `posixpath`: (P1) `/x` (tuyệt đối), (P2) tương đối. Với `_path` là `ntpath`, phân loại CHỈ bằng `splitdrive` và ký tự đầu phần sau ổ, KHÔNG gọi `isabs` (đo §0.4: `isabs("\\fake")` khác nhau giữa 3.11/3.12 và 3.13): (N1) ổ khớp `fullmatch(r"[A-Za-z]:")` VÀ phần sau ổ bắt đầu bằng `\` hoặc `/` ⇒ tuyệt đối theo ký tự ổ; (N2) ổ khớp `fullmatch(r"[\\/]{2}[^\\/?.][^\\/]*[\\/][^\\/]+")` (UNC `\\server\share`, máy chủ không bắt đầu bằng `?` hay `.`, share khác rỗng) VÀ phần sau ổ RỖNG hoặc bắt đầu bằng `\`/`/` ⇒ tuyệt đối UNC (gốc share `\\server\share` được nhận); (N3) ổ rỗng VÀ đường không bắt đầu bằng `\`/`/` ⇒ tương đối, ghép cwd. Bị từ chối (liệt kê đủ đường vào): (R1) ổ chữ cái mà phần sau ổ rỗng hoặc không bắt đầu bằng phân cách (`C:`, `D:fake` — theo ổ); (R2) ổ rỗng mà đường bắt đầu bằng phân cách (`\fake` — gốc ổ hiện tại); (R3) đường thiết bị `\\?\…`, `\\.\…` (ổ không khớp N2 vì máy chủ bắt đầu bằng `?`/`.`); (R4) UNC thiếu share (`\\server`); (R5) mọi ổ khác không khớp N1/N2. Với `posixpath` chỉ có `/x` (tuyệt đối) và tương đối. Hai dạng Windows còn lại bị từ chối với `đường không hợp lệ`: tương đối THEO Ổ (`D:fake` — ổ có, không gốc; đo 06:20:01Z bằng `ntpath`: `isabs` False, `splitdrive` = `('D:', 'fake')`, và review lượt 4 đo `join('C:\\cwd', 'D:fake')` = `D:fake`) và tuyệt đối THEO GỐC Ổ HIỆN TẠI (`\fake` — không ổ, có gốc; `isabs` False). Để đo được trên mọi nền, hàm nhận tham số nội bộ `_path` (mặc định `os.path`) và `cwd` tuỳ chọn; bỏ thành phần rỗng (hậu tố `/`, `//`) và `.`; (3) còn `..` ⇒ từ chối với cụm mới `đường không hợp lệ`; (4) dựng lại đường tuyệt đối. Đường dựng ở (4) là đường DUY NHẤT được kiểm và được truyền cho `_ghi_nguyen_tu_0600`, và là đường W5 trả về (đường kiểm == đường ghi == đường báo). | `scripts/tl_gws.py` |
| M2 | W4 và W5: chuẩn hoá `cfgdir` bằng M1, rồi `_kiem_dich_ghi(<cfgdir chuẩn>/credentials.json, <cfgdir chuẩn>, ("credentials.json",))` TRƯỚC `makedirs` — luật (b) của packet 1 khi ấy `lstat` chính `cfgdir` chuẩn (đã bỏ hậu tố), nên `alias/`, `alias/.` bị nhận đúng là liên kết. W4 còn đòi `bundle["gws_cred"]` là `str` và `encode("utf-8")` thành công, sai ⇒ `dữ liệu không hợp lệ`. Được phép thì ghi bằng `_ghi_nguyen_tu_0600(dest, data)` thay `makedirs` + `open("wb")` + `chmod`. Ngoài kho thì nội dung tệp như base. | `scripts/tl_gws.py` |
| M3 | Hợp đồng lỗi: theo M4 của packet 1 (gồm định dạng dòng cố định `[thẻ] ✗ <cụm>: <chi tiết repr>`, nhận diện bằng `fullmatch` phần đầu dòng), thêm cụm thứ sáu `đường không hợp lệ`; `cfgdir` và mọi đường nội suy đi qua `repr` nên `\n` trong đường không sinh dòng thứ hai. W4 bị từ chối hoặc lỗi ghi ⇒ ĐÚNG MỘT dòng `[bootstrap] ✗ …` ra stderr, `degraded = True`, chạy tới đúng một dòng `agent_creds:`, rc 1 (rc 4 khi `--require-agent-creds` với agent chưa `ĐÃ NẠP`, như base); dòng `✓ gws cred → …` KHÔNG in. W5 trả `(False, <lý do chứa cụm>)`; `cmd_gws_auth_load` in một dòng `✗` và trả 2 như nhánh lỗi sẵn có. Không ngoại lệ thoát ra: kiểu và encode của `gws_cred` kiểm TRƯỚC; lời ghi W4/W5 chỉ bắt `OSError` (§4b). Tập ngoại lệ khai gắn với từng LƯỢT gọi (không theo ca) = cột "ngoại lệ khai" của bảng §4b; ngoại lệ ngoài tập của lượt đang chạy ⇒ `ngoai_le_la`. | `scripts/tl_gws.py` |
| M6 | Thêm vào thân `_kiem_dich_ghi` (packet 1 chỉ nhận diện liên kết bằng `S_ISLNK`) vế: một đường cũng là liên kết khi `getattr(st, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT` (Windows, có từ Python 3.5; phủ junction và mọi reparse point; không dùng `os.path.isjunction`, chỉ có từ 3.12). Chỉ đổi biểu thức nhận diện; chữ ký, thứ tự luật và hợp đồng lỗi giữ nguyên. Áp cho MỌI caller, nên từ lúc packet này land, W1–W3 và W6 của packet 1 cũng chặn junction. Phép đo: N3c (giả lập, mọi nền, đi qua W5 và một lời gọi W1), N4 (junction thật). | `scripts/tl_gws.py` |
| M7 | Kiểm DỮ LIỆU của W6 trong `cmd_bootstrap` (chuyển từ packet 1, mã + ca + đột biến): (a) `token` và `webappUrl` (nếu có) là `str`, encode được UTF-8 và KHÔNG chứa `\x00`, kiểm CẢ HAI TRƯỚC bất kỳ phép gán `os.environ` nào (đo 06:13:09Z: surrogate ⇒ `UnicodeEncodeError` ở `os.environ`; 06:20:01Z: NUL ⇒ `ValueError: embedded null byte`; base gán `TL_TOKEN` trước `TL_WEBAPP`); sai ⇒ một dòng `[bootstrap] ✗ dữ liệu không hợp lệ: …`, không đặt hai biến, không đọc/ghi config, `degraded = True`; (b) config cũ parse được mà không phải `dict` (đo: `.update` ⇒ `AttributeError`) xử như config không parse được của base: `existing = {}` rồi ghi, không dòng lỗi; (c) `json.dumps(existing, ensure_ascii=False).encode("utf-8")` ném `UnicodeEncodeError` (khoá khác token mang surrogate) ⇒ `dữ liệu không hợp lệ`, không ghi, `TL_TOKEN` vẫn đặt, `degraded = True`. W6 bắt `UnicodeEncodeError` CHỈ quanh bước (c). | `scripts/tl_gws.py` |
| M4 | Fragment `scripts/test_fragments/wp433_gws_cred_dich_ngoai_kho.py`, `TEST_ID = "wp433_gws_cred_dich_ngoai_kho"`, `run(tl_module)`, cùng khuôn với fragment packet 1 (M5 của nó) nhưng tự chứa (không import fragment khác: gói nạp từng fragment riêng): rig HOME/`USERPROFILE`/`CODEX_HOME`/`GOOGLE_WORKSPACE_CLI_CONFIG_DIR`/`TL_*`/cwd tạm khôi phục trong `finally`; thay `AGENT_CREDS_FILEID`/`TL_AGENT_CREDS_FILEID`, `_public_curl_bytes`, `_gas`, `_secrets_fetch`, `load_creds`, `_ensure_nlm_installed`, `cmd_gws_bootstrap_cowork`, `gws_exe` bằng đồ giả có đếm; lớp chặn `subprocess`/`urlopen` (dấu `MANG_BI_CHAN`) chỉ trong cửa sổ gọi `tl_gws`; mọi đầu ra ra STDERR; đột biến trên bản sao trong bộ nhớ, neo khớp đúng 1 lần, `compile`/`bind` thành công, phân hạng `TinHieuChotCa(AssertionError)` theo (ca, nhãn), cùng luật "ngoại lệ dự kiến" của M5 packet 1 (bắt tập đóng ở biên lời gọi, đổi thành nhãn; ngoài tập thì lan ra, không tín dụng). Ca và đột biến viết dạng bảng. | fragment |
| M5 | Tái sinh `scripts/tl_test_fragments_bundled.py` bằng `generate_bundled_module_bytes(scripts/test_fragments)`; không sửa tay; không đụng `RELEASE_MANIFEST.json`. | bundled |

## 4. `nghiem_thu`

Ký hiệu như đặc tả packet 1 §4 (K, SENT = `SENTINEL-wp433-gws-…`, sạch(K), stderr đúng). "Fixture gws chuẩn" =
`cmd_bootstrap --env code --no-nlm --no-gws`, HOME ngoài mọi kho, bundle có `token` và `gws_cred`, KHÔNG `nlm_auth`, agent giả
`KHÔNG CẤU HÌNH`, `gws_exe` giả trả có; với `cfgdir` ngoài kho nó trả rc 0 — nên mọi rc 1 trong ca dùng fixture này chỉ đến từ W4.

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| N1 | `w4_trong_kho` (fixture gws chuẩn) và `w5_trong_kho` (`_gws_auth_load`, `_public_curl_bytes` giả): `GOOGLE_WORKSPACE_CLI_CONFIG_DIR = K/gwscfg` ⇒ [`ma`] W4 rc 1, W5 `(False, …)`; [`stderr`] W4 đúng một dòng `nằm trong kho git`, W5 lý do chứa cụm ấy; [`sach`] `K/gwscfg` không tồn tại, sạch(K); [`agent_creds`] W4 một dòng `agent_creds:`; SENT không trong đầu ra. Vế âm base: §0.2 E1, E2. | `db_w4_bo_chot`, `db_w5_bo_chot` (bỏ lời gọi `_kiem_dich_ghi` tại đúng một chỗ) ⇒ chỉ ca của chỗ ấy, nhãn `sach`. `db_w4_quen_degraded` (nhánh từ chối W4 không đặt `degraded`) ⇒ `w4_trong_kho`, nhãn `ma`. |
| N2w | `duong_windows_ba_dang` (mọi nền): gọi thẳng `_duong_dich_chuan(p, cwd="C:\\cwd", _path=ntpath)` ⇒ [`o_tuong_doi`] `D:fake` bị từ chối `đường không hợp lệ`; [`goc_o`] `\fake` bị từ chối `đường không hợp lệ`; [`tuyet_doi_o`] `D:\fake` được nhận, trả `D:\fake`; [`tuong_doi`] `fake` được nhận, trả `C:\cwd\fake`; [`unc_goc`] `\\server\share` và `\\server\share\x` được nhận, trả nguyên dạng đã dựng lại; [`thiet_bi`] `\\?\C:\x`, `\\.\pipe\x` bị từ chối; [`unc_thieu_share`] `\\server` bị từ chối; [`o_tran`] `C:` bị từ chối. Ca chạy trên Python 3.11–3.13 với cùng kết quả (không gọi `isabs`). | `db_cho_phep_theo_o` (dạng có ổ mà không gốc đi qua nhánh ghép cwd) ⇒ `o_tuong_doi`. `db_cho_phep_goc_o` (dạng có gốc mà không ổ được coi là tuyệt đối) ⇒ `goc_o`. `db_tu_choi_unc_goc` (áp điều kiện "phần sau ổ bắt đầu bằng phân cách" của N1 cho cả UNC) ⇒ `unc_goc`. `db_nhan_thiet_bi` (bỏ ràng buộc máy chủ không bắt đầu bằng `?`/`.` ở N2) ⇒ `thiet_bi`. `db_unc_khong_can_share` (regex N2 cho phép share rỗng) ⇒ `unc_thieu_share`. |
| N2 | `w5_goc_bieu_dien`: `that` thư mục thật ngoài kho, `alias` symlink tới `that`, cwd = thư mục cha. Lần lượt `cfgdir` = `<tuyệt đối>/alias`, `<tuyệt đối>/alias/`, `<tuyệt đối>/alias/.`, `alias`, `alias/`, `alias/.` ⇒ [`goc_<i>`] `(False, …)` chứa `là liên kết tượng trưng`, `that` rỗng. `x/../that` ⇒ [`hai_cham`] `(False, …)` chứa `đường không hợp lệ`. Vế dương [`tuong_doi_thuong`]: `cfgthuong` (tương đối, chưa có) ⇒ `(True, d)` với `d == os.path.join(<cwd của ca>, "cfgthuong", "credentials.json")`, tệp đúng byte. `w4_goc_alias_cham`: fixture gws chuẩn với `cfgdir` = `<tuyệt đối>/alias/.` ⇒ [`goc_w4`] rc 1, một dòng `là liên kết tượng trưng`, `that` rỗng. | `db_lstat_tho` (W5 đưa chuỗi `cfgdir` thô vào `_kiem_dich_ghi` thay đường chuẩn) ⇒ nhãn `goc_1` (`alias/`). `db_w4_khong_chuan_hoa` (W4 dùng `cfgdir` thô) ⇒ `w4_goc_alias_cham`, nhãn `goc_w4`. `db_bo_cam_hai_cham` ⇒ `hai_cham`. `db_ghi_duong_tho` (kiểm đường chuẩn nhưng ghi và trả `os.path.join(cfgdir_thô, "credentials.json")`) ⇒ `tuong_doi_thuong` (đường trả về tương đối). |
| N3 | `w4_symlink_tep`: `cfgdir` ngoài kho, `cfgdir/credentials.json` là symlink tới `K/dich.json` (`CU`) ⇒ fixture gws chuẩn rc 1, [`dich_giu`] `K/dich.json` còn `CU`, [`stderr`] một dòng `là liên kết tượng trưng`. | `db_bo_symlink_cuoi` (luật (b) của `_kiem_dich_ghi` bỏ qua chính `dich`; neo trên thân hàm ở base thật) ⇒ nhãn `stderr` (thay nguyên tử đã giữ `dich_giu`, nên đột biến này đo riêng lớp từ chối). Ca và đột biến này CHUYỂN từ packet 1 (N6(1) cũ của nó) để giữ trần packet ấy. |
| N3b | Chuyển từ packet 1 (N5 cũ của nó) để giữ trần packet ấy — hai chuỗi của `_trong_kho_git` qua `_kiem_dich_ghi`: (1) `w5_chuoi_realpath`: `L` là symlink NGOÀI kho trỏ vào `K/sub`, `cfgdir` = `L/gws` (luật (b) không kiểm `L` vì nằm trên `goc`) ⇒ [`sach`] `(False, …)` chứa `nằm trong kho git`, sạch(K); (2) `w5_chuoi_tu_vung`: `lk` là symlink TRONG K trỏ ra T, `cfgdir` = `K/lk/gws` ⇒ [`tu_choi_tu_vung`] `(False, …)` chứa `nằm trong kho git`, T rỗng. | `db_chi_tu_vung` (trong `_kiem_dich_ghi`, thay lời gọi `_trong_kho_git` bằng phép đi lên chỉ trên `os.path.abspath`) ⇒ (1) `sach`. `db_chi_realpath` (chỉ `os.path.realpath`) ⇒ (2) `tu_choi_tu_vung`. Neo đặt trên thân `_kiem_dich_ghi` của base thật; KHÔNG sửa `_trong_kho_git` (PD7 canh). |
| N3c | M6, `reparse_gia_lap` (mọi nền) — `os.lstat` giả trả cho ĐÚNG đường `cfgdir` một kết quả có `st_mode` thư mục thường và `st_file_attributes = stat.FILE_ATTRIBUTE_REPARSE_POINT` (1024) ⇒ [`reparse`] W5 `(False, …)` chứa `là liên kết tượng trưng`, không tệp; [`reparse_w1`] cùng đồ giả cho `~/.notebooklm-mcp-cli/profiles/default`, jar của bundle chứa khoá LỒNG `profiles/default/cookies.json` (cùng `auth.json`) để W1 buộc phải đi qua tiền tố gắn bit ⇒ `cmd_nlm_auth_pull` rc 1, một dòng `là liên kết tượng trưng` (chứng minh vế mới áp cho caller của packet 1); đối chứng [`khong_bit`] `st_file_attributes = stat.FILE_ATTRIBUTE_DIRECTORY` (16) ⇒ `(True, …)`. | `db_bo_reparse` (neo trên nguồn candidate đã áp M6, như N4) ⇒ `reparse` và `reparse_w1` (cùng một mục bảng §4b, ba đích kể cả N4). `db_reparse_moi_thu` (mọi thuộc tính khác 0 là liên kết) ⇒ `khong_bit`. |
| N3d | Ca hồi quy cho nhánh MÃ KHÔNG ĐỔI của packet 1 (W1/W3 giữ nhánh định dạng base, W2 giữ điều kiện truthy — §2 của đặc tả packet 1), đặt ở đây để giữ trần packet ấy: `jar_rong_base` — (8) [`jar_rong_base`] hậu điều của nhánh định dạng sẵn có: W1 với `nlm_auth` = `{}` hoặc vắng ⇒ rc 1 và đúng dòng `⚠ bundle chưa có nlm_auth` của base (1652), không dòng `dữ liệu không hợp lệ`; W3 với jar `{}`, `[]`, `[["auth.json", "x"]]` ⇒ `(False, "nlm_cred rỗng/sai định dạng.")` nguyên văn base (1956); W2 với `nlm_auth` = `{}` ⇒ như base (không dòng nào về jar, rc 0 nếu phần khác thành công). (gọi `cmd_nlm_auth_pull`, `_nlm_auth_load`, `cmd_bootstrap` của base thật, cùng rig). | `db_w1_jar_rong_moi` (W1 đưa `{}` vào `_kiem_jar_nlm` thay nhánh base) ⇒ `jar_rong_base`. |
| N3e | `w5_duong_xuong_dong`: ký tự xuống dòng nằm trong CHÍNH đường được in — kho là thư mục `k\nho` (có `.git`), `cfgdir` = `k\nho/gws`, nên chi tiết lý do (đường kho do `_trong_kho_git` trả) chứa `\n` (đo 06:33:10Z trong thư mục tạm thật, `python3 -I` trên bản sao base: thư mục kho tên `k\nho` tạo được, `_trong_kho_git` trả đường kho CHỨA `\n`, dòng dựng không `repr` tách thành 2 dòng, có `repr` 1 dòng) ⇒ [`mot_dong`] `cmd_gws_auth_load` (với `_gws_auth_load` thật) in ĐÚNG một dòng `✗`, phần lý do `fullmatch` `nằm trong kho git: .*` với chi tiết bằng `repr(<đường kho>)`, rc 2; Điều kiện nền: POSIX dựng kho THẬT `k\nho`; Windows không dựng được tên ấy (review lượt 7: `ntpath.isreserved('k\nho')` đúng) nên trong cửa sổ gọi thay `_trong_kho_git` trên module bằng đồ giả trả đường kho THẬT của ca nối thêm `\nx` cho đúng đường đích của ca (đường khác đi hàm thật), với CÙNG hậu điều. Ca chạy trên MỌI nền, không vào `bỏ_qua` hay `chỉ_windows`. `w4` cùng `cfgdir` ⇒ stderr đúng một dòng từ chối. | `db_khong_repr_gws` (W4/W5 nội suy đường thô) ⇒ `mot_dong`. |
| N4 | `w5_reparse_windows`, CHỈ khi `os.name == "nt"`: `cfgdir` là junction thật (`mklink /J` qua `cmd /c` ngoài cửa sổ chặn) trỏ ra T ⇒ [`junction`] `(False, …)` chứa `là liên kết tượng trưng`, T rỗng. Trên POSIX ca thuộc nhóm `chỉ_windows`, không tính `bỏ_qua`. Đo native trên máy Windows của chủ kho theo `ADR-0057`–`0059`; không đo được thì hồ sơ land ghi vế này `KHÔNG ĐO ĐƯỢC`. Đây là ca junction THẬT (hành vi hệ điều hành) cho vế reparse point của `_kiem_dich_ghi`; ca giả lập ở N3c. | `db_bo_reparse` (neo: vế `FILE_ATTRIBUTE_REPARSE_POINT` do M6 thêm, trên NGUỒN CANDIDATE đã áp M6 — base thật không có vế ấy, §6; cùng một mục trong bảng đột biến với N3c, hai ca đích ghi riêng; luật (b) chỉ còn `S_ISLNK`) ⇒ nhãn `junction`, chỉ Windows. Lời khai "junction không cho `S_ISLNK`" chưa đo (§8). |
| N5 | Vế dương nguyên tử, mỗi chỗ một ca — `w4_nguyen_tu`, `w5_nguyen_tu`: `cfgdir` ngoài kho có sẵn `credentials.json` cũ; bọc `os.replace` bằng bộ quan sát ghi nhận mọi lời gọi; SAU khi writer trả về, [`nguyen_tu`] lọc lời gọi có ĐÍCH = `credentials.json`: đúng MỘT, nguồn cùng thư mục, lúc thay đích vẫn là bản cũ, quyền nguồn 0600 (chỉ POSIX); rồi tệp đúng byte, quyền 0600 CHỈ kiểm trên POSIX (`os.name != "nt"`, như packet 1 N2 và §2); W4 rc 0 và in `✓ gws cred → …`. Hardlink: `credentials.json` là hardlink của H (`CU`) ⇒ [`ban_kia_giu`] H còn `CU`. | `db_w4_khong_nguyen_tu`, `db_w5_khong_nguyen_tu` (về `makedirs` + `open("wb")` + `chmod`) ⇒ chỉ ca của chỗ ấy, nhãn `nguyen_tu` (0 lời gọi tới đích). |
| N6 | `w4_du_lieu_sai_dang`, hai lượt: `N6.kieu` — `gws_cred` là số; `N6.surrogate` — `gws_cred` chứa surrogate đơn (chuỗi thoát JSON dựng trong bytes rồi mã hoá) ⇒ [`kieu`], [`surrogate`] rc 1, một dòng `dữ liệu không hợp lệ`, không tệp `credentials.json`, không tệp tạm, không ngoại lệ. | `db_w4_bo_kiem_encode` (chỉ kiểm `str`) ⇒ `surrogate`. `db_w4_bo_kiem_kieu` ⇒ `kieu`. |
| N7 | `chung_hop_dong_loi`: (1) [`require`] `w4_trong_kho` kèm `--require-agent-creds` ⇒ rc 4, dòng từ chối vẫn có, một `agent_creds:` (cũng là phép đo precedence rc 4 mà packet 1 chuyển sang đây); (2) `os.replace` giả ném `OSError` CHỈ khi đích = `credentials.json`: [`oserror_w4`] fixture gws chuẩn ⇒ rc 1, một dòng `[bootstrap] ✗ … ghi lỗi`, không dòng `✓ gws cred`, không tệp tạm sót, bản cũ giữ byte; [`oserror_w5`] lượt `N7.2-W5a`: `_gws_auth_load` ⇒ `(False, …)` chứa `ghi lỗi`; lượt `N7.2-W5b`: `cmd_gws_auth_load` (với `_gws_auth_load` thật, đồ giả `os.replace` ấy) ⇒ rc 2, một dòng `✗`; lượt `N7.2-W4` là vế `oserror_w4`; (3) [`stderr`] mọi ca từ chối của N1–N6 có stderr đúng. Thêm: `python3 ops/cloud_agent_creds_test.py` trên head `TONG: DAT`, `PD*` vẫn `GIET`, từng ca bằng base; fragment packet 1 vẫn ĐẠT (không neo nào lệch). | `db_w4_oserror_lan`, `db_w5_oserror_lan` (bỏ `except OSError` tại đúng một chỗ) ⇒ `oserror_w4`, `oserror_w5`. `db_w4_in_hai_dong` (thêm dòng stderr không chứa cụm) ⇒ `stderr`. `db_require_thua_rc1` ⇒ `require`. |
| N8 | Tự kiểm như N10 của packet 1: (a) mỗi đột biến giết đúng (ca, nhãn), W4 và W5 có ca đích riêng; (b) MỘT dòng tổng kết RA STDERR `[wp433_gws_cred_dich_ngoai_kho] CA: dự_kiến=a chạy=b đạt=c bỏ_qua=d chỉ_windows=w · DOT BIEN: dự_kiến=e chạy=f giết_đúng=g bỏ_qua=h chỉ_windows=v · HONG: i`; `run` True chỉ khi `b == c`, `f == g`, `i == 0`, `a == b + d + w`, `e == f + h + v`; trên POSIX `d == h == 0`; N3e chạy trên mọi nền (Windows giả lập `_trong_kho_git`), không vào `bỏ_qua` hay `chỉ_windows`; (c) đột biến tự kiểm: `AttributeError` qua `except` đổi kiểu ⇒ TÍN DỤNG GIẢ, chỉ thêm chú thích ⇒ SỐNG SÓT; (d) neo 0/2 lần hoặc không `compile` ⇒ `HONG`; (e) stdout của `run` rỗng. | Trên cây tạm: đổi ca đích `db_w5_bo_chot` sang `w4_trong_kho` ⇒ False; TẮT nhãn `goc_1` của `w5_goc_bieu_dien` ⇒ `db_lstat_tho` không giết đúng nhãn ⇒ False; neo khớp 2 lần ⇒ `HONG: 1`, False; ép bỏ qua ca symlink trên POSIX ⇒ False; in tổng kết ra stdout ⇒ (e) đỏ. (f) `tu_kiem_sai_luot`: khai lượt đích của §4b dòng 26 là `W6.token` ⇒ ngoại lệ khớp loại + dấu ở lượt `W6.encode` ⇒ không giết đúng ⇒ False. |
| N9w6 | `w6_du_lieu`, fixture gws chuẩn (HOME ngoài kho), các lượt: `W6.token` — `token` chứa surrogate đơn NGOÀI dải surrogateescape (`\ud800`, dựng bằng chuỗi thoát JSON) ⇒ [`token_hong`] rc 1, một dòng `dữ liệu không hợp lệ`, `TL_TOKEN` không đặt, config cũ giữ byte, một `agent_creds:`; `W6.encode` — `rootFolderId` chứa surrogate ⇒ [`surrogate_config`] rc 1, một dòng, `TL_TOKEN` đặt, config cũ giữ byte; `W6.dict_a`/`_b`/`_c` — config cũ `[]`/`null`/`"s"` ⇒ [`config_khong_dict`] rc 0, stderr rỗng, config sau lượt là `dict` mang `token`; `W6.nul` — hai biến đặt sẵn, `webappUrl` chứa `\x00` ⇒ [`env_nul`] rc 1, một dòng, cả hai biến giữ giá trị trước lượt. | §4b dòng 25–29. |
| N9 | Exact head: `--selftest` ĐẠT N/N hai số bằng nhau trên clone thật, N = N_base + 1, DELTA = 0 ca đỏ mới (base và head trong CÙNG một lệnh); `test-fragments-check --json` ⇒ `ok: true`; `bundle_fragment_check.py --json` ⇒ `ok: true`, `failed: []`. | Không tái sinh bundled ⇒ `TEST_ID_SET_MISMATCH`; sửa tay bundled ⇒ `GENERATED_BUNDLE_STALE`. |
| N10 | Lane worker `ci.yml` (521–532 ở `641108c`, đo lại) tại chỗ: `release-manifest --root . --out <tạm>` rồi `release-verify <tạm> --root . --strict` ⇒ `ok: true`, `expected_file_count == checked_file_count`. Manifest committed lệch bundled trên PR head; phiên land tái sinh manifest trong commit land, hồ sơ land ghi `release-verify RELEASE_MANIFEST.json --strict` `ok: true` trên commit ấy. | Sửa tay một tệp trong gói sau khi sinh manifest tạm ⇒ `ok: false`. |
| N11 | Exact head, lệnh + rc + bằng chứng dương: `ruff check --select F` delta = 0 trên `scripts/tl_gws.py`, 0 trên fragment và bundled; `git diff --check` sạch; `doctrine-scan`, `adr-song` rc 0; dưới `set -o pipefail`: `git diff --numstat <base>..<head> > numstat.txt` (rc ≠ 0 ⇒ đỏ), (i) đúng 3 dòng, (ii) mỗi dòng khớp `^[0-9]+\t[0-9]+\t<đường>$`, tập đường == §1, (iii) tổng cột thêm ≤ 450. | Tên chưa định nghĩa ⇒ delta ≠ 0. Tệp ngoài §1 ⇒ (i)/(ii). Trần: cùng lệnh trên `numstat.txt` dựng tay đúng 3 dòng, đúng tập đường §1, cột thêm tổng 450 ⇒ (iii) XANH; đổi một cột cho tổng 451 ⇒ (iii) ĐỎ. `<base>` không tồn tại ⇒ rc 128 ⇒ đỏ. Đầu vào rỗng ⇒ (i). `doctrine-scan`/`adr-song`: gate kế thừa, chưa có phép đỏ riêng (L3). |


### 4b. Bảng đột biến — NGUỒN DUY NHẤT (thắng mọi mô tả đột biến rải trong §4)

Ký hiệu và luật như §4b của đặc tả packet 1, gồm luật LƯỢT GỌI: tập ngoại lệ khai gắn với từng lượt; ngoại lệ ngoài tập của lượt đang
chạy ⇒ ca dừng với nhãn `ngoai_le_la` (không bao giờ là nhãn đích); đột biến chỉ GIẾT khi tín hiệu mang đúng (ca, lượt, nhãn). Ràng buộc cài đặt: kiểm kiểu/encode của `gws_cred` làm TRƯỚC khi ghi; lời ghi W4/W5 chỉ bắt `OSError`; đồ giả `os.replace`
ném `OSError("wp433-oserror")`; fixture `hai_cham` có sẵn thư mục thật `x` (đo 06:42:22Z: `os.makedirs("…/x/../that")` không ném,
tự tạo `x` nếu vắng — có sẵn `x` để cơ chế không phụ thuộc điều ấy). Đột biến neo trên NGUỒN CANDIDATE (đã áp M1, M2, M6).

| # | đột biến | ca đích | nhãn | cơ chế | ngoại lệ khai ở biên ca | tự kiểm |
|---|---|---|---|---|---|---|
| 1 | `db_w4_bo_chot` | `w4_trong_kho` | `sach` | H | — | lập luận (§0.2 E2) |
| 2 | `db_w5_bo_chot` | `w5_trong_kho` | `sach` | H | — | lập luận (§0.2 E1) |
| 3 | `db_w4_quen_degraded` | `w4_trong_kho` | `ma` | H | — | lập luận |
| 4 | `db_lstat_tho` | `w5_goc_bieu_dien` | `goc_1` | H | — | đo 05:31:18Z: `lstat("alias/")` không phải symlink |
| 5 | `db_w4_khong_chuan_hoa` | `w4_goc_alias_cham` | `goc_w4` | H | — | đo 05:31:18Z: `lstat("alias/.")` không phải symlink |
| 6 | `db_bo_cam_hai_cham` | `w5_goc_bieu_dien` | `hai_cham` | H | — | đo 06:42:22Z: `makedirs("x/../that")` không ném |
| 7 | `db_ghi_duong_tho` | `w5_goc_bieu_dien` | `tuong_doi_thuong` | H | — | lập luận |
| 8 | `db_cho_phep_theo_o` | `duong_windows_ba_dang` | `o_tuong_doi` | H | — | đo 06:42:22Z: `ntpath.join("C:\\cwd", "D:fake")` = `D:fake`, không ném |
| 9 | `db_cho_phep_goc_o` | `duong_windows_ba_dang` | `goc_o` | H | — | đo 06:42:22Z: `ntpath.join("C:\\cwd", "\\fake")` = `C:\\fake`, không ném |
| 10 | `db_chi_tu_vung` | `w5_chuoi_realpath` | `sach` | H | — | lập luận |
| 11 | `db_chi_realpath` | `w5_chuoi_tu_vung` | `tu_choi_tu_vung` | H | — | lập luận |
| 12 | `db_bo_symlink_cuoi` | `w4_symlink_tep` | `stderr` | H | — | lập luận (§0.2 S4) |
| 13 | `db_bo_reparse` | `reparse_gia_lap` (N3c) | `reparse` và `reparse_w1` (jar có khoá lồng `profiles/default/cookies.json`) | H | — | đo 06:42:22Z: `1024 & REPARSE` ≠ 0 |
| 13b | (cùng mục 13) | `w5_reparse_windows` (N4, chỉ Windows) | `junction` | H | — | chưa đo (Windows) |
| 14 | `db_reparse_moi_thu` | `reparse_gia_lap` | `khong_bit` | H | — | đo 06:42:22Z: `16 & REPARSE` = 0 |
| 15 | `db_w4_khong_nguyen_tu` | `w4_nguyen_tu` | `nguyen_tu` | H | — | lập luận |
| 16 | `db_w5_khong_nguyen_tu` | `w5_nguyen_tu` | `nguyen_tu` | H | — | lập luận |
| 17 | `db_w4_bo_kiem_kieu` | `w4_du_lieu_sai_dang` | `kieu` | E — `.encode` trên số | lượt `N6.kieu`: `AttributeError` chứa `'int' object has no attribute 'encode'` | đo: `(5).encode` ⇒ đúng thông điệp |
| 18 | `db_w4_bo_kiem_encode` | `w4_du_lieu_sai_dang` | `surrogate` | E — `encode` ở lời ghi | lượt `N6.surrogate`: `UnicodeEncodeError` chứa `surrogates not allowed` | đo: đúng thông điệp |
| 19 | `db_w4_in_hai_dong` | `chung_hop_dong_loi` | `stderr` | H | — | lập luận |
| 20 | `db_w4_oserror_lan` | `chung_hop_dong_loi` | `oserror_w4` | E | lượt `N7.2-W4`: `OSError` chứa `wp433-oserror` | lập luận (thông điệp do đồ giả đặt) |
| 21 | `db_w5_oserror_lan` | `chung_hop_dong_loi` | `oserror_w5` | E | lượt `N7.2-W5a` và `N7.2-W5b` (cùng nhãn đích): `OSError` chứa `wp433-oserror` | lập luận |
| 22 | `db_khong_repr_gws` | `w5_duong_xuong_dong` | `mot_dong` | H | — | đo 06:33:10Z: không `repr` ⇒ 2 dòng |
| 23 | `db_require_thua_rc1` | `chung_hop_dong_loi` | `require` | H | — | lập luận |
| 24 | `db_w1_jar_rong_moi` | `jar_rong_base` | `jar_rong_base` | H — `_kiem_jar_nlm({})` trả lý do, không ném | — | lập luận |
| 25 | `db_w6_bo_kiem_token` (chỉ bỏ kiểm encode của `token`) | `w6_du_lieu` | `token_hong` (lượt `W6.token`) | E hoặc H theo nền — gán `os.environ` với `\ud800`: POSIX ném (đo §0.4, ba bản Python); nếu nền không ném (Windows chưa đo) thì `TL_TOKEN` bị đặt ⇒ hậu điều `token_hong` đỏ (H) | lượt `W6.token`: `UnicodeEncodeError` chứa `surrogates not allowed` | đo 2026-11-19T04:52:30Z: `\udc80` KHÔNG ném trên POSIX (surrogateescape), `\ud800` ném — fixture dùng `\ud800` |
| 26 | `db_w6_bo_kiem_encode` (bỏ bắt quanh bước (c)) | `w6_du_lieu` | `surrogate_config` (lượt `W6.encode`) | E — tuần tự hoá | lượt `W6.encode`: `UnicodeEncodeError` chứa `surrogates not allowed` | đo 06:42:22Z: đúng thông điệp |
| 27 | `db_w6_bo_kiem_dict` | `w6_du_lieu` | `config_khong_dict` (lượt `W6.dict_a`) | E — `existing.update` | lượt `W6.dict_a`, `W6.dict_b`, `W6.dict_c`: `AttributeError` chứa `object has no attribute 'update'` | đo 06:42:22Z: ba giá trị ⇒ đúng thông điệp |
| 28 | `db_w6_bo_kiem_nul` (chỉ bỏ kiểm NUL) | `w6_du_lieu` | `env_nul` (lượt `W6.nul`) | E hoặc H theo nền — gán `TL_WEBAPP`; không ném thì biến bị đổi ⇒ hậu điều `env_nul` đỏ | lượt `W6.nul`: `ValueError` chứa `embedded null` (POSIX đo được `embedded null byte`; thông điệp Windows chưa đo nên dấu lấy tiền tố chung) | đo 06:20:01Z, 06:42:22Z, 2026-11-19T04:52:30Z |
| 29 | `db_w6_gan_token_truoc` | `w6_du_lieu` | `env_nul` (lượt `W6.nul`) | H — `TL_TOKEN` đổi | — | lập luận |
| 30 | `db_tu_choi_unc_goc` | `duong_windows_ba_dang` | `unc_goc` | H — trả lý do thay đường | — | đo 2026-11-19T04:52:30Z: `splitdrive("\\\\server\\share")` phần sau ổ rỗng |
| 31 | `db_nhan_thiet_bi` | `duong_windows_ba_dang` | `thiet_bi` | H — trả đường thay lý do | — | đo 2026-11-19T04:52:30Z: `\\?\C:`, `\\.\pipe` là "ổ" |
| 32 | `db_unc_khong_can_share` | `duong_windows_ba_dang` | `unc_thieu_share` | H | — | đo 2026-11-19T04:52:30Z: `splitdrive("\\\\server")` = (`\\server`, `""`) |

Dòng 25–29 chuyển từ packet 1 (2026-11-18T06:53:23Z). Dòng 25 và 26 cùng (loại, dấu) trong cùng ca nhưng gắn lượt khác nhau; tự kiểm `tu_kiem_sai_luot` (N8(f)): khai lượt đích của dòng 26 là `W6.token` ⇒ ngoại lệ khớp loại + dấu ở lượt khác ⇒ không giết đúng ⇒ `run` trả `False`.
Rà cùng hình dạng (lượt 9): hai dòng E cùng ca (`w4_du_lieu_sai_dang`: 17, 18) có (loại, dấu) KHÁC nhau và nay gắn lượt riêng; dòng 21 khai trên cả hai lượt W5 cùng nhãn để ca không dừng với `ngoai_le_la` trước lượt đích. Đột biến gộp chốt: W4 tách (đích: 1; kiểu/encode: 17, 18; chuẩn hoá: 5); W5 tách (đích: 2; chuẩn hoá: 4) — không còn đột biến bỏ hai chốt một lúc.
Tự kiểm phân hạng (N8(c)): như packet 1, dấu `wp433-tu-kiem`, nhắm `w4_trong_kho` (tập khai rỗng).
Tổng: **32** đột biến (mục 13 có ba (ca, nhãn) đích), 8 dòng có E (17, 18, 26, 27 E thuần; 25, 28 E hoặc H theo nền; 20, 21 thông điệp do rig đặt), 24 dòng H thuần.
Tự kiểm bằng phép đo: **17** dòng (4, 5, 6, 8, 9, 13, 14, 17, 18, 22, 25–28, 30–32); 15 dòng lập luận, xác nhận khi chạy bảng trên mã thật (N8(a)).

## 5. `pham_vi_e`

Không chạm E4, không chạm E5: chỉ sửa mã đường ghi, mọi ca dùng giá trị giả, HOME/cfgdir tạm, đồ giả thay tải Drive (rig chặn
cả hằng baked), không LIVE, không đẩy Package. Ngoại lệ bundled ở §1 là quyết định của chủ kho cho đúng packet này.

## 6. `luat_dung`

- Trần lời gọi Codex theo dòng khai `ADR-0055`; chạm trần ⇒ Review Rescue Checkpoint; xin tăng mang **E2**.
- Trần kích thước `ADR-0053`: numstat (N11) vượt 450 ⇒ dừng TRƯỚC review, đi revision đặc tả (chủ kho đã chọn tách thay vì nâng
  trần, 18-11-2026); xin `nang_tran` chỉ khi chủ kho đổi quyết định đó — **E2**.
- Packet `NLM-GWS-DICH-NGOAI-KHO` chưa land, hoặc `_kiem_dich_ghi` trên base thật không có chữ ký `(dich, goc, thanh_phan)` và
  hợp đồng lỗi như M1/M4 của packet ấy, hoặc cần sửa thân hàm ấy NGOÀI vế reparse của M6, hoặc vế reparse đã có sẵn trên base thật
  (packet 1 đổi phạm vi) ⇒ không cấp lease / dừng, đi revision.
- Chưa có comment cấp ngoại lệ bundled cho packet này trên Issue #433 (§1) ⇒ không cấp lease.
- Cần sửa ngoài write set, hoặc preflight (quét §0.1 của đặc tả packet 1, chạy lại trên base thật) thấy chỗ ghi credential từ
  bundle khác W1–W6 ⇒ dừng, đi revision.
- Neo PD, chuỗi khoá `wp727`, hoặc neo đột biến của fragment packet 1 không giữ được nguyên văn ⇒ dừng, đi revision.
- Đặc tả không thuộc Mission nên chờ chủ kho duyệt băm theo `ADR-0067` — **E2**. Không có điểm hỏi nào khác còn mở.

**Quyết định đã có (chủ kho, 18-11-2026, qua phiên điều phối):** phương án B cho bundled (§1); tách W4/W5 thành packet này.

## 7. `hinh_dang_ke_thua`

Như §7 của đặc tả packet 1: số đếm hình dạng lỗi của tiền nhiệm **KHÔNG ĐO ĐƯỢC** (biên nhận không chép vào kho; đọc thành một
hình dạng là suy luận từ tiêu đề PR). Bộ đếm hiện tại là bộ đếm CÓ CHỨNG CỨ, DÙNG CHUNG với packet `NLM-GWS-DICH-NGOAI-KHO` (xem §7
của đặc tả ấy: mức đặc tả 3, mức mã 0); không reset khi tách. Hai lượt review đặc tả gốc đã bắt hai lớp của chính
đường W4/W5: ghi xuyên thư mục cha là liên kết (S5) và `lstat` chuỗi thô không thấy `alias/`, `alias/.` (L1); M1–M2 và N2 đáp
lại bằng đường dựng từ thành phần, đường kiểm == đường ghi, và một đột biến riêng cho mỗi lớp.

## 8. `chua_do_duoc`

- Máy thật có thể để `~/.config/gws` là liên kết, hoặc đặt `GOOGLE_WORKSPACE_CLI_CONFIG_DIR` có `..`: sau packet, lượt nạp bị từ
  chối với một dòng lý do. Chưa đo trên máy nào.
- Windows: trước packet này, packet 1 KHÔNG chặn junction (chỉ `S_ISLNK`). Junction không cho `S_ISLNK` (chưa đo, đọc tài liệu); vế reparse point từ chối MỌI reparse point, kể cả placeholder
  đồng bộ đám mây — chưa đo; đường có ổ đĩa và `\` qua M1 (2) — chưa chạy trên Windows thật. N4 đo native khi có phiên trên máy
  Windows của chủ kho.
- Kích thước (ước lượng tĩnh, chưa đo; tính lại 2026-11-19T04:5xZ, neo vào số đo packet 1 ở §0.4): `tl_gws.py` +70–90 (M1 có danh sách cho phép UNC/ổ ~26–32; M2 W4 ~12–15 và W5 ~9–12 dòng thêm, thay mẫu makedirs+open+chmod; M6 ~2 kể cả sửa docstring 1175–1176; M7 ~14–18); fragment +320–415 (rig tự chứa như `_Rig` packet 1 ~110–130; 18 hàm ca ~110–160; bảng 32 đột biến ~50–65; khung chạy + tự kiểm (c)(f) ~50–60); bundled +1 ⇒ **391–506 dòng thêm, 3 tệp**, điểm giữa ~448 — CHẠM TRẦN 450, đầu cao vượt. Đã ở trạng thái DỪNG theo §6 trước review (xem §9, câu Q1). N11 đo trên exact head.
- `review_class`, lease của ba đường, nền test: đo khi cấp lease trên base thật (sau packet 1).

## 9. Lịch sử review

Review Codex lượt 3 của đặc tả gốc (trên bản packet 1 `d863a253…`) chỉ ra tên `wp433b_…` không `fullmatch` `_PACKET_TEST_ID_PATTERN` = `wp[1-9][0-9]*_[a-z0-9]+(?:_[a-z0-9]+)*` (`scripts/tl_core/test_fragments.py:23`; đo lại 06:13:09Z: `wp433b_…` False, `wp433_gws_cred_dich_ngoai_kho` True) ⇒ đổi tên tệp, `TEST_ID` và tiền tố SENTINEL. Cùng lượt: nhận hai ca chuỗi `_trong_kho_git` và phép đo rc 4 từ packet 1 (N3b, N7(1)); phản chứng trần 450/451 với đúng 3 dòng (N11); E2 tại điều kiện comment.

Review Codex lượt 4 (trên packet 1 `d8c961e9…` và bản này `dcd5fa74…`): M1 chốt ba dạng đường Windows (`D:fake`, `\fake` từ chối; `D:\fake` nhận) với ca chạy mọi nền qua `ntpath` (N2w); nhận ca symlink tệp cuối + `db_bo_symlink_cuoi` từ packet 1 (N3).

Review Codex lượt 5: định dạng dòng cố định và `repr` cho đường (M3, N3e); quyền 0600 chỉ POSIX (N5); nhận N3c (reparse giả lập) và N3d (`jar_rong_base`) từ packet 1 để giữ trần packet ấy; bộ đếm có chứng cứ dùng chung (§7).

Điều chỉnh của phiên điều phối (trước lượt 6): MÃ vế reparse chuyển hẳn sang packet này (M6), luật dừng §6 cho phép sửa thân `_kiem_dich_ghi` đúng vế ấy; N3d ghi rõ là hồi quy cho nhánh mã không đổi của packet 1.

Review Codex lượt 6: N3e đặt `\n` vào đường kho được in; neo `db_bo_reparse` trên nguồn candidate đã áp M6 (N3c, N4); mốc §8 theo `date -u` (2026-11-18T06:33:42Z).

Review Codex lượt 7: N3e chạy mọi nền (Windows giả lập `_trong_kho_git`); M4 dùng luật ngoại lệ dự kiến của packet 1.
Review Codex lượt 8: lập §4b — bảng ĐẦY ĐỦ 24 đột biến kèm cơ chế chết và ngoại lệ khai (nguồn duy nhất); rà toàn bảng tìm thêm `db_w4_bo_kiem_kieu`, `db_w4_bo_kiem_encode` chết bằng ngoại lệ — đã khai; `db_bo_reparse` thêm đích `reparse_w1`. Tự kiểm: 10 dòng bằng phép đo, 14 dòng lập luận.

Review Codex lượt 9 (2026-11-18T06:51:08Z): `reparse_w1` dùng jar có khoá lồng; M1 kiểm dạng "có gốc, thiếu ổ" và "theo ổ" TRƯỚC `isabs` (khác biệt 3.11/3.12 với 3.13); §4b khai ngoại lệ theo lượt và rà cùng hình dạng.

Điều chỉnh trước lượt 10 (2026-11-18T06:53:23Z): nhận khối kiểm DỮ LIỆU W6 từ packet 1 (M7, N9w6, §4b dòng 25–29) để packet 1 có biên 34.

**Hoãn (quyết định chủ kho 18-11-2026, Review Rescue Checkpoint):** packet này làm revision với ngân sách lời gọi Codex RIÊNG sau khi packet `NLM-GWS-DICH-NGOAI-KHO` land. Bốn finding lượt 10 và trạng thái sau lần soạn lại 2026-11-19 (CHƯA qua review):
- P2 UNC — ĐÃ SỬA: M1 chuyển sang danh sách CHO PHÉP N1/N2/N3 (posix P1/P2), liệt kê đủ đường bị từ chối R1–R5; UNC gốc share nhận; thiết bị `\\?\`/`\\.\` và UNC thiếu share từ chối; không gọi `isabs`. N2w thêm bốn nhãn dương/âm, §4b thêm ba đột biến 30–32, mỗi đột biến gỡ đúng một chốt.
- P2 env — ĐÃ SỬA: fixture `W6.token` dùng `\ud800` (đo §0.4: `\udc80` lọt surrogateescape trên POSIX, `\ud800` ném trên 3.11–3.13); dòng 25 và 28 khai cơ chế "E hoặc H theo nền" — ném thì ngoại lệ khai của lượt chuyển thành nhãn, không ném thì hậu điều biến môi trường đổi làm nhãn đỏ; dấu NUL lấy tiền tố `embedded null`.
- P3 M3 — ĐÃ SỬA: tập ngoại lệ khai gắn theo LƯỢT; bỏ dòng trống, năm dòng 25–29 trở lại trong bảng.
- P3 §8 — ĐÃ SỬA: N9w6 có SÁU lượt (`token`, `encode`, `dict_a`, `dict_b`, `dict_c`, `nul`); ước lượng tính lại ở §8.

**Câu hỏi cho chủ kho (chặn review):**
- **Q1 — Kích thước (CHẶN).** Ước lượng 391–506 dòng thêm, điểm giữa ~448, sát/vượt trần 450 (§8). Lựa chọn: (a) TÁCH: P2a = W4/W5 credential gws (M1, M2, M3, M6; N1, N2w, N2, N3, N3b, N3c, N3e, N4, N5, N6, N7, N8; §4b dòng 1–23, 30–32), ước ~330–410; P2b = kiểm DỮ LIỆU W6 (M7; N9w6, N3d; §4b dòng 24–29), ước ~150–200 (rig tự chứa lặp lại); P2b không phụ thuộc P2a. (b) `nang_tran` lên 520 cho packet này (ADR-0053, E2), giữ nguyên một packet. *Khuyến nghị: (a) tách* — hai phần không chung đường mã (W4/W5 khác W6), và hình dạng "sát trần rồi phải tách" đã xảy ra ở packet 1; tách bây giờ rẻ hơn tách sau review.
- **Q2 — UNC.** Có cho phép `GOOGLE_WORKSPACE_CLI_CONFIG_DIR` trỏ tới share mạng (`\\server\share\…`) không? *Khuyến nghị: có* (đặc tả hiện nhận UNC, chỉ từ chối thiết bị và thiếu share); nếu chủ kho muốn cấm thì N2 của M1 bị gỡ, `unc_goc` đổi thành ca âm. Không chặn review.
- **Q3 — Ngoại lệ bundled (E2, §1).** Cần comment mới của chủ kho trên #433 nêu đúng `packet_id`, đúng tệp `scripts/tl_test_fragments_bundled.py` và sha256 đặc tả đã đóng băng (comment 6973856830 chỉ phủ packet 1). Không chặn review, chặn cấp lease.

## 10. Nhật ký revision

- 2026-11-19T04:5xZ (phiên điều phối #1206, phiên con): đo lại §0.1 trên `3b64746`, thêm §0.4; đóng bốn finding lượt 10 (xem §9);
  thêm §4b dòng 30–32; tính lại §8. Dừng TRƯỚC lời gọi Codex vì Q1 (kích thước) chặn. Bản trước: `6c654d64…` (lưu `rv433p2/dac-ta-ban0-hoan.md`).
