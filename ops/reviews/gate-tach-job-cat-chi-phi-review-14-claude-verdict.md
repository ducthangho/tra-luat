verdict: changes_requested
reviewed_sha: 86b0feb1959c78affbe8cd59fb2f47df36437e82

# VERDICT-ADDENDUM — làm rõ 6 ca acceptance-r14 (cùng review 14, cùng SHA, không phải lượt mới)

- Trạng thái: **HOÀN TẤT** — hai dòng đầu là canonical và ĐÃ CHỐT (`changes_requested`); chi tiết ở
  «KẾT LUẬN HIỆU LỰC» cuối tệp. (Dòng này ban đầu là placeholder «ĐANG LÀM RÕ» mang verdict gốc
  `approve`, đổi đúng MỘT lần khi chốt theo đúng quy trình; nhật ký dưới giữ nguyên, không xoá.)
- Cùng reviewer session review14 (5fe3ff30-a9cf-47f0-b745-43216fa3feef), độc lập executor; deadline
  tuyệt đối 2026-09-13T19:50:04Z không reset.
- VERDICT.md gốc GIỮ BẤT BIẾN — sha256 tự đo ghi ở nhật ký bên dưới, phải khớp neo
  `1bb273cd37b67f79e0359f1777d60712c3e0fc2030f5ea189018bd687e5e7d88`.
- Phạm vi: đúng 6 đầu vào của `acceptance-r14.json` (đọc bytes, tự tái lập trên clone) + đối chiếu
  R13 ADDENDUM và bảng săn review14; KHÔNG săn 6 hướng mới; không chạy shell/fixture nội dung; chỉ
  parser offline. Không mạng/CI/`--chay`/commit.
- Ghi chú bối cảnh: master ngoài sandbox đã dịch `9938e7c` → `c16bd329` (chỉ hai tệp packet_loop);
  product HEAD/base/spec/lease KHÔNG đổi ⇒ không đổi candidate của static review; tích hợp mới là
  `not_measured` — không dùng làm căn cứ approve/đỏ cho consumer.

## Nhật ký phép đo (append-only)
### A. Neo bất biến + tái lập 6 ca trên CLONE của reviewer
- `VERDICT.md` gốc tự đo sha256 = `1bb273cd37b67f79e0359f1777d60712c3e0fc2030f5ea189018bd687e5e7d88` — **KHỚP neo, BẤT BIẾN**.
- `acceptance-r14.json` (bytes) sha256 = `13ace694bab6944e2268e45fe85fe1a46e3ed24e8c93d8d9a9882fd13b1bc8f5`; 6 ca.
- Tái lập (`scratch/adden_a_6ca.py` — import module từ clone, carrier đúng mô tả: run opaque giữa bước pin/probe đúng và registry `--chay` đúng trong MỘT job `gate`):
```
'echo hi ||'            -> errors=0 checks=3 parser=('KHONG', None, False, 0, False) | khop-executor=True
'echo hi |'             -> errors=0 checks=3 parser=('KHONG', None, False, 0, False) | khop-executor=True
'echo hi ;;;'           -> errors=0 checks=3 parser=('KHONG', None, False, 0, False) | khop-executor=True
'echo hi && || echo hi' -> errors=0 checks=3 parser=('KHONG', None, False, 0, False) | khop-executor=True
'echo hi >'             -> errors=0 checks=3 parser=('KHONG', None, False, 0, False) | khop-executor=True
'V=${x'                 -> errors=0 checks=3 parser=('KHONG', None, False, 0, False) | khop-executor=True
```
⇒ Lời khai executor ĐÚNG từng ca: consumer CHẤP NHẬN cả 6 (errors=[]), lexer cấp chứng chỉ `KHONG`
("phân tích được, không liên quan") cho cả 6 chuỗi.

