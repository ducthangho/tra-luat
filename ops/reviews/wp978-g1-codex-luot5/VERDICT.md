Verdict: request_changes
Reviewed commit: afcadd5673009dd4a6a56076af04f57b0ba56c11
Spec sha256: eccd6dd2917f76d6158d5c9574f4d4c2070ba22ef3da96b4dfcf6e820c301638

**P0=0, P1=0, P2=1, P3=0.** Còn lớp `git-reader-fixture-domain-incomplete`. Z01 đã được khóa đúng bằng fixture mergetag mới. Tuy nhiên, quét 49 phép biến đổi header tìm thấy **19 mutant sống c53 và làm sai kết quả Git native trên commit hợp lệ**, cùng **3 mutant sống làm sai quy tắc M1** trên commit hợp lệ. Đây là một lớp thiếu độ phủ, không phải 22 finding độc lập. Mã sản phẩm hiện tại đúng trên các nhân chứng native dùng để chứng minh P2.

Verdict chỉ neo commit trên, không cấp quyền push, merge hay land. Reviewer độc lập, offline; mọi phép thử sản phẩm chạy trên bản sao dưới OUT. Không chạy suite mặc định ~40 phút.

**ĐỐI CHIẾU LƯỢT TRƯỚC**

Đã đối chiếu verdict lượt 1, bản **tạm** lượt 2, lượt 3 và lượt 4. Các kết quả dưới đây được tự chạy trong lượt này; không nhận lời khai executor hay verdict cũ làm phép đo mới. Script cũ được đọc, bỏ đoạn ghi kết luận cũ và neo lại mutation trên head hiện tại trước khi chạy.

| Lớp / biểu hiện | Kết luận | Phép đo ở lượt này |
|---|---|---|
| `git-commit-body-encoding-lam-hong-metadata` | Giữ đóng | N1 head rc0/base rc3 có UnicodeDecodeError; 50/50 quan sát reader đúng. 7/7 biến thể main SHA-1 trên head rc0/checkout passed, gồm Latin-1 author/message và extension không UTF-8. [Reader](independent-results.json), [main](independent-main-results.json). |
| `git-object-type-not-checked` | Giữ đóng | Blob dạng commit, blob không UTF-8, tree/tag đều None trên SHA-1/SHA-256; criterion head rc0/base rc3. Main blob head not_measured, base passed dù cả hai outer rc0. [Criterion](criterion-r978_noncommit_must_be_none-head.json). |
| `git-header-cr-split-creates-parents` | Giữ đóng | Nhân chứng CR-author fsck strict rc0, native không có cha, ancestry rc1. Main control/CR head rc12/12, đều failed; base rc12/0. Criterion head rc0/base rc3. [Git](cr-author-results.json), [main](cr-author-main-results.json). |
| `git-header-extension-creates-parents` | Giữ đóng | Parent sau committer/extension có fsck strict rc0, native/head không nhận làm cha. Main head control và hai biến thể rc12/failed; base hai biến thể rc0/passed. Criterion head 3/3 rc0; base hai biến thể rc3. [Git](extension-finding.json), [main](extension-main-results.json). |
| `git-reader-fixture-domain-incomplete` | Z01 đã đóng; lớp còn P2 | R/Y 14/14 GIET đúng c53; Z01 rc3 đúng fixture index 9. Bốn nhân chứng mergetag/continuation SHA-1/SHA-256: head criterion rc0, Z01 rc3. Lớp còn các survivor ở bảng đầy đủ bên dưới. [R/Y](supplemental-mutant-results.json), [Z01](child-F13_lstrip_dau_dong.json), [criterion](regression-commands.json). |
| X01–X10: batch header, kích thước, kiểu, rc, lỗi chạy Git | Giữ đóng về test | Tái dẫn xuất đột biến từ 7fcfe18 lên mã head: 10/10 child rc3, DO đúng c53. X07 dùng literal text=True và input str, bị UnicodeDecodeError. [Replay X](x-replay-results.json). |
| X11 và bộ bọc lỗi reader | Không xác nhận tín dụng giả | X11 ném từ trong reader: rc3. Lỗi import và binding ngoài reader: rc4/TIN_DUNG_GIA, không tính GIET. [Đối chứng](wrapper-controls.json). |

