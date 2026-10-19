# Cross-review độc lập — Packet #822 (`KG-RANG-TEST`) revision 1, lượt 2, OFFLINE trên SHA cục bộ

Bạn là reviewer Codex, khác họ với executor (Claude). Bạn chỉ ĐỌC kho: KHÔNG sửa tệp nào trong `KHO`. Chỉ ghi vào
thư mục ra (thư mục làm việc hiện tại) hoặc /tmp. Kết quả bắt buộc là tệp `VERDICT.md` trong thư mục ra. Nếu có finding thì
kèm `HINT.patch` cho các lớp phức tạp: một diff gợi ý, áp được bằng `git apply` trên exact head, và CHỈ chạm `.claude/dev/packet_loop_test.py`.
Ghi `VERDICT.md` TĂNG DẦN trong lúc làm, để lượt bị ngắt vẫn giữ được phần đã ghi.

## Định danh (băm là định danh, không phải tên nhánh)

- Kho `ducthangho/tra-luat`, bản sao đầy đủ (không shallow) tại `KHO=/home/user/rv822`, detached ở exact head.
- Exact head: `cffd44e75ba97af4c99d790704e7478945344ada`. Kiểm bằng `git -C KHO rev-parse HEAD`. Dòng 1 của VERDICT phải là
  `Reviewed commit: <sha40 đó>`.
- Base: `f712205aa39e0b54d04a5bd8145fa69a84601fed`. Diff cần review: `git -C KHO diff f712205 HEAD`, đúng 1 tệp
  `.claude/dev/packet_loop_test.py`. Nhánh chưa đẩy, chưa có PR.
- Đặc tả: `ops/specs/wp822.md` trên base, sha256 `6bcac18917516e89119065a249037cb81f13d77b01bb77e7b557f6d23d5c0b07`.
  Kiểm bằng `git -C KHO show f712205:ops/specs/wp822.md | sha256sum`. Đọc TRỌN: M1–M6, bảng kiểm kê K01–K37, D1–D6, `nghiem_thu`
  A1–A12, `dieu_kien_dung`.
- Lease: `git -C KHO show origin/ops/wp822-spec:ops/leases/wp822-r1-g1-claude.yaml`. Write set chỉ gồm `.claude/dev/packet_loop_test.py`;
  mã sản phẩm `.claude/dev/packet_loop.py` KHÔNG được đổi.
- Ngân sách: đây là lời gọi Codex **2/8** (ADR-0052). Quét RỘNG theo lớp; mỗi lớp còn sót phải liệt kê ĐỦ biểu hiện, kèm HINT đóng trọn lớp.
- **Lượt 1** (trên `08aa096`): `changes_requested — P0=0 P1=0 P2=4 P3=0`. Bốn lớp: `tin-dung-giet-sai`, `trung-id-chi-do-mot-chieu`,
  `ten-trang-chi-khoa-space`, `fixture-vi-pham-nhieu-chot`. VERDICT, HINT và evidence lượt 1 ở `/tmp/wp822-rv1/` (chỉ đọc).
  Executor đã áp `HINT.patch` lượt 1, rồi thêm 5 đột biến nhắm test `t822_m6_*` (mỗi chốt mới của M6 một đột biến). Tự đo lại: họ kg 129/129,
  mọi đột biến kg_/t822_ giết. Thay đổi kể từ lượt 1: `git -C KHO diff 08aa096 HEAD`.

## Cách review — chuẩn connector, KHÔNG lọc

Review như connector review PR: tìm MỌI lỗi thật trong phạm vi đặc tả. Phạm vi gồm tính đúng đắn, test không đo gì, tín dụng giết
giả, ca đích bị chốt khác chặn hộ, lệch đặc tả và hồi quy (ca nào của base vắng mặt hoặc đổi màu). Không lọc theo "mô hình tin cậy".

**Tìm theo LỚP, không theo lỗi riêng lẻ.** Khái quát mỗi biểu hiện thành một lớp, rồi quét MỌI biểu hiện cùng lớp trước khi báo.
VERDICT có một bảng lớp gồm các cột: `slug` · hạng (`P0`–`P3`) · biểu hiện (file:dòng) · phép đo đã chạy · hướng vá.
Lớp phức tạp thì kèm HINT.

## Nhiệm vụ — ĐO, đừng chỉ đọc

