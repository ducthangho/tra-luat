verdict: approve
reviewed_sha: 91bbc824e017268629b77308e1027a0a0a462fe0

**0 P1 / 0 P2 / 0 P3. Bảy lớp đều 0 thể hiện sống; tám đột biến được phát hiện và khôi phục.** Năm hunk lượt 7 vá đúng các lỗi đã chỉ; phép quét toàn tệp lần này không tìm thêm thể hiện hoặc lớp mới. Chín cổng nền đều rc=0. Không suy nội dung đúng từ cổng xanh.

Reviewer: Codex, dựa trên GPT-6 theo chỉ thị phiên; provider OpenAI (`openai_codex`), execution surface agent qua API có shell sandbox, transport `machine`. Không có attestation độc lập về backend model/effort thực thi verdict. CLI Codex/Claude cục bộ là công cụ được thử, không chứng nhận danh tính reviewer. Không dùng sub-agent hoặc context Executor.

Authority/phạm vi: PROMPT.md của gói yêu cầu review offline trên bản sao, ghi VERDICT/HINT/evidence tại đây và chạy phản chứng trên clone tạm. Không sửa `cay-kho/`, không push/merge/đăng GitHub, không gọi reviewer model, không tự soạn nội dung tấn công. State dùng trong probe chỉ là fixture, không là lease/approval thật. Không xác thực GitHub authority, generation hoặc head live ngoài snapshot.

Git: HEAD đúng SHA trên, tree **b0af2b4b6eeac2f54376a7e0a269ae8c62ceea8f**; base **bb7013c7669da19304a8769e5b25f8c1f8951e9c** là ancestor và chính merge-base. Diff đúng **một tệp `.claude/skills/cross-review/SKILL.md`, +247/−147**; HEAD 520 dòng, base 420 dòng. Nguồn sạch. [Setup](evidence/setup.json), [Git và replay](evidence/extra-probes.json), [kiểm cuối](evidence/final-check.json).

## Quét vét cạn — tập vật thể và kích thước

Đã ghi kiểm kê **trước khi phân loại lỗi**, bằng `python3 evidence/inventory.py`. Phân hoạch 520 dòng thành **23 fence** và **93 đơn vị văn bản ngoài fence**; **0 dòng không trắng bị bỏ ngoài hai tập**. Các đơn vị giữ nguyên văn, gồm frontmatter, heading, bảng, bullet và đoạn văn; không chỉ trích những câu giống lỗi cũ. [Script](evidence/inventory.py), [toàn văn có ID/dòng](evidence/inventory.md), [annotation từng đơn vị](evidence/semantic-ledger.json).

| Lớp / tập duyệt đã chốt | Kích thước và cách chứng minh phạm vi |
|---|---|
| `va-qua-tay-mat-cong-cu` | **400 ứng viên**: mọi inline span, §, token đường/tên tệp và tên mục trích dẫn. Phân loại đủ 400: **161 tham chiếu/đầu vào/đích công cụ, 239 literal/cờ/giá trị không hứa một đích**. Trong đó có đủ **45 dấu §**, 26 lần nhắc tệp Git, 60 đường/hiện vật mẫu. Bổ sung **11 quan hệ trỏ theo ngữ cảnh** và sổ **22 lần dẫn PR/r/commit**; các sổ này có giao nhau, không cộng thành số con trỏ duy nhất. |
| `lenh-khong-noi-hien-vat` | **23 fence = 21 khối chứa lệnh + 2 mẫu Markdown**. Mỗi khối có bảng producer→consumer, biến, placeholder, stdout và lệnh thử. Các lệnh inline cũng được xét trong đủ 400 ứng viên/93 đơn vị; có bảng giới hạn cho cú pháp rời và ca cần dịch vụ. |
| `loi-khai-vuot-phep-do` | **93 đơn vị ngoài fence + toàn bộ nội dung 21 fence lệnh**, bao gồm comment. Đây là tập lấy dư bao phủ mọi câu đứng cạnh lệnh; **93 không phải số câu kết luận**. Đọc cả đoạn để giữ chủ thể, điều kiện và lượng từ, rồi so với source/output. |
| `adapter-chep-doctrine` | Đọc lại **520/520 dòng**, theo cùng 93 đơn vị và 23 fence; hỏi riêng câu nào tự đặt authority, assurance, budget, schema hoặc completion. |
| `neo-sha-tu-head-dong` | Cùng **93 đơn vị + 23 fence**; theo đủ tuyến lấy dữ liệu, diff/numstat, checkout, log và record-review. Có **2 nơi tạo/ghi artifact cần kiểm nguồn SHA**: B09 và B22. |
| `phan-hoach-trang-thai` | Cùng **93 đơn vị + 23 fence**; so nhánh rc/subtype/header/EOF/quota/PID/cd/ref/slug/blocked. Không lọc chỉ theo chữ pass/fail. |
| `don-vi-byte` | Cùng toàn tệp, kèm **242 token chứa số** làm chỉ mục lấy dư: có ngày, ID, model, cờ và đường dẫn, không gọi cả 242 là phép đo vật lý. So đơn vị/mẫu số và phạm vi lịch sử. |

