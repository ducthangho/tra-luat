import json
from pathlib import Path

B = Path(__file__).resolve().parents[1]
O = B / 'do-review12'

text = '''# VERDICT — cross-review khác nền, LƯỢT 12, PR #468

verdict: dang-do
reviewed_sha: 02b0b86bf64a89b561a75ff060164332792fb73d

Kết luận nội dung: **changes_requested — 2 P1, 2 P2, 0 P3**. Lượt 11: **2 ĐÃ VÁ THẬT, 1 CHƯA VÁ**; P2 manifest của lượt 10 cũng **ĐÃ VÁ THẬT**. Một P1 là trạng thái chồng lease đã biết; P1 còn lại thuộc **bundle thiếu ref**, không phải lỗi mới trong mã lease.

**Ngoài P1 chờ 14:30:07Z, còn 3 finding: 1 P1 về năng lực đo của bundle và 2 P2 về hồ sơ hai phiên.** Chưa đủ điều kiện để lượt kế chỉ đọc lại trạng thái sau hạn rồi approve.

Reviewer: Codex / OpenAI, phiên API độc lập, shell cục bộ; transport đầu ra: tệp sandbox. Đã tạo VERDICT ngay lúc bắt đầu và ghi dần kết luận. Phạm vi đóng theo PROMPT: không mạng, không sửa checkout, không commit/push lên repository, không đăng GitHub/ghi receipt hay state. Các đường `ops/...` dưới đây tính từ `cay-kho/`; bằng chứng mới nằm trong `do-review12/`. Không gọi agent khác. Các kho giả do selftest tạo nằm trong thư mục tạm của sandbox, không phải nhánh executor.

## ĐỐI CHIẾU LƯỢT TRƯỚC

- `bia-mo-mot-ref-khong-thu-hoi-moi-ban` [P1]: **CHƯA VÁ — CHƯA VÁ VỀ MÁY** lúc **2026-09-07T13:15:45.214989Z**. Gọi `_quet_lease_toan_kho(..., doi_chieu_ref=False)` thật trên mirror: 90 cặp `(blob,path)`; registry có **2** người giữ (#456 và exec-1r4), ci.yml có **1**. Blob #456 chưa bia mộ trên `origin/master`: `8b2103c06687546379a17f6deafc97f1fe0173fd`. Bốn cạnh #456 → r1 → r2 → r3 → r4 đều đúng hai chiều. Mô phỏng cùng snapshot tại 14:30:06/07/08Z cho registry **2/1/1**, ci.yml **1/1/1**; mô hình đặt bia mộ trên mọi bản #456 trong snapshot cho **1/1**. **Đây chưa phải readback sau hạn hoặc quét đủ máy chủ**: mirror chỉ có 3 tên nhánh, xem finding bundle riêng. Issue #463 mục “Cập nhật 13:01Z” khai đúng mức về trạng thái máy: thu hồi bằng comment không tự đổi kết quả quét YAML, vẫn 2 người giữ, chưa bắt tay, phải đo lại. Không xác minh được comment/thẩm quyền hoặc phép fetch 302/302 từ sandbox.

- `bien-do-khac-head-khong-phai-nhieu-runner` [P2]: **ĐÃ VÁ THẬT**. Parse YAML r4 trước/sau c43347d: chỉ **1** lá `/viec_trong_lease/4` đổi, tập **52** khóa không đổi. Mục billing gọi đúng đối chiếu lịch sử cùng tree nhưng khác event/lane; nói không tách được nhiễu runner và không nới A1/A5. Ngưỡng 135,00, spec/write-set hash, authority, mốc và chuỗi thay thế giữ nguyên; spec A1≤25,00/A5≤135,00 không đổi. Header mô tả phạm vi sửa trung thực. Chữ “lượt 10” là tên được giao ban đầu cho reviewer sau được vận chuyển thành lượt 11, đã giải thích ở DOC-MANIFEST; `11:5xZ` chỉ là ghi chú thời điểm sửa, không phải thời điểm commit đã tự đo. `lease_publish.py check` r4 **rc=0**, có “ĐĂNG ĐƯỢC”; không suy đó là A9 đạt.

- `manifest-luot8-liet-ke-hien-vat-khong-duoc-giao` [P2 lượt 11 **và** P2 lượt 10]: **ĐÃ VÁ THẬT**, giữ nguyên slug chung. Chạy `sha256sum -c`: gói lượt 8 **69/69**, lượt 9/artifact-repair **69/69**, gói lượt 11 **128/128**, đều **rc=0**. Lượt 11 được dựng bằng tệp thường theo ánh xạ DOC-MANIFEST (`VERDICT.md` → verdict11; `do-review10/` → gói11), không sửa manifest. 19 tệp rig đã được thêm tại **17c6901**; 4c18cb2 không thay chúng. Sai lời kể về commit sửa được ghi riêng bên dưới, không mở lại lỗi toàn vẹn đã đóng.

## BẢNG ĐO

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| HEAD / tree / trạng thái | exact reviewed_sha; sạch | HEAD `02b0b86bf64a89b561a75ff060164332792fb73d`; tree `cee08e8eeecbb581c36a2058153b43dc29724b0a`; status rỗng | có |
| Môi trường git | abbrev=7, không shallow | 7; false; origin HTTPS GitHub, không gọi mạng | có |
| Diff từ c43347d | patch và numstat được giao | khớp byte; 267 tệp, +75698/−1, 4 commit, 0 path ngoài ops | có |
| Full diff so origin/master | patch và numstat được giao | khớp byte; 613 tệp, +165904/−0, 0 path ngoài ops | có |
| Spec/runtime đổi sau c43347d | thuần hồ sơ ops | 0 spec; 0 path trong .github/.claude/scripts | có |
| Năng lực tái đo toàn ref | EVIDENCE: kho nguồn 302/302; master + 9 nhánh giữ blob cũ | bare có 3 head; checkout 1 local branch, 3 remote branch name + 1 symbolic HEAD; chỉ 2 tên ref được giao giữ blob cũ | **không đủ nguồn để xác minh lời khai kho nguồn** |
| Danh sách lịch sử lượt 10 | 10 tên nhánh giữ blob cũ, không tính HEAD | JSON lịch sử có 10; 9 tên trong đó không có trong mirror này | có về byte lịch sử; không phải readback hiện hành |
| Snapshot 13:15:45.214989Z | registry=2; ci.yml=1 | 90 cặp blob/path, 2/1 | có trên tập ref được giao |
| Chuỗi thay thế | #456→r1→r2→r3→r4 | 4/4 cạnh hai chiều đúng | có |
| Mô phỏng hết hạn | #456 hết 14:30:07Z | 14:30:06/07/08Z: registry 2/1/1, ci.yml 1/1/1 | có trong mô hình |
| Mô hình bia mộ mọi bản #456 | hướng khắc phục | registry 2→1; ci.yml vẫn 1 | có trong mô hình; không phải sửa ref thật |
| YAML billing r4 | một mục văn đổi | 1 lá đổi; 52/52 khóa giữ tập; bản chiếu bằng byte | có |
| Lease r4 | 1440 phút, 2 path, 3 neo d28c4b1 | 10:17:12Z 07-09 → 10:17:12Z 08-09; 1440 phút; 2 path; 3 neo đúng | có |
| Hash write set r4 | `0f7b869da648e9b21023e461925efd0d45bca58fb308a8fcc82bc55ad9f66ef0` | tự tính đúng cùng hash | có |
| Bốn spec/hash/alias/blob Issue/bản chiếu | #463 r4; #464–466 r1 | 4/4 khớp; GATE/LO neo 1a33030, 2A/2B neo b743f17 | có |
| Null trong lease / bản chiếu GATE | GATE cấp thật, 3 nháp chưa cấp | GATE 0 null; mỗi nháp 5 null; 4/4 lease GATE chiếu bằng byte | có |
| Manifest lượt 8 | 69/69 | 69/69, rc0, toàn tệp thường | có |
| Manifest lượt 9/artifact-repair | 69/69; thêm 19 rig | 69/69, rc0; 19/19 thêm tại17c6901 | có |
| Manifest lượt 11 | 128/128, theo DOC-MANIFEST | 128/128, rc0 sau ánh xạ đường đúng | có |
| Tệp trong hai gói | hiện vật lượt10/11 | 111/129 tệp thường; 0/0 symlink; gói11 gồm 127 hiện vật + ARTIFACTS + DOC-MANIFEST, verdict nằm ngoài | đo bổ sung |
| Receipt/verdict lượt 10 | 25294 B; SHA256 khai | 25294 B; `5e22088b996a4b6e4f564159703ed311bba2c0cf6b137cb9a0614bc9c7476672` | có |
| Receipt/verdict lượt 11 | 22385 B; SHA256 khai | 22385 B; `852ba0df07c83a8fc2f2bd02f6658157156e96944273139e6cc8d2aa227cbffd` | có |
| Hai evidence_url | commit đầu tiên chứa verdict; SHA được review là tổ tiên | 2/2 blob khớp; 2/2 đúng commit đầu tiên (17c6901/4c18cb2); 2/2 ancestry; bản chiếu receipt/verdict 4/4 khớp | có |
| Reviewer launcher lượt 10 | model/thread/prompt/thời lượng/rc/stdout KHÔNG ĐO ĐƯỢC | 0 nguồn run.json/prompt/session gốc trong gói; commit có lời tự khai model/rc, không có attestation máy | khai giới hạn phù hợp |
| Phiên vận chuyển lượt 10 | “không rõ session URL” | commit17c6901 có `Claude-Session: https://claude.ai/code/session_0186nh13XYsStVs1usBCsx5Y` | **không**; có nguồn tự khai để trích |
| Khung giờ lượt 10 | receipt: 11:35–11:50Z | gói lưu launch11:24:25; số đo11:26/11:29; final-check11:47:28.896723Z | **không**; chưa biết thời lượng launcher chính xác |
| Attestation lượt 11 | run a25fea88; thread01a07ba6-71b9-7f80-9deb-9ef6616243b8; model6/6;939.246s;rc0;552459B | schema chấp nhận; 0 run/session/stdout gốc trong gói để đo độc lập | **KHÔNG ĐO ĐƯỢC**, không nhận schema là bằng chứng sự thật |
| Prompt lượt 11 | SHA256 `9d0caf1fa2f106d0def639d6df9e07cf8bcf3df30e42d32588c62df3a255d7ee` | không có prompt nguyên bản lượt11 để băm lại | **KHÔNG ĐO ĐƯỢC** |
| Làm tròn thời lượng11 / final-check | 939.246→939.2/939; trước hạn | làm tròn nhất quán; gói final-check11:50:17.131690Z | có về số ghi trong hồ sơ, không đo lại runtime |
| Commit sửa 19 tệp | receipt11/GHI-NHAN: cùng commit chứa verdict11 | 17c6901 thêm19; 4c18cb2 thay0 tệp gói rig cũ | **không** |
| Chênh vận chuyển | GHI-NHAN: trước5giây, dẫn DOC-MANIFEST | DOC-MANIFEST không có số5; commit11:50:33→12:17:11 cách1598s; không có log push | **KHÔNG ĐO ĐƯỢC chênh push** |
| Thử sửa metadata trong bộ nhớ | không đổi assurance/identity reviewer | receipt10:2 neo,2 trường prose đổi; receipt11:2 neo,1 trường ghi chú đổi; GHI-NHAN:2 neo; băm/verdict/neo/assurance nguyên | có trong thử nghiệm |
| Issue463 “Cập nhật13:01Z” | comment12:57:06Z;6/6 nghiệm thu;302ref;2/1;chưa init | 2/1 tự tái lập trên tập con; lời phân biệt comment/YAML đúng; comment,6/6,302ref/comm không có nguồn readback trực tiếp | nhất quán về trạng thái máy; phần còn lại **KHÔNG ĐO ĐƯỢC** |
| lease_publish check r4 | rc0 | rc0, “ĐĂNG ĐƯỢC”, tự khai không chạy 2 lớp GitHub | có; không thay A9 |
| lease_publish_test | 121/121 | rc0;121/121;đã chạy121,bỏ qua0 | có |
| bien_nhan_v2 | 26 v2 ĐẠT | rc0;26v2;11/11legacy;42nợ;79tổng;0vi phạm,0không đo được | có về schema/băm/neo |
| doctrine / ADR | sạch;46/46 | rc0;7tệp,0chép / rc0;46ADR,46dòng;1ngoại lệ trạng thái0016 theo cổng | có |
| doc-claims strict | ok:true | rc0,ok:true;106tệp;367advisory,0cờ cứng;10lớp chạy,0lớp bỏ qua trong tập được bật | có; root không có ops |
| EOL toàn index | ok:true | rc0,ok:true;1453quét,1431kiểm,22bỏ qua policy,0vi phạm | có |

Các số hash/giá trị đầy đủ và lệnh cụ thể nằm trong `snapshot.json`, `billing.json`, `lease-supplement.json`, `artifacts.json`, `standards.json`, `ref-coverage.json`, `prose-models.json`; không dùng log lịch sử để khai test mới chạy. Thời gian dưới đây là của **cổng reviewer tự chạy**, không phải thời lượng phiên Codex lịch sử.

| lệnh/cổng tự chạy trong cay-kho | rc | giây | stdout/stderr byte |
|---|---:|---:|---:|
__GATE_ROWS__

### bia-mo-mot-ref-khong-thu-hoi-moi-ban  [P1]  #456 vẫn giữ registry cùng r4 trước hạn

TỆP/DÒNG: `ops/specs/GATE-TACH-JOB-CAT-CHI-PHI.md:579` (A9); `ops/lease_publish.py:547`, `:570`, `:935`; bản #456 trên `origin/master`, blob `8b2103c06687546379a17f6deafc97f1fe0173fd`; `ops/issues/463-GATE-TACH-JOB-CAT-CHI-PHI.md:126–131`.

VẤN ĐỀ: Số người giữ tại 13:15:45.214989Z là registry2/ci.yml1. Comment thu hồi được hồ sơ dẫn không phải đầu vào của scanner; một bản có bia mộ không truyền trạng thái sang blob cũ trên ref khác. A9 chưa đạt. Hồ sơ mới **không khai đã đóng** và vẫn ghi chưa bắt tay; không có bằng chứng executor đã thi công runtime trái A9. Hết hạn có thể kết thúc trạng thái chồng hiện hành, không hồi tố hợp lệ hóa các lần cấp r2/r3/r4 trước đó.

ĐÃ THỬ VÁ: Có, chỉ trong bộ nhớ: đặt bia mộ hai chiều cho mọi bản #456 trong snapshot → registry1/ci.yml1. Giữ nguyên ref/dữ liệu, đổi giờ sang14:30:07Z cũng cho1/1. Hướng xử lý: readback đủ ref sau hạn hoặc chủ kho hoàn tất đường thu hồi bằng dữ liệu mà scanner đọc; không tự sửa/cấp lại lease. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: `python3 -B do-review12/measure.py snapshot` rc0; dùng hàm sản phẩm `_quet_lease_toan_kho`, `_phan_loai_lease`, `_bia_mo_doi_xung`, `_lease_cham_duong`. Đo thật90cặp,4/4cạnh; ba mốc mô phỏng cho2/1/1 và1/1/1; `check` r4 rc0. Không gọi CLI có readback mạng, không giả GitHub. Sau14:30:07Z thực tế và toàn bộ302ref: **KHÔNG ĐO ĐƯỢC** trong lượt này.

ĐỘ TIN: cao về bằng chứng dương chồng lease và hành vi thời gian; không chứng nhận trạng thái toàn máy chủ.

### mirror-thieu-ref-khong-du-do-a9  [P1]  Bundle không giao tập ref để tái đo khẳng định 302 ref

TỆP/DÒNG: `EVIDENCE.md:13–15`; `PROMPT.md:4`; `tai-lieu/PROTOCOL-trich-8-12-13.md` §8, đoạn “Reviewer phải được cấp NĂNG LỰC ĐO LẠI HIỆN TRẠNG”; dữ liệu `do-review12/cay-kho-refs.tsv`, `kho-git-refs.tsv`.

VẤN ĐỀ: EVIDENCE dẫn phép đo quyết định A9 trên302/302ref và blob cũ trênmaster+9nhánh, nhưng cả bare mirror và checkout chỉ mang3tên nhánh. Checkout đủ nội dung/lịch sử tại HEAD và không shallow **không đồng nghĩa đủ ref**. Giới hạn này không được tự khai; câu “GitHub trực tiếp không đo được” chưa nói rằng ngay snapshot ref kho nguồn cũng không được giao đủ để tái đo. Đây là lỗi năng lực đo của bundle theo §8. Tập con vẫn đủ chứng minh có hai người giữ trước hạn, nhưng không đủ kết luận toàn kho chỉ còn một sau hạn. Không khẳng định phép đo kho nguồn13:01Z sai hoặc máy chủ hiện chỉ có3nhánh.

ĐÃ THỬ VÁ: Không thể phục dựng snapshot302ref hiện hành từ nguồn được giao. Đã kiểm nguồn bare dự phòng: cũng chỉ3head; JSON lịch sử lượt10 biết10tên giữ blob cũ,9tên không hiện diện trong mirror, nhưng không được biến tên/lịch sử cũ thành ref hiện hành. Hướng sửa bundle: bên điều phối xuất lại đầy đủ tên+OID tại giờ readback, clone đủ các ref vào sandbox, kèm phép so tập tên/OID nguồn→mirror và tự khai phần chưa đo; sau đó quét lại. Không cần thay logic lease hay sửa nhánh PR chỉ để chữa môi trường reviewer. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: `python3 -B do-review12/prose_models.py` rc0 có phép kiểm coverage; `git -C cay-kho for-each-ref --format='%(refname)\t%(objectname)\t%(symref)'` và phép tương tự với `kho.git`. Chuẩn hóa bỏ symbolic HEAD: checkout1local+3remote, bare3head; tập tên khớp nhau nhưng không tái lập được302ref đã khai. Không có mạng/nguồn snapshot mới để thử sửa đầy đủ.

ĐỘ TIN: cao về phần được giao và giới hạn suy luận; số ref GitHub thực tế **KHÔNG ĐO ĐƯỢC**.

### bien-nhan-luot10-bo-sot-va-tron-dau-vet-phien  [P2]  Biên nhận bỏ sót URL vận chuyển và chép khung giờ của lượt khác

TỆP/DÒNG: `ops/reviews/pr468-hoso-4-packet-review-10-codex-verdict.receipt.yaml:57`, `:69`; nguồn đối chứng là trailer `Claude-Session` của17c6901 và `ops/reviews/pr468-hoso-4-packet-review-10-codex/do-review10/final-check.json:26`.

VẤN ĐỀ: “không rõ session URL” bỏ sót nguồn ngay trong commit17c6901: `https://claude.ai/code/session_0186nh13XYsStVs1usBCsx5Y`. Đây là **URL phiên vận chuyển tự khai trong commit**, chưa phải danh tính model reviewer được xác thực. Receipt còn nói lượt10 chạy11:35–11:50Z, trong khi chính gói10 lưu log bắt đầu11:24:25 và có các phép đo11:26/11:29 trước khung ấy. Phải trích đúng dấu vết của từng phiên. `KHONG_do_duoc` cho thread/run/prompt/runtime chính xác và `review_deferred` vẫn hợp lý vì không có attestation máy; finding này **không yêu cầu nâng assurance** từ một URL Claude hoặc lời tự khai model/rc trong commit.

ĐÃ THỬ VÁ: Có, thay hai mỏ neo trong bộ nhớ: dẫn session URL với nhãn nguồn commit, ghi các mốc đã lưu và giữ thời lượng launcher là chưa đo được. Sau parse, chỉ hai trường prose `github_submitter_identity` và `KHONG_do_duoc` đổi; `model_reviewer_identity`, assurance, verdict, hash, reviewed_sha, evidence_url và anchor nguyên trạng. Không xuất bản vá receipt/authority. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: `python3 -B do-review12/standards.py` và `python3 -B do-review12/prose_models.py`, đều rc0;2/2mỏ neo duy nhất. `git show -s --format=%B 17c6901` có trailer nguồn. Cổng receipt hiện vẫn rc0: lỗi sự thật/provenance này không được cổng cấu trúc kiểm. Không lấy khoảng launch→final-check làm thời lượng toàn phiên.

ĐỘ TIN: cao về byte và mốc được lưu; quyền truy cập/độc lập của URL phiên chưa xác minh trực tiếp.

### ghi-nhan-luot11-gan-sai-commit-va-moc-van-chuyen  [P2]  Hồ sơ mới gán sai commit sửa gói và thiếu nguồn cho “5 giây”

TỆP/DÒNG: `ops/reviews/pr468-hoso-4-packet-review-11-codex-verdict.receipt.yaml:6–7`, `:28`; `ops/reviews/GHI-NHAN-CROSS-REVIEW-LUOT5-KHONG-HOAN-TAT.md:259`, `:264`; đối chứng `ops/reviews/README.md:269` và commit4c18cb2.

VẤN ĐỀ: Receipt và GHI-NHAN nói cả hai P2 được vá ở commit chứa verdict11 (4c18cb2). Git cho thấy19tệp rig đã được thêm ở17c6901;4c18cb2 chỉ sửa billing và đo lại gói đã đủ, không thay tệp nào của rig gói9. Chính README mới và body commit4c18cb2 ghi đúng điều đó. Do vậy các bản ghi mới tự mâu thuẫn về nguồn bản sửa. Câu lượt10 “lên nhánh trước5giây” dẫn DOC-MANIFEST cũng không có số5 hoặc log push trong nguồn ấy. Hai commit cách1598giây theo timestamp tác giả/committer; **không được dùng chênh commit làm chênh push**. Thứ xác minh được là thứ tự commit và nội dung từng commit.

ĐÃ THỬ VÁ: Có, thử sửa hai mỏ neo receipt11 trong bộ nhớ: ghi19tệp được bổ sung tại17c6901, billing tại4c18cb2; chỉ trường YAML ghi chú `evidence_url_ghi_chu` thay đổi, mọi identity/assurance/verdict/neo giữ nguyên. GHI-NHAN có hai mỏ neo duy nhất để đồng bộ nguồn sửa và bỏ con số push chưa có bằng chứng hoặc bổ sung log thật. Giữ nguyên byte verdict lịch sử và ghi nhận hai phiên độc lập. Không xuất bản vá authority. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: `git diff-tree --no-commit-id --name-status -r 17c6901 -- ops/reviews/pr468-hoso-4-packet-review-9-codex/artifact-repair/rig` →19dòng thêm; cùng lệnh với4c18cb2 →0dòng. `standards.py`/`prose_models.py` rc0; manifest gói9 vẫn69/69rc0. `git show -s --format=fuller` cho11:50:33Z và12:17:11Z. Không có chứng cứ thời điểm publish để định lượng khoảng “lên nhánh”.

ĐỘ TIN: cao về commit sửa; chỉ xác nhận thiếu bằng chứng cho chênh push, không khẳng định hai lần push phải cách1598giây.

## STANDARDS — KẾT LUẬN VÀ GIỚI HẠN

Hai hàng README dẫn đúng verdict/receipt/gói, đúng SHA được review, số byte và số finding từng phiên (lượt10:1P1+1P2; lượt11:1P1+2P2). DOC-MANIFEST giải thích đổi tên lượt11, manifest bảo toàn byte. Sự cố hai phiên được tự khai, không gộp thành một lượt; hai trailer Claude-Session khác nhau hỗ trợ lời khai hai phiên vận chuyển, không chứng minh danh tính Codex. Các lỗi còn lại về nguồn/mốc nằm trong hai P2 trên.

Receipt10 không có run/session/prompt gốc để chứng minh reviewer identity. Giữ `review_deferred` ở bản dựng lại là thận trọng đúng mức, không xóa sự tồn tại của verdict `changes_requested`. Receipt11 có đủ trường attestation và schema/băm/neo đúng, nhưng thread, prompt hash,939.246s,552459byte và6/6 mục model chỉ có lời khai của bên vận chuyển: **KHÔNG ĐO ĐƯỢC độc lập** vì không giao raw launcher/session/prompt. Không kết luận những số ấy bịa, cũng không nhận chúng là đã tự tái đo. `cross_approved` trong receipt là nhãn assurance được khai cho lượt lịch sử, không phải verdict approve của head hiện tại hay merge authorization.

Issue463 mục13:01Z phân biệt đúng quyết định thu hồi bằng comment với trạng thái máy chưa đạt A9. Mốc12:57:06Z, quyền comment,6/6 nghiệm thu#456,302/302ref,`comm -23` và CI run34121309671/34125520827: không có readback máy chủ trong phạm vi này. Không dùng cổng local xanh để chứng nhận GitHub CI hay branch protection. EVIDENCE tự khai chưa chạy packet_loop_test/ci_dang_ky toàn bộ; lượt này cũng không chạy các suite runtime dài vì diff sauc43347d không sửa mã runtime. Doc-claims không quétops, nên các phép kiểm trực tiếp mới hỗ trợ kết luận hồ sơ.

Đã review phần đổi sauc43347d trên hai trục: **Spec** (billing/A9, ngưỡng, hash, chuỗi lease và bản chiếu) và **Standards** (hai receipt, README, ghi nhận điều phối, lịch sử commit, manifest, năng lực đo và cổng hồ sơ). Không tuyên bố tái nghiệm thu bốn packet hoặc Windows/billing thật.

## KIỂM CUỐI VÀ BÀN GIAO

__FINAL_CHECK__

Lượt kế cần sửa hai P2 hồ sơ, giao đủ snapshot ref theo §8, rồi sau14:30:07Z quét lại trên cả hai đường write set. Chỉ đóng P1 trạng thái khi kết quả thực trên đủ ref là1người giữ=exec-1r4 và không còn #456 CÒN_HẠN chưa bia mộ. Mô phỏng lần này không thay được phép đó.

VERDICT và bằng chứng chỉ được ghi ra sandbox; việc đăng GitHub/record-review thuộc bên điều phối vì PROMPT cấm mạng. Không có approval/merge/land nào được thực hiện.

verdict: dang-do
'''

names = ['lease-publish-test', 'bien-nhan-v2', 'doctrine-scan', 'adr-song', 'doc-claims', 'eol', 'eol-json']
rows = []
for name in names:
    d = json.loads((O / f'{name}.json').read_text())
    command = ' '.join(d['command'])
    rows.append(f"| `{command}` | {d['rc']} | {d['elapsed_seconds']:.3f} | {d['stdout_bytes']}/{d['stderr_bytes']} |")
text = text.replace('__GATE_ROWS__', '\n'.join(rows))
(B / 'VERDICT.md').write_text(text)
