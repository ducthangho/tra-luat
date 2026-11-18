# wp1393 r1 — accept so sánh bằng chứng publication theo phần bất biến (ACCEPT-SNAPSHOT-COMPARE)
packet_id: wp1393
revision: 1

Trạng thái: đặc tả đóng băng cho Packet #1393 thuộc Mission #1172 revision 63 (https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-6975953837). Quyết định chủ kho: https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-6975912237 .

## Vấn đề (đo trên máy đích, 18/11/2026)

`_1174_human_evidence` trong `.claude/dev/packet_loop.py` (master `3bdb479`) gọi lại `_1174_collect` khi `accept`. Sau đó nó đòi biên nhận bên gọi nộp và biên nhận vừa thu khớp nhau ở mọi khoá của `_1174_COLLECTOR_KEYS`, trừ `started_utc` và `ended_utc`.

Bộ khoá này gồm:
- `raw_snapshot_sha256`: băm toàn bộ feed Repository Activity, ref, tag và PR;
- `cursor_coverage`: số trang của từng họ.

Cả hai đổi mỗi khi có push vào bất kỳ nhánh nào, hoặc có PR mới, trong khoảng giữa hai lần thu. Feed thêm bản ghi, rồi thêm trang sau mỗi 100 bản ghi.

Với WP1308 g8 (H `6886ebe`, audit 6972844021), đo được:
- Bốn lần thu lúc 09:23, 09:34, 09:45 và 10:06Z cho `status`, `earliest` (id `50810680773`), `dag_coverage` và `cursor_coverage` trùng nhau.
- `raw_snapshot_sha256` khác nhau ở cả bốn lần.
- `accept` trả `publication evidence UNKNOWN/FAIL` dù cả hai lần thu đều là `RECORDED_EARLIEST_MATCH` cho cùng earliest.

Chi tiết ở #1393.

## Hợp đồng

Có hai lớp kiểm, và đặc tả này giữ chúng tách biệt:
- **Lớp hợp lệ** — `_1174_collector_receipt(receipt, head, audit, repo_id)`, KHÔNG đổi. Nó đã từ chối với thông báo riêng: sai `schema`/`repo`/`repo_id`/`head`/audit/`query_scope`/`ref_scope`/`event_scope`/`residual_classes`/định dạng `raw_snapshot_sha256` (`collector receipt closed bindings`); họ `cursor_coverage` ngoài `query_scope` hoặc giá trị không phải int trong 1..1000 (`collector cursor schema`); `earliest` sai dạng (`collector earliest schema`); `status == "RECORDED_EARLIEST_MATCH"` mà thiếu `earliest`, `dag_coverage` khác true, hoặc tập họ khác `query_scope` (`collector success completeness`).
- **Lớp so sánh** — phần cuối `_1174_human_evidence`, đối tượng của packet này.

1. **Validate cả `collected`.** Hiện chỉ `supplied` đi qua `_1174_collector_receipt`. Thêm một lời gọi `_1174_collector_receipt(collected, head, audit, repo["id"])` (hàm không đổi) TRƯỚC phép so sánh; vị trí: sau dòng `collected["status"] != "FAIL"` hoặc trước nó, nhưng `collected` FAIL vẫn phải ra `publication evidence FAIL` (FAIL là trạng thái hợp lệ với validator nên thứ tự nào cũng giữ được điều này — ca đối chứng ở mục 5 khoá lại).
2. **Hàm so sánh thuần.** Tách phép so sánh thành hàm module-level `_1174_receipts_agree(supplied, collected) -> bool`, không I/O, không ném ngoại lệ với dict bất kỳ có đủ khoá (thiếu khoá hoặc sai kiểu ⇒ trả `False`). Nó trả `True` khi và chỉ khi:
   - mọi khoá trong `_1174_RECEIPT_IMMUTABLE_KEYS` (hằng mới, đúng tập: `schema`, `repo_id`, `repo`, `head`, `audit_comment_id`, `audit_updated_at`, `audit_sha256`, `query_scope`, `ref_scope`, `event_scope`, `dag_coverage`, `earliest`, `residual_classes`, `status`) bằng nhau giữa hai biên nhận;
   - `cursor_coverage` của cả hai là dict, `set(supplied["cursor_coverage"]) == set(collected["cursor_coverage"]) == set(supplied["query_scope"])`, và mọi giá trị ở cả hai là `int` (không phải `bool`) ≥ 1. Số trang KHÔNG được so.
   `raw_snapshot_sha256`, `started_utc`, `ended_utc` không được so. Hằng phải thoả `_1174_RECEIPT_IMMUTABLE_KEYS | {"cursor_coverage","raw_snapshot_sha256","started_utc","ended_utc"} == _1174_COLLECTOR_KEYS` — đặt một assert mức module hoặc một ca kiểm, để thêm khoá mới vào receipt mà quên phân loại là ĐỎ.
