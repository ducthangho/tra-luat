# Handoff wp835 g4 — ADR-0056 ngưỡng thu hồi lease 6 giờ (executor `wp835-r4-g4-claude`)

Packet #835 · revision 4 · generation 4 · `review_class: sensitive` · executor `claude`
(`session_016aK6Uy4CzUZFKnDmoHRQps`, cùng phiên với g3) · reviewer `codex`. Phiên giao việc: `session_01FLVLxi5gKZgtVvbuTCEqEn`.
Lease `ops/leases/wp835-r4-g4-claude.yaml` @ `e2ff789` (thay `wp835-r3-g3-claude` bằng bia mộ hai chiều, `d3c6a5e`).
Đặc tả r4 `ops/specs/wp835-lease-6h-governance-r4.md` sha256 `72bd6361…4e05e` (đo lại, khớp), DELTA trên r3
`71403df8…6ddc` và r2 `da98e225…7833`. Handoff g3: `ops/handoff/wp835-g3-claude.md` trên `ops/wp835-r3-g3-lease@79fd653`.

Nhánh `agent/wp835-g4-claude`, base `d2e3052`, head **`87fd7611001ebffd20a87c934fcf578644984b4b`**, đẩy MỘT lần sau
khi Codex approve. **PR #931 (DRAFT).** KHÔNG merge/land/deploy — việc của chủ kho.

## Đã làm
| tệp | việc |
|---|---|
| `docs/PROTOCOL_DA_PHIEN.md` | Port bản vá r2 (`062292b..a62ba1f`): ba hunk §3.6/§4 + mẫu lease áp sạch sau khi đổi `ADR-0055`→`ADR-0056`. §20: dòng `ADR-0017` trỏ `ADR-0056`; dòng `ADR-0056` thêm tay NGAY SAU dòng `ADR-0055` của #919. Dòng `ADR-0052`/`ADR-0055` nguyên byte. |
| `docs/adr/0056-lease-no-progress-six-hours.md` | Mới: ADR r2 đổi số + provenance r3 (dòng Trạng thái, "đo lại 25-10-2026 tại base `d2e3052`") + câu write set theo r4 E1 (commit `87fd761`, đáp WP835-R3-01). Ngày Accepted `2026-10-19`. Giữ `CHƯA KÍCH HOẠT VẬN HÀNH`. |
| `scripts/tl_selftest.py`, `RELEASE_MANIFEST.json` | Nguyên byte so base (r4 E1), đã kiểm `git diff --quiet d2e3052 HEAD -- …`. |

Diff: 2 tệp, +62 −3 (≤ 2 tệp, ≤ 150 dòng thêm). Commit: `3785f95` (port, r3/g3) → `87fd761` (câu write set, r4).
`.github/coordination/change-impact.v1.json` vắng ở base. `origin/master` lúc đẩy: chỉ thêm `ops/land/**` so base, không chạm write set (Q4).

## N1–N7 trên `87fd761`
- **N1 ĐẠT**: §4 360 phút chỉ cho lease MỚI sau kích hoạt; `lease_until` tuyệt đối, generation/fencing, bia mộ hai
  chiều, exact head nêu "KHÔNG đổi"; đoạn `review_sla` chỉ đổi cụm "thu-hồi-30-phút" → "thu-hồi-6-giờ (360 phút, …)";
  heartbeat 15 phút sau `changes_requested` giữ nguyên. Codex (cả hai lượt) so lại sau chuẩn hoá: bằng nhau.
- **N2 ĐẠT**: `adr-song` rc 0 — 55 ADR, 55 dòng §20, khớp 1–1.
- **N3 ĐẠT**: `doctrine-scan` rc 0 (10 tệp, 0 chỗ chép); `git diff --check d2e3052 HEAD` rc 0.
- **N4 ĐẠT** (tại chỗ): `python scripts/tl.py --selftest` ⇒ `== tl selftest 1731/1731 ==` rc 0, `[OK] r291_docs_ngoai_goi`,
  cây sạch tại `87fd761`. Bằng chứng phụ từ g3 (head `3785f95`): thêm một `docs/*.md` ⇒ 1731/1731; đổi ratchet gói
  192→193 ⇒ 1730/1731, r291 FAIL. Trong sandbox Codex selftest ra `1729/1731` ở CẢ base lẫn head (`r226_*`, `r268_*`:
  `git commit` của fixture rc 128 vì công cụ ký commit gọi MCP localhost bị chặn) — tạo tác môi trường reviewer, delta 0.
- **N5 ĐẠT**: `release-verify --strict --json` `ok=true`, 192 == 192, manifest không sửa; `doc-claims-check --strict`
  rc 2 ở cả base và head với đúng MỘT cờ chung `docs/AUDIT_LAUNCHER_VONG_3.md:462 f08e45b SHA_NOT_A_COMMIT` (clone nông) ⇒ delta 0.
- **N6**: chờ `ci.yml` lượt PR #931 trên head — đọc bằng check run, cập nhật ở comment #835.
- **N7 ĐẠT**: ADR và dòng §20 giữ `CHƯA KÍCH HOẠT VẬN HÀNH`.

## Review (ngân sách Codex 2/2 đã dùng hết, không reset theo generation)
- Lượt 1/2 (g3) @ `3785f95`: `changes_requested`, một P2 WP835-R3-01 → chủ kho duyệt r4.
  Hồ sơ `ops/reviews/wp835-r3-g3-claude-review-1-codex-*` trên `ops/wp835-r3-g3-lease`.
- Lượt 2/2 (g4) @ `87fd761`: **`approve`**, WP835-R3-01 "ĐÃ VÁ THẬT — đóng", không P0/P1/P2/P3 mới.
  `launcher.py run` `6c5f75a9`, `codex-cli 0.164.0`, `model_reasoning_effort=xhigh`, `model_phuc_vu` đo được `gpt-6.1-sol`,
  932,1 s, rc 0. Hồ sơ `ops/reviews/wp835-r4-g4-claude-review-2-codex-{prompt.md,run.json,verdict.md}` trên nhánh này.
  Reviewer tự ghi: approve là kết luận nội dung; N4 trong sandbox của nó vẫn failed (tạo tác trên), N6 chưa chạy.

## Lỗi khác lộ ra (không vá — Q5)
- Sandbox Codex `workspace-write`: ký commit qua MCP localhost làm fixture git của `r226_*`/`r268_*` rc 128 ⇒ reviewer
  không tái lập được N/N. Nợ môi trường review.
- `doc-claims-check --strict` đỏ sẵn trên clone nông (`f08e45b`).
- Sự cố điều phối nhỏ: executor đã soạn một bản spec r4 cục bộ cùng đường dẫn trước khi thấy lease g4; bản ấy KHÔNG
  được đẩy (push bị từ chối non-fast-forward vì bia mộ g3 đã lên trước), bản có thẩm quyền là `72bd6361…`.
- `/tmp/.git` rỗng: kiểm sau cả hai lượt Codex — KHÔNG có.
