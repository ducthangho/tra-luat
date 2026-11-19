Bạn là reviewer ĐỘC LẬP (họ OpenAI), chỉ đọc, LƯỢT 3. Worktree kho tra-luat ở commit 3b647461db7c8ded1bddd9aafc5c6aa5eead223f. Đối tượng: đặc tả `ops/specs/LAUNCHER-BAM-LOG-NEN-WINDOWS-r1.md` (bản 3, chưa commit). Bản lượt trước: `ops/specs/BAN2-truoc-luot3.md`. Verdict lượt 2 của bạn (5 P2, 2 P3) được tóm tắt ở mục "Lượt 2" của §11.

Việc:
1. `diff -u ops/specs/BAN2-truoc-luot3.md ops/specs/LAUNCHER-BAM-LOG-NEN-WINDOWS-r1.md`; kiểm TỪNG finding lượt 2 đã thực sự đóng, bằng đo trên mã khi cần (dòng `HONG <ca>:` mà `--lap-ca` in; cách runner tách bảng harness và cộng `DOT_BIEN_HOOK`; thân `_r387_*`, `_r1252_run`, ca (a′)). Ghi rõ finding nào CÒN MỞ.
2. Tìm lỗi MỚI do bản 3 đưa vào: (t3b)/(t3c)/(t4a–d)/(t5)/(t6), H1–H7 (mỗi mục có giết đúng nhãn đã khai không, có chết ở chốt khác/tín dụng giả không, mẫu có khớp đúng một chỗ được không), (t5) vá `_r1252_run` toàn cục + `m._job_windows`/`m._pid_trong_job` trước `_r387_chay` có khả thi và khôi phục sạch không, bộ bọc `_job_windows` cài trên mọi nền có làm ca POSIX/`t*` khác đổi hành vi không, kiểm 22/0/9.
3. L1–L7 (`.claude/skills/soan-spec/SKILL.md`) cho phần đã đổi.

Chỉ nêu finding có bằng chứng. Không sửa tệp nào. Mỗi finding: mức, vị trí, bằng chứng, cách sửa. Kết thúc bằng đúng một dòng cuối: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`.
