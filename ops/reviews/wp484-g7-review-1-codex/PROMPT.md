# Cross-review độc lập — Packet #484 (wp484 r7/g7, hồi sinh #509 Codex credential refresh), PR #792, lượt 1

Bạn là reviewer Codex, khác họ với executor g7 (Claude). Vai READ-ONLY với mã: KHÔNG sửa tệp nào trong `KHO`.
Chỉ được ghi vào thư mục làm việc hiện tại (thư mục ra). Kết quả bắt buộc: tệp `VERDICT.md` trong thư mục ra.
Ghi `VERDICT.md` SỚM (khung + finding đầu tiên) rồi cập nhật dần — lượt bị ngắt vẫn giữ được phần đã ghi.
KHÔNG dùng credential thật trong bất kỳ phép thử nào; không chạy lệnh nào ghi vào `~/.codex` thật.

## Định danh (băm là định danh, không phải tên nhánh)

- Kho `ducthangho/tra-luat`, bản sao tại `KHO` (cuối prompt), checkout detached đúng head.
- Exact head: `99e79b107d4fd138dcd3e5ad51851a846fac9eb5` (tree `8c19048843e861c306d568e9f9f5ff63a2393ba9`),
  nhánh `agent/wp484-g7-claude`, PR #792.
- Base: `653fef3f52f3130dd6f597c1036430ffb807fef1` (`origin/master`). Diff PR: `git -C KHO diff 653fef3 99e79b1`
  (25 tệp, ~+2693/−260; phần lớn là công g2–g6 của Codex trên #509, chưa từng vào master).
- Head cũ của #509 (g6, Codex executor): `faaedff19af12063b9c1232e602e2e3fec479861`. Phần do g7 (Claude) thêm:
  merge `c874820` (master vào faaedff, 2 xung đột) và các commit `b794e71`, `c09eee8`, `99e79b1`.
  Xem riêng: `git -C KHO diff c874820 99e79b1` và `git -C KHO show c874820 --cc`.
- Đặc tả đóng băng r7: `SPEC` (cuối prompt), sha256 `35a81f47dbea985ed867147fbf952be485faf5c3106e9c8afed27a0b41a533e1`.
  Spec r6 (phạm vi g6) nằm trong cây: `ops/specs/wp-codex-credential-refresh.md` + `ops/specs/history/`.
  Handoff g7: `ops/handoff/wp484-g7-claude.md`. Lớp review: `sensitive`.

## Nhiệm vụ

1. Đọc spec r7 (`muc_tieu`, `nghiem_thu`, `dieu_kien_merge`) và handoff g7, rồi diff.
2. Trọng tâm A — phần g7:
   - Giải xung đột `.claude/hooks/session-start.sh`: khối chụp `TL_CODEX_SNAPSHOT` phải chạy TRƯỚC mọi lệnh ngoài
     (master thêm `GOC=…$(dirname …)` và `ghi_dau_vet_hook`). Thứ tự hiện tại đúng chưa? Còn lệnh ngoài nào chạy
     khi `CODEX_AUTH_JSON` còn trong môi trường không?
   - Giải xung đột `.claude/dev/launcher_test.py`: có ca hay mục `DOT_BIEN` nào của master hoặc của #509 bị mất/nhân đôi?
   - Bốn P2 (thread trên #509): (XLy) thay `auth.json` không CAS — g7 khai THU HẸP chứ không đóng, nợ
     `codex-auth-json-khong-cas`; (XL-) home chưa tạo ⇒ rc 3; (XMG) `_danh_dau_auth_hong` False không bị nuốt, ở
     `launcher._do_codex_song` VÀ `codex_cred.cmd_kiem`; (XML) `CODEX_HOME` sai ⇒ `Chan(13)` qua
     `_cho_snapshot_hoac_chan`. Bản vá có đúng, đủ mọi lối vào không (tìm lối thứ ba)? Lời khai trong comment/
     handoff có rộng hơn phép đo không?
   - Bộ test kín: dòng `os.environ.pop("CODEX_AUTH_JSON", None)` ở đầu `launcher_test.py` và ca
     `r484_g7_bo_test_kin_voi_credential_cua_phien`. Có ca nào cần biến mà nay mất răng? Có đường nào khác để bộ
     test thừa hưởng credential phiên (khoá chữ thường trên Windows, `env=` dựng từ đâu khác)?
3. Trọng tâm B — toàn diff PR so master: hành vi credential (`launcher.py`, `codex_cred.py`, `codex_env_policy.py`,
   `session_start.py`, `session-start.sh`, `launcher-windows.yml`) có fail-open, lộ bí mật, ghi ra ngoài
   `CODEX_HOME`, hay hồi quy so master không? Các ca master có bị đổi nghĩa không?
4. ĐO, đừng chỉ đọc. Có python3 trong PATH. Ví dụ:
   `cd KHO && PYTHONDONTWRITEBYTECODE=1 python3 -B .claude/dev/launcher_test.py --lap-ca <ca> --lan 1`;
   cả suite `python3 -B .claude/dev/launcher_test.py` (~25 phút); `python3 -B .claude/dev/codex_cred_test.py`.
   Executor khai (đo 17-10, Linux): launcher_test 214/214 cả khi CÓ và KHÔNG có `CODEX_AUTH_JSON` giả (bỏ qua 2 ca
   Windows-only `t62`, `r484_g4_windows_sid_alias_identity`); codex_cred_test nền 16/16, đột biến 16/16;
   packet_loop_test TỔNG ĐẠT; ruff F delta so master 0. Ba đột biến g7 trong `DOT_BIEN`
   (`g7_home_sai_lai_traceback`, `g7_nuot_loi_ghi_trang_thai`, `g7_bo_doc_lai_truoc_replace`) đo trên bản sao tạm,
   mỗi cái giết ca đích bằng assertion của chính ca.
5. Đột biến: KHÔNG sửa `KHO`. Chép ra thư mục tạm (`mktemp -d`) rồi sửa bản sao.
6. Hướng thử nào cần SOẠN nội dung nhạy cảm (đường dẫn thoát cây, mã khai thác) thì đừng soạn — mô tả bằng lời.

## Định dạng VERDICT.md

- Dòng đầu: `Reviewed commit: 99e79b107d4fd138dcd3e5ad51851a846fac9eb5`
- Dòng 2: `Spec SHA-256: <băm bạn tự đo trên SPEC>`
- Dòng 3: `verdict: approve` hoặc `verdict: changes_requested`; dòng 4: `P0=… P1=… P2=… P3=…`.
- Mỗi finding: mã (F01…), mức (P0–P3), tệp:dòng, mô tả, PHÉP ĐO đã chạy (lệnh + output thật cắt gọn), HINT patch nếu phức tạp.
- Bảng ≥ 6 HƯỚNG THỬ độc lập (giả thuyết · lệnh · output · LỖI / KHÔNG PHẢI LỖI / KHÔNG ĐO ĐƯỢC).
- Mục "Đã đo" (lệnh + rc), mục "KHÔNG ĐO ĐƯỢC" (thứ không đo được + lý do).
- Ngưỡng lớp `sensitive`: approve chỉ khi P0=0 và P1=0; mỗi P2/P3 còn mở phải nêu rõ để chủ kho quyết.

## Đường dẫn

- KHO: `/tmp/claude-0/-home-user-tra-luat/f5ea9c29-b7bf-59b1-89c5-898536fe68e2/scratchpad/rv792`
- SPEC: `/tmp/claude-0/-home-user-tra-luat/f5ea9c29-b7bf-59b1-89c5-898536fe68e2/scratchpad/rv792-out/spec-wp484-r7.md`
- Thư mục ra (ghi VERDICT.md ở đây): `/tmp/claude-0/-home-user-tra-luat/f5ea9c29-b7bf-59b1-89c5-898536fe68e2/scratchpad/rv792-out`
