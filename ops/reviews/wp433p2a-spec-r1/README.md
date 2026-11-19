# wp433p2a — review đặc tả `GWS-CRED-DICH-NGOAI-KHO-A` r1 (packet P2a của #433)

Đặc tả đóng băng: `ops/specs/GWS-CRED-DICH-NGOAI-KHO-A-r1.md`, sha256
`b0065947f941a122716cff1b15a81ad65fe9b92a15fb9effad1456100c64624d` (= `dac-ta-ban7.md`).

Sáu lượt review độc lập (Codex, read-only), mỗi lượt trên clone master `3b647461db7c8ded1bddd9aafc5c6aa5eead223f`.
Lệnh dùng cho mỗi lượt:

    codex exec --sandbox read-only --skip-git-repo-check -C <clone master 3b64746> "$(cat prompt-luotN.md)" < /dev/null

| lượt | bản được review | dòng cuối verdict |
|---|---|---|
| 1 | `dac-ta-ban1.md` | `KET_LUAN: request_changes` |
| 2 | `dac-ta-ban2.md` | `KET_LUAN: request_changes` |
| 3 | `dac-ta-ban3.md` | `KET_LUAN: request_changes` |
| 4 | `dac-ta-ban5.md` | `KET_LUAN: request_changes` |
| 5 | `dac-ta-ban6.md` | `KET_LUAN: request_changes` |
| 6 | `dac-ta-ban7.md` | `KET_LUAN: approve` |

- `dac-ta-ban0-truoc-tach.md`: bản trước khi chủ kho tách P2a/P2b (19-11).
- `dac-ta-ban4.md`: bản trung gian, chưa đưa review; bản 5 là bản 4 cộng các sửa sau khi chủ kho nâng trần lên 550 dòng.
- Sau lượt 1, phiên điều phối dừng 1/10 và hỏi chủ kho (tách P2a POSIX / P2c Windows-UNC, nâng trần 550), rồi review tiếp.
- `luotN.stdout.txt`: toàn bộ output Codex; `luotN.verdict.txt`: phần verdict trích ra.

Tổng 6/10 lời gọi Codex review đặc tả (ADR-0055), ngoài ngân sách PR.
Chủ kho duyệt băm `b0065947…` ngày 2026-11-19 (ADR-0067, AskUserQuestion phiên điều phối #1206).
Ngoại lệ bundled (E2, Q3): comment chủ kho https://github.com/ducthangho/tra-luat/issues/433#issuecomment-7002145681.

Finding còn mở, không chặn: P3 lượt 6 — `pc_probe_quyen` chưa có đối chứng `winerror` 1/50 (nhánh được phép bỏ qua hardlink).
Giao executor thêm đối chứng ấy nếu nằm trong trần, và ghi kết quả vào thân PR.
