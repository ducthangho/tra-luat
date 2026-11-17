# wp1370 r1 — bằng chứng publication qua Repository Activity API (PUBLICATION-ACTIVITY-API)
packet_id: wp1370
revision: 1

Trạng thái: đặc tả đóng băng cho Packet #1370, Mission #1172 revision 61 (https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-6945156953). Quyết định chủ kho: https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-6945148714 .

## Vấn đề (đo được 17/11/2026)

`accept` của WP1174 cần biên nhận `wp1174_publication_receipt` do `_1174_collect` (`.claude/dev/packet_loop.py`) dựng: bằng chứng rằng exact head H được đưa lên server lần đầu SAU khi chủ kho sửa comment audit lần cuối (`audit.updated_at`). Khi `accept`, mã canonical thu thập lại và so khớp với biên nhận do bên gọi nộp.

Nguồn hiện tại là `GET repos/<kho>/events`. Trên kho này nó không bao giờ cho ra `RECORDED_EARLIEST_MATCH`:

1. Payload `PullRequestEvent` đã bị GitHub rút gọn: `pull_request` chỉ còn `url, id, number, head{ref,sha}, base{ref,sha,repo{id,url,name}}`; không còn `html_url` và `base.repo.full_name`. Chốt `collector PR event identity` vì thế ném lỗi với mọi event `opened`. Ngoài ra action `merged` không nằm trong tập action, nên đặt `dag=False`.
2. Mọi `CreateEvent` đều đặt `dag=False`, mà agent tạo nhánh liên tục: 16 `CreateEvent` trong 300 event.
3. Events API thiếu PushEvent. 300 event giữ lại phủ 14/11 02:04Z tới 17/11 10:15Z nhưng không có PushEvent nào của ngày 17/11, kể cả lần push H `226bba5` của WP1308 g7 lúc 09:32:46Z.

`GET repos/<kho>/activity` (Repository activities API) thì ghi đủ: 9174 bản ghi trong 92 trang, từ 2026-07-05 tới nay, xếp từ mới tới cũ. Các khoá `id, node_id, activity_type, ref, before, after, timestamp, actor`. Các loại `push`, `force_push`, `branch_creation`, `branch_deletion`, `pr_merge`. Phân trang bằng cursor `after=` trong header `Link`; lưu ý URL trang sau dạng `/repositories/<id>/activity…`. Ví dụ đo được: `09:32:46Z push refs/heads/ops/wp1308-target-r5-g7 60c6f40 -> 226bba5` và `06:37:08Z branch_creation … 0000…0000 -> 60c6f40`.

## Hợp đồng

Ký hiệu: A = `audit.updated_at`; "X chứa H" nghĩa là `git merge-base --is-ancestor H X` trả 0 (H là tổ tiên hoặc bằng X). Mọi phép xét "chứa H" chạy trên object cục bộ đã có; không xác định được thì là KHÔNG ĐO ĐƯỢC.

1. **Nguồn bằng chứng.** Họ `events` trong phạm vi thu thập được thay bằng Repository activities API của đúng kho `_1174_REPO`. Các họ `git/matching-refs/heads`, `git/matching-refs/tags`, `pulls?state=all` giữ nguyên vai trò. `_1174_collect` không còn đọc Events API.
2. **Phủ toàn bộ lịch sử, có mốc neo độc lập** (sửa F1 của spec review lượt 1).
   - Đọc **toàn bộ** feed activity theo cursor tới khi hết trang; không dừng sớm ở mốc audit.
   - Chỉ coi là phủ đủ khi đồng thời: (a) không còn cursor trang sau; (b) bản ghi cũ nhất là `branch_creation` của nhánh mặc định (`default_branch` đọc từ `GET repos/<kho>`) với `before` toàn số 0; (c) `timestamp` của bản ghi đó không sớm hơn `created_at` của kho; (d) không bản ghi nào trước nó. Thiếu bất kỳ điều kiện nào thì `UNKNOWN`. Feed hết trang **không** tự nó chứng minh lịch sử đầy đủ.
   - Thứ tự: dữ liệu từ mới tới cũ. Bản ghi cùng `timestamp` xét như nhau, không bản ghi nào được dùng làm điểm dừng.
   - Cursor phải neo đúng kho: chỉ nhận trang sau thuộc `repos/<kho>/activity` hoặc `repositories/<repo_id>/activity` với đúng `repo_id` đã đo. Nếu mã cần đọc header `Link` hoặc dùng đường `repositories/<repo_id>`, chỉ mở rộng tối thiểu đúng hai dạng ấy, có kiểm danh tính; không nới phạm vi endpoint nào khác của `_1174_api`.
   - Trần mới cho riêng bộ thu thập: ≤1000 trang tổng mọi họ, ≤64 MB, ≤900 s tổng, cộng deadline của người gọi. Trần ở `_1174_human_evidence` (`collection_end`) được nâng tương ứng, vẫn bị chặn bởi hạn của admission. Chạm trần thì `UNKNOWN`, không bao giờ cho ra kết quả rút gọn.
