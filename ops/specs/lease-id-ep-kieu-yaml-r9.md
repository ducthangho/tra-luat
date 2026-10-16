# ĐẶC TẢ — `LEASE-ID-EP-KIEU-YAML` — **revision 9, ĐÓNG BĂNG**

**Thay đổi so với r8** (theo review lượt 8 trên r8 và Q12, nay thêm vào §3). Mục tiêu (hàng `objective`), write set
(§4), nền nghiệm thu và ngữ nghĩa A1–A10 **không đổi**. Q12 đổi hai giá trị closure (vế review của `required_checks`,
`land_obligations`), nên đây là revision mới theo luật miễn trừ ở #682:

| chỗ | r8 | r9 |
|---|---|---|
| reviewer lượt thi hành | `claude -p` qua `launcher.py run` (phương án B, do phiên soạn r8 tự chọn), mức `same_provider_approved` khi đủ bằng chứng | subagent `review-opus-max` (cấu hình Opus 5.5 `max`) trong phiên điều phối, mức `review_deferred`, land bằng `human_audited` (Q12); bỏ mọi lời khai "phiên mới" hay độc lập |
| closure | `required_checks` ghi "review Claude Opus 5.5 `max`"; `land_obligations` ghi "Chủ kho audit + merge" | `required_checks` ghi review subagent mức `review_deferred` kèm biên nhận khai `che_do`; `land_obligations` ghi rõ mức `human_audited` (Q12) |
| ghi chú dưới closure | năm tiêu chí (a)–(e) cho đường B | bốn tiêu chí cho đường subagent, kiểm được bằng `_thieu` và băm; băm định nghĩa ghim CẤU HÌNH, không phải nguồn đo runtime |
| `depends_on` | (3) là revision 8; (4) dời nền chỉ khi #687 land | (3) là revision 9; (4) tổng quát hoá: BẤT KỲ packet nào land đổi một tệp write set sau nền ⇒ dời nền, đo bằng `git diff --quiet <nền> origin/master -- <write set>` lúc cấp; đo lại 05:17Z 01-10: lease #687 generation 3 đang giữ `ops/lease_publish_test.py` |
| §3 | Q1–Q11 | thêm Q12, trích nguyên văn; ghi chú Q10 về điều kiện (3) |
| §4, §6, A2, A3, A8 | không nêu kiểm kê `t70` | nghĩa vụ cập nhật tập literal `mong` của `t70` (trong write set), §6 mục 8; phiên soạn r9 đo lại đột biến |
| dòng dõi, §8, §9, §10 | r7, Q11 | r8, review lượt 8, Q12; §8 đo lại nền, ref, người giữ; §9 bộ đếm sau lượt 8 và cách áp HINT lượt 8; §10 trạng thái ba lớp của đường review |

Bảng thay đổi r7 → r8 nằm ở đầu r8 (xem `thay_the_cho`).

