verdict: changes_requested
reviewed_sha: 664aaf326f5b084cf51a5005c48a7dbb72699bd8

# VERDICT-ADDENDUM — làm rõ H3/H4 (cùng review 13, cùng SHA, không phải lượt mới)

- Trạng thái: **HOÀN TẤT** — hai dòng đầu là canonical và ĐÃ CHỐT (`changes_requested`); chi tiết ở
  «KẾT LUẬN HIỆU LỰC» cuối tệp. (Dòng này ban đầu là placeholder «ĐANG LÀM RÕ», cập nhật khi xong theo
  đúng quy trình; nhật ký dưới giữ nguyên, không xoá.)
- VERDICT.md gốc GIỮ BẤT BIẾN, tự đo lại sha256 = `31fd353c4dca35f1a71b64609830ab192e901f3741d59f9f953374fafe5e7aef`
  — khớp neo trong yêu cầu. Approve của lượt gốc được giữ làm LỊCH SỬ; tệp này là bản làm rõ có thẩm quyền
  thay kết luận HIỆU LỰC, đăng kèm nhau nguyên văn.
- `SPEC-CANONICAL-r23.md` tự đo sha256 = `7089ad0d7c4322ffe5677f100cd31f44115fb15af1f7efe4087b7b267e7de482`
  — khớp `spec_hash` lease r23 (xác nhận lại kết luận CRLF-artefact của lượt gốc bằng bản bytes chuẩn).
- Phạm vi: đúng 3 đầu vào của `acceptance-r13.json` + biến thể đo thêm cùng lớp; không săn hướng mới;
  không thực thi shell/install; chỉ parser offline trên clone của reviewer.

## Nhật ký phép đo (append-only)

### A. Tái lập 3 ca `acceptance-r13.json` trên CLONE của reviewer (phạm vi B — không chạy script executor)
Lệnh: `scratch/addendum_probe.py` (đọc `acceptance_r13.py` để lấy NGUYÊN VĂN 3 đầu vào; import module từ
clone; `yaml.safe_dump` → `loi_ruff_ci`). Output:
```
H3-CR-token                        errors=[] checks=3
H4-escaped-dollar-parenthesis      errors=[] checks=3
H4-comment-in-substitution         errors=[] checks=3
```
⇒ **KHỚP acceptance-r13.json từng ca**: consumer CHẤP NHẬN cả ba (rejected_by_consumer=false).

### B. Biến thể CÙNG LỚP — đo thêm để biết độ rộng lỗ (cùng script)
```
CR-trong-probe-sau-pin-dung   (probe = "ruff\r--version")            errors=[] checks=3
CR-cuoi-token-pin             (pin  = "…ruff==0.15.15\r\n…")         errors=[] checks=3
CR-lam-tach-python-m-pip      (install = "python\r-m\rpip install …") errors=[] checks=3
```
⇒ Lỗ CR phủ CẢ BA vai chứng chỉ: prefix installer, token pin, và probe — không chỉ ca argv[0] của executor.

### C. Đo trên `ci.yml` THẬT (định giá rủi ro hồi quy cho hướng sửa)
```
byte \r trong ci.yml: 0 · run bodies: 51 · ký tự C0 (ngoài \n\t) trong bodies: 0
bodies chứa '$(': 2 — không body nào có '#' sau '$(' cùng dòng
bodies còn '(' ngoài dạng '$(': 5 (toàn bộ nằm trong nháy hoặc dạng đã xử lý — xem D)
```

### D. DRESS-REHEARSAL hướng sửa (prototype trong `scratch/mutants/`, KHÔNG phải patch-as-hint)
`scratch/addendum_fixproto.py` dựng 2 prototype trên BẢN SAO (ROOT ghim clone) và đo TRỌN:
| prototype | suite | ci.yml thật | 6 phản ví dụ (A+B) |
|---|---|---|---|
| mH = chặn C0 (ngoài `\n\t`) trong `_dong_logic` + nhận `#`-comment trong `_cuoi_thay_lenh` | **rc=0 · 214/214 · TỔNG ĐẠT** | **0 lỗi** | đóng **5/6** (còn `\$(`) |
| mG = mH + `(`/`)` trần ngoài nháy ⇒ ValueError | **rc=0 · 214/214 · TỔNG ĐẠT** | **0 lỗi** | đóng **6/6** |
⇒ Rủi ro hồi quy của hướng sửa là SỐ ĐO, không phải ước: 0 fixture đổi màu, workflow thật 0 lỗi
(5 body chứa `(` đều trong nháy/`$(`-dạng nên luật ngoặc-trần không bắn oan).

