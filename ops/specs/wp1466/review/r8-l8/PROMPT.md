# Cross-review ĐẶC TẢ wp1466 r8 — lượt 8 (reviewer: Codex)

Bạn là REVIEWER độc lập, chỉ đọc. Không sửa kho, không push, không gọi API GitHub để ghi. Chỉ được ghi vào
`out/` trong thư mục làm việc: verdict ở `out/VERDICT.md`, nháp và script đo cũng để dưới `out/`.
Viết verdict bằng tiếng Việt.

## Đối tượng
- Kho `github.com/ducthangho/tra-luat`. Mirror đầy đủ ở `kho.git`, cây làm việc ở `cay-kho/`, `core.abbrev` ghim 7.
  Ref `refs/remotes/origin/*` là ảnh chụp 394 nhánh lấy ngày 21-11-2026.
- Commit được review: `e215940d15286add6fe30947cfccda09a09d82c0` (nhánh `ops/wp1466-spec`).
- Tệp được review: `ops/specs/wp1466.md`, revision 8, sha256
  `98790505d927224bc5e1e42e8f9460376a911a913e2e1d1b12bdf36c5eb20834`. Kiểm băm này đầu tiên; lệch thì dừng, ghi `blocked`.
- Base của đặc tả: `48d372e14f190dae83a75ccbca8ee9a0b25635c5`. `origin/master` nay ở `4e56f00`.
- Lượt trước là lượt 7 trên r7, commit `3c89d87fffbc06a59ad276bb3171e43ef89c2768`. Verdict:
  `cay-kho/ops/specs/wp1466/review/r7-l7/VERDICT.md`. Bảng (i) còn 1 lớp P2 (`tien-kiem-lease-chua-du`, F11.f/g/h/i);
  bảng (ii) có 4 lớp nợ kế nhiệm. Các lượt 1–6 ở `r1-l1/` … `r6-l6/`.
  Diff r7→r8: `git -C cay-kho diff 3c89d87 e215940 -- ops/specs/wp1466.md`.
- Nguyên mẫu mã KHÔNG đổi so với r5: `cay-kho/ops/specs/wp1466/nguyen-mau-r5/nguyen-mau.patch`. Hiện vật r8 (rà soát, đo
  lease thật) ở `cay-kho/ops/specs/wp1466/rut-tien-kiem-r8/`.

## Sự kiện từ lượt 7 (bạn không mở được URL; nội dung tóm ở đây)
- Chủ kho quyết theo E2 (ghi hộ ở #1466, comment 7058057029, nguyên văn "Tách khối ra (Recommended)"): rút khối tiền
  kiểm tự dựng khỏi wp1466; điều kiện cấp lease chỉ dùng công cụ sẵn có (so tập ref, `ai-dang-giu` cho từng đường dẫn)
  và khai đúng giới hạn; mở packet riêng có tên nợ làm công cụ tiền kiểm toàn kho; lớp chuyển sang bảng (ii).
- Packet kế nhiệm đã mở: **Issue #1484** "[Packet proposed] Tiền kiểm lease toàn kho", `depends_on: [1466]`, thẩm
  quyền là quyết định E2 trên. Nợ: `INV-02-TIEN-KIEM-CAP-LEASE-KHONG-CLOSURE` (tên đã có sẵn trong ADR-0068 mục Nợ và
  ô `còn nợ` của INV-02; r8 không đổi văn bản ADR để khỏi chạm đơn vị khoá K01; mối nối tới #1484 nằm trong đặc tả,
  xem D17).
- R8 (người soạn Opus 5.5) xoá khối `tien-kiem`, viết lại điều kiện 3a–3e chỉ bằng công cụ sẵn có, và ghi giới hạn
  G1–G10 là nợ #1484, wp1466 không hứa gì về chúng.

## Việc của bạn
Đọc trước: `cay-kho/docs/PROTOCOL_DA_PHIEN.md` (§1, §4, §5, §8, §8.3, §12, §20), `cay-kho/.claude/skills/soan-spec/SKILL.md`
(L1–L7), `cay-kho/CLAUDE.md`, ADR-0053, 0055, 0067.

1. **ĐỐI CHIẾU LƯỢT TRƯỚC (làm trước).** Từng nhóm biểu hiện còn mở cuối lượt 7 ở cả hai bảng; bốn nhãn §8; bằng chứng
   tự đo. Phần chuyển sang #1484 KHÔNG được ghi `ĐÃ VÁ THẬT`. U = 1. Áp đúng ba điều kiện vào bảng (ii) của các lượt
   trước: (1) wp1466 không còn lời hứa hay tiêu chí nào chạm tới biểu hiện; (2) nợ có tên; (3) Issue kế nhiệm được
   nêu. Thiếu một thì ở bảng (i). Rà TOÀN VĂN đặc tả tìm câu còn hứa đóng ranh giới tiền kiểm (kể cả mục 0, 1, 3, 9,
   14, 16–19, bảng INV). Xét riêng: việc mối nối #1484 chỉ nằm trong đặc tả mà không nằm trong văn bản ADR-0068 có
   làm hỏng điều kiện (2)/(3) không, hay chỉ là một chỗ lệch hình thức (khi đó hạng bao nhiêu và vì sao).
2. **Kiểm điều kiện 3a–3e mới:** có tự mâu thuẫn, có hứa gì công cụ sẵn có không làm được, có còn đúng protocol §4/§5
   cho việc cấp lease không, có mâu thuẫn với C5 (merge thẳng master) không. Đo lại các số r8 khai (lease thật, rà grep).
3. **Kiểm diff r7→r8 không tái mở lớp đã đóng:** các khối `khoa`, protocol, `adr`, `do-pham-vi`, `so-dang-ky` phải
   trùng byte với r7; nguyên mẫu không đổi. Săn lớp mới chỉ trong phần đổi. Kiểm thêm L3, L6, L7, trần ADR-0053/0055
   (lời gọi này là 9/10).

Hướng thử nào cần dựng nội dung kiểu tấn công đường dẫn hay chuỗi độc hại thì MÔ TẢ BẰNG LỜI; đừng tự soạn payload.
Ghi `out/VERDICT.md` SỚM với đủ khung và bảng đối chiếu, rồi cập nhật sau mỗi phát hiện.

## Mẫu verdict (bắt buộc, theo `.claude/skills/cross-review/SKILL.md`)
P0–P3. Mỗi finding có ĐÚNG MỘT slug lớp kebab-case. Lớp cũ giữ slug cũ. Tách hay gộp lớp phải kèm bảng nối.
Khái quát và quét mọi biểu hiện cùng lớp trước khi báo.

```
verdict: approve | changes_requested | blocked
reviewed_sha: e215940d15286add6fe30947cfccda09a09d82c0
spec_sha256: 98790505d927224bc5e1e42e8f9460376a911a913e2e1d1b12bdf36c5eb20834
reviewer: {provider: codex, model_family: openai, surface: codex_cli, transport: machine, session_id: <id hoặc KHONG_DO_DUOC>}
review_axes: [Spec, Standards/Security]
assurance: cross_approved (đề nghị; executor họ claude)
dem: {so_lop_mo_wp1466: , so_bieu_hien_mo: , P0: , P1: , P2: , P3: , so_lop_no_ke_nhiem: }
hoi_tu: {U: 1, F: , ty_le: , lop_moi: , lop_tai_mo: , lop_lan_thu_tam: [<slug>...]}

## ĐỐI CHIẾU LƯỢT TRƯỚC
### Theo từng finding
| finding lượt 7 | slug | nhãn | bằng chứng tự đo |
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
