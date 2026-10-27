# Cross-review Codex — packet #886 (wp886, PYTHON-PROBE-THEO-PATH), lượt 1/5

Bạn là REVIEWER (họ OpenAI) cho một bản vá do executor họ Claude viết. Lớp review: **sensitive**.
Kho: github.com/ducthangho/tra-luat. Bạn KHÔNG có mạng/GitHub; mọi thứ cần đo đã nằm trong thư mục này.

## Bố trí (thư mục làm việc hiện tại = gốc sandbox)
- `cay-kho/` — clone ở **head ứng viên** `a9be5828fb7b937ec8c9f7f1dc6b5a48babbafa5` (nhánh `agent/wp886-g1-claude`).
- `nen/` — clone ở **base** `1ccc31498b7d37c12305e8f1b5bf2d1fc217b92e` (`origin/master` đã merge vào head; diff base..head = đúng 5 tệp của PR).
- `kho.git/` — mirror bare (nguồn là clone NÔNG nên có cảnh báo "shallow roots"; head/base đủ để đo).
- `evidence/spec.md` — đặc tả ĐÓNG BĂNG, sha256 phải là `28d1bb708621c6d410aa2f22ba11f295a5a9407d74d7aa736ddd30421e4f96a6` (tự đo lại).
- `evidence/lease.yaml` — lease `wp886-r1-g1-claude` (bản sao offline; đừng suy authority live từ nó).
- `evidence/diff.patch`, `evidence/numstat.txt` — diff base..head (5 tệp).
- `evidence/EXECUTOR_GATES.md` — kết quả cổng executor tự chạy (LỜI KHAI, không phải bằng chứng — đo lại cái nào cần).
- `out/` — nơi DUY NHẤT bạn được ghi. KHÔNG sửa `cay-kho/`, `nen/`, `kho.git/`.

Đọc trước: `evidence/spec.md` (nguồn sự thật, nhất là N1–N7, Q1–Q9, mục "Cổng"), `cay-kho/CLAUDE.md`
(các mục "Bài học đắt giá" về đột biến/tín dụng giả, hai vế A/B, `/tmp/.git`), và diff.

## Bối cảnh lỗi (từ #858)
`ops/cong_cu.py` `_chay` từng thay `python` bằng `sys.executable` (commit `e062b8e`), nên probe `python`,
PyYAML, jsonschema đo trình đang chạy checker, không đo bản shell gọi; `python` hỏng đầu PATH vẫn `DAT`.
Bản vá giải `python` theo PATH đúng thứ tự dòng chọn `PY` của `ops/cai_cong_cu.sh` (`python` → `python3` → `py -3`),
luật native như `_ten_tran_giai_ra` của `.claude/dev/launcher.py` (Windows chỉ nhận đuôi PATHEXT).

## PHẠM VI LƯỢT NÀY (bắt buộc đọc)
Lượt 1/5, gọi SỚM theo chỉ thị điều phối: chỉ review phần **N1–N5 không phụ thuộc fixture** của `ops/cong_cu_test.py`.
Lỗi đã biết, KHÔNG báo lại thành finding mới: tiền kiểm `python_alias_behavior_test` (`ops/cong_cu_test.py`) đỏ trên
Windows vì fixture `python3` không đuôi bị luật native PATHEXT (N6) bỏ qua. Lỗi ấy đã có P1 của connector, và sẽ được
sửa ở revision r2 (fixture `python3.cmd` trên Windows) vì tệp ấy nằm NGOÀI write set r1. Chỉ báo nếu bạn thấy bản vá
`ops/cong_cu.py` SAI theo cách khác (ví dụ N6 cài đặt lệch luật native), không phải chính xung đột fixture ấy.
Ưu tiên tìm P1/P2/P3 trong 5 tệp của diff: ops/cong_cu.py, .claude/dev/launcher_test.py, scripts/tl_selftest.py,
RELEASE_MANIFEST.json, changelog.d/wp-886.md.

## Việc phải làm (theo thứ tự)
1. Neo: `git -C cay-kho rev-parse HEAD 'HEAD^{tree}'`, như vậy với `nen`; tự băm spec; hai cây sạch đầu/cuối.
2. Chạy **ca có sẵn** trên head VÀ trên base+test-head (dựng bản sao thường trong `out/`, một lệnh dựng cả hai vế):
   `PYTHONDONTWRITEBYTECODE=1 python3 -B .claude/dev/launcher_test.py --lap-ca <TEN> --lan 1` cho:
   `r886_n1_ten_tran_theo_path_moi_nen` `r886_n2_python_hong_dau_path_khong_DAT`
   `r886_n3_chi_python3_DAT_va_do_dung_interpreter` `r886_n4_khong_ten_nao_noi_ro_thieu_gi`
   `r886_n6_giai_ten_tinh_windows_va_posix` `r886_ten_python_khop_cai_cong_cu_sh`
   `r858_cai_python_khong_in_thu_muc_ban_hong` và các `r858_*`, `r802_runner_tra_lai_con_tro_nguoi_goi`.
   Phản chứng N2 phải ĐỎ trên base (bằng `TinHieuChotCa`, không phải lỗi vô can).
