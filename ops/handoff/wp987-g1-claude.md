# Handoff wp987 g1 — executor `claude` (phiên cloud), 27-10-2026

- Packet #987 r1 · lease `ops/leases/wp987-r1-g1-claude.yaml` @ `2987464` (hạn `2026-10-29T13:15:00Z`) · đặc tả
  `ops/specs/wp987.md` sha256 `9403038447154f1e2e714c40fa8561460a2bac08e8a06708923a5541a5047b15` (băm lại blob nhánh lease: khớp).
- Nhánh code `agent/wp987-g1-claude`, rẽ từ `20a2e2b`, head **`a2e2ebf812f57254affe9344fd02530efa1a0130`**
  (tree `427c0775c0f1b4f5fdadaf10c6e65bc23d4182aa`), đẩy **một lần**. PR draft #991.
- Không merge/land/deploy. Không force-push, không rebase, không xoá ref.
- Master lúc đẩy vẫn là `20a2e2b`; không có gì chạm write set (Q4).

## Diff (2 tệp, +17/−11; trần 2 tệp / 60 dòng)
- **M1** `.claude/skills/cross-review/SKILL.md` mục 4: đọc model/effort/sandbox từ `run.json`. Kèm một lệnh Python in 9 trường.
  Chỉ `*_trang_thai = DO_DUOC` là đo được. Header `stderr.log` là lời khai phụ; vắng header ≠ chưa đo.
  Câu `r368` giữ nguyên văn.
  Câu cũ *"Header này không phải thống kê model thực thi … như `modelUsage`"* được thay bằng câu tương đương cho `model_phuc_vu`.
- **M2** `.agents/skills/cross-review/SKILL.md`: `$Run = Get-Content -Raw -LiteralPath $RunJson | ConvertFrom-Json`, rồi đọc
  `$Run.model_phuc_vu` / `effort_phuc_vu` / `sandbox_quan_sat` và các `*_trang_thai`/`*_ly_do`.

## Tiêu chí — đo trên `a2e2ebf` (clone thường, không nông, `core.abbrev 7`)
- **N1** `python .claude/dev/packet_loop.py doctrine-scan --root .` ⇒ rc 0, `sạch — đã quét 10 tệp, 0 chỗ chép doctrine`.
  `git diff --check` rc 0.
- **N2** `rg -n -F '"<tên>"' .claude/dev/launcher.py`, dòng ghi đầu tiên của từng tên:
  `model_phuc_vu` 1831 · `model_phuc_vu_trang_thai` 1832 · `model_phuc_vu_ly_do` 1834 · `effort_phuc_vu` 1838 ·
  `effort_phuc_vu_trang_thai` 1839 · `effort_phuc_vu_ly_do` 1841 · `sandbox_quan_sat` 2150 · `sandbox_trang_thai` 2151 ·
  `sandbox_ly_do` 2153.
  Tên khác có nhắc, đếm bằng `rg -c -F`: `KHONG_THAY_LENH` 1 · `_BoLocStderr` 2 · `_LayMauSandbox` 2 · `RUST_LOG` 4.
- **N3** `rg -n 'stderr.log' .claude/skills/cross-review/SKILL.md .agents/skills/cross-review/SKILL.md`:
  - `.claude:139`: tiêu đề mục 4 — nói rõ KHÔNG đọc từ `stderr.log`.
  - `.claude:151`: quan sát codex-cli 0.164 không in header (wp923 g2: 39 byte); là bằng chứng, không phải nguồn đo.
  - `.claude:179`: `tail -50 <run>/stderr.log` ở mục *container chết giữa lượt*, dùng để chẩn đoán reconnect, không đo model.
  - `.agents` không còn chuỗi `stderr.log`; dòng 69 nhắc `$StderrLog` chỉ để nói header là lời khai phụ.
- **N4** `python scripts/tl.py --selftest` ⇒ `== tl selftest 1731/1731 ==`, transport 12/12, rc 0. Chạy tại chỗ trên tree `427c077`;
  commit `0876d56` → `a2e2ebf` là amend không đổi tree. CI: đọc check run trên PR #991, cập nhật ở báo cáo #987.

