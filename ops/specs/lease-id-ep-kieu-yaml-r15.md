# ĐẶC TẢ — `LEASE-ID-EP-KIEU-YAML` — **revision 15, ĐÓNG BĂNG**

**Thay đổi so với r14** (theo review lượt 14 trên r14, dưới Q13). Mục tiêu (hàng `objective`), write set (§4), nền nghiệm
thu (`ab457c6`), mọi giá trị trong bảng closure, nội dung năm điều kiện cấp (điều kiện (3) chỉ đổi số revision), chuỗi lệnh
đo điều kiện cấp và `s5.py` (giống từng byte r14, OID `c730245c…2694`), và ngữ nghĩa A1–A7, A9, A10 **không đổi**. Đổi:
phép quét động của A8 (theo HINT lượt 14: `threading.setprofile` cài trước khi nạp, vế lật theo độ sâu trên mọi luồng, tập
L, câu H2, tạo tác toàn tiến trình, giới hạn khai theo tính chất (α), (β), (γ)); số đo hiện tại. Đây là revision mới vì đặc
tả đóng băng đổi byte (công thức băm).

**r15 giữ nền `ab457c6`.** REST `gh api repos/ducthangho/tra-luat/commits/master` (chỉ đọc) lúc 17:18:24Z 07-10 trả
`ab457c6…`; `adg2` (chỉ đọc; `FETCH_HEAD` 17:17:01Z 07-10, không do phiên soạn r15 fetch): `origin/master` = `ab457c6`,
`git diff --quiet ab457c6… refs/remotes/origin/master -- <hai tệp>` rc=0, `ls-tree` hai tệp ra 2 dòng (blob `93cff2f…`,
`7dd06ab…`), nên điều kiện (4) rc=0 tại lúc đo và không dời nền. r15 không chạy lại chuỗi lệnh cấp (khối lệnh và `s5.py`
không đổi byte); số của lượt chạy thật gần nhất là của r13 (13:12:13Z–13:13:11Z, hàng `depends_on`), không phải số lúc cấp.
Điều kiện (3) chưa thoả (r15 chưa review), nên vẫn **không cấp**; mọi điều kiện phải đo lại lúc cấp.

| chỗ | r14 | r15 |
|---|---|---|
| A8, phép quét động | vế lật cài `threading.setprofile` sau khi nạp và trả *"giá trị lúc vào khung"*; giới hạn khai theo danh sách E5f, E8e, E8g, E8l | HINT lượt 14: cài `threading.setprofile` trước khi nạp; lật theo độ sâu trên mọi luồng; sau mỗi ca trả giá trị gốc và ghi tập L; câu H2 thêm điều kiện cần; tạo tác toàn tiến trình khai như tạo tác của seam; giới hạn khai theo tính chất (α), (β), (γ); đoạn *Review lượt 14 đo*. Phiên soạn r15 sửa thêm theo đo: giá trị gốc là `os.name` lúc bộ quét bắt đầu (V9), (α) nêu E8u, E8v, tạo tác nêu V10, danh sách của handoff viết theo tính chất; đoạn *Phiên soạn r15 đo lại* |
| số đo hiện tại | phiên soạn r14 | phiên soạn r15: `quet14.py` và `quet14b.py` trên cùng cây, ma trận 69 hàng và quét đủ nền ở 3.11, 3.12 trong một lệnh |
| dòng dõi, §3, §8, §9, §10 | r13, lượt 13 | r14, lượt 14; §9 bộ đếm sau lượt 14 và chỗ HINT lượt 14 chưa đủ hay sai so với đo |

Bảng thay đổi r13 → r14 nằm ở đầu r14 (xem `thay_the_cho`).

| trường | giá trị |
|---|---|
| `schema_version` | 1 (protocol §3.2) |
| `packet_id` | `wp678` (ID bền theo protocol §3.2, `wp<issue>`); tên đọc được: `LEASE-ID-EP-KIEU-YAML`. Hai tên chỉ cùng một packet; lease dùng `wp678` hoặc tên đọc được đều phải kèm `packet_issue: 678`. |
| `revision` | **15** |
| `thay_the_cho` | revision 14: `ops/specs/lease-id-ep-kieu-yaml-r14.md`, sha256 `ec4d97f5488cc5da27a97daec9b617428e42774139fa632fe6008b315e59b0ed`, commit `284a03fa6eff0356a79cca2926b889a6a98896f0` (cha `35e7f9c`). Đây là commit TẠO tệp: trong worktree soạn r15, `git log --diff-filter=A --format=%H -- <tệp>` ra giá trị ấy (commit 2026-10-07T15:38:20Z), đúng 1 commit chạm tệp, và `sha256sum` trên output của `git show 284a03f:<tệp>` ra đúng băm trên (2632 dòng; đo 17:18:19Z 07-10). Định danh r14 là băm và OID, không phải tên nhánh: lúc soạn r15 commit ấy **chưa** có trên GitHub (REST `gh api repos/ducthangho/tra-luat/commits/284a03f…` lúc 17:18:24Z 07-10 trả HTTP 422 *"No commit found"*; `adg2` `git cat-file -t 284a03f…` báo không lấy được object), nên tra theo OID, trên GitHub nếu đã đẩy, chưa thì ở nhánh `claude/spec-wp678-r7` của phiên điều phối. r14 được review lượt 14 (reviewer độc lập do phiên điều phối giao; VERDICT tự khai Claude Opus 5.5 `claude-opus-5-5` effort `max`, chạy như subagent, và ghi rằng chỉ dẫn hệ thống nó nhận trùng nguyên văn thân định nghĩa `review-opus-max` nhưng model và effort đang phục vụ là `KHÔNG ĐO ĐƯỢC`; tự khai là cấu hình được giao, không phải runtime evidence; trên `284a03f`): `changes_requested`, 0 P1 / 1 P2 / 0 P3 theo lớp; VERDICT sha256 `69f5f01072227ef8481f5fb9cf6ba9bcaf2ff45ecc5fd6a8bacf7bfc3ba2eb6b` (218 dòng), HINT sha256 `7a8976acfd7c4305ac60566868f0f2f593cc89b86b39fe5d1e066f21557e85e3` (1 nhóm, 4 hunk); bản chiếu ở #678 comment `6042680156` (tạo 17:01:33Z 07-10, app `claude`; đọc qua REST `gh api` của phiên lúc 17:18:34Z 07-10: thân 2693 byte, sha256 `86e352e1265a0f905b5121255a4892c8c7c7f183181b2f7197875109ddeb817d`, 0 thực thể HTML, là bản TÓM TẮT có hai băm trên và tự ghi *"Comment này là bản chiếu của tệp verdict cục bộ."*, không chép nguyên VERDICT; dòng `reviewer` của bản chiếu ghi `review-opus-max` là lời của phiên điều phối, không phải phép đo). Chuỗi r1–r13: xem hàng `thay_the_cho` của r14 (r13 `711b7b74…4bb1`, commit `35e7f9c`, review lượt 13 `changes_requested`). |
| `packet_issue` | **#678** |
| `mission_issue` | **#682** (Mission Issue, object ID `5627190292`, tạo 29-09-2026, tiêu đề *"Mission wp678: quyết định chủ kho + miễn trừ closure có phạm vi cho LEASE-ID-EP-KIEU-YAML"*). Issue này do **phiên agent đăng HỘ chủ kho** bằng credential chủ kho, nên `author_association: OWNER` không chứng minh chủ kho tự gõ; nguồn thẩm quyền là các câu trả lời của chủ kho trong phiên (Q0–Q6) được trích trong thân #682; Q7 do chủ kho chốt sau đó và ghi ở #682 comment `5888143430`; Q8 ở #682 comment `5888631719`; Q9 ở #682 comment `5888660607`; Q10 ở #682 comment `5911243074`; Q11 ở #682 comment `5912559230`; Q12 ở #682 comment `5925190705` (xem §3); Q13 ở #682 comment `5928886724` (tạo `2026-10-01T09:44:15Z`), là bản chiếu lời khai của phiên điều phối (xem §3). Packet cha #579 (đặc tả `ops/specs/dang-lease-dau-truoc-kiem-sau-r30.md`) không khai `mission_issue` và không cấp ngoại lệ gì cho packet này. |
| `nguon_cap_viec` | Phát hiện phụ của #677 (mục *"Phát hiện phụ — TÁCH packet riêng"*). Chủ kho quyết định tách packet 29-09-2026, rồi trả lời *"Đồng ý"* trong phiên cho ba đề xuất: (a) mở Issue + soạn đặc tả; (b) chỉ nhận **chuỗi thật**, bỏ cả `int`; (c) xếp sau `T131-DEADLINE-DEM-SPAWN`. Q3 xác nhận riêng: #678 comment `5885268193`. **r2** là hệ quả của cross-review lượt 1 trên PR #679 (comment `5885578969`, VERDICT sha256 `d4acdd38…b8add`), dưới chỉ thị chủ kho *"cross-review #679 đi, theo phân lớp, không theo từng lỗi, có hint patch"*. **r3** là hệ quả của cross-review lượt 2 trên PR #679 (comment `5886034260`, VERDICT sha256 `aa9a68d3…d4882`: 1 P1 / 3 P2 / 1 P3 theo lớp), và của quyết định chủ kho chọn neo lớp P1 bằng Mission Issue mới (#682). **r4** là hệ quả của cross-review lượt 3 trên PR #679 (comment `5887068702`, VERDICT sha256 `1eb00c7a…7e819`: 0 P1 / 2 P2 / 1 P3 theo lớp; P1 của lượt 2 đã đóng). **r5** là hệ quả của cross-review lượt 4 trên PR #679 (comment `5888141866`, VERDICT sha256 `9abc767695097d523d4e5faedd6929678f71c4d21b9fca620480230575986ed3`: 0 P1 / 1 P2 / 0 P3 theo lớp; lớp `bo-quet-chung-cu-khong-neo-anh`), của điều kiện dừng đã đăng ký ở comment `5887068702` (§9), và của quyết định Q7 của chủ kho (Mission #682, comment `5888143430`; §3). **r6** là hệ quả của cross-review lượt 5 trên PR #679 (comment `5888630117`, VERDICT sha256 `ce14afd8ba46d5b17bc1f121b2ae8fe042771af37847acdbd348ecb9942ac33d`: 0 P1 / 2 P2 / 0 P3 theo lớp; hai lớp `bo-quet-chung-cu-khong-neo-anh` và `bo-quet-nghiem-thu-thieu-mien`) và của hai quyết định chủ kho ở Mission #682: Q8 (uỷ quyền cấp lease `wp678`, thứ tự và bốn điều kiện cấp; comment `5888631719`) và Q9 (toàn vẹn object-store nằm NGOÀI phạm vi A9); §3. **r7** không vá finding nào: cross-review lượt 6 (VERDICT sha256 `9569bf0d715fe8daed90aba00ccdb2e39262dd12f094713ceb38722f8d10c18d`) approve r6 với 0 P1/P2/P3. r7 là hệ quả của quyết định Q10 của chủ kho (Mission #682, comment `5911243074`; §3): codex, reviewer của r6, hết quota, nên reviewer lượt thi hành và vế review của `required_checks` đổi sang Claude Opus 5.5 `max`. **r8** là hệ quả của review lượt 7 trên r7 (`088511f`; VERDICT sha256 `992eb9f0…794c`: 0 P1 / 2 P2 / 3 P3 theo lớp, xem `thay_the_cho`) và của quyết định Q11 của chủ kho (Mission #682, comment `5912559230`; §3): thứ tự #677 rồi #678 là thứ tự LAND, nên r8 soạn sau khi #677 land, dời nền nghiệm thu sang master sau #677 và thêm điều kiện cấp (5) (lựa chọn chủ kho đã chọn). Cụm *áp HINT lượt 7 trong một lần* chỉ có trong đoạn Hệ quả mà chính comment Q11 gắn nhãn diễn giải của phiên agent, không phải lời chủ kho; r8 không áp nhóm 2 của HINT ấy như đã viết (§9). Phương án B cho lượt review thi hành (dòng reviewer của r8) là lựa chọn của phiên soạn r8 trong phạm vi Q10 (Opus 5.5 `max`, hạ assurance vì cùng họ), **không** phải quyết định của chủ kho; tới r8 chủ kho chưa được hỏi riêng về nó, và khi được hỏi ở Q12 thì chủ kho bỏ nó. **r9** là hệ quả của review lượt 8 trên r8 (`f958e14`; VERDICT sha256 `68da880f…fe82`: 0 P1 / 4 P2 / 3 P3 theo lớp, xem `thay_the_cho`) và của quyết định Q12 của chủ kho (Mission #682, comment `5925190705`; §3): chủ kho chọn *"A: subagent, review_deferred (Recommended)"*, nên r9 bỏ phương án B, chạy review lượt thi hành bằng subagent mức `review_deferred`, land bằng `human_audited`, và áp HINT lượt 8 trừ năm hunk chỉ phục vụ B (§9). Cụm *đơn giản hóa closure, đóng hai P2 của B* nằm trong mô tả kèm của lựa chọn đã chọn; cách r9 làm điều đó cụ thể ra sao là việc của phiên soạn r9. **r10** là hệ quả của review lượt 9 trên r9 (`2469f3e`; VERDICT sha256 `bb5bf15b…ee31`: 0 P1 / 2 P2 / 2 P3 theo lớp, xem `thay_the_cho`) và của quyết định Q13 tại Review Rescue Checkpoint (§3, §9): lượt 9 ghi chuyển tiếp 8→9 là chuyển tiếp thứ hai liên tiếp dưới 50%, phiên điều phối dừng vòng vá và hỏi chủ kho, chủ kho chọn *"Áp HINT, lặp không trần"*. r10 áp cả HINT lượt 9 rồi sửa thêm theo phép đo của chính phiên soạn r10 (§9). Nguồn của Q13 là lời khai của phiên điều phối, chiếu lên #682 comment `5928886724` (hàng `mission_issue`). r10 còn dời nền nghiệm thu sang `163fd5d` vì #687 land và đổi một tệp write set (điều kiện (4)); gộp việc ấy vào r10 là quyết định của phiên điều phối, không phải câu hỏi đã hỏi chủ kho. **r11** là hệ quả của review lượt 10 trên r10 (`42292b4`; VERDICT sha256 `2046565a…384e`: 0 P1 / 2 P2 / 2 P3 theo lớp, xem `thay_the_cho`) và của Q13 (§3): chuyển tiếp 9→10 là 1/4 khi đọc chặt (2/4 nếu tách F10-6), chủ kho đã quyết lặp không trần, nên phiên điều phối giao soạn r11; r11 áp cả HINT lượt 10 rồi sửa thêm theo phép đo của chính phiên soạn r11 (§9). r11 không dời nền. **r12** là hệ quả của review lượt 11 trên r11 (`e48423a`; VERDICT sha256 `7082d6db…1c9f`: 0 P1 / 2 P2 / 0 P3 theo lớp, xem `thay_the_cho`) và của Q13 (§3): tỷ lệ vá thật 10→11 là 2/4 (VERDICT lượt 11), chủ kho đã quyết lặp không trần, nên phiên điều phối giao soạn r12; r12 áp cả HINT lượt 11 rồi sửa thêm theo phép đo của chính phiên soạn r12 (§9). r12 còn dời nền nghiệm thu sang `ab457c6` vì wp709 land và đổi cả hai tệp write set (điều kiện (4)); gộp việc ấy vào r12 là chỉ thị của phiên điều phối, không phải câu hỏi đã hỏi chủ kho. **r13** là hệ quả của review lượt 12 trên r12 (`d5a57c1`; VERDICT sha256 `eb28deae…2e3f`: 0 P1 / 2 P2 / 1 P3 theo lớp, xem `thay_the_cho`) và của Q13 (§3): tỷ lệ vá thật 11→12 là 0/2 theo lớp (5/5 theo finding; VERDICT lượt 12), chủ kho đã quyết lặp không trần, nên phiên điều phối giao soạn r13; r13 áp cả HINT lượt 12 rồi sửa thêm theo phép đo của chính phiên soạn r13 (§9). r13 không dời nền: `origin/master` vẫn là `ab457c6` (hàng nền nghiệm thu). **r14** là hệ quả của review lượt 13 trên r13 (`35e7f9c`; VERDICT sha256 `372efdfe…c244`: 0 P1 / 1 P2 / 1 P3 theo lớp, xem `thay_the_cho`) và của Q13 (§3): tỷ lệ vá thật 12→13 là 1/3 theo lớp (9/9 theo finding; VERDICT lượt 13), chủ kho đã quyết lặp không trần, nên phiên điều phối giao soạn r14; r14 áp HINT lượt 13 rồi sửa thêm theo phép đo của chính phiên soạn r14 (§9). r14 không dời nền: `origin/master` vẫn là `ab457c6` (hàng nền nghiệm thu). **r15** là hệ quả của review lượt 14 trên r14 (`284a03f`; VERDICT sha256 `69f5f010…eb6b`: 0 P1 / 1 P2 / 0 P3 theo lớp, xem `thay_the_cho`) và của Q13 (§3): tỷ lệ vá thật 13→14 là 1/2 theo lớp (3/4 theo finding; VERDICT lượt 14), chủ kho đã quyết lặp không trần, nên phiên điều phối giao soạn r15; r15 áp HINT lượt 14 rồi sửa thêm theo phép đo của chính phiên soạn r15 (§9). r15 không dời nền: `origin/master` vẫn là `ab457c6` (hàng nền nghiệm thu). |
| `objective` | Mọi đường đưa `lease_id` vào danh tính chỉ nhận chuỗi thật khớp `LEASE_ID`, đóng va chạm do ép giá trị không phải chuỗi thành chuỗi. Danh tính là giá trị sau `yaml.safe_load`: các cách viết ra cùng một chuỗi hợp lệ cố ý là cùng danh tính (ví dụ `'yes'` và `!!str yes`), không yêu cầu phân biệt cú pháp YAML. |
| `review_class` | **`sensitive`**: chạm `ops/lease_publish.py`, tức cổng đăng lease. |
| `risk` | **`sensitive`**: cùng lý do. |
| `executor` | `claude` (Claude Opus 5.5, effort ≥ medium) |
| `environment` | **`cloud`**. Packet không đo hành vi phụ thuộc nền (không đồng hồ ngủ máy, không đường dẫn Windows); tiền lệ các đặc tả `ops/specs/*` cùng lớp khai `cloud`. Chủ kho đổi thì phải ra revision mới. |
| reviewer | **Đổi ở r7 (Q10); đường chạy chốt ở r9 theo Q12** (bỏ phương án B của r8). Subagent `review-opus-max` do phiên điều phối giao việc, cấu hình Claude Opus 5.5 (`claude-opus-5-5`), effort `max`; cùng đường với hai lượt review đặc tả 7 và 8. Định nghĩa nằm ở phạm vi người dùng (`~/.claude/agents/review-opus-max.md`), **không** có trong kho, nên bị ghim bằng băm ở ghi chú dưới closure; băm ấy ghim CẤU HÌNH được giao, **không** phải nguồn đo runtime. Model và effort đã phục vụ lượt chạy: `KHONG_do_duoc` (PROTOCOL :710–711: cấu hình yêu cầu không phải runtime evidence; tiền lệ `ops/reviews/phan-bien-quy-trinh-review-2-claude-verdict.receipt.yaml` ghi *"không đường nào trong phiên trả model đang phục vụ"*). Mức assurance: **`review_deferred`** (PROTOCOL §8 mục 4, :568). Biên nhận **phải** tự khai `che_do: subagent_trong_phien_dieu_phoi` (tiền lệ `ops/reviews/phan-bien-quy-trinh-review-{1,2}-claude-verdict.receipt.yaml`); đã khai thì validator bác `same_provider_approved` và chỉ đích danh `review_deferred` (`ops/bien_nhan_v2.py` :703, :720–726). Lượt này **không** mang lời khai độc lập nào: nó chạy trong phiên điều phối, cùng họ Claude với executor, không có `session_run_id` hay `phien_doc_lap`. Vì vậy nó không là `cross_approved` (§8 mục 1, :562; validator bác khi hai bên cùng họ, :734–737) và không là `same_provider_approved` (§8 mục 3, :565–567 đòi phiên/context/checkout mới độc lập, không fork context executor). Validator không tự phát hiện subagent: biên nhận bỏ `che_do` mà thêm một `session_run_id` bất kỳ vẫn qua `same_provider_approved` (đo ở ghi chú dưới closure), nên khai `che_do` là nghĩa vụ khai trung thực, không phải chốt máy. Không dùng `advisory_review`: tên ấy không thuộc bốn mức của §8 (PROTOCOL §8.1 :715–716 xếp ChatGPT Web vào đúng mức ấy nhưng không giới hạn tên cho riêng nó; kho có biên nhận `anthropic_claude` ghi `advisory_review`, r9 theo bốn mức của §8). `review_deferred` không thay `cross_approved` cho class `sensitive`: với mức ấy, land đòi cross-review khác nền tảng hoặc human review có audit (:662–663), và Q12 chọn `human_audited` (ghi chú gate land ngay dưới closure). Số dòng: `docs/PROTOCOL_DA_PHIEN.md` :562 (mục 1), :565–567 (mục 3), :568 (mục 4), :662–663, :710–716 (§8.1) trên `20ec8d5` và `163fd5d`, tức :606, :609–611, :612, :706–707, :754–760 trên `ab457c6` (cùng nội dung từng dòng; bảng đổi tọa độ ở mục *Tọa độ trên nền mới*); PROTOCOL giống hệt giữa `423b4ba`, `20ec8d5` và `163fd5d`, còn `163fd5d..ab457c6` đổi `54 10` (wp709: danh tính provider); `ops/bien_nhan_v2.py` giống hệt giữa `423b4ba`, `20ec8d5`, `163fd5d` và `ab457c6` (`git diff --quiet` rc=0, sha256 `38cda51c…badefc`). Lịch sử: r1–r6 khai `codex` (`gpt-6-astra`, effort ≥ medium), sáu lượt review đặc tả chạy bằng codex; r7 khai subagent `review-opus-max`, mức `review_deferred`; r8 khai `claude -p` qua `launcher.py run`, mức `same_provider_approved` khi đủ bằng chứng (phương án B), bỏ ở r9 theo Q12 sau khi review lượt 8 đo ba khe của nó (`run.json` không lưu argv; `session_run_id` không chứng minh độc lập; probe trust của launcher chặn `CHAN [15]` ở sandbox chưa trust). |
| `depends_on` | **Theo Q8 (§3), viết lại ở r6; r7 đổi điều kiện (3); r8 thêm điều kiện (5) theo Q11; r9 tổng quát hoá điều kiện (4) theo review lượt 8; r10 đo (1), (4), (5) bằng **chuỗi lệnh đo điều kiện cấp** (mục ngay sau Công thức băm; review lượt 9) và đo lại; r11 viết lại chuỗi ấy theo tiêu chí DƯƠNG cho mọi bước (review lượt 10) và đo lại; r12 thêm bước (0) cấu hình vận chuyển và bước (iv) `s5.py` (review lượt 11), dời nền theo (4) và đo lại; r13 sửa `s5.py` (review lượt 12 và phép đo của phiên soạn r13: liệt kê tệp lease không qua nháy; chặn tên có ký tự ngắt dòng và mục cây không phải tệp thường; danh sách cho phép trên ký tự và hình dạng mục write set), giữ nền và đo lại; r14 không đổi chuỗi lệnh hay `s5.py`, chỉ đổi số revision ở (3) (review lượt 13); r15 cũng vậy (review lượt 14).** Chủ kho uỷ quyền cấp lease `wp678` (Q8). Thứ tự: đợi lease `lease-publish-windows-do-r1-g1-claude` của packet #687 (giữ `ops/lease_publish_test.py`) nhả (Q8; đo r9: lease #687 đang giữ tệp ấy là generation 3; đo r10: #687 đã land, bản lease g3 trên master rút hạn từ `a6de9d1`, xem dưới), và **#677 land trước** (Q11: *"#677 rồi #678"* là thứ tự LAND). Năm điều kiện cấp, cả năm phải thoả và **đo lại lúc cấp** bằng chuỗi lệnh ấy, không nhận số dưới đây thay phép đo: (1) bước (iv) ra `NGƯỜI_GIỮ 0`, rc=0, cho cả `ops/lease_publish.py` lẫn `ops/lease_publish_test.py`, theo cả phép khớp của `ai-dang-giu` lẫn phép khớp PROTOCOL §5 của `s5.py` (từ r12), trên kho vừa qua bước (0) và (iii) và sau đó qua bước (vii), mỗi bước đạt tiêu chí DƯƠNG của nó (bảng tiêu chí của mục *Chuỗi lệnh đo điều kiện cấp*); (2) không lượt review nào đang chạy; (3) lease neo `spec_hash` của revision **cuối cùng đã review sạch** (0 P1/P2/P3), review bằng lượt subagent `review-opus-max` (cấu hình Opus 5.5 `max`) mức `review_deferred` (Q12; dòng reviewer và ghi chú Q10 ở §3); từ r15, đó là **revision 15** khi lượt review của nó sạch và chưa có revision nào sau nó; (4) nếu #687 land trước và đổi `ops/lease_publish_test.py` thì dời nền nghiệm thu bằng một revision mới **trước** khi cấp, không cấp trên nền cũ (đã xảy ra hai lần: PR #701, r10 dời nền sang `163fd5d`; PR #712 của wp709, r12 dời nền sang `ab457c6`); **tổng quát hoá** (chặt hơn Q8, không nới): bước (v) `git diff --quiet "$NEN" refs/remotes/origin/master -- ops/lease_publish.py ops/lease_publish_test.py` phải rc=0 và `git ls-tree` hai tệp ấy trên `refs/remotes/origin/master` ra đúng 2 dòng (rc=0 của `diff --quiet` một mình là bằng chứng ÂM: đường dẫn vắng ở cả hai rev cũng cho rc=0, §10), chạy trên kho vừa qua bước (iii) (phép so tập tên một mình KHÔNG làm `origin/master` hết là ref đệm cũ: máy chủ land một commit đổi tệp write set thì tập tên không đổi; review lượt 9 đo, phiên soạn r10 tái lập, §10); rc=1, tức **bất kỳ** packet nào (#687 hay packet khác) đã land thay đổi một tệp write set sau nền, ⇒ cũng dời nền bằng revision mới trước khi cấp; rc khác hoặc không chạy được ⇒ không cấp; (5) **#677 đã land** (Q11): PR #689 `merged: true`, merge commit của nó là tổ tiên của `origin/master` lúc cấp (bước (vi) rc=0), và nền nghiệm thu chứa merge ấy; không đo được một trong ba vế ⇒ không cấp. Đây là kiểm loại trừ write set theo luật khớp PROTOCOL §5 bước 1, 3, 4 (`s5.py`: đường dẫn chính xác hay prefix thư mục, mục chuỗi hay ánh xạ `{type: exact|prefix, path}`, `write_set` lẫn `effective_write_set`; mục ngoài danh sách cho phép tính là phủ; tệp lease liệt kê không qua nháy, tên có ký tự ngắt dòng hay mục không phải tệp thường làm chuỗi `KHÔNG_XÁC_ĐỊNH`), trên miền ref, luật hạn và luật bia mộ của `ai-dang-giu` (giới hạn ở mục *Giới hạn* của chuỗi lệnh), cộng điều kiện cấp của Q8 và Q11, **không** phải cổng quét kiểu `lease_id`: cổng quét kiểu chỉ đặt trước land (A9, Q7). **Hiện tại (r15, 07-10):** phiên soạn r15 không chạy lại chuỗi (khối lệnh và `s5.py` không đổi byte); REST `master` 17:18:24Z = `ab457c6`, và `adg2` (chỉ đọc, `FETCH_HEAD` 17:17:01Z): `origin/master` = `ab457c6`, `git diff --quiet` hai tệp rc=0, `ls-tree` 2 dòng, tức điều kiện (4) rc=0 tại lúc đo; điều kiện (3): r15 chưa review, chưa thoả; vậy **không cấp**. **Lịch sử r14 (07-10):** phiên soạn r14 không chạy lại chuỗi (khối lệnh và `s5.py` không đổi byte); `adg2` sau `fetch --prune` 15:16:37Z–15:16:38Z: `origin/master` = `ab457c6`, `git diff --quiet` hai tệp rc=0, `ls-tree` 2 dòng, tức điều kiện (4) rc=0 tại lúc đo; điều kiện (3): r14 chưa review, chưa thoả; vậy **không cấp**. **Lịch sử r13 (07-10), phiên soạn r13 tự đo** trên `adg2` (clone sạch trong scratch của phiên điều phối; `fetch --prune` rồi `merge --ff-only` lúc 12:06:44Z–12:06:45Z: `origin/master` = `ab457c6`, `status --porcelain --ignored` 0 dòng), bằng đúng chuỗi lệnh r13 (khối lệnh và `s5.py` trích từ chính tệp này; `s5.py` chép vào `T`, OID khớp), chỉ thay giá trị `T` (`chay_that.py` của phiên soạn r12, chép nguyên byte, sha256 `455ad810…9847`; script ở scratch, không vào kho; `python` 3.11.15 tại `/usr/local/bin/python`, git 2.43.0; môi trường thật của container, gồm `GIT_CONFIG_*` của phiên). Lượt 13:12:13Z–13:13:11Z, 46 bước (36 dòng cộng 10 dòng lặp ở (vii)), chạy một lượt, mọi bước rc=0, không lệch: (0) `cong_cu` 6 dòng, `nong` `false`, endpoint `https://github.com/ducthangho/tra-luat` (1 dòng, `endpoint.khop` `1`), `cau_hinh` 4 dòng (`remote.origin.url`, `remote.origin.fetch` và hai dòng `url.https://github.com/.insteadof` của phạm vi command), `cau_hinh.dem` `4` = `cau_hinh.khop` `4`; (i) `fetch` rc=0, `merge --ff-only` rc=0; (ii)/(iii) và (vii) `may_chu.raw` 472 = `mc` 472 = `chung` 472, `thieu` 0, `master` 1 = `master.chung` 1 (OID `ab457c651eb4428705f0492163080b661c858b72`), `thua` 1 dòng (`refs/heads/HEAD`, vô hại); (iv) `cong_cu.oid` = `nen.oid` = `93cff2f97e01ebf41c18a4c5a1bd90343b343bbe`, `s5.oid` = `c730245ceea8cc5368d5ef84f8e296cd35102694`; `ai-dang-giu ops/lease_publish.py` ⇒ rc=0, dòng cuối `NGƯỜI_GIỮ 0: không có`, 0 dòng `CÒN_HẠN`; `ai-dang-giu ops/lease_publish_test.py` ⇒ rc=0, cùng dòng cuối, 0 dòng `CÒN_HẠN`; `s5.py` ⇒ rc=0, dòng cuối `S5 TỰ_KIỂM 38/38 đạt; NGƯỜI_GIỮ 0 ở 2/2 đường dẫn`, 0 dòng `KHÔNG_DIỄN_GIẢI`, 0 dòng `CÒN_HẠN`, và tập dòng lease mà `s5.py` liệt kê cho mỗi đường dẫn bằng đúng tập của `ai-dang-giu` (75 và 123 dòng); `adg.1.khop` = `adg.2.khop` = `s5.khop` = `1`; (v) `diff --quiet` rc=0, `v.ls` 2 dòng (blob `93cff2f…` và `7dd06ab…`); (vi) hai rc=0. Hai lease `wp709-exec-g1-codex-20261005` và `wp709-exec-g2-codex-20261006` (nhánh `codex/wp709-bootstrap`) nay ở nhãn `HẾT_HẠN` (g2 hết hạn `2026-10-07T10:30:00Z`). Kết luận theo chuỗi: **(1), (4), (5) đạt tại lúc đo**, bằng bằng chứng dương ở mọi bước. Đây là dữ kiện lúc soạn, không phải lời khai lúc cấp: (1) chỉ kết luận được bằng chuỗi chạy lúc cấp. Điều kiện (2): phiên soạn r13 KHÔNG ĐO ĐƯỢC. Điều kiện (3): r13 chưa review, chưa thoả; vậy **không cấp**. Điều kiện (4): rc=0 với nền `ab457c6` (13:13Z). Điều kiện (5): vế REST giữ từ r9 (PR #689 `merged: true`), hai vế tổ tiên rc=0 ở (vi). (b) Kho `/home/user/tra-luat`: r13 không đo (không `fetch` vào kho chính). **Lịch sử r12 (07-10), phiên soạn r12 tự đo** trên `adg2` (clone sạch trong scratch của phiên điều phối; `fetch --prune` rồi `merge --ff-only` lúc 08:2xZ: `origin/master` = `ab457c6`, `status --porcelain --ignored` 0 dòng), bằng đúng chuỗi lệnh r12 (`s5.py` chép vào `T`, OID khớp), chỉ thay giá trị `T` (script ở scratch, không vào kho; `python` 3.11.15, git 2.43.0; môi trường thật của container, gồm `GIT_CONFIG_*` của phiên). Lượt 09:07:36Z–09:08:28Z, 46 bước (36 dòng cộng 10 dòng lặp ở (vii)), chạy một lượt, không lệch: (0) `cong_cu` 6 dòng, `nong` `false`, endpoint `https://github.com/ducthangho/tra-luat` (1 dòng, `endpoint.khop` `1`), `cau_hinh` 4 dòng (`remote.origin.url`, `remote.origin.fetch` và hai dòng `url.https://github.com/.insteadof` từ phạm vi command, tức `GIT_CONFIG_*` của phiên), `cau_hinh.dem` `4` = `cau_hinh.khop` `4`; (i) `fetch` rc=0, `merge --ff-only` rc=0; (ii)/(iii) và (vii) `may_chu.raw` 470 = `mc` 470 = `chung` 470, `thieu` 0, `master` 1 = `master.chung` 1 (OID `ab457c651eb4428705f0492163080b661c858b72`); (iv) `cong_cu.oid` = `nen.oid` = `93cff2f97e01ebf41c18a4c5a1bd90343b343bbe`, `s5.oid` = `2f6bde6c90098dd0781252984c5ede31efb62e01`; `ai-dang-giu ops/lease_publish.py` ⇒ **rc=11**, `NGƯỜI_GIỮ 1: wp709-exec-g2-codex-20261006`; `ai-dang-giu ops/lease_publish_test.py` ⇒ **rc=11**, cùng người giữ; `s5.py` ⇒ **rc=11**, hai đường dẫn cùng một dòng `CÒN_HẠN` (`refs/remotes/origin/codex/wp709-bootstrap:ops/leases/wp709-exec-g2-codex-20261006.yaml`), 0 dòng `KHÔNG_DIỄN_GIẢI`, và tập dòng lease mà `s5.py` liệt kê cho mỗi đường dẫn bằng đúng tập của `ai-dang-giu` (75 và 123 dòng; tức trên 470 nhánh hiện tại phép khớp §5 không thấy thêm lease nào); (v) `diff --quiet` rc=0, `v.ls` 2 dòng; (vi) hai rc=0. Kết luận theo chuỗi: **không cấp** ở (iv) (bước đầu tiên không đạt). Tệp lease ấy (đọc bằng `git show` rồi `yaml.safe_load`): `packet_issue: 709`, `role: executor`, `provider: codex`, `generation: 2`, `write_set` 6 mục gồm cả hai tệp (cùng 6 mục ở `effective_write_set`), `leased_at_utc: '2026-10-06T11:58:00Z'`, `lease_expires_at_utc: '2026-10-07T10:30:00Z'`; đầu nhánh `94908a0` (2026-10-06T11:57:45Z), không là tổ tiên của `origin/master` dù PR #712 đã merge. Vậy **điều kiện (1) CHƯA thoả** tới `2026-10-07T10:30:00Z` (trừ khi lease ấy được thu hồi sớm bằng bia mộ hai chiều). Đây là dữ kiện lúc soạn, không phải lời khai lúc cấp. Lượt đo đầu 08:39:09Z–08:40:36Z với một bản `s5.py` trước (24 ca tự kiểm, OID khác) ra cùng kết luận và cùng người giữ. Điều kiện (2): phiên soạn r12 KHÔNG ĐO ĐƯỢC. Điều kiện (3): r12 chưa review, chưa thoả. Điều kiện (4): rc=0 với nền `ab457c6` (09:08Z); với nền cũ `163fd5d` là rc=1 (`git diff --quiet 163fd5d… refs/remotes/origin/master -- <hai tệp>`, 09:27:22Z; `--numstat` ở đầu tệp), là phép đo khiến r12 dời nền. Điều kiện (5): vế REST giữ từ r9 (PR #689 `merged: true`), hai vế tổ tiên rc=0 ở (vi). (b) Kho `/home/user/tra-luat`: r12 không đo (không `fetch` vào kho chính). **Lịch sử r11 (01-10), phiên soạn r11 tự đo** trên `adg2` (clone sạch trong scratch của phiên điều phối; `fetch --prune` rồi `merge --ff-only` lúc 11:04:55Z–11:04:56Z: `origin/master` = `7e5958e`, `status --porcelain --ignored` 0 dòng), bằng đúng chuỗi lệnh r11, chỉ thay giá trị `T` (script ở scratch, không vào kho; Python 3.11.15, git 2.43.0). Lượt 11:22:06Z–11:22:53Z, 40 bước (30 dòng cộng 10 dòng lặp ở (vii)), chạy một lượt, không lệch: (0) `cong_cu` 6 dòng, `nong` `false`, endpoint `https://github.com/ducthangho/tra-luat` (1 dòng, `endpoint.khop` `1`); (i) `fetch` rc=0, `merge --ff-only` rc=0; (ii)/(iii) và (vii) `may_chu.raw` 456 = `mc` 456 = `chung` 456, `thieu` 0, `master` 1 = `master.chung` 1 (OID `7e5958e440285c8d63d2f710cf97ba20b85f2926`); (iv) `cong_cu.oid` = `nen.oid` = `1b4de52895334405afeb530479139d6bb4d4ce96`; `ai-dang-giu ops/lease_publish.py` ⇒ rc=0, `NGƯỜI_GIỮ 0: không có`; `ai-dang-giu ops/lease_publish_test.py` ⇒ **rc=11**, dòng cuối `NGƯỜI_GIỮ 1: no-ton-677-687-r1-g1-claude`, đúng một dòng `CÒN_HẠN` (`refs/remotes/origin/claude/no-ton-677-687:ops/leases/no-ton-677-687-r1-g1-claude.yaml`), nên dòng `grep` kế tiếp rc=1; (v) `diff --quiet` rc=0, `v.ls` 2 dòng; (vi) hai rc=0. Kết luận theo chuỗi: **không cấp** ở (iv). Tệp lease ấy (đọc bằng `git show` rồi `yaml.safe_load`): `packet_issue: 704`, `packet_id: NO-TON-677-687`, `generation: 1`, `write_set` 8 mục gồm `ops/lease_publish_test.py`, `leased_at_utc: '2026-10-01T09:55:00Z'`, `lease_expires_at_utc: '2026-10-02T09:55:00Z'`, `start_from_sha` `a6de9d1`, `spec_hash` `905fdccb…52bd` bằng sha256 của `ops/specs/no-ton-677-687-r1.md` trên cùng nhánh; đầu nhánh `8418fb5` (09:54:30Z), chưa là tổ tiên của `origin/master`. Đặc tả #704 chỉ cho đổi thân `t194` hoặc một helper chỉ `t194` dùng (B3.3), trần +150/−20 dòng (B3.4). Vậy **điều kiện (1) CHƯA thoả** tới `2026-10-02T09:55:00Z`, và #704 land trước lúc cấp thì điều kiện (4) ra rc=1 ⇒ revision mới dời nền. Đây là dữ kiện lúc soạn, không phải lời khai lúc cấp; lease cấp 09:55:00Z, tức 10 phút sau lượt đo cuối của r10 (09:45Z). Điều kiện (2): phiên soạn r11 KHÔNG ĐO ĐƯỢC. Điều kiện (3): r11 chưa review, chưa thoả. Điều kiện (4): rc=0 với nền `163fd5d` (11:22Z). Điều kiện (5): vế REST giữ từ r9 (PR #689 `merged: true`), hai vế tổ tiên rc=0 ở (vi). (b) Kho `/home/user/tra-luat`: r11 không đo (không `fetch` vào kho chính). **Lịch sử r10 (01-10), phiên soạn r10 tự đo** trên `adg2` (clone sạch trong scratch của phiên điều phối: không nông, refspec `+refs/heads/*:refs/remotes/origin/*`, `refs/heads` 1 ref, `refs/replace` 0 ref, `status --porcelain --ignored` 0 dòng), bằng đúng chuỗi lệnh ấy với `<nền nghiệm thu>` = `163fd5d`, `<merge commit PR #689>` = `20ec8d5` (script ở scratch, không vào kho; Python 3.11.15, git 2.43.0). Lượt 09:45:15Z–09:45:40Z: (i) `fetch` rc=0, `merge --ff-only` rc=0, `origin/master` = `a6de9d12d0ddd13bb35c4decea54bf626806162c` (merge PR #702 bookkeeping #687, sau merge PR #699 bookkeeping #677; 118 tệp so `163fd5d`: 81 dưới `ops/land/`, 7 dưới `ops/leases/`, 29 dưới `ops/reviews/`, 1 dưới `ops/specs/`; 0 ở `.github/`, 0 tệp nằm ngay dưới `ops/`); (ii) `ls-remote` rc=0, 462 tên; (iii) cục bộ 462 tên, lệch theo tên 0 dòng cả hai chiều, lệch theo cặp tên + OID 0 dòng cả hai chiều; (iv) `ops/lease_publish.py` ⇒ `NGƯỜI_GIỮ 0: không có`, rc=0; `ops/lease_publish_test.py` ⇒ `NGƯỜI_GIỮ 0: không có`, rc=0, 0 dòng `CÒN_HẠN`; (v) `git diff --quiet 163fd5d origin/master -- ops/lease_publish.py ops/lease_publish_test.py` rc=0; (vi) `git merge-base --is-ancestor 20ec8d5 origin/master` rc=0; (vii) lệch cặp 0 dòng. Lease g3 của #687 trên `origin/master` (`a6de9d1`) nay là blob `976915a`, khai `lease_expires_at_utc: '2026-10-01T05:55:00Z'` (rút hạn), và `ai-dang-giu` xếp nó `HẾT_HẠN`. Lượt trước, 09:18:18Z–09:18:38Z, khi `origin/master` còn là `163fd5d`: (iv) `ops/lease_publish_test.py` ⇒ `NGƯỜI_GIỮ 1: lease-publish-windows-do-r3-g3-claude`, **rc=11**, dòng `CÒN_HẠN` duy nhất là bản trên `refs/heads/master` (blob `372cbfd`, `lease_expires_at_utc: '2026-10-02T01:12:00Z'`, `da_bi_thay_the` vắng), còn bản rút hạn khi ấy chỉ nằm trên `refs/remotes/origin/claude/cap-lease-687-g3` (đầu `5955819`, 05:42:57Z, tiêu đề *"lease(#687 g3): thu hồi bằng rút hạn về 05:55Z — packet đã merge (PR #701, 163fd5d)"*) và `refs/remotes/origin/claude/bookkeeping-687-pr701`; (v) với nền cũ `20ec8d5` ra **rc=1**, là phép đo khiến r10 dời nền. Hai lượt cách nhau 27 phút cho hai kết quả người giữ khác nhau vì master đổi giữa chừng (bài học *"SỔ LEASE KHÔNG NẰM MỘT CHỖ"* của CLAUDE.md). Đây là **dữ kiện lúc soạn, KHÔNG phải lời khai điều kiện (1) thoả**: (1) chỉ kết luận được bằng chuỗi lệnh chạy lúc cấp. Điều kiện (2): phiên soạn r10 KHÔNG ĐO ĐƯỢC. Điều kiện (3): r10 chưa review, chưa thoả. Điều kiện (4): rc=0 với nền `163fd5d` lúc 09:45:39Z. Điều kiện (5): vế REST giữ từ r9 (PR #689 `merged: true`, merge commit `20ec8d5`), vế tổ tiên đo lại rc=0, vế "nền chứa merge" đo bằng `git merge-base --is-ancestor 20ec8d5 163fd5d` rc=0. PR #701: REST `GET /repos/ducthangho/tra-luat/pulls/701` (HTTP 200 09:27:03Z, không token) ⇒ `merged: true`, `merged_at` `2026-10-01T05:42:28Z`, `merge_commit_sha` `163fd5d448d8d3e65766ee238f33be0f47ae72c4`, base `20ec8d5`, head `claude/lease-publish-windows-do`. (b) Kho `/home/user/tra-luat`: r10 không đo (không `fetch` vào kho chính). **Lịch sử r9 (01-10), phiên soạn r9 tự đo.** (a) Clone sạch có sẵn trong scratch của phiên điều phối (`adg2`: không nông, refspec `+refs/heads/*:refs/remotes/origin/*`, `refs/heads` 1 ref, `refs/replace` 0 ref, cây sạch), `git fetch -q --prune` cùng refspec rc=0 (05:17:32Z–05:17:33Z), `git merge --ff-only origin/master` rc=0: `origin/master` = `20ec8d5`. `ls-remote --heads` 461 tên, `for-each-ref refs/remotes/origin` 461 tên (bỏ `HEAD`), lệch theo tên 0 dòng cả hai chiều, lệch theo cặp tên + OID 0 dòng (05:17:40Z–05:17:41Z). `ai-dang-giu ops/lease_publish.py` (05:17:46Z–05:17:57Z) ⇒ dòng cuối `NGƯỜI_GIỮ 0: không có`, rc=0, 0 dòng `CÒN_HẠN`. `ai-dang-giu ops/lease_publish_test.py` (05:17:57Z–05:18:07Z) ⇒ dòng cuối `NGƯỜI_GIỮ 1: lease-publish-windows-do-r3-g3-claude`, **rc=11**, đúng một dòng `CÒN_HẠN` (`refs/remotes/origin/claude/cap-lease-687-g3:ops/leases/lease-publish-windows-do-r3-g3-claude.yaml`). Tệp lease ấy (đọc bằng `git show` rồi `yaml.safe_load`): `packet_issue: 687`, `generation: 3`, `write_set` chỉ `ops/lease_publish_test.py`, `leased_at_utc: '2026-10-01T01:12:00Z'`, `lease_expires_at_utc: '2026-10-02T01:12:00Z'`, `start_from_sha` `89fc4fa`; đầu ref là commit `eca94d1` (01:11:15Z, tiêu đề *"lease(#687): r3 g3 — mở lại sau khi #677 land; …"*). Vậy **điều kiện (1) CHƯA thoả**: #687 giữ `ops/lease_publish_test.py` tới `2026-10-02T01:12:00Z`. Điều kiện (2): phiên soạn r9 KHÔNG ĐO ĐƯỢC. Điều kiện (3): r9 chưa được review, chưa thoả. Điều kiện (4): `git diff --quiet 20ec8d5 origin/master -- ops/lease_publish.py ops/lease_publish_test.py` rc=0 (05:18:23Z), thoả tại lúc đo; vì #687 đang giữ `ops/lease_publish_test.py`, nếu nó land và đổi tệp ấy thì phép đo này ra rc=1 và phải có revision mới dời nền trước khi cấp. Điều kiện (5): REST `GET /repos/ducthangho/tra-luat/pulls/689` (HTTP 200, 05:22Z, không token) ⇒ `merged: true`, `merged_at` `2026-10-01T00:55:22Z`, `merge_commit_sha` `20ec8d5d0e86cb7dc01f202c7596407a957e5961`; `20ec8d5` là `origin/master` và là nền nghiệm thu, nên thoả tại lúc đo. (b) Kho `/home/user/tra-luat`: r9 không đo (không `fetch` vào kho chính). **Lịch sử r8 (01-10), phiên soạn r8 tự đo.** (a) Clone mới từ `origin` ở scratch (clone 01:10:39Z–01:10:47Z, không nông, refspec `+refs/heads/*:refs/remotes/origin/*`, `refs/heads` chỉ có `master`, rồi `fetch` cùng refspec rc=0): `ls-remote --heads` 459 tên, `for-each-ref refs/remotes/origin` 459 tên (bỏ `HEAD`), lệch theo cặp tên + OID 0 dòng cả hai chiều, lệch theo tên 0 dòng (01:10:48Z); `origin/master` = `20ec8d5`. `ai-dang-giu ops/lease_publish.py` (01:10:52Z–01:11:03Z) và `ai-dang-giu ops/lease_publish_test.py` (01:11:04Z–01:11:15Z) đều ra dòng cuối `NGƯỜI_GIỮ 0: không có`, rc=0, 0 dòng `CÒN_HẠN`. Sáu lease #677 `dot-bien-l-bien-cong-khai-exec-1`…`exec-6` đều `HẾT_HẠN`; lease g6 (`dot-bien-l-bien-cong-khai-exec-6-claude-20260930`, `refs/remotes/origin/claude/cap-lease-677-g6`) nay khai `lease_expires_at_utc: '2026-10-01T01:10:00Z'`, gốc `03:27Z`, rút hạn ở commit `35e23d7` (01:01:20Z, *"thu hồi bằng rút hạn về 01:10Z — packet đã merge (PR #689, 20ec8d5)"*). g6 chỉ giữ `ops/lease_publish_test.py`, và phép đo người giữ tệp ấy bắt đầu **64 giây** sau mốc 01:10:00Z; trước mốc ấy g6 còn hạn. Hai lease #687 vẫn `HẾT_HẠN`. (b) Kho `/home/user/tra-luat`: r8 **không** đo lại (không `fetch` vào kho chính); lời giải thích `CHAN [12]` của r7 dưới đây giữ làm lịch sử. Điều kiện (2): phiên soạn r8 KHÔNG ĐO ĐƯỢC. Điều kiện (3): r8 chưa được review, chưa thoả. Điều kiện (4): #687 chưa land (không merge nào của #687 trong `git log --first-parent 89fc4fa..20ec8d5`, 10 merge), nên không phải dời nền vì #687. Điều kiện (5): REST `GET /repos/ducthangho/tra-luat/pulls/689` (HTTP 200, 01:06:46Z) ⇒ `merged: true`, `merged_at` `2026-10-01T00:55:22Z`, `merge_commit_sha` `20ec8d5d0e86cb7dc01f202c7596407a957e5961`, `merged_by` `ducthangho`, base `fc852ff`; `20ec8d5` chính là `origin/master` và là nền nghiệm thu của r8, nên thoả tại lúc đo. Tương tác với #677: §10 và A2. **Lịch sử r7 (30-09).** *Lời khai của phiên điều phối, đo 12:2xZ, không phải phép đo của phiên soạn r7:* hai tệp `NGƯỜI_GIỮ 0` qua `ai-dang-giu`, sau khi so tên + OID của `ls-remote --heads` với `for-each-ref`, 0 lệch; không lượt review `wp678` nào đang chạy; r6 approve sạch; nền `89fc4fa`→`423b4ba` không đổi hai tệp. *Phiên soạn r7 tự đo:* (a) trong một clone mới từ `origin` ở scratch (clone 12:27:46Z–12:27:52Z, không nông, `refs/heads` chỉ có `master`): `ls-remote --heads` 458 tên, `for-each-ref refs/remotes/origin` 458 tên (bỏ `HEAD`), lệch theo cặp tên + OID 0 dòng cả hai chiều (12:27:58Z); `ai-dang-giu ops/lease_publish.py` và `ai-dang-giu ops/lease_publish_test.py` đều ra dòng cuối `NGƯỜI_GIỮ 0: không có`, rc=0, 0 dòng `CÒN_HẠN` (12:28:03Z–12:28:25Z); hai lease #687 (`lease-publish-windows-do-r1-g1-claude`, `lease-publish-windows-do-r2-g2-claude`) ở nhãn `HẾT_HẠN`, tệp lease trên `refs/remotes/origin/claude/lease-publish-windows-do` nay khai `lease_expires_at_utc` lần lượt `'2026-09-29T11:50:00Z'` và `'2026-09-29T11:45:00Z'` (commit `6112b89` rút hạn). (b) Cùng hai lệnh trong kho `/home/user/tra-luat` và worktree dùng chung ref của nó ra **`CHAN [12]` `KHÔNG_XÁC_ĐỊNH`, rc=12** (12:27:18Z), vì nhánh cục bộ `ops/spec-lease-id-ep-kieu-yaml` (`03a7219`, là tổ tiên của `origin/master`) có upstream `[gone]`; phép so tên + OID ở kho ấy cũng 458/458, 0 lệch (12:27:11Z). Tức kết quả phụ thuộc kho đo: lúc cấp phải đo ở kho không vướng `CHẶN [12]`, và không đọc rc=12 thành `NGƯỜI_GIỮ 0`. Điều kiện (2): phiên soạn r7 KHÔNG ĐO ĐƯỢC. Điều kiện (4): #687 chưa land (không merge nào của #687 trong `git log --first-parent 89fc4fa..423b4ba`, 7 merge) và hai tệp không đổi (hàng nền nghiệm thu), nên không phải dời nền. Ngoài bốn điều kiện, xem §10 về nhánh thi hành của #677. Lịch sử r6 (10:48Z–10:49Z 29-09): `ops/lease_publish.py` `NGƯỜI_GIỮ 0`, rc=0; `ops/lease_publish_test.py` `NGƯỜI_GIỮ 1: lease-publish-windows-do-r1-g1-claude`, rc=11, lease ấy khi đó `CÒN_HẠN` và khai `lease_expires_at_utc: '2026-09-30T10:20:00Z'`, nên điều kiện (1) chưa thoả; so tên ref: máy chủ 511, cục bộ 512, thiếu cục bộ 0, thừa cục bộ 1 (`claude/bookkeeping-574-land`, ref đệm cũ, vô hại). Lịch sử cũ hơn: đo 10:14Z (r5) và 09:44Z (r4) cả hai tệp `NGƯỜI_GIỮ 0` (lease của #687 chưa có, `leased_at` 10:20Z); đo 07:59Z 29-09 `ai-dang-giu ops/lease_publish_test.py` ⇒ `NGƯỜI_GIỮ 1: t131-deadline-dem-spawn-exec-1-claude-20260929`, đã `HẾT_HẠN` (`lease_expires_at_utc: '2026-09-29T08:15:00Z'`) và T131 **đã land** (PR #680, `89fc4fa`). |
| nền nghiệm thu | **r15 giữ nền này**: REST `master` lúc 17:18:24Z 07-10 = `ab457c6`; `adg2` (chỉ đọc, `FETCH_HEAD` 17:17:01Z 07-10) `origin/master` = `ab457c6`, `git diff --quiet` hai tệp rc=0 và `ls-tree` hai tệp 2 dòng. **r14 giữ nền này**: `adg2` sau `fetch --prune` 15:16:37Z–15:16:38Z 07-10 `origin/master` = `ab457c6`, `git diff --quiet` hai tệp rc=0 và `ls-tree` hai tệp 2 dòng. **r13 giữ nền này**: `adg2` sau `fetch --prune` 12:06:44Z–12:06:45Z 07-10 và ở lượt chạy thật của chuỗi r13 (13:12:13Z–13:13:11Z, hàng `depends_on`) `origin/master` = `ab457c6`, `git diff --quiet` hai tệp rc=0 và `v.ls` 2 dòng; r13 không đo lại các số hạng phụ thuộc nền dưới đây (hai tệp write set giống hệt nền). `origin/master` lúc dời nền: `ab457c651eb4428705f0492163080b661c858b72` (merge PR #712, tức wp709 land; dời ở r12 theo điều kiện cấp (4)); wp709 là 18 commit không phải merge trong `8c98afa..ab457c6`, 17 trong số đó chạm hai tệp write set. Đo r12 (`adg2` sau `fetch --prune`, 08:2xZ–09:08Z 07-10): `origin/master` = `ab457c6`; `git merge-base --is-ancestor 163fd5d ab457c6` rc=0 và `git merge-base --is-ancestor 20ec8d5 ab457c6` rc=0; `git log --first-parent 163fd5d..ab457c6` 5 merge, 211 tệp đổi (122 dưới `ops/land/`, 65 dưới `ops/reviews/`, 11 dưới `ops/leases/`, 3 dưới `ops/specs/`, 3 dưới `.claude/dev/`, cộng hai tệp write set, `docs/PROTOCOL_DA_PHIEN.md`, `.github/workflows/ci.yml` và vài tệp khác); `git diff --numstat 163fd5d ab457c6` ⇒ `ops/lease_publish.py` `161 1`, `ops/lease_publish_test.py` `372 12`, `docs/PROTOCOL_DA_PHIEN.md` `54 10`, `.github/workflows/ci.yml` `90 4` (ci.yml đổi ở #703, `7e5958e`, giống hệt từ đó tới `ab457c6`); blob hai tệp trên `ab457c6`: `93cff2f97e01ebf41c18a4c5a1bd90343b343bbe` (sha256 `dbf3b905…8f67`, 2366 dòng) và `7dd06ab6e71a1fae73a29fca31df4a9b271aa081` (sha256 `273ebd3f…8008`, 11866 dòng). So `ast` các định nghĩa cấp module (07-10): `ops/lease_publish.py` thêm 6 (`PROVIDER_FAMILIES`, `MODEL_FAMILIES`, `RUNTIME_CAPABILITIES`, `_kiem_capability_khai`, `_kiem_executor_khai_voi_human_reviewer`, `_kiem_provider_identity`), xoá 0, đổi 2 (`PROVIDERS` nay dẫn xuất từ `PROVIDER_FAMILIES`; `kiem()` thêm đúng một lời gọi `_kiem_provider_identity(lease)` ở :984, ngay sau phép kiểm trường bắt buộc, TRƯỚC D1, xem §2 và A1); mọi hàm khác giống hệt thân, chỉ dời dòng: dòng L của `163fd5d` thành L + 159 khi 90 ≤ L ≤ 824 và L + 160 khi L ≥ 825 (đo bằng `grep -n` trên hai blob, §2). `ops/lease_publish_test.py` thêm 3 (`t01_legacy_provider_aliases`, `t01_executor_assurance_target_is_not_review_verdict`, `t01_ag_identity_and_family_gate`), xoá 0, đổi thân 4 (`t40` bản Windows của fixture actionlint, `t153` và `t155` đổi `--chi-ca=t01_` thành tên đầy đủ vì tiền tố `t01_` nay chọn bốn ca, `t190` thêm hàng `provider` khai rỗng); `t70`, `t178`, `t193`, `t199`, `t203`, `t125`, `_ca_doc_than_buoc`, `_ca_ung_vien_gian_tiep`, `_chay_buoc_dang`, `_chay_buoc_dang_that`, `_buoc_workflow`, `_ly_do_bo_qua_workflow`, `main`, `_chay_main_meta`, `SO_BO_QUA`, `lease_mau`, `_yaml_that` giống hệt thân, chỉ dời dòng (tọa độ mới ở §4). `ops/bien_nhan_v2.py`, `ops/bien_nhan_v2_test.py`, `.github/workflows/ops-publish-lease.yml` và `ops/chay_lease_publish_test.sh` giống hệt giữa `163fd5d` và `ab457c6` (`git diff --quiet` rc=0). Tương tác của các phần wp709 thêm với nghĩa vụ của packet này: §4, A1, A8, ghi chú dưới closure, §10. Đây là **nền bất biến** để đo diff và nghiệm thu. Packet CHƯA thi hành, chưa có diff hay lịch sử finding trên mã, nên việc dời nền ở r12 là quyết định bền (chính r12) theo protocol §3.2.1 và theo điều kiện (4), không phải dùng HEAD mới để xoá diff. **Lịch sử nền r10–r11** (nguyên văn r11): `origin/master` lúc dời nền ở r10: `163fd5d448d8d3e65766ee238f33be0f47ae72c4` (merge PR #701, tức #687 land; dời ở r10 theo điều kiện cấp (4)). **r11 giữ nền này** (`adg2` sau `fetch --prune`, 11:04:56Z 01-10): `origin/master` = `7e5958e440285c8d63d2f710cf97ba20b85f2926` (merge PR #703); `git diff --quiet 163fd5d448d8d3e65766ee238f33be0f47ae72c4 refs/remotes/origin/master -- ops/lease_publish.py ops/lease_publish_test.py` rc=0; `git ls-tree` hai tệp ở hai rev ra cùng hai dòng (blob `1b4de52895334405afeb530479139d6bb4d4ce96` và `2eba10abb3eeb39a5531d12689afba536004e4a4`); `git merge-base --is-ancestor 163fd5d… refs/remotes/origin/master` rc=0. #703 đổi `.github/workflows/ci.yml`: ba dòng mà đặc tả trích trên `163fd5d` (:574, :590, :630) nằm ở :628, :670, :711 trên `7e5958e`; review lượt 10 đo tên job giữ nguyên và suite 198/198 dưới 3.12.3 trên `7e5958e`. Đây là **nền bất biến** để đo diff và nghiệm thu. Packet CHƯA thi hành, chưa có diff hay lịch sử finding trên mã, nên việc dời nền ở r10 là quyết định bền (chính r10) theo protocol §3.2.1 và theo điều kiện (4), không phải dùng HEAD mới để xoá diff. Đo r10 (`adg2`, 09:2xZ–09:45Z 01-10): `git merge-base --is-ancestor 20ec8d5 163fd5d` rc=0; `git diff --quiet 20ec8d5 163fd5d -- ops/lease_publish.py` rc=0 (blob sha256 `dd17b94c…4f83` ở cả hai nền), nên các phép đo §1/§2 làm trên `1741e0a` vẫn hợp lệ; `git diff --numstat 20ec8d5 163fd5d -- ops/lease_publish_test.py` ⇒ `482 63`. So `ast` các định nghĩa cấp module của hai bản `ops/lease_publish_test.py`: thêm 11 (3 hằng `SO_BO_QUA` :569–575, `NHAN_UBUNTU_CHO_PHEP` :577, `RE_TONG_KET` :4615; 5 hàm phụ `_nhan_runs_on`, `_ca_ung_vien_gian_tiep`, `_ca_gia`, `_xac_minh_transcript_ab`, `_dung_transcript_ab`; 3 ca `@ca` `t193`, `t194`, `t203`), xoá 0, đổi thân 10 (`_ly_do_bo_qua_workflow`, `_chay_main_meta`, `main`, `t71`, `t72`, `t73`, `t98`, `t125`, `t158`, `t160`); `t70`, `t178`, `_ca_doc_than_buoc`, `_chay_buoc_dang`, `_chay_buoc_dang_that`, `_buoc_workflow` giống hệt thân, chỉ dời dòng. `.github/workflows/ops-publish-lease.yml`, `.github/workflows/ci.yml`, `ops/chay_lease_publish_test.sh`, `ops/bien_nhan_v2.py`, `ops/bien_nhan_v2_test.py` và `docs/PROTOCOL_DA_PHIEN.md` giống hệt giữa hai nền (`git diff --quiet` rc=0). Tương tác của các phần #687 thêm với nghĩa vụ của packet này: §4, A3, A8, §10. `origin/master` lúc đo cuối (`a6de9d1`, 09:45:15Z) không đổi tệp write set nào so `163fd5d` (điều kiện (4) rc=0). **Lịch sử nền:** r8 dời sang `20ec8d5d0e86cb7dc01f202c7596407a957e5961` (merge PR #689, tức #677 land; Q11) theo cùng lý lẽ §3.2.1; r9 giữ nền ấy: `origin/master` vẫn là `20ec8d5` lúc 05:17:33Z 01-10 (clone `adg2` sau `fetch --prune`), và `git diff --quiet 20ec8d5 origin/master -- ops/lease_publish.py ops/lease_publish_test.py` rc=0 (05:18:23Z). Đo 01-10 trên clone mới (r8): `origin/master` = `20ec8d5` (01:03:48Z và 01:10:47Z); `git merge-base --is-ancestor 89fc4fa 20ec8d5` rc=0; `git diff --quiet 89fc4fa 20ec8d5 -- ops/lease_publish.py` rc=0 (blob sha256 `dd17b94c…4f83` ở cả hai nền), nên các phép đo §1/§2 làm trên `1741e0a` vẫn hợp lệ; `git diff --numstat 89fc4fa 20ec8d5 -- ops/lease_publish_test.py` ⇒ `600 15`, bằng đúng `fc852ff..20ec8d5` (base của PR #689) và `423b4ba..20ec8d5`. Toàn bộ chênh do 9 commit `test(#677)` từ `11f73ac` tới `adad5f5`: thêm 18 hàm (8 ca `t195`–`t202` và 10 hàm phụ, trong đó `_chay_buoc_dang_that`), đổi thân đúng hai ca có sẵn (`t70`, `t154`); `t178`, `t131`, `t139`, `t192`, `_chay_buoc_dang`, `_buoc_workflow` giống hệt thân (so bằng `ast`), chỉ dời dòng. `.github/workflows/ops-publish-lease.yml` giống hệt (`git diff --quiet` rc=0). **Lịch sử nền cũ hơn:** r1 và r2 dùng `1741e0a1ab7ebce4b26912aefadca56ddfcdc691`; r3 dời sang `89fc4fac8cea65979cc2483043dc8cd07a6e8518` (PR #680, T131 land) theo cùng lý lẽ §3.2.1; r4, r5 và r6 **giữ nguyên** nền của r3: `git fetch` rồi `git rev-parse origin/master` đo 09:44Z 29-09 (r4), 10:14Z 29-09 (r5) và 10:48Z 29-09 (r6) vẫn ra `89fc4fac8cea65979cc2483043dc8cd07a6e8518`. r7 cũng giữ nền này, nhưng vì lý do khác: `origin/master` đã sang `423b4ba14078701859b9e6ac101a68a3fc4ddef4` (`git ls-remote origin refs/heads/master`, 12:26:45Z 30-09), còn `git diff --stat 89fc4fa 423b4ba -- ops/lease_publish.py ops/lease_publish_test.py` ra output **rỗng**, rc=0; cùng lúc `git diff --quiet` cùng phạm vi rc=0 và `git merge-base --is-ancestor 89fc4fa 423b4ba` rc=0. Giữa `1741e0a` và `89fc4fa`, `ops/lease_publish.py` giống hệt (`git diff --quiet` rc=0) và `ops/lease_publish_test.py` đổi +13/−19 (bốn hunk: hai trong t131, một trong t139, một trong t192). Nếu bất kỳ packet nào (#687 hay packet khác) land trước khi cấp và đổi một tệp write set, nền phải dời bằng revision mới trước khi cấp (điều kiện 4, kể cả phần tổng quát hoá). Nền tiếp nối (continuation base), nếu khác nền mà không đổi tệp write set nào, phải được khai riêng lúc cấp lease, không thay nền này. (Hết phần nguyên văn r11; hai câu cuối áp nguyên cho nền `ab457c6`.) |
| `spec_hash` | Xem **Công thức băm** ngay dưới. Giá trị **không** nằm trong tệp này. |

**Công thức băm.** `spec_hash` = SHA-256 trên **toàn bộ bytes** của tệp này tại commit đã đóng
băng: `sha256sum ops/specs/lease-id-ep-kieu-yaml-r15.md`, không loại dòng nào. Giá trị được công
bố **ngoài** tệp: comment trên #678 và lease, kèm OID commit + đường dẫn. Hai tên `spec_hash`
và `spec_sha256` nếu cùng xuất hiện thì mang **cùng** một giá trị. Đổi bất kỳ byte nào ⇒
revision mới, băm mới, lease mới. Vì khối closure dưới đây nằm **trong** tệp, cùng một `spec_hash`
không thể đi với hai closure khác nhau (đóng phản chứng "hai lease khác `required_checks` cùng
một băm" của lượt 2).

**Chuỗi lệnh đo điều kiện cấp (1), (4), (5)** (từ r10; viết lại ở r11 theo review lượt 10; r12 thêm bước (0) cấu hình
vận chuyển và bước (iv) `s5.py` theo review lượt 11; r13 đổi `s5.py`, tức hai dòng OID và `grep` ở (iv), theo review lượt 12; r14 và r15 không đổi khối hay `s5.py`; chặt hơn Q8, không nới).
Chạy liền nhau bằng bash, từ gốc MỘT clone có refspec `+refs/heads/*:refs/remotes/origin/*`; tệp tạm nằm trong `$T`,
NGOÀI cây làm việc, và `$T/s5.py` là khối mã *`s5.py`* ngay dưới chuỗi, chép từng byte (dòng `git hash-object` ở (iv)
đo việc chép). Handoff ghi từng dòng, UTC, rc, và nội dung mọi tệp trong `$T` (riêng `adg.1`, `adg.2`, `s5.out` ghi
dòng cuối, mọi dòng `CÒN_HẠN` và mọi dòng `KHÔNG_DIỄN_GIẢI`; `cau_hinh` ghi với phần xác thực đã che). `NEN` là nền
nghiệm thu, `M689` là merge commit của PR #689. Bộ thử của phiên soạn r13 chạy đúng khối dưới đây, từng dòng, với
`s5.py` trích từ khối mã của chính tệp này (§10).

```
T=/thu/muc/tam/ngoai/cay                                                   # (0)   đường dẫn tuyệt đối, NGOÀI cây làm việc, đã tạo sẵn, chứa `s5.py`
export LC_ALL=C GIT_NO_REPLACE_OBJECTS=1                                   # (0)   cố định cho mọi bước sau
NEN=ab457c651eb4428705f0492163080b661c858b72                               # (0)   OID đủ 40 hex, không viết tắt
M689=20ec8d5d0e86cb7dc01f202c7596407a957e5961                              # (0)   OID đủ 40 hex, không viết tắt
command -v git sort comm wc grep python > "$T/cong_cu"                     # (0)   rc=0 VÀ đúng 6 dòng
git rev-parse --is-shallow-repository > "$T/nong"                          # (0)   rc=0, nội dung đúng `false`
git remote get-url --all origin > "$T/endpoint"                            # (0)   rc=0, đúng 1 dòng
grep -c -x -F -e https://github.com/ducthangho/tra-luat -e https://github.com/ducthangho/tra-luat.git "$T/endpoint" > "$T/endpoint.khop"   # (0)   rc=0, nội dung `1`
git config --get-regexp '^(remote[.]origin|url)[.]' > "$T/cau_hinh"        # (0)   rc=0
wc -l < "$T/cau_hinh" > "$T/cau_hinh.dem"                                  # (0)   rc=0
grep -c -x -F -e 'remote.origin.url https://github.com/ducthangho/tra-luat' -e 'remote.origin.url https://github.com/ducthangho/tra-luat.git' -e 'remote.origin.fetch +refs/heads/*:refs/remotes/origin/*' -e 'url.https://github.com/.insteadof git@github.com:' -e 'url.https://github.com/.insteadof ssh://git@github.com/' "$T/cau_hinh" > "$T/cau_hinh.khop"   # (0)   rc=0, bằng `cau_hinh.dem`
git fetch origin '+refs/heads/*:refs/remotes/origin/*'                    # (i)   rc=0
git merge --ff-only refs/remotes/origin/master                             # (i)   rc=0
git ls-remote --heads origin > "$T/may_chu.raw"                            # (ii)  rc=0
sort "$T/may_chu.raw" > "$T/mc"                                            # (iii) rc=0
git for-each-ref --format='%(objectname)%09refs/heads/%(refname:lstrip=3)' refs/remotes/origin > "$T/cb.raw"   # (iii) rc=0
sort "$T/cb.raw" > "$T/cb"                                                 # (iii) rc=0
git for-each-ref --format='%(objectname)%09refs/heads/master' refs/remotes/origin/master > "$T/master"         # (iii) rc=0
comm -23 "$T/mc" "$T/cb" > "$T/thieu"                                      # (iii) rc=0
comm -13 "$T/mc" "$T/cb" > "$T/thua"                                       # (iii) rc=0
comm -12 "$T/mc" "$T/cb" > "$T/chung"                                      # (iii) rc=0
comm -12 "$T/master" "$T/chung" > "$T/master.chung"                        # (iii) rc=0
wc -l "$T/may_chu.raw" "$T/mc" "$T/chung" "$T/thieu" "$T/master" "$T/master.chung" > "$T/dem"   # (iii) rc=0
git hash-object ops/lease_publish.py > "$T/cong_cu.oid"                    # (iv)  rc=0
git rev-parse "$NEN:ops/lease_publish.py" > "$T/nen.oid"                   # (iv)  rc=0
git hash-object "$T/s5.py" > "$T/s5.oid"                                   # (iv)  rc=0, nội dung đúng `c730245ceea8cc5368d5ef84f8e296cd35102694`
python ops/lease_publish.py ai-dang-giu ops/lease_publish.py > "$T/adg.1" 2>&1        # (iv)  rc=0
grep -c -x -F 'NGƯỜI_GIỮ 0: không có' "$T/adg.1" > "$T/adg.1.khop"                     # (iv)  rc=0, nội dung `1`
python ops/lease_publish.py ai-dang-giu ops/lease_publish_test.py > "$T/adg.2" 2>&1   # (iv)  rc=0
grep -c -x -F 'NGƯỜI_GIỮ 0: không có' "$T/adg.2" > "$T/adg.2.khop"                     # (iv)  rc=0, nội dung `1`
python "$T/s5.py" ops/lease_publish.py ops/lease_publish_test.py > "$T/s5.out" 2>&1     # (iv)  rc=0
grep -c -x -F 'S5 TỰ_KIỂM 38/38 đạt; NGƯỜI_GIỮ 0 ở 2/2 đường dẫn' "$T/s5.out" > "$T/s5.khop"   # (iv)  rc=0, nội dung `1`
git diff --quiet "$NEN" refs/remotes/origin/master -- ops/lease_publish.py ops/lease_publish_test.py   # (v)   rc=0
git ls-tree refs/remotes/origin/master -- ops/lease_publish.py ops/lease_publish_test.py > "$T/v.ls"  # (v)   rc=0, đúng 2 dòng
git merge-base --is-ancestor "$M689" refs/remotes/origin/master            # (vi)  rc=0
git merge-base --is-ancestor "$M689" "$NEN"                                # (vi)  rc=0
# (vii) chạy lại nguyên văn mọi dòng (ii) và (iii) ở trên, cùng tiêu chí
```

**`s5.py`** (bước (iv), từ r12; bản r13). Nội dung giữa hai dòng rào dưới đây, mỗi dòng kết thúc bằng LF: 207 dòng, OID git
blob `c730245ceea8cc5368d5ef84f8e296cd35102694`, sha256 `708790485694de7d2379928fec30f09dd8491803677764c94b2c7a55841d02f6`.
Nó không ghi gì vào kho. Nó nạp `ops/lease_publish.py` của cây làm việc (blob đã được so với blob của nền ở dòng
`cong_cu.oid`), thay hai thứ: hàm `_lease_cham_duong`, và lệnh `ls-tree -r` mà `ai-dang-giu` dùng để liệt kê tệp lease
(bọc `GOI_GIT`); rồi gọi `main(["ai-dang-giu", <đường dẫn>])` cho từng đường dẫn. Vì vậy miền ref, phép so tên nhánh máy
chủ, luật hạn, luật bia mộ và mã thoát là của chính `ai-dang-giu`; chỉ phép khớp đường dẫn là theo PROTOCOL §5, và mục
write set chỉ diễn giải được khi qua danh sách CHO PHÉP: chuỗi, hay ánh xạ chỉ có khoá `type`, `path` với `type` là `exact`
hay `prefix`; mọi ký tự thuộc bảng chữ của đường dẫn trong kho; không đoạn nào rỗng, là `.`, `..` hay kết thúc bằng `.`.
Tên tệp lease được liệt kê không qua nháy kiểu C của git. Mục cây mà dòng dựng lại không còn là đúng một dòng dưới
`str.splitlines` (tên có ký tự ngắt dòng), hay mục không phải tệp thường (mode khác `100644`, `100755`: gitlink, symlink),
làm lệnh liệt kê ra rc=1, nên `ai-dang-giu` ra 12. Trước khi quét, nó tự kiểm 38 ca (32 ca `CA` của phép khớp, 6 ca của
`bao_goi_git`); sai một ca thì rc=12 và không quét. Dòng kết luận chỉ in khi mọi đường dẫn ra `NGƯỜI_GIỮ 0` (rc=0); có
người giữ thì rc=11; `ai-dang-giu` chặn thì rc=12. Lịch sử: r12 ghim bản 112 dòng (OID `2f6bde6c…2e01`, 25 ca); HINT lượt
12 đề xuất bản 174 dòng (OID `b70ca3a8…55f0`, 31 ca), mà phiên soạn r13 đo được là CẤP ở mười kịch bản mà bản r13 không cấp
(§9, §10), nên r13 không ghim bản ấy.

```python
"""s5.py — bước (iv) của chuỗi cấp wp678 (đặc tả r13): ai đang giữ đường dẫn, khớp theo PROTOCOL §5.

Gọi từ gốc clone: python <T>/s5.py <đường dẫn> ...   Không ghi gì vào kho.
Dùng NGUYÊN lenh_ai_dang_giu của ops/lease_publish.py (quét ref, so tên nhánh máy chủ, hạn, bia mộ);
chỉ thay _lease_cham_duong: đọc write_set VÀ effective_write_set; mục chuỗi hay ánh xạ {type, path};
đường dẫn chính xác hoặc prefix thư mục; đổi separator, NFC, case-fold, bỏ tiền tố planned:.
Mục không diễn giải được tính là PHỦ (fail-close). Diễn giải được = danh sách CHO PHÉP: mục là chuỗi, hay ánh xạ chỉ có
khoá `type`, `path` với `type` là `exact` hay `prefix` (PROTOCOL §3.2); mọi ký tự của đường dẫn (sau khi đổi separator,
bỏ khoảng trắng hai đầu và bỏ `planned:`) thuộc BANG_CHU, bảng chữ của đường dẫn trong kho (chỉ `A-Za-z0-9`, `-`, `.`,
`/`, `_`); không đoạn nào rỗng, là `.`/`..` hay kết thúc bằng `.`. Tự kiểm CA trước khi quét; sai một ca thì rc=12.
Lớp liệt kê tệp: `ls-tree -r` không `-z` của `_quet_lease_toan_kho` bọc tên tệp không-ASCII (hay có dấu nháy kép, dấu
chéo ngược) trong nháy kiểu C nên bộ lọc đuôi `.yaml` bỏ qua tệp lease ấy; `bao_goi_git` gọi lại bằng `-z`, dựng lại
dòng không nháy và đưa đuôi `.YAML`/`.YML` về chữ thường. Mục mà dòng dựng lại không còn là đúng MỘT dòng dưới
`str.splitlines` (tên có ký tự ngắt dòng), hay không phải tệp thường (mode khác 100644/100755: gitlink, symlink),
làm lời gọi ra rc=1 nên `ai-dang-giu` ra 12.
"""
import importlib.util
import sys
import unicodedata

CHEO = chr(92)
NUL, TAB, LF = chr(0), chr(9), chr(10)
BANG_CHU = frozenset("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._/-")
KHONG_DIEN_GIAI = []


def bao_goi_git(goi_goc):
    """Bọc GOI_GIT của ops/lease_publish.py: `ls-tree -r` không `-z` ⇒ gọi lại bằng `-z`, đổi NUL thành xuống dòng
    (dạng `meta<TAB>đường dẫn` KHÔNG nháy), đuôi tệp lease về chữ thường; mục mà dòng dựng lại không là đúng một dòng
    dưới `splitlines` (thứ `_quet_lease_toan_kho` dùng để tách), hay không phải tệp thường, ⇒ rc=1; lệnh khác giữ nguyên."""
    def goi(*a, cwd=None):
        if len(a) > 2 and a[0] == "ls-tree" and a[1] == "-r" and "-z" not in a:
            p = goi_goc("ls-tree", "-r", "-z", *a[2:], cwd=cwd)
            if p.returncode == 0:
                dong = []
                for muc in p.stdout.split(NUL):
                    meta, tab, duong = muc.partition(TAB)
                    if tab and duong.lower().endswith((".yaml", ".yml")):
                        duong = duong[:duong.rindex(".")] + duong[duong.rindex("."):].lower()
                    x = meta + tab + duong
                    if muc and x.splitlines() != [x]:
                        p.returncode, p.stderr = 1, f"s5: tên có ký tự ngắt dòng: {muc!r}"
                        return p
                    if muc and meta.split()[:2] not in (["100644", "blob"], ["100755", "blob"]):
                        p.returncode, p.stderr = 1, f"s5: mục không phải tệp thường: {muc!r}"
                        return p
                    dong.append(x)
                p.stdout = LF.join(dong)
            return p
        return goi_goc(*a, cwd=cwd)
    return goi


def chuan(s):
    s = unicodedata.normalize("NFC", s.replace(CHEO, "/").strip())
    return unicodedata.normalize("NFC", s.casefold()).removeprefix("planned:")


def phu(muc, dich):
    """True hay False khi diễn giải được mục write set; None khi không."""
    if isinstance(muc, dict):
        if not set(muc) <= {"type", "path"}:
            return None
        if muc.get("type") not in ("exact", "prefix"):
            return None
        muc = muc.get("path")
    if not isinstance(muc, str):
        return None
    r = muc.replace(CHEO, "/").strip()
    if r[:8].lower() == "planned:":
        r = r[8:]
    if not r or any(c not in BANG_CHU for c in r):
        return None
    m = chuan(r)
    doan = m.rstrip("/").split("/")
    if m.startswith("/") or any(x in ("", ".", "..") for x in doan):
        return None
    if any(x.endswith(".") for x in doan):
        return None
    goc = "/".join(doan)
    d = chuan(dich)
    return d == goc or d.startswith(goc + "/")


def cham(lease, dich):
    kq = False
    for khoa in ("write_set", "effective_write_set"):
        ws = lease.get(khoa)
        if ws is None:
            continue
        for muc in (ws if isinstance(ws, list) else [ws]):
            p = phu(muc, dich)
            if p is None:
                KHONG_DIEN_GIAI.append(f"{lease.get('lease_id')!r} {khoa} {muc!r}")
                return True
            kq = kq or p
    return kq


T, P = "ops/lease_publish_test.py", "ops/lease_publish.py"
CA = [
    ({"write_set": [T]}, T, True),
    ({"write_set": ["ops/"]}, T, True),
    ({"write_set": ["ops"]}, P, True),
    ({"write_set": ["planned:ops/"]}, T, True),
    ({"write_set": ["Ops/Lease_Publish_Test.py"]}, T, True),
    ({"write_set": ["OPS/"]}, P, True),
    ({"write_set": ["ops/lea" + chr(0x17F) + "e_publish_test.py"]}, T, True),
    ({"write_set": ["ops/cafe" + chr(0x301) + "/"]}, "ops/caf" + chr(0xE9) + "/x.py", True),
    ({"write_set": [{"type": "prefix", "path": "ops/"}]}, T, True),
    ({"write_set": [{"type": "exact", "path": T}]}, T, True),
    ({"effective_write_set": ["ops/"]}, P, True),
    ({"write_set": "ops/"}, T, True),
    ({"write_set": ["ops" + CHEO + "lease_publish_test.py"]}, T, True),
    ({"write_set": ["ops/*"]}, T, True),
    ({"write_set": ["../ops/"]}, T, True),
    ({"write_set": [7]}, T, True),
    ({"write_set": [T]}, P, False),
    ({"write_set": ["planned:" + P]}, T, False),
    ({"write_set": ["ops/lease"]}, T, False),
    ({"write_set": ["ops/leases/"]}, T, False),
    ({"write_set": ["opsx/"]}, T, False),
    ({"write_set": [T + "c"]}, T, False),
    ({"write_set": []}, T, False),
    ({"write_set": None}, T, False),
    ({}, T, False),
    ({"write_set": ["ops/lease_publish.py" + LF + T]}, T, True),
    ({"write_set": ["ops/lease_publish.py, " + T]}, T, True),
    ({"write_set": ["ops/{lease_publish,lease_publish_test}.py"]}, T, True),
    ({"write_set": ["ops/lease_publish.py " + T]}, T, True),
    ({"write_set": [{"type": "regex", "path": "ops/lease_publish_tes..py"}]}, T, True),
    ({"write_set": [{"type": "exact", "path": "ops/khac.py", "them": T}]}, T, True),
    ({"write_set": [T + "."]}, T, True),
]


class Gia:
    def __init__(self, so):
        self.stdout, self.returncode, self.stderr = so, 0, ""


CA_GOI_GIT = ("a", "b", "c", "d", "e", "f")


def tu_kiem_goi_git():
    """Sáu ca của `bao_goi_git`: (a) `ls-tree -r` không `-z` ⇒ gọi `-z`, tên không-ASCII và tên có nháy kép hiện KHÔNG
    nháy, đuôi hoa về thường; (b) lệnh khác và `ls-tree -r -z` đi nguyên; (c) tên chứa LF, (d) tên chứa U+2028, cả hai
    dựng thêm một dòng `meta<TAB>đường dẫn` giả trỏ blob khác, ⇒ rc khác 0; (e) gitlink, (f) symlink ⇒ rc khác 0."""
    goi_ra, sai = [], []
    A, B = "100644 blob " + "a" * 40 + TAB, "100644 blob " + "b" * 40 + TAB
    def gia_tra(so):
        def gia(*a, cwd=None):
            goi_ra.append(a)
            return Gia(so)
        return gia
    gia = gia_tra(A + "ops/leases/" + chr(0xE9) + ".yaml" + NUL + B + "ops/leases/q" + chr(34) + "x.YML" + NUL)
    p = bao_goi_git(gia)("ls-tree", "-r", "refs/x", "--", "ops/leases", cwd=".")
    if goi_ra[0][:3] != ("ls-tree", "-r", "-z") or p.returncode != 0 or p.stdout.split(LF) != [
            A + "ops/leases/" + chr(0xE9) + ".yaml", B + "ops/leases/q" + chr(34) + "x.yml", ""]:
        sai.append("a")
    goi_ra.clear()
    bao_goi_git(gia)("rev-parse", "HEAD", cwd=".")
    bao_goi_git(gia)("ls-tree", "-r", "-z", "refs/x", cwd=".")
    if goi_ra != [("rev-parse", "HEAD"), ("ls-tree", "-r", "-z", "refs/x")]:
        sai.append("b")
    for ten, so in (("c", A + "ops/leases/z" + LF + B + "z2.yaml" + NUL),
                    ("d", A + "ops/leases/z" + chr(0x2028) + B + "z2.yaml" + NUL),
                    ("e", "160000 commit " + "c" * 40 + TAB + "ops/leases/con" + NUL),
                    ("f", "120000 blob " + "d" * 40 + TAB + "ops/leases/ln.yaml" + NUL)):
        if bao_goi_git(gia_tra(so))("ls-tree", "-r", "refs/x", "--", "ops/leases", cwd=".").returncode == 0:
            sai.append(ten)
    return sai


def main(argv):
    sai = [i for i, (lease, dich, mong) in enumerate(CA) if cham(lease, dich) is not mong]
    sai += ["goi_git:" + x for x in tu_kiem_goi_git()]
    KHONG_DIEN_GIAI.clear()
    if sai:
        print(f"S5 TỰ_KIỂM sai ở ca {sai}")
        return 12
    if not argv:
        print("S5 thiếu đường dẫn")
        return 2
    spec = importlib.util.spec_from_file_location("lease_publish_s5", "ops/lease_publish.py")
    lp = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(lp)
    lp._lease_cham_duong = cham
    lp.GOI_GIT = bao_goi_git(lp.GOI_GIT)
    rcs = []
    for duong in argv:
        print(f"== {duong}")
        sys.stdout.flush()
        rcs.append(lp.main(["ai-dang-giu", duong]))
        sys.stdout.flush()
    for x in KHONG_DIEN_GIAI:
        print(f"KHÔNG_DIỄN_GIẢI: {x}")
    if all(r == 0 for r in rcs):
        so = len(CA) + len(CA_GOI_GIT)
        print(f"S5 TỰ_KIỂM {so}/{so} đạt; NGƯỜI_GIỮ 0 ở {len(rcs)}/{len(argv)} đường dẫn")
        return 0
    print(f"S5 rc theo đường dẫn: {rcs}")
    return 12 if 12 in rcs else max(rcs)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

**Nguyên lý, áp cho mọi bước.** Review lượt 10 chạy đúng từng dòng chuỗi r10 và thấy nó CẤP nhầm ở bốn ca; phiên
soạn r11 liệt kê hết các đường cùng cơ chế trước khi viết lại (§9, §10). Chuỗi chỉ được kết luận từ **bằng chứng
DƯƠNG**: (a) rc của TỪNG lệnh là 0, đọc ngay sau lệnh; không có pipeline (rc của pipeline là rc của lệnh cuối) và
không có `$(…)`; (b) mỗi kết quả là một giá trị cụ thể so BẰNG giá trị mong đợi, không phải "không thấy lệch":
`thieu` 0 dòng chỉ được đọc khi `may_chu.raw`, `mc`, `chung` cùng một số dòng ≥ 1 và dòng `master` của máy chủ có
trong `chung`; (c) mọi tên là tên đầy đủ: `refs/remotes/origin/master`, OID 40 hex; (d) thứ được đo là đúng thứ được
khai: endpoint và cấu hình chọn đường vận chuyển thuộc danh sách CHO PHÉP, công cụ đo là blob của nền và `s5.py` là
blob ghim, phép khớp write set là phép khớp của PROTOCOL §5, object đọc không qua `refs/replace`; (e) đọc theo thứ tự
bước: bước đầu tiên không đạt tiêu chí quyết định nhãn.

| bước | đạt khi và chỉ khi |
|---|---|
| (0) | mọi dòng rc=0; `cong_cu` đúng 6 dòng; `nong` đúng `false`; `endpoint` đúng 1 dòng; `endpoint.khop` đúng `1`; `cau_hinh.khop` = `cau_hinh.dem` (≥ 1) |
| (i) | `fetch` rc=0; `merge --ff-only` rc=0 |
| (ii), (iii) | mọi dòng rc=0; trong `dem`: `may_chu.raw` = `mc` = `chung` ≥ 1, `thieu` = 0, `master` = `master.chung` = 1 |
| (iv) | mọi dòng rc=0; `cong_cu.oid` = `nen.oid` (40 hex); `s5.oid` = OID ghi ở dòng ấy; `adg.1.khop` = `adg.2.khop` = `s5.khop` = `1` |
| (v) | `diff --quiet` rc=0; `v.ls` đúng 2 dòng |
| (vi) | hai dòng rc=0 |
| (vii) | như (ii), (iii) |

`thieu` khác 0 trong khi mọi dòng của (ii), (iii) (hay (vii)) rc=0 và `may_chu.raw` = `mc` ≥ 1 ⇒ đệm lệch máy chủ ⇒ chạy lại cả chuỗi từ đầu
MỘT lần; vẫn lệch ⇒ `KHÔNG_XÁC_ĐỊNH`. `ai-dang-giu` hay `s5.py` rc=11 (`NGƯỜI_GIỮ` khác 0), `diff --quiet` rc=1, hay
`merge-base` rc=1 ⇒ điều kiện không thoả ⇒ **không cấp**. Mọi trường hợp khác không đạt bảng trên ⇒
`KHÔNG_XÁC_ĐỊNH` ⇒ không cấp. Danh sách cho phép của endpoint là đúng hai chuỗi trong dòng `grep` ở (0), khớp nguyên
dòng; dạng khác (đường dẫn tệp, `file://`, URL có phần xác thực, URL qua proxy cục bộ, kho khác) ⇒ `KHÔNG_XÁC_ĐỊNH`,
handoff ghi nó với phần xác thực đã che; thêm một dạng là đổi đặc tả, tức revision mới. Không viết *"mọi điều kiện
khác đạt"* cho quy tắc chạy lại: `chung` = `mc` − `thieu`, nên `mc` = `chung` kéo theo `thieu` = 0, và đọc từng chữ thì
quy tắc ấy không bao giờ thoả (review lượt 11 đo S4, S5, S8c: KXĐ ngay lần đầu). Cùng luật danh sách cho phép áp cho
`cau_hinh`: danh sách là đúng năm chuỗi trong dòng `grep` thứ hai ở (0), khớp nguyên dòng; mọi dòng khác của
`remote.origin.*` hay `url.*` (`vcs`, `proxy`, `uploadpack`, `pushurl`, `promisor`, `url` thứ hai, `insteadOf` hay
`pushInsteadOf` khác, phần thừa của một giá trị nhiều dòng…) làm `cau_hinh.khop` khác `cau_hinh.dem` ⇒
`KHÔNG_XÁC_ĐỊNH`, handoff ghi nguyên văn với phần xác thực đã che; thêm một dòng vào danh sách là đổi đặc tả, tức
revision mới. `s5.py` có dòng kết luận khác dòng `grep` ở (iv), hay rc khác 0 và 11, ⇒ `KHÔNG_XÁC_ĐỊNH`. Đọc theo thứ
tự bước: bước đầu tiên không đạt tiêu chí quyết định nhãn (không cấp hay `KHÔNG_XÁC_ĐỊNH`); các bước sau vẫn chạy và
vẫn ghi vào handoff.

Vì sao từng bước (đo ở §10, mục *Ref đệm cũ*). `ai-dang-giu` tự so tập tên chiều thiếu cục bộ (`ops/lease_publish.py`
:300–309, :507–511) nhưng không `fetch` và không so OID, nên ref CŨ cùng tên lọt qua nó và qua lệnh (4) (hai ca của
lượt 9); `fetch` xong chưa chứng minh đệm khớp máy chủ lúc so (máy chủ đổi ngay sau `fetch`), nên có (ii), (iii) và
lặp ở (vii); thiếu `merge --ff-only` thì `ai-dang-giu` ra `CHẶN [12]`; (vii) vì (iv)–(vi) mất 19 và 22 giây ở hai
lượt đo r10, cả 40 bước mất 47 giây ở lượt đo r11, ở lượt đo r12 bước (iv) mất 50 giây, cả 46 bước 52 giây, và ở lượt đo r13 bước (iv) mất 56 giây, cả 46 bước 58 giây
(tải máy trung bình khoảng 6,8 trên 4 lõi). `git remote get-url --all` in đúng URL mà `fetch` và
`ls-remote` dùng: nó đã áp `insteadOf` (cả cấu hình kho lẫn biến `GIT_CONFIG_*`), và khi `remote.origin.url` có hai
giá trị thì cả ba cùng dùng giá trị đầu; đòi đúng 1 dòng để không phải dựa vào thứ tự ấy. `GIT_DIR` trỏ kho khác thì
`get-url` in origin của kho ấy, nên endpoint vẫn là phép đo đúng. `command -v` có tên vắng vẫn rc=0, nên phải đếm
dòng. Định dạng `for-each-ref` ở (iii) dựng sẵn đúng dạng dòng của `ls-remote` (OID, tab, `refs/heads/<tên>`), nên
không cần `awk` hay `grep -v`; dòng `refs/heads/HEAD` sinh từ `refs/remotes/origin/HEAD` rơi vào `thua`, vô hại.
`GIT_NO_REPLACE_OBJECTS=1` vì `ai-dang-giu` đọc lease bằng `ls-tree` không tắt replace: một `refs/replace` cục bộ thay
đầu nhánh có lease còn hạn làm nó ra `NGƯỜI_GIỮ 0`. Blob công cụ so với blob của nền vì chuỗi chạy
`ops/lease_publish.py` của cây làm việc: bản bị sửa mà chưa commit vẫn chạy. Tên `refs/remotes/origin/master` và OID
đủ 40 hex vì tên ngắn bị che: `origin/master` bởi tag hay nhánh cục bộ cùng tên (review lượt 10 đo), OID viết tắt bởi
nhánh mang đúng mấy ký tự ấy (git chỉ cảnh báo trên stderr rồi dùng ref), còn OID đủ 40 hex thì git dùng object.
`git ls-tree` ở (v) vì `git diff --quiet` trên đường dẫn không có ở cả hai rev cũng rc=0; giữ `diff --quiet` vì chỉ
nó thấy đổi mode (cùng blob, khác mode ⇒ rc=1). Dòng `master` ở (iii) là bằng chứng dương rằng ref mà (v), (vi) đọc
đã được so với máy chủ. Dòng `nong` là chốt CHẨN ĐOÁN: kho nông chỉ làm `merge-base --is-ancestor` ra sai âm tính
(không cấp), không làm cấp nhầm; nó đổi trường hợp ấy thành `KHÔNG_XÁC_ĐỊNH` thay vì "không phải tổ tiên".

Vì sao bước (0) cấu hình và bước (iv) `s5.py` (r12; review lượt 11 đo hai đường, phiên soạn r12 liệt kê và đo thêm,
§10). **Cấu hình.** `git remote get-url --all` in URL mà `fetch` và `ls-remote` dùng (đã áp `insteadOf`), nhưng không in
CHƯƠNG TRÌNH nói với URL ấy: `remote.origin.vcs` đưa `fetch`, `ls-remote` qua `git-remote-<vcs>` (N3 của review lượt 11),
`remote.origin.uploadpack` thay chương trình phía máy chủ của đường vận chuyển cục bộ, và các khoá ấy tới từ cấu hình
kho, `include.path`, `includeIf`, `GIT_CONFIG_GLOBAL`, `GIT_CONFIG_PARAMETERS` hay `GIT_CONFIG_COUNT` như nhau. Đo (kho
tạm, git 2.43.0, 07-10): `git config --get-regexp '^(remote[.]origin|url)[.]'` hiện dòng `remote.origin.*` thêm vào
từ cả sáu nguồn ấy; một giá trị nhiều dòng tách thành dòng thừa nên rơi khỏi danh sách cho phép; `get-url --all` áp
`insteadOf` mà không áp `pushInsteadOf` (`get-url --push` mới áp). Chuỗi r11 CẤP nhầm ở năm đường (`vcs` trong cấu hình
kho, qua `include.path`, qua `GIT_CONFIG_PARAMETERS`, qua `GIT_CONFIG_GLOBAL`; `uploadpack`), chuỗi r11 + HINT và chuỗi
r12 bắt cả năm (§10). `url.*` vào danh sách theo chỉ thị của phiên điều phối, và nói thẳng: nó KHÔNG đóng thêm đường cấp
nhầm nào trong bộ thử, vì `insteadOf` viết lại URL của `fetch` thì endpoint đã bắt (S11, S12), còn `pushInsteadOf` không
chạm `fetch` hay `ls-remote`; nó làm danh sách cho phép phủ trọn họ khoá viết lại URL, với giá là một dòng `url.*` vô hại
ngoài danh sách cũng ra KXĐ (§10). Danh sách cho phép đúng hai dòng `url.*` mà container phiên soạn có
sẵn ở phạm vi command (viết lại `git@github.com:` và `ssh://git@github.com/` sang `https://github.com/`, không chạm URL
`https://`). Biểu thức chính quy viết bằng `[.]` thay cho dấu chấm thoát.
**Phép khớp write set.** `ai-dang-giu <đường dẫn>` so mục `write_set` bằng NGUYÊN CHUỖI (`_lease_cham_duong`,
`ops/lease_publish.py` :704–708 trên `ab457c6`, :545–549 trên `163fd5d`): mục phải là chuỗi, chỉ bỏ `planned:`, so
bằng. PROTOCOL §5 (:297, :299–302 trên `ab457c6`) cho write set dạng đường dẫn chính xác hoặc prefix thư mục, đòi đổi
separator, NFC và case-fold trước khi so giao; lược đồ §3.2 (:149–151) viết mục dạng `{type, path}`; và loại trừ là trên
EFFECTIVE write set (:32, :322, :329). Vì vậy một lease còn hạn viết theo các dạng ấy giữ hai tệp mà `ai-dang-giu` ra
`NGƯỜI_GIỮ 0`. Ngoài ba đường của review lượt 11 (`ops/`, `Ops/Lease_Publish_Test.py`, `{type: prefix, path: ops/}`),
phiên soạn r12 tự liệt kê thêm mười đường cùng cơ chế: prefix không có `/` cuối, `planned:ops/`, prefix viết hoa, ký tự
Unicode case-fold về ASCII (`ſ` U+017F), mục ánh xạ `exact`, mục ánh xạ prefix không `/`, chỉ `effective_write_set`,
`write_set` vô hướng, glob, separator ngược. HINT lượt 11 (`ai-dang-giu ops/`) đóng hai trong mười ba (`ops/`,
`planned:ops/`), chuỗi r11 không đóng đường nào, chuỗi r12 đóng cả mười ba (§10).
**Vì sao `s5.py` mà không sửa `_lease_cham_duong` trong lượt thi hành** (câu hỏi của phiên điều phối: (a) chuỗi tự quét
theo luật PROTOCOL bằng script nhúng có ca thử, hay (b) sửa `_lease_cham_duong` nếu đã thuộc objective và write set). (b)
KHÔNG hợp lệ, đo được: `ops/lease_publish.py` thuộc write set, nhưng objective và §6 mục 1–8 chiếu đúng vào các đường
D1–D8 mà `grep -n lease_id` liệt kê (§2); thân `_lease_cham_duong` (:704–708) không đọc `lease_id` (0 lần) và chỉ
có một lời gọi, trong `lenh_ai_dang_giu` (:2267); sửa nó đổi ngữ nghĩa `ai-dang-giu` cho mọi người dùng, tức thêm một
mục tiêu, mà theo PROTOCOL §3.2 (:163–164 trên `ab457c6`) đổi objective là revision mới, còn phát hiện ngoài spec thì
xuất handoff chứ agent không tự mở write set (:179–181); §5 của đặc tả này cũng xếp cùng họ lỗi ngoài quyết định chủ kho vào phát hiện ngoài spec.
Vậy chọn (a), và ghi phát hiện ngoài spec (mục *Giới hạn*). `s5.py` không vá `ai-dang-giu`: nó chạy nguyên
`lenh_ai_dang_giu` và chỉ thay phép khớp trong chính tiến trình của mình, nên phần còn lại (ref, hạn, bia mộ, mã thoát)
là của công cụ đã đo; phép khớp của nó là tập TRÊN của phép khớp nguyên chuỗi (mục khớp nguyên chuỗi cũng khớp §5),
nên nó chỉ có thể thêm người giữ, không bớt. Mục không diễn giải được tính là PHỦ: lease còn hạn mang mục như thế làm
chuỗi không cấp (fail-close; giá là tính sống). **Diễn giải được là danh sách CHO PHÉP, không phải danh sách cấm.** Bản r12 liệt kê các dạng không
diễn giải được (không phải chuỗi hay ánh xạ có `path` chuỗi; rỗng; tuyệt đối; có `:`; có đoạn `.`, `..` hay rỗng; có ký tự
glob) và để lọt năm dạng `write_set` mà `kiem()` vẫn nhận (đăng được; review lượt 12 đo `kiem()` ở `ab457c6`, `lease_id`
hợp lệ): khối văn bản hai dòng, một chuỗi có dấu phẩy, ngoặc nhọn, hai đường dẫn cách bằng khoảng trắng, hai đường dẫn cách
bằng chấm phẩy; cả năm CẤP nhầm (đối chứng ASCII KHÔNG CẤP). HINT lượt 12 đảo phần KÝ TỰ sang danh sách cho phép, nhưng ở
tầng HÌNH DẠNG thì vẫn là danh sách cấm: `phu()` của nó đọc `path` của mục ánh xạ mà bỏ qua `type` và mọi khoá khác. Phiên
soạn r13 đo (`kiem()` của `ab457c6` trên `_lease_v2` của suite, lớp `sensitive`, 3.11.15 và 3.12.3, 12:52Z 07-10): bốn
dạng dưới đều QUA cổng đăng, và chuỗi đã áp HINT CẤP ở cả bốn khi một lease CÒN HẠN mang chúng (§10): `{type: regex, path:
'ops/lease_publish_tes..py'}` (PROTOCOL §3.2 chỉ cho `exact | prefix`; đọc như regex thì mục ấy phủ tệp);
`{type: exact, path: ops/khac.py, them: ops/lease_publish_test.py}` (khoá ngoài lược đồ); `{path: ops/lease_publish_tes}`
(thiếu `type`); `ops/lease_publish_test.py.` (đoạn kết thúc bằng dấu chấm: Win32 bỏ dấu chấm cuối khi chuẩn hoá đường dẫn;
hành vi NTFS `KHÔNG ĐO ĐƯỢC` ở đây, và git 2.43.0 với `core.protectNTFS=true` không từ chối tên ấy, đo 12:1xZ). Nay mục
diễn giải được khi và chỉ khi: là chuỗi, hay ánh xạ chỉ có khoá `type`, `path` với `type` đúng `exact` hay `prefix` và `path`
là chuỗi; mọi ký tự của đường dẫn, sau khi đổi separator, bỏ khoảng trắng hai đầu và bỏ `planned:`, thuộc bảng chữ
`A-Za-z0-9._/-`; các đoạn không rỗng, không là `.`/`..`, không kết thúc bằng `.`. Bảng chữ lấy từ kho, đo lại ở `adg2`
(12:17Z 07-10, MỌI ref `refs/heads` và `refs/remotes` trừ `*/HEAD`, tức 473 ref; `do_adg2.py` ở scratch): hợp các đường dẫn
của mọi cây là 3986 đường dẫn, 0 ký tự ngoài bảng (review lượt 12 đo 2766 đường dẫn trên riêng cây `ab457c6`). Mọi mục write
set trên 473 ref (589 cặp `(blob, đường dẫn)` lease dưới `ops/leases/`, 0 lỗi parse; 12:18Z): `write_set` 1407 mục (1384
chuỗi chính xác, 23 chuỗi prefix như `ops/reviews/`), `effective_write_set` 123 mục chuỗi ở 21 cặp, cộng 2 cặp khai
`null` (23 cặp có khoá; bộ đếm `co_khoa_effective` của `do_dem.py` tính cả cặp `null`), 0 mục ánh xạ, 0 đoạn kết thúc bằng dấu chấm, **0 mục không diễn giải được theo luật r13**; 59 cặp không có khoá
nào trong hai khoá (39 khai `scope_files`, 6 `scope_files_can_xet`, 6 `delta_scope_files`, 8 không trường phạm vi nào; cả 59
`HẾT_HẠN`), nên không giữ gì. Vậy lúc đo, luật r13 không
chặn lease nào; 6 cặp `CÒN_HẠN` lúc 12:18Z (của wp685 và wp710) đều diễn giải được và không chạm hai tệp. Giá, nói thẳng:
một lease còn hạn có mục ngoài danh sách cho phép (không-ASCII, khoảng trắng, `type` lạ, khoá lạ, dấu chấm cuối) chặn mọi
lần cấp tới lúc nó hết hạn; thêm ký tự hay hình dạng vào danh sách là đổi đặc tả. `planned:` bị bỏ trước khi kiểm bảng chữ.
Mục exact trỏ một thư mục tổ tiên cũng tính là phủ (chặt hơn §5, có chủ đích). Mỗi chốt có ca tự kiểm riêng và kịch bản
chuỗi riêng làm nó ĐỎ khi bị gỡ (§10, *Chuỗi lệnh r13 trên bộ thử*). Ở lượt chạy thật, `s5.py` liệt kê đúng tập lease
của `ai-dang-giu` cho từng đường dẫn (hàng `depends_on`).

**Giới hạn, nói thẳng.** Chuỗi này **thu hẹp** cửa sổ giữa đo và cấp, **không đóng** nó: đo rồi cấp không nguyên tử.
Nó kiểm URL endpoint và các khoá `remote.origin.*`, `url.*`, KHÔNG kiểm danh tính máy chủ sau tầng vận chuyển: một proxy
hay tầng vận chuyển trả danh sách nhánh bị cắt bớt thì `ls-remote` của chuỗi lẫn `ls-remote` bên trong `ai-dang-giu` và
`s5.py` cùng thiếu dòng ấy, và chuỗi CẤP (phiên soạn r11 đo, §10, S15; phiên soạn r12 đo lại cùng kết quả). Trạng thái
ấy `KHÔNG ĐO ĐƯỢC` bằng git: từ phía client nó giống hệt một nhánh đã xoá trên máy chủ (một dòng `thua`); một kênh thứ
hai (REST `git/matching-refs/heads/`, MCP github) chỉ bắt được cắt bớt riêng ở kênh git, vì mọi kênh của container cùng
đi qua một proxy. Cùng lớp, và cũng `KHÔNG ĐO ĐƯỢC` từ chuỗi: cấu hình `http.*` và biến môi trường chọn proxy hay chọn
nguồn tin TLS (`HTTPS_PROXY`, `http.proxy`, `http.<url>.proxy`, `http.sslVerify`, `GIT_SSL_CAINFO`; container phiên soạn
đặt `HTTPS_PROXY` và `GIT_SSL_CAINFO` trong môi trường cùng `http.proxyauthmethod` ở cấu hình global, đo tên chứ không in
giá trị, tức đi qua một proxy với CA riêng, nên không có giá trị nào để ghim), và `GIT_EXEC_PATH`
(chọn bản `git-remote-https`). `core.gitProxy`, `core.sshCommand`, `GIT_SSH_COMMAND` chỉ áp cho đường `git://` và
`ssh://`, mà endpoint chỉ cho `https://`. Fence trước merge/land cũng đòi ghi endpoint (PROTOCOL :395–398 trên `ab457c6`,
:365–368 trên `163fd5d`). Phép khớp của `s5.py` làm bước 1, 3, 4 của PROTOCOL §5 (separator, NFC, case-fold; với mục đã qua bảng chữ thì NFC là
đồng nhất, xem dưới) và đọc cả mục ánh xạ lẫn `effective_write_set`; nó KHÔNG làm bước 2 và bước 5 theo nghĩa của dispatcher: mục tuyệt đối, có
`.`/`..` hay glob không bị từ chối mà bị coi là PHỦ, và symlink không resolve được từ nội dung lease. NFC một mình không
tạo được va chạm với hai đường dẫn ASCII của write set: duyệt mọi code point (Python 3.11.15, Unicode 14.0.0) chỉ có
U+037E, U+1FEF và U+212A chuẩn hoá NFC về ASCII (`;`, `` ` ``, `K`), và hai tên tệp không chứa ký tự nào trong số ấy,
kể cả sau case-fold. Case-fold thì có: mười ba code point mà `NFC(casefold(c))` là ASCII (mười một khi chỉ casefold;
U+037E và U+1FEF thêm qua NFC; đo 3.11.15, 3.12.3, 3.13.12), trong đó `ſ` (về `s`) và `ﬅ`, `ﬆ` (về `st`) ghép được tên
`lease_publish*`. Từ khi có bảng chữ (HINT lượt 12, giữ ở r13), mục có ký tự không-ASCII KHÔNG tới phép chuẩn hoá: nó là
không diễn giải được, tức PHỦ; nên cả mười ba code point ấy lẫn mọi dạng NFC đều PHỦ, và trong `s5.py` NFC cùng case-fold
ngoài ASCII không còn đường nào tới được. Đo (phiên soạn r13, §10): đột biến bỏ NFC cả hai lần làm đỏ 0 ca tự kiểm và
không đổi kịch bản chuỗi nào; ca `ſ` (ca 6) và ca `e` cộng dấu sắc tổ hợp U+0301 (ca 7) nay qua nhánh không diễn giải được; bỏ case-fold chỉ làm
đỏ hai ca chữ hoa ASCII (ca 4, 5). Câu của r12 *"ca NFC nằm ở tự kiểm của `s5.py`"* vì vậy không còn đúng.
Miền ref vẫn là của `ai-dang-giu`: lease trên nhánh tên có đuôi `/HEAD` làm cả ba lệnh ra `CHẶN [12]` ⇒ KXĐ (review
lượt 11 N1, fail-close; phiên soạn r12 đo lại cùng kết quả). Chuỗi không ghim đồng hồ: `ai-dang-giu` xếp hạn bằng
`datetime.now(timezone.utc)` của máy chạy, nên đồng hồ chạy nhanh làm lease còn hạn thành `HẾT_HẠN` (`KHÔNG ĐO ĐƯỢC`
từ chuỗi: không có nguồn giờ thứ hai). Phép khớp nguyên chuỗi của `ai-dang-giu` hẹp hơn PROTOCOL §5 là **phát hiện
ngoài spec**: executor ghi vào handoff để mở packet đưa phép khớp của `ai-dang-giu` về §5 (khi ấy `s5.py` thành thừa),
không vá trong write set này. Mọi phiên khác dựa vào `ai-dang-giu` để cấp lease vẫn chịu khuyết tật ấy cho tới lúc đó.
**Phát hiện ngoài spec thứ hai, cùng lớp (review lượt 12 đo; phiên soạn r13 đo lại và mở rộng).** `_quet_lease_toan_kho` liệt kê tệp lease bằng `ls-tree -r` KHÔNG `-z` rồi lọc
đuôi `.yaml`/`.yml` trên chuỗi đã qua nháy kiểu C của git: tên tệp có ký tự không-ASCII (`é`, `ệ`), nháy kép hay dấu chéo ngược, và đuôi
viết hoa (`.YAML`), làm tệp lease bị bỏ qua; lease CÒN_HẠN giữ hai tệp vẫn ra `NGƯỜI_GIỮ 0` (chạy đúng lệnh `git diff --name-only` của bước
*tìm lease vừa đổi* và vòng `read` của bước *đăng* trong `ops-publish-lease.yml` trên tên `é`: tên bị nháy, `[ -f ]` sai, `continue` im lặng, nên lease ấy cũng
không được đăng). Trên bộ thử của phiên soạn (khối r12 và `s5.py` r12 trích từ chính tệp này, `ab457c6`):
mười kịch bản tên tệp (`R1`), lease CÒN_HẠN giữ `ops/lease_publish_test.py`, r12 CẤP nhầm ở **6** (tên `é`, tên `ệ`, nháy kép, dấu chéo
ngược, thư mục con không-ASCII, đuôi `.YAML`) và KHÔNG CẤP ở 4 đối chứng (ASCII, có dấu cách, `.yml`, thư mục con ASCII); `s5.py` r12 không bù được vì
tệp bị lọc trước khi tới phép khớp. Cùng tệp đã có `_ls_tree_z` (`ops/lease_publish.py` :1977, F02) cho sổ thu hồi.
**Liệt kê hết các cửa trước khi vá** (phiên soạn r13: đọc `_quet_lease_toan_kho` :641–701 trên `ab457c6`, rồi đo từng
đường). Tệp lease đi qua năm cửa trước phép khớp: (1) đặc tả đường dẫn `ops/leases` của `ls-tree` (phân biệt hoa thường);
(2) văn bản của `ls-tree` (nháy kiểu C khi không có `-z`); (3) tách dòng bằng `str.splitlines`, sau khi `GOI_GIT` đã đổi CR
thành LF; (4) chỉ giữ mục kiểu `blob`, rồi đọc NỘI DUNG bằng `cat-file -p <oid>` lấy từ dòng; (5) lọc đuôi `.yaml`/`.yml`
phân biệt hoa thường. HINT lượt 12 đóng cửa (2) và phần hoa thường của (5) bằng `-z` cộng hạ đuôi, nhưng chính việc dựng
lại DÒNG từ đầu ra `-z` mở cửa (3): tên tệp chứa một ký tự mà `splitlines` coi là ngắt dòng, theo sau là `100644 blob <OID
của một blob khác><TAB>z2.yaml`, bị tách thành HAI dòng; dòng thật không có đuôi `.yaml` nên bị bỏ, dòng giả trỏ blob của
một lease cũ đã hết hạn. Đo trực tiếp (`do_f1a.py` ở scratch; mỗi ca một kho máy chủ riêng; lease CÒN HẠN giữ
`ops/lease_publish_test.py`; 12:12Z–12:57Z 07-10, lượt hợp nhất 33 ca 12:57:29Z–12:57:53Z, §10): công cụ nền rc=0 (tên bị nháy nên lọt như F12-1a); `s5.py` của HINT
**rc=0, `NGƯỜI_GIỮ 0`** ở cả tám ký tự ngắt dòng thử (LF, CR, VT, FF, FS, NEL, U+2028, U+2029); `s5.py` r13 rc=12. Đặt
`core.quotePath=false` với U+2028 hay NEL: công cụ nền rc=12 (git vẫn nháy TAB nên dòng giả không có TAB thật), `s5.py`
của HINT vẫn rc=0. Cùng cơ chế ở cửa (4): symlink là mục `blob` mode `120000` mà nội dung là CHUỖI ĐÍCH; liên kết
`ln.yaml` trỏ tệp `{lease_id: x}` trong cùng thư mục (tệp ấy chứa lease còn hạn, không đuôi `.yaml`) có nội dung là một
ánh xạ YAML không write set, nên công cụ nền và `s5.py` của HINT rc=0, `s5.py` r13 rc=12 (bước *đăng* của workflow thì
`[ -f ]` theo liên kết và đăng nội dung của đích); liên kết trỏ ra ngoài thư mục (nội dung là một đường dẫn) cho cả ba
rc=12 (`lease không phải ánh xạ`). Gitlink (`160000 commit`) dưới `ops/leases/` của một submodule chứa lease còn hạn: công
cụ nền và `s5.py` của HINT rc=0 (mục không phải `blob` bị bỏ), `s5.py` r13 rc=12 (nội dung ở kho khác: `KHÔNG ĐO ĐƯỢC`).
Tên nhánh chứa U+2028 hay NEL: cả ba rc=12 (`ls-remote có dòng hỏng`). Vì vậy `s5.py` r13 thêm hai chốt theo danh sách
CHO PHÉP vào `bao_goi_git`: dòng dựng lại phải là đúng MỘT dòng dưới chính `str.splitlines` mà `_quet_lease_toan_kho` dùng
(đo hiệu ứng lên bộ tách, không liệt kê ký tự), và mục phải là `blob` mode `100644` hay `100755`; sai thì lệnh liệt kê trả
rc=1 và `ai-dang-giu` ra 12. Đo cả mười một dạng tên tệp của review lượt 12 trên `s5.py` r13: rc=11 ở chín dạng (hai
đối chứng ASCII và có dấu cách, cùng `é`, `ệ` (R1), nháy kép, dấu chéo ngược, TAB, `.YAML`, `.Yml`); rc=12 ở tên có LF trần; rc=1 (`UnicodeDecodeError`) ở tên không phải
UTF-8, tức `KHÔNG_XÁC_ĐỊNH` theo chuỗi; không dạng nào ra rc=0. Đo trên `adg2` (473 ref, 12:17Z 07-10): dưới
`ops/leases/` 0 mục không phải blob, 0 symlink, 0 tên có ký tự ngắt dòng, 0 tên ngoài bảng chữ, 0 đuôi viết hoa, và cả
37081 mục cây (đếm lặp qua các ref; 13:17Z) đều `100644 blob`; nên hai chốt không chặn gì lúc đo. **Miền tệp: giới hạn được khai, không đóng.** Tệp ngoài `ops/leases/` (kể cả thư mục khác hoa
thường như `ops/Leases/`), hay có đuôi khác `.yaml`/`.yml` sau khi hạ chữ thường (`x.yaml ` có dấu cách cuối,
`x.yaml.nhap`), không được `ai-dang-giu` đọc; đo trực tiếp: công cụ nền, `s5.py` của HINT và `s5.py` r13 cùng rc=0 ở ba ca
ấy. Đó cũng là miền của workflow đăng (`git diff --name-only … -- 'ops/leases/*.yaml' 'ops/leases/*.yml'`, đặc tả đường
dẫn phân biệt hoa thường), nên tệp ngoài miền không được đăng; PROTOCOL không định nghĩa chỗ đặt tệp lease (`grep` 0 dòng
`ops/leases` trong `docs/PROTOCOL_DA_PHIEN.md` ở `ab457c6`). Trên `adg2`: 0 đường dẫn khác hoa thường với `ops/leases/`;
4 tên `.yaml.nhap` (bản nháp lease, có mặt trên 286 đến 296 ref); 299 cặp YAML ngoài `ops/leases/` có khoá `lease_id`, cả
299 là biên nhận dưới `ops/reviews/`, 0 cặp có `write_set`, `effective_write_set` hay `lease_expires_at_utc`. Trên bộ thử
chuỗi (§10), `s5.py` r13 cho cả mười hàng R1 KHÔNG CẤP và giữ nguyên kết quả của 63 kịch bản cũ. Sửa `_quet_lease_toan_kho`
là phát hiện ngoài spec như phép khớp nguyên chuỗi: executor ghi vào handoff, không vá trong write set này.

**Closure đóng băng** (các trường dispatcher dẫn xuất, protocol §3.2). Kho chưa có dispatcher
sinh chúng và chưa có policy canonical cho closure; khối này do phiên điều phối điền tay theo
**miễn trừ có phạm vi** ghi ở Mission Issue #682: chỉ `wp678`, mọi revision từ r3, hết hiệu lực
ở lần đầu một policy canonical cho closure xuất hiện trên nhánh mặc định; đổi bất kỳ giá trị
closure ⇒ revision mới, `spec_hash` mới, lease mới; write set không mở rộng.
**Miễn trừ vẫn áp cho r13.** Thân #682 đọc qua REST `GET /repos/ducthangho/tra-luat/issues/682` (`gh api` của phiên
soạn r13, 12:35:55Z 07-10, rc=0; `updated_at` `2026-10-01T09:44:15Z`; sha256 thân UTF-8
`76bee6fb159ffb5a8c9cbd74896dd5793443457b5f0ebf6a284eb3350e2e0dd2`, 3416 byte, 0 thực thể HTML, bằng đúng băm r12 đo lúc
08:36:26Z 07-10, r8 lúc 01:08:54Z, r9 lúc 05:22Z, r10 lúc 09:31:01Z và r11 lúc 11:29:48Z 01-10); hai dòng dưới chép từng byte từ dòng 29 và 31 của thân ấy (bỏ gạch đầu dòng):
  > Áp cho **packet `wp678` duy nhất**, mọi revision kể từ r3.
  >
  > Đổi bất kỳ giá trị nào ở bảng trên ⇒ revision mới, `spec_hash` mới, lease mới.

Bảng trên #682 còn ghi vế cross-review codex của r3; r7 đổi đúng vế ấy theo Q10 bằng revision mới, đúng luật của miễn
trừ; r8 **không** đổi giá trị closure nào (chỉ thêm ghi chú kiểm ngoài bảng); r9 đổi hai giá trị (vế review của
`required_checks`, `land_obligations`) theo Q12, bằng revision mới, đúng luật của miễn trừ; r10, r11, r12, r13, r14 và r15 **không** đổi giá trị closure nào (chỉ sửa ghi chú kiểm ngoài bảng; r12 thêm ghi chú về luật danh tính
của wp709); write set không mở rộng.
**Hiệu lực của miễn trừ đo bằng danh sách đúng hai đường dẫn** (từ r11), chạy cả lúc cấp (cùng clone và `T`, ngay
sau chuỗi lệnh đo điều kiện cấp) lẫn lúc land:

```
git ls-tree -r --name-only refs/remotes/origin/master -- .github/coordination/ > "$T/coord"   # rc=0, ít nhất 1 dòng
grep -c -x -F -e .github/coordination/change-impact.v1.json -e .github/coordination/schemas/change-impact.v1.schema.json "$T/coord" > "$T/coord.khop"   # nội dung đúng `0` (rc=1 của grep -c nghĩa là 0 dòng khớp)
git grep -c -F .github/coordination/change-impact.v1.json refs/remotes/origin/master -- docs/PROTOCOL_DA_PHIEN.md ops/lease_publish.py > "$T/coord.neo"   # rc=0, đúng 2 dòng
```

Hai đường dẫn ấy là đúng hai đường dẫn PROTOCOL :306–307 trên `ab457c6` (:276–277 trên `163fd5d`) đặt cho
change-impact policy và schema của nó; `ops/lease_publish.py` :1256 trên `ab457c6` (:1096 trên `163fd5d`;
`PATH_POLICY_CLOSURE`) trỏ cùng đường dẫn thứ nhất. `coord.khop` khác `0` ⇒ policy
canonical đã có ⇒ miễn trừ hết hiệu lực ⇒ không cấp, không land theo revision này. `coord` rỗng, rc ngoài mức nêu,
hay `coord.neo` khác 2 dòng (PROTOCOL hoặc `ops/lease_publish.py` đã đổi chỗ đặt policy) ⇒ `KHÔNG_XÁC_ĐỊNH` ⇒ không
cấp, không land. Phiên soạn r13 đo (12:36:17Z 07-10, `adg2`, cùng ba lệnh, `LC_ALL=C GIT_NO_REPLACE_OBJECTS=1`) ở
`refs/remotes/origin/master` (`ab457c6`): `ls-tree` rc=0, 4 dòng (cùng bốn tệp kể dưới), `coord.khop` `0` (grep rc=1),
`coord.neo` 2 dòng, mỗi tệp 1 (rc=0); cùng kết quả với r12. Phiên soạn r12 đo (09:00:29Z 07-10, `adg2`, cùng ba lệnh, `LC_ALL=C GIT_NO_REPLACE_OBJECTS=1`) ở
`ab457c6` và ở `refs/remotes/origin/master` (cũng là `ab457c6`): `ls-tree` rc=0, 4 dòng (cùng bốn tệp kể dưới),
`coord.khop` `0` (grep rc=1), `coord.neo` 2 dòng, mỗi tệp 1 (rc=0); tức chưa có policy canonical, bằng bằng chứng
dương. Phiên soạn r11 đo (11:3xZ 01-10, `adg2`, cùng ba lệnh, rev thay cho `refs/remotes/origin/master`) ở
`89fc4fa`, `20ec8d5`, `163fd5d`, `a6de9d1` và `refs/remotes/origin/master` (`7e5958e`): `ls-tree` rc=0, 4 dòng
(`f2-d-groupb-recovery.md`, `f2-d-worktree-recovery.md`, `f2-d-writer-inventory.md`,
`schemas/review_verdict.v1.schema.json` dưới `.github/coordination/`), khớp `0`, mỗi tệp neo 1 dòng; tức chưa có
policy canonical, bằng bằng chứng dương. Review lượt 10 đo cùng kết luận bằng `git cat-file -e` (rc khác 0 ở năm
mốc); rc khác 0 của `cat-file -e` không tách "vắng" khỏi "không đọc được cây hay ref", nên r11 so trên danh sách của
một cây đã đọc được. Phép lọc lịch sử dưới đây (r7–r10) chỉ còn là hồ sơ, không phải phép đo hiệu lực: nó KHÔNG thấy
được hai đường dẫn ấy vì tên không chứa `polic`, `closure` hay `dispatcher`. Phép lọc lịch sử: trong 128 tệp
đổi `89fc4fa..20ec8d5` không tên nào chứa `polic`, `closure`, `dispatcher`; 16 dòng thêm nhắc `change_policy`, `policy
canonical` hoặc `closure policy` đều thuộc hồ sơ wp678 (spec r2–r6, verdict lượt 3, 4, 6), và `423b4ba..20ec8d5` thêm 0
dòng như thế (lọc theo tên và chuỗi, không chứng minh vắng mặt). Lịch sử: r7 đọc #682 qua REST lúc 12:33Z 30-09 và lọc 61
tệp `89fc4fa..423b4ba`. r9: `origin/master` vẫn là `20ec8d5` (05:17:33Z 01-10), nên không có tệp đổi nào ngoài
phạm vi lọc của r8. r10: 7 tệp đổi `20ec8d5..163fd5d` (nền mới) và 118 tệp `163fd5d..a6de9d1` (`origin/master` lúc đo cuối):
cả hai không tên nào chứa `polic`, `closure`, `dispatcher`, và 0 dòng thêm nhắc ba cụm trên (cùng phép lọc, 09:2xZ–09:56Z
01-10).

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
audit; Q12 chọn `human_audited`). Số dòng PROTOCOL trong ghi chú này là trên `163fd5d`; trên `ab457c6` chúng là
:725–726, :696, :706–707, :607–608, :702 (cùng nội dung).

**Ghi chú về cách kiểm vế review của `required_checks`** (viết lại ở r9 theo Q12; mục (a) sửa ở r10 theo review lượt 9;
không phải giá trị closure).
`claude-opus-5-5` và `effort max` trong vế ấy là CẤU HÌNH giao cho subagent, không phải runtime evidence (PROTOCOL
:710–711). Vế review **đạt** khi và chỉ khi biên nhận của lượt có đủ bốn điều:
(a) **mức, chế độ và cổng biên nhận**: `assurance: review_deferred`, `model_reviewer_identity.che_do:
subagent_trong_phien_dieu_phoi`, và biên nhận qua `ops/bien_nhan_v2.py` ở cả hai tầng: `_thieu` trả **0** lỗi, **và**
trên cây chứa biên nhận ở `ops/reviews/` (cây đủ lịch sử để tra `reviewed_sha` và commit trong `evidence_url`)
`kiem()` không có mục vi phạm nào mang tên tệp biên nhận, còn CLI `python ops/bien_nhan_v2.py` không in mục
`KHÔNG ĐO ĐƯỢC` nào mang tên tệp ấy hay áp cho cả lượt (nguồn từ vựng provider hỏng). `kiem()` là thứ CI chạy: job
`gate-ops` gọi `python ops/bien_nhan_v2_test.py` (`.github/workflows/ci.yml` :590 trên `163fd5d`, :670 trên
`7e5958e` và `ab457c6`), ca `c1` (:345–350) chạy `kiem()`
trên kho thật và đòi 0 vi phạm nhưng không đếm `chua_do`; CLI trả rc=2 khi có `KHÔNG ĐO ĐƯỢC` (`ops/bien_nhan_v2.py`
:1043–1065). Vì vậy `_thieu` 0 lỗi là điều kiện CẦN, không đủ; bộ đếm `ĐẠT v2` của `kiem()` cũng không đủ, vì
`kiem()` đếm ĐẠT theo vi phạm mà không xét `chua_do` (:994–1000). Review lượt 9 đo (05:41:48Z 01-10) một biên nhận
mẫu `_thieu` 0 lỗi mà `evidence_url` là URL PR với `anchor.loai: canonical_ancestry` ⇒ `kiem()` 1 vi phạm, còn bản neo
blob đúng ⇒ 0. Phiên soạn r10 tái lập và đo thêm trên nền mới (09:55:49Z 01-10; cây `git archive 163fd5d` đủ,
`PROVIDER_NGUON_HONG` là `None`; lần đầu 09:25:54Z trên cây `20ec8d5`, cùng mọi kết quả dưới; mỗi mẫu một kho git tạm có verdict và biên nhận đã commit; script ở scratch, không vào kho): mẫu neo blob
đúng ⇒ `_thieu` 0, `kiem()` 0 vi phạm và 0 `KHÔNG ĐO ĐƯỢC`, CLI rc=0; mẫu URL PR ⇒ `_thieu` 0, `kiem()` 1 vi phạm
(*"khai `anchor.loai: canonical_ancestry` nhưng `evidence_url` KHÔNG phải URL blob ghim commit"*), CLI rc=1; mẫu neo
blob đúng mà `reviewed_sha` không có trong kho ⇒ `_thieu` 0, `kiem()` 0 vi phạm, `ĐẠT v2` 1, nhưng **1** mục `KHÔNG ĐO
ĐƯỢC` mang tên tệp, CLI rc=2. Cùng script trên cây archive `20ec8d5` thiếu `.claude/dev/launcher.py` hay `AGENTS.md` ⇒
`PROVIDER_NGUON_HONG` khác `None`, CLI rc=2 kể cả với mẫu đúng: phép kiểm này phải chạy trên cây đủ. CLI trên kho thật
ở `163fd5d` (clone sạch, 09:56:17Z; cùng kết quả lúc 09:25:31Z): rc=0, *"163 ĐẠT v2 · 11/11 miễn trừ legacy
(băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 216"*; ở `a6de9d1` (`adg2`, 09:56Z): rc=0, *"174
ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 227"*. Review lượt 10 không đo được vế *"0 KHÔNG ĐO ĐƯỢC"* ở `a6de9d1` (mirror của họ thiếu commit `4bc9432` mà một biên nhận neo); phiên soạn r11 đo lại trên một bản sao lấy cả 457 ref theo dõi của `adg2` (`4bc9432` có mặt), `python3.12`: ở `a6de9d1` (11:33:51Z) và ở `7e5958e` (11:34:09Z) cùng dòng trên, rc=0. Phiên soạn r12 đo lại trên nền `ab457c6`
(`ops/bien_nhan_v2.py` giống hệt, sha256 `38cda51c…`; script `bn10.py` của review lượt 10 chép nguyên byte, sha256
`0d073c79…b7f1`, clone đầy đủ `ab457c6`, `python3.12`, 08:58:51Z 07-10): ba mẫu kho tạm ⇒ `_thieu` 0, 0, 0; `kiem()`
0, 1, 0 vi phạm và 0, 0, 1 `KHÔNG ĐO ĐƯỢC`; CLI rc 0, 1, 2; CLI trên kho thật ở `ab457c6` (`adg2`, 471 ref theo dõi
gồm `origin/HEAD`, 08:58:52Z): rc=0, *"186 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm ·
0 KHÔNG ĐO ĐƯỢC · tổng 239"*. Phiên soạn r13 chạy lại CLI ấy trên kho thật ở `ab457c6` (`adg2`, 473 ref theo dõi gồm
`origin/HEAD`, `ops/bien_nhan_v2.py` sha256 `38cda51c…`, python3.12, 12:38:24Z–12:38:34Z 07-10): rc=0, cùng dòng trên; r13
không đo lại ba mẫu kho tạm (nền và `ops/bien_nhan_v2.py` không đổi). Phiên soạn r9 đo `_thieu` (05:18:49Z
01-10, `ops/bien_nhan_v2.py` của
`20ec8d5`, sha256 `38cda51c9b46fb0b9ede91a63d89902c0c1b0faaca52d65e07c7ed31a5badefc`; script ở scratch, không vào kho):
biên nhận tiền lệ `phan-bien-quy-trinh-review-2` nguyên byte ⇒ 0 lỗi; một biên nhận mẫu dựng từ nó cho `wp678`
(`model_reviewer_identity.provider: anthropic`, `che_do` như trên, `review_deferred`) ⇒ **0** lỗi; cùng mẫu đổi sang
`same_provider_approved` ⇒ 1 lỗi (*"tự khai chạy trong phiên điều phối"*); đổi sang `human_audited` ⇒ 2 lỗi; bỏ
`che_do`, thêm `session_run_id: 'x'` rồi khai `same_provider_approved` ⇒ 0 lỗi (nên `che_do` là nghĩa vụ khai, không
phải chốt máy). Phiên soạn r10 đo lại năm số ấy trên `ops/bien_nhan_v2.py` của `163fd5d` (cùng sha256, 09:56:05Z):
0, 0, 1, 2, 0. Phiên soạn r12 đo lại trên `ab457c6` (cùng sha256, 08:58:51Z 07-10): 0, 0, 1, 2, 0.
(b) **model và effort**: biên nhận ghi `claude-opus-5-5` và `max` là cấu hình yêu cầu, và ghi model/effort đã phục vụ
là `KHONG_do_duoc`. Không nâng lời khai này lên, và không ghi `modelUsage` hay `session_run_id` cho một lượt không
sinh ra chúng.
(c) **định nghĩa**: sha256 của `~/.claude/agents/review-opus-max.md` lúc giao việc bằng
`e225b81cf2fbdd0f05a54a689cac17db8972b2f8c0684a0a30931875cd4b792c` (1175 byte; đo 12:33Z 30-09 và 01:14:09Z 01-10;
phiên soạn r9 đo lại 05:18:56Z 01-10, phiên soạn r12 đo lại 09:39:49Z 07-10, phiên soạn r13 đo lại 12:36:10Z 07-10, phiên soạn r14 đo lại 15:17:55Z 07-10, phiên soạn r15 đo lại 17:18:57Z 07-10, cùng băm, frontmatter `model:
claude-opus-5-5`, `effort: max`). Băm này ghim CẤU HÌNH mà
phiên điều phối giao; nó **không** là nguồn đo runtime, không chứng minh định nghĩa đã được nạp hay model ấy đã phục
vụ. Thiếu hoặc lệch ⇒ **không** đạt; đổi định nghĩa ⇒ revision mới.
(d) **kết luận**: sha256 VERDICT và HINT; VERDICT 0 P1/P2/P3 theo lớp trên exact `reviewed_sha`.
Đạt bốn điều này là có một lượt review ở mức `review_deferred`, **không** phải thẩm quyền land: land vẫn đòi
`human_audited` (ghi chú gate land ở trên). Không có đường lùi nào phải canh: Q12 bỏ đường `claude -p`, nên không còn
nhánh "launcher chặn thì dừng hỏi chủ kho" của r8.

**Ghi chú về hợp đồng lease với luật danh tính của wp709** (mới ở r12; không phải giá trị closure). Từ `ab457c6`,
`kiem()` của cổng đăng gọi `_kiem_provider_identity` (`ops/lease_publish.py` :136, lời gọi ở :984) ngay sau phép kiểm
trường bắt buộc: `provider` hay `executor` khai rỗng ⇒ rc=8; lease `role: executor` mà `executor` khác `provider` ⇒
rc=8; `assurance_target` chứa `cross_approved` mà reviewer cùng provider hay cùng họ model với executor ⇒ rc=10. Phiên
soạn r12 đo (09:0xZ 07-10, Python 3.12.3, script `do_kiem.py` ở scratch, không vào kho; `kiem(bo_qua_han=True)` trên lease
tiền lệ claude-executor của #704, `no-ton-677-687-r1-g1-claude.yaml` trên `refs/remotes/origin/claude/no-ton-677-687`, bỏ
các trường `prompt_*` như A1, rồi đổi sang các trường dạng `wp678`; cùng lệnh với `ops/lease_publish.py` của `163fd5d` để
so): tiền lệ nguyên văn (`provider: anthropic_claude`, `executor: claude`, `role: executor`, `assurance_target:
human_audited`) và bản đổi `packet_issue`, `packet_id`, `lease_id`, `write_set` sang `wp678` ⇒ qua ở cả hai nền;
`provider: claude` cùng `reviewer: claude` với `human_audited` hay `review_deferred` ⇒ qua; `reviewer: human` với
`human_audited` ⇒ qua; bỏ hẳn `provider`, `role`, `assurance_target` ⇒ qua (legacy); `assurance_target: cross_approved`
hay `cross_approved_or_human_audited` với `reviewer: claude` ⇒ **rc=10** trên `ab457c6`, qua trên `163fd5d`;
`provider: ' '` ⇒ rc=8 trên `ab457c6`; `executor: codex` mà `provider: claude` ⇒ rc=8 trên `ab457c6`. Vì vậy lease
`wp678` (executor `claude`; review mức `review_deferred` bằng subagent cùng họ; land bằng `human_audited`) **không** được
khai `assurance_target` chứa `cross_approved`; khai `human_audited` (đúng gate land) hoặc bỏ trường. Đây là luật của
cổng, closure không đổi. `ops/bien_nhan_v2.py` không đổi ở wp709 (blob giống hệt), nên mục (a) của ghi chú trên giữ
nguyên. Lược đồ PROTOCOL mới (lease :249–264, lease reviewer :266–272, evidence reviewer :516–520 trên `ab457c6`) thêm
`role`, `provider`, `model_family`, `execution_surface`, `transport`, bắt buộc cho `google_antigravity`; Claude Code giữ
danh tính cũ, họ `claude` (:3–13).

**Descriptor nguồn closure** = `{mission_issue: 682, object_id: 5627190292}`. Closure do phiên
điều phối điền tay theo miễn trừ ấy, **không** do executor tự khai. Lease phải **chép** đúng các
giá trị trên, không được thêm hay đổi; lệch ⇒ **DỪNG**. Băm thân Issue ở phía nhận là
**KHÔNG ĐO ĐƯỢC** từ phiên soạn r6 (đường đọc MCP chuẩn hoá thực thể HTML trong thân issue, xem
CLAUDE.md), nên descriptor neo bằng object ID + số Issue, không bằng băm thân. Phiên soạn r8, r9, r10, r11, r12 và r13 đọc được thân qua REST
và ghi băm ở đoạn miễn trừ trên (cùng một băm), như phép đo tại từng thời điểm; descriptor **không** đổi thành băm thân.

**GIỚI HẠN LỜI KHAI:** mọi khẳng định chỉ chứng minh tới đúng phép đo ghi kèm.
**Ba trạng thái:** có · không · **KHÔNG ĐO ĐƯỢC**.

**Tọa độ trên nền mới** (từ r12). Số dòng mà các mục kế thừa của đặc tả trích là trên nền ghi kèm, mặc định `163fd5d`
(blob `ops/lease_publish.py` ở đó giống hệt `1741e0a`, `89fc4fa`, `20ec8d5`; PROTOCOL giống hệt `423b4ba`, `20ec8d5`). Trên
`ab457c6`, cùng nội dung từng dòng nằm ở các tọa độ dưới (đo 07-10: `grep -n` trên hai blob của `ops/lease_publish.py`;
`difflib.SequenceMatcher` theo dòng cho PROTOCOL). `ops/lease_publish.py`: dòng L giữ nguyên khi L ≤ 88, thành L + 159
khi 90 ≤ L ≤ 824, thành L + 160 khi L ≥ 825 (dòng 89 cũ, `PROVIDERS = ("claude", "codex")`, được thay bằng khối danh
tính của wp709; một dòng thêm sau :824); ví dụ `_khop_tien_to` :140 → :299, `_ten_nhanh_may_chu` :300–309 → :459–468,
`_cac_ref_cuc_bo` :312–324 → :471–483, `_lease_cham_duong` :545–549 → :704–708, `PATH_POLICY_CLOSURE` :1096 → :1256,
nhánh bia mộ một chiều của `ai-dang-giu` :2111–2118 → :2271–2278. `docs/PROTOCOL_DA_PHIEN.md`: :255–259 → :285–289,
:267 → :297, :269–273 → :299–303, :276–277 → :306–307, :299 → :329, :365–368 → :395–398, :562–568 → :606–612, :636 →
:680, :652 → :696, :658 → :702, :662–663 → :706–707, :681–682 → :725–726, :710–716 → :754–760, :1043–1049 → :1087–1093,
:1054–1056 → :1098–1100. Tọa độ của `ops/lease_publish_test.py` và `.github/workflows/ci.yml` trên `ab457c6` ghi ngay tại
§4, A2, A8; tọa độ D1–D9 ở §2.

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
`grep -n lease_id ops/lease_publish.py` (38 dòng trên `ab457c6`, gồm chú thích và dòng dùng biến; lệnh của r12 (mẫu `"lease_id"` cộng mẫu chỉ số trong ngoặc vuông) chỉ ra 19 dòng, riêng mẫu `"lease_id"` ra 16, và BỎ SÓT
`.get('lease_id')` ở :2106 cùng `lease_id` gán ra biến ở :2283), không phải bằng trí nhớ.

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

Trên `ab457c6` (wp709) mọi dòng ấy giữ nguyên nội dung và dời: D1 :1021, D2 :1109, D3 :827, D4 :1230, D5 :746/:751,
D6 :768/:771, D7 :2270/:2283, D8 :2098/:2102/:2106 và :2127, D9 :2234/:2249 và :2299/:2303, `kiem_ban_ghi_thu_hoi`
:1352 (đo 07-10, chính lệnh `grep` trên chạy trên blob `93cff2f`). `kiem()` của nền ấy gọi thêm
`_kiem_provider_identity(lease)` ở :984, TRƯỚC D1 (A1; ghi chú dưới closure).

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
  subagent trong phiên điều phối (như lượt 7, 8 và 9) được tính cho (3) khi VERDICT sạch trên exact `reviewed_sha` và
  biên nhận tự khai `che_do: subagent_trong_phien_dieu_phoi`, mức `review_deferred`, đạt cổng biên nhận như mục (a) của
  ghi chú dưới closure (`_thieu`, `kiem()` và CLI; từ r10); model/effort của lượt ấy là CẤU
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
- **Q13 — Review Rescue Checkpoint sau review lượt 9: áp HINT, lặp không trần** (chủ kho, trắc nghiệm
  `AskUserQuestion` trong phiên điều phối, 01-10-2026, sau review lượt 9 và bản chiếu #678 comment `5925743728`). Neo:
  https://github.com/ducthangho/tra-luat/issues/682#issuecomment-5928886724, id `5928886724`, tạo
  `2026-10-01T09:44:15Z`, **phiên điều phối đăng** qua app `claude`, nên `author_association: OWNER` không chứng minh chủ
  kho tự gõ. Comment ấy là **bản chiếu lời khai của phiên điều phối**, đăng sau quyết định, và tự ghi *"Kho không có
  hiện vật nào đo được câu trả lời này"*. Đọc qua REST `GET /repos/ducthangho/tra-luat/issues/comments/5928886724`
  (HTTP 200, 09:46:46Z 01-10, không token), sha256 thân UTF-8
  `5f1ff74e41b4ff4ef7a8367730bf43c913f12985e62f59605a3d180a7bec0878`, 1662 byte, 16 dòng, 0 thực thể HTML; các dòng 5,
  7–9, 11 và 13 của thân chép từng byte dưới đây (dòng 5 và ba mô tả nhãn cũng khớp từng byte văn bản mà phiên điều
  phối giao cho phiên soạn r10):
  > **Câu hỏi (header "wp678 §12"):** wp678 chạm điều kiện dừng §12: hai chuyển tiếp liên tiếp vá thật dưới 50% (7→8: 0/5; 8→9: 2/7). Lượt 9 còn 2 P2: (1) điều kiện cấp/dời nền so tập TÊN ref nên không bắt ref đệm cũ — cần so TÊN+OID (bài học đã có trong CLAUDE.md); (2) nghĩa vụ cập nhật t70 mô tả sai vị từ (helper gọi trong hàm lồng/lambda/comprehension). Cả hai có cách sửa đo được trong HINT. Checkpoint quyết:
  >
  > - [ ] **Thu hẹp rồi lặp tiếp (Recommended)** — r10 = HINT lượt 9 + THU HẸP: điều kiện cấp đọc thẳng một lệnh đo chuẩn (so tên+OID rồi ai-dang-giu), bỏ lời văn tự do; ép ca A3/A2 gọi helper ở cấp đỉnh để t70 đo đúng. Thêm tối đa 1 lượt review; còn P1/P2 thì dừng hẳn.
  > - [x] **Áp HINT, lặp không trần** — Bỏ qua điều kiện dừng §12, lặp tới 0/0/0 như #688.
  > - [ ] **Tạm dừng wp678** — Đóng băng ở r9; mở lại khi codex có quota (03-10 18:31) để cross-review độc lập.
  >
  > **Trả lời của chủ kho:** "Áp HINT, lặp không trần".
  >
  > **Lưu ý:** đây là lời khai của phiên điều phối. Kho không có hiện vật nào đo được câu trả lời này.

  Áp vào r10 (việc của phiên soạn r10, không phải lời chủ kho): áp cả HINT lượt 9, rồi sửa thêm những chỗ mà phép đo
  của phiên soạn r10 cho thấy HINT chưa đủ (§9). Theo mô tả kèm, Q13 bỏ qua điều kiện dừng của §12 (điểm dừng theo tỷ lệ
  :1047–1048 đã kích hoạt ở 8→9, §9) cho chuỗi review đặc tả `wp678`; r10 đọc *"0/0/0"* là một lượt review cho 0 P1 / 0 P2
  / 0 P3. Q13 không nói gì về mục tiêu, write set, nền nghiệm thu, giá trị closure, năm điều kiện cấp hay gate land, nên
  r10 giữ nguyên chúng; việc dời nền ở r10 đến từ điều kiện (4), không từ Q13. Theo §12 :1055–1056, revision mới không
  reset lịch sử lớp: bộ đếm hình dạng ở §9 tiếp tục từ lượt 9.

  Áp vào r11 (việc của phiên soạn r11, không phải lời chủ kho): Q13 vẫn áp cho chuỗi review đặc tả `wp678`, nên tỷ lệ
  chuyển tiếp 9→10 mà review lượt 10 báo (1/4 đọc chặt; 2/4 nếu tách F10-6) là số báo cáo, không phải điểm dừng (§9).
  r11 áp cả HINT lượt 10 rồi sửa thêm theo phép đo của chính phiên soạn r11; mục tiêu, write set, nền nghiệm thu, giá
  trị closure, nội dung năm điều kiện cấp và gate land giữ nguyên.

  Áp vào r12 (việc của phiên soạn r12, không phải lời chủ kho): Q13 vẫn áp cho chuỗi review đặc tả `wp678`, nên tỷ lệ
  chuyển tiếp 10→11 mà review lượt 11 báo (2/4 = 50%) là số báo cáo, không phải điểm dừng (§9). r12 áp cả HINT lượt 11
  rồi sửa thêm theo phép đo của chính phiên soạn r12; mục tiêu, write set, giá trị closure, nội dung năm điều kiện cấp
  và gate land giữ nguyên. Việc dời nền ở r12 đến từ điều kiện (4) (wp709 land, PR #712), không từ Q13.

  Áp vào r13 (việc của phiên soạn r13, không phải lời chủ kho): Q13 vẫn áp cho chuỗi review đặc tả `wp678`, nên tỷ lệ
  chuyển tiếp 11→12 mà review lượt 12 báo (0/2 = 0% theo lớp, 5/5 theo finding) là số báo cáo, không phải điểm dừng (§9).
  r13 áp cả HINT lượt 12 rồi sửa thêm theo phép đo của chính phiên soạn r13; mục tiêu, write set, nền nghiệm thu, giá trị
  closure, nội dung năm điều kiện cấp (riêng (1) đo bằng `s5.py` r13, chặt hơn) và gate land giữ nguyên.

  Áp vào r14 (việc của phiên soạn r14, không phải lời chủ kho): Q13 vẫn áp, nên tỷ lệ chuyển tiếp 12→13 mà review lượt 13
  báo (1/3 = 33% theo lớp, 9/9 theo finding) là số báo cáo, không phải điểm dừng (§9). r14 áp HINT lượt 13 rồi sửa thêm theo
  phép đo của chính phiên soạn r14; mục tiêu, write set, nền nghiệm thu, giá trị closure, nội dung năm điều kiện cấp, chuỗi
  lệnh, `s5.py` và gate land giữ nguyên.

  Áp vào r15 (việc của phiên soạn r15, không phải lời chủ kho): Q13 vẫn áp, nên tỷ lệ chuyển tiếp 13→14 mà review lượt 14
  báo (1/2 = 50% theo lớp, 3/4 theo finding) là số báo cáo, không phải điểm dừng (§9). r15 áp HINT lượt 14 rồi sửa thêm theo
  phép đo của chính phiên soạn r15; mục tiêu, write set, nền nghiệm thu, giá trị closure, nội dung năm điều kiện cấp, chuỗi
  lệnh, `s5.py` và gate land giữ nguyên.

## 4. `write_set`

- `ops/lease_publish.py`
- `ops/lease_publish_test.py`

Không đường dẫn nào khác. Riêng đặc tả này (`ops/specs/lease-id-ep-kieu-yaml-r15.md`, và các bản r1–r14 nó thay) là hồ sơ
của lượt soạn spec, **không** thuộc write set của lượt thi hành.

Trong `ops/lease_publish_test.py` có ca của packet khác mà lượt thi hành phải giữ xanh (A8), và **hai** chốt kiểm kê
mà chính việc của packet này có thể buộc phải sửa: `t70` (của #677) và `t193` (của #687). Tọa độ trên nền `ab457c6`; trên `163fd5d` ghi sau dấu chấm phẩy khi khác (thân mọi hàm dưới giống hệt giữa hai nền, so `ast`).

**`t70`** (`@ca` :3397, thân :3398–3412; :3039, :3040–3054). **Vị từ thật, đọc từ mã:** `_ca_doc_than_buoc` (:3393–3394; :3035–3036) giữ những hàm
trong `CA` (danh sách mọi ca `@ca`) có `_chay_buoc_dang` hoặc `_chay_buoc_dang_that` trong `fn.__code__.co_names`, tức
tên ấy xuất hiện như một định danh (không phải chuỗi hay chú thích) trong code object **cấp đỉnh** của chính hàm ca.
`t70` đạt khi và chỉ khi ba vế cùng đúng (:3410–3411; :3052–3053): `not ly_do`; `sorted(x.split("_")[0] for x in doc_than) ==
sorted(mong)`, tức đa tập **tiền tố** tên ca (`t51`, `t195`, …) bằng đúng literal `mong` (13 phần tử, :3409; :3051); và
`_ca_doc_than_buoc([_a, _b, _c]) == ["_a", "_b"]`, với `_a`, `_b`, `_c` là ba hàm giả lồng trong `t70` (:3406–3408; :3048–3050).
Vị từ ấy KHÔNG đo *gọi*: phiên soạn r10 đo (A2) rằng tham chiếu chỉ nằm trong hàm lồng, lambda hay generator expression
không được tính ở Python 3.11, 3.12 lẫn 3.13 (chính `t70` dựa vào điều ấy: `_a`/`_b` tham chiếu helper mà `t70` không
thuộc `mong`); tham chiếu chỉ nằm trong list, set hay dict comprehension được tính ở 3.12 và 3.13 mà không ở 3.11; nhắc trong
chú thích, docstring hay chuỗi không được tính ở bản nào; gọi qua một hàm bọc cấp module cũng không được tính.

**`t193`** (`@ca` :10973, thân :10974–11104; :10613, :10614–10744; thêm bởi #687). Sổ `SO_BO_QUA` (:569–575 ở cả hai nền, 12 tên) là danh sách ca ĐƯỢC
bỏ qua khi nền là `nt`, mỗi tên kèm cặp `(WORKFLOW_DANG, "dang")`. `t193` lấy ứng viên bằng `_ca_ung_vien_gian_tiep(CA)`
(:3415–3431; :3057–3073: như vị từ của `t70` nhưng đi tiếp qua các hàm cấp module mà ca tham chiếu), CHẠY THẬT từng ứng viên dưới nền
`nt` mô phỏng, và đòi: tập ca ỨNG VIÊN thật sự ném `BoQuaNen` bằng đúng `SO_BO_QUA`, đúng cặp (ca ngoài ứng viên không được chạy); tiền tố của sổ bằng một literal
riêng (:11009–11010; :10649–10650, 12 tiền tố, không có `t199` vì `t199` tự bắt `BoQuaNen`); và với từng ca ấy, `main()` dưới nền `nt`
ĐỎ khi thiếu tên trong sổ, BỎ QUA khi đủ sổ. Hai helper ném `BoQuaNen(WORKFLOW_DANG, "dang")` ở guard nền, trước mọi I/O, khi nền
là `nt` (`_chay_buoc_dang` :3114–3115; :2756–2757; sau hai `import` và hai phép chuẩn hoá `guard_hong`; `_chay_buoc_dang_that` :11229–11230; :10869–10870; câu lệnh đầu sau docstring), nên một ca GỌI helper mà không tự bắt `BoQuaNen` thì ném. Dưới nền `posix` các ca ấy chạy
thật; dưới nền `nt` thì `main()` chỉ BỎ QUA ca có trong sổ và ĐỎ ca ném mà ngoài sổ, đúng thứ `t193` mô phỏng (vế M3). Với ứng viên, `t193` chỉ ghi nhận kết cục `BoQuaNen`; ca ném ngoại lệ khác dưới
`nt` bị bỏ qua (`nem_nt`, nhánh `except Exception: pass`), nên `t193` xanh với một ca mà `main()` dưới `nt` ĐỎ vì
ngoại lệ khác (phiên soạn r11 đo, §10).
CI chạy suite bằng 3.12 (`gate-ops`, `.github/workflows/ci.yml` :574, chạy ở :630 trên `163fd5d`; :628 và :711 trên
`7e5958e` và `ab457c6`); `python` mặc định của container phiên soạn r10, r11 và r12 là 3.11.15. wp709 thêm ba ca
`t01_*` (không tham chiếu helper; D, G, sổ và hai literal không đổi, A2, A8) và đổi `--chi-ca=t01_` thành tên đầy đủ
ở `t153`, `t155`, vì tiền tố `t01_` nay chọn bốn ca; hai literal của `t70`, `t193` so đa tập TIỀN TỐ, nên ca mới của
packet này không dùng lại tiền tố đã có.

**Nghĩa vụ trong write set** (§6 mục 8; đo ở A8): (i) mọi ca `@ca` MỚI hoặc ĐÃ SỬA mà dùng một trong hai helper (kể
cả ca biên A3, và `t178` nếu bản sửa ở A2 dùng helper) phải tham chiếu helper ấy **trực tiếp ở cấp đỉnh thân hàm ca**,
tức trong một câu lệnh của chính hàm (kể cả bên trong `if`, `with`, `try`), không CHỈ trong hàm lồng, lambda, generator
expression hay comprehension, và không qua một hàm bọc cấp module; lời gọi thật vẫn được nằm trong comprehension nếu
cấp đỉnh có tham chiếu (ví dụ gán helper cho một biến cục bộ trước). Hai hàm giả `_a`/`_b` của `t70` là phép thử vị từ,
không phải "dùng helper", và giữ nguyên. (ii) Thêm tiền tố tên (`tNNN`) của mọi ca ở (i) vào literal `mong` của `t70`.
(iii) Dưới nền `nt` (seam của `t193`), mỗi ca ở (i) phải KẾT THÚC bằng đúng một trong hai: **đạt**, hoặc **ném
`BoQuaNen(WORKFLOW_DANG, "dang")` ra khỏi thân ca**. Ca ném thì thêm **tên đầy đủ** vào `SO_BO_QUA` với cặp
`(WORKFLOW_DANG, "dang")` **và** thêm tiền tố vào literal của `t193` (:11009–11010); ca tự bắt `BoQuaNen` và xử lý thành
kết quả đạt (như `R12` ở A8; `t199` cũng tự bắt nhưng dưới seam của phép quét thuộc K, vì seam ép `nt` vào chỗ nó
tự đo nền posix, A8) thì KHÔNG được thêm vào cả hai (thừa sổ cũng làm `t193` ĐỎ, A2). Ca
kết thúc bằng ngoại lệ KHÁC dưới `nt` là trái (iii): ví dụ bắt `BoQuaNen` rồi ném lại kiểu khác, hoặc gọi helper
trong một luồng khác để `BoQuaNen` không ra khỏi thân ca. Ca như vậy qua `t70` và `t193` mà `main()` dưới nền `nt`
ĐỎ, tức ĐỎ trên Windows ở lượt master (phiên soạn r11 đo, §10). Số ca mới bắt đầu từ `t204`: trên nền `ab457c6`, số lớn nhất vẫn là
`t203` (của #687; wp709 chỉ thêm ca tiền tố `t01`), và cả hai literal so theo tiền tố. Với (i), tập vị từ của `t70` trên ứng viên như nhau ở 3.11, 3.12
và 3.13 (A2), nên `mong` không phụ thuộc bản Python. `t193` chỉ canh (iii) cho ca thuộc ứng viên của nó: ca GỌI THẬT helper qua đường mà vị từ tĩnh và `_ca_ung_vien_gian_tiep` không đi theo (`globals()` hay `getattr`, `functools.partial` hay bí danh cấp module, lambda hoặc hàm lồng trong một hàm bọc, decorator đóng gói helper, tham số mặc định, phương thức lớp) để cả `t70` lẫn `t193` xanh ở 3.11, 3.12 và 3.13 trong khi `main()` dưới nền `nt` ĐỎ NGOÀI SỔ (review lượt 10 đo); các cách viết ấy đều trái (i). Ngoài ra ca kết thúc bằng ngoại lệ khác dưới `nt` trái (iii) mà qua cả `t70` lẫn `t193` (phiên soạn r11 đo, §10). Phép quét động ở A8 (vế N − D và vế K) bắt cả hai loại. Ca GỌI THẬT helper qua đường lạ rồi tự bắt `BoQuaNen` (dưới `nt` kết thúc bằng đạt) trái (i), (ii) mà lọt cả `t70`, `t193` lẫn hai vế ấy (review lượt 11 đo), nên A8 thêm vế H đo LỜI GỌI thật; nghĩa vụ đo bằng kết cục và lời gọi, không bằng một danh sách cách viết bị cấm. Đó là **nghĩa vụ trong write set**, không phải mở rộng phạm vi, và
không phải sửa đặc tả #677 hay #687.

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
   sự thật mới. Ví dụ đã biết: `t178` :8283–8284 (trên `ab457c6`; :7924–7925 trên `163fd5d`, :7789–7790 trên `20ec8d5`, :7763–7764 trên `89fc4fa`, :7769–7770 trên `1741e0a`; thân `t178` giống hệt giữa năm nền, chỉ dời dòng) viết *"`lease_id` sai KIỂU thì không có chốt
   tương ứng trong `kiem()`"*. Executor phải grep tìm hết, đừng chỉ sửa chỗ này.
8. `ops/lease_publish_test.py` — Giữ nghĩa vụ ở §4: (i) ca `@ca` mới hoặc đã sửa mà dùng `_chay_buoc_dang` hay
   `_chay_buoc_dang_that` thì tham chiếu helper ấy trực tiếp ở cấp đỉnh thân hàm ca; (ii) thêm tiền tố tên (`tNNN`)
   của các ca ấy vào literal `mong` của `t70`; (iii) dưới nền `nt`, mỗi ca ấy kết thúc bằng đạt, hoặc bằng `BoQuaNen` với tên
   đầy đủ trong `SO_BO_QUA` và tiền tố trong literal của `t193`; không bằng ngoại lệ khác (§4). Không đổi phép so literal thành phép đếm động, không nới vị
   từ `_ca_doc_than_buoc` hay `_ca_ung_vien_gian_tiep`, và không nới phép so sổ của `t193`: `t70` cố ý giữ tập mong
   đợi là literal độc lập (chú thích R1-F6 trong ca).

## 7. `nghiem_thu`

Mỗi tiêu chí nêu phép đo làm nó ĐỎ (L3). "Đột biến" nghĩa là chạy trên **bản sao tạm**, với
`PYTHONDONTWRITEBYTECODE=1`.

- **A1 (mục 1, D1)** — Ca mới: các dạng `true` `yes` `on` `1.5` `1.50` `0x1F` `017` `1_000`
  `5` `2026-09-29`, viết thành **văn bản YAML** và đọc qua `_doc_yaml` (không dựng dict bằng
  tay, để phép đo đi qua đúng lớp gây lỗi), đều cho `kiem()` ⇒ rc=8. Đối chứng `'yes'` có nháy
  ⇒ qua.
  **ĐỎ khi:** trả D1 về `str(lease["lease_id"])` ⇒ các dạng trên qua. **Fixture phải qua `_kiem_provider_identity` của
  nền** (tương tác với wp709, từ r12): trên `ab457c6`, `kiem()` gọi hàm ấy TRƯỚC D1 (§2), nên lease mà nó bác thì rc=10
  hay rc=8 che D1 và ca chết vì lý do vô can (A10). Phiên soạn r12 đo (09:00:59Z 07-10, `a1.py` ở scratch; Python 3.11.15
  và 3.12.3, cùng kết quả; `ops/lease_publish.py` của `ab457c6` và của `163fd5d`): mẫu
  `wp55-r4-review-viet-lai-codex-20260815.yaml` bỏ các trường `prompt_*` (`role: reviewer`, `provider: codex`,
  `assurance_target: cross_approved`, không khai `executor`), mười dạng viết thành YAML, đọc qua `_doc_yaml` rồi
  `kiem(bo_qua_han=True)` ⇒ trên `163fd5d` **qua** cả mười dạng lẫn đối chứng `'yes'`, trên `ab457c6` **rc=10** cả mười
  dạng LẪN đối chứng (*"lease khai cross_approved nhưng thiếu executor/reviewer identity hoặc model family"*); cùng mẫu
  thêm `executor: claude` ⇒ trên cả hai nền **qua** cả mười dạng (kiểu bool, float, int, date) lẫn đối chứng. Vậy trên
  nền `ab457c6` ca này ĐỎ khi dùng fixture qua được luật danh tính, còn mẫu wp55 nguyên văn không dùng được làm fixture.
  Fixture của suite (`lease_mau()`, `_yaml_that`, giống hệt thân giữa hai nền) qua luật ấy (`t198` xanh trên nền). Lịch
  sử: r10 đo 09:54:50Z 01-10 trên cây `git archive 163fd5d` (mẫu wp55 nguyên văn) và r8 đo 01:10:22Z 01-10 trên
  `20ec8d5`, cùng kết quả **qua**.
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
  `wp678`, Q11). Đặc tả #677 lúc ấy có r1–r7 trên master (`44620e8`); bản đóng băng mà PR #689 land theo là r8 (`ops/specs/dot-bien-l-bien-cong-khai-r8.md`, commit tạo `f860ab7` 29-09 17:09:42Z), vào master qua bookkeeping #699 (`b7e32e0`), là tệp `ops/specs/` duy nhất trong 118 tệp `163fd5d..a6de9d1`. Ca
  của #677 trong `ops/lease_publish_test.py`: `t195` :10642 (tập (i), khoá dãy lời gọi rỗng), `t196` :10686 và `t197`
  :10704 (tập (ii), chỉ khoá `rc≠0`, 0 POST, không "bỏ qua", và theo docstring `t196` cố ý **không** khoá dãy lời gọi
  *"để giữ đúng khi #678 đổi đường từ chối"*), `t198` :10733 (đối chứng `wp-ok-1`, đúng 1 POST và đúng dãy bốn lời
  gọi), `t199`–`t202` :10744–11034; helper `_chay_buoc_dang_that` :10506. `t202` bơm vectơ quan sát của `L` **ghi cứng**
  (đo 30-09 trên `85124dc`), không chạy `L` sống. Docstring `t195`–`t197` khai `L` đổi kết quả các ô ấy; đó là phép
  đo trên `89fc4fa`, chưa đo trên ứng viên. Trên nền, cả tám ca xanh (A8). **Tọa độ r10 (trên `163fd5d`):** `t195` :10996, `t196`
  :11040, `t197` :11058, `t198` :11087, `t199`–`t202` :11098–11388, helper `_chay_buoc_dang_that` :10860; ca của #687
  `t193` :10614–10744, `t194` :10758–10829, `t203` :11392–11441; cả 198 ca xanh trên nền mới (A8). **Tọa độ r12 (trên `ab457c6`):** `t195` :11356, `t196` :11400, `t197` :11418, `t198` :11447,
  `t199`–`t202` :11458–11748, helper `_chay_buoc_dang_that` :11220; ca của #687 `t193` :10974–11104, `t194`
  :11118–11189, `t203` :11752–11801; cả 201 ca xanh trên nền (A8). `t70` :3398–3412
  (M6 của #677; vị từ `_ca_doc_than_buoc` :3393–3394; trên `163fd5d` là :3040–3054 và :3035–3036; trên `20ec8d5` là
  :2995–3009 và :2990–2991) ghim literal
  `mong` gồm tiền tố tên các ca mà vị từ nhận (§4), nên ca biên A3 phải theo nghĩa vụ (i)–(iii) của §4; review lượt 8 đo
  trên bản sao `20ec8d5`: thêm một ca chỉ tham chiếu helper ở cấp đỉnh (không gọi) ⇒ `t70` ĐỎ (`0/1`), đối chứng
  cây gốc `1/1`. Phiên soạn r9 đo lại 05:20:07Z–05:20:08Z 01-10 trên cây `git archive 20ec8d5 ops .github`, lệnh
  `PYTHONDONTWRITEBYTECODE=1 python3 ops/lease_publish_test.py --chi-ca=t70_`: gốc `1/1`; thêm một ca `@ca` chỉ nhắc
  `_chay_buoc_dang_that` ⇒ `0/1`, dòng ĐỎ *"kiểm kê ca đọc thân bước lệch tập mong đợi"*; thêm cả tên ca ấy vào
  `mong` ⇒ `1/1`; 0 tệp `.pyc`. Đó là kiểm kê, không phải bằng chứng nhánh; nghĩa vụ sửa `mong` thuộc write set (§4,
  §6 mục 8). Review lượt 9 đo thêm (05:39:54Z–05:40:08Z 01-10, mỗi biến thể một cây `git archive 20ec8d5 ops .github`
  riêng, cùng lệnh; ghi Python 3.11 | 3.12): ca mới gọi helper chỉ trong hàm lồng ⇒ không thêm tên `1/1` | `1/1`, thêm
  tên `0/1` | `0/1`; chỉ trong lambda ⇒ không thêm `1/1` | `1/1`, thêm `0/1` | `0/1`; chỉ trong list comprehension ⇒ không
  thêm `1/1` | `0/1`, thêm `0/1` | `1/1` (không tập `mong` nào xanh ở cả hai bản); sửa `t178` thêm một dòng nhắc helper ở
  cấp đỉnh ⇒ không thêm `0/1` | `0/1`, thêm `t178` ⇒ `1/1` | `1/1`; 0 tệp `.pyc`. Quét vị từ trên nền: cấp đỉnh 13 ca
  (đúng `mong`), quét đệ quy mọi code object 14 (thêm chính `t70`).
  Phiên soạn r10 tái lập và mở rộng trên nền mới (09:49:48Z–09:50:54Z 01-10; mỗi biến thể một cây `git archive 163fd5d`
  của `ops/lease_publish.py`, `ops/lease_publish_test.py`, `ops/chay_lease_publish_test.sh` và `.github`; lệnh
  `PYTHONDONTWRITEBYTECODE=1 <py> ops/lease_publish_test.py --chi-ca=<ca>`, `<py>` là `python3.11` (3.11.15),
  `python3.12` (3.12.3), `python3.13` (3.13.12); ca mới mang số `t204`; ghi `3.11 | 3.12 | 3.13`; "không thêm" và "thêm"
  là thiếu và có tiền tố ca ấy trong `mong`). Gốc: `t70` và `t193` đều `1/1` ở ba bản. Với `t70`: tham chiếu cấp đỉnh
  (chỉ nhắc tên, hoặc gọi trong `if False:`, hoặc gán cho biến cục bộ rồi gọi trong comprehension), và sửa `t178` thêm
  một dòng nhắc cấp đỉnh ⇒ không thêm `0/1`, thêm `1/1`, ở ba bản; chỉ trong hàm lồng, lambda hay generator expression ⇒
  không thêm `1/1`, thêm `0/1`, ở ba bản; chỉ trong list comprehension (ca mới, hoặc `t178` sửa) ⇒ không thêm
  `1/1 | 0/1 | 0/1`, thêm `0/1 | 1/1 | 1/1`; chỉ nhắc trong docstring, chú thích và chuỗi ⇒ không thêm `1/1`, thêm
  `0/1`, ở ba bản. Các biến thể chỉ tham chiếu mà không gọi thật (cấp đỉnh, `if False:`, comprehension trên dãy rỗng)
  để `t193` `1/1` ở ba bản. Tương tác `t193` (3.11 | 3.12, hai bản cùng kết quả ở mọi ô): ca mới GỌI THẬT
  `_chay_buoc_dang_that` ở cấp đỉnh, không thêm gì ⇒ `t70` `0/1`, `t193` `0/1`; chỉ thêm `mong` ⇒ `t70` `1/1`, `t193`
  `0/1`; thêm `mong` và `SO_BO_QUA` ⇒ `t193` `0/1`; thêm `mong` và literal của `t193` ⇒ `t193` `0/1`; thêm cả ba ⇒
  `t70` `1/1`, `t193` `1/1`; ca gọi thật nhưng tự bắt `BoQuaNen`, thêm `mong` ⇒ cả hai `1/1`, mà thêm cả sổ và literal
  ⇒ `t193` `0/1`; ca gọi qua một hàm bọc cấp module, không thêm gì ⇒ `t70` **`1/1`**, `t193` `0/1`, thêm sổ và literal
  ⇒ cả hai `1/1`, tức `t70` xanh mà kiểm kê thiếu ca ấy. 0 tệp `.pyc`. Phép quét (09:51:18Z; D là tập vị từ `t70`, R là
  quét đệ quy qua `co_consts`, G là `_ca_ung_vien_gian_tiep(CA)`; ba bản cùng kết quả trừ dạng comprehension): nền 198
  ca, D 13 (đúng `mong`), R 14, chỉ lồng `{t70}`, G 14 với G − D = `{t202}` (`t202` tham chiếu ca `t195`, mà `t195` gọi
  helper), D − G rỗng, sổ 12 với D − sổ = `{t199}`; biến thể hàm lồng ⇒ chỉ lồng `{t70, t204}`; biến thể comprehension
  ⇒ chỉ lồng `{t70, t204}` ở 3.11, `{t70}` ở 3.12 và 3.13; biến thể hàm bọc ⇒ G − D = `{t202, t204}`, chỉ lồng `{t70}`.
  Đo thẳng vị từ (`H & set(fn.__code__.co_names)`) trên các hàm dựng riêng, ba bản: tham chiếu trong `if`, `with`,
  `try`, và tham chiếu cấp đỉnh rồi gọi trong comprehension ⇒ được tính ở cả ba; list, set và dict comprehension ⇒ tính ở
  3.12, 3.13, không ở 3.11; generator expression, lambda, hàm lồng, chuỗi ⇒ không tính ở bản nào. Script ở scratch,
  không vào kho. Lịch sử: lần đo đầu của r10 trên `20ec8d5` (09:22:15Z–09:22:52Z, hai mươi biến thể của `t70`, ca mới
  mang số `t203`) cho cùng kết quả ở mọi biến thể chung; quét nền `20ec8d5`: 195 ca, cấp đỉnh 13, đệ quy 14, chỉ lồng
  `{t70}`.
  Phiên soạn r12 tái lập trên nền mới (09:02:03Z–09:03:21Z 07-10; mỗi biến thể một cây `git archive ab457c6` của
  `ops/lease_publish.py`, `ops/lease_publish_test.py`, `ops/chay_lease_publish_test.sh`, `ops/bash_nen.py` và `.github`;
  lệnh như trên; ca mới mang số `t204`; `python3.11` (3.11.15), `python3.12` (3.12.3), `python3.13` (3.13.12) cùng kết
  quả ở mọi ô): gốc `t70` `1/1`, `t193` `1/1`; ca chỉ tham chiếu `_chay_buoc_dang_that` ở cấp đỉnh, không thêm gì ⇒ `t70`
  `0/1`, `t193` `1/1`; thêm `mong` ⇒ cả hai `1/1`; ca GỌI THẬT ở cấp đỉnh, không thêm gì ⇒ `t70` `0/1`, `t193` `0/1`;
  chỉ thêm `mong` ⇒ `t70` `1/1`, `t193` `0/1`; thêm `mong` và sổ ⇒ `t193` `0/1`; thêm `mong` và literal của `t193` ⇒
  `t193` `0/1`; thêm cả ba ⇒ cả hai `1/1`; 0 tệp `.pyc`. Quét tĩnh (`tinh.py` ở scratch; ba bản cùng kết quả): nền
  `ab457c6` 201 ca, D 13 (đúng `mong`), R 14, chỉ lồng `{t70}`, G 14, G − D `{t202}`, D − G rỗng, sổ 12, D − sổ
  `{t199}`, y như `163fd5d` (198 ca); ba ca `t01_*` của wp709 không thuộc D, R hay G.
  Sửa cả docstring D2 và `t178` để tách bằng chứng lịch sử khỏi hành vi sau D3.
- **A3 (mục 2, D3) — CA BIÊN WORKFLOW** — Thân bước `đăng` trích từ
  `.github/workflows/ops-publish-lease.yml` (dùng lại bộ trích sẵn có trong suite, không chép
  lại), `lease_publish.py` thật, `gh` giả **trên PATH** và **giữ trạng thái**. Issue đã có comment
  bot ``**Lease `True`**``; lease mới khai `lease_id: yes` ⇒ bước **khác 0** và **0 POST**. Kèm
  ca đối chứng dương: một `lease_id` chuỗi hợp lệ khác ⇒ bước 0 và đúng **1 POST**, để giàn hỏng
  không thể xanh.
  **ĐỎ khi:** chạy trên nền `ab457c6` (`.github/workflows/ops-publish-lease.yml` giống hệt từ `89fc4fa`;
  `ops/lease_publish.py` khác `163fd5d` chỉ ở khối danh tính của wp709, §2) ⇒ bước `rc=0`, 0 POST. Đo lại 09:01:42Z
  07-10 trên cây `git archive ab457c6` (3.11.15 và 3.12.3, cùng kết quả; `a3.py` ở scratch): `lease_id: yes` gặp comment
  bot ``**Lease `True`**`` ⇒ `rc=0`, **0 POST**, 2 lời gọi, có dòng *"đã đăng trước đó"*; đối chứng `'fresh-id'` ⇒
  `rc=0`, **1 POST**, 4 lời gọi (lease dựng bằng `_yaml_that`, nên qua luật danh tính của wp709). Lịch sử r10 trên
  `163fd5d`: đo 09:54:50Z 01-10 trên cây
  `git archive 163fd5d` bằng `_chay_buoc_dang_that` mà #677 đưa vào suite (thân giống hệt `20ec8d5`; thân bước `đăng`
  trích bằng `_buoc_workflow`, `gh` giả trên PATH, giữ trạng thái; lease dựng bằng `_yaml_that`, comment bằng
  `_dau_bot` của suite): `lease_id: yes` gặp comment bot ``**Lease `True`**`` ⇒ `rc=0`, **0 POST**, 2 lời gọi, có dòng
  *"đã đăng trước đó"*; đối chứng `'fresh-id'` ⇒ `rc=0`, **1 POST**, 4 lời gọi. Lịch sử: r8 đo 01:10:22Z 01-10 trên
  `20ec8d5`, cùng `rc` và số POST. Lần đo đầu ở biên là của cross-review lượt 1 (§1).
  Nếu ca biên này dùng `_chay_buoc_dang_that` hoặc `_chay_buoc_dang` (phép đo ĐỎ ở trên dùng `_chay_buoc_dang_that`),
  nó phải tham chiếu helper ở cấp đỉnh thân hàm ca và thêm tiền tố tên vào `mong` của `t70` (§4, §6 mục 8). Khi đã
  tham chiếu ở cấp đỉnh, thiếu tiền tố thì `t70` ĐỎ ở cả 3.11, 3.12 lẫn 3.13 (A2). Chỉ tham chiếu trong hàm lồng, lambda
  hay generator expression thì `t70` vẫn xanh dù thiếu tiền tố, nên vi phạm ấy chỉ lộ ở phép quét của A8. Ca biên GỌI
  THẬT `_chay_buoc_dang_that` mà không tự bắt `BoQuaNen` thì còn phải vào `SO_BO_QUA` và literal của `t193` (§4 (iii));
  thiếu một trong hai thì `t193` ĐỎ (A2) khi ca biên thuộc ứng viên của `t193`, tức khi nó tham chiếu helper đúng (i); gọi qua đường khác thì `t193` vẫn xanh và chỉ phép quét động ở A8 bắt. Dưới nền `nt` ca biên phải kết thúc bằng `BoQuaNen` có trong sổ (hoặc bằng đạt nếu nó tự bắt và xử lý `BoQuaNen`), không bằng ngoại lệ khác (§4 (iii)); vế K của phép quét động ở A8 đo điều ấy.
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
  **ĐỎ khi:** trả phép ép kiểu về riêng từng toán hạng ở D5 (:587, :592; trên `ab457c6` :746, :751) và D6 (:609,
  :612; :768, :771),
  giữ nguyên các chốt còn lại; mỗi mutant phải giết đúng ca đổi kiểu toán hạng ấy.
  Không hoàn nguyên cả hàm rồi nhận đó là bằng chứng mọi vị trí đọc đều có răng. Nền vẫn gộp: phiên soạn r12 gọi thẳng
  `_bia_mo_doi_xung` (09:05:44Z 07-10, `do.py` ở scratch) với lease cũ `lease_id: 1000` (int) trỏ `da_bi_thay_the`
  tới lease mới `thay_the_cho: "1000"` ⇒ `True` trên cả `ab457c6` lẫn `163fd5d`.
- **A6 (mục 4, D7)** — Hai lease trên hai ref, `lease_id: yes` và `lease_id: on`, cùng giữ một
  đường dẫn ⇒ `ai-dang-giu` in `KHÔNG_XÁC_ĐỊNH` cho cả hai và thoát khác 0.
  **ĐỎ khi:** chạy trên nền với hai lease còn hạn ⇒ `NGƯỜI_GIỮ 1: True`, rc=11 (phiên soạn r12 đo lại 09:05:44Z 07-10
  trên `ab457c6` và `163fd5d`, kho tạm hai nhánh: cùng dòng ấy, rc=11).
  Vì nền đã khác 0, ca phải chốt nhãn `KHÔNG_XÁC_ĐỊNH` và danh tính ref/path của cả hai
  lease lỗi; không chỉ kiểm `rc != 0`. Đo lại 29-09-2026 bằng fixture hai ref trong review #679.
- **A7 (mục 5, D8)** — Đo riêng cả `check --du-bao` và `ai-dang-giu --du-bao`.
  `check` qua D1 trước; `ai-dang-giu` gọi dự báo trước vòng D7 và không gọi D1. Không dùng
  kết quả không tới được của `check` để miễn nhánh `ai-dang-giu`, hoặc chỉ đo lời gọi trực
  tiếp helper rồi suy thành khả năng tới được từ CLI. Lease sai kiểu vẫn tới :1967 trên
  `163fd5d` (:2127 trên `ab457c6`; phiên soạn r12 đo 09:05:44Z 07-10: `ai-dang-giu --du-bao` với lease
  `lease_id: 1_000` in `DU_BAO: 1000`, cùng kết quả ở hai nền); fixture của `check --du-bao` cũng phải qua `_kiem_provider_identity` của nền như A1
  (review lượt 12 đo trên `ab457c6`: mẫu kiểu wp55, `cross_approved` thiếu executor, ra rc=10 trước D1 với cả mười một dạng `lease_id` thử ở A1); khi thêm chốt ở D8 cần ca trực tiếp để D7/D1 không che mutant của chính D8.
  · Tới được ⇒ chốt + ca, đột biến gỡ chốt ⇒ ĐỎ.
  · Không tới được ⇒ một ca chứng minh lease sai kiểu bị chặn **trước** các dòng ấy, kèm đột biến
  gỡ chốt D1 để chứng minh ca có răng. Ghi rõ đã chọn nhánh nào và bằng phép đo nào.
- **A8 (mục 6/7, cả write set)** — Toàn suite `ops/lease_publish_test.py` **delta = 0 ca đỏ**
  so với nền. Số lịch sử đo 06:4xZ 29-09 trên `1741e0a`: **185/187**. Hai ca đỏ là `t137` và `t159`,
  cả hai `KHÔNG ĐO ĐƯỢC: thiếu shellcheck` (lời khai lịch sử, không dùng làm nền hiện tại).
  Review #679 đo lại 29-09-2026: **187/187**, rc=0, bỏ qua=0, với shellcheck 0.9.0 và
  actionlint 1.7.7; hai tệp Python có cùng blob với `1741e0a` (lịch sử). **Nền hiện tại**
  (`ab457c6`, r12): suite **201/201** dưới Python 3.11.15 (08:27:32Z–08:34:16Z 07-10) và **201/201** dưới 3.12.3
  (08:27:32Z–08:35:00Z, hai lượt song song), rc=0 và bỏ qua 0 ở cả hai; 201 bằng số `^@ca` đếm tĩnh; log mỗi lượt có
  201 dòng vào và 201 dòng ra `QUA` (không kể dòng `[A]`/`[B]` của tiến trình con trong `t125`); `t125` mất 230,8 và
  253,4 giây. Hai clone (`git clone --no-hardlinks` từ `adg2`, `checkout --detach ab457c6`, `core.abbrev 7`) dựng trong
  **một** lệnh; mỗi lượt đặt `python` và `python3` trỏ đúng bản đang đo; PyYAML 6.0.1, git 2.43.0, shellcheck 0.9.0,
  actionlint 1.7.7; 0 tệp `.pyc` và `status --porcelain --ignored` 0 dòng sau mỗi lượt. Ba ca thêm so `163fd5d` là
  `t01_*` của wp709. Lịch sử `163fd5d` (r10): suite **198/198** dưới Python 3.11.15 (09:46:39Z–09:53:20Z 01-10) và **198/198** dưới 3.12.3
  (09:53:20Z–10:00:41Z), rc=0 và bỏ qua 0 ở cả hai; 198 bằng số `^@ca` đếm tĩnh; log mỗi lượt có 198 dòng vào và 198
  dòng ra `QUA`. Hai clone (`git clone --no-hardlinks` từ `adg2`, `checkout --detach 163fd5d`, `core.abbrev 7`) dựng
  trong **một** lệnh; mỗi lượt đặt `python` và `python3` trỏ đúng bản đang đo (CI có `python` là 3.12); PyYAML 6.0.1
  (CI cài 6.0.3), git 2.43.0, shellcheck 0.9.0, actionlint 1.7.7; 0 tệp `.pyc` và `status --porcelain --ignored` 0 dòng
  sau mỗi lượt. Ba ca thêm so `20ec8d5` là `t193`, `t194`, `t203` của #687; `t125` (chạy lại cả suite trong tiến trình
  con, 199 giây ở lượt 3.11) và `t203` lấy danh sách ca động từ `CA`, không ghim literal nào mà ca mới phải sửa. Lịch
  sử `20ec8d5` (r8): **195/195**, rc=0, bỏ qua 0 (01:11:15Z–01:16:50Z 01-10, 3.11.15), cùng **một** lệnh với vế
  `89fc4fa` **187/187** (01:06:03Z–01:11:15Z); review lượt 9 tái lập 195/195 dưới 3.12.3. Tám ca thêm từ `89fc4fa` tới
  `20ec8d5` là `t195`–`t202` của #677 (A2). Lịch sử `89fc4fa`:
  187/187 đo 08:0xZ 29-09 trên commit merge `589336f` (cây của `89fc4fa` + các tệp spec). Lệnh: từ gốc repo chạy
  `PYTHONDONTWRITEBYTECODE=1 TMPDIR=<scratch> python ops/lease_publish_test.py`.
  Khi thi hành, đo lại **cả hai vế** (nền và ứng viên) trong **một** lệnh, cùng công cụ.
  `python -m ruff check --select F ops/lease_publish.py ops/lease_publish_test.py`: delta F = 0. Nền `ab457c6` có **11**
  lỗi F: 9 lỗi của tệp test như `163fd5d` (cùng tập, bỏ số dòng) cộng 2 `F841` mới của wp709 ở `ops/lease_publish.py`
  :198–199 (biến `executor_surface`, `executor_transport` trong `_kiem_provider_identity`), §8; hai lỗi ấy ngoài
  objective, executor không sửa; chúng thuộc nền nên không tính vào delta.
  **ĐỎ khi:** ứng viên có thêm ca đỏ (kể cả `t70`, `t193`), hoặc có thêm lỗi F, hoặc nghĩa vụ ở §4 không được đo là đạt.
  Vế (iii) do `t193` canh trong suite **chỉ cho ca thuộc ứng viên** `_ca_ung_vien_gian_tiep(CA)` và chỉ với kết cục `BoQuaNen` (ngoại lệ khác bị `nem_nt` bỏ qua); vế (i), (ii) và toàn bộ (iii) đo thêm như sau.
  Đo nghĩa vụ ấy trên ứng viên: `PYTHONDONTWRITEBYTECODE=1 python3.11 ops/lease_publish_test.py --chi-ca=t70_` và cùng
  lệnh với `python3.12` đều `1/1` (hai bản lệch nhau ⇒ có ca chỉ tham chiếu helper trong comprehension, trái (i)); và
  một phép quét dưới `python3.11` liệt kê các ca `@ca` có tên helper trong `co_names` của một code object lồng bất kỳ
  (đệ quy qua `co_consts`) mà không có ở cấp đỉnh phải ra đúng `{t70}` (nền: cấp đỉnh 13, đệ quy 14, chỉ lồng `{t70}`,
  A2; quét dưới 3.12 hay 3.13 không thấy dạng comprehension). Phép quét là dụng cụ của executor ở scratch, không vào
  kho; handoff ghi lệnh, output và bản Python. Thiếu `python3.11` hay `python3.12` ⇒ vế tương ứng `KHÔNG ĐO ĐƯỢC`, ghi
  vào handoff, không tính là đạt. Thêm: tập G − D (ứng viên gián tiếp của `t193` trừ tập vị từ của `t70`, đo ở cả `python3.11` lẫn `python3.12`: hàm bọc gọi helper trong list comprehension chỉ vào G ở 3.12 và 3.13)
  trên ứng viên phải bằng đúng tập ấy trên nền (`{t202}`, A2); có thêm phần tử nghĩa là có ca gọi helper qua hàm bọc
  cấp module, trái (i). **Phép quét động: tiêu chí nghiệm thu của (iii), và của phần (i) mà vị từ tĩnh không thấy** (HINT lượt 10 đề xuất
  hai vế đầu; r11 thêm vế K và chốt cách chạy). Dụng cụ của executor ở scratch, không vào kho; mô phỏng đúng seam của
  `t193` (`nem_nt`): đặt `<gốc>/ops` đầu `sys.path` (như khi chạy `python ops/lease_publish_test.py`), nạp
  `ops/lease_publish_test.py` như module (từ r15; review lượt 14, E8n: cài `threading.setprofile` TRƯỚC khi nạp, hàm profile
  chưa làm gì tới lúc nạp xong, để luồng `threading` khởi động lúc nạp module cũng mang nó), vá `_ly_do_bo_qua_workflow` để
  `nen` mặc định là `nt`, **và** (từ r14; review lượt 13, họ E8) lật `os.name` thành `nt` trong lúc còn khung mở của một hàm
  có tên `_ly_do_bo_qua_workflow` HOẶC có bytecode (`co_code`) bằng bytecode của guard đã nạp (`sys.setprofile` và
  `threading.setprofile`; bộ nhớ đệm theo code object giữ tham chiếu mạnh). `os.name` là trạng thái TOÀN TIẾN TRÌNH, nên phép
  lật đếm độ sâu trên mọi luồng, có khoá (từ r15; review lượt 14, V1): giá trị gốc là `os.name` lúc bộ quét bắt đầu, trước khi
  nạp (theo dụng cụ đã đo; V9); khung guard CUỐI CÙNG ra thì trả giá trị gốc, không *"trả giá trị lúc vào khung"* (hai luồng cùng ở trong guard thì cách ấy để
  `os.name` kẹt `nt` cho mọi ca chạy sau); sau MỖI ca, còn khung guard mở hay `os.name` khác giá trị gốc thì ghi ca ấy vào
  tập L rồi trả giá trị gốc. Mục đích: guard của một BẢN SAO ở module nạp lại (globals mới, kể cả khi đổi tên guard:
  lớp `BoQuaNen` riêng, seam dict không vá tới) cũng thấy nền `nt` như trên Windows thật; rồi CHẠY MỌI ca `@ca`
  trong `CA` và xếp mỗi ca vào đúng một tập: đạt; N (ném `BoQuaNen` của module đã nạp, ghi cặp `(Path(tep).resolve(), ten_job)`);
  K (ném ngoại lệ khác, kể cả `BoQuaNen` của một lớp khác lớp của module đã nạp; ghi tên lớp kèm module). Cùng lượt ghi H: tập ca mà trong lúc chạy có lời gọi THẬT tới code object của `_chay_buoc_dang` hay
  `_chay_buoc_dang_that` (`sys.setprofile` và `threading.setprofile`, so `frame.f_code`), nên thấy cả lời gọi qua
  `globals()`, `partial`, bí danh, decorator hay luồng tạo bằng `threading`, kể cả khi ca tự bắt `BoQuaNen` (giới hạn
  đo ở đoạn *Giới hạn của vế H* dưới). Cùng lượt ghi H2: tập ca mà trong lúc chạy một thể hiện `BoQuaNen` được TẠO RA; dụng cụ
  gán lại `BoQuaNen.__init__` ở cấp LỚP (ghi tên ca đang chạy rồi gọi hàm cũ), nên H2 thấy cả ca tự bắt `BoQuaNen`, cả khi helper là BẢN
  SAO DÙNG CHUNG globals của module đã nạp (`exec` mã nguồn helper vào bản chép `globals()`, `code.replace`, bản sao dựng ở cấp module), trong
  luồng `_thread` thô, và khi ca tự gọi `sys.setprofile(None)`; H2 không thấy ca mà guard không chạy (lỗi trước guard), chạy trong tiến trình con,
  hay là guard của BẢN SAO ở một module NẠP LẠI (globals mới; họ E8 ở đoạn *Giới hạn của vế H*): ca ấy vào K (hay vào N khi chính module đã nạp bị nạp lại tại chỗ, E8h) nhờ vế lật `os.name` ở
  trên, nhưng CHỈ KHI khung guard của bản sao chạy lúc hàm profile của bộ quét đang hoạt động trên luồng của nó, khớp tên hay bytecode, và đọc `os.name` của
  chính module `os` trong khung ấy; thiếu một điều kiện là giới hạn (α), (β), (γ) ở đoạn họ E8. Đạt khi và chỉ khi, ở **cả**
  `python3.11` **lẫn** `python3.12`: (q1) N bằng đúng `SO_BO_QUA` của ứng
  viên, đúng cặp; (q2) N − D rỗng, với D là tập vị từ của `t70` trên ứng viên ở cùng bản Python; (q3) tập TÊN của K
  trên ứng viên trừ tập ấy trên nền rỗng (ca của nền rời K thì handoff ghi ca nào, vì sao); (q4) tập TÊN của H − D
  trên ứng viên bằng đúng tập ấy trên nền; (q5) tập TÊN của H2 − D trên ứng viên bằng đúng tập ấy trên nền. Nền và ứng viên quét trong **một** lệnh, cùng bản Python, cùng kiểu cây
  (clone đầy đủ, chạy từ gốc), vì K phụ thuộc cách quét (đo dưới). Ca thuộc N − D là ca gọi helper không qua tham chiếu
  cấp đỉnh, trái (i); ca của ứng viên thuộc K mà không thuộc K của nền là ca kết thúc bằng ngoại lệ khác dưới `nt`, trái
  (iii), và nó ĐỎ trên Windows dù `t70`, `t193` cùng xanh. Ca của ứng viên thuộc H − D mà không thuộc H − D của nền
  là ca gọi helper không qua tham chiếu cấp đỉnh, trái (i), (ii), kể cả khi nó tự bắt `BoQuaNen`. K của nền gồm tạo
  tác của seam (`t199`, `t203` tự đo nền posix): một ca mới cùng kiểu (vá `os.name` để đo guard, hay quanh một lời gọi guard: V9 ở đoạn *Phiên soạn r15 đo lại*) vào K dù trên Windows
  thật có thể đạt; gặp thì handoff nêu, không tự tính là đạt. Cùng cách xử lý cho tạo tác của vế lật (từ r15; review lượt 14):
  trong lúc còn khung guard mở, MỌI luồng thấy `os.name` là `nt`, nên ca hợp lệ chạy mã phụ thuộc `os.name` (dựng `Path`) ở
  một luồng khác song song với guard có thể vào K dù trên Windows thật đạt (V6 ở đoạn họ E8; V10, guard chạy ở luồng khởi động lúc nạp, ở đoạn *Phiên soạn r15 đo lại*), và mọi ca thuộc L. Thiếu
  `python3.11` hay `python3.12` ⇒ vế ấy `KHÔNG ĐO ĐƯỢC`, không tính là đạt. Handoff ghi lệnh, bản Python, thời gian chạy, và
  N, N − D, K, H − D, H2 − D, L của cả hai vế.
  **Vế (S)** (tĩnh, một lần; đo ở 3.11, 3.12 và 3.13 cho cùng kết quả): so cây `ast` của `ops/lease_publish_test.py` ở nền
  và ở ứng viên. Một LẦN XUẤT HIỆN là một giá trị chuỗi (hay bytes) chứa chuỗi con `chay_buoc_` (tiền tố của hai tên helper;
  ở `ab457c6` không tên nào khác có nó) ở BẤT KỲ trường nào của BẤT KỲ nút nào, duyệt bằng `ast.walk` cộng `ast.iter_fields`,
  không theo một danh sách loại nút: hằng chuỗi, tên, thuộc tính, tên đối số từ khoá, tên tham số, tên hàm hay lớp, tên
  trong `global`, `nonlocal`, `import`, `except … as`. Mỗi lần được khoá theo (loại nút, trường, nội dung, hàm bao ngoài),
  với hàm bao ngoài là `def` hay `lambda` gần nhất mà nút nằm trong THÂN của nó (decorator, giá trị mặc định và chú thích
  kiểu của một hàm không thuộc thân hàm ấy); chỉ phần ứng viên HƠN nền (đa tập) được xét. Lần mới ĐƯỢC PHÉP khi và chỉ khi
  là `Name.id` hay `Attribute.attr` nằm trong thân một hàm (lời gọi, tham chiếu trần, hay gán cho một biến cục bộ, đúng ví
  dụ ở (i)); MỌI lần mới khác làm (S) ĐỎ, gồm cả (a) hằng chuỗi hay bytes (docstring, thông điệp, `globals()["…"]`,
  `getattr`, mã đưa cho `exec`, `eval` hay tiến trình con, kể cả chuỗi nhiều dòng) và (b) mọi thứ ngoài thân hàm (bí danh hay
  bản sao cấp module; thân `class`, decorator hay giá trị mặc định của hàm cấp module), nhưng không chỉ hai dạng ấy: tên
  đối số từ khoá hay tên tham số chứa chuỗi con cũng ĐỎ (từ r13). Chú thích `#` không nằm trong `ast` nên không bị đếm.
  Mỗi lần mới bị ĐỎ là một finding mở cho reviewer, không tự tính là đạt; handoff liệt kê từng lần mới có chuỗi con và
  dạng của nó. Vị trí (cấp đỉnh thân ca) và hiệu ứng vẫn do `t70`, (q2), (q4), (q5) đo.
  Nghĩa vụ (i) chỉ được đo là đạt khi cả (q1) đến (q5) lẫn (S) đạt.
  Review lượt 11 đo (script quét viết độc lập theo chữ đoạn này, clone đủ `163fd5d`): nền 311,6 giây
  (3.11.15) và 361,9 giây (3.12.3), hai lượt song song ⇒ N đúng 12 ca của sổ, đúng cặp, N − D rỗng,
  K = {`t199`, `t203`}; có `setprofile` (3.12.3, 503,4 giây) ⇒ H − D của nền = {`t193`}. Biến thể
  N9 (gọi `globals()["_chay_buoc_dang_that"]` rồi `except BoQuaNen: return`) và N10 (gọi qua `globals()` trong một
  luồng, nuốt `BoQuaNen`), không thêm `mong`, sổ hay literal ⇒ `t70` `1/1`, `t193` `1/1`, N, K, N − D không có `t204`, ở
  3.11 lẫn 3.12, chỉ H − D thêm `t204`; quét đủ N9 cùng lệnh với nền (3.12.3) ⇒ N bằng sổ (q1 đạt), N − D rỗng, K bằng nền (q2, q3 đạt), H − D = {`t193`, `t204`} khác nền (594,5 giây). M7, R11, R12 ⇒
  H − D bằng nền; M1–M3, M5, N1–N8, R13 ⇒ H − D thêm `t204`.
  **Phiên soạn r12 đo trên nền `ab457c6`** (`quet12.py` ở scratch, viết theo chữ đoạn này: `<gốc>/ops` đầu `sys.path`,
  seam `nem_nt`, chạy mọi ca, `sys.setprofile` và `threading.setprofile` bật quanh từng ca với hàm so `frame.f_code` với
  code object của hai helper; hai clone đầy đủ `ab457c6`, chạy từ gốc, `python` và `python3` trỏ đúng bản,
  `PYTHONDONTWRITEBYTECODE=1`; MỖI bản Python MỘT lệnh: quét đủ nền, rồi quét đủ N9, N10, M7, rồi pha nhanh mọi biến
  thể, trả nền và kiểm sha256 sau mỗi biến thể; hai lệnh chạy song song từ 08:35:56Z 07-10 trên máy 4 lõi, tải trung bình
  khoảng 8; xong 09:21:37Z ở 3.11 và 09:30:05Z ở 3.12, cả hai `status --porcelain --ignored` 0 dòng, 0 tệp `.pyc`). Ghi
  `3.11 | 3.12`. Nền ⇒ 201 ca = 187 đạt + N 12 + K 2: N bằng đúng sổ, đúng cặp, N − D rỗng, K = {`t199`, `t203`}
  (`TinHieuChotCa`), H − D = {`t193`}, ở cả hai bản (629,9 | 742,2 giây); ba ca `t01_*` của wp709 đạt dưới seam. Quét đủ
  cùng lệnh với nền: N9 (648,4 | 834,6 giây) và N10 (606,3 | 682,3 giây) ⇒ 202 ca, N bằng sổ (q1 đạt), N − D rỗng (q2
  đạt), K bằng nền (q3 đạt), H − D = {`t193`, `t204`} khác nền (**q4 ĐỎ**) ở cả hai bản; M7 làm đúng (606,0 | 780,7 giây)
  ⇒ N bằng sổ của ứng viên (có `t204`), N − D rỗng, K bằng nền, H − D bằng nền: không vế nào báo nhầm. Pha nhanh
  (`--chi-ca=t70_`, `t193_`, `t204_` bằng chính suite dưới posix, cộng quét chỉ `t70`, `t193`, `t204` có H; biến thể chèn
  `t204_moi` trước `def main(`; 19 biến thể của lượt 11 dựng lại trên `ab457c6` bằng `patch --fuzz=0` từ diff của chúng so
  `163fd5d`, các dòng thêm và bớt khớp từng dòng bản gốc; thêm E1–E7 của phiên soạn r12), cùng kết quả ở hai bản, trừ N5
  (hàm bọc gọi helper trong list comprehension: ở 3.12 `t193` `0/1` dưới posix và K có `t193`, vì `_ca_ung_vien_gian_tiep`
  thấy ca ấy ở 3.12 mà không ở 3.11, A2):
  M1–M3, N1–N8 ⇒ `t70` `1/1`, `t193` `1/1`, `t204` thuộc N − D và H − D (q2, q4 bắt); M5 ⇒ K có `t204`
  (`TinHieuChotCa`) và H − D có `t204` (q3, q4); M6 ⇒ chỉ K có `t204` (`AssertionError`; tham chiếu ở cấp đỉnh nên `t204`
  thuộc D); N9, N10 ⇒ CHỈ H − D có `t204` (q4); R13 ⇒ `t193` `0/1` dưới posix, K có `t193`, `t204` thuộc N − D và H − D;
  E7 (helper ném trước guard) ⇒ H − D có `t204`; M7, R11 (làm đúng) và R12 (tự bắt, có `mong`) ⇒ không vế nào bắt.
  **Giới hạn của vế H, đo** (cùng các lệnh trên; E2, E6 bản đầu dựng hàm bản sao không kèm `__defaults__` nên `t204` ném
  `TypeError` dưới posix, tức tự ĐỎ trong suite; bản sửa E2b, E6b chạy
  riêng, cùng nền trong MỘT lệnh mỗi bản Python, trên cây `git archive ab457c6`, 09:28:11Z–09:28:53Z 07-10).
  H so code object, nên KHÔNG thấy lời gọi tới một BẢN SAO của helper hay lời gọi không đi qua profile của luồng: E1
  (`exec` mã nguồn của helper vào một dict rồi gọi), E2b (`types.FunctionType(code.replace(...))` dựng trong ca), E6b (bản
  sao như thế dựng ở cấp module), E3 (`_thread.start_new_thread`, luồng không qua `threading`), E4 (ca tự gọi
  `sys.setprofile(None)`), E5 (gọi helper trong tiến trình con) — mỗi đường tự bắt `BoQuaNen`, nên `t70` `1/1`, `t193`
  `1/1`, `t204` `1/1` dưới posix, và N, K, N − D, H − D không có `t204`, ở 3.11.15 lẫn 3.12.3. Các cách viết ấy trái (i),
  và vế H không thấy chúng. **Hướng đóng, review lượt 12 đo** (dụng cụ ở scratch của reviewer; cây `git archive ab457c6` cộng biến thể `t204_moi`, một lượt
  `--chi t204` mỗi bản Python; 3.11.15 và 3.12.3 cùng kết quả; `t70` `1/1`, `t193` `1/1`, `t204` `1/1` ở E1, E2b, E3, E4, E5, E5f, E6b, E7): H2 bắt E1, E2b, E3, E4, E6b (`t204` thuộc
  H2 − D, H − D rỗng); H2 không bắt E5 (tiến trình con) và E7 (lỗi trước guard; H bắt). Vế (S) trên 36 biến thể (26 của bộ phiên soạn lượt 10 và 11; E2b, E5d, E5f,
  E6b; sáu biến thể do reviewer dựng): ĐỎ ở 22: E1 đến E7 (cả E2, E6 của bộ phiên soạn lẫn E2b, E6b chạy được), E5d, M1 đến M3, N1 đến N3, N6, N9, N10 và ba biến thể của
  reviewer (tên chẻ ở dấu gạch dưới cuối `chay_buoc_`, docstring nhắc tên, chuỗi nhiều dòng gửi tiến trình con: biến thể cuối chỉ (S) bắt, vì tiến trình con không chịu hook);
  xanh ở 14: năm ca hợp lệ (M7, R11, R12, gán helper cho biến cục bộ, chú thích nhắc tên), bảy biến thể mà tên vẫn đứng như mã trong thân hàm (M5, M6, N4, N5, N7, N8, R13:
  K, N − D, H − D hay H2 − D bắt cả bảy), E5e (tên chẻ, gọi trong tiến trình hiện tại: H − D và H2 − D bắt) và E5f. Mỗi nhánh của (S) có biến
  thể riêng làm nó ĐỎ khi bị gỡ: bỏ (a) ⇒ 16 biến thể từ ĐỎ thành xanh, bỏ (b) ⇒ 6; hai tập rời nhau (16 + 6 = 22). Baseline H2 − D (clone đủ `ab457c6`, MỘT lệnh mỗi
  bản Python: 590,5 giây ở 3.11.15, 700,5 giây ở 3.12.3; 201 ca = 187 đạt + N 12 + K 2) bằng nhau ở cả hai bản: {`t71`, `t72`, `t73`, `t98`, `t193`, `t203`}.
  Còn lại sau H, H2 và (S): gọi helper trong tiến trình con bằng tên dựng từ mảnh không chứa `chay_buoc_` (E5f: `'_chay_' + 'buoc_dang_that'`): `t70`, `t193`,
  `t204` `1/1`, N, K, H − D, H2 − D rỗng, (S) xanh, ở cả hai bản Python; không vế nào thấy, khai là giới hạn và đọc diff vẫn cần.
  E5f là một HỌ, không phải một cách viết: mọi cách dựng tên helper mà KHÔNG giá trị chuỗi nào trong mã nguồn (hằng, tên, tên
  đối số, tên tham số…) chứa `chay_buoc_`, rồi gọi trong tiến trình con; (S) r13 thu hẹp họ ấy (E5g, E5i nay ĐỎ) mà không
  đóng được nó, vì không phép tĩnh nào đọc được chuỗi chỉ thành hình lúc chạy, còn tiến trình con nằm ngoài mọi hook. Ca mới dùng
  `_chay_main_meta` hay `_ca_gia` (như `t71`, `t72`, `t73`, `t98`) vào H2 − D vì ca giả ném `BoQuaNen`: handoff nêu ca nào, vì sao; không tự tính là đạt.
  **Họ E8 — BẢN SAO helper trong một module NẠP LẠI, cùng tiến trình (review lượt 13 đo; dụng cụ ở scratch của reviewer, cây
  `git archive ab457c6` tối thiểu như bộ phiên soạn, MỘT lệnh cho 3.11.15 và 3.12.3, hai bản cùng kết quả).** Ca `t204_moi` nạp lại
  chính tệp test thành một module MỚI rồi gọi helper của module ấy: E8a (`importlib.util.spec_from_file_location` cùng tệp, tên
  module khác, `exec_module`, gọi `m2._chay_buoc_dang_that(...)`; thêm `t204` vào `mong`), E8c (`exec` toàn bộ mã nguồn tệp, lệch
  một dòng, vào một dict mới, gọi qua `types.SimpleNamespace(**ns)._chay_buoc_dang_that`; thêm `t204` vào `mong`), E8d (như E8c,
  tên helper dựng từ mảnh, không sửa `mong`). Cả ba: `t70`, `t193`, `t204` `1/1` dưới posix; `quet13.py` của phiên soạn r13
  (`--chi t204`) không xếp `t204` vào N, K, N − D, H − D hay H2 − D; (S) r13 và (S) của HINT lượt 12 cùng xanh. Mà `main()` chạy
  như `__main__` dưới một mô phỏng `nt` lật `os.name` trong khung guard của MỌI bản sao ĐỎ (`BoQuaNen` của bản sao); đối chứng M7
  (helper gốc, có sổ) dưới cùng mô phỏng ra BỎ QUA. Cơ chế: seam chỉ vá MỘT dict module, nên guard của bản sao đọc `os.name` thật
  và dưới seam chạy như posix (không ném), còn trên Windows nó ném `BoQuaNen` của CHÍNH module bản sao, lớp mà `main()` của
  `__main__` không bắt; H, H2 so code object và lớp của module đã nạp; (S) cho phép `Attribute.attr` trong thân hàm. E8a, E8c có
  tên helper ở cấp đỉnh nên thuộc D: N − D, H − D, H2 − D mù theo cấu trúc, còn (q1), (q3) không thấy gì vì dưới seam ca đạt.
  E8b (`importlib.import_module("lease_publish_test")`) chỉ bị bắt (N có `t204`; (q1) ĐỎ khi quét đủ) vì bộ quét đăng ký đúng tên
  ấy trong `sys.modules`, điều chữ đặc tả không đòi. Họ E8 không thuộc E5f (không tiến trình con; tên helper có mặt nguyên văn)
  và có từ trước r13 (cùng xanh dưới (S) của HINT lượt 12). Vế lật `os.name` ở đoạn *Phép quét động* (bộ quét `quet13.py` thêm
  đúng phần ấy) đưa E8a, E8c, E8d và E8f (bản sao `exec` với guard ĐỔI TÊN, khớp nhờ bytecode) vào K (`BoQuaNen@<module bản
  sao>`, (q3) ĐỎ) ở cả hai bản; trên nền và trên 38 biến thể cũ (`--chi t204`) N, K, N − D, H − D, H2 − D giống hệt bộ quét
  không có vế ấy, năm ca hợp lệ không bị báo nhầm; quét ĐỦ nền (clone đầy đủ `ab457c6`, MỘT lệnh, hai bản song song):
  bản khoá theo tên và bản khoá theo tên hoặc bytecode cùng cho 201 ca = 187 đạt + N 12 + K 2,
  N bằng đúng sổ, đúng cặp, N − D rỗng, K = {`t199`, `t203`}, H − D = {`t193`}, H2 − D = {`t71`, `t72`, `t73`, `t98`, `t193`,
  `t203`}, giống hệt bộ quét theo chữ r13 chạy cùng cách (status 0 dòng, 0 `.pyc`).
  **Phiên soạn r14 đo lại vế lật** (dụng cụ viết riêng theo chữ đoạn *Phép quét động*, không dùng mã của reviewer:
  `quet14.py` là `quet13.py` của phiên soạn r13 cộng vế lật, N là `BoQuaNen` của module đã nạp, K ghi lớp kèm module, thêm
  `q1_chi` so N với sổ thu hẹp về các ca đã chạy; oracle `mo_phong_nt14.py` chạy tệp test như `__main__` và lật `os.name`
  trong khung guard khoá theo tên, bytecode hoặc cặp (tên tệp, dòng `def`), bằng `sys.monitoring` ở 3.12, bằng
  `sys.setprofile` cộng bọc `_thread.start_new_thread` ở 3.11; `chay14.py` chạy MỘT lệnh cho 3.11.15 và 3.12.3, hai luồng
  song song, 15:04:04Z–15:33:21Z 07-10, PATH có `~/.local/bin`, tối đa hai lượt quét động cùng lúc). Ma trận (cây tối thiểu như bộ phiên
  soạn r13; nền và 51 biến thể: 38 cũ, E8a–E8g của reviewer lượt 13, E8h–E8m mới; mỗi cây: `quet13.py` và `quet14.py`
  `--chi t204`, suite `--chi-ca=t70_`, `t193_`, `t204_`, (S) r13, oracle; trả nền 52/52 mỗi bản, 0 `.pyc`): suite, (S) r13
  và hai bộ quét cho cùng kết quả ở hai bản trên mọi hàng, trừ N5 (`t193` `0/1` ở 3.12, như A2); oracle cùng mã thoát ở hai
  bản trên mọi hàng, trừ E8l (dưới). Trên nền và 38 biến thể cũ, hai bộ quét cho cùng N, N − D, H − D,
  H2 − D và cùng tập TÊN của K; năm ca hợp lệ không bị báo nhầm. Mười ba biến thể họ E8 đều qua `t193`, `t204` (`1/1`) và
  (S) r13; `t70` `1/1` trừ E8m (tên helper chỉ nằm trong hàm lồng). Vế lật đưa vào K: E8a, E8c, E8d, E8f, E8i
  (`runpy.run_path`), E8j (bỏ mục `sys.modules` rồi nhập lại cùng tên; K ghi `BoQuaNen@lease_publish_test` của module
  mới), E8k (`types.ModuleType` cộng `exec` không lệch dòng), E8m (bản sao gọi trong `threading.Thread`); vào N, tức (q1)
  ĐỎ: E8b (`import_module` đúng tên bộ quét đăng ký) và E8h (`importlib.reload` module đã nạp, tại chỗ, nên `BoQuaNen` mới
  là lớp của chính module ấy). Không có vế lật, `quet13.py` chỉ thấy E8b (N) và E8m (H − D). Oracle ĐỎ ở cả mười ba biến
  thể ở 3.12; ở 3.11 ĐỎ ở mười hai, xanh ở E8l. Quét ĐỦ nền (clone đầy đủ từ `adg2`, `checkout --detach ab457c6`,
  `core.abbrev 7`, chạy từ gốc; `quet13.py` rồi `quet14.py` trên cùng clone): hai bộ quét cùng cho 201 ca = 187 đạt + N 12
  + K 2 ở cả hai bản; N bằng đúng sổ, đúng cặp; N − D rỗng; K = {`t199`, `t203`}; H − D = {`t193`}; H2 − D = {`t71`, `t72`, `t73`, `t98`, `t193`, `t203`};
  `quet13.py` 597,3 | 694,7 giây, `quet14.py` 562,9 | 660,6 giây (3.11.15 | 3.12.3); sau mỗi lượt `status --porcelain --ignored` 0 dòng và 0
  `.pyc`.
  **Review lượt 14 đo** (dụng cụ ở scratch của reviewer; cây tối thiểu như bộ phiên soạn; mỗi hàng chép đúng lệnh của
  `chay14.py`: `quet13.py` và `quet14.py` `--chi t204`, suite `--chi-ca=t70_`, `t193_`, `t204_`, (S) r13, oracle
  `mo_phong_nt14.py`; MỘT lệnh cho 3.11.15 và 3.12.3; trả nền đủ, 0 `.pyc`). E8n (bản sao gọi trong luồng thợ của
  `ThreadPoolExecutor` khởi động LÚC NẠP module; thêm `t204` vào `mong`) và E8n2 (luồng `threading.Thread` cộng hàng đợi,
  khởi động lúc nạp): `t70`, `t193`, `t204` `1/1`, (S) r13 xanh; `quet13.py` lẫn `quet14.py` không xếp `t204` vào N, K,
  N − D, H − D hay H2 − D, 0 lần lật, ở cả hai bản, lặp 5/5; oracle ĐỎ (`BoQuaNen` của bản sao) ở cả hai bản. Lý do:
  `threading.setprofile` chỉ áp cho luồng khởi động SAU lời gọi, mà bộ quét r14 cài nó sau khi nạp. Ca HỢP LỆ (đạt trên
  Windows thật vì `nen="posix"` tường minh): V1 (hai luồng, mỗi luồng gọi guard 150 lần) ⇒ với *"trả giá trị lúc vào khung"*,
  `os.name` kẹt `nt` sau ca ở cả hai bản và 3.11 K có `t204` (`NotImplementedError`), lặp 5/5; đặt ca ấy đầu `CA` rồi quét
  `--chi t000,t01_,t02,t03,t04,t05` ⇒ `quet14.py` 1/12 đạt, K 11, tức 9 ca nền chạy sau nó mà `quet13.py` cho đạt nay vào K
  (`NotImplementedError`); `quet13.py` 10/12 đạt, K 2 (hai ca `t01` `FileNotFoundError`, tạo tác của cây tối thiểu, có ở cả
  hai bộ quét), ở cả hai bản; V6 (luồng nền dựng `Path` trong lúc luồng chính gọi
  guard) ⇒ `quet14.py` K có `t204` ở cả hai bản (5/5), `quet13.py` không; oracle cũng ĐỎ ở V6 vì nó lật `os.name` toàn tiến
  trình như bộ quét. Bộ quét đề xuất (`quet14.py` cộng ba thay đổi ở đoạn *Phép quét động*: cài `threading.setprofile` trước
  khi nạp, đếm độ sâu, trả giá trị gốc sau mỗi ca), chạy cùng lệnh với `quet14.py` (`--chi t204`) trên nền, 38 biến thể cũ,
  13 biến thể E8 và tám biến thể của lượt 14: khác `quet14.py` đúng ba hàng — E8n, E8n2 vào K (`BoQuaNen@ban_sao_204`); V1
  đạt, `os.name` không lệch — ở cả hai bản; kịch bản V1 đầu `CA` cho 10/12 đạt, K 2, như `quet13.py`; V6 vẫn vào K (tạo tác
  toàn tiến trình, khai ở đoạn *Phép quét động*). Quét ĐỦ nền (clone đầy đủ `ab457c6`, `quet14.py` rồi bộ đề xuất trên cùng
  clone, MỘT lệnh mỗi bản): hai bộ quét cùng cho 201 ca = 187 đạt + N 12 + K 2 ở cả hai bản; N bằng đúng sổ, đúng cặp; N − D rỗng; K = {`t199`, `t203`}; H − D = {`t193`}; H2 − D = {`t71`, `t72`, `t73`, `t98`, `t193`, `t203`}; L rỗng; 118 lần lật mỗi lượt; `quet14.py` 695,1 | 977,0 giây, bộ đề xuất 788,1 | 762,9 giây (3.11.15 | 3.12.3; 16:18:22Z–16:52:24Z 07-10, máy chung); sau mỗi lượt `status --porcelain --ignored` 0 dòng và 0 `.pyc`. Cùng lượt: E8q (ca thay hàm profile bằng một hàm khác
  `None` rồi gọi bản sao) lọt mọi cổng ở cả hai bản, oracle `sys.monitoring` ĐỎ ở 3.12; E8p (bản sao nhập `os` qua
  `__import__` riêng, đọc ảnh `os.name` chụp lúc dựng) lọt mọi cổng ở cả hai bản dù có một lần lật, và oracle cũng mù
  (lật module `os` thật) nên kết cục Windows `KHÔNG ĐO ĐƯỢC`; E8w (module `profile`) vào K ở cả hai bản vì `AssertionError` của
  chính module `profile` dưới hàm profile của bộ quét, không phải nhờ vế lật; E8w2 (`cProfile`) lọt ở 3.11 (`cProfile` thay
  hàm của `sys.setprofile`, rồi để `None` sau `disable`), vào K ở 3.12 (`sys.getprofile()` vẫn là hàm cũ trong lúc
  `cProfile` bật); V7 (bản sao chỉ đọc hằng) không bị báo nhầm.
  **Phiên soạn r15 đo lại** (`chay15.py` ở scratch: MỘT lệnh cho 3.11.15 và 3.12.3, hai luồng song song, 17:17:58Z–18:15:07Z 07-10;
  `quet14.py` của phiên soạn r14 rồi `quet14b.py` của reviewer lượt 14, chép nguyên byte, liền nhau trên cùng cây; cây tối
  thiểu như bộ phiên soạn r13; nền và 68 biến thể: 38 cũ, E8a–E8m, tám của lượt 14 và E8p dựng lại bằng script của reviewer
  (khớp từng byte, §10), tám mới dưới; mỗi cây: hai bộ quét `--chi t204`, suite `--chi-ca=t70_`, `t193_`, `t204_`, (S) r13,
  oracle; trả nền 69/69 mỗi bản, 0 `.pyc`). Trên nền và 51 biến thể chung với phiên soạn r14, suite, (S) r13, oracle và
  `quet14.py` trùng từng hàng với hiện vật r14; trên 60 hàng của lượt 14, `quet14b.py` khác `quet14.py` đúng ba hàng như đoạn
  trên, ở cả hai bản, L rỗng và `os.name` không lệch sau lượt ở cả 60; ca hợp lệ (nền, năm ca của r13, V1, V7) không bị
  `quet14b.py` báo, V6 vào K như đã khai; lặp 5 lần (`--chi t204`, ba bộ quét) E8n, E8n2, V1, V6
  cho đúng kết cục đoạn trên ở 5/5 mỗi bản. Năm biến thể mới cùng cơ chế E8n (bản sao chạy trong ngữ cảnh dựng lúc nạp hay
  ngoài khung ca; `t70`, `t193`, `t204` `1/1`, (S) r13 xanh, oracle ĐỎ, ở cả hai bản): E8r (task `asyncio` tạo lúc nạp, vòng
  sự kiện trong luồng `threading` khởi động lúc nạp) vào K với `quet14b.py`, lọt `quet14.py`; E8s (bộ xử lý tín hiệu đăng ký
  lúc nạp) và E8t (`__del__` của đối tượng tạo lúc nạp) vào K với cả hai bộ quét, vì chạy trên luồng chính trong khung ca;
  E8u (ca đăng ký `atexit` gọi bản sao, `os._exit(1)` khi bị ném; oracle ĐỎ bằng mã thoát) và E8v (bản sao gọi ngay lúc nạp
  module) lọt cả hai, thuộc (α). Ca hợp lệ mới: V8 (luồng nền ở lại trong guard khi ca kết thúc) ⇒ `quet14b.py` L = {`t204`}
  và `os.name` về giá trị gốc, `quet14.py` để `os.name` lệch; đặt đầu `CA` (`--chi t000,t01_,t02,t03,t04,t05`) ⇒
  `quet14b.py` 10/12 đạt, L = {`t000`}, `quet14.py` 1/12, `quet13.py` 10/12; V9 (ca tự vá `os.name` thành `nt` quanh lời gọi
  guard rồi đọc nó) ⇒ `quet14b.py` K có `t204` (`TinHieuChotCa`), `quet14.py` không, ở cả hai bản; V10 (luồng nền khởi động
  lúc nạp gọi guard với `nen="posix"`) ⇒ `quet14b.py` L = {`t204`} ở cả hai bản, K có `t204` ở 3.11; cùng sáu tiền tố
  trên (11 ca): `quet14b.py` L có 8 | 11 ca, K thêm 0 | 1 ca (phụ thuộc lịch luồng); `quet14.py`, `quet13.py` 9/11
  đạt, K chỉ hai ca `t01` `FileNotFoundError` của cây tối thiểu (như kịch bản V1), không lật lần nào. Quét ĐỦ nền
  (clone đầy đủ từ `adg2`, `checkout --detach ab457c6`, `core.abbrev 7`, chạy từ gốc; `quet14.py` rồi `quet14b.py` trên cùng
  clone): hai bộ quét cùng cho 201 ca = 187 đạt + N 12 + K 2 ở cả hai bản; N bằng đúng sổ, đúng cặp; N − D rỗng; K =
  {`t199`, `t203`}; H − D = {`t193`}; H2 − D = {`t71`, `t72`, `t73`, `t98`, `t193`, `t203`}; L rỗng; 118 lần lật mỗi lượt; `os.name` không lệch; `quet14.py`
  1167,3 | 1749,0 giây, `quet14b.py` 1066,0 | 790,4 giây (3.11.15 | 3.12.3; máy chung); sau mỗi lượt `status --porcelain --ignored` 0 dòng và 0 `.pyc`.
  Còn lại, khai là giới hạn THEO TÍNH CHẤT (lọt mọi cổng kể cả vế lật; một biến thể mới thuộc một nhóm dưới đây là trong
  giới hạn đã khai, không phải lỗ mới): (α) khung guard của bản sao chạy lúc hàm profile của bộ quét không hoạt động trên
  luồng của nó: trước khi nạp xong, ở mọi luồng (E8v); ngoài khung một ca trên luồng chính (E8u, lúc thoát); trên luồng
  không mang hàm ấy (E8e, `_thread` thô; oracle ĐỎ ở hai bản); hay sau khi ca thay hoặc tắt hàm ấy (E8l
  `sys.setprofile(None)`, E8q; oracle `sys.monitoring` ĐỎ ở 3.12); (β) guard của bản sao không khớp tên lẫn bytecode (E8g; review lượt 13 ghi kết
  cục Windows `KHÔNG ĐO ĐƯỢC`, oracle khoá thêm theo dòng `def` ra ĐỎ ở hai bản), hay không đọc `os.name` của chính module
  `os` trong khung guard ấy (E8p); (γ) tiến trình con (E5f). Vế lật vì vậy THU HẸP họ E8, không đóng nó; oracle là mô
  phỏng, Windows thật `KHÔNG ĐO ĐƯỢC` ở đây. Handoff liệt kê mọi chỗ MỚI trong ca mới hoặc đã sửa mà nạp hay dựng mã lúc
  chạy, đổi hàm profile, hay cho mã chạy ngoài khung ca trên luồng chính hoặc ngoài luồng ấy (mã cấp module chạy lúc nạp,
  mã đăng ký chạy về sau, luồng, tiến trình con), kèm lời gọi cụ thể (đã gặp: `exec`, `eval`, `compile`, `importlib`,
  `runpy`, `__import__`, `types.FunctionType`, `_thread`, `threading`, `asyncio`, `signal`, `atexit`, `sys.setprofile`,
  `profile`, `cProfile`, `subprocess`), để đọc diff (không phải cổng tự động).
  **Phiên soạn r13 đo lại** (dụng cụ viết riêng theo chữ đoạn này, không dùng mã của reviewer: `quet13.py` cho đạt, N, K,
  H, H2, D; `s13.py` cho (S) theo luật ở trên; `chay26_13.py` chạy MỘT lệnh cho cả hai bản Python, hai luồng song song, mỗi
  bản một cây `git archive ab457c6` (`.github`, `ops/*.py`) riêng, chép đè `ops/lease_publish_test.py` từng biến thể rồi trả
  nền và kiểm sha256; 12:34:59Z–12:38:43Z 07-10; trả nền đúng 39/39 mỗi bản, 0 tệp `.pyc`). 38 biến thể: 26 của bộ phiên
  soạn, 10 của reviewer lượt 12 (E2b, E5d, E5f, E6b và sáu `bt2`, áp `patch --fuzz=0` lên blob `7dd06ab`), và hai biến thể
  mới cùng cơ chế E5f: E5g lấy tên helper từ tên đối số từ khoá (`next(iter(dict(_chay_buoc_dang_that=0)))`), E5i từ tên
  tham số của một lambda (`co_varnames[0]`), cả hai rồi gọi helper trong tiến trình con. Mỗi biến thể ở mỗi bản: `quet13.py
  --chi t204`, suite `--chi-ca=t70_`, `t193_`, `t204_`, (S) của HINT lượt 12 (tệp `quet_s_ast.py` của reviewer) và (S) r13.
  3.11.15 và 3.12.3 cùng kết quả ở mọi biến thể trừ N5 (`t193` `0/1` ở 3.12, như A2). H2 bắt E1, E2b, E3, E4, E6b (và mọi
  biến thể có lời gọi helper trong tiến trình hiện tại mà guard chạy tới), không bắt E5, E5d, E5f, E5g, E5i (tiến trình con)
  và E7 (H bắt). (S) của HINT tái lập đúng số của reviewer (26 biến thể: động và (S) cùng bắt 15, chỉ động 7, chỉ (S) 1,
  không cổng nào 0; 36 biến thể cũ: ĐỎ 22), nhưng để lọt E5g và E5i: `t70`, `t193`, `t204` `1/1`, N, K, H − D, H2 − D rỗng,
  (S) của HINT xanh, ở cả hai bản; tức với (S) của HINT có BA biến thể không cổng nào thấy (E5f, E5g, E5i). (S) của HINT còn
  lệch chính chữ của nó ở N7 (`def t204_moi(h=_chay_buoc_dang_that):`, giá trị mặc định của một hàm cấp module, mà (b) nói
  là ĐỎ): công cụ cho xanh, vì nó so nút con trực tiếp của `FunctionDef` với các biểu thức mặc định, mà biểu thức mặc định
  nằm dưới nút `arguments`, nên phép so không bao giờ khớp. (S) r13: ĐỎ 25/38; xanh 13 = năm ca hợp lệ (M7, R11, R12, L1,
  E5c), bảy biến thể mà tên đứng như mã trong thân hàm (M5, M6, N4, N5, N8, R13, E5e: K, N − D, H − D hay H2 − D bắt cả
  bảy) và E5f. Phủ chéo trên 26 biến thể của bộ phiên soạn: động và (S) cùng bắt 16, chỉ động 6, chỉ (S) 1 (E5), không cổng
  nào 0, ba ca hợp lệ không cổng nào báo nhầm; trên 38: 19, 7, 6 (E5, E5d, E5g, E5i, E5k, E5m), 1 (E5f), năm ca hợp lệ báo
  nhầm 0. Đột biến của chính (S) r13 (mỗi cái thay đúng một chuỗi trong `s13.py`; 3.11, 3.12, 3.13 cùng kết quả): bỏ điều
  kiện loại nút (mọi lần trong thân hàm đều được phép) ⇒ 18 biến thể từ ĐỎ thành xanh; bỏ điều kiện thân hàm ⇒ 7; hai tập
  rời nhau (18 + 7 = 25); lùi về danh sách loại nút của HINT (`Constant`, `Name`, `Attribute`, `alias`, tên hàm, tên lớp) ⇒
  2 (E5g, E5i); tính giá trị mặc định như thân hàm (lỗi của công cụ HINT) ⇒ 1 (N7); không đột biến nào làm ca hợp lệ ĐỎ.
  Baseline đủ trên hai clone đầy đủ `ab457c6` (`quet13.py`, MỘT lệnh cho hai bản, song song; chạy từ gốc, `python` trỏ đúng
  bản, `PYTHONDONTWRITEBYTECODE=1`; 13:00:36Z–13:11:45Z 07-10; sau quét `status --porcelain --ignored` 0 dòng và 0 `.pyc` ở
  cả hai clone): 201 ca = 187 đạt + N 12 + K 2 ở cả hai bản; N bằng đúng sổ, đúng cặp (q1); N − D rỗng; K = {`t199`,
  `t203`}; H − D = {`t193`}; H2 − D = {`t71`, `t72`, `t73`, `t98`, `t193`, `t203`}; 560,1 giây ở 3.11.15, 668,8 giây ở
  3.12.3. Khớp số của review lượt 12. Lượt đầu cùng lệnh (12:50:18Z–12:59:53Z) chạy với PATH thiếu `~/.local/bin` (nơi có
  `actionlint`): K có thêm `t33`, `t137`, `t159` (`AssertionError`, `TinHieuChotCa`), còn N, H − D, H2 − D không đổi; chạy
  lại riêng ba ca ấy với PATH đủ thì cả ba đạt. Vậy K phụ thuộc cả PATH, không chỉ kiểu cây: nền và ứng viên phải quét với
  cùng môi trường, như (q3) đã đòi, và handoff ghi PATH.
  Số đo của phiên soạn r11 trên `163fd5d` (chi tiết ở §10, gạch *Tương tác với #687*): trên nền, N bằng đúng 12 ca của sổ, đúng cặp, N − D rỗng, ở
  3.11.15 và 3.12.3; K là 2 ca (`t199`, `t203`, hai ca mà seam ép `nt` vào chỗ chúng tự đo nền posix) khi phép quét đặt
  `ops/` đầu `sys.path`, và là 11 ca khi thiếu dòng ấy (thêm 9 ca `import bash_nen` ném `ModuleNotFoundError`); review
  lượt 10 ghi 18 ca ở môi trường của họ. Một lượt quét đủ mất 419,9 giây khi chạy một mình (3.12.3) và tới 687,2 giây khi bốn lượt chạy
  song song (review lượt 10: 382,5 giây ở 3.12.3). Biến thể (ca `t204` chèn trước `def main(`): mọi đường gọi lạ (tám đường của lượt 10 và ba
  đường phiên soạn r11 thêm) vào N − D = `{t204}` ở cả hai bản; hai đường làm `BoQuaNen` không ra khỏi thân ca (M5 gọi
  trong luồng khác, M6 đổi kiểu ngoại lệ) qua (q1), (q2) mà (q3) bắt; ca làm đúng (M7; R12 tự bắt) không bị bắt nhầm.
  **Vì sao giữ làm tiêu chí nghiệm thu, không thành ca test mới trong write set** (lựa chọn của phiên soạn r11, theo câu
  hỏi của phiên điều phối): (1) chi phí và tương tác với `t125`: phép quét chạy lại MỌI ca, nên một lượt quét đủ mất
  gần bằng một lượt suite (đo dưới); thành một `@ca` thì nó chạy cả bên trong hai tiến trình con mà `t125` dựng để chạy
  lại toàn suite, dưới trần thời gian dẫn xuất (`AB_HAN_GIAY`, `t156` chặn hai đầu), nên thời gian suite tăng nhiều lần
  và `t125` có thể vượt trần (suy luận từ cấu trúc, chưa dựng thử); (2) phạm vi: đó là một chốt kiểm kê thứ ba chồng lên
  thiết kế kiểm kê của #677 (`t70`) và #687 (`t193`); thêm nó vào suite (và giữ hay bỏ ứng viên tĩnh của `t193`) là
  quyết định của packet sở hữu kiểm kê ấy, không thuộc objective của packet này; (3) nghĩa vụ (i)–(iii) chỉ áp cho ca mới
  hoặc đã sửa của lượt thi hành này, các ca ấy đóng băng lúc land, nên một lần quét đủ trên ứng viên cuối, ghi vào
  handoff và được reviewer chạy lại, phủ hết chúng; (4) tiền lệ: #687 đo sổ bằng một phép quét mọi ca NGOÀI suite
  (docstring `t193`), đúng M2 của đặc tả #687 r3. Cái giá, nói thẳng: sau land, một packet khác thêm ca gọi helper qua
  đường lạ, hay làm `BoQuaNen` không ra khỏi thân ca, thì không cổng nào trong suite bắt. Lỗ ấy của `t193` (ứng viên
  tĩnh; bỏ qua ngoại lệ khác) là phát hiện ngoài spec: executor ghi vào handoff để mở packet riêng, không vá trong
  write set này.
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
  `origin/master` `89fc4fa` (đọc và chạy lại 10:49Z; blob giống hệt trên `20ec8d5` và `163fd5d`, sha256 `dd17b94c…4f83`,
  nên mọi số dòng dưới giữ nguyên; trên `ab457c6` các hàm ấy giống hệt thân, dời +159: `_danh_sach_thay_the_cho`
  :720–731, `_bia_mo_doi_xung` :734–756, nhánh `KHÔNG_XÁC_ĐỊNH` :2271–2278):
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
**r10 dời nền sang `163fd5d` và đo lại nền, ref, người giữ, suite (3.11 và 3.12), kích thước và ruff** (09:15Z–10:01Z
01-10, `adg2` sau `fetch --prune` và hai clone sạch của nó; ref và người giữ bằng chuỗi lệnh đo điều kiện cấp), ghi
trước số r9/r8 ở từng gạch. Số đo trên `20ec8d5` giữ dưới nhãn lịch sử.
**r11 giữ nền `163fd5d` và đo lại nền, ref, người giữ bằng chuỗi lệnh r11** (11:04Z–11:23Z 01-10, `adg2`), ghi trước
số r10 ở ba gạch ấy. Suite, kích thước và ruff không đo lại (hai tệp write set giống hệt nền); số giữ từ r10, và review
lượt 10 đã tái lập (suite 198/198 dưới 3.11.15 và 3.12.3 trên `163fd5d`, 198/198 dưới 3.12.3 trên `7e5958e`; ruff 9
lỗi F cùng tập ở `20ec8d5`, `163fd5d`, `7e5958e`).
**r12 dời nền sang `ab457c6` và đo lại nền, ref, người giữ (chuỗi lệnh r12), suite (3.11 và 3.12), kích thước, ruff**
(08:2xZ–09:2xZ 07-10, `adg2` sau `fetch --prune` và hai clone sạch của nó), ghi trước số r11/r10 ở từng gạch. Số đo
trên `163fd5d` giữ dưới nhãn lịch sử.
**r13 giữ nền `ab457c6` và đo lại nền, ref, người giữ bằng chuỗi lệnh r13** (12:06Z–13:13Z 07-10, `adg2`), ghi trước số r12
ở ba gạch ấy. Suite, kích thước và ruff không đo lại (hai tệp write set giống hệt nền); số giữ từ r12, và review lượt 12 đã
tái lập (suite 201/201 dưới 3.11.15 và 3.12.3, ruff 11 lỗi F, kích thước, trên `ab457c6`).
**r15 giữ nền `ab457c6`** (REST `master` 17:18:24Z 07-10; `adg2` chỉ đọc, `FETCH_HEAD` 17:17:01Z). r15 không chạy lại
chuỗi lệnh (khối và `s5.py` không đổi byte), nên ref và người giữ dưới đây vẫn là số r13; suite, kích thước, ruff vẫn là số r12.
**r14 giữ nền `ab457c6`** (`adg2` sau `fetch --prune` và `merge --ff-only`, 15:16:37Z–15:16:38Z 07-10). r14 không chạy lại
chuỗi lệnh (khối và `s5.py` không đổi byte), nên ref và người giữ dưới đây vẫn là số r13; suite, kích thước, ruff vẫn là số r12.

- **Nền.** r15: lúc 17:18:24Z 07-10 REST `master` = `ab457c6`; `adg2` (`FETCH_HEAD` 17:17:01Z) `git diff --quiet ab457c6…
  refs/remotes/origin/master -- <hai tệp>` rc=0; nền giữ `ab457c6`. r14: lúc 15:16:38Z 07-10 `origin/master` = `ab457c6`, `git diff --quiet ab457c6… refs/remotes/origin/master --
  <hai tệp>` rc=0; nền giữ `ab457c6`. r13: lúc 12:06:45Z và 13:12Z 07-10 `origin/master` = `ab457c6`; `git diff --quiet ab457c6…
  refs/remotes/origin/master -- <hai tệp>` rc=0 (13:13Z, bước (v) của chuỗi); nền giữ `ab457c6`.
  r12: lúc 08:2xZ 07-10 `origin/master` = `ab457c6` (merge PR #712, wp709 land); `git diff --numstat 163fd5d
  ab457c6 -- <hai tệp>` ⇒ `161 1` và `372 12`; `git diff --quiet 163fd5d… refs/remotes/origin/master -- <hai tệp>` rc=1
  (09:27:22Z), tức điều kiện (4) với nền cũ, nên r12 **dời** nền nghiệm thu sang
  `ab457c6` (hàng nền nghiệm thu); lúc 09:08Z `diff --quiet ab457c6… refs/remotes/origin/master -- <hai tệp>` rc=0.
  r11: lúc 11:04:56Z 01-10 `origin/master` = `7e5958e` (merge PR #703), `git diff --quiet 163fd5d…
  refs/remotes/origin/master -- <hai tệp>` rc=0 và `git ls-tree` hai tệp ra cùng hai dòng ở hai rev; nền giữ `163fd5d`.
  r10: lúc 09:15:49Z 01-10 `origin/master` = `163fd5d` (merge PR #701, #687 land) và `git diff --quiet
  20ec8d5 origin/master -- <hai tệp>` **rc=1** (09:18:38Z; `ops/lease_publish.py` rc=0, `ops/lease_publish_test.py`
  `482 63`), nên r10 **dời** nền nghiệm thu sang `163fd5d` (hàng nền nghiệm thu). Lúc 09:45:15Z `origin/master` =
  `a6de9d1` (hai PR bookkeeping), `git diff --quiet 163fd5d origin/master -- <hai tệp>` rc=0 (09:45:39Z), nền giữ
  `163fd5d`. r9 (05:17:33Z 01-10): `origin/master` = `20ec8d5`; `git diff --quiet 20ec8d5 origin/master -- <hai tệp>`
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
- **Ref.** r13 (`adg2`, chuỗi lệnh r13, 13:12:13Z–13:13:11Z 07-10): `may_chu.raw` = `mc` = `chung` = 472 dòng, `thieu` 0,
  dòng `master` có trong phần chung, ở cả (iii) lẫn (vii); `thua` 1 dòng (`refs/heads/HEAD`); endpoint
  `https://github.com/ducthangho/tra-luat`; `--is-shallow-repository` ⇒ `false`; `for-each-ref refs/remotes/origin` 473
  ref (gồm `origin/HEAD`). r12 (`adg2`, chuỗi lệnh r12, 09:07:36Z–09:08:28Z 07-10): `may_chu.raw` = `mc` = `chung` = 470 dòng, `thieu` 0,
  dòng `master` có trong phần chung, ở cả (iii) lẫn (vii); `thua` 1 dòng (`refs/heads/HEAD` sinh từ `origin/HEAD`);
  endpoint `https://github.com/ducthangho/tra-luat`; `--is-shallow-repository` ⇒ `false`; `for-each-ref
  refs/remotes/origin` 471 ref (gồm `origin/HEAD`). r11 (`adg2`, chuỗi lệnh r11, 11:22:06Z–11:22:53Z 01-10): `may_chu.raw` = `mc` = `chung` = 456 dòng,
  `thieu` 0, dòng `master` có trong phần chung, ở cả (iii) lẫn (vii); endpoint `https://github.com/ducthangho/tra-luat`;
  `--is-shallow-repository` ⇒ `false`. r10 (`adg2`, bước (iii) và (vii) của chuỗi lệnh, hai lượt 09:18:19Z/09:18:38Z và 09:45:17Z/09:45:40Z 01-10):
  462/462 tên, lệch tên 0 dòng cả hai chiều, lệch cặp tên + OID 0 dòng cả hai chiều ở cả bốn lần; `refs/replace` 0
  ref, `refs/heads` 1 ref, `--is-shallow-repository` ⇒ `false` (09:18:38Z và 09:45:40Z). r9 (05:17:40Z–05:17:41Z 01-10, `adg2`): 461/461 tên, lệch tên 0 dòng cả hai chiều, lệch tên + OID 0 dòng;
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
- **Người giữ.** r13, `adg2` (13:12Z–13:13Z 07-10, chuỗi lệnh r13): `ops/lease_publish.py` và `ops/lease_publish_test.py`
  cùng `NGƯỜI_GIỮ 0: không có`, rc=0, 0 dòng `CÒN_HẠN`, ở `ai-dang-giu` lẫn `s5.py` r13 (0 dòng `KHÔNG_DIỄN_GIẢI`); hai lease
  wp709 ở nhãn `HẾT_HẠN` ⇒ điều kiện (1) đạt tại lúc đo (hàng `depends_on`). Lúc 12:18Z có 6 cặp lease `CÒN_HẠN` trên 473
  ref (wp685, wp710), không cặp nào chạm hai tệp (§ *Chuỗi lệnh*, đoạn danh sách cho phép). r12, `adg2` (09:07Z–09:08Z 07-10, chuỗi lệnh r12): `ops/lease_publish.py` và `ops/lease_publish_test.py`
  cùng `NGƯỜI_GIỮ 1: wp709-exec-g2-codex-20261006`, **rc=11**, ở `ai-dang-giu` lẫn `s5.py` (packet #709, đã land qua
  PR #712; hạn `2026-10-07T10:30:00Z`) ⇒ điều kiện (1) chưa thoả (hàng `depends_on`). r11, `adg2` (11:22Z 01-10, chuỗi
  lệnh r11): `ops/lease_publish.py` `NGƯỜI_GIỮ 0`, rc=0;
  `ops/lease_publish_test.py` `NGƯỜI_GIỮ 1: no-ton-677-687-r1-g1-claude`, **rc=11** (packet #704, hạn
  `2026-10-02T09:55:00Z`) ⇒ điều kiện (1) chưa thoả (hàng `depends_on`). r10, `adg2`: lượt 09:45:28Z–09:45:39Z 01-10 (`origin/master` = `a6de9d1`): cả hai tệp `NGƯỜI_GIỮ 0`,
  rc=0, 0 dòng `CÒN_HẠN`; lượt 09:18:19Z–09:18:38Z (`origin/master` = `163fd5d`): `ops/lease_publish.py` `NGƯỜI_GIỮ 0`,
  rc=0, `ops/lease_publish_test.py` `NGƯỜI_GIỮ 1: lease-publish-windows-do-r3-g3-claude`, **rc=11**, dòng `CÒN_HẠN` duy
  nhất là bản trên `refs/heads/master` (hạn `2026-10-02T01:12:00Z`), bản rút hạn về 05:55Z khi ấy chưa vào master. Dữ
  kiện lúc soạn, không phải lời khai điều kiện (1) thoả (hàng `depends_on`). r9 (05:17:46Z–05:18:07Z 01-10, `adg2`): `ops/lease_publish.py` `NGƯỜI_GIỮ 0`, rc=0;
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
  `PYTHONDONTWRITEBYTECODE=1`; script ở scratch, không vào kho; trên `ab457c6` hai hàm giống hệt thân, so `ast`).
  `_danh_sach_thay_the_cho`: `None`,
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
- **Suite.** Nền hiện tại (`ab457c6`, r12): **201/201** dưới 3.11.15 (08:27:32Z–08:34:16Z 07-10) và **201/201** dưới
  3.12.3 (08:27:32Z–08:35:00Z, song song), rc=0, bỏ qua 0 (chi tiết ở A8). Lịch sử `163fd5d` (r10): **198/198** dưới 3.11.15 (09:46:39Z–09:53:20Z 01-10) và **198/198** dưới
  3.12.3 (09:53:20Z–10:00:41Z), rc=0, bỏ qua 0 (chi tiết ở A8). Lịch sử `20ec8d5` (r8): **195/195**, rc=0, bỏ qua 0,
  01:11:15Z–01:16:50Z 01-10; cùng một lệnh, vế `89fc4fa`: **187/187**, rc=0, bỏ qua 0, 01:06:03Z–01:11:15Z. Lịch sử `89fc4fa`: **187/187**, rc=0,
  bỏ qua 0, đo 08:0xZ 29-09 trên commit merge
  `589336f` (cây `89fc4fa` + tệp spec), `PYTHONDONTWRITEBYTECODE=1 python ops/lease_publish_test.py`
  với `shellcheck` 0.9.0 + `actionlint` 1.7.7. Không đo lại ở r4, r5 và r6 (hai tệp Python giống hệt
  `origin/master`, `git diff --quiet` rc=0 lúc 10:49Z, xem mục **Nền**). Reviewer lượt 7 tự đo 187/187, rc=0, bỏ
  qua 0 trên cả `89fc4fa` lẫn `423b4ba` (VERDICT lượt 7, hướng 9, 13:15Z–13:26Z 30-09). Reviewer lượt 4 tự đo
  187/187, rc=0, bỏ qua 0 (VERDICT lượt 4, không ghi UTC riêng cho phép đo này); reviewer lượt 5 tự đo
  187/187, rc=0, bỏ qua 0 (VERDICT lượt 5, `verify.py` 10:42:51Z).
  Lịch sử trên `1741e0a`: r1 khai 185/187 lúc container thiếu `shellcheck` (`t137`, `t159` báo
  `KHÔNG ĐO ĐƯỢC: thiếu shellcheck`); lượt 1 đo 187/187.
- **Kích thước.** r12 (07-10, `git show <nền>:<tệp> | wc -l`, `grep -c '^@ca'`): `ops/lease_publish.py` **2366** dòng
  trên `ab457c6`; `ops/lease_publish_test.py` **11866** dòng, **201** ca, số ca lớn nhất vẫn `t203` (wp709 thêm ba ca
  tiền tố `t01`). r10 (09:5xZ 01-10, cùng hai lệnh): `ops/lease_publish.py` 2206 dòng trên `163fd5d`;
  `ops/lease_publish_test.py` **11506** dòng, **198** ca, số ca lớn nhất `t203` (nay có `t193`, `t194`, `t203` của #687).
  r8 (01-10, `git show <nền>:<tệp> | wc -l`, `grep -c '^@ca'`): `ops/lease_publish.py` 2206 dòng ở
  cả `89fc4fa` và `20ec8d5`; `ops/lease_publish_test.py` **11087** dòng, **195** ca, số ca lớn nhất `t202` trên
  `20ec8d5` (không có `t193`, `t194`), so 10502 dòng, 187 ca, `t192` trên `89fc4fa`. Lịch sử (đo lại 10:51Z 29-09, kết
  quả bằng số đo 10:14Z): 2206 / 10502 trên `89fc4fa`; 10508 trên `1741e0a`.
- **Ruff.** r12 (08:35:22Z 07-10, cây `git show` tối thiểu của mỗi nền, `ruff check --no-cache --select F`, nhị phân
  ruff 0.15.8): rc=1, **9** lỗi ở `163fd5d` (7 `F401`, 2 `F541`, đều trong `ops/lease_publish_test.py`) và **11** ở
  `ab457c6`: 9 lỗi ấy (cùng tập, bỏ số dòng) cộng 2 `F841` ở `ops/lease_publish.py` :198–199 (`executor_surface`,
  `executor_transport`, biến gán mà không dùng trong `_kiem_provider_identity` của wp709). Nền cho "delta F = 0" của A8
  nay là 11 lỗi trên `ab457c6`; hai `F841` ngoài objective, executor không sửa. r10 (09:55:39Z 01-10, cây `git archive` tối thiểu của mỗi nền, cùng lệnh dưới): rc=1, **9** lỗi ở cả
  `20ec8d5` lẫn `163fd5d` (7 `F401`, 2 `F541`, đều trong `ops/lease_publish_test.py`; `ops/lease_publish.py` 0), tập lỗi
  bỏ số dòng giống nhau ⇒ #687 thêm 0 lỗi F; nền cho "delta F = 0" của A8 nay là 9 lỗi trên `163fd5d`. r8 (01:20:42Z 01-10): `python -m ruff` vắng (`No module named ruff`), nhưng có nhị phân `ruff` 0.15.8.
  `ruff check --no-cache --select F ops/lease_publish.py ops/lease_publish_test.py`, chạy trên cả hai vế của A8:
  rc=1, **9** lỗi ở cả `89fc4fa` lẫn `20ec8d5` (7 `F401`, 2 `F541`, đều trong `ops/lease_publish_test.py`;
  `ops/lease_publish.py` 0), và tập lỗi (bỏ số dòng) giống nhau ⇒ #677 thêm 0 lỗi F. Đây là nền cho "delta F = 0" của
  A8 khi nền là `20ec8d5`. Lịch sử: `KHÔNG ĐO ĐƯỢC` ở phiên soạn r1–r7 (module vắng trong sandbox).

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
(VERDICT lượt 8, đối chiếu lượt trước). Một chuyển tiếp <50% CHƯA là điểm dừng theo tỷ lệ: §12 :1047–1048 đòi HAI
chuyển tiếp liên tiếp <50%, và 7→8 là tỷ lệ xác định đầu tiên (6→7 là `N/A`; :1046–1047 cấm ghép hai tỷ lệ thấp qua `N/A`),
nên điểm dừng theo tỷ lệ được quyết ở chuyển tiếp 8→9, tức lượt review của r9. Thứ đã kích hoạt (từ lượt 7, còn ở lượt 8) là luật một
lớp ở ba lượt (:1054–1056; `hop-dong-dong-bang-thieu-neo` ở lượt 1, 2, 7, 8), đòi xem lại cách làm tại checkpoint; câu
hỏi *"lượt
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

**Bộ đếm hình dạng sau lượt 9, điều kiện dừng §12, và cách r10 xử lý.** Lượt 9 (trên r9) ra 0 P1 / 2 P2 / 2 P3, bốn
lớp: `thu-tu-677-bo-ngo-o-dieu-kien-cap` (P2, VÁ SINH LỖI MỚI, có mặt ở lượt **7, 8 và 9**),
`tuong-tac-677-kiem-ke-t70-chua-neu` (P2, VÁ SINH LỖI MỚI, lượt 8 và 9), `hop-dong-dong-bang-thieu-neo` (P3, VÁ SINH LỖI
MỚI, lượt **1, 2, 7, 8 và 9**) và `dieu-kien-dung-12-doc-mot-chuyen-tiep` (P3, MỚI). Đọc đúng §12 (:1043–1049): tỷ lệ
của một chuyển tiếp là số lớp ĐÃ VÁ THẬT trên số lớp còn mở cuối lượt trước; 6→7 là `N/A`, 7→8 là 0/5 (tỷ lệ xác định
đầu tiên), 8→9 là 2/7 khi đọc chặt §8.3 (VERDICT lượt 9; 3/7 hoặc 4/7 nếu tính một hoặc hai lớp đóng vì Q12 bỏ B là vá
thật). Với hai cách đọc đầu, 8→9 là chuyển tiếp **thứ hai liên tiếp** dưới 50%, nên điểm dừng theo tỷ lệ của §12
(:1047–1048) **ĐÃ KÍCH HOẠT ở chuyển tiếp 8→9**: dừng vòng vá, đưa bằng chứng tới Review Rescue Checkpoint. Độc lập
với tỷ lệ, luật một lớp ở ba lượt (:1054–1056) cũng kích hoạt với `thu-tu-677-bo-ngo-o-dieu-kien-cap` và
`hop-dong-dong-bang-thieu-neo`. Phiên điều phối dừng vòng vá (bản chiếu `5925743728` kết bằng đúng câu ấy) và hỏi chủ
kho; chủ kho chọn *"Áp HINT, lặp không trần"* (Q13, §3). Vậy r10 tồn tại vì một quyết định **lặp tiếp có chủ ý** tại
checkpoint, không phải vì điều kiện dừng chưa chạm; r10 không tự nới §12, và lịch sử lớp không reset (:1055–1056).

Cách áp HINT lượt 9 (VERDICT `bb5bf15b…ee31`, HINT `af52b8b5…c861`, 9 hunk trong 4 nhóm), đo 01-10 (trước 09:15Z)
trong scratch của phiên soạn r10, GNU patch 2.7.6: chép r9 thành bản sao tên r10, `sed` chỉ đổi đường dẫn ở bốn cặp
dòng `---`/`+++` (đổi ngược lại thì khớp từng byte HINT gốc), `patch -p0 --fuzz=0` rc=0, 9/9 hunk, 0 fuzz, một hunk
báo offset 22 dòng (nhóm 4), 997 → 1034 dòng; bản ra khớp từng byte bản kỳ vọng reviewer dựng độc lập (sha256
`4a1d9591…c964`). Rồi sửa thêm, mỗi chỗ dựa trên phép đo của chính phiên soạn r10, không dựa trên lời HINT:
(1) `thu-tu-677-bo-ngo-o-dieu-kien-cap`: HINT đúng hướng (so cặp tên + OID) nhưng viết thành văn xuôi, ghi "không đo
được ⇒ không cấp" mà không nói phát hiện "không đo được" bằng gì; viết theo kiểu pipeline thường gặp (như khối mẫu so
tập tên trong CLAUDE.md) thì máy chủ không với tới được vẫn cho `comm -23` 0 dòng, tức đường thứ ba của cùng lớp (§10,
ca (iii)). r10 viết (1), (4), (5) thành chuỗi lệnh cố định (sau Công thức băm), kiểm rc của `ls-remote` riêng, thêm
bước so cặp lần hai, và đo trên kho bare tại chỗ rằng chuỗi bắt cả hai ca của lượt 9 lẫn hai ca tự liệt kê (§10). Sửa
thêm câu ở §10 (gạch T131/#687) còn ghi "kèm so tập tên ref" như nghĩa vụ lúc cấp. Câu *"trên cùng kho vừa qua phép so
tập tên ref ở (1)"* mà r9 thêm tay (đoạn trên) chính là F9-1.
(2) `tuong-tac-677-kiem-ke-t70-chua-neu`: HINT neo nghĩa vụ vào "tập vị từ nhận dưới Python của CI"; `python` mặc định
của container là 3.11.15, nên executor đo tại chỗ sẽ thấy tập khác CI ở mọi ca chỉ gọi helper trong comprehension (A2),
và HINT vẫn gọi đối tượng so là "tập ca", trong khi `t70` so đa tập **tiền tố** tên với ba vế. r10 đặt nghĩa vụ vào quy
tắc tham chiếu cấp đỉnh (cùng kết quả ở 3.11, 3.12, 3.13), thêm phép đo vi phạm (A8), và sửa câu lịch sử ở A2 ghi lượt 8
đo "một ca gọi helper" (phép đo ấy là ca chỉ tham chiếu ở cấp đỉnh, VERDICT lượt 9 tự nêu).
(3) `hop-dong-dong-bang-thieu-neo`: HINT thêm vế `kiem()`; r10 đo thêm rằng bộ đếm `ĐẠT v2` vẫn đếm một biên nhận có
`KHÔNG ĐO ĐƯỢC` mang tên tệp và ca CI `c1` không đếm `chua_do`, nên mục (a) ghi tiêu chí theo mục mang tên tệp cộng CLI.
(4) `dieu-kien-dung-12-doc-mot-chuyen-tiep`: HINT sửa câu đọc §12 ở đoạn trước; r10 thêm đoạn này.
(5) Q13 (§3, trích từ bản chiếu `5928886724`), header, dòng dõi, §10.
(6) **Dời nền** `20ec8d5` → `163fd5d`: phép đo điều kiện (4) lúc 09:18:38Z ra rc=1 vì #687 land (PR #701), và phiên
điều phối quyết gộp việc dời nền vào r10. Đo lại trên nền mới mọi số phụ thuộc nền: suite 198/198 ở 3.11 và 3.12,
ruff 9 lỗi F (delta 0), kích thước, tọa độ ca, đột biến `t70`, cổng biên nhận, A1, A3, điểm nóng lease (§8, A1–A3,
A8, §10). Rà phần #687 thêm theo bài học *tương tác với packet vừa land* thì gặp một chốt kiểm kê thứ hai: `t193` và
sổ `SO_BO_QUA` (§4). Ca gọi helper thật mà không tự bắt `BoQuaNen` làm `t193` ĐỎ nếu thiếu sổ hoặc thiếu literal, và
ca gọi qua hàm bọc cấp module qua được `t70` mà vẫn thiếu trong kiểm kê (A2, đo trên `163fd5d`). Nghĩa vụ (iii) và
phép đo G − D của A8 là hệ quả của lần rà ấy, không phải của HINT lượt 9.
Đây là lời khai về cách làm, không phải lời khai rằng lớp đã sạch; lượt review của r10 kiểm điều đó.

**Bộ đếm hình dạng sau lượt 10, và cách r11 xử lý.** Lượt 10 (trên r10) ra 0 P1 / 2 P2 / 2 P3, bốn lớp:
`thu-tu-677-bo-ngo-o-dieu-kien-cap` (P2, VÁ SINH LỖI MỚI, có mặt ở lượt **7, 8, 9 và 10**),
`tuong-tac-677-kiem-ke-t70-chua-neu` (P2, VÁ SINH LỖI MỚI, lượt **8, 9 và 10**), `hop-dong-dong-bang-thieu-neo` (P3,
CÒN MỞ, lượt **1, 2, 7, 8, 9 và 10**) và `so-do-nen-khong-khop` (P3, TÁI PHÁT, lượt **7, 8 và 10**);
`dieu-kien-dung-12-doc-mot-chuyen-tiep` ĐÃ VÁ THẬT. Tỷ lệ chuyển tiếp 9→10 (§12 :1043–1049) là **1/4** khi đọc chặt
§8.3 và **2/4** nếu người điều phối tách F10-6 khỏi `hop-dong-dong-bang-thieu-neo` thành lớp riêng (VERDICT lượt 10).
Chuỗi: 6→7 `N/A`, 7→8 0/5, 8→9 2/7, 9→10 1/4 (hoặc 2/4); đọc chặt thì 9→10 là chuyển tiếp thứ BA liên tiếp dưới 50%.
Luật một lớp ở ba lượt (:1054–1056) cũng đang kích hoạt với ba lớp trên. Q13 (*"Áp HINT, lặp không trần"*) đã quyết
tại checkpoint, nên các số này là số báo cáo, không phải điểm dừng; r11 không tự nới §12 và lịch sử lớp không reset.

Hai lớp P2 lặp đúng hình dạng *"VÁ ĐÚNG CHỖ ĐƯỢC CHỈ RỒI BỎ SÓT ĐƯỜNG THỨ BA"*: r10 vá đúng đường lượt 9 chỉ (so cặp
tên + OID; vị từ cấp đỉnh), rồi lượt 10 tìm ra đường thứ ba của cùng cơ chế (endpoint, bằng chứng âm, tên bị che;
đường gọi helper lạ). Vì vậy r11 **không vá theo danh sách ca của HINT** mà làm ba việc: (1) gọi tên cơ chế chung của
mỗi lớp; (2) tự liệt kê mọi đường của cơ chế ấy trước khi viết chữ, kể cả đường HINT không nêu, và dựng mỗi đường
thành một kịch bản chạy được; (3) cho mỗi đường một chốt riêng, rồi đột biến gỡ từng chốt trên đúng kịch bản của nó
để chứng minh chốt có răng (§10).
- `thu-tu-677-…`: cơ chế chung là *chuỗi kết luận từ thứ nó không ghim*. Các đường: máy chủ nào (endpoint; `insteadOf`
  trong cấu hình kho hay trong `GIT_CONFIG_*`; `GIT_DIR`; nhiều giá trị `remote.origin.url`); bước biến đổi có thật sự
  chạy không (công cụ vắng; tệp bị cắt; `ls-remote` rỗng mà rc=0); tên trỏ object nào (tên ref ngắn; OID viết tắt;
  `refs/replace`); công cụ nào đo (bản sửa chưa commit); lịch sử có đủ không (kho nông); "không có khác biệt" có phải
  vì không có gì để so không (`diff --quiet` trên đường dẫn vắng); máy chủ có được hỏi về chính ref mà (v), (vi) đọc
  không (dòng `master`). Nguyên lý vá: bằng chứng DƯƠNG cho mọi bước (mục *Chuỗi lệnh*). Đường còn lại mà không chuỗi
  client nào đóng được: tầng vận chuyển nói dối (S15), khai `KHÔNG ĐO ĐƯỢC`.
- `tuong-tac-677-…`: cơ chế chung là *kiểm kê tĩnh đo TÊN, không đo KẾT CỤC*. Các đường: mọi cách gọi mà `co_names`
  cấp đỉnh và `_ca_ung_vien_gian_tiep` không đi theo (tám đường của lượt 10, cộng `eval` một chuỗi,
  `sys.modules[__name__]`, bảng dict cấp module), và mọi cách làm `BoQuaNen` không ra khỏi thân ca (gọi trong luồng
  khác; bắt rồi ném lại kiểu khác). Nguyên lý vá: nghĩa vụ (iii) viết theo KẾT CỤC dưới nền `nt`, đo bằng chạy thật mọi
  ca (A8), không thêm một danh sách cách gọi bị cấm.
- `hop-dong-…` (F10-6): đo hiệu lực miễn trừ bằng danh sách đúng hai đường dẫn trên cây đã đọc được, không bằng bộ lọc
  chuỗi, không bằng một rc khác 0.
- `so-do-…` (F10-7): sửa A2 và §10 thành r8, rồi rà mọi chỗ nhắc revision đặc tả #677.

Cách áp HINT lượt 10 (VERDICT `2046565a…384e`, HINT `cb7f265e…1c97`, 11 hunk trong 4 nhóm), đo 01-10 (11:0xZ) trong
scratch của phiên soạn r11, GNU patch 2.7.6: chép r10 thành bản sao, `sed` chỉ đổi đường dẫn ở bốn cặp dòng
`---`/`+++`, `patch --fuzz=0 -p0` rc=0, 11/11 hunk, 0 fuzz, 8 hunk báo offset (2 hoặc 15 dòng), 1304 → 1319 dòng;
bản ra khớp từng byte bản kỳ vọng reviewer dựng độc lập (sha256 `001251f7…755d`). Rồi sửa thêm, mỗi chỗ dựa trên phép
đo của chính phiên soạn r11, không dựa trên lời HINT. **Chỗ HINT lượt 10 chưa đủ hoặc sai so với đo** (§10):
(1) `thu-tu-677-…`, chuỗi viết lại hẳn: (a) HINT để `<nền nghiệm thu>` và `<merge commit PR #689>` ở dạng viết tắt và
chặn ca "nhánh mang đúng 7 ký tự ấy" chỉ nhờ quy tắc *"stderr có `ambiguous`"*, một danh sách CẤM trên văn bản tự do;
r11 bỏ quy tắc ấy, dùng OID đủ 40 hex (S17). (b) HINT không tắt replace: một `refs/replace` cục bộ làm `ai-dang-giu`
ra `NGƯỜI_GIỮ 0` và HINT CẤP nhầm (S16). (c) HINT không ghim công cụ đo: `ops/lease_publish.py` bị sửa mà chưa
commit, HINT CẤP nhầm (S18). (d) Bước (v) của HINT vẫn chỉ là `git diff --quiet`: đường dẫn vắng ở cả hai rev cũng
rc=0, và HINT CẤP nhầm khi đường dẫn trong lệnh bị gõ sai lúc máy chủ đã land đổi write set (S25). (e) HINT không đòi
dòng `master` của máy chủ có trong phần chung: tầng vận chuyển bỏ riêng dòng ấy thì HINT CẤP nhầm (S24). (f) Phép đếm
DƯƠNG của HINT là pipeline `comm -12 mc cb | wc -l`, rc của nó là rc của `wc`, trái chính quy tắc *"bất kỳ bước nào
rc khác 0"* của HINT; phép đếm vẫn bắt `comm` vắng, nên đây là mâu thuẫn chữ, không phải ca cấp nhầm. (g) HINT ghi
`sort` bị cắt ở 4 KB *"cũng chặn tình cờ"*: chỉ đúng khi riêng bước `sort` của `mc` bị cắt (bộ thử lượt 10 đặt
`ulimit -f` cho đúng bước ấy: `mc` 4096 byte, `cb` 16362 byte); giới hạn cỡ tệp thật kế thừa cho mọi tiến trình, cắt
cả hai bước `sort` ở cùng byte, và khi ấy r10 theo chữ **CẤP nhầm** (S8c); HINT và r11 bắt bằng rc=153. (h) HINT viết
dạng URL *"trực tiếp hoặc qua proxy git của phiên"*, không phải một danh sách cho phép; trong container này
`git remote get-url` ra `https://github.com/ducthangho/tra-luat` (proxy nằm ở tầng vận chuyển, không ở URL), nên r11
liệt kê đúng hai chuỗi. (i) HINT cho `grep -v` rc=1; r11 bỏ `grep -v`, không còn ngoại lệ nào cho quy tắc rc.
(2) `tuong-tac-677-…`: HINT thêm phép quét động *"N bằng sổ, N − D rỗng"* và ghi *"ca ném lỗi khác `BoQuaNen` không
tính"*; đúng chỗ không tính ấy là lỗ: M5 (gọi helper trong `threading.Thread`) và M6 (bắt `Exception` rồi ném
`AssertionError`) qua cả `t70`, `t193` lẫn hai vế của HINT, mà `main()` dưới `nt` ĐỎ (§10). r11 viết lại (iii) theo kết
cục và thêm vế K. Chọn giữ phép quét làm tiêu chí nghiệm thu, không làm ca test mới (lý do ở A8).
(3) `hop-dong-…`: HINT đo bằng `git cat-file -e` rc khác 0, tức một bằng chứng âm; r11 đo bằng danh sách trên cây đã
đọc được, cộng mỏ neo (đoạn miễn trừ).
(4) `so-do-…`: HINT sửa A2 và §10; phiên soạn r11 rà lại mọi chỗ nhắc `dot-bien-l-bien-cong-khai` hay "đặc tả #677":
câu hỏi Q11 trích nguyên văn nhắc *"đặc tả #677 r7 (trên master)"* (đúng lúc hỏi; giữ nguyên vì là trích từng byte);
§10 gạch *Nhánh thi hành #677* nhắc r7 như phép đo ngày 30-09 (thêm chú thích r8); A2 phần r1–r7 có nhãn "nay đã cũ".
Không còn câu nào khai r7 là bản đóng băng mà PR #689 land theo.
(5) Header, dòng dõi, Q13 (§3), §8, §10; số đo lúc soạn của điều kiện (1) đổi vì #704 đang giữ `ops/lease_publish_test.py`.
Đây là lời khai về cách làm, không phải lời khai rằng lớp đã sạch; lượt review của r11 kiểm điều đó.


**Bộ đếm hình dạng sau lượt 11, và cách r12 xử lý.** Lượt 11 (trên r11) ra 0 P1 / 2 P2 / 0 P3, hai lớp:
`thu-tu-677-bo-ngo-o-dieu-kien-cap` (P2, VÁ SINH LỖI MỚI, có mặt ở lượt **7, 8, 9, 10 và 11**) và
`tuong-tac-677-kiem-ke-t70-chua-neu` (P2, VÁ SINH LỖI MỚI, lượt **8, 9, 10 và 11**); `hop-dong-dong-bang-thieu-neo` và
`so-do-nen-khong-khop` ĐÃ VÁ THẬT. Tỷ lệ chuyển tiếp 10→11 (§12, PROTOCOL :1087–1093 trên `ab457c6`) là **2/4 = 50%**,
không dưới 50% (VERDICT lượt 11). Chuỗi: 6→7 `N/A`, 7→8 0/5, 8→9 2/7, 9→10 1/4 (hoặc 2/4), 10→11 2/4. Luật một lớp ở
ba lượt (:1098–1100) vẫn kích hoạt với hai lớp P2. Q13 (*"Áp HINT, lặp không trần"*) đã quyết tại checkpoint, nên các số
này là số báo cáo, không phải điểm dừng; r12 không tự nới §12 và lịch sử lớp không reset.

VERDICT lượt 11 gợi ý (không phải điều kiện) rằng phần còn lại của cả hai lớp nằm ở NGỮ NGHĨA của hai dụng cụ đặc tả
mượn, không ở chữ: `ai-dang-giu` khớp nguyên chuỗi, seam `nt` chỉ đo kết cục. r12 làm theo hướng ấy, không vá thêm chữ
theo danh sách ca: (1) `thu-tu-677-…`: thay NGỮ NGHĨA của phép khớp trong chính chuỗi (`s5.py` chạy `lenh_ai_dang_giu`
với phép khớp PROTOCOL §5), sau khi tự liệt kê mười ba đường cùng cơ chế (ba của lượt 11, mười của phiên soạn r12) và
sáu nguồn cấu hình chọn chương trình vận chuyển; mỗi đường thành một kịch bản chạy được; mỗi chốt mới có đột biến gỡ
riêng làm đúng kịch bản của nó CẤP (§10); phần không đóng được bằng chuỗi (tầng vận chuyển, proxy/TLS, `GIT_EXEC_PATH`,
đồng hồ) khai `KHÔNG ĐO ĐƯỢC`, và khuyết tật của chính `ai-dang-giu` thành phát hiện ngoài spec. (2) `tuong-tac-677-…`:
đo LỜI GỌI thật (vế H) thay cho chỉ kết cục, sau khi đo trên nền mới rằng N9, N10 lọt q1–q3 mà H bắt; rồi tự liệt kê
các đường mà chính vế H không thấy (E1–E7: gọi bản sao `exec` của mã nguồn, `code.replace`, luồng `_thread` thô, tắt
profile, tiến trình con, bản sao chụp trước ở cấp module, lỗi trước guard) và đo từng đường (A8); các đường lọt được khai
là giới hạn, không gọi là đã đóng.

Cách áp HINT lượt 11 (VERDICT `7082d6db…1c9f`, HINT `cbc398ef…8de4`, 8 hunk trong 2 nhóm), đo 07-10 (08:2xZ) trong
scratch của phiên soạn r12, GNU patch 2.7.6: chép r11 (`fd1138c3…4a98`) vào một cây tạm đúng đường dẫn mà các dòng
`---`/`+++` của HINT nêu (không cần `sed`), `patch -p0 --fuzz=0 --verbose` rc=0, 8/8 hunk, 0 fuzz, hai hunk nhóm 2 báo
offset 26 dòng, 1614 → 1666 dòng, sha256 `bda2f35feb606a49397c729c40f187af5872c351cacc66889007212aa24e7ae6`, khớp băm
VERDICT ghi (`bda2f35f…`). Bản ấy là điểm xuất phát của r12; rồi sửa thêm, mỗi chỗ dựa trên phép đo của chính phiên soạn
r12, không dựa trên lời HINT. **Chỗ HINT lượt 11 chưa đủ hoặc sai so với đo** (§10):
(1) `thu-tu-677-…`: (a) `ai-dang-giu ops/` của HINT đóng đúng hai trong mười ba đường cùng cơ chế (`ops/`,
`planned:ops/`); mười một đường còn lại vẫn CẤP nhầm dưới chuỗi r11 + HINT, gồm cả những đường HINT không khai làm giới
hạn (`effective_write_set`, mà PROTOCOL :32, :329 lấy làm cơ sở loại trừ; prefix không `/`; prefix viết hoa; `write_set`
vô hướng; glob; separator ngược; mục ánh xạ `exact`). Câu HINT *"`ops/` là prefix thư mục duy nhất phủ hai tệp (dạng
tuyệt đối, `.`/`..` bị §5 bước 2 từ chối)"* đúng với đầu vào đã qua dispatcher, mà lease trên nhánh thì không qua
dispatcher nào; nên *"đóng đúng đường ấy"* hẹp hơn lời khai. (b) Danh sách cho phép của HINT chỉ phủ `remote.origin.*`;
năm đường cấu hình ở §10 HINT đều bắt, nhưng dòng `url.*` ngoài danh sách thì lọt (vô hại ở bộ thử, vì endpoint bắt
`insteadOf`); r12 mở rộng sang `url.*` theo chỉ thị, với giá được khai. (c) Biểu thức chính quy của HINT thoát dấu chấm bằng
dấu chéo ngược (hai ký tự trong dòng lệnh); r12 viết `[.]`, nên số dấu chéo ngược của tệp không tăng so r11. (d) HINT để `adg.3` cùng nhãn
khớp với `adg.1`, `adg.2`; r12 bỏ `adg.3` vì `s5.py` phủ nó (mọi mục khớp `ai-dang-giu ops/` cũng khớp §5 của cả hai
tệp; đột biến gỡ `s5.py` làm kịch bản `ops/` CẤP, §10). (e) Sửa chữ quy tắc chạy lại của HINT là đúng: bộ chấm r12 đọc từng
chữ cho S4, S5 ra *chạy lại ⇒ không cấp*, S8c ra KXĐ ở rc=153; r12 thêm luật đọc theo thứ tự bước cho đủ chữ.
(2) `tuong-tac-677-…`: vế H của HINT đúng và có răng trên nền mới (N9, N10 chỉ bị H bắt, ở 3.11 lẫn 3.12; A8); VERDICT lượt 11
khai giới hạn của H là *"lời gọi trong tiến trình con không thấy"* mà không đo; r12 đo bảy đường (E1–E7, A8): vế H lọt sáu
đường (bản sao `exec` mã nguồn, bản sao `code.replace` trong ca và ở cấp module, luồng `_thread` thô, ca tự tắt profile,
tiến trình con) và chỉ bắt một (helper ném trước guard). (q3) dạng
*"K ứng viên − K nền rỗng"* của HINT đúng; ví dụ `t199` đã sửa ở §4. Số đo của HINT là trên `163fd5d`; r12 đo lại mọi số
ấy trên `ab457c6`.
(3) Dời nền (`163fd5d` → `ab457c6`): phép đo điều kiện (4) với nền cũ ra rc=1 vì wp709 land; phiên điều phối giao gộp
việc dời nền vào r12. Đo lại trên nền mới mọi số phụ thuộc nền: suite 201/201 ở 3.11 và 3.12, ruff 11 lỗi F (delta so
`163fd5d` là 2 `F841` của wp709, ngoài objective), tọa độ ca và helper, đột biến `t70`, phép quét động, cổng biên nhận,
A1, A3, A5–A7, điểm nóng lease, `ci.yml`. Rà phần wp709 thêm theo bài học *tương tác với packet vừa land* thì gặp một
tương tác thật: `kiem()` gọi `_kiem_provider_identity` TRƯỚC D1, nên mẫu lease mà A1 dùng để đo ĐỎ trên nền (wp55, lease
reviewer khai `cross_approved` mà thiếu `executor`) nay ra rc=10 ở mọi dạng lẫn đối chứng; ca A1 phải dùng fixture qua
được luật danh tính, nếu không thì rc=10 che D1 (A1). Cùng luật ấy đặt ràng buộc lên chính lease `wp678` (ghi chú dưới
closure). Ba ca `t01_*` của wp709 không đụng nghĩa vụ `t70`/`t193`/sổ/helper (A2, A8).
Đây là lời khai về cách làm, không phải lời khai rằng lớp đã sạch; lượt review của r12 kiểm điều đó.

**Bộ đếm hình dạng sau lượt 12, và cách r13 xử lý.** Lượt 12 (trên r12) ra 0 P1 / 2 P2 / 1 P3, ba lớp:
`thu-tu-677-bo-ngo-o-dieu-kien-cap` (P2, CÒN MỞ, có mặt ở lượt **7, 8, 9, 10, 11 và 12**),
`tuong-tac-677-kiem-ke-t70-chua-neu` (P2, CÒN MỞ, lượt **8, 9, 10, 11 và 12**) và `chinh-xac-hoa-so-hieu-va-tham-chieu` (P3,
mới). VERDICT lượt 12 ghi cả hai biểu hiện mới của lớp đầu là CÓ TỪ TRƯỚC r12 (r11 cũng CẤP ở R1 và R4), nên không xếp
VÁ SINH LỖI MỚI; năm finding của lượt 11 đóng thật. Tỷ lệ chuyển tiếp 11→12 (§12, PROTOCOL :1087–1093 trên `ab457c6`) là
**0/2 = 0%** theo lớp (5/5 theo finding). Chuỗi: 6→7 `N/A`, 7→8 0/5, 8→9 2/7, 9→10 1/4 (hoặc 2/4), 10→11 2/4, 11→12 0/2.
Luật một lớp ở ba lượt (:1098–1100) vẫn kích hoạt với hai lớp P2. Q13 (*"Áp HINT, lặp không trần"*) đã quyết tại
checkpoint, nên các số này là số báo cáo, không phải điểm dừng; r13 không tự nới §12 và lịch sử lớp không reset. Lượt 12
do Claude Sonnet 5.5 chạy, không phải subagent `review-opus-max` (VERDICT lượt 12, Lưu ý 1); điều kiện cấp (3) không đổi
chữ, nên chỉ một lượt `review-opus-max` sạch mới thoả nó.

VERDICT lượt 12 gợi ý (không phải điều kiện) rằng cả hai lớp còn mở vì cùng một hình dạng: *một phép đo hẹp hơn thứ nó
khai*. Phiên soạn r13 kiểm gợi ý ấy trên chính HINT lượt 12 trước khi nhận nó, và gặp lại đúng hình dạng ấy ở chính bản vá
(bài học *"VÁ ĐÚNG CHỖ ĐƯỢC CHỈ RỒI BỎ SÓT ĐƯỜNG THỨ BA"* và *"Danh sách CẤM không bao giờ đủ"* của CLAUDE.md): (1) bọc `-z`
dựng lại DÒNG từ đầu ra NUL, nên mở cửa mới ở bộ tách dòng (tiêm dòng qua ký tự ngắt dòng; CẤP nhầm ở cả tám ký tự thử);
(2) danh sách cho phép KÝ TỰ để nguyên danh sách cấm ở tầng HÌNH DẠNG mục ánh xạ (`type`, khoá lạ) và ở tầng KIỂU mục
cây (gitlink, symlink); (3) vế (S) duyệt một danh sách loại nút nên mù tên đối số từ khoá và tên tham số, và công cụ đo
của nó lệch chính chữ của nó ở giá trị mặc định cấp module. r13 liệt kê hết cửa trước khi vá: (1) đọc
`_quet_lease_toan_kho` và đặt tên năm cửa trước phép khớp (đặc tả đường dẫn, văn bản `ls-tree`, bộ tách dòng, kiểu mục,
đuôi), đo từng cửa (33 ca trực tiếp, 15 kịch bản chuỗi R5/R6), đóng cửa bộ tách dòng bằng phép đo HIỆU ỨNG lên chính bộ
tách và cửa kiểu mục bằng danh sách cho phép mode, khai cửa đặc tả đường dẫn và phần còn lại của cửa đuôi là miền của
công cụ, trùng miền workflow đăng; (2) đảo hình dạng mục ánh xạ sang danh sách cho phép (`type` thuộc {`exact`,
`prefix`}, khoá thuộc {`type`, `path`}) và thêm luật đoạn kết thúc bằng dấu chấm; (3) viết lại (S) thành danh sách cho
phép thật trên MỌI trường chuỗi của MỌI nút `ast`, đo lại 38 biến thể trên hai bản Python trong một lệnh. Mỗi chốt mới có
ca tự kiểm riêng và kịch bản chuỗi riêng làm nó ĐỎ khi bị gỡ, cộng hai đột biến *lùi về danh sách cấm* (chỉ LF; chỉ kiểu
`blob`) làm đúng hàng của chúng CẤP (§10).

Cách áp HINT lượt 12 (VERDICT `eb28deae…2e3f`, HINT `e1b57491…ad23`, 20 hunk trong 3 nhóm), đo 07-10 (12:05Z) trong
scratch của phiên soạn r13, GNU patch 2.7.6: chép r12 (`c356c1a7…a083`) vào một thư mục tạm, dùng `sed` đổi các dòng
`---`/`+++` của cả ba nhóm sang tên bản chép, `patch -p0 --fuzz=0 --dry-run --verbose` rồi `patch -p0 --fuzz=0 --verbose`,
cả hai rc=0, 20/20 hunk, 0 fuzz, 2153 → 2261 dòng, sha256
`aa166a2a25bc3b12d984e2eca73b57bf3d4ced9ae2b40d752c6d22ecfbf5ff24`, khớp băm VERDICT ghi. Bản ấy là điểm xuất phát của r13;
rồi sửa thêm, mỗi chỗ dựa trên phép đo của chính phiên soạn r13, không dựa trên lời HINT. **Chỗ HINT lượt 12 chưa đủ hoặc
sai so với đo** (§10):
(1) `thu-tu-677-…`: (a) bọc `-z` của HINT tự mở đường tiêm dòng: tám ký tự ngắt dòng, `s5.py` của HINT rc=0 ở cả tám, và
ở cả hai ca lặp lại với `core.quotePath=false` (U+2028, NEL; công cụ nền khi ấy ra rc=12); (b) symlink có nội dung là ánh xạ YAML, và gitlink: `s5.py` của
HINT rc=0; (c) `type` lạ, khoá lạ, thiếu `type`, đoạn kết thúc bằng dấu chấm: `kiem()` nhận cả bốn, chuỗi đã áp HINT CẤP ở
cả bốn; (d) lời khai *"`s5.py` mới … không dạng nào ra rc=0"* đúng cho mười một dạng tên reviewer thử, nhưng rộng hơn
phép đo (đường tiêm ở (a)); (e) câu của r12 *"ca NFC nằm ở tự kiểm"* (HINT không sửa) không còn đúng khi đã có bảng chữ:
bỏ NFC hay bỏ đổi separator làm đỏ 0 ca tự kiểm và không đổi kịch bản chuỗi nào; (f) bảng chữ HINT giao phiên soạn đo lại
trên `adg2`: 473 ref, 3986 đường dẫn, 1530 mục write set, 0 ngoài bảng, 0 bị luật r13 chặn; (g) đoạn §10 *Đột biến gỡ từng
chốt mới của r12* và lượt chạy thật ở hàng `depends_on` mô tả `s5.py` r12: r13 chạy lại bộ đột biến với `s5.py` r13 (hai
mươi mốt đột biến của `s5.py` cộng ba đột biến văn bản, 1307 lượt) và chạy lại chuỗi thật trên `adg2`.
(2) `tuong-tac-677-…`: (a) vế (S) của HINT mù tên đối số từ khoá và tên tham số (E5g, E5i: không cổng nào thấy); (b) số đo
(S) của HINT lệch chữ của nó ở N7 (giá trị mặc định cấp module: chữ nói ĐỎ, công cụ cho xanh), nên *"xanh ở 14"* và
*"chỉ động 7"* là của công cụ, không phải của chữ; (c) phần còn lại tái lập đúng: H2 bắt E1, E2b, E3, E4, E6b; tập ĐỎ của
(S) của HINT trên 36 biến thể cũ là 22, cùng tập; phủ chéo 26 biến thể 15/7/1/0/3.
(3) `chinh-xac-hoa-…` (P3): sáu mục của HINT nhóm 3 đúng khi đo lại: băm `dbf3b905…8f67`; `grep -n lease_id` trên blob
`93cff2f` ra 38 dòng và có đủ 19 tọa độ D1–D9 (lệnh cũ có nháy kép ra 19 dòng); dict comprehension (`co_names` của hàm có
list, set hay dict comprehension chứa tên helper: có ở 3.12.3 và 3.13.12, không ở 3.11.15; genexp, lambda không ở bản nào;
13:16Z); điều kiện fixture của
A7 (`check --du-bao` của `ab457c6`, mẫu wp55 bỏ `prompt_*`, hạn dời ra tương lai: rc=10 ở cả mười một dạng; thêm `executor:
claude` thì rc=0 ở cả mười một; 12:37Z 07-10, python3.12); mười ba code point (NFC 3, casefold 11, `NFC(casefold)` 13 ở
3.11.15, 3.12.3, 3.13.12; 13:03Z); câu về năm điều kiện (nay ở đoạn *Thay đổi so với r12*).
Kiểm nền: `origin/master` vẫn là `ab457c6` (12:06:45Z và lượt chạy thật, hàng `depends_on`), nên r13 không dời nền và không
đo lại các số hạng phụ thuộc nền của r12 (suite, ruff, tọa độ, A1–A6; riêng điều kiện fixture của A7 đo lại ở (3)).
Đây là lời khai về cách làm, không phải lời khai rằng lớp đã sạch; lượt review của r13 kiểm điều đó.

**Bộ đếm hình dạng sau lượt 13, và cách r14 xử lý.** Lượt 13 (trên r13; VERDICT `372efdfe…c244`) ra 0 P1 / 1 P2 / 1 P3:
`tuong-tac-677-kiem-ke-t70-chua-neu` (P2, CÒN MỞ, lượt **8, 9, 10, 11, 12 và 13**; biểu hiện mới là họ E8, có từ trước r13)
và `chinh-xac-hoa-so-hieu-va-tham-chieu` (P3, CÒN MỞ; ba câu mới của r13); `thu-tu-677-bo-ngo-o-dieu-kien-cap` ĐÃ VÁ THẬT
(mở từ lượt 7). Tỷ lệ chuyển tiếp 12→13 (§12, PROTOCOL :1087–1093 trên `ab457c6`) là **1/3 = 33%** theo lớp (9/9 theo
finding). Chuỗi: 6→7 `N/A`, 7→8 0/5, 8→9 2/7, 9→10 1/4 (hoặc 2/4), 10→11 2/4, 11→12 0/2, 12→13 1/3: hai chuyển tiếp liền
nhau dưới 50%; Q13 đã quyết nên đây là số báo cáo, không phải điểm dừng. Luật một lớp ở ba lượt (:1098–1100) vẫn kích hoạt
với `tuong-tac-677-…`. Lượt 13 không sạch, nên điều kiện cấp (3) vẫn chưa thoả dù danh tính `review-opus-max` của lượt ấy
có được xác nhận hay không (VERDICT lượt 13, Lưu ý 1). VERDICT lượt 13 (Lưu ý 3) gọi tên hình dạng lặp: dụng cụ đo hẹp
hơn thứ nó khai; vế lật đo HIỆU ỨNG (guard thấy `nt`) mà vẫn khoá guard theo tên hay bytecode, nên chỉ THU HẸP. Phiên soạn
r14 kiểm điều ấy bằng biến thể mới cùng cơ chế trước khi nhận HINT (A8). **Chỗ HINT lượt 13 chưa đủ hoặc sai so với đo**
(§10): (1) câu H2 của HINT xếp mọi bản sao ở module nạp lại vào K, mà `importlib.reload` module đã nạp (E8h) vào N, tức
(q1) bắt; (2) HINT khai giới hạn E5f, E8e, E8g mà thiếu E8l: ca tự gọi `sys.setprofile(None)` rồi gọi bản sao lọt cả vế
lật; (3) HINT ghi kết cục Windows của E8g `KHÔNG ĐO ĐƯỢC`; oracle của phiên soạn r14 khoá thêm theo dòng `def` ra ĐỎ ở hai
bản, vẫn là mô phỏng; (4) phần còn lại của nhóm 1 tái lập đúng bằng dụng cụ riêng: E8a, E8c, E8d, E8f vào K, nền và 38
biến thể cũ không đổi tập nào, quét đủ nền giống hệt, năm ca hợp lệ không bị báo nhầm; (5) nhóm 2 đúng khi đo lại (ảnh 473
ref dựng lại: 21 danh sách khác rỗng, 0 danh sách rỗng, cộng 2 cặp `null`; 39, 6, 6, 8; `ten_tep_11.py`: chín dạng rc=11), nhưng r13
còn bốn chỗ số tự khai lệch đo mà HINT không nêu, r14 sửa: OID viết tắt của `s5.py` r12 (`…1e01` thành `…2e01`, hai chỗ),
`_ls_tree_z` :1976 thành :1977, `_quet_lease_toan_kho` :641–702 thành :641–701, và câu về lệnh `grep` của r12 ở §2 (19 là
của lệnh hai mẫu; riêng mẫu `"lease_id"` ra 16). Đây là lời khai về cách làm, không phải lời khai rằng lớp đã sạch; lượt
review của r14 kiểm điều đó.

**Bộ đếm hình dạng sau lượt 14, và cách r15 xử lý.** Lượt 14 (trên r14; VERDICT `69f5f010…eb6b`) ra 0 P1 / 1 P2 / 0 P3:
`tuong-tac-677-kiem-ke-t70-chua-neu` (P2, CÒN MỞ, lượt **8 đến 14**; F14-1 VÁ HỜ: giới hạn khai theo API, E8n, E8n2 lọt;
F14-2 VÁ SINH LỖI MỚI: vế lật đổi `os.name` toàn tiến trình, V1, V6) và `chinh-xac-hoa-so-hieu-va-tham-chieu` ĐÃ VÁ THẬT
(P3 ở lượt 12–13). Tỷ lệ chuyển tiếp 13→14 (§12, PROTOCOL :1087–1093 trên `ab457c6`) là **1/2 = 50%** theo lớp (3/4 theo
finding). Chuỗi: 6→7 `N/A`, 7→8 0/5, 8→9 2/7, 9→10 1/4 (hoặc 2/4), 10→11 2/4, 11→12 0/2, 12→13 1/3, 13→14 1/2: không thêm
cặp chuyển tiếp liền nhau dưới 50%; Q13 đã quyết nên đây là số báo cáo. Luật một lớp ở ba lượt (:1098–1100) vẫn kích hoạt
với `tuong-tac-677-…` (bảy lượt). Lượt 14 không sạch, nên điều kiện cấp (3) vẫn chưa thoả. VERDICT lượt 14 (Lưu ý 3) gọi
tên hình dạng lặp: dụng cụ được MÔ TẢ rộng hơn thứ nó đo; r15 giữ cách khai giới hạn theo tính chất của HINT và kiểm nó
bằng biến thể mới cùng cơ chế (A8, đoạn *Phiên soạn r15 đo lại*). **Chỗ HINT lượt 14 chưa đủ hoặc sai so với đo** (§10):
(1) HINT viết *"khung guard ĐẦU TIÊN vào thì lưu giá trị gốc"*, còn `quet14b.py`, dụng cụ ra mọi số của HINT, lấy giá trị
gốc một lần lúc bộ quét bắt đầu; hai cách khác nhau ở ca tự vá `os.name` quanh lời gọi guard (V9: `quet14b.py` K ở cả hai
bản, `quet14.py` đạt); r15 viết theo dụng cụ đã đo và xếp V9 vào tạo tác của seam đã khai; (2) (α) của HINT nêu E8n, E8n2
*"khi dụng cụ cài sau lúc nạp"*, mà theo chữ r15 dụng cụ cài trước nên hai biến thể ấy (và E8r) vào K; hai biến thể lọt
`quet14b.py` là E8v (lúc nạp) và E8u (lúc thoát), HINT không nêu, cả hai thuộc (α) theo tính chất, r15 nêu và viết lại (α)
theo hàm profile có hoạt động trên luồng ấy hay không; (3) cài `threading.setprofile` trước khi nạp đưa cả luồng khởi động
lúc nạp vào vế lật, nên ca hợp lệ có luồng ấy gọi guard (V10) gây L ở mọi lượt đo và K ở một số lượt, mà `quet14.py`
không có; câu tạo tác toàn tiến trình
của HINT phủ nó theo tính chất, r15 nêu V10 cạnh V6; (4) danh sách của handoff trong HINT liệt kê theo API, r15 viết theo
tính chất kèm lời gọi đã gặp; (5) phần còn lại của HINT tái lập đúng: khác đúng ba hàng trên 60 hàng ở cả hai bản, kịch bản
V1 đầu `CA`, các kết cục E8p, E8q, E8w, E8w2, V6, V7, lặp 5/5, và quét đủ nền cùng mọi tập. Đây là lời khai về cách làm,
không phải lời khai rằng lớp đã sạch; lượt review của r15 kiểm điều đó.

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
  delta F của ứng viên chưa đo vì chưa có ứng viên. r12 đo lại trên `ab457c6`: 11 lỗi (9 cũ cộng 2 `F841` của wp709,
  §8). r9 không đo lại ruff; r10 đo lại trên nền mới `163fd5d` (§8: vẫn 9 lỗi, cùng tập). r11 không đo lại; review lượt 10 tái lập 9 lỗi cùng tập ở `20ec8d5`, `163fd5d` và `7e5958e`. Lịch sử: `KHÔNG ĐO ĐƯỢC` ở phiên soạn r1–r7; r7 khai cũng vậy ở mọi
  lượt review tới lúc ấy.
- Băm thân Mission Issue #682 ở phía nhận: r8 đọc qua REST và ghi `76bee6fb…0dd2` (01:08:54Z 01-10, đoạn miễn trừ),
  một phép đo tại một thời điểm. Lịch sử: `KHÔNG ĐO ĐƯỢC` ở r6 (đường đọc MCP chuẩn hoá thực thể
  HTML); r7 đọc #682 qua REST nhưng không ghi băm; r9 đọc lại 05:22Z 01-10, r10 đọc lại 09:31:01Z, r11 đọc lại 11:29:48Z 01-10 và r12 đọc lại 08:36:26Z 07-10, cùng
  băm, 3416 byte. Descriptor vẫn neo bằng số Issue + object ID `5627190292`.
- **Đường `claude -p` qua `launcher.py run` (phương án B của r8): BỎ ở r9 theo Q12.** Phép dò 01:07Z 01-10 của r8 (một
  lượt `claude -p` ngắn, không qua launcher) và các phép đo của review lượt 8 (`run.json` không lưu argv; validator
  nhận mọi chuỗi ở `session_run_id`; probe `claude_trust` của launcher chặn `CHAN [15]` ở sandbox chưa trust, đo với
  `claude` giả) giữ làm lịch sử. Trust và quyền công cụ ở chế độ `-p`, hành vi `claude` thật qua launcher: `KHÔNG ĐO
  ĐƯỢC`, và packet này không còn cần đo chúng. Lớp `duong-review-b-chua-do-dau-cuoi` (lượt 8) **đóng vì bỏ B**, không
  phải vì B đã được đo đầu cuối.
- **Hai lớp còn lại của đường review (lượt 8), trạng thái ở r9.** `hop-dong-dong-bang-thieu-neo`: closure và ghi chú
  dưới nó nay chỉ khai thứ kiểm được (mức và chế độ qua `_thieu`, từ r10 cộng `kiem()` và CLI theo review lượt 9, băm
  định nghĩa, VERDICT sạch) và khai model/effort đã
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
  vẫn phải đo lại lúc cấp lease cho `wp678` (r6 khi ấy ghi `ai-dang-giu` kèm so tập tên ref; từ r10 là chuỗi lệnh đo
  điều kiện cấp, so cặp tên + OID; từ r11 mọi bước của chuỗi ấy có tiêu chí dương). Chưa đo được: #687 có
  land trước hay không và có đổi `ops/lease_publish_test.py` hay không (điều kiện 4 của Q8); nếu có thì
  cần revision mới dời nền. **r7 (30-09):** hai lease #687 `HẾT_HẠN`, hai tệp `NGƯỜI_GIỮ 0` ở clone mới, #687
  chưa land tới `423b4ba` (hàng `depends_on`); vẫn phải đo lại lúc cấp. **r8 (01-10):** hai lease #687 vẫn `HẾT_HẠN`,
  #687 chưa land tới `20ec8d5`, hai tệp `NGƯỜI_GIỮ 0` ở clone mới (hàng `depends_on`); vẫn phải đo lại lúc cấp.
  **r9 (01-10, 05:17Z–05:18Z):** `ops/lease_publish_test.py` do lease `lease-publish-windows-do-r3-g3-claude` (#687,
  generation 3, cấp `2026-10-01T01:12:00Z`) giữ tới `2026-10-02T01:12:00Z`, nên điều kiện (1) chưa thoả; #687 chưa land
  tới `20ec8d5` (= `origin/master` lúc đo). #687 land và đổi tệp ấy ⇒ điều kiện (4) ⇒ revision mới dời nền trước khi
  cấp. **r10 (01-10):** điều đó đã xảy ra: #687 land qua PR #701 (`163fd5d`, `2026-10-01T05:42:28Z`) và đổi
  `ops/lease_publish_test.py` (`482 63`) ⇒ điều kiện (4) rc=1 (09:18:38Z) ⇒ r10 dời nền sang `163fd5d`. Người giữ
  `ops/lease_publish_test.py`: 09:18Z `NGƯỜI_GIỮ 1` (bản lease g3 trên master còn hạn tới `2026-10-02T01:12:00Z`), 09:45Z
  `NGƯỜI_GIỮ 0` sau khi bản rút hạn vào master (`a6de9d1`); dữ kiện lúc soạn, không phải lời khai điều kiện (1) thoả
  (hàng `depends_on`). **r11 (01-10, 11:22Z):** `ops/lease_publish_test.py` do lease `no-ton-677-687-r1-g1-claude`
  (#704, cấp 09:55:00Z) giữ tới `2026-10-02T09:55:00Z`, nên điều kiện (1) chưa thoả; #704 đổi tệp ấy (thân `t194`),
  land trước lúc cấp ⇒ điều kiện (4) ⇒ revision mới dời nền (hàng `depends_on`). **r12 (07-10, 09:07Z):** #704 không
  còn giữ (lease g1 và g2 của nó đều `HẾT_HẠN`; nhánh `claude/no-ton-677-687` chưa là tổ tiên của `origin/master`);
  nhưng wp709 land (PR #712) và đổi cả hai tệp ⇒ điều kiện (4) ⇒ r12
  dời nền sang `ab457c6`; người giữ cả hai tệp lúc soạn là lease `wp709-exec-g2-codex-20261006` (hạn
  `2026-10-07T10:30:00Z`), còn hạn dù packet đã land (hàng `depends_on`).
- **Nhánh thi hành #677 đổi một tệp write set mà chưa land (đo r7, 30-09; nay đã land và lớp đã đóng, xem cuối
  gạch).** Đặc tả #677 đã vào master (PR
  #684, `44620e8`). Nhánh `claude/dot-bien-l-bien-cong-khai-20260929` (đầu `8e630c0`, 09:48:22Z, merge-base
  `423b4ba`) đổi `ops/lease_publish_test.py` +596/−15 (`git diff --stat origin/master...<nhánh>`). Năm lease
  `exec-1`…`exec-5` của #677 giữ tệp ấy tới `2026-09-30T10:48:00Z`, output `ai-dang-giu` 12:28Z ghi cả năm
  `HẾT_HẠN`. Commit `6112b89` ghi *"chủ kho chốt #677 đi trước"* (lời khai trong commit), nhưng thứ tự còn có nguồn
  **trên master**: đặc tả #677 r7 (`ops/specs/dot-bien-l-bien-cong-khai-r7.md`, có từ `44620e8`; bản đóng băng mà PR #689 land theo là
  r8, giữ cùng quyết định ở :294 và :401, xem A2) ghi quyết định chủ
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
  #687 generation 3 đang giữ `ops/lease_publish_test.py` (hàng `depends_on`); r10 cho thấy nó kích hoạt thật (#687
  land đổi tệp write set, đầu tệp). Phiên soạn r10 đo lại (09:5xZ 01-10, `git archive <rev> ops/leases` cộng
  `yaml.safe_load`): trên `163fd5d` 122 tệp `.yaml` (cộng 4 `.nhap`), 0 lỗi parse, 26 tệp khai giữ
  `ops/lease_publish*.py`, 9 packet (thêm #687); trên `a6de9d1` (`origin/master` lúc đo cuối) 128 tệp `.yaml`, 0 lỗi
  parse, 32 tệp, 10 packet (thêm #677). Phiên soạn r12 đo lại (09:03:33Z 07-10, cùng cách): trên `ab457c6` 132 tệp
  `.yaml` (cộng 4 `.nhap`), 0 lỗi parse, 32 tệp khai giữ `ops/lease_publish*.py`, 10 packet (#203, #206, #227, #238,
  #244, #396, #579, #676, #677, #687); trên `163fd5d` 122 tệp, 26 tệp, 9 packet (khớp số r10). Lease của #704 và của
  wp709 nằm trên nhánh, không trên master.
- **Ref đệm cũ ở điều kiện (1) và (4)** (review lượt 9, 05:43Z–05:53Z 01-10; kho bare đóng vai máy chủ dựng tại chỗ,
  clone refspec `+refs/heads/*:refs/remotes/origin/*`, `ai-dang-giu` của `20ec8d5`; không mạng). `ai-dang-giu` không
  `fetch`; nó chỉ so TÊN nhánh máy chủ thiếu cục bộ và nhánh cục bộ tụt sau remote-tracking (`ops/lease_publish.py`
  :370–421, :482–511), không so OID với máy chủ. (i) Máy chủ land một commit đổi `ops/lease_publish_test.py`, clone
  chưa fetch: tập tên 1/1, `comm` 0 dòng hai chiều; `ai-dang-giu` rc=0 `NGƯỜI_GIỮ 0`; lệnh của (4) rc=0;
  `merge-base --is-ancestor <nền> origin/master` rc=0; chỉ phép so tên + OID lệch (2 dòng). (ii) Máy chủ thêm lease g2
  CÒN_HẠN giữ `ops/lease_publish_test.py` trên CÙNG nhánh với lease g1 đã hết hạn: tập tên 2/2, 0 lệch; `ai-dang-giu`
  rc=0 `NGƯỜI_GIỮ 0`; so tên + OID lệch 2 dòng. Sau `git fetch origin '+refs/heads/*:refs/remotes/origin/*'`: (i) lệnh
  của (4) rc=1, (ii) `NGƯỜI_GIỮ 1` rc=11. Vì vậy (1) và (4) đòi thêm phép so tên + OID; phép so tập tên của Q8 giữ
  nguyên nhưng một mình nó không đủ. Fence trước merge/land (PROTOCOL :365–368, §5.1, §13) đã đòi so bằng
  tên **và** OID; điều kiện cấp ở đây mượn cách so tên + OID ấy, nhưng chỉ cho nhánh (`ls-remote --heads`), vì
  `ai-dang-giu` chỉ quét `refs/heads` và `refs/remotes` (`ops/lease_publish.py` :312–324); fence đầy đủ còn gồm `HEAD`,
  tag và `refs/pull/*`. **Phiên soạn r10 tái lập và mở rộng** (09:19:55Z–09:19:58Z 01-10; kho bare tại chỗ đóng vai máy
  chủ, `ai-dang-giu` của `20ec8d5`, giống hệt `163fd5d`; Python 3.11.15; script ở scratch) bằng đúng chuỗi lệnh đo điều kiện cấp, chạy hai
  cách: bỏ bước (i) (mô phỏng người quên `fetch`) và đủ chuỗi. (i) Packet khác land đổi `ops/lease_publish_test.py`: bỏ
  `fetch` ⇒ tên 1/1, `comm` theo tên 0 dòng hai chiều (kiểu pipeline lẫn kiểu chuỗi lệnh), cặp tên + OID `comm -23`
  **1 dòng** (`master <OID mới>`; `comm -13` 1 dòng là OID cũ, tổng hai chiều 2 dòng đúng như lượt 9 đếm) nên chuỗi
  DỪNG ở bước (iii), trong khi `ai-dang-giu` rc=0 `NGƯỜI_GIỮ 0` và lệnh (4)
  rc=0 trên đệm cũ; đủ chuỗi ⇒ (iii) 0 dòng, (iv) `NGƯỜI_GIỮ 0` rc=0, (v) **rc=1**. (ii) Lease g2 còn hạn trên nhánh đã
  có tên: bỏ `fetch` ⇒ tên 2/2, 0 lệch, cặp `comm -23` **1 dòng** (`claude/lease-khac <OID mới>`); đủ chuỗi ⇒ (iii) 0
  dòng, (iv) `NGƯỜI_GIỮ 1: khac-g2-claude` rc=11. (iii) Tự liệt kê, `origin` trỏ tới đường dẫn không tồn tại: so tập tên
  kiểu pipeline cho `comm -23` **0 dòng** (`comm -13` 1 dòng), tức fail-open; chuỗi lệnh: `fetch` rc=128, `ls-remote`
  rc=128, 0 dòng ⇒ `KHÔNG_XÁC_ĐỊNH`; riêng `ai-dang-giu` cũng tự ra `CHẶN [12]` `KHÔNG_XÁC_ĐỊNH` vì nó tự gọi `ls-remote`
  (:300–309). (iv) Tự liệt kê, máy chủ đổi ngay sau `fetch`: (iii) và (vii) `comm -23` 1 dòng; `fetch` lại ⇒ 0 dòng, (v)
  rc=1. Thiếu `merge --ff-only` sau `fetch` ⇒ `ai-dang-giu` `CHẶN [12]` `NHÁNH_CỤC_BỘ_TỤT_SAU` (lượt đo trước, 09:19:35Z,
  khi script chưa có bước ấy). 0 tệp `.pyc`. Một lỗi đo của chính phiên soạn r10, ghi để không lặp: lượt đo kho thật
  đầu tiên (09:17:33Z) in `$?` sau một `$(date …)` trong cùng câu `echo`, nên `$?` là mã của `date` và in rc=0 cho lệnh
  (4) và cho `ai-dang-giu` (`NGƯỜI_GIỮ 1`), trong khi mã thật là 1 và 11; mọi số r10 ở hàng `depends_on` và §8 lấy từ
  lượt đã sửa (09:18:18Z), bắt rc vào biến ngay sau lệnh.
  **Review lượt 10 đo thêm** (10:21:57Z–10:22:28Z và 10:45:43Z–10:45:46Z 01-10; kho bare tại chỗ đóng vai máy chủ;
  `ops/lease_publish.py` của `163fd5d`, blob `dd17b94c…4f83`; Python 3.11.15; chuỗi chạy đúng từng dòng của r10 và chấm
  theo đúng chữ r10). Tái lập: hai ca lượt 9 ⇒ không cấp; quên `fetch` ⇒ vẫn lệch ⇒ `KHÔNG_XÁC_ĐỊNH`; máy chủ không
  tới ⇒ `KHÔNG_XÁC_ĐỊNH`; máy chủ đổi ngay sau `fetch` hay sau `ls-remote` ⇒ lệch ở (iii) hay (vii), đo lại, không cấp.
  Nhưng chuỗi CẤP ở bốn ca mà máy chủ thật đã có lease `CÒN_HẠN` giữ `ops/lease_publish_test.py` hoặc đã land đổi
  write set: (S7a, S7b) `origin` là một mirror chưa cập nhật của máy chủ (clone của clone), mọi bước qua với ảnh của
  mirror; (S8a, S8b) `comm` hoặc `awk` vắng (rc=127) cộng máy chủ đổi ngay sau `fetch`, `comm -23` ra 0 dòng ở (iii)
  và (vii) nên (iv) đọc ref cũ ra `NGƯỜI_GIỮ 0`. Thêm (S9b, S10b): HEAD tách rời không nhánh cục bộ, và tag
  `origin/master` (có trên máy chủ, `git clone` lấy theo) hoặc nhánh cục bộ `origin/master` trỏ nền cũ, máy chủ land
  đổi write set ⇒ (v) so với ref bị che, rc=0, CẤP; còn nhánh `master` thì (iv) ra `CHẶN [12]`, chặn tình cờ. `sort` của
  riêng `mc` bị cắt ở 4 KB (S8c) cũng chặn tình cờ vì dòng cuối bị cắt dở (cắt cả hai bước `sort` thì r10 CẤP nhầm,
  gạch kế tiếp). Cùng bộ thử: kiểm endpoint chặn S7a, S7b (bộ thử so
  với đường dẫn máy chủ tại chỗ thay cho phép kiểm URL mạng); đòi rc mọi bước và phép đếm DƯƠNG chặn S8a, S8b;
  `refs/remotes/origin/master` tường minh làm S9b, S10b ra (v) rc=1; đối chứng sạch vẫn cấp.
- **Chuỗi lệnh r11 trên bộ thử** (phiên soạn r11, 11:21:14Z–11:23:30Z 01-10, S19 chạy lại 11:24:54Z–11:25:02Z sau
  khi sửa cách dựng; kho bare tại chỗ đóng vai máy chủ, `ops/lease_publish.py` của `163fd5d` blob sha256
  `dd17b94c…4f83`; Python 3.11.15, git 2.43.0; PATH của chuỗi chỉ gồm `git`, `sort`, `comm`, `wc`, `grep`, `awk`,
  `python`; script ở scratch, không vào kho). Bộ thử trích khối lệnh từ CHÍNH tệp đặc tả (r10; r10 + HINT lượt 10) hay
  từ bản r11, chạy từng dòng trong một tiến trình bash, ghi rc, stdout, stderr và ảnh các tệp tạm sau mỗi bước, rồi
  chấm theo đúng chữ của văn bản ấy. Nó chỉ thay giá trị `T`, hai OID (của kho dựng tại chỗ; r10 và HINT dùng 7 ký tự
  đầu như chính văn bản ấy viết) và danh sách cho phép endpoint (hai URL GitHub đổi thành đường dẫn kho bare). Mỗi
  cặp (kịch bản, văn bản) dựng máy chủ mới; 0 tệp `.pyc`. "g2" là lease còn hạn giữ `ops/lease_publish_test.py`
  trên nhánh đã có tên; "land" là máy chủ land một commit đổi tệp ấy. Ô `CẤP` ở hàng mà máy chủ thật có g2 hay đã
  land là cấp nhầm.

| kịch bản | r10 | r10 + HINT | r11 |
|---|---|---|---|
| S0 đối chứng, máy chủ sạch | CẤP | CẤP | CẤP |
| S1 land; S2 g2; S4 g2 ngay sau `fetch`; S5 g2 sau `ls-remote` | không cấp | không cấp | không cấp |
| S3 `origin` không tồn tại; S1n, S2n quên `fetch` | KXĐ | KXĐ | KXĐ |
| S7a, S7b `origin` là mirror cũ + g2 hay land | **CẤP** | KXĐ | KXĐ |
| S8a `comm` vắng + g2 ngay sau `fetch` | **CẤP** | KXĐ | KXĐ |
| S8b `awk` vắng + g2 ngay sau `fetch` | **CẤP** | KXĐ | không cấp (r11 không dùng `awk`; lệch, đo lại, thấy g2) |
| S8c 300 nhánh, cả hai bước `sort` bị `ulimit -f 4` + g2 ngay sau `fetch` | **CẤP** | KXĐ | KXĐ |
| S9, S10 tag hay nhánh cục bộ `origin/master` trỏ nền cũ, có nhánh `master` + land | không cấp (`CHẶN [12]`, tình cờ) | không cấp | không cấp |
| S9b, S10b như trên, HEAD tách rời, không nhánh cục bộ | **CẤP** | không cấp | không cấp |
| S11 `insteadOf` trong cấu hình kho đổi URL sang mirror + g2 | **CẤP** | KXĐ | KXĐ |
| S12 cùng `insteadOf` qua `GIT_CONFIG_COUNT`/`KEY`/`VALUE` + g2 | **CẤP** | KXĐ | KXĐ |
| S13a `GIT_DIR` trỏ clone của mirror + g2 | **CẤP** | KXĐ | KXĐ |
| S13b `GIT_DIR` trỏ clone thứ hai của máy chủ + g2 | không cấp | không cấp | không cấp |
| S14 `ls-remote` trả rỗng, rc=0 + g2 ngay sau `fetch` | KXĐ | KXĐ | KXĐ |
| S15 `ls-remote` bỏ dòng nhánh có lease + g2 ngay sau `fetch` | **CẤP** | **CẤP** | **CẤP** (giới hạn) |
| S16 `refs/replace` cục bộ thay đầu nhánh có g2 | **CẤP** | **CẤP** | không cấp |
| S17 nhánh mang 7 ký tự đầu OID nền, trỏ master mới + land | **CẤP** | KXĐ (stderr `ambiguous`) | không cấp |
| S18 `ops/lease_publish.py` ở cây làm việc bị sửa, chưa commit + g2 | **CẤP** | **CẤP** | KXĐ |
| S19 clone nông, máy chủ sạch | CẤP | CẤP | KXĐ (chặt hơn; CẤP ở đây không sai) |
| S20 hai giá trị `remote.origin.url`, máy chủ đứng trước, máy chủ sạch | CẤP | CẤP | KXĐ (chặt hơn) |
| S20b hai giá trị, mirror đứng trước + g2 | **CẤP** | KXĐ | KXĐ |
| S21 `wc` vắng, máy chủ sạch | CẤP | KXĐ | KXĐ |
| S24 tầng vận chuyển bỏ riêng dòng `master` + land ngay sau `fetch` | **CẤP** | **CẤP** | KXĐ |
| S25 đường dẫn ở (v) gõ sai + land | **CẤP** | **CẤP** | KXĐ |

  Cấp nhầm: r10 17 kịch bản, r10 + HINT 5 (S15, S16, S18, S24, S25), r11 1 (S15, tầng vận chuyển nói dối, khai ở mục
  *Chuỗi lệnh*). Tái lập đúng bảng của lượt 10 cho S0–S10b, trừ S8c: bộ thử lượt 10 đặt `ulimit -f` cho riêng bước
  `sort` của `mc` (`mc` 4096 byte, `cb` 16362 byte), nên `comm` lệch "tình cờ"; bộ thử r11 cắt cả hai bước `sort` (giới
  hạn cỡ tệp kế thừa cho mọi tiến trình), hai tệp cắt ở cùng byte, và r10 CẤP nhầm.
  **Đột biến gỡ từng chốt của r11** (11:25:02Z–11:26:17Z, cùng bộ thử; gỡ chốt văn bản bằng sửa dòng lệnh, gỡ chốt chấm
  bằng bỏ tiêu chí): bỏ kiểm endpoint ⇒ S7a, S7b, S11, S12, S13a, S20b đều **CẤP**; trả `refs/remotes/origin/master`
  về `origin/master` ở (i), (v), (vi) ⇒ S9b, S10b **CẤP**; rút `NEN`, `M689` về 7 ký tự ⇒ S17 **CẤP** (r11 không có
  quy tắc stderr); bỏ `GIT_NO_REPLACE_OBJECTS=1` ⇒ S16 **CẤP**; bỏ so blob công cụ ⇒ S18 **CẤP**; bỏ dòng `master` ⇒
  S24 **CẤP**; bỏ đếm `v.ls` ⇒ S25 **CẤP**; bỏ `nong` ⇒ S19 CẤP (chốt chẩn đoán). Họ "bước biến đổi không chạy" có
  BỐN lớp chồng nhau: rc từng lệnh, phép đếm `dem`, đếm `command -v`, dòng `master`. Đã đo: bỏ riêng rc, riêng `dem`,
  riêng đếm `command -v`, hay cả ba lớp ấy cùng lúc ⇒ S8a, S21, S8c vẫn không cấp (S14 đo với riêng `dem`: vẫn KXĐ);
  bỏ cả bốn ⇒ S8a, S21, S14 **CẤP** (S8c vẫn lệch tình cờ ở `comm`). Tổ hợp hai lớp chưa đo. Vậy
  mỗi chốt mới có kịch bản riêng làm nó ĐỎ khi bị gỡ, trừ đếm `command -v` (dư thừa với rc và phép đếm, giữ để báo sớm)
  và `nong` (chẩn đoán).
  **Review lượt 11 đo thêm** (12:22Z–12:45Z 01-10; bộ thử phiên soạn chỉ đổi hai đường dẫn tới bản cùng băm; bộ
  thử lượt 10 nguyên byte cộng một lớp phủ chạy đúng từng dòng khối r11 và một bộ chấm đọc từng chữ bảng tiêu chí):
  tái lập bảng trên (r10 17, HINT 5, r11 1) và bảng đột biến; trên kịch bản của lượt 10 chuỗi r11 không CẤP nhầm ca nào.
  Đường mới, máy chủ thật có lease còn hạn giữ `ops/lease_publish_test.py`: (N1) nhánh tên `claude/lease-moi/HEAD` ⇒
  `ai-dang-giu` `CHẶN [12]` (`_cac_ref_cuc_bo` bỏ mọi ref đuôi `/HEAD`, nên tên ấy luôn thiếu trong đệm) ⇒ KXĐ,
  fail-close; (N2) lease `write_set: [ops/]` ⇒ r10, r10 + HINT và r11 đều **CẤP**, cùng kết quả với
  `Ops/Lease_Publish_Test.py` và với mục dạng ánh xạ `{type: prefix, path: ops/}`; (N3) `remote.origin.vcs` trỏ helper
  phục vụ mirror cũ ⇒ cả ba **CẤP** với `endpoint.khop` = `1`. Thêm hai cặp dòng mà HINT lượt 11 đề xuất (`remote.cfg`, `ai-dang-giu ops/`) ⇒ 32
  kịch bản giữ nguyên kết quả, N2 (`ops/`) ⇒ không cấp (rc=11), N3 ⇒ KXĐ (`remote.cfg` 3 dòng); dạng hoa/thường và
  dạng ánh xạ vẫn CẤP. r12 thay hai cặp dòng ấy bằng bước (0) cấu hình và `s5.py`; kết quả ở gạch *Chuỗi lệnh r12 trên
  bộ thử* dưới. Đọc từng chữ thì quy tắc chạy lại của r11 không thoả: S4, S5, S8c ra KXĐ ngay lần đầu,
  còn bộ chấm của phiên soạn đọc theo ý nên chạy lại rồi ra không cấp (đã sửa chữ ở mục *Chuỗi lệnh*).
  **Sự kiện git làm lý lẽ cho chuỗi** (kho tạm, git 2.43.0, 11:1xZ 01-10): `git diff --quiet A B -- <đường dẫn vắng ở
  cả hai>` rc=0; cùng blob khác mode ⇒ `diff --quiet` rc=1, blob OID bằng nhau; nhánh tên bằng 7 ký tự đầu một OID ⇒
  `rev-parse` và `diff` dùng NHÁNH, rc=0, stderr `warning: refname '…' is ambiguous.`; tag tên bằng đủ 40 hex ⇒ git dùng
  OBJECT, cảnh báo tương tự; `command -v git sort <tên vắng> comm` và `command -v git <tên vắng>` đều rc=0; `insteadOf`
  trong cấu hình kho hay qua `GIT_CONFIG_*` ⇒ `git remote get-url --all` in URL đã viết lại và `ls-remote` hỏi đúng URL
  ấy; hai giá trị `remote.origin.url` ⇒ `get-url` in giá trị đầu, `--all` in 2 dòng, `ls-remote` và `fetch` dùng giá
  trị đầu (đo cả hai thứ tự); `GIT_DIR` trỏ kho khác ⇒ `get-url` in origin của kho ấy, `--show-toplevel` vẫn là thư mục
  đang đứng.
- **Chuỗi lệnh r12 trên bộ thử** (phiên soạn r12; lượt cuối, với khối lệnh và `s5.py` trích từ chính tệp này,
  09:30:38Z–09:33:09Z 07-10; lượt trước trên bản khối tách rời cùng nội dung, 08:48Z–08:55Z, cùng kết quả; scratch, không
  vào kho). Dùng NGUYÊN
  `harness.py`, `kich_ban_r11.py`, `kich_ban_moi.py` của lượt 11 (bản của reviewer, sha256 `c5bd5509…`, `880806442…`,
  `c34e48ce…`; khối r11 `chuoi_r11.txt` sha256 `3241aa33…`, khớp từng dòng khối của r11), chỉ đổi `ops/lease_publish.py`
  của máy chủ dựng tại chỗ thành blob của `ab457c6`; thêm `h12.py` (văn bản r11 + HINT lượt 11, chấm bằng bộ chấm r11
  cộng tiêu chí hai cặp dòng của HINT như reviewer lượt 11 viết; văn bản r12, chấm ĐÚNG CHỮ bảng tiêu chí r12, theo thứ tự
  bước) và kịch bản mới của phiên soạn r12. Văn bản r12 trích từ CHÍNH tệp này; `s5.py` chép vào `T` trước mỗi lượt và
  OID mong đợi đọc từ chính dòng tiêu chí của khối. Bộ thử thay đúng bốn thứ: `T`, hai OID (của kho tại chỗ), danh sách
  cho phép endpoint, và dòng `remote.origin.url` của danh sách cho phép cấu hình (cả hai thành đường dẫn kho bare đóng
  vai máy chủ). Môi trường sạch (`HOME` tạm, `GIT_CONFIG_NOSYSTEM=1`, `PATH` chỉ gồm `git`, `sort`, `comm`, `wc`, `grep`,
  `awk`, `python` 3.11.15), nên không có dòng `url.*` nào trừ khi kịch bản đặt. Mỗi cặp (kịch bản, văn bản) dựng máy chủ
  mới; 0 tệp `.pyc`. 32 kịch bản cũ cho cùng một kết quả ở cả ba văn bản và trùng cột r11 của bảng lượt 11 ở trên (CẤP
  nhầm chỉ S15). Kịch bản mới (lease giữ tệp ở hàng N2, N4 và ở N3 trừ ba hàng cuối là `CÒN_HẠN`; ô CẤP ở hàng ấy là cấp
  nhầm; hàng K và ba hàng N3 cuối là máy chủ không có người giữ, CẤP là đúng):

| kịch bản | r11 | r11 + HINT lượt 11 | r12 |
|---|---|---|---|
| N1 nhánh `claude/lease-moi/HEAD` (trước và ngay sau `fetch`) | KXĐ | KXĐ | KXĐ (`CHẶN [12]`) |
| N1, N2, N3 đối chứng (lease exact; không `vcs`) | không cấp | không cấp | không cấp |
| N2 `ops/`; `planned:ops/` | **CẤP** | không cấp | không cấp |
| N2 `Ops/Lease_Publish_Test.py`; `OPS/`; `ops/leaſe_publish_test.py` (U+017F) | **CẤP** | **CẤP** | không cấp |
| N2 `ops` (prefix không `/`) | **CẤP** | **CẤP** | không cấp |
| N2 ánh xạ `{type: prefix, path: ops/}`; `{type: prefix, path: ops}`; `{type: exact, path: ops/lease_publish_test.py}` | **CẤP** | **CẤP** | không cấp |
| N2 chỉ `effective_write_set` giữ tệp | **CẤP** | **CẤP** | không cấp |
| N2 `write_set: ops/` (vô hướng) | **CẤP** | **CẤP** | không cấp |
| N2 `ops/*` (glob); separator ngược | **CẤP** | **CẤP** | không cấp (không diễn giải được ⇒ phủ; separator đổi thành `/`) |
| K `ops/reviews/`; `ops/lease`; `ops/leases/` (không phủ hai tệp) | CẤP | CẤP | CẤP |
| N3 `remote.origin.vcs` trong cấu hình kho; qua `include.path`; qua `GIT_CONFIG_PARAMETERS`; qua `GIT_CONFIG_GLOBAL`; `remote.origin.uploadpack` (cả năm: helper hay chương trình phục vụ mirror cũ + g2) | **CẤP** | KXĐ | KXĐ (`cau_hinh` 3 dòng, khớp 2) |
| N3 `remote.origin.pushurl` vô hại, máy chủ sạch | CẤP | KXĐ | KXĐ (chặt hơn) |
| N3 `url.https://example.invalid/.insteadOf zz:` vô hại, máy chủ sạch | CẤP | CẤP | KXĐ (chặt hơn) |
| N3 hai dòng `url.*` của danh sách cho phép qua `GIT_CONFIG_COUNT`, máy chủ sạch | CẤP | CẤP | CẤP |
| N4 `s5.py` trong `T` bị thay bằng bản in sẵn dòng kết luận, + g2 | không cấp | không cấp | KXĐ (`s5.oid` lệch) |
| N4 như trên, lease `ops/` | **CẤP** | không cấp | KXĐ (`s5.oid` lệch) |

  Cấp nhầm trên 63 kịch bản: r11 20 (S15, mười ba hàng N2, năm hàng N3, N4 `ops/`), r11 + HINT lượt 11 12 (S15 và mười
  một hàng N2), r12 1 (S15, tầng vận chuyển nói dối, khai ở mục *Chuỗi lệnh*). r12 chặt hơn ở hai kịch bản vô hại
  (`pushurl`, `url.*` ngoài danh sách): KXĐ thay vì CẤP, giá của danh sách cho phép.
  **Đột biến gỡ từng chốt mới của r12** (LỊCH SỬ: mô tả `s5.py` r12, OID `2f6bde6c…2e01`, 25 ca; với `s5.py` r13 xem gạch
  *Chuỗi lệnh r13 trên bộ thử* ngay dưới) (09:33:16Z–09:39:21Z trên văn bản trích từ chính tệp này, lặp lại lượt
  08:55:41Z–08:59:18Z cùng kết quả; cùng bộ thử; gỡ chốt văn bản bằng bỏ dòng, gỡ chốt chấm
  bằng bỏ tiêu chí, gỡ phép khớp bằng thay `s5.py` của `T` bằng bản đột biến): bỏ hai dòng `s5` ⇒ cả mười ba hàng N2
  **CẤP**; bỏ ba dòng `cau_hinh` ⇒ năm hàng N3 **CẤP**; bỏ tiêu chí `s5.oid` ⇒ N4 `ops/` **CẤP**. Đột biến phép khớp (mười
  đột biến, mỗi cái thay đúng một chuỗi trong `s5.py`, `assert count == 1`): ở mức đơn vị, cả mười làm ĐỎ ít nhất một ca
  tự kiểm (bỏ case-fold ⇒ ca 4, 5, 6; bỏ NFC cả hai lần ⇒ ca 7; bỏ separator ⇒ ca 12; bỏ `planned:` ⇒ ca 17; bỏ prefix
  ⇒ 8 ca; bỏ ánh xạ ⇒ ca 8, 9; bỏ `effective_write_set` ⇒ ca 10; bỏ vô hướng ⇒ ca 11; mục không diễn giải được thành
  không phủ ⇒ ca 13, 14, 15; tiền tố chuỗi thay prefix thư mục ⇒ ca 18), cùng kết quả ở 3.11.15 và 3.12.3. Ở mức chuỗi,
  với tiêu chí `s5.oid` tắt (bản đột biến khác OID): chỉ đổi phép khớp ⇒ mọi kịch bản N2 và K ra KXĐ (tự kiểm sai ⇒
  rc=12); đổi phép khớp VÀ bỏ các ca tự kiểm nó làm đỏ, dòng `grep` chỉnh theo số ca mới (đột biến hai lớp) ⇒ đúng các
  kịch bản của chốt ấy **CẤP**: case-fold ⇒ ba hàng (`Ops/Lease_Publish_Test.py`, `OPS/`, U+017F); prefix ⇒ bảy hàng (`ops/`, `planned:ops/`,
  `ops`, `OPS/`, hai ánh xạ prefix, vô hướng); ánh xạ ⇒ ba hàng ánh xạ; `effective_write_set` ⇒ hàng ấy; vô hướng ⇒ hàng
  ấy; không diễn giải được ⇒ hàng glob; separator ⇒ hàng ấy; còn tiền tố chuỗi thay prefix thư mục (khớp RỘNG) ⇒ kịch bản
  đối chứng `ops/lease` thành **không cấp** (đối chứng có răng chống khớp quá rộng). Hai đột biến đơn vị không có kịch
  bản chuỗi: NFC (ASCII, mục *Giới hạn*) và `planned:` (bỏ nó thì `planned:` rơi vào nhánh không diễn giải được, tức PHỦ:
  chặt hơn, không cấp nhầm). Vậy mỗi chốt mới có kịch bản riêng làm nó ĐỎ khi bị gỡ; tự kiểm của `s5.py` là lớp thứ hai,
  độc lập với các kịch bản. Sự kiện git làm lý lẽ cho bước (0) cấu hình ở mục *Chuỗi lệnh*.
- **Chuỗi lệnh r13 trên bộ thử** (phiên soạn r13, 12:23:27Z–12:28:03Z 07-10; khối lệnh và `s5.py` trích từ chính tệp này,
  OID mong đợi đọc từ chính dòng tiêu chí của khối; scratch, không vào kho). Dùng NGUYÊN `harness.py`, `h12.py` của phiên
  soạn r12 và kịch bản R1 (`moi_ct.py`), R4 (`moi_ct3.py`) của review lượt 12, chép nguyên byte, thêm `moi_ct5.py` (R5,
  R6) của phiên soạn r13; `tat_ca13.py` chạy 106 kịch bản (63 của phiên soạn r12, R1 10, R4 18, R5 10, R6 5) với `python`
  của chuỗi lần lượt là 3.11.15, 3.12.3, 3.13.12; mỗi kịch bản một máy chủ mới; 0 tệp `.pyc`. Ba bản cùng kết quả: KHÔNG CẤP
  61, KXĐ 36, CẤP 9 = S0, S15, ba hàng K, N3 `url.*` cho phép (sáu hàng sạch hay đã khai, như lượt 12) và ba hàng miền đã
  khai. 91 kịch bản cũ: so TỪNG HÀNG với json của review lượt 12 trên chuỗi đã áp HINT (`cuoi_91_py3.1x.json`), cùng nhãn ở
  cả 91 hàng và cả ba bản (KHÔNG CẤP 56, KXĐ 29, CẤP 6); chỉ hai hàng N4 khác chữ, ở OID mong đợi trong thông điệp KXĐ;
  tức các chốt mới không đổi hàng cũ nào. Cùng 15 kịch bản R5, R6 trên văn bản đã áp HINT (`r13_base.md`, `s5.py` của HINT; 12:22:42Z):

| kịch bản (lease CÒN HẠN giữ `ops/lease_publish_test.py`, trừ đối chứng) | chuỗi đã áp HINT lượt 12 | r13 |
|---|---|---|
| R5 tên tệp chứa LF, CR, NEL hay U+2028, rồi dòng `meta<TAB>` giả trỏ blob lease cũ | **CẤP** | KXĐ (`s5.py` rc=12) |
| R5 tên có LF trần | KXĐ | KXĐ |
| R5 symlink `ln.yaml` trỏ tệp `{lease_id: x}` cùng thư mục | **CẤP** | KXĐ |
| R5 gitlink `ops/leases/sub` của submodule chứa lease | **CẤP** | KXĐ |
| R5 lease ở `ops/lease/`, ở `ops/Leases/`, tên đuôi `.yaml` có dấu cách cuối (miền) | CẤP | CẤP (giới hạn khai) |
| R6 `{type: regex, …}`; `{type: exact, path: ops/khac.py, them: …}`; `{path: …}` thiếu `type`; `….py.` | **CẤP** | không cấp (rc=11) |
| R6 đối chứng `{type: exact, path: ops/lease_publish_test.py}` | không cấp | không cấp |

  **Đột biến gỡ từng chốt của chuỗi r13** (12:31:15Z–12:48:50Z 07-10, `dot13.py`, `python` 3.11 của chuỗi, 1307 lượt, 0
  `.pyc`, thư mục của mỗi lượt xoá bằng `shutil`; đột biến của `s5.py` dựng bằng `dot_bien_s5_r13.py`, mỗi cái thay đúng một
  chuỗi, `assert count == 1`; bản HAI LỚP bỏ các ca tự kiểm mà đột biến làm đỏ, dòng `grep` chỉnh theo số ca còn lại, tiêu chí
  `s5.oid` tắt). Mức đơn vị (3.11.15, 3.12.3, 3.13.12 cùng kết quả; chỉ số ca của `CA` tính từ 0, ca `a`–`f` của
  `bao_goi_git`): bỏ case-fold ⇒ ca 4, 5; bỏ NFC cả hai lần ⇒ 0 ca; bỏ đổi separator (ở `chuan` hay ở `phu`) ⇒ 0 ca; bỏ
  `planned:` ở `phu` ⇒ ca 17; bỏ prefix ⇒ ca 1, 2, 3, 5, 8, 10, 11; bỏ ánh xạ ⇒ ca 8, 9; bỏ `effective_write_set` ⇒ ca 10;
  bỏ vô hướng ⇒ ca 11; không diễn giải được thành không phủ ⇒ 12 ca (6, 7, 13, 14, 15, 25 đến 31); tiền tố chuỗi thay prefix
  thư mục ⇒ ca 18; bỏ dòng gán `lp.GOI_GIT` ⇒ 0 ca (chốt này chỉ có răng ở mức chuỗi); bỏ hạ đuôi ⇒ ca `a`; bỏ bảng chữ ⇒
  ca 13, 25 đến 28; bỏ chốt ngắt dòng ⇒ ca `c`, `d`; chốt ngắt dòng lùi về *chỉ LF* ⇒ ca `d`; bỏ chốt mode ⇒ ca `e`, `f`;
  chốt mode lùi về *chỉ kiểu `blob`* ⇒ ca `f`; bỏ chốt khoá ánh xạ ⇒ ca 30; bỏ chốt `type` ⇒ ca 29; bỏ chốt dấu chấm cuối ⇒
  ca 31. Mức chuỗi (bản hai lớp, trên 59 kịch bản: mười sáu hàng N2 và K, R1, R4, R5, R6; kể dưới là các hàng CẤP ngoài sáu
  hàng luôn CẤP, tức ba hàng K và ba hàng miền R5): case-fold ⇒ hai hàng (`Ops/Lease_Publish_Test.py`, `OPS/`); NFC,
  separator (cả hai chỗ), `planned:` ⇒ không hàng nào (mục lạ rơi vào không diễn giải được, tức PHỦ: chặt hơn, không cấp
  nhầm); prefix ⇒ tám hàng; ánh xạ ⇒ sáu hàng (ba hàng ánh xạ N2, `R4_path_list`, `R4_ews_ngoac`, đối chứng ánh xạ R6);
  `effective_write_set` ⇒ hai hàng; vô hướng ⇒ ba hàng; không diễn giải được ⇒ 22 hàng (N2 `ſ` và glob, 16 hàng R4, bốn hàng
  R6); tiền tố chuỗi ⇒ đối chứng `ops/lease` thành **không cấp**; bỏ dòng gán `lp.GOI_GIT` ⇒ mười ba hàng (sáu R1, bốn R5
  tiêm dòng, tên LF trần, symlink ánh xạ, gitlink); bỏ hạ đuôi ⇒ `R1_ext_hoa`; bỏ bảng chữ ⇒ tám hàng (glob N2,
  `R4_glob_docs` và sáu hàng nhiều đường dẫn hay dấu cách); bỏ chốt ngắt dòng ⇒ bốn hàng R5 tiêm dòng; *chỉ LF* ⇒ đúng hai
  hàng R5 NEL và U+2028 (LF và CR vẫn bị bắt, vì `GOI_GIT` đổi CR thành LF); bỏ chốt mode ⇒ symlink ánh xạ và gitlink; *chỉ
  kiểu `blob`* ⇒ đúng symlink ánh xạ; bỏ chốt khoá ⇒ `R6_khoa_them`; bỏ chốt `type` ⇒ `R6_type_regex`, `R6_thieu_type`; bỏ
  chốt dấu chấm ⇒ `R6_cham_cuoi`. Đột biến văn bản: bỏ hai dòng `s5` ⇒ 48 trong 53 hàng N2, R1, R4, R5, R6 (ngoài sáu hàng
  luôn CẤP) CẤP, năm hàng còn lại là bốn đối chứng R1 và đối chứng ASCII của R4, mà công cụ nền tự thấy; bỏ ba dòng
  `cau_hinh` ⇒ cả tám hàng N3 CẤP; bỏ tiêu chí `s5.oid` với đồ giả của r12 (in `25/25`) ⇒ N4 vẫn KXĐ vì dòng `grep` `38/38`
  bắt trước; với đồ giả in đúng dòng của r13 (`n4_13.py`, 12:49Z) ⇒ có tiêu chí `s5.oid`: KXĐ ở cả hai hàng N4; tắt tiêu chí:
  hàng prefix `ops/` **CẤP**, hàng exact không cấp (dòng `ai-dang-giu` tự thấy). Vậy mỗi chốt có kịch bản riêng ĐỎ khi bị
  gỡ, trừ NFC, đổi separator và bỏ `planned:`: ở r13 ba chốt ấy không còn răng về an toàn, vì bảng chữ đã đẩy mọi mục
  chúng từng xử lý sang nhánh PHỦ; chúng chỉ giữ cho mục ASCII hợp lệ được so đúng (tính sống; `planned:` còn ca tự kiểm 17).
  **Đo trực tiếp các đường F12-1a** (`do_f1a.py`, 33 ca, mỗi ca một kho máy chủ riêng, lease CÒN HẠN giữ
  `ops/lease_publish_test.py` trừ hai đối chứng; công cụ nền, `s5.py` của HINT và `s5.py` r13 chạy trên cùng kho;
  12:57:29Z–12:57:53Z 07-10, python 3.11, 0 `.pyc`): công cụ nền rc=0 ở 25 ca, rc=11 ở 3, rc=12 ở 5; `s5.py` của HINT rc=0
  ở 19 ca (tám ký tự ngắt dòng, hai trong số ấy lặp lại với `core.quotePath=false`, symlink ánh xạ, gitlink, bốn hình dạng
  R6, ba ca miền); `s5.py` r13 rc=0 chỉ ở ba ca miền, rc=11 ở 13, rc=12 ở 16, rc=1 ở tên không phải UTF-8.
- **Phiên soạn r15 đo lại** (07-10; scratch, không vào kho; `PYTHONDONTWRITEBYTECODE=1`). (a) Áp HINT lượt 14 lên bản
  chép r14 (`ec4d97f5…b0ed`): `patch -p0 --fuzz=0 --dry-run --verbose` rồi `patch -p0 --fuzz=0 --verbose`, cả hai rc=0, 4/4
  hunk, 0 fuzz, 0 offset, 0 `.orig`/`.rej`; sau áp sha256 `55fd69a5…c20d`, 2669 dòng, bằng `SPEC_moi.sha256` của reviewer
  lượt 14. (b) Biến thể của reviewer lượt 14 dựng lại bằng chính script của reviewer (`dung_rv14.py`, `dung_e8p.py`,
  `dung_v1_dau.py` trên blob `7dd06ab`): 10/10 khớp `bien_the.sha256`. (c) Phép quét động và oracle: A8, đoạn *Phiên soạn
  r15 đo lại*. (d) Số mới của review lượt 14 mà r15 giữ (đoạn *Review lượt 14 đo*): thời gian và khung giờ quét đủ khớp
  hiện vật `du_3.11.json`, `du_3.12.json` của reviewer; mọi tập và kết cục đo lại bằng `chay15.py` và `lap5_r15.py`.
- **Phiên soạn r14 đo lại** (07-10; scratch, không vào kho; `PYTHONDONTWRITEBYTECODE=1`). (a) Áp HINT lượt 13 lên bản
  chép r13 (`711b7b74…4bb1`): `patch -p0 --fuzz=0 --dry-run --verbose` rồi `patch -p0 --fuzz=0 --verbose`, cả hai rc=0, 4/4
  hunk, 0 fuzz, 0 offset; sau áp sha256 `38eeafbf…8758`, 2556 dòng, bằng `SPEC_all.md` của reviewer lượt 13. (b) Phép quét
  động và oracle: A8, đoạn *Phiên soạn r14 đo lại vế lật*. (c) Ảnh 473 ref của r13 dựng lại (`do_anh_r13.py`, chạy từ gốc
  `adg2`, 15:07:56Z–15:08:15Z): `refs/heads/master` = `ab457c6` cộng 472 dòng `may_chu.raw` của lượt chạy thật r13, OID đọc
  thẳng từ object DB của `adg2`, nhãn hạn ở mốc 12:18:00Z. Tái lập đúng mọi số r13 khai: 473 ref, 3986 đường dẫn, 0 ký tự
  ngoài bảng, 589 cặp, 0 lỗi parse, 1384 + 23 = 1407 mục `write_set`, 123 mục `effective_write_set`, 0 mục ánh xạ, 0 đoạn
  chấm cuối, 0 mục không diễn giải được, 59 cặp thiếu cả hai khoá (cả 59 `HẾT_HẠN`), 6 cặp `CÒN_HẠN` (wp685, wp710) không
  chạm hai tệp, 37081 mục cây dưới `ops/leases/` đều `100644 blob`, 4 tên `.yaml.nhap` trên 286 đến 296 ref, 299 cặp YAML
  ngoài `ops/leases/` có `lease_id` (cả 299 dưới `ops/reviews/`, 0 cặp giống lease), 2766 đường dẫn trên cây `ab457c6`, 6
  biên nhận `wp678-spec-review-*`. Phân rã thêm: 23 cặp có khoá `effective_write_set` = 21 danh sách khác rỗng + 2 `null`
  (0 danh sách rỗng); 59 = 39 `scope_files` + 6 `scope_files_can_xet` + 6 `delta_scope_files` + 8 không trường phạm vi
  (bốn nhóm rời nhau). (d) Mười một dạng tên tệp (`ten_tep_11.py`: cùng mười một tên và cùng lease với
  `tai_hien_ten_tep_s5.sh` của lượt 12, `s5.py` trích từ r13, 15:09:03Z–15:09:12Z): rc=11 ở chín, rc=12 ở LF trần, rc=1 ở
  tên không phải UTF-8. (e) Số r13 tự khai mới so với r12 (`kiem_so_r13.py`: 75 phép so trên git của worktree soạn và `adg2`,
  VERDICT và HINT lượt 12, readback REST #678, hiện vật của phiên soạn r13, ảnh ở (c), ba bản Python): 72 KHỚP, 3 lệch,
  đúng bốn chỗ r14 sửa (§9, mục (5)). KHỚP gồm: dòng dõi r12; ba bản `s5.py` (112 dòng 25 ca, 174 dòng 31 ca, 207 dòng 38
  ca); hiện vật lượt chạy thật 13:12Z (46 bước rc=0, 472 dòng, 75 và 123 dòng lease, (iv) 56 giây, cả chuỗi 58 giây); tọa độ
  PROTOCOL; ba lệnh `coord`; mười ba code point và comprehension ở ba bản; fixture A7 (rc=10 rồi rc=0 ở mười một dạng); bốn
  dạng R6 qua `kiem()`; `core.protectNTFS`; 106/61/36/9 ở ba bản và 91 hàng cũ (56/29/6, chỉ N4 hai lần khác chữ); R1 trên
  r12 (6 CẤP, 4 không); bảng R5/R6; 1307 lượt, 21 đột biến đơn vị từng hàng ở ba bản, các hàng mức chuỗi và đột biến văn
  bản; 33 ca; phủ chéo 19/7/6/1/5/0; đột biến (S) 18/7/2/1; baseline quét đủ. Không so: tải máy 6,8 ở lượt chạy thật và lượt
  `n4_13.py` 12:49Z (không có hiện vật), cùng các mốc giờ ngoài các hàng trên.
- **Tương tác với wp709, packet land ngay trước r12** (đo r12 trên `ab457c6`; hàng nền nghiệm thu, §2, §4, A1, A2, A8,
  ghi chú dưới closure). Rà theo bài học *tương tác với packet vừa land*, từng chỗ của packet này mà wp709 có thể chạm:
  (1) **nghĩa vụ `t70`/`t193`/sổ/helper** (§4): wp709 thêm ba ca `t01_*` không tham chiếu helper nào; `t70`, `t193`, sổ,
  hai helper, `_ca_doc_than_buoc`, `_ca_ung_vien_gian_tiep`, `main`, `_chay_main_meta` giống hệt thân (so `ast`); D, R, G,
  sổ và hai literal không đổi; ba ca mới đạt dưới seam `nt` (N, K, H không chứa chúng); đột biến `t70` cho cùng bảng ở
  3.11, 3.12, 3.13 (A2). Một tiền lệ đáng nhớ: wp709 đặt bốn ca chung tiền tố `t01_`, nên `--chi-ca=t01_` nay chọn bốn ca
  (wp709 sửa `t153`, `t155` sang tên đầy đủ); hai literal của `t70`, `t193` so đa tập tiền tố, nên ca mới của packet này
  không dùng lại tiền tố đã có (§4). (2) **`_lease_cham_duong` (F11-1)**: không đổi, chỉ dời :545–549 → :704–708; vì vậy
  khuyết tật khớp nguyên chuỗi còn nguyên trên nền mới và `s5.py` vẫn cần (mục *Chuỗi lệnh*). `_quet_lease_toan_kho`,
  `lenh_ai_dang_giu`, `_cac_ref_cuc_bo` cũng giống hệt thân. (3) **`kiem()` của cổng đăng**: thêm `_kiem_provider_identity`
  TRƯỚC D1 — tương tác thật: mẫu lease A1 cũ ra rc=10 ở mọi dạng (A1 đổi fixture), và lease `wp678` không được khai
  `assurance_target` chứa `cross_approved` (ghi chú dưới closure). A3 (bước `đăng`, lease dựng bằng `_yaml_that`), A5 (riêng D5,
  gọi thẳng), A6 và A7 (`ai-dang-giu --du-bao`) cho cùng kết quả ĐỎ trên hai nền; `check --du-bao` của A7 đi qua `kiem()`
  nên fixture của nó cũng phải qua luật danh tính, như A1. (4) **Hợp đồng biên nhận
  và closure**: `ops/bien_nhan_v2.py` và `ops/bien_nhan_v2_test.py` giống hệt; `_thieu`, `kiem()`, CLI cho cùng các số trên
  `ab457c6` (ghi chú dưới closure); `required_checks` trỏ bốn job `gate`, `gate-ops`, `gate-registry`, `gate-packet-loop`
  và workflow `thu-hoi` (`ops-thu-hoi-admission.yml`, `name: thu-hoi`), đều còn trên `ab457c6`; gate land `human_audited`
  (PROTOCOL :607–608 trên `ab457c6`) không đổi chữ; PROTOCOL mới chỉ cho `human` làm reviewer với `human_audited` (:266–272)
  và cấm `cross_approved` khi cùng họ (:11–12), khớp với closure (review `review_deferred` cùng họ, land
  `human_audited`). (5) **Ruff**: hai `F841` mới của wp709 ở `ops/lease_publish.py` (A8, §8), ngoài objective. (6) **Người
  giữ**: lease executor g2 của wp709 còn hạn tới `2026-10-07T10:30:00Z` sau khi land (hàng `depends_on`).
- **Tương tác với #687, packet land ngay trước r10** (đo r10 trên `163fd5d`, A2, A8). #687 thêm sổ `SO_BO_QUA` và ca
  `t193`, nên từ nền này có **hai** chốt kiểm kê cho các ca dùng `_chay_buoc_dang*`: `t70` (tĩnh, tham chiếu trực tiếp ở
  cấp đỉnh) và `t193` (chạy thật dưới nền `nt` mô phỏng, ca nào ném `BoQuaNen` phải có trong sổ và literal). Hai tập
  khác nhau ngay trên nền: `t199` thuộc `mong` mà không thuộc sổ (tự bắt `BoQuaNen`), `t202` thuộc ứng viên gián tiếp
  của `t193` mà không thuộc `mong` (tham chiếu ca `t195`). Nghĩa vụ (iii) của §4 và phép đo G − D của A8 sinh ra từ đây. Review lượt 10 đo thêm (10:25:11Z–10:28:08Z 01-10; 39 biến thể × 3.11/3.12/3.13 trên bản sao `git archive 163fd5d`; ca mới mang số `t204`): tái lập đủ bảng của A2, kể cả ở 3.13; bảy đường GỌI THẬT helper (`globals()` theo tên, `functools.partial`, bí danh cấp module, lambda trong hàm bọc, decorator đóng gói helper, tham số mặc định, phương thức lớp) cho `t70` `1/1`, `t193` `1/1`, D 13, G − D `{t202}` và tập chỉ lồng `{t70}` y như nền ở cả ba bản, trong khi `main()` dưới seam `nt` ĐỎ NGOÀI SỔ; hàm bọc gọi helper trong list comprehension làm `t193` ở 3.11 ngược 3.12 (G thấy ca ở 3.12 và 3.13, không ở 3.11). Phép quét động của A8 bắt cả tám ở 3.11 lẫn 3.12 và không bắt nhầm ca làm đúng (i)–(iii) hay ca tự bắt `BoQuaNen`.
  **Phiên soạn r11 đo** (11:10Z–12:11Z 01-10; clone đầy đủ `163fd5d` từ `adg2`, chạy từ gốc, `python` và `python3`
  trỏ đúng bản đang đo, `PYTHONDONTWRITEBYTECODE=1`; mỗi biến thể chép đè `ops/lease_publish_test.py` của bản sao rồi
  kiểm sha256, đo xong chép trả nền rồi kiểm `status --porcelain --ignored` 0 dòng và 0 tệp `.pyc`; script ở scratch,
  không vào kho). Biến thể chèn ca `t204_moi` ngay trước `def main(` như `dotbien.py` của lượt 10: dùng lại tệp biến thể
  N1–N8, R11–R13 của lượt 10, thêm M1 (`eval("_chay_buoc_dang_that")(…)`), M2 (`getattr(sys.modules[__name__], …)`),
  M3 (bảng dict cấp module), M5 (gọi helper trong `threading.Thread`, rồi kiểm kết quả), M6 (lời gọi cấp đỉnh trong
  `try`, `except Exception` ném lại `AssertionError`; có tiền tố trong `mong`), M7 (gọi cấp đỉnh, có `mong`, sổ và
  literal: làm đúng); M1–M7 gọi `_chay_buoc_dang_that(_yaml_that("wp-ok-1"))` như `t198`.
  Đo nhanh (`--chi-ca=t70_`, `--chi-ca=t193_`, `--chi-ca=t204_`, cộng phép quét chỉ ca `t204`; 3.11.15 và 3.12.3, 11:10:30Z–11:11:42Z):
  N1–N8, M1, M2, M3 ⇒ `t70` `1/1`, `t193` `1/1` (trừ N5 ở 3.12: `t193` `0/1`), `t204` đạt dưới posix, `t204` thuộc N mà
  không thuộc D; R13 ⇒ `t193` `0/1` (ứng viên gián tiếp bắt) và cũng vào N − D; M5, M6 ⇒ `t70` `1/1`, `t193` `1/1`, `t204`
  đạt dưới posix, N KHÔNG chứa `t204`, K chứa `t204` (`TinHieuChotCa` ở M5, `AssertionError` ở M6); M7 và R11 đủ cả ba vế (làm đúng) ⇒
  `t204` thuộc N, N − D rỗng, K không chứa `t204`; R12 tự bắt có `mong` ⇒ N, K đều không chứa `t204`. `main()` dưới seam
  `nt` (`probe.py` của lượt 10 trên cây `git archive 163fd5d` tối thiểu, ca `t204_moi`, sổ mặc định; 3.11 và 3.12 cùng
  kết quả): M1, N3 ⇒ rc=1, *"bỏ qua NGOÀI SỔ"*; M5 ⇒ rc=1, *"t204_moi: []"*; M6 ⇒ rc=1, *"helper hong: BoQuaNen"*; M7 ⇒
  rc=0, *"BỎ QUA t204_moi"*.
  Quét đủ mọi ca, bản không đặt `ops/` đầu `sys.path` (`quet_nt.py` của lượt 10, sha256 `9fc0ca4b…acc`, mở rộng để in thêm
  tên ca của K và D; phần tính N, N − D giữ nguyên từng dòng; ba lượt song song, 11:12:03Z–11:58:11Z): nền 3.11.15 hai
  lượt (529,3 và 509,3 giây) và 3.12.3 (613,7 giây) ⇒ N đúng 12 ca của sổ, đúng cặp, N − D rỗng, K đúng 11 ca, cùng tập
  ở cả ba lượt (`t32`, `t35`–`t40`, `t152`, `t155` ném `ModuleNotFoundError`; `t199`, `t203` ném `TinHieuChotCa`); N3
  (3.11, 3.12) và N5 (3.11) ⇒ N − D = `{t204}`, K bằng nền; M5 và M6 (3.11, 3.12) ⇒ N bằng sổ, N − D rỗng (hai vế của
  HINT ĐẠT), K bằng nền cộng `t204`; M7 (3.11, 3.12) ⇒ N bằng sổ cộng `t204`, N − D rỗng, K bằng nền; R12 tự bắt mà vẫn
  thêm vào sổ và literal (3.12) ⇒ N khác sổ (thừa `t204`) và K có thêm `t193` (chính `t193` ĐỎ). Chín ca
  `ModuleNotFoundError` là tạo tác của cách nạp: chúng `import bash_nen`, tìm được khi chạy `python
  ops/lease_publish_test.py` (thư mục `ops/` đứng đầu `sys.path`) mà không tìm được khi phép quét nạp module từ thư mục
  khác. Bản thêm đúng dòng `sys.path.insert(0, <gốc>/ops)` (bốn lượt, 11:39:55Z–12:10:43Z): nền 3.11.15 (548,6 giây)
  và 3.12.3 (422,6 giây) ⇒ N đúng 12 ca của sổ, N − D rỗng, K chỉ còn `t199`, `t203`; M6 (3.11, 454,4 giây) ⇒ K thêm `t204`
  (`AssertionError`); M5 (3.12, 419,9 giây, chạy một mình) ⇒ K thêm `t204` (`TinHieuChotCa`). Vậy K phụ thuộc cách quét, và (q3) phải so nền với ứng viên trong cùng một lệnh.
  `t125` và `t203` (thêm hoặc đổi bởi #687) lấy danh sách ca động từ `CA`, không ghim literal nào mà ca mới phải sửa.
  `t193` chỉ MÔ PHỎNG nền `nt` (seam `nen='nt'`); hành vi trên Windows thật: `KHÔNG ĐO ĐƯỢC` ở phiên soạn r10. Đặc tả
  #687 (`ops/specs/lease-publish-windows-do-r1.md`…`-r3.md`) không được đọc ở lượt ấy; nghĩa vụ trên dựa vào mã và phép
  đo trên `163fd5d`, không dựa vào lời đặc tả ấy. Phiên soạn r11 đọc r3 (`ops/specs/lease-publish-windows-do-r3.md`,
  sha256 `d4d6715d…543e`, commit tạo `050e625`): M2 đòi sổ *"Phải đo bằng chạy thật, không suy từ tên"*, và docstring
  `t193` ghi #687 đã đo sổ bằng *"phép quét MỌI ca ngoài suite"*; phép quét động ở A8 là đúng phép đo ấy, giữ ngoài
  suite như tiền lệ.
- **KHÔNG ĐO LẠI ở r10 khi dời nền** (giữ số cũ kèm nhãn của chúng): phép đo ĐỎ của A5, A6, A7 (lần cuối ở review
  #679 và lượt 1); bullet *Miền con trỏ trong runtime* của §8 (10:49Z 29-09); bảng §1 và số dòng §2 (trên `1741e0a`);
  fsck kho soạn và số quét lease r4 (tham khảo, §8). Lý do: chúng chỉ phụ thuộc `ops/lease_publish.py`, mà blob ấy
  giống hệt giữa `1741e0a`, `89fc4fa`, `20ec8d5` và `163fd5d` (`git diff --quiet` rc=0, sha256 `dd17b94c…4f83`), hoặc
  không phụ thuộc nền; đó là suy luận từ băm, không phải phép đo lại. r11 không dời nền; mọi số đo trên `163fd5d` giữ từ
  r10, đã được review lượt 10 tái lập (VERDICT lượt 10, bảng đo). **r12 dời nền sang `ab457c6`, nơi blob
  `ops/lease_publish.py` KHÁC** (khối danh tính của wp709), nên lý do *"blob giống hệt"* không còn đứng cho nền mới:
  phiên soạn r12 đo lại phép đo ĐỎ của A1, A3 (A1, A3), của A5 riêng D5, A6 và A7 (A5–A7; kho tạm, 09:05:44Z 07-10) trên
  cả `ab457c6` lẫn `163fd5d`, cùng kết quả ĐỎ (A1 chỉ khi fixture qua luật danh tính). Bảng §1, số dòng §2 (trên
  `1741e0a`, kèm tọa độ trên `ab457c6`), fsck kho soạn, số quét lease r4 và bullet *Miền con trỏ* giữ nhãn cũ: các hàm
  của chúng giống hệt thân giữa `163fd5d` và `ab457c6` (so `ast`), chỉ dời dòng.
- **Q13: neo là một bản chiếu, không phải hiện vật của câu trả lời.** #682 comment `5928886724` do phiên điều phối đăng
  sau quyết định (09:44:15Z 01-10) và tự ghi *"Kho không có hiện vật nào đo được câu trả lời này"*; phiên soạn r10 chỉ
  đo được rằng bản chiếu ấy khớp từng byte văn bản điều phối giao (§3), không đo được câu trả lời của chủ kho.
- **Trần vòng review (quan sát ngoài phạm vi chấm của VERDICT).** `docs/adr/0048-tran-vong-review-len-muoi.md`
  (Trạng thái: Accepted 2026-09-12) đặt trần mười vòng review hợp lệ cho một PR packet, vượt trần phải khai khối
  `nang_tran`; VERDICT lượt 10 (hướng 13) đo thêm rằng một vòng chỉ được tính khi có biên nhận hợp lệ. Phiên soạn r11
  đếm trên `7e5958e`: 6 tệp `ops/reviews/wp678-spec-review-*-codex-verdict.receipt.yaml` (lượt 1–6); lượt 7–10 chưa có
  biên nhận trên master. Lượt review của r11 là lượt thứ 11 của chuỗi đặc tả; nếu lượt 7–10 được ghi biên nhận hợp lệ
  thì nó là vòng 11. Chuỗi review ĐẶC TẢ (sáu lượt trên PR #679, bốn lượt cục bộ) có thuộc trục ấy không, và có cần
  khối `nang_tran` không: phiên soạn r11 không đánh giá, `KHÔNG ĐO ĐƯỢC`. Q13 là quyết định về §12, không phải khối
  `nang_tran`. Phiên soạn r12 đếm trên `ab457c6`: vẫn 6 biên nhận `wp678-spec-review-*` (lượt 1–6); lượt 7–11 chưa có
  biên nhận trên master. Lượt review của r12 là lượt thứ 12 của chuỗi đặc tả; đánh giá trục ấy vẫn `KHÔNG ĐO ĐƯỢC`.
  Phiên soạn r13 đếm trên `ab457c6` (`adg2`, 13:0xZ 07-10): vẫn 6 biên nhận `wp678-spec-review-*` trên master, và cũng
  đúng 6 tên biên nhận `wp678` khi quét `ops/reviews/` của cả 473 ref theo dõi; lượt 7–12 chưa có biên nhận ở đâu trong
  `adg2`. Lượt review của r13 là lượt thứ 13 của chuỗi đặc tả; VERDICT lượt 12 (Lưu ý 2) xin phiên điều phối hỏi chủ kho
  trước khi ghi biên nhận lượt 7–12 và trước khi mở r13; đó là việc của điều phối, phiên soạn r13 không đánh giá trục ấy,
  `KHÔNG ĐO ĐƯỢC`. Phiên soạn r14 đếm trên `adg2` sau `fetch --prune` (mọi ref `refs/heads` và `refs/remotes`, 15:19:48Z
  07-10): vẫn 6 biên nhận `wp678-spec-review-*` trên `ab457c6` và chỉ chừng ấy tên biên nhận `wp678` trên mọi ref; lượt 7–13
  chưa có biên nhận. Lượt review của r14 là lượt thứ 14 của chuỗi đặc tả; trục ADR-0048 vẫn là việc của điều phối,
  `KHÔNG ĐO ĐƯỢC` với phiên soạn r14. Phiên soạn r15 đếm lúc 17:19:12Z 07-10: trên `ab457c6` qua REST (`git/trees` đệ quy,
  `truncated` false) vẫn 6 biên nhận `wp678-spec-review-*`, và trên 476 ref của `adg2` (`FETCH_HEAD` 17:17:01Z) chỉ chừng
  ấy tên `wp678` dưới `ops/reviews/`; lượt 7–14 chưa có biên nhận. Lượt review của r15 là lượt thứ 15 của chuỗi đặc tả;
  trục ADR-0048 vẫn là việc của điều phối, `KHÔNG ĐO ĐƯỢC` với phiên soạn r15.
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
  r7 (sai từ lúc ghi: bản PR #689 land theo là r8 của đặc tả #677, soạn 29-09, vào master qua bookkeeping #699; xem A2); mã của #677 land ở `20ec8d5` (xem A2, tọa độ r8).
- Trạng thái máy chủ GitHub ngoài `ls-remote`: không đo ở r6 (REST tới `repos/…` bị proxy chặn ở phiên soạn
  r6). Phiên soạn r7 gọi được REST `repos/…` (HTTP 200, có `X-Github-Request-Id`), chỉ để đọc Q10 và #682. Phiên soạn
  r8 cũng gọi được (HTTP 200, có `X-Github-Request-Id`), chỉ để đọc Q11, Q8, #682, PR #689 và #678 comment
  `5912542067`. Phiên soạn r9 gọi REST không token (HTTP 200, có `X-Github-Request-Id`), chỉ để đọc #682 (thân và
  comment, Q12), PR #689 và các comment của #678. Phiên soạn r10 gọi REST không token (HTTP 200, có
  `X-Github-Request-Id`), chỉ để đọc PR #701, #678 comment `5925743728`, #682 comment `5928886724`, các comment của #678 và #682 từ 06:00Z 01-10, và
  thân #682. Phiên soạn r11 gọi REST không token (HTTP 200, có `X-Github-Request-Id`), chỉ để đọc các comment của #678
  từ 10:00Z 01-10 và thân #682; `fetch` và `ls-remote` tới GitHub chỉ chạy trong `adg2`. Phiên soạn r12 gọi REST qua
  `gh api` (client GitHub tích hợp của phiên, đi qua proxy của phiên; HTTP 200, có `X-Github-Request-Id`), chỉ để đọc:
  #678 comment `5932137088`, các comment của #678 từ 12:00Z 01-10 (1 comment, chính nó), thân #682 và các comment của
  #682 từ 10:00Z 01-10 (0 comment), PR #712, và Issue #685, #686 cùng các comment của #686 (theo chỉ thị của phiên
  điều phối); `fetch` và `ls-remote` tới GitHub chỉ chạy trong `adg2`.
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
