verdict: changes_requested
reviewed_sha: d47ea5949366c8d470ef0b1538e0fafa725bd35e

**KHÔNG CÒN P1 · KHÔNG CÒN P2 · CÒN 5 P3: 1 lớp F, 1 lớp C, 1 lớp E và 2 nợ D.** Ba lỗi hồ sơ mới là lý do yêu cầu sửa. Hai nợ D không chặn approve một mình. Không chấm việc thiếu giải thích dài thành lỗi; cũng không nhận lời khai “tối giản” thay cho đọc bản vá.

Reviewer: Codex/GPT-6 theo cấu hình phiên, provider OpenAI, execution surface agent API có shell, transport machine; khác provider executor Claude theo chỉ thị giao việc. Không chứng thực độc lập backend/model phục vụ; không ghi transition `cross_approved`, không cấp quyền merge.

Base đầy đủ: `4b5184e21373eb8f8a36493d0282ebd020bb4458`; tree: `0483b52226db766baa87badbeb9bb25976d4ed8d`. Authority là chỉ thị trực tiếp cho lượt 15, điều kiện dừng tới P3 và ngoại lệ hai nợ D. Chỉ thao tác trong workspace, không mạng, không tự soạn payload đường dẫn. `cay-kho/` giữ nguyên HEAD, status trước/sau rỗng. Cổng chạy trên `review15-current/`; phép thử trong `review15-probes/` và `review15-merge/`; TMPDIR cho bộ chạy trong workspace, tắt pycache, actionlint 1.7.7 được thêm **thư mục** vào cuối PATH. Các checkout/merge/update-ref dưới đây chỉ thực hiện trên bản sao của reviewer.

Bằng chứng và script tái chạy: [measurements.json](review15-evidence/measurements.json), [gates.json](review15-evidence/gates.json), [merges.json](review15-evidence/merges.json), [probes.json](review15-evidence/probes.json), [extra.json](review15-evidence/extra.json), [pending-clean.json](review15-evidence/pending-clean.json). Stdout từng cổng nằm cùng thư mục. Đường dẫn kho trong finding tính từ `cay-kho/`.

## ĐỐI CHIẾU LƯỢT TRƯỚC

- `phan-chung-edited-nang-loi-ke-thanh-hien-vat`: **ĐÃ VÁ THẬT** — CHANGELOG:1569–1586 và land evidence:215–225 không còn dùng run làm phản chứng offline. Cả hai ghi thiếu raw event, phân biệt `pull_request_target` với `pull_request`, thu bằng chứng trực tiếp về nội dung cấu hình. Hai YAML thật khớp tên event/tập types được trích. Tuyên bố về lần run và nguyên nhân vẫn KHÔNG ĐO ĐƯỢC; bản vá đã nhận đúng giới hạn này. Không coi việc nhắc lại câu sai trong đoạn bác là tái phạm.
- `chuoi-nam-merge-chep-sai-bon-moc`: **VÁ SINH LỖI MỚI** — đã sửa thật chuỗi thành **6/1/4/2/11**, neo đính chính `f618e01`, không sửa lịch sử. Tôi tái chạy năm cây với HEAD=cha1 rồi HEAD=merge: đúng chuỗi đó, sau commit đều 0. Nhưng bảng mới ghi lần 2 “biên nhận thêm = 2”, thực tế **A=1, M=1**. Kết luận mới “4/5” vì thế sai; xem finding lớp F. Đây là lỗi phát sinh ở cột/diễn giải mới, không phải chuỗi vi phạm cũ còn nguyên.
- `cong-byte-co-rang-cong-claims-khong-dem-su-that`: **CHƯA VÁ** — ba đột biến một byte độc lập tại heading r358, heading r360 và phép trừ finding: claims đều rc0/ok=true, release đều rc2/failed chỉ CHANGELOG. Mã cổng ngoài tám tệp thay đổi; giữ nợ D.
- `cong-receipt-chua-dinh-nghia-cay-dang-merge`: **CHƯA VÁ** — `_neo_git` vẫn ghim ancestry vào HEAD trong khi `kiem` đọc tệp trên đĩa; năm cặp thử vẫn đổi kết quả theo HEAD. Giữ nợ D. Riêng câu mới “mọi lần merge chưa commit đều…” là lỗi E của bản chiếu trong message, ghi riêng; không biến nợ D thành lý do yêu cầu sửa mã cổng ở PR này.