[400 hàng con trỏ và các quan hệ ngữ cảnh](evidence/pointer-audit.md), [22 locator lịch sử](evidence/history-locators.json), [bảng 23 khối](evidence/command-audit.md), [242 token số](evidence/numeric-candidates.json), [số đếm](evidence/audit-counts.json).

**Vì sao tập đủ:** parser fence kiểm đóng/mở và kiểm phủ mọi dòng không trắng; phần ngoài fence được giữ nguyên, không có predicate loại văn bản theo chủ đề. Regex con trỏ chỉ giúp lập chỉ mục; sau đó đã đọc toàn bộ 93 đơn vị và cả 23 fence để bắt tên mục xuống dòng, “xem (1)”, “phía trên/bên dưới”, tên hàm và con trỏ lịch sử. Phép kiểm phủ dòng chứng minh phạm vi đọc; **không chứng minh máy hiểu nghĩa**. Annotation ngữ nghĩa là công của reviewer, có phản chứng ở mục đột biến.

**Từng đích hứa gì:** §4/8/9/10.2/12/13 đều có thật và có nội dung được dẫn; `GOI_AGENT_DA_NEN.md` L395–413 có cờ neo kho; `CLAUDE.md` L197–240 có phép so nguồn/đệm, L881–917 có phái sinh/verify. Các tệp công cụ tồn tại, hàm/CLI được đọc và thử. `PROMPT.md`, `SPEC.md`, run/log và đường `<…>` là đầu vào ví dụ, không phải lời hứa chúng đã tracked trong kho. Con trỏ dịch vụ và số lịch sử có giới hạn riêng, không được đánh dấu “đã kiểm live”.

**Từng khối chạy đến đâu:** B01/B03/B05/B07/B08 và Git/diff/patch/helper ở B09–B15/B20/B22 chạy thật; B04/B06/B11 thay riêng lời gọi model bằng stand-in đọc stdin/argv; B02 thay phần công cụ có thể gọi mạng/credential/cài đặt; B21/B23 và metadata B09 dùng gh stand-in. B16/B19 là Markdown. B17 chạy hai lệnh trước mũi tên chú giải; đổi mẫu tiến trình đồng bộ sang token riêng của harness. B13 chỉ thay dòng remove để giữ thư mục tạm theo PROMPT. Không gộp các trường hợp này thành “21 lượt thực thi dịch vụ thật”.

## Bản vá lượt 7 có đóng cả lớp không

**ĐỐI CHIẾU LƯỢT TRƯỚC:** đã đọc VERDICT-LUOT-7.md, HINT-LUOT-7.patch và VERDICT-LUOT-6.md. Lấy blob từ parent `aaef55bf77f061015d46b14411475d7f448beb05`, áp nguyên HINT lượt 7 trên scratch bằng `patch -p0 --fuzz=0 --verbose`: **rc=0, 5/5 hunk**, kết quả **bằng byte HEAD**. [Lệnh/output replay](evidence/extra-probes.json).

