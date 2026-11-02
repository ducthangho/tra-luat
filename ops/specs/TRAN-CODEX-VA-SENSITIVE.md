# Đặc tả packet — TRAN-CODEX-VA-SENSITIVE (revision 1)

- `packet_id`: **TRAN-CODEX-VA-SENSITIVE**; ID bền `wp<packet_issue>`.
- `packet_issue`: **(để trống — chủ kho cấp)**
- `mission_issue`: **(để trống — chủ kho cấp)**
- `revision`: **1** · `generation`: 1 · soạn **16:56Z 16-10-2026**
- `base`: `origin/master` @ `653fef3f` (đo 16:56Z 16-10-2026)
- `depends_on`: **`[]`**
- `executor`: claude · `environment`: cloud
- `risk`: **sensitive** · `review_class`: **sensitive** (đổi hai ADR đang hiệu lực về ngân sách review và
  ngưỡng kích thước — tức REVIEW AUTHORITY; cùng lớp với tiền lệ `TRAN-VONG-REVIEW-LEN-BON`)

## `nguon_cap_viec`

Chỉ thị chủ kho `ducthangho` **16-10-2026**, truyền qua phiên điều phối `session_01CSM7GNazhN6uGJb4v1TqBT`
rồi được chủ kho **xác nhận trực tiếp** trong phiên soạn spec này (trả lời *"Đồng ý các khuyến nghị"*):

1. Trần **lời gọi Codex mỗi PR** (trục LỜI GỌI, `codex_review_calls_used`): **2 → 8**.
2. Trần kích thước packet **`sensitive`** của `ADR-0044`: **≤ 3 tệp / ≤ 300 dòng thêm → ≤ 6 tệp / ≤ 450
   dòng thêm**. Chủ kho ban đầu nêu `≤ 10 tệp`; đã đổi thành **6** theo Q1 dưới đây.

