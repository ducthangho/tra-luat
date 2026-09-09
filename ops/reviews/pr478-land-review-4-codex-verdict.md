verdict: changes_requested
reviewed_sha: 5a4dd859ef791ca046aea3af4bab2731883323ec
base_sha: 802fc01b5db866478459dbc4a65d008a38619898
reviewed_tree: ec6b886b396ac8ec05c7e1949a5fb10cdd63680f

Không phát hiện P1. Có **3 P2 về lời khai cần sửa** và **13 P3**, trong đó 2 P3 về giới hạn/chỗ vá còn sót, 11 P3 ghi nhận **khẳng định đúng nhưng bảng điều phối bỏ sót**, theo yêu cầu lượt này. `changes_requested` yêu cầu sửa hồ sơ; ba P2 không được nâng thành điều kiện chặn land theo thang phân hạng đã giao. Không phát hiện hồi quy ở các cổng đã chạy.

Reviewer: Codex/OpenAI, thực thi lệnh cục bộ bằng công cụ shell; không có nguồn độc lập để xác nhận tên model/effort cụ thể của phiên này. Executor được khai là Claude. Chỉ dùng nội dung trong gói, không gọi mạng, không đọc transcript ngoài gói, không tự soạn payload tấn công, không commit/push. Không sửa nội dung tracked của `cay-kho/`.

Các đường `ops/...`, `docs/...`, `.github/...`, `CLAUDE.md` dưới đây tính từ `cay-kho/`. Mọi lệnh bắt đầu `python3 -B do-luot4/...` chạy từ **gốc gói**. Script và kết quả thật nằm trong [do-luot4](do-luot4/); các phép đo có thể chạy lại bằng [audit.py](do-luot4/audit.py) và [run_checks.py](do-luot4/run_checks.py). Worktree `do-luot4/master/` là bản đo riêng, detached tại đúng base SHA.

## ĐỐI CHIẾU LƯỢT TRƯỚC

**Không có verdict gốc lượt 1–3 của #478 để đối chiếu đầy đủ.** Quét tên đường dẫn trong `git rev-list --objects --all` của cả `cay-kho` và `kho.git` không có `pr478`/`478-verdict`. Điều này chỉ chứng minh không tìm được đường dẫn ấy trong snapshot; không chứng minh GitHub không có comment. Lời khai `get_comments` trả mảng rỗng: **KHÔNG ĐO ĐƯỢC**, không có mạng/snapshot phản hồi.

Tôi đối chiếu các đính chính hiện hành và thông điệp commit `8f7becb`, `260f7c6`, `5a4dd85`. Đây là **kiểm lời khai “đã vá”**, không giả làm đối chiếu nguyên văn finding của reviewer trước.

- `land-operator-khong-co-neo`: **ĐÃ VÁ THẬT về phân loại nguồn** — dòng 37–44 đã ghi attestation, thiếu JSON thô và không độc lập xác minh `merged_by`. Git object có author `notebyme88`, committer `GitHub`; không chứng minh actor thao tác. Danh tính merge trên GitHub vẫn **KHÔNG ĐO ĐƯỢC**. Giới hạn toàn tệp còn thiếu ở P3 giữ nguyên slug bên dưới.
- `sai-p1-theo-luot`: **ĐÃ VÁ THẬT** — đếm heading finding trên chín verdict cho đúng `{7:4,8:2,9:1,10:1,11:1,12:2,13:0,14:0,15:0}`. Lượt 11 có tiêu đề nội bộ “lượt 10”, nhưng `DOC-MANIFEST.md` giải thích đánh số lại khi vận chuyển; không tự loại nó như bản trùng.
- `cross-review-14-15-thieu-hien-vat`: **ĐÃ VÁ THẬT ở head này** — đủ hai verdict, mục lục, receipt v2; manifest `59/59` và `45/45`, rc=0. `bien_nhan_v2` báo 30 ĐẠT v2, 0 vi phạm; lease trên head `121/121`, bỏ qua 0. Không còn hai hồi quy cổng mà thông điệp commit tự khai. Cổng xác minh blob/ancestry không chứng minh GitHub giữ URL vĩnh viễn; receipt đã khai giới hạn đó.
- `bookkeeping-spec-thu-hoi-da-cu`: **ĐÃ VÁ THẬT khi đối chiếu ref trong gói** — tip `2aee80a2ff6a088ff39a2a8bc882db978df64c75`, commit UTC `2026-09-07T22:53:12Z`, spec revision 6, `packet_issue: CHƯA CÓ`, §0 ghi hết 6/6 và checkpoint thuộc chủ kho. Tình trạng review/Issue trên máy chủ sau snapshot không kiểm được.
- `sai-dem-diff-head-chua-review`: **ĐÃ VÁ THẬT** — đúng một commit `17f4a1b` sau `745d888`; hai tệp, `+23/−8`, đều trong `ops/reviews/`. Việc vá đã đóng *toàn bộ* P3 hay chưa là câu khác, xem finding riêng.
- `role-khong-dung-contract-v1`: **ĐÃ VÁ THẬT về trường role** — `role: land_operator` khớp mẫu ở `docs/PROTOCOL_DA_PHIEN.md:466`; thông tin ghi hộ chuyển sang `recorded_by`. Không suy schema parse được thành approval hợp lệ.
- `ly-do-khong-do-ci-bo-sot-duong-actions`: **ĐÃ VÁ THẬT về mức lời khai** — CI gắn nhãn attestation, rút câu exact head; `CLAUDE.md:583` thực sự nhắc endpoint riêng. Tĩnh có đúng 6 điều kiện sai trên push/master/windows. Việc điều phối thực sự probe endpoint, số job/bước và trạng thái API: **KHÔNG ĐO ĐƯỢC**.
- `bookkeeping-a9-ha-ket-luan-thanh-cau-hoi`: **ĐÃ VÁ THẬT** — bốn thời điểm cấp, bốn hash, revision 1/2/3/4 và generation đều 1 khớp YAML; cả bốn trước hạn #456. ADR-0034 có điều khoản đổi contract phải revision + generation mới. Lời khai hiện phân biệt vi phạm cấp sớm với quyết định xử lý còn thiếu và không suy đã thi công runtime trái phép.
- `bien-nhan-14-15-gan-doi-so-model-vao-run-json`: **ĐÃ VÁ THẬT trong hai receipt** — cả hai đã gọi model/effort/thread là attestation; `run.json.lenh` chỉ có `chuong_trinh`, `so_doi_so`, `van_tay`. Tuy nhiên tiêu đề land evidence còn khai model/effort không kèm giới hạn; tính vào P3 dưới đây, không coi nguồn model đã được bổ sung.
- `land-evidence-gioi-han-chua-phu-het-loi-khai`: **CHƯA VÁ trên phạm vi tự kiểm được** — dòng 37–44 chỉ giới hạn một nhóm nguồn, chưa bao phủ các câu hiện hành ở 24–31, tiêu đề 58 và bookkeeping 194–196. Không có verdict lượt 3 để bảo đảm đây là toàn bộ phạm vi finding cũ.

