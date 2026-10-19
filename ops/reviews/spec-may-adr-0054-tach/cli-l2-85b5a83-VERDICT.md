VERDICT: changes_requested
P0=0 P1=1 P2=2 P3=0

## Lớp hien-vat-hop-le-chua-du-tham-quyen — P1

- biểu hiện: `ops/specs/wp812.md:muc_tieu/M2` — Các điều kiện của `_du_dieu_kien_approve` chưa buộc verdict trong biên nhận phải là `approve`.
- đường lỗi cụ thể: Biên nhận đúng packet, generation, SHA, spec, danh tính và assurance nhưng mang `changes_requested` với toàn P3 vẫn thỏa các điều kiện đã liệt kê. Người gọi truyền `--verdict approve` có thể đưa nó vào `approved_pending`, rồi `accepted`. Trong mã hiện hành, `a.verdict` điều khiển transition độc lập; probe chỉ đổi verdict trong bộ nhớ cho thấy cả `_thieu` và `_neo_git` vẫn nhận `approve`, `changes_requested`, `blocked`. I10 đã khóa phạm vi nhưng chưa khóa quyết định.
- hướng sửa ở mức lớp: Ràng buộc quyết định ghi state với verdict của reviewer trong hiện vật đã xác minh; vào `approved_pending` phải có verdict `approve`. Thêm baseline approve và các ca chỉ đổi verdict thành `changes_requested`/`blocked`; đột biến bỏ đối chiếu phải làm ca đỏ. Giữ khả năng ghi hai verdict ấy vào lịch sử theo #814.

## Lớp neo-hien-vat-khong-phan-biet-ngu-canh — P2

- biểu hiện: `ops/specs/may-adr-0054-chung.md:bat_bien/I10` — Buộc mọi hiện vật tại một cửa khớp cùng tuple của state, kể cả bằng chứng thuộc nguồn và đích khác nhau.
- biểu hiện: `ops/specs/wp815.md:muc_tieu/M1–M2` — Chuyển generation cần đồng thời lease g2 và biên nhận finding muộn thuộc g1.
- biểu hiện: `ops/specs/wp816.md:muc_tieu/M1` — `va-ci` cần bằng chứng connector trên head cũ H0 trong khi `pending_sha` đã là bản vá S1.
- đường lỗi cụ thể: Với `record-push va-ci`, H0 phải khác S1 vì bản vá đổi commit; bằng chứng connector đúng H0 bị I10 loại nếu phải khớp SHA ứng viên hiện hành. Tương tự, tại chuyển generation, không một generation hiện hành duy nhất nào đồng thời khớp lease g2 và biên nhận nguồn g1. Các đường hợp lệ mà nghiệm thu yêu cầu vì thế xung đột với bất biến chung.
- hướng sửa ở mức lớp: Định nghĩa neo theo vai trò của hiện vật: bằng chứng nguồn khớp state nguồn, bằng chứng ứng viên khớp state đích. Giữ đủ bốn thành phần neo cho từng vai trò. Thêm ca dương H0≠S1 và g1≠g2, cùng ca âm tráo nguồn/đích; tránh sửa bằng cách bỏ kiểm SHA hoặc generation chung.

## Lớp khoi-tao-moi-mau-thuan-duong-cu — P2

- biểu hiện: `ops/specs/may-adr-0054-chung.md:bat_bien/I9` — Yêu cầu đường legacy giữ nguyên và mọi ca có sẵn tiếp tục đạt.
- biểu hiện: `ops/specs/wp812.md:muc_tieu/M1,nghiem_thu` — `init` bắt buộc đọc, xác minh lease/spec; thiếu lease phải dừng và không tạo state.
- đường lỗi cụ thể: Trên `85b5a83ca65f1a3c7b8ae9d5cc0176c26656b840`, `cmd_init` chưa cần lease vẫn trả rc=0 và tạo `awaiting_lease`; probe chặn `_save` trong bộ nhớ xác nhận hành vi này. Ca hiện có `case_init_KHONG_duoc_tu_cap_lease` đòi chính kết quả ấy. Cùng đầu vào thiếu lease không thể vừa giữ hành vi cũ theo I9, vừa không tạo state theo M1.
- hướng sửa ở mức lớp: Chốt lại phạm vi tương thích và thời điểm bắt buộc xác minh lease/spec, rồi làm I9 và M1 thống nhất. Khóa bằng ca legacy chưa có lease và ca packet áp ADR-0054 không thể đi tiếp bằng đường legacy. Không dùng ngoại lệ theo môi trường test để che mâu thuẫn.