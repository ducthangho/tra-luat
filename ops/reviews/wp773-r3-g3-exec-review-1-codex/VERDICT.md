Reviewed commit: 128b2e892f91dd353367c082bfc9cf2c300ecfb7
Verdict: request_changes — P1=0 P2=2 P3=0

Reviewer: OpenAI Codex, họ GPT-6, phiên độc lập với executor Claude; công cụ shell chạy trực tiếp trong sandbox. Không có bằng chứng runtime để tự chứng nhận launcher/model receipt; không tự cấp assurance land. Review read-only đối với `/home/user/rv773`; mọi bản sao, phép đo và artifact nằm ngoài KHO.

## F1 — P2 — Mẫu nhận bằng chứng có đột biến sống hoặc tổng kết đỏ

Vị trí: `.claude/dev/ci_dang_ky_test.py:53` (g2).

Mẫu có đúng hai nhóm bắt nhưng chỉ kiểm hai số CA. Hai số DOT BIEN chỉ bị ép dương, không bị ép bằng nhau. `re.search(..., re.M)` cùng `(?s)` và `.*` còn cho phép bỏ qua dòng đỏ, nhận một dòng `TONG: DAT` khác, hoặc nhận tổng kết DAT trước một tổng kết DO. Điều này không đạt yêu cầu nghiệm thu “đầu ra hỏng không qua”, dù dòng đăng ký đúng nguyên mẫu Q1-r2.

Tái hiện: sau `cp -a /home/user/rv773 /tmp/review773`, chạy `python3.13 -B ./probe773.py`. Script gọi chính `bang_chung_xanh` và `chay_moi` với bộ duy nhất mới đăng ký, runner giả trả rc=0. Kết quả trong `probe.log`:

```text
groups 2
DB_36_37 bang_chung_xanh= True chay_moi_rc= 0
extra_error bang_chung_xanh= True chay_moi_rc= 0
DO_then_DAT bang_chung_xanh= True chay_moi_rc= 0
selfcheck_DO bang_chung_xanh= True chay_moi_rc= 0
```

Đầu vào là tổng kết thật, lần lượt đổi 37/37 thành 36/37; nối `TONG: DO` phía sau; đặt DO trước DAT; đổi tự kiểm thành DO. Đây là đo tầng tiêu thụ bằng seam, không phải khẳng định bộ test hiện tại tự trả rc=0 khi thất bại. Hiện producer trả rc=1 khi đột biến sống nên kiểm rc còn bảo vệ đường chạy thật; lỗi nằm ở lớp bằng chứng độc lập và khả năng bắt hồi quy.

Đột biến trên chính mục đăng ký cũng chưa được khóa: `NEVER_MATCH` và `.*` đều chạy registry không `--chay` rc=0, `PHẢN CHỨNG: 1025/1025 đỏ đúng`, `TỔNG: ĐẠT`. Tái hiện:

```sh
cd /tmp/review773
GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false python3.13 -B /path/to/output/mutate773.py wrong_pattern
GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false python3.13 -B /path/to/output/mutate773.py permissive
```

Driver chỉ thay chuỗi mã trong bộ nhớ rồi chạy entrypoint thật với `__file__` gốc của bản sao. Log đầy đủ: `mutation-pattern.log`, `mutation-permissive.log`. Bỏ mục hoặc sai đường dẫn bị registry bắt đúng; sai mẫu chỉ chắc chắn bị phát hiện khi thực thi consumer và đầu ra tương ứng không khớp.

Đề xuất sửa: tại dòng 53, dùng nhóm không bắt và backreference/lookahead để buộc số đột biến bằng nhau, giữ đúng hai nhóm CA; ràng buộc tổng kết cuối và từ chối tổng kết mâu thuẫn/tự kiểm DO. Thêm phản chứng qua chính `chay_moi` cho các trường hợp trên, rc khác 0, và đột biến mẫu sai/rộng. Rủi ro vá: neo toàn chuỗi quá chặt có thể từ chối log hợp lệ; kiểm lại output thật và đường LF/CRLF của subprocess. Vì r2 ghim nguyên mẫu và đúng một dòng thêm, cần điều phối sửa spec/write set trước khi thêm phản chứng; reviewer không tự mở phạm vi.

