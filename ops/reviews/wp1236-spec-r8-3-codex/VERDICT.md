Review chỉ đọc tại HEAD `09cc1a225169a1ed22cca4aaab5d74faff72e998`, tree `65234f92f718cbb0bcf144054331fe5e6e67662e`. Không gọi mạng; kho vẫn sạch. Script và kết quả đo nằm trong `work/`. Phép kiểm tích hợp dùng bản sao generation 1 ghép grammar tham chiếu, chưa phải mã triển khai r8. Chưa đo PowerShell thật.

# VERDICT wp1236 r8 vòng 3

spec_sha256: 885017a688ae72fb479ee5e6234dd483f27182285b1f9d8a5b1ee3ee1adad1ee

## Finding vòng 2 của tôi

- I01 / H03: ĐÓNG — `audit_metadata.py` xác nhận **109 = 106 chạy shell (41 rc 0 + 65 rc khác 0) + 3 chỉ kiểm grammar**, đúng câu sửa.
- I02: ĐÓNG — `audit_a20_open_domain.py`: A20(e′) cho `["mien_mo_khac_1"]`; bỏ chốt đếm miền mở cho `[]`, assertion chuyển từ đạt sang trượt.
- H01: ĐÓNG — đo lại A14(i′) đúng một lý do đủ bốn phần; A15 đúng **43 lượt = 30/13**, **29 tên = 23/6**.
- H02: ĐÓNG — điều kiện cấp lượt 2–4 tại dòng 809–810 khớp ADR-0052.
- H04: ĐÓNG — `(None, "pwsh")` phân biệt được thứ tự kiểm qua hai lý do khác nhau.
- G16: ĐÓNG — run `41397205258` vẫn `not_measured`, thiếu đúng tám job bắt buộc.
- G17: ĐÓNG — bốn tổ hợp workflow/event đã đo; chỉ `ci.yml` + `push` được nhận là run land.
- G18: ĐÓNG — cộng các số hạng ước lượng được **2022 ≈ 2020**, nằm trong **1900–2050**; trần đề xuất **2150** vẫn đòi chủ kho duyệt băm hiện hành.
- G19: ĐÓNG — năm vế A20(f)–(i′) tiếp tục phân biệt năm đột biến tương ứng qua `kiem_so_luat` và `kiem`.
- G20: ĐÓNG — **29/29** provenance tại base r7 và **31/31** tại `d26b36f`; run sớm nhất vẫn `40268583940`.

## Findings mới

- id: J01
  severity: P2
  vi_tri: SPEC.md:949,995–999
  van_de: A14-S6 chưa đóng lớp lỗi grammar vì chèn ký tự chỉ trên mẫu `python`, còn tổ hợp ống chỉ có hai thành phần.
  bang_chung: `python3 -I -B work/audit_corpus.py` ⇒ **52/52 đột biến** nới từng ký tự của `P` riêng cho nhánh `bash` hoặc `pwsh` có **0 lệch trên 168 vế cũ và 11.838 đầu vào sinh**; tập được nhận không đổi nên phép (b) cũng không bắt được. Đột biến chỉ kiểm thành phần đầu/cuối của ống cũng sống; đối chứng vô hại có `true` ở giữa ba thành phần bị tham chiếu từ chối nhưng được đột biến nhận. Kho sinh được nhận chỉ có **36 lệnh đơn + 50 ống hai thành phần**.
  de_xuat: Sinh theo từng nhánh `DANG`, từng vị trí `P`/`W` và từng vị trí trong ống, gồm thành phần giữa; đo các đột biến cục bộ theo nhánh. Giữ đây là cùng lớp thiếu độ phủ đã được dòng 1435 đếm hai lần và xét lại phương pháp theo ADR-0037, thay vì chỉ thêm các vế reviewer vừa chỉ.

