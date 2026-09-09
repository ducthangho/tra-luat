---
kieu: dac_ta_packet
packet: WP-CODEX-CREDENTIAL-REFRESH
packet_id: wp-codex-credential-refresh
ban: r1
trang_thai: ready
authority: https://github.com/ducthangho/tra-luat/issues/484
base_sha: c87b0679a837055ee4cc33ac48c9adb8d7ad8784
generation: 1
risk: sensitive
review_class: sensitive
---

# Codex credential theo `CODEX_HOME`

## Objective

Materialize `CODEX_AUTH_JSON` vào `<CODEX_HOME>/auth.json`, fallback
`~/.codex/auth.json`, rồi loại raw snapshot khỏi môi trường child. Giữ các chốt
validate, chống hạ cấp và ghi nguyên tử hiện có.

## Executor và review

- Executor: `openai_codex` / `codex_cli` / `gpt-6-astra` / effort `high`.
- Reviewer: phiên Codex độc lập, read-only, effort `xhigh`.
- Same-provider verdict chỉ là bằng chứng bổ sung; land cần `human_audited`.
- Patch-as-hint chỉ được dùng cho test thuần, không dùng cho launcher/credential runtime.

## Write set

- `.claude/dev/launcher.py`
- `.claude/dev/launcher_test.py`
- `.claude/dev/codex_cred.py`
- `.claude/dev/codex_cred_test.py`
- `.claude/dev/codex_env_policy.py`
- `.claude/hooks/session-start.sh`
- `.claude/hooks/session_start.py`
- `CHANGELOG.md`
- `ops/specs/wp-codex-credential-refresh.md`
- `ops/leases/wp-codex-credential-refresh-exec-g1.yaml`
- `ops/handoff/wp-codex-credential-refresh-exec-g1.md`

## Acceptance

1. `CODEX_HOME` khác rỗng chọn `<CODEX_HOME>/auth.json`; vắng/rỗng chọn `~/.codex/auth.json`.
2. Launcher, hook và `codex_cred.py` dùng cùng quy tắc.
3. Chỉ ghi JSON object có `tokens` object; thư mục `0700`, tệp `0600`, replace nguyên tử.
4. Không hạ cấp snapshot mới hơn trên đĩa; không in raw credential.
5. Launcher materialize trước khi sinh child và bỏ `CODEX_AUTH_JSON` khỏi environment child.
6. Test dương/âm chứng minh custom home, fallback home và child không nhận raw snapshot.

## Bootstrap allowlist

- `npm install -g @openai/codex`
- `python -m pip install -r requirements.txt`
- `python -m pip install PyYAML==6.0.3`
- `apt-get install -y ripgrep`

Không merge, land, deploy hoặc gọi LIVE trong vai Executor.
