# Đặc tả packet `WINDOWS-LOCAL-MAY-CHU-KHO` r2: hạn cho khoá bỏ rơi và mở phạm vi sang mọi máy Windows của chủ kho

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544

| trường | giá trị |
|---|---|
| packet | `WINDOWS-LOCAL-MAY-CHU-KHO` (mission #748), revision 2, generation 1 |
| review_class | `sensitive` (cổng lease tính `sensitive` cho `docs/PROTOCOL_DA_PHIEN.md`, tiền lệ r1) |
| write set | `docs/adr/0058-windows-local-han-khoa-va-pham-vi-may.md` (planned), `docs/PROTOCOL_DA_PHIEN.md` |
| base | `origin/master` lúc cấp lease (đo khi soạn: `d31df1e`, merge của PR #1022) |
| executor | `anthropic_claude` (Claude Code remote, Linux) |
| reviewer | `openai_codex` qua `launcher.py run`, phiên mới, neo đúng head |
| depends_on | r1 đã land (`ADR-0057`, PR #1022) |

## 1. Vì sao
ADR-0057 có hiệu lực từ 29-10-2026. Ngay trong ngày đó đã đo được hai lỗ mà r1 không phủ.

| # | sự kiện | số đo | bài học |
|---|---|---|---|
| D7 | khoá bỏ rơi | Phiên `session_015GtxrYjGJtmjF3eT1nCSG9` ghi khoá `D:\tl-win\KHOA.txt` lúc 09:24:55Z. Laptop mất kết nối khoảng 10:00Z, offline tới ~11:37Z. Khoá nằm đó khoảng 2 giờ 15 phút, trong khi máy không chạy test nào (`session_015GtxrbUPS7zGdffB8Sfo8Y` kiểm lúc ~11:40Z: chỉ có 2 tiến trình python của MCP browser-use). Phiên giữ khoá không xoá được từ xa nên tự tuyên bố khoá hết hiệu lực qua `send_message`. | ADR-0057 §3 chỉ có "xoá khi xong", không có hạn. Máy tắt khi đang giữ khoá thì khoá bị kẹt mãi, và mọi phiên khác phải ĐỢI theo §3 |
| D8 | máy thứ hai | VM GCE `tra-luat-win` ở trạng thái RUNNING (đo bằng `gcloud` trên laptop, ~11:40Z) nhưng không có trong `list_devices` của Desktop Commander (chỉ có ASUS-LAPTOP). `gcloud` trong container cloud không có credential. | ADR-0057 §1 chỉ nêu ASUS-LAPTOP. Máy Windows thứ hai của chủ kho chưa có luật, và quy ước khoá một-tệp không nói khoá thuộc máy nào |
| D9 | chu trình đủ đầu tiên | `t27`: master `9666771` cho 0/1 ĐỎ, #1007 head `10446ff` cho 2/2 QUA, đo local trên ASUS-LAPTOP lúc 11:39:56Z–11:40:20Z. #1022 head `f4d15ed`: 3/3 ĐẠT local. | quy trình chạy được trọn vòng; lỗ ở D7 và D8 là lỗ thật, không phải giả định |

## 2. Thay đổi
1. **Thêm ADR-0058** tại `docs/adr/0058-windows-local-han-khoa-va-pham-vi-may.md`, trạng thái `Accepted` khi chủ kho duyệt spec_hash. ADR này **sửa đúng hai điểm** của ADR-0057 (§1 Phạm vi và §3 Khoá), giữ nguyên mọi điểm khác theo tiền lệ ADR-0056 với ADR-0017. Không sửa tệp ADR-0057.
   - **Phạm vi (thay §1 của ADR-0057):** là mọi máy Windows của chủ kho đang có mặt trong `list_devices` của Desktop Commander với trạng thái `Online`. Hiện có ASUS-LAPTOP; VM `tra-luat-win` chỉ thuộc phạm vi khi nó xuất hiện trong `list_devices`. Máy không có trong `list_devices` thì không dùng, và không tìm đường khác (ví dụ `gcloud`, RDP) để vào máy đó.
   - **Khoá theo máy:** mỗi máy có khoá và sổ đo riêng ở thư mục gốc `tl-win` của chính máy đó. Thư mục gốc là `D:\tl-win\`, hoặc `C:\tl-win\` nếu máy không có ổ `D:`. Mọi đường dẫn `D:\tl-win\…` trong ADR-0057 được đọc theo nghĩa này. Kết quả đo ghi thêm tên máy (cột `ghi_chu`, dạng `may=<tên trong list_devices>`).
   - **Hạn khoá (bổ sung cho §3 của ADR-0057):**
     - Dòng khoá có thêm một trường hạn: `<session_id>\t<UTC bắt đầu>\t<UTC hạn>\t<việc>`. Hạn không quá **2 giờ** sau lúc bắt đầu.
     - Hết hạn mà phiên giữ khoá vẫn cần máy thì phải ghi lại dòng với hạn mới (gia hạn).
     - Khoá được coi là **hết hiệu lực** khi (a) quá hạn ghi trong dòng, hoặc (b) dòng theo dạng cũ của ADR-0057 (không có trường hạn) đã quá 2 giờ kể từ UTC bắt đầu, hoặc (c) phiên giữ khoá đã tuyên bố bỏ khoá. Trường hợp (c) phải có bằng chứng: tin nhắn của chính phiên đó hoặc comment trên PR của nó.
     - Phiên tiếp nhận khoá hết hiệu lực làm theo thứ tự: chạy bước kiểm tải (§4 của ADR-0057); ghi một dòng vào sổ đo với `ghi_chu` nêu khoá cũ (session, UTC) và lý do (a)/(b)/(c); thay nội dung khoá bằng dòng của mình. Dù có tiếp nhận khoá, vẫn không được dừng tiến trình của phiên khác.
   - **Số đo D7–D9** của §1, kèm mục "không cổng nào cưỡng chế" (vẫn 0 cổng, như ADR-0057).
2. **`docs/PROTOCOL_DA_PHIEN.md`:**
   - thêm đúng một dòng ADR-0058 vào bảng §20, cột cổng ghi `không cổng — kỷ luật executor`;
   - sửa ô mô tả của dòng ADR-0057 trong §20 để nêu "phạm vi và khoá sửa bởi ADR-0058". Chỉ sửa ô ấy;
   - câu con trỏ ở §10.2 đổi thành nhắc cả `ADR-0057` lẫn `ADR-0058`, vẫn dạng câu trung tính (finding P1 lượt 1 của r1: con trỏ không được tạo thêm nghĩa vụ).

   Không chép doctrine vào protocol.

## 3. Tiêu chí xong
- `python .claude/dev/packet_loop.py adr-song --root .` cho rc=0.
- `doctrine-scan` cho rc=0. `python scripts/tl.py doc-claims-check --json` cho `ok`.
- Diff chạm đúng 2 tệp của write set, không chạm `docs/adr/0057-*`.
- Review chéo Codex qua `launcher.py run` trên đúng head, tới khi 0 P0–P3.
- Điều kiện merge của ADR-0057 áp dụng: nếu chạy local thì phải theo chính luật khoá mới, và ghi sổ đo.

## 4. Trần
- Kích thước: ≤ 2 tệp / ≤ 120 dòng thêm.
- Lời gọi Codex: 10 theo dòng khai ADR-0055.

## 5. Ngoài phạm vi
- Không viết công cụ khoá nguyên tử hay bộ đọc sổ đo. Khoá vẫn là tệp văn bản không nguyên tử, như ADR-0057 đã khai.
- Không cấp credential `gcloud` cho container, và không cài Desktop Commander lên VM. Hai việc ấy là của chủ kho.
- Không sửa CI và không đổi check bắt buộc.
