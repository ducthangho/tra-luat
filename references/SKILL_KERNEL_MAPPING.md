# SKILL_KERNEL_MAPPING — Bảng đối chiếu Pha F (mục nào đi đâu) — ĐÃ THỰC THI v1.34.0 (user chọn (a) 41.8KB, 2026-07-09); giữ làm hồ sơ

| # | Section SKILL.md hiện tại (dòng) | KB | Đích | Cách xử lý |
|---|---|---|---|---|
| 1 | Frontmatter + header (1-26) | 0.7 | KERNEL | nguyên văn (frontmatter Cowork đọc) |
| 2 | DETERMINISTIC WORKFLOW GATES + PHÁT HÀNH & NHÁNH (27-50) | 3.6 | KERNEL | nguyên văn |
| 3 | §0 NGUYÊN TẮC BẤT BIẾN (51-89) | 12.1 | KERNEL | nguyên văn — linh hồn skill |
| 4 | §1 KHỞI ĐỘNG (90-155) | 7.2 | KERNEL | nguyên văn — BƯỚC 0 curl sống-còn |
| 5 | §1 chú giải dài (156-185) | 4.4 | RUNBOOK §A (đã có sẵn nội dung tương đương) | thay bằng 2 dòng pointer |
| 6 | §2 CỔNG VẬN HÀNH (186-204) | 8.0 | KERNEL | nguyên văn |
| 7 | §3 KẾT PHIÊN + mảnh profile (205-217) | 0.7 | KERNEL | nguyên văn |
| 8 | §4 CLI 27KB (218-317) | 27.0 | references/COMMANDS.md | nguyên văn sang file mới; kernel giữ bảng nhóm ~2KB + pointer |
| 9 | §5-8 cấu trúc/tra cứu/script-map/webapp (318-342) | 3.2 | KERNEL | nguyên văn |
| 10 | §9 PHỤ THUỘC (343-466) | 13.3 | references/DEPENDENCIES.md | nguyên văn sang file mới; kernel giữ 2 dòng đầu + pointer |
| 11 | v1.17.26 gate (467-473) | 0.6 | KERNEL | nguyên văn (đang hiệu lực) |
| 12 | STAGE4_BRIDGE + Stage5 harness (474-568) | 7.8 | Doctrine rút ~1.5KB trong kernel; chi tiết đã sống ở workflow cards + GATES | viết lại nén |
| — | (mới) LỆNH KIỂM CUỐI + DANH MỤC REFERENCES | +1.5 | KERNEL | viết mới |

**Kích thước draft: 41.8KB** — vượt đích 20-35KB (~20%) vì GIỮ NGUYÊN VĂN trọn §0 Bất biến (12.1KB) +
§1 Khởi động (7.2KB — khối BƯỚC 0 curl sống-còn) + §2 Cổng vận hành (8KB). Lựa chọn khi duyệt:
(a) CHẤP NHẬN 41.8KB — ưu tiên an toàn doctrine (khuyến nghị); (b) nén thêm §1 phần sau BƯỚC 0 + §2 xuống
~5KB mỗi mục → ~34KB, đổi lấy việc phải viết-lại-lời các đoạn mệnh lệnh (rủi ro drift ngữ nghĩa).

**Kết quả draft:** xem `references/SKILL_KERNEL_DRAFT.md`. **CHANGELOG (458KB):** khi duyệt sẽ cắt còn
10 version gần nhất, phần cũ chuyển `references/changelog_archive/CHANGELOG-2026H1.md` (nguyên văn).

**Quy trình khi bạn DUYỆT:** (1) SKILL_KERNEL_DRAFT.md → SKILL.md (bump v1.34.0); (2) cắt CHANGELOG + archive;
(3) full gate + zip + deploy + curl verify; (4) BẠN re-import Capabilities (bắt buộc — đổi lớn doctrine);
(5) workflow-audit thêm check kernel-size ≤ 40KB + links references tồn tại (chống phình trở lại).
