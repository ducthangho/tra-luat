# ĐẶC TẢ ĐÓNG BĂNG — `CI-CAI-JSONSCHEMA` — **BẢN 1**

Packet **tí hon, gỡ chặn**. Sinh ra vì `gate (ubuntu-latest)` — required status check của
ruleset kho — ĐANG ĐỎ trên PR #389, và nó chặn cả #389 lẫn mọi packet nối tiếp.

**GIỚI HẠN LỜI KHAI:** chứng minh BYTE tới consumer adapter. KHÔNG tuyên bố model "đã hiểu".
**Ba trạng thái:** có · không · **KHÔNG ĐO ĐƯỢC** — trạng thái thứ ba làm cổng ĐỎ.

---

## Phép đo mở packet

Thử merge #389 qua MCP:

```
405 Repository rule violations found
Required status check "gate (ubuntu-latest)" is failing.
```

Log lượt `gate` `33190773588` (head `6edbd046`, event `pull_request`, conclusion `failure`):

```
File ".claude/dev/packet_loop.py", line 44, in <module>
  from review_verdict_binding import (
File ".claude/dev/review_verdict_binding.py", line 14, in <module>
  from jsonschema import exceptions as jsonschema_exceptions
ModuleNotFoundError: No module named 'jsonschema'
```

Gần như TOÀN BỘ `packet_loop_test` ĐỎ với `init: đòi rc=0, được rc=1` — `packet_loop.py`,
công cụ **gate lifecycle** của protocol, không import nổi.

Lịch sử `gate` trên nhánh `codex/w1-p1-van-chuyen-prompt-exec-3`:

```
b92b401a   success   <- lượt cuối còn xanh
47a50395   FAILURE   <- commit r3, chỗ `from jsonschema` vào kho
4ac8b6a9   FAILURE
6edbd046   FAILURE
```

Đo thêm: `grep` `jsonschema` trong `requirements*` / `pyproject.toml` / `.github/workflows/`
⇒ **KHÔNG Ở ĐÂU**. `ci.yml` chỉ cài `PyYAML==6.0.3`.

**VÌ SAO KHÔNG AI THẤY:** bốn vòng cross-review đều chạy trong container có sẵn
`jsonschema 4.26.0`, và bundle reviewer KHÔNG cấp đường đọc kết quả CI. Ba lần khai
"`packet_loop_test` TỔNG ĐẠT" đều đúng **ở đó** và sai **ở nơi tính điểm**. Đúng lớp bài
học *"chạy được ở đây"* trong `CLAUDE.md`.

---

## Write set — HAI đường

```
.github/workflows/ci.yml
ops/cong_cu_test.py
```

**Vì sao HAI mà không MỘT.** `T6` trong `ops/cong_cu_test.py` (d.141–156) chốt allowlist
setup bằng **tên bước → tuple lệnh CHÍNH XÁC**; dòng `pip install` hiện nằm nguyên văn ở
d.146. Đổi `ci.yml` mà không đổi `T6` ⇒ `T6` ĐỎ. Hai tệp là số nhỏ nhất đóng được, không
phải nới phạm vi.

**KHÔNG đụng** `.claude/dev/**`, **KHÔNG** `ops/lease_publish.py`, **KHÔNG** `ops/cong_cu.py`,
**KHÔNG** `ops/cong_cu.yaml`.

---

## TRÌNH TỰ — đọc kỹ, đây là chỗ dễ sai nhất

`review_verdict_binding.py` **chỉ tồn tại trên nhánh packet**, chưa có trên `master`. Đo được:
`ls .claude/dev/review_verdict_binding.py` trên `ops/cap-lease-w1-p1` ⇒ không có tệp.

Nên **hôm nay trên master KHÔNG mã nào import `jsonschema`**. Packet này cài một phụ thuộc
cho thứ **sắp** tới. Đó là CỐ Ý và đúng thứ tự: cài trước, merge #389 sau. Ngược lại thì
#389 không bao giờ qua được gate để mà merge.

Hệ quả cho A2 dưới đây: phép đo bao phủ phải **tự dẫn xuất** tập import, nên hôm nay nó
thấy `yaml` và ngày mai tự thấy `jsonschema` — không ghi cứng tên nào.

---

## Mục nghiệm thu

**A1 — CI cài `jsonschema`, ghim phiên bản.** Bước `pip install` trong job `gate` phải cài
`jsonschema` với phiên bản GHIM CHÍNH XÁC (`==`), không `>=`, không thả trôi. Ghim
`4.26.0` — đúng phiên bản mọi phép đo của W1-P1 đã chạy trên đó; CI phải chạy cùng bản
sinh ra bằng chứng.

