# Kiểm kê các đại lượng BANG_KHAI chưa tách thành mục đo

Mỗi dòng là một thể hiện của lớp `bang-khai-bo-sot-dai-luong`, kể cả khi số ấy đúng. Không đếm số hiệu issue/commit, ngày giờ hay số thứ tự mục thành số đo. Hai phép đo khác mốc có thể dùng cùng một giá trị; không vì trùng giá trị mà gộp đại lượng. Các số vốn đã là thành phần của một hàng BANG_KHAI không được tính lại.

| # | Đại lượng bị bỏ sót · nơi khai | Kết quả/giới hạn phép đo |
|---|---|---|
| 1 | 4 biến môi trường được xóa · commit 540, `_mo_kenh` | 4; `count_extra.py`, và phép bỏ xóa làm catalogue 15/1 |
| 2 | 3 vùng cắt · commit 540/handoff | 3; `count_extra.py` |
| 3 | cận dưới 2 lần cho **mọi** neo · commit 540 | Sai với 16/26 mục; `count_extra.py` |
| 4 | neo except có 8 dấu cách · commit 540/handoff | 8; AST ExceptHandler có `as ex` |
| 5 | except trong t159 có 12 dấu cách · cùng nguồn | 12; cùng phép đếm |
| 6 | +764 dòng ở commit đầu · commit 540 | 764; `count_claims.py` |
| 7 | 137 dòng chú thích ở commit đầu · commit 540 | 137; cùng phép đếm |
| 8 | ~87 dòng docstring ở commit đầu · commit 540 | 89 theo AST; đã ghi chênh lệch có ký hiệu xấp xỉ |
| 9 | ~470 dòng mã ở commit đầu · commit 540 | 471 theo cùng quy tắc |
| 10 | suite commit đầu 3m32s (212s) · commit 540 | KHÔNG ĐO ĐƯỢC lần lịch sử: không có log suite lần đó trong bundle; không lấy wrapper HEAD thay vào |
| 11 | t163 commit đầu 2.0s · commit 540 | KHÔNG ĐO ĐƯỢC thời lượng lịch sử; không gộp với t163 HEAD 53.7s |
| 12 | t125 commit đầu lên 107.4s tuyệt đối · commit 540 | KHÔNG ĐO ĐƯỢC thời lượng lịch sử; **khác** delta +107.4s tại hàng 19 BANG_KHAI |
| 13 | trần 3 tệp cho sensitive · commit 540/handoff | ADR-0044 dòng 5 có ≤3; diff thật có 1 |
| 14 | tiền lệ S2=1500 cho #504 · commit 540/handoff | lease gen 2 nhánh `ops/cap-lease-504` thật ghi tran_moi=1500; chỉ xác minh văn bản offline |
| 15 | 8 control âm · commit 540, t162 | 8 KDD; `count_extra.py`, t162 chạy đủ |
| 16 | 2 control dương · t162/CONTROL_512 | 2 GIET; cùng phép đo |
| 17 | retry đúng 1 lần (2 attempts) · commit 540/M3 | control Exception thật: attempts=[1,2], KDD; `logs/retry-count.json` |
| 18 | 3 trạng thái phân hạng · commit 540/M3 | 3 hằng GIET/KHONG_GIET/KDD; bộ control hiện chỉ đòi 2 trạng thái, xem finding coverage |
| 19 | 2 dòng tổng kết làm bằng chứng dương cho A2 · commit a1 | có t161 và t162; log t163 và mã nhánh XANH; đây khác 3 dòng A5 |
| 20 | chiều ngược A2 đạt 6/7 · commit a1 | tái lập đúng 6/7, t163 rc=1; BANG_KHAI #10 chỉ ghi rc và tên cực sai |
| 21 | chiều xuôi A2 rc=[0,0] · commit a1/handoff | tái lập đúng trong t163; #10 của bảng chỉ giữ chiều ngược [1,1] |
| 22 | t163 53.6s ở phép đo commit a1 · commit a1 | nguồn khai 53.6; log wrapper sau ghi 53.670 (~53.7), lần gate review 53.788; không coi chênh thời gian là regression |
| 23 | script delta hỏng chỉ còn 1 dòng log · handoff/prompt | KHÔNG ĐO ĐƯỢC log bản hỏng từ bundle; chỉ có lời khai và script đã sửa |
| 24 | script delta hỏng in số ca 0 · handoff | KHÔNG ĐO ĐƯỢC lần lịch sử vì cùng giới hạn |
| 25 | tổng 412 ref trong gương · prompt | 412, `count_claims.py` |
| 26 | 8 local heads · prompt | 8, cùng phép đếm |
| 27 | 39 tags · prompt | 39, cùng phép đếm |
| 28 | master có 2175 commit · prompt | 2175, rev-list --count; không shallow |
| 29 | 18 vị trí gọi chính tệp · comment `_mo_kenh` / prompt | 18 biểu thức AST nhưng 5 mảng lệnh tự gọi; xem finding đơn vị đếm |
| 30 | nhãn kết quả: bản port 4, mẫu 3 · comment M2 | port có DAT/BO_QUA/DO_CHOT/DO_KHAC; mẫu có DAT/DO_CHOT/DO_KHAC; khác số trạng thái phân hạng |
| 31 | 454 lời gọi tiền tố tĩnh · spec rev 3 | 454; `spec_counts.py` trên blob thật của 36f68c7 |
| 32 | 8 lời gọi tiền tố tĩnh va chạm · spec rev 3 | 8; cùng phép đo |
| 33 | 4 ca có tiền tố tĩnh va chạm · spec rev 3 | t96/t133/t136/t151; cùng phép đo |
| 34 | t96 có 4 thông điệp va chạm · spec rev 3 | 4; cùng phép đo |
| 35 | 39 lời gọi không đọc được tiền tố tĩnh · spec rev 3 | 39; 34 f-string bắt đầu bằng biểu thức và 5 biểu thức thông điệp khác |
| 36 | 21 tiền tố động có hình dạng va chạm · spec rev 3 | 21; cùng phép đo |
| 37 | 7 ca trong nhóm tiền tố động · spec rev 3 | 7 tên trong `logs/spec-counts.log`; t133 trùng nhóm tĩnh |
| 38 | cận dưới 29 lời gọi va chạm · spec rev 3 | 8+21=29; **không** khẳng định mọi giá trị runtime của 21 biểu thức đều va chạm |
| 39 | cận dưới 10 ca trong hợp hai nhóm · spec rev 3 | 4+7−1=10; cùng giới hạn runtime |

