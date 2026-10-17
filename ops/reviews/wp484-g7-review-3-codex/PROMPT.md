# Cross-review độc lập — Packet #484 (wp484 r8/g7), PR #792, lượt 3/3 (CUỐI, trần nâng bởi chủ kho)

Bạn là reviewer Codex, khác họ với executor g7 (Claude). Vai READ-ONLY với mã: KHÔNG sửa tệp nào trong `KHO`.
Chỉ ghi vào thư mục làm việc hiện tại; kết quả bắt buộc `VERDICT.md`, ghi SỚM rồi cập nhật. Không dùng credential
thật, không ghi `~/.codex` thật. Đây là lời gọi Codex CUỐI: chủ kho nâng trần 2→3
(https://github.com/ducthangho/tra-luat/issues/484#issuecomment-6228814972) với điều kiện lượt này chưa approve
thì packet DỪNG hẳn. Hãy phân biệt rõ cái gì CHẶN và cái gì là nợ/P3 có thể để chủ kho quyết.

## Định danh

- `KHO` (cuối prompt) detached đúng head `cfd3550b6336eecb6847543a5f33200b57dd81ba`
  (tree `87ef372ec6d779610a2d7ce9aae74b6a57febafb`), PR #792. Base `653fef3f52f3130dd6f597c1036430ffb807fef1`.
- Head lượt 2: `b355ff8b3d081c8b64ce803f53a4a09216411a29`. Delta lượt vá 3: `git -C KHO diff b355ff8 cfd3550`
  (3 tệp, +79/−6: `session_start.py`, `launcher_test.py`, handoff). Gồm `7cc31e9` (ca credential-status giải stderr
  UTF-8 — Windows cp1252), `84f2a8e` (G01+G02), `cfd3550` (handoff).
- Verdict lượt 1 `VERDICT1` (sha256 `21671d6e…`) và lượt 2 `VERDICT2` (sha256
  `778dac6507e5ca5f56c90d0d2f61bea4d301c2a34b036af1704d644a4c49ea6c`), bản sao nguyên byte.
- Đặc tả: `SPEC7` (`35a81f47…`) + `SPEC8` (`4a512dd38721c3c4eec7978489ba06485feab32f94a0c5637a085d6c694ba38c`).
  Quyết định chủ kho đang hiệu lực: nợ CAS (Q3), F01 chấp nhận giới hạn (r8). Handoff mục "Lượt vá 3".

## Nhiệm vụ

1. G01 (lượt 2): bridge nay gọi `_codex_chay_duoc(env)` — `codex --version` có hạn 8s, đòi rc=0 VÀ có đầu ra, child
   nhận env đã gỡ `CODEX_AUTH_JSON`. Còn lối nào CLI "có mặt nhưng không dùng được" lọt qua (ví dụ `--version` đạt
   nhưng probe thật hỏng; timeout; Windows PATHEXT/`.cmd`)? Child probe này có thấy snapshot qua đường nào không?
   Nhánh "có codex chạy được" còn giữ thứ tự cũ `prepare → bash --version → hook`?
2. G02 (lượt 2): fixture `r484_g2_hook_shell_scrub_truoc_probe` nay có `codex`/`claude`/`npm` giả và PATH bỏ mọi thư
   mục chứa bản thật; gọi npm là ĐỎ. Còn phụ thuộc máy chạy (mạng, installer, tool khác) không? Ca còn răng không?
3. Hồi quy do delta lượt 3 (đường thứ ba), và mọi thứ còn mở từ lượt 1–2 mà bạn thấy chưa đóng.
4. ĐO. Executor khai (17-10, Linux): `launcher_test.py` 219/219 cả có/không `CODEX_AUTH_JSON` giả; `codex_cred_test.py`
   18/18 + đột biến 18/18; `packet_loop_test.py` ĐẠT; `ops/cong_cu_test.py` (CONG_CU_TEST_BAN_KINH=manh) cổng cây thật
   ĐẠT; đột biến tay: `_codex_chay_duoc` luôn True ⇒ ca G01 ĐỎ; gỡ `unset CODEX_AUTH_JSON` khỏi hook ⇒ ca scrub ĐỎ;
   bỏ nhánh hoãn ⇒ ca F04 bridge ĐỎ. Windows: `launcher-windows` XANH trên `7cc31e9`; `gate`/`gate-cong-cu` Windows ĐỎ
   do `t23`/`t49` của `ops/cong_cu_test.py` — executor khai đỏ sẵn, thuộc wp748 (diff không đụng `ops/`).
   Lưu ý môi trường sandbox (`/tmp/.git` ở lượt 1): phép đo tích hợp storage bị chặn thì ghi KHÔNG ĐO ĐƯỢC.
5. Đột biến chỉ trên bản sao tạm. Hướng thử cần soạn nội dung nhạy cảm thì mô tả bằng lời.

## Định dạng VERDICT.md

- Dòng 1 `Reviewed commit: cfd3550b6336eecb6847543a5f33200b57dd81ba`; dòng 2 `Spec SHA-256: <SPEC8 tự đo>`;
  dòng 3 `verdict: approve|changes_requested`; dòng 4 `P0=… P1=… P2=… P3=…`.
- Bảng đối chiếu G01, G02 (và F04 tổng thể) với phép đo; finding mới mã H01…; bảng ≥ 6 hướng thử; "Đã đo"; "KHÔNG ĐO ĐƯỢC".
- Ngưỡng `sensitive`: approve khi P0=0, P1=0 và mọi P2/P3 còn mở hoặc có quyết định chủ kho, hoặc được bạn nêu rõ để
  chủ kho quyết. Nợ đã có quyết định (CAS, F01) không tính là finding mở.

## Đường dẫn

- KHO: `/tmp/claude-0/-home-user-tra-luat/f5ea9c29-b7bf-59b1-89c5-898536fe68e2/scratchpad/rv792c`
- SPEC7: `/tmp/claude-0/-home-user-tra-luat/f5ea9c29-b7bf-59b1-89c5-898536fe68e2/scratchpad/rv792c-out/spec-wp484-r7.md`
- SPEC8: `/tmp/claude-0/-home-user-tra-luat/f5ea9c29-b7bf-59b1-89c5-898536fe68e2/scratchpad/rv792c-out/spec-wp484-r8.md`
- VERDICT1: `/tmp/claude-0/-home-user-tra-luat/f5ea9c29-b7bf-59b1-89c5-898536fe68e2/scratchpad/rv792c-out/VERDICT-luot1.md`
- VERDICT2: `/tmp/claude-0/-home-user-tra-luat/f5ea9c29-b7bf-59b1-89c5-898536fe68e2/scratchpad/rv792c-out/VERDICT-luot2.md`
- Thư mục ra: `/tmp/claude-0/-home-user-tra-luat/f5ea9c29-b7bf-59b1-89c5-898536fe68e2/scratchpad/rv792c-out`
