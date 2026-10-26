verdict: approve
reviewed_sha: 1f731c7bfc99c8fca3cba74d4cd8bbf6a14db986
base_sha: ba222ffd1615f0d74b59985b9612f725211b62f5
Reviewed commit: 1f731c7bfc99c8fca3cba74d4cd8bbf6a14db986
reviewed_tree: 13843e747b31df410a56e83b1dbc2f98a76e7d2d
packet: wp899-r4-g4
generation: 4
spec_hash: be1e1feabe7c23b832168e36b0cce333043863af505e65c48d5a22d2101cef45
review_class: sensitive
review_call: 11/12 (offline cuối, theo authority trong prompt)
role: reviewer
provider: openai_codex
model_family: openai
model: gpt-6.1-sol (CLI-published)
effort: xhigh (CLI-published)
session_id: 01a175b4-e325-74b1-b29d-14552f553759
execution_surface: codex_cli
transport: machine
github_submitter_identity: null
independent_from_executor_session: true
review_axes: [spec, standards_security]
assurance: review_deferred (chờ receipt vận chuyển/định danh sau khi process kết thúc)

**Nội dung đạt V2: P0=0, P1=0, P2=0.** Hai lớp còn nợ P3: D02 và F10/D05, có quyết định đề xuất dưới đây. Đã đo lại **1009/1009 mã tập đóng: 1001 GIET, 8 tương đương, 0 SONG ngoài danh sách, 0 TIN_DUNG_GIA, 0 chứng minh tương đương sai**. Bộ thường **52/52 ca, 292/292 mutant giết đúng lý do, tự kiểm 2/2, TONG: DAT**. Không tìm được lỗi sản phẩm trên phạm vi tự đo. Approve này là verdict nội dung trên exact SHA, không tự chuyển state, tạo `cross_approved`, miễn A9 hay cấp quyền đẩy/land. A13 còn phần chỉ người vận chuyển đo được sau khi lượt này kết thúc.

## Authority, preflight và giới hạn

Đọc CONTEXT, protocol, CLAUDE, skill cross-review, kế hoạch đa provider, prompt offline, toàn bộ spec r4 và các mục được dẫn trong r2/r3. Nguồn authoritative của lượt offline là `.review-input/wp899-r4.md` do user chỉ định; hash bytes đúng `be1e1feabe7c23b832168e36b0cce333043863af505e65c48d5a22d2101cef45`. Không dùng tên nhánh thay định danh. Chấp nhận nguyên Q1–Q12, D01/D02, checkpoint nâng budget lên 12, trần khoảng 2050 và effective write set g4 chỉ còn hai tệp; không mở lại các quyết định ấy thành finding. Không tự xác minh freshness GitHub/lease qua mạng.

`snapshot-start.json` giữ command/rc: origin `https://github.com/ducthangho/tra-luat.git`; detached HEAD đúng OID trên; base là commit có thật và ancestor (rc0); `core.abbrev=7`. Diff base→HEAD chỉ có `ops/ci_provenance.py` +444 và `ops/ci_provenance_test.py` +1600 = **2044 dòng**. Đã đọc cả delta `d2cca1580ed23dbbc532fb21481d0fac1e6ad8ac..HEAD` và toàn bộ mã sản phẩm; `git diff --check`, tracked diff/index/status đều rc0/rỗng. `frontier11.json` giữ SHA-256 hai nguồn sản phẩm/test. Mọi sửa đổi và bản sao phản chứng do reviewer tạo nằm trong `.review/`, không sửa branch Executor.

Runtime: Linux x86_64, Python 3.13.17, PyYAML 6.0.3, Git 2.43.0, Ruff 0.15.15; sandbox workspace-write, approval never, nhiệm vụ offline. `identity11.json` đọc đúng rollout của thread/cwd này: CLI 0.164.0, `originator=codex_exec`, `model_provider=openai`, model/effort như trên. Đây là **model do CLI công bố**; model phục vụ từng request **KHÔNG ĐO ĐƯỢC**. File rollout còn đang được ghi; stdout `thread.started`, terminal/launcher rc, size/hash rollout cuối và receipt vận chuyển chưa ở phạm vi reviewer đang chạy, owner phải hoàn tất A13 sau process. `codex --version` rc0 có cảnh báo không tạo được PATH aliases trên filesystem chỉ đọc; không diễn giải thành phép đo gọi model khác.

## BẢNG LỚP

Hai lớp P3 / hai biểu hiện còn mở; không có lớp P0–P2 còn mở. Không dùng các mutant ngoài bảng cố định để mở rộng thước F10 của r4.

