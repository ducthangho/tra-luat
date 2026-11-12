Còn **1 P2 chặn thi công** và **1 P3 về mô tả**. Review chỉ đọc tại HEAD `2e5bce991423e51e539bd7ae57b3e9aeed4c902c`, tree `c1b4a760f325cb53c4569ae5de99a08c271a756a`; không gọi mạng, kho vẫn sạch. Phép kiểm tích hợp dùng mô hình generation 1 ghép K7-S, chưa phải mã triển khai r8. Chưa đo PowerShell thật.

# VERDICT wp1236 r8 vòng 4
spec_sha256: 5153cf17e3f5f73871fc0248db783919535b48df94b987f75594acd76924de8b

## Finding vòng 3 của tôi

- J01: CÒN MỞ — 91 đột biến cũ đã bị bắt, nhưng hai biến thể tiền xử lý giữ nguyên hằng và hai lời gọi `fullmatch` vẫn không lệch trên 168 vế bảng cùng 61.530 đầu vào sinh; xem I01.
- J02: ĐÓNG — harness giữ nguyên byte, chạy Bash thật và tách ba lớp; chạy lại khớp **9 nuốt / 40 không chạy / 42 chỉ lệch tham chiếu**.
- J03: ĐÓNG — B1/C1/D1 đã có assertion `GIOI_HAN` và m-B1b/m-C1b/m-D1b; A1 bổ sung CLI `kiem-ho-so` cùng m-A1c.
- J04: ĐÓNG — đo `len(KT) = 35`, khớp bản sửa.
- I01 / H03: ĐÓNG — **109 = 106 chạy shell (41 rc 0 + 65 rc khác 0) + 3 chỉ grammar**.
- I02: ĐÓNG — A20(e′) trả `mien_mo_khac_1`; bỏ chốt đếm miền mở làm cả assertion trực tiếp và qua `kiem` đổi màu.
- H01: ĐÓNG — A14(i′) đúng một lý do đủ bốn phần; A15 đúng **43 lượt = 30/13**, **29 tên = 23/6**.
- H02: ĐÓNG — điều kiện cấp lượt 2–4 tại dòng 814–815 khớp ADR-0052.
- H04: ĐÓNG — `(None, "pwsh")` trả hai lý do khác nhau khi đảo thứ tự kiểm.
- G16: ĐÓNG — ca trên run `41397205258` đạt assertion thiếu đúng tám job bắt buộc.
- G17: ĐÓNG — ca `a21_pham_vi_land` chạy lại đạt, giữ phân biệt workflow và sự kiện.
- G18: ĐÓNG — cộng các số hạng ước mới được **2.185**, nằm trong **2.050–2.200**; trần đề xuất **2.300** vẫn cần chủ kho duyệt.
- G19: ĐÓNG — năm vế A20(f)–(i′) phân biệt năm đột biến qua cả kiểm sổ và `kiem`.
- G20: ĐÓNG — **29/29** provenance tại base r7 và **31/31** tại `d26b36f` khớp tập job; run sớm nhất vẫn `40268583940`.

## Findings mới

- id: I01
  severity: P2
  vi_tri: SPEC.md:384–388,949,1007–1012
  van_de: Kế thừa J01: A14-S0 khóa hằng nhưng chưa khóa logic sử dụng hằng, nên chưa đóng lớp “cài đặt khác mà tưởng tương đương”; đây là thiếu chốt nghiệm thu chặn THI CÔNG, không chỉ câu chữ.
  bang_chung: `python3 -I -B work/audit_s0.py` ⇒ hai biến thể bỏ BOM đầu chuỗi hoặc chuyển chữ đầu lệnh thành chữ thường đều giữ nguyên sáu hằng/flags, chỉ tham chiếu `RE_DON`, `RE_ONG`, chỉ gọi hai `fullmatch`, không thêm regex; cả hai có **0 lệch/168 vế bảng** và **0 lệch/61.530 đầu vào sinh**. Tuy nhiên chúng nhận lần lượt chuỗi có BOM trước `python ops/x.py` và `Python ops/x.py`, trong khi tham chiếu từ chối. `audit_fixture.py` xác nhận qua mô hình `kiem`: biến thể trả `passed`, tham chiếu trả `not_measured`. Đối chứng chỉ đổi `RE_ONG.fullmatch` thành `.match` bị bộ hành vi bắt (**9.816 lệch**), nhưng hai biến thể tiền xử lý vẫn sống.
  de_xuat: Chốt phần grammar và toàn thân `cu_phap_run` bằng AST tham chiếu, bỏ thuộc tính vị trí; kiểm cả kiểu/binding của hai regex để không nhận wrapper chỉ giả `pattern`/`flags`. Thêm đột biến tiền xử lý, đổi phương thức và wrapper, đòi A14-S0 tự đỏ. Giữ ca hành vi kiểm đường gọi qua `kiem`. Hệ quả cần ghi rõ: refactor phần đã khóa phải cập nhật hợp đồng; comment và định dạng không nên làm ca đỏ.

- id: I02
  severity: P3
  vi_tri: SPEC.md:955; sinh_r8.py:63,72–73
  van_de: Mô tả kho sinh chưa khớp hiện vật về số hạt và cách lấy mẫu chèn ký tự trong ống; đây là lỗi mô tả, không chặn thi công độc lập.
  bang_chung: `python3 -I -B work/audit_facts.py` ⇒ **24 hạt = 4 + 16 + 4**, không phải 34; nhánh chèn vào ống có điều kiện `i % 3 == 0`, kho chứa **666/1.989** thân phân biệt của phép chèn đầy đủ vào ba vị trí, thiếu **1.323**.
  de_xuat: Sửa 34 thành 24 và khai rõ phép lấy mẫu trong ống; nếu muốn đòi chèn đầy đủ thì bỏ lấy mẫu và đo lại các số phụ thuộc. Khóa metadata bằng assertion để mô tả không trôi tiếp.

## Đã đo lại, khớp

- A14-S6: **61.530 / 2.647 / 0 lệch / 0 nuốt / 0 không chạy**.
- **91/91** đột biến kho sinh bị bắt; lệch **24–1.440** đầu vào mỗi cái; phân loại **9/40/42**. Năm tệp JSON chạy lại khớp nội dung hiện vật cung cấp.
- **53/53** đột biến bảng đổi đúng ca đích; **109/109** vế âm bị từ chối; **7/7** vế dương gọi chương trình hỏng và truyền lỗi.
- Phép đo độc lập trong môi trường sạch: **792 lượt lệnh đơn + 48 lượt ống ba thành phần**, Python/Bash thật; tất cả gọi chương trình hỏng và trả rc khác 0.
- **7/7** băm hiện vật generation 1 khớp; **52/52** vế gốc bị grammar từ chối.
- `F-ok + VL-F` ⇒ `passed`; `F-ok-goc` ⇒ `not_measured`, đúng **13** lý do K7-S.
- Census: `d26b36f`/`fe84620` **30/24/6**, `8983e1b` **30/25/5**; **14/24** bước được nhận có đối số.
- Q-r8-5: **0/39** provenance lệch checkout/head; **28/28** workflow blob khớp.
- Generation 1: **3 tệp, +1.620/−0**; danh mục mới cộng đúng **158 đột biến**; `luat_sha256` giữ nguyên.
- OID land ADR-0052/0053 khớp ba phép kiểm trên lịch sử/ref cục bộ; không xác minh độ mới của remote qua mạng.

KET_LUAN: changes_requested
