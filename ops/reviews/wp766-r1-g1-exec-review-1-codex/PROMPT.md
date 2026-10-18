# Cross-review độc lập — Packet #766 (wp766, t81 phụ thuộc PID của lượt chạy), lượt 1

Bạn là reviewer Codex, khác họ với executor (Claude). Vai READ-ONLY với mã: KHÔNG sửa tệp nào trong kho. Chỉ được
ghi vào thư mục làm việc hiện tại (thư mục ra). Kết quả bắt buộc: tệp `VERDICT.md` trong thư mục ra. Ghi `VERDICT.md`
SỚM (khung + finding đầu tiên) rồi cập nhật dần — lượt bị ngắt giữa chừng vẫn giữ được phần đã ghi.

## Định danh (băm là định danh, không phải tên nhánh)

- Kho: `ducthangho/tra-luat`, bản sao sẵn tại `KHO` = đường dẫn ghi ở cuối prompt.
- Exact head cần review: `701f41c686cef8456d43528ab9556a6b867cd7d6` (nhánh `agent/wp766-r1-g1-claude`, PR #772).
- Base: `e0273d31aba78b014aa89297f32ff86f9daf0277`. Diff cần review: `git -C KHO diff e0273d3 701f41c`.
- Đặc tả đóng băng: `ops/specs/wp766.md`, sha256 `da3095b47567dc8cb94137d0cc675d722eb256a77c8e06ddb90a216e7f148666`.
  Không có trong cây head; bản sao ở `SPEC` (cuối prompt). Kiểm băm trước khi tin. Các mục đánh dấu mũi tên
  (khuyến nghị) trong spec đã được chủ kho chốt đúng khuyến nghị.
- Issue: https://github.com/ducthangho/tra-luat/issues/766.

## Nhiệm vụ

1. Đọc spec (mục `muc_tieu` M1–M5, `nghiem_thu`), rồi diff. Hai tệp: `.claude/dev/launcher_test.py` (t81, helper
   `_pid_gia_khac_minh`, `_than_t81`, ca mới `r766_t81_khong_phu_thuoc_pid_cua_luot_chay`, mục `DOT_BIEN_HARNESS`
   `pid_gia_quay_ve_ghi_cung`) và `changelog.d/wp-766.md`. `launcher.py` KHÔNG đổi — `_chup_cay` cố ý bỏ `os.getpid()`.
2. ĐO, đừng chỉ đọc. Có sẵn `python3.12`, `python3.13` trong PATH. Ví dụ:
   `cd KHO && PYTHONDONTWRITEBYTECODE=1 python3.13 -B .claude/dev/launcher_test.py --lap-ca <ten_ca> --lan 1`.
   Để ép PID của lượt chạy, có sẵn shim `EP_PID` (cuối prompt): `cd KHO && python3.13 EP_PID <pid|that> --lap-ca <ca> --lan 1`
   (nó gán `os.getpid = lambda: pid` rồi chạy launcher_test.py). Chạy shim trên base để thấy lỗi gốc: dựng bản sao
   base bằng `git -C KHO worktree` là KHÔNG nên (launcher có probe `.git` là tệp); hãy `git clone KHO <tmp>` rồi
   `checkout e0273d3`.
   Executor khai (đo 16-10-2026):
   - M1: chạy toàn suite base với `os.getpid` bị móc ghi (ca, PID trong ảnh) ở hai chỗ loại trừ `launcher.py`
     (`_chup_cay` `ra.pop(os.getpid(), None)`, `_giet_rieng` `q == os.getpid()`): chỉ t81 đưa PID GIẢ (10,11,12);
     t156/t157/t160/t161 dùng PID tiến trình con thật. Ca khác cấp PID giả (500/501…) đều stub hai hàm ấy.
   - Base: t81 HỎNG với getpid=10 (vế b), 11 (vế a), 12 (vế b). Nhánh: t81 và r766 qua với getpid ∈ {thật,1,10,11,12,13,99999}.
   - Suite đầy đủ (hai vế cùng rig clone): 3.13 base 195/195 → nhánh 196/196; 3.12 base hỏng `r351` → nhánh hỏng
     `r351` (đỏ sẵn, môi trường); bỏ qua `t62` cả bốn. `--dot-bien` trên nhánh (3.13): 236/236 đạt, 1 KHÔNG ĐO ĐƯỢC
     (`124_khi_chau_con_song`, đích t62 chỉ Windows). ruff F launcher_test.py 5→5.
   Bạn có thể đo lại tuỳ thời gian (full suite ~5 phút/phiên bản; `--dot-bien` lâu hơn).
3. Đột biến để đo răng: KHÔNG sửa tệp trong KHO. Chép toàn kho ra /tmp rồi sửa bản sao.
4. Soi riêng:
   - M1 có đủ không: còn ca nào đưa PID cứng/giả vào ĐƯỜNG THẬT có loại trừ `os.getpid()` (hoặc so PID với PID của
     chính tiến trình theo cách khác) mà phép móc của executor bỏ sót? Phép móc chỉ bắt lời gọi `os.getpid` từ hai
     hàm ấy — có chỗ nào khác trong `launcher.py` so PID với `os.getpid()`/`os.getppid()` hoặc đọc `/proc/self`?
   - `_pid_gia_khac_minh` đọc `os.getpid()` LÚC GỌI — trong mọi đường r766 ép, fixture có bao giờ chọn trùng PID bị ép không?
     Hai vế (a)/(b) của t81 có giữ đúng ngữ nghĩa cũ (cùng hình cây) không?
   - r766 có thật sự ĐỎ khi fixture quay về PID cứng (đột biến harness), và chết bằng `TinHieuChotCa` (không traceback)?
     Hai đột biến cũ của t81 (`chup_cay_khong_fail_closed_trong_cay`, `chup_cay_fail_closed_ca_may`) còn răng?
   - Ép `os.getpid` trong r766 có rò sang ca sau không (harness `_co_lap_toan_cuc` + `finally`)? Nếu ca ném giữa vòng?
   - Tập ép có đủ không: có giá trị getpid nào làm t81/r766 đỏ mà r766 không thử?
   - Lời khai trong changelog/docstring có rộng hơn phép đo không (vd "chỉ t81", "getppid phòng thủ")?
   - Tiêu chí nghiệm thu nào trong spec chưa đáp ứng hoặc chưa đo?
5. Nếu một hướng thử cần SOẠN nội dung nhạy cảm (đường dẫn thoát cây, mã khai thác), đừng soạn — mô tả bằng lời trong VERDICT.

## Định dạng VERDICT.md

- Dòng đầu: `Reviewed commit: 701f41c686cef8456d43528ab9556a6b867cd7d6`
- `verdict: approve` hoặc `verdict: changes_requested`; đếm `P1=`, `P2=`, `P3=`.
- Mỗi finding: mã (F01…), mức (P1/P2/P3), tệp:dòng, mô tả, PHÉP ĐO đã chạy (lệnh + kết quả), và HINT patch nếu phức tạp.
- Bảng ≥ 6 HƯỚNG THỬ độc lập (giả thuyết · lệnh · output thật cắt gọn · kết luận LỖI / KHÔNG PHẢI LỖI / KHÔNG ĐO ĐƯỢC).
- Mục "Đã đo" liệt kê mọi lệnh đã chạy kèm rc/kết quả; mục "KHÔNG ĐO ĐƯỢC" cho thứ không đo được và lý do.
- Ngưỡng: approve chỉ khi P1=0 và P2=0.

## Đường dẫn

- KHO: `/tmp/claude-0/-home-user-tra-luat/4db0e1e9-e429-5947-8704-a56b7bbfbbd7/scratchpad/rv1`
- SPEC: `/tmp/claude-0/-home-user-tra-luat/4db0e1e9-e429-5947-8704-a56b7bbfbbd7/scratchpad/rv1-out/spec-wp766.md`
- EP_PID: `/tmp/claude-0/-home-user-tra-luat/4db0e1e9-e429-5947-8704-a56b7bbfbbd7/scratchpad/rv1-out/ep_pid.py`
- Thư mục ra (ghi VERDICT.md ở đây): `/tmp/claude-0/-home-user-tra-luat/4db0e1e9-e429-5947-8704-a56b7bbfbbd7/scratchpad/rv1-out`