## F2 — P2 — `c11` buộc hồ sơ luôn giữ miễn trừ dù đã đạt luật

Vị trí: `ops/land_evidence_nguon_test.py:270` (g1, nay được nối CI bởi dòng 53 của g2).

`c11` bắt `28/28 miễn trừ` trên cây sống. Theo Q2/L5, hồ sơ thay byte phải mất miễn trừ và được kiểm đủ luật; hồ sơ đã đạt luật phải được chấp nhận. Chốt này làm CI đỏ với cập nhật hợp lệ của hồ sơ cũ, dù bộ kiểm rc=0. Nó biến snapshot cutover thành điều kiện giữ nguyên vĩnh viễn nội dung cây sống.

Tái hiện: `python3.13 -B ./operation773.py` trên bản sao tạm. Script chọn tên đầu tiên trong danh sách miễn trừ, thêm một newline rồi khôi phục bằng `finally`. Không đổi mã bộ kiểm. Kết quả `operation.log`:

```text
baseline checker_rc 0 ... 2 ĐẠT · 28/28 miễn trừ ... tổng 30
baseline c11 (0, '')
exempt_byte_change checker_rc 0 ... 3 ĐẠT · 27/28 miễn trừ ... 0 vi phạm ... tổng 30
exempt_byte_change c11 (3, 'DO:c11_cay_that_dat_va_mien_tru_du:...')
```

Đổi hồ sơ ấy thành YAML vô hại hợp lệ cũng cho checker rc=0 nhưng c11 rc=3. Thêm một hồ sơ mới hợp lệ cho checker rc=0, `3 ĐẠT · 28/28 miễn trừ`, c11 rc=0: việc tăng số hồ sơ tự nó không gây vỡ. Hồ sơ mới thiếu nguồn sẽ làm c11 đỏ qua rc của checker; đó là cổng L1 chủ ý, không phải false positive. Hai sự cố thiếu nguồn đã nêu cho thấy cần áp dụng cổng cho hồ sơ tương lai; không nên chữa bằng mở rộng miễn trừ.

Đề xuất sửa: ở c11 chỉ đòi cây sống đạt luật; chuyển chốt đủ miễn trừ sang fixture snapshot độc lập. Giữ c09 kiểm mất miễn trừ và c10 khóa danh sách/băm. Thêm ca hồi quy: hồ sơ miễn trừ thay byte nhưng vẫn hợp lệ phải xanh; hồ sơ mất miễn trừ có vi phạm vẫn đỏ; danh sách miễn trừ đổi vẫn đỏ. Rủi ro vá: bỏ điều kiện m=k đơn thuần có thể làm mất kiểm kê snapshot, nên phải giữ chốt snapshot riêng. Đây là finding toàn PR về tác động khi nối CI, không phải tuyên bố g1 đổi sau lượt approve trước; sửa vượt write set riêng g2, cần authority tương ứng.

## Đã đo