| lớp | hạng | biểu hiện (tệp:dòng) | phép đo tái hiện | HINT patch | ước lượng dòng |
|---|---|---|---|---|---|
| D02 `uses-nhieu-dong` | P3 kế thừa | `ops/ci_provenance.py:174`: tên implicit của uses nhiều dòng giữ dòng đầu | Assertion lịch sử `name_uses_whole_value` trong `history11`; không có log runner mới | **Giữ nợ theo quyết định chủ kho**, owner `ducthangho`; không vá trong r4. Nếu mở lại, dùng successor cùng fixture runner thật cho uses nhiều dòng. Ca phải phân biệt toàn giá trị uses với dòng đầu; tránh đổi luật tên run cùng lúc. Rủi ro: đổi bộ ghép tên run ngoài scope. | 0 ở packet này |
| F10 `fixture-dinh-danh-buoc-chi-giu-dang-khop`, D05 `try-boundary-chua-duoc-catalogue-khoa` | P3, mutant ngoài tập đóng; HEAD đúng | `ops/ci_provenance_test.py:1044`, `ops/ci_provenance.py:158`: c52 kiểm lỗi parse nhưng chưa khóa lỗi ngoài vùng parse. Mutant dời return kiểm kiểu vào try sống **52/52** ca catalogue | `wide-try-catalogue.stdout.txt` có 52 rc0; `patch11-results.json` đo HEAD để lỗi validation nổi lên, mutant nuốt lỗi; test bổ sung `r11_scope_outside_parse` giết đúng bằng TinHieuChotCa/rc3 | **Đề xuất ghi nợ test, owner `ducthangho`, xử lý successor; không vá sản phẩm, không mở vòng r4 chỉ vì P3.** Nếu được giao, thêm fault injection tại c52 hoặc ca riêng: safe_load trả dict hợp lệ, phép kiểm kiểu phía sau ném sentinel, đòi sentinel nổi lên. Khóa mutant mở rộng try. Chốt đặt ở test reader vì chính vùng try là tính chất cần giữ. Rủi ro: mock `type`/module không khôi phục làm nhiễm ca sau; dùng module mới hoặc context khôi phục. | khoảng 8–15 dòng test khi được giao |

D05 nối **đúng slug F10**, không tạo lớp mới để xóa lịch sử. Đây là thiếu răng đối với một thay đổi ngoài tập đóng; dữ liệu bình thường không làm built-in `type` của HEAD ném sentinel. Không có lỗi sản phẩm thật và không có mutant của chính tập đóng sống; vì vậy áp mục 7: P3. Phép đo bổ sung của reviewer đã giết mutant này, nhưng **không** khai catalogue hiện có đã giết nó.

## ĐỐI CHIẾU LƯỢT TRƯỚC và bản vá lượt 10

Lượt có verdict gần nhất là r4 lượt 9 / `d2cca1580ed23dbbc532fb21481d0fac1e6ad8ac`; lượt 10 không có verdict, chỉ có quan trắc OverflowError. Không coi output bị cắt là review hoàn chỉnh.

| finding/biểu hiện cũ | kết quả trên HEAD | bằng chứng tự đo |
|---|---|---|
| F12 `loi-constructor-yaml-thoat-doc-wf` / P2 | **ĐÃ VÁ THẬT** trong phạm vi reader đã đo | Chạy lại nguyên 8 fixture F12 bằng reader Git thật/REST stateful: 8 con rc0, Gate/ghép not_measured, không marker, không traceback. Đối chứng có nháy rc0/Gate passed. `product-yaml9-results.json`, `yaml-fixtures.*`. |
| OverflowError lượt 10 và lỗi parse theo lớp | **ĐÃ VÁ THẬT** bằng đổi ranh giới | Tiêm OverflowError/LookupError/TypeError/RuntimeError/OSError/lớp Exception riêng vào safe_load đều trả None; không soạn YAML hỏng mới. KeyboardInterrupt/SystemExit vẫn nổi lên. 10 mutant bắt từng lớp đơn/tuple lượt 9 chết rc3 đúng c52. `patch11-results.json`. |
| Vùng try của bản vá | HEAD đúng; D05/P3 về catalogue | AST xác nhận try có đúng một assignment gọi safe_load. 10 đối chứng kiểu trả về, kể cả dict subclass và jobs sai kiểu, giữ chốt exact dict/jobs. Mutant try rộng sống catalogue, bị test tiêm lỗi ranh giới của reviewer giết; không nhầm hai phạm vi ấy. |
| F10/D03 alias job và name bước có biểu thức giữa chuỗi | **ĐÃ VÁ THẬT biểu hiện cũ** | Hai mutant startswith thay kiểm contains chết đúng c52, baseline cùng ca rc0. `classifier11-results.json`, tên `L9_D03_*`; HEAD tiếp tục chặn `Build ${{x}}`. F10 còn D05/P3 ngoài bảng. |
| D04 đếm số bước xác thực | **ĐÃ VÁ THẬT** | `L9_D04_dem_mot_buoc` chết đúng c51 do hai bước phải được đếm 2; baseline rc0. |
| D02 | GIỮ NỢ, không gọi là vá | Assertion lịch sử và authority đã giao; không có fixture runner thật mới. |
| ExceptHandler/RecursionError lượt 8 | Giữ đóng | `gap8.py` và `gap_e2e8.py` dùng fixture có sẵn: HEAD trả None / Gate not_measured / không marker; mutant bỏ vùng bắt RecursionError ném RecursionError và chết đúng c52. |

