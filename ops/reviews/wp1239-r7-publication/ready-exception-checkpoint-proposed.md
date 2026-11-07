## Checkpoint đề xuất: điều kiện bỏ draft trên exact H7 — chưa được duyệt

Quyết định miễn F1/F2 đã hiệu lực tại6704067442; publication đã thực hiện theo chỉ thị chủ kho/6704099531. H7 public trên PR1261: **`4c319cc4f71b2f9a5c69a4b1be75e1add5f8aeaa`**, tree **`539a02f355c4ade3cee7c99efa327a4a729e79bb`**, S7 **`9607e3eba96b2ce091e34196cbb8ede31a521ff9`**. Hai tài liệu giữ nguyên bytes. Không xin duyệt lại F1/F2.

### Cổng còn thiếu để bỏ draft
ADR0060M6 yêu cầu connector review đúng commit trước bỏ draft. Probe canonical `_doc_connector` rc12, đủ trang ba endpoint PRreviews/reviewcomments/issuecomments, không có review của `chatgpt-codex-connector[bot]` trên H7. Đây là cổng tách biệt với F1/F2 về serving-family và receipt test. K4 validator cũng chỉ nhận modelverdictapprove/humanaudit đúng schema; nó chưa có đường tiêu thụ ngoại lệ owner_waived cho hai P1/P2, nên không thể khai machinegatepassed từ waiver.

Budget toàn PR đã3/3, không tự gọi connector như một lời gọi thứ4, không giả output/actor/KET_LUANapprove, không sửa checker hoặc state để mở khóa. Raw Codex review đã hoàn tất rc0 trên exactH7, contentN1–N4/R1–R4 đạt; verdictblocked chỉ hai finding đã được owner miễn. Independent runtime gpt-6.1-sol/xhigh/read-only và hash/snapshots đã xác minh.

### Ngoại lệ hẹp đề xuất để chủ kho quyết định
Chỉ cho PR1261 và exactH7/tree trên: không yêu cầu thêm connectorcall trước bỏ draft (ngoại lệ M6/K3); chấp nhận bộ reviewCLI đã hoàn tất + quyết định owner_waivedF1/F2 làm đường chấp nhận có chỉ thị chủ kho, thay việc đòi thêm literal modelapprove/humanaudit của K4 cho chính hai điểm đã miễn. Giữ rawverdictblocked, không khai cross_approved/human_audited hoặc machineK3/K4passed. Đây là acceptance exception do chủ kho quyết định, không phải sửa hai tài liệu hoặc policy chung.

Chỉ thực hiện bỏ draft nếu **tất cả GitHubLinuxCI/check bắt buộc và thu-hoi trên H7 đều success**, provenance/source/definition/tested binding đủ, remotehead vẫnH7/livecanonical vẫnS7/policy không đổi và không có finding mới ngoài hai finding đã miễn. CI đang chạy; không miễn CI, không gỡ protection, không dùng admin/bypass. Sau ready chỉ readback trạng thái; **không merge/land/deploy**, không auto-merge, không model/attempt/budget mới, không gọi phục hồi AGY. Ngoại lệ hết hiệu lực ngay khi H/tree/canonical thay đổi hoặc P0 kết thúc.

Đây là **PROPOSED**, chưa có quyền bỏ draft từ checkpoint này. Trong khi chờ, giữ draft và tiếp tục theo dõi CIrun42352790095. Chủ kho cũng có thể chọn giữ draft; không tự tăng modelbudget để lách điều kiện.
