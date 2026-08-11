# ADR-0018 — EOL canonical theo loại tệp

- **Trạng thái:** Accepted (2026-08-03, phiên grilling)

Mọi tệp text trong repo dùng LF, riêng `*.cmd` và `*.bat` dùng CRLF; binary giữ nguyên byte. `.gitattributes`,
`.editorconfig`, writer tạo artifact tracked, pre-commit và CI cùng cưỡng chế một chính sách, thay cho `* -text`
và việc chấp nhận mỗi tệp tự giữ dạng EOL lịch sử. Quyết định này đổi byte có chủ đích ở một migration riêng,
đòi hỏi renormalize, kiểm diff, tái sinh manifest và chạy parity Windows–Linux; đổi lại checkout và artifact không
còn phụ thuộc nền tảng hay công cụ đã ghi tệp.

Migration EOL là một maintenance mission có cửa sổ riêng. Nếu dispatcher chưa tồn tại, người vận hành thực hiện
**operational freeze/drain**: chốt từ `origin/master` mới nhất, kiểm kê worktree cùng PR/branch đang sống, ngừng
mở writer mới và yêu cầu từng chủ phiên push, bàn giao hoặc hủy. Khi dispatcher đã tồn tại, cùng bất biến này
được cưỡng chế bằng `PAUSE`, ngừng cấp lease và đợi mọi lease kết thúc; không dùng một control chưa được triển
khai làm điều kiện bootstrap.

Migration gồm ba commit tách trách nhiệm: (A) policy `.gitattributes`/`.editorconfig`, helper ghi text canonical
và validator Python dùng chung cho hook/CI; đồng thời thay mọi hook shell chỉ so EOL với `HEAD`; (B) chỉ
`git add --renormalize .`, không trộn logic; (C) tái sinh manifest, golden/derived artifact rồi chạy parity
Windows–Linux. Validator kiểm blob trong index theo policy đích, xử lý đúng Unicode, khoảng trắng và file mới,
không dựa vào `core.autocrlf` hay shell command substitution. `--no-verify` không phải đường migration chuẩn.
Golden byte fixtures và binary tiếp tục `-text`.

Trước khi bắt đầu ghi lại SHA nền và sau khi land ghi SHA **EOL base**. Commit renormalize phải được chứng minh
chỉ đổi newline. Mọi branch/worktree cũ rebase lên EOL base trước khi tiếp tục ghi hoặc nhận lease mới;
dispatcher chỉ mở lại sau khi land gate xanh. Cách này chấp nhận một lần xung đột có kiểm soát để loại bỏ xung
đột newline lặp lại về sau.
