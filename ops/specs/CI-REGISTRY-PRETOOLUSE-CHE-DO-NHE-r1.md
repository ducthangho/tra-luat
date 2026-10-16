---
kieu: dac_ta_packet
packet: CI-REGISTRY-PRETOOLUSE-CHE-DO-NHE
packet_id: CI-REGISTRY-PRETOOLUSE-CHE-DO-NHE
ban: r1
trang_thai: dong_bang_khi_dang_bam
nguon_cap_viec: >-
  Chỉ thị chủ kho trong phiên Claude Code 26-09-2026 (phiên executor #643), sau số đo A7 của #643:
  "Làm chế độ nhẹ cho pretooluse_guard_test, tạo issue cấp lease".
ghi_chu_hinh_dang: Chưa cổng nào đọc tệp này. Nó là DỮ LIỆU cho lease và cho reviewer.
---

# `CI-REGISTRY-PRETOOLUSE-CHE-DO-NHE` — chế độ nhẹ cho `pretooluse_guard_test` (bản **r1**)

- `packet_id`: **`CI-REGISTRY-PRETOOLUSE-CHE-DO-NHE`** · `revision`: 1 · `generation`: 1 (dự kiến)
- `review_class`: **`sensitive`** — sửa bộ test của hook bảo vệ (`pretooluse_guard`) và chính sách chọn test của CI.
- `risk`: `sensitive` · `environment`: `cloud` · `depends_on`: `[]` (kế thừa cơ chế của #643, đã land ở `6d9581c`)
- executor: `anthropic_claude` · `claude_code` · `claude-opus-5-5`
- assurance: Codex CLI tại chỗ + Codex connector (`advisory_review`); **`human_audited`** là cổng land.
- base: `origin/master` **`2ab6f13d06dc4815c19dba72b38d89f9531f84ff`** (đo 2026-09-26T13:29:35Z)

## 1. Phép đo nền

- Run `36238709647` (master `2ab6f13`, lượt đầu chạy chế độ nhẹ của #643): `gate-registry` **13m08s**, trong đó
  `.claude/hooks/pretooluse_guard_test.py` **756,50 s** (≈ 96 % bước test), `subagent_ghi_detect_test` 286,72 s.
- Tại chỗ (container, head `2ab6f13`): bộ có **39** ca nền và **34** đột biến. Chỉ chạy ca nền (nhánh
  `nen_bo_qua_dot_bien`) mất **10,2 giây** ⇒ vòng đột biến chiếm ≈ 98 % thời lượng.
- Bộ đã có sẵn nhánh "bỏ vòng đột biến, ca nền chạy đủ" cho Windows (`chay()`, `dat_windows`, `dong_windows`),
  với chốt `so_dot_bien > 0` (bài học #319).

## 2. Lệch protocol có duyệt

Mở rộng lệch của #643 (`docs/PROTOCOL_DA_PHIEN.md:839-840`, selector không qua shadow) sang **một bộ thứ hai**.
Căn cứ: chỉ thị chủ kho ở đầu tệp. Phạm vi y hệt #643: chỉ **vòng đột biến** của bộ này bị bỏ khi diff không
chạm vùng; 39 ca nền và mọi bộ khác vẫn chạy mọi lượt; các fallback fail-closed của `ke_hoach` (#643) giữ nguyên.

## 3. Ngoài phạm vi

| thứ | lý do |
|---|---|
| `subagent_ghi_detect_test` (≈ 287 s) | packet sau nếu cần |
| sửa `pretooluse_guard.py` (hook) | không đụng hành vi hook |
| sửa `ci.yml` | không cần; env con do `ci_dang_ky_test.py` đặt |
| Windows | Windows vốn đã bỏ vòng đột biến bộ này; hành vi Windows không đổi |

## 4. Write set — 2 đường

| # | đường dẫn | vì sao |
|---|---|---|
| W1 | `.claude/hooks/pretooluse_guard_test.py` | cờ môi trường chế độ nhẹ + dòng bằng chứng riêng + ca tự kiểm |
| W2 | `.claude/dev/ci_dang_ky_test.py` | thêm bộ vào `NHE`/`MAU_DAY_DU`; mẫu bằng chứng chế độ nhẹ; miễn trừ Windows; phản chứng |

Ngưỡng ADR-0044: ≤ 3 tệp, ≤ 300 dòng thêm.

## 5. Mục tiêu

| # | mục tiêu | đường |
|---|---|---|
| M1 | cờ `PRETOOLUSE_GUARD_KHONG_DOT_BIEN=1` ⇒ chạy đủ 39 ca nền, **bỏ** vòng đột biến, in dòng riêng `TONG: CA a/b dat · DOT BIEN n muc CHE DO NHE — do khi diff cham vung` (KHÔNG mang chữ `bi giet`), `DAT` chỉ khi đủ ca nền và `n > 0`. Nhánh Windows đứng TRƯỚC và không đổi | W1 |
| M2 | `ci_dang_ky_test.py`: bộ vào `NHE` (cờ trên) và `MAU_DAY_DU` (chế độ đủ đòi dòng `DOT BIEN x/x bi giet`, x>0); chế độ nhẹ chỉ nhận **mẫu nhẹ riêng** của bộ; Windows miễn đòi `MAU_DAY_DU` cho bộ có trong `MOI_WINDOWS` (Windows vốn không chạy đột biến bộ này) | W2 |
| M3 | vùng của bộ theo luật #643: `{bộ, .claude/hooks/pretooluse_guard.py}` ∪ vùng chung | W2 (không đổi mã `ke_hoach`) |

## 6. Nghiệm thu

| # | tiêu chí | phép đo làm ĐỎ |
|---|---|---|
| A1 | W1 tự kiểm: cờ bật ⇒ không chạy đột biến, dòng nhẹ đúng dạng, `DAT` khi ca nền đủ; `n = 0` ⇒ `DO`; dòng nhẹ không chứa `bi giet` | ca thuần mới trong W1 + đột biến |
| A2 | W2: chế độ nhẹ + dòng nhẹ ⇒ ĐẠT; chế độ nhẹ + dòng Linux đủ ⇒ ĐẠT; chế độ đủ + chỉ dòng nhẹ ⇒ ĐỎ; Windows + chế độ đủ + dòng Windows ⇒ ĐẠT | ca `p-*` qua CHÍNH `chay_moi` |
| A3 | `ke_hoach`: diff chạm `pretooluse_guard.py` hoặc bộ ⇒ đủ; diff `docs/` ⇒ nhẹ | ca `p-*` |
| A4 | CI của PR (chạm `ci_dang_ky_test.py` ⇒ đủ) xanh; sau land, lượt master không chạm vùng in `nhe` cho cả hai bộ | A4 sau land là quan sát, không phải cổng land |

## 7. Ngân sách CI

`0 / 1 / 2` lượt `pull_request` (mỗi lượt = một workflow run; chạy lại job trong cùng run không tính thêm).

## 8. Điều kiện dừng

S1 chạm đường ngoài W1/W2 · S2 CI đỏ vì packet · S4 push chỉ sau review tại chỗ sạch · S5 > 300 dòng ·
S6 hết hạn lease ⇒ handoff §7.
