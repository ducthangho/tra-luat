# Review offline MÃ — wp1236 đợt A theo đặc tả r11 — lượt 9 — reviewer độc lập, theo PROTOCOL §8.3 (ADR-0060 M12: review trước push)

Lưu ý: đây là lần chạy lại của lượt 9 — lần đầu bị cắt giữa chừng khi tiến trình phiên khởi động lại (không có kết luận). Tệp trung gian của lần đầu ở `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a11-9b-codex/bang_chung/luot9_bi_cat/` là LỜI KHAI, đo lại trước khi dùng. Đây là lời gọi Codex 10/10 (CUỐI) của đợt A.

Bạn là reviewer ĐỘC LẬP, read-only, cho MÃ của work packet `sensitive` wp1236 đợt A. Kho: ducthangho/tra-luat.

## Bối cảnh
Lượt 8 (`lich_su/VERDICT_ma_luot8.json`, `5a1bf33`): changes_requested — N01 P2 `test-thieu-chot` (11 đột biến độc lập mới sống), N02 P3 (ledger `identity_72_67`/`ref_no_boundary`), N03 P2 `hop-dong-dau-vao-dau-ra-chua-chot` (đầu ra nhánh Windows lệch regex consumer). Chủ kho quyết E1: ĐÓNG MIỀN bằng đặc tả r11. Đặc tả r11 bản sửa 2 (sha256 `30386131d8017bf982ca0be7707c8d5fd3035e9586c5f94a446f45c40fc863d1`) được review đặc tả vòng 11 APPROVE (`lich_su/VERDICT_dac_ta_r11_vong11.json`) và chủ kho duyệt băm + trần 2100 dòng (#1236 issuecomment-7058143773). Lease mới `wp1236-a-r11-g1-claude-20261121` (`LEASE.yaml`).
Đặc tả r11 thêm luật 6 (tập 125 ô ĐÓNG có băm `628e2704…` phủ hạt giống + phép chiếu; thứ tự ưu tiên luật 1/2/4/5 trước luật 6; đột biến sống mà một ô của tập phân biệt được ⇒ P2, không ô nào phân biệt ⇒ P3 `ngoai_bang_dong`), luật 7 (bốn dòng tổng kết liền nhau đúng regex trên mọi nền + ca tự kiểm producer→consumer), dạng ledger `KHONG_AP_DUNG → <id> TUONG_DUONG`, `tep_danh_gia` theo token tối đại (lookbehind không bắt buộc), seam độc lập nền. ĐỌC phân hạng của luật 6 TRƯỚC khi xếp mức finding cho đột biến sống.

## Quyền
- CHỈ ĐỌC trong `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a11-9b-codex/repo`. Không sửa, không commit, không push. Không gọi GitHub/mạng.
- Tạo tệp nháp/script/bản sao đột biến CHỈ dưới `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a11-9b-codex/work/`. Hướng thử đòi soạn nội dung tấn công thì MÔ TẢ BẰNG LỜI.

## Đầu vào
- Ứng viên: `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a11-9b-codex/repo`, HEAD `2719f81` (đủ 40 hex: `git rev-parse HEAD`). Base lease `010046f2141799ec6ffc9cfa1322d49df3f3f680`. Diff: `git diff 010046f...HEAD` (3 tệp). So lượt 8: `git diff 5a1bf33 HEAD` (CHỈ tệp test; mã sản phẩm `ops/gate_output_doi_chieu.py` byte-bằng `79b3c24`).
- Đặc tả `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a11-9b-codex/SPEC.md` (kiểm sha256; lệch thì dừng); tập ô `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a11-9b-codex/bang_o.json`. Lease `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a11-9b-codex/LEASE.yaml`.
- Bằng chứng executor (`/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a11-9b-codex/bang_chung/`), là LỜI KHAI — đo lại:
  - `suite.log` (Linux, Python 3.13.18): CA 45/45 · DOT BIEN 146/146 · TU KIEM DAT · TONG DAT.
  - `ledger_kho_152_2719f81.jsonl`: luật 5 trên kho cộng dồn 152 ID (`kho_dot_bien_reviewer_luot6_7_8.jsonl`): 140 GIET kèm ca · 7 TUONG_DUONG · 5 KHONG_AP_DUNG (gồm `identity_72_67` dạng → TUONG_DUONG và `ref_no_boundary` → CHOT_DA_BO theo r11). Kết quả `kq152.jsonl`.
  - `ledger_hang_45.jsonl`: ledger hàng của luật 6 (21 hàng có ô, 24 hàng `ngu_phap`; 125/125 ô được trỏ).
  - Bất biến (a) trên 2719f81: `tl.py --selftest` 1784/1784, `git diff --check` 0; numstat +1795/−0 (trần 2100); `ci_dang_ky_test.py` TỔNG ĐẠT.
- Đọc thêm: `CLAUDE.md` · `docs/PROTOCOL_DA_PHIEN.md` §8, §8.3, §12 · `docs/adr/0057-windows-local-may-chu-kho.md` · `docs/adr/0060*`.

## Việc phải làm
0. **Nhãn cho MỌI lớp lượt 8** (N01, N02, N03 và lớp lịch sử nối) — bốn nhãn §8.3, đo trên HEAD. Giữ slug.
1. **Luật 6**: `bang_o()` sinh đúng tệp `bang_o.json` và băm `BAM_BANG_O`; mọi đầu vào gốc đọc từ `hat_giong`; mỗi ô chạy qua hàm lá VÀ consumer với kỳ vọng âm chính xác; ledger hàng đúng.
2. **Luật 7 + seam**: `a127` thật sự đưa đầu ra `main()` qua `chay_moi` hai chế độ nền với bốn đối chứng đỏ; `a128` đo m65/m79 không cần POSIX; `CHI_POSIX` chỉ còn ca cần symlink thật.
3. **Quét độc lập** (bắt buộc): tự dựng đột biến ngoài kho; với MỖI đột biến sống không tương đương, phân hạng theo luật 6 (ghi luật bị vi phạm hoặc `id` ô phân biệt, hoặc `ngoai_bang_dong` P3). Ghim kho mới thành cặp (luật 5).
4. Luật 5: kiểm ledger 152 ID (7 TUONG_DUONG, 5 KHONG_AP_DUNG).
5. `python3 -B ops/gate_output_doi_chieu_test.py`; `ruff --select F` ba tệp; `python3 -B .claude/dev/ci_dang_ky_test.py`; `git diff --numstat 010046f...HEAD` so trần 2100; `git diff --check 010046f...HEAD`.

## Mức nghiêm trọng — §8 nguyên văn
`sensitive`: approve chỉ khi 0 P0/P1/P2 mở; **mỗi P3 phải đóng** (bạn xác nhận có bằng chứng, hoặc chủ kho miễn neo exact SHA). Mỗi P2+ phải có phép đo.

## Đầu ra — HAI tệp
1. `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a11-9b-codex/work/VERDICT.json` ghi tăng dần; kiểm `python3 /tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a11-9b-codex/kiem_verdict_lop.py /tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a11-9b-codex/work/VERDICT.json --vong 9` (phải HOP_LE; lưu `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a11-9b-codex/work/kiem_verdict.txt`). Khoá: `reviewed_sha`, `spec_sha256`, `vong`: 9, `findings` [`id` P01…, `class_slug`, `severity`, `vi_tri`, `van_de`, `bang_chung`, `de_xuat`], `class_table`, `prior_class_status` [`slug`, `finding_cu`, `luot_xuat_hien`, `status`, `evidence`, `chua_do_duoc`], `bang_noi_slug`, `hoi_tu` {`luot8_sang_9`: "|F|/|U|", `lop_lap_lan_ba`: [...]}, `da_do_khop`, `verdict`.
2. `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a11-9b-codex/work/VERDICT.md` — tóm tắt; dòng cuối `KET_LUAN: approve | changes_requested`.
