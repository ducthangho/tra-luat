Verdict: request_changes
Reviewed commit: bef14035718cae862369101f79dc61e938ae6b00
Spec sha256: eccd6dd2917f76d6158d5c9574f4d4c2070ba22ef3da96b4dfcf6e820c301638

| slug | hạng P0–P3 | biểu hiện file:dòng | phép đo/tái hiện đã chạy | hướng vá |
|---|---|---|---|---|
| `git-object-type-not-checked` | **P2** | `ops/ci_provenance.py:137–145`, qua `moc_checkout:245–254` | Git xác nhận object là **blob**, nhưng reader trả tree/parents và `main` ghi checkout `passed`, rc 0. Criterion độc lập đỏ đúng rc 3 trên cả head/base. [Bằng chứng](independent-main-results.json), [criterion](criterion-r978_noncommit_must_be_none-head.json). | Xác minh loại object gốc là commit trước khi lấy metadata; thêm blob có header OID hợp lệ, tree và annotated tag vào ca âm. |
| `git-header-cr-split-creates-parents` | **P2** | `ops/ci_provenance.py:143–144`, qua `moc_checkout:252–254` | Commit có CR trong author qua `git fsck --strict` rc 0; Git đọc **0 parent**, reader đọc **1 parent giả**. `main` đối chứng rc 12, biến thể CR rc 0/checkout `passed`; cả head/base. [Git](cr-author-results.json), [main](cr-author-main-results.json). | Tách dòng header theo LF của định dạng Git; không để CR bên trong giá trị author trở thành dòng `parent`. Khoá bằng đối chiếu parents native và ca main âm. |
| `git-reader-fixture-domain-incomplete` | **P3** | `ops/ci_provenance_test.py:1071–1093` | **10 mutant không tương đương vẫn qua 53/53 ca**; 1 mutant tương đương cũng sống. Bỏ hoàn toàn kiểm số tree gây rc 4, không được tính giết đúng. [Kết quả](supplemental-mutant-results.json), [phản chứng](mutation-witnesses.json). | Mở miền fixture cho SHA-256, độ dài/ký tự OID, parent lỗi, nhiều tree, body giống header, loại object và lỗi chạy Git; giữ phân biệt rc 3/4. |

**P0=0, P1=0, P2=2, P3=1; đếm theo ba nguyên nhân.** Hai P2 là lỗi có sẵn ở base, không phải hồi quy do diff này. Chúng vẫn nằm trong reader được giao review không lọc và mâu thuẫn hợp đồng metadata; vì còn P2 nên không approve. P3 là nợ độ phủ test, không biến yêu cầu N2 từ ba mutant thành một tập đóng mới.

F13 `git-commit-body-encoding-lam-hong-metadata` của review A **đã vá thật trong các biểu hiện được giao và đã đo**: message/author không UTF-8 và blob không UTF-8. Hai P2 trên có nguyên nhân khác F13; không gọi chúng là F13 tái mở. Verdict này chỉ neo commit ở dòng 2, không cấp quyền push, merge, land hay deploy.

**Định danh và phạm vi tự kiểm**

