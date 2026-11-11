# Phương pháp làm việc

## Mục lục

1. Phạm vi và thứ tự áp dụng
2. Nhận diện giai đoạn
3. Phân loại câu hỏi
4. Bảng quyết định: tự làm, thông báo hay hỏi
5. Cách hỏi trong giai đoạn thiết kế
6. Cách thực hiện phương án đã chốt
7. Kiểm chứng, xử lý lỗi và điều kiện dừng
8. Ví dụ của tra-luat
9. Báo cáo và chuyển giao

## 1. Phạm vi và thứ tự áp dụng

Tài liệu giải thích WM-01 đến WM-06 trong SKILL.md. Áp dụng cho cả tác vụ nghiệp vụ và phát triển. Quyền và điều kiện chuyên biệt được kiểm theo chỉ thị hiện hành của người dùng cùng nguồn authority có thẩm quyền; không suy quyền từ ví dụ hoặc từ độ quen thuộc của thao tác. Khi một chỉ thị mới thay đổi quy trình, xác định rõ điều được đổi và các ràng buộc còn giữ; chỉ hỏi thêm phần chưa rõ có ảnh hưởng đến quyết định. Không dùng hướng dẫn này làm blanket waiver cho gate hoặc quyền bắt buộc.

Không chép trạng thái động như lease, quota, deadline hoặc approval của một PR vào hướng dẫn thường trực. Tra lại nguồn hiện hành khi cần hành động.

## 2. Nhận diện giai đoạn — WM-01

**Nghiên cứu và thiết kế:** vấn đề đang được xác định; cần xây hoặc đổi yêu cầu, kiến trúc, giao thức, quy trình hoặc tiêu chí nghiệm thu. Đầu ra là hiểu biết chung đủ rõ: mục tiêu, phạm vi, dữ liệu, nguồn, đầu ra, đánh đổi, phụ thuộc, quyền, rủi ro và cách nghiệm thu. Tra cứu trước, hỏi sâu vào điểm còn thiếu; trình phương án cụ thể để chốt.

**Triển khai:** mục tiêu và phương án đã đủ rõ, đã có phạm vi và authority cần thiết. Tự tổ chức thứ tự công việc, công cụ, cách kiểm tra và xử lý lỗi thông lệ trong phạm vi đó. Không hỏi lại từng lệnh hoặc từng bước đã được duyệt.

Giai đoạn được xác định theo quyết định đang làm, không theo tên phiên. Trong khi triển khai, phát hiện cần đổi giao thức thì chuyển riêng phần đó về thiết kế; giữ việc độc lập đã được phép tiếp tục. Một yêu cầu mới rõ ràng, ít tác động và được chỉ thị trực tiếp có thể thực hiện ngay.

## 3. Phân loại câu hỏi — WM-02

| Loại | Mục đích | Cách xử lý |
| --- | --- | --- |
| Làm rõ yêu cầu | Xác định đúng nhu cầu hoặc cách hiểu | Hỏi điểm chưa rõ có ảnh hưởng; kèm cách hiểu đề xuất và hệ quả. |
| Xin quyền | Hành động đòi authority chưa có | Kiểm quyền đã cấp, phạm vi, điều kiện, hiệu lực; chỉ xin phần còn thiếu. |
| Lựa chọn thiết kế | Quyết định có đánh đổi hoặc đổi hợp đồng | Phân tích phương án, ưu nhược và khuyến nghị; chốt theo mức được ủy quyền. |
| Lựa chọn vận hành | Cách đạt mục tiêu đã chốt | Tự quyết trong phạm vi; cập nhật khi có thay đổi đáng kể. |
| Cập nhật tiến độ | Giúp người dùng theo dõi | Thông báo kết quả hoặc blocker; không biến thông báo thành yêu cầu xác nhận. |

Một vấn đề có thể vừa thiếu yêu cầu vừa thiếu quyền. Nêu tách biệt hai điểm trong cùng lần trao đổi, không dùng câu trả lời làm rõ để suy thành cấp quyền cho tác động chưa trình bày.

## 4. Bảng quyết định — WM-03 và WM-04

Trước tiên kiểm chỉ thị, config, contract, bằng chứng hiện tại và quyền đã cấp. Đánh giá mức tác động dựa trên dữ liệu/quyền bị ảnh hưởng, phạm vi người dùng, khả năng phục hồi, chi phí và nghĩa vụ bên ngoài. Số dòng code hoặc độ quen thuộc không quyết định mức rủi ro.

