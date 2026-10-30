# Handoff wp1045 — executor `claude` (phiên cloud), 30-10-2026

- Packet #1045 `CAI-CONG-CU-DAT-THEO-TRANG-THAI` r1 · lease `ops/leases/wp1045-r1-g2-claude.yaml` (g2, thay g1 sau `nang_tran`
  2→4 do chủ kho cho; g1 mang `da_bi_thay_the`) · đặc tả `ops/specs/wp1045.md`, sha256
  `8e187b9130e18a757f4f24dfcea6761f688a5f69e21d17356b198b8cc5bd508e`.
- Nhánh `agent/wp1045-g1-claude`, PR #1047, head **`201460203f42485f589add150896f2febc00c027`**. Diff so base `5e458f4` đúng hai
  tệp: `ops/cai_cong_cu.sh`, `.claude/dev/launcher_test.py`. Không merge/land, không force-push.

## Lịch sử nhánh
| commit | nội dung |
|---|---|
| `8828631` | `cong_cu_dat` quyết DAT theo `trang_thai` của chính công cụ (M1); gọi trực tiếp chưa DAT ⇒ thoát 3 (M2); ca + đột biến (M3/M4) |
| `daedfb7` | rig `truc_tiep` của r858 tách cả hàm helper + fail-close khi thiếu lệnh |
| `dcfef4d` | merge `origin/master` (chỉ `ops/land/**`) để `thu-hoi` thấy base là tổ tiên |
| `c3cdb8f` | vá Codex lượt 1: kiểm cuối không dừng trần dưới errexit · eval không vào ngữ cảnh điều kiện · khoá dọn tạm + mã gốc |
| `b07adcc` | ca hình dạng đổi mốc bằng `bang()` thay `sh.index` (ném `ValueError` = tín dụng giả) |
| `2014602` | vá Codex lượt 2 (P3): ca `r1045_bat_buoc_kiem_cuoi_luot_source_hong_thi_dung_ca_loat` + 2 đột biến |

## Nghiệm thu — đo trên `2014602`
- **A1** `launcher_test.py` — chạy qua `launcher-windows.yml` gọi tay `runner_set=windows-and-ubuntu`, run 41110458965:
  - `launcher (ubuntu-latest)` (job 124251225638): `312/312 ca DA CHAY QUA (tong 314, bo qua 2, hong 0)`;
    `DOT BIEN: 502/502 dat (4 khong do duoc tren nen nay)`. Mọi đột biến `wp1045_*` giết đúng ca đích (bảng trong log).
  - `launcher (windows-latest)` (job 124251225248): `255/255 ... (tong 314, bo qua 59, hong 0)`; `DOT BIEN: 410/410 dat (96
    khong do duoc)`. Bốn ca hành vi `r1045_*` dùng bash giả ⇒ `BO QUA shell POSIX` như các ca r858 cùng họ; ca hình dạng
    `r1045_hinh_dang_dat_theo_trang_thai` CHẠY và giết các đột biến hình dạng trên Windows. Bán kính đột biến hành vi chỉ đo trên Ubuntu.
  - Lượt PR thường KHÔNG chạy tệp này (workflow chỉ chạy trên PR có nhãn `windows`; `gate` không gọi nó) — vì thế phải gọi tay.
- **A2** phản chứng: ca (a)(b) của M3 ĐỎ với `cai_cong_cu.sh` của master (đo cục bộ trên bản sao đủ cây; Codex lượt 3 đo lại
  độc lập: bảng (a)–(d) head/base trong `luot3/VERDICT.md`).
- **A3** `ops/cong_cu_test.py` delta 0 so base (Codex lượt 3); `bash ops/cai_cong_cu.sh shellcheck` rc0, DAT.
- **A4** CI lượt PR `gate` run 41099144196: 23/23 job xanh, nhãn `ubuntu-latest`. Windows `gate` `workflow_dispatch`
  `runner_set=windows-only` run 41099486628: `conclusion: success`; `gate-cong-cu (windows-latest, 0)` và
  `gate-packet-loop (windows-latest)` xanh ở bước `cài shellcheck cho G5 (cài xong đo lại)` và bước `G5 …` — lỗi gốc của packet
  (runner Windows đỏ G5 vì thiếu shellcheck, đo ở run 41069257658 attempt 1) đã khỏi. `gate-cong-cu-gop` `skipped` đúng thiết kế.
  ruff F delta 0 · `git diff --check` rc0 · `doctrine-scan` rc0 (Codex lượt 3).

## Cross-review Codex — 3/4 lời gọi (trần g2)
`launcher.py run ... -- codex exec -m gpt-6-astra -c model_reasoning_effort=xhigh --sandbox workspace-write`. Hiện vật nguyên byte
ở `ops/handoff/wp1045-g1-claude/luot{1,2,3}/` (PROMPT, VERDICT, run/{run.json,checkpoint.json,stdout.log,stderr.log}) kèm
`SHA256SUMS`. Thư mục `evidence/` mà VERDICT trỏ tới nằm trong sandbox reviewer, KHÔNG chép (2,2 GB lượt 1, chủ yếu bản sao cây).

| lượt | run_id | head | thời lượng | model_phuc_vu | verdict | sha256 verdict |
|---|---|---|---|---|---|---|
| 1 | `d160eb1999444fcaa8e6c877deaedc6d` | `daedfb7` | 825.648 s, rc0 | `gpt-6-astra` | request_changes (1 P2, 2 P3) | `a94f5c8b…297cfe` |
| 2 | `f71a2bfc8420410584d516e14afd3e61` | `b07adcc` | 910.839 s, rc0 | `gpt-6-astra` | request_changes (1 P3) | `8b9755e0…7a2097` |
| 3 | `8381511e234e453d876e4dee7204ee75` | `2014602` | 836.55 s, rc0 | `gpt-6-astra` | **approve** (0/0/0/0) | `edf9683e…bd65f86` |

`effort_phuc_vu` cả ba: `xhigh`. Lượt 3: 16/16 đột biến đăng ký chết, 28/28 ca đích đỏ đúng `TinHieuChotCa`; 4 đột biến tự thêm
cũng chết. Launcher toàn suite trong sandbox reviewer có 13 ca đỏ CHUNG head/base (môi trường: `/var/tmp` chỉ đọc, `/tmp/.git`
rỗng) — delta 0, không quy cho bản vá.

## Việc còn lại
- Merge/land: chủ kho (`uy_quyen_merge: false`). Còn 1 lời gọi Codex trong trần g2, chưa dùng.
