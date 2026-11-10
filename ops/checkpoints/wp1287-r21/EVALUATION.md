# Đánh giá quy trình mới và hiện hành — WP1287

| Yêu cầu | Hiện hành | Quy trình áp dụng đợt này |
|---|---|---|
| Gom lỗi | Protocol8.3 đã yêu cầu lớp nguyên nhân/stable ID | Lập ledger biểu hiện; sửa chung bằng helper khi lỗi cắt ngang nhiều nơi |
| Vị trí lỗi | Anchors/evidence trong verdict | Finding mới bắt buộc file, start_line, end_line tại exact SHA; validator từ chối thiếu |
| Lượt sau | Đối chiếu mọi finding trước và quét lớp trên candidate | Discovery chỉ diff từ SHA vừa review; ngữ cảnh chỉ phục vụ hunk, lỗi cũ được kiểm bằng regression/trạng thái |
| Không báo trùng | Stable ID, lịch sử lớp | findings[] cấm ID/slug cũ; lỗi chưa vá vẫn ở previous_finding_status và vẫn chặn |
| Sau ba lần | Protocol12 đã có rescue checkpoint | Giữ trần, không reset khi đổi revision; xét lại thiết kế ngay khi test/review cho thấy chưa sửa được cơ chế |

Số đo phạm vi: r20 chỉ xét68 dòng thay đổi thay vì401 dòng toàn candidate; r21 chỉ xét17 thay vì410. Hai lượt cộng85 thay vì811 dòng thay đổi nếu đọc lại toàn candidate tương ứng (giảm89,52% theo phạm vi diff). Đây không phải số dòng model thực tế đã đọc, không phải tỷ lệ tiết kiệm token/thời gian. Ngữ cảnh và hướng dẫn vẫn chiếm đầu vào đáng kể.

Bằng chứng chất lượng: r20 không tạo ID/finding mới, vẫn giữ PREFLIGHT-001 ở VA_HO khi tìm thấy hash callback nuốt lỗi. Nghĩa là dedup không che lỗi cũ. Đã đổi hướng từ thêm Stop cục bộ sang helper tính/kiểm SHA256 trước export và dùng chung ở cả Capture/Cleanup. Bộ test mới32/32 trên PS5.1/7 bao gồm lỗi lần đọc thứ hai, digest null/sai, lệnh hash lỗi/mất, tệp bị khoá và bốn mutant khôi phục callback cũ. Manifest cũ được giữ khi lỗi. Test đầu thiếu biểu hiện Bash nested substitution; phép quét version-query đủ vị trí đã bắt rồi sửa,35/35. Các70 kiểm tra native cũ được dùng lại theo hash từng component không đổi, không giả là đã rerun.

Bộ test hash đầu có lỗi dựng double: PS5 autoload Utility thay double sau Select-Object, khiến phép tiêm lỗi lần đọc thứ hai không xảy ra. Đã giữ kết quả hỏng và sửa harness bằng import module trước double; không coi các ca đó là bằng chứng product xanh. Positive helper trong BOTH PS5.1/7 sau đó đã chạy thành công trong đúng Code Mode/read-only sandbox với module path từng engine; đây là bootstrap capability riêng, không thay negative matrix.

Hiệu quả đo được: review r20 đã tuân thủ không báo trùng, giữ cùng stable ID và tìm ra biểu hiện còn sót. Chưa có bằng chứng cho rằng tổng vòng vá ít hơn quy trình cũ: mẫu chỉ một Packet, r20 vẫn changes_requested, và chi phí lập ledger/test/receipt phát sinh ban đầu. Thời gian/token của các lượt có khác scope, snapshot layout và mức coverage; không dùng thời gian ngắn hơn của một lượt dừng sớm làm chứng minh nhanh hơn.

Khuyến nghị áp dụng: tiếp tục pattern+delta+regression+dedup; checklist pattern phải liệt kê cả dạng cú pháp/điểm gọi, không chỉ grep tên lệnh. Rủi ro delta-only là bỏ sót lỗi nền/cắt ngang; giữ full review ban đầu, đọc phụ thuộc cần thiết, regression cho lớp cũ và trần ba vòng. Các nghĩa vụ OP-F01/U10/assurance không bị xoá vì giảm scope. Đây là quy trình của đợt sửa theo chỉ thị chủ kho, chưa tự sửa protocol chung hoặc tạo release approval.

Kết quả r21: CLI trả approve cho H3..H4, findings[] rỗng. Reviewer độc lập xác minh helper hash mới trên PS5.1/7, thứ tự trường và các lỗi bắt buộc; PREFLIGHT-001 được DA_VA_THAT trong phạm vi biểu hiện hash còn lại. CONFIG-001 giữ giới hạn độc lập cũ; OP-F01/U10/assurance chưa đóng. Approval này chỉ cho delta, không là candidate/release/Mission approval.

Đối chiếu biên nhận cuối phát hiện transport Python write_text trên Windows đã đổi LF thành CRLF ở prompt/spec. Đã chứng minh byte khác biệt chỉ đúng phép đổi newline, source Git vẫn exact SHA/tree; giữ nguyên raw native files/verdict. Biên nhận chưa được nhận làm formal gate. Đã sửa writer triển vọng sang binary-write và thêm canonical-hash check trước model; bốn đối chứng (LF Unicode, CRLF drift, nội dung sai, ghi đè file đã đóng băng) đều đạt trên Linux và native Windows. Đây là lỗi vận hành được ghi thẳng vào đánh giá, không dùng chữ approve của CLI để xoá audit/gate còn thiếu.

Kết luận: áp dụng tiếp pattern+delta+regression+dedup và byte freeze trước review. Có bằng chứng giảm scope và ngăn báo trùng; chưa đủ bằng chứng giảm tổng chi phí/thời gian hoặc số vòng so với hiện hành. Source đã hội tụ ở delta cuối trong ba source-review cycles, dùng hết8/8 lời gọi; không gọi thêm. Việc merge/land vẫn chờ các nghĩa vụ nghiệm thu và assurance riêng.
