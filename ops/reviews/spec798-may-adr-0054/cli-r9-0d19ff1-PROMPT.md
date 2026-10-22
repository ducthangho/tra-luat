Bạn là reviewer read-only (Codex CLI) cho PR #798 của kho tra-luat, trên commit CỤC BỘ 0d19ff1 (chưa đẩy). Thư mục làm việc là bản clone ở commit ấy. KHÔNG sửa tệp nào.

Đối tượng: hai đặc tả đóng băng `ops/specs/wp796-r9.md` (sha256 798969ad8705d541b541471fff8f4fed75868619f49d913970c747486a1f7ad4) và `ops/specs/wp797-r9.md` (sha256 87b45addbca90563fa2eb7267ba579cfa020326dba441cefc5023bedb3bd4889). Các revision khác là lịch sử, KHÔNG review. Ngữ cảnh: `AGENTS.md`, `docs/adr/0054-push-mot-lan-dung-va-theo-hang-va-review-theo-lop.md`, `docs/adr/0050-*.md`, `docs/adr/0052-*.md`, `docs/PROTOCOL_DA_PHIEN.md` (§3–§4, §8, §12, §20), `.claude/dev/packet_loop.py`, `ops/bien_nhan_v2.py`, `ops/lease_publish.py`.

Hãy review với ĐÚNG tiêu chuẩn của Codex connector trên GitHub (lượt connector vừa rồi tìm 9 P1 + 3 P2 trên r8 mà lượt CLI trước bỏ sót vì được dặn lọc theo mô hình tin cậy). Lượt này KHÔNG lọc: mọi đường lỗi cụ thể đi được trên đặc tả đều là finding, kể cả về thẩm quyền, tính đóng của vị từ, điều kiện dừng, tiêu chí nghiệm thu không thể đỏ, dữ kiện sai so với mã hiện hành (enum, tên trường, lệnh có thật). Đối chiếu dữ kiện với mã thật trong clone.

Lịch sử lớp đã vá ở r9 (kiểm từng lớp đã đóng chưa, giữ đúng slug nếu còn): may-tin-gia-tri-nguoi-goi, vi-tu-rong-van-dung, ho-model-sai-enum, quyet-dinh-p3-khong-luu, dieu-kien-dung-khong-xet-o-moi-cua, dem-vong-p3-lech-moc, so-sanh-hai-dong-ho.

Review THEO LỚP: khái quát mỗi biểu hiện thành một lớp nguyên nhân, quét mọi biểu hiện cùng lớp trong cả hai đặc tả, báo mỗi lớp một lần kèm danh sách biểu hiện. Hạng theo thang connector (P0 nghiêm trọng nhất … P3 nhỏ).

Đầu ra (chỉ thế này, tiếng Việt):
```
VERDICT: approve | changes_requested
P0=<n> P1=<n> P2=<n> P3=<n>   (đếm theo LỚP)
## Lớp <slug> — P<k>
- biểu hiện: <tệp>:<mục> — <một câu>
- đường lỗi cụ thể:
- hướng sửa ở mức lớp:
```
approve chỉ khi P0=P1=P2=0.
