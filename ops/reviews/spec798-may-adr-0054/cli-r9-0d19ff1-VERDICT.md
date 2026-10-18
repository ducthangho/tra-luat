VERDICT: changes_requested
P0=0 P1=5 P2=4 P3=0   (đếm theo LỚP)

## Lớp may-tin-gia-tri-nguoi-goi — P1

- biểu hiện: `ops/specs/wp796-r9.md`:M1 — `REF` do người gọi chọn và lease qua `lease_publish.py check` chưa chứng minh lease đã được người có thẩm quyền công bố.
- biểu hiện: `ops/specs/wp796-r9.md`:_doc_connector — So hậu tố `/N` chưa ràng buộc repository; chỉ đối chiếu `review_comments` cũng chưa chứng minh tệp comment tóm tắt đủ trang.
- biểu hiện: `ops/specs/wp796-r9.md`:M3 — Luật `kiem-gate` hiện hành chỉ xét tên, ID, SHA và kết quả, nên check cùng tên từ producer khác có thể thay kết quả gate bắt buộc.
- biểu hiện: `ops/specs/wp796-r9.md`:M5 — Checkpoint phải có `packet_issue`, nhưng điều kiện nhận chưa đòi trường ấy bằng packet hiện tại.
- biểu hiện: `ops/specs/wp796-r9.md`:M5; `ops/specs/wp797-r9.md`:M2 — Slug dùng tăng bộ đếm vẫn do người gọi cung cấp, chưa có phép đối chiếu với ánh xạ lớp đã ghi.
- đường lỗi cụ thể: `lease_publish.kiem()` hiện nhận một lease chưa công bố chỉ với năm trường bắt buộc; đặt lease đầy đủ trên ref tự chọn vẫn thỏa đường M1. Với gate, phản chứng trong bộ nhớ dùng check bắt buộc `failure` ID 100 và check cùng tên từ producer khác `success` ID 101: `cmd_kiem_gate` trả 0. Checkpoint của packet khác cùng generation/SHA cũng không bị điều kiện M5 loại; đổi slug giữa các lần gọi làm phân tán `finding_counts`.
- hướng sửa ở mức lớp: Mỗi đầu vào mở quyền phải được đối chiếu với nguồn authority và đầy đủ phạm vi định danh: lease đã công bố, repository/PR, producer của gate, packet/generation/SHA của checkpoint và ánh xạ finding–slug đã neo. Thêm ca âm chỉ đổi từng thành phần này, giữ các điều kiện khác hợp lệ.

## Lớp ho-model-sai-enum — P1

- biểu hiện: `ops/specs/wp796-r9.md`:M2 — Đòi họ model của biên nhận bằng đúng `openai` trong lease, trong khi validator biên nhận dùng họ `gpt`.
- biểu hiện: `ops/specs/wp796-r9.md`:M2; `ops/specs/wp797-r9.md`:M1 — Đòi provider bằng đúng giữa hai hợp đồng dùng tên khác nhau: lease dùng `codex`, biên nhận dùng `openai_codex`.
- đường lỗi cụ thể: Đo trực tiếp `_ho_model_cua_ten("openai")` trả chuỗi rỗng; thêm `model_family: openai` vào biên nhận cross-review hợp lệ làm `_thieu()` báo không xác định được họ reviewer. Khai `provider: codex` cũng bị `_mri()` từ chối. Biên nhận dùng giá trị hợp lệ `gpt`/`openai_codex` lại không bằng đúng lease `openai`/`codex`.
- hướng sửa ở mức lớp: Định nghĩa adapter chuẩn hóa giữa hợp đồng lease và biên nhận trước phép so danh tính; ánh xạ rõ `openai ↔ gpt`, `codex ↔ openai_codex` và `execution_surface ↔ surface`. Kiểm bằng biên nhận thật qua validator, đồng thời giữ ca âm cho khác họ hoặc khác bề mặt thực sự.

## Lớp dieu-kien-dung-khong-xet-o-moi-cua — P1

