# Review offline MÃ — wp1236 đợt A theo đặc tả r11 — lượt 10 — reviewer độc lập, theo PROTOCOL §8.3 (ADR-0060 M12: review trước push)

Bạn là reviewer ĐỘC LẬP, read-only, cho MÃ của work packet `sensitive` wp1236 đợt A. Kho: ducthangho/tra-luat. Đây là lời gọi Codex 11/12 của đợt A (chủ kho nâng trần 10 → 12, #1236 issuecomment-7060159910).

## Bối cảnh
Lượt 9 (`lich_su/VERDICT_ma_luot9.json`, `2719f81`): changes_requested, hội tụ 8→9 = 1/2 — P01 P2 `test-thieu-chot` (luật 4: 10 đột biến `r9b_*` — `\d`/`\s` Unicode, `landed_<8 số>`, khoảng trắng đầu/sau token — chưa qua consumer), P02 P2 (bộ máy ô chưa đọc đầu vào từ `hat_giong`), P03 P3 `ngoai_bang_dong` (`r9b_event_tab`, `r9b_name_inner_spaces`). Chủ kho quyết: vá P01/P02 trong phạm vi đặc tả r11 đã duyệt (không đổi tập ô), và đồng ý MIỄN P03 theo ADR-0060 M1 neo exact SHA sau vá (comment miễn chưa đăng — chờ verdict này). Đặc tả r11 (sha256 `30386131…`) và lease `wp1236-a-r11-g1-claude-20261121` không đổi.

## Quyền
- CHỈ ĐỌC trong `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a11-10-codex/repo`. Không sửa, không commit, không push. Không gọi GitHub/mạng.
- Tạo tệp nháp/script/bản sao đột biến CHỈ dưới `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a11-10-codex/work/`. Hướng thử đòi soạn nội dung tấn công thì MÔ TẢ BẰNG LỜI.

## Đầu vào
- Ứng viên: `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a11-10-codex/repo`, HEAD `9c17a34` (40 hex: `git rev-parse HEAD`). Base lease `010046f2141799ec6ffc9cfa1322d49df3f3f680`. Diff: `git diff 010046f...HEAD` (3 tệp). So lượt 9: `git diff 2719f81 HEAD` (CHỈ tệp test; mã sản phẩm byte-bằng `79b3c24`).
- Đặc tả `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a11-10-codex/SPEC.md` (kiểm sha256 `30386131d8017bf982ca0be7707c8d5fd3035e9586c5f94a446f45c40fc863d1`); tập ô `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a11-10-codex/bang_o.json`; lease `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a11-10-codex/LEASE.yaml`.
- Bằng chứng executor (`/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a11-10-codex/bang_chung/`), là LỜI KHAI — đo lại:
  - `suite.log`: CA 46/46 · DOT BIEN 146/146 · TU KIEM DAT · TONG DAT (Linux, Python 3.13.18).
  - `ledger_kho_167_9c17a34.jsonl`: luật 5 trên kho cộng dồn 167 ID (`kho_dot_bien_luot6_7_8_9.jsonl` = 152 + 15 của lượt 9): 153 GIET · 7 TUONG_DUONG · 5 KHONG_AP_DUNG · 2 NGOAI_BANG_DONG (đúng hai ID P03, chờ chủ kho miễn). Kết quả `kq167.jsonl`.
  - `ledger_hang_45.jsonl` (luật 6). Bất biến (a): `git diff --check` 0; numstat +1850/−0 (trần 2100); `ci_dang_ky_test.py` TỔNG ĐẠT. `tl.py --selftest` = 1770/1784 trên CẢ `9c17a34` LẪN nền `2719f81` trong môi trường hiện tại (`selftest_9c17a34.log`: các ca `wp433_gws_cred*`/`wp433_nlm_gws*` đỏ do môi trường sau khi phiên khởi động lại; lượt 9 đo 1784/1784 ở môi trường trước) — delta = 0, hãy tự đo lại cả hai vế.
- Đọc thêm: `CLAUDE.md` · `docs/PROTOCOL_DA_PHIEN.md` §8, §8.3, §12 · `docs/adr/0060*`.

## Việc phải làm
0. **Nhãn cho MỌI lớp lượt 9** (P01, P02, P03 và lớp lịch sử nối) — bốn nhãn §8.3, đo trên HEAD. Giữ slug. P03: xác nhận hai đột biến vẫn đúng là `ngoai_bang_dong` (P3), không nâng hạng.
1. **P01**: `a129` phủ đủ mười `r9b_*` qua hàm lá VÀ `kiem_ho_so`; còn biến thể nào CÙNG MIỀN ngữ pháp luật 4 (lớp ký tự Unicode của `\d`, `\s`) mà vẫn sống không.
2. **P02**: `chay_o` đọc byte fixture, thư mục, tên tương đối và hai mẫu hồ sơ consumer từ `hat_giong`; thay hạt giống bằng nguồn khác có băm hợp lệ thì kết quả đổi theo.
3. **Quét độc lập** (bắt buộc): phân hạng từng đột biến sống theo luật 6 (luật bị vi phạm hoặc `id` ô, hoặc `ngoai_bang_dong` P3). Ghim kho mới thành cặp.
4. Luật 5: kiểm ledger 167 ID.
5. `python3 -B ops/gate_output_doi_chieu_test.py`; `ruff --select F` ba tệp; `python3 -B .claude/dev/ci_dang_ky_test.py`; numstat so trần 2100; `git diff --check 010046f...HEAD`.

## Mức nghiêm trọng — §8 nguyên văn
`sensitive`: approve chỉ khi 0 P0/P1/P2 mở; **mỗi P3 phải đóng** (bạn xác nhận có bằng chứng, hoặc chủ kho miễn neo exact SHA). Mỗi P2+ phải có phép đo. P3 chờ miễn: ghi rõ trong verdict là `chờ miễn chủ kho`, verdict `approve` chỉ khi mọi thứ khác sạch và điều kiện duy nhất còn lại là lời miễn ấy.

## Đầu ra — HAI tệp
1. `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a11-10-codex/work/VERDICT.json` ghi tăng dần; kiểm `python3 /tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a11-10-codex/kiem_verdict_lop.py /tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a11-10-codex/work/VERDICT.json --vong 10` (phải HOP_LE; lưu `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a11-10-codex/work/kiem_verdict.txt`). Khoá: `reviewed_sha`, `spec_sha256`, `vong`: 10, `findings` [`id` Q01…, `class_slug`, `severity`, `vi_tri`, `van_de`, `bang_chung`, `de_xuat`], `class_table`, `prior_class_status` [`slug`, `finding_cu`, `luot_xuat_hien`, `status`, `evidence`, `chua_do_duoc`], `bang_noi_slug`, `hoi_tu` {`luot9_sang_10`: "|F|/|U|", `lop_lap_lan_ba`: [...]}, `da_do_khop`, `verdict`.
2. `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a11-10-codex/work/VERDICT.md` — tóm tắt; dòng cuối `KET_LUAN: approve | changes_requested`.
