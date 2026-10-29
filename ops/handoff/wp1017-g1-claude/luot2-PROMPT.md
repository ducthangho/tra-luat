# Cross-review packet #1017 `BIEN-NHAN-V2-TEST-WINDOWS` r1, lượt 2 (lời gọi CUỐI theo trần lease)

Bạn là reviewer KHÁC HỌ (OpenAI Codex), executor là Claude. Bạn ĐỘC LẬP: không tin lời khai của executor, chỉ tin phép
đo của chính bạn. Bạn KHÔNG sửa kho; chỉ ghi trong thư mục sandbox.

## Đầu vào trong sandbox
- `cay-kho/` — clone thường (`.git` là THƯ MỤC, không nông), detached ở head ứng viên
  `8036ddb47a2e769703cc897798b3ba2182389c49`. Base `e9967f07b95c6458afc63dabf4a5c0494e90eca7` (lúc cấp lease); `origin/master`
  hiện là `735b181`.
- `SPEC.md` — đặc tả đóng băng (sha256 `e1e709be14e2e7c2a81de39c3acf2666c746e7146116dee669cadee4dad8ed19`).
- `DIFF.patch` — `git diff e9967f0..HEAD` (đúng một tệp `ops/bien_nhan_v2_test.py`).
- `DIFF-LUOT2.patch` — `git diff b2e2410..HEAD` (vá sau lượt 1).
- `VERDICT-LUOT1.md` — verdict lượt 1 trên `b2e2410` (request_changes, P2 `nhanh-tiem-thieu-chot-tu-kiem`).

Trước phép đo: `git config core.abbrev 7`; Python dùng `PYTHONDONTWRITEBYTECODE=1`; fixture git cô lập bằng
`GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null`. Đột biến chạy trên BẢN SAO ĐỦ CÂY (bộ test đọc
`.claude/dev/launcher.py`).

## Thay đổi từ lượt 1 (executor khai — hãy ĐO)
1. `_tiem_git`: thay `_chay_git` của module `bnv2` HIỆN HÀNH (`globals()` lúc vào), gỡ trong `finally`. Các nguồn tiêm lên mức
   module: `_nguon_lstat_tiem`, `_nguon_canh_bao_tiem`, `_c96_tiem`, `_qua_nguon_c91`.
2. Ca mới `c97_NHANH_TIEM_co_rang_tren_module_da_thay_va_tu_go`: trên bản sao VÔ HẠI (chỉ đổi một docstring) ba nhánh tiêm phải
   QUA; trên bản sao m116/m114/m125 đúng nhánh tương ứng phải ĐỎ; `Path.lstat`/`_chay_git` phải trở lại object cũ, kể cả khi
   thân `with` ném lỗi.
3. c91 `cau_hinh_canh_bao`: `core.fsyncObjectFiles` → `core.fsync=khong-co-thanh-phan-1017` (git for Windows 2.55 không cảnh báo
   khoá cũ — đo trên máy Windows của chủ kho; khoá mới cảnh báo cả hai nền), vẫn probe qua `bnv2._chay_git`, không thấy thì
   `GHI CHÚ` + nguồn tiêm.
4. c91 `run_json_ten_qua_dai`: thử hai thành phần theo thứ tự, mỗi cái lstat độc lập — tên 300 ký tự (ENAMETOOLONG POSIX) rồi
   `b*40 + "<c"` (WinError 123/EINVAL Windows); dấu stderr lấy từ chính thành phần đã dùng; tạo sẵn `ops/reviews`.

## Bằng chứng Windows (KHÔNG đo được trong sandbox — đọc như dữ liệu, không như phép đo của bạn)
CI `workflow_dispatch` windows-only run 40853717478 trên `8036ddb`, job `gate-ops (windows-latest)`: bước `bien-nhan v2
selftest` in `94/94 ca đạt · 137/137 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt`, `TỔNG: ĐẠT`. Bước sau đỏ ở `t27` của packet
#1006 (khác packet, ngoài write set). Bạn không có Windows: phần nào chỉ Windows mới đo được thì ghi `KHÔNG ĐO ĐƯỢC`.

## Việc của bạn — ĐO, đừng đọc
1. ĐỐI CHIẾU LƯỢT TRƯỚC: P2 lượt 1 đã vá thật chưa — chạy lại đúng hai đột biến lượt 1 bạn báo SỐNG (`mod = _BNV2_THAT`; bỏ
   khôi phục `Path.lstat`) trên toàn suite; đòi chúng nay CHẾT, và chết ĐÚNG chốt của c97 (đọc tên ca + thông báo).
2. Toàn suite `python3 ops/bien_nhan_v2_test.py` trên head (đòi `TỔNG: ĐẠT`, `N/N` bằng nhau); trên base để so số ca.
3. Tự nghĩ thêm đột biến cho phần MỚI (c97, `_tiem_git`, hai thành phần lstat, `core.fsync`) — ví dụ: c97 bỏ đối chứng vô hại;
   c97 so `mong_dat` sai chiều; probe `core.fsync` luôn coi là có cảnh báo; thành phần `<` dùng dấu của thành phần dài; bỏ
   `mkdir` ops/reviews. Báo cái nào SỐNG và vì sao.
4. c97 có thể chết vì lỗi RIG (không phải lỗi sản phẩm) không — tức tín dụng giả? Có rò rỉ toàn cục (module `bnv2`/`CONG`, tệp
   tạm `_TAM_DOT_BIEN`) sang ca sau không?
5. Phạm vi: diff chỉ `ops/bien_nhan_v2_test.py`; không đụng `ops/bien_nhan_v2.py`. `git diff --check`; ruff F delta 0 so base;
   `python3 .claude/dev/packet_loop.py doctrine-scan --root .`; `python3 ops/bien_nhan_v2.py --root .`.

Hướng thử nào cần soạn nội dung nhạy cảm thì MÔ TẢ BẰNG LỜI, đừng tự dựng.

## Đầu ra — ghi TĂNG DẦN vào `VERDICT.md` trong sandbox
Dòng 1: `Verdict: approve` hoặc `Verdict: request_changes`. Dòng 2: `Reviewed commit: 8036ddb47a2e769703cc897798b3ba2182389c49`.
Dòng 3: `Spec sha256: e1e709be14e2e7c2a81de39c3acf2666c746e7146116dee669cadee4dad8ed19`.
Rồi: tóm tắt, mục `ĐỐI CHIẾU LƯỢT TRƯỚC`, bảng finding `- [P0..P3] <slug>: <vị trí> — <lệnh tái hiện> — <output> — <hướng vá>`.
Ngưỡng approve: không P0/P1/P2/P3 (điều kiện merge của chủ kho tính cả P3). Mỗi khẳng định kèm lệnh và output; không đo được
thì ghi `KHÔNG ĐO ĐƯỢC`. Không tự khai bề mặt chạy của chính bạn. Không cấp quyền merge/land.
