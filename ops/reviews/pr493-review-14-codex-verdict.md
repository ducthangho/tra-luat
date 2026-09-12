verdict: changes_requested
reviewed_sha: f618e0190e9649f3a59f735465960acca70fa050

**KHÔNG CÒN P1 · KHÔNG CÒN P2 · CÒN 4 P3: 1 lớp A, 1 lớp B, 2 nợ lớp D.** Lý do yêu cầu sửa là hai lỗi hồ sơ A/B dưới đây. Không dùng nợ D hoặc thống kê CI chưa kiểm chứng làm lý do kéo dài review. Nếu chỉ còn D thì `approve` hợp lệ theo chỉ thị lượt này.

Reviewer: Codex/GPT-6 theo cấu hình phiên, provider OpenAI, execution surface agent API có shell, transport machine; khác provider executor Claude theo giao việc. Không chứng thực độc lập backend/model đã phục vụ, không ghi transition `cross_approved`, không cấp quyền merge.

Base: `4b5184e21373eb8f8a36493d0282ebd020bb4458`; tree: `20a6522025cb8c30daefc5c4e479f63767fd01ad`. Chỉ đọc/ghi trong workspace, không mạng, không tự soạn payload đường dẫn. `cay-kho/` giữ nguyên, status trước/sau rỗng. Các cổng và đột biến chạy trên bản sao `review14-current/`, `review14-probes/`, `review14-merge/`; TMPDIR trong `review14-tmp/`. Thư mục actionlint 1.7.7 được thêm cuối PATH; cổng dùng `core.abbrev=7` qua môi trường và tắt pycache.

Bằng chứng tự chạy: [measurements.json](review14-evidence/measurements.json), [gates.json](review14-evidence/gates.json), [merges.json](review14-evidence/merges.json), [probes.json](review14-evidence/probes.json), [extra.json](review14-evidence/extra.json), [source-scope.json](review14-evidence/source-scope.json). Script tái chạy và stdout nằm cùng thư mục. Hai lỗi chọn phạm vi của parser reviewer đã sửa trước kết luận: bảng mục lục phải dừng ở cuối bảng liên tục, không gom các bảng giải thích bên dưới; bảng lượt phải giới hạn trong r360, không lấy hàng trùng số ở r362. Các output cuối đã đối chiếu lại cấu trúc nguồn.

## ĐỐI CHIẾU LƯỢT TRƯỚC

- `chieu-edited-mat-pham-vi-ci-yml`: **VÁ SINH LỖI MỚI** — lỗi B cũ tại hai trường đã được sửa thật: land evidence:212–215 và receipt lượt 2:94–99 cùng nêu đúng `.github/workflows/ci.yml` tại `2ec6171`, `pull_request` không `types`, giới hạn tập mặc định và riêng workflow `gate`. Nhưng phần giải thích mới thêm tại CHANGELOG:1568–1571 nâng một lần chạy không có raw event/run thành “phản chứng có sẵn, không cần mạng”; còn bỏ tên event `pull_request_target` của workflow đối chứng. Đây là lỗi A mới trong cách chứng minh bản vá, không phải hai câu cũ còn nguyên. Xem finding `phan-chung-edited-nang-loi-ke-thanh-hien-vat`.
- `cong-byte-co-rang-cong-claims-khong-dem-su-that`: **CHƯA VÁ** — tự chạy ba mutant độc lập: heading r358 `1016→1017`, heading r360 `5→6`, phép trừ `13 − 2 = 11→12`. Mỗi mutant đổi đúng một byte, giữ 956984 byte CHANGELOG. Cả ba claims rc0/ok=true; cả ba release rc2/ok=false, failed chỉ CHANGELOG. Nợ D được phép giữ.

Tổng đối chiếu: **0 ĐÃ VÁ THẬT · 0 VÁ HỜ · 1 VÁ SINH LỖI MỚI · 1 CHƯA VÁ**. Trạng thái tổng hợp đầu tiên không phủ nhận việc đã sửa đúng cả hai trường cũ.

