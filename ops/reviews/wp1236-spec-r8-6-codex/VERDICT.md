Còn **1 P2 chặn thi công và 1 P3**. Theo quyết định `6700574797`, chuyển sang **HUMAN AUDIT của chủ kho**, không mở thêm vòng review.

Review tại HEAD `5244493221624ca9f521ff2af6cd0444746818a6`, tree `da09cb0ce78511ce951316412ac4eb113b9cd6d3`. Không gọi mạng; 13.085 tệp trong checkout không đổi nội dung, kho sạch. Phép đo tích hợp dùng bản sao generation 1 ghép K7-S, chưa phải mã generation 2; chưa đo PowerShell thật.

# VERDICT wp1236 r8 vòng 6

spec_sha256: 7c85e68e1ac5a5875925a4a48b7c5b691b146bbdcf4d740e274eb29ff09ab1c4

## Finding vòng 5 của tôi

- I01 vòng 5 / I01 vòng 4 / J01: CÒN MỞ — các biến thể đã nêu bị bắt, nhưng `inspect.getsource(f)` vẫn có thể kiểm nguồn khác với mã thực thi; xem I01 dưới.
- I02 vòng 5: ĐÓNG — đo đúng **325 = 112 + 7 + 206**; mẫu có **69 vắng, 69 sh, 68 bash**, 8 đầu vào được nhận.
- I03 vòng 5: ĐÓNG — bảng disposition được chỉ định là ánh xạ chuẩn duy nhất; m-S6 giữ ca đích `g_chu_so_unicode`.
- I02 vòng 4: ĐÓNG — đo lại **24 hạt**, **222/665** lượt chèn được lấy mẫu.
- J02: ĐÓNG — harness không đổi byte từ vòng trước; chạy lại cho **0 nuốt lỗi, 0 không chạy**, có assertion nguyên byte.
- J03: ĐÓNG — A1/B1/C1/D1 giữ yêu cầu và đột biến riêng; API nay xuất `GIOI_HAN_K7S`, tách khỏi hằng cũ.
- J04: ĐÓNG — đo lại `len(KT) = 35`.
- I01 vòng 2 / H03: ĐÓNG — **112 vế = 109 chạy shell + 3 chỉ grammar**; **42 rc 0 = 37 nuốt lỗi + 5 không gọi chương trình**.
- I02 vòng 2: ĐÓNG — A20(e′) trả `mien_mo_khac_1`; qua `kiem` trả `not_measured` và `so_luat_hong`.
- H01: ĐÓNG — A14(i′) trả đúng một lý do đủ bốn phần; A15 đúng **43 lượt = 30/13**, **29 tên = 23/6**.
- H02: ĐÓNG — điều kiện lượt 2–4 tại dòng 837–838 khớp ADR-0052 và phần được ADR-0055 giữ nguyên.
- H04: ĐÓNG — `(None, "pwsh")` vẫn phân biệt thứ tự kiểm; m-S19 đổi đúng ca đích.
- G16: ĐÓNG — chạy lại `a03k_run_duong_nhanh_that` đạt.
- G17: ĐÓNG — chạy lại `a21_pham_vi_land` đạt.
- G18: ĐÓNG — các số hạng ước lượng vẫn cộng thành **2.248**, trong khoảng **2.150–2.300**; trần 2.400 vẫn cần chủ kho duyệt.
- G19: ĐÓNG — A20(f)–(i) bị từ chối với lý do riêng; A20(i′) có sổ lành và `kiem` trả `passed`.
- G20: ĐÓNG — **29/29** provenance tại base r7 và **31/31** tại `d26b36f` khớp tập job; run sớm nhất vẫn **40268583940**.

## Findings mới

