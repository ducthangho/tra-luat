verdict: approve
reviewed_sha: 86b0feb1959c78affbe8cd59fb2f47df36437e82

# VERDICT — packet #463, lượt review 14 (reviewer: Claude, độc lập)

- generation: 4, revision: 23
- lease: gate-tach-job-cat-chi-phi-exec-5-codex-20260914-r23
- tree kỳ vọng: 8c16548e844c4adfdf2134535e23efee400ba8fe
- base: bb7013c7669da19304a8769e5b25f8c1f8951e9c
- review_class/effective_review_class: sensitive
- reviewer identity: provider=anthropic_claude (alias claude), model=claude-fable-5, effort=max, execution_surface=claude_code, transport=machine/local
- A1/A5/CI: not_run (theo chủ kho) — KHÔNG khai passed
- Trạng thái: HOÀN TẤT — verdict hai dòng đầu là canonical, chốt tại mục "KẾT LUẬN CUỐI"
  (đầu lượt hai dòng ấy là placeholder changes_requested đúng quy trình; sửa MỘT lần khi đóng, không xoá nhật ký)

P1: 0
P2: 0
P3: 1 (`ruff-fixture-thieu-rang-chot-moi`/bien-nguong-C0 — không chặn)

## Nhật ký phép đo (append-only)

### B0. Neo & baseline (không tính N)
- Clone: HEAD `86b0feb1959c78affbe8cd59fb2f47df36437e82` · tree `8c16548e844c4adfdf2134535e23efee400ba8fe` · porcelain RỖNG — KHỚP prompt.
- A8: `git diff --numstat bb7013c..HEAD` = `648+126 = 774` additions, đúng **2** đường dẫn (`.claude/dev/ci_dang_ky_test.py` · `.github/workflows/ci.yml`) — khớp 774/1000, ≤ trần.
- Byte-identity workflow: blob `HEAD:.github/workflows/ci.yml` = blob `3bbc6b4:.github/workflows/ci.yml` = `cb025a5a704a8f73319fee4ddded0010678e8f02` — **BYTE-IDENTICAL** ✓.
- Registry suite (KHÔNG `--chay`), tự chạy `C:/Python313/python.exe -X utf8 -B .claude/dev/ci_dang_ky_test.py`: rc=0, `ĐĂNG KÝ 21/21 · LAUNCHER WINDOWS 4/4 · RUFF CI 3/3 · PHẢN CHỨNG 245/245 · TỔNG ĐẠT`.
  Diff với `r14-freeze-registry.txt`: chỉ lệch dòng chú thích `rc=0` đầu tệp freeze; `freeze ≡ sandbox-registry.txt` IDENTICAL. ⇒ lời khai 245/245 TỰ TÁI LẬP trên exact SHA.

### V. XÁC MINH VÁ R13 (không tính vào N hướng mới)
**V1 — 6 phản ví dụ addendum PHẢI ĐỎ tại consumer** (`scratch/v1_addendum_6ca.py`, import module từ clone, -B):
```
A1-cr-installer: errors=3 ĐỎ  · B1-cr-probe: errors=3 ĐỎ · B2-cr-pin: errors=3 ĐỎ
B3-cr-prefix:   errors=3 ĐỎ  · A2-escaped-dollar-paren: errors=2 ĐỎ · A3-comment-in-substitution: errors=2 ĐỎ
```
Cả 6 mang thông điệp `ngoài miền cú pháp: [gate/bước N]` — KPT đúng chiều fail-close, KHÔNG còn ca nào đúc GHIM
từ argv phi-POSIX hay được tha thành KHONG. **P2 lexical-boundary: ĐÃ VÁ THẬT (hành vi).**