Tổng đối chiếu bốn slug: **1 ĐÃ VÁ THẬT · 0 VÁ HỜ · 1 VÁ SINH LỖI MỚI · 2 CHƯA VÁ**.

## BẢN VÁ CÓ TỐI GIẢN KHÔNG

**Không đúng luật “chỉ sửa đúng câu sai, không viết thêm đoạn tổng kết”.** Git xác nhận patch được giao bằng byte `git diff f618e01 HEAD`, chỉ một commit mới, một cha; không có merge trong lượt này.

| tệp | thêm | bớt |
|---|---:|---:|
| CHANGELOG.md | 43 | 6 |
| RELEASE_MANIFEST.json | 5 | 5 |
| ops/land/pr491-r358-ghi-so-land-evidence.yaml | 9 | 4 |
| Tổng | **57** | **15** |

Manifest là cập nhật dẫn xuất. Trong văn bản có phần sửa cần thiết (nguồn run/event và bảng đính chính), nhưng cũng có diễn giải mới: CHANGELOG:1569–1586 thay 4 dòng bằng 17 dòng, thêm bảng lượt 14, thêm khối “4/5” và đoạn “Điều đáng nhớ…” tại 1613–1614. Đoạn cuối là tổng kết mới rõ ràng. Thông điệp commit mới còn tổng kết đối chiếu và khái quát nợ cổng; đây chính là nơi hai finding C/E phát sinh.

Số dòng `r360` theo cùng ranh giới heading: **263 tại 2c57e99 → 617 tại f618e01 → 654 tại d47ea59**. Lượt 14→15 tăng **37**, lượt 6→14 tăng **354**, lượt 6→15 tăng **391**. Lời giao việc gán 654/+391 cho lượt 14 bị lệch một lượt. Không quy sai số ở prompt thành lỗi mới của kho; ghi để không dùng tiền đề sai khi đánh giá độ tối giản.

Không đòi thêm một đoạn giải thích nào để đóng A. Phần B đã sửa chuỗi nhưng mở một phép kiểm kê mới sai; tối giản hay không không miễn phép đo đó. Việc dài hơn tự nó không được đếm thành finding thứ sáu.

## SOI HIỆN VẬT SẼ SỐNG TRONG KHO

**Land evidence:** đã đọc các trường và nhãn nguồn, không lấy việc parse YAML được làm chứng nhận nội dung.

| nhóm trường | tự đối chiếu / hạng nguồn |
|---|---|
| `p1_theo_luot: {1:3,2:0}`, `luot_cuoi` | Đếm heading hai verdict: **3/5/6** và **0/3/10**; khớp 14/13 finding, 0 P1 ở lượt 2 |
| `doi_chieu_luot_truoc` | Parse 14 dòng slug của verdict 2: **7/1/0/6**; ba slug P1 lượt 1 đều ĐÃ VÁ THẬT |
| `authorized_head_sha`, `reviewed_sha`, `khop_head_da_merge` | Cùng `2ec6171f7a2e21ae950633f9e328329a355f7a6d`, đúng cha2 `00e017a` |
| “land evidence thứ bảy” | `ls-tree` tại `00e017a`: **6** tệp trước khi thêm; khớp |
| provider/role/session/recorded_by/generation và chỉ thị chủ kho | Metadata do bên ghi tự khai; chỉ thị được nhận rõ là không có URL bền. KHÔNG ĐO ĐƯỢC danh tính backend/transcript độc lập |
| approval, merged_by, CI/jobs/timestamps, bot, sửa body/readback | Nhãn attestation GitHub đầu tệp và các giới hạn tại trường liên quan phủ nhóm này; thiếu response/raw body ⇒ KHÔNG ĐO ĐƯỢC sự kiện độc lập |
| `pre_merge_checks[0]` | rc, duration, worktree_sach, so_muc_ban được nhãn riêng là scalar launcher từ run.json ngoài kho. 0 P1/SHA tách đúng thành phép đo Git/verdict |
| các số cổng lịch sử | Chú thích nhận thiếu stdout gốc. Chạy lại trên SHA có thể kiểm tính tái lập, không chứng nhận lần chạy cũ; 146 hiện tại không thay cho 121 lịch sử |
| `bookkeeping` về edited | Đã sửa cả hai vế hạng nguồn/phạm vi event; không còn coi runtime là hiện vật offline |
| 11 còn sống lúc merge | 13 heading đo được, trừ 2 sửa body được thuật lại. Không có hiện vật xác nhận việc sửa trước merge; chỉ khớp số học có điều kiện |

