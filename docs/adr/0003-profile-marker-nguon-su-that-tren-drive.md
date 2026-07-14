# ADR-0003 — Profile marker trên Drive là nguồn sự thật về tồn tại/định danh profile; config là cache

- **Trạng thái:** Accepted (2026-07-10, phiên grilling cải tiến profile)
- **Bối cảnh:** Doctrine cũ: "config local là nguồn sự thật duy nhất" về profile; `_PROFILES_INDEX` và
  `profile-list --discover` chỉ là bản chiếu/heuristic (đoán profile qua sự hiện diện registry Sheet +
  manifest JSON trong folder hoặc `_meta`). Hệ quả thực tế: agent ở phiên/máy khác KHÔNG liệt kê được
  profile trong `Van_ban_thuong` (config không được đồng bộ); folder legacy không mang metadata nào
  (văn phong, quan hệ profile, mô tả phạm vi) để sinh Instruction; thêm profile ở một máy đòi re-stage
  config thủ công ở mọi nơi khác.
- **Quyết định:**
  1. Mỗi profile có **marker** `tra_luat_profile.json` trong `_meta` của folder profile (tên theo
     convention `tra_luat_*` sẵn có để discover khỏi đoán) — schema cố định
     (`schema`, định danh: profile/rootFolderId/notebookId/registryDocId/manifestId/categories/
     manifestScope; metadata mô tả chuẩn: `description`, `style`, `relations`, `created_at`/`updated_at`).
  2. **Marker = nguồn sự thật về TỒN TẠI + ĐỊNH DANH + metadata mô tả** của profile.
     **Config = nguồn sự thật về LỰA CHỌN runtime** (defaultProfile, token, webappUrl) + bản materialize
     cây profile để chạy offline.
  3. Đồng bộ **MỘT CHIỀU** qua `profile-sync` (marker Drive → config). Ghi marker CHỈ qua lệnh tl
     (create/promote/adopt/set/rename/delete — journaled + readback); cấm sync hai chiều, cấm sửa tay.
  4. Backfill một lần cho profile hiện hữu (config → sinh marker); `profile-doctor` kiểm drift
     marker↔config↔index; `relations` chỉ mô tả (đưa vào Instruction), KHÔNG mở scope đọc runtime.
- **Phương án đã loại:**
  - *Giữ config là nguồn sự thật, marker chỉ là bản chiếu* — không giải quyết gốc: máy khác thêm profile
    thì config nơi khác vẫn mù, marker-lệch-config cần trọng tài mà bản chiếu không làm trọng tài được.
  - *Cải thiện heuristic discover, không marker* — Drive vẫn không tự mô tả, không chỗ chứa metadata mới.
  - *Sync hai chiều* — hai nguồn sự thật cùng ghi = lớp bug reconcile kinh điển; bác ngay từ đầu.
- **Hệ quả:** Thêm một artifact per-profile phải giữ đúng (doctor gánh); lệnh mutation profile phải ghi
  2 nơi (marker + config) trong một giao dịch journaled. Đổi lại: mọi env liệt kê/khám phá profile không
  cần heuristic, metadata (văn phong/quan hệ) sống cùng profile trên Drive, config trở thành cache có thể
  dựng lại (`profile-sync`) thay vì tài sản phải re-stage tay. Doctrine "config là nguồn sự thật duy nhất"
  trong SKILL.md/COMMANDS.md phải sửa lời theo ADR này (kernel-diff cần user duyệt + re-import).
