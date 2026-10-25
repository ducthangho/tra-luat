# WP748 r25/g25 — `launcher.py run` ghi model do máy chủ trả cho từng response của lượt codex (spec v2)

## Thay thế

Tệp này **thay toàn bộ** spec v1 `ops/specs/wp748-r25-launcher-model-phuc-vu.md`
(sha256 `5f85d350bc78a28693b1cb095bfa2fa62353975c3ba0e714a2a59c6e8e4dafa3`, commit `1c879c0`). v1 giữ nguyên làm hồ
sơ, không còn là nguồn thi hành. Lý do: hai vòng cross-review Codex qua `launcher.py run` (l909c trên `83d305f`, l909d
trên `aaad9ab`) chỉ ra hợp đồng §2 của v1 tự mâu thuẫn — vừa đòi trace không chạm đĩa, vừa hứa *"dòng không phải trace
vẫn vào `stderr.log` như cũ"*, mà không có cách phân biệt hai loại dòng ấy mà không đoán (R25-SEC-01, R25-CONTRACT-07).

tran_loi_goi_codex: ADR-0052@8ab100793df9831505f495543a74044b91c2c9ab
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

v1 **thiếu** hai dòng trên, nên theo luật fail-closed của `ADR-0052`/`ADR-0053` packet chịu trần cũ (2 lời gọi Codex;
3 tệp / 300 dòng thêm) và đã vượt cả hai trước khi v2 được soạn. Ghi thẳng: lỗi của executor khi soạn v1.

## Thẩm quyền và nguồn gốc

Gốc: https://github.com/ducthangho/tra-luat/issues/748#issuecomment-6378484722 (OWNER, 2026-10-24T01:59:43Z).
Điều chỉnh v2: chủ kho chọn trong phiên Claude Code 24-10-2026 phương án *"Chỉ giữ dòng trong danh sách cho phép"* và
*"Nâng trần riêng r25 lên 550"*; 25-10-2026 *"Tôi duyệt trần 10"*. Lease mới chỉ có hiệu lực khi chủ kho đăng comment
cấp quyền trên #748 neo `spec_hash` của tệp này.
Executor: Claude Code (`anthropic_claude`, `claude_code`, remote Linux). Reviewer: Codex độc lập chỉ đọc qua
`launcher.py run`, neo đúng head cuối. Review Class `sensitive`. PR #909.

## Write set hiệu lực (không đổi)

1. `.claude/dev/launcher.py`
2. `.claude/dev/launcher_test.py`

## Hợp đồng

1. **Nguồn duy nhất:** trường `model` của đối tượng `response` trong sự kiện `response.created` hoặc
   `response.completed` do máy chủ gửi, đọc từ dòng log TRỌN VẸN khớp đúng `TRACE tungstenite::protocol: Received
   message {…}` (UTF-8 chặt; `id` và `model` là chuỗi khác rỗng sau khi bỏ khoảng trắng). Không suy từ `-m`,
   `turn_context`, header CLI hay tên chương trình.
2. **Không chạm đĩa — danh sách cho phép NGUYÊN VĂN:** với lượt codex, `stderr.log` chỉ nhận dòng trọn vẹn (đầu dòng,
   kết thúc bằng xuống dòng) bằng nguyên văn một mục của hằng `_STDERR_CHO_PHEP` trong mã (hiện chỉ
   `Reading additional input from stdin...`). Mọi byte khác bị bỏ; `run.json` chỉ ghi số đếm `stderr_bo_dong`,
   `stderr_bo_byte`. Không có tệp tạm nào nhận dòng trace. Thay câu *"dòng không phải trace vẫn vào stderr.log như
   cũ"* của v1: chẩn đoán stderr của lượt codex bị mất là đánh đổi chủ kho đã chấp nhận. `RUST_LOG` của con bị
   GHI ĐÈ bằng đúng target `tungstenite::protocol=trace` (không nối với giá trị thừa kế); có ghi đè thì ghi sổ.