**Tự đọc cả hai `on:`:** `ci.yml` có `push.branches=[master]`, `pull_request` không `types`, `workflow_dispatch`; blob bằng byte bản `2ec6171`. `workflow-thu-hoi.yml` có **`pull_request_target`**, `types=[opened,reopened,synchronize,ready_for_review,edited]`, `branches=[master]`; bằng byte bản base và head. Đây là phép đo cấu hình. Danh sách activity mặc định được hồ sơ nêu nhất quán; YAML không tự chứa đặc tả mặc định của nền tảng. Không dùng mạng để xác minh riêng đặc tả đó. Việc run `34560860197` thật sự chạy vì sửa body lúc `04:05:08Z`: **KHÔNG ĐO ĐƯỢC**, thiếu event action/changes, run/job response và readback có mốc.

**Vét lời “GitHub không phát”:** trong các tệp sống thuộc write set có ba dòng khớp literal: CHANGELOG:1565 là trích câu sai để bác; :1570 là câu điều kiện của lập luận phản chứng mới; land evidence:215 là lời cấm viết câu rộng. Không còn câu khẳng định cũ ở hai trường. Vì vậy “chỉ còn duy nhất trích dẫn đính chính” đúng về việc bỏ khẳng định cũ, **không đúng nếu hiểu là đúng một hit literal hoặc mọi hit chỉ là trích dẫn**. Không mở thêm finding chỉ vì số hit; vấn đề thực chất nằm ở lập luận mới. Receipt lượt 1, README và thân PR không chứa câu khẳng định rộng cũ; các bản chép và bảng khẳng định không được đếm thành lỗi độc lập.

**“Ba lượt liên tiếp cùng hình dạng” đứng vững ở mức mô tả ba trường hợp.** Đã đọc lại blob tại ba reviewed SHA và các finding gốc, không chỉ đọc lời tổng kết mới:

| lượt | bản chiếu tại SHA đã review | giới hạn bị bỏ | đối chứng |
|---|---|---|---|
| 11 / b43d4ab | land evidence, `pre_merge_checks[0]` | scalar launcher không có nhãn runtime/attestation; nhãn đầu tệp chỉ phủ GitHub | receipt đã ghi run.json ngoài kho; verdict 11 chỉ đúng trường này |
| 12 / e921131 | receipt lượt 1, `dieu_phoi_do_lai` của lỗi CI | viết cặp mẫu “thuộc run” chắc chắn | nguồn pr477:158–179 giữ “được cho là”, thiếu response cùng job/attempt |
| 13 / 89d938e | land evidence và receipt lượt 2 | bỏ tên workflow và điều kiện cấu hình | CHANGELOG và ci.yml giới hạn vào một workflow |

Cả ba làm câu mạnh hơn nguồn bằng cách bỏ điều kiện. Không suy từ ba ví dụ rằng mọi thao tác rút gọn đều vậy, cũng không chứng minh thứ tự tâm lý “cắt đầu tiên” hoặc quan hệ nhân quả của phương pháp vá. Các finding B khác trong các lượt đó vẫn tồn tại riêng; ba ví dụ không phải toàn bộ finding của ba lượt.

## KIỂM MERGE LẦN 5 VÀ "QUY LUẬT" TẠO TÁC

**Cả năm số cấu trúc đều khớp:** `r364→r363→r362→r361→r360→r359→r358→r356`; 0 số r trùng trong tập heading `# ★ dev-side — rN:`; 269 hàng dữ liệu bảng “Cảnh báo đang có hiệu lực”; 120 hàng dữ liệu bảng “Mục lục”; 0 hàng nguyên văn trùng trong hai bảng. Loại header/separator, không cộng bảng giải thích phía dưới mục lục.

**Không nuốt r362:** toàn mục r362 bằng byte blob `4b5184e:CHANGELOG.md`, 646 dòng mới mang sang. Các mục r364/r363/r361/r359/r356 cũng bằng byte base. `git merge-tree --write-tree f0763a0 4b5184e` chỉ báo xung đột manifest; cây tự merge khác head chỉ tại manifest. Tái dựng thật `merge --no-commit --no-ff` trên bản sao cho cùng kết quả; thay manifest bằng bản đã giải rồi `git write-tree` ra đúng tree của reviewed SHA. Chạy `release-manifest` sinh lại được manifest **bằng byte** bản giao. Điều này xác nhận kết quả tái sinh; không chứng thực thao tác lịch sử của executor khi thiếu transcript.

**Tách delta:**

