Verdict: request_changes
Reviewed commit: bf8ef9125ba54312d41baf3eb6ed88d564758256
Spec sha256: eccd6dd2917f76d6158d5c9574f4d4c2070ba22ef3da96b4dfcf6e820c301638

**P0=0, P1=0, P2=1, P3=0.** Giữ lớp `git-reader-fixture-domain-incomplete`. Ma trận mới khóa đủ các mutant không tương đương đã báo lượt 5–6, nhưng **chưa đóng lớp theo cấu trúc**: 15/25 mutant mới (5 phép đơn và 10 tổ hợp) còn sống c53, có phản chứng trên commit Git hợp lệ. Trong 252 mẫu liên trục (228 OID khác nhau) và 300 mẫu dựng lại ma trận bằng graph thật, reader head trả đúng cả 552 phép so (528 OID khác nhau); finding thuộc độ phủ test, chưa phải lỗi sản phẩm mới.

Verdict chỉ neo SHA dòng 2, không cấp quyền push, merge hay land. Không chạy suite mặc định. Mọi phép thử và hiện vật nằm trong OUT. [Tổng hợp phép quét](cross-summary.json), [criterion độc lập](cross-criterion-results.json), [lịch sử verdict tạm](VERDICT.progress.md).

**ĐỐI CHIẾU LƯỢT TRƯỚC**

Đã đối chiếu verdict lượt 1, bản tạm lượt 2, lượt 3–6. Sản phẩm không đổi từ `aa2a1f3` đến head; diff `2c907a4..head` chỉ thêm 13 dòng ma trận và 5 dòng catalogue test. Các kết quả dưới đây là phép đo lượt này. [Diff lượt này](step1-diff.patch), [scope/AST](scope.json).

| Lớp / nhóm | Trạng thái | Bằng chứng lượt 7 |
|---|---|---|
| `git-commit-body-encoding-lam-hong-metadata` | Giữ đóng trong miền đo | N1 head rc0/base rc3 có UnicodeDecodeError. Reader độc lập 28/28 đúng trên SHA-1/SHA-256, gồm Latin-1 body, author và extension. Main head trên UTF-8/ba dạng Latin-1 rc0, checkout passed; base ném UnicodeDecodeError ở ba dạng Latin-1. |
| `git-object-type-not-checked` | Giữ đóng | Blob dạng commit, blob không UTF-8, tree/tag/thiếu object đều None trên hai định dạng. Main blob dạng commit: head rc0 nhưng checkout not_measured; base rc0/checkout passed. |
| `git-header-cr-split-creates-parents` | Giữ đóng | CR trong author không tạo cha ở native/head. Main control/CR trên head rc12/12, failed; base rc12/0. |
| `git-header-extension-creates-parents` | Giữ đóng | Parent sau committer hoặc extension không thành ancestry. Main head rc12/failed, base rc0/passed; native xác nhận không có cha. |
| `git-reader-fixture-domain-incomplete` | Khóa biểu hiện cũ, **còn P2** | 49 D: 39 rc3/10 rc0; 33 B/P: 23 rc3/10 rc0. Chỉ nhóm tương đương cũ còn sống. Quét mới phát hiện 15 survivor không tương đương bên dưới. |
| Batch framing, lỗi Git, OID, SHA-256, số/thứ tự parent | Giữ khóa test hiện có | 48/48 child F13 rc3 và DO đúng c53; runner chay_dot_bien phân hạng 48/48 GIET. |
| Bộ bọc ngoại lệ reader | Không thấy tín dụng giả trong đối chứng | AttributeError bên trong reader rc3; lỗi import và binding ngoài frame reader rc4. Literal text=True + input str rc3 có UnicodeDecodeError. |

Reader/main dùng Git thật và REST/workflow giả của harness; không đo mạng hay SHA-256 toàn tuyến main. Kho regression có tree/parent thật, fsck strict rc0. Base exception ở script main là exception bắt được trong cùng tiến trình, không gán giả thành rc con. [Reader](regression-reader.json), [main](regression-main.json), [lệnh Git](regression-git-commands.json), [đối chứng wrapper](wrapper-controls.json).

**Bảng lớp còn mở**

