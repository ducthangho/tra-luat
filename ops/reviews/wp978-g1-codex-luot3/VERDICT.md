Verdict: request_changes
Reviewed commit: fdf1f05c1b3d845a694c796a81a8bd5c218a68c8
Spec sha256: eccd6dd2917f76d6158d5c9574f4d4c2070ba22ef3da96b4dfcf6e820c301638

**Còn 2 lớp P2: 1 lỗi metadata trên mã head thật và 1 lớp thiếu độ phủ có mutant không tương đương sống trên đầu vào Git hợp lệ. P0=0, P1=0, P2=2, P3=0.** Hai biểu hiện P2 lượt 1 đã vá thật; F13 encoding đã được sửa. 53/53 ca và 22/22 mutant F13 xanh không bắt được lỗi mới bên dưới. Verdict chỉ neo commit trên, không cấp quyền push, merge hay land.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn đối chiếu là verdict lượt 1 tại `bef14035718cae862369101f79dc61e938ae6b00` và **bản tạm, không phải verdict hoàn chỉnh**, lượt 2 tại `7fcfe18181ce4d089225900e36d3aed878877e7f`. Mọi kết quả dưới đây được chạy lại trong lượt này.

| Lớp / biểu hiện trước | Kết luận trên head | Phép đo riêng |
|---|---|---|
| `git-object-type-not-checked` — P2 lượt 1 | **ĐÃ VÁ THẬT** trong miền đã kiểm | Blob có header commit/OID hợp lệ, blob không UTF-8, tree và tag đều trả None trên SHA-1/SHA-256. Criterion blob: head rc 0, base rc 3. Main với blob: head checkout `not_measured`, base `passed`; cả hai outer rc 0, không đánh đồng rc 0 với checkout passed. [Reader](independent-results.json), [main](independent-main-results.json), [criterion](criterion-r978_noncommit_must_be_none-head.json). |
| `git-header-cr-split-creates-parents` — P2 lượt 1 | **ĐÃ VÁ THẬT** cho cơ chế CR/splitlines | Commit chứa CR trong author: native Git 0 parent, `fsck --strict` rc 0, `merge-base --is-ancestor` rc 1. Head trả 0 parent. Main control/CR trên head rc 12/12, đều checkout failed; base rc 12/0. Criterion head rc 0/base rc 3. [Git](cr-author-results.json), [main](cr-author-main-results.json), [criterion](criterion-r978_author_must_not_create_parent-head.json). |
| `git-reader-fixture-domain-incomplete` — P3 lượt 1 | **ĐÃ VÁ các biểu hiện cũ; lớp CÒN MỞ, P2 theo ngưỡng prompt hiện tại** | Mười mutant không tương đương sống lượt 1 và R05 từng lỗi rc 4 được chuyển sang neo mã head: **11/11 rc 3, đúng c53**. Tuy nhiên Y01/Y02 mới vẫn sống 53/53 ca và sai trên Git hợp lệ; xem bảng lớp và nhân chứng dưới. Không đổi slug để xóa lịch sử lớp. [Catalogue neo/thay](supplemental-mutant-catalogue.json), [kết quả](supplemental-mutant-results.json). |
| X01 — bỏ đếm trường batch header | **ĐÃ VÁ THẬT về test** | c53 head giết bằng stdout rỗng: child rc 3, `DO:c53_git_commit_khong_utf8:`. |
| X02 — chấp nhận header thừa trường | **ĐÃ VÁ THẬT về test** | Header được tiêm bằng cách thêm trường vào stdout Git thật: child rc 3 đúng c53. Đây là phép thử lỗi giao thức được tiêm, không gọi nó là stdout bình thường do Git sinh. |
| X03 — chấp nhận payload ngắn | **ĐÃ VÁ THẬT về test** | Cắt 2 byte cuối stdout Git thật: child rc 3 đúng c53. |
| X04 — chấp nhận payload dài | **GIỮ ĐÓNG** | Child rc 3 đúng c53; ca nhiều dòng SHA phát hiện nhận thừa payload. X04 không nằm trong năm survivor toàn ca của lượt 2. |
| X05 — bỏ bắt UnicodeEncodeError | **ĐÃ VÁ THẬT về test** | SHA chứa surrogate `\udc80`: child rc 3 đúng c53. |
| X06 — bỏ bắt SubprocessError | **ĐÃ VÁ THẬT về test** | Tiêm TimeoutExpired: child rc 3 đúng c53. |
| Bộ bọc `doc()` và X11 | **Không xác nhận cáo buộc tín dụng giả cho X11** | X11 ném AttributeError ngay khi vào reader, làm hỏng cả commit hợp lệ; rc 3 là phát hiện vi phạm hợp đồng không-ném. Hai đối chứng lỗi ngoài reader đều rc 4/TIN_DUNG_GIA. Có chênh lệch câu chữ M2, phân tích riêng dưới. |

