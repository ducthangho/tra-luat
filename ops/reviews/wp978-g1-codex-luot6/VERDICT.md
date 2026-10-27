Verdict: request_changes
Reviewed commit: 2c907a47e22c7b0706df766176180a798ed7f69f
Spec sha256: eccd6dd2917f76d6158d5c9574f4d4c2070ba22ef3da96b4dfcf6e820c301638

**P0=0, P1=0, P2=1, P3=0.** Còn lớp `git-reader-fixture-domain-incomplete`. Toàn bộ **22 survivor không tương đương của lượt 5 đã bị khóa đúng**, nhưng quét tiếp ranh giới header/body và dãy parent tìm thấy **10 mutant khác sống c53**: 8 sai so với Git native, 2 sai quy tắc M1 trên commit hợp lệ. Đây là **một lớp thiếu miền fixture**, không phải 10 finding độc lập. Mã sản phẩm head đúng trên toàn bộ 86 nhân chứng hợp lệ của phép quét mới.

Verdict neo đúng SHA ở dòng 2; không cấp quyền push, merge hay land. Mọi phép thử chạy trong OUT; SRC không đổi. Không chạy suite mặc định ~40 phút. [Audit số liệu](final-evidence-audit.json), [lịch sử verdict tạm](VERDICT.progress.md).

**ĐỐI CHIẾU LƯỢT TRƯỚC**

Đã đối chiếu lượt 1, bản tạm lượt 2, lượt 3, 4, 5. Kết quả dưới đây được tự đo ở lượt này. Mã sản phẩm tại `afcadd5`, `aa2a1f3` và head giống hệt nhau; diff lượt này chỉ đổi test. [AST/scope](ast-scope.json), [diff lượt này](step1-diff.patch).

| Lớp / biểu hiện | Trạng thái | Phép đo lượt 6 |
|---|---|---|
| `git-commit-body-encoding-lam-hong-metadata` | Giữ đóng | N1 head rc0/base rc3 có UnicodeDecodeError. Reader độc lập 26/26 đúng trên SHA-1/SHA-256, gồm Latin-1 author/message và extension không UTF-8. Main head trên các commit này rc0/checkout passed; base ném UnicodeDecodeError. [Reader](regression-reader.json), [main](regression-main.json). |
| `git-object-type-not-checked` | Giữ đóng | Blob dạng commit, blob không UTF-8, tree/tag đều None trên hai định dạng. Main blob dạng commit: head rc0 nhưng checkout **not_measured**, base rc0/checkout passed; không đánh đồng outer rc0 với passed. |
| `git-header-cr-split-creates-parents` | Giữ đóng | Commit CR-author có graph thật, fsck strict rc0, native/head không có cha. Main control/CR head rc12/12, đều failed; base rc12/0. |
| `git-header-extension-creates-parents` | Giữ đóng | Parent sau committer hoặc extension: fsck strict rc0; native/head không nhận làm cha. Main head cả hai rc12/failed; base rc0/passed. |
| `git-reader-fixture-domain-incomplete` | Đóng các biểu hiện lượt 5; **lớp còn P2** | D01–D49: 39 rc3 đúng DO:c53, gồm đủ 22 survivor không tương đương cũ; chỉ 10 tương đương còn sống. Quét mới 33 mutant phát hiện 10 survivor không tương đương, trình bày bên dưới. [Đối chiếu D](D-audit.md), [raw và lý do](D-reason-audit.json). |
| Lỗi giao thức batch, OID, SHA-256, số/thứ tự cha, lỗi chạy Git đã đóng | Giữ đóng về test | F13 tương ứng đều rc3 đúng c53; bao gồm header thừa trường, payload cụt/dài, rc khác 0, kiểu SHA, UnicodeEncodeError/SubprocessError/OSError, số tree và OID. Toàn bộ 43 child F13 có DO đúng ca, không rc4. [Catalogue neo/thay](f13-catalogue.json), [receipts](checks-summary.json). |
| Bộ bọc lỗi reader / X11 | Không có bằng chứng tín dụng giả | AttributeError trong reader rc3; lỗi import và lỗi binding ngoài frame reader đều rc4. Literal `text=True` + input str rc3, có UnicodeDecodeError. [Đối chứng](wrapper-controls.json). |

