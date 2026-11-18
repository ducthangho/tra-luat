Review độc lập lượt 8, Issue #433. HEAD `641108cb997872b0ef2a277ea9c8faf8b82532bb`, tree `e6c7c50863421e32cac4f5f1894f176d758375b1`. Phép thử `python3 -I -B` trên Linux, Python 3.13.18, trả rc 0. Dùng dữ liệu giả trong RAM, không ghi worktree, không gọi mạng. Windows native, junction thật và gate triển khai `not_run`.

| Finding lượt 7 | Packet | Trạng thái | Bằng chứng |
|---|---|---|---|
| P2 — Fixture `k\nho` không dựng được trên Windows | 1 và 2 | **Đóng ở mức đặc tả** | N8(2b) và N3e giữ kho thật trên POSIX, dùng đồ giả `_trong_kho_git` trên Windows. Thử bằng `ntpath` với các đường đối số W1/W4/W5 cho thấy chỉ đường đích nhận hậu tố xuống dòng. Đường khác trong cùng kho và đường ngoài kho đi qua hàm thật của base. `repr` cho một dòng, nội suy thô cho hai dòng. |
| P2 — Ngoại lệ thoát làm đột biến W6 không được tính là giết đúng | 1 | **Chưa đóng hết** | M5 đã cho `UnicodeEncodeError` và `ValueError` có dấu hiệu đã khai đi qua biên thành đúng nhãn. Phép thử xác nhận `AttributeError` ngoài tập lan nguyên đối tượng và vẫn là tín dụng giả theo N10(c). Tuy nhiên, `db_w6_bo_kiem_dict` còn vướng chính luật này. |

### Finding còn mở và finding mới

| Mức | Packet | Finding |
|---|---|---|
| **P2 — còn mở từ lượt 7** | 1 | **N3 `db_w6_bo_kiem_dict` không thể giết đúng nhãn theo M5.** Bỏ kiểm `dict` rồi gọi `.update` với `[]`, `null` hoặc `"s"` ném `AttributeError` ở cả ba lượt thử. M5 yêu cầu ngoại lệ này lan nguyên vẹn, nhưng N3 đòi nhãn `config_khong_dict`. Có thể khai một phép bắt riêng tại biên của ca này và giữ tự kiểm N10(c) ngoài tập, hoặc đổi đột biến để nó trả về và làm hỏng hậu điều `config_khong_dict`. |
| **P2 — mới, cùng lớp với lượt 7** | 1 và 2 | **Các đột biến bỏ `except OSError` thiếu khai báo ở biên ca.** Packet 1 N8 đòi `db_oserror_lan` giết bằng `oserror_w1`. Packet 2 N7 đòi `db_w4_oserror_lan` và `db_w5_oserror_lan` giết bằng `oserror_w4` và `oserror_w5`. Đồ giả `os.replace` ném `OSError`, nhưng M5 packet 1 và luật M4 packet 2 dẫn chiếu đều không khai ngoại lệ này cho các ca đó. Phép thử xác nhận `OSError` lan nguyên đối tượng, nên không được tính là giết đúng. Khai riêng `OSError` kèm dấu fixture cho từng ca đích sẽ giữ được tập đóng. |
| **P3 — mới** | 2 | **N3c có hậu điều `reparse_w1` nhưng thiếu đột biến buộc hậu điều này đổi màu.** `db_bo_reparse` chỉ đòi nhãn W5 `reparse` và nhãn Windows `junction`. Bỏ riêng kiểm tra `reparse_w1` vẫn đáp ứng cả hai đích đã khai. Thêm `reparse_w1` làm đích riêng của chính đột biến bỏ bit để đo việc M6 áp dụng cho caller packet 1. |

**Chuyển phạm vi.** Packet 1 §2, §3 và §8 nhất quán về `S_ISLNK` và giới hạn junction. Mã reparse, ca giả lập và junction thật cùng thuộc packet 2. Packet 2 M6 và §6 chỉ cho đổi biểu thức nhận diện trong `_kiem_dich_ghi`. Phép thử biểu thức trong RAM phân biệt thư mục thường, bit reparse `1024` và đối chứng bit thư mục `16`. N3c gọi W1 qua `reparse_w1`, với thiếu sót về đích đột biến nêu trên. `jar_rong_base` ở packet 2 N3d đo hồi quy cho nhánh mã packet 1 giữ nguyên.

**L1–L7 và trần.** L1 có đơn vị đếm và L2 ánh xạ được các thay đổi vào ba tệp của từng write set. Các lỗi L3 và phép đo dòng thuộc L6 nằm trong bảng trên. L4 khai phần bộ đếm tiền nhiệm chưa đo được và dùng chung bộ đếm hiện tại. Với L5, cộng lại được **384–439 dòng thêm** cho packet 1 và **340–406** cho packet 2, còn biên lần lượt **11** và **44** dòng theo đầu trên của ước lượng. Số `numstat` thực tế chờ candidate. Cả hai §6 yêu cầu dừng trước review ở 451 dòng trở lên. L7 không có điểm hỏi mới ngoài các điều kiện thẩm quyền đã dẫn.

