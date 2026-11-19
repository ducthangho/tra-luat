# WP1319 r1 — Prompt review độc lập (Codex, chỉ đọc)

Bạn là reviewer độc lập cho lượt kiểm native r1 của Packet #1319 (nghiệm thu bổ sung Mission #1238, repo tra-luat).
Bạn KHÔNG sửa gì trong kho, KHÔNG chạy lệnh mạng, KHÔNG gọi model khác. Chỉ đọc và chạy lệnh đọc/kiểm băm cục bộ.

## Đầu vào (đều nằm trong thư mục làm việc của bạn)
- `spec/wp1319-r1.md` — đặc tả đóng băng. sha256 phải khớp `spec_hash` trong `spec/wp1319-r1-g1-operator.yaml`.
- `evidence/` — gói bằng chứng đã giải nén từ zip đóng băng. `evidence.zip.sha256` ghi băm zip, còn `MANIFEST.json` ghi path/size/sha256 từng tệp.
- `repo/` — bản sao kho ở đúng SHA `13bf69f6eb797e859619a2062e7c9577e6a9cc0b`, chỉ để đọc harness và SKILL.
- Không có kết luận nào của operator trong đầu vào. Hãy tự dẫn ra kết luận từ raw.

## Việc phải làm
1. Kiểm `MANIFEST.json` khớp từng tệp trong `evidence/` (size + sha256). Lệch hay thiếu tệp nào thì đó là finding P1.
2. Với từng bước N1–N6 của đặc tả: đọc log/report raw và kết luận `passed` / `failed` / `skipped` / `not_run`.
   Phải trích **marker dương** cụ thể (dòng `N/N`, `rc=0`, `SETUP OK`, `PIN OK`, `CLEANUP OK`, report JSON của harness).
   `rc=0` mà không có marker dương thì KHÔNG tính là passed.
3. Các khối N5 (`N5-*.ps1` trong `evidence/scripts/`) khai là trích NGUYÊN VĂN từ
   `repo/.agents/skills/playwright-browser/SKILL.md`, chỉ thay placeholder. Hãy tự trích lại rồi diff. Mọi khác biệt
   ngoài placeholder là finding.
4. Đánh giá các chỗ operator lệch đặc tả, đã khai trong `evidence/*NOTE*.txt`: đặt lại `PSModulePath`, lượt N2 thứ nhất
   hỏng, chạy N5 trên PS7. Mỗi chỗ: lệch có làm sai kết luận không? Có che một FAIL thật không?
5. Tìm lời khai rộng hơn phép đo. Ví dụ: coi chụp `example.com` là xác minh pháp lý; coi WhatIf trên cấu hình giả là
   chứng minh không mutation trên gateway thật; coi harness có fake backend là hành vi thật.
6. Kiểm bằng chứng không chứa secret/token/cookie/profile. Đường dẫn cá nhân và hostname thì chỉ ghi nhận là riêng tư,
   không phải secret.

## Đầu ra
Ghi `VERDICT.md` gồm:
- `verdict: approve | request_changes`
- bảng N1–N6: kết luận, marker trích nguyên văn, tệp nguồn, sha256 tệp nguồn
- danh sách finding, mỗi cái có mức P1/P2/P3, bằng chứng và đề xuất
- mục "giới hạn": những gì r1 KHÔNG chứng minh

Không có finding thì ghi rõ `0 finding` và nêu bạn đã kiểm những gì.
