# Cross-review độc lập — Packet #484 (wp484 r8/g7), PR #792, lượt 4 (chỉ H01)

Bạn là reviewer Codex, khác họ với executor g7 (Claude). Vai READ-ONLY với mã: KHÔNG sửa tệp nào trong `KHO`.
Chỉ ghi vào thư mục làm việc hiện tại; kết quả bắt buộc `VERDICT.md`, ghi SỚM rồi cập nhật. Không dùng credential
thật, không ghi `~/.codex` thật, không chạy installer thật (apt-get/cargo/npm/winget/choco) trên máy này.

Chủ kho nâng trần lời gọi Codex 3→4 CHỈ cho lượt này
(https://github.com/ducthangho/tra-luat/issues/484#issuecomment-6236261955), câu hỏi duy nhất: **sau lượt vá H01,
còn P2 nào mở không?** Trần attempt đã hết (4/4) — finding nào bạn nêu sẽ đến tay chủ kho, không có lượt vá tự động.

## Định danh

- `KHO` detached đúng head `0f31bb3e6151dd0cc67e8d4664b139259383b8d5` (tree `f6074ae53c0f4032eb17b56e01d432c5990c0065`).
  Head lượt 3: `cfd3550b6336eecb6847543a5f33200b57dd81ba`. Delta: `git -C KHO diff cfd3550 0f31bb3`
  (2 tệp, +24/−2: `.claude/dev/launcher_test.py` — chỉ fixture ca `r484_g2_hook_shell_scrub_truoc_probe`;
  `ops/handoff/wp484-g7-claude.md` mục "Lượt vá 4").
- Verdict lượt 3 `VERDICT3` (sha256 `9b0fef233238fec7007cc80a6eb5f5ac8bb4c58310da2ced1e50c83b29d0bfc4`): approve,
  P2=1 (H01). Lượt 1–2: `VERDICT1`, `VERDICT2`. Đặc tả `SPEC8` (sha256
  `4a512dd38721c3c4eec7978489ba06485feab32f94a0c5637a085d6c694ba38c`).
- Script đột biến của executor (tham khảo, KHÔNG phải bằng chứng — tự đo lại): `DOT_BIEN_EXECUTOR`.

## Nhiệm vụ

1. H01 đã đóng chưa? Đọc lại H01 trong `VERDICT3` và delta. Fixture nay có `rg` giả chạy được và `apt-get`/`sudo`/
   `cargo` giả (ghi nhật ký `CAI …`, thoát 97); phép so installer bắt `NPM `/`CAI `/`SACH -m pip`. Executor cố ý KHÔNG
   lọc PATH theo các tên này (vì `/usr/bin` chứa cả coreutils); `fakebin` đứng đầu PATH. Còn đường nào hook chạm
   installer/mạng/công cụ của máy chạy mà fixture không che (tên trần khác, đường dẫn tuyệt đối, `command -v` trỏ ra
   ngoài `fakebin`, biến môi trường kéo hành vi máy chạy)? Liệt kê từ CHÍNH `.claude/hooks/session-start.sh` tại head.
2. Ca còn răng không? Tự chạy đột biến trên BẢN SAO TẠM (không sửa `KHO`): ít nhất (a) `rg` giả hỏng ⇒ hook đi nhánh
   cài ⇒ ca phải ĐỎ đúng assertion "fixture gọi installer"; (b) như (a) nhưng gỡ `CAI ` khỏi phép so ⇒ ca phải XANH;
   (c) mọi đột biến tay lượt 3 trên ca này (gỡ `unset CODEX_AUTH_JSON` khỏi hook ⇒ ĐỎ) vẫn giết. Mỗi đột biến phải
   chết bởi assertion của CHÍNH ca, không phải lỗi vô can.
3. Hồi quy do delta (bất kỳ ca nào khác đổi màu; hạn ngạch `ops/bash_nen.py` cho `launcher_test.py` = 7 lời gọi bash
   trần; ruff F delta so `cfd3550` = 0).
4. ĐO. Executor khai (17-10, Linux): `launcher_test.py` 219/219 cả có/không `CODEX_AUTH_JSON` giả (2 ca Windows bỏ
   qua); ca H01 lặp 3/3; ruff F 5/5 (delta 0); `bash_nen quet` ĐẠT. CI Ubuntu trên `0f31bb3` xanh. Phép đo bị sandbox
   chặn thì ghi KHÔNG ĐO ĐƯỢC, đừng làm tròn.
5. Hướng thử cần soạn nội dung nhạy cảm thì mô tả bằng lời.

## Định dạng VERDICT.md

- Dòng 1 `Reviewed commit: 0f31bb3e6151dd0cc67e8d4664b139259383b8d5`; dòng 2 `Spec SHA-256: <SPEC8 tự đo>`;
  dòng 3 `verdict: approve|changes_requested`; dòng 4 `P0=… P1=… P2=… P3=…`.
- Bảng H01: trạng thái (đóng / đóng một phần / mở) + phép đo; finding mới mã J01…; bảng ≥ 4 hướng thử; "Đã đo";
  "KHÔNG ĐO ĐƯỢC".
- Ngưỡng `sensitive`: approve khi P0=0, P1=0 và mọi P2/P3 còn mở đã có quyết định chủ kho hoặc được bạn nêu rõ để chủ
  kho quyết. Nợ đã có quyết định (CAS, F01) không tính là finding mở. Câu hỏi của chủ kho là "đã hết P2 chưa" — trả
  lời thẳng câu ấy ở đầu phần thân.

## Đường dẫn

- KHO: `/tmp/claude-0/-home-user-tra-luat/f5ea9c29-b7bf-59b1-89c5-898536fe68e2/scratchpad/rv792d`
- SPEC8: `/tmp/claude-0/-home-user-tra-luat/f5ea9c29-b7bf-59b1-89c5-898536fe68e2/scratchpad/rv792d-out/spec-wp484-r8.md`
- VERDICT1: `/tmp/claude-0/-home-user-tra-luat/f5ea9c29-b7bf-59b1-89c5-898536fe68e2/scratchpad/rv792d-out/VERDICT-luot1.md`
- VERDICT2: `/tmp/claude-0/-home-user-tra-luat/f5ea9c29-b7bf-59b1-89c5-898536fe68e2/scratchpad/rv792d-out/VERDICT-luot2.md`
- VERDICT3: `/tmp/claude-0/-home-user-tra-luat/f5ea9c29-b7bf-59b1-89c5-898536fe68e2/scratchpad/rv792d-out/VERDICT-luot3.md`
- DOT_BIEN_EXECUTOR: `/tmp/claude-0/-home-user-tra-luat/f5ea9c29-b7bf-59b1-89c5-898536fe68e2/scratchpad/rv792d-out/executor-do_h01.py`
- Thư mục ra: `/tmp/claude-0/-home-user-tra-luat/f5ea9c29-b7bf-59b1-89c5-898536fe68e2/scratchpad/rv792d-out`