- HEAD KHO đúng SHA dòng đầu; tree `b01215cb9486206c7c115a1e40f4789597a46d89`; status sạch trước/sau. Base so diff: `fb490a7c3fa2992c6f4635ed091dafa813df2fe7`.
- Spec đọc từ `origin/ops/wp773-r2-g2-lease` tại OID `c311c61707eb3a2bc51c81b9b884e665a01f90ce`, đúng path được giao. `git show ... | sha256sum` = `c70c19b57ad1d9bf0304a04bbb259b0b74ebc366824c24597c7207b7beaf14a0`.
- `git diff --numstat fb490a7 128b2e8`: registry 1 thêm/0 xóa; bộ kiểm 321/0; test 402/0. Đúng ba tệp trong write set g1+g2. `git diff 8b496f9 128b2e8 -- ops/land_evidence_nguon.py ops/land_evidence_nguon_test.py` rỗng; không có delta g1 cần review lại toàn bộ theo mục 5.
- `git diff --check fb490a7 128b2e8` rc=0. Ruff `--select F` trên hai tệp g1 rc=0.
- Python 3.13.16, bản sao `/tmp/review773`: `python3.13 -B ops/land_evidence_nguon_test.py` rc=0, CA 14/14, DOT BIEN 37/37 bị giết đúng lý do, tự kiểm DAT, TONG DAT (`test.log`).
- `python3.13 -B .claude/dev/ci_dang_ky_test.py`: lần đầu rc=1 do git global bật ký SSH với key không có trong môi trường. Chạy lại với `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false` rc=0, đăng ký 24/24, phản chứng 1025/1025 (`registry.log`). Chỉ override cấu hình cho tiến trình tạo kho tạm, không sửa config KHO.
- `python3.13 -B ops/land_evidence_nguon.py --root /home/user/rv773` từ bản sao rc=0: `2 ĐẠT · 28/28 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 30` (`real-tree.log`).
- Mẫu thật khớp nhóm `('14', '14')`. Các biến thể chỉ có TONG DO, CA 13/14, DOT BIEN 0/0, thiếu DOT BIEN, đảo thứ tự, CA 0/0, NHE, CRLF thô, tiền tố LOG từng dòng đều bị từ chối (consumer rc=1). Dòng thêm trung tính giữa tổng kết được nhận; không tự coi log trung tính là lỗi. Các trường hợp mâu thuẫn được nêu ở F1.
- Gọi consumer thật chỉ với mục mới, `so_worker=2`, không thay runner: rc=0 trong 41,00 giây, có `CI_DANG_KY ops/land_evidence_nguon_test.py: ĐẠT rc=0` (`probe.log`). Bộ không nằm trong NHE, MAU_DAY_DU hay nhóm chia mảnh; kế hoạch không có bộ này nên fallback `day_du`, không truyền cờ cắt vòng đột biến. Trần một bộ 5400 giây, job 105 phút; thời gian đo không chỉ ra vấn đề timeout.
- GitHub API read-only lúc khoảng 2026-10-18T03:18Z: [run 39093007806](https://github.com/ducthangho/tra-luat/actions/runs/39093007806) của exact head còn `in_progress`; `gate-registry (ubuntu-latest)` job 117573575709 đã success. Log xác nhận CA 14/14, DOT BIEN 37/37, dòng CI_DANG_KY bắt buộc; JSON ghi rc=0, `che_do=day_du`, 28,357 giây. Checkout thực tế là merge ref `7cf03f5`, log ghi rõ merge exact head vào `fb490a7`. `gate-ops`, `gate` và các job khác còn chạy: chưa đạt tiêu chí “mọi check xanh”. Trích log lưu `CI-evidence.log`; không suy pending thành pass.

## Ngoài phạm vi

- Không sửa mã hay hồ sơ KHO, không đăng comment/review lên GitHub, không merge hoặc land. Chưa đo Windows, toàn bộ `--chay` cục bộ và kết quả cuối các job CI đang chạy; đã đo riêng consumer thật của mục mới và log CI Ubuntu.
- Mẫu Q1-r2 và trần đúng một dòng khiến việc khắc phục F1 cần revision/authority nếu thêm test. F2 thuộc g1 hiện có và tác động vận hành toàn PR được yêu cầu đánh giá; không tự coi lease g2 cho phép sửa nó.
- Review trước ở `8b496f9` được dùng làm mốc delta, không thay thế phép đo mới. Không mở lại review thuật toán g1 không đổi ngoài rủi ro cây sống được giao rõ trong lượt này.