`product_yaml9.py` được chép sang `.review/product_yaml11.py`, giữ nguyên 9 byte fixture và quy trình Git/REST; chỉ sửa assertion cuối từ kỳ vọng crash cũ sang kỳ vọng bản vá. Hai script gap8 được chép vào `.review/`; do HEAD đã đổi tuple sang Name `Exception`, neo mutation được đổi sang bắt riêng `yaml.YAMLError` để giữ nguyên mục tiêu bỏ RecursionError. Assertion “all_green” cũ đổi sang đòi mutant bị ca đích giết; khai rõ không chạy nguyên neo `.elts.pop` đã hết hợp lệ. Không dùng lỗi setup của script cũ làm finding sản phẩm.

Với U gồm bốn lớp còn mở ở verdict 9 `{F12,F10,D02,D04}`, đóng trọn được `{F12,D04}` = **2/4 (50%)**. F10 đã đóng D03 nhưng còn D05/P3 mới cùng lớp; không tính hạ hạng hay đổi thước thành đóng toàn lớp. D02 giữ nợ không được tính vá. Không tự cấp thêm budget hoặc review offline.

## Bộ sinh, phân hạng và BẢNG KIỂU NÚT

`audit11.py` tái dựng từng lượt duyệt AST/chỉnh/unparse/compile, so **cả ID và nguồn** với `sinh_dot_bien_dong`: **1009** nguồn có hiệu lực, **0 compile skip, 0 trùng ID**, thêm mã ngoài chín hàm không đổi dãy ID. Hai no-op loại có ghi sổ: `doc_wf#12:tra_None`, `_gio#7:tra_None`; không phải mutant bị nuốt. Có 13 nhóm nguồn trùng, vẫn giữ đủ ID. Danh sách tương đương không trỏ mã rời tập. Không nhận con số executor làm bằng chứng.

Đối chiếu bảng kiểu nút lượt 8/9: đo thêm **41 mutant** trên Assign/Expr/AugAssign (bỏ statement), USub→UAdd, BinOp dict-union→intersection, NamedExpr bỏ binding, ExceptHandler thu hẹp lớp, Slice biên động ±1. **41 GIET đúng ca, 0 SONG, 0 TIN_DUNG_GIA** (`operators11-results.json`). Bản vá lớp Exception đã được đo riêng bằng fault injection như trên. Chưa tìm được lỗ kiểu nút theo mục 3a: một mutant bậc một tự nhiên sống và đổi kết quả spec định nghĩa. Không tuyên bố các kiểu không toán tử đã được bao phủ mọi cách sửa.

`criteria11.py` và `classifier11.py` đo rc0, lỗi vô can rc4, rc3 sai tên, rc3 đúng tên; chỉ trường hợp cuối được GIET. Đã chạy bốn fixture qua **toàn pipeline** `chay_dot_bien_dong`: ba trường hợp không giết đều rc1/TONG DONG DO; đúng ca mới rc0/DAT. `--tat-ca-ca` tiếp tục sau rc4 và dừng sau rc3 đúng ca đầu tiên. A7 có baseline rc0 và hai mutant rc3 đúng c18/c19; không thay bằng tổng suite.

Census: **49 kiểu / 1525 nút**, gồm hàm lồng và nút phụ trợ. Cột thứ ba đếm nút có `_toan_tu` riêng sau khi bỏ docstring. Eq/In/And/Not… được biến đổi tại nút cha; số 0 ở nút phụ trợ không tự là lỗ. Bảng này khai khả năng và giới hạn, không là chứng nhận mọi kiểu đã được mutation coverage đầy đủ.

| kiểu nút | số nút | nút có toán tử riêng | có / không / mutant đo được |
|---|---|---|---|
| Add | 5 | 0 | Không riêng; xem phép đo bổ sung và nút cha. |
| And | 17 | 0 | Không riêng; xem phép đo bổ sung và nút cha. |
| Assign | 21 | 0 | Không riêng; xem phép đo bổ sung và nút cha. |
| Attribute | 48 | 0 | Không riêng; xem phép đo bổ sung và nút cha. |
| AugAssign | 1 | 0 | Không riêng; xem phép đo bổ sung và nút cha. |
| BinOp | 8 | 0 | Không riêng; xem phép đo bổ sung và nút cha. |
| BitOr | 3 | 0 | Không riêng; xem phép đo bổ sung và nút cha. |
| BoolOp | 25 | 25 | Có: and<->or, bo_ve0, bo_ve1, bo_ve2, bo_ve3, bo_ve4, bo_ve5, bo_ve6 |
| Call | 109 | 14 | Có: bo_doi_so0, bo_doi_so1, bo_doi_so2 |
| Compare | 37 | 37 | Có: so0->Eq, so0->GtE, so0->In, so0->Is, so0->IsNot, so0->Lt, so0->NotEq, so0->NotIn, so1->GtE, so1->Lt |
| Constant | 159 | 139 | Có: +1, -1, bool, chuoi0, chuoi1, chuoi2, chuoi3, chuoi4, chuoi5, chuoi6, chuoi7 |
| Continue | 1 | 0 | Không riêng; xem phép đo bổ sung và nút cha. |
| Dict | 7 | 0 | Không riêng; xem phép đo bổ sung và nút cha. |
| Eq | 5 | 0 | Không riêng; xem phép đo bổ sung và nút cha. |
| ExceptHandler | 2 | 0 | Không riêng; xem phép đo bổ sung và nút cha. |
| Expr | 11 | 0 | Không riêng; xem phép đo bổ sung và nút cha. |
| For | 3 | 0 | Không riêng; xem phép đo bổ sung và nút cha. |
| FunctionDef | 10 | 0 | Không riêng; xem phép đo bổ sung và nút cha. |
| GeneratorExp | 8 | 0 | Không riêng; xem phép đo bổ sung và nút cha. |
| If | 15 | 15 | Có: if_dung, if_sai |
| IfExp | 12 | 12 | Có: ifexp_khac, ifexp_than |
| In | 6 | 0 | Không riêng; xem phép đo bổ sung và nút cha. |
| Is | 12 | 0 | Không riêng; xem phép đo bổ sung và nút cha. |
| IsNot | 2 | 0 | Không riêng; xem phép đo bổ sung và nút cha. |
| Lambda | 1 | 0 | Không riêng; xem phép đo bổ sung và nút cha. |
| List | 8 | 0 | Không riêng; xem phép đo bổ sung và nút cha. |
| ListComp | 7 | 0 | Không riêng; xem phép đo bổ sung và nút cha. |
| Load | 388 | 0 | Không riêng; xem phép đo bổ sung và nút cha. |
| LtE | 2 | 0 | Không riêng; xem phép đo bổ sung và nút cha. |
| Name | 320 | 0 | Không riêng; xem phép đo bổ sung và nút cha. |
| NamedExpr | 5 | 0 | Không riêng; xem phép đo bổ sung và nút cha. |
| Not | 11 | 0 | Không riêng; xem phép đo bổ sung và nút cha. |
| NotEq | 4 | 0 | Không riêng; xem phép đo bổ sung và nút cha. |
| NotIn | 7 | 0 | Không riêng; xem phép đo bổ sung và nút cha. |
| Or | 8 | 0 | Không riêng; xem phép đo bổ sung và nút cha. |
| Return | 20 | 20 | Có: tra_None |
| SetComp | 1 | 0 | Không riêng; xem phép đo bổ sung và nút cha. |
| Slice | 5 | 0 | Không riêng; xem phép đo bổ sung và nút cha. |
| Store | 66 | 0 | Không riêng; xem phép đo bổ sung và nút cha. |
| Sub | 1 | 0 | Không riêng; xem phép đo bổ sung và nút cha. |
| Subscript | 57 | 0 | Không riêng; xem phép đo bổ sung và nút cha. |
| Try | 2 | 0 | Không riêng; xem phép đo bổ sung và nút cha. |
| Tuple | 21 | 0 | Không riêng; xem phép đo bổ sung và nút cha. |
| USub | 2 | 0 | Không riêng; xem phép đo bổ sung và nút cha. |
| UnaryOp | 13 | 11 | Có: bo_not |
| arg | 21 | 0 | Không riêng; xem phép đo bổ sung và nút cha. |
| arguments | 11 | 0 | Không riêng; xem phép đo bổ sung và nút cha. |
| comprehension | 16 | 4 | Có: bo_loc0 |
| keyword | 1 | 0 | Không riêng; xem phép đo bổ sung và nút cha. |

Phép đo cho các hàng không có toán tử: 41 mutant mới nêu trên; Try mở rộng có đối chứng D05; các method/slice/bỏ phần tử đã có thước ở lượt 8/9 không được tự coi đã đo lại toàn frontier ngoài tập trong lượt này. Trọng tâm r4 theo authority vẫn là bảng toán tử cố định và lỗi sản phẩm.

## Tám chứng minh `TUONG_DUONG`