| slug | hạng | file:dòng | phép đo | hướng vá |
|---|---|---|---|---|
| `git-reader-fixture-domain-incomplete` | **P2** | `ops/ci_provenance_test.py:1109`, `:1114`, `:1115`, `:1123`; điểm đột biến tại `ops/ci_provenance.py:151`, `:152`, `:156` | C01–C15 sống c53 rc0 nhưng sai so native trên graph strict-valid. 30 cặp mutant × định dạng có criterion head rc0/mutant rc3 đúng DO. Sáu đại diện C01–C06 sống đủ 53/53 ca mỗi bản. | Mở grammar của fixture tới tổ hợp tên trường/phân cách/control, kiểu xuống dòng và continuation; bổ sung các mẫu đẳng thức/thứ tự parent có lặp cách quãng và lặp ≥3. Dùng nhãn kỳ vọng từ cấu trúc sinh và oracle native; khóa bằng các mutant có phản chứng. |

**Không có P3 mở** trong phạm vi, nên không có mục P3 cần quyết định giữ nợ. Owner xử lý P2: executor wp978 và chủ kho/điều phối #978. Không đổi slug, không chuyển thành nợ mới để xóa lịch sử. Không cần sửa reader head đang đúng trên các nhân chứng này.

**Phản chứng mới và tương tác liên trục**

[Catalogue đủ cặp neo/thay và hash tệp](cross-catalogue.json), [inventory đủ 25 mục](cross-inventory.md), [kết quả c53](cross-c53-results.json), [252 fixture/raw bytes/OID/native/head/mutant](cross-fixtures.json).

| ID | Phép biến đổi tổng quát, không nhận diện fixture | Nhân chứng thuộc grammar Git hợp lệ | Sai khác |
|---|---|---|---|
| C01 | Tách dòng tại SP đầu tiên, rstrip riêng tên trường rồi ghép lại; không strip payload | Extension sau committer có `tree<TAB><SP><oid>`; tương tự CR/VT/FF trước SP | Native/head giữ metadata đúng; mutant tạo tree cấp ngoài thứ hai và trả None. c53 chỉ thử TAB thay SP hoặc TAB đầu dòng, chưa thử TAB ngay trước SP phân cách. |
| C02 | Unfold `CR LF SP` thành SP trước tách header/body | Extension `tree<CR><LF><SP><oid>` | Ghép hai dòng thành tree bổ sung; native/head đúng, mutant None. |
| C03 | Unfold `LF TAB` thành SP | Extension `tree<LF><TAB><oid>` | Tương tự; fixture unfold hiện có chỉ dùng LF+SP. |
| C04 | Unfold `CR LF TAB` thành SP | Extension `tree<CR><LF><TAB><oid>` | Tương tự trên tổ hợp CRLF và TAB. |
| C05 | Chỉ append parent nếu OID chưa có trong `cha[:-1]` — lỗi lệch một phần tử của phép loại trùng | Dãy A,B,A hoặc A,A,A với object cha thật | Native/head giữ cả ba cha; mutant còn hai. Mẫu trùng duy nhất trong ma trận là A,A, không phân biệt được phép này. |
| C06–C15 | Toàn bộ 10 cặp kết hợp của năm phép trên; giữ thứ tự phép biến đổi trong catalogue | Kết hợp key/control, folding, body nhiều đoạn, parent root/3/17 hoặc các kiểu lặp | Cả 10 sống c53 rc0 và đều có nhân chứng khác native. Đây là các biểu hiện của cùng lớp. |

C05 là đột biến thuật toán (lát danh sách sai), không gắn nhánh riêng theo SHA, tên fixture hay độ dài OID. C01–C04 là các phép chuẩn hóa parser thông thường áp toàn dữ liệu, cũng không nhắm một fixture cụ thể.

**Tương tác thật, không chỉ cộng hai lỗi riêng:** C06 trên commit SHA-1 **036fd5e579ed7aff052c158b196a78ae2b520b36**, fixture `key_TAB_fold_CRLF_SP_three_paragraphs`. Extension chứa tên `tree` rồi TAB, CRLF, SP và OID ở dòng tiếp. C01 riêng và C02 riêng đều trả đúng metadata như head/native; chỉ khi unfold CRLF+SP **rồi** rstrip tên trường, dòng mới trở thành `tree <oid>` và mutant trả None. Commit còn có 3 cha thật và body nhiều đoạn. Nhân chứng cùng cấu trúc trên SHA-256 cũng phân biệt được. Đây chính là tổ hợp giữa chuẩn hóa tên trường, phân cách vật lý và continuation mà ma trận hiện tại không sinh.

