# ADR-0061 — Không ghi được trạng thái "credential Codex bị từ chối" thì lần gọi sau probe lại: chấp nhận vĩnh viễn

- **Trạng thái:** Accepted (2026-11-02). Chủ kho `ducthangho` chọn "ADR chấp nhận (Recommended)" cho Issue #825 qua
  AskUserQuestion trong phiên `session_015Gtxra7iT6mwM1kqpdggt6` ngày 01-11-2026, rồi bảo làm ngay ("Đồng ý làm đi",
  02-11-2026). Thi hành bằng packet `CODEX-REJECTED-STATE-KHONG-GHI-DUOC-ADR` revision 1 · generation 1, đặc tả
  wp825.md trong ops/specs (sha256 `dee36a11…812e`), không phải một phiên tự đặt quy ước. Thứ định danh đặc tả là băm, không
  phải tên nhánh: tìm tệp ở `master` trước, chưa thấy thì fetch nhánh `ops/wp825-r1-g1-lease`.
- Đóng nợ có tên `codex-rejected-state-khong-ghi-duoc` (#825), sinh từ packet #484 (land qua PR #792).

## Giới hạn được chấp nhận
Khi credential Codex bị dịch vụ **từ chối**, `.claude/dev/launcher.py` ghi danh tính của credential ấy vào state chờ
snapshot. Việc ghi này do `_danh_dau_auth_hong` làm, qua `_KhoCodex` dưới `CODEX_HOME`. Có state ấy thì lần gọi sau
không thử lại đúng credential đã biết là hỏng.

Nếu lần ghi danh tính bị từ chối hỏng, hai lối kiểm sống báo lỗi ghi; materializer cũng có
lý do riêng. Kho không dựng chỗ lưu dự phòng cho danh tính ấy. ADR này chấp nhận vĩnh viễn
khả năng probe lặp khi state vẫn đọc được nhưng chưa nhớ danh tính đã bị từ chối.

## Hậu quả và điều kiện áp dụng
Đơn vị đếm là **lời probe mạng ở mức gọi helper**; số lần gọi suy từ luồng mã,
chưa đo số request mạng bên trong Codex CLI.
Khi state vẫn đọc được, chưa chứa danh tính bị từ chối, credential giữ nguyên và probe vẫn
bị dịch vụ từ chối, lỗi ghi lặp trước bước promote state sẽ làm lần gọi kiểm sống sau thử lại
credential ấy. Mỗi lượt đi đến nhánh này gọi helper probe một lần; materializer cần có snapshot
đủ điều kiện probe thay cho credential cũ. Lý do CHẶN lỗi ghi lặp lại khi cùng lỗi ghi còn tồn tại.

Kết quả ghi hỏng không bảo đảm state chưa thay đổi: `_KhoCodex.write` có thể đã `os.replace`
state rồi mới lỗi ở `os.fsync` thư mục trên POSIX. Nếu lần sau đọc được danh tính đã lưu thì
lượt đó không probe. Nếu state không đọc được, `_dang_cho_snapshot` cũng chặn mà không probe;
materializer có thể trả lỗi đọc/ghi state chung. Vì vậy lý do lần sau có thể khác lý do lỗi ghi.
Các ca ở dưới khóa việc báo lỗi, không chứng minh một bảo đảm tổng quát về mọi lỗi I/O hoặc
mọi xen kẽ ghi; không suy từ kết quả `False` rằng mọi tệp state đều giữ nguyên.

## Cách phát hiện — cả ba lối đều báo lỗi to, mỗi lối có lý do riêng
1. `launcher._do_codex_song` (đo trên `c7174bf`): khi `_danh_dau_auth_hong` trả `False`, lối này trả lý do bắt đầu bằng
   `KHÔNG ghi được trạng thái chờ snapshot sau khi …`, kèm `CHẶN: sửa CODEX_HOME (quyền/dung lượng) trước khi thử lại`.
   Lý do này khác hẳn trường hợp đã ghi xong. Khoá bằng ca r484_g7_khong_ghi_duoc_trang_thai_tu_choi_phai_noi_ra và đột
   biến `g7_nuot_loi_ghi_trang_thai` trong `.claude/dev/launcher_test.py`.
2. Materializer `chuan_bi_xac_thuc`: khoá bằng ca r484_g7_materializer_khong_ghi_duoc_trang_thai_noi_dung_ly_do và đột
   biến `g7_f01_materializer_gop_loi`.
3. `codex_cred.cmd_kiem`: khoá bằng ca `t16_khong_ghi_duoc_trang_thai_tu_choi_phai_noi_ra` trong
   `.claude/dev/codex_cred_test.py`.

Đo trên `c7174bf` lúc 00:5xZ ngày 02-11-2026: hai ca `r484_g7_*` ra `1/1 qua` khi chạy `--lap-ca`, và
`codex_cred_test.py` ra `TỔNG: ĐẠT`. Các ca này là **bằng chứng hành vi** rằng lỗi không bị nuốt. Chúng không phải cổng
đọc ADR này. Lệnh tái lập từ gốc kho (dùng temp ngoài repository và tránh `/tmp/.git` nếu có):

```bash
python3 -B .claude/dev/launcher_test.py --lap-ca r484_g7_khong_ghi_duoc_trang_thai_tu_choi_phai_noi_ra --lan 1
python3 -B .claude/dev/launcher_test.py --lap-ca r484_g7_materializer_khong_ghi_duoc_trang_thai_noi_dung_ly_do --lan 1
python3 -B .claude/dev/codex_cred_test.py
```

## Cách gỡ
Sửa quyền hoặc giải phóng dung lượng của `CODEX_HOME`, rồi gọi lại. Lần ghi kế tiếp thành công thì state được lưu, và
từ đó không còn probe lặp. Nếu credential thật sự hỏng thì đăng nhập lại (`codex login --device-auth`), hoặc chạy
`python3 .claude/dev/launcher.py chuan-bi` để khôi phục từ biến.

## Vì sao không dựng chỗ lưu dự phòng
Những nguyên nhân làm hỏng lần ghi chính (đĩa đầy, sai quyền, hệ tệp chỉ đọc) thường làm hỏng luôn lần ghi dự phòng trên
cùng máy. Chỗ dự phòng vì vậy mua thêm rất ít, mà lại thêm một đường ghi credential state phải canh. **Mệnh đề này là suy
luận, CHƯA ĐO trên từng loại hỏng.** Nếu sau này có số đo cho thấy một chỗ dự phòng sống sót được trong một loại hỏng
phổ biến, ADR này phải được xét lại bằng một ADR mới.

## Cưỡng chế
Đo trên `origin/master` `c7174bf`: `rg -c 'ADR-0061|0061-codex' <tệp>` không khớp ở cả sáu
vị trí dưới đây (stdout rỗng, rc=1). Đây chỉ là số dòng nhắc định danh ADR. Đo thêm khái niệm
bằng `rg -c 'codex-rejected-state-khong-ghi-duoc|_danh_dau_auth_hong|KHÔNG ghi được trạng thái' <tệp>`:

| vị trí cổng | khớp định danh ADR | khớp khái niệm |
|---|---|---|
| `ops/lease_publish.py` | 0 | 0 |
| `.claude/dev/packet_loop.py` | 0 | 0 |
| `.claude/dev/launcher.py` | 0 | 4 dòng |
| `.claude/dev/gate_lifecycle.py` | 0 | 0 |
| `.github/workflows/ci.yml` | 0 | 0 |
| `.github/workflows/ops-publish-lease.yml` | 0 | 0 |

Theo định nghĩa cột §20, đây là mức **có nhắc: launcher.py×4**, chưa chứng minh có cổng đọc
quyết định chấp nhận giới hạn. Đọc các nhánh `_danh_dau_auth_hong`, `chuan_bi_xac_thuc`,
`_do_codex_song` và `codex_cred.cmd_kiem` thấy hành vi báo lỗi được mã hóa sẵn; không thấy
consumer của quyết định chấp nhận trong ADR. Đây là đối chiếu luồng mã, không phải hệ quả
riêng của phép grep tên. Việc chấp nhận vẫn sống bằng kỷ luật đọc. `adr-song` đọc đăng ký
và metadata trạng thái của ADR, không kiểm hậu quả hay thực thi quyết định chấp nhận này.
Các ca/đột biến ở mục *Cách phát hiện* là bằng chứng hành vi báo lỗi.
