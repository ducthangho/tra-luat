# Handoff wp1079 — executor `claude` (phiên cloud), 01-11-2026

- Packet #1079 `LAUNCHER-TEST-ORACLE-VA-FIXTURE` r1 · lease hiệu lực `ops/leases/wp1079-r1-g7-claude.yaml` (g1–g6 mang
  `da_bi_thay_the`) · đặc tả `ops/specs/wp1079.md`, sha256 `81070fa2c5a00bc0bb63867c7173f310cba9002001b68a26d62726ec904cbf5b`.
- Nhánh `agent/wp1079-g1-claude`, PR #1115, head **`af057e9`**. Diff so base `7eeb1d9` (chỉ `.claude/`; head có merge
  `origin/master`): `.claude/dev/launcher_test.py` +785/−111, `.claude/dev/codex_cred_test.py` +49/−7 (tổng **+834/−118**).
- **TRẦN DÒNG VƯỢT:** lease g7 cho 800, diff thật 834 (+34) — phần tăng là bản vá Codex lượt 6 (chủ kho duyệt "Vá 2 hàm, dừng
  gọi Codex") + ca khoá nhánh hook. CHƯA có quyết định nâng trần cho +34 này — chờ chủ kho.
- **M-1 CHƯA ĐẠT:** head cuối KHÔNG có verdict approve của Codex. Lượt 6/6 (cuối, trên `e3bcaf0`) còn 1 P1; bản vá của nó
  (`af057e9`) đúng nguyên mẫu Codex đã đo, nhưng chưa được Codex review. Chủ kho chọn dừng gọi Codex.
- Nợ tách: **#1117** (F04 lượt 2 — mã cấp module của bản test đột biến thấy nonce kênh trước `main`; lỗi kiến trúc).
- Không merge/land, không force-push.

## Quyết định của chủ kho (ghi hộ, băm byte KHÔNG ĐO ĐƯỢC)
| lease / lúc | quyết định |
|---|---|
| g1 | phạm vi: F01+F02 chung, #824–#826 để sau; F01 chỉ neutral + chấm theo loại (không cô lập process) |
| g2 | trần dòng 300→380 |
| g3 | trần dòng 380→480, gọi Codex 2/2 |
| g4 | vá F01/F05/F06/F07, F04 ghi nợ #1117; Codex 2→3, trần dòng 480→640 |
| g5 | vá F08, Codex 3→4; trần dòng 640→720 |
| g6 | cấm đăng ký ca trùng `__code__`, bỏ phép trừ F08; Codex 4→5 |
| g7 | vá (kiem_registry ở mọi điểm vào), Codex 5→6; trần dòng 720→800 |
| sau lượt 6 | "Vá 2 hàm, dừng gọi Codex" |

## Thiết kế cuối
- (a) nhánh sản phẩm `chay_dot_bien`: `cham_mot_ca` (chỉ `TinHieuChotCa` KHÔNG sinh trong ca đã đăng ký khác là `giet`) +
  `ket_luan_mutant` (neutral trên bản gốc; neutral đỏ ⇒ KHÔNG ĐO ĐƯỢC tính hỏng; ca đích thiếu/trùng ⇒ hỏng — F06).
- (b) nhánh harness: `cham_lap_ca` đọc KÊNH KẾT QUẢ (tệp + nonce, gỡ khỏi `os.environ` trước khi ca chạy), không đọc stdout;
  reporter ghi `TinHieuChotCa` chỉ khi `isinstance` và không từ ca khác, còn lại `khac:<qualname>`; bản sao harness giữ bố
  cục kho (`.claude/hooks`, `ops/bash_nen.py`, `codex_cred*.py`). Giới hạn đã khai: nợ #1117.
- (c) `codex_cred_test.chay_suite`: `ten_do(ten, e, ca)` — `TinHieuChotCa` riêng hoặc `assert` trần ở chính tệp, không từ
  ca khác; lỗi vô can mang `(<Loại>)`.
- `kiem_registry`: từ chối CA có hai ca chung `__code__` — gọi ở `ca`, đầu `chay_dot_bien` (nhánh hook gọi thẳng `fn()`),
  đầu `cham_mot_ca`/`chay_bo_ca` (TRƯỚC thân ca), trong `chot_tu_ca_khac`; `chay_suite` của codex_cred_test có chốt tương
  đương. Gọi thẳng `fn()` ở chỗ khác KHÔNG được che (khai trong docstring).
- F02: fixture N13 dựng môi trường cha THÙ ĐỊCH (rg hỏng, installer ghi `AMBIENT`, `BASH_ENV` ghi log); mọi installer giải về
  shim của fixture; HOME tạm; lọc `BASH_ENV`/`ENV`/`BASH_FUNC_*`; bước dò bash chạy dưới cùng env đã lọc.
- Sửa ca bị tín dụng giả: 28 `assert` trần → `bang` (r484_g2 ×2), 3 `raise AssertionError` → `TinHieuChotCa`; r01/r10 qua
  `_r1079_run_json`; t115 bọc `_doc_mcp_json`; r13 gọi helper chung `_t70_prompt_file_chan` (không gọi ca t70).

## Đính chính lời khai trong lịch sử commit
- `5548919` khai "5 dot bien moi" — SAI (Codex lượt 4 F09): thêm 4 tên (`wp1079_bo_kiem_ca_dich_vang`,
  `wp1079_bo_kiem_ca_khac`, `wp1079_bo_tien_to_khac`, `wp1079_cc_bo_kiem_ca_khac`) và sửa 3 hàng đã có.
- `5368c34` khai "Loi goi THAT ... (F05) van bi loai" — SAI (Codex lượt 4 F05).
- `c5acb70` khai F05/F08 "dong theo CAU TRUC" — SAI (Codex lượt 5: gán `CA` thẳng vượt qua).
- `e3bcaf0` khai "moi diem vao chay ca" — rộng hơn phép đo (Codex lượt 6: `cham_mot_ca`/`chay_bo_ca`).
- Đổi hình dạng lặp: F08 mở lại BA lần ở ba ranh giới (`@ca` → gán `CA` → hàm chạy ca) — đúng mẫu "vá đúng chỗ được chỉ rồi
  bỏ sót đường thứ ba" trong `CLAUDE.md`.

## Nghiệm thu — đo trên `af057e9` (Linux, phiên này, `/tmp/.git` vắng)
- **A1** `launcher_test.py`: `350/350 ca DA CHAY QUA (tong 352, bo qua 2, hong 0)` · `--dot-bien`: `548/548 dat (4 khong do
  duoc tren nen nay)` · `codex_cred_test.py`: `TỔNG: ĐẠT`.
- **A2** chỉ siết bộ chấm (a) trên các ca của base `7eeb1d9` ⇒ đúng 11 đột biến SAI (511/522): 5 chết bằng `assert` trần,
  6 bằng lỗi vô can (FileNotFoundError r01/r10; JSONDecodeError/TypeError ×2/AttributeError t115). Mỗi ca khoá mới đỏ trên
  head trước bản vá của nó (Codex đo cho các ca HINT, xem `luot*/VERDICT.md`).
- **A3** N13 với `rg` hỏng + installer ghi log: base gọi installer ngoài **7** lần mà ca PASS; head **0**.
- **A4** ruff F delta 0 (`launcher_test` 5/5, `codex_cred_test` 0/0) · `git diff --check` rc0 · `doctrine-scan` rc0 · CI PR
  #1115 trên `af057e9`: đọc check run (lúc ghi: 15 success, 8 đang chạy, 0 failure).
- CI head cũ `7df242e` có hai đỏ phụ thuộc thời gian KHÔNG lặp lại ở head sau: `t51` (`ops/cong_cu_test.py`, 5,93s > hạn
  2,5s) và `A11` (`ops/cloud_agent_creds_test.py`, neutral đỏ vì tiến trình con chưa dừng) — hai tệp ngoài diff.

## Cross-review Codex — 6/6 lời gọi
`launcher.py run ... -- codex exec -c model_reasoning_effort=xhigh --sandbox workspace-write`. Hiện vật nguyên byte ở
`ops/handoff/wp1079-g1-claude/luot{1..6}/` (PROMPT, VERDICT, HINT, run/{run.json,checkpoint.json,stdout.log,stderr.log}) kèm
`SHA256SUMS`. `luot1/chan-truoc-spawn/`: lần chạy bị launcher `CHAN [11]` TRƯỚC spawn (remote clone không phải GitHub) —
không gọi codex, không tính vào trần. HINT.patch giữ nguyên byte của reviewer.

| lượt | run_id | head | thời lượng | model_phuc_vu | verdict |
|---|---|---|---|---|---|
| 1 | `c15064fcc9ea462ebbf38cedff296bb8` | `c73dff3` | 1030.21 s | KHONG_DO_DUOC (`gpt-6.1-sol` trong danh sách) | changes_requested (0/2/1/0) |
| 2 | `e1593942232745bc95b140131c6a437b` | `d929ee2` | 1020.507 s | DO_DUOC `gpt-6.1-sol` | changes_requested (0/4/1/0) |
| 3 | `650afa538bae4e7da0e871ea3e853a8e` | `7df242e` | 1244.986 s | DO_DUOC `gpt-6.1-sol` | changes_requested (0/1/0/0) |
| 4 | `a3c032d75dc845928bc7ec5a6df8f587` | `5368c34` | 740.527 s | DO_DUOC `gpt-6.1-sol` | changes_requested (0/2/0/0) |
| 5 | `b8dccf08881c41c5865aa36c29f53542` | `c5acb70` | 1238.612 s | DO_DUOC `gpt-6.1-sol` | changes_requested (0/1/0/0) |
| 6 | `dc65e6da38724bdc83cabd478c976e30` | `e3bcaf0` | 1040.643 s | DO_DUOC `gpt-6.1-sol` | changes_requested (0/1/0/0) |

(P0/P1/P2/P3.) Ca HINT được nhận (khai `hint_provenance` trong commit): lượt 1 ×4, lượt 2 ×6 (bỏ ca F04), lượt 3 ×3 (sau gỡ
vì đổi thiết kế), lượt 4 ×1 (+2 thay bằng ca từ chối), lượt 5 ×2, lượt 6 ×2.

## Việc còn lại
- Chủ kho: quyết trần dòng (+34 so g7) và merge khi M-1 chưa đạt (`uy_quyen_merge: false`).
- Nợ #1117 (runner tin cậy ngoài mã bị đột biến); nợ cũ #824–#826 vẫn mở; nợ "cô lập process từng mutant" (spec Ngoài phạm vi).
- Sau merge: rút hạn lease g7.
