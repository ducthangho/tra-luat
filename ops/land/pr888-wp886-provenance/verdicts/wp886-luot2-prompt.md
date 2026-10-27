# Cross-review Codex — packet #886 (wp886), revision 2, lượt 2/5

Bạn là REVIEWER (họ OpenAI) cho bản vá do executor họ Claude viết. Lớp review: **sensitive**. Không mạng/GitHub.

## Bố trí (cwd = gốc sandbox)
- `cay-kho/` — head ứng viên `1c138c714f9c192ea730b65c5d18ff5eda1ca660` (nhánh `agent/wp886-g1-claude`, PR #888).
- `nen/` — base `33e6d4c32d26663a87bbdd6f1350890fa6042cc5` (`origin/master` đã merge vào head; diff base..head = đúng 6 tệp của PR).
- `kho.git/` — mirror bare (nguồn là clone NÔNG, cảnh báo "shallow roots" là bình thường).
- `evidence/spec.md` (r1, sha256 `28d1bb708621c6d410aa2f22ba11f295a5a9407d74d7aa736ddd30421e4f96a6`) và
  `evidence/spec-r2.md` (DELTA r2, sha256 `c019dbbacf838cddac40da8b360a0564c9383a10a07821735a7f3366ef72d68b`) — tự băm lại.
- `evidence/lease.yaml` (lease r2, bản sao offline) · `evidence/diff.patch` · `evidence/numstat.txt`.
- `evidence/verdict-luot1.md` — verdict lượt 1 (approve phạm vi N1–N5 trên `a9be582`); đối chiếu trước khi săn mới.
- `evidence/EXECUTOR_GATES.md` — LỜI KHAI của executor, không phải bằng chứng.
- `out/` — nơi DUY NHẤT bạn được ghi. KHÔNG sửa `cay-kho/`, `nen/`, `kho.git/`.

Đọc: hai spec (r2 là delta: write set 6 tệp; trong `ops/cong_cu_test.py` CHỈ được sửa fixture
`python_alias_behavior_test`; tiêu chí N8), `cay-kho/CLAUDE.md` (bài học đột biến/tín dụng giả, hai vế A/B một lệnh,
`/tmp/.git`), diff.

## Thay đổi từ lượt 1
- Commit `7ce1b02`: chốt "mục PATH rỗng = cwd" trong `r886_n6` + đột biến `wp886_cc_bo_muc_PATH_rong` (gợi ý H01 lượt 1).
- Merge master (gồm #895 sửa nhiều chỗ khác của `ops/cong_cu_test.py`, KHÔNG thuộc PR).
- Commit `1c138c7` (r2): fixture `python_alias_behavior_test` — Windows tạo `python3.cmd` gọi `sys.executable`
  (luật native PATHEXT của N6 không nhận tên không đuôi), POSIX giữ symlink `python3`. Executor chọn `.cmd` thay symlink
  `python3.exe` vì chạy python qua symlink trên Windows chưa đo được; phiên điều phối xác nhận `.cmd` nằm trong r2.

## Việc phải làm
1. Neo head/base/tree, tự băm hai spec, cây sạch đầu/cuối.
2. Đối chiếu lượt 1: gợi ý H01 đã được đóng chưa (đột biến bỏ mục PATH rỗng phải bị `r886_n6` giết bằng TinHieuChotCa).
3. Kiểm phạm vi r2: diff `ops/cong_cu_test.py` base..head chỉ chạm `python_alias_behavior_test`; ≤ 6 tệp / ≤ 450 dòng thêm.
4. Chạy ca có sẵn (`PYTHONDONTWRITEBYTECODE=1 python3 -B .claude/dev/launcher_test.py --lap-ca <TEN> --lan 1`) trên head
   và trên base+test-head (hai vế dựng trong MỘT lệnh, bản sao thường trong `out/`): mọi `r886_*`, `r858_*`,
   `r802_runner_tra_lai_con_tro_nguoi_goi`. `ops/cong_cu_test.py` N/N trên head (bản sao; đọc dòng `cong_cu_test: N/M đạt`
   và `tiền kiểm bỏ qua=0`). Nếu bán kính đột biến quá lâu, ghi KHÔNG ĐO ĐƯỢC cho phần đó.
5. Fixture Windows: đánh giá bằng phép đo thuần Python (ví dụ dựng thư mục có `python3.cmd`, gọi
   `_python_theo_path(..., la_windows=True)` của `ops/cong_cu.py` để chắc tên ấy được giải; và tên không đuôi thì không).
   Không chạy được `.cmd` trên Linux thì ghi rõ phần đó KHÔNG ĐO ĐƯỢC; đừng suy runtime Windows.
6. Đột biến BẢN VÁ trên bản sao tạm: 10 `wp886_cc_*` có sẵn + tự nghĩ thêm. Chỉ `TinHieuChotCa` của ĐÚNG ca đích tính là giết.
7. N7: `release-verify RELEASE_MANIFEST.json --strict --json` (ok, expected==checked) và `tl.py --selftest` N/N.
8. Săn ≥ 6 hướng ĐỘC LẬP (giả thuyết · lệnh · output thật · kết luận). Gợi ý: quoting của `python3.cmd` khi
   `sys.executable` có khoảng trắng/ký tự đặc biệt; `%*` và đối số có dấu ngoặc kép; fixture còn đúng khi symlink bị
   cấm (nhánh `BoQuaMoiTruong`) trên POSIX; ảnh hưởng của merge master lên các ca r886; T7 "cac duong goi khac ban"
   khi PyYAML/jsonschema probe giải sang interpreter khác `python`. Hướng cần nội dung kiểu thoát cây thư mục thì mô tả bằng lời.

## Bẫy
- `/tmp/.git` có thể là mount rỗng chỉ đọc dưới `codex-linux-sandbox` ⇒ một số `r484_*`/`r858_goc_tam_*` đỏ giả; so base.
- `-B` và `PYTHONDONTWRITEBYTECODE=1`; TMPDIR riêng dưới `out/tmp/`. Không gọi mạng/GitHub; không `rm -rf` ngoài `out/`.
- Job Windows `gate`/`gate-packet-loop` đỏ ở bước cài `shellcheck` trên runner — không thuộc diff; đừng báo lại trừ khi bạn
  chứng minh được nó do diff.

## Đầu ra — GHI SỚM, GHI TĂNG DẦN vào `out/VERDICT.md`
```
verdict: approve | changes_requested | pending
reviewed_head: 1c138c714f9c192ea730b65c5d18ff5eda1ca660
reviewed_sha: 1c138c714f9c192ea730b65c5d18ff5eda1ca660
reviewed_tree: <tree của head>
review_class: sensitive
provider: openai_codex
model: <model header CLI công bố>
model_family: openai
reasoning_effort: <effort header CLI công bố>
execution_surface: codex_cli
transport: machine
review_round: 2/5
```
Sau header: Kết luận · Neo và môi trường · Đối chiếu lượt 1 · Bảng finding (ID `F886-NN`, mức P0–P3, tệp:dòng, bằng chứng,
hướng sửa BẰNG LỜI) · Bảng N1–N8 · Bảng đột biến · Các hướng săn. `approve` chỉ khi không còn P0/P1/P2/P3 mở trong phạm vi
bản vá; không đo được thì ghi `KHÔNG ĐO ĐƯỢC`, không ghi thành xanh. Không viết patch sản phẩm.