Các phép main dùng REST/workflow giả của harness, reader Git thật; không tuyên bố đo mạng, workflow Git thật hoặc SHA-256 toàn tuyến main. Các ngoại lệ base trong script độc lập được ghi là exception, không gán thành mã thoát tiến trình con. N1 có rc thật riêng.

**Bảng lớp còn mở**

| slug | hạng | file:dòng | phép đo | hướng vá |
|---|---|---|---|---|
| `git-reader-fixture-domain-incomplete` | **P2** | `ops/ci_provenance_test.py:1095`, `:1098`, `:1107`, `:1121`, `:1126`; mutation tại `ops/ci_provenance.py:151`, `:156`, `:159` | 10 mutant sống c53 rc0; 20 nhân chứng mutant × định dạng: head criterion rc0, mutant rc3 đúng DO. Sáu đại diện sống đủ 53/53 ca mỗi bản. Tất cả nhân chứng có tree/parent thật, hash-object không dùng --literally, fsck strict rc0. | Bổ sung fixture theo các nhóm: dấu ngăn đầu tiên và message nhiều đoạn; dòng continuation chỉ có whitespace; header không có body; giữ multiplicity/thứ tự/toàn bộ parent, kể cả octopus dài. Dùng graph thật, kiểm fsck; tách oracle native khỏi None theo M1; thêm mutation cho các nhóm. |

Không có P3 mở trong phạm vi. Owner xử lý: executor wp978 và chủ kho/điều phối #978. Giữ slug cũ; không chuyển nợ hay đổi tên để xóa lịch sử. Các số trên chứng minh thiếu độ phủ, không chứng minh reader head đang sai. Hướng vá nhỏ nhất nằm ở fixture/criterion và catalogue, không đòi sửa sản phẩm đang đúng trên nhân chứng.

**10 survivor mới và nhân chứng phân biệt**

[Script quét](boundary_sweep.py), [33 cặp neo/thay nguyên văn và SHA-256](boundary-catalogue.json), [kết quả c53](boundary-c53-results.json), [122 phép dựng fixture và raw bytes](boundary-fixtures.json), [lệnh Git](boundary-git-commands.json), [tổng hợp mutant/nhân chứng](boundary-summary.json).

| Mutant | Thay đổi thực tế | Nhân chứng strict-valid | Kết quả |
|---|---|---|---|
| B01 `last_blank` | `split(b"\n\n", 1)` → `rsplit(b"\n\n", 1)` | `body_middle_metadata`, `body_start_metadata_then_blank`, `literal_blank_inside_extension` | Đọc metadata trong message trước dấu ngăn cuối; head/native đúng, mutant None. **Native**. |
| B03 `space_blank` | Coi `\n[ \t]*\n` là ranh giới header/body | `continuation_blank_20`, `_09`, `_2009` | Cắt sớm tại dòng SP/TAB, bỏ tree bổ sung phía sau; head None, mutant dict. **M1**. |
| B07 `strip_payload_first` | `.strip()` toàn payload trước tách header | `empty_tree_no_body` | Commit có extension `tree ` rồi LF, không body; strip xóa dấu cách và biến `tree ` thành `tree`. Head None, mutant dict. **M1**. |
| P09 `dedup` | Chỉ append nếu OID chưa có trong cha | `duplicate_parent` với dãy A,B,A | Native/head giữ đủ A,B,A; mutant còn A,B. Git hash-object và fsck strict đều rc0. **Native**. |
| P_cap_003 | Trả `cha[:3]` | octopus 5 cha thật | Native/head 5; mutant 3. |
| P_cap_004 | Trả `cha[:4]` | octopus 5 cha thật | Native/head 5; mutant 4. |
| P_cap_008 | Trả `cha[:8]` | octopus 17 cha thật | Native/head 17; mutant 8. |
| P_cap_016 | Trả `cha[:16]` | octopus 17 cha thật | Native/head 17; mutant 16. |
| P_cap_064 | Trả `cha[:64]` | octopus 65 cha thật | Native/head 65; mutant 64. |
| P_cap_256 | Trả `cha[:256]` | octopus 257 cha thật | Native/head 257; mutant 256. |

Mỗi hàng đã đo trên cả SHA-1 và SHA-256. Tất cả **10/10 c53 rc0**. Criterion độc lập dùng assertion `bang`, chạy tiến trình con thật: **20/20 head rc0 + `CA: 1/1 dat`**, **20/20 mutant rc3 + `DO:r978_boundary_parent_domain:`**; không có rc4. [Criterion](boundary_criterion.py), [receipts](criterion-and-allcase-results.json).