## BẢNG ĐO

Ký hiệu: **khớp nguồn** nghĩa là nội dung hiện vật khớp lời khai; không mặc nhiên xác thực lần chạy lịch sử. **Đo mới** là lệnh reviewer thực chạy. **Không đo được** không phải pass hoặc fail. `BS` là mục không xuất hiện trong bảng 14 hàng của điều phối; các khẳng định định lượng BS đo được có finding riêng bên dưới. ID Issue/PR, số hiệu ADR, SHA và số phiên bản là định danh, không tự được tính thành một số lượng mới để nhân finding.

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| Exact head/base và bản tệp được giao | `5a4dd85` / `802fc01` | full SHA và tree như đầu verdict; `LAND_EVIDENCE.yaml` bằng byte tệp trong Git | Có |
| Phạm vi diff theo prompt | 112 tệp, +12873/−0; 1 land evidence 196 dòng + 111 hiện vật | `audit.py git`: đúng 112, +12873/−0; chỉ một path ngoài `ops/reviews/` là land evidence, +196 | Có |
| Mã vận hành trong diff | 0 | Các path thêm thuộc land/review artifacts; có script đo trong artifacts, không thay mã/cổng vận hành của kho | Có, theo phạm vi runtime đã giao |
| Năng lực snapshot | 307 heads, 62 tags, 324 pull refs; không nông; abbrev 7 | Đếm trực tiếp đúng; pull refs đếm trong `kho.git` | Có; không xác nhận server hiện tại |
| Ref `origin/master` để chạy nguyên lệnh | Được mô tả là base | Không có `refs/remotes/origin/master`; `refs/heads/master` đúng `802fc01…` | Gói thiếu tên ref; xem ghi chú môi trường |
| Căn cứ mở đầu, dòng 3 | ADR-0045 đòi vết này | ADR-0045: ngoại lệ Codex executor sensitive; ADR-0034: nghĩa vụ land evidence nói chung | Sai phạm vi dẫn nguồn |
| **BS:** thứ tự land evidence, dòng 7–8 | Tệp thứ HAI, trước là `plat-x8` | Base có 1 tệp land-evidence YAML; head có đúng 2; log thêm `plat-x8` trước | Có trong lịch sử/snapshot đã kiểm |
| Schema/role, dòng 11–18 | version 1, generation 1, input `[1]`, role land_operator | YAML đọc được, role/version khớp mẫu protocol; bốn lease GATE đều generation 1 | Khớp cấu trúc; generation của *land attempt* và session identity chỉ là khai báo |
| Authorization, dòng 20–31 | head `17f4a1b`, approver `notebyme88`, hai APPROVED 22:54:28Z/23:15:00Z; neo cái sau | SHA là commit thật; hai review ID, actor, state, time, commit_id và URL không có snapshot API để kiểm | **KHÔNG ĐO ĐƯỢC về approval** |
| Hai DISMISSED / ~5 phút blocked / classifier từ chối | Có và có nguyên nhân được nêu | Không có raw timeline/response/record thực thi tương ứng | **KHÔNG ĐO ĐƯỢC** |
| “Mỗi commit đẩy sau approval đều huỷ approval”, dòng 31 | Quy luật tuyệt đối | Git objects không cho biết cấu hình dismiss stale reviews hoặc diễn biến từng lần push | **KHÔNG ĐO ĐƯỢC**; câu cần giữ mức attestation |
| Người merge và merged_at, dòng 35–49 | `notebyme88`; `2026-09-07T23:21:22Z` | Git author `notebyme88`, committer `GitHub`; Git commit time đổi UTC là `23:21:21Z` | Actor/API time **KHÔNG ĐO ĐƯỢC**; lệch 1 giây giữa hai loại timestamp không chứng minh khai sai |
| `cross_review.so_luot`, dòng 58–60 | 15 lượt | 10 verdict có tên lượt 6–15; chưa có verdict 1–4; lượt 5 có tài liệu nói không hoàn tất, không phải verdict | Không đủ chứng minh 15 verdict hoàn tất; số thứ tự lớn nhất đúng 15 |
| Model/effort trong tiêu đề 58 | codex gpt-6-astra xhigh | Hai receipt 14/15 nói không có nguồn chứng model/effort; run.json không lưu argv/model/effort | **KHÔNG ĐO ĐƯỢC** |
| P1 lượt 7 | 4 | 4 heading `[P1]` | Có |
| P1 lượt 8 | 2 | 2 | Có |
| P1 lượt 9 | 1 | 1 | Có |
| P1 lượt 10 | 1 | 1 | Có |
| P1 lượt 11 | 1 | 1; có giải thích đổi số lượt trong DOC-MANIFEST | Có |
| P1 lượt 12 | 2 | 2 | Có |
| P1 lượt 13 | 0 | 0 | Có |
| P1 lượt 14 | 0 | 0 | Có |
| P1 lượt 15 | 0 | 0 | Có |
| Phạm vi verdict trên master, dòng 71 | Lượt 6–13 có trước, 14/15 thêm cùng PR | `git cat-file -e BASE:path`: 6–13 có; 14/15 chưa có trên base, có trên head | Có |
| Manifest 14/15, dòng 73 | 59/59; 45/45, rc=0 | `sha256sum -c`: đúng cả hai | Có |
| Lượt cuối, dòng 79–84 | 15, reviewed_sha `745d888…`, approve, 0 P1/0 P2/1 P3 | Đọc verdict và đếm heading đúng toàn bộ | Có |
| **BS:** khoảng giữa head review/merge, dòng 86–87 | Giữa hai SHA là commit `17f4a1b` | `git log --format=%H 745d888..17f4a1b`: đúng 1 commit | Có |
| Diff riêng `17f4a1b`, dòng 87–88 | 2 tệp, +23/−8, toàn ops/reviews, 0 runtime | Manifest +1/−1; README +22/−7 | Có |
| `17f4a1b` “vá nốt P3”, dòng 87 | Đóng P3 còn lại của lượt 15 | Sửa ba hàng phân loại, bỏ ±5 s, thêm phương pháp; vẫn giữ câu về chạy lại để đối chiếu byte gốc mà lượt 15 yêu cầu làm rõ | Chưa đóng trọn phần đã nêu |
| Head merge chưa qua cross-review, dòng 88–89 | Không có lượt trên `17f4a1b` | Không verdict #468 được giao nào neo SHA ấy; lượt 15 neo cha | Khớp hồ sơ trong gói; không chứng minh không tồn tại review ngoài gói |
| Full-gate chạy MỘT lần, dòng 93 | Một lần theo chỉ thị | Có một bộ cặp kết quả và lời ghi README; không có launcher lịch sử để đếm mọi invocation | **KHÔNG ĐO ĐƯỢC số lần thực chạy** |
| Neo full-gate, dòng 95 | Nền `b416830`, sau `f77f198` | Hai SHA tồn tại, README ghi đúng; không có launcher để ràng buộc từng output với cây chạy lịch sử | Khớp nguồn, provenance lịch sử chưa xác thực |
| **BS:** DELTA trên bốn cặp, dòng 95 | 0 | So byte `cidk.tail`, `ploop.tail`, `lease.norm`, `doc-claims.json`: 4/4 bằng nhau | Có, đúng phạm vi đã thu hẹp |
| **BS:** sáu bộ và cặp rc, dòng 96 | cidk 0/0; ploop 0/0; lease 1/1; doctrine 0/0; adr 0/0; doc 0/0 | Hai tệp `.rc`, mỗi tệp 6 record, khớp từng cặp | Khớp log tổng hợp; không xác thực 12 exit code lịch sử |
| **BS:** không out=0B, dòng 97 | Không bộ nào | 12 trường out đã ghi đều >0: 2934, 8752, 8971, 69, 113, 70861 B mỗi vế | Khớp log; stdout gốc chỉ giữ đủ một bộ |
| **BS:** 1/6 stdout tự đếm lại được, dòng 101 | 1/6 | Chỉ doc có raw đủ 70861 B; cidk tail 206 B, ploop tail 96 B, lease norm 8827 B; doctrine/adr không có output | Có về nguyên liệu được giao |
| **BS:** suite trước merge, dòng 99–100, 140 | t33 chạy và đỏ; 120/121 | Hai log norm đều có `ĐỎ t33…` do thiếu actionlint; tổng `120/121`, chạy 121, bỏ qua 0 | Có trong log; không gọi nó là skipped |
| CI push `34169756563`, dòng 108–109 | Ubuntu success 44 bước/0 hỏng; Windows success 43/0 | Không có response API/jobs tương ứng | **KHÔNG ĐO ĐƯỢC** |
| CI PR `34168159148`, dòng 110–111, 123 | Ubuntu success 44 bước/0 hỏng; một job | Không có response API/labels/checkout log tương ứng | **KHÔNG ĐO ĐƯỢC** |
| Windows 4 skipped, dòng 113 | Điều phối đọc 4 | Không có snapshot job API | **KHÔNG ĐO ĐƯỢC** |
| **BS:** sáu điều kiện sai, dòng 114–116 | 6, kèm sáu tên | Parse YAML tại base: 40 bước khai trong workflow; 10 bước có if; đúng 6 if sai trên push/master/windows, đúng tên đã nêu | Có về tĩnh; 40 không phải số bước API |
| Rút exact-head CI, dòng 119–121 | PR run không chứng minh test đúng `17f4a1b` | Checkout trong workflow không ghim `ref` về head; source không chứa checkout log riêng | Thu hẹp kết luận đúng; không xác thực run GitHub |
| 44 tools, ít nhất HAI client, probe trả 4 tools, dòng 127–131 | Có lời tự đính chính, CLAUDE.md:583 | Dòng 580–584 có quy tắc hai client và endpoint riêng; số tool trả về lần probe không kiểm được | Khớp văn bản dẫn; API **KHÔNG ĐO ĐƯỢC** |
| `merge-base --is-ancestor`, dòng 133 | ĐÚNG | Nguyên lệnh origin/master rc=128 do thiếu ref; thay bằng exact base SHA: rc=0 | Quan hệ Git đúng |
| Merge parents, dòng 133 | `b416830` + `17f4a1b` | Hai parent OID đúng; merge method phù hợp Git object | Có |
| `rev-list --count`, dòng 135 | 0 | Nguyên lệnh origin/master rc=128; dùng exact base: stdout `0`, rc=0 | Quan hệ Git đúng |
| Lease trên master, dòng 137 | rc=0, 121/121, chạy 121, bỏ qua 0 | Đo mới đúng cả bốn giá trị; marker t33 không đỏ | Có |
| **BS:** stdout lease, dòng 137 | 8649 B | Master 8649 B; head cũng 8649 B | Có ở lần đo mới; không khôi phục stdout lịch sử |
| Thời lượng lease, dòng 137 | 71 s | Master 79.129 s; head 80.593 s trong lượt này | Thời lượng lịch sử **KHÔNG ĐO ĐƯỢC**; không gọi chênh mới là hồi quy |
| Phiên bản/cách cài actionlint, dòng 137 | 1.7.7, cài bằng ops/cai_actionlint.sh | Binary đường tuyệt đối trong cong-cu.txt trả 1.7.7; CI ghim AL_VER 1.7.7 và gọi installer | Khớp bản/cấu hình; thao tác cài lịch sử không xác thực |
| Doc-claims master, dòng 142 | rc=0, ok:true, 70861 B | Đo mới rc=0, ok:true, **70854 B**; byte bằng bản sandbox đã giao | Kết quả gate khớp; output lịch sử khác có giải thích về snapshot |
| Manifest master, dòng 145 | 13, 0 hỏng | 12 ARTIFACTS + 1 băm trần; 967/967 mục ARTIFACTS và băm trần đều khớp | Có; không đánh đồng băm trần với manifest chuẩn |
| **BS:** kiểm trực tiếp, dòng 145 | 9 gói rc=0 | Đúng 9 manifest direct rc=0, tổng 613 mục | Có |
| Ánh xạ lượt 12,13,11, dòng 146–147 | 178/178, 48/48, 128/128 | Đúng, mọi rc=0 | Có |
| Băm prompt, dòng 147–148 | Băm trần, khớp `e60c376a…` | `e60c376ab385ccc9b3cc8d2cdd87620b2110c8a68e607c879a6100c6b3f9958c` | Có; đã nằm trong phạm vi kiểm 13 tệp băm |
| **BS:** bốn gói OK=0/N vì đổi bố cục, dòng 150–152 | 4 | **3** manifest: lượt 11,12,13. Băm trần rc=1 nhưng không parse được dòng checksum, không có mẫu số N | Sai; finding P2 |
| `_kiem_bia_mo` chưa sửa, dòng 169 | Vẫn dùng any | `ops/lease_publish.py:606` còn `not any(...)`; không có diff runtime | Có về mã hiện tại; không thử nội dung tấn công mới |
| Spec r6/tip/time, dòng 171–172 | r6, `2aee80a…`, 22:53:12Z | Ref, YAML trong spec, author/committer time đúng | Có |
| **BS:** trần 6/6, dòng 173–174 | Đã dùng hết | §0 spec có 6 hàng invocation: 1,2,3,4a,4b,5; ghi 4a chết vẫn đếm và trần 6 đã hết | Khớp hồ sơ; invocation/approval tăng trần trên server không xác thực |
| r6 chưa review; chưa Packet Issue; checkpoint | Trạng thái chặn hiện tại | Nội dung spec ghi đúng ba điều này | Khớp hồ sơ snapshot; trạng thái ngoài Git **KHÔNG ĐO ĐƯỢC** |
| Mốc chụp ref cũ, dòng 177 | 23:43:30Z | Không có chứng từ snapshot mang mốc ấy được chỉ ra; gói hiện tại ghi 2026-09-08T01:20:13Z | Mốc lịch sử **KHÔNG ĐO ĐƯỢC**; không thay bằng giờ gói mới |
| Bốn giờ cấp GATE, dòng 181 | 03:37:33 / 07:50:35 / 09:44:51 / 10:17:12Z | Đúng các trường leased_at_utc ngày 2026-09-07 của bốn YAML | Có |
| Hạn #456 và quan hệ, dòng 182,192 | 14:30:07Z 07-09; cả bốn trước hạn | YAML tiền nhiệm ghi đúng hạn; so cùng ngày đúng 4/4 | Có |
| Hash/revision/generation, dòng 183–184 | 4 hash khác; r1/2/3/4; g1/1/1/1 | Đọc từng số hạng và đếm distinct đúng | Có |
| A9 đã xác định, chưa có quyết định xử lý | Lệch điều khoản, không phải câu hỏi mở | Verdict 10 có lập luận cấp r3/r4 khi còn giao; ADR-0034:5–8 có điều khoản; bốn YAML khớp | Có về bằng chứng trong gói; không kết luận quyết định ngoài gói không tồn tại |
| P1 #456 đóng bằng thời gian, dòng 191–192 | Có readback sau hạn | Tệp DOC-READBACK có đo sau 14:30:07Z; mã phân loại dùng hạn <= giờ xét | Khớp hồ sơ; không tái thực hiện lần đọc server lịch sử |
| Bốn Packet Issue #463–466 và Mission #467 open, dòng 194 | Cả năm còn open | Có bốn hồ sơ Issue trong ops/issues; trạng thái GitHub không từ đó suy ra được | **KHÔNG ĐO ĐƯỢC trạng thái open** |
| PR #477 đang cross-review, chưa merge, dòng 196 | Chưa merge | Không có raw PR API tại mốc khai | **KHÔNG ĐO ĐƯỢC**; Git ref không thay PR state |

