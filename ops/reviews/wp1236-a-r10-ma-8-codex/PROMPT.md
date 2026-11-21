# Review offline MÃ — wp1236 đợt A theo đặc tả r10 — lượt 8 — reviewer độc lập, theo PROTOCOL §8.3 (ADR-0060 M12: review trước push)

Bạn là reviewer ĐỘC LẬP, read-only, cho MÃ của work packet `sensitive` wp1236 đợt A. Kho: ducthangho/tra-luat.

## Bối cảnh
Lượt 7 (`lich_su/VERDICT_ma_luot7.json`, review trên `f4f17bc`) ra changes_requested: M01 P2 `test-thieu-chot` (14/15 đột biến độc lập sống; reviewer ghi đây là lớp lặp ≥3 lượt, đòi đổi PHƯƠNG PHÁP chứ không vá từng ví dụ), M02 P3 (argparse in `usage:`; đã vá ở `79b3c24`), M03 P3 (ledger). Lời miễn M01/M03 của chủ kho neo `79b3c24` KHÔNG còn hiệu lực cho HEAD này (SHA khác; và ADR-0060 M1 chỉ cho miễn P3). Chủ kho chọn VÁ M01.
Windows local (ADR-0057) tại `79b3c24` trên máy chủ kho đỏ: a117 tạo thư mục tên `con` (tên thiết bị dành riêng Windows, WinError 267); 13 đột biến sống vì ca đích chỉ chạy trên POSIX. Đây là lỗi của bộ test, mã sản phẩm không đổi.
Đặc tả r10 sha256 `3ee831738c70c5eabb27720e295b4953c9a9bdd1ac29a03cc7b964d28658fcdc`: luật 1, 2, 4, 5 BẮT BUỘC; luật 3 là công cụ khuyến nghị; reviewer mã tự quét độc lập.

## Quyền
- CHỈ ĐỌC trong `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a10-8-codex/repo`. Không sửa, không commit, không push. Không gọi GitHub/mạng.
- Tạo tệp nháp/script/bản sao đột biến CHỈ dưới `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a10-8-codex/work/`. Hướng thử đòi soạn nội dung tấn công thì MÔ TẢ BẰNG LỜI.

## Đầu vào
- Ứng viên: `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a10-8-codex/repo`, HEAD `5a1bf33` (đủ 40 hex: `git rev-parse HEAD`). Base lease `010046f2141799ec6ffc9cfa1322d49df3f3f680`. Diff: `git diff 010046f...HEAD` (3 tệp). Thay đổi của lượt này: `git diff 79b3c24 HEAD` (CHỈ `ops/gate_output_doi_chieu_test.py`; mã sản phẩm `ops/gate_output_doi_chieu.py` giữ nguyên byte so với `79b3c24`/`f4f17bc` trừ M02).
- Đặc tả `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a10-8-codex/SPEC.md` (kiểm sha256; lệch thì dừng). Lease `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a10-8-codex/LEASE.yaml`.
- Bằng chứng executor (`/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a10-8-codex/bang_chung/`), là LỜI KHAI — đo lại:
  - `suite.log`: `python -B ops/gate_output_doi_chieu_test.py` → CA 42/42 · DOT BIEN 146/146 · TU KIEM DAT · TONG DAT (Linux, Python 3.13.18).
  - `ledger_kho_141_5a1bf33.jsonl`: ledger luật 5 trên kho cộng dồn `kho_dot_bien_reviewer_luot6_va7.jsonl` (141 ID = 127 lượt 6 + 14 lượt 7): 129 GIET (kèm ca) · 7 TUONG_DUONG (lý do chép từ ledger lượt 7 vì mã sản phẩm không đổi — tự kiểm) · 5 KHONG_AP_DUNG kèm thay thế. Cả 14 ID `r7_*` GIET. Kết quả chạy `kq141.jsonl` (`quet_dot_bien.py hoi-quy` rồi `chay`).
