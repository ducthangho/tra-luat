# K3-CONNECTOR-STATE-V1 r2 — K3 của kiem-merge đọc comment tóm tắt `codex-review-state:v1`

- packet_id: K3-CONNECTOR-STATE-V1
- revision: 2
- Thay r1 (sha256 26e9697e…288a, @6eb1163): r1 coi `null` ở hai cờ là sai kiểu, nhưng connector dùng đúng `null` khi
  `status` là `"running"` (đo trên PR #1286, issuecomment-6722995278, 14:54:58Z). r2 sửa B2(e)/(g) và thêm ca C2.
- Issue: #1288 · tracker #1206
- Chủ kho duyệt mở packet ngày 2026-11-08 (phiên điều phối session_015GtxrYPjZCTZeRiazdssgq).
- Executor: Google Antigravity CLI `agy`, model `gemini-4-argon-high`. Reviewer: Codex.

## 1. Vấn đề

Connector `chatgpt-codex-connector[bot]` không còn đăng kết luận sạch dạng `**Reviewed commit:** \`<sha>\``.
Nay nó giữ MỘT issue comment tóm tắt và sửa nó tại chỗ mỗi lượt. Thân comment có dòng:

```
<!-- codex-review-state:v1 {"code_review":{"commit_sha":"<sha>","has_any_findings":false,"has_unresolved_findings":false,"status":"completed"},"security_review":{"commit_sha":null,"has_any_findings":null,"has_unresolved_findings":null,"status":null}} -->
```

`_neo_connector` trong `.claude/dev/packet_loop.py` chỉ đọc `Reviewed commit:`, nên trả `None` cho comment này.
Vì vậy `_doc_connector` báo `connector chưa xong trên <head>` (K3 THIẾU), dù connector đã xong và sạch.

Ca thật: PR #1270, head `5824094e78a0afe9d0af8866df45c50b24334767`, issuecomment-6721722576. Thân comment
nguyên văn được lưu ở `ops/land/pr1270-wp1179-provenance/readback-connector-issuecomment-6721722576.json`
(nằm trên master sau khi PR land #1286 merge; nếu chưa thì lấy ở nhánh `ops/land-1179`).

## 2. Hành vi phải có

Marker được nhận diện bằng regex
`<!--\s*codex-review-state:v1\s+(\{.*?\})\s*-->` (DOTALL), chỉ trong issue comment có `user.login == BOT_CONNECTOR`.
Quy ước về kết quả của `_neo_connector`: `"hien"` là kết luận trên head; `"cu"` là neo một head khác hợp lệ;
`"hong"` là thiếu, sai hoặc mơ hồ, và làm gate dừng; `None` là không có khai báo.

B1. Comment không có marker: hành vi giữ nguyên từng byte như hiện tại.

B2. Có marker thì:
- (a) Có NHIỀU HƠN một marker ⇒ `"hong"`.
- (b) JSON không parse được, không phải object, hoặc `code_review` không phải object ⇒ `"hong"`.
- (c) `code_review.commit_sha` không phải chuỗi khớp `SHA_RE` (40 hex thường) ⇒ `"hong"`.
  KHÔNG nhận tiền tố, chữ hoa hay khoảng trắng.
- (d) `commit_sha != head` ⇒ `"cu"`.
- (e) `commit_sha == head` thì kiểm kiểu như sau. Sai kiểu ⇒ `"hong"`.
  - `status` phải là chuỗi.
  - Khi `status == "completed"`: hai cờ phải là `bool` THẬT. `0`, `1`, `"false"` hay `null` đều là sai kiểu.
  - Khi `status != "completed"` (ví dụ `"running"`): mỗi cờ là `bool` hoặc `null`. Kiểu khác là sai kiểu.
- (f) `commit_sha == head`, đúng kiểu, `status == "completed"`, cả hai cờ đều `False` ⇒ kết luận SẠCH trên head.
  Kết luận này đếm như `"hien"` cho điều kiện "connector đã xong" ở `_doc_connector`.
- (g) `commit_sha == head`, đúng kiểu, nhưng `status != "completed"` HOẶC một trong hai cờ là `True` ⇒
  KHÔNG phải kết luận sạch.
  - Comment này không được làm connector "xong". Nếu không có bằng chứng xong nào khác, gate báo
    `connector chưa xong` như cũ.
  - Comment này cũng không làm gate dừng kiểu `"hong"`.
  - Executor chọn cách biểu diễn: thêm giá trị trả về mới, hoặc tách hàm. Ràng buộc: mọi chỗ gọi
    `_neo_connector` hiện có vẫn đúng nghĩa, kể cả nhánh `p0p2` của `mo-lai`.
- (h) Comment có CẢ marker LẪN dòng `Reviewed commit:`: hai phía phải cùng kết luận (cùng `hien`, hoặc cùng `cu`).
  Khác nhau ⇒ `"hong"`.

B3. Finding vẫn đọc như cũ:
- Badge `P0`–`P3` nằm ở review và review comment, và luật hạng giữ nguyên.
- Comment tóm tắt không có badge. Nếu nó CÓ badge thì áp đúng luật hiện hành cho issue comment.
- Phần `security_review` được BỎ QUA hoàn toàn.

B4. Phần `biet` (tập SHA đã biết) giữ nguyên. Việc SHA 40 hex trong marker lọt vào `biet` qua regex sẵn có là chấp nhận được.

B5. `has_unresolved_findings == True` trên head KHÔNG được đọc thành sạch, kể cả khi `has_any_findings == False`.
Đây là chốt đóng-thất-bại.

## 3. Kiểm (bắt buộc, mỗi mục một ca `k3s_…` trong `packet_loop_test.py`)

C1. Ca dương: comment tóm tắt hợp lệ trên head, không có review hay `Reviewed commit:` nào ⇒ `kiem-merge` qua được
K3. Dựng fixture từ đúng thân comment 6721722576, chỉ thay `commit_sha` bằng head của fixture.

C2. Mỗi nhánh B2(a)–(h) và B5 có ít nhất một ca. Bắt buộc có ca `status: "running"` với hai cờ `null` trên head
(mẫu thật: PR #1286 issuecomment-6722995278 lúc running). Ca này phải ra "chưa xong", KHÔNG ra `"hong"`. Ca nào cũng phải khẳng định THÔNG ĐIỆP hoặc mã cụ thể,
không chỉ `rc != 0`. Đây là bài học "ca có MẶT khác ca có ĐO" trong CLAUDE.md.

C3. Hồi quy:
- Mọi ca `r834_*` hiện có và toàn bộ suite giữ nguyên số ca qua, cộng thêm các ca mới.
- Số đếm in ở dòng `SỐ LIỆU` phải khớp `len(CASES)` và `len(MUTANTS)`.

C4. Đột biến: mỗi chốt sau có ít nhất một mục `MUTANTS` riêng, và mỗi mục bị giết bởi đúng ca đích của nó:
- bỏ kiểm `status == "completed"`;
- bỏ kiểm `has_unresolved_findings`;
- nhận tiền tố SHA thay vì đủ 40 hex;
- nhận `0`/`1` như bool;
- bỏ chốt nhiều marker;
- bỏ chốt mâu thuẫn với `Reviewed commit:`.

C5. Phản chứng chạy được: chạy `kiem-merge` của bản vá trên bộ đầu vào thật của PR #1270 ⇒ K3 ĐẠT.
- Bộ đầu vào là các readback trong `ops/land/pr1270-wp1179-provenance/kiem-merge/`.
- Nếu thư mục thiếu tệp nào, dựng lại từ REST GET và ghi rõ nguồn.
- So với `origin/master` trên cùng đầu vào ⇒ K3 THIẾU.
- Hai vế phải dựng trong MỘT lệnh.

C6. `python3 .claude/dev/packet_loop.py doctrine-scan --root .` và `adr-song --root .` đều rc 0.
`python -m ruff check --select F` có delta F so với master bằng 0.

## 4. Trần

- Write set đúng 2 tệp: `.claude/dev/packet_loop.py` và `.claude/dev/packet_loop_test.py`.
- Diff `git diff --numstat origin/master...HEAD`: `packet_loop.py` ≤ 60 dòng thêm, ≤ 10 dòng xoá; tổng ≤ 400 dòng thêm.
- Gọi `agy` thi công tối đa 3 lượt (một lượt đầu, hai lượt vá).
- Codex review tối đa 3 lời gọi, kể cả lượt connector. Gọi offline bằng `launcher.py run` với `--chup-workspace`.
- Vượt bất kỳ trần nào ⇒ Review Rescue Checkpoint (ADR-0037), DỪNG và hỏi chủ kho.

## 5. Ngoài phạm vi

- Sửa `security_review`, reaction 👍 của bot, hoặc `updated_at` của comment.
- Đổi luật K3 với review object hoặc review comment.
- Mọi tệp ngoài write set, kể cả `docs/PROTOCOL_DA_PHIEN.md`.
- Vá các ca, đột biến hay chỗ khác của packet #1174.

## 6. Base và va chạm

- Base là `origin/master` tại lúc cấp lease. Lease chỉ cấp khi lease `wp1174-r17-g14-codex` đã hết hạn hoặc được nhả.
- Nếu #1174 merge trước khi PR này merge: gộp `origin/master` vào nhánh packet, chạy lại C3–C6, và báo xung đột cho
  phiên điều phối thay vì tự giải những đoạn của #1174.

## 7. Windows

Thay đổi chỉ là phân tích chuỗi và JSON, không gọi API riêng của nền nào. Đề xuất Windows `not_required`.
Chủ kho xác nhận bằng dòng `windows: <H> mien` trên PR. Không chạy CI Windows.

## 8. Hoàn tất

- PR merge vào master với `kiem-merge` rc 0, và chính K3 của PR này được đọc bằng bộ phân tích mới.
- Có hồ sơ land và biên bản M8. Lease được nhả.
