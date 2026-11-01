# Handoff wp1077 — executor `claude` (phiên cloud), 31-10 → 01-11-2026

- Packet #1077 `DOCTOR-ENOEXEC-BI-CHE` r1 · lease hiệu lực `ops/leases/wp1077-r1-g6-claude.yaml` (g6; g1–g5 mang
  `da_bi_thay_the`) · đặc tả `ops/specs/wp1077.md`, sha256 `eabbb725650addad531429d48801667f2ef05a6090c00123d1d4146c7b89c3f3`.
- Nhánh `agent/wp1077-g1-claude`, PR #1080, head **`ee3dc6d20d47becd0ab9379c22583bc5587c64b2`**. Diff so base `086f1b7` đúng hai
  tệp (`git diff --numstat 086f1b7..ee3dc6d`): `.claude/dev/launcher.py` +57/−9, `.claude/dev/launcher_test.py` +283/−11
  (tổng **+340/−20**, trần 345 sau `nang_tran_lan_4`). Không merge/land, không force-push.

## Quyết định của chủ kho trong packet (đều ghi hộ, băm byte KHÔNG ĐO ĐƯỢC)
| lease | quyết định |
|---|---|
| g2 | nâng trần Codex 2→4; THU HẸP phạm vi F1: `_git` và `_do_codex_song` không vá, tách #1083 |
| g3 | nâng trần Codex 4→5, trần dòng thêm 300→330 |
| g4 | nâng trần Codex 5→10 |
| g5 | miễn trừ **W-1077-1** (`$0` của shebang qua phần tử PATH rỗng là `./<tên>`); trần dòng 330→345 |
| g6 | mở rộng W-1077-1 sang ứng viên cwd sinh từ phần tử PATH QUÁ DÀI (cùng cơ chế) |

## Thiết kế cuối (`_chay_probe_nhu_shell`)
Duyệt PATH theo `__execvpe` glibc: ứng viên `<phần tử>/<tên>` giữ nguyên dạng (giữ `/` cuối ⇒ `bin//tên`); phần tử rỗng, hoặc
quá dài nhưng không phải cuối ⇒ ứng viên cwd `<tên>` (execve qua `./<tên>` — W-1077-1); phần tử cuối quá dài bị bỏ. Chỉ
EACCES/ENOENT/ESTALE/ENOTDIR/ENODEV/ETIMEDOUT sang ứng viên sau; ENOEXEC ⇒ `/bin/sh` chạy CHÍNH chuỗi ứng viên; lỗi khác ném ngay;
hết ⇒ EACCES nếu từng gặp. `executable=` giữ `argv[0]`. Đo độ dài bằng `os.fsencode`. Windows giữ nguyên `subprocess.run`.
Phạm vi: probe CLI của `CONG_CU`/`KHA_NANG` (`_phien_ban`, `_xac_thuc_kem_dau_ra`, codex login status, llm ×3, gh auth status,
gh api, claude mcp get); CHƯA phủ `_git`, `_do_codex_song` — #1083.

## Đính chính lời khai trong lịch sử commit (Codex F5/F6)
- `dcfb011` khai "+228 dòng" — SAI; đo `086f1b7..dcfb011`: 2 tệp, +236/−19.
- `57e2d4a` khai "t103/t113 không so tên lệnh" — SAI cho `t103` (có phép so `cmd[:2] == ["gh","api"]`, hai nhánh cùng `Rc(0)`).
- `e61def4` khai "như bash/execvp" — SAI (bash chạy lại bằng chính bash); `01b9734` khai "như execvp glibc" — rộng hơn hành vi
  (ETXTBSY/ELOOP), sửa ở `c4af726`.

## Nghiệm thu — đo trên `ee3dc6d` (Linux, phiên này)
- **A1** `python3 .claude/dev/launcher_test.py`: `323/323 ca DA CHAY QUA (tong 325, bo qua 2, hong 0)` — 2 ca bỏ qua là ca
  Windows. `--dot-bien`: `DOT BIEN: 518/518 dat (4 khong do duoc tren nen nay)`; 16 đột biến `wp1077_*` giết đúng ca đích, không
  ca nào chết bằng ngoại lệ ngoài assertion (lượt 10 đo độc lập: 22/22 cặp `TinHieuChotCa`).
- **A2** phản chứng: mỗi ca mới ĐỎ trên head TRƯỚC bản vá của nó (base `086f1b7` cho ca M3; `dcfb011`/`57e2d4a`/`1027f85`/
  `4fa4720`/`01b9734`/`7879902` cho các ca F4 lần lượt) — lệnh và output trong commit message từng lượt.
