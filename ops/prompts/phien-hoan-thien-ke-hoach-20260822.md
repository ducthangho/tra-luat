# Giao việc — PHIÊN HOÀN THIỆN KẾ HOẠCH + ĐỒNG BỘ PROTOCOL (22-08-2026)

**Người giao:** `ducthangho`, in-session 22-08-2026 (*"tập trung vào hoàn thiện kế hoạch cho tôi"*).
**Mục đích:** làm kế hoạch đủ tốt để **phân việc cho agent**. **KHÔNG thi công packet nào.**

> **Đây KHÔNG phải lease.** `docs/PROTOCOL_DA_PHIEN.md` §7: prompt/handoff không mang thẩm quyền.
> Việc của phiên là **TÀI LIỆU + ĐỀ XUẤT**, không sửa mã, không tự cấp lease.

Mở phiên: đọc `CLAUDE.md` + `docs/PROTOCOL_DA_PHIEN.md`, rồi
`python3 .claude/dev/launcher.py doctor`.

## Nền đã đo — 22-08-2026, master `a5bfe07`. KIỂM LẠI, ĐỪNG TIN

| # | phát hiện | lệnh tái lập |
|---|---|---|
| 1 | Protocol gần như không đổi từ 20-08: **1** commit `6f49692`, **+22/-15**, PROTO-01-FIX về máy trạng thái — không liên quan quản trị | `git log --oneline --since=2026-08-20 origin/master -- docs/PROTOCOL_DA_PHIEN.md` |
| 2 | **Protocol KHÔNG trỏ tới ADR nào trong ba ADR quản trị mới**: `0043` ⇒ 0 · `0044` ⇒ 0 · `0045` ⇒ 0 | `grep -c 0043 docs/PROTOCOL_DA_PHIEN.md` |
| 3 | `ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md` — thứ `CLAUDE.md:523` gọi là *"bản đồ packet"* — **0** commit từ 19-08, nhắc `PLAT-X*`/`AG-*`/`SLICE-*` **0** lần | `grep -c 'PLAT-X' ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md` |
| 4 | Cổng `ops/lease_publish.py` cưỡng chế **0/8** chốt của mục D; nó chỉ có `prompt_path`+`prompt_sha256_required` (RC_NEO=6) và 5 trường `BAT_BUOC` | `grep -cE 'review_class\|spec_sha256\|assurance_target\|cross_provider\|leased_at_utc' ops/lease_publish.py` |
| 5 | Bệnh *"khai mà cổng không đọc"*. `review_class:` **10/49**. Với spec thì là **HAI khoá khác nhau**: `spec_sha256:` **5/49** và `spec_sha256_required:` **6/49** — cổng đọc **0** dòng cả ba. **Con số 11 ở bản đầu là đếm CHUỖI CON, gộp nhầm hai lược đồ** (cross-review lượt 4 bắt) | `grep -c '^spec_sha256:' ops/leases/*.yaml \| grep -v ':0' \| wc -l` — đếm ĐÚNG KHOÁ, và làm y thế cho `^spec_sha256_required:` |
| 6 | Kế hoạch đang chạy thật là `ops/THAM_DINH_KE_HOACH_20260821.md` §"BẢN THAY THẾ cho V0–V6": **A xong · B xong · C một phần · D 0/8 · E chưa · F chưa** | đọc §"Kế hoạch thi hành" |

**Mâu thuẫn gốc — VIẾT LẠI 22-08-2026 sau khi cross-review lượt 4 bác tiền đề bản đầu (P2 trên
PR #230).** Bản đầu viết *"agent đọc protocol… **không thấy** canon 2 vòng ở đâu"*. **Sai, đo được:**

```
docs/PROTOCOL_DA_PHIEN.md:543  "Trần 2 lượt Codex/PR, các bộ đếm §12, và mức assurance
                                theo class không đổi."
docs/PROTOCOL_DA_PHIEN.md:561  "Mỗi PR được dùng tối đa hai lượt Codex: một review đầu và
                                một rereview sau khi Executor gom bản vá. Lượt hai chưa
                                approve phải chuyển sang checkpoint…"
```

Protocol **KHÔNG im lặng**. Chỗ hở thật hẹp hơn nhiều, và cũng khó hơn:

1. **Thiếu quy kết ADR** — protocol trỏ `0043`/`0044`/`0045` **0 lần**, nên không ai biết luật ở
   `:561` đã được nâng thành canon bằng ADR nào, hay ADR ấy có sửa gì nó không.
2. **HAI TRỤC có thể đang bị lẫn.** `:561` khai trần theo **LƯỢT GỌI CODEX** (gắn với một provider).
   ADR-0043 khai trần theo **VÒNG REVIEW**, cố ý **provider-agnostic**, và nói thẳng *"trục VÒNG tách
   khỏi trục LỜI GỌI và trục ATTEMPT; các trần độc lập và trần chạm trước thắng."* Hai câu này
   **không đồng nghĩa**: một reviewer `claude` không tiêu lượt Codex nào nhưng vẫn tiêu một vòng.
   Việc A phải phân định điều đó, **không** được giả định chúng là một.

**Vì sao ghi cả cái sai:** tiền đề *"protocol im lặng"* dẫn tới bản vá *"chép luật vào protocol"* —
và làm thế là **dựng canon thứ hai** cạnh `:561`, đúng thứ việc A sinh ra để chống. Một tiền đề sai
đẻ ra một bản vá làm hỏng thêm.

Ba ADR hiện tới tay agent qua **lease** và `.claude/skills/soan-spec/SKILL.md` — đường vòng, không
qua nguồn.

## Việc, theo thứ tự

**A — Agent cần đọc GÌ để làm đúng?** Câu trả lời hiện tại là *"protocol + 3 ADR + 4 kế hoạch +
skill"*, và protocol không trỏ 3 ADR. Đề xuất cách chữa (protocol trỏ ADR · gộp ADR vào protocol ·
một § *"quy tắc đang hiệu lực"*). **HỎI người giữ kho trước khi sửa** — đây là quyết định kiến trúc
tài liệu, không phải dọn dẹp.

