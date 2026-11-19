<!-- Sao nguyen van truong body cua readback-pr-1415.json (PR #1415, head 6e49b68). Nhan: loi_khai_co_neo. -->

Packet #433 revision 2 generation 1 (P2a), đặc tả `GWS-CRED-DICH-NGOAI-KHO-A` r1.

## Định danh

| | |
|---|---|
| Issue / lease | #433 · `wp433-r2-g1-claude` (`ops/leases/wp433-r2-g1-claude.yaml` trên `ops/wp433-p2a-spec`, commit `e6d056c9428073cb307691e9d8c91caeac5dc735`; `lease_publish.py check` rc 0 lúc 2026-11-19T07:58:18Z) |
| Đặc tả | `ops/specs/GWS-CRED-DICH-NGOAI-KHO-A-r1.md`, sha256 `b0065947f941a122716cff1b15a81ad65fe9b92a15fb9effad1456100c64624d` (tự đo, khớp lease) |
| Base | `3b647461db7c8ded1bddd9aafc5c6aa5eead223f` (tree `306ec6c89a18ac12988d0b324a0867f6d3e91a54`) |
| Exact head | `6e49b6807886e1d42b22245dd394a2f19a99bfb5` |
| Tree | `6d49d42d31e6b415f9c5472258365bab828ee605` |
| Numstat `base..head` | `scripts/test_fragments/wp433_gws_cred_dich_ngoai_kho.py` +389/−0 · `scripts/tl_gws.py` +48/−19 · `scripts/tl_test_fragments_bundled.py` +1/−0 ⇒ 3 tệp, **438 dòng thêm** (trần 550) |
| Ngoại lệ bundled | https://github.com/ducthangho/tra-luat/issues/433#issuecomment-7002145681 |

Một commit. Không sửa thân `_kiem_dich_ghi`, `_trong_kho_git`, `_ghi_nguyen_tu_0600`; không đụng `RELEASE_MANIFEST.json` (phiên land tái sinh).

## M1–M5

- **M1** `_duong_dich_chuan(p, cwd)`: ghép `cwd` theo chuỗi (không `abspath`/`normpath`/`realpath`), bỏ thành phần rỗng và `.`; từ chối NUL, chuỗi chỉ khoảng trắng, còn `..`, và gốc `/`. Lý do `đường không hợp lệ: <repr>`.
- **M2** `_dich_cred_gws(cfgdir_tho)` dùng chung cho W4 và W5: trên POSIX gọi `_kiem_dich_ghi(dest, "/", (*thành_phần, "credentials.json"))` nên luật (b) `lstat` mọi tổ tiên từ `/` tới chính tệp. Nền khác trả đích như base. Ghi bằng `_ghi_nguyen_tu_0600`; lời gọi chốt và writer nằm trong một `try … except OSError` ở mỗi chỗ. W4 kiểm kiểu và encode trước; điều kiện vào nhánh là `"gws_cred" in bundle and bundle["gws_cred"] != ""`.
- **M3** W4 bị từ chối hoặc lỗi ghi: đúng một dòng `[bootstrap] ✗ <cụm>: <chi tiết>` ra stderr, `degraded = True`, không in `✓ gws cred`. W5 trả `(False, "<cụm>: …")`; thành công trả `(True, dest)` với `dest` là đường đã kiểm.
- **M4** Fragment `wp433_gws_cred_dich_ngoai_kho`: 11 ca, 46 lượt, 37 đột biến (`_DU_KIEN` tách khỏi `_DB`), 3 tự kiểm phân hạng, sổ lượt `_LUOT_DU_KIEN`, bộ quan sát bốn pha có nhật ký, mọi đầu ra ra stderr.
- **M5** `scripts/tl_test_fragments_bundled.py` sinh bằng `generate_bundled_module_bytes("scripts/test_fragments")`, không sửa tay.

## N1–N12 đã đo trên exact head

Linux, Python 3.13.18, giờ UTC theo máy. Base và head là hai clone thường (`.git` là thư mục) dựng trong cùng một lệnh, `core.abbrev=7`, `autocrlf=false`, `eol=lf`. `/tmp/.git` không tồn tại lúc đo.

| # | Lệnh | rc | Bằng chứng dương |
|---|---|---|---|
| N1–N9 | `run(tl)` của fragment mới trên clone head (07:41:05Z) | 0 | `CA: dự_kiến=11 chạy=11 đạt=11 bỏ_qua=0 chỉ_posix=0 · LUOT: dự_kiến=46 chạy=46 đạt=46 bỏ_qua=0 chỉ_posix=0 · DOT BIEN: dự_kiến=37 chạy=37 giết_đúng=37 bỏ_qua=0 chỉ_posix=0 · HONG: 0 · TU_KIEM: 3/3`, `run` True |
| N8 | `python3 ops/cloud_agent_creds_test.py` base và head (07:44:30Z–07:49:36Z) | 0 / 0 | cả hai `CA: 60/60 dat`, `DOT BIEN: 91/91 bi giet dung ly do`, `TONG: DAT`; tập dòng theo ca của hai log bằng nhau |
| N8 | fragment packet 1 trên head | 0 | `CA … chạy=18 đạt=18 · DOT BIEN … chạy=30 giết_đúng=30 · HONG: 0`, `run` True |
| N10 | `python3 scripts/tl.py --selftest`, base rồi head, tuần tự (07:49:55Z–07:58:08Z) | 0 / 0 | base `1779/1779`, head `1780/1780`; khác biệt duy nhất giữa hai danh sách ca là thêm `[OK] wp433_gws_cred_dich_ngoai_kho` |
| N10 | `tl.py test-fragments-check --json` | 0 | `ok: true`, `expected_sha256 == actual_sha256 == be32c696…` |
| N10 | `.github/checks/bundle_fragment_check.py --json` | 0 | `ok: true`, `failed: []` |
| N11 | `release-manifest --root . --out <tạm>` rồi `release-verify <tạm> --root . --strict --json` | 0 / 0 | `ok: true`, `expected_file_count == checked_file_count == 185` |
| N12 | `ruff check --select F` | — | `tl_gws.py` base 95, head 95, tập thông điệp bằng nhau (delta 0); fragment và bundled: `All checks passed!` |
| N12 | `git diff --check base..head` | 0 | |
| N12 | `packet_loop.py doctrine-scan --root .` / `adr-song --root .` | 0 / 0 | `sạch — đã quét 12 tệp` / `66 ADR … khớp 1–1` |
| N12 | `git diff --numstat base..head` dưới `pipefail` + bộ kiểm | 0 | 3 dòng, tập đường bằng write set, tổng thêm 438 ≤ 550 |

### Phép đo làm cổng đỏ (đã chạy)

| Phép | Kết quả |
|---|---|
| N8: đổi một ký tự trong neo `PD2` của `tl_gws.py` | `cloud_agent_creds_test` rc 1, `DOT BIEN: 90/91`, `TONG: DO`, dòng `PD2_luon_tra_duong_dan: HONG neo phải xuất hiện đúng 1 lần (thấy 0)` |
| N8: đổi một ký tự trong một neo của fragment packet 1 | fragment ấy `HONG: 1`, `giết_đúng=29`, `run` False |
| N10: chuyển riêng fragment mới ra khỏi `scripts/test_fragments` | selftest `1779/1779` (bằng N_base, đỏ vế N_base + 1) |
| N10: `run` của fragment trả `False` | selftest `1779/1780`, rc 1 |
| N10: giữ bundled của base | `bundle_fragment_check` `TEST_ID_SET_MISMATCH` rc 1; `test-fragments-check` `GENERATED_BUNDLE_STALE` rc 2 |
| N10: sửa tay một ký tự trong bundled | `test-fragments-check` `GENERATED_BUNDLE_STALE` rc 2 (`bundle_fragment_check` vẫn `ok: true`: nó không so băm) |
| N11: sửa một byte / xoá một tệp trong gói sau khi sinh manifest tạm | `release-verify` rc 2, `ok: false` ở cả hai |
| N12: thêm tên chưa định nghĩa | ruff 96 (delta 1) |
| N12: khoảng trắng cuối dòng | `git diff --check` rc 2 |
| N12: numstat dựng tay | tổng 550 xanh; 551 đỏ (iii); đường ngoài write set đỏ (ii); cột `-` đỏ (ii); rỗng đỏ (i); base không tồn tại rc 128 |

### Phản chứng bộ đo trên bản sao fragment (ngoài numstat), 19/19 đúng kỳ vọng

Mỗi phép đổi đúng một thứ trên bản sao rồi gọi `run(tl)`.

| Phép | `run` | Dòng nêu vế |
|---|---|---|
| đối chứng (không đổi gì) | True | không `VẾ SAI` |
| `pc_tiem_khong_ghi` | False | `ghi_loi_theo_pha · W4.mkstemp · tiem` |
| `pc_bo_luot` (bỏ `W5.cfg_la_tep`) | False | `LUOT: dự_kiến=46 chạy=45`, `VẾ SAI: so_luot`, ca vẫn đạt 11/11 |
| `pc_bo_ca_moi` (gỡ `m1_bien`) | False | `so_ca`, `so_luot` |
| `pc_bo_qua_ngoai_danh_sach` | False | `bo_qua_trong_ds` |
| `pc_bo_qua_khi_ho_tro` | False | `bo_qua_co_can_cu` |
| `pc_probe_quyen`, đối chứng (`nt` cố định, probe thành công) | True | lượt chạy, không `BO_QUA` |
| `pc_probe_quyen` (`PermissionError`, `errno` 13, `winerror` 5) | False | `probe hardlink: ('PermissionError', 13, 5)`, `bỏ_qua=0`, đột biến 37 `TIN_DUNG_GIA` |
| N9: thêm ID vào `_DU_KIEN` | False | `so_dot_bien` |
| N9: đổi lượt đích `db_w5_bo_chot` sang `W4` | False | `db_w5_bo_chot: TIN_DUNG_GIA` |
| N9: tắt nhãn `goc_1` | False | `db_lstat_tho: TIN_DUNG_GIA` |
| N9: neo khớp 2 lần | False | `HONG: 1` |
| N9: ép bỏ một ca `posix` trên POSIX | False | `so_luot`, `nen` |
| N9: bộ phân hạng bỏ so lượt | False | `tự kiểm GIET ≠ TIN_DUNG_GIA`, `TU_KIEM: 2/3` |
| N9: `tu_kiem_doi_kieu` ném thẳng `AssertionError`, không qua `except` | False | `TU_KIEM: 2/3` (thiếu `__context__` kiểu `AttributeError`) |
| N9: in tổng kết ra stdout | False | (f) |

**P3 của review đặc tả lượt 6 — đã làm** (trên bản sao, cùng thiết lập `nt` cho bộ phân loại): probe ném `OSError` có `winerror` 1, rồi 50. Cả hai cho `BO_QUA nguyen_tu·W5.hardlink`, `LUOT … chạy=45 đạt=45 bỏ_qua=1`, `DOT BIEN … chạy=36 giết_đúng=36 bỏ_qua=1` (u = h = 1). `run` vẫn False ở đây vì máy đo là POSIX, nơi vế `nen` đòi u = 0; đó là vế duy nhất sai. Thêm một đối chứng: `winerror` 1 mà không cố định `nt` thì lượt đỏ, không bỏ qua.

## Chưa đo

- Windows thật: nhánh `nt` của `_dich_cred_gws`, các ca nền `mọi` trên Windows, phép thử `os.link` thật và mã `winerror` thật. Bộ phân loại bỏ qua chỉ được đo bằng lỗi giả trên Linux.
- TOCTOU giữa lúc kiểm và `os.replace` (giới hạn đã khai ở §2 đặc tả).
- macOS và máy có tổ tiên của `cfgdir` là symlink. Phép đo chỉ-đọc duy nhất: trong container này `~/.config/gws` mặc định được chốt cho phép.
- CI của PR này chưa chạy lúc viết thân; lane LAND (`release-verify RELEASE_MANIFEST.json --strict`) là việc của phiên land.
- `full gate` 8 bước: không chạy; chỉ các lệnh trong bảng trên.

## Ghi chú cho reviewer

- Điểm tự chọn trong phạm vi đặc tả: (1) tín hiệu `TinHieuChotCa` mang đúng một bộ (ca, lượt, nhãn) là nhãn đỏ đầu tiên, ca dừng tại đó; (2) `_duong_dich_chuan` tách phép từ chối NUL/khoảng trắng thành một `if` riêng trước khi ghép để đột biến `db_nhan_goc` không đỏ sớm ở lượt `nul`; (3) số ca `bỏ_qua` in hằng 0 vì không có trạng thái ấy ở mức ca; (4) vế `nen` trên nền khác POSIX so với bộ hằng (7, 27, 21); (5) lỗi probe hardlink ngoài danh sách cho phép thành tín hiệu có nhãn là chính dòng chẩn đoán.
- Hành vi đổi có chủ ý theo đặc tả: W5 thành công trả đường đã chuẩn hoá (tuyệt đối) thay cho `join` của giá trị thô; `gws_cred` có mặt mà sai kiểu (kể cả `0`, `None`) bị từ chối với `dữ liệu không hợp lệ: gws_cred` thay vì cảnh báo thiếu.
- Ghi chú môi trường đo: selftest cần commit `358451e8` (base của fragment `wp1099`) trong object store; clone cục bộ không mang nó nên tôi cho bốn clone đo trỏ `alternates` về kho chính, áp như nhau cho base và head. Lượt selftest đầu tiên của base chết vì tôi chạy bốn selftest song song và chúng giẫm lên cùng một tệp `/tmp/tl_selftest_pin_cfg38.json`; số trong bảng là lượt chạy lại tuần tự.

---
_Generated by [Claude Code](https://claude.ai/code)_
