# Review offline MÃ — wp1236 đợt A theo đặc tả r12 — lượt 12 — reviewer độc lập, theo PROTOCOL §8.3 (ADR-0060 M12: review trước push)

Bạn là reviewer ĐỘC LẬP, read-only, cho MÃ của work packet `sensitive` wp1236 đợt A. Kho: ducthangho/tra-luat. Lời gọi Codex 13 của đợt A (chủ kho cấp thêm ngân sách khi cần, #1236 issuecomment-7063135049).

## Bối cảnh
Review mã lượt 9–11 trên r11 (`lich_su/VERDICT_ma_luot11.json`) không hội tụ ở lớp `test-thieu-chot` vì `\d`/`\s`/`\S`/`\w` là lớp Unicode. Chủ kho quyết E1 hai lần (issuecomment-7062234670, -7062521692) và duyệt đặc tả **r12** sha256 `4589daf1fd666b03a68b7d7dcd5c60903c10e946963fd324c9ee6185ed8e2dc7` (issuecomment-7063475061; review đặc tả vòng 15 approve, `lich_su/VERDICT_dac_ta_r12_vong15.json`). r12 ĐỔI LUẬT CỔNG: **luật 8** ngữ pháp ASCII đóng (+ sáu chỗ văn bản tự do có mệnh đề tường minh, oracle là kết quả TOÀN biểu thức sau tiền xử lý của tuyến); **luật 9** "test đủ" = mọi đột biến không tương đương của (A) manifest `quet_dot_bien.py do` (bản ghim sha256 `1b3e4a9e…`, 24 toán tử) ∪ (B) kho hồi quy cộng dồn — đều GIET/TUONG_DUONG có chứng minh/(B) KHONG_AP_DUNG theo luật 5; đột biến reviewer tự dựng NGOÀI (A)∪(B) ⇒ P3 `ngoai_bang_dong`; thứ tự xét duy nhất (B) → (A) → ngoài. ĐỌC luật 8–9 TRƯỚC khi xếp mức. Lease mới `wp1236-a-r12-g1-claude-20261121` (`LEASE.yaml`).

## Quyền
- CHỈ ĐỌC trong `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a12-12-codex/repo`. Không sửa, không commit, không push. Không gọi GitHub/mạng.
- Tạo tệp nháp CHỈ dưới `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a12-12-codex/work/`. Hướng thử đòi soạn nội dung tấn công thì MÔ TẢ BẰNG LỜI.

## Đầu vào
- Ứng viên: `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a12-12-codex/repo`, HEAD `9d8f600` (40 hex: `git rev-parse HEAD`). Base lease `010046f2141799ec6ffc9cfa1322d49df3f3f680`. So lượt 11: `git diff 0d81487 HEAD` (module: 10 regex sang lớp ASCII; test: a131 thay a129/a130, a132, thông điệp CLI nguyên văn, `khong_nem`, neo m20/m128/m129).
- Đặc tả `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a12-12-codex/SPEC.md` (kiểm sha256); tập ô `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a12-12-codex/bang_o.json`; lease `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a12-12-codex/LEASE.yaml`.
- Bằng chứng executor (`/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a12-12-codex/bang_chung/`), LỜI KHAI — đo lại:
  - `suite.log`: CA 47/47 · DOT BIEN 146/146 · TU KIEM DAT · TONG DAT.
  - `do.log` + `do/`: `quet_dot_bien.py do module test kho248.jsonl` ⇒ `HOAN_TAT`, TONG 993 · GIET 970 · SONG_SACH 23 · VO_CAN 0 · LOI_CHAY 0.
  - `kho248.jsonl` = kho 201 ID (lượt 6–11, sha256 `191225ca…`) + 47 cặp chuyển neo r12 (`kho_port_r12.jsonl`, `p12_*`).
  - `ledger_A_9d8f600.jsonl`: (A) 798 = 783 GIET + 15 TUONG_DUONG (chứng minh từng loại). `ledger_B_248_9d8f600.jsonl`: (B) 248 = 187 GIET · 8 TUONG_DUONG · 53 KHONG_AP_DUNG (20 → cặp thay thế cùng nghĩa GIET; 28 → CHOT_DA_BO vì nghĩa cũ nay chính là luật 8, kèm đối chứng NGƯỢC GIET; 5 giữ ledger cũ).
  - Bất biến (a): `git diff --check` 0; numstat +2014/−0 (trần 2100); `ci_dang_ky_test.py` TỔNG ĐẠT; ruff F sạch; `tl.py --selftest` 1770/1784 trên CẢ HEAD lẫn nền (các ca `wp433_gws_cred*` đỏ do môi trường), delta 0 — tự đo hai vế.
- Đọc thêm: `CLAUDE.md` · `docs/PROTOCOL_DA_PHIEN.md` §8, §8.3, §12 · `docs/adr/0060*`.

## Việc phải làm
0. **Nhãn cho MỌI lớp lượt 11** (S01, S02 và lớp lịch sử nối) — bốn nhãn §8.3, đo trên HEAD. Giữ slug.
1. **Mã khớp đặc tả r12**: mọi regex module đúng NGUYÊN VĂN mục *Module mới*; không còn `\d`/`\s`/`\S`/`\w`; hành vi `token` (casefold rồi match) và sáu chỗ văn bản tự do như đặc tả.
2. **Luật 8**: a131 oracle lấy từ regex đặc tả (không đọc module), đủ 128 ASCII + tập âm liệt kê ở mỗi vị trí, đúng tuyến (casefold ở token; JSON có Cs ở readback), cả hàm lá và consumer; ba đối chứng tách dòng lazy.
3. **Luật 9**: chạy lại `do` (hoặc đủ tập con để kiểm) — mẫu số, `HOAN_TAT`, từng TUONG_DUONG của (A), từng KHONG_AP_DUNG của (B) (nhất là 28 `CHOT_DA_BO`: nghĩa cũ có thật là luật r12 không; đối chứng ngược có đúng chiều không).
4. **Quét độc lập**: đột biến bạn tự dựng — phân hạng theo thứ tự luật 9: thuộc (B)? thuộc manifest (A)? còn lại ⇒ P3 `ngoai_bang_dong` (ghim cặp). Lỗi HÀNH VI của mã (khác đặc tả) là finding theo mức thật, không phải `ngoai_bang_dong`.
5. `python3 -B ops/gate_output_doi_chieu_test.py`; `ruff --select F`; `python3 -B .claude/dev/ci_dang_ky_test.py`; numstat so trần 2100; `git diff --check 010046f...HEAD`.

## Mức nghiêm trọng — §8 nguyên văn
`sensitive`: approve chỉ khi 0 P0/P1/P2 mở; **mỗi P3 phải đóng** (bạn xác nhận có bằng chứng, hoặc chủ kho miễn neo exact SHA). Mỗi P2+ phải có phép đo. P3 chờ miễn: ghi `chờ miễn chủ kho`; verdict `approve` chỉ khi điều kiện duy nhất còn lại là lời miễn ấy.

## Đầu ra — HAI tệp
1. `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a12-12-codex/work/VERDICT.json` ghi tăng dần; kiểm `python3 /tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a12-12-codex/kiem_verdict_lop.py /tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a12-12-codex/work/VERDICT.json --vong 12` (phải HOP_LE; lưu `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a12-12-codex/work/kiem_verdict.txt`). Khoá: `reviewed_sha`, `spec_sha256`, `vong`: 12, `findings` [`id` T01…, `class_slug`, `severity`, `vi_tri`, `van_de`, `bang_chung`, `de_xuat`], `class_table`, `prior_class_status` [`slug`, `finding_cu`, `luot_xuat_hien`, `status`, `evidence`, `chua_do_duoc`], `bang_noi_slug`, `hoi_tu` {`luot11_sang_12`: "|F|/|U|", `lop_lap_lan_ba`: [...]}, `da_do_khop`, `verdict`.
2. `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a12-12-codex/work/VERDICT.md` — tóm tắt; dòng cuối `KET_LUAN: approve | changes_requested`.
