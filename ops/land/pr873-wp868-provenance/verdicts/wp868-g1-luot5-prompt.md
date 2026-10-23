# Cross-review Codex — packet #868 (`wp868`, CAI-TACH-KENH-KET-QUA), lượt 5/5

Bạn là REVIEWER độc lập, họ model `openai`, cho một executor họ `claude`. Lớp review **sensitive**, assurance mục tiêu
`cross_approved`. Bạn KHÔNG có quyền merge/land/deploy, KHÔNG gọi mạng/GitHub, KHÔNG sửa cây `cay-kho/` hay `nen/`
(chỉ đọc; mọi bản sao, đột biến, fixture đặt dưới `out/`). Prompt này KHÔNG phải lease; thứ định danh tệp là BĂM.

## Neo (tự kiểm lại, đừng tin bảng này)
- Thư mục làm việc: thư mục chứa tệp prompt này (gọi là `$R`). `cay-kho/` = working clone ở **reviewed head**,
  `nen/` = clone ở **base**, cùng nguồn, `core.abbrev=7`. `kho.git` = mirror bare (đủ mọi nhánh, gồm `ops/*`).
- reviewed_head: `f07f88c75cabbef691c86ac8746317a6c0705162` · base (merge-base với master): `9e9a74b2a396ef458d25c51a5563efafbb45ba0c`.
- Spec: `git -C cay-kho show origin/ops/wp868-spec:ops/specs/wp868.md | sha256sum` phải bằng
  `0d950c2b98b9e024bf1cc43a77c5d3351b5f4c21e6307b2e36ba9cdeca7b3f69`. Spec là nguồn sự thật duy nhất của tiêu chí.
- Lease: `git -C cay-kho show origin/ops/wp868-r1-g1-lease:ops/leases/wp868-r1-g1-claude.yaml` (merge conditions
  M-1..M-5, write set 7 đường dẫn, trần diff 6 tệp/450 dòng thêm).
- Bối cảnh #858 (cùng mã, cùng gốc lỗi): `git -C cay-kho show origin/ops/wp858-r1-g2-lease:ops/reviews/wp858-g1-luot{4,5}-codex-verdict.md`
  — F858-03 bị mở lại bốn lần theo bốn đường; packet này đổi KIẾN TRÚC (kênh kết quả riêng) thay vì vá lọc tiếp.
- `diff.patch`, `numstat.txt` trong `$R` là diff base..head.

## ĐỐI CHIẾU LƯỢT TRƯỚC (bắt buộc, làm TRƯỚC khi săn mới) — ĐÂY LÀ LỜI GỌI CUỐI 5/5
- Verdict lượt 4 (head `0bfc73d`): `git -C cay-kho show origin/ops/wp868-r1-g1-lease:ops/reviews/wp868-g1-luot4-codex-verdict.md`
  (sha256 `bf0dd45fa0d29e8d9a63c9897914113c5481070c97488a61201db13d2712d5d5`); lượt 1–3 cùng thư mục. Lượt 4 đóng F868-06,
  MỞ LẠI F868-02 (cleanup trên hai đường `exit 7` của reader sau khi công thức cài THÀNH CÔNG).
- Diff kể từ lượt 4: `diff-tu-luot4.patch` — CHỈ `.claude/dev/launcher_test.py`. Executor khai: `r868_doc_kenh_hong_thi_dung`
  dùng TMPDIR sân riêng, cat giả ghi lại đường dẫn kênh (chứng minh kênh có thật), hai biến thể đọc-lỗi/payload-rác đòi không
  còn `cai_cong_cu.*`; hình dạng đòi trap EXIT là DUY NHẤT; đột biến `wp868_sh_go_trap_sau_eval`. Chạy lại mutant
  `clear-exit-trap-after-recipe` CỦA BẠN trên head mới; ghi ĐÓNG/CHƯA ĐÓNG kèm lệnh + output. Giữ ID/slug.
- Executor tự liệt kê mọi đường thoát SAU khi tạo thư mục kênh: installer lỗi (ca cũ), đọc lỗi exit 7, payload rác exit 7
  (ca này), thành công (rm tường minh + trap), batch (rm tường minh mỗi lượt). Nếu bạn thấy đường thứ sáu, đo nó.
- Executor đo: launcher_test 250/250 (`/tmp/.git` vắng); `--dot-bien` 310/310; diff 6 tệp/421 dòng thêm. Connector Codex
  GitHub review `0bfc73d` (trước bản vá này): không finding.
- Không còn lời gọi nào sau lượt này. Head sạch (không P0/P1/P2/P3 mở) ⇒ `approve`.

