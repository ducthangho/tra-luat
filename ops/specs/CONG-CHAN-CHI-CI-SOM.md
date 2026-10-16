# Đặc tả packet — CONG-CHAN-CHI-CI-SOM (revision 1)

- `packet_id`: **CONG-CHAN-CHI-CI-SOM**; ID bền `wp<packet_issue>`.
- `packet_issue`: **(để trống — chủ kho cấp)**
- `mission_issue`: **(để trống — chủ kho cấp)**
- `revision`: **1** · `generation`: 1 · soạn **11:5xZ 11-09-2026**
- `depends_on`: **`[]`**
- `executor`: claude · `environment`: cloud
- `risk`: **sensitive** · `review_class`: **sensitive** (hook là **thẩm quyền chặn công cụ** của agent)

## `nguon_cap_viec`

Chỉ thị chủ kho **11-09-2026**: *"Không chạy CI, full CI cho tới khi đủ điều kiện merge"*.

**Đo được — hôm nay KHÔNG gì chặn được việc ấy:**

| nơi | phép đo | kết quả |
|---|---|---|
| `.claude/settings.json` | khoá `hooks.PreToolUse[0].matcher` | **`"Bash"`** — chỉ khớp Bash |
| `.claude/hooks/pretooluse_guard.py` | dòng `947` | `if data.get("tool_name") != "Bash":` ⇒ **return sớm** |
| `.claude/skills/*/SKILL.md` (6 tệp) | `grep -i 'workflow_dispatch\|chạy CI\|full CI\|actions_run_trigger'` | **0** quy định |
| `docs/PROTOCOL_DA_PHIEN.md` | cùng mẫu | **0** quy định (3 hit `workflow_dispatch` đều mô tả) |
| `.claude/dev/packet_loop.py` | `void-attempt --reason quota` | xử lý **SAU** khi đã cạn, không chặn chi |

⇒ Mọi lời gọi MCP — kể cả `mcp__github__actions_run_trigger` — **đi qua không ai nhìn**.

**Giá đã trả, đo 11:0xZ 11-09-2026:** 8 lượt `gate (windows-latest)` `cancelled` trên `push`/`master`
đốt **723,96 phút TÍNH TIỀN** (hệ số Windows ×2) = **36,2 %** hạn mức Free `2.000` phút/tháng, và thu
được **0 thông tin** (bước `lease-publish selftest` bị cắt, không bước nào sau nó chạy).
Tiền lệ nặng hơn: `ci.yml:19-24` ghi kho **đã cạn quota thật** 12-08-2026, CI đứng hình.

**Vì sao packet này tồn tại RIÊNG khỏi packet doctrine:** `ADR-0043`/`ADR-0037` là hai luật đúng,
được chủ kho duyệt, và `§20` ghi cả hai **`0 cổng`**. Một luật không có cổng là một luật không tồn tại
đúng lúc nó cần nhất. Nếu chỉ làm được một packet trong hai, **làm packet này**.

## `review_class` và ngưỡng

`sensitive` ⇒ `ADR-0044`: **≤ 3 tệp, ≤ 300 dòng thêm**. Packet này **đúng 3 tệp** — **không còn chỗ
trống**. Đường thứ tư ⇒ **DỪNG và hỏi chủ kho**.

## `write_set`

| # | đường dẫn | vì sao |
|---|---|---|
| 1 | `.claude/settings.json` | `matcher` phải phủ lời gọi MCP, không chỉ `Bash` |
| 2 | `.claude/hooks/pretooluse_guard.py` | nhánh phân loại + quyết định chặn |
| 3 | `.claude/hooks/pretooluse_guard_test.py` | phản chứng cho từng nhánh |

Không ký tự đại diện. **KHÔNG** đụng `.claude/dev/packet_loop.py` (nợ `SO-CANON-CHUA-TON-TAI`),
**KHÔNG** đụng `.claude/skills/**` (packet doctrine riêng), **KHÔNG** đụng `.github/workflows/**`.

## `ngoai_pham_vi`

1. **KHÔNG viết cổng `so-canon`** cho trần vòng review — nợ riêng.
2. **KHÔNG chặn lượt CI do GitHub tự bắn** (`pull_request`, `push`). Đó là **cổng**, không phải chi
   tiêu tuỳ ý; chặn nó là tháo cổng.
3. **KHÔNG đổi `concurrency` hay ma trận của `ci.yml`** — thuộc `#463`/`T125`.
4. **KHÔNG tự quyết "đủ điều kiện merge" bằng cách đọc trạng thái PR từ hook.** Hook chạy cục bộ,
   không có mạng bảo đảm; một chốt phụ thuộc mạng sẽ **fail-open khi mạng hỏng** — đúng thứ phải tránh.
   Cơ chế là **khai báo tường minh** (xem `M2`), không phải suy đoán.