| Finding / hunk lượt 7 | Kiểm độc lập trên HEAD | Kết luận |
|---|---|---|
| `neo-sha-tu-head-dong`, H1 | L209 định nghĩa cả `<base_sha>`/`<reviewed_sha>` là OID chốt; B09 Git dùng trực tiếp cả hai. Gh metadata được ghi rõ lấy tại lúc gọi. Stand-in cố ý trả metadata khác nhưng diff/numstat vẫn cùng cặp SHA. | **ĐÃ VÁ THẬT**; metadata là quan sát có nhãn, không còn làm nguồn neo. |
| `lenh-khong-noi-hien-vat`, H2 | B10 cấp RV rồi clone/checkout/status thật0. B12 cấp R riêng trước `$R/kho.git`, `$R/cay-kho`; RV và R là hai layout khác nhau, không bị dùng lẫn. | **ĐÃ VÁ THẬT**, quét đủ mọi lần dùng biến không tìm thêm đường đứt. |
| `loi-khai-vuot-phep-do`, H3 | B15 so tên+OID, trừ HEAD. M8 giữ tên nhưng đổi OID: echo in diff1; bỏ objectname mới lọt0. Ref tag nằm ngoài phép hỏi vẫn có thể khác. | **ĐÃ VÁ THẬT**; câu giới hạn đúng phạm vi, không quá hẹp. |
| `va-qua-tay-mat-cong-cu`, H4 | Protocol §10.2 L699–709 có `release-manifest --root … --out …`; CLI help0; sinh manifest tạm0 và bằng byte canonical. §9/CLAUDE vẫn giữ con trỏ tệp phái sinh. | **ĐÃ VÁ THẬT**, không làm mất policy hoặc cú pháp. |
| `neo-sha-tu-head-dong`, H5 | L493 định nghĩa SHA từ VERDICT. Helper thật trên fixture: SHA khớp0, stale5. M5 đổi về lấy gh động: state mới chấp nhận0 dù artifact là SHA cũ. | **ĐÃ VÁ THẬT**; nguồn SHA là điểm khác biệt, không phải đổi tên placeholder đơn thuần. |

**Diff merge-base:** với PR được giao, base chính là merge-base; `git diff base head` và `git diff base...head` **bằng byte, 43.081 byte**. Probe DAG phân kỳ cho thấy hai cú pháp khác nhau: endpoint diff có cả xoá `base-only.md`, merge-base diff chỉ thêm `feature.md`. Git vẫn lấy được diff theo merge-base bằng ba dấu chấm; việc bỏ `gh pr diff` không làm mất khả năng ấy. Câu HEAD chỉ hứa diff theo cặp OID chốt, không hứa mọi endpoint diff bằng màn hình PR của GitHub. Vì vậy không nâng khác biệt phạm vi này thành finding. Chưa so với API GitHub live.

**Mã `ref diff rc`:** `$?` trong echo được mở rộng ngay sau `diff`, nên thuộc diff. M8 đo **1→0→1** khi bỏ/khôi phục objectname. Mã cuối cả khối vẫn0 do `rev-parse --is-shallow-repository`; không dùng nó thay mã diff. Lệnh có thể chứng minh tập tên+OID trong namespace ấy khớp tại lúc đọc nếu các producer đọc thành công; không kiểm mọi namespace, object hoặc máy chủ.

Sau replay và quét cả 520 dòng, không thấy năm hunk sinh lỗi mới. Kết luận “đóng lớp” chỉ nói tập và revision đã kiểm, không bảo đảm mọi sửa đổi tương lai.

## Bảy lớp — bảng quét

| Lớp | Thể hiện sống trên HEAD | Phản chứng phép quét |
|---|---:|---|
| adapter-chep-doctrine | 0 | M1 |
| va-qua-tay-mat-cong-cu | 0 | M2 |
| lenh-khong-noi-hien-vat | 0 | M3 |
| neo-sha-tu-head-dong | 0 | M5 |
| loi-khai-vuot-phep-do | 0 | M4 + M8 |
| phan-hoach-trang-thai | 0 | M6 |
| don-vi-byte | 0 | M7 |