- id: J02
  severity: P2
  vi_tri: SPEC.md:949,997; sinh_r8.py:20–38,82–85
  van_de: Phép (b) thay đổi cú pháp đang cần đo trước khi chạy shell, đồng thời gộp “chưa chạy chương trình” thành “nuốt lỗi”.
  bang_chung: `python3 -I -B work/audit_harness.py` ⇒ với đầu vào sẵn có của m-S15[27], harness trả **rc 1, DA_CHAY=True**, nhưng thân nguyên byte trả **rc 2, DA_CHAY=False**, lỗi dấu nháy chưa đóng; m-S15[22] tương tự. Nguyên nhân là đổi cả token đường dẫn sang `ops/_t*.py`, xóa luôn ký tự thử. Trong nhóm **13/32**, chỉ **6** đột biến có lần `rc=0` và chương trình đã chạy; **7** còn lại gồm **252 phép chạy rc khác 0, DA_CHAY=False**. Lỗi này tái hiện trên nhánh `python`, độc lập với chương trình giả `bash`/`pwsh`.
  de_xuat: Giữ nguyên cú pháp và ký tự thử khi bố trí chương trình hỏng cho từng thành phần; thêm tự kiểm đối chiếu thân gốc với thân thực thi. Tách số đo “nuốt lỗi”, “không chạy” và lỗi cú pháp; sửa lời khai 13/32 tương ứng.

- id: J03
  severity: P3
  vi_tri: SPEC.md:342–344; bảng nghiệm thu B/C/D
  van_de: Nghĩa vụ in lại dòng `GIOI_HAN` tại ba cổng B/C/D chưa có assertion và đột biến riêng theo L3.
  bang_chung: A1 tại dòng 892 đã đòi đúng một dòng và có m-A1b; các bảng B/C/D chỉ đòi trạng thái, mã thoát hoặc lý do, không đòi nội dung dòng này.
  de_xuat: Bổ sung kiểm stdout tại đường CLI thành công của từng cổng và đột biến bỏ dòng tại chính cổng đó.

- id: J04
  severity: P3
  vi_tri: SPEC.md:949
  van_de: Số ký tự dùng để chèn được khai là 37 nhưng hiện vật thực tế có 35.
  bang_chung: `python3 -I -B work/audit_corpus.py` ⇒ `KT_count: 35`; số **11.838** được sinh từ tập 35 ký tự ấy.
  de_xuat: Sửa thành 35, hoặc bổ sung hai ký tự còn thiếu rồi đo lại toàn bộ số đếm.

## Đã đo lại, khớp

- Kho sinh: **11.838 lượt đầu vào, 86 nhận, 0 lệch, 0 cờ lỗi của harness**; giới hạn phép đo nêu tại J02.
- **32/32** đột biến bị phép (a) bắt, mỗi đột biến lệch **30–150** đầu vào; **53/53** đột biến cũ đổi đúng ca đích.
- Grammar trong môi trường sạch: **468 lệnh đơn + 12 ống** chạy Python/Bash thật đều gọi chương trình và truyền lỗi; chưa tìm thấy phản ví dụ nuốt lỗi.
- **7/7** băm hiện vật gốc khớp; **52/52** vế generation 1 bị từ chối trực tiếp và qua mô hình `kiem`.
- `F-ok` với commit con áp `VL-F` ⇒ `passed`; `F-ok-goc` ⇒ **13 lý do trên 10/22 job**. Câu thay G05 đã rõ.
- Census YAML: `d26b36f`/`fe84620` **30/24/6**, `8983e1b` **30/25/5**; đúng hai bước luật khác nhau; **14/24** bước được nhận có đối số.
- Action theo tag: checkout **9**, setup-python **8**, upload-artifact **3**, download-artifact **2**; **0** ghim SHA. Vị trí ghi `GITHUB_PATH` đúng **:193/:226**.
- Q-r8-4(c): **0/30** bước khai `sh`, tác động **22/22** job. Q-r8-5: **0/39** provenance lệch checkout/head, **28/28** blob workflow khớp.
- Generation 1 đúng **3 tệp, +1620/−0**; `luat_sha256` giữ nguyên.

KET_LUAN: changes_requested
