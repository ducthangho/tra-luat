# wp433p2b — review đặc tả `GWS-CRED-DICH-NGOAI-KHO-B` r1 (P2b của #433)

Bản cuối: `../GWS-CRED-DICH-NGOAI-KHO-B-r1.md` = `dac-ta-ban3.md`, sha256 `cd0b51a3d458de79c577f1573899fe0518aa2871dfc217fa143b822da1bac267`.
Ba lượt Codex read-only trên clone master `11bd0336d00b4a9544e70dcbbe049d372053a3ec`:
`codex exec --sandbox read-only --skip-git-repo-check -C <clone> "$(cat prompt-luotN.md)" < /dev/null`

| lượt | bản | kết luận |
|---|---|---|
| 1 | dac-ta-ban1.md (`cd88fbe9…`) | request_changes (4 P2, 3 P3) |
| 2 | dac-ta-ban2.md (`c63c1166…`) | request_changes (2 P2) |
| 3 | dac-ta-ban3.md (`cd0b51a3…`) | approve (1 P3 mở) |

3/10 lời gọi Codex review đặc tả (ADR-0055). Script đo + output ở `do/` (prototype dựng NGOÀI kho, không commit).
P3 còn mở (lượt 3): N1b — nhãn `tien_de` của `W6.web_utf8` phải được chấm TRƯỚC khi giả lập/gọi `cmd_bootstrap`
(không thì locale ASCII thật cho `ngoai_le_la` thay vì `tien_de`). Giao executor làm đúng thứ tự ấy; không đổi hành vi được đo.