- Base `c8d92ba05c3ea875d8f84d94195430302690286d` là cha trực tiếp của head; `origin/master` trong clone trỏ đúng base. Detached HEAD; tree `2467466bf3f081f0857dc1ef9f67860b84abea9c`.
- SHA-256 đặc tả khớp đầy đủ. Đã đọc lease `wp978-r1-g1-claude`, revision 1/generation 1/review class sensitive. Freshness của lease/remote không xác minh online; authority cho lượt read-only này là prompt được giao.
- [Diff](diff.patch): đúng `ops/ci_provenance.py` (+9/-5) và `ops/ci_provenance_test.py` (+29/-0), tổng **2 tệp, +38/-5**, dưới cả dự kiến 60 dòng thêm và trần 6 tệp/450 dòng thêm. So AST của mọi hàm/lớp sản phẩm cho thấy chỉ `git_cuc_bo` đổi; `git_blob`, `doc_wf`, REST, `moc_checkout`, `main` giữ nguyên.
- Mọi phép thử chạy trên `out/head` hoặc fixture/mutant trong `out/`; `src/` chỉ đọc. Python bytecode tắt; `TMPDIR=out/tmp` tuyệt đối; `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_SYSTEM=/dev/null`, `GIT_OPTIONAL_LOCKS=0`; Ruff `--no-cache`.
- Linux, Python **3.13.17**, Git **2.43.0**, PyYAML **6.0.3**, Ruff **0.17.3**. Đây là bare lint, không phải kiểm pin/probe Ruff của CI.
- [Identity](identity.json): launcher run `9a9441ce01d44929b9074b69b73902ee`, `openai_codex`, `codex_cli`, transport `machine`; họ GPT-6 theo chỉ dẫn phiên. Không có header CLI đủ model/effort trong stderr: **exact serving model/effort chưa đo được**, không mượn identity của review A. Executor thuộc họ Claude theo assignment/lease, không có phép đo runtime độc lập của executor. Không cấp `cross_approved` từ lượt request_changes này.

**Đối chiếu M1–M3 và N1–N7**

| Tiêu chí | Trạng thái | Kết quả tự đo / giới hạn |
|---|---|---|
| M1 | Đạt phần sửa F13; còn lỗi hợp đồng reader | `cat-file -p` trả bytes; tách body trước; OID 40/64 lowercase hex; chỉ giải mã ASCII sau kiểm; chữ ký không đổi. Hai P2 ở bảng lớp cần xử lý riêng. |
| M2 | passed | `c53` có đo, không return sớm: head rc 0; base đỏ đúng UnicodeDecodeError. Git thật dựng ba commit, ca main sinh provenance và đối chiếu tree/parents. Phép đo reviewer dùng cả parent object thật và workflow blob thật. |
| M3 | passed | Đúng ba tên F13 trong catalogue, đích c53; ba child rc 3 và `DO:c53_git_commit_khong_utf8:`. |
| N1 | **passed** | Head rc 0; cùng ca + `CI_PROVENANCE_MA=out/base/ops/ci_provenance.py` rc 3, `DO:c53_…: … UnicodeDecodeError`. Hai kết quả đúng kỳ vọng **2/2**. [Head](n1-head.json), [base](n1-base.json). |
| N2 | **passed** | Lệnh được yêu cầu gọi `t.chay_dot_bien(*x)` đã chạy rc 0, **3/3 GIET**. Chạy lại riêng ba child giữ rc/output đầy đủ: **3/3 rc 3**, đúng ca, không rc 4. [Runner](n2-prescribed.json), [child](mandatory-mutants-results.json). |
| N3 | **not_run** cho suite mặc định | Không chạy `python -B ops/ci_provenance_test.py` (~40 phút gồm 295 mutant). Đã chạy riêng **53/53 ca**, rc 0; chạy lại đúng 9 ca Git bắt buộc **9/9**, mỗi ca rc 0. Chưa xác nhận `DOT BIEN: 295/295`, `TONG: DAT` hay toàn suite base. [53 ca](all-head-cases.json), [9 ca](final-checks-results.json). |
| N4 | **passed** | Bare Ruff head/base đều rc 0, `All checks passed!`: **2/2**, delta F=0. `git diff --check HEAD^ HEAD` rc 0; diff +38/-5 đọc được. [Head](n4-head-ruff.json), [base](n4-base-ruff.json), [diff check](n4-diff-check.json). |
| N5 | **passed** | `doctrine-scan --root .` rc 0: quét **10 tệp**, 0 chỗ chép; `adr-song --root .` rc 0: **55 ADR/55 dòng**, khớp 1–1. Hai gate **2/2**. [Doctrine](n5-doctrine.json), [ADR](n5-adr.json). |
| N6 | **not_measured** | Không truy cập mạng/GitHub theo prompt; không có check run `ci.yml` trên exact head được tự đọc. Không nhận lời khai xanh thay bằng chứng. |
| N7 | **not_applicable; not_run** | Không chạy `--dot-bien-dong`: `git_cuc_bo` không thuộc `HAM_DONG`. Không khai đạt. [Catalogue/HAM_DONG](catalogue-counts.json). |