### B. Đối chiếu tiền lệ — R13 H4 đo GÌ, trên CARRIER nào (đọc `prior-review-13-original.md` H4)
R13 H4 kết luận `;;`/subshell/redirect/`&>` ⇒ KPT — nhưng các probe H4 đều mang tiền tố `pin`
(carrier CÀI ĐẶT: `pin && #cmt\nprobe`, `pin &&\n<EOF>`…): KPT khi ấy đến từ cờ `bad`/`after` trên lệnh
LIÊN QUAN. Carrier OPAQUE cho các cấu trúc này CHƯA TỪNG được đo ở R7–R13 lẫn bảng săn R14 của tôi
(H8 của tôi đo need-`&&` trên carrier CÀI; `||`/`|`/`;;;`/`>`-EOF/`${` opaque thì không). Hai ca opaque
DUY NHẤT từng được phân xử là `echo \$(pip…)` và `V=$(echo hi # )` — R13-ADDENDUM tuyên LỖI với căn cứ
«chuỗi không phải câu lệnh POSIX hợp lệ ⇒ nằm NGOÀI câu miền ⇒ fail-close đòi KPT; "ngoài miền không
được biến thành KHONG" (lease viec_dau_tien) bị vi phạm nguyên văn» — và r14 đã VÁ đúng theo phán quyết
ấy cho carrier opaque (`ngoac-tran-opaque`, `c0-*-tran` đều là `echo hi …` opaque, fixture đòi ĐỎ).
⇒ KHÔNG phải hồi quy r14 (đường emit/op/redirect/`${` không đổi trong diff r13→r14); là PHẦN CÒN LẠI
của đúng lớp mà addendum đã phân xử — sáu thành viên mới của lớp, chưa ai đo tới lượt này.

### B2. Phản chứng hồi quy — 6 ca trên BASE r13 `664aaf3` (`scratch/adden_b_base_6ca.py`)
```
BASE-r13: cả 6 ca -> errors=0, parser[0]=KHONG  (GIỐNG HỆT HEAD r14)
```
⇒ **ĐO ĐƯỢC, không phải suy từ diff:** r14 KHÔNG hồi quy — toleration này có sẵn từ ≤ r13, là phần
CHƯA ĐƯỢC PHÂN XỬ của cùng lớp lexical-boundary mà R13-ADDENDUM đã phân xử trên hai thành viên khác.

### C. Trả lời câu hỏi — consumer CÓ được tha các cấu trúc này thành KHONG chỉ vì invocation opaque không? **KHÔNG.**
Cả 6 chuỗi KHÔNG phải câu lệnh POSIX hợp lệ (XCU, dẫn đúng mục):
1. `echo hi ||` — 2.9.3 Lists: sau `OR_IF` phải có (linebreak +) pipeline; EOF ⇒ câu chưa hoàn chỉnh.
2. `echo hi |` — 2.9.2 Pipelines: sau `|` phải có command; EOF ⇒ không hợp lệ.
3. `echo hi ;;;` — `;;` (DSEMI) chỉ hợp lệ làm terminator case-item TRONG `case`; ngoài `case` ⇒ syntax
   error; `;;;` còn thừa một `;` không có lệnh.
4. `echo hi && || echo hi` — sau `AND_IF` phải là pipeline; `||` không phải pipeline ⇒ lệnh RỖNG giữa hai
   toán tử ⇒ không hợp lệ.
5. `echo hi >` — 2.7 Redirection: `[n]>word` — toán tử redirect phải có WORD đích; EOF ⇒ syntax error.
6. `V=${x` — 2.6.2 Parameter Expansion: `${` phải có `}` khớp (đếm mức ngoặc); thiếu ⇒ không hợp lệ.
Miền công khai (SPEC «Miền công khai» + docstring dòng 423: «lệnh đơn argv tĩnh, quoting POSIX hợp lệ,
nối dòng, newline/;/&&») KHÔNG chứa chuỗi nào trong 6; không câu công bố nào cấp quyền «opaque thì miễn
cú pháp» — (3) docstring chỉ đặt opaque «ngoài phạm vi CÀI ĐẶT», không ngoài phạm vi CÚ PHÁP. Tiền lệ
R13-ADDENDUM áp thẳng: `KHONG` nghĩa là «phân tích ĐƯỢC và không liên quan» — một chuỗi không phân tích
được theo ngữ nghĩa đã công bố thì chứng chỉ ấy là chứng chỉ SAI, bất kể bước có liên quan hay không;
luật lease «ngoài miền không được biến thành KHONG» và chốt chủ kho «ngoài miền phải fail-close» bị vi
phạm nguyên văn — y hệt hai ca `\$(`/`# )` đã bị tuyên LỖI, và r14 đã nhận phán quyết ấy khi vá
`ngoac-tran-opaque` (carrier opaque, fixture đòi ĐỎ). Không viện runtime (đã RÚT từ R13-ADDENDUM), không
đổi câu hợp đồng. **Ranh giới KHÔNG đổi bởi phán quyết này:** thân script/`python -c`/stdin, DỮ LIỆU
trong nháy và heredoc-body vẫn ngoài phạm vi soi cú pháp (đối chứng dương mục D giữ nguyên màu toàn bộ);
thứ bị soi là VĂN BẢN `run:` trực tiếp trong YAML — đúng mặt phẳng mà 6 ca nằm trên đó.
⇒ **VI PHẠM — LỖI sản phẩm, lớp 2.**

