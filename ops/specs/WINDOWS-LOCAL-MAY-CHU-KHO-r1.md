# Đặc tả packet `WINDOWS-LOCAL-MAY-CHU-KHO` r1: đưa quy ước dùng máy Windows của chủ kho vào protocol

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544

| trường | giá trị |
|---|---|
| packet | `WINDOWS-LOCAL-MAY-CHU-KHO` (mission #748), revision 1, generation 1 |
| review_class | `systemic` (đổi quy tắc protocol cho mọi executor) |
| write set | `docs/adr/0057-windows-local-may-chu-kho.md` (planned), `docs/PROTOCOL_DA_PHIEN.md` |
| base | `origin/master` lúc cấp lease (đo khi soạn: `735b181`) |
| executor | `anthropic_claude` (Claude Code remote, Linux) |
| reviewer | `openai_codex` qua `launcher.py run`, phiên mới, neo đúng head |
| depends_on | không |

## 1. Vì sao
Ngày 29-10-2026, chủ kho chỉ thị trong phiên điều phối `session_01V2PEqhkb91vD5PCBM5yXbm`. Theo chỉ thị này, khi máy Windows local của chủ kho bật và Desktop Commander hoạt động, executor được dùng máy đó để chạy test và vá lỗi Windows. Điều kiện merge gồm hai vế: hết P1, P2, P3, **và** đã vá hết các lỗi Windows local (nếu đã chạy test local). Chủ kho yêu cầu đo hiệu quả trước rồi mới đưa vào protocol.

Quy ước hiện chỉ được gửi tới từng phiên qua `send_message`. Các số đo dưới đây lấy từ `D:\tl-win\do-luong.csv` trên ASUS-LAPTOP và từ log của phiên, ngày 29-10-2026:

| # | sự kiện | số đo | bài học |
|---|---|---|---|
| D1 | chạy song song `tl selftest`, `lease_publish_test`, `packet_loop_test` trên `1cc847d` | `t192_S8` đỏ khi chạy song song; chạy riêng trên `e9967f0` lúc máy rảnh ra 3/3 ĐẠT (8 s) | chạy chồng sinh **đỏ giả**, nên khoá một-phiên-một-lúc là cần, không phải nghi lễ |
| D2 | hai phiên chưa nhận quy ước | PID 17016 (`wp960-win`) và PID 22884 (`tl1014`, PR #1014 đã đóng) chạy `bien_nhan_v2_test` từ 09:06Z và 09:10Z, ngoài khoá, trong lúc phiên #1006 giữ khoá từ 09:24Z | quy ước gửi qua tin nhắn thì không tới được mọi phiên; phải nằm ở **nơi mọi phiên đọc** |
| D3 | `packet_loop_test` không in tiến độ (stdout đệm) | 65 phút với `pl.out` = 0 byte rồi phải dừng tay | lượt chạy dài trên local phải in tiến độ (`python -u` hoặc nhật ký từng ca) |
| D4 | độ sẵn sàng | Desktop Commander trả `CONNECT_TIMEOUT` cho `session_015GtxrZ1Tt93F4NLUUhKYQy` lúc ~09:00Z và ~09:23Z; máy offline khoảng 3 giờ trước 07:48Z | local là năng lực **có lúc có lúc không**, nên không được làm điều kiện bắt buộc vô điều kiện |
| D5 | lợi ích | `tl selftest` 1738/1738 local trong khoảng 10 phút; Windows CI qua `workflow_dispatch` ~40 phút cộng hàng đợi, và hôm đó bị billing chặn nhiều giờ | khi máy sẵn sàng thì local nhanh hơn CI và không phụ thuộc billing |
| D6 | lỗi phát hiện | trên master: `t27` (Windows-only, packet #1006), `r929` (WinError 5, đã vá #1010), `bien_nhan_v2_test` c91/c93/c96 (#1017) | local tái hiện đúng lỗi Windows thật mà CI Linux không thấy |

## 2. Thay đổi
1. **Thêm ADR-0057** `docs/adr/0057-windows-local-may-chu-kho.md`, trạng thái `Accepted` khi chủ kho duyệt spec_hash. Nội dung:
   - **Phạm vi:** máy Windows của chủ kho (hiện là ASUS-LAPTOP) truy cập qua Desktop Commander. Executor chỉ dùng máy khi `list_devices` báo `Online`.
   - **Điều kiện merge cộng thêm:** nếu packet đã chạy test trên Windows local thì mọi lỗi local do diff gây ra phải được vá trước merge. Lỗi có sẵn trên base phải được nêu tên, kèm SHA đo nền. Máy offline thì vế này không áp, và PR phải ghi rõ "không đo local". Local **không thay** check bắt buộc của CI, mà chỉ cộng thêm.
   - **Khoá:** `D:\tl-win\KHOA.txt` có nội dung tức là máy đang bận. Phiên nào giữ khoá thì ghi `<session_id>\t<UTC>\t<việc>` và xoá nội dung khi xong. Không chạy test nặng khi khoá đang do phiên khác giữ.
   - **Kiểm tải trước khi đo:** chạy `Get-CimInstance Win32_Process -Filter "Name='python.exe'"`. Nếu có tiến trình không thuộc phiên mình thì ghi vào kết quả đo, và không tự dừng tiến trình của phiên khác.
   - **Cô lập:** mỗi phiên làm trong thư mục riêng `D:\tl-win\<session_id>\` (clone từ GitHub, `core.abbrev 7`). Không đụng kho làm việc của chủ kho.
   - **Môi trường:** `PYTHONUTF8=1`, `PYTHONIOENCODING=utf-8`, `PYTHONDONTWRITEBYTECODE=1`; dùng `python`; đường dẫn có dấu thì dùng `git -C`.
   - **Tiến độ:** lượt chạy quá 5 phút phải in tiến độ (`python -u` hoặc nhật ký từng ca).
   - **Đo lường:** mỗi lượt ghi một dòng vào `D:\tl-win\do-luong.csv` theo các cột `thoi_diem,session,packet,sha,bo_test,dat,tong,ca_do,thoi_luong_s,phat_hien_boi,loi_that,da_va,ghi_chu`.
   - **Bằng chứng:** PR ghi SHA đã đo, lệnh chạy, N/N, và nói rõ đó là "local".
   - **Xem xét lại:** sau 10 packet có dùng local, hoặc sau 30 ngày, chủ kho xét lại ADR dựa trên `do-luong.csv`.
2. **`docs/PROTOCOL_DA_PHIEN.md`:**
   - thêm đúng một dòng ADR-0057 vào bảng §20, với cột "cổng nào ĐỌC luật ấy" ghi `không cổng — kỷ luật executor`;
   - thêm một câu con trỏ ở §10.2 (worker gate) dẫn tới ADR-0057.

   Không chép doctrine vào protocol: `doctrine-scan` phải giữ rc=0.

## 3. Tiêu chí xong
- `python .claude/dev/packet_loop.py adr-song --root .` rc=0 (ADR mới có dòng trong §20 và dòng `Trạng thái` đọc được).
- `python .claude/dev/packet_loop.py doctrine-scan --root .` rc=0. `doc-claims-check` ok.
- Diff chỉ chạm đúng 2 tệp của write set.
- Review chéo Codex qua `launcher.py run` trên đúng head, lặp tới khi 0 P0–P3.
- Không cổng nào cưỡng chế ADR này; ADR phải nói thẳng điều đó.

## 4. Trần
- Kích thước: ≤ 2 tệp / ≤ 140 dòng thêm.
- Lời gọi Codex: 10 theo dòng khai ADR-0055.

## 5. Ngoài phạm vi
- Không viết công cụ tự động cho khoá hoặc sổ đo. Nếu số đo về sau cho thấy cần, việc đó thuộc một packet sau.
- Không sửa CI và không đổi check bắt buộc.
- Không dừng tiến trình của phiên khác. Dọn máy là việc của chủ kho.
