# Review offline MÃ — wp1236 đợt A theo đặc tả r10 — lượt 7 — reviewer độc lập, theo PROTOCOL §8.3 (ADR-0060 M12: review trước push)

Bạn là reviewer ĐỘC LẬP, read-only, cho MÃ của work packet `sensitive` wp1236 đợt A. Kho: ducthangho/tra-luat.

## Bối cảnh
Đợt A r9 dừng ở Review Rescue Checkpoint sau lượt 6 (`lich_su/VERDICT_ma_luot6.json`: L01 P2, L02 P3 thuộc `test-thieu-chot`; L03 P3 `mo-ta-duong-dan-lech-hop-dong`). Đặc tả r10 (sha256 `3ee831738c70c5eabb27720e295b4953c9a9bdd1ac29a03cc7b964d28658fcdc`, chủ kho duyệt; review vòng 8 approve) đổi nghiệm thu: luật 1, 2, 4, 5 BẮT BUỘC; luật 3 (bộ quét) là công cụ khuyến nghị; reviewer mã tự quét độc lập. Thi công lại trên lease `wp1236-a-r10-g1-claude-20261121` (trần ≤ 3 tệp / ≤ 1700 dòng). Lượt 1–5 không theo §8.3; lớp `test-thieu-chot` đã nối với `nghiem-thu-khong-co-lap-chot-dich` ở mức đặc tả. Đính chính lịch sử: hội tụ 4→5 của mã là `KHONG_DO_DUOC`, không phải 0/1.

## Quyền
- CHỈ ĐỌC trong `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a10-7-codex/repo`. Không sửa, không commit, không push. Không gọi GitHub/mạng.
- Tạo tệp nháp/script/bản sao đột biến CHỈ dưới `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a10-7-codex/work/`. Hướng thử đòi soạn nội dung tấn công thì MÔ TẢ BẰNG LỜI.

## Đầu vào
- Ứng viên: `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a10-7-codex/repo`, HEAD `f4f17bc` (đủ 40 hex: `git rev-parse HEAD`). Base `origin/master` `010046f2141799ec6ffc9cfa1322d49df3f3f680`. Diff: `git diff 010046f...HEAD` (3 tệp). So với mã r9 `c2d606b` (lượt 6 review): `git diff c2d606b HEAD -- ops/` (c2d606b có trong kho).
- Đặc tả `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a10-7-codex/SPEC.md` (kiểm sha256 trước; lệch thì dừng). Lease `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a10-7-codex/LEASE.yaml`.
- Bằng chứng executor (`/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a10-7-codex/bang_chung/`), là LỜI KHAI — đo lại:
  - `quet_do_1db0ae5_kq.jsonl` + `quet_do_1db0ae5_out.txt`: lượt `do` của bộ quét (công cụ khuyến nghị) trên commit TRƯỚC `1db0ae5`: 916 = 871 giết / 41 sống sạch / 4 lỗi vô can, HOAN_TAT. `phan_loai_41_song_1db0ae5.jsonl`: phân loại 41 (28 tương đương có lý do, 10 đã rút gọn mã ở f4f17bc, 3 đã thêm ca).
  - `ledger_kho_127_f4f17bc.jsonl`: ledger luật 5 đủ 127 ID trên f4f17bc (115 GIET, 7 TUONG_DUONG, 5 KHONG_AP_DUNG kèm thay thế); kết quả chạy `kho_va_thay_the_f4f17bc_kq.jsonl`.
  - Bộ quét `quet_dot_bien.py` và kho `kho_dot_bien_reviewer_luot6.jsonl` (bản ghim trên nhánh đặc tả). Lệnh: `python3 quet_dot_bien.py do <module> <test> <kho> --thu-muc-ra <thư mục>` (~90 phút / 4 lõi, Python 3.13) — dùng hay không tuỳ bạn.
- Đọc thêm: `CLAUDE.md` · `docs/PROTOCOL_DA_PHIEN.md` §8, §8.3, §12 · `ops/kiem_ho_so_land.py` · `.claude/dev/packet_loop.py` (`CHECK_BAT_BUOC`).

## Việc phải làm
0. **Nhãn cho MỌI lớp lượt 6** (và lịch sử nối) — bốn nhãn §8.3, kèm phép đo trên HEAD. Giữ slug.
1. **Nghiệm thu bắt buộc r10**: luật 1 (mỗi lý do cố định: ca đích + đối chứng + đột biến riêng chết vì `TinHieuChotCa` của đúng ca), luật 2 (năm ô trùng ID), luật 4 (ma trận nghĩa qua đúng consumer: hàm lá + `kiem_ho_so` với `head=None`; `head` khác None qua `kiem_mien` trực tiếp), luật 5 (ledger 127 ID: kiểm từng KHONG_AP_DUNG và từng TUONG_DUONG). Mục *Module mới* của đặc tả (K1–K8, tên lý do, CLI và mẫu đầu ra cố định).
2. **Quét độc lập của bạn** (bắt buộc theo r10): tự dựng toán tử ngoài bộ quét của executor; mỗi đột biến sống không tương đương là finding theo §8. Soi các chỗ rút gọn mã ở f4f17bc/1db0ae5 (bỏ lookbehind RE_TEP_DG, nhãn skip thành bool, `.decode()` mặc định, `".." in pp.parts`, bỏ `"moc": None`, tính moc theo n/so_pass) có đổi hành vi không.
3. Lời khai dương sai / chặn oan trên `ops/land/**` tại base `8048551` (47/10/9; 25/56/39/50; 94/170 landed lệch 0).
4. `python3 -B ops/gate_output_doi_chieu_test.py` (khai: CA 40/40 · DOT BIEN 145/145 · TU KIEM DAT · TONG DAT); `ruff --select F` ba tệp; `python3 -B .claude/dev/ci_dang_ky_test.py`; `git diff --numstat 010046f...HEAD` so trần 1700; `git diff --check`.

## Mức nghiêm trọng — §8 nguyên văn
`sensitive`: approve chỉ khi 0 P0/P1/P2 mở; **mỗi P3 phải đóng** (bạn xác nhận có bằng chứng, hoặc chủ kho miễn neo exact SHA). Mỗi P2+ phải có phép đo.

## Đầu ra — HAI tệp
1. `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a10-7-codex/work/VERDICT.json` ghi tăng dần; kiểm `python3 /tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a10-7-codex/kiem_verdict_lop.py /tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a10-7-codex/work/VERDICT.json --vong 7` (phải HOP_LE; lưu `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a10-7-codex/work/kiem_verdict.txt`). Khoá: `reviewed_sha`, `spec_sha256`, `vong`: 7, `findings` [`id` M01…, `class_slug`, `severity`, `vi_tri`, `van_de`, `bang_chung`, `de_xuat`], `class_table`, `prior_class_status` [`slug`, `finding_cu`, `luot_xuat_hien`, `status`, `evidence`, `chua_do_duoc`], `bang_noi_slug`, `hoi_tu` {`luot6_sang_7`: "|F|/|U|", `lop_lap_lan_ba`: [...]}, `da_do_khop`, `verdict`.
2. `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a10-7-codex/work/VERDICT.md` — tóm tắt; dòng cuối `KET_LUAN: approve | changes_requested`.
