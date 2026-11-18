## Review độc lập lượt 6 · Issue #433

Base `641108cb997872b0ef2a277ea9c8faf8b82532bb`, tree `e6c7c50863421e32cac4f5f1894f176d758375b1`. Checkout ở detached HEAD, khớp hai ref cục bộ `master` và `origin/master`. Hai đặc tả là tệp chưa được Git theo dõi, nên lượt review neo vào SHA-256 của từng tệp.

| Packet | SHA-256 đặc tả |
|---|---|
| 1 · NLM-GWS | `adfbe103366d4fac01528b34ba7e5f6abceeee85653ba72f1d916e9d2ec073c1` |
| 2 · GWS-CRED | `0ed2aa0719d430c43bc807e34ae1e9ab55cd6e848d986c9cc7fb4dd5ec517e4b` |

Reviewer `openai_codex`, phiên API với shell cục bộ, transport `machine`. Các phép thử `python3 -I -B` trong RAM trên Linux/Python 3.13.18 trả rc 0, gồm các khẳng định tái hiện lỗi đặc tả. Dữ liệu hoàn toàn giả. Junction native, CI và gate trên mã triển khai chưa chạy.

## Findings lượt 5

| Mức | Packet | Trạng thái | Bằng chứng |
|---|---|---|---|
| P2 | 1 | **Đóng** | N6(1) có `w1_la_symlink` và `db_bo_tien_to_cuoi`. Trong RAM, `S_ISLNK` chỉ đúng ở lá. Vòng đủ tiền tố từ chối và vòng bỏ lá cho qua. Ca yêu cầu rc 1, lá vẫn là symlink, đích giữ byte và không có tệp jar mới. |
| P2 | 1 | **Chưa đóng** | `repr` giữ một dòng và `fullmatch` phân loại đúng khoá chứa cụm lỗi khác. Tuy nhiên M4 vẫn yêu cầu cả dòng “chứa đúng một” cụm, trái với N8. `db_khong_repr` cũng sống trên fixture đã ghi. |
| P2 | 2 | **Chưa đóng** | M3 kế thừa định dạng cố định, nhưng `db_khong_repr_gws` sống trên fixture N3e. |
| P2 | 2 | **Đóng** | N5 giới hạn kiểm 0600 trên POSIX cho cả nguồn lúc `replace` và tệp sau ghi. Phép thử điều kiện nhận `posix/0600`, bác `posix/0666` và bỏ kiểm mode ở `nt/0666` giả lập. |
| P3 | Cả hai | **Đóng** | §7 dùng chung bộ đếm, ghi 3 lần ở mức đặc tả và 0 ở mức mã, không reset khi tách. Số đếm tiền nhiệm được ghi là chưa đo được. Stdout năm lượt trước vẫn là chứng cứ được dẫn nhưng chưa đối chiếu độc lập trong checkout này. |