Giữ cả tám. Từng mã được chạy lại trong toàn tập đóng; thêm đầu vào phân biệt riêng dưới đây. Mẫu hữu hạn là đối chứng; lập luận cấu trúc mới là lý do giữ.

| mã | giữ / bác | lập luận | đối chứng tự chạy |
|---|---|---|---|
| `ghep_job#24:-1` | GIỮ | `khop[-1]` thay `khop[0]` chỉ được tính khi `len(khop) == 1`, mà danh sách một phần tử có [0] và [-1] là cùng một phần tử | 25 cặp, 0 khác biệt |
| `chan_buoc#103:bo_doi_so1` | GIỮ | `str(t.get('run'))` thay `str(t.get('run', ''))` chỉ khác ở bước KHÔNG có `run:`: chuỗi tìm là 'None' thay vì '' — cả hai đều không chứa `GITHUB_ENV`/`GITHUB_PATH`, nên `re.search` cùng trả None | 7 cặp, 0 khác biệt |
| `tach_buoc#173:chuoi2` | GIỮ | chuỗi chỉ đứng trong `len('##[group]Run ')`: biến dạng hoa/thường/đảo hoa giữ NGUYÊN độ dài 13 nên lát cắt `lenh` không đổi (biến dạng đổi độ dài — hậu tố, bớt ký tự, khoảng trắng, rỗng — bị giết) | 5 cặp, 0 khác biệt |
| `tach_buoc#173:chuoi3` | GIỮ | chuỗi chỉ đứng trong `len('##[group]Run ')`: biến dạng hoa/thường/đảo hoa giữ NGUYÊN độ dài 13 nên lát cắt `lenh` không đổi (biến dạng đổi độ dài — hậu tố, bớt ký tự, khoảng trắng, rỗng — bị giết) | 5 cặp, 0 khác biệt |
| `tach_buoc#173:chuoi4` | GIỮ | chuỗi chỉ đứng trong `len('##[group]Run ')`: biến dạng hoa/thường/đảo hoa giữ NGUYÊN độ dài 13 nên lát cắt `lenh` không đổi (biến dạng đổi độ dài — hậu tố, bớt ký tự, khoảng trắng, rỗng — bị giết) | 5 cặp, 0 khác biệt |
| `do_dau_duong#127:bo_ve0` | GIỮ | bỏ vế `goi and`: khi `goi` rỗng thì `all(goi)` là True nhưng `[g[2] for g in goi]` cũng rỗng ⇒ vòng lặp không chạy lần nào, y như nhánh `else []` | 351 cặp, 0 khác biệt |
| `do_dau_duong#306:chuoi1` | GIỮ | `run.rstrip('')` (cả hai mã cùng một nguồn đột biến) chỉ để lại các `\n` cuối ⇒ `split` sinh thêm đoạn RỖNG ở đuôi; `dong_logic` biến đoạn rỗng thành '' (hoặc nối vào dòng `\` đang dở rồi `strip()` ra cùng chuỗi), và `if d` bỏ ''. Phép so khối `run.rstrip("\n") == …` đứng TRƯỚC không đổi | 351 cặp, 0 khác biệt |
| `do_dau_duong#306:chuoi4` | GIỮ | `run.rstrip('')` (cả hai mã cùng một nguồn đột biến) chỉ để lại các `\n` cuối ⇒ `split` sinh thêm đoạn RỖNG ở đuôi; `dong_logic` biến đoạn rỗng thành '' (hoặc nối vào dòng `\` đang dở rồi `strip()` ra cùng chuỗi), và `if d` bỏ ''. Phép so khối `run.rstrip("\n") == …` đứng TRƯỚC không đổi | 351 cặp, 0 khác biệt |

## Tập đóng đã đo

Lệnh thật `python -B ops/ci_provenance_test.py --dot-bien-dong 8`, thông qua wrapper chỉ ghi command/rc/stdout/stderr `.review/run11.py`. **Chạy lại mới cả 1009/1009**, không lấy mẫu thay, không dùng lại log executor, không dùng resume (`CIP_DONG_TIEP` và `CI_PROVENANCE_MA` không đặt, có receipt). Kết quả **1001 GIET + 8 SONG đúng danh sách tương đương; 0 TIN_DUNG_GIA; TONG DONG: DAT, rc0**.

`full-validation11.json` đối chiếu 1009 record/ID duy nhất và prefix hash nguồn của từng mutant với audit độc lập; không thiếu/thừa ID. Đã đo lại đủ **57/57** mã chưa giết lượt đầu: **49 GIET + 8 tương đương**. File gốc chứa 1009 record = 952 GIET + 30 SONG + 27 TIN_DUNG_GIA; regex đọc cả record nối dòng, không đếm số dòng làm số mã. Không có mã thứ 58. Đã kiểm cả chín hàm; số nguồn: `_env_chan` 33, `doc_wf` 14, `ghep_job` 46, `ten_du_kien` 71, `_gio` 19, `ghep_buoc` 292, `chan_buoc` 96, `tach_buoc` 229, `do_dau_duong` 209.

## Săn lỗi sản phẩm

**Không tìm được lỗi sản phẩm mới** trong các hướng đã chạy. Oracle mới seed899011 có **2000/2000** kịch bản khớp cả ghép, lý do, markers, số bước xác thực và Gate; lịch sử seed899009 **1000/1000**, seed899008 **300/300**, không mismatch. Thử REST đảo thứ tự số bước; key/alias Unicode và ký tự regex; tiền tố matrix; run/uses/skipped xen kẽ; env null/vắng và defaults các mức; shell; tiền tố VAR; PATH trước bước; sai số nhóm/REST/YAML, tên, giờ, number, job. Oracle dựng kỳ vọng theo các trục spec, không gọi hàm sản phẩm để dựng đáp án.

`history11.py` chép/rerun script lượt 1–7 trên HEAD: **169 assertion cases** của lượt 3–7 đạt, **2×34 quan trắc** lượt 1/2 không ném; không gọi các quan trắc là assertion suite. Các fixture parse hỏng chỉ lấy từ `.review-input/`. Không tự soạn nội dung tấn công nhạy cảm, không đo bằng mạng, không cố vượt gốc tin của workflow/action tại SHA. Kiểm thêm constructor/PyYAML version, parser khác, dữ liệu log Windows/composite thật mới là **KHÔNG ĐO ĐƯỢC** trong lượt này.

## ĐỐI CHIẾU F01–F11

| lớp | trạng thái trên HEAD | bằng chứng / giới hạn |
|---|---|---|
| F01 `thieu-dinh-danh-van-passed` | GIỮ ĐÓNG trong miền đo | c22 và metadata/collection; thiếu không nâng thành passed; suite và oracle. |
| F02 `nhac-ten-script-thanh-thuc-thi` | GIỮ ĐÓNG các biểu hiện đã giao | c23/c25–27/c35/c40–43, history, oracle: đúng bước/job, khối nguyên văn, nested/composite fail-closed. Giữ giới hạn gốc tin. |
| F03 `phan-trang-dem-thay-vi-chung-minh-du` | GIỮ ĐÓNG | c20: trang thiếu/lặp/total đổi cho jobs/artifacts, không chỉ len=total. |
| F04 `rest-gia-khong-neo-run` | GIỮ ĐÓNG | c20 và RestGia stateful: URL run/attempt/log sai không được trả state của run đúng. |
| F05 `duong-loi-bo-dong-dem-bat-buoc` | GIỮ ĐÓNG | c01/c18/c19/c22, A7 receipt dương/âm riêng. |
| F06 `redirect-loi-thoat-ngoai-bo-boc` | GIỮ ĐÓNG | c24: mock lỗi trước/sau redirect và không mang token; không phải phép đo network thật. |
| F07 `a10-doi-sha-khi-checkout-skipped` | GIỮ ĐÓNG theo authority | A10 replay 13+1 / 22+1; chuan-bi không có SHA, không bù bằng head REST. |
| F08 `nguon-workflow-git-khong-duoc-kiem-thu` | GIỮ ĐÓNG | c34 Git/blob thật, thiếu path/nonUTF8; F12 parse sau reader được kiểm riêng. |
| F09 `thoi-diem-khong-hop-le-van-ghep` | GIỮ ĐÓNG trong miền đo | c38/c51: lịch/biên/format/cửa sổ, oracle và replay. |
| F10 `fixture-dinh-danh-buoc-chi-giu-dang-khop` | Đóng các biểu hiện chặn cũ, còn D05/P3 | Đủ tập đóng, audit generator, lớp ExceptHandler, D03 đã có răng; Try-boundary ngoài bảng được khai riêng, không gọi toàn lớp đóng. |
| F11 `chan-path-chua-co-phan-chung` | GIỮ ĐÓNG | c42/c47–51, lịch sử và oracle mới: PATH trước/cùng job, khác job/sau không làm bẩn. |

## Đối chiếu A1–A27

| tiêu chí | trạng thái / phép đo và giới hạn |
|---|---|
| A1 | passed, c01: help đủ bốn cờ, sai đối số rc2 và dòng đếm. |
| A2 | passed, c02: attempt lệch failed/rc12, đối chứng đúng passed. |
| A3 | passed offline, c03–09: Linux/Windows fixture, thiếu/nhiều/lệch SHA, PR parents; không là Windows/PR LIVE execution. |
| A4 | passed, c10–15 và M4/M12: runner0/not_run, skipped, marker đúng bước, MOI import một nguồn. |
| A5 | passed, c16: Workflow definition luôn not_measured, REST path chỉ là lời khai. |
| A6 | passed, c17: fault injection writer, không để đích nửa vời/giữ đích cũ. |
| A7 | passed, c18/c19, hai receipt baseline rc0 / mutant rc3 đúng ca; đếm và REST403/rc3. |
| A8 | passed: 52/52, 292/292, tự kiểm2, TONG DAT; full closed 1009/1009 đạt. |
| A9 | **failed, giới hạn đã khai g4**: registry rc1, ĐĂNG KÝ25/24, test sống chưa đăng ký. `--chay` not_run; không sửa file ngoài write set. Cần lease khác khôi phục MOI trước gate-registry/land. |
| A10 | passed replay offline / LIVE KHÔNG ĐO ĐƯỢC: 37 hash đúng, hai provenance byte-identical; không suy retention/freshness endpoint hôm nay. |
| A11 | passed local theo authority: 2 tệp/2044 dòng; diff-check0; Ruff0; doctrine10/0; ADR53/53. |
| A12 | not_run/not_measured: không ls-remote, không đẩy/CI/connector; không chứng nhận nhánh remote chưa tồn tại. |
| A13 | partial / KHÔNG ĐO ĐƯỢC phần cuối process: identity CLI/thread/cwd đã đọc, terminal/launcher/rollout cuối do owner thu sau; verdict chưa tự tạo assurance. |
| A14 | passed, c25: metadata màu không thành kịch bản. |
| A15 | passed, c26: khối tập con không thành xác thực. |
| A16 | passed, c27/c52: toàn khối/nguyên văn/tối giản và đối chứng dương. |
| A17 | passed, c28–31/c46/c48–52: env/null/D01, shell/defaults/VAR; giữ giới hạn uses đứng trước. |
| A18 | **passed trong miền tự đo**: c32/c34/c52, 8 scalar F12 + đối chứng Git thật, fixture gap8, 18 tiêm lỗi/kiểu; 10 mutant bắt hẹp bị c52 giết. |
| A19 | passed, c33 và lịch sử: run trùng job khác, chặn từ đúng job. |
| A20 | passed, c36: số nhóm/REST/YAML, không zip cắt ngắn. |
| A21 | passed, c37/c48–52: tên explicit/implicit/mismatch; hai mutant D03 c52 giết. D02 giữ theo authority. |
| A22 | passed, c38/c51, lịch/giờ/format/cửa sổ và replay thật. |
| A23 | passed, c39/c47–52: key/name/prefix/duy nhất; không đánh giá biểu thức matrix. |
| A24 | passed, c40/c35 và nested lịch sử; không ép giết đột biến tương đương. |
| A25 | passed offline, c41/composite lịch sử; composite runner thật mới KHÔNG ĐO ĐƯỢC. |
| A26 | passed, c42/c47–51 và oracle: ENV/PATH trước/cùng job, khác job/sau. |
| A27 | passed, c43: khối của bước khác không thành marker. |

## Replay A10

Chạy `replay11.py` bằng mã HEAD, Git objects cục bộ, REST stateful từ hiện vật A10 và log đầy đủ. **37/37** log khớp `SHA256SUMS`; hai provenance **khớp từng byte** bản trên `52e9573`; không có khác biệt cần giải thích. `replay8-results.json` giữ từng hash/request giả/trạng thái.

| run / attempt | Run | Checkout / ghép | Gate / marker | SHA-256 provenance |
|---|---|---|---|---|
| 39342960764 /1 | passed | 13 passed b27fe85… +1 chuan-bi not_measured; ghép13/14 | 14 Gate not_measured,0 failed,0 marker trong MOI (vẫn có đường ngoài MOI/not_measured) | `5ad9afeafb5312101ae326d738855e8adb1e46e7e4240944c2b21e12ed2bafe0` |
| 40074551995 /1 | passed | 22 passed dc65714… +1 chuan-bi not_measured; ghép22/23 | 23 Gate not_measured,0 failed;8 nhanh_don_duoc not_measured/che_do_khong_xac_dinh; gate-nhanh-gop không marker | `24ffa770ff268876c030f12f59fee1010956138ba2ca3fa4370710456ffd185b` |

Labels đều ubuntu-latest; Workflow definition vẫn not_measured. Replay không thay LIVE, GraphQL, freshness remote hay required CI trên SHA này.

## Command, rc, trạng thái và bằng chứng

Mỗi label có `<label>.json` (command, rc tiến trình thật, elapsed, hash stdout/stderr) và `<label>.stdout.txt` / `.stderr.txt`. Wrapper đặt `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR/TMP/TEMP` trong `.review/tmp`; các lệnh chạy ca/đột biến dùng `-B`. Positive evidence cụ thể ở các mục trên, không chỉ rc0. Bản gốc và mutant được dựng trong cùng checkout/runtime; không vá rồi hoàn nguyên trên cây thật.

| label | command thực sự | rc | trạng thái | thời gian |
|---|---|---|---|---|
| `preflight` | `python -B .review/preflight11.py` | 0 | passed | 2.0s |
| `yaml-fixtures` | `python -B .review/product_yaml11.py` | 0 | passed | 2.6s |
| `patch` | `python -B .review/patch11.py` | 0 | passed | 32.5s |
| `gap-fixtures` | `python -B .review/gap8.py` | 0 | passed | 24.3s |
| `gap-e2e` | `python -B .review/gap_e2e8.py` | 0 | passed | 0.6s |
| `generator-audit` | `python -B .review/audit11.py` | 0 | passed | 101.7s |
| `equivalences` | `python -B .review/equivalence11.py` | 0 | passed | 0.5s |
| `operators` | `python -B .review/operators11.py` | 0 | passed | 44.8s |
| `criteria` | `python -B .review/criteria11.py` | 0 | passed | 2.2s |
| `classifier-pipeline` | `python -B .review/classifier11.py` | 0 | passed | 22.8s |
| `wide-try-catalogue` | `python -B .review/closed8.py child .review/patch-wide-try.py doc_wf` | 0 | passed | 65.9s |
| `history` | `python -B .review/history11.py` | 0 | passed | 16.6s |
| `product-history` | `python -B .review/product8.py` | 0 | passed | 0.6s |
| `product-oracle` | `python -B .review/product9.py` | 0 | passed | 0.5s |
| `product-new-oracle` | `python -B .review/product11.py` | 0 | passed | 0.8s |
| `replay` | `python -B .review/replay11.py` | 0 | passed | 5.1s |
| `suite` | `python -B ops/ci_provenance_test.py` | 0 | passed | 2325.5s |
| `closed` | `python -B ops/ci_provenance_test.py --dot-bien-dong 8` | 0 | passed | 1844.4s |
| `ruff` | `python -B -m ruff check --no-cache --select F ops/ci_provenance.py ops/ci_provenance_test.py` | 0 | passed | 0.2s |
| `doctrine` | `python -B .claude/dev/packet_loop.py doctrine-scan --root .` | 0 | passed | 0.8s |
| `adr` | `python -B .claude/dev/packet_loop.py adr-song --root .` | 0 | passed | 0.3s |
| `registry` | `python -B .claude/dev/ci_dang_ky_test.py` | 1 | failed / giới hạn g4 đã khai | 0.9s |

`ruff-contract11.json` riêng ghi `loi_ruff_ci`: 3 hợp đồng,0 lỗi. Đây là kiểm pin/probe cấu trúc CI; bare lint thật trên **hai tệp mới** có receipt riêng `ruff.json`, All checks passed. Bare lint scripts/tl.py và full release/legacy selftest toàn kho **not_run**. Registry được giữ `failed`, không đổi thành skipped/pass. Không có required check skipped nào được nhận làm pass.

Mạng/LIVE, GitHub/connector, push/merge/land/deploy **not_run**. Native Windows, GraphQL, runtime action đổi môi trường, remote freshness và phần định danh sau process **not_measured/KHÔNG ĐO ĐƯỢC**. Không nâng những giới hạn đó thành pass, waiver hoặc land authorization.

Bước đọc lại artifact đầu tiên `python -B .review/finalize11.py` rc1/KeyError do label receipt `snapshot-end` ghi đè tệp snapshot cùng tên; không là lỗi sản phẩm/test. Đã tách label thành `preflight-end`, chạy lại snapshot cuối và finalizer. `artifact-correction11.json` giữ lỗi đã quan sát; kết quả đối chiếu cuối dưới đây dùng snapshot đúng cấu trúc.

## Read-only và bàn giao

`snapshot-start.json` / `snapshot-end.json` / `snapshot-comparison11.json` đối chiếu HEAD/tree, diff/index/status và path/size/SHA-256 của **16771 tệp** tracked/untracked/ignored ngoài `.review/`: **không có delta quan sát được**. Chỉ chứng minh hai mốc trong checkout được giao, không chứng minh chưa từng ghi rồi hoàn nguyên; repo nguồn ngoài checkout không thuộc quan sát. `.review/` là scratch ngoại lệ user cấp. Không gọi subagent, mạng, đăng GitHub hoặc đẩy Git.

`evidence-manifest11.json` neo path/size/SHA-256 của artifact ổn định sau khi mọi phép đo kết thúc; manifest không tự băm chính nó. Verdict **approve nội dung trên exact SHA**; đề xuất giữ D02 và F10/D05 làm nợ P3 như bảng. Gate-registry/A9, completion receipt A13 và lượt connector12/12 là công việc của vai được giao tiếp theo, không được tính đã hoàn tất bởi lượt offline này.
