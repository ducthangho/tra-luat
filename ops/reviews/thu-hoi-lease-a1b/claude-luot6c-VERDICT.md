# Review Claude độc lập — lượt 6c (agent `spec-reviewer-max`, effort **max**) — spec `THU-HOI-LEASE-A1b` bản nháp 10

- đối tượng: `ops/specs/THU-HOI-LEASE-A1b.md` @ `e009b99` (sha256 `af86b561…`); 445 = 445 ref lúc đo
- reviewer: subagent Claude agent `spec-reviewer-max` (định nghĩa cục bộ, không trong kho), read-only;
  `same_provider_approved` — bổ sung, KHÔNG thay `human_audited`; KHÔNG tính vào trần Codex
- ghi chú hình dạng: tóm lược do phiên điều phối ghi lại, không phải raw output bất biến.

VERDICT: changes_requested — **0 P1 / 4 P2 / 5 P3**

1. [P2] A6/A5 — oracle `check`/`ai-dang-giu` không giết mutant bỏ kết quả discovery mà áp luật mới trên map cục bộ
   (`_du_bao_check` `ops/lease_publish.py@67802bf:1763–1770`; so mỏ neo nằm trong `kham_pha_nguon` :1329–1333).
2. [P2] A5 — tập dẫn độc lập không vai nào được ghi; bản chép của điều phối thoả được tiêu chí.
3. [P2] A5 / M1 — delta kho thật nhận trên lời khai executor; r9 `:628` Q10(g) đòi chủ kho readback; fact (g) trôi.
4. [P2] §7 — lớp "mốc giờ lệch" chạm lượt review thứ ba mà không checkpoint (§12 `:1053–1055`, `:1102–1103`);
   cột "số lần" thiếu đơn vị; "tập rỗng" đếm theo lượt là 2.
5. [P3] trần bản nháp 1 là 4 (`65a612a:9`).
6. [P3] §8.7 descriptor `f974b6db…`.
7. [P3] A3 "tất định" thiếu đầu vào: `do_q6_hk.py` nạp `ops/lease_publish.py` từ cây `<kho>` (đo: ba lệnh trên
   `5c79fa2` ⇒ rc 0/0/0, sha256 `fca744cd…`/`c35d316d…`/`1fc99cd9…`, khớp log r3).
8. [P3] `claude-tu-kiem-nhap10.md` neo `a4010f4` chỉ còn trong reflog.
9. [P3] `dong_bang` không đòi chủ kho xác nhận Q15-diễn giải.

Xử lý: checkpoint (mục 4) đưa lên chủ kho ⇒ Q18 "vá tiếp mọi finding"; vá cả 9 ở bản nháp 11.
