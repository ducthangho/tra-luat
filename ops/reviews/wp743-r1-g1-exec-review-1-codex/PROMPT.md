# Cross-review độc lập — Packet #743 (py314-path-exists-nuot-oserror), lượt 1

Bạn là reviewer Codex, khác họ với executor (Claude). Vai READ-ONLY với mã: KHÔNG sửa tệp nào trong kho. Chỉ được
ghi vào thư mục làm việc hiện tại (thư mục ra). Kết quả bắt buộc: tệp `VERDICT.md` trong thư mục ra.

## Định danh (băm là định danh, không phải tên nhánh)

- Kho: `ducthangho/tra-luat`, bản sao sẵn tại `KHO` = đường dẫn ghi ở cuối prompt.
- Exact head cần review: `80e0fac0a4ab8c74486cf3bab1a73e1dec600994` (nhánh `agent/wp743-g1-claude`).
- Base: `9fddb1d19e8e5b753bb687673846d484fb710182`. Diff cần review: `git -C KHO diff 9fddb1d 80e0fac`.
- Đặc tả đóng băng: `ops/specs/py314-path-exists-nuot-oserror-r1.md`, sha256
  `e2121dc07571edb24bf410badccf88d0d35a3d1ddba1f1a490ab378b607d8519`. Không có trong cây head; bản sao ở
  `SPEC` (cuối prompt). Kiểm băm trước khi tin.
- Issue: https://github.com/ducthangho/tra-luat/issues/743 (nội dung chính đã chép trong spec mục `loi`).

## Nhiệm vụ

1. Đọc spec, rồi diff. Hai tệp: `.claude/dev/launcher.py` (hàm `_con_song`) và `.claude/dev/launcher_test.py`.
2. ĐO, đừng chỉ đọc. Có sẵn `python3.12`, `python3.13`, `python3.14` trong PATH. Ví dụ:
   `cd KHO && PYTHONDONTWRITEBYTECODE=1 python3.14 -B .claude/dev/launcher_test.py --lap-ca <ten_ca> --lan 1`.
   Ca đích: `r743_con_song_tham_do_bang_stat_giu_errno_moi_phien_ban`, `t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan`,
   `t157_giet_cay_khi_stat_EACCES_van_tron_ven`, `t117_moi_mau_dot_bien_phai_khop_DUNG_MOT_cho`.
   Executor khai: full suite 3.14 chỉ hỏng `r09`,`r15`,`r351` (đỏ sẵn ở nền, ngoài phạm vi); 3.12 bằng nền; 3.13 195/195;
   đột biến `wp685_*`+`r743_*` 59/59 bị giết trên 3.12 và 3.14. Bạn có thể đo lại tuỳ thời gian (full suite ~5 phút/phiên bản).
3. Đột biến bản vá để đo răng: chép `launcher.py` ra thư mục ra hoặc /tmp, sửa bản sao, KHÔNG sửa tệp trong KHO. Bộ test
   nạp launcher qua `LAUNCHER_DANG_DUNG`; cách dễ nhất là chạy `launcher_test.py --dot-bien` trên một bản sao TOÀN KHO
   trong /tmp, hoặc tự viết driver nạp module và lọc `DOT_BIEN`.
4. Soi riêng:
   - Phân loại errno có đúng đặc tả Q2 không; có đường nào kết luận "chết" mạnh hơn trước (fail-open của chốt 124/125)?
   - Hành vi trên 3.12/3.13 có đổi so với `Path.exists()` cũ (EBADF/ELOOP, ValueError) và đổi ấy có được spec cho phép?
   - Seam `_CsSeam` có thật sự chặn thao tác mới trên MỌI phiên bản; ca r743 có đỏ trên 3.12 khi gọi lại `exists()`?
   - Các mẫu `DOT_BIEN` `wp685_a`, `wp685_f`, `wp685_m4` đổi theo phép thăm dò mới — có làm mất răng đột biến nào?
   - Có đột biến nào "bị giết" vì lỗi vô can (tín dụng giả) thay vì chốt `TinHieuChotCa` không?
   - Tiêu chí nghiệm thu trong spec có tiêu chí nào chưa được đáp ứng hoặc chưa đo?
5. Nếu một hướng thử cần SOẠN nội dung nhạy cảm (đường dẫn thoát cây, mã khai thác), đừng soạn — mô tả bằng lời trong VERDICT.

## Định dạng VERDICT.md

- Dòng đầu: `Reviewed commit: 80e0fac0a4ab8c74486cf3bab1a73e1dec600994`
- `verdict: approve` hoặc `verdict: changes_requested`; đếm `P1=`, `P2=`, `P3=`.
- Mỗi finding: mã (F01…), mức (P1/P2/P3), tệp:dòng, mô tả, PHÉP ĐO đã chạy (lệnh + kết quả), và HINT patch nếu phức tạp.
- Mục "Đã đo" liệt kê mọi lệnh đã chạy kèm rc/kết quả; mục "KHÔNG ĐO ĐƯỢC" cho thứ không đo được và lý do.
- Ngưỡng: approve chỉ khi P1=0 và P2=0.

## Đường dẫn

- KHO: `/tmp/claude-0/-home-user-tra-luat/25822fa2-ac40-52b8-b361-6687f0dd1ccb/scratchpad/rv`
- SPEC: `/tmp/claude-0/-home-user-tra-luat/25822fa2-ac40-52b8-b361-6687f0dd1ccb/scratchpad/rv-out/spec-r1.md`
- Thư mục ra (ghi VERDICT.md ở đây): `/tmp/claude-0/-home-user-tra-luat/25822fa2-ac40-52b8-b361-6687f0dd1ccb/scratchpad/rv-out`
