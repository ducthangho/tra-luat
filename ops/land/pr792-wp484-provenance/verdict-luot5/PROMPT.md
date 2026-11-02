# Cross-review độc lập — Packet #484 (wp484 r8/g7), PR #792, lượt 5 (attempt 5: J01 + `failure_class`)

Bạn là reviewer Codex, khác họ với executor g7 (Claude). Vai READ-ONLY với mã: KHÔNG sửa tệp nào trong `KHO`.
Chỉ ghi vào thư mục làm việc hiện tại; kết quả bắt buộc `VERDICT.md`, ghi SỚM rồi cập nhật. Không dùng credential
thật, không ghi `~/.codex` thật, không chạy installer thật (apt-get/cargo/npm/winget/choco) trên máy này.

Thẩm quyền: chủ kho nâng trần attempt 4→8 và lời gọi Codex 4→5
(https://github.com/ducthangho/tra-luat/issues/484#issuecomment-6237196943). Đây là lời gọi Codex CUỐI được cấp.
Câu hỏi: **sau attempt 5, còn P0/P1/P2 nào mở không?**

## Định danh

- `KHO` detached đúng head `907214d2cd0b67ff444b3adf734811eab39bfc71` (tree `735f7ee67c4e2bf2612fcdc4d6027eff453baeb0`).
  Head lượt 4: `0f31bb3e6151dd0cc67e8d4664b139259383b8d5`. Delta: `git -C KHO diff 0f31bb3 907214d` (3 tệp, +93/−3).
- Verdict lượt 4 `VERDICT4` (sha256 `841bf022163d7594ce82a9a9411e8a5ab17ab36cfadf343f4cbd8d92c3a4741b`): approve, P2=1 (J01).
  Lượt 1–3: `VERDICT1`..`VERDICT3`. Đặc tả `SPEC8` (sha256 `4a512dd38721c3c4eec7978489ba06485feab32f94a0c5637a085d6c694ba38c`).
- Ngoài VERDICT4, connector Codex trên GitHub review toàn PR @ `0f31bb3` và nêu (bạn không có quyền đọc GitHub; nội dung
  chép lại ở đây):
  - **P1** "spec/lease không có trong cây PR" — executor trả lời: chúng ở nhánh `ops/wp484-r7-spec` theo quy ước lease
    sống trên `ops/**`; không phải lỗi mã. Bạn có thể đánh giá lập luận ấy từ tài liệu trong `KHO` (`CLAUDE.md`, mục
    "SỔ LEASE KHÔNG NẰM MỘT CHỖ"; `docs/PROTOCOL_DA_PHIEN.md`).
  - **P2** `launcher.py`: `ban_ghi["failure_class"] = "unknown"` gán ngay sau `Popen` và không bao giờ gỡ, nên lượt
    `xong`/`ma_thoat=0` vẫn mang nhãn thất bại. ⇒ **đã vá trong delta này.**
  - **P2** `_kiem_resume`: checkpoint resume không đối chiếu `checkpoint_id` với một `run.json` gốc trong `run_root`.
    ⇒ chủ kho quyết **nợ có tên** `launcher-resume-checkpoint-khong-rang-buoc-luot-goc`, KHÔNG vá trong packet này —
    không tính là finding mở.
- Script đột biến của executor (tham khảo, KHÔNG phải bằng chứng — tự đo lại): `DOT_BIEN_EXECUTOR`.

## Nhiệm vụ

1. **J01 đóng chưa?** Fixture `r484_g2_hook_shell_scrub_truoc_probe` nay lọc `BASH_ENV`/`ENV`/`BASH_FUNC_*`, đặt `HOME`
   tạm, thêm `actionlint` giả. Ca mới `r484_g8_hook_scrub_kin_voi_bash_env` gọi lại ca trên với `BASH_ENV`/`ENV` trỏ
   tệp khởi động chèn `ambient/` (rg hỏng + installer gián điệp) lên đầu PATH, rồi đòi `NAP` CÓ và `NGOAI …` VẮNG.
   Chạy lại đúng phản chứng `env-escape` của bạn ở lượt 4 trên head mới. Còn đường nào khác từ môi trường máy chạy
   (bạn đã liệt kê: `PYTHONPATH`/`PYTHONHOME`, startup Python, …) đáng là P2 THẬT (có phản chứng chạy được), hay chỉ
   là suy đoán? Đừng cộng finding suy đoán.
2. **`failure_class`:** lượt `xong` + rc 0 không còn khoá; rc≠0 / `qua_han` / `bi_ngat` / `da_dung` vẫn `unknown`?
   Còn đường nào lượt thành công mang nhãn hoặc lượt hỏng mất nhãn? Ca `r484_g8_run_xong_khong_mang_failure_class`.
3. Hai đột biến mới đã đăng ký (`g8_xong_rc0_van_giu_failure_class` trong `DOT_BIEN`, `g8_fixture_chep_nguyen_moi_truong`
   trong `DOT_BIEN_HARNESS`) có giết ca đích bằng assertion của CHÍNH ca không? Chạy trên BẢN SAO TẠM.
4. Hồi quy: ca nào khác đổi màu so `0f31bb3`; ruff F delta; hạn ngạch `ops/bash_nen.py` cho `launcher_test.py` (7).
5. ĐO. Executor khai (17-10, Linux): `launcher_test.py` 221/221 cả có/không `CODEX_AUTH_JSON` giả (2 ca Windows bỏ
   qua); ca J01 lặp 3/3; hai đột biến giết ca đích; ruff F 5/5; `bash_nen quet` ĐẠT. Môi trường sandbox chặn phép đo
   (vd `/tmp/.git` làm `_KhoCodex` từ chối home dưới `/tmp`) thì ghi KHÔNG ĐO ĐƯỢC, dùng seam khai rõ như lượt 4.
6. Hướng thử cần soạn nội dung nhạy cảm thì mô tả bằng lời.

## Định dạng VERDICT.md

- Dòng 1 `Reviewed commit: 907214d2cd0b67ff444b3adf734811eab39bfc71`; dòng 2 `Spec SHA-256: <SPEC8 tự đo>`;
  dòng 3 `verdict: approve|changes_requested`; dòng 4 `P0=… P1=… P2=… P3=…`.
- Trả lời thẳng câu hỏi ở đầu thân. Bảng J01 + `failure_class` + P1 connector (đánh giá lập luận); finding mới mã
  K01…; bảng ≥ 4 hướng thử; "Đã đo"; "KHÔNG ĐO ĐƯỢC".
- Ngưỡng `sensitive`: approve khi P0=0, P1=0 và mọi P2/P3 còn mở đã có quyết định chủ kho hoặc được bạn nêu rõ để
  chủ kho quyết. Nợ đã có quyết định (CAS, F01, checkpoint) không tính là finding mở.

## Đường dẫn

- KHO: `/tmp/claude-0/-home-user-tra-luat/f5ea9c29-b7bf-59b1-89c5-898536fe68e2/scratchpad/rv792e`
- SPEC8: `/tmp/claude-0/-home-user-tra-luat/f5ea9c29-b7bf-59b1-89c5-898536fe68e2/scratchpad/rv792e-out/spec-wp484-r8.md`
- VERDICT1..4: `/tmp/claude-0/-home-user-tra-luat/f5ea9c29-b7bf-59b1-89c5-898536fe68e2/scratchpad/rv792e-out/VERDICT-luot{1,2,3,4}.md`
- DOT_BIEN_EXECUTOR: `/tmp/claude-0/-home-user-tra-luat/f5ea9c29-b7bf-59b1-89c5-898536fe68e2/scratchpad/rv792e-out/executor-do_g8.py`
- Thư mục ra: `/tmp/claude-0/-home-user-tra-luat/f5ea9c29-b7bf-59b1-89c5-898536fe68e2/scratchpad/rv792e-out`