Không tìm thấy trường runtime mới mất nhãn như lỗi A cũ trong land evidence. Không nâng metadata tự khai hoặc số GitHub được gắn nhãn thành xác thực thẩm quyền. YAML `ci.yml` ghi `pull_request` không types; `ops-thu-hoi-admission.yml` ghi `pull_request_target` với `[opened,reopened,synchronize,ready_for_review,edited]`. Đặc tả mặc định GitHub không nằm trong chính YAML và không được tra mạng; kết luận cấu hình không phải chứng cứ run đã chạy.

**Hai verdict nguyên văn:**

| tệp | byte | SHA-256 | lịch sử tới reviewed SHA |
|---|---:|---|---|
| pr491-review-1-codex-verdict.md | 35088 | 38d7fb2eac39da2bbdb2d76dc43c1f0f3f505498686ffa5ad5478a7c7491248c | 0 commit M |
| pr491-review-2-codex-verdict.md | 36958 | 14c726e5ccefb76e21b23901db48915edba871640bb1bd4b169d3961d9920468 | 0 commit M |

Băm/byte đều khớp receipt. `git log --diff-filter=M --format=%H -- <tệp>` rỗng cả hai; commit A duy nhất là `34e9d35be0fc52406e3659bfc24c388bf54262cd`; `git show <commit-A>:<tệp>` bằng byte HEAD. Không có sửa byte kể từ khi vào lịch sử này; không xác thực khâu trước khi nhập Git.

**Hai receipt v2:** suite **146/146, chạy 146, bỏ 0**, rc0; gọi riêng `t26_moi_bien_nhan_review_phai_khop_BAM_tep_no_tro_toi` và `t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc` cũng đạt. Tự kiểm thêm 4+5 ID đều có cùng verdict trên hàng bảng cảnh báo; hai hàng mục lục có verdict/receipt. Đối chiếu nội dung:

| lượt / caveat ID | kết quả |
|---|---|
| 1 / HEAD-LUOT-1-KHONG-PHAI-HEAD-DA-MERGE | ba4a258 khác 2ec6171; khớp header và cha merge |
| 1 / SAU-P3-KHONG-DEU-MOT-LOAI-5-cong-1 | Đúng 5 heading độ phủ và 1 giới hạn cổng trong sáu P3 |
| 1 / MODEL-YEU-CAU-khac-MODEL-DA-PHUC-VU | Khớp giới hạn verdict tự khai; không xác thực model backend |
| 1 / phan-cong-CAM-tu-soan-phan-chung | Khớp giới hạn phạm vi nguồn; không suy độ phủ đầy đủ |
| 2 / changes_requested-KHONG-phai-chua-dat-dieu-kien-dung | Verdict giữ changes_requested và nhận 0 P1 đạt điều kiện lịch sử; khớp |
| 2 / HET-P1-khong-phai-HET-FINDING-11-con-song-luc-merge | 13 lúc review; 11=13−2 khi nhận attestation hai sửa body. **KHÔNG ĐO ĐƯỢC số thật còn sống lúc merge** từ gói này |
| 2 / NAM-FINDING-BOT-la-duong-THU-BA-ba-cai-MOI | Receipt có 5 báo cáo, 3 mới/2 trùng; hai slug trùng nối được nguồn. Sự kiện bot/PR là thông tin điều phối bổ sung, không phải 5 heading trong verdict gốc |
| 2 / MODEL-YEU-CAU-khac-MODEL-DA-PHUC-VU | Khớp giới hạn nhận dạng của nguồn |
| 2 / phan-cong-CAM-tu-soan-phan-chung | Khớp giới hạn và việc nguồn thuật lại đột biến nội dung |

