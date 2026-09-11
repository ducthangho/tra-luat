# WP422 — giải mã đường dẫn Git porcelain — r1/g1

## Authority
Chủ kho chỉ thị trực tiếp: “Xử lý #422 bằng agy đi, cấp lease, cấp quyền cho bạn tự quyết”. Sau đó: “Lặp vá, cross-review (tìm, phân theo lớp lỗi, không theo từng lỗi), đăng verdict cho tới khi approve hoặc hết P1, P2. Không CI, full CI trong quá trình lặp.” Controller ghi hộ quyền được giao; không suy danh tính Approver từ tài khoản GitHub.

Controller được tự quyết đặc tả, cấp lease, điều phối, quyết định remediation và công bố bằng chứng trong phạm vi #422. Không cấp quyền sửa nợ khác, secrets, deploy/LIVE hoặc giả verdict. E1/E2 của WP498 không được kế thừa: theo quyền tự quyết mới, WP422 dùng cơ chế thủ công được mô tả dưới đây riêng cho packet này.

## Frozen contract
- Issue422; revision1; generation1; base_sha6786637343452359eeb2ec5aaaaef709a623be95.
- Branch codex/wp422-g1-agy; clone riêng; executor google_antigravity / antigravity CLI / machine-local, requested model gemini-3.1-pro-high. Không khai runtime-attested khi receipt không chứng minh.
- Reviewer openai_codex ở session riêng, không nhận context Executor; sensitive vì thay hook phát hiện ghi.
- Product write set đúng hai tệp: .claude/hooks/subagent_ghi_detect.py và .claude/hooks/subagent_ghi_detect_test.py. Derived set rỗng; tối đa300 dòng thêm. Không sửa settings, workflow, launcher, snapshot trust, manifest/version/changelog.
- Bốn trường Dispatcher change_policy_sha/effective_write_set/required_checks/land_obligations chưa có nguồn máy hiện hành: giữ null trong lease; dùng scope và acceptance ở đây làm hợp đồng thủ công. Không giả policy hash, không đổi packet_loop để chấp nhận provider AG.
- Authority files do Controller sở hữu trên nhánh codex/wp422-authority-r1; AG chỉ đọc.

## Acceptance theo lớp lỗi
1. Giải trích dẫn đường dẫn porcelain đúng byte: octal UTF-8 thành tên Unicode thật, escapes tab/newline/quote/backslash không bị phá; tên không trích dẫn giữ nguyên. Không làm hỏng tên chứa Unicode đã hiện nguyên văn khi core.quotePath=false.
2. Tên byte không phải UTF-8 round-trip bằng surrogateescape trên nền hỗ trợ; không biến thành unknown vì giải mã mất byte. Khai rõ trường hợp Windows không biểu diễn được tên đó. Malformed input phải trả unknown/None hoặc thất bại có kiểm soát, không crash cả lượt hay khai clean giả.
3. Đo bằng kho Git thật, thư mục cha ASCII, tên tệp có dấu. Hook unchanged: clean với so_duong_da_bam_noi_dung>0, khong_bam_duoc rỗng/vắng; sửa nội dung cùng đường dẫn: changed. RC hook vốn0 không đủ nghiệm thu. Đo core.quotePath=true/false; ASCII đối chứng giữ đúng.
4. Test mới phải bắt đúng hồi quy bỏ bước giải mã, có mutant thực chạy chết bởi ca đích; t25 cũ không bị ghi công cho lỗi tên tệp mà nó không đo. Kiểm thêm escaped names và nguyên vẹn byte để phát hiện cùng lớp lỗi, không chỉ ví dụ Vietnamese.
5. Targeted/component probes Windows native và WSL Linux, baseline/candidate cùng đầu vào. Không chạy full selftest, full CI, workflow_dispatch hoặc tạo PR trong vòng lặp. Đăng verdict trên Issue422; push nhánh codex không có PR khi cần neo immutable commit.
6. Ruff F trên hai tệp không tăng lỗi, git diff --check, exact scope/size, SHA/tree và hashes bằng chứng phải khớp. Phép đo failed/skipped/not_run khai riêng.
7. Codex review theo lớp lỗi: (a) byte/encoding/parser semantics; (b) clean/changed/unknown và fail-close; (c) test oracle/mutation attribution; (d) scope/provenance. Mỗi lớp phải xét phản chứng liên quan và xếp P1/P2/P3; không chỉ sửa từng ví dụ.
8. Lặp AG remediation và Codex independent review, đăng từng verdict đến approve hoặc không còn P1/P2 theo chỉ thị chủ kho. Đây là override trần hai vòng riêng #422; sau mỗi2 vòng Controller đánh giá hội tụ. Finding không giảm hoặc cần scope khác: ghi checkpoint và tự chọn tách/giữ phạm vi theo quyền được giao; không lặp vô hạn cùng cách vá.

## Manual lifecycle
Lease chỉ active sau scan ownership toàn bộ remote branches, full sorted ref-set snapshot (kể cả tags), lease check và publication/readback. Heartbeat <=30m; mỗi AG run <=45m; lease6h; review SLA2h. Head đổi thì verdict cũ stale. Ref drift phải phân loại trước ghi tiếp; không lấy ref count thay hash. Handoff gồm head/tree, changed paths, test commands/RC/positive markers, provider/model identity limits, finding-class closure.

No-CI loop completion là technical accepted (approve hoặc0P1/P2), không phải full gate pass/landed. Không tự tạo machine cross_approved khi thiếu identity receipts. Việc PR/land/gate sau vòng lặp được báo riêng; không kích hoạt CI trong vòng lặp.