Tiền lệ đúng hình dạng: `ADR-0048` (packet `TRAN-VONG-REVIEW-LEN-BON` r2, PR #524/#527) — thay **đúng một
con số** của một ADR đang hiệu lực, không hồi tố, con số chỉ một chỗ ở.

## Quyết định đã chốt với chủ kho (16-10-2026)

| # | câu hỏi | quyết định |
|---|---|---|
| Q1 | Trần `sensitive` 10 tệp vượt trần packet thường (6 tệp) — đảo thứ bậc của `ADR-0044` | **≤ 6 tệp / ≤ 450 dòng thêm**. Trần packet thường (≤ 6 tệp / ≤ 1.000 dòng thêm+xoá) **KHÔNG đổi**. Khác đơn vị giữa hai trần (`thêm` so với `thêm+xoá`) giữ nguyên, ngoài phạm vi |
| Q2 | Một hay hai ADR | **Hai**: `ADR-0052` (trục LỜI GỌI), `ADR-0053` (kích thước `sensitive`) |
| Q3 | Đọc "review đầu + rereview" và luật `systemic` khi trần là 8 | Mọi lượt Codex **thứ hai trở đi** (2…8) chỉ được cấp khi còn P0/P1, finding cắt ngang hoặc cần xác minh lại; hết lượt 8 chưa approve ⇒ Review Rescue Checkpoint |
| Q4 | Mức DÀNH SẴN của `ADR-0041` ("tối đa hai Codex review cho PR `sensitive`") | **Giữ 2.** Trần 8 là TRẦN được dùng, không phải mức dành sẵn. `ADR-0041` không đổi; `ADR-0052` phải nói tường minh điều này |
| Q5 | Hồi tố | **Không.** Neo `spec_hash` đóng băng, mốc = ngày ADR được chấp nhận, như `ADR-0048` |
| Q6 | Chép số mới hay trỏ | **Trỏ.** Con số chỉ ở ADR mới; `docs/PROTOCOL_DA_PHIEN.md` trỏ, không chép |

## Số ADR

`docs/adr/` trên `origin/master` có tới `0050` (đo 16:56Z 16-10-2026). **`0051` đã bị chiếm** trên nhánh
`claude/human-audited-khai-ai-dang-r1` (`docs/adr/0051-human-audited-khai-ai-dang-va-gioi-han-cua-no.md`,
chưa merge) — đo bằng `git ls-tree` trên **mọi** `refs/remotes/origin/*` sau `git fetch` đầy đủ. Nên dùng
**`0052`** và **`0053`**. Đo lại trước khi commit ADR; nếu số đã bị chiếm thì DỪNG hỏi, đừng tự nhảy số.

## VẤN ĐỀ ĐO ĐƯỢC — con số LỜI GỌI đang bị CHÉP ở năm chỗ trong protocol

`rg` trên `docs/ ops/ .claude/ .agents/ AGENTS.md CLAUDE.md CONTEXT.md` (đo 16:56Z 16-10-2026, bỏ
`ops/reviews/`, `ops/leases/`, `ops/evidence/`):

| tệp:dòng | nội dung | xử lý |
|---|---|---|
| `docs/PROTOCOL_DA_PHIEN.md:695` | "Trần 2 lượt Codex/PR … không đổi" | đổi sang TRỎ `ADR-0052` |
| `docs/PROTOCOL_DA_PHIEN.md:713-717` | "tối đa hai lượt Codex: một review đầu và một rereview… Lượt hai chưa approve…" | đổi sang TRỎ `ADR-0052`, bỏ số |
| `docs/PROTOCOL_DA_PHIEN.md:728` | `systemic`: "chỉ cấp lượt hai khi còn P0/P1…" | đổi theo Q3: "lượt thứ hai trở đi", không số trần |
| `docs/PROTOCOL_DA_PHIEN.md:1123` | "Hai lượt Codex review trên cùng PR là một stop condition" | TRỎ `ADR-0052` |
| `docs/PROTOCOL_DA_PHIEN.md:1129` | "tối đa hai trên một PR" | TRỎ `ADR-0052` |
| `docs/adr/0036:6-7`, `0037:5`, `0038:7`, `0041:9` | chép "hai lượt" | **KHÔNG sửa** — hồ sơ đã đóng; con trỏ tiến nằm ở §20 |
| `docs/adr/0044:5` | "≤ 3 tệp và ≤ 300 dòng thêm" | **KHÔNG sửa** — `ADR-0053` thay số; con trỏ tiến ở §20 |
| `.claude/skills/soan-spec/SKILL.md:89` | trỏ `0044` cho ngưỡng | **ngoài write set** — xem `ngoai_pham_vi` #4 |

**Mã và cổng: KHÔNG chỗ nào ghi cứng hai con số.** `rg -l "codex_review_calls_used|review_calls" --type py .`
⇒ **0 tệp** (đo 16:56Z 16-10-2026). §20 ghi `ADR-0044` → **`0 cổng`**. Nên packet này **không** đụng
Python, không có delta ruff.

## `review_class` và ngưỡng

`sensitive` ⇒ ngưỡng **CŨ** của `ADR-0044` áp cho chính packet này (≤ 3 tệp, ≤ 300 dòng thêm), vì đặc tả
này đóng băng **TRƯỚC** khi `ADR-0053` được chấp nhận — đúng luật không hồi tố mà nó ban hành. Packet này
**3 tệp**, ước lượng ~180–250 dòng thêm (ADR-0048 tham chiếu ~150 dòng).

## `write_set`

| # | đường dẫn | vì sao |
|---|---|---|
| 1 | `docs/adr/0052-tran-loi-goi-codex-len-tam.md` | ADR mới — trục LỜI GỌI 2 → 8 |
| 2 | `docs/adr/0053-tran-kich-thuoc-sensitive-len-sau-tep.md` | ADR mới — trần `sensitive` 3/300 → 6/450 |
| 3 | `docs/PROTOCOL_DA_PHIEN.md` | năm chỗ chép số → trỏ; dòng §20 cho `0052`, `0053`; ghi chú thay số ở các dòng §20 của `0036`, `0037`, `0038`, `0044` |

Không ký tự đại diện. `ai-dang-giu` cho cả ba đường dẫn ⇒ **`NGƯỜI_GIỮ 0`**, `rc=0` (đo 16:5xZ 16-10-2026,
sau khi đồng bộ `master` cục bộ — lần đầu bị `CHAN [12] NHÁNH_CỤC_BỘ_TỤT_SAU`). Đo lại trước khi cấp lease.

## `ngoai_pham_vi`

1. **KHÔNG sửa ADR cũ** (`0036`, `0037`, `0038`, `0041`, `0043`, `0044`) và **KHÔNG sửa đặc tả đã đóng
   băng nào** — cùng lý do `ADR-0048`: sửa là viết lại một lời khai đúng tại thời điểm của nó.
2. **KHÔNG đổi trục VÒNG** (`ADR-0048`, mười) và **trục ATTEMPT**.
3. **KHÔNG đổi trần packet thường** (≤ 6 tệp / ≤ 1.000 dòng thêm+xoá) và **KHÔNG** thống nhất đơn vị
   `thêm` / `thêm+xoá` giữa hai trần.
4. **KHÔNG sửa `.claude/skills/soan-spec/SKILL.md:89`** — đặt vào thì write set thành 4 tệp, vượt trần
   `sensitive` CŨ đang áp cho chính packet này. Dòng ấy trỏ `ADR-0044` (vẫn tồn tại, không phải con trỏ
   chết), người đọc tới ngưỡng qua §20. Ghi là **nợ** cho một packet `routine` sau khi `ADR-0053` land.
5. **KHÔNG đổi mức dành sẵn của `ADR-0041`** (Q4).
6. **KHÔNG viết cổng nào canh hai trần** — `codex_review_calls_used` không có bộ đếm trong mã; ngưỡng
   kích thước `0 cổng`. Xem `chua_do_duoc`.

## `muc_tieu`

| # | mục tiêu | chiếu vào |
|---|---|---|
| M1 | `ADR-0052` khai trần LỜI GỌI Codex mỗi PR là **tám**; trỏ `ADR-0036`/`0037`/`0038` là nơi số cũ được chép; nói tường minh trục VÒNG và ATTEMPT không đổi | #1 |
| M2 | `ADR-0052` khai luật cấp lượt theo Q3 và giữ mức dành sẵn **hai** của `ADR-0041` theo Q4 | #1 |
| M3 | `ADR-0052` ghi rằng với reviewer Codex, trần 8 lời gọi chạm **trước** trần 10 vòng (lời gọi đếm cả lượt hỏng; vòng chỉ đếm verdict hợp lệ) | #1 |
| M4 | `ADR-0053` khai trần `sensitive` là **≤ 6 tệp và ≤ 450 dòng thêm**; trần thường không đổi; trỏ `ADR-0044` là tiền nhiệm | #2 |
| M5 | Cả hai ADR khai luật hiệu lực **không hồi tố**: mốc = ngày chấp nhận, thứ neo = `spec_hash` đóng băng | #1, #2 |
| M6 | Cả hai ADR giữ cơ chế vượt trần `nang_tran` (`ai_nang`, `can_cu`, `tran_cu`, `tran_moi`) và nói thẳng **không cổng nào cưỡng chế** nó (không chép lời khai sai của `ADR-0043`) | #1, #2 |
| M7 | Protocol: năm chỗ chép số LỜI GỌI thành TRỎ `ADR-0052`; §20 có đúng một dòng cho mỗi ADR mới; dòng `0036`/`0037`/`0038`/`0044` ghi *đã bị thay số*, không xoá | #3 |

## `nghiem_thu`

**A1 (M7) — `adr-song` xanh.** `python3 .claude/dev/packet_loop.py adr-song --root .` ⇒ `rc=0`; số ADR trên
đĩa **BẰNG** số dòng §20. **Phép làm ĐỎ:** xoá dòng §20 của `0053` ⇒ `adr-song` ĐỎ (cổng đã có răng).

**A2 (M1, M7) — con số LỜI GỌI chỉ một chỗ ở.**
`rg -n "hai lượt Codex|2 lượt Codex|tối đa hai trên một PR|tám lượt|8 lượt" docs/PROTOCOL_DA_PHIEN.md` ⇒
**0 dòng**; cùng lệnh trên `docs/adr/0052-*.md` ⇒ ≥ 1. **Phép làm ĐỎ:** chép "tám lượt" hoặc giữ "hai lượt
Codex" ở bất kỳ dòng nào của protocol ⇒ khác 0 ⇒ ĐỎ.

**A3 (M4, M7) — con số `sensitive` chỉ một chỗ ở.** `rg -n "450 dòng|6 tệp và" docs/PROTOCOL_DA_PHIEN.md` ⇒
**0 dòng**. **Phép làm ĐỎ:** chép ngưỡng mới vào protocol ⇒ ĐỎ.

**A4 (M5) — luật hiệu lực cho đúng MỘT câu trả lời.** Kiểm bằng lời trên ba ca: (a) đặc tả đóng băng trước
mốc ⇒ trần cũ; (b) từ mốc trở đi ⇒ trần mới; (c) **chính đặc tả này** ⇒ trần `sensitive` CŨ. Hai ADR phải
nêu **mốc** và **thứ neo**. **Phép làm ĐỎ:** bỏ mốc hoặc viết "áp dụng cho mọi packet" ⇒ ca (c) mâu thuẫn
với write set 3 tệp ⇒ ĐỎ.

**A5 (M2) — `ADR-0041` không bị đọc là đổi.** `ADR-0052` có câu tường minh "mức dành sẵn hai của `ADR-0041`
không đổi". **Phép làm ĐỎ:** thiếu câu ⇒ người đọc suy dành sẵn 8 ⇒ ĐỎ (kiểm bằng đọc — chưa có máy).

**A6 (M6) — `nang_tran` giữ nguyên, lời khai cưỡng chế đúng mức.** Mỗi ADR mới có khối vượt trần đủ bốn tên
VÀ câu "không cổng nào cưỡng chế". Đo lại trước khi viết:
`rg -c "nang_tran|ai_nang|tran_cu|tran_moi" --type py .` ⇒ ghi số kèm giờ đo. **Phép làm ĐỎ:** ADR khai
"cổng đăng lease từ chối" trong khi đếm ra 0 ⇒ ĐỎ.

**A7 — `ADR-0044` cũ cho chính packet.** `git diff --numstat origin/master...HEAD` ⇒ đúng **3** đường dẫn ở
`write_set`, tổng `additions` ≤ **300**.

**A8 — `doctrine-scan` xanh.** `python3 .claude/dev/packet_loop.py doctrine-scan --root .` ⇒ `rc=0`.

**Điều kiện dừng:** `sensitive` ⇒ đòi cross-review khác nền **`approve`** tường minh (hoặc `human_audited`).
Trần lời gọi Codex cho chính PR này là trần **CŨ (2)** — đặc tả đóng băng trước `ADR-0052`.

## `hinh_dang_ke_thua`

`khong_ap_dung` — không phải packet khắc phục. Ghi kèm một hình dạng tiền lệ để reviewer soi:
`ADR-0048` bản đầu **chép lời khai cưỡng chế** từ `ADR-0043` ("không có khối ấy thì cổng đăng lease từ
chối") mà không đo, phải sửa ở r2. `A6` sinh ra để chặn đúng hình dạng ấy.

## `chua_do_duoc`

1. **Không cổng nào canh trần 8.** `codex_review_calls_used` không có bộ đếm trong mã (0 tệp `*.py`, đo
   16:56Z 16-10-2026). Nâng trần không đổi gì có thể đo được cho tới khi có bộ đếm — cùng họ nợ
   `SO-CANON-CHUA-TON-TAI`.
2. **Không cổng nào canh ngưỡng kích thước** (`ADR-0044` → `0 cổng` ở §20).
3. **Không đo được trần 8 hay 450 có "đúng"**: con số là **quyết định của chủ kho**. Không có dữ liệu kho
   nào về số lời gọi Codex thực dùng mỗi PR (`ops/PHAN_BIEN_QUY_TRINH_BUILD_REVIEW_20260905.md:143`: bộ đếm
   này được ghi ở **2/57** biên nhận). ADR không được khai mạnh hơn thế.
4. **Không có con trỏ tiến** từ `ADR-0036`/`0037`/`0038`/`0044` tới ADR mới ngoài bảng §20 — cùng nợ mà
   `ADR-0048` đã khai cho `ADR-0043`.