| trường | giá trị |
|---|---|
| `schema_version` | 1 (protocol §3.2) |
| `packet_id` | `wp678` (ID bền theo protocol §3.2, `wp<issue>`); tên đọc được: `LEASE-ID-EP-KIEU-YAML`. Hai tên chỉ cùng một packet; lease dùng `wp678` hoặc tên đọc được đều phải kèm `packet_issue: 678`. |
| `revision` | **9** |
| `thay_the_cho` | revision 8: `ops/specs/lease-id-ep-kieu-yaml-r8.md`, sha256 `f173e7cf2f132dacdf34d9ab00cc966a5a7d5705baffcc585d577beed5ee5a3b`, commit `f958e147754bed8e9e7034dd28450681f19c3db0` (cha `088511f`). Đây là commit TẠO tệp: trong worktree soạn r9, `git log --diff-filter=A --format=%H -- <tệp>` ra giá trị ấy, đúng 1 commit chạm tệp, và `sha256sum` trên output của `git show f958e14:<tệp>` ra đúng băm trên (890 dòng; 05:28:57Z 01-10). Định danh r8 là băm và OID, không phải tên nhánh: lúc soạn r9 commit ấy **chưa** có trên GitHub (clone `adg2` sau `fetch --prune` 05:17:33Z 01-10, `git cat-file -t` báo không có object), nên tra theo OID, trên GitHub nếu đã đẩy, chưa thì ở nhánh `claude/spec-wp678-r7` của phiên điều phối. r8 được review lượt 8 (subagent trong phiên điều phối, model/effort tự khai Claude Opus 5.5 `max`, trên `f958e14`): `changes_requested`, 0 P1 / 4 P2 / 3 P3 theo lớp; VERDICT sha256 `68da880f92f5afd4ba2fa31ed89265e31d083f11aecce79a501ccbab3352fe82`, HINT sha256 `41e3763cedde5ae1e9d8de2f5ddcbda345428f696cc5a69d35cf3fc57aaca400`; bản chiếu ở #678 comment `5925164956`. Chuỗi r1–r7: xem hàng `thay_the_cho` của r8 (r7 `8cb02436…b707`, commit `088511f`, review lượt 7 `changes_requested`). |
| `packet_issue` | **#678** |
| `mission_issue` | **#682** (Mission Issue, object ID `5627190292`, tạo 29-09-2026, tiêu đề *"Mission wp678: quyết định chủ kho + miễn trừ closure có phạm vi cho LEASE-ID-EP-KIEU-YAML"*). Issue này do **phiên agent đăng HỘ chủ kho** bằng credential chủ kho, nên `author_association: OWNER` không chứng minh chủ kho tự gõ; nguồn thẩm quyền là các câu trả lời của chủ kho trong phiên (Q0–Q6) được trích trong thân #682; Q7 do chủ kho chốt sau đó và ghi ở #682 comment `5888143430`; Q8 ở #682 comment `5888631719`; Q9 ở #682 comment `5888660607`; Q10 ở #682 comment `5911243074`; Q11 ở #682 comment `5912559230`; Q12 ở #682 comment `5925190705` (xem §3). Packet cha #579 (đặc tả `ops/specs/dang-lease-dau-truoc-kiem-sau-r30.md`) không khai `mission_issue` và không cấp ngoại lệ gì cho packet này. |
| `nguon_cap_viec` | Phát hiện phụ của #677 (mục *"Phát hiện phụ — TÁCH packet riêng"*). Chủ kho quyết định tách packet 29-09-2026, rồi trả lời *"Đồng ý"* trong phiên cho ba đề xuất: (a) mở Issue + soạn đặc tả; (b) chỉ nhận **chuỗi thật**, bỏ cả `int`; (c) xếp sau `T131-DEADLINE-DEM-SPAWN`. Q3 xác nhận riêng: #678 comment `5885268193`. **r2** là hệ quả của cross-review lượt 1 trên PR #679 (comment `5885578969`, VERDICT sha256 `d4acdd38…b8add`), dưới chỉ thị chủ kho *"cross-review #679 đi, theo phân lớp, không theo từng lỗi, có hint patch"*. **r3** là hệ quả của cross-review lượt 2 trên PR #679 (comment `5886034260`, VERDICT sha256 `aa9a68d3…d4882`: 1 P1 / 3 P2 / 1 P3 theo lớp), và của quyết định chủ kho chọn neo lớp P1 bằng Mission Issue mới (#682). **r4** là hệ quả của cross-review lượt 3 trên PR #679 (comment `5887068702`, VERDICT sha256 `1eb00c7a…7e819`: 0 P1 / 2 P2 / 1 P3 theo lớp; P1 của lượt 2 đã đóng). **r5** là hệ quả của cross-review lượt 4 trên PR #679 (comment `5888141866`, VERDICT sha256 `9abc767695097d523d4e5faedd6929678f71c4d21b9fca620480230575986ed3`: 0 P1 / 1 P2 / 0 P3 theo lớp; lớp `bo-quet-chung-cu-khong-neo-anh`), của điều kiện dừng đã đăng ký ở comment `5887068702` (§9), và của quyết định Q7 của chủ kho (Mission #682, comment `5888143430`; §3). **r6** là hệ quả của cross-review lượt 5 trên PR #679 (comment `5888630117`, VERDICT sha256 `ce14afd8ba46d5b17bc1f121b2ae8fe042771af37847acdbd348ecb9942ac33d`: 0 P1 / 2 P2 / 0 P3 theo lớp; hai lớp `bo-quet-chung-cu-khong-neo-anh` và `bo-quet-nghiem-thu-thieu-mien`) và của hai quyết định chủ kho ở Mission #682: Q8 (uỷ quyền cấp lease `wp678`, thứ tự và bốn điều kiện cấp; comment `5888631719`) và Q9 (toàn vẹn object-store nằm NGOÀI phạm vi A9); §3. **r7** không vá finding nào: cross-review lượt 6 (VERDICT sha256 `9569bf0d715fe8daed90aba00ccdb2e39262dd12f094713ceb38722f8d10c18d`) approve r6 với 0 P1/P2/P3. r7 là hệ quả của quyết định Q10 của chủ kho (Mission #682, comment `5911243074`; §3): codex, reviewer của r6, hết quota, nên reviewer lượt thi hành và vế review của `required_checks` đổi sang Claude Opus 5.5 `max`. **r8** là hệ quả của review lượt 7 trên r7 (`088511f`; VERDICT sha256 `992eb9f0…794c`: 0 P1 / 2 P2 / 3 P3 theo lớp, xem `thay_the_cho`) và của quyết định Q11 của chủ kho (Mission #682, comment `5912559230`; §3): thứ tự #677 rồi #678 là thứ tự LAND, nên r8 soạn sau khi #677 land, dời nền nghiệm thu sang master sau #677 và thêm điều kiện cấp (5) (lựa chọn chủ kho đã chọn). Cụm *áp HINT lượt 7 trong một lần* chỉ có trong đoạn Hệ quả mà chính comment Q11 gắn nhãn diễn giải của phiên agent, không phải lời chủ kho; r8 không áp nhóm 2 của HINT ấy như đã viết (§9). Phương án B cho lượt review thi hành (dòng reviewer của r8) là lựa chọn của phiên soạn r8 trong phạm vi Q10 (Opus 5.5 `max`, hạ assurance vì cùng họ), **không** phải quyết định của chủ kho; tới r8 chủ kho chưa được hỏi riêng về nó, và khi được hỏi ở Q12 thì chủ kho bỏ nó. **r9** là hệ quả của review lượt 8 trên r8 (`f958e14`; VERDICT sha256 `68da880f…fe82`: 0 P1 / 4 P2 / 3 P3 theo lớp, xem `thay_the_cho`) và của quyết định Q12 của chủ kho (Mission #682, comment `5925190705`; §3): chủ kho chọn *"A: subagent, review_deferred (Recommended)"*, nên r9 bỏ phương án B, chạy review lượt thi hành bằng subagent mức `review_deferred`, land bằng `human_audited`, và áp HINT lượt 8 trừ năm hunk chỉ phục vụ B (§9). Cụm *đơn giản hóa closure, đóng hai P2 của B* nằm trong mô tả kèm của lựa chọn đã chọn; cách r9 làm điều đó cụ thể ra sao là việc của phiên soạn r9. |
| `objective` | Mọi đường đưa `lease_id` vào danh tính chỉ nhận chuỗi thật khớp `LEASE_ID`, đóng va chạm do ép giá trị không phải chuỗi thành chuỗi. Danh tính là giá trị sau `yaml.safe_load`: các cách viết ra cùng một chuỗi hợp lệ cố ý là cùng danh tính (ví dụ `'yes'` và `!!str yes`), không yêu cầu phân biệt cú pháp YAML. |
| `review_class` | **`sensitive`**: chạm `ops/lease_publish.py`, tức cổng đăng lease. |
| `risk` | **`sensitive`**: cùng lý do. |
| `executor` | `claude` (Claude Opus 5.5, effort ≥ medium) |
| `environment` | **`cloud`**. Packet không đo hành vi phụ thuộc nền (không đồng hồ ngủ máy, không đường dẫn Windows); tiền lệ các đặc tả `ops/specs/*` cùng lớp khai `cloud`. Chủ kho đổi thì phải ra revision mới. |
| reviewer | **Đổi ở r7 (Q10); đường chạy chốt ở r9 theo Q12** (bỏ phương án B của r8). Subagent `review-opus-max` do phiên điều phối giao việc, cấu hình Claude Opus 5.5 (`claude-opus-5-5`), effort `max`; cùng đường với hai lượt review đặc tả 7 và 8. Định nghĩa nằm ở phạm vi người dùng (`~/.claude/agents/review-opus-max.md`), **không** có trong kho, nên bị ghim bằng băm ở ghi chú dưới closure; băm ấy ghim CẤU HÌNH được giao, **không** phải nguồn đo runtime. Model và effort đã phục vụ lượt chạy: `KHONG_do_duoc` (PROTOCOL :710–711: cấu hình yêu cầu không phải runtime evidence; tiền lệ `ops/reviews/phan-bien-quy-trinh-review-2-claude-verdict.receipt.yaml` ghi *"không đường nào trong phiên trả model đang phục vụ"*). Mức assurance: **`review_deferred`** (PROTOCOL §8 mục 4, :568). Biên nhận **phải** tự khai `che_do: subagent_trong_phien_dieu_phoi` (tiền lệ `ops/reviews/phan-bien-quy-trinh-review-{1,2}-claude-verdict.receipt.yaml`); đã khai thì validator bác `same_provider_approved` và chỉ đích danh `review_deferred` (`ops/bien_nhan_v2.py` :703, :720–726). Lượt này **không** mang lời khai độc lập nào: nó chạy trong phiên điều phối, cùng họ Claude với executor, không có `session_run_id` hay `phien_doc_lap`. Vì vậy nó không là `cross_approved` (§8 mục 1, :562; validator bác khi hai bên cùng họ, :734–737) và không là `same_provider_approved` (§8 mục 3, :565–567 đòi phiên/context/checkout mới độc lập, không fork context executor). Validator không tự phát hiện subagent: biên nhận bỏ `che_do` mà thêm một `session_run_id` bất kỳ vẫn qua `same_provider_approved` (đo ở ghi chú dưới closure), nên khai `che_do` là nghĩa vụ khai trung thực, không phải chốt máy. Không dùng `advisory_review`: tên ấy không thuộc bốn mức của §8 (PROTOCOL §8.1 :715–716 xếp ChatGPT Web vào đúng mức ấy nhưng không giới hạn tên cho riêng nó; kho có biên nhận `anthropic_claude` ghi `advisory_review`, r9 theo bốn mức của §8). `review_deferred` không thay `cross_approved` cho class `sensitive`: với mức ấy, land đòi cross-review khác nền tảng hoặc human review có audit (:662–663), và Q12 chọn `human_audited` (ghi chú gate land ngay dưới closure). Số dòng: `docs/PROTOCOL_DA_PHIEN.md` :562 (mục 1), :565–567 (mục 3), :568 (mục 4), :662–663, :710–716 (§8.1) trên `20ec8d5`; PROTOCOL và `ops/bien_nhan_v2.py` giống hệt giữa `423b4ba` và `20ec8d5` (`git diff --quiet` rc=0). Lịch sử: r1–r6 khai `codex` (`gpt-6-astra`, effort ≥ medium), sáu lượt review đặc tả chạy bằng codex; r7 khai subagent `review-opus-max`, mức `review_deferred`; r8 khai `claude -p` qua `launcher.py run`, mức `same_provider_approved` khi đủ bằng chứng (phương án B), bỏ ở r9 theo Q12 sau khi review lượt 8 đo ba khe của nó (`run.json` không lưu argv; `session_run_id` không chứng minh độc lập; probe trust của launcher chặn `CHAN [15]` ở sandbox chưa trust). |
| `depends_on` | **Theo Q8 (§3), viết lại ở r6; r7 đổi điều kiện (3); r8 thêm điều kiện (5) theo Q11; r9 tổng quát hoá điều kiện (4) theo review lượt 8 và đo lại.** Chủ kho uỷ quyền cấp lease `wp678` (Q8). Thứ tự: đợi lease `lease-publish-windows-do-r1-g1-claude` của packet #687 (giữ `ops/lease_publish_test.py`) nhả (Q8; đo r9: lease #687 đang giữ tệp ấy nay là generation 3, xem dưới), và **#677 land trước** (Q11: *"#677 rồi #678"* là thứ tự LAND). Năm điều kiện cấp, cả năm phải thoả và **đo lại lúc cấp**, không nhận số dưới đây thay phép đo: (1) `ai-dang-giu ops/lease_publish.py` và `ai-dang-giu ops/lease_publish_test.py` đều ra `NGƯỜI_GIỮ 0`, và chỉ tin kết quả ấy sau khi so `git ls-remote --heads origin` với `git for-each-ref refs/remotes/origin` theo **tập tên** (thiếu ref cục bộ ⇒ MÙ ⇒ fail-close, không cấp); (2) không lượt review nào đang chạy; (3) lease neo `spec_hash` của revision **cuối cùng đã review sạch** (0 P1/P2/P3); từ r9, đó là **revision 9**, review sạch bằng lượt subagent `review-opus-max` (cấu hình Opus 5.5 `max`) mức `review_deferred` (Q12; dòng reviewer và ghi chú Q10 ở §3); (4) nếu #687 land trước và đổi `ops/lease_publish_test.py` thì dời nền nghiệm thu bằng một revision mới **trước** khi cấp, không cấp trên nền cũ; **tổng quát hoá** (chặt hơn Q8, không nới): lúc cấp, trên cùng kho vừa qua phép so tập tên ref ở (1) (để `origin/master` không là ref đệm cũ), `git diff --quiet <nền nghiệm thu> origin/master -- ops/lease_publish.py ops/lease_publish_test.py` phải rc=0; rc=1, tức **bất kỳ** packet nào (#687 hay packet khác) đã land thay đổi một tệp write set sau nền, ⇒ cũng dời nền bằng revision mới trước khi cấp; rc khác hoặc không chạy được ⇒ không cấp; (5) **#677 đã land** (Q11): PR #689 `merged: true`, merge commit của nó là tổ tiên của `origin/master` lúc cấp (`git merge-base --is-ancestor <merge commit> origin/master` rc=0), và nền nghiệm thu chứa merge ấy; không đo được một trong ba vế ⇒ không cấp. Đây là kiểm loại trừ write set của protocol cộng điều kiện cấp của Q8 và Q11, **không** phải cổng quét kiểu `lease_id`: cổng quét kiểu chỉ đặt trước land (A9, Q7). **Hiện tại (r9, 01-10), phiên soạn r9 tự đo.** (a) Clone sạch có sẵn trong scratch của phiên điều phối (`adg2`: không nông, refspec `+refs/heads/*:refs/remotes/origin/*`, `refs/heads` 1 ref, `refs/replace` 0 ref, cây sạch), `git fetch -q --prune` cùng refspec rc=0 (05:17:32Z–05:17:33Z), `git merge --ff-only origin/master` rc=0: `origin/master` = `20ec8d5`. `ls-remote --heads` 461 tên, `for-each-ref refs/remotes/origin` 461 tên (bỏ `HEAD`), lệch theo tên 0 dòng cả hai chiều, lệch theo cặp tên + OID 0 dòng (05:17:40Z–05:17:41Z). `ai-dang-giu ops/lease_publish.py` (05:17:46Z–05:17:57Z) ⇒ dòng cuối `NGƯỜI_GIỮ 0: không có`, rc=0, 0 dòng `CÒN_HẠN`. `ai-dang-giu ops/lease_publish_test.py` (05:17:57Z–05:18:07Z) ⇒ dòng cuối `NGƯỜI_GIỮ 1: lease-publish-windows-do-r3-g3-claude`, **rc=11**, đúng một dòng `CÒN_HẠN` (`refs/remotes/origin/claude/cap-lease-687-g3:ops/leases/lease-publish-windows-do-r3-g3-claude.yaml`). Tệp lease ấy (đọc bằng `git show` rồi `yaml.safe_load`): `packet_issue: 687`, `generation: 3`, `write_set` chỉ `ops/lease_publish_test.py`, `leased_at_utc: '2026-10-01T01:12:00Z'`, `lease_expires_at_utc: '2026-10-02T01:12:00Z'`, `start_from_sha` `89fc4fa`; đầu ref là commit `eca94d1` (01:11:15Z, tiêu đề *"lease(#687): r3 g3 — mở lại sau khi #677 land; …"*). Vậy **điều kiện (1) CHƯA thoả**: #687 giữ `ops/lease_publish_test.py` tới `2026-10-02T01:12:00Z`. Điều kiện (2): phiên soạn r9 KHÔNG ĐO ĐƯỢC. Điều kiện (3): r9 chưa được review, chưa thoả. Điều kiện (4): `git diff --quiet 20ec8d5 origin/master -- ops/lease_publish.py ops/lease_publish_test.py` rc=0 (05:18:23Z), thoả tại lúc đo; vì #687 đang giữ `ops/lease_publish_test.py`, nếu nó land và đổi tệp ấy thì phép đo này ra rc=1 và phải có revision mới dời nền trước khi cấp. Điều kiện (5): REST `GET /repos/ducthangho/tra-luat/pulls/689` (HTTP 200, 05:22Z, không token) ⇒ `merged: true`, `merged_at` `2026-10-01T00:55:22Z`, `merge_commit_sha` `20ec8d5d0e86cb7dc01f202c7596407a957e5961`; `20ec8d5` là `origin/master` và là nền nghiệm thu, nên thoả tại lúc đo. (b) Kho `/home/user/tra-luat`: r9 không đo (không `fetch` vào kho chính). **Lịch sử r8 (01-10), phiên soạn r8 tự đo.** (a) Clone mới từ `origin` ở scratch (clone 01:10:39Z–01:10:47Z, không nông, refspec `+refs/heads/*:refs/remotes/origin/*`, `refs/heads` chỉ có `master`, rồi `fetch` cùng refspec rc=0): `ls-remote --heads` 459 tên, `for-each-ref refs/remotes/origin` 459 tên (bỏ `HEAD`), lệch theo cặp tên + OID 0 dòng cả hai chiều, lệch theo tên 0 dòng (01:10:48Z); `origin/master` = `20ec8d5`. `ai-dang-giu ops/lease_publish.py` (01:10:52Z–01:11:03Z) và `ai-dang-giu ops/lease_publish_test.py` (01:11:04Z–01:11:15Z) đều ra dòng cuối `NGƯỜI_GIỮ 0: không có`, rc=0, 0 dòng `CÒN_HẠN`. Sáu lease #677 `dot-bien-l-bien-cong-khai-exec-1`…`exec-6` đều `HẾT_HẠN`; lease g6 (`dot-bien-l-bien-cong-khai-exec-6-claude-20260930`, `refs/remotes/origin/claude/cap-lease-677-g6`) nay khai `lease_expires_at_utc: '2026-10-01T01:10:00Z'`, gốc `03:27Z`, rút hạn ở commit `35e23d7` (01:01:20Z, *"thu hồi bằng rút hạn về 01:10Z — packet đã merge (PR #689, 20ec8d5)"*). g6 chỉ giữ `ops/lease_publish_test.py`, và phép đo người giữ tệp ấy bắt đầu **64 giây** sau mốc 01:10:00Z; trước mốc ấy g6 còn hạn. Hai lease #687 vẫn `HẾT_HẠN`. (b) Kho `/home/user/tra-luat`: r8 **không** đo lại (không `fetch` vào kho chính); lời giải thích `CHAN [12]` của r7 dưới đây giữ làm lịch sử. Điều kiện (2): phiên soạn r8 KHÔNG ĐO ĐƯỢC. Điều kiện (3): r8 chưa được review, chưa thoả. Điều kiện (4): #687 chưa land (không merge nào của #687 trong `git log --first-parent 89fc4fa..20ec8d5`, 10 merge), nên không phải dời nền vì #687. Điều kiện (5): REST `GET /repos/ducthangho/tra-luat/pulls/689` (HTTP 200, 01:06:46Z) ⇒ `merged: true`, `merged_at` `2026-10-01T00:55:22Z`, `merge_commit_sha` `20ec8d5d0e86cb7dc01f202c7596407a957e5961`, `merged_by` `ducthangho`, base `fc852ff`; `20ec8d5` chính là `origin/master` và là nền nghiệm thu của r8, nên thoả tại lúc đo. Tương tác với #677: §10 và A2. **Lịch sử r7 (30-09).** *Lời khai của phiên điều phối, đo 12:2xZ, không phải phép đo của phiên soạn r7:* hai tệp `NGƯỜI_GIỮ 0` qua `ai-dang-giu`, sau khi so tên + OID của `ls-remote --heads` với `for-each-ref`, 0 lệch; không lượt review `wp678` nào đang chạy; r6 approve sạch; nền `89fc4fa`→`423b4ba` không đổi hai tệp. *Phiên soạn r7 tự đo:* (a) trong một clone mới từ `origin` ở scratch (clone 12:27:46Z–12:27:52Z, không nông, `refs/heads` chỉ có `master`): `ls-remote --heads` 458 tên, `for-each-ref refs/remotes/origin` 458 tên (bỏ `HEAD`), lệch theo cặp tên + OID 0 dòng cả hai chiều (12:27:58Z); `ai-dang-giu ops/lease_publish.py` và `ai-dang-giu ops/lease_publish_test.py` đều ra dòng cuối `NGƯỜI_GIỮ 0: không có`, rc=0, 0 dòng `CÒN_HẠN` (12:28:03Z–12:28:25Z); hai lease #687 (`lease-publish-windows-do-r1-g1-claude`, `lease-publish-windows-do-r2-g2-claude`) ở nhãn `HẾT_HẠN`, tệp lease trên `refs/remotes/origin/claude/lease-publish-windows-do` nay khai `lease_expires_at_utc` lần lượt `'2026-09-29T11:50:00Z'` và `'2026-09-29T11:45:00Z'` (commit `6112b89` rút hạn). (b) Cùng hai lệnh trong kho `/home/user/tra-luat` và worktree dùng chung ref của nó ra **`CHAN [12]` `KHÔNG_XÁC_ĐỊNH`, rc=12** (12:27:18Z), vì nhánh cục bộ `ops/spec-lease-id-ep-kieu-yaml` (`03a7219`, là tổ tiên của `origin/master`) có upstream `[gone]`; phép so tên + OID ở kho ấy cũng 458/458, 0 lệch (12:27:11Z). Tức kết quả phụ thuộc kho đo: lúc cấp phải đo ở kho không vướng `CHẶN [12]`, và không đọc rc=12 thành `NGƯỜI_GIỮ 0`. Điều kiện (2): phiên soạn r7 KHÔNG ĐO ĐƯỢC. Điều kiện (4): #687 chưa land (không merge nào của #687 trong `git log --first-parent 89fc4fa..423b4ba`, 7 merge) và hai tệp không đổi (hàng nền nghiệm thu), nên không phải dời nền. Ngoài bốn điều kiện, xem §10 về nhánh thi hành của #677. Lịch sử r6 (10:48Z–10:49Z 29-09): `ops/lease_publish.py` `NGƯỜI_GIỮ 0`, rc=0; `ops/lease_publish_test.py` `NGƯỜI_GIỮ 1: lease-publish-windows-do-r1-g1-claude`, rc=11, lease ấy khi đó `CÒN_HẠN` và khai `lease_expires_at_utc: '2026-09-30T10:20:00Z'`, nên điều kiện (1) chưa thoả; so tên ref: máy chủ 511, cục bộ 512, thiếu cục bộ 0, thừa cục bộ 1 (`claude/bookkeeping-574-land`, ref đệm cũ, vô hại). Lịch sử cũ hơn: đo 10:14Z (r5) và 09:44Z (r4) cả hai tệp `NGƯỜI_GIỮ 0` (lease của #687 chưa có, `leased_at` 10:20Z); đo 07:59Z 29-09 `ai-dang-giu ops/lease_publish_test.py` ⇒ `NGƯỜI_GIỮ 1: t131-deadline-dem-spawn-exec-1-claude-20260929`, đã `HẾT_HẠN` (`lease_expires_at_utc: '2026-09-29T08:15:00Z'`) và T131 **đã land** (PR #680, `89fc4fa`). |
| nền nghiệm thu | `origin/master` `20ec8d5d0e86cb7dc01f202c7596407a957e5961` (merge PR #689, tức #677 land; Q11). Đây là **nền bất biến** để đo diff và nghiệm thu. Packet CHƯA thi hành, chưa có diff hay lịch sử finding trên mã, nên việc dời nền ở r8 là quyết định bền (chính r8) theo protocol §3.2.1 và theo Q11, không phải dùng HEAD mới để xoá diff. r9 giữ nền này: `origin/master` vẫn là `20ec8d5` lúc 05:17:33Z 01-10 (clone `adg2` sau `fetch --prune`), và `git diff --quiet 20ec8d5 origin/master -- ops/lease_publish.py ops/lease_publish_test.py` rc=0 (05:18:23Z), nên điều kiện (4) không đòi dời nền tại lúc đo. Đo 01-10 trên clone mới (r8): `origin/master` = `20ec8d5` (01:03:48Z và 01:10:47Z); `git merge-base --is-ancestor 89fc4fa 20ec8d5` rc=0; `git diff --quiet 89fc4fa 20ec8d5 -- ops/lease_publish.py` rc=0 (blob sha256 `dd17b94c…4f83` ở cả hai nền), nên các phép đo §1/§2 làm trên `1741e0a` vẫn hợp lệ; `git diff --numstat 89fc4fa 20ec8d5 -- ops/lease_publish_test.py` ⇒ `600 15`, bằng đúng `fc852ff..20ec8d5` (base của PR #689) và `423b4ba..20ec8d5`. Toàn bộ chênh do 9 commit `test(#677)` từ `11f73ac` tới `adad5f5`: thêm 18 hàm (8 ca `t195`–`t202` và 10 hàm phụ, trong đó `_chay_buoc_dang_that`), đổi thân đúng hai ca có sẵn (`t70`, `t154`); `t178`, `t131`, `t139`, `t192`, `_chay_buoc_dang`, `_buoc_workflow` giống hệt thân (so bằng `ast`), chỉ dời dòng. `.github/workflows/ops-publish-lease.yml` giống hệt (`git diff --quiet` rc=0). **Lịch sử nền:** r1 và r2 dùng `1741e0a1ab7ebce4b26912aefadca56ddfcdc691`; r3 dời sang `89fc4fac8cea65979cc2483043dc8cd07a6e8518` (PR #680, T131 land) theo cùng lý lẽ §3.2.1; r4, r5 và r6 **giữ nguyên** nền của r3: `git fetch` rồi `git rev-parse origin/master` đo 09:44Z 29-09 (r4), 10:14Z 29-09 (r5) và 10:48Z 29-09 (r6) vẫn ra `89fc4fac8cea65979cc2483043dc8cd07a6e8518`. r7 cũng giữ nền này, nhưng vì lý do khác: `origin/master` đã sang `423b4ba14078701859b9e6ac101a68a3fc4ddef4` (`git ls-remote origin refs/heads/master`, 12:26:45Z 30-09), còn `git diff --stat 89fc4fa 423b4ba -- ops/lease_publish.py ops/lease_publish_test.py` ra output **rỗng**, rc=0; cùng lúc `git diff --quiet` cùng phạm vi rc=0 và `git merge-base --is-ancestor 89fc4fa 423b4ba` rc=0. Giữa `1741e0a` và `89fc4fa`, `ops/lease_publish.py` giống hệt (`git diff --quiet` rc=0) và `ops/lease_publish_test.py` đổi +13/−19 (bốn hunk: hai trong t131, một trong t139, một trong t192). Nếu bất kỳ packet nào (#687 hay packet khác) land trước khi cấp và đổi một tệp write set, nền phải dời bằng revision mới trước khi cấp (điều kiện 4, kể cả phần tổng quát hoá). Nền tiếp nối (continuation base), nếu khác nền mà không đổi tệp write set nào, phải được khai riêng lúc cấp lease, không thay nền này. |
| `spec_hash` | Xem **Công thức băm** ngay dưới. Giá trị **không** nằm trong tệp này. |

**Công thức băm.** `spec_hash` = SHA-256 trên **toàn bộ bytes** của tệp này tại commit đã đóng
băng: `sha256sum ops/specs/lease-id-ep-kieu-yaml-r9.md`, không loại dòng nào. Giá trị được công
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
**Miễn trừ vẫn áp cho r9.** Thân #682 đọc qua REST `GET /repos/ducthangho/tra-luat/issues/682` (HTTP 200, 05:22Z
01-10, không token; sha256 thân UTF-8 `76bee6fb159ffb5a8c9cbd74896dd5793443457b5f0ebf6a284eb3350e2e0dd2`, 3416 byte,
0 thực thể HTML, bằng đúng băm r8 đo lúc 01:08:54Z); hai dòng dưới chép từng byte từ dòng 29 và 31 của thân ấy (bỏ gạch đầu dòng):
  > Áp cho **packet `wp678` duy nhất**, mọi revision kể từ r3.
  >
  > Đổi bất kỳ giá trị nào ở bảng trên ⇒ revision mới, `spec_hash` mới, lease mới.

