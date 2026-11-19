# Review độc lập ĐẶC TẢ (chưa thi công) — packet #1342 WP1174-WINDOWS-BACKEND r5 (bậc r1d-a1-ii), lượt 1

Bạn là reviewer độc lập, CHỈ ĐỌC. Không sửa tệp, không commit, không gọi mạng.

- Cây làm việc: thư mục hiện tại = worktree tách rời của `origin/master` `11bd0336d00b4a9544e70dcbbe049d372053a3ec`. Tệp CHƯA commit duy nhất là đặc tả cần review: `ops/specs/WP1174-WINDOWS-BACKEND-r5.md` (sha256 4657e5d22bbbb05a50bfaaf4b1ff8833c01119ff5ef6d1c80323ee4b4ca5843e).
- Đặc tả bậc trước (r4, đã land a2c7d75): `git show origin/ops/wp1342-r4-spec:ops/specs/WP1174-WINDOWS-BACKEND-r4.md`; các bản nháp và 13 lượt review r4 ở `git show origin/ops/wp1342-r4-spec:ops/reviews/wp1342-spec-r4/<tệp>` (đặc biệt `dac-ta-ban2.md` định nghĩa J4/J5/J12/e1/e2 cũ, và `luot2.verdict.txt` có finding về e1/e2/J12 mà r4 hoãn sang bậc này). Hồ sơ land r4: `ops/land/pr1407-wp1342-land-evidence.yaml` và `ops/land/pr1407-wp1342-provenance/`.
- Quy tắc: `docs/PROTOCOL_DA_PHIEN.md`, `.claude/skills/soan-spec/SKILL.md`, `docs/adr/0053-*.md`, `docs/adr/0055-*.md`.
- Công cụ đo sẵn (ngoài kho, chỉ đọc/chạy): `/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/spec1342a1ii/n2_test_r5.py` (= n2_test_r4.py sau sed như §0 ghi), `/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/spec1342a1ii/n2_r5_extra.py` (hai phản chứng mới + khối mô phỏng r5; chạy từ thư mục `/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/spec1342a1ii`), `/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/spec1342a1ii/base_r5.py` (= blob test base).

## Việc (ĐO bằng lệnh, ghi lệnh + rc; chỗ nào không đo được ghi `not_run` và lý do)

1. Đo lại mọi số ở §0 (SHA, blob, số dòng, numstat, ba phép đo dòng khai ADR, neo `_1174_WIN_JOB_LIMIT = 0x2000` khớp đúng 1 lần, `0x2800` 0 lần trong tệp test base) và báo số nào sai.
2. Phạm vi: đối chiếu r4 §2 "Để r1d-a1-ii", r4 bản 2 (J4/J5/J12, e1/e2) và finding lượt 2 r4 cho e1/e2/J12 — bản này có phủ đủ, có chỗ nào bị bỏ hoặc tự thêm ngoài phạm vi không. Quyết định chọn write set CHỈ tệp test (Đ1) có hợp lý không.
3. Tìm đường làm J4/J5/J12 XANH GIẢ hoặc ĐỎ sai nhãn trên Windows thật: job ngoài của tiến trình chạy ca che phản chứng; bước fixture lạ bị bỏ qua im lặng; quan sát sau khi job ngoài đóng; tái dùng PID; thứ tự assertion; cửa sổ 90 s; hành vi Win32 khai ở §0 có sai so với tài liệu Microsoft mà bạn biết không (nói rõ đâu là tài liệu, đâu là suy luận).
4. Bảng §4b: mỗi đột biến có khớp đúng một chỗ, có dấu hiệu riêng không (e1 vs e2 vs a2 r4 vs a1), đối chứng có hợp lệ không, e1c có thật sự đo răng của đối chứng (ii) không.
5. N1–N8: mỗi tiêu chí có phép đo làm nó ĐỎ chạy được không. Chạy `cd /tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/spec1342a1ii && python3 n2_test_r5.py base_r5.py base_r5.py` và `python3 n2_r5_extra.py` để kiểm lời khai N2/§0.
6. Ngân sách dòng (ước 127–181, trần 450) có cơ sở không.

Lưu ý giao việc: nếu một hướng thử cần nội dung tệp dạng đường dẫn thoát khỏi cây thư mục, MÔ TẢ BẰNG LỜI thay vì tự soạn nó.

## Đầu ra

Tiếng Việt. Mỗi finding: mức P0–P3, mục đặc tả, bằng chứng (lệnh + kết quả), câu thay thế đề xuất. Cuối cùng một bảng tóm tắt. DÒNG CUỐI CÙNG đúng một trong hai:
KET_LUAN: approve
KET_LUAN: request_changes