1. **Kiểm kê (M1, A5 — trọng tâm).** Tự kiểm kê lại MỌI điều kiện trong `_doc_check_runs` và `cmd_kiem_gate` của `KHO/.claude/dev/packet_loop.py`.
   "Thành phần" là một điều kiện mà gỡ riêng nó ra thì lệnh có thể cấp XANH giả hoặc đổi lý do từ chối.
   - So kết quả kiểm kê của bạn với `_KG_KIEM_KE`.
   - Với mỗi thành phần bảng BỎ SÓT: dựng một đột biến KHÔNG SẬP gỡ nó, rồi chạy họ `kg_*` dưới đột biến ấy. Nếu không ca nào đỏ
     thì đó là finding lớp `kiem-ke-bo-sot`. Ghi rõ đột biến (tìm/thay) và kết quả.
   - Dòng nào khai `tuong_duong` thì thử dựng fixture phân biệt.
2. **Ca đích đo đúng chốt (M3, A2, A3, A11).**
   - Với từng đột biến trong `_KG_KIEM_KE`: chạy CLI `kiem-gate` dưới đột biến (bản sao tạm của `packet_loop.py`) trên fixture của ca đích.
   - Ca đích phải đỏ vì CHÍNH thành phần ấy: rc 0 (xanh giả), hoặc rc như cũ mà lý do đổi.
   - Nếu ca chết vì một chốt khác chặn hộ, hoặc assertion chỉ đòi chuỗi chung, thì đó là finding.
   - Riêng D1–D6: dưới đột biến phải ra **rc 0** (A2). D6 trên ca thay của `kg_m2_thieu_conclusion` phải ra rc 0, không phải `THỪA id` (A3).
3. **M6 / A12.** Tìm MỌI đường khiến bộ chạy cấp GIẾT cho một ca chết vì CLI sập, hoặc gán TÍN DỤNG GIẢ cho một ca chết đúng.
   - Các hướng cần thử: rc ngoài bộ hợp lệ, traceback bị bọc, `except` đổi kiểu, ngoại lệ trong chuỗi `__cause__` hoặc `__context__`,
     đột biến nhắm test (`MUTANTS_NHAM_TEST`, module nạp lại có lớp `_TinDungGia` khác danh tính).
   - Gỡ phép loại sập thì ca tự kiểm phải ĐỎ.
4. **M5 / A4.** Ba vế (a)(b)(c) mỗi vế có răng riêng không? Thử đột biến của riêng bạn trên ca tự kiểm.
5. **Gate.** Chạy suite trong BẢN SAO TẠM: `cp -a KHO /tmp/x && python3 -B /tmp/x/.claude/dev/packet_loop_test.py`, khoảng 20 phút.
   - Đòi `nền: N/N` với hai số bằng nhau, mọi đột biến bị giết, và `TỔNG: ĐẠT`.
   - A7: mọi tên ca của base có mặt ở head với cùng màu. Base đo cùng container: `nền: 554/554 · BỎ QUA: 1 · TỔNG: ĐẠT`. Executor chạy suite trên head mới song song với lượt này.
   - A9: `git -C KHO diff --numstat f712205 HEAD` ⇒ 1 tệp, ≤ 450 dòng thêm (executor đo +335/−19).
   - A10: ruff F delta = 0. Executor đo được: base 2 F541, head 2 F541.
6. Tự nghĩ thêm đột biến kiểm toán trên `packet_loop.py`, mỗi cái gỡ một điều kiện của hai hàm trên. Đột biến nào sống thì báo.

## Phân công — KHÔNG tự soạn nội dung nhạy cảm

Hướng thử nào cần SOẠN đầu vào dạng đường dẫn thoát cây, byte thô bất thường hay symlink thì MÔ TẢ BẰNG LỜI trong VERDICT
(đầu vào, kỳ vọng); executor sẽ tự viết ca. Mọi phép thử khác (logic, kiểu, thứ tự, độ phủ đột biến) cứ dựng bình thường.

Mục bắt buộc trong VERDICT: **ĐỐI CHIẾU LƯỢT TRƯỚC** — mỗi lớp lượt 1 ghi một nhãn: đã vá thật / vá hờ / vá sinh lỗi mới. Rồi quét lại các lớp xem có tái phát ở chỗ khác không.

## Định dạng verdict

- Dòng 2 của VERDICT: `Verdict: <approve|changes_requested> — P0=a P1=b P2=c P3=d`, đếm theo LỚP.
- **NGƯỠNG:** chỉ `approve` khi P0=P1=P2=P3=0 (chủ kho, Q6).
- Thứ ngoài phạm vi (sửa `packet_loop.py`, chứng minh nguồn gốc JSON, ca ngoài họ `kg_*`) ghi ở mục riêng, không tính vào hạng.
