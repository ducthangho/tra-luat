# Handoff wp978-g1-claude — nợ F13 của #899 (`git_cuc_bo` đọc metadata commit bằng bytes)

- packet #978 · lease `wp978-r1-g1-claude` (`ops/leases/wp978-r1-g1-claude.yaml`, nhánh `ops/wp978-r1-g1-lease`)
- spec `ops/specs/wp978.md` sha256 `eccd6dd2917f76d6158d5c9574f4d4c2070ba22ef3da96b4dfcf6e820c301638` (commit `5f438b4`)
- base `c8d92ba05c3ea875d8f84d94195430302690286d` · head approve `53ec046fc6c9ebc2b60871a5c0413570d3b0430d` trên `agent/wp978-g1-claude`
- executor phiên `session_015GtxrZYA5uRwjhUvsG1i8A`

## Thứ tự (khai thẳng)
Bản vá đầu được viết THĂM DÒ trước khi có lease, để đo kích thước cho đặc tả; không commit/đẩy trước lease. Spec `5f438b4`
→ lease `83de8bc` (check rc 0, run `ops-publish-lease.yml` 40482277284 `success` 09:44Z) → commit `bef1403` (cha = base_sha).
Phiên điều phối `session_01B8U8TTEwfMS1u4u4E1VmRW` nhắc thứ tự này. Suite bằng chứng chạy SAU lease xanh.

## Quyết định chủ kho (ghi hộ trên #978)
- 6438443889: cấp việc + lease. 6441085134: trần Codex 2 → 4. 6442791177: trần → 8 (ADR-0052; 10 cần dòng khai ADR-0055 ⇒ r2),
  luật V1–V3 của wp899. 6445001458: lớp độ phủ còn lại (đột biến sống, sản phẩm vẫn đúng) ⇒ P3 + nợ
  `wp978-git-reader-differential-fuzz` (owner ducthangho, test vi sai sinh ngẫu nhiên theo ngữ pháp header Git).

## Thay đổi (diff base..head: 2 tệp, +157/-6)
- `ops/ci_provenance.py` `git_cuc_bo`: một lời gọi `git cat-file --batch` (sha qua stdin) ⇒ loại object + nội dung cùng ảnh,
  không peel tag; đòi header `<oid> commit <size>`, kích thước khớp, rc 0; đọc BYTES, tách phần đầu tại LF-LF, dòng tại LF;
  `tree` phải là dòng đầu và duy nhất; `parent` = dãy LIỀN SAU (ngữ pháp Git); OID 40/64 hex; chỉ giải mã ASCII sau kiểm.
  Không dùng `git log %P` vì clone nông (CI) graft cha (lượt 4 đo: 0 cha thay vì 5).
- `ops/ci_provenance_test.py`: ca `c53` (Git thật, `hash-object`, oracle Git native `log --no-walk`, ma trận 350 commit,
  tiêm lỗi git); 53 mục `DOT_BIEN` `F13_*`.

## Review Codex (gpt-6-astra, xhigh, `launcher.py run`) — 8/8 lời gọi
| lượt | head | verdict | lớp |
|---|---|---|---|
| 1 | bef1403 | request_changes | F13 đóng; P2 `git-object-type-not-checked`, P2 `git-header-cr-split-creates-parents` (có sẵn từ base); P3 độ phủ |
| 2 | 7fcfe18 | (cắt rc 1, VERDICT tạm) | 2 P2 đóng; 5 đột biến sống, nghi vấn bộ bọc NEM |
| 3 | fdf1f05 | request_changes | P2 `git-header-extension-creates-parents` (có sẵn từ base); P2 độ phủ |
| 4 | aa2a1f3 | request_changes | P2 độ phủ (lstrip header) |
| 5 | afcadd5 | request_changes | P2 độ phủ: 22/49 phép chuẩn hoá header sống |
| 6 | 2c907a4 | request_changes | P2 độ phủ: 10 đột biến ranh giới/dãy parent |
| 7 | bf8ef91 | request_changes | P2 độ phủ: 15 đột biến tổ hợp ⇒ chủ kho hạ P3 |
| 8 | 53ec046 | **approve** | P0=P1=P2=0; P3 độ phủ (S01 `tree: <oid>`, S02 backslash-LF) ⇒ nợ fuzz |
Hiện vật: `ops/reviews/wp978-g1-codex-luot{1..8}/`. Hình dạng lỗi: "parser tay tạo parent giả" 2 lần (CR, extension);
"độ phủ fixture" 5 lần liên tiếp ⇒ đã hỏi chủ kho (bài học đếm hình dạng lỗi).

## Nghiệm thu trên 53ec046
- N1: c53 head rc 0; với sản phẩm base ⇒ `DO:c53_…` UnicodeDecodeError (rc 3).
- N2: 53/53 F13 GIET đúng c53 (gồm 3 đột biến M3 dạng tương ứng: giải mã toàn stdout, giải mã phần đầu, bỏ kiểm OID).
- N3: full suite trên clone riêng `53ec046` (14:52:53Z → 15:45:33Z): `CA: 53/53` · `DOT BIEN: 345/345` · `TU KIEM PHAN HANG: DAT` · `TONG: DAT` rc 0. Base `c8d92ba`: `52/52` · `292/292`.
- N4: ruff F (0.17.3) hai tệp base/head `All checks passed!` ⇒ delta 0; `git diff --check` rc 0.
- N5: doctrine-scan rc 0; adr-song rc 0 (55/55).
- N6: CI PR — đo sau khi đẩy. N7: không áp dụng (`git_cuc_bo` ngoài `HAM_DONG`), không chạy.

## Lệch đặc tả cần chủ kho xác nhận
- Kích thước +157 dòng > "dự kiến ≤ 60" (dưới trần ADR-0053 450).
- Hai P2 có sẵn từ base được vá trong packet (executor xếp vào M1, không phải "lỗi khác" của Q5).
- M2 viết "chỉ UnicodeDecodeError thành tín hiệu chốt"; bộ bọc `doc()` đổi MỌI ngoại lệ NỔI TỪ khung `git_cuc_bo` thành
  giá trị (hợp đồng không-ném); lỗi ngoài khung ⇒ rc 4. Reviewer lượt 3–8 không xác nhận tín dụng giả.
- Tên đột biến M3 `F13_doc_text_true` nay là `F13_giai_ma_toan_stdout` (mã đổi sang `--batch`).

## Sai sót của executor (khai)
- Hai lần sửa tệp test khi full suite đang chạy trong cây làm việc ⇒ hai lượt suite bị huỷ, không dùng làm bằng chứng;
  từ đó suite chạy trên clone riêng của đúng SHA.
- Lần đầu ghi sai SHA đầy đủ trong prompt lượt 1 (sửa trước khi gọi).

## Chưa đo được
Windows native; `ci_dang_ky_test.py --chay`; băm byte lời chủ kho; model/effort phục vụ của Codex (header CLI không đủ).
