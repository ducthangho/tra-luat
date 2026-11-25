# Review ĐẶC TẢ wp1236 r10 bản sửa 3 — vòng 8 — reviewer độc lập, theo PROTOCOL §8.3

Bạn là reviewer ĐỘC LẬP cho một ĐẶC TẢ packet (không phải mã), review class `sensitive`. Kho: ducthangho/tra-luat.

## Bối cảnh
Vòng 7 (`lich_su/VERDICT_vong7_codex.json`, đúng §8.3) cho r10 bản sửa 2: `changes_requested`, X01 P2 (lớp `nghiem-thu-khong-co-lap-chot-dich`, lỗ trong bộ quét ghim ở luật 3). Hội tụ 6→7 = 0/2. Chủ kho quyết E1 (#1236 issuecomment-7053621494): **thu hẹp luật 3** thành công cụ khuyến nghị; nghiệm thu bắt buộc = luật 1, 2, 4, 5 + quét độc lập của reviewer mã. Bản sửa 3 thực hiện quyết định đó. Lưu ý đính chính: VERDICT vòng 6 và 7 chép `hoi_tu.lich_su_giu_nguyen.ma4_sang_5 = "0/1"`; số đúng là `KHONG_DO_DUOC` (verdict mã lượt 4–5 không có slug) — đừng chép lại. Vòng 6 run.json có model `KHONG_DO_DUOC`.

## Quyền
- CHỈ ĐỌC trong `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r10-8-codex/repo`. Không sửa, không commit, không push. Không gọi GitHub/mạng.
- Được tạo tệp nháp/script đo CHỈ dưới `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r10-8-codex/work/`.

## Đầu vào
- Đặc tả: `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r10-8-codex/SPEC.md`, sha256 `3ee831738c70c5eabb27720e295b4953c9a9bdd1ac29a03cc7b964d28658fcdc` (= `git show 81dc1eb:ops/specs/wp1236-r10.md`). Kiểm sha256 trước; lệch thì dừng. Phần mới: `git diff 33b6803 81dc1eb`.
- Kho `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r10-8-codex/repo` HEAD `81dc1eb73925babe638ed50222e0354bf7488248`. Lịch sử vòng 1–7 ở `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r10-8-codex/lich_su/` và `ops/reviews/wp1236-spec-*`.
- `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r10-8-codex/ISSUE.md`; `CLAUDE.md`; `docs/PROTOCOL_DA_PHIEN.md` §8, §8.3, §12; `docs/adr/0044*`, `0053*`, `0055*`, `0060*`, `0067*`.

## Việc phải làm
0. **Nhãn cho MỌI lớp của vòng 7** (X01 và các lớp lịch sử còn `VA_MOT_PHAN`): bốn nhãn §8.3, kèm phép đo/trích dẫn. Giữ slug.
1. **Sau khi thu hẹp luật 3, nghiệm thu bắt buộc (luật 1, 2, 4, 5 + quét độc lập của reviewer mã) có đủ chặt và kiểm được không?** Luật 5 vẫn dùng `hoi-quy` của bộ quét: phần đó có còn lỗ kiểu X01 làm nghĩa vụ hồi quy mất ID không? Còn câu nào trong đặc tả coi luật 3 là bắt buộc (mâu thuẫn nội tại)?
2. **Quét lớp** trước khi báo; số tổng và `nang_tran` (đề nghị 1700, chờ E2) có nhất quán với bản sửa 3 không.
3. Không mở lại các lớp đã `DA_VA_THAT` trừ khi bản sửa 3 làm hỏng chúng (có phép đo).

## Mức nghiêm trọng — §8 nguyên văn
`sensitive`: approve chỉ khi 0 P0/P1/P2 mở; **mỗi P3 phải đóng** (reviewer xác nhận có bằng chứng, hoặc chủ kho miễn neo exact SHA). Mỗi P2 trở lên phải có phép đo hoặc trích dẫn.

## Đầu ra — HAI tệp
1. `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r10-8-codex/work/VERDICT.json`, ghi tăng dần; kiểm bằng `python3 /tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r10-8-codex/kiem_verdict_lop.py /tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r10-8-codex/work/VERDICT.json --vong 8` (phải `HOP_LE`; lưu vào `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r10-8-codex/work/kiem_verdict.txt`). Khoá: `spec_sha256`, `vong`: 8, `findings` [`id` Y01…, `class_slug`, `severity`, `vi_tri`, `van_de`, `bang_chung`, `de_xuat`], `class_table` [`slug`, `finding_ids`, `manifestations`, `highest_open_severity`, `nguon`, `common_fix`, `closing_check`, `ly_do_va_rieng`], `prior_class_status` [`slug`, `finding_cu`, `vong_xuat_hien`, `status`, `evidence`, `chua_do_duoc`], `bang_noi_slug`, `hoi_tu` {`vong7_sang_8`: "|F|/|U|", `lop_lap_lan_ba`: [...]}, `da_do_khop`, `verdict`.
2. `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r10-8-codex/work/VERDICT.md` — tóm tắt; dòng cuối `KET_LUAN: approve | changes_requested`.
