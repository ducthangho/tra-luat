verdict: changes_requested
reviewed_sha: 89d938efbc03a50a3efbc163d0f1ade29f66de08

**KHÔNG CÒN P1 · KHÔNG CÒN P2 · CÒN 2 P3: một lỗi lớp B và nợ lớp D.** Hai lỗi B cụ thể của lượt 12 đã vá thật; phép vét theo trường phát hiện một bản chiếu khác còn mất phạm vi nguồn. Không dùng nợ D hoặc thống kê CI chưa kiểm chứng làm lý do yêu cầu sửa tiếp.

Reviewer: Codex/GPT-6 theo cấu hình phiên, provider OpenAI, execution surface agent API có shell, transport machine; khác provider executor Claude theo chỉ thị giao việc. Không chứng thực độc lập model backend, không tự ghi transition `cross_approved`, không cấp quyền merge.

Base tự đo: `27c413c3e531800431cad9db4452d7236505a5a9`; tree: `02f20f92f9a9af0c663a2c53b4d74ad822334c98`. Kho `cay-kho/` giữ nguyên, status trước/sau rỗng. Chạy cổng trên `review13-current/`, đột biến trên `review13-probe/`; TMPDIR các phép chạy đặt trong workspace. Thêm thư mục actionlint 1.7.7 vào cuối PATH; đặt `core.abbrev=7` qua môi trường. Không mạng, không tự soạn payload đường dẫn.

Sai thao tác của reviewer cần công bố: đầu phiên có một lệnh chuyển hướng bản đọc ba tài liệu sang `/tmp/unused`, ngoài thư mục được người dùng cho phép. Đây là vi phạm ranh giới ghi của phiên review; tệp đó không được dùng làm bằng chứng. Các script, log và kết quả review dưới đây nằm trong workspace. Không khai phiên tuân thủ tuyệt đối ràng buộc thư mục.

Bằng chứng: [measurements.json](review13-evidence/measurements.json), [extra.json](review13-evidence/extra.json), [static.json](review13-evidence/static.json), [gates.json](review13-evidence/gates.json), [probes.json](review13-evidence/probes.json). Script tái chạy và stdout cổng ở cùng thư mục. Hai lỗi parser của reviewer (tên slice có hậu tố; README dùng basename) đã sửa trước kết luận, không tính output lỗi là phép đo âm.

## ĐỐI CHIẾU LƯỢT TRƯỚC

- `doi-chieu-luot10-chep-nham-hang-luot9`: **ĐÃ VÁ THẬT** — LỚP B. Tự parse các dòng slug trong phần `ĐỐI CHIẾU` của đủ 12 verdict, không đếm các tổng văn xuôi. Hàng 10 ở CHANGELOG:647 đúng `3·1·0·1`, tổng 5, nguồn lượt 9. Toàn bộ ô đã điền số ở hàng 2–11 khớp nguồn; hàng 4/5 được bổ sung đúng. Không có ô số nào còn lệch nguồn.
- `receipt-pr491-luot1-chieu-cap-run-mat-gioi-han-nguon`: **ĐÃ VÁ THẬT** — LỚP B. Receipt lượt 1:56–65 khôi phục “ĐƯỢC CHO LÀ” cùng giới hạn thiếu response trước/sau, job/attempt/danh sách bước. Đối chiếu `ops/land/pr477-dung-goi-review-land-evidence.yaml:156–179`: đúng mức dè dặt, giữ nguyên nhân CHƯA XÁC ĐỊNH, không biến hai tổng thành chứng minh cơ chế. Không kéo quá tay: trường băm/byte và số heading vẫn được trình bày riêng, tự đo khớp 35088 byte và 3/5/6.
- `cong-byte-co-rang-cong-claims-khong-dem-su-that`: **CHƯA VÁ** — LỚP D. Tự chạy ba đột biến độc lập, mỗi lần đổi đúng một byte và giữ 896404 byte CHANGELOG: heading r358 `1016→1017`, heading r360 `5→6`, phép trừ `13 − 2 = 11→12`. Cả ba claims rc0/ok=true/flags=[]; cả ba release rc2, failed chỉ CHANGELOG. Nợ D được phép giữ theo chỉ thị lượt 13.

Tổng: **2 ĐÃ VÁ THẬT · 0 VÁ HỜ · 0 VÁ SINH LỖI MỚI · 1 CHƯA VÁ**.

