# Phần chung — packet MAY-ADR-0054-a…e (revision 1)

Đóng băng 17-10-2026. Mỗi đặc tả con dẫn tệp này bằng sha256; đổi tệp này là revision mới của **mọi** packet con.

## Nguồn

`docs/adr/0054-push-mot-lan-dung-va-theo-hang-va-review-theo-lop.md` §2 (năm yêu cầu cho packet máy) và mục *Hiệu lực*.
Chủ kho 17-10-2026: tách thành 5 packet tuần tự (#812 → #816), executor Antigravity `Amargon 4.0` effort high
(`provider: google_antigravity`, `model_family: gemini`, `execution_surface: antigravity`, `transport: machine/local`),
reviewer Codex (`model_family: openai`) ⇒ `cross_approved` theo `ADR-0050`.

Bản thiết kế gộp trước đây (wp796/wp797 r1–r10, commit `2cd0bcd` trên nhánh `claude/spec-p3-dot`) và 10 lượt review của nó
(`ops/reviews/spec798-may-adr-0054/`) là **đầu vào thiết kế**, không phải đặc tả: executor đọc để biết các đường lỗi đã lộ,
nhưng chỉ bị ràng buộc bởi bất biến dưới đây và mục tiêu của packet mình.

## Vì sao đặc tả dạng bất biến

Đặc tả gộp mô tả cơ chế bằng văn xuôi; mỗi revision thêm cơ chế nên thêm bề mặt, và review phân kỳ (Codex CLI 5 → 6 → 5 → 9 →
11 lớp qua r5–r10). Đặc tả con chỉ nói **điều gì phải luôn đúng** và **phép đo nào làm nó đỏ**; cơ chế do executor chọn và
review bắt lỗi trên **mã thật**.

## Mô hình tin cậy

`packet_loop.py` chạy cục bộ trong tay executor. Máy không chống được executor cố ý gian lận; thẩm quyền thật nằm ở lease
do workflow đăng, connector, CI và quyết định merge của chủ kho. Mỗi đầu vào thuộc một hạng:

| hạng | là gì |
|---|---|
| **Đ** | máy tự đo: object/ref git sau khi tự `git fetch`, `git ls-remote` |
| **H** | hiện vật trong git có validator sẵn: lease (`ops/lease_publish.py`), biên nhận (`ops/bien_nhan_v2.py`) |
| **R** | readback GitHub do người gọi lấy; máy chỉ kiểm nhất quán và ghi sha256 |

## Bất biến (mọi packet con phải giữ, review đo theo đây)

| # | bất biến |
|---|---|
| I1 | Chuyển trạng thái **mở thêm quyền** (vào `approved_pending`, vào `accepted`, rời `cho_chu_kho`, tạo generation, ghi một lần đẩy) có ít nhất một đầu vào hạng Đ hoặc H; hạng R chỉ bổ sung. |
| I2 | Lease có thẩm quyền khi đủ ba: (H) qua `ops/lease_publish.py check`; (Đ) `ai-dang-giu` sau fetch đủ ref theo CLAUDE.md trả nó là người giữ write set; (R, bổ sung) readback comment của `github-actions[bot]` trên Packet Issue chứa đúng `lease_id` — tức workflow đã **đăng**. Thiếu một ⇒ không có thẩm quyền. |
| I3 | Miền giá trị **đóng**: giá trị ngoài miền liệt kê (hạng ngoài {`P0`,`P1`,`P2`,`P3`}, kết luận check ngoài danh sách cho phép) ⇒ không đạt. Tập **bằng chứng dương** (check bắt buộc, finding dùng để mở lại) rỗng ⇒ không đạt; tập **finding còn mở** được phép rỗng (đó là kết quả sạch). |
| I4 | Lỗi **đầu vào** ⇒ từ chối, state giữ nguyên từng byte. Kết quả **hợp lệ** chạm điều kiện dừng ⇒ ghi sổ đủ rồi `blocked`. |
| I5 | Một hàm xét dừng duy nhất (`_xet_dung`, do **#812** viết), gọi ở mọi cửa **đưa packet đi tiếp** mà packet hiện hành mở hoặc sửa; cửa **khép** công việc (ghi kết quả lượt đang mở) không bị nó chặn. Packet sau thêm cửa mới thì gọi đúng hàm ấy. |
| I6 | Mọi quyền phái sinh (mở lại, checkpoint, ngoại lệ đẩy) neo `(nguyên nhân, generation, sha)`, bị thay khi có sự kiện cùng loại mới hơn, và mất sau khi dùng. |
| I7 | Check bắt buộc định danh bằng **(app, workflow, tên job)** và chỉ lấy attempt mới nhất của run mới nhất trên head (dùng `kiem-gate` sau khi #788 land, đúng protocol §10.2). Readback GitHub neo **một kho + một PR + một head**, và "đủ trang" đo bằng **tập ID phân biệt**, không bằng số đếm. Không so chéo hai không gian ID, không so đồng hồ máy với đồng hồ GitHub. |
| I8 | So danh tính lease ↔ biên nhận qua đúng hàm chuẩn hoá của `ops/bien_nhan_v2.py`; giá trị không ánh xạ được ⇒ không đạt. |
| I10 | Mỗi hiện vật dùng ở một cửa có **vai trò** khai rõ, và khớp đủ **(packet, generation, sha, spec_hash)** của đúng ngữ cảnh vai trò ấy: hiện vật **ứng viên** khớp generation hiện hành và SHA ứng viên; hiện vật **nguồn** (vd bằng chứng connector trên head đã mở lại, biên nhận finding muộn của generation trước) khớp generation và SHA **nguồn** đã ghi trong state. Lệch một trong bốn của vai trò mình, hay dùng sai vai trò ⇒ không đạt. |
| I11 | **Phân lớp là việc của reviewer.** Mọi finding đi vào bộ đếm (offline, connector, muộn) mang slug lấy từ bảng lớp trong biên nhận hạng H (I10); executor không tự đặt slug. Slug ổn định xuyên ID, nguồn và generation; đổi phải qua bảng nối có lý do trong biên nhận. |
| I9 | Packet không chịu `ADR-0054` đi đường cũ **y như trước**; mọi ca có sẵn của `packet_loop_test.py` vẫn ĐẠT (gồm `init` chưa có lease ⇒ `awaiting_lease`). Chế độ `ADR-0054` chỉ được xác định ở **đường lease mới** của `record-lease` (đọc lease từ ref remote); đường `record-lease` cũ (truyền trường lease trực tiếp) giữ nguyên và luôn cho `luat_adr0054: false`. |

## Điều kiện dừng và đẩy (mọi packet con)

Review Codex CLI offline neo SHA cục bộ, prompt nêu sha256 đặc tả con **và** tệp này; reviewer review **không lọc**
(chuẩn connector). Hết P0/P1/P2 thì dừng (tối đa hai vòng thêm vì P3, dừng nếu số lớp P3 không giảm). Đẩy **một lần**; CI
đỏ ⇒ chỉ vá CI kèm biên nhận; connector P0–P2 ⇒ DỪNG hỏi chủ kho. Trần lời gọi Codex mỗi PR theo `ADR-0052` (8). Diff mỗi
packet ≤ 450 dòng thêm (`ADR-0053`); vượt ⇒ DỪNG hỏi chủ kho. Không merge.

tran_loi_goi_codex: ADR-0052@8ab100793df9831505f495543a74044b91c2c9ab
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab
