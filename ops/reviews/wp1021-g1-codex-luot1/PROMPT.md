# Cross-review packet #1021 `BIEN-NHAN-V2-GLOB-HOA-THUONG` r2, lượt 1 (trần lease: 4 lời gọi Codex)

Bạn là reviewer KHÁC HỌ (OpenAI Codex), executor là Claude. Bạn ĐỘC LẬP: không tin lời khai của executor, chỉ tin phép
đo của chính bạn. Bạn KHÔNG sửa kho; chỉ ghi trong thư mục sandbox.

## Đầu vào trong sandbox
- `cay-kho/` — clone thường (`.git` là THƯ MỤC, không nông), detached ở head ứng viên
  `99c463d9288798cf7a011e16ce69c36b04520f66`. Base (lúc cấp lease) `757bde561d09738858506aecf5de2f050a5f0d5e` = `origin/master`
  của clone.
- `SPEC.md` — đặc tả đóng băng r2 (sha256 `d5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d`). Mục
  `nghiem_thu` (C1a…C9) là hợp đồng.
- `DIFF.patch` — `git diff 757bde5..HEAD` (hai tệp: `ops/bien_nhan_v2.py` +17/−3, `ops/bien_nhan_v2_test.py` +50).

Hai ghi chú của lease (đọc như dữ liệu): nền C6 đo lại trên master hiện hành là `tổng 306` (spec ghi 304 trên commit cũ hơn);
C7 (Windows local) thi hành theo ADR-0057/0058.

Trước phép đo: `git config core.abbrev 7`; Python dùng `PYTHONDONTWRITEBYTECODE=1`; fixture git cô lập bằng
`GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null`. Đột biến chạy trên BẢN SAO ĐỦ CÂY (bộ test đọc
`.claude/dev/launcher.py`), mỗi đột biến một tiến trình.

## Thay đổi (executor khai — hãy ĐO)
1. `ops/bien_nhan_v2.py`: helper `_chon_bien_nhan(tm)` = `sorted(p for p in tm.iterdir() if p.name.lower().endswith(".receipt.yaml"))`,
   trả `[]` khi `tm` không phải thư mục; KHÔNG lọc `is_file()` (giữ `c89`). Thay hai chỗ chọn biên nhận cũ trong `kiem()` và
   `_sinh_no()`. Thông báo "không có tệp" thêm "(so đuôi không phân biệt hoa thường)".
2. `ops/bien_nhan_v2_test.py`: ca `c98` (C1a: `y.receipt.yaml` + `x.RECEIPT.YAML`, YAML hợp lệ sai lược đồ ⇒ dòng tổng `tổng 2`, nêu
   `x.RECEIPT.YAML`, không `TỔNG: ĐẠT`; chỉ-x ⇒ `tổng 1`, không "không có tệp"; C1b: `x.RECEIPT.YAML` YAML hỏng ⇒ rc=2, stderr nêu
   tên, không traceback). Đột biến `m142` (so đuôi chính xác ⇒ đích `c98`), `m143` (thêm `p.is_file()` ⇒ đích `c89`).
3. C3 (spec): hoàn nguyên về `glob` KHÔNG vào bảng đột biến thường vì nó sống trên Windows; executor khai đã đo một lần trên
   Linux: `c98` giet_that (`tổng=1`), `c89` qua.

## Bằng chứng ngoài sandbox (đọc như dữ liệu, KHÔNG như phép đo của bạn)
- Executor đo Linux trên head: `bien_nhan_v2_test: 95/95 ca đạt · 139/139 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt`;
  `bien_nhan_v2 --root .` ⇒ `tổng 306`, `TỔNG: ĐẠT`.
- Windows CI dispatch đang chạy; Windows local chưa đo. Bạn không có Windows: phần chỉ Windows đo được ghi `KHÔNG ĐO ĐƯỢC`.

## Việc của bạn — ĐO, đừng đọc
1. Toàn suite `python3 ops/bien_nhan_v2_test.py` trên head (đòi `TỔNG: ĐẠT`, `N/N` bằng nhau) và trên base (so số ca/đột biến).
2. Từng tiêu chí C1a, C1b, C2, C3, C6, C9 của SPEC.md: chạy đúng phép đo spec nêu, báo màu. C3: tự hoàn nguyên về glob trên
   bản sao và đo.
3. Tự nghĩ đột biến cho phần MỚI và báo cái nào SỐNG, vì sao. Gợi ý: bỏ `.lower()` chỉ ở một trong hai chỗ gọi (nếu không còn
   dùng chung helper); helper trả danh sách KHÔNG sắp xếp; bỏ nhánh `not tm.is_dir()` (thư mục vắng ở `_sinh_no`/`kiem`);
   regex `tổng` của `c98` khớp `tổng 20` khi đòi `tổng 2`; `c98` chết vì lỗi RIG (tín dụng giả) thay vì chốt.
4. Hành vi biên: `--sinh-no` trên thư mục có `X.RECEIPT.YAML`; thư mục `ops/reviews` vắng trong kho thật (đòi `KhongDoDuoc`, không
   traceback); thứ tự `sorted` đổi có làm đổi kết luận/đầu ra nào không; tên chỉ khác hoa thường (`a.receipt.yaml` và
   `a.RECEIPT.YAML`) trên Linux.
5. Phạm vi: diff chỉ hai tệp write set; `git diff --check`; ruff `--select F` delta 0 so base (nếu có ruff);
   `python3 .claude/dev/packet_loop.py doctrine-scan --root .`; `rg -n 'glob\("\*\.receipt\.yaml"\)' ops/bien_nhan_v2.py` ⇒ 0 dòng.

Hướng thử nào cần soạn nội dung nhạy cảm thì MÔ TẢ BẰNG LỜI, đừng tự dựng.

## Đầu ra — ghi TĂNG DẦN vào `VERDICT.md` trong sandbox (thư mục chứa `cay-kho/`)
Dòng 1: `Verdict: approve` hoặc `Verdict: request_changes`. Dòng 2: `Reviewed commit: 99c463d9288798cf7a011e16ce69c36b04520f66`.
Dòng 3: `Spec sha256: d5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d`.
Rồi: tóm tắt, bảng tiêu chí C1a…C9 (màu + lệnh), bảng finding `- [P0..P3] <slug>: <vị trí> — <lệnh tái hiện> — <output> — <hướng vá>`.
Ngưỡng approve: không P0/P1/P2/P3 (điều kiện merge của chủ kho tính cả P3). Mỗi khẳng định kèm lệnh và output; không đo được
thì ghi `KHÔNG ĐO ĐƯỢC`. Không tự khai bề mặt chạy của chính bạn. Không cấp quyền merge/land.