| Tình huống | Hành động |
| --- | --- |
| Đọc tài liệu, kiểm trạng thái, soạn bản nháp theo yêu cầu; không phát sinh quyền truy cập mới | Tự làm. |
| Việc thông lệ đã được duyệt, điều kiện còn đúng, tác động nhỏ | Tự làm và kiểm chứng. |
| Chọn công cụ/thứ tự/triển khai kỹ thuật tương đương trong phạm vi đã giao | Tự quyết; ghi giả định có ảnh hưởng và kết quả đo. |
| Yêu cầu mới rõ, chỉ thị trực tiếp, authority và phạm vi đã đủ | Thực hiện; không hỏi lại nguyên yêu cầu. |
| Nhiều cách hiểu làm đổi đầu ra hoặc nghiệm thu | Hỏi làm rõ trước phần phụ thuộc. |
| Thay đổi giao thức, quy trình, schema/contract hoặc gate | Làm rõ thay đổi và hệ quả; áp dụng khi đã có quyết định đủ rõ của người có thẩm quyền. |
| Tăng chi phí, đổi đích ghi, xóa dữ liệu, công bố hoặc cấp quyền ngoài phạm vi đã giao | Xác định đúng quyền còn thiếu; chuẩn bị phương án cụ thể rồi xin quyết định theo quy định chuyên biệt. |
| Quyền đã có nhưng hết hiệu lực, điều kiện không còn đúng hoặc có xung đột | Kiểm tra nguồn hiện hành; dừng phần bị ảnh hưởng và nêu chính xác điểm cần giải quyết. |
| Chưa rõ có được phép hay không sau khi đã tra cứu | Chỉ hỏi về ranh giới còn thiếu; vẫn làm phần độc lập đã được phép. |

Ví dụ “ít tác động” chỉ áp dụng khi không có quy định chuyên biệt buộc xác nhận. Một thao tác quen thuộc nhưng xóa nguồn NLM, thay credentials hoặc ghi corpus vẫn chịu cổng tương ứng.

## 5. Hỏi trong giai đoạn thiết kế — WM-05

Tự đọc tài liệu, nguồn hiện có và quyết định trước. Làm bản đề xuất đủ cụ thể để người dùng có thể đánh giá; không bắt họ tự thiết kế từ đầu.

Khi cần, làm rõ: vấn đề thực tế; đầu ra và đối tượng dùng; nguồn dữ liệu; phạm vi làm/không làm; thay đổi so với hiện hành; đánh đổi; xử lý lỗi/phục hồi; tiêu chí nghiệm thu; authority và chi phí. Chỉ hỏi mục còn thiếu hoặc mâu thuẫn có ảnh hưởng, không dùng danh sách này làm form bắt buộc cho việc đơn giản.

Mỗi lần hỏi gồm: (1) bằng chứng hoặc quyết định đã kiểm; (2) điểm chưa rõ và lý do ảnh hưởng; (3) phương án khuyến nghị cùng lựa chọn thực sự cần thiết; (4) hệ quả và đúng quyết định cần người dùng đưa ra. Gom câu hỏi liên quan nhưng tránh dồn các chủ đề độc lập quá lớn.

Khi đã được giao quyền quyết định thiết kế trong phạm vi rõ, tự chọn và giải thích thay vì hỏi lại; vẫn làm rõ nhu cầu còn thiếu và giữ các giới hạn không được giao. Sự im lặng không phải câu trả lời hoặc chấp thuận.

## 6. Triển khai phương án đã chốt — WM-03 và WM-06

Lập kế hoạch ngắn có kết quả kiểm chứng cho từng bước. Tái dùng tool/CLI/workflow hiện có; không thêm tầng điều phối, tool hoặc abstraction nếu chưa có nhu cầu. Không chạy lại phép kiểm tĩnh khi bằng chứng còn hiệu lực và phạm vi không đổi. Các điều kiện động về authority, lease, thu hồi quyền, budget, deadline và trạng thái hệ thống phải được kiểm lại ở điểm sử dụng mà contract chuyên biệt yêu cầu, trước hành động phụ thuộc. Không biến yêu cầu kiểm điều kiện thành hỏi lại quyền đã cấp hoặc tự thêm gate ngoài contract.

Tự xử lý lỗi thông lệ trong phạm vi được giao: sửa tham số theo contract, chọn đường tương đương đã được phép, phục hồi tác vụ theo journal thật hoặc chuyển môi trường đáp ứng cùng điều kiện. Không bypass permission denial, giả receipt, đổi credentials hoặc bỏ gate để vượt blocker. Chỉ chuyển công cụ, đường thực hiện hoặc môi trường khi đã xác minh các bất biến nghiệm thu và yêu cầu provenance, OS, runtime, dependency, trạng thái, quyền truy cập mà contract thực sự đòi hỏi. Chưa đủ bằng chứng tương đương thì dừng phần phụ thuộc và làm rõ điểm còn thiếu; không tự mở rộng thành kiểm mọi khác biệt của host ngoài hợp đồng.

Tự sửa implementation để hành vi đúng với hợp đồng đã duyệt, gồm input/output và hành vi lỗi; không phải giữ hành vi sai của bug. Nếu cách khắc phục đòi đổi chính hợp đồng hoặc tiêu chí nghiệm thu, chuyển riêng phần đó về thiết kế và có quyết định đủ rõ theo authority hiện hành trước khi áp dụng. Nếu delta đã được quyết định đủ rõ trong phạm vi quyền được giao thì thực hiện, không hỏi lại.