## Trả lời câu 1 — miền công bố có chứa ba chuỗi đó không? **KHÔNG.**
Hai văn bản công bố (SPEC-CANONICAL-r23 «Miền công khai» + docstring `loi_ruff_ci`): lệnh đơn **đối số
tĩnh**, **quoting POSIX hợp lệ**, ngăn bằng **newline/`;`/`&&`**, khớp **grammar invocation công bố**;
«mọi lệnh khác ngoài grammar bị từ chối»; «Không kiểm env hoặc mô phỏng runtime».
Ngữ nghĩa token POSIX (XCU 2.2 Quoting · 2.3 Token Recognition · 2.6.3 Command Substitution): dấu tách
TRƯỜNG là `<blank>` không nháy = {space, tab}; `<newline>` là dấu ngăn LỆNH; **CR không phải blank, không
phải toán tử** — nó là ký tự thường nằm TRONG từ.
1. `pip\rinstall ruff==0.15.15` ⇒ argv POSIX = [`pip\rinstall`, `ruff==0.15.15`]: argv[0] không khớp
   prefix nào của grammar công bố, không opaque, không assignment ⇒ luật đã công bố («ngoài whitelist
   không được suy KHONG» + `viec_dau_tien` lease: «ngoài miền không được biến thành KHONG») đòi
   **KHONG_PHAN_TICH_DUOC**. Thực thi: `shlex.split` (bảng trắng `" \t\r\n"` ⊋ POSIX blank, dòng 177)
   chế ra argv `["pip","install","ruff==0.15.15"]` và cấp **GHIM** — chứng chỉ mạnh nhất được cấp từ một
   argv mà ngữ nghĩa công bố KHÔNG sinh ra. Đo B cho thấy cùng cơ chế cấp cả PROBE (`ruff\r--version`)
   lẫn pin-token (`ruff==0.15.15\r`). **Ngoài miền + không bị từ chối = fail-close bị vi phạm theo chiều
   XẤU NHẤT (chiều NHẬN).**
2. `echo \$(pip install ruff)` ⇒ sau quote-removal của `\$`, `(` không nháy là ký tự tạo token riêng và
   mở compound — không được đứng sau WORD trong lệnh đơn (XCU 2.3/2.9): chuỗi **không phải câu lệnh POSIX
   hợp lệ**. 3. `V=$(echo hi # )` ⇒ trong `$()`, `)` đóng phải tìm bằng cách PARSE nội dung (XCU 2.6.3);
   `#` mở comment tới newline nuốt mất `)` ⇒ substitution **không đóng** ⇒ không phải câu lệnh hợp lệ.
   Cả hai nằm NGOÀI câu miền «quoting POSIX hợp lệ … ngăn bằng newline/;/&&» ⇒ fail-close đòi KPT; thực
   thi trả **KHONG** (lexer `_dong_logic`/`_cuoi_thay_lenh` nhận một SIÊU TẬP của POSIX tại `(`-trần
   (dòng 232 chỉ đặt cờ `bad`) và tại `#`-trong-`$()` (dòng 148-159 không biết comment)). Khác ca 1: hai ca
   này KHÔNG đúc ra chứng chỉ (bước được tha là bước trơ), nhưng câu lease «ngoài miền không được biến
   thành KHONG» bị vi phạm theo đúng nguyên văn.
**Về lập luận runtime của chính tôi ở lượt gốc:** «parser nhận sai nhưng shell sẽ chết ồn dưới `-e`» là
lập luận KHÔNG HỢP LỆ cho câu hỏi chấp nhận của consumer — nó bảo vệ một cổng TĨNH bằng đúng thứ tài
nguyên mà hợp đồng của cổng từ bỏ («Không kiểm env hoặc mô phỏng runtime») và chủ kho đã loại khỏi phạm
vi; nó cũng ngược tiền lệ R9→R11 (finding «lexer làm hỏng argv trước khi vị từ chạy» được tính lỗi sản
phẩm mà không cần trình diễn runtime). Tôi RÚT lập luận đó cho mục đích chấp nhận; nó chỉ còn giá trị
định MỨC (P2 thay vì P1 — chưa ai trình diễn green-gate-với-ruff-sai đầu-cuối; ca R11 CÓ trình diễn
runtime bypass cũng chỉ P2). Ghi thêm một sự thật đo được đóng nốt đường lùi «thực tế không xảy ra»:
scalar YAML nháy kép `"pip\rinstall …"` KHÔNG chứa byte CR nào trong tệp — CR chỉ hiện ra sau
`yaml.safe_load`, nên cổng EOL (§9) lẫn checkout ép LF đều MÙ với nó (đo A: round-trip safe_dump giữ nguyên).

