# Đặc tả packet — QUY-TRINH-LAP-REVIEW-VA-DIEU-KIEN-DUNG (revision 13)

> **BẢN NHÁP — CHƯA ĐÓNG BĂNG.** Tập lớp còn thiếu kết quả cross-review của **#586** và **#597**
> (cả hai đang chạy lúc soạn). Chỉ đo `sha256` và neo lease sau khi tập lớp ĐỦ — một spec thiếu lớp
> sẽ phải bump ngay vòng sau, đúng thứ r13 sinh ra để chấm dứt.

- `packet_id`: **QUY-TRINH-LAP-REVIEW-VA-DIEU-KIEN-DUNG**; ID bền `wp523`.
- `packet_issue`: **523** · `mission_issue`: **499**
- `revision`: **13** · `generation`: **13** · soạn **21-09-2026**
- `thay_the_cho`: **revision 12** (`spec_sha256`
  `9fc90435ad7c8b4ae93d19f8b163c5cffca9168e3df6043d8fe54ab880fe8059`, 11 580 B, nhánh
  `claude/spec-quy-trinh-r12-20260920`). r12…r1 **giữ nguyên trên đĩa làm hồ sơ**.
- `executor`: **`claude`** · `reviewer_provider`: **`openai_codex`** · `assurance_target`:
  **`cross_approved`**
- `review_class`: **`sensitive`** — không đổi.

## Vì sao r13 PHẢI là revision mới — bốn cò §3.2, không phải một

§3.2: *"Đổi objective, acceptance, write set, dependency, **executor** hoặc environment tạo revision
mới và làm lease cũ mất hiệu lực."* r13 đổi **bốn** thứ trong sáu:

| cò | r12 | **r13** |
|---|---|---|
| `write_set` | đúng hai tệp skill | **thêm** `ops/leases/…exec-12….yaml` và `ops/reviews/**` |
| `acceptance` | ký một lần rồi land | **lặp** vá → cross-review theo LỚP → verdict, tới `cross_approved` |
| `assurance_target` | `human_audited` | **`cross_approved`** |
| `reviewer_provider` | `human` | **`openai_codex`** |

*(Liệt kê đủ **sáu** trường của §3.2 — bản r12 chỉ kể bốn và bỏ sót `dependency`, `environment`;
đó là lớp `revision-trigger-understatement`, xem `L-M` bên dưới.)*

## Vì sao r12 KHÔNG land — một phép đo, không phải một đổi ý

Chủ kho chốt r12 là **Review Rescue Checkpoint §12**: land slice ổn dưới `human_audited`, chuyển bốn
lớp mở thành nợ. Chữ ký đã có thật: `issuecomment-5757310858`, `ducthangho`, `OWNER`,
`2026-09-21T08:04:17Z`, dòng neo `Reviewed commit: 27283d2…` đúng một lần.

Rồi cross-review codex (`15:37Z`–`15:56Z`, chấm **theo LỚP**) ra **13 lớp**, và một lớp làm đổ tiền đề:

**`.claude/skills/cross-review/SKILL.md` tại `27283d2` mã hoá điều kiện dừng**

> \| `sensitive` \| **`approve` tường minh** của reviewer **khác nền** \|

**`docs/PROTOCOL_DA_PHIEN.md` dòng 665–666** nói

> `sensitive`: … Phải có Codex `cross_approved` **hoặc** `human_audited`; hết quota mà chưa có human
> thì pause.

Và `grep -c human_audited` trên **cả hai** tệp skill tại head ⇒ **0 · 0**.

Tức **201 dòng sắp land cấm chính con đường mà packet này vừa dùng để được duyệt.** Packet
`sensitive` kế tiếp gặp lúc codex hết quota sẽ va thẳng vào nó.

### Điều đáng ghi hơn con số

