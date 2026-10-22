Reviewed commit: 92df2756e2018f833da34211afbf8b20ebbdcc6e
Verdict: request_changes — P1=0 P2=0 P3=1

Review độc lập Codex, read-only đối với `/home/user/rv773` (KHO). Bản sao thực thi `/tmp/rv773-r2`; không sửa KHO, không gửi review/comment hay land. Không tự cấp assurance `human_audited`.

## F1 — P3 — Chốt mới `m ≤ k` chưa có phản chứng bảo vệ

Vị trí: `ops/land_evidence_nguon_test.py:275`.

Vá F2 đã sửa hành vi hiện tại đúng: c11 chấp nhận hồ sơ mất miễn trừ nhưng vẫn đạt luật. Tuy nhiên bỏ riêng `and int(m.group(1)) <= n` không làm bất kỳ ca hay đột biến tích hợp nào đỏ. Đây là thiếu bảo vệ hồi quy của chốt mới, đúng phép đo được yêu cầu ở lượt này; chưa phải lỗi validator đang chấp nhận hồ sơ sai trên cây thật. Phân hạng P3 vì tác động hiện tại là độ bền kiểm thử, không phải vi phạm luật nguồn đang lọt CI.

Tái hiện (driver và log kèm trong thư mục ra):

```sh
cp -a /home/user/rv773 /tmp/rv773-r2
cd /tmp/rv773-r2
python3.13 -B /path/to/output/mutate-r2.py bound
python3.13 -B /path/to/output/probe-r2.py
```

Driver `bound` chỉ bỏ điều kiện trên trong mã test nạp ở bộ nhớ, rồi chạy entrypoint đầy đủ. Kết quả đo (`mut-bound.log`): rc=0, `CA: 14/14 dat`, `DOT BIEN: 37/37 bi giet dung ly do`, `TU KIEM PHAN HANG: DAT (2 dot bien)`, `TONG: DAT`.

Probe thay seam `kiem` của c11 bằng rc=0 và tổng kết `29/28 miễn trừ`, để xác nhận đột biến có đổi hành vi:

```text
c11_fake29 original (3, 'DO:c11_cay_that_dat_va_mien_tru_du:...29/28 miễn trừ')
c11_fake29 no_bound (0, '')
```

Đề xuất: thêm phản chứng tự kiểm c11 bằng đầu ra giả qua seam, khóa các chiều rc khác 0, mẫu số sai, m>k bị từ chối, m=k và m<k hợp lệ được nhận. Đưa đột biến bỏ giới hạn vào phép tự kiểm đó để bản gốc xanh và bản bỏ chốt đỏ đúng lý do. Không cần phụ thuộc nội dung hồ sơ thật để tạo m>k. Khoản ngoài phạm vi r3 về đột biến mục `MOI` không bao phủ thay đổi g1/c11 này.

## Đã đo

