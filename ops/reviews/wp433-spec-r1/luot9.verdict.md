## Issue #433 · Review độc lập lượt 9

### Finding lượt 8

| Mức | Packet | Finding | Trạng thái |
|---|---|---|---|
| P2 | 1 | `db_w6_bo_kiem_dict` chết bằng `AttributeError` ngoài tập khai | **Đóng.** §4b #11 khai đúng ca `chung_du_lieu_sai_dang` và nhãn `config_khong_dict`. Phép đo với `[]`, `null` và `"s"` đều cho `AttributeError` chứa `object has no attribute 'update'`. |
| P2 | 1 và 2 | Các đột biến `oserror` làm lan ngoại lệ chưa khai | **Đóng.** Packet 1 #26 và packet 2 #20–21 khai đúng `OSError("wp433-oserror")` ở biên các lời gọi tương ứng. Packet 1 #27 giữ cơ chế H vì đột biến vẫn bắt lỗi và đổi hành vi trả về. |
| P3 | 2 | `db_bo_reparse` thiếu đích `reparse_w1` | **Đóng về khai báo.** N3c và §4b #13 đã thêm đích W1. Việc fixture có đi tới tiền tố gắn bit hay không vẫn cần sửa như finding dưới đây. |

### Finding mới

- **P2 · Packet 1 · §4b #8–10 chưa định danh đủ biên bắt ngoại lệ.** Cả ba mục khai cùng ca, cùng `UnicodeEncodeError` và cùng dấu `surrogates not allowed`, nhưng yêu cầu ba nhãn khác nhau. Tôi chạy ba phép thử trong RAM và xác nhận cả ba cùng khớp điều kiện đã khai. Tra theo tập của cả ca sẽ không xác định được nhãn nào thuộc lời gọi đang chạy. Gắn tập khai vào từng lượt gọi N3(3), N3(4), N3(5) và kiểm đỏ khi ngoại lệ khớp kiểu, thông điệp nhưng phát sinh ở lượt khác. [Packet 1 §4b](ops/specs/NLM-GWS-DICH-NGOAI-KHO-r1.md#4b-bảng-đột-biến--nguồn-duy-nhất-thắng-mọi-mô-tả-đột-biến-rải-trong-4)
- **P2 · Packet 1 · N1/N8 chưa chứng minh W3 áp chốt đích ghi.** `db_w3_bo_chot` bỏ cả kiểm jar lẫn kiểm đích, còn fixture đích dùng khóa `../thoat.json`. Nếu W3 chỉ bỏ `_kiem_dich_ghi` và vẫn giữ `_kiem_jar_nlm`, N1 vẫn từ chối đúng khóa và N8(3) vẫn kiểm được thứ tự trước chống hạ cấp. Phản chứng trong RAM xác nhận hai phiên bản cho cùng kết quả với khóa lạ và chỉ khác nhau khi khóa hợp lệ đi tới đích bị chặn. Cần một ca W3 có jar hợp lệ, đích bị chặn và đột biến chỉ bỏ chốt đích. [Packet 1 N1/N8](ops/specs/NLM-GWS-DICH-NGOAI-KHO-r1.md#4-nghiem_thu)
- **P2 · Packet 2 · `reparse_w1` chưa buộc W1 đi qua tiền tố gắn bit.** N3c giả lập `lstat` cho `profiles/default` nhưng chưa khai jar W1 chứa khóa nào. Phép dựng tiền tố theo M1 xác nhận jar hợp lệ chỉ có `auth.json` bỏ qua tiền tố ấy, còn `profiles/default/cookies.json` đi qua. Chốt khóa lồng trong fixture và yêu cầu §4b #13 chết ở cả `reparse` lẫn `reparse_w1`, cộng thêm `junction` trên Windows. [Packet 2 N3c](ops/specs/GWS-CRED-DICH-NGOAI-KHO-r1.md#4-nghiem_thu)
- **P3 · Packet 1 · §4b #7 cần fixture `list` khác rỗng.** N3(1) chỉ ghi kiểu `list`. Với `[]`, các nhánh giữ nguyên của W1 và W2 dừng trước `_kiem_jar_nlm`, nên không có `AttributeError` do `.items()` như dòng E khai. Với `[1]`, phép thử cho đúng loại và thông điệp. [Packet 1 N3](ops/specs/NLM-GWS-DICH-NGOAI-KHO-r1.md#4-nghiem_thu)
- **P3 · Packet 2 · M1 ghi sai kết quả `isabs` trên nền hỗ trợ.** `ntpath.isabs("\\fake")` trả `True` trên Python 3.11.18 và 3.12.3, `False` trên 3.13.18. Cả ba trả ổ rỗng từ `splitdrive`. N2w yêu cầu từ chối đúng. M1 cần nói rõ kiểm tra dạng **có gốc, thiếu ổ** trước nhánh chấp nhận theo `isabs`. [Packet 2 M1/N2w](ops/specs/GWS-CRED-DICH-NGOAI-KHO-r1.md#3-muc_tieu)

### Phạm vi và bằng chứng

- **§4b và L1–L7.** Đã rà từng mục trên giấy. Packet 1 có 32 đột biến, 8 E và 24 H. Packet 2 có 24 đột biến, 4 E và 20 H. Dòng 13b là đích native bổ sung của #13. `python3 -IB` trả rc 0 cho phép đối chiếu số đếm và các phép thử nguyên tố của 12 mục E trên Linux 3.13.18. Các finding chỉ ra lỗi L3/L5 ở biên ca, độ phủ hoặc nền đo. Không phát hiện thêm lỗi mức P0–P3 ở L1, L2, L4, L6, L7. Số đếm tiền nhiệm ở L4 vẫn được khai chưa đo được. Phép chạy fragment, bảng đột biến trên candidate và junction native đều `not_run`.
- **Chuyển phạm vi.** Packet 1 nhất quán giữa §2, §3 và §8 về `S_ISLNK` và giới hạn junction. Packet 2 M6 chỉ thêm một vế nhận diện vào `_kiem_dich_ghi`. Mô phỏng trong RAM xác nhận bỏ bit làm mất từ chối ở cả hai caller khi chúng tới đường được giả lập, còn nhận mọi thuộc tính khác 0 làm hỏng đối chứng bit `16`. `jar_rong_base` nằm ở packet 2 và kiểm hồi quy nhánh packet 1 giữ nguyên.
- **Trần.** Hai ước lượng cộng đúng, packet 1 **384–439** dòng thêm, dư 11 ở đầu trên, packet 2 **340–406**, dư 44. Mỗi packet có 3 tệp. Phép thử số liệu giả cho 450 đạt và 451 đỏ. §6 của cả hai yêu cầu dừng trước review và sửa revision khi số đo thật vượt 450.
- **Mỏ neo.** `openai_codex`, phiên Codex qua API, transport máy. `HEAD` và `master` cùng OID `641108cb997872b0ef2a277ea9c8faf8b82532bb`, tree `e6c7c50863421e32cac4f5f1894f176d758375b1`. Hai đặc tả là tệp chưa theo dõi. SHA-256 packet 1 `e415e6aef09860975d34bac518d9b0959b0f7d830e685184d48cf5d6c5592c6a`, packet 2 `72a2570c9d631914106b82ea9a8709da75ae19c8ddd2595973c5e3f2e7f0718f`. Review chỉ đọc, dùng dữ liệu giả trong RAM.

KET_LUAN: request_changes
tokens used
96,402
## Issue #433 · Review độc lập lượt 9

### Finding lượt 8

| Mức | Packet | Finding | Trạng thái |
|---|---|---|---|
| P2 | 1 | `db_w6_bo_kiem_dict` chết bằng `AttributeError` ngoài tập khai | **Đóng.** §4b #11 khai đúng ca `chung_du_lieu_sai_dang` và nhãn `config_khong_dict`. Phép đo với `[]`, `null` và `"s"` đều cho `AttributeError` chứa `object has no attribute 'update'`. |
| P2 | 1 và 2 | Các đột biến `oserror` làm lan ngoại lệ chưa khai | **Đóng.** Packet 1 #26 và packet 2 #20–21 khai đúng `OSError("wp433-oserror")` ở biên các lời gọi tương ứng. Packet 1 #27 giữ cơ chế H vì đột biến vẫn bắt lỗi và đổi hành vi trả về. |
| P3 | 2 | `db_bo_reparse` thiếu đích `reparse_w1` | **Đóng về khai báo.** N3c và §4b #13 đã thêm đích W1. Việc fixture có đi tới tiền tố gắn bit hay không vẫn cần sửa như finding dưới đây. |

### Finding mới

- **P2 · Packet 1 · §4b #8–10 chưa định danh đủ biên bắt ngoại lệ.** Cả ba mục khai cùng ca, cùng `UnicodeEncodeError` và cùng dấu `surrogates not allowed`, nhưng yêu cầu ba nhãn khác nhau. Tôi chạy ba phép thử trong RAM và xác nhận cả ba cùng khớp điều kiện đã khai. Tra theo tập của cả ca sẽ không xác định được nhãn nào thuộc lời gọi đang chạy. Gắn tập khai vào từng lượt gọi N3(3), N3(4), N3(5) và kiểm đỏ khi ngoại lệ khớp kiểu, thông điệp nhưng phát sinh ở lượt khác. [Packet 1 §4b](ops/specs/NLM-GWS-DICH-NGOAI-KHO-r1.md#4b-bảng-đột-biến--nguồn-duy-nhất-thắng-mọi-mô-tả-đột-biến-rải-trong-4)
- **P2 · Packet 1 · N1/N8 chưa chứng minh W3 áp chốt đích ghi.** `db_w3_bo_chot` bỏ cả kiểm jar lẫn kiểm đích, còn fixture đích dùng khóa `../thoat.json`. Nếu W3 chỉ bỏ `_kiem_dich_ghi` và vẫn giữ `_kiem_jar_nlm`, N1 vẫn từ chối đúng khóa và N8(3) vẫn kiểm được thứ tự trước chống hạ cấp. Phản chứng trong RAM xác nhận hai phiên bản cho cùng kết quả với khóa lạ và chỉ khác nhau khi khóa hợp lệ đi tới đích bị chặn. Cần một ca W3 có jar hợp lệ, đích bị chặn và đột biến chỉ bỏ chốt đích. [Packet 1 N1/N8](ops/specs/NLM-GWS-DICH-NGOAI-KHO-r1.md#4-nghiem_thu)
- **P2 · Packet 2 · `reparse_w1` chưa buộc W1 đi qua tiền tố gắn bit.** N3c giả lập `lstat` cho `profiles/default` nhưng chưa khai jar W1 chứa khóa nào. Phép dựng tiền tố theo M1 xác nhận jar hợp lệ chỉ có `auth.json` bỏ qua tiền tố ấy, còn `profiles/default/cookies.json` đi qua. Chốt khóa lồng trong fixture và yêu cầu §4b #13 chết ở cả `reparse` lẫn `reparse_w1`, cộng thêm `junction` trên Windows. [Packet 2 N3c](ops/specs/GWS-CRED-DICH-NGOAI-KHO-r1.md#4-nghiem_thu)
- **P3 · Packet 1 · §4b #7 cần fixture `list` khác rỗng.** N3(1) chỉ ghi kiểu `list`. Với `[]`, các nhánh giữ nguyên của W1 và W2 dừng trước `_kiem_jar_nlm`, nên không có `AttributeError` do `.items()` như dòng E khai. Với `[1]`, phép thử cho đúng loại và thông điệp. [Packet 1 N3](ops/specs/NLM-GWS-DICH-NGOAI-KHO-r1.md#4-nghiem_thu)
- **P3 · Packet 2 · M1 ghi sai kết quả `isabs` trên nền hỗ trợ.** `ntpath.isabs("\\fake")` trả `True` trên Python 3.11.18 và 3.12.3, `False` trên 3.13.18. Cả ba trả ổ rỗng từ `splitdrive`. N2w yêu cầu từ chối đúng. M1 cần nói rõ kiểm tra dạng **có gốc, thiếu ổ** trước nhánh chấp nhận theo `isabs`. [Packet 2 M1/N2w](ops/specs/GWS-CRED-DICH-NGOAI-KHO-r1.md#3-muc_tieu)

### Phạm vi và bằng chứng

- **§4b và L1–L7.** Đã rà từng mục trên giấy. Packet 1 có 32 đột biến, 8 E và 24 H. Packet 2 có 24 đột biến, 4 E và 20 H. Dòng 13b là đích native bổ sung của #13. `python3 -IB` trả rc 0 cho phép đối chiếu số đếm và các phép thử nguyên tố của 12 mục E trên Linux 3.13.18. Các finding chỉ ra lỗi L3/L5 ở biên ca, độ phủ hoặc nền đo. Không phát hiện thêm lỗi mức P0–P3 ở L1, L2, L4, L6, L7. Số đếm tiền nhiệm ở L4 vẫn được khai chưa đo được. Phép chạy fragment, bảng đột biến trên candidate và junction native đều `not_run`.
- **Chuyển phạm vi.** Packet 1 nhất quán giữa §2, §3 và §8 về `S_ISLNK` và giới hạn junction. Packet 2 M6 chỉ thêm một vế nhận diện vào `_kiem_dich_ghi`. Mô phỏng trong RAM xác nhận bỏ bit làm mất từ chối ở cả hai caller khi chúng tới đường được giả lập, còn nhận mọi thuộc tính khác 0 làm hỏng đối chứng bit `16`. `jar_rong_base` nằm ở packet 2 và kiểm hồi quy nhánh packet 1 giữ nguyên.
- **Trần.** Hai ước lượng cộng đúng, packet 1 **384–439** dòng thêm, dư 11 ở đầu trên, packet 2 **340–406**, dư 44. Mỗi packet có 3 tệp. Phép thử số liệu giả cho 450 đạt và 451 đỏ. §6 của cả hai yêu cầu dừng trước review và sửa revision khi số đo thật vượt 450.
- **Mỏ neo.** `openai_codex`, phiên Codex qua API, transport máy. `HEAD` và `master` cùng OID `641108cb997872b0ef2a277ea9c8faf8b82532bb`, tree `e6c7c50863421e32cac4f5f1894f176d758375b1`. Hai đặc tả là tệp chưa theo dõi. SHA-256 packet 1 `e415e6aef09860975d34bac518d9b0959b0f7d830e685184d48cf5d6c5592c6a`, packet 2 `72a2570c9d631914106b82ea9a8709da75ae19c8ddd2595973c5e3f2e7f0718f`. Review chỉ đọc, dùng dữ liệu giả trong RAM.

KET_LUAN: request_changes
rc=0 xong 2026-11-18T06:47:59Z