**A2 — phép đo BAO PHỦ, không phải phép đo MỘT TÊN.** Thêm một ca vào `ops/cong_cu_test.py`
**tự dẫn xuất** tập module bên thứ ba mà `.claude/dev/*.py` và `ops/*.py` import (quét AST,
loại `sys.stdlib_module_names`, loại stem tệp nội bộ), rồi đòi MỖI tên trong tập ấy có mặt
trong lệnh `pip install` của job `gate`.

Ghi cứng `"jsonschema"` là **danh sách CẤM trá hình** — nó đóng đúng lần này và mù với phụ
thuộc kế tiếp. `CLAUDE.md` đã trả giá bốn lần cho hình dạng ấy.

**Phép đo làm A2 ĐỎ:** (a) gỡ `jsonschema` khỏi dòng `pip install` ⇒ ca ĐỎ **sau khi** #389
land; (b) **kiểm ngay hôm nay** bằng cách bơm một import giả (`import mot_goi_khong_ton_tai`)
vào một tệp tạm trong phạm vi quét ⇒ ca phải ĐỎ. Vế (b) là thứ chứng minh ca có răng **trước**
khi phụ thuộc thật xuất hiện — không có nó thì A2 hôm nay xanh mà chưa đo gì.

**A3 — `T6` cập nhật khớp, không nới.** Allowlist của `T6` phải khớp ĐÚNG dòng `pip install`
mới. Không được nới `T6` thành so lỏng (ví dụ `startswith`) — nới là gỡ chính cổng ấy.
**Phép đo làm nó ĐỎ:** thêm một bước setup lạ trước G5 ⇒ `T6` vẫn phải ĐỎ.

**A4 — gate XANH.** Sau bản vá, `gate (ubuntu-latest)` trên PR của packet này phải
`conclusion: success`. Đây là mục DUY NHẤT không đo được offline — phải đọc bằng
`actions_list` / `get_job_logs` qua endpoint MCP `/mcp/x/actions`.

**A5 — không đụng hành vi nào khác.** `ops/cong_cu_test.py` phải giữ nguyên mọi ca sẵn có;
`ops/cong_cu.py kiem-tra --json` không đổi kết quả.

---

## Nền phải ĐO LẠI trước khi bắt đầu

Trên `origin/master` sạch, clone (**KHÔNG worktree**), `git config core.abbrev 7`,
`PYTHONDONTWRITEBYTECODE=1` + `PYTHONPYCACHEPREFIX` ra ngoài cây:

```
python3 ops/cong_cu_test.py        <- đo và ghi lại con số, KHÔNG chép từ đây
python3 ops/cong_cu.py kiem-tra --json
actionlint                          <- CẦN shellcheck TRÊN PATH
```

**`actionlint` không có `shellcheck` trên PATH thì tự tắt tích hợp TRONG IM LẶNG** và trả
`rc=0 / 0 finding` — trông TỐT HƠN nền, thật ra không đo gì. W1-P1 đã vấp đúng chỗ này.

Đặc tả này CỐ Ý không chép số nền: nó được soạn trên nhánh `ops/**`, và một con số không ghi
ĐIỀU KIỆN ĐO thì sẽ trôi mà không ai biết.

---

## Điều kiện DỪNG

- **S1** cần đường dẫn thứ BA ⇒ DỪNG, khai.
- **S2** vượt **80 dòng thêm+xoá** ⇒ DỪNG. Packet này là hai dòng cấu hình cộng một ca test;
  vượt xa thế nghĩa là đã hiểu sai phạm vi.
- **S3** muốn nới `T6` thay vì cập nhật nó ⇒ DỪNG. Nới là gỡ cổng.
- **S4** muốn ghi cứng tên `jsonschema` làm phép đo bao phủ ⇒ DỪNG, xem A2.
- **S5** muốn sửa `.claude/dev/**` ⇒ DỪNG, chúng thuộc #368/#390 và đang bị lease giữ.
- **S6** chạm trần HAI vòng review (ADR-0043) ⇒ DỪNG, không tự nâng.

---

## Nợ đi kèm, KHÔNG thuộc packet này

**`bundle-reviewer-mu-voi-CI`** — bốn vòng cross-review của W1-P1 không có đường đọc kết quả
CI, nên cả một LỚP lỗi ("xanh ở đây, đỏ ở nơi tính điểm") nằm ngoài tầm với của reviewer.
Cùng họ với bài học *"reviewer không đo được thì review chỉ là soát chính tả"*. Cách chữa
thuộc `.claude/skills/cross-review/SKILL.md` và quy trình dựng bundle ⇒ packet riêng.

**KHÔNG ĐO ĐƯỢC:** parity Windows — job `windows-latest` chỉ chạy ở `master`,
`workflow_dispatch`, hoặc PR gắn nhãn `windows`.
