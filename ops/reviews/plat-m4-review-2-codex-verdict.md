Finding P2 lượt 1 đã **đóng**: với `https://user:SENTINEL@host.test/mcp`, `urlopen` giả ghi `full_url`/`host` nhưng nhận `0` lời gọi; kết quả là `khong_do_duoc`, `ok=false`, mô tả không chứa sentinel. URL sạch tạo đúng một bản ghi `{full_url: https://host.test/mcp, host: host.test}`. Ca `t143` đạt `1/1`.

### Findings

1. **P1 — Không có đặc tả có thẩm quyền**

   - Bằng chứng: `sha256sum ops/specs/plat-m4-v0.md` trả `rc=1, No such file or directory`; `git ls-tree` cũng không có đường dẫn này. Băm yêu cầu vì thế là **KHÔNG ĐO ĐƯỢC**, không phải “khớp”.
   - Bất biến bị cắt: reviewer không thể kiểm trục Spec hoặc xác minh `spec_hash` trước review.
   - Gợi ý vá: sửa review bundle/chỉ thị để cung cấp artifact bất biến đúng băm mà không thêm tệp thứ ba vào delta sản phẩm. Khóa bằng kiểm băm, delta đúng hai tệp và worktree sạch. Tránh trỏ tới ref động vì có thể stale.

2. **P2 — URL méo vẫn làm lộ bí mật qua mô tả**

   Tại [launcher.py], hai nhánh lỗi vẫn nội suy nguyên `url`.

   - Bằng chứng với `urlopen` giả: các đầu vào `http:///user:SENTINEL@host/mcp`, `javascript:user:SENTINEL@host`, `http ://user:SENTINEL@host/mcp`, và `http://?u=user:SENTINEL@host` đều trả `khong_do_duoc`, không probe, nhưng `desc_has_secret=true`.
   - Bất biến bị cắt: dữ liệu có thể là credential không được đi vào diagnostic, kể cả URL không parse thành `userinfo`.
   - Gợi ý vá: không nội suy URL thô trong mọi nhánh từ chối; chỉ trả loại lỗi hoặc metadata đã lọc. Thêm các sentinel malformed-URL trên và mutant đổi thông báo an toàn về `{url!r}`. Rủi ro là giảm chi tiết chẩn đoán; có thể giữ `scheme` và cờ `hostname_present` thay vì URL.

3. **P2 — Test chưa khóa biên cấu trúc của `userinfo`**

   Tại [launcher_test.py]:

   - Ba mutant khai sẵn đều có răng: bỏ scheme guard `1/1`, bỏ userinfo guard `1/1`, từ chối nhưng vẫn in URL `1/1`.
   - Mutant bổ sung `if ai_ep != (None, None):` → `if "@" in str(url):` vẫn cho `t143` đạt `1/1`, nhưng chặn nhầm `@` trong path/query.
   - Mutant `if p_ep.username:` cũng vẫn đạt `1/1`, nhưng `https://:SENTINEL@host/mcp` bị probe và sentinel xuất hiện trong cả `full_url` lẫn `host`.
   - Bất biến bị cắt: suite phải phân biệt `userinfo` theo cấu trúc, không theo ký tự hoặc username truthy.
   - Gợi ý vá: thêm ca `@` trong path/query phải probe, cùng ca username rỗng/password có giá trị phải bị từ chối; nối hai mutant trên vào bảng. Cập nhật docstring hiện vẫn khai “sáu điều + điều thứ bảy”, chưa phản ánh các ràng buộc mới. Rủi ro vá là chặn oan URL hợp lệ nếu quay lại dò ký tự.

Bằng chứng tổng: Linux/CPython 3.11.15 đạt `142/142` ca chạy; mutation đạt `134/134`, một mutant riêng Windows là **KHÔNG ĐO ĐƯỢC**. Windows và endpoint MCP thật cũng **KHÔNG ĐO ĐƯỢC** tại môi trường này. Delta đúng hai tệp, `git diff --check` đạt, HEAD không đổi và `git status --short` rỗng.

VERDICT: blocked
Reviewed commit: 7a2320fe13b4aad3e7b298d070125a01762a8e54
