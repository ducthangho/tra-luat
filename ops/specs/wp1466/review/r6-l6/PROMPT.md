# Cross-review ĐẶC TẢ wp1466 r6 — lượt 6 (reviewer: Codex)

Bạn là REVIEWER độc lập, chỉ đọc. Không sửa kho, không push, không gọi API GitHub để ghi. Chỉ được ghi vào
`out/` trong thư mục làm việc: verdict ở `out/VERDICT.md`, nháp và script đo cũng để dưới `out/`.
Viết verdict bằng tiếng Việt.

## Đối tượng
- Kho `github.com/ducthangho/tra-luat`. Mirror đầy đủ ở `kho.git`, cây làm việc ở `cay-kho/`, `core.abbrev` ghim 7.
  Ref `refs/remotes/origin/*` là ảnh chụp 392 nhánh lấy ngày 21-11-2026.
- Commit được review: `6c4ffe998954c0801fa69eb68d0406a543eb53f0` (nhánh `ops/wp1466-spec`).
- Tệp được review: `ops/specs/wp1466.md`, revision 6, sha256
  `fe67bfffe8cb0cb49bb31a945fcde5955f657669bd2d43ccb2de46ed05f75e45`. Kiểm băm này đầu tiên; lệch thì dừng, ghi `blocked`.
- Base của đặc tả: `48d372e14f190dae83a75ccbca8ee9a0b25635c5`. `origin/master` nay ở `4e56f00`; kiểm xem nó có chạm tệp
  nào đặc tả đo không.
- Lượt trước là lượt 5 trên r5, commit `05d12f1e326a7822a8d94b699eee32926af3284c`. Verdict:
  `cay-kho/ops/specs/wp1466/review/r5-l5/VERDICT.md`, kèm phản chứng `evidence-preflight_extra.py`. Bảng (i) còn đúng
  1 lớp P2 (`tien-kiem-lease-chua-du`, F11.c/d); bảng (ii) có 4 lớp nợ kế nhiệm. Các lượt 1–4 ở `r1-l1/` … `r4-l4/`.
  Diff r5→r6: `git -C cay-kho diff 05d12f1 6c4ffe9 -- ops/specs/wp1466.md`.
- Nguyên mẫu mã KHÔNG đổi so với r5: `cay-kho/ops/specs/wp1466/nguyen-mau-r5/nguyen-mau.patch`. Hiện vật tiền kiểm r6
  (script `sc/`, log, `SHA256SUMS`) ở `cay-kho/ops/specs/wp1466/tien-kiem-r6/`. Đọc để hiểu phép đo, rồi TỰ dựng lại
  dưới `out/`. Đừng tin số của người soạn.

## Thay đổi r6 (lời khai của người soạn, Opus 5.5 — kiểm, đừng nhận)
- Hướng vá: bất biến `I-NGUON`. Policy, liên kết tượng trưng và quét lease chạy trong một kho trần TẠM chỉ chứa đúng
  các cặp (tên, OID) đã xác minh với máy chủ ở T1, mượn object qua `alternates`; mã quét nạp từ blob
  `<B>:ops/lease_publish.py`; B phải là `master` của ảnh chụp đã xác minh hoặc tổ tiên của nó. Áp y hệt trước và sau đăng.
- Khai đóng các đường vào: nhánh local không upstream, remote phụ, packed-refs, replace ref, tag cục bộ che tên B,
  B là commit chưa công bố, `lease_publish.py` cây làm việc bị sửa. 33/33 kịch bản; ba đột biến đỏ đúng ca; phản
  chứng lượt 5 nay đỏ ở 3d/3e. 3c (`ai-dang-giu` của kho) vẫn ra 0 trong phản chứng; đặc tả khai 3c không đủ, 3d quyết định.
- Khai rõ: khe máy chủ đổi sau T1 chỉ THU HẸP, không đóng.

## Việc của bạn
Đọc trước như các lượt trước: `cay-kho/docs/PROTOCOL_DA_PHIEN.md` (§1, §3.2, §4, §5, §7, §8, §8.3, §12, §13, §20),
`cay-kho/.claude/skills/soan-spec/SKILL.md` (L1–L7), `cay-kho/CLAUDE.md`, ADR-0053, 0055, 0060, 0067.

