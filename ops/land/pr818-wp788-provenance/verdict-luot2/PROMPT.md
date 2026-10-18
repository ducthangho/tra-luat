# Cross-review lượt 2 (phân lớp) — packet wp788 (#788), `packet_loop.py kiem-gate`

Bạn là REVIEWER (họ openai) cho executor họ claude. KHÔNG sửa tệp nào trong kho, KHÔNG push, KHÔNG gọi
GitHub. Làm việc trong thư mục hiện tại (bản sao kho, detached tại head cần review). Thư mục nháp riêng:
`mktemp -d` ngoài kho.

## Định danh (băm là định danh)

- `reviewed_sha`: `git rev-parse HEAD` phải bằng `4ffae005eb1c434d660cbfb713ad21ed92115a8a`; khác ⇒ dừng, ghi `blocked`.
- Head lượt 1: `e995730464da03223cf636e49ad32e220c6ec720` (verdict lượt 1 `blocked`, P1=1 P3=1, bản chép ở
  `/tmp/claude-0/-home-user-tra-luat/aec15584-50e8-55b9-b3a8-d6a2cfe55128/scratchpad/rv2/.review/VERDICT_LUOT1.md`, sha256 `a56b90bafebf4e1669b60d148b359ed5e88b6b345ac650d42c3bac44be4208d3`).
- Delta từ lượt 1: hai commit — `49a47ba` merge `origin/master` `d347d42` (PR #801, chỉ
  `.claude/skills/soan-spec/SKILL.md`; xử lý drift cho check `thu-hoi`) và `4ffae00` vá F01/F02.
- base spec: `d8b15cb0730c85e7019aee627c3bfa645a6d3eaf`; nền so delta mới: `d347d426334bbe1bbb1161184ab0acffee9be054`.
- spec: `/tmp/claude-0/-home-user-tra-luat/aec15584-50e8-55b9-b3a8-d6a2cfe55128/scratchpad/rv2/.review/SPEC.md`, sha256 phải bằng `82dc170446c3a4431739a3effbec8cb55adadc13d69f5c510f8782a2b45eb54e`.
- write set: `.claude/dev/packet_loop.py`, `.claude/dev/packet_loop_test.py`. Lớp review `sensitive`.
- Chủ kho đã quyết (trên #788) vá F01 trong packet này sau checkpoint H3=4 và review theo phân lớp.

## Ghi verdict TĂNG DẦN

Tạo `/tmp/claude-0/-home-user-tra-luat/aec15584-50e8-55b9-b3a8-d6a2cfe55128/scratchpad/rv2/.review/VERDICT.md` NGAY (dòng đầu `verdict: dang_review`), nối thêm sau mỗi mục; cuối cùng sửa dòng
đầu thành `verdict: approve | changes_requested | blocked`.

## Phân lớp — làm theo đúng thứ tự, đừng làm lại lượt 1

**Lớp A — ĐỐI CHIẾU LƯỢT TRƯỚC (bắt buộc).** Với F01 và F02 của lượt 1: ĐÃ ĐÓNG / CHƯA ĐÓNG / ĐÓNG MỘT PHẦN,
kèm lệnh + output thật trên head này. Dựng lại đúng các probe của lượt 1 (cùng id khác suite; khác tên; một
id hai tên bắt buộc; mâu thuẫn xuyên trang; bản trùng nhất quán; `--check-suite` 4301 chữ số) bằng
`python -c 'import json; …'` trong thư mục nháp rồi chạy `python .claude/dev/packet_loop.py kiem-gate …`.

**Lớp B — diff MỚI.** `git diff e995730464da03223cf636e49ad32e220c6ec720 HEAD -- .claude/dev` và
`git diff --numstat d347d426334bbe1bbb1161184ab0acffee9be054 HEAD` (trần ≤ 3 tệp, ≤ 300 dòng thêm so
nền — đo con số, đừng nhận lời). Kiểm commit merge không mang thay đổi nào khác ngoài nội dung của
`d347d42`: `git diff d347d426334bbe1bbb1161184ab0acffee9be054 HEAD --stat` chỉ được có hai tệp write set.

**Lớp C — săn lớp H3 TRÊN CODE MỚI** — *"lệnh tin bằng chứng hơn mức bằng chứng chứng minh được"*. Chốt
danh tính F01 và đường F02 có tạo đường vào H3 mới không (ví dụ: so danh tính thiếu trường nào lệnh dùng để
quyết xanh; dự phòng F02 có thể khớp nhầm; thứ tự kiểm làm một chốt che chốt khác)? Liệt kê mọi trường lệnh
đọc để quyết XANH và đối chiếu với tập trường của chốt danh tính. Finding H3 mới ⇒ ghi rõ "H3" (H3 hiện 4;
lên 5 là dừng packet).

**Lớp D — bảng đột biến.** `bash /tmp/claude-0/-home-user-tra-luat/aec15584-50e8-55b9-b3a8-d6a2cfe55128/scratchpad/rv2/.review/mut_all.sh "$PWD/.claude/dev" kg_ <thư-mục-nháp>` (mỗi đột biến
một bản sao, một tiến trình, `-B`, `PYTHONDONTWRITEBYTECODE=1`). Audit TOÀN BỘ trong MỘT lượt, nhưng CHỈ
cần trình bày chi tiết: các đột biến mới hoặc đổi (`kg_f01_*`, `kg_f02_*`, `kg_n1_bo_kiem_dang`,
`kg_n2_chi_kiem_bat_buoc`) và mọi ô có trạng thái khác lượt 1. Executor khai: `kg_f02_bo_bat_tran_int` chết
bằng traceback CÓ CHỦ Ý (lỗi đang khoá chính là traceback) và được bù bằng `kg_f02_du_phong_khop_nham` chết
vì đổi màu — hãy thẩm định lời khai này, đừng nhận. Gom mọi ô sai chốt vào MỘT finding kèm một HINT.

**Lớp E — gate.** `python -B .claude/dev/packet_loop_test.py` chạy NỀN ngay từ đầu
(`> /tmp/claude-0/-home-user-tra-luat/aec15584-50e8-55b9-b3a8-d6a2cfe55128/scratchpad/rv2/.review/suite.out 2>&1`), đòi `nền: N/N` hai số bằng nhau và `TỔNG: ĐẠT`. Không cần làm lại ma trận
N1–N7 từ đầu: chỉ cập nhật ô nào đổi so lượt 1.

Phản chứng chỉ là dữ liệu JSON và đối số CLI; đừng soạn nội dung dạng tấn công đường dẫn hay mã độc.

## Ngoài phạm vi (spec `ngoai_pham_vi`) — không ghi finding

Không gọi mạng; không `--run-id`; không neo `app`; không nối `land-packets`; không xác thực tệp là phản hồi
API thật hay suite thuộc đúng `ci.yml`.

## Dạng finding và kết luận

Mỗi finding: `id`, `P1|P2|P3`, trục, lớp, tệp:dòng, bằng chứng chạy được, HINT (P1/P2 bắt buộc). Ngưỡng
`sensitive`: approve chỉ khi P0=P1=P2=0 và mỗi P3 có hướng xử lý. Mục `ĐỐI CHIẾU LƯỢT TRƯỚC` bắt buộc. Kết
thúc bằng `reviewed_sha`, verdict, đếm P1/P2/P3, bảng ô N1–N7 đã đổi so lượt 1.
