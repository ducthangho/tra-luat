# Review offline ĐẶC TẢ packet — lượt 4

Bạn là reviewer độc lập. Thư mục làm việc là một clone của kho `ducthangho/tra-luat` ở commit
`e4b1d788925f664f325795f8b2c536827369809b`. Thứ định danh tệp là BĂM, không phải tên nhánh.
Đối tượng review: `ops/specs/CI-DUONG-NHANH-BO-DOT-BIEN-r1.md`
(sha256 `cff326ac63f59e8126b0becc204f9c641f90dc1948c3ea45a75d5640d90b4d47`).
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

## Lượt 4 — thêm
Lượt 3 (`4a50827`) đã approve 0/0/0/0. Sau đó: `35a395b` (trần 300, đích M10 là `y04`) và `e4b1d78` (xử P1 của connector
`@codex review` trên PR #1144: gương Windows `.claude/dev/chay-cong-windows.ps1` / `t30` `t32` của
`.claude/dev/chay-cong-windows_test.ps1` bị sót khỏi write set). Diff: `git diff 4a50827 e4b1d78 -- ops/specs/`.
Việc: (1) kiểm §2.3 và A8b: con số đo nền (34/36, 5 khoá, 7 dấu vân, 2 job mới, 2 bước) có khớp được bằng đọc mã
không (không có pwsh trong sandbox — đọc `Doc-DauVanCi`, `t30`, bảng `$DauVanCi`); quyết định KHÔNG ghim lại
`$DauVanCi` có làm A8b xanh rỗng không; (2) lớp lỗi đã lặp HAI lần: *ghim cấu trúc / bộ đọc `ci.yml` bị sót ngoài
write set* (lần 1 `Y04_ENV_BUOC_CHE_DO`, lần 2 gương PowerShell). Quét TOÀN KHO mọi bộ đọc `ci.yml` theo mọi đuôi tệp
(`.py .ps1 .sh .yml .md`…) — `rg -l "ci\.yml|chuan-bi|gate-ops"` — và với từng bộ, kết luận thêm `env:` vào bước
harness có làm nó đổi màu không. Lần thứ ba của lớp này là ngưỡng dừng.
