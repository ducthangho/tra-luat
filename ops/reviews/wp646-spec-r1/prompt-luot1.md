Bạn là reviewer ĐỘC LẬP (họ OpenAI) cho một ĐẶC TẢ packet tài liệu, chưa có mã. CHỈ ĐỌC; không ghi tệp trong thư mục làm việc; không gọi mạng. Chạy thử trong RAM hoặc bản sao dưới /tmp.

Thư mục làm việc: worktree kho tra-luat trên master 641108c, cộng `ops/specs/LEASE-TRUONG-KHAI-NGHIA-r1.md` (Issue #646). Packet sửa đúng một tệp `docs/PROTOCOL_DA_PHIEN.md`: thêm văn xuôi sau khối YAML §4 nói rõ `heartbeat_at` là lời khai (không cổng nào đọc), hạn nào có cổng cưỡng chế (`lease_expires_at_utc` ở ops/lease_publish.py; `lease_until` ở kiem-dong-wp D4), và `reviewed_sha_required` là mỏ neo xuất phát được phép bằng base (exact head do kiem-merge K0/K3/K4 và record-review đo).

Đọc: đặc tả; `.claude/skills/soan-spec/SKILL.md` (L1–L7); `docs/PROTOCOL_DA_PHIEN.md` §4 và §20; `ops/lease_publish.py` (BAT_BUOC, kiem, _phan_loai_lease, _BANG_LOP, _tinh_lop_tu_write_set, kiểm reviewed_sha_required); `.claude/dev/packet_loop.py` (cmd_kiem_dong_wp D4, cmd_kiem_merge K0/K3/K4, record-review); `docs/adr/0056-*.md`; `scripts/tl_core/workflow.py` doc-claims-check (L1 có quét trong khối mã có rào không).

Việc: (1) kiểm từng lời khai sự thật §0 bằng grep/đọc mã (số đếm 58/175, các tệp:dòng); (2) theo L1–L7, mỗi N có phép đỏ đỏ được không; (3) văn bản M1–M3 có nói đúng hơn hay sai sự thật nào về cổng không (tìm mọi chỗ khác đọc heartbeat_at, lease_until, lease_expires_at_utc, reviewed_sha_required, kể cả workflow .github/ và ops/*.py); (4) có lý do gì mục 1 của #646 không nên để ngoài phạm vi.

Đầu ra stdout: bảng kiểm sự thật, finding P0–P3 (chỗ, vấn đề, câu thay thế). Dòng CUỐI CÙNG đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`. Chỉ approve khi không còn P0–P2.