## `muc_tieu`

| # | mục tiêu | chiếu vào |
|---|---|---|
| M1 | Hook **NHÌN THẤY** lời gọi MCP: `matcher` phủ `mcp__github__actions_run_trigger`, và thân hook không còn `return` sớm cho mọi `tool_name != "Bash"`. | #1, #2 |
| M2 | **Ba loại chi, chỉ loại thứ ba bị chặn.** (a) CI **gác cổng** do GitHub tự bắn — hook không thấy, không đụng. (b) CI **làm nhạc cụ đo** — cho phép khi phiên khai tường minh một **ngân sách `N`** đã đóng băng trong spec packet, kèm `run_id` ghi biên nhận. (c) CI **thăm dò** — **CHẶN**. | #2 |
| M3 | **FAIL-CLOSE.** Không đọc được khai báo ngân sách, hoặc khai báo không phân tích được ⇒ **CHẶN**, không phải cho qua. | #2 |
| M4 | Hook **KHÔNG** mở rộng thẩm quyền sang công cụ khác: mọi `tool_name` ngoài tập được khai vẫn đi qua y như trước. Nới `matcher` không được biến hook thành cổng chặn mọi thứ. | #1, #2 |
| M5 | Mỗi nhánh quyết định có **phản chứng riêng**. | #3 |

## `nghiem_thu`

**A1 (M1) — hook THẬT SỰ nhìn thấy lời gọi MCP.**
Ca `rXX_hook_nhin_thay_actions_run_trigger`: bơm payload `{"tool_name": "mcp__github__actions_run_trigger", …}`
vào hook. Đòi: hook **xử lý** nó (đi tới nhánh quyết định), không `return` sớm.
**Phép làm ĐỎ:** khôi phục `if data.get("tool_name") != "Bash": return` ⇒ ca ĐỎ.
**Kèm phép đo cấu hình, KHÔNG thay thế được ca trên:** `json.load('.claude/settings.json')` ⇒
`hooks.PreToolUse` phải có mục khớp tên công cụ MCP. **Hai phép đo riêng vì chúng mù đúng chỗ nhau**:
`matcher` đúng mà thân hook `return` sớm ⇒ vẫn mù; thân hook đúng mà `matcher` không khớp ⇒ hook
**không được gọi lần nào**. Kho đã trả giá cho đúng kiểu *"cổng vắng mặt trông giống cổng xanh"*.

**A2 (M2) — ba loại chi phân biệt được, mỗi loại một ca.**
- (a) lời gọi **không phải** dispatch CI (ví dụ `mcp__github__issue_read`) ⇒ **cho qua**;
- (b) dispatch CI **có** khai báo ngân sách hợp lệ, chưa cạn ⇒ **cho qua**, và bộ đếm tăng **1**;
- (c) dispatch CI **không** khai báo ngân sách ⇒ **CHẶN**.
**Phép làm ĐỎ:** gộp (b) và (c) (cho qua mọi dispatch) ⇒ ca (c) ĐỎ · chặn cả (a) ⇒ ca (a) ĐỎ.
Đòi đọc **nhật ký quyết định** của hook, không chỉ đọc mã thoát — nếp đã trả giá ở `ops-don-ref`
(`40/40` trong khi một đột biến xoá hẳn lệnh phá vẫn qua).

**A3 (M2) — ngân sách CẠN thì chặn, và bộ đếm đếm ĐÚNG.**
Ca `rXX_ngan_sach_can_thi_chan`: khai `N = 2`; lời gọi thứ **1** và **2** cho qua, lời gọi thứ **3**
**CHẶN**. Đòi **số lần cho qua = 2**, đọc từ nhật ký.
**Phép làm ĐỎ:** bỏ phép so với `N` ⇒ lời gọi thứ 3 lọt ⇒ ĐỎ · đếm sai chiều (off-by-one) ⇒ ĐỎ.

**A4 (M3) — FAIL-CLOSE, ba biên.**
Thiếu tệp khai báo · tệp có mà không parse được · parse được mà thiếu trường `N`.
Cả ba ⇒ **CHẶN**. **Phép làm ĐỎ:** biến bất kỳ biên nào thành "cho qua" ⇒ ca ĐỎ.
Một cổng tự tắt khi thiếu đầu vào là **cổng không tồn tại đúng lúc nó cần nhất**.

