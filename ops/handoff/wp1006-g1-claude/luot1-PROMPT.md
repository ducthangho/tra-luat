# Cross-review packet #1006 `T27-GLOB-HOA-THUONG` r1, lượt 1

Bạn là reviewer KHÁC HỌ (OpenAI Codex), executor là Claude. Bạn ĐỘC LẬP: không tin lời khai của executor,
chỉ tin phép đo của chính bạn. Bạn KHÔNG sửa kho; chỉ được ghi trong thư mục sandbox.

## Đầu vào trong sandbox (thư mục làm việc hiện tại)
- `cay-kho/` — clone thường (`.git` là THƯ MỤC, không nông) của `ducthangho/tra-luat`, detached ở head ứng viên
  `183e28f4b59467895c411db7f565dd21769ee511`. Base `79dbaf443f90daece751d9ab2537796bbd6084bf` (= origin/master lúc cấp lease) có trong object store.
- `SPEC.md` — đặc tả đóng băng (sha256 `6c21bd26b64aa5a57925875789a8d9f9f3132a00ae53416b1ac4d0ad703e3eef`).
- `DIFF.patch` — `git diff 79dbaf4..183e28f4b59467895c411db7f565dd21769ee511`.

Trước mọi phép đo trong `cay-kho/`: `git config core.abbrev 7`; nếu `git commit` cần, cô lập bằng
`GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null`.

## Lỗi gốc packet sửa
`t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc` trong `ops/lease_publish_test.py` duyệt verdict bằng
`Path.glob("*-verdict.md")`. Glob của pathlib phân biệt hoa thường theo nền (Windows không, POSIX có), nên
`ops/reviews/wp929-g1-codex-luot{1,2}-VERDICT.md` chỉ thấy trên Windows ⇒ t27 đỏ trên Windows, xanh trên Linux.

## Việc của bạn — ĐO, đừng đọc
1. Chạy `python3 ops/lease_publish_test.py --chi-ca=t27_` trên head; chạy cùng lệnh trên base để thấy base XANH
   trên Linux (tức Linux mù) và đọc thông báo.
2. Đột biến TRÊN BẢN SAO TẠM (đừng sửa `cay-kho/` tại chỗ, đừng để `.pyc` cũ: `PYTHONDONTWRITEBYTECODE=1`):
   - (a) `_liet_ke_theo_duoi` quay về `sorted(thu_muc.glob("*" + duoi))` ⇒ ca `t27_phan_chung_*` phải ĐỎ.
   - (b) như (a) và vô hiệu chốt tự kiểm bộ liệt kê trong ca phản chứng ⇒ ca phải vẫn ĐỎ ở nhánh `_kiem_muc_luc`.
   - (c) tự nghĩ thêm đột biến khác (ví dụ chỉ so `endswith` không `lower()`, bỏ `is_file()`, đổi `goc`) và báo
     cái nào SỐNG.
   Đọc TÊN CA và THÔNG BÁO của lỗi, không chỉ mã thoát: chết vì lỗi vô can là tín dụng giả.
3. Ca phản chứng có đo đúng thứ nó khai không? Có nhánh nào làm nó xanh rỗng không?
4. Hai biên nhận mới `ops/reviews/wp929-g1-codex-luot{1,2}-VERDICT.receipt.yaml`: đối chiếu TỪNG lời khai (a) với
   kho — băm/byte verdict, `reviewed_sha`, tổ tiên với merge `ab94c4f`, commit neo `8d3f655` (commit duy nhất chạm
   tệp; tổ tiên của base), cửa sổ lease, số P đếm từ tệp verdict, findings_ids. Chạy
   `python3 ops/bien_nhan_v2.py --root .` (đòi `TỔNG: ĐẠT`). Byte tệp verdict phải KHÔNG đổi so với base.
5. `ops/reviews/README.md`: hai hàng Mục lục + hai hàng cảnh báo; executor còn XOÁ một dòng trống (sau hàng
   `wp960-review-2-codex-verdict.md` cuối của bảng cảnh báo) vì nó cắt bảng, làm ba hàng `doctor-github-mcp-review-6`,
   `don-nhanh-base-review-4/5` không render thành bảng. Kiểm lời khai ấy trên base.
6. Phạm vi: diff chỉ được chạm write set
   `ops/lease_publish_test.py`, `ops/reviews/README.md`, hai biên nhận trên. Chạy `git diff --check`.
7. Nếu đủ thời gian: `python3 ops/lease_publish_test.py` toàn bộ trên head (đòi `N/N` hai số bằng nhau).
   Ca nào cần mạng/`actionlint`/`shellcheck` thì ghi BỎ QUA/KHÔNG ĐO ĐƯỢC, đừng đọc thành lỗi của packet.

Hướng thử nào cần soạn nội dung nhạy cảm (đường dẫn thoát cây thư mục, v.v.) thì MÔ TẢ BẰNG LỜI, đừng tự dựng.

## Đầu ra — ghi TĂNG DẦN vào `VERDICT.md` trong sandbox
Dòng 1: `Verdict: approve` hoặc `Verdict: request_changes`. Dòng 2: `Reviewed commit: 183e28f4b59467895c411db7f565dd21769ee511`.
Dòng 3: `Spec sha256: 6c21bd26b64aa5a57925875789a8d9f9f3132a00ae53416b1ac4d0ad703e3eef`.
Rồi: tóm tắt, bảng finding `- [P0..P3] <slug>: <vị trí> — <lệnh tái hiện> — <output> — <hướng vá>`.
Ngưỡng approve: không P0/P1/P2. Mỗi khẳng định kèm lệnh đã chạy và output; không đo được thì ghi `KHÔNG ĐO ĐƯỢC`.
Không cấp quyền merge/land.