Sáu bản B01/B03/B07/P09/P_cap_003/P_cap_256 đã chạy thêm `--tat-ca-ca`: mỗi bản đủ **53/53 ca rc0** (318 quan sát ca), không chỉ outer rc0. Bốn cap còn lại đã chạy c53 và criterion, không khai đã chạy toàn ca.

B01 là phản chứng boundary không phụ thuộc cách hiểu M1: commit SHA-1 **a06c8fd8eb296d91e15a6df5dc6c5ebfcb5a58d7** có message nhiều đoạn; `tree <OID>` nằm trong message giữa hai dấu ngăn LF-LF. Cắt tại dấu đầu đúng; cắt tại dấu cuối nhận nhầm tree thứ hai và trả None. Nhân chứng P09 **10036ad951f2ef9037979f0edfba72cfba00f719** xác nhận native giữ cha lặp. B03 **f6f7409239d89b8cd8826c1d3b3e014cd6a87054** và B07 **aa02b65a1f2a2c30f008b0f9b8bb2d91fa7d5c10** dùng oracle **M1**: native bỏ qua extension và trả dict, còn hợp đồng đóng băng yêu cầu None khi hơn một dòng `tree `. Không gọi khác biệt có chủ ý này là lỗi sản phẩm.

Ví dụ tái chạy trên artifact hiện tại, từ thư mục chứa PROMPT.md:

```text
PYTHONDONTWRITEBYTECODE=1 python -B out/boundary_criterion.py sha1-body_middle_metadata out/head/ops/ci_provenance.py
PYTHONDONTWRITEBYTECODE=1 python -B out/boundary_criterion.py sha1-body_middle_metadata out/boundary-mutants/B01_last_blank.py
```

Kỳ vọng rc0 rồi rc3. Module review_common đặt TMPDIR trong OUT và Git config global/system `/dev/null`. Mọi mutant chỉ đổi parser/metadata; không nhắm SHA hoặc tên fixture. Các mức cap là các biểu hiện cùng cơ chế mất phần đuôi danh sách, không phải sáu lớp riêng.

**Quét V3: miền đã kiểm và các phép tương đương**

Bộ mới thử **122 cấu trúc**, gồm **86 commit hợp lệ** trên hai định dạng và **36 cấu trúc bị hash-object từ chối rc128**, không dùng `--literally`. Mọi commit được ghi thành công đều fsck strict rc0; fsck cuối hai kho đều rc0. Reader head khớp kỳ vọng native/M1 **86/86**. [Fsck SHA-1](boundary-final-fsck-sha1.json), [SHA-256](boundary-final-fsck-sha256.json).

Đã quét dấu ngăn đầu/cuối, dấu ngăn ba LF, nhiều dòng trống, message nhiều đoạn, LF-LF thật trong giá trị extension, continuation SP/TAB/CR, header không có body, cha trước tree, cha giữa hai tree, header chen giữa các cha, parent giữa author/committer, parent muộn, dấu cách thừa ở đầu/giữa/cuối parent, cha lặp, sort/reverse và octopus 1/3/5/17/65/257 cha. Literal LF-LF kết thúc header ngay; dòng tiếp nối có SP không tạo cùng ranh giới.

Parent giữa hai tree ở vùng trước author, parent trước tree, header/ngắt dòng chen giữa các parent, parent giữa author/committer và các dòng parent thừa SP/TAB/CR đều bị Git từ chối khi ghi; không dùng chúng làm P2 “Git hợp lệ”. Hai tree ở **extension sau committer** với parent ở giữa thì Git chấp nhận nhưng M1 yêu cầu None; head và biến thể chọn vị trí cha sau tree cuối đều None. Các parent muộn hợp lệ không phải ancestry; đã kiểm cả native và main.

Trong **33 mutant mới**: **13 bị giết c53**, **10 sống không tương đương** ở bảng trên, **10 sống tương đương trên miền strict-valid**. Không lấy “chưa tìm thấy” làm chứng minh cho nhóm tương đương:

- B05 partition, B06 split mọi dấu rồi lấy phần đầu, B12 regex LF-LF: cùng lấy đúng prefix trước LF-LF đầu tiên, hoặc toàn payload nếu không có dấu ngăn; tương đương phép tách hiện tại.
- P02 bỏ dòng rỗng, P03 bỏ whitespace và P04 quét tới author: commit strict-valid có dãy parent liên tiếp trước author. Không có dòng chen hợp lệ ở vùng đó; author vẫn chặn trước mọi extension. Vì thế không đổi dãy cha, không đổi phép đếm tree.
- P05 rstrip, P06 strip, P07 lấy token đầu của giá trị parent: parent thật strict-valid có đúng OID rồi LF, không có SP/TAB/CR thừa. Đã thử 8 dạng delimiter/trailing và Git từ chối. Parent muộn không đi vào vòng lặp. Không có thay đổi trên miền hợp lệ.
- P08 lstrip trước nhận parent: các dòng metadata đầu strict-valid không thụt lề; author không mất tiền tố và vẫn dừng vòng lặp. Không thể nhận continuation sau author làm cha.

P12 `last_tree_parents` thuộc **13 bị giết**, nhưng cũng tương đương trên miền strict-valid theo guard đúng một tree/đứng đầu. Nó chết ở c53 bởi object lỗi không có tree gây ValueError; không đếm là survivor mới hay phản chứng native. B02/B04/B08/B09/B10/B11/B13/B14/P01/P10/P11/P13 đã bị c53 giết và cũng có nhân chứng hợp lệ trong bảng dữ liệu. [Inventory đủ 33](boundary-inventory.md).

Đây là quét hữu hạn theo các cơ chế của lớp được giao, không tuyên bố vét mọi chương trình parser có thể viết. Những nhóm còn thiếu đã được báo cùng lượt, không giữ lại để báo nhỏ giọt ở lượt sau.

**49 mutant D và 10 tương đương cũ**

Đã kiểm mã sản phẩm không đổi từ afcadd5, sao chép đúng 49 tệp D vào OUT rồi chạy với test head qua `CI_PROVENANCE_MA`. **39/49 rc3**, mọi output đều có `DO:c53_git_commit_khong_utf8:` và danh sách index sai đúng cơ chế; **10/49 rc0**, không rc4. Bảng [D-audit.md](D-audit.md) ghi đủ từng D, index fixture và lý do; [raw](D-reason-audit.json) giữ output đầy đủ.

Ví dụ D06 chết tại index19 (TAB đầu tree); D18 tại index10 (VT trong author); D09 tại index22 (Tree); D15 tại index23 (gập tree key); D03/D28 tại index25 (empty tree M1), D27 tại index26 (CRLF boundary M1). D37 chết bằng object lỗi CR trong tree, không phải một nhân chứng strict-valid. Đã kiểm lại cả dấu `DO` và nội dung, không chỉ rc.

Nhóm còn sống chính xác: **D10, D11, D12, D14, D16, D31, D33, D38, D39, D42**. Chạy thêm trên 86 fixture hợp lệ của lượt này: **860/860 kết quả bằng head**. [So sánh](old-equivalence-checks.json). Lập luận E1–E6 tiếp tục đúng với chính các phép biến đổi này:

- E1 D10/D11: cắt tại NUL không đổi miền strict-valid không chứa NUL. Đo thêm 5 vị trí NUL × hai định dạng; Git từ chối cả 10 ngay ở hash-object, không dùng literally. [Đối chứng](nul-controls.json).
- E2 D12: sau khi cắt tại LF-LF đầu tiên không còn dòng rỗng nội bộ để nối qua hai phần header; bỏ phần tử rỗng không đổi metadata.
- E3 D14/D16/D33: whitespace/continuation hợp lệ nằm sau author/committer, còn vòng parent dừng ở author. Xóa chúng hoặc lstrip riêng parent ở đó không mở lại vòng lặp và không sinh tree cấp ngoài.
- E4 D31: UTF-8 replacement rồi encode, vẫn tách LF trên bytes, giữ các byte ASCII quyết định tên trường/phân cách/OID; byte ngoài ASCII trong OID vẫn không qua regex. M1 vẫn cấm cách làm này trên toàn stdout; tương đương kết quả không phải khuyến nghị áp dụng.
- E5 D38/D39: cắt đuôi dòng tại VT/FF không tạo tiền tố metadata mới; control trong tree/parent thật không hợp lệ, extension tree vẫn bị đếm như trước. D37 cùng lập luận về miền hợp lệ nhưng đã chết trên object lỗi.
- E6 D42: guard `len(tree)==1` khiến tree đầu và cuối là cùng phần tử.