Z01 chết **đúng lý do**: output nguyên văn `DO:c53_git_commit_khong_utf8:git_cuc_bo lệch ở [(9, None)]`. Index 9 chính là mergetag thêm ở dòng 1105, không phải lỗi setup/import. Lstrip biến ` tree <OID>` trong tag thành tree cấp ngoài, khiến mutant trả None. Bốn criterion độc lập dùng commit có cha/tree thật và fsck strict rc0 xác nhận cùng cơ chế. [Fixture](extra-fixtures.json), [kết quả](extra-mutant-results.json).

**Bảng lớp còn mở**

| slug | hạng | file:dòng | phép đo | hướng vá |
|---|---|---|---|---|
| `git-reader-fixture-domain-incomplete` | **P2** | `ops/ci_provenance_test.py:1095–1123` (fixture/assertion/oracle c53); vị trí mutation `ops/ci_provenance.py:151–152` | 22 mutation không tương đương sống c53 rc0: 19 có head = native, mutant sai; 3 làm sai M1. Mỗi mutation có nhân chứng SHA-1 và SHA-256 fsck strict rc0, criterion độc lập head rc0/mutant rc3. Ba đại diện D06/D18/D15 còn sống đủ 53/53 ca. | Mở rộng bảng fixture theo các trục byte phân cách, khoảng trắng, hoa/thường, continuation và boundary; thêm mutation tương ứng. Giữ nguyên sản phẩm đúng trên nhân chứng native; tách assertion theo M1 với trường hợp spec cố ý chặt hơn Git. |

Không có P3 mở trong phạm vi lượt này. Giữ nguyên slug vì nguyên nhân vẫn là miền fixture chưa phân biệt các cách chuẩn hóa header.

**Nhân chứng và cách tái lập**

D18 thay đúng biểu thức gán `dong` bằng tách LF hoặc VT. Commit SHA-1 **a6e1373a17ab2a5145d7eb4a0194d9d9c7a81d1b** có author chứa byte VT bao quanh `tree <OID>`; Git coi đó là nội dung author. Fsck strict rc0, native/head trả tree và đủ 5 cha theo đúng thứ tự. Mutant tách thành dòng tree thứ hai, trả None; c53 vẫn rc0 và toàn bộ 53 ca vẫn xanh. [c53](D18_split_VT-c53.json), [toàn ca](all-cases-D18_split_VT.json), [criterion head](criterion-D18_split_VT-sha1-head.json), [criterion mutant](criterion-D18_split_VT-sha1-mutant.json).

D06 lstrip riêng TAB sống vì fixture mới chỉ khóa SP. Commit **b91cba499f1ada0cb3aa52e1aa87aed529dcb362** có dòng extension bắt đầu TAB rồi `tree <OID>`: head/native đúng, mutant None. D15 unfold LF+SP sống với commit **7e4af5c24f360f9e05b03e454d061c41c5214a68** có extension `tree` (không có dấu cách sau tên) rồi continuation chứa OID: phép unfold tự tạo `tree <OID>` cấp ngoài. Cả hai có fsck strict rc0 và sống 53/53 ca. [Tổng hợp toàn ca](domain-all-cases-summary.json).

[Catalogue và toàn bộ kết quả](all-domain-results.json) lưu đúng cặp neo/thay, hash file mutant, rc c53 và mọi nhân chứng phân biệt. [Fixture](all-domain-fixtures.json) lưu raw bytes dạng hex, OID, lệnh/output native và fsck. [Criterion](domain_criterion.py), [88 lần chạy head/mutant](domain-criterion-results.json) cho **44/44 head rc0, 44/44 mutant rc3** đúng prefix `DO:r978_header_normalization:`; không lấy rc0 của script thu thập làm kết quả sản phẩm. Cả **44/44** nhân chứng được băm lại bằng hash-object **không có --literally**, rc0 và đúng OID. [Receipt](witness-rehash-without-literally.json).

