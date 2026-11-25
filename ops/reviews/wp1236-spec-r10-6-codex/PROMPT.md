# Review ĐẶC TẢ wp1236 r10 bản sửa 1 — vòng 6 — reviewer độc lập, theo PROTOCOL §8.3

Bạn là reviewer ĐỘC LẬP cho một ĐẶC TẢ packet (không phải mã), review class `sensitive`. Kho: ducthangho/tra-luat.

## Bối cảnh
Vòng 5 (`/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r10-6-codex/lich_su/VERDICT_vong5_codex.json`, đúng §8.3) cho r10 bản `98165993…`: `changes_requested`, V01 P2 (`nghiem-thu-khong-co-lap-chot-dich`: luật 3–5 chưa tái lập được, route `head` sai consumer), V02 P3 (`so-do-khong-cung-pham-vi-nguon`). Reviewer đề xuất ghim bộ quét và chạy pilot trên mã r9 `c2d606b`. Bản sửa 1 làm đúng việc đó. Các vòng trước ở `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r10-6-codex/lich_su/`.

## Quyền
- CHỈ ĐỌC trong `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r10-6-codex/repo` và `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r10-6-codex/ma_r9_git`. Không sửa, không commit, không push. Không gọi GitHub/mạng.
- Được tạo tệp nháp/script đo/kết quả CHỈ dưới `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r10-6-codex/work/`.
- Hướng thử nào đòi soạn nội dung tấn công thì MÔ TẢ BẰNG LỜI.

## Đầu vào
- Đặc tả: `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r10-6-codex/SPEC.md`, sha256 `2a1e3cb870c20491af3efb7efdd900f0d372c01a78411e80087ff231999a884e` (= `git show 19fd74a:ops/specs/wp1236-r10.md`). Kiểm sha256 trước; lệch thì dừng. Phần mới: `git diff 4b5e3c6 19fd74a`.
- Kho `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r10-6-codex/repo` HEAD `19fd74ac8a69c4912b5f9484630a607c5dd11184`. Bộ quét ghim: `ops/reviews/wp1236-r10-soan/quet_dot_bien.py` (sha256 khai trong đặc tả), kho cặp `kho_dot_bien_reviewer_luot6.jsonl`, kết quả pilot `pilot_c2d606b_kq.jsonl` (không có `src`).
- Mã r9 để chạy lại pilot: `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r10-6-codex/ma_r9_git` (clone đầy đủ, HEAD `c2d606b`, có commit base `8048551` cho ca `git archive`). Lệnh pilot của executor, chạy từ `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r10-6-codex/work`:
  `python3 <repo>/ops/reviews/wp1236-r10-soan/quet_dot_bien.py sinh /tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r10-6-codex/ma_r9_git/ops/gate_output_doi_chieu.py --ra m.jsonl`;
  `… hoi-quy <repo>/ops/reviews/wp1236-r10-soan/kho_dot_bien_reviewer_luot6.jsonl - /tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r10-6-codex/ma_r9_git/ops/gate_output_doi_chieu.py --ra h.jsonl`;
  `cat m.jsonl h.jsonl > all.jsonl`; `… chay all.jsonl /tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r10-6-codex/ma_r9_git/ops/gate_output_doi_chieu_test.py --ra kq.jsonl --song-song 4` (~45 phút trên 4 lõi). Có thể chạy một tập con có lý do.
- Hiện vật review mã r9 lượt 6: `git show refs/remotes/origin/ops/wp1236-r9-a-lease:ops/reviews/wp1236-a-r9-ma-6-codex/…`.
- `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r10-6-codex/ISSUE.md`; `CLAUDE.md`; `docs/PROTOCOL_DA_PHIEN.md` §8, §8.3, §12; `docs/adr/0044*`, `0053*`, `0055*`, `0060*`, `0067*`.

## Việc phải làm
0. **Nhãn cho MỌI lớp của vòng 5** (V01, V02 và các lớp lịch sử còn `VA_MOT_PHAN`): `DA_VA_THAT` · `VA_MOT_PHAN` · `CHUA_VA` · `KHONG_DO_DUOC`, kèm phép đo. Giữ slug; tách/gộp thì ghi `bang_noi_slug`.
1. **Bộ quét có đúng là thước đo tái lập được không**: tất định (sinh hai lần), mỗi mã toán tử làm đúng như docstring, bộ chạy giữ loader sản phẩm và phân hạng đúng (GIẾT chỉ khi `TinHieuChotCa`), hoi-quy tái dựng đúng 127 bản gốc, pilot tái hiện 25/25. Chạy lại ít nhất một phần pilot. Có toán tử nào bạn hay review lượt 6 dùng mà manifest không sinh được không? Có cách để executor làm xanh luật 3 mà không đóng lớp (vd lách bằng danh sách tương đương, bằng KHONG_AP_DUNG, bằng đổi test để đột biến chết vì lỗi vô can) không?
2. **Luật 4** route consumer đã đúng chưa; **luật 5** cách tái dẫn xuất trên head mới có lỗ không.
3. **Quét lớp** trước khi báo; **số tổng** (V02) đã đồng bộ chưa; khối `nang_tran` đề nghị 1700 có căn cứ đo không.
4. Nếu cách làm này vẫn không chống đỡ được bằng phép đo, nói thẳng (E1).

## Mức nghiêm trọng — §8 nguyên văn
`sensitive`: approve chỉ khi 0 P0/P1/P2 mở; **mỗi P3 phải đóng** (reviewer xác nhận có bằng chứng, hoặc chủ kho miễn neo exact SHA). Mỗi P2 trở lên phải có phép đo hoặc trích dẫn.

## Đầu ra — HAI tệp
1. `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r10-6-codex/work/VERDICT.json`, ghi tăng dần; kiểm bằng `python3 /tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r10-6-codex/kiem_verdict_lop.py /tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r10-6-codex/work/VERDICT.json --vong 6` (phải `HOP_LE`; lưu vào `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r10-6-codex/work/kiem_verdict.txt`). Khoá: `spec_sha256`, `vong`: 6, `findings` [`id` W01…, `class_slug`, `severity`, `vi_tri`, `van_de`, `bang_chung`, `de_xuat`], `class_table` [`slug`, `finding_ids`, `manifestations`, `highest_open_severity`, `nguon`, `common_fix`, `closing_check`, `ly_do_va_rieng`], `prior_class_status` [`slug`, `finding_cu`, `vong_xuat_hien`, `status`, `evidence`, `chua_do_duoc`], `bang_noi_slug`, `hoi_tu` {`vong5_sang_6`: "|F|/|U|", `lop_lap_lan_ba`: [...]}, `da_do_khop`, `verdict`.
2. `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r10-6-codex/work/VERDICT.md` — tóm tắt; dòng cuối `KET_LUAN: approve | changes_requested`.
