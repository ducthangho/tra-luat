# VERDICT — human_audited, packet #675 CAI-CONG-CU-SIGPIPE r2 g2 (PR #681)

**BẢN CHIẾU. Nguồn có thẩm quyền là COMMENT trên GitHub, không phải tệp này.**

Với verdict của một MÔ HÌNH, kho quy ước tệp có băm là nguồn và comment là bản chiếu. Lượt
`human_audited` thì ngược lại. §8 neo nó vào **danh tính bền trên GitHub**, mà một tệp trong kho
không mang được danh tính ấy. Nên:

| | |
|---|---|
| nguồn có thẩm quyền | https://github.com/ducthangho/tra-luat/pull/681#issuecomment-5894711486 |
| tác giả | `ducthangho` · `author_association: OWNER` (KHÔNG phân biệt được người với phiên agent, xem #566) |
| thời điểm | `2026-09-29T16:51:51Z` (`updated_at` bằng `created_at`, tức comment chưa bị sửa) |
| ai đăng | chủ kho tự dán. Phiên điều phối chỉ soạn văn bản và KHÔNG gọi API đăng comment này |

## Phép đo bản ĐÃ ĐẾN

Đọc ngược qua REST `GET /repos/ducthangho/tra-luat/issues/comments/5894711486`, đo trên BYTE THÔ
của trường `body`:

| | giá trị |
|---|---|
| byte | **2765** |
| xuống dòng | LF × 34, CRLF × 0 |
| kết thúc | không có LF cuối |
| sha256 | `4f013241ce72f21503e082a0e7b81648bb39ba3d70338b3d64c82aa84c8c2bc4` |
| `Reviewed commit:` | đúng **1** lần |
| SHA đầy đủ `41d52ae4…dc360` | đúng **1** lần |

Bản ĐÃ ĐẾN **không** khớp từng byte với bản nháp phiên điều phối soạn. Chủ kho dán văn bản **đã
render**, nên cú pháp Markdown mất: tiêu đề `##`, dấu backtick, số thứ tự danh sách và dòng trống.
Nội dung chữ giữ nguyên. Tầng nào bỏ định dạng thì **KHÔNG ĐO ĐƯỢC** (clipboard, trình duyệt hay ô
nhập). Không suy thêm.

KHÔNG sửa comment gốc cho khớp. Comment là nguồn có thẩm quyền; sửa nó là **thay** bằng chứng, không
phải **vá**.

Dưới đây chép nguyên văn thân comment ĐÃ ĐẾN, từng byte, rồi thêm một LF cuối cho tệp. Sửa tệp này
**không** đổi được verdict; muốn đổi thì phải đổi ở comment.

---

VERDICT — human_audited · approve
Reviewed commit: 41d52ae461b267f7f5291a0794c5328cc00dc360
dang_boi: chu_kho_tu_dang
assurance_target: human_audited
review_class: sensitive
packet: #675 CAI-CONG-CU-SIGPIPE revision 2 / generation 2
lease: cai-cong-cu-sigpipe-r2-g2-claude (thay_the_cho cai-cong-cu-sigpipe-r1-g1-claude)
spec: ops/specs/CAI-CONG-CU-SIGPIPE-r2.md @ acbd000 · sha256 81fb6d533a892ec33c9b6b3f161dc1eca971579f4acfdb277c26521539be71cc
immutable_acceptance_baseline: cd23c7dbc7833d64a8e87e8ffd94f194c18e0060
Tôi đã tự đọc spec r2 và toàn bộ diff của W1–W5 trên đúng head này. Diff tính từ cd23c7d chỉ chạm năm tệp, +297/−5:
ops/cai_cong_cu.sh
ops/cai_actionlint.sh
ops/dung_goi_review.sh
ops/don_ref_chot_test.sh
ops/do_sigpipe.sh
Diff 89fc4fa..41d52ae cũng chỉ chạm đúng năm tệp ấy. Tôi không dựa vào bản tóm tắt của executor.
Chấp nhận:
Bản vá sản phẩm (W1–W3, W5):
Ba phép gán printf … | head -1 dưới set -euo pipefail được thay bằng khai triển tham số.
if ! printf … | grep -q trong don_ref_chot_test.sh được thay bằng dò đầu từng đối số bằng case (B1).
Cả năm lượt Codex đều xác nhận các thay đổi này đúng.
W4 ops/do_sigpipe.sh là phép đo phản chứng chạy tay, chưa nối vào CI.
Codex lượt 5 (gpt-6-astra/xhigh) cho approved, 0 P1 / 0 P2 / 0 P3, trên đúng SHA này:
Tệp: ops/reviews/cai-cong-cu-sigpipe-r2-review-5-codex-verdict.md, sha256 e8df38feba3818407c25527b10ac9ae57da0104e0e4a84a0fe4125ba709572d4.
Mọi finding F1–F3, B1, G1–G4, H1–H4, I1 đều đã đóng.
Giới hạn tôi chấp nhận, theo quyết định checkpoint S3 lần 2 (#675):
J1 (lần thứ 5 cùng hình dạng phep-do-khong-neo-ma-chay): probe B1 của W4 gọi lam với một bộ đối số cố định, nên một hồi quy chỉ nằm ở nhánh tao-tag sẽ lọt.
Ba giới hạn executor tự khai: phá đồng thời trap và seam; gọi lam bằng đường tuyệt đối; PATH của caller.
W4 --lan 10 chạy khoảng 4 phút.
Cả ba nhóm giới hạn trên chuyển sang packet kế nhiệm: nối phản chứng vào CI, mở sau khi #668 land.
Land: merge master vào head bằng ngoại lệ master drift (§5.1).
BASE 89fc4fa.
DRIFT đến 44620e8 gồm 15 tệp. Tất cả nằm trong ops/specs/, ops/land/, ops/leases/.
Đã đối chiếu sáu kích hoạt, không trúng dòng nào. git merge-tree sạch.
Khai thẳng phạm vi chữ ký này: nó xác nhận "tôi đã đọc và chấp nhận". Nó KHÔNG phải một lượt dò tìm độc lập. Phép đo là của năm lượt Codex và phiên điều phối. Đừng đọc chữ ký này thành "đã soi ở mức reviewer".
