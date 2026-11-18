<!-- Sao nguyen van truong body cua readback-pr-1394.json (PR #1394, head 80f926c). Nhan: loi_khai_co_neo. -->

Packet #433 `NLM-GWS-DICH-NGOAI-KHO` revision 1 generation 1 (packet 1 trong 2; W4/W5 và junction thuộc `GWS-CRED-DICH-NGOAI-KHO`).

## Neo

| trường | giá trị |
|---|---|
| lease | `ops/leases/wp433-r1-g1-claude.yaml` trên `ops/wp433-r1-g1-lease` (`a2a3d5c6bfa3159f8066da4dea36398a00a46364`) |
| đặc tả | `ops/specs/NLM-GWS-DICH-NGOAI-KHO-r1.md`, sha256 `3721e4684c12a22ab165a032c409ddb979dc9786e8862f9cdbaeba4bd7a74f88` (đo lại bằng `git show … \| sha256sum`: khớp) |
| base | `eca1d125b82783a6a736c7023751ba53cc9a49c8` |
| head H | `80f926c9866e4ab2c32a4253359b72c4de511962` (một commit, một lần push) |
| tree | `5f12998f24ea1cd21062480e8849c9396276759b` |
| ngoại lệ bundled | https://github.com/ducthangho/tra-luat/issues/433#issuecomment-6973856830 — `scripts/tl_test_fragments_bundled.py` sinh bằng `generate_bundled_module_bytes`; `RELEASE_MANIFEST.json` KHÔNG có trong diff (phiên land tái sinh) |

`git diff --numstat base..H` (rc 0, đúng 3 dòng, tập đường == write set, tổng thêm **448 ≤ 450**):

```
353	0	scripts/test_fragments/wp433_nlm_gws_dich_ngoai_kho.py
94	42	scripts/tl_gws.py
1	0	scripts/tl_test_fragments_bundled.py
```

## Thay đổi

- `_kiem_dich_ghi(dich, goc, thanh_phan)` (M1): (a) cha của đích không nằm trong kho git (`_trong_kho_git`); (b) `goc` và mọi tiền tố tới chính tệp đích, nếu đang tồn tại, không phải symlink (`S_ISLNK`). Không tạo, không ghi.
- `_kiem_jar_nlm` (M2): jar là dict khác rỗng, khoá bằng nguyên văn một phần tử `_NLM_AUTH_RELS`, giá trị là `str` encode UTF-8 được.
- W1 `cmd_nlm_auth_pull`, W2 `cmd_bootstrap`, W3 `_nlm_auth_load`: kiểm jar và đích của mọi khoá trước mọi `makedirs`/ghi; ghi từng tệp bằng `_ghi_nguyen_tu_0600`. W3 kiểm trước chốt chống hạ cấp.
- W6 (M3): `degraded = False` dời lên trước W6; kiểm jar một lần ngay sau giải mã; chốt đích config trước lần đọc phục vụ merge; ghi nguyên tử; không lưu `nlm_auth` bị từ chối vào config; lỗi ghi config thành `✗ ghi lỗi` + rc 1 (bỏ dòng `✓ token nạp env (ghi config lỗi…)`).
- M4: mỗi lần từ chối in đúng một dòng `[<thẻ>] ✗ <cụm>: <chi tiết>`; đường và khoá qua `repr`.
- Fragment `wp433_nlm_gws_dich_ngoai_kho` (M5, M6): 18 ca, 30 đột biến chép bảng §4b, phân hạng theo (ca, lượt, nhãn), đột biến áp trên bản sao trong bộ nhớ.

Thân `_trong_kho_git` và `_ghi_nguyen_tu_0600` không đổi. Các neo PD của `ops/cloud_agent_creds_test.py` vẫn khớp đúng một lần (đếm bằng `grep -cF`: 1, 1, 1 cho ba neo đã thử). Hai dòng thành công mà `wp727_tl_gws_refresh` khoá giữ nguyên.

## Đo được (Linux, Python 3.13.18, head H)

Base và head dựng bằng cùng một script (`git clone` thường, `core.abbrev 7`, `autocrlf false`, `eol lf`), hai clone riêng.

| # | lệnh | rc | bằng chứng |
|---|---|---|---|
| N11 | `python3 scripts/tl.py --selftest` trên base | 0 | `== tl selftest 1778/1778 ==` |
| N11 | cùng lệnh trên H | 0 | `== tl selftest 1779/1779 ==`; diff danh sách `[OK]`/`[FAIL]` giữa hai vế: đúng một dòng thêm `[OK] wp433_nlm_gws_dich_ngoai_kho`, 0 ca đỏ |
| N10(b) | dòng tổng kết của fragment (stderr) | — | `CA: dự_kiến=18 chạy=18 đạt=18 bỏ_qua=0 · DOT BIEN: dự_kiến=30 chạy=30 giết_đúng=30 bỏ_qua=0 · HONG: 0` |
| N11 | `python3 scripts/tl.py test-fragments-check --json` | 0 | `ok: true`, `status: current` |
| N11 | `python3 .github/checks/bundle_fragment_check.py --json` | 0 | `ok: true`, `failed: []`, `case_count: 13` |
| N12 | `release-manifest --root . --out <tạm>` rồi `release-verify <tạm> --root . --strict --json` | 0 | `ok: true`, `185 == 185` |
| N8 | `python3 ops/cloud_agent_creds_test.py` trên base và trên H | 0 / 0 | cả hai: `CA: 60/60 dat` · `DOT BIEN: 91/91 bi giet dung ly do` · `TU KIEM PHAN HANG: DAT (4 dot bien)` · `TONG: DAT`; hai log giống nhau sau khi bỏ số giây |
| N13 | `ruff check --select F` (0.17.5) fragment + bundled | 0 | `All checks passed!` |
| N13 | `git diff --check` | 0 | rỗng |
| N13 | `packet_loop.py doctrine-scan --root .` / `adr-song --root .` | 0 / 0 | — |
| §6 | lệnh quét chỗ ghi của §0.1 trên H | — | chỗ ghi credential còn lại ngoài chốt chỉ là W4 (1782–1784) và W5 (1931–1933), thuộc packet 2; không có chỗ thứ bảy |

**Vế âm trên base** (cùng các ca, nguồn `tl_gws.py` của base nạp trong bộ nhớ): 16/18 ca đỏ, khớp §0.2 (ví dụ `w1_pull_rel_thoat` đỏ `khong_thoat`, `khong_jar`, `ma`, `stderr`). Hai ca xanh trên base là `w6_chi_config_ngoai_kho` (vế dương) và `d5_khong_claude` (răng từ `db_tao_claude`, đúng N9).

**Bảng đột biến §4b**: 30/30 giết đúng (ca, lượt, nhãn). `db_tao_claude` chỉ làm hỏng `khong_claude`, không hỏng `codex_da_nap`. Bốn dòng E (10, 11, 22, 24) chết bằng đúng ngoại lệ đã khai ở đúng lượt.

**Tự kiểm N10 trên bản sao fragment trong bộ nhớ** (mỗi dòng một lượt `run`):

| phép | kết quả |
|---|---|
| (1) đổi lượt đích `db_w3_bo_kiem_jar` sang `N1k-W1` | `run` False, đột biến ấy `TIN_DUNG_GIA` |
| (2) tắt nhãn `khong_khoa_la` của `N1k-W1` | `run` False, `db_w1_bo_kiem_jar` `SONG_SOT` |
| (3) neo khớp 2 lần | `run` False, `HONG: 1` |
| (4) ép bỏ qua ca symlink trên POSIX | `run` False (`bỏ_qua=6`, đột biến `bỏ_qua=9`) |
| (5) in tổng kết ra stdout | `run` False |
| (6) dòng 11 khai lượt `N3.1-W1` | `run` False, `TIN_DUNG_GIA` |
| (7) dưới `db_w6_bo_symlink` | `w6_chi_config_trong_kho` (HOME = `K/home`) XANH, HOME = `K` XANH, chỉ `w6_symlink_config` ĐỎ |

Trong fragment, bốn dòng tự kiểm phân hạng (`tu_kiem_attributeerror` → TIN_DUNG_GIA, `tu_kiem_chu_thich` → SONG_SOT, `tu_kiem_sai_luot` → TIN_DUNG_GIA, `tu_kiem_neo_lap` → HONG) là điều kiện để `run` trả True.

## Lệch so với nguyên văn tiêu chí — cần người duyệt quyết

- **N13 ruff F trên `scripts/tl_gws.py`: delta là −2, không phải 0.** Base 91 F821 + 4 F401 + 2 F811; H 91 F821 + 3 F401 + 1 F811. Không có phát hiện mới. Hai phát hiện cũ biến mất vì `import stat` ở đầu tệp nay được dùng (`stat.S_ISLNK`): `F401 stat imported but unused` (dòng 15) và `F811 Redefinition of unused stat` (dòng 2258 ở base). Không dòng import nào bị sửa.
- **N10(5) vế thứ hai chưa chạy**: đã đo `run` trả False khi in ra stdout; chưa dựng cây tạm để chạy `bundle_fragment_check.py` cho ra `ok: false`.

## Chưa đo được

- Windows: chưa chạy. Nhánh giả lập `_trong_kho_git` của ca `mot_dong` (N8.2b) và nhánh bỏ qua khi không tạo được liên kết chưa từng thực thi. Packet này không chặn junction/reparse (theo §2).
- CI trên H: chưa có lượt nào lúc mở PR.
- `RELEASE_MANIFEST.json` committed lệch bundled trên PR head (đúng thiết kế §0.4, N12); phiên land tái sinh.
- Fragment chạy khoảng 22 giây trên máy này (34 lượt nạp `tl_gws` trong bộ nhớ); chưa đo trên runner CI.
- Bundle `nlm_auth` thật trên Drive và máy thật có dotfile là symlink: không đo (E4, §8).

Chưa gọi Codex. Không merge, không approve. Mọi push thêm chờ phiên điều phối xác nhận chủ kho duyệt (ADR-0060 M5).

---
_Generated by [Claude Code](https://claude.ai/code/session_015Gtxrc8gnsVH6di9W6eJsd)_