3. **Object đầy đủ.** Mọi OID khác số 0 xuất hiện trong `before`/`after` của feed phải có mặt cục bộ trước khi xét. OID thiếu được tải bằng **một** lệnh fetch theo SHA (GitHub cho tải commit không còn ref theo SHA; đo 17/11: 3/3 mẫu tải được). Fetch vào kho của bộ thu thập, **không** tạo hay đổi ref nào. Còn OID nào không tải được thì `UNKNOWN`.
4. **Kiểm danh tính từng bản ghi.** `id` là số nguyên dương. `activity_type` thuộc đúng `push`, `force_push`, `branch_creation`, `branch_deletion`, `pr_merge`; loại lạ thì `UNKNOWN`. `ref` có dạng `refs/heads/…` hoặc `refs/tags/…` hợp lệ với `git check-ref-format`. `before`/`after` là OID 40 hex. `timestamp` đọc được và không muộn hơn lúc bắt đầu thu thập. Bản ghi sai kiểu thì ném lỗi `UNKNOWN`, không bỏ qua im lặng.
5. **Introduction và ảnh trước** (sửa F2). Với mỗi bản ghi:
   - **Introduction:** `after` khác 0, chứa H, và loại là `push`/`force_push`/`branch_creation`/`pr_merge`.
   - **Quan sát ảnh trước:** `before` khác 0 và chứa H, với mọi loại, kể cả `branch_deletion` và `force_push`.
     - Có `timestamp` ≤ A thì là bằng chứng H đã lộ trước audit: `FAIL`.
     - Có `timestamp` > A thì phải tồn tại một introduction **sớm hơn hẳn** có `after` đúng bằng `before` này; nếu không thì `UNKNOWN`.
     - `branch_deletion` không bao giờ là introduction.
   - Không xác định được quan hệ chứa thì `UNKNOWN`.
6. **PR** (sửa F3).
   - Mọi PR trong `pulls?state=all` có `head.repo` thiếu hoặc khác đúng kho này thì `UNKNOWN`: lịch sử head của PR từ fork không định ngày được. Đo 17/11: 0/929 PR như vậy.
   - Với PR cùng kho, mọi lần head đổi đều là activity trên nhánh head, nên được phủ bởi mục 5. Không dùng `created_at` của PR để định ngày head.
7. **DAG trên ref và PR hiện tại.** Như cũ: mọi head, tag và head PR hiện đang chứa H phải có một introduction có `after` đúng bằng tip đó; nếu không thì `UNKNOWN`.
8. **Kết luận.**
   - `FAIL` nếu có introduction hoặc quan sát ảnh trước chứa H với `timestamp` ≤ A.
   - `RECORDED_EARLIEST_MATCH` chỉ khi đồng thời: phủ đủ theo mục 2, object đủ theo mục 3, không có `UNKNOWN` nào từ mục 4–7, và có ít nhất một introduction.
   - Mọi trường hợp còn lại là `UNKNOWN`.
   - `earliest` là introduction sớm nhất theo `timestamp` rồi `id`, với các trường `id` (dạng `str`), `time`, `ref`, `actor`, `before`, `after`.
9. **Biên nhận.** Schema `wp1174_publication_receipt.v2`, cùng tập khoá với v1, chỉ khác giá trị:
   - `query_scope` = `["activity", "git/matching-refs/heads", "git/matching-refs/tags", "pulls?state=all"]`;
   - `event_scope` = `"repository_activity"`.
   `_1174_collector_receipt` chỉ nhận v2. Phép so khi `accept` (thu thập lại rồi so mọi khoá trừ `started_utc`, `ended_utc`) giữ nguyên. `residual_classes` giữ nguyên.
