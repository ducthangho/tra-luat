verdict: changes_requested
reviewed_sha: 86f87b2004f6054572cc787ae660518763b29b95
reviewed_base: 46d9561c8cc4b0cf530fc7ca4015de8f07c6aeec
reviewed_files_sha256:
  CHANGELOG.md: f7c076d358ab84be6f13ada642262ae4d98e69738213cf3691e39dbbfb04db06
  RELEASE_MANIFEST.json: 22353f3f1d58431c496377b03ffe12ae5c6b9a77948c7c712ef4b1dbbbf6743f
  ops/reviews/README.md: 5e64d00d7b9a14519f530ed757b939bf96e15ec92cd62f8cd862a4db19c5d35b
  ops/reviews/pr516-review-1-codex-verdict.md: 1a1235739ebf920811570f3a05b3799f8743aa8e7618b7f9099e001d4e8dc1f0
  ops/reviews/pr516-review-1-codex-verdict.receipt.yaml: d3dbc8d8e64f59c0763819dd8310371b144a9d90b12b7b996875ae947ba18e9b
  ops/reviews/pr516-review-2-codex-verdict.md: e2d0fc65a809cb7e2be27804f518d41a09a8329b672ae8ebfa438603cb0202fe
  ops/reviews/pr516-review-2-codex-verdict.receipt.yaml: 00d97faba0dc8b423f292709f6629e8a177d016271bf3f7cba0a91233d6b029b
  ops/reviews/pr516-review-3-codex-verdict.md: 532e022c16f75ba5780de45e4e4056788f58ac275d6638a1fbb5c55088cda968
  ops/reviews/pr516-review-3-codex-verdict.receipt.yaml: ec121e2541e0a7c5a35fd502b316ec58cbf2be1d1b235809108b1949950d7e82
  ops/reviews/pr516-review-4-codex-verdict.md: 4d227acbc81641f2a25d68870ecf3dbb047a9df390b4382afd853e9452496ca4
  ops/reviews/pr516-review-4-codex-verdict.receipt.yaml: 0722c7ed458ea9e0dd673d037d6b297878d094e05ed74e18389b929daad6af42
  ops/reviews/pr516-review-5-codex-verdict.md: d66f58020aa0330c44597fe87635c9f70eb60d49e5db444cd09da7b24a82a38b
  ops/reviews/pr516-review-5-codex-verdict.receipt.yaml: 44e41a5878a52875e4c01781ed4b0a01fdde8bf53acb216bb538d80adb5f992c
model_tu_khai: GPT-6 / Codex (tự khai theo ngữ cảnh phiên; không attestation độc lập backend)
review_round: 1
so_p1: 0
so_p2: 3
so_p3: 1
so_the_hien: 21
hint_sha256: 292c42b6fcf58b497539bab6b68536325cd31e05f9c80bb83b399ccd89e66245

**changes_requested — 0 lớp P1 / 3 lớp P2 / 1 lớp P3; 21 thể hiện trong diff.** Các scalar runtime, băm/byte verdict, số finding, assurance và neo ở HEAD khớp. Ba lớp P2 sửa được trong PR: nhãn/mức bằng chứng, template sai lượt, và tóm tắt đổi tập đối tượng. Lớp template gán lỗi đọc của lượt 2 sang lượt 3 là cơ chế mới rõ nhất; các lớp còn lại tiếp tục hình dạng lời khai vượt phép đo.

Không xếp P1 cho lỗ cổng đã có sẵn và đã công khai: các mutant so_p2/byte/assurance sống thật, nhưng giá trị của năm receipt hiện tại không khai sai ở chốt đó. Severity P1 của caveat lượt 5 không phải finding P1 mới.

Đơn vị đếm: mỗi hàng trong bảng thể hiện dưới đây là một vị trí lời khai hoặc bản chiếu của nó; khối cùng chịu một nhãn nguồn được tính một thể hiện. Số finding là số **lớp**, không phải số hàng. EVIDENCE/meta ngoài diff và lỗi cũ của pr511 không cộng vào 21.

## Bảng đo lại

R1…R5 = năm receipt `ops/reviews/pr516-review-N-codex-verdict.receipt.yaml`; V1…V5 = verdict `.md` cạnh receipt, byte bằng `nguon/VERDICT.rvhs516-N.md`. Số sau dấu `:` là dòng **HEAD gốc**, không phải dòng sau HINT. `KHỚP nguồn` chỉ là khớp nội dung báo cáo; không chứng thực sự kiện GitHub hoặc biến phép chạy cũ thành phép chạy mới. Không coi một hàng hỗn hợp trong bảng này là một scalar đo được. Các trường không thể xác thực từ gói ghi rõ KHÔNG ĐO ĐƯỢC.

### Phạm vi, số tổng hợp, cấu trúc, assurance và nguồn

| khai | đo | khớp? |
|---|---|---|
| HEAD / origin/master / 3 commit | 86f87b2 / 46d9561; rev-list base..HEAD = 3; chuỗi 8fd3f48→896bfbf→86f87b2 | KHỚP |
| 13 tệp, +1732/−5, không đổi sản phẩm | 13 files changed, 1732 insertions(+), 5 deletions(-); tập tệp là 5 verdict + 5 receipt + README + CHANGELOG + manifest; không tệp sản phẩm trong diff | KHỚP |
| 13 reviewed_files_sha256 là byte của HEAD | Từng băm lấy từ worktree và so git show HEAD:path; True | KHỚP |
| CHANGELOG:3–4; README:15 — 5 verdict, 5 receipt, 13 cảnh báo, 5 mục lục, 1 đoạn nguồn | 5/5; caveat phân bố 2/3/3/2/3=13; 13 cặp độc nhất, thêm đúng 1 hàng đoạn nguồn + 1 trống + 13 cảnh báo + 5 mục lục = 20 LF | KHỚP |
| README 736→756; cảnh báo 29–41; mục lục 404–408 (EVIDENCE) | LF 736→756 khớp. Cảnh báo mới 29–41; mục lục mới 419–423. 404–408 là lời khai ngoài diff bị lệch vị trí sau chèn. | KHỚP LF; KHÔNG KHỚP vị trí trong EVIDENCE |
| README:15 — năm lượt trên BỐN head | run/V1…V5 = 899f305, a41fc69, 5f45e6e, c98c33e, c98c33e: 4 SHA duy nhất | KHỚP |
| README:15 và evidence_url_ghi_chu — Bảng đo 255/142/44/61/24 dòng | Các mục ## cho khoảng V1 25–279 (255), V2 59–200 (142), V3 27–70 (44), V4 35–95 (61), V5 38–61 (24). Đếm cả heading và dòng trống, không gọi đây là số hàng dữ liệu. | KHỚP |
| R1…R4:evidence_url_ghi_chu — phần còn lại 1–24+280–353; 1–58+201–237; 1–26+71–106; 1–34+96–163 | Các khoảng là phần bù đúng của Bảng đo tới dòng cuối. R5 toàn bộ 83 dòng đúng. Comment thật có bỏ/giữ đúng các khoảng không: KHÔNG ĐO ĐƯỢC. | KHỚP khoảng local; KHÔNG ĐO ĐƯỢC comment |
| R2 cross_approved; R3 cross_approved | V2 có ## ĐỐI CHIẾU tại 25, năm slug cũ đều ĐÃ VÁ THẬT ở 31–35, approve 0/0/0, rc=0+XONG. V3 mục tại 19: lượt sandbox 2 không có finding; P1 assurance connector ĐÃ VÁ THẬT, re-anchor KHÔNG ÁP DỤNG với bằng chứng; approve 0/0/0, rc=0+XONG. Tương xứng phạm vi/head, không hồi tố khẳng định không thể có finding về sau. | KHỚP |
| R1/R4/R5 cross_reviewed | R1/R4 verdict changes_requested; V4 mục ĐỐI CHIẾU: lượt 3 không có finding nên không ép tạo một trạng thái cho tập rỗng. R5 approve và P2-E01 ĐÃ VÁ THẬT ở V5:29, nhưng run rc=1/stdout 0; giữ mức thấp hơn approval là thận trọng và không vượt đo. | KHỚP |
| R5 trang_thai=xong cùng ma_thoat=1 | Hai khóa run.json đúng vậy. xong là trạng thái wrapper đã kết thúc, không đồng nghĩa thành công; receipt không khai chạy sạch. | KHỚP |
| R5 caveat muc=P1 trong receipt nhưng so_p1=0 | P1 là mức cảnh báo cách dùng verdict, không phải finding mới của V5. Heading finding V5 bằng 0; không cộng severity caveat vào số finding. | KHỚP |
| R2 codex_connector_cung_head ↔ caveat ↔ CHANGELOG:39–42 | Cùng head a41fc69, bỏ draft 19:39:43Z, completed 19:52:04Z, 2 P1, assurance vá 5f45e6e; không có câu R2 phủ nhận connector cùng head. Các sự kiện/threads/resolve là (b), KHÔNG ĐO ĐƯỢC từ local. | KHỚP nội bộ; KHÔNG ĐO ĐƯỢC GitHub |
| R5 github_submitter_identity.ghi_chu ↔ APPROVE-HO-SO caveat | Cùng phân biệt verdict được vận chuyển không tự là authorization; uỷ quyền được tác giả quy cho luật chung chủ kho, không cho reviewer approve. Không tự mâu thuẫn. Comment 5640499918 và sổ gen4 uy_quyen_merge.jsonl không có nguồn độc lập trong gói. | KHỚP nội bộ; KHÔNG ĐO ĐƯỢC sự kiện/uỷ quyền |
| R1…R5 receipt_khong_khai | Không khai backend đã chạy; R1–3 không khai là head cuối; R4 phân biệt lỗi gói review; R5 không khai run sạch; không lượt nào nhận chạy lại mọi phép đo trước. Các phủ định phù hợp phạm vi verdict; câu template ở R1 về lượt trước không tạo một lời khai đã chạy trước. | KHỚP |
| R1 mirror | Nguồn #511 có trong prompt:11–13 và inventory stderr:58–87; không có lượt #516 trước lượt 1. Phần template đó sai; phần #511/runs/actionlint được bản ghi inventory hỗ trợ. | KHÔNG KHỚP — lớp template |
| R2 mirror | prompt:10–13 liệt kê lượt 1 #516, hai VERDICT/HINT #511, run 417a209c/8873d98d, actionlint 1.7.7. Không gán gói hiện tại #517 làm gói #516 lượt 2. | KHỚP nguồn mô tả; version binary lịch sử không tái chạy |
| R3 mirror | prompt:14–16 không liệt kê hết, nhưng inventory rg --files stderr:50 trở đi có hai lượt #516 trước, cả VERDICT/HINT #511, 8 tệp run #511 và actionlint. Không được suy vắng mặt chỉ từ prompt rút gọn. | KHỚP inventory được ghi; version binary KHÔNG ĐO ĐƯỢC |
| R4 mirror | prompt:15–17 có ba lượt trước và verdict #511; inventory stderr:47 trở đi xác nhận HINT #511 và actionlint. Lệnh inventory cố ý loại nguon/runs/** nên không đo được sự hiện diện hai run #511 trong chính gói lượt 4. | KHỚP phần thấy; KHÔNG ĐO ĐƯỢC phần bị loại; không kết tội vắng mặt |
| R5 mirror | prompt:14–15 chỉ liệt kê bốn lượt #516; inventory stderr:44 trở đi thực có cả hai VERDICT/HINT #511, hai run #511, actionlint. Không coi phần bị prompt lược bỏ là tệp không tồn tại. | KHỚP inventory được ghi; version binary KHÔNG ĐO ĐƯỢC |
| R1…R5 mirror: core.abbrev 7 / đủ ref / không nông / clone từ guong.git | Cây được giao cho lượt #517: core.abbrev=7, is-shallow=false, 347 ref kể origin/HEAD. Không lấy cây #517 chứng thực config hoặc độ đầy đủ remote live của năm gói cũ. | KHỚP cây hiện tại; lịch sử chỉ đối chiếu prompt/log |
| R1…R5 anchor.mo_ta và reviewed_sha tổ tiên master | Đã đọc đủ mỗi mắt cha trong bảng chính; cả bốn SHA review là tổ tiên 46d9561, neo8fd3f48 là tổ tiên HEAD, không là tổ tiên base. Không lẫn reviewed_sha với commit chứa verdict mới. | KHỚP |
| 5 evidence_url / git log --all --diff-filter=A | Cả năm đúng một commit thêm tệp: 8fd3f484d512f34ab459d1aef09ae2977f07ba65; băm blob URL bằng receipt và worktree; canonical_ancestry cao là đúng ở HEAD được cấp. | KHỚP |
| anchor.gioi_han 5 receipt: lượt 2 và 4 đo hai receipt pr511 mất khi squash | Tái dựng a41fc69 lên6786637: merge/ff83/0, squash81/2; c98c33e lên8802924: merge/ff100/0, squash98/2. Hai vi phạm chỉ pr511, đúng câu lịch sử. Xem bảng land hiện tại: 5 receipt pr516, không cộng thêm pr511/pr493. | KHỚP |
| Land HEAD #517 lên46d9561: merge/ff vững, squash mất | Merge/ff105/0/158; squash100/5/158, năm receipt pr516 mất neo8fd3f48. Neo120d47a/pr511 và98f931b/pr493 đã là tổ tiên base nên không mất. Không gán số2 lịch sử thành số hiện tại. | KHỚP |
| 105 ĐẠT (100+5), legacy11/11, nợ42, tổng158, vi phạm0, chưa đo0 | HEAD v2 rc0:105+11+42=158; bản sao base46d9561 rc0:100+11+42=153. Tái chạy t26/t27 rc0/0. | KHỚP |
| release-verify --strict --json:180/180, hash khớp | {'ok': True, 'strict': True, 'expected_file_count': 180, 'checked_file_count': 180, 'package_hash_expected': '29d1ceff514d138c0f2e9743efc5b6d9e5a6bb63f8ee8161d27d0cdae3b598ef', 'package_hash_current': '29d1ceff514d138c0f2e9743efc5b6d9e5a6bb63f8ee8161d27d0cdae3b598ef', 'package_hash_match': True, 'errors': []} | KHỚP |
| RELEASE_MANIFEST.json tái sinh bằng công cụ | Tái sinh deterministic trên bản sao: rc0, 30336 B, SHA 22353f3f1d58431c496377b03ffe12ae5c6b9a77948c7c712ef4b1dbbbf6743f, bằng byte HEAD. Không sửa manifest tay trong HINT. | KHỚP |
| VERSION vẫn1.36.68 từr336 | release-verify và manifest khai skill_version1.36.68; scripts/tl.py có VERSION tương ứng; CHANGELOG mục r336 nêu phiên bản. Không có diff VERSION trong PR. | KHỚP |
| HINT1 8 hunk / 4 tệp được áp nguyên ởa4c14c7 | Tự áp patch --batch --fuzz=0 --verbose trên899f305: rc0,8/8 hunk,4 tệp bằng bytea4c14c7; ngoài HINT chỉ manifest. Tái sinh manifest30335B,b86df2af… bằng byte. Không chứng thực thao tác executor lịch sử chỉ từ kết quả tương đương. | KHỚP |
| R2/R3/R5 hint_patch.noi_dung — một dòng ghi chú | HINT2=1LF/1dòng; HINT3=1LF/1dòng; HINT5=4LF/4dòng. HINT1=120LF, HINT4=9LF, EVIDENCE.HINT4=11LF. Số hunk lần lượt8/0/0/0/0 và EVIDENCE.HINT1hunk; byte/hash trong bảng riêng. | R2/R3 KHỚP; R5 KHÔNG KHỚP — lớp template |
| R4:37 và CHANGELOG:44 — 4/4pr511,34/34pr493,110 dòngr369, r368:111/r367:586 | Tái so Git:4/4 và34/34 bằng byte cha tương ứng;110 dòng đầu cha1+nội dungbase bằng CH@c98c33e; heading1/111/586 khớp. README trừ89hàngpr493 bằng cha1, trừ10dòngpr511 bằngbase;19/19blobneo đúng. | KHỚP |
| R5:37 — 7tệp,+1313/−5;7/7băm soV4,4+34 tệp | git diff8802924...c98c33e xác nhận7/+1313/−5; frontmatter V4/V5 có7SHA bằng nhau và đều bằng blobc98c33e. So34+4tệp cũng khớp. Đây là phép so cùnghead, khác câu7tệp không đổi qua merge ởR3. | KHỚP |
| R4/V4 — dựng lại merge,3tệp xung đột,19neo,72+17 hàngpr493 | Các số có đúng trongV4:47–62,75–88; phép đồng nhất file và19neo được tự kiểm lại ởhistory.json. Không chạy lại git merge sinh conflict-marker lần này, không chứng thực rc/lịch sử reviewer bằng việc đọc báo cáo. | KHỚP số và quan hệ kiểm lại; thao tác dựng merge cũ là(c) |
| R1 3+6 lối land lịch sử,342ref,literalr368/r3693/1 | V1 ghi đúng các số này; lần này tái dựng9 trạng thái land (3HEAD+3R2+3R4), không nhận là chạy lại6 trạng thái PR#511 củaV1. Bộ ref cũ342 không có snapshot đầy đủ để phục hồi từ347hiện tại. | KHỚP báo cáo nguồn; phép chạy/tập ref cũ KHÔNG ĐO ĐƯỢC |
| R2:38 — v283/0/tổng136; R3:37 —83/0; R4/R5 —100/0/tổng153 | Tái chạy v2 trên a41fc69,5f45e6e,c98c33e:83/0/136,83/0/136,100/0/153; khớp. Giá trị t26/t27/release cũ có trong từngV; mutant mới kiểm trên HEAD#517. | KHỚP |
| R5:36 — câu EVIDENCE:9 đúng một lần,áp nguyên EVIDENCE.HINT | V5:29,34,48 ghi câu sửa và so dòng+; patch hiện có1hunk,1940B,sha7acb408c… đúng. Gói#517 không có EVIDENCE của lượt4/5 nguyên bản nên không tự chạy lại phép áp/câu đếm lịch sử. | KHỚP báo cáo/patch; EVIDENCE cũ KHÔNG ĐO ĐƯỢC |
| R5:97/CHANGELOG:51 — last.md rỗng; executor tính băm | last.md không được cấp. SHA verdict đo lại được; không chứng minh ai tính lần đầu từ việc băm khớp. stdout0/rc1/đuôi lỗi đo trực tiếp được. | KHÔNG ĐO ĐƯỢC last.md/ai tính băm lịch sử |
| V5/receipt — chốt20:50:46Z,7băm khớpV4,đủ các mục | V5:41 tự ghi2026-09-11T20:50:46.158039+00:00; các mục có thật,7băm bằngV4. Đây là timestamp reviewer ghi, không attestation độc lập thời điểm ghi tệp. | KHỚP |
| CHANGELOG:9–14 —344/344,comm0/0,r3701,r3710,r3720 ở21:06Z | KHÔNG ĐO ĐƯỢC hai tập ref trên kho nguồn lúc đó; nhãn tác giả thuật lại/KHÔNG ĐO ĐƯỢC đã đặt đúng. Không có mạng, origin là URL GitHub; không gọi ls-remote. | KHÔNG ĐO ĐƯỢC lịch sử; nhãn đúng |
| r370 bị nhường vì phiên kia ghi trước; so tip ref với896bfbf | Tip origin/claude/vaerr-514-authorization-url=7718863 lúc21:28:22Z >896bfbf21:08:50Z. Nhưng commit thêm r370 là368495a lúc20:56:41Z <896bfbf (và <8fd3f48 20:59:13Z). Tipmuộn không bác việc mục r370 được ghi trước; lý do nhường số là(b). | KHỚP thứ tự Git liên quan; động cơ KHÔNG ĐO ĐƯỢC |
| CHANGELOG:85–87 — commit3 sửa tiêu đề/Hệ quả/NỢ,caveatP1/README/manifest | git show86f87b2 đúng4tệp,25insertions/18deletions; loại chỉnh sửa đúng. Câu quota đầu mục còn sót là lớp nguồn; việc4cổng đã chạy trước commit là lịch sử(b). | KHỚP |
| CHANGELOG:39–42 —2P1 connector,6fe742e không tồn tại/squash tổng hợp | git cat-file -t6fe742e rc128 chỉ chứng minh object không có trong clone; hai blobpr511 tại120d47a đúng và neo tổ tiên. Nguồn gốc squash/threads/cơ chế chỉkích lúc bỏdraft là(b), không đo được. | KHỚP kỹ thuật giới hạn tại clone; KHÔNG ĐO ĐƯỢC GitHub |
| CHANGELOG:59 —ubuntu job103411426056 và thu-hoi success; merge20:56:47Z | Commit46d9561 có committerdate2026-09-12T03:56:47+07:00=11-09T20:56:47Z và hai cha đúng. API merge/CI job/trạng thái không có hiện vật độc lập trong gói. | KHỚP Git metadata; KHÔNG ĐO ĐƯỢC sự kiện CI/API |
| CHANGELOG:71–75/99–110 —#512,S6,4finding(1P1+3P2),trần2vòng,2verdict34537/26824B,băm88f0a645/74259a45,doctor2providerTHIẾU | Không có hai verdict#512,CI/connector/doctor output hoặc nguồn luật chủ kho trong gói; không đọc doctrine bị cấm. Các số này là(b)thuật lại, không được tự xác nhận. Việc hai verdict không có trong ops/reviews ởHEAD kiểm được qua danh sách tệp. | KHÔNG ĐO ĐƯỢC các số/trạng thái ngoài gói |
| CHANGELOG:93–109 —giới hạn so_p*/verdict_bytes/assurance,ba lần xác nhận,nợ chưa có packet | Các đoạnr367/r369/r371 nêu hai scalar so_p*/byte đã có nợ; assurance được bổ sung bằng mutantV3. Không hiểu thành cả3trường đều đo ởcả3mục. Mutant mới3scalar sống4/4; tình trạng chưa có packet/chủkho nângtrần là(b), không đo trong phạm vi này. | KHỚP |
| doc-claims-check/doctrine-scan7tệp/số ởmô tảPR | Không chạy riêng các cổng đó và không mở tài liệu bị cấm để kiểm chúng; không có mô tảPR/CIlive. release-verify đã chạy và tự báo checks của nó; không gọi đó là log lịch sử hai lệnh riêng. | KHÔNG ĐO ĐƯỢC lời khai lịch sử |
| EVIDENCE/meta dòngverdict354/238/107/164/84 | Tệp đều kết thúcLF, wc-l353/237/106/163/83. meta516.json mang cùng giá trị+1; các scalar runtime trongmeta khớp nguồnrun/log đã đối chiếu nhưngmeta không được dùng làm căn cứ. | KHÔNG KHỚP số dòng; lỗi ngoài diff chỉ ghi chú |