- Đọc thêm: `CLAUDE.md` · `docs/PROTOCOL_DA_PHIEN.md` §8, §8.3, §12 · `docs/adr/0057-windows-local-may-chu-kho.md`.

## Việc phải làm
0. **Nhãn cho MỌI lớp lượt 7** (M01 `test-thieu-chot`, M02, M03 và lớp lịch sử nối) — bốn nhãn §8.3, kèm phép đo trên HEAD. Giữ slug.
1. **Đổi phương pháp M01 có thật không**: ca `a124_danh_tinh_chinh_xac_provenance` (bảng mọi trường so chính xác × họ biến đổi hoa/thường, khoảng trắng đầu, khoảng trắng cuối; hàm lá VÀ `kiem_ho_so`), `a125_day_url_va_ngu_phap_consumer` (dãy labels đảo/lặp/thiếu, URL lặp, dấu phân cách và `./` qua consumer, ba trường readback), bổ sung `a210_cli` (fixture thứ sáu T-khong-prov, tiền tố `GIỚI HẠN:`, stem dự phòng). Kiểm: bảng có ĐỦ mọi phép so `==`/`!=`/`in` trên chuỗi danh tính trong mã sản phẩm không (tự liệt kê từ mã, đừng tin bảng); ngoài họ biến đổi đã chọn còn họ chuẩn hoá nào khác (Unicode NFC/NFKC, tiền tố/hậu tố, `startswith`, `in` chuỗi con…) mà mã phải chặn mà bảng không chặn.
2. **Windows**: vá a117 (`conx`), tách a204, tập `CHI_POSIX` (11 đột biến bị bỏ qua có khai báo khi `os.name != "posix"`, mẫu số trừ đi và in ra). Kiểm: tập ấy có đúng là chỉ các đột biến mà ca đích THẬT SỰ không đo được ngoài POSIX không; trên POSIX nó có làm yếu gì không (đột biến `CHI_POSIX` ghi tên lạ phải đỏ); có cách nào làm TONG DAT giả trên Windows không.
3. **Quét độc lập của bạn** (bắt buộc theo r10) trên HEAD: tự dựng toán tử ngoài bộ quét của executor; mỗi đột biến sống không tương đương là finding theo §8. Ghim kho mới thành cặp như luật 5.
4. Luật 5: kiểm ledger 141 ID (đặc biệt 7 TUONG_DUONG và 5 KHONG_AP_DUNG).
5. `python3 -B ops/gate_output_doi_chieu_test.py`; `ruff --select F` ba tệp; `python3 -B .claude/dev/ci_dang_ky_test.py`; `git diff --numstat 010046f...HEAD` so trần 1700; `git diff --check 010046f...HEAD`.

## Mức nghiêm trọng — §8 nguyên văn
`sensitive`: approve chỉ khi 0 P0/P1/P2 mở; **mỗi P3 phải đóng** (bạn xác nhận có bằng chứng, hoặc chủ kho miễn neo exact SHA). Mỗi P2+ phải có phép đo.

## Đầu ra — HAI tệp
1. `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a10-8-codex/work/VERDICT.json` ghi tăng dần; kiểm `python3 /tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a10-8-codex/kiem_verdict_lop.py /tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a10-8-codex/work/VERDICT.json --vong 8` (phải HOP_LE; lưu `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a10-8-codex/work/kiem_verdict.txt`). Khoá: `reviewed_sha`, `spec_sha256`, `vong`: 8, `findings` [`id` N01…, `class_slug`, `severity`, `vi_tri`, `van_de`, `bang_chung`, `de_xuat`], `class_table`, `prior_class_status` [`slug`, `finding_cu`, `luot_xuat_hien`, `status`, `evidence`, `chua_do_duoc`], `bang_noi_slug`, `hoi_tu` {`luot7_sang_8`: "|F|/|U|", `lop_lap_lan_ba`: [...]}, `da_do_khop`, `verdict`.
2. `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a10-8-codex/work/VERDICT.md` — tóm tắt; dòng cuối `KET_LUAN: approve | changes_requested`.
