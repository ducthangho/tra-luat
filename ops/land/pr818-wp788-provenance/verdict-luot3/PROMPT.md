# Cross-review lượt 3 (phân lớp) — packet wp788 (#788), `packet_loop.py kiem-gate`

Bạn là REVIEWER (họ openai) cho executor họ claude. KHÔNG sửa tệp nào trong kho, KHÔNG push, KHÔNG gọi
GitHub. Làm việc trong thư mục hiện tại (bản sao kho, detached tại head cần review). Thư mục nháp riêng:
`mktemp -d` ngoài kho.

## Định danh (băm là định danh)

- `reviewed_sha`: `git rev-parse HEAD` phải bằng `8264089a14f79867091da2629edbf45a22854c39`; khác ⇒ dừng, ghi `blocked`.
- Lượt 1 (`e995730`, `blocked`, F01 P1 + F02 P3) — `/tmp/claude-0/-home-user-tra-luat/aec15584-50e8-55b9-b3a8-d6a2cfe55128/scratchpad/rv3/.review/VERDICT_LUOT1.md`, sha256 `a56b90ba…08d3`.
- Lượt 2 (`4ffae005eb1c434d660cbfb713ad21ed92115a8a`, `changes_requested`, F03 P2; F01/F02 ĐÃ ĐÓNG) —
  `/tmp/claude-0/-home-user-tra-luat/aec15584-50e8-55b9-b3a8-d6a2cfe55128/scratchpad/rv3/.review/VERDICT_LUOT2.md`, sha256 `12d77d786cfe7af5ec915c1c48c76a0583d5b78191bdb69243c6dbcc1d05f3c4`.
- Delta từ lượt 2: một commit `8264089` (chỉ test) vá F03 theo đúng HINT lượt 2.
- base spec: `d8b15cb0730c85e7019aee627c3bfa645a6d3eaf`; nền so delta mới: `d347d426334bbe1bbb1161184ab0acffee9be054`.
- spec: `/tmp/claude-0/-home-user-tra-luat/aec15584-50e8-55b9-b3a8-d6a2cfe55128/scratchpad/rv3/.review/SPEC.md`, sha256 phải bằng `82dc170446c3a4431739a3effbec8cb55adadc13d69f5c510f8782a2b45eb54e`.
- write set: `.claude/dev/packet_loop.py`, `.claude/dev/packet_loop_test.py`. Lớp review `sensitive`.
- Chủ kho đã quyết: vá trong packet này, review phân lớp, **lặp tới khi hết P1/P2/P3** — tức lượt này
  cần săn cả P3 trên TOÀN BỘ diff so `d347d42` (không chỉ delta), vì một P3 bỏ sót là một vòng vá nữa.

## Ghi verdict TĂNG DẦN

Tạo `/tmp/claude-0/-home-user-tra-luat/aec15584-50e8-55b9-b3a8-d6a2cfe55128/scratchpad/rv3/.review/VERDICT.md` NGAY (dòng đầu `verdict: dang_review`), nối thêm sau mỗi mục; cuối cùng sửa dòng
đầu thành `verdict: approve | changes_requested | blocked`.

## Phân lớp — làm theo đúng thứ tự, đừng làm lại lượt 1

**Lớp A — ĐỐI CHIẾU LƯỢT TRƯỚC (bắt buộc).** F03 của lượt 2: ĐÃ ĐÓNG / CHƯA ĐÓNG, kèm lệnh + output
thật (bảng đột biến không còn ô nào chết bằng traceback; ca nền `kg_f02_suite_vuot_tran_int` và đột biến
`kg_f02_du_phong_khop_nham` còn nguyên và còn răng). F01/F02 chỉ cần xác nhận lại một probe mỗi cái.

**Lớp B — diff mới** `git diff 4ffae005eb1c434d660cbfb713ad21ed92115a8a HEAD`, và đo lại
`git diff --numstat d347d426334bbe1bbb1161184ab0acffee9be054 HEAD` (trần ≤ 3 tệp, ≤ 300 dòng thêm).

**Lớp C — rà TOÀN BỘ diff so `d347d42` lần cuối, săn mọi mức P1–P3.** Hai lượt trước chủ yếu săn H3; lượt
này thêm: tính đúng của thông điệp lỗi/cảnh báo (định dạng N4 đúng nguyên văn spec), `--help`/epilog,
chú thích nói đúng điều mã làm (lời khai trong comment phải đo được), tên ca test khớp điều nó đo, ca nào
trong `nghiem_thu` còn thiếu ca test hoặc thiếu đột biến, và mọi chỗ `_kg_dem` tự điền `total_count` có
thể làm một ca đo nhầm chốt. Lớp H3 vẫn săn (H3 = 4; lên 5 là dừng packet).

**Lớp D — bảng đột biến.** `bash /tmp/claude-0/-home-user-tra-luat/aec15584-50e8-55b9-b3a8-d6a2cfe55128/scratchpad/rv3/.review/mut_all.sh "$PWD/.claude/dev" kg_ <thư-mục-nháp>`. Audit TOÀN BỘ
trong MỘT lượt; trình bày chi tiết chỉ các ô có trạng thái khác lượt 2. Traceback = tín dụng giả, không
ngoại lệ. Gom mọi ô sai chốt vào MỘT finding.

**Lớp E — gate.** `python -B .claude/dev/packet_loop_test.py` chạy NỀN ngay từ đầu
(`> /tmp/claude-0/-home-user-tra-luat/aec15584-50e8-55b9-b3a8-d6a2cfe55128/scratchpad/rv3/.review/suite.out 2>&1`); đòi `nền: N/N` hai số bằng nhau và `TỔNG: ĐẠT`.

Phản chứng chỉ là dữ liệu JSON và đối số CLI; đừng soạn nội dung dạng tấn công đường dẫn hay mã độc.

## Ngoài phạm vi (spec `ngoai_pham_vi`) — không ghi finding

Không gọi mạng; không `--run-id`; không neo `app`; không nối `land-packets`; không xác thực tệp là phản hồi
API thật hay suite thuộc đúng `ci.yml`.

## Dạng finding và kết luận

Mỗi finding: `id`, `P1|P2|P3`, trục, lớp, tệp:dòng, bằng chứng chạy được, HINT (P1/P2 bắt buộc). Ngưỡng
`sensitive`: approve chỉ khi P0=P1=P2=0 và mỗi P3 có hướng xử lý; nhưng hãy BÁO mọi P3 tìm được — chủ kho muốn vá cả P3. Mục `ĐỐI CHIẾU LƯỢT TRƯỚC` bắt buộc. Kết
thúc bằng `reviewed_sha`, verdict, đếm P1/P2/P3, bảng ô N1–N7 đã đổi so lượt 2.