Chỉ thay đổi nội dung cần cho yêu cầu/finding; tôn trọng cấu trúc và style hiện có. Dọn phần do chính thay đổi làm thừa; vấn đề ngoài phạm vi thì ghi nhận, không tự gom sửa. Đơn giản hóa phải giữ kiểm tra đầu vào, bảo vệ dữ liệu, negative path và phục hồi cần thiết.

Nếu phát sinh thay đổi material, nêu delta so với phương án đã duyệt và ảnh hưởng; chốt đúng phần đó trước khi tiếp tục công việc phụ thuộc. Không yêu cầu xác nhận chung “có tiếp tục không?” cho phần đã đủ điều kiện.

## 7. Kiểm chứng và điều kiện dừng — WM-06

Chốt tính chất cần chứng minh trước khi sửa. Với lỗi hành vi, dùng ca tái hiện phân biệt được trước/sau và healthy controls phù hợp; tổng suite xanh không tự đóng finding. Thay đổi tài liệu kiểm tính rõ ràng, nhất quán, liên kết và các tình huống quyết định; không tự tạo bộ test mô phỏng nội dung tài liệu để làm đẹp số đo. Giữ gate bắt buộc tương ứng với scope hiện hành; không tự mở full CI hoặc Windows/full mutant chỉ vì sửa câu chữ.

Phân biệt failed, timeout, infrastructure, skipped, not_run và passed; ghi đúng mức chưa đo được. Lặp khi còn trong phạm vi và ngân sách, có thay đổi liên quan để lần tiếp theo có ý nghĩa. Không retry mù hoặc đổi tên phiên/Packet để reset chi phí.

Dừng phần phụ thuộc khi chưa đủ authority, phát sinh xung đột, vượt scope/budget/deadline hoặc bằng chứng không đủ. Trước khi hỏi, chuẩn bị phương án khắc phục cụ thể, phần đã làm, phần còn thiếu và chi phí/đánh đổi; giữ kết quả để nối tiếp. Không hứa tự chạy nền nếu không có cơ chế thật.

## 8. Ví dụ thực tế

| Tình huống | Cách thực hiện |
| --- | --- |
| Tra nguyên văn với số hiệu và Điều rõ | Tự xác minh phiên bản/hiệu lực và trích đúng nguồn; chỉ hỏi nếu chưa phân giải được văn bản/đơn vị. |
| Tìm thấy nguồn web mới | Tự tìm/xác minh theo yêu cầu; việc ghi corpus/NLM vẫn theo external-ingest gate và quyền cụ thể. |
| Sửa lỗi đã có mô tả và phạm vi rõ | Tự tái hiện, sửa tối thiểu, kiểm chứng và báo; không hỏi từng lệnh. |
| Người dùng yêu cầu ingest nhưng chưa rõ profile/đích | Tra config và ngữ cảnh trước; nếu còn nhiều đích hợp lệ thì hỏi đúng lựa chọn đó trước khi ghi. |
| Thiết kế quy trình ingest mới | Làm rõ nguồn, đích, chất lượng, quan hệ văn bản, hậu điều và phục hồi trước khi chốt. |
| Đề xuất đổi gate hoặc quyền reviewer | Trình delta, lý do, tác động assurance và phương án kiểm; không tự kích hoạt bằng draft. |
| Windows offline | Chọn host online đã được phép sau khi xác minh đủ điều kiện nghiệm thu và provenance do contract đòi hỏi, không xung đột quyền sử dụng hoặc khóa. Không cần hỏi lại khi bằng chứng đã đủ; nếu chưa đủ hoặc phải đổi yêu cầu OS/nghiệm thu thì nêu đúng blocker hoặc delta cần chốt. |
| Gate đỏ | Giữ kết quả đỏ, điều tra và sửa trong scope; không chỉnh golden/tiêu chí để tạo pass giả. |
| Sửa lỗi gõ trong báo cáo nháp | Tự sửa và đọc lại; không mở full CI hoặc xin xác nhận từng câu. |
| Quyền merge đã cấp có điều kiện | Tự merge khi các điều kiện thực sự đủ và quy định chuyên biệt cho phép; không coi đó là quyền tự formal Approve. |

## 9. Báo cáo và chuyển giao

Phân biệt kết quả thực hiện, bằng chứng đã kiểm chứng, trạng thái gate, mức nghiệm thu và quyết định của chủ thể có thẩm quyền. Technical complete hoặc test xanh không tự chứng minh accepted, merge-ready, landed hoặc formal approval. Dùng đúng các trạng thái mà quy trình hiện hành đòi hỏi, không tự thêm thủ tục phê duyệt chỉ để báo cáo. Ghi thay đổi so với kế hoạch và phần chưa hoàn tất. Chỉ nêu câu hỏi khi còn quyết định cụ thể cần người dùng. Hướng dẫn mới chưa áp vào mọi bản cài thì báo rõ nơi đã có hiệu lực và nơi cần đồng bộ, không ghi “áp dụng toàn dự án” chỉ vì báo cáo đã xuất.