### D. DRESS-REHEARSAL hướng sửa CẤP LỚP (`scratch/adden_d_proto.py` → `scratch/mutants/proto_opgrammar_…py`; KHÔNG phải patch-as-hint)
Ba luật LỚP (không ngoại lệ từng chuỗi): **(i)** danh sách toán tử ĐÓNG `{;, &, &&, |, ||}` — run toán tử
ngoài danh sách ⇒ ValueError; toán hạng đủ hai phía: mở rộng `need` cho `&&/||/|` và mở rộng «thiếu lệnh»
cho MỌI toán tử thật (giữ miễn cho `\n` — linebreak sau toán tử vẫn hợp lệ POSIX); **(ii)** toán tử
redirect ngoài nháy phải có ĐÍCH trước điểm kết lệnh (check-lookahead, không đổi cách tiêu thụ — giữ
nguyên đường `2>&1` hiện hành); **(iii)** `${` ngoài nháy phải đóng `}` (đếm mức ngoặc). Prototype
**+14 dòng lexer**, đo TRỌN:
```
suite:  rc=0 · ĐĂNG KÝ 21/21 · RUFF CI 3/3 · PHẢN CHỨNG 245/245 · TỔNG ĐẠT · 0 fixture đổi màu
6 ca:   đều KPT + consumer 2-lỗi — trace TỪNG LUẬT: 'thiếu vế phải' (||, |) · 'toán tử ngoài miền' (;;;)
        · 'thiếu lệnh' (&& ||) · 'redirect thiếu đích' (>) · 'parameter expansion chưa đóng' (${x)
đối chứng dương (9): echo a || echo b · a | wc -l · a > f · a >> f · ${X} · a & · 2>/dev/null ·
        printf x > ruff.toml · pin &&\n probe — HEAD=proto TỪNG CA, 0 đổi màu
```
⇒ Nguy cơ hồi quy là SỐ ĐO: 0 fixture đổi màu, `ci.yml` thật vẫn 3/3 hợp đồng. Khả thi trong trần:
+14 dòng lexer + ~11 dòng fixture (6 âm theo đúng 6 ca + ~5 dương) + 1-2 dòng docstring ⇒ ước
**774 + ~27-35 ≈ 801-809 ≤ 1000**, vẫn ĐÚNG 2 path (chỉ tệp consumer đổi). Ghi chú cho executor:
thông điệp `need` nên nói chung «thiếu vế phải toán tử» thay vì «&&» (prototype giữ chuỗi cũ — thẩm mỹ,
không đổi hành vi); biến thể `${` chưa đóng NẰM TRONG nháy kép đã đóng (`echo "${x"` → KHONG ở cả HEAD
lẫn prototype — đo mục D2) là thành viên SÓT của lớp trong ngữ cảnh nháy — luật (iii) cần áp cả nhánh
quote `"` khi vá thật; `echo "${x""` thì cả hai bản đã KPT sẵn nhờ luật nháy chưa đóng.

## Finding (hiệu chỉnh — cộng vào verdict gốc)

