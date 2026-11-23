# wp1500 r1 — K1 nhận tiền tố WP chữ hoa trong H1 đặc tả

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab
dieu_kien_merge: ADR-0060@36d7c5dcdcbbb27176b75135125b9009f9fe0587

- packet_id: wp1500; revision: 1;
- packet_issue: 1500
- nguon_cap_viec: https://github.com/ducthangho/tra-luat/issues/1500
- review_class: sensitive
- pham_vi_e: E5 vì sửa cổng merge K1. Không chạm E4.
- Trạng thái đề xuất. Base canonical `a99a74f75867172fe62f984d7528f5d5bd73dacb`, đo lúc 16:18 UTC ngày 23/11/2026. Các blob trong write set giống base nơi đã ghi nhận lỗi WP1499.

## Mục tiêu và write_set

1. `.claude/dev/packet_loop.py`: Trong đường đặc tả ghim `spec_ref` của K1, H1 hợp lệ `# WP<digits> r<N> — <title>` được diễn giải là cùng định danh với lease `wp<digits>` khi chuỗi chữ số ASCII trùng nguyên văn. Chỉ bổ sung cách đối chiếu tiền tố ASCII `WP` trong H1. Giữ mọi kết quả vốn khớp nguyên văn, gồm H1 và lease cùng chữ hoa. Dùng định danh H1 sau đối chiếu để kiểm nhất quán với các khai báo khác. Trường `packet_id` tường minh, kể cả Markdown inline, vẫn phải khớp lease nguyên văn.
2. `.claude/dev/packet_loop_test.py`: Kiểm thử K1 qua đường đọc đặc tả ghim. Giữ ca hồi quy ADR-0063, thêm ca dương và ca âm phân biệt việc chỉ đối chiếu tiền tố H1 với việc hạ chữ toàn bộ định danh.
3. `docs/adr/0063-merge-spec-ref-va-human-audit.md`: Ghi rõ dạng H1 được đối chiếu trong contract nguồn và giới hạn của nó. Bảo toàn các neo rollout và nội dung K4.

## Ngoài phạm vi

Không thay đổi byte đặc tả, lease, audit hoặc head WP1499. Không cho thêm quyền merge, bỏ cổng hoặc sửa cơ chế audit. Giữ nguyên revision, kiểm grammar trên văn bản gốc, OID/ref/path, SHA-256, ưu tiên nguồn, kiểm trùng bytes và đường legacy không có `spec_ref`. Không đưa phép Unicode case-fold, chuẩn hóa trường tường minh, chuẩn hóa dạng viết lẫn hoa/thường hoặc chuyển phần số sang kiểu số nguyên vào phép so.

## Nghiệm thu

- A1: H1 `WP1499 r6` và lease `wp1499` qua K1. Cùng ca có khai báo tường minh `wp1499` cũng qua. H1 chữ thường và trường hợp H1/lease cùng chữ hoa đã khớp sẵn vẫn qua. Bỏ phép đối chiếu mới hoặc tiếp tục áp nó lên lease đã khớp chữ hoa thì ít nhất một ca dương phải đỏ.
- A2: Sai chuỗi chữ số, kể cả thêm/bớt số 0 đầu; tiền tố viết lẫn; mã ngoài WP chỉ khác hoa/thường; khai báo tường minh chữ hoa hoặc khác mã; revision xung đột vẫn bị K1 chặn. Sai OID/path/hash, nguồn trùng khác bytes và H1 sai grammar vẫn đỏ tại chốt tương ứng. Đột biến hạ chữ toàn bộ định danh hoặc chuẩn hóa cả trường tường minh phải làm ca phản chứng đỏ.
- A3: Dùng fixtures hiện hành xác nhận K4 vẫn yêu cầu audit khớp đúng head, mã lease và hash đặc tả. Khóa trường hợp audit lệch định danh phải đỏ. Chạy bộ `packet_loop_test.py` và báo riêng kết quả ca mới, ca hồi quy và các đột biến mục tiêu thuộc thay đổi này.
- A4: Review đối chiếu trọn đoạn mô tả mới trong ADR với hành vi A1–A3 và neo rollout hiện có. Đoạn bỏ mất giới hạn H1, cho phép hạ chữ trường tường minh hoặc làm mất neo rollout phải đỏ khi đối chiếu.

## Căn cứ và điều kiện triển khai

- hinh_dang_ke_thua: Một hình dạng lỗi đã ghi ở PR #1499, K1 báo `spec packet_id không khớp lease` khi H1 chữ hoa và lease chữ thường mô tả cùng WP. [Biên nhận](https://github.com/ducthangho/tra-luat/pull/1499#issuecomment-7104415483)
- luat_dung: E5 theo ADR-0067. Chủ kho duyệt SHA-256 theo đặc tả này và cấp quyền E5 và lease riêng trước khi sửa cổng. Review độc lập, audit chủ kho và duyệt land neo head theo protocol hiện hành.
- chua_do_duoc: Chưa có diff ứng viên, kết quả CI, baseline test mới hoặc kiểm thử đột biến của #1500. Bằng chứng PR #1499 chỉ dùng để xác định lỗi đầu vào.

Nội dung đề xuất ảnh hưởng đúng ba tệp nêu trong write_set. Không sửa đối tượng được cấp quyền, nguồn thẩm quyền hay scope của lệnh merge. Thay đổi duy nhất về điều kiện tiếp nhận là nhận bí danh tiêu đề H1 đã mô tả ở A1.