3. **Điều kiện accept** thay `all(supplied[k] == collected[k] for k in keys)` bằng `_1174_receipts_agree(supplied, collected)`; mọi vế còn lại giữ nguyên: `collected["status"] != "FAIL"` (`publication evidence FAIL`), rồi `collected["status"] == "RECORDED_EARLIEST_MATCH"`, `collected["dag_coverage"] is True`, `collected["earliest"] is not None` (`publication evidence UNKNOWN/FAIL`). Giữ mọi kiểm tra snapshot audit/comment, deadline `collection_end`, thông báo lỗi hiện có. Không đổi `_1174_collect`, `_1174_collector_receipt`, `_1174_COLLECTOR_KEYS`, schema receipt v2, hay đường `accept`/human/gate nào khác.
4. **Không có đường nào mới cho bằng chứng yếu hơn.** Ngoài `raw_snapshot_sha256` và số trang, không vế nào được nới; đặc biệt `earliest` (cả sáu trường), `audit_*`, `status`, `dag_coverage` vẫn phải bằng nhau.

5. **Ca kiểm bắt buộc.** Mọi ca dương phải đòi kết quả DƯƠNG cụ thể (rc=0 + `PASS`, hoặc trạng thái `accepted` đã ghi); UNKNOWN/skipped/not_run không bao giờ thoả một ca dương. Mọi ca âm của đường `accept` phải đòi trạng thái state KHÔNG đổi (state revision và `accepted_sha` như trước).
   a. **Sửa ca hiện có `wp1174_activity_accept_roundtrip`** (giữ ID): hai mục `("raw_snapshot_sha256","0"*64)` và `("cursor_coverage",dict(..., activity=2))` chuyển từ danh sách "phải từ chối" sang dương — `guard-first-publication` rc=0 `PASS`. Mọi ca âm khác của nó giữ nguyên, với đúng thông báo hiện có.
   b. **Ca mới `wp1174_activity_accept_snapshot_drift`** — đường `accept` THẬT (`_accept_entry1174` hoặc tham số mới của nó viết lại tệp `publication_receipt` trước khi gọi `accept`), ba biến thể dương độc lập, mỗi biến thể phải ra trạng thái `accepted` gắn đúng H và audit:
      - `digest_only`: chỉ `raw_snapshot_sha256` khác (hex 64 hợp lệ);
      - `count_only`: chỉ số trang của MỘT họ khác (vẫn int 1..1000, cùng tập họ);
      - `both`: cả hai.
      Kèm một biến thể âm trên cùng đường: `earliest.id` khác ⇒ từ chối `publication evidence UNKNOWN/FAIL`, state không đổi.
   c. **Ca mới `wp1174_receipt_agree_unit`** — gọi thẳng `_1174_receipts_agree` trên hai biên nhận hợp lệ dựng từ fixture:
      - `True` cho: giống hệt; chỉ digest khác; chỉ số trang khác; cả hai; chỉ `started_utc`/`ended_utc` khác.
      - `False` cho, mỗi ca khác đúng một thứ: từng khoá trong `_1174_RECEIPT_IMMUTABLE_KEYS` (14 ca, mỗi ca một giá trị khác hợp kiểu); `cursor_coverage` thiếu một họ ở `supplied`; thiếu một họ ở `collected`; thừa một họ ngoài `query_scope` ở cả hai; giá trị 0; giá trị `True` (bool); giá trị chuỗi; `cursor_coverage` không phải dict; thiếu khoá `cursor_coverage`.
   d. **Ca lớp hợp lệ trên đường accept** (có thể gộp vào b): `supplied` RECORDED với `dag_coverage` false ⇒ `collector success completeness`; `cursor_coverage` một họ = 0 ⇒ `collector cursor schema`; `residual_classes` khác ⇒ `collector receipt closed bindings`. Các ca này đo lớp hợp lệ vẫn đứng trước, KHÔNG được ghi là đo phép so sánh.
   e. **Đối chứng FAIL:** `collected` FAIL vẫn cho `publication evidence FAIL` (ca hiện có trong `accept_roundtrip` giữ nguyên là đủ, miễn còn xanh).
   f. **Ca validate `collected`:** một fixture mà `_1174_collect` (qua seam) trả biên nhận RECORDED hỏng lớp hợp lệ (vd. `residual_classes` lệch) phải bị từ chối với thông báo của validator — chứng minh lời gọi ở mục 1 có thật.
   Đăng ký mọi ca mới vào inventory WP1174, giữ nhất quán các literal đếm.

