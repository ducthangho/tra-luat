# Đặc tả packet — QUY-TRINH-LAP-REVIEW-VA-DIEU-KIEN-DUNG (revision 12)

- `packet_id`: **QUY-TRINH-LAP-REVIEW-VA-DIEU-KIEN-DUNG**; ID bền `wp523`.
- `packet_issue`: **523** · `mission_issue`: **499**
- `revision`: **12** · `generation`: **11** · soạn **20-09-2026**
- `thay_the_cho`: **revision 11** (`spec_sha256`
  `42b0f477b7db2b1cb954ee9a345c9fcc1a2fb805ec9c260461187180fdc4226b`, 474 dòng, nhánh
  `claude/spec-quy-trinh-r11-20260913`). r11…r1 **giữ nguyên trên đĩa làm hồ sơ**.
- `executor`: **`claude`** · `reviewer_provider`: **`human` (chủ kho)** · `assurance_target`:
  **`human_audited`**
- `review_class`: **`sensitive`** — không đổi.

> **r12 LÀ MỘT REVIEW RESCUE CHECKPOINT (§12), KHÔNG phải một vòng vá nữa.**
> Chỉ thị chủ kho: PR #529 `issuecomment-5751125101` (`ducthangho`, OWNER, `2026-09-20T16:36:19Z`),
> đã đọc ngược qua API. Nguyên văn: *"Review Rescue Checkpoint theo §12 — đi đường (a), tách slice ổn."*

## `nguon_cap_viec`

Chỉ thị trên. §3.2 nói thẳng: *"Đổi objective, acceptance, write set, dependency, **executor** hoặc
environment tạo revision mới và làm lease cũ mất hiệu lực"*. r12 đổi **bốn** thứ trong danh sách ấy
(objective, acceptance, write set, executor), nên nó **phải** là revision mới + generation mới +
cấp lại lease. Lease gen 10 (`quy-trinh-lap-review-r11-exec-10-codex-20260913`) **mất hiệu lực**, và
nó cũng đã **hết hạn** `2026-09-14T12:00Z` từ trước.

## VÌ SAO CÓ r12 — một phép đếm, không phải một cảm giác

Chín lượt cross-review cho một thay đổi **201 dòng, toàn tài liệu**. Verdict lượt 9: **`blocked`**,
`0 P1 · 3 P2 · 1 P3 · 9 thể hiện`. Trần ADR-0048 là **mười** lượt ⇒ còn **đúng một**.

Phép đo quyết định — **không lớp mở nào là lỗi của nội dung skill**:

| lớp | chạm thật sự | trong write set r12? |
|---|---|---|
| `dac-ta-r5-giu-luat-cu-trai-tieu-chi-moi` | `LEASE:130` | **không** |
| `bien-nhan-thieu-so-ci-da-chi` | ledger + `receipt5` | **không** |
| `bien-nhan-luot-8-lan-du-lieu-luot-6` | `receipt8` | **không** |
| `phep-do-doctrine-khong-du-rang` | bộ quét `doctrine-scan` | **không** — `S4` cấm |

