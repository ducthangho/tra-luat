# Đặc tả packet LAND-EVIDENCE-KHAI-PHAI-CO-NGUON — r2 (đợt g2)

Đặc tả đóng băng. Sửa tệp này là đổi băm; muốn đổi thì soạn `land-evidence-khai-phai-co-nguon-r3.md`, không sửa đè.
Soạn bởi phiên Claude Code `session_017khPoiSXW9Yvefabg6MWaH` ngày 16-10-2026. r2 **không thay** r1
(`ops/specs/land-evidence-khai-phai-co-nguon-r1.md`, sha256 `063ccaa692372d8f431af07fcb86acccef32435e4b69e7a63e3b0a4ee67e02dd`):
mọi luật L1–L5, Q2, Q3, Q5, Q6 và bảng nghiệm thu g1 của r1 giữ nguyên. r2 chỉ sửa **Q1** (chỗ nối CI của g2 và điều kiện xong
packet) và ghi lại **Q4** (trần g1 đã nâng). Các lựa chọn dưới đây là KHUYẾN NGHỊ; chủ kho chấp nhận bằng chính comment cấp
lease g2 neo băm tệp này.

## packet_id · packet_issue

- `packet_id`: `land-evidence-khai-phai-co-nguon`
- `packet_issue`: [#773](https://github.com/ducthangho/tra-luat/issues/773)
- `revision`: 2

## vi_sao_co_r2 (đo được, không suy)

1. **r1 Q1 giả định sai rằng g1 land được một mình.** Trên PR #778, `gate-registry (ubuntu-latest)` và `gate-ops (ubuntu-latest)`
   ĐỎ với dòng `ĐỎ: test sống chưa đăng ký: ops/land_evidence_nguon_test.py`. `.claude/dev/ci_dang_ky_test.py::kiem` đòi mọi
   `*_test.py` sống phải có tên trong `MOI` hoặc `DA_NOI`; `gate-ops` ca `k01_so_dang_ky_nhan_muc_da_noi` đòi sổ sạch. Nên
   g1 và g2 phải land CÙNG nhau.
2. **r1 Q1 đặt sai chỗ nối.** Chỗ đúng là MỘT mục trong `MOI` của `.claude/dev/ci_dang_ky_test.py`, không phải `ci.yml`:
   mục `MOI` do chính `gate-registry` chạy (`--chay`) và khớp dòng tổng kết bằng mẫu; mục `DA_NOI` thì đòi một workflow gọi
   tên tệp (chốt "CI không gọi mục đăng ký"). Nguyên mẫu trên bản sao nháp (thêm một dòng `MOI`): `python .claude/dev/ci_dang_ky_test.py`
   rc=0.
3. **Trần g1:** chủ kho nâng 600 → 700 dòng thêm tại
   [issuecomment-6221230175](https://github.com/ducthangho/tra-luat/issues/773#issuecomment-6221230175). g1 ở `98d7d25`: 2 tệp / 700.

## quyet_dinh (khuyến nghị, chủ kho chấp nhận bằng comment cấp lease g2)

- **Q1-r2 — chỗ nối:** g2 thêm đúng MỘT dòng vào `MOI` của `.claude/dev/ci_dang_ky_test.py`:
  `"ops/land_evidence_nguon_test.py": r"(?s)^CA: (\d+)/(\d+) dat$.*^DOT BIEN: [1-9]\d*/[1-9]\d* bi giet dung ly do$.*^TONG: DAT$",`
  Mẫu có ĐÚNG HAI nhóm bắt: `bang_chung_xanh` chỉ đòi `N == N > 0` khi `len(m.groups()) == 2` — nhiều nhóm hơn thì phép so bị
  BỎ QUA âm thầm (đo trên mã hiện có). Không sửa `ci.yml`, không thêm mục `NHE`/`MAU_DAY_DU`.
- **Q1-r2 — cách land:** commit g2 đẩy vào CHÍNH nhánh `agent/wp773-g1-claude` (PR #778), để g1 và g2 vào master trong một merge.
  Lease g2 dùng nhánh ấy với `branch_ownership: shared_with_g1` (cùng executor, cùng packet).
- **Q1-r2 — xong packet:** #773 xong khi PR #778 (g1 + g2) land với `gate-registry` và `gate-ops` XANH trên head land.
- **Q4-r2 — trần g2:** 1 tệp, ≤ 5 dòng thêm.

## write_set (g2)

1. `.claude/dev/ci_dang_ky_test.py`

Đo trước khi cấp: `python ops/lease_publish.py ai-dang-giu .claude/dev/ci_dang_ky_test.py` phải ra `NGƯỜI_GIỮ 0` sau khi fetch đủ
ref (`ls-remote --heads` = `for-each-ref`, so TẬP TÊN). Đo 2026-10-16T17:22Z: `NGƯỜI_GIỮ 1` — lease
`wp748-r14-g14-claude-windows-20261016`, hết hạn `2026-10-16T23:34:32Z`.

## nghiem_thu (g2)

| Mục | Tiêu chí | Phép đo làm ĐỎ |
|---|---|---|
| diff | `git diff` trên `.claude/dev/ci_dang_ky_test.py` đúng 1 dòng thêm, 0 dòng xoá; không tệp nào khác ngoài write set g1 + g2. | Dòng thừa, tệp lạ. |
| registry | `python .claude/dev/ci_dang_ky_test.py` rc=0 cục bộ. | rc≠0. |
| mẫu | Mẫu khớp đầu ra thật của `ops/land_evidence_nguon_test.py` và nhóm bắt ra `(N, N)` với N>0; đầu ra có `TONG: DO` hoặc `CA: 13/14` thì KHÔNG khớp / không qua `bang_chung_xanh`. | Khớp đầu ra hỏng. |
| CI | Trên head PR #778 sau g2 (đã merge `origin/master`): `gate-registry`, `gate-ops` và mọi check khác XANH; log `gate-registry` có `CI_DANG_KY ops/land_evidence_nguon_test.py: ĐẠT rc=0`. | Check đỏ, hoặc dòng ấy vắng. |
| review | Codex CLI read-only trên exact SHA của head g2: P1=0, P2=0, P3=0. | Finding mở. |

## phu_thuoc

- PR #787 (gắn nguồn cho 4 lời khai trong `ops/land/pr772-wp766-land-evidence.yaml`) phải vào master trước khi #778 merge
  `origin/master`: hồ sơ ấy vào master sau cutover nên không được miễn trừ, và đang ĐỎ 4×L1 trên bộ kiểm g1.

## ngoai_pham_vi

- Mọi sửa `ops/land_evidence_nguon*.py` (đã xong ở g1; review lượt 7 approve P1=P2=P3=0 tại `98d7d25`).
- `ci.yml`, `NHE`, `MAU_DAY_DU`, `VUNG_*`.

## chua_do_duoc

- Thời gian thêm vào `gate-registry` trên CI: cục bộ bộ test ~45 s (2 worker). Đo thật sau khi đẩy g2.