| khoảng | bản chất | tự đếm numstat |
|---|---|---|
| 89d938e..f0763a0 | vá lượt 13 | 4 tệp, +39/−12 |
| f0763a0..f618e01 | merge master lần 5 | 26 tệp, +4236/−5 |
| 89d938e..f618e01 | patch giao giữa hai lượt | 28 tệp, +4270/−12 |
| 4b5184e..f618e01 | write set PR trên base mới | 8 tệp, +1766/−26 |

Không cộng trực tiếp số tệp/hunk của hai bước để suy net diff. `ops/cong_cu.py` +23 dòng và các hiện vật pr497 đến từ master, không phải bản vá riêng của PR trên base mới. Diff so base của mã cổng và hai workflow rỗng.

**Chuỗi số của thông điệp commit mới SAI; cơ chế lặp lại thì tái hiện được.** Với mỗi merge, giữ nguyên cây tệp đã giải, đo trước với HEAD trỏ cha thứ nhất, rồi đo với HEAD trỏ merge commit. Mỗi trạng thái dùng checker của chính cây lịch sử đó. Đây là A/B thay HEAD trên cây đã commit, không giả làm transcript lần merge lịch sử. Riêng lần 5 còn chạy merge chưa commit thật, có MERGE_HEAD=4b5184e và index/tree đúng như trên: vẫn 11 vi phạm, rc1.

| lần | merge | cha 1 / master mang vào | receipt mới từ master | neo phân biệt | vi phạm HEAD=cha1 | HEAD=merge |
|---|---|---|---:|---:|---:|---:|
| 1 | 7e236cf | f5098dd / c31d8f1 | 6 (pr490 lượt 1–6) | 6 | 6 | 0 |
| 2 | dd4a3ae | 9349bb0 / 0721811 | 1 (pr490 lượt 7) | 1 | 1 | 0 |
| 3 | 9e78e19 | cc21507 / c00c88a | 4 (pr492 lượt 1–4) | 1 | 4 | 0 |
| 4 | e921131 | f6df7fb / 27c413c | 2 (pr500 lượt 1–2) | 1 | 2 | 0 |
| 5 | f618e01 | f0763a0 / 4b5184e | 11 (pr497 lượt 1–11) | 6 | 11 | 0 |

Đúng là **6/1/4/2/11**, tổng 24 lượt-vi-phạm; không phải **2/2/1/4/11**, tổng 20. Không gọi 24 là số commit neo: lần 3 bốn receipt cùng một neo, lần 5 mười một receipt có sáu neo. Sáu neo lần 5 là `209bb19`, `3c82ae3`, `4d2a6f6`, `5ef3b3d`, `60b99bd`, `8104480`; cả sáu ancestry tới cha1 rc1, tới cha2 rc0, tới merge rc0. Danh sách receipt và toàn lỗi ở merges.json/log.

**Quan hệ bằng nhau không phải khớp trùng hợp trong năm ca đã đo**, vì mỗi receipt mới đều có neo thuộc cha2 nhưng chưa thuộc cha1, và các kiểm khác đều qua. `_neo_git` kiểm ancestry theo từng receipt, nên nhiều receipt chung neo vẫn sinh nhiều lỗi. Nhưng đây **không phải quy luật cho mọi merge**: receipt mới có thể trỏ một neo đã thuộc HEAD; receipt/neo có thể hỏng ở kiểm khác; thiếu object có thể cho KHÔNG ĐO ĐƯỢC. Không nhận câu “chưa lần nào là lỗi thật” như bảo lãnh mọi lần merge tương lai.

**Trả lời nợ cổng:** đáng ghi thành nợ có địa chỉ tại `ops/bien_nhan_v2.py:_neo_git` (:808–824) và `kiem` (:861). Nó ghép dữ liệu trên đĩa với ancestry của HEAD, chưa có hợp đồng rõ cho cây đang merge. Đây là khuyết của giao diện kiểm trước commit; phép kiểm canonical ancestry theo HEAD không sai trong hợp đồng kiểm một commit đã chốt. Cây Git tự nó không chứa cha, nên “đọc ancestry từ cây” không thể có nghĩa chỉ thay HEAD bằng tree hash. Nợ cần một candidate commit có tập cha xác định, hoặc trả trạng thái chưa đo được cho trạng thái dở; không được bỏ chốt tổ tiên. Ghi riêng nợ D bên dưới, không yêu cầu mở mã trong PR ghi sổ này.

