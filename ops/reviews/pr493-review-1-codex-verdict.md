verdict: changes_requested
reviewed_sha: 4af7e2907e86cfcad10c0d097c4678a800d32c04

**CÒN P1:** lời khai “13 finding còn sống lúc merge” mâu thuẫn với chính hai P2 được khai đã sửa trước merge. Cổng byte và cổng receipt có răng; chúng không chứng minh lời khai đúng.

Reviewer: Codex, provider OpenAI, chạy công cụ shell cục bộ qua API; khác provider executor Claude. Không xác thực độc lập model backend. Phạm vi do người dùng giao: đọc hiện vật offline, chạy phép đo sẵn có và đột biến nội dung trên bản sao `cay-kho/`, ghi verdict; không push, merge, mạng hay tự soạn payload đường dẫn. Đây là kết quả cross-review, không tự cấp merge authorization. Tree đo: `ff37d8995f6a79a51d8d24f449e187654447c7dd`.

## BẢNG ĐO

Đường dẫn mã/tài liệu bên dưới tương đối với `cay-kho/`, trừ hiện vật gói được ghi rõ. “Khớp nội dung nguồn” không có nghĩa sự kiện GitHub đã được xác minh. Log và JSON đo nằm trong `review-evidence/`.

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| Exact head | 4af7e2907e86cfcad10c0d097c4678a800d32c04 | `git rev-parse HEAD` đúng toàn bộ OID; cây sạch trước đo | Có |
| Quy mô delta | prompt nói 8 tệp, +1350/−5 | `git diff --shortstat 00e017a 4af7e29`: 8 tệp, **+1196/−20**; `numstat.txt` và `diff.patch` khớp git nguyên văn | Tóm tắt prompt lệch; hai hiện vật diff đúng, không quy thành lỗi nội dung PR |
| Mã thực thi thay đổi | Không | 8 đường dẫn chỉ CHANGELOG, manifest, land evidence, README, hai verdict và hai receipt | Có |
| Toàn vẹn gói hiện vật | ARTIFACTS.sha256 | Tự băm **3203/3203**, không lệch | Có; không chứng thực nguồn sinh |
| Ref snapshot | 318/318/318, lệch 0/0 | Tập tên+OID `nguon-refs.tsv`, `mirror-refs.tsv`, heads cây: 318, bằng nhau; kho không shallow | Có; không hỏi lại máy chủ |
| Root repo | neo launcher 394e934… | `rev-list --max-parents=0 HEAD`: 394e93468fc8d84ec20938e6df8fb7ab72b2cc37 | Có |
| Chuỗi #468→#489 | 7 PR, #486 trước #480 | `rev-list --count --first-parent b416830..c0a5cbe` =7; log: #468, #477, #478, #486, #480, #487, #489 | Có |
| Payload chuỗi | 1016 tệp, 247458 dòng thêm, chỉ ops | `git diff --shortstat` đúng; tập thành phần đường dẫn cấp đầu = {ops} | Có |
| Land evidence | 6 trước, tệp mới thứ bảy | `ls-tree --name-only` trên c0a5cbe và 00e017a =6; HEAD =7 | Có |
| Head PR491 vào merge | 2ec6171, đúng head lượt 2 | `merge-base --is-ancestor 2ec6171 00e017a` rc0; cha thứ hai 00e017a đúng reviewed_sha receipt/verdict lượt2 | Có |
| Hai verdict: severity | 3/5/6 và 0/3/10 | Regex toàn tệp đúng từng số; heading finding =14 và13 | Có; `p1_theo_luot` thực sự đo được |
| Trạng thái 14 slug cũ | 7 thật, 1 hờ, 0 sinh lỗi, 6 chưa | Đếm marker in đậm trong verdict2 =7/1/0/6; ba slug P1 nằm nhóm thật | Có |
| Băm verdict1 | 38d7fb2e… | 38d7fb2eac39da2bbdb2d76dc43c1f0f3f505498686ffa5ad5478a7c7491248c | Có |
| Băm verdict2 | 14c726e5… | 14c726e5ccefb76e21b23901db48915edba871640bb1bd4b169d3961d9920468 | Có |
| Nguyên văn nguồn lượt2 | giữ nguyên | So byte `VERDICT-PR491-LUOT2.md` với verdict trong kho bằng nhau | Có; lượt1 không có bản nguồn độc lập ngoài blob đã neo |
| Byte/head trong mục lục | 35088/ba4a258d; 36958/2ec6171f | Đọc byte và header verdict khớp cả receipt lẫn hai hàng README | Có |
| verdict_path | đường dẫn đầy đủ ops/reviews/... | Cả hai trỏ đúng tệp, không chỉ basename | Có |
| evidence_url | commit đầu chứa verdict | `git log --diff-filter=A --format=%H -1 -- <tệp>`: cả hai =34e9d35be0fc52406e3659bfc24c388bf54262cd, đúng URL; commit chỉ thêm hai verdict | Có |
| Cảnh báo | 9 hàng, ID cùng hàng verdict | Parse ô bảng: 4+5 ID đều ở cột id và đúng verdict; thêm 2 hàng mục lục, 9 hàng cảnh báo | Có hình thức |
| Nợ lúc merge | 13 finding lượt2 còn sống +5 bot | Lượt2 có13 khi review; receipt lại ghi2 P2 đã sửa trước merge, nên còn **11 của lượt2** theo chính hồ sơ; 5 bot có giao tập | **Không** |
| Phép hợp của “5” | 1 P2 lượt2 +4 bot, bot as-of trùng | Tập lỗi nội dung {nhãn nguồn, neo spec, gói/payload, #490, phạm vi ref} có5. Bot as-of là tập con lỗi nhãn; bot ref sửa lời khai, P3 ref sửa bảng trích | Có về 5 đối tượng; không đồng nghĩa 5 đã đóng |
| Vá #1 nhãn nguồn | đã vá | Có nhãn installer, Issue/PR, cặp run, bốn lượt; nhưng khung vẫn “hai loại/mọi số Git”, ba lượt t33 và probe builder còn thiếu nhãn; bảng BA loại gán số hàng sai | **VÁ HỜ** |
| Vá #2 neo bd32d11 | cảnh báo không canonical | `merge-base --is-ancestor bd32d1145a4b890da695dc56196997b582c5be1e 2ec6171` rc1; thân đã tự khai chưa snapshot, khung đầu vẫn bao mọi số Git | Đã công bố giới hạn; chưa làm neo bền, khung chưa nhất quán |
| Vá #3 gói/payload | bcde19d5→d47be343, 8075509→8089302 | `git show <sha>:RELEASE_MANIFEST.json` tại c0a5cbe/2ec6171 khớp; bản vá nói rõ payload ops không vào gói, r358 đổi gói | Có, vá thật |
| Vá #4 #490 | dự định tương lai, trạng thái thuật lại | Đã giải thích ngay sau câu in đậm; không còn phải suy là đã land #490 | Vá giới hạn lời khai; tồn tại/trạng thái PR **KHÔNG ĐO ĐƯỢC** offline |
| Vá #5 mọi ref | chỉ branch head | Đã thay chính câu mở bằng BRANCH HEAD, có cảnh báo tag/namespace; builder dùng --heads | Có, vá lời khai thật; P3 độ phủ khác vẫn mở |
| Current manifest | 180 tệp, hợp lệ | 180, hash a812f04beb23ab7f73574bf60e95863d6b7b4e32e0de31e2a0aef85f4885b79f, total_bytes8103458; ops có0 mục, CHANGELOG có trong kê | Có |
| VERSION | 1.36.68, không nâng ở PR này | Tệp VERSION =1.36.68, không trong delta | Có trong phạm vi PR này |
| release strict | ok,180/180 | rc0, ok=true, failed=[], package_hash_match=true | Có |
| release đột biến | phải đỏ | Đổi đúng một byte, giữ size809136: rc2, failed chỉ CHANGELOG.md, hash_match=false; khôi phục rc0 | Có răng |
| doc claims strict | rc0,ok=true | Control rc0; đổi 1016→1017 toàn CHANGELOG vẫn rc0; đổi riêng tiêu đề r359 5→6 cũng rc0/ok=true | Khớp giới hạn cổng, không phải P1 cổng |
| lease suite | 121/121, chạy121,bỏ0 | python3 -B ops/lease_publish_test.py: rc0, đúng121/121/chạy121/bỏ0 | Có |
| Receipt validator hiện tại | 43 v2, tổng96,0 vi phạm | rc0; 43 v2+11 legacy+42 nợ=96;0 vi phạm;0 KHÔNG ĐO ĐƯỢC | Có |
| Receipt trên master cũ | 41 v2,tổng94 | PR mới thêm2 receipt; lượt này chạy validator ở HEAD, không tái chạy cây00e017a | Số cũ chưa trực tiếp chạy lại |
| t26/t27 chặn | băm / ID | Control đều PASS; đổi byte verdict ⇒ t26 AssertionError LỆCH BĂM; đổi ID ô cảnh báo ⇒ t27 AssertionError đúng caveat | Có |
| t33 khi thiếu actionlint | AssertionError,0 subprocess | Gọi chính hàm, mock shutil.which=None: AssertionError; subprocess.run call_count=0 | Có: ca chạy, lint chưa chạy |
| doctrine-scan / adr-song | rc0/rc0 | rc0/rc0; 7 tệp,0 chép doctrine;46 ADR/46 hàng | Có |
| run.json lượt14/15 | 35 khóa; lenh3 khóa | Parse cả hai:35; lenh={chuong_trinh,so_doi_so,van_tay} | Có cấu trúc; không chứng thực model |
| _kiem_bia_mo | any tại606 | Đọc ops/lease_publish.py:606 đúng any | Có mã; không tái dựng payload mới |
| CI merge Ubuntu | 44;40+4;20m38s | **KHÔNG ĐO ĐƯỢC** run/job offline. Phép cộng44, trừ timestamp1238s khớp | Số học khớp; sự kiện không xác minh |
| CI merge Windows | 44;38+6;49m09s | **KHÔNG ĐO ĐƯỢC** run/job offline. Phép cộng44, trừ timestamp2949s khớp | Số học khớp; sự kiện không xác minh |
| Biên Windows |10m51s, hẹp hơn11m45s | 3600−2949=651s;3600−2895=705s;hẹp54s | Có số học; không chứng minh xu hướng |
| CI/merge source label | attestation | Land evidence dòng7–10 gắn nhãn mọi sự kiện GitHub; khong_do_duoc nhắc thiếu JSON thô | Có nhãn trong land evidence; r359/thân PR thiếu nhãn tại các đoạn CI |
| Approval, ba run đỏ/một xanh, không merge khi đỏ, Windows đầu tiên, edited không bắn job | sự kiện đã diễn ra | **KHÔNG ĐO ĐƯỢC** offline. Đọc được cấu hình ci.yml pull_request không types, push master, matrix và timeout60; workflow duyệt có ready_for_review | Chỉ xác minh cấu hình, không xác minh lịch sử |
| Runtime hai lượt |696s/714s,rc0 | Receipt tự khai thiếu run.json gốc; thời gian bắt đầu/kết thúc tự khai không phải chứng cứ runtime độc lập | **KHÔNG ĐO ĐƯỢC** |
| Tự thú mất bản vá |806980→806981, checkout mất sửa | Không có log/bản nháp; bytes Git ở00e017a/34e9d35=794980, cdd0b1d=807870, HEAD=809136;806980 có thể là bản nháp khác | **KHÔNG ĐO ĐƯỢC**, không suy là số giả |
| Tự thú đếm8 |8, thân4 nhóm, cộng nhầm2 P2 | Các commit còn trong lịch sử đã ghi5; không có bản nháp8 hay transcript. Chỉ cộng2 vào5 cho7, không tái dựng đủ phép tính8 | **KHÔNG ĐO ĐƯỢC** nguyên nhân/tần suất |
| Lời học cũ về đột biến thật | có sẵn trong CLAUDE | CLAUDE.md:692 có đúng câu trích | Có văn bản; không chứng minh phiên đã đọc |
| 10 P3 lượt2 |9 bo-sot +1 cổng | Đếm slug đúng9+1; một trong9 là bỏ toàn thân PR do không đưa input, không phải regex | Số khớp; giải pháp gộp cả9 không đúng |
| Bảng khẳng định | trích các hiện vật | Tái chạy script với đúng hai muc-* cho byte bằng bảng; thiếu thân PR; r359 chỉ dòng1–110, r358 thực bắt đầu122 và kéo đến332, slice sau chỉ111–300 | Thiếu đầu vào và mệnh đề không chữ số |

### no-luc-merge-dem-ca-hai-p2-da-dong  [P1]  Số 13 finding còn sống lúc merge tự mâu thuẫn với hai P2 đã sửa
TỆP/DÒNG: ops/reviews/README.md:18,278; ops/reviews/pr491-review-2-codex-verdict.receipt.yaml:7,192–194; cùng receipt:83–102.
VẤN ĐỀ: 13 là tổng finding lúc verdict ra đời, không thể đồng thời là số còn sống lúc merge khi hồ sơ khẳng định hai P2 đã sửa TRƯỚC merge. Theo chính lời khai sửa đó, lượt2 còn1 P2+10 P3=11. Câu “13+5 còn sống” còn mời người đọc cộng cả những mục trùng bot/lượt2. Đây là số trạng thái sự kiện sai trong mục lục/biên nhận mới, không phải lỗi của verdict nguyên văn. Việc hết P1 của PR491 vẫn không bị phủ nhận.
ĐÃ THỬ VÁ: không — giữ nguyên verdict; sửa receipt và README thành “13 lúc review; hai P2 khai đã sửa trước merge;11 còn lại”, tách năm báo cáo bot khỏi tổng lỗi phân biệt; đổi ID caveat ở cả receipt và cột id nếu ID còn gắn13-con-song. Giữ nhãn attestation cho việc sửa thân PR.
ĐÃ THỬ NGHIỆM: Parse verdict đếm13; safe_load receipt thấy đúng hai mục da_va:true và mô tả trước merge. 13−2=11. t27 control PASS bất chấp mâu thuẫn nội dung; mutant ID làm t27 đỏ. Sự kiện sửa thân PR thực tế KHÔNG ĐO ĐƯỢC do không có response PR491, nhưng hai mệnh đề của chính hồ sơ không thể cùng đúng.
ĐỘ TIN: cao

### nhan-nguon-van-va-than-de-nguyen-khung  [P2]  Lỗi nhãn nguồn chưa đóng nên “năm đã vá” còn quá rộng
TỆP/DÒNG: CHANGELOG.md:74–95,131–137,192–210,222–225,276–282,295–299.
VẤN ĐỀ: Khung vẫn xếp “mọi số Git” vào hai loại, còn thân thêm loại ngoài canonical. Ba lượt t33 vẫn không có nhãn tại chỗ dù verdict2 chỉ rõ thiếu nguồn đếm. Probe PATH/sentinel được gọi “đo được” nhưng chỉ nội dung mã đo lại được, sự kiện động không có log. Bảng builder nói “hai hàng cuối” trong khi thiếu shellcheck nằm hàng ĐẦU; nói “bốn hàng còn lại” bỏ phần AL_VER rỗng/sai định dạng cùng hàng đầu. Bốn phản ví dụ được r359 kể không bao trọn finding nguồn thật, vốn còn ba lượt t33 và phân loại builder. Có tiến bộ rõ, nhưng chưa đóng toàn bộ; 5 là số đối tượng sửa, không phải số đã đóng sạch.
ĐÃ THỬ VÁ: không — sửa ngay khung phân loại, gắn nguồn cho ba lượt và probe, tách AL_VER/thiếu shellcheck thành ca riêng hoặc thêm cột nguồn theo ca. Không thay số lịch sử bằng số hôm nay.
ĐÃ THỬ NGHIỆM: Đọc finding so-lich-su-bi-mat-nhan-nguon trong verdict2 và từng hunk git diff; xác nhận bảng6 hàng, thiếu shellcheck chung hàng đầu. Tái chạy t33 chứng minh fail tiền điều kiện, không chứng minh số ba lượt lịch sử. Những sự kiện cũ KHÔNG ĐO ĐƯỢC offline.
ĐỘ TIN: cao

### dong-chin-p3-khong-deu-can-bo-trich-moi  [P2]  Lại gộp lỗi thiếu input vào giới hạn regex
TỆP/DÒNG: CHANGELOG.md:100–107; than-pr-493.md:52; ops/reviews/pr491-review-2-codex-verdict.receipt.yaml:103–111.
VẤN ĐỀ: Đúng9 slug bo-sot, nhưng bo-sot-toan-than-pr nói rõ đây KHÔNG phải hạn chế regex: thiếu input thân PR, kể cả dòng có chữ số. Câu “đóng chín cái đầu đòi một bộ trích phủ cả văn xuôi: công cụ mới, cổng riêng” hoãn cả sửa chữa đã làm được bằng script hiện tại. Không phải mọi định lượng viết bằng chữ đều bị bỏ: dòng chứa chữ số khác vẫn được giữ.
ĐÃ THỬ VÁ: không — tách nợ cấp input khỏi nợ trích mệnh đề; sửa khẳng định toàn xưng về regex thành “bỏ dòng không có chữ số”.
ĐÃ THỬ NGHIỆM: Chạy trich_khang_dinh.py với hai input tái tạo bảng đúng byte; script vòng qua sys.argv[1:] đã hỗ trợ thêm thân PR. Đọc finding nguồn xác nhận chính nó đã nêu nguyên nhân này.
ĐỘ TIN: cao

### nhan-attestation-khong-di-cung-ban-tom-tat  [P2]  R359 và thân PR lại trình bày sự kiện CI như phép đo không kèm giới hạn nguồn
TỆP/DÒNG: CHANGELOG.md:51–72; than-pr-493.md:17–28; ops/land/pr491-r358-ghi-so-land-evidence.yaml:7–10.
VẤN ĐỀ: Land evidence tự khai đúng attestation, nhưng r359 và thân PR sao lại số CI/cổng duyệt, gọi ĐO được mà không đem theo nhãn thiếu response thô tại đoạn ấy. Người đọc hai bản này không thấy ranh giới mà chính r358 đang được sửa để bảo vệ. Không khẳng định các số CI sai.
ĐÃ THỬ VÁ: không — gắn nhãn attestation và dẫn land evidence ngay tại hai nhóm CI/cổng duyệt; giữ riêng số học tự kiểm được.
ĐÃ THỬ NGHIỆM: Đọc ba hiện vật; land evidence có nhãn, hai đoạn tóm tắt không có. CI, approval, lần Windows đầu tiên KHÔNG ĐO ĐƯỢC vì cấm mạng và không có JSON thô.
ĐỘ TIN: cao

### suy-mat-ref-thanh-mat-object-tuc-thi  [P2]  Không là tổ tiên chưa chứng minh xóa một nhánh là mất khả năng tra OID
TỆP/DÒNG: CHANGELOG.md:91,278–282; ops/reviews/README.md:19; ops/reviews/pr491-review-2-codex-verdict.receipt.yaml:121.
VẤN ĐỀ: Cảnh báo độ bền đúng, nhưng “chỉ tra được chừng nào ref nhánh còn sống/số chết khi nhánh bị xoá” mạnh hơn phép đo ancestry. Object có thể còn do ref khác, clone khác hoặc chưa bị thu gom. Ngay gói này có cả refs/heads/... và refs/remotes/mirror-cuc-bo/... chứa OID. Hỏng bảo đảm fetch từ canonical khác với chứng minh OID lập tức không tra được.
ĐÃ THỬ VÁ: không — viết “không được bảo đảm tồn tại trong clone tương lai chỉ lấy canonical history”; nếu muốn neo bền thì lưu snapshot được theo dõi. Không sửa/xóa ref để thử.
ĐÃ THỬ NGHIỆM: merge-base rc1; `git for-each-ref --contains bd32d1145a4b890da695dc56196997b582c5be1e --format='%(refname)'` trả hai ref nêu trên. Không đo GC máy chủ.
ĐỘ TIN: cao

### hai-tu-thu-thieu-nguyen-lieu-kiem-doc-lap  [P3]  Chưa chứng minh được bản nháp mất sửa và phép tính tám
TỆP/DÒNG: CHANGELOG.md:76–80,114–120; than-pr-493.md:56–59.
VẤN ĐỀ: Không có transcript checkout, output verifier với806980/806981 hoặc bản nháp ghi8. Số byte của các commit không trùng số bản nháp, nhưng không bác được một trạng thái chưa commit. Lời giải “cộng hai” chưa giải thích đầy đủ8 so5; “lần thứ hai trong cùng phiên” cũng không thể đếm từ git. Không gọi thiếu chứng cứ là thú tội sai, cũng không chứng nhận đã đúng.
ĐÃ THỬ VÁ: không — ghi đây là tự thuật chưa có log, cung cấp bản nháp/output nếu còn; chỉ giải thích số8 khi dựng lại được các hạng cộng.
ĐÃ THỬ NGHIỆM: `git log 00e017a..HEAD` có3 commit; hai commit có r359 đều đã ghi5. Đếm byte blob trong package-slices.json; CLAUDE:692 khớp câu trích. Hai sự kiện tự thú và mức rộng/hẹp của chúng: KHÔNG ĐO ĐƯỢC.
ĐỘ TIN: cao về thiếu chứng cứ; thấp về lịch sử chưa commit

### cong-byte-co-rang-cong-claims-khong-dem-su-that  [P3]  Cổng xanh vẫn cho con số sai trong tiêu đề r359 đi qua
TỆP/DÒNG: CHANGELOG.md:1,105,122; scripts/tl.py; RELEASE_MANIFEST.json.
VẤN ĐỀ: release kiểm tính toàn vẹn; claims không kiểm phép đếm5 finding hay1016 tệp. Đây là giới hạn đã khai, không phải P1 và không phủ nhận răng release.
ĐÃ THỬ VÁ: có — đột biến byte cùng kích thước và số5→6 trên bản sao được giao, khôi phục nguyên byte trong finally; không tái sinh manifest.
ĐÃ THỬ NGHIỆM: review-evidence/mutations.json: release mutant rc2, failed=[CHANGELOG.md], package_hash_match=false, control/restored rc0; claims1016→1017 rc0. r359-five-to-six.out: ok=true, flags=[]; lệnh trả0. t26/t27 cũng đỏ đúng mutant tương ứng.
ĐỘ TIN: cao

### bo-sot-pham-vi-ref-va-vat-chat-hoa  [P3]  Bảng vẫn thiếu chính phạm vi branch head và giới hạn namespace
TỆP/DÒNG: CHANGELOG.md:182,184–188; trich_khang_dinh.py:15–18.
VẤN ĐỀ: Dòng chứa số PR ở183 được giữ, nhưng câu phạm vi ở182 và lời giới hạn tag/namespace cùng bước vật chất hóa không có chữ số nên rơi. Có tên finding ở r359 không thay thế việc trích đủ mệnh đề được sửa.
ĐÃ THỬ VÁ: không — Thêm nguyên đoạn với đối tượng/namespace, không đổi kết quả heads thành mọi ref.
ĐÃ THỬ NGHIỆM: Đọc mã builder --heads và tập heads318 khớp snapshot; omitted.txt ghi thiếu các dòng trên. Namespace khác của máy chủ KHÔNG ĐO ĐƯỢC.
ĐỘ TIN: cao về độ phủ bảng; sự kiện thiếu nguồn không được chứng nhận

### bo-sot-tu-khai-evidence-va-manifest  [P3]  Hợp đồng đầu ra EVIDENCE và manifest vẫn mất khỏi bảng
TỆP/DÒNG: CHANGELOG.md:187–188; BANG_KHANG_DINH.txt.
VẤN ĐỀ: Hai dòng không chữ số chứa việc sinh EVIDENCE, cách trích, phần bỏ sót và lập manifest bị bỏ. Bảng không thể hiện được lời khai hợp đồng đầu ra này.
ĐÃ THỬ VÁ: không — Thêm trọn mệnh đề đầu ra, tách tính toàn vẹn hiện vật khỏi provenance sinh gói.
ĐÃ THỬ NGHIỆM: Regex không chọn187–188; băm độc lập3203 mục khớp. Không chạy lại builder vì nó gọi mạng.
ĐỘ TIN: cao về độ phủ bảng; sự kiện thiếu nguồn không được chứng nhận

### bo-sot-pham-vi-nen-chua-do  [P3]  Phủ định đo macOS/Windows native tiếp tục vắng
TỆP/DÒNG: CHANGELOG.md:299; BANG_KHANG_DINH.txt.
VẤN ĐỀ: Dòng không chữ số chứa giới hạn Linux+Bash và chưa đo hai nền native bị bỏ; có thể đọc nhầm các probe builder là đa nền.
ĐÃ THỬ VÁ: không — Bổ sung giới hạn trong đúng phạm vi probe builder, không phủ định các số CI Windows riêng.
ĐÃ THỬ NGHIỆM: Tái trích đúng hai input, không có dòng tương ứng299; môi trường lượt này Linux. Hai nền khác KHÔNG ĐO ĐƯỢC.
ĐỘ TIN: cao về độ phủ bảng; sự kiện thiếu nguồn không được chứng nhận

### bo-sot-nguong-hai-client  [P3]  Bảng không chứa ngưỡng ít nhất hai client
TỆP/DÒNG: CHANGELOG.md:310–311; muc-r358-da-va.md; BANG_KHANG_DINH.txt.
VẤN ĐỀ: Ngưỡng viết bằng chữ bị bỏ; hơn nữa cả phần cuối r358 không được đưa vào input. Đây là quy tắc định lượng trong nội dung review, dù nó không cấp phép gọi mạng ở lượt này.
ĐÃ THỬ VÁ: không — Đưa đủ r358 vào input rồi bổ sung trọn câu ngưỡng và nguồn; tuân thủ cấm mạng.
ĐÃ THỬ NGHIỆM: Đọc CHANGELOG và CLAUDE khớp ngưỡng; slice sau kết thúc ở dòng300 của CHANGELOG; regex cũng không chọn310–311.
ĐỘ TIN: cao về độ phủ bảng; sự kiện thiếu nguồn không được chứng nhận

### bo-sot-pham-vi-r-va-hai-sentinel  [P3]  Bảng giữ thao tác nhưng mất đối tượng và hậu quả probe
TỆP/DÒNG: CHANGELOG.md:297–299; BANG_KHANG_DINH.txt.
VẤN ĐỀ: Dòng297 có9.9.9 được giữ; hai dòng sau thiếu số, làm mất phạm vi chốt không nhìn chính thư mục đầu ra và kết quả cả hai sentinel bị xóa. Không tự dựng lại payload để lấp lỗ.
ĐÃ THỬ VÁ: không — Bổ sung nguyên mệnh đề cùng nhãn thuật lại. Nếu cần động nghiệm, điều phối chuẩn bị sẵn phép đo an toàn với dữ liệu đánh dấu; reviewer chỉ chạy.
ĐÃ THỬ NGHIỆM: Đọc nguồn và kết quả regex: thiếu298–299. Hậu quả động KHÔNG ĐO ĐƯỢC với nguyên liệu được giao; không tự soạn chuỗi đường dẫn.
ĐỘ TIN: cao về độ phủ bảng; sự kiện thiếu nguồn không được chứng nhận

### bo-sot-input-than-pr-va-duoi-r358  [P3]  Bảng thiếu cả thân PR493 và phần cuối mục r358
TỆP/DÒNG: BANG_KHANG_DINH.txt; muc-r359.md; muc-r358-da-va.md; CHANGELOG.md:301–332; than-pr-493.md.
VẤN ĐỀ: Bảng đúng byte kết quả hai slice:1–110 và111–300 của CHANGELOG. Mục r358 thật còn301–332, bao gồm cận dưới20 finding,1/6 stdout và35 khóa. Không có section thân PR493, dù nó có số CI, receipt96 và lời khai lần đẩy cdd0b1d. Đây là thiếu input, không do regex. Tên slice r359 cũng không chứa đoạn tự thú cuối; đoạn ấy đang ở slice mang tên r358.
ĐÃ THỬ VÁ: không — Cắt theo heading thực thay vì110/190 dòng cố định; gọi script với đủ hai mục và thân PR. Sau đó vẫn cần bổ sung mệnh đề không chữ số.
ĐÃ THỬ NGHIỆM: Tái chạy script với hai muc-* bằng bảng nguyên byte; package-slices.json ghi section và offset; đọc heading tiếp theo tại333 để xác định đủ r358.
ĐỘ TIN: cao về độ phủ bảng; sự kiện thiếu nguồn không được chứng nhận

### bo-sot-hop-dong-phan-loai-nguon  [P3]  Bảng không giữ toàn bộ lượng từ và hai loại nguồn
TỆP/DÒNG: CHANGELOG.md:131–138; BANG_KHANG_DINH.txt.
VẤN ĐỀ: Các dòng131–136 không chữ số bị bỏ, chỉ137 chứa PR491 được giữ. Bảng còn đuôi lời hứa nhãn nhưng mất định nghĩa hai loại, mọi số Git và mọi sự kiện GitHub; đây là phạm vi thiết yếu cho việc kiểm bản vá.
ĐÃ THỬ VÁ: không — Đưa nguyên khối phân loại vào bảng mệnh đề, nối các đối tượng với nhãn nguồn thay vì chỉ giữ dòng có mã PR.
ĐÃ THỬ NGHIỆM: Regex bỏ131–136/138; đọc khung đủ thấy hai loại cùng lời hứa toàn xưng; đối chiếu thân276–282 tự nhận có ngoại lệ.
ĐỘ TIN: cao về độ phủ bảng; sự kiện thiếu nguồn không được chứng nhận

### bo-sot-dieu-kien-chot-so-ci  [P3]  Điều kiện completed trước khi chốt số CI vẫn vắng
TỆP/DÒNG: CHANGELOG.md:257–259; BANG_KHANG_DINH.txt.
VẤN ĐỀ: Cả ba dòng không chữ số bị bỏ: thiếu quy tắc chỉ trả số khi completed và phải KHÔNG ĐO ĐƯỢC khi in_progress. Bảng giữ con số nhưng mất điều kiện được dùng nó.
ĐÃ THỬ VÁ: không — Thêm trọn điều kiện kèm giới hạn rằng quy tắc không chứng minh nguyên nhân lần đọc cũ.
ĐÃ THỬ NGHIỆM: Đọc257–259 và regex: cả ba vắng; nguồn land evidence cũ cũng nêu quy tắc. Hành vi run thật KHÔNG ĐO ĐƯỢC offline.
ĐỘ TIN: cao về độ phủ bảng; sự kiện thiếu nguồn không được chứng nhận

### bo-sot-gioi-han-du-lieu-run-json  [P3]  Bảng mất giới hạn không lưu argv/model của run.json
TỆP/DÒNG: CHANGELOG.md:324–331; BANG_KHANG_DINH.txt.
VẤN ĐỀ: Phần này nằm ngoài slice, đồng thời dòng326/331 không số chứa danh sách khóa và giới hạn tự khai/model sẽ vẫn mất nếu chỉ nới slice mà giữ regex. Đếm35 không chứng nhận model.
ĐÃ THỬ VÁ: không — Đưa toàn đoạn cấu trúc và phủ định provenance vào bảng, kiểm JSON thực, không chỉ tìm model ở cấp cao.
ĐÃ THỬ NGHIỆM: Parse hai run.json:35 khóa cấp cao,3 khóa lenh đúng; bảng hiện tại không chứa đoạn324–331.
ĐỘ TIN: cao về độ phủ bảng; sự kiện thiếu nguồn không được chứng nhận

### bo-sot-dieu-kien-kich-hoat-workflow  [P3]  Bảng mất tập sự kiện dùng để giải thích tại sao sửa thân PR không bắn CI
TỆP/DÒNG: CHANGELOG.md:42–49; BANG_KHANG_DINH.txt.
VẤN ĐỀ: Dòng42 còn ci.yml và pull_request, nhưng43 mất mặc định các types và48 mất danh sách ready_for_review; bảng không còn đủ điều kiện để đối chiếu hai workflow. Đây là phạm vi của lời khai CI, không phải số hiệu vô hại.
ĐÃ THỬ VÁ: không — Bổ sung toàn mệnh đề cấu hình và nhãn lịch sử; phân biệt workflow không đăng ký edited với lời khái quát rằng GitHub không có activity đó.
ĐÃ THỬ NGHIỆM: Regex bỏ43,47–49; đọc hai YAML cho cấu hình khác nhau. Lịch sử run và xử lý sự kiện máy chủ KHÔNG ĐO ĐƯỢC.
ĐỘ TIN: cao về độ phủ bảng; sự kiện thiếu nguồn không được chứng nhận

Các đột biến chỉ áp dụng bản sao được người dùng giao; đã phục hồi nguyên byte, không commit và không tái sinh manifest. Chứng cứ chính: `review-evidence/measurements.json`, `mutations.json`, `package-slices.json`, `omitted.txt`, `*.out`. Tệp verdict PR491 giữ nguyên băm. Kết luận không dựa vào việc cổng xanh để chứng nhận sự thật trong văn xuôi.