Ba lớp là **hồ sơ của chính packet**; lớp thứ tư là **nợ scanner có sẵn** (reviewer: *"lớp cũ còn
sống, không phải regression r10"*). Tức packet đang tiêu lượt review để sửa hồ sơ của các lượt
review trước, chứ không phải để sửa nội dung skill.

`CLAUDE.md`: *"cùng một hình dạng lặp ba lần trở lên thì câu hỏi đúng là **có nên làm việc này
không**, không phải **vá thế nào**"*. Ở đây hình dạng ấy lặp tới lượt thứ chín.

## `muc_tieu` — CHỈ nội dung skill

**M-SLICE:** đưa nội dung `M1`–`M10` của quy trình lặp review vào hai tệp skill, hợp nhất với bản
master hiện hành, **không mang theo hồ sơ review của packet**.

`M1`–`M16` và `M17-GO` của r11 **giữ nguyên** làm định nghĩa nội dung phải có. r12 **không** đổi một
mục tiêu nội dung nào; nó chỉ **thu hẹp phạm vi giao hàng**.

## `write_set` — ĐÚNG HAI đường

| # | đường dẫn | kiểu |
|---|---|---|
| 1 | `.claude/skills/cross-review/SKILL.md` | exact |
| 2 | `.claude/skills/work-packet/SKILL.md` | exact |

**BỎ** `ops/reviews/` (prefix) của r3–r11. Checkpoint nói rõ *"KHÔNG mang theo hồ sơ review của
packet"*.

**Hệ quả phải nói trước:** biên nhận `human_audited` của lượt này nằm ở `ops/reviews/`, tức **ngoài
write set r12**. Nó đi bằng một **PR bookkeeping riêng** — tiền lệ #567 cho #551. Đừng đọc việc ấy
thành "slice thiếu biên nhận".

**KHÔNG** đụng `docs/PROTOCOL_DA_PHIEN.md`, `.claude/hooks/**`, `packet_loop.py`, `CHANGELOG.md`,
`RELEASE_MANIFEST.json`, hay r1–r11 của chính đặc tả này.

Đo được (20-09-2026, `origin/master` `700ca8c`): `.claude/**` có **0/180** tệp trong
`RELEASE_MANIFEST.json` ⇒ slice **không** tái sinh manifest, **không** ghi lại golden.
`CHANGELOG.md` **có** trong manifest — đó là lý do nó bị loại khỏi write set.

## `assurance` — `human_audited`, và nói thẳng nó YẾU HƠN ở chỗ nào

`codex` **hết hạn token** (`access_token=-24.9h`, đo 20-09-2026) và `agy` không có CLI trong
container ⇒ `cross_approved` **không đạt được**. §8 cho class `sensitive` hai đường ngang hàng, nên
`human_audited` là đường còn lại — **không phải một lần hạ ngưỡng**.

**Nhưng nó yếu hơn r6–r11 theo một cách phải khai:** `M16` của r6 đặt *"reviewer dựng PHÉP ĐO"* làm
trụ, và chín lượt codex đã dựng thước thật. **Một lượt audit của người không dựng thước** — nó xác
nhận *"tôi đã đọc và chấp nhận"*. Chữ ký ấy **không thay được phép dò tìm**. Ai đọc `approve` của
r12 thành *"đã qua cùng mức soi như các lượt trước"* là đọc sai.

## `ngoai_pham_vi`

1. **KHÔNG vá bốn lớp mở trong slice này.** Chúng đã thành nợ có Issue: **#582** (ba lớp hồ sơ) ·
   **#583** (lớp scanner, cần packet riêng theo `S4`).
2. **KHÔNG hoàn nguyên phần master đã có.** master đã trôi **+212/−53** trên chính hai tệp ấy kể từ
   `merge-base 19de566`. Hợp nhất phải **giữ cả hai phía**; mất một mục của master là hỏng.
3. **KHÔNG tự định nghĩa `P1`/`P2`/`P3`** (kế thừa `ngoai_pham_vi` 9 của r11 — kho không có nguồn
   định nghĩa cả ba; khai nợ, đừng lấp chỗ trống).
4. **KHÔNG sửa biên nhận / `VERDICT.md` của các lượt đã giao** — chúng neo theo băm, `t26`/`t27` canh.
5. **KHÔNG dựng lại cổng quét tên.** `M17-GO` của r10 gỡ nó có căn cứ đo được: cả ba lần lớp chép
   doctrine bị bắt đều do reviewer **ĐỌC**, không lần nào do bộ quét, và bộ quét mù hai lần theo hai
   cách khác nhau.
6. **KHÔNG nới write set để "tiện tay"** — thêm đường thứ ba là `S1`, phải DỪNG và xin revision.

## `nghiem_thu`

| # | nghĩa vụ | đo thế nào |
|---|---|---|
| `A1` | Diff cuối chạm **đúng hai** tệp trong write set, không tệp nào khác | `git diff --name-only` so `base_sha` |
| `A2` | Mọi mục `M1`–`M10` của r11 **có mặt** trong bản hợp nhất | đối chiếu chuỗi đặc trưng; kỷ luật đọc, **không** phải cổng |
| `A3` | **Không mục nào của master bị mất** trong hợp nhất | đối chiếu chuỗi đặc trưng của phía master |
| `A4` | Bảy cổng đạt, **delta so nền master = 0** | `rc` đọc TRỰC TIẾP từng tiến trình, **không qua pipe** |
| `A5` | `release-verify --strict` giữ `ok=true`, `expected == checked` | `180 == 180` ở nền 20-09 |
| `A6` | Chủ kho đọc **đúng diff hai tệp** trên exact `reviewed_sha` rồi ký | comment có `author_association: OWNER`, đọc ngược qua API |

**Nền đã đo (20-09-2026, `origin/master` `700ca8c`, `core.abbrev=7`):**

| cổng | `rc` nền | ghi chú |
|---|---|---|
| `doctrine-scan` | **0** | sạch, quét 10 tệp |
| `adr-song` | **0** | |
| `doc-claims-check --strict` | **0** | |
| `bien_nhan_v2` | **0** | `132 ĐẠT v2 · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 185` |
| `release-verify --strict` | **0** | `ok=true`, `180 == 180`, `package_hash_match=true` |
| `git diff --check` | **0** | |
| `lease_publish_test` | **1** | **ĐỎ SẴN 164/166** — `t137` và `t159`, cả hai `KHÔNG ĐO ĐƯỢC: thiếu shellcheck` |

`lease_publish_test` **đỏ sẵn vì container không có `shellcheck`**, không phải vì slice. Tiêu chí là
**DELTA = 0**, không phải "0 tuyệt đối" — cùng doctrine với ngưỡng ruff ở `CLAUDE.md`.

`bien_nhan_v2` phải đo theo **bất biến**, không theo số tuyệt đối: `vi phạm == 0` và
`KHÔNG ĐO ĐƯỢC == 0`; `miễn trừ legacy == 11/11`; `NỢ đóng băng` không tăng; `ĐẠT v2` **không giảm**
so nền đo lại **ngay trước** gate. Nền đã trôi `124 → 131 → 132` trong ba ngày — ghim số tuyệt đối
là tự báo động giả.

## `dieu_kien_dung` — DANH SÁCH ĐẦY ĐỦ, KHÔNG kế thừa qua con trỏ

Kế thừa nguyên tắc của r7: mục này **không** trỏ sang lease hay revision khác. Danh sách dưới đây là
bản có thẩm quyền DUY NHẤT, và lease gen 11 phải chép **đúng** nó.

- **`S1`** — cần đường dẫn thứ BA ngoài hai tệp skill. DỪNG, xin revision.
- **`S2`** — tổng dòng thêm của **HAI tệp sản phẩm**, đo từ `base_sha` tới head cuối, **> 300**
  (trần ADR-0044 cho `sensitive`). **KHÔNG cộng hai khoảng.**
- **`S3`** — muốn đụng `docs/PROTOCOL_DA_PHIEN.md` hay `.claude/hooks/**`.
- **`S4`** — muốn vá `packet_loop.py` / `doctrine-scan`: KHÔNG trong write set; nợ riêng **#583**.
- **`S5`** — muốn sửa `VERDICT.md` hoặc biên nhận của một lượt đã giao (neo theo băm).
- **`S6`** — muốn đổi định nghĩa `P1`/`P2`/`P3` hay đổi slug của một lớp cũ (slug là **khoá đếm**).
- **`S7`** — hợp nhất ba chiều làm **mất** một mục của master hoặc của #529 mà không có chỗ đặt lại.
  DỪNG và báo chủ kho; KHÔNG bỏ bớt cho hết xung đột.
- **`S8` ĐÃ RÚT từ r7** — số để trống có chủ đích, KHÔNG đánh số lại.
- **`S12'`** — chuẩn bị đóng băng mà phép quét *"còn sót luật cũ"* chỉ khớp theo **TÊN**, hoặc hạ một
  luật xuống thành *"báo cáo để người đọc tự phán"*. Đó là phép dò chính tả, không phải phép đo.
- **`S13` (mới ở r12)** — muốn vá **bất kỳ lớp nào trong bốn lớp mở** để lấy `approve`. Đó là **LÁCH
  checkpoint**: chúng đã được chuyển thành nợ có Issue, và vá lẻ ở đây làm slice phình đúng thứ
  checkpoint sinh ra để cắt. DỪNG.
- **`S14` (mới ở r12)** — chủ kho **không** đọc được trọn diff hai tệp trước khi ký, hoặc muốn ký
  dựa trên tóm tắt của executor. `human_audited` §8 đòi người audit **tự đọc spec/diff**; một chữ ký
  trên bản tóm tắt là `KHÔNG ĐO ĐƯỢC`, không phải `approve`.

## `chua_do_duoc` — khai thẳng

1. **Tập lớp mở lấy từ `findings_ids` của lượt 9.** Nếu một finding lượt 1–8 nhắm vào **nội dung
   skill** từng bị bỏ im lặng thay vì vá, nó không hiện trong tập ấy và r12 không thấy.
2. **Hợp nhất ba chiều có thể làm mất nội dung theo cách cổng không thấy.** `doctrine-scan` và
   `doc-claims-check` không đo *"đủ mục hay chưa"*. `A2`/`A3` là **kỷ luật đọc**, không phải cổng —
   nói ra để không ai đọc chúng thành đã có máy canh.
3. **Slice land KÈM `phep-do-doctrine-khong-du-rang` còn mở.** Scanner vẫn mù hai dạng chép sau khi
   land. Đánh đổi **có chủ đích và được khai**.
4. **Không cổng nào cưỡng chế `M1`–`M10`** — chúng là chữ, tức kỷ luật đọc. Chính skill phải khai
   điều này (`ngoai_pham_vi` 2 của r3 đòi vậy).