Chi tiết manifest master (tất cả `ARTIFACTS.sha256`, trừ dòng băm trần):

| gói dưới ops/reviews | cách kiểm | kết quả thật |
|---|---|---|
| full-gate-pr468-20260907 | trực tiếp | 12/12, rc=0 |
| lượt 6 | trực tiếp | 62/62, rc=0 |
| lượt 7 | trực tiếp | 66/66, rc=0 |
| lượt 8 | trực tiếp | 69/69, rc=0 |
| lượt 9/artifact-repair | trực tiếp | 69/69, rc=0 |
| lượt 10/goi-y/cay/ops/reviews/lượt 9/artifact-repair | trực tiếp | 69/69, rc=0 |
| lượt 11 | qua manifest11-layout của lượt 12 | 128/128, rc=0 |
| lượt 11/artifact9-repair | trực tiếp | 69/69, rc=0 |
| lượt 12 | DOC-MANIFEST | 178/178, rc=0 |
| lượt 12/manifest11-layout | trực tiếp | 128/128, rc=0 |
| lượt 12/manifest11-layout/do-review10/artifact9-repair | trực tiếp | 69/69, rc=0 |
| lượt 13 | DOC-MANIFEST | 48/48, rc=0 |
| lượt 13/bundle-PROMPT.sha256 | so băm trần với bundle-PROMPT.md | khớp |