Đếm AST catalogue: base **52 ca/292 mutant**, head **53 ca/295 mutant**, delta đúng **+1/+3**. Đây là đếm khai báo, không phải receipt chạy suite base/head. N3 và N6 vẫn thiếu bằng chứng đầy đủ ngay cả nếu vá xong các finding.

**Phép đo độc lập đóng F13 và các biên**

[Script](independent.py) dùng helpers REST của suite sau khi đọc mã, nhưng tự tạo kho SHA-1/SHA-256, tree chứa workflow thật và ba parent commit thật. Thứ tự parent cố ý không sắp xếp; `git show --format=%T%n%P` là đối chứng native. Không gọi `c53` để làm oracle cho phép đo này. Đã đọc hai script review A; không nhận kết quả cũ, không chạy lại script thiếu `encoding_child.py` trong bộ tham chiếu.

| Phép đo | Kết quả |
|---|---|
| Root và 7 biến thể commit trên mỗi định dạng Git | **16/16** head trả đúng tree/parents dạng `str`, đúng thứ tự. Có UTF-8, Latin-1 message, Latin-1 author, cả hai, không có encoding header, body giống metadata, extension header không UTF-8. |
| Main thật, reader metadata và workflow Git thật, REST giả | **7/7** biến thể SHA-1 trên head: child rc 0, có provenance, checkout `passed`, đúng tree/parents. **3/3** biến thể Latin-1 bắt buộc (message, author, cả hai) trên base: child rc 1/UnicodeDecodeError, không có provenance; UTF-8 base rc 0. [Raw](independent-main-results.json). |
| SHA-256 | **8/8** commit reader đúng OID 64 ký tự. Không suy ra main hỗ trợ SHA-256 toàn tuyến: `RE_SHA`/`RE_HEX40` vẫn giới hạn 40 trong phần mã không đổi; main SHA-256 chưa chạy. |
| Tree, annotated tag thông thường, blob thường, blob không UTF-8, tree/parent lỗi, độ dài OID sai, uppercase, metadata chỉ trong body, SHA thiếu/rỗng/không hợp lệ, PATH không có git | Head trả None ở các ca âm tương ứng. Blob chứa header OID hợp lệ và blob chứa CR tạo dòng metadata là ngoại lệ sai được ghi P2; không nói mọi non-commit đã đạt. |
| Lỗi chạy Git | Git thiếu thật trên PATH và SHA không tồn tại đã đo. Fault injection rc 128 có stdout giống commit, OSError, TimeoutExpired, SubprocessError: **4/4** trả None. [Edges](runtime-error-edges.json). |
| Tổng quan sát reader | **46/50** khớp hợp đồng; bốn sai khác là hai dạng blob × hai định dạng OID, cùng lớp thiếu kiểm loại object. Phép đo CR trong **commit thật** được giữ riêng ở finding thứ hai. [Raw](independent-results.json). |

**Chi tiết P2 và hướng xử lý**

`git-object-type-not-checked`: object `53ccbfc481e6262a236b458c06ddf81a6b66e756` có loại `blob`. Bytes đầu chứa tree `e5ba99e78ade86c08b2157d66ca6107d66b92a02` và parent `d48d1a98a44dd4318006e063659e40b128f7d685`. `cat-file -p` không xác thực loại; kiểm regex chỉ xác thực chuỗi OID. Reader trả chính hai giá trị này. Qua REST/log fixture chỉ vào SHA blob, `main` rc 0, checkout `passed` với lý do `head_sha_trong_parents_merge_tong_hop`. [Provenance](main-artifacts/sha1-commit_shaped_blob-head/provenance.yaml). Docstring dòng 137 hứa non-commit trả None nhưng không đúng. Chưa chứng minh một checkout Git bình thường tự phát log SHA blob; bằng chứng chứng minh sai hợp đồng reader và khả năng mốc checkout nhận metadata của blob khi log fixture tham chiếu nó.