### ruff-khuon-chua-chung-minh-provisioning  [P2]  (sub-class MỚI: opaque-structural-grammar — GIỮ stable slug, không reset lịch sử)  Sáu cấu trúc POSIX-invalid trong bước opaque được cấp chứng chỉ KHONG
TỆP/DÒNG: `.claude/dev/ci_dang_ky_test.py:227-231` (nhánh separator nhận MỌI run `;&|` làm «toán tử» không
có danh sách đóng), `:184` («thiếu lệnh» chỉ phủ `;`/`&&`), `:185` (`need` chỉ theo dõi `&&` — `||`/`|`
cụt vế phải lọt), `:242-244` (`<`/`>` chỉ đặt cờ `bad`, không đòi đích), (không dòng nào theo dõi `${`
chưa đóng — thiếu vắng, không phải sai dòng).
VẤN ĐỀ + COUNTEREXAMPLE (đều đã CHẠY, mục A/B/B2): 6 chuỗi POSIX-invalid (`echo hi ||` · `echo hi |` ·
`echo hi ;;;` · `echo hi && || echo hi` · `echo hi >` · `V=${x`) đặt làm bước opaque giữa pin/probe đúng
và registry đúng ⇒ `loi_ruff_ci` trả `errors=[]`, lexer cấp `KHONG` — chứng chỉ «phân tích được, không
liên quan» cho chuỗi không phân tích được. Cùng LỚP với sub-class lexical-boundary (R13-ADDENDUM): quyết
định nhận dựa trên phép đọc văn bản KHÔNG trùng ngữ nghĩa công bố; khác chỗ: lỗ nằm ở tầng TOÁN
TỬ/CẤU TRÚC thay vì bảng chữ cái/comment/ngoặc. Không phải hồi quy r14 (B2: base r13 y hệt).
HƯỚNG SỬA CẤP LỚP: ba luật (i)/(ii)/(iii) ở mục D — đóng DANH SÁCH toán tử, đóng TOÁN HẠNG, đóng ĐÍCH
redirect, đóng `}` của `${` — kèm mở rộng luật (iii) sang ngữ cảnh nháy kép; SỬA docstring thêm một câu
công bố («toán tử ngoài {; & && | ||}, toán tử cụt vế, redirect thiếu đích, `${` chưa đóng bị từ chối»).
FIXTURE/MUTANT KHOÁ: 6 fixture âm đúng 6 ca + ~5 fixture dương (`a || b` · `a > f` · `${X}` · `a &` ·
`2>&1` đã có `nguyen-nhan-lexer`); MỖI luật một mutant riêng — gỡ danh-sách-đóng ⇒ ca `;;;` LỌT; gỡ
need-mở-rộng ⇒ `||`/`|` LỌT; gỡ «thiếu lệnh»-mở-rộng ⇒ `&& ||` LỌT; gỡ redirect-đích ⇒ `>` LỌT; gỡ
`${`-đóng ⇒ `V=${x` LỌT. Kèm đột biến NỚI danh sách cho phép (thêm `;;` vào tuple) phải làm ca `;;;` ĐỎ
— và nhớ bài học H6 của verdict gốc: fixture phải lấy cả phần tử BIÊN của mỗi luật, đừng chỉ phần tử
giữa (ví dụ `|||` cho op-list, `a > | b` cho redirect-đích).
NGUY CƠ HỒI QUY: **ĐÃ ĐO** (mục D): 245/245 nguyên vẹn, ci.yml thật 3/3, 9 đối chứng dương giữ màu.
Dưới trần: ước 801-809/1000, đúng 2 path — KHÔNG cần nới trần hay mở path.
ĐÃ THỬ VÁ: prototype trong `scratch/mutants/` của reviewer (KHÔNG phải patch-as-hint — tệp thuộc
authority/gate, `§8` loại trừ cho sensitive; executor tự dẫn xuất).
ĐÃ THỬ NGHIỆM: toàn bộ mục A/B/B2/D/D2. ĐỘ TIN: cao — mọi mệnh đề chấp nhận/từ chối đo trực tiếp trên
hàm sản phẩm tại exact SHA ở CẢ HEAD lẫn base lẫn prototype; phần POSIX dẫn chuẩn XCU 2.6.2/2.7/2.9.2/2.9.3.

