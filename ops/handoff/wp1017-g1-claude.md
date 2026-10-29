# Handoff wp1017 g1 — executor `claude` (phiên cloud), 29-10-2026

- Packet #1017 `BIEN-NHAN-V2-TEST-WINDOWS` r1 · lease `ops/leases/wp1017-r1-g1-claude.yaml` @ `9b412e4` (bản chiếu
  https://github.com/ducthangho/tra-luat/issues/1017#issuecomment-6492448145) · đặc tả `ops/specs/wp1017.md` @ `649541d`,
  sha256 `e1e709be14e2e7c2a81de39c3acf2666c746e7146116dee669cadee4dad8ed19`.
- Phiên ghi lease CŨNG là executor (chỉ thị chủ kho trong phiên `session_015GtxrYjGJtmjF3eT1nCSG9`).
- Nhánh `agent/wp1017-g1-claude`, PR draft #1018, head **`8036ddb47a2e769703cc897798b3ba2182389c49`**. Diff đúng 1 tệp
  `ops/bien_nhan_v2_test.py` (+225/−35 so base `e9967f0`). Không merge/land, không force-push.

## Lịch sử nhánh
| commit | nội dung |
|---|---|
| `b2e2410` | M1 fixture LF (`_kho_cau`, c93); M2 c91 tên quá dài đo nền + nguồn tiêm lstat; M3 c96 probe PATH + biến thể tiêm |
| `c949c91` | vá Codex lượt 1 (P2): `_tiem_git` theo module hiện hành, nguồn tiêm mức module, ca `c97`; c91 `cau_hinh_canh_bao` probe + tiêm |
| `8036ddb` | nguồn THẬT của c91 chạy được trên Windows: `core.fsync=<lạ>`, thành phần `<`; tạo sẵn `ops/reviews` |

## Gốc lỗi (đo)
- c93/c91: chế độ văn bản Python đổi `\n`→`\r\n` trên Windows. Tái hiện trên Linux bằng byte CRLF ra đúng
  `5cfd3f5e87ecd0877a62d75e22c3cf005d842524` / `70363d663b5f549bdc70e2b0ce3838c2ad43ffd7` của log CI.