Chín caveat không mâu thuẫn với verdict trong các giới hạn trên. Hậu tố `11-con-song-luc-merge` không được xác thực chỉ vì t27 xanh; receipt `dieu_kien_dung_da_thoa.khong_suy_rong` ghi rõ phụ thuộc ATTESTATION, README có nhãn nguồn cho nhóm PR491. Không có chứng cứ bác hai sửa body để tự đổi 11 về 13.

## BẢNG ĐO

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| Exact HEAD/base | d47ea59 / 4b5184e | Full OID/tree đầu verdict; ancestry rc0 | Có |
| first-parent base..HEAD | thêm bản vá thuần | 23 commit; f618e01..HEAD chỉ d47ea59, một cha f618e01 | Có |
| delta toàn PR | numstat theo base không đổi | **8 tệp,+1808/−26**; numstat và diff bằng byte Git | Có |
| delta lượt 14→15 | patch thuần | **3 tệp,+57/−15**, patch bằng byte Git | Có |
| chiến thuật tối giản | không tổng kết mới | Có diễn giải/tổng kết mới, r360 tăng37 dòng | Không |
| r360 lượt 6→14 | 263→654,+391 | 263→617,+354; 654 thuộc lượt15 | Không, lời giao việc |
| năm số vi phạm trước commit | 6/1/4/2/11 | Cùng cây, HEAD=cha1: rc1 và 6/1/4/2/11 lỗi ancestry | Có |
| năm số sau commit | hết vi phạm | HEAD=merge: cả5 rc0, 0 vi phạm | Có |
| receipt thêm qua 5 merge | 6/2/4/2/11 | Bộ lọc A + đuôi .receipt.yaml: **6/1/4/2/11** | Không, F |
| phản chứng lần2 / 4 trên5 | 2 receipt mới / 1 lỗi | 1 receipt A, 1 receipt M / 1 lỗi; bằng nhau **5/5** trong mẫu | Không, F |
| đối chiếu lượt14 trong message mới | 1/0/0/1 | Nguồn **0/0/1/1** | Không, C |
| mọi merge chưa commit đều đỏ | lượng từ mọi | Merge pending f618e01←d47ea59: rc0, 0 lỗi, MERGE_HEAD tồn tại | Không, E |
| YAML/bản chiếu trong gói | từ cây | 6/6 bản chép YAML/README/workflow bằng byte HEAD | Có |
| năm slice mục r | cắt đúng heading | 5/5 bằng byte: r364=97,r362=646,r360=654,r359=120,r358=233 dòng | Có |
| 14 hàng bảng r360 | SHA/verdict/severity | Parse 14 verdict: **14/14 khớp**; cột đối chiếu chi tiết dưới | Có |
| hai verdict nguyên văn | byte/băm ghim | Cả hai khớp, 0 commit M, blob A=HEAD | Có |
| p1_theo_luot | 3 / 0 | 3 / 0 heading P1 | Có |
| 9 caveat và t26/t27 | đúng liên kết/băm | 9/9 hàng tương ứng; cả hai ca đạt | Có trong hợp đồng |
| ARTIFACTS.sha256 | toàn vẹn hiện vật | **3359/3359** băm khớp ở lần kiểm cuối | Có, không xác thực nguồn sinh |
| bảng khẳng định | 3482 dòng dữ liệu | Tái chạy 11 input bằng byte; 3482 dòng không rỗng,2145 có số;3506 dòng vật lý gồm khung | Có với đơn vị đã khai |
| ref snapshot | 329/329/329,lệch0 | Ba TSV bằng byte, local heads329 | Có cục bộ; máy chủ KHÔNG ĐO ĐƯỢC |
| thông điệp commit trích | từ Git range base..HEAD | Bằng byte `git log --format=%H%n%B%n--- 4b5184e..HEAD` | Có vận chuyển, không bảo đảm nội dung |
| bien_nhan_v2.py | 67 v2,tổng120,sạch | rc0;67+11 legacy+42 nợ=120;0 vi phạm,0 KHÔNG ĐO ĐƯỢC | Có |
| lease_publish_test.py | 146/146 | rc0;146/146,chạy146,bỏ0 | Có |
| release-verify --strict --json | xanh,180/180 | rc0,ok=true,180/180,hai hash match=true;failed/extra/required_missing/errors rỗng | Có |
| doc-claims-check --strict --json | xanh | rc0,ok=true,106 tệp,flags=[],370 advisory | Có trong hợp đồng |
| doctrine-scan --root . | sạch | rc0,7 tệp,0 chỗ chép doctrine | Có |
| adr-song --root . | sạch | rc0,46 ADR/46 hàng,khớp1–1,tha trạng thái0016 | Có |
| nợ claims | cổng không kiểm các số này | 3/3 mutant qua claims;3/3 release đỏ chỉ CHANGELOG | Nợ D còn |
| CI/approval thật và số11 lúc merge | thuật lại | Thiếu raw response/body/run; không mạng | KHÔNG ĐO ĐƯỢC |
| kho review giữ nguyên | read-only | HEAD và status trước/sau không đổi | Có |

