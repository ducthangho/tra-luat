# ĐO ĐỘC LẬP — phiên chính, sau vòng 1 (21-08-2026)

Mọi số dưới đây do PHIÊN CHÍNH tự chạy trên cây làm việc, KHÔNG lấy từ báo cáo nào.

## 1. Kiểm lại phép đo mới của Fable (`seam`)
- `seam` trong `ops/reviews/*.receipt.yaml`: **0/24** — ĐÚNG như Fable khai.
- `seam` trong `ops/leases/*.yaml`: **0/41** — ĐÚNG.
- `seam` xuất hiện trong **5 tệp `.py`** (tên biến/khái niệm nội bộ), KHÔNG phải trường dữ liệu.
⇒ Vị từ "cùng seam" KHÔNG máy-đọc-được ở bất kỳ biên nhận/lease nào. Cạnh (2) của tôi là CỔNG GIẢ. Fable đúng.

## 2. Kiểm lại đề xuất lint `$?`-sau-pipeline
- Dòng có pipeline kết bằng lệnh lọc, phạm vi `scripts/ ops/ .claude/`: **47**
- Chỗ ĐỌC `$?` ngay sau một pipeline: **0**
⇒ Lint này là **RATCHET-TẠI-KHÔNG**: thêm vào là xanh ngay, không phải sửa gì, và nó KHOÁ trạng thái sạch
hiện tại. Chi phí gần bằng 0. (Fable khai "chưa quét được" ở mục KHÔNG ĐO ĐƯỢC — nay đã đo.)

## 3. Kiểm lại `_kiem_neo_prompt` (cơ sở cho cạnh neo tài liệu)
- `ops/lease_publish.py:153` — hàm CÓ THẬT, đã gọi ở dòng 298. Họ mã `RC_NEO=6` có sẵn.
- `prompt_path` + `prompt_sha256_required`: **82/82** khối lease — kỷ luật neo prompt đã PHỔ QUÁT.
⇒ Mở rộng sang tài liệu kế hoạch/spec là ĐI TIẾP một cơ chế đã chạy, không phải dựng cơ chế mới.

## 4. PHÉP ĐO QUYẾT ĐỊNH — cả đề bài lẫn Fable đều KHÔNG chạy
Câu hỏi: lease trích tài liệu ngoài `prompt_path` có resolve được từ `origin/master` không?

| đo ở đâu | kết quả |
|---|---|
| 41 lease, 18 lease có trích dẫn ngoài `prompt_path` | trích dẫn KHÔNG resolve từ `origin/master`: **0** |

Nhìn qua tưởng "không có bệnh". SAI — vì phép đo trên đo **TRẠNG THÁI CUỐI**, sau khi lịch sử đuổi kịp.
Đo lại tại **THỜI ĐIỂM CẤP LEASE**:

| vật | lên master lúc | lease trích nó cấp lúc | lệch |
|---|---|---|---|
| `ops/specs/plat-m4-v0.md` | `d27337b` **03:58:21Z** | `plat-m4-exec-2-claude` **02:05Z** | **−1h53m** |
| `ops/specs/plat-m4-v0.md` | (nt) | `plat-m4-review-2-codex` **02:30Z** | **−1h28m** |

⇒ Cổng neo-tài-liệu-vào-ref-bền sẽ **ĐỎ ĐÚNG HAI LẦN NÓ CẦN ĐỎ**, và xanh bây giờ chỉ vì lịch sử đã đuổi kịp.
Đây chính là ca đã LÀM HỎNG một lượt review thật (prompt trỏ `kho/ops/specs/plat-m4-v0.md`, cây reviewer
đứng ở packet head — tệp không có ở đó). Bài học ấy hiện chỉ là VĂN XUÔI; đây là đường biến nó thành phép kiểm.

**Hệ quả cho thiết kế:** cổng phải chạy ở **ĐIỂM CHUYỂN TRẠNG THÁI** (lúc cấp/đăng lease), KHÔNG phải hậu kiểm
trên cây hiện tại. Hậu kiểm cho ra 0/0 và kết luận "không có bệnh" — đúng lỗi "hỏi chỗ tiện tay thay vì hỏi
chỗ kết luận được ghi" mà kho đã trả giá ba lần trong một phiên.

## 5. Khai thẳng — nợ quy trình của chính lượt này
Lượt codex vòng 1 chạy `-s read-only` nên codex KHÔNG ghi được tệp báo cáo ra ngoài `./kho`; nó phải in
nguyên văn vào câu trả lời. Đây là **lần thứ tư trong ba ngày** một lượt review bị hỏng vì cách PHIÊN CHÍNH
dựng sandbox/bundle, không phải vì reviewer. Ba lần trước: prompt trỏ tệp không có trong cây · bundle thiếu
lease X4 · `| tail` nuốt rc. **Cùng một hình dạng, lần thứ tư** — theo đúng luật của kho ("đếm HÌNH DẠNG lỗi,
đừng chỉ đếm lỗi"), ngưỡng 3 đã vượt: câu hỏi đúng không còn là "vá thế nào" mà là **"có nên dựng sandbox
bằng tay nữa không"** ⇒ việc E (script dựng sandbox reviewer) của kế hoạch A–F KHÔNG còn là việc tuỳ chọn.
