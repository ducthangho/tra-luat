# Cross-review ĐẶC TẢ wp1466 r10, lượt 10 (reviewer: Codex, effort high)

Bạn là REVIEWER độc lập và chỉ đọc.
- Không sửa kho, không push, không gọi API GitHub để ghi.
- Chỉ ghi vào `out/`: verdict vào `out/VERDICT.md`; nháp và script cũng đặt dưới `out/`.
- Viết bằng tiếng Việt.

## Đối tượng
- Kho `github.com/ducthangho/tra-luat`. Mirror ở `kho.git`; cây làm việc ở `cay-kho/`, ghim `core.abbrev 7`, detach tại commit được review.
- Commit được review: `feb0b773bfed9456e6862c8154a9711d8f11912d`, nhánh `ops/wp1466-spec-r10`, PR #1566.
- Tệp được review: `ops/specs/wp1466.md` revision 10, sha256 `ac1593e6cfe22896de372cb601cec6198350dec0bef5077dc80f6b8a44646966`.
  Kiểm băm này ĐẦU TIÊN; lệch thì ghi `blocked` và dừng.
- Lượt trước, review đặc tả lượt 9 trên r9:
  - verdict: `cay-kho/ops/specs/wp1466/review/r9-l9/VERDICT.md` (approve);
  - r9 đã land ở `695916e` (PR #1550).
- Diff r9→r10: `git -C cay-kho diff 695916e feb0b77 -- ops/specs/wp1466.md`. Hồ sơ dựng máy ở `cay-kho/ops/specs/wp1466/r10/`.
- Mã executor: H `da4e876` ở ref `refs/exec/h`.
- Verdict review mã exact-H lượt 1 trên H ấy: `exec-out/VERDICT-ma-h-l1.md`, kết quả `blocked`, gồm P2 `phep-dem-ban-sao-khong-phu-ca-tep` và P3 `ca-id-chi-do-mot-gia-tri`.
- Handoff của executor: `exec-out/HANDOFF*.md`.

## Vì sao có r10 (bạn không mở được URL; nội dung tóm ở đây)
- **Q3 (E3), chủ kho chọn "Thu hẹp lời hứa, chuyển #1469":**
  - ADR-0068 và đặc tả nói đúng phép (3) đo được: chỉ đếm bản hiển thị đứng thành đơn vị cùng loại.
  - Bản sao không đứng thành đơn vị là nợ `INV-KHOA-BAN-SAO-DINH-CHU`, giao Issue #1469.
  - Mã phép (3) không đổi.
- **E2, chủ kho chọn "Nâng trần lên 500 dòng":** dùng để đóng P3 bằng ca G8 cho ID thật và các biên, cùng một đột biến thu hẹp miền số về 99.
- **Chủ kho đã duyệt băm r10 (E5)** và chọn review r10 bằng Codex CLI. Đây là lời gọi 12/13 (ADR-0055).

## Chỉ thị bắt buộc của chủ kho
Đọc NGUYÊN VĂN:
- `cay-kho/.claude/skills/cross-review/SKILL.md`;
- `cay-kho/docs/PROTOCOL_DA_PHIEN.md` §7, §8, §8.3, §12;
- `cay-kho/docs/adr/0060-dieu-kien-merge-va-moc-ready.md` (M1–M12), ADR-0062, ADR-0063;
- `cay-kho/.claude/skills/soan-spec/SKILL.md`;
- `cay-kho/CLAUDE.md`.

Review THEO LỚP:
- Khái quát mỗi biểu hiện thành một lớp, gắn slug ổn định; giữ slug cũ cho lớp cũ.
- Quét mọi biểu hiện cùng lớp trước khi báo.
- Không lấy danh sách của executor làm trần.
- Không gộp slug, không đổi hạng.
- Reviewer không tự ghi nợ, không tự miễn P3.

## Việc
1. **Đối chiếu lượt trước.** Các lớp đã đóng ở lượt 9 có bị r10 tái mở không? Hai lớp của review mã lượt 1:
   - P2: kiểm xem việc chuyển sang bảng (ii) có đủ ba điều kiện không:
     (1) wp1466 không còn lời hứa hay tiêu chí nào chạm tới biểu hiện. Rà TOÀN VĂN đặc tả và khối `adr`, tìm câu còn hứa "bất kỳ", "đúng một bản" mà chưa thu hẹp;
     (2) nợ có tên, và tên ấy nằm trong mục *Nợ* của khối `adr`;
     (3) Issue kế nhiệm được nêu.
     Theo §8.3, phần chuyển đi KHÔNG được ghi `ĐÃ VÁ THẬT`.
   - P3: yêu cầu ở dòng G8 có đủ để đóng lớp không, và có đo được không?
2. **Diff r9→r10 không phá phần khác:**
   - sáu khối protocol, khối `khoa`, `do-pham-vi`, `so-dang-ky` phải trùng byte với r9;
   - số đếm "28 tên nợ" phải khớp số mục *Nợ* thật trong khối `adr`;
   - trần 500 phải nhất quán ở mọi chỗ (N12, mục 10);
   - dòng Trạng thái của 8.1 phải dẫn đúng lần duyệt r10.
3. **Đo:**
   - Dựng H `da4e876`, áp phần diff r9→r10 của khối `adr` vào tệp ADR trong một cây tạm dưới `out/`.
   - Chạy `doc-claims-check --strict --json`, `doctrine-scan`, `adr-song`.
   - Quét mọi chuỗi trong backtick mới thêm vào khối `adr`, tìm các lớp L1–L12 có thể đọc nhầm chúng.
4. **Săn lớp mới chỉ trong phần r10 đổi.** Kiểm L1–L7 của soan-spec và trần ADR-0053/0055.

Hướng nào cần dựng nội dung tấn công thì MÔ TẢ BẰNG LỜI.
Ghi `out/VERDICT.md` SỚM, rồi cập nhật dần.

## Mẫu verdict
```
verdict: approve | changes_requested | blocked
reviewed_sha: feb0b773bfed9456e6862c8154a9711d8f11912d
spec_sha256: ac1593e6cfe22896de372cb601cec6198350dec0bef5077dc80f6b8a44646966
reviewer: {provider: codex, model_family: openai, surface: codex_cli, transport: machine, effort: high, session_id: <id hoặc KHONG_DO_DUOC>}
review_axes: [Spec, Standards/Security]
dem: {so_lop_mo_wp1466: , so_bieu_hien_mo: , P0: , P1: , P2: , P3: , so_lop_no_ke_nhiem: }
hoi_tu: {U: , F: , lop_moi: , lop_tai_mo: }
## ĐỐI CHIẾU LƯỢT TRƯỚC
| slug | nhãn | bằng chứng tự đo |
## BẢNG LỚP (i): lớp MỞ của wp1466
| slug lớp | biểu hiện | hạng | phương án chung | phép kiểm/giới hạn |
## BẢNG LỚP (ii): nợ kế nhiệm có authority
| slug lớp | biểu hiện | Issue kế nhiệm | tên nợ | bằng chứng wp1466 không còn khai gì |
## BẢNG SĂN   (ít nhất 6 hướng ĐỘC LẬP, có LỆNH + OUTPUT THẬT)
## BẢNG ĐO
### <slug>  [P0|P1|P2|P3]  <tiêu đề>
TỆP/DÒNG:
VẤN ĐỀ:
GỢI Ý VÁ:
ĐÃ THỬ NGHIỆM:
ĐỘ TIN:
```
Chỉ ghi `approve` khi bảng (i) có 0 finding P0–P3. Nêu rõ những gì bạn KHÔNG đo được.