- KHO đúng exact SHA dòng đầu, `git status --short` sạch trước/sau. Spec đọc trực tiếp bằng `git show` từ ba ref lease được giao. SHA256 r2: `c70c19b57ad1d9bf0304a04bbb259b0b74ebc366824c24597c7207b7beaf14a0`; r3: `81543d80b4d27cbecdcce4bfcdfe5a8974bb8a17cae6e8a2de56d0e53b4ee012`.
- `git diff --numstat fb490a7 92df275`: registry 1 thêm/0 xóa; validator 321/0; test 407/0. Đúng ba tệp thuộc write set g1+g2. `git diff --check` sạch. Ruff F trên hai tệp g1: `All checks passed!`.
- So với `8b496f9`, validator g1 không đổi; test chỉ đổi docstring, thêm ba dòng c09 và sửa c11 như diff vá F2. Đã đọc lại delta này và spec r1 L1–L5/Q2/Q6; không tìm thêm lỗi thuật toán trong delta.
- Python 3.13.16. `python3.13 -B ops/land_evidence_nguon_test.py` trong bản sao rc=0: CA 14/14, DOT BIEN 37/37 bị giết đúng lý do, tự kiểm 2 đột biến DAT, TONG DAT (`test-r2.log`). Ca c09 gọi riêng rc=0.
- `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false python3.13 -B .claude/dev/ci_dang_ky_test.py` rc=0: `PHẢN CHỨNG: 1025/1025 đỏ đúng`, `TỔNG: ĐẠT` (`registry-r2.log`). Override chỉ áp dụng tiến trình tạo repo fixture, không sửa cấu hình KHO.
- Bộ kiểm từ bản sao, `--root /home/user/rv773`, rc=0: `2 ĐẠT · 28/28 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 30`; `TỔNG: ĐẠT`.
- Mẫu r3 có **3 nhóm bắt**, đúng revision mới, thay yêu cầu 2 nhóm của r2. `bang_chung_xanh` gọi `re.search(..., re.M)` và bỏ phép so hai nhóm khi có ba nhóm; backreference trong regex tự ép N/N và M/M dương. Mẫu thật qua, consumer rc=0.
- Qua chính `bang_chung_xanh` và `chay_moi` với runner seam rc=0: CA 13/14, CA 0/0, DOT BIEN 0/0, DOT BIEN 36/37, thiếu DOT BIEN, chỉ TONG DO, DO trước/sau tổng kết DAT, tự kiểm DO, dòng thừa sau cuối hoặc chen giữa bốn dòng, sai thứ tự, đầu ra NHE, tiền tố LOG ở từng dòng đều bị từ chối; consumer rc=1 (`probe-r2.log`). Bốn dòng tổng kết liền nhau ở cuối được khóa đúng. Log trung tính trước tổng kết vẫn được phép theo r3.
- CRLF thô không khớp, nhưng subprocess thật dùng `text=True`, `stderr=STDOUT` chuẩn hóa CRLF thành LF: đầu ra CRLF qua `subprocess.run(..., text=True)` được mẫu nhận. Không thấy lỗi Windows/CRLF ở tầng regex; chưa chạy Windows thật. Tiền tố timestamp do giao diện CI hiển thị không nằm trong chuỗi subprocess mà regex nhận.
- Bỏ dòng đăng ký: rc=1, `test sống chưa đăng ký`. Sai đường dẫn: rc=1, thêm `mục đăng ký không có tệp`. Sai mẫu `NEVER_MATCH`: registry rc=0, 1025/1025. Bỏ lookahead cấm DO hoặc bỏ `\Z`: registry vẫn rc=0, 1025/1025; probe tương ứng nhận DO trước DAT hoặc log thừa sau DAT. Đây là nợ chung đã được r3 loại khỏi phạm vi, không đếm finding mới.
- Consumer thật chỉ chạy mục mới (`consumer-r2.py`), 2 worker, rc=0 sau 40,71 giây: `CI_DANG_KY ops/land_evidence_nguon_test.py: ĐẠT rc=0`; báo cáo ghi `che_do=day_du`, CA 14/14 và DOT BIEN 37/37 (`consumer-r2.log`).
- Bộ mới không nằm trong NHE, MAU_DAY_DU hay các bộ chia mảnh. `chay_moi` fallback `DAY_DU`; producer không có cờ nhẹ, luôn chạy vòng 37 đột biến. Workflow gọi registry `--chay`. Trần một bộ 5400 giây, job 105 phút; thời gian khoảng một phút không chỉ ra vấn đề timeout riêng cho mục mới.
- Đo vận hành trong bản sao: thêm newline vào một hồ sơ miễn trừ vẫn đạt luật ⇒ checker rc=0, c11 rc=0 (m giảm xuống 27/28). Thêm hồ sơ tương lai hợp lệ ⇒ checker rc=0, c11 rc=0. Không còn false positive giữ m=k của F2 cũ. Hồ sơ tương lai vi phạm L1 sẽ làm cây thật đỏ theo rc: đó là cổng chủ ý của Q2/L5, không phải test dễ vỡ do tăng số hồ sơ. Hai sự cố thiếu nguồn trước đây là vi phạm cần sửa ở hồ sơ, không nên mở rộng miễn trừ. Rủi ro CI đỏ khi hồ sơ tương lai sai luật còn tồn tại theo thiết kế; không xếp finding.
- GitHub API read-only cho exact head không truy cập được: `proxyconnect tcp ... socket: operation not permitted`. Vì vậy chưa xác nhận hàng CI của bảng nghiệm thu (mọi check xanh và log exact head); không suy trạng thái đang chạy thành pass.

## Ngoài phạm vi

- Theo r3: cơ chế registry không `--chay` chưa tự phát hiện mẫu MOI sai/rộng, áp dụng mọi mục. Đã đo và ghi nợ, không yêu cầu sửa cơ chế chung trong packet này. Hai mutant regex sống không được tính lại thành F1 của lượt 1.
- Chưa chạy Windows thật, toàn bộ registry `--chay` cục bộ, hoặc xác nhận kết quả CI từ xa. Đã chạy riêng consumer của mục mới; chi tiết log nằm trong artifact kèm theo.
- Không soạn nội dung bằng chứng nhạy cảm giả. Probe chỉ dùng tổng kết test, seam và hồ sơ vô hại. Không sửa hồ sơ thật, không thay lease/spec, không cấp quyền land.