Đếm từng ô dưới đây theo thứ tự **ĐÃ VÁ THẬT / VÁ HỜ / VÁ SINH LỖI MỚI / CHƯA VÁ**:

| verdict / hàng | tự đếm | tổng slug / lượt nguồn | ô hiện tại |
|---|---|---|---|
| 1 | không có phần đối chiếu | không áp dụng | `—`, đúng |
| 2 | 0/6/0/11 | 17 / 1 | khớp |
| 3 | 7/3/0/10 | 20 / 2 | khớp |
| 4 | 1/2/0/14 | 17 / 3 | khớp |
| 5 | 3/0/1/13 | 17 / 4 | khớp |
| 6 | 11/2/0/1 | 14 / 5 | khớp |
| 7 | 4/3/2/1 | 10 / 6 | khớp |
| 8 | 7/0/1/1 | 9 / 7 | khớp |
| 9 | 7/2/0/1 | 10 / 8 | khớp |
| 10 | 3/1/0/1 | 5 / 9 | khớp |
| 11 | 2/0/0/1 | 3 / 10 | khớp |
| 12 | 1/0/0/1 | 2 / 11 | ghi “điền ở lượt sau”, chưa có số để so |

Hàng 5 đếm **17 slug theo dõi**, không phải 16 finding còn sống của lượt 4: nguồn lượt 5 nói rõ giữ thêm slug đã đóng `bo-sot-gioi-han-du-lieu-run-json`. Không báo nhầm lỗi bảo toàn tổng. Hàng 12 là ô công khai chưa điền; không coi là số chép sai, cũng không chứng nhận lời “toàn bộ cột” theo nghĩa đã có số ở cả 12 hàng. Các bộ P1/P2/P3, SHA viết tắt và verdict của 12 hàng đều khớp 12 nguồn.

**Kiểm cách chữa gốc:** CHANGELOG:868–917 và thân PR:88 đã bỏ chỉ dẫn dùng `ops/**` làm tập vét; các hit còn lại là trích cách cũ để bác. Danh sách nêu bảy nơi chứa bản chiếu, có cả hai receipt; tên viết tắt/brace mở được duy nhất bằng `git ls-tree`. Hai verdict nguyên văn được giữ làm đối chứng, manifest được kiểm bằng cổng byte. Quy tắc phân loại **từng trường** là đúng và rộng hơn việc sửa hai địa chỉ. Tuy nhiên **kết quả vét chưa đóng hết lớp B**: trường bookkeeping trong land evidence và `no_con_lai[].va_the_nao` của receipt lượt 2 còn bỏ giới hạn cấu hình, xem finding bên dưới. Đây là thể hiện cũ còn sót, không phải lỗi do khôi phục chữ “được cho là” sinh ra.

## KIỂM COMMENT VỀ CHECK thu-hoi

Gói không có raw comment/readback riêng cho comment đang hỏi, không có JSON 200 runs/jobs/event hoặc ruleset. Tôi kiểm các mệnh đề (a)–(d) theo nội dung người dùng cung cấp; **KHÔNG ĐO ĐƯỢC** việc comment đã đăng nguyên byte ấy. `workflow-thu-hoi.yml` khớp byte với blob ở base `27c413c` và HEAD. Gói có local branch `master=27c413c`; không có ref `origin/master` trong checkout, nên không giả vờ lệnh đọc ref ấy thành công.