## SOI HIỆN VẬT SẼ SỐNG TRONG KHO

**Land evidence — phân hạng theo trường:**

| nhóm | phép đo và kết quả |
|---|---|
| p1_theo_luot, luot_cuoi | Heading verdict 1 = 3 P1 / 5 P2 / 6 P3; verdict 2 = 0 / 3 / 10. `{1:3,2:0}` đúng, đo được từ nguồn trong kho |
| doi_chieu_luot_truoc | Đếm các dòng slug/trạng thái của verdict 2 = 7/1/0/6, tổng 14; ba slug P1 đều ĐÃ VÁ THẬT |
| reviewed_sha, authorized_head_sha, khop_head_da_merge | Đều 2ec6171f7a2e21ae950633f9e328329a355f7a6d; bằng cha thứ hai của 00e017a |
| “land evidence thứ bảy” | ls-tree ở 00e017a có 6 tệp ops/land trước khi thêm; khớp |
| provider/role/session/recorded_by, chỉ thị trực tiếp | Metadata và tự thuật; không có chứng thực backend hay transcript chỉ thị; không nâng thành phép đo danh tính |
| approval/merged_by/CI/jobs/PR/bot | Có nhãn attestation đầu tệp và giới hạn PAT/JSON tại trường liên quan. KHÔNG ĐO ĐƯỢC sự kiện/API độc lập |
| pre_merge_checks[0] | Bốn scalar launcher được ghi riêng là attestation run.json ngoài kho; 0 P1 và SHA được tách đúng thành đo được |
| các số cổng lịch sử | Chú thích :123–126 thừa nhận thiếu stdout gốc. Có thể chạy lại trên SHA, không xác nhận lần chạy lịch sử; 146 hiện nay không thay cho 121 lịch sử |
| bookkeeping sửa hai P2 / 11 còn sống | 13 heading và hai P2 thân PR có thật trong verdict; việc sửa thân PR trước merge là attestation, không hiện vật trong Git |
| bookkeeping giải thích edited | Hai câu phạm vi cũ đã sửa; lời run đã bắn vẫn thuộc nhãn GitHub đầu tệp. Tuy nhiên “chính kho này có phản chứng” bỏ event pull_request_target, cùng lập luận quá mức ở CHANGELOG |

Không tìm thêm scalar runtime mất nhãn như lượt 11 trong land evidence. **Không chứng nhận mọi trường đã đúng lập luận nguồn**: phần phản chứng mới vẫn có vấn đề. Chỗ sự kiện bị trình bày như bằng chứng offline không nhãn nằm ở CHANGELOG:1568–1571; không báo nhầm rằng nhãn GitHub đầu land evidence hoàn toàn vắng.

**Hai verdict nguyên văn:**

| tệp trong ops/reviews | byte | SHA-256 | lịch sử |
|---|---:|---|---|
| pr491-review-1-codex-verdict.md | 35088 | 38d7fb2eac39da2bbdb2d76dc43c1f0f3f505498686ffa5ad5478a7c7491248c | 0 commit M |
| pr491-review-2-codex-verdict.md | 36958 | 14c726e5ccefb76e21b23901db48915edba871640bb1bd4b169d3961d9920468 | 0 commit M |

Cả hai khớp `verdict_bytes`/`verdict_sha256` của receipt. `git log --diff-filter=M --format=%H -- <tệp>` rỗng. Commit thêm đầu tiên chung là `34e9d35be0fc52406e3659bfc24c388bf54262cd`; blob tại đó bằng byte HEAD cả hai. Không có dấu sửa byte trong lịch sử tới reviewed SHA; không chứng thực quá trình trước khi đưa vào Git.

**Hai receipt v2:** suite 146/146 đạt, chạy 146, bỏ 0, gồm t26 và t27. Ngoài chạy suite, đã tự băm verdict, kiểm hai tên verdict/receipt cùng hàng mục lục, và chín cặp verdict/ID cùng hàng cảnh báo. Tất cả đạt. T26 kiểm băm, t27 kiểm liên kết bảng; chúng không xác nhận sự thật của event hay lời giải thích caveat.