Toàn bộ X01–X11 được chạy trực tiếp từ bản sao các tệp mutant lượt 2 với **test head**, đều rc 3 đúng c53: [receipt đầy đủ](x-replay-results.json). Mã sản phẩm `7fcfe18` và head giống nhau; việc dùng các tệp này không trộn phiên bản sản phẩm.

## Bảng lớp còn mở

| slug | hạng P0–P3 | biểu hiện file:dòng | phép đo/tái hiện | hướng vá |
|---|---|---|---|---|
| `git-header-extension-creates-parents` | **P2** | `ops/ci_provenance.py:151–155`, đặc biệt dòng 152 quét mọi dòng `parent ` trong toàn header | Commit Git hợp lệ có `parent <OID>` sau `committer` hoặc sau một extension header: native Git không có parent, head lại trả một parent. Main control rc 12/failed; cả hai biến thể rc 0/passed. [Git/reader](extension-finding.json), [main](extension-main-results.json), [criterion head](extension-criterion-parent_after_committer-head.json). | Đọc quan hệ cha đúng vùng cú pháp của commit: dòng tree đầu, tiếp theo là dãy parent liên tiếp trước author/committer; không biến extension thành ancestry. Thêm ca control/extension, đối chiếu native Git và main âm. Giữ bytes, thứ tự parent, SHA-256, root/octopus; tránh vá bằng từ chối rộng mọi extension hoặc giải mã author/message. |
| `git-reader-fixture-domain-incomplete` | **P2** | `ops/ci_provenance_test.py:1095–1113` — fixture SHA-1 chỉ có 0/2 parent, fixture SHA-256 chỉ có 0 parent | Y01 cắt danh sách còn 2 parent; Y02 chỉ chấp nhận parent dài 40 hex. **Mỗi mutant sống 53/53 ca, từng ca rc 0**. Commit 3 parent thật phân biệt Y01; commit SHA-256 có parent thật phân biệt Y02; cả hai `fsck --strict` rc 0. Head nguyên bản đúng trên hai nhân chứng này. [Kết quả](supplemental-mutant-results.json), [nhân chứng](new-mutation-witnesses.json). | Bổ sung fixture 3 parent thật, giữ thứ tự cố ý không sắp xếp; thêm commit SHA-256 có parent thật. Assertion so đủ danh sách và OID với native Git; thêm đột biến tương ứng. Chỉ mở miền reader, không suy main hỗ trợ SHA-256 toàn tuyến. Tránh dùng fixture thiếu parent object hoặc mock Git làm mất ý nghĩa của nhân chứng. |

Lỗi extension là **lỗi có sẵn ở base**, không phải hồi quy mới do diff. Nó có cùng hậu quả parent giả với lỗi CR cũ, nhưng cơ chế khác: ranh giới LF hiện đã đúng, còn vị trí ngữ pháp của dòng parent bị bỏ qua. Vì cần một chốt khác, dùng slug mới và giữ lớp CR cũ đã đóng. Q5 không cấp quyền reviewer vá lỗi khác; lượt này chỉ ghi bằng chứng và hướng xử lý.

### P2 trên mã sản phẩm thật: extension không phải quan hệ cha