**Lượt audit của NGƯỜI đã ký duyệt một nội dung CẤM chính việc audit của người.** Chữ ký là thật,
việc đọc là thật, và nó vẫn bỏ sót. Đây là bằng chứng chạy được cho câu mà **chính biên nhận của
lượt ấy tự khai**:

> Một lượt audit của NGƯỜI không dựng thước — nó xác nhận *"tôi đã đọc và chấp nhận"*. Chữ ký ấy
> **KHÔNG thay được phép dò tìm**.

Lời khai đó viết ra như một sự thận trọng hình thức. Tám phút cross-review biến nó thành **phép đo**.
`M16` của r6 — *"reviewer dựng PHÉP ĐO"* — nay có phản chứng cho chiều ngược lại: bỏ phép dò tìm thì
mất đúng lớp mà chữ ký không thấy.

Hệ quả cho r13: `assurance_target` **phải** là `cross_approved`, và chữ ký `27283d2` **mất hiệu lực**
— không vì thủ tục, mà vì nó ký một nội dung sai.

## `muc_tieu`

**M-VÁ:** đóng **toàn bộ** tập lớp của lượt cross-review `21-09-2026`, rồi lặp vá → cross-review →
verdict cho tới khi đạt **`cross_approved`**.

**M-CI:** **full CI** (gồm Windows qua `workflow_dispatch`) trên head ứng viên trước khi đủ điều kiện
merge. Chỉ thị chủ kho `16:0xZ`. Lưu ý `ci.yml` chỉ thêm Windows cho `workflow_dispatch` hoặc nhãn
`windows`, và **gắn nhãn KHÔNG tự sinh lượt chạy** (workflow không khai `types: [labeled]`).

## BẢNG LỚP — 13 lớp, đếm theo LỚP; thể hiện đếm riêng

Nguồn: cross-review codex `21-09-2026`. Cột **đã tự đo** = phiên executor đã tái hiện độc lập, không
nhận lời khai.

### #585 — nội dung skill, head `27283d2` · `4 P1 · 4 P2`

| id | slug | hạng | chạm | đã tự đo |
|---|---|---|---|---|
| `L-A` | `adapter-loai-duong-human-audited` | **P1** | `cross-review/SKILL.md:451` | **CÓ** — `grep -c human_audited` = 0·0 so PROTOCOL:665-666 |
| `L-B` | `mien-review-sau-moi-lan-doi-head` | **P1** | `work-packet/SKILL.md:266` | chưa |
| `L-C` | `dieu-kien-dung-bo-quen-P0` | **P1** | `cross-review/SKILL.md:450` | chưa |
| `L-D` | `cam-tuyet-doi-workflow-dispatch` | **P1** | `work-packet/SKILL.md:280` | chưa — nhưng chỉ thị full CI của chủ kho **xác nhận bằng vận hành** |
| `L-E` | `M5-tinh-ty-le-bang-finding-khong-phai-lop` | P2 | `work-packet/SKILL.md:212` | chưa |
| `L-F` | `do-drift-tren-ref-cuc-bo-stale` | P2 | `cross-review/SKILL.md:235` | chưa |
| `L-G` | `khang-dinh-am-PR-512-khong-neo-run-id` | P2 | `work-packet/SKILL.md:288` | chưa |
| `L-H` | `suy-hoi-tu-tu-ty-le-bo-qua-lop-moi` | P2 | `work-packet/SKILL.md:249` | chưa |

### #587 — lease, head `0babf61` · `2 P1 · 3 P2`

| id | slug | hạng | chạm | đã tự đo |
|---|---|---|---|---|
| `L-I` | `renewal-moves-acceptance-baseline` | **P1** | lease gen 12 | **CÓ** — gen 11 `395bc7b1` → gen 12 `a1bbdc1`, trái `PROTOCOL:185` |
| `L-J` | `unverifiable-spec-source` | **P1** | lease gen 11 + 12 | chưa — spec chỉ neo TÊN NHÁNH, không neo commit OID |
| `L-K` | `unanchored-authority-parameter` | P2 | lease gen 11 | chưa — hạn 12h chỉ có trong văn của người ghi |
| `L-L` | `false-measurement-anchor` | P2 | lease gen 12 | **CÓ** — trích `lease_publish.py:1847-1848` là `policy_T`; chỗ thật **1947-1948** |
| `L-M` | `revision-trigger-understatement` | P2 | lease gen 12 | **CÓ** — §3.2 có **sáu** trường, lease kể **bốn** |