6. **Mutant bắt buộc** — mỗi mutant phải làm ca đích ĐỎ đúng ở assertion của chính ca đó (không phải lỗi dựng fixture, không phải ca khác); và ca đích phải XANH trên mã chưa đột biến.
   - `m1393_compare_raw_snapshot` (so lại `raw_snapshot_sha256` trong `_1174_receipts_agree`) ⇒ đích: `digest_only` của 5b và các vế digest của 5c.
   - `m1393_compare_cursor_counts` (so giá trị `cursor_coverage`) ⇒ đích: `count_only` của 5b và vế số trang của 5c.
   - `m1393_drop_earliest` (bỏ `earliest` khỏi `_1174_RECEIPT_IMMUTABLE_KEYS`) ⇒ đích: 5c (vế `earliest`) và biến thể âm của 5b.
   - `m1393_cursor_family_unchecked` (bỏ phép so tập họ trong `_1174_receipts_agree`) ⇒ đích: 5c (các vế thiếu/thừa họ). Ở đường accept, validator che phần này; đích đơn vị là đích đúng, không cần mutant ghép.
   - `m1393_collected_unvalidated` (bỏ lời gọi validate `collected` ở mục 1) ⇒ đích: 5f.

7. **Không hồi quy.**
   - Mọi ca `wp1174_activity_*`, `wp1174_lifecycle*`, `wp1174_writer_accept`, `wp1174_race_accept` giữ nguyên ID và xanh (riêng `accept_roundtrip` theo 5a).
   - Kiểm kê anchor: mọi product mutant đã đăng ký khớp đúng một lần.
   - Ruff F delta so base bằng 0.

## Write set

- `.claude/dev/packet_loop.py`
- `.claude/dev/packet_loop_test.py`

## Quy trình và quyền

Lease `wp1393-r1-g1-claude`: executor Claude (`claude-fable-5-2`), reviewer Codex (`gpt-6-astra`).
- Spec review và source review do Codex làm.
- Audit H là `owner_delegated_audit` theo https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-6916538696 .
- Chỉ push sau khi review approve, định dạng K4, trên đúng H.
- Sau push: draft PR, CI PR Ubuntu, connector, `kiem-merge` K0–K7. Merge do chủ kho bấm.
- Windows CI, full M9 và K6 Windows tập trung được miễn như #1370 (https://github.com/ducthangho/tra-luat/issues/1370#issuecomment-6945530872). Lý do: write set và loại thay đổi giống hệt #1370.
- Không target G5, LIVE hay installation. `accept` của WP1308 chạy ở generation riêng (g9) sau khi packet này land.
