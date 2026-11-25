Review độc lập **đặc tả wp1236 r10, vòng 5**, class `sensitive`: **changes_requested** — **1 P2, 1 P3**, thuộc hai lớp. P3 chưa được miễn nên vẫn chặn approval theo protocol §8.

Mỏ neo: HEAD `4b5e3c6b15eb311540447d67d0e0ad62a85e71d1`, tree `293d124054e74bb0459b69c2e5df6691b74af49d`; SHA-256 SPEC `9816599335afce624a058b445f0d9d85b1683fcc32aa232b874fa43b506c63ff`, khớp nguyên byte với blob `ops/specs/wp1236-r10.md` tại HEAD. Đã đọc diff r9→r10 và rà phần không đổi với các nghĩa vụ mới.

- **V01 — P2 — `nghiem-thu-khong-co-lap-chot-dich`**, nối alias `test-thieu-chot`: luật 3–5 chưa chốt một phép quét có thể tái lập. Tập (a)–(l) chưa chứa đầy đủ các toán tử đã dùng ở lượt 6; giá trị thay của g/h/i còn để executor chọn, và bộ quét ngoài kho chỉ buộc giao băm/biên nhận. Luật 4 còn yêu cầu đi qua `kiem_ho_so` cho `head` có/không, trong khi consumer này luôn gọi `kiem_mien(..., None)`; nhánh có head thuộc D2b. Cần manifest toán tử/site/phép thay/target, nguồn bộ đo và ma trận đúng consumer trước khi giao thi công tiếp. Vị trí: SPEC:316–337, đối chiếu :113–141 và :182–183.
- **V02 — P3 — `so-do-khong-cung-pham-vi-nguon`**: bảng A có **30 ca**, nhưng căn cứ kích thước vẫn ghi **28**; có **năm luật** nhưng phần dẫn ghi BA; review mã lượt 6 có **ba finding thuộc hai lớp**, không phải ba lớp. Cần đồng bộ các tổng hiện tại và tách chúng khỏi số lịch sử. Vị trí: SPEC:298, :341–372, :416–417, :542–549.

Luật 5 **giữ được hồi quy cũ**. Đã tìm đủ nguồn trong sandbox gốc, khớp MANIFEST lưu trong Git: 138 dòng trong năm JSONL, **127 ID duy nhất**, 11 bản trùng cùng bytes, không có xung đột nguồn hoặc regex hỏng. Chạy lại năm đối chứng trên bản sao fixture thật: `ref_any_run`, `ref_txt_wild`, `key_alpha_only`, `phi_substring`, `phi_skip_descendants` đều làm consumer từ có vi phạm thành `[]`; control sạch vẫn `[]`. Đây là phép đo trên mã r9 `c2d606b`, không phải kết quả kiểm implementation r10. Các mẫu cũ được luật 5 giữ không làm danh sách toán tử tổng quát (a)–(l) tự trở thành đầy đủ.

Theo tiêu chí E1 được giao, **chưa có đủ bằng chứng để công nhận cách đóng lớp mới của r10**. Giữ Review Rescue Checkpoint; đề xuất chốt bundle phép đo và chạy pilot trên `c2d606b`, phân biệt đúng 25 survivor không tương đương trước khi tiếp tục. Những phần đã đo có ích: ma trận năm ô trùng ID, hồi quy 127 ID và năm đối chứng consumer. Không kết luận mọi phương án đều bất khả thi, cũng không đòi chứng minh mọi chương trình bằng một tập toán tử hữu hạn. Chưa có căn cứ E3 rằng thiết kế đúng chữ r10 cho lời khai dương lọt ngoài giới hạn đã công bố.

Đối chiếu tất cả lớp của vòng 4 và lớp mã được kế thừa — các dòng trùng U01/U02 với lịch sử được gộp theo slug, giữ đầy đủ ID gốc trong JSON:

| Slug | Nhãn trên r10 | Bằng chứng/phần còn lại |
|---|---|---|
| `xuong-dong-khong-khop-byte-that` | DA_VA_THAT | SPEC:68–79; LF/CRLF đạt, CR lẻ/trộn bị chặn. |
| `nghiem-thu-khong-co-lap-chot-dich` — gồm U02 | VA_MOT_PHAN | Năm ô trùng ID đúng lý do; luật 3–5 còn V01. |
| `nang-tran-thieu-hop-dong-authority` | DA_VA_THAT | Khối nâng trần đủ; user xác nhận 1400; numstat r9 = 1324. |
| `d2b-thieu-neo-attempt` | DA_VA_THAT | SPEC:168–181, C3; int không bool, chỉ nhánh passed, neo header. |
| `so-do-khong-cung-pham-vi-nguon` | VA_MOT_PHAN | Corpus/số r9 đúng; tổng r10 tái mở ở V02. |
| `trang-thai-job-khong-khop-conclusion` | DA_VA_THAT | Bản sao T-fail đổi sang passed bị `ket_luan_lech`. |
| `landed-khong-buoc-loi-khai-hop-le` | DA_VA_THAT | Giữ ba dạng và lời khai hợp lệ; parity 170 hồ sơ/94 landed/0 lệch. |
| `l8-chua-chot-thu-tu-cutover` | DA_VA_THAT | Cutover trước L8; pr680 khớp băm và có vi phạm nếu áp L8. |
| `khong-kiem-co-toan-ven-provenance` | DA_VA_THAT | Bốn biến thể K3 đều `provenance_chua_du`, control đạt. |
| `hop-dong-dau-vao-dau-ra-chua-chot` — gồm U01 | DA_VA_THAT | SPEC:142–150, :184–196, C6 tách marker passed/waiver, lỗi và nhánh không chạy. |
| `nguon-doc-khong-neo-cung-snapshot` | DA_VA_THAT | L8 nhận dữ liệu đã nạp; D2b lấy dữ liệu từ OID, kiểm mode/path trong cây Git. |
| `he-qua-gioi-han-khai-thieu` | DA_VA_THAT | Hậu duệ/waiver/forgery/giới hạn log và Issue mục 3 vẫn được khai. |
| `pham-vi-kiem-chung-trai-adr-windows` — U03 | DA_VA_THAT | A/C required, B theo diff; miễn CI chỉ A theo user, local vẫn bắt buộc, skipped không tính đạt. |
| `test-thieu-chot` — mã lượt 1–6 | VA_MOT_PHAN | Nối vào lớp nghiệm thu, không đếm thêm lớp; giữ hai chuyển tiếp 0/1 và V01. |
| `mo-ta-duong-dan-lech-hop-dong` — mã L03 | VA_MOT_PHAN | Spec đã chốt `./tệp` hợp lệ; docstring mã r9 vẫn chưa sửa, chưa có mã r10 để xác nhận đóng. |

**Hội tụ vòng 4→5: 2/3.** F = U01, U03; U02 chưa đóng toàn lớp. Lớp số liệu tái mở không nằm trong U vòng 4 nên không thêm vào mẫu số. Lịch sử ba lớp lặp từ vòng 1–3 và hai chuyển tiếp mã 0/1 giữ nguyên; tỷ lệ 2/3 không xoá checkpoint hay cấp thêm ngân sách.

Các số đã đo khớp: 66 tệp = 47 passed/10 failed/9 not_measured; 170 hồ sơ = 25 cutover/56 đỏ/39 đạt/50 không lời khai; 93 vi phạm; 50 script = 20/28/2; 60/62 trích dẫn phân giải đúng. Hai script tham chiếu rc 0, stdout trùng byte với hiện vật trong kho. `audit_r5.py` rc 0 (`AUDIT_R5_COMPLETE`); `audit_method_r5.py` rc 0 (`METHOD_R5_COMPLETE`, 5/5 đối chứng). Chi tiết command, hash và kết quả nằm trong JSON cùng các tệp `audit_*.json`.

Số **1324/1400** đúng cho mã r9 và trần được xác nhận; chưa đo kích thước r10, không suy 76 dòng còn lại đủ cho mọi sửa đổi. Windows CI của A được miễn theo xác nhận của user về issuecomment-7048063512; audit neo exact head và Windows local vẫn là nghĩa vụ về sau. `luat_dung` vẫn giữ E2 cho trần, E5 cho authority, E3 cho bằng chứng đảo mục tiêu; checkpoint §12/E1 không bị bỏ chỉ vì danh sách này không chép lại E1.

`passed`, `failed`, `skipped`, `not_run` được tách trong JSON. Không chạy implementation r10, Windows, CI, full release/land gate hoặc Ruff cho review đặc tả; không gọi GitHub/mạng. Phiên `openai_codex / codex_service / machine`; model/effort/session phục vụ không đo được, không suy từ tên thư mục hay actor. Không tự tạo cross-approval hoặc authority land. Hai checkout được giữ chỉ đọc; snapshot cuối và validator được ghi trong `VERDICT.json` và `kiem_verdict.txt`.

KET_LUAN: changes_requested