Chạy lại một criterion từ thư mục chứa PROMPT.md, với các kho fixture đã tạo dưới OUT:

```sh
PYTHONDONTWRITEBYTECODE=1 python -B out/domain_criterion.py sha1-author_sep_tree_0b out/head/ops/ci_provenance.py native
PYTHONDONTWRITEBYTECODE=1 python -B out/domain_criterion.py sha1-author_sep_tree_0b out/domain-mutants/D18_split_VT.py native
```

Kỳ vọng lần lượt rc0 và rc3. Module review_common tự đặt TMPDIR dưới OUT, cấu hình Git global/system /dev/null và danh tính Git giả.

**Quét lớp biến đổi header — đủ 49 mục đã đo**

Tập mới có **198 fixture: 168 fsck strict chấp nhận, 30 bị từ chối** trên SHA-1/SHA-256. Các object lỗi được loại khỏi kho sau khi ghi receipt để không làm bẩn fsck của ca sau. Fsck cuối toàn bộ hai kho đều rc0. Thêm bộ 22 fixture của lượt 4 đã chạy lại độc lập. Phép quét phủ mọi nhóm được prompt nêu và mở rộng tới Unicode line separator/NFKC/xóa control. Đây là inventory hữu hạn có phép đo, không tuyên bố vét mọi chương trình parser có thể viết.

Trong bảng: **G/3** = GIET đúng c53, **S/0** = sống c53. “Native” là head bằng oracle Git, mutant khác. “M1” là head đúng quy tắc đếm tree/OID của spec; không đồng nhất với native. Tên fixture bỏ prefix SHA-1/SHA-256; cả hai định dạng đều được đo. Cột kết quả tương đương dùng lập luận E1–E6 bên dưới.

