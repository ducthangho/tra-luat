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
| 5 | Bệnh *"khai mà cổng không đọc"* nay có **HAI** field: `review_class` **10/49** lease khai · `spec_sha256` **11/49** khai — cổng đọc **0** dòng cả hai | `grep -l '^review_class' ops/leases/*.yaml \| wc -l` |
| 6 | Kế hoạch đang chạy thật là `ops/THAM_DINH_KE_HOACH_20260821.md` §"BẢN THAY THẾ cho V0–V6": **A xong · B xong · C một phần · D 0/8 · E chưa · F chưa** | đọc §"Kế hoạch thi hành" |

**Mâu thuẫn gốc:** `CLAUDE.md:513` khai protocol là *"nguồn quy tắc duy nhất"*, nhưng ba luật người
giữ kho vừa duyệt sống **ngoài** nó và nó **không trỏ tới**. Agent đọc protocol thấy
`max_attempts_per_packet: 3` (dòng 73) và **không thấy** canon 2 vòng của ADR-0043 ở đâu. Ba ADR ấy
hiện chỉ tới tay agent qua **lease** và qua `.claude/skills/soan-spec/SKILL.md` — đường vòng, không
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

**C — Mục D tách thành mấy packet?** Đã tách: `review_class` → `PLAT-X8` (#225, spec bản 3b
`308d0cf4…`, chưa lease) · cross-provider theo họ model → `PLAT-X7` (#220, proposed) · phần còn lại
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
| **PR #230** (`claude/opus-5-plan-steps-y5r6ci`, 7 tệp) | con trỏ chết + hộp cảnh báo đặc tả PLAT-X8 + nợ mục 12. Chờ người giữ kho merge |
| **PLAT-X8** (#225) | chờ #227 land rồi ra đặc tả **bản 4**; sáu chỗ phải sửa ghi sẵn trong hộp cảnh báo đầu `ops/specs/plat-x8.md` |
| **#227** (`codex/lease-dang-exec-1`) | chưa có PR, chưa land |

Bắt đầu bằng **đo lại** bảng "Nền đã đo". Cái nào không tái lập được thì **nói ra**, đừng lặng lẽ dùng.
