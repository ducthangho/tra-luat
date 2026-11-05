Bạn là reviewer phản biện. Trả lời NGẮN, từng câu riêng, đánh số Q1..Q5. Với MỖI câu, cho đúng ba mục:
(a) kết luận: đồng ý / không đồng ý / còn tuỳ, kèm lý do một đến ba câu;
(b) MỘT ca phản chứng cụ thể làm phương án khuyến nghị sai (đầu vào → kết quả sai);
(c) một tiêu chí kiểm được BẰNG MÁY (lệnh, phép so, hoặc luật trên dữ liệu), không phải lời khuyên chung.
Không tóm tắt câu hỏi, không lặp đề. Nếu thiếu dữ kiện để kết luận thì nói thiếu gì, đừng đoán.

BỐI CẢNH (giả định, kho phần mềm tổng quát):
- Một kho dùng CI có "concurrency group" theo NHÁNH với cancel-in-progress cho lượt push lên nhánh chính. Luật quy trình: một thay đổi
  chỉ được ghi "đã land" khi có gate CI XANH trên ĐÚNG commit merge, đủ bốn mốc: (1) run: lượt chạy của sự kiện push với head_sha = commit
  merge; (2) checkout: mỗi job checkout đúng SHA đó; (3) workflow definition: blob của tệp workflow đã chạy được neo bằng băm;
  (4) gate output: output test có dấu hiệu dương (vd "N/N" hai số bằng nhau), không chỉ mã thoát 0.
- Commit merge M (thay đổi A: 5 tệp, sửa luật loại tệp khỏi gói phát hành + test + manifest tái sinh). Lượt CI push trên M bị HUỶ sau
  9 giây, 0 job chạy, vì commit merge D được push 28 giây sau vào cùng nhánh. D = merge thay đổi B (4 tệp: sửa chính cấu hình
  concurrency của CI sang nhóm theo SHA + test của nó). M là tổ tiên của D. Lượt push trên D XANH đủ bốn mốc.
- Trước merge, head của thay đổi A có CI pull_request xanh 23/23 job và review sạch. Hiện trạng nhánh chính (nhiều commit sau D)
  đo lại vẫn đúng mục tiêu của A.
- Người giữ kho đã chọn tạm thời ghi A là "merged, landed=false".

Q1. Phương án X: dựng một nhánh tạm trỏ ĐÚNG M rồi gọi tay workflow_dispatch trên nó. Lượt ấy có thay được lượt push bị huỷ cho
    luật "gate trên đúng commit merge" không? Liệt kê những gì KHÁC nhau giữa lượt dispatch muộn và lượt push gốc (định nghĩa
    workflow đọc tại ref nào, phiên bản action/runner trôi theo thời gian, biến sự kiện, secrets...), và cái nào trong số đó làm
    bằng chứng yếu đi THẬT SỰ so với chỉ là khác hình thức.

Q2. Phương án Y: coi lượt xanh trên hậu duệ D là bằng chứng cho M ("phủ bằng hậu duệ"). Đưa điều kiện ĐỦ, kiểm được bằng máy, để
    phép phủ này hợp lệ. Đặc biệt: D sửa chính cấu hình CI và test — điều đó phá phép phủ ở đâu?

Q3. Giữa "để landed=false vĩnh viễn kèm ghi chú", X và Y: phương án nào tối ưu khi chi phí là phút CI + công người, và rủi ro là một
    lời khai land sai? Có phương án thứ tư rẻ hơn mà không yếu hơn không?

Q4. Thay đổi A đưa một thư mục mảnh changelog (mỗi packet một tệp markdown) RA KHỎI gói phát hành để tiết kiệm khe (gói có trần
    cứng số tệp). Hệ quả: changelog trong gói (một tệp CHANGELOG duy nhất, được băm trong manifest) không còn chứa nội dung các
    mảnh. So sánh ba cơ chế hợp nhất: (i) lúc land mỗi packet, (ii) lúc bump version/đóng gói, gộp mọi mảnh vào CHANGELOG rồi xoá
    mảnh, (iii) sinh CHANGELOG từ mảnh lúc build gói mà không commit. Cơ chế nào an toàn với manifest băm nội dung và với nhiều
    phiên song song cùng sửa CHANGELOG?

Q5. Một tài liệu NẰM TRONG gói có hai liên kết tương đối trỏ vào thư mục vừa bị loại khỏi gói. Bộ kiểm con trỏ hiện chỉ kiểm liên
    kết tới một thư mục con cụ thể nên không bắt được. Luật kiểm tối thiểu nào bắt được MỌI liên kết từ tệp trong gói tới tệp ngoài
    gói, mà không báo động giả với liên kết web hay neo trong cùng tệp?