**P2 còn mở · Cả hai packet · Ca xuống dòng kiểm sai đường.** Tôi chạy nguyên hàm `_trong_kho_git` của base trong RAM, với `lstat` giả chỉ công nhận `K/.git`. Cả `K/a\nb/home/.notebooklm-mcp-cli` và `K/a\nb/gws` đều trả `K`. M1 của packet 1 quy định in **đường kho**, nên bỏ `repr` vẫn cho `nằm trong kho git: K`, đúng một dòng và vẫn `fullmatch`. Đặt ký tự xuống dòng trong chính đường kho được trả về, hoặc dùng một ca từ chối khác mà chi tiết thực sự mang đường chứa ký tự đó. Riêng packet 1, dòng `ngoài danh sách cho phép: 'x là liên kết tượng trưng'` khớp đúng một tiền tố nhưng chứa hai cụm. M4 cần giới hạn điều kiện “đúng một” vào trường phân loại. [Packet 1 M4](ops/specs/NLM-GWS-DICH-NGOAI-KHO-r1.md#3-muc_tieu) · [Packet 1 N8](ops/specs/NLM-GWS-DICH-NGOAI-KHO-r1.md#4-nghiem_thu) · [Packet 2 N3e](ops/specs/GWS-CRED-DICH-NGOAI-KHO-r1.md#4-nghiem_thu)

## Findings mới

- **P2 · Packet 2 · N4 đặt neo đột biến trên phiên bản chưa có vế cần xoá.** N4 yêu cầu neo `FILE_ATTRIBUTE_REPARSE_POINT` trong thân `_kiem_dich_ghi` “trên base thật”. §6 đồng thời cấm cấp lease nếu base đã có vế đó. Theo quy tắc neo phải khớp đúng một lần, đột biến này sẽ `HONG` ngay từ bước tìm neo. Neo cần đặt trên nguồn candidate đã áp M6 và dùng chung với N3c. [Packet 2 N4](ops/specs/GWS-CRED-DICH-NGOAI-KHO-r1.md#4-nghiem_thu) · [Packet 2 §6](ops/specs/GWS-CRED-DICH-NGOAI-KHO-r1.md#6-luat_dung)
- **P3 · Cả hai packet · Mốc ước lượng §8 sai theo đồng hồ phiên.** Hai tệp ghi đã “tính lại 06:40Z”, trong khi `date -u` lúc đọc trả `06:31:17Z` cùng ngày. Các tổng cộng đúng, nhưng mốc L5 cần phản ánh giờ tính thực tế. [Packet 1 §8](ops/specs/NLM-GWS-DICH-NGOAI-KHO-r1.md#8-chua_do_duoc) · [Packet 2 §8](ops/specs/GWS-CRED-DICH-NGOAI-KHO-r1.md#8-chua_do_duoc)

## Phạm vi reparse, trần và L1–L7

- **Reparse:** Packet 1 nhất quán về phạm vi hiện hành. §2, §3 và §8 chỉ nhận diện `S_ISLNK` và khai rõ giới hạn junction. Mã và hai phép đo reparse nằm ở packet 2. `jar_rong_base` cũng chuyển sang packet 2, còn điều kiện nhánh W1–W3 giữ nguyên. M6 của packet 2 chỉ thêm một vế nhận diện vào hàm chung. Mô phỏng trong RAM cho cả tiền tố W5 và `reparse_w1` xác nhận bit 1024 đổi kết quả từ cho qua sang từ chối, còn thuộc tính 16 được cho qua. N4 vẫn vướng neo như trên.
- **Trần:** Packet 1 cộng đúng **384–439 dòng thêm**, còn **11** dòng ở đầu trên. Packet 2 cộng đúng **340–406**, còn **44**. Mỗi packet có **3 tệp**. Với ba dòng `numstat` giả và đúng tập đường dẫn, 450 xanh, 451 đỏ. §6 của cả hai yêu cầu dừng trước review và đi revision nếu vượt. Hai OID ADR đúng trên lịch sử first-parent cục bộ, với `cat-file` tại OID và cha lần lượt trả 0 và 128. Độ mới của ref chưa được xác minh qua fetch. Kích thước triển khai vẫn là ước lượng, chờ `numstat` trên exact head.
- **L1–L7:** L1 có đơn vị đếm, L2 ánh xạ mục tiêu vào write set, L4 ghi rõ bằng chứng kế thừa còn thiếu, L7 dùng E2 và điều kiện cấp quyền đã nêu. L3 và L6 còn lỗi ở phép thử xuống dòng và neo N4. L5 còn mốc §8 cần sửa.

KET_LUAN: request_changes
tokens used
90,765
## Review độc lập lượt 6 · Issue #433

Base `641108cb997872b0ef2a277ea9c8faf8b82532bb`, tree `e6c7c50863421e32cac4f5f1894f176d758375b1`. Checkout ở detached HEAD, khớp hai ref cục bộ `master` và `origin/master`. Hai đặc tả là tệp chưa được Git theo dõi, nên lượt review neo vào SHA-256 của từng tệp.

| Packet | SHA-256 đặc tả |
|---|---|
| 1 · NLM-GWS | `adfbe103366d4fac01528b34ba7e5f6abceeee85653ba72f1d916e9d2ec073c1` |
| 2 · GWS-CRED | `0ed2aa0719d430c43bc807e34ae1e9ab55cd6e848d986c9cc7fb4dd5ec517e4b` |

Reviewer `openai_codex`, phiên API với shell cục bộ, transport `machine`. Các phép thử `python3 -I -B` trong RAM trên Linux/Python 3.13.18 trả rc 0, gồm các khẳng định tái hiện lỗi đặc tả. Dữ liệu hoàn toàn giả. Junction native, CI và gate trên mã triển khai chưa chạy.

## Findings lượt 5

| Mức | Packet | Trạng thái | Bằng chứng |
|---|---|---|---|
| P2 | 1 | **Đóng** | N6(1) có `w1_la_symlink` và `db_bo_tien_to_cuoi`. Trong RAM, `S_ISLNK` chỉ đúng ở lá. Vòng đủ tiền tố từ chối và vòng bỏ lá cho qua. Ca yêu cầu rc 1, lá vẫn là symlink, đích giữ byte và không có tệp jar mới. |
| P2 | 1 | **Chưa đóng** | `repr` giữ một dòng và `fullmatch` phân loại đúng khoá chứa cụm lỗi khác. Tuy nhiên M4 vẫn yêu cầu cả dòng “chứa đúng một” cụm, trái với N8. `db_khong_repr` cũng sống trên fixture đã ghi. |
| P2 | 2 | **Chưa đóng** | M3 kế thừa định dạng cố định, nhưng `db_khong_repr_gws` sống trên fixture N3e. |
| P2 | 2 | **Đóng** | N5 giới hạn kiểm 0600 trên POSIX cho cả nguồn lúc `replace` và tệp sau ghi. Phép thử điều kiện nhận `posix/0600`, bác `posix/0666` và bỏ kiểm mode ở `nt/0666` giả lập. |
| P3 | Cả hai | **Đóng** | §7 dùng chung bộ đếm, ghi 3 lần ở mức đặc tả và 0 ở mức mã, không reset khi tách. Số đếm tiền nhiệm được ghi là chưa đo được. Stdout năm lượt trước vẫn là chứng cứ được dẫn nhưng chưa đối chiếu độc lập trong checkout này. |

**P2 còn mở · Cả hai packet · Ca xuống dòng kiểm sai đường.** Tôi chạy nguyên hàm `_trong_kho_git` của base trong RAM, với `lstat` giả chỉ công nhận `K/.git`. Cả `K/a\nb/home/.notebooklm-mcp-cli` và `K/a\nb/gws` đều trả `K`. M1 của packet 1 quy định in **đường kho**, nên bỏ `repr` vẫn cho `nằm trong kho git: K`, đúng một dòng và vẫn `fullmatch`. Đặt ký tự xuống dòng trong chính đường kho được trả về, hoặc dùng một ca từ chối khác mà chi tiết thực sự mang đường chứa ký tự đó. Riêng packet 1, dòng `ngoài danh sách cho phép: 'x là liên kết tượng trưng'` khớp đúng một tiền tố nhưng chứa hai cụm. M4 cần giới hạn điều kiện “đúng một” vào trường phân loại. [Packet 1 M4](ops/specs/NLM-GWS-DICH-NGOAI-KHO-r1.md#3-muc_tieu) · [Packet 1 N8](ops/specs/NLM-GWS-DICH-NGOAI-KHO-r1.md#4-nghiem_thu) · [Packet 2 N3e](ops/specs/GWS-CRED-DICH-NGOAI-KHO-r1.md#4-nghiem_thu)

## Findings mới

- **P2 · Packet 2 · N4 đặt neo đột biến trên phiên bản chưa có vế cần xoá.** N4 yêu cầu neo `FILE_ATTRIBUTE_REPARSE_POINT` trong thân `_kiem_dich_ghi` “trên base thật”. §6 đồng thời cấm cấp lease nếu base đã có vế đó. Theo quy tắc neo phải khớp đúng một lần, đột biến này sẽ `HONG` ngay từ bước tìm neo. Neo cần đặt trên nguồn candidate đã áp M6 và dùng chung với N3c. [Packet 2 N4](ops/specs/GWS-CRED-DICH-NGOAI-KHO-r1.md#4-nghiem_thu) · [Packet 2 §6](ops/specs/GWS-CRED-DICH-NGOAI-KHO-r1.md#6-luat_dung)
- **P3 · Cả hai packet · Mốc ước lượng §8 sai theo đồng hồ phiên.** Hai tệp ghi đã “tính lại 06:40Z”, trong khi `date -u` lúc đọc trả `06:31:17Z` cùng ngày. Các tổng cộng đúng, nhưng mốc L5 cần phản ánh giờ tính thực tế. [Packet 1 §8](ops/specs/NLM-GWS-DICH-NGOAI-KHO-r1.md#8-chua_do_duoc) · [Packet 2 §8](ops/specs/GWS-CRED-DICH-NGOAI-KHO-r1.md#8-chua_do_duoc)

## Phạm vi reparse, trần và L1–L7

- **Reparse:** Packet 1 nhất quán về phạm vi hiện hành. §2, §3 và §8 chỉ nhận diện `S_ISLNK` và khai rõ giới hạn junction. Mã và hai phép đo reparse nằm ở packet 2. `jar_rong_base` cũng chuyển sang packet 2, còn điều kiện nhánh W1–W3 giữ nguyên. M6 của packet 2 chỉ thêm một vế nhận diện vào hàm chung. Mô phỏng trong RAM cho cả tiền tố W5 và `reparse_w1` xác nhận bit 1024 đổi kết quả từ cho qua sang từ chối, còn thuộc tính 16 được cho qua. N4 vẫn vướng neo như trên.
- **Trần:** Packet 1 cộng đúng **384–439 dòng thêm**, còn **11** dòng ở đầu trên. Packet 2 cộng đúng **340–406**, còn **44**. Mỗi packet có **3 tệp**. Với ba dòng `numstat` giả và đúng tập đường dẫn, 450 xanh, 451 đỏ. §6 của cả hai yêu cầu dừng trước review và đi revision nếu vượt. Hai OID ADR đúng trên lịch sử first-parent cục bộ, với `cat-file` tại OID và cha lần lượt trả 0 và 128. Độ mới của ref chưa được xác minh qua fetch. Kích thước triển khai vẫn là ước lượng, chờ `numstat` trên exact head.
- **L1–L7:** L1 có đơn vị đếm, L2 ánh xạ mục tiêu vào write set, L4 ghi rõ bằng chứng kế thừa còn thiếu, L7 dùng E2 và điều kiện cấp quyền đã nêu. L3 và L6 còn lỗi ở phép thử xuống dòng và neo N4. L5 còn mốc §8 cần sửa.

KET_LUAN: request_changes
rc=0 xong 2026-11-18T06:32:44Z
