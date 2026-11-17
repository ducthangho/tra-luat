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

1. **Nguồn bằng chứng.** Họ `events` trong phạm vi thu thập được thay bằng Repository activities API của đúng kho `_1174_REPO`. Các họ `git/matching-refs/heads`, `git/matching-refs/tags`, `pulls?state=all` giữ nguyên vai trò. Không còn đọc Events API trong `_1174_collect`.
2. **Phân trang và phủ.** Đọc activity từ mới tới cũ theo cursor, đúng kho, trong các trần hiện có (≤100 trang tổng, ≤120 s mỗi lượt, ≤180 s tổng, ≤30 MB, deadline của người gọi). Dừng khi gặp bản ghi có `timestamp` ≤ `audit.updated_at` (đã chạm biên), hoặc khi hết trang. Hết trang mà không chạm biên thì chỉ coi là phủ đủ nếu bản ghi cũ nhất là sự kiện tạo kho hoặc không còn trang nào; trường hợp mơ hồ là `UNKNOWN`. Cursor phải neo đúng kho: chỉ nhận đường `repos/<kho>/activity` hoặc `repositories/<repo_id>/activity` với đúng `repo_id` đã đo; mọi kho/đường khác làm cả lượt `UNKNOWN`. `_1174_api` chỉ nhận endpoint `repos/<kho>…`, nên nếu cần đường `repositories/<id>` hoặc cần đọc header `Link`, author mở rộng tối thiểu và có kiểm, không nới phạm vi endpoint nào khác.
3. **Kiểm danh tính từng bản ghi.** `id` số nguyên dương, `activity_type` thuộc đúng 5 loại trên, `ref` dạng `refs/heads/…` hoặc `refs/tags/…` hợp lệ với `git check-ref-format`, `before`/`after` là OID 40 hex, `timestamp` đọc được và không muộn hơn lúc bắt đầu thu thập. Bản ghi sai kiểu thì ném lỗi `UNKNOWN`, không bỏ qua im lặng. Loại activity lạ thì `dag=False`.
4. **Introduction.** Một activity là introduction của H khi `after` khác toàn số 0, commit có trong kho cục bộ, và `git merge-base --is-ancestor H after` cho kết quả là tổ tiên. Áp cho cả `push`, `force_push`, `branch_creation` và `pr_merge`. Không xác định được quan hệ (commit thiếu, lỗi git) thì `dag=False`. `branch_deletion` không phải introduction.
5. **Kết luận.** Giữ ba trạng thái và đúng thứ tự cũ:
   - `FAIL` nếu có introduction nào có `timestamp` ≤ `audit.updated_at`;
   - `RECORDED_EARLIEST_MATCH` chỉ khi lượt đầy đủ, đã chạm biên, `dag=True` và có ít nhất một introduction;
   - còn lại là `UNKNOWN`.
   `earliest` là introduction sớm nhất (theo `timestamp`, rồi `id`), với các trường `id, time, ref, actor, before, after`, dùng `str(id)`.
6. **DAG trên ref và PR hiện tại.** Như cũ: mọi head trong `git/matching-refs/heads`, mọi tag và mọi PR (`pulls?state=all`, head sha) đang chứa H phải có một introduction mà `after` đúng bằng tip đó; nếu không thì `dag=False`.
7. **Biên nhận.** Schema mới `wp1174_publication_receipt.v2`. Cùng tập khoá với v1, chỉ khác giá trị: `query_scope` = `["activity", "git/matching-refs/heads", "git/matching-refs/tags", "pulls?state=all"]`, `event_scope` = `"repository_activity"`. `_1174_collector_receipt` chỉ nhận v2. Phép so khi `accept` (thu thập lại rồi so mọi khoá trừ `started_utc` và `ended_utc`) giữ nguyên. `residual_classes` giữ nguyên.
8. **Không đổi:** các chốt khác của `accept` và `_1174_human_evidence`; `_owner_record`; `kiem-merge`; mọi cổng; danh sách thẩm quyền.

## Bằng chứng bắt buộc (`.claude/dev/packet_loop_test.py`)

- **Cập nhật fixture.** Các ca hiện có đang dùng họ `events` cho `_1174_collect` phải chuyển sang fixture activity tương đương. Ý định của từng ca phải giữ nguyên: thành công, FAIL trước audit, UNKNOWN khi thiếu phủ, deadline, sai danh tính, ref/PR không được giải thích. Không được xoá ID ca nào.
- **Ca mới `wp1370_*`**, mỗi ca neo vào assertion của chính nó:
  - payload thật rút gọn được bỏ qua đúng cách, không ném lỗi; dựng từ đúng các khoá đo được trong mục Vấn đề;
  - phân trang qua cursor nhiều trang, dừng ở biên audit;
  - push trước audit cho `FAIL`;
  - không chạm biên cho `UNKNOWN`;
  - cursor trỏ sang kho khác cho `UNKNOWN`;
  - `force_push` và `pr_merge` được tính là introduction;
  - có `branch_creation`/`branch_deletion` của nhánh khác mà vẫn `RECORDED_EARLIEST_MATCH`;
  - biên nhận v1 bị từ chối.
- **Đột biến:** ít nhất bốn mutant đăng ký trong `MUTANTS`, mỗi cái có ca đích riêng:
  - bỏ kiểm biên audit (`FAIL` thành pass);
  - bỏ kiểm kho của cursor;
  - bỏ yêu cầu chạm biên phủ;
  - coi `branch_deletion` là introduction.
- Ruff F delta so với master = 0. `tl.py --selftest` N/N trước push.

## Quy trình và quyền

Lease `wp1370-r1-g1-claude`: executor Claude (`claude-fable-5-2`), reviewer Codex (`gpt-6-astra`). Spec review và source review do Codex làm. Audit H là `owner_delegated_audit` theo https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-6916538696 . Chỉ push sau khi review approve định dạng K4 trên đúng H. Sau đó draft PR, CI PR Ubuntu, connector, full M9, `kiem-merge` K0–K7. Merge do chủ kho bấm. Windows CI miễn theo https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-6916597687; K6 cần lượt Windows tập trung hoặc dòng miễn có bằng chứng.

Không target G5, LIVE hay installation. `accept` của WP1308 chạy ở generation riêng sau khi gói này land.