**adapter-chep-doctrine — bảng sống 0 dòng:**

| ID | Dòng | Nghĩa vụ tự đặt |
|---|---|---|

Các chữ “BẮT BUỘC/PHẢI” còn lại là giải thích cờ/config/regex công cụ hoặc đã dẫn yêu cầu canonical. Bảng bậc mô tả `_BAC`/`chon`; bảng ≥6 hướng là prompt lịch sử; mẫu verdict nói rõ không phải schema đủ. Không có điều kiện nghiệm thu, quota pool hoặc quyền review do adapter tự đặt. M1 chứng minh đọc nghĩa bắt được quy tắc mới dù doctrine-scan vẫn0.

**va-qua-tay-mat-cong-cu — bảng sống 0 dòng:**

| ID | Dòng | Đích vắng hoặc thiếu nội dung hứa |
|---|---|---|

Đã kiểm tồn tại và nội dung, không chỉ hết broken link. Recipe/code vẫn có tại các con trỏ cụ thể nêu trên. API/package live và locator lịch sử chưa kiểm độc lập được ghi riêng; thiếu kết nối không bị đổi thành finding đường dẫn sai.

**lenh-khong-noi-hien-vat — bảng sống 0 dòng:**

| ID | Dòng | Tuyến producer→consumer bị đứt |
|---|---|---|

B04 ghi reviewer.json, B05 đọc đúng; B09 ghi cả diff.patch/numstat.txt; B10 cấp RV; B12 cấp R; B14 ghi hai tệp rồi comm đọc; B20 lưu GOI_Y_VA.diff trước patch; cả ba B21 đọc VERDICT.md. PY đều cấp trước dùng. Input placeholder được thay bằng giá trị đã khai trong fixture; không coi placeholder là cú pháp shell chạy nguyên văn.

**neo-sha-tu-head-dong — bảng sống 0 dòng:**

| ID | Dòng | Nguồn SHA động dùng thay revision đã đọc |
|---|---|---|

B09/B22 dùng SHA chốt; B10/B12 checkout exact SHA. `gh pr view`, `status`, `log`, ref comparison là phép quan sát hiện trạng có nhãn, không còn được chuyển thành SHA của verdict cũ. M5 kiểm cụ thể nhánh artifact cũ/state mới.

**loi-khai-vuot-phep-do — bảng sống 0 dòng:**

| ID | Dòng | Câu khai rộng hơn output/source |
|---|---|---|

Các câu ưu tiên đã giới hạn đúng: **spark trong #518** từ chối max, không phải mọi model; ba model bị **tài khoản đã thử** từ chối không là danh sách đầy đủ; quan sát quota chưa xác định pool/độc lập; launcher **có thể** còn dang_chay; không nói cần cả ba dấu hiệu. Header là CLI tự khai, không attestation model hay đo ảnh hưởng effort. `r368` có nguồn thuật lại trong CHANGELOG L576–600 và `ops/land/pr493-land-evidence.yaml` L76–78; không có raw của 17 lượt để replay.

Cặp cd/interpreter/echo được thử: số echo **1/0/7/127** lần lượt cho cd vắng/Python0/Python7/interpreter vắng; cả block có thể0. Ma trận16 ca helper: approve/blocked không finding0; changes_requested không finding2; slug sai2; SHA vắng/hoa/viết tắt/lệch5; chạm same-failure3 với cả ba verdict. Câu HEAD chỉ mô tả nhánh kiểm finding và có con trỏ §12, không hứa mọi slug hợp lệ đều0.

Các số 154/437/299s, 3/13, 526, 14,5/16GB và 2/5 giữ nhãn lịch sử; không suy nhân quả từ hai prompt, không coi sáu HINT thành chứng minh điều kiện cần. Commit merge #518 đọc được và thuật lại đúng7 lượt/6 HINT/13 hunk. Đó là đối chiếu nguồn thuật lại, **không phải chạy lại những lượt ấy**.

