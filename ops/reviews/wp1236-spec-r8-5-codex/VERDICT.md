Còn **1 P2 chặn thi công và 2 P3**. Theo quyết định `6700073306`, cần dừng và trình chủ kho.

Review chỉ đọc tại HEAD `c1c0f63c7197f8d59c092219e61160495b51f6b2`, tree `a9ad2bcc9bab17242c88db386052f5dc106d98ef`; kho sạch, không gọi mạng. Phép kiểm tích hợp dùng mô hình generation 1 ghép K7-S, chưa phải mã triển khai r8. Chưa đo PowerShell thật.

Bằng chứng chính: [kiểm năm vế A14-S0](/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-5-codex/work/audit_s0.json), [kiểm qua `kiem`](/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-5-codex/work/audit_integration.json).

# VERDICT wp1236 r8 vòng 5

spec_sha256: 36bbcee68fcbbd5079a399f5cc8a8d00e179d6615272c7ed9754199da4b70b6c

## Finding vòng 4 của tôi

- I01 vòng 4 / J01: CÒN MỞ — bảy biến thể đã bị bắt, nhưng hai biến thể mới qua đủ năm vế A14-S0 và các đầu vào hành vi đã đo; xem I01 dưới.
- I02 vòng 4: ĐÓNG — đo đúng **24 hạt**, lấy **222/665** lượt chèn; phần ống chứa **666/1.989** thân phân biệt.
- J02: ĐÓNG — harness và đột biến kho sinh không đổi byte so vòng trước; chạy lại tham chiếu cho **0 nuốt lỗi, 0 không chạy**, vẫn kiểm nguyên byte.
- J03: ĐÓNG — A1/B1/C1/D1 giữ assertion cùng đột biến riêng; API đã xuất `GIOI_HAN`, B/C/D lấy hằng từ module.
- J04: ĐÓNG — đo `len(KT) = 35`.
- I01 vòng 2 / H03: ĐÓNG — số mới đúng **112 = 109 chạy shell + 3 chỉ grammar**; **42 rc 0 = 37 nuốt lỗi + 5 không gọi chương trình**, còn **67 rc khác 0**.
- I02 vòng 2: ĐÓNG — A20(e′) trả `mien_mo_khac_1`; bỏ chốt làm cả kiểm sổ và kết quả qua `kiem` đổi màu.
- H01: ĐÓNG — A14(i′) trả đúng một lý do đủ bốn phần; A15 đúng **43 lượt = 30/13**, **29 tên = 23/6**.
- H02: ĐÓNG — điều kiện lượt 2–4 tại dòng 834–835 khớp ADR-0052, được ADR-0055 giữ nguyên.
- H04: ĐÓNG — `(None, "pwsh")` vẫn phân biệt được thứ tự hai phép kiểm.
- G16: ĐÓNG — chạy lại `a03k_run_duong_nhanh_that` đạt assertion thiếu đúng tám job.
- G17: ĐÓNG — chạy lại `a21_pham_vi_land` đạt.
- G18: ĐÓNG — cộng số hạng được **2.248**, nằm trong **2.150–2.300**; trần **2.400** vẫn ghi là đề xuất cần chủ kho duyệt.
- G19: ĐÓNG — năm vế A20(f)–(i′) phân biệt năm đột biến qua kiểm sổ và `kiem`.
- G20: ĐÓNG — **29/29** provenance tại base r7 và **31/31** tại `d26b36f` khớp tập job; run sớm nhất là `40268583940`.

## Findings mới

- id: I01
  severity: P2
  vi_tri: SPEC.md:416–418,969,973,1030–1037
  van_de: Kế thừa I01 vòng 4: A14-S0 chưa ràng buộc callable thực tế với định nghĩa được kiểm AST, cũng chưa chứng minh dict tại lời gọi giữ nguyên dữ liệu workflow; đây là thiếu chốt nghiệm thu **chặn THI CÔNG**.
  bang_chung: `python3 -I -B work/audit_s0.py` ⇒ hai biến thể chuẩn hoá Unicode NFC — gán lại `cu_phap_run` sau định nghĩa, hoặc chuẩn hoá bản sao bước trước lời gọi — đều qua **5/5 vế**, **0 lệch/171 vế bảng**, **0 lệch/61.530 đầu vào sinh**. `python3 -I -B work/audit_integration.py` ⇒ cả hai qua **209/209** đầu vào lấy mẫu qua `kiem`; với `python ops/K.py` (`K` là U+212A), tham chiếu trả `not_measured`, cả hai biến thể trả `passed`. Các biến thể này vi phạm yêu cầu nguyên văn nhưng những phép nghiệm thu đã quy định không phát hiện được.
  de_xuat: Ràng buộc callable thực tế với duy nhất định nghĩa đã kiểm, bao gồm việc gán lại/decorator; đồng thời chốt đường lấy `run`/`shell` nguyên trạng từ workflow và sử dụng kết quả. Đòi cả hai biến thể làm chốt cấu trúc đỏ; thêm riêng nhân chứng Unicode vào bảng không đủ đóng lớp.

