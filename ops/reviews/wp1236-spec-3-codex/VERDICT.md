Đã review tại HEAD `cc4162d0e0c61e8c085642ad52362166a0fbd2da`, tree `21f89c3c8cd1b7c523f9e2d63dfff1945ee155ca`. Không gọi mạng; đối chiếu băm đầu/cuối của 12.493 tệp không có thay đổi, Git sạch.

Số đo nằm trong [census.txt](/tmp/claude-0/-home-user-tra-luat/c92183b3-a8f8-5623-a5f6-065b91f250aa/scratchpad/review/r3-codex/work/census.txt) và [probes.txt](/tmp/claude-0/-home-user-tra-luat/c92183b3-a8f8-5623-a5f6-065b91f250aa/scratchpad/review/r3-codex/work/probes.txt). Module mới chưa tồn tại: nhận xét về ca nghiệm thu và đột biến là kiểm hợp đồng, không phải lời khai đã chạy triển khai. Chưa xác minh được nguồn N1/N2 ngoài clone được cấp.

# VERDICT wp1236 r3 vòng 3

spec_sha256: e4166c02939f154c1d434b97840655d6184e028085f8ec8fe5b99bed885f5f22

## Finding vòng 2 của tôi

Các id dưới đây thuộc VERDICT vòng 2, gồm những finding kế thừa.

- F01: ĐÓNG — K5 tiếp tục đối chiếu tên, nhãn, kết luận và chọn luật từ provenance.
- F02: ĐÓNG — Đã thêm attempt, cấm thừa kế neo và đòi bằng chứng ở merge SHA; lỗi phân loại mới của r3 ghi tại G09.
- F03: ĐÓNG — Phép nối tên REST đã sửa đúng lỗi cũ; lỗi mới do dùng `chan_buoc` ghi tại G08.
- F04: ĐÓNG — K3 vẫn bác tập job rỗng, toàn skipped và chỉ còn `chuan-bi`.
- F05: ĐÓNG — Định nghĩa lời khai và các số 64, 8/9, 36 đều được đo lại, khớp.
- F06: ĐÓNG — Bốn loại dấu hiệu vẫn biểu diễn được ngữ nghĩa cần kiểm.
- F07: ĐÓNG — Các chốt C1/C2/C3 và yêu cầu phân biệt đột biến tương đương được giữ.
- F08: ĐÓNG — Cột neo giới hạn đúng phạm vi băm/tập job; K1 bác head rút gọn.
- G01: ĐÓNG — Đã bỏ giả định tên REST bằng `Run <CMD>`; `ghep_buoc` nguyên trạng ghép được 23/23 job của dữ liệu `pr1231`.
- G02: ĐÓNG — Các đường thiếu attempt, kế thừa neo tổ tiên và chỉ có bằng chứng pre-merge đã được chặn trong hợp đồng.
- G03: ĐÓNG — Bảng giá trị, miễn trừ theo băm và hàng `pr679` đều khớp phép đo.
- G04: ĐÓNG — A4a chuyển sang canh trực tiếp phép so tên, không còn yêu cầu giết đột biến chọn nguồn tương đương.
- G05: CÒN MỞ — P2: URL + SHA + lý do tự khai vẫn không chứng minh waiver bền của owner đúng phạm vi theo protocol §10.2.3; cần readback/receipt có căn cứ thẩm quyền, không chỉ loại actor và nội dung comment khỏi phạm vi.
- G06: ĐÓNG — Miền hiệu lực chặn luật cũ cho run ngoài miền; vấn đề sinh lại bằng chứng lịch sử ghi tại G10.
- G07: ĐÓNG — L-7 đã bỏ yêu cầu mọi lời khai đều dương và thêm B8 cho lời khai phụ; sai số cùng thiếu sót phạm vi của Q7 ghi tại G11.

## Findings mới

- id: G08
  severity: P1
  vi_tri: SPEC.md dòng 194–205, 460–466, 486–487
  van_de: K7 dùng nguyên trạng `chan_buoc` khiến bước registry trong fixture dương và nhiều bước CI thật bắt buộc trở thành `not_measured`.
  bang_chung: "`python -B work/probes.py` ⇒ bước `test registry (phạm vi + các bộ chưa được nối)` có REST `success`, nhưng `chan_buoc=True`, `extra_keys=['env']`; `ci_provenance.py:252–254` chặn mọi khóa bước ngoài `KHOA_BUOC`, trong đó không có `env`. F-ok phải giữ nguyên bước này, còn A15 chỉ kiểm tên/kết luận nên không phát hiện việc K7 bác nó."
  de_xuat: "Chốt lại điều kiện kiểm chế độ chạy phù hợp với workflow thật; nếu cần adapter hoặc sửa hàm dùng chung thì quy định rõ trong đặc tả/write set. Giữ nguyên `env` của fixture và thêm đường dương chạy đủ K7 trên workflow thật."