Ở head có thêm hai manifest 14/15: 59/59 và 45/45. Những tệp `*.mapped.sha256` trong artifact lượt 14/15 là danh sách đường dẫn tuyệt đối của máy cũ, không phải manifest nguồn mới; không chạy các đường máy cũ. Script tạo lại đường nằm trong gói từ manifest nguồn, giữ nguyên hash/thứ tự rồi gọi `sha256sum -c` thật. Kết quả hash không chứng minh mọi tệp ngoài manifest cũng được băm.

## KẾT QUẢ CỔNG VÀ GIỚI HẠN SNAPSHOT

| cây/lệnh | rc | bằng chứng dương và output |
|---|---:|---|
| master: `python3 -B ops/lease_publish_test.py` | 0 | `121/121 đạt; đã chạy=121, bỏ qua=0`; 8649 B stdout; 79.129 s |
| head: cùng lệnh lease | 0 | `121/121 đạt; đã chạy=121, bỏ qua=0`; 8649 B stdout; 80.593 s |
| head: `python3 -B ops/bien_nhan_v2.py` | 0 | 30 ĐẠT v2; 11/11 legacy băm khớp; 42 NỢ; 0 vi phạm; 0 KHÔNG ĐO ĐƯỢC; tổng 83; `TỔNG: ĐẠT` |
| master và head: `python3 -B scripts/tl.py doc-claims-check --strict` | 0/0 | cả hai `ok: true`; cùng 70854 B và bằng byte bản sandbox được giao |
| head: binary actionlint **đường tuyệt đối trong cong-cu.txt**, lint ci.yml và ops-publish-lease.yml | 0 | stdout/stderr rỗng; cùng binary có probe `--version` = 1.7.7 |

Hai lượt lease có stderr 56 B: `warning: You appear to have cloned an empty repository.` Đây là output có thật, không bị bỏ khỏi hiện vật; suite vẫn có marker dương đủ 121 ca. `run_checks.py` đặt TMPDIR trong gói và đưa thư mục binary đã ghim vào PATH cho t33; các lời gọi actionlint trực tiếp dùng đường tuyệt đối.

`audit.py docdiff` xác nhận hai JSON được giao lệch **duy nhất một giá trị reason**, 70861 → 70854 B: `1835b46` từ `SHA_NOT_A_COMMIT_IN_HISTORICAL_DOC` thành `SHA_NOT_REACHABLE_FROM_HEAD`. Trong gói, `git cat-file -t 1835b46` trả `commit`; `git tag --contains 1835b46` trả duy nhất `archive/dlbrut-ke-hoach-dau`; phép ancestor với cả base và head đều rc=1. **Không coi đây là hồi quy PR hoặc đổi số lịch sử 70861 thành số mới.** Hai snapshot khác nhau về khả năng tra object. Khẳng định kho nền thiếu đúng **23 tag** vẫn **KHÔNG ĐO ĐƯỢC độc lập** từ hai JSON: không có inventory tag nền để so tập. Đủ tag/ref trong gói không chứng minh mọi máy khác có cùng object; finding về khả tra SHA phải neo vào snapshot cụ thể, không chỉ neo head SHA.

