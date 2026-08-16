# Audit launcher vòng 7

Ngày đo: 2026-08-13. Nền tại chỗ: Linux; mọi kết luận riêng Windows được tách rõ
giữa giả lập fail-closed và phép đo cần runner Windows thật.

## CHẶN

1. `_giet_cay`: khi PID mẹ đã biến mất, `_thanh_vien_nhom` trả `None` trên
   Windows nhưng điều kiện `if not con` đọc nó như `[]`, rồi trả “cả cây đã chết”.
   Tái hiện bằng `t78_khong_do_duoc_nhom_KHONG_phai_cay_rong`; trước vá nó bắt
   `KetGiet.tron_ven=True` mà đường giết Windows chưa được gọi.
2. `_job_windows` bỏ qua giá trị trả về của `SetInformationJobObject`. Job có thể
   được quảng cáo là hoạt động dù bước cấu hình thất bại. `t79` giả lập API trả 0;
   sau vá hàm trả `None`, đóng đúng handle và không gọi `OpenProcess`.
3. `_pid_trong_job` đóng đinh buffer 512 PID. Job lớn hơn làm truy vấn thiếu chỗ;
   không có đường tăng buffer. `t80` giả lập lượt đầu cần 100 PID khi sức chứa 64,
   lượt hai trả đủ 100; sau vá nhận chính xác danh sách 1..100.
4. `_chup_cay` trên Windows lọc im lặng mọi tiến trình thiếu `CreationDate` và bỏ
   qua dòng sai khuôn. Một hậu duệ mất khỏi ảnh có thể làm kiểm tra sau giết xanh
   giả. `t81` đưa một dòng hợp lệ và một dòng `NO_CREATION_DATE`; sau vá trả `None`.
5. Sàn đột biến chỉ đỏ khi không đo được ca nào. Một nền chỉ đo 5/35 vẫn có thể
   xanh. `t82` chốt sàn 70%; 25/35 được chấp nhận, 24/35 và 5/35 bị từ chối.
6. Probe `taskkill /T` của workflow chỉ in mã và trạng thái rồi luôn thành công.
   Probe `t62` cũng coi “BỎ QUA” là thành công. Cả hai đã được đổi thành lỗi cứng.

## ĐÃ VÁ

- Năm lỗi mã/test ở trên có phản chứng `t78`–`t82` và năm đột biến riêng.
- Query PID Job Object tăng buffer tối đa tám lượt; lỗi không giải thích được vẫn
  trả `None`, tuyệt đối không trả `[]`.
- PowerShell chụp cây phát dòng `ERR` cho PID thiếu ngày tạo; parser coi mọi dòng
  thiếu/sai là ảnh không đủ bằng chứng.
- Workflow Windows giữ lại mã `taskkill` trước lệnh khác, bắt cả mã khác 0 lẫn PID
  còn sống, và bắt `t62` bỏ qua bất ngờ.

## KHÔNG VÁ ĐƯỢC

- Không chạy được Job Object, `taskkill`, CIM, `GetProcessTimes`, console cp1258
  hay semantics PowerShell trên Linux. CI `launcher (Windows thật)` phải đo chúng.
- Khe con cực ngắn trên Windows vẫn còn: lấy danh tính qua CIM có thể hụt sau khi
  con thoát. Vá đúng cần lấy `FILETIME` từ handle `Popen` bằng `GetProcessTimes`,
  rồi chứng minh khóa đó khớp `CreationDate.Ticks` trên Windows thật. Chưa vá vì
  chuyển epoch/múi giờ sai sẽ làm chốt luôn từ chối giết.
- Buffer động đã được giả lập, nhưng ca Job Object thật có hơn 512 PID chưa chạy ở
  đây. CI Windows nên dựng job riêng, thêm hơn 512 tiến trình nhẹ, xác nhận query
  trả đủ hoặc trả `None` (không bao giờ `[]`), rồi dọn bằng `TerminateJobObject`.

## GHI NHẬN

- Baseline trước sửa: `doctor` rc=0; launcher `77/77` (qua 76, bỏ qua 1);
  đột biến `34/34` (1 không đo được); ruff sạch.
- `python3 scripts/tl.py --selftest` baseline ra `1695/1697`, rc=1, chỉ hỏng đúng
  `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` và
  `r268_l2_trichotomy_theo_trang_thai_object`. Đây đúng hiện vật sandbox đã biết;
  không có ca mới và không dùng nó để chặn vòng này.
- Ratchet vòng 6 đúng: ba tài liệu ngoài gói, manifest 179 mục, toàn bộ 55 Markdown
  dưới `docs/` bị loại khỏi gói. Báo cáo này nâng đúng 55→56 và cây 234→235.
- Không còn con trỏ dạng hai chấm kèm số từ tài liệu vào mã `.claude/`.
- Bước “cây làm việc sạch” không đo nội dung thư mục tạm; nó đo đúng một việc khác:
  test có rò tệp tracked/untracked vào worktree hay không. Vì vậy bước vẫn có giá trị.
- Mã con vẫn có thể trùng mã launcher theo thiết kế; `run.json.trang_thai` là trường
  phân biệt. Kiểm đứt ống hiện tại vẫn giữ mã qua `main` sau thay đổi vòng 5–6.
- Với nền không hỗ trợ nhóm, snapshot không bị xóa ngay nhưng `t77` chứng minh lượt
  chạy sau quét snapshot quá 24 giờ. Đây là dọn trễ có chủ ý, không phải dọn ngay.

## Phép đo Windows cần chạy

Workflow `.github/workflows/launcher-windows.yml` phải chạy trọn: bộ phản chứng,
bộ đột biến, probe đứt ống, cp1258, `t62` và `taskkill /T`. Bổ sung một probe API
thật kiểm ba trạng thái tách biệt: cấu hình Job thành công, query lỗi trả “không đo
được”, query thành công với danh sách rỗng chỉ sau `TerminateJobObject`.

## Số cuối

- Launcher: **82/82** ca (qua 81, bỏ qua 1, hỏng 0), rc=0.
- Đột biến: **39/39** đạt (1 không đo được trên Linux), rc=0.
- Selftest: chạy thô trong sandbox **1695/1697**, chỉ r226/r268; chạy với duy nhất
  `commit.gpgsign=false` qua biến cấu hình Git đạt **1697/1697**, rc=0.
- Gate: **17/17** lệnh thực thi rc=0 với cùng biến Git; ruff `--select F` sạch.
- Manifest: **179** tệp, `required_missing=[]`; `release-verify --strict` rc=0.
- Git status cuối **không rỗng**: đúng bảy tệp dự kiến sửa/thêm. Commit không chạy
  được vì sandbox gắn metadata worktree read-only; Git báo không tạo được
  `index.lock` trong `.git/worktrees/wt-audit7`.

Nguyên nhân sandbox được xác định bằng đầu ra thật của ca commit repo tạm:
`environment-runner code-sign` thử gọi MCP ở `127.0.0.1`, nhận
`socket: operation not permitted`, sau hai lần thử thì Git báo
`fatal: failed to write commit object`. Vì CI không cài wrapper ký này, lượt gate
cuối tắt riêng `commit.gpgsign` ở môi trường tiến trình; không sửa cấu hình người dùng.