| lượt / caveat ID | tự đối chiếu nguồn |
|---|---|
| 1 / HEAD-LUOT-1-KHONG-PHAI-HEAD-DA-MERGE | ba4a258 ở header khác head đã merge 2ec6171; đúng |
| 1 / SAU-P3-KHONG-DEU-MOT-LOAI-5-cong-1 | Sáu heading P3 = năm về độ phủ + một ghi nhận giới hạn cổng; đúng nội dung verdict |
| 1 / MODEL-YEU-CAU-khac-MODEL-DA-PHUC-VU | Phân biệt yêu cầu model với model đã phục vụ; verdict tự khai không chứng thực build; khớp giới hạn |
| 1 / phan-cong-CAM-tu-soan-phan-chung | Đúng ràng buộc được nguồn khai; không suy “không finding” thành “không lỗ” |
| 2 / changes_requested-KHONG-phai-chua-dat-dieu-kien-dung | Verdict dòng 4 giữ 0 P1 và điều kiện dừng lịch sử “hết P1”; không đổi changes_requested thành approve |
| 2 / HET-P1-khong-phai-HET-FINDING-11-con-song-luc-merge | 13 lúc review là đo được; 11 = 13−2 có điều kiện nhận attestation hai sửa body. KHÔNG ĐO ĐƯỢC số finding thật còn sống lúc merge độc lập |
| 2 / NAM-FINDING-BOT-la-duong-THU-BA-ba-cai-MOI | Receipt liệt kê 5, có 3 mới/2 trùng; hai slug trùng nối được verdict. Đây là thông tin bổ sung của điều phối, không phải 5 finding có trong verdict gốc; sự kiện bot/status PR KHÔNG ĐO ĐƯỢC độc lập |
| 2 / MODEL-YEU-CAU-khac-MODEL-DA-PHUC-VU | Khớp giới hạn nhận dạng của verdict dòng 6; không xác thực backend |
| 2 / phan-cong-CAM-tu-soan-phan-chung | Khớp phạm vi dòng 8 và các đột biến nội dung được verdict thuật lại |

Chín caveat khớp **nội dung và hạng nguồn trong các giới hạn trên**. Riêng hậu tố `11-con-song-luc-merge` không được cấp chứng nhận chân trị chỉ nhờ t27 xanh: receipt đã cảnh báo con số phụ thuộc attestation ở `dieu_kien_dung_da_thoa.khong_suy_rong`; README có nhãn chung ngay đầu khối cảnh báo. Không đòi sửa lại thành 13 khi chưa có bằng chứng phủ định hai sửa body.

