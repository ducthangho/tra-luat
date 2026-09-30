# ĐẶC TẢ — `LEASE-ID-EP-KIEU-YAML` — **revision 6, ĐÓNG BĂNG**

| trường | giá trị |
|---|---|
| `schema_version` | 1 (protocol §3.2) |
| `packet_id` | `wp678` (ID bền theo protocol §3.2, `wp<issue>`); tên đọc được: `LEASE-ID-EP-KIEU-YAML`. Hai tên chỉ cùng một packet; lease dùng `wp678` hoặc tên đọc được đều phải kèm `packet_issue: 678`. |
| `revision` | **6** |
| `thay_the_cho` | revision 5: `ops/specs/lease-id-ep-kieu-yaml-r5.md`, sha256 `cbf9c8380f0da45e2af07034cc6715b75c8ac2deb36a4967497b94d1a9394150`, commit `00d2ee3`. Chuỗi lịch sử: revision 4 `ops/specs/lease-id-ep-kieu-yaml-r4.md`, sha256 `2726d59ffb683f44e68c1409241250c40025bc02a9c9bfb257e767831a1e17f2`, commit `a9019a9`; revision 3 `ops/specs/lease-id-ep-kieu-yaml-r3.md`, sha256 `64c67225335cf50b2a394ffda005e03d338ff545757b210640fd05ac14564af1`, commit `4c1915c`; revision 2 `ops/specs/lease-id-ep-kieu-yaml-r2.md`, sha256 `1575fb3e605b88e94d29e704789dcbaecbbcc3fb25e5c963796655b4d55d5715`, commit `aecdccd`; revision 1 `ops/specs/lease-id-ep-kieu-yaml-r1.md`, sha256 `578916a9b04965b178e5dcaf949c725771129d0cb4d4e13f216adb5056d5fa7c`, commit `342e62c7`. |
| `packet_issue` | **#678** |
| `mission_issue` | **#682** (Mission Issue, object ID `5627190292`, tạo 29-09-2026, tiêu đề *"Mission wp678: quyết định chủ kho + miễn trừ closure có phạm vi cho LEASE-ID-EP-KIEU-YAML"*). Issue này do **phiên agent đăng HỘ chủ kho** bằng credential chủ kho, nên `author_association: OWNER` không chứng minh chủ kho tự gõ; nguồn thẩm quyền là các câu trả lời của chủ kho trong phiên (Q0–Q6) được trích trong thân #682; Q7 do chủ kho chốt sau đó và ghi ở #682 comment `5888143430`; Q8 ở #682 comment `5888631719`; Q9 ở #682 comment `5888660607` (xem §3). Packet cha #579 (đặc tả `ops/specs/dang-lease-dau-truoc-kiem-sau-r30.md`) không khai `mission_issue` và không cấp ngoại lệ gì cho packet này. |
| `nguon_cap_viec` | Phát hiện phụ của #677 (mục *"Phát hiện phụ — TÁCH packet riêng"*). Chủ kho quyết định tách packet 29-09-2026, rồi trả lời *"Đồng ý"* trong phiên cho ba đề xuất: (a) mở Issue + soạn đặc tả; (b) chỉ nhận **chuỗi thật**, bỏ cả `int`; (c) xếp sau `T131-DEADLINE-DEM-SPAWN`. Q3 xác nhận riêng: #678 comment `5885268193`. **r2** là hệ quả của cross-review lượt 1 trên PR #679 (comment `5885578969`, VERDICT sha256 `d4acdd38…b8add`), dưới chỉ thị chủ kho *"cross-review #679 đi, theo phân lớp, không theo từng lỗi, có hint patch"*. **r3** là hệ quả của cross-review lượt 2 trên PR #679 (comment `5886034260`, VERDICT sha256 `aa9a68d3…d4882`: 1 P1 / 3 P2 / 1 P3 theo lớp), và của quyết định chủ kho chọn neo lớp P1 bằng Mission Issue mới (#682). **r4** là hệ quả của cross-review lượt 3 trên PR #679 (comment `5887068702`, VERDICT sha256 `1eb00c7a…7e819`: 0 P1 / 2 P2 / 1 P3 theo lớp; P1 của lượt 2 đã đóng). **r5** là hệ quả của cross-review lượt 4 trên PR #679 (comment `5888141866`, VERDICT sha256 `9abc767695097d523d4e5faedd6929678f71c4d21b9fca620480230575986ed3`: 0 P1 / 1 P2 / 0 P3 theo lớp; lớp `bo-quet-chung-cu-khong-neo-anh`), của điều kiện dừng đã đăng ký ở comment `5887068702` (§9), và của quyết định Q7 của chủ kho (Mission #682, comment `5888143430`; §3). **r6** là hệ quả của cross-review lượt 5 trên PR #679 (comment `5888630117`, VERDICT sha256 `ce14afd8ba46d5b17bc1f121b2ae8fe042771af37847acdbd348ecb9942ac33d`: 0 P1 / 2 P2 / 0 P3 theo lớp; hai lớp `bo-quet-chung-cu-khong-neo-anh` và `bo-quet-nghiem-thu-thieu-mien`) và của hai quyết định chủ kho ở Mission #682: Q8 (uỷ quyền cấp lease `wp678`, thứ tự và bốn điều kiện cấp; comment `5888631719`) và Q9 (toàn vẹn object-store nằm NGOÀI phạm vi A9); §3. |
| `objective` | Mọi đường đưa `lease_id` vào danh tính chỉ nhận chuỗi thật khớp `LEASE_ID`, đóng va chạm do ép giá trị không phải chuỗi thành chuỗi. Danh tính là giá trị sau `yaml.safe_load`: các cách viết ra cùng một chuỗi hợp lệ cố ý là cùng danh tính (ví dụ `'yes'` và `!!str yes`), không yêu cầu phân biệt cú pháp YAML. |
| `review_class` | **`sensitive`**: chạm `ops/lease_publish.py`, tức cổng đăng lease. |
| `risk` | **`sensitive`**: cùng lý do. |
| `executor` | `claude` (Claude Opus 5.5, effort ≥ medium) |
| `environment` | **`cloud`**. Packet không đo hành vi phụ thuộc nền (không đồng hồ ngủ máy, không đường dẫn Windows); tiền lệ các đặc tả `ops/specs/*` cùng lớp khai `cloud`. Chủ kho đổi thì phải ra revision mới. |
| reviewer | `codex` (`gpt-6-astra`, effort ≥ medium) |
| `depends_on` | **Theo Q8 (§3), viết lại ở r6.** Chủ kho uỷ quyền cấp lease `wp678`; thứ tự là đợi lease `lease-publish-windows-do-r1-g1-claude` của packet #687 (giữ `ops/lease_publish_test.py`) nhả. Bốn điều kiện cấp, cả bốn phải thoả và **đo lại lúc cấp**, không nhận số dưới đây thay phép đo: (1) `ai-dang-giu ops/lease_publish.py` và `ai-dang-giu ops/lease_publish_test.py` đều ra `NGƯỜI_GIỮ 0`, và chỉ tin kết quả ấy sau khi so `git ls-remote --heads origin` với `git for-each-ref refs/remotes/origin` theo **tập tên** (thiếu ref cục bộ ⇒ MÙ ⇒ fail-close, không cấp); (2) không lượt review nào đang chạy; (3) lease neo `spec_hash` của revision **cuối cùng đã review sạch** (0 P1/P2/P3); (4) nếu #687 land trước và đổi `ops/lease_publish_test.py` thì dời nền nghiệm thu bằng một revision mới **trước** khi cấp, không cấp trên nền cũ. Đây là kiểm loại trừ write set của protocol cộng điều kiện cấp của Q8, **không** phải cổng quét kiểu `lease_id`: cổng quét kiểu chỉ đặt trước land (A9, Q7). **Hiện tại, đo 10:48Z–10:49Z 29-09 (r6):** `ai-dang-giu ops/lease_publish.py` ⇒ dòng cuối `NGƯỜI_GIỮ 0: không có`, rc=0; `ai-dang-giu ops/lease_publish_test.py` ⇒ dòng cuối `NGƯỜI_GIỮ 1: lease-publish-windows-do-r1-g1-claude`, rc=11. Lease ấy ở nhãn `CÒN_HẠN`, tệp lease ở `refs/remotes/origin/claude/lease-publish-windows-do` khai `packet_issue: 687`, `write_set` gồm đúng `ops/lease_publish_test.py`, `leased_at_utc: '2026-09-29T10:20:00Z'`, `lease_expires_at_utc: '2026-09-30T10:20:00Z'` (đọc bằng `git show`, 10:49Z). Nên điều kiện (1) **chưa thoả** ở thời điểm đo và phép hỏi cấp lease `wp678` hiện phải chờ. So tên ref: máy chủ 511, cục bộ 512, thiếu cục bộ 0, thừa cục bộ 1 (`claude/bookkeeping-574-land`, `ls-remote` không còn nhánh này: ref đệm cũ, vô hại). Lịch sử: đo 10:14Z (r5) và 09:44Z (r4) cả hai tệp `NGƯỜI_GIỮ 0` (lease của #687 chưa có, `leased_at` 10:20Z); đo 07:59Z 29-09 `ai-dang-giu ops/lease_publish_test.py` ⇒ `NGƯỜI_GIỮ 1: t131-deadline-dem-spawn-exec-1-claude-20260929`, đã `HẾT_HẠN` (`lease_expires_at_utc: '2026-09-29T08:15:00Z'`) và T131 **đã land** (PR #680, `89fc4fa`). |
| nền nghiệm thu | `origin/master` `89fc4fac8cea65979cc2483043dc8cd07a6e8518` (PR #680, T131 land). Đây là **nền bất biến** để đo diff và nghiệm thu. r1 và r2 dùng `1741e0a1ab7ebce4b26912aefadca56ddfcdc691`; packet CHƯA thi hành, chưa có diff hay lịch sử finding trên mã, nên việc dời nền ở r3 là quyết định bền (chính r3) theo protocol §3.2.1, không phải dùng HEAD mới để xoá diff. r4, r5 và r6 **giữ nguyên** nền của r3: `git fetch` rồi `git rev-parse origin/master` đo 09:44Z 29-09 (r4), 10:14Z 29-09 (r5) và 10:48Z 29-09 (r6) vẫn ra `89fc4fac8cea65979cc2483043dc8cd07a6e8518`. Nếu #687 land trước và đổi `ops/lease_publish_test.py`, nền phải dời bằng revision mới trước khi cấp (Q8, điều kiện 4). `ops/lease_publish.py` giống hệt giữa hai nền (`git diff --quiet` rc=0), nên các phép đo §1/§2 làm trên `1741e0a` vẫn hợp lệ; chỉ `ops/lease_publish_test.py` đổi (+13/−19, bốn hunk: hai trong t131, một trong t139, một trong t192). Nền tiếp nối (continuation base), nếu khác, phải được khai riêng lúc cấp lease, không thay nền này. |
| `spec_hash` | Xem **Công thức băm** ngay dưới. Giá trị **không** nằm trong tệp này. |

**Công thức băm.** `spec_hash` = SHA-256 trên **toàn bộ bytes** của tệp này tại commit đã đóng
băng: `sha256sum ops/specs/lease-id-ep-kieu-yaml-r6.md`, không loại dòng nào. Giá trị được công
bố **ngoài** tệp: comment trên #678 và lease, kèm OID commit + đường dẫn. Hai tên `spec_hash`
và `spec_sha256` nếu cùng xuất hiện thì mang **cùng** một giá trị. Đổi bất kỳ byte nào ⇒
revision mới, băm mới, lease mới. Vì khối closure dưới đây nằm **trong** tệp, cùng một `spec_hash`
không thể đi với hai closure khác nhau (đóng phản chứng "hai lease khác `required_checks` cùng
một băm" của lượt 2).

**Closure đóng băng** (các trường dispatcher dẫn xuất, protocol §3.2). Kho chưa có dispatcher
sinh chúng và chưa có policy canonical cho closure; khối này do phiên điều phối điền tay theo
**miễn trừ có phạm vi** ghi ở Mission Issue #682: chỉ `wp678`, mọi revision từ r3, hết hiệu lực
ở lần đầu một policy canonical cho closure xuất hiện trên nhánh mặc định; đổi bất kỳ giá trị
closure ⇒ revision mới, `spec_hash` mới, lease mới; write set không mở rộng.

| trường | giá trị |
|---|---|
| `change_policy_sha` | `null` — chưa có policy canonical; descriptor thay thế là miễn trừ ở #682 |
| `effective_write_set` | `ops/lease_publish.py` · `ops/lease_publish_test.py` (exact) |
| `effective_review_class` | `sensitive` |
| `required_checks` | Trên PR thi hành: `gate (ubuntu-latest)`, `gate-ops (ubuntu-latest)`, `gate-registry (ubuntu-latest)`, `gate-packet-loop (ubuntu-latest)` của `.github/workflows/ci.yml`, và workflow `thu-hoi`; cross-review codex 0 P1/P2/P3 |
| `land_obligations` | Chủ kho audit + merge (không tự merge/approve); ghi sổ verdict + HINT các lượt vào `ops/reviews/` kèm receipt và mục README; thu hồi lease sau land; đóng #678; cập nhật #677 về tương tác A2 |

**Descriptor nguồn closure** = `{mission_issue: 682, object_id: 5627190292}`. Closure do phiên
điều phối điền tay theo miễn trừ ấy, **không** do executor tự khai. Lease phải **chép** đúng các
giá trị trên, không được thêm hay đổi; lệch ⇒ **DỪNG**. Băm thân Issue ở phía nhận là
**KHÔNG ĐO ĐƯỢC** từ phiên này (đường đọc MCP chuẩn hoá thực thể HTML trong thân issue, xem
CLAUDE.md), nên descriptor neo bằng object ID + số Issue, không bằng băm thân.

**GIỚI HẠN LỜI KHAI:** mọi khẳng định chỉ chứng minh tới đúng phép đo ghi kèm.
**Ba trạng thái:** có · không · **KHÔNG ĐO ĐƯỢC**.

---

## 1. Vấn đề

`_doc_yaml` dùng `yaml.safe_load` (YAML 1.1), nên một vô hướng không nháy được tự ép kiểu.
`kiem()` làm `str(lease["lease_id"])` **rồi mới** `LEASE_ID.fullmatch`. Vì vậy nhiều cách viết
khác nhau cho ra **cùng một danh tính**, và danh tính ấy là thứ cổng đăng dùng để chống đăng trùng.

Bảng đo 06:2xZ 29-09-2026 trên `1741e0a`. Cách dựng: lease
`wp55-r4-review-viet-lai-codex-20260815.yaml`, bỏ các trường `prompt_*`, gọi
`kiem(bo_qua_han=True)` không truyền `tep`, nên **đường bia mộ chưa chạy** ở phép đo này.

| YAML `lease_id:` | kiểu | `str()` | `_tien_kiem_mien_dang` | `kiem()` |
|---|---|---|---|---|
| `true` `yes` `on` `True` | bool | `True` | rc=8 | qua |
| `1.5` `1.50` | float | `1.5` | rc=8 | qua |
| `0x1F` | int | `31` | qua | qua |
| `017` | int | `15` | qua | qua |
| `1_000` | int | `1000` | qua | qua |
| `2026-09-29` | date | `2026-09-29` | rc=8 | qua |
| `'yes'` (đối chứng) | str | `yes` | qua | qua |

Va chạm đo tại `_kiem_comment_da_co`, với `_doc_gh` giả trả **một** comment của
`github-actions[bot]`. Sáu cặp (comment có sẵn ↔ lease mới) `True`↔`yes`, `True`↔`on`,
`1.5`↔`1.50`, `31`↔`0x1F`, `15`↔`017`, `1000`↔`1_000` đều cho **rc=9**, tức cổng coi lease là
đã đăng nên lease mới **không bao giờ được đăng**. Đối chứng `khac-lease`↔`yes` cho rc=0, nên
cách dựng không cho kết quả giả.

Ở **biên workflow** (thân bước `đăng` trích bằng `_buoc_workflow`, `lease_publish.py` thật, `gh`
giả trên PATH, giữ trạng thái), cross-review lượt 1 đo trên `342e62c7` (cùng blob hai tệp Python
với `1741e0a`): lease `yes` gặp comment ``**Lease `True`**`` ⇒ bước `rc=0`, **0 POST**; đối chứng
`'fresh-id'` ⇒ `rc=0`, **1 POST**. Tức lease hợp lệ bị bỏ qua mà bước vẫn xanh. Ca khoá ở A3
biến phép đo ấy thành ca của suite.

## 2. Các đường `lease_id` đi vào danh tính (số dòng trên `1741e0a`)

Liệt kê HẾT trước khi vá (bài học *"VÁ ĐÚNG CHỖ ĐƯỢC CHỈ RỒI BỎ SÓT ĐƯỜNG THỨ BA"*). Tìm bằng
`grep -n '"lease_id"\|\[.lease_id.\]' ops/lease_publish.py`, không phải bằng trí nhớ.

| # | chỗ | hiện trạng |
|---|---|---|
| D1 | `kiem()` :861 | `str()` rồi mới so regex ⇒ nhận bool/float/int/date |
| D2 | `_tien_kiem_mien_dang` :949 | nhận `str\|int`, chặn `bool`; lệch với D1 |
| D3 | `_kiem_comment_da_co` :668 | `str()` ⇒ va chạm ở §1 |
| D4 | `dung_than` :1070 | f-string ⇒ đăng dấu đã bị ép kiểu |
| D5 | `_bia_mo_doi_xung` :587/:592 | `str(... or "")` cho cả lease cũ lẫn lease được quét |
| D6 | `_kiem_bia_mo` :609/:612 | `str(... or "")`; trong khi `_danh_sach_thay_the_cho` đòi chuỗi thật |
| D7 | `lenh_ai_dang_giu` :2110/:2123 | `str(...)` rồi dùng làm khoá người giữ ⇒ `yes` và `on` gộp về `True` |
| D8 | `_du_bao_check` :1938/:1942/:1946; `_du_bao_ai_dang_giu` :1967 | :1938/:1942 so giá trị thô; :1946 f-string, :1967 `str()` rồi tra tập ID thu hồi |
| D9 | in :2074/:2089; `lenh_con_tro_treo` :2139/:2143 | chỉ hiển thị; không gán hai chỗ sau cho D7 |
| — | `kiem_ban_ghi_thu_hoi` :1192 | **ĐÃ** đòi `isinstance(str)`: tiền lệ trong chính tệp, không sửa |

Ngoài tệp: `.github/workflows/*.yml` **không** đọc `lease_id` (grep 0 dòng).
`.claude/dev/packet_loop.py` :769–771 **đã** đòi `isinstance(str)` cho `lease_id` (tiền lệ thứ hai).

## 3. Quyết định

- **Q1 — Danh sách CHO PHÉP kiểu** (chủ kho, 29-09): `lease_id` hợp lệ khi và chỉ khi nó là
  `str` **ngay sau `yaml.safe_load`** **và** khớp `LEASE_ID`. `int` cũng bị từ chối. Sai ⇒
  `Chan(RC_NOI_DUNG)`, tức rc=8.
- **Q2 — Một hàm dùng chung** (chủ kho, 29-09): mọi đường D1–D8 đọc `lease_id` qua **một**
  hàm, không ai tự gọi `str()` lên giá trị thô.
- **Q3 — Lease sai kiểu gặp trong lúc QUÉT** (đã được chủ kho xác nhận cùng Q1–Q4 tại
  packet #678, theo authority giao cross-review): ở D5, D6, D7, một lease **khác** mang `lease_id` không phải
  chuỗi thì **không** được ép sang chuỗi để so. D7 in `KHÔNG_XÁC_ĐỊNH` cho nó và thoát khác 0
  (fail-close, cùng hình dạng với nhánh bia mộ một chiều đang có). D5/D6 coi nó là **không
  khớp** bất kỳ tên nào, và vì vậy bia mộ trỏ tới nó sẽ không thoả.
- **Q4 — Thứ tự**: sau `T131-DEADLINE-DEM-SPAWN`. Hai packet còn chồng write set là #677 và
  `LEASE-PUBLISH-WINDOWS-DO`; chủ kho xếp, packet này không tự nhảy lên trước.
- **Q7 — Cổng A9 CHỈ đặt trước LAND** (chủ kho, 29-09, Mission #682 comment `5888143430`): cổng là
  một helper có ca kiểm do **executor viết** trong `ops/lease_publish_test.py`. **KHÔNG** có cổng quét
  trước khi cấp lease, và không bên nào phải bàn giao dụng cụ đo trước cấp. Số quét cũ ở §8 giữ làm
  THAM KHẢO có nhãn. Lý do (chép vào đặc tả để không phải suy lại): câu mà một phép quét trước cấp
  trả lời, tức *"có lease nào đang dựa vào ép kiểu không"*, đã được trả lời để chốt Q1 (0 lease sai
  kiểu trên 563 cặp, đo 09:44Z); rủi ro thật chỉ hiện ra lúc land, và A9 đặt trước land chặn đúng lúc
  ấy. Q7 bác phần "dụng cụ đo độc lập bàn giao trước cấp lease, chưa có thì DỪNG cấp" mà HINT lượt 4
  đề xuất.
- **Q8 — Uỷ quyền cấp lease `wp678`, thứ tự và bốn điều kiện cấp** (chủ kho, 29-09, Mission #682
  comment `5888631719`): chủ kho uỷ quyền cấp lease `wp678`. Thứ tự: đợi lease
  `lease-publish-windows-do-r1-g1-claude` của packet #687, đang giữ `ops/lease_publish_test.py` tới
  `2026-09-30T10:20:00Z`, nhả. Cấp chỉ khi cả bốn điều kiện thoả: (1) cả hai tệp của write set
  `NGƯỜI_GIỮ 0`, sau khi so `ls-remote --heads` với `for-each-ref refs/remotes/origin` theo tập tên;
  (2) không lượt review nào đang chạy; (3) lease neo `spec_hash` của revision cuối đã review sạch;
  (4) nếu #687 land trước và đổi `ops/lease_publish_test.py` thì dời nền nghiệm thu bằng revision mới
  trước khi cấp. Q8 **không** thêm cổng quét kiểu `lease_id` trước cấp: Q7 còn nguyên. Điều kiện (1) đã
  có dạng "không lease nào còn hiệu lực giữ hai tệp" ở `depends_on` của r5, r6 thêm phép so tập tên
  ref; điều kiện (2)–(4) là mới ở r6. Trạng thái đo của điều kiện (1) ở header.
- **Q9 — Toàn vẹn object-store NGOÀI phạm vi A9** (chủ kho, 29-09, Mission #682 comment `5888660607`): câu A9 trả lời là *"có `lease_id` sai kiểu không"*, không phải *"kho có hỏng không"*.
  Yêu cầu r5 và HINT lượt 5 về băm toàn chuỗi (commit, tree gốc, mọi tree con, blob) **bị bác** và
  thay bằng **điều kiện tiên quyết**: `git fsck --full` rc=0 chạy trong **cùng lượt quét** A9, output
  và rc ghi vào handoff, kèm câu nói thẳng rằng nó **không nguyên tử** (fsck kiểm một ảnh, lượt quét
  đọc một ảnh khác nếu kho đổi giữa chừng) và đó là **rủi ro được chấp nhận có chủ đích**. GIỮ yêu cầu
  băm blob trên chính bytes đưa vào parser (rẻ, đã có từ r5). `fsck` rc khác 0 ⇒ `KHÔNG ĐO ĐƯỢC` ⇒
  không land. Hệ quả cho hợp đồng: helper A9 **không** kiểm commit, tree gốc hay tree con, và không
  được đọc là đã kiểm; ca "tree con hỏng" của lượt 5 nằm ngoài phạm vi helper và được bắt bởi điều kiện
  tiên quyết fsck (A9, Phụ lục A).

## 4. `write_set`

- `ops/lease_publish.py`
- `ops/lease_publish_test.py`

Không đường dẫn nào khác. Riêng đặc tả này (`ops/specs/lease-id-ep-kieu-yaml-r6.md`, và các bản r1, r2, r3, r4, r5 nó thay) là hồ sơ
của lượt soạn spec, **không** thuộc write set của lượt thi hành.

## 5. `ngoai_pham_vi`

- `.github/workflows/**`: không đọc `lease_id`, và phiếu cấm sửa trừ khi chủ kho cho phép rõ.
- `.claude/dev/packet_loop.py`: đã đòi chuỗi (§2).
- `kiem_ban_ghi_thu_hoi` và sổ thu hồi: đã đòi chuỗi (§2).
- Ép kiểu của **các trường khác** (`reviewed_sha_required`, `expires_utc`…): cùng họ lỗi, nhưng
  không nằm trong quyết định của chủ kho. Lượt thi hành gặp thì ghi thành phát hiện ngoài spec,
  **không** tự mở rộng.
- Idempotency theo nội dung thay vì theo `lease_id`: là việc của #584.
- Thêm/đổi lease trên Issue thật để thử: không làm, mọi phép đo dùng `gh` giả.

## 6. `muc_tieu`

Mỗi dòng chiếu vào **một** đường dẫn trong write set (L2).

1. `ops/lease_publish.py` — Thêm một hàm (tên tuỳ executor, ví dụ `_lease_id_hop_le`) nhận giá
   trị thô và trả `str` hoặc ném `Chan(RC_NOI_DUNG)`. Dùng nó ở D1 và D2.
2. `ops/lease_publish.py` — D3 và D4 tự gọi hàm ấy. Không dựa vào việc `kiem()` đã chạy trước;
   mỗi đường một chốt riêng.
3. `ops/lease_publish.py` — D5 và D6 so danh tính theo Q3, bỏ `str(... or "")` lên giá trị thô.
4. `ops/lease_publish.py` — D7 theo Q3: gặp lease sai kiểu thì in `KHÔNG_XÁC_ĐỊNH` và thoát khác 0.
5. `ops/lease_publish.py` — D8 so bằng giá trị đã qua hàm ở mục 1, hoặc chứng minh đường ấy
   không tới được với giá trị sai kiểu (xem A7).
6. `ops/lease_publish_test.py` — Một ca cho mỗi mục 1–5, theo §7.
7. `ops/lease_publish_test.py` — Sửa các docstring/chú thích đang **khai hiện trạng lỗi** thành
   sự thật mới. Ví dụ đã biết: `t178` :7763–7764 (trên `89fc4fa`; trước là 7769–7770 trên `1741e0a`) viết *"`lease_id` sai KIỂU thì không có chốt
   tương ứng trong `kiem()`"*. Executor phải grep tìm hết, đừng chỉ sửa chỗ này.

## 7. `nghiem_thu`

Mỗi tiêu chí nêu phép đo làm nó ĐỎ (L3). "Đột biến" nghĩa là chạy trên **bản sao tạm**, với
`PYTHONDONTWRITEBYTECODE=1`.

- **A1 (mục 1, D1)** — Ca mới: các dạng `true` `yes` `on` `1.5` `1.50` `0x1F` `017` `1_000`
  `5` `2026-09-29`, viết thành **văn bản YAML** và đọc qua `_doc_yaml` (không dựng dict bằng
  tay, để phép đo đi qua đúng lớp gây lỗi), đều cho `kiem()` ⇒ rc=8. Đối chứng `'yes'` có nháy
  ⇒ qua.
  **ĐỎ khi:** trả D1 về `str(lease["lease_id"])` ⇒ các dạng trên qua. Trên nền `89fc4fa` (mã `ops/lease_publish.py` giống hệt `1741e0a`) ca
  này ĐỎ.
- **A2 (mục 1, D2)** — Mở rộng trục `lease_id` sai kiểu của `t178` thêm `int`; giữ chốt
  `_do_dau_da_dang` trả về bình thường và **0** lời gọi GitHub. Đo thêm D2 trực tiếp:
  `_tien_kiem_mien_dang` nhận `int` ⇒ `Chan(RC_NOI_DUNG)`; chuỗi hợp lệ ⇒ trả về.
  **ĐỎ khi:** trả riêng D2 về `(str, int)` ⇒ ca trực tiếp nhận trả về thay vì rc=8.
  Không đòi phép dò gọi GitHub khi D2 bị gỡ: D3 có chốt độc lập trước `_doc_gh`, nên vẫn
  có thể giữ số gọi bằng 0. Không dời chốt D3 xuống sau mạng chỉ để giết mutant D2.
  Tương tác #677: `L` gỡ riêng D2 nay có thể sống ở phép đếm mạng của `t178`; ca trực tiếp
  phải giết `L` bằng `TinHieuChotCa` đúng ca. #677 **chưa có đặc tả đóng băng** (Issue #677
  khai `revision 0`, đo 06:2xZ 29-09; vẫn chưa có đặc tả đóng băng tại 07:59Z 29-09, nội dung nghĩa vụ hai thứ tự dưới đây không đổi). Cập nhật đo 09:45Z 29-09: tệp `ops/specs/dot-bien-l-bien-cong-khai-r1.md` (sha256 `81468e21c7a7d32167d210b17813dab2b825992a1587b86d8bc8b3dc9142a4da`) đã có ở `refs/remotes/origin/claude/spec-dot-bien-l-bien-cong-khai-20260929` (`c78a5d06`), chưa có trên master; trạng thái đóng băng và lease của nó không đo ở lượt này, nên packet này vẫn không neo acceptance nào vào nó.
  Hai thứ tự, hai nghĩa vụ: packet này land TRƯỚC ⇒ đặc tả #677 phải được soạn trên nền mới
  và coi ca trực tiếp của A2 là nơi `L` chết; #677 land TRƯỚC ⇒ ca của #677 nằm trong
  `ops/lease_publish_test.py`, tức trong write set này, và lượt thi hành phải giữ nó xanh
  với ý nghĩa đã đổi. Executor **không** sửa đặc tả #677.
  Sửa cả docstring D2 và `t178` để tách bằng chứng lịch sử khỏi hành vi sau D3.
- **A3 (mục 2, D3) — CA BIÊN WORKFLOW** — Thân bước `đăng` trích từ
  `.github/workflows/ops-publish-lease.yml` (dùng lại bộ trích sẵn có trong suite, không chép
  lại), `lease_publish.py` thật, `gh` giả **trên PATH** và **giữ trạng thái**. Issue đã có comment
  bot ``**Lease `True`**``; lease mới khai `lease_id: yes` ⇒ bước **khác 0** và **0 POST**. Kèm
  ca đối chứng dương: một `lease_id` chuỗi hợp lệ khác ⇒ bước 0 và đúng **1 POST**, để giàn hỏng
  không thể xanh.
  **ĐỎ khi:** chạy trên nền `89fc4fa` (mã giống hệt `1741e0a`) ⇒ bước `rc=0`, 0 POST (lời khai của phiếu; ca này là phép
  đo đầu tiên của nó).
  Kèm ca **đơn vị**: gọi thẳng `_kiem_comment_da_co` với `lease_id=True` ⇒ rc=8, **không** rc=9.
  Đột biến gỡ chốt riêng của D3 (giữ nguyên D1) ⇒ ca đơn vị ĐỎ.
- **A4 (mục 2, D4)** — Gọi thẳng `dung_than` với `lease_id` không phải chuỗi ⇒ rc=8.
  **ĐỎ khi:** gỡ chốt riêng của D4 ⇒ nó trả thân có ``**Lease `True`**``.
- **A5 (mục 3, D5/D6)** — Fixture kho git tạm: lease cũ `lease_id: 1_000` (int) mang
  `da_bi_thay_the: <mới>`; lease mới khai `thay_the_cho: "1000"` ⇒ `_kiem_bia_mo` rc=8. Đối
  chứng: lease cũ `lease_id: "1000"` có nháy ⇒ qua. Đo riêng `_bia_mo_doi_xung` bằng cặp tương
  tự: bản sai kiểu ⇒ `False`, bản chuỗi ⇒ `True`.
  Bổ sung đầu còn lại: ở D5, lease cũ chuỗi trỏ `da_bi_thay_the: "1000"`, lease được
  quét có `lease_id: 1_000` và trỏ ngược ⇒ `False`; đổi ID được quét thành `"1000"` ⇒ `True`.
  Ở D6, gọi trực tiếp với lease mới `lease_id: 1_000`, lease cũ chuỗi trỏ ngược `"1000"`
  ⇒ rc=8; đổi ID lease mới thành `"1000"` ⇒ qua. Không đi qua D1 trong các ca đơn vị này.
  **ĐỎ khi:** trả phép ép kiểu về riêng từng toán hạng ở D5 (:587, :592) và D6 (:609, :612),
  giữ nguyên các chốt còn lại; mỗi mutant phải giết đúng ca đổi kiểu toán hạng ấy.
  Không hoàn nguyên cả hàm rồi nhận đó là bằng chứng mọi vị trí đọc đều có răng.
- **A6 (mục 4, D7)** — Hai lease trên hai ref, `lease_id: yes` và `lease_id: on`, cùng giữ một
  đường dẫn ⇒ `ai-dang-giu` in `KHÔNG_XÁC_ĐỊNH` cho cả hai và thoát khác 0.
  **ĐỎ khi:** chạy trên nền với hai lease còn hạn ⇒ `NGƯỜI_GIỮ 1: True`, rc=11.
  Vì nền đã khác 0, ca phải chốt nhãn `KHÔNG_XÁC_ĐỊNH` và danh tính ref/path của cả hai
  lease lỗi; không chỉ kiểm `rc != 0`. Đo lại 29-09-2026 bằng fixture hai ref trong review #679.
- **A7 (mục 5, D8)** — Đo riêng cả `check --du-bao` và `ai-dang-giu --du-bao`.
  `check` qua D1 trước; `ai-dang-giu` gọi dự báo trước vòng D7 và không gọi D1. Không dùng
  kết quả không tới được của `check` để miễn nhánh `ai-dang-giu`, hoặc chỉ đo lời gọi trực
  tiếp helper rồi suy thành khả năng tới được từ CLI. Lease sai kiểu vẫn tới :1967 trên
  nền; khi thêm chốt ở D8 cần ca trực tiếp để D7/D1 không che mutant của chính D8.
  · Tới được ⇒ chốt + ca, đột biến gỡ chốt ⇒ ĐỎ.
  · Không tới được ⇒ một ca chứng minh lease sai kiểu bị chặn **trước** các dòng ấy, kèm đột biến
  gỡ chốt D1 để chứng minh ca có răng. Ghi rõ đã chọn nhánh nào và bằng phép đo nào.
- **A8 (mục 6/7, cả write set)** — Toàn suite `ops/lease_publish_test.py` **delta = 0 ca đỏ**
  so với nền. Số lịch sử đo 06:4xZ 29-09 trên `1741e0a`: **185/187**. Hai ca đỏ là `t137` và `t159`,
  cả hai `KHÔNG ĐO ĐƯỢC: thiếu shellcheck` (lời khai lịch sử, không dùng làm nền hiện tại).
  Review #679 đo lại 29-09-2026: **187/187**, rc=0, bỏ qua=0, với shellcheck 0.9.0 và
  actionlint 1.7.7; hai tệp Python có cùng blob với `1741e0a` (lịch sử). **Nền hiện tại**
  (`89fc4fa`): suite **187/187**, rc=0, bỏ qua 0, đo 08:0xZ 29-09 trên commit merge `589336f`
  (cây của `89fc4fa` + các tệp spec) với shellcheck 0.9.0 + actionlint 1.7.7. Lệnh: từ gốc repo chạy
  `PYTHONDONTWRITEBYTECODE=1 TMPDIR=<scratch> python ops/lease_publish_test.py`.
  Khi thi hành, đo lại **cả hai vế** (nền và ứng viên) trong **một** lệnh, cùng công cụ.
  `python -m ruff check --select F ops/lease_publish.py ops/lease_publish_test.py`: delta F = 0.
  **ĐỎ khi:** ứng viên có thêm ca đỏ, hoặc có thêm lỗi F.
- **A9 (cổng đo lease sai kiểu, CHỈ đặt trước LAND, theo Q7)** — Trước khi xin land, executor chạy
  một helper do **chính executor viết** trong `ops/lease_publish_test.py`, kèm ca kiểm của nó (danh
  mục ở cuối mục này), rồi ghi vào handoff: UTC, lệnh tái lập nguyên văn, output, tập ref+OID và các
  số đếm. Có bất kỳ lease nào không qua Q1 ⇒ **DỪNG land**, báo chủ kho. Điều kiện tiên quyết
  `git fsck --full` (Q9, bullet riêng bên dưới) không đạt hoặc không có bằng chứng trong handoff ⇒
  `KHÔNG ĐO ĐƯỢC` ⇒ cũng **không land**. **KHÔNG có cổng quét trước khi
  cấp lease** (Q7): cấp lease không đòi số quét nào, và không bên nào phải bàn giao dụng cụ đo trước
  cấp. Lý do, chép từ Q7: câu mà phép quét trước cấp trả lời (*"có lease nào đang dựa vào ép kiểu
  không"*) đã được trả lời để chốt Q1 (0 lease sai kiểu trên 563 cặp, đo 09:44Z, §8); rủi ro thật chỉ
  hiện ra lúc land, và A9 đặt trước land chặn đúng lúc ấy. Số ở §8 là **tham khảo**, không thay A9.
  Ca kiểm của suite chỉ dựng kho tạm (không phụ thuộc số ref hay lease của kho thật, để suite không
  trôi theo kho); lần quét kho thật là một lần chạy riêng của helper, ghi vào handoff.
  Nghĩa vụ chứng cứ của helper. Tất cả đã tích luỹ qua bốn lượt review và được **giữ nguyên**: gỡ mã
  tham chiếu khỏi đặc tả không gỡ nghĩa vụ nào. **Hai chỗ r6 đổi**, cả hai từ lượt 5: bullet *Schema
  con trỏ* viết lại cho đủ miền tuỳ chọn, và toàn vẹn object-store chuyển thành điều kiện tiên quyết
  theo Q9 (không còn đòi helper kiểm tree).
  · **Miền.** `refs/heads/*` và `refs/remotes/*`, chỉ bỏ ref có leaf HEAD VÀ là symbolic ref; ref thường
  có hậu tố `/HEAD` vẫn phải quét (runtime hiện bỏ cả hậu tố này; đây là miền nghiệm thu bảo thủ hơn,
  không yêu cầu đổi bộ liệt kê ref runtime). Đọc cả `.yaml` lẫn `.yml` dưới `ops/leases/`. Quét thêm
  `ops/leases_retired/` với nhãn lịch sử riêng.
  · **Lỗi không được im lặng.** Kiểm rc của mọi lệnh Git và bắt cả cảnh báo ref hỏng trên `stderr` (Git
  bỏ lặng lẽ ref hỏng mà vẫn trả rc=0, xem cuối Phụ lục A). Lỗi parse, tài liệu không phải ánh xạ, thiếu
  ID, ID không qua Q1 ⇒ báo lỗi. Không im lặng bỏ mục lỗi khỏi mẫu số.
  · **Schema con trỏ (viết lại ở r6, từ lượt 5).** Hai trường đều **tuỳ chọn**, và miền hợp lệ của
  helper phải BẰNG miền runtime đang nhận, không hẹp hơn. Đọc từ `ops/lease_publish.py` trên
  `origin/master` `89fc4fa` (đọc và chạy lại 10:49Z):
  `thay_the_cho` qua `_danh_sach_thay_the_cho` (:561–572). Vắng trường (`.get` trả `None`), `null`
  hoặc chuỗi rỗng ⇒ danh sách rỗng, HỢP LỆ (:563–564). Chuỗi chỉ gồm khoảng trắng ⇒ cũng danh sách
  rỗng, HỢP LỆ (:565–567: `strip()` rỗng thì trả `[]`). Chuỗi không trắng ⇒ một con trỏ. Danh sách ⇒
  mọi phần tử phải là chuỗi không trắng, danh sách rỗng hợp lệ (:568–571); phần tử không phải chuỗi
  hoặc trắng ⇒ LỖI. Kiểu khác (`False`, `0`, ánh xạ, số) ⇒ LỖI (:572; `False in (None, "")` là
  `False`, nên `False` và `0` không lọt vào nhánh "không có con trỏ").
  `da_bi_thay_the` qua `_bia_mo_doi_xung` (:575–597). Vắng trường, `null` hoặc chuỗi rỗng ⇒ hàm trả
  `None`, nghĩa là **không có bia mộ**, HỢP LỆ (:581–583). Chuỗi không trắng ⇒ bia mộ. **Mọi giá trị
  khác** ⇒ hàm trả `False` (:584–585), tức bia mộ không hợp lệ: gồm mọi giá trị không phải chuỗi
  (danh sách kể cả rỗng, `False`, `0`, ánh xạ) **và chuỗi chỉ gồm khoảng trắng** (`raw_moi.strip()`
  rỗng ⇒ `False`, không phải `None`; đã chạy lại: `"   "` ⇒ `False`). Ở `ai-dang-giu`, `False` với lease
  còn hạn thành `KHÔNG_XÁC_ĐỊNH` (:2111–2118). Helper báo LỖI (rc=1) cho các dạng này bất kể hạn:
  đó là miền nghiệm thu bảo thủ, kế thừa r4, không đòi đổi runtime.
  Hệ quả: **hai trường KHÔNG cùng miền** (chuỗi trắng hợp lệ ở `thay_the_cho`, lỗi ở
  `da_bi_thay_the`; danh sách hợp lệ ở `thay_the_cho`, lỗi ở `da_bi_thay_the`), nên không dùng chung
  phép chấp nhận cho cả hai và không dùng kiểm "giá trị sai" (truthiness) chung: nó nuốt luôn `False`
  và `0`. Không biến việc kiểm schema thành yêu cầu mọi bia mộ lịch sử đều còn cặp đối xứng trên cùng
  ref. Chỉ đo, không sửa lease cũ.
  · **Neo ảnh theo OID.** Giữ map ref→OID của lần liệt kê; đọc tree và blob theo OID đã liệt kê, không
  đọc lại tên ref có thể trôi. Tắt Git replace ở MỌI lệnh Git: OID phải chỉ đúng object gốc, không phải
  object do `refs/replace` hoặc `GIT_REPLACE_REF_BASE` thay thế.
  · **Neo bytes vào OID (mới ở r5, từ lượt 4).** Băm object Git của blob theo object format của kho trên
  CHÍNH bytes đưa vào YAML parser: đọc bytes một lần, băm và phân tích cùng một biến bytes (đọc hai
  lần rồi ghép là mở lại cửa đua). `cat-file` rc=0 không chứng minh băm khớp OID. Sai băm hoặc thiếu
  object ⇒ **KHÔNG ĐO ĐƯỢC** (rc=2), không kết luận lease sạch hay hỏng từ nội dung đó. Phép băm này
  chỉ áp cho **blob** mà helper đưa vào parser; `git fsck --full` (bullet ngay dưới) không thay nó, vì
  fsck kiểm một ảnh rồi để phép quét phân tích một ảnh khác, còn phép băm gắn với chính bytes được
  phân tích. Hai thứ bổ sung cho nhau, không thay nhau.
  · **Điều kiện tiên quyết toàn vẹn object-store (mới ở r6, Q9).** Toàn vẹn object-store là **NGOÀI
  phạm vi** helper A9: câu helper trả lời là *"có `lease_id` sai kiểu không"*, không phải *"kho có hỏng
  không"*. Thay cho yêu cầu băm commit, tree gốc và tree con của r5 và HINT lượt 5 (đã bị Q9 bác), lượt
  quét A9 ở kho thật phải đi kèm `git fsck --full` chạy trong **cùng lượt**, cùng kho. Handoff ghi
  lệnh nguyên văn, UTC đầu và cuối, **output nguyên văn** (rỗng thì ghi rõ "rỗng") và **rc**. rc=0 là
  điều kiện cần để phép quét được tính; rc khác 0, không chạy được, hoặc thiếu output/rc trong handoff
  ⇒ **KHÔNG ĐO ĐƯỢC** ⇒ không land. Nói thẳng, ghi cả vào handoff: điều kiện này **không nguyên tử**.
  fsck kiểm một ảnh của kho, lượt quét đọc một ảnh khác nếu kho đổi giữa chừng (ref, gói, object thêm
  hoặc bị thay), nên fsck rc=0 không chứng minh ảnh mà helper đọc là nguyên vẹn. Đó là **rủi ro được
  chấp nhận có chủ đích** của Q9, không phải khe chưa thấy. Hệ quả, để không ai đọc rộng: (a) helper
  không phải băm, không phải kiểm commit hay tree, và ca kiểm của nó không được thiết kế để bắt tree
  hoặc commit hỏng; (b) báo cáo sạch của helper chỉ nói về các cặp (đường dẫn, OID blob) như
  `ls-tree` trả và về bytes blob đã băm khớp OID ấy; nó **không** tuyên bố cạnh tree→blob hay cấu trúc
  cây là nguyên vẹn; (c) phần đó dựa vào fsck tiên quyết cộng rủi ro không nguyên tử ở trên.
  · **Ghi kết quả.** UTC, lệnh/script nguyên văn, tập ref+OID, số blob, số cặp (blob,path), số ánh xạ
  đủ ID, số từng kiểu và lỗi riêng, cộng lệnh, thời gian, output và rc của `git fsck --full`. Số kiểu và số ánh xạ tính theo cặp (blob,path); số blob ghi riêng,
  không suy hai mẫu số bằng nhau. Báo riêng miền lịch sử. Đối chiếu tên+OID với nguồn ref được cấp, không
  lấy số ref bằng nhau thay cho map bằng nhau. Offline chỉ chứng minh snapshot mirror, không khai đã đo
  máy chủ live; không truy cập được nguồn cần thiết là KHÔNG ĐO ĐƯỢC.
  · **Phân loại mã thoát.** 0 = không lỗi. 1 = lỗi lease, kèm JSON đầy đủ và `errors` khác rỗng. 2 =
  KHÔNG ĐO ĐƯỢC: lỗi Git/đầu vào, lỗi môi trường/giải mã, constructor YAML ném ngoại lệ ngoài `YAMLError`,
  vượt khả năng parser/tài nguyên, hoặc lỗi chưa phân loại. Chỉ rc=1 KÈM JSON đầy đủ mới là bằng chứng
  lỗi lease; stdout rỗng không là bằng chứng dương; lỗi chưa phân loại không được gán cho lease. Quy tắc
  áp cho lượt chạy kết thúc có kiểm soát: timeout, OS kill hoặc không đọc được output thì caller ghi
  KHÔNG ĐO ĐƯỢC, không đổi mã thoát thô thành kết luận về lease. Ca kiểm phải đi qua CHÍNH biên phân
  loại mã thoát ấy, không chỉ gọi hàm rồi tự tính một biến mang tên rc; mỗi ca ghi riêng loại ngoại lệ,
  rc và sự hiện diện JSON, không nhận "khác 0" làm đạt.
  · **Mỗi ca tự kiểm một kho Git tạm riêng.** Dựng mọi ca trong một kho có thể để lỗi ca trước làm ca sau
  đỏ, nên không chứng nhận được tính độc lập.
  Danh mục ca tối thiểu của helper (mỗi dòng là một ca; bảng lịch sử ở Phụ lục A là nguồn của danh mục):
  · Phải báo lỗi (rc=1): lease `int` ở tệp `.yml`; ID sai kiểu chỉ trên head cục bộ; ID sai kiểu chỉ ở ref
  thường `topic/HEAD`; thiếu ID; tài liệu không phải ánh xạ; YAML lỗi; `da_bi_thay_the` là list;
  `thay_the_cho: [""]`, `["   "]` và `da_bi_thay_the: "   "`; thêm ở r6: `thay_the_cho: false` và
  `thay_the_cho: 0`, `da_bi_thay_the: false` và `da_bi_thay_the: 0` (mỗi giá trị một ca; chúng KHÔNG
  phải "không có con trỏ"). Đối chứng phải qua (rc=0): chuỗi hợp lệ; `thay_the_cho: []`.
  · **Miền con trỏ tuỳ chọn (mới ở r6, từ lượt 5).** Ca dương (rc=0), **mỗi dạng một ca riêng trong
  một kho tạm riêng**, lease chuỗi hợp lệ, không thêm lỗi nào khác: `thay_the_cho` vắng; `thay_the_cho:
  null`; `thay_the_cho: ""`; `thay_the_cho: "   "` (chuỗi trắng, runtime cho ra danh sách rỗng);
  `da_bi_thay_the` vắng; `da_bi_thay_the: null`; `da_bi_thay_the: ""`. (`thay_the_cho: []` đã ở
  trên.) Không gộp các dạng vào một fixture: một ca gộp để đột biến siết sai riêng một dạng sống sót
  khi dạng khác che. Đột biến phải giết bằng `TinHieuChotCa` của đúng ca: (i) siết bác riêng từng
  dạng hợp lệ ở trên ⇒ ca dạng ấy ĐỎ (rc=1 thay vì 0); (ii) dùng kiểm truthiness chung thay cho
  phép so đúng miền (nuốt `False`/`0`) ⇒ ca âm `false`/`0` ĐỎ (rc=0 thay vì 1); (iii) dùng chung
  phép chấp nhận list cho cả hai trường ⇒ ca `da_bi_thay_the` là list ĐỎ.
  · Lỗi Git ⇒ rc=2: ref hỏng (OID toàn 0); thư mục kho không tồn tại.
  · Replace: khi `refs/replace` thay commit hoặc blob, map giữ OID chứa ID sai kiểu thì vẫn rc=1, kể cả
  khi replacement chứa chuỗi hợp lệ; đối chứng không replacement giữ nguyên kết quả.
  · Race: đổi ref từ commit ID sai kiểu sang commit chuỗi ngay sau lần liệt kê; phép quét vẫn đọc OID đã
  liệt kê và báo lỗi.
  · Cùng blob ở `ops/leases/` và `ops/leases_retired/` phải báo đúng các miền và cặp; map ref/OID có mặt.
  · Biên đầu vào và tài nguyên ⇒ rc=2: blob không phải UTF-8; ngày không tồn tại; số vượt giới hạn chuyển
  đổi; tài liệu quá sâu; nếu helper có biên dòng lệnh thì thêm thiếu/thừa argv, Git vắng, PyYAML vắng.
  Đối chứng: YAML lỗi thông thường ⇒ rc=1; tệp lease hợp lệ rất lớn ⇒ rc=0. Hàng nào của bảng Phụ lục A
  không áp dụng cho hình dạng helper thì ghi rõ lý do trong handoff, không lặng lẽ bỏ.
  · **Object-store hỏng, CHỈ ở blob (mới ở r5 từ lượt 4; thu hẹp ở r6 theo Q9).** Trên kho tạm: ref và
  tree giữ nguyên, blob mang OID của lease `int` nhưng bytes lưu dưới OID ấy là lease chuỗi hợp lệ ⇒
  rc=2, **không** 0 và **không** 1. Thiếu hẳn object blob ⇒ rc=2. Đối chứng khôi phục đúng bytes ⇒ rc=1
  (lỗi lease `int`).
  · **Tree con, tree gốc, commit hỏng: NGOÀI phạm vi helper (Q9).** Helper **không** có ca cho chúng và
  suite không đòi helper bắt chúng. Ca "tree con hỏng" của lượt 5 (tree con dưới `ops/leases` bị thay
  bytes dưới OID cũ để trỏ tới một blob chuỗi có băm đúng; `ls-tree` vẫn rc=0, không stderr, băm blob
  vẫn khớp) **không được đóng bởi helper**; nó được bắt bởi điều kiện tiên quyết `git fsck --full`
  ở trên. Bằng chứng fsck nhìn thấy lớp lỗi ấy là số **reviewer lượt 5** đo trên fixture riêng của họ
  (VERDICT lượt 5, 10:37:11Z: `fsck` rc=11 với tree hỏng ở kho loose, rc=12 ở kho packed), không phải
  số đo của phiên soạn r6 và không phải phép đo trên helper. Khe không nguyên tử nói ở bullet điều
  kiện tiên quyết vẫn còn và được chấp nhận.
  **ĐỎ khi:** đột biến gỡ từng nghĩa vụ ở trên làm đúng ca của nó ĐỎ, mỗi ca giết bằng `TinHieuChotCa`
  của chính ca ấy (cùng quy tắc A10); riêng đột biến gỡ phép băm blob làm ca object-store hỏng (ở blob)
  ĐỎ (helper trả 0 hoặc 1 thay vì 2). Đối chứng chuỗi hợp lệ phải qua. Điều kiện tiên quyết fsck **không**
  có đột biến của helper; bằng chứng của nó là dòng lệnh, output và rc trong handoff.
  Không dùng làm dụng cụ: `quet.py` nháp (bỏ qua `.yml`, thiếu ID và tài liệu không phải ánh xạ) và khối
  mã bộ quét của r4 (đã gỡ, Phụ lục A; nó còn âm giả ở ca object-store hỏng).
- **A10 (tự kiểm của bộ đột biến)** — Mỗi đột biến ở A1–A7 phải giết ca đích **bằng
  `TinHieuChotCa` của đúng ca ấy**, không bằng một ngoại lệ vô can (bài học *"ĐỘT BIẾN BỊ GIẾT
  KHÔNG PHẢI ĐỘT BIẾN BỊ GIẾT ĐÚNG LÝ DO"*). Bảng kết quả khai ba hạng: giết thật / tín dụng giả /
  sống sót.

## 8. Số đo nền (thời điểm đo cạnh từng số)

Đo lại 10:48Z–10:51Z 29-09-2026 trong container phiên soạn r6 (kho không nông: `git rev-parse
--is-shallow-repository` ⇒ `false`, 10:48Z). Số nào **đo lại ở r6** ghi giờ 10:48Z–10:51Z; số **giữ từ r5**
(10:14Z) hoặc r4 (09:44Z) ghi rõ là giữ. Số của r1, r2, r3 và của các lượt cross-review giữ dưới nhãn lịch
sử, không dùng làm số hiện tại.

- **Nền.** `git fetch -q origin '+refs/heads/*:refs/remotes/origin/*'` rồi `git rev-parse
  origin/master`, đo 09:04Z, 09:44Z (r4), 10:14Z (r5) và 10:48Z (r6; `fetch` rc=0): cả bốn lần `89fc4fac8cea65979cc2483043dc8cd07a6e8518`.
  Nền nghiệm thu không phải dời. `git diff --quiet origin/master -- ops/lease_publish.py
  ops/lease_publish_test.py` ⇒ rc=0 (10:49Z; trước đó 10:14Z và 09:46Z). Sau bước này chạy `git branch -f
  master refs/remotes/origin/master` (rc=0) để master cục bộ trùng `origin/master` `89fc4fac`, đúng điều kiện
  của mã chặn `CHẶN [12]`.
- **Ref.** `git ls-remote --heads origin` (hỏi máy chủ) so `git for-each-ref
  refs/remotes/origin` (đọc đệm), theo **tập tên**, bỏ `HEAD`, `comm -23` và `comm -13`:
  máy chủ **511**, cục bộ **512**; `comm -23` (có trên máy chủ, thiếu cục bộ) **0 dòng**; `comm -13`
  (thừa cục bộ) **1 dòng**, `claude/bookkeeping-574-land`, mà `git ls-remote --heads origin
  claude/bookkeeping-574-land` trả rỗng, rc=0 (10:48Z, sau `fetch`, `ls-remote` rc=0). Chiều lệch là **thừa
  cục bộ**: ref đệm của một nhánh đã xoá trên máy chủ (`fetch` không kèm prune), vô hại, không phải mù.
  Vì `fetch` không prune nên số cục bộ 512 lớn hơn số 510 của r5 không chứng minh có thêm nhánh nào.
  `refs/replace` hiện có 0 ref; `refs/heads` có 3 ref (đếm 10:48Z; đếm lại 10:53Z sau `branch -f master`, vẫn 3).
  Lịch sử: 503 ở r1 (06:1xZ); 505 ở r2 (07:2xZ); 506 = 506 ở r3 (07:59Z); 510 = 510 ở r4 (09:44Z) và r5 (10:14Z).
- **Người giữ** (10:48Z–10:49Z, r6). `python ops/lease_publish.py ai-dang-giu ops/lease_publish.py` ⇒
  dòng cuối `NGƯỜI_GIỮ 0: không có`, rc=0 (không có dòng `CÒN_HẠN` nào); `ai-dang-giu
  ops/lease_publish_test.py` ⇒ dòng cuối `NGƯỜI_GIỮ 1: lease-publish-windows-do-r1-g1-claude`, **rc=11**,
  đúng một dòng `CÒN_HẠN` (`refs/remotes/origin/claude/lease-publish-windows-do:ops/leases/lease-publish-windows-do-r1-g1-claude.yaml`).
  Không gặp mã chặn `CHẶN [12]`. Tệp lease ấy khai `packet_issue: 687`, `write_set:
  ops/lease_publish_test.py`, `leased_at_utc: '2026-09-29T10:20:00Z'`, `lease_expires_at_utc:
  '2026-09-30T10:20:00Z'` (đọc bằng `git show`, 10:49Z). Đây là điều kiện (1) của Q8 và nó **chưa thoả** ở
  thời điểm đo. Lịch sử 10:14Z (r5) và 09:44Z (r4): cả hai tệp `NGƯỜI_GIỮ 0`, khi lease của #687 chưa tồn
  tại. Lease T131 ở nhãn `HẾT_HẠN`: tệp lease ở `refs/remotes/origin/claude/bookkeeping-676` khai
  `lease_expires_at_utc: '2026-09-29T08:15:00Z'`. Lịch sử 07:59Z: `ai-dang-giu ops/lease_publish.py` ⇒
  `NGƯỜI_GIỮ 0`; `ai-dang-giu ops/lease_publish_test.py` ⇒
  `NGƯỜI_GIỮ 1: t131-deadline-dem-spawn-exec-1-claude-20260929`.
- **Toàn vẹn object-store của kho soạn (tham khảo, KHÔNG phải cổng).** `git fsck --full` trên
  `/home/user/tra-luat`, git 2.43.0, 10:49:12Z–10:49:26Z: **rc=0**, output rỗng (0 dòng), 13,7 giây. Đây là
  số đo của kho phiên soạn, **không** phải bằng chứng cho điều kiện tiên quyết của A9 (cái đó phải chạy ở
  kho và lượt quét của lượt land) và không nguyên tử với bất kỳ phép quét nào (Q9).
- **Miền con trỏ trong runtime** (10:49Z, chạy `_danh_sach_thay_the_cho` và `_bia_mo_doi_xung` từ blob
  `ops/lease_publish.py` của `origin/master`, sha256 `dd17b94cb880f27ba0291fa9a020c2ee3465dd55b13195f99424dfa10c834f83`,
  `PYTHONDONTWRITEBYTECODE=1`; script ở scratch, không vào kho). `_danh_sach_thay_the_cho`: `None`,
  chuỗi rỗng, chuỗi `"   "`, `[]` ⇒ `[]`; `["x"]` ⇒ `["x"]`; `[""]`, `["   "]`, `[1]`, `False`, `0`, `{}`
  ⇒ `None` (lỗi). `_bia_mo_doi_xung` (lease cũ `cu`, lease mới `moi` trỏ ngược `["cu"]`): `da_bi_thay_the`
  vắng, `None`, chuỗi rỗng ⇒ `None`; chuỗi `"   "`, `[]`, `["x"]`, `[""]`, `["   "]`, `False`, `0`, `{}`,
  `[1]` ⇒ `False`; chuỗi `"moi"` ⇒ `True`. Khớp bảng của lượt 5 (VERDICT lượt 5, hướng 4 và
  `pointer_transfer`) và khớp bullet *Schema con trỏ* ở A9.
- **Quét lease: THAM KHẢO, không phải cổng (Q7). Số giữ từ r4 (09:44Z), KHÔNG quét lại ở r5 và r6.** Số dưới
  do khối mã bộ quét của r4 tạo ra (blob r4: sha256 `2726d59f…17f2`, commit `a9019a9`); khối mã đã gỡ
  khỏi r5 theo §9. Không dùng chúng thay A9 và không đặt chúng làm cổng cấp lease hay land: bộ quét ấy
  còn âm giả với object-store hỏng (Phụ lục A, phát hiện của lượt 4). Lệnh lịch sử, qua entry point:
  `PYTHONDONTWRITEBYTECODE=1 python3 quet_r4.py /home/user/tra-luat`, JSON `utc`
  `2026-09-29T09:44:23.898266+00:00`, rc=0: `ref_count` **512** (510 `refs/remotes` + 2
  `refs/heads`), `blob_count` **563**, `pair_count` **563**, `mapping_count_pairs` **563**,
  `id_count_pairs` **563**, `type_counts_pairs` `{str: 563}`, `areas`: `ops/leases` 563 blob /
  563 cặp, `ops/leases_retired` 0 blob / 0 cặp, `errors` **0**.
  `ops/leases_retired` = 0 trên mọi ref là số **đo** ở 09:44Z, không phải giả định.
  Lịch sử r3 (07:59:26Z, khối mã r3): rc=0, `ref_count` 508 (506 + 2), 562 blob / 562 cặp /
  562 ánh xạ / 562 có ID, `{str: 562}`, `errors` 0. Chênh r3 → r4: ref +4 (đều `refs/remotes`,
  khớp 506 → 510 của `ls-remote`), blob +1; vì sao 4 ref mới chỉ thêm 1 blob thì chưa truy nguyên
  (`KHÔNG ĐO ĐƯỢC`, không đổi kết luận vì mọi `lease_id` đều là chuỗi). Lịch sử xa hơn: 559 ở r1
  và lượt 1; 560 ở r2 (sau `fetch` 07:21Z), khi hai nhánh đẩy sau lượt `fetch` trước đó
  (`ops/cap-lease-ci-duong-nhanh-ho-so`, `ops/cap-lease-ci-g5-cong-cu-chia-manh`) mỗi nhánh thêm
  một tệp lease so với master mà tổng chỉ tăng 1 blob. Đây là trôi số của L5 xảy ra ngay trong
  lúc soạn, và nó lặp lại ở r4. Số của **reviewer lượt 5** trên ảnh mirror họ được cấp (không phải số
  của phiên soạn, không có UTC riêng cho phép đo, VERDICT lượt 5 bảng đo): 513 ref = 512 + 1 cục bộ; 564
  blob / 564 cặp; kiểu `str` 564; `invalid` rỗng; `bad_hash` rỗng; `ops/leases_retired` 0/0. Khác ảnh và khác
  thành phần ref với số r4, nên không so trực tiếp; cả hai cùng cho mọi `lease_id` là chuỗi. Vẫn là tham
  khảo, không phải cổng.
- **Suite.** Nền hiện tại: **187/187**, rc=0, bỏ qua 0, đo 08:0xZ 29-09 trên commit merge
  `589336f` (cây `89fc4fa` + tệp spec), `PYTHONDONTWRITEBYTECODE=1 python ops/lease_publish_test.py`
  với `shellcheck` 0.9.0 + `actionlint` 1.7.7. Không đo lại ở r4, r5 và r6 (hai tệp Python giống hệt
  `origin/master`, `git diff --quiet` rc=0 lúc 10:49Z, xem mục **Nền**). Reviewer lượt 4 tự đo
  187/187, rc=0, bỏ qua 0 (VERDICT lượt 4, không ghi UTC riêng cho phép đo này); reviewer lượt 5 tự đo
  187/187, rc=0, bỏ qua 0 (VERDICT lượt 5, `verify.py` 10:42:51Z).
  Lịch sử trên `1741e0a`: r1 khai 185/187 lúc container thiếu `shellcheck` (`t137`, `t159` báo
  `KHÔNG ĐO ĐƯỢC: thiếu shellcheck`); lượt 1 đo 187/187.
- **Kích thước** (đo lại 10:51Z, `git show origin/master:<tệp> | wc -l`, kết quả bằng số đo 10:14Z). `ops/lease_publish.py` 2206
  dòng (không đổi giữa hai nền); `ops/lease_publish_test.py` **10502** dòng trên `89fc4fa`
  (10508 trên `1741e0a`); 187 ca, số ca lớn nhất `t192` (đo 08:0xZ, không đo lại).
- **Ruff**: vẫn `KHÔNG ĐO ĐƯỢC` ở phiên soạn (module vắng trong sandbox);
  A8 bắt lượt thi hành đo cả hai vế.

Mọi con số trên phải được **đo lại** trước mỗi bước công bố: đăng băm/revision, cấp lease
và land (L5). Ghi thời điểm đầy đủ và lệnh cạnh số mới; giữ số cũ với nhãn lịch sử nếu cần.
Quyết định neo vào **bất biến** (mọi `lease_id` là chuỗi; không lease nào còn hiệu lực giữ hai
tệp của write set lúc cấp), không neo vào con số 510/511/563. Theo Q7, bất biến thứ nhất được **đo bằng A9
lúc land**, không bằng số quét ở §8.

## 9. `hinh_dang_ke_thua`

`khong_ap_dung`: đây không phải packet khắc phục một lượt thất bại. Nguồn là một phát hiện phụ
của #677, không kèm bộ đếm hình dạng lỗi nào.

Rủi ro hình dạng đã biết, ghi để lượt thi hành canh: *"VÁ ĐÚNG CHỖ ĐƯỢC CHỈ RỒI BỎ SÓT ĐƯỜNG THỨ
BA"*. §2 liệt kê 8 đường sửa (D1–D8) cộng D9 chỉ hiển thị; lượt thi hành phải **grep lại** chứ không tin bảng này là
đủ, và khai đường nào mới tìm thấy.

**Bộ đếm hình dạng (phát sinh trong chuỗi review của chính đặc tả này).** Lớp `bo-quet-*`, tức
bộ quét tham chiếu (từng nằm ở Phụ lục A, đã gỡ mã ở r5), có mặt ở **cả 5 lượt** review (đếm hình dạng, đừng chỉ đếm lỗi):

| lượt | bản được review | biểu hiện của lớp `bo-quet-*` |
|---|---|---|
| 1 | r1 | thiếu miền |
| 2 | r2 | thiếu miền; không neo ảnh; không có cửa chạy |
| 3 | r3 | không neo ảnh (`git replace`); cửa chạy phân loại lỗi còn hở |
| 4 | r4 | không neo ảnh: bytes blob có thể mang băm khác OID đã liệt kê dù `cat-file` rc=0 (object-store hỏng dựng chủ ý); replace, race và phân loại CLI cũ đã đóng |
| 5 | r5 | hai lớp, 0 P1 / 2 P2 / 0 P3. `bo-quet-chung-cu-khong-neo-anh`: băm blob đúng vẫn không bảo chứng cạnh tree→blob, vì tree con bị đổi bytes dưới OID cũ vẫn cho `ls-tree` rc=0 (loose và packed; fsck của reviewer bắt được). `bo-quet-nghiem-thu-thieu-mien`: bullet *Schema con trỏ* của r5 làm mất `null` và chuỗi rỗng, đã được runtime nhận, khi thay mã bằng văn xuôi (tái phát **do chính việc chuyển giao**) |

Mỗi bản vá đều đúng chỗ được chỉ, và lần nào lượt sau cũng ra một biểu hiện khác của cùng lớp.
r4 vá đúng hai biểu hiện lượt 3 chỉ ra (tắt replace ở mọi lệnh Git; một biên CLI phân loại
mọi lỗi chưa biết thành `KHONG_DO_DUOC`, rc=2) và chạy thật mọi ca ở Phụ lục A; đó là bằng chứng
cho hai biểu hiện ấy, **không** phải lời khai rằng lớp đã sạch.

**Hình dạng đếm được ở lượt 5, và cái chặn nó.** Biểu hiện `không neo ảnh` có mặt ở **bốn lượt liên
tiếp (2, 3, 4, 5)**, và mỗi lần vá đưa ta xuống **một tầng sâu hơn của đồ thị object**: lượt 2 chưa neo
ảnh (mức đầu, theo bảng trên), lượt 3 `git replace`, lượt 4 bytes blob, lượt 5 tree con.
Đó là bệnh *"VÁ ĐÚNG CHỖ ĐƯỢC CHỈ RỒI BỎ SÓT ĐƯỜNG THỨ BA"* ở dạng cầu thang: vá đúng tầng được chỉ,
tầng dưới luôn còn. Cùng hình dạng lặp ba lần trở lên thì câu hỏi đúng là *"có nên làm việc này không"*,
không phải *"vá thế nào"* (bài học *"BẢY phát hiện cùng MỘT đường"* của CLAUDE.md). **Q9 (§3) là quyết định chặn chuỗi đào sâu ấy bằng cách đổi câu hỏi**:
helper trả lời *"có `lease_id` sai kiểu không"*, còn *"kho có hỏng không"* dời sang một điều kiện tiên
quyết (`git fsck --full`, không nguyên tử, rủi ro được chấp nhận). Nó **không** phải lời khai rằng tầng
tree đã được kiểm: nó là quyết định không kiểm ở helper. Lớp `bo-quet-nghiem-thu-thieu-mien` cũng có
mặt ở lượt 1, 2 và 5 (ba trên năm lượt); ở lượt 5 nó tái phát vì r5 chuyển nghĩa vụ từ mã sang văn xuôi
và văn xuôi mất các ngoại lệ mà mã mang ngầm. r6 chữa bằng cách ghi miền theo CHÍNH hành vi runtime
kèm số dòng (A9) và bằng một ca dương riêng cho mỗi dạng hợp lệ, không bằng một câu "giữ nguyên".

**Điều kiện dừng, đã đăng ký trước** trên PR #679 (comment `5887068702`): nếu lượt 4 còn ra
một lớp `bo-quet-*`, thì r5 **GỠ mã bộ quét khỏi đặc tả**; §8 hạ số quét xuống "tham khảo,
không phải cổng"; cổng là helper A9 có ca kiểm trong `ops/lease_publish_test.py`.

**Điều kiện dừng ĐÃ KÍCH HOẠT ở lượt 4** (comment `5888141866`: 0 P1 / 1 P2 / 0 P3, lớp
`bo-quet-chung-cu-khong-neo-anh`). r5 làm đúng điều đã đăng ký: (1) gỡ khối mã bộ quét khỏi Phụ lục A và
không vá tiếp nó; (2) hạ số quét ở §8 thành "tham khảo, không phải cổng"; (3) cổng là helper A9 có ca
kiểm trong `ops/lease_publish_test.py`, và theo Q7 (§3) cổng ấy **chỉ đặt trước land**. Phần HINT lượt 4
đòi bên cấp việc bàn giao dụng cụ đo độc lập trước cấp lease, chưa có thì DỪNG cấp, **không được áp**:
Q7 đã bác.

**Gỡ mã KHÔNG tự đóng finding lượt 4.** Sau r5 đặc tả không còn dụng cụ quét nào, nên finding không còn
chỗ để sai trong mã ấy, nhưng cũng chưa có gì chứng minh nó đã đóng. Nó được **chuyển** thành nghĩa vụ của
helper A9 (phép băm blob trên chính bytes đưa vào parser, và ca object-store hỏng **ở blob** của A9).
Nhãn đúng cho tới lúc helper có mặt và ca ấy chạy là "chuyển giao", không phải "đã đóng". r5 cũng không phải lời khai
rằng lớp `bo-quet-*` đã sạch: đó là quyết định thôi vá tiếp một dụng cụ đã sinh ra biểu hiện mới ở cả
bốn lượt.

**Phần HINT lượt 5 áp và không áp ở r6.** Nhóm `bo-quet-nghiem-thu-thieu-mien` **được áp** (vắng, `null`,
chuỗi rỗng hợp lệ; `False`/`0` không đồng nhất với chúng; danh sách phần tử trắng và `da_bi_thay_the` là
list vẫn lỗi; ca dương riêng cho từng dạng). Nhóm `bo-quet-chung-cu-khong-neo-anh` **không được áp**:
nó đòi băm toàn chuỗi commit, tree gốc, tree con và blob, mà Q9 bác. Đây là hai xử lý khác nhau cho hai
lớp trong cùng một VERDICT, không phải chọn lọc tuỳ ý. Lớp `bo-quet-chung-cu-khong-neo-anh` ở lượt 5
mang nhãn **"ngoài phạm vi theo Q9, bắt bởi điều kiện tiên quyết fsck"**, không phải "đã đóng".

## 10. `chua_do_duoc`

- Mã thực thi chưa tồn tại, nên mọi tiêu chí A1–A10 mới được kiểm **khả thi**: hai lượt
  cross-review đã dựng mô hình chốt tạm trên bản sao để kiểm A1–A10; vẫn **chưa có ứng viên
  thật**.
- **Helper A9 chưa tồn tại** (do executor viết sau khi có lease, Q7). Đặc tả này không còn dụng cụ quét
  nào; mọi bảng ca ở Phụ lục A là hồ sơ lịch sử của bộ quét r4 đã gỡ. Finding lượt 4 (blob sai băm vẫn
  báo sạch) **chưa được đóng bởi dụng cụ nào**: nó chuyển thành ca bắt buộc "object-store hỏng, chỉ ở
  blob" của helper (A9). Chưa có bằng chứng dương nào cho ca ấy trên helper. Finding lượt 5 về tree con
  **không** chuyển cho helper (Q9); điều kiện tiên quyết `git fsck --full` cũng chưa có lần chạy nào ở
  lượt land thật (số fsck ở §8 là của kho phiên soạn, không thay nó).
- Đường `DU_BAO`: lượt 1 đo được `ai-dang-giu --du-bao` đưa `int` tới :1967 (không qua D1).
  `check --du-bao` sau D1: chưa đo trên ứng viên. A7 bắt đo cả hai.
- Ruff: `KHÔNG ĐO ĐƯỢC` ở phiên soạn và ở mọi lượt review.
- Băm thân Mission Issue #682 ở phía nhận: `KHÔNG ĐO ĐƯỢC` (đường đọc MCP chuẩn hoá thực thể
  HTML); descriptor neo bằng số Issue + object ID `5627190292`.
- Lease T131 còn giữ `ops/lease_publish_test.py` là trạng thái đo 07:59Z 29-09 (lịch sử); đo 09:44Z và
  10:14Z cả hai tệp `NGƯỜI_GIỮ 0` và lease T131 ở nhãn `HẾT_HẠN`. **Đo 10:48Z–10:49Z (r6):**
  `ops/lease_publish_test.py` do lease `lease-publish-windows-do-r1-g1-claude` (#687) giữ tới
  `2026-09-30T10:20:00Z`, nên điều kiện cấp (1) của Q8 chưa thoả. Người giữ có thể đổi bất kỳ lúc nào;
  vẫn phải đo lại (`ai-dang-giu`, kèm so tập tên ref) lúc cấp lease cho `wp678`. Chưa đo được: #687 có
  land trước hay không và có đổi `ops/lease_publish_test.py` hay không (điều kiện 4 của Q8); nếu có thì
  cần revision mới dời nền.
- **Rủi ro được chấp nhận của Q7 (không phải finding).** Trước khi bản vá này land, `ai-dang-giu` hiện
  hành có thể coi một cặp bia mộ dùng ID kiểu `int` là đối xứng (ép `str()` ở :587/:592 làm `1000` và
  `"1000"` trùng nhau): reviewer lượt 5 (hướng 6, 10:31:47Z) dựng lease cũ còn hạn `da_bi_thay_the: "1000"`
  và lease đối ứng `lease_id: 1000` (int) trỏ ngược; nền trả rc=0 / `NGƯỜI_GIỮ 0`, mô hình Q3 nghiêm trả
  rc=12. Kho thật **không** có ID nào như thế: 0 `lease_id` sai kiểu trên 563 cặp (đo 09:44Z, r4, §8) và
  `str` 564/564 trên ảnh của reviewer lượt 5. Cửa sổ ấy tồn tại vì Q7 chỉ đặt A9 trước land, không đặt
  cổng kiểu trước cấp lease: **đó là rủi ro được chủ kho chấp nhận có chủ đích ở Q7**, không phải khe
  chưa thấy, và r6 không khôi phục cổng trước cấp.
- Bộ quét lịch sử r4 (mã đã gỡ): các ca ở hai bảng Phụ lục A đã CHẠY (28 ca CLI của r4 không lệch mong
  đợi, cộng 1 ca race gọi `quet()` trực tiếp). Còn `KHÔNG ĐO ĐƯỢC`: timeout, OS kill, hết bộ nhớ; Python
  khác 3.11.15; PyYAML khác 6.0.1; ngưỡng độ sâu và kích thước (chỉ thử 5000 lớp và 400026 byte).
  Script và output của các phép đo ở thư mục scratch của phiên soạn, không vào kho. Các bảng ấy **không
  chứng minh toàn vẹn blob** (xem phát hiện lượt 4 ở cuối Phụ lục A), nên không được nhận làm bằng chứng
  thay A9.
- Tệp `ops/specs/dot-bien-l-bien-cong-khai-r1.md` của #677 có trên nhánh
  `claude/spec-dot-bien-l-bien-cong-khai-20260929` (đo 09:45Z); trạng thái đóng băng và lease
  của nó không đo ở lượt này (xem A2).
- Trạng thái máy chủ GitHub ngoài `ls-remote`: không đo (REST tới `repos/…` bị proxy chặn).
- Q3 đã được chủ kho xác nhận (#678 comment `5885268193`); không còn là câu hỏi mở.

## Phụ lục A — hồ sơ lịch sử bộ quét tham chiếu (đã gỡ mã theo §9)

Bộ quét tham chiếu của r2–r4 từng nằm ở đây dưới dạng một khối mã Python. Nó là công cụ của phiên soạn,
**không** phải mã sản phẩm, và theo điều kiện dừng ở §9 (đã kích hoạt ở lượt 4) r5 **đã gỡ khối mã**;
không chép lại nó vào revision sau dưới tên khác. Ai cần tái lập lịch sử thì đọc blob của r4 (sha256
`2726d59ffb683f44e68c1409241250c40025bc02a9c9bfb257e767831a1e17f2`, commit `a9019a9`) hoặc của r3
(sha256 `64c67225…4af1`, commit `4c1915c`); định danh là băm và commit, không phải tên nhánh. Đó là đọc
để hiểu lịch sử, **không** dùng làm cổng: khối mã r4 còn âm giả ở ca object-store hỏng (cuối phụ lục).

Các nghĩa vụ chứng cứ (neo ảnh theo OID, tắt Git replace, bytes khớp OID, phân loại 0/1/2, mỗi ca một
kho tạm riêng) nay nằm ở **A9**. Hai bảng dưới đây chỉ là hồ sơ LỊCH SỬ của những gì r4 đã đo, và là nguồn
của danh mục ca mà helper A9 phải có; vì mục đích ấy **không ca nào bị xoá**.

**Lịch sử.** Bảng r2 (đo 07:28Z 29-09) là lời khai không tái lập được (r2 không công bố wrapper
sinh mã thoát). Bảng r3 (07:5xZ 29-09) có 15 ca CLI cộng 1 ca race, cả 15 ca CLI khớp mong đợi;
15 ca ấy được chạy lại nguyên ở r4 và cho cùng rc và cùng loại lỗi. Bảng r3 không có ca replace,
argv, Git/PyYAML vắng, giải mã, ngày, số, độ sâu; hai P2 của lượt 3 nằm đúng ở các miền đó.

**Phép đo 1 — CLI (LỊCH SỬ r4).** Đo 09:43:32Z–09:43:37Z 29-09 (Python 3.11.15, PyYAML 6.0.1, git 2.43.0).
Khối mã của r4 (blob nêu ở đầu phụ lục) được trích đúng byte ra `quet_r4.py`; script `tukiem_r4.sh`
(mở rộng từ `tukiem_r3.sh`) chạy `python3 quet_r4.py <kho>` cho từng dòng, **mỗi ca một kho git
tạm riêng** (dựng mọi ca trong một kho có thể để lỗi ca trước làm ca sau đỏ, nên không dùng cách
đó để chứng nhận ca độc lập). Output gốc: `tukiem_r4.out`. Script và output nằm ở thư mục scratch
của phiên soạn, **không** vào kho. 28 ca của r4 (15 kế thừa + 13 mới) và 2 lần chạy khối mã r3
trên kho replace làm đối chứng độ răng. Mọi dòng có rc=2 đều có stdout rỗng, không JSON, và
dòng stderr `KHONG_DO_DUOC: <Loại>`.

| ca | mong | được (rc, JSON?, errors hoặc loại lỗi) |
|---|---|---|
| đối chứng: một lease chuỗi hợp lệ | 0 | 0, JSON, `errors` rỗng |
| `lease_id: 1_000` trong tệp `.yml` | 1 | 1, JSON, `lease_id=1000` |
| thiếu `lease_id` | 1 | 1, JSON, `thieu_lease_id` |
| tài liệu là danh sách | 1 | 1, JSON, `khong_phai_anh_xa` |
| YAML hỏng | 1 | 1, JSON, `parse` |
| `da_bi_thay_the: [x]` | 1 | 1, JSON, `da_bi_thay_the` |
| `thay_the_cho: [""]` | 1 | 1, JSON, `thay_the_cho` |
| `thay_the_cho: ["   "]` | 1 | 1, JSON, `thay_the_cho` |
| `da_bi_thay_the: "   "` | 1 | 1, JSON, `da_bi_thay_the` |
| `thay_the_cho: []` (hợp lệ) | 0 | 0, JSON, `errors` rỗng |
| `lease_id: on` chỉ trên head cục bộ | 1 | 1, JSON, `lease_id=True`, `ref_count` 2 |
| `lease_id: yes` chỉ trên ref thường `topic/HEAD` | 1 | 1, JSON, `lease_id=True`, `ref_count` 2 |
| cùng blob ở `ops/leases` và `ops/leases_retired` | 0 | 0, JSON; blob 1, cặp 2; mỗi miền 1 blob / 1 cặp |
| ref hỏng (OID toàn 0) | 2 | 2, không JSON, `KhongDoDuoc` (git for-each-ref) |
| thư mục kho không tồn tại | 2 | 2, không JSON, `KhongDoDuoc` |
| **replace commit**: `main` trỏ commit X (`lease_id: 1_000`), `git replace X Y` với Y mang `lease_id` chuỗi hợp lệ (`refs/replace` có 1 ref) | 1 | 1, JSON, `lease_id=1000` |
| đối chứng, cùng kho, **khối mã r3** (không tắt replace) | r3 âm giả | 0, JSON, `errors` rỗng (đúng âm giả lượt 3 nêu) |
| đối chứng, cùng dựng nhưng KHÔNG replace | 1 | 1, JSON, `lease_id=1000` |
| **replace blob**: blob chứa `lease_id: 1_000` bị `git replace` bằng blob sạch | 1 | 1, JSON, `lease_id=1000` |
| đối chứng, cùng kho, **khối mã r3** | r3 âm giả | 0, JSON, `errors` rỗng |
| thiếu argv (không đối số) | 2 | 2, không JSON, `KhongDoDuoc` (cách dùng) |
| thừa argv (2 đối số) | 2 | 2, không JSON, `KhongDoDuoc` (cách dùng) |
| PyYAML vắng (`yaml.py` giả ném `ImportError` đặt ở `PYTHONPATH`) | 2 | 2, không JSON, `ImportError` |
| git vắng (`PATH` là thư mục rỗng, python gọi bằng đường dẫn tuyệt đối) | 2 | 2, không JSON, `FileNotFoundError` |
| blob không phải UTF-8 (`lease_id: ` rồi hai byte 0xFF 0xFE, dựng bằng `printf`) | 2 | 2, không JSON, `UnicodeDecodeError` |
| `lease_id: 2026-02-30` (ngày không tồn tại) | 2 | 2, không JSON, `ValueError` (day is out of range for month) |
| `lease_id` là số 5000 chữ số | không định trước; HINT dự kiến 2 | 2, không JSON, `ValueError` (Exceeds the limit (4300 digits) for integer string conversion) |
| tài liệu 5000 lớp `[` lồng nhau | không định trước; HINT dự kiến 2 | 2, không JSON, `RecursionError` |
| đối chứng: YAML lỗi thông thường (`lease_id: [`) | 1 | 1, JSON, `parse` |
| đối chứng: tệp lease hợp lệ 400026 byte (khoá `ghi_chu` dài) | 0 | 0, JSON, `errors` rỗng |

**Không có ca nào lệch mong đợi** (0/28 ca r4; hai lần chạy khối mã r3 cho 0 đúng như lượt 3
báo). Giới hạn của phép đo: ngưỡng 4300 chữ số là của CPython 3.11 và `RecursionError` phụ thuộc
giới hạn đệ quy mặc định, chưa đo phiên bản Python khác; chưa thử timeout, OS kill hay hết bộ
nhớ (caller phải coi output thiếu là KHÔNG ĐO ĐƯỢC, xem trên); độ sâu chỉ thử 5000 lớp và kích
thước chỉ thử 400026 byte, không suy ra ngưỡng.

**Phép đo 2 — race (LỊCH SỬ r4).** Đo 09:43:57Z 29-09. Script `race_r4.py` nạp `quet_r4.py`, dựng kho tạm
(`main` trỏ commit `lease_id: 1_000`, một commit sạch riêng), chèn `git update-ref` vào hàm
`git` của module ngay sau lần `for-each-ref` đầu tiên, rồi gọi `quet()` **trực tiếp**. Đây là
phép đo tại seam: nó **không** chứng minh mã thoát CLI và không nằm trong `tukiem_r4.sh`. Output
gốc: `race_r4.out`, cùng thư mục scratch, không vào kho.

| ca | mong | được |
|---|---|---|
| ref đổi sang commit sạch NGAY SAU `for-each-ref` (seam, gọi `quet()` trực tiếp) | map giữ OID cũ; `errors` có `lease_id=1000` | seam đã chèn; ref đã sang commit sạch `8dce401e`, nhưng `refs` vẫn giữ OID cũ `cdeca03d` và `errors` = `lease_id=1000` |

Lần chạy đầu của `race_r4.py` (09:43:53Z) in `False` ở dòng tự kiểm cuối vì script so tuple với
list, một lỗi của chính phép so trong script chứ không phải của khối mã (map và `errors` đã
đúng ở lần đó); phép so được sửa và chạy lại, `race_r4.out` là output của lần chạy lại.

**Ghi chú r6 về miền con trỏ.** Bảng CLI ở trên **không có** ca dương cho `thay_the_cho` vắng, `null`,
chuỗi rỗng, chuỗi trắng, hay `da_bi_thay_the` vắng, `null`, chuỗi rỗng: đó là chỗ hở mà lượt 5 chỉ ra.
Theo `pointer_transfer` của reviewer (10:32:52Z, chạy trên khối mã r4), khối mã r4 nhận `None` và chuỗi
rỗng ở cả hai trường (rc=0); số ấy là của reviewer, không phải bảng r4 và không phải đo của phiên soạn.
Các ca dương thiếu được đưa vào danh mục A9 ở r6 (mỗi dạng một ca), cùng hai ca âm `false`/`0`.

Ca ref hỏng (OID toàn 0) là lý do bộ quét r4, và nay là helper A9, phải đọc `stderr` chứ không chỉ `rc`: git **bỏ lặng lẽ** một ref hỏng và vẫn
trả 0, tức một phép quét "mọi ref" có thể quét thiếu mà không báo.

**Phát hiện của lượt 4: chưa có dụng cụ nào đóng nó; helper A9 phải đóng.** Reviewer lượt 4 dựng
object-store hỏng có chủ ý (không tạo va chạm SHA, không sửa kho nguồn) và thấy bộ quét r4 báo sạch. Tái
lập ở phiên soạn r5, đo 10:16Z 29-09 (Python 3.11.15, PyYAML 6.0.1, git 2.43.0; kho tạm object format
sha1, mỗi ca một kho tạm riêng; bytes khối mã r4 khớp blob r4, `cmp` rc=0). Script `objr5.py` và output
nằm ở scratch của phiên soạn, không vào kho. Bộ quét r4 **không** bị sửa để chạy phép đo này.

| ca | hợp đồng A9 đòi | bộ quét r4 được |
|---|---|---|
| đối chứng: blob `lease_id: 1000` nguyên vẹn | 1 | 1, JSON, `lease_id=1000` |
| ghi đè object blob bằng bytes `lease_id: good-id` dưới ĐÚNG OID cũ (ref và tree giữ nguyên) | **2** (KHÔNG ĐO ĐƯỢC) | **0**, JSON, `errors` rỗng, `refs` bằng đối chứng; `cat-file blob` rc=0; băm bytes đã đọc `13e1d8b3…` khác OID đã liệt kê `0a0253c7…`; `git fsck --full` rc=3 |
| khôi phục đúng bytes gốc | 1 | 1, JSON, `lease_id=1000`; `git fsck --full` rc=0 |
| xoá hẳn object blob | 2 | 2, không JSON, `KhongDoDuoc` (git cat-file) |
| ghi đè object tree bằng một tree rỗng đã nén, dưới OID cũ | **ngoài phạm vi helper (Q9)**; điều kiện tiên quyết fsck | 2, không JSON, `KhongDoDuoc` (git ls-tree): hành vi của bộ quét r4 trên đúng fixture này, không phải nghĩa vụ của helper |

Dòng thứ hai là âm giả: rc=0 kèm JSON đầy đủ và `errors` rỗng, trong khi bytes đã phân tích không mang
OID có trong map. Dòng "xoá hẳn object blob" thuộc hợp đồng helper (rc=2). Dòng tree hỏng chỉ ghi lại rằng, trên đúng
fixture ấy (một tree rỗng), Git từ chối ở `ls-tree`; nó **không** chứng minh Git tự từ chối MỌI tree
hỏng, và **không** đặt cho helper nghĩa vụ kiểm tree. Lượt 5 đã cho thấy chiều ngược lại: tree con bị đổi
bytes dưới OID cũ để trỏ tới một blob chuỗi có băm đúng thì `ls-tree` vẫn rc=0, không stderr, băm blob
vẫn khớp (VERDICT lượt 5, `tree_probe`, 10:37:11Z; loose và packed; không phải số đo của phiên soạn).
Theo Q9, ca đó **ngoài phạm vi** helper A9 và được bắt bởi điều kiện tiên quyết `git fsck --full`
(reviewer đo rc=11 ở loose, rc=12 ở packed), với khe không nguyên tử đã được chấp nhận (A9). Dòng blob sai
băm thì Git **không** tự báo, đó là lý do A9 đòi băm blob trên chính bytes đã đọc. Commit hỏng: VERDICT
lượt 4 đo Git tự từ chối (bộ quét ra 2); ca ấy không được tái lập ở r5 và r6, và cũng ngoài phạm vi
helper theo Q9. Đây là dụng cụ hỏng trên fixture dựng chủ ý, **không**
phải lời khai rằng kho thật có object hỏng: reviewer lượt 4 băm mọi blob của snapshot đã quét và thấy
khớp (VERDICT lượt 4), phép đo ấy cũng không được tái lập ở r5.