Bảng trên #682 còn ghi vế cross-review codex của r3; r7 đổi đúng vế ấy theo Q10 bằng revision mới, đúng luật của miễn
trừ; r8 **không** đổi giá trị closure nào (chỉ thêm ghi chú kiểm ngoài bảng); r9 đổi hai giá trị (vế review của
`required_checks`, `land_obligations`) theo Q12, bằng revision mới, đúng luật của miễn trừ; write set không mở rộng.
Chưa thấy policy canonical: trong 128 tệp
đổi `89fc4fa..20ec8d5` không tên nào chứa `polic`, `closure`, `dispatcher`; 16 dòng thêm nhắc `change_policy`, `policy
canonical` hoặc `closure policy` đều thuộc hồ sơ wp678 (spec r2–r6, verdict lượt 3, 4, 6), và `423b4ba..20ec8d5` thêm 0
dòng như thế (lọc theo tên và chuỗi, không chứng minh vắng mặt). Lịch sử: r7 đọc #682 qua REST lúc 12:33Z 30-09 và lọc 61
tệp `89fc4fa..423b4ba`. r9: `origin/master` vẫn là `20ec8d5` (05:17:33Z 01-10), nên không có tệp đổi nào ngoài
phạm vi lọc của r8.

| trường | giá trị |
|---|---|
| `change_policy_sha` | `null` — chưa có policy canonical; descriptor thay thế là miễn trừ ở #682 |
| `effective_write_set` | `ops/lease_publish.py` · `ops/lease_publish_test.py` (exact) |
| `effective_review_class` | `sensitive` |
| `required_checks` | Trên PR thi hành: `gate (ubuntu-latest)`, `gate-ops (ubuntu-latest)`, `gate-registry (ubuntu-latest)`, `gate-packet-loop (ubuntu-latest)` của `.github/workflows/ci.yml`, và workflow `thu-hoi`; review bằng subagent `review-opus-max` trong phiên điều phối (cấu hình Claude Opus 5.5 `claude-opus-5-5`, effort `max`), mức `review_deferred`, 0 P1/P2/P3 theo phân lớp trên exact `reviewed_sha`, kèm VERDICT + HINT và biên nhận tự khai `che_do: subagent_trong_phien_dieu_phoi` (r3–r6 ghi cross-review codex; r7–r8 ghi review Claude Opus 5.5 `max`; đổi theo Q12) |
| `land_obligations` | Chủ kho audit mức `human_audited` (PROTOCOL §8 mục 2; Q12) + merge (không tự merge/approve); ghi sổ verdict + HINT các lượt vào `ops/reviews/` kèm receipt và mục README; thu hồi lease sau land; đóng #678; cập nhật #677 về tương tác A2 |