Mười đối chứng C16–C25 kết hợp lower/rstrip, ranh giới cuối, xóa continuation, sort/dedup và các phép mới: **10/10 rc3, DO đúng c53**. Không có rc4 trong 25 mutant mới. C01–C15 đều không tương đương; không xếp survivor mới nào là tương đương chỉ vì chưa tìm thấy witness.

Các kho quét mới có **276 mẫu đích mỗi định dạng, tương ứng 264 OID khác nhau** (150 mẫu ma trận + 126 mẫu liên trục), cùng tree/blob và 257 cha thật. Đã gọi `fsck --strict --no-dangling` với **276 mục OID đích làm root tường minh**, rc0 trên từng kho. Hai tên shape `fold_CRLF_TAB` và `key_CR_fold_LF_TAB` sinh cùng bytes nên có 12 mẫu lặp mỗi định dạng; các số 252/552 là số phép so, không phải số OID độc nhất. Mọi commit được dựng bằng `hash-object -t commit -w --stdin`, không dùng --literally. [Fsck SHA-1](cross-fsck-with-roots-sha1.json), [fsck SHA-256](cross-fsck-with-roots-sha256.json), [lệnh Git đầy đủ](cross-git-commands.json).

Criterion tiến trình con dùng `bang`, không suy kết quả từ outer collector rc0: **30/30 head rc0 + `CA: 1/1 dat`; 30/30 mutant rc3 + `DO:r978_cross_axis_domain:`**. Sáu đại diện C01–C06 chạy thêm `--tat-ca-ca`, mỗi bản đủ **53/53 ca rc0** (318 quan sát); chín tổ hợp còn lại chỉ chạy c53 và criterion, không khai đã chạy toàn ca. [Criterion](cross_criterion.py), [receipts](cross-criterion-results.json), [toàn ca](cross-allcases-results.json).

Tái lập từ thư mục chứa PROMPT.md (repo fixture đã được giữ dưới OUT):

```sh
PYTHONDONTWRITEBYTECODE=1 python -B out/cross_criterion.py sha1-key_TAB_fold_CRLF_SP_three_paragraphs out/head/ops/ci_provenance.py
PYTHONDONTWRITEBYTECODE=1 python -B out/cross_criterion.py sha1-key_TAB_fold_CRLF_SP_three_paragraphs out/cross-mutants/C06_key_rstrip__unfold_CRLF_SP.py
```

Kỳ vọng rc0 rồi rc3. Module `common.py` đặt TMPDIR dưới OUT và vô hiệu cấu hình Git global/system cho các lệnh thử.

**Audit 82 mutant cũ và các tương đương**

Đã sao chép nguyên vẹn 49 tệp D và 33 tệp B/P sang OUT; sản phẩm làm nền không đổi. **62/82 rc3**, output có DO đúng c53 và nội dung sai đúng phép biến đổi; **20/82 rc0**, không rc4. [Inventory](old-mutant-inventory.md), [raw output, index sai và diff từng mutant](old-mutant-audit.json).

Các biểu hiện lượt 6 được khóa tại: B01 index29 (metadata giữa hai đoạn body); B03 index32 (continuation chỉ SP trước tree); B07 index47 (tree rỗng, không body); P09 index87 (hai parent trùng); các cap 3/4/8/16/64/256 index147 (257 cha). Các khóa lượt 5 vẫn đúng: D06 index19 (TAB đầu), D18 index10 (VT author), D09 index22 (Tree), D15 index23 (gập LF+SP), D03/D28 index25 (tree rỗng M1), D27 index26 (CRLF M1). D30 chết bằng OID lỗi có byte ngoài ASCII ở index183; D37 chết bằng object cố ý lỗi CR ở index185; P12 chết NEM:ValueError tại object không tree index178. Không lấy ba ca lỗi này làm bằng chứng strict-valid hay lỗi import/setup.

Survivor đúng danh sách executor khai: D10/D11/D12/D14/D16/D31/D33/D38/D39/D42; B05/B06/B12; P02–P08. Đã chạy chúng trên toàn bộ 552 fixture mới: **11.040/11.040 kết quả bằng head/kỳ vọng**. [Phép so](old-equivalence-new-domain.json). Lập luận tương đương giữ nguyên trong miền Git strict-valid:

- D10/D11: cắt ở NUL là identity khi commit strict-valid không chứa NUL; phép đo loại NUL của lượt 5–6 là căn cứ miền, không tính là thử mới ở lượt này.
- D12: bỏ phần tử rỗng sau khi đã lấy prefix trước LF-LF đầu không nối được hai vùng header/body.
- D14/D16/D33: whitespace/continuation hợp lệ ở sau author/committer; vòng parent đã dừng, còn các phép này không sinh tree cấp ngoài.
- D31: UTF-8 replacement rồi encode, vẫn tách LF bytes, giữ các byte ASCII quyết định tiền tố/phân cách/OID. M1 vẫn cấm replacement toàn stdout; tương đương quan sát không phải đề nghị triển khai.
- D38/D39: cắt đuôi dòng tại VT/FF không tạo tiền tố mới; tree/parent thật có control trong giá trị không strict-valid; extension đã bắt đầu tree vẫn bị đếm trước/sau cắt.
- D42: guard buộc đúng một tree nên phần tử đầu/cuối là một.
- B05/B06/B12: partition, split mọi dấu lấy phần đầu và regex literal đều lấy đúng prefix trước LF-LF đầu tiên.
- P02–P04: dãy parent strict-valid liên tiếp trước author, không có dòng trống/whitespace/header khác chen vào hợp lệ; author vẫn chặn.
- P05–P07: giá trị parent thật strict-valid đúng OID, không có whitespace hoặc token dư; parent muộn không tới vòng append.
- P08: metadata thật trước author không thụt lề; lstrip riêng ở vòng parent không vượt được author để nhận continuation làm cha.

Đây là lập luận cho chính các phép biến đổi đã cung cấp, không phải chứng minh mọi tổ hợp của chúng đều tương đương. C06 là bằng chứng vì sao tương đương hoặc vô hại trên một vùng dữ liệu không được suy qua phép hợp thành tùy ý.

**Ma trận 150 commit: độc lập oracle và tính hợp lệ**

Capture chạy c53 head thật cho thấy **150/150** object ma trận ghi rc0 bằng hash-object thường, không --literally; giữ đủ raw bytes/OID. Có **50 nhánh dict và 100 nhánh None**. Đã rehash nguyên byte trong kho riêng và khớp 150 OID. [Capture](c53-capture.json), [audit từng mẫu](matrix-exact-audit.json), [rehash](matrix-exact-rehash.json).

Biểu thức `so_tree` không gọi sản phẩm và kỳ vọng parent lấy từ danh sách sinh; nhánh dict còn đối chiếu Git native. Tuy nhiên phần tách LF-LF/đếm tiền tố dùng **cùng thuật toán và biểu thức** với sản phẩm: độc lập về thực thi/dữ liệu, chưa phải oracle có thuật toán độc lập. Tôi kiểm chéo bằng state machine duyệt byte, không dùng split/startswith của parser, và bằng nhãn grammar: extension 0/5 ⇒ dict; extension 1–4 ⇒ None, không phụ thuộc parser. Cả 150 mẫu khớp; không tìm được kỳ vọng M1 sai trong ma trận hiện tại.

Dựng lại đúng grammar 5×6×5 trên cả SHA-1/SHA-256 bằng cha thật: **300/300 head đúng**, oracle native đúng metadata đã sinh cho cả 300; 200 ca None là M1 cố ý chặt hơn native vì có thêm dòng tree cấp ngoài. Nhánh None lấy từ nhãn sinh extension, không lấy từ sản phẩm hoặc một bản sao thuật toán parser. [Dữ liệu ma trận dựng lại](matrix-rebuilt.json). Không gọi khác biệt M1/native là lỗi sản phẩm.

**Graph nguyên bản c53 vẫn thiếu parent object.** Kho riêng chỉ chứa đúng 150 commit ma trận và tree/blob, kiểm fsck với cả 150 OID làm root trả **rc2, 259 missing commit**; không có object cố ý lỗi `hong` trong kho này. Điều này phân biệt “hash-object chấp nhận cấu trúc” với “graph kết nối đầy đủ”. Không cộng thêm P3, theo giới hạn đã nêu ở lượt 6; các phản chứng P2 lần này dùng graph đầy đủ và fsck rc0. [Fsck nguyên ma trận với root tường minh](matrix-exact-isolated-fsck-with-roots.json).