| mệnh đề | kết quả tự kiểm |
|---|---|
| (a) dòng 86 đòi workflow_sha == base.sha | **Đo được, đúng.** `TL_S` lấy từ `github.event.pull_request.base.sha`, `TL_WF_SHA` lấy từ `github.workflow_sha`. Chạy riêng đúng dòng 86 bằng hai scalar được cung cấp: khác nhau trả **12**, bằng nhau trả **0**. Không chạy curl/fetch/workflow. Đây là tái hiện nhánh lỗi, không phải log run thật. |
| (a) định nghĩa “luôn lấy TIP master”, “chỉ thoả khi master chưa nhích kể từ base PR” | **KHÔNG ĐO ĐƯỢC** quy tắc nền tảng/runtime từ gói này: thiếu event/context và nguồn đặc tả GitHub tương ứng; bị cấm mạng. Mã chỉ chứng minh phép so hai giá trị context, không tính `merge-base` hay kiểm “master đã nhích”. Không đồng nhất `base.sha` của event với base Git cố định của gói. Không nhận, cũng không bác giải thích ấy bằng suy luận. |
| (b) 14/14 đỏ trên mọi PR trong 200 runs gần nhất | **KHÔNG ĐO ĐƯỢC**: không tập API để đếm/lọc, không run ID/attempt/conclusion đầy đủ. Số này không trở thành phép đo của reviewer. |
| (b) aad3d01/#500, dae1aed/#501 đã merge | **Đo được phần Git:** cả hai OID là tổ tiên `27c413c`, ancestry rc0/0. Trạng thái PR và kết luận check tương ứng trên máy chủ: **KHÔNG ĐO ĐƯỢC**. Ancestry không xác nhận màu check. |
| (b) “đỏ sẵn, delta PR này = 0” | **Đo được delta mã:** base..HEAD không đổi workflow hay `ops/lease_publish.py`. **KHÔNG ĐO ĐƯỢC delta kết quả CI/quan hệ nhân quả**; không suy nó từ diff rỗng hay hai commit đã nhập lịch sử. |
| (c) header tự khai CHƯA KÍCH HOẠT, cờ False | **Đo được:** header :4–7 đúng như khai; `ops/lease_publish.py:929` gán `SO_THU_HOI_KICH_HOAT = False`. |
| (c) “chưa là required check” | **Đo được rằng header tự khai như vậy. KHÔNG ĐO ĐƯỢC cấu hình required check thực tế** vì không có branch protection/ruleset API. Header không xác thực cấu hình máy chủ. |
| (d) types có edited; ci.yml không khai edited | **Đo được cấu hình:** target workflow :25–28 có 5 activity types gồm `edited`; ci.yml :10–20 có `pull_request` không `types`, push/master và dispatch. Cấu hình ci.yml cũng nguyên byte so `2ec6171`. |
| (d) run đỏ thực sự bắn vì sửa thân PR, không phải push; gate không bắn | **KHÔNG ĐO ĐƯỢC sự kiện thực tế:** thiếu event `action`, thay đổi body, danh sách runs và thời điểm. `edited` không tự nói trường nào được sửa; cùng cấu hình còn có `synchronize`. Không gán nguyên nhân run chỉ từ YAML. |

**Comment có khai rộng hơn phép đo không?** Có, nếu đọc các kết luận “luôn/chỉ”, “delta = 0” về hành vi CI, “chưa required” và nguyên nhân lần chạy như những sự thật được gói chứng minh. Phần chứng minh tại chỗ chỉ là phép so SHA, trigger/cờ và delta mã. Thống kê 14/14 là lời khai ngoài gói, **chưa kiểm chứng chứ không bị chứng minh sai**. Cách diễn đạt có thể kiểm toán là tách “đã đọc cấu hình”, “điều phối thuật kết quả API” và “giả thuyết giải thích”. Không mở finding chống mã workflow ngoài write set chỉ vì chưa xác nhận API.

## SOI HIỆN VẬT SẼ SỐNG TRONG KHO

**Land evidence — đã mở và phân hạng các nhóm trường:**

| nhóm trường | phép đo / giới hạn | kết quả |
|---|---|---|
| cross_review.p1_theo_luot, luot_cuoi | Đếm heading `^### .*\[P[123]\]` trên hai verdict | **3/5/6 = 14**, **0/3/10 = 13**; `{1:3,2:0}` đúng; không phải attestation |
| doi_chieu_luot_truoc | Đếm từng slug nguồn verdict2 | **7/1/0/6 = 14**, ba P1 đều ĐÃ VÁ THẬT |
| authorized_head_sha, reviewed_sha, khop_head_da_merge | Đọc header verdict và cha merge `00e017a` | Cùng `2ec6171f7a2e21ae950633f9e328329a355f7a6d`, đúng cha thứ hai |
| Land evidence thứ bảy | `git ls-tree -r --name-only 00e017a ops/land/` | 6 tệp trước khi thêm, đúng |
| Metadata phiên, provider/model, chỉ thị trực tiếp | Tự khai, không có chứng thực backend/session | Đúng khi đọc là metadata/attestation; KHÔNG ĐO ĐƯỢC danh tính đã phục vụ |
| Approval, merged_by, CI/run/job, thời gian, trạng thái PR, bot | Nhãn giới hạn đầu tệp; nhãn PAT và trường khong_do_duoc | Có nhãn; KHÔNG ĐO ĐƯỢC sự kiện bằng API trong sandbox |
| pre_merge_checks[0], bốn scalar runtime | Nhãn tại chỗ :105–118; thiếu run.json | Đúng hạng attestation; riêng 0 P1 và SHA vẫn là đo được |
| Các output cổng lịch sử | Chú thích :123–126 nói thiếu stdout gốc | Có thể chạy lại hành vi, không xác nhận lần chạy lịch sử; không lấy 146 hiện nay thay 121 lịch sử |
| Bookkeeping 13−2=11 và năm bot | 13 heading; hai P2 thân PR thật có trong nguồn; bot có 3 mới/2 trùng theo receipt | Số học có điều kiện đúng; việc sửa trước merge và kết quả bot vẫn KHÔNG ĐO ĐƯỢC độc lập |
| Bookkeeping giải thích edited | So :212 với CHANGELOG:481–488 và cấu hình | **Mất phạm vi nguồn**, finding B bên dưới |

