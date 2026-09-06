# VERDICT — cross-review LƯỢT 1, PR #452 (`ops/PHAN_BIEN_QUY_TRINH_BUILD_REVIEW_20260905.md`)

- **reviewed_sha:** `07eb236f9a4831d70c469165d31305830d572370`
- **verdict:** `changes_requested` · **assurance:** `same_provider_approved` (KHÔNG phải `cross_approved`)
- **Reviewer:** hai phiên Claude độc lập, vai read-only, chạy song song, không thấy nhau.
- **XUẤT XỨ — nói trước:** reviewer chạy như subagent TRONG phiên, KHÔNG qua `launcher.py run`.
  Không có `run.json`, không `prompt_sha256`, không `thoi_luong_giay`. Bản đầy đủ sống trong transcript
  subagent, NGOÀI kho. Tệp này là bản ghi do phiên điều phối soạn từ kết quả nhận được; mỗi finding
  dưới đây **đã được phiên điều phối ĐO LẠI ĐỘC LẬP** bằng lệnh ghi kèm. Cái ĐO LẠI được là bằng chứng;
  câu chữ của reviewer thì **KHÔNG ĐO ĐƯỢC**.

## Hướng A — đo lại mọi con số

| # | Bản 1 khai | Đo lại | Lệnh |
|---|---|---|---|
| A1 | `spec_hash` **14/82 = 17,1%** | **10/82** — `grep -l` đếm cả tệp chỉ NHẮC tên; **3** tệp thừa nói nguyên văn *"KHÔNG khai `spec_hash` làm mỏ neo"* ⇒ đếm tệp TỪ CHỐI khai thành ĐÃ khai | `grep -lE '^ *spec_hash: *[0-9a-f]{64}' ops/leases/*.yaml` |
| A2 | mốc CLAUDE.md `2/74 = 3%` | dùng **phương pháp chặt** ⇒ bản 1 so **lỏng với chặt** | tái lập tại `9e6d50d` |
| A3 | `review_rounds_used` 10/57 · `codex_review_calls_used` 2/57 · `thoi_luong_giay` n=9 | **4** · **0** · **1** là trường schema; phần còn lại là văn xuôi | `grep -lE '^ *<tên>: *[^ ]'` |
| A4 | "6 biến thể lẻ" | `blocked` là **giá trị CANON** ⇒ ngoài canon = **5**; **52/57 = 91,2%** đã đúng canon | `grep -h '^verdict:' \| sort \| uniq -c` |
| A5 | "cạn ~ngày 11" | số học của chính hai số hạng ra **~7,4** | `2000/(8100/30)` |
| A6 | lệnh tái hiện ở §0 | **KHÔNG tái hiện được** — để lại đuôi `,stdout_byte=…` nên mọi chuỗi bắt đầu bằng `=`, `sort -n` sắp tất cả về 0 | chạy đúng lệnh in trong tài liệu |
| A7 | "gắn nhãn `windows` KHÔNG sinh lượt chạy nào" | **SAI với kho**: `launcher-windows.yml` khai `types:[opened,synchronize,reopened,labeled]` + `windows-latest`. Khảo sát **1/7** workflow rồi kết luận cho 7 | `grep -l windows-latest .github/workflows/*.yml` |
| A8 | MVP-1 "đóng schema" | schema **ĐÃ TỒN TẠI**: `review_verdict.v1.schema.json`, enum đúng 3 canon, 16 `required`, `additionalProperties:false`; `launcher.py`/`packet_loop.py` tham chiếu **0 lần** | đọc tệp + `grep -c` |
| A9 | PR #250 là "phản chứng đo được" | `CLAUDE.md` + `PROTOCOL §8` cấm: *"chưa có biên nhận trong kho… KHÔNG TÁI LẬP ĐƯỢC… đừng dùng như một gate đã kiểm"* | `sed -n '393,394p' CLAUDE.md` |

**Đại lượng bị bỏ sót, reviewer tìm ra:** mẫu n=9 đến từ **3 dòng việc**, **8/9 reviewer là `claude`** (chỉ 1 codex) ⇒ gọi nó "median một lượt cross-review" là sai nhãn; corpus dừng 30-08 (cửa sổ 17 ngày); một packet (`wp55`) chiếm 32% corpus.

## Hướng B — phá lập luận

- **B1 · "9/13 đã có trong PROTOCOL" rộng hơn bảng §2 của chính tài liệu** — chỉ **5/9** neo thuần PROTOCOL; còn lại ADR-0036, skill, `CLAUDE.md`.
- **B2 · F1 tối ưu nhầm tài nguyên, và tiền đề sai** — Linux **6,6′ (13-08) → 21m52s–25m14s (29-08)**, chậm **3,4×**; một lượt ubuntu-only hôm nay đắt hơn cả lượt HAI NỀN đã làm cạn hạn mức. `ci.yml:63`: *"NÂNG TRẦN KHÔNG CHỮA NGUYÊN NHÂN"*.
- **B3 · "trần 2 lượt/PR, cứng" sai** — ADR-0043 nới được bằng `nang_tran`; `grep -c nang_tran ops/lease_publish.py` = **0**; §20 ghi `ADR-0043 | 0 cổng`.
- **B4 · "số vòng review KHÔNG ĐO ĐƯỢC" sai** — `cmd_bien_nhan` đếm theo lớp tương đương `reviewed_sha`, không theo `luot`. Lỗ THẬT lớn hơn: packet **#249 chạy BỐN vòng, để lại 0 biên nhận**, suite vẫn 98/98 xanh.
- **B5 · `packet_id` sai hệ thống** — **18** biên nhận khai `packet_id: wp55` nhưng `lease_id` trải **≥5** dòng việc ⇒ "15 packet riêng biệt" không phải 15 packet.
- **B6 · F3 đổi nghĩa một giá trị CANON** — `blocked` nghĩa *spec thiếu*, `CHUYEN_HOP_LE["blocked"] = ()` là **trạng thái tận cùng**. Luật "không đo được ⇒ `blocked`" biến một sự cố vận hành thành revision packet.
- **B7 · MVP-3 không an toàn** — **0/3** lượt Windows dispatch từng hoàn tất; ≥112 phút tính tiền/lượt; `concurrency.group` của dispatch khác của PR ⇒ **không** bị `cancel-in-progress`; và người quyết định "packet đụng nền" là executor — tái tạo đúng M5.
- **B8 · Việc thứ tư bị bỏ** — PROTOCOL §8 **đã là luật** về cấp năng lực đo cho reviewer (mirror + `core.abbrev=7`); tài liệu trình bày nó như phát hiện riêng rồi không đưa vào MVP.

## Yêu cầu

Sửa §0 theo phép đo; đảo hoặc rút kết luận trung tâm; viết lại MVP-1/2/3; thêm MVP-4; rút PR #250 khỏi vai bằng chứng.
