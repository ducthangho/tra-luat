# Cross-review Codex — packet #910 (wp910 r3, CI-TIMEOUT-150 pha B), lượt 1/2

Bạn là REVIEWER (họ OpenAI) cho một bản vá do executor họ Claude viết. Lớp review: **sensitive** (workflow CI + cổng CI).
Kho: github.com/ducthangho/tra-luat. Bạn KHÔNG có mạng/GitHub; mọi thứ cần đo đã nằm trong thư mục này.

## Bố trí (thư mục làm việc hiện tại = gốc sandbox)
- `cay-kho/` — clone ở **head ứng viên** `a7da46390177cdc2d64f516dedac19857bee86dd` (nhánh `agent/wp910-g3-claude`).
- `nen/` — clone ở **base** `1797c32` (`origin/master` lúc rẽ nhánh; spec r3 đo trên `50a59a9`, giữa hai commit chỉ
  có tệp `ops/land/**` — tự kiểm bằng `git -C kho.git diff --stat 50a59a9 1797c32`).
- `kho.git/` — mirror bare.
- `evidence/spec-wp910.md` (r1, sha256 `2383ca2e540203e0b449e3f6118d84817f81984e937d463e99a7b862449a6613`),
  `evidence/spec-wp910-r2.md` (r2, `c3179d006b46fa82fe144cc1200dab72dbd9e88de28159f541504a7831dde7fc`),
  `evidence/spec-wp910-r3.md` (r3, `bb015dc66b08f9c559a0eecb1966558030991135bbf1a8004ac7108509a433bc`). r3 là DELTA trên
  r1 + r2 — đọc cả ba, tự đo lại ba băm.
- `evidence/lease.yaml` — lease `wp910-r3-g3-claude` (bản sao offline; đừng suy authority live từ nó).
- `evidence/diff.patch`, `evidence/numstat.txt` — diff base..head (4 tệp).
- `out/` — nơi DUY NHẤT bạn được ghi. KHÔNG sửa `cay-kho/`, `nen/`, `kho.git/`.

## Việc phải làm
1. Neo: `git -C cay-kho rev-parse HEAD 'HEAD^{tree}'`, như vậy với `nen`; tự băm ba spec; hai cây sạch đầu/cuối.
2. **N1/N2** — tự trích danh sách `(tệp, job, bước, timeout-minutes)` từ YAML đã parse của `ci.yml`,
   `ci-dot-bien-du.yml`, `launcher-windows.yml` ở base và head. Đúng 3 giá trị bảng r3 đổi thành 150; mọi timeout khác
   (job và bước) giữ nguyên. Diff hai workflow chỉ chạm đúng 3 dòng ấy.
3. **Hai hằng băm** — tự nạp `cay-kho/.claude/dev/ci_dang_ky_test.py` (bản sao trong `out/`) và gọi
   `bam_gate_nhanh()`, `bam_gate_registry()` trên `ci.yml` của HEAD ⇒ phải bằng `BAM_GATE_NHANH`, `BAM_GATE_REGISTRY`
   mới; gọi trên `ci.yml` của BASE ⇒ phải bằng hai hằng CŨ trong `nen/`. Diff của tệp này chỉ được chạm hai hằng và
   literal đột biến `timeout-trung`. Kiểm đột biến `timeout-trung` còn RĂNG: chuỗi neo mới phải xuất hiện đúng trong
   `ci-dot-bien-du.yml` của head (nếu không khớp thì ca `p651-M4-yaml-tho-timeout-trung` phải ĐỎ — thử trên bản sao).
4. **N3** — `actionlint` trên hai workflow ở base và head (nếu có công cụ); ghi rõ `shellcheck` có mặt không.
5. **N4** — trên BẢN SAO trong `out/` (không trên `cay-kho/`), head VÀ base:
   `PYTHONDONTWRITEBYTECODE=1 python3 -B .claude/dev/ci_dang_ky_test.py` (KHÔNG `--chay`; đọc `TỔNG:`) và
   `PYTHONDONTWRITEBYTECODE=1 python3 -B ops/ci_duong_nhanh_test.py` (đọc `CA:`, `DOT BIEN:`). Nếu sandbox chặn một ca vì
   lý do môi trường (socket, loopback…), so với base và ghi delta, đừng ghi xanh.
6. **Săn ≥ 3 hướng độc lập** (giả thuyết · lệnh · output thật · kết luận LỖI | KHÔNG PHẢI LỖI | KHÔNG ĐO ĐƯỢC). Gợi ý:
   hằng/ngưỡng khác phụ thuộc trần job (`GIAY_TOI_DA_MOT_BO` phải < 60 × timeout `gate-registry`; ca
   `p643-tran-bo-nho-hon-timeout-job`); test/công cụ nào khác ghim 30/105 của hai job này (kể cả lane chỉ chạy Windows
   hoặc chỉ chạy trên master); chú thích nêu giá trị cũ nay sai (chỉ ghi nhận — spec cấm sửa ngoài các dòng nêu);
   băm `BAM_GATE_REGISTRY` có bao env/defaults cấp workflow — bản vá có vô tình đổi gì ngoài timeout không.

## Bẫy đã biết
- `/tmp/.git` có thể là mount rỗng chỉ đọc dưới `codex-linux-sandbox`; đặt `TMPDIR` riêng dưới `out/tmp/`.
- Đừng ghi `.pyc`: dùng `-B` và `PYTHONDONTWRITEBYTECODE=1`. Không gọi mạng/GitHub; không `rm -rf` ngoài `out/`.

## Đầu ra — GHI SỚM, GHI TĂNG DẦN
Tạo ngay `out/VERDICT.md` với header dưới đây (verdict tạm `pending`) và cập nhật sau MỖI bước:

```
verdict: approve | changes_requested | pending
reviewed_head: a7da46390177cdc2d64f516dedac19857bee86dd
reviewed_sha: a7da46390177cdc2d64f516dedac19857bee86dd
reviewed_tree: <tree của head>
review_class: sensitive
provider: openai_codex
model: <model header CLI công bố>
model_family: openai
reasoning_effort: <effort header CLI công bố>
execution_surface: codex_cli
transport: machine
review_round: 1/2
```

Sau header: Kết luận · Neo và môi trường · Bảng finding (ID `F910B-NN`, mức P0–P3, tệp:dòng, bằng chứng, hướng sửa
BẰNG LỜI) · Bảng N1–N4 + hai hằng băm · Các hướng săn. `approve` chỉ khi không còn P0/P1/P2/P3 mở trong phạm vi bản vá;
thứ không đo được ghi `KHÔNG ĐO ĐƯỢC`. Không viết patch sản phẩm.