Vì hàng cuối, chưa thể trả lời “mọi trường đã đúng hạng/phạm vi nguồn”. Các số CI có cộng trừ được cũng chỉ kiểm số học, không nâng thành sự kiện đã xác minh.

**Hai verdict nguyên văn:**

| tệp | byte tự đo | SHA-256 tự đo | lịch sử sửa |
|---|---:|---|---|
| ops/reviews/pr491-review-1-codex-verdict.md | 35088 | `38d7fb2eac39da2bbdb2d76dc43c1f0f3f505498686ffa5ad5478a7c7491248c` | 0 commit M |
| ops/reviews/pr491-review-2-codex-verdict.md | 36958 | `14c726e5ccefb76e21b23901db48915edba871640bb1bd4b169d3961d9920468` | 0 commit M |

Băm/byte khớp cả hai receipt. `git log --diff-filter=M --format=%H -- <tệp>` đều rc0/stdout rỗng. Commit thêm đầu tiên cả hai là `34e9d35be0fc52406e3659bfc24c388bf54262cd`; `git diff-tree` xác nhận commit chỉ thêm hai verdict. Đọc blob ngay commit đó và so byte HEAD: **2/2 bằng nhau**. Kết luận giới hạn ở lịch sử đi tới reviewed SHA, không chứng thực quá trình sinh trước Git.

**Hai biên nhận v2:** suite **146/146 đạt, đã chạy 146, bỏ 0**, bao gồm t26 kiểm băm và t27 kiểm quan hệ bảng. Tự đối chiếu riêng hai hàng mục lục README:308/309 và chín cặp verdict/ID README:32–40, tất cả đúng hàng. T26/t27 không kiểm chân trị lời giải thích về event.

| lượt / caveat | đối chiếu nội dung |
|---|---|
| 1 / HEAD-LUOT-1-KHONG-PHAI-HEAD-DA-MERGE | ba4a258 khác 2ec6171; Git và header khớp, không gán finding head cũ cho master |
| 1 / SAU-P3-KHONG-DEU-MOT-LOAI-5-cong-1 | Sáu heading P3: năm độ phủ, một giới hạn cổng; đúng ghi nhận dương cuối verdict |
| 1 / MODEL-YEU-CAU-khac-MODEL-DA-PHUC-VU | Giữ phân biệt model yêu cầu/đã phục vụ; không xác minh backend |
| 1 / phan-cong-CAM-tu-soan-phan-chung | Khớp giới hạn phạm vi nguồn; không biến không thử thành không có lỗ |
| 2 / changes_requested-KHONG-phai-chua-dat-dieu-kien-dung | Khớp verdict2:4: 0 P1 thoả điều kiện lịch sử, vẫn changes_requested |
| 2 / HET-P1-khong-phai-HET-FINDING-11-con-song-luc-merge | 13 lúc review; 11 chỉ khi nhận attestation hai P2 đã sửa; các nhãn giới hạn ở receipt/README giữ điều kiện này |
| 2 / NAM-FINDING-BOT-la-duong-THU-BA-ba-cai-MOI | Danh sách receipt có 5, 3 mới/2 trùng; hai slug trùng nối được nguồn. Sự kiện bot/review ID/trạng thái #490 KHÔNG ĐO ĐƯỢC độc lập, không giả là dữ kiện từ verdict gốc |
| 2 / MODEL-YEU-CAU-khac-MODEL-DA-PHUC-VU | Khớp giới hạn ở verdict2:6 |
| 2 / phan-cong-CAM-tu-soan-phan-chung | Khớp phạm vi ở verdict2:8 và các đột biến nội dung được thuật lại; không lẫn với payload bị cấm |