Gói cũng thiếu ref `origin/master`. Đã giữ nguyên sự thiếu đó, lưu rc=128 của hai lệnh nguyên văn, rồi đo quan hệ với exact `base_sha`; cả ancestry và số commit ngoài base đều đúng. Không biến lỗi tên ref của gói thành lỗi dữ liệu trong PR. Cuối lượt, `git status --short` ở cả head và worktree master rỗng; các thay đổi scratch chỉ nằm trong gói.

## FINDING VỀ NỘI DUNG

### land-evidence-dem-bon-goi-doi-bo-cuc  [P2]  Ba manifest sai bố cục bị khai thành bốn gói có mẫu số N

TỆP/DÒNG: `ops/land/pr468-hoso-4-packet-land-evidence.yaml:150`–152; đối chiếu 145–148.

VẤN ĐỀ: có 3 manifest chuẩn không kiểm trực tiếp từ thư mục gói được: lượt 11, 12, 13. Tệp thứ tư trả lỗi là `bundle-PROMPT.sha256`, chỉ chứa băm trần; `sha256sum -c` không parse được record nào, không phải `OK=0/N` do đổi tên/làm phẳng. Câu giải thích hiện hành gộp hai nguyên nhân, dù thân ngay trước đã nhận đúng băm trần. Đây là lỗi còn lại khi sửa thân mà không đồng bộ lời tổng hợp. Không có bằng chứng hỏng hash; vì vậy P2, không P1. Đây cũng là một khẳng định định lượng bảng điều phối bỏ sót.

ĐÃ THỬ VÁ: không — đề nghị sửa câu thành “3 manifest lượt 11/12/13 lỗi do bố cục; băm trần là trường hợp thứ tư không dùng được `-c`, do định dạng”. Giữ nguyên 13 tệp băm và 0 hỏng; không sửa hash để làm lệnh sai bố cục xanh.

ĐÃ THỬ NGHIỆM: `python3 -B do-luot4/audit.py manifests` rc=0. Trên master: 9 direct rc=0; ba direct sai bố cục có `direct_ok=0`, `direct_rc=1`, sau ánh xạ đạt 128/128, 178/178, 48/48. `sha256sum -c do-luot4/master/ops/reviews/pr468-hoso-4-packet-review-13-codex/bundle-PROMPT.sha256` rc=1, stdout rỗng, stderr `no properly formatted checksum lines found` (lưu `do-luot4/bare-check.json`). Phép đo này khóa cả số lượng lẫn hai nguyên nhân; tránh sửa thành “chỉ ba phép kiểm trực tiếp lỗi”, vì tổng số không dùng được `-c` vẫn là bốn.

ĐỘ TIN: cao.

### land-evidence-so-luot-khong-co-don-vi  [P2]  Số thứ tự cuối 15 được dùng làm tổng review mà không khai lượt chưa hoàn tất

TỆP/DÒNG: `ops/land/pr468-hoso-4-packet-land-evidence.yaml:58`–60; `ops/reviews/GHI-NHAN-CROSS-REVIEW-LUOT5-KHONG-HOAN-TAT.md:1`–6.

VẤN ĐỀ: `so_luot: 15` và tiêu đề “CROSS-REVIEW: 15 lượt” không định nghĩa đếm số thứ tự, invocation hay verdict hoàn tất. Trong gói có 10 verdict hoàn tất mang tên 6–15; chưa tìm được verdict 1–4, và tài liệu lượt 5 nói rõ “KHÔNG phải verdict”, không hoàn tất. Vì vậy không thể xác nhận tổng 15 bằng cách đếm verdict như bảng điều phối yêu cầu. `luot_cuoi.so: 15` đúng nhưng không chứng minh số hạng “15 lượt hoàn tất”. Không khẳng định tổng lịch sử thật chỉ có 10, cũng không dùng thiếu tệp để phủ nhận từng review ngoài gói.

ĐÃ THỬ VÁ: không — giữ số thứ tự cuối 15 ở trường có sẵn; định nghĩa đơn vị `so_luot` hoặc đánh dấu nó chưa đủ nguồn. Khai 10 verdict hiện có, lượt 1–4 thiếu nguồn và lượt 5 không hoàn tất. Nếu 15 là bộ đếm attempt, cần inventory attempt và quy tắc đếm. Rủi ro của vá là thay mù 15 bằng 10, làm một lời khai quá mức khác.

ĐÃ THỬ NGHIỆM: `python3 -B do-luot4/audit.py reviews git sources` rc=0: 10 verdict #468; số thứ tự lớn nhất 15; source lượt 5 phủ nhận có verdict hoàn tất. Quét object paths toàn bộ refs ở `cay-kho` và `kho.git` chưa tìm ra verdict 1–5 theo tên PR/lượt. Kết quả toàn bộ invocation trên GitHub/phiên trước: **KHÔNG ĐO ĐƯỢC**, không có log nguồn đầy đủ.

ĐỘ TIN: cao về số hiện vật và sự thiếu định nghĩa; vừa về phạm vi lịch sử không được giao.

### land-evidence-dan-adr-sai-pham-vi  [P2]  Câu mở lấy nghĩa vụ của ngoại lệ đảo vai làm căn cứ cho hồ sơ Claude executor

TỆP/DÒNG: `ops/land/pr468-hoso-4-packet-land-evidence.yaml:3`–5; `docs/adr/0045-ngoai-le-dao-vai-executor-reviewer.md:5`–8.

VẤN ĐỀ: ADR-0045 đặt yêu cầu vết máy đọc được cho **ngoại lệ Codex executor trên packet sensitive**, cụ thể lease khai review class/ngoại lệ. Hồ sơ này khai executor Claude, reviewer Codex; không khai lần sử dụng ngoại lệ ấy. Câu “mỗi lần dùng” bị trích khỏi đối tượng và nối thành lý do bắt buộc của tệp. Nghĩa vụ ghi approver/authorization/operator/merge/post-check/bookkeeping có nguồn trực tiếp ở ADR-0034:17–20 và mẫu land evidence ở Protocol:466–488. Có căn cứ đúng để ghi hồ sơ; lỗi là dẫn căn cứ sai phạm vi.