Các số 157 ca, 2 vùng cắt và các lời khai tương đương đã được ghi vào lớp chuyên biệt trong VERDICT, không cộng lại vào bảng này. Giá trị 365 remotes đã có ở BANG_KHAI #24 nên không tính là bỏ sót. Tương tự không tính lại 59 phép đổi/0 bang còn lại hay các số hạng t125…t160 của #1.

Lệnh đã chạy: `python3 ket-qua/count_extra.py`, `python3 ket-qua/count_claims.py`, `python3 ket-qua/spec_counts.py` (đều rc=0); đọc hai commit bằng `git show -s --format=%B`; đọc handoff/lease bằng `git show ref:path`. Lệnh t162/t163 và các log nằm trong VERDICT. Phạm vi lịch sử KHÔNG ĐO ĐƯỢC được giữ nguyên, không biến thành “không có vấn đề”.

Thân PR #532 và nguyên văn comment #530/5647445521 không có bản snapshot trong các hiện vật packet đã cấp. Không truy cập mạng theo chỉ thị: độ đầy đủ của lời khai chỉ xuất hiện trong hai nguồn đó là **KHÔNG ĐO ĐƯỢC**. 39 là số thể hiện đã tìm thấy và ghi được nguồn, không phải lời hứa đã tìm hết mọi số.