| ID | Phép biến đổi | c53 | Nhân chứng Git hợp lệ / kết luận |
|---|---|---|---|
| D01 | lstrip ASCII | G/3 | Native: `leading_tree_20` |
| D02 | strip hai phía | G/3 | Native: `leading_tree_20` |
| D03 | rstrip sau tách header | S/0 | M1: `empty_tree_sp` |
| D04 | gộp whitespace bằng split/join | G/3 | Native: `leading_tree_20` |
| D05 | gộp SP/TAB, không bỏ đầu dòng | S/0 | Native: `key_delimiter_09` |
| D06 | lstrip TAB | S/0 | Native: `leading_tree_09` |
| D07 | bỏ đúng một SP tiếp nối | G/3 | Native: `leading_tree_20` |
| D08 | lower toàn dòng | G/3 | Native: `extension_key_54726565` |
| D09 | lower riêng tên header | S/0 | Native: `extension_key_54726565` |
| D10 | cắt từng dòng ở NUL | S/0 | E1 |
| D11 | cắt payload ở NUL | S/0 | E1 |
| D12 | bỏ dòng rỗng sau tách header | S/0 | E2 |
| D13 | bỏ dòng rỗng trước tách header | G/3 | Native: `body_metadata` |
| D14 | bỏ dòng chỉ có whitespace sau tách | S/0 | E3 |
| D15 | unfold LF+SP thành SP | S/0 | Native: `unfold_tree_key` |
| D16 | bỏ dòng bắt đầu SP/TAB | S/0 | E3 |
| D17 | tách LF hoặc CR | G/3 | Native: `author_sep_tree_0d` |
| D18 | tách LF hoặc VT | S/0 | Native: `author_sep_tree_0b` |
| D19 | tách LF hoặc FF | S/0 | Native: `author_sep_tree_0c` |
| D20 | tách LF hoặc FS | S/0 | Native: `author_sep_tree_1c` |
| D21 | tách LF hoặc GS | S/0 | Native: `author_sep_tree_1d` |
| D22 | tách LF hoặc RS | S/0 | Native: `author_sep_tree_1e` |
| D23 | tách LF hoặc byte NEL | S/0 | Native: `author_sep_tree_85` |
| D24 | bytes.splitlines | G/3 | Native: `author_sep_tree_0d` |
| D25 | Latin-1 → str.splitlines | G/3 | Native: `author_sep_tree_0d` |
| D26 | UTF-8 replacement → str.splitlines | G/3 | Native: `author_sep_tree_0d` |
| D27 | CRLF → LF trước tách header | S/0 | M1: `crlf_blank_before_tree` |
| D28 | rstrip từng dòng trước tách header | S/0 | M1: `empty_tree_sp` |
| D29 | TAB → SP | S/0 | Native: `key_delimiter_09` |
| D30 | ASCII decode ignore | G/3 | Native: `leading_tree_85` |
| D31 | UTF-8 replacement, vẫn tách LF bytes | S/0 | E4 |
| D32 | nhận tree sau whitespace | G/3 | Native: `leading_tree_20` |
| D33 | nhận parent sau whitespace, vẫn dừng tại author | S/0 | E3 |
| D34 | đọc cả body như header | G/3 | Native: `body_metadata` |
| D35 | chỉ nhận ranh giới CRLF-CRLF | G/3 | Native: `body_metadata` |
| D36 | gộp mọi ASCII whitespace | S/0 | Native: `key_delimiter_09` |
| D37 | cắt từng dòng tại CR | G/3 | E5; c53 giết bằng object lỗi |
| D38 | cắt từng dòng tại VT | S/0 | E5 |
| D39 | cắt từng dòng tại FF | S/0 | E5 |
| D40 | lstrip chỉ SP | G/3 | Native: `leading_tree_20` |
| D41 | quét parent sau author/extension | G/3 | Native: `late_parent` |
| D42 | tree cuối thay tree đầu | S/0 | E6 |
| D43 | tách UTF-8 LS | S/0 | Native: `author_sep_tree_e280a8` |
| D44 | tách UTF-8 PS | S/0 | Native: `author_sep_tree_e280a9` |
| D45 | tách UTF-8 NEL | S/0 | Native: `author_sep_tree_c285` |
| D46 | expandtabs | S/0 | Native: `key_delimiter_09` |
| D47 | Unicode NFKC | S/0 | Native: `nfkc_fullwidth_key` |
| D48 | xóa CR trong dòng | S/0 | Native: `leading_tree_0d` |
| D49 | xóa byte điều khiển ASCII trong dòng | S/0 | Native: `leading_tree_09` |

Tổng **17 GIET + 22 sống không tương đương trên Git hợp lệ + 10 sống tương đương trong miền hợp lệ**. Trong 17 bị giết, D37 chỉ có phản chứng trên object lỗi; không tự gọi nó là không tương đương trên Git hợp lệ. Chỉ D06/D18/D15 trong 22 survivor được chạy thêm toàn bộ 53 ca; các mục còn lại có phép đo c53 và criterion riêng, không khai toàn ca đã chạy.