ĐÃ THỬ VÁ: không — thay viện dẫn mở đầu bằng ADR-0034 và mẫu land evidence trong Protocol; không sửa ADR và không bỏ nghĩa vụ lưu evidence. Kiểm lại câu mở phải mô tả đúng đối tượng áp dụng, không chỉ đổi số hiệu trong cùng câu trích sai.

ĐÃ THỬ NGHIỆM: `python3 -B do-luot4/audit.py sources` rc=0, lưu nguyên đoạn ADR-0045, ADR-0034, Protocol và dòng provider/executor của land evidence trong `sources.json`. Đọc trực tiếp `sed -n '5,8p' cay-kho/docs/adr/0045-ngoai-le-dao-vai-executor-reviewer.md` và `sed -n '17,20p' cay-kho/docs/adr/0034-governance-change-control-review-land-authority.md` cho hai phạm vi khác nhau nêu trên.

ĐỘ TIN: cao.

### land-evidence-khai-dong-p3-khi-con-sot  [P3]  Lời “vá nốt P3” chưa bao gồm một câu mà verdict 15 yêu cầu làm rõ

TỆP/DÒNG: `ops/land/pr468-hoso-4-packet-land-evidence.yaml:87`; `ops/reviews/full-gate-pr468-20260907/README.md:57`; verdict 15:80 và phần gợi ý sau finding.

VẤN ĐỀ: bản vá `17f4a1b` sửa thật ba hàng phân loại nguồn, bỏ sai số ±5 s và thêm cách lập inventory. Nhưng README vẫn viết “muốn đối chiếu byte gốc phải chạy lại”. Verdict 15 đã chỉ đúng câu này và yêu cầu nói rõ chạy lại sinh log mới, không khôi phục byte lịch sử đã mất. Land evidence gọi commit là “vá nốt P3” mà không giữ phần dư này. Giữ mức P3 của vấn đề gốc: giới hạn 1/6 và thiếu raw vẫn được công khai, chưa thấy authority/gate bị nới.

ĐÃ THỬ VÁ: không — ghi trạng thái P3 “đã vá phần bảng/phương pháp; còn câu raw cần làm rõ”, hoặc sửa câu ở nguồn và kiểm lại rồi mới khai đóng. Không tái chạy suite để thay thế log lịch sử. Rủi ro là sửa review verdict cũ theo kết luận mới; nên giữ nguyên verdict lịch sử.

ĐÃ THỬ NGHIỆM: `python3 -B do-luot4/audit.py fullgate sources` rc=0; diff `17f4a1b` không sửa câu còn sót, source README hiện hành vẫn có nó, source verdict 15:80 đã nêu nó. Không còn launcher `fullgate.sh` trong `git ls-files`; inventory vẫn chỉ giữ lease norm và hai tail.

ĐỘ TIN: cao.

### land-evidence-gioi-han-chua-phu-het-loi-khai  [P3]  Giới hạn đã thêm chưa phủ phần authorization, tiêu đề và bookkeeping

TỆP/DÒNG: `ops/land/pr468-hoso-4-packet-land-evidence.yaml:24`–31, 37–44, 58, 93, 137, 177, 194–196.

VẤN ĐỀ: giới hạn `merged_by`/CI đã sửa thực chất nhưng một số phần khác vẫn đứng như lời xác nhận: hai APPROVED và danh tính khác nhau ở mục authorization; quy luật huỷ approval ở dòng 31; model/effort trong tiêu đề; số lần full-gate, thời lượng lịch sử 71 s; giờ snapshot cũ; trạng thái open của Issue/Mission và PR #477 chưa merge. Đặc biệt hai receipt vừa được sửa để nói model/effort/thread không có nguồn, nhưng tiêu đề dòng 58 còn `gpt-6-astra xhigh` không gắn nhãn. Hash và các cổng offline xanh không đối chứng được các mệnh đề này. Finding cũ vẫn đúng trên head; không tự dựng lại nội dung verdict lượt 3.

ĐÃ THỬ VÁ: không — thêm giới hạn nguồn ở cấp toàn tệp hoặc từng trường, chỉ rõ nhóm attestation, snapshot thời điểm nào, nguồn thô nào thiếu. Đối với model/effort, dẫn đúng giới hạn của hai receipt. Giữ những số reviewer thật sự tái tính được, tránh hạ cả bảng thành “không đo được”.

ĐÃ THỬ NGHIỆM: `python3 -B do-luot4/audit.py sources docdiff` rc=0: `run.json.lenh` của cả hai lượt chỉ ba khoá, receipt hiện hành thừa nhận không có model/effort/thread; title vẫn chứa model/effort. Snapshot hiện giao mang giờ `2026-09-08T01:20:13Z`, không chứng minh mốc lịch sử 23:43:30Z. Các API fact liệt kê trên: **KHÔNG ĐO ĐƯỢC**, không có mạng và không có raw response tương ứng trong gói. Lần đo lease mới 79.129/80.593 s không xác thực hay bác 71 s lịch sử.

ĐỘ TIN: cao về khoảng thiếu nguồn và phạm vi câu chữ; không kết luận các sự kiện API ấy sai.

## FINDING VỀ KHẲNG ĐỊNH ĐÚNG MÀ BẢNG ĐIỀU PHỐI BỎ SÓT

Các P3 sau ghi nhận độ phủ của **bảng giao review**, không phải phát hiện PR khai sai. Theo yêu cầu “mỗi khẳng định bị bỏ sót vẫn tính finding”, từng mục có slug riêng. Không nhân theo từng phần tử của cùng map/cặp số, tương tự một hàng `p1_theo_luot` trong bảng gốc.

### bang-do-bo-sot-land-evidence-thu-hai  [P3]  Bảng bỏ sót khẳng định đây là tệp land evidence thứ hai

TỆP/DÒNG: `ops/land/pr468-hoso-4-packet-land-evidence.yaml:7`–8.

VẤN ĐỀ: chữ “HAI” là số lượng ngoài bảng 14 hàng. Đo lại khớp: base chỉ có `plat-x8-land-evidence.yaml`, head thêm tệp đang review. Không tính hồ sơ “SAN_SANG_LAND” cũ là cùng loại land-evidence YAML.

ĐÃ THỬ VÁ: có — bổ sung hàng BS trong BẢNG ĐO của verdict này; không cần đổi giá trị trong PR. Giữ tiêu chí loại tệp khi đếm, tránh biến “hai tệp YAML loại này” thành “kho chỉ từng có hai tài liệu về land”.

ĐÃ THỬ NGHIỆM: `python3 -B do-luot4/audit.py git` rc=0; `land_files` có đúng 2 path. `git -C cay-kho ls-tree -r --name-only 802fc01 ops/land` trả 1 path; `git -C cay-kho log --all --format='%h %s' -- ops/land/` có commit tạo `plat-x8` trước commit tạo tệp hiện tại.

