tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# GWS-CRED-DICH-NGOAI-KHO-N r2 — đóng bốn nợ có tên của #433 trên đường ghi credential (`tl_gws.py`)

- packet_id: GWS-CRED-DICH-NGOAI-KHO-N; revision: 2 (thay r1 `fa48e076…`; lý do ở §0.5 và §10);

| trường | giá trị |
|---|---|
| `packet_issue` | #433 |
| `nguon_cap_viec` | Bốn nợ có tên trên #433: `wp433-w6-chot-to-tien`, `wp433-bundle-khong-phai-dict`, `wp433-trong-kho-git-nuot-oserror` (issuecomment-7008271757, chủ kho quyết ghi nợ khi duyệt P2b) và `wp433-pk1-n84-windows` (issuecomment-7015527750, chủ kho quyết 19-11 khi land C1). Chủ kho 2026-11-20 (phiên điều phối #1206): "xử lý các khoản nợ". |
| `phu_thuoc` | P2a, P2b, C1, R đã land (R: PR #1431, merge `b71f445`; hồ sơ land PR #1436). Gọi lại hợp đồng lỗi sáu cụm của P2a (`_CUM`: `nằm trong kho git`, `là liên kết tượng trưng`, `ngoài danh sách cho phép`, `dữ liệu không hợp lệ`, `ghi lỗi`, `đường không hợp lệ`). |
| `review_class` | `sensitive` (`scripts/tl_gws.py` là đường ghi credential). |
| `diem_xuat_phat_r2` | Exact head r1 `143115a2b43a42f483db8cb0b3aa0a75b68e1d94` (tree `3b200640563c8673fa7faebdc49a41b3028061ee`, PR #1441, base `dd1985be73d3cf65f3580f7049039ae3dab50d3d`) trên nhánh `agent/wp433-r6-g1-claude`. Executor vá r2 bằng commit MỚI trên CÙNG nhánh (không amend, không force-push); numstat và trần đo từ base `dd1985b`. M1–M6 của r1 giữ nguyên nội dung đã có ở `143115a`; r2 chỉ thêm M7. |
| `base` | `8a72d28d7a413047733277545fc8547f32010593` (merge PR #1436; tree `df0bbe85dc230c595d44c197eae694fe41feecf8`; blob `tl_gws.py` `1acf4ef1…`, sha256 `f2acadef…`; blob fragment packet 1 `f7769ece…`, sha256 `45ca8983…`). Phiên thi hành đo lại §0 trên base thật của lease và DỪNG nếu lệch. |

Các mục **[ĐÃ CHỐT Qn]** dưới đây là quyết định của chủ kho ngày 2026-11-20 (phiên điều phối #1206); muốn đổi thì phải ra revision mới.

## 0. Hiện trạng (đo trên `8a72d28`)

Bằng chứng chạy được ở `ops/reviews/wp433p2n-spec-r1/` (probe Desktop, ca tái hiện Linux; lệnh và đầu ra thô).

- **(1) `wp433-pk1-n84-windows` — lỗi ở TEST, không ở mã.** Fragment `scripts/test_fragments/wp433_nlm_gws_dich_ngoai_kho.py` dòng 239
  và 241 dựng bộ chọn đích ném lỗi bằng phép so CHUỖI: W2 `thay=lambda d: d.startswith(nlm)`, W6 `thay=lambda d: d == cfg`, với
  `nlm`, `cfg` dựng bằng `os.path.join(HOME, …)` (dấu `\` trên nt). Mã dựng đích bằng `os.path.expanduser("~/.notebooklm-mcp-cli")`
  (dòng 1952) và `os.path.expanduser("~/.tra_luat_config.json")` (dòng 1899); `ntpath.expanduser` giữ nguyên phần đuôi `/…`, nên đích
  thật là `C:\…\h13/.notebooklm-mcp-cli\auth.json` và `C:\…\h14/.tra_luat_config.json` — hai phép so chuỗi luôn sai, `os.replace`
  không bao giờ ném, ghi THÀNH CÔNG, vị từ `rc == 1 and _dung(err, "bootstrap", "ghi")` sai. Đo Desktop `DESKTOP-T9R33P2` (Windows 11
  10.0.26300, Python 3.12.10) 2026-11-20T01:30Z trên clone sạch `8a72d28` (tree khớp): biến thể `goc` ⇒ `run() -> False`, `ĐỎ
  chung_hop_dong_loi: [('N8.4-W2', 'oserror_w2'), ('N8.4-W6', 'oserror_w6')]`, `CA 17/18`, `DOT BIEN 30/30`; biến thể `log` in đường mà
  `os.replace` nhận (`…\h13/.notebooklm-mcp-cli\auth.json` so với `…\h13\.notebooklm-mcp-cli` ⇒ `False`; W6 tương tự); biến thể
  `chuan` (chỉ đổi hai phép so thành so sau `os.path.normcase(os.path.normpath(·))`) ⇒ `run() -> True`, `CA 18/18`, `DOT BIEN 30/30`.
  Đầu ra thô: `ops/reviews/wp433p2n-spec-r1/desktop-wp433n-out-20261120T012952Z/`. Linux, cùng probe: `goc` và `chuan` đều `run() -> True`,
  `CA 18/18`, `DOT BIEN 30/30` (`probe-linux.txt`).
- **(2) `wp433-w6-chot-to-tien`.** W6 (`cmd_bootstrap`, dòng 1899–1902) gọi `_kiem_dich_ghi(cfgp, cfgp, ())`: luật (b) chỉ `lstat` CHÍNH
  `cfgp`, không thư mục tổ tiên nào; W4/W5 qua `_dich_cred_gws` (POSIX dòng 1220–1229, chốt từ `/`; nt `_dich_cred_gws_nt` dòng
  1305–1325, chốt từ gốc ổ). Tái hiện Linux: HOME là symlink → T (ngoài kho) ⇒ W6 in `✓ config … → <L>/.tra_luat_config.json` và tệp nằm ở
  `T`; cùng lượt, gws cfgdir `<L>/.config/gws` bị W4 từ chối `là liên kết tượng trưng: '<L>'`. Tương tự khi một TỔ TIÊN của HOME là symlink.
- **(3) `wp433-bundle-khong-phai-dict`.** `cmd_bootstrap` (W2/W6, dòng 1881–1888) và `cmd_nlm_auth_pull` (W1, dòng 1832–1836) gọi
  `bundle.get(...)` ngay sau `json.loads`; bundle giải mã ra JSON không phải object ⇒ `AttributeError` thoát khỏi lệnh (traceback, không
  dòng `✗`). Tái hiện Linux với bundle `[1, 2]`, `"chuoi"`, `7`, `null`: cả hai lệnh ném `AttributeError: '<kiểu>' object has no attribute 'get'`.
- **(4) `wp433-trong-kho-git-nuot-oserror`.** `_trong_kho_git` (dòng 1120–1140) bắt `except OSError: pass` quanh `os.lstat(<d>/.git)`:
  mọi lỗi ngoài "chưa có" (EACCES, ELOOP, EIO…) bị đọc thành "không có `.git` ở đây" và vòng đi tiếp lên tổ tiên. Tái hiện Linux (bọc
  `os.lstat` ném `PermissionError` đúng ở `<K>/.git`, K là kho thật): trước khi bọc `_trong_kho_git(<K>/con) == <K>`; khi bọc ⇒ `None`,
  và `_kiem_dich_ghi(<K>/con/f, "/", …)` ⇒ `None` (được ghi). C1 đã viết `_co_git_nt` ba trạng thái cho nhánh nt của W4/W5; mọi người gọi
  khác (W1–W3, W6, W4/W5 POSIX, `_bootstrap_agent_creds` dòng 1446) vẫn đi qua hàm nuốt lỗi.
- Nguyên mẫu M2–M4 (`nguyen-mau/ap_proto.py`, đo 2026-11-20 trên Linux, `ket-qua-linux.txt`): số lần mỗi chuỗi neo `_DB`/`_TU_KIEM` của P2a, P2b, packet 1, C1, R trên bản nguyên mẫu BẰNG base; năm fragment `run` True, bộ đếm CA/LUOT/DOT BIEN y hệt base; `tai_hien.py` trên nguyên mẫu: (2) W6 không ghi, (3) rc 3 cả hai lệnh, (4) `PermissionError` lan ra.
- **(5) Hồi quy C1 trên Windows do M2 — thước đo CŨ của C1, không phải lỗi mã (đo 2026-11-20 trên Desktop, lý do ra r2).** Đo native §4c của PR #1441 (https://github.com/ducthangho/tra-luat/pull/1441#issuecomment-7030452526): fragment C1 `wp433_gws_cred_win_duong.py` `run() -> False` trên head `143115a`, đỏ đúng `tich_hop_nt · W4.loai_o_loi`, tất định; base `dd1985b` `True`. Cơ chế: lượt ấy thay `_loai_o_nt` bằng hàm ném `OSError` rồi chạy `bootstrap`; trên head W6 gọi `_chot_thu_muc(dirname(cfgp))`, nhánh nt đi qua `_duong_dich_chuan_nt` ⇒ `_loai_o_nt` ⇒ `OSError` lan tới `except OSError` của W6 ⇒ W6 TỪ CHỐI (`ghi lỗi: OSError`, fail-closed đúng hợp đồng M2). Vị từ C1 cũ đòi ĐÚNG MỘT dòng `✗` (của W4) nên đỏ; hai đột biến đích `W5.git_loi`/`W5.realpath_loi` (lượt SAU W4.loai_o_loi trong cùng ca) thành tín dụng giả vì ca dừng sớm. Chẩn đoán Desktop `DESKTOP-T9R33P2` 2026-11-20T04:44–04:57Z (clone sạch head `143115a` tree `3b200640…` và base `dd1985b` tree `4cc3d1a8…`; bản C1 có in chẩn đoán ngay trước `r.xs`), nguyên văn lượt thật trên head: `CHAN_DOAN W4.loai_o_loi kq=1 err=['[bootstrap] ✗ ghi lỗi: OSError', '[bootstrap] ✗ ghi lỗi: OSError']` — dòng ĐẦU là W6 (khối W6 chạy trước W4 trong `cmd_bootstrap`), dòng HAI là W4; stdout không có `✓ config`/`✓ gws cred`. Đo thêm: (i) đột biến C1 `db_nt_git_nuot_loi` SỐNG SÓT khi chỉ sửa `W4.loai_o_loi` (head + bản sửa (a) của M7: `CA 3/3 · LUOT 76/76 · DOT BIEN 46/47`), vì M4 làm `_trong_kho_git` cũng lan lỗi `lstat` ở `<pk>\.git` — lớp thứ hai che lớp `_co_git_nt`; (ii) head + đủ M7 (a)+(b): `run True`, `CA 3/3 · LUOT 76/76 · DOT BIEN 47/47 · HONG 0 · TU_KIEM 3/3`, hai lần; (iii) phản chứng base `dd1985b` + đủ M7: `run False`, đỏ đúng `tich_hop_nt · W4.loai_o_loi · hop_dong` (W6 base còn ghi ⇒ một dòng `✗`). Linux (head và base, đủ M7): `run True`, bộ đếm bằng bản gốc (`CA 2/2 chỉ_nt 1 · LUOT 65/65 chỉ_nt 11 · DOT BIEN 39/39 chỉ_nt 8`). Đầu ra thô: Desktop `F:\tl-win\session_015GtxrZk6gmfQKo7g4BfMBS\r2-bang-chung.zip` (sha256 `bc68aae96e53b8f7bcd77fe4252cbd7e8990d26c88f7df56800b5b0e7433ab90`, gồm ba thư mục `wp433n-r2*-out-*` và ba driver); driver, diff và log Linux trong `ops/reviews/wp433p2n-spec-r1/r2/`.
- Người gọi `_kiem_dich_ghi`/`_dich_cred_gws`/`_dich_jar_nlm` đều đã bọc `except OSError` ⇒ `ghi lỗi: …` (W1 1841–1843, W2 1953–1955, W3
  2163–2165, W4 1937–1941, W5 2087–2091, W6 1900–1918). `_bootstrap_agent_creds` được `cmd_bootstrap` bọc `except Exception` ⇒ `KHÔNG ĐO ĐƯỢC`.

## 1. `write_set`

```
scripts/tl_gws.py
scripts/test_fragments/wp433_gws_cred_no.py
scripts/test_fragments/wp433_gws_cred_win_duong.py
scripts/test_fragments/wp433_nlm_gws_dich_ngoai_kho.py
scripts/tl_test_fragments_bundled.py
```

r2 THÊM `scripts/test_fragments/wp433_gws_cred_win_duong.py` (fragment C1) — CHỈ cho M7; năm tệp, dưới trần sáu tệp của `ADR-0053`.

KHÔNG `RELEASE_MANIFEST.json`. Bundled chỉ sinh bằng `generate_bundled_module_bytes(scripts/test_fragments)`. **Điều kiện trước khi cấp
lease (E2):** comment của chủ kho trên #433 cấp ngoại lệ bundled nêu đúng `packet_id` `GWS-CRED-DICH-NGOAI-KHO-N`, đúng một tệp
`scripts/tl_test_fragments_bundled.py` và sha256 của đặc tả r2 này đã đóng băng (comment cho r1 `7028469434` KHÔNG áp cho r2); lease trỏ URL comment. Phiên land tái sinh manifest.

## 2. `ngoai_pham_vi`

- `secrets-set` (dòng 1014) cũng `bundle[...] = …` trên bundle chưa kiểm kiểu; đường ấy GHI lên Drive và không thuộc bốn nợ — để nợ riêng
  nếu chủ kho muốn (`wp433-secrets-set-bundle-khong-phai-dict`).
- Đổi cách dựng đường bằng `expanduser("~/…")` trong mã cho đẹp dấu phân cách: không (Q1).
- TOCTOU, tag reparse không phải name-surrogate: như P2a §2 và R §2.
- Fragment C1 chỉ được sửa đúng M7; mọi dòng khác, `_DB`, `_TU_KIEM`, `_LUOT_DU_KIEN`, `_DU_KIEN` của nó giữ nguyên.
- P2b đỏ SẴN trên Windows (`wp433-p2b-w6-windows`, nợ riêng: https://github.com/ducthangho/tra-luat/issues/433#issuecomment-7030544194): KHÔNG sửa trong N; D4 miễn trừ P2b khi delta 0 (§4c).
- Không sửa `ops/**`, `.github/**`, `scripts/tl_selftest.py`, fragment P2a/R, `RELEASE_MANIFEST.json`, `changelog.d/*`, `VERSION`,
  `CHANGELOG.md`, `SKILL.md`.

## 3. `muc_tieu`

| # | mục tiêu | tệp |
|---|---|---|
| M1 | **[ĐÃ CHỐT Q1: sửa test]** Fragment packet 1: ĐÚNG hai phép so ở dòng 239 và 241 đổi thành so sau `os.path.normcase(os.path.normpath(·))` hai vế (W2: `startswith` của bản chuẩn hoá `nlm` cộng `os.sep`, để `…cli2` không khớp; W6: bằng nhau). Không sửa dòng nào khác của fragment ấy; mọi `_DB`/`_TU_KIEM` của nó giữ nguyên số lần khớp. | fragment packet 1 |
| M2 | **[ĐÃ CHỐT Q2: A, chốt từ gốc như W4/W5]** **[ĐÃ CHỐT Q5: có]** THÊM, KHÔNG viết lại: một hàm mới `_chot_thu_muc(thu_muc) -> str \| None` chỉ kiểm luật (b) (liên kết: `S_ISLNK` hoặc bit `FILE_ATTRIBUTE_REPARSE_POINT` như `_kiem_dich_ghi`) trên MỌI tiền tố từ gốc tới chính `thu_muc`; KHÔNG kiểm `.git` (đã có ở lời gọi tệp hiện hành, cùng chuỗi tổ tiên); KHÔNG tạo/ghi gì; tiền tố chưa tồn tại (`FileNotFoundError`/`NotADirectoryError`) bỏ qua, lỗi `lstat` khác LAN RA. Tách thành phần: POSIX bằng `_duong_dich_chuan(thu_muc, <cwd>)`, nt bằng `_duong_dich_chuan_nt` (ổ có chữ, REMOVABLE/FIXED); `os.getcwd()` CHỈ được gọi khi `thu_muc` là đường tương đối cần ghép cwd (HOME tuyệt đối không phụ thuộc cwd); lý do chuẩn hoá ⇒ trả nguyên lý do ấy; `thu_muc` QUY VỀ GỐC — viết trực tiếp (`/`, `X:\\`) hoặc đường hợp lệ mà sau khi ghép với cwd và bỏ thành phần rỗng/`.` theo parser không còn thành phần nào (vd `.` với cwd là gốc) ⇒ chỉ `lstat` chính gốc, KHÔNG trả `đường không hợp lệ`: POSIX `/`; nt gốc tuyệt đối có chữ ổ (`X:\\`) chỉ được nhận với tuple thành phần rỗng SAU KHI loại ổ đo bằng `_loai_o_nt` là REMOVABLE (2) hoặc FIXED (3), loại khác ⇒ `đường không hợp lệ: <repr>`. Parser C1 `_duong_dich_chuan_nt` và W4/W5 KHÔNG đổi (ngoại lệ gốc nằm trong `_chot_thu_muc`). Lý do liên kết dùng đúng chuỗi cụm `là liên kết tượng trưng: {repr(tiền_tố)[:200]}`. Gọi ở hai chỗ, mỗi chỗ CHÈN một dòng mới, không sửa dòng hiện có: (i) W6, ngay sau dòng `ly_cfg = _kiem_dich_ghi(cfgp, cfgp, ())` và trước mọi `os.path.exists`/đọc: `ly_cfg = ly_cfg or _chot_thu_muc(os.path.dirname(cfgp))`; (ii) cuối `_dich_jar_nlm`, sau vòng khoá hiện hành: `return _chot_thu_muc(os.path.dirname(nbase))` thay cho `return None` cuối hàm (W1–W3 đi qua hàm này). Mọi dòng là neo `_DB`/`_TU_KIEM` của fragment P2a, P2b, packet 1, C1, R giữ NGUYÊN VĂN (danh sách nhạy nhất: `_W1`, `_W3`, `_W6`, `ly_nlm = _dich_jar_nlm(nbase, jar) or _ghi_jar_nlm(nbase, jar)`, `_kiem_dich_ghi(dest, "/", (*chuan[1], "credentials.json"))`, `(kho_dich := _trong_kho_git(os.path.dirname(dich)))`, `def _dich_jar_nlm(`); `_dich_cred_gws`/`_dich_cred_gws_nt` KHÔNG đổi. Mã MỚI không được chứa nguyên văn một chuỗi neo nào của năm fragment ấy (vd vế bit của R phải viết khác chữ) — đo bằng N6. Nguyên mẫu tham khảo (KHÔNG phải mã thi công): `ops/reviews/wp433p2n-spec-r1/nguyen-mau/` — trên Linux giữ đúng số neo của cả năm fragment và cả năm `run` True với bộ đếm bằng base. | `scripts/tl_gws.py` |
| M3 | **[ĐÃ CHỐT Q3: rc 3]** Ngay sau `json.loads` của bundle trong `cmd_bootstrap` (trước dòng in `bundle giải mã OK`) và `cmd_nlm_auth_pull` (trước `nlm = bundle.get("nlm_auth")`), CHÈN kiểm: không phải `dict` ⇒ đúng một dòng stderr `[<thẻ>] ✗ dữ liệu không hợp lệ: bundle`, trả **3** (cùng mã với "giải mã lỗi"). Bước nạp cấu hình `load_creds` phía trước GIỮ NGUYÊN (phục vụ tải bundle; có thể gán `TL_TOKEN`/`TL_WEBAPP` từ config sẵn — hành vi base). Hợp đồng: không gán env NÀO từ bundle, không ghi tệp nào, không gọi `_bootstrap_agent_creds`, không in dòng `bundle giải mã OK`. Không sửa dòng neo `    nlm = bundle.get("nlm_auth")\n    if not nlm:\n` và `_GOI` của fragment P2b. | `scripts/tl_gws.py` |
| M4 | `_trong_kho_git` ba trạng thái như `_co_git_nt`: chỉ `FileNotFoundError`/`NotADirectoryError` là "chưa có"; lỗi `lstat` khác LAN RA. Docstring nêu hợp đồng mới. Người gọi giữ nguyên (đã bọc `OSError`). | `scripts/tl_gws.py` |
| M5 | Fragment mới `wp433_gws_cred_no.py`, `TEST_ID = "wp433_gws_cred_no"`: khuôn fragment R (nạp `tl_gws` vào bộ nhớ, đột biến trên bản sao, neo khớp đúng 1 lần, `TinHieuChotCa(AssertionError)` phân hạng theo (ca, lượt, nhãn), sổ `_LUOT_DU_KIEN`/`_DU_KIEN` viết riêng, mọi đầu ra ra STDERR, khôi phục trong `finally`). | fragment mới |
| M6 | Tái sinh bundled; không sửa tay. | bundled |
| M7 | **[ĐÃ CHỐT chủ kho 20-11: sửa KỲ VỌNG test C1, giữ W6 fail-closed]** Fragment C1, ca `tich_hop_nt` (nt), ĐÚNG hai chỗ, nguyên văn ở `ops/reviews/wp433p2n-spec-r1/r2/c1-m7.diff`: (a) lượt `W4.loai_o_loi`: TRƯỚC lời gọi chụp `c6 = pathlib.Path(os.path.expanduser("~/.tra_luat_config.json"))` và `c6_truoc` (byte, hoặc `None`); nhãn `hop_dong` đổi `err == [_W4 + "ghi lỗi: OSError"]` thành `… * 2` (W6 rồi W4, mỗi writer đúng một dòng), giữ các vế còn lại; THÊM nhãn `w6=" ✓ config " not in out and <byte c6 sau> == c6_truoc`. KHÔNG dùng `not os.path.lexists(c6)`: các lượt W4 trước trong CÙNG ca đã ghi config hợp lệ (đo Desktop: nguyên mẫu `lexists` đỏ nhãn `w6`). (b) lượt `W5.git_loi`: bộ tiêm `lstat` ném `PermissionError` CHỈ ở lần gọi ĐẦU vào `<pk>\.git` (danh sách `mot` một phần tử) thay vì mọi lần. Lý do đo được: sau M4, `_trong_kho_git` cũng lan lỗi ở cùng đường, nên với bộ tiêm mọi-lần đột biến C1 `db_nt_git_nuot_loi` (nuốt lỗi trong `_co_git_nt`) SỐNG SÓT trên Desktop — lớp thứ hai che lớp thứ nhất; tiêm một lần trả lại khả năng đo riêng `_co_git_nt` (đột biến ⇒ lần `lstat` thứ hai thành công ⇒ `nằm trong kho git` ⇒ đỏ `hop_dong`). Không đổi lượt nào khác, không đổi `_DB`/`_TU_KIEM`/`_LUOT_DU_KIEN`/`_DU_KIEN`. | fragment C1 |

## 4. `nghiem_thu`

"W6 đúng khi từ chối" = `rc == 1`, đúng một dòng stderr `fullmatch` `\[bootstrap\] ✗ <cụm>: .+` cho W6, `TL_TOKEN` đã gán, tệp đích
và tệp ở đích thật KHÔNG đổi byte, không tệp tạm còn lại.

| # | ca (nền) | lượt và tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|---|
| N1 | fragment packet 1 (mọi) | `run()` True trên Linux VÀ trên Desktop (D2); `N8.4-W2`, `N8.4-W6` đạt; `DOT BIEN 30/30`, `HONG 0`. Phép so W2 chuẩn hoá không khớp anh em tên (`<HOME>\.notebooklm-mcp-cli2\x` ⇒ không ném). | Trên Desktop, base: `run() -> False` ở đúng hai lượt ấy (đã đo, §0). Đột biến `db_w6_oserror_kieu_cu` của chính fragment (đích `N8.4-W6`) vẫn GIET trên cả hai nền — chứng minh lượt W6 đo được nhánh lỗi, không chỉ đổi màu. |
| N2 | `to_tien` (mọi; nhánh symlink chỉ khi `os.symlink` dựng được, như R) | Thứ tự lượt trong ca: `W6.to_tien_lk` ĐẦU TIÊN, `W2.to_tien_lk` thứ hai, rồi các lượt còn lại (để đột biến 1 và 4 đỏ ở đúng lượt đích trước mọi lượt khác cùng khôi phục ghi). Ở hai lượt đích, nhãn `lk` CHỈ phát cho phản chứng xác định: mất từ chối ở đường đang đo VÀ writer được gọi đúng đích ấy VÀ byte ở T đổi; sai hậu điều khác mang nhãn riêng (vd `dong_loi`, `ghi_khac`). Các lượt W6 chạy `bootstrap` với `env=chat` (không cài đặt, không W4/W2), `load_creds` cô lập khỏi đích merge, và ĐẶT SẴN config JSON ở T cho cả hai fixture liên kết; trong W6 đếm riêng số lần `os.path.exists(cfgp)` và số lần mở đọc `cfgp` — cả hai phải bằng 0 khi bị chặn (đối chứng: bỏ điều kiện `ly_cfg is None` trước `exists` phải ĐỎ ở phép đo thứ tự đọc; đối chứng này là tự kiểm của rig, không thêm vào §4b). Rig cô lập đường đang đo: mỗi lượt đếm số lần gọi `_ghi_nguyen_tu_0600` theo ĐÍCH và số lần `open` đích `cfgp` để đọc (bọc tạm `open` trong không gian tên `tl_gws`, khôi phục sau lượt), chụp ảnh byte tệp đích và tệp ở T trước/sau. `W6.home_lk` (HOME là symlink → T ngoài kho; bundle chỉ `token`, không `gws_cred`/`nlm_auth`) ⇒ W6 đúng khi từ chối, cụm `lk`, chi tiết `repr(<HOME>)`, writer 0 lần cho `cfgp`, open-đọc `cfgp` 0 lần; `W6.to_tien_lk` (HOME = `<L>/home`, L symlink) ⇒ như trên, chi tiết `repr(<L>)`; `W6.kho` (HOME trong kho) ⇒ cụm `kho` (hồi quy); `W6.thuong` (HOME thường ngoài kho, config cũ `{"cu": 1}`) ⇒ ghi, merge giữ `cu`, rc 0 (hồi quy); `W6.thuong_cwd_mat` (như trên, HOME tuyệt đối, `os.getcwd()` bọc ném `FileNotFoundError` trong cửa sổ chốt) ⇒ vẫn merge, giữ `cu`, rc 0; `W6.goc` (gọi trực tiếp `_chot_thu_muc` với gốc của nền viết trực tiếp, VÀ với `.` khi cwd giả lập là gốc) ⇒ `None` và đúng một lần `lstat` trên gốc chuẩn ở cả hai dạng; trên nt thêm `W6.goc_o_mang` (gốc ổ với bộ đo loại ổ giả trả 4) ⇒ `đường không hợp lệ` và 0 lần `lstat`, và `W6.goc_o_co_dinh` (bộ đo giả trả 3) ⇒ `None` và ĐÚNG một lần `lstat` trên gốc chuẩn (bọc `lstat` bằng bộ đếm chuyển tiếp). `W1.to_tien_lk` (`nlm-auth-pull`), `W2.to_tien_lk` (`bootstrap`, bundle chỉ `nlm_auth` — không `token`, không `gws_cred`, nên `lk` chỉ có thể đến từ jar), `W3.to_tien_lk` (`_nlm_auth_load` với tải giả) — mỗi lượt HOME = `<L>/home` ⇒ cụm `lk`, writer 0 lần cho mọi đích jar, không tệp jar ở T. | Đột biến 1 ⇒ `W6.to_tien_lk` đỏ (writer gọi cho `cfgp`, tệp ở T đổi); base cho `✓ config` (đã đo, §0). Đột biến 4 ⇒ `W2.to_tien_lk` đỏ (writer gọi cho đích jar). |
| N3 | `bundle_kieu` (mọi) | Với bundle `[1, 2]`, `"x"`, `7`, `null`, `true`: `bootstrap` và `nlm-auth-pull` mỗi lệnh rc 3, đúng một dòng stderr `[<thẻ>] ✗ dữ liệu không hợp lệ: bundle`, stdout không có `bundle giải mã OK` và `agent_creds:`; `TL_TOKEN`/`TL_WEBAPP` BẰNG ảnh chụp ngay sau `load_creds` (rig bọc `load_creds` gốc để chụp, không thay nó); `_bootstrap_agent_creds` gọi 0 lần; writer 0 lần; HOME không tệp mới. Bundle `{}` (dict rỗng) giữ hành vi base (hồi quy). Thứ tự lượt trong ca: `bootstrap.list` ĐẦU TIÊN, `pull.list` thứ hai, rồi các kiểu còn lại. `tu_kiem_sai_luot` dùng đột biến 2, khai `pull.list` thay cho `bootstrap.list`, giữ nguyên kiểu tín hiệu, ca và nhãn `rc3`; tự kiểm này chạy cả khi lượt symlink bị bỏ qua. Lượt `bootstrap.list` và `pull.list` gọi lệnh trong `try`: CHỈ `AttributeError` có `e.name == "get"`, `type(e.obj) is list` và frame cuối của traceback thuộc chính hàm lệnh đích (`cmd_bootstrap` hoặc `cmd_nlm_auth_pull`, so `co_name`) được đổi thành `TinHieuChotCa(ca, lượt, "rc3")`; ngoại lệ khác lan ra như lỗi giàn (không tính giết). | Base ném `AttributeError` (đã đo). Đột biến 2 (bỏ kiểm ở `cmd_bootstrap`) ⇒ `bootstrap.list`; 3 (bỏ kiểm ở `cmd_nlm_auth_pull`) ⇒ `pull.list`. |
| N4 | `ba_trang_thai` (mọi) | Lượt `perm` chạy ĐẦU TIÊN trong ca và gọi TRỰC TIẾP `_trong_kho_git(<K>/con)` với `os.lstat` được bọc: ném `PermissionError(13)` đúng khi đối số, sau `normcase(normpath)`, bằng `<K>/.git` (K kho thật); mọi đối số khác chuyển nguyên cho hàm gốc; bọc khôi phục trong `finally`; lượt đòi probe ĐÃ trúng đúng 1 lần (đếm) và hàm ném `PermissionError`. Lượt `notfound`: K nằm trong một kho CHA ngoài K; `FileNotFoundError` giả ở `<K>/.git` ⇒ probe trúng đúng một lần và `_trong_kho_git` trả ĐÚNG đường kho cha (mốc dương của việc đi tiếp). Lượt `notdir`: cùng fixture, `NotADirectoryError` giả ở `<K>/.git` ⇒ trúng đúng một lần, trả đúng kho cha (đối chứng: bản chỉ bắt `FileNotFoundError` phải đỏ ở `notdir`). Lượt `w6_ghi_loi` (riêng, sau `perm`): `bootstrap` với HOME = `<K>/con/h`, cùng probe ⇒ W6 `ghi lỗi`, writer 0 lần. EACCES POSIX THẬT (thư mục không quyền `x`) là phép đo BỔ SUNG NGOÀI sổ fragment: chạy bằng root ⇒ ghi `not_run` kèm lý do trong hồ sơ PR, không vào `_LUOT_DU_KIEN`; lượt `perm` giả lập vẫn bắt buộc và tính trong sổ. | Đột biến 5 (`except (FileNotFoundError, NotADirectoryError)` về `except OSError`) ⇒ `perm` đỏ (đích duy nhất). |
| N5 | tự kiểm | Như R N3: `_DU_KIEN` == tập ID `_DB`; `_LUOT_DU_KIEN` viết riêng và khớp số lượt đã ghi; một dòng tổng kết STDERR; `run` True chỉ khi mọi đẳng thức đếm đúng; `tu_kiem_doi_kieu`, `tu_kiem_chu_thich`, `tu_kiem_sai_luot` cho đúng hạng; stdout của `run` rỗng. Danh sách `bỏ_qua` cho phép VIẾT RIÊNG trong fragment mới (không mượn của R): đúng các lượt symlink `W6.home_lk`, `W6.to_tien_lk`, `W1/W2/W3.to_tien_lk` và đột biến 1, 4; mỗi lần bỏ qua phải kèm `winerror == 1314` từ probe `os.symlink` của CHÍNH lượt đó; bỏ qua lượt/ID khác ⇒ `run` False. | Như R N3 (thêm ID thừa, gỡ lượt, in ra stdout, phân hạng bỏ so lượt, bỏ qua ngoài danh sách ⇒ False). |
| N6 | gate | Như R N4: selftest N/N hai số bằng nhau, N = N_base + 1, delta 0 ca đỏ mới; `test-fragments-check --json` `ok: true`; `bundle_fragment_check.py --json` `ok: true`, `failed: []`; neo `_DB`/`_TU_KIEM` của fragment P2a, P2b, packet 1, C1, R: số lần trên candidate BẰNG base (đếm từng chuỗi; đo lượt review 1 trên base: P2a 40 (27 chuỗi), P2b 40 (21), packet 1 36 (28), C1 51 (42), R 6 (4)); năm fragment ấy `run` True trên Linux; `ops/cloud_agent_creds_test.py` `TONG: DAT` từng ca bằng base; lane worker `release-manifest` tạm + `release-verify --strict --json` rc 0, `ok: true`, `expected_file_count == checked_file_count`; `ruff --select F` delta 0; `git diff --check`, `doctrine-scan`, `adr-song` rc 0; so exact OID base/head với lease trước numstat; numstat dưới `pipefail`: đúng 5 dòng, tập đường == §1, tổng thêm ≤ 450. Neo C1: số lần mỗi chuỗi `_DB`/`_TU_KIEM` của C1 trong `tl_gws.py` không đổi (M7 chỉ sửa tệp test). | Như R N4. |
| N8 | C1 (M7) | Linux: `run` True, bộ đếm bằng base (`CA 2/2 chỉ_nt 1 · LUOT 65/65 chỉ_nt 11 · DOT BIEN 39/39 chỉ_nt 8 · TU_KIEM 3/3`). Desktop (D4): `run` True, `CA 3/3 · LUOT 76/76 · DOT BIEN 47/47 · HONG 0 · TU_KIEM 3/3`. | Base `dd1985b` + bản C1 của r2 trên Desktop: `run` False, đỏ đúng `tich_hop_nt · W4.loai_o_loi · hop_dong` (W6 base còn ghi ⇒ một dòng `✗`) — phản chứng rằng nhãn mới đo hành vi M2. |
| N7 | đo native (§4c) | Hồ sơ PR ghi lệnh, shell, exact head/tree, đầu ra thô, rc và kết luận của MỌI phép bắt buộc ở §4c. | Phép bắt buộc thiếu, trái kỳ vọng hoặc `KHÔNG ĐO ĐƯỢC` ⇒ không land. |

### 4b. Bảng đột biến — NGUỒN DUY NHẤT

Neo trên NGUỒN CANDIDATE, mỗi neo khớp đúng 1 lần.

| # | đột biến | ca · lượt | nhãn | nền |
|---|---|---|---|---|
| 1 | `db_w6_bo_chot_thu_muc`: xoá đúng dòng chèn `ly_cfg = ly_cfg or _chot_thu_muc(os.path.dirname(cfgp))` (neo là cả dòng ấy, khớp 1 lần) | `to_tien` · `W6.to_tien_lk` | `lk` | mọi (cần symlink) |
| 2 | `db_bootstrap_bo_kiem_bundle`: bỏ kiểm kiểu bundle ở `cmd_bootstrap` | `bundle_kieu` · `bootstrap.list` | `rc3` | mọi |
| 3 | `db_pull_bo_kiem_bundle`: bỏ kiểm kiểu bundle ở `cmd_nlm_auth_pull` | `bundle_kieu` · `pull.list` | `rc3` | mọi |
| 4 | `db_jar_bo_chot_thu_muc`: `return _chot_thu_muc(os.path.dirname(nbase))` về `return None` (neo cả dòng, khớp 1 lần, trong thân `_dich_jar_nlm`) | `to_tien` · `W2.to_tien_lk` | `lk` | mọi (cần symlink) |
| 5 | `db_nuot_oserror`: except của `_trong_kho_git` về `OSError` | `ba_trang_thai` · `perm` | `lan_ra` | mọi |

Tổng: **5** đột biến. Trên nt thiếu quyền symlink (`winerror == 1314`): lượt symlink `bỏ_qua` theo danh
sách cho phép RIÊNG của fragment này (N5); đột biến 1 và 4 khi ấy `bỏ_qua`, KHÔNG tính giết; nền ấy phải còn đo chúng bằng junction (D3).

### 4c. Đo native Windows (`DESKTOP-T9R33P2`, dự phòng VM)

Chung như R §4c (ghim exact head/tree; `python`; rig dưới thư mục phiên; dọn đúng thứ mình tạo; không ghi kho thật; offline).

| # | bắt buộc | dựng / lệnh | kỳ vọng |
|---|---|---|---|
| D1 | không | `ver`; Developer Mode; hệ tệp ổ | ghi lại |
| D2 | có | Rig clone base/candidate bằng `git -c core.longpaths=true clone …` (cây có đường quá MAX_PATH; lượt r1 lần đầu `KHÔNG ĐO ĐƯỢC` vì `Filename too long`). Trên máy Windows mà probe symlink VÀ hardlink của packet 1 đều thành công (Desktop; thiếu quyền ⇒ VM đủ quyền, cùng base/candidate ghim; ghi kết quả probe): `run(tl)` của fragment packet 1 trên BA vế, mỗi vế một tiến trình: base; bản sao base chỉ áp hai dòng M1; candidate. Trên vế M1 thêm phép thử trực tiếp hai biểu thức so: đích con `<HOME>\\.notebooklm-mcp-cli\\auth.json` khớp, tên anh em `<HOME>\\.notebooklm-mcp-cli2\\x` trượt; W6 khớp đúng đích `expanduser` | base `False` đúng hai lượt `N8.4-W2`/`N8.4-W6`; vế M1 và candidate `True`, `CA 18/18`, `DOT BIEN 30/30`, ghi kết quả từng lượt N8.4 và bộ đếm; phép thử biểu thức đúng như trên. Không chạy được ⇒ `KHÔNG ĐO ĐƯỢC` |
| D3 | có | Có thể trên máy thiếu quyền symlink (junction không cần). Fixture junction: HOME (`USERPROFILE`) là junction → T, và HOME có tổ tiên là junction; thêm một lời gọi `_chot_thu_muc` với gốc ổ native đang chứa fixture (kỳ vọng `None`, ghi đối số và số lần `lstat` trên gốc — đúng 1). Chạy W6 (`bootstrap`, bundle chỉ `token`), W1 (`nlm-auth-pull`), W2 (`bootstrap`, bundle chỉ `nlm_auth`), W3 (`_nlm_auth_load`, tải giả) bằng: candidate; bản sao áp đột biến 1; bản sao áp đột biến 4; bản sao candidate bỏ vế bit reparse TRONG `_chot_thu_muc`. Ghi tiền tố bị chặn, rc/giá trị trả về, số lần gọi writer, ảnh byte tệp ở T trước/sau | candidate: cả bốn từ chối cụm `lk` đúng tiền tố, writer 0, T không đổi; đột biến 1: W6 ghi vào T; đột biến 4: W2 ghi jar vào T; bỏ vế bit: ghi (junction không phải `S_ISLNK`). Thiếu fixture junction, thiếu vế đối chứng, hoặc sai kỳ vọng ⇒ không land |
| D4 | có | Trên máy đủ quyền của D2: `run(tl)` của fragment mới, R, C1, P2a, P2b, packet 1, mỗi cái một tiến trình; P2b chạy thêm trên base `dd1985b` cùng máy | fragment mới, R, C1, P2a, packet 1: `run()` True; P2b: MIỄN TRỪ khi bộ đếm candidate BẰNG base (đỏ sẵn `wp433-p2b-w6-windows`, đo r1: 28/32, bốn đột biến W6 sống ở cả hai vế) — candidate tệ hơn base ⇒ không land; ghi bộ đếm từng fragment; fragment mới: mọi `bỏ_qua` theo N5; fragment kế thừa: đối chiếu `bỏ_qua` với quy tắc của CHÍNH fragment ấy |
| D5 | có (T3) | Như R D12 (tái sinh manifest trong commit land, selftest + mọi gate lane LAND trên hai nền, cùng SHA/tree) | xanh cả hai nền |

## 5. `pham_vi_e`

Không chạm E4, E5: đường ghi local; ca dùng giá trị giả, thư mục tạm, đồ giả thay tải Drive; không LIVE, không đẩy Package.

## 6. `luat_dung`

- Trần lời gọi Codex theo `ADR-0055`; trần kích thước `ADR-0053` (≤ 6 tệp, ≤ 450 dòng thêm) đo bằng numstat thật trước khi công bố; vượt ⇒
  DỪNG, nâng trần là **E2**.
- C1 trên Desktop không `True` sau M7, hoặc bộ đếm C1 khác `3/3 · 76/76 · 47/47` ⇒ dừng, revision.
- §0 lệch trên base thật (thân `_trong_kho_git`, khối W6, hai dòng 239/241 của fragment packet 1) ⇒ dừng, revision.
- Một neo của fragment P2a/P2b/packet 1/C1/R lệch số lần so với base, hoặc một đột biến của chúng đổi hạng (GIET → khác) ⇒ dừng, revision.
- D2: vế M1 không `True` ⇒ dừng, (1) không phải lỗi so chuỗi như §0 khai, revision; vế M1 `True` mà candidate `False` ⇒ dừng, phân loại theo lượt/neo đỏ (lỗi của M2–M4, không của M1).
- Chưa có comment ngoại lệ bundled đúng `packet_id` ⇒ không cấp lease (**E2**). Đặc tả chờ chủ kho duyệt băm theo `ADR-0067` (**E2**).

## 7. `hinh_dang_ke_thua`

(1) là lớp "cổng đỏ vì THƯỚC ĐO so chuỗi, không vì mã" — cùng họ bài học "ca có MẶT khác ca có ĐO" của `CLAUDE.md`; (2) và (4) là
lớp "chốt nhìn THIẾU" (thiếu tổ tiên; đọc trạng thái thứ ba thành "không") của cùng hình dạng P2a/C1/R. Mức đặc tả N: 0 lượt lúc soạn.

## 8. `chua_do_duoc`

- Lượt thật EACCES trên POSIX (N4) chưa chạy trong phiên soạn: container chạy root, quyền thư mục không chặn root.
- D3 (junction làm HOME) chưa đo.
- Kích thước: nguyên mẫu `tl_gws.py` ĐO `+32/−2` (`git apply --numstat nguyen-mau.diff`), cộng nhánh gốc ổ nt và docstring M4 ước +4–8 ⇒ +36–40; fragment packet 1 +2/−2; fragment mới (ước lượng tĩnh):
  khung và tự kiểm theo R 95–110 (R thật 234 dòng), rig HOME/symlink/bọc `lstat`/đếm writer-open 45–60, N2–N4 lượt 55–70, `_DB` 5 mục 6–8 ⇒ **201–248**; bundled +2/−1 ⇒ tổng
  **~241–292**, dưới trần 450 ⇒ MỘT packet. Gate dùng numstat THẬT của đủ bốn tệp.
- r2 (đo trên bản nguyên mẫu: head `143115a` + M7 + bundled tái sinh, so base `dd1985b`): `wp433_gws_cred_no.py` 359/0 · `wp433_gws_cred_win_duong.py` 5/2 · `wp433_nlm_gws_dich_ngoai_kho.py` 2/2 · `tl_gws.py` 44/3 · `tl_test_fragments_bundled.py` 3/2 ⇒ **5 tệp, 413 dòng thêm, 9 xoá** (trần 450).

## 9. Lịch sử và quyết định

- Chủ kho 2026-11-20: xử lý bốn nợ; phiên điều phối đề xuất gộp một packet vì cả bốn chạm `tl_gws.py`/fragment #433.
- Chủ kho 2026-11-20 (sau đo native PR #1441): hồi quy C1 trên Windows ⇒ ra r2, sửa KỲ VỌNG test C1, giữ W6 fail-closed; P2b đỏ sẵn trên Windows ⇒ ghi nợ riêng `wp433-p2b-w6-windows`, miễn trừ cho N (delta 0).
- Chủ kho 2026-11-20 chốt cả bốn quyết định theo khuyến nghị: Q1 sửa test · Q2 = A (chốt từ gốc) · Q3 = rc 3 · Q5 = có. Q4 không cần chọn (`_trong_kho_git` chuyển sang ba trạng thái).

## 10. Nhật ký revision

- 2026-11-20T01:5xZ (phiên con của điều phối #1206): bản 1, đo §0 trên `8a72d28` (Linux + Desktop).
- 2026-11-20 (lượt review 1, Codex `request_changes`, 5 P2 + 2 P3): M2 đổi từ "tổng quát hoá `_dich_cred_gws(_nt)`" sang THÊM `_chot_thu_muc` (chỉ luật liên kết, gốc→thư mục) chèn sau dòng neo W6 và cuối `_dich_jar_nlm` — không sửa dòng neo nào, không đi qua nhánh `_co_git_nt` (P2-1, P2-2); HOME là gốc chỉ kiểm gốc (P3-2); M3 giữ `load_creds`, hợp đồng "không gán env TỪ BUNDLE", N3 chụp env sau `load_creds`, đếm agent/writer (P2-3); đột biến 1/4 neo trọn dòng chèn, N2 cô lập đường ghi bằng đếm writer/open và bundle tối thiểu, N3 chỉ đổi `AttributeError` `.get`/`list` của đúng lệnh thành tín hiệu (P2-4); N2 thêm W3, D3 chạy W1–W3 + W6 trên junction với bản đột biến 1, 4 và bản bỏ vế bit, N5 danh sách bỏ qua riêng kèm `winerror 1314` (P2-5); D2 ba vế base / chỉ M1 / candidate và phép thử anh em (P3-1); N4 `perm` gọi trực tiếp, đích duy nhất của đột biến 5. Thêm nguyên mẫu đo neo.
- 2026-11-20 (lượt review 2, Codex `request_changes`, 4 P2 + 2 P3): N2 xếp `W6.to_tien_lk`, `W2.to_tien_lk` lên đầu ca và nhãn `lk` chỉ cho phản chứng xác định (P2-1); N3 nhận dạng `AttributeError` bằng `name`/`obj`/frame thay vì chuỗi (P2-2); EACCES POSIX thật ra ngoài sổ, root ⇒ `not_run` (P2-3); D2 bắt buộc trên máy Windows đủ quyền symlink+hardlink, D3 được trên máy thiếu quyền (P2-4); gốc ổ nt chỉ nhận sau kiểm loại ổ, đo bằng bộ đo giả + D3 (P3-1); §8 theo numstat nguyên mẫu `+32/−2` (P3-2).
- 2026-11-20 (lượt review 3, Codex `request_changes`, 2 P2 + 3 P3): W6 đo bằng `env=chat`, config đặt sẵn ở T, đếm `exists`/mở đọc `cfgp` (P2); ghim `bootstrap.list`, `pull.list` đầu ca N3, `tu_kiem_sai_luot` dùng đột biến 2 (P2); gốc ổ đếm `lstat` (P3); `notfound` hai kho lồng nhau (P3); D4 trên máy đủ quyền, bỏ qua theo quy tắc từng fragment (P3).
- 2026-11-20 (lượt review 4, Codex `request_changes`, 1 P2 + 2 P3): ngoại lệ gốc áp cả cho đường tương đối quy về gốc (`.` với cwd gốc), N2 đo hai dạng (P2); N4 thêm lượt `notdir` (P3); §8 tổng 241–292 (P3).
- 2026-11-20 (lượt review 5, Codex `approve`, 1 P3): sau approve, đóng P3 bằng sửa đặc tả — `os.getcwd()` chỉ gọi cho đường tương đối, N2 thêm `W6.thuong_cwd_mat`. Sửa này KHÔNG được chiếu lại (bản lượt 5 được approve: `rv/dac-ta-luot5.md`; khác biệt ở `rv/sau-luot5.diff`).
- 2026-11-20T05:00Z (phiên con của điều phối #1206): **bản r2.** Lý do: đo native PR #1441 (comment 7030452526) bắt hồi quy C1 trên Windows do M2 (§0 (5)). Thêm fragment C1 vào write set (5 tệp), M7 (sửa kỳ vọng `W4.loai_o_loi` và tiêm lỗi một lần ở `W5.git_loi`), N8, D2 rig `core.longpaths`, D4 miễn trừ P2b delta 0, §8 numstat r2 đo được 413. Điểm xuất phát: exact head `143115a`, executor vá bằng commit mới. Nguyên mẫu và đo Desktop/Linux: `ops/reviews/wp433p2n-spec-r1/r2/`. Chưa chiếu Codex.
