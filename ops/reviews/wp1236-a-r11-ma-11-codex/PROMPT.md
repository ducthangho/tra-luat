# Review offline MÃ — wp1236 đợt A theo đặc tả r11 — lượt 11 — reviewer độc lập, theo PROTOCOL §8.3 (ADR-0060 M12: review trước push)

Bạn là reviewer ĐỘC LẬP, read-only, cho MÃ của work packet `sensitive` wp1236 đợt A. Kho: ducthangho/tra-luat. Đây là lời gọi Codex **12/12 — CUỐI** của đợt A (trần nâng ở #1236 issuecomment-7060159910).

## Bối cảnh
Lượt 10 (`lich_su/VERDICT_ma_luot10.json`, `9c17a34`): changes_requested, hội tụ 9→10 = 0/1 — Q01 P2 `test-thieu-chot` (luật 4: 16 đột biến — `\d`/`\s`/`\S` là lớp UNICODE; chữ số Unicode ở URL/ngày miễn, khoảng trắng Unicode ở URL/lý do, xuống dòng ở token, khối Nd khác), Q02 P3 = P03 cũ (`r9b_event_tab`, `r9b_name_inner_spaces`, `ngoai_bang_dong`, chủ kho đồng ý miễn neo exact SHA — comment miễn CHƯA đăng, chờ verdict này). Chủ kho quyết E1 (#1236 issuecomment-7060894032): PHỦ VÉT CẠN lớp ký tự trong test, không đổi đặc tả, không đổi mã sản phẩm. Đặc tả r11 (`30386131…`) và lease `wp1236-a-r11-g1-claude-20261121` không đổi.

## Quyền
- CHỈ ĐỌC trong `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a11-11-codex/repo`. Không sửa, không commit, không push. Không gọi GitHub/mạng.
- Tạo tệp nháp/script/bản sao đột biến CHỈ dưới `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a11-11-codex/work/`. Hướng thử đòi soạn nội dung tấn công thì MÔ TẢ BẰNG LỜI.

## Đầu vào
- Ứng viên: `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a11-11-codex/repo`, HEAD `0d81487` (40 hex: `git rev-parse HEAD`). Base lease `010046f2141799ec6ffc9cfa1322d49df3f3f680`. Diff: `git diff 010046f...HEAD`. So lượt 10: `git diff 9c17a34 HEAD` (CHỈ tệp test: ca `a130_lop_unicode_vet_can`; mã sản phẩm byte-bằng `79b3c24`).
- Đặc tả `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a11-11-codex/SPEC.md` (sha256 `30386131d8017bf982ca0be7707c8d5fd3035e9586c5f94a446f45c40fc863d1`); tập ô `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a11-11-codex/bang_o.json`; lease `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a11-11-codex/LEASE.yaml`.
- Bằng chứng executor (`/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a11-11-codex/bang_chung/`), là LỜI KHAI — đo lại:
  - `suite.log`: CA 47/47 · DOT BIEN 146/146 · TU KIEM DAT · TONG DAT.
  - `ledger_kho_186_0d81487.jsonl`: luật 5 trên kho cộng dồn 186 ID (`kho_dot_bien_luot6_7_8_9_10.jsonl`): 172 GIET · 7 TUONG_DUONG · 5 KHONG_AP_DUNG · 2 NGOAI_BANG_DONG (đúng hai ID P03/Q02). `kq.jsonl`.
  - a130: hàm lá `doc_danh_gia` trên MỌI 680 ký tự Nd ở 7 vị trí `\d` và MỌI 138 558 ký tự `\w` ở `conclusion`; consumer trên fixture thật với 67 khối Nd gán vòng (giữ giá trị) ở run/attempt/job id/dòng tổng/skipped cũ/skipped v3; `landed_<8 \d>` và token `\s` (29 ký tự) MỌI ký tự qua cả hai tuyến; URL id `\d` mọi Nd, ngày miễn mọi Nd không-ASCII (⇒ `han`), `\s` trong đường URL và đầu lý do (⇒ `url`/`dong_mien`), đại diện `\S` mỗi general category (⇒ []).
  - Bất biến (a): `git diff --check` 0; numstat +1985/−0 (trần 2100); `ci_dang_ky_test.py` TỔNG ĐẠT; ruff F sạch. `tl.py --selftest` = 1770/1784 trên CẢ HEAD lẫn nền `2719f81` ở môi trường hiện tại (các ca `wp433_gws_cred*`/`wp433_nlm_gws*`), delta = 0 — tự đo lại hai vế.
- Đọc thêm: `CLAUDE.md` · `docs/PROTOCOL_DA_PHIEN.md` §8, §8.3, §12 · `docs/adr/0060*`.

## Việc phải làm
0. **Nhãn cho MỌI lớp lượt 10** (Q01, Q02 và lớp lịch sử nối) — bốn nhãn §8.3, đo trên HEAD. Giữ slug. Q02: xác nhận hai đột biến vẫn đúng `ngoai_bang_dong` (P3).
1. **Q01**: a130 có thật sự vét cạn mọi vị trí `\d`/`\s`/`\S`/`\w` của MỌI regex trong `ops/gate_output_doi_chieu.py` (tự liệt kê từ mã) qua hàm lá VÀ consumer không; còn vị trí/lớp nào sót.
2. **Quét độc lập** (bắt buộc): phân hạng từng đột biến sống theo luật 6 (luật bị vi phạm hoặc `id` ô, hoặc `ngoai_bang_dong` P3). Ghim kho mới thành cặp.
3. Luật 5: kiểm ledger 186 ID.
4. `python3 -B ops/gate_output_doi_chieu_test.py`; `ruff --select F` ba tệp; `python3 -B .claude/dev/ci_dang_ky_test.py`; numstat so trần 2100; `git diff --check 010046f...HEAD`.

## Mức nghiêm trọng — §8 nguyên văn
`sensitive`: approve chỉ khi 0 P0/P1/P2 mở; **mỗi P3 phải đóng** (bạn xác nhận có bằng chứng, hoặc chủ kho miễn neo exact SHA). Mỗi P2+ phải có phép đo. P3 chờ miễn: ghi rõ `chờ miễn chủ kho`; verdict `approve` chỉ khi mọi thứ khác sạch và điều kiện duy nhất còn lại là lời miễn ấy.

## Đầu ra — HAI tệp
1. `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a11-11-codex/work/VERDICT.json` ghi tăng dần; kiểm `python3 /tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a11-11-codex/kiem_verdict_lop.py /tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a11-11-codex/work/VERDICT.json --vong 11` (phải HOP_LE; lưu `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a11-11-codex/work/kiem_verdict.txt`). Khoá: `reviewed_sha`, `spec_sha256`, `vong`: 11, `findings` [`id` S01…, `class_slug`, `severity`, `vi_tri`, `van_de`, `bang_chung`, `de_xuat`], `class_table`, `prior_class_status` [`slug`, `finding_cu`, `luot_xuat_hien`, `status`, `evidence`, `chua_do_duoc`], `bang_noi_slug`, `hoi_tu` {`luot10_sang_11`: "|F|/|U|", `lop_lap_lan_ba`: [...]}, `da_do_khop`, `verdict`.
2. `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a11-11-codex/work/VERDICT.md` — tóm tắt; dòng cuối `KET_LUAN: approve | changes_requested`.
