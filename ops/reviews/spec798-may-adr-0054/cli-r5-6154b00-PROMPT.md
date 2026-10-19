Bạn là reviewer read-only (Codex CLI) cho PR #798 của kho tra-luat, trên commit CỤC BỘ 6154b00 (chưa đẩy). Thư mục làm việc là bản clone ở commit ấy. KHÔNG sửa tệp nào.

Đối tượng review: hai đặc tả đóng băng `ops/specs/wp796-r5.md` (sha256 2f145f4ede67b2d120a2ae35a6c26633307126219c3c14811f40855fd2e7ca94) và `ops/specs/wp797-r5.md` (sha256 d008e75795180c46200f2f8a5cfca83163dc07f46c526b816e247c16d7173284). Các tệp `wp79x.md`, `-r2.md`, `-r3.md`, `-r4.md` là lịch sử, KHÔNG review. Ngữ cảnh: `docs/adr/0054-push-mot-lan-dung-va-theo-hang-va-review-theo-lop.md`, `docs/PROTOCOL_DA_PHIEN.md` (§4, §8.3, §12, §20), `.claude/dev/packet_loop.py`, `ops/bien_nhan_v2.py`, `ops/lease_publish.py`.

Ba lượt connector trước đã bắt 11 → 11 → 13 finding, gần như cùng ba lớp. r4 vá theo lớp: thêm mục "Mô hình tin cậy" (hạng Đ/H/R; chuyển mở quyền phải có ít nhất một đầu vào Đ hoặc H; executor cố ý gian lận là NGOÀI phạm vi máy, thẩm quyền thật nằm ở lease workflow, connector, CI, chủ kho merge). Đánh giá ĐẶC TẢ theo mô hình ấy: một finding chỉ hợp lệ nếu (a) vi phạm chính luật của mô hình tin cậy, hoặc (b) là lỗi đúng sai/nhất quán/tiêu chí không thể đỏ, hoặc (c) chính mô hình tin cậy mâu thuẫn với ADR-0054/protocol. "Executor gian lận có thể làm giả X" KHÔNG phải finding nếu X thuộc hạng R chỉ bổ sung, hoặc nếu chuyển ấy thu hẹp quyền.

Review THEO LỚP: khái quát mỗi biểu hiện thành một lớp nguyên nhân, quét mọi biểu hiện cùng lớp trong cả hai đặc tả, báo mỗi lớp một lần kèm danh sách biểu hiện.

Đầu ra (chỉ thế này, tiếng Việt):
```
VERDICT: approve | changes_requested
P0=<n> P1=<n> P2=<n> P3=<n>   (đếm theo LỚP)
## Lớp <slug> — P<k>
- biểu hiện: <tệp>:<mục> — <một câu>
- vì sao là lỗi theo (a)/(b)/(c):
- hướng sửa ở mức lớp:
```
approve chỉ khi P0=P1=P2=0.

Lượt CLI trước (trên r4) ra 5 lớp: hien-vat-hop-le-chua-du-tham-quyen (P1), checkpoint-chu-kho-bi-day-qua-thoi-diem-va (P1), chuyen-generation-giu-nham-ngu-canh-thuc-thi (P2), tu-choi-verdict-lam-mat-lich-su-va-budget (P2), ca-nghiem-thu-khong-phan-biet-dung-sai (P2). Kiểm từng lớp đã đóng chưa (giữ đúng slug nếu còn), rồi quét lớp mới.