[Script tái hiện](extension_finding.py) tạo kho cô lập trong `out/fixture-extension`, workflow blob thật và commit đối chứng. Object được ghi bằng `git hash-object -t commit -w --stdin`, **không dùng `--literally`**. Hai biến thể chỉ thêm sau dòng committer:

```text
parent <OID-của-commit-không-liên-quan>
```

hoặc một dòng `x-review value` trước dòng parent đó. Đây không phải nội dung đường dẫn và không có thử thoát cây.

Với cả hai biến thể:

- `git show --no-patch --format=%T%n%P` rc 0, parents rỗng; `git fsck --strict` rc 0; `git merge-base --is-ancestor` với OID giả rc 1.
- `git_cuc_bo` head và base đều trả parent không tồn tại trong ancestry của Git.
- Main dùng REST giả, **reader metadata và workflow Git thật**: control rc 12/checkout failed; biến thể rc 0/checkout passed, lý do `head_sha_trong_parents_merge_tong_hop`.
- [Criterion riêng](extension_criterion.py), chạy ở tiến trình con thật: 2 biến thể × head/base = **4/4 rc 3**, prefix `DO:r978_extension_must_not_create_parent:`. Control head/base **2/2 rc 0**. Không dùng rc 0 của script thu thập làm bằng chứng tính chất đã đạt.

Đây là sai metadata và kết luận checkout có thể quan sát được. Phép đo không chứng minh một workflow GitHub cụ thể đang dùng commit này; không cần khẳng định đó để chứng minh sai hợp đồng reader trên object Git hợp lệ.

### Đột biến bổ sung và ngưỡng hạng

[Script](additional_mutations.py) tạo mutant trên bản sao, ghi cặp neo/thay và SHA-256. 14 mutant bổ sung: **12 GIET**, **2 SONG_SOT**, **0 TIN_DUNG_GIA**. Trong 12 GIET có 11 đối chiếu R cũ và Y03 sắp xếp parent.

| Mutant sống | Nhân chứng phân biệt | Tương đương? |
|---|---|---|
| Y01 `cha[:2]` trước giải mã parents | Commit SHA-1 có 3 parent thật. Native Git/head giữ đủ 3 đúng thứ tự; mutant bỏ parent cuối. Cả 53 ca vẫn rc 0. | **Không**; đầu vào Git hợp lệ, fsck rc 0. |
| Y02 chỉ cho parent `[0-9a-f]{40}` | Commit SHA-256 có 3 parent thật. Native Git/head trả metadata với OID 64 ký tự; mutant trả None. Cả 53 ca vẫn rc 0. | **Không**; đầu vào Git hợp lệ, fsck rc 0. |

Theo ngưỡng trong prompt, hai biểu hiện này là P2 của **một lớp thiếu độ phủ**, không phải hai lỗi sản phẩm hiện tại. Không dùng nhánh trả sai chỉ trên stdout Git bất khả sinh để nâng hạng. R08 tương đương của lượt 1 không được đếm như một lỗ hổng chưa đóng hay như một mutant mới đã chạy ở lượt này. Không chạy tập đột biến đóng toàn reader.

### Phán xét bộ bọc `doc()`

Tôi đồng ý với lập luận giới hạn của executor về **X11**. Khi exception thoát từ chính lời gọi reader trên commit hợp lệ, caller không nhận dict/None, và main không có chốt bắt exception đó. X11 do đó phá tính chất đang được kiểm; gọi nó là “unrelated sentinel” không làm lỗi trở thành vô can.

Đã tiêm hai đối chứng trên bản sao: AttributeError lúc import module, và TypeError khi binding lời gọi trước khi vào thân reader. Cả hai **rc 4/TIN_DUNG_GIA**, không được đổi thành assertion. [Script/nhân chứng](wrapper_and_witnesses.py), [receipt](wrapper-controls.json). X11 **rc 3** đúng c53; không tìm được mutant cụ thể chứng minh tín dụng giả theo hợp đồng không-ném trong các phép này. Kiểm traceback chỉ cho biết lỗi đã đi qua reader, không chứng minh mọi lỗi hạ tầng tương lai có nguồn gốc từ mutant.

