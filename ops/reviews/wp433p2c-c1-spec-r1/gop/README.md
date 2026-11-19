# wp433p2c — soạn và review đặc tả GWS-CRED-DICH-NGOAI-KHO-C r1 (P2c của #433)

Bản hiện hành: ../GWS-CRED-DICH-NGOAI-KHO-C-r1.md (= dac-ta-ban4.md, CHƯA review).
Review Codex chỉ đọc trên worktree master 11bd0336 (đã xoá), lệnh:
  codex exec --sandbox read-only --skip-git-repo-check -C <clone> "$(cat prompt-luotN.md)" < /dev/null

| lượt | bản | sha256 | kết luận |
|---|---|---|---|
| 1 | dac-ta-ban1.md | 96893bdf… | request_changes (4 P1, 5 P2, 1 P3) |
| 2 | dac-ta-ban2.md | 20e58ab1… | request_changes (3 P1, 5 P2, 1 P3) |
| 3 | dac-ta-ban3.md | 744b8f5e… | request_changes (2 P1, 4 P2, 1 P3) |
| — | dac-ta-ban4.md | b477d23e… | chưa review; R3-1 chờ chủ kho (§9 Q2) |

3/10 lời gọi Codex (ADR-0055). luotN.stdout.txt = toàn bộ output; luotN.verdict.txt = phần finding.
nguyen-mau/: nguyên mẫu bộ phân loại M1/M2 và bộ chạy đột biến (r4: 28/28 trên 3.11/3.12/3.13).