## BẢNG ĐO

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| head / base | f618e01 / 4b5184e | full SHA đầu verdict; ancestry rc0 | Có |
| first-parent base..HEAD | lịch sử vá và 5 merge master | 22 commit; hai commit cuối f0763a0 và f618e01 | Có |
| diff và numstat | base mới; delta giữa lượt có merge | Hai patch bằng byte Git; numstat bằng byte; bốn khoảng đã tách phía trên | Có |
| năm số cấu trúc merge | thứ tự r / 0 / 269 / 120 / 0 | đúng cả năm | Có |
| nội dung master r362 | mang nguyên vào | 646 dòng, toàn mục bằng byte | Có |
| chỉ manifest xung đột | CHANGELOG/README tự merge | merge-tree và merge chưa commit thật đồng ý; cây cuối bằng head | Có |
| manifest tái sinh | 180 tệp | tái sinh byte-exact, 8251306 byte; hash a402ed1c… | Có về kết quả |
| lần 5 trước/sau commit | 11→0; 11 receipt / 6 neo | tái hiện cả A/B và merge chưa commit thật | Có |
| chuỗi vi phạm 5 merge | 2/2/1/4/11 | 6/1/4/2/11 | **Không, finding B** |
| số lỗi = receipt master mang sang | “đúng quy luật” | bằng nhau ở cả 5 ca với điều kiện ancestry đã đo | Có trong 5 ca; không phổ quát |
| câu edited ở hai trường | giữ phạm vi ci.yml | cả hai đã sửa | Có |
| phản chứng runtime offline | run 34560860197 do sửa body | thiếu raw event/run; YAML là pull_request_target | **Không đủ chứng minh, finding A** |
| ba lượt nới rộng nguồn | 11/12/13 cùng hình dạng | ba blob lịch sử và nguồn đối chứng khớp mô tả | Có ở mức ba trường hợp |
| hai verdict / hai receipt | 35088 / 36958; hash ghim | byte/hash đúng, không commit M, nguồn đầu tiên giữ nguyên | Có |
| p1_theo_luot | 3 / 0 | đếm heading 3 / 0 | Có |
| t26 / t27 và 9 caveat | băm + liên kết cùng hàng | suite và đối chiếu riêng đạt; giới hạn chân trị nêu trên | Có trong hợp đồng |
| bảng 13 lượt | SHA/verdict/severity/cột đối chiếu | 13/13 SHA, verdict, severity khớp; các ô số đối chiếu đều khớp | Có; ô 13 chưa điền |
| ARTIFACTS.sha256 | băm hiện vật gói | 3346/3346 khớp | Có, không xác thực nguồn sinh |
| bản chép YAML/README/workflow | từ cây | 6/6 bằng byte, ci.yml bằng 2ec6171; thu-hoi bằng base | Có |
| năm slice | cắt theo mục r | 5/5 bằng byte mục tương ứng ở HEAD | Có |
| bảng khẳng định | 11 input / 3405 dòng | chạy lại byte-exact; 2109 dòng có chữ số | Có trong tập input |
| ref snapshot | 326/326/326, lệch 0 | ba TSV bằng nhau, local heads 326 | Có cục bộ; máy chủ KHÔNG ĐO ĐƯỢC |
| thông điệp commit | bản trích range base mới | bằng byte git log đã khai | Có về vận chuyển, không bảo đảm đúng nội dung |
| bien_nhan_v2.py | sạch | rc0; 67 v2 + 11 legacy + 42 nợ = 120; 0 vi phạm, 0 KHÔNG ĐO ĐƯỢC | Có |
| lease_publish_test.py | đạt | rc0; 146/146, chạy 146, bỏ 0 | Có |
| release-verify --strict --json | xanh | rc0/ok=true, 180/180, hai hash match=true; failed/extra/required_missing/errors rỗng | Có |
| doc-claims-check --strict --json | xanh | rc0/ok=true, flags=[], 106 tệp, 370 advisory | Có trong hợp đồng |
| doctrine-scan --root . | sạch | rc0, 7 tệp, 0 chỗ chép doctrine | Có |
| adr-song --root . | sạch | rc0, 46 ADR / 46 hàng, khớp1–1; tha trạng thái0016 | Có |
| nợ claims | ba mutant sống | 3/3 claims xanh, 3/3 release đỏ đúng CHANGELOG | Nợ D còn |
| CI thật/required check/cause của run | lời điều phối | không API response, event context hoặc ruleset | KHÔNG ĐO ĐƯỢC |
| kho nguồn giữ nguyên | chỉ review | status trước/sau rỗng, exact head giữ nguyên | Có |

Các lệnh cổng đúng sáu lệnh người dùng gợi ý, thêm `-B`/môi trường để không sinh pycache. Không chạy CI từ xa hoặc Windows/macOS native; không tính chúng là pass.

**Từng ô đối chiếu của bảng r360**, thứ tự ĐÃ VÁ THẬT / VÁ HỜ / VÁ SINH LỖI MỚI / CHƯA VÁ; đếm dòng slug trong phần ĐỐI CHIẾU, không đếm các tổng văn xuôi:

| lượt verdict | tự đếm | tổng slug / lượt nguồn | ô ở head |
|---|---|---|---|
| 1 | không áp dụng | không có đối chiếu | —; đúng |
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
| 12 | 1/0/0/1 | 2 / 11 | khớp |
| 13 | 2/0/0/1 | 3 / 12 | “điền ở lượt sau”; chưa có số |

Không ô số nào còn lệch nguồn. Hàng 5 theo dõi 17 slug, gồm slug đã đóng được giữ lại, không đồng nhất với 16 finding còn sống ở lượt 4. “Sinh toàn bộ cột” không có nghĩa đã điền ô lượt cuối: lời hẹn ở ô 13 là rõ, không phải số sai.