## Cross-review Codex — 2/10 lời gọi (spec Q1, ADR-0055)
- Gọi qua `.claude/dev/launcher.py run`:
  `codex exec --json -m gpt-6.1-sol -c model_reasoning_effort=xhigh --sandbox workspace-write`.
- Sandbox: clone thường detached tại head + `SPEC.md` + `diff.patch`.
- Dòng khai ADR-0055 đo lại trên clone KHÔNG nông, trước mọi lời gọi:
  - `cat-file -e d2e3052:docs/adr/0055-tran-loi-goi-codex-len-muoi.md` rc 0;
  - trên `d2e3052^1` rc 128;
  - `d2e3052` có trong first-parent của `origin/master`.
- Model/effort/sandbox dưới đây đọc từ `run.json`, đúng như M1 hướng dẫn.

| lượt | run_id | prompt sha256 | thời lượng | model_phuc_vu | effort | sandbox | verdict |
|---|---|---|---|---|---|---|---|
| 1 | `da438d8f0baa413586eff0a65f9e6fa2` | `fae71431…` | 841,6 s | `gpt-6.1-sol` DO_DUOC | `[xhigh]` DO_DUOC | DO_DUOC | `blocked` |
| 2 | `0e1042359a214887bcdedd2cce365dbb` | `68ce98eb…` | 324,2 s | `gpt-6.1-sol` DO_DUOC | `[xhigh]` DO_DUOC | DO_DUOC | **`approve`** |

- `stderr.log` của cả hai lượt: 39 byte, không có header model. Đây đúng ca M1 xử lý.
- **Lượt 1** `blocked`: không có P0/P1/P2, chặn duy nhất ở HƯỚNG 8 vì sandbox không có `pwsh` và không tải được.
  - Vì sao gọi lượt 2: còn phần chặn, và cần xác minh phần ấy.
  - Phiên chính cài PowerShell 7.4.6 (bản phát hành chính thức) vào `/opt/pwsh`. Driver của reviewer cho `POWERSHELL_PARITY 3/3`.
- **Lượt 2** `approve`:
  - PowerShell thật đạt 3/3 trên fixture.
  - Dòng gán nguyên văn của adapter chạy trên `run.json` THẬT của lượt 1, khớp Python 9/9 trường.
  - Không có finding mới.
- Hiện vật nằm ở `ops/reviews/wp987-g1-claude-review-{1,2}-codex/` (`PROMPT.md`, `VERDICT.md`, `run.json`):
  - `VERDICT.md` lượt 1: sha256 `6136b7e7de0e4390…`;
  - `VERDICT.md` lượt 2: sha256 `e9e7006e8b040451…`.
  - Thư mục `review-evidence/` mà verdict trỏ tới KHÔNG được commit: script đo và log nằm ở scratch của phiên, link trong verdict là
    link chết. Muốn đo lại thì chạy lại theo lệnh ghi trong verdict.

## Lỗi khác lộ ra — ghi lại, KHÔNG vá (Q5)
- **`model_phuc_vu` không phải danh sách tên model.** Đó là danh sách bản ghi `{response_id, model, su_kien}`, khử trùng theo
  `response_id`+`model`.
  - M1 viết "danh sách model theo từng khung response"; reviewer xếp là KHÔNG PHẢI LỖI (HƯỚNG 9).
  - Người đọc `.agents` (`$Run.model_phuc_vu`) sẽ nhận một mảng object. Lượt sau có thể nói rõ hơn nếu cần.
- **Selftest trong sandbox reviewer** lần đầu ra 1727/1731: bốn ca `r218/r226/r264/r268` đỏ vì thiếu `core.abbrev` và vì fixture
  git gọi dịch vụ ký commit localhost (bị chặn).
  - Đặt lại môi trường thì 1731/1731. Đây là lỗi nơi chạy, không phải lỗi mã; nợ của packet khác.
- **Sandbox Codex không ra được mạng để tải PowerShell** (curl rc 7 qua proxy cục bộ). Packet nào cần reviewer chạy `pwsh` thì phiên
  điều phối phải cài trước.