- id: I01  
  severity: P2  
  vi_tri: SPEC.md:415–419,972,1036–1043  
  van_de: Kế thừa I01 vòng 5: A14-S0 chưa khóa mã thực thi của callable, vì `inspect.getsource(f)` lần theo `__wrapped__`, còn phép gián điệp thay callable trước khi chạy; đây là thiếu chốt nghiệm thu **chặn THI CÔNG**.  
  bang_chung: `python3 -I -B work/audit_s0_v6.py` đo wrapper vô hại chỉ đếm lời gọi: vế (1)–(4) trả `[]`, nguồn của `f` bằng nguồn hàm gốc nhưng nguồn của `f.__code__` khác; cả 10 đối số gián điệp giữ nguyên và wrapper không được gọi. `audit_followup_v6.py` xác nhận trên mô hình tích hợp: mọi chốt hằng/binding/AST đạt, `F-ok` vẫn `passed`, `F-ok-goc` vẫn có 13 lý do; gián điệp ghi **43/43** lời gọi mỗi fixture và **0** lượt chạy wrapper. Nguồn Python tại `inspect.py:1255` gọi `unwrap(object)`; `functools.py:62` gắn `wrapper.__wrapped__ = wrapped`. Hướng sai khác chỉ mô tả, không dựng module tấn công: wrapper chuẩn hóa NFC qua binding toàn cục rồi dùng metadata ấy sẽ được kiểm như hàm gốc. Đã đo NFC không đổi **171 vế bảng/gốc**, **61.530 đầu vào sinh** và đối số hai workflow; riêng `python ops/K.py\n`, tham chiếu từ chối nhưng sau NFC được nhận. Các ca Kelvin của vế (5) thay wrapper bằng gián điệp nên không kiểm phần xử lý bên trong wrapper. Xem [bằng chứng A14-S0](/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-6-codex/work/audit_s0_v6.json) và [đối chiếu tích hợp](/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-6-codex/work/audit_followup_v6.json).  
  de_xuat: Sửa vế (3)/(4) để kiểm đối tượng hàm và mã thực thi thực tế với tham chiếu tin cậy; không dùng nguồn đã tự unwrap làm bằng chứng đồng nhất callable. Thêm đối chứng wrapper có `__wrapped__`, giữ các đối chứng docstring/chú thích/định dạng/kiểu trả về để tránh chặn oan. Chỉ cấm riêng `__wrapped__` chưa chứng minh được việc không sửa `__code__` mà giữ metadata nguồn; cần nêu rõ phạm vi bảo đảm để chủ kho human audit.

- id: I02  
  severity: P3  
  vi_tri: SPEC.md:814,1033–1034  
  van_de: Căn cứ kích thước vẫn ghi **164 đột biến**, chưa cộng ba đột biến m-S27–m-S29 mới; đây là lỗi số đếm, **không chặn thi công**.  
  bang_chung: `git diff 3eb4be1 2c7f69c -- ops/specs/wp1236-r8.md` thêm m-S27, m-S28, m-S29 mà không bỏ đột biến cũ; theo cùng phạm vi đếm, **53 + 91 + 8 + 6 + 6 + 3 = 167**.  
  de_xuat: Sửa thành 167, cập nhật phân rã và ghi phần tăng của bản sửa 5 trong ước lượng; giữ phân biệt ước lượng với numstat thật và không tự đổi trần đã đề xuất.

## Đã đo lại, khớp

- `main_v5`: ba bản được phép đạt; sáu biến thể đối tượng hàm, hai biến thể đường gọi và bảy biến thể vòng 4 đều bị bắt. Nạp từ tệp bằng `spec_from_file_location` lấy nguồn được; chưa thấy chặn oan trong các biến thể được phép đã đo.
- [A14-S3b tích hợp](/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-6-codex/work/audit_integration_v6.json): **325/325** khớp trạng thái và danh sách lý do; gián điệp hai fixture và **10/10** ca đặc biệt đạt.
- A14-S6: **61.530 đầu vào, 2.647 nhận, 0 lệch, 0 nuốt lỗi, 0 không chạy** trong môi trường sạch.
- **53/53** đột biến bảng đổi đúng ca đích; **91/91** đột biến kho sinh bị vế (a) bắt, lệch **24–1.440** đầu vào.
- **7/7** băm hiện vật generation 1 khớp; **52/52** vế gốc bị từ chối; năm JSON chạy lại khớp hiện vật soạn.
- A14-S5 đã thống nhất điều kiện POSIX; A14-S6 đã quy định cờ bỏ phần shell trong vòng đột biến.
- Census: `d26b36f`/`fe84620` đúng **30/24/6**, `8983e1b` đúng **30/25/5**; Q-r8-5 đúng **0/39** lệch checkout/head và **28/28** blob khớp.
- Generation 1 đúng **3 tệp, +1.620/−0**. Không phát hiện thêm số đo sai hay mâu thuẫn ADR trong Q-r8-1…5 và ngân sách lời gọi.
- [Kiểm toàn vẹn cuối lượt](/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-6-codex/work/final_integrity.json): SHA đặc tả, HEAD/tree giữ nguyên; **0 delta nội dung checkout**.

KET_LUAN: changes_requested