- biểu hiện: `ops/specs/wp796-r9.md`:M5 — `mo-lai` cộng `finding_counts` nhưng vẫn quy định chuyển sang `running` hoặc `cho_chu_kho` khi bộ đếm đã chạm trần.
- biểu hiện: `ops/specs/wp796-r9.md`:M5 — `chu-kho-duyet` có thể đưa packet từ `cho_chu_kho` về `running` mà không xét lại trần đã chạm.
- biểu hiện: `ops/specs/wp796-r9.md`:M1; `ops/specs/wp797-r9.md`:M2 — Đường `init` thông thường chưa bị cấm đối với lease generation kế tiếp, nên có thể bỏ qua đường kế thừa ngân sách và tiêu thụ state cũ.
- đường lỗi cụ thể: Hai lần `mo-lai ci-do` cùng slug làm bộ đếm đạt `same_failure_limit`, nhưng M5 vẫn đưa về `running`; `begin-attempt` hiện chỉ kiểm trần attempt, không kiểm bộ đếm finding đã tồn tại. Tương tự, gọi `init` với lease g2 và thư mục mới, bỏ `--tu-state-dir`, đi qua M1 mà không thực hiện các chốt bảo toàn của M2.
- hướng sửa ở mức lớp: Dùng chung một phép xét điều kiện dừng tại mọi cửa tiếp tục công việc. Lease thay thế/generation kế tiếp phải đi qua đường kế thừa bắt buộc. Thêm phản chứng chạm trần qua `mo-lai`, qua checkpoint và qua `init` thông thường.

## Lớp quyen-va-ci-cu-con-hieu-luc — P1

- biểu hiện: `ops/specs/wp796-r9.md`:M5 — Nhánh `connector` không quy định xóa hoặc thay thế quyền `mo_lai_tu` đã sinh từ lần `ci-do` trước.
- biểu hiện: `ops/specs/wp797-r9.md`:M3 — `va-ci` không tiêu thụ quyền mở lại và không đòi đó là lần mở lại hiện hành dẫn tới `pending_sha`.
- đường lỗi cụ thể: H0 được mở lại vì CI, tạo `mo_lai_tu=H0`; vá thành S1 và ghi push `va-ci`. Connector sau đó báo P1 trên S1; chủ kho chỉ cho phép vá. Sau khi vá thành S2 và được approve, quyền H0 vẫn còn, nên `record-push va-ci` có thể dùng readback sạch của H0 để nhận lần đẩy S2, không cần checkpoint `cho_phep_day` cho S2.
- hướng sửa ở mức lớp: Neo quyền vào sự kiện mở lại hiện hành, gồm nguyên nhân, generation và SHA nguồn; tiêu thụ khi ghi push và thay thế khi có lần mở lại khác. Khóa bằng ca xuyên suốt CI → connector → chỉ cho vá → thử đẩy bằng quyền CI cũ.

## Lớp chuyen-generation-giu-nham-ngu-canh-thuc-thi — P1

- biểu hiện: `ops/specs/wp797-r9.md`:M2 — `branch` không thuộc nhóm NGỮ CẢNH hoặc ĐẶT LẠI, nên theo quy tắc “mọi khóa còn lại CHÉP”, nhánh g1 được giữ trong state g2.
- biểu hiện: `ops/specs/wp797-r9.md`:M3 — Mọi phép đo push đọc `branch` của state, nên lỗi kế thừa này điều khiển trực tiếp nhánh được xác minh.
- đường lỗi cụ thể: Lease mới giao `agent/wp797-g2-antigravity`, nhưng state mới vẫn mang `agent/wp797-g1-antigravity`. Đẩy S lên đúng nhánh g2 rồi gọi `record-push the-he-moi` sẽ hỏi nhánh g1 và từ chối; nếu g1 tình cờ cũng trỏ S, máy nhận bằng chứng từ sai nhánh.
- hướng sửa ở mức lớp: Đưa mọi trường định tuyến phái sinh từ lease, gồm `branch`, vào nhóm dựng lại. Ca generation kế tiếp phải dùng hai tên nhánh và hai đầu nhánh khác nhau, kiểm cả state lẫn ref thực sự được hỏi.

## Lớp quyet-dinh-p3-khong-luu — P2

