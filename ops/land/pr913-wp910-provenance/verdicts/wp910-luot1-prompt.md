# Cross-review Codex — packet #910 (wp910 r2, CI-TIMEOUT-150 pha A), lượt 1/2

Bạn là REVIEWER (họ OpenAI) cho một bản vá do executor họ Claude viết. Lớp review: **sensitive** (workflow CI).
Kho: github.com/ducthangho/tra-luat. Bạn KHÔNG có mạng/GitHub; mọi thứ cần đo đã nằm trong thư mục này.

## Bố trí (thư mục làm việc hiện tại = gốc sandbox)
- `cay-kho/` — clone ở **head ứng viên** `6e09f4b013629ae3d8d6e75f1a1c8e10aaa960b4` (nhánh `agent/wp910-g1-claude`).
- `nen/` — clone ở **base** `e739ac1b74024a20949425c447fb6cf025317c0e`.
- `kho.git/` — mirror bare.
- `evidence/spec-r1.md` (sha256 `2383ca2e540203e0b449e3f6118d84817f81984e937d463e99a7b862449a6613`) và
  `evidence/spec-r2.md` (sha256 `c3179d006b46fa82fe144cc1200dab72dbd9e88de28159f541504a7831dde7fc`) — r2 là DELTA, đọc cả hai.
  Tự đo lại hai băm.
- `evidence/lease.yaml` — lease `wp910-r2-g2-claude` (bản sao offline; đừng suy authority live từ nó).
- `evidence/diff.patch`, `evidence/numstat.txt` — diff base..head.
- `out/` — nơi DUY NHẤT bạn được ghi. KHÔNG sửa `cay-kho/`, `nen/`, `kho.git/`.

## Việc phải làm
1. Neo: `git -C cay-kho rev-parse HEAD 'HEAD^{tree}'`, như vậy với `nen`; tự băm hai spec; hai cây sạch đầu/cuối.
2. **N1/N2** — tự trích danh sách `(tệp, job, bước, timeout-minutes)` từ YAML đã parse của `.github/workflows/ci.yml` và
   `.github/workflows/launcher-windows.yml` ở base và head. Đúng 4 giá trị bảng r2 đổi thành 150; `gate-nhanh-manh` giữ 30;
   mọi timeout khác (job và bước) giữ nguyên. `git diff` của hai workflow chỉ chạm đúng 4 dòng ấy.
3. **N3** — `actionlint` trên hai workflow ở base và head (nếu có công cụ); ghi rõ `shellcheck` có mặt không.
4. **N4** — trên BẢN SAO trong `out/` (không trên `cay-kho/`), head VÀ base:
   `PYTHONDONTWRITEBYTECODE=1 python3 -B ops/ci_duong_nhanh_test.py` (đọc dòng `CA:` và `DOT BIEN:`) và
   `PYTHONDONTWRITEBYTECODE=1 python3 -B .claude/dev/ci_dang_ky_test.py` (KHÔNG `--chay`; đọc `TỔNG:`).
   Kiểm đột biến `yml_gate_timeout_1_phut` trên head còn RĂNG: mỏ neo literal mới khớp đúng job `gate` và đột biến vẫn
   giết đúng ca `y13_khoa_topology_cua_ci_yml_ngoai_than_run` (thử gỡ/đổi neo trên bản sao để thấy nó thành vô hiệu thì ĐỎ).
5. **Săn ≥ 3 hướng độc lập** (giả thuyết · lệnh · output thật · kết luận LỖI | KHÔNG PHẢI LỖI | KHÔNG ĐO ĐƯỢC). Gợi ý:
   có test/công cụ nào khác trong kho ghim giá trị timeout cũ (60/120/40) của các job này mà chưa được cập nhật, hoặc
   chỉ chạy trên Windows/lane LAND nên lượt PR Ubuntu không thấy; chú thích trong ci.yml/launcher-windows.yml nêu giá trị
   cũ mà nay sai (chỉ ghi nhận — spec cấm sửa ngoài dòng timeout); `gate-nhanh-manh` có thực sự giữ nguyên byte;
   timeout 150 có vượt giới hạn nào của GitHub Actions hay của job phụ thuộc (`needs`) không; phép băm khác
   (`BAM_GATE_REGISTRY`…) có bao trùm các job đã đổi không.

## Bẫy đã biết
- `/tmp/.git` có thể là mount rỗng chỉ đọc dưới `codex-linux-sandbox`; đặt `TMPDIR` riêng dưới `out/tmp/`.
- Đừng ghi `.pyc`: dùng `-B` và `PYTHONDONTWRITEBYTECODE=1`. Không gọi mạng/GitHub; không `rm -rf` ngoài `out/`.

## Đầu ra — GHI SỚM, GHI TĂNG DẦN
Tạo ngay `out/VERDICT.md` với header dưới đây (verdict tạm `pending`) và cập nhật sau MỖI bước:

```
verdict: approve | changes_requested | pending
reviewed_head: 6e09f4b013629ae3d8d6e75f1a1c8e10aaa960b4
reviewed_sha: 6e09f4b013629ae3d8d6e75f1a1c8e10aaa960b4
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

Sau header: Kết luận · Neo và môi trường · Bảng finding (ID `F910-NN`, mức P0–P3, tệp:dòng, bằng chứng, hướng sửa
BẰNG LỜI) · Bảng N1–N4 · Các hướng săn. `approve` chỉ khi không còn P0/P1/P2/P3 mở trong phạm vi bản vá; thứ không đo
được ghi `KHÔNG ĐO ĐƯỢC`. Không viết patch sản phẩm.