## Trả lời câu 2 — fail-close CHƯA ĐẠT ⇒ hạ lớp 2 và verdict hiệu lực
- **Lớp 2 (lexer/composition/order/shell): changes_requested** (thay approve của lượt gốc).
- **Lớp 1: approve** (không đổi — H1/H2 đo đúng, không liên quan tầng token). **Lớp 3: approve** (không
  đổi — khuyết tật nằm ở lexer lớp 2; fixture khoá đi KÈM bản vá lớp 2).
- **Verdict HIỆU LỰC: changes_requested** («approve cuối chỉ khi cả ba lớp approve»).
- Số finding hiệu lực: **P1=0 · P2=1 · P3=1** (P3 `ruff-ham-chet-khong-caller` của lượt gốc giữ nguyên).

### ruff-khuon-chua-chung-minh-provisioning  [P2]  (sub-class MỚI: lexical-boundary — GIỮ stable slug, không reset lịch sử)
TỆP/DÒNG: `.claude/dev/ci_dang_ky_test.py:177` (`shlex.split` — bảng trắng `" \t\r\n"` rộng hơn POSIX
blank ⇒ CR thành dấu tách từ), `:232` (`(`/`)` trần chỉ đặt cờ `bad`, không fail-close), `:148-159`
(`_cuoi_thay_lenh` không nhận `#`-comment khi dò `)`), docstring `:425` («quoting POSIX hợp lệ» — lời
công bố là ranh NGOÀI mà lexer đang nhận một siêu tập).
VẤN ĐỀ + COUNTEREXAMPLE (đều đã CHẠY, mục A/B): 6 chuỗi ngoài miền công bố được chấp nhận, trong đó 4 ca
CR đúc chứng chỉ GHIM/probe/prefix từ argv phi-POSIX (`errors=[]` toàn phần); 2 ca POSIX-invalid được tha
thành KHONG. Cùng LỚP với hai sub-class trước của slug (R10 khuôn-chuỗi, R11 shell-selector): quyết định
nhận/từ chối dựa trên một phép đọc VĂN BẢN không trùng với ngữ nghĩa đã công bố cho chính văn bản ấy.
HƯỚNG SỬA CẤP LỚP (mô tả bằng lời — KHÔNG đính hunk: tệp thuộc authority/gate, `§8` loại patch-as-hint
cho sensitive; prototype đo được giữ trong `scratch/` của reviewer làm bằng chứng khả thi):
1. Đóng BẢNG CHỮ CÁI token về miền công bố: trong vòng quét `_dong_logic`, gặp ký tự `ord(c) < 32` ngoài
   `\n`/`\t` (CR, FF, VT, NUL…) ⇒ `ValueError` ⇒ KPT. Thân heredoc không bị đụng (được tiêu thụ ở nhánh
   riêng — vẫn là dữ liệu).
2. `_cuoi_thay_lenh` nhận `#`-comment (ngoài nháy, sau blank/`(`/đầu): nhảy tới newline; `)` bị comment
   nuốt ⇒ chốt «command substitution chưa đóng» SẴN CÓ tự bắn.
3. `(`/`)` trần ngoài nháy và ngoài nhánh `$(` ⇒ `ValueError` (mG); HOẶC nếu chủ kho chọn giữ khoan dung
   cho lệnh opaque thì SỬA CÂU CÔNG BỐ cho khớp mã («lexer nhận siêu tập POSIX trên lệnh không liên
   quan») — chọn MỘT, không để câu rộng hơn mã. Khuyến nghị mG: đã đo 0 tác động (D).
FIXTURE/MUTANT KHOÁ (thêm vào `_FX`/`_them`, ~6-12 dòng, dư trần A8 747→≤1000): 6 fixture kỳ vọng ≥1 đúng
theo 6 phản ví dụ A/B; ba mutant riêng ba cửa — gỡ luật C0 ⇒ 4 ca CR LỌT + main rc=1; gỡ `#`-handling ⇒
ca comment LỌT; gỡ luật ngoặc ⇒ ca `\$(` LỌT (mỗi cửa một chốt riêng, đúng doctrine).
NGUY CƠ HỒI QUY: **ĐÃ ĐO** (mục D): suite 214/214 nguyên vẹn, `ci.yml` thật 0 lỗi ở cả mH lẫn mG. Biên
cần chủ kho quyết: C0 trong NHÁY là dữ liệu của lệnh opaque — luật «C0 mọi nơi» chặn oan dạng ấy
(fail-close, hiện 0 ca thật); muốn hẹp hơn thì «C0 ngoài nháy» + một ca riêng cho CR-trong-nháy ở lệnh
liên quan (hiện đã KHONG_GHIM ⇒ đỏ sẵn).
ĐỘ TIN: cao — mọi mệnh đề chấp nhận/từ chối đo trực tiếp trên hàm sản phẩm tại exact SHA; phần POSIX dẫn
chuẩn (XCU 2.2/2.3/2.6.3), không suy từ chạy shell nào.

