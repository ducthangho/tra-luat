# wp744 — Đính chính P2 của PR #724, spec r3

Đặc tả đóng băng. Sửa tệp này là đổi băm; muốn đổi thì soạn r4. Soạn bởi phiên Claude Code
`session_01FBUBzbedsJaUtQvX4vEYDE` ngày 19-10-2026. r3 **thay** r2 (`ops/specs/wp744-dinh-chinh-p2-r2.md` trên nhánh
`ops/wp744-r2-g2-lease`, sha256 `9391705db12b820af9eb59fe05cc2008eebde648964b8a6be8e063ed957adba8`) ở ba điểm: write set,
tuyến PR, base. Mọi điều khác của r2 về nội dung bốn finding còn lại giữ nguyên.

## Định danh

- `packet_id`: `wp744`; `packet_issue`: #744; `revision`: 3; `generation`: 3.
- Executor: `claude` (Claude Code, phiên trên, Linux cloud). Reviewer: Codex CLI độc lập qua `.claude/dev/launcher.py run`,
  `model_family: openai` ⇒ `cross_approved` khi verdict approve neo exact head.
- `risk`/`review_class`: sensitive (giữ như r2: nội dung canary/stage chạm ranh giới credential).
- Nguồn nội dung: PR #747 head `fffd14f4546f5eb44b3fe1138bc49c9703c7ed97` (g2, Antigravity), đã có verdict nội dung PASS
  và identity `cross_approved` trên đúng head ấy (#747 issuecomment-6134280972, -6134358607).

## vi_sao_co_r3 (đo được 19-10-2026, không suy)

1. `ops/specs/wp728-do-linux-doc-lap-wp710-r2.md` ĐÃ có trên master, blob `0f05c51d…`, do PR #755 (15-10) — một r2 khác,
   đã qua nhiều lượt cross-review và đã được lease neo băm. Bản trong #747 cùng tên, blob `0f7c8d19…`. Merge #747 là ghi đè
   một spec đóng băng ⇒ **loại wp728 khỏi write set**. Ba finding #4242170329/331/336 phía wp728 do r2 của #755 phủ.
2. Ba spec `wp725/726/727-…-r2.md` CHƯA có trên master; finding #4242170323 và #4242170327 (canary/stage, wp726) không xuất
   hiện ở tệp nào trên master. Giữ ba tệp này.
3. Base cũ `mission/744/integration` = `8aebf14`, tụt sau master 585 commit. Mọi mỏ neo mà ba tệp trích (blob/sha256 r1,
   blob `scripts/nlm-auto-refresh.sh` `03f726fb…`, fragment `scripts/test_fragments/wp726_script_nlm_canary.py`
   `19ace16d…`) đo lại trên master `5618020a`: **khớp từng giá trị**; hai tệp mã không đổi từ `8aebf14`.

## quyet_dinh

- **Q1 — write set (3 tệp chính xác):**
  1. `ops/specs/wp725-nlm-huong-dan-tai-lieu-r2.md`
  2. `ops/specs/wp726-nlm-script-phan-quyet-canary-r2.md`
  3. `ops/specs/wp727-nlm-refresh-va-goi-y-tl-gws-r2.md`
- **Q2 — tuyến:** nhánh `agent/wp744-g3-claude` từ master `5618020a`, PR đích **`master`**, theo quyết định chủ kho trong phiên
  ("Rút gọn + đổi đích master"). Đây là **sai lệch có ghi** so với Protocol §5 (Packet PR vào `mission/<issue>/integration`),
  cùng loại tiền lệ #755 (wp728 r2: spec-only `ops/**` → PR master, khai rõ). Lý do: packet chỉ thêm tài liệu dưới `ops/specs/`,
  không mã sản phẩm; nhánh integration tụt 585 commit.
- **Q3 — nội dung:** lấy nguyên văn ba tệp từ `fffd14f`, CHỈ sửa câu "quy tắc tương lai" cho khớp sự thật: Protocol §5 vẫn là
  mặc định, nhưng đã có ngoại lệ có ghi do chủ kho quyết (#755, chính #744 r3). Không đổi ma trận finding, mỏ neo, hay phạm vi.
- **Q4 — kích thước:** ≤ 3 tệp, ≤ 80 dòng thêm.
- **Q5 — review:** tối đa 3 lời gọi Codex; push MỘT LẦN khi đủ điều kiện merge (chỉ thị chủ kho).
- **Q6 — sau merge:** đóng PR #747 là thay thế (nêu lý do wp728), cập nhật #744.

## nghiem_thu

| Mục | Tiêu chí | Phép đo làm ĐỎ |
|---|---|---|
| write set | diff so master đúng 3 tệp mới, không tệp nào khác | thêm/sửa tệp ngoài Q1 |
| nội dung | so với `fffd14f`, chỉ khác các câu về quy tắc tuyến tương lai | đổi ma trận finding, mỏ neo, phạm vi |
| mỏ neo | mọi blob/sha256/comment-id trích trong ba tệp phân giải đúng trên master | một mỏ neo lệch |
| không đè | `ops/specs/wp728-do-linux-doc-lap-wp710-r2.md` trên master không đổi | blob khác `0f05c51d…` |
| gate | `git diff --check` sạch; `doctrine-scan` rc 0; CI trên exact head xanh | một mục đỏ |
| review | Codex approve trên exact head, không P0/P1/P2 | finding mở |

## ngoai_pham_vi

Runtime canary/stage của wp726 và audit Linux wp728 vẫn OPEN, thuộc Packet riêng. Không sửa r1, mã, lease khác, CI, manifest.
