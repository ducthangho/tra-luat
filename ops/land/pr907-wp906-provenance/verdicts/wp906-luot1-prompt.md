# Cross-review Codex — packet #906 (wp906, CONG-CU-YAML-CHU-THICH), lượt 1/2

Bạn là REVIEWER (họ OpenAI) cho một bản vá do executor họ Claude viết. Lớp review: **sensitive** (cổng lease tính
`ops/cong_cu.yaml` là tệp công cụ của gate, dù diff chỉ là chú thích). Kho: github.com/ducthangho/tra-luat.
Bạn KHÔNG có mạng/GitHub; mọi thứ cần đo đã nằm trong thư mục này.

## Bố trí (thư mục làm việc hiện tại = gốc sandbox)
- `cay-kho/` — clone ở **head ứng viên** `35d87eb073ae8c6f79049c0097b4208cc2139c47` (nhánh `agent/wp906-g1-claude`).
- `nen/` — clone ở **base** `1c20f3bd6a7ed08114feaf1d91c0790360b8f581` (`origin/master` lúc cấp lease).
- `kho.git/` — mirror bare.
- `evidence/spec.md` — đặc tả ĐÓNG BĂNG, sha256 phải là `683d648a678e93ec874d32e9d611aca88d756cd2088391ddbfb406d807452337` (tự đo lại).
- `evidence/lease.yaml` — lease `wp906-r1-g1-claude` (bản sao offline; đừng suy authority live từ nó).
- `evidence/diff.patch`, `evidence/numstat.txt` — diff base..head.
- `out/` — nơi DUY NHẤT bạn được ghi. KHÔNG sửa `cay-kho/`, `nen/`, `kho.git/`.

Đọc trước: `evidence/spec.md` (nguồn sự thật: N1–N3, mục Cổng, Q1–Q5) và diff.

## Việc phải làm
1. Neo: `git -C cay-kho rev-parse HEAD 'HEAD^{tree}'`, như vậy với `nen`; tự băm spec; hai cây sạch đầu/cuối.
2. **N1** — đọc câu chú thích mới trong `cay-kho/ops/cong_cu.yaml` (khối dưới `git.cai`) và ĐỐI CHIẾU với mã thật:
   `cay-kho/ops/cong_cu.py` (`TEN_PYTHON`, `_python_theo_path`, `_chay`) và dòng chọn `PY` trong `cay-kho/ops/cai_cong_cu.sh`.
   Câu có nói đúng hành vi hiện hành (thứ tự tên, không rơi về `sys.executable`) không? Có trỏ đúng nợ đã đóng
   (#886 / PR #888) không? Phần câu về `chon_thu_muc_chay_duoc` (wp858 L1) có giữ nghĩa không? Có lời khai nào RỘNG
   hơn mã (ví dụ nói `py -3` trên mọi nền) không?
3. **N2** — tự đo: `yaml.safe_load` của `nen/ops/cong_cu.yaml` và `cay-kho/ops/cong_cu.yaml` phải `==`; mọi dòng đổi
   trong `git -C cay-kho diff 1c20f3b HEAD -- ops/cong_cu.yaml` phải bắt đầu bằng khoảng trắng + `#`.
4. **N3** — không dòng nào khác đổi, kể cả kết thúc dòng/khoảng trắng cuối (so byte ngoài hai dòng ấy; kiểm CRLF/LF,
   newline cuối tệp). Diff PR đúng 1 tệp.
5. Cổng (trên BẢN SAO trong `out/`, không trên `cay-kho/`): `PYTHONDONTWRITEBYTECODE=1 python3 -B ops/cong_cu.py kiem-tra --json`
   trên head VÀ base (so delta; thiếu `shellcheck` là nền máy, không phải lỗi bản vá); `python3 .claude/dev/packet_loop.py
   doctrine-scan --root .`; `git config core.abbrev 7` rồi `python3 scripts/tl.py doc-claims-check --strict`.
   `ops/cong_cu_test.py` rất lâu (hàng trăm đột biến) — chạy nếu kịp, ghi `KHÔNG ĐO ĐƯỢC` nếu không, đừng ghi xanh.
6. **Săn ≥ 3 hướng độc lập** (giả thuyết · lệnh · output thật · kết luận LỖI | KHÔNG PHẢI LỖI | KHÔNG ĐO ĐƯỢC). Gợi ý:
   có công cụ/test nào đọc NỘI DUNG CHÚ THÍCH của `cong_cu.yaml` (grep chuỗi nợ, doc-claims, doctrine-scan) mà bản vá
   làm đổi kết quả; chuỗi `python-probe-khong-theo-PATH` còn được nhắc ở đâu khác trong kho với nghĩa "đang mở";
   ký tự Unicode (`→`, `·`) có làm hỏng bộ đọc nào chạy trên Windows/cp1258 không; độ dài dòng so với các dòng lân cận.

## Bẫy đã biết
- `/tmp/.git` có thể là mount rỗng chỉ đọc dưới `codex-linux-sandbox`; đặt `TMPDIR` riêng dưới `out/tmp/`.
- Đừng ghi `.pyc`: dùng `-B` và `PYTHONDONTWRITEBYTECODE=1`. Không gọi mạng/GitHub; không `rm -rf` ngoài `out/`.

## Đầu ra — GHI SỚM, GHI TĂNG DẦN
Tạo ngay `out/VERDICT.md` với header dưới đây (verdict tạm `pending`) và cập nhật sau MỖI bước:

```
verdict: approve | changes_requested | pending
reviewed_head: 35d87eb073ae8c6f79049c0097b4208cc2139c47
reviewed_sha: 35d87eb073ae8c6f79049c0097b4208cc2139c47
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

Sau header: Kết luận · Neo và môi trường · Bảng finding (ID `F906-NN`, mức P0–P3, tệp:dòng, bằng chứng, hướng sửa
BẰNG LỜI) · Bảng N1–N3 · Cổng · Các hướng săn. `approve` chỉ khi không còn P0/P1/P2/P3 mở trong phạm vi bản vá; thứ
không đo được ghi `KHÔNG ĐO ĐƯỢC`. Không viết patch sản phẩm.
