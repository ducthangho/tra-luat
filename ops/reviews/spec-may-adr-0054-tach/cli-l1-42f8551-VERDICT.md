VERDICT: changes_requested
P0=0 P1=2 P2=2 P3=0   (đếm theo LỚP)

## Lớp hien-vat-hop-le-chua-du-tham-quyen — P1

- biểu hiện: `ops/specs/may-adr-0054-chung.md`:I2 — Phép đo người giữ được dùng làm thẩm quyền lease, dù `ai-dang-giu` không xác minh lease đã được workflow công bố.
- biểu hiện: `ops/specs/wp812.md`:M2 — Điều kiện nhận biên nhận thiếu ràng buộc `packet_id` và `generation` với state hiện hành.
- biểu hiện: `ops/specs/wp814.md`:M1 — Chỉ dùng phần kiểm lược đồ của vị từ approve khiến bảng lớp của verdict không phải approve chưa bị buộc khớp SHA/spec/generation đang review.
- biểu hiện: `ops/specs/wp812.md`:M3 — `github-actions` cộng luật `kiem-gate` chưa phân biệt đúng workflow và attempt phát check bắt buộc.
- đường lỗi cụ thể: Probe trong bộ nhớ trên mã tại HEAD cho thấy lease chưa công bố vẫn qua `lease_publish.kiem()` và được `lenh_ai_dang_giu()` trả `NGƯỜI_GIỮ 1`, rc=11. Validator biên nhận cũng không kiểm phạm vi packet/generation; receipt g1 có cùng SHA/spec vẫn thỏa các điều kiện M2 được liệt kê ở g2. Với CI, check bắt buộc đỏ ID 100 và check cùng tên xanh ID 101 từ workflow khác, cùng app và head, khiến `cmd_kiem_gate()` trả rc=0. I1 chỉ đòi có đầu vào Đ/H, còn I7 chưa bổ sung phạm vi workflow/attempt, nên các đường lỗi này vẫn được phép.
- hướng sửa ở mức lớp: Buộc mỗi bằng chứng khớp cả thẩm quyền nguồn lẫn phạm vi sử dụng: lease được cấp/công bố đúng hiện vật; mọi receipt khớp packet/generation/SHA/spec; CI khớp workflow/run/attempt bắt buộc theo protocol §10.2. Các kênh có hợp đồng khác nhau nên cần phép kiểm riêng theo cùng bất biến. Thêm đối chứng lease chưa công bố, receipt sai generation/SHA và check cùng app nhưng sai workflow; gỡ từng chốt phải làm ca tương ứng đỏ.

## Lớp dinh-danh-lop-khong-duoc-chuan-hoa — P1

- biểu hiện: `ops/specs/wp813.md`:M2 — Sổ `id → slug` bất biến chỉ giữ ánh xạ cho cùng ID, chưa giữ danh tính lớp khi connector tạo ID mới.
- biểu hiện: `ops/specs/wp815.md`:M2 — Finding muộn được cộng theo lớp nhưng chưa bị ràng buộc vào cùng hệ slug ổn định của các vòng trước.
- đường lỗi cụ thể: Cùng một nguyên nhân xuất hiện dưới comment `c1`, rồi `c2`; người gọi gán lần lượt `loi-a` và `loi-b`. Không ánh xạ ID nào bị đổi, nhưng mỗi bộ đếm chỉ bằng 1 nên `same_failure_limit=2` không chặn. Quy tắc ổn định của #814 chỉ được đặt cho bảng lớp từ biên nhận, chưa nối sang hai đường nhận finding này. Đây là đường lỗi đã nêu trong verdict r10.
- hướng sửa ở mức lớp: Đặt bất biến danh tính lớp xuyên ID, nguồn finding và generation; đổi cách phân lớp phải có bảng nối được đối chiếu với lịch sử. Thêm ca cùng nguyên nhân dưới hai ID mới phải tăng cùng bộ đếm, cùng đối chứng hai nguyên nhân độc lập vẫn được đếm riêng.

## Lớp vi-tu-tap-rong-qua-rong — P2

- biểu hiện: `ops/specs/may-adr-0054-chung.md`:I3 — Quy tắc “mọi vị từ trên tập” đều thất bại khi tập rỗng cấm cả những tập rỗng biểu thị kết quả sạch.
- biểu hiện: `ops/specs/wp812.md`:M2–M3 — Approve không finding và connector không P0–P2 cần chấp nhận tập finding rỗng, trái I3.
- biểu hiện: `ops/specs/wp814.md`:M2 — Vòng vá loại bỏ hết lớp P3 tạo tập lớp rỗng nhưng vẫn phải có đường hoàn tất.
- đường lỗi cụ thể: Receipt approve có `lop=[]`, CI đầy đủ và connector hoàn tất không finding là ứng viên sạch theo ADR-0054. Giữ nguyên I3 sẽ loại ứng viên này; nhận ứng viên lại vi phạm phần chung. Đây là mâu thuẫn bất biến, không phụ thuộc cơ chế triển khai.
- hướng sửa ở mức lớp: Tách tính đóng của enum khỏi yêu cầu khác rỗng. Quy định khác rỗng cho tập bằng chứng dương cần tồn tại, như check bắt buộc hoặc finding dùng mở lại; cho phép tập finding còn mở rỗng. Nghiệm thu phải có approve sạch và chuyển P3 từ một lớp về không lớp.

## Lớp bat-bien-chung-phu-thuoc-nguoc — P2

- biểu hiện: `ops/specs/may-adr-0054-chung.md`:I5 — Mọi packet con phải giữ yêu cầu một hàm xét dừng duy nhất tại mọi cửa đi tiếp.
- biểu hiện: `ops/specs/wp812.md`:M1–M3, `ngoai_pham_vi` — Packet mở các cửa init/approve/accept nhưng loại xét dừng dùng chung khỏi phạm vi sang #813.
- biểu hiện: `ops/specs/wp813.md`:M1, `depends_on` — Hàm đáp ứng I5 chỉ được giao ở successor phụ thuộc #812.
- đường lỗi cụ thể: Mã hiện hành chưa có `_xet_dung`; các phép chặn nằm riêng trong từng handler. Candidate cuối #812 phải hoặc làm phần đã bị loại khỏi phạm vi, hoặc vi phạm I5 tại nghiệm thu. #813 phụ thuộc #812 nên không thể cung cấp phần thiếu để nghiệm thu #812 độc lập.
- hướng sửa ở mức lớp: Giao phần bất biến cần thiết cho predecessor đầu tiên sử dụng nó, hoặc khai rõ hiệu lực theo giai đoạn cùng acceptance cho trạng thái trung gian chưa kích hoạt. Kiểm riêng candidate cuối #812 trước khi có mã #813 để chứng minh lát cắt đầu tự đủ.