3. **Đột biến BẢN VÁ** trên bản sao tạm (không bao giờ trên `cay-kho/`): ngoài 8 đột biến `wp886_cc_*` có sẵn
   trong `DOT_BIEN_HOOK`, tự nghĩ thêm đột biến của `ops/cong_cu.py` mà bộ ca KHÔNG giết. Chỉ `TinHieuChotCa`
   của ĐÚNG ca đích tính là giết; mọi ngoại lệ khác là tín dụng giả.
4. `cay-kho/ops/cong_cu_test.py` phải N/N KHÔNG sửa (chạy `python3 ops/cong_cu_test.py` trong một BẢN SAO, đọc
   dòng `cong_cu_test: N/M đạt`); `python3 ops/cong_cu.py kiem-tra --json` trên máy bạn: python/PyYAML/jsonschema.
5. N7: `python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` (ok, expected==checked) và
   `python3 scripts/tl.py --selftest` (N/N) trên head.
6. **Săn ≥ 6 hướng ĐỘC LẬP**, mỗi hướng: giả thuyết · lệnh · output thật · kết luận (LỖI | KHÔNG PHẢI LỖI | KHÔNG ĐO
   ĐƯỢC). Gợi ý (không bắt buộc, không giới hạn): mục PATH rỗng/tương đối; tệp không thực thi được đứng trước;
   thư mục tên `python`; `py` không hiểu `-3`; PATHEXT rỗng/lạ; hai probe cùng công cụ đo hai interpreter khác nhau
   (T7 "cac duong goi khac ban"); thông điệp N4 với PATH có `py` nhưng không có hai tên đầu; ca `cai_cong_cu.sh
   --bat-buoc` end-to-end khi `python` đầu PATH hỏng; Windows `.cmd`/`.bat` qua `subprocess`; ảnh hưởng tới
   `kiem_tra_canary` (dùng `lenh[0]` của probe).
   Hướng nào cần dựng nội dung kiểu thoát cây thư mục/đường dẫn độc hại thì **mô tả bằng lời** cho executor viết —
   đừng tự soạn payload.
7. Kiểm diff PR ≤ 5 tệp / ≤ 450 dòng thêm (M-4), chỉ chạm write set; `ruff check --select F` delta = 0 so base.

## Bẫy đã biết
- `/tmp/.git` có thể là mount rỗng chỉ đọc khi bạn chạy dưới `codex-linux-sandbox` ⇒ một số `r484_*`/`r858_goc_tam_*`
  đỏ giả. Đặt `TMPDIR` riêng dưới `out/tmp/`, và so với base để tách lỗi môi trường.
- Đừng ghi `.pyc`: dùng `-B` và `PYTHONDONTWRITEBYTECODE=1`.
- Không gọi mạng/GitHub; không `rm -rf` ngoài `out/`.

## Đầu ra — GHI SỚM, GHI TĂNG DẦN
Tạo ngay `out/VERDICT.md` với header dưới đây (verdict tạm `pending`) và cập nhật sau MỖI bước, để lượt bị ngắt
vẫn giữ được phần đã đo:

```
verdict: approve | changes_requested | pending
reviewed_head: a9be5828fb7b937ec8c9f7f1dc6b5a48babbafa5
reviewed_sha: a9be5828fb7b937ec8c9f7f1dc6b5a48babbafa5
reviewed_tree: <tree của head>
review_class: sensitive
provider: openai_codex
model: <model header CLI công bố>
model_family: openai
reasoning_effort: <effort header CLI công bố>
execution_surface: codex_cli
transport: machine
review_round: 1/5
```

Sau header: Kết luận · Neo và môi trường · Bảng finding (ID ổn định `F886-NN`, mức P0–P3, vị trí tệp:dòng, bằng
chứng, hướng sửa BẰNG LỜI) · Bảng N1–N7 · Bảng đột biến (giết/sống/tín dụng giả) · Các hướng săn · Đánh giá câu hỏi
Windows ở trên. `approve` chỉ khi không còn P0/P1/P2/P3 mở trong phạm vi bản vá; mọi thứ không đo được ghi
`KHÔNG ĐO ĐƯỢC`, không ghi thành xanh. Không viết patch sản phẩm.