10. **Không đổi:** các chốt khác của `accept` và `_1174_human_evidence` (trừ trần thời gian ở mục 2); `_owner_record`; `kiem-merge`; mọi cổng; danh sách thẩm quyền.

## Bằng chứng bắt buộc (`.claude/dev/packet_loop_test.py`) — sửa F4

- **Đặt tên.** Mọi ca mới đặt tên `wp1174_activity_*` và mọi mutant mới đặt tên `m1174_activity_*`. Nhờ đó chúng hưởng nguyên các chốt sẵn có của harness: ca `wp1174_*` bị skip thì đỏ, `_required1174`, mutant `m1174_*` thiếu ca đích hoặc đối chứng thì đỏ, mutant bị skip thì đỏ. Ca mới được thêm vào tập bắt buộc mà `_WP1174_MAIN_REQUIRED` đọc, nếu tập đó liệt kê theo ID. Không đổi cách xử lý ca phụ thuộc nền đã có.
- **Chuyển fixture.** Mọi ca hiện có dùng họ `events` cho `_1174_collect` phải chuyển sang fixture activity tương đương, giữ đúng ý định và giữ nguyên ID. Mỗi phép kiểm con gốc (gồm các ca PR trước audit và PR sau audit không được giải thích) phải có ánh xạ tường minh sang phép kiểm activity tương ứng, ghi trong chú thích của ca. Không được thay "PR opened" bằng "PR merged" chỉ để giữ ID.
- **Ca mới**, mỗi ca có oracle trạng thái chính xác:
  - payload thật rút gọn, dựng từ đúng các khoá đo được, không làm ném lỗi;
  - phân trang nhiều trang, phủ tới mốc neo, cho `RECORDED_EARLIEST_MATCH`;
  - lần publish H cũ hơn nằm **ở trang sau** một bản ghi trước audit không liên quan, cho `FAIL`;
  - như trên nhưng bản ghi biên cùng `timestamp`, cũng cho `FAIL`;
  - force-push trước audit có `before` chứa H, rồi publish lại sau audit, cho `FAIL`;
  - `branch_deletion` có `before` chứa H trước audit, cho `FAIL`; xoá nhánh khác đã được giải thích đầy đủ vẫn cho `RECORDED_EARLIEST_MATCH` (đối chứng);
  - không có mốc neo `branch_creation` của nhánh mặc định, cho `UNKNOWN`;
  - OID không tải được, cho `UNKNOWN`;
  - cursor trỏ sang kho khác, cho `UNKNOWN`;
  - PR có head repo khác, cho `UNKNOWN`;
  - `force_push` hoặc `pr_merge` làm introduction sau audit, cho `RECORDED_EARLIEST_MATCH`;
  - biên nhận v1 bị `_1174_collector_receipt` từ chối;
  - vòng v2 đầy đủ qua `accept`/guard: biên nhận khớp thì đạt, đổi một khoá bất biến thì bị từ chối.
- **Đột biến:** ít nhất năm mutant `m1174_activity_*`, mỗi cái có ca đích và đối chứng khác họ:
  - dừng đọc ở bản ghi biên audit đầu tiên;
  - bỏ yêu cầu mốc neo của mục 2;
  - bỏ xét ảnh trước của mục 5;
  - coi ảnh trước của `branch_deletion` như introduction hợp lệ, với counterexample chuyên dụng: một nhánh chứa H bị xoá trước audit vẫn ra pass;
  - bỏ kiểm kho của cursor.
  Mỗi mutant phải làm ca đích đỏ vì assertion của chính ca đó, còn ca dương trên bytes chưa đột biến thì xanh.
- Ruff F delta so với master = 0. `tl.py --selftest` N/N trước push.

## Quy trình và quyền

Lease `wp1370-r1-g1-claude`: executor Claude (`claude-fable-5-2`), reviewer Codex (`gpt-6-astra`). Spec review và source review do Codex làm. Audit H là `owner_delegated_audit` theo https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-6916538696 . Chỉ push sau khi review approve định dạng K4 trên đúng H. Sau đó draft PR, CI PR Ubuntu, connector, full M9, `kiem-merge` K0–K7. Merge do chủ kho bấm. Windows CI miễn theo https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-6916597687; K6 cần lượt Windows tập trung hoặc dòng miễn có bằng chứng.

Không target G5, LIVE hay installation. `accept` của WP1308 chạy ở generation riêng sau khi gói này land.