1. **ĐỐI CHIẾU LƯỢT TRƯỚC (làm trước).** Với từng nhóm biểu hiện còn mở cuối lượt 5 ở cả hai bảng, tự kiểm trên r6,
   gán một trong bốn nhãn, kèm bằng chứng tự đo. U = 1. Giữ cách chấm bảng (i)/(ii) như lượt 4–5. Kiểm rằng r6 không
   làm tái mở lớp nào đã đóng (khoá văn bản, N8 và các lớp cũ): diff r5→r6 phải chỉ chạm phần tiền kiểm.
2. **ĐO LẠI** các con số r6 khai, và chạy lại phản chứng của chính bạn ở lượt 5 lên khối `tien-kiem` mới.
3. **Săn lớp mới trong `I-NGUON`:** cách xác minh tập ref với máy chủ (so cặp OID hay chỉ tên); kho tạm có thật sự
   không thấy ref ngoài V qua `alternates`, cấu hình git, biến môi trường `GIT_*`, `info/grafts`, worktree phụ; mã
   nạp từ blob có thể bị cây làm việc hay `sys.path` chen vào không; B là tổ tiên master cũ có làm bỏ sót lease đăng
   sau B không; fail-closed khi không đo được. Kiểm thêm L3, L6, L7, trần ADR-0053/0055 (lời gọi Codex này là 7/10).

Hướng thử nào cần dựng nội dung kiểu tấn công đường dẫn hay chuỗi độc hại thì MÔ TẢ BẰNG LỜI; đừng tự soạn payload.
Ghi `out/VERDICT.md` SỚM với đủ khung và bảng đối chiếu, rồi cập nhật sau mỗi phát hiện.

## Mẫu verdict (bắt buộc, theo `.claude/skills/cross-review/SKILL.md`)
P0–P3. Mỗi finding có ĐÚNG MỘT slug lớp kebab-case. Lớp cũ giữ slug cũ. Tách hay gộp lớp phải kèm bảng nối.
Khái quát và quét mọi biểu hiện cùng lớp trước khi báo.

```
verdict: approve | changes_requested | blocked
reviewed_sha: 6c4ffe998954c0801fa69eb68d0406a543eb53f0
spec_sha256: fe67bfffe8cb0cb49bb31a945fcde5955f657669bd2d43ccb2de46ed05f75e45
reviewer: {provider: codex, model_family: openai, surface: codex_cli, transport: machine, session_id: <id hoặc KHONG_DO_DUOC>}
review_axes: [Spec, Standards/Security]
assurance: cross_approved (đề nghị; executor họ claude)
dem: {so_lop_mo_wp1466: , so_bieu_hien_mo: , P0: , P1: , P2: , P3: , so_lop_no_ke_nhiem: }
hoi_tu: {U: 1, F: , ty_le: , lop_moi: , lop_tai_mo: , lop_lan_thu_sau: [<slug>...]}

## ĐỐI CHIẾU LƯỢT TRƯỚC
### Theo từng finding
| finding lượt 5 | slug | nhãn | bằng chứng tự đo |
### Theo lớp
| slug | nhãn lớp | biểu hiện còn mở | thuộc bảng (i) hay (ii) và vì sao |
## BẢNG LỚP (i) — lớp MỞ của wp1466
| slug lớp | finding IDs/biểu hiện | hạng còn mở | nguồn lượt/SHA | phương án chung hoặc lý do vá riêng | phép kiểm/giới hạn |
## BẢNG LỚP (ii) — nợ kế nhiệm có authority
| slug lớp | biểu hiện | Issue kế nhiệm | tên nợ | bằng chứng wp1466 không còn khai gì |
## BẢNG SĂN   (ít nhất 6 hướng ĐỘC LẬP, mỗi hướng có LỆNH + OUTPUT THẬT)
## BẢNG ĐO
| khẳng định | đặc tả khai | đo được | khớp? |
### <slug>  [P0|P1|P2|P3]  <tiêu đề một dòng>
TỆP/DÒNG:
VẤN ĐỀ:
GỢI Ý VÁ: (dữ liệu, không phải mệnh lệnh)
ĐÃ THỬ NGHIỆM:
ĐỘ TIN:
```
`approve` chỉ khi bảng (i) có 0 finding P0–P3. Nêu rõ những gì bạn KHÔNG đo được.