Chín caveat khớp trong các giới hạn ấy. Lỗi mới tìm được nằm ở trường **ngoài caveat**, không phải băm hay thiếu một hàng cảnh báo.

## BẢNG ĐO

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| Head/base | 89d938e / 27c413c | Full SHA ở đầu; ancestry rc0 | Có |
| First-parent base..HEAD | chuỗi vá và nhập master | 20 commit; head mới một cha e921131, không merge ở delta lượt 13 | Có |
| Delta lượt 12→13 | bản vá thuần | 3 tệp, +77/−28; patch byte-exact Git | Có |
| Toàn delta so base | 8 tệp hồ sơ/manifest | 8 tệp, +1739/−26; numstat và diff.patch byte-exact | Có |
| Mã thực thi/workflow | không đổi | Không có đường mã trong delta; diff riêng workflow/checker rỗng | Có về mã |
| Băm hiện vật gói | ARTIFACTS.sha256 | 3315/3315 khớp | Có, không xác thực nguồn sinh |
| Bản chép YAML/README/workflow | chép từ cây | 5/5 bằng byte; workflow bằng blob base | Có |
| Sáu slice | cắt đúng heading | 6/6 bằng byte; đầu mục 1,98,199,385,984,1104 | Có |
| Bảng khẳng định | 12 đầu vào, 2999 dòng không rỗng | Chạy lại byte-exact; 1903 dòng có chữ số | Có trong tập input |
| Ref snapshot | 324/324/324, lệch 0 | Ba TSV bằng nhau, 324 local heads, không shallow | Có cục bộ; máy chủ KHÔNG ĐO ĐƯỢC |
| origin/master | tên ref trong lời hướng dẫn | Checkout không có ref ấy; local master=27c413c | Không đo bằng origin/master; dùng OID đã ghim |
| Thứ tự heading đầu | 364→363→361→360→359→358→356 | Regex đúng bảy heading ấy | Có |
| Bảng 12 lượt: severity/head/verdict | các hàng đã ghi | 12/12 khớp nguồn | Có |
| Bảng đối chiếu | sinh lại cột | Mười ô số hàng 2–11 khớp; hàng 1 không áp dụng; hàng 12 chủ ý chưa điền | Có với ô có số; chưa phải cột điền đủ |
| Receipt1 cặp run | giữ dè dặt nguồn | “được cho là”, thiếu response/job/attempt; băm/severity vẫn đo được | Có |
| Vét theo trường | đóng các bản chiếu sót | Quy tắc đã sửa; còn hai trường về edited mất phạm vi | Chưa đóng lớp B |
| `python3 -B ops/bien_nhan_v2.py` | 0 vi phạm, tổng109 | rc0; 56v2+11legacy+42nợ=109; 0 vi phạm, 0 KHÔNG ĐO ĐƯỢC của cổng | Có |
| `python3 -B ops/lease_publish_test.py` | 146/146 | rc0; 146/146; đã chạy146, bỏ0 | Có |
| `python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | 180/180 xanh | rc0, ok=true, hai hash match=true; failed/extra/required_missing/errors rỗng | Có |
| Manifest | 180 tệp, 8190726 byte | Kiểm byte qua release; package hash `1799ccdfd21e397a53b4f56366b3acef19b5bba5011faec8befa07b65a545a29` | Có |
| `python3 scripts/tl.py doc-claims-check --strict --json` | xanh | rc0, ok=true, flags=[]; 106 tệp, 370 advisory | Có trong hợp đồng cổng |
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | rc0 | rc0; 7 tệp, 0 chỗ chép doctrine | Có |
| `python3 .claude/dev/packet_loop.py adr-song --root .` | rc0 | rc0; 46 ADR/46 hàng, khớp1–1; output tha trạng thái0016 | Có |
| Ba mutant nội dung | nợ D | Mỗi mutant đổi1byte; claims0/true, release2/false | Nợ còn |
| Dòng86 thu-hoi | khác SHA ⇒12 | Đúng dòng lệnh với scalar đã khai: rc12; control bằng SHA: rc0 | Có về nhánh mã |
| 14/14, trigger run thật, required check | lời điều phối/API | Thiếu response/run context/ruleset | KHÔNG ĐO ĐƯỢC |
| Kho được review không sửa | read-only | status rỗng trước/sau; hai bản sao cũng sạch sau khôi phục | Có |

Các cổng dùng thêm `-B`/môi trường không sinh pycache; không thay logic lệnh. Không chạy full CI từ xa, Windows/macOS native hoặc full selftest sản phẩm; không tính các phần ấy là pass.

### chieu-edited-mat-pham-vi-ci-yml  [P3]  Hai hồ sơ biến giới hạn trigger của ci.yml thành quy tắc phát event của GitHub
LỚP: B
TỆP/DÒNG: `ops/land/pr491-r358-ghi-so-land-evidence.yaml:212`; `ops/reviews/pr491-review-2-codex-verdict.receipt.yaml:94`. Đối chứng trong chính PR: `CHANGELOG.md:481–488`, `.github/workflows/ci.yml:10–20`.
VẤN ĐỀ: Hai trường viết “GitHub không phát `pull_request` cho sự kiện `edited`”. Nguồn có phạm vi hẹp hơn: **ci.yml không khai types**, nên **workflow ấy** không chạy trên edited theo tập mặc định được nguồn nêu. Bản chiếu bỏ cả tên cấu hình lẫn điều kiện mặc định, đổi “workflow không chạy” thành “nền tảng không phát event”. Đây là sai lệch phạm vi đọc trực tiếp được giữa các bản ghi, dù nhận attestation hai P2 đã sửa trước merge. Nhãn attestation về sự kiện lịch sử không sửa được sự đổi nghĩa của câu giải thích. Không dùng việc `pull_request_target` có edited để chứng minh semantics `pull_request`; đó là hai event khác nhau. Semantics GitHub độc lập KHÔNG ĐO ĐƯỢC ở sandbox này, và không cần giả định nó để thấy bản chiếu rộng hơn nguồn.
CÙNG LỚP CÒN Ở ĐÂU: Hai trường nêu trên là hai thể hiện của cùng một lỗi, tính MỘT finding. Bản chép YAML ngoài cây trùng byte, không đếm thêm. README:33 nói không bắn CI trong ngữ cảnh lịch sử; thân PR:109 giữ “edited không nằm trong tập ấy”; CHANGELOG giữ tên workflow và điều kiện — không đánh đồng chúng với câu phủ định event ở hai YAML.
ĐÃ THỬ VÁ: không — không sửa hồ sơ executor. Hướng vá cụ thể: ở cả hai YAML, thay lời giải thích bằng “`ci.yml` tại `2ec6171` dùng tập activity mặc định, không có `edited`, nên sửa thân PR không kích hoạt workflow `gate` ấy và không đổi head”. Giữ nguyên nhãn attestation cho việc thật sự sửa/readback trước merge; không nâng lời giải thích thành bằng chứng runtime.
ĐÃ THỬ NGHIỆM: `python3 -B review13-evidence/static_check.py` rc0, lưu nguyên từng dòng nguồn/bản chiếu; `git diff 2ec6171 HEAD -- .github/workflows/ci.yml` rỗng, nên không phải nhầm do ci.yml thay đổi. Bộ receipt rc0 và suite146/146 vẫn xanh: các cổng không so nghĩa câu này. Sự kiện/API thực tế KHÔNG ĐO ĐƯỢC vì thiếu response và cấm mạng.
ĐỘ TIN: cao về mất phạm vi nguồn; không kết luận màu CI hay cơ chế phát event thực tế.

### cong-byte-co-rang-cong-claims-khong-dem-su-that  [P3]  Cổng claims vẫn nhận ba sai số nội dung dù cổng byte chặn
LỚP: D
TỆP/DÒNG: `scripts/tl_core/workflow.py:1430`; các mẫu tại heading r358/r360 và phép trừ trong CHANGELOG.
VẤN ĐỀ: Ba mutant độc lập giữ kích thước, thay đúng một byte, vẫn claims rc0/ok=true. Release phát hiện băm đổi nhưng không xác minh con số lịch sử đúng. Đây là nợ hợp đồng cổng đã biết, không phải regression mã ở PR hồ sơ.
CÙNG LỚP CÒN Ở ĐÂU: Ba mẫu đã tự đo trong `review13-evidence/probes.json`; không suy thành kết luận mọi loại mệnh đề đều lọt.
ĐÃ THỬ VÁ: không — thay hợp đồng cổng ngoài phạm vi; user cho phép giữ riêng nợ D.
ĐÃ THỬ NGHIỆM: `python3 -B review13-evidence/probe.py` rc0; 3/3 claims rc0/true/flags=[], 3/3 release rc2/false, failed chỉ CHANGELOG; đã khôi phục byte gốc, status bản sao rỗng.
ĐỘ TIN: cao.