Vá ở reader để mọi caller dùng cùng kiểm loại; giữ đường bytes và phân biệt object gốc với đối tượng được peel. Chỉ đổi `-p` thành `commit` chưa đủ: mutant R09 tự peel annotated tag và vẫn sống 53/53. Test cần đòi blob/tree/tag trả None, commit Unicode/Latin-1/SHA-256 vẫn trả metadata; thêm mutant bỏ kiểm loại phải chết đúng ca. Rủi ro cần kiểm là mất hỗ trợ commit hợp lệ, vô tình chấp nhận tag được peel hoặc đổi hành vi khi Git không đọc được object. Không cần đổi REST hay main để vá lớp này.

`git-header-cr-split-creates-parents`: object commit `da7c54fccbb740860d074ebbacc999547f44ca10` có **0 dòng parent** theo Git. Author chứa CR bao quanh một đoạn giống `parent <OID>`; `bytes.splitlines()` coi CR là xuống dòng, dù header Git được phân cách bằng LF. Git native trả parents rỗng, `git fsck --strict` rc 0 và `git merge-base --is-ancestor` đối với OID bị nhận nhầm trả rc 1. Head lẫn base lại trả parent `604b1b137d09909fb0769c158d7209e7120b23bf`.

[Script tái hiện](cr_author.py) chạy main với cùng REST head là commit không liên quan: control không có CR **rc 12/checkout failed**; author có CR **rc 0/checkout passed**. [Provenance sai](main-artifacts/cr-author-carriage_return-head/provenance.yaml). Đây là sai parents của một commit mà Git chấp nhận, không phải chỉ lỗi lời mô tả. Tiêu chí độc lập [r978_author_must_not_create_parent](criterion-r978_author_must_not_create_parent-head.json) đỏ rc 3 đúng lý do.

Vá đúng bộ tách dòng bytes trong `git_cuc_bo`, giữ CR trong giá trị của dòng author và chỉ nhận tree/parent ở ranh giới LF. Test cần đối chiếu Git native, commit root/merge, Latin-1 author, nội dung message giống header và main đối chứng âm; mutant đưa lại cách tách dòng rộng phải chết đúng assertion. Rủi ro là xử lý thiếu ranh giới header/body hoặc vô tình chuẩn hoá dữ liệu trước khi kiểm OID. Kiểm loại object ở finding thứ nhất không đóng lớp này, vì object ở đây thật sự là commit; hai finding cần hai chốt riêng.

Hai criterion reviewer đều trả **rc 3 + `DO:<đúng ca>:` trên head và base (4/4 phản chứng đúng)**; không dùng rc 0 của script thu thập để gọi tính chất lỗi là passed. [Script tiêu chí](finding_criteria.py), [receipt](final-checks-results.json).

**Đột biến bắt buộc và đột biến bổ sung**

| Mutant bắt buộc | Child rc / hạng | Lý do thực tế |
|---|---|---|
| `F13_doc_text_true` | 3 / GIET | UTF-8 decoder đọc message Latin-1 trước khi có bytes, `UnicodeDecodeError`. |
| `F13_giai_ma_ca_phan_dau` | 3 / GIET | Decoder đọc author Latin-1 trong header, `UnicodeDecodeError`. |
| `F13_bo_kiem_oid` | 3 / GIET | Blob `tree zz` trả metadata thay vì None, sai assertion danh sách kết quả. |

