# wp1342 — review đặc tả `WP1174-WINDOWS-BACKEND` r5 (bậc r1d-a1-ii)

Đặc tả đóng băng: `ops/specs/WP1174-WINDOWS-BACKEND-r5.md`, sha256
`0550af2102ab4616f2639572195bb28bcb01346d35d5be70af62284df53e0791` (= `dac-ta-ban6.md`), base `4eda94e9effc6cfe7fcc0b3e3fb4151ad437ecbd`.

Sáu lượt review độc lập (Codex, read-only) trên clone master, lệnh mỗi lượt:

    codex exec --sandbox read-only --skip-git-repo-check -C <clone master> "$(cat prompt-luotN.md)" < /dev/null

| lượt | bản | kết luận |
|---|---|---|
| 1 | `dac-ta-ban1.md` | `request_changes` |
| 2 | `dac-ta-ban2.md` | `request_changes` |
| 3 | `dac-ta-ban3.md` | phiên dừng giữa chừng, không in verdict (vẫn tính một lời gọi); quan sát cuối đã sửa ở bản 4 |
| 4 | `dac-ta-ban4.md` | `request_changes` |
| 5 | `dac-ta-ban5.md` | `request_changes` |
| 6 | `dac-ta-ban6.md` | `approve` (dòng `KET_LUAN: approve` trong `luot6.verdict.txt`) |

6/10 lời gọi Codex (ADR-0055), ngoài ngân sách PR. Chủ kho duyệt băm `0550af21…` và phạm vi "chỉ tệp test,
không thêm kiểm runtime vào `_1174_win_spawn_job`" ngày 2026-11-19 (ADR-0067, AskUserQuestion phiên điều phối #1206).
