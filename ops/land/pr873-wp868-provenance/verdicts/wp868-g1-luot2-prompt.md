# Cross-review Codex — packet #868 (`wp868`, CAI-TACH-KENH-KET-QUA), lượt 2/5

Bạn là REVIEWER độc lập, họ model `openai`, cho một executor họ `claude`. Lớp review **sensitive**, assurance mục tiêu
`cross_approved`. Bạn KHÔNG có quyền merge/land/deploy, KHÔNG gọi mạng/GitHub, KHÔNG sửa cây `cay-kho/` hay `nen/`
(chỉ đọc; mọi bản sao, đột biến, fixture đặt dưới `out/`). Prompt này KHÔNG phải lease; thứ định danh tệp là BĂM.

## Neo (tự kiểm lại, đừng tin bảng này)
- Thư mục làm việc: thư mục chứa tệp prompt này (gọi là `$R`). `cay-kho/` = working clone ở **reviewed head**,
  `nen/` = clone ở **base**, cùng nguồn, `core.abbrev=7`. `kho.git` = mirror bare (đủ mọi nhánh, gồm `ops/*`).
- reviewed_head: `ac4a6cb78a136b5e7f55abfac90b75ddd3cd080d` · base (merge-base với master): `9e9a74b2a396ef458d25c51a5563efafbb45ba0c`.
- Spec: `git -C cay-kho show origin/ops/wp868-spec:ops/specs/wp868.md | sha256sum` phải bằng
  `0d950c2b98b9e024bf1cc43a77c5d3351b5f4c21e6307b2e36ba9cdeca7b3f69`. Spec là nguồn sự thật duy nhất của tiêu chí.
- Lease: `git -C cay-kho show origin/ops/wp868-r1-g1-lease:ops/leases/wp868-r1-g1-claude.yaml` (merge conditions
  M-1..M-5, write set 7 đường dẫn, trần diff 6 tệp/450 dòng thêm).
- Bối cảnh #858 (cùng mã, cùng gốc lỗi): `git -C cay-kho show origin/ops/wp858-r1-g2-lease:ops/reviews/wp858-g1-luot{4,5}-codex-verdict.md`
  — F858-03 bị mở lại bốn lần theo bốn đường; packet này đổi KIẾN TRÚC (kênh kết quả riêng) thay vì vá lọc tiếp.
- `diff.patch`, `numstat.txt` trong `$R` là diff base..head.

## ĐỐI CHIẾU LƯỢT TRƯỚC (bắt buộc, làm TRƯỚC khi săn mới)
- Verdict lượt 1 (head `1965b71`): `git -C cay-kho show origin/ops/wp868-r1-g1-lease:ops/reviews/wp868-g1-luot1-codex-verdict.md`
  (sha256 `0a2e05421e5f304331ca3eff2786bb2e4c05399d37886fd97db7ab0b4c9889b7`). Lượt 1 thoát giữa chừng (rc=1 sau 21 phút)
  nên một số cổng của nó chưa xong.
- Diff kể từ lượt 1: `diff-tu-luot1.patch` trong `$R`. Executor khai: F868-01 vá reader (`cat && printf x`, đọc hỏng ⇒
  exit 7) kèm ca `r868_doc_kenh_hong_thi_dung` (đỏ trên `1965b71`); F868-02 ca `r868_don_kenh_khi_loi`; F868-03 biến
  thể CRLF trong `r868_khong_bo_chon_doc_dong_cuoi`; ba đột biến `wp868_sh_doc_kenh_nuot_loi` · `bo_trap_exit` ·
  `duong_lui_bo_cat_cr`. ĐỪNG tin lời khai: với mỗi F868-0x, chạy lại witness/mutant của chính bạn ở lượt 1 trên head mới,
  ghi ĐÓNG/CHƯA ĐÓNG kèm lệnh + output. Giữ nguyên ID và slug lớp; lớp mới mới được ID mới (F868-04…).
- Executor đo được (Q9, packet khác): sau khi một lượt Codex KẾT THÚC, `/tmp/.git` RỖNG còn sót (không còn mount) vẫn làm
  11 ca `r484_*` đỏ ("Codex home is inside a repository"); xoá thư mục rỗng ấy thì xanh. Đo trong sandbox của bạn và ghi,
  đừng tính là hồi quy nếu nền đỏ y hệt.
- Lượt 1 ghi selftest 1730/1731 do driver ép `core.abbrev` qua môi trường; executor đo 1731/1731 khi `core.abbrev` đặt bằng
  `git config` cục bộ. Kiểm lại theo cách của bạn.

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
`execution_surface: codex_cli`, `transport: machine`, `review_round: 2/5`. Rồi: Kết luận · Neo và môi trường · bảng
finding (ID `F868-NN`, mức P0–P3, slug lớp ổn định, vị trí, bằng chứng, hướng xử lý bằng lời) · bảng hướng săn · bảng
lệnh → kết quả thật · Không đo được. `approve` chỉ khi không còn P0/P1/P2 mở. Không viết patch sản phẩm.