**Ghi chú về gate land** (có từ r7; từ r9 mức `human_audited` cũng ghi trong giá trị `land_obligations`, Q12). Thiếu `cross_approved` thì land `sensitive` đòi
`human_audited`: PROTOCOL ghi *"Phải có Codex `cross_approved` hoặc `human_audited`; hết quota mà chưa có human
thì pause"* (:681–682; cũng :652, :662–663). Vế "Chủ kho audit" của `land_obligations` phải đạt đúng §8 mục 2
(:563–564: danh tính bền trên GitHub, độc lập với executor/tác giả, tự đọc spec/diff, evidence audit và verdict
bền neo exact `reviewed_sha`), kèm readback verdict/receipt exact-head trước land (:658). Comment do phiên agent
đăng hộ bằng credential chủ kho không phải evidence ấy, và validator cấm biên nhận của mô hình khai
`human_audited` (`ops/bien_nhan_v2.py` :793–796). Review subagent sạch ở mức `review_deferred` mà chưa có human
audit ⇒ **không land** (PROTOCOL :662–663: `review_deferred` phải có cross-review khác nền tảng hoặc human review có
audit; Q12 chọn `human_audited`).

**Ghi chú về cách kiểm vế review của `required_checks`** (viết lại ở r9 theo Q12, không phải giá trị closure).
`claude-opus-5-5` và `effort max` trong vế ấy là CẤU HÌNH giao cho subagent, không phải runtime evidence (PROTOCOL
:710–711). Vế review **đạt** khi và chỉ khi biên nhận của lượt có đủ bốn điều:
(a) **mức và chế độ**: `assurance: review_deferred`, `model_reviewer_identity.che_do: subagent_trong_phien_dieu_phoi`,
và `_thieu` của `ops/bien_nhan_v2.py` trả **0** lỗi. Phiên soạn r9 đo (05:18:49Z 01-10, `ops/bien_nhan_v2.py` của
`20ec8d5`, sha256 `38cda51c9b46fb0b9ede91a63d89902c0c1b0faaca52d65e07c7ed31a5badefc`; script ở scratch, không vào kho):
biên nhận tiền lệ `phan-bien-quy-trinh-review-2` nguyên byte ⇒ 0 lỗi; một biên nhận mẫu dựng từ nó cho `wp678`
(`model_reviewer_identity.provider: anthropic`, `che_do` như trên, `review_deferred`) ⇒ **0** lỗi; cùng mẫu đổi sang
`same_provider_approved` ⇒ 1 lỗi (*"tự khai chạy trong phiên điều phối"*); đổi sang `human_audited` ⇒ 2 lỗi; bỏ
`che_do`, thêm `session_run_id: 'x'` rồi khai `same_provider_approved` ⇒ 0 lỗi (nên `che_do` là nghĩa vụ khai, không
phải chốt máy).
(b) **model và effort**: biên nhận ghi `claude-opus-5-5` và `max` là cấu hình yêu cầu, và ghi model/effort đã phục vụ
là `KHONG_do_duoc`. Không nâng lời khai này lên, và không ghi `modelUsage` hay `session_run_id` cho một lượt không
sinh ra chúng.
(c) **định nghĩa**: sha256 của `~/.claude/agents/review-opus-max.md` lúc giao việc bằng
`e225b81cf2fbdd0f05a54a689cac17db8972b2f8c0684a0a30931875cd4b792c` (1175 byte; đo 12:33Z 30-09 và 01:14:09Z 01-10;
phiên soạn r9 đo lại 05:18:56Z 01-10, frontmatter `model: claude-opus-5-5`, `effort: max`). Băm này ghim CẤU HÌNH mà
phiên điều phối giao; nó **không** là nguồn đo runtime, không chứng minh định nghĩa đã được nạp hay model ấy đã phục
vụ. Thiếu hoặc lệch ⇒ **không** đạt; đổi định nghĩa ⇒ revision mới.
(d) **kết luận**: sha256 VERDICT và HINT; VERDICT 0 P1/P2/P3 theo lớp trên exact `reviewed_sha`.
Đạt bốn điều này là có một lượt review ở mức `review_deferred`, **không** phải thẩm quyền land: land vẫn đòi
`human_audited` (ghi chú gate land ở trên). Không có đường lùi nào phải canh: Q12 bỏ đường `claude -p`, nên không còn
nhánh "launcher chặn thì dừng hỏi chủ kho" của r8.

**Descriptor nguồn closure** = `{mission_issue: 682, object_id: 5627190292}`. Closure do phiên
điều phối điền tay theo miễn trừ ấy, **không** do executor tự khai. Lease phải **chép** đúng các
giá trị trên, không được thêm hay đổi; lệch ⇒ **DỪNG**. Băm thân Issue ở phía nhận là
**KHÔNG ĐO ĐƯỢC** từ phiên soạn r6 (đường đọc MCP chuẩn hoá thực thể HTML trong thân issue, xem
CLAUDE.md), nên descriptor neo bằng object ID + số Issue, không bằng băm thân. Phiên soạn r8 và r9 đọc được thân qua REST
và ghi băm ở đoạn miễn trừ trên (cùng một băm), như phép đo tại từng thời điểm; descriptor **không** đổi thành băm thân.

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
  ref; điều kiện (2)–(4) là mới ở r6. Trạng thái đo của điều kiện (1) ở header. **Đo r8:** thân comment
  `5888631719` đọc qua REST (HTTP 200, 01:08:53Z 01-10; sha256 thân UTF-8
  `3a8c40a6cfad91079874e1a0b8d80099262aa343929137c9b2cbf1026971c45e`, 1187 byte, 0 thực thể HTML; đăng qua app
  `claude`): bốn điều kiện cùng nội dung với tóm tắt trên (thân viết "cross-review" ở điều kiện 2 và 3; vế review đổi
  theo Q10), và thân **không** nhắc #677 (chuỗi `677` xuất hiện 0 lần). Thứ tự với #677 do Q11 quyết, không do Q8.
