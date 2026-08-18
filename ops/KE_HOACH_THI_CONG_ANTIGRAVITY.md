# Kế Hoạch Thi Công & Điều Phối Antigravity — tra-luat

Tài liệu lưu trữ kế hoạch thi công, phân tầng rủi ro và lộ trình chuyển tiếp cho Google Antigravity trong kho mã nguồn `tra-luat` khi Claude Code và Codex cạn hạn mức (quota).

---

## 1. Bối Cảnh & Nguyên Tắc Điều Hành

- **Tình trạng:** Claude Code và OpenAI Codex tạm thời hết quota API.
- **Quyết định:** Sử dụng Antigravity làm **Executor** và **Reviewer dự phòng** theo cơ chế `same_provider_approved` (quy định tại `ADR-0024` và `AGENTS.md`).
- **Phân loại nhiệm vụ:**
  - Tập trung giải quyết các **Packet Nhóm A (Routine)** và **Nhóm B (Systemic-Low)** để không làm gián đoạn tiến độ hoàn thiện repository.
  - Trì hoãn các thay đổi nhạy cảm (Nhóm C: state machine, lock CAS, security authority, LIVE deployment) cho tới khi có cross-review hoặc human audit.

---

## 2. Danh Mục Các Packet Triển Khai

| Packet | ID | Tên Packet / Nhiệm vụ | Phạm vi Write-Set | Phân tầng Rủi ro | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **Packet 1** | AG-T0-04 | Version Generator Fail-Closed | `scripts/gen_instructions.py` | Nhóm A (Routine) | **MERGED (PR #163)** |
| **Packet 2** | AG-T0-02 | Clean Cross-Review Adapter & Root AGENTS.md | `.claude/skills/cross-review/SKILL.md`, `AGENTS.md` | Nhóm A (Routine) | **MERGED (PR #164)** |
| **Packet 3** | AG-T0-01 | Fix Windows Subprocess Encoding & Add AGY to Launcher | `.claude/dev/launcher.py` | Nhóm B (Systemic-Low) | **SẴN SÀNG** |
| **Packet 4** | AG-T0-03 | Argparse Parser-Tree Coverage Report | `scripts/tl_core/command_registry.py` | Nhóm B (Systemic-Low) | **DỰ KIẾN** |
| **Packet 5** | AG-T0-05 | Command Spec Sync & Golden Surface Hardening | `references/golden/parser_surface.json` | Nhóm A (Routine) | **DỰ KIẾN** |

---

## 3. Quy Trình Thi Công Chuẩn Mỗi Packet

Mọi Packet do Antigravity thực hiện phải tuân thủ nghiêm ngặt chu trình 5 bước:

1. **Branching:** Tạo branch `agent/<packet-id>-<slug>` từ `origin/master`.
2. **Implementation & Unit Test:** Viết mã tối thiểu, đảm bảo fail-closed, chạy selftest nội bộ đạt 100%.
3. **Independent Review Subagent:** Khởi tạo Reviewer Subagent trong phiên riêng để soi diff và chạy độc lập test suite, xuất Verdict `ag_review_verdict.v1`.
4. **Publishing PR & Review Comment:** Mở PR trên GitHub (`gh pr create`) và đăng biên bản Reviewer Verdict lên comment PR.
5. **CI Gate & Land:** Chờ GitHub Actions CI `gate` báo xanh 100% trước khi merge vào `master`.

---

## 4. Quản Lý Nợ Review (Review Debt)

* Các Packet Nhóm A (Routine) mang **0 nợ review**.
* Các Packet Nhóm B (Systemic-Low) được đánh dấu cần **1 lượt re-audit bổ sung** (bởi Claude Code hoặc Codex) khi quota được khôi phục.