### phan-chung-edited-nang-loi-ke-thanh-hien-vat  [P3]  Đoạn vá mới gọi sự kiện thiếu raw evidence là phản chứng offline
LỚP: A
TỆP/DÒNG: `CHANGELOG.md:1568` (đoạn 1568–1571); liên quan `ops/land/pr491-r358-ghi-so-land-evidence.yaml:216`; đối chứng `.github/workflows/ops-thu-hoi-admission.yml:25`.
VẤN ĐỀ: Cụm “Phản chứng có sẵn, không cần mạng” bao cả “đã bắn đúng lúc thân PR #493 được sửa”, rồi suy “tự mâu thuẫn với một hiện vật khác”. Gói chỉ có cấu hình và lời kể run/time, không raw event/run để chứng minh lần chạy, nguyên nhân hoặc thay đổi body. Hơn nữa YAML ghi `pull_request_target`, không phải `pull_request` trong câu đang bác; một workflow khác có edited không tự chứng minh nền tảng đã phát loại event kia. Lỗi là cấp độ bằng chứng và phạm vi suy luận, **không phải đã chứng minh run không xảy ra**.
CÙNG LỚP CÒN Ở ĐÂU: land evidence có cùng lập luận “chính kho này có phản chứng”, nhưng số run ở đó được nhãn GitHub đầu tệp phủ; không đếm nó thành một lỗi thiếu nhãn độc lập. `muc-r360.md`/BANG là bản chép của cùng đoạn. EVIDENCE cuối tệp còn nói lượt 13 “không bác mệnh đề nào”, trong khi verdict 13 đã phân biệt rất rõ mã đo được và runtime chưa đo; không dùng câu của gói làm chứng cứ chấp thuận.
ĐÃ THỬ VÁ: không sửa hồ sơ; hướng vá tại chính đoạn CHANGELOG và bookkeeping: tách cấu hình (nêu đủ event) khỏi lời điều phối về run, ghi thiếu raw evidence và bỏ kết luận run là phản chứng offline. Đây là chỗ sinh lập luận, không cần sửa workflow. Muốn chứng minh runtime thì cần hiện vật phù hợp; không cần đợi nó để sửa câu đúng phạm vi.
ĐÃ THỬ NGHIỆM: parse hai YAML bằng BaseLoader giữ nguyên khóa `on`; so blob head/base/2ec6171; đọc đoạn mới và vét các hit. Kết quả cấu hình nêu trên; runtime KHÔNG ĐO ĐƯỢC do thiếu dữ liệu và cấm mạng. Kiểm khóa bản vá: đọc riêng đoạn sửa vẫn phân biệt event, nguồn và điều kiện; không chỉ dán nhãn attestation ở nơi khác. Nguy cơ vá: tiếp tục bỏ tên event hoặc nâng YAML thành bằng chứng chạy thật.
ĐỘ TIN: cao

### chuoi-nam-merge-chep-sai-bon-moc  [P3]  Thông điệp merge mới ghi 2/2/1/4/11 thay cho 6/1/4/2/11
LỚP: B
TỆP/DÒNG: thông điệp commit `f618e0190e9649f3a59f735465960acca70fa050`, bản trích `thong-diep-commit.txt:17`.
VẤN ĐỀ: Chuỗi tuyên bố có thứ tự “ở năm lần merge” sai cả bốn số trước lần 5. Bản tổng kết không theo kịp năm cây/cha lịch sử; chính message 7e236cf đã ghi sáu vi phạm. Sai này nằm trong hiện vật sẽ sống cùng Git, không chỉ ở prompt. Đẳng thức receipt/lỗi đúng trong các ca đo không cứu được chuỗi đầu vào sai.
CÙNG LỚP CÒN Ở ĐÂU: cùng chuỗi trong BANG_KHANG_DINH là bản trích message; các ô bảng đối chiếu r360 đã kiểm không sai. Không quy toàn bộ luật ancestry thành sai chỉ vì chuỗi bị chép nhầm.
ĐÃ THỬ VÁ: không sửa lịch sử. Hướng rẻ: thêm đính chính có neo đích danh f618e01 vào hồ sơ sống, kèm bảng commit/cha/receipt/lỗi sinh từ phép đo; không cần amend/rebase chỉ để xoá dấu vết lời cũ. Giữ điều kiện của đẳng thức, đừng chỉ đổi năm số từ trí nhớ.
ĐÃ THỬ NGHIỆM: `review14-evidence/merge_probe.py`: mỗi cây lịch sử A/B HEAD=cha1 so HEAD=merge; kết quả 6/1/4/2/11→0/0/0/0/0; liệt kê receipt mới và neo, đối chiếu từng cái. Ca khóa bản vá: sinh đủ năm hàng cùng OID, so từng ô, tổng 24 lượt-vi-phạm; không trộn số neo với số receipt. Nguy cơ vá: đảo lần 3/4 hoặc làm mất điều kiện để biến năm ca thành luật mọi merge.
ĐỘ TIN: cao

