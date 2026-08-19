# Vòng 3 — chốt joint recommendation

Tiếp tục cùng session read-only. Codex nhận các kết luận vòng 2 sau:

1. **W0-M3 = P0, trước W0-M2.** Probe phải gọi path/candidate thực, thử candidate kế tiếp và ghi từng candidate +
   error; hai fingerprint giữ actor/environment/time riêng, không suy khả dụng toàn kho.
2. **W0-M4 = P0.** Chấp nhận chẩn đoán wall-clock vs Windows standby của vòng 2 và cách sửa chờ lát cắt + so lại
   `_bay_gio()`; thêm phản chứng clock jump và monotonic evidence. Không cần packet dò trước.
3. **F2/F4/F6/F7** nhận như đã hội tụ.
4. **F3** dùng hai Packet nhỏ:
   - W0-R2: nâng `review_delivery_receipt`, validator/cổng hiện có, compatibility và anchor declaration;
   - W0-R3: `packet_loop` chỉ nhận receipt ID/hash + identity đã validate; không có raw schema song song.
5. **F5:** W1-S1 sau W1-P1 + W0-R3, đồng bộ adapter mỏng; bootstrap trước đó dùng skill hiện tại và khai
   transport caveat.

## Thứ tự Codex đề nghị

Hai seam serial, chạy song song tối đa hai writer:

```text
launcher lane: W0-M3(P0) → W0-M4(P0) → W0-M1(P0) → W0-M2(P1)
review lane  : W0-R1(P0) → W0-R2(P1) → W0-R3(P1)
independent  : W0-C1(P1) lấy slot đầu tiên an toàn sau một lane đóng/yield, nếu Codex executor budget cho phép
```

Lý do: M3 mở lane Codex thật; M4 làm deadline có nghĩa trước agent run dài; M1 sửa lời khai pass/skip; M2 làm sạch
encoding. Không preempt writer đang chạy. Rework được slot kế tiếp theo tie-break đã thống nhất.

## Path/prefix dự kiến để Packet Spec đóng băng

Đây là proposed path, không khẳng định tệp đã có:

```text
W0-C1  planned:.claude/dev/review_connector.py
       planned:.claude/dev/review_connector_test.py
W0-R2  ops/lease_publish.py
       ops/lease_publish_test.py
       planned:.github/coordination/schemas/review_delivery_receipt.v2.schema.json
W0-R3  .claude/dev/packet_loop.py
       .claude/dev/packet_loop_test.py
W1-P1  .claude/dev/launcher.py
       .claude/dev/launcher_test.py
       planned:.github/coordination/schemas/review_verdict.v1.schema.json
W1-G1  planned:.claude/dev/gate_lifecycle.py
       planned:.claude/dev/gate_lifecycle_test.py
W1-G2  .claude/dev/gate_lifecycle_test.py
W1-C2a .claude/dev/review_connector.py
       .claude/dev/review_connector_test.py
W1-C2b planned:.github/workflows/review-connector-shadow.yml
W1-S1  .claude/skills/cross-review/SKILL.md
```

W0-M3/M4/M1/M2 đều dùng `.claude/dev/launcher.py`/`launcher_test.py` theo đúng Packet; write set cụ thể được đóng
băng ở Issue. W1-G2 không sửa production gate; mutation tạo temp copy từ production và runner nằm trong test file.

## Bộ chỉnh sửa trong khung đề nghị người dùng duyệt một lần

A. Sửa fingerprint + thêm W0-M3/W0-M4 và đổi hàng đợi M1.
B. Sửa §7.4a/§7.5 theo state order chạy được.
C. Tách review/executor call counters.
D. Tái dùng receipt hiện có qua W0-R2/R3, khai anchor strength; không bắt tag tuyệt đối.
E. Thêm W1-S1 và đánh dấu command target-after-W1-S1 ngay tại code block.
F. Pin `planned:` path/prefix và thêm tie-break/rework next-slot.
G. Khai L9 skipped trong evidence dossier.

## Yêu cầu kết luận

1. Cho verdict `AGREE | AGREE_WITH_CHANGE | DISAGREE` với thứ tự, path map và bundle A–G.
2. Kiểm xem W0-M3/M4/M1/M2 serial lane có bỏ lỡ dependency hoặc sửa quá nhiều không.
3. Nêu tối đa 3 chỉnh sửa cuối nếu thật sự cần; đừng mở scope mới nếu không có phản chứng.
4. Kết thúc bằng:
   - `JOINT_RECOMMENDATION`
   - `REMAINING_DISSENT`
   - `OWNER_DECISIONS` — chỉ thay đổi 9 điểm khung hoặc lựa chọn sản phẩm thực sự, không liệt kê việc sửa docs.

Không sửa file.