## Bảng câu cũ → kết luận hiệu lực (VERDICT.md gốc BẤT BIẾN — liệt kê, không xoá)
| vị trí trong VERDICT.md gốc (`1bb273cd…`) | kết luận cũ | kết luận hiệu lực |
|---|---|---|
| Kết luận lớp 2 «không phản ví dụ lớp nào còn dựng được» | approve | **changes_requested** — 6 phản ví dụ opaque-structural dựng được (executor tự nộp, reviewer tái lập cả trên HEAD lẫn base); câu cũ là lời khai RỘNG HƠN phép đo của chính bảng săn R14 (H8 chỉ đo need-`&&` carrier cài; không đo `||`/`|`/`;;;`/`>`-EOF/`${` opaque) — tự phê theo đúng doctrine kho |
| «Kết luận theo LỚP» hàng 2 | approve | **changes_requested** (P2 mới ở trên) |
| «KẾT LUẬN CUỐI» verdict approve · P1=0 · P2=0 · P3=1 | approve · 0/0/1 | **changes_requested · 0/1/1** |
| Lớp 1 approve (H1/H2) | approve | **GIỮ NGUYÊN** — 6 ca không đụng nhận dạng installer/prefix; không ca nào đúc GHIM/probe/registry sai |
| Lớp 3 approve + P3 `ruff-fixture-thieu-rang-chot-moi`/bien-nguong-C0 | approve, P3 giữ slug R11 | **GIỮ NGUYÊN** — fixture khoá 6 ca đi KÈM bản vá lớp 2 (đúng khuôn R13-ADDENDUM); P3 giữ nguyên slug/ánh xạ R11, không reset lịch sử vì subtype mới |
| Bảng săn 8 hướng + mọi phép đo V1-V5/H1-H8 | như gốc | **GIỮ NGUYÊN giá trị đo** — chỉ nhãn kết luận lớp 2 bị thay |

## KẾT LUẬN HIỆU LỰC (chốt — thay placeholder đầu tệp; hai dòng đầu tệp là canonical)
- verdict hiệu lực: **changes_requested** · reviewed_sha `86b0feb1959c78affbe8cd59fb2f47df36437e82`
  (tree `8c16548e844c4adfdf2134535e23efee400ba8fe`).
- Lớp: 1 **approve** · 2 **changes_requested** · 3 **approve**. Findings hiệu lực: **P1=0 · P2=1 · P3=1**
  (P2 = `ruff-khuon-chua-chung-minh-provisioning`/opaque-structural-grammar — mục Finding trên;
  P3 = `ruff-fixture-thieu-rang-chot-moi`/bien-nguong-C0 — nguyên văn trong VERDICT.md gốc, slug R11).
- VERDICT.md gốc giữ nguyên byte (`1bb273cd…`); approve trong đó là LỊCH SỬ đã bị addendum này thay hiệu
  lực. Hai bản đăng nguyên văn cùng nhau.
- A1/A5/CI/A2-conclusions/A6-readback/A9: vẫn not_run/KHÔNG ĐO ĐƯỢC theo chỉ thị — không đổi. Master-dịch
  `c16bd329`: not_measured, không phải căn cứ.
- Hiện vật addendum: `scratch/adden_a_6ca.py` · `scratch/adden_b_base_6ca.py` · `scratch/adden_d_proto.py`
  · `scratch/mutants/base_r13_664aaf3_ci_dang_ky_test.py` · `scratch/mutants/proto_opgrammar_ci_dang_ky_test.py`.
- Bất biến cuối lượt addendum (ĐO SAU khi viết xong thân — ghi ở dòng dưới cùng): clone HEAD/tree/porcelain.
- Identity: provider anthropic_claude (alias claude) · model claude-fable-5 · effort max ·
  execution_surface claude_code · transport machine/local — validator so `modelUsage` thô.
- ĐO CUỐI LƯỢT: clone HEAD 86b0feb1959c78affbe8cd59fb2f47df36437e82 · tree 8c16548e844c4adfdf2134535e23efee400ba8fe · porcelain RỖNG (0 dòng) — KHỚP, không đổi; VERDICT.md gốc đo lại sha256 = 1bb273cd37b67f79e0359f1777d60712c3e0fc2030f5ea189018bd687e5e7d88 — BẤT BIẾN, khớp neo.

### D2 (tái bút — gắn nhãn cho phép đo đã dẫn ở mục D, output thật; append-only nên nằm cuối)
```
'echo "${x}"'  | HEAD: KHONG                 | proto: KHONG                  (đóng ngoặc — tha, GIỮ)
'echo "${x""'  | HEAD: KHONG_PHAN_TICH_DUOC  | proto: KHONG_PHAN_TICH_DUOC   (KPT sẵn nhờ luật nháy chưa đóng)
'echo "${x"'   | HEAD: KHONG                 | proto: KHONG                  (thành viên SÓT trong ngữ cảnh nháy kép — nêu ở Finding, luật (iii) áp cả nhánh quote khi vá thật)
```