**A5 (M4) — KHÔNG mở rộng thẩm quyền.**
Ca `rXX_khong_chan_cong_cu_ngoai_tap`: bơm **≥ 5** `tool_name` khác nhau ngoài tập được khai
(gồm `Bash` với một lệnh vô hại, và ít nhất hai tên MCP khác) ⇒ **tất cả cho qua**, và hành vi của
nhánh `Bash` sẵn có **không đổi**.
**Phép làm ĐỎ:** chặn theo *"tên có chứa `actions`"* ⇒ một tên vô can bị chặn ⇒ ca ĐỎ.
**Vì sao ca này bắt buộc:** nới `matcher` là mở cho hook thấy nhiều hơn; nếu nhánh quyết định viết
rộng, nó chặn oan việc hợp lệ. Kho đã đo được cả hai chiều hỏng — bộ quét tự viết từng **chặn nhầm**
6 tệp doctrine (báo 14 lease, thật là 0).

**A6 (M4) — hồi quy của nhánh `Bash` bằng 0.**
`python3 .claude/hooks/pretooluse_guard_test.py` ⇒ **N/N** với hai số **BẰNG NHAU**, và `N` **không
nhỏ hơn** số ca trước packet. Không tin `rc=0` suông.
**Phép làm ĐỎ:** bất kỳ ca `Bash` sẵn có nào tụt.

**A7 (M5) — mỗi nhánh có đột biến riêng.**
Đếm bằng `(tên ca, tên đột biến, đã chạy, ĐỎ)`; nhánh nào không có đột biến riêng thì **không tính**.
Đòi **≥ 6** ca mới, mỗi ca **đúng một** đột biến làm nó ĐỎ. Ca không đổi màu theo đột biến chỉ định
**không** được đếm.

**A8 (toàn packet) — `ADR-0044`.** `git diff --numstat` ⇒ đúng **3** đường dẫn, `additions` ≤ `300`.
**3 tệp là ĐÚNG TRẦN, không dư chỗ nào** ⇒ đường thứ tư ⇒ **DỪNG và hỏi chủ kho**.

**A9 — danh sách CHO PHÉP, không phải danh sách CẤM.**
Tập công cụ bị chặn phải là một **danh sách liệt kê tường minh** trong mã, không phải một mẫu chuỗi.
**Phép làm ĐỎ:** đột biến **nới** danh sách để chứa một tên vô can ⇒ ca `A5` phải ĐỎ; đột biến đổi
danh sách thành `if 'actions' in ten` ⇒ `A5` phải ĐỎ.
Căn cứ: `CLAUDE.md` — *"danh sách CẤM không bao giờ đủ, phải đảo thành danh sách CHO PHÉP"*; đo được
ở `v1.36.68` (PR #104): ba tên tấn công `rc=0` → `rc=4`.

**Điều kiện dừng:** `sensitive` ⇒ đòi cross-review **`approve`** tường minh.

## `chua_do_duoc`

1. **Hook KHÔNG chặn được mọi đường phóng CI.** Nó thấy lời gọi công cụ của **phiên này**; nó **không**
   thấy: người dùng bấm nút trên giao diện GitHub · một workflow khác gọi `workflow_dispatch` ·
   một phiên khác trên máy khác. Phạm vi phải khai đúng trong chính hook, **không** đặt tên to hơn thứ
   nó chặn — kho đã trả giá cho đúng lỗi ấy (cờ *"CODEX BI CHAN"* mà chỉ một trong nhiều cửa đọc).
2. **Không đo được "đủ điều kiện merge" từ hook.** Vì vậy `M2` dùng **khai báo ngân sách tường minh**
   thay vì suy đoán trạng thái PR. Đánh đổi: một phiên cố tình khai sai `N` vẫn qua được. Cơ chế này
   chống **chi tiêu do quán tính**, **không** chống cố ý — khai thẳng, đừng khai là đã chặn.
3. **Chưa đo được hook có thật sự được nền gọi cho lời gọi MCP hay không.** `A1` đo **hợp đồng** (payload
   vào hook thì hook xử đúng) và **cấu hình** (`matcher` khớp); nó **không** đo rằng Claude Code thật sự
   bắn `PreToolUse` cho công cụ MCP trên nền này. Phiên thi công phải **đo hành vi thật một lần** và ghi
   vào biên nhận; không đo được ⇒ khai `KHÔNG ĐO ĐƯỢC`, **không** khai là đã chặn.
   Đây là mục quan trọng nhất của packet: nếu nền không bắn hook cho MCP thì **cả packet là trang trí**,
   và điều đó phải lộ ra ở biên nhận chứ không nằm im.
