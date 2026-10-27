Reviewed commit: 6f69f9de6675058a22f70697634f833b9a193f20
Verdict: approve — P1=0 P2=0 P3=0

Review độc lập Codex (OpenAI, agent qua API với shell cục bộ); executor Claude. KHO `/home/user/rv773` được giữ read-only, sạch trước/sau; chỉ sửa bản sao `/tmp/rv778-review` và artifact ngoài KHO. Tree `2121397a1e12840b89900991a64b4ce1821b0785`. Không có finding mở trong phạm vi mã/spec. Approval này không xác nhận điều kiện CI/land chưa đo được.

## Đã đo

### Định danh, phạm vi, kiểm tra cơ bản

- `git -C /home/user/rv773 rev-parse HEAD` khớp exact SHA dòng đầu. Spec đọc bằng `git show` trên các ref được giao. SHA256 r2 `c70c19b57ad1d9bf0304a04bbb259b0b74ebc366824c24597c7207b7beaf14a0`; r3 `81543d80b4d27cbecdcce4bfcdfe5a8974bb8a17cae6e8a2de56d0e53b4ee012`. Đã đọc bảng nghiệm thu r2/r3 và r1.
- `git diff --numstat fb490a7 HEAD`: registry 1 thêm/0 xóa; validator 321/0; test 424/0. Đúng ba tệp write set g1+g2; g1 **2 tệp / 745 dòng thêm**, dưới trần 750 được giao. `git diff --check fb490a7 HEAD` rc=0. `python3.13 -m ruff check --select F ops/land_evidence_nguon.py ops/land_evidence_nguon_test.py` rc=0, `All checks passed!`.
- So `8b496f9`, validator không đổi; test đổi docstring, thêm c09 mất miễn trừ nhưng đạt luật, thay chốt c11, thêm helper và c15. Đã đọc lại toàn validator và delta test; không phát hiện lỗi mới cần phân hạng.
- Bản sao tạo bằng `cp -a /home/user/rv773/. /tmp/rv778-review/`. Python 3.13.16. `python3.13 -B ops/land_evidence_nguon_test.py` rc=0: `CA: 15/15 dat`, `DOT BIEN: 37/37 bi giet dung ly do`, `TU KIEM PHAN HANG: DAT (2 dot bien)`, `TONG: DAT` (test-r3.log).
- `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false python3.13 -B .claude/dev/ci_dang_ky_test.py` trong bản sao rc=0: `PHẢN CHỨNG: 1025/1025 đỏ đúng`, `TỔNG: ĐẠT` (registry-r3.log). Override chỉ dành cho commit fixture của test, không sửa cấu hình KHO.

### Vá lượt 2 đã đóng và có phản chứng

Chạy `python3.13 -B probe-r3.py` (driver kèm theo, dùng bản sao tại đường dẫn trên), rc=0. c15 gốc `(0, '')`; sáu đột biến helper được nạp trong bộ nhớ, không sửa KHO:

| Đột biến `_cay_that_dat` | Kết quả c15 |
|---|---|
| Bỏ `and int(m.group(1)) <= n` | rc=3, `DO:c15… ['m>k']` |
| `<= n` → `< n` | rc=3, `['m=k']` |
| `<= n` → `== n` | rc=3, `['m<k']` |
| Bỏ `rc == 0` | rc=3, `['rc_1']` |
| Mẫu số cố định → `\d+` | rc=3, `['mau_so_sai']` |
| Cho thiếu match qua | rc=3, `['mau_so_sai', 'khong_dong']` |

Đều chết bằng `TinHieuChotCa`, không phải traceback. Chốt m≤k nay có răng, đóng P3 lượt 2. Bản gốc nhận m=k và m<k, từ chối m>k, sai mẫu số, rc=1 và thiếu dòng.

### Mẫu đăng ký và đường tiêu thụ

