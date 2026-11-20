tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# GWS-CRED-DICH-NGOAI-KHO-P2BW r1 — fragment P2b đỏ trên Windows vì bộ quan sát so đường dẫn bằng CHUỖI (nợ `wp433-p2b-w6-windows`)

- packet_id: GWS-CRED-DICH-NGOAI-KHO-P2BW; revision: 1;

| trường | giá trị |
|---|---|
| `packet_issue` | #433 |
| `nguon_cap_viec` | Nợ có tên `wp433-p2b-w6-windows` (https://github.com/ducthangho/tra-luat/issues/433#issuecomment-7030544194), ghi khi đo native PR #1441; chủ kho 2026-11-20 (phiên điều phối #1206): "Đồng ý, bắt đầu đi" (xử lý nợ này sau khi packet N land). |
| `phu_thuoc` | P2b (PR #1421) và packet N (PR #1441, merge `64fa515`; hồ sơ land PR #1451, merge `94cbb36`) đã land. |
| `review_class` | `sensitive` theo đường dẫn: fragment kiểm đường ghi credential `cmd_bootstrap` W6. Mã `scripts/tl_gws.py` KHÔNG đổi. |
| `base` | `94cbb3688427a820de746df60a929e264981d248` (merge PR #1451). Từ `64fa515` tới `94cbb36` không commit nào chạm `scripts/`. Blob fragment P2b sha256 ở §0. Phiên thi hành đo lại §0 trên base thật của lease và DỪNG nếu lệch. |

## 0. Hiện trạng (đo trên `94cbb36`)

Bằng chứng chạy được ở `ops/reviews/wp433p2bw-spec-r1/` (nguyên mẫu, runner, đầu ra Linux và Desktop).

- **Triệu chứng (đo 20-11 trên Desktop `DESKTOP-T9R33P2`, Windows 11, Python 3.12.10):** `wp433_gws_cred_dich_ngoai_kho_b.py` `run() -> False`,
  `DOT BIEN … giết_đúng=28` trên 32 đột biến chạy được (4 `CHI_POSIX`), bốn đột biến `SONG_SOT`: `db_w6_tu_choi_van_chot`, `db_w6_tu_choi_van_doc`,
  `db_w6_tu_choi_ghi_lai`, `db_w6_encode_ghi_cu` (nhãn đích `khong_chot`, `khong_doc`, `khong_ghi`, `khong_ghi`). Y hệt trên `dd1985b` và trên head N
  (comment 7030452526, 7032232129); Linux `run() -> True` 36/36.
- **Nguyên nhân — ở TEST, không ở mã.** Bộ quan sát trong `_Rig.goi` đếm lời gọi trên ĐƯỜNG CONFIG bằng so CHUỖI với `self.cfg`
  (`os.path.join(HOME, ".tra_luat_config.json")`, dấu `\` trên nt): `op`: `f == cfg`; `kd`: `dich == cfg`; `gh`: `path == cfg`. Mã dựng đích bằng
  `os.path.expanduser("~/.tra_luat_config.json")` (`tl_gws.py` dòng 1939), và `ntpath.expanduser` giữ nguyên đuôi `/…` ⇒ chuỗi `…\home/.tra_luat_config.json`
  khác chuỗi `…\home\.tra_luat_config.json` dù cùng tệp. Ba bộ đếm `chot`/`doc`/`ghi` luôn 0 trên nt ⇒ nhãn `khong_chot`/`khong_doc`/`khong_ghi` không bao giờ
  đỏ ⇒ bốn đột biến chèn đúng các lời gọi ấy SỐNG. Cùng lớp với nợ `wp433-pk1-n84-windows` của packet 1 (đóng ở packet N, M1).
- **Phản chứng Linux (cơ chế, chạy được):** runner `chay_p2b_gia_nt.py` thay `os.path.expanduser` sao cho `~/.tra_luat_config.json` ra `<HOME>/./.tra_luat_config.json`
  (khác CHUỖI, cùng tệp — đúng hình dạng nt). Fragment base: `giết_đúng=32`/36, ba đột biến `SONG_SOT` (`…van_doc`, `…ghi_lai`, `encode_ghi_cu`), `VẾ SAI: giet_dung`,
  `run False`. Nguyên mẫu (M1 dưới đây): `giết_đúng=36`, `run True`. Không giả lập: base và nguyên mẫu cùng `CA 3/3 · LUOT 29/29 · DOT BIEN 36/36 · HONG 0 · TU_KIEM 3/3`.
  Giả lập Linux chỉ làm sống ba trong bốn đột biến (`db_w6_tu_choi_van_chot` vẫn bị giết dưới giả lập); trên nt cả bốn sống — số đo quyết định là Desktop.
- **Desktop (đo 2026-11-20T08:08–08:15Z, clone `94cbb36` tree `2a38dae8`, sạch sau đo; `ops/reviews/wp433p2bw-spec-r1/desktop/`, zip sha256
  `4887d8ca09c325788c316b782263b8bcbcbe120ac15b26e48fe34f6b9d9c0a66`):** hình dạng đường `expanduser= '…\\hd/.tra_luat_config.json'` ·
  `join= '…\\hd\\.tra_luat_config.json'` · `bang_chuoi= False` · `bang_sau_chuan_hoa= True`. Base hai lần: `rc=1`, đúng bốn `SONG_SOT` như trên,
  `DOT BIEN: dự_kiến=36 chạy=32 giết_đúng=28 chỉ_posix=4`, `VẾ SAI: giet_dung`, `RUN False`. Nguyên mẫu hai lần: `rc=0`,
  `CA: dự_kiến=3 chạy=2 đạt=2 chỉ_posix=1 · LUOT: dự_kiến=29 chạy=27 đạt=27 chỉ_posix=2 · DOT BIEN: dự_kiến=36 chạy=32 giết_đúng=32 chỉ_posix=4 · HONG: 0 · TU_KIEM: 3/3`, `RUN True`.

## 1. `write_set`

```
scripts/test_fragments/wp433_gws_cred_dich_ngoai_kho_b.py
scripts/tl_test_fragments_bundled.py
```

KHÔNG `scripts/tl_gws.py`, KHÔNG `RELEASE_MANIFEST.json`. Bundled chỉ sinh bằng `generate_bundled_module_bytes(scripts/test_fragments)`. **Điều kiện trước khi cấp
lease (E2):** comment của chủ kho trên #433 cấp ngoại lệ bundled nêu đúng `packet_id` `GWS-CRED-DICH-NGOAI-KHO-P2BW`, đúng một tệp
`scripts/tl_test_fragments_bundled.py` và sha256 của đặc tả này đã đóng băng; lease trỏ URL comment. Phiên land tái sinh manifest.

## 2. `ngoai_pham_vi`

- Đổi cách dựng đường `expanduser("~/…")` trong mã: không (cùng quyết định Q1 của packet N).
- `_DB`, `_TU_KIEM`, `_LUOT_DU_KIEN`, `_DU_KIEN`, `_KHAI`, các hàm ca và vị từ nhãn của fragment P2b: giữ nguyên; chỉ bộ quan sát trong `_Rig.goi` đổi.
- `secrets-set` dùng bundle chưa kiểm kiểu: nợ riêng nếu chủ kho muốn (`wp433-secrets-set-bundle-khong-phai-dict`, đã ghi ở đặc tả N §2).
- Không sửa `ops/**`, `.github/**`, `scripts/tl_selftest.py`, fragment khác, `RELEASE_MANIFEST.json`, `changelog.d/*`, `VERSION`, `CHANGELOG.md`, `SKILL.md`.

## 3. `muc_tieu`

| # | mục tiêu | tệp |
|---|---|---|
| M1 | Trong fragment P2b, ĐÚNG năm chỗ, nguyên văn ở `ops/reviews/wp433p2bw-spec-r1/p2bw.diff`: (a) thêm hàm mức module `_nc = lambda p: os.path.normcase(os.path.normpath(os.fspath(p)))` (kèm chú thích nêu nợ); (b) trong `_Rig.goi`, `cfg` lấy `_nc(self.cfg)` thay `self.cfg`; (c) `op`: điều kiện đếm đọc đổi `f == cfg` thành `isinstance(f, (str, os.PathLike)) and _nc(f) == cfg` (giữ nguyên vế kiểm chế độ mở); (d) `kd`: `dem["chot"] += _nc(dich) == cfg`; (e) `gh`: `dem["ghi"] += _nc(path) == cfg`. Không sửa dòng nào khác. | fragment P2b |
| M2 | Tái sinh bundled; không sửa tay. | bundled |

## 4. `nghiem_thu`

| # | ca (nền) | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|---|
| N1 | P2b trên Linux | `run()` True, `CA 3/3 · LUOT 29/29 · DOT BIEN 36/36 · HONG 0 · TU_KIEM 3/3`, BẰNG base. | Bộ đếm khác base ⇒ đỏ. |
| N2 | P2b trên Linux, giả lập hình dạng nt (`chay_p2b_gia_nt.py`) | Candidate `run()` True 36/36; base `run()` False, đúng ba đột biến `SONG_SOT` như §0 và `VẾ SAI: giet_dung`. | Base không đỏ ⇒ phép giả lập không đo cơ chế ⇒ dừng. |
| N3 | gate | selftest N/N hai số bằng nhau, N = N_base (không thêm ca); `test-fragments-check --json` `ok: true`; `bundle_fragment_check.py --json` `ok: true`, `failed: []`; lane worker `release-manifest` tạm + `release-verify --strict` `ok: true`; `git diff --check` sạch; `doctrine-scan`, `adr-song` rc 0; ruff F delta 0. | Bất kỳ vế nào khác. |
| N4 | đo native (§4c) | Hồ sơ PR ghi lệnh, shell, exact head/tree, đầu ra thô, rc và kết luận của MỌI phép bắt buộc ở §4c. | Thiếu, trái kỳ vọng hoặc `KHÔNG ĐO ĐƯỢC` ⇒ không land. |

### 4b. Đột biến

Không thêm đột biến mới: bốn đột biến hiện có (`db_w6_tu_choi_van_chot`, `db_w6_tu_choi_van_doc`, `db_w6_tu_choi_ghi_lai`, `db_w6_encode_ghi_cu`)
CHÍNH LÀ phép đo của M1 — trên nt chúng phải chuyển từ `SONG_SOT` sang `GIET` (đúng ca, lượt, nhãn) mà không đột biến nào khác đổi hạng.

### 4c. Đo native Windows (`DESKTOP-T9R33P2`, dự phòng VM)

Chung như packet N §4c (ghim exact head/tree; clone `git -c core.longpaths=true`; `python`; rig dưới thư mục phiên; dọn đúng thứ mình tạo; offline).

| # | bắt buộc | dựng / lệnh | kỳ vọng |
|---|---|---|---|
| D1 | có | `run(tl)` fragment P2b trên base `94cbb36` và trên candidate, mỗi vế một tiến trình, mỗi vế HAI lần | base `False`, `giết_đúng=28`, đúng bốn `SONG_SOT` như §0 (phản chứng); candidate `True`, `DOT BIEN … giết_đúng=32 chỉ_posix=4 · HONG 0 · TU_KIEM 3/3`, `CA 3 chạy 2 · chỉ_posix 1`, `LUOT … chỉ_posix=2`; hai lần y hệt |
| D2 | có | Cùng máy: `run(tl)` các fragment #433 khác (P2a, packet 1, C1, R, N) trên candidate | `True` tất cả (không đổi so với base — write set không chạm chúng) |
| D3 | có (T3) | Tái sinh manifest trong PR manifest sau land, selftest + gate lane LAND | xanh |

## 5. `pham_vi_e`

Không chạm E4, E5: chỉ sửa test; dữ liệu giả, thư mục tạm, không mạng, không LIVE, không đẩy Package.

## 6. `luat_dung`

- Trần lời gọi Codex theo `ADR-0055`; trần kích thước `ADR-0053` đo bằng numstat thật; vượt ⇒ DỪNG.
- §0 lệch trên base thật (ba so chuỗi trong `_Rig.goi`, dòng `cfgp = os.path.expanduser(…)` của `tl_gws.py`) ⇒ dừng, revision.
- D1: candidate không `True`, hoặc base không đỏ đúng bốn đột biến ⇒ dừng, revision (nguyên nhân không phải so chuỗi như §0 khai).
- Một đột biến P2b đổi hạng trên Linux so base ⇒ dừng.
- Chưa có comment ngoại lệ bundled đúng `packet_id` ⇒ không cấp lease (**E2**). Đặc tả chờ chủ kho duyệt băm theo `ADR-0067` (**E2**).

## 7. `hinh_dang_ke_thua`

Lớp "cổng đỏ vì THƯỚC ĐO so chuỗi, không vì mã" — y hệt `wp433-pk1-n84-windows` (packet N M1), và họ "ca có MẶT khác ca có ĐO" của `CLAUDE.md`:
ở đây ba bộ đếm CÓ MẶT trên nt nhưng không ĐO (luôn 0), nên nhãn của chúng xanh vô điều kiện. Rút ra: mọi so đường dẫn trong fragment
#433 phải qua `normcase(normpath(·))`; lần quét này chỉ tìm thấy ba chỗ trong P2b (chỗ còn lại đã sửa ở packet N).

## 8. `chua_do_duoc` và dự toán

- Numstat nguyên mẫu (đo, base `94cbb36`, bundled tái sinh bằng generator): `wp433_gws_cred_dich_ngoai_kho_b.py` 5/4 · `tl_test_fragments_bundled.py` 1/1 ⇒ **2 tệp, 6 dòng thêm, 5 xoá**.
- Desktop: đã đo (§0). Chưa đo D2 (năm fragment #433 khác trên candidate) — việc của phiên thi hành; write set không chạm chúng.

## 9. Lịch sử và quyết định

- Chủ kho 2026-11-20: ghi nợ `wp433-p2b-w6-windows`, miễn trừ cho packet N (delta 0); sau khi N land: "Đồng ý, bắt đầu đi".
- Không có quyết định mở: sửa thuần test, không đổi hành vi mã.

## 10. Nhật ký revision

- 2026-11-20T08:1xZ (phiên con của điều phối #1206): bản 1, đo §0 trên `94cbb36` (Linux + Desktop).
