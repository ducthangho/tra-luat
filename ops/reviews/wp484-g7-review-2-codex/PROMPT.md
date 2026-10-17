# Cross-review độc lập — Packet #484 (wp484 r8/g7), PR #792, lượt 2/2 (review lại cuối)

Bạn là reviewer Codex, khác họ với executor g7 (Claude). Vai READ-ONLY với mã: KHÔNG sửa tệp nào trong `KHO`.
Chỉ được ghi vào thư mục làm việc hiện tại (thư mục ra). Kết quả bắt buộc: `VERDICT.md` trong thư mục ra; ghi SỚM
rồi cập nhật dần. KHÔNG dùng credential thật; không ghi vào `~/.codex` thật. Đây là lời gọi Codex CUỐI cho PR này
(protocol §8): chưa approve thì packet chuyển sang checkpoint, nên hãy nêu rõ cái gì còn chặn và cái gì không.

## Định danh

- Kho `ducthangho/tra-luat` tại `KHO` (cuối prompt), detached đúng head.
- Exact head: `b355ff8b3d081c8b64ce803f53a4a09216411a29` (tree `812a7fcc3038c625077a1dbd992ced1e6174185d`), PR #792.
- Base: `653fef3f52f3130dd6f597c1036430ffb807fef1` (`origin/master`). Diff PR: `git -C KHO diff 653fef3 b355ff8`.
- Head lượt 1: `99e79b107d4fd138dcd3e5ad51851a846fac9eb5`. Delta lượt vá 2: `git -C KHO diff 99e79b1 b355ff8`
  (7 tệp, +315/−44).
- Verdict lượt 1 của bạn (bản sao nguyên byte): `VERDICT1` (cuối prompt), sha256 `21671d6e…`.
- Đặc tả: r7 `SPEC7` (sha256 `35a81f47…`) + sửa đổi r8 `SPEC8` (sha256
  `4a512dd38721c3c4eec7978489ba06485feab32f94a0c5637a085d6c694ba38c`). r8 ghi hai quyết định chủ kho:
  **F01 chấp nhận giới hạn** (nợ `codex-rejected-state-khong-ghi-duoc`; N4 hạ thành "mọi lối báo lỗi ghi state bằng
  lý do riêng") và **F04 mở rộng write set** thêm `.claude/hooks/session_start.py`. Nợ CAS (Q3) giữ nguyên.
- Handoff: `ops/handoff/wp484-g7-claude.md` (mục "Lượt vá 2"). Lớp review: `sensitive`.

## Nhiệm vụ

1. Với TỪNG finding F01–F04 của lượt 1: bản vá có đóng đúng cái bạn đã đo không? Chạy lại đúng phép đo của bạn
   (`review_checks.py` của lượt 1 không có trong thư mục này — hãy dựng lại phép thử tương đương) trên head mới.
   - F01: theo quyết định chủ kho, KHÔNG còn đòi "lần sau không probe"; đòi cả ba lối (`launcher._do_codex_song`,
     `codex_cred.cmd_kiem`, materializer `chuan_bi_xac_thuc`) báo lỗi ghi state bằng lý do RIÊNG.
   - F02: `token_invalidated` là từ chối kể cả rc=0 + marker.
   - F03: `_danh_dau_auth_hong(home, da_probe)`; cả hai lối truyền bytes đã probe. Còn lối nào ghi danh tính đọc lại?
   - F04: shell dời materialize xuống sau bước cài CLI; bridge hoãn materialize khi vắng `codex`. Snapshot thô có tới
     được shell / installer / child nào không? Thứ tự mới có làm hỏng điều gì master đang giữ (vd probe credential
     phía dưới chạy trước materialize, `credential-status`, doctor)? Nhánh "có codex" của bridge còn như cũ không?
2. Soi hồi quy do chính lượt vá 2 gây ra (tìm "đường thứ ba" — lối vào mà bản vá không phủ), và các ca test đã sửa:
   `r484_g2_hook_shell_scrub_truoc_probe` (shim viết lại, nay đo bằng nhật ký), `r484_g2_bridge_scrub_va_chot_remote`
   (ghim `shutil.which`), ca dùng `bash_nen.tim_bash()`. Ca nào bị nới lỏng tới mức mất răng?
3. ĐO, đừng chỉ đọc. Executor khai (17-10, Linux, sau khi `/tmp/.git` của sandbox lượt 1 đã biến mất):
   `launcher_test.py` 218/218 cả có/không `CODEX_AUTH_JSON` giả; `codex_cred_test.py` 18/18 + đột biến 18/18;
   `packet_loop_test.py` ĐẠT; `ops/cong_cu_test.py` (CONG_CU_TEST_BAN_KINH=manh) cổng cây thật ĐẠT; 5 đột biến g7 trong
   `DOT_BIEN` + 2 đột biến tay F04 giết ca đích bằng assertion. **Lưu ý môi trường:** ở lượt 1 sandbox của bạn có
   `/tmp/.git` rỗng làm `_KhoCodex` từ chối mọi home dưới `/tmp`; nếu lặp lại, ghi KHÔNG ĐO ĐƯỢC cho phép đo tích
   hợp thay vì coi là lỗi sản phẩm, và dùng seam như lượt 1.
4. Đột biến: KHÔNG sửa `KHO`; chép ra thư mục tạm (`mktemp -d`). Hướng thử cần soạn nội dung nhạy cảm thì mô tả bằng lời.

## Định dạng VERDICT.md

- Dòng 1: `Reviewed commit: b355ff8b3d081c8b64ce803f53a4a09216411a29`
- Dòng 2: `Spec SHA-256: <băm SPEC8 bạn tự đo>`
- Dòng 3: `verdict: approve` hoặc `verdict: changes_requested`; dòng 4: `P0=… P1=… P2=… P3=…`.
- Bảng đối chiếu F01–F04 (ĐÃ ĐÓNG / CHƯA ĐÓNG / ĐÓNG THEO QUYẾT ĐỊNH CHỦ KHO) với phép đo.
- Finding mới: mã G01…, mức, tệp:dòng, PHÉP ĐO (lệnh + output), HINT nếu phức tạp.
- Bảng ≥ 6 hướng thử; mục "Đã đo"; mục "KHÔNG ĐO ĐƯỢC".
- Ngưỡng `sensitive`: approve khi P0=0, P1=0, và mỗi P2/P3 còn mở hoặc đã có quyết định chủ kho, hoặc bạn nêu rõ để
  chủ kho quyết. Nợ đã có quyết định (CAS, F01) không tính là finding mở.

## Đường dẫn

- KHO: `/tmp/claude-0/-home-user-tra-luat/f5ea9c29-b7bf-59b1-89c5-898536fe68e2/scratchpad/rv792b`
- SPEC7: `/tmp/claude-0/-home-user-tra-luat/f5ea9c29-b7bf-59b1-89c5-898536fe68e2/scratchpad/rv792b-out/spec-wp484-r7.md`
- SPEC8: `/tmp/claude-0/-home-user-tra-luat/f5ea9c29-b7bf-59b1-89c5-898536fe68e2/scratchpad/rv792b-out/spec-wp484-r8.md`
- VERDICT1: `/tmp/claude-0/-home-user-tra-luat/f5ea9c29-b7bf-59b1-89c5-898536fe68e2/scratchpad/rv792b-out/VERDICT-luot1.md`
- Thư mục ra: `/tmp/claude-0/-home-user-tra-luat/f5ea9c29-b7bf-59b1-89c5-898536fe68e2/scratchpad/rv792b-out`