Lần kiểm băm ban đầu có một lệch do reviewer ghi nhầm bản tổng hợp tài liệu vào helper `protocol-read.txt` có sẵn trong gói. Đã tìm lại đúng byte gốc từ `docs/PROTOCOL_DA_PHIEN.md`, khôi phục và kiểm băm toàn bộ lại 3359/3359. Không quy lệch do reviewer gây ra thành finding của PR; không có tệp trong `cay-kho/` bị sửa.

**Từng ô đối chiếu bảng r360:** chỉ đếm dòng slug/trạng thái trong phần ĐỐI CHIẾU của từng verdict, không đếm tổng văn xuôi hay bảng khác. Thứ tự số: ĐÃ VÁ THẬT / VÁ HỜ / VÁ SINH LỖI MỚI / CHƯA VÁ.

| lượt | tự parse | tổng slug | ô ở r360 |
|---|---|---:|---|
| 1 | không có đối chiếu | — | —; đúng |
| 2 | 0/6/0/11 | 17 | khớp |
| 3 | 7/3/0/10 | 20 | khớp |
| 4 | 1/2/0/14 | 17 | khớp |
| 5 | 3/0/1/13 | 17 | khớp |
| 6 | 11/2/0/1 | 14 | khớp |
| 7 | 4/3/2/1 | 10 | khớp |
| 8 | 7/0/1/1 | 9 | khớp |
| 9 | 7/2/0/1 | 10 | khớp |
| 10 | 3/1/0/1 | 5 | khớp |
| 11 | 2/0/0/1 | 3 | khớp |
| 12 | 1/0/0/1 | 2 | khớp |
| 13 | 2/0/0/1 | 3 | khớp |
| 14 | **0/0/1/1** | 2 | “điền ở lượt sau”; chưa khai số, không sai |

Hàng5 theo dõi cả slug đã đóng nên tổng17 không đồng nghĩa17 finding còn sống. Không ô số đã điền nào lệch. **Chỗ lệch lượt14 nằm trong message commit mới**, không phải ô hẹn điền của CHANGELOG.