- biểu hiện: `ops/specs/wp796-r9.md`:M2–M4 — P3 trong biên nhận offline được phép đi qua `_du_dieu_kien_approve`, nhưng xử lý và lưu `xu_ly_p3` chỉ bao phủ P3 của connector.
- biểu hiện: `ops/specs/wp797-r9.md`:M1 — Bảng lớp offline chỉ bắt buộc `slug`, `hang`, `finding_ids`, chưa bắt buộc quyết định có căn cứ cho P3 còn mở.
- biểu hiện: `ops/specs/wp796-r9.md`:M4 — Chỉ lý do có điều kiện khác rỗng; chưa quy định từ chối tên nợ, owner hoặc hướng xử lý rỗng.
- đường lỗi cụ thể: Biên nhận offline `approve` còn một lớp P3 nhưng không có disposition vẫn thỏa vị từ. Connector sau đó sạch thì `accept` lưu `xu_ly_p3=[]` và nhận packet `sensitive`, dù P3 offline chưa có quyết định bắt buộc theo ADR-0054 §3. Chuỗi `ID=:::abcdefghijkl` cũng chưa bị các điều kiện M4 loại.
- hướng sửa ở mức lớp: Dùng một sổ disposition cho toàn bộ P3 còn mở từ offline và connector; kiểm các trường bắt buộc khác rỗng và lưu quyết định gắn finding/SHA. Thêm ca offline-P3/connector-sạch và ca từng trường disposition rỗng.

## Lớp dem-vong-p3-lech-moc — P2

- biểu hiện: `ops/specs/wp797-r9.md`:M1 — Sau khi đổi verdict đầu thành mốc vòng 0, điều kiện giảm lớp vẫn bắt đầu “từ vòng thứ hai”.
- đường lỗi cụ thể: Mốc có hai lớp P3; vòng vá thứ nhất vẫn có hai lớp. Đọc đúng cách đánh số mới, vòng 1 chưa phải “vòng thứ hai”, nên chưa phải giảm; ADR-0054 yêu cầu dừng ngay khi bất kỳ vòng vá thêm nào không giảm. A2 lại yêu cầu chính chuyển tiếp 2 → 2 này bị chặn.
- hướng sửa ở mức lớp: Tách số thứ tự verdict khỏi số vòng vá; so giảm ngay từ vòng vá 1 với mốc 0. Có ca riêng mốc → vòng 1 không giảm, với trần attempt/review đủ rộng để không che phép đo.

## Lớp so-sanh-hai-dong-ho — P2

- biểu hiện: `ops/specs/wp796-r9.md`:_doc_connector; M3 — `moc_connector` lấy ID lớn nhất chung từ comment tóm tắt và comment finding.
- biểu hiện: `ops/specs/wp797-r9.md`:M2 — Finding muộn phải có ID lớn hơn mốc chung ấy, dù hai loại comment thuộc hai không gian ID khác nhau.
- đường lỗi cụ thể: Readback PR #732 trong clone có comment connector ở endpoint issue ID `6099688920`, còn comment diff ID `4238336830`. Finding diff đến sau với ID `4238336831` vẫn nhỏ hơn mốc chung và bị từ chối, dù timestamp mới hơn. Đổi sang thời gian máy chủ chưa làm hai dãy ID trở nên so sánh được.
- hướng sửa ở mức lớp: Lưu watermark riêng theo loại đối tượng/endpoint, kèm repository và PR; chỉ so ID trong cùng không gian. Kiểm ca finding diff đến muộn khi ID tóm tắt lớn hơn, gồm cả trường hợp cùng giây.

## Lớp ca-nghiem-thu-khong-phan-biet-dung-sai — P2

- biểu hiện: `ops/specs/wp796-r9.md`:A2 — Lease thiếu hoặc blob lệch hash vẫn được liệt kê là kết quả `false`, trái M1 và A11 yêu cầu lỗi, không tạo state.
- biểu hiện: `ops/specs/wp797-r9.md`:A3 — Vẫn yêu cầu từ chối `created_at ≤ accepted_at`, trái M2 và A9 đã bỏ so với đồng hồ cục bộ.
- đường lỗi cụ thể: Một `init` xử lý đúng lease thiếu theo M1 không thể đồng thời tạo kết quả chế độ `false` như A2. Với thời gian máy chủ mốc 12:00, finding 12:01 và `accepted_at` cục bộ 12:10, M2 phải nhận nhưng A3 phải từ chối; hai tiêu chí yêu cầu kết quả ngược nhau trên cùng đầu vào.
- hướng sửa ở mức lớp: Đồng bộ toàn bộ oracle nghiệm thu với yêu cầu r9: lỗi authority phải phân biệt với chế độ `false`; finding muộn chỉ so watermark máy chủ đúng loại. Mỗi ca cần baseline dương và thay đúng một yếu tố để đột biến đỏ vì chốt được nhắm tới.