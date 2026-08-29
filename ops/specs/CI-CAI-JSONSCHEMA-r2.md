# ĐẶC TẢ ĐÓNG BĂNG — `CI-CAI-JSONSCHEMA` — **BẢN SỬA ĐỔI 2**

Thay bản 1 (`d98702ff035e5bb7…`). Bản 1 **vẫn đúng về nguyên nhân** nhưng **sai về tầm**: nó
chỉ vá `ci.yml` cho đúng một tên gói. Chủ kho đòi một **QUY TẮC**: thêm bất kỳ công cụ/gói nào
vào skill thì môi trường runtime phải được bảo đảm có nó.

Kho **đã có sẵn** cơ chế cho luật ấy và bản 1 không dùng: `ops/cong_cu.yaml` — bản kê công cụ
tất định, một nguồn cho probe, canary, cổng G5 và lệnh cài **theo từng nền**
(`linux|macos|windows`). Bản 2 đặt `jsonschema` vào đúng chỗ ấy và dựng phép đo bao phủ trỏ
vào **bản kê**, không trỏ vào một dòng `pip install`.

**GIỚI HẠN LỜI KHAI:** chứng minh BYTE tới consumer adapter. KHÔNG tuyên bố model "đã hiểu".
**Ba trạng thái:** có · không · **KHÔNG ĐO ĐƯỢC** — trạng thái thứ ba làm cổng ĐỎ.

---

## VÌ SAO CÓ BẢN SỬA ĐỔI 2

Bản 1 đóng đúng một lỗ và để nguyên cái sinh ra lỗ. Lần sau ai thêm một `import` bên thứ ba
vào `.claude/dev/**` thì CI lại đỏ y hệt, và lại không ai thấy cho tới lúc merge.

Sai lầm ấy cùng họ với thứ chính packet W1-P1 vừa trả giá: **vá một thể hiện thay vì đóng một
lớp.** Ba vòng cross-review của W1-P1 mỗi vòng đóng một tầng của cùng một bệnh; bản 1 đang
lặp lại đúng nếp đó ở quy mô hạ tầng.

---

## Nguyên nhân — giữ nguyên từ bản 1

Thử merge #389 qua MCP:

```
405 Repository rule violations found
Required status check "gate (ubuntu-latest)" is failing.
```

Log lượt `gate` `33190773588` (head `6edbd046`, `pull_request`, `failure`):

```
File ".claude/dev/packet_loop.py", line 44, in <module>
  from review_verdict_binding import (
File ".claude/dev/review_verdict_binding.py", line 14, in <module>
  from jsonschema import exceptions as jsonschema_exceptions
ModuleNotFoundError: No module named 'jsonschema'
```