**Không che chênh lệch đặc tả:** M2 đóng băng viết “Chỉ `UnicodeDecodeError` được đổi thành tín hiệu chốt … lỗi khác giữ nguyên là vô can.” Implementation hiện rộng hơn, chuyển mọi Exception có khung reader thành `NEM:<lớp>`. Về hành vi no-throw, X11 được giết hợp lệ; về đối chiếu nguyên văn, M2 không hoàn toàn khớp. Cần ghi quyết định này vào hồ sơ/đặc tả có thẩm quyền, không tuyên bố câu chữ M2 đã tự đổi. Đây là lưu ý hợp đồng; không dùng nó thay bằng chứng cho hai P2 ở bảng trên.

## N1–N7

| Tiêu chí | Trạng thái | rc và bằng chứng dương |
|---|---|---|
| N1 | **passed** | Test head c53 rc **0**; cùng test với mã base rc **3**, `DO:c53_git_commit_khong_utf8:` chứa UnicodeDecodeError. **2/2** kết quả đúng kỳ vọng. [Head](n1-head.json), [base](n1-base.json). |
| N2 | **passed về giết đột biến hành vi** | Lệnh import/`chay_dot_bien` đúng prompt rc **0**, **22/22 GIET**. Chạy riêng lại từng child: **22/22 rc 3** đúng c53, không rc 4. M3 gọi tên `F13_doc_text_true`, catalogue hiện dùng `F13_giai_ma_toan_stdout`; đột biến literal text=True với input kiểu str cũng được đo riêng qua X07, rc 3 chứa UnicodeDecodeError. Không giấu đổi tên. [Runner](n2-prescribed.json), [child](f13-children.json), [X07](replay-X07_text_true.json). |
| N3 | **not_run** | Không chạy suite mặc định (~40 phút), executor chịu trách nhiệm. Đã chạy đúng `--tat-ca-ca`: outer rc **0**, JSON có đủ **53/53** ca, từng rc **0**, không chỉ đọc mã thoát ngoài. Catalogue base **52 ca/292 mutant**, head **53 ca/314 mutant**; delta +1/+22, không khai +3 hay đã chạy 314/314. [Ca](all-head-cases.json), [tổng hợp](all-head-summary.json), [đếm AST](catalogue-counts.json). |
| N4 | **passed** | Bare Ruff `--no-cache --select F` trên hai tệp: head/base đều rc **0**, `All checks passed!`, delta F=0. `git diff --check c8d92ba HEAD` rc **0**. Không phải receipt kiểm pin/probe Ruff của CI. [Head](n4-head-ruff.json), [base](n4-base-ruff.json), [diff](n4-diff-check.json). |
| N5 | **passed** | doctrine-scan rc **0**, **10 tệp/0 chỗ chép**; adr-song rc **0**, **55 ADR/55 dòng**, khớp 1–1, output ghi ngoại lệ trạng thái ADR-0016. [Doctrine](n5-doctrine-scan.json), [ADR](n5-adr-song.json). |
| N6 | **not_measured** | Không mạng/GitHub; không tự đọc check run ci.yml trên exact head. Không nhận lời khai executor thay kết quả đo. |
| N7 | **not_applicable; not_run** | `git_cuc_bo` không thuộc `HAM_DONG`; không chạy `--dot-bien-dong`, không khai passed. |

Các quan sát dương bổ sung: **50/50 reader** trong bộ tái hiện lượt 1 đúng kỳ vọng; **7/7** biến thể SHA-1 qua main rc 0/checkout passed, gồm author/message Latin-1 và body giống metadata. Reader SHA-256 được đo riêng, không suy main hỗ trợ SHA-256 toàn tuyến. Các số 50/50 này là phạm vi bộ cũ; chúng không bao gồm hai biến thể extension mới bị lỗi. [Script](independent.py), [reader](independent-results.json), [main](independent-main-results.json).

## Định danh, phạm vi và tính toàn vẹn

