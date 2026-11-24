# LEASE-KIEM-NGHIEM-MOI-DUONG r1 — kiểm lease thêm/sửa ở MỌI PR bằng một workflow riêng (đặc tả đóng băng)

- **Packet:** #1445. Revision 1, generation 1. Role `executor` (Claude), Review Class `sensitive`.
- **Căn cứ:**
  - Issue #1445 đo trên `6774181`: 48/209 lease không qua `lease_publish.kiem` nghiêm. Nguyên nhân: bộ kiểm chỉ chạy ở đường nhanh
    (`ci_duong_nhanh.py kiem-re`, PR chỉ đổi `ops/{land,leases,reviews,specs}/**`) và ở `ops-publish-lease.yml`. Lease đi kèm PR
    đường thường vào master mà không ai kiểm; PR đầu tiên sửa riêng lease ấy mới đỏ (PR #1442).
  - Đo tác động (20/11, 17 PR merge có thêm/sửa lease từ 06/11): 16 đi đường thường. Lease của các phiên khác (wp1166, wp1308,
    wp1389, wp1404) đều qua kiểm nghiêm; chỉ khuôn lease operator của phiên điều phối #1238 từng hỏng.
  - Chủ kho 20/11 chọn làm #1445, rồi chọn *"Tách workflow riêng"*, vì `ci.yml`, `ops/ci_duong_nhanh.py`, `ops/ci_duong_nhanh_test.py`
    đang bị lease `wp1448-r2-g1-claude` (Mission #1172) giữ tới 2026-11-23T08:00Z.

## 1. Hành vi
1. Thêm `ops/kiem_lease_pr.py`. Mã này **chỉ import** từ `ops/ci_duong_nhanh.py`, không sửa tệp ấy:
   - `doc_diff(env)`: tập tệp đổi của PR, cùng định nghĩa với bộ phân loại (hợp `base...head`, merge-tree, diff tới `github.sha`;
     `None` = không đo được);
   - `kiem_lease(doi)`: cùng ngữ nghĩa với `kiem-re`. Lease còn hạn chạy `lease_publish.py check`; lease hết hạn chạy
     `kiem(bo_qua_han=True)`. Bỏ qua tệp đã xoá. Cả `.yaml` lẫn `.yml`.
2. Luật thoát:
   - sự kiện khác `pull_request` ⇒ in lý do, rc 0, **không gọi git**;
   - `doc_diff` = `None` ⇒ in `KHONG DO DUOC`, rc 1 (fail-close);
   - có lỗi lease ⇒ in từng lỗi, rc 1;
   - không lỗi (kể cả 0 lease đổi) ⇒ rc 0.
   Dòng tổng kết luôn có số lease đổi và số lỗi.
3. Thêm workflow `.github/workflows/lease-pr.yml`:
   - `on: pull_request`, `permissions: contents: read`, một job `kiem-lease-pr` trên `ubuntu-latest`;
   - `actions/checkout@v4` với `fetch-depth: 0` (bia mộ cần các ref khác), `setup-python` 3.12, PyYAML 6.0.3 + jsonschema 4.26.0
     như `gate-ops`;
   - chạy selftest `python ops/kiem_lease_pr_test.py` rồi `python ops/kiem_lease_pr.py`, với env `CI_DUONG_NHANH_SU_KIEN` =
     `github.event_name`, `_GOC` = `pull_request.base.sha`, `_DAU` = `pull_request.head.sha`, `_MERGE` = `github.sha`.
4. Đăng ký `ops/kiem_lease_pr_test.py` vào `DA_NOI` của `.claude/dev/ci_dang_ky_test.py`, vì workflow mới gọi trực tiếp tệp ấy.
5. **Không** đổi `ci.yml`, `ci_duong_nhanh.py`, `lease_publish.py`. Đường nhanh giữ nguyên, nên PR chỉ đổi hồ sơ sẽ được kiểm hai lần,
   cùng kết quả.

## 2. Giới hạn đã biết (ghi rõ, không xử lý ở r1)
- Check mới **chưa chặn merge** cho tới khi chủ kho thêm context `kiem-lease-pr` vào ruleset. Việc đó là cấu hình GitHub, ngoài
  quyền của phiên.
- Thẩm quyền: `check` giữ chốt `GITHUB_ACTOR`, nên PR do actor ngoài danh sách cấp lease đẩy, mà có thêm/sửa lease còn hạn, sẽ đỏ.
  Đây là hành vi của đường nhanh hiện nay (docstring `ci_duong_nhanh.py`, Issue #674), nay mở rộng sang đường thường. Đo 20/11:
  40 PR merge gần nhất đều do chủ kho đẩy.
- Không đụng `workflow_dispatch`/`push`: cổng là PR.

## 3. Test
`ops/kiem_lease_pr_test.py`, tự chứa, không Pester. In `CA: n/n dat` và `TONG: DAT`. Ít nhất các ca:
- sự kiện `push` ⇒ rc 0, không lời gọi git;
- PR thiếu hoặc hỏng SHA ⇒ rc 1, `KHONG DO DUOC`;
- PR có lease hỏng thật ⇒ rc 1, lỗi nêu đúng tệp. Fixture: lease đã hết hạn trên cây thật thiếu `reviewed_sha_required`;
- PR có lease tốt thật ⇒ rc 0;
- PR chỉ xoá lease ⇒ rc 0;
- PR không có lease ⇒ rc 0, dòng tổng kết `0 lease`;
- khoá cấu trúc workflow: `on`, `permissions`, `fetch-depth`, đúng hai lệnh `run`, đúng bốn biến env.
- Fixture mất tiền đề (tệp đổi nội dung) ⇒ ca báo `fixture vo hieu`, không xanh giả.
- Đột biến tối thiểu, mỗi cái phải làm ít nhất một ca đỏ: bỏ chốt sự kiện; đổi `None` ⇒ rc 0; nuốt lỗi lease; bỏ `fetch-depth: 0`.

Chạy tại chỗ trước push: `kiem_lease_pr_test.py`, `ci_dang_ky_test.py` (kiểm sổ), `actionlint` trên workflow mới,
`lease_publish_test.py` ca `t24` (cấm dấu bỏ-qua-CI trong workflow).

## 4. Review và CI
- Codex offline qua `launcher.py run`, **tối đa 2 lời gọi**; P0–P2 chặn merge. Thêm connector Codex trên PR.
- CI của PR, gồm workflow mới tự chạy trên chính PR này.
- Đặc tả này không có dòng hiệu lực ADR-0060, nên luật cũ áp: không bắt buộc `full_mutant_audit`. Đột biến tối thiểu ở §3 là phần
  bắt buộc.

## 5. Write set (không glob)
- `ops/kiem_lease_pr.py`
- `ops/kiem_lease_pr_test.py`
- `.github/workflows/lease-pr.yml`
- `.claude/dev/ci_dang_ky_test.py`
- `ops/specs/lease-pr-r1.md`
- `ops/leases/lease-pr-r1-g1-claude.yaml`
- `ops/acceptance/lease-pr/r1/VERDICT.md`