- **Q9 — Toàn vẹn object-store NGOÀI phạm vi A9** (chủ kho, 29-09, Mission #682 comment `5888660607`): câu A9 trả lời là *"có `lease_id` sai kiểu không"*, không phải *"kho có hỏng không"*.
  Yêu cầu r5 và HINT lượt 5 về băm toàn chuỗi (commit, tree gốc, mọi tree con, blob) **bị bác** và
  thay bằng **điều kiện tiên quyết**: `git fsck --full` rc=0 chạy trong **cùng lượt quét** A9, output
  và rc ghi vào handoff, kèm câu nói thẳng rằng nó **không nguyên tử** (fsck kiểm một ảnh, lượt quét
  đọc một ảnh khác nếu kho đổi giữa chừng) và đó là **rủi ro được chấp nhận có chủ đích**. GIỮ yêu cầu
  băm blob trên chính bytes đưa vào parser (rẻ, đã có từ r5). `fsck` rc khác 0 ⇒ `KHÔNG ĐO ĐƯỢC` ⇒
  không land. Hệ quả cho hợp đồng: helper A9 **không** kiểm commit, tree gốc hay tree con, và không
  được đọc là đã kiểm; ca "tree con hỏng" của lượt 5 nằm ngoài phạm vi helper và được bắt bởi điều kiện
  tiên quyết fsck (A9, Phụ lục A).
- **Q10 — Đổi reviewer lượt thi hành sang Claude Opus 5.5 `max` bằng revision 7** (chủ kho, trắc nghiệm trong
  phiên, trả lời `2026-09-30T12:21:07Z` theo transcript; neo https://github.com/ducthangho/tra-luat/issues/682#issuecomment-5911243074,
  id `5911243074`, tạo `12:24:28Z`, **phiên agent đăng HỘ**, nên `author_association: OWNER` không chứng minh chủ
  kho tự gõ). Đọc qua REST `GET /repos/ducthangho/tra-luat/issues/comments/5911243074` (HTTP 200, 12:33:01Z
  30-09), sha256 thân UTF-8 `69cc35b179d4c9f94459c2d874156f8f303fb32e67b90c81e0f2cd617bc22d2f`, 2151 byte; các
  dòng dưới chép từng byte từ thân ấy:
  > **Câu hỏi (nguyên văn):** "Lease wp678: đủ 4 điều kiện Q8 (đo 12:2xZ: hai tệp NGƯỜI_GIỮ 0 sau khi so tên+OID ref 0 lệch; không review wp678 nào đang chạy; r6 d1f9dd79 approve sạch; nền 89fc4fa→423b4ba không đổi hai tệp). Vướng: closure r6 đóng băng required_checks gồm "cross-review codex 0 P1/P2/P3", mà codex hết quota tới 03-10 18:31 — lease 24h cấp bây giờ sẽ hết hạn trước khi có review codex. Đổi reviewer sang Opus là đổi closure ⇒ phải ra r7 + review r7. Làm sao?"
  >
  > **Các lựa chọn:**
  > - "Hoãn tới khi codex có lại" — không chọn. Mô tả kèm: "Không cấp bây giờ; hẹn check-in 03-10 ~19:00Z đo lại 4 điều kiện rồi cấp. Giữ r6 nguyên."
  > - **"Ra r7 đổi reviewer sang Opus"** — **ĐÃ CHỌN**. Mô tả kèm: "Soạn r7 (chỉ đổi reviewer/required_checks sang Opus 5.5 max, hạ assurance tương ứng vì cùng họ), review r7, rồi cấp lease. Thực thi ngay trong phiên này."
  > - "Cấp ngay, review sau" — không chọn. Mô tả kèm: "Cấp lease 24h bây giờ, thực thi xong để sẵn; review codex chạy khi có quota (lease có thể phải gia hạn — bạn quyết khi đó)."

  Hệ quả (diễn giải của phiên soạn, **không** phải lời chủ kho; chính thân comment gắn cho đoạn tương ứng nhãn
  *"diễn giải của phiên agent, không phải lời chủ kho"*): chỉ đổi reviewer lượt thi hành, vế review của
  `required_checks` và mức assurance; mục tiêu, write set, nền nghiệm thu, A1–A10 giữ nguyên. Lease chỉ cấp sau
  khi r7 review sạch và bốn điều kiện Q8 đo lại lúc cấp. Q10 không nới gate land. Mốc "03-10 18:31" không ghi
  năm, múi giờ; phiên soạn r7 không đo nó. Ghi chú r8: lựa chọn của Q10 (Opus 5.5 `max`, hạ assurance vì cùng
  họ) không đổi; điều kiện cấp nay là năm điều kiện ở `depends_on` (thêm (5) theo Q11), và đường chạy reviewer theo
  dòng reviewer. Điều kiện cấp (3) là review **đặc tả**; từ r9 (Q12) nó và vế review của `required_checks` trên PR thi
  hành đi cùng một đường, chỉ khác đối tượng được review: lượt
  subagent trong phiên điều phối (như lượt 7, lượt 8) được tính cho (3) khi VERDICT sạch trên exact `reviewed_sha` và
  biên nhận tự khai `che_do: subagent_trong_phien_dieu_phoi`, mức `review_deferred`; model/effort của lượt ấy là CẤU
  HÌNH (định nghĩa ghim băm ở ghi chú dưới closure), nguồn đo `KHONG_do_duoc` (PROTOCOL :710–711), không được đọc
  thành đã đo Opus 5.5 `max`.
- **Q11 — Thứ tự #677 / #678 là thứ tự LAND** (chủ kho, trắc nghiệm trong phiên, trả lời `2026-09-30T13:44:41Z`
  theo transcript; neo https://github.com/ducthangho/tra-luat/issues/682#issuecomment-5912559230, id `5912559230`, tạo
  `2026-09-30T13:44:59Z`, **phiên agent đăng HỘ** qua app `claude`, nên `author_association: OWNER` không chứng minh
  chủ kho tự gõ). Đọc qua REST `GET /repos/ducthangho/tra-luat/issues/comments/5912559230` (HTTP 200, 01:06:31Z 01-10),
  sha256 thân UTF-8 `392069d134cb3f87cada3917bbca9cc9568c51cd1045aa83cc17974f03b68106`, 1741 byte, 0 thực thể HTML;
  các dòng 5–17 của thân chép từng byte dưới đây, **kể cả nhãn** mà thân gắn cho đoạn "Hệ quả":
  > **Lúc:** 2026-09-30T13:44:41Z (transcript).
  >
  > **Câu hỏi (nguyên văn):** "wp678: đặc tả #677 r7 (trên master) ghi quyết định của bạn "Sau #676: #677 rồi #678". Nhánh mã của #677 đã sửa ops/lease_publish_test.py (+596/−15), PR #689 chưa land, và năm lease của #677 đã hết hạn. Thứ tự đó nghĩa là gì?"
  >
  > **Các lựa chọn:**
  > - **"Thứ tự land: đợi #677"** — **ĐÃ CHỌN**. Mô tả kèm: "Không cấp lease wp678 cho tới khi #677 land; r8 dời nền nghiệm thu sang master sau #677 và ghi thêm điều kiện cấp (5): #677 đã land."
  > - "#678 đi trước" — không chọn.
  > - "Chỉ là thứ tự lease" — không chọn.
  >
  > **Hệ quả** (diễn giải của phiên agent, không phải lời chủ kho):
  > - **Không cấp lease wp678** cho tới khi #677 (PR #689) land.
  > - r7 (`088511f`, cục bộ) có review lượt 7 là `changes_requested` 0/2/3 ([#678 comment 5912542067](https://github.com/ducthangho/tra-luat/issues/678#issuecomment-5912542067)). Lớp `thu-tu-677-bo-ngo-o-dieu-kien-cap` đóng theo quyết định này.
  > - r8 soạn **sau khi #677 land**, trong một lần: áp HINT lượt 7, dời nền nghiệm thu sang master sau #677, và thêm điều kiện cấp (5). Làm vậy để khỏi tốn một vòng review cho nền sẽ đổi.

  Áp vào r8 (việc của phiên soạn r8, không phải lời chủ kho): điều kiện cấp (5) ở `depends_on`; nền nghiệm thu dời
  sang `20ec8d5` (merge PR #689); lớp `thu-tu-677-bo-ngo-o-dieu-kien-cap` của lượt 7 đóng theo quyết định này (§10).
  Câu hỏi nêu "+596/−15" là số của nhánh #677 lúc hỏi (`git diff --numstat 423b4ba...8e630c0`, đo lại 01-10: `596 15`);
  PR #689 land thêm hai commit (`3c308b3`, `adad5f5`), nên chênh đã land là +600/−15 (`fc852ff..20ec8d5`).
- **Q12 — Đường review của lượt thi hành: subagent, `review_deferred`** (chủ kho, trắc nghiệm trong phiên, trả lời
  `2026-10-01T05:12:47Z` theo transcript; neo https://github.com/ducthangho/tra-luat/issues/682#issuecomment-5925190705,
  id `5925190705`, tạo `2026-10-01T05:12:59Z`, **phiên agent đăng HỘ** qua app `claude`, nên `author_association:
  OWNER` không chứng minh chủ kho tự gõ). Đọc qua REST `GET /repos/ducthangho/tra-luat/issues/682/comments` (HTTP 200,
  05:13:50Z 01-10, không token), sha256 thân UTF-8 `4c9d5e198e81eff941b2c18f45d25e80e56b75e5a2a7334cacd2629f6cf2af2f`,
  1648 byte, 0 thực thể HTML; các dòng 5–14 của thân chép từng byte dưới đây, **kể cả nhãn** mà thân gắn cho đoạn
  "Hệ quả":
  > **Lúc:** 2026-10-01T05:12:47Z (transcript).
  >
  > **Câu hỏi (nguyên văn):** "wp678: review lượt 8 ra 0/4/3, tỉ lệ vá thật 0/5 (dưới ngưỡng 50% của §12). Hai trong bốn P2 sinh ra từ 'phương án B' mà phiên soạn tự chọn: review lượt thi hành bằng `claude -p` qua launcher.py run. Đường này cần bạn cấp trust cho sandbox (launcher chặn CHAN[15]; agent không được tự trust), và vẫn không chứng minh được phiên độc lập. Dù đường nào, land vẫn cần human_audited của bạn. Chọn đường review lượt thi hành?"
  >
  > **Các lựa chọn:**
  > - **"A: subagent, review_deferred (Recommended)"** — **ĐÃ CHỌN**. Mô tả kèm: "Bỏ phương án B; review thi hành bằng subagent Opus 5.5 max như các packet khác, mức review_deferred, land bằng human_audited. r9 đơn giản hóa closure, đóng hai P2 của B."
  > - "B: claude -p, tôi cấp trust" — không chọn.
  > - "Đợi codex (03-10)" — không chọn.
  >
  > **Hệ quả** (diễn giải của phiên agent, không phải lời chủ kho): r9 bỏ phương án B. Review của lượt thi hành chạy bằng subagent Opus 5.5 max, mức `review_deferred`, và land bằng `human_audited`.

  Áp vào r9 (việc của phiên soạn r9, không phải lời chủ kho): dòng reviewer, vế review của `required_checks`,
  `land_obligations` và ghi chú dưới closure viết lại cho đường subagent mức `review_deferred`; ba lớp của lượt 8 gắn
  với đường review (`hop-dong-dong-bang-thieu-neo`, `dong-reviewer-loi-khai-rong-hon-do`,
  `duong-review-b-chua-do-dau-cuoi`) xử lý như ghi ở §10; năm hunk của HINT lượt 8 chỉ phục vụ B không được áp (§9).
  Q12 không đổi mục tiêu, write set, nền nghiệm thu hay A1–A10, và không nới gate land: `review_deferred` thấp hơn
  mức `same_provider_approved` mà r8 nhắm tới, nên land dựa hẳn vào `human_audited`. Thân không kèm mô tả cho hai
  lựa chọn không chọn.

## 4. `write_set`

- `ops/lease_publish.py`
- `ops/lease_publish_test.py`

Không đường dẫn nào khác. Riêng đặc tả này (`ops/specs/lease-id-ep-kieu-yaml-r9.md`, và các bản r1–r8 nó thay) là hồ sơ
của lượt soạn spec, **không** thuộc write set của lượt thi hành.

Trong `ops/lease_publish_test.py` có ca của packet khác mà lượt thi hành phải giữ xanh (A8), và một ca **phải sửa**
vì chính việc của packet này: `t70` (:2995–3009 trên `20ec8d5`) so tập literal `mong` (13 tên) với mọi ca có
`_chay_buoc_dang` hoặc `_chay_buoc_dang_that` trong `co_names` (vị từ `_ca_doc_than_buoc` :2990–2991). Mọi ca mới gọi
một trong hai helper ấy, gồm ca biên A3 nếu nó dùng helper như phép đo ĐỎ của A3 (`_chay_buoc_dang_that`), phải được
thêm tên vào `mong`; đó là **nghĩa vụ trong write set** (§6 mục 8, A2), không phải mở rộng phạm vi và không phải sửa
đặc tả #677.

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
   sự thật mới. Ví dụ đã biết: `t178` :7789–7790 (trên `20ec8d5`; :7763–7764 trên `89fc4fa`, :7769–7770 trên `1741e0a`; thân `t178` giống hệt giữa ba nền, chỉ dời dòng) viết *"`lease_id` sai KIỂU thì không có chốt
   tương ứng trong `kiem()`"*. Executor phải grep tìm hết, đừng chỉ sửa chỗ này.
8. `ops/lease_publish_test.py` — Thêm tên mọi ca mới gọi `_chay_buoc_dang` hoặc `_chay_buoc_dang_that` (gồm ca
   biên A3 nếu nó gọi một trong hai helper ấy) vào tập literal `mong` của `t70`. Không đổi phép so literal thành phép đếm động và không nới vị từ
   `_ca_doc_than_buoc`: `t70` cố ý giữ tập mong đợi là literal độc lập (chú thích R1-F6 trong ca).

## 7. `nghiem_thu`

Mỗi tiêu chí nêu phép đo làm nó ĐỎ (L3). "Đột biến" nghĩa là chạy trên **bản sao tạm**, với
`PYTHONDONTWRITEBYTECODE=1`.

- **A1 (mục 1, D1)** — Ca mới: các dạng `true` `yes` `on` `1.5` `1.50` `0x1F` `017` `1_000`
  `5` `2026-09-29`, viết thành **văn bản YAML** và đọc qua `_doc_yaml` (không dựng dict bằng
  tay, để phép đo đi qua đúng lớp gây lỗi), đều cho `kiem()` ⇒ rc=8. Đối chứng `'yes'` có nháy
  ⇒ qua.
  **ĐỎ khi:** trả D1 về `str(lease["lease_id"])` ⇒ các dạng trên qua. Trên nền `20ec8d5` (mã `ops/lease_publish.py` giống hệt `89fc4fa` và `1741e0a`) ca
  này ĐỎ: đo 01:10:22Z 01-10 trên `20ec8d5`, cả mười dạng viết thành YAML, đọc qua `_doc_yaml` rồi
  `kiem(bo_qua_han=True)` ⇒ **qua** (kiểu bool, float, int, date), đối chứng `'yes'` ⇒ qua.
- **A2 (mục 1, D2)** — Mở rộng trục `lease_id` sai kiểu của `t178` thêm `int`; giữ chốt
  `_do_dau_da_dang` trả về bình thường và **0** lời gọi GitHub. Đo thêm D2 trực tiếp:
  `_tien_kiem_mien_dang` nhận `int` ⇒ `Chan(RC_NOI_DUNG)`; chuỗi hợp lệ ⇒ trả về.
  **ĐỎ khi:** trả riêng D2 về `(str, int)` ⇒ ca trực tiếp nhận trả về thay vì rc=8.
  Không đòi phép dò gọi GitHub khi D2 bị gỡ: D3 có chốt độc lập trước `_doc_gh`, nên vẫn
  có thể giữ số gọi bằng 0. Không dời chốt D3 xuống sau mạng chỉ để giết mutant D2.
  Tương tác #677: `L` gỡ riêng D2 nay có thể sống ở phép đếm mạng của `t178`; ca trực tiếp
  phải giết `L` bằng `TinHieuChotCa` đúng ca. Lịch sử (r1–r7, nay đã cũ, xem tọa độ r8 ngay dưới): #677 **chưa có đặc tả đóng băng** (Issue #677
  khai `revision 0`, đo 06:2xZ 29-09; vẫn chưa có đặc tả đóng băng tại 07:59Z 29-09, nội dung nghĩa vụ hai thứ tự dưới đây không đổi). Cập nhật đo 09:45Z 29-09: tệp `ops/specs/dot-bien-l-bien-cong-khai-r1.md` (sha256 `81468e21c7a7d32167d210b17813dab2b825992a1587b86d8bc8b3dc9142a4da`) đã có ở `refs/remotes/origin/claude/spec-dot-bien-l-bien-cong-khai-20260929` (`c78a5d06`), chưa có trên master; trạng thái đóng băng và lease của nó không đo ở lượt này, nên packet này vẫn không neo acceptance nào vào nó.
  Hai thứ tự, hai nghĩa vụ: packet này land TRƯỚC ⇒ đặc tả #677 phải được soạn trên nền mới
  và coi ca trực tiếp của A2 là nơi `L` chết; #677 land TRƯỚC ⇒ ca của #677 nằm trong
  `ops/lease_publish_test.py`, tức trong write set này, và lượt thi hành phải giữ nó xanh
  với ý nghĩa đã đổi. Executor **không** sửa đặc tả #677.
  **Tọa độ r8 (đo trên `20ec8d5`): nhánh thứ hai là nhánh đã xảy ra** (#677 land qua PR #689 trước khi cấp lease
  `wp678`, Q11). Đặc tả #677 đóng băng ở `ops/specs/dot-bien-l-bien-cong-khai-r7.md` (trên master từ `44620e8`). Ca
  của #677 trong `ops/lease_publish_test.py`: `t195` :10642 (tập (i), khoá dãy lời gọi rỗng), `t196` :10686 và `t197`
  :10704 (tập (ii), chỉ khoá `rc≠0`, 0 POST, không "bỏ qua", và theo docstring `t196` cố ý **không** khoá dãy lời gọi
  *"để giữ đúng khi #678 đổi đường từ chối"*), `t198` :10733 (đối chứng `wp-ok-1`, đúng 1 POST và đúng dãy bốn lời
  gọi), `t199`–`t202` :10744–11034; helper `_chay_buoc_dang_that` :10506. `t202` bơm vectơ quan sát của `L` **ghi cứng**
  (đo 30-09 trên `85124dc`), không chạy `L` sống. Docstring `t195`–`t197` khai `L` đổi kết quả các ô ấy; đó là phép
  đo trên `89fc4fa`, chưa đo trên ứng viên. Trên nền, cả tám ca xanh (A8). `t70` :2995–3009 (M6 của #677; vị từ `_ca_doc_than_buoc` :2990–2991) ghim một tập
  **literal** các ca gọi `_chay_buoc_dang` hoặc `_chay_buoc_dang_that`, nên ca biên A3, nếu gọi một trong hai helper ấy,
  phải được thêm tên vào tập ấy; review lượt 8 đo trên bản sao `20ec8d5`: thêm một ca gọi helper ⇒ `t70` ĐỎ (`0/1`), đối chứng
  cây gốc `1/1`. Phiên soạn r9 đo lại 05:20:07Z–05:20:08Z 01-10 trên cây `git archive 20ec8d5 ops .github`, lệnh
  `PYTHONDONTWRITEBYTECODE=1 python3 ops/lease_publish_test.py --chi-ca=t70_`: gốc `1/1`; thêm một ca `@ca` chỉ nhắc
  `_chay_buoc_dang_that` ⇒ `0/1`, dòng ĐỎ *"kiểm kê ca đọc thân bước lệch tập mong đợi"*; thêm cả tên ca ấy vào
  `mong` ⇒ `1/1`; 0 tệp `.pyc`. Đó là kiểm kê, không phải bằng chứng nhánh; nghĩa vụ sửa `mong` thuộc write set (§4,
  §6 mục 8).
  Sửa cả docstring D2 và `t178` để tách bằng chứng lịch sử khỏi hành vi sau D3.
- **A3 (mục 2, D3) — CA BIÊN WORKFLOW** — Thân bước `đăng` trích từ
  `.github/workflows/ops-publish-lease.yml` (dùng lại bộ trích sẵn có trong suite, không chép
  lại), `lease_publish.py` thật, `gh` giả **trên PATH** và **giữ trạng thái**. Issue đã có comment
  bot ``**Lease `True`**``; lease mới khai `lease_id: yes` ⇒ bước **khác 0** và **0 POST**. Kèm
  ca đối chứng dương: một `lease_id` chuỗi hợp lệ khác ⇒ bước 0 và đúng **1 POST**, để giàn hỏng
  không thể xanh.
  **ĐỎ khi:** chạy trên nền `20ec8d5` (`ops/lease_publish.py` và `.github/workflows/ops-publish-lease.yml` giống hệt
  `89fc4fa`; mã giống hệt `1741e0a`) ⇒ bước `rc=0`, 0 POST. Đo 01:10:22Z 01-10 trên `20ec8d5` bằng
  `_chay_buoc_dang_that` mà #677 đưa vào suite (thân bước `đăng` trích bằng `_buoc_workflow`, `gh` giả trên PATH, giữ
  trạng thái): `lease_id: yes` gặp comment bot ``**Lease `True`**`` ⇒ `rc=0`, **0 POST**, có dòng *"đã đăng trước đó —
  bỏ qua"*; đối chứng `'fresh-id'` ⇒ `rc=0`, **1 POST**. Lần đo đầu ở biên là của cross-review lượt 1 (§1).
  Nếu ca biên này gọi `_chay_buoc_dang_that` hoặc `_chay_buoc_dang` (phép đo ĐỎ ở trên dùng `_chay_buoc_dang_that`),
  phải thêm tên nó vào `mong` của `t70` (A2, §6 mục 8); quên thì `t70` ĐỎ trên ứng viên.
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
  (`20ec8d5`): suite **195/195**, rc=0, bỏ qua 0; 195 bằng số `^@ca` đếm tĩnh. Đo 01:11:15Z–01:16:50Z 01-10, cùng
  **một** lệnh dựng cả hai vế (`git clone --no-hardlinks`, `checkout --detach`, `core.abbrev 7`) với vế `89fc4fa`:
  **187/187**, rc=0, bỏ qua 0 (01:06:03Z–01:11:15Z); Python 3.11.15, PyYAML 6.0.1, git 2.43.0, shellcheck 0.9.0,
  actionlint 1.7.7; 0 tệp `.pyc` sau lượt ở mỗi vế. Tám ca thêm là `t195`–`t202` của #677 (A2). Lịch sử `89fc4fa`:
  187/187 đo 08:0xZ 29-09 trên commit merge `589336f` (cây của `89fc4fa` + các tệp spec). Lệnh: từ gốc repo chạy
  `PYTHONDONTWRITEBYTECODE=1 TMPDIR=<scratch> python ops/lease_publish_test.py`.
  Khi thi hành, đo lại **cả hai vế** (nền và ứng viên) trong **một** lệnh, cùng công cụ.
  `python -m ruff check --select F ops/lease_publish.py ops/lease_publish_test.py`: delta F = 0.
  **ĐỎ khi:** ứng viên có thêm ca đỏ (kể cả `t70` khi `mong` thiếu tên một ca mới gọi helper), hoặc có thêm lỗi F.
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
  `origin/master` `89fc4fa` (đọc và chạy lại 10:49Z; blob giống hệt trên `20ec8d5`, sha256 `dd17b94c…4f83`, nên mọi
  số dòng dưới giữ nguyên):
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
sử, không dùng làm số hiện tại. **r7 chỉ đo lại nền, ref, người giữ** (12:26Z–12:28Z 30-09, ở header); số khác giữ từ r6.
**r8 đo lại nền, ref, người giữ, suite, kích thước và ruff** (01:03Z–01:21Z 01-10, clone mới từ GitHub trong scratch,
không nông); các gạch dưới ghi số r8 trước, số r6/r7 sau với nhãn lịch sử. Số không ghi r8 là giữ từ r6.
**r9 đo lại nền, ref và người giữ** (05:17Z–05:18Z 01-10, clone sạch `adg2` sau `fetch --prune`), ghi trước số r8 ở ba
gạch ấy; suite, kích thước và ruff giữ từ r8, vì `origin/master` vẫn là `20ec8d5` nên hai tệp write set giống hệt nền
r8 đã đo (review lượt 8 tái lập: suite 195/195 và 187/187, ruff 9 lỗi F ở cả hai vế).

- **Nền.** r9 (05:17:33Z 01-10): `origin/master` = `20ec8d5`; `git diff --quiet 20ec8d5 origin/master -- <hai tệp>`
  rc=0 (05:18:23Z); nền giữ nguyên. r8 (01-10): `origin/master` = `20ec8d5` (clone mới 01:03:48Z, và lại 01:10:47Z); nền nghiệm thu **dời** sang
  đó (hàng nền nghiệm thu, Q11). `ops/lease_publish.py` giống hệt `89fc4fa` (`git diff --quiet` rc=0, sha256 blob
  `dd17b94c…4f83` cả hai nền); `ops/lease_publish_test.py` `600 15` (`git diff --numstat 89fc4fa 20ec8d5`). Lịch sử:
  `git fetch -q origin '+refs/heads/*:refs/remotes/origin/*'` rồi `git rev-parse
  origin/master`, đo 09:04Z, 09:44Z (r4), 10:14Z (r5) và 10:48Z (r6; `fetch` rc=0): cả bốn lần `89fc4fac8cea65979cc2483043dc8cd07a6e8518`.
  r7 (12:26:45Z 30-09): `origin/master` = `423b4ba`, hai tệp write set không đổi so `89fc4fa`; câu dưới là số r6.
  Nền nghiệm thu khi ấy không phải dời. `git diff --quiet origin/master -- ops/lease_publish.py
  ops/lease_publish_test.py` ⇒ rc=0 (10:49Z; trước đó 10:14Z và 09:46Z). Sau bước này chạy `git branch -f
  master refs/remotes/origin/master` (rc=0) để master cục bộ trùng `origin/master` `89fc4fac`, đúng điều kiện
  của mã chặn `CHẶN [12]`.
- **Ref.** r9 (05:17:40Z–05:17:41Z 01-10, `adg2`): 461/461 tên, lệch tên 0 dòng cả hai chiều, lệch tên + OID 0 dòng;
  `refs/replace` 0 ref, `refs/heads` 1 ref, `--is-shallow-repository` ⇒ `false`. r8 (01:10:48Z 01-10, clone mới): 459/459 tên, lệch tên + OID 0 dòng cả hai chiều (hàng `depends_on`);
  `refs/replace` 0 ref, `refs/heads` 1 ref (`master`), `--is-shallow-repository` ⇒ `false` (đếm 01:20:34Z). r7 (12:27Z
  30-09): 458/458 tên, lệch tên + OID 0 dòng. Số dưới là của r6 (10:48Z 29-09), nay là lịch sử. `git ls-remote --heads origin` (hỏi máy chủ) so `git for-each-ref
  refs/remotes/origin` (đọc đệm), theo **tập tên**, bỏ `HEAD`, `comm -23` và `comm -13`:
  máy chủ **511**, cục bộ **512**; `comm -23` (có trên máy chủ, thiếu cục bộ) **0 dòng**; `comm -13`
  (thừa cục bộ) **1 dòng**, `claude/bookkeeping-574-land`, mà `git ls-remote --heads origin
  claude/bookkeeping-574-land` trả rỗng, rc=0 (10:48Z, sau `fetch`, `ls-remote` rc=0). Chiều lệch là **thừa
  cục bộ**: ref đệm của một nhánh đã xoá trên máy chủ (`fetch` không kèm prune), vô hại, không phải mù.
  Vì `fetch` không prune nên số cục bộ 512 lớn hơn số 510 của r5 không chứng minh có thêm nhánh nào.
  `refs/replace` có 0 ref; `refs/heads` có 3 ref (r6: đếm 10:48Z; đếm lại 10:53Z sau `branch -f master`, vẫn 3).
  Lịch sử: 503 ở r1 (06:1xZ); 505 ở r2 (07:2xZ); 506 = 506 ở r3 (07:59Z); 510 = 510 ở r4 (09:44Z) và r5 (10:14Z).
- **Người giữ.** r9 (05:17:46Z–05:18:07Z 01-10, `adg2`): `ops/lease_publish.py` `NGƯỜI_GIỮ 0`, rc=0;
  `ops/lease_publish_test.py` `NGƯỜI_GIỮ 1: lease-publish-windows-do-r3-g3-claude`, **rc=11**, lease #687 generation 3
  giữ tới `2026-10-02T01:12:00Z` (hàng `depends_on`) ⇒ điều kiện (1) chưa thoả. r8 (01:10:52Z–01:11:15Z 01-10): hai tệp `NGƯỜI_GIỮ 0`, rc=0, ở clone mới; lease g6 của #677 đã rút
  hạn về 01:10:00Z (hàng `depends_on`); kho chính không đo lại. r7 (12:28Z 30-09): hai tệp `NGƯỜI_GIỮ 0` ở clone mới,
  rc=12 ở kho chính. Số dưới là của r6 (10:48Z–10:49Z), nay là lịch sử. `python ops/lease_publish.py ai-dang-giu ops/lease_publish.py` ⇒
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
- **Suite.** Nền hiện tại (`20ec8d5`, r8): **195/195**, rc=0, bỏ qua 0, 01:11:15Z–01:16:50Z 01-10; cùng một lệnh,
  vế `89fc4fa`: **187/187**, rc=0, bỏ qua 0, 01:06:03Z–01:11:15Z (chi tiết ở A8). Lịch sử `89fc4fa`: **187/187**, rc=0,
  bỏ qua 0, đo 08:0xZ 29-09 trên commit merge
  `589336f` (cây `89fc4fa` + tệp spec), `PYTHONDONTWRITEBYTECODE=1 python ops/lease_publish_test.py`
  với `shellcheck` 0.9.0 + `actionlint` 1.7.7. Không đo lại ở r4, r5 và r6 (hai tệp Python giống hệt
  `origin/master`, `git diff --quiet` rc=0 lúc 10:49Z, xem mục **Nền**). Reviewer lượt 7 tự đo 187/187, rc=0, bỏ
  qua 0 trên cả `89fc4fa` lẫn `423b4ba` (VERDICT lượt 7, hướng 9, 13:15Z–13:26Z 30-09). Reviewer lượt 4 tự đo
  187/187, rc=0, bỏ qua 0 (VERDICT lượt 4, không ghi UTC riêng cho phép đo này); reviewer lượt 5 tự đo
  187/187, rc=0, bỏ qua 0 (VERDICT lượt 5, `verify.py` 10:42:51Z).
  Lịch sử trên `1741e0a`: r1 khai 185/187 lúc container thiếu `shellcheck` (`t137`, `t159` báo
  `KHÔNG ĐO ĐƯỢC: thiếu shellcheck`); lượt 1 đo 187/187.
- **Kích thước.** r8 (01-10, `git show <nền>:<tệp> | wc -l`, `grep -c '^@ca'`): `ops/lease_publish.py` 2206 dòng ở
  cả `89fc4fa` và `20ec8d5`; `ops/lease_publish_test.py` **11087** dòng, **195** ca, số ca lớn nhất `t202` trên
  `20ec8d5` (không có `t193`, `t194`), so 10502 dòng, 187 ca, `t192` trên `89fc4fa`. Lịch sử (đo lại 10:51Z 29-09, kết
  quả bằng số đo 10:14Z): 2206 / 10502 trên `89fc4fa`; 10508 trên `1741e0a`.
- **Ruff.** r8 (01:20:42Z 01-10): `python -m ruff` vắng (`No module named ruff`), nhưng có nhị phân `ruff` 0.15.8.
  `ruff check --no-cache --select F ops/lease_publish.py ops/lease_publish_test.py`, chạy trên cả hai vế của A8:
  rc=1, **9** lỗi ở cả `89fc4fa` lẫn `20ec8d5` (7 `F401`, 2 `F541`, đều trong `ops/lease_publish_test.py`;
  `ops/lease_publish.py` 0), và tập lỗi (bỏ số dòng) giống nhau ⇒ #677 thêm 0 lỗi F. Đây là nền cho "delta F = 0" của
  A8. Lịch sử: `KHÔNG ĐO ĐƯỢC` ở phiên soạn r1–r7 (module vắng trong sandbox).

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

**Bộ đếm hình dạng sau lượt 7, và cách r8 xử lý.** Lượt 7 (trên r7) ra năm lớp, hai lớp tái mở:
`hop-dong-dong-bang-thieu-neo` nay có mặt ở lượt **1, 2 và 7**, `so-do-nen-khong-khop` ở lượt 1 và 7 (VERDICT lượt 7,
bảng đối chiếu). Một lớp có mặt ở ba lượt khác nhau đòi xét lại cách làm, không vá thêm chữ (PROTOCOL §12 :1054–1056;
ADR-0037). Vì vậy r8 **không** giữ nhóm 2 của HINT lượt 7 như đã viết (phương án A: ghi chú làm tiêu chí quyết định
được, nhưng model vẫn không đo được), mà đổi **cách chạy** reviewer sang phương án B của chính VERDICT ấy (model đo
bằng `modelUsage`, `session_run_id` từ launcher), giữ hai phần của nhóm 2 còn đúng: ghim băm định nghĩa và khai
`KHONG_do_duoc` cho effort. Nhóm 1, 3, 4, 5 (5 trong 6 hunk của HINT; nhóm 5 có 2 hunk) áp nguyên văn — áp cả HINT lên r7
bằng `patch -p0 --fuzz=0` cho rc=0, 6/6 hunk (review lượt 8 đo lại cùng kết quả) — rồi cập nhật theo Q11 và
nền mới. Đây là lời khai về cách làm, không phải lời khai rằng lớp đã sạch; lượt review của r8 kiểm điều đó.
Phiên soạn r9 tái lập phép áp cả HINT lượt 7 lên r7 (05:26:09Z 01-10): rc=0, 6/6 hunk, 0 fuzz.

**Bộ đếm hình dạng sau lượt 8, và cách r9 xử lý.** Lượt 8 (trên r8) ra 0 P1 / 4 P2 / 3 P3, bảy lớp;
`hop-dong-dong-bang-thieu-neo` nay có mặt ở lượt **1, 2, 7 và 8**, và tỷ lệ lớp ĐÃ VÁ THẬT trên số lớp còn mở cuối lượt
7 là 0/5 (1/5 nếu người điều phối bác việc nối F8-9 vào `so-do-nen-khong-khop`), dưới ngưỡng 50% của PROTOCOL §12
(VERDICT lượt 8, đối chiếu lượt trước). Theo §12 đó là điểm dừng vòng vá và Review Rescue Checkpoint; câu hỏi *"lượt
review thi hành chạy bằng đường nào"*, mà VERDICT khuyến nghị đưa lên chủ kho trước r9, đã được hỏi và trả lời ở Q12.
Hai trong bốn P2 của lượt 8 sinh từ phương án B, tức từ một cách làm phiên soạn r8 tự chọn; r9 không vá B mà bỏ B theo
Q12, nên đây là đổi cách làm có quyết định chủ kho, không phải vá thêm chữ.
Cách áp HINT lượt 8 (VERDICT `68da880f…fe82`, HINT `41e3763c…a400`, 11 hunk trong 7 nhóm), đo 01-10 trong scratch của
phiên soạn r9, GNU patch 2.7.6: (1) áp **cả** HINT lên một bản sao r8 (chỉ `sed` đổi đường dẫn ở các dòng `---`/`+++`),
`patch -p0 --fuzz=0` rc=0, 11/11 hunk, 0 fuzz, 6 hunk báo offset, 890 → 927 dòng (khớp số VERDICT báo); (2) dựng nền r9
từ HINT **bỏ 5 hunk chỉ phục vụ B**: hai hunk của nhóm `dong-reviewer-loi-khai-rong-hon-do` (dòng reviewer, mục (c)),
hunk 1 của `hop-dong-dong-bang-thieu-neo` (mục (b), vân tay argv), hai hunk của `duong-review-b-chua-do-dau-cuoi`
(bootstrap trust, lượt khói); **giữ 6 hunk**: hunk 2 của `hop-dong-dong-bang-thieu-neo` (ghi chú Q10 về điều kiện
(3)), hai hunk của `thu-tu-677-bo-ngo-o-dieu-kien-cap`, và một hunk mỗi nhóm `q10-he-qua-mat-nhan-dien-giai`,
`so-do-nen-khong-khop`, `tuong-tac-677-kiem-ke-t70-chua-neu`; HINT đã lọc áp lên một bản sao r8 mới, `patch -p0
--fuzz=0` rc=0, 6/6 hunk, 0 fuzz, 3 hunk báo offset 4 dòng, 890 → 902 dòng; (3) sửa tay hai câu trong hunk giữ mà Q12
làm sai: *"chủ kho chưa được hỏi riêng về nó"* ở `nguon_cap_viec`, và *"khác vế review của `required_checks` trên PR thi
hành"* ở ghi chú Q10; sửa thêm một câu của hunk `tuong-tac-677-kiem-ke-t70-chua-neu` cho đúng phạm vi đo (*"ca biên A3
(gọi một trong hai helper ấy)"* thành có điều kiện, vì A3 chỉ đòi dùng lại bộ trích sẵn có, không đòi gọi helper) và
thêm vào phần tổng quát hoá của điều kiện (4) chốt *"trên cùng kho vừa qua phép so tập tên ref ở (1)"*; đo lại các số
mà hunk giữ ghi "review lượt 8 đo" (23 tệp lease và 8 packet; đột biến `t70`) và
ghi số của phiên soạn r9 cạnh chúng; (4) rồi viết phần của Q12 (dòng reviewer, closure, ghi chú dưới closure, §3,
§10), §4, §6 mục 8, A3, A8, §8 và header. Đây là lời khai về cách làm, không phải lời khai rằng lớp đã sạch; lượt
review của r9 kiểm điều đó.

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
- Ruff: r8 đo được nền (§8: 9 lỗi F ở tệp test, 0 ở `ops/lease_publish.py`, giống nhau trên `89fc4fa` và `20ec8d5`);
  delta F của ứng viên chưa đo vì chưa có ứng viên. r9 không đo lại ruff (nền không đổi). Lịch sử: `KHÔNG ĐO ĐƯỢC` ở phiên soạn r1–r7; r7 khai cũng vậy ở mọi
  lượt review tới lúc ấy.
- Băm thân Mission Issue #682 ở phía nhận: r8 đọc qua REST và ghi `76bee6fb…0dd2` (01:08:54Z 01-10, đoạn miễn trừ),
  một phép đo tại một thời điểm. Lịch sử: `KHÔNG ĐO ĐƯỢC` ở r6 (đường đọc MCP chuẩn hoá thực thể
  HTML); r7 đọc #682 qua REST nhưng không ghi băm; r9 đọc lại 05:22Z 01-10, cùng băm, 3416 byte. Descriptor vẫn neo bằng số Issue + object ID `5627190292`.
- **Đường `claude -p` qua `launcher.py run` (phương án B của r8): BỎ ở r9 theo Q12.** Phép dò 01:07Z 01-10 của r8 (một
  lượt `claude -p` ngắn, không qua launcher) và các phép đo của review lượt 8 (`run.json` không lưu argv; validator
  nhận mọi chuỗi ở `session_run_id`; probe `claude_trust` của launcher chặn `CHAN [15]` ở sandbox chưa trust, đo với
  `claude` giả) giữ làm lịch sử. Trust và quyền công cụ ở chế độ `-p`, hành vi `claude` thật qua launcher: `KHÔNG ĐO
  ĐƯỢC`, và packet này không còn cần đo chúng. Lớp `duong-review-b-chua-do-dau-cuoi` (lượt 8) **đóng vì bỏ B**, không
  phải vì B đã được đo đầu cuối.
- **Hai lớp còn lại của đường review (lượt 8), trạng thái ở r9.** `hop-dong-dong-bang-thieu-neo`: closure và ghi chú
  dưới nó nay chỉ khai thứ kiểm được (mức và chế độ qua `_thieu`, băm định nghĩa, VERDICT sạch) và khai model/effort đã
  phục vụ là `KHONG_do_duoc`; điều kiện cấp (3) kiểm cùng cách (ghi chú Q10, §3). Lớp đóng ở mức *"neo vào thứ kiểm
  được"*, **không** phải *"đã đo model"*: model và effort phục vụ lượt chạy vẫn `KHÔNG ĐO ĐƯỢC`.
  `dong-reviewer-loi-khai-rong-hon-do`: r9 không còn lời khai *"phiên và context mới"*, không dùng `session_run_id` làm
  bằng chứng độc lập, và không dẫn tiền lệ `same_provider_approved` nào (cả `don-nhanh-base-review-7` lẫn
  `pr492-review-4`), vì mức `review_deferred` không đòi bằng chứng độc lập; tiền lệ đúng cho đường subagent là
  `phan-bien-quy-trinh-review-{1,2}`.
- Lease T131 còn giữ `ops/lease_publish_test.py` là trạng thái đo 07:59Z 29-09 (lịch sử); đo 09:44Z và
  10:14Z cả hai tệp `NGƯỜI_GIỮ 0` và lease T131 ở nhãn `HẾT_HẠN`. **Đo 10:48Z–10:49Z (r6):**
  `ops/lease_publish_test.py` do lease `lease-publish-windows-do-r1-g1-claude` (#687) giữ tới
  `2026-09-30T10:20:00Z`, nên điều kiện cấp (1) của Q8 chưa thoả. Người giữ có thể đổi bất kỳ lúc nào;
  vẫn phải đo lại (`ai-dang-giu`, kèm so tập tên ref) lúc cấp lease cho `wp678`. Chưa đo được: #687 có
  land trước hay không và có đổi `ops/lease_publish_test.py` hay không (điều kiện 4 của Q8); nếu có thì
  cần revision mới dời nền. **r7 (30-09):** hai lease #687 `HẾT_HẠN`, hai tệp `NGƯỜI_GIỮ 0` ở clone mới, #687
  chưa land tới `423b4ba` (hàng `depends_on`); vẫn phải đo lại lúc cấp. **r8 (01-10):** hai lease #687 vẫn `HẾT_HẠN`,
  #687 chưa land tới `20ec8d5`, hai tệp `NGƯỜI_GIỮ 0` ở clone mới (hàng `depends_on`); vẫn phải đo lại lúc cấp.
  **r9 (01-10, 05:17Z–05:18Z):** `ops/lease_publish_test.py` do lease `lease-publish-windows-do-r3-g3-claude` (#687,
  generation 3, cấp `2026-10-01T01:12:00Z`) giữ tới `2026-10-02T01:12:00Z`, nên điều kiện (1) chưa thoả; #687 chưa land
  tới `20ec8d5` (= `origin/master` lúc đo). #687 land và đổi tệp ấy ⇒ điều kiện (4) ⇒ revision mới dời nền trước khi
  cấp.
- **Nhánh thi hành #677 đổi một tệp write set mà chưa land (đo r7, 30-09; nay đã land và lớp đã đóng, xem cuối
  gạch).** Đặc tả #677 đã vào master (PR
  #684, `44620e8`). Nhánh `claude/dot-bien-l-bien-cong-khai-20260929` (đầu `8e630c0`, 09:48:22Z, merge-base
  `423b4ba`) đổi `ops/lease_publish_test.py` +596/−15 (`git diff --stat origin/master...<nhánh>`). Năm lease
  `exec-1`…`exec-5` của #677 giữ tệp ấy tới `2026-09-30T10:48:00Z`, output `ai-dang-giu` 12:28Z ghi cả năm
  `HẾT_HẠN`. Commit `6112b89` ghi *"chủ kho chốt #677 đi trước"* (lời khai trong commit), nhưng thứ tự còn có nguồn
  **trên master**: đặc tả #677 r7 (`ops/specs/dot-bien-l-bien-cong-khai-r7.md`, có từ `44620e8`) ghi quyết định chủ
  kho *"Sau #676: #677 rồi #678"* (Q10 của #677, bảng §3) và *"#677 trước #678"* (§9, Q7/Q10); Q15 của nó (29-09)
  ghi PR mã #689 còn lượt codex cuối, và `git log 423b4ba` không có merge nào của #689. Lease #677 hết hạn nên điều
  kiện (1) không còn chặn, trong khi land authority tách khỏi executor lease (PROTOCOL :255–259): #689 có thể land
  giữa lượt thi hành `wp678`, còn nếu #677 cần lease mới trên tệp ấy thì bị lease `wp678` chặn. Q8 không được trích
  nguyên văn ở r6/r7, và 6/6 biên nhận `ops/reviews/wp678-spec-review-*-codex-verdict.receipt.yaml` tóm Q8 là
  *"cap sau khi lease cua #687 va #677 nha ops/lease_publish_test.py"*, nên câu "không phải điều kiện Q8" chưa có
  phép đo. **Theo Q4, bên cấp lease không tự suy thứ tự từ bốn điều kiện:** trước khi cấp, hỏi chủ kho thứ tự
  `wp678` ↔ #677 (câu hỏi nêu PR #689 và nhánh trên) và ghi câu trả lời bền; chưa có ⇒ không cấp. #677 land trước
  và đổi `ops/lease_publish_test.py` ⇒ dời nền bằng revision mới trước khi cấp, như điều kiện (4).
  **Đã thi hành ở r8 (đo 01-10).** Câu trả lời bền là Q11 (§3, #682 comment `5912559230`): thứ tự LAND, không cấp lease
  `wp678` tới khi #677 land. #677 đã land: PR #689 `merged: true` lúc `2026-10-01T00:55:22Z`, merge commit `20ec8d5` =
  `origin/master` (REST và clone mới, hàng `depends_on`); nhánh `8e630c0` là tổ tiên của `20ec8d5` (`merge-base
  --is-ancestor` rc=0), `git diff --numstat 423b4ba...8e630c0` ⇒ `596 15` như r7 khai, và hai commit sau nó
  (`3c308b3`, `adad5f5`) đưa chênh đã land lên `600 15`. r8 là revision dời nền (hàng nền nghiệm thu) và thêm điều kiện
  (5). Nguyên văn Q8 nay đo được (§3 Q8): thân **không** nhắc #677, nên câu "không phải điều kiện Q8" của r7 khớp thân
  Q8, còn lời tóm của 6/6 biên nhận rộng hơn thân. Commit `6112b89` nay có trong clone mới (trên
  `origin/claude/lease-publish-windows-do`); tiêu đề của nó có đúng cụm *"chủ kho chốt #677 đi trước"*. Lớp
  `thu-tu-677-bo-ngo-o-dieu-kien-cap` (lượt 7): biểu hiện (i), (ii) và phần #677 của (iii) **đóng theo Q11**, kiểm bằng
  điều kiện (5) và nền `20ec8d5`; phần tổng quát của (iii), tức điều kiện dời nền chỉ nêu tên #687/#677, đóng bằng điều
  kiện (4) tổng quát hoá (r9, theo HINT review lượt 8). Write set này là điểm nóng: trên `20ec8d5`, 23 tệp `ops/leases/*.yaml` khai giữ
  `ops/lease_publish*.py`, thuộc 8 packet khác nhau (#203, #206, #227, #238, #244, #396, #579, #676), chưa kể #677 và
  #687 (review lượt 8 đo; phiên soạn r9 đo lại 01-10 trên `git archive 20ec8d5 ops/leases` cộng `yaml.safe_load`:
  119 tệp lease, 0 lỗi parse, cùng 23 tệp và 8 packet). Hiện trạng r9 cho thấy điều kiện (4) không phải giả định: lease
  #687 generation 3 đang giữ `ops/lease_publish_test.py` (hàng `depends_on`).
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
  của nó không đo ở lượt này (xem A2). r8: đặc tả #677 r1–r7 đã trên master (PR #684, `44620e8`), bản đóng băng là
  r7; mã của #677 land ở `20ec8d5` (xem A2, tọa độ r8).
- Trạng thái máy chủ GitHub ngoài `ls-remote`: không đo ở r6 (REST tới `repos/…` bị proxy chặn ở phiên soạn
  r6). Phiên soạn r7 gọi được REST `repos/…` (HTTP 200, có `X-Github-Request-Id`), chỉ để đọc Q10 và #682. Phiên soạn
  r8 cũng gọi được (HTTP 200, có `X-Github-Request-Id`), chỉ để đọc Q11, Q8, #682, PR #689 và #678 comment
  `5912542067`. Phiên soạn r9 gọi REST không token (HTTP 200, có `X-Github-Request-Id`), chỉ để đọc #682 (thân và
  comment, Q12), PR #689 và các comment của #678.
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
