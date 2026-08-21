# ADR-0044 — Ngưỡng kích thước packet, neo từ số đo của chính kho

- **Trạng thái:** Accepted (2026-08-21, thẩm định ba bên; chủ kho phê duyệt Q6)

Một packet `sensitive` chạm authority: **≤ 3 tệp và ≤ 300 dòng thêm**. Một packet thường:
**≤ 6 tệp và ≤ 1.000 dòng thêm cộng xoá** theo `git diff --numstat`. Vượt một trong hai ngưỡng thì
dừng TRƯỚC review để revision thiết kế, hoặc khai lý do trong spec; không tự mở hai PR chồng lấn.

Ngưỡng neo từ dữ liệu của chính kho chứ không từ cảm tính "packet nhỏ": `PLAT-M4` = 2 tệp, +351/−25 ⇒
**một vòng, một finding**; `PLAT-X4` = 4 tệp, +721/−159 ⇒ **ba vòng, tám finding**. Gói gộp `PLAT-X4`+`PLAT-X5`
đo từ merge-base thật `909d3e17..e071e0aa` = 5 tệp, +923/−210 = **1.133 dòng**, tức lớn hơn cái đã chứng minh
là quá lớn; kể cả sau khi bỏ `t34` (95 dòng) vẫn ≈1.038. Chính phép đo này bác phương án gộp một packet mà
hai trong ba bên thẩm định đã bỏ phiếu, và là lý do chọn tách hai slice.

Giao write set không cấm hai packet nối tiếp, nhưng nối tiếp chỉ hợp lệ khi slice sau mọc trên
`mission/<issue>/integration` **đã nhận** slice trước (`docs/PROTOCOL_DA_PHIEN.md:288-291`), không mọc trên một
PR chưa merge. Chuỗi `#203`→`#206` của ngày 20-08 sinh ra từ đúng chỗ này: hai packet trên cùng seam mà bỏ
integration branch — đo được là ngày ấy không có integration branch nào cho lane PLAT và 7/8 lease khai
`target_branch_neu_land: master`.

Cưỡng chế: cổng write-set và `numstat` chạy TRƯỚC review; `base_sha` không phải tổ tiên nhánh mặc định thì
lease phải khai `xep_tang{tren_pr, thu_tu_land, ke_hoach_rebase}`, thiếu thì thoát khác 0. Fixture đỏ có sẵn:
lease `plat-x5-exec-1r2` neo base `a09aae62` vốn không thuộc master.

Quyết định này mở write set `ops/lease_publish.py` cho gói cưỡng chế kế tiếp (chủ kho phê duyệt Q4). Nói thẳng
vì sao cần nói: `ops/THAM_DINH_CHUNG_CLAUDE_CODEX_KE_HOACH.md:96` từng CẤM mở tệp ấy cho `W0-R2`. Đây là một
duyệt MỚI cho một mục đích KHÁC, có ghi; không phải lờ đi lệnh cấm cũ. Gói ấy phải làm SAU hai slice vì write
set giao nhau.
