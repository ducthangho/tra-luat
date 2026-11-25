# Review offline MÃ — wp1236 đợt B theo đặc tả r12 — lượt 5 (XÁC NHẬN) — reviewer độc lập, theo PROTOCOL §8.3 và ADR-0060

Bạn là reviewer ĐỘC LẬP, read-only, cho MÃ của work packet `sensitive` wp1236 **đợt B** (luật L8 trong `ops/land_evidence_nguon.py`). Kho: ducthangho/tra-luat. Đây là lời gọi Codex **5/6** của đợt B (trần do chủ kho nâng, #1236 issuecomment-7152104422). Effort: high (chủ kho chỉ định).

## Vì sao có lượt này
Lượt 4 (của bạn, `lich_su/VERDICT_luot4.*`) review ĐÚNG ứng viên `bca55c1` và kết luận `changes_requested` CHỈ vì một P3 (B02, lớp `nghiem-thu-khong-co-lap-chot-dich`, `ngoai_bang_dong`) đang chờ chủ kho miễn; không còn P0/P1/P2. Sau đó chủ kho đã miễn B02 neo đúng SHA này. Lời miễn (trích nguyên văn từ #1236 issuecomment-7156364013, đăng 2026-11-25T07:53:18Z bằng tài khoản chủ kho, phiên agent ghi hộ câu chủ kho gõ):

```
mien_p3: bca55c1cd09c57180d60b05d5ca1813828ae1d10 nghiem-thu-khong-co-lap-chot-dich
```
Câu của chủ kho: *"Cho miễn P3, ghi nợ và xử lý ở packet sau"*. Nợ ghi: `WP1236-B02-bat-bien-bo-sinh-test-dot-A`. Trước đó một bản ghi hộ khác ở issuecomment-7153679183 (`B02: bca55c1… mien`, lựa chọn của chủ kho "Miễn B02 neo bca55c1").

Bạn KHÔNG truy cập được GitHub; coi trích dẫn trên là đầu vào do điều phối cung cấp, và ghi rõ trong verdict rằng bạn dựa vào nó (không tự kiểm được tác giả comment). Cổng `kiem-merge` K5 sẽ tự đo dòng `mien_p3:` ấy trên GitHub.

Mục tiêu lượt 5: xác nhận rằng trên ĐÚNG `bca55c1` (a) không có gì đổi so với lượt 4, (b) không có finding P0–P2 nào lượt 4 bỏ sót, (c) điều kiện duy nhất còn lại của lượt 4 là lời miễn B02 nay đã có — rồi ra kết luận chính thức theo §8.

## Quyền
- CHỈ ĐỌC trong `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/b5-5-codex/repo`. Không sửa, không commit, không push. Không gọi GitHub/mạng.
- Tệp nháp, bản sao để đột biến: CHỈ dưới `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/b5-5-codex/work/`. Hướng thử nào đòi soạn nội dung tấn công thì MÔ TẢ BẰNG LỜI.

## Đầu vào
- `repo` ở HEAD `bca55c1cd09c57180d60b05d5ca1813828ae1d10` (tree `14f1571aada834fc22ea32c29076df8834c05bd6`), base `f602325574c62184caf16309631f5f680ca5cee2`. Diff toàn đợt `git diff f602325 HEAD`.
- `SPEC.md` (sha256 phải là `4589daf1fd666b03a68b7d7dcd5c60903c10e946963fd324c9ee6185ed8e2dc7`), `LEASE.yaml`.
- Verdict lượt 1–4 của bạn và các probe: `lich_su/`.
- Bằng chứng executor `bang_chung/` (lời khai).
- Thông tin sau lượt 4, do điều phối đo (lời khai, bạn không kiểm lại được, chỉ ghi nhận): Windows local M3 trên DESKTOP-T9R33P2 xanh cho `bca55c1` (biên nhận #1236 issuecomment-7161189686: selftest 1786/1786, suite B 38/38 · 145/145, tập ca đỏ `ci_duong_nhanh_test` ung = nen, delta 0); CI GitHub PR #1526 xanh; connector Codex trên PR #1526: completed, không finding.

## Việc phải làm
1. Xác nhận `git rev-parse HEAD` = `bca55c1…`, cây sạch, và `git diff f602325 HEAD` chỉ chạm hai tệp write set.
2. Chạy lại: `python3 -B ops/land_evidence_nguon_test.py` (đòi `CA: N/N`, `DOT BIEN: M/M`, `TONG: DAT`); `python3 -B ops/land_evidence_nguon.py --root .`; `python3 -m ruff check --select F` hai tệp (so base); `git diff --check f602325 HEAD`; numstat (trần 560).
3. Đối chiếu lớp (§8.3): gán nhãn cho lớp `nghiem-thu-khong-co-lap-chot-dich`, xử lý B01 (lượt 4: DA_VA_THAT) và B02 (miễn neo SHA). Nếu bạn phát hiện finding MỚI mức P0–P2, báo đầy đủ với phép đo; P3 mới ⇒ báo và ghi `chờ miễn chủ kho`.
4. Quét nhanh theo lớp toàn diff một lượt nữa để chắc lượt 4 không bỏ sót P0–P2 (ưu tiên: thứ tự nạp module trước miễn trừ, nhánh KHÔNG ĐO ĐƯỢC rc 2, `MIEN_TRU_L8` khớp băm byte).

## Mức nghiêm trọng — §8 nguyên văn
`sensitive`: approve chỉ khi 0 P0/P1/P2 mở; **mỗi P3 phải đóng** (bạn xác nhận có bằng chứng, hoặc chủ kho miễn neo exact SHA). Mỗi P2+ phải có phép đo.

## Đầu ra
1. `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/b5-5-codex/work/VERDICT.json`; kiểm `python3 /tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/b5-5-codex/kiem_verdict_lop.py /tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/b5-5-codex/work/VERDICT.json --vong 5` (phải HOP_LE; lưu stdout vào `work/kiem_verdict.txt`). Khoá như lượt 4: `reviewed_sha`, `spec_sha256`, `vong`: 5, `dot`: "B", `findings`, `class_table`, `m3_windows`, `luat9`, `prior_class_status`, `hoi_tu` {`luot4_sang_5`: "|F|/|U|", `lop_lap_lan_ba`: [...]}, `da_do_khop`, `verdict`. Một P3 đã được chủ kho miễn neo SHA thì ghi trong `prior_class_status` (status + evidence trỏ lời miễn), KHÔNG để nó làm `verdict` thành `changes_requested`.
2. `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/b5-5-codex/work/VERDICT.md` — tóm tắt; dòng cuối `KET_LUAN: approve | changes_requested`.
3. **Tin nhắn trả lời cuối cùng của bạn** (thứ in ra stdout) phải KẾT THÚC bằng đúng một dòng riêng, không định dạng, không ký tự nào sau nó: `KET_LUAN: approve` hoặc `KET_LUAN: changes_requested` — trùng với dòng cuối của VERDICT.md. Cổng `kiem-merge` K4 đọc dòng cuối của stdout này.
