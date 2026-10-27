Verdict: request_changes
Reviewed commit: aa2a1f326eb964b1cf8f45454593971e0ab11b73
Spec sha256: eccd6dd2917f76d6158d5c9574f4d4c2070ba22ef3da96b4dfcf6e820c301638

**Còn 1 lớp P2: `git-reader-fixture-domain-incomplete`. P0=0, P1=0, P2=1, P3=0.** Lỗi sản phẩm `git-header-extension-creates-parents` đã được sửa trong các phép đo độc lập. Y01/Y02 đã bị giết. Tuy nhiên, mutant mới Z01 chuẩn hóa khoảng trắng đầu dòng header vẫn sống đủ 53/53 ca, dù trả sai trên commit Git hợp lệ có header nhiều dòng. Mã head hiện trả đúng trên các nhân chứng này; finding còn lại thuộc độ phủ test. Theo ngưỡng của prompt, chưa đủ điều kiện approve.

Verdict chỉ neo SHA trên, không cấp quyền push, merge hoặc land. Đây là lượt cuối 4/4 theo assignment; không đề nghị tự mở lượt review tiếp theo.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Đã đọc verdict lượt 1, bản **tạm** lượt 2 và verdict lượt 3; không nhận kết quả cũ làm bằng chứng đã chạy ở lượt này. Script cũ được đọc trước khi sao vào OUT; đã bỏ đoạn ghi verdict với kết luận hard-code cũ và sửa neo mutant cho mã head.

| Lớp / biểu hiện | Kết luận trên head | Phép đo tự chạy |
|---|---|---|
| `git-commit-body-encoding-lam-hong-metadata` — F13 gốc | **ĐÃ VÁ, không thấy hồi quy trong miền đo** | N1 head rc 0; cùng test với sản phẩm base rc 3 chứa `UnicodeDecodeError`. Bộ reader cũ 50/50 đúng; 7/7 biến thể SHA-1 qua main rc 0/checkout passed, gồm author/message Latin-1, message giống metadata, extension không UTF-8. [Reader](independent-results.json), [main](independent-main-results.json). |
| `git-object-type-not-checked` | **GIỮ ĐÓNG** | Blob dạng commit, blob không UTF-8, tree và tag trên SHA-1/SHA-256 đều None. Criterion head rc 0/base rc 3. Main blob: head `not_measured`, base `passed`, cả hai outer rc 0; không dùng rc 0 để suy checkout passed. [Criterion](criterion-r978_noncommit_must_be_none-head.json). |
| `git-header-cr-split-creates-parents` | **GIỮ ĐÓNG** | Commit CR trong author: fsck strict rc 0, native parents rỗng, kiểm ancestry rc 1; head trả 0 parent. Main control/CR trên head rc 12/12 và failed, base rc 12/0. Criterion head rc 0/base rc 3. [Git](cr-author-results.json), [main](cr-author-main-results.json). |
| `git-header-extension-creates-parents` — P2 lượt 3 | **ĐÃ VÁ THẬT** | Hai commit có `parent` sau committer / sau extension đều fsck strict rc 0, native không có cha, head trả 0 cha. Main control và hai biến thể trên head đều rc 12/failed; base control rc 12, hai biến thể rc 0/passed. Criterion head 3/3 rc 0; base control rc 0, hai biến thể rc 3. [Git](extension-finding.json), [main](extension-main-results.json), [criterion](extension-criterion-parent_after_committer-head.json). |
| `git-reader-fixture-domain-incomplete` | **ĐÓNG các biểu hiện cũ, lớp CÒN MỞ P2** | 14/14 mutant R/Y neo lại đúng head đều rc 3/GIET đúng c53, gồm Y01 cắt còn 2 cha và Y02 chỉ nhận cha 40 hex. Nhân chứng của cả hai dùng 3 cha thật, fsck strict rc 0; head đúng, mutant sai. Z01 mới vẫn sống và không tương đương; xem dưới. [R/Y](supplemental-mutant-results.json), [nhân chứng Y](new-mutation-witnesses.json). |
| X01–X06: đếm trường batch, thừa trường, payload ngắn/dài, UnicodeEncodeError, SubprocessError | **GIỮ ĐÓNG về test** | Tái dẫn xuất từng thay đổi lên mã head, không dùng nguyên sản phẩm cũ. 6/6 child rc 3 đúng c53. Các stdout bị cắt/thừa là phép tiêm lỗi giao thức, không tuyên bố Git bình thường sinh ra chúng. [Catalogue](x-mutant-catalogue.json), [receipt](x-replay-results.json). |
| X07–X11, bộ bọc lỗi reader | **Không xác nhận tín dụng giả cho X11** | 5/5 child rc 3 đúng c53; X07 dùng literal `text=True` với input str, báo UnicodeDecodeError. Lỗi import module và lỗi binding trước khi vào reader đều rc 4/TIN_DUNG_GIA. [Đối chứng](wrapper-controls.json), [X07](replay-X07_text_true.json), [X11](replay-X11_unrelated_reader_attributeerror.json). |

