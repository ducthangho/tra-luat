# PROMPT REVIEWER — bản thẩm định "vòng lặp tri thức" (PR "#214"). Neo `825558a5`.

Reviewer khác nền (codex) cho một PR **thuần tài liệu** do `claude` soạn. **Read-only.** Kho ở
`./kho`; tệp bạn tạo phải nằm NGOÀI cây ấy. Chốt: `git -C kho status --short` RỖNG ở cuối lượt,
HEAD vẫn `825558a59fd93623dd2f2c9123577361e9e3abca`.

## PR này là gì

12 tệp, tất cả `ops/`, `+1137/−0`, **0 dòng mã**. Nó ghi lại một cuộc thẩm định 3 vòng × 3 bên
về câu hỏi *"có nên tất định hoá việc lưu bài học không"*, kèm **6 báo cáo gốc** và 3 đề bài
neo băm. Kết luận: **KHÔNG** nên tất định hoá việc LƯU.

**Bạn là một trong ba bên ấy** — ba báo cáo `codex-vong{1,2,3}.md` là của một phiên codex khác.
Đừng coi đó là lợi thế: bạn KHÔNG có ký ức của phiên đó, và việc của bạn là kiểm xem bản hợp
nhất có **trung thực với các báo cáo gốc** hay không, chứ không phải xác nhận lại kết luận.

## Việc — bốn trục, xếp theo giá trị

**1. Bản hợp nhất có XUYÊN TẠC báo cáo gốc không?** Đây là trục quan trọng nhất và là thứ chỉ
review mới bắt được. `ops/THAM_DINH_VONG_LAP_TRI_THUC_20260821.md` tóm tắt 6 báo cáo trong
`ops/tham-dinh/tri-thuc-20260821/`. Đối chiếu từng khẳng định lớn với nguồn:
- Bản hợp nhất khai *"cả hai bên ĐỘC LẬP bác khung của đề bài"* — đúng không?
- Khai *"Fable rút chữ ký vòng 1 của chính mình"* và *"cả hai bên ĐỔI Ý ở vòng 2"* — đúng không?
- Khai vòng 3 *"hội tụ hoàn toàn"* — trong khi §5 lại ghi còn **một** khác biệt (lát 1 lấy
  check `a` hay `d`). Hai câu ấy có mâu thuẫn nhau không?

**2. `BAM.txt` có khớp không.** Chạy `sha256sum -c BAM.txt` trong thư mục ấy. Rồi hỏi tiếp:
bảng đầu tệp hợp nhất liệt kê băm **3 đề bài** — có khớp tệp thật không?

**3. Các CON SỐ trong bản hợp nhất có đo lại được không?** Nó khai nhiều số cụ thể; kiểm ít
nhất bốn cái, mỗi cái tự chạy lệnh:
- `seam` = **0/24** receipt và **0/41** lease
- khối "Bài học đắt giá" trong `CLAUDE.md` = **160** dòng kể tiêu đề
- `verdict_usage_caveats` có ở **14/24** receipt
- `chi_la_chu` = **0** occurrence toàn kho
Số nào lệch là finding. Lưu ý: kho đã đổi từ lúc soạn (nhiều PR đã land) — nếu số lệch **vì
cây đã đổi** chứ không vì bản hợp nhất sai, hãy nói rõ như vậy thay vì tính là lỗi.

**4. Có lời khai nào RỘNG HƠN phạm vi đo được không?** Mục 10 tự khai 6 thứ "KHÔNG đo được".
Đọc ngược: có khẳng định nào trong 9 mục còn lại đáng ra phải nằm ở mục 10 mà không nằm?
Đặc biệt soi mục 4 (bảng "4 lượt review hỏng") và mục 6 (thứ tự thi công).

## Bốn chốt của kho
1. Bằng chứng DƯƠNG, đừng dừng ở `rc=0`.
2. Ba trạng thái: `có` · `không` · **`KHÔNG ĐO ĐƯỢC`** — cái thứ ba phải được KHAI.
3. Đừng kết luận "X không có" từ một grep hẹp; hỏi "nếu X có thật thì nó được ghi ở đâu".
4. Khai thẳng thứ bạn không đo được.

Đây là PR tài liệu: **không có mã để chạy đột biến**. Đừng cố ép một khuôn review mã lên nó —
giá trị của lượt này nằm ở trục 1 và trục 4.

## Đầu ra
Mỗi finding: bằng chứng chạy được · mức (P0..P3) · bất biến bị cắt · gợi ý vá.
Kết thúc bằng đúng hai dòng, mỗi dòng ĐÚNG MỘT LẦN:

```
VERDICT: approve | changes_requested | blocked
Reviewed commit: 825558a59fd93623dd2f2c9123577361e9e3abca
```
