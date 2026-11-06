Review tại HEAD `cf0ee8b1581c13aa3ab5377c444a43fe56b84b10`, tree `851cec7ad4a0325213b3b8b1d6991f3447087d41`. Không gọi mạng; kho vẫn sạch. Phép kiểm tích hợp dùng grammar tham chiếu ghép vào bản sao `508d678` trong `work/`, không phải mã triển khai r8. Chưa đo PowerShell thật vì thiếu `pwsh`.

# VERDICT wp1236 r8 vòng 1
spec_sha256: 2a8c42e1d711e3c09281df6d36eb8c5a698c577ebad688e52e9ce0583c5828ff

## Finding vòng 7 của tôi

- G16: ĐÓNG — `duong_nhanh` tiếp tục ngoài phạm vi, chuyển sang #1257 và giữ hệ quả về waiver.
- G17: ĐÓNG — D2b vẫn dùng chung `la_run_land`, đòi `ci.yml` và `push`.
- G18: ĐÓNG — Trần A1 generation 2 được khai riêng, chỉ hiệu lực khi chủ kho duyệt băm chính revision này.
- G19: CÒN MỞ — P3: A20 tại dòng 878 vẫn chỉ yêu cầu các vế a–e, chưa bổ sung ca và đột biến riêng cho ba điều kiện kiểm sổ đã báo.
- G20: CÒN MỞ — P3: dòng 1184 vẫn ghi run sớm nhất `40842340568`; `python3 -I -B work/metadata_r8.py` đo lại trên `b796259` được **40268583940**, thuộc pr945.

## Findings mới

- id: H01  
  severity: P2  
  vi_tri: SPEC.md:871–872, đối chiếu 422–424  
  van_de: Kỳ vọng của A14(i′) và A15 khiến triển khai đúng hợp đồng vẫn trượt nghiệm thu.  
  bang_chung: `python3 -I -B work/contracts_r8.py` xác nhận A14(i′) trả `cu_phap_run:ong_khong_bash_tuong_minh:gate-packet-loop (ubuntu-latest):packet-loop selftest`, còn đặc tả thiếu thành phần tên job. Với A15, ghép đúng bước REST success cho ra **43 lượt bước: 30 nhận/13 chặn**, tương ứng **29 tên: 23 nhận/6 chặn**. Số **24/6** chỉ đúng khi quét toàn bộ YAML, tính thêm `tl selftest (luot PR — khong sinh bang chung)` không chạy trong run push này.  
  de_xuat: Sửa đầy đủ lý do A14(i′); tách phép kiểm A15 theo REST thành 43 lượt/29 tên và phép kiểm toàn YAML thành 30 tên, ghi kỳ vọng riêng cho từng tập.

- id: H02  
  severity: P2  
  vi_tri: SPEC.md:781, `tran_loi_goi_codex_A1_gen2.dieu_kien_luot`  
  van_de: Điều kiện cấp lượt 2–4 được nới so với ADR-0052 nhưng lại ghi là tuân ADR ấy.  
  bang_chung: Đặc tả cho phép khi “còn P0–P2 hoặc cần xác minh bản vá”; ADR-0052 dòng 23–25 chỉ cho phép khi còn **P0/P1, finding cắt ngang, hoặc cần xác minh bản vá**. Một P2 đơn lẻ chưa vá, không cắt ngang, đủ điều kiện theo r8 nhưng không đủ theo ADR; ADR-0055 giữ nguyên điều kiện này.  
  de_xuat: Dẫn đúng điều kiện ADR-0052; nếu muốn nới thì khai rõ thành ngoại lệ cần chủ kho quyết định.

- id: H03  
  severity: P3  
  vi_tri: SPEC.md:431–435  
  van_de: “36 vế nuốt lỗi thật” nhầm số lần thoát 0 với số lần chương trình lỗi thực sự được gọi rồi bị che mã thoát.  
  bang_chung: `python3 -I -B work/shell_measure.py`, có dấu xác nhận chương trình lỗi đã chạy, cho **36 rc=0 nhưng chỉ 31 có thực thi chương trình lỗi**. Năm vế còn lại là `g_python_c`, `g_python_stdin`, `g_lenh_ngoai_ds`, `g_python_c_tran`, `g_bash_c_tran`.  
  de_xuat: Ghi riêng 36 vế thoát 0 và 31 vế nuốt lỗi thật; thêm kiểm chứng đã chạy chương trình lỗi vào phép đo.

- id: H04  
  severity: P3  
  vi_tri: SPEC.md:936–938, đối chiếu 354–359  
  van_de: Đổi thứ tự kiểm kiểu `run` và kiểm `shell` không tương đương theo hợp đồng trả lý do.  
  bang_chung: `python3 -I -B work/mutation_audit.py`: đầu vào `(None, "pwsh")` trả `lenh_ngoai_cu_phap` theo thứ tự quy định, nhưng trả `shell_ngoai_cu_phap` khi đảo thứ tự; cả 98 vế hiện có đều không phân biệt được đột biến này.  
  de_xuat: Bỏ kết luận tương đương; bổ sung đầu vào đồng thời sai kiểu `run` và ngoài tập `shell`, kèm đột biến đảo thứ tự.

## Đã đo lại, khớp

- **Không tìm thấy phản ví dụ mất mã thoát trong phạm vi đã chạy:** 429 lệnh đơn và 7 pipeline được nhận đều trả lỗi; có kiểm ký tự `= : - . /`, đối số `--`, đường dẫn và LF cuối.
- Corpus tham chiếu: **91 vế âm bị từ chối, 7 vế dương truyền lỗi**; `g_* = 39`, `kt_* = 24`.
- **40/40 đột biến** đổi kết quả đúng ca đích; m-S12′ làm đỏ đúng hai vế pipeline dương.
- Census YAML: `d26b36f` và `fe84620` **30/24/6**; `8983e1b` **30/25/5**.
- `F-ok + VL-F` ⇒ **passed**; `F-ok-goc` ⇒ **not_measured**, đúng **13 lý do trên 10/22 job J**.
- `chan_k7` chặn ba khóa môi trường `BASH_ENV`, `SHELLOPTS`, `BASH_FUNC_python%%` ở cả ba mức trước grammar; 19 ca kế thừa được chọn chạy trên mô hình đều đạt.
- `luat_sha256` giữ nguyên **ee0f2db86fc579ff236ff0417de0658a184a4ed4871468c90a2f0c42417037cc**; **16 nhóm bắt số thuộc 13 mẫu**.
- `git diff --numstat 08bcb51...508d678`: **539 + 1080 + 1 = 1620 dòng thêm**, đúng ba tệp; phép cộng dự toán ra **1845**, nằm trong khoảng 1750–1900, vẫn là ước lượng.

KET_LUAN: changes_requested