Không đếm lại R08 tương đương của lượt 1 như một survivor mới. Bộ đột biến đóng toàn reader không được chạy.

## Lớp còn mở

| slug | hạng | file:dòng | phép đo | hướng vá |
|---|---|---|---|---|
| `git-reader-fixture-domain-incomplete` | **P2** | `ops/ci_provenance_test.py:1095`–1121, fixture/oracle trong c53; vị trí đột biến sản phẩm `ops/ci_provenance.py:151` | Z01 thêm `lstrip()` cho mỗi dòng header: c53 rc 0, `--tat-ca-ca` đủ 53/53 ca rc 0. Bốn commit hợp lệ (mergetag và extension continuation, SHA-1/SHA-256), fsck strict rc 0: native/head trả đúng tree + 5 cha, Z01 trả None. Criterion riêng head rc 0, Z01 rc 3 trên cả 4 nhân chứng. | Bổ sung c53 bằng commit có header nhiều dòng, continuation giữ dấu cách và chứa dòng `tree <OID>` trong nội dung tag/extension; đối chiếu đủ tree và thứ tự cha với native Git, thêm mutant chuẩn hóa đầu dòng. Dùng cây/cha thật và fsck strict cho nhân chứng. Không cần sửa sản phẩm vốn đúng trên các ca này. |

Cùng nguyên nhân thiếu miền fixture với lượt trước nên giữ slug, không tạo lớp mới để xóa lịch sử.

### Phản chứng cụ thể cho Z01

Trong bản sao sản phẩm, thay đúng **một** biểu thức:

```python
# Neo ở dòng gán dong:
than[:int(loai[2])].split(b"\n\n", 1)[0].split(b"\n")
# Thay bằng:
[x.lstrip() for x in than[:int(loai[2])].split(b"\n\n", 1)[0].split(b"\n")]
```

Đây là thay đổi parser bỏ khoảng trắng đầu dòng, không gài SHA hay tên fixture. Một `mergetag` hợp lệ nhúng nội dung annotated tag, các dòng tiếp nối bắt đầu bằng dấu cách. Message của tag được phép có dòng `tree <OID>`; khi ở trong commit, nó là ` tree <OID>`. Z01 biến dòng đó thành trường tree cấp ngoài, khiến phép đếm thấy hai tree và trả None. Head giữ dấu cách nên đọc đúng.

[Script dựng fixture/đột biến](extra_domain.py), [cặp neo/thay và hash](extra-mutant-catalogue.json), [kết quả Z01](Z01_strip_header_lines-result.json), [53 ca của Z01](Z01_strip_header_lines-all-cases.json). Nhân chứng SHA-1 mergetag là **51d58674c8c066689d50d121f7333ce3720cd6c8**; bốn nhân chứng đầy đủ, raw bytes dạng hex, native output và rc fsck nằm trong [extra-fixtures.json](extra-fixtures.json). Đã ghi riêng payload mergetag thành object tag thật và chạy fsck strict rc 0 cho cả SHA-1/SHA-256: [mergetag-valid-tags.json](mergetag-valid-tags.json). Không dùng `--literally` cho những nhân chứng này.

[Criterion độc lập](continuation_criterion.py) dùng assertion của harness, chạy trong tiến trình con thật: **4/4 head rc 0**, **4/4 Z01 rc 3**, prefix `DO:r978_continuation_header_metadata:`; không chỉ dựa vào mã thoát script thu thập. [Receipt](continuation-criterion-results.json). Vì sai trên đầu vào Git hợp lệ và sống toàn bộ ca hiện có, Z01 là mutant **không tương đương**, đạt ngưỡng P2 của prompt. Không phải P3 chỉ về stdout Git bất khả sinh, cũng không phải lỗi head hiện tại.

Vá tại fixture/criterion c53 là lựa chọn nhỏ nhất: khóa việc giữ nguyên dấu cách continuation, tree thật và toàn bộ danh sách cha; mutant Z01 phải chết đúng assertion. Không nên vá bằng từ chối rộng `gpgsig`/`mergetag`, giải mã cả header, hoặc tự bỏ khoảng trắng vì có thể làm hỏng commit hợp lệ và tái mở F13. Dùng Git native trong kho không nông làm oracle; không suy sang hỗ trợ SHA-256 toàn tuyến main. Người xử lý finding/quyết định bước sau: executor và chủ kho/điều phối #978 theo budget hiện hành.

### Đo bổ sung và lựa chọn reader