- id: I02
  severity: P3
  vi_tri: SPEC.md:973
  van_de: A14-S3b ghi “200 thân” nhưng công thức lấy mẫu hiện tại cho 209 đầu vào và, theo thứ tự kho sinh, chỉ chọn `shell` vắng; đây là lỗi mô tả/lấy mẫu, không chặn thi công độc lập.
  bang_chung: Lấy `corpus[::300]` theo vòng lặp `sinh_r8.py` cho **206 đầu vào, 206 thân riêng, tất cả shell=None**; cộng ba vế mới thành **209**, được chạy qua `kiem` trong `audit_integration.py`.
  de_xuat: Chốt thứ tự và công thức lấy mẫu, sửa số đếm tương ứng; lấy mẫu phân tầng nếu muốn ca này phủ cả ba giá trị `shell`.

- id: I03
  severity: P3
  vi_tri: SPEC.md:982–1007,1035–1037
  van_de: Quy tắc “mỗi đột biến một ca đích” còn mâu thuẫn giữa bảng disposition và đoạn giải thích; đây là lỗi hợp đồng bằng chữ, không chặn thi công độc lập.
  bang_chung: Bảng ghi m-S6 sửa lớp ký tự/cờ nhưng đích là `g_chu_so_unicode` của A14-S1; dòng 1035 lại quy định “đột biến SỬA HẰNG … → A14-S0”, trong khi dòng 1033 cũng xếp m-S6 vào nhóm sửa hằng.
  de_xuat: Chọn bảng disposition làm ánh xạ chuẩn duy nhất; phân biệt rõ ca đích với các ca khác cũng phát hiện đột biến.

## Đã đo lại, khớp

- A14-S0: bản gốc và bản đổi chú thích/docstring/định dạng đều đạt; bảy biến thể của hiện vật soạn đều đỏ. Chưa thấy chặn oan trong các thay đổi được phép này.
- m-S26 dạng `.strip()` bị vế 5 bắt; mẫu A14-S3b cũng phân biệt **2** đầu vào. m-S0f đỏ vì cờ, nhưng **0 lệch hành vi/61.530** đầu vào.
- A14-S6: **61.530 đầu vào / 2.647 nhận / 0 lệch / 0 nuốt / 0 không chạy**; khoảng **127 giây**, phù hợp ước hai phút. Quy định POSIX và chỉ chạy vế shell một lần đã được ghi rõ.
- **53/53** đột biến bảng đổi đúng ca đích; **91/91** đột biến kho sinh bị vế (a) bắt, lệch **24–1.440** đầu vào.
- Phép đo độc lập bằng Python/Bash thật: **792 lượt lệnh đơn + 48 lượt ống**, tất cả gọi chương trình hỏng và truyền mã lỗi.
- **7/7** băm hiện vật generation 1 khớp; **52/52** vế gốc bị từ chối. Năm JSON chạy lại khớp hiện vật soạn.
- `F-ok + VL-F` ⇒ `passed`; `F-ok-goc` ⇒ `not_measured`, đúng **13** lý do.
- Census: `d26b36f`/`fe84620` **30/24/6**, `8983e1b` **30/25/5**; Q-r8-5 đúng **0/39** lệch checkout/head và **28/28** blob workflow khớp.
- Generation 1 đúng **3 tệp, +1.620/−0**; danh mục mới cộng **164 đột biến**. Không phát hiện thêm số đo sai hay mâu thuẫn ADR trong Q-r8-1…5/ngân sách.
- `git diff --name-only 9607e3e...HEAD -- . ':!ops/specs/**' ':!ops/reviews/**'` ⇒ rỗng; merge master không đưa thay đổi ngoài hai phạm vi vào diff nhánh.

KET_LUAN: changes_requested