- c91 tên quá dài: Windows ENOENT. Ký tự cấm `<` cho WinError 123/EINVAL (số đo của phiên #1014 trên máy Windows chủ kho).
- c91 `cau_hinh_canh_bao`: git for Windows 2.55.0.windows.5 KHÔNG cảnh báo `core.fsyncObjectFiles` (tôi đo trực tiếp trên laptop:
  rc=0, stderr rỗng; git 2.43 Linux có cảnh báo). `core.fsync=<thành phần lạ>` cảnh báo trên cả hai nền.
- c96: git giả `#!/bin/sh` không đuôi — `CreateProcess` chỉ tìm `git.exe`.

## Tiêu chí — đo trên `8036ddb`
- **A1 Linux**: `python3 ops/bien_nhan_v2_test.py` ⇒ `94/94 ca đạt · 137/137 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM`, `TỔNG: ĐẠT`,
  0 dòng `GHI CHÚ` (Linux dựng được mọi nguồn thật).
- **A1 Windows (CI)**: `workflow_dispatch` windows-only run 40853717478, job `gate-ops (windows-latest)` ⇒ `bien-nhan v2 selftest`
  `94/94 · 137/137 · TỔNG: ĐẠT`. Bước sau (`lease-publish selftest`) nay chạy được và đỏ đúng **t27** của #1006 (`253/254`) — lỗi của
  #1006, vá ở PR #1007, ngoài write set này (comment issuecomment-6494386439 trên #1018).
- **A1 Windows (laptop chủ kho)**: **KHÔNG ĐO ĐƯỢC.** Giữ khoá `D:\tl-win\KHOA.txt` từ 09:24:55Z; lượt nền master `e9967f0` (PID 836)
  chạy từ 09:27Z trong lúc có 2 `bien_nhan_v2_test` của phiên khác chạy song song (PID 17016, 22884); Desktop Commander ngừng phản
  hồi ~09:58Z, máy offline từ ~09:53Z. Không có số nào ⇒ không ghi `do-luong.csv`. Khoá đã báo phiên điều phối là hết hiệu lực.
- **A2** răng (bản sao đủ cây; driver chạy đúng ca qua `_chay_1`):
  | đột biến | kết quả |
  |---|---|
  | tắt biến thể thật + m116 | c91 ĐỎ tại `run_json_lstat_loi_tiem` |
  | tắt biến thể thật + m125 | c96 ĐỎ tại `merge-base/tiem` |
  | gốc + m116 / m125 | ĐỎ tại biến thể thật (`run_json_ten_qua_dai`, `merge-base/path`) |
  | ghi CRLF trong `_kho_cau` | c93 `gian_giao` đúng SHA của Windows |
  | `_tiem_git` vá `_BNV2_THAT` · không gỡ `Path.lstat` · không gỡ `_chay_git` · tiêm khớp mọi lệnh | c97 ĐỎ đúng chốt từng cái |
- **A3** ruff F: 1 F541 base và head ⇒ delta 0 · `git diff --check` rc0 · `doctrine-scan` rc0 · `bien_nhan_v2 --root .` `TỔNG: ĐẠT`.
- **A4** CI lượt PR (Ubuntu) run 40853716224 trên `8036ddb`: xanh toàn bộ (gồm `gate-ops`, `gate-packet-loop`, `gate-registry`).

## Cross-review Codex — 2/2 lời gọi (trần lease)
`launcher.py run ... -- codex exec -m gpt-6-astra -c model_reasoning_effort=xhigh --sandbox workspace-write`. Hiện vật nguyên byte ở
`ops/handoff/wp1017-g1-claude/` (SHA256SUMS kèm). `model_phuc_vu` cả hai lượt DO_DUOC.

| lượt | run_id | head | thời lượng | model_phuc_vu | verdict | sha256 verdict |
|---|---|---|---|---|---|---|
| 1 | `3812cda47ec1435191836ad4d1182949` | `b2e2410` | 1159.139 s, rc0 | `gpt-6-astra` 30/30, `xhigh` | request_changes (1 P2) | `538cb520…f65b43c` |
| 2 | `a2dd257c4cf84810a4833797ce91e8c0` | `8036ddb` | 1184.429 s, rc0 | `gpt-6-astra` 47/47, `xhigh` | **approve** (0/0/0/0) | `47e87131…e3426988` |

Lượt 2 ghi bốn đột biến CỦA MÃ TEST còn SỐNG, xếp là giới hạn độ phủ (không phải finding):
1. bỏ cặp đối chứng vô hại của c97 (ca không tự khoá việc xoá đối chứng của nó);
2. bỏ probe cảnh báo `core.fsync` (tương đương trên git có cảnh báo);
3. thành phần `<` dùng dấu của thành phần dài (POSIX không tới thành phần thứ hai);
4. bỏ `mkdir ops/reviews` — **đáng chú ý nhất**: Linux lặng lẽ lùi về nguồn tiêm, có `GHI CHÚ` nhưng suite vẫn xanh.
Không vá thêm: hết trần lời gọi Codex và mọi commit mới mất neo verdict approve. Đề xuất cho packet sau: chốt "trên POSIX, nguồn thật
của c91/c96 PHẢI dựng được" (đếm `GHI CHÚ` = 0 trên Linux) để (4) đỏ.

## Việc còn lại
- t27 trên Windows: cần #1006 và #1017 cùng có mặt; merge một trong hai vào master rồi merge master vào cái còn lại và gọi lại
  `workflow_dispatch` windows-only.
- Merge/land: chủ kho (`uy_quyen_merge: false`). Điều kiện merge mới của chủ kho (hết P1/P2/P3; hết lỗi Windows local nếu đã chạy):
  Codex lượt 2 không còn finding; Windows CI xanh ở phần của packet này; laptop không đo được.
