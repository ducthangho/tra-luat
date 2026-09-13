# Đại lượng bị BANG_KHAI vòng 2 bỏ sót

Mỗi hàng là một thể hiện của `bang-khai-bo-sot-dai-luong`, kể cả số đúng. Phân biệt đại lượng/mốc đo, không chỉ tập chữ số. Không đếm issue ID, SHA, phiên bản công cụ, số thứ tự hay ngày giờ làm đại lượng. Không đếm lại số sai đã có lớp riêng. Đây là các mục đã tìm thấy, không phải lời hứa bảng mới đầy đủ.

Các phép đếm chạy bằng `python3 ket-qua/count_claims.py`, `python3 ket-qua/spec_counts.py` (rc=0); hành vi chạy bằng `probe.py`, log gate và các log được dẫn trong VERDICT. “Log lịch sử” nghĩa là đối chiếu hiện vật đã lưu, không đồng nghĩa tái chạy hay xác thực độc lập sự kiện lịch sử. Số thiếu raw evidence ghi KHÔNG ĐO ĐƯỢC.

| # | Đại lượng · nguồn | Đo lại / giới hạn |
|---|---|---|
| 1 | 59 lời gọi bang chuyển tín hiệu · M1/spec/commit | 59, so AST base→HEAD |
| 2 | 9 ca thuộc M1 · cùng nguồn | 9 ca đổi, không ca cũ nào khác đổi AST |
| 3 | t125 đổi 3 lời gọi · M1 | 3 |
| 4 | t153 đổi 5 lời gọi · M1 | 5 |
| 5 | t154 đổi 10 lời gọi · M1 | 10 |
| 6 | t155 đổi 4 lời gọi · M1 | 4 |
| 7 | t156 đổi 11 lời gọi · M1 | 11 |
| 8 | t157 đổi 6 lời gọi · M1 | 6 |
| 9 | t158 đổi 7 lời gọi · M1 | 7 |
| 10 | t159 đổi 4 lời gọi · M1 | 4; có thêm 1 chot đã có ở nền, không được tính là chuyển mới |
| 11 | t160 đổi 9 lời gọi · M1 | 9 |
| 12 | 0 bang còn lại trong chín ca · commit 540 | 0 |
| 13 | 4 biến môi trường kênh bị xoá · M2/commit | 4; bỏ xoá tái hiện 3 bản ghi ca +4 đóng lượt |
| 14 | Port có 4 nhãn kết quả · comment M2 | DAT/BO_QUA/DO_CHOT/DO_KHAC |
| 15 | Mẫu #513 có 3 nhãn · comment M2 | DAT/DO_CHOT/DO_KHAC, đối chiếu nguồn trong gương |
| 16 | 3 trạng thái phân hạng · M3 | GIET/KHONG_GIET/KHONG_DO_DUOC; cả ba có control hiện tại |
| 17 | Retry đúng 1 lần · M3 | 2 attempts với lỗi spawn; các lỗi chuẩn bị còn lọt, xem finding M3 |
| 18 | Hai ca con của A2 · commit a1 | t161+t162, t163 chạy thật cả hai |
| 19 | A2 chiều xuôi rc=[0,0] · commit a1/handoff | Đúng trên gate gốc |
| 20 | A2 chiều ngược rc=[1,1] · commit a1/handoff | Đúng trên a2-reverse.log |
| 21 | A2 chiều ngược 6/7 · commit a1/handoff | Đúng, t163 rc=1 |
| 22 | 8 dấu cách của neo except · commit/handoff | ExceptHandler main có col_offset=8 |
| 23 | 12 dấu cách của except t159 · cùng nguồn | col_offset=12 |
| 24 | +764 dòng ở 540b6f1 · commit | 764 |
| 25 | 137 chú thích ở 540b6f1 · commit | 137 |
| 26 | 67 dòng trống ở 540b6f1 · commit | 67 |
| 27 | ~87 docstring ở 540b6f1 · commit | 89 theo AST; đồng thời thuộc lớp phân rã lịch sử |
| 28 | ~470 mã ở 540b6f1 · commit | 471; cùng lớp phân rã |
| 29 | +802 dòng ở a1c7d7f · commit/handoff | 802 |
| 30 | 148 chú thích ở a1c7d7f · commit/handoff | 148 |
| 31 | 67 dòng trống ở a1c7d7f · commit/handoff | 67 |
| 32 | ~90 docstring ở a1c7d7f · commit/handoff | 89; cùng lớp phân rã |
| 33 | ~497 mã ở a1c7d7f · commit/handoff | 498; cùng lớp phân rã |
| 34 | Suite commit đầu 3m32s · commit 540 | 212s khai; KHÔNG ĐO ĐƯỢC lượt lịch sử vì thiếu log gắn đúng lượt |
| 35 | t161 commit đầu 49.4s · commit 540 | Lượt log riêng lưu 49.372s, làm tròn49.4; không chứng minh là cùng lượt commit nói tới |
| 36 | t162 commit đầu 2.2s · commit 540 | KHÔNG ĐO ĐƯỢC lượt đó; log lỗi lượt đầu1.947s là lượt khác |
| 37 | t163 commit đầu 2.0s · commit 540 | KHÔNG ĐO ĐƯỢC lượt đó; không lấy t163 sau A2 ~53s thay thế |
| 38 | t125 commit đầu107.4s tuyệt đối · commit540 | KHÔNG ĐO ĐƯỢC lượt đó; khác đại lượng delta+107.4 ở BANG_KHAI#21 |
| 39 | t163 ở a1c7d7f53.6s · commit a1 | Log riêng53.516, wrapper53.670; khác lượt, không thể xác thực đúng53.6 |
| 40 | t125 nền53.0s · handoff chi phí | Log gốc53.039s, làm tròn53.0 |
| 41 | t125 sau160.4s · cùng nguồn | Log gốc160.378s, làm tròn160.4 |
| 42 | Trần sensitive3 tệp · ADR0044/commit/handoff | Văn bản quy định≤3; không đổi sang trần số đường của packet |
| 43 | Tiền lệ #504 S2=1500 · commit/handoff | Lease windows-lease-suite-exec-2-claude-20260912.yaml ghi tran_moi1500 |
| 44 | Dư198 dòng lúc cấp r2 · lease | 1000−802=198; kiểm riêng802 bằng diff |
| 45 | Script chi phí hỏng còn1 dòng log · handoff | KHÔNG ĐO ĐƯỢC lần lỗi; chỉ có bản script đã sửa và lời khai |
| 46 | Script chi phí hỏng báo0 ca · handoff | KHÔNG ĐO ĐƯỢC cùng lượt lỗi |
| 47 | 0 tệp canh trần vòng · handoff | Không có biến/khối đọc review_rounds_limit trong packet_loop/lease_publish; đây là kiểm mã tĩnh, không khẳng định mọi hệ thống ngoài kho |
| 48 | Lượt đầu A1 có2/10 lỗi neo · commit/handoff | Log lưu đúng2 LỆCH ở hai control dương |
| 49 | Lượt đầu A1 đạt8/10 · cùng nguồn | Log lưu8/10, suite0/1; raw process rc của lượt ấy không lưu riêng |
| 50 | Tự kiểm trước ghim cột5/6 · commit/handoff | KHÔNG ĐO ĐƯỢC lượt lịch sử; đếm chuỗi không chứng minh kết quả5/6 |
| 51 | Tự kiểm sau ghim cột6/6 · cùng nguồn | Sáu mục DO hiện đều làm control lệch; không xác thực lượt lịch sử không có log |
| 52 | Catalogue mất tín dụng còn15 GIET khi thừa kế kênh · commit | 16 gốc; riêng selector trở thành KDD, các mutant khác không đổi source; đã đo kênh selector hai lần |
| 53 | Catalogue có1 KDD khi thừa kế kênh · cùng nguồn | Đã đo riêng selectorKDD; không lẫn với số bản ghi4 đóng lượt |
| 54 | Tổng412 ref · prompt | 412 |
| 55 | 8 heads · prompt | 8 |
| 56 | 365 remotes · prompt | 365; không xác minh bằng tập remote live độc lập |
| 57 | 39 tags · prompt | 39 |
| 58 | Mẫu493 bang/chot · spec | 493 trên blob thật, OID sai đã ghi riêng |
| 59 | 454 tiền tố tĩnh · spec | 454 |
| 60 | 39 lời gọi không đọc được tiền tố tĩnh · spec | 39 |
| 61 | 8 lời gọi tĩnh va chạm · spec | 8 |
| 62 | 4 ca tĩnh va chạm · spec | 4 |
| 63 | t96 có4 thông điệp va chạm · spec | 4 |
| 64 | 21 tiền tố động dạng va chạm · spec | 21, đây là hình dạng AST; không khẳng định mọi giá trị runtime |
| 65 | 7 ca thuộc nhóm động · spec | 7 |
| 66 | ≥29 lời gọi thuộc hai nhóm · spec | 8+21=29; hai nhóm đã đếm riêng |
| 67 | ≥10 ca trong hợp hai nhóm · spec | 4+7−1=10; t133 giao hai nhóm |

Bốn hàng27/28/32/33 xuất hiện ở lớp số sai **và** ở đây vì đại lượng đồng thời bị bảng bỏ sót. Không cộng thành hai lớp hoặc hai lần lỗi số. Các con số60/6,13 biểu thức còn lại,2175 master và1 tệp so base đã được ghi ở lớp riêng, không tính vào67 hàng này.

Nguyên văn thân PR và các comment 5647635305/5648007043 không có snapshot đầy đủ trong bundle. Mọi lời khai chỉ tồn tại ở những nguồn ấy: KHÔNG ĐO ĐƯỢC offline. Các con số8.5 phút,19:09Z và mtime19:08:56 của lượt chết trước cũng không có raw log/process snapshot tương ứng để reviewer này đo lại.