`gate` trên nhánh packet: `b92b401a` success → `47a50395` **FAILURE** → `4ac8b6a9` **FAILURE**
→ `6edbd046` **FAILURE`. `jsonschema` không được khai ở `requirements*`, `pyproject.toml`, hay
workflow nào.

**Bốn vòng cross-review không thấy** vì cả bốn chạy trong container có sẵn `jsonschema 4.26.0`,
và bundle reviewer không cấp đường đọc kết quả CI.

---

## WINDOWS — đo được, KHÔNG phải suy luận

```
job `gate` · runs-on: ${{ matrix.os }} · ["ubuntu-latest","windows-latest"]
bước "cài PyYAML (bộ cổng đăng lease cần)" : KHÔNG có `if:` ⇒ chạy trên CẢ HAI nền
```

Nên phụ thuộc thêm vào bước ấy là Windows có luôn. Ma trận chỉ quyết định **khi nào**
`windows-latest` được bật (master · `workflow_dispatch` · PR gắn nhãn `windows`) — đó là câu
hỏi khác với **chạy thì có cài không**.

**BẪY NỀN, phải tuân:** `CLAUDE.md` ghi *"Không được giả định Windows có `python3`"*. Mọi probe
và mọi lệnh cài trong bản kê phải dùng `python`, KHÔNG `python3`.

---

## Write set — BA đường

```
ops/cong_cu.yaml
ops/cong_cu_test.py
.github/workflows/ci.yml
```

`T6` trong `ops/cong_cu_test.py` (d.141–156) chốt allowlist setup bằng **tên bước → tuple lệnh
CHÍNH XÁC**; dòng `pip install` nằm nguyên văn ở d.146. Đổi `ci.yml` mà không đổi `T6` ⇒ `T6` ĐỎ.

**KHÔNG đụng** `.claude/dev/**` (đang bị lease `w1-p1-…-exec-4` giữ), **KHÔNG** `ops/cong_cu.py`
(cơ chế đã đủ — xem dưới), **KHÔNG** `ops/lease_publish.py`.

**Đã đo rằng `ops/cong_cu.py` KHÔNG cần sửa:** `_chay(pb["lenh"])` gọi
`subprocess.run(argv)` với argv bất kỳ (d.64), không giả định nhị phân — nên probe dạng
`[python, -c, "import jsonschema; ..."]` chạy được nguyên trạng. Nếu khi thi công phát hiện
ngược lại thì đó là **S1**: DỪNG, khai, đừng lặng lẽ mở tệp thứ tư.

---

## QUY TẮC — đây là sản phẩm chính của packet

> **Thêm một công cụ hoặc gói vào bất kỳ mã nào của kho thì phải khai nó trong
> `ops/cong_cu.yaml` kèm lệnh cài cho MỌI nền mà cổng chạy trên đó. Chưa khai thì cổng ĐỎ.**

Luật viết trong tài liệu không chạy. Nên luật này phải là **một ca test**, không phải một đoạn
văn — đúng bài học `CLAUDE.md`: *"NGHĨ RA được phép thử mà KHÔNG CHẠY nó thì phép thử ấy KHÔNG
TỒN TẠI"*.

---

## Mục nghiệm thu

**A1 — khai `jsonschema` trong bản kê.** Mục `cong_cu.jsonschema` phải có: `ban_ghim: "4.26.0"`
(ghim CHÍNH XÁC — đúng bản mọi phép đo của W1-P1 đã chạy trên đó), `probe` dùng `python`
(KHÔNG `python3`) bắt trọn token phiên bản, và `cai` chạy được trên cả ba nền. `bat_buoc` đặt
theo đúng ngữ nghĩa schema, và nếu đặt `false` thì phải nói VÌ SAO ngay tại chỗ.

*Phép đo làm nó ĐỎ:* gỡ mục ấy khỏi bản kê ⇒ A2 phải ĐỎ.

**A2 — phép đo BAO PHỦ, trỏ vào BẢN KÊ.** Thêm một ca vào `ops/cong_cu_test.py` **tự dẫn xuất**
tập module bên thứ ba mà `.claude/dev/*.py` và `ops/*.py` import (quét AST, loại
`sys.stdlib_module_names`, loại stem tệp nội bộ), rồi đòi MỖI tên trong tập ấy **có mặt trong
`ops/cong_cu.yaml`**.

Ghi cứng `"jsonschema"` là **danh sách CẤM trá hình** — đóng đúng lần này, mù với gói kế tiếp.
`CLAUDE.md` đã trả giá bốn lần cho hình dạng ấy.

*Phép đo làm nó ĐỎ, và phải chạy được NGAY HÔM NAY:* bơm `import mot_goi_khong_ton_tai` vào một
tệp tạm trong phạm vi quét ⇒ ca phải ĐỎ. Không có vế này thì A2 hôm nay xanh mà **chưa đo gì** —
đúng bệnh *"ca có MẶT khác ca có ĐO"*.

**A3 — CI thật sự cài.** Bước `pip install` của job `gate` phải cài `jsonschema` ghim đúng bản
mà A1 khai. Hai chỗ lệch nhau là hai bản trôi — nên thêm một chốt đòi **bản ghim trong
`cong_cu.yaml` khớp bản trong `ci.yml`**.

*Phép đo làm nó ĐỎ:* đổi một trong hai bản ghim ⇒ chốt phải ĐỎ.

**A4 — `T6` cập nhật khớp, KHÔNG nới.** Allowlist phải khớp ĐÚNG dòng `pip install` mới. Cấm
nới thành so lỏng (`startswith`, `in`) — nới là gỡ chính cổng ấy.
*Phép đo làm nó ĐỎ:* thêm một bước setup lạ trước G5 ⇒ `T6` vẫn phải ĐỎ.

**A5 — gate XANH trên CẢ HAI nền.** `gate (ubuntu-latest)` phải `success`; và vì packet này
đụng hạ tầng công cụ, phải gọi tay `workflow_dispatch` để có **`gate (windows-latest)`** cũng
`success` TRƯỚC khi merge. `CLAUDE.md` ghi rõ: gắn nhãn `windows` KHÔNG sinh lượt chạy nào
(`ci.yml` khai `pull_request:` không kèm `types:`), nên nhãn là đường SAI.
Đây là mục duy nhất không đo được offline — đọc qua endpoint MCP `/mcp/x/actions`.

**A6 — không đụng hành vi nào khác.** Mọi ca sẵn có của `ops/cong_cu_test.py` giữ nguyên;
`python ops/cong_cu.py kiem-tra --json` không đổi kết quả ngoài mục mới.

---

## TRÌNH TỰ — chỗ dễ sai nhất, giữ nguyên từ bản 1

`review_verdict_binding.py` **chỉ tồn tại trên nhánh packet**, chưa có trên `master`. Nên hôm
nay trên master **không mã nào import `jsonschema`**. Packet này khai và cài một phụ thuộc cho
thứ **sắp** tới. Cố ý, và đúng thứ tự: **land packet này trước, merge #389 sau** — ngược lại
thì #389 không bao giờ qua nổi gate để mà merge.

Hệ quả cho A2: phép đo phải **tự dẫn xuất**, nên hôm nay nó thấy `yaml` và ngày mai tự thấy
`jsonschema`. Đó là lý do A2 cần vế "import giả" để chứng minh có răng ngay bây giờ.

---

## Nền phải ĐO LẠI trước khi bắt đầu

Trên `origin/master` sạch, clone (**KHÔNG worktree**), `git config core.abbrev 7`,
`PYTHONDONTWRITEBYTECODE=1` + `PYTHONPYCACHEPREFIX` ra ngoài cây:

```
python ops/cong_cu_test.py
python ops/cong_cu.py kiem-tra --json
actionlint                          <- CẦN shellcheck TRÊN PATH
```

**`actionlint` thiếu `shellcheck` trên PATH thì tự tắt tích hợp TRONG IM LẶNG** và trả
`rc=0 / 0 finding` — trông TỐT HƠN nền, thật ra không đo gì. W1-P1 đã vấp đúng chỗ này.

Đặc tả CỐ Ý không chép số nền: một con số không ghi ĐIỀU KIỆN ĐO thì sẽ trôi mà không ai biết.

---

## Điều kiện DỪNG

- **S1** cần đường dẫn thứ TƯ — kể cả khi hoá ra `ops/cong_cu.py` phải sửa ⇒ DỪNG, khai.
- **S2** vượt **120 dòng thêm+xoá** ⇒ DỪNG. (Bản 1 đặt 80 cho hai tệp; bản 2 có ba tệp và một
  mục bản kê đầy đủ. Vượt xa 120 nghĩa là đã hiểu sai phạm vi.)
- **S3** muốn nới `T6` thay vì cập nhật nó ⇒ DỪNG. Nới là gỡ cổng.
- **S4** muốn ghi cứng tên `jsonschema` làm phép đo bao phủ ⇒ DỪNG, xem A2.
- **S5** muốn sửa `.claude/dev/**` ⇒ DỪNG, đang bị lease `w1-p1-…-exec-4` giữ.
- **S6** chạm trần HAI vòng review (ADR-0043) ⇒ DỪNG, không tự nâng.

---

## Nợ đi kèm, KHÔNG thuộc packet này

**`bundle-reviewer-mu-voi-CI`** — bốn vòng cross-review của W1-P1 không có đường đọc kết quả CI,
nên cả một LỚP lỗi ("xanh ở đây, đỏ ở nơi tính điểm") nằm ngoài tầm với của reviewer. Cùng họ
bài học *"reviewer không đo được thì review chỉ là soát chính tả"*. Cách chữa thuộc
`.claude/skills/cross-review/SKILL.md` và quy trình dựng bundle ⇒ packet riêng.

**`quy-tac-cong-cu-chua-vao-doctrine`** — quy tắc ở trên sau khi có cổng canh thì nên có một
dòng trong `CLAUDE.md` và một dòng trong `docs/PROTOCOL_DA_PHIEN.md` §20 trỏ về nó. Cả hai tệp
đều ngoài write set ba đường ⇒ packet riêng. **Thứ tự đúng là CỔNG TRƯỚC, CHỮ SAU** — ngược lại
thì ta có một câu doctrine không ai cưỡng chế, đúng thứ ADR-0043 vừa trả giá (`review_rounds_used`
và `nang_tran`: 0 tệp cưỡng chế).

**KHÔNG ĐO ĐƯỢC:** chưa có phép đo nào cho môi trường runtime Cowork. `.claude/**` bị loại khỏi
gói phát hành (`_RELEASE_EXCLUDE_DIRS`), nên `jsonschema` KHÔNG cần cho runtime skill — nhưng câu
ấy hiện dựa trên đọc cấu hình, chưa có ca test nào khoá. Khai là **KHÔNG ĐO ĐƯỢC**, không làm tròn.