3. **Sổ:** `run.json` thêm `model_phuc_vu` = danh sách `{response_id, model, su_kien}` theo thứ tự đến (khử trùng
   theo `response_id` + `model`) và `model_phuc_vu_trang_thai` ∈ {`DO_DUOC`, `KHONG_DO_DUOC`}. `DO_DUOC` chỉ khi đủ
   bốn điều kiện: có ít nhất một khung nhận được · bộ lọc không hỏng · luồng đọc stderr đã tới EOF trong hạn chờ ·
   không có đoạn nào trông như khung `response.created`/`completed` mà không nhận được (vượt trần đọc, cụt ở EOF,
   giữa đoạn đọc, UTF-8 hỏng, id/model rỗng). Thiếu một điều ⇒ `KHONG_DO_DUOC` kèm lý do, vẫn ghi danh sách đã nhận.
   Trạng thái và các trường sổ suy từ MỘT ảnh chụp lấy sau khi chốt trạng thái luồng đọc. Lệnh không phải codex ⇒
   không có khoá `model_phuc_vu*`/`stderr_bo*`, hành vi cũ giữ nguyên.
4. **Không đo ngược:** không sửa biên nhận/hồ sơ cũ.
5. **Không yếu hơn hiện tại:** mọi chốt cũ của `lenh_run` (giết cây khi quá hạn, mã 124/125, Job Object Windows, ghi
   sổ `stdout_byte`/`stderr_byte`/sha256, neo prompt) giữ nguyên; đọc ống stderr có trần độ dài mỗi lần đọc (cả đường
   xả khi lỗi) và không làm treo lượt chạy khi con hoặc cháu còn giữ ống (chờ có hạn 10 giây).

## Trần

nang_tran:
  - truc: kich_thuoc
    ai_nang: chủ kho ducthangho (lựa chọn "Nâng trần riêng r25 lên 550", phiên 24-10-2026; neo bằng comment cấp quyền trên #748)
    can_cu: "numstat so base master e739ac1 tại b5b6aef: .claude/dev/launcher.py +136/-3, .claude/dev/launcher_test.py +362/-0 (2 tệp, +498). Tách packet thì chốt và ca test/đột biến của chính chốt ấy nằm ở hai PR, mỗi PR không tự chứng minh được."
    tran_cu: "ADR-0053: ≤ 6 tệp / ≤ 450 dòng thêm"
    tran_moi: "≤ 2 tệp / ≤ 550 dòng thêm"
  - truc: loi_goi_codex
    ai_nang: chủ kho ducthangho ("Tôi duyệt trần 10", phiên 25-10-2026; neo bằng comment cấp quyền trên #748)
    can_cu: "đã dùng 5 trên PR #909: l909a (fea07f1) và l909b (56263ec) bị dừng sau khi có output, l909c (83d305f) và l909d (aaad9ab) chạy trọn, connector Codex khi PR được đánh dấu ready (b5b6aef, 0 finding). ADR-0055 (#919) nâng trần chung lên mười nhưng chưa land, nên r25 không trích được OID của nó."
    tran_cu: "ADR-0052: 8"
    tran_moi: "10"

## Chấp nhận

- Ca test dùng con GIẢ (không mạng, không credential thật) in khung trace giả có chuỗi bí mật mẫu: `run.json`,
  `stdout.log`, `stderr.log` và thư mục lượt chạy KHÔNG chứa chuỗi ấy; `model_phuc_vu` đúng từng response; ca không có
  khung, ca mất khung, ca bộ lọc hỏng, ca ống còn mở ⇒ `KHONG_DO_DUOC`; ca hai model ⇒ ghi cả hai; quá hạn vẫn 124/125.
- Mỗi chốt mới có đột biến riêng làm ca đích ĐỎ, giết bởi `TinHieuChotCa` của đúng ca đích.
- `launcher_test.py` N/N trên Linux; lane Windows (`launcher-windows.yml`) xanh.
- Một lượt `launcher.py run` thật với codex cho `DO_DUOC`, `stderr.log` chỉ chứa dòng cho phép, quét bí mật sạch.
- Trong trần đã nâng ở trên; vượt ⇒ dừng, hỏi chủ kho.
- Codex review qua `launcher.py run` trên head cuối: 0 P0/P1/P2; chủ kho duyệt trên SHA cụ thể trước merge.

## Dừng

Dừng và báo khi: người giữ chồng lấn; cần ghi ngoài write set; codex đổi định dạng khiến nguồn đo biến mất hoặc dòng
không phải trace mới xuất hiện cần cho chẩn đoán (đổi danh sách cho phép = revision mới); hết trần lời gọi; hoặc thiếu
bằng chứng dương.