**B — Bản đồ packet đúng thực tại.** Mọi họ đang chạy: `PLAT-M*` · `PLAT-X4…X8` · `AG-T0-*` ·
`SLICE-*` · `LEASE-DANG` (#227) · `W0/W1/W2`. Mỗi dòng: Issue · trạng thái đo bằng **HIỆN VẬT trên
master** · write set · thứ tự · chặn ai.
**Kiểm PR #229 TRƯỚC** — nó đang dựng `ops/HANG_DOI_PACKET.md` cho THỨ TỰ packet; đừng dựng chỗ thứ
hai nói cùng chuyện.

**C — Mục D tách thành mấy packet?** Đã tách: `review_class` → `PLAT-X8` (#225, spec bản **3i**
`ca852d95ab59…`, chưa lease — va chạm write set với lease sống của `#238`) · cross-provider theo họ model → `PLAT-X7` (#220, proposed) · phần còn lại
→ *"mục D"*, chưa mở Issue. Cắt phần còn lại cho vừa trần ADR-0044 (`sensitive` ≤3 tệp / ≤300 dòng
thêm) rồi trình người giữ kho.

## Ràng buộc — không thương lượng

- **ĐỌC ĐƯỢC KẾ HOẠCH KHÔNG PHẢI ĐƯỢC GIAO VIỆC.** Không tự cấp lease, không thi công.
- Mọi con số kèm **ĐƠN VỊ** và **lệnh tái lập**. "Đo được" mà không chạy lại được thì đừng viết.
- Trạng thái packet đo bằng **hiện vật trên master**, KHÔNG bằng trạng thái Issue — đo 22-08: cả bốn
  Issue #206 #215 #225 #227 đều `open` trong khi hai packet đầu **đã land**.
- Quét lease/verdict phải quét **mọi ref `refs/remotes/origin/ops/*`**, không chỉ master. Xem bài học
  `SỔ LEASE KHÔNG NẰM MỘT CHỖ` (`CLAUDE.md`) và nợ mục **12** (`ops/NO_KY_THUAT.md`).
- **Land tài liệu kế hoạch TRƯỚC, rồi mới thi hành từ nó.** Bài học đắt nhất của đợt 21-08: bản hợp
  nhất tốn ~3 giờ máy của ba bên độc lập rồi **bị thực tế vượt qua trong vài giờ** vì nó nằm trên một
  PR chưa merge — phiên kia không có cách nào đọc được nó.
- Đề xuất dạng *"ghi thêm vào CLAUDE.md / thêm chốt vào SKILL"* phải kèm một ca `rXX_` chạy được —
  không thì nó là chỗ các ca đi chết (§5 điều khoản khoá của bản hợp nhất).

## Đang treo — ĐỪNG ĐỤNG

| thứ | trạng thái |
|---|---|
| ~~**PR #230**~~ | **ĐÃ MERGE** 22-08 (master `3f64167`). Dòng này giữ làm lịch sử |
| **PLAT-X8** (#225) | chờ **`#238`** land (KHÔNG phải `#227` — nó land 05:16Z rồi bị revert qua PR #237); **mười ba** chỗ phải sửa, ghi trong hộp ⛔ đầu `ops/specs/plat-x8.md` bản **`3i`** (`ca852d95ab59…`). **Chưa cấp lease được**: **BA** lease của `#238` giữ đúng cả hai tệp `write_set` của `PLAT-X8` tới `2026-08-23T15:00:00Z`. Khi cấp: packet là `sensitive` + executor `codex` ⇒ **ngoại lệ `ADR-0045`**, lease phải khai rõ — và **chưa cổng nào kiểm việc ấy** (`§20` xếp `ADR-0045` là `0 cổng`), nên phải tự kiểm bằng tay |
| **#227** | **land rồi REVERT**: PR #234 merge 05:16:40Z ⇒ master ĐỎ Windows `59/68` ⇒ PR #237 hoàn nguyên ba tệp mã, giữ hồ sơ. Land lại là packet **`#238`** |

Bắt đầu bằng **đo lại** bảng "Nền đã đo". Cái nào không tái lập được thì **nói ra**, đừng lặng lẽ dùng.
