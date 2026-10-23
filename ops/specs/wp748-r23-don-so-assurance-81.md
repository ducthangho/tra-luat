# WP748 r23/g23 — dọn sổ reviewer assurance §8.1 cho hai hồ sơ land có họ model reviewer `khong_do_duoc`

## Thẩm quyền và nguồn gốc

Chủ kho cấp packet ở https://github.com/ducthangho/tra-luat/issues/748#issuecomment-6355107238 (OWNER, 2026-10-23T01:22:44Z).
Executor: Claude Code (`anthropic_claude`, `claude_code`, remote Linux). Reviewer: phiên Codex độc lập chỉ đọc qua
`launcher.py run`, neo đúng head cuối. Review Class `sensitive`. Base `origin/master`
`747f983ccbcaf29a8e5228d09fd05b5a5ab6e479` (tree `e90538be053b07d47987932a7ca899c073fd4598`).

Nguồn lớp lỗi: connector P1 #867 r4355165076 trên hồ sơ r21 (`ops/land/pr862-wp748-r21-land-evidence.yaml`), chủ kho chọn (a):
biên nhận `launcher.py run` không mang model đã phục vụ lượt chạy, nên họ model reviewer ở mức `khong_do_duoc`
(`docs/PROTOCOL_DA_PHIEN.md` §8), và §8.1: "Evidence fallback hoặc không đủ nhận dạng thì chưa nhận assurance". AGENTS.md §4:
assurance không gắn theo tên công cụ.

## Lỗi

- **#845** — `ops/land/pr846-wp845-land-evidence.yaml` trên master khai `landed: true` với reviewer là Codex qua
  `launcher.py run 964888d9`; biên nhận ấy không có trường model ⇒ cùng lớp lỗi.
- **r22 (#869)** — merge `7400df4` (head `b9318cc`), Codex lượt 5 `approve` qua `launcher.py run 76825653`; chưa có hồ sơ land.
  Biên nhận cũng không có trường model.

## Write set hiệu lực

1. `ops/land/pr846-wp845-land-evidence.yaml`
2. `ops/land/pr869-wp748-r22-land-evidence.yaml`
3. `ops/land/pr869-wp748-r22-provenance/`

Quét `ai-dang-giu` 2026-10-23T01:23:43Z trên bản sao bare: `ls-remote` 546 = cục bộ 546 (thiếu 0, thừa 0); cả ba đường dẫn
`NGƯỜI_GIỮ 0`.

## Thay đổi

- `pr846`: điều kiện reviewer assurance §8.1 ghi **CHƯA ĐẠT** kèm lý do `khong_do_duoc`; `landed: true` → `landed: false`; header
  ghi đúng trạng thái và điều kiện mở lại. Không đổi lời khai đo đạc khác; không xoá lịch sử.
- `pr869`: hồ sơ land mới theo khuôn `pr849`/`pr862` — merge, gate, `full_mutant_audit`, lease r22 đã hết hạn, review 5 lượt
  (lượt 5 `approve`, biên nhận `76825653`), `landed: false` vì cùng lý do. Provenance: verdict lượt 5, `run.json`, prompt
  + băm, readback PR/merge, `SHA256SUMS`. Ghi thẳng phần `not_measured` (4 job gộp CI và `dot-bien-gop` không được cấp runner
  lúc merge; Codex connector review lúc merge đang chạy).
- Điều kiện mở lại cho cả hai: launcher đo được model phục vụ (`do_may`), HOẶC chủ kho ghi xác nhận bền `khai_co_audit` trên
  exact SHA (tự khai yếu hơn `do_may` tại chỗ dùng), HOẶC `human_audited`.

## Chấp nhận

- `python3 ops/land_evidence_nguon.py --root .` không vi phạm mới; `kiem-re` DAT; quét bí mật sạch; không CR lẻ.
- CI xanh trên head cuối.
- Codex review qua `launcher.py run` trên head cuối: 0 P0/P1/P2.
- Chủ kho duyệt lần cuối trên SHA cụ thể trước merge.

## Dừng

Dừng và báo khi: người giữ chồng lấn, cần ghi ngoài write set, cổng `land_evidence_nguon` đòi sửa tệp ngoài write set, hoặc
thiếu bằng chứng dương.
