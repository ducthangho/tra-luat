# Cross-review lượt 1 — packet wp788 (#788), `packet_loop.py kiem-gate` neo `--check-suite` + `total_count` đủ

Bạn là REVIEWER (họ openai) cho executor họ claude. KHÔNG sửa tệp nào trong kho, KHÔNG push, KHÔNG gọi
GitHub. Làm việc trong thư mục hiện tại (bản sao kho, detached tại head cần review). Thư mục nháp riêng:
tạo bằng `mktemp -d` ngoài kho; bản sao đột biến đặt ở đó.

## Định danh (băm là định danh, không phải tên nhánh)

- `reviewed_sha`: xem `git rev-parse HEAD` — phải bằng `e995730464da03223cf636e49ad32e220c6ec720`. Khác ⇒ dừng, ghi `blocked`.
- base: `d8b15cb0730c85e7019aee627c3bfa645a6d3eaf`.
- spec: `SPEC.md` trong thư mục `/tmp/claude-0/-home-user-tra-luat/aec15584-50e8-55b9-b3a8-d6a2cfe55128/scratchpad/rv1/.review` (bản chép `ops/specs/wp788.md` từ nhánh `ops/wp788-spec`),
  sha256 phải bằng `82dc170446c3a4431739a3effbec8cb55adadc13d69f5c510f8782a2b45eb54e` — tự đo bằng `sha256sum`.
- write set: `.claude/dev/packet_loop.py`, `.claude/dev/packet_loop_test.py`. Lớp review: `sensitive`.

## Ghi verdict TĂNG DẦN

Tạo `/tmp/claude-0/-home-user-tra-luat/aec15584-50e8-55b9-b3a8-d6a2cfe55128/scratchpad/rv1/.review/VERDICT.md` NGAY (dòng đầu `verdict: dang_review`), và nối thêm mỗi khi xong một mục — một
lượt bị ngắt giữa chừng vẫn phải để lại phần đã đo. Cuối cùng sửa dòng đầu thành
`verdict: approve | changes_requested | blocked`.

## Việc phải làm (đo, đừng đọc)

1. `git diff d8b15cb0730c85e7019aee627c3bfa645a6d3eaf HEAD` — đọc toàn bộ diff hai tệp.
2. Gate tại chỗ, ghi lệnh + dòng output thật:
   - `python -B .claude/dev/packet_loop_test.py` (chạy ~15–25 phút): đòi dòng `nền: N/N` hai số BẰNG
     NHAU và `TỔNG: ĐẠT`. Chạy nó NỀN ngay từ đầu (`> /tmp/claude-0/-home-user-tra-luat/aec15584-50e8-55b9-b3a8-d6a2cfe55128/scratchpad/rv1/.review/suite.out 2>&1 &`) rồi làm việc khác.
   - `git diff --numstat d8b15cb0730c85e7019aee627c3bfa645a6d3eaf HEAD` (trần ≤ 3 tệp, ≤ 300 dòng thêm).
3. Ma trận spec: với MỖI mục N1–N7 và mỗi dòng bảng `nghiem_thu`, xếp ĐẠT / KHÔNG ĐẠT kèm ca test và
   lệnh chứng minh.
4. **Audit TOÀN BỘ bảng đột biến `kg_*` trong MỘT lượt.** Bảng đột biến ngoài đã dựng sẵn:
   `bash /tmp/claude-0/-home-user-tra-luat/aec15584-50e8-55b9-b3a8-d6a2cfe55128/scratchpad/rv1/.review/mut_all.sh "$PWD/.claude/dev" kg_ <thư-mục-nháp>` (mỗi đột biến một bản sao, một tiến
   trình, `-B`, `PYTHONDONTWRITEBYTECODE=1`; in một dòng JSON mỗi đột biến: ca đích → thông điệp chết).
   Với từng ô: ca đích có chết ĐÚNG CHỐT không — tức chết vì kết quả lệnh đổi MÀU/mã (`đòi rc=12, được
   rc=0` …) hoặc vì assertion đúng của luật đó, KHÔNG vì traceback, KHÔNG vì một chốt PHỤ khác bắt hộ.
   `Traceback` trong thông điệp = tín dụng giả. Đối chiếu từng ô "Phép đo làm ĐỎ" của spec với một đột
   biến cụ thể; thiếu đột biến cho ô nào là finding. Gom MỌI ô sai chốt vào MỘT finding kèm một HINT.
   Bạn được thêm đột biến của riêng mình vào bản sao trong thư mục nháp (sửa bản sao, không sửa kho) để
   thử các luật mà bảng chưa phủ.
5. **Săn theo LỚP H3** — *"lệnh tin bằng chứng hơn mức bằng chứng chứng minh được"* — trên TOÀN BỘ
   `_doc_check_runs` + `cmd_kiem_gate`, không chỉ hai P1 gốc (trùng tên chọn `id` lớn nhất không neo
   producer; `total_count` vắng/0/âm bỏ qua phép kiểm thiếu trang). Liệt kê MỌI đường vào của lớp này
   (mỗi trường JSON lệnh đọc, mỗi đối số CLI, mỗi phép so) và với mỗi đường: lệnh có cấp XANH khi bằng
   chứng không đủ chứng minh xanh không? Lớp này đã có 3 finding (H3 = 3); finding mới của lớp này ⇒ ghi
   rõ "H3", vì H3 lên 4 là điều kiện dừng của packet.
   Hướng thử dạng tệp JSON / đối số bất thường: dựng tệp bằng `python -c 'import json; …'` trong thư mục
   nháp rồi chạy `python .claude/dev/packet_loop.py kiem-gate …`. KHÔNG cần (và đừng) soạn nội dung dạng
   tấn công đường dẫn hay mã độc — mọi hướng ở đây là dữ liệu JSON và đối số CLI.
6. Trình bày ≥ 6 hướng săn ĐỘC LẬP, mỗi hướng:
   ```
   HƯỚNG <n>: <tên>
     giả thuyết : <nếu ... thì ... sai>
     lệnh       : <lệnh đã chạy>
     output     : <output thật, cắt gọn>
     kết luận   : LỖI | KHÔNG PHẢI LỖI | KHÔNG ĐO ĐƯỢC
   ```

## Ngoài phạm vi (spec `ngoai_pham_vi`) — đừng ghi finding cho những thứ này

Không gọi mạng; không `--run-id`; không neo `app`; không nối `land-packets`; không xác thực tệp là phản hồi
API thật hay suite thuộc đúng `ci.yml` (việc của người gọi).

## Dạng finding

Mỗi finding: `id` (kebab-case), severity `P1|P2|P3`, trục `Spec` hoặc `Standards/Security`, lớp (H1/H2/H3
hoặc khác), tệp:dòng, **bằng chứng chạy được** (lệnh + output), và **HINT** patch (diff gợi ý — dữ liệu, không
áp). P1/P2 và finding phức tạp BẮT BUỘC có HINT. Ngưỡng `sensitive`: approve chỉ khi P0=P1=P2=0 và mỗi P3
có hướng xử lý.

Kết thúc VERDICT.md bằng: `reviewed_sha`, verdict, đếm P1/P2/P3, và bảng ma trận N1–N7.