- **E1 — D10/D11, NUL:** mọi fixture NUL ở tree/parent/author/extension/body đều bị fsck strict từ chối (10/10 trên hai định dạng; `nulInHeader`, `nulInCommit` hoặc lỗi parse). Không có byte NUL trong miền strict-valid, nên cắt ở NUL là identity. Không dùng đối tượng lỗi làm P2 “Git hợp lệ”.
- **E2 — D12:** sau khi cắt tại LF-LF đầu tiên, không còn dòng rỗng nội bộ có thể nối hai khối header. Bỏ phần tử rỗng không đổi tree hoặc dãy parent hợp lệ.
- **E3 — D14/D16/D33:** tree và dãy parent thật phải đứng trước author và dùng đúng tiền tố cấp ngoài. Dòng trống-whitespace/continuation hợp lệ nằm ở phần mở rộng sau author/committer; xóa chúng hoặc lstrip riêng parent ở đó không vượt được chốt dừng tại author. Không xóa hay tạo dòng tree cấp ngoài. Lstrip tree là phép khác, đã có D32 bị giết.
- **E4 — D31:** decode UTF-8 replacement rồi encode giữ các byte ASCII quyết định tên trường, LF/SP và OID; OID có byte không ASCII vẫn không qua regex. Không tách bằng Unicode splitlines. M1 vẫn cấm dùng replacement trên toàn stdout; tương đương quan sát không phải đề nghị triển khai theo cách này.
- **E5 — D37/D38/D39:** cắt đuôi dòng tại CR/VT/FF không sinh tiền tố tree/parent mới. Tree/parent thực có control trong giá trị không qua fsck; extension đã bắt đầu `tree ` vẫn bị đếm thêm trước và sau khi cắt, nên đều None. D37 chết ở c53 vì đối tượng cố ý hỏng `tree <OID> CR parent <OID>`, không phải vì một commit strict-valid.
- **E6 — D42:** trước khi dùng tree[0]/tree[-1], guard buộc đúng một phần tử; hai chỉ số trỏ cùng giá trị.

Các lập luận trên gắn với chính phép biến đổi và parser hiện tại, kèm đối chiếu trên 168 fixture hợp lệ; không lấy “chưa tìm thấy” làm chứng minh tương đương cho cách viết parser khác. **Rstrip, CRLF normalization và unfold không tương đương**: boundary sweep đã tìm được phản chứng, nên không xếp nhầm chúng vào E1–E6.

**Ba survivor theo M1 và ranh giới oracle**

D03/D28 làm mất dòng extension `tree ` khi rstrip đổi nó thành `tree`; D27 biến CRLF-CRLF bên trong extension thành dấu ngăn header/body sớm và bỏ qua tree cấp ngoài phía sau. Các commit này fsck strict chấp nhận và Git native bỏ qua extension, nhưng **M1 yêu cầu None khi không đúng một dòng tree hoặc giá trị không hợp lệ**. Head trả None đúng M1; mutant trả dict. Criterion của ba mục này dùng `spec_M1`, không giả vờ native kỳ vọng None. Ngay cả khi chủ kho quyết định thay đổi hợp đồng này ở revision sau, **19 mutant có head = native còn lại đã đủ giữ P2**. [Boundary fixtures](boundary-fixtures.json), [kết quả](domain-criterion-results.json).

Tương tự, có **16/168** fixture strict-valid mà head khác native do uppercase OID hoặc tree bổ sung trong extension; tất cả nằm ở quy tắc M1 cố ý chặt hơn Git. Không gọi chúng là lỗi sản phẩm mới trái spec. Trường `expected` trong fixture đầu tiên biểu thị metadata đã dựng; chỉ mode `spec_M1` của criterion boundary dùng kỳ vọng từ chối theo đặc tả. Tránh đưa những ca này vào nhánh oracle luôn đòi dict của c53.

**Hướng vá lớp P2**

Vá tại **c53 và catalogue DOT_BIEN** trong `ops/ci_provenance_test.py`, vì phần thiếu là bằng chứng bảo vệ reader; các counterexample native chưa đòi đổi sản phẩm. Phương án nhỏ nhất là bảng fixture tham số hóa: các byte CR/VT/FF/FS/GS/RS/NEL và UTF-8 NEL/LS/PS trong author; TAB và whitespace làm đầu dòng hoặc phân cách tên header; key khác hoa/thường, key chứa control/NFKC; extension `tree` có continuation; các boundary SP/CRLF và tree rỗng theo M1. Mỗi nhóm phải có tree thật, đủ cha thật không sắp xếp, check fsck strict và so metadata với native khi hợp đồng cho phép; giữ các ca None theo M1 ở nhánh assertion riêng.