### phan-chung-bon-tren-nam-dem-receipt-sua-thanh-them  [P3]  Bảng đính chính ghi hai receipt mới ở merge chỉ thêm một
LỚP: F
TỆP/DÒNG: `CHANGELOG.md:1600`, :1609–1611; message `d47ea5949366c8d470ef0b1538e0fafa725bd35e`, bản trích `thong-diep-commit.txt:13`–15.
VẤN ĐỀ: Cột “biên nhận thêm” ghi2 ở dd4a3ae rồi dùng làm phản chứng cho mẫu5 ca. `git diff --name-status dd4a3ae^1 dd4a3ae -- ops/reviews/` cho receipt lượt7 là A, receipt lượt6 là M. Chỉ **1 receipt thêm**; hai là số receipt bị đụng tới nếu tính A+M. Lỗi ancestry chỉ thuộc lượt7. Chuỗi receipt mới thật là6/1/4/2/11, khớp chuỗi lỗi cả5 ca; kết luận4/5 sai. Chọn F vì phép kiểm kê không giữ phân biệt đơn vị “thêm” với “thay đổi”.
CÙNG LỚP CÒN Ở ĐÂU: câu phản chứng/4/5 trong cùng mục; thông điệp commit mới; muc-r360/BANG là bản chép, không đếm riêng. Không kết luận đẳng thức đúng cho mọi merge chỉ vì năm ca khớp.
ĐÃ THỬ VÁ: không sửa kho. Sửa đúng ô2→1 và rút câu phản chứng4/5; giữ giới hạn “năm ca đã đo không chứng minh quy luật phổ quát”. Với message bất biến, đính chính ngắn neo d47ea59 ở hồ sơ sống là đủ, không cần viết lại lịch sử hay thêm tự sự.
ĐÃ THỬ NGHIỆM: `review15-evidence/merges.py` chạy5 cây/10 lần cổng, lọc receipt A theo cha1→merge; rc/lỗi trước=(1,6),(1,1),(1,4),(1,2),(1,11), sau cả5=(0,0). `extra.json` giữ diff A/M. Ca khóa: mỗi hàng bảng phải khớp danh sách A, receipt M không được cộng; rủi ro vá là đổi cả chuỗi lỗi đúng hoặc nâng5/5 thành luật mọi đầu vào.
ĐỘ TIN: cao

### doi-chieu-luot14-trong-message-doi-sinh-loi-thanh-va-that  [P3]  Message mới gán trạng thái trái verdict lượt14
LỚP: C
TỆP/DÒNG: message commit `d47ea5949366c8d470ef0b1538e0fafa725bd35e`, `thong-diep-commit.txt:5`; nguồn `VERDICT-LUOT-14.md:14`–16.
VẤN ĐỀ: “Đối chiếu2 slug lượt13” ghi1 ĐÃ VÁ THẬT,0 VÁ SINH LỖI MỚI,1 CHƯA VÁ. Nguồn gán `chieu-edited-mat-pham-vi-ci-yml` là **VÁ SINH LỖI MỚI**, slug D là CHƯA VÁ: đúng phải **0/0/1/1**. Việc lõi lỗi cũ đã đóng không cho bản chiếu thay nhãn reviewer đã chọn; nguồn đã nói rõ điều đó ngay trong dòng slug.
CÙNG LỚP CÒN Ở ĐÂU: BANG trích message; ô14 của r360 chưa điền nên không có nhãn sai ở đó. Phần narrative message tự nói bản vá cũ hỏng ngược càng cho thấy cần giữ nhãn sinh lỗi.
ĐÃ THỬ VÁ: không. Đính chính ngắn dòng thống kê neo message d47ea59, dùng nguyên trạng thái nguồn. Không cần điền thêm ô14 hay kéo dài bảng để sửa lỗi này.
ĐÃ THỬ NGHIỆM: parser `measure.py` giới hạn phần ĐỐI CHIẾU, cho2 dòng và0/0/1/1; trích message bằng Git byte-exact. Ca khóa: so bốn số theo thứ tự cố định với hai dòng nguồn; rủi ro vá là đếm câu giải thích “đã sửa thật” như một trạng thái độc lập hoặc gộp trạng thái lượt15 vào lượt14.
ĐỘ TIN: cao

### no-cong-bi-khai-thanh-moi-merge-pending-deu-do  [P3]  Message khái quát năm ca thành mọi merge chưa commit
LỚP: E
TỆP/DÒNG: message commit `d47ea5949366c8d470ef0b1538e0fafa725bd35e`, `thong-diep-commit.txt:36`–37.
VẤN ĐỀ: Câu “nên **mọi lần merge chưa commit đều báo vi phạm giả**” vượt điều kiện thực: phải có receipt trên đĩa neo commit chưa thuộc HEAD và qua các kiểm trước đó. Khi không thêm neo ngoài HEAD, pending merge có thể xanh. Đây là lỗi kết luận hồ sơ, khác nợ D của hợp đồng cổng.
CÙNG LỚP CÒN Ở ĐÂU: BANG trích message. Finding D lượt14 đã giới hạn rõ các ca/điều kiện; không dùng nó chứng nhận chữ “mọi”.
ĐÃ THỬ VÁ: không. Rút “mọi”, giới hạn câu vào các merge đã đo có receipt neo chưa thuộc HEAD; đính chính ngắn có neo d47ea59. Không mở mã cổng để làm đúng một lời khái quát sai.
ĐÃ THỬ NGHIỆM: trên `review15-merge/`, checkout f618e01 rồi `git merge --no-commit --no-ff d47ea59`; HEAD=f618e01, MERGE_HEAD=d47ea59, tree=0483b522… đúng tree reviewed. Chạy `python3 -B ops/bien_nhan_v2.py`: **rc0,67 v2,tổng120,0 vi phạm,0 KHÔNG ĐO ĐƯỢC**. Có MERGE_HEAD thật, chưa commit; không cần dựng payload. Kết quả trong pending-clean.json/log. Ca khóa: giữ cả ca pending xanh này và5 ca ancestry đỏ; rủi ro vá là đảo thành “mọi merge pending đều xanh” hoặc bỏ kiểm ancestry.
ĐỘ TIN: cao

