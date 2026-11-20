tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# GWS-CRED-DICH-NGOAI-KHO-N r1 — đóng bốn nợ có tên của #433 trên đường ghi credential (`tl_gws.py`)

- packet_id: GWS-CRED-DICH-NGOAI-KHO-N; revision: 1;

| trường | giá trị |
|---|---|
| `packet_issue` | #433 |
| `nguon_cap_viec` | Bốn nợ có tên trên #433: `wp433-w6-chot-to-tien`, `wp433-bundle-khong-phai-dict`, `wp433-trong-kho-git-nuot-oserror` (issuecomment-7008271757, chủ kho quyết ghi nợ khi duyệt P2b) và `wp433-pk1-n84-windows` (issuecomment-7015527750, chủ kho quyết 19-11 khi land C1). Chủ kho 2026-11-20 (phiên điều phối #1206): "xử lý các khoản nợ". |
| `phu_thuoc` | P2a, P2b, C1, R đã land (R: PR #1431, merge `b71f445`; hồ sơ land PR #1436). Gọi lại hợp đồng lỗi sáu cụm của P2a (`_CUM`: `nằm trong kho git`, `là liên kết tượng trưng`, `ngoài danh sách cho phép`, `dữ liệu không hợp lệ`, `ghi lỗi`, `đường không hợp lệ`). |
| `review_class` | `sensitive` (`scripts/tl_gws.py` là đường ghi credential). |
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
- Người gọi `_kiem_dich_ghi`/`_dich_cred_gws`/`_dich_jar_nlm` đều đã bọc `except OSError` ⇒ `ghi lỗi: …` (W1 1841–1843, W2 1953–1955, W3
  2163–2165, W4 1937–1941, W5 2087–2091, W6 1900–1918). `_bootstrap_agent_creds` được `cmd_bootstrap` bọc `except Exception` ⇒ `KHÔNG ĐO ĐƯỢC`.

## 1. `write_set`

```
scripts/tl_gws.py
scripts/test_fragments/wp433_gws_cred_no.py
scripts/test_fragments/wp433_nlm_gws_dich_ngoai_kho.py
scripts/tl_test_fragments_bundled.py
```

KHÔNG `RELEASE_MANIFEST.json`. Bundled chỉ sinh bằng `generate_bundled_module_bytes(scripts/test_fragments)`. **Điều kiện trước khi cấp
lease (E2):** comment của chủ kho trên #433 cấp ngoại lệ bundled nêu đúng `packet_id` `GWS-CRED-DICH-NGOAI-KHO-N`, đúng một tệp
`scripts/tl_test_fragments_bundled.py` và sha256 của đặc tả này đã đóng băng; lease trỏ URL comment. Phiên land tái sinh manifest.

## 2. `ngoai_pham_vi`

- `secrets-set` (dòng 1014) cũng `bundle[...] = …` trên bundle chưa kiểm kiểu; đường ấy GHI lên Drive và không thuộc bốn nợ — để nợ riêng
  nếu chủ kho muốn (`wp433-secrets-set-bundle-khong-phai-dict`).
- Đổi cách dựng đường bằng `expanduser("~/…")` trong mã cho đẹp dấu phân cách: không (Q1).
- TOCTOU, tag reparse không phải name-surrogate: như P2a §2 và R §2.
- Không sửa `ops/**`, `.github/**`, `scripts/tl_selftest.py`, fragment P2a/C1/R, `RELEASE_MANIFEST.json`, `changelog.d/*`, `VERSION`,
  `CHANGELOG.md`, `SKILL.md`.

## 3. `muc_tieu`

| # | mục tiêu | tệp |
|---|---|---|
| M1 | **[ĐÃ CHỐT Q1: sửa test]** Fragment packet 1: ĐÚNG hai phép so ở dòng 239 và 241 đổi thành so sau `os.path.normcase(os.path.normpath(·))` hai vế (W2: `startswith` của bản chuẩn hoá `nlm` cộng `os.sep`, để `…cli2` không khớp; W6: bằng nhau). Không sửa dòng nào khác của fragment ấy; mọi `_DB`/`_TU_KIEM` của nó giữ nguyên số lần khớp. | fragment packet 1 |
| M2 | **[ĐÃ CHỐT Q2: A, chốt từ gốc như W4/W5]** W6 dựng đích và chốt bằng CÙNG đường của W4/W5: `_dich_cred_gws` và `_dich_cred_gws_nt` nhận thêm tham số tên tệp (mặc định `"credentials.json"`, mọi lời gọi cũ giữ nguyên chữ); W6 gọi với thư mục `os.path.expanduser("~")` và tên `.tra_luat_config.json`, dùng `dest` trả về làm đích đọc-merge và ghi, lý do khác `None` ⇒ một dòng `[bootstrap] ✗ <lý do>`, `degraded`, KHÔNG đọc tệp cũ, KHÔNG ghi. **[ĐÃ CHỐT Q5: có]** áp cùng đường gốc→đích cho `_dich_jar_nlm` (W1–W3), vì `~/.notebooklm-mcp-cli` có cùng khe. | `scripts/tl_gws.py` |
| M3 | **[ĐÃ CHỐT Q3: rc 3]** Ngay sau `json.loads` của bundle trong `cmd_bootstrap` và `cmd_nlm_auth_pull`: không phải `dict` ⇒ đúng một dòng `[<thẻ>] ✗ dữ liệu không hợp lệ: bundle` ra stderr, trả **3** (cùng mã với "giải mã lỗi"), không gán env, không ghi gì, không gọi `_bootstrap_agent_creds`. | `scripts/tl_gws.py` |
| M4 | `_trong_kho_git` ba trạng thái như `_co_git_nt`: chỉ `FileNotFoundError`/`NotADirectoryError` là "chưa có"; lỗi `lstat` khác LAN RA. Docstring nêu hợp đồng mới. Người gọi giữ nguyên (đã bọc `OSError`). | `scripts/tl_gws.py` |
| M5 | Fragment mới `wp433_gws_cred_no.py`, `TEST_ID = "wp433_gws_cred_no"`: khuôn fragment R (nạp `tl_gws` vào bộ nhớ, đột biến trên bản sao, neo khớp đúng 1 lần, `TinHieuChotCa(AssertionError)` phân hạng theo (ca, lượt, nhãn), sổ `_LUOT_DU_KIEN`/`_DU_KIEN` viết riêng, mọi đầu ra ra STDERR, khôi phục trong `finally`). | fragment mới |
| M6 | Tái sinh bundled; không sửa tay. | bundled |

## 4. `nghiem_thu`

"W6 đúng khi từ chối" = `rc == 1`, đúng một dòng stderr `fullmatch` `\[bootstrap\] ✗ <cụm>: .+` cho W6, `TL_TOKEN` đã gán, tệp đích
và tệp ở đích thật KHÔNG đổi byte, không tệp tạm còn lại.

| # | ca (nền) | lượt và tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|---|
| N1 | fragment packet 1 (mọi) | `run()` True trên Linux VÀ trên Desktop (D2); `N8.4-W2`, `N8.4-W6` đạt; `DOT BIEN 30/30`, `HONG 0`. Phép so W2 chuẩn hoá không khớp anh em tên (`<HOME>\.notebooklm-mcp-cli2\x` ⇒ không ném). | Trên Desktop, base: `run() -> False` ở đúng hai lượt ấy (đã đo, §0). Đột biến `db_w6_oserror_kieu_cu` của chính fragment (đích `N8.4-W6`) vẫn GIET trên cả hai nền — chứng minh lượt W6 đo được nhánh lỗi, không chỉ đổi màu. |
| N2 | `to_tien` (mọi; nhánh symlink chỉ khi `os.symlink` dựng được, như R) | `W6.home_lk` (HOME là symlink → T ngoài kho) ⇒ W6 đúng khi từ chối, cụm `lk`, chi tiết `repr(<HOME>)`; `W6.to_tien_lk` (HOME = `<L>/home`, L symlink) ⇒ cụm `lk`, chi tiết `repr(<L>)`; `W6.kho` (HOME trong kho) ⇒ cụm `kho` (hồi quy); `W6.thuong` (HOME thường ngoài kho, config cũ `{"cu": 1}`) ⇒ ghi, merge giữ `cu`, rc 0 với fixture không thiếu gì (hồi quy). `W1.to_tien_lk` và `W2.to_tien_lk` (HOME = `<L>/home`) ⇒ cụm `lk`, jar không ghi. | Đột biến 1 (W6 về `_kiem_dich_ghi(cfgp, cfgp, ())`) ⇒ `W6.home_lk` hoặc `W6.to_tien_lk` đỏ; base cho `✓ config` ở cả hai (đã đo, §0). Đột biến 4. |
| N3 | `bundle_kieu` (mọi) | Với bundle `[1, 2]`, `"x"`, `7`, `null`, `true`: `bootstrap` và `nlm-auth-pull` mỗi lệnh rc 3, đúng một dòng stderr `[<thẻ>] ✗ dữ liệu không hợp lệ: bundle`, stdout không có `agent_creds:`, `TL_TOKEN` không bị gán, HOME không tệp mới. Bundle `{}` (dict rỗng) giữ hành vi base (hồi quy). | Base ném `AttributeError` (đã đo). Đột biến 2 (bỏ kiểm ở `cmd_bootstrap`) và 3 (bỏ kiểm ở `cmd_nlm_auth_pull`), mỗi cái một lượt đích riêng. |
| N4 | `ba_trang_thai` (mọi) | Bọc `os.lstat` ném `PermissionError(13)` đúng ở `<K>/.git` (K kho thật, so sau `normcase(normpath)`): `_trong_kho_git(<K>/con)` ném `PermissionError`; `bootstrap` với HOME = `<K>/con/h` ⇒ W6 `ghi lỗi`, không ghi; `FileNotFoundError` giả ở cùng chỗ ⇒ đi tiếp lên tổ tiên như base (hồi quy, trả tổ tiên có `.git` cao hơn nếu có, ngược lại `None`). POSIX thêm lượt thật: thư mục không quyền `x` cho người chạy (bỏ qua khi chạy bằng root, ghi lý do; không tính là đạt). | Đột biến 5 (`except (FileNotFoundError, NotADirectoryError)` về `except OSError`) ⇒ lượt `PermissionError` đỏ. |
| N5 | tự kiểm | Như R N3: `_DU_KIEN` == tập ID `_DB`; `_LUOT_DU_KIEN` viết riêng và khớp số lượt đã ghi; một dòng tổng kết STDERR; `run` True chỉ khi mọi đẳng thức đếm đúng; `tu_kiem_doi_kieu`, `tu_kiem_chu_thich`, `tu_kiem_sai_luot` cho đúng hạng; stdout của `run` rỗng. | Như R N3 (thêm ID thừa, gỡ lượt, in ra stdout, phân hạng bỏ so lượt ⇒ False). |
| N6 | gate | Như R N4: selftest N/N hai số bằng nhau, N = N_base + 1, delta 0 ca đỏ mới; `test-fragments-check --json` `ok: true`; `bundle_fragment_check.py --json` `ok: true`, `failed: []`; neo `_DB`/`_TU_KIEM` của fragment P2a, packet 1, C1, R: số lần trên candidate BẰNG base; bốn fragment ấy `run` True trên Linux; `ops/cloud_agent_creds_test.py` `TONG: DAT` từng ca bằng base; lane worker `release-manifest` tạm + `release-verify --strict --json` rc 0, `ok: true`, `expected_file_count == checked_file_count`; `ruff --select F` delta 0; `git diff --check`, `doctrine-scan`, `adr-song` rc 0; so exact OID base/head với lease trước numstat; numstat dưới `pipefail`: đúng 4 dòng, tập đường == §1, tổng thêm ≤ 450. | Như R N4. |
| N7 | đo native (§4c) | Hồ sơ PR ghi lệnh, shell, exact head/tree, đầu ra thô, rc và kết luận của MỌI phép bắt buộc ở §4c. | Phép bắt buộc thiếu, trái kỳ vọng hoặc `KHÔNG ĐO ĐƯỢC` ⇒ không land. |

### 4b. Bảng đột biến — NGUỒN DUY NHẤT

Neo trên NGUỒN CANDIDATE, mỗi neo khớp đúng 1 lần.

| # | đột biến | ca · lượt | nhãn | nền |
|---|---|---|---|---|
| 1 | `db_w6_ve_chot_cu`: lời gọi chốt W6 về `_kiem_dich_ghi(cfgp, cfgp, ())` (giữ phần còn lại) | `to_tien` · `W6.to_tien_lk` | `lk` | mọi (cần symlink) |
| 2 | `db_bootstrap_bo_kiem_bundle`: bỏ kiểm kiểu bundle ở `cmd_bootstrap` | `bundle_kieu` · `bootstrap.list` | `rc3` | mọi |
| 3 | `db_pull_bo_kiem_bundle`: bỏ kiểm kiểu bundle ở `cmd_nlm_auth_pull` | `bundle_kieu` · `pull.list` | `rc3` | mọi |
| 4 | `db_jar_ve_chot_cu`: `_dich_jar_nlm` về `_kiem_dich_ghi(<đích>, nbase, tp)` | `to_tien` · `W2.to_tien_lk` | `lk` | mọi (cần symlink) |
| 5 | `db_nuot_oserror`: except của `_trong_kho_git` về `OSError` | `ba_trang_thai` · `perm` | `lan_ra` | mọi |

Tổng: **5** đột biến. Trên nt thiếu quyền symlink (`winerror == 1314`): lượt symlink `bỏ_qua` theo danh
sách cho phép của R; đột biến 1 và 4 khi ấy `bỏ_qua`, KHÔNG tính giết; nền ấy phải còn đo N2 bằng junction (D3).

### 4c. Đo native Windows (`DESKTOP-T9R33P2`, dự phòng VM)

Chung như R §4c (ghim exact head/tree; `python`; rig dưới thư mục phiên; dọn đúng thứ mình tạo; không ghi kho thật; offline).

| # | bắt buộc | dựng / lệnh | kỳ vọng |
|---|---|---|---|
| D1 | không | `ver`; Developer Mode; hệ tệp ổ | ghi lại |
| D2 | có | `run(tl)` của fragment packet 1 trên base và trên candidate, mỗi vế một tiến trình | base `False` đúng hai lượt `N8.4-W2`/`N8.4-W6`; candidate `True`, `CA 18/18`, `DOT BIEN 30/30` |
| D3 | có | W6 với HOME (`USERPROFILE`) là junction → T, và HOME có tổ tiên là junction (Q2 = A); gọi bằng candidate và bằng bản sao áp đột biến 1 | candidate từ chối cụm `lk`; bản đột biến ghi (`✓ config`) |
| D4 | có | `run(tl)` của fragment mới, R, C1, P2a, packet 1, mỗi cái một tiến trình | mỗi `run()` True |
| D5 | có (T3) | Như R D12 (tái sinh manifest trong commit land, selftest + mọi gate lane LAND trên hai nền, cùng SHA/tree) | xanh cả hai nền |

## 5. `pham_vi_e`

Không chạm E4, E5: đường ghi local; ca dùng giá trị giả, thư mục tạm, đồ giả thay tải Drive; không LIVE, không đẩy Package.

## 6. `luat_dung`

- Trần lời gọi Codex theo `ADR-0055`; trần kích thước `ADR-0053` (≤ 6 tệp, ≤ 450 dòng thêm) đo bằng numstat thật trước khi công bố; vượt ⇒
  DỪNG, nâng trần là **E2**.
- §0 lệch trên base thật (thân `_trong_kho_git`, khối W6, hai dòng 239/241 của fragment packet 1) ⇒ dừng, revision.
- Một neo của fragment P2a/packet 1/C1/R lệch số lần so với base ⇒ dừng, revision (M2 đổi chữ ký `_dich_cred_gws` — kiểm trước tiên).
- D2 trên candidate không `True` ⇒ dừng: (1) không phải lỗi so chuỗi như §0 khai, revision.
- Chưa có comment ngoại lệ bundled đúng `packet_id` ⇒ không cấp lease (**E2**). Đặc tả chờ chủ kho duyệt băm theo `ADR-0067` (**E2**).

## 7. `hinh_dang_ke_thua`

(1) là lớp "cổng đỏ vì THƯỚC ĐO so chuỗi, không vì mã" — cùng họ bài học "ca có MẶT khác ca có ĐO" của `CLAUDE.md`; (2) và (4) là
lớp "chốt nhìn THIẾU" (thiếu tổ tiên; đọc trạng thái thứ ba thành "không") của cùng hình dạng P2a/C1/R. Mức đặc tả N: 0 lượt lúc soạn.

## 8. `chua_do_duoc`

- Lượt thật EACCES trên POSIX (N4) chưa chạy trong phiên soạn: container chạy root, quyền thư mục không chặn root.
- D3 (junction làm HOME) chưa đo.
- Kích thước (ước lượng tĩnh): `tl_gws.py` +14–24 (M2 6–12, M3 4–6, M4 2–3, docstring); fragment packet 1 +2/−2; fragment mới: khung
  và tự kiểm theo R 95–110, rig HOME/symlink/bọc `lstat` 35–50, N2–N4 lượt 40–55, `_DB` 5 mục 6–8 ⇒ **176–223**; bundled +2/−1 ⇒ tổng
  **~195–250**, dưới trần 450 ⇒ MỘT packet.

## 9. Lịch sử và quyết định

- Chủ kho 2026-11-20: xử lý bốn nợ; phiên điều phối đề xuất gộp một packet vì cả bốn chạm `tl_gws.py`/fragment #433.
- Chủ kho 2026-11-20 chốt cả bốn quyết định theo khuyến nghị: Q1 sửa test · Q2 = A (chốt từ gốc) · Q3 = rc 3 · Q5 = có. Q4 không cần chọn (`_trong_kho_git` chuyển sang ba trạng thái).

## 10. Nhật ký revision

- 2026-11-20T01:5xZ (phiên con của điều phối #1206): bản 1, đo §0 trên `8a72d28` (Linux + Desktop).
