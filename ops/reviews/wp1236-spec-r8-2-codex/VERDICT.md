Review tại HEAD `a52954721ebeb29cff9e58e3fdade17d7b565929`, tree `cff10985b8b0640aa3760d3c86e5db65d1d91579`. Không gọi mạng; kho vẫn sạch. Phép kiểm tích hợp dùng bản sao generation 1 ghép grammar tham chiếu trong `work/`, không phải mã triển khai r8. Chưa đo PowerShell thật vì thiếu `pwsh`.

# VERDICT wp1236 r8 vòng 2
spec_sha256: a37c41a37dc4cdebabfbfa50777cc4bc3a5352f0618e5bde31945a0bceb5619c

## Finding vòng 1 của tôi

- H01: ĐÓNG — `audit_integration.py` xác nhận A14(i′) đúng một lý do đủ bốn phần; `audit_metadata.py` đo A15 đúng **43 lượt = 30/13**, **29 tên = 23/6**.
- H02: ĐÓNG — Điều kiện lượt 2–4 tại dòng 800–801 khớp ADR-0052: còn P0/P1, finding cắt ngang hoặc cần xác minh bản vá.
- H03: CÒN MỞ — P3: phép tách **41 = 36 + 5** đã đúng, nhưng lời khai thực thi của 68 vế còn lại vẫn gộp ba vế không chạy; xem I01.
- H04: ĐÓNG — `audit_remaining.py` xác nhận m-S19 đổi lý do của `(None, "pwsh")`; ca mới phân biệt được thứ tự kiểm.
- G16: ĐÓNG — `audit_remaining.py` đo run `41397205258` vẫn `not_measured`, thiếu đúng tám job; `duong_nhanh` tiếp tục chuyển sang #1257.
- G17: ĐÓNG — Bốn tổ hợp workflow/event đã đo: chỉ `ci.yml` + `push` được `la_run_land` nhận; D2b/D10 giữ điều kiện ấy.
- G18: ĐÓNG — Dự toán cộng được **1955**, trong khoảng 1850–2000; trần 2050 khai riêng và chỉ hiệu lực khi chủ kho duyệt băm hiện hành.
- G19: ĐÓNG — Năm vế A20(f)–(i′) phân biệt được năm đột biến tương ứng, kể cả qua lý do `so_luat_hong` của `kiem`.
- G20: ĐÓNG — Đo lại **29/29** provenance trên `b796259`; run sớm nhất đúng **40268583940**, thuộc pr945.

## Findings mới

- id: I01
  severity: P3
  vi_tri: SPEC.md:440,448
  van_de: Tiếp H03: câu “mỗi vế chạy THẬT” và “68 vế còn lại Bash không nuốt lỗi” tính cả ba vế harness không chạy.
  bang_chung: `python3 -I -B work/audit_metadata.py` ⇒ `rc_nonzero: 65`; `rc_bash: null` ở `g_pwsh_shell`, `g_run_khong_phai_chuoi`, `g_run_khong_phai_chuoi_pwsh`.
  de_xuat: Ghi rõ 109 vế được phân loại grammar; 106 vế chạy shell gồm 41 rc 0 và 65 rc khác 0; ba vế còn lại chỉ kiểm grammar.

- id: I02
  severity: P3
  vi_tri: SPEC.md:222,903 — chốt đúng một miền mở và A20(e)
  van_de: A20 chưa có ca và đột biến riêng phân biệt việc bỏ chốt “đúng một miền mở”, vì hai miền mở đồng thời cũng vi phạm chốt miền chồng nhau.
  bang_chung: `python3 -I -B work/audit_a20_open_domain.py` ⇒ bỏ chốt đếm miền mở vẫn thỏa các assertion được đặc tả yêu cầu ở A20(a)–(i′); A20(e) vẫn có `so_luat_hong` nhờ `mien_chong`, còn đầu vào không có miền mở đổi từ `["mien_mo_khac_1"]` thành `[]`.
  de_xuat: Thêm vế mọi miền đều đóng, băm và miền hợp lệ, kèm đột biến bỏ chốt đếm miền mở; đòi chính vế ấy đỏ.

## Đã đo lại, khớp

- **109/109** vế âm: **106/2/1** theo lý do; **41 rc 0 = 36 nuốt lỗi + 5 không gọi chương trình lỗi**; **7/7** vế dương thực thi và truyền lỗi.
- **53/53** đột biến tham chiếu đổi đúng ca đích; m-S12′ làm đỏ đúng hai pipeline dương.
- **7/7** băm hiện vật gốc khớp; **52/52** vế generation 1 bị từ chối cả trực tiếp và qua mô hình `kiem`.
- **468 lệnh đơn + 12 pipeline** được nhận trong môi trường sạch đều thực thi chương trình và trả lỗi; chưa tìm thấy phản ví dụ nuốt lỗi.
- `F-ok` dùng commit con của `fe84620` ⇒ `passed`; `F-ok-goc` ⇒ đúng **13 lý do trên 10/22 job J**. m-S16, m-S17, m-S20 và m-A15c phân biệt được ca đích.
- Census YAML: `d26b36f`/`fe84620` **30/24/6**; `8983e1b` **30/25/5**. **22/22** job J có `setup-python` trước bước luật.
- `91686a6` thực sự gộp bước updater mà `36ee6cb` thêm trước đó; mô tả R4a/R4b khớp lịch sử.
- Generation 1: **3 tệp, +1620/−0**; phép cộng dự toán **1955**, trần đề xuất **2050**.
- `luat_sha256` giữ nguyên; **16 nhóm bắt số thuộc 13 mẫu**. Không còn finding P0/P1/P2.

KET_LUAN: approve
