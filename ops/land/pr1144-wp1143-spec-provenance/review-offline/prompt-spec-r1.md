# Review offline ĐẶC TẢ packet — lượt 1

Bạn là reviewer độc lập. Thư mục làm việc là một clone của kho `ducthangho/tra-luat` ở commit
`caa22e5903a5639c20c81320a0baf8c47b8f6f36`. Thứ định danh tệp là BĂM, không phải tên nhánh.
Đối tượng review: `ops/specs/CI-DUONG-NHANH-BO-DOT-BIEN-r1.md`
(sha256 `f3b7eb71012fe73c6882f37f51a30423e203cc06be61adc7f2194d75ab03641a`).
Bối cảnh: `ops/specs/CI-LAN-LUU-TRU-r1.md` (packet tiền nhiệm #1113, tiêu chí A12),
`ops/ci_duong_nhanh.py`, `ops/ci_duong_nhanh_test.py`, `.github/workflows/ci.yml`,
`.claude/dev/ci_dang_ky_test.py`, `docs/PROTOCOL_DA_PHIEN.md`, `.claude/skills/soan-spec/SKILL.md`
(luật L1–L6). Nguồn số canary: `git show origin/claude/ghi-so-land-1113:ops/land/pr1128-wp1113-provenance/readback-jobs-41371625809-canary-a12.json`
và `...:ops/land/pr1128-wp1113-land-evidence.yaml`. Các ref `origin/*` đã có cục bộ; KHÔNG có mạng.

Sandbox chỉ đọc: được chạy lệnh đọc (`git show`, `grep`, `python -c` không ghi tệp), không sửa gì.
Đừng chạy cả bộ `ops/ci_duong_nhanh_test.py` (dài, cần ghi tệp tạm). Hướng thử nào cần dựng nội dung
nhạy cảm thì mô tả bằng lời.

Soi theo LỚP lỗi, mỗi lớp ghi rõ đã kiểm gì (kể cả khi không thấy lỗi):

1. **Số liệu (L1/L5).** Đo lại mọi con số kiểm được từ kho: 113 ca, 419 đột biến, 5 mẫu rc + 3 đột biến tự kiểm,
   1159 s / 966 / 636 / 303 / 193 / 27 s từ JSON canary. Kiểm SỐ HẠNG, không chỉ quan hệ.
2. **Write set (L2).** Mọi mục §2 có thực hiện được chỉ trong ba tệp §3 không? Đặc biệt: bảng ghim
   `KHUNG_BUOC`, `RUN_BUOC_PACKET`, `TAP_CHO_PHEP`, `BUOC_HARNESS`, các ca `y*`, `BAM_GATE_*` trong
   `.claude/dev/ci_dang_ky_test.py`, `ops/cong_cu_test.py`, `ops/lease_publish_test.py` — thêm khối `env:`
   vào bước harness có làm lệch ghim/băm nào nằm NGOÀI write set không? Bộ đột biến hiện có có đột biến
   được `ci.yml` không (M6/M7)?
3. **Tiêu chí có thể đỏ (L3/L6).** Với từng A1–A11: phép đo nào làm nó đỏ, có cách nào xanh mà không đo gì?
   Tiêu chí khớp chuỗi có vế dương + vế âm chưa? A1 có thật sự chặn bản vá tắt đột biến ở đường đầy đủ không?
4. **An toàn của đường nhanh.** Có đường nào `che_do=duong_nhanh` mà diff đổi được mã harness/bộ phân loại/
   `ci.yml`? Giá trị env có fail-close đủ chưa? Tiến trình con thừa kế biến (C3) — còn chỗ gọi con nào bị sót?
   Push master và `workflow_dispatch`: output `che_do` có luôn được đặt không?
5. **Khả thi của A6 (tiền-canary).** PR có base là một nhánh KHÔNG phải master: `chuan-bi`/`ops/ci_duong_nhanh.py`
   có phân loại nó thành `duong_nhanh` không, hay luôn `day_du`? Nếu không khả thi, đề xuất cách đo thay thế.
6. **Mâu thuẫn nội tại / thứ tự với #1132** (lease `ci-concurrency-master`, nhánh `origin/agent/wp1132-g1-claude`
   sửa cùng hai tệp): đặc tả có chỗ nào sẽ gãy sau khi #1132 land không?

Đầu ra (stdout): danh sách finding, mỗi finding `[Pn] tiêu đề — tệp:dòng — bằng chứng đo được — đề xuất`.
Dòng cuối cùng đúng dạng: `VERDICT: approve|request_changes P0=a P1=b P2=c P3=d`.