**Tính hợp lệ của chính fixture mới trong c53**

Đã chạy c53 thật có ghi nhận lệnh Git và giữ kho tạm; lấy **đúng byte/đúng OID** của 17 commit mới (index10–26), dựng từng kho kiểm riêng với đúng tree/blob. Cả 17 ghi bằng hash-object thường rc0, nhưng **17/17 fsck strict rc2**: thiếu hai object parent `5618020a67709ca6f2c93138905df0aa8d9c2df6` và `400589368e09ab2ee0e734b7af08b93478035503`. Không có chẩn đoán lỗi cấu trúc header khác trong phép đo này. [Capture c53](c53-capture.json), [17 receipt fsck](exact-c53-validity.json), [script](fixture_validity.py).

Vì vậy không thể gọi nguyên kho fixture c53 hiện tại là graph đã qua fsck strict. Native log vẫn đọc được OID cha từ header nên test có sức phân biệt, nhưng đó không phải bằng chứng tồn tại parent object. Đây là giới hạn đã có từ các lượt trước, không tự tạo một lớp P3 mới.

Để kiểm cấu trúc mới độc lập, đã dựng **đủ 17 dạng × SHA-1/SHA-256 = 34 commit** với cha thật, giữ đúng các byte phân cách/control và dạng extension. Cả **34/34 hash-object rc0, fsck strict rc0**, head khớp native cho 30 ca dict và M1 cho 4 ca None. Các nhân chứng P2 mới cũng dùng graph thật. Hướng bổ sung fixture nên tạo parent object thật và kiểm fsck, không đổi các byte đang cần thử hoặc biến oracle native thành oracle cho các ca M1 cố ý từ chối.

**N1–N7**

| Tiêu chí | Trạng thái | rc và bằng chứng dương |
|---|---|---|
| N1 | **passed** | Head c53 rc0; cùng test với sản phẩm base rc3, `DO:c53_git_commit_khong_utf8:` có `NEM:UnicodeDecodeError`. [Head](n1-head.json), [base](n1-base.json). |
| N2 | **passed về hành vi đột biến** | Lệnh import/chay_dot_bien đúng prompt rc0, **43/43 GIET**. Chạy riêng child: **43/43 rc3**, đúng c53, 0 rc4. Literal text=True cũng rc3 đúng UnicodeDecodeError. [Lệnh quy định](n2-prescribed.json), [children](checks-summary.json), [literal](wrapper-controls.json). |
| N3 | **not_run** | Không chạy suite mặc định. Đã chạy `--tat-ca-ca`: outer rc0, JSON đủ **53/53 ca**, từng rc0. Catalogue base **52 ca/292 mutant**, head **53 ca/335 mutant**; không khai 335/335 hoặc TONG: DAT. [Ca](all-head-cases.json), [đếm](catalogue-counts.json). |
| N4 | **passed** | Bare Ruff F --no-cache head/base đều rc0, `All checks passed!`, delta F0; git diff --check base..head rc0. Không phải receipt Ruff pin/probe của CI. [Head](n4-head-ruff.json), [base](n4-base-ruff.json), [diffcheck](preflight.json). |
| N5 | **passed** | doctrine-scan rc0, **10 tệp/0 chỗ chép**; adr-song rc0, **55 ADR/55 dòng** khớp 1–1, có ngoại lệ trạng thái ADR-0016. [Doctrine](n5-doctrine.json), [ADR](n5-adr.json). |
| N6 | **not_measured** | Offline; không đọc check run ci.yml trên exact head, không dùng lời khai executor thay phép đo. |
| N7 | **not_applicable; not_run** | `git_cuc_bo` không nằm trong HAM_DONG; không chạy --dot-bien-dong và không khai đạt. [Catalogue](catalogue-counts.json). |