ĐỘ TIN: cao trong loại hiện vật được nêu.

### bang-do-bo-sot-mot-commit-chen  [P3]  Kiểm numstat chưa kiểm số commit giữa hai mốc

TỆP/DÒNG: `ops/land/pr468-hoso-4-packet-land-evidence.yaml:86`–87.

VẤN ĐỀ: bảng gốc đòi numstat của `17f4a1b`, chưa đòi kiểm khẳng định giữa hai mốc chỉ là commit ấy. Hai phép đo trả lời hai câu khác nhau. Đo thêm khớp, không tìm thấy commit trung gian khác.

ĐÃ THỬ VÁ: có — thêm hàng khoảng commit vào BẢNG ĐO; không sửa PR. Kiểm cả membership của khoảng và số phần tử, không chỉ đọc commit tip.

ĐÃ THỬ NGHIỆM: `git -C cay-kho log --format=%H 745d888..17f4a1b` rc=0, đúng một dòng `17f4a1b85b8d5146c5e6dddbdc40f11111a659f7`; được lưu trong `audit.py git`.

ĐỘ TIN: cao.

### bang-do-bo-sot-bon-cap-delta  [P3]  Bảng bỏ sót số cặp hiện vật và DELTA trước merge

TỆP/DÒNG: `ops/land/pr468-hoso-4-packet-land-evidence.yaml:95`.

VẤN ĐỀ: lời khai DELTA=0 trên bốn cặp nằm ngoài bảng gốc. Cả bốn cặp đều bằng byte. Tính đúng này chỉ phủ tail/norm/JSON được lưu, không suy thành sáu stdout gốc bằng nhau.

ĐÃ THỬ VÁ: có — thêm hàng BS và kết quả so từng cặp; không sửa PR. Giữ tên/bố cục nguyên liệu để lần sau không mở rộng phạm vi DELTA.

ĐÃ THỬ NGHIỆM: `python3 -B do-luot4/audit.py fullgate` rc=0; bốn `pairs.*.equal=true`. Kích thước mỗi vế: cidk.tail 206 B, ploop.tail 96 B, lease.norm 8827 B, doc JSON 70861 B.

ĐỘ TIN: cao.

### bang-do-bo-sot-sau-bo-full-gate  [P3]  Bảng bỏ sót sáu cặp mã thoát được khai trong full-gate

TỆP/DÒNG: `ops/land/pr468-hoso-4-packet-land-evidence.yaml:95`–96.

VẤN ĐỀ: số bộ và map cặp rc không có trong bảng gốc. Đọc hai log tổng hợp khớp cả sáu số hạng; thiếu launcher không cho phép xác thực exit code lịch sử độc lập.

ĐÃ THỬ VÁ: có — thêm map và loại nguồn vào BẢNG ĐO; không sửa PR. Không dùng `rc=0` của script đọc log làm bằng chứng sáu suite đã xanh.

ĐÃ THỬ NGHIỆM: `python3 -B do-luot4/audit.py fullgate` rc=0; `nen.rc`/`sau.rc` mỗi tệp 6 record, lần lượt cidk 0, ploop 0, lease 1, doctrine-scan 0, adr-song 0, doc-claims-check 0 ở cả hai vế. Mã thoát thực của lần chạy lịch sử: **KHÔNG ĐO ĐƯỢC độc lập**, vì không có launcher/raw provenance.

ĐỘ TIN: cao về nội dung log; không xác nhận provenance lịch sử.

### bang-do-bo-sot-out-khong-rong  [P3]  Bảng bỏ sót lượng stdout bằng không trong lời khai full-gate

TỆP/DÒNG: `ops/land/pr468-hoso-4-packet-land-evidence.yaml:97`.

VẤN ĐỀ: “Không bộ nào out=0B” là một khẳng định định lượng riêng. Cả 12 trường out trong hai log đều dương; chưa có raw stdout để xác minh độc lập 5/6 bộ.

ĐÃ THỬ VÁ: có — thêm hàng BS, ghi rõ đây là đọc trường đã tổng hợp. Không đánh đồng file tail không rỗng với toàn stdout của lần chạy gốc.

ĐÃ THỬ NGHIỆM: `python3 -B do-luot4/audit.py fullgate` rc=0, hai log cùng bộ kích thước `[2934,8752,8971,69,113,70861]` B; 0/12 trường bằng 0. Kích thước gốc của năm bộ không đủ hiện vật: **KHÔNG ĐO ĐƯỢC độc lập**.

ĐỘ TIN: cao về các trường log.

### bang-do-bo-sot-mot-phan-sau-stdout  [P3]  Bảng bỏ sót mẫu số sáu và độ phủ một stdout nguyên vẹn

TỆP/DÒNG: `ops/land/pr468-hoso-4-packet-land-evidence.yaml:101`.

VẤN ĐỀ: khẳng định 1/6 đo lại khớp nguyên liệu. Nó không có trong bảng gốc, dù giới hạn này quyết định nên đọc các con số full-gate mạnh tới đâu.

ĐÃ THỬ VÁ: có — bổ sung hàng BS với loại từng output. Giữ cả tử số lẫn mẫu số; không suy ratio từ câu README mà không kiểm inventory.

ĐÃ THỬ NGHIỆM: `python3 -B do-luot4/audit.py fullgate` rc=0: đủ raw doc JSON 70861 B; hai tail 206/96 B; lease norm 8827 B khác kích thước stdout gốc khai 8971 B; không có output doctrine-scan/adr-song. Sáu bộ phân rã thành 1 raw + 2 tail + 1 norm + 2 không output.

ĐỘ TIN: cao về khả năng tự đếm từ nguyên liệu; không xác nhận launcher gốc.

### bang-do-bo-sot-lease-truoc-merge  [P3]  Bảng chỉ yêu cầu 121/121 sau merge và bỏ 120/121 trước merge

TỆP/DÒNG: `ops/land/pr468-hoso-4-packet-land-evidence.yaml:99`–100, 140.

VẤN ĐỀ: số 120/121 là lời khai riêng và dễ bị nhầm với skipped. Hai log trước merge đều ghi đã chạy 121, bỏ qua 0, t33 đỏ do thiếu actionlint; khớp câu đã đính chính.

ĐÃ THỬ VÁ: có — thêm hàng BS; giữ tách passed/failed/skipped và phạm vi lint bên trong t33. Không sửa số lịch sử thành kết quả xanh hiện tại.

ĐÃ THỬ NGHIỆM: `python3 -B do-luot4/audit.py fullgate` rc=0; `lease_tail` có `ĐỎ t33_workflow_dang_lease_phai_qua_actionlint` và `lease_publish: 120/121 đạt; đã chạy=121, bỏ qua=0`; hai log norm bằng byte. Đọc hàm t33 cho thấy assert thiếu tool xảy ra trước subprocess lint.