## Trả lời câu 3 — không săn hướng mới
Đây là ĐÍNH CHÍNH/phân loại lại H3+H4 của chính review 13. Các kết luận KHÁC trong H3/H4 đứng nguyên vì
chúng là ca TỪ CHỐI đúng (fail-close): `\f`/`\v`-trong-token ⇒ KHONG_GHIM/KPT (đỏ), `&&`-vắt-dòng nhận
đúng POSIX, `&&`-EOF/`;;`/subshell/redirect/`&>` ⇒ KPT. Bảng săn 8 hướng của lượt gốc giữ nguyên giá trị
đo; CHỈ nhãn kết luận của H3 («KHÔNG PHẢI LỖI SẢN PHẨM») và của hai ca H4 (`escape-dollar-paren`,
`comment-trong-thay-lenh`: «KHÔNG PHẢI LỖI») bị THAY bằng LỖI — gộp về một finding P2 ở trên.

## Dấu vết thay đổi kết luận (bản gốc BẤT BIẾN — liệt kê câu bị thay, không xoá)
| vị trí trong VERDICT.md gốc (`31fd353c…`) | kết luận cũ | kết luận hiệu lực |
|---|---|---|
| H3 dòng kết luận | «KHÔNG PHẢI LỖI SẢN PHẨM … thoả rỗng» | LỖI — thuộc P2 lexical-boundary (4 ca CR) |
| H4 hai ca `escape-dollar-paren` · `comment-trong-thay-lenh` | «KHÔNG PHẢI LỖI … chết ồn» | LỖI — cùng P2 (tha ngoài-miền thành KHONG) |
| Kết luận lớp 2 | approve | **changes_requested** |
| TÓM TẮT «verdict: approve … P3=1» | approve · 0/0/1 | **changes_requested · 0/1/1** |
| Ghi chú H3 «nếu muốn khoá hẳn … ≤3 dòng» | tuỳ chọn | BẮT BUỘC (nâng thành finding; đã dress-rehearsal) |
Tự phê đúng doctrine kho: lượt gốc đã phạm «lời khai rộng hơn phép đo» — mượn trạng thái runtime chưa đo
(«mọi shell trong miền chạy -e») để bào chữa cho một cổng tĩnh; addendum này sửa bằng phép đo, giữ lịch sử.

## KẾT LUẬN HIỆU LỰC (chốt — thay placeholder đầu tệp; hai dòng đầu tệp là canonical)
- verdict hiệu lực: **changes_requested** · reviewed_sha `664aaf326f5b084cf51a5005c48a7dbb72699bd8`.
- Lớp: 1 **approve** · 2 **changes_requested** · 3 **approve**. Findings hiệu lực: **P1=0 · P2=1 · P3=1**
  (P2 = `ruff-khuon-chua-chung-minh-provisioning`/lexical-boundary; P3 = `ruff-ham-chet-khong-caller`).
- VERDICT.md gốc giữ nguyên byte (`31fd353c…`), approve trong đó là LỊCH SỬ đã bị addendum này thay hiệu lực.
- A1/A5/CI/A2-conclusion/A6-readback/A9: vẫn not_run/KHÔNG ĐO ĐƯỢC theo chỉ thị — không đổi.
- Hiện vật addendum: `scratch/addendum_probe.py` · `scratch/addendum_fixproto.py` ·
  `scratch/mutants/mH_c0_comment_ci_dang_ky_test.py` · `scratch/mutants/mG_c0_comment_paren_ci_dang_ky_test.py`.
- Bất biến cuối lượt addendum (ĐÃ ĐO sau khi viết xong thân tệp): clone HEAD `664aaf326f5b084cf51a5005c48a7dbb72699bd8`
  · tree `4fbf9f5b8385c946e39431bb3982d0b40c97f405` · porcelain rỗng (0 dòng) — KHỚP; `VERDICT.md` gốc đo lại
  sha256 = `31fd353c4dca35f1a71b64609830ab192e901f3741d59f9f953374fafe5e7aef` — BẤT BIẾN, khớp neo.
- Identity: provider anthropic_claude (alias claude) · model claude-fable-5 · effort max ·
  execution_surface claude_code · transport machine/local — validator so `modelUsage` thô.
