# Review Codex offline lượt 1 — packet #1265 THU-HOI-ADMISSION-MERGE-BASE-A r13 g2 (Review Class: sensitive)

Bạn là reviewer ĐỘC LẬP (họ OpenAI). Executor là một phiên Claude khác. Lượt này CHỈ ĐỌC trên thư mục làm việc.

**Không ghi bất kỳ tệp nào trong thư mục làm việc.** Lệnh cấm gồm tệp ignored, `__pycache__`, `.git/**` và `git config`. Lượt chạy bằng `launcher.py run --chup-workspace`; chỉ cần một lần ghi vào cây là cả lượt vô hiệu. Gốc workspace có sẵn hai thư mục rỗng `.aws/` và `.codex/`; đừng xoá chúng.

**Bước đầu tiên:** chạy `git clone --no-hardlinks <thư mục làm việc> /tmp/rv1265-copy`, rồi chạy `git config core.abbrev 7` trong bản sao. Mọi lệnh chạy TRONG bản sao, và `TMPDIR` đặt ngoài cả hai cây.

## Neo
- HEAD phải là `017fc8527c3a69b672e7b1a8b661735bb9cd3de8`, tree `380b0250e6b7cf58f70aef9b0d0d9d0c1d53e68c`, cha DUY NHẤT là base `426d1b06e292a7db272a0f942bef0794479b58a6` (master, merge PR #1317). Khác ⇒ `request_changes`.
- Đặc tả nằm trong cây: `ops/specs/THU-HOI-ADMISSION-MERGE-BASE-A-r13.md`, sha256 phải là `10fe7e052b3e0f4c0acc79e844b6d746466e6b3c98fa030222a08df80203d855`. Tự đo; lệch thì DỪNG và `request_changes`.
- Write set của lease `wp1265-r13-g2-claude` gồm ĐÚNG HAI tệp:
  - `docs/adr/0066-admission-thu-hoi-theo-merge-base.md` (tệp mới);
  - `docs/PROTOCOL_DA_PHIEN.md` (chỉ được thêm MỘT dòng bảng §20, ngay sau dòng `ADR-0065`).
- Base đã mới hơn base lúc soạn đặc tả. Packet GIAM-HOI-P2 vừa land ở base, thêm dòng `ADR-0067` vào §20, nên dòng ADR-0066 phải nằm GIỮA ADR-0065 và ADR-0067.
- Bundle chưa push. Chưa có CI hay PR, nên A10 (CI) ngoài phạm vi lượt này.

## Việc
1. Đọc toàn bộ đặc tả, nhất là bảng nghiệm thu (mục "## 4. nghiem_thu": A1–A10, kèm đột biến và cột "hình dạng"), mục tiêu 1–2 và mục *Cưỡng chế*.
2. Đọc diff `426d1b0..017fc85`.
3. **Tự đo lại** từng tiêu chí A1–A9 bằng lệnh của bạn, trong bản sao. Đừng tin số của executor. Với mỗi tiêu chí:
   - chạy ít nhất một đột biến mà đặc tả nêu, trên bản sao tạm, và xác nhận nó làm tiêu chí ĐỎ đúng lý do;
   - khôi phục lại sau đó.
4. Đo lại các con số mà ADR ghi ở mục *Cưỡng chế*: số lần `grep -c 'ADR-0066'` và số dòng tệp ở sáu vị trí cổng tại base `426d1b0`. Đối chiếu với `ops/lease_publish.py` và các tệp cổng thật. Ghi mọi số lệch.
5. Executor tự khai bốn chỗ phải diễn giải. Soát từng chỗ, và nói rõ chỗ nào trái đặc tả hay trái ADR-0060 / protocol:
   - (a) mục *Cưỡng chế* viết sáu dòng dạng gạch đầu dòng thay vì bảng, để giữ dấu `|` trong lệnh;
   - (b) lý do loại ba phương án (giữ "S tổ tiên H", strict trên ruleset, merge ba chiều) là lời executor tự suy từ mục 0 và mục tiêu 1b, đặc tả không nêu;
   - (c) executor thêm ba mục đặc tả không đòi: dòng Ký hiệu, đoạn "ba trạng thái" trong Quyết định, mục Giới hạn. Chúng có làm R1–R6 khớp sai đoạn, hoặc thêm khẳng định chưa đo không;
   - (d) ADR trỏ sang "đặc tả B r13, mục tiêu 4" (`ops/specs/THU-HOI-ADMISSION-MERGE-BASE-B-r13.md`, có trong cây). Mở đặc tả B kiểm số mục ấy có đúng không.
6. Kiểm mọi khẳng định trong ADR: có đúng với mã (`ops/lease_publish.py`, workflow `ops-thu-hoi-admission.yml`) và với đặc tả không? Câu nào mạnh hơn phép đo là finding.
7. Chạy `python3 -B .claude/dev/packet_loop.py adr-song --root .` và `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .`. Ghi rc và dòng kết.

## Giới hạn
- Không gọi mạng. Không push, không đăng gì.
- Không đề xuất sửa tệp ngoài write set.
- Một phản chứng cần dựng đường dẫn thoát khỏi cây thì MÔ TẢ bằng lời, đừng tự soạn.

## Đầu ra
In ra stdout một báo cáo, có ba phần:
- Bảng A1–A9: tiêu chí · lệnh · số đo · đột biến đã chạy · kết quả.
- Danh sách finding, mỗi cái gồm: mức P0–P3, tệp:dòng, mô tả, phản chứng chạy được hoặc lý do.
- Phần trả lời cho (a)–(d).

Dòng CUỐI CÙNG của stdout phải là đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`.

Chỉ chọn `approve` khi đủ cả hai điều kiện:
- không còn finding P0, P1 hay P2;
- A1–A9 đều đạt bằng phép đo của chính bạn.
