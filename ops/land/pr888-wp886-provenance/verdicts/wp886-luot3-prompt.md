# Cross-review Codex — packet #886 (wp886), revision 2, lượt 3/5

Bạn là REVIEWER (họ OpenAI) cho bản vá do executor họ Claude viết. Lớp review: **sensitive**. Không mạng/GitHub.

## Bố trí (cwd = gốc sandbox)
- `cay-kho/` — head ứng viên `99b354ca7bcc40ce0c4f7d9db445b852510b5809` (PR #888).
- `nen/` — base `33e6d4c32d26663a87bbdd6f1350890fa6042cc5` (master đã merge vào head; diff base..head = đúng 6 tệp PR).
  Master sau đó tiến tới `2c11396`, chỉ thêm `CLAUDE.md` và `ops/land/**` — không chạm 6 tệp của PR (đọc `evidence/` nếu
  cần, nhưng đó không phải phạm vi review).
- `kho.git/` — mirror bare (clone nông; cảnh báo shallow là bình thường).
- `evidence/spec.md` (r1, sha256 `28d1bb708621c6d410aa2f22ba11f295a5a9407d74d7aa736ddd30421e4f96a6`),
  `evidence/spec-r2.md` (delta r2, sha256 `c019dbbacf838cddac40da8b360a0564c9383a10a07821735a7f3366ef72d68b`) — tự băm lại.
- `evidence/lease.yaml` (lease r2 offline) · `evidence/diff.patch` · `evidence/numstat.txt`.
- `evidence/verdict-luot1.md`, `evidence/verdict-luot2.md` — hai verdict trước; lượt 2 `pending` vì N8 Windows không đo
  được offline, không có finding.
- `evidence/delta-tu-luot2.patch` — đúng phần đổi từ head lượt 2 (`1c138c7`) tới head này: thêm chốt thứ tự PATH và ca
  POSIX `r886_n1_bo_qua_tep_khong_thuc_thi`, hai đột biến `wp886_cc_dao_thu_tu_PATH` / `wp886_cc_bo_X_OK` (gợi ý H06/H07
  lượt 2). Không đổi mã sản phẩm.
- `evidence/ci-readback/` — **bản đọc lại từ GitHub API của executor** (dữ liệu, không phải lời khai tự viết):
  `jobs-<run>.json` (tên job, `conclusion`, `labels`, `runner_id`, `head_sha`) cho ba run trên head này:
  `40050753537` (ci.yml, pull_request, Ubuntu), `40050767584` (ci.yml, workflow_dispatch `runner_set=windows-only`),
  `40050769532` (launcher-windows.yml, workflow_dispatch); cùng log đầy đủ của job `gate-cong-cu (windows-latest, 0)` và
  job launcher Windows. Hãy tự kiểm `head_sha` của từng job khớp head ở trên và `runner_id` khác 0.
- `out/` — nơi DUY NHẤT bạn được ghi.

## Việc phải làm
1. Neo head/base/tree, băm hai spec, cây sạch đầu/cuối.
2. Đối chiếu lượt 2: H06/H07 đã đóng chưa — `wp886_cc_bo_X_OK` phải bị `r886_n1_bo_qua_tep_khong_thuc_thi` giết và
   `wp886_cc_dao_thu_tu_PATH` bị `r886_n6` giết, bằng `TinHieuChotCa` đúng ca. Đếm lại số đột biến `wp886_cc_*` bằng AST.
3. N8 + M-3 + M-5 bằng `evidence/ci-readback/`: đọc log `gate-cong-cu (windows-latest, 0)` tìm dòng
   `cong_cu_test: N/M đạt; ... tiền kiểm bỏ qua=K` và kết luận về `python_alias_behavior_test`; liệt kê các dòng `BỎ QUA`
   và đánh giá chúng có phải giới hạn nền (so `evidence/verdict-luot2.md` / base) hay ca bị né. Đọc log launcher Windows:
   số ca, số đột biến, dòng `wp886_*`. Nói rõ bạn KHÔNG tự chạy được Windows — đây là đọc bằng chứng, không phải đo.
4. Chạy lại ca liên quan trên head (và base+test-head khi có nghĩa, hai vế một lệnh): mọi `r886_*`, `r858_cai_python_*`,
   `r802_runner_tra_lai_con_tro_nguoi_goi`. Đột biến trên bản sao tạm cho 11 `wp886_cc_*` + tự nghĩ thêm cho phần mới.
5. N7: `release-verify --strict` (ok, expected==checked) và `tl.py --selftest` N/N trên head.
6. Săn thêm ≥ 4 hướng ĐỘC LẬP mới (không lặp H01–H10 của lượt 2) cho phần đổi từ lượt 2 và cho toàn bản vá. Mỗi hướng:
   giả thuyết · lệnh · output thật · kết luận.

## Bẫy
- `/tmp/.git` có thể là mount rỗng chỉ đọc ⇒ `r858_goc_tam_*` đỏ giả; so base. `-B`, `PYTHONDONTWRITEBYTECODE=1`, TMPDIR
  riêng dưới `out/tmp/`. Không mạng; không `rm -rf` ngoài `out/`.
- Lượt chạy toàn bộ launcher/`cong_cu_test` bán kính rất lâu; ưu tiên ca đích và đột biến. Phần không chạy trọn ghi `KHÔNG ĐO ĐƯỢC`.

## Đầu ra — GHI SỚM, GHI TĂNG DẦN vào `out/VERDICT.md`
```
verdict: approve | changes_requested | pending
reviewed_head: 99b354ca7bcc40ce0c4f7d9db445b852510b5809
reviewed_sha: 99b354ca7bcc40ce0c4f7d9db445b852510b5809
reviewed_tree: <tree của head>
review_class: sensitive
provider: openai_codex
model: <model header CLI công bố>
model_family: openai
reasoning_effort: <effort header CLI công bố>
execution_surface: codex_cli
transport: machine
review_round: 3/5
```
Sau header: Kết luận · Neo · Đối chiếu lượt 2 · Bảng finding (ID `F886-NN`, P0–P3, tệp:dòng, bằng chứng, hướng sửa BẰNG
LỜI) · Bảng N1–N8 · Bảng đột biến · Hướng săn. `approve` khi không còn P0/P1/P2/P3 mở trong phạm vi bản vá và bằng chứng
CI đọc lại đủ cho N8/M-3; phần không đo được thì ghi `KHÔNG ĐO ĐƯỢC` kèm lý do, không ghi thành xanh. Không viết patch sản phẩm.