- **A3** `doctor` tại chỗ với `rg` không shebang đầu PATH: base rc=12 `BI_CHE`, head rc=0 `co rg`.
- **A4** ruff F delta 0 (launcher 0/0, launcher_test 5/5) · `git diff --check` rc0 · `doctrine-scan` rc0 · CI lượt PR trên
  `ee3dc6d`: xem PR #1080 (đọc check run, không suy).
- Bẫy môi trường: khi Codex chạy song song, `/tmp/.git` rỗng làm đỏ 11 ca `r484_*` — mọi số A1 ở trên đo khi `/tmp/.git` vắng.

## Cross-review Codex — 10/10 lời gọi (trần g4–g6)
`launcher.py run ... -- codex exec -c model_reasoning_effort=xhigh --sandbox workspace-write`. Hiện vật nguyên byte ở
`ops/handoff/wp1077-g1-claude/luot{1..10}/` (PROMPT, VERDICT, HINT nếu có, run/{run.json,checkpoint.json,stdout.log,stderr.log})
kèm `SHA256SUMS`. Thư mục `evidence/` của reviewer KHÔNG chép (nằm trong sandbox reviewer, phần lớn là bản sao cây).

| lượt | run_id | head | thời lượng | model_phuc_vu | verdict | sha256 verdict |
|---|---|---|---|---|---|---|
| 1 | `0957f9a38dd54e86a0942c39f248c030` | `e61def4` | 1315.941 s, rc0 | DO_DUOC `gpt-6.1-sol` | changes_requested (0 P0, 2 P1, 1 P2, 0 P3) | `f8b45110…0e9694` |
| 2 | `bc1b29d6c305427fa0cd9befcfe917a4` | `dcfb011` | 1413.598 s, rc0 | DO_DUOC `gpt-6.1-sol` | changes_requested (0 P0, 3 P1, 0 P2, 0 P3) | `cbd15d7e…b2ecd3` |
| 3 | `ceb22db5cc524d8f901d95cd0b7abc0d` | `57e2d4a` | 1522.451 s, rc0 | DO_DUOC `gpt-6.1-sol` | changes_requested (0 P0, 2 P1, 0 P2, 0 P3) | `ab9ea553…8bdb2d` |
| 4 | `46882d3c4101482c8dd4fe3d1b9db994` | `1027f85` | 1467.247 s, rc0 | DO_DUOC `gpt-6.1-sol` | changes_requested (0 P0, 1 P1, 1 P2, 0 P3) | `438d21f7…e47ed4` |
| 5 | `016195d4bb3c4086a397e551296cc7ff` | `4fa4720` | 1931.702 s, rc0 | DO_DUOC `gpt-6.1-sol` | changes_requested (0 P0, 1 P1, 0 P2, 0 P3) | `0742fc0b…b8d9f0` |
| 6 | `287b2a60d309476f92c2fbf69f00ae2e` | `01b9734` | 1698.68 s, rc0 | DO_DUOC `gpt-6.1-sol` | changes_requested (0 P0, 1 P1, 0 P2, 0 P3) | `e6b6eb9f…b9acdf` |
| 7 | `763c03a558ad4143a3d326b50fbcc0d8` | `c4af726` | 1522.101 s, rc0 | KHONG_DO_DUOC `gpt-6.1-sol` | changes_requested (0 P0, 1 P1, 0 P2, 0 P3) | `c034f94e…a02bb7` |
| 8 | `c491c7bb6dfe405093d0c454af2c498a` | `7879902` | 1279.399 s, rc0 | DO_DUOC `gpt-6.1-sol` | changes_requested (0 P0, 1 P1, 1 P2, 0 P3) | `438d0156…2d7c77` |
| 9 | `be389b81233248469d95479301b250a9` | `457e413` | 1258.797 s, rc0 | DO_DUOC `gpt-6.1-sol` | changes_requested (0 P0, 1 P1, 0 P2, 0 P3) | `c7638a5e…688a9a` |
| 10 | `5cfca6a99b7b411bbb7b9cc89bed47a6` | `ee3dc6d` | 1046.117 s, rc0 | DO_DUOC `gpt-6.1-sol` | approve (0 P0, 0 P1, 0 P2, 0 P3) | `995bea5d…2aae27` |

Lượt 7: `model_phuc_vu_trang_thai = KHONG_DO_DUOC` (một dòng khung response không đọc được; danh sách thiếu) — họ model của
lượt ấy không được khai là đã đo. Lượt 10 (approve) đo được: `gpt-6.1-sol`.

## Việc còn lại
- Merge/land: chủ kho (`uy_quyen_merge: false`).
- #1078 (`cai_cong_cu.sh` chọn Python): spec sẵn ở `ops/specs/wp1078.md`; cấp lease khi lease này nhả `launcher_test.py`.
- #1083: `_git` và `_do_codex_song` (phần F1 không vá).