## Việc phải làm
1. **Từng tiêu chí N1–N7 của spec**: chạy phản chứng có sẵn (`r868_*`, `r858_*`, `r831_*`, `r802_*` trong
   `.claude/dev/launcher_test.py`, dùng `--lap-ca TEN --lan N`) trên head VÀ trên nền (chép `launcher_test.py` của head vào
   một bản sao của `nen/` dưới `out/`). Spec đòi (a)(b) của N1 ĐỎ trên nền — kiểm. Ghi lệnh + output thật.
2. **Đột biến BẢN VÁ** (trên bản sao dưới `out/`, KHÔNG trên `cay-kho/`): ngoài bảng `DOT_BIEN_HOOK` có sẵn (`--dot-bien`),
   tự nghĩ các đột biến KHÔNG tương đương vào `ops/cai_cong_cu.sh`/`ops/cong_cu.yaml` mà bộ ca hiện có KHÔNG giết. Chỉ
   `TinHieuChotCa` tính là giết; đột biến chết vì lỗi vô can là tín dụng giả.
3. **Săn ≥ 6 hướng ĐỘC LẬP**, mỗi hướng có LỆNH + OUTPUT THẬT, mẫu:
   ```
   HƯỚNG <n>: <tên>
     giả thuyết : <nếu ... thì ... sai>
     lệnh       : <lệnh đã chạy>
     output     : <output thật, cắt gọn>
     kết luận   : LỖI | KHÔNG PHẢI LỖI | KHÔNG ĐO ĐƯỢC
   ```
   Gợi ý vùng (không phải trần): kênh có thật sự riêng không (biến export? dưới `bash -a` / `SHELLOPTS=allexport`?);
   `--bat-buoc` (các lượt `source` dùng chung shell: trap EXIT ghi đè nhau, thư mục tạm có bị rò/xoá nhầm, kênh của lượt
   trước có lọt sang lượt sau không); ngữ nghĩa errexit của `( set +e; eval )` so với `$( )` cũ — mã thoát công thức hỏng
   có còn ≠ 0 ở mọi đường; công thức không gọi bộ chọn (N3: pip, `cai_actionlint.sh`) — chạy `ops/cong_cu_test.py` N/N;
   writer muộn giữ stdout (N2) và giữ STDERR; CRLF/Windows Git Bash (`mktemp -d`, `cygpath`) — phần nào chỉ mô phỏng
   được thì ghi KHÔNG ĐO ĐƯỢC; hồi quy N4 của #858 (`bash` không đưa `rg` hỏng lên đầu PATH); `rg.cai.windows` mới bỏ
   kiểm `rg.exe` và đổi điều kiện ghi `$GITHUB_PATH`; các đột biến cũ bị đổi neo/bỏ (Q4) — có mất chốt nào không.
   Hướng nào cần soạn nội dung dạng tấn công đường dẫn/thoát thư mục thì MÔ TẢ BẰNG LỜI, đừng tự dựng.
4. **Cổng**: `launcher_test.py` nền/head (có và không `CODEX_AUTH_JSON` giả), `--dot-bien`, `PYTHONDONTWRITEBYTECODE=1`,
   hai vế dựng trong MỘT lệnh; `ops/cong_cu_test.py`; `bash -n`; `ruff check --select F` delta; `tl.py --selftest`;
   `tl.py release-verify RELEASE_MANIFEST.json --strict --json` (`ok=true`, expected==checked);
   `packet_loop.py doctrine-scan --root .`; `tl.py doc-claims-check --strict`. Lưu ý: khi một sandbox Codex đang chạy,
   `/tmp/.git` chỉ đọc có thể làm `t86`/`r484_*` đỏ giả — đo và ghi, đừng tính là hồi quy nếu đỏ cả nền.
5. Diff: đúng 6 tệp, ≤ 450 dòng thêm, đúng write set (không có `ops/handoff/*`).

## Verdict
Ghi `$R/VERDICT.md` NGAY từ đầu (header + "đang chạy"), cập nhật sau mỗi hướng — lượt bị cắt vẫn giữ được phần đã đo.
Header (YAML-ish, từng dòng `khoá: giá trị`): `verdict` (approve | changes_requested), `reviewed_head`, `reviewed_sha`,
`reviewed_tree`, `review_class: sensitive`, `provider: openai_codex`, `model`, `model_family: openai`, `reasoning_effort`,
`execution_surface: codex_cli`, `transport: machine`, `review_round: 5/5`. Rồi: Kết luận · Neo và môi trường · bảng
finding (ID `F868-NN`, mức P0–P3, slug lớp ổn định, vị trí, bằng chứng, hướng xử lý bằng lời) · bảng hướng săn · bảng
lệnh → kết quả thật · Không đo được. `approve` chỉ khi không còn P0/P1/P2 mở. Không viết patch sản phẩm.
