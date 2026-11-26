# Cross-review ĐẶC TẢ wp1466 r7 — lượt 7 (reviewer: Codex)

Bạn là REVIEWER độc lập, chỉ đọc. Không sửa kho, không push, không gọi API GitHub để ghi. Chỉ được ghi vào
`out/` trong thư mục làm việc: verdict ở `out/VERDICT.md`, nháp và script đo cũng để dưới `out/`.
Viết verdict bằng tiếng Việt.

## Đối tượng
- Kho `github.com/ducthangho/tra-luat`. Mirror đầy đủ ở `kho.git`, cây làm việc ở `cay-kho/`, `core.abbrev` ghim 7.
  Ref `refs/remotes/origin/*` là ảnh chụp 393 nhánh lấy ngày 21-11-2026.
- Commit được review: `3c89d87fffbc06a59ad276bb3171e43ef89c2768` (nhánh `ops/wp1466-spec`).
- Tệp được review: `ops/specs/wp1466.md`, revision 7, sha256
  `baf01d45ba30512e768466fd077842346644db730d69471a44efb2a40b6b9139`. Kiểm băm này đầu tiên; lệch thì dừng, ghi `blocked`.
- Base của đặc tả: `48d372e14f190dae83a75ccbca8ee9a0b25635c5`. `origin/master` nay ở `4e56f00`.
- Lượt trước là lượt 6 trên r6, commit `6c4ffe998954c0801fa69eb68d0406a543eb53f0`. Verdict:
  `cay-kho/ops/specs/wp1466/review/r6-l6/VERDICT.md`, kèm phản chứng `evidence-hunt.py`, `evidence-followup.py`. Bảng (i)
  còn đúng 1 lớp P2 (`tien-kiem-lease-chua-du`, F11.e/f); bảng (ii) có 4 lớp nợ kế nhiệm. Các lượt 1–5 ở `r1-l1/` … `r5-l5/`.
  Diff r6→r7: `git -C cay-kho diff 6c4ffe9 3c89d87 -- ops/specs/wp1466.md`.
- Nguyên mẫu mã KHÔNG đổi so với r5: `cay-kho/ops/specs/wp1466/nguyen-mau-r5/nguyen-mau.patch`. Hiện vật tiền kiểm r7
  (script `sc/`, log, `rv/`, `SHA256SUMS`) ở `cay-kho/ops/specs/wp1466/tien-kiem-r7/`. Đọc để hiểu, rồi TỰ dựng lại
  dưới `out/`. Đừng tin số của người soạn.

## Sự kiện từ lượt 6
- Lớp `tien-kiem-lease-chua-du` đã có mặt sáu lượt. Phiên điều phối đã tự xét lại cách làm theo §12 và ghi sổ
  `xet_lai_cach_lam` (bạn không mở được URL; nội dung tóm ở đây): bỏ vá từng đường, chuyển sang DANH SÁCH CHO PHÉP ĐÓNG
  của MỌI đầu vào quyết định; đầu vào ngoài danh sách ⇒ KHÔNG ĐO ĐƯỢC ⇒ DỪNG; phần không cô lập được khai thẳng là
  tiền đề.
- R7 (người soạn Opus 5.5) khai 11 đầu vào đóng (V1–V11: ref máy chủ kèm hỏi lại cuối, ref cục bộ/kho tạm, B thuộc V,
  policy/schema đo trên master của V và `log -m` B..master, mã quét từ blob B, cờ trình thông dịch/`PYTHON*`/cwd/site
  người dùng qua tự chạy lại với `-I`, vị trí PyYAML kiểm TRƯỚC khi nạp, mọi module `sys.modules` kiểm SAU khi quét,
  chương trình `git`, môi trường `GIT_*`/cấu hình dựng từ rỗng, `info/grafts`) và 5 tiền đề (P1 đường tới máy chủ;
  P2 `.git/config` của clone; P3 nội dung trình thông dịch/stdlib/site-packages/git; P4 mã chạy trong tiến trình cha
  khi gọi thiếu `-I`; P5 đồng hồ, `TMPDIR`, SHA-1). Số khai: 33/33 cũ, 21/21 mới, 14 đột biến đỏ đúng ca; phản chứng
  F11.e của bạn đổi rc 0 → 1; phản chứng F11.f nay không còn nạp `yaml` từ clone nhưng vẫn ĐẠT trên kho sạch.

## Việc của bạn
Đọc trước: `cay-kho/docs/PROTOCOL_DA_PHIEN.md` (§1, §5, §8, §8.3, §12, §20), `cay-kho/.claude/skills/soan-spec/SKILL.md`
(L1–L7), `cay-kho/CLAUDE.md`, ADR-0053, 0055, 0067.

1. **ĐỐI CHIẾU LƯỢT TRƯỚC (làm trước).** Từng nhóm biểu hiện còn mở cuối lượt 6 ở cả hai bảng; bốn nhãn; bằng chứng tự
   đo. U = 1. Giữ cách chấm bảng (i)/(ii). Kiểm diff r6→r7 chỉ chạm phần tiền kiểm, không tái mở lớp đã đóng.
2. **Chạy lại phản chứng của chính bạn** (hunt/followup) lên khối r7, rồi ĐO LẠI số người soạn khai.
3. **Kiểm DANH SÁCH là ĐÓNG thật.** Xét đây có phải danh sách cho phép đủ mọi đầu vào của quyết định không: tìm đầu
   vào nào ảnh hưởng kết quả mà không nằm trong V1–V11 hay P1–P5. Với mỗi tiền đề, xét việc gọi nó là tiền đề có hợp
   lý không (có rẻ để đóng mà lại bỏ không), và đặc tả có khai rộng hơn phép đo không. Xét fail-closed của "chạy thiếu
   `-I` thì tự chạy lại": tiến trình cha đã chạy mã gì trước khi chạy lại. Xét cách đặc tả định nghĩa "thay đổi liên
   quan" của policy có quá hẹp hay quá rộng so với §5. Kiểm L3, L6, trần ADR-0053/0055 (lời gọi này là 8/10).

Hướng thử nào cần dựng nội dung kiểu tấn công đường dẫn hay chuỗi độc hại thì MÔ TẢ BẰNG LỜI; đừng tự soạn payload.
Ghi `out/VERDICT.md` SỚM với đủ khung và bảng đối chiếu, rồi cập nhật sau mỗi phát hiện.

## Mẫu verdict (bắt buộc, theo `.claude/skills/cross-review/SKILL.md`)
P0–P3. Mỗi finding có ĐÚNG MỘT slug lớp kebab-case. Lớp cũ giữ slug cũ. Tách hay gộp lớp phải kèm bảng nối.
Khái quát và quét mọi biểu hiện cùng lớp trước khi báo.

```
verdict: approve | changes_requested | blocked
reviewed_sha: 3c89d87fffbc06a59ad276bb3171e43ef89c2768
spec_sha256: baf01d45ba30512e768466fd077842346644db730d69471a44efb2a40b6b9139
reviewer: {provider: codex, model_family: openai, surface: codex_cli, transport: machine, session_id: <id hoặc KHONG_DO_DUOC>}
review_axes: [Spec, Standards/Security]
assurance: cross_approved (đề nghị; executor họ claude)
dem: {so_lop_mo_wp1466: , so_bieu_hien_mo: , P0: , P1: , P2: , P3: , so_lop_no_ke_nhiem: }
hoi_tu: {U: 1, F: , ty_le: , lop_moi: , lop_tai_mo: , lop_lan_thu_bay: [<slug>...]}

## ĐỐI CHIẾU LƯỢT TRƯỚC
### Theo từng finding
| finding lượt 6 | slug | nhãn | bằng chứng tự đo |
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