### #586 · #597 — CHƯA CÓ

Cross-review đang chạy lúc soạn (#586 từ `15:44Z` trên `5497cf5`; #597 từ `15:58Z` trên `ffd11a7`).
**Đóng băng spec này chỉ sau khi cả hai trả kết quả.** Vắng mặt ở đây là *"chưa chạy xong"*, **không
phải** *"sạch"* — đúng lớp mà chính packet này tồn tại để dạy.

## `dieu_kien_dung`

- `S1` — cần đường dẫn ngoài `write_set`. DỪNG, xin revision.
- `S2` — tổng dòng thêm của hai tệp **sản phẩm**, đo từ `immutable_acceptance_baseline` tới head
  cuối, vượt trần ADR-0044 cho `sensitive`. KHÔNG cộng hai khoảng.
- `S3` — muốn đụng `docs/PROTOCOL_DA_PHIEN.md` hay `.claude/hooks/**`.
- `S4` — muốn vá `packet_loop.py` / `doctrine-scan`: nợ riêng **#583**.
- `S5` — muốn sửa `VERDICT.md` hoặc biên nhận của một lượt **đã giao**.
- `S6` — muốn đổi định nghĩa `P0`–`P3` hoặc đổi **slug** của một lớp cũ (slug là khoá đếm).
- `S7` — hợp nhất làm MẤT một mục của master hoặc của #529 mà không có chỗ đặt lại.
- `S8` **đã rút từ r7** — số để trống có chủ đích, KHÔNG đánh số lại.
- `S12'` — chuẩn bị đóng băng mà phép quét *"còn sót luật cũ"* chỉ khớp theo TÊN.
- `S13` (từ r12) — vá một lớp **chỉ để lấy approve** thay vì vì nó sai.
- `S14` (từ r12, **giữ và mở rộng**) — ký dựa trên bản tóm tắt của executor là `KHÔNG ĐO ĐƯỢC`.
  **r13 thêm:** một `approve` **không kèm phép đo tái hiện được** cho từng lớp cũng là
  `KHÔNG ĐO ĐƯỢC` — kể cả khi nó đến từ cross-review.
- `S15` (**mới ở r13**) — **đóng băng spec khi tập lớp chưa đủ.** Nếu một lượt cross-review đang
  chạy mà chưa trả kết quả, DỪNG; đo `sha256` lúc ấy là neo lease vào một bản đồ thiếu chỗ.
- `S16` (**mới ở r13**) — **dời `immutable_acceptance_baseline`.** `PROTOCOL:185` cấm; r12 đã vi
  phạm đúng chỗ này (`L-I`). Baseline của packet giữ `395bc7b1be6c275d8de697f8d8541bb36a290c9e`.

## `chua_do_duoc` — khai thẳng

- Tập lớp **chưa đủ**: thiếu #586 và #597.
- **Danh tính người ký KHÔNG đo được** — `author_association` không tách chủ kho khỏi phiên chạy
  bằng token chủ kho. Nợ **#566** (họ hàng **#338**). r13 **không** trích trường ấy làm bằng chứng.
- `cross_approved` của r13 sẽ do **connector codex** cấp. Nó **không** phải người, và lượt vừa rồi
  cho thấy nó mạnh ở chỗ chữ ký người yếu — **nhưng chưa đo được chiều ngược lại**: lớp nào người
  thấy mà nó không. Đừng đọc r13 thành *"máy hơn người"*.
