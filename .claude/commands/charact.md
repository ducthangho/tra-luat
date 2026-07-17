---
description: Capture characterization 1..n lệnh tl (offline fake-home, --json --deterministic, scrub _scrub_volatile) vào scripts/.tl_state/charact/ — §6.1 kế hoạch guard-va-boc-tl-core
argument-hint: <cli-name…> | --clusters [--stability 2]
---

Capture CHARACTERIZATION theo §6.1 (TRƯỚC khi động code — baseline so-khớp-byte cho MOVE Đợt A/B):

```bash
cd /c/qh/tra-luat && /c/Python313/python .claude/dev/charact_capture.py $ARGUMENTS
```

- Không tham số / `--clusters` = TOÀN BỘ cmd của 2 cụm `ingest_ops` + `nlm_ops` (map qua parser thật).
- `--stability 2` = chạy 2 lượt và so byte (R7 — baseline chỉ tin được khi ×2 byte-hệt).
- Harness tự dựng FAKE-HOME TRỐNG tại `scripts/.tl_state/charact_home` (HOME/USERPROFILE giả, config giả
  webappUrl RỖNG → offline thuần, thông điệp lỗi nội bộ tất định; journal/cache rơi vào fake-home).
- Out: `scripts/.tl_state/charact/<cli-name>.json` (schema charact.v1; JSON stdout scrub bằng chính
  `tl._scrub_volatile`, path thay `<REPO>`/`<FAKEHOME>`).
- CẤM tuyệt đối trong charact: `--apply`, `--confirm` (harness assert cứng).

So-khớp SAU move: chạy lại đúng lệnh trên rồi `git diff --no-index` (hoặc so bytes) giữa 2 bộ
`.tl_state/charact/` — lệch = BUG của move (DỪNG, theo R6/§6.5). Kết quả dài → giao `tl-auditor` đọc.
