# ADR-0061 — Không ghi được trạng thái "credential Codex bị từ chối" thì lần gọi sau probe lại: chấp nhận vĩnh viễn

- **Trạng thái:** Accepted (2026-11-02). Chủ kho `ducthangho` chọn "ADR chấp nhận (Recommended)" cho Issue #825 qua
  AskUserQuestion trong phiên `session_015Gtxra7iT6mwM1kqpdggt6` ngày 01-11-2026, rồi bảo làm ngay ("Đồng ý làm đi",
  02-11-2026). Thi hành bằng packet `CODEX-REJECTED-STATE-KHONG-GHI-DUOC-ADR` revision 1 · generation 1, đặc tả
  `ops/specs/wp825.md` (sha256 `dee36a11…812e`), không phải một phiên tự đặt quy ước. Thứ định danh đặc tả là băm, không
  phải tên nhánh: tìm tệp ở `master` trước, chưa thấy thì fetch nhánh `ops/wp825-r1-g1-lease`.
- Đóng nợ có tên `codex-rejected-state-khong-ghi-duoc` (#825), sinh từ packet #484 (land qua PR #792).

## Giới hạn được chấp nhận
Khi credential Codex bị dịch vụ **từ chối**, `.claude/dev/launcher.py` ghi danh tính của credential ấy vào state chờ
snapshot. Việc ghi này do `_danh_dau_auth_hong` làm, qua `_KhoCodex` dưới `CODEX_HOME`. Có state ấy thì lần gọi sau
không thử lại đúng credential đã biết là hỏng.

Nếu chính lần ghi đó hỏng (đĩa đầy, sai quyền trên `CODEX_HOME`, hệ tệp chỉ đọc), `_danh_dau_auth_hong` trả `False`, và
kho **không có chỗ nào khác** để nhớ hộ. ADR này chấp nhận vĩnh viễn rằng trong trường hợp đó, lần gọi sau sẽ probe lại
đúng credential đã bị từ chối.

## Hậu quả quan sát được
Đơn vị đếm là **lời probe mạng mỗi lần gọi**:
- mỗi lần gọi sau một lần ghi hỏng tốn thêm **1** lần probe credential đã bị từ chối;
- lần nào kết quả cũng là từ chối, kèm cùng lý do CHẶN (xem mục dưới);
- không có trạng thái nào bị ghi sai. Kho chỉ *không nhớ* được điều đã biết.

## Cách phát hiện — cả ba lối đều báo lỗi to, mỗi lối có lý do riêng
1. `launcher._do_codex_song` (đo trên `c7174bf`): khi `_danh_dau_auth_hong` trả `False`, lối này trả lý do bắt đầu bằng
   `KHÔNG ghi được trạng thái chờ snapshot sau khi …`, kèm `CHẶN: sửa CODEX_HOME (quyền/dung lượng) trước khi thử lại`.
   Lý do này khác hẳn trường hợp đã ghi xong. Khoá bằng ca `r484_g7_khong_ghi_duoc_trang_thai_tu_choi_phai_noi_ra` và đột
   biến `g7_nuot_loi_ghi_trang_thai` trong `.claude/dev/launcher_test.py`.
2. Materializer `chuan_bi_xac_thuc`: khoá bằng ca `r484_g7_materializer_khong_ghi_duoc_trang_thai_noi_dung_ly_do` và đột
   biến `g7_f01_materializer_gop_loi`.
3. `codex_cred.cmd_kiem`: khoá bằng ca `t16_khong_ghi_duoc_trang_thai_tu_choi_phai_noi_ra` trong
   `.claude/dev/codex_cred_test.py`.

Đo trên `c7174bf` lúc 00:5xZ ngày 02-11-2026: hai ca `r484_g7_*` ra `1/1 qua` khi chạy `--lap-ca`, và
`codex_cred_test.py` ra `TỔNG: ĐẠT`. Các ca này là **bằng chứng hành vi** rằng lỗi không bị nuốt. Chúng không phải cổng
đọc ADR này.

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
**0 cổng đọc ADR này.** Đo trên `origin/master` `c7174bf`, với `rg -c 'ADR-0061|0061-codex' <tệp>` trên đủ sáu vị trí
cổng mà §20 của `docs/PROTOCOL_DA_PHIEN.md` liệt kê:

| vị trí cổng | kết quả |
|---|---|
| `ops/lease_publish.py` | 0 dòng |
| `.claude/dev/packet_loop.py` | 0 dòng |
| `.claude/dev/launcher.py` | 0 dòng |
| `.claude/dev/gate_lifecycle.py` | 0 dòng |
| `.github/workflows/ci.yml` | 0 dòng |
| `.github/workflows/ops-publish-lease.yml` | 0 dòng |

Hành vi được ADR này mô tả (báo lỗi to) vẫn có ca test và đột biến khoá ở mục *Cách phát hiện*. Việc **chấp nhận** giới
hạn thì chỉ sống bằng kỷ luật đọc. `adr-song` canh việc ADR này được đăng ký trong §20, không canh nội dung của nó.
