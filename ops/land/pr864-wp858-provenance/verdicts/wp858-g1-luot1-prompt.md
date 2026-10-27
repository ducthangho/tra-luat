# Cross-review lượt 1 — packet #858 (wp858), lớp `sensitive`

Bạn là REVIEWER độc lập (họ openai) cho một packet do Claude thi công. Bạn KHÔNG sửa mã sản phẩm trong cây được giao,
KHÔNG push, KHÔNG gọi GitHub. Mọi đột biến chạy trên BẢN SAO TẠM dưới `out/`, không ghi đè tệp trong `kho/`.

## Định danh — tự kiểm, đừng tin câu chữ này
- Cây review: `kho/` (cùng thư mục với tệp này), HEAD phải là `bfbd2732a0e5359cbeb2a4d5336fc3dc7d2a7121`.
- Nền so sánh: `git merge-base HEAD origin/master` (master đã được merge vào nhánh theo Q7 của spec). Nền lúc cấp
  lease là `3a3a3caca5de4934ff53851feb6994c2c7b84ad5`.
- Spec: `git show origin/ops/wp858-spec:ops/specs/wp858.md`, sha256 phải là
  `5a61e959281f852592b2a5420b4618718d2364db8fa6320934d2651bbb7d4c54`. Spec là nguồn sự thật.
- Lease: `git show origin/ops/wp858-r1-g1-lease:ops/leases/wp858-r1-g1-claude.yaml` (write set 7 đường dẫn).
- Phụ lục có thẩm quyền của chủ kho cho riêng `python` (comment #858 6312034981, ghi lại nguyên văn ý ở đây vì bạn
  không có mạng): chọn phương án (a) — `python.cai.*` vẫn gọi hàm chọn chung; ca `r858_*` cho python CHỈ khẳng định
  (1) không bao giờ in thư mục của bản hỏng, (2) rc 0 khi tên trần đã DAT. KHÔNG đòi "probe thấy python của thư mục
  ứng viên" vì `ops/cong_cu.py::_chay` thay `python` bằng `sys.executable`. Không sửa `ops/cong_cu.py`. Đây là nợ có
  tên `python-probe-khong-theo-PATH`, không phải đã đóng.

## Thay đổi (đọc `git diff $(git merge-base HEAD origin/master) HEAD`)
- `ops/cai_cong_cu.sh`: hàm `chon_thu_muc_chay_duoc [--win] <ten> <ung vien>...`.
- `ops/cong_cu.yaml`: 12 công thức `git`/`python`/`shellcheck`/`bash` gọi hàm ấy; `rg` giữ bộ chọn riêng (Q1).
- `.claude/dev/launcher_test.py`: ca `r858_*`, 9 đột biến `wp858_*` trong `DOT_BIEN_HOOK`, runner đột biến nhận
  thêm đích `cai_sh` và `selftest`.
- `scripts/tl_selftest.py`: L3 (thư mục tạm riêng cho edit-skill) + ratchet gói 189 → 190.
- `changelog.d/wp-858.md`, `RELEASE_MANIFEST.json`.

## Lời khai của executor — mỗi câu là một GIẢ THUYẾT để bạn bác
1. N1–N3: với git/shellcheck/bash × linux/macos/windows, bản hỏng đầu PATH ⇒ DAT và thư mục chọn là bản tốt;
   không ứng viên nào DAT ⇒ công thức thoát ≠ 0. Ca: `r858_cai_{linux,macos,windows}_chon_ban_chay_duoc`.
2. N4: phản chứng Codex #831 lượt 4 (`rg` hỏng cùng thư mục với `bash`, `--bat-buoc`) đỏ trên nền, xanh trên head.
   Ca: `r858_bat_buoc_bash_khong_dua_rg_hong_len_dau`. Cơ chế: tên trần đã DAT thì hàm KHÔNG in thư mục nào.
3. N6: `r858_selftest_editskill_thu_muc_rieng` + selftest không đổi số ca (1731/1731 trên head).
4. Sàn đột biến Windows (≥70% đo được mỗi nền; master đo 197/281): mọi đột biến wp858 có thêm ca thuần Python
   (`r858_hinh_dang_cong_thuc_cai` hoặc ca N6) nên đo được trên Windows.
5. L2 (`t86` đỏ khi hai suite song song): executor KHÔNG tái hiện được (15 lượt suite song song, có/không
   `CODEX_AUTH_JSON` giả, đều xanh) nên KHÔNG vá. Khai là chưa đo được gốc.
6. `--dot-bien` toàn bảng trước bản vá cuối: 285/286, đột biến sống `wp858_sh_khong_ung_vien_van_rc0` đã được giết
   bằng phép eval trực tiếp trong chiều âm (commit `b0de05a`). Chưa chạy lại toàn bảng sau đó.

## Việc của bạn (ưu tiên theo thứ tự)
1. Chạy các ca có sẵn: `PYTHONDONTWRITEBYTECODE=1 python .claude/dev/launcher_test.py --lap-ca <ten> --lan 1` cho
   từng ca `r858_*`, cùng các ca `r831_*` và `r802_cai_rg_windows_chon_ban_chay_duoc`, `r802_bang_cai_rg_khop_cong_cu_yaml`.
2. Đo lời khai 2 trên NỀN: dựng bản sao tạm của `kho/`, khôi phục `ops/cong_cu.yaml` + `ops/cai_cong_cu.sh` của nền,
   giữ `launcher_test.py` của head, chạy ca N4 — phải ĐỎ với `rg: DO`.
3. ĐỘT BIẾN BẢN VÁ trên bản sao tạm: gỡ từng chốt của hàm (kiểm tên trần, kiểm `-f/-x`, chọn bằng checker,
   `return 1`, ghi `$GITHUB_PATH`, `cygpath -u/-w`) và từng ứng viên Q2 trong YAML; báo chốt nào gỡ ra mà KHÔNG ca
   nào đỏ (đột biến sống) — đó là finding. Chỉ `TinHieuChotCa` của ca đích mới tính là giết.
4. Chạy `python .claude/dev/launcher_test.py --dot-bien` một lần trên head; báo số `DOT BIEN: x/y`.
5. Soi các đường mà executor có thể chưa nghĩ tới: công thức Windows có glob `Python3*` (khoảng trắng? không khớp?),
   `set -euo pipefail` trong `$(eval ...)`, hàm được `source` trong vòng `--bat-buoc`, khoảng trắng trong đường dẫn
   ứng viên, `ProgramFiles` vắng, `cygpath` vắng trên Windows. Hướng nào cần soạn nội dung nhạy cảm (đường dẫn thoát
   cây, v.v.) thì MÔ TẢ BẰNG LỜI trong verdict, đừng tự soạn.
6. Lời khai 5: nếu bạn dựng được phép tái hiện `t86` thì ghi lệnh + kết quả; không thì ghi "không tái hiện".

## Đầu ra — BẮT BUỘC
Ghi `out/VERDICT.md` với:
- dòng đầu `verdict: approve` hoặc `verdict: changes_requested`;
- `reviewed_head: bfbd2732a0e5359cbeb2a4d5336fc3dc7d2a7121`;
- bảng finding: id, mức P0–P3, tệp:dòng, phép đo tái hiện (lệnh → kết quả thật), đề xuất vá;
- bảng "lệnh → kết quả thật" cho mọi phép bạn chạy (kể cả xanh);
- mục "không đo được" liệt kê thứ bạn không kiểm được và vì sao.
Không tính một lời khai là đúng nếu bạn chưa chạy phép đo cho nó.
