# Nghiệm thu packet #1514 LLM-RANH-GIOI-KHOAN (PR #1517) — DỪNG, chưa merge

- Đặc tả hiện hành: `ops/specs/llm-ranh-gioi-khoan-r9.md` · lease `ops/leases/llm-ranh-gioi-khoan-r9-g1-claude.yaml`.
- Head mã cuối đã review: `fcb12b3873c3bec2c339029136243ed2c804ce05` (r9). Baseline `64b7f2c14776d5d0e1d34a6be4725490956f5bec`.
- Trạng thái: **KHÔNG đủ điều kiện merge** theo ADR-0060 M1 (0 P0/P1/P2 mở): còn **1 P2 mở (K1)**. Chủ kho chọn 25-11-2026
  *"Stop; leave the PR draft, file a debt issue"*. PR giữ draft, không merge.

## §6.1–6.2 Gate cục bộ trên `fcb12b3`
| Lệnh | Kết quả |
| --- | --- |
| `python scripts/tl_core/llm_route_test.py` | 56/56 ca, 102/102 đột biến bị giết |
| `python scripts/tl.py --selftest` | 1789/1789 |
| `release-verify RELEASE_MANIFEST.json --strict` | ok, 187/187 |
| `workflow-audit --strict` · `golden-test` · `determinism-audit --strict` · `doc-claims-check --strict` | rc 0 cả bốn |
| `ruff --select F scripts/tl.py` | 12 F821 = nền master (delta 0) |

## §6.3 Đo Windows bản địa (§3)
- Run `45553156011` (`workflow_dispatch`, `runner_set=windows-only`) trên `9541e02` (r4):
  - `gate (windows-latest)`: **ĐẠT**, `tl selftest 1789/1789`, gồm `r380_llm_khai_niem_bien_dau_vao [OK]` (lỗi run `45542712141` đã vá ở r4).
  - `gate-registry (windows-latest)`: dòng `CI_DANG_KY scripts/tl_core/llm_route_test.py: ĐẠT rc=0` (06:07:24Z); job sau đó bị huỷ
    (`cancelled`) ở bước khác — dòng của `llm_route_test` đã ghi trước lúc huỷ.
  - `gate-packet-loop*(windows)` đỏ ở `wp1174_admission_*` (`.claude/dev/packet_loop.py`, không thuộc diff) — comment PR #1517.
- r5–r9 CHƯA đo lại trên Windows (`not_measured`); diff r5–r9 chỉ đổi regex/nhánh thuần Python trong `llm_route.py` và test.

## §6.4 Cross-review Codex (trần nâng 5 → 10, 10/10 lời gọi đã dùng)
| Lượt | SHA | Kết luận | Finding mở |
| --- | --- | --- | --- |
| 1 | `89c60dc` | chặn preflight | B1 |
| 2 | `53c49ab` | REQUEST_CHANGES | A1–A4 |
| 3 | `64153db` | REQUEST_CHANGES | C1, C2 |
| 4 | `e9fc10c` | REQUEST_CHANGES | D1 (P1), D2, D3 |
| 5 | `9541e02` | APPROVE | E1, E2 (P2) |
| 6 | `aed16f3` | APPROVE | F1, F2 (P2) |
| 7 | `0ec7ca0` | APPROVE | G1 (P2) |
| 8 | `4d357d1` | APPROVE | H1 (P2) |
| 9 | `5aa5b34` | APPROVE | J1 (P2) |
| 10 | `fcb12b3` | APPROVE | **K1 (P2) — mở** |

Hồ sơ từng lượt: `ops/acceptance/llm-ranh-gioi-khoan/r1/review-N-codex/`.

## Kết luận về lớp `ranh-gioi-khoan`
Mười lượt liên tiếp tìm ra một biểu hiện mới của CÙNG một lớp: trên văn bản thô, khoản có điểm và lời dẫn nhóm có cùng hình dạng.
r6–r9 đóng được bằng cấu trúc phần câu dẫn (danh sách cho phép), đánh số nội dòng (tập bao) và toàn bộ nguồn mất số (không cho dòng
điểm). K1 nằm ở nguồn CÓ số (nhánh điểm và tiếp dòng "là" — có nguyên trên master `64b7f2c`, `llm_route.py:522`, `:526`); đóng
nó trên văn bản thô đòi chặn mọi khoản có điểm, tức bỏ chức năng phổ biến. Nợ chuyển sang Issue #1525 (nguồn có cấu trúc).