Bộ mới có **22/22** commit trên SHA-1/SHA-256: root, một cha, octopus 5 cha không sắp xếp, `gpgsig` nhiều dòng, `mergetag` nhiều dòng, hai header cùng có mặt, encoding Latin-1, parent muộn trên commit có cha thật, message chứa metadata và continuation. Cả 22 có `hash-object` rc 0, native log rc 0, `fsck --strict` rc 0 và metadata head bằng oracle. Chỉ kiểm cấu trúc Git; không thực hiện xác thực mật mã của chữ ký. [Fixture](extra-fixtures.json), [lệnh Git](extra-git-commands.json).

Ba probe Z: Z01 sống không tương đương; Z02 đổi `break` thành `continue` bị giết c53 rc 3 (tái kiểm cơ chế F13 quét cả header); Z03 lấy `tree[-1]` thay `tree[0]` sống 53/53 nhưng **tương đương** do chốt `len(tree) == 1` trước khi trả. Z03 không tạo finding. [Kết quả](extra-mutant-results.json). Không tuyên bố đã vét hết đột biến reader.

**Đồng ý giữ `cat-file --batch` trong sản phẩm.** Tôi tạo clone nông depth 1 bằng transport filesystem cục bộ (`--no-local`, không mạng) từ commit octopus thật. Git xác nhận shallow=true; fsck strict rc 0. `git log -1 --no-walk --format=%T%n%P` trả tree và **0 cha**, còn `git_cuc_bo` giữ đúng **5 cha** từ object như kho đầy đủ. Dùng trực tiếp `%P` để thay reader sẽ làm mất quan hệ merge tại biên shallow, đúng mối lo của executor. [Clone](shallow-clone.json), [kết quả](shallow-results.json).

Oracle log trong c53 dùng kho không nông và đọc được OID cha dù các object cha tổng hợp không tồn tại. Điều đó đủ bắt Y01/Y02; không đồng nghĩa toàn bộ graph fixture c53 đã qua fsck. Các nhân chứng reviewer nêu trên có object cha thật và đã qua fsck riêng.

### Lưu ý hợp đồng M1–M3

`--batch` thay `-p` lấy đồng thời loại object gốc và bytes, không peel tag; thay đổi này đóng lớp non-commit cũ. Parent được lấy ở dãy liên tiếp ngay sau tree đầu, phù hợp native Git trong các phép đo.

M2 đóng băng viết **“Chỉ `UnicodeDecodeError` được đổi thành tín hiệu chốt … lỗi khác giữ nguyên là vô can.”** Bộ bọc hiện chuyển mọi Exception có frame reader thành `NEM:<lớp>`; câu chữ chưa khớp. X11 ném ngay trong reader, vi phạm hành vi dict/None; việc giết X11 được chứng minh bằng đối chứng, không đủ để tự sửa nghĩa M2. Giữ lưu ý này cho chủ kho xác nhận bằng hồ sơ có thẩm quyền; không tự sửa đặc tả hoặc che chênh lệch. Finding P2 bên trên không dựa vào tranh luận câu chữ này.

M3 gọi tên `F13_doc_text_true`, catalogue dùng `F13_giai_ma_toan_stdout`; đã chạy thêm X07 literal text=True và bị giết rc 3. N3 nêu tăng 3 mutant, catalogue thực tăng 26; báo đúng số đo, không tuyên bố khớp nguyên văn +3.

## N1–N7

| Tiêu chí | Trạng thái | rc và bằng chứng dương |
|---|---|---|
| N1 | **passed** | Head c53 rc **0**; test head với mã base rc **3**, `DO:c53_git_commit_khong_utf8:` chứa UnicodeDecodeError. [Head](n1-head.json), [base](n1-base.json). |
| N2 | **passed về hành vi đột biến** | Lệnh import/`chay_dot_bien` đúng prompt rc **0**, **26/26 GIET**. Chạy lại từng child: **26/26 rc 3** đúng c53, 0 rc 4. Literal text=True cũng được đo như trên. [Runner](n2-prescribed.json), [child](f13-children.json). |
| N3 | **not_run** | Không chạy suite mặc định ~40 phút. Đã chạy riêng `--tat-ca-ca`: outer rc **0**, JSON **53/53** ca, từng rc **0**. AST catalogue base **52 ca/292 mutant**, head **53 ca/318 mutant**; không khai 318/318 hoặc suite mặc định passed. [Ca](all-head-cases.json), [tổng hợp](all-head-summary.json), [catalogue](catalogue-counts.json). |
| N4 | **passed** | Ruff `--no-cache --select F` trên hai tệp head/base đều rc **0**, `All checks passed!`, delta F=0. `git diff --check base HEAD` rc **0**. Đây là bare Ruff, không phải receipt pin/probe Ruff của CI. [Head](n4-head-ruff.json), [base](n4-base-ruff.json), [diff](n4-diff-check.json). |
| N5 | **passed** | doctrine-scan rc **0**, **10 tệp/0 chỗ chép**; adr-song rc **0**, **55 ADR/55 dòng**, khớp 1–1, output ghi ngoại lệ trạng thái ADR-0016. [Doctrine](n5-doctrine-scan.json), [ADR](n5-adr-song.json). |
| N6 | **not_measured** | Offline, không đọc check run ci.yml trên GitHub; không dùng lời khai executor thay kết quả đo. |
| N7 | **not_applicable; not_run** | `git_cuc_bo` không thuộc `HAM_DONG`; không chạy `--dot-bien-dong`, không khai passed. [Catalogue](catalogue-counts.json). |

