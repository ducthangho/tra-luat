# Review Codex offline lượt 2/2 — packet #1240 ASSURANCE-81-MODEL-EFFORT-TUY-CHON r1: lượt THAY lượt 1 (run bc004964), TUÂN THỦ READ-ONLY

Bạn là reviewer độc lập (họ OpenAI). QUY TẮC TUYỆT ĐỐI: KHÔNG ghi bất kỳ tệp nào trong thư mục làm việc này. Cấm cả tệp bị .gitignore bỏ qua, `.git/config` (kể cả `git config` cục bộ, như `core.abbrev`), và việc ghi rồi dọn sau. Lượt 1 bị loại vì selftest sinh 20 tệp ignored trong checkout rồi mới dời đi. Phiên điều phối so sha256 của MỌI tệp trong cây (gồm `.git`) trước và sau lượt này; lệch một byte là lượt vô hiệu.

Bước ĐẦU TIÊN: `git clone --no-hardlinks <thư mục làm việc> /tmp/rv1240-copy`, hoặc `cp -a`. Cấu hình (`git config core.abbrev 7`…), selftest, test, đột biến, script đo: chỉ chạy TRONG bản sao. Lệnh chỉ đọc (`git diff/show/rev-parse/log`, đọc tệp) thì chạy trực tiếp được.

## Neo
- HEAD phải là `ecd30737e10cb7cdffe0e17178c28b3a12448874` (head đã merge của PR #1249, merge commit `51d6509`). Khác thì kết luận request_changes.
- Base: `3163f4d02a583787a9340c63a1f5eebd3780d970`.
- Đặc tả: `ops/specs/assurance-81-model-effort-tuy-chon-r1.md`, sha256 `e7c6707860ba6a7ca6d24b1cadc2510b4b93952048375bdc332e0328d601487e`. Chủ kho đã chốt Q1 = theo provider, Q2 = không tính.

## Việc phải kiểm: review ĐẦY ĐỦ diff `3163f4d..HEAD` (4 tệp) theo đặc tả
- Đúng ngữ nghĩa: L7 mới trong `ops/land_evidence_nguon.py` (model/effort tuỳ chọn, sandbox bắt buộc, giá trị rác vẫn ĐỎ); văn bản §8.1, §8 mục 1, §20 trong `docs/PROTOCOL_DA_PHIEN.md`; ADR-0065 đủ (i)–(vi).
- Chạy (TRONG BẢN SAO) A1–A11 của đặc tả, mỗi tiêu chí có vế dương và đột biến vế âm. Riêng A7: `land_evidence_nguon --root .` trên base và trên head trong CÙNG MỘT lệnh, kết quả ĐẠT/miễn trừ/vi phạm phải giống hệt.
- `python ops/land_evidence_nguon_test.py` ⇒ `TONG: DAT`, dòng `DOT BIEN: N/N` hai số bằng nhau. `python scripts/tl.py --selftest` ⇒ N/N.
- A8: `ops/kiem_ho_so_land.py` không đổi so với base.
- Đã biết, không chặn: F1 P3 của lượt 1 (7 đột biến sống của c23) đã chuyển nợ sang #1236. Không tính lại thành P1/P2.
- K-f: tự khai mọi lệnh có thể ghi đã chạy trong bản sao nào (in đường dẫn), và xác nhận KHÔNG ghi gì vào thư mục làm việc.

## Đầu ra
Ghi phát hiện theo bậc P0/P1/P2/P3, mỗi phát hiện kèm lệnh tái hiện. Dòng cuối cùng của stdout, đúng nguyên văn, chữ thường:
`KET_LUAN: approve` nếu không còn P0/P1/P2; ngược lại `KET_LUAN: request_changes`.
