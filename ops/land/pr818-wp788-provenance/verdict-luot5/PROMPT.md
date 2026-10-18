# Cross-review lượt 5 (phân lớp) — packet wp788 (#788), `packet_loop.py kiem-gate`

Bạn là REVIEWER (họ openai) cho executor họ claude. KHÔNG sửa tệp nào trong kho, KHÔNG push, KHÔNG gọi
GitHub. Làm việc trong thư mục hiện tại (bản sao kho, detached tại head cần review). Thư mục nháp riêng:
`mktemp -d` ngoài kho.

## Định danh (băm là định danh)

- `reviewed_sha`: `git rev-parse HEAD` phải bằng `984032f375aa0c8fe6039dfd35f6842acd49c926`; khác ⇒ dừng, ghi `blocked`.
- Lượt 1 (`e995730`, `blocked`, F01 P1 + F02 P3) — `/tmp/claude-0/-home-user-tra-luat/aec15584-50e8-55b9-b3a8-d6a2cfe55128/scratchpad/rv5/.review/VERDICT_LUOT1.md`, sha256 `a56b90ba…08d3`.
- Lượt 2 (`4ffae005eb1c434d660cbfb713ad21ed92115a8a`, `changes_requested`, F03 P2; F01/F02 ĐÃ ĐÓNG) —
  `/tmp/claude-0/-home-user-tra-luat/aec15584-50e8-55b9-b3a8-d6a2cfe55128/scratchpad/rv5/.review/VERDICT_LUOT2.md`, sha256 `12d77d786cfe7af5ec915c1c48c76a0583d5b78191bdb69243c6dbcc1d05f3c4`.
- Lượt 3 (`8264089a14f79867091da2629edbf45a22854c39`, `changes_requested`, F04 P3 + F05 P3; F01/F02/F03 ĐÃ
  ĐÓNG) — `/tmp/claude-0/-home-user-tra-luat/aec15584-50e8-55b9-b3a8-d6a2cfe55128/scratchpad/rv5/.review/VERDICT_LUOT3.md`, sha256 `376c2d8cb91a73be9d74cad10ff97ef88db22bf15294cfb7819a673adc0b845f`.
- Lượt 4 (`47591ebc51af917523e67191b2e96939506b78fe`, `changes_requested`, F04 P3 tái mở — tên chứa ký tự
  ngắt dòng tách dòng cảnh báo N4; F05 ĐÃ ĐÓNG) — `/tmp/claude-0/-home-user-tra-luat/aec15584-50e8-55b9-b3a8-d6a2cfe55128/scratchpad/rv5/.review/VERDICT_LUOT4.md`, sha256
  `ebfddfb6e6fdc03b4c53e5989061864b14680967700821072ce7b54889aa5f75`.
