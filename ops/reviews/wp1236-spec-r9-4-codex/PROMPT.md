# Review lại ĐẶC TẢ wp1236 r9 (bản sửa 3) — vòng 4 — reviewer độc lập, theo PROTOCOL §8.3

Bạn là reviewer ĐỘC LẬP cho một ĐẶC TẢ packet (không phải mã), review class `sensitive`. Kho: ducthangho/tra-luat.

## Vì sao có vòng này
Ba vòng trước (Codex và Claude, `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r9-4-codex/lich_su/VERDICT_vong{1,2,3}_{codex,claude}.md`) KHÔNG theo §8.3: finding không có slug lớp, không có bảng lớp, từ vòng 2 dùng ĐÓNG/CÒN MỞ thay cho bốn nhãn theo lớp. Chủ kho bác dùng chúng để approve. Hai approve vòng 3 nhắm bản `50269a88…`; bản hiện hành `e3efa593…` (bản sửa 3, soạn giả tự áp các P3 vòng 3) CHƯA từng được review. Vòng này phải (1) dựng lịch sử lớp cho vòng 1–3 của CẢ HAI reviewer, (2) review bản `e3efa593` đầy đủ theo §8.3.

## Quyền
- CHỈ ĐỌC trong `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r9-4-codex/repo`. Không sửa, không commit, không push. Không gọi GitHub/mạng.
- Được tạo tệp nháp/script đo CHỈ dưới `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r9-4-codex/work/`.
- Hướng thử nào đòi soạn nội dung tấn công thì MÔ TẢ BẰNG LỜI; dựng biến thể bằng cách SỬA BẢN SAO fixture thật là được.

## Đầu vào
- Đặc tả: `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r9-4-codex/SPEC.md`, sha256 `e3efa593c6dbbd15a0850702dfbc927ce51c3f1361642292e2f0b235c1bee6a8` (= `git show 176feba:ops/specs/wp1236-r9.md`). Kiểm sha256 trước; lệch thì dừng. Các bản trước: vòng 3 nhắm `50269a88…` (`git log --oneline -- ops/specs/wp1236-r9.md` để tìm commit), vòng 2 `18da18c4…` (`d81f359`), vòng 1 `ba466e72…` (`89c07bc`). `git diff <commit vòng 3> 176feba -- ops/specs/wp1236-r9.md` là phần chưa ai review.
- Kho ở `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r9-4-codex/repo`, HEAD `176feba`, lịch sử đầy đủ. r8 để đối chiếu: `git show refs/remotes/origin/claude/spec-1236-r8:ops/specs/wp1236-r8.md`.
- Bản tham chiếu đo của soạn giả: `ops/reviews/wp1236-r9-soan/` (`python3 -B ops/reviews/wp1236-r9-soan/thamchieu.py .` và `do_loi_khai.py .` từ gốc kho).
- `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r9-4-codex/ISSUE.md`: thân #1236, quyết định chủ kho liên quan, thân #1257.
- Đọc thêm: `CLAUDE.md` · `docs/PROTOCOL_DA_PHIEN.md` §8, §8.3, §10.2.2, §12, §20 · `.claude/skills/soan-spec/SKILL.md` · `docs/adr/0053*`, `0055*`, `0060*`, `0067*` · `ops/land_evidence_nguon.py` · `.claude/dev/packet_loop.py` (`cmd_kiem_dong_wp`, `CHECK_BAT_BUOC`) · `ops/ci_provenance.py` · ba phiên bản `ops/land/*/danh_gia_gate.py`.

