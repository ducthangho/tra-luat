# ADR-0063 — Nguồn spec ghim OID và human audit exact head

- **Trạng thái:** Accepted; có hiệu lực từ commit land ADR này trên first-parent `master`.
- **Nguồn:** Packet #1187, PR1184-MERGE-CONTRACT r1, spec đóng băng do owner duyệt.

## Contract nguồn

K1 giữ spec tại H; khi lease khai `spec_ref`, nguồn authoritative là `refs/heads/...@<OID40>` và `spec_path` đúng `--spec`. Đọc object bất biến, so bytes SHA256 với `spec_hash` và `spec_sha256_required` nếu có, Packet/revision với lease. Spec dạng YAML dùng `packet_id:`/`revision:` riêng dòng; dạng Markdown dùng dòng `- packet_id: ...; revision: N;`. Không đọc working tree hoặc resolve nhánh trôi. Nguồn đã khai lỗi thì đỏ; có cả blob tại H thì phải cùng bytes/hash. Giữ ba trạng thái 0/1/≥2 dòng ADR-0062.

K4 giữ nguyên model run/stdout. Human dùng `--human-audit-comment` raw API JSON riêng; không đổi thành artifact model. Comment phải từ owner canonical `ducthangho`, GitHub `User`, association `OWNER`, đúng repo/PR, ID/URL/timestamps; caller không đổi owner. Body là duy nhất YAML record, cấm duplicate key/alias, đóng schema `human_exact_head_audit.v1` trong spec. Exact H/tree/spec/Packet/revision/generation/PR, verdict approve, assurance human_audited và hai review axes phải khớp. `open_findings` là list `{slug, severity}`; P0–P2 chặn, P3 chuyển K5 với khoá `human:<slug>`. Free text và agent repost không phải audit. Khi truyền cả model và human, cả hai phải hợp lệ trên cùng H.

## Thời điểm và chuyển tiếp

M5/M12 vẫn yêu cầu review offline trước push cho candidate mới. Human path đọc `--human-remote-run` raw API push run đúng repo/full H/URL/created_at. Candidate mới cần audit updated_at trước run; người vận hành còn phải xác minh đó là lần push đầu, không dùng run chạy muộn để hợp thức hoá review sau push.

Riêng candidate đã ở GitHub trước ADR-0062 (`1f0941e9bba1d1d517eda4174167b81963c06bd5`, merged_at `2026-11-04T08:36:24Z`), được audit sau push khi có thêm `--human-transition-comment` của owner. Body đóng schema `human_audit_transition.v1`: các field packet/revision/generation/pr/reviewed_sha/reviewed_tree/spec_sha256 như audit; thêm `adr0062_oid`, `remote_run` URL, `disposition: accept_post_push_audit`, `reason` khác rỗng và `transition_source` URL chính comment. Phải xác minh raw run trước mốc, OID mốc trên first-parent master và thật sự đưa ADR-0062 vào cây, ADR-0063 đã land. Thiếu hoặc sai bất kỳ binding nào thì chặn; H/tree đổi làm audit cũ stale.

Đây là ngoại lệ thời điểm có owner disposition cho candidate lịch sử; không tuyên bố đã review trước push. Không hồi tố packet đã merge, không sửa lịch sử Accepted. Audit không phải approval/authorization/merge. M1/M3/M6/M9, K0/K2/K3/K5/K6/K7, Windows, CI exact H và thời hạn review giữ nguyên. Ngân sách/lịch sử push, advisory calls/rounds không reset; owner phải checkpoint budget trước connector #1184. Không tự nâng advisory thành human/cross assurance.