**phan-hoach-trang-thai — bảng sống 0 dòng:**

| ID | Dòng | Trạng thái bị gộp/tách sai |
|---|---|---|

EOF trước model khác review thất bại; lỗi unsupported khác quota; sed đọc được khác header đủ; thiếu khóa khác chết, khớp khóa khác sống, Z khác tiến triển; stat im khác chết; cd lỗi khác cổng đã chạy; ls-remote lỗi khác đếm0; diff1 khác lỗi công cụ; grep-count0/rc1 khác cổng đỏ; helper blocked/trần3 khác thiếu SHA5. Không có lời khai biến skipped/cancelled/chưa đo thành pass. M6 bơm đúng sự nhập nhằng đọc được/đã xác nhận vào comment.

**don-vi-byte — bảng sống 0 dòng:**

| ID | Dòng | Đơn vị / quy đổi / mẫu số sai |
|---|---|---|

Đã phân biệt số model/effort, điểm bậc, phiên bản, số lượt, giây, byte, GB và OID/hash. Các nhóm8/9,6/9,3/9,2/9 có thể giao nhau; không cộng thành phân hoạch. 500/90000 là ví dụ outputTokens, không số byte hoặc phần việc đã đo. 6/6 #518 khác mẫu2/5 #250/#252. 14,5/16 giữ GB, không tự đổi GiB. Stat `%s` đo byte; `%Y` mốc giây; khoảng60s đã chạy thật. Các giá trị lịch sử không có raw vẫn giữ giới hạn vừa nêu.

## Lớp KHÁC tìm được

**0 lớp mới / 0 finding.** Đã thử thêm thứ tự bố trí, tính nhất quán hai layout patch, metadata không dùng làm neo, diff endpoint/merge-base trên DAG phân kỳ, trạng thái local/HTTPS của origin, launcher snapshot thay stdin và các nhánh rc bị che bởi lệnh cuối.

Không coi mẫu Markdown chưa hoàn chỉnh là lỗi P2 khi chính tài liệu đã ghi đó không phải schema đủ. Không coi câu trỏ canonical là mất công cụ nếu đích thực có nội dung đã hứa. Không coi thiếu raw lịch sử hoặc môi trường không cho gọi dịch vụ là chứng cứ câu thuật lại sai.

## Phép đo nền

Chạy lần lượt bằng `python3 evidence/run_gates.py` từ clone **sạch, đầy đủ, ngoài cây review**: `/tmp/rv521-l8-ast1o3ro/gates`. Clone thứ hai `/tmp/rv521-l8-ast1o3ro/experiments` cũng sạch lúc dựng, chỉ dùng cho probe/mutant. Cả hai detached exact HEAD, non-shallow, `core.abbrev=7`, `core.autocrlf=false`; PATH đặt actionlint1.7.7 của gói trước tool hệ thống. Mirror/source/experiment có cùng **356 head tên+OID** sau bỏ origin/HEAD; con số này không xác thực máy chủ live.

