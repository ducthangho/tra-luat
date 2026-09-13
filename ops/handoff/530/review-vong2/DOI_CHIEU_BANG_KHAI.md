# Đối chiếu đủ24 hàng của BANG_KHAI vòng2

Nguồn định lượng: counts.json/spec-counts.json, các log gate và probe, history/ trích bằng git show từ gương. Các driver rc=0 là thực thi phép đo thành công; rc của ca con đỏ dự kiến ghi riêng. Không xem kiểm lại metadata do tác giả ghi là xác thực độc lập raw log không được cấp.

| # | Kết quả đo lại | Kết luận |
|---|---|---|
| 1 | +995/−61 đúng cho test; diff toàn cây so dc02c9b có3 tệp; so master d706abd chỉ1 tệp | Có lệch phạm vi đại lượng; xem NỢ mốc nền. Không vi phạm write set do hai tệp khác đến từ master |
| 2 | Lease exec-1r2 ghi S2=1000; 1000−995=5 | Đúng văn bản lease và diff, không gọi GitHub để xác thực comment cấp quyền |
| 3 | Lease ghi S6=10; trong hồ sơ đã hoàn tất một vòng1 trước lượt này | Phù hợp hồ sơ offline; số vòng đã đăng trên GitHub KHÔNG ĐO ĐƯỢC. Lượt bị giết không tự tính là vòng hoàn tất |
| 4 | Wrapper rc=0; CHA/A/B159/159, đã chạy159, bỏ qua0; đúng3 dòng;0 dòng đỏ kể cả prefixed | Đạt A5; count_claims.py có assertions kiểm các hậu điều |
| 5 | AST base155→HEAD159; wrapper có159 dòng ra cấp cha | Đúng; có thêm t161/t162/t163/t164 |
| 6 | t161 mẫu16, GIET16, KHONG_GIET0,KDD0; rc=0 | Đúng A4 trên tập catalogue được chạy |
| 7 | t16212/12,10 đóng băng+2bổ sung; rc=0 | Đúng; hai control mới có răng, gỡ riêng hành vi bị cấm làm11/12 rc=1 |
| 8 | t1637/7,6DO+1XANH; rc=0 | Số đầu ra đúng; không chứng minh7 phép đo đáng tin: bốn mục vẫn cấp tín dụng cho ngoại lệ vô can |
| 9 | t16413/13,rc=0 | Đúng số đầu vào/KDD; không đồng nghĩa mỗi chốt có răng |
| 10 | Bảng có3/4/2 phần tử | Đếm cấu trúc đúng, phân hạng “4 bị hấp thụ” sai với ít nhất2/4; còn các chốt khác chưa được bảng kiểm kê |
| 11 | Tái dựng biên trước t164 từ d5e7e7d bằng bỏ ca mới; gỡ riêng7 chốt, chạy t161+t162+t163 cho từng bản:21 lượt ca, mọi rc=0 | Đúng7/7 chưa được các ca ấy canh; log seven-before*. Không gọi đây là tái tạo nguyên môi trường lịch sử |
| 12 | Sáu nhánh if trong ma trận + phép thu hẹp vỏ: đúng3/7 làm t164 đỏ | Đúng số đo; suy luận4 còn lại không có đầu vào phân biệt bị bác |
| 13 | Log lịch sử TRƯỚC lưu7/7,10/10,16/16rc0. Hiện nới raw AssertionError và cấpGIET cho ca sống đều t16211/12rc1; đổi Exception không chọn lọc được logSAU ghi5/7rc1 | Bản sửa hẹp có tác dụng. Biến thể chọn lọcKDD hiện vẫn7/7rc0, lớp chưa đóng |
| 14 | Có4 mụcDO kỳ vọngKDD trong7 mục tổng, chỉ6 mục làDO | Tái dựng oracle luôn đòiGIET để kiểm4 mục đỏ; xem first-oracle.log. Bản nháp lịch sử không có source/log đầy đủ để xác thực chính lượt ấy |
| 15 | doctrine-scanrc0:7tệp/0chỗ; adr-songrc0:48ADR/48dòng | Đúng; output công bố ngoại lệ ADR0016 thiếu trạng thái |
| 16 | Verdict24341B, hash4505cdce… đúng; run.json ghi rc0,stderr677628B,1801.441s; trừ hai timestamp=1801.441344s | Kích thước/hash verdict kiểm từ bytes; thời lượng đúng mức làm tròn. Raw stderr không có nên677628B không xác thực độc lập được |
| 17 | Đếm heading v1:0P1/4P2/2P3/4NỢ; BO_SOT_SO v1 có39hàng | Đúng số lớp và số mục được ghi; không diễn giải39 thành tổng mọi đại lượng còn thiếu |
| 18 | CONTROL_512 có10, kỳ vọng8KDD+2GIET | Đúng, AST/module và t162 xác nhận |
| 19 | CONTROL_BO_SUNG_512 có2 | Đúng |
| 20 | _VUNG_CAT_512 có4 | Đúng; tên CHOT_CHUA_CO_CONTROL_512 mà prompt còn nêu đã không tồn tại |
| 21 | Log lịch sử104.4→319.4; t12553.039→160.378s. Đo lại hai clone riêng, giá trị thô cost/results.json | Chênh theo lượt được ghi ở NỢ thời lượng; không đảo quyết định chấp nhận chi phí. Delta214.9 không thể kiểm chính xác từ hai số tổng chỉ lưu1chữ số thập phân |
| 22 |18biểu thức sys.executable,5vị trí tự gọi suite/bản sao | Đúng số trong bảng. Comment còn gọi13biểu thức khác là lời gọi mã, có3vị trí thực ra dùng dựng/copyfixture |
| 23 |26mục:16neo khớp1lần,8khớp2,2khớp3; tính cả2control bổ sung là28mục:18/8/2 | Đúng cho mẫu26đã chỉ định; không cần sửa cận dưới hay mẫu số đóng băng |
| 24 | Gỡ xoá4biến + mutant selector:2attempts đều có3bản ghi ca(t01,t01,t155)+4đóng lượt; KDD“sau đóng lượt” | Đúng đường kênh đã đính chính; xem inherited-1.jsonl/inherited-2.jsonl. Không có157ca chạy trọn |

Hai câu ở7079/7176 mà lượt bị giết từng chỉ ra đã được sửa đúng tại HEAD: “chạy trọn cả hai bảng” và dẫn về numstat, không còn ghi dư26. Nhưng còn câu tương đương vật hoá và các con số động khác trong write set, đã ghi theo lớp.

Lượt cũ bị giết: thiếu transcript/raw log và ảnh chụp tiến trình của lượt ấy trong bundle;8.5phút,19:09Z và mtime19:08:56 là KHÔNG ĐO ĐƯỢC bởi reviewer này. Không dùng trạng thái run.json đang_chay làm bằng chứng process còn sống.