## Việc phải làm
0. **Lịch sử lớp vòng 1–3 (§8.3).** Gán MỖI finding cũ của cả hai reviewer (R…, S…, T… và ID bên Claude) đúng một `class_slug` theo NGUYÊN NHÂN; gộp finding cùng cơ chế, kể cả khác reviewer, vào một lớp (ghi `bang_noi_slug`). Với từng lớp, gắn nhãn trên bản `e3efa593`: `DA_VA_THAT` · `VA_MOT_PHAN` · `CHUA_VA` · `KHONG_DO_DUOC`, kèm phép đo hoặc trích dẫn. `DA_VA_THAT` CHỈ khi mọi biểu hiện trong phạm vi đã đóng, bản sửa không sinh biểu hiện mới cùng cơ chế, không còn phần phải đo. Đếm số lớp xuất hiện ở ≥ 3 vòng (§12: lặp lần ba).
1. **Quét lớp trước khi báo.** Với mỗi lớp (cũ hay mới), quét MỌI biểu hiện cùng lớp trong đặc tả trước khi ghi finding; không báo lỗi lẻ.
2. **Bản sửa 3** (phần chưa ai review) có đúng không, có làm mâu thuẫn chỗ khác không.
3. **Thiết kế có đạt mục 1–2 của Issue #1236 không** — tìm một lời khai dương mà hồ sơ MỚI qua được L8/D2b mà không có tệp danh-gia khớp provenance của một run land thật (ngoài giới hạn đã khai ở `chua_do_duoc`/`ngoai_pham_vi`). Đặc tả có đủ chặt để executor không tự suy (tên lý do, mã thoát, ca, đột biến) không?
4. Số đo (47/10/9, 25/56/39/50, 94/94…), `kich_thuoc`, `nang_tran`, `pham_vi_e`, `luat_dung`, `tran_loi_goi_codex`: chỉ nêu nếu sai số đo, sai ADR, hay thiếu hệ quả.

## Mức nghiêm trọng — §8 nguyên văn
Review class `sensitive`: approve chỉ khi 0 P0/P1/P2 mở; **mỗi P3 phải đóng** (reviewer xác nhận có bằng chứng, hoặc chủ kho miễn neo exact SHA). P3 KHÔNG tự động "không chặn"; liệt kê đủ. Mỗi P2 trở lên phải có phép đo hoặc trích dẫn cụ thể.

## Đầu ra — HAI tệp
1. `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r9-4-codex/work/VERDICT.json` — JSON, ghi tăng dần. Kiểm bằng `python3 /tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r9-4-codex/kiem_verdict_lop.py /tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r9-4-codex/work/VERDICT.json --vong 4` (phải in `HOP_LE`; lưu output vào `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r9-4-codex/work/kiem_verdict.txt`).
```json
{
  "spec_sha256": "<đo được>", "vong": 4,
  "findings": [{"id": "U01", "class_slug": "<slug>", "severity": "P0|P1|P2|P3", "vi_tri": "<mục/dòng SPEC.md>",
                "van_de": "<một câu>", "bang_chung": "<lệnh + output rút gọn, hoặc trích dẫn>", "de_xuat": "<cách vá CHUNG cho lớp>"}],
  "class_table": [{"slug": "<slug>", "finding_ids": ["U01"], "manifestations": ["<biểu hiện>"], "highest_open_severity": "P2|null",
                   "nguon": "<vòng/sha256 đặc tả>", "common_fix": "<cách vá chung>", "closing_check": "<phép kiểm đóng lớp>",
                   "ly_do_va_rieng": "<chỉ khi phải vá từng biểu hiện>"}],
  "prior_class_status": [{"slug": "<slug>", "finding_cu": ["R01", "..."], "vong_xuat_hien": [1, 2], "status": "DA_VA_THAT|VA_MOT_PHAN|CHUA_VA|KHONG_DO_DUOC",
                          "evidence": "<phép đo/trích dẫn trên e3efa593>", "chua_do_duoc": "<phần chưa đo, nếu có>"}],
  "bang_noi_slug": [{"slug": "<slug>", "finding_cu": ["..."], "ly_do_gop": "<cùng cơ chế gì>"}],
  "hoi_tu": {"vong1_sang_2": "<|F|/|U| hoặc KHONG_DO_DUOC kèm lý do>", "vong2_sang_3": "...", "vong3_sang_4": "...",
             "lop_lap_lan_ba": ["<slug>"]},
  "da_do_khop": ["<liệt kê ngắn>"],
  "verdict": "approve|changes_requested"
}
```
`class_table` có ĐÚNG một dòng cho mỗi slug của `findings`; `prior_class_status` phủ MỌI lớp của vòng 1–3.
2. `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r9-4-codex/work/VERDICT.md` — tóm tắt người đọc, dòng cuối đúng dạng `KET_LUAN: approve | changes_requested`.