**V2 — đối chứng dương + docstring:** fixture accept-side có mặt và XANH trong 245/245: `comment-dong-sau` ·
`hash-trong-tu` · `hash-sau-blank-escape` · `hash-sau-nhay` · `hash-sau-escape-noi-dong` · `ngoac-escape-opaque` ·
`c0-{0..3}-nhay` · `c0-{0..3}-heredoc` (C0 trong nháy/heredoc là DỮ LIỆU). Docstring `loi_ruff_ci` công bố đúng
hai câu mới (dòng 427-428: "Ngoặc trần, C0 ngoài nháy … dữ liệu nháy/heredoc giữ nguyên" · "Comment chỉ mở tại
đầu từ chưa quote/escape, kể cả trong $(...)"). KHÔNG thêm chốt env/runtime — đúng chỉ thị chủ kho.

**V3 — mutant ĐỘC LẬP tự dựng cho 5 cửa mới** (`scratch/v3_mutants.py`, bản sao riêng tên, ROOT ghim clone):
| mutant tự dựng | rc | tally | fixture LỌT | khớp mutation-r14.json? |
|---|---|---|---|---|
| m1 gỡ luật C0 trần | 1 | 237/245 | 4 cr-* + 4 c0-*-tran (8) | khớp `c0-plain` TỪNG TÊN |
| m2 gỡ luật C0-escape | 1 | 241/245 | c0-{0..3}-escape (4) | khớp `c0-escape` TỪNG TÊN |
| m3 gỡ `#`-handling trong `_cuoi_thay_lenh` | 1 | 242/245 | comment-nuot-ngoac · comment-dong-sau · hash-sau-blank-noi-dong | khớp `substitution-comment` TỪNG TÊN |
| m4 gỡ raise ngoặc trần | 1 | 243/245 | ngoac-sau-dollar-escape · ngoac-tran-opaque | khớp `bare-parenthesis` TỪNG TÊN |
| m5 hồi quy `not word` → `cur[-1].isspace()` | 1 | 244/245 | hash-sau-blank-escape-khong-che-cai | khớp `comment-token-boundary` TỪNG TÊN |
⇒ Mẫu 5/17 (đúng 5 cửa MỚI của r14) tự tái lập độc lập: semantic đổi (fixture flip), main rc=1, tập LỌT khớp
từng tên. 12 mutant còn lại: 5 đã được R13 tự dựng tái lập (mA..mE ↔ registry-poison, workflow-shell-default,
shell-before-body, outside-diagnostic, probe-order — mã cửa không đổi trong r14); 7 còn lại nhận ở mức lời khai
nhất quán + suite tự chạy khớp freeze.

**V4 — P3 `ruff-ham-chet-khong-caller`: ĐÃ VÁ THẬT.** Diff r13→r14 xoá đúng 4 helper: `_cham_ruff` ·
`_loai_mot_dong` · `_probe_sau_ghim` · `_la_registry`; grep cả tệp: 0 lần xuất hiện còn lại (không caller treo).
`_phan_loai_cai_ruff` (có 47 fixture caller `nhan-*`) GIỮ NGUYÊN — đúng ranh giới finding.

**V5 — Ruff F trên tệp consumer: rc=0 "All checks passed"** (khớp `r14-freeze-ruff.txt`) · **actionlint ci.yml:
rc=0** (khớp `r14-freeze-actionlint.txt`) — ci.yml byte-identical nên delta actionlint so 3bbc6b4 = 0 theo cấu trúc.

## BẢNG SĂN — 8 hướng MỚI độc lập (N=8; lớp 1: H1-H2 · lớp 2: H3-H5, H8 · lớp 3: H6-H7)
Không hướng nào trùng đầu vào R7–R13 (đối chiếu PRIOR_HUNT_INDEX: requirements/options · wrapper/prefix ·
CR/FF/VT · operators/continuation/`\$(`/comment-in-substitution · shell scope · registry conjunction (bước
cùng job LẪN `hai-job-chay-registry` đã thành fixture) · parity20 · harness trùng tên). Script: `scratch/hunt_h1_h8.py`,
`scratch/v3_mutants.py` (m6), `scratch/h6b_escape_nguong.py`.

### H1 [LỚP 1] — biên TRÊN của bảng chữ cái: ký tự ≥ 0x7F/DEL mà cổng C0 (`ord < 32`) không chạm
Giả thuyết: NBSP/U+2028/U+3000/ZWSP/DEL trong token installer không bị luật C0 bắt; nếu shlex tách khác POSIX
thì tái sinh đúng lỗ CR ở dải trên. Đo: `shlex.split("pip\xa0install") == ['pip\xa0install']` (MỘT từ, ĐỒNG
NHẤT POSIX — các ký tự này không phải blank POSIX và không nằm trong bảng trắng shlex ⇒ không có divergence
lớp lexical để khai thác). Consumer: `pip<NBSP>install`, `pip<DEL>install`, `pip<U+2028>install`,
`pip<U+3000>install`, `pip<ZWSP>install` + pin-có-NBSP-đuôi ⇒ **đều 3-lỗi ĐỎ** (unknown→KPT / KHONG_GHIM);
đối chứng space thật ⇒ 0-lỗi. **KHÔNG PHẢI LỖI** — fail-close đúng cả dải trên, không cần luật mới.

### H2 [LỚP 1] — biên HOA/thường của grammar invocation
`PIP install` · `pip INSTALL` · `Pip install` ⇒ **đều ĐỎ** (so sánh case-sensitive, đúng ngữ nghĩa POSIX:
tên lệnh khác byte là lệnh khác). `pip install RUFF==0.15.15` ⇒ **0-lỗi GHIM** — ĐÚNG CHỦ Ý: `_chuan_ten`
chuẩn hoá PEP503 (pip coi RUFF ≡ ruff, certificate vẫn thật), nhất quán fixture sẵn có `nhan-ten-hoa-thuong`
(`Ruff==0.15.15` → GHIM). **KHÔNG PHẢI LỖI.**

### H3 [LỚP 2] — comment TOP-LEVEL × vai chứng chỉ (fixtures r14 chỉ phủ phía `$()` + ca `;`)
`pin#x` giữa từ ⇒ token `ruff==0.15.15#x` → KHONG_GHIM ĐỎ (POSIX: `#` giữa từ là dữ liệu) · `install #ruff==…`
⇒ req bị comment nuốt → KPT ĐỎ · `pin # chú thích` ⇒ 0-lỗi GHIM (comment sau blank bị bỏ đúng) ·
`ruff --version#x` ⇒ probe KHÔNG được cấp → ĐỎ · `ruff --version # ok` ⇒ 0-lỗi. Cả 5 khớp POSIX từng ca —
biên `not word` đúng ở top-level cho CẢ pin lẫn probe. **KHÔNG PHẢI LỖI.**

### H4 [LỚP 2] — parity bắt cặp escape: `\$(` phải vẫn ACTIVE, đếm backslash lẻ/chẵn không được nhầm
`echo \$(pip install ruff)` (2 backslash ⇒ `$(` ACTIVE) → trace **"lệnh liên quan trong command substitution
ngoài miền"** ĐỎ · `\\$(` (3 ⇒ `$` literal + ngoặc trần) → **"ngoặc trần ngoài miền lệnh đơn"** ĐỎ · `\\$(`
(4 ⇒ ACTIVE) → "lệnh liên quan" ĐỎ · đối chứng `\$(` → "ngoặc trần" ĐỎ. Chẵn/lẻ đổi ĐÚNG nhánh chẩn đoán
từng bậc — bộ tiêu thụ escape theo CẶP, không đếm nhìn-lùi. **KHÔNG PHẢI LỖI.**

### H5 [LỚP 2] — biên grammar heredoc chưa đo (r14 chỉ thêm C0-trong-body)
`<<<` herestring → "heredoc ngoài miền" ĐỎ (POSIX không có `<<<` — từ chối đúng) · `<<A <<B` hai heredoc →
ĐỎ (fail-close có chủ đích, POSIX cho phép nhưng NGOÀI miền công bố — chiều CHẶN, hợp đồng đóng cho phép) ·
`<<-END` đóng bằng tab → **0-lỗi** (nhánh `tabs=True` chạy đúng, decoy `pip install ruff==0.15.14` trong body
là DỮ LIỆU) · `<<END` không quote + body TĨNH → **0-lỗi** (body không `$(`/backtick giữ nguyên là dữ liệu) ·
tag số `<<1AB` → ĐỎ. Cả accept-side lẫn reject-side đúng công bố. **KHÔNG PHẢI LỖI.**

### H6 [LỚP 3] — RĂNG của hai cổng C0 chỉ mọc ở NỬA DƯỚI dải: mutant thu hẹp ngưỡng SỐNG 245/245 — **LỖI (P3)**
Giả thuyết: fixture C0 chỉ mẫu {NUL 0x00, VT 0x0B, FF 0x0C, CR 0x0D} — toàn bộ < 0x0E — nên đột biến
`ord(c) < 32 → ord(c) < 14` không fixture nào phân biệt được. Đo (m6, `scratch/v3_mutants.py`):
**rc=0 · 245/245 · 0 LỌT — SỐNG SÓT**, trong khi KHÔNG tương đương: `echo hi\x0e|\x10|\x1f` ⇒ HEAD **2 lỗi**,
m6 **0 lỗi** (A/B `scratch/h6_ab_nguong.py`); 4 ký tự fixture đối chứng GIỐNG hệt hai bản. Cửa escape Y HỆT:
m7 (`ord(nxt) < 14`) cũng **SỐNG 245/245**, A/B `echo hi\<U+000E>` HEAD 2 ↔ m7 0 (`scratch/h6b_escape_nguong.py`).
Đối chiếu doctrine: giết "gỡ cả luật" (c0-plain/c0-escape ĐÃ chết) mà không giết "thu hẹp luật" đúng là ca
"đột biến nới danh sách cho phép phải làm ca đích ĐỎ — không có nó thì không biết ca đang đo danh sách hay đo
thứ khác". Mã sản phẩm ĐÚNG; lưới fixture hụt biên ⇒ P3 (chi tiết ở Finding).

### H7 [LỚP 3] — biên KIỂU của `if`: bool `true` và `null` (fixtures cũ chỉ đo chuỗi "false"/"0"/biểu thức)
`if: true` (bool YAML) trên bước cài → **3-lỗi ĐỎ** (mọi `if` hiện diện ⇒ bước thành KPT — nhất quán chính
sách đã chốt: consumer không định giá điều kiện, fail-close kể cả điều kiện luôn-đúng) · `if: null` → **0-lỗi**
(`_buoc_co_dieu_kien` neo `is not None`; GitHub chạy bước có `if:` rỗng như không điều kiện ⇒ chấp nhận là ĐÚNG
ngữ nghĩa nền) · `if: true` trên bước registry → ĐỎ (check 3). **KHÔNG PHẢI LỖI** — biên kiểu đã đo, hai phía
nhất quán semantics GH.

### H8 [LỚP 2] — bảo toàn `need`-&& xuyên dòng comment (composition mới; R13 chỉ đo `&&`-vắt-dòng trần)
`pin &&\n# note\nruff --version` → **0-lỗi** (POSIX cho linebreak+comment sau `&&`; GHIM+probe giữ nguyên) ·
`pin && # note` EOF → ĐỎ "thiếu vế phải" · `pin && # note\nruff --version` → 0-lỗi. Comment không nuốt nghĩa
vụ vế phải, cũng không chặn oan tổ hợp hợp lệ. **KHÔNG PHẢI LỖI.**

## ĐỐI CHIẾU LƯỢT TRƯỚC (R13 original + addendum — verdict hiệu lực changes_requested)
- `ruff-khuon-chua-chung-minh-provisioning` [P2, sub-class lexical-boundary]: **ĐÃ VÁ THẬT** — bằng chứng TỰ ĐO:
  (1) cả 6 phản ví dụ addendum ĐỎ tại consumer với reason KPT (V1); (2) ba cửa vá đúng đặc tả addendum: C0 ngoài
  nháy kể cả escape (hai luật riêng, dòng 193-194 + 198-199), `#`-comment theo đầu-từ-thật trong `_cuoi_thay_lenh`
  (dòng 159-162) VÀ trong `_dong_logic` (dòng 217 — `not word` thay `cur[-1].isspace()`), ngoặc trần fail-close
  (dòng 220-221); (3) MỖI cửa một mutant riêng có răng — m1..m5 tự dựng chết đúng tập fixture từng tên (V3);
  (4) accept-side không chặn oan: 11 fixture dương + H3/H4/H5/H8 của lượt này đều khớp POSIX. KHÔNG mượn runtime.
- `ruff-ham-chet-khong-caller` [P3]: **ĐÃ VÁ THẬT** — 4 helper đúng danh sách bị xoá; git grep toàn kho 0 tham
  chiếu còn lại; 16 hàm private còn lại đều có >=1 caller thật (V4); helper có fixture caller (`_phan_loai_cai_ruff`)
  giữ nguyên.

## BẢNG ĐO — mọi con số đã đo, kể cả cái khớp
| khẳng định | khai / hợp đồng | đo được | khớp? |
|---|---|---|---|
| Exact head | 86b0feb1959c78affbe8cd59fb2f47df36437e82 | rev-parse đầu VÀ cuối lượt khớp; porcelain 0 dòng cả hai lần | Có |
| Tree | 8c16548e844c4adfdf2134535e23efee400ba8fe | khớp (đo lại cuối lượt) | Có |
| Base | bb7013c7669da19304a8769e5b25f8c1f8951e9c | dùng đúng cho numstat | Có |
| A8 additions / path | 774 <= 1000, đúng 2 path | 648+126=774, đúng 2 path; delta r14 CHỈ tệp consumer (+51/−24) | Có |
| ci.yml byte-identical 3bbc6b4 | tuyên bố nhiệm vụ | blob `cb025a5a70…` ở CẢ HAI commit | Có |
| Registry suite (KHÔNG --chay) | 245/245, rc=0, TỔNG ĐẠT | tự chạy: 21/21 · 4/4 · 3/3 · 245/245 · TỔNG ĐẠT · rc=0 | Có |
| freeze ≡ sandbox ≡ tự chạy | executor khai bằng nhau | diff: freeze≡sandbox IDENTICAL; tự chạy ≡ freeze trừ dòng chú thích `rc=0` | Có |
| Ruff F | rc=0 | `python -m ruff check --no-cache --select F` → All checks passed | Có |
| actionlint ci.yml | rc=0 | rc=0, 0 chẩn đoán | Có |
| spec_hash lease r23 | 7089ad0d7c4322ff… | SPEC-r23.md (LF) sha256 khớp đủ 64 ký tự | Có |
| frozen-r14.json | head/tree/base/774/2path/245/17 | khớp từng trường với phép đo của tôi | Có |
| 17 mutant mutation-r14.json | 17/17 killed | 5 cửa MỚI tự dựng độc lập: 5/5 chết, tập LỌT khớp TỪNG TÊN (V3); 5 cửa cũ đã được R13 tự dựng (mA..mE); 7 còn lại: lời khai + suite parity | Có (mẫu 5/17 mới + 5/17 kế thừa) |
| Răng theo TỪNG cửa mới | mỗi cửa một chốt riêng | m1→8 fixture · m2→4 · m3→3 · m4→2 · m5→1, các tập KHÔNG giao nhau | Có |
| Mutant thu hẹp ngưỡng C0 | (không khai) | m6 `<14`: SỐNG 245/245 dù không tương đương (U+000E/10/1F flip 2→0); m7 escape `<14`: SỐNG 245/245, flip y hệt | **KHÔNG — finding P3** |
| A7 bốn fixture bố cục | 4 ca giữ màu | có mặt trong 245, suite ĐẠT (chua-tach/da-tach-dung/thieu-ruff/sau-registry) | Có |
| Hai phản chứng giữ màu | ruff-pin-required · ruff-version-probe-required | cả hai trong 245, ĐỎ đúng | Có |
| Đúng-một-registry-job + cùng-bước | fixture khoá | `hai-job-chay-registry` + `registry-cung-buoc-ngoai-mien` đều trong 245, ĐỎ đúng | Có |
| A4 trực tiếp trên cây | 60 mỗi job, không mức bước | 60/60/60 · step-timeout False cả 3 · job-if None cả 3 | Có |
| A3(1)(2b) trực tiếp | matrix/prefix9 | matrix.os cùng chuỗi cả 3; prefix9 hai job mới == gate; `on:` đọc qua khoá `True` có đủ push/pull_request/workflow_dispatch; concurrency có | Có |
| A1 / A5 / A2-conclusions / A6-readback / CI | not_run theo chủ kho | không CI, không dispatch, không mạng — KHÔNG ĐO ĐƯỢC, không đọc thành passed | Đúng trạng thái |
| A9 | lease khai holders 0, 371 heads, comm rỗng | offline không tái đo được ref-set remote — nhận ở mức hiện vật lease | KHÔNG ĐO ĐƯỢC (đúng phạm vi) |
| Cây review nguyên trạng | không sửa/commit | mọi đột biến ở `scratch/mutants/*` tên riêng, ROOT ghim clone; porcelain 0 + HEAD/tree không đổi đo lại cuối lượt | Có |

## Hai trục bổ sung
- **Trục Spec:** r14 delta nằm TRỌN trong write set (chỉ `.claude/dev/ci_dang_ky_test.py`; `ci.yml` không đổi
  byte). Miền công khai (SPEC «Miền công khai» + docstring 421-435) và THỰC THI khớp nhau trên mọi probe đã đo —
  hai câu docstring mới mô tả đúng ba cửa; M7 «cài trong CÙNG job, TRƯỚC bước registry» cưỡng chế đúng (fixture
  cùng-bước/khác-job/hai-job/không-job đều ĐỎ). Không thêm chốt env/runtime — đúng chỉ thị. A8 774/1000 hai path.
  Trần A8=1000 là ngoại lệ CÓ PHẠM VI neo tại A8 spec r23 — khớp.
- **Trục Standards/Security:** cả ba cửa mới đều fail-close chiều CHẶN (raise → KPT), không cửa nào mở đường
  nhận; ValueError gom về `_doc_run_ruff` — không có đường ngoại lệ thoát ra ngoài; đệ quy `$()` trần 16; heredoc
  quét tuyến tính — không lộ DoS mới. Không secrets, không dependency mới, Ruff F sạch. Verdict này KHÔNG đính
  patch-as-hint (đúng §8 cho sensitive/workflow-authority); mọi hướng sửa mô tả bằng lời + số đo từ scratch.

## Finding

### ruff-fixture-thieu-rang-chot-moi  [P3]  (sub-class MỚI: bien-nguong-C0 — GIỮ stable slug R11, không reset lịch sử)  Fixture C0 chỉ mẫu nửa DƯỚI dải nên mutant thu hẹp ngưỡng sống 245/245
TỆP/DÒNG: `.claude/dev/ci_dang_ky_test.py:1062` (tuple ký tự C0 của fixture — 4 ký tự ord 0x0D/0x0C/0x0B/0x00,
TOÀN BỘ < 0x0E) so với hai cổng dùng ngưỡng dải `ord(c) < 32` (dòng 193) và `ord(nxt) < 32` (dòng 198).
VẤN ĐỀ + COUNTEREXAMPLE (đã CHẠY): đột biến `< 32 → < 14` ở TỪNG cổng cho hai mutant KHÔNG tương đương
(`echo hi` + U+000E/U+0010/U+001F ⇒ HEAD 2 lỗi, mutant 0 lỗi — A/B `scratch/h6_ab_nguong.py`,
`scratch/h6b_escape_nguong.py`) mà CẢ HAI sống trọn suite (`rc=0 · 245/245`). Bốn ký tự mẫu đều nằm dưới mọi
ngưỡng T trong (0x0E..0x20] nên cả họ mutant thu-hẹp vô hình với lưới hiện tại — đúng ca doctrine «đột biến nới
danh sách cho phép phải làm ca đích ĐỎ»; giết «gỡ cả luật» chưa chứng minh giết «hẹp luật».
HƯỚNG SỬA CẤP LỚP (bằng lời): thêm ký tự BIÊN TRÊN của dải C0 vào tuple fixture — U+001F (US) là đủ về toán học:
với MỌI ngưỡng T <= 31, U+001F bị HEAD từ chối mà mutant nhận ⇒ ca `tran`+`escape` của nó ĐỎ ⇒ cả họ mutant
ngưỡng chết; NUL sẵn có đã khoá biên dưới. Tuỳ chọn thêm U+000E cho một điểm giữa nửa trên.
TEST/MUTANT KHOÁ: chính hai mutant m6/m7 trong `scratch/mutants/` làm phản chứng bắt buộc — sau khi thêm U+001F,
chạy lại hai mutant phải cho `rc=1` với ca `c0-4-tran`/`c0-4-escape` LỌT.
NGUY CƠ HỒI QUY: xấp xỉ 0 — mở rộng tuple thêm 1 phần tử (+4 fixture sinh tự động, +0..1 dòng, dư trần A8
774→<=1000); không đổi mã sản phẩm; HEAD đã từ chối U+001F sẵn (đo ở A/B) nên fixture mới xanh ngay trên HEAD.
ĐÃ THỬ VÁ: không — tệp thuộc write set packet + authority/gate (sensitive, §8 loại patch-as-hint); hướng sửa mô
tả bằng lời, mutant phản chứng đã nằm sẵn trong scratch của reviewer.
ĐÃ THỬ NGHIỆM: m6/m7 + A/B ba ký tự nửa trên + đối chứng 4 ký tự fixture (GIỐNG hệt hai bản — chứng minh vì sao
sống). ĐỘ TIN: cao.
VÌ SAO P3 (không phải P2): khác R11 (hai chốt KHÔNG răng — gỡ cả mệnh đề vẫn sống), ở đây gỡ-cả-luật CHẾT đúng
tập (m1/m2), sản phẩm từ chối đúng TOÀN dải C0 trên HEAD (đo trực tiếp), lỗ chỉ nằm ở độ mịn lưới đột biến cho
hồi quy tương lai — không đổi hành vi cổng trên bất kỳ đầu vào nào hôm nay.

## Kết luận theo LỚP
| lớp | verdict | căn cứ |
|---|---|---|
| 1. Installer/domain | **approve** | R11/R13 approve đứng vững; H1 (dải >=0x7F: NBSP/DEL/U+2028/U+3000/ZWSP — fail-close đủ, shlex≡POSIX một-từ) + H2 (hoa/thường: case-sensitive đúng, PEP503 GHIM đúng chủ ý); không đường nào biến ngoài-miền thành KHONG hay đúc chứng chỉ sai |
| 2. Lexer/composition/order/shell | **approve** | P2 lexical-boundary VÁ THẬT với răng riêng từng cửa (V1-V3); H3 (comment top-level × chứng chỉ) · H4 (parity escape chẵn/lẻ) · H5 (biên heredoc herestring/đôi/tab-đóng/tag) · H8 (need-&& xuyên comment) — 19 probe đều khớp POSIX/miền công bố từng ca, không phản ví dụ lớp nào dựng được |
| 3. Consumer/spec/workflow/fixtures | **approve** (kèm 1 P3 không chặn) | ba chốt pin/probe/registry + đúng-một-registry-job đo qua fixture và probe; A7 4 fixture + 2 phản chứng giữ màu; A8 774/2path; byte-identity 3bbc6b4; A4/A3-cấu-trúc đo trực tiếp; P3 `ruff-fixture-thieu-rang-chot-moi`/bien-nguong-C0 — lưới fixture, không phải hành vi cổng; H7 biên kiểu `if` nhất quán |

## KẾT LUẬN CUỐI (thay placeholder đầu tệp; hai dòng đầu tệp là canonical)
- verdict: **approve** · reviewed_sha `86b0feb1959c78affbe8cd59fb2f47df36437e82` (tree `8c16548e844c4adfdf2134535e23efee400ba8fe`).
- Findings: **P1=0 · P2=0 · P3=1** (`ruff-fixture-thieu-rang-chot-moi`/bien-nguong-C0 — không chặn, không đổi
  hành vi cổng; hướng đóng <=1 dòng, phản chứng sẵn trong scratch).
- Cả ba lớp approve ⇒ approve toàn cục theo điều kiện «cả ba lớp». Bảng săn 8 hướng mới độc lập (2/4/2 theo
  lớp), 19+ probe, 7 mutant tự dựng.
- Assurance: **cross_approved CHỈ cho CODE REVIEW trên exact SHA trên.** A1/A5/CI/A2-conclusions/A6-readback:
  **not_run/KHÔNG ĐO ĐƯỢC** theo chỉ thị chủ kho — approve này KHÔNG thay các phép đo ấy, KHÔNG mang quyền
  merge; điều kiện land theo spec/protocol (trong đó A6(b0) ruleset TRƯỚC merge) vẫn nguyên. Verdict vận chuyển
  nguyên văn lên Issue #463, không phải GitHub native approval.
- Identity: provider anthropic_claude (alias claude) · model claude-fable-5 · effort max · execution_surface
  claude_code · transport machine/local — validator so `modelUsage` thô.
- Bất biến cuối lượt (đo SAU khi viết xong thân): clone HEAD/tree không đổi · porcelain 0 dòng · mọi hiện vật
  reviewer nằm ở `VERDICT.md` + `scratch/` ngoài clone.