### cong-byte-co-rang-cong-claims-khong-dem-su-that  [P3]  Cổng claims chưa bắt ba loại sai số nội dung đã đo nhiều lượt
LỚP: D
TỆP/DÒNG: `scripts/tl_core/workflow.py:1163` (`_doc_claims_scan_one`) và :1430 (`_doc_claims_check`); các câu thử ở `CHANGELOG.md:1031`, :1349, :1768.
VẤN ĐỀ: Ba mutant nội dung sai số vẫn qua claims; release chỉ phát hiện không khớp manifest. Không dùng cổng byte để chứng nhận sự thật con số. Nợ ngoài write set, không chặn approve một mình.
CÙNG LỚP CÒN Ở ĐÂU: ba nhóm tổng chuỗi, số đối tượng heading, phép trừ finding đều sống; không suy mọi loại khẳng định đều không được kiểm.
ĐÃ THỬ VÁ: không; giữ nợ có địa chỉ cho packet mã cổng. Hướng vá: kiểm có cấu trúc theo hợp đồng từng đại lượng và nguồn đếm, không hardcode ba chuỗi. Không sửa receipt hay băm verdict để làm xanh.
ĐÃ THỬ NGHIỆM: `review14-evidence/probes.py`, ba mutant một byte độc lập; claims rc0/ok=true/flags=[]; release rc2, failed chỉ CHANGELOG; control xanh. Ca khóa: cả ba mutant phải đỏ ở cổng nội dung, control xanh. Nguy cơ vá: regex bắt nhầm trích dẫn lịch sử hoặc câu đính chính thành khẳng định hiện hành.
ĐỘ TIN: cao

### cong-receipt-chua-dinh-nghia-cay-dang-merge  [P3]  Kiểm tệp đang merge nhưng ancestry vẫn ghim HEAD cũ
LỚP: D
TỆP/DÒNG: `ops/bien_nhan_v2.py:808`–824 (`_neo_git`), :861 (`kiem`).
VẤN ĐỀ: Bộ kiểm đọc receipt từ đĩa nhưng so neo với HEAD; trong pending merge hai đầu vào không đại diện cùng candidate. Nó báo “vi phạm” đối với receipt hợp lệ của cha master sẽ thuộc merge. Đây là nợ hợp đồng kiểm trước commit; không phải lý do bỏ kiểm tổ tiên hoặc gọi cổng sai khi nó đang kiểm chính HEAD đã chốt. Chỉ ghi nợ, không chặn PR ghi sổ.
CÙNG LỚP CÒN Ở ĐÂU: cả năm merge tái hiện; nhiều receipt cùng neo vẫn được tính riêng. Các cổng chỉ kiểm byte/cấu trúc không gặp đúng vấn đề ancestry này.
ĐÃ THỬ VÁ: không; đề nghị packet riêng định nghĩa candidate commit/tree+parents tường minh và ràng buộc tree với nội dung đang kiểm, hoặc báo trạng thái chưa đo được cho pending state. Không thay HEAD bằng tree hash; tree không có ancestry. Không nhận tùy ý MERGE_HEAD hay mọi object đang có làm chứng cứ canonical.
ĐÃ THỬ NGHIỆM: năm A/B cùng cây ở merges.json; merge lần 5 thật chưa commit có MERGE_HEAD=4b5184e, tree bằng reviewed tree, rc1/11 lỗi; cây tại merge commit rc0/0 lỗi. Ca khóa: cùng candidate/cha cho kết quả nhất quán trước và sau khi ghi commit; neo ở nhánh không liên quan vẫn phải bị chặn, thiếu object vẫn phải báo KHÔNG ĐO ĐƯỢC. Nguy cơ vá: mở rộng tổ tiên quá mức để receipt neo nhánh rẽ lọt qua, hoặc kiểm tree không khớp dữ liệu đĩa.
ĐỘ TIN: cao về hành vi; vừa về lựa chọn giao diện kế nhiệm