- HEAD detached **fdf1f05c1b3d845a694c796a81a8bd5c218a68c8**, tree **1005c3629e521e503e31f326e81ca02051dcd4e5**. Chuỗi cha tự đo đúng `c8d92ba05c3ea875d8f84d94195430302690286d` → `bef14035718cae862369101f79dc61e938ae6b00` → `7fcfe18181ce4d089225900e36d3aed878877e7f` → head. `origin/master` local trỏ base. SHA-256 đặc tả khớp đủ 64 ký tự.
- Diff base..head đúng **2 tệp, +99/-6**: sản phẩm +18/-6, test +81/-0. Lượt 2..head chỉ đổi test. Vượt dự kiến 60 dòng thêm; dưới trần ADR-0053 6 tệp/450 dòng thêm. [Diff](diff.patch), [diff lượt 2](step1-test-diff.patch), [numstat](numstat.txt).
- So AST các hàm/lớp sản phẩm: chỉ `git_cuc_bo` đổi; có thêm hằng regex OID. `git_blob`, REST, `doc_wf`, `moc_checkout`, main không đổi. `--batch` thay `-p` để lấy loại object gốc cùng payload, không peel tag. Hai sửa lỗi cũ nằm trong hợp đồng reader nêu ở M1; không phát hiện thay đổi sang vùng ngoài write set. [AST](ast-scope.json).
- Đã đọc bản lease revision 1/generation 1/review class sensitive. Freshness remote/lease và lời nâng trần trên GitHub không được đo online; authority cho lượt offline là prompt hiện tại, nêu lời gọi 3/4. Không suy bản lease cũ còn ghi trần 2 thành lý do xin lại quyền đã được prompt cấp.
- Reviewer là Codex/họ OpenAI theo session; launcher ghi `openai_codex`, `codex_cli`, transport `machine`, run **8ef03e69f5d040a48dd03e76cdd9b5a2**. Exact serving model/effort **not_measured**: stderr không có header đủ thông tin. Executor họ Claude theo assignment/lease, runtime không được tự đo. `assurance_target: cross_approved` là mục tiêu, **không phải assurance được cấp bởi verdict request_changes này**. [Identity](identity.json).
- Linux; Python **3.13.17**, Git **2.43.0**, PyYAML **6.0.3**, Ruff **0.17.3**. [Versions](versions.json).
- Mọi thử nghiệm chạy trong bản sao `out/head`, mutant/fixture dưới `out/`. `PYTHONDONTWRITEBYTECODE=1`, `python -B`, TMPDIR tuyệt đối `out/tmp`, Git global/system config `/dev/null`, optional locks tắt; Ruff no-cache. Fixture có danh tính Git giả được đặt qua biến môi trường. Không cài công cụ, không mạng, không GitHub, không push/merge/land; không sửa `src/`.
- Snapshot cuối: **7205/7205** tệp tracked cùng SHA-256 đầu; HEAD/tree không đổi; tracked/index diff rỗng; status gồm untracked/ignored rỗng. Bản sao `out/head` cũng khớp 7205 tệp source. Snapshot đầu chưa lưu riêng ignored, nên không khẳng định đã so toàn bộ ignored ở cả hai mốc hay toàn bộ byte `.git`. [Đầu](preflight.json), [cuối](final-source-snapshot.json).

Lệnh đầy đủ, cwd, rc, stdout/stderr và thời lượng được giữ trong từng receipt JSON; script điều phối [bước 2](phase2.py), [ca/F13/gate](checks.py), [mutant bổ sung](additional_mutations.py) cho phép tái lập trên bản sao. Lịch sử verdict tăng dần ở [VERDICT.progress.md](VERDICT.progress.md). Để chạy lại, dùng bản sao/fixture mới dưới OUT; không chạy script trên SRC.

D02, F10/D05 của #899, `.claude/dev/ci_dang_ky_test.py --chay`, Workflow definition, LIVE CI, Windows native và SHA-256 toàn tuyến main ngoài phạm vi: không tính hạng, không tuyên bố đã đo hay đã đóng. Không soạn hoặc thử nội dung đường dẫn thoát cây.