Receipt `c53-exact-fsck.json` là phép thăm dò trên kho capture có cả object `hong` cố ý lỗi nên rc3; không dùng nó để kết luận ma trận sai cấu trúc. Receipt `matrix-exact-isolated-fsck.json` không truyền root, rc0 kèm “No default references”; không dùng nó làm bằng chứng kết nối graph. Kết luận ở trên dựa vào phép kiểm root tường minh.

**Hướng vá theo lớp và giới hạn**

Vá trong **c53 và DOT_BIEN**, giữ các nhân chứng đã khóa. Thay vì chỉ thêm tên mutant hay vài ví dụ riêng, mở bộ sinh với các trục có ý nghĩa cú pháp: vị trí whitespace/control trong tên trường và cạnh SP phân cách; LF/CRLF; continuation SP/TAB/hỗn hợp; có/không body và body nhiều đoạn. Kiểm các tích liên trục, nhất là ghép dòng rồi chuẩn hóa tên, vì hai phép riêng có thể cùng không làm sai trên một mẫu trong khi hợp thành làm sai.

Với parent, thêm các mẫu đẳng thức A,A; A,B,A; A,A,A; A,A,B cùng thứ tự không sắp xếp và số cha hiện có; không chỉ tăng một ngưỡng cap tùy ý. Tạo object cha thật, giữ raw bytes trước hash; fsck strict với OID đích tường minh. Dùng kỳ vọng từ nhãn cấu trúc sinh cho M1 và native cho metadata; kiểm baseline xanh và mutant rc3/DO đúng c53. C01–C15 cùng các D/B/P đã có là bộ khóa cụ thể có thể tái lập.

Rủi ro khi vá: normalize fixture trước hash sẽ xóa byte đang thử; dùng native thay M1 cho mọi ca làm oracle sai hợp đồng; chép parser sản phẩm vào expected tạo tự xác nhận; bắt lỗi setup/import thành DO tạo tín dụng giả; sinh tích quá lớn làm test tốn thời gian. Phương án cần giữ ma trận hữu hạn, có nhãn và chứng cứ sức phân biệt, không hứa vét mọi chương trình parser.

Lớp **chưa đóng**, nên không chuyển phần chưa quét thành nợ để approve. Phép quét lượt này hữu hạn ở 25 transform và các grammar đã ghi; chưa vét mọi chuỗi byte Unicode/control, mọi độ dài/thứ tự cha hay mọi phép hợp thành parser. Không giữ lại một survivor đã đo để báo nhỏ giọt: toàn bộ 15 đã có trong catalogue/summary. Miền ngoài phạm vi vẫn theo prompt.

**N1–N7**

| Tiêu chí | Trạng thái | rc và bằng chứng dương |
|---|---|---|
| N1 | **passed** | c53 head rc0; cùng test dùng sản phẩm base rc3, DO đúng c53 chứa NEM:UnicodeDecodeError. [Head](n1-head.json), [base](n1-base.json). |
| N2 | **passed về hành vi đột biến** | Runner import/chay_dot_bien rc0, **48/48 GIET**; chạy riêng **48/48 child rc3**, DO đúng c53, không rc4. Literal text=True cũng rc3 có UnicodeDecodeError. [Runner](n2-prescribed.json), [phân hạng](n2-prescribed-results.json), [children](checks-summary.json). |
| N3 | **not_run** | Không chạy suite mặc định. Đã chạy --tat-ca-ca: outer rc0, JSON đủ **53/53 ca rc0**. Base 52 ca/292 mutant, head 53 ca/340 mutant; không khai 340/340 hoặc TONG: DAT. [Ca head](all-head-cases.json), [catalogue](catalogue-counts.json). |
| N4 | **passed** | Ruff F --no-cache head/base rc0, All checks passed, delta F0; git diff --check base..head rc0. Đây không phải receipt Ruff pin/probe CI. [Head](n4-head-ruff.json), [base](n4-base-ruff.json), [diffcheck](preflight.json). |
| N5 | **passed** | doctrine-scan rc0: 10 tệp/0 chỗ chép; adr-song rc0: 55 ADR/55 dòng khớp 1–1, ghi ngoại lệ trạng thái ADR-0016. [Doctrine](n5-doctrine.json), [ADR](n5-adr.json). |
| N6 | **not_measured** | Offline; không đọc check run ci.yml exact head, không nhận lời khai executor thay đo. |
| N7 | **not_applicable; not_run** | git_cuc_bo không thuộc HAM_DONG; không chạy --dot-bien-dong, không khai đạt. [Catalogue](catalogue-counts.json). |

