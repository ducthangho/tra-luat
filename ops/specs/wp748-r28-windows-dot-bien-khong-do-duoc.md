# Đặc tả packet #748 r28: ca đích của đột biến sandbox phải khai KHÔNG ĐO ĐƯỢC trên nền không phải Linux

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

| trường | giá trị |
|---|---|
| packet | #748 `wp748`, revision 28, generation 1 |
| review_class | `sensitive` (lane launcher) |
| write set | `.claude/dev/launcher_test.py` |
| base | `origin/master` lúc cấp lease (đo khi soạn: `f577ab5`) |
| executor | `anthropic_claude` (Claude Code remote, Linux) |
| reviewer | `openai_codex` qua `launcher.py run`, phiên mới, read-only, neo đúng head |

## 1. Vì sao
Sau khi PR #957 (r27) merge vào `0615234`, lượt push master của `launcher-windows.yml` (run `40437650224`) đỏ ở bước `Tu dot bien`. Lý do là đột biến `r27_lenh_run_khong_lay_mau` (xoá `sandbox.bat_dau()`) cho kết quả `SAI giet 0/1`.

Trên nền không phải Linux, `_LayMauSandbox` không có luồng lấy mẫu, nên `bat_dau()` không làm gì. Ca đích `r927_lenh_run_ghi_effort_va_sandbox_vao_run_json` khi đó chạy nhánh "ngoài Linux" và kiểm `KHONG_DO_DUOC`. Kết quả này đúng cả khi có lẫn khi không có `bat_dau()`.

Vì vậy, trên nền này đột biến **không đo được**. Nhưng ca đích không khai điều đó, nên bộ chạy đột biến đếm đột biến là SỐNG.

Phép đo trên cùng lượt chạy ấy: test 255/255 qua, mọi đột biến khác hoặc OK hoặc KHÔNG ĐO ĐƯỢC. Lane PR không bắt được lỗi này vì #957 không mang nhãn `windows`.

## 2. Thay đổi
Trong `r927_lenh_run_ghi_effort_va_sandbox_vao_run_json`, ở nhánh không phải Linux:
- vẫn chạy đủ các phép kiểm hiện có (effort `DO_DUOC`, sandbox `KHONG_DO_DUOC`);
- sau đó trả về một chuỗi lý do bỏ qua phần phụ thuộc `/proc`.

Theo hợp đồng của bộ chạy đột biến, đột biến nào chỉ có ca đích này sẽ thành "KHÔNG ĐO ĐƯỢC trên nền này". Phép đo của nó vẫn còn nguyên trên Ubuntu.

Đột biến `r27_lenh_run_khong_ghi_so` vẫn bị giết trên Windows: bỏ `ghi_so` thì phép kiểm `KHONG_DO_DUOC` ĐỎ trước khi tới chỗ trả về.

## 3. Tiêu chí xong
- **Ubuntu:** `launcher_test` N/N; mọi đột biến r25–r27 và r952 bị giết đúng ca đích, không đổi so với trước.
- **Windows** (PR mang nhãn `windows`, hoặc gọi tay `launcher-windows.yml`): bước `Tu dot bien` xanh; `r27_lenh_run_khong_lay_mau` ghi "KHÔNG ĐO ĐƯỢC trên nền này"; mọi đột biến khác OK hoặc KHÔNG ĐO ĐƯỢC.
- Review chéo Codex qua `launcher.py run` trên đúng head, tới khi 0 P0–P3.

## 4. Trần
- Kích thước: ≤ 1 tệp / ≤ 20 dòng thêm.
- Lời gọi Codex: 10 theo dòng khai ADR-0055.