- Delta từ lượt 4: một commit. **Chính sách do chủ kho chốt** (issue #788, 18-10): `--bat-buoc` chứa bất kỳ
  ký tự nào `str.splitlines()` cắt ⇒ `RC_ARG` (thay đổi miền CLI có quyết định). Chủ kho cũng **cho phép vượt
  trần 300 dòng thêm** cho packet này (đo được 316) — KHÔNG ghi finding cho việc vượt trần ấy.
- base spec: `d8b15cb0730c85e7019aee627c3bfa645a6d3eaf`; nền so delta mới: `d347d426334bbe1bbb1161184ab0acffee9be054`.
- spec: `/tmp/claude-0/-home-user-tra-luat/aec15584-50e8-55b9-b3a8-d6a2cfe55128/scratchpad/rv5/.review/SPEC.md`, sha256 phải bằng `82dc170446c3a4431739a3effbec8cb55adadc13d69f5c510f8782a2b45eb54e`.
- write set: `.claude/dev/packet_loop.py`, `.claude/dev/packet_loop_test.py`. Lớp review `sensitive`.
- Chủ kho đã quyết: vá trong packet này, review phân lớp, **lặp tới khi hết P1/P2/P3** — tức lượt này
  cần săn cả P3 trên TOÀN BỘ diff so `d347d42` (không chỉ delta), vì một P3 bỏ sót là một vòng vá nữa.

## Ghi verdict TĂNG DẦN

Tạo `/tmp/claude-0/-home-user-tra-luat/aec15584-50e8-55b9-b3a8-d6a2cfe55128/scratchpad/rv5/.review/VERDICT.md` NGAY (dòng đầu `verdict: dang_review`), nối thêm sau mỗi mục; cuối cùng sửa dòng
đầu thành `verdict: approve | changes_requested | blocked`.

## Phân lớp — làm theo đúng thứ tự, đừng làm lại lượt 1

**Lớp A — ĐỐI CHIẾU LƯỢT TRƯỚC (bắt buộc).** F04: dựng lại 11 biến thể ngắt dòng của lượt 4 (U+000A, 000B,
000C, 000D, 001C, 001D, 001E, 0085, 2028, 2029, CRLF) cả ở `--bat-buoc` lẫn ở `name` trong JSON; đòi: tên bắt
buộc chứa ngắt dòng ⇒ rc=2 với lý do nêu xuống dòng; run JSON mang tên ngắt dòng mà tên bắt buộc sạch thì
không có dòng cảnh báo nào bị tách (stderr mọi dòng `CẢNH BÁO:` đều đúng một dòng). Đối chứng: tab, chuỗi
`\` + `n`, nháy đơn/đôi, Unicode in được. F01/F02/F03/F05: một phép xác nhận mỗi cái.

**Lớp B — diff mới** `git diff 47591ebc51af917523e67191b2e96939506b78fe HEAD`; đo lại
`git diff --numstat d347d426334bbe1bbb1161184ab0acffee9be054 HEAD` (2 tệp trong write set; số dòng chỉ đo,
trần đã được chủ kho miễn). Kiểm chú thích mới nói đúng điều mã làm.

**Lớp C — rà TOÀN BỘ diff so `d347d42` lần cuối, săn mọi mức P1–P3.** Thêm: chốt từ chối ngắt dòng có làm
gãy ca/luồng nào khác (tên rỗng, tên chỉ khoảng trắng, tên trùng); `--help` hoặc lời nhắn có cần nêu ràng
buộc mới không; còn đường nào khác in tên ra stderr/stdout có thể tách dòng (dòng `ĐỎ`, dòng XANH, lý do
`VẮNG`) — nếu có, đó là một phần của F04 hay là ngoài hợp đồng N4. Lớp H3 vẫn săn (H3 = 4; lên 5 là dừng).

**Lớp D — bảng đột biến.** `bash /tmp/claude-0/-home-user-tra-luat/aec15584-50e8-55b9-b3a8-d6a2cfe55128/scratchpad/rv5/.review/mut_all.sh "$PWD/.claude/dev" kg_ <thư-mục-nháp>`. Audit TOÀN BỘ
trong MỘT lượt; trình bày chi tiết chỉ các ô có trạng thái khác lượt 4. Traceback = tín dụng giả, không
ngoại lệ. Gom mọi ô sai chốt vào MỘT finding.

**Lớp E — gate.** `python -B .claude/dev/packet_loop_test.py` chạy NỀN ngay từ đầu
(`> /tmp/claude-0/-home-user-tra-luat/aec15584-50e8-55b9-b3a8-d6a2cfe55128/scratchpad/rv5/.review/suite.out 2>&1`); đòi `nền: N/N` hai số bằng nhau và `TỔNG: ĐẠT`.

Phản chứng chỉ là dữ liệu JSON và đối số CLI; đừng soạn nội dung dạng tấn công đường dẫn hay mã độc.

## Ngoài phạm vi (spec `ngoai_pham_vi`) — không ghi finding

Không gọi mạng; không `--run-id`; không neo `app`; không nối `land-packets`; không xác thực tệp là phản hồi
API thật hay suite thuộc đúng `ci.yml`.

## Dạng finding và kết luận

Mỗi finding: `id`, `P1|P2|P3`, trục, lớp, tệp:dòng, bằng chứng chạy được, HINT (P1/P2 bắt buộc). Ngưỡng
`sensitive`: approve chỉ khi P0=P1=P2=0 và mỗi P3 có hướng xử lý; nhưng hãy BÁO mọi P3 tìm được — chủ kho muốn vá cả P3. Mục `ĐỐI CHIẾU LƯỢT TRƯỚC` bắt buộc. Kết
thúc bằng `reviewed_sha`, verdict, đếm P1/P2/P3, bảng ô N1–N7 đã đổi so lượt 4.
