Bạn là reviewer ĐỘC LẬP (họ OpenAI), lượt 7, cho đặc tả `ops/specs/LEASE-TRUONG-KHAI-NGHIA-r1.md` (Issue #646). CHỈ ĐỌC; không ghi tệp trong thư mục làm việc; không gọi mạng. Chạy thử trong RAM hoặc bản sao/rig git dưới /tmp.

Worktree master 641108c. `ops/specs/LEASE-TRUONG-KHAI-NGHIA-r1-ban6.md` là bản bạn review lượt 6 (request_changes: P2 N1+N5 bỏ lọt đổi mode Git; P3 §6 đếm lượt cũ; P3 §8 ghi 13 dòng). Bản hiện tại thêm script `n1.sh` nhúng trong đặc tả với năm chốt (a) đúng một tệp, (b) numstat `14 0`, (c) `diff --summary` rỗng, (d) mode 100644 giữ nguyên, (e) blob H bằng `git hash-object --no-filters` của tệp kỳ vọng dựng bởi N5 `--ky-vong`. §9 liệt kê thay đổi.

Việc: (1) Trích `n1.sh` và script N5 từ đặc tả, dựng rig git tạm: H đúng khối ⇒ rc 0; `chmod +x`, chèn sai vị trí cùng numstat, thêm tệp, CRLF ⇒ rc ≠ 0; đột biến bỏ từng chốt có ca đổi màu. (2) Tìm cách khác làm N1+N5 xanh giả (vd symlink thay tệp, đổi tên tệp, submodule, tệp thứ hai ngoài pathspec) hoặc đỏ oan với H hợp lệ. (3) §6 điểm chờ E2 đúng số lượt (nay 7 sau lượt này). (4) Rà L1–L7. Chỉ nêu finding mới nếu là lỗi thật có phản chứng chạy được hoặc mâu thuẫn trích dẫn được.

Đầu ra stdout: bảng finding lượt 6 (đóng/chưa), finding mới P0–P3. Dòng CUỐI CÙNG đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`. Chỉ approve khi không còn P0–P2.
