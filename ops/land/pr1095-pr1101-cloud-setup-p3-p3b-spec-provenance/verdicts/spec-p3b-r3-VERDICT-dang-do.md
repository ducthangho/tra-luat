verdict: pending
reviewed_sha: c6e4388ae1fece11f735f4cbe234de04fea56b37
reviewed_tree: 7d808014be27ff5646f996885a99a1f813645020

## DANH TÍNH

Đang đo danh tính và kiểm tra cây chỉ đọc.

Đo đầu lượt:

```text
$ git -C cay-kho rev-parse HEAD HEAD^{tree}
c6e4388ae1fece11f735f4cbe234de04fea56b37
7d808014be27ff5646f996885a99a1f813645020
$ git -C cay-kho status --porcelain=v1 --ignored
(output rỗng)
$ sha256sum cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r{1,2,3}.md
15fe242a65c8df1ff393cdc15784642013e904bacb9b754b0d72a64237dac11e  r1
c6e53a00c7370ce0d75d9bcd954f8b7e69aa7383a0f5e6427a29e5e0d0e3ed8d  r2
e2246e90aaf35b6b006b40a258e694a99c796a1ff1a8ac21aebb408121efa121  r3
```

Khớp HEAD, tree và SHA-256 r3 được giao; cây sạch, kể cả ignored. Bản hiệu lực: r3. Không dùng mạng, dịch vụ hay credential thật.

## FINDINGS (ghi tăng dần)

### F01 — P2 — `auth-hint-khong-ben-qua-ba-probe`

- **Tệp:dòng:** `ops/specs/cloud-setup-p3b-nlm-401-r3.md:99–100` (cùng khẳng định ở dòng 232; write_set cấm sửa `tl_gws.py` ở dòng 58–60).
- **Mô tả:** `_nlm_auth_alive` không chứng minh `auth_hint` bền qua cả ba probe. Hàm chỉ xét `r` của probe CUỐI (`tl_gws.py:333–355`). Hai probe đầu lỗi mạng rồi probe cuối lỗi auth vẫn trả `False`/mã 3, và đặc tả sẽ cho tự ghi đè jar dù tiền đề “auth_hint bền qua 3 lần” chưa được chứng minh. A13 chỉ thử ba lỗi đồng nhất, nên không phát hiện lớp này. Đây là khẳng định sai về hành vi mã đang làm nền cho chốt fail-close, không phải yêu cầu sửa mã cũ vô điều kiện.
- **Phép đo tái hiện đã chạy:** `python3 -B review_probe.py` (rc 0), AST lấy nguyên hai hàm `_nlm_auth_alive`/`_nlm_canary_raw_get` từ đúng checkout; `_imp` trả `nlm_cli` giả, không ngủ và không mạng. `connection refused` ×3 ⇒ `None`/mã 2; `HTTP 403 permission denied` ⇒ `None`/mã 2; `Authentication expired` ×3 ⇒ `False`/mã 3. Nhưng chuỗi `[connection refused, connection refused, Authentication expired]` và `[Authentication expired, connection refused, Authentication expired]` cũng ⇒ `False`/mã 3. Tiến trình con vô hại xác nhận cùng mã. Bằng chứng: `review_probe.results.json`.
- **Đề xuất sửa:** ra revision mới xác định rõ độ bền cần đo; nếu vẫn yêu cầu cả ba probe có auth_hint, thêm phép đo chuỗi trộn vào A13 và triển khai chốt thực sự (mở write_set cho helper/test cần thiết, hoặc thiết kế wrapper trong tệp đã được phép). Không mô tả helper hiện tại là đã cưỡng chế điều kiện ấy.

### F02 — P2 — `D1-khong-khop-markdown-giu-nguyen`

- **Tệp:dòng:** `ops/specs/cloud-setup-p3b-nlm-401-r3.md:157` (ràng buộc giữ chữ cũ: dòng 125–127).
- **Mô tả:** D1 yêu cầu chuỗi `CẤM tự` còn ở MỖI tệp sau khi chỉ gộp khoảng trắng. `QUY_TRINH_RA_SOAT_3_TANG.md:49` thực tế viết `**CẤM** tự`; gộp khoảng trắng không bỏ dấu `**`. Câu ngoại lệ bắt buộc thêm cũng không chứa `CẤM tự`. Vì vậy làm đúng mục tiêu 5 (“Mọi chữ cũ giữ”) vẫn làm D1 đỏ; đặc tả chưa có thước đo thực thi nhất quán (L3/L6b).
- **Phép đo tái hiện đã chạy:** `python3 -B review_probe.py` (rc 0). Đọc hai tài liệu và chỉ thêm câu ngoại lệ chính xác trong RAM, gộp bằng `' '.join(text.split())`: số câu ngoại lệ sau thêm = 1 ở mỗi tệp; `CẤM tự` có ở RASOAT nhưng không có ở QUY_TRINH cả trước lẫn sau thêm. Chạy nguyên thân ca `r213_auth_carve_out_khong_pha_thu_tu` với các hằng thật và đường đọc tài liệu giả trong RAM: base và bản thêm đều `True`; **không cần sửa `tl_selftest.py` để giữ r213**. Bằng chứng: `review_probe.results.json`.
- **Đề xuất sửa:** quy định bỏ markup inline trước khi kiểm, hoặc kiểm riêng mẫu đúng của mỗi tệp (`CẤM tự` và `**CẤM** tự`) trên đoạn đã nối dòng, kèm phép dương/âm/đột biến. Giữ nguyên ca r213 và điều cấm dành cho agent.
