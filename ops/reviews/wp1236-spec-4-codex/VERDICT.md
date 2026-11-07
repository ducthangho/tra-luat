Đã review tại HEAD `deacebf4b590e1dc78706d7374090306d66cd9cf`, tree `ad8b3803d4cfca2d4fbf3b76ed1ebf563146e55f`. Không gọi mạng; đối chiếu 12.375 tệp không có thay đổi, Git sạch.

Bằng chứng: [số đếm](work/census.json), [phản thực tế K7](work/k7.json), [probe readback và A22](work/read_only_probes.txt). Module mới chưa tồn tại: phép đo K7 mô phỏng vị từ của đặc tả; nhận xét về D8 là đối chiếu hợp đồng. Không kiểm được nguồn N1/N2 ngoài các ref được cấp.

G05 vẫn cần sửa tại phần `owner_waived` và D2b: readback phải chứng minh **nội dung miễn trừ đúng phạm vi** theo §10.2.3. Comment duyệt merge hoặc chỉ nhắc SHA không đủ. Cần thêm ca âm dùng comment có thật, đúng actor/SHA nhưng không miễn Gate output, cùng ca dương có waiver đủ context/OS, lý do, phạm vi/hạn và điều kiện thay thế.

# VERDICT wp1236 r4 vòng 4

spec_sha256: c8e79de93545c6003e36162f03465213c4d97566a32156faf7a1ba69042b519b

## Finding vòng 3 của tôi

- F01: ĐÓNG — K5 giữ đối chiếu danh tính và chọn luật từ provenance.
- F02: ĐÓNG — Neo vẫn bắt buộc attempt, không thừa kế và phân biệt head land.
- F03: ĐÓNG — Ghép bước theo tên REST/YAML, không còn giả định `Run <CMD>`.
- F04: ĐÓNG — K3 bác T/J rỗng và tập chỉ có `chuan-bi`.
- F05: ĐÓNG — Định nghĩa lời khai và các số 64, 8/9, 36 vẫn khớp.
- F06: ĐÓNG — Bốn loại dấu hiệu vẫn biểu diễn được ngữ nghĩa cần kiểm.
- F07: ĐÓNG — C1–C3 và quy tắc không tính đột biến tương đương vẫn được giữ.
- F08: ĐÓNG — Cột neo giới hạn đúng phạm vi; K1 tiếp tục bác head rút gọn.
- G01: ĐÓNG — Các bước luật ghép được với dữ liệu REST/YAML thật.
- G02: ĐÓNG — Thiếu attempt, thừa kế neo và chỉ có bằng chứng pre-merge vẫn bị chặn.
- G03: ĐÓNG — Bảng giá trị, miễn trừ theo băm và hàng `pr679` khớp.
- G04: ĐÓNG — A4a canh trực tiếp phép so tên.
- G05: CÒN MỞ — **P2**, SPEC.md dòng 238–246 và 290 chỉ đòi body chứa SHA; `python -B work/read_only_probes.py` xác nhận readback `pr1130` thỏa cả bốn điều kiện nhưng nội dung chỉ duyệt head sau merge, không miễn Gate output đúng phạm vi.
- G06: ĐÓNG — K2 vẫn chặn luật ngoài miền hiệu lực.
- G07: ĐÓNG — Lời khai phụ `not_measured` của `launcher-windows.yml` được phép qua B8.
- G08: ĐÓNG — Phản thực tế trên `F-that` cho 43 bước thuộc 22 job không bị `chan_k7` chặn; vị từ cũ chặn 19 job.
- G09: ĐÓNG — Phạm vi land độc lập token; B9 và B11 kiểm lời khai hỗn hợp và thiếu neo.
- G10: ĐÓNG — `tom` chọn phiên bản theo miền chứa run, có T6 kiểm sinh lại bằng chứng lịch sử.
- G11: ĐÓNG — Số provenance push khớp; K3 và phạm vi land đã nêu rõ cách xử lý Windows.
- G12: ĐÓNG — A20c–e bổ sung đầu vào sổ lỗi và T3 có đột biến làm chính ca đích đỏ; thiếu sót mới cùng lớp nghiệm thu ghi ở G14–G15.

