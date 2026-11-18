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

1. **Phép so sánh khi `accept`.** Biên nhận nộp (`supplied`) và biên nhận thu lại (`collected`) phải trùng đúng từng giá trị ở các khoá bất biến sau:
   - `schema`, `repo_id`, `repo`, `head`;
   - `audit_comment_id`, `audit_updated_at`, `audit_sha256`;
   - `query_scope`, `ref_scope`, `event_scope`;
   - `dag_coverage`, `earliest`, `residual_classes`, `status`.
2. **`cursor_coverage`.** So tập khoá, không so số trang. Tập khoá của `supplied["cursor_coverage"]` và `collected["cursor_coverage"]` phải trùng nhau và trùng `set(query_scope)`. Mỗi giá trị phải là số nguyên ≥ 1. Thiếu một họ, thừa một họ, hoặc có giá trị không hợp lệ thì phải từ chối.
3. **Bỏ khỏi phép so sánh:** `raw_snapshot_sha256`, `started_utc`, `ended_utc`.
   - `_1174_collector_receipt` vẫn phải kiểm định dạng `raw_snapshot_sha256` của cả hai biên nhận như hiện nay.
   - Không khoá nào khác của `_1174_COLLECTOR_KEYS` được bỏ.
4. **Điều kiện giữ nguyên, không nới:**
   - `collected["status"] != "FAIL"`, nếu sai thì `publication evidence FAIL`;
   - `collected["status"] == "RECORDED_EARLIEST_MATCH"`;
   - `collected["dag_coverage"] is True`;
   - `collected["earliest"] is not None`;
   - mọi kiểm tra snapshot audit/comment trước và sau khi thu;
   - deadline `collection_end`;
   - thông báo lỗi hiện có.
   Không thay đổi `_1174_collect`, `_1174_collector_receipt`, `_1174_COLLECTOR_KEYS`, schema receipt v2, hay bất kỳ đường `accept`/human/gate nào khác.
5. **Ca kiểm bắt buộc.** Đăng ký vào inventory WP1174, giữ nhất quán các literal đếm.
   - `wp1174_activity_accept_snapshot_drift`. Dựng hai biên nhận chỉ khác `raw_snapshot_sha256` và số trang `cursor_coverage` (cùng tập họ). Chạy đường `accept` thật trên fixture như các ca `accept_roundtrip` hiện có. Kết quả phải được chấp nhận.
   - Các ca con phải bị từ chối với `publication evidence UNKNOWN/FAIL`, mỗi ca khác đúng một thứ:
     - `earliest` (id khác, hoặc time khác);
     - tập họ `cursor_coverage` (thiếu một họ);
     - giá trị `cursor_coverage` bằng 0;
     - `status`;
     - `dag_coverage`;
     - `residual_classes`;
     - `audit_sha256`.
   - Có một ca đối chứng: `collected` FAIL vẫn cho `publication evidence FAIL`.
6. **Mutant bắt buộc.** Mỗi mutant phải làm ca đích đỏ đúng ở assertion của chính ca đó.
   - `m1393_compare_raw_snapshot`: khôi phục việc so `raw_snapshot_sha256`.
   - `m1393_compare_cursor_counts`: so số trang `cursor_coverage`.
   - `m1393_drop_earliest`: bỏ `earliest` khỏi phép so.
   - `m1393_cursor_family_unchecked`: không kiểm tập họ của `cursor_coverage`.
7. **Không hồi quy.**
   - Mọi ca `wp1174_activity_*`, `wp1174_lifecycle*`, `wp1174_writer_accept` và `wp1174_race_accept` giữ nguyên ID và xanh.
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