- id: G09
  severity: P1
  vi_tri: SPEC.md dòng 244–256, 264, 524–525, 630–632
  van_de: Định nghĩa lời khai land phụ thuộc vào trạng thái dương/waived, khiến trạng thái thất bại hoặc chưa đo bị loại trước khi L-7 kiểm tính hợp lệ.
  bang_chung: "Dòng 256 chỉ định nghĩa lời khai land cho lời khai “dương hoặc owner_waived”; dòng 264 cho lời khai ngoài land chỉ cần đúng định dạng. Vì vậy, khi đã có một lời khai land đạt, một lời khai khác ở cùng merge SHA mang `failed` hoặc `not_measured` không chịu yêu cầu “MỌI lời khai land”; điều này không cưỡng chế được Q8. Đây là phản chứng hợp đồng, chưa chạy module mới."
  de_xuat: "Xác định phạm vi land độc lập với token trạng thái, theo run/attempt/head/context cần thiết, rồi kiểm disposition. Thêm ca hỗn hợp: một lời khai đạt và một lời khai bắt buộc thất bại/chưa đo; phân biệt rõ lịch sử hoặc context tùy chọn."

- id: G10
  severity: P2
  vi_tri: SPEC.md dòng 137–143, 176–177, 280–281, 481
  van_de: Sau khi thêm v2, `tom` luôn chọn luật hiện hành nên không thể sinh bằng chứng hợp lệ cho run lịch sử còn thuộc miền v1.
  bang_chung: "Hợp đồng quy định v2 có miền bắt đầu tại R, nhưng `tom` luôn dùng `LUAT_HIEN_HANH`; với run < R, tệp sinh mang hash v2 sẽ bị K2 bác `luat_ngoai_mien_hieu_luc`. A9b chỉ kiểm tệp v1 đã có, không kiểm đường sinh lại mà mục sửa hồ sơ cũ yêu cầu."
  de_xuat: "Cho `tom` chọn phiên bản theo miền chứa run, hoặc nhận phiên bản tường minh và kiểm miền; thêm ca khép vòng sinh lại run lịch sử sau khi bổ sung v2."

- id: G11
  severity: P2
  vi_tri: SPEC.md dòng 625–628
  van_de: Q7 dựa trên số liệu sai và suy không đúng rằng run Windows luôn nằm ngoài phạm vi lời khai land.
  bang_chung: "`python -B work/measure.py census` ⇒ 30 tệp provenance event `push`: 26 tệp `ci.yml` có 23 job và 4 tệp `launcher-windows.yml` có 2 job, không phải 28 tệp đều 23 job Ubuntu; readback xác nhận nhánh master. `python -B work/probes.py` còn tìm thấy run có Windows cùng `merge_commit` gốc tại pr1127, pr1128, pr945, pr957 và pr964."
  de_xuat: "Sửa số đếm theo đúng đơn vị tệp/workflow và nêu cách xử lý Windows ở cùng merge SHA; quyết định phạm vi bắt buộc theo context, không suy từ OS hoặc SHA khác nhau."

- id: G12
  severity: P2
  vi_tri: SPEC.md dòng 449–456, 492, 510
  van_de: A20b và T3 chưa có phép đo làm đúng ca đích đổi màu khi gỡ chốt được chỉ định.
  bang_chung: "A20a kiểm bảng có khóa bằng băm nội dung, A20b ghim bảng kỳ vọng; với bảng nguyên vẹn, bỏ tự kiểm băm lúc nạp vẫn để cả hai đạt vì không có đầu vào sai băm. T3 lại ghi đột biến phải làm A20 đỏ, trong khi dòng 451 đòi assertion của chính ca đích. Module chưa tồn tại nên đây là đối chiếu hợp đồng, không phải kết quả chạy mutant."
  de_xuat: "Thêm đầu vào bảng sai băm và assertion riêng kiểm việc từ chối khi nạp; thiết kế đột biến T3 làm đường dương của chính T3 thất bại, tách khỏi ca bảo vệ toàn vẹn sổ luật."

## Đã đo lại, khớp

- Băm đặc tả; HEAD/tree; clone không shallow; diff với base chỉ thêm đặc tả r3, 687 dòng.
- 64 giá trị = 44 measured + 1 passed + 3 not_measured + 1 chuỗi khác + 9 mapping + 6 list.
- 9 hồ sơ có tên trong L5, 8 còn khớp băm; L8 hồi tố 36 hồ sơ, đủ hàng `pr679`.
- `tu_do` 13 hồ sơ, 11 chỉ có dạng này; `merge_commit` gốc 118/123; chuẩn hóa tên khóa không thêm khóa mới.
- 28 hồ sơ chứa 34 provenance; 753 job `not_measured`, 1 `failed`; tập job/log khớp ở 34/34 tệp.
- L-7 hồi tố 49 hồ sơ: 32 có lời khai, 17 không có.
- Hai cổng hiện tại đều rc 0: `98 ĐẠT · 25/28 miễn trừ · 0 vi phạm`; `49/49 landed True đạt`.
- Ruff 0.17.3: nền rc 1, gồm 1 F841 và 2 F541 đúng vị trí đặc tả; năm tệp còn lại không lỗi F.
- Numstat lúc tạo các cặp nguồn/test: 393/656, 279/318, 140/263; ba phép kiểm OID ADR-0052/0053 khớp trên ref cục bộ.
- `ghep_buoc` ghép được 23/23 job từ REST và header thật; hai phụ thuộc canon hiện có nạp được độc lập. Chưa kiểm đường D2b hoàn chỉnh.
- `doctrine-scan`: rc 0, 10 tệp, 0 chỗ chép doctrine.

KET_LUAN: changes_requested