Các ca mục tiêu đều xanh trước khi đột biến. Ba child trên có đầy đủ `DO:c53_git_commit_khong_utf8:` trong raw output; phần tail của runner có thể cắt prefix nhưng không được dùng để tự suy hạng.

[Script mutant](supplemental_mutations.py), [cặp neo/thay và hash](supplemental-mutant-catalogue.json), [kết quả](supplemental-mutant-results.json), [script nhân chứng](mutation_witnesses.py). Mọi mutant sống c53 được chạy tiếp **toàn bộ 53 ca** qua `--tat-ca-ca`; kiểm JSON đủ 53 phần tử, mọi rc=0, không chỉ tin rc tiến trình ngoài.

| Mutant reviewer | Kết quả | Tương đương? / nhân chứng đã chạy |
|---|---|---|
| R01 `oid_only40` | SONG_SOT, **53/53**, rc 0 | Không: commit SHA-256 hợp lệ bị trả None. |
| R02 `oid_range` | SONG_SOT, **53/53**, rc 0 | Không: nhận OID dài 41 ký tự; head từ chối. |
| R03 `oid_loweralnum` | SONG_SOT, **53/53**, rc 0 | Không: nhận giá trị 40 ký tự `g`, không phải hex. |
| R04 `accept_multiple_trees` | SONG_SOT, **53/53**, rc 0 | Không: hai dòng tree được lấy dòng đầu; head trả None. |
| R05 `remove_tree_count` | **TIN_DUNG_GIA**, c53 rc 4 | IndexError khi danh sách tree rỗng. Không cộng GIET; khác head, nhưng tín hiệu không đúng assertion. |
| R06 `header_crlf` | SONG_SOT, **53/53**, rc 0 | Không: không cắt header/body tại LF-LF; body giống metadata làm commit hợp lệ bị trả None. |
| R07 `read_body` | SONG_SOT, **53/53**, rc 0 | Không: đọc tree/parent trong message; cùng nhân chứng body_metadata như R06. |
| R08 `replace_full_stdout` | SONG_SOT, **53/53**, rc 0 | **Tương đương về kết quả reader** trong mô hình bytes này; xem chứng minh dưới. Cách làm vẫn trái cấm rõ của M1, không đề nghị dùng. |
| R09 `catfile_commit` | SONG_SOT, **53/53**, rc 0 | Không: annotated tag được peel thành commit; head trả None, mutant trả metadata. |
| R10 `catfile_blob` | **GIET**, c53 rc 3 | Ba commit hợp lệ trả None; `DO:c53_…:`. |
| R11 `reverse_parents` | **GIET**, c53 rc 3 | Thứ tự parents khác kỳ vọng; `DO:c53_…:`. |
| R12 `validate_tree_only` | SONG_SOT, **53/53**, rc 0 | Không: parent `zz` được trả ra; head từ chối. |
| R13 `ignore_invalid_bytes` | SONG_SOT, **53/53**, rc 0 | Không: byte không ASCII trong OID bị xoá trước kiểm; giá trị lỗi trở thành hợp lệ. |
| R14 `drop_oserror` | SONG_SOT, **53/53**, rc 0 | Không: PATH không có git làm FileNotFoundError nổi lên; head trả None. |

Tổng **14 mutant: 2 GIET + 1 TIN_DUNG_GIA + 11 SONG_SOT**; trong 11 sống có **10 không tương đương**, đều có phản chứng phân biệt head/mutant **10/10**, và 1 tương đương. Các object cố ý hỏng metadata trong nhân chứng được dựng bằng `hash-object --literally`; không gọi chúng là commit hợp lệ. Nhân chứng SHA-256, body_metadata và annotated tag dùng object hợp lệ.