KET_LUAN: request_changes
tokens used
60,003
Review độc lập lượt 8, Issue #433. HEAD `641108cb997872b0ef2a277ea9c8faf8b82532bb`, tree `e6c7c50863421e32cac4f5f1894f176d758375b1`. Phép thử `python3 -I -B` trên Linux, Python 3.13.18, trả rc 0. Dùng dữ liệu giả trong RAM, không ghi worktree, không gọi mạng. Windows native, junction thật và gate triển khai `not_run`.

| Finding lượt 7 | Packet | Trạng thái | Bằng chứng |
|---|---|---|---|
| P2 — Fixture `k\nho` không dựng được trên Windows | 1 và 2 | **Đóng ở mức đặc tả** | N8(2b) và N3e giữ kho thật trên POSIX, dùng đồ giả `_trong_kho_git` trên Windows. Thử bằng `ntpath` với các đường đối số W1/W4/W5 cho thấy chỉ đường đích nhận hậu tố xuống dòng. Đường khác trong cùng kho và đường ngoài kho đi qua hàm thật của base. `repr` cho một dòng, nội suy thô cho hai dòng. |
| P2 — Ngoại lệ thoát làm đột biến W6 không được tính là giết đúng | 1 | **Chưa đóng hết** | M5 đã cho `UnicodeEncodeError` và `ValueError` có dấu hiệu đã khai đi qua biên thành đúng nhãn. Phép thử xác nhận `AttributeError` ngoài tập lan nguyên đối tượng và vẫn là tín dụng giả theo N10(c). Tuy nhiên, `db_w6_bo_kiem_dict` còn vướng chính luật này. |

### Finding còn mở và finding mới

| Mức | Packet | Finding |
|---|---|---|
| **P2 — còn mở từ lượt 7** | 1 | **N3 `db_w6_bo_kiem_dict` không thể giết đúng nhãn theo M5.** Bỏ kiểm `dict` rồi gọi `.update` với `[]`, `null` hoặc `"s"` ném `AttributeError` ở cả ba lượt thử. M5 yêu cầu ngoại lệ này lan nguyên vẹn, nhưng N3 đòi nhãn `config_khong_dict`. Có thể khai một phép bắt riêng tại biên của ca này và giữ tự kiểm N10(c) ngoài tập, hoặc đổi đột biến để nó trả về và làm hỏng hậu điều `config_khong_dict`. |
| **P2 — mới, cùng lớp với lượt 7** | 1 và 2 | **Các đột biến bỏ `except OSError` thiếu khai báo ở biên ca.** Packet 1 N8 đòi `db_oserror_lan` giết bằng `oserror_w1`. Packet 2 N7 đòi `db_w4_oserror_lan` và `db_w5_oserror_lan` giết bằng `oserror_w4` và `oserror_w5`. Đồ giả `os.replace` ném `OSError`, nhưng M5 packet 1 và luật M4 packet 2 dẫn chiếu đều không khai ngoại lệ này cho các ca đó. Phép thử xác nhận `OSError` lan nguyên đối tượng, nên không được tính là giết đúng. Khai riêng `OSError` kèm dấu fixture cho từng ca đích sẽ giữ được tập đóng. |
| **P3 — mới** | 2 | **N3c có hậu điều `reparse_w1` nhưng thiếu đột biến buộc hậu điều này đổi màu.** `db_bo_reparse` chỉ đòi nhãn W5 `reparse` và nhãn Windows `junction`. Bỏ riêng kiểm tra `reparse_w1` vẫn đáp ứng cả hai đích đã khai. Thêm `reparse_w1` làm đích riêng của chính đột biến bỏ bit để đo việc M6 áp dụng cho caller packet 1. |

**Chuyển phạm vi.** Packet 1 §2, §3 và §8 nhất quán về `S_ISLNK` và giới hạn junction. Mã reparse, ca giả lập và junction thật cùng thuộc packet 2. Packet 2 M6 và §6 chỉ cho đổi biểu thức nhận diện trong `_kiem_dich_ghi`. Phép thử biểu thức trong RAM phân biệt thư mục thường, bit reparse `1024` và đối chứng bit thư mục `16`. N3c gọi W1 qua `reparse_w1`, với thiếu sót về đích đột biến nêu trên. `jar_rong_base` ở packet 2 N3d đo hồi quy cho nhánh mã packet 1 giữ nguyên.

**L1–L7 và trần.** L1 có đơn vị đếm và L2 ánh xạ được các thay đổi vào ba tệp của từng write set. Các lỗi L3 và phép đo dòng thuộc L6 nằm trong bảng trên. L4 khai phần bộ đếm tiền nhiệm chưa đo được và dùng chung bộ đếm hiện tại. Với L5, cộng lại được **384–439 dòng thêm** cho packet 1 và **340–406** cho packet 2, còn biên lần lượt **11** và **44** dòng theo đầu trên của ước lượng. Số `numstat` thực tế chờ candidate. Cả hai §6 yêu cầu dừng trước review ở 451 dòng trở lên. L7 không có điểm hỏi mới ngoài các điều kiện thẩm quyền đã dẫn.

KET_LUAN: request_changes
rc=0 xong 2026-11-18T06:40:38Z