## Findings mới

- id: G13
  severity: P2
  vi_tri: SPEC.md dòng 98–106
  van_de: Hai hàng `danh_gia` và `tom` không khớp đơn vị đếm mà r4 công bố.
  bang_chung: "`python -B work/measure.py census` ⇒ `danh_gia=[6,2]`, `tom=[7,3]`, `tu_do=[13,11]`, thay vì `[6,4]`, `[4,4]`, `[13,11]`; các cặp là tổng hồ sơ/chỉ có dạng ấy. Lời khai dương tại pr1130, pr1138 và pr1142 trích cả tệp `danh_gia` lẫn tệp khớp định dạng `tom`; pr1127 còn trích tệp dạng tự do."
  de_xuat: Sửa số thành 6/2, 7/3, 13/11 và giữ danh sách hồ sơ đối chiếu; nếu muốn loại trích dẫn phụ thì định nghĩa lại phạm vi và đo lại đồng nhất cả ba hàng.

- id: G14
  severity: P2
  vi_tri: SPEC.md dòng 526–527
  van_de: A22 kiểm tiền tố tên trong `sys.modules` nên có thể báo rỗng dù đã nạp tệp phụ thuộc bị cấm.
  bang_chung: "`python -B work/read_only_probes.py` ⇒ sau `import ops.kiem_ho_so_land`, biểu thức A22 trả `[]` trong khi `Actually loaded: True`; nạp bằng `spec_from_file_location`/`exec_module` cũng tạo checker hoạt động nhưng biểu thức vẫn trả `[]`."
  de_xuat: Kiểm danh tính theo đường dẫn tệp và theo dõi việc thực thi loader, bao gồm module không được đăng ký trong `sys.modules`; thêm đối chứng cho import dạng package và nạp trực tiếp bằng đường dẫn.

- id: G15
  severity: P2
  vi_tri: SPEC.md dòng 475 và 592
  van_de: Đột biến m-D8a không làm chính ca D8 đổi màu theo hợp đồng hiện tại.
  bang_chung: "D8 chỉ có đầu vào thiếu `ops/ci_provenance.py` trên ref và đòi rc 8; m-D8a chỉ chép module vẫn thiếu phụ thuộc, nên lỗi nạp cũng phải ra rc 8 theo dòng 294–295. Ca đích tiếp tục đạt; đây là đối chiếu hợp đồng, chưa chạy mã mới."
  de_xuat: Khôi phục vế dương của D8 với đủ ba tệp canon để m-D8a làm nó thất bại, hoặc chuyển đích đột biến sang D1; giữ vế thiếu tệp để kiểm m-D8b và không tính lỗi nạp vô can thành assertion giết đột biến.

## Đã đo lại, khớp

- Băm SPEC, HEAD/tree, clone không nông; diff với `3163f4d` chỉ thêm đặc tả r4.
- 118/123 hồ sơ có `merge_commit` gốc; hai hồ sơ nhiều PR có H lần lượt gồm **3** và **2** head; pr721/pr732 landed nhưng H rỗng.
- 30 provenance push = 26 `ci.yml` × 23 job + 4 `launcher-windows.yml` × 2 job.
- `pr1231`: T = 23, J = 22; ghép được 43 bước luật, không lệch tập khóa `env:` giữa `fe84620` và `3163f4d`.
- `CHECK_BAT_BUOC` đúng dòng 2402, gồm năm job `ci.yml` trên Ubuntu.
- 34 provenance thuộc 28 hồ sơ; 753 job `not_measured`, 1 `failed`; tập job/log khớp 34/34; không trùng tên bước trong 754 job.
- 64 giá trị lời khai; L8 hồi tố 36 hồ sơ; L-7 hồi tố 49 hồ sơ, gồm 32 có lời khai và 17 không có.
- Hai cổng nền rc 0: `98 ĐẠT · 25/28 miễn trừ · 0 vi phạm` và `49/49 landed True đạt`; `doctrine-scan` rc 0.

KET_LUAN: changes_requested