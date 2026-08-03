# ADR-0001 — Chỉ canonical đánh version; nhánh song song giao nộp bundle không-version

- **Trạng thái:** Superseded by ADR-0017 (2026-08-03)
- **Bối cảnh:** Skill được phát triển đồng thời ở nhiều phiên (Code local, Cowork, Chat, Codex). Đã xảy ra
  3 lần nhánh song song tự đánh số trùng canonical (bundle "1.33.44/45", Codex "1.33.49", Pha B "1.33.54"
  — trùng số nhưng KHÁC nội dung) và 1 lần tự publish thẳng lên Drive Package (1.33.46) đè kênh phát hành,
  tạo drift 12 version giữa LIVE và canonical. Luật "không tự đánh số" từng chỉ nằm trong memory phiên —
  không có gì cưỡng chế.
- **Quyết định:**
  1. Chỉ cây canonical (`D:\Quốc hội\tra-luat`, remote ducthangho/tra-luat) được tăng `VERSION` và
     `drive-push` lên Package.
  2. Nhánh song song xuất sản phẩm qua `tl bundle-export`: zip giữ nguyên VERSION fork-point + sinh
     `BUNDLE_META.json` (commit gốc, danh sách file đổi, test thêm).
  3. `drive-push` phát hiện `BUNDLE_META.json` trong cây → TỪ CHỐI push (trừ `--force` tường minh).
  4. Doctrine ghi ở SKILL.md để agent mọi phiên tuân theo; canonical merge bundle rồi mới đánh số
     (một version có thể gộp nhiều bundle).
- **Phương án đã loại:**
  - *Chỉ doctrine, không code* — đã chứng minh không đủ (các phiên vi phạm đều có doctrine trong context).
  - *Khoá version qua sổ trung tâm (Sheet/API)* — thêm phụ thuộc mạng cho thao tác offline, quá nặng.
- **Hệ quả:** Nhánh song song mất khả năng "ship thẳng" (chấp nhận: mọi thay đổi phải qua canonical merge
  + gate). Chi phí merge dồn về canonical — đổi lấy một nguồn sự thật duy nhất về version/LIVE.
  Guard chỉ chặn đường chuẩn (`drive-push`); ai cố tình upload tay ngoài CLI vẫn vượt được — chấp nhận,
  vì mục tiêu là chống NHẦM chứ không chống phá hoại.
