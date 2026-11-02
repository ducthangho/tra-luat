# Cross-review lượt 2 PR ducthangho/tra-luat#896 — reviewer: codex — chấm BẢN VÁ của hai lượt trước

## Đối tượng
- `reviewed_sha`: `8d56009a09af7b3ef93801df105f9483de212cc7` (head đã merge của PR #946, merge `21fe565` trên master). Đây là trạng thái đã mang CẢ HAI bản vá dưới đây.
- PR #896 merge `27dcc3b`, head `816f43988eb3012726120ad00166a989cc2b9af6`. Lượt 1 (`verdict-cu/pr896-review-1-codex-verdict.md`) chấm `816f439` ra `changes_requested`, 1 P2: `CLAUDE.md` mô tả `t162` rộng hơn phạm vi nó đo.
- **Bản vá P2** = commit `3bc4244fe5533a71b197a0efb8f79e40175c1a3e` (chỉ sửa `CLAUDE.md`, +3/-2), vào master qua #915. Diff: `diff-3bc4244.patch`, `numstat-3bc4244.txt`.
- Lượt `pr915-review-1` (`verdict-cu/pr915-review-1-codex-verdict.md`) chấm head #915 `2789cbb6a0c7ded65fc4e448de7f24b7fe4b425f` ra `changes_requested`, 1 P1: verdict lượt 2 của #870/#889 tự khai execution surface `codex_service`, trong khi `run.json` ghi `codex_cli`, và chưa có caveat nào ghi lại.
- **Bản vá P1** = commit `a9bc9349103adfc971f4a1f7431a9655aecaaefb` (cha `cc0a3c9`): caveat `VERDICT-KHAI-SAI-EXECUTION-SURFACE` trong biên nhận + `ops/reviews/README.md`, kèm ba biên nhận mới (`pr870-review-3`, `pr889-review-3`, `pr915-review-1`) và khối `cap_nhat_20261026` ở `ops/land/pr8{70,89,96}-*-land-evidence.yaml`. Diff: `diff-a9bc934.patch`, `numstat-a9bc934.txt`.
- Lời khai của bên giao (tự kiểm, đừng tin): từ `3bc4244` tới `8d56009`, `CLAUDE.md` không đổi.

## Nhiệm vụ chính: ĐO LẠI TỪNG KHẲNG ĐỊNH tại `8d56009a09af7b3ef93801df105f9483de212cc7`
Danh sách dưới KHÔNG đủ — mỗi khẳng định bạn tìm ra mà nó bỏ sót được tính là finding.

(a) **P2 của pr896-review-1 đã đóng chưa.** Câu đã sửa trong `CLAUDE.md` (mục "(c)", đoạn "Nguồn sự thật, theo thứ tự hỏi") có khớp hành vi thật của `t162_M4_evaluator_toi_gian_chuan_bi`, `t161_M3_chot_nguon_duy_nhat_ma_tran_ci` (cả hai trong `ops/lease_publish_test.py`) và `loi_g5_workflow` (`.claude/dev/ci_dang_ky_test.py`) không. PHẢI đo bằng ĐỘT BIẾN, không chỉ đọc: chép `.github/workflows/ci.yml` (và nếu cần cả tệp test) ra thư mục tạm NGOÀI `cay-kho/`, đổi `exclude:` / `if:` / `needs:` mức job, đổi output `os` của `chuan-bi`, rồi chạy t162/t161/`loi_g5_workflow` trên bản sao; ghi ca nào ĐỎ, ca nào vẫn XANH. Kiểm riêng: câu có khai rộng hơn phép đo không (vd "phần mảnh/gom của `gate-cong-cu*`" có đúng phủ MỌI job tiền tố ấy tại SHA này không); câu có còn sót vế nào của bản trước (vd "đọc ca ấy là đọc ma trận HIỆN HÀNH") không; `CLAUDE.md` tại `8d56009` có đúng bằng tại `3bc4244` không (`git diff`).

(b) **P1 của pr915-review-1 đã đóng chưa.** Caveat `VERDICT-KHAI-SAI-EXECUTION-SURFACE` có mặt ĐỦ ở mọi biên nhận cần nó và có hàng tương ứng trong `ops/reviews/README.md` không (biên nhận nào của #870/#889 mang verdict tự khai `codex_service`? đếm bằng `grep` trên các `*-verdict.md`, đừng chỉ tin danh sách trên). Dòng verdict được trích (số dòng, nguyên văn) có đúng không; `run.json` được trích có thật ghi `execution_surface: codex_cli` không. Chạy riêng từng ca:
`python3 ops/lease_publish_test.py --chi-ca=t26_`, `--chi-ca=t27_`, `--chi-ca=t138_` — ghi rc + dòng tổng kết (đòi `N/N` hai số BẰNG NHAU, đừng tin rc). Rồi đột biến trên BẢN SAO của kho (ví dụ `git worktree add` hoặc `git clone` từ `mirror.git` vào thư mục tạm ngoài `cay-kho/`, checkout `8d56009`): xoá MỘT hàng caveat của README ⇒ ca nào ĐỎ? xoá caveat khỏi biên nhận ⇒ ca nào ĐỎ? Ca nào không đỏ thì ghi rõ chốt ấy không có răng.

(c) **Lời khai trong ba biên nhận mới và khối `cap_nhat_20261026`** có khớp hiện vật không: số sự kiện `model_phuc_vu` và số `response_id` khác nhau trong từng `run.json`, model đọc được, `verdict_sha256`/`verdict_bytes`, `reviewed_sha`/`reviewed_tree`/`base_sha`, `thoi_luong_giay`, `prompt_sha256` = sha256 PROMPT.md, `so_p*` với dòng `Kết quả`, `evidence_url` trỏ commit nào và commit đó có đúng CHỈ mang hiện vật không, mức đảm bảo (`cross_approved` chỉ hợp lệ khi `approve` + model đo được ở họ khác executor), và các mốc §10.2.2 (Run/Checkout/Workflow definition/Gate output) trong ba hồ sơ land có nhãn `measured` mà tệp nguồn được trỏ tới thật sự có trong kho và chứa dữ liệu đó không. `sha256sum -c SHA256SUMS` trong từng thư mục hiện vật có sạch không.

(d) Chạy và ghi rc + dòng kết luận: `python3 ops/bien_nhan_v2.py --root .` và `python3 ops/land_evidence_nguon.py --root .` tại `cay-kho/`. Thêm hai cổng: `python3 .claude/dev/packet_loop.py doctrine-scan --root .` và `python3 scripts/tl.py doc-claims-check --json` (đòi `"ok": true`).

## Ghi VERDICT.md TĂNG DẦN
Tạo `VERDICT.md` ở thư mục này (thư mục chứa PROMPT.md, KHÔNG phải trong `cay-kho/`) NGAY khi bắt đầu (dòng đầu `verdict: dang_lam`), nối thêm sau MỖI hướng thử. Cuối cùng sửa dòng đầu thành `verdict: approve` hoặc `verdict: changes_requested`, dòng 2 `reviewed_sha: 8d56009a09af7b3ef93801df105f9483de212cc7`, dòng 3 `Kết quả: <n> P0, <n> P1, <n> P2, <n> P3.`

Cấu trúc:
```
verdict: ...
reviewed_sha: ...
Kết quả: ...

## KẾT LUẬN VỀ HAI FINDING CŨ
- P2 pr896-review-1 (t162): ĐÃ ĐÓNG | CHƯA ĐÓNG | ĐÓNG MỘT PHẦN — bằng chứng
- P1 pr915-review-1 (surface): ĐÃ ĐÓNG | CHƯA ĐÓNG | ĐÓNG MỘT PHẦN — bằng chứng

## BẢNG ĐO
| khẳng định | bên giao khai | đo được (lệnh) | khớp? |

## BẢNG SĂN   (>= 6 hướng ĐỘC LẬP, mỗi hướng có LỆNH + OUTPUT THẬT)
HƯỚNG n: <tên>
  giả thuyết : ...
  lệnh       : ...
  output     : ...
  kết luận   : LỖI | KHÔNG PHẢI LỖI | KHÔNG ĐO ĐƯỢC

### <slug-kebab>  [P0|P1|P2|P3]  <tiêu đề>
TỆP/DÒNG:
VẤN ĐỀ:
ĐÃ THỬ NGHIỆM: <lệnh + kết quả, hoặc KHÔNG ĐO ĐƯỢC + lý do>
ĐỘ TIN: cao/vừa/thấp
```
P1 = khẳng định sai về sự thật đo được TẠI `8d56009a09af7b3ef93801df105f9483de212cc7`. P2 = khai rộng hơn phép đo / thiếu điều kiện. P3 = diễn đạt.
Không có finding thì vẫn phải có BẢNG ĐO đủ và BẢNG SĂN >= 6 hướng có output thật; "approve" không có output là không hợp lệ.
Trong VERDICT.md, nếu tự khai môi trường chạy của mình thì chỉ ghi điều bạn ĐO được; đừng tự đặt tên execution surface (đó chính là lỗi P1 của lượt trước).
Gợi ý vá (nếu có) ghi vào `HINT.patch` ở thư mục này, định dạng `patch -p0` từ gốc `cay-kho/`.

## Ràng buộc
Bạn là reviewer CHỈ ĐỌC + ĐO, độc lập với executor (Claude). KHÔNG sửa `cay-kho/` (mọi đột biến làm trên BẢN SAO ở thư mục tạm), KHÔNG push, KHÔNG gọi mạng (sandbox không có mạng). Bạn chỉ CHẠY các ca test có sẵn và ĐỘT BIẾN tệp cấu hình/tài liệu/biên nhận trên bản sao; không cần tự soạn mã khai thác nào.
Mọi khẳng định phải đo TẠI `8d56009a09af7b3ef93801df105f9483de212cc7` — master hiện tại có thể khác, đừng lấy nó làm chuẩn. Thứ định danh tệp là SHA, không phải tên nhánh.
Cây đầy đủ, KHÔNG shallow, tại `cay-kho/` (HEAD detached đúng `8d56009a09af7b3ef93801df105f9483de212cc7`; mọi nhánh ở `refs/remotes/origin/*`; `core.abbrev=7`). Mirror trần: `mirror.git`. Hai verdict cũ: `verdict-cu/`.
Lưu ý môi trường: nếu `launcher_test` hay ca nào báo `Codex home is inside a repository` thì đó là tạo tác của sandbox (`/tmp/.git`), ghi là KHÔNG ĐO ĐƯỢC chứ đừng ghi thành finding.