ĐỘ TIN: cao về log/cấu trúc hàm.

### bang-do-bo-sot-byte-lease  [P3]  Bảng bỏ sót 8649 byte stdout của bộ lease

TỆP/DÒNG: `ops/land/pr468-hoso-4-packet-land-evidence.yaml:137`.

VẤN ĐỀ: hàng 8 bảng gốc nêu rc và số ca, bỏ kích thước stdout. Đo mới trên master và head đều khớp 8649 B. Cùng dòng còn 71 s lịch sử: đã đưa vào bảng dưới mức KHÔNG ĐO ĐƯỢC, không lấy thời gian chạy mới để bác nó.

ĐÃ THỬ VÁ: có — bổ sung byte stdout và nguồn đo; không sửa PR. Phân biệt stderr riêng 56 B, không cộng nó vào stdout để tạo mismatch giả.

ĐÃ THỬ NGHIỆM: `python3 -B do-luot4/run_checks.py` rc=0; mục `lease-master` trong `checks.json` ghi stdout_bytes=8649, rc=0. Lượt head cùng lệnh thực trong `lease-head.json` cũng 8649 B, rc=0. `wc -c do-luot4/lease-master.stdout do-luot4/lease-head.stdout` cho 8649 và 8649.

ĐỘ TIN: cao cho phép đo mới; không tự nhận đã phục hồi log lịch sử.

### bang-do-bo-sot-chin-manifest-truc-tiep  [P3]  Bảng bỏ số hạng chín dù yêu cầu kiểm tổng mười ba

TỆP/DÒNG: `ops/land/pr468-hoso-4-packet-land-evidence.yaml:145`.

VẤN ĐỀ: tổng 13 đúng không tự chứng minh số 9 direct đúng. Kiểm từng manifest cho đúng 9 direct, ba phải giải bố cục và một băm trần. Bảng gốc chỉ liệt kê tổng cùng ba số ánh xạ.

ĐÃ THỬ VÁ: có — bổ sung hàng BS và bảng phân rã đầy đủ phía trên. Không đếm thêm các tệp diagnostic `.mapped.sha256` của máy cũ như manifest nguồn.

ĐÃ THỬ NGHIỆM: `python3 -B do-luot4/audit.py manifests` rc=0; lọc `tree=master, mode=direct` có 9 record, đều rc=0, tổng 613 mục. Ba manifest ánh xạ có 354 mục; 613+354=967 mục ARTIFACTS. Băm trần được so riêng.

ĐỘ TIN: cao.

### bang-do-bo-sot-sau-buoc-if-sai  [P3]  Bảng bỏ phép đếm tĩnh sáu bước dù prompt có nêu hướng nghi ngờ

TỆP/DÒNG: `ops/land/pr468-hoso-4-packet-land-evidence.yaml:114`–116.

VẤN ĐỀ: số 6 không nằm trong bảng 14 hàng; có trong hướng nghi ngờ và vẫn cần đo. Kết quả tĩnh đúng cả số lượng lẫn tập tên. Không giải được vế API 4 skipped bằng phép đếm này.

ĐÃ THỬ VÁ: có — thêm hàng BS và lưu truth table. Không thay 4 bằng 6 trong trường API, không suy success/failure của job từ số bước khai trong YAML.

ĐÃ THỬ NGHIỆM: `python3 -B do-luot4/audit.py ci` rc=0, 40 step khai tĩnh, 10 có if, 6 false trên push/master/windows: PR EOL-base, don-nhanh, cgroup Linux, tl selftest PR, ci-phamvi selftest, release-verify WORKER. `ci-static.json` giữ nguyên biểu thức từng bước. Vế API: **KHÔNG ĐO ĐƯỢC**, thiếu response job tương ứng.

ĐỘ TIN: cao về phân tích tĩnh; không đo được vế API.

### bang-do-bo-sot-sau-loi-goi-review-spec  [P3]  Bảng bỏ trần 6/6 trong bản đính chính spec

TỆP/DÒNG: `ops/land/pr468-hoso-4-packet-land-evidence.yaml:173`–174.

VẤN ĐỀ: hàng 11 của bảng gốc chỉ nêu revision/tip/timestamp, bỏ bộ đếm 6/6. Spec r6 tại đúng tip có sáu hàng invocation 1,2,3,4a,4b,5, không phải sáu số thứ tự review hoàn tất. 4a được khai chết nhưng vẫn tính budget; §0 ghi trần 6 đã hết. Đây là đối chiếu số hạng trong hồ sơ, không xác thực runtime/approval tăng trần của các phiên ấy.

ĐÃ THỬ VÁ: có — bổ sung hàng BS với đơn vị invocation và giới hạn nguồn; không đổi số trong PR. Giữ phân biệt invocation/void/verdict khi áp cách sửa cho bộ đếm 15 của #468.

ĐÃ THỬ NGHIỆM: `python3 -B do-luot4/audit.py bookkeeping` rc=0, `review_rows` có đúng 6 hàng tại tip `2aee80a…`; text §0 phân rã `3 lượt + 4a chết + 4b + 5`. Số invocation thực và thẩm quyền nâng budget: **KHÔNG ĐO ĐƯỢC độc lập**, không có log/response gốc tương ứng.

ĐỘ TIN: cao về nội dung/count hàng spec; vừa về kết luận lịch sử vốn chỉ là nguồn tự khai.

## KIỂM CUỐI VÀ PHẦN KHÔNG KẾT LUẬN

Đã kiểm những con số viết bằng chữ ở các câu hiện hành, không chỉ chữ số; đối chiếu từng phần tử map P1 và từng lease, không chỉ tổng/quan hệ. Những lời cũ được trích rồi đánh dấu SAI không bị tính như khẳng định hiện hành. Inventory được lập thủ công khi đọc đủ 196 dòng, rồi đối chiếu các nguồn Git/file và các mode script đã lưu; vẫn có thể bỏ sót cách diễn đạt hàm ý hoặc nguồn ngoài gói. Bảng này không phải trần: mục bỏ sót tiếp tục tính finding, không tự miễn trừ.

Không xác nhận GitHub CI, review timeline, merged_by, Issue/PR state, branch protection hay việc giữ object trên server. Không coi absence của ref/snapshot là bằng chứng sự kiện không xảy ra. Không dùng kết quả này làm merge authorization hoặc nghiệm thu các packet #463–466/Mission #467. Các cổng xanh ở đây xác nhận đúng phần chúng đã chạy; chưa có bằng chứng rằng chúng validate mọi lời khai trong land evidence.