Giữ lưu ý hợp đồng từ lượt trước: M1 viết cat-file -p, sản phẩm dùng --batch để lấy loại object gốc cùng bytes; M2 chỉ nêu UnicodeDecodeError nhưng bộ bọc hiện nhận Exception có frame reader; M3 dùng tên F13_doc_text_true, catalogue dùng F13_giai_ma_toan_stdout; N3 nêu tăng 3 mutant, thực tăng 48. Không tự sửa đặc tả hay tuyên bố khớp nguyên văn. Finding P2 dựa trên phản chứng hành vi, không dựa vào tranh luận câu chữ. Native %P ở kho đầy đủ không phải đề nghị thay reader khi checkout shallow.

**Định danh, phạm vi và toàn vẹn**

- HEAD detached **bf8ef9125ba54312d41baf3eb6ed88d564758256**, tree **bda6de0688b85b29b5eb192a02192cd2ce860a46**. Base/local origin/master **c8d92ba05c3ea875d8f84d94195430302690286d**. Đủ chuỗi base → bef1403 → 7fcfe18 → fdf1f05 → aa2a1f3 → afcadd5 → 2c907a4 → head, các SHA/parent đầy đủ trong [preflight](preflight.json). Hash đặc tả khớp 64 ký tự.
- Diff base..head đúng **2 tệp, +152/-6**, trong write set, dưới trần sensitive 6 tệp/450 dòng nhưng vượt dự kiến 60 dòng thêm của đặc tả. AST sản phẩm chỉ thay git_cuc_bo và thêm regex OID; main/moc_checkout/git_blob/doc_wf/REST không đổi. [Diff](diff.patch), [scope](scope.json).
- Reviewer Codex, họ OpenAI/GPT-6 theo chỉ dẫn phiên; launcher ghi **openai_codex / codex_cli / machine**, run **43402fb648164b9b80c6d89ec5d681b7**. Exact serving model/effort **not_measured**. Executor họ Claude theo assignment, không tự đo runtime. Không gọi subagent hoặc model phụ. `assurance_target: cross_approved`; verdict request_changes không cấp approved assurance. [Identity](identity.json).
- Packet r1/g1 sensitive, lời gọi 7/8 theo prompt hiện hành; không lấy trần 2 cũ để xin lại quyền đã được assignment cấp. Không truy cập remote để đo freshness lease/issuecomment.
- Linux; version Python/Git/PyYAML/Ruff và rc nằm trong [versions](versions.json). Dùng python -B, PYTHONDONTWRITEBYTECODE=1, TMPDIR tuyệt đối dưới OUT, Git global/system config /dev/null, optional locks tắt, Ruff no-cache. Không cài công cụ.
- Snapshot cuối: **7.205/7.205 tệp tracked SRC không đổi SHA-256**, bản sao head vẫn khớp; HEAD/tree/spec không đổi, trạng thái tracked/index/untracked/ignored rỗng. Không suy đây là kiểm mọi byte .git hoặc chứng minh chưa từng ghi rồi hoàn nguyên. [Audit cuối](final-source-snapshot.json).

Lệnh/cwd/rc/stdout/stderr/thời lượng trong từng receipt. Script chính: [bootstrap](bootstrap.py), [checks](checks.py), [N2](n2_runner.py), [capture](capture.py), [regression](regression.py), [quét liên trục](cross_sweep.py), [criterion/audit](finish.py), [fsck roots](fsck_roots.py), [tương đương](equivalence.py), [audit cuối](final_audit.py). Bản sao head nguyên trạng nằm trong `out/head`; mọi mutant nằm ở `out/mutants` hoặc `out/cross-mutants`.

D02 và F10/D05 của #899; .claude/dev/ci_dang_ky_test.py; Workflow definition; LIVE CI; Windows native; SHA-256 toàn tuyến main đều ngoài phạm vi, không tính hạng và không khai đã đo. Không soạn/thử nội dung đường dẫn thoát cây. Không mạng, GitHub, push, merge hay land.