### Byte, hash, từng scalar runtime, finding, caveat và neo của năm receipt

| khai | đo | khớp? |
|---|---|---|
| R1/nguon: verdict nguyên byte | cmp rc=0 | KHỚP |
| R1:18: verdict_sha256=1a1235739ebf920811570f3a05b3799f8743aa8e7618b7f9099e001d4e8dc1f0 | 1a1235739ebf920811570f3a05b3799f8743aa8e7618b7f9099e001d4e8dc1f0 | KHỚP |
| R1:19: verdict_bytes=74068 | 74068 | KHỚP |
| R1:16: verdict=changes_requested | changes_requested | KHỚP |
| R1:20: reviewed_sha=899f305997544dc78947af6dd58aa490ed3538f3 | 899f305997544dc78947af6dd58aa490ed3538f3 | KHỚP |
| R1:21: reviewed_base=05ba3f96520a7f9e7f8676585cf6041e5e75c796 | 05ba3f96520a7f9e7f8676585cf6041e5e75c796 | KHỚP |
| R1:10: luot=1 | 1 | KHỚP |
| V1: EVIDENCE/meta khai 354 dòng | wc -l=353; splitlines=353; ends_LF=True | KHÔNG KHỚP (ngoài diff; xem P3 tại CHANGELOG:53 cho V5) |
| V1: các mục ## | [(25, '## Bảng đo lại'), (280, '## Findings'), (314, '## Mutant đã chạy'), (343, '## chua_do_duoc')] | KHỚP |
| R1:26: so_p1=0 | 0 heading; frontmatter=0 | KHỚP |
| R1:27: so_p2=4 | 4 heading; frontmatter=4 | KHỚP |
| R1:28: so_p3=1 | 1 heading; frontmatter=1 | KHỚP |
| R1:29: ['tong-hop-mutant-dem-bon-thay-vi-ba', 'pham-vi-no-khong-rong-hon-r367', 'nguon-lich-su-van-gan-nhan-do', 'muc-luc-bo-nhan-thuat-lai-cua-nguon', 'dem-dong-readme-lech-mot'] | [(282, '### tong-hop-mutant-dem-bon-thay-vi-ba [P2]'), (288, '### pham-vi-no-khong-rong-hon-r367 [P2]'), (294, '### nguon-lich-su-van-gan-nhan-do [P2]'), (302, '### muc-luc-bo-nhan-thuat-lai-cua-nguon [P2]'), (310, '### dem-dong-readme-lech-mot [P3]')] | KHỚP |
| R1.hint_patch: sha256=036fa165ad01a6f573046ffb3e3e6f093a1c0d92ff2f754621a53705c17e94df | 036fa165ad01a6f573046ffb3e3e6f093a1c0d92ff2f754621a53705c17e94df | KHỚP |
| R1.hint_patch: bytes=28684 | 28684 | KHỚP |
| HINT1: hunk/tệp | 8/4 | KHỚP |
| R1:48: provider=openai_codex | header: OpenAI Codex v0.154.0; provider: openai; run.json wrapper provider=local_process, execution_surface=subprocess; hai tầng khác nhau | KHỚP |
| R1:49: surface=codex_cli | header: OpenAI Codex v0.154.0; provider: openai; run.json wrapper provider=local_process, execution_surface=subprocess; hai tầng khác nhau | KHỚP |
| R1:50: transport=machine | run.json=machine | KHỚP |
| R1:51: model_yeu_cau=gpt-6-astra | gpt-6-astra | KHỚP |
| R1:52: KHONG_DO_DUOC — codex exec không xuất modelUsage; reviewer tự khai `GPT-6 / Codex` trong model_tu_khai | model_tu_khai=GPT-6 / Codex / OpenAI, theo cấu hình phiên; không chứng thực model build bằng telemetry độc lập; header là cấu hình, không attestation backend | KHÔNG ĐO ĐƯỢC |
| R1:53: effort=xhigh | xhigh | KHỚP |
| R1:54: session_run_id=a146d00d | run.json=a146d00d | KHỚP |
| R1:55: run_id_day_du=a146d00de4044d0dacf3cda7bd63c08c | run.json=a146d00de4044d0dacf3cda7bd63c08c | KHỚP |
| R1:56: prompt_sha256=46c086d5dc016280daddc3ab966b427b7994715d13b7ba0aa478a7a7fef95d2d | run.json=46c086d5dc016280daddc3ab966b427b7994715d13b7ba0aa478a7a7fef95d2d | KHỚP |
| R1:56: prompt_sha256=46c086d5dc016280daddc3ab966b427b7994715d13b7ba0aa478a7a7fef95d2d | đo tệp=46c086d5dc016280daddc3ab966b427b7994715d13b7ba0aa478a7a7fef95d2d | KHỚP |
| R1:57: bat_dau_utc=2026-09-11T19:02:32.739156+00:00 | run.json=2026-09-11T19:02:32.739156+00:00 | KHỚP |
| R1:58: ket_thuc_utc=2026-09-11T19:20:41.998248+00:00 | run.json=2026-09-11T19:20:41.998248+00:00 | KHỚP |
| R1:59: thoi_luong_giay=1089.259 | run.json=1089.259 | KHỚP |
| R1:60: ma_thoat=0 | run.json=0 | KHỚP |
| R1:61: trang_thai=xong | run.json=xong | KHỚP |
| R1:62: stdout_byte=323 | run.json=323 | KHỚP |
| R1:62: stdout_byte=323 | đo tệp=323 | KHỚP |
| R1:63: stdout_sha256=2706f5660800fa5b4cbff3cfe192e71e632c830c9407d3c1a8e90c0521c0a3da | run.json=2706f5660800fa5b4cbff3cfe192e71e632c830c9407d3c1a8e90c0521c0a3da | KHỚP |
| R1:63: stdout_sha256=2706f5660800fa5b4cbff3cfe192e71e632c830c9407d3c1a8e90c0521c0a3da | đo tệp=2706f5660800fa5b4cbff3cfe192e71e632c830c9407d3c1a8e90c0521c0a3da | KHỚP |
| R1:64: stderr_byte=464458 | run.json=464458 | KHỚP |
| R1:64: stderr_byte=464458 | đo tệp=464458 | KHỚP |
| R1:65: stderr_sha256=046afd8feab6c35fef4409d8799e3bd00a6e4172c44eed28062448ad72a1711c | run.json=046afd8feab6c35fef4409d8799e3bd00a6e4172c44eed28062448ad72a1711c | KHỚP |
| R1:65: stderr_sha256=046afd8feab6c35fef4409d8799e3bd00a6e4172c44eed28062448ad72a1711c | đo tệp=046afd8feab6c35fef4409d8799e3bd00a6e4172c44eed28062448ad72a1711c | KHỚP |
| R1:66: so_lan_chet_truoc_khi_xong=0 (attestation) | run.json không có bộ đếm retry; chỉ một run được cấp mỗi lượt | KHÔNG ĐO ĐƯỢC |
| R1:67: prompt.snapshot byte và dòng cuối stdout | prompt 9972 B, sha=46c086d5dc016280daddc3ab966b427b7994715d13b7ba0aa478a7a7fef95d2d; XONG=1a1235739ebf920811570f3a05b3799f8743aa8e7618b7f9099e001d4e8dc1f0 | KHỚP |
| R1:59: 1089.259 | hiệu chính xác=1089.259092; làm tròn 3 chữ số=1089.259 | KHỚP |
| R1:20: 899f305997544dc78947af6dd58aa490ed3538f3 | run.head=899f305997544dc78947af6dd58aa490ed3538f3 | KHỚP |
| R1:84: {'cay_kho_sach': True, 'commit_them_ngoai_head': 0, 'bang_chung': 'run.json worktree_sach: true; reviewer tự đo cuối lượt: HEAD 899f305, git status sạch; chỉ ghi vào scratch/.'} | run.worktree_sach=True; so_muc_ban=0; trạng thái lúc snapshot; không chứng minh mọi thời điểm | KHỚP |
| R1:22: https://github.com/ducthangho/tra-luat/blob/8fd3f484d512f34ab459d1aef09ae2977f07ba65/ops/reviews/pr516-review-1-codex-verdict.md | add commits=['8fd3f484d512f34ab459d1aef09ae2977f07ba65']; ancestor rc=0; blob sha=1a1235739ebf920811570f3a05b3799f8743aa8e7618b7f9099e001d4e8dc1f0, byte=74068 | KHỚP |
| R1.caveat CHANGES-REQUESTED-TREN-899f305-DA-VA-o-a4c14c7-KHONG-phai-trang-thai-cuoi: P2; mo_ta+phai_lam_gi → README | cặp có 1 hàng, dòng [42]; nội dung bằng nhau sau bỏ bold/escape=True | KHỚP |
| R1.caveat BANG-DO-LAI-KHONG-LEN-COMMENT-tep-trong-kho-la-ban-du: P3; mo_ta+phai_lam_gi → README | cặp có 1 hàng, dòng [43]; nội dung bằng nhau sau bỏ bold/escape=True | KHỚP |
| README mục lục R1: byte=74068 | dòng 423, cột byte=74 068 | KHỚP |
| README mục lục R1: thời lượng làm tròn | 1089 s; exact 1089.259092 | KHỚP |
| R2/nguon: verdict nguyên byte | cmp rc=0 | KHỚP |
| R2:18: verdict_sha256=e2d0fc65a809cb7e2be27804f518d41a09a8329b672ae8ebfa438603cb0202fe | e2d0fc65a809cb7e2be27804f518d41a09a8329b672ae8ebfa438603cb0202fe | KHỚP |
| R2:19: verdict_bytes=36923 | 36923 | KHỚP |
| R2:16: verdict=approve | approve | KHỚP |
| R2:20: reviewed_sha=a41fc69f1d06a2976968a2830c19623eb2e8fd29 | a41fc69f1d06a2976968a2830c19623eb2e8fd29 | KHỚP |
| R2:21: reviewed_base=6786637343452359eeb2ec5aaaaef709a623be95 | 6786637343452359eeb2ec5aaaaef709a623be95 | KHỚP |
| R2:10: luot=2 | 2 | KHỚP |
| V2: EVIDENCE/meta khai 238 dòng | wc -l=237; splitlines=237; ends_LF=True | KHÔNG KHỚP (ngoài diff; xem P3 tại CHANGELOG:53 cho V5) |
| V2: các mục ## | [(25, '## ĐỐI CHIẾU LƯỢT TRƯỚC'), (59, '## Bảng đo lại'), (201, '## Findings'), (205, '## Mutant đã chạy'), (228, '## chua_do_duoc')] | KHỚP |
| R2:26: so_p1=0 | 0 heading; frontmatter=0 | KHỚP |
| R2:27: so_p2=0 | 0 heading; frontmatter=0 | KHỚP |
| R2:28: so_p3=0 | 0 heading; frontmatter=0 | KHỚP |
| R2:29: [] | [] | KHỚP |
| R2.hint_patch: sha256=b31ce9e602be0d6f9989a4167496a99b0e2988c796f88db0f6d9bf0b88d407e7 | b31ce9e602be0d6f9989a4167496a99b0e2988c796f88db0f6d9bf0b88d407e7 | KHỚP |
| R2.hint_patch: bytes=82 | 82 | KHỚP |
| HINT2: hunk/tệp | 0/0 | KHỚP |
| R2:42: provider=openai_codex | header: OpenAI Codex v0.154.0; provider: openai; run.json wrapper provider=local_process, execution_surface=subprocess; hai tầng khác nhau | KHỚP |
| R2:43: surface=codex_cli | header: OpenAI Codex v0.154.0; provider: openai; run.json wrapper provider=local_process, execution_surface=subprocess; hai tầng khác nhau | KHỚP |
| R2:44: transport=machine | run.json=machine | KHỚP |
| R2:45: model_yeu_cau=gpt-6-astra | gpt-6-astra | KHỚP |
| R2:46: KHONG_DO_DUOC — codex exec không xuất modelUsage; reviewer tự khai `GPT-6 / Codex` trong model_tu_khai | model_tu_khai=GPT-6 / Codex / OpenAI, theo cấu hình phiên; không chứng thực độc lập model build; header là cấu hình, không attestation backend | KHÔNG ĐO ĐƯỢC |
| R2:47: effort=xhigh | xhigh | KHỚP |
| R2:48: session_run_id=457a6568 | run.json=457a6568 | KHỚP |
| R2:49: run_id_day_du=457a65688ca44a49a6513dbb7ff81c52 | run.json=457a65688ca44a49a6513dbb7ff81c52 | KHỚP |
| R2:50: prompt_sha256=c3a0b624245c69cad155c01c9a103709084b7ce025f10ed17473082ca5ea4043 | run.json=c3a0b624245c69cad155c01c9a103709084b7ce025f10ed17473082ca5ea4043 | KHỚP |
| R2:50: prompt_sha256=c3a0b624245c69cad155c01c9a103709084b7ce025f10ed17473082ca5ea4043 | đo tệp=c3a0b624245c69cad155c01c9a103709084b7ce025f10ed17473082ca5ea4043 | KHỚP |
| R2:51: bat_dau_utc=2026-09-11T19:25:49.390178+00:00 | run.json=2026-09-11T19:25:49.390178+00:00 | KHỚP |
| R2:52: ket_thuc_utc=2026-09-11T19:37:11.951613+00:00 | run.json=2026-09-11T19:37:11.951613+00:00 | KHỚP |
| R2:53: thoi_luong_giay=682.561 | run.json=682.561 | KHỚP |
| R2:54: ma_thoat=0 | run.json=0 | KHỚP |
| R2:55: trang_thai=xong | run.json=xong | KHỚP |
| R2:56: stdout_byte=389 | run.json=389 | KHỚP |
| R2:56: stdout_byte=389 | đo tệp=389 | KHỚP |
| R2:57: stdout_sha256=923a32a7d4a9a738d153a61e90df0ce2933fc96d31df57c57c9af85ad2537bdd | run.json=923a32a7d4a9a738d153a61e90df0ce2933fc96d31df57c57c9af85ad2537bdd | KHỚP |
| R2:57: stdout_sha256=923a32a7d4a9a738d153a61e90df0ce2933fc96d31df57c57c9af85ad2537bdd | đo tệp=923a32a7d4a9a738d153a61e90df0ce2933fc96d31df57c57c9af85ad2537bdd | KHỚP |
| R2:58: stderr_byte=1305501 | run.json=1305501 | KHỚP |
| R2:58: stderr_byte=1305501 | đo tệp=1305501 | KHỚP |
| R2:59: stderr_sha256=b779a7ec78b341003c6f98ab975eab64093e750c3e2bd04d715cd3f45ac1acb0 | run.json=b779a7ec78b341003c6f98ab975eab64093e750c3e2bd04d715cd3f45ac1acb0 | KHỚP |
| R2:59: stderr_sha256=b779a7ec78b341003c6f98ab975eab64093e750c3e2bd04d715cd3f45ac1acb0 | đo tệp=b779a7ec78b341003c6f98ab975eab64093e750c3e2bd04d715cd3f45ac1acb0 | KHỚP |
| R2:60: so_lan_chet_truoc_khi_xong=0 (attestation) | run.json không có bộ đếm retry; chỉ một run được cấp mỗi lượt | KHÔNG ĐO ĐƯỢC |
| R2:61: prompt.snapshot byte và dòng cuối stdout | prompt 6417 B, sha=c3a0b624245c69cad155c01c9a103709084b7ce025f10ed17473082ca5ea4043; XONG=e2d0fc65a809cb7e2be27804f518d41a09a8329b672ae8ebfa438603cb0202fe | KHỚP |
| R2:53: 682.561 | hiệu chính xác=682.561435; làm tròn 3 chữ số=682.561 | KHỚP |
| R2:20: a41fc69f1d06a2976968a2830c19623eb2e8fd29 | run.head=a41fc69f1d06a2976968a2830c19623eb2e8fd29 | KHỚP |
| R2:78: {'cay_kho_sach': True, 'commit_them_ngoai_head': 0, 'bang_chung': 'run.json worktree_sach: true; reviewer tự đo cuối lượt: HEAD a41fc69, git status sạch; chỉ ghi vào scratch/.'} | run.worktree_sach=True; so_muc_ban=0; trạng thái lúc snapshot; không chứng minh mọi thời điểm | KHỚP |
| R2:22: https://github.com/ducthangho/tra-luat/blob/8fd3f484d512f34ab459d1aef09ae2977f07ba65/ops/reviews/pr516-review-2-codex-verdict.md | add commits=['8fd3f484d512f34ab459d1aef09ae2977f07ba65']; ancestor rc=0; blob sha=e2d0fc65a809cb7e2be27804f518d41a09a8329b672ae8ebfa438603cb0202fe, byte=36923 | KHỚP |
| R2.caveat APPROVE-TREN-a41fc69-CONNECTOR-CODEX-RA-2-P1-SAU-DO-mot-DUNG: P2; mo_ta+phai_lam_gi → README | cặp có 1 hàng, dòng [39]; nội dung bằng nhau sau bỏ bold/escape=True | KHỚP |
| R2.caveat VERDICT-BYTES-VA-SO-P-TRONG-BIEN-NHAN-KHONG-CO-CONG-NAO-CANH: P2; mo_ta+phai_lam_gi → README | cặp có 1 hàng, dòng [40]; nội dung bằng nhau sau bỏ bold/escape=True | KHỚP |
| R2.caveat BANG-DO-LAI-KHONG-LEN-COMMENT-tep-trong-kho-la-ban-du: P3; mo_ta+phai_lam_gi → README | cặp có 1 hàng, dòng [41]; nội dung bằng nhau sau bỏ bold/escape=True | KHỚP |
| README mục lục R2: byte=36923 | dòng 422, cột byte=36 923 | KHỚP |
| README mục lục R2: thời lượng làm tròn | 683 s; exact 682.561435 | KHỚP |
| R3/nguon: verdict nguyên byte | cmp rc=0 | KHỚP |
| R3:18: verdict_sha256=532e022c16f75ba5780de45e4e4056788f58ac275d6638a1fbb5c55088cda968 | 532e022c16f75ba5780de45e4e4056788f58ac275d6638a1fbb5c55088cda968 | KHỚP |
| R3:19: verdict_bytes=14796 | 14796 | KHỚP |
| R3:16: verdict=approve | approve | KHỚP |
| R3:20: reviewed_sha=5f45e6e99bcd4cf8a410b99031d4a600bf5e83bb | 5f45e6e99bcd4cf8a410b99031d4a600bf5e83bb | KHỚP |
| R3:21: reviewed_base=6786637343452359eeb2ec5aaaaef709a623be95 | 6786637343452359eeb2ec5aaaaef709a623be95 | KHỚP |
| R3:10: luot=3 | 3 | KHỚP |
| V3: EVIDENCE/meta khai 107 dòng | wc -l=106; splitlines=106; ends_LF=True | KHÔNG KHỚP (ngoài diff; xem P3 tại CHANGELOG:53 cho V5) |
| V3: các mục ## | [(19, '## ĐỐI CHIẾU LƯỢT TRƯỚC'), (27, '## Bảng đo lại'), (71, '## Findings'), (81, '## Mutant đã chạy'), (98, '## chua_do_duoc')] | KHỚP |
| R3:26: so_p1=0 | 0 heading; frontmatter=0 | KHỚP |
| R3:27: so_p2=0 | 0 heading; frontmatter=0 | KHỚP |
| R3:28: so_p3=0 | 0 heading; frontmatter=0 | KHỚP |
| R3:29: [] | [] | KHỚP |
| R3.hint_patch: sha256=f2703a7cad006c63204c715a83f5dbbbb232ecd81fbaa5d75ae8efaff21080e9 | f2703a7cad006c63204c715a83f5dbbbb232ecd81fbaa5d75ae8efaff21080e9 | KHỚP |
| R3.hint_patch: bytes=100 | 100 | KHỚP |
| HINT3: hunk/tệp | 0/0 | KHỚP |
| R3:42: provider=openai_codex | header: OpenAI Codex v0.154.0; provider: openai; run.json wrapper provider=local_process, execution_surface=subprocess; hai tầng khác nhau | KHỚP |
| R3:43: surface=codex_cli | header: OpenAI Codex v0.154.0; provider: openai; run.json wrapper provider=local_process, execution_surface=subprocess; hai tầng khác nhau | KHỚP |
| R3:44: transport=machine | run.json=machine | KHỚP |
| R3:45: model_yeu_cau=gpt-6-astra | gpt-6-astra | KHỚP |
| R3:46: KHONG_DO_DUOC — codex exec không xuất modelUsage; reviewer tự khai `GPT-6 / Codex` trong model_tu_khai | model_tu_khai=GPT-6 / Codex (tự khai theo ngữ cảnh phiên; không xác thực độc lập backend); header là cấu hình, không attestation backend | KHÔNG ĐO ĐƯỢC |
| R3:47: effort=xhigh | xhigh | KHỚP |
| R3:48: session_run_id=0449ddb0 | run.json=0449ddb0 | KHỚP |
| R3:49: run_id_day_du=0449ddb060af46b6ba99417600e752c4 | run.json=0449ddb060af46b6ba99417600e752c4 | KHỚP |
| R3:50: prompt_sha256=890ab3aa7d61fb0a3c120ef744cc4df654db842420b87ebb08e574007cc3c405 | run.json=890ab3aa7d61fb0a3c120ef744cc4df654db842420b87ebb08e574007cc3c405 | KHỚP |
| R3:50: prompt_sha256=890ab3aa7d61fb0a3c120ef744cc4df654db842420b87ebb08e574007cc3c405 | đo tệp=890ab3aa7d61fb0a3c120ef744cc4df654db842420b87ebb08e574007cc3c405 | KHỚP |
| R3:51: bat_dau_utc=2026-09-11T19:57:45.973441+00:00 | run.json=2026-09-11T19:57:45.973441+00:00 | KHỚP |
| R3:52: ket_thuc_utc=2026-09-11T20:05:28.210979+00:00 | run.json=2026-09-11T20:05:28.210979+00:00 | KHỚP |
| R3:53: thoi_luong_giay=462.238 | run.json=462.238 | KHỚP |
| R3:54: ma_thoat=0 | run.json=0 | KHỚP |
| R3:55: trang_thai=xong | run.json=xong | KHỚP |
| R3:56: stdout_byte=330 | run.json=330 | KHỚP |
| R3:56: stdout_byte=330 | đo tệp=330 | KHỚP |
| R3:57: stdout_sha256=67060145c80ff8f672084f78d5c36c8f5dd3e891eed8e6ef643c5e80c0182e08 | run.json=67060145c80ff8f672084f78d5c36c8f5dd3e891eed8e6ef643c5e80c0182e08 | KHỚP |
| R3:57: stdout_sha256=67060145c80ff8f672084f78d5c36c8f5dd3e891eed8e6ef643c5e80c0182e08 | đo tệp=67060145c80ff8f672084f78d5c36c8f5dd3e891eed8e6ef643c5e80c0182e08 | KHỚP |
| R3:58: stderr_byte=406484 | run.json=406484 | KHỚP |
| R3:58: stderr_byte=406484 | đo tệp=406484 | KHỚP |
| R3:59: stderr_sha256=c5d3f7ff6aa18ee0d2f17f45c2cb6a3d8957d3a2a47f2dc87bc747c7f4757e62 | run.json=c5d3f7ff6aa18ee0d2f17f45c2cb6a3d8957d3a2a47f2dc87bc747c7f4757e62 | KHỚP |
| R3:59: stderr_sha256=c5d3f7ff6aa18ee0d2f17f45c2cb6a3d8957d3a2a47f2dc87bc747c7f4757e62 | đo tệp=c5d3f7ff6aa18ee0d2f17f45c2cb6a3d8957d3a2a47f2dc87bc747c7f4757e62 | KHỚP |
| R3:60: so_lan_chet_truoc_khi_xong=0 (attestation) | run.json không có bộ đếm retry; chỉ một run được cấp mỗi lượt | KHÔNG ĐO ĐƯỢC |
| R3:61: prompt.snapshot byte và dòng cuối stdout | prompt 6140 B, sha=890ab3aa7d61fb0a3c120ef744cc4df654db842420b87ebb08e574007cc3c405; XONG=532e022c16f75ba5780de45e4e4056788f58ac275d6638a1fbb5c55088cda968 | KHỚP |
| R3:53: 462.238 | hiệu chính xác=462.237538; làm tròn 3 chữ số=462.238 | KHỚP |
| R3:20: 5f45e6e99bcd4cf8a410b99031d4a600bf5e83bb | run.head=5f45e6e99bcd4cf8a410b99031d4a600bf5e83bb | KHỚP |
| R3:78: {'cay_kho_sach': True, 'commit_them_ngoai_head': 0, 'bang_chung': 'run.json worktree_sach: true; reviewer tự đo cuối lượt: HEAD 5f45e6e, git status sạch; chỉ ghi vào scratch/.'} | run.worktree_sach=True; so_muc_ban=0; trạng thái lúc snapshot; không chứng minh mọi thời điểm | KHỚP |
| R3:22: https://github.com/ducthangho/tra-luat/blob/8fd3f484d512f34ab459d1aef09ae2977f07ba65/ops/reviews/pr516-review-3-codex-verdict.md | add commits=['8fd3f484d512f34ab459d1aef09ae2977f07ba65']; ancestor rc=0; blob sha=532e022c16f75ba5780de45e4e4056788f58ac275d6638a1fbb5c55088cda968, byte=14796 | KHỚP |
| R3.caveat APPROVE-TREN-5f45e6e-KHONG-PHAI-HEAD-DA-MERGE-xung-dot-voi-r368: P2; mo_ta+phai_lam_gi → README | cặp có 1 hàng, dòng [36]; nội dung bằng nhau sau bỏ bold/escape=True | KHỚP |
| R3.caveat REVIEWER-TU-KHAI-LOI-PHAM-VI-DOC-launcher-ngoai-bang-_TRANSPORT_CONTRACTS: P3; mo_ta+phai_lam_gi → README | cặp có 1 hàng, dòng [37]; nội dung bằng nhau sau bỏ bold/escape=True | KHỚP |
| R3.caveat BANG-DO-LAI-KHONG-LEN-COMMENT-tep-trong-kho-la-ban-du: P3; mo_ta+phai_lam_gi → README | cặp có 1 hàng, dòng [38]; nội dung bằng nhau sau bỏ bold/escape=True | KHỚP |
| README mục lục R3: byte=14796 | dòng 421, cột byte=14 796 | KHỚP |
| README mục lục R3: thời lượng làm tròn | 462 s; exact 462.237538 | KHỚP |
| R4/nguon: verdict nguyên byte | cmp rc=0 | KHỚP |
| R4:18: verdict_sha256=4d227acbc81641f2a25d68870ecf3dbb047a9df390b4382afd853e9452496ca4 | 4d227acbc81641f2a25d68870ecf3dbb047a9df390b4382afd853e9452496ca4 | KHỚP |
| R4:19: verdict_bytes=16275 | 16275 | KHỚP |
| R4:16: verdict=changes_requested | changes_requested | KHỚP |
| R4:20: reviewed_sha=c98c33eb3e3260a10cd98dc0a6118981a45b7639 | c98c33eb3e3260a10cd98dc0a6118981a45b7639 | KHỚP |
| R4:21: reviewed_base=8802924d1744b4c3bcde8a198265b86b89c957bc | 8802924d1744b4c3bcde8a198265b86b89c957bc | KHỚP |
| R4:10: luot=4 | 4 | KHỚP |
| V4: EVIDENCE/meta khai 164 dòng | wc -l=163; splitlines=163; ends_LF=True | KHÔNG KHỚP (ngoài diff; xem P3 tại CHANGELOG:53 cho V5) |
| V4: các mục ## | [(19, '## ĐỐI CHIẾU LƯỢT TRƯỚC'), (35, '## Bảng đo lại'), (96, '## Findings'), (128, '## Mutant đã chạy'), (146, '## chua_do_duoc')] | KHỚP |
| R4:26: so_p1=0 | 0 heading; frontmatter=0 | KHỚP |
| R4:27: so_p2=1 | 1 heading; frontmatter=1 | KHỚP |
| R4:28: so_p3=0 | 0 heading; frontmatter=0 | KHỚP |
| R4:29: ['p2-e01-evidence-khai-doan-nguon-493-khong-ton-tai'] | [(98, '### P2-E01 — [P2] EVIDENCE khai giữ một đoạn nguồn riêng của #493 mà base không có')]; id trong receipt là alias chữ thường của P2-E01 cùng nội dung, không phải slug nguyên văn nguồn | KHỚP NỘI DUNG (ALIAS) |
| R4.hint_patch: sha256=a17f443e68231401403060b63899e723b1810d54b55e452ed6c1e88f9643f195 | a17f443e68231401403060b63899e723b1810d54b55e452ed6c1e88f9643f195 | KHỚP |
| R4.hint_patch: bytes=853 | 853 | KHỚP |
| HINT4: hunk/tệp | 0/0 | KHỚP |
| R4:43: provider=openai_codex | header: OpenAI Codex v0.154.0; provider: openai; run.json wrapper provider=local_process, execution_surface=subprocess; hai tầng khác nhau | KHỚP |
| R4:44: surface=codex_cli | header: OpenAI Codex v0.154.0; provider: openai; run.json wrapper provider=local_process, execution_surface=subprocess; hai tầng khác nhau | KHỚP |
| R4:45: transport=machine | run.json=machine | KHỚP |
| R4:46: model_yeu_cau=gpt-6-astra | gpt-6-astra | KHỚP |
| R4:47: KHONG_DO_DUOC — codex exec không xuất modelUsage; reviewer tự khai `GPT-6 / Codex` trong model_tu_khai | model_tu_khai=GPT-6 / Codex (tự khai theo ngữ cảnh phiên; không xác thực độc lập backend); header là cấu hình, không attestation backend | KHÔNG ĐO ĐƯỢC |
| R4:48: effort=xhigh | xhigh | KHỚP |
| R4:49: session_run_id=04792ddf | run.json=04792ddf | KHỚP |
| R4:50: run_id_day_du=04792ddf40654b9c86152a66b714a85a | run.json=04792ddf40654b9c86152a66b714a85a | KHỚP |
| R4:51: prompt_sha256=3b27cd89c9e47b6f6a7b8153f7533ad17aaed0a02f94addd5de0c94863344795 | run.json=3b27cd89c9e47b6f6a7b8153f7533ad17aaed0a02f94addd5de0c94863344795 | KHỚP |
| R4:51: prompt_sha256=3b27cd89c9e47b6f6a7b8153f7533ad17aaed0a02f94addd5de0c94863344795 | đo tệp=3b27cd89c9e47b6f6a7b8153f7533ad17aaed0a02f94addd5de0c94863344795 | KHỚP |
| R4:52: bat_dau_utc=2026-09-11T20:33:15.430967+00:00 | run.json=2026-09-11T20:33:15.430967+00:00 | KHỚP |
| R4:53: ket_thuc_utc=2026-09-11T20:43:46.465180+00:00 | run.json=2026-09-11T20:43:46.465180+00:00 | KHỚP |
| R4:54: thoi_luong_giay=631.034 | run.json=631.034 | KHỚP |
| R4:55: ma_thoat=0 | run.json=0 | KHỚP |
| R4:56: trang_thai=xong | run.json=xong | KHỚP |
| R4:57: stdout_byte=482 | run.json=482 | KHỚP |
| R4:57: stdout_byte=482 | đo tệp=482 | KHỚP |
| R4:58: stdout_sha256=cd96c28be34dc069cd41622171cd008583a4392d119e05228f276db3a0656341 | run.json=cd96c28be34dc069cd41622171cd008583a4392d119e05228f276db3a0656341 | KHỚP |
| R4:58: stdout_sha256=cd96c28be34dc069cd41622171cd008583a4392d119e05228f276db3a0656341 | đo tệp=cd96c28be34dc069cd41622171cd008583a4392d119e05228f276db3a0656341 | KHỚP |
| R4:59: stderr_byte=397589 | run.json=397589 | KHỚP |
| R4:59: stderr_byte=397589 | đo tệp=397589 | KHỚP |
| R4:60: stderr_sha256=9e412aa864d501d9e90e33b9428642f2708319ac21ab6894b0db7dc9a3b4f7d1 | run.json=9e412aa864d501d9e90e33b9428642f2708319ac21ab6894b0db7dc9a3b4f7d1 | KHỚP |
| R4:60: stderr_sha256=9e412aa864d501d9e90e33b9428642f2708319ac21ab6894b0db7dc9a3b4f7d1 | đo tệp=9e412aa864d501d9e90e33b9428642f2708319ac21ab6894b0db7dc9a3b4f7d1 | KHỚP |
| R4:61: so_lan_chet_truoc_khi_xong=0 (attestation) | run.json không có bộ đếm retry; chỉ một run được cấp mỗi lượt | KHÔNG ĐO ĐƯỢC |
| R4:62: prompt.snapshot byte và dòng cuối stdout | prompt 5086 B, sha=3b27cd89c9e47b6f6a7b8153f7533ad17aaed0a02f94addd5de0c94863344795; XONG=4d227acbc81641f2a25d68870ecf3dbb047a9df390b4382afd853e9452496ca4 | KHỚP |
| R4:54: 631.034 | hiệu chính xác=631.034213; làm tròn 3 chữ số=631.034 | KHỚP |
| R4:20: c98c33eb3e3260a10cd98dc0a6118981a45b7639 | run.head=c98c33eb3e3260a10cd98dc0a6118981a45b7639 | KHỚP |
| R4:79: {'cay_kho_sach': True, 'commit_them_ngoai_head': 0, 'bang_chung': 'run.json worktree_sach: true; reviewer tự đo cuối lượt: HEAD c98c33e, git status sạch; chỉ ghi vào scratch/.'} | run.worktree_sach=True; so_muc_ban=0; trạng thái lúc snapshot; không chứng minh mọi thời điểm | KHỚP |
| R4:22: https://github.com/ducthangho/tra-luat/blob/8fd3f484d512f34ab459d1aef09ae2977f07ba65/ops/reviews/pr516-review-4-codex-verdict.md | add commits=['8fd3f484d512f34ab459d1aef09ae2977f07ba65']; ancestor rc=0; blob sha=4d227acbc81641f2a25d68870ecf3dbb047a9df390b4382afd853e9452496ca4, byte=16275 | KHỚP |
| R4.caveat CHANGES-REQUESTED-CHI-VI-EVIDENCE-GOI-REVIEW-cay-kho-duoc-ket-luan-giu-du-hai-phia: P2; mo_ta+phai_lam_gi → README | cặp có 1 hàng, dòng [34]; nội dung bằng nhau sau bỏ bold/escape=True | KHỚP |
| R4.caveat BANG-DO-LAI-KHONG-LEN-COMMENT-tep-trong-kho-la-ban-du: P3; mo_ta+phai_lam_gi → README | cặp có 1 hàng, dòng [35]; nội dung bằng nhau sau bỏ bold/escape=True | KHỚP |
| README mục lục R4: byte=16275 | dòng 420, cột byte=16 275 | KHỚP |
| README mục lục R4: thời lượng làm tròn | 631 s; exact 631.034213 | KHỚP |
| R5/nguon: verdict nguyên byte | cmp rc=0 | KHỚP |
| R5:18: verdict_sha256=d66f58020aa0330c44597fe87635c9f70eb60d49e5db444cd09da7b24a82a38b | d66f58020aa0330c44597fe87635c9f70eb60d49e5db444cd09da7b24a82a38b | KHỚP |
| R5:19: verdict_bytes=7577 | 7577 | KHỚP |
| R5:16: verdict=approve | approve | KHỚP |
| R5:20: reviewed_sha=c98c33eb3e3260a10cd98dc0a6118981a45b7639 | c98c33eb3e3260a10cd98dc0a6118981a45b7639 | KHỚP |
| R5:21: reviewed_base=8802924d1744b4c3bcde8a198265b86b89c957bc | 8802924d1744b4c3bcde8a198265b86b89c957bc | KHỚP |
| R5:10: luot=5 | 5 | KHỚP |
| V5: EVIDENCE/meta khai 84 dòng | wc -l=83; splitlines=83; ends_LF=True | KHÔNG KHỚP (ngoài diff; xem P3 tại CHANGELOG:53 cho V5) |
| V5: các mục ## | [(21, '## ĐỐI CHIẾU LƯỢT TRƯỚC'), (38, '## Bảng đo lại'), (62, '## Findings'), (68, '## Mutant đã chạy'), (72, '## chua_do_duoc')] | KHỚP |
| R5:26: so_p1=0 | 0 heading; frontmatter=0 | KHỚP |
| R5:27: so_p2=0 | 0 heading; frontmatter=0 | KHỚP |
| R5:28: so_p3=0 | 0 heading; frontmatter=0 | KHỚP |
| R5:29: [] | [] | KHỚP |
| R5.hint_patch: sha256=434746d144c289eb5ee7301cf0de704338857ab40c1c50cad0f26928f0960c0c | 434746d144c289eb5ee7301cf0de704338857ab40c1c50cad0f26928f0960c0c | KHỚP |
| R5.hint_patch: bytes=300 | 300 | KHỚP |
| HINT5: hunk/tệp | 0/0 | KHỚP |
| R5:41: provider=openai_codex | header: OpenAI Codex v0.154.0; provider: openai; run.json wrapper provider=local_process, execution_surface=subprocess; hai tầng khác nhau | KHỚP |
| R5:42: surface=codex_cli | header: OpenAI Codex v0.154.0; provider: openai; run.json wrapper provider=local_process, execution_surface=subprocess; hai tầng khác nhau | KHỚP |
| R5:43: transport=machine | run.json=machine | KHỚP |
| R5:44: model_yeu_cau=gpt-6-astra | gpt-6-astra | KHỚP |
| R5:45: KHONG_DO_DUOC — codex exec không xuất modelUsage; reviewer tự khai `GPT-6 / Codex` trong model_tu_khai | model_tu_khai=GPT-6 / Codex (tự khai theo ngữ cảnh phiên; không xác thực độc lập backend); header là cấu hình, không attestation backend | KHÔNG ĐO ĐƯỢC |
| R5:46: effort=xhigh | xhigh | KHỚP |
| R5:47: session_run_id=6c8b0629 | run.json=6c8b0629 | KHỚP |
| R5:48: run_id_day_du=6c8b06299cc84124ab44f2b714dc23f1 | run.json=6c8b06299cc84124ab44f2b714dc23f1 | KHỚP |
| R5:49: prompt_sha256=d76cba7dbcc6cd8e053677833cd457706dc011092ab45f3284955c91052aad65 | run.json=d76cba7dbcc6cd8e053677833cd457706dc011092ab45f3284955c91052aad65 | KHỚP |
| R5:49: prompt_sha256=d76cba7dbcc6cd8e053677833cd457706dc011092ab45f3284955c91052aad65 | đo tệp=d76cba7dbcc6cd8e053677833cd457706dc011092ab45f3284955c91052aad65 | KHỚP |
| R5:50: bat_dau_utc=2026-09-11T20:46:27.703545+00:00 | run.json=2026-09-11T20:46:27.703545+00:00 | KHỚP |
| R5:51: ket_thuc_utc=2026-09-11T20:50:47.714891+00:00 | run.json=2026-09-11T20:50:47.714891+00:00 | KHỚP |
| R5:52: thoi_luong_giay=260.011 | run.json=260.011 | KHỚP |
| R5:53: ma_thoat=1 | run.json=1 | KHỚP |
| R5:54: trang_thai=xong | run.json=xong | KHỚP |
| R5:55: stdout_byte=0 | run.json=0 | KHỚP |
| R5:55: stdout_byte=0 | đo tệp=0 | KHỚP |
| R5:56: stdout_sha256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | run.json=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | KHỚP |
| R5:56: stdout_sha256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | đo tệp=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | KHỚP |
| R5:57: stderr_byte=169008 | run.json=169008 | KHỚP |
| R5:57: stderr_byte=169008 | đo tệp=169008 | KHỚP |
| R5:58: stderr_sha256=0ab8223ccf43092542c385f74217b05576d561eb82d43632ab9b4cdde69e6db4 | run.json=0ab8223ccf43092542c385f74217b05576d561eb82d43632ab9b4cdde69e6db4 | KHỚP |
| R5:58: stderr_sha256=0ab8223ccf43092542c385f74217b05576d561eb82d43632ab9b4cdde69e6db4 | đo tệp=0ab8223ccf43092542c385f74217b05576d561eb82d43632ab9b4cdde69e6db4 | KHỚP |
| R5:59: so_lan_chet_truoc_khi_xong=0 (attestation) | run.json không có bộ đếm retry; chỉ một run được cấp mỗi lượt | KHÔNG ĐO ĐƯỢC |
| R5:60: prompt.snapshot byte và dòng cuối stdout | prompt 3739 B, sha=d76cba7dbcc6cd8e053677833cd457706dc011092ab45f3284955c91052aad65; XONG=KHÔNG CÓ | KHỚP |
| R5:52: 260.011 | hiệu chính xác=260.011346; làm tròn 3 chữ số=260.011 | KHỚP |
| R5:20: c98c33eb3e3260a10cd98dc0a6118981a45b7639 | run.head=c98c33eb3e3260a10cd98dc0a6118981a45b7639 | KHỚP |
| R5:77: {'cay_kho_sach': True, 'commit_them_ngoai_head': 0, 'bang_chung': 'run.json worktree_sach: true; reviewer tự đo cuối lượt: HEAD c98c33e, git status sạch; chỉ ghi vào scratch/.'} | run.worktree_sach=True; so_muc_ban=0; trạng thái lúc snapshot; không chứng minh mọi thời điểm | KHỚP |
| R5:22: https://github.com/ducthangho/tra-luat/blob/8fd3f484d512f34ab459d1aef09ae2977f07ba65/ops/reviews/pr516-review-5-codex-verdict.md | add commits=['8fd3f484d512f34ab459d1aef09ae2977f07ba65']; ancestor rc=0; blob sha=d66f58020aa0330c44597fe87635c9f70eb60d49e5db444cd09da7b24a82a38b, byte=7577 | KHỚP |
| R5.caveat MA-THOAT-1-CODEX-HET-QUOTA-luc-ket-thuc-verdict-day-du-tren-dia-assurance-cross_reviewed: P1; mo_ta+phai_lam_gi → README | cặp có 1 hàng, dòng [31]; nội dung bằng nhau sau bỏ bold/escape=True | KHỚP |
| R5.caveat APPROVE-HO-SO-la-dieu-kien-DUNG-merge-theo-LUAT-CHUNG-chu-kho-14-4xZ: P2; mo_ta+phai_lam_gi → README | cặp có 1 hàng, dòng [32]; nội dung bằng nhau sau bỏ bold/escape=True | KHỚP |
| R5.caveat LUOT-5-KHONG-DO-LAI-merge-land-mutant-nhu-luot-4: P3; mo_ta+phai_lam_gi → README | cặp có 1 hàng, dòng [33]; nội dung bằng nhau sau bỏ bold/escape=True | KHỚP |
| README mục lục R5: byte=7577 | dòng 419, cột byte=7 577 | KHỚP |
| README mục lục R5: thời lượng làm tròn | 260 s; exact 260.011346 | KHỚP |
| EVIDENCE.HINT4: sha 7acb408c…, 1 hunk | 7acb408cb1ba8dcc6327502daa8ad3fe9ec8719b85b405fdcb688686c322ea62, 1940 B, 1 hunk, 1 tệp | KHỚP |
| quét ref hiện tại: tiêu đề r370 | 2: ['refs/remotes/origin/claude/vaerr-514-authorization-url', 'refs/remotes/origin/claude/vaerr-514-authorization-url-wip']; tổng ref=347 | KHỚP |
| quét ref hiện tại: tiêu đề r371 | 1: ['refs/remotes/origin/claude/land-516-bookkeeping']; tổng ref=347 | KHỚP |
| quét ref hiện tại: tiêu đề r372 | 0: []; tổng ref=347 | KHỚP |
| chuỗi neo/commit: 46d9561 | 46d9561c8cc4b0cf530fc7ca4015de8f07c6aeec 8802924d1744b4c3bcde8a198265b86b89c957bc c98c33eb3e3260a10cd98dc0a6118981a45b7639 2026-09-12T03:56:47+07:00 Merge pull request #516 from ducthangho/claude/land-511-bookkeeping | KHỚP |
| chuỗi neo/commit: c98c33e | c98c33eb3e3260a10cd98dc0a6118981a45b7639 5f45e6e99bcd4cf8a410b99031d4a600bf5e83bb 8802924d1744b4c3bcde8a198265b86b89c957bc 2026-09-11T20:27:25+00:00 Merge origin/master (8802924, PR #514 = r368 hồ sơ #493) vào claude/land-511-bookkeeping — giải xung đột CHANGELOG (r369 trên r368), README (hàng cảnh báo/mục lục hai bên đều giữ, r369 trước), manifest tái sinh bằng công cụ | KHỚP |
| chuỗi neo/commit: 5f45e6e | 5f45e6e99bcd4cf8a410b99031d4a600bf5e83bb a41fc69f1d06a2976968a2830c19623eb2e8fd29 2026-09-11T19:54:56+00:00 r369: Codex connector P1 (a41fc69) — hạ assurance receipt lượt 2 của #511 cross_approved → cross_reviewed vì verdict thiếu mục ĐỐI CHIẾU LƯỢT TRƯỚC; caveat + README + CHANGELOG; P1 "re-anchor" không áp dụng (commit 6fe742e không tồn tại — squash tổng hợp của connector); manifest tái sinh | KHỚP |
| chuỗi neo/commit: a41fc69 | a41fc69f1d06a2976968a2830c19623eb2e8fd29 a4c14c72cb743638f05f7c7b5a7710c27aa60993 6786637343452359eeb2ec5aaaaef709a623be95 2026-09-11T19:22:02+00:00 Merge origin/master (6786637, PR #515 cong_cu) vào claude/land-511-bookkeeping — làm mới base.sha cho preflight thu-hoi; không chạm hồ sơ | KHỚP |
| chuỗi neo/commit: a4c14c7 | a4c14c72cb743638f05f7c7b5a7710c27aa60993 899f305997544dc78947af6dd58aa490ed3538f3 2026-09-11T19:22:01+00:00 r369: áp NGUYÊN HINT cross-review hồ sơ lượt 1 (codex, 0 P1 / 4 P2 / 1 P3) — đếm đúng 5 mutant (3 ĐỎ / 2 SỐNG), nợ so_p*/verdict_bytes KHÔNG rộng hơn r367 (0 trường mới), số ref lịch sử gắn nhãn KHÔNG ĐO ĐƯỢC, README mang nhãn nguồn (b)/(c) và "số lần chết 0 là attestation", README 637→646 dòng; manifest tái sinh | KHỚP |
| chuỗi neo/commit: 8fd3f48 | 8fd3f484d512f34ab459d1aef09ae2977f07ba65 46d9561c8cc4b0cf530fc7ca4015de8f07c6aeec 2026-09-11T20:59:13+00:00 r371: 5 verdict codex cross-review HỒ SƠ của PR #516 (r369) vào ops/reviews/ — NGUYÊN BYTE, commit riêng làm neo blob cho evidence_url | KHỚP |
| chuỗi neo/commit: 896bfbf | 896bfbf5718ba4ffa443674e1b61d0719a8794bf 8fd3f484d512f34ab459d1aef09ae2977f07ba65 2026-09-11T21:08:50+00:00 r371: ghi sổ #516 — 5 biên nhận v2 cho 5 verdict codex (neo blob 8fd3f48), README (1 đoạn nguồn + 13 cảnh báo + 5 hàng mục lục), CHANGELOG r371, manifest tái sinh | KHỚP |
| chuỗi neo/commit: 86f87b2 | 86f87b2004f6054572cc787ae660518763b29b95 896bfbf5718ba4ffa443674e1b61d0719a8794bf 2026-09-12T02:30:40+00:00 r371: sửa lời khai quota — "không thể cross-review trước 15-09" là lời của công cụ, không phải phép đo (probe codex 02:3xZ 12-09 rc=0) | KHỚP |


### Metadata và từng khối lời khai còn lại trong receipt

| khai | đo | khớp? |
|---|---|---|
| ops/reviews/pr516-review-1-codex-verdict.receipt.yaml:4 schema_version=2 | YAML parse được; schema v2 kiểm đạt ở HEAD; đây là trường phân loại hồ sơ. | KHỚP lược đồ |
| ops/reviews/pr516-review-1-codex-verdict.receipt.yaml:5 receipt_id=pr516-review-1-codex-20260911-a146d00d | ID gắn PR516/lượt1/ngày20260911/short_ida146d00d,không có va chạm trong5receipt. | KHỚP đối chiếu cấu tạo |
| ops/reviews/pr516-review-1-codex-verdict.receipt.yaml:6 kind=review_delivery_receipt | YAML parse được; schema v2 kiểm đạt ở HEAD; đây là trường phân loại hồ sơ. | KHỚP lược đồ |
| ops/reviews/pr516-review-1-codex-verdict.receipt.yaml:7 packet_id=PR516-BOOKKEEPING-511 | Metadata do tác giả gán (PRhồsơ/khônglease/role/phiênviết); prompt/commit mô tả cùng vai trò. Không có chứngthực độc lập cho nghĩa ngoàiYAML. | KHAI BÁO; không nâng thành đo |
| ops/reviews/pr516-review-1-codex-verdict.receipt.yaml:8 lease_id=khong-co-lease | Metadata do tác giả gán (PRhồsơ/khônglease/role/phiênviết); prompt/commit mô tả cùng vai trò. Không có chứngthực độc lập cho nghĩa ngoàiYAML. | KHAI BÁO; không nâng thành đo |
| ops/reviews/pr516-review-1-codex-verdict.receipt.yaml:9 phase_key=HO-SO-CROSS-REVIEW-PHIEN-20260911 | Metadata do tác giả gán (PRhồsơ/khônglease/role/phiênviết); prompt/commit mô tả cùng vai trò. Không có chứngthực độc lập cho nghĩa ngoàiYAML. | KHAI BÁO; không nâng thành đo |
| ops/reviews/pr516-review-1-codex-verdict.receipt.yaml:11 role=reviewer | Metadata do tác giả gán (PRhồsơ/khônglease/role/phiênviết); prompt/commit mô tả cùng vai trò. Không có chứngthực độc lập cho nghĩa ngoàiYAML. | KHAI BÁO; không nâng thành đo |
| ops/reviews/pr516-review-1-codex-verdict.receipt.yaml:12 provider=codex | Reviewer tự khai Codex; tác giả commit tự khai Claude. Headerlog phù hợp; không chứng thực danh tính thực/khác backend. | KHỚP tự khai; backend KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-1-codex-verdict.receipt.yaml:13 executor_provider=claude | Reviewer tự khai Codex; tác giả commit tự khai Claude. Headerlog phù hợp; không chứng thực danh tính thực/khác backend. | KHỚP tự khai; backend KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-1-codex-verdict.receipt.yaml:14 cross_provider=True | Reviewer tự khai Codex; tác giả commit tự khai Claude. Headerlog phù hợp; không chứng thực danh tính thực/khác backend. | KHỚP tự khai; backend KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-1-codex-verdict.receipt.yaml:124 delivered=True | verdict và receipt có thật ở HEAD,blobneo đúng; không suy đã giao lên comment từ delivered. | KHỚP hiện vật repo |
| ops/reviews/pr516-review-1-codex-verdict.receipt.yaml:125 delivered_by=claude-session | Metadata do tác giả gán (PRhồsơ/khônglease/role/phiênviết); prompt/commit mô tả cùng vai trò. Không có chứngthực độc lập cho nghĩa ngoàiYAML. | KHAI BÁO; không nâng thành đo |
| ops/reviews/pr516-review-1-codex-verdict.receipt.yaml:126 authoritative_source=repo_file | verdict và receipt có thật ở HEAD,blobneo đúng; không suy đã giao lên comment từ delivered. | KHỚP hiện vật repo |
| ops/reviews/pr516-review-1-codex-verdict.receipt.yaml:127 receipt_written_by=claude-session | Metadata do tác giả gán (PRhồsơ/khônglease/role/phiênviết); prompt/commit mô tả cùng vai trò. Không có chứngthực độc lập cho nghĩa ngoàiYAML. | KHAI BÁO; không nâng thành đo |
| ops/reviews/pr516-review-1-codex-verdict.receipt.yaml:128 receipt_written_at_utc=2026-09-11T21:06:00Z | Timestamp21:06:00Z có thật trongYAML; commitchứareceipt896bfbf21:08:50Z nên thứtự có thể phùhợp, không đo thờiđiểmghi thực tế. | KHÔNG ĐO ĐƯỢC thời điểm viết |
| ops/reviews/pr516-review-1-codex-verdict.receipt.yaml:40 mục1: 2 verdict pr511 trong kho `cmp` khớp byte bản sandbox; băm/byte 2 receipt và cột byte 2 hàng README khớp; số finding đếm từ tiêu đề khớp so_p1/so_p2/so_p3; run.json 417a209c/8873d98d CÓ `thoi_luong_giay` khớp hiệu timestamp; neo blob 120d47a đúng 1 commit, tổ tiên HEAD. | Đối chiếu nội dung V1 và bảng kỹ thuật phía trên. Các băm/Git/cổng tái chạy được ghi riêng; phép chạy/remote/runtime #511 ở sandbox lịch sử là nguồn(c), không chứng thực lại toàn bộ từ lời kể. | KHỚP nguồn theo phạm vi; phần không tái đo = KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-1-codex-verdict.receipt.yaml:40 mục2: 5 mutant cổng: M1 (băm verdict) v2+t26 ĐỎ; M2 (xoá hàng cảnh báo) t27 ĐỎ; M4 (evidence_url sang commit không chứa tệp) v2 ĐỎ; M3 (so_p2 5→4) và M5 (verdict_bytes 83049→83048) SỐNG 4/4 — giới hạn cổng đã công khai từ r367. | Đối chiếu nội dung V1 và bảng kỹ thuật phía trên. Các băm/Git/cổng tái chạy được ghi riêng; phép chạy/remote/runtime #511 ở sandbox lịch sử là nguồn(c), không chứng thực lại toàn bộ từ lời kể. | KHỚP nguồn theo phạm vi; phần không tái đo = KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-1-codex-verdict.receipt.yaml:40 mục3: 3 lối land lên 05ba3f9: merge/ff giữ neo 120d47a (v2 83 ĐẠT); squash ⇒ anchor rc=1, v2 81 ĐẠT / 2 vi phạm (2 receipt pr511). Thêm 6 lối land lịch sử của hai head PR #511 tái lập đúng số r367 (79/2 vi phạm). | Đối chiếu nội dung V1 và bảng kỹ thuật phía trên. Các băm/Git/cổng tái chạy được ghi riêng; phép chạy/remote/runtime #511 ở sandbox lịch sử là nguồn(c), không chứng thực lại toàn bộ từ lời kể. | KHỚP nguồn theo phạm vi; phần không tái đo = KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-1-codex-verdict.receipt.yaml:40 mục4: 4 P2: (a) receipt1:44 + README:332 viết "4 mutant ĐỎ" khi nguồn có 5 mutant (3 ĐỎ / 2 SỐNG) — sai đơn vị; (b) "rộng hơn r367 một trường" sai: receipt pr510 lượt 2 đã ghi verdict_bytes, tập trường mới = 0; (c) 340/340, comm 0/0, r369=0 đặt dưới nhãn ĐO — không tái đo được từ gói; (d) README/hàng mục lục thuật sự kiện GitHub và "chạy trọn ngay lần đầu" không mang nhãn (b)/attestation. 1 P3: README 638→647 khai sai, đúng là 637→646. | Đối chiếu nội dung V1 và bảng kỹ thuật phía trên. Các băm/Git/cổng tái chạy được ghi riêng; phép chạy/remote/runtime #511 ở sandbox lịch sử là nguồn(c), không chứng thực lại toàn bộ từ lời kể. | KHỚP nguồn theo phạm vi; phần không tái đo = KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-1-codex-verdict.receipt.yaml:40 mục5: Quét mọi refs/remotes/origin trong gói: 342 ref; tiêu đề r368 ở 2 ref (land-493-bookkeeping, -wip), r369 ở 1 ref (nhánh PR); literal r368/r369 3/1 ref. `origin` là URL GitHub, không mạng ⇒ ls-remote KHÔNG ĐO ĐƯỢC. | Đối chiếu nội dung V1 và bảng kỹ thuật phía trên. Các băm/Git/cổng tái chạy được ghi riêng; phép chạy/remote/runtime #511 ở sandbox lịch sử là nguồn(c), không chứng thực lại toàn bộ từ lời kể. | KHỚP nguồn theo phạm vi; phần không tái đo = KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-1-codex-verdict.receipt.yaml.github_submitter_identity.actor=ducthangho | GitHub/session/sổủyquyền không có nguồn độc lập được cấp. Các lời khai GH là(b); riêng R5 không mâu thuẫn với caveat, như bảng trên. | KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-1-codex-verdict.receipt.yaml.github_submitter_identity.la_tac_gia_PR=True | GitHub/session/sổủyquyền không có nguồn độc lập được cấp. Các lời khai GH là(b); riêng R5 không mâu thuẫn với caveat, như bảng trên. | KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-1-codex-verdict.receipt.yaml.github_submitter_identity.ghi_chu=`ADR-0040`: verdict do tài khoản tác giả PR vận chuyển KHÔNG là merge authorization; lượt này không phải lượt cuối — không có gì để uỷ quyền. | GitHub/session/sổủyquyền không có nguồn độc lập được cấp. Các lời khai GH là(b); riêng R5 không mâu thuẫn với caveat, như bảng trên. | KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-1-codex-verdict.receipt.yaml.github_submitter_identity.phien_van_chuyen=https://claude.ai/code/session_01Lnos1VZ4KSzHLG9u4UETiW | GitHub/session/sổủyquyền không có nguồn độc lập được cấp. Các lời khai GH là(b); riêng R5 không mâu thuẫn với caveat, như bảng trên. | KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-1-codex-verdict.receipt.yaml.codex_connector_cung_head.kich_luc=KHÔNG — connector chỉ kích khi bỏ draft (19:39Z trên a41fc69); không chạy lại trên head này | Đối chiếu cùng lời kể trong EVIDENCE/CHANGELOG/caveat; không có reviewobject/threads/CIlive để đo sự kiện, timestamp, sốfindinghay trạngthái resolve. | KHÔNG ĐO ĐƯỢC (b) |
| ops/reviews/pr516-review-1-codex-verdict.receipt.yaml.codex_connector_cung_head.hoan_tat_luc=KHONG_AP_DUNG | Đối chiếu cùng lời kể trong EVIDENCE/CHANGELOG/caveat; không có reviewobject/threads/CIlive để đo sự kiện, timestamp, sốfindinghay trạngthái resolve. | KHÔNG ĐO ĐƯỢC (b) |
| ops/reviews/pr516-review-1-codex-verdict.receipt.yaml.codex_connector_cung_head.ket_qua=Không có review object của connector trên head này. | Đối chiếu cùng lời kể trong EVIDENCE/CHANGELOG/caveat; không có reviewobject/threads/CIlive để đo sự kiện, timestamp, sốfindinghay trạngthái resolve. | KHÔNG ĐO ĐƯỢC (b) |
| ops/reviews/pr516-review-1-codex-verdict.receipt.yaml:79: {"duong_dan": "KHONG_CO", "ghi_chu": "scratch/ trong sandbox ngoài kho (audit/ledger/mutant/land/hint_replay và log từng cổng)."} | Danh sách ops/reviews không chứa scratch artifact; run.json xác nhận snapshot head/worktree_sach. Không chứng minh toàn bộ lịch sử đọc/ghi/commitngoàihead hoặc thực thi lại từ mô tả. Các phủ định giữ phạm vi như đã phân tích. | KHỚP phần có hiện vật; lịch sử ngoài gói KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-1-codex-verdict.receipt.yaml:83: {"cay_kho_sach": true, "commit_them_ngoai_head": 0, "bang_chung": "run.json worktree_sach: true; reviewer tự đo cuối lượt: HEAD 899f305, git status sạch; chỉ ghi vào scratch/."} | Danh sách ops/reviews không chứa scratch artifact; run.json xác nhận snapshot head/worktree_sach. Không chứng minh toàn bộ lịch sử đọc/ghi/commitngoàihead hoặc thực thi lại từ mô tả. Các phủ định giữ phạm vi như đã phân tích. | KHỚP phần có hiện vật; lịch sử ngoài gói KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-1-codex-verdict.receipt.yaml:114: ["Model build và danh tính model thật của codex exec: không có modelUsage, chỉ có lời tự khai.", "run.json/stdout.log/stderr.log/prompt.snapshot không vào kho ⇒ scalar runtime là attestation.", "Sự kiện GitHub lúc reviewer đọc: sandbox không mạng."] | Danh sách ops/reviews không chứa scratch artifact; run.json xác nhận snapshot head/worktree_sach. Không chứng minh toàn bộ lịch sử đọc/ghi/commitngoàihead hoặc thực thi lại từ mô tả. Các phủ định giữ phạm vi như đã phân tích. | KHỚP phần có hiện vật; lịch sử ngoài gói KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-1-codex-verdict.receipt.yaml:129: ["Không khai model đã chạy — codex không đo được.", "Không khai đây là trạng thái cuối của #516 — head đã merge là c98c33e (lượt 4–5).", "Không khai reviewer chạy lại mọi phép đo của các lượt trước — mỗi lượt đo phần delta được giao."] | Danh sách ops/reviews không chứa scratch artifact; run.json xác nhận snapshot head/worktree_sach. Không chứng minh toàn bộ lịch sử đọc/ghi/commitngoàihead hoặc thực thi lại từ mô tả. Các phủ định giữ phạm vi như đã phân tích. | KHỚP phần có hiện vật; lịch sử ngoài gói KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-2-codex-verdict.receipt.yaml:4 schema_version=2 | YAML parse được; schema v2 kiểm đạt ở HEAD; đây là trường phân loại hồ sơ. | KHỚP lược đồ |
| ops/reviews/pr516-review-2-codex-verdict.receipt.yaml:5 receipt_id=pr516-review-2-codex-20260911-457a6568 | ID gắn PR516/lượt2/ngày20260911/short_id457a6568,không có va chạm trong5receipt. | KHỚP đối chiếu cấu tạo |
| ops/reviews/pr516-review-2-codex-verdict.receipt.yaml:6 kind=review_delivery_receipt | YAML parse được; schema v2 kiểm đạt ở HEAD; đây là trường phân loại hồ sơ. | KHỚP lược đồ |
| ops/reviews/pr516-review-2-codex-verdict.receipt.yaml:7 packet_id=PR516-BOOKKEEPING-511 | Metadata do tác giả gán (PRhồsơ/khônglease/role/phiênviết); prompt/commit mô tả cùng vai trò. Không có chứngthực độc lập cho nghĩa ngoàiYAML. | KHAI BÁO; không nâng thành đo |
| ops/reviews/pr516-review-2-codex-verdict.receipt.yaml:8 lease_id=khong-co-lease | Metadata do tác giả gán (PRhồsơ/khônglease/role/phiênviết); prompt/commit mô tả cùng vai trò. Không có chứngthực độc lập cho nghĩa ngoàiYAML. | KHAI BÁO; không nâng thành đo |
| ops/reviews/pr516-review-2-codex-verdict.receipt.yaml:9 phase_key=HO-SO-CROSS-REVIEW-PHIEN-20260911 | Metadata do tác giả gán (PRhồsơ/khônglease/role/phiênviết); prompt/commit mô tả cùng vai trò. Không có chứngthực độc lập cho nghĩa ngoàiYAML. | KHAI BÁO; không nâng thành đo |
| ops/reviews/pr516-review-2-codex-verdict.receipt.yaml:11 role=reviewer | Metadata do tác giả gán (PRhồsơ/khônglease/role/phiênviết); prompt/commit mô tả cùng vai trò. Không có chứngthực độc lập cho nghĩa ngoàiYAML. | KHAI BÁO; không nâng thành đo |
| ops/reviews/pr516-review-2-codex-verdict.receipt.yaml:12 provider=codex | Reviewer tự khai Codex; tác giả commit tự khai Claude. Headerlog phù hợp; không chứng thực danh tính thực/khác backend. | KHỚP tự khai; backend KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-2-codex-verdict.receipt.yaml:13 executor_provider=claude | Reviewer tự khai Codex; tác giả commit tự khai Claude. Headerlog phù hợp; không chứng thực danh tính thực/khác backend. | KHỚP tự khai; backend KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-2-codex-verdict.receipt.yaml:14 cross_provider=True | Reviewer tự khai Codex; tác giả commit tự khai Claude. Headerlog phù hợp; không chứng thực danh tính thực/khác backend. | KHỚP tự khai; backend KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-2-codex-verdict.receipt.yaml:124 delivered=True | verdict và receipt có thật ở HEAD,blobneo đúng; không suy đã giao lên comment từ delivered. | KHỚP hiện vật repo |
| ops/reviews/pr516-review-2-codex-verdict.receipt.yaml:125 delivered_by=claude-session | Metadata do tác giả gán (PRhồsơ/khônglease/role/phiênviết); prompt/commit mô tả cùng vai trò. Không có chứngthực độc lập cho nghĩa ngoàiYAML. | KHAI BÁO; không nâng thành đo |
| ops/reviews/pr516-review-2-codex-verdict.receipt.yaml:126 authoritative_source=repo_file | verdict và receipt có thật ở HEAD,blobneo đúng; không suy đã giao lên comment từ delivered. | KHỚP hiện vật repo |
| ops/reviews/pr516-review-2-codex-verdict.receipt.yaml:127 receipt_written_by=claude-session | Metadata do tác giả gán (PRhồsơ/khônglease/role/phiênviết); prompt/commit mô tả cùng vai trò. Không có chứngthực độc lập cho nghĩa ngoàiYAML. | KHAI BÁO; không nâng thành đo |
| ops/reviews/pr516-review-2-codex-verdict.receipt.yaml:128 receipt_written_at_utc=2026-09-11T21:06:00Z | Timestamp21:06:00Z có thật trongYAML; commitchứareceipt896bfbf21:08:50Z nên thứtự có thể phùhợp, không đo thờiđiểmghi thực tế. | KHÔNG ĐO ĐƯỢC thời điểm viết |
| ops/reviews/pr516-review-2-codex-verdict.receipt.yaml:35 mục1: Áp lại HINT lượt 1 (`patch --batch --fuzz=0 --verbose -p0`) lên 899f305 trong clone cục bộ: 8/8 hunk succeeded không fuzz/offset; 4 tệp `cmp` bằng byte a4c14c7; `git diff 899f305..a4c14c7 --numstat` đúng 4 tệp HINT + manifest; manifest tái sinh (`python3 -B scripts/tl.py release-manifest --deterministic --out`) bằng byte 30 335 B / b86df2af…. | Đối chiếu nội dung V2 và bảng kỹ thuật phía trên. Các băm/Git/cổng tái chạy được ghi riêng; phép chạy/remote/runtime #511 ở sandbox lịch sử là nguồn(c), không chứng thực lại toàn bộ từ lời kể. | KHỚP nguồn theo phạm vi; phần không tái đo = KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-2-codex-verdict.receipt.yaml:35 mục2: 5 finding lượt 1 ĐÃ VÁ THẬT — bảng ĐỐI CHIẾU LƯỢT TRƯỚC với bằng chứng tự đo từng slug (đếm 5 dòng bảng mutant nguồn #511 lượt 1:358–362; receipt pr510 lượt 2:119–122 tại 05ba3f9 đã có verdict_bytes; CHANGELOG:10–18 nhãn thuật lại/KHÔNG ĐO ĐƯỢC; README:15 nhãn (a)/(b)/(c); LF blob 05ba3f9 và 6786637 đều 637, HEAD 646). | Đối chiếu nội dung V2 và bảng kỹ thuật phía trên. Các băm/Git/cổng tái chạy được ghi riêng; phép chạy/remote/runtime #511 ở sandbox lịch sử là nguồn(c), không chứng thực lại toàn bộ từ lời kể. | KHỚP nguồn theo phạm vi; phần không tái đo = KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-2-codex-verdict.receipt.yaml:35 mục3: HEAD qua 4 cổng: v2 83 ĐẠT / 0 vi phạm / tổng 136; t26/t27 QUA; release strict 180/180. 5 mutant cổng lặp lại kết quả lượt 1 (M1/M2/M4 GIẾT, M3/M5 SỐNG 4/4). 3 lối land lên 6786637 (commit-tree): merge/ff giữ neo, squash ⇒ 81 ĐẠT / 2 vi phạm. | Đối chiếu nội dung V2 và bảng kỹ thuật phía trên. Các băm/Git/cổng tái chạy được ghi riêng; phép chạy/remote/runtime #511 ở sandbox lịch sử là nguồn(c), không chứng thực lại toàn bộ từ lời kể. | KHỚP nguồn theo phạm vi; phần không tái đo = KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-2-codex-verdict.receipt.yaml:35 mục4: Reviewer tự khai LỖI PHẠM VI ĐỌC: lệnh trích `_TRANSPORT_CONTRACTS` dùng sai dấu kết thúc nên đã xuất cả phần sau bảng trong .claude/dev/launcher.py; không dùng phần ấy làm căn cứ, không tự khai đã giữ trọn rào chắn đọc. | Đối chiếu nội dung V2 và bảng kỹ thuật phía trên. Các băm/Git/cổng tái chạy được ghi riêng; phép chạy/remote/runtime #511 ở sandbox lịch sử là nguồn(c), không chứng thực lại toàn bộ từ lời kể. | KHỚP nguồn theo phạm vi; phần không tái đo = KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-2-codex-verdict.receipt.yaml.github_submitter_identity.actor=ducthangho | GitHub/session/sổủyquyền không có nguồn độc lập được cấp. Các lời khai GH là(b); riêng R5 không mâu thuẫn với caveat, như bảng trên. | KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-2-codex-verdict.receipt.yaml.github_submitter_identity.la_tac_gia_PR=True | GitHub/session/sổủyquyền không có nguồn độc lập được cấp. Các lời khai GH là(b); riêng R5 không mâu thuẫn với caveat, như bảng trên. | KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-2-codex-verdict.receipt.yaml.github_submitter_identity.ghi_chu=`ADR-0040`: verdict do tài khoản tác giả PR vận chuyển KHÔNG là merge authorization; lượt này không phải lượt cuối — không có gì để uỷ quyền. | GitHub/session/sổủyquyền không có nguồn độc lập được cấp. Các lời khai GH là(b); riêng R5 không mâu thuẫn với caveat, như bảng trên. | KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-2-codex-verdict.receipt.yaml.github_submitter_identity.phien_van_chuyen=https://claude.ai/code/session_01Lnos1VZ4KSzHLG9u4UETiW | GitHub/session/sổủyquyền không có nguồn độc lập được cấp. Các lời khai GH là(b); riêng R5 không mâu thuẫn với caveat, như bảng trên. | KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-2-codex-verdict.receipt.yaml.codex_connector_cung_head.kich_luc=2026-09-11T19:39:43Z — bỏ draft trên a41fc69; Completed 19:52:04Z | Đối chiếu cùng lời kể trong EVIDENCE/CHANGELOG/caveat; không có reviewobject/threads/CIlive để đo sự kiện, timestamp, sốfindinghay trạngthái resolve. | KHÔNG ĐO ĐƯỢC (b) |
| ops/reviews/pr516-review-2-codex-verdict.receipt.yaml.codex_connector_cung_head.hoan_tat_luc=2026-09-11T19:52:04Z | Đối chiếu cùng lời kể trong EVIDENCE/CHANGELOG/caveat; không có reviewobject/threads/CIlive để đo sự kiện, timestamp, sốfindinghay trạngthái resolve. | KHÔNG ĐO ĐƯỢC (b) |
| ops/reviews/pr516-review-2-codex-verdict.receipt.yaml.codex_connector_cung_head.ket_qua=2 P1 — thread discussion_r3992864226 (assurance receipt pr511 lượt 2 ghi cross_approved dù thiếu mục ĐỐI CHIẾU LƯỢT TRƯỚC: ĐÚNG, vá ở 5f45e6e) và thread discussion_r3992864232 (re-anchor về 6fe742e: KHÔNG ÁP DỤNG, commit không tồn tại); cả hai thread đã reply + resolve. Id review object của connector trên #516 không được ghi lại. | Đối chiếu cùng lời kể trong EVIDENCE/CHANGELOG/caveat; không có reviewobject/threads/CIlive để đo sự kiện, timestamp, sốfindinghay trạngthái resolve. | KHÔNG ĐO ĐƯỢC (b) |
| ops/reviews/pr516-review-2-codex-verdict.receipt.yaml:73: {"duong_dan": "KHONG_CO", "ghi_chu": "scratch/ trong sandbox ngoài kho (audit/ledger/mutant/land/hint_replay và log từng cổng)."} | Danh sách ops/reviews không chứa scratch artifact; run.json xác nhận snapshot head/worktree_sach. Không chứng minh toàn bộ lịch sử đọc/ghi/commitngoàihead hoặc thực thi lại từ mô tả. Các phủ định giữ phạm vi như đã phân tích. | KHỚP phần có hiện vật; lịch sử ngoài gói KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-2-codex-verdict.receipt.yaml:77: {"cay_kho_sach": true, "commit_them_ngoai_head": 0, "bang_chung": "run.json worktree_sach: true; reviewer tự đo cuối lượt: HEAD a41fc69, git status sạch; chỉ ghi vào scratch/."} | Danh sách ops/reviews không chứa scratch artifact; run.json xác nhận snapshot head/worktree_sach. Không chứng minh toàn bộ lịch sử đọc/ghi/commitngoàihead hoặc thực thi lại từ mô tả. Các phủ định giữ phạm vi như đã phân tích. | KHỚP phần có hiện vật; lịch sử ngoài gói KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-2-codex-verdict.receipt.yaml:114: ["Model build và danh tính model thật của codex exec: không có modelUsage, chỉ có lời tự khai.", "run.json/stdout.log/stderr.log/prompt.snapshot không vào kho ⇒ scalar runtime là attestation.", "Sự kiện GitHub lúc reviewer đọc: sandbox không mạng."] | Danh sách ops/reviews không chứa scratch artifact; run.json xác nhận snapshot head/worktree_sach. Không chứng minh toàn bộ lịch sử đọc/ghi/commitngoàihead hoặc thực thi lại từ mô tả. Các phủ định giữ phạm vi như đã phân tích. | KHỚP phần có hiện vật; lịch sử ngoài gói KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-2-codex-verdict.receipt.yaml:129: ["Không khai model đã chạy — codex không đo được.", "Không khai đây là trạng thái cuối của #516 — head đã merge là c98c33e (lượt 4–5).", "Không khai reviewer chạy lại mọi phép đo của các lượt trước — mỗi lượt đo phần delta được giao."] | Danh sách ops/reviews không chứa scratch artifact; run.json xác nhận snapshot head/worktree_sach. Không chứng minh toàn bộ lịch sử đọc/ghi/commitngoàihead hoặc thực thi lại từ mô tả. Các phủ định giữ phạm vi như đã phân tích. | KHỚP phần có hiện vật; lịch sử ngoài gói KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-3-codex-verdict.receipt.yaml:4 schema_version=2 | YAML parse được; schema v2 kiểm đạt ở HEAD; đây là trường phân loại hồ sơ. | KHỚP lược đồ |
| ops/reviews/pr516-review-3-codex-verdict.receipt.yaml:5 receipt_id=pr516-review-3-codex-20260911-0449ddb0 | ID gắn PR516/lượt3/ngày20260911/short_id0449ddb0,không có va chạm trong5receipt. | KHỚP đối chiếu cấu tạo |
| ops/reviews/pr516-review-3-codex-verdict.receipt.yaml:6 kind=review_delivery_receipt | YAML parse được; schema v2 kiểm đạt ở HEAD; đây là trường phân loại hồ sơ. | KHỚP lược đồ |
| ops/reviews/pr516-review-3-codex-verdict.receipt.yaml:7 packet_id=PR516-BOOKKEEPING-511 | Metadata do tác giả gán (PRhồsơ/khônglease/role/phiênviết); prompt/commit mô tả cùng vai trò. Không có chứngthực độc lập cho nghĩa ngoàiYAML. | KHAI BÁO; không nâng thành đo |
| ops/reviews/pr516-review-3-codex-verdict.receipt.yaml:8 lease_id=khong-co-lease | Metadata do tác giả gán (PRhồsơ/khônglease/role/phiênviết); prompt/commit mô tả cùng vai trò. Không có chứngthực độc lập cho nghĩa ngoàiYAML. | KHAI BÁO; không nâng thành đo |
| ops/reviews/pr516-review-3-codex-verdict.receipt.yaml:9 phase_key=HO-SO-CROSS-REVIEW-PHIEN-20260911 | Metadata do tác giả gán (PRhồsơ/khônglease/role/phiênviết); prompt/commit mô tả cùng vai trò. Không có chứngthực độc lập cho nghĩa ngoàiYAML. | KHAI BÁO; không nâng thành đo |
| ops/reviews/pr516-review-3-codex-verdict.receipt.yaml:11 role=reviewer | Metadata do tác giả gán (PRhồsơ/khônglease/role/phiênviết); prompt/commit mô tả cùng vai trò. Không có chứngthực độc lập cho nghĩa ngoàiYAML. | KHAI BÁO; không nâng thành đo |
| ops/reviews/pr516-review-3-codex-verdict.receipt.yaml:12 provider=codex | Reviewer tự khai Codex; tác giả commit tự khai Claude. Headerlog phù hợp; không chứng thực danh tính thực/khác backend. | KHỚP tự khai; backend KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-3-codex-verdict.receipt.yaml:13 executor_provider=claude | Reviewer tự khai Codex; tác giả commit tự khai Claude. Headerlog phù hợp; không chứng thực danh tính thực/khác backend. | KHỚP tự khai; backend KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-3-codex-verdict.receipt.yaml:14 cross_provider=True | Reviewer tự khai Codex; tác giả commit tự khai Claude. Headerlog phù hợp; không chứng thực danh tính thực/khác backend. | KHỚP tự khai; backend KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-3-codex-verdict.receipt.yaml:124 delivered=True | verdict và receipt có thật ở HEAD,blobneo đúng; không suy đã giao lên comment từ delivered. | KHỚP hiện vật repo |
| ops/reviews/pr516-review-3-codex-verdict.receipt.yaml:125 delivered_by=claude-session | Metadata do tác giả gán (PRhồsơ/khônglease/role/phiênviết); prompt/commit mô tả cùng vai trò. Không có chứngthực độc lập cho nghĩa ngoàiYAML. | KHAI BÁO; không nâng thành đo |
| ops/reviews/pr516-review-3-codex-verdict.receipt.yaml:126 authoritative_source=repo_file | verdict và receipt có thật ở HEAD,blobneo đúng; không suy đã giao lên comment từ delivered. | KHỚP hiện vật repo |
| ops/reviews/pr516-review-3-codex-verdict.receipt.yaml:127 receipt_written_by=claude-session | Metadata do tác giả gán (PRhồsơ/khônglease/role/phiênviết); prompt/commit mô tả cùng vai trò. Không có chứngthực độc lập cho nghĩa ngoàiYAML. | KHAI BÁO; không nâng thành đo |
| ops/reviews/pr516-review-3-codex-verdict.receipt.yaml:128 receipt_written_at_utc=2026-09-11T21:06:00Z | Timestamp21:06:00Z có thật trongYAML; commitchứareceipt896bfbf21:08:50Z nên thứtự có thể phùhợp, không đo thờiđiểmghi thực tế. | KHÔNG ĐO ĐƯỢC thời điểm viết |
| ops/reviews/pr516-review-3-codex-verdict.receipt.yaml:35 mục1: Connector P1 "assurance" — ĐÃ VÁ THẬT: verdict pr511 lượt 2 thiếu mục ĐỐI CHIẾU LƯỢT TRƯỚC và cả bốn cụm canonical (grep); receipt2:20 đã hạ cross_approved → cross_reviewed; caveat/README/CHANGELOG nói rõ giới hạn; mức hạ đúng cho một review đã thực hiện nhưng chưa đáp ứng hợp đồng tái-review. Reviewer chỉ đọc đoạn PROTOCOL_DA_PHIEN 548–578 sau grep được phép. | Đối chiếu nội dung V3 và bảng kỹ thuật phía trên. Các băm/Git/cổng tái chạy được ghi riêng; phép chạy/remote/runtime #511 ở sandbox lịch sử là nguồn(c), không chứng thực lại toàn bộ từ lời kể. | KHỚP nguồn theo phạm vi; phần không tái đo = KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-3-codex-verdict.receipt.yaml:35 mục2: Connector P1 "re-anchor" — KHÔNG ÁP DỤNG: `git cat-file -t 6fe742e` rc=128 (object không có trong clone); `merge-base --is-ancestor 120d47a HEAD` rc=0; hai blob tại URL neo khớp byte verdict và băm receipt; v2 83 ĐẠT / 0 vi phạm. Reviewer KHÔNG suy từ việc thiếu object rằng đã chứng minh nguồn gốc "squash tổng hợp của connector". | Đối chiếu nội dung V3 và bảng kỹ thuật phía trên. Các băm/Git/cổng tái chạy được ghi riêng; phép chạy/remote/runtime #511 ở sandbox lịch sử là nguồn(c), không chứng thực lại toàn bộ từ lời kể. | KHỚP nguồn theo phạm vi; phần không tái đo = KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-3-codex-verdict.receipt.yaml:35 mục3: Mutant M1 (đảo assurance receipt pr511 lượt 2 về cross_approved) SỐNG qua v2/t26/t27/release (4/4) — cổng không kiểm cấu trúc/phân loại tái-review; kết quả xanh KHÔNG được dùng để chứng minh cross_approved là đúng. | Đối chiếu nội dung V3 và bảng kỹ thuật phía trên. Các băm/Git/cổng tái chạy được ghi riêng; phép chạy/remote/runtime #511 ở sandbox lịch sử là nguồn(c), không chứng thực lại toàn bộ từ lời kể. | KHỚP nguồn theo phạm vi; phần không tái đo = KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-3-codex-verdict.receipt.yaml:35 mục4: Kết luận approve là về hồ sơ hiện tại, không hồi tố biến verdict pr511 lượt 2 thành đúng cấu trúc, không đóng nợ validator hay nợ hồ sơ pr510. | Đối chiếu nội dung V3 và bảng kỹ thuật phía trên. Các băm/Git/cổng tái chạy được ghi riêng; phép chạy/remote/runtime #511 ở sandbox lịch sử là nguồn(c), không chứng thực lại toàn bộ từ lời kể. | KHỚP nguồn theo phạm vi; phần không tái đo = KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-3-codex-verdict.receipt.yaml.github_submitter_identity.actor=ducthangho | GitHub/session/sổủyquyền không có nguồn độc lập được cấp. Các lời khai GH là(b); riêng R5 không mâu thuẫn với caveat, như bảng trên. | KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-3-codex-verdict.receipt.yaml.github_submitter_identity.la_tac_gia_PR=True | GitHub/session/sổủyquyền không có nguồn độc lập được cấp. Các lời khai GH là(b); riêng R5 không mâu thuẫn với caveat, như bảng trên. | KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-3-codex-verdict.receipt.yaml.github_submitter_identity.ghi_chu=`ADR-0040`: verdict do tài khoản tác giả PR vận chuyển KHÔNG là merge authorization; lượt này không phải lượt cuối — không có gì để uỷ quyền. | GitHub/session/sổủyquyền không có nguồn độc lập được cấp. Các lời khai GH là(b); riêng R5 không mâu thuẫn với caveat, như bảng trên. | KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-3-codex-verdict.receipt.yaml.github_submitter_identity.phien_van_chuyen=https://claude.ai/code/session_01Lnos1VZ4KSzHLG9u4UETiW | GitHub/session/sổủyquyền không có nguồn độc lập được cấp. Các lời khai GH là(b); riêng R5 không mâu thuẫn với caveat, như bảng trên. | KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-3-codex-verdict.receipt.yaml.codex_connector_cung_head.kich_luc=KHÔNG — connector chỉ kích khi bỏ draft (19:39Z trên a41fc69); không chạy lại trên head này | Đối chiếu cùng lời kể trong EVIDENCE/CHANGELOG/caveat; không có reviewobject/threads/CIlive để đo sự kiện, timestamp, sốfindinghay trạngthái resolve. | KHÔNG ĐO ĐƯỢC (b) |
| ops/reviews/pr516-review-3-codex-verdict.receipt.yaml.codex_connector_cung_head.hoan_tat_luc=KHONG_AP_DUNG | Đối chiếu cùng lời kể trong EVIDENCE/CHANGELOG/caveat; không có reviewobject/threads/CIlive để đo sự kiện, timestamp, sốfindinghay trạngthái resolve. | KHÔNG ĐO ĐƯỢC (b) |
| ops/reviews/pr516-review-3-codex-verdict.receipt.yaml.codex_connector_cung_head.ket_qua=Không có review object của connector trên head này. | Đối chiếu cùng lời kể trong EVIDENCE/CHANGELOG/caveat; không có reviewobject/threads/CIlive để đo sự kiện, timestamp, sốfindinghay trạngthái resolve. | KHÔNG ĐO ĐƯỢC (b) |
| ops/reviews/pr516-review-3-codex-verdict.receipt.yaml:73: {"duong_dan": "KHONG_CO", "ghi_chu": "scratch/ trong sandbox ngoài kho (audit/ledger/mutant/land/hint_replay và log từng cổng)."} | Danh sách ops/reviews không chứa scratch artifact; run.json xác nhận snapshot head/worktree_sach. Không chứng minh toàn bộ lịch sử đọc/ghi/commitngoàihead hoặc thực thi lại từ mô tả. Các phủ định giữ phạm vi như đã phân tích. | KHỚP phần có hiện vật; lịch sử ngoài gói KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-3-codex-verdict.receipt.yaml:77: {"cay_kho_sach": true, "commit_them_ngoai_head": 0, "bang_chung": "run.json worktree_sach: true; reviewer tự đo cuối lượt: HEAD 5f45e6e, git status sạch; chỉ ghi vào scratch/."} | Danh sách ops/reviews không chứa scratch artifact; run.json xác nhận snapshot head/worktree_sach. Không chứng minh toàn bộ lịch sử đọc/ghi/commitngoàihead hoặc thực thi lại từ mô tả. Các phủ định giữ phạm vi như đã phân tích. | KHỚP phần có hiện vật; lịch sử ngoài gói KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-3-codex-verdict.receipt.yaml:114: ["Model build và danh tính model thật của codex exec: không có modelUsage, chỉ có lời tự khai.", "run.json/stdout.log/stderr.log/prompt.snapshot không vào kho ⇒ scalar runtime là attestation.", "Sự kiện GitHub lúc reviewer đọc: sandbox không mạng."] | Danh sách ops/reviews không chứa scratch artifact; run.json xác nhận snapshot head/worktree_sach. Không chứng minh toàn bộ lịch sử đọc/ghi/commitngoàihead hoặc thực thi lại từ mô tả. Các phủ định giữ phạm vi như đã phân tích. | KHỚP phần có hiện vật; lịch sử ngoài gói KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-3-codex-verdict.receipt.yaml:129: ["Không khai model đã chạy — codex không đo được.", "Không khai đây là trạng thái cuối của #516 — head đã merge là c98c33e (lượt 4–5).", "Không khai reviewer chạy lại mọi phép đo của các lượt trước — mỗi lượt đo phần delta được giao."] | Danh sách ops/reviews không chứa scratch artifact; run.json xác nhận snapshot head/worktree_sach. Không chứng minh toàn bộ lịch sử đọc/ghi/commitngoàihead hoặc thực thi lại từ mô tả. Các phủ định giữ phạm vi như đã phân tích. | KHỚP phần có hiện vật; lịch sử ngoài gói KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-4-codex-verdict.receipt.yaml:4 schema_version=2 | YAML parse được; schema v2 kiểm đạt ở HEAD; đây là trường phân loại hồ sơ. | KHỚP lược đồ |
| ops/reviews/pr516-review-4-codex-verdict.receipt.yaml:5 receipt_id=pr516-review-4-codex-20260911-04792ddf | ID gắn PR516/lượt4/ngày20260911/short_id04792ddf,không có va chạm trong5receipt. | KHỚP đối chiếu cấu tạo |
| ops/reviews/pr516-review-4-codex-verdict.receipt.yaml:6 kind=review_delivery_receipt | YAML parse được; schema v2 kiểm đạt ở HEAD; đây là trường phân loại hồ sơ. | KHỚP lược đồ |
| ops/reviews/pr516-review-4-codex-verdict.receipt.yaml:7 packet_id=PR516-BOOKKEEPING-511 | Metadata do tác giả gán (PRhồsơ/khônglease/role/phiênviết); prompt/commit mô tả cùng vai trò. Không có chứngthực độc lập cho nghĩa ngoàiYAML. | KHAI BÁO; không nâng thành đo |
| ops/reviews/pr516-review-4-codex-verdict.receipt.yaml:8 lease_id=khong-co-lease | Metadata do tác giả gán (PRhồsơ/khônglease/role/phiênviết); prompt/commit mô tả cùng vai trò. Không có chứngthực độc lập cho nghĩa ngoàiYAML. | KHAI BÁO; không nâng thành đo |
| ops/reviews/pr516-review-4-codex-verdict.receipt.yaml:9 phase_key=HO-SO-CROSS-REVIEW-PHIEN-20260911 | Metadata do tác giả gán (PRhồsơ/khônglease/role/phiênviết); prompt/commit mô tả cùng vai trò. Không có chứngthực độc lập cho nghĩa ngoàiYAML. | KHAI BÁO; không nâng thành đo |
| ops/reviews/pr516-review-4-codex-verdict.receipt.yaml:11 role=reviewer | Metadata do tác giả gán (PRhồsơ/khônglease/role/phiênviết); prompt/commit mô tả cùng vai trò. Không có chứngthực độc lập cho nghĩa ngoàiYAML. | KHAI BÁO; không nâng thành đo |
| ops/reviews/pr516-review-4-codex-verdict.receipt.yaml:12 provider=codex | Reviewer tự khai Codex; tác giả commit tự khai Claude. Headerlog phù hợp; không chứng thực danh tính thực/khác backend. | KHỚP tự khai; backend KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-4-codex-verdict.receipt.yaml:13 executor_provider=claude | Reviewer tự khai Codex; tác giả commit tự khai Claude. Headerlog phù hợp; không chứng thực danh tính thực/khác backend. | KHỚP tự khai; backend KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-4-codex-verdict.receipt.yaml:14 cross_provider=True | Reviewer tự khai Codex; tác giả commit tự khai Claude. Headerlog phù hợp; không chứng thực danh tính thực/khác backend. | KHỚP tự khai; backend KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-4-codex-verdict.receipt.yaml:119 delivered=True | verdict và receipt có thật ở HEAD,blobneo đúng; không suy đã giao lên comment từ delivered. | KHỚP hiện vật repo |
| ops/reviews/pr516-review-4-codex-verdict.receipt.yaml:120 delivered_by=claude-session | Metadata do tác giả gán (PRhồsơ/khônglease/role/phiênviết); prompt/commit mô tả cùng vai trò. Không có chứngthực độc lập cho nghĩa ngoàiYAML. | KHAI BÁO; không nâng thành đo |
| ops/reviews/pr516-review-4-codex-verdict.receipt.yaml:121 authoritative_source=repo_file | verdict và receipt có thật ở HEAD,blobneo đúng; không suy đã giao lên comment từ delivered. | KHỚP hiện vật repo |
| ops/reviews/pr516-review-4-codex-verdict.receipt.yaml:122 receipt_written_by=claude-session | Metadata do tác giả gán (PRhồsơ/khônglease/role/phiênviết); prompt/commit mô tả cùng vai trò. Không có chứngthực độc lập cho nghĩa ngoàiYAML. | KHAI BÁO; không nâng thành đo |
| ops/reviews/pr516-review-4-codex-verdict.receipt.yaml:123 receipt_written_at_utc=2026-09-11T21:06:00Z | Timestamp21:06:00Z có thật trongYAML; commitchứareceipt896bfbf21:08:50Z nên thứtự có thể phùhợp, không đo thờiđiểmghi thực tế. | KHÔNG ĐO ĐƯỢC thời điểm viết |
| ops/reviews/pr516-review-4-codex-verdict.receipt.yaml:36 mục1: Cây Git sau giải xung đột với r368 (#514): 4/4 tệp pr511 bằng byte cha 1 (5f45e6e); 34/34 tệp pr493 bằng byte base (8802924); CHANGELOG = 110 dòng r369 + toàn bộ CHANGELOG@8802924 (bằng byte; r369 dòng 1, r368 dòng 111, r367 dòng 586); README bỏ 89 hàng pr493 = README@5f45e6e, bỏ 10 dòng pr511 = README@8802924; manifest tái sinh bằng byte (30 336 B / 0ff73960…); không còn marker xung đột. | Đối chiếu nội dung V4 và bảng kỹ thuật phía trên. Các băm/Git/cổng tái chạy được ghi riêng; phép chạy/remote/runtime #511 ở sandbox lịch sử là nguồn(c), không chứng thực lại toàn bộ từ lời kể. | KHỚP nguồn theo phạm vi; phần không tái đo = KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-4-codex-verdict.receipt.yaml:36 mục2: Cổng HEAD: v2 100 ĐẠT / 0 vi phạm / tổng 153; t26/t27 QUA; release strict 180/180; `git diff --check` sạch. 19 receipt / 2 neo (120d47a cho pr511, 98f931b cho 17 receipt pr493): 19/19 blob bằng byte verdict; merge/ff giữ cả 19 neo; squash ⇒ 2 receipt pr511 mất tổ tiên (98 ĐẠT / 2 vi phạm) — giới hạn đã ghi từ lượt 2. | Đối chiếu nội dung V4 và bảng kỹ thuật phía trên. Các băm/Git/cổng tái chạy được ghi riêng; phép chạy/remote/runtime #511 ở sandbox lịch sử là nguồn(c), không chứng thực lại toàn bộ từ lời kể. | KHỚP nguồn theo phạm vi; phần không tái đo = KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-4-codex-verdict.receipt.yaml:36 mục3: P2-E01 DUY NHẤT: EVIDENCE.md:9 của GÓI REVIEW (ngoài kho) khai "đoạn nguồn của #493 do master đưa vào ở chỗ khác" — đo: base lẫn HEAD KHÔNG có đoạn nguồn riêng nào cho #493, master chỉ thêm 72 + 17 hàng bảng. Cây đúng, lời khai sai; sửa bằng EVIDENCE.HINT.patch (1 hunk) ngoài kho. | Đối chiếu nội dung V4 và bảng kỹ thuật phía trên. Các băm/Git/cổng tái chạy được ghi riêng; phép chạy/remote/runtime #511 ở sandbox lịch sử là nguồn(c), không chứng thực lại toàn bộ từ lời kể. | KHỚP nguồn theo phạm vi; phần không tái đo = KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-4-codex-verdict.receipt.yaml:36 mục4: Mutant: xoá 1 hàng cảnh báo pr493 (README 736→735) ⇒ t27 ĐỎ rc=1 nêu đúng caveat/verdict — GIẾT. | Đối chiếu nội dung V4 và bảng kỹ thuật phía trên. Các băm/Git/cổng tái chạy được ghi riêng; phép chạy/remote/runtime #511 ở sandbox lịch sử là nguồn(c), không chứng thực lại toàn bộ từ lời kể. | KHỚP nguồn theo phạm vi; phần không tái đo = KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-4-codex-verdict.receipt.yaml.github_submitter_identity.actor=ducthangho | GitHub/session/sổủyquyền không có nguồn độc lập được cấp. Các lời khai GH là(b); riêng R5 không mâu thuẫn với caveat, như bảng trên. | KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-4-codex-verdict.receipt.yaml.github_submitter_identity.la_tac_gia_PR=True | GitHub/session/sổủyquyền không có nguồn độc lập được cấp. Các lời khai GH là(b); riêng R5 không mâu thuẫn với caveat, như bảng trên. | KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-4-codex-verdict.receipt.yaml.github_submitter_identity.ghi_chu=`ADR-0040`: verdict do tài khoản tác giả PR vận chuyển KHÔNG là merge authorization; lượt này không phải lượt cuối — không có gì để uỷ quyền. | GitHub/session/sổủyquyền không có nguồn độc lập được cấp. Các lời khai GH là(b); riêng R5 không mâu thuẫn với caveat, như bảng trên. | KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-4-codex-verdict.receipt.yaml.github_submitter_identity.phien_van_chuyen=https://claude.ai/code/session_01Lnos1VZ4KSzHLG9u4UETiW | GitHub/session/sổủyquyền không có nguồn độc lập được cấp. Các lời khai GH là(b); riêng R5 không mâu thuẫn với caveat, như bảng trên. | KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-4-codex-verdict.receipt.yaml.codex_connector_cung_head.kich_luc=KHÔNG — connector chỉ kích khi bỏ draft (19:39Z trên a41fc69); không chạy lại trên head này | Đối chiếu cùng lời kể trong EVIDENCE/CHANGELOG/caveat; không có reviewobject/threads/CIlive để đo sự kiện, timestamp, sốfindinghay trạngthái resolve. | KHÔNG ĐO ĐƯỢC (b) |
| ops/reviews/pr516-review-4-codex-verdict.receipt.yaml.codex_connector_cung_head.hoan_tat_luc=KHONG_AP_DUNG | Đối chiếu cùng lời kể trong EVIDENCE/CHANGELOG/caveat; không có reviewobject/threads/CIlive để đo sự kiện, timestamp, sốfindinghay trạngthái resolve. | KHÔNG ĐO ĐƯỢC (b) |
| ops/reviews/pr516-review-4-codex-verdict.receipt.yaml.codex_connector_cung_head.ket_qua=Không có review object của connector trên head này. | Đối chiếu cùng lời kể trong EVIDENCE/CHANGELOG/caveat; không có reviewobject/threads/CIlive để đo sự kiện, timestamp, sốfindinghay trạngthái resolve. | KHÔNG ĐO ĐƯỢC (b) |
| ops/reviews/pr516-review-4-codex-verdict.receipt.yaml:74: {"duong_dan": "KHONG_CO", "ghi_chu": "scratch/ trong sandbox ngoài kho (audit/ledger/mutant/land/hint_replay và log từng cổng)."} | Danh sách ops/reviews không chứa scratch artifact; run.json xác nhận snapshot head/worktree_sach. Không chứng minh toàn bộ lịch sử đọc/ghi/commitngoàihead hoặc thực thi lại từ mô tả. Các phủ định giữ phạm vi như đã phân tích. | KHỚP phần có hiện vật; lịch sử ngoài gói KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-4-codex-verdict.receipt.yaml:78: {"cay_kho_sach": true, "commit_them_ngoai_head": 0, "bang_chung": "run.json worktree_sach: true; reviewer tự đo cuối lượt: HEAD c98c33e, git status sạch; chỉ ghi vào scratch/."} | Danh sách ops/reviews không chứa scratch artifact; run.json xác nhận snapshot head/worktree_sach. Không chứng minh toàn bộ lịch sử đọc/ghi/commitngoàihead hoặc thực thi lại từ mô tả. Các phủ định giữ phạm vi như đã phân tích. | KHỚP phần có hiện vật; lịch sử ngoài gói KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-4-codex-verdict.receipt.yaml:109: ["Model build và danh tính model thật của codex exec: không có modelUsage, chỉ có lời tự khai.", "run.json/stdout.log/stderr.log/prompt.snapshot không vào kho ⇒ scalar runtime là attestation.", "Sự kiện GitHub lúc reviewer đọc: sandbox không mạng."] | Danh sách ops/reviews không chứa scratch artifact; run.json xác nhận snapshot head/worktree_sach. Không chứng minh toàn bộ lịch sử đọc/ghi/commitngoàihead hoặc thực thi lại từ mô tả. Các phủ định giữ phạm vi như đã phân tích. | KHỚP phần có hiện vật; lịch sử ngoài gói KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-4-codex-verdict.receipt.yaml:124: ["Không khai model đã chạy — codex không đo được.", "Không khai lượt 4 là lỗi của PR — P2 ở gói review.", "Không khai reviewer chạy lại mọi phép đo của các lượt trước — mỗi lượt đo phần delta được giao."] | Danh sách ops/reviews không chứa scratch artifact; run.json xác nhận snapshot head/worktree_sach. Không chứng minh toàn bộ lịch sử đọc/ghi/commitngoàihead hoặc thực thi lại từ mô tả. Các phủ định giữ phạm vi như đã phân tích. | KHỚP phần có hiện vật; lịch sử ngoài gói KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-5-codex-verdict.receipt.yaml:4 schema_version=2 | YAML parse được; schema v2 kiểm đạt ở HEAD; đây là trường phân loại hồ sơ. | KHỚP lược đồ |
| ops/reviews/pr516-review-5-codex-verdict.receipt.yaml:5 receipt_id=pr516-review-5-codex-20260911-6c8b0629 | ID gắn PR516/lượt5/ngày20260911/short_id6c8b0629,không có va chạm trong5receipt. | KHỚP đối chiếu cấu tạo |
| ops/reviews/pr516-review-5-codex-verdict.receipt.yaml:6 kind=review_delivery_receipt | YAML parse được; schema v2 kiểm đạt ở HEAD; đây là trường phân loại hồ sơ. | KHỚP lược đồ |
| ops/reviews/pr516-review-5-codex-verdict.receipt.yaml:7 packet_id=PR516-BOOKKEEPING-511 | Metadata do tác giả gán (PRhồsơ/khônglease/role/phiênviết); prompt/commit mô tả cùng vai trò. Không có chứngthực độc lập cho nghĩa ngoàiYAML. | KHAI BÁO; không nâng thành đo |
| ops/reviews/pr516-review-5-codex-verdict.receipt.yaml:8 lease_id=khong-co-lease | Metadata do tác giả gán (PRhồsơ/khônglease/role/phiênviết); prompt/commit mô tả cùng vai trò. Không có chứngthực độc lập cho nghĩa ngoàiYAML. | KHAI BÁO; không nâng thành đo |
| ops/reviews/pr516-review-5-codex-verdict.receipt.yaml:9 phase_key=HO-SO-CROSS-REVIEW-PHIEN-20260911 | Metadata do tác giả gán (PRhồsơ/khônglease/role/phiênviết); prompt/commit mô tả cùng vai trò. Không có chứngthực độc lập cho nghĩa ngoàiYAML. | KHAI BÁO; không nâng thành đo |
| ops/reviews/pr516-review-5-codex-verdict.receipt.yaml:11 role=reviewer | Metadata do tác giả gán (PRhồsơ/khônglease/role/phiênviết); prompt/commit mô tả cùng vai trò. Không có chứngthực độc lập cho nghĩa ngoàiYAML. | KHAI BÁO; không nâng thành đo |
| ops/reviews/pr516-review-5-codex-verdict.receipt.yaml:12 provider=codex | Reviewer tự khai Codex; tác giả commit tự khai Claude. Headerlog phù hợp; không chứng thực danh tính thực/khác backend. | KHỚP tự khai; backend KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-5-codex-verdict.receipt.yaml:13 executor_provider=claude | Reviewer tự khai Codex; tác giả commit tự khai Claude. Headerlog phù hợp; không chứng thực danh tính thực/khác backend. | KHỚP tự khai; backend KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-5-codex-verdict.receipt.yaml:14 cross_provider=True | Reviewer tự khai Codex; tác giả commit tự khai Claude. Headerlog phù hợp; không chứng thực danh tính thực/khác backend. | KHỚP tự khai; backend KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-5-codex-verdict.receipt.yaml:123 delivered=True | verdict và receipt có thật ở HEAD,blobneo đúng; không suy đã giao lên comment từ delivered. | KHỚP hiện vật repo |
| ops/reviews/pr516-review-5-codex-verdict.receipt.yaml:124 delivered_by=claude-session | Metadata do tác giả gán (PRhồsơ/khônglease/role/phiênviết); prompt/commit mô tả cùng vai trò. Không có chứngthực độc lập cho nghĩa ngoàiYAML. | KHAI BÁO; không nâng thành đo |
| ops/reviews/pr516-review-5-codex-verdict.receipt.yaml:125 authoritative_source=repo_file | verdict và receipt có thật ở HEAD,blobneo đúng; không suy đã giao lên comment từ delivered. | KHỚP hiện vật repo |
| ops/reviews/pr516-review-5-codex-verdict.receipt.yaml:126 receipt_written_by=claude-session | Metadata do tác giả gán (PRhồsơ/khônglease/role/phiênviết); prompt/commit mô tả cùng vai trò. Không có chứngthực độc lập cho nghĩa ngoàiYAML. | KHAI BÁO; không nâng thành đo |
| ops/reviews/pr516-review-5-codex-verdict.receipt.yaml:127 receipt_written_at_utc=2026-09-11T21:06:00Z | Timestamp21:06:00Z có thật trongYAML; commitchứareceipt896bfbf21:08:50Z nên thứtự có thể phùhợp, không đo thờiđiểmghi thực tế. | KHÔNG ĐO ĐƯỢC thời điểm viết |
| ops/reviews/pr516-review-5-codex-verdict.receipt.yaml:35 mục1: P2-E01 ĐÃ VÁ THẬT: EVIDENCE.md:9 nay chứa nguyên văn câu đề nghị của lượt 4, đúng 1 lần, bằng dòng `+` của EVIDENCE.HINT (sha256 7acb408c…, 1 hunk); mục `## Lượt 5` không có lời khai vượt đo. | Đối chiếu nội dung V5 và bảng kỹ thuật phía trên. Các băm/Git/cổng tái chạy được ghi riêng; phép chạy/remote/runtime #511 ở sandbox lịch sử là nguồn(c), không chứng thực lại toàn bộ từ lời kể. | KHỚP nguồn theo phạm vi; phần không tái đo = KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-5-codex-verdict.receipt.yaml:35 mục2: Cây như lượt 4: HEAD c98c33e / base 8802924; diff ba chấm 7 tệp +1313/−5; 7/7 băm khớp lượt 4 và bằng blob HEAD; diff pr511 so 5f45e6e và pr493 so 8802924 đều rỗng (4 + 34 tệp). | Đối chiếu nội dung V5 và bảng kỹ thuật phía trên. Các băm/Git/cổng tái chạy được ghi riêng; phép chạy/remote/runtime #511 ở sandbox lịch sử là nguồn(c), không chứng thực lại toàn bộ từ lời kể. | KHỚP nguồn theo phạm vi; phần không tái đo = KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-5-codex-verdict.receipt.yaml:35 mục3: Cổng HEAD: v2 100 ĐẠT / 0 vi phạm / tổng 153; t26/t27 PASS (importlib, python -B); release strict 180/180. Merge dựng lại / 3 lối land / mutant: KHÔNG đo lại — như lượt 4. | Đối chiếu nội dung V5 và bảng kỹ thuật phía trên. Các băm/Git/cổng tái chạy được ghi riêng; phép chạy/remote/runtime #511 ở sandbox lịch sử là nguồn(c), không chứng thực lại toàn bộ từ lời kể. | KHỚP nguồn theo phạm vi; phần không tái đo = KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-5-codex-verdict.receipt.yaml.github_submitter_identity.actor=ducthangho | GitHub/session/sổủyquyền không có nguồn độc lập được cấp. Các lời khai GH là(b); riêng R5 không mâu thuẫn với caveat, như bảng trên. | KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-5-codex-verdict.receipt.yaml.github_submitter_identity.la_tac_gia_PR=True | GitHub/session/sổủyquyền không có nguồn độc lập được cấp. Các lời khai GH là(b); riêng R5 không mâu thuẫn với caveat, như bảng trên. | KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-5-codex-verdict.receipt.yaml.github_submitter_identity.ghi_chu=`ADR-0040`: verdict do tài khoản tác giả PR vận chuyển KHÔNG là merge authorization; uỷ quyền merge là LUẬT CHUNG chủ kho ~14:4xZ, ghi ở PR #516 comment 5640499918; sổ local gen4 uy_quyen_merge.jsonl có dòng KHAI BÁO cho c98c33e. | GitHub/session/sổủyquyền không có nguồn độc lập được cấp. Các lời khai GH là(b); riêng R5 không mâu thuẫn với caveat, như bảng trên. | KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-5-codex-verdict.receipt.yaml.github_submitter_identity.phien_van_chuyen=https://claude.ai/code/session_01Lnos1VZ4KSzHLG9u4UETiW | GitHub/session/sổủyquyền không có nguồn độc lập được cấp. Các lời khai GH là(b); riêng R5 không mâu thuẫn với caveat, như bảng trên. | KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-5-codex-verdict.receipt.yaml.codex_connector_cung_head.kich_luc=KHÔNG — connector chỉ kích khi bỏ draft (19:39Z trên a41fc69); không chạy lại trên head này | Đối chiếu cùng lời kể trong EVIDENCE/CHANGELOG/caveat; không có reviewobject/threads/CIlive để đo sự kiện, timestamp, sốfindinghay trạngthái resolve. | KHÔNG ĐO ĐƯỢC (b) |
| ops/reviews/pr516-review-5-codex-verdict.receipt.yaml.codex_connector_cung_head.hoan_tat_luc=KHONG_AP_DUNG | Đối chiếu cùng lời kể trong EVIDENCE/CHANGELOG/caveat; không có reviewobject/threads/CIlive để đo sự kiện, timestamp, sốfindinghay trạngthái resolve. | KHÔNG ĐO ĐƯỢC (b) |
| ops/reviews/pr516-review-5-codex-verdict.receipt.yaml.codex_connector_cung_head.ket_qua=Không có review object của connector trên head này. | Đối chiếu cùng lời kể trong EVIDENCE/CHANGELOG/caveat; không có reviewobject/threads/CIlive để đo sự kiện, timestamp, sốfindinghay trạngthái resolve. | KHÔNG ĐO ĐƯỢC (b) |
| ops/reviews/pr516-review-5-codex-verdict.receipt.yaml:72: {"duong_dan": "KHONG_CO", "ghi_chu": "scratch/ trong sandbox ngoài kho (audit/ledger/mutant/land/hint_replay và log từng cổng)."} | Danh sách ops/reviews không chứa scratch artifact; run.json xác nhận snapshot head/worktree_sach. Không chứng minh toàn bộ lịch sử đọc/ghi/commitngoàihead hoặc thực thi lại từ mô tả. Các phủ định giữ phạm vi như đã phân tích. | KHỚP phần có hiện vật; lịch sử ngoài gói KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-5-codex-verdict.receipt.yaml:76: {"cay_kho_sach": true, "commit_them_ngoai_head": 0, "bang_chung": "run.json worktree_sach: true; reviewer tự đo cuối lượt: HEAD c98c33e, git status sạch; chỉ ghi vào scratch/."} | Danh sách ops/reviews không chứa scratch artifact; run.json xác nhận snapshot head/worktree_sach. Không chứng minh toàn bộ lịch sử đọc/ghi/commitngoàihead hoặc thực thi lại từ mô tả. Các phủ định giữ phạm vi như đã phân tích. | KHỚP phần có hiện vật; lịch sử ngoài gói KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-5-codex-verdict.receipt.yaml:113: ["Model build và danh tính model thật của codex exec: không có modelUsage, chỉ có lời tự khai.", "run.json/stdout.log/stderr.log/prompt.snapshot không vào kho ⇒ scalar runtime là attestation.", "Sự kiện GitHub lúc reviewer đọc: sandbox không mạng."] | Danh sách ops/reviews không chứa scratch artifact; run.json xác nhận snapshot head/worktree_sach. Không chứng minh toàn bộ lịch sử đọc/ghi/commitngoàihead hoặc thực thi lại từ mô tả. Các phủ định giữ phạm vi như đã phân tích. | KHỚP phần có hiện vật; lịch sử ngoài gói KHÔNG ĐO ĐƯỢC |
| ops/reviews/pr516-review-5-codex-verdict.receipt.yaml:128: ["Không khai model đã chạy — codex không đo được.", "Không khai lượt chạy kết thúc sạch — ma_thoat=1 (quota), xem caveat P1.", "Không khai reviewer chạy lại mọi phép đo của các lượt trước — mỗi lượt đo phần delta được giao."] | Danh sách ops/reviews không chứa scratch artifact; run.json xác nhận snapshot head/worktree_sach. Không chứng minh toàn bộ lịch sử đọc/ghi/commitngoàihead hoặc thực thi lại từ mô tả. Các phủ định giữ phạm vi như đã phân tích. | KHỚP phần có hiện vật; lịch sử ngoài gói KHÔNG ĐO ĐƯỢC |


### Nội dung 13 cảnh báo và 5 hàng mục lục

Cả 13 cặp verdict/id có đúng một hàng; nối `mo_ta` với `phai_lam_gi_khi_chay_lai`, bỏ bold và escape dấu `|`, được nội dung bằng hàng README ở cả 13 cặp. Đó là phép kiểm vận chuyển nội dung, chưa đủ để chứng minh nội dung đúng. Bảng lớp chỉ ra các lỗi được sao nguyên sang README.

| khai | đo | khớp? |
|---|---|---|
| R1:2caveat/README40–41 | Finding0/4/1, HINT8/4, băm1a123573…/74068B, khoảng25–279đúng; câu mutant mất chữĐỎ là lớp tậpđối tượng. Sự kiệncomment5639563938/bỏbảng/vượttrần là(b)khôngđođược. | KHỚP phầnđo; lỗiđãgomlớp |
| R2:3caveat/README37–39 | Head/approve0/0/0đúng; connector2P1 và comment5639724005 là(b). Mutant nguồn5→4,83049→83048 sống4/4 đúng V2; khoảng59–200/142đúng. | KHỚP nguồn/phạmvi |
| R3:3caveat/README34–36 | Head5f45e6e/approve0/0/0đúng; 7tệpkhôngđổiquamerge sai; lỗiđọc launcher thuộcV2; khoảng27–70/44,băm532e022c…/14796Bđúng; comment5640016566 và405là(b). | 2thểhiện nội dung đãgomlớp, không phải2finding mới |
| R4:2caveat/README32–33 | P2duynhấtEVIDENCE/khôngởPRđúng V4;19neo,4+34tệpđúng. khoảng35–95/61đúng; comment5640422345 và chú thíchbảnchiếu24–~100 không cócommentđểđo. | KHỚP nguồn/phầnlocal; comment KHÔNG ĐO ĐƯỢC |
| R5:3caveat/README29–31 | Rc1/stdout0/verdictđủ/assurancecross_reviewedđúng; probechưađođượclàlớpnguồn. Luậtchung/comment/CI/actor là(b); lượt5khôngchạylạimerge/land/mutantđúng V5:70,74–75. | KHỚP phầnđo; probeđãgomlớp |
| README:419 mục lụcR5 | Headc98c33e,260s,0/0/0,7577B,7/7cùngV4,t26/t27/v2100/release180 đúng nguồn;rc1/stdout0đúngrun. Merge20:56:47Z/luậtchung(b), retry0attestation đúngnhãn. | KHỚP theo nguồn |
| README:420 mục lụcR4 | 631s,0/1/0,16275B,4/4pr511/34/34pr493,19/19neo,2vi phạmsquashcũđúng; mutantxóahàngpr493 đượcV4ghi và không tựgán làphépchạymới. | KHỚP theo nguồn |
| README:421 mục lụcR3 | 462s,0/0/0,14796B,receiptpr511hạassurance,object6fe742evắngrc128,neo120d47a,v283/0đúng; mutantassurance4/4nguồnV3. (b)405/mergec98c33e đúngnhãn. | KHỚP theo nguồn |
| README:422 mục lụcR2 | 683s,0/0/0,36923B,5findingđóng,8/8hunk4tệp/manifestkhớpđãreplay;83/0/180nguồnđúng. TựkhailỗiđọclauncherởđâygánđúngV2; connector(b). | KHỚP theo nguồn |
| README:423 mục lụcR1 | 1089s,0/4/1,74068B,HINT8/4,5slugsđúng; retry0attestationđúng. Nhãn(a)trướckhốikếtquảsandboxcũ sailớpnguồn; sựkiệnápHINTlịch sử khôngchứngthựcthêm. | KHỚP con số; KHÔNG KHỚP nhãn |


## Findings theo lớp

### nguon-thuat-lai-bi-nang-thanh-do [P2]

**Hạng lớp:** P2. **Số thể hiện:** 10.

**Cơ chế chung:** Khi tổng hợp, nhãn nguồn không đi cùng mệnh đề: kết quả sandbox cũ bị gắn (a), lịch sử thao tác nằm dưới (a), số đối chiếu được lại bị phủ bằng (b); thông điệp lỗi và probe thuật lại được dùng để kết luận trạng thái quota. Cùng cơ chế làm độ mạnh của lời khai lệch khỏi nguồn, không có sai băm/neo hiện tại.

| Vị trí (HEAD gốc) | Khai | Đo |
|---|---|---|
| CHANGELOG.md:1 | probe 12-09 chạy được, trong tiêu đề không ghi nguồn | Không có log probe trong gói; EVIDENCE cũng xác nhận đây là (b). Chỉ đối chiếu được lời tác giả, không đo được rc=0 của probe. |
| CHANGELOG.md:4 | dừng bằng SỰ KIỆN: reviewer khác nền không còn quota | run 6c8b0629 chỉ chứng minh rc=1 và hai thông điệp lỗi ở cuối stderr vào 11-09; không đo khả dụng hiện tại. Chính mục Hệ quả thuật lại probe 12-09 chạy được. Câu cũ còn sót sau commit 3. |
| CHANGELOG.md:22 | Năm lượt — (b) trừ chỗ ghi (a); bảng 26–30 không có (a) | Bảng chứa Git/băm/byte/số finding trực tiếp đối chiếu được, runtime có run.json/log; không phải toàn bộ đều là sự kiện GitHub thuật lại. Các nhóm nguồn đã phân ở 16–20 nhưng nhãn bao bảng không giữ phân loại đó. |
| CHANGELOG.md:65 | probe 02:3xZ 12-09 rc=0 trình bày như kết quả; từ đó suy cửa sổ giới hạn | KHÔNG ĐO ĐƯỢC probe/thời lượng quota từ gói. Câu cuối nói thông điệp lỗi là (b) chưa gắn nguồn cho chính probe. HINT giữ lời thuật lại, không bác rc lịch sử. |
| CHANGELOG.md:77 | Phạm vi — (a), bao cả amend trước push và thứ tự chạy cổng trước/sau commit | Git chứng minh nội dung 3 commit, không chứng minh chưa từng push/tham chiếu neo, thao tác amend đã xảy ra hay lúc tác giả chạy từng cổng. Giá trị gate hiện tại tái chạy khớp, lịch sử thao tác vẫn KHÔNG ĐO ĐƯỢC. |
| CHANGELOG.md:101 | giới hạn ấy hoá ra ngắn | Không có phép đo thời lượng cửa sổ quota; gói chỉ có run lỗi 11-09 và lời thuật lại probe 12-09. |
| ops/reviews/pr516-review-5-codex-verdict.receipt.yaml:99 | probe cho thấy giới hạn ấy KHÔNG kéo dài tới 15-09 | Probe không được cấp log; câu suy trạng thái giới hạn mạnh hơn hiện vật. Giữ (b) theo tác giả và giới hạn kết luận ở thông điệp không đủ chứng minh ngày chạy lại. |
| ops/reviews/README.md:29 | hàng caveat P1 lặp nguyên câu probe chứng minh độ dài giới hạn | Khớp receipt về chữ; cùng chỗ vượt nguồn ở R5:99, không thành chứng cứ thứ hai. |
| ops/reviews/README.md:15 | Giới hạn cổng đo lại … sống qua 4 cổng (a) | Theo V1/V2 là mutant so_p2/verdict_bytes, V3 là assurance tại những head #516; đoạn đầu đã gọi sandbox cũ là (c), cuối lại nâng sang (a). Mutant mới của lượt #517 này cho cùng kết quả nhưng không hồi tố đổi nguồn của văn bản tác giả. |
| ops/reviews/README.md:423 | (a) bao cmp nguồn #511, runtime 417a209c/8873d98d, 5 mutant và 3+6 lối land | Đây là các phép chạy do V1 kể lại. Gói hiện tại không có hai bản sandbox #511 và hai thư mục run đó trực tiếp; nguồn cũ có trong log/V1 không biến thành phép chạy mới của tác giả r371. HINT giữ (c) trước khối này. |

**Cách chữa chung:** Gắn phạm vi (a)/(b)/(c) ngay tại bảng hoặc mệnh đề: chỉ băm/byte/Git/finding đo từ hiện vật là (a), tách runtime được đối chiếu với nguồn ngoài kho, lịch sử điều phối/probe thiếu log là (b), phép chạy sandbox cũ là (c). Chỉ ghi stderr báo giới hạn; bỏ kết luận hiện không còn quota hoặc đã đo được độ dài cửa sổ quota.

**HINT:** khối `# LỚP nguon-thuat-lai-bi-nang-thanh-do` trong `HINT.patch`, phủ tất cả thể hiện trên.

### template-khong-khoa-theo-luot [P2]

**Hạng lớp:** P2. **Số thể hiện:** 4.

**Cơ chế chung:** Template hoặc đoạn cảnh báo được chép sang receipt khác mà không khóa bằng review_round/run_id và nguồn verdict của lượt đó. Điều này tạo ra hiện vật quá khứ không có ở lượt 1, và gán lời tự khai của reviewer lượt 2 cho lượt 3. Thể hiện mô tả HINT5 một dòng chỉ ở mức P3; hạng lớp P2 lấy từ các thể hiện gán sai nguồn.

| Vị trí (HEAD gốc) | Khai | Đo |
|---|---|---|
| ops/reviews/pr516-review-1-codex-verdict.receipt.yaml:76 | nguon/ có VERDICT/HINT các lượt trước của chính reviewer | prompt a146d00d:9–13 và stdout của rg --files trong stderr:58–87 chỉ liệt kê 2 VERDICT/HINT #511, run 417a209c/8873d98d, actionlint; không có lượt #516 trước lượt 1. Hai lượt là của #511, đã được cộng riêng trong cùng câu. |
| ops/reviews/pr516-review-3-codex-verdict.receipt.yaml:104 | Reviewer tự khai ở đầu verdict lỗi đọc quá bảng launcher | V3:1–27 không có lời tự khai đó; toàn V3 không có launcher/_TRANSPORT_CONTRACTS. Lời tự khai nguyên văn ở V2:23; R2:39 và README:422 đã gán đúng lượt 2. |
| ops/reviews/README.md:35 | caveat lỗi đọc launcher mang tên pr516-review-3 | Cặp tên/id khớp R3 nên t27 xanh; nội dung thuộc V2. Đây là lớp mới về gán nguồn sang sai lượt, khác đếm nhầm scalar runtime. |
| ops/reviews/pr516-review-5-codex-verdict.receipt.yaml:33 | HINT: 0 hunk — một dòng ghi chú | HINT lượt 5 có 4 LF/4 dòng ghi chú, không phải một. Mẫu một dòng đúng với HINT2/HINT3 nhưng không đúng HINT5; số hunk0,byte300 và băm vẫn khớp. |

**Cách chữa chung:** Sinh mô tả gói theo inventory từng lượt; lượt 1 chỉ có nguồn PR #511. Chuyển caveat lỗi đọc launcher từ receipt 3 sang receipt 2, cùng hàng README, giữ nguyên cả năm verdict. Sửa HINT5 thành 4 dòng ghi chú, không sao mô tả một dòng từ lượt khác. Tổng caveat vẫn 13; phân bố mới 2/4/2/2/3.

**HINT:** khối `# LỚP template-khong-khoa-theo-luot` trong `HINT.patch`, phủ tất cả thể hiện trên.

### tong-hop-doi-tap-doi-tuong [P2]

**Hạng lớp:** P2. **Số thể hiện:** 6.

**Cơ chế chung:** Câu rút gọn giữ con số nhưng đổi tập đối tượng mà số ấy mô tả: số mutant ĐỎ thành tổng mutant, bốn tệp bất biến thành toàn bộ bảy tệp diff, PR được review thành PR chứa hồ sơ review. Các scalar so_p* hiện tại vẫn đúng; lỗi nằm ở câu tổng hợp và đối tượng của phép đếm.

| Vị trí (HEAD gốc) | Khai | Đo |
|---|---|---|
| ops/reviews/pr516-review-1-codex-verdict.receipt.yaml:104 | đếm 4 mutant khi có 5 | V1:282–286: lời khai cũ là 4 mutant ĐỎ, số đúng là 3 ĐỎ trên tổng 5; có 4 kết quả cổng đỏ. Câu rút gọn đã bỏ thuộc tính ĐỎ và đổi lỗi 4→3 thành tổng 4→5. |
| ops/reviews/README.md:40 | đếm 4 mutant khi có 5 | Lặp sai tập đếm của R1:104; V1 nói tổng 5 = 3 ĐỎ + 2 SỐNG. |
| ops/reviews/README.md:15 | đếm 4 mutant khi có 5 | Bản tóm tắt nguồn lặp cùng phép rút gọn mất thuộc tính ĐỎ. |
| ops/reviews/pr516-review-3-codex-verdict.receipt.yaml:98 | Nội dung 7 tệp hồ sơ không đổi qua merge (lượt 4 đo) | So 5f45e6e→c98c33e: chỉ 4 tệp pr511 bằng byte. CHANGELOG 1001730→1042451 B, README 341484→390677 B, manifest cùng 30336 B nhưng băm khác. V4:24 và bảng 45–62 nói đúng 4/4, giữ hai phía không phải bảy tệp bất biến. |
| ops/reviews/README.md:34 | Nội dung 7 tệp hồ sơ không đổi qua merge | Khớp chữ receipt 3 nhưng cùng sai đối tượng so sánh. 7/7 chỉ đúng khi so hai lượt 4 và 5 trên cùng c98c33e, không đúng qua merge 5f45e6e→c98c33e. |
| CHANGELOG.md:32 | lần thứ TƯ (r366→r367→r369→r371) | Bốn finding P2 và một P3 V1 thuộc PR #516/r369. Các mục r364:1027, r366:906–910, r367:793–795, r369:147–152 xác nhận chuỗi r364/r366/r367/r369. r371 đang chứa verdict r369, chưa thể lấy chính nó làm PR thứ tư đã bị V1 chấm. |

**Cách chữa chung:** Giữ tên tập và mốc cạnh từng con số: 5 mutant gồm 3 ĐỎ/2 SỐNG; 4 tệp pr511 bất biến, ba tệp tích hợp đổi; bốn PR đã ăn finding là r364/r366/r367/r369. Áp cùng sửa ở receipt và mọi bản chiếu README/CHANGELOG.

**HINT:** khối `# LỚP tong-hop-doi-tap-doi-tuong` trong `HINT.patch`, phủ tất cả thể hiện trên.

### dem-dong-cong-them-duoi-lf [P3]

**Hạng lớp:** P3. **Số thể hiện:** 1.

**Cơ chế chung:** Lời khai số dòng tăng một so số LF và số dòng thực tế của tệp kết thúc bằng LF. Meta trung gian có cùng hình dạng +1 ở cả năm verdict; không có script sinh meta nên không kết luận được chính xác implementation gây ra lỗi.

| Vị trí (HEAD gốc) | Khai | Đo |
|---|---|---|
| CHANGELOG.md:53 | VERDICT lượt 5 có 84 dòng | Nguon và tệp trong kho đều 7577 B, 83 LF, 83 splitlines, kết thúc LF. Receipt5:25 khai toàn bộ 83 dòng là đúng; meta516[5].verdict_lines=84 và EVIDENCE cũng 84. |

**Cách chữa chung:** Đếm LF bằng wc -l, chỉ cộng một nếu tệp không rỗng và không kết thúc LF. Sửa 84→83 trong CHANGELOG; không sửa verdict nguyên byte. Các số +1 trong EVIDENCE/meta ngoài diff được ghi chú, không tính thêm thể hiện PR.

**HINT:** khối `# LỚP dem-dong-cong-them-duoi-lf` trong `HINT.patch`, phủ tất cả thể hiện trên.

## Mutant đã chạy

Chạy cổng gốc bằng Python `-B`; t26/t27 nạp qua importlib và chọn đúng hàm trong `CA`. Bản sao là `scratch/luot1/repo`, reset về HEAD gốc trước mỗi mutant. Không chỉnh verdict hoặc mã cổng; không tái sinh manifest cho mutant. Đối chứng cây gốc và bản sao: cả bốn rc=0.

| Mutant | v2 | t26 | t27 | release strict | Kết luận |
|---|---|---|---|---|---|

| M1-hash — R1: verdict_sha256, đổi chữ số đầu1→0 | 1 | 1 | 0 | 0 | GIẾT đúng chốt |

| M2-warning — Xoá1hàngcảnhbáoR1 khỏiREADME | 0 | 0 | 1 | 0 | GIẾT đúng chốt |

| M3-so-p2 — R1:so_p2 4→3 | 0 | 0 | 0 | 0 | SỐNG 4/4 — đúng giới hạn đã khai |

| M4-bytes — R1:verdict_bytes74068→74067 | 0 | 0 | 0 | 0 | SỐNG 4/4 — đúng giới hạn đã khai |

| M5-assurance — R5:assurancecross_reviewed→cross_approved | 0 | 0 | 0 | 0 | SỐNG 4/4 — đúng giới hạn đã khai |

| M6-evidence — R1:evidence_url commit8fd3f48→46d9561 (commitcóthật,khôngchứatệp) | 1 | 0 | 0 | 0 | GIẾT đúng chốt |


V2 mutant M1 báo băm blob không khớp; M6 báo commit có thật nhưng không chứa đường dẫn. T26 M1 báo LỆCH BĂM; t27 M2 nêu đúng cặp verdict/caveat bị xoá. Release không bao phủ các receipt/README này nên rc0 không chứng minh các scalar hoặc nội dung cảnh báo đúng. Đây là giới hạn có sẵn, không phải mã mới của PR.

### Land hiện tại và lịch sử được tái dựng

| Lối land | Commit cục bộ | Cha | v2 tự chạy |
|---|---|---|---|

| merge | `46faad54245a63f151e9b46cc65341e8d690dbad` | 46d9561c8cc4b0cf530fc7ca4015de8f07c6aeec 86f87b2004f6054572cc787ae660518763b29b95 | bien_nhan_v2: 105 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 158; TỔNG: ĐẠT, rc=0 |

| ff | `86f87b2004f6054572cc787ae660518763b29b95` | 896bfbf5718ba4ffa443674e1b61d0719a8794bf | bien_nhan_v2: 105 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 158; TỔNG: ĐẠT, rc=0 |

| squash | `c5403bb31c50d1a7b8f4d24c3b529660732395f2` | 46d9561c8cc4b0cf530fc7ca4015de8f07c6aeec | bien_nhan_v2: 100 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 5 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 158, rc=1 |


Cùng tree HEAD, merge có cha base+HEAD; ff dùng HEAD hiện có; squash có **duy nhất cha base**. Squash mất đúng năm receipt pr516, không cộng pr511/pr493. Hai bộ land lịch sử còn được tái dựng: a41fc69/base6786637 có 83/0→81/2 khi squash; c98c33e/base8802924 có 100/0→98/2. SHA mô phỏng và log nằm ở `logs/history.json`; không gọi mô phỏng này là land thật trên GitHub.

### Kiểm HINT

HINT có **20 hunk / 6 tệp duy nhất**, gom thành bốn khối lớp (kể cả P3). Áp thực bằng `patch --batch --fuzz=0 --verbose -p0` trên bản sao HEAD: rc0, 20/20 hunk, không fuzz/offset; sáu tệp kết quả bằng byte bản đề nghị. Chuyển một caveat R3→R2 nên tổng 13 giữ nguyên; HINT không đổi năm verdict và không chứa diff manifest. Sau khi tái sinh manifest bằng công cụ, v2/t26/t27/release đều rc0, v2 vẫn105/0/158, release180/180.

Mã đo: `scratch/luot1/audit.py`, `gates.py`, `probes.py`, `history.py`, `make_hint.py`; dữ liệu `audit.json`, `logs/probes.json`, `logs/history.json`, `logs/hint-check.json`. Mỗi lệnh cổng có `.json` (argv,cwd,rc,thờiđiểm), `.stdout`, `.stderr`. Những file này là hiện vật của lượt #517 hiện tại, không nhận chúng là log của năm lượt #516.

## chua_do_duoc

- Không mạng; `origin` trỏ GitHub. Không gọi `ls-remote`, không xác thực comment, review object, threads/resolve, CI/job, draft/405/API merge, luật chủ kho, tài khoản vận chuyển hay sổ local gen4. Git commit metadata đo được không tự chứng thực đầy đủ sự kiện GitHub.
- Không có snapshot hai tập ref kho nguồn lúc21:06Z: 344/344,comm0/0 và1/0/0 lịch sử là KHÔNG ĐO ĐƯỢC. Quét347ref hiện tại cho r370=2,r371=1,r372=0 không kết tội hay xác nhận số lịch sử.
- Probe quota12-09 và last.md lượt5 không có trong gói; model backend/attestation danh tính và số retry không đo được. Run.json/log cho phép đối chiếu các scalar được cấp, không chứng minh nhà cung cấp thật phục vụ model gì hoặc chưa có lần phóng nào khác.
- EVIDENCE của các lượt #516 cũ, artifact scratch của họ, binary actionlint và run#511 không được cấp trực tiếp ở gói#517. Có thể đọc inventory/báo cáo trong stderr của nguồn để phân biệt hiện diện được ghi với vắng mặt, nhưng không phục hồi toàn bộ môi trường lịch sử; đặc biệt inventory lượt4 loại runs/** nên không kết tội hai run#511 vắng mặt.
- Số dòng +1 trong EVIDENCE/meta và vị trí mục lục404–408 của EVIDENCE là sai lời khai ngoài diff; chỉ số83/84 đã lan vào CHANGELOG được tính P3. Lỗi mất dấu phẩy ở các hàng pr511 cũ và khuyết cấu trúc verdict pr510 đã land nằm ngoài diff, không tính finding mới.
- Không đọc `cay-kho/CLAUDE.md`, `cay-kho/docs/PROTOCOL_DA_PHIEN.md`, `cay-kho/.claude/skills/**`, `cay-kho/AGENTS.md`; không mở đường tuyệt đối nhúng trong nguồn và không dùng mạng. Chỉ thực thi các cổng gốc được yêu cầu; không trích tài liệu mà mã cổng có thể tự dùng làm chỉ dẫn. Không chạy toàn lease suite, không chạy riêng doctrine-scan/doc-claims-check, không tuyên bố đã đo các log lịch sử đó.
- Mọi sửa/đột biến/commit-tree nằm trong `scratch/luot1/`. Git cây gốc cuối lượt phải sạch; phép kiểm cuối và băm13tệp được lưu `scratch/luot1/logs/final-state.json`.