Dùng [các cặp mutation đã chạy](all-domain-results.json) làm tiêu chí khóa: sau bổ sung, 22 survivor phải chết **rc3 + DO:c53**, các ca gốc vẫn xanh. Ít nhất các đại diện TAB, VT, key-only lower và unfold phải có criterion phân biệt độc lập; không chỉ đưa lại lstrip đã được khóa. Một bảng theo trục dữ liệu rẻ hơn 22 fixture chép tay; đưa thêm đầy đủ graph SHA-1/SHA-256 giúp kiểm validity tốt hơn các parent OID tổng hợp hiện tại.

Rủi ro khi vá: chuẩn hóa dữ liệu fixture trước khi hash làm mất chính byte cần thử; dùng oracle native cho ca M1 cố ý từ chối làm test sai hợp đồng; dùng parser sản phẩm làm oracle tạo tự xác nhận; bắt rộng lỗi setup thành GIET tạo tín dụng giả. Giữ raw bytes và đối chứng rc, không từ chối rộng gpgsig/mergetag hoặc sửa reader đang đúng trên các nhân chứng. Owner xử lý finding: executor wp978 và chủ kho/điều phối #978. Đây là hướng vá cùng packet, không phải đề xuất mở thêm lớp/nợ để bỏ lịch sử.

**N1–N7**

| Tiêu chí | Trạng thái | rc và bằng chứng dương |
|---|---|---|
| N1 | **passed** | Head c53 rc0; cùng test với sản phẩm base rc3, DO đúng c53 chứa UnicodeDecodeError. [Head](n1-head.json), [base](n1-base.json). |
| N2 | **passed về hành vi đột biến** | Lệnh import/chay_dot_bien đúng prompt rc0: **27/27 GIET**. Chạy riêng từng child: **27/27 rc3**, DO đúng c53, không rc4. Literal text=True X07 cũng rc3. [Runner](n2-prescribed.json), [child](f13-children.json), [X](x-replay-results.json). |
| N3 | **not_run** | Không chạy suite mặc định. `--tat-ca-ca` outer rc0, JSON **53/53 ca rc0**. AST: base 52 ca/292 mutant, head 53/319. Lời khai executor 319/319 ở tham-chieu không phải phép đo reviewer. [53 ca](all-head-cases.json), [đếm](catalogue-counts.json). |
| N4 | **passed** | Ruff F `--no-cache` head/base đều rc0, All checks passed, delta F0. Read-only git diff --check base..head rc0. [Head](n4-head-ruff.json), [base](n4-base-ruff.json), [diff](n4-diff-check.json). Không phải receipt Ruff pin/probe của CI. |
| N5 | **passed** | doctrine-scan rc0, 10 tệp/0 chỗ chép; adr-song rc0, 55 ADR/55 dòng khớp 1–1, output ghi ngoại lệ trạng thái ADR-0016. [Doctrine](n5-doctrine.json), [ADR](n5-adr.json). |
| N6 | **not_measured** | Offline, không đọc check run ci.yml trên GitHub, không dùng lời khai thay đo. |
| N7 | **not_applicable; not_run** | git_cuc_bo không nằm trong HAM_DONG; không chạy --dot-bien-dong, không khai passed. [Catalogue](catalogue-counts.json). |

**Hợp đồng, định danh và toàn vẹn**

Giữ ghi chú từ lượt 4: M1 gọi -p nhưng --batch hiện lấy được loại object gốc và bytes, đóng lớp non-commit mà không peel tag. Clone shallow cục bộ depth1 đã đo lại: native log tại biên trả 0 cha nhưng reader giữ đủ 5 cha từ object, fsck strict rc0. Không đề nghị thay reader bằng `%P` trực tiếp. [Shallow](shallow-results.json).

M2 đóng băng nói chỉ UnicodeDecodeError được đổi thành tín hiệu chốt; bộ bọc hiện đổi Exception có frame reader thành NEM. Đối chứng X11/import/binding xác định hành vi nhưng không tự sửa câu chữ M2. Giữ lưu ý này để chủ kho xác nhận trong hồ sơ có thẩm quyền; P2 hiện tại không dựa vào tranh luận đó. M3 gọi tên F13_doc_text_true nhưng catalogue dùng F13_giai_ma_toan_stdout; literal text=True đã được đo riêng. N3 tăng thực tế 27 mutant so base, không khai khớp nguyên văn +3 của spec cũ.