Giữ các lưu ý hợp đồng từ lượt trước: M1 viết `-p`, sản phẩm dùng `--batch` để đọc loại object gốc cùng payload; M2 chỉ cho đổi UnicodeDecodeError thành tín hiệu chốt nhưng bộ bọc hiện nhận Exception có frame reader; M3 gọi tên `F13_doc_text_true`, catalogue dùng `F13_giai_ma_toan_stdout`; N3 nêu tăng 3 mutant, thực tăng 43. Không tự sửa nghĩa đặc tả hay tuyên bố khớp nguyên văn. P2 ở verdict này dựa trên phản chứng hành vi đã đo, không dựa vào tranh luận câu chữ. Không đề nghị thay reader bằng native `%P` trực tiếp; oracle ở đây chỉ dùng kho đầy đủ, không suy sang biên shallow.

**Định danh, phạm vi và toàn vẹn**

- HEAD detached **2c907a47e22c7b0706df766176180a798ed7f69f**, tree **407d6a53ca0d69a1c0d86ffcdd67acb792dd4775**. Chuỗi base **c8d92ba05c3ea875d8f84d94195430302690286d** → **bef14035718cae862369101f79dc61e938ae6b00** → **7fcfe18181ce4d089225900e36d3aed878877e7f** → **fdf1f05c1b3d845a694c796a81a8bd5c218a68c8** → **aa2a1f326eb964b1cf8f45454593971e0ab11b73** → **afcadd5673009dd4a6a56076af04f57b0ba56c11** → head được tự đo; local origin/master trỏ base. Hash đặc tả khớp đủ 64 ký tự. [Preflight](preflight.json).
- Diff base..head **2 tệp, +134/-6**, nằm trong write set; vượt dự kiến 60 dòng thêm nhưng dưới trần sensitive 6 tệp/450 dòng. Diff afcadd5..head chỉ đổi test. AST sản phẩm so base: chỉ `git_cuc_bo` đổi, thêm regex OID; main/moc_checkout/git_blob/doc_wf/REST không đổi. [Diff](diff.patch), [scope](ast-scope.json).
- Reviewer Codex/họ OpenAI; launcher ghi **openai_codex / codex_cli / machine**, run **21a89a7408e64c2a9508406e5b44b335**. Exact serving model/effort **not_measured**; họ GPT-6 theo chỉ dẫn phiên. Executor họ Claude theo assignment, không tự đo runtime executor. Không dùng context executor hoặc gọi subagent/phiên model phụ. `assurance_target: cross_approved`; request_changes này không cấp approved assurance. [Identity](identity.json).
- Packet r1/g1, sensitive, lượt 6/8 theo prompt được giao. Không truy cập remote để đo freshness lease/issuecomment; không dùng trần 2 cũ trong spec để xin lại quyền review đã được assignment hiện tại cấp. Không phát sinh lời gọi model phụ.
- Linux, Python **3.13.17**, Git **2.43.0**, PyYAML **6.0.3**, Ruff **0.17.3**. Python -B/PYTHONDONTWRITEBYTECODE=1, TMPDIR tuyệt đối trong OUT, Git global/system config /dev/null, optional locks tắt, Ruff no-cache. Các tiến trình kiểm thử cục bộ chạy đồng thời; không mạng/GitHub, không cài công cụ. [Versions](versions.json), [runtime](runtime.json).
- Snapshot đầu/cuối: **7.205/7.205 tệp tracked SRC giữ nguyên SHA-256**, bản sao head cũng khớp; HEAD/tree/spec không đổi, tracked/index diff rỗng, status gồm untracked/ignored rỗng. Không suy đây là kiểm mọi byte `.git` hay chứng minh lịch sử chưa từng ghi rồi hoàn nguyên. [Snapshot cuối](final-source-snapshot.json).

Lệnh/cwd/rc/stdout/stderr/thời lượng được lưu trong receipt. Script điều phối: [bootstrap](bootstrap.py), [checks](checks.py), [regressions](regressions.py), [boundary sweep](boundary_sweep.py), [criterion và audit D](finish_measurements.py), [audit cuối](final_audit.py). Các script dựng kho dùng OUT mới; không thiết kế chạy đè fixture cũ.

D02 và F10/D05 của #899, `.claude/dev/ci_dang_ky_test.py`, mốc Workflow definition, LIVE CI, Windows native, SHA-256 toàn tuyến main ngoài phạm vi; không tính hạng hay tuyên bố đã đo. Không tự soạn hoặc thử nội dung đường dẫn thoát cây. Các thay đổi và hiện vật review chỉ nằm dưới OUT.