R08 giải mã UTF-8 với replacement rồi encode UTF-8 lại **trước cùng parser bytes**. Các dấu phân cách, tên trường và mọi OID được chấp nhận đều là ASCII; phép vòng này không tạo/xoá ASCII. Byte không ASCII nằm trong giá trị OID vẫn không thể qua regex, còn ở author/body thì bị bỏ qua. Vì vậy không thay kết quả metadata/None với cùng stdout/returncode; khảo sát bốn vị trí × 256 byte cho **1024/1024** bằng nhau ([raw](replacement-equivalence-sample.json)). Đây không phải chứng minh tương đương của mọi cách dùng `errors="replace"`: chuyển sang parser chuỗi có `str.splitlines()` sẽ có miền dấu phân cách khác. M1 cấm phương pháp thay ký tự trên toàn stdout dù biến thể cụ thể này tương đương quan sát.

P3 đề nghị bổ sung ca theo các miền trên và hai ca P2, thay vì chỉ thêm nhiều tên mutant. Chỗ cần sửa là fixture/criterion của reader; rủi ro là dùng mock thay Git thật làm mất kiểm loại object hoặc biến lỗi ngoại lệ vô can thành tín dụng. Người cần quyết định xử lý nợ: chủ kho/điều phối #978; chưa có quyết định giữ nợ mới trong bundle. N7 không yêu cầu đóng toàn bộ mutant reader, nên không hạ kết quả N2 đã đạt vì các mutant bổ sung.

**Lệnh, giới hạn và toàn vẹn**

Các receipt JSON lưu command, cwd, env override, rc, thời lượng, stdout/stderr. Các lệnh chính đã chạy từ bản sao:

```text
python -B ops/ci_provenance_test.py --mot-ca c53_git_commit_khong_utf8
CI_PROVENANCE_MA=<out/base/ops/ci_provenance.py> python -B ops/ci_provenance_test.py --mot-ca c53_git_commit_khong_utf8
python -B -c '<lệnh import và t.chay_dot_bien cho F13 trong prompt>'
python -B ops/ci_provenance_test.py --tat-ca-ca
python -B ops/ci_provenance_test.py --mot-ca <c05/c06/c07/c08/c09/c22/c32/c34/c53, tên đầy đủ trong receipt>
python -B -m ruff check --no-cache --select F ops/ci_provenance.py ops/ci_provenance_test.py
git diff --check HEAD^ HEAD
python -B .claude/dev/packet_loop.py doctrine-scan --root .
python -B .claude/dev/packet_loop.py adr-song --root .
```

Script reviewer chạy từ thư mục chứa PROMPT.md: `python -B out/independent.py`, `python -B out/cr_author.py`, `python -B out/supplemental_mutations.py`, `python -B out/mutation_witnesses.py`, `python -B out/final_checks.py`. Script thu thập rc 0 chỉ chứng minh thu thập hoàn tất; kết quả sản phẩm/criterion được giữ riêng trong bảng và receipt. Các tiến trình thử độc lập có chạy đồng thời; không gọi subagent hay phiên model phụ.

N3 suite mặc định, N6 CI exact SHA, LIVE, Windows native và bộ `ci_dang_ky_test.py --chay` **không chạy/chưa đo** như đã ghi; không nhận các số executor khai làm kết quả reviewer. D02 và F10/D05 của #899 ngoài phạm vi, không cộng hạng và không tuyên bố đã đóng. Không thử hay tự soạn nội dung đường dẫn thoát cây; hướng đó không cần để tái hiện các finding hiện tại.

Source đầu/cuối: **7205/7205 tệp tracked cùng SHA-256**, HEAD/tree không đổi, tracked/index diff rỗng, trạng thái cuối cả untracked/ignored rỗng. [Đầu](preflight.json), [cuối](final-source-snapshot.json). Snapshot đầu không lưu riêng trạng thái ignored; không suy rộng thành kiểm toàn bộ byte `.git` hay chứng minh lịch sử chưa từng ghi rồi hoàn nguyên. Không sửa source, không GitHub, không mạng, không push/merge/land. Tiến trình ghi báo cáo tăng dần được giữ trong [VERDICT.progress.md](VERDICT.progress.md); bản này là kết luận cuối.