## Định danh, phạm vi, toàn vẹn

- HEAD detached **aa2a1f326eb964b1cf8f45454593971e0ab11b73**, tree **dc762d40a2c3e60bcbebc2bf78c38addc611c25d**. Tự kiểm đúng chuỗi base **c8d92ba05c3ea875d8f84d94195430302690286d** → **bef14035718cae862369101f79dc61e938ae6b00** → **7fcfe18181ce4d089225900e36d3aed878877e7f** → **fdf1f05c1b3d845a694c796a81a8bd5c218a68c8** → head; local origin/master trỏ base. SHA-256 đặc tả khớp đủ 64 ký tự. [Preflight](preflight.json).
- Diff base..head đúng **2 tệp, +116/-6**; vượt dự kiến 60 dòng thêm nhưng dưới trần ADR-0053 6 tệp/450 dòng. Đã đọc diff lượt 3..head và toàn diff sản phẩm. So AST: chỉ hàm `git_cuc_bo` thay đổi, thêm hằng regex OID; main, moc_checkout, git_blob, REST và doc_wf không đổi. [Diff](diff.patch), [diff lượt 3](step1-diff.patch), [numstat](numstat.txt), [AST](ast-scope.json).
- Assignment wp978 revision 1/generation 1, sensitive; đã đọc bản lease. Freshness remote và lời nâng trần trên GitHub không được đo; lượt offline 4/4 theo prompt hiện tại. Không lấy trần 2 trong lease/spec cũ để xin lại quyền đã được assignment cấp.
- Reviewer Codex/họ OpenAI theo session; launcher ghi `openai_codex`, `codex_cli`, transport `machine`, run **cbf632208a6442b0a2d99764327cf91c**. Exact serving model/effort **not_measured**. Executor họ Claude theo assignment/lease, không tự đo runtime. Không có context executor hoặc subagent. `assurance_target: cross_approved` là mục tiêu; verdict request_changes này không cấp assurance approved. [Identity](identity.json).
- Linux, Python **3.13.17**, Git **2.43.0**, PyYAML **6.0.3**, Ruff **0.17.3**. [Versions](versions.json).
- Mọi phép thử chạy trên bản sao `out/head`, fixture/mutant dưới OUT. Dùng Python `-B`, PYTHONDONTWRITEBYTECODE=1, TMPDIR tuyệt đối dưới OUT, Git global/system config `/dev/null`, optional locks tắt, Ruff no-cache. Danh tính Git fixture là dữ liệu giả. Không mạng, không GitHub, không push/merge/land; không cài công cụ, không sửa SRC.
- Snapshot cuối: **7205/7205** tệp tracked SRC giữ nguyên SHA-256, head/tree/spec hash không đổi; status gồm untracked/ignored rỗng cả đầu/cuối, tracked/index diff rỗng. Bản sao head cũng khớp 7205 tệp source. Không suy đây là kiểm mọi byte `.git` hoặc chứng minh lịch sử chưa từng ghi rồi hoàn nguyên. [Snapshot cuối](final-source-snapshot.json), [audit số liệu](final-evidence-audit.json).

Lệnh đầy đủ, cwd, rc, stdout/stderr và thời lượng của các check nằm trong receipt JSON; các lệnh Git dựng/đối chiếu fixture có rc/output riêng. Script điều phối: [bootstrap](bootstrap.py), [bước 2](phase2.py), [N/checks](checks.py), [replay X](replay_x.py), [miền mới](extra_domain.py), [criterion mới](continuation_witness.py), [audit cuối](final_audit.py). Khi tái lập, dùng OUT mới và bản sao riêng; các script dựng kho không phải thiết kế để chạy đè nhiều lần trên fixture cũ. [Lịch sử verdict tạm](VERDICT.progress.md).

D02 và F10/D05 của #899, `.claude/dev/ci_dang_ky_test.py --chay`, mốc Workflow definition, LIVE CI, Windows native và SHA-256 toàn tuyến main ngoài phạm vi; không tính hạng hoặc tuyên bố đã đo. Không soạn hay thử nội dung đường dẫn thoát cây.
