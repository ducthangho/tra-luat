# ADR-0017 — GitHub PR là bàn giao chính; canonical độc quyền phát hành

- **Trạng thái:** Accepted (2026-08-03, phiên grilling)

GitHub là nguồn sự thật điều phối: Issue giữ work packet, prompt bàn giao, phạm vi và trạng thái; pull request
giữ thay đổi mã, bằng chứng test và review. Các task local hoặc cloud làm việc trên branch/worktree riêng và bàn
giao bằng PR; bundle chỉ là đường dự phòng khi task không truy cập được Git. Quyền merge vào canonical, bump
version và deploy vẫn thuộc duy nhất canonical. Cách này dùng chung được trên máy tính, điện thoại và cloud nhưng
chấp nhận phụ thuộc GitHub; quyết định này thay thế hình thức bàn giao chỉ-bundle của ADR-0001.

GitHub Actions là dispatcher và nơi chạy worker cloud khi máy local không sẵn sàng. Credential nhà cung cấp nằm
trong GitHub Secrets; workflow chỉ được ghi Issue, PR và feature branch. Dispatcher và worker không được merge
nhánh canonical, bump version hoặc deploy. Giới hạn này giữ chuỗi công việc chạy khi máy Windows tắt mà không
chuyển quyền phát hành ra khỏi canonical.

Mỗi work packet chỉ định đúng một executor (`claude` hoặc `codex`) làm bên ghi duy nhất; nền tảng còn lại review
PR ở chế độ read-only. Dispatcher chỉ reroute sau khi đã thu hồi claim cũ, nên hai nền tảng không bao giờ cùng
triển khai một packet hoặc cùng ghi một branch.

Mỗi work packet cũng bắt buộc chỉ định môi trường thực thi (`cloud` hoặc `local`) độc lập với executor; mặc định
là `cloud` vì máy Windows có thể tắt. `local` chỉ dùng khi cần tài nguyên cục bộ, kiểm thử Windows hoặc người dùng
chọn rõ. Dispatcher không được âm thầm đổi môi trường; nếu môi trường đã chọn không khả dụng thì chuyển packet
sang `PAUSE`. GitHub Issue/PR là trạng thái bền xuyên thiết bị; lịch sử chat chỉ là giao diện quan sát/thao tác,
không phải nguồn sự thật.

Worker cloud là lane offline tuyệt đối: chỉ nhận provider credential và GitHub token tối thiểu để đọc work packet,
ghi feature branch/PR và chạy gate offline. Config và credential của Drive, GAS, registry, NLM và deploy không
được cấp cho workflow worker. Kiểm thử hoặc thao tác LIVE chỉ diễn ra ở canonical sau khi người dùng cho phép;
guard nhận diện CI chỉ là lớp chống nhầm bổ sung, không được coi là ranh giới an ninh.

Claim vật lý là lease do dispatcher tuần tự cấp, gồm `packet_id`, `executor`, `branch`, `write_set_hash`,
`generation`, `heartbeat_at` và `lease_until`; assignee/label chỉ là hình chiếu UI. Sau 30 phút không có tiến
triển, dispatcher thu hồi lease và tăng generation trước khi reroute. CI từ chối branch hoặc PR mang generation
cũ, nên worker cũ sống lại không tạo split-brain.

Write set khai báo chỉ nhận đường dẫn chính xác hoặc prefix thư mục, được chuẩn hóa Unicode, hoa/thường và dấu
phân cách theo path portable. Dispatcher tính effective write set bằng closure bắc cầu của change-impact rules
có hướng trên canonical rồi mới kiểm giao nhau/cấp lease; CI tính lại closure và từ chối diff ngoài tập hiệu lực
hoặc lệch policy/hash. Mở rộng phạm vi hay đổi closure là một lần cấp lại lease. Các tệp phái sinh dùng chung
(`VERSION`, `CHANGELOG.md`, `RELEASE_MANIFEST.json`) chỉ thuộc phiên land tuần tự.

Mỗi Mission Issue khai mission envelope; mặc định mỗi packet chạy tối đa 3 lần và 45 phút/lần, cùng fingerprint
lỗi xuất hiện 2 lần thì `blocked`, toàn mission tối đa 20 packet và độ sâu kế nhiệm 5. Chạm trần hoặc cần quyền
LIVE chuyển mission sang `PAUSE`. Thuật ngữ claim vật lý là `leased`; điều kiện `complete` không lặp tại ADR này
mà tuân duy nhất ADR-0030 và state machine trong protocol để không bỏ sót trạng thái non-terminal.

Khi kết thúc, executor bắt buộc xuất handoff máy đọc được với `status` (`done`, `needs_followup` hoặc `blocked`),
tóm tắt, changed paths, bằng chứng test, việc còn lại, failure fingerprint và danh sách packet kế nhiệm. Mỗi đề
xuất kế nhiệm khai mục tiêu, write set, phụ thuộc, executor, môi trường, tiêu chí hoàn tất và khóa chống sinh
trùng. Dispatcher chỉ nhận handoff hợp lệ, khử trùng theo mission/generation và khóa đó, rồi tự tạo Issue/prompt,
lease và branch/worktree riêng. Packet cloud chạy ngay; packet local chờ host Windows trực tuyến rồi tự chạy.
Chỉ `PAUSE`, `blocked`, yêu cầu quyền LIVE hoặc cổng land/deploy mới cần người dùng can thiệp.

Đánh số được trì hoãn hoàn toàn tới phiên land. Worker không sửa `VERSION`, hằng version trong `tl.py`, header
`SKILL.md`, `CHANGELOG.md` hoặc `RELEASE_MANIFEST.json`; test và artifact dùng ID bền `wp<issue>_<slug>`, còn
ghi chú thay đổi nằm ở `changelog.d/wp-<issue>.md`. Phiên land mới gán `r`/version, bump ba chỗ, hợp nhất và xóa
fragment, tái sinh manifest rồi chạy full gate. Nhờ vậy không cần allocator số trung tâm.

CI tách hai lane. Worker gate trên PR kiểm lease generation, effective write set, EOL và các gate offline, sinh manifest
tạm ngoài repo để verify/bundle nên worker không commit tệp phái sinh. Land gate tuần tự mới rebase/tích hợp PR,
gán release, hợp nhất fragment, tái sinh manifest committed và chạy full parity Windows–Linux trước khi merge
canonical hoặc deploy.