- r3 quy định **3 nhóm bắt**, thay yêu cầu 2 nhóm của r2. Dòng hiện tại khớp nguyên mẫu r3. `bang_chung_xanh` dùng `re.search(..., re.M)`; với ba nhóm, regex tự ép N/N và M/M dương bằng backreference. Đầu ra thật CA 15/15 phù hợp mẫu; không khóa cứng 14 ca.
- Probe qua chính `bang_chung_xanh` và `chay_moi` với runner trả rc=0: đầu ra hợp lệ qua, consumer rc=0. Tất cả trường hợp sau trượt, consumer rc=1: `TONG: DO`; CA 13/14; CA 0/0; DOT BIEN 0/0; DOT BIEN 36/37; thiếu DOT BIEN; dòng thừa sau cuối hoặc chen giữa tổng kết; đảo thứ tự; DO trước tổng kết; TU KIEM PHAN HANG DO trước tổng kết; dòng NHE; tiền tố CI trên từng dòng. Log trung tính trước tổng kết được nhận đúng chủ ý r3. Xem probe-r3.log.
- CRLF thô bị từ chối; đầu ra CRLF qua subprocess `text=True` được chuẩn hóa LF và được nhận. Runner thật `_chay_co_lap` dùng `text=True`, UTF-8 và `stderr=STDOUT`, nên không thấy lỗi CRLF ở đường dùng thực. Prefix timestamp do giao diện CI hiển thị không nằm trong buffer subprocess. Chưa chạy Windows thật.
- `python3.13 -B registry-mut-r3.py`: bỏ dòng đăng ký ⇒ rc=1, `test sống chưa đăng ký`; đổi đường dẫn ⇒ rc=1 và thêm `mục đăng ký không có tệp`. Đổi mẫu thành NEVER_MATCH, bỏ lookahead cấm DO, hoặc bỏ `\Z` ⇒ registry không `--chay` vẫn rc=0, 1025/1025. Probe chứng minh hai mẫu nới lỏng lần lượt nhận DO trước DAT và log sau DAT. Đây đúng là thiếu bảo vệ chung đã ghi ngoài phạm vi r3, không tính lại finding packet.
- Bộ mới không trong NHE/MAU_DAY_DU/các bộ chia mảnh. `ke_hoach(set()).get(path, (DAY_DU,))` trả `day_du`; `env_theo_che_do` trả `{}`; producer luôn chạy 37 đột biến, không có cờ nhẹ. Workflow gọi registry `--chay`. Trần mỗi bộ 5400 giây, job registry 105 phút; chưa thấy vấn đề timeout riêng do thêm bộ khoảng một phút. Không suy tổng thời gian toàn job từ thời gian một bộ.

### Cây thật và độ bền khi master thay đổi

- Gọi `kiem(nap(), Path('/home/user/rv773'))` từ test trong bản sao, rc=0: `2 ĐẠT · 28/28 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 30`, `TỔNG: ĐẠT`.
- Trong bản sao, thêm hồ sơ tương lai vô hại `x: ok` rồi gọi riêng c11 ⇒ rc=0. Thêm newline vào một hồ sơ miễn trừ vẫn đạt luật rồi gọi c11 ⇒ rc=0; hoàn nguyên ngay. Tăng số hồ sơ hoặc giảm m khi mất miễn trừ hợp lệ không còn gây đỏ giả.
- Hồ sơ tương lai thiếu nguồn vẫn làm rc checker khác 0 và c11 đỏ. Đây là rủi ro vận hành có thật, nhưng là enforcement theo Q2/L1/L5, không phải lỗi độ bền test: hồ sơ mới phải đạt luật; không được tự nối vào miễn trừ để xanh. Hai sự cố đã nêu phù hợp cơ chế này. Không xếp P1/P2/P3 khi hồ sơ vi phạm bị cổng từ chối đúng thiết kế.

- Consumer thật riêng mục mới: `python3.13 -B /tmp/consumer-r3.py` rc=0, `CI_DANG_KY ops/land_evidence_nguon_test.py: ĐẠT rc=0`; CA 15/15, DOT BIEN 37/37. Báo cáo ghi `che_do=day_du`, 2 worker, **41.366 giây** (consumer-r3.log). Driver gọi `chay_moi` với `_chay_that` thật và chỉ giới hạn tập mục cần chạy.

## Ngoài phạm vi

- Nợ chung của registry không `--chay`: chưa tự canh chất lượng mẫu của từng mục MOI. Các đột biến regex sống đã đo ở trên; r3 loại rõ việc sửa cơ chế này khỏi packet. Không thấy lý do kỹ thuật để phủ nhận phạm vi ấy.
- CI exact head **chưa xác nhận**. Lệnh read-only `gh api repos/ducthangho/tra-luat/commits/6f69f9de6675058a22f70697634f833b9a193f20/check-runs` rc=1: `proxyconnect tcp … socket: operation not permitted`. Hàng CI trong nghiệm thu r2 (mọi check xanh và log gate-registry trên đúng SHA) vẫn cần bằng chứng trước land; trạng thái đang chạy không được tính pass.
- Chưa chạy Windows thật hoặc toàn bộ registry `--chay`; consumer riêng mục mới được đo bên dưới. Không soạn bằng chứng nhạy cảm giả, không sửa hồ sơ KHO, không gửi comment/review GitHub, không merge/land hay cấp assurance human_audited.