HEAD detached **afcadd5673009dd4a6a56076af04f57b0ba56c11**, tree **f38e60365520375c50ad25ab3791a8fa6aad2d8a**. Chuỗi base **c8d92ba05c3ea875d8f84d94195430302690286d** → **bef14035718cae862369101f79dc61e938ae6b00** → **7fcfe18181ce4d089225900e36d3aed878877e7f** → **fdf1f05c1b3d845a694c796a81a8bd5c218a68c8** → **aa2a1f326eb964b1cf8f45454593971e0ab11b73** → head được tự kiểm. Local origin/master trỏ base; hash đặc tả khớp. [Preflight](preflight.json), [chuỗi/scope](ast-scope.json).

Diff base..head đúng **2 tệp, +119/-6**; vượt dự kiến 60 dòng thêm nhưng dưới trần sensitive 6 tệp/450 dòng. Lượt aa2a1f3..head chỉ thêm **3 dòng test**; sản phẩm cùng blob. AST sản phẩm: chỉ git_cuc_bo đổi, thêm regex OID; main/moc_checkout/git_blob/doc_wf/REST không đổi. [Diff toàn bộ](diff.patch), [diff lượt này](step1-diff.patch), [AST](ast-scope.json).

Reviewer Codex/họ OpenAI; launcher ghi **openai_codex / codex_cli / machine**, run **31fda992006a4c41861fbe418ee27510**. Exact serving model/effort **not_measured**. Executor họ Claude theo assignment/lease, không tự đo runtime. Không có context executor hoặc phiên model phụ; chỉ chạy các tiến trình kiểm tra cục bộ. `cross_approved` là assurance target, verdict request_changes này không cấp approved assurance. [Identity](identity.json). Assignment r1/g1 sensitive, lời gọi 5/8 theo prompt; không truy cập remote để xác minh freshness/issuecomment và không dùng trần 2 cũ để xin lại quyền đã được assignment cấp.

Linux, Python **3.13.17**, Git **2.43.0**, PyYAML **6.0.3**, Ruff **0.17.3**. Dùng `python -B`, PYTHONDONTWRITEBYTECODE=1, TMPDIR tuyệt đối `out/tmp`, Git global/system config /dev/null, optional locks tắt trong runner, Ruff no-cache. Mọi fixture/mutant/artifact nằm dưới OUT; không cài công cụ. [Versions](versions.json).

Snapshot cuối: **7.205/7.205 tệp tracked SRC không đổi SHA-256**, head/tree/spec không đổi, tracked/index diff rỗng, status gồm untracked/ignored rỗng ở đầu/cuối. Bản sao head cũng khớp 7.205 tệp nguồn. Không suy thành kiểm mọi byte `.git` hay chứng minh lịch sử chưa từng ghi rồi hoàn nguyên. [Snapshot cuối](final-source-snapshot.json).

Lệnh đầy đủ, cwd, rc, stdout/stderr và thời lượng nằm trong các receipt JSON. Script điều phối: [checks](checks.py), [regression](regression.py), [replay X](replay_x.py), [domain](header_domain.py), [boundary](domain_boundary.py), [Unicode/control bổ sung](domain_extra.py), [criterion và toàn ca](domain_verify.py), [audit](final_audit.py). Tái tạo fixture bằng OUT mới; không chạy các script này trên SRC. [Lịch sử verdict cập nhật](VERDICT.progress.md).

D02, F10/D05 của #899, ci_dang_ky_test.py --chay, Workflow definition, LIVE CI, Windows native, SHA-256 toàn tuyến main đều ngoài phạm vi; không tính hạng hoặc khai đã đo. Không soạn/thử nội dung đường dẫn thoát cây. Không mạng, GitHub, push, merge hay land.
