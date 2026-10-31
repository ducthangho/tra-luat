# Biên nhận cross-review — packet `WINDOWS-LOCAL-MAY-CHU-KHO` r3 g1 (mission `gh-1035`)

- Nhánh code: `agent/windows-local-may-chu-kho-r3-claude`, base `adb3d2e977daf9b5623bfc9c7b71b361ecbcf4fc`.
- Đặc tả: sha256 `f1a666a32161f0607ac27bc8c3be6963bb6367e64f02825635a75cc8185fa973`.
- Reviewer: `openai_codex` qua `.claude/dev/launcher.py run`, mỗi lượt một phiên mới, sandbox mới, clone đầy đủ từ
  GitHub (không shallow) checkout đúng head, `codex exec -c model_reasoning_effort=xhigh --sandbox workspace-write`.
  Prompt không trỏ tới verdict cũ. Model/effort/sandbox đọc từ `run/run.json` của từng lượt.
- Snapshot §8.2 của `cay-kho/` chụp TRƯỚC và SAU mỗi lượt, ngoài sandbox, bằng `snapshot.py`
  (HEAD, tree, `git diff --binary`, `git diff --cached --binary`, untracked, ignored, sha256 từng tệp).
  Tệp snapshot không chép vào kho; mỗi lượt có `snapshot-khong-chep.txt` ghi các trường và sha256 của hai tệp.
- Trần 10 lời gọi Codex (ADR-0055); đã dùng 6 (`dem-loi-goi-codex.txt`).

| lượt | run_id | head | verdict | P0/P1/P2/P3 | snapshot trước = sau |
|---|---|---|---|---|---|
| 1 | 4e172cc150d345bcb54413854a6f7410 | 144c96a | changes_requested | 0/2/0/0 | có |
| 2 | b8b6535ff8844a3c83977af31404f6bc | b4ccc45 | changes_requested | 0/0/1/0 | có |
| 3 | 56ff8cd6e41d4a8da95814236621454a | 1479568 | changes_requested | 0/1/0/0 | có |
| 4 | 3991830bb42944d19c51e5cf163e6eb3 | ea9c0dc | changes_requested | 0/0/1/0 | có |
| 5 | 1258493544ce4c4fadbc391b3d3373ac | 27b6eff | changes_requested | 0/0/0/1 | có |
| 6 | 5df131b5072c4c44b9db7181b0e17a6a | c13505a2c36a70c47f5c740146fd5ad6794a9882 | **approved** | 0/0/0/0 | có |

`chung-cu-d10.txt`: bản chép nguyên văn output đọc chỉ-đọc từ ASUS-LAPTOP qua Desktop Commander ngày 31-10-2026
(nguồn của ca D10 trong ADR-0059). Lượt 4 nhận bản đầu của tệp này; lượt 5–6 nhận bản bổ sung nguồn `selftest.ps1`.
Bản mỗi lượt đã nhận nằm trong thư mục lượt đó.