| Lệnh | rc | Bằng chứng dương |
|---|---:|---|
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | 0 | 7 tệp,0 chuỗi cấm. [Log](evidence/gate-doctrine.json). |
| `python3 .claude/dev/packet_loop.py adr-song --root .` | 0 | 47 ADR/47 hàng, ngoại lệ trạng thái0016 công bố. [Log](evidence/gate-adr.json). |
| `python3 ops/bien_nhan_v2.py --root .` | 0 | 113 đạt v2 +11/11 miễn legacy +42 nợ đóng băng =166;0 vi phạm/chưa đo. **Không gọi166 là đạt v2.** [Log](evidence/gate-receipts.json). |
| `python3 ops/lease_publish_test.py` | 0 | 147/147 đạt; chạy147, bỏ qua0. Catalog37 mutant:34 giết thật,3 sống chủ đích,0 tín dụng giả. [Log](evidence/gate-lease.json). |
| `python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | 0 | ok=true, expected=checked=180; các mảng lỗi rỗng. [Log](evidence/gate-release.json). |
| `python3 scripts/tl.py golden-test --json` | 0 | ok=true,20 ca. [Log](evidence/gate-golden.json). |
| `python3 scripts/tl.py doc-claims-check --strict --json` | 0 | ok=true,107 tệp,0 hard flag,374 advisory. [Log](evidence/gate-claims.json). |
| `python3 .githooks/eol_policy.py --all --json` | 0 | 2082 scanned,2060 checked,22 skipped,0 violations. [Log](evidence/gate-eol.json). |
| `python3 .claude/dev/idiom_py_test.py` | 0 | 7 ca,0 bỏ qua,9 mutant,7 tệp phạm vi;389 lời gọi ngoài phạm vi là chẩn đoán nợ, không phải fail. [Log](evidence/gate-idiom.json). |

**Không có cổng nền đỏ**, nên điều kiện chạy lại cổng đỏ trên clone sạch khác không phát sinh. B13 vẫn đối chiếu riêng doc-claims trên worktree và clone cùngSHA, cả hai0; không gọi đó là lặp toàn bộ chín cổng. Các rc khác0 trong probe/mutation là phản chứng có chủ đích hoặc lỗi harness đã phân biệt, không phải kết quả cổng nền.

Hỏng harness đã lưu và xử lý: (1) init fixture truyền mission chuỗi, CLI đòi số; sửa999, resume B22–B23/inline; (2) resolver heading ban đầu chỉ nhận số mục có dấu chấm cuối, bỏ lọt10.2; sửa grammar rồi kiểm đủ45 dấu§; (3) DAG scratch bị cấu hình ký commit kế thừa gọi signer loopback và bị sandbox từ chối; không ký được commit, không có kết quả mạng thành công. Dựng DAG mới, đặt `commit.gpgsign=false` riêng fixture, chạy lại thành công; (4) import runpy không cần thiết thiếu launcher trên sys.path; bỏ import đó, chạy tiếp đủ ma trận. Không dùng những lần lỗi này làm finding sản phẩm hoặc bằng chứng dương. [Log gốc và lần resume](evidence/extra-probes.json), [script resume](evidence/resume_extra.py).

## Đột biến và khôi phục

Lệnh: **`python3 evidence/mutations.py`**. Mỗi ca sửa tệp trong clone experiments, giữ snapshot mutant để đọc, chạy phép kiểm trước/sau, khôi phục byte trong `finally`, rồi chạy lại phép kiểm và `git diff --exit-code`. [Script](evidence/mutations.py), [lệnh/output/hash từng ca](evidence/mutations.json), [khôi phục cuối](evidence/mutation-restoration.json).

| Mutant / lớp | Thay đổi và phép kiểm | Trước → sau → khôi phục | Kết luận |
|---|---|---|---|
| M1 doctrine | Bơm nghĩa vụ nộp đúng10 phản chứng mới kết thúc. Đọc chủ thể/nghĩa vụ/completion theo cách đọc93 đơn vị. doctrine-scan thật vẫn0/0/0. | Bảng sống **0→1→0** | Phép đọc bắt nghĩa vụ ngoài danh sách chuỗi. Đây là annotation reviewer, không giả nhận script là semantic scanner. |
| M2 con trỏ | Đổi heading neo kho sang “Mã thoát”, một heading có thật. Resolver cắt đúng đoạn; kiểm nội dung hứa cờ `--expected-repo`. | Đích tồn tại cả3; thiếu nội dung **0→1→0** | Bắt đích có thật nhưng không chứa công cụ đã hứa. |
| M3 hiện vật | B05 đọc REVIEWER.json trong khi B04 tạo reviewer.json; chạy vị từ thật. | Consumer rc **0→1→0**; sống **0→1→0** | Bắt đứt tuyến ngoài nhóm VERDICT đã vá trước đó. |
| M4 lời khai | Đổi “không kiểm mọi namespace/object” thành “kiểm mọi”. Thêm tag riêng ngoài origin; B15 vẫn diff0. | Bảng sống **0→1→0**; block rc0 cả3 | Câu mới không được phép hỏi origin chống đỡ. Không dùng rc0 làm kiểm toàn kho. |
| M5 neo SHA | Đổi B22 thành lấy head bằng gh tại lúc ghi. Artifact giữBASE, state/gh giữHEAD; helper thật. | Helper rc **5→0→5**; sống **0→1→0** | Đường động nhận nhầm revision; SHA artifact cố định bị chặn đúng khi stale. Gh chỉ stand-in. |
| M6 trạng thái | Comment sed bị đổi từ “chưa xác nhận” sang “đã xác nhận header/đủ trường”; chạy trên tệp rỗng. | Sed rc0/output rỗng cả3; sống **0→1→0** | Đọc được không đồng nghĩa đã đo hai trường. |
| M7 đơn vị | Bơm comment `%s` trả KiB; stat tệp biết trước1024byte trả1024, không phải1KiB. | Output1024 cả3; sống **0→1→0** | Phép quét số bao gồm cả comment, phát hiện đơn vị sai. |
| M8 câu nghi nhất lượt7 | Giữ lời hứa “tên và OID”, bỏ `%(objectname)` ở cả hai producer B15. Ref master clone khácOID nguồn nhưng cùng tên. | **echo diff1→0→1**; sống **0→1→0** | Bắt mất dữ liệu ngay trong H3 lượt7; không dựa vào rc cuối khối, vốn0 cả3. |

M2/M3/M5/M8 có oracle nội dung đích hoặc hành vi độc lập; M1/M4/M6/M7 còn cần đối chiếu **nghĩa câu** với kết quả. Trường `live` của các ca đó ghi đánh giá reviewer theo đúng tập quét, không được quảng bá thành bộ chứng minh ngữ nghĩa tự động hoặc bảo đảm bắt mọi cách diễn đạt.

**Khôi phục đủ8/8:** SHA256 tệp trước/sau mỗi ca bằng **723e18317f6ec216798957963d0a11d7f3ba712a7fda690044999777ee330c8e**; cả8 `git diff --exit-code` rc0. Tag fixture đã gỡ, OID master đã đặt lại giá trị cũ; B15 cuối in `ref diff rc=0` và `false`. Git status experiments và nguồn đều rỗng. Không dọn các thư mục tạm.

## HINT.patch và giới hạn

Chọn **giữ HINT.patch rỗng: 0 byte, 0 hunk, 0 tệp**, vì verdict approve và không có finding. Lệnh đúng yêu cầu **`cd cay-kho && patch -p0 --fuzz=0 --dry-run < ../HINT.patch` trả rc=0**; với tệp rỗng, đây là phép kiểm không có patch để áp, không phải bằng chứng đã sửa sản phẩm. Nguồn vẫn exact HEAD/sạch. [Kiểm cuối](evidence/final-check.json).

Không có hunk mới chạm câu lượt5/6/7. Việc sửa câu/format trong M1–M8 chỉ là đột biến trên bản sao và đã khôi phục; không đưa mutant vào HINT.

**KHÔNG kiểm được:** GitHub/CI/head/quota/assurance live; contract MCP GitHub hiện hành; identity backend model; khả năng tài khoản gọi model/effort tại thời điểm này; raw log của phần lớn số lịch sử #513/#518/#250/#252 và1.151s; chính sách sandbox trên mọi nền; Windows/macOS; container restart thật. Launcher được thử với child Python local và snapshot, không phải một lượt model review hoặc phép đo sập container. Các nhãn “thuật lại/đo trong lượt đó” không bị nâng thành bảo đảm hiện tại.

`approve` này là kết quả nội dung của snapshot được giao, không tự đăng GitHub, ghi assurance vào state, cấp quyền merge hay xác thực mọi số lịch sử. Evidence cho phép đọc lại từng tập và từng phản chứng; không có lời khai “cổng xanh nên nội dung đúng”.
