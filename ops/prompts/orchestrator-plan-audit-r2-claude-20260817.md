# Vòng 2 — phản biện Codex và đề nghị hội tụ

Tiếp tục đúng session Reviewer read-only của vòng 1. Không sửa file. Hãy phản biện các kết luận dưới đây dựa trên
code và số đo, rồi cho biết `AGREE | AGREE_WITH_CHANGE | DISAGREE` từng mục. Mục tiêu là hội tụ trong khung 9 điểm
chủ kho đã chốt, không tối đa hóa số thay đổi.

## Điểm Codex đồng ý

1. **F2:** thứ tự §7.5 đang sai. Target phải là `begin-attempt`/publish handoff/`record-post`/`transition reviewing`
   trước model review; `record-review` sau output + publish/readback.
2. **F4:** tách `codex_review_calls_used` khỏi `codex_executor_calls_used`; có thể có total derived, nhưng trần hai
   call/PR chỉ áp review. Executor call không ăn review quota.
3. **F6:** Packet đang rework vì finding được ưu tiên ở **slot kế tiếp**, không cưỡng bức ngắt writer đang chạy;
   pin mọi `planned:` thành path/prefix cụ thể trước claim.
4. **F7:** §13 phải khai L9 skipped riêng.

## Điểm cần chỉnh cách chữa

### F1 — hai environment có thể cùng đúng

Vòng 1 chạy ngoài sandbox dưới user `admin`: Codex/GitHub/PyYAML khỏe hơn. Lượt lập kế hoạch chạy trong sandbox
`CodexSandboxOffline`: Codex probe `PermissionError`, GitHub `CHUA_XAC_THUC`, PyYAML thiếu. Đây chính là bài học
environment-scoped; không nên viết đè snapshot cũ thành “sai”.

Codex đồng ý bug probe cụ thể: launcher tính `shutil.which('codex')` rồi gọi tên trần, không thử candidate kế tiếp.
Đề nghị:

- giữ hai fingerprint có actor/environment/time riêng;
- thêm Packet **W0-M3** (không dùng hậu tố M1b) cho probe path/candidate fallback; W0-M2 giữ encoding truth;
- W0-M3 chạy sau W0-M1 vì cùng `launcher_test.py`, có thể trước hoặc sau W0-M2 nhưng không song song;
- sửa mọi kết luận khả dụng thành environment-scoped, không tuyên bố Codex toàn kho hỏng/khỏe.

Bạn có đồng ý không? Có cần W0-M3 đứng P0 trước W0-M2 không?

### F3 — tái dùng receipt, nhưng không bắt tag tuyệt đối

Đồng ý không tạo schema song song. Đề nghị:

- W0-R2 nâng `review_delivery_receipt` hiện có lên revision mới, thêm/chuẩn hóa
  `model_reviewer_identity` và `github_submitter_identity`, giữ compatibility với `delivered_by` /
  `receipt_written_by`, giữ `t26`/`t27`;
- Packet state chỉ tham chiếu receipt ID/hash và các identity đã validate, không tự nhận raw fields không có receipt;
- tách W0-R3 nếu việc nối `packet_loop` với receipt làm W0-R2 chạm hai seam quá rộng;
- durable anchor là contract: canonical ancestry **hoặc** protected `luu-tru/*` tag/check object phù hợp. Không yêu
  cầu tạo tag cho mọi verdict nếu canonical/check đã cho đường readback bền.

Bạn có đồng ý contract anchor tổng quát này, hay có bằng chứng protocol hiện tại bắt tag cho mọi verdict?

### F5 — đồng bộ skill sau khi prompt transport có hình dạng thật

Đồng ý dossier không được dựng công thức trái skill. Đề nghị Packet **W1-S1** sau W1-P1 + W0-R2, không W0-S1:

- trước W1-S1, bootstrap dùng adapter hiện tại và khai caveat transport;
- W1-S1 chỉ đổi cú pháp adapter mỏng để gọi launcher/transport đã land;
- tiếp tục dùng review sandbox chuẩn bị sẵn, phạm vi đọc đóng; không chuyển sang full review worktree chỉ vì
  `read-only` chặn ghi;
- dossier §7.4 ghi target-after-W1-S1, không khai là current command.

Bạn có đồng ý thứ tự này không?

## Finding mới từ chính lượt gọi vòng 1 — deadline có vẻ không cưỡng chế

Launcher record của vòng 1 thật:

```text
bat_dau_utc  = 2026-08-17T13:48:47.077426+00:00
deadline_utc = 2026-08-17T14:18:46.257012+00:00
ket_thuc_utc = 2026-08-17T14:46:23.279132+00:00
trang_thai   = xong
ma_thoat     = 0
duration     = 3456.202s
```

Code `launcher.py:1389+` có vẻ dùng `p.wait(timeout=con_lai)`, nhưng số đo cho thấy process sống thêm ~27 phút
sau deadline mà không thành `qua_han`. Hãy kiểm code/test và phân biệt: lỗi launcher, clock/record artifact, hay
cách wrapper Claude/Job Object khiến timeout không cưỡng chế. Nếu chưa đủ để chẩn đoán, hãy đề nghị Packet phản
chứng nhỏ thay vì kết luận nguyên nhân. Điều này có cần thêm W0-M4 không?

## Đầu ra vòng 2

1. Bảng verdict cho 7 finding vòng 1 + finding deadline mới.
2. Danh sách điều chỉnh đã đồng thuận trong khung.
3. Danh sách bất đồng còn lại cần vòng 3.
4. Chỉ mục nào thật sự đổi 9 điểm khung mới được gắn `OWNER_DECISION`; đừng nâng thay đổi Packet thành đổi khung.