### cong-byte-co-rang-cong-claims-khong-dem-su-that  [P3]  Claims vẫn không bắt ba sai số nội dung
LỚP: D
TỆP/DÒNG: `scripts/tl_core/workflow.py:1163`, :1430; ca tại `CHANGELOG.md:1805`, :1031, :1350.
VẤN ĐỀ: Release kiểm toàn vẹn byte; claims không bác1016→1017,5→6 và13−2=11→12. Nợ ngoài write set, không chặn approve một mình.
CÙNG LỚP CÒN Ở ĐÂU: cả ba nhóm đại lượng; không suy mọi khẳng định đều lọt.
ĐÃ THỬ VÁ: không; giữ cho packet mã cổng. Hướng: hợp đồng đại lượng/nguồn đếm có cấu trúc, phân biệt trích lịch sử với khẳng định hiện hành, không hardcode ba chuỗi.
ĐÃ THỬ NGHIỆM: `probes.py` tạo3 mutant độc lập, mỗi mutant giữ960029 byte; cả3 claims rc0/ok=true; cả3 release rc2/failed chỉ CHANGELOG. Control xanh trong gates.json. Ca khóa: ba mutant đỏ ở cổng nội dung, control xanh; rủi ro vá là regex kết tội cả câu trích để đính chính.
ĐỘ TIN: cao

### cong-receipt-chua-dinh-nghia-cay-dang-merge  [P3]  Cổng đọc tệp đang merge nhưng ancestry vẫn theo HEAD
LỚP: D
TỆP/DÒNG: `ops/bien_nhan_v2.py:808`–824 (`_neo_git`), :861 (`kiem`).
VẤN ĐỀ: Dữ liệu đĩa và HEAD có thể không cùng candidate khi chưa commit. Năm cây lịch sử cho kết quả khác theo HEAD dù nội dung không đổi. Đây là nợ giao diện cho trạng thái dở; ancestry theo HEAD của commit đã chốt không tự nó sai. Ngoài write set, không chặn approve một mình.
CÙNG LỚP CÒN Ở ĐÂU: năm merge đã thử; không phải mọi merge pending, như phản chứng E phía trên.
ĐÃ THỬ VÁ: không; packet riêng cần định nghĩa candidate commit với tập cha, ràng buộc nó với nội dung đang kiểm, hoặc báo chưa đo được cho trạng thái chưa đủ hợp đồng. Tree đơn lẻ không có ancestry; không chỉ thay HEAD bằng tree hash.
ĐÃ THỬ NGHIỆM: `merges.py` giữ mỗi cây lịch sử, thay HEAD cha1/merge trên bản sao:6/1/4/2/11→0/0/0/0/0. Đây là A/B cây/HEAD, không giả nhận đã tái dựng toàn bộ5 thao tác merge lịch sử. Ca khóa: cùng candidate có kết quả nhất quán trước/sau commit, neo nhánh không liên quan vẫn bị chặn, thiếu object vẫn chưa đo được; rủi ro vá là mở tập tổ tiên quá mức. Không cần sửa nợ này để đóng3 lỗi hồ sơ phía trên.
ĐỘ TIN: cao về hành vi; vừa về giao diện kế nhiệm
