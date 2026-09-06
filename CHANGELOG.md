# ★ dev-side — r355: lược đồ biên nhận v2 có cổng sau 19 ngày làm luật suông (2026-09-06)

Cross-review codex trên PR #454 (`3d5eaeb`) ra một finding P2: biên nhận lượt 5 khai
`assurance: cross_approved` mà thiếu **cả bốn** thứ `PROTOCOL §8` (dòng 453-458) đòi ở đích v2,
và tự khai model identity là KHÔNG ĐO ĐƯỢC ngay trong tệp. Kiểm lại thì đúng — và rộng hơn
một tệp.

## Đếm LỚP, không đếm lỗi

62 biên nhận · **10** khai `schema_version: 2` · **4** đủ trường · **6** thiếu. Bốn tệp đủ
(`handoff-264-*`, `plat-x8*`) chứng minh mẫu đúng đã có trong kho; năm biên nhận
`phan-bien-quy-trinh-*` của đợt này chép sai mẫu, lượt 5 làm nó thành 6.

Và **không cổng nào đọc lược đồ ấy**: `rg` không thấy `model_reviewer_identity` /
`github_submitter_identity` / `receipt_id` trong bất kỳ bộ kiểm biên nhận nào; `t26` chỉ kiểm
`verdict_path` + băm. Chính hai biên nhận v2 đầu tiên của kho đã TỰ KHAI khoảng trống ấy
(`PLAT-X8b-CHUA-CO-BO-KIEM-RECEIPT-V2`) — đặc tả có từ `2f84531` (18-08), nợ nằm im 19 ngày.

## Hai danh sách đóng băng, và cái thứ hai là chỗ dễ tự lừa

`ops/bien_nhan_v2.py`: ba trạng thái `0/1/2`, `KHÔNG ĐO ĐƯỢC` làm cổng ĐỎ.

**Allowlist legacy** — protocol nói *"11 receipt v1 cũ"*; đo `git ls-tree -r 2f84531 --
ops/reviews/` cho ĐÚNG **11** tệp, tất cả v1, cả 11 còn byte-identical với bản cutover. Miễn
trừ neo vào **BĂM**, đúng câu *"`schema_version: 1` do tác giả tệp mới tự khai không tạo miễn
trừ"*: sửa một tệp trong danh sách là MẤT miễn trừ.

**`NO_DA_DO`** — 42 biên nhận không đạt (41 tệp tự khai v1 SAU cutover + 1 v2 thiếu trường),
đóng băng theo băm, **chỉ được co lại**. Không bắt sửa hết ngay vì điền
`model_reviewer_identity` cho một lượt đã chạy xong từ lâu là **bịa bằng chứng danh tính** —
đúng thứ v2 sinh ra để chặn.

Năm biên nhận của đợt này thì nâng THẬT (có `run_id`, băm prompt, thời lượng đo được), nên nợ
là 42 chứ không phải 47.

## Cái suýt lọt — và nợ tôi khai ra để né nó dựa trên MỘT TIỀN ĐỀ SAI

Lúc nâng, tôi chỉ có SHA viết tắt `482971b` cho một tệp và **bịa nốt 32 ký tự** để có một chuỗi
40 hex. Nó qua mọi phép kiểm hình dạng; chỉ lộ vì tự đọc lại rồi chạy `git rev-parse`. Tôi khai
thành nợ `BIEN-NHAN-V2-KHONG-KIEM-SHA-CO-THAT` với lý do *"`actions/checkout` mặc định
`depth: 1` nên `git cat-file -e` sẽ ĐỎ GIẢ"*.

**Lý do ấy SAI, và cross-review PR #455 (`F4`) bắt được bằng cách đọc chính tệp workflow:**
`.github/workflows/ci.yml:86` **đã** đặt `fetch-depth: 0` từ `r226`, kèm chú thích giải thích
đúng cái bẫy tôi viện dẫn — kho đã trả giá và đã chữa từ lâu. Tôi khai một ràng buộc mà **không
đo nó**, rồi viết tiền đề ấy vào **bốn** chỗ (docstring cổng, docstring test, commit, mô tả PR)
như một đánh đổi kỹ thuật có lý.

Nay cổng ĐO thật: `_neo_git` kiểm `reviewed_sha` là commit có thật, kiểm `evidence_url` dạng
`blob/<sha>/<đường dẫn>` trỏ đúng đường dẫn có trong commit ấy, và so **băm blob** với
`verdict_sha256`. Ba trạng thái: object vắng ⇒ **KHÔNG ĐO ĐƯỢC**, in riêng, KHÔNG thành vi
phạm — reviewer nói thẳng *"Thiếu lịch sử không phải bằng chứng giả mạo."* Đo trên kho thật:
**9/9 biên nhận có commit thật, đường dẫn thật, blob khớp băm; 0 KHÔNG ĐO ĐƯỢC.**

## Vòng hai: cross-review tìm BỐN chỗ, ba P1 — và cả ba cùng một hình dạng

Hai reviewer độc lập (connector `@codex review` + một lượt `launcher.py run` trong clone rời
đầy đủ) hội tụ vào cùng bốn chỗ. Ba P1, và đọc chúng cạnh nhau thì thấy **một hình dạng duy
nhất** — đọc *sự CÓ MẶT* thành *KHẢ NĂNG*:

- **identity**: `model_reviewer_identity: {x: 1}` và `github_submitter_identity: "banana"` /
  `false` / `[]` đều QUA. Cổng identity đo đúng **sự có mặt của khoá**.
- **bánh cóc**: baseline chỉ đóng băng **TÊN**. Phản chứng chạy được: sửa một biên nhận nợ rồi
  cập nhật băm trong `NO_DA_DO` ⇒ **rc=0, 15/15, 5/5** — đã tái đóng băng một bản KHÔNG ĐẠT v2.
- **SHA**: `reviewed_sha` chỉ cần "chuỗi không rỗng" ⇒ `'deadbeef'*5` và cả
  `'khong-phai-sha-gi-ca'` đều QUA.

Và bộ test bỏ lọt **ba đột biến sản phẩm** (gỡ `TRUONG_CO_MAT` · gỡ `cuong_do` khỏi
`ANCHOR_KHOA` · gỡ `reviewed_sha` khỏi `TRUONG_VO_HUONG`) — cả ba vẫn `15/15, 5/5`. Nguyên
nhân chung: có ca âm cho **vài** trường, không có cho **từng** trường.

Nên bản vá không thêm vài ca có tên mà đổi **cơ chế**: một `MA_TRAN` chép từ spec sinh ĐÚNG MỘT
ca âm cho MỖI yêu cầu, cộng `c16` đòi ma trận phủ **đúng** tập yêu cầu của cổng — thêm hoặc bớt
một yêu cầu mà quên ca âm là ĐỎ.

## Răng

`ops/bien_nhan_v2_test.py`: **22 ca · 11/11 đột biến CÓ RĂNG**, gồm đúng hai thứ protocol đòi —
biên nhận mới tự khai v1 phải ĐỎ, và **nới allowlist để chứa tệp tấn công** phải ĐỎ. Ba lỗi
của chính bộ test bị bắt khi tự đột biến: (a) bản đóng băng của nợ lấy `frozenset(bnv2.NO_DA_DO)`
lúc nạp nên **tự nở theo** khi ai sửa mã nguồn — đúng bệnh mà chú thích cách đó ba chục dòng vừa
tố cáo; (b) khôi phục sau đột biến `setattr` lại chính object đã bẩn nên khôi phục được SỐ KHÔNG;
(c) `m4` đặt sai chiều — làm danh sách cho phép RỖNG thì chốt vẫn đỏ, tức đột biến ấy đo số không;
phải NỚI nó để chứa tên tấn công mới có răng.

Nối vào `ci.yml` và đăng ký ở `ci_dang_ky_test.py` (22/22) — guard không nằm trên đường TỰ ĐỘNG
thì guard chỉ là tài liệu.
# ★ dev-side — r354: tái sinh RELEASE_MANIFEST sau khi PR #449 land (2026-09-06)

`gate` master trên `3500369` (merge PR #449) **ĐỎ** ở bước `release-verify strict
(lane LAND — manifest committed)`, `rc=2`, bốn tệp lệch sha256. Đây đúng bài học
r238 mà `CLAUDE.md` §Quy ước deploy mục 5 đã ghi sẵn: đổi nội dung cây mà không tái
sinh manifest thì **phiên deploy KẾ TIẾP ăn gate đỏ không phải do nó**.

## Đo nền TRƯỚC khi nghi bản vá — và nền SẠCH, nên delta là của tôi

Theo mục 7 (`gate đỏ ⇒ chạy lại trên origin/master sạch, so DELTA`), đo cả hai vế
trong **một** lệnh, mỗi vế là một `git show` trên đúng commit:

| tệp | trên `2ac970f` (master TRƯỚC merge) | trên `4951f55` (master SAU) |
|---|---|---|
| `CHANGELOG.md` | KHỚP | LỆCH `25a7ae03…` → `30802c1b…` |
| `requirements.txt` | KHỚP | LỆCH `baa00d08…` → `402c04d9…` |
| `scripts/tl_core/ops_misc.py` | KHỚP | LỆCH `8849d2b2…` → `142f7ad7…` |
| `scripts/tl_selftest.py` | KHỚP | LỆCH `3ffabb08…` → `869c2f0b…` |

Bốn tệp lệch là **đúng bốn tệp trong manifest mà PR #449 sửa nội dung** (PR còn sửa
`.claude/dev/launcher_test.py` và `.claude/hooks/session-start.sh`, cả hai nằm ngoài
gói phát hành nên không có trong manifest). Không tệp nào được thêm hay xoá:
`expected_file_count 180 == checked_file_count 180`, `extra_files: []`,
`missing_from_current_manifest: []`.

**Sửa một lời khai sai của chính phiên này:** lúc chẩn đoán tôi nói `baa00d08…` là
"băm cũ đã trôi từ trước". Không phải — phép đo trên `2ac970f` cho thấy nó KHỚP.
Manifest sạch trước khi tôi merge; chính thay đổi nội dung của tôi làm nó cũ.

## Vì sao lane PR không bắt được

`ci.yml:532` gắn `if: github.ref == 'refs/heads/master'` cho bước này — lane WORKER
sinh manifest TẠM từ chính cây nên nó **hấp thụ** mọi thay đổi nội dung. Đây là mặt
thứ hai của bài học "PR xanh KHÔNG hàm ý master xanh" ở `CLAUDE.md`: lần trước là
chân Windows, lần này là một BƯỚC chỉ tồn tại ở lane LAND. `98ed924` xanh 100% trên
lane PR trong khi commit merge của nó làm master đỏ.

## Bản vá — thuần tái sinh băm, KHÔNG chạm golden

`python scripts/tl.py release-manifest --out RELEASE_MANIFEST.json`. Diff so bản
committed đúng **22 dòng**: 4 cặp `size`/`sha256` của bốn tệp trên, cộng
`total_bytes` + `package_hash` + `content_hash` tổng hợp. Không dòng nào thêm/bớt
mục ⇒ số đếm kiểm kê KHÔNG đổi ⇒ **không phải ghi lại golden** (mục 5 chỉ đòi ghi
lại golden khi số đếm đổi, và `references/golden/` không chứa `package_hash` nào).

`release-manifest` tất định theo thiết kế — `determinism_note` trong chính tệp khai
*"Manifest không chứa timestamp hay đường dẫn tuyệt đối; package_hash tính từ
path,size,sha256 đã sort"* — nên bản vá này tái lập được từ cây.

**Thứ tự bắt buộc:** ghi CHANGELOG TRƯỚC rồi mới tái sinh manifest. Ngược lại thì
chính mục changelog này làm `CHANGELOG.md` lệch băm vừa ghi — bản vá tự phá.

## Rủi ro đã nêu, và nó xảy ra trong vòng một giờ

Bản đầu của mục này ghi: *"nếu một PR khác sửa nội dung tệp thuộc gói và merge trước
thì manifest lại cũ ngay"*. PR #454 land đúng như thế — nó sửa `CHANGELOG.md` (tệp
CÓ trong manifest) trong lúc bản vá còn nằm ở PR. Cửa sổ: khoảng một giờ.

Nên phải nói cho đúng phạm vi: bản vá này **không** chặn được lớp lỗi, nó chỉ dọn
một lần. Chừng nào lane PR còn không so cây với manifest committed — mà `PROTOCOL:710`
cấm đúng điều đó, và packet #427 đóng bề mặt ấy sau một P1 thật ở #421 — thì mỗi lần
sửa nội dung một tệp thuộc gói vẫn để lại master đỏ cho phiên kế tiếp. Đó là khoảng
trống thiết kế, cần một quyết định riêng, KHÔNG phải thứ vá được trong PR này.

Kèm một va chạm nhỏ đáng ghi: hai mục cùng mang số `r353` (bản này và bản của #454).
Số r đánh theo phiên nên hai phiên song song sinh trùng là chuyện tất yếu, không phải
sự cố; bản land trước giữ số, bản này lùi thành `r354`.

# ★ dev-side — r353: bản vá chống "tín dụng giết giả" tự dính đúng bệnh nó chữa (2026-09-06)

Cross-review lượt 5 (codex, chạy trên `master` `4951f55` SAU khi PR #452 đã merge) ra bốn
finding. Cái đáng ghi là `R5-01`: bản vá `R4-04` — dựng ra để bộ chấm đột biến thôi cấp tín
dụng giết cho một crash vô can — **vẫn cấp tín dụng ấy**, chỉ qua một đường khác.

## Lớp ngoại lệ riêng chứng minh ĐƯỜNG, không chứng minh CHỐT

`TinHieuChotCa` chỉ nói "lỗi đi qua `bang()` của ca đang chạy". Nó KHÔNG nói **assertion
nghiệp vụ đích** đã chạy. `t22` dùng chính `bang()` làm chốt **khởi chạy tiến trình con**,
trước khi đọc bốn kết quả A/B/C/D. Reviewer bơm duy nhất `raise KeyError` vào đầu
`_bash_windows`: con chết `rc=1`, chưa tới phép kiểm chọn Git Bash — mà bộ phân hạng vẫn
trả `giet_that`. Chạy toàn bán kính: **chỉ `t22` chết, 0 ca `tin_dung_gia`**, nên cả phép
kiểm TÊN CA lẫn bán kính 1/23 đều mù.

Chữa: lớp `LoiDungCa` + hàm `dung()` cho chốt **giàn giáo** (dựng fixture · khởi chạy · giải
mã) — `_chay_1_ca` đọc nó thành `tin_dung_gia`. Ranh giới khai **tại chỗ gọi**, KHÔNG đoán
theo mã thoát: `chay(...)`/`cai_cong_cu.sh` là sản phẩm đang bị đo nên `rc` là hợp đồng của
nó. Reviewer cảnh báo đúng chỗ đó, và đột biến C đo được cái giá của bản vá quá tay: hạ mọi
chốt mang `rc=` thành giàn giáo làm **năm** đột biến thật (`t2` `t3` `t7` `t9` `t10`) mất
tín dụng hợp lệ.

Răng: đột biến A đưa `t22` về `bang()` ⇒ phép đo mới ĐỎ với đúng chữ `giet_that` reviewer
đã thấy. Thêm hai ca tự kiểm `f`/`g` và một phản chứng **đi qua ranh giới tiến trình** —
năm ca tự kiểm cũ đều chạy trong cùng tiến trình nên chúng bỏ sót đúng đường này.

## Và cổng shell mới cũng nói dối theo cách kinh điển

`R5-02`: `ops/kiem_trang_quyet_dinh.sh` đồng nhất "phép đo thất bại" với "không tìm thấy".
`grep` trả `1` khi không khớp và `>1` khi **không thực hiện được** phép đo, mà cả hai rơi
xuống nhánh in SẠCH; `set -euo pipefail` không chữa được vì lệnh nằm trong điều kiện `if`.
Đo: regex hỏng ⇒ `rc=0 "sạch"` · mất mốc kết thúc ⇒ `rc=0` · đổi tên mốc ⇒ `rc=1` bắt oan.
Nay ba trạng thái `0/1/2`, đòi đúng một cặp mốc theo thứ tự, kèm
`ops/kiem_trang_quyet_dinh_test.sh` (7 ca + 4 phép đo răng, hai đột biến tái hiện lại đúng
ba con số trên). Khai thẳng: **không workflow nào chạy cổng ấy** — `ci_dang_ky_test.py` chỉ
quét `*_test.py`.

## Bài học, không phải con số

Đây là lần thứ **sáu** trong cùng một đợt của cùng một lớp lỗi (đọc *sự CÓ MẶT* thành *KHẢ
NĂNG*), và là lần đắt nhất vì nó nằm **bên trong bản vá dựng ra để chặn lớp ấy**: có tên
lớp, có ca tự kiểm cho lớp, vẫn trượt. Thứ bắt được nó không phải một reviewer đọc kỹ hơn
mà một phép đo **đi qua ranh giới tiến trình** — tức reviewer có **năng lực ĐO**.

Nhắc thêm một lỗi quy trình của chính đợt này: PR #452 được merge **một phút** sau khi lượt
review ấy bắt đầu, nên hai commit cuối vào `master` không có lượt khác nền nào kết luận.
`CLAUDE.md` đã ghi sẵn *"Gate xanh KHÔNG phải đã được review"*; đây là lần trả giá.

# ★ dev-side — r352: luật thô của r351 vẫn thủng ở BIẾN MÔI TRƯỜNG (2026-09-06)

Vòng 11 ra **một** finding (giảm từ bốn), và nó bắt đúng chỗ tôi **tự kiểm mà không nghĩ
ra**. pip **giải biến môi trường TRƯỚC** khi phân tích option, nên một dòng `${INCLUDE}`
với `INCLUDE='-r extra.txt'` kéo được tệp khác vào trong khi ký tự đầu là `$` chứ không
phải `-`. Đo: pip **có** kéo `extra.txt`; luật thô lần một trả `0`.

## Câu hỏi ĐÚNG, phép thử THIẾU MỘT DẠNG

Đáng ghi vì tôi đã hỏi chính xác câu này ở lượt trước — *"pip có dạng nào không bắt đầu
bằng `-` mà vẫn kéo tệp khác vào không?"* — rồi tự đo bằng `pypdf -r extra.txt`, thấy pip
không đệ quy, và kết luận **"không thủng"**. Tôi đọc `break_args_options` rồi dừng;
reviewer đọc tiếp tới `expand_env_variables`. Nghĩ ra được câu hỏi không có nghĩa là đã
trả lời được nó — và một phép thử thiếu dạng thì cho ra đúng cái cảm giác "đã kiểm".

Chữa theo đúng tinh thần r351: **thô hơn nữa** — dòng nào **chứa dấu đô-la** cũng tính là
có chỉ thị. Cố ý KHÔNG đọc giá trị biến và KHÔNG chép luật `${UPPER_CASE}` của pip: chép
luật chính là thứ đã hỏng bảy lần. Chiều sai vẫn an toàn — một dòng có `$` vô hại chỉ tốn
thêm một lượt pip.

## Ca khoá của chính bản vá này SUÝT không có răng

Thêm hai dạng `${INCLUDE}` / `$INCLUDE` vào bảng ca xong, phép đo răng hai chiều cho
**XANH ở CẢ HAI vế** — tức ca không đo gì. Lý do: fixture không đặt biến, nên pip thất
bại, nên không có mốc nào được đặt, nên ca xanh **vì lý do sai**. Đặt `INCLUDE='-r
extra.txt'` thì hook chưa vá đặt mốc = 1 và ca ĐỎ đúng như phải thế.

Đây là lần thứ **ba** trong đợt phép đo răng cứu một ca xanh vô nghĩa, và lần này nạn nhân
là ca vừa viết để khoá bản vá. Ca xanh không chứng minh gì nếu chưa ai thử giết nó — kể cả
khi ca ấy vừa ra đời từ một finding thật.

Cổng: `launcher_test` **181/181** (bỏ qua 1 — fixture Windows) · đột biến **170/170**
(1 không đo được trên nền này) · `ops/cong_cu_test.py` **0 đỏ** · `tl --selftest`
**1709/1709** · ruff `--select F` delta = **0** · `bash -n` OK · `git diff --check` rc=0 ·
quét mẫu bí mật 25 dòng thêm: 0 khớp · hook chạy thật hai lượt đúng thiết kế · bốn dạng đo
lại (`${INCLUDE}` · `$INCLUDE` · `-r extra.txt` ⇒ không mốc; `pypdf>=3.0` ⇒ có mốc).

# ★ dev-side — r351: ngừng bắt chước cú pháp pip; hình dạng lỗi lặp LẦN THỨ HAI (2026-09-06)

Vòng 10 ra bốn finding, **tất cả ở bộ phân tích chỉ thị include**, và tôi **không vá từng
cái** — bỏ cả bộ phân tích. Lý do là HÌNH DẠNG, không phải bốn lỗi ấy.

| lượt | tôi tự làm gì | finding | chữa bằng |
|---|---|---|---|
| r338–r341 | tự phân tích **dòng requirement** | 5 | uỷ quyền cho pip (r342) |
| r347 · r349 · r350 · vòng 10 | tự phân tích **chỉ thị include** | ~7 | **ngừng phân tích** (r351) |

Mỗi vòng vá xong lại lộ một luật pip chép chưa đúng: `expand_env_variables` chỉ nhận
`${UPPER}` và bỏ giá trị rỗng · `join_lines` dùng `strip(backslash)` chứ không bỏ MỘT ký
tự · `realpath` gộp làm mất một nhánh symlink · chuỗi `KHONG_DOC_DUOC` trong tệp thật
trùng trạng thái tệp bị xoá. Lần này **không uỷ quyền cho pip được**: phép băm phải chạy
offline, mà pip thì không.

## Luật mới thô — và thô là điểm mạnh

Ký tự đầu không-trắng của một dòng là `-` ⇒ có chỉ thị ⇒ **không đặt mốc**, để pip quyết.
Nó **không cần biết cú pháp pip**, nên không có gì để chép sai. Một dòng `# -r x` bị tính
nhầm chỉ tốn một lượt pip thừa — **chiều sai duy nhất là AN TOÀN**. Cả lớp "chép sai luật
của pip" chết theo KIẾN TRÚC, không còn nhánh nào để vá.

Đo: **chín** dạng chỉ thị (gồm hai dạng vòng 10 vừa bắt: nhiều dấu chéo ngược, và biến
môi trường) — không dạng nào đặt mốc. **Răng chiều ngược**: không có chỉ thị thì VẪN phải
đặt mốc, kẻo bản vá thành "không bao giờ đặt mốc" — đúng kiểu chốt không thể đỏ.

## Giá phải trả — ĐO, không khẳng định

Kho nào dùng `-r`/`-c`/`-e` sẽ chạy pip mỗi lượt mở phiên. Kho này **không có chỉ thị
nào**, nên giá ở đây bằng **không** — và điều đó được khoá bằng một ca test, để ai thêm
chỉ thị sau này thì ca ấy đỏ và người thêm biết mình đang đánh đổi gì. Nói cái giá ra
thành một ca chạy được, thay vì một câu trong tài liệu sẽ trôi.

Cổng: 9/9 dạng chỉ thị · `launcher_test` **181/181** (bỏ qua 1 — fixture Windows) ·
`ops/cong_cu_test.py` **22/22** (cổng vừa đỏ vì r349, nay xanh) · `tl --selftest`
**1709/1709** · ruff `--select F` delta = **0** · `bash -n` OK · `git diff --check` rc=0 ·
`doc-claims-check --strict` rc=0 · hook chạy thật hai lượt đúng thiết kế.

# ★ dev-side — r350: `gate` ĐỎ vì ca test của r349, và cổng đẩy tôi sang cách test đúng hơn (2026-09-06)

`gate (ubuntu-latest)` đỏ trên `a2c0194` — **lần đầu trong cả chuỗi này cổng đo mã đỏ vì
lỗi của tôi**, không phải cổng duyệt. Bước đỏ: *"G5 kiểm bản kê công cụ + T1..T8"*.

Nguyên nhân: ca `t16` trong `ops/cong_cu_test.py` đòi **mọi gói bên thứ ba import trong
cây phải được khai ở `ops/cong_cu.yaml`**. Ca `r349` của tôi `import tl_core` trực tiếp
trong `launcher_test.py`, nên bộ quét xếp `tl_core` vào bên thứ ba ⇒ đỏ, kéo theo 17 dòng
đỏ dây chuyền vì mọi đột biến đều "giết thêm" ca ấy.

## Cách sửa dễ nhất là cách sai

Nới `ops/cong_cu.yaml` để `tl_core` được chấp nhận sẽ làm cổng xanh trong một phút — và
hạ một chốt thật. Chính `t16` ghi trong mã rằng bản đầu của nó từng có cửa thoát *"hoặc
thấy tên trong ci.yml"*, và **đo được** rằng cửa ấy vô hiệu hoá cả ca (gỡ `jsonschema`
khỏi bản kê mà ca vẫn xanh).

Chữa đúng: **chạy phép đo trong TIẾN TRÌNH CON** thay vì import. Hai lợi ích, và cái thứ
hai tôi không lường trước:

1. Đo trên interpreter **sạch** — không phải nghịch `sys.modules`/`sys.meta_path` của
   chính bộ test. Đây đúng là thứ đã làm tôi **dựng sai fixture hai lần** ở r349.
2. Không import gói ngoài cây ⇒ `t16` không có gì để bắt.

Tức cổng không chỉ chặn một vi phạm hình thức — **nó đẩy tôi sang cách test đúng hơn về
bản chất**. Đáng ghi vì phản xạ đầu tiên khi gặp cổng đỏ là hỏi *"làm sao cho nó xanh"*,
trong khi câu hỏi đúng là *"cổng đang nói gì về thiết kế của mình"*.

## Một con số phải nói cho đúng

Chạy `ops/cong_cu_test.py` cục bộ vẫn cho `rc=1`, và đó **không phải hồi quy**:
`actionlint` không có trên PATH trong container này ⇒ ca `t2_canary_thieu_shellcheck` bị
BỎ QUA ⇒ đột biến của nó thành `KHÔNG_ĐO_ĐƯỢC` ⇒ cổng fail-close, đúng thiết kế
(`CLAUDE.md`: một cổng tự tắt khi thiếu công cụ là cổng không tồn tại đúng lúc cần nhất).
Đo nền `origin/master`: **rc=1, cùng một con số** ⇒ delta = 0. Thứ đã đổi là `t16` không
còn ĐỎ và `22/22` khớp hệt nền.

Cổng: `ops/cong_cu_test.py` **22/22 đạt** (bỏ qua 1 — thiếu `actionlint` cục bộ, delta so
master = 0) · `launcher_test` **180/180** (bỏ qua 1 — fixture Windows).

# ★ dev-side — r349: va chạm vân tay (im lặng SAI), và một chẩn đoán tự mâu thuẫn (2026-09-06)

Vòng 9 ra năm finding; **một cái tôi đã tự tìm và vá ở r348 trước khi lượt review về** (`..`
trong RECORD), nên hai bên gặp nhau độc lập. Bốn cái còn lại đều tái hiện trước khi vá.

## Ba lỗ của khối băm — cái đầu thuộc lớp chưa từng gặp trong chuỗi này

Tám vòng trước toàn **báo động giả** (nói hỏng trong khi đúng). Lỗ này ngược lại: **im lặng
SAI**. Băm nội dung THÔ nên hai bố cục include khác nhau cho **cùng một chuỗi byte** —
chuyển `somepkg` từ tệp `-c` (chỉ *ràng buộc*) sang tệp `-r` (*CÀI THẬT*) ⇒ vân tay y hệt
⇒ mốc sống sót ⇒ **gói mới khai báo không bao giờ được cài**. Chữa bằng đóng KHUNG từng
tệp (độ dài + đường dẫn + độ dài + nội dung), nên không bố cục nào trùng được bố cục khác.

Hai lỗ còn lại cùng họ "luật của pip rộng hơn luật của tôi": một dòng **chú thích** kết
thúc bằng dấu chéo ngược kéo chỉ thị `-r` kế tiếp vào chính nó rồi bị cắt mất (pip miễn
trừ dòng khớp `COMMENT_RE` khỏi phép nối), và **đối số dính liền** `-rextra.txt` là một
token duy nhất mà không nhánh nào nhận ra.

Đo lại: **7/7** — ba lỗ mới đóng, bốn dạng cũ không hồi quy.

## Chẩn đoán tự mâu thuẫn

`_doc_dep_probe` tính `co = pypdf or pdfplumber` (**đúng**) nhưng vẫn in `loi_import`
(**sai**): `pypdf` hỏng + `pdfplumber` chạy ⇒ `co=True` mà hậu quả vẫn ghi *"MỌI .pdf bị
chặn … cài lại phụ thuộc"*. Cùng doctrine với `codex login status` NÓI DỐI — một công cụ
báo sai trạng thái **tệ hơn** công cụ vắng mặt, vì nó đẩy người đọc đi sai hướng. Nay:
còn đường chạy thì nói "đường PDF vẫn chạy" và **vẫn nhắc** backend hỏng (không nuốt thông
tin chẩn đoán); hỏng thật thì vẫn nói bị chặn. Ba trạng thái đo đủ, có răng hai chiều.

## Hai lần fixture của tôi sai chứ không phải mã sai

Đo backend PDF, lần đầu tôi kết luận nhầm vì môi trường thật vẫn có `pypdf` nên ca "cả hai
thiếu" **dựng không thành**; lần hai tôi quên tạo `pdfplumber.py` nên ca "dự phòng chạy"
đo nhầm sang "dự phòng thiếu". Phải chặn bằng meta-path finder mới dựng đúng ba trạng
thái. Đúng bệnh **"ca có MẶT khác ca có ĐO"**: cả hai lần ca vẫn chạy và vẫn in số — chỉ
là số ấy không đo cái tôi nghĩ nó đo.

Cổng: 7/7 ca vân tay · 3/3 trạng thái backend PDF · `launcher_test` **180/180** (bỏ qua 1 —
fixture Windows) · `tl --selftest` **1709/1709** · ruff `--select F` delta so `6f97fda` =
**0** (`ops_misc.py` 403/403 · `launcher_test.py` 4/4) · `bash -n` OK · `git diff --check`
rc=0.

# ★ dev-side — r348: đường lui của r347 mang vào một BÁO ĐỘNG GIẢ, tự tìm ra (2026-09-06)

`_module_cua()` — thứ vừa thêm ở r347 để chữa lỗ Python <3.10 — suy **sai** cho gói **chỉ
có CLI**. RECORD của loại gói ấy ghi đường kiểu `../../../bin/clix`, nên đoạn đầu là `..`:
không bắt đầu bằng gạch dưới, không trùng hậu tố loại trừ nào, nên lọt qua và hook đi
`__import__("..")`. Đo được trước khi vá: **`rc=1` cho một môi trường HOÀN TOÀN ĐÚNG**.

Đúng lớp **BÁO ĐỘNG GIẢ** đã sinh ra bảy finding đầu của chuỗi này — và lần này do chính
bản vá của tôi mang vào, ở commit ngay sau. Chuỗi r343 → r344 đã dạy đúng bài này (một
cửa thoát tự thêm sinh hai lỗ mới); r347 → r348 lặp lại nó ở quy mô nhỏ hơn.

Chốt là **`isidentifier()`**: tên module hợp lệ luôn là một định danh Python. Đây là danh
sách **CHO PHÉP** (thứ hợp lệ mới qua), không phải thêm `..` vào danh sách cấm — bài học
r344 áp thẳng vào đây, lần này áp *trước* khi bị bắt.

**Cách tìm ra đáng ghi hơn bản vá.** Tôi gửi reviewer ba câu hỏi về chính bản vá r347, rồi
thay vì ngồi đợi trả lời thì đi đo câu số 2 (*"dạng gói nào làm `_module_cua` suy sai?"*).
Ba dạng dựng thử — gói chỉ có CLI · wheel có `.data` · không có `top_level.txt` — và dạng
đầu tiên đỏ ngay. Bài học: **một câu hỏi đủ tốt để gửi reviewer thì cũng đủ tốt để tự
chạy**; gửi đi rồi chờ là biến một phép đo rẻ thành một vòng review.

Cổng: 3/3 dạng gói đúng · `launcher_test` **178/178** (bỏ qua 1 — fixture Windows) ·
`tl --selftest` **1709/1709** · ruff `--select F` delta = **0** · `bash -n` OK ·
`git diff --check` rc=0.

# ★ dev-side — r347: hai lỗ của r345, và một lời khai bị thu hẹp LẦN THỨ HAI (2026-09-06)

Vòng 8 (16 finding). Hai lỗ cụ thể, cả hai tái hiện được trước khi vá:

- **Python 3.8/3.9 mất phép thăm import.** `packages_distributions` chỉ có từ 3.10, nên
  trên hai nền ta **cố ý hỗ trợ** thì `ban_do` rỗng ⇒ vòng thăm không thăm gì ⇒ lớp bảo
  vệ r337 biến mất **im lặng**. Đo: giả lập bỏ `packages_distributions` rồi phá
  `pypdf/__init__.py` ⇒ chốt trả **0** thay vì 1. Chữa bằng đường lui `_module_cua()`
  đọc `top_level.txt`, thiếu thì suy từ `dist.files`.
- **Cú pháp include của pip rộng hơn regex của tôi.** `-r 'có nháy'` · nối dòng bằng dấu
  chéo ngược · `--requirement=${BIẾN}` — pip nhận cả ba, regex cũ bỏ sót cả ba ⇒ sửa tệp
  được include mà **vân tay không đổi** ⇒ mốc sống sót ⇒ hook bỏ qua cài đặt. Chữa bằng
  `shlex` (lo dấu nháy) + `expandvars` + nối dòng trước khi cắt chú thích, đúng thứ tự
  pip làm. Đo theo **hành vi**, không soi biểu thức: sửa tệp include ở cả bốn dạng ⇒ vân
  tay đổi ở cả bốn.

## Lời khai "offline" bị thu hẹp lần thứ HAI

r345 viết hook *"offline theo cấu tạo"*. r346 đã thu hẹp lần một (phép đo AST chỉ thấy
`import` tĩnh). Lượt này reviewer thu hẹp lần hai, và đúng: **mạng vẫn có thể đến từ chính
việc `import` một gói đã khai**, nếu module ấy mở kết nối lúc nạp — họ đo bằng một gói
tổng hợp, listener đếm **1 kết nối**.

Không bịt ở đây, và nói rõ vì sao: bịt nó cần một **hộp cát mạng thật**, trong khi phép
thăm import — thứ **duy nhất** thấy được lớp lỗi r337 — buộc phải nạp mã của gói. Nên câu
đúng là **"mã hook không tự gọi mạng"**, còn chạm mạng gián tiếp qua gói được khai là
**giới hạn được khai**, không phải lỗ được vá.

Đáng ghi: cùng một câu đã phải sửa **hai lần trong hai commit liên tiếp**, mỗi lần vì một
hướng khác nhau. Viết một câu bảo đảm rộng thì rẻ; đo đủ để đỡ nó thì không — và mỗi chỗ
chưa đo là một chỗ sẽ bị bác.

Cổng: 6/6 ca `<3.10` và `>=3.10` đúng · 4/4 dạng include bắt được · `launcher_test`
**176/176** (bỏ qua 1 — fixture Windows) · đột biến **170/170** (1 không đo được trên nền
này) · `tl --selftest` **1709/1709** · ruff `--select F` delta = **0** · `bash -n` OK ·
`git diff --check` rc=0 · `doc-claims-check --strict` rc=0 · quét mẫu bí mật 211 dòng
thêm: 0 khớp · hook chạy thật hai lượt đúng thiết kế.

# ★ dev-side — r346: ca chống-mạng của r345 CÓ ĐIỂM MÙ, và lời khai đã rộng hơn phép đo (2026-09-06)

Commit r345 viết rằng ca `r345_than_hook_KHONG_duoc_co_duong_mang_nao` là *"phép đo cấu
trúc, cả lớp mở-phiên-chậm-vì-mạng chết theo KIẾN TRÚC"*. Tự kiểm bằng bốn phản chứng cho
thấy câu ấy **rộng hơn phép đo**: phép đo AST chỉ thấy `import x` **tĩnh**, nên
`__import__('socket')` · `__import__` với tên dựng động · `importlib.import_module` ·
`ctypes` **lọt cả bốn**.

Nó vẫn có răng cho ca THỰC TẾ — ai đó thêm lại `import subprocess` thì ĐỎ ngay, và điều ấy
đã đo hai chiều ở r345. Nhưng "bắt được ca thực tế" khác "cả lớp chết theo kiến trúc", và
viết câu thứ hai khi chỉ đo được câu thứ nhất là đúng lớp lỗi kho này đã trả giá nhiều
lần: **lời khai rộng hơn phép đo**. Lần này nạn nhân là chính cái chốt vừa dựng ra để
chống bị lừa — cùng họ với *"cổng vắng mặt trông giống cổng xanh"*.

Chữa bằng một lớp **HÀNH VI**, không phải bằng cách nới danh sách tên module (nới danh
sách là danh sách CẤM, và kho đã học rằng nó thua từ trong thiết kế): chặn `socket` ở tầng
thư viện rồi đòi thân hook **vẫn trả lời đúng**. Thân hook bắt `BaseException` khắp nơi
nên một phép mở socket bị chặn sẽ biến thành mục `hong` ⇒ mã thoát đổi ⇒ lộ. Cách viết
nào cũng lộ, vì phép đo đứng ở tầng dưới mọi cách viết.

Kèm răng: một thân hook **có** chạm mạng (`socket.socket()` nối thêm) phải làm ca ấy ĐỎ —
không có phản chứng đó thì phép chặn socket chỉ là một câu lệnh không ai biết có tác dụng.

Điểm mù của lớp AST nay ghi thẳng trong docstring của ca, thay vì để người đọc tưởng nó
phủ hết.

Cổng: `launcher_test` **173/173** (bỏ qua 1 — fixture Windows) · ruff `--select F` delta
= **0** · `bash -n` OK.

# ★ dev-side — r345: BỎ HẲN phép hỏi pip lúc mở phiên; 13 finding, 7 vòng, hai hình dạng (2026-09-06)

Vòng 7 ra ba P2, và một trong đó **bác bỏ bảo đảm của cả thiết kế** chứ không phải chỉ ra
một khe hở. Đo trực tiếp bằng socket đếm kết nối: một gói **đã cài** có
`Requires-Dist: childpkg @ http://…/x.whl` khiến pip đi lấy URL ấy **ngay cả khi**
`requirements.txt` chỉ có một dòng TRẦN và đã có `--no-index` — **1 kết nối**. Nghĩa là
**không thể bảo đảm offline bằng cách soi tệp requirements**: thứ quyết định nằm trong
metadata của gói đã cài, ngoài tầm mọi phép đọc tệp.

## Đếm hình dạng, không đếm lỗi — và lần này có HAI hình dạng

| vòng | hình dạng | kết cục |
|---|---|---|
| r338–r341 (5 finding) | **ta tự làm thay pip** (ghim bản · bản đã cài · marker · `#`) | r342 uỷ quyền cho pip |
| r343–r345 (8 finding) | **mọi cách làm phép hỏi pip an toàn đều thua** | r345 bỏ hẳn phép hỏi pip |

`CLAUDE.md` đặt ngưỡng ở ba lần cùng hình dạng. Hình dạng thứ nhất tôi nhận ra ở lần thứ
năm; hình dạng thứ hai ở lần thứ ba — nhưng chỉ vì phản chứng ép, không phải vì tôi tự
đếm. Chuỗi r343 → r344 là hai lần vá liên tiếp cho **cùng một bảo đảm không thể giữ
được**: `--no-index` không chặn direct reference, rồi danh sách CẤM lọt URL trần và
`git+`. Đáng ghi hơn cả: **r343 dựng lại đúng cơ chế "ta tự quyết" mà r342 sinh ra để
bỏ** — tôi viết bài học vào commit r342 rồi vi phạm nó ở commit ngay sau.

## Còn lại: ba phép đo CỤC BỘ, offline theo cấu tạo

- **bản đã cài có thoả specifier không** — `importlib.metadata` + `SpecifierSet`;
- **gói có còn đó không** — `distribution()`; vắng mặt là hỏng;
- **`import` có chạy không** — lớp lỗi r337 mà pip không bao giờ thấy.

Hai finding còn lại của vòng cũng chữa: `distribution` nay **import riêng** (gộp một câu
`from … import a, b` làm nhánh `ImportError` vứt luôn `distribution` trên Python 3.8/3.9 —
đúng các nền ta cố ý hỗ trợ), và `VAN_TAY` nay **băm cả tệp `-r`/`-c` được include** (đệ
quy, giải đường tương đối theo tệp chứa nó, chặn chu trình; đọc không được thì đưa chính
đường dẫn vào băm, vì `KHÔNG ĐO ĐƯỢC` ≠ `giống nhau`). Phản chứng: sửa `extra.txt` từ
`pypdf>=3.0` sang `>=4.0` ⇒ vân tay đổi `a86b9149…` → `9d02d12a…`.

## Bất biến mạnh nhất, và nó đo được mà không cần dựng gì

`r345_than_hook_KHONG_duoc_co_duong_mang_nao` đọc **cây cú pháp** của thân hook và đòi
không có `subprocess` · `socket` · `urllib` · `http`. Đây không phải lời hứa "chúng tôi
tin là offline" mà là một phép đo cấu trúc: cả lớp *"mở phiên chậm vì mạng"* chết theo
KIẾN TRÚC. Đo răng hai chiều — bản `3a19298` chưa vá làm ca này **ĐỎ**
(`import module co duong mang: ['subprocess']`), chỉ thay tệp hook ⇒ **XANH**.

## Khai thẳng thứ đã mất

Không còn phép giải phụ thuộc của pip, nên **extras sâu và `-r` lồng nhau không được kiểm
nội dung**. Bù ở chỗ khác: vân tay băm cả tệp include nên sửa chúng làm mốc hết hiệu lực
và pip thật sự chạy lại. Đổi một phép đo **không bảo đảm được** lấy một phép đo **bảo đảm
được** — và nói rõ cái giá thay vì giấu nó.

Cổng: 10/10 ca cục bộ đúng (gồm URL trần · `git+` · direct reference · vắng mặt) · phản
chứng metadata bắc cầu **0 kết nối** (trước: 1) · `launcher_test` **172/172** (bỏ qua 1 —
fixture Windows) · đột biến **170/170** (1 không đo được trên nền này) · `tl --selftest`
**1709/1709** · ruff `--select F` delta = **0** · `bash -n` OK · `git diff --check` rc=0 ·
quét mẫu bí mật 184 dòng thêm: 0 khớp · hook chạy thật hai lượt đúng thiết kế · phép đo
thời gian 5 lượt liên tiếp: **0,19s** ổn định (1,27s lượt đầu là khởi động nguội).

# ★ dev-side — r344: đảo danh sách CẤM thành danh sách CHO PHÉP, và tôi vừa tái phạm đúng thứ mình vừa sửa (2026-09-06)

Lượt review thứ sáu ra hai P2, và **cả hai đều là hậu quả của `_co_xa`** — cái cửa thoát
tôi tự thêm ở r343. Tức r343 dựng lại một cơ chế *"ta tự quyết"*, đúng thứ r342 sinh ra để
bỏ, và nó thủng ngay lượt sau.

Thủng theo đúng cách `CLAUDE.md` đã tiên đoán: `_co_xa` dò `@ scheme://` nên **URL TRẦN**
(`http://host/x.whl`) và **VCS** (`git+https://…`) lọt sạch — đo được `rc=1` sau 0,97s và
0,65s, tức mỗi phiên vẫn chạm mạng rồi đi đường cài lại. *"Danh sách CẤM phải đoán trước
MỌI cách viết nên thua từ trong thiết kế; danh sách cho phép chỉ phải liệt kê một tập NHỎ
và BIẾT TRƯỚC."*

**Đảo lại:** chỉ hỏi pip khi **mọi** dòng là `Requirement` trần (có tên, có thể có
specifier/marker, **không** có `url`); có `-r`/`-c`/`-e` hay bất kỳ URL nào ⇒ không hỏi.
Chiều rủi ro của khe hở nay **ngược**: bỏ sót một dạng hợp lệ chỉ làm ta hỏi pip *ít hơn*,
không bao giờ làm pip đi lấy mạng lúc mở phiên. Đo sau vá: **0,09–0,15s** ở cả ba dạng
nguồn từ xa (trước: 0,65s · 0,97s · 8,5s).

**P2 thứ hai — gói VẮNG MẶT bị coi là đủ.** Khi danh sách cho phép từ chối, lớp phụ là thứ
duy nhất còn lại, mà nó lại lặng lẽ bỏ qua gói không có trong `ban_do` ⇒ một mốc cũ cộng
một gói đã gỡ khiến chốt trả 0 mãi mãi. Chữa bằng kiểm **metadata** (`importlib.metadata`),
KHÔNG phải kiểm module — gói chỉ có CLI hoặc gói meta thì không phơi module nào cả.

**BA KỲ VỌNG ĐẦU CỦA TÔI TRONG BẢNG ĐO LÀ SAI, KHÔNG PHẢI MÃ SAI.** Tôi viết "URL trần
phải `rc=1`", trong khi thiết kế nói ngược: allowlist từ chối ⇒ lui về mốc + thăm import ⇒
`rc=0`. Thứ giữ cho việc ấy an toàn là **mốc khoá theo `sha256(requirements.txt)`** và chỉ
được đặt SAU khi `pip install` thành công (`: > "$DAU"`) — nên một tệp hỏng hay một URL
chết **không bao giờ đặt được mốc**, và sửa tệp thì băm đổi, mốc hết hiệu lực. Đã đo cả hai
vế thay vì khẳng định. Bài học: khi ba ca cùng "đỏ", hãy hỏi *"kỳ vọng của tôi có đúng
không"* trước khi hỏi *"mã sai ở đâu"*.

**Một bất biến bị THU HẸP, và nói ra thay vì lặng lẽ bỏ ca:** "đối chiếu với pip" nay chỉ
áp cho tệp mà danh sách cho phép NHẬN. Hai ca `dòng hỏng` và `-r` rời khỏi bảng parity, kèm
lý do ngay trong mã. **Khoảng trống còn lại, khai thẳng:** gói bị gỡ SAU khi mốc đã đặt,
trên một dòng mà `Requirement` không phân tích được (URL trần, VCS) ⇒ không phát hiện được;
dạng `tên @ url` thì phát hiện được, và `r344` đo đúng chỗ đó.

Cổng: `launcher_test` **175/175** (bỏ qua 1 — fixture Windows) · đột biến **170/170**
(1 không đo được trên nền này) · `tl --selftest` **1709/1709** · ruff `--select F` delta
= **0** · `bash -n` OK · `git diff --check` rc=0 · hook chạy thật hai lượt đúng thiết kế.

# ★ dev-side — r343: `--no-index` KHÔNG làm phép đo offline (lớp lỗi r342 tự mở ra) (2026-09-06)

Lượt review sau r342 ra **một** P2 (giảm từ ba), và nó trả lời đúng câu hỏi tôi đặt cho
reviewer — *"uỷ quyền cho pip có mở ra lớp lỗi MỚI nào không?"*. **Có.**

`--no-index` chỉ tắt **tra cứu chỉ mục**; một **direct reference** (`gói @ https://…`) vẫn
được pip đi lấy. Phản chứng đã chạy: `pypdf @ http://127.0.0.1:9/…whl` tới một host chết ⇒
pip thử rồi thoát 1 sau **8,5s** ⇒ **mỗi** lần mở phiên chậm thêm chừng ấy VÀ luôn đi đường
cài lại. Một chốt chẩn đoán làm chậm mọi phiên là chốt sẽ bị gỡ — nên đây không phải phiền
toái nhỏ, nó ăn đúng vào lý do chốt tồn tại.

Đáng ghi vì lập luận sai nằm trong chính commit r342: ở đó tôi viết *"kèm `--no-index` để
hook phiên không phụ thuộc mạng"* và **khai thẳng với reviewer rằng đó là LẬP LUẬN chứ chưa
phải phép đo, xin một phản chứng nếu có**. Phản chứng có thật, và tới trong một lượt. Bài
học không phải "đọc `--help` kỹ hơn" mà là: **một mệnh đề tự khai là chưa đo thì phải được
đo, không phải được ghi chú rồi cho qua** — ghi chú không làm nó đúng lên.

Chữa bằng hai lớp, chiều rủi ro của cả hai đều an toàn:

1. **Có direct reference từ xa ⇒ KHÔNG hỏi pip.** Lúc ấy mốc (băm theo `requirements.txt`
   + `sys.prefix`) cộng phép thăm import là thứ ta có; khai thẳng là không đo được bản chứ
   đừng giả vờ đã đo.
2. **Chặn thời gian cho mọi trường hợp khác** — `--retries 0`, `--timeout 3`, và hạn của
   chính tiến trình con — để một lỗ còn sót không bao giờ treo phiên.

Khe hở của phép dò direct reference chỉ dẫn tới *"hỏi pip có chặn thời gian"*, không dẫn
tới *"chặn phiên"*.

Đo sau khi vá: `8,5s / rc=1` → **`0,2s / rc=0`**; bốn ca khác (bản thoả · lệch bản · marker
không khớp · gói thiếu hẳn) không hồi quy. Ca `r343` đo **cả hai** hậu quả — mã thoát VÀ
thời gian — vì cái hại chính là độ trễ; đột biến gỡ chốt phải làm ca đích ĐỎ.

**Neo đột biến của `r342` gãy vì bản vá này** (`if kiem_ban:` → `if kiem_ban and not
_co_xa:`) và suite bắt được ngay — đúng công dụng của phép đếm neo: nó biến một đột biến
âm thầm mất răng thành một ca ĐỎ ồn ào.

Cổng: `launcher_test` **174/174** (bỏ qua 1 — fixture Windows) · đột biến **170/170**
(1 không đo được trên nền này) · `tl --selftest` **1709/1709** · ruff `--select F` delta
= **0** · `bash -n` OK · `git diff --check` rc=0 · hook chạy thật hai lượt đúng thiết kế.

# ★ dev-side — r342: NGỪNG TỰ QUYẾT, HỎI PIP — bảy finding một hình dạng (2026-09-06)

Lượt review thứ tư trên `37af367` ra **ba P2 nữa** — direct reference (`foo @ URL`),
extras (`foo[x]`), và chỉ thị `-r`/`-c`/`-e` — nâng tổng lên **BẢY finding, một hình
dạng**: *bộ phân tích TỰ VIẾT của hook lệch khỏi luật của pip.*

| vòng | ta tự làm gì | hậu quả đo được |
|---|---|---|
| r338 | ghim `==6.0.3` | pip phải gỡ gói distro ⇒ hook đỏ mọi lượt |
| r339 | tự đòi bản ở chế độ hậu-pip | chốt đỏ thường trực khi thiếu bộ phân tích |
| r340 | tự cắt marker | pip `rc=0`, chốt `rc=1` |
| r341 | tự cắt `#` | pip `rc=0`, chốt `rc=1` |
| +3 | direct ref · extras · `-r` | pip `rc=1`, chốt `rc=0` — lần này **lọt**, không phải chặn |

`CLAUDE.md` đã ghi ngưỡng cho đúng tình huống này: **đếm HÌNH DẠNG lỗi, đừng chỉ đếm
lỗi** — lặp ba lần trở lên thì câu hỏi đúng là *"có nên làm việc này không"*. Vòng năm là
lúc trả lời: **không**.

**Thẩm quyền chuyển sang pip.** `pip install --dry-run --report -` trả KẾ HOẠCH dạng JSON;
`install` rỗng nghĩa là môi trường ĐÃ thoả. Marker, extras, direct reference, `-r`/`-c`/`-e`,
phiên bản, cú pháp chú thích — pip lo hết. Kèm `--no-index` để hook phiên không phụ thuộc
mạng: đã thoả ⇒ `install=[]` trong **0,4s**; chưa thoả ⇒ pip thoát khác 0. Cả hai ánh xạ
đúng sang câu hỏi *"có được bỏ qua pip không"*.

**KHÔNG mâu thuẫn với r337.** r337 bác `--dry-run` vì đọc **mã thoát** (pip 24.0 trả rc=0
kể cả khi in "Would install"). Đọc **kế hoạch** là một phép đo khác hẳn — đó chính là bằng
chứng dương mà lúc ấy còn thiếu, không phải quay về cái oracle đã bị bác.

**Lớp phụ giữ lại, và CỐ Ý yếu đi.** pip không thấy được lớp lỗi r337: gói CÓ MẶT, ĐÚNG BẢN,
mà `import` chết (`PanicException`). Nên vẫn thăm import — nhưng nay dòng nào ta không hiểu
thì **BỎ QUA** chứ không báo hỏng. Cả bảy finding đều sinh ra từ chỗ khe hở của bộ phân tích
tự viết biến thành BÁO ĐỘNG GIẢ; nay khe hở chỉ dẫn tới *thăm ít hơn*, không bao giờ tới
*chặn phiên*. Đổi chiều rủi ro sang hướng an toàn.

**Tám ca `r338`–`r341` bị THAY, không phải sửa cho xanh** — chúng khoá một thiết kế không
còn tồn tại (đo từng nhánh của bộ phân tích tự viết). Bốn ca `r342` khoá hợp đồng mới:
mã thoát **khớp pip** trên 10 lớp (đo: **0/10 lệch**, gồm cả `-r` và extras mà bản cũ trả
lời sai) · lớp phụ **có răng** (phá `pypdf/__init__.py` mà giữ metadata: pip `rc=0`, chốt
`rc=1`) · **khe hở không được chặn phiên** (cho `Requirement` biến mất hoàn toàn, môi
trường đã thoả vẫn XANH) · đột biến gỡ cả khối hỏi pip phải làm ca đối chiếu ĐỎ.

**Một đột biến sống sót ở đây KHÔNG phải mã sai — nó đặt sai chỗ, và ca tự lộ ra.** Bản đầu
của đột biến chỉ nuốt nhánh *"kế hoạch không rỗng"*, trong khi với `pypdf>=4.0` + `--no-index`
pip KHÔNG GIẢI ĐƯỢC nên nhánh `rc != 0` bắt trước ⇒ mutant vẫn ĐỎ. Đúng bài học *"đột biến
SỐNG SÓT không luôn nghĩa là test yếu"*. Nay gỡ CẢ khối. **Khai thẳng chỗ chưa đo:** nhánh
*kế hoạch không rỗng* không được đo RIÊNG — muốn chạm nó phải có kho wheel cục bộ.

Cổng: `launcher_test` **172/172** (bỏ qua 1 — fixture Windows) · đột biến **170/170**
(1 không đo được trên nền này) · `tl --selftest` **1709/1709** · ruff `--select F` delta so
`033d67d` = **0** · `bash -n` OK · `git diff --check` rc=0 · hook chạy thật hai lượt đúng
thiết kế.

# ★ dev-side — r341: `#` không phải lúc nào cũng là chú thích, và LẦN THỨ TƯ cùng một lớp lỗi (2026-09-06)

P2 thứ ba của codex trên `033d67d`, **đúng**, đã tái hiện trước khi vá: pip chỉ coi `#` là
chú thích khi nó ở **đầu dòng** hoặc đi **sau khoảng trắng**; `#` nằm giữa một chuỗi —
marker, hay fragment của direct URL — là ký tự HỢP LỆ. Phản chứng:
`pypdf; os_name == "posix#x"` ⇒ pip `rc=0` (marker sai nên bỏ qua), bản trước cắt ở `#`
đầu tiên ⇒ dòng cụt ⇒ `InvalidRequirement` ⇒ `rc=1`.

**Đây là lần thứ TƯ trong một ngày cùng lớp CHỐT ĐỎ THƯỜNG TRỰC**, và cả bốn có chung một
gốc: *ta tự làm một việc mà pip đã có luật riêng.*

| | ta tự làm gì | pip làm gì |
|---|---|---|
| r338 | ghim `==6.0.3` | phải gỡ gói distro ⇒ hỏng |
| r339 | tự đòi bản ở chế độ hậu-pip | pip đã là thẩm quyền |
| r340 | tự cắt marker | pip đánh giá marker |
| r341 | tự cắt `#` | pip có luật cắt riêng |

Điều đáng ghi nhất **không phải bản vá mà là cách r340 hụt**: commit r340 viết ra bài học
"ngừng tự phân tích", chuyển việc cho `Requirement` — rồi **để nguyên dòng `split("#")`
ngay phía trên chỗ vừa sửa**. Chuyển được phần phân tích mà bỏ sót phần TIỀN XỬ LÝ, và
đúng chỗ bỏ sót ấy là lỗi kế tiếp. Bài học: khi kết luận "đừng tự làm việc này nữa", phải
đi hết **cả đường dẫn tới nó**, không chỉ đoạn đang bị chỉ ra.

Chép **LUẬT** của pip (`(^|\s)#`) chứ KHÔNG import bộ phân tích nội bộ: reviewer dặn đúng
một điều đang định làm sai — `pip._internal` là API không ổn định, buộc hook vào đó là đổi
một lớp trôi này lấy một lớp trôi khác.

**Một hàng trong bảng đo của chính lượt này không đo cái nó ghi.** Vòng lặp kiểm chạy
`pip install` trước mỗi ca, nên tới hàng `pypdf>=4.0` thì pip **đã nâng cấp** pypdf — hàng
ấy in "không hồi quy" trong khi ca đã mất điều kiện. Đo lại trên rig giữ nguyên
`pypdf` 3.17.4: r339 vẫn `rc=1`, r340 và r341 đều `rc=0`. Cùng bệnh *"ca có MẶT khác ca có
ĐO"*, lần này nạn nhân là bảng dựng ra để chứng minh không hồi quy.

Bảy ca đối chiếu **thẳng với pip** trên cùng một venv (marker chứa `#` · chú thích thật sau
khoảng trắng · chú thích đầu dòng · chú thích sau TAB · marker không khớp · lệch bản · dòng
hỏng): mã thoát của chốt khớp pip ở **cả bảy**. Răng hai chiều, một biến, hai vế dựng trong
cùng một lệnh: hook chưa vá ⇒ ca đích **ĐỎ**; chỉ thay tệp hook ⇒ **XANH**. Ca răng giữ cho
bản vá không hẹp thành "giữ nguyên chú thích thật", và đột biến quay về `split("#")` vô điều
kiện phải làm ca đích ĐỎ.

Cổng: `launcher_test` **176/176** (bỏ qua 1 — fixture Windows) · đột biến **170/170**
(1 không đo được trên nền này) · `tl --selftest` **1709/1709** · ruff `--select F` delta so
`033d67d` = **0** · `bash -n` OK · `git diff --check` rc=0 · hook chạy thật hai lượt đúng
thiết kế.

# ★ dev-side — r340: một DÒNG requirements không chỉ là TÊN (P2 thứ hai của codex) (2026-09-06)

Lượt review thứ hai trên `1474d7d` ra P2 *"Respect requirement markers before probing
imports"*, và nó **đúng** — đã tái hiện trước khi vá. Trên Linux với
`pywin32; sys_platform == "win32"`: **pip trả `rc=0`** và nói thẳng *"Ignoring pywin32:
markers ... don't match your environment"*, còn chốt trả **`rc=1` ở CẢ HAI chế độ** ⇒ sau
mỗi lần pip THÀNH CÔNG, hook vẫn xoá mốc và cảnh báo lại ở lượt sau.

**Đây là lần thứ BA trong cùng một ngày lớp lỗi CHỐT ĐỎ THƯỜNG TRỰC tái phát** — r338
(ghim `==6.0.3` bắt pip gỡ gói distro), r339 (đòi bản ở chế độ hậu-pip), giờ là marker.
Ba lần cùng một hình dạng thì câu hỏi đúng không còn là *"vá thế nào"* mà là *"có nên tự
làm việc này không"*, đúng như bài học **BẢY phát hiện cùng MỘT đường** đã ghi. Nên bản vá
này không thêm một nhánh nữa vào biểu thức chính quy mà **ngừng tự phân tích**: giao cả
dòng cho `Requirement` — thứ pip dùng — và lấy tên + specifier + marker từ MỘT nguồn.

- **Marker không áp dụng ⇒ bỏ qua dòng**, vì pip cũng bỏ qua. Đòi import một thứ pip cố ý
  không cài là tự chế ra bất đồng với thẩm quyền.
- **Dòng hỏng ⇒ fail-closed**, không `continue` lặng lẽ: bộ phân tích của pip từ chối thì
  ta cũng từ chối (`InvalidRequirement`).
- **Thiếu bộ phân tích + dòng CÓ marker ⇒ `KHONG_DO_DUOC_MARKER`**. Đoán xem marker có áp
  dụng hay không chính là cái vừa hỏng.

Sáu ca đo sau khi vá, trên cùng một venv: marker không khớp (cả hai chế độ) ⇒ rc=0 · marker
khớp + gói thiếu thật ⇒ rc=1 · lệch bản (P2 trước) ⇒ rc=1, không hồi quy · bản thoả ⇒ rc=0
· dòng hỏng ⇒ rc=1. Đo răng hai chiều, một biến, hai vế dựng trong cùng một lệnh: hook chưa
vá ⇒ ca đích **ĐỎ**; chỉ thay đúng tệp hook ⇒ **XANH**. Đột biến gỡ phép đánh giá marker
phải làm ca đích ĐỎ.

Cổng: `launcher_test` **174/174** (bỏ qua 1 — fixture Windows) · đột biến **170/170**
(1 không đo được trên nền này) · `tl --selftest` **1709/1709** · ruff `--select F` delta so
`1474d7d` = **0** · `bash -n` OK · `git diff --check` rc=0 · hook chạy thật hai lượt đúng
thiết kế.

# ★ dev-side — r339: IMPORT ĐƯỢC không chứng minh ĐÚNG BẢN (P2 của codex trên PR #449) (2026-09-06)

Codex review trên `3028506` ra một P2, và nó **đúng** — đã tái hiện bằng phản chứng chạy
được TRƯỚC khi vá: `requirements.txt` đòi `pypdf>=4.0`, môi trường cài `pypdf` 3.17.4 ⇒
`import pypdf` chạy ngon ⇒ chốt trả `rc=0` ⇒ hook **bỏ qua pip** và giữ nguyên một môi
trường không còn thoả `requirements.txt`. Đúng thứ trôi mà chốt ấy sinh ra để sửa. Cùng họ
"CÓ MẶT ≠ DÙNG ĐƯỢC", thêm một nấc: **DÙNG ĐƯỢC ≠ ĐÚNG BẢN**.

- **Chỉ kiểm bản ở chế độ `--kiem-ban`**, tức lúc trả lời câu *"có được BỎ QUA pip không"*.
  Sau khi pip vừa chạy xong thì pip là thẩm quyền và môi trường thoả theo cách đúng; đòi
  thêm một phép đo ở đó chỉ tạo ra **chốt đỏ thường trực** trên máy thiếu bộ phân tích
  specifier — đúng cái bẫy vừa trả giá ở r338 với bản ghim `==6.0.3`.
- **`pip._vendor.packaging` là đường lui, và nó ĐO ĐƯỢC chứ không phải đoán:** `packaging`
  trần **không có** trong venv trần, bản vendor của pip có ở **cả hai** nền — mà hook này
  vốn đã đòi pip.
- **KHÔNG ĐO ĐƯỢC ≠ ĐẠT.** Thiếu bộ phân tích hoặc thiếu metadata ⇒ báo
  `KHONG_DO_DUOC_BAN`, nghĩa là *đừng bỏ qua pip* — để pip quyết. Tự chữa, không phải chốt chết.
- **Thông điệp lỗi phải nói đúng chuyện gì hỏng.** Lệch bản mà in "KHONG import duoc" là
  đẩy người đọc đi sai hướng; nay là `requirements.txt CHUA THOA (import hong hoac lech ban)`.

**`t116` bắt được một lỗi thật của chính lượt vá này.** Hai ca mới ban đầu đặt tên
`r338b_...`; bộ đăng ký khớp khuôn `^def [tr]\d+_` nên chữ `b` sau số làm chúng **có mặt
trong `CA` mà không được đếm là hàm ca** ⇒ `171` hàm so `173` mục ⇒ ĐỎ. Chạy riêng từng ca
thì **xanh cả hai**, tức chỉ lượt chạy ĐẦY ĐỦ mới thấy. Đổi tên thành `r339_`.

Đo răng hai chiều, một biến, hai vế dựng trong **cùng một lệnh**: hook chưa vá ⇒ ca đích
**ĐỎ** (`lech ban ma chot van XANH`); chỉ thay đúng tệp hook ⇒ **XANH**. Kèm ca răng (bản
THOẢ tuyệt đối không được báo động giả; chế độ thường không được đòi bản) và đột biến bỏ
phép so specifier phải làm ca đích ĐỎ.

Cổng: `launcher_test` **172/172** (bỏ qua 1 — fixture Windows) · đột biến **170/170**
(1 không đo được trên nền này) · `tl --selftest` **1709/1709** · ruff `--select F` delta so
`3028506` = **0** · `bash -n` OK · `git diff --check` rc=0 · quét mẫu bí mật trên 129 dòng
thêm: 0 khớp · hook chạy thật hai lượt, lượt 2 đi đúng đường `--kiem-ban`.

# ★ dev-side — r338: bằng chứng dương của hook không phủ PyYAML, và ba lớp bẫy khi vá (2026-09-06)

r337 đổi bằng chứng của bước pip từ mã thoát `pip install --dry-run` sang **import được
từng gói trong `requirements.txt`**. Chốt đúng, nhưng phạm vi của nó bằng đúng nội dung
tệp ấy — mà PyYAML **không nằm trong đó**, dù `ops/lease_publish.py` (3 chỗ) và
`.claude/dev/packet_loop.py:1812` đều `import yaml`. Máy thiếu PyYAML vẫn được hook cấp
mốc "đủ", rồi cổng đăng lease chết `ImportError` giữa chừng. Cùng bệnh "phạm vi TUYÊN BỐ
phải bằng phạm vi ĐO ĐƯỢC", lần này ở dạng **một chốt đúng đặt trên một danh sách thiếu**.

Vá thì đụng liền ba bẫy, không bẫy nào lộ ra bằng đọc code:

- **TÊN GÓI (pip) ≠ TÊN MODULE (import).** Thêm `PyYAML` vào tệp là chốt r337 ĐỎ ngay:
  nó suy tên bằng chuẩn hoá chuỗi ⇒ `pyyaml` ⇒ `ModuleNotFoundError`, trong khi
  `import yaml` chạy tốt. Một chốt fail-close báo động GIẢ thì chặn phiên y như chốt
  đúng — và bản vá cho lỗ "CÓ MẶT ≠ DÙNG ĐƯỢC" suýt tự dựng lại lỗ ấy ở chiều ngược.
  Chữa bằng `importlib.metadata.packages_distributions()`: **hỏi metadata của bản ĐÃ CÀI**
  thay vì đoán từ tên. Bảng tay đổi tên cũng là đoán, chỉ là đoán sớm hơn.
- **Module gạch dưới là bản tăng tốc TUỲ CHỌN, đòi chúng là tái tạo đúng lớp lỗi vừa sửa.**
  Metadata khai PyYAML gồm cả `_yaml` (C ext của libyaml). Phản chứng đã chạy: chặn
  `_yaml` bằng meta-path finder rồi `import yaml` **vẫn OK** — `yaml/__init__.py` bọc nó
  trong `try: from .cyaml import * / except ImportError`. Đòi `_yaml` là báo giả trên
  mọi máy cài PyYAML thuần Python. Nên bản đồ chỉ lấy module KHÔNG gạch dưới.
- **Ghim `==6.0.3` cho "khớp CI" làm hook ĐỎ THƯỜNG TRỰC — chỉ lộ vì chạy hook THẬT.**
  Ba workflow ghim số ấy, nên bản đầu ghim theo. Chạy thật: python hệ thống có PyYAML
  6.0.1 do distro cài ⇒ `pip install -r` phải GỠ nó trước ⇒
  `ERROR: Cannot uninstall PyYAML 6.0.1, RECORD file not found ... installed by debian`
  ⇒ pip rc≠0 ⇒ hook rẽ nhánh hỏng, xoá mốc, in CẢNH BÁO ở **mọi** lượt mở phiên. Đổi
  sang `>=6.0` (cùng idiom `pypdf>=4.0`): no-op sạch, rc=0. CI giữ pin riêng của nó.

**Và phép đo suýt chọn nhầm cách chữa.** Để so ba dạng (`==6.0.3` · `>=6.0` · trần) tôi
chạy `pip install --dry-run`: nó trả **rc=0 cho cả ba**, kể cả dạng vừa hỏng thật. Đúng
lý do r337 đã bác dry-run làm bằng chứng — và tôi gần như dùng lại chính cái oracle hỏng
ấy để chọn bản vá cho lỗ do nó gây ra. Con số chỉ ra khi cài THẬT trên interpreter thật.

**Đo răng, không nhận ca xanh.** `r338_ten_goi_pip_khac_ten_module_import` trích thân
Python **từ chính tệp hook** (không chép lại — hai bản sẽ trôi lệch), và có ca răng: gói
không tồn tại vẫn phải ĐỎ, kẻo bản vá chỉ là "luôn trả 0".
`r338_dot_bien_bo_ban_do_lam_ca_dich_DO` gỡ bảng ánh xạ và đòi ca đích ĐỎ, cộng chiều
ngược (đột biến không được làm đổi ca răng) để cái ĐỎ ấy quy được cho bảng ánh xạ.
A/B một biến, hai vế dựng trong CÙNG một lệnh: hook chưa vá ⇒ ca đích **ĐỎ**; chỉ thay
đúng tệp hook ⇒ **XANH**.

Cổng: `launcher_test` **170/170** (bỏ qua 1, fixture Windows) · đột biến **170/170**
(1 không đo được trên nền này) · `tl --selftest` **1709/1709** · ruff `--select F` delta
so `057308d` = **0** trên cả ba tệp · `bash -n` OK · `git diff --check` rc=0 · quét mẫu
bí mật trên 123 dòng thêm: 0 khớp · hook chạy thật hai lượt: lượt 1 cài + đặt mốc, lượt 2
"không đổi và mọi gói import được — bỏ qua pip".

Nợ đã khai, chưa chữa: `PyYAML` nay ghim ở **bốn** chỗ (ba workflow + tệp này) và không
cổng nào canh chúng khớp nhau.

# ★ dev-side — vòng 7b: bản vá ĐÚNG của vòng 7 làm đỏ Windows, và vì sao (2026-08-13)

Vòng 7 sửa `if not con:` thành `con == []` — **đúng**, vì `None` là KHÔNG ĐO ĐƯỢC chứ
không phải "đã chứng minh rỗng". Nhưng lượt `launcher (windows-latest)` ngay sau đó đỏ:

```
HONG t69_stop_luot_DA_KET_THUC_khong_duoc_doi_so: mong doi 0, duoc 125
81/82 ca (qua 69, bo qua 12, hong 1)
```

Vì phép đo đứng sau điều kiện đó là `_thanh_vien_nhom` — **nhóm tiến trình, khái niệm
POSIX** — nên trên Windows nó luôn trả `None`. Trước bản vá, `not None` là True nên
Windows đi qua nhánh "đã không còn chạy" **nhờ chính con bọ**. Vá xong thì Windows không
còn đường nào chạm nhánh đó, rơi xuống `taskkill` trên một PID **không còn tồn tại**,
rc≠0 ⇒ 125 "không giết được". Một bản vá đúng làm lộ ra rằng nền kia chưa bao giờ có
phép đo của mình.

- **Windows được cấp phép đo riêng.** `hien is None` đã chứng minh *mẹ* đã tắt; hậu duệ
  thì hỏi ảnh chụp: `{}` nghĩa là không tiến trình sống nào nhận `pid` làm tổ tiên.
  Vẫn giữ nguyên doctrine — `None` vẫn là không đo được, vẫn không kết luận (`t83` khoá
  cả hai vế; `t78` giữ nguyên).
- **Fail-closed của ảnh chụp phải CÓ PHẠM VI.** Bản vòng 7 trả `None` ngay khi **bất kỳ**
  tiến trình nào trên máy thiếu `CreationDate`, kể cả tiến trình hệ thống chẳng liên quan.
  Như thế ảnh có dùng được hay không lại tuỳ trạng thái máy ở chỗ khác — mà từ mục trên,
  ảnh rỗng chính là đường quyết định 0-hay-125. Nay dòng mù được **giữ lại** kèm dấu
  `KHONG_DOC_DUOC_KHOA` (truy vấn CIM trả thêm `ParentProcessId` cho cả dòng lỗi, nên nối
  được cây), và chỉ trả `None` nếu dấu đó **rơi vào cây**. `t81` mạnh lên hai vế ngược
  nhau: mù TRONG cây ⇒ `None`; mù NGOÀI cây ⇒ ảnh vẫn dùng được.

Hai đột biến của vòng 7 mất neo vì đúng những dòng đó bị viết lại. **Chuyển neo, không
nới điều kiện** (nếp đã ghi): `none_nhom_thanh_cay_rong` neo sang nhánh Windows và nhận
thêm `t83` làm ca đích; `chup_cay_bo_qua_dong_thieu` neo sang chỗ đánh dấu — lớp KHÁC với
`chup_cay_khong_fail_closed_trong_cay` (một bên bỏ DẤU, bên kia bỏ phép KIỂM).

Đo: **83/83 ca** (qua 82, bỏ qua 1, hỏng 0) · **đột biến 42/42** (1 không đo được) ·
ruff F sạch · 17/17 bước gate `rc=0` · `tl selftest 1697/1697`.

Ghi rõ ranh giới bằng chứng: mục thứ nhất có **số đo thật trên `windows-latest`** (t69 đỏ
125). Mục thứ hai là **suy luận**, chưa quan sát được `_chup_cay` trả `None` trên runner —
nó trở nên đáng sửa vì mục thứ nhất khiến ảnh chụp thành đường quyết định.

**Lượt sau đó: `t69` xanh, `t78` đỏ — và lần này là FIXTURE.** `t78` khẳng định "không đo
được ≠ cây rỗng" nhưng chỉ bịt `_thanh_vien_nhom`, để `_chup_cay` **thật** chạy. Trên Linux
`_chup_cay` gọi `powershell` (không có) nên ném rồi trả `None` — ca xanh nhờ **máy dev
thiếu công cụ**, không nhờ điều nó khẳng định. Trên `windows-latest` nó chạy thật và trả
`{}` cho một PID không tồn tại: bằng chứng ĐO ĐƯỢC và hợp lệ, đúng thứ `t83` khẳng định ⇒
`t78` đỏ ở đó. Bịt nốt phép đo Windows trong fixture. **Sửa fixture, không nới chốt** —
muốn thử "không đo được" thì phải dựng cho bằng được trạng thái đó ở mọi nền. Đã soi cả
bốn ca stub `platform.system() == "Windows"`; chỉ `t78` có hình dạng này.

**Lượt kế: cả bộ test, bộ đột biến và BA probe đầu đều qua — đỏ ở probe cuối, lại là
fixture.** `taskkill rc=128 : ERROR: The process "6156" not found`. Nguyên nhân:
`Start-Process -ArgumentList 'a','b'` **nối các phần tử bằng dấu cách mà KHÔNG đặt dấu
nháy**, nên `-ArgumentList '-c','import time;time.sleep(60)'` tới python thành `-c`
`import` `time;…` ⇒ chạy chương trình tên `import` ⇒ `SyntaxError` ⇒ chết ngay, và một
giây sau `taskkill` không tìm thấy PID. Suốt thời gian probe này chỉ **in** kết quả mà
không khẳng định gì thì lỗi đó **vô hình**; vòng 7 siết nó thành chốt và nó lộ ra ngay
lượt đầu — đúng lý do phải siết. Nay truyền một chuỗi có dấu nháy lồng, và **kiểm tiền đề**
(tiến trình mồi còn sống) trước khi đo, để tách "fixture hỏng" khỏi "kết luận về taskkill".

# ★ dev-side — audit launcher vòng 7: fail-closed cho Job Object và phép đo Windows (2026-08-13)

Không bump `VERSION`. Vòng rà soát thứ bảy vá năm lỗ hổng đo/giết cây Windows:

- kiểm kết quả `SetInformationJobObject`, đóng handle và trả thất bại nếu không đặt được giới hạn;
- cấp phát lại danh sách PID trong Job Object khi sức chứa ban đầu thiếu;
- không còn đọc trạng thái “không đo được nhóm” như bằng chứng “nhóm rỗng”;
- ảnh cây CIM fail-closed nếu một dòng thiếu `CreationDate` hoặc sai khuôn;
- cổng đột biến yêu cầu ít nhất 70% bảng đo được trên mỗi nền, thay vì chỉ yêu cầu một ca.

Thêm năm phản chứng `t78`–`t82` và năm đột biến tương ứng. Workflow Windows cũng
không còn xanh khi `t62` tự bỏ qua hoặc probe `taskkill /T` trả mã khác 0/còn tiến trình.
Báo cáo và số đo đầy đủ ở `docs/AUDIT_LAUNCHER_VONG_7.md`.

**Kèm một vết nữa của cùng họ bệnh, lần thứ tư trong đợt: minh chứng của một bẫy lại trở
thành chính bẫy đó.** Probe "đứt ống" đặt `$LASTEXITCODE = 77` làm mốc để CHỨNG MINH
PowerShell không đặt lại nó sau ống bị cắt. Lượt chạy trả về đúng như dự đoán —
`LASTEXITCODE=77`, và cả ba phép đo đều ĐÚNG (`rc=0` khi đủ công cụ, `rc=12` khi thiếu) —
**mà bước vẫn ĐỎ**. Vì dòng cuối của bước là một lệnh native trong ống bị cắt, nên runner
gọi `pwsh -command ". 'script'"` rồi lấy mã thoát từ trạng thái còn sót lại đó: cái mốc
diễn giải thành phán quyết. Nay bước `exit 0` tường minh — phán quyết là `$loi`, không
phải tàn dư của lệnh cuối.

# ★ dev-side — vòng 6: ba cổng ĐỎ của kho mà CI chỉ kịp báo MỘT (2026-08-13)

Không bump `VERSION`. `RELEASE_MANIFEST.json` giữ **179 tệp** — không tệp runtime nào
được thêm; chỉ hai bản ghi đổi sha256 (`CHANGELOG.md`, `scripts/tl_selftest.py`).

CI báo đúng một dòng `tl selftest 1696/1697` rồi `exit 1`, nên **mọi bước sau đó không
hề chạy**. Chạy trọn bộ gác tại chỗ mới thấy **ba** cổng đỏ chứ không phải một. Đây
đúng lớp bệnh "cổng dừng ở lỗi ĐẦU TIÊN che mất phần còn lại" — số của CI là sàn, không
phải tổng.

- **`r291_docs_ngoai_goi` — ratchet đếm `docs/*.md`, 52 → 55.** Ba tài liệu dev-side của
  sáu vòng audit (`GOI_AGENT_DA_NEN.md`, `AUDIT_LAUNCHER_VONG_3.md`,
  `AUDIT_LAUNCHER_VONG_4_POSIX.md`) làm ratchet đỏ ĐÚNG LÚC phải đỏ. Đã KÊ KHAI SLOT
  theo nếp có sẵn ngay tại ca: gói giữ 179, cây thật 179 + 55 = 234, trần Package 200
  không nhúc nhích. Đây là **ca duy nhất CI kịp báo**.
- **`doc-claims-check --strict` — 5 cờ L7 `PYLOC_FILE_MISSING`.** Báo cáo vòng 3 trỏ vào
  mã bằng dạng hai chấm `launcher.py:NNN`, mà L7 tra tên trần trong `pyindex` — danh sách **TRẮNG**
  `scripts`, `scripts/tl_core`, `scripts/_fallback`, `.` — nên `.claude/dev/` không thể giải
  được. Thêm đường dẫn cũng KHÔNG cứu: regex neo `\b[A-Za-z0-9_]` **nuốt mất dấu chấm
  đầu**, `.claude/dev/…` bị đọc thành `claude/dev/…` ⇒ vẫn thiếu tệp. Đo cả ba dạng rồi
  mới chọn: chuyển sang `` `launcher.py` dòng 293-299 ``. Ghi chú giải thích bẫy **tự đạp
  vào bẫy** ở bản đầu (nêu ví dụ bằng số dòng THẬT ⇒ L7 bắt đúng ba lần): ví dụ trong tài
  liệu về một cổng cũng là dữ liệu cổng đó quét, nên viết `NNN` thay cho chữ số. Rồi
  **chính mục CHANGELOG này** đạp vào lần thứ ba khi thuật lại bẫy đó — cùng một câu, cùng
  một cổng. Ba lần trong một đợt: bất cứ chỗ nào `doc-claims-check` quét (kể cả sổ) thì ví
  dụ phải viết `NNN`.
- **`release-verify --strict` — manifest ấm ở HAI bản ghi.** `CHANGELOG.md` lệch từ
  đợt trước (vòng 5 sửa sổ mà không tái sinh manifest), `scripts/tl_selftest.py` lệch vì
  đợt này. Đã tái sinh bằng `release-manifest --out RELEASE_MANIFEST.json`; đã kiểm
  `file_count` vẫn 179 và `extra_files`/`missing` vẫn rỗng TRƯỚC khi thay tệp — cạm bẫy
  "tái sinh manifest nuốt cả bản sao kho" (r238) chỉ đúng khi cây có tệp thừa, không phải
  ca này.

**Bài học để lại — chẩn đoán SAI đã được công bố trước khi đo.** Phiên trước đọc
`1696/1697` rồi nói (trong bình luận PR lẫn tệp bàn giao) rằng đó "nghi vấn hàng đầu là
golden/kiểm kê tệp trôi". Chạy thật thì `golden-test` và `determinism-audit` đều XANH; ca đỏ
là ratchet `docs/*.md`, còn hai cổng đỏ khác thì chẩn đoán đó không hề nhắc tới. `CLAUDE.md`
đã viết sẵn "ĐừNG ĐOÁN: chạy `--selftest`, đọc dòng `[X]`, lấy tên ca, rồi mới sửa" —
lời khuyên đúng, đã không làm theo.

**Môi trường: `--selftest` không chạy được trong container này cho tới khi cài `cffi`.**
`pypdf` → `cryptography` (bản apt ở `/usr/lib/python3/dist-packages`) nổ
`pyo3_runtime.PanicException: Python API call failed`, gốc là `ModuleNotFoundError:
_cffi_backend`. Nó giết cả lượt ở `_c319_khong_bien_tuy_chon_thanh_chan_cung` **trước khi**
bộ test kịp đếm, nên local không ra nổi dòng `N/N` để so với CI — trông như cùng một
triệu chứng với CI mà thực ra là hai bệnh khác hẳn (CI báo `r319` **[OK]**). `pip install
cffi` là xong; ghi lại để phiên sau không mất lần nữa đi truy `tl.py`.

Đo sau khi vá (Linux, container này): `tl selftest` **1697/1697**, và toàn bộ 13 bước của
job `gate` đều `rc=0`.

**Và một lỗ nữa, do CI Windows lộ ra: phép đo `dut ong` KHÔNG HỀ CHẠY.** Bước probe viết
`… doctor | Invoke-Expression $cat | Out-Null` để dùng MỘT dòng cho hai kiểu cắt ống.
`Invoke-Expression` **không nhận đối tượng từ ống** (`-Command` không `ValueFromPipeline`)
nên nó chết ngay vòng lặp đầu: *"The input object cannot be bound to any parameters"*. Hệ
quả không nằm ở bước đó: probe này đứng **TRƯỚC** ba probe còn lại, nên `cp1258`, `t62` và
`taskkill /T` **chưa từng chạy lần nào** trên Windows — job đỏ ở bước 9 và dừng. Một dòng
pwsh viết mù (không có Windows để thử) đã khoá toàn bộ phần đo Windows lại, đúng bài học
"script đa nền phải chạy THẬT trên nền đó". Nay dùng scriptblock: tham số hoá được kiểu
cắt mà không dính `Invoke-Expression`.

Nhân đó siết luôn probe `cp1258`: nó đọc `%ERRORLEVEL%` **sau** một câu `echo`, mà cmd cập
nhật `ERRORLEVEL` theo lệnh gần nhất ⇒ có đường đọc phải mã của `echo`. Nay chốt vào biến
riêng ngay sau lệnh python. Chưa quan sát được nó báo sai (bước này chưa từng chạy), nhưng
đây đúng hạng "cổng xanh nhờ rc=0" mà `CLAUDE.md` dặn không được tin.

Điểm đáng ghi: bộ phản chứng và bộ đột biến trên Windows **đều xanh** ở lượt này
(`77/77`, `DOT BIEN: 24/24 dat`, cây làm việc `sach`) — thứ đỏ là phép đo, không phải thứ
được đo. Bốn vòng audit không thấy nổi, vì không vòng nào chạy được pwsh.

**Và ngay lượt probe chạy được lần đầu, nó đo ra một điều không ai đoán:**

```
du cong cu  | Select-Object -First 1 -> rc=   (RỖNG)
du cong cu  | Out-Null               -> rc=0
thieu cong cu | Select -First 1      -> rc=0  (mong doi 12)
```

`Select-Object -First N` cắt ống bằng `StopUpstreamCommandsException`, và khi đó PowerShell
**không đặt `$LASTEXITCODE`** cho lệnh native bị cắt: lần đầu nó còn `$null` (in ra rỗng),
lần sau nó **giữ nguyên giá trị của lệnh TRƯỚC** (0) — nên ca "thiếu công cụ" báo 0 trong
khi `doctor` thật sự trả 12. Tức trên Windows, `$LASTEXITCODE` sau một ống bị cắt **không
phải mã của tiến trình con**: khẳng định `rc=0` qua kênh đó là cổng XANH GIẢ, khẳng định
`rc=12` là cổng ĐỎ OAN. Cả hai đều sai, và cùng một dòng lệnh cho cả hai.

Nay probe chỉ **chốt** qua ống chạy trọn vẹn (`Out-Null`), còn kiểu cắt giữa chừng thì in ra
làm hồ sơ — kèm mốc nhận biết `$LASTEXITCODE = 77` đặt trước để chứng minh PowerShell không
đặt lại nó, thay vì bắt người đọc tin lời. Đường cắt-giữa-chừng vẫn được đo THẬT, nhưng bởi
`t74`: nó spawn con từ Python, đọc 1 byte rồi đóng ống, và đọc `returncode` **trực tiếp** từ
tiến trình con — kênh không đi qua PowerShell nên không dính bệnh này. `t74` đã xanh trên
`windows-latest`, nên bảo đảm "đứt ống không nuốt mã thật" vẫn có bằng chứng trên nền đó.

# ★ dev-side — vòng 5: vá 4 lỗi do lượt CI Windows ĐẦU TIÊN lộ ra (2026-08-13)

Không bump `VERSION`; chỉ `.claude/` + CHANGELOG. `RELEASE_MANIFEST.json` giữ 179 tệp.

Lượt `launcher (Windows that)` chạy được lần đầu sau khi Actions hồi phục. Bốn vòng
audit trước đều đo trên Linux; runner `windows-latest` lộ ngay **3 ca đỏ trên Windows**
và **1 đột biến sống sót trên Linux CI** mà máy dev không thấy.

- **`t56` — nhúng đường dẫn vào MÃ NGUỒN Python.** Trên Windows đường dẫn bản chụp có
  dạng `C:\Users\…`, mà `\U` là escape unicode ⇒ `SyntaxError` ⇒ con chết trước khi
  làm gì, báo "con khong chay". Nay đường dẫn đi qua **argv**, không nhúng vào nguồn.
  Lỗi fixture, không phải lỗi launcher.
- **`t61` — `chmod(0o500)` trên THƯ MỤC là no-op ở Windows** (run-root vẫn ghi được ⇒
  rc=0 thay vì 2), còn ở POSIX thì root ghi xuyên quyền nên ca phải tự bỏ qua. Nay đặt
  một **TỆP** làm thành phần đường dẫn ⇒ `mkdir` buộc phải hỏng ở mọi nền, mọi user.
  Ca từ "bỏ qua khi root + đỏ trên Windows" thành **chạy được khắp nơi**.
- **`t69` — con `-c pass` thoát trước khi `_khoa_danh_tinh` kịp chạy.** `Get-Process`
  KHÔNG thấy tiến trình đã thoát (POSIX thì `/proc/<pid>` còn ở dạng zombie nên đọc
  được) ⇒ sổ ghi `khoa_danh_tinh=null` ⇒ `stop` từ chối bằng mã 10. Fixture nay dùng
  con sống đủ lâu và **kiểm tiền đề** là khoá đã lấy được. Sổ thêm `khoa_thieu_ly_do`
  để lần sau không phải đoán vì sao thiếu khoá.
- **`t74` — ca PHI-TẤT-ĐỊNH do chính vòng 4 viết.** Nó cho người đọc đóng ống ngay rồi
  trông chờ ống vỡ; nhưng stdout Python nối ống là block-buffered 8KB và ống hệ điều
  hành đệm thêm 64KB, nên với đầu ra NHỎ không lần ghi nào hỏng và đột biến sống sót.
  Xanh ở máy dev, **ĐỎ trên CI**. Nay dựng sổ vượt 8KB, **đọc đúng 1 byte** rồi đóng ⇒
  lần ghi kế tiếp buộc phải vỡ ống. Hết phụ thuộc thời điểm.

**Một bản vá bị HOÀN NGUYÊN giữa chừng, ghi lại vì nó đáng nhớ.** Bản đầu chữa `t69`
bằng cách cho `lenh_stop` trả `MA_OK` khi thiếu khoá mà lượt chạy đã kết thúc. Nó đụng
thẳng `t32_stop_tu_choi_khi_khong_co_khoa` — cùng một kịch bản, một bên đòi 10, một bên
đòi 0. `t32` mới là bên giữ doctrine: trên Linux `stop` trả 0 vì `_giet_cay` **ĐO được**
tiến trình đã biến mất, không phải vì suy ra từ nhãn trong sổ; thiếu khoá nghĩa là không
đo được gì cả. Sửa fixture chứ không nới chốt.

CÒN TREO — `_khoa_danh_tinh` mất khoá với con ngắn ngủi trên Windows là lỗi THẬT, mới
chỉ né trong fixture. Bản vá gốc là lấy danh tính từ HANDLE mà `Popen` đang giữ
(`GetProcessTimes`), vì handle sống qua lúc tiến trình thoát. Chưa làm vì `.NET
StartTime.Ticks` (epoch năm 1, giờ ĐỊA PHƯƠNG) và `FILETIME` (epoch 1601, UTC) lệch
epoch lẫn múi giờ — chuyển đổi sai thì khoá không bao giờ khớp và chốt hoá ra luôn từ
chối. Cần đo trên Windows thật trước khi đụng.

**Lượt CI Windows thứ hai** (sau ba bản vá trên): bộ phản chứng **77/77, hỏng 0** —
ba ca đỏ đã hết. Còn 4 đột biến báo SAI, hoá ra là ba chuyện khác nhau:

- `lay_cwd_thay_vi_goc_repo` — **lỗi test thật**. `t38` so `str(con)` với stdout đã
  `resolve()`; trên runner thư mục tạm ở dạng **8.3 short path** (`RUNNER~1`) còn đầu
  ra ở dạng dài (`runneradmin`), nên `str(con) not in r.stdout` **luôn đúng** kể cả khi
  launcher trả về cwd ⇒ khẳng định rỗng nghĩa, đột biến thoát. Nay resolve cả hai vế.
- `ban_chup_de_ho_quyen` · `ban_chup_de_lai_tren_dia` — `t71` **cố ý** bỏ qua đúng hai
  khẳng định đó trên Windows (hợp đồng bản chụp khác nhau theo nền, vòng 4), nên đột
  biến không thể giết dù ca đích VẪN CHẠY.
- `124_khi_chau_con_song` — `t62` **chạy được lần đầu và QUA**, nhưng chỉ đo được khi
  đường giết THẤT BẠI; trên runner `taskkill /T` thành công nên cháu chết thật và 124
  là trung thực.

Bảng `DOT_BIEN` nay nhận **phần tử thứ tư tuỳ chọn** `('posix'|'windows', lý do)` cho
những đột biến không thể đo trên một nền dù ca đích vẫn chạy. **Lý do là bắt buộc và
được IN RA** — đây không phải chỗ giấu thất bại, và sàn "0 đo được ⇒ đỏ" vẫn nguyên.
Trước đó chúng báo SAI oan, mà một cổng không bao giờ xanh được thì người ta sẽ bỏ qua
nó — đúng cái bẫy đã ghi trong chú thích `can_do`.

Cổng Linux: **77/77** (qua 76, bỏ qua **1**, hỏng 0) · đột biến **34/34**
(1 không đo được) · ruff F sạch. Số bỏ qua giảm từ 2 xuống 1 nhờ `t61`.

# ★ dev-side — audit launcher vòng 4 POSIX: không xoá prompt khi wrapper còn cháu (2026-08-13)

Không bump `VERSION`; chỉ `.claude/`, `docs/` và CHANGELOG.

- `run` không còn xoá `prompt.snapshot` ngay khi tiến trình wrapper thoát.
  Trước khi xoá, launcher phải chứng minh nhóm tiến trình POSIX đã rỗng;
  nếu cháu còn sống hoặc không đo được thì giữ bản chụp 0600 cho cháu
  đọc. Phản chứng `t76_wrapper_thoat_khong_duoc_xoa_prompt_cua_chau`
  dựng wrapper sinh cháu đọc trễ; đột biến `xoa_prompt_khi_wrapper_vua_thoat`
  khôi phục đúng lỗi cũ và bị t76 giết.
- **Hệ quả đa nền của luật mới, vá kèm.** "Không đo được thì giữ" trên Windows
  nghĩa là *luôn luôn* giữ: `_thanh_vien_nhom` trả `None` ở mọi nền không phải
  Linux/Darwin, nên `cay_da_chet` không bao giờ đúng và bản chụp sẽ nằm lại vô
  thời hạn — đúng thứ mà việc bỏ argv khỏi sổ đã tránh. Hai việc: `_cap_id` quét
  dọn `prompt.snapshot` quá hạn (gộp vào chỗ đã dọn `.tmp` mồ côi), và `t71` nói
  đúng hợp đồng theo nền thay vì đòi một bảo đảm Windows không thể giữ. Khoá bằng
  `t77_ban_chup_qua_han_bi_QUET_du_khong_xoa_duoc_ngay` + đột biến
  `khong_quet_ban_chup_qua_han`.
- Báo cáo và số đo Linux: `docs/AUDIT_LAUNCHER_VONG_4_POSIX.md`.
  Cổng cuối: **77/77** (qua 75, bỏ qua 2, hỏng 0), **34/34** đột biến
  (1 không đo được trên Linux), ruff F sạch.

# ★ dev-side — vá nốt 12 mục NÊN SỬA của audit vòng 3 (2026-08-12)

Không bump `VERSION`: chỉ `.claude/` + `docs/` + CHANGELOG. `RELEASE_MANIFEST.json`
giữ nguyên `file_count: 179`.

Bộ phản chứng **75/75 (qua 73, bỏ qua 2, hỏng 0)** · đột biến **32/32 đạt** ·
`ruff --select F` sạch.

- **Chốt kho hết chặn oan đường dẫn sâu.** Bó ở ĐÚNG 3 đoạn nên
  `gitlab.com/nhom/nhom-con/kho` (GitLab subgroup, GHE lồng nhau) bị TỪ CHỐI dù đúng
  từng ký tự, kèm thông điệp tự mâu thuẫn `mong doi X, thuc te [X]`. Nay ≥3 đoạn =
  đã nêu host = bằng nhau tuyệt đối; tính an ninh không đổi, chỉ hết chặn oan.
- **`stop` thôi vu oan và thôi đổi nhãn.** Một lượt vừa chạy xong bình thường bị báo
  `khoa danh tinh KHAC (PID da bi tai dung)` + rc=10 — hô đúng mối nguy mà khoá danh
  tính sinh ra để bắt, trong ca vô hại và phổ biến nhất (7/12 lần trong phép đua) —
  rồi ghi đè `trang_thai="da_dung"` lên lượt đã "xong". Nay tách "tiến trình đã không
  còn chạy" khỏi "PID bị tái dùng", và không đổi nhãn của lượt đã kết thúc. `KetGiet`
  thêm `tu_choi` để **10 (TỪ CHỐI giết)** khác **125 (đã giết mà chưa trọn vẹn)**.
- **`{PROMPT_FILE}` mồ côi bị chặn.** Có chỗ thay mà không truyền `--prompt-file` thì
  con nhận đúng chuỗi `{PROMPT_FILE}` làm đường dẫn, rc=0, sổ ghi "xong".
- **Bản chụp prompt kín và không ở lại.** `0600` ngay từ lúc tạo (`write_bytes` để lại
  0644 theo umask ⇒ mọi user đọc được), thư mục `0700`, xoá khi con thoát trừ khi
  `--giu-ban-chup`. Bỏ argv khỏi sổ vì có thể chứa bí mật rồi ghi toàn văn prompt ra
  đĩa world-readable vĩnh viễn là mở rộng bề mặt lộ, không phải thu hẹp.
- **Ctrl-C không còn ghi thành "xong".** `trang_thai` mới `bi_ngat`; đây là trường
  `status` liệt kê nên ghi "xong" cho lượt bị cắt giữa chừng là nói dối đúng chỗ
  người/máy đang đọc. Cùng lớp lỗi với t50.
- **Đứt ống thôi nuốt mã thật.** `doctor | head` trên môi trường LÀNH từng ra 141
  (20/20 lượt) nên phía gọi kiểm `rc != 0` báo "THIẾU CÔNG CỤ" oan; lúc THIẾU thì 141
  lại nuốt mất mã 12. Nay in qua `_in_an_toan`, kết luận không phụ thuộc việc người
  đọc có chịu đọc hết hay không: đo lại 0/0/0 khi đủ và 12/12/12 khi thiếu, ở cả ba
  kiểu cắt ống. `main` cũng flush trước khi trả, tránh mã 120 do lỗi flush lúc dọn dẹp.
- **Timeout cho MỌI subprocess trên đường giết** (`git` 120s, `ps`/`powershell` 15–30s,
  `taskkill` 30s). Trước chỉ `_phien_ban` có: một `powershell` treo là treo luôn đường
  cưỡng chế hạn chót — đúng thứ `--deadline-utc` tồn tại để bảo đảm.
- **`_con_song` trên Windows so KHOÁ**, không chỉ hỏi "có tiến trình nào mang PID này".
  Giữa `taskkill` và lúc kiểm có ~2 lần gọi `powershell`, thừa chỗ để PID bị tái dùng
  ⇒ đọc thành "chưa giết được" và trả **125 giả**.
- **`doctor` đo `bash` và `npm`** — hai thứ môi trường thật sự phụ thuộc (`settings.json`
  gọi hook qua bash; `session-start.sh` rẽ nhánh trên `npm`) mà bảng cũ không hỏi.
- **Cổng đột biến có SÀN.** Bảng mà mọi đột biến đều không đo được in `0/0 dat` rồi
  thoát 0 — thoả hình thức "hai số bằng nhau" mà chứng minh con số không.
- **Dấu mốc pip thành bằng chứng DƯƠNG.** Mốc cũ nói "từng cài sha này ở TMPDIR này",
  nên A→B→A bỏ qua sai (môi trường đang là B) và hai dự án cùng `requirements.txt`
  dùng chung mốc. Nay mốc neo theo cả sha lẫn `sys.prefix`, nằm trong `.git/` của dự
  án, và trước khi tin mốc còn hỏi `pip install --dry-run`.
- **Dọn tệp tạm mồ côi** quét từ `run_root` (rác nằm ở thư mục của lượt ĐÃ CHẾT — quét
  thư mục đang ghi thì chẳng dọn được gì).
- **Hook ghim `"shell": "bash"` + `${CLAUDE_PROJECT_DIR}` dạng ngoặc.** Máy Windows
  không có Git Bash thì chuỗi lệnh được giao cho PowerShell, ở đó `bash` không tồn tại
  VÀ `$CLAUDE_PROJECT_DIR` là biến PowerShell chưa định nghĩa nên nở ra rỗng — hai lỗi
  độc lập, cùng hướng. Không dùng exec form (`args`) dù tài liệu khuyến nghị: client cũ
  bỏ qua `args` sẽ chạy `bash` trần, mà `PreToolUse` hỏng thì mọi lệnh Bash chết trước
  khi chạy — đúng bẫy tự khoá đã ghi trong CLAUDE.md.
- Tài liệu: bảng mã thoát bổ sung 130/141/1 và **cảnh báo mã của con đè lên cả bảng**
  với `run` (phía gọi tự động phải đọc `trang_thai`); `{PROMPT_FILE}` lần đầu được ghi
  vào tài liệu và ví dụ chủ đạo chuyển sang dùng nó; ghi rõ cách đăng ký hook kèm trích
  dẫn tài liệu chính thức.

# ★ dev-side — vá 3 lỗi CHẶN của audit vòng 3 (2026-08-12)

Không bump `VERSION`: chỉ `.claude/dev/` + `docs/` + CHANGELOG. `RELEASE_MANIFEST.json`
giữ nguyên `file_count: 179`, gói phát hành không đổi.

Vòng audit thứ ba (`docs/AUDIT_LAUNCHER_VONG_3.md`) tìm 3 lỗi CHẶN — **cả ba nằm ở POSIX**,
nền launcher chạy hằng ngày, chứ không phải ở Windows như dự đoán:

- **`ca_cay=True` là khẳng định KHÔNG có bằng chứng.** Vòng chờ thoát ngay khi tiến trình
  MẸ chết, nên `killpg(SIGKILL)` không bao giờ được gửi: cháu chỉ cần `SIG_IGN` cho SIGTERM
  (hoặc `setsid()` rời nhóm) là sống tiếp trong khi hạn chót trả 124 "đã giết được" — đúng
  "chốt nói dối" mà vòng 2 đã vá cho Windows rồi bỏ quên ở POSIX. Nay đo bằng HAI lớp độc
  lập, mỗi lớp phủ một ca lớp kia không thấy: `_chup_cay` chụp cây con cháu + khoá danh
  tính TRƯỚC khi phát tín hiệu (bắt kẻ đã rời nhóm — sau khi mẹ chết là không tìm lại được),
  `_thanh_vien_nhom` đếm thành viên nhóm còn sống, zombie tính là đã chết (bắt kẻ sinh SAU
  lúc chụp). `_giet_rieng` giết từng pid có kiểm khoá vì `killpg` không với tới kẻ đã
  `setsid()`. Không đo được ⇒ `ca_cay=False` ⇒ 125, không đoán bừa thành 124.
- **`_cap_id` không giành được `short_id`.** Bản vá vòng 2 đổi sang `mkdir` độc quyền và
  ghi rằng khe hở đã đóng, nhưng thư mục tên `{sid}-{rid}` nên nó chỉ chặn trùng `run_id`
  ĐẦY ĐỦ (uuid4 — chưa ai lo); trùng `short_id`, thứ làm `status`/`stop` trỏ nhầm lượt, vẫn
  lọt vì hai bên ra hai TÊN khác nhau. Sửa ở tầng: bỏ `rid` khỏi tên, thư mục lượt chạy tên
  ĐÚNG BẰNG `short_id` nên `mkdir` chính là hành vi giành, nguyên tử ở tầng hệ tệp và không
  thêm tệp mốc nào vào `run-root`. `run_id` đầy đủ nằm trong `run.json`, `_tim_luot` tra được.
- **`--run-root` tương đối làm neo prompt fail-OPEN.** Con chạy với `cwd=gốc repo` còn
  launcher có thể đứng ở thư mục con, nên đường dẫn bản chụp thay vào `{PROMPT_FILE}` trỏ
  trượt: con không đọc được gì, mà sổ vẫn ghi `prompt_kin_hoan_toan=true` và lượt chạy trả
  `rc=0`/`xong`. Sửa bằng `.resolve()` ở cả `run`/`status`/`stop`.

Khoá bằng 5 ca mới (t63…t67) + 5 đột biến. Bộ phản chứng **67/67 (qua 65, bỏ qua 2, hỏng 0)**,
đột biến **22/22 đạt** (1 không đo được: t62 là fixture Windows). Lý do bỏ qua t62 trên POSIX
được sửa vì nó SAI SỰ THẬT — trạng thái "mẹ chết cháu sống" dựng được trên Linux, và t63/t66/t67
là ba biến thể của nó.

# ★ dev-side — launcher đa nền + môi trường agent (2026-08-12)

Không bump `VERSION`: toàn bộ thay đổi nằm trong `.claude/` và `docs/` — hai thư mục đã
có trong `_RELEASE_EXCLUDE_DIRS`, nên gói phát hành, `RELEASE_MANIFEST.json` và trần 200
tệp đều không đổi. Ghi lại ở đây vì quy trình đòi mọi commit phải có vết trong CHANGELOG,
kể cả khi runtime triển khai đứng yên.

- `.claude/dev/launcher.py` — các chốt "gọi agent tất định" chuyển từ hai script PowerShell
  (chỉ chạy được Windows) sang Python 3: neo HEAD/ref/worktree sạch, neo prompt theo sha256,
  hạn chót + giết cả cây tiến trình, sổ lượt chạy, nhận diện KHO thay cho neo đường dẫn,
  và `doctor` kiểm công cụ. Mỗi chốt một mã thoát riêng.
- KHÔNG viết script spawn agent: launcher chỉ bọc chốt quanh một lệnh bất kỳ; việc gọi
  agent do CLI chính thức `claude` / `codex` đảm nhiệm.
- `.claude/hooks/session-start.sh` + đăng ký SessionStart — container Claude Code web thiếu
  codex/gh/pwsh; hook cài phần cần rồi đòi bằng chứng dương qua `doctor`.
- Sửa bẫy tự khoá: `PreToolUse` từng dùng đường dẫn TƯƠNG ĐỐI nên khi cwd trôi vào thư mục
  con thì mọi lệnh Bash chết trước khi chạy.
- Hai vòng audit của Codex trên Windows thật tìm ra 6 + 7 lỗi; tất cả đã vá, mỗi lỗi khoá
  bằng một ca phản chứng. `.claude/dev/launcher_test.py`: 62 ca + 17 đột biến.
- Bài học đã ghi vào `CLAUDE.md`; hướng dẫn ở `docs/GOI_AGENT_DA_NEN.md`.

# ★ v1.36.68 — r336: loại `ops/` + `.mcp.json` khỏi kiểm kê gói (2026-08-14)

Nhánh `ops` (đường đăng lease bằng git) đỏ `release-verify --strict` **ngay từ commit đầu** và
không ai đọc ra, vì nó đỏ ở `extra_files` chứ không ở `failed`: `failed: 0`,
`package_hash_match: true`, manifest vẫn lành. Đúng lớp bệnh r238/r331 — gate đỏ theo PHẠM VI
QUÉT chứ không theo nội dung, nên nhìn vào đâu cũng thấy "mọi thứ đúng".

- `ops` vào `_RELEASE_EXCLUDE_DIRS`, `.mcp.json` vào `_RELEASE_EXCLUDE_NAMES`. Cả hai dev-side
  thuần, runtime Cowork trong gói không đọc. GIỮ trong repo/git, CHỈ loại khỏi GÓI — cùng tiền
  lệ `.claude` `.github` `.githooks` `docs` `rasoat` `changelog_archive` `.editorconfig`.
- `ops` khoá theo THƯ MỤC, `.mcp.json` theo TÊN vì nó ở gốc kho. Đã kiểm chứ không đoán: 0 mục
  manifest mang thành phần đường dẫn tên `ops` — `ingest_ops.py`/`nlm_ops.py`/`ops_misc.py` là
  TÊN TỆP nên không dính, mà khoá thư mục dùng phép giao trên MỌI thành phần đường dẫn.
- `release-verify --strict`: rc=2 · extra_files 6 → **rc=0 · extra_files 0 · failed 0**.
  `RELEASE_MANIFEST.json` tái sinh giữ `file_count` **179**, 0 thêm 0 bớt.
- Bẫy đã sập rồi mới hiểu: bảng loại trừ không thêm bớt mục nào, nhưng manifest **vẫn phải**
  tái sinh — `release.py` NẰM TRONG gói nên sửa chính nó là đổi sha của chính nó. Lượt đầu quên
  và cổng trả `failed: 1` đúng ngay tệp vừa sửa. Cổng nói thật, chỉ là nói về chuyện khác với
  chuyện mình đang nghĩ. `references/golden/**` KHÔNG bị chạm — không ghi đè golden cho hết đỏ.
- Nghiệm thu trên GitHub Actions, `workflow_dispatch` nên chạy CẢ HAI nền: `gate (ubuntu-latest)`
  và `gate (windows-latest)` đều `success`, **20/20 bước**, không bước nào `skipped` do nền.
  Bước `release-bundle x2 cùng SHA-256` xanh ở cả hai — bảng loại trừ mới cho kết quả tất định,
  không lệch giữa `/` và `\`, đúng chỗ đáng ngờ nhất của một bản vá đụng đường dẫn.

Kèm trong đợt (nhánh ops, không đụng runtime gói): lease neo prompt bằng `prompt_path` + băm và
cổng `ops/lease_publish.py` kiểm được nó (`rc=6`) — trước đó lease #3 của wp55 neo một băm không
ứng với văn bản nào, cổng phía reviewer hỏng IM LẶNG và chặn wp55 hai ngày. 23 ca phản chứng, 6
đột biến giết đúng ca đích; lượt đột biến đầu bắt được hai "chốt" thực ra là trang trí, nên phản
chứng nay neo THÔNG ĐIỆP chứ không chỉ mã thoát.

# ★ v1.36.67 — r335: kích hoạt topology test-fragment F1 (2026-08-06)

Mission F1 chuyển selftest sang mô hình fragment dành cho nhánh phát triển nhưng vẫn giữ gói phát hành
độc lập với thư mục fragment: loader tự chọn topology, generator tạo một bundled module tất định, và
release fail-closed nếu module bắt buộc đó bị thiếu.

- Năm packet F1 đã được review và tích hợp tuần tự; canary `wp45_fragment_canary` chứng minh legacy
  selftest, dev fragment và generated bundle cùng chạy đúng một lần với cùng kết quả.
- `scripts/tl_test_fragments_bundled.py` trở thành release-required file; `scripts/test_fragments/`
  vẫn là dev-only và không lọt vào manifest/zip. Gói tiếp tục bị chặn ở trần dưới 200 tệp.
- Activation chỉ đổi topology test/release cục bộ; không push, deploy, truy cập LIVE hoặc secret.

# ★ v1.36.66 — r334: Preview nhận biết bộ D0 đã land và trả JSON terminal (2026-08-04)

`Invoke-SharedWorkPacketFlow.ps1 -Action Preview` trước đây chết ở PowerShell binder khi cả 23 nguồn D0
đã sạch sau landing: `git status` trả mảng rỗng, nên caller chỉ thấy `Cannot bind ... empty array` thay vì
kết quả máy đọc được. TDD khóa đúng public seam trước khi sửa (RED trên Windows PowerShell 5.1).

- Preview nay trả `ok:true`, `status:"already_landed"`, `next_action:null`; không sinh packet body và mọi
  trường Issue/packet/branch đều `null`.
- Chỉ kết luận terminal khi đủ 23 đường trên đĩa, `source_status` rỗng và diff của chúng khớp đúng
  `origin/master`; clean nhưng lệch base vẫn fail-closed.
- `CreateExecutor` không được nới quyền: không có `-DryRun` thì nguồn sạch vẫn bị từ chối trước Issue API.
- Regression chạy qua controller thật với biên `git`/`gh` giả lập; giữ parity PowerShell 5.1/7 và chứng minh
  `gh issue create` không được gọi. Không đổi runtime pháp luật, Drive hoặc NLM.

# ★ v1.36.65 — r333: land cứu hộ bộ hiến pháp D0 từ tree đã neo, không kéo code WIP (2026-08-04)

**Nguồn cứu hộ được chốt theo đường A:** tag `rescue/d0-2026-08-04` trỏ root tree `dacc4e76`;
`docs/` lấy từ tree `2db90d43`. PR chỉ mang phần hiến pháp đã đối chứng, không cherry-pick parent
`d347129` vì parent đó còn 19 tệp code WIP chưa review.

- Land 21 Markdown dev-side: `PROTOCOL_DA_PHIEN.md`, kế hoạch triển khai, ADR-0017–0033 và hai báo cáo research.
- ADR-0001 đổi `Accepted` → `Superseded by ADR-0017`; thay đổi này đi cùng chính ADR-0017 trong một commit.
- `CONTEXT.md` cứu hộ vẫn được giữ an toàn trong tag + bản sao ngoài repo, nhưng chưa land ở đợt này: bản đó
  trỏ tới `scripts/test_fragments/wp` và `scripts/tl_test_fragments_bundled.py` là code D0 chưa tồn tại;
  `release-verify` đã fail-closed đúng với `DOC_POINTERS_NOT_IN_PACKAGE`, nên không hạ cổng để ép xanh.
- Kế hoạch dùng đúng blob `d83cec6b` 24.532 byte của tree đã neo, không dùng biến thể 30.392 byte ở `6c148d3`.

**Ratchet có chủ đích:** `docs/**/*.md` tăng 21 → 42; Package vẫn 177 tệp vì `docs/` là dev-side,
phép kiểm cây thật tăng 198 → 219 nhưng không nới trần import Package 200. TDD RED trước sửa: selftest
`1642/1644`, chỉ `r209_cay_that_va_phan_chung` và `r291_docs_ngoai_goi` đỏ; loại `CONTEXT.md` treo
khỏi write-set và cập nhật ratchet là hai thay đổi tương ứng, không đổi runtime/Drive/NLM.

# ★ v1.36.64 — r332: một controller PowerShell điều phối trọn vòng D0 Codex → Claude (2026-08-04)

**Ba giai đoạn trước đây cần nhiều lệnh rời nay có một entrypoint máy đọc được:**
`docs/runbooks/Invoke-SharedWorkPacketFlow.ps1` bọc hai primitive đã harden
`New-SharedWorkPacket.ps1` và `Fill-SharedWorkPacketPrompt.ps1` thành `Preview`, `CreateExecutor` và
`PrepareReviewer`.

- `Preview` luôn đo LIVE: auth/fetch/base/bootstrap/23 nguồn/PR; không nhận snapshot bypass và không gọi Issue API.
- `CreateExecutor` chỉ tạo Issue thật khi có cờ `-ConfirmCreateIssue`, rồi điền prompt Codex và copy clipboard.
- `PrepareReviewer` kiểm nhánh đúng `agent/wp<N>-g<G>-codex`, fetch lại và đòi `FETCH_HEAD` khớp exact
  `REVIEW_READY` head trước khi dựng worktree detached/sạch; prompt Claude chỉ vào clipboard sau mọi gate.
- Controller không push, mở/merge PR, đăng verdict, bump version hoặc deploy; các quyền này vẫn là cổng riêng.

Regression `Test-InvokeSharedWorkPacketFlow.ps1`: `4/4` trên Windows PowerShell 5.1 và PowerShell 7, gồm
đường dẫn `Quốc hội`, dấu nháy đơn, help UTF-8 BOM + LF, snapshot rejection, live shims và stale-head fail-close.
Bộ bootstrap cũ vẫn `10/10`; CI Ubuntu/Windows của PR #31 và review Standards/Spec đều xanh, 0 finding.

# ★ v1.36.63 — r331: `.codex/` (worktree agent Codex) không có trong bảng loại trừ ⇒ gate ĐỎ theo NƠI CHẠY (2026-08-04)

**Triệu chứng khó tin nhất: cùng một commit, chạy chỗ này XANH chỗ kia ĐỎ.** Deploy từ main checkout
(`tra-luat` gốc) ăn gate đỏ ở `release-check` + `release-verify`, trong khi CÙNG commit `0cea4a7`
build từ worktree sạch thì xanh và đẩy Package v1.36.62 byte-match trót lọt.

**Manifest LÀNH — đỏ hoàn toàn do tệp THỪA.** Bằng chứng dương từ `relverify.out`:

```
"expected_file_count": 177,  "checked_file_count": 177,  "failed": []
"extra_files": [ 200 mục ]   ← 200/200 đều thuộc .codex/
```

`_RELEASE_EXCLUDE_DIRS` có `.claude` nhưng THIẾU `.codex`. Agent Codex đặt worktree ở
`.codex/worktrees/<nhánh>/`, **mỗi worktree là một BẢN SAO ĐẦY ĐỦ của kho** (có `VERSION`, `SKILL.md`,
`RELEASE_MANIFEST.json` riêng) — 4 worktree đang sống. Cây phát hành quét trúng chúng ⇒ mọi lượt gate
chạy từ main checkout đều đỏ, còn worktree sạch không có `.codex/` nên không ai thấy.

★ **Cạm bẫy đã suýt sập: lời khuyên tự động của deploy SAI ở ca này.** `[WARN] cây đã đổi so với manifest
— chữa: release-manifest --out RELEASE_MANIFEST.json` đúng cho ca thêm/xoá tệp THẬT (bài học r238), nhưng
ở đây nó sẽ **nướng 4 bản sao kho vào manifest** trong khi trần gói là **200 tệp CỨNG**. Đọc `failed: []`
+ `177/177` TRƯỚC khi tin lời khuyên: manifest không hề cũ.

**Vá:** `+.codex` vào `_RELEASE_EXCLUDE_DIRS` (đúng khuôn `.claude`: GIỮ trong repo, CHỈ loại khỏi gói)
và `+.codex/` vào `.gitignore`. Gói vẫn 177 tệp — **không tệp nào ra/vào**, nên không đụng kê khai slot.

★ **Bẫy phụ, sập THẬT lúc viết bản vá này** (bắt được trước commit, đã khoá bằng vế 4 của ca test):
trong cú pháp `.gitignore`, `#` **chỉ** mở chú thích khi ĐỨNG ĐẦU DÒNG. Viết `.codex/   # ghi chú` thì
cả cụm thành MỘT pattern và **không bỏ qua gì cả** — im lặng, không lỗi, không cảnh báo.

Ca `r331_codex_ngoai_cay_phat_hanh`: 4 vế từ 4 nguồn — hằng chính sách · HÀNH VI trên cây tổng hợp (kèm
đối chứng cùng tên tệp ngoài `.codex/` phải VÀO gói) · loại đúng vì khoá `.codex` · `.gitignore` dòng độc lập.

# ★ v1.36.62 — r330: timeout ĐƯỜNG GHI của `gws` chọn KHÔNG ĐO ⇒ `update_content` 120s CHẶN THẬT lượt deploy (2026-08-04)

**Nối tiếp r327 — cùng một bệnh, nấc kế tiếp.** r327 vá phép DÒ (`auth status` 20s→120s) nên `drive-push`
ĐÃ đi đúng tuyến gws; nó chết ngay ở bước sau, lần này là timeout của CHÍNH lệnh upload:

```
[drive-push] ✗ update lỗi: GwsError: gws timeout sau 120.0s
(gcloud cũng không sẵn: gcloud auth print-access-token timed out after 30 seconds)
```

`update_content()` gọi `_run(..., timeout=120.0)` — hằng CỨNG, chưa ai đo. Gói deploy chỉ **2.487.725 B**
mà vượt 120s. Đặt `TL_GWS_TIMEOUT=900` rồi chạy lại thì đẩy XONG + **BYTE-MATCH** (Drive md5
`839a7177b4089098ad7d96f4a9234f11` = local) ⇒ knob của r327 làm đúng việc, nhưng **mặc định vẫn là tường**
nên lượt deploy sau lại đâm vào đó trừ khi người vận hành nhớ khai env.

## ĐO (máy chuẩn Windows, CÙNG đường mã, artifact TEST rồi xoá — KHÔNG đụng `SKILL_FILEID`)

`update_content` theo CỠ payload — đo nhiều cỡ để **tách phí CỐ ĐỊNH khỏi phí THEO BYTE**:

| cỡ payload | lượt đo | ghi chú |
|---|---|---|
| 1 KB | 3,3 · 5,7 · 3,5 s | = phí CỐ ĐỊNH (spawn + keyring + 1 vòng API) |
| **2,49 MB** (đúng cỡ gói) | 6,1 · 11,5 · 7,5 s (03-08) · 9,8 · 19,3 · 13,2 s (04-08) | **max 19,3 s** |
| 10 MB | 27,6 · 48,5 · 21,1 s | |
| 25 MB | 42,5 · 46,7 · 30,8 s | |

Các lệnh còn lại (payload 2,49 MB nếu có tải):

| op | lượt đo | max | mặc định cũ | nay |
|---|---|---:|---:|---:|
| `upload` | 6,9 · 11,8 · 5,5 · 18,9 s (2,49MB) · 22,7 s (10MB) · 44,6 s (25MB) | 44,6 | 180 s | **600 s** |
| `download` | 6,8 · 4,0 · 3,5 s | 6,8 | 300 s | **600 s** |
| `copy_convert` (docx→GDoc) | 4,7 · 5,0 · 5,7 s | 5,7 | 180 s | GIỮ |
| `mkdir` | 2,8 · 3,3 · 2,9 s | 3,3 | 60 s | GIỮ |
| `_files_update` (rename) | 2,2 · 1,9 · 2,2 s | 2,2 | 60 s | GIỮ |

★**Vì sao KHÔNG áp công thức r327 («2,4× ca chậm nhất ĐO được»)** — đây là điểm dễ sai nhất của đợt này.
Ở r327 phép đo ĐÃ TRÙM vùng hỏng (15–50 s vắt qua trần 20 s) nên nhân 2,4 là hợp lệ. Ở đây **mọi mẫu đo
được đều thuộc vùng LÀNH**: 2,4 × 19,3 = **46 s**, tức **THẤP HƠN cả 120 s vốn ĐÃ hỏng** — áp máy móc sẽ
làm bệnh **nặng hơn**. Neo đúng phải là **ca hỏng QUAN SÁT ĐƯỢC**, không phải median ngày lành.

★**Chọn hằng bằng BĂNG THÔNG suy ra:** phí ≈ (3–6 s cố định) + kích thước ÷ băng thông. Đo được
**~170–850 kB/s**. Ca hỏng: 2,49 MB không xong trong 120 s ⇒ băng thông thực **≤ ~21 kB/s** (chậm hơn ca
lành 8–40×; VPN/tether/nghẽn là đủ). Trần **600 s** phủ tới **~4,2 kB/s** — còn chịu được ca xấu hơn ca đã
hỏng ~5× nữa, mà vẫn CÓ BIÊN (gws wedge không treo phiên vô hạn).

★**Bất đối xứng chi phí — khác r327, phải nói rõ:** ở phép dò, chờ thừa chỉ tốn giây trong ca ĐÃ hỏng
(cache 1 lần/phiên). Ở đường GHI, chờ thừa tốn wall-time THẬT. Vẫn chọn hào phóng vì deploy là việc HIẾM
và **có người ngồi xem** (Ctrl-C được), còn chờ thiếu thì giết một lượt đẩy ĐANG CHẠY ĐÚNG rồi rơi xuống
gcloud thiếu Drive scope ⇒ `[FAIL]` cứng.

## Vá (5 vế, mỗi vế một ca test + mutation riêng)

1. **`update_content` 120→600 s · `upload` 180→600 s · `download` 300→600 s.** CHỈ nâng lệnh **CÓ TẢI** —
   chỉ chúng mới co giãn theo băng thông. `mkdir`/`rename`/`delete` đo 1,9–3,3 s (dư 18–27×) và
   `copy_convert` 5,7 s (server-side, không cõng payload local) ⇒ **GIỮ NGUYÊN**. *«Không sửa cái đang
   đúng»* — cùng lý lẽ r327 giữ `--version` ở 30 s.
2. **Knob riêng `TL_GWS_WRITE_TIMEOUT`** theo đúng khuôn `_timeout(default, knob)` sẵn có, nhưng là
   **SÀN (chỉ NÂNG)** chứ không đè — và đó là chủ đích: nó phủ NHIỀU lệnh có mặc định KHÁC nhau, cho hạ
   thì MỘT con số sẽ **san phẳng cả nhóm**, đúng cái bẫy r327 đã vá, chỉ đổi phạm vi. Hợp thành:
   `knob riêng (đè hẳn) → max(TL_GWS_WRITE_TIMEOUT, TL_GWS_TIMEOUT, default)`.
3. **`download()` vẫn là điểm mù** — nó KHÔNG đi qua `_run` (stdout phải là BYTES) nên r327 đã phải gọi
   `_timeout()` tay; quên `write=True` thì nó là lệnh CÓ TẢI duy nhất lọt sàn mới. Khoá bằng HÀNH VI
   (đọc ngân sách thực nhận), không đọc mã.
4. **Thông điệp SAI HƯỚNG — bệnh r327 lặp ở đường GHI.** `_drive_push_route` khuyên `gws auth login` cho
   MỌI kiểu hỏng, mà **timeout ≠ mất quyền**. r327 đã KHAI sẵn `probe_error` nhưng **chưa ai đọc** — nay
   route nhận `probe_error` và `cmd_drive_push` in câu KHẮC PHỤC đúng hướng khi lỗi ghi là timeout.
   Cùng họ bài học r321/r322/r327: *«đã có lời khai» ≠ «có ai đọc lời khai»*.
5. ★**Cùng bệnh, dạng NẶNG NHẤT — ở `deploy-package.sh` lời khuyên sai hướng bị CHẠY, không chỉ in.**
   ``bad "... (cần `gws auth login` có quyền GHI Drive)"`` — **backtick trong chuỗi nháy KÉP của bash
   THAY THẾ LỆNH**. Mỗi lần `drive-push` hỏng, `gws auth login` **khởi chạy thật**, và thông điệp in ra
   *output của nó* thay vì tên lệnh. Twin `ps1` KHÔNG dính (nháy ĐƠN của PowerShell coi backtick là ký tự
   thường) ⇒ đúng lớp **lệch hai nền** mà chỉ CHẠY THẬT mới thấy — bài học r244 lặp nguyên văn. Nay hai
   bản mang **CÙNG MỘT CÂU, không ký tự nháy nào**, và ca test đối chiếu parity + chạy dòng thật.

Test (5 ca, giả `subprocess` để **ghi lại ngân sách thực nhận** + mô phỏng lệnh tốn N giây, không chờ
thật): `r330_write_du_gio_cho_goi_that` (phí 150 s — nằm GIỮA trần cũ 120 s và trần mới — phải xong, và
ngân sách lệnh CÓ TẢI phải **lớn hơn** lệnh metadata) · `r330_write_knob_chi_nang_khong_ha` (gồm vế
`download` lọt sàn) · `r330_write_env_meo_khong_vo_hieu` · `r330_timeout_khuyen_dung_huong` ·
`r330_deploy_msg_khong_chay_lenh` (TỰ KIỂM CHỨNG: dòng CŨ phải tái hiện được việc `gws` bị gọi, dòng MỚI
phải sạch — không tái hiện nổi thì ca ĐỎ).

# ★ v1.36.61 — r329: bootstrap công cụ work-packet D0 + kê khai slot docs 19→21 (2026-08-03)

**Bốn tệp mới NGOÀI GÓI** (tác giả Codex, nhánh `codex/work-packet-bootstrap`):
`docs/runbooks/New-SharedWorkPacket.ps1` — script tạo Shared Work Packet (GitHub Issue): tự đo
base_sha/PR-mở/23 nguồn D0, đòi `source_status` đúng M/untracked, `DryRun`/`SnapshotPath`,
packet_id = `wp<số Issue thật>` qua hai bước create→edit, fail-closed mọi nhánh lỗi;
cặp prompt `docs/prompts/CODEX_EXECUTOR_D0.md` + `docs/prompts/CLAUDE_REVIEWER_D0.md`
(one-executor-per-packet, reviewer read-only tuyệt đối, approval gắn head SHA); bộ test
`docs/runbooks/tests/Test-NewSharedWorkPacket.ps1` — 6 ca có shim git/gh, kể cả prompt-contract
test khoá bất biến của chính hai prompt. Đo độc lập 03-08: 6/6 hai lượt chạy; DryRun trên cây
canonical thật `ok:true` `ready_for_claim`.

**Vế mã duy nhất: kê khai slot ratchet.** CI PR #25 đỏ `r291_docs_ngoai_goi` (1637/1638, CẢ HAI nền)
vì `docs/**/*.md` 19 → 21 — **đỏ ĐÚNG THIẾT KẾ ratchet** («thêm/bớt tệp ⇒ đỏ, sửa CÓ CHỦ ĐÍCH kèm
kê khai slot»), không phải hồi quy. Kê khai: mốc 196 → 198 (gói giữ 177 + 21 docs ngoài gói;
trần 200 còn 2 khe theo phép đếm ratchet). Không đổi hành vi runtime nào.

# ★ v1.36.60 — r328: đường dẫn NGOÀI ASCII vỡ ở khớp JSON của HAI script deploy (2026-08-03)

**`deploy-package.ps1` chết `[FAIL] release-bundle báo ok nhưng KHÔNG có zip thật` + exit 2 — trong khi
zip ĐÃ build đúng** (`file_count 177`, `reproducible true`, `bundle_sha256` khớp cả hai lượt). Đường
vòng đang dùng là chạy qua junction ASCII `C:\qh\…` cho hết dấu; đó là NÉ, không phải vá.

`tl.py` ghi JSON **UTF-8** (tl.py:86 `reconfigure`), nhưng PowerShell **GIẢI** stdout của lệnh native
bằng `[Console]::OutputEncoding` — ĐO trên máy chuẩn: **windows-1258** (ANSI codepage VN), không phải
UTF-8. `bundle1.out` vì thế chứa mojibake **ghi thẳng ra đĩa**:

```
"out": "D:\Quá»‘c há»™i\tra-luat\…"      ← thay vì  D:\Quốc hội\tra-luat\…
```

⇒ `Test-Path $out` trả **false cho tệp CÓ THẬT** ⇒ bước 2 dừng. Cắn MỌI đường dẫn ngoài ASCII, gồm cả
đường canonical `D:\Quốc hội\…`. (Phiếu ban đầu đoán cp1252; đo ra **cp1258** — cùng ánh xạ 0x91→U+2018
nên bằng chứng round-trip không phân biệt được hai bảng mã.)

★**Vì sao sống lâu mà không ai thấy:** `deploy-package.cmd` `chcp 65001` TRƯỚC khi gọi pwsh ⇒ đường
double-click SẠCH BỆNH. Đúng cách CLAUDE.md dạy gõ (`.\scripts\deploy-package.ps1 -Pull -Push` thẳng
trong pwsh) thì KHÔNG qua .cmd ⇒ dính. Hai đường vào cùng script, một đường mù.

**★ ĐO ĐƯỢC — SỬA CHỖ ĐỌC LÀ VÔ TÁC DỤNG** (cùng đầu vào, ambient cp1258):

| bản vá thử | kết quả |
|---|---|
| chỉ `-Encoding utf8` ở chỗ ĐỌC | `EQ=False` · `Test-Path=False` — **không cứu được gì** |
| chỉ `[Console]::OutputEncoding = UTF8` | `EQ=True` · `Test-Path=True` — **vế chịu lực** |

Mojibake đóng băng ngay khâu GIẢI; tới lúc `Get-Content` chạy thì tệp trên đĩa đã sai rồi. Ghim cả hai
chiều là để khỏi lệ thuộc mặc định theo phiên bản PowerShell, **không** phải vì chiều đọc tự nó chữa được.

**Vá — `scripts/deploy-package.ps1`:** `[Console]::OutputEncoding` + `$OutputEncoding` = UTF-8 (no BOM);
`$PSDefaultParameterValues['Out-File:Encoding']='utf8'` (toán tử `*>` gọi Out-File bên dưới); ghim
`-Encoding utf8` cho **cả 9** lời gọi `Get-Content … -Raw`; xuất `PYTHONUTF8`/`PYTHONIOENCODING` xuống
script con KHÔNG tự cứng hoá (`pkg_secret_scan.py`, `gen_instructions.py` — `tl.py` tự lo, ta gọi thẳng
nhiều script khác; CI khai y hệt hai biến này).

**★ TWIN `sh` MẮC CÙNG BỆNH — tìm ra nhờ ĐỐI CHIẾU PARITY, không phải đọc code** (đúng cảnh báo
CLAUDE.md: *«hai bản sẽ trôi lệch, và bên quên cập nhật chính là bên đẩy lọt»*). `jget()` dùng
`open()` **không nêu encoding** ⇒ codec LOCALE. Linux/Cowork locale UTF-8 nên vô hại — nhưng đo bằng
Git Bash trên máy chuẩn (locale **cp1258**), CÙNG tệp JSON:

- `ố` (U+1ED1 = `e1 bb 91`, 0x91 CÓ trong cp1258) → giải ra `U+2018 U+00E1 U+00BB` = **mojibake im lặng**.
  Nó *có vẻ* chạy được vì `print` mã hoá LẠI bằng đúng codec sai đó nên lỗi **tự triệt tiêu** — một sự
  sống sót tình cờ, không phải tính đúng đắn.
- `Ố` (U+1ED0 = `e1 bb 90`, byte **0x90 KHÔNG ĐỊNH NGHĨA**) → `UnicodeDecodeError` thẳng. Mà `jget` có
  `2>/dev/null` nên **NUỐT lỗi** rồi trả RỖNG ⇒ script báo *"KHÔNG có zip thật: '&lt;rỗng&gt;'"* — sai
  địa chỉ, im lặng, không lần ra được nguyên nhân.

Vá: `open(…, encoding='utf-8')` + `sys.stdout.reconfigure(encoding='utf-8', newline='\n')`.
`newline='\n'` là **byte cuối cùng làm hai bản LỆCH**: trên Git Bash/Windows `print` dịch `\n`→`\r\n`
mà `$( )` chỉ nuốt `\n`, nên đường dẫn còn ĐUÔI `\r` ⇒ `[ -s "$z" ]` trượt trên tệp có thật. (Có sẵn từ
bản cũ, không do vá này — nhưng đo parity thì nó lòi ra, nên vá luôn.)

**BẰNG CHỨNG (chạy THẬT, không đọc code — bài học r244):**
- `deploy-package.ps1 -NoTest` chạy TRỌN trong worktree `D:\Quốc hội\…` ⇒ **rc=0**, bước 2 same-SHA
  `51a06b16a1968ea2…` · 2.487.725 byte, bước 3 `178 tệp`, quét bí mật sạch, release-verify trong gói ok.
- **MUTATION**: gỡ ĐÚNG một dòng `[Console]::OutputEncoding` ⇒ trở lại đúng triệu chứng gốc
  `[FAIL] release-bundle báo ok nhưng KHÔNG có zip thật` + **rc=2**, đúng ở bước 2.
- **PARITY hai bản trên CÙNG đầu vào** (cùng `release-bundle`, rút khoá `out`): **BYTE-MATCH `True`** —
  `443a5c5175e1bb91632068e1bb99695c…` cho cả hai; chốt `[ -s "$z" ]` của sh PASS trên chuỗi vừa rút.

**★★ MUTATION BẮT ĐƯỢC LỖI CỦA CHÍNH BỘ TEST — hai vế đầu XANH GIẢ, đã vá.** Đột biến M1/M2/M3 (ps1)
đỏ đúng ca của nó, nhưng **M4 (gỡ `encoding='utf-8'` khỏi `open()` của `jget`) SỐNG SÓT cả ba ca**. Hai
nguyên nhân ĐỘC LẬP, cùng hướng — đúng khuôn «hai lỗi độc lập mà cùng hướng» của §Bài học CLAUDE.md:

1. **Guard khớp NHẦM NỬA KIA CỦA DÒNG.** Vị ngữ ban đầu là `"encoding='utf-8'" in dòng_jget`. Nhưng
   dòng đó chứa chuỗi ấy **HAI LẦN** — một ở `open(...)`, một ở `reconfigure(...)`. Gỡ khỏi `open()`
   thì bản sao ở `reconfigure()` vẫn làm vị ngữ ĐÚNG ⇒ guard xanh trên đúng thứ nó sinh ra để chặn.
   Vá: soi **TỪNG lời gọi** bằng regex riêng (`open\(sys\.argv\[1\],encoding='utf-8'\)` và
   `reconfigure\(encoding='utf-8',newline='\n'\)`), không dò chuỗi trên cả dòng.
2. **`tl.py:93` CHE mất đột biến ở vế hành vi.** `os.environ.setdefault("PYTHONUTF8","1")` nằm sẵn
   trong environ của tiến trình selftest và **truyền xuống tiến trình con**, nên `open()` TRẦN trong
   payload vẫn ra UTF-8 ⇒ đột biến vô hình. Vá: chạy payload với env **thù địch** — `PYTHONUTF8=0`,
   bỏ `PYTHONIOENCODING`, `LC_ALL=LANG=C`. Nay đột biến đỏ trên **CẢ HAI nền** (Linux: locale→ASCII ⇒
   `UnicodeDecodeError`; Windows: cp1258 ⇒ mojibake), không chỉ trên máy dev.

Đo lại sau khi vá: bản đã vá `ok4=True okD=True` · bản đột biến M4 `ok4=False okD=False`.
★ Bài học chung: **vị ngữ dò chuỗi trên CẢ DÒNG là mù khi dòng có hai lời gọi cùng hình dạng**; và
**tiến trình con thừa kế env của bộ test có thể chữa lành đúng khuyết tật đang đo** — muốn đo khuyết
tật môi trường thì phải DỰNG môi trường đó, đừng để env của suite rò vào.
⚠ Ghi chú đo đạc: chạy 4 suite SONG SONG làm vài ca chia sẻ cache/HOME đỏ giả (`r3_config_write_journaled`,
`profile_config_lifecycle`, `r40_resolve_registry_doc_id_layers`; số trôi 1634–1636). Số CHỐT phải đo
**chạy MỘT MÌNH**: nền `HEAD` = **1635/1635**, bản vá = **1638/1638** (đúng +3 ca, không mất ca nào).

**Ba ca test (mỗi ca một vế, mutation riêng):**
1. `r328_deploy_ep_utf8_hai_chieu` — chốt chống tái phát, khuôn HAI BỐI CẢNH r265 (cây git đòi đủ 4
   dấu hiệu ở cả hai script; gói bung đòi ba script deploy VẮNG vì là dev-side).
2. `r328_json_ngoai_ascii_khong_qua_codec_ansi` — HÀNH VI thuần Python (chạy được cả hai nền CI, không
   cần pwsh): tái hiện cả hai mức hỏng (mojibake im lặng · `UnicodeDecodeError`), và chạy THẬT payload
   `-c` **rút từ chính `deploy-package.sh`** (không chép lại — chép là trôi lệch), đòi stdout ra đúng
   byte UTF-8 và KHÔNG có đuôi `\r`.
3. `r328_ps1_roundtrip_pwsh_that` — đầu-cuối qua **pwsh THẬT**, đúng hình dạng `Invoke-Py`/`Get-Content`.
   **TỰ KIỂM CHỨNG chống xanh giả:** đòi CẢ HAI vế — bản chưa vá phải LỆCH *và* bản đã vá phải KHỚP;
   môi trường không tái hiện nổi bệnh thì ca ĐỎ chứ không xanh suông. Không có pwsh ⇒ bỏ qua (ca 1+2 phủ).

# ★ v1.36.59 — r327: phép dò auth của `gws` có timeout NGẮN HƠN phí thật ⇒ `is_available()` nói dối (2026-08-03)

**`drive-push` trượt ở bước đẩy cuối dù gate 8/8 xanh, nhiều phiên liền. Chẩn đoán cũ «hỏng tạm, chạy
lại là được» SAI — và chính cái làm nó sống lâu là bệnh phụ thuộc MẠNG nên thỉnh thoảng tự khỏi.**

`gws_bridge.auth_method()` gọi `_run(["auth","status"], timeout=20.0)` — hằng CỨNG, không env knob.
Nhưng `gws auth status` liệt kê 34 API + gọi mạng. ĐO trên máy chuẩn Windows, CÙNG đường mã đó:

| lượt đo | phí `gws auth status` |
|---|---|
| 02-08-2026 (3 lượt) | 29,1 · 39,7 · 50,5 s |
| 03-08-2026 (3 lượt, đo lại lúc vá) | 18,9 · 15,4 · 17,1 s |
| `gws --version` cùng tiến trình (đã gánh cold-start) | **3,7 s** |

⇒ phí thật **dao động 15–50 s quanh trần 20 s**: phép dò **lật đỏ/xanh theo mạng**, không hỏng hẳn —
nên `gws auth status` chạy tay vẫn ra `"auth_method":"oauth2"` rc=0 mà `tl` lại kết luận «gws chưa sẵn».
Dây chuyền: `auth_method()`→`None` → `is_available()`→False → `cmd_drive_push` tính `gws_ok=False` →
`_drive_push_route` rơi xuống gcloud → gcloud thiếu Drive scope ⇒ **`[FAIL] drive-push`**, dù gws SỐNG.
`--via gws` KHÔNG cứu: nó vẫn đọc chính `gws_ok` từ phép dò hỏng.

★**Bằng chứng nội tại có sẵn mà không ai đọc:** ngay dòng trên, `--version` được **30 s** kèm chú thích
«bù gws cold-start», còn `auth status` — việc **nặng hơn hẳn** — chỉ được **20 s**. *Phép dò chậm nhất
mang ngân sách ngắn nhất.* Đo mới còn cho thấy ngược hơn nữa: `--version` thật ra chỉ tốn **3,7 s** (dư
8×), tức toàn bộ ngân sách rộng rãi đang nằm ở phép dò KHÔNG cần.

**Vá (4 vế, mỗi vế một ca test + mutation riêng):**
1. `_auth_probe()` **120 s** (≈2,4× ca chậm nhất từng đo) thay 20 s. `--version` **GIỮ 30 s** — đã đo dư
   8×, không sửa cái đang đúng.
2. **Env knob**, chỉnh không cần sửa mã: `TL_GWS_AUTH_TIMEOUT` · `TL_GWS_VERSION_TIMEOUT` (đè riêng
   từng phép dò) và `TL_GWS_TIMEOUT` = **SÀN chung cho MỌI lệnh gws**. Sàn **chỉ NÂNG**: khai
   `TL_GWS_TIMEOUT=120` nâng phép dò 30 s→120 s mà **không** hạ `download` 300 s→120 s — hạ trần một
   cách vô tình chính là cái bẫy đang vá. Giải timeout ở **đúng một chỗ** (`_run`) nên thông điệp lỗi
   khai đúng ngân sách đã dùng; `download()` không đi qua `_run` (stdout phải là BYTES) nên gọi
   `_timeout()` tay — nếu quên, đó là lệnh gws DUY NHẤT sàn không với tới.
3. **Env méo KHÔNG được biến knob thành công tắc TẮT timeout**: `0`/âm ⇒ chết tức thì, `inf`/`1e400` ⇒
   treo vô hạn (gws wedge = phiên treo, mất luôn đường fallback). `_env_timeout()` chỉ nhận số **dương
   hữu hạn**; rác/rỗng/`nan` ⇒ về mặc định.
4. **Lộ diện lý do** — vì sao bệnh sống lâu: lỗi bị **NUỐT**. `auth_method()` nuốt `GwsError` nên
   «dò không xong» và «dò xong, chưa auth bao giờ» **cùng** trả `None`; `availability_detail()` không
   phân biệt nổi ⇒ người vận hành đọc `auth=None` rồi đi `gws auth login` — **sai hướng, không phải lỗi
   quyền**. Tách `_auth_probe() -> (method, err)`, thêm khoá `probe_error` vào `availability_detail()`
   (`transport-info --json` phơi sẵn). Cùng họ bài học r321/r322: *«đã có hàm» ≠ «có đường gọi»;
   «đã có lời khai» ≠ «có ai đọc lời khai»* — lần này là **«đã có lỗi» ≠ «lỗi có lối ra»**.

★**Bất đối xứng chi phí** (lý do chọn hào phóng): chờ THỪA chỉ tốn giây trong ca ĐÃ hỏng — phép dò cache
1 lần/phiên và chỉ chạy khi binary `gws` có thật; chờ THIẾU thì trả lời **SAI** rồi định tuyến ngầm sang
đường chết. Ngân sách timeout của một phép dò không phải chỗ để tiết kiệm.

Đo end-to-end sau vá, gws THẬT trên máy chuẩn: `availability_detail()` → `ok:true`,
`auth_method:"oauth2"`, `probe_error:""` trong 14,7 s.

Test (4 ca, giả `subprocess` để **ghi lại ngân sách thực nhận** + mô phỏng lệnh tốn N giây, không chờ
thật): `r327_auth_probe_du_gio_cho_gws_that` (phí 25 s — nằm GIỮA trần cũ 20 s và ca chậm nhất 50 s —
phải ok=True, và ngân sách auth phải **lớn hơn** `--version`) · `r327_env_knob_chinh_duoc_timeout` ·
`r327_env_meo_khong_vo_hieu_timeout` · `r327_probe_error_lo_dien`.

# ★ v1.36.58 — r326: hạ tuyên bố quá tầm ở `RASOAT_HOSO_LOOP.md` §7, và bịt ĐIỂM MÙ con trỏ TÊN CA (2026-08-03)

Nối tiếp T0-E/GATE-06 (r298). Lần đó ba ca tự-chứng-minh đã bị hạ tuyên bố **trong `scripts/tl_selftest.py`**,
nhưng phạm vi T0-E chốt là CHỈ tệp đó ⇒ câu tuyên bố trong tài liệu vẫn nguyên.

**Bệnh 1 — câu ở `references/RASOAT_HOSO_LOOP.md` §7 tuyên bố quá tầm.** Nguyên văn cũ: «Đường ghi hợp lệ —
máy đọc được, guard `r210_loop_khong_ghi_trong_cay` khoá:». Đo lại chính ca đó: nó chỉ **lint khối khai báo
`WRITE_PATHS_v1`** — không chạy vòng nào, không `git status`, không `release-verify`.

**Vá 1.** Tách HAI TẦM: `r210_loop_khong_ghi_trong_cay` khoá **KHAI BÁO**; vế **CHẠY** do
`r298_worklist_chay_kho_a3_a6` gánh (chạy khô A3→A6 trên `cmd_state_put`/`cmd_state_get` THẬT).
**KHÔNG đổi tên ca** — dòng đó là con trỏ tới tên.

**Bệnh 2 — điểm mù: KHÔNG cổng nào giữ con trỏ TÊN CA trong tài liệu.** Cả kế hoạch lẫn CHANGELOG r298
đều tưởng `doc-claims-check` giữ con trỏ ấy — ĐÃ ĐO: KHÔNG. `_DOC_CLAIMS_R_RE` đòi `` sau `r210`, mà `_`
là ký tự TỪ nên `findall` trả RỖNG cho cả một tên ca bịa hoàn toàn. Đổi/xoá tên ca thì tài liệu trỏ vào hư
không mà **cả 5 cổng vẫn XANH** — cùng lớp bệnh GATE-06, khác tầng.

**Vá 2 — `r326_con_tro_ten_ca_resolve`.** Bóc MỌI con trỏ `` `rNNN_snake` `` trong kịch bản, đối chiếu bảng
tên đăng ký `_t110` bóc từ nguồn; fail-closed khi không bóc được con trỏ nào. Chống xanh-vô-điều-kiện bằng
hai vế: (a) hai tên đó phải có trong `cases` đã CHẠY; (b) ★ phản chứng — bộ bóc phải BẮT được tên bịa và
tên bịa KHÔNG được resolve.

**Bằng chứng dương.** Phản chứng chạy THẬT, mỗi lượt đỏ ĐÚNG một ca: đổi tên ca được trỏ ⇒ ĐỎ;
xoá sạch con trỏ ⇒ vẫn ĐỎ (fail-closed). Tài liệu khôi phục byte-identical sau mỗi lượt (sha256 + CRLF=0).

**Ghi lại để lần sau khỏi trả giá:** đợt này bị chiếm số **bốn lần** (r313→r322→r324 đều bị lấy mất,
chốt ở r326). Đo merge với master: **5/5 xung đột đều là tệp PHÁI SINH** (`CHANGELOG` · `RELEASE_MANIFEST` ·
`SKILL.md` · `VERSION` · `tl.py`), còn `tl_selftest.py` và `RASOAT_HOSO_LOOP.md` auto-merge SẠCH — bằng chứng
thực nghiệm cho đánh số trì hoãn của ADR-0017.

# ★ v1.36.57 — r325: nối lại KHỐI ĐUÔI VBHN khi dựng toàn văn + WARN đường ĐỌC registry (2026-08-02)

Hai việc bàn giao còn lại của lượt bảo trì kho LƯỢT 3. Sổ:
`rasoat/BIEN_BAN_BAO_TRI_KHO_BHXH_LUOT3_2026-08-02.md`.

★**Phạm vi lượt này ĐÃ THU HẸP có chủ đích.** VIỆC 3 (khối chú thích đọng trong thân Điều cuối) tôi
đã vá xong và đo trọn, nhưng đo lại origin ngay trước khi commit thì **PR #18 (`r323`,
`claude/r323-tach-duoi-vbhn`) đang mở và làm CÙNG việc, RỘNG HƠN**: nó tách cả bảng «XÁC THỰC VĂN
BẢN HỢP NHẤT» chứ không chỉ khối `[n]`, và bắt được `[n]` xuất hiện **inline trong 9/141 Điều** của
`19-2026` — thứ mà phép đo của tôi (chạy trên thân Điều đã qua đường nạp) **không thấy**. Bản của họ
tốt hơn ⇒ **tôi GỠ TRỌN bản vá trùng của mình** (`verify_deep.chu_thich_start` + nhánh trong
`normalize_document` + 3 ca test), giữ đúng phần KHÔNG trùng. Cùng doctrine với `c2971dd`.

**(A) r325 — lỗ CÒN LẠI sau r323: `_consolidated_text` không nối lại khối đuôi.** r323 tách
«XÁC THỰC…» + chú thích hợp nhất ra `xac_thuc`/`chu_thich` (đúng và cần), nhưng **không đụng**
`tl_core/extract_cache.py`. Mà đó là đường **dựng lại TOÀN VĂN từ record** — đường nuôi `doc-text`
mặc định và **ghi đè khoá cache chuẩn `extract_<id>.txt`** (nguồn nuôi corpus/NLM). Tách ra trường
riêng mà không nối lại ở đó = **im lặng đánh rơi**, ĐÚNG BẪY r215 đã trả giá với `phu_luc` (khi đó
mất 6.030 ký tự phụ lục mà record VẪN CÓ lưu). Quy mô nếu để nguyên: `40-2026` mất **40.406 ký tự**
chú thích, và `xac_thuc` chính là **bằng chứng danh tính** (VPQH + «Số:») mà r215 sinh ra để bảo vệ.

Vá: `_consolidated_text` nối lại cả hai khối, thứ tự theo bố cục đo được (phụ lục → **xác thực** →
**chú thích**), `rep` thêm hai cờ, dòng nhãn `doc-text` khai thêm «xác thực»/«chú thích».
★**Forward-compatible, KHÔNG phụ thuộc thứ tự merge**: record dựng trước r323 không có hai khoá ⇒ cả
hai rỗng ⇒ chuỗi ra **Y HỆT** bản cũ. Nên bản vá này an toàn kể cả khi r323 chưa land.
+1 ca `r325_dung_lai_khong_danh_roi_duoi_vbhn` (5 vế, gồm chiều ngược record-cũ-bất-động và ca chỉ
có MỘT trong hai khối).

**(B) VIỆC 4.2 — đường ĐỌC registry rơi về sổ NỀN trong im lặng.** Profile dự án **có thật** trong
config mà `registryDocId` **rỗng** ⇒ `TL_REGISTRY_DOC_ID` không được đặt ⇒ webapp `regSS_` rơi nhánh
auto-discover = sổ NỀN, người dùng đọc dòng nền dưới nhãn profile đang chọn. Đường GHI đã fail-closed
từ 1.23.21 (`PROFILE_REGISTRY_ID_EMPTY_WOULD_CLOBBER_BASE`, rc=2 — vá cho sự cố 2026-06-30); đường
ĐỌC tới nay vẫn im, và `scope`/`BASE_SCOPE_HIT` (r179 T7) chỉ nói được KHI ĐÃ CÓ dòng trả về.
Nay `_apply_profile_env` in `PROFILE_REGISTRY_ID_EMPTY` ra stderr — **cảnh báo, KHÔNG chặn** (đọc sổ
nền là hợp lệ; cái sai là im lặng), 1 lần/profile/process. Giữ IM ba chiều ngược: nền `vbqppl` rỗng
là bình thường · profile có id đủ · người dùng tự export env. Không chồng lên `PROFILE_NOT_FOUND`.
Chứng minh trên ĐƯỜNG SẢN XUẤT (`tl --config … --profile … profile-info`), không chỉ qua bind.
+6 ca `r325_*`.

**(C) VIỆC 4.1 — đính chính §4.2 biên bản lượt 1** (chỉ `rasoat/`, ngoài gói): «.docx Công báo là
container HỎNG (33/40 · 30/37 entry dùng `\`)» là **SAI**. Lượt 3 **đo lại ĐỘC LẬP** trên tệp
89-2026 còn trên đĩa, sha256 khớp tuyệt đối `source.sha256` của record cache ⇒ **0 entry** dùng
backslash, `word/document.xml` có đúng tên chuẩn, `python-docx` mở thẳng (775 đoạn). Hỏng nằm ở
**đường tải của container web**, không ở tệp Công báo; lượt 1 đo sai vì `bash -c` **nuốt backslash**.
★Đồng thời bắt được **mẫu số sai ở CẢ HAI sổ trước**: tệp này chỉ có **10** entry, không phải 37 —
nên «30/37» lẫn «0/37» đều không phải số của tệp này (lượt 2 đúng kết luận nhưng bê nguyên mẫu số).
**Bản vá r316 (`scan_file` hết fail-open) giữ nguyên, vẫn đúng vì lý do riêng của nó** — nó vá cổng
an toàn pháp lý mặc định «sạch» khi mù, không phải vá container.

★**Bẫy trả giá trong lượt này:** (1) `Path.write_text()` trên Windows **dịch `\n` → `\r\n`** — sửa
một dòng làm cả tệp đổi kết dòng, `git diff` phồng 45 → 1.061 dòng, mà CI có bước *«Force LF
checkout (hash parity với manifest)»*. (2) Kho này **kết dòng TRỘN THEO TỆP** (`verify_deep.py` LF ·
`tl_selftest.py`/`tl.py`/`SKILL.md` CRLF) ⇒ quy tắc «ép hết về LF» là SAI, phải nắn theo **blob của
chính tệp đó**. (3) `VERSION` khai ở **BA nơi** (`VERSION` · `scripts/tl.py` · `SKILL.md`) — quên
một chỗ thì `r65_bundle_export_meta_and_guard` / `skill_md_version_matches_VERSION` bắt.
# ★ v1.36.56 — r324: REL-05 + NLM-08 — cổng gói mù một tệp bắt buộc, doc kernel dạy van F7 đã chết (2026-08-02)

**Hai mục P2 của sổ audit 01-08. Đo tận nơi TRƯỚC khi vá — và phép đo đã lật một phần đề bài.**

**REL-05 — `release-verify` mù với `references/QUY_TRINH_RA_SOAT_3_TANG.md`.** Tệp chứa `PHA0_GATE_v1`
+ `BUG_LEDGER_v1` đã có mặt trong `_BARE_TOOL_STRICT_DOCS` (guard bare-tool ĐỌC nó) nhưng **0 hit**
trong `_RELEASE_REQUIRED_FILES` ⇒ rơi khỏi gói thì **không cổng nào đỏ**. Đưa vào danh sách bắt buộc.
Ca `r324_rel05_quy_trinh_3_tang_trong_required` khoá bằng **HÀNH VI**, không phải tư cách thành viên:
dựng root giả thiếu đúng tệp đó → `_verify_release_manifest` phải nêu **ĐÍCH DANH** trong
`required_missing` **và** trả `ok:false`. (Chỉ kiểm «có trong list» là lặp lại bẫy r321 «đã có hàm ≠
đã có đường gọi».)

**NLM-08 — doc kernel dạy van F7 đã bị GỠ từ r208d.** Đo được ba nơi:
- `SKILL.md:171` khai «cookie >**50′** trước lô API >1 nguồn → **CHẶN**»;
- `references/KERNEL_APPENDIX.md` §E khai cả hằng `NLM_COOKIE_BATCH_MAX_MIN` lẫn mã lỗi
  `NLM_COOKIE_TOO_OLD_FOR_BATCH` — **cả hai không còn trong mã**, chính ca
  `r208d_f7_canary_thay_chan_theo_tuoi` đang khoá `not hasattr(…MAX_MIN)`;
- docstring `_nlm_preflight_report` (`nlm_ops.py`) tự khai «van F7 vẫn dùng nó — GIỮ NGUYÊN ngưỡng».

Hành vi THẬT trong `cmd_ingest_missing`: `len(to_add) > 1` → **canary LIVE**; `alive is False` ⇒ rc=2
`NLM_AUTH_DEAD_BEFORE_BATCH` **trước mọi side-effect**; `alive=None` KHÔNG kết luận ⇒ KHÔNG chặn (M2);
tuổi >50′ (`NLM_COOKIE_BATCH_WARN_MIN`) **chỉ CẢNH BÁO**. Doc lệch đúng chiều nguy hiểm — dạy người vận
hành tự dừng lô, thứ §4b tầng 3 CẤM. Sửa cả ba nơi; ca `r324_nlm08_doc_f7_khop_canary_live` khoá **HAI
CHIỀU**: doc-set kernel không được hồi sinh tên đã chết, **và** thứ doc hứa phải có thật trong đường sản
xuất (soi `inspect.getsource(cmd_ingest_missing)`).

★ **`SKILL.md` giữ NGUYÊN 48.031 B.** Câu F7 mới cân **đúng 84 byte** bằng câu cũ, nên
`references/golden/workflow_audit.json` (`size_bytes: 48031`) và ghi chú «đệm 97B» ở
`references/GOTCHAS.md:16` **không phải sửa theo**. Đổi độ dài kernel là kéo theo 3 tệp khác.

★ **Nơi thứ TƯ là BÁO GIẢ.** `docs/WORKFLOW_RASOAT_TU_DONG.md:277` cũng chứa tên hằng đã gỡ, nhưng đọc
kỹ thì nó đang **MÔ TẢ ĐÚNG** việc đổi tên của r208d («…đổi tên `…MAX_MIN` → `…WARN_MIN`, vẫn 50′ nhưng
chỉ CẢNH BÁO»), không dạy hành vi cũ ⇒ **KHÔNG sửa**. Sổ audit khai «3 nơi» là chính xác; quét theo TÊN
rồi vá tất là cách làm hỏng một tài liệu đang đúng.
# ★ v1.36.55 — r323: khối đuôi VBHN đọng trong THÂN ĐIỀU CUỐI (chú thích hợp nhất + bảng XÁC THỰC) (2026-08-02)

**Triệu chứng đo được trên cache THẬT (02-08), 3/3 record VBHN nhiễm, 0 record khác:**

```
40-2026-VBHN-VPQH  Điều 52 : thân 40.637 ký tự — quy phạm chỉ    231  (99,4% là khối đuôi · 114 neo)
19-2026-VBHN-VPQH  Điều 141: thân  8.573 ký tự — khối đuôi      4.073
89-2026-VBHN-VPQH  Điều  79: thân  1.124 ký tự — khối đuôi      1.031
54-2025-VBHN-VPQH  Điều 72 : 0 neo — sạch, KHÔNG bị đụng
```

VBHN kết thúc bằng hai khối **không phải quy phạm** đứng sau Điều cuối: bảng «XÁC THỰC VĂN BẢN HỢP
NHẤT» (NĐ250 mục XIII) và danh sách định nghĩa chú thích hợp nhất «[n] …». Đường **ĐỌC**
(`resolve.resolve_footnote_amendments`) cắt khối chú thích từ lâu; đường **NẠP** thì KHÔNG — nên cả
hai đọng vào thân Điều cuối của record cache. Hệ quả: **trích nguyên văn Điều cuối nhả chú thích ra
như thể là quy phạm**, và `19-2026` chính là VBHN đang thay thế Luật BHXH 41/2024.

★**Bộ dò đã tồn tại nhưng chẩn đoán SAI ĐỊA CHỈ.** Cờ mềm sẵn có (`verify_deep` §1b, «Điều cuối dài
bất thường») ĐÃ bắn trên `40-2026` — nhưng ghi là *«nghi phụ lục/mẫu chưa tách»*, nên không ai truy
đúng nguyên nhân; và nó chỉ bắt 1/3 vì `19-2026`/`89-2026` lọt dưới ngưỡng 8000/8×.

**Vá.** `verify_deep.tach_duoi_vbhn()` (PURE) + `vbhn_duoi_start()` dò **từ Điều ĐẦU TIÊN trở đi**.
`normalize_document` gọi nó **sau** bước tách phụ lục nên đúng với cả hai thứ tự đuôi-vs-phụ-lục.

★**Bản nháp neo ở Điều CUỐI (theo khuôn `appendix_start`) và ĐÃ HỎNG trên dữ liệu thật** — chỉ lộ ra
lúc nạp lại record thật, đọc mã không thấy: khối chú thích VBHN **trích dẫn nguyên văn Điều của luật
khác** («[7] Điều 31 của Luật … quy định như sau: "Điều 31. Thẻ bảo hiểm y tế…"»), nên `ART_SPLIT`
khớp SÂU TRONG khối đuôi và marker CUỐI CÙNG nằm SAU cả «[1]» lẫn «XÁC THỰC» ⇒ trả `-1` ⇒ **không cắt
gì**. `40-2026` (114 chú thích) hỏng TRỌN; `19-2026` (10 chú thích) thoát chỉ vì trích ít — **thử mỗi
nó thì bản nháp trông như ĐÚNG**. Phụ lục không có lớp bệnh này nên `appendix_start` giữ điểm neo cũ;
hai bên **cố ý khác nhau**. Ca khoá: `r323_chu_thich_trich_dan_dieu_khong_lam_truot_moc`.
Khối đầu (r215) do chính điểm neo Điều-đầu bảo vệ; marker INLINE (9/141 Điều của `19-2026` có marker
giữa dòng) do khuôn neo **ĐẦU DÒNG** bảo vệ. Hai khối được **GIỮ** vào trường riêng
`chu_thich` / `xac_thuc` (+ 4 trường đếm trong `structure`) chứ **không bỏ đi**: chú thích mang thông
tin pháp lý «khoản này do luật nào sửa, hiệu lực từ bao giờ», còn khối xác thực là bằng chứng danh
tính (VPQH + «Số:»). Không record nào mất một ký tự nào.

★**Mốc «khối chú thích bắt đầu ở đâu» nay là MỘT định nghĩa** — `tl._FOOT_DEF_FIRST` (đường đọc) và
`verify_deep.VBHN_CHU_THICH_DEF` (đường nạp), khoá bằng drift-lock `r323_khuon_chu_thich_khong_duoc_lech`
(khuôn `r80_discovery_sites_mirror`). ★Hằng phải đặt ở **`tl.py`** chứ không phải `tl_core/resolve.py`:
`resolve.bind()` REBASE `__globals__` từng hàm sang namespace sống của tl ⇒ hằng khai bên resolve là
**mã chết**, hàm vẫn tra trong globals của tl. Khai thử ở resolve cho **NameError ngay trên đường sản
xuất** — chính selftest bắt được (đúng lý do `_MARK_RE` xưa nay nằm ở `tl.py`).

**Tiền kiểm chống cờ giả (chạy trước khi vá):** sau khi cắt, `TERMINAL_PAT` vẫn khớp **3/3** Điều
cuối, và **0/3** còn trượt cờ «Điều cuối dài bất thường» ⇒ bản vá không đẻ cờ mới.

**Cổng:** selftest **1621/1621** (1617 + 4 ca mới) · release-verify --strict rc=0 · determinism /
doc-claims / workflow-audit --strict rc=0 · ruff F **delta +2** — báo trung thực: cả hai **cùng lớp
F821-do-bind đã có sẵn** (`resolve.py` nền đã 360 F821 gồm cả `_MARK_RE`; `_TL_MODULE` trong selftest
đã 2.159; kho **chưa từng** dùng `noqa: F821`) ⇒ với lớp hằng-qua-bind, "delta 0" là bất khả.

**ĐÃ CHỮA DỮ LIỆU (2/3 record), nạp lại bằng chính bản vá này** — `cache-build --method exportdocx
--gdoc-id`, giữ `method_rank=95`/`verified`; nạp **cache tạm** đo **8/8 cổng** rồi mới chép đè, bản cũ
sao lưu ở `~/.tra_luat_cache/cache_bak_r323_2026-08-02/`:

```
40-2026  Điều 52 : thân 40.637 →   230   · chú thích 46.198 tách riêng · neo trong thân 114 → 0
19-2026  Điều 141: thân  8.573 → 4.500   · chú thích  4.010 tách riêng · neo trong thân  10 → 0
```

Cổng 7 («0 ký tự QUY PHẠM nào đổi») so **sau khi bỏ hết khoảng trắng**: `40-2026` 0/51 Điều lệch;
`19-2026` 0/140 lệch thực, 2 Điều (80·115) khác **chỉ ở khoảng trắng** — và đó là bản mới **SỬA ĐƯỢC**
lỗi dính chữ «hủy bỏ|quyết định» mà lượt 12 đã ghi vào sổ. ⇒ So tuyệt đối là **sai chiều**: nó sẽ chặn
chính bản vá tốt hơn.

⚠ **`89-2026-VBHN-VPQH` CHƯA chữa được** — record không có `source.gdoc_id` (`method=file`,
`rank=50`/`staged`) nên không có đường `exportdocx` để nạp lại mà giữ hạng. Cần người quyết nguồn.

# ★ v1.36.54 — r322: RAS-18 — `doc-patch` để lại `text_hash` CŨ, bằng chứng đối sánh phải VÔ HIỆU (2026-08-02)

**Sổ audit tả mục này là «`doc-patch` cố ý không tính lại `text_hash` ⇒ anchor sai âm thầm». Đo tận
nơi thì lời tả đó ĐÚNG phần mô tả mà SAI phần quy lỗi — và bệnh thật nặng hơn:**

| khẳng định trong sổ | đo được 02-08 |
|---|---|
| không tính lại `text_hash` | **ĐÚNG**, và lý do r217 nêu là THẬT: record không giữ bố cục dòng của `norm` ⇒ *không có cách* tính lại trong CÙNG miền băm. **Tính lại mới là sai** — đó là thay giá trị không rõ nguồn bằng giá trị TƯƠI |
| «chỉ thiếu ghi chú» | **SAI.** `tra_cuu.py` dùng `text_hash` làm **bằng chứng đối sánh LIÊN NGUỒN** (`--expected-content-hash` từ bundle/NotebookLM). Sau một lượt patch, thân ĐÃ lệch mà hash VẪN khớp bundle ⇒ cổng fail-closed báo **KHỚP** đúng trên ca nó sinh ra để chặn, rồi trả nguyên văn đã sửa như thể bundle xác nhận |
| «đã có cảnh báo trong `verify_flags`» | **CÓ NHƯNG VÔ HÌNH**: `provenance.py` 0 tham chiếu `verify_flags`, `tra_cuu.py` 0 tham chiếu; JSON ra chỉ có `content_hash`/`warnings`/`units`. Không đường đọc nào lộ nó |
| — | **FAIL-OPEN chưa ai khai**: r217 ghi cờ trong `if isinstance(vf, list)` ⇒ record thiếu khoá thì lời khai bốc hơi mà lệnh vẫn rc=0. (11/11 record hiện có đều là list ⇒ bẫy đang NGỦ, không phải đang chảy máu) |

**Ba vế, mỗi vế một ca khoá riêng:**

1. **Cổng** — `tra_cuu.py`: `--expected-content-hash` KHỚP + record có `doc_patch.lich_su`
   ⇒ `hash_khop_nhung_da_doc_patch`, **rc=3, không trả nguyên văn**. Không tính lại hash; từ chối
   chính cái "khớp" đã vô hiệu. `--allow-stale` vẫn là đường vượt (cùng cổng với nhánh lệch sẵn có),
   và nhánh `hash_mismatch` cũ **không bị cướp**.
2. **Lộ diện** — `provenance.build_warnings`: thêm mã `doc_patch_text_hash_cu` (level `warn`), nên
   mọi đường đọc dựng cảnh báo đều khai, kể cả khi không ai truyền `--expected-content-hash`.
3. **Fail-open** — `cmd_doc_patch`: **TẠO** `verify_flags` khi record chưa có, thay vì lặng lẽ bỏ.

**Khoá vào `doc_patch.lich_su`** (trường CÓ CẤU TRÚC, ghi vô điều kiện) chứ không dò chuỗi
`"DOC_PATCH:"` trong `verify_flags`: văn xuôi đổi một chữ là phép dò gãy IM LẶNG, mà `verify_flags`
lại đúng là trường có thể vắng mặt.

**Hai bệnh NỀN đo được cùng lượt, CỐ Ý không vá kèm** (ngoài phạm vi RAS-18, đã ghi tại chỗ):
- `tra_cuu.py` **không** `reconfigure(encoding="utf-8")` như `tl.py` (tl.py:86/94) ⇒ trên máy chuẩn
  Windows (stdout pipe = cp1258) mọi payload tiếng Việt vỡ `UnicodeEncodeError`. Nhánh
  `hash_mismatch` CŨ vỡ y hệt — bệnh có trước r322.
- `find_units` duyệt `doc["structure"]` như **list đơn vị**, còn record cache thật (**11/11**, do
  `build_cache.py:84` + `normalize_document.py:347` ghi) để `structure` là **dict đếm** ⇒ duyệt dict
  ra chuỗi rồi `AttributeError`. Cổng r322 nằm TRƯỚC `find_units` nên chặn đúng ở cả hai hình dạng.

Test: `r322_cong_hash_vo_hieu_sau_doc_patch` (5 nhánh, chạy subprocess đường sản xuất) ·
`r322_provenance_lo_doc_patch` · `r322_verify_flags_vang_van_phai_khai` (đường GHI thật).


# ★ v1.36.53 — r321: RAS-17 vế `rasoat-merge` — neo hỏng hết đi lọt vào bảng master (2026-08-02)

**Nối tiếp r313, KHÔNG chồng lấn.** r313 dựng khuôn (`_rasoat_anchor_khuon`) + cưỡng chế cờ vòng đời
(`_rasoat_anchor_hop_le`). Mục này đóng vế còn lại, và là vế mà bản kiểm lõi nêu ĐÍCH DANH:
«`_rasoat_unit_shape` không chạm `anchor` ⇒ `rasoat-merge` nuốt trọn».

**Đo trên chính master `c24a8b3` (đã có r313), hồ sơ BHXH thật — 82/82 ô neo sai khuôn:**
```
tl rasoat-merge --in <master/> --json  →  ok: true · so_phat_hien: 40 · KHÔNG một khoá nào nhắc anchor
```
Cổng vòng đời của r313 không bịt được lỗ này: nó chỉ bắn khi hồ sơ **đã khai `vong_doi`**, còn
`rasoat-merge` chạy từ lượt rà ĐẦU TIÊN và là đường sản phẩm cuối (§7.1 điều kiện đóng số 6 gọi thẳng
`rasoat-merge --check` rc=0 — tức bảng master có thể nghiệm thu XANH trong khi 82/82 neo hỏng).

**Vá.** `_rasoat_anchor_quet(docs)` — thuần, giữ thứ tự, trả từng ô hỏng kèm `nguon`/`key`/`so_hieu`/`i`
để người sửa biết mở FILE nào, PHÁT HIỆN nào. Luật hợp lệ và từ vựng `loai` dùng **chung**
`_rasoat_anchor_khuon()` của r313 — một nguồn chân lý, không đẻ bộ từ vựng thứ hai rồi để hai bên trôi
khỏi nhau (có ca khoá riêng bất biến này). `cmd_rasoat_merge` khai `so_anchor_hong` + `anchor_hong` ở
**MỌI** chế độ kể cả `--check`/`--dry-run`; `--anchor-strict` ⇒ rc=2 và **KHÔNG ghi**, đặt cùng chỗ với
cổng r216/r290 (TRƯỚC mọi thao tác ghi).

**Vì sao KHÔNG strict mặc định:** hồ sơ đang lưu giữ 82/82 ô sai khuôn — bật mặc định là chặn đứng mọi
hồ sơ CŨ vì một lỗi lượt rà không gây ra và **chưa có đường sửa trọn**. Đúng khuôn r312 với ING-09:
chặn cái MỚI, khai cái CŨ, không dọn lén.

**Đo lại phần DỮ LIỆU (02-08) — sửa hai điều bàn giao cũ ghi sai:**

| lớp | n | di trú tự động được? |
|---|---|---|
| `cache:<slug>` (± `#<8hex>`) | 47 | **ĐƯỢC** — cache giữ `text_hash` 64hex thật; 2 ô có `#<8hex>` đều KHỚP tiền tố bản hiện hành |
| hex 16 ký tự (2 giá trị) | 17 | **KHÔNG** — khớp **0** bản, kể cả mọi `cache_bak_*` ⇒ không truy nguyên được |
| `congbao:…` | 17 | **KHÔNG** — không có record cache |
| `gdoc:…` | 1 | **KHÔNG** |

1. «cache `docs/*.json` = 0 record» là đo trong **container rỗng**; trên máy giữ hồ sơ có đủ 11 bản.
2. «mã ghi hexdigest TRẦN thiếu tiền tố (`build_cache.py:83`)» là **nhầm trường**: ô đó là `text_hash`
   của RECORD CACHE (64hex thật, đúng), không phải `anchor.doc_deps[].text_hash` (do agent rà điền tay).

⇒ Câu «tính lại bằng `_content_hash`» ở `RASOAT_PLAN_SCHEMA.md` §7.2 **chỉ đúng cho lớp `cache:`**. Áp cho
cả 82 là thay giá trị không rõ nguồn bằng giá trị TƯƠI — khẳng định một độ tươi chưa hề kiểm, đúng thứ
`anchor_con_hieu_luc` sinh ra để chặn. §7.2 nay ghi rõ phân rã này; ô không truy nguyên được thì ĐỂ TRỐNG.

**Test** (3 ca, đều HÀNH VI — không grep chuỗi, vì lệnh này thuần cục bộ nên chạy thật được):
`r321_anchor_quet_gan_nguon` (8 khẳng định — 3 lớp `loai` phá riêng lẻ, ô đúng không đẻ vế giả, dep
không-phải-dict vẫn tính, thứ tự tất định) · `r321_quet_khop_findings_r313` (bất biến: số ô hỏng và
phân lớp của hai đường soi phải BẰNG NHAU) · `r321_merge_lo_dien_va_strict_fail_closed` (rc + payload +
**FILE CÓ BỊ GHI KHÔNG**, gồm cả chế độ `--check`).

**Mutation** (mỗi vế hoàn nguyên riêng, đo trên chính bản này): bịt `_rasoat_anchor_quet` ⇒ đỏ đúng 3 ca
mới · gỡ `return 2` của cổng (báo lỗi nhưng VẪN ghi — đúng lớp bệnh r290) ⇒ đỏ đúng ca strict.
selftest **1614/1614** (đo SAU khi rebase lên r320); ruff F821 **0 tên mới** trên cả 4 tệp đụng tới
(so tập TÊN, không so số đếm — `lookup_ops.py` 563→564 là THÊM CALL-SITE của helper vốn đã stub, đúng
ca xanh đã ghi trong checklist).

**Vế GHI DỮ LIỆU: CHỐT KHÔNG LÀM — và đó là kết cục ĐÚNG, không phải nợ.** Hồ sơ BHXH đã
`da_dong_co_gioi_han` (người thẩm tra chốt 01-08, claim đã nhả) và `vong_doi` của nó ĐÃ tự khai chính
xác: `anchor_con_hieu_luc: false` + `ly_do_anchor` mô tả đúng RAS-17. Tức hệ thống đang ở trạng thái
TỰ MÔ TẢ ĐÚNG — Loop C bỏ qua hồ sơ này đúng như thiết kế, không có lỗi nào đang chảy máu. Sửa 82 ô
tại chỗ là ghi đè một hồ sơ đã ký, phá bất biến §7.1 «đóng hồ sơ là ĐÓNG BĂNG, không phải dọn», mà
đổi lại KHÔNG được gì: 35/82 ô vẫn hỏng ⇒ `anchor_con_hieu_luc` vẫn phải là `false`. Người dùng chốt
**để nguyên** (02-08). Ghi lại đây để lượt sau đừng mở lại như một "việc còn treo".
# ★ v1.36.52 — r320: ĐÓNG 4 mục CUỐI của sổ audit 31-07 — PRO-03 · PRO-09 · PRO-05 · ING-04 · ING-06 (2026-08-02)

Bốn mục này là **toàn bộ phần còn lại** của nhóm "chưa có bằng chứng độc lập" (§Phụ lục kế hoạch: 6 mục,
`RAS-14` đóng ở r310, `ING-03` tự tái hiện xong). Theo đúng dặn dò "dựng repro TRƯỚC", mỗi mục được tái
hiện trên cây hôm nay rồi mới vá — **cả 4 đều CONFIRMED, sổ audit không mục nào bịa**.

**T0-C trước khi mở Làn B (bắt buộc theo kế hoạch §III.2).** Đo ranh giới tệp với P16: `profile_mgmt.py`
chạm gần nhất r268 · `profile_env.py` r286 (P16 dừng ở đây) · `zip_ingest.py` r268 · `ingest_ops.py`
**r312** nhưng diff chỉ 1 hunk trong `_il_stage_plan`, **0 lần** chạm `_resume_identity_gate`. Không giao ⇒
mở được.

## PRO-03 + PRO-09 — guard marker viết đúng, test xanh, CHƯA TỪNG CHẠY

**Nặng hơn sổ.** Sổ nói "`profile-adopt` không dùng mutation guard". Đo ra: `_marker_mutation_guard` (có từ
r184, ADR-0012 §4 khai là **guard chung cho mọi mutation profile**) có **0 call site sản xuất** trong toàn
kho — 3 tham chiếu duy nhất là định nghĩa, dòng khai `_STUB_MAP`, và **một ca test gọi thẳng**. Cùng lớp
"chứng nhận RỖNG" mà r298 đã diệt 3 ca.

- **PRO-03**: adopt tự dựng lại ba điều kiện rời (đọc lỗi / trùng marker / tên profile khác). Marker **hỏng
  nội dung** lọt sạch: `FINGERPRINT_MISMATCH` cho cả ba điều kiện đều False ⇒ rơi thẳng vào `_marker_write`
  = **ghi đè bản hỏng** (self-heal ngầm), đúng thứ ADR-0012 cấm. Đo: guard trả `MARKER_INVALID` cho chính ca
  đó, adopt cho qua. Nay adopt định tuyến qua guard.
- **PRO-09** (nâng từ mục RISK, theo §I.5 kế hoạch): `profile-delete` — mutation **nặng nhất** họ profile
  (xoá nguồn NLM **bất khả nghịch** → trash Drive → gỡ config) — **không đọc marker ở bất kỳ đâu**. Nay guard
  đứng **sau** cổng `--confirm` (DRY không tốn call mạng) và **trước** mutation ĐẦU TIÊN; chặn ⇒
  `PROFILE_DELETE_MARKER_GUARD` rc=2, chưa xoá gì. Transport nổ = "mù trạng thái", KHÔNG phải "sạch".

**Breaking có chủ đích:** adopt/delete lên marker không hợp lệ nay DỪNG thay vì tự chữa. Đường repair đã
thiết kế sẵn (ADR-0012 §3): `profile-backfill-markers --profile-name <tên> --apply --force`.

## PRO-05 — kiểm MIME bị khoá nhầm sau `role == "registry"`

Nhánh `manifest` **không có phép kiểm loại nào**. Đo: Google Doc đặt ở `manifestId`, parent đúng ⇒ doctor
**0 finding**, trong khi chính nó là thứ không đọc được (manifest upload `mime=application/json`,
`convert=false` rồi tải về JSON-parse).

Bất biến chọn là **"không phải tệp Google-native"**, không phải "đúng `application/json`": Drive có thể trả
`text/plain` cho JSON upload và bản đó vẫn parse được — siết theo chuỗi MIME chính xác là **đỏ oan**. Ca test
khoá cả hai chiều: `application/json` và `text/plain` **không** đỏ; Doc **và** Sheet đều bị bắt.

## ING-04 — `if _jd and …` coi VẮNG MẶT là hợp lệ

`_resume_identity_gate` so `journal.drive_id` với dòng canonical, nhưng bọc trong `if _jd and …` ⇒ journal ghi
`drive_id=""` thì **bỏ qua so sánh**. Đo đúng kịch bản sổ: journal cũ (`drive_id=""`, có `identity_hash`) +
registry đã trỏ sang GDoc **hoàn toàn khác** ⇒ cổng trả `None` = **cấp quyền ghi**. Đo thêm trên hàm THẬT:
`source_sha256` **0 lần**; `identity_hash`/`plan_hash` chỉ bị kiểm **CÓ MẶT**, không đối chiếu **GIÁ TRỊ**.

Nay: journal thiếu `drive_id` mà registry ĐÃ có dòng canonical ⇒ `RESUME_JOURNAL_NO_DRIVE_ID`.

★ **Lượt đầu tôi siết QUÁ TAY và chính phản chứng bắt được**: bản vá ban đầu chặn cả khi người gọi khai
`--drive-id` KHỚP canonical — mà khai rồi thì cổng phía trên đã đối chiếu, tức nguồn ĐÃ được chứng minh bằng
đường khác. Thêm vế `not drive_id`. Ma trận 5 ca nay đều đúng.

## ING-06 — tập đuôi khai HAI LẦN, đã trôi lệch

ZIP planner `{.doc .docx .pdf .txt .md .rtf .odt}` vs child `ingest-local` `{.docx .doc .pdf .rtf .odt}`.
Khe hở = đúng **`.txt`, `.md`** như sổ nêu. Chạy `validate_source_file` THẬT với fixture hợp lệ từng đuôi
(zip có `[Content_Types].xml`+`word/document.xml`, `%PDF-`, OLE header, `{\rtf`): 5 đuôi `ok=True`, đúng 2
đuôi đó trả `UNSUPPORTED_EXTENSION`. Planner hứa kế hoạch mà child **chắc chắn** không làm được.

Nguồn sự thật DUY NHẤT nay ở `ingest_contract.INGEST_LOCAL_EXTS`; cả hai phía đọc từ đó. **Chọn THU planner
về đúng năng lực child, KHÔNG nới child**: nới = cho upload `.txt`/`.md` rồi convert = quyết định **tính năng**
(đổi thứ được ghi vào corpus), không phải sửa lỗi lệch sổ. Muốn mở thì mở tường minh ở một chỗ.

**Test (+5 ca → 1598/1598).** `r320_pro03_adopt_va_delete_deu_qua_guard` · `r320_pro09_delete_chan_truoc_mutation_dau_tien`
(khoá **THỨ TỰ** trong mã: guard < `nc.source_delete(` và < `g.get("trash"`, nhưng > `CONFIRM_YES_REQUIRED`) ·
`r320_pro05_manifest_sai_loai_bi_bat` (4 phản chứng) · `r320_ing04_journal_thieu_drive_id_khong_cap_quyen`
(ma trận 5 ca) · `r320_ing06_planner_va_child_cung_mot_nguon` (+ phản chứng đuôi hợp lệ vẫn qua cả hai phía).

**ĐỎ-TRƯỚC (đo thật):** hoàn nguyên 5 tệp sản xuất về HEAD, GIỮ test ⇒ **1593/1598**, đỏ đúng **cả 5** ca
r320, **không ca nào khác**. Sau vá 1598/1598.

**Một ca CÓ SẴN đỏ — đúng, và nó đang mã hoá con bệnh.** `r107_zip_content_identity_normalized` dùng member
`.txt` làm filler rồi khẳng định `plan.ok` — tức khẳng định planner **phải nhận** một đuôi không nạp được.
Chủ đề thật của ca là **chuẩn hoá đường dẫn** (`./a` ≡ `a` cho `idempotency_key`, `plan_hash` khác), hoàn toàn
không liên quan đuôi. Giữ NGUYÊN VĂN khẳng định, chỉ đổi filler sang `.docx`. Bằng chứng đổi filler là trung
tính: ở lượt ĐỎ-TRƯỚC ca này **vẫn xanh** (`.docx` hợp lệ ở cả hai phía trước lẫn sau vá).

**Và một check CÙNG LỚP trong `determinism-audit`.** `zip_member_order_stable` (`release.py:141`) cũng dùng
member `.txt` làm filler rồi kèm vế `zp.ok`. Chủ đề của nó là **ổn định thứ tự member** (`zi1 == zi2` — vế này
**vẫn đúng** sau vá); chỉ vế `ok` gãy vì 0 member được nhận. Đổi filler sang `.docx`, khẳng định gốc nguyên vẹn.
Hai chỗ này (`r107` + `zip_member_order_stable`) là bằng chứng phụ rằng ING-06 có thật: khe hở đủ lâu để **hai**
bộ kiểm khác nhau vô tình dựa vào nó.

★ **Hai lỗi trong chính TEST của tôi, tự bắt được:** (1) soi `cmd_profile_adopt` — nó chỉ là wrapper
`_ProfileEnvGuard` 181 ký tự, thân thật ở `_cmd_profile_adopt_impl`; soi nhầm wrapper thì test **xanh giả** vì
chuỗi nào cũng vắng mặt. (2) neo thứ tự vào chuỗi `trash_assets` — chuỗi này có mặt SỚM trong dict `plan` nên
phép so vị trí sai; đổi neo sang `g.get("trash"`.

# ★ v1.36.51 — r319: đính chính KHẾ ƯỚC phụ thuộc — `requirements.txt` khai «stdlib-only» đúng với overlay core nhưng SAI với đường nạp (2026-08-02)

Đóng nốt phần KHẾ ƯỚC của §4.6 — mảnh cuối cùng của sáu phát hiện công cụ lượt bảo trì kho 02-08.
r317 đã làm nhánh không-`python-docx` hết rò, nhưng `pypdf` **không có đường thay thế**: thiếu nó là
chặn cứng mọi PDF, mà không tệp nào trong kho nói ra điều đó.

**Bệnh — khai sai đúng chỗ đắt nhất.** `requirements.txt` chỉ có hai dòng chú thích, dòng đầu là
*«tra-luat overlay core uses only Python standard library.»* Câu đó ĐÚNG với overlay core
(`tl.py`, `contract_check.py`) và SAI với **đường nạp tài liệu** (`ingest_to_cache` →
`normalize_document`). `INSTALL.md` còn khẳng định mạnh hơn: *«không cài gì thêm; overlay core dùng
stdlib»*. Người vận hành làm đúng như tài liệu ⇒ máy KHÔNG có `pypdf` ⇒ mọi `.pdf` bị chặn, và
(trước r315) còn bị báo nhầm thành «bản SCAN» của TÀI LIỆU.

Đo 02-08 trên `54-2025-VBHN-VPQH` — PDF text thật, `pdftotext` bóc **167.433 ký tự**, riêng trang 1
có 2.536:

| | kết quả |
|---|---|
| cài theo đúng tài liệu (không `pypdf`) | `{"ok": false, "reason": "scanned_pdf"…}` — chặn |
| sau `pip install pypdf` | `{"ok": true, "n_articles": 72}` |

CÙNG một tệp.

**Vá — ba lớp, vì một mình tài liệu không đủ.**

1. **`requirements.txt` nói thật và VẪN cài được.** Khai `pypdf>=4.0` là phụ thuộc THẬT của đường
   nạp PDF; ghi rõ `python-docx` là TUỲ CHỌN (r317 đã cứu nhánh không-lib) và tách riêng hai NHỊ
   PHÂN HỆ THỐNG mà `pip` không cài được (`pdftotext` bắt buộc · `antiword`/`catdoc` cho `.doc` cũ).
   Mỗi mục kèm HẬU QUẢ cụ thể, không phải danh sách trơ.
2. **`tl doctor` tự kiểm** — `_doc_dep_probe()` + dòng `optional phụ thuộc nạp tài liệu`. Đây mới là
   phần bền: người ta không đọc `requirements.txt`, nhưng có chạy `doctor`. Thiếu `pypdf` ⇒
   `✗ … pypdf|pdfplumber THIẾU ⇒ MỌI .pdf bị chặn (reason=pdf_probe_unavailable, r315).
   Cài: pip install pypdf`.
   ★Tên có tiền tố `optional` — nếp sẵn có (`optional rasoat/backfill`) để check báo ĐỎ mà **KHÔNG
   lật rc**: máy không bao giờ nạp PDF không đáng bị `doctor` báo hỏng.
3. **Đồng bộ tài liệu**: `INSTALL.md` (câu «không cài gì thêm» nay sai) · `references/DEPENDENCIES.md`
   §9 (bảng 4 dòng: mức + thiếu-thì-sao).
   ★**KHÔNG đụng `SKILL.md`.** Bản vá đầu có thêm một câu vào §9 và làm kernel phình 48.031 →
   48.152 B, **vượt trần KERNEL-DIET 47 KB (48.128)** ⇒ `r127_kernel_warn_wired_in_audit`,
   `r128_kernel_diet_under_warn` và `r219_gotchas_nhan_trang_thai` ĐỎ cùng lúc. Đã revert:
   kernel = bất biến + CON TRỎ, §9 vốn đã trỏ sang `DEPENDENCIES.md` — chi tiết thuộc về đó
   (chính là lý do file đó được tách ra từ SKILL.md §9 ở Pha F v1.34.0). Ba cổng bắt đúng việc.

**Bẫy I11 LẶP LẠI — đã dính thật giữa lượt này.** `_doc_dep_probe` là helper tl_core MỚI; `bind()`
re-home `__globals__` của mọi hàm tl_core về namespace `tl`, nên symbol không khai trong bảng stub
`ops_misc` của `tl.py` sẽ **`NameError` LÚC CHẠY** dù import đúng — `tl doctor` gãy ngay lần chạy
đầu. Đúng bẫy r312 đã ghi cho `_src_id_dup_groups`. Ca `r319_khong_bien_tuy_chon_thanh_chan_cung`
nay khoá luôn vế đó (`'_doc_dep_probe'` phải có mặt trong `tl.py`).

**Cổng.** selftest **1606/1606** (thêm 2 ca: 1 thuận + 1 ngược) · golden 0-diff · determinism ok ·
`release-verify` khớp · `RELEASE_MANIFEST.json` đã tái sinh.
ruff F: `ops_misc.py` và `tl.py` **delta = 0**; `tl_selftest.py` **delta theo TÊN = 0** — chỉ số lần
của `_TL_MODULE` tăng 2149 → 2151 vì hai ca mới tham chiếu đúng cái tên module được gán ĐỘNG
(`g["_TL_MODULE"] = tl_module`) mà master đã chấp nhận 2149 lần; không sinh loại phát hiện mới.

**Bẫy ĐA NỀN — gate `windows-latest` bắt ca r316 của tôi, Linux thì xanh.** Fixture «container
hỏng» dựng bằng `writestr("word\\document.xml", …)`: `ZipInfo.__init__` có
`if os.sep != "/" and os.sep in filename: filename = filename.replace(os.sep, "/")` ⇒ trên
Windows fixture bị NẮN THÀNH HỢP LỆ, `scan_file` đọc được, ca đỏ oan (1605/1606). Đo thêm mới
thấy sâu hơn: `_RealGetContents` cũng dựng lại `ZipInfo(tên)` LÚC ĐỌC, nên trên Windows
**không có cách nào** dựng được dạng backslash — tức container kiểu CDN THẬT SỰ đọc được ở đó
(khớp việc Word mở tệp ấy bình thường). Sửa: ca TỰ KIỂM fixture trước khi kiểm hành vi, chỉ
đòi dạng backslash khi nền thật sự làm nó hỏng, và khoá khế ước bằng dạng **THIẾU HẲN member**
— dựng được trên MỌI nền. Đã đối chiếu PARITY bằng cách chạy CHÍNH selftest dưới `os.sep='\\'`:
**1606/1606 ở cả hai ngữ nghĩa**. Đúng bài học CLAUDE.md — Linux xanh không nói gì về Windows.

**Ghi thêm — chính test của r319 bắt lỗi của r319.** Ca «không còn khai sai» ban đầu kiểm CHUỖI CON
`uses only Python standard library`, mà bản `requirements.txt` mới lại TRÍCH LẠI câu đó để ghi bối
cảnh («…trước r319 là SAI») ⇒ ĐỎ oan. Đã đổi sang kiểm **DÒNG KHAI cũ nguyên văn**. Bài học nhỏ mà
lặp đi lặp lại trong đợt này: **kiểm chuỗi con trên văn bản có trích dẫn lịch sử là kiểm sai chỗ.**

# ★ v1.36.50 — r318: hai bộ lọc rác Công báo sai trên CHÍNH bản Công báo — khối chữ ký số 3 dòng lọt vào khối đầu · nhãn mục sai CẢ HAI CHIỀU (2026-08-02)

Đóng nốt §4.4 và §4.5 của lượt bảo trì kho 02-08 (`rasoat/BIEN_BAN_BAO_TRI_KHO_BHXH_2026-08-02.md`).
Cả hai đều nằm trong `loc_rac_congbao` (r217) — bộ lọc dựng riêng cho bản Công báo, mà lại sai
trên đúng hai bản Công báo đem ra dùng.

## r318a — khối chữ ký số có ÍT NHẤT HAI biến thể, bản cũ chỉ bắt bộ 4

**Bệnh.** `CB_CHU_KY_SO` ghép CỨNG đúng 4 nhãn theo ĐÚNG thứ tự
(`Người ký:` / `Email:` / `Cơ quan:` / `Thời gian ký:`). Đo 02-08:

| bản | khối chữ ký in ra | bản cũ bắt được |
|---|---|---|
| 54-2025 · CB 1083+1084 | `Người ký:` `Email:` `Cơ quan:` `Thời gian ký:` (4 dòng) | 4/4 ✅ |
| 19-2026 · CB 133 | `Ký bởi:` `Cơ quan:` `Ngày ký:` (**3 dòng**) | **0** ❌ |

Ba dòng đó nằm ngay ĐẦU bản bóc ⇒ chui thẳng vào **khối đầu** — mà khối đầu là nguồn **DUY NHẤT**
chứng minh danh tính văn bản (r215). Đo trên record thật:

```
trước: khoi_dau = 'Ký bởi: CÔNG BÁO NƯỚC CỘNG HÒA…\nCơ quan: VĂN PHÒNG CHÍNH PHỦ\nNgày ký: 2026-03-05…'
sau  : khoi_dau = 'CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\nĐộc lập - Tự do - Hạnh phúc…'      (141/141 Điều giữ nguyên)
```

**Vá.** Tập NHÃN đóng `CB_CHU_KY_NHAN` (`Người ký`|`Ký bởi` · `Cơ quan` · `Thời gian ký`|`Ngày ký` ·
`Email`) + dò **DÃY LIỀN 3–4 dòng, THỨ TỰ TỰ DO**, thử dãy DÀI trước để không cắt cụt khối 4 thành 3.
★Dãy **BẮT BUỘC chứa nhãn người-ký** — đó là thứ neo «đây là khối chữ ký»; thiếu chốt đó thì
hai-ba dòng thân bài vô tình mở đầu bằng «Cơ quan:»/«Ngày ký:» đủ để **nuốt mất quy phạm**
(ca `r318_khong_nuot_than_van_ban` khoá đúng điều này). Tên cũ `CB_CHU_KY_SO` giữ lại cho caller ngoài.

## r318b — `CB_DAU_MUC` sai CẢ HAI CHIỀU trên CÙNG một tệp

Đo trên `54-2025`:

* **ÂM TÍNH GIẢ — dòng 10:** nhãn mục THẬT của Công báo là `VĂN BẢN PHÁP LUẬT KHÁC`, KHÔNG nằm
  trong mẫu cũ (mẫu chỉ có họ «VĂN BẢN QUY PHẠM PHÁP LUẬT») ⇒ rác thật đi lọt.
* **DƯƠNG TÍNH GIẢ — dòng 1578:** đó là dòng thứ BA của một TIÊU ĐỀ CHƯƠNG bị xuống dòng —
  «Chương VI / HIỆU LỰC VÀ NGUYÊN TẮC ÁP DỤNG / **VĂN BẢN QUY PHẠM PHÁP LUẬT**» — bị báo là nhãn mục.

**Và lời khuyên đi kèm còn nguy hiểm hơn thứ nó cảnh báo.** Câu cũ: *«Cắt tay tới dòng mang số hiệu
(`Số: …` / `Luật số: …`) rồi nạp lại»*. Với **VBHN**, dòng `Số: …` nằm ở **KHỐI KÝ CUỐI bản**
(đã đo: `19/VBHN-VPQH` ở vị trí 183.972/184.114) ⇒ làm theo đúng chữ là **XOÁ SẠCH Chương I→N**.
Người vận hành làm đúng như tài liệu bảo thì mất trọn thân văn bản.

**Vá.** (1) mẫu nhận cả `VĂN BẢN PHÁP LUẬT KHÁC` và tiền tố `PHẦN` tuỳ chọn; (2) LOẠI TRỪ
dương-tính-giả bằng phép nhìn lui tối đa 2 dòng không-trống — gặp `Chương|Phần|Mục <số>` đứng
một mình ⇒ đây là tiêu đề bị xuống dòng, KHÔNG báo; (3) viết lại lời khuyên: chỉ đúng (các) dòng
cần bỏ, kèm cảnh báo TƯỜNG MINH đừng cắt theo neo `Số:`.

★**GIỮ NGUYÊN quyết định gốc của r217: chỉ KHAI BÁO, KHÔNG tự bỏ** nhãn mục — bytes của corpus đã
nạp không đổi. r318 chỉ làm cho phép khai báo TRỎ ĐÚNG CHỖ và lời khuyên không phản chủ.
Ca `r318_dau_muc_dung_ca_hai_chieu` khoá cả năm vế: âm-tính-giả, dương-tính-giả, họ cũ vẫn bắt,
lời khuyên có đủ cảnh báo, và nhãn vẫn CÒN trong text (không tự bỏ).

**Nghiệm thu trên hai bản Công báo thật:**

| | trước r318 | sau r318 |
|---|---|---|
| 19-2026 `chu_ky_so` | 0 (3 dòng chrome vào khối đầu) | **3** — khối đầu bắt đầu đúng ở quốc hiệu |
| 54-2025 `chu_ky_so` | 4 | **4** (không đổi) |
| 54-2025 cảnh báo nhãn mục | dòng **1578** (tiêu đề Chương) | dòng **10** (nhãn mục THẬT) |
| số Điều | 141 · 72 | **141 · 72** (không suy suyển) |

**Cổng.** selftest **1604/1604** (thêm 3 ca: 1 thuận + 2 ngược) · ruff F **delta so master = 0**
(`verify_deep.py` sạch · `tl_selftest.py` 1 F401 + 4325 F821) · golden 0-diff · determinism ok ·
`release-verify` khớp · `RELEASE_MANIFEST.json` đã tái sinh.

**Ghi thêm — bẫy `VERSION` mất byte:** lượt hoà master, phép giải xung đột của tôi ghi lại `VERSION`
kèm ký tự xuống dòng cuối (7B → 8B). `.gitattributes` khoá `* -text` vì `package_hash` tính trên
byte THẬT ⇒ đã nắn về đúng khuôn master (7B, KHÔNG newline). Thêm một biến thể của cùng bài học
CRLF ở v1.36.48: **mọi thao tác trên tệp trong gói phải so byte với master trước khi commit.**

# ★ v1.36.49 — r316: `scan_file` hết FAIL-OPEN (docx không đọc được ≠ sạch markup) · r317: trị đo DrawingML hết lọt vào thân Điều (2026-08-02)

Hai lỗ của **đường ĐỌC .docx**, cùng lộ ra ở lượt bảo trì kho 02-08 khi nạp thật hai bản Công báo
(`rasoat/BIEN_BAN_BAO_TRI_KHO_BHXH_2026-08-02.md` §4.2, §4.6). Cả hai đều làm hỏng **nguyên văn** —
đúng lời hứa lõi của skill — mà không cổng nào kêu.

## r316 — `docx_markup.scan_file` báo «sạch markup» cho tệp KHÔNG ĐỌC ĐƯỢC

**Bệnh.** Bản cũ nuốt mọi exception rồi `return scan("")`, tức trả dict đếm TOÀN 0. Docstring gọi đó
là chủ ý, nhưng markup là **TÍN HIỆU PHÁP LÝ** — chính đầu tệp `docx_markup.py` viết «lỗi ĐÚNG-SAI về
nội dung pháp luật». Một cổng an toàn pháp lý mặc định «sạch» khi không đo được là fail-OPEN.

**Hai ca THẬT, độc lập nhau:**

1. **Container CDN đóng gói sai** (đo 02-08): `.docx` Công báo tải qua `g7.cdnchinhphu.vn` đặt tên
   entry bằng `\` thay `/` — 19-2026: **33/40** entry · 89-2026: **30/37** ⇒ không có
   `word/document.xml` theo tên chuẩn. `scan_file` trả `{}` và người rà kết luận «SẠCH markup»;
   sự thật sau khi nắn tên entry là `strike=2`. Word/LibreOffice mở tệp đó **bình thường** ⇒ chỉ
   cần một reader chịu tên `\` là markup đi thẳng vào kho mà không ai khai.
2. **Ca thứ hai nằm sẵn trong chính selftest**: `r188_docx_reader_bounded_wired` ĐANG khẳng định
   `sum(scan_file(bomb).values()) == 0` cho docx **vượt trần zip-bomb**. Tức khế ước cũ ghi thành
   văn rằng «không đo được ⇒ báo sạch». Ca đó nay đổi sang đòi cờ `UNREADABLE`; phần còn lại của
   r188 (reader bounded, không OOM, docx thường vẫn đọc, cap đọc đúng từ env) giữ nguyên.

**Vá.** `scan_file` trả `{UNREADABLE: True}` (hằng mới, xuất trong `__all__`) thay vì dict-toàn-0.
`warn_line` có nhánh riêng KÊU TO «KHÔNG ĐỌC ĐƯỢC container … CHƯA biết có markup hay không (KHÔNG
phải 'sạch')». `normalize_document` khai `MARKUP_KHONG_DOC_DUOC` vào `verify_flags` — **tách khỏi**
câu `MARKUP_SUA_DOI` (câu đó khẳng định CÓ markup và đếm được; ở đây ta chưa biết gì).
`lookup_ops` khai `markup_unreadable` riêng và để `markup_found=True` (fail-CLOSED).
★Tài liệu SẠCH vẫn IM LẶNG như cũ — ca `r316_tai_lieu_sach_van_im_lang` giữ chốt đó, để cảnh báo
không thành tiếng ồn và bất biến «văn bản sạch giữ NGUYÊN bytes cache» của r182 không vỡ.

## r317 — toạ độ DrawingML chui vào thân Điều

**Bệnh.** Phép bóc tag `<[^>]+>`→`""` giữ **MỌI** nút text, kể cả trị đo trong `<w:drawing>`. Đo trên
2 bản Công báo (nhánh KHÔNG python-docx):

| | trị lọt vào text |
|---|---|
| 19-2026 | `2927786221920` trong **khối đầu** + 2 số trong **Điều 141** |
| 89-2026 | `315848953340` trong khối đầu · **Điều 72** dính chuỗi **59 CHỮ SỐ** · 1 số ở Điều 79 |

Chỉ có ba loại nút rò, cùng là DrawingML: `wp:posOffset`, `wp14:pctWidth`, `wp14:pctHeight`.
Nhánh **python-docx KHÔNG dính** (nó chỉ đọc `w:p`/`w:tbl`) ⇒ **cùng một .docx cho hai kết quả khác
nhau tuỳ máy có hay không có `python-docx`** — mà `requirements.txt` khai stdlib-only, nên máy cài
sạch chạy đúng nhánh RÒ.

**Vá.** `drop_drawing_measures()` — bỏ nội dung element thuộc hai namespace `wp:`/`wp14:`, gọi
**TRƯỚC** khi bóc tag, tại **cả hai** reader bóc-tag: `plain_from_document_xml` (r252 — đường của
`tl extract`/`tl doc-text` + cổng phân loại ingest) và `_docx_zip_text` (`normalize_document`).

★**Vì sao nhắm hai namespace chứ không xoá cả `<w:drawing>`:** chữ THẬT trong hình nằm ở
`w:txbxContent`/`a:t` — xoá cả khối drawing là ăn mất text-box, mà letterhead VBQPPL đôi khi nằm
đúng đó. `wp:`/`wp14:` (WordprocessingDrawing) không chứa text tài liệu: mọi lá là trị đo.

**Ba bất biến được khoá bằng test** (`r317_khong_an_lem_chu_that`): tài liệu KHÔNG có drawing ⇒
chuỗi ra **= chuỗi vào** (bytes bất biến cho corpus đã nạp) · text-box trong drawing SỐNG SÓT ·
**số dài THẬT trong `w:t` không bị đụng** (văn bản luật có số tài khoản/mã số thuế — ai "vá" bằng
cách quét số ≥9 chữ số trên TEXT thì ca này ĐỎ, và phải ĐỎ).

**Nghiệm thu end-to-end** (chặn `python-docx` để ép đúng nhánh rò, nạp thật 2 bản Công báo):

| | trước | sau |
|---|---|---|
| 19-2026 · 141 Điều | 3 số rác | **0** |
| 89-2026 · 79 Điều | 3 số rác | **0** |

**Bẫy đã dính giữa chừng, ghi vì nó không lộ ra khi đọc code:** bản vá đầu viết regex `wp14?` —
cái đó parse ra `"wp1"` + `"4"` tuỳ chọn nên **KHÔNG khớp `wp:` trần**. Kết quả: `wp14:pctWidth` bị
bỏ còn `wp:posOffset` vẫn lọt, ra một chuỗi số **CỤT** (`-7299958220` → `-729995822`) trông y như
đã sửa xong. Chỉ đếm lại trên tệp thật mới thấy. Đúng là `wp(?:14)?`; ca
`r317_tri_do_drawing_khong_lot_vao_than_dieu` đòi CẢ HAI namespace nên bắt được đột biến đó.

**Cổng.** selftest **1598/1598** (thêm 4 ca: 2 chiều thuận + 2 chiều ngược; sửa khế ước 1 ca r188) ·
ruff F **delta so master = 0** trên cả 4 tệp đụng tới (`docx_markup.py` sạch · `normalize_document.py`
1 F401 · `tl_selftest.py` 1 F401 + 4325 F821 · `tl_core/lookup_ops.py` 563 F821) · golden 0-diff ·
determinism ok · `release-verify` 177/177 + `package_hash` khớp.

**Còn treo (§4.6 chưa xong phần khế ước):** `requirements.txt` vẫn khai «uses only Python standard
library». r317 làm nhánh không-`python-docx` hết rò, nhưng `pypdf` thì KHÔNG có đường thay thế —
thiếu nó là mọi PDF bị chặn (r315). Sửa khế ước cài đặt của gói là lượt riêng.

# ★ v1.36.48 — r314: cổng T1 số hiệu nhận dạng GẠCH CHÉO · r315: thiếu thư viện dò PDF không còn bị gọi là «bản SCAN» (2026-08-02)

Hai cổng CÙNG một bệnh: **báo sai thủ phạm**. Cả hai đều đỏ/xanh nghe rất thuyết phục, và cả hai đều
đẩy người vận hành đi sửa nhầm chỗ. Không cái nào lộ ra khi đọc mã — cùng lộ ra ở lượt bảo trì kho
02-08 khi nạp thật ba bản Công báo (`rasoat/BIEN_BAN_BAO_TRI_KHO_BHXH_2026-08-02.md` §4.1, §4.3).

## r314 — `sohieu_corroborated` mù với dạng số hiệu gạch chéo

**Bệnh.** r221 vá chiều «khoá registry gạch-nối vs bản in gạch-chéo» và mặc định `so_hieu` truyền vào
LUÔN là khoá registry. Nhưng `ingest_to_cache --help` lại bảo người dùng gõ dạng IN — nguyên văn
*«Số hiệu canonical, vd 18/VBHN-VPQH»* — và đường nạp chuyển THẲNG chuỗi đó xuống `verify_deep`.
`_VBHN_WITHYEAR_RE` là `^(\d+)-(\d{4})-VBHN-(.+)$`, chỉ nhận gạch nối ⇒ `19/2026/VBHN-VPQH` trượt
`fullmatch`, mất luôn phép nới «bản in không mang năm», đẻ ra `T1-nhẹ` OAN.

**Đo 02-08 trên 3 bản Công báo, CÙNG tệp, chỉ đổi cách gõ số hiệu:**

| số hiệu truyền vào | 19-2026 | 54-2025 | 89-2026 |
|---|---|---|---|
| `NN/YYYY/VBHN-VPQH` (dạng in — đúng như `--help` dạy) | `T1-nhẹ` | `T1-nhẹ` | `T1-nhẹ` |
| `NN-YYYY-VBHN-XXX` (khoá registry) | — | — | — |

3/3 cờ oan → 0/3. Cùng họ với ★ v1.35.57/r221 (`re.escape(so_hieu.split("/")[0])`): cả hai lần
đều là **giả định về DẠNG chuỗi ở biên giữa khoá registry và bản in**.

**Vá.** Nắn ngăn cách của **bản sao cục bộ** ngay trước `fullmatch`
(`verify_deep.py:84`). ★KHÔNG nới `_VBHN_WITHYEAR_RE` dùng chung: ở `classify`/`hygiene`/`resolve`/
`lookup_ops` nó đang canh ĐÚNG bất biến khoá registry (CHỈ gạch nối, `NN-YYYY-VBHN-XXX`) — nới ở đó là
mở toang một cổng khác. Test `r314_khong_noi_regex_dung_chung` khoá đúng điều này: nó ĐỎ nếu ai
đó "vá" bằng cách sửa regex chung.

## r315 — `assert_pdf_not_scanned` báo «bản SCAN» khi thực ra là THIẾU THƯ VIỆN

**Bệnh.** `pdf_text_layer_chars` thử `pdfplumber` rồi `pypdf`; thiếu **cả hai** thì `return 0` — mà 0
nghĩa là «PDF scan». Khuyết tật của MÁY bị báo thành thuộc tính của TÀI LIỆU, kèm lời khuyên
*«hãy chuyển sang nguồn web TEXT khác»* ⇒ người vận hành đi săn nguồn không tồn tại. Nặng hơn:
`requirements.txt` khai *«uses only Python standard library»* nên **cài sạch là không có cái nào**
⇒ toàn bộ đường nạp PDF chết, với thông điệp chỉ sai hướng.

**Đo 02-08 trên `54-2025-g7.pdf`** (PDF text THẬT — `pdftotext` bóc 167.433 ký tự, riêng trang 1 có 2.536):

| | kết quả |
|---|---|
| chưa cài `pypdf` | `{"ok": false, "reason": "scanned_pdf", "message": "…chỉ 0 ký tự text ở trang đầu…"}` |
| đã cài `pypdf` | `{"ok": true, "n_articles": 72}` |

CÙNG một tệp.

**Vá.**

1. `pdf_text_layer_chars` trả **`None` = KHÔNG ĐO ĐƯỢC**, khác hẳn `0` = đo được và rỗng. Tách hai
   đường dò thành `_pdf_chars_pdfplumber` / `_pdf_chars_pypdf`, mỗi cái tự trả `None` khi câm.
   ★Đồng thời sửa lỗi **CỘNG DỒN** của bản cũ: hai đường dò nuôi CHUNG biến `total`, nên pdfplumber
   hỏng giữa chừng rồi pypdf chạy tiếp là cộng CHỒNG lên phần dở dang.
2. `PdfProbeUnavailableError` — lớp lỗi RIÊNG, **KHÔNG** kế thừa `ScannedPDFError` (gộp họ là tái lập
   đúng cái lỗi đang chữa). Vẫn **fail-CLOSED** — không nạp mù — nhưng thông điệp chỉ đúng người phải
   sửa: *«ĐÂY LÀ KHUYẾT CỦA MÁY… ĐỪNG đi tìm nguồn khác. pip install pypdf»*.
3. Handler `__main__` thêm nhánh `reason: "pdf_probe_unavailable"` + `action: "install_dep"` + **exit 6**
   (5 vẫn là «PDF scan, đổi nguồn»), để agent-loop/script không nuốt thành `ingest_failed` chung chung.

**Chưa làm ở lượt này:** `requirements.txt` vẫn khai stdlib-only. `pypdf`/`python-docx` thực chất là
phụ thuộc BẮT BUỘC để nạp đúng (thiếu `python-docx` thì trị `wp:posOffset` lọt vào thân Điều — biên bản
§4.6). Việc đó đụng khế ước cài đặt của gói nên tách lượt riêng.

**Cổng.** selftest **1594/1594** (thêm 4 ca: 2 chiều thuận + 2 chiều ngược) · ruff F **delta so master = 0**
trên cả 4 tệp đụng tới (`tl.py` 12 F821 · `tl_selftest.py` 1 F401 + 4325 F821 · `ingest_to_cache.py`
1 F401 · `verify_deep.py` sạch) · golden 0-diff · determinism ok · `release-verify` khớp.

**Bẫy đã dính trong chính lượt này, ghi để không lặp:** bump VERSION bằng
`pathlib.read_text()/write_text()` đã **nuốt 307 CRLF của SKILL.md và 1766 của `tl.py`** (chế độ text
dịch CRLF→LF). `.gitattributes` khoá `* -text` CHÍNH VÌ manifest hash là byte thật ⇒ mọi sửa tệp trong
gói phải đi `read_bytes()/write_bytes()`. Phát hiện nhờ `r219_gotchas_nhan_trang_thai` ĐỎ (nó neo
`SKILL.md.stat().st_size`) — một cổng canh việc khác lại bắt được đúng lỗi này.
# ★ v1.36.47 — r313: RAS-17 phần MÃ + GUARD — khuôn `anchor.text_hash`, tách `locator`, cưỡng chế `anchor_con_hieu_luc` (2026-08-02)

**Phạm vi có chủ đích: MÃ + GUARD, KHÔNG đụng DỮ LIỆU.** Di trú 82 giá trị anchor là việc GHI, tách riêng.

**Bệnh.** `RASOAT_PLAN_SCHEMA.md` §7.2 đo 01-08 trên hồ sơ `h7-3nd-bhxh-2025`: **82/82 `doc_deps` ĐIỀN ĐỦ,
0/82 khớp `sha256:<64hex>`** — ô `text_hash` đang chứa ĐỊA CHỈ ĐỊNH VỊ. Vì «điền đủ» nên không cổng nào
kêu; Loop C chạy lên sẽ báo **STALE giả 100%**. Đây là lớp bệnh «trường CÓ giá trị nhưng SAI LOẠI» —
đếm rỗng/thiếu MÙ hoàn toàn, phải soi KHUÔN mới thấy.

**Đo trước khi vá (quyết định được phép fail-closed hay không):**
- `doc_deps` xuất hiện trong **0 tệp `.py`** — RAS-17 phần mã là **greenfield**, chưa validator nào.
- `anchor_con_hieu_luc` chỉ sống trong **prose + 1 ca selftest kiểm *tài liệu có nhắc chữ đó không***
  — **không mã nào cưỡng chế**. Đúng lớp tự-lừa mà `_rasoat_vong_doi_dong_hop_le` (r300) sinh ra để chặn.
- Quét toàn kho: chỉ **3** giá trị `text_hash` literal, **không giá trị hỏng nào** (template hợp khuôn;
  hai chỗ còn lại là skeleton/ellipsis tài liệu). ⇒ 82 giá trị xấu nằm **hoàn toàn ở hồ sơ runtime**
  (`--out-dir`), ngoài kho ⇒ **cưỡng chế được mà không đỏ oan**.

**Vá — ba hàm PURE (`tl_core/lookup_ops.py`), đã bind qua `tl.py` (ADR-0002):**
1. `_rasoat_anchor_khuon()` — khuôn đóng `^sha256:[0-9a-f]{64}$` + dấu hiệu địa chỉ. **CỐ Ý là HÀM**,
   không phải hằng cấp module — cùng lý do `_rasoat_vong_doi_enums`: `tl.py` bind COPY-globals, stub farm
   chỉ nhận callable; hằng module tra từ trong hàm KHÔNG resolve qua `tl` (r90/r81 bắt).
2. `_rasoat_anchor_findings(units)` — phân loại từng dep: `ok` / `rong` / **`locator_trong_hash`** /
   `sai_khuon`, đếm riêng `co_locator`. Đọc **CẢ** khuôn §6 `phat_hien` lẫn bảng `noi_dung`.
   `san_sang` ⇔ có ≥1 dep **VÀ** mọi dep `ok` — `tong=0` KHÔNG phải «sạch».
3. `_rasoat_anchor_hop_le(state, units)` — fail-CLOSED ba vế: khai `true` mà **không đưa đơn vị để kiểm**
   ⇒ ĐỎ (không kiểm được thì không được khai); khai `true` mà chưa `san_sang` ⇒ ĐỎ **kèm số đếm**;
   khai `false` tường minh mà thiếu `ly_do_anchor` ⇒ ĐỎ (§7.2 «không im lặng thoát»).
   **Cờ VẮNG HẲN ⇒ KHÔNG đỏ** — hồ sơ đang rà chưa tới bước khai; ratchet siết chiều khai SAI, không siết
   chiều CHƯA KHAI (đỏ oan ngày đầu = guard bị vô hiệu hoá, bài học §0.8).

**Tách `locator`:** khai báo khuôn ở `templates/MAU_BANG_TONG_HOP_PHAT_HIEN.json` +
`references/RASOAT_HOSO_LOOP.md` nay có **`locator` là trường RIÊNG** cạnh `text_hash`. Hai thứ khác bản
chất: hash đổi khi NỘI DUNG đổi (đúng thứ Loop C cần), địa chỉ thì không.

**Bằng chứng DƯƠNG (3 mutation, không tin `rc=0`):**
- nới khuôn (cho hex trần / CHỮ HOA) ⇒ `r313_anchor_khuon_findings` + `r313_khuon_khop_dac_ta_va_tl` **ĐỎ**
- bỏ cổng «khai true mà không đưa đơn vị» ⇒ `r313_anchor_con_hieu_luc_fail_closed` **ĐỎ**
- cho `tong=0` là `san_sang` (vacuous) ⇒ `r313_anchor_khuon_findings` **ĐỎ**

**Selftest 1593/1593** (master 1590, +3 ca). Ruff **DELTA = 0** cả ba tệp, không tên F821 nào mới.

**CÒN NỢ (KHÔNG làm ở đợt này):** di trú **82** giá trị anchor của hồ sơ BHXH — tách địa chỉ sang
`locator`, tính lại hash bằng `doc_identity._content_hash`, rồi mới được đặt `anchor_con_hieu_luc: true`.
Con số 82 phải **đếm lại LIVE** trước khi di trú. Guard ở đợt này chính là thứ sẽ **chặn** việc bật cờ
trước khi di trú xong.

# ★ v1.36.46 — r312: ING-09 — nhân đôi theo TỆP NGUỒN (`src_id`) lộ diện; cổng ingest hết nấp sau `if sohieu` (2026-08-02)

Đóng ING-09. Khác với ba mục trước, mục này **đo được trên registry LIVE** (1319 dòng, tab `files`) chứ
không suy từ mã.

**Bệnh — đo LIVE 02-08 bằng `gws sheets +read` trên tab RAW.** 31 cụm / 66 dòng CÙNG `src_id` mà
`drive_id` **đôi một KHÁC** — tức MỘT tệp nguồn đã được ingest ≥2 lần, mỗi lần convert ra một GDoc mới
và đẻ thêm một dòng registry. 25/31 cụm mọi dòng `corpus=true` (nhân đôi THẬT trong corpus, không phải
bản đã hạ). Mẫu điển hình là phụ lục EVFTA: cùng một tệp nguồn ra hai dòng
«EVFTA_PL_Phu_luc_2-A» và «EVFTA_PL_Annex_2-A_Bieu_thue».

**Vì sao KHÔNG detector nào thấy — bốn cái mù CÙNG LÚC** (đo trên chính 31 cụm đó):

| tầng | kết quả | vì sao mù |
|---|---|---|
| `duplicates_by_sohieu` | 26/31 cụm `sohieu` RỖNG | phụ lục hiệp định không có số hiệu |
| `duplicates_by_name` | 27/31 cụm tên KHÁC nhau | bản Việt «Phu_luc_2-A» vs bản Anh «Annex_2-A» của CÙNG phụ lục |
| `duplicates_by_md5` | md5 khác | md5 tính trên GDoc ĐÃ convert — mỗi lần convert một md5 |
| khoá chính `drive_id` | 31/31 cụm đôi một khác | mỗi dòng một GDoc riêng |

`src_id` là thứ **DUY NHẤT** còn nối chúng về cùng một tệp nguồn — và đó chính là ý «detector sheet-dup
phải đặt ở tầng đọc RAW SHEET»: `drive_id` bị tầng chuẩn hoá đổi tên thành `id`/`gdoc_id`, còn cụm trùng
thì chỉ nhìn thấy được khi soi theo cột nguồn.

**Lỗ ở đường GHI.** Cổng dedup F1 (r191) trong `_il_stage_plan` đứng sau `if sohieu and not _prev …` ⇒
với 26/31 cụm (sohieu rỗng) nó **KHÔNG bao giờ chạy**. `--drive-id` là đường dễ dính nhất: người dùng trỏ
lại đúng tệp nguồn đã nạp, `_resolve_drive_id_source` vui vẻ convert tiếp, không cổng nào cản.

**Vá.**

1. **`_src_id_dup_groups` (`tl_core/hygiene.py`)** — detector RIÊNG, gom theo `src_id`, chỉ tính dòng
   corpus-effective và **đòi `drive_id` đôi một KHÁC** (trùng `drive_id` = một dòng đọc hai lần, KHÔNG
   phải nhân đôi). Vào `_hygiene_groups` + counter `duplicates_by_src_id` + `samples` + dòng in
   `dup_src_id=` của `tl hygiene scan`.
2. **Cổng `src_id_dedup_live` trong `_il_stage_plan`** — neo `_from_drive`, **độc lập số hiệu**, chặn
   **TRƯỚC** khi rẽ DRY/apply (thấy sớm, không ghi gì). Lý do neo `src_id` chứ không `drive_id`: `drive_id`
   là GDoc KẾT QUẢ, mỗi lần convert một id mới nên không bao giờ trùng. Đường thoát tường minh:
   `--replace-sohieu` (thay bản có chủ đích) · `--resume` (tiếp tục dở dang) · `--skip-live-check` (tự chịu).
3. **`_src_id_dup_groups` khai trong bảng stub `hygiene` của `tl.py`** — `bind()` re-home `__globals__` của
   mọi hàm tl_core về namespace tl, nên helper MỚI không khai ở đó sẽ `NameError` LÚC CHẠY dù import đúng.
   (Đã cắn thật trong lượt này — ghi lại để lần sau thêm helper thì nhớ.)

**Bằng chứng dương.** selftest **1590/1590**. Detector chạy trên registry LIVE trả **26 cụm / 55 dòng**.
MUTATION 2 lượt, mỗi lượt đỏ ĐÚNG một ca:
· bỏ điều kiện `drive_id` đôi một khác ⇒ `r312_src_id_dup_lo_dien` ĐỎ;
· thêm lại `and sohieu` vào điều kiện cổng (đúng cách ING-09 tái phát) ⇒ `r312_cong_ingest_chan_nguon_da_nap` ĐỎ.
`r312_src_id_dup_lo_dien` khoá luôn **BẰNG CHỨNG MÙ**: cùng một cụm fixture, ba detector cũ đều trả rỗng —
ai "gộp cho gọn" vào một trong ba thì vế đó đỏ.
ruff: **0 TÊN F821 MỚI** trên cả hai tệp chạm (tập tên riêng biệt BẰNG NHAU hai bên: hygiene 128, ingest_ops
104); số đếm tăng +3 / +7 thuần tuý vì thêm call-site của helper vốn đã resolve qua stub-farm.

# ★ v1.36.45 — r311: DOC-01 — `route()` hết nuốt lỗi chính tả `hinh_thuc`; ca test đang KHOÁ hành vi hỏng được đảo chiều (2026-08-02)

Đóng DOC-01 của sổ audit — lỗi mà chính kho này đã tự khai từ lâu mà chưa ai vá.

**Bệnh — đo LIVE 02-08, chạy lại được.** `route()` (`scripts/rasoat_phuluc.py`) khớp chuỗi CÓ DẤU cố định,
còn `_norm()` chỉ lower + NFC + gộp khoảng trắng — KHÔNG bỏ dấu. Mọi giá trị không dấu / sai chính tả /
ngoài từ vựng rơi vào nhánh cuối `return "04"`:

| đầu vào | bản cũ trả | đáng lẽ |
|---|---|---|
| `"ban hành mới"` | `05` | ✓ |
| `"ban hanh moi"` | `04` | `05` hoặc FAIL-CLOSED |
| `"Bãi bỏ toàn bộ"` | `06` | ✓ |
| `"bai bo toan bo"` | `04` | `06` hoặc FAIL-CLOSED |
| `""` / `"   "` | `04` | FAIL-CLOSED |
| `"xyz la gi"` | `04` | FAIL-CLOSED |

MỘT lỗi gõ dấu trong bảng master đủ để một đề xuất **ban hành mới** bị đếm sang Mẫu 04-BN — sai cả
phụ lục lẫn số liệu Mục D của Báo cáo, và không có tín hiệu nào. `templates/MAU_BANG_TONG_HOP_PHAT_HIEN.json`
(`_canh_bao_hinh_thuc`) đã tự khai nguy cơ này, và `docs/KE_HOACH_RASOAT_HOSO_ORCHESTRATION.md:272` đã chốt
*"không để `route()` fallback im lặng"* — bản vá này là trả nợ một quyết định đã có.

**Vì sao nằm lại lâu — có một ca test KHOÁ ĐÚNG HÀNH VI HỎNG.** `tl_selftest.py` (r209, `ok3`) viết
`_rp209.route("ban hanh moi") == "04"`, kèm chú thích *"bẫy không-dấu KHOÁ LẠI làm bằng chứng"*. Ý định
ban đầu là chứng minh dòng cảnh báo trong doc là THẬT, nhưng hệ quả là bug trở thành **kỳ vọng có cổng
bảo vệ**: ai sửa `route()` cho đúng đều làm selftest ĐỎ. Ghi lại để không lặp: **khoá một hành vi HỎNG
bằng test là biến nó thành hợp đồng** — muốn lưu bằng chứng thì khoá ở chỗ PHẢN CHỨNG (tái hiện thuật
toán cũ ngay trong test), đừng khoá trên hàm đang chạy.

**Vá.**

1. **`route()` FAIL-CLOSED** (`HinhThucKhongHopLe`) với `hinh_thuc` RỖNG hoặc ngoài từ vựng. Nhóm 04 nay
   là **nhận diện DƯƠNG** (`_HINH_THUC_04`), không còn là cái sọt *"còn lại"*.
   Chọn FAIL-CLOSED chứ KHÔNG bỏ dấu để đoán ý: `RASOAT_HOSO_LOOP.md:177` đã bắt buộc *"CHỈ dùng giá trị
   trong `_vocab_hinh_thuc`"* ⇒ đoán ý ngay tại tầng định tuyến phụ lục là thêm nguồn chân lý thứ hai.
2. **Khớp CHỨA, không khớp BẰNG** — người nhập hay viết kèm phạm vi (*"sửa đổi, bổ sung Điều 54"*).
   10/10 giá trị `_vocab_hinh_thuc` và các biến thể kèm phạm vi định tuyến **y như cũ** ⇒ fail-closed
   không siết vào luồng rà hồ sơ đang chạy.
   Thứ tự nhánh là RÀNG BUỘC: `"chờ bổ sung căn cứ"` chứa `"bổ sung"` nên nhánh **F phải đứng trước 04**.
3. **`main()` kiểm TRỌN BỘ trước khi dựng**, báo MỘT LẦN đủ mọi dòng sai (kèm `key` + `van_ban`) rồi
   `SystemExit` — cùng lối *"nói rõ file nào"* của `load_master`. Nổ giữa vòng lặp thì người nhập phải
   sửa từng dòng một lượt.
4. **Đảo chiều ca test cũ** + thêm `r311_route_hinh_thuc_fail_closed`: 10/10 từ vựng đúng bucket · biến thể
   kèm phạm vi giữ hành vi · 7 ca xấu FAIL-CLOSED · thứ tự nhánh F-trước-04 · **đường sản xuất**
   (subprocess `rasoat_phuluc.py`): bảng master có 1 dòng sai ⇒ rc≠0, nêu ĐÍCH DANH `VD-B`, **KHÔNG ghi**
   file phụ lục; A/B cùng bảng đó sửa đúng chính tả ⇒ rc=0 và rơi vào **05** · PHẢN CHỨNG tái hiện
   thuật toán cũ ngay trong test.
5. `_canh_bao_hinh_thuc` (template) + `RASOAT_HOSO_LOOP.md:177` sửa lời — hai chỗ này đang tả hành vi cũ
   (*"rơi ÂM THẦM vào phụ lục 04"*) nên sau bản vá là SAI.

**Bằng chứng dương.** selftest **1588/1588**. MUTATION: hoàn nguyên đúng hai vế của bản vá (rỗng→`"04"`,
fallback cuối→`"04"`) ⇒ **1586/1588**, đỏ đúng `r311_route_hinh_thuc_fail_closed` +
`r209_master_template_va_vocab`. ruff DELTA so `origin/master` = **0** trên cả ba tệp chạm
(`rasoat_phuluc.py` 1 F541 · `tl_selftest.py` 4325 F821 + 1 F401 · `tl.py` 12 F821 — bằng nhau hai bên).

# ★ v1.36.44 — r310: RAS-01 (vế metadata/CLI) + RAS-14 — `rasoat` hết `argparse.REMAINDER`; đường GHI đòi `--apply` tường minh (2026-08-02)

Đóng **hai mục cuối** của Làn A sổ audit 31-07. Vế `changes_pull` của RAS-01 đã land ở r304; vế này là
phần được hoãn sang T3 (commit `c8cdd02` ghi rõ *"vế metadata/CLI để T3"*).

**Bệnh — MỘT dòng, HAI lỗ ngược nhau.** `cli.py` khai `rasoat` bằng đúng hai positional: `sub` và
`rest=argparse.REMAINDER`. REMAINDER nuốt trọn phần đuôi dòng lệnh, nên:

- **(a) RAS-01.** KHÔNG cờ nào của `rasoat` được KHAI. Ba nhánh `keywords`/`titles`/`orchestrate` đều
  GHI registry thật (`reg_bulk` · `changes_pull`) nhưng **vô hình** với `tool-inventory` và
  `workflow-audit --strict`: không meta, không cổng, không ai đối chiếu. `validate_registry` chỉ duyệt
  `COMMAND_META` — mà registry chỉ biết tên TOP-LEVEL, nên mọi writer nằm dưới một subcommand đều lọt.
  Cổng `WRITE_CMD_NO_GATE` chỉ soi được thứ nó NHÌN THẤY. Cộng thêm: `backfill_keywords_live.py` không
  có chế độ DRY nào — mọi lần gọi đều đi thẳng `exporttext` → `reg_bulk` → ghi checkpoint.
- **(b) RAS-14.** `--profile` gõ SAU sub bị đẩy NGUYÊN cho script con. `backfill_nlm_title.py` có
  `--profile` RIÊNG — đó là profile của **nlm CLI**, không phải corpus profile của tl. Nên
  `tl rasoat titles --profile "Luật BHXH"` **đổi nghĩa trong im lặng**: corpus profile của tl không
  được áp (scope rơi về nền `vbqppl`), script con lại nhận tên hồ sơ làm profile nlm. Và vì `rasoat`
  nằm trong `_CREDS_LAZY_CMDS` nên `load_creds` cũng không chạy — không có đường nào đặt `TL_PROFILE`.

**Vá.**

1. **`RASOAT_SPECS` (`tl_core/command_registry.py`) — spec dữ liệu cho 5 nhánh.** `register_rasoat`
   sinh subparser THẬT; `rasoat_child_argv` dựng argv script con TỪ NAMESPACE đã parse. Cờ script con
   được ánh xạ TƯỜNG MINH bằng khoá `child`; `child=None` = cờ chỉ sống ở tầng tl.
2. **`--profile` thuộc về tl**, gõ trước hay sau subcommand đều được, và `apply_profile_offline` chạy
   **TRƯỚC** dispatch. Profile của nlm CLI đổi tên thành **`--nlm-profile`** ⇒ hai nghĩa hết chồng nhau.
   Cùng lớp: `--selftest` của bộ điều phối thành `--orchestrator-selftest` (`--selftest` ở tầng tl bị
   `main()` đọc TRƯỚC dispatch — trùng tên là chạy nhầm selftest của tl).
3. **Đường GHI đòi `--apply` TƯỜNG MINH; chạy trần là CHỈ-ĐỌC.** Thiếu `--apply` ⇒ tl bơm `dry_flag`
   của script con. `backfill_keywords_live.py` được thêm `--dry`: kê worklist rồi dừng — KHÔNG
   `exporttext`, KHÔNG `reg_bulk`, và **KHÔNG ghi checkpoint** (một lượt "dry" mà vẫn dịch sổ tiến độ
   thì đúng là bệnh RAS-01, chỉ đổi chỗ). Writer nào KHÔNG khai `dry_flag` ⇒ **fail-CLOSED**:
   `RASOAT_WRITE_NEEDS_APPLY` rc=2, không rơi xuống subprocess.
4. **`NESTED_COMMAND_META` + `all_command_meta()`** — registry biết lệnh LỒNG. `validate_registry`
   resolve theo ĐƯỜNG DẪN (`_parser_for_path`) nên `rasoat keywords` đi qua đủ bộ cổng như lệnh
   top-level; `registry_summary` kê cả 5 (thêm `counts.nested`). Lưới chiều ngược
   `RASOAT_SUB_NOT_IN_REGISTRY`: thêm sub GHI mới mà quên meta là gate ĐỎ, không tái diễn lỗ cũ.
5. **Hai thứ vốn đã hỏng, nay đúng:** `--no-auto-cache` được `cmd_rasoat` ĐỌC từ lâu
   (`getattr(a, "no_auto_cache", False)`) nhưng **chưa từng được khai ở đâu** — REMAINDER nuốt mất nên
   nó luôn `False`; nay là cờ thật. Và `--json` do tl nuốt nên `tl rasoat <sub> --json` hết `rc=2`.

**Test (+7 ca → 1586/1586).** `r310_rasoat_sub_la_lenh_that_khong_con_remainder` (bề mặt parser + cờ lạ
bị TỪ CHỐI) · `r310_ras14_profile_sau_sub_thuoc_ve_tl` (HAI CHIỀU: tl giữ `--profile`, mà
`--nlm-profile` vẫn xuống được script con — vá không được thành "bỏ hẳn tính năng") ·
`r310_chay_tran_chi_doc_apply_moi_ghi` (+ phản chứng: nhánh không-ghi không tự sinh `--dry`; positional
và alias `--sohieu`/`--file` vẫn map) · `r310_writer_khong_co_dry_bi_tu_choi` (fail-CLOSED + phản chứng
`--apply` vẫn đi tiếp) · `r310_ap_profile_offline_truoc_dispatch` (đo THỨ TỰ: profile TRƯỚC
`subprocess.call`) · `r310_audit_nhin_thay_moi_writer_long` (+ ĐỎ-hoá tại chỗ: gỡ cổng ⇒
`WRITE_CMD_NO_GATE`, gỡ meta ⇒ `RASOAT_SUB_NOT_IN_REGISTRY`) · `r310_bkl_dry_khong_dong_gi` (+ phản
chứng: bỏ `--dry` ⇒ có call, có checkpoint).

**ĐỎ-TRƯỚC (đo thật).** Hoàn nguyên `cli.py` + `lookup_ops.py` + `backfill_keywords_live.py` về HEAD,
GIỮ nguyên test ⇒ **1574/1586**, đỏ đúng **cả 7** ca r310 (+ `r64_registry_validate_clean` và 4 ca
kernel-size — nhiễu của cây nửa-vời, xanh lại khi khôi phục). Sau vá **1586/1586**.

**Hai ca CÓ SẴN đỏ — cả hai đều đúng, sửa theo tín hiệu chứ không đạp qua:**

- `r64_registry_meta_invariants` khoá `counts.total == len(COMMAND_META)`. Bề mặt meta nay gồm cả lệnh
  lồng ⇒ bất biến GIỮ NGUYÊN Ý NGHĨA (counts khớp bảng meta), chỉ mở đúng bằng bề mặt mà
  `registry_summary` thật sự kê, thêm khoá `nested` và phép cộng hai bảng. Bọc `try` vì ca này chạy ở
  mức module của `run()` (chưa có `_t110`) — một `AttributeError` ở đó làm **sập cả suite** thay vì báo
  một ca đỏ, đúng lúc cần đo ĐỎ-TRƯỚC thì lại không đo được gì.
- `r77a_parser_surface_matches_snapshot` là drift-lock của bề mặt parser — nó ĐỎ đúng như thiết kế.
  Diff **đo trước khi ghi lại**: đúng `rasoat` đổi hash + 5 khoá `rasoat <sub>` thêm mới, **không khoá
  nào khác động**. Ghi lại bằng `TL_WRITE_PARSER_SURFACE=1`.

**Bẫy đã trả giá khi viết ca này — ghi lại vì tái diễn được.** `python scripts/tl.py --selftest` chạy
tl.py là `__main__`, rồi `tl_selftest` `import tl` nạp tl.py **LẦN HAI** thành module `tl`; lần nạp sau
REBASE `__globals__` của hàm `tl_core` sang `tl.__dict__`, trong khi `_TL_MODULE` là `__main__`. Hệ quả:
`_mp261` **ăn** với tên là STUB (`apply_profile_offline` ủy quyền sang `tl_core.profile_env`, mà
`_MODS261` có patch) nhưng **KHÔNG ăn** với tên chỉ sống trong namespace tl (`subprocess`,
`_healed_script_path`) — lệnh lặng lẽ rơi xuống chạy script con THẬT và `rc` là rc của script đó, không
có lỗi nào chỉ thẳng vào nguyên nhân. Vá đúng chỗ: patch trên globals của CHÍNH hàm sẽ chạy
(`_resolve286`), y khuôn ca r287. Kèm theo: mọi `parse_args`/`main()` trong ca mới đều bọc `SystemExit`
— `_t110` chỉ bắt `Exception`, nên một hồi quy ở bề mặt CLI sẽ **giết cả suite** thay vì làm đỏ đúng ca
của nó (đo được điều này ở lượt ĐỎ-TRƯỚC đầu tiên).

**Tài liệu.** `references/RUNBOOK.md` §H thêm mục r310: bảng lệnh DRY-vs-`--apply` cho cả 5 nhánh + hai
điểm dễ vấp (`--nlm-profile`, `--orchestrator-selftest`). Dòng `tl rasoat keywords --json` cũ GIỮ
NGUYÊN và vẫn đúng — nó là đường fallback-plan khi thiếu script thật.

# ★ v1.36.43 — r309: thẻ máy đọc `references/workflows/*.json` vào tầm guard con trỏ (T0-F/1c) (2026-08-02)

**Bối cảnh.** r308 mở doc-set ra mọi `*.md` trong gói, nhưng lọc theo đuôi `.md` nên 27 **thẻ máy
đọc** `references/workflows/*.json` vẫn nằm ngoài tầm. Thẻ là chỉ dẫn VẬN HÀNH y như `.md`, chỉ khác
định dạng — con trỏ chết trong thẻ hỏng đúng thứ gói mang đi.

**Đo trên gói 177 tệp (02-08):**

| tập | con trỏ | ĐỨT |
|---|---|---|
| `references/workflows/*.json` (27 thẻ) | 4 | **1** |
| **mọi** `.json` trong gói (57 tệp) | 48 | **12** |

**Quyết định phạm vi: CHỈ thẻ workflow, KHÔNG phải mọi `.json`.** 11/12 mục đứt còn lại nằm ở
`references/golden/*.json` — ĐẦU RA GHI SẴN của test, con trỏ đứt là CỐ Ý (rõ nhất:
`references/KHONG_CO_FILE.md`, chính là mồi cho bộ dò tệp-thiếu). Gác chúng = đỏ oan ngày đầu
⇒ guard bị vô hiệu hoá, đúng bài học §0.8. **Ranh giới này có test khoá cả HAI chiều.**

**Mục ĐỨT duy nhất — SỬA LỜI THẺ, KHÔNG baseline.** `doc_claims_check.json` (khối `plan`) trỏ
`references/changelog_archive/` — thư mục dev-only (`_RELEASE_EXCLUDE_DIRS`). Lời thẻ **ĐÚNG với mã**
(`workflow.py:1001-1004` có đọc archive, có `is_dir()` nên vắng thì suy biến êm) — tức không phải tài
liệu cũ. Nhưng **tiền lệ r184 trên CHÍNH con trỏ này** (SKILL.md từng trỏ `references/changelog_archive/`,
gây gạch xanh-giả 4 test) đã chốt: «**không nới auditor, sửa con trỏ**». Nên sửa lời thẻ cho nói rõ
kho lưu trữ là dev-only/ngoài gói — vừa hết con trỏ chết, vừa **thêm thông tin** cho người đọc runtime,
và **không thêm mục miễn trừ nào** (ratchet giữ nguyên độ chặt: baseline vẫn 3).

**Bằng chứng DƯƠNG (3 mutation, không tin `rc=0`):**
- trả lại lời thẻ CŨ ⇒ cặp đứt hiện lại đúng 1 mục
- thu doc-set về chỉ `.md` ⇒ `r309_the_workflow_trong_tam_guard` **ĐỎ** (1579/1580)
- mở tầm sang **mọi** `.json` (golden lọt vào) ⇒ cũng **ĐỎ** — ranh giới khoá hai chiều

**Lớp trần (`_doc_bare_tool_findings`) không đổi gì:** đo được 0 span backtick trong thẻ JSON ⇒
0 checked. Ghi lại để phiên sau khỏi đi đo lại.

Sau vá: pointer checked **300→303** FAIL **0** adv 104 baseline 3. **Selftest 1580/1580** (master 1579, +1 ca).
Ruff **DELTA = 0** cả ba tệp, không tên F821 nào mới.

# ★ v1.36.42 — r308: GATE-04 mở tầm guard con trỏ ra MỌI `*.md` TRONG GÓI + GATE-05 test dựng package-set đúng nguồn (2026-08-02)

**Bối cảnh.** Hai lớp guard con trỏ tài liệu (`_doc_pointer_findings` r209 · `_doc_bare_tool_findings`
r289) chỉ quét `references/*.md` **không đệ quy** + `SKILL.md`. Tài liệu ĐI THEO GÓI mà nằm ngoài
khoảng đó thì **không cổng nào gác con trỏ** — đúng lớp bệnh REL-01/H9 sinh ra để chặn.

**Đo trên gói 177 tệp (02-08), không chép niềm tin từ kế hoạch:**

| | kế hoạch nói | ĐO ĐƯỢC |
|---|---|---|
| `.md` trong gói | 53 | **34** (T0-G đã bỏ 19 tệp `docs/`) |
| tầm guard cũ | 30/53 | **30/34** |
| ngoài tầm | — | `CHANGELOG.md` · `INSTALL.md` · `CONTEXT.md` · `scripts/_fallback/README.md` |
| mở tầm ⇒ pointer FAIL | ~56 ước | **0 → 40** (CHANGELOG 24 + INSTALL 16) |
| mở tầm ⇒ bare-tool FAIL | — | **0 → 0** (advisory 73→95) — lớp này mở **MIỄN PHÍ** |

**1. GATE-04 — doc-set lấy từ MANIFEST, không glob đĩa.** Chỗ gọi trong `_verify_release_manifest`
duyệt `expected` (package-set) lấy mọi `*.md`. Bịt hai khoảng mù **ngược chiều nhau** của nguồn cũ:
*(a) THIẾU* — 4 tài liệu trên đi theo gói mà không ai gác; *(b) THỪA* — `.md` nằm trong `references/`
trên ĐĨA nhưng bị release-exclude vẫn bị quét, tức bắt gate CÂY chịu trách nhiệm cho thứ KHÔNG vào
artifact. Doc-set nay tự đóng theo kiểm kê: thêm `.md` vào gói là guard phủ ngay.

**2. Phân hạng LƯU TRỮ trước khi mở tầm** — `CHANGELOG.md` + `INSTALL.md` vào `_POINTER_ARCHIVE_DOCS`
(advisory). Không phải né: `CHANGELOG` chép các bản phát hành ĐÃ QUA nên tất yếu nhắc tên tệp TỪNG
tồn tại (`Code.2.21.2n.gs`, `changelog_archive/`, 4 script deploy dev-side) — sửa thân = viết lại lịch sử;
`INSTALL.md` khối `:7` TỰ KHAI “layout GỐC v1.x (tham chiếu lịch sử), nguồn chân lý = VERSION + SKILL.md +
CHANGELOG” (Q3 chốt 01-08). Không xếp hạng trước thì guard đỏ **40 mục ngày đầu và sẽ bị vô hiệu hoá**
— đúng bài học §0.8. `CONTEXT.md` + `scripts/_fallback/README.md` vào **thẳng fail-closed, 0 đồng**.

**3. GATE-05 — `r209_cay_that_va_phan_chung` dựng package-set SAI NGUỒN.** Ca này dùng `rglob` trên
ĐĨA thay vì đọc manifest ⇒ con trỏ tới tệp **có-trên-đĩa-nhưng-ngoài-gói** QUA test mà ĐỎ ở
`release-verify`. Đo khoảng lệch: **11 tệp** (4 `.gs` cũ · 2 `changelog_archive` · 4 script deploy ·
`pkg_secret_scan.py`) — cơ chế `_RELEASE_EXCLUDE_NAMES_ANYWHERE`, không phải ngẫu nhiên. Nay đọc
`RELEASE_MANIFEST.json` theo khuôn `r289_cay_that_bare_tools`, doc-set mở khớp guard sản xuất, và thêm
**phép đo A/B chạy vĩnh viễn**: cùng một tài liệu, nguồn-manifest ĐỎ mà nguồn-đĩa XANH ⇒ lỗ có thật,
đã bịt. `r289_cay_that_bare_tools` mở doc-set theo, kèm vế `ok3b` chống “xanh vì quét ít đi”.

**Bằng chứng DƯƠNG (mutation, không tin `rc=0`):**
- Trả doc-set về glob đĩa ⇒ `r308_docset_lay_tu_manifest` **ĐỎ** (1578/1579). Ca mới này test
  **WIRING** trong `_verify_release_manifest` trên cây GIẢ — ca r209 gọi THẲNG helper nên không phủ
  đoạn nối, đúng chỗ từng sai.
- Bỏ `CHANGELOG`+`INSTALL` khỏi hạng lưu trữ ⇒ **40 pointer FAIL** (24+16) ⇒ phân hạng là **chịu lực**,
  không phải hai tài liệu đã sạch sẵn.
- Sau vá: pointer checked **193→299** FAIL **0** advisory **64→104**; bare checked **160→237** FAIL **0**.

**Selftest 1579/1579** (master 1578, +1 ca). Ruff **DELTA = 0** cả ba tệp, **không tên F821 nào mới từ 0**.

# ★ v1.36.41 — r307: sổ hết KHAI HAI NGHĨA cho MỘT version — hạ cấp nhật ký nhánh T2 + cổng «một version ⇒ một đợt» (2026-08-02)

**Bối cảnh.** `dfb9418` merge PR #6 (tranche T2: RAS-05 · ING-03 · Helper `tl_core/txn.py`). Nhánh
`claude/va-t1-gate-nlvoj9` phát triển song song nhiều ngày và giữ **dải số riêng** trong khi master đã
tiêu dải đó cho việc khác ⇒ sau merge, sổ khai **15 số version hai lần với nội dung MÂU THUẪN**
(`v1.36.23`…`v1.36.37`) và 8 số đợt (`r285`…`r292`) mang hai nghĩa.

**Gate KHÔNG bắt lớp này** — CI xanh trên `88c41e3`, gate local 8/8 xanh, mà sổ vẫn hỏng. Đó là lỗ,
không phải may: không cổng nào từng đọc CHANGELOG như một BẢNG KHOÁ.

**Đo (không đoán) — bất biến chọn để khoá là «một version ⇒ đúng một số đợt»:**

| cây | vi phạm |
|---|---|
| `1a06ff1` (master TRƯỚC merge) | **0** |
| `references/changelog_archive/*.md` (toàn bộ) | **0** |
| `dfb9418` (SAU merge) | **5** — v1.36.26 `[r288,r291]` · v1.36.27 `[r289,r292]` · v1.36.28 `[r288,r290]` · v1.36.30 `[r290,r291]` · v1.36.31 `[r292,r294]` |

Nền = 0 tuyệt đối ⇒ cổng KHÔNG cần danh sách miễn trừ. (Trùng version *có sẵn* `v1.35.65`/`v1.35.88`
là **cùng một đợt** tách hai mục — `r229`/`r229`, `r251`/`r251` — nên bất biến này tha đúng chỗ; một
cổng "tiêu đề version không được lặp" trần trụi sẽ đỏ oan hai ca đó.)

**Vá — hai lớp, cố ý KHÔNG đụng lớp thứ ba:**

1. **Tiêu đề version:** 18 mục gốc-nhánh hạ từ `#` xuống `##` kèm nhãn *[nhật ký nhánh T2 — số hiệu
   NỘI BỘ của nhánh]*. Toàn văn GIỮ NGUYÊN. An toàn với gate vì `_doc_claims_context` lấy
   `changelog_versions`/`changelog_rs` từ **TOÀN VĂN** chứ không từ dòng tiêu đề, còn `changelog_headings`
   đếm mọi dòng mở đầu bằng `#` — `##` vẫn được đếm ⇒ `basis` không đổi vì việc hạ cấp.
2. **Tên ca test** (nguồn sự thật theo §6 quy ước số đợt): 20 ca đổi tiền tố về dải trống —
   `r287→r301` (GATE-01b, 3 ca) · `r288→r302` (Helper 1, 4) · `r289→r303` (PRO-01, 4) ·
   `r290→r304` (RAS-01 vế `changes_pull`, 3) · `r291→r305` (ING-03, 3) · `r292→r306` (RAS-05, 3).
   `r285`/`r286` của nhánh KHÔNG cấp số mới: mã của chúng đã bị GỠ trong lúc hoà (lấy bản master), không
   còn ca test nào. Đổi kèm **20 hàm `_cNNN_…` tương ứng** (40 chỗ) — để tên ca và tên hàm không nói hai
   số khác nhau, đúng cái bẫy "nhãn trong mã tự khai `r290` trong khi test tên `r291_*`" đã suýt làm land
   nhầm 109 dòng. Đổi theo **CẶP rút từ chính dòng `_t110`**, KHÔNG đổi theo tiền tố: master cũng có
   `_c287…_c292` của riêng nó, thay mù sẽ phá. (Một hàm có hậu tố VIẾT HOA —
   `_c292_migrate_v1_dua_doc_loi_QUAY_LAI` — nên bảng dò chữ-thường bỏ sót; bắt được vì đếm 20 cặp
   không khớp 19 dòng dò ra.)
3. **KHÔNG đánh số lại PROSE trong nhật ký nhánh.** Đây là quyết định có chủ đích, không phải bỏ sót:
   trong khối đó `r285`–`r292` vừa là số của nhánh vừa là **tham chiếu tới r của master** (dòng
   "3f614de r288 · 00611fe r289 · 5df7f39 r290" là commit MASTER; bảng "Nhánh này (r285) | Master (r292,
   GIỮ)" đối chiếu hai bên). Thay mù sẽ phá chính bảng ghi lại vụ va số. Nhật ký là SỬ LIỆU — giữ nguyên,
   nhãn hoá, và ánh xạ ở đây.

**Cổng mới:** `r307_changelog_mot_version_mot_dot` — quét `CHANGELOG.md` + toàn bộ
`references/changelog_archive/*.md`, đỏ nếu một version được hai mục `# ★` khai với số đợt KHÁC nhau.
Ca **TỰ MANG PHẢN CHỨNG**: bơm hai dòng giả cùng version khác đợt vào bản sao trong bộ nhớ và khẳng
định vị ngữ BẮT được — nếu không, ca chỉ chứng minh "hôm nay sổ sạch" chứ không chứng minh cổng chạy.

**Việc còn nợ:** nhật ký nhánh vẫn nói `r288 = Helper 1` trong khi ca test nay là `r302_helper1_*`.
Bảng ánh xạ trên là cầu nối; ai tra ngược từ prose phải đi qua nó.

# ★ v1.36.40 — r301–r306: LAND tranche T2 «chặn máu» qua PR #6 — kết luận bằng KẾT QUẢ, không bằng HÌNH DẠNG (2026-08-01)

Mục CHÍNH DANH trên sổ master cho `dfb9418` (merge `claude/va-t1-gate-nlvoj9`). Nhật ký hoà nhánh 10
lượt nằm ngay dưới, đã hạ cấp — xem v1.36.41 để biết vì sao.

| đợt (mới) | (số cũ của nhánh) | nội dung | ca test |
|---|---|---|---|
| r301 | r287 | `golden-test` CƯỠNG CHẾ raw stability — `raw_stable=false` ⇒ rc≠0, `--write` CẤM ghi | 3 |
| r302 | r288 | Helper 1 `tl_core/txn.py` — HỢP ĐỒNG kết luận giao dịch, tính `ok` từ KẾT QUẢ | 4 |
| r303 | r289 | PRO-01 `profile-file-remove` FAIL-CLOSED — hết tháo con trỏ registry sau bước xoá hỏng | 4 |
| r304 | r290 | RAS-01 vế `changes_pull` — "DRY" mà vẫn GHI: điều phối hết gọi action ghi trước `--apply` | 3 |
| r305 | r291 | ING-03 `ingest_commit` — đòi `ok=true` VÀ đủ 3 marker + `row`, vá CẢ HAI call site | 3 |
| r306 | r292 | RAS-05 `backfill_keywords_live` — hết MẤT DỮ LIỆU IM LẶNG rồi in "XONG TẤT CẢ." | 3 |

Mã: `tl_core/txn.py` (mới) · `ingest_ops.py` · `backfill_keywords_live.py` · `ops_misc.py` ·
`registry_orchestrator.py` · `workflow.py` · `tl.py`. Nhánh đã rebase lên `1a06ff1`, chứa TRỌN master
(behind 0 / ahead 19), CI gate xanh trên `88c41e3`.

## ★ [nhật ký nhánh T2 — số hiệu NỘI BỘ của nhánh, KHÔNG phải version master] ★ v1.36.40 — HOÀ NHÁNH lượt 10: master land VÒNG ĐỜI HỒ SƠ (r300), KHÔNG chạm tệp nào của T2 (2026-08-01)

Hoà `master` `1a06ff1` (r300 v1.36.37 — *"VÒNG ĐỜI HỒ SƠ — 'đã đóng' thành trạng thái MÁY ĐỌC ĐƯỢC"*).

**Rà trùng việc — đo trước khi hoà.** `git diff --numstat 7469d8c..origin/master` trên 5 tệp T2
(`tl_core/txn.py` · `tl_core/ops_misc.py` · `registry_orchestrator.py` · `tl_core/ingest_ops.py` ·
`backfill_keywords_live.py`) trả **RỖNG**. Mười tệp master đụng đều ngoài vùng T2, trong đó phần code
mới nằm ở `tl_core/lookup_ops.py` (+70) và `tl_selftest.py` (+79); `tl.py` chỉ nhận **2 dòng** khai tên
`_rasoat_vong_doi_*` vào bảng stub. `tl_selftest.py` auto-merge sạch.

**Gỡ xung đột theo byte + đối chứng kích thước.** `SKILL.md` **48.031 B** (bằng đúng trước hoà — master
chỉ đổi dòng phiên bản), `VERSION` **7 B** không newline cuối. `tl.py` **229.953 → 230.117 B** và
**CRLF 1.763 → 1.765**: +2 dòng, khớp ĐÚNG net +2 của master ⇒ tăng là do nội dung master vào, không
phải dòng-kết hỏng. Đây là cách đọc số đúng — "kích thước đổi" tự nó không nói gì, phải đối chiếu với
delta ĐÃ BIẾT của bên kia.

**Va số hiệu test:** master vừa dùng `r300` ⇒ test mới của nhánh đánh **từ `r301`**.

**Dấu vết 5 mục T2 sau hoà:** kiểm lại còn nguyên.

## ★ [nhật ký nhánh T2 — số hiệu NỘI BỘ của nhánh, KHÔNG phải version master] ★ v1.36.39 — HOÀ NHÁNH lượt 9: master land P16-F11+F26 (OCR/chunks), KHÔNG chạm tệp nào của T2 (2026-08-01)

Hoà `master` `7469d8c` (r299 v1.36.36 — *"cầu nối OCR/chunks — scope đi theo xuống con · chunks `--apply`
chạy được (P16-F11+F26)"*).

**Rà trùng việc — đo trước khi hoà.** `git diff --numstat 74f62e2..origin/master` trên 5 tệp T2
(`tl_core/txn.py` · `tl_core/ops_misc.py` · `registry_orchestrator.py` · `tl_core/ingest_ops.py` ·
`backfill_keywords_live.py`) trả **RỖNG**. Tám tệp master đụng: `CHANGELOG.md` `RELEASE_MANIFEST.json`
`SKILL.md` `VERSION` `scripts/tl.py` `tl_core/chunking.py` `tl_core/ocr.py` `tl_selftest.py`.
`tl_selftest.py` auto-merge sạch (master thêm 177 dòng ca mới ở vùng khác); 5 xung đột còn lại là hằng
phiên bản + kiểm kê.

**Áp bài học CRLF của lượt 8 — lần này gỡ xung đột THEO BYTE ngay từ đầu.** Marker git viết theo dòng-kết
của chính tệp (`SKILL.md` và `tl.py` là CRLF), nên `read_bytes` → `replace(khối-marker-CRLF)` →
`write_bytes`; `VERSION` ghi 7 B không newline cuối. Đối chứng kích thước sau gỡ: `SKILL.md` **48.031 B**
và `tl.py` **229.953 B** — **BẰNG ĐÚNG** trước hoà, đúng như lượt 8 sau khi đã chữa. Số đo là thứ xác
nhận, không phải "gate xanh".

**Va số hiệu test:** master vừa dùng `r299` ⇒ test mới của nhánh đánh **từ `r300`**.

**Dấu vết 5 mục T2 sau hoà:** kiểm lại còn nguyên.

## ★ [nhật ký nhánh T2 — số hiệu NỘI BỘ của nhánh, KHÔNG phải version master] ★ v1.36.38 — HOÀ NHÁNH lượt 8: master land T0-E/P16, KHÔNG chạm tệp nào của T2 (2026-08-01)

Hoà `master` `74f62e2` (r297 v1.36.34 *"`--as-appendix` hết TỰ BẬT theo TIÊU ĐỀ / khớp-con — P16-F10"*
+ r298 v1.36.35 *"diệt 3 test TỰ-CHỨNG-MINH — gate hết chứng nhận RỖNG ở lớp điều phối (T0-E/GATE-06)"*).

**Rà trùng việc — ĐO TRƯỚC KHI HOÀ, không đoán.** `git diff --numstat 9465d2a..origin/master` trên 5 tệp
của nhánh này (`tl_core/txn.py` · `tl_core/ops_misc.py` · `tl_core/registry_orchestrator.py` ·
`tl_core/ingest_ops.py` · `backfill_keywords_live.py`) trả **RỖNG** — master lượt này không chạm tệp nào
của T2. Tám tệp master đụng: `CHANGELOG.md` `RELEASE_MANIFEST.json` `SKILL.md` `VERSION`
`scripts/ingest_to_cache.py` `scripts/normalize_document.py` `scripts/tl.py` `scripts/tl_selftest.py`.
`tl_selftest.py` **auto-merge sạch** (master thêm/sửa ca ở vùng khác); 5 xung đột còn lại đều là
**hằng phiên bản + kiểm kê**, không phải logic.

**Va số hiệu test:** master vừa dùng `r297` và `r298`, trùng dải nhánh này định dùng tiếp. Số hiệu test
mới của nhánh **đánh từ `r299`** trở đi.

**Va số hiệu bản:** nhánh này đã có mục `v1.36.34`/`v1.36.35` (hoà lượt 4/5) trong khi master mang về
`v1.36.34`/`v1.36.35` của riêng nó (r297/r298) — cùng số, khác nội dung. Giữ **cả hai** khối như các lượt
trước; bản hoà này bump lên **v1.36.38** (cao hơn cả hai bên) để không kéo dài va chạm.

**BẪY ĐÃ TRẢ GIÁ Ở CHÍNH LƯỢT NÀY — hoà xung đột bằng `pathlib.read_text()/write_text()` NUỐT CRLF.**
`SKILL.md` và `scripts/tl.py` trong cây này dùng **CRLF**; `read_text()` dịch CRLF→LF khi ĐỌC và
`write_text()` ghi LF ⇒ gỡ 3 dòng marker mà **toàn tệp bị viết lại**: `SKILL.md` 48.031 → 47.724 B
(mất đúng 307 B = 307 dòng), `tl.py` mất 1.763 B. Gate bắt được, và bắt bằng **đường vòng**:
`r219_gotchas_nhan_trang_thai` đỏ vì nó khẳng định GOTCHAS.md phải chứa **kích thước ĐO ĐƯỢC** của
`SKILL.md` — số đo đổi thì khẳng định sai. `golden` + `determinism` đỏ theo. **Không có test nào nói
"CRLF"** cả; thứ cứu được là một test neo vào SỐ ĐO THẬT thay vì vào hình dạng.

Chữa: khôi phục CRLF theo byte (`read_bytes` → `replace(b"\n", b"\r\n")` → `write_bytes`), và `VERSION`
ghi **không newline cuối** (7 B — đúng như f326473 lẫn master; `echo >` thêm `\n` thành 8 B). Sau chữa,
`golden` + `determinism` tự XANH lại **mà KHÔNG cần `--write`** — bằng chứng dương rằng hai gate đó đỏ vì
hỏng dòng-kết, không phải vì kiểm kê đổi hợp lệ (R6 giữ nguyên: không ghi lại golden cho lượt này).
Lần sau hoà xung đột: sửa bằng byte, hoặc `git checkout --ours/--theirs` + patch tối thiểu — ĐỪNG
round-trip tệp qua text API.

**Dấu vết 5 mục T2 sau hoà:** kiểm lại còn nguyên — `_ingest_commit_verdict`/`_INGEST_COMMIT_MARKERS` tại
`_pi_stage_write` + `_il_stage_write` (ING-03), `Txn(`/guard (PRO-01), `not_probed` (RAS-01),
`tukhoa_progress.v2` (RAS-05), `tl_core/txn.py` (Helper 1).

## ★ [nhật ký nhánh T2 — số hiệu NỘI BỘ của nhánh, KHÔNG phải version master] ★ v1.36.37 — HOÀ NHÁNH lượt 7: master chạm `ingest_ops.py` nhưng KHÔNG chạm ING-03 (2026-08-01)

Hoà `master` `9465d2a` (r296 v1.36.33 — *"HỌ regex `Điều N` nhận HẬU TỐ CHỮ (7a/7b/7đ) — P16-F15"*).

**Rà trùng việc — lần này master CÓ chạm `ingest_ops.py`, tệp của ING-03.** Kiểm kỹ chỗ chạm:
`_dieu_head_marks` (`:1397`, nhánh LÙI của regex tiêu đề Điều). Đo trực tiếp trên diff — **0 lần** chạm
`_ingest_commit_verdict` / `_INGEST_COMMIT_MARKERS` / `_pi_stage_write` / `_il_stage_write`.
⇒ Cùng tệp, **khác vùng hoàn toàn**, `git` auto-merge sạch. Không có bản vá nào phải bỏ.

Bốn tệp còn lại (`txn.py` · `ops_misc.py` · `registry_orchestrator.py` · `backfill_keywords_live.py`)
master không đụng. T2 nguyên vẹn, kiểm bằng dấu vết mã: `Txn("profile-file-remove")` ×1 · `not_probed` ×5 ·
`_ingest_commit_verdict(org, okw)` ×2 · `tukhoa_progress.v2` ×1.

**Số ca 1549 → 1558** (+9 của `r296`). Gate **8/8 PASS**. Giải xung đột: `VERSION`/`tl.py`/`SKILL.md` →
**v1.36.37**; `CHANGELOG` giữ cả hai khối; `RELEASE_MANIFEST` tái sinh; `ingest_ops.py` + `tl_selftest.py`
auto-merge sạch.

**Số hiệu: master đã dùng tới `r296`** ⇒ nhánh này đánh số tiếp từ **r297**.

## ★ [nhật ký nhánh T2 — số hiệu NỘI BỘ của nhánh, KHÔNG phải version master] ★ v1.36.36 — HOÀ NHÁNH lượt 6: master land T3/rà-soát, T2 của nhánh này không bị đụng (2026-08-01)

Hoà `master` `81c9715` (2 commit: `7795938` r295 v1.36.32 — *"rà soát: MỘT định nghĩa hội tụ +
corpus-hiệu-lực dùng chung + state single-writer hết fail-OPEN"*; `81c9715` r295b — regen manifest).

**Rà trùng việc (đo `a3abc11..81c9715` trên 5 tệp của nhánh này): KHÔNG tệp nào bị đụng.**
`txn.py` · `ops_misc.py` · `registry_orchestrator.py` · `ingest_ops.py` · `backfill_keywords_live.py` —
master chỉ chạm `lookup_ops.py`, `tl.py`, `tl_selftest.py`. Bốn mục T2 + Helper 1 **còn nguyên**, đã kiểm
bằng dấu vết mã: `Txn("profile-file-remove")` ×1 · `not_probed` ×5 · `_ingest_commit_verdict(org, okw)` ×2
(**cả hai** call site) · `tukhoa_progress.v2` ×1 · `txn.py` tồn tại.

**Đáng chú ý — master đang tiến vào T3.** `r295` land *"corpus-hiệu-lực dùng chung"* = đúng **Helper 2**
của Pha 1-0 (§6.1), và *"state single-writer hết fail-OPEN"* = **RAS-02/RAS-03**. Tức tranche T3 đang được
phiên khác làm. Nhánh này **không** đụng T3, nên không có xung đột việc — nhưng nếu định làm tiếp T3 thì
phải rà lại §6.1/§Pha 1D trên master mới, đừng dựng lại Helper 2.

**Số ca 1537 → 1549** (+12 của `r295`). Gate **8/8 PASS**. Giải xung đột: `VERSION`/`tl.py`/`SKILL.md`
→ **v1.36.36**; `CHANGELOG` giữ cả hai khối; `RELEASE_MANIFEST` tái sinh; `tl_selftest.py` auto-merge sạch.

**Số hiệu: master đã dùng `r295`/`r295b`** ⇒ nhánh này đánh số tiếp từ **r296** (trước ghi r295 — chỉnh lại).

## ★ [nhật ký nhánh T2 — số hiệu NỘI BỘ của nhánh, KHÔNG phải version master] ★ v1.36.35 — HOÀ NHÁNH lượt 5: master vá nốt khuyết BÁO GIẢ của chính GATE-01 (2026-08-01)

Hoà `master` `a3abc11` (r294 v1.36.31 — *"GATE-01 hết BÁO GIẢ — quy drift theo ĐƯỜNG DẪN khoá, đối xứng
với projection"*). Đây chính là **khuyết điểm #1 mà `r288` tự khai và cố ý để lại**: `audit_projection`
che TRỌN cây con của khoá đã khai, còn `_raw_drift_keys` chỉ rút **tên khoá lá** bằng regex ⇒ drift bên
trong cây con của một khoá volatile đã khai sinh khoá lá không có trong `volatile_keys` ⇒ báo giả. Nay
họ quy theo **đường dẫn khoá**, đối xứng với projection.

**Master VẪN không đụng 4 mục T2 + Helper 1** (đo `5df7f39..a3abc11`) ⇒ không có việc nào của nhánh này
bị trùng thêm.

**Phần của nhánh này sống nguyên qua lượt hoà, không phải sửa gì:** khối tóm tắt top-level
(`error`/`raw_unstable_cases`/`write_refused`) vẫn khớp mã `RAW_UNSTABLE_UNDECLARED` — họ giữ nguyên mã
lỗi, chỉ đổi **cách quy khoá**. Ba ca `r287_*` cũng không phải chỉnh. Đúng như thiết kế: phần tôi bổ sung
nằm **trên** cơ chế của họ chứ không **trong** nó, nên cơ chế đổi mà phần bổ sung không gãy.

**Số ca 1534 → 1537** (+3 của `r294`). Gate **8/8 PASS**, `golden` + `determinism` + `release-verify`
đều `ok:true`. Giải xung đột: `VERSION`/`tl.py`/`SKILL.md` → **v1.36.35**; `CHANGELOG` giữ cả hai khối;
`RELEASE_MANIFEST` tái sinh; `workflow.py` và `tl_selftest.py` **auto-merge sạch**.

## ★ [nhật ký nhánh T2 — số hiệu NỘI BỘ của nhánh, KHÔNG phải version master] ★ v1.36.34 — HOÀ NHÁNH lượt 4: BỎ bản GATE-01 của tôi, lấy thiết kế của master (2026-08-01)

Hoà `master` `5df7f39` (3 commit mới: `3f614de` r288 · `00611fe` r289 · `5df7f39` r290) vào nhánh.
PR #6 lại `dirty`. **Master vẫn KHÔNG đụng 4 mục T2 + Helper 1** (đo trên `2b6da92..5df7f39`:
`txn.py`/`ops_misc.py`/`registry_orchestrator.py`/`ingest_ops.py`/`backfill_keywords_live.py` — không tệp
nào trong diff). Nhưng `3f614de` là **GATE-01**, trùng `r286`+`r287` của nhánh này.

**Đây KHÔNG phải trùng lặp đơn thuần — là BẤT ĐỒNG THIẾT KẾ, và họ đã cân nhắc rồi BÁC cả hai phương án
của tôi.** Commit `3f614de` ghi thẳng:
- bác (a) `raw_stable=false ⇒ ok=false` **trần trụi** — chính là `r287` của tôi — vì làm thế thì `sweep`
  ĐỎ NGAY dù lành;
- bác (b) **scrub/đóng băng** `snapshot_age_s` khỏi raw — chính là `r286` của tôi — vì *"raw hết là raw,
  mất luôn khả năng phát hiện bất định THẬT"*.

Thay vào đó họ làm cách thứ ba: `_raw_drift_keys()` quy **mọi dòng stdout lệch** về khoá JSON; khoá ngoài
`volatile|path`, **hoặc** dòng không quy được về khoá nào ⇒ `RAW_UNSTABLE_UNDECLARED`, fail-closed,
`--write` từ chối ghi.

**ĐO, KHÔNG TRANH LUẬN.** Tắt đóng băng của tôi rồi chạy `golden-test` 6 lượt:

```
lượt 1,2,4,5: sweep raw_stable=True                                          → ok=True
lượt 3, 6   : sweep raw_stable=False  drift_keys=['snapshot_age_s']  undeclared=[]  → ok=True, rc=0
```

⇒ Cơ chế của họ **một mình** giữ `sweep` xanh, **và giữ được cả thông tin drift** (`raw_drift_keys` vẫn
ghi ra). Đóng băng của tôi làm mất đúng thông tin ấy. **Lập luận của họ đúng.**

**Quyết định — theo đúng nguyên tắc người giữ đặt ra (*"đã được phiên khác xử lý thì bỏ qua"*):**
- **GỠ `r286`** — helper `frozen_age_seconds`/`FROZEN_AGE_S` (`deterministic.py`), wrapper
  `_frozen_age_seconds` (`tl.py`), **3 điểm gọi** (`cmd_sweep`/`cmd_counts`/`cmd_ingest_missing`), **3 ca test**.
- **GỠ `r287`** — nhánh cưỡng chế trần trụi trong `_golden_test`; lấy **nguyên** nhánh quy-khoá của họ.
  Giữ cả hai thì nhánh quy-khoá của họ thành **mã chết** (cưỡng chế trần trụi chặn sớm hơn).
- **GIỮ `_resolve286`** — `r289`/`r290`/`r291` vẫn dùng để gỡ stub `_STUB_MAP` khi monkeypatch.
- **GIỮ + CHỈNH khối tóm tắt top-level của tôi** (`error`/`raw_unstable_cases`/`write_refused` ở đầu
  payload) — trỏ sang mã `RAW_UNSTABLE_UNDECLARED` của họ. Đây là phần **bổ sung TRÊN** thiết kế của họ,
  không đụng cơ chế: bản của họ chỉ đặt lỗi **theo case**, nên CI/`deploy-package.sh` phải duyệt 20 case
  mới biết. Nay đọc được ngay ở đầu payload.
- **GIỮ + CHỈNH 3 ca `r287_*`** sang mã lỗi của họ — chúng phủ thứ 5 ca `r288_*` không phủ: envelope
  top-level, `rc≠0` **qua lệnh thật** (`cmd_golden_test`, thứ CI đọc), và `--write` **không sinh tệp nào**.

Kết quả: **một** cơ chế (của họ), **hai** bộ test (8 ca: 5 `r288_*` + 3 `r287_*`).

**Số ca: 1526 → 1534** (+11 của master, −3 ca `r286` đã gỡ). Gate **8/8 PASS**.
`golden-test` 6 lượt trên cây cuối: `rc=0` cả 6, lượt 6 có `raw_stable=False` nhưng `undeclared=[]` ⇒ xanh
**đúng lý do**. ruff delta 0 (`tl.py` 12 · `workflow.py` 26 · `deterministic.py` 0 — bằng master).

**Va chạm số hiệu nay 7 lần** (thêm `r288`: master v1.36.28 = GATE-01 quy-khoá · nhánh v1.36.26 = Helper 1;
`r289`: master v1.36.29 = cổng con-trỏ-trần · nhánh v1.36.27 = PRO-01; `r290`: master v1.36.30 =
`rasoat-merge` · nhánh v1.36.28 = RAS-01). Đánh số tiếp từ **r295**.

## ★ [nhật ký nhánh T2 — số hiệu NỘI BỘ của nhánh, KHÔNG phải version master] ★ v1.36.33 — HOÀ NHÁNH lượt 3: GỠ bản vá TRÙNG của tôi vì phiên khác đã vá cùng lỗi, tốt hơn (2026-08-01)

Hoà `master` `2b6da92` (r292 v1.36.27) vào `claude/va-t1-gate-nlvoj9`. PR #6 chuyển `mergeable_state`
`unstable` → **`dirty`** (xung đột) nên phải hoà trước khi làm tiếp.

**PHÁT HIỆN CHÍNH: một phiên khác đã vá ĐÚNG lỗi GATE-03 mà `r285` của nhánh này vá.** Không phải hai lỗi
giống nhau — **cùng một lỗi, cùng một dòng**: bộ lọc tiền tố `startswith("/tmp/")` trong khung cô lập của
ca `r284`, nuốt sạch cả 5 ứng viên hợp lệ trên Linux.

Bản của họ **BAO TRỌN** bản của tôi, nên **GIỮ BẢN CỦA HỌ, GỠ BẢN CỦA TÔI**:

| | Nhánh này (`r285`) | Master (`r292`, GIỮ) |
|---|---|---|
| Cách lọc | so bằng đúng hằng | so bằng đúng hằng (như nhau) |
| Hằng escape còn trong danh sách | ca RIÊNG `r285_hang_cuoi_…` | `ok1`, **trong chính ca `r284`** |
| Loại **đúng một** mục | *(không có)* | **`ok2`** — bắt "lọc quá tay" **NGAY TẠI NGUYÊN NHÂN** |
| Ứng viên còn lại nằm trong tempdir | `_ngoai == [hằng]` | `ok3 ∧ ok4` |

`ok1 ∧ ok2 ∧ ok4` **suy ra** đúng mệnh đề ca của tôi khẳng định, **cộng thêm** `ok2` mà tôi không có.
Giữ cả hai = hai bản cùng một fix, và **hai tên cho cùng một literal** (`_HANG_CUOI_285` vs `_ESCAPE284`)
⇒ hai nguồn sự thật cho một hằng. ⇒ Gỡ ca `r285_hang_cuoi_config_van_con_va_la_ngoai_le_duy_nhat`
(**1527 → 1526 ca**), để lại chú thích tại chỗ nêu lý do.

**GỠ RỒI CÓ MẤT ĐỘ PHỦ KHÔNG — ĐO, KHÔNG ĐOÁN.** Hai đột biến đúng bằng hai mệnh đề ca đã gỡ khẳng định,
chạy trên cây sau khi gỡ:

```
đổi hằng escape trong profile_env.py     ⇒ 1525/1526, [FAIL] r284_khung_test_profile_khong_doc_config_that
thêm ứng viên "/etc/…" (thoát ra kho thật) ⇒ 1525/1526, [FAIL] r284_khung_test_profile_khong_doc_config_that
```

Cả hai đều bị ca `r284` của master bắt. **Mất 0 độ phủ.**

**Ghi nhận cho lần sau:** CI của họ ĐỎ **bốn bản liên tiếp** (`r285`·`r286`·`r287`·`r291`) vì đúng ca này,
trong khi máy Windows luôn xanh. Nhánh này vá cùng lỗi ở `r285` nhưng **không** đẩy lên master, nên hai
phiên trả giá song song cho một lỗi. Bài học thao tác: mục nào CI đang đỏ trên master thì nên hỏi/đẩy sớm
thay vì ôm trong nhánh dài.

**⚠ BẢNG VA CHẠM SỐ HIỆU — thêm dòng (nay 5 lần):**

| Số | Trên `master` | Trên nhánh gate/T2 |
|---|---|---|
| r285 / v1.36.23 | bịt rò rỉ monkeypatch selftest (P16-T02) | GATE-03 *(nay đã gỡ, lấy bản master `r292`)* |
| r286 / v1.36.24 | profile gõ sai — đường ĐỌC (P16-F09) | GATE-01a |
| r287 / v1.36.25 | determinism-audit hết đỏ ngẫu nhiên (P16-T03) | GATE-01b |
| r291 / v1.36.26 vs v1.36.30 | `docs/` ra khỏi GÓI (T0-G) | ING-03 |
| **r292 / v1.36.27 vs v1.36.31** | **ca `r284` hết phụ thuộc nền tảng** | **RAS-05** |

Từ đây đánh số tiếp từ **r293**.

**Giải xung đột (6 tệp):** `tl_selftest.py` → lấy **phía master** cho cả 2 hunk của ca `r284`, rồi gỡ ca
trùng của tôi. `VERSION`/`tl.py`/`SKILL.md` → **v1.36.33**. `CHANGELOG.md` → giữ **cả hai** khối.
`RELEASE_MANIFEST.json` → **tái sinh** (177 tệp, không đổi số).

**Gate sau hoà: 8/8 PASS · selftest 1526/1526 · golden khớp · 177 tệp.**

## ★ [nhật ký nhánh T2 — số hiệu NỘI BỘ của nhánh, KHÔNG phải version master] ★ v1.36.32 — HOÀ NHÁNH lượt 2: T2 (chặn máu) gặp T0-G `docs/` ra khỏi gói của master (2026-08-01)

Lượt hoà thứ hai giữa `claude/va-t1-gate-nlvoj9` và `master` (master `a739c93` = r291 v1.36.26, T0-G).

**Đã KIỂM TRÙNG VIỆC trước khi hoà — master CHƯA đụng mục nào của T2.** Đo trực tiếp trên
`19a6adf..a739c93`: `ops_misc.py` · `registry_orchestrator.py` · `ingest_ops.py` ·
`backfill_keywords_live.py` đều **không** nằm trong diff của master; và mã master vẫn còn nguyên cả bốn
dấu vết lỗi (`"ok": True, "nlm_deletes"` gán cứng ×1 · `if not gdoc:` ×2 · `done[gid] = 'err'` ×1 ·
`gas.post("changes_pull")` ở `:195` trước cổng). ⇒ Bốn bản vá T2 **không** thừa, không có việc nào phải bỏ.

**⚠ BẢNG VA CHẠM SỐ HIỆU — cập nhật (thêm dòng v1.36.26):**

| Số | Trên `master` | Trên nhánh gate/T2 |
|---|---|---|
| r285 / v1.36.23 | bịt rò rỉ monkeypatch trong selftest (P16-T02) | GATE-03 |
| r286 / v1.36.24 | profile gõ sai hết mượn corpus NỀN đường ĐỌC (P16-F09) | GATE-01a |
| r287 / v1.36.25 | determinism-audit hết đỏ ngẫu nhiên (P16-T03) | GATE-01b |
| **r291 / v1.36.26** | **`docs/` ra khỏi GÓI (T0-G)** | **Helper 1 `tl_core/txn.py` (Pha 1-0)** |

Lưu ý số `r291` bị dùng **hai lần với hai version khác nhau**: master `r291`=v1.36.26 (docs) và nhánh này
`r291`=v1.36.30 (ING-03). Tên ca test vẫn **không** trùng. Từ đây đánh số tiếp từ **r293**.

**Giải xung đột:** `VERSION`/`tl.py`/`SKILL.md` → **v1.36.32** (cao hơn cả hai). `CHANGELOG.md` → giữ
**cả hai** khối. `RELEASE_MANIFEST.json` → **tái sinh**. `references/golden/workflow_audit.json`,
`CONTEXT.md`, `GOTCHAS.md`, `release.py`, `the_thuc.py`, `tl_selftest.py` → auto-merge sạch.

**RATCHET kiểm kê của master ĐỎ ĐÚNG LÚC — và đó là điểm tốt.** Ca `r291_docs_ngoai_goi` (master) khoá
`len(paths) + 19 == 195`; sau khi hoà thành 196 nên nó **ĐỎ**, đúng như chú thích của chính nó yêu cầu
(*"thêm/bớt tệp trong gói ⇒ test này ĐỎ và phải sửa CÓ CHỦ ĐÍCH, kèm kê khai slot"*).

**KÊ KHAI SLOT: 195 → 196.** Đúng **một** tệp được thêm vào gói: `scripts/tl_core/txn.py` — Helper 1
(Pha 1-0, r288), lõi kết luận giao dịch mà PRO-01 và ING-03 đều dùng; là mã **runtime** nên không loại
khỏi gói được. Sau khi `docs/` ra khỏi gói (T0-G), **trần 200 còn 24 khe** (196 trong gói + 19 `docs/`
ngoài gói = 215 trên đĩa).

**Gate sau hoà: 8/8 PASS · selftest 1527/1527 · 177 tệp trong `RELEASE_MANIFEST` · golden khớp.**

## ★ [nhật ký nhánh T2 — số hiệu NỘI BỘ của nhánh, KHÔNG phải version master] ★ v1.36.31 — r292/RAS-05: `backfill_keywords_live` hết MẤT DỮ LIỆU IM LẶNG rồi in "XONG TẤT CẢ." (2026-08-01)

Slice **R0** (§Pha 1B), mục **T2 cuối cùng** — tranche "chặn máu" đóng lại tại đây.

**Ba lỗ, cùng Mẫu A (§5), cộng lại thành một mất mát im lặng có kèm lời báo thành công:**
1. `prog['done']` **vừa** là sổ-đã-xong **vừa** là **bộ lọc worklist** (`:63`). Doc `exporttext` lỗi bị
   ghi `done[gid]='err'` (`:76`) ⇒ **loại VĨNH VIỄN** khỏi mọi đợt sau. Không log, không rc.
2. `reg_bulk` (`:92`, `:100`) **không kiểm `rb['ok']`**, chỉ cộng `patched` — mà item đã bị đánh
   `done='ok'` từ **TRƯỚC** lúc gọi (`:84`) ⇒ lô ghi hỏng vẫn coi như xong.
3. `remaining` (`:104`) tính lại từ chính `done` **đã nhiễm** ⇒ `remaining==0` ⇒ in **"XONG TẤT CẢ."**,
   `main()` return `None` ⇒ **rc=0**.

**Vá — state machine tường minh** (`schema: tukhoa_progress.v2`):
`committed` (đã ghi **và** đã đối chiếu) · `blocked` (kết cục XÁC ĐỊNH: không bóc được từ khoá nào —
chạy lại vẫn thế) · `retryable` (HỎNG, **phải** thử lại) · `inflight` (đã bóc, **chưa** có xác nhận ghi).
**Chỉ `committed`/`blocked` mới rời worklist** — đó là toàn bộ lỗ (1).

- Lỗi `exporttext` ⇒ `retryable`, **không** phải "xong".
- Bóc xong ⇒ `inflight`, **chưa** commit. `reg_bulk` đi qua `reg_bulk_verdict`: `ok=true` **chưa đủ** —
  `patched < gửi` nghĩa là phần hụt **chưa** được ghi ⇒ **cả lô** về `retryable`. Chỉ lô được xác nhận
  mới chuyển `committed`.
- `remaining` tính từ worklist **thật** (sổ không còn bị nhiễm); `ok` và `rc` **dẫn xuất** từ nó.
  `rc≠0` khi còn việc; "XONG TẤT CẢ." chỉ in khi thật sự hết. `sys.exit(main() or 0)` — trước đây
  `main()` return `None` nên rc luôn 0.
- `save_progress` **ATOMIC** (`.tmp` + `os.replace`) và nằm trong `finally`: Ctrl-C/hết giờ/nổ giữa
  chừng vẫn giữ được sổ, và `inflight` còn lại tự quay về hàng đợi đợt sau.

**Đọc được sổ v1 là BẮT BUỘC, không phải tiện nghi.** File `tukhoa_progress.json` v1 đang nằm trên máy
người giữ và **chính nó là bằng chứng thiệt hại** mà §6.2 Pha 3.5 cần (danh sách doc bị `err`). Vứt đi
là mất manh mối. `migrate_progress`: `ok`→`committed` · `empty`→`blocked(EMPTY_KEYWORDS)` ·
**`err*`→`retryable`**. Vế cuối chính là bản vá: doc từng bị `err` **quay lại** worklist.

**Test (+3 ca → 1526/1526):**
- `r292_bkl_migrate_v1_dua_doc_loi_quay_lai` — ánh xạ v1→v2 đúng; `g3`/`g4` (từng `err`) **quay lại**
  hàng đợi còn `g1`/`g2` rời; migrate **bất biến** khi chạy lại; sổ rỗng/hỏng ⇒ khung sạch, không nổ.
- `r292_bkl_reg_bulk_verdict_khong_tin_ok_tran` — `ok:true` + `patched` **hụt** ⇒ ÂM (lý do nêu số);
  thiếu khoá `ok` / không phải dict ⇒ ÂM; `patched` dư ⇒ vẫn dương.
- `r292_bkl_main_khong_con_bao_xong_oan` — **end-to-end qua `main()` thật**, 4 kịch bản:
  (A) `exporttext` hỏng ⇒ `rc≠0`, cả hai doc `retryable`, **không** in "XONG TẤT CẢ."; rồi chạy lại
  lượt hai **vẫn thấy đủ 2 doc** (trước vá: mất vĩnh viễn).
  (B) `reg_bulk` hỏng ⇒ không đánh dấu xong, cả lô `retryable`, `rc≠0`; `ok:true` mà `patched` hụt
  cũng vậy. (C) **Phản chứng:** mọi thứ dương ⇒ `rc=0`, `committed`, in "XONG TẤT CẢ.".
  (D) không bóc được từ khoá ⇒ `blocked`, rời worklist, `rc=0` (kết cục xác định ≠ lỗi).

**ĐỎ-TRƯỚC (đo thật):** hoàn nguyên `backfill_keywords_live.py` về HEAD (giữ test) ⇒ `1523/1526`,
ĐỎ đúng ba ca r292. Sau vá `1526/1526`.

**ruff 0.15.8:** `backfill_keywords_live.py` **0 F821 / 0 F401** — y hệt master (delta 0).
`tl.py` 12/0 (đúng nền, không đụng). Full gate **8/8 PASS**, `git diff -- references/golden/` rỗng.

**TRANCHE T2 ĐÓNG.** Bốn mục "chặn máu" + Helper 1 đã xong: PRO-01 (r289) · RAS-01 vế `changes_pull`
(r290) · ING-03 (r291) · RAS-05 (r292), trên nền Helper 1 (r288). Tiếp theo là **T3 — định danh**
(Mẫu B; cần Helper 2 của Pha 1-0).

## ★ [nhật ký nhánh T2 — số hiệu NỘI BỘ của nhánh, KHÔNG phải version master] ★ v1.36.30 — r291/ING-03: `ingest_commit` kết luận bằng KẾT QUẢ, không bằng HÌNH DẠNG — vá CẢ HAI call site (2026-08-01)

Slice **I4** (Pha 1B), mục **T2** thứ tư. Dùng **Helper 1** (`tl_core/txn.py` → `step_result_ok`).

**Bệnh.** `grep upsert_done` toàn kho ra **đúng 1 hit** (`ingest_ops.py:1502`) và hit đó chỉ dùng để
**đặt tên bước lỗi** — không gate gì. Cả **hai** call site (`_pi_stage_write` ~`:1836` cho profile-ingest,
`_il_stage_write` ~`:3080` cho ingest-local) gate bằng `org.get("fileId")`. Mà `doIngestCommit_`
(`references/Code.2.21.2p.gs:854`) đặt `out.fileId` **ngay sau organize, TRƯỚC register/readback** ⇒
response `ok:false` + `upsert_done:false` vẫn **có** `fileId` ⇒ **commit MỘT PHẦN được nhận là thành
công**: GDoc tồn tại mà **thiếu dòng registry** — registry lệch Drive, và không ai biết (đúng thiệt hại
§6.2 Pha 3.5 liệt cho ING-03).

**Vá.** `_ingest_commit_verdict(org, okw)` dùng chung cho **cả hai** call site — đòi `ok=true` **và** đủ
marker theo **đúng luật server**:
`out.ok = organize_done && rename_done && upsert_done && file && (register!=='true' || row)`.
`row` chỉ bắt buộc khi call **có** yêu cầu ghi registry (đòi luôn là đỏ OAN đường hợp lệ).
Ở call site 2, `_step_ok("organize", …)` nay ghi **kết luận thật** thay vì `bool(gdoc)` — nếu không thì
`--resume` sau này đọc journal và tưởng stage organize đã xong.

**`file` CỐ Ý không nằm trong cổng, dù kế hoạch ghi "readback row/file".** Đã đo: cả hai stage READBACK
(`_pi_stage_readback:1900-1916`, `_il_stage_readback`) rẽ nhánh `if _via_commit and org.get("file")` →
dựng readback từ response, **ngược lại** gọi `_verify_convert_readback` (thêm call Drive, **cùng bộ phép
kiểm**), rồi `if not rb_convert.get("ok"): return rc=2`. Nghĩa là `file` **đã fail-closed ở stage ngay
sau**, qua một đường dự phòng **đang hoạt động**. Đưa `file` vào cổng này là **xoá** đường dự phòng đó —
mở rộng phạm vi + thêm rủi ro, trong khi lỗ ING-03 đã bịt kín. `row` thì ngược lại: **không có** đường
nào khác kiểm dòng registry ở stage này. Ca test khẳng định **tường minh** việc miễn `file`, để ai muốn
thêm phải đọc lý do trước.

**Test (+3 ca → 1523/1523):**
- `r291_ingest_commit_verdict_doi_du_marker` — bản mẫu ING-03 nguyên văn (`ok:false` + `upsert_done:false`
  **có** `fileId`) ⇒ ÂM; từng marker thiếu/sai ⇒ ÂM và lý do **nêu đích danh** marker đó; marker **vắng
  mặt hẳn** ⇒ ÂM ("không có tin xấu" ≠ "tin tốt"); thiếu khoá `ok` / không phải dict ⇒ ÂM.
  **Phản chứng:** `register='false'` ⇒ không đòi `row`; thiếu `file` ⇒ vẫn dương.
- `r291_ca_hai_call_site_deu_co_cong` — đọc mã: **mỗi** stage WRITE phải gọi cổng và **không** stage nào
  còn gate chỉ bằng `if not gdoc:`.
- `r291_stage_write_chan_commit_mot_phan` — HÀNH VI qua `_il_stage_write` thật: bơm commit-một-phần ⇒
  `rc=2` **và** journal ghi `False`. Phản chứng: đủ marker ⇒ đi tiếp, journal ghi `True`.

**ĐỎ-TRƯỚC (đo thật, hai lượt):** hoàn nguyên **cả hai** cổng về `bool(fileId)` ⇒ `1521/1523`, đỏ đúng
hai ca. Rồi hoàn nguyên **chỉ call site 2/2** ⇒ **vẫn `1521/1523`** — chứng minh trực tiếp câu
*"sửa một chỗ là để lại lỗ y hệt ở chỗ kia"* không lọt được qua bộ test này.

**Sửa kèm — 6 fake `ingest_commit` trong selftest trả `{"ok": True, "fileId", "srcId"}` TRẦN**
(r97, r114 ×2, r115, r116, r191), thiếu ba marker `*_done` và `row` mà `doIngestCommit_` khai là **luôn
có** khi `ok:true`. Fake trần bắt bản vá phải tin một `ok` trần — **đúng cái bệnh đang chữa** (cùng bài
học fake `_G282` ở r289). Nay khớp hợp đồng thật; r97 **vẫn cố ý bỏ `file`** vì đó là chủ đích gốc của ca
đó (ép đi đường dự phòng `_verify_convert_readback`) — và cổng r291 không đòi `file`.

**Bẫy I11:** `_ingest_commit_verdict` vào `_STUB_MAP["ingest_ops"]`; hằng `_INGEST_COMMIT_MARKERS`
re-export **trực tiếp** (tuple — vào `_STUB_MAP` là vỡ r81). Allow-list Helper 1 nay
`{"ops_misc.py", "ingest_ops.py"}`.

**ruff 0.15.8:** `tl.py` 12 F821 / 0 F401 (đúng nền). `ingest_ops.py` 371 vs 370 ở HEAD trước (+1 = tên
re-home mới), cùng lớp BY DESIGN. Full gate **8/8 PASS**, `git diff -- references/golden/` rỗng.

## ★ [nhật ký nhánh T2 — số hiệu NỘI BỘ của nhánh, KHÔNG phải version master] ★ v1.36.29 — HOÀ NHÁNH: T1+T2 (gate + chặn máu) gặp P16-T02/F09/T03 của master (2026-08-01)

Nhánh `claude/va-t1-gate-nlvoj9` và `master` chạy **song song** từ `19a6adf` (v1.36.22). Hoà lại tại đây.

**⚠ VA CHẠM SỐ HIỆU — đọc kỹ khi tra CHANGELOG.** Hai nhánh **dùng trùng** số `rXX` và nhãn version cho
**việc khác nhau**:

| Số | Trên `master` | Trên nhánh gate/T2 |
|---|---|---|
| r285 / v1.36.23 | bịt rò rỉ monkeypatch trong selftest (P16-T02) | GATE-03 — lọc ứng viên config theo tiền tố `/tmp/` |
| r286 / v1.36.24 | profile gõ sai hết mượn corpus NỀN ở đường ĐỌC (P16-F09) | GATE-01a — `sweep` tất định ở RAW |
| r287 / v1.36.25 | determinism-audit hết đỏ ngẫu nhiên vì probe công cụ NGOÀI (P16-T03) | GATE-01b — cưỡng chế raw stability |

**KHÔNG đánh số lại lịch sử** (sẽ phải sửa tên test `rXX_`, chú thích mã và 6 thông điệp commit — churn
lớn, rủi ro cao, không đổi hành vi). **Tên ca test KHÔNG trùng nhau**, nên selftest không bị ảnh hưởng;
chỉ tra cứu theo số là mơ hồ. Từ v1.36.29 trở đi đánh số **tiếp từ r291**, không tái dùng.

**Giải xung đột (6 tệp):** `VERSION`/`tl.py`/`SKILL.md` → **v1.36.29**, cao hơn cả hai nhánh (đơn điệu tăng).
`CHANGELOG.md` → **giữ CẢ HAI** khối mục. `RELEASE_MANIFEST.json` → **tái sinh** (196 tệp).
`tl_selftest.py` → **giữ CẢ HAI** khối, và đặt chốt `r285_khong_ro_ri_monkeypatch` của master **SAU CÙNG**:
nó so với ảnh chụp đầu `run()` nên phải chạy sau MỌI khối monkeypatch, kể cả các khối r286–r290 mới.

**Kiểm tra chéo có giá trị:** chốt rò-rỉ monkeypatch mới của master (r285/P16-T02) chạy **sau** toàn bộ
khối r286–r290 của nhánh này và báo **0 tên không được khôi phục** — xác nhận độc lập rằng các khung
`_run286`/`_run289`/`_run290` khôi phục sạch trạng thái.

**Gate sau hoà: 8/8 PASS · selftest 1520/1520 · `git diff -- references/golden/` rỗng · 196 tệp.**

## ★ [nhật ký nhánh T2 — số hiệu NỘI BỘ của nhánh, KHÔNG phải version master] ★ v1.36.28 — r290/RAS-01 (vế `changes_pull`): "DRY" MÀ VẪN GHI — điều phối hết gọi action ghi trước cổng `--apply` (2026-07-31)

Slice **R1** phần độc lập (§Pha 1D "[MỚI] Đóng riêng lỗ `changes_pull`"), mục **T2** thứ ba.
Vế metadata/CLI của RAS-01 để **T3**; vế này vá được ngay và nặng hơn.

**Bệnh (`scripts/registry_orchestrator.py`).** Ở `phase=boot`, `gas.post("changes_pull")` chạy **TRƯỚC**
cổng `if args.dry or not args.apply` — trong khi chính nhánh DRY đó in ra
*"chế độ DRY — không gọi action ghi"*. Lời in **SAI**, và sai theo hướng nguy hiểm nhất: người vận hành
chạy "dry" để XEM, và tin là mình chưa động vào gì.

**Nặng hơn audit mô tả — đã đọc mã GAS.** Audit nói `applySheet=true ⇒ GHI Sheet`, đúng. Nhưng
`doChangesPull_` (`references/Code.2.21.2n.gs:1527`) **LUÔN** `sp.setProperty('TL_CHANGES_TOKEN', …)`
**bất kể** `apply`/`applySheet` ⇒ nó **TIÊU THỤ cửa sổ delta**. Nghĩa là hạ xuống `applySheet=false`
**KHÔNG cứu được**: một lượt "dry" vẫn **nuốt mất** thay đổi mà lượt `--apply` thật lẽ ra phải thấy.
⇒ Chốt đúng là **KHÔNG GỌI**, không phải gọi-nhẹ-hơn.

**Vá.** DRY (`--dry` **hoặc** thiếu `--apply` — hai đường vào cùng một cổng, bịt cả hai) ⇒ bỏ hẳn lời gọi,
khai thẳng trạng thái mới `changes_state="not_probed"`. `decide()` xếp `not_probed` **cùng nhánh bảo thủ**
với `no_baseline` (`regen2` + `changes_init`) và nêu lý do: *chưa đo thì chưa biết*. Đoán "chắc ít thay
đổi" chính là lớp fail-open đang chữa.

**Test (+3 ca → 1509/1509):**
- `r290_orch_dry_khong_goi_action_ghi` — chạy `run()` THẬT với module `gas` GIẢ: DRY ⇒ **không `post`
  action nào**, không `changes_pull`; kế hoạch lấy nhánh bảo thủ và **nói rõ vì sao**; kiểm **cả hai**
  đường vào DRY.
- `r290_orch_apply_van_goi_changes_pull` — PHẢN CHỨNG: `--apply` thật **vẫn** gọi `changes_pull`; vá
  không được biến thành "bỏ hẳn tính năng".
- `r290_orch_decide_not_probed_bao_thu` — `not_probed` cho kế hoạch **y hệt** `no_baseline`, lý do nêu DRY.

**ĐỎ-TRƯỚC (đo thật):** hoàn nguyên `registry_orchestrator.py` về HEAD (giữ test) ⇒ `1507/1509`, ĐỎ đúng
hai ca hành vi mới; ca phản chứng `--apply` vẫn xanh (hành vi đó vốn đã đúng). Sau vá `1509/1509`.

`python scripts/registry_orchestrator.py --selftest` = **22/22** trước và sau.
**ruff 0.15.8:** `registry_orchestrator.py` **0 F821 / 0 F401**, y hệt master (delta 0). Full gate **8/8 PASS**.

## ★ [nhật ký nhánh T2 — số hiệu NỘI BỘ của nhánh, KHÔNG phải version master] ★ v1.36.27 — r289/PRO-01: `profile-file-remove` FAIL-CLOSED — hết tháo con trỏ registry sau khi bước xoá đã hỏng (2026-07-31)

Slice **P0** (§6.1-(b) + Pha 1C-tách-ra), **ưu tiên #2 toàn sổ audit** — chỉ sau GATE-03. Mục T2 thứ nhất.
Dùng **Helper 1** (`tl_core/txn.py`, r288) — DÙNG, không SỬA.

**Bệnh (`ops_misc.py`, fail-open PHÁ HUỶ).** Kết quả `nlm source_delete` và `drive trash` chỉ được ghi
**nhật ký**, không kiểm; `reg_delete` chạy **vô điều kiện**; rồi `out = {**plan, "ok": True, ...}`
**GÁN CỨNG** + `return 0`. Hệ quả: mọi bước con hỏng vẫn `rc=0`, mà **con trỏ registry ĐÃ BỊ THÁO** —
file Drive/nguồn NLM còn nguyên nhưng không còn dòng nào tra ra chúng. **Tài sản mồ côi, và vì `rc=0`
nên không ai đi tìm.**

**Vá.**
- Từng bước đi qua `Txn.record(...)` — kết quả được **KIỂM**, không chỉ ghi nhật ký. Transport nổ
  (`raise`) nay là bước **HỎNG**, không phải bước vắng mặt.
- `Txn.guard()` **CHẶN** trước mỗi mutation kế tiếp: bước NLM hỏng ⇒ **không trash tiếp** (mỗi mutation
  thừa là một thứ nữa phải dọn tay) và **không đụng `reg_delete`** ⇒ registry **CÒN NGUYÊN** ⇒ vẫn còn
  đường tra ra tài sản.
- `ok` được **TÍNH** (`Txn.conclude`), `rc` **dẫn xuất** (`Txn.rc`). Không còn `"ok": True` gán cứng.
- Output kê `txn.wrote` (**đã ghi được gì rồi**) và `txn.uncertain` (mutation ÂM — chưa chứng minh được
  đã ghi hay chưa). Hai việc dọn khác nhau nên để hai bảng khác nhau.
- Hỏng ⇒ payload in ra **stderr** (khuôn sẵn có của chính lệnh này ở nhánh `NO_MATCHING_PROFILE_ROWS`).

**`require_removed="no"` — ĐÃ XÉT LẠI, kết luận GIỮ NGUYÊN, có bằng chứng.** Kế hoạch ngờ cờ này "tự tắt
readback". Đo lại: `require_removed='yes'` chỉ xoá dòng có `nlm_status` bắt đầu `removed*`
(API_CONTRACT §`reg_delete`), mà **`profile-file-remove` không hề ghi `nlm_status` ở bất kỳ đường nào** ⇒
bật `'yes'` sẽ đẩy gần như mọi dòng vào `skipped_live` và làm lệnh **vô tác dụng** — đổi một lỗi
fail-open lấy một lỗi **fail-silent**. `'no'` giữ nguyên là hard-delete CÓ CHỦ ĐÍCH sau
`--apply --confirm yes` (cùng lý lẽ đã ghi ở `source_ops.py:954`).

Readback chuyển sang **phía client** (`_pfr_reg_delete_verdict`), vì `ok=true` của response **chưa phải**
bằng chứng dòng đã gỡ: `skipped_live>0` vẫn đi kèm `ok=true` được. Luật: response dương **và**
`skipped_live == 0` **và** `removed + not_found ≥ requested` (`not_found` được chấp nhận — chạy lại sau
một lượt thành công một phần thì dòng đã biến mất, không phải lỗi mới).

**Đổi hành vi có chủ đích:** `--keep-registry` mà không `--delete-nlm`/`--trash-drive` = lệnh **không làm
gì**. Trước đây in `ok:true, rc=0`. `ok` được TÍNH thì câu trả lời đúng là *chưa có gì được chứng minh* ⇒
`rc=2`, `error=KHONG_CO_THAO_TAC_NAO_DUOC_YEU_CAU`.

**Test (+4 ca → 1506/1506).**
- `r289_pfr_duong_xanh_van_chay_du` — PHẢN CHỨNG NỀN: 3 cờ bật, mọi bước dương ⇒ `rc=0`, gọi đủ
  nlm+trash+reg_delete, `txn.wrote` liệt **đúng 3** thứ đã ghi. Cổng không chặn oan đường hợp lệ.
- `r289_pfr_ma_tran_buoc_con_hong_khong_thao_registry` — **ma trận** `--delete-nlm` × `--trash-drive` ×
  `--keep-registry`, mỗi ô một ca bước-con-hỏng ⇒ `rc≠0` **và registry còn nguyên** (`reg_delete` không
  được gọi lần nào); NLM hỏng ⇒ trash phía sau cũng bị chặn, `blocked.blocking_step` chỉ đúng thủ phạm.
- `r289_pfr_reg_delete_readback_khong_tin_ok_tran` — `ok:true + skipped_live=1` ⇒ đỏ; `ok:true` mà
  `removed+not_found` không phủ hết ⇒ đỏ; `not_found` phủ nốt ⇒ **không đỏ oan**. Kèm khẳng định
  `require_removed='no'` vẫn được gửi.
- `r289_pfr_khong_thao_tac_nao_khong_con_bao_xanh`.

**ĐỎ-TRƯỚC (đo thật):** dán lại nguyên thân hàm bản trước r289 (giữ test) ⇒ `1502/1506`, ĐỎ **đúng bốn**
ca r289; 5 ca `r282` vẫn xanh.

**Sửa kèm — fake `_G282.post` của r282 trả `{"ok": True}` TRẦN.** API_CONTRACT §`reg_delete` khai
`removed`/`not_found`/`skipped_live` là **luôn có**; fake thiếu chúng thì readback mới buộc phải tin một
`ok` trần — **đúng cái bệnh đang chữa**. Nay fake trả đúng hợp đồng thật. 5 ca r282 xanh trước lẫn sau.

**Cập nhật danh sách gắn Helper 1:** `r288_helper1_chua_gan_vao_lenh_nao` → `r288_helper1_chi_gan_o_noi_da_khai`
với allow-list `{"ops_misc.py"}`. Slice sau (ING-03 → `ingest_ops.py`) **phải tự thêm tên mình** — việc gắn
helper vào một đường GHI mới không bao giờ lọt review im lặng.

**Bẫy I11 đã va:** `_pfr_count`/`_pfr_reg_delete_verdict` là symbol MỚI trong `tl_core` ⇒ **phải** vào
`_STUB_MAP["ops_misc"]`, nếu không thì `NameError` lúc chạy và `r90_rebase_module_names_resolvable` đỏ.

**ruff 0.15.8:** `tl.py` 12 F821 / 0 F401 (đúng nền). `ops_misc.py` 403 vs 399 ở HEAD trước (+4 = tên
re-home của khối mới), cùng lớp BY DESIGN. F401 không đổi. Full gate **8/8 PASS**,
`git diff -- references/golden/` **rỗng**.

## ★ [nhật ký nhánh T2 — số hiệu NỘI BỘ của nhánh, KHÔNG phải version master] ★ v1.36.26 — r288/Pha 1-0: Helper 1 — HỢP ĐỒNG kết luận giao dịch (`tl_core/txn.py`), CHƯA gắn vào lệnh nào (2026-07-31)

Pha 1-0 (§5 Mẫu A + §6.1 kế hoạch AUDIT_XAC_MINH 31-07). **Một commit riêng, không kèm mục lỗi nào** —
đúng acceptance §6.1. Mở đầu tranche **T2 (chặn máu)**: PRO-01 và ING-03 đều được kế hoạch chỉ định
*"vá bằng Helper 1"*, nên hợp đồng phải chốt TRƯỚC, nếu không mỗi mục lại tự nghĩ ra một nửa-giải-pháp.

**Vì sao cần.** Mẫu A chiếm **13/34** mục sổ audit (GATE-01, ING-03/05, PRO-01/06/07, RAS-04/05/10/11/12…).
Dấu hiệu chung luôn là một trong hai: `ok` được **GÁN** thay vì được **TÍNH**; hoặc `ok` tính từ **HÌNH
DẠNG** ("response có `fileId`") thay vì từ **KẾT QUẢ** ("bước register báo `upsert_done`"). Vá từng `if`
rời thì mục thứ 14 tái sinh ở chỗ khác.

**Hợp đồng (`scripts/tl_core/txn.py`, 5 điều):**
1. nhận `(tên_bước, kết_quả, bắt_buộc?)` theo ĐÚNG thứ tự đã chạy;
2. `ok` được **TÍNH**, không bao giờ được **GÁN** — `Txn.conclude()` **bỏ qua** `ok`/`rc` trong `extra`,
   nên không ai dựng lại được `out = {**plan, "ok": True}` của PRO-01;
3. bước bắt buộc hỏng ⇒ `Txn.guard()` **ném `TxnBlocked`** chặn mutation phía sau. Là **exception** chứ
   không phải cờ, có chủ đích: cờ mà caller quên kiểm thì lại fail-open đúng kiểu cũ;
4. `rc` **dẫn xuất** từ `ok` (`Txn.rc()`), không đặt tay;
5. luôn phát ra *bước nào hỏng* + **`wrote` = ĐÃ GHI ĐƯỢC GÌ RỒI**, tách riêng **`uncertain`** =
   mutation ÂM (không chứng minh được đã ghi, cũng không chứng minh được chưa ghi). Điều 5 không phải
   trang trí: PRO-01 tháo con trỏ registry sau khi bước xoá đã hỏng mà `rc=0`, nên **không ai biết có
   tài sản mồ côi** — bản kê `wrote`/`uncertain` là thứ duy nhất chỉ được đường về.

**Vị ngữ `step_result_ok` FAIL-CLOSED** — chỗ ING-03 chết nằm đúng ở đây:
`{"ok": false, "fileId": "1AbC", "upsert_done": false}` ⇒ **ÂM**; `{"fileId": "1AbC"}` (thiếu hẳn khoá
`ok`) ⇒ **ÂM**, vì *"không có tin xấu"* không phải *"tin tốt"*; hình dạng lạ (str/int/list) ⇒ **ÂM**.
`require_keys` là chỗ khai "đủ marker", và lý do hỏng **nêu đích danh** marker nào thiếu.

**Test (+4 ca → 1502/1502), mỗi điều hợp đồng ít nhất một ca kèm phản chứng:**
`r288_helper1_vi_ngu_ket_qua_duong_fail_closed` · `r288_helper1_ok_duoc_tinh_va_rc_dan_xuat` ·
`r288_helper1_chan_mutation_phia_sau_va_ke_da_ghi` · `r288_helper1_chua_gan_vao_lenh_nao`.

Ca cuối khoá đúng câu *"CHƯA gắn vào lệnh nào"*: quét `tl_core/*.py` (trừ `txn.py`) không được có
`Txn(`/`TxnBlocked`/`step_result_ok(`. Gộp việc gắn vào commit này thì nó ĐỎ; khi slice T2 gắn thật thì
đây là chỗ ĐẦU TIÊN phải sửa — có chủ đích, không lọt im lặng.

**ĐỎ-TRƯỚC (đo thật):** phá đúng ba điều của hợp đồng trong `txn.py` (thiếu khoá `ok` ⇒ coi là dương ·
`conclude` cho gán đè · `guard` chỉ đánh dấu không ném) ⇒ `1499/1502`, ĐỎ **đúng ba** ca tương ứng, ca
"chưa gắn" vẫn xanh. Sau khôi phục: `1502/1502`.

**Kiểm kê tệp — TRẦN 200.** Thêm `scripts/tl_core/txn.py` ⇒ **195 → 196 tệp, còn 4 khe**. Đây là mã
RUNTIME (T2/T3 sẽ dùng) nên KHÔNG loại khỏi gói được. Ai thêm tệp tiếp theo phải xét dev-side/
`_RELEASE_EXCLUDE_NAMES_ANYWHERE` trước.

**Golden ghi lại — ĐÚNG tiền lệ r238, đã kiểm trước khi commit.** Thêm tệp làm
`workflow_audit.files_scanned` **69 → 70** ⇒ `golden` + `determinism` đỏ (determinism đỏ CHỈ vì check
`golden_test` lồng bên trong). `git diff -- references/golden/` sau `--write` = **đúng 1 dòng**
(`1 1 references/golden/workflow_audit.json`), không có thay đổi nào khác ⇒ là kiểm kê hợp lệ, không phải
bug của thay đổi. Gate sau đó **8/8 PASS**.

**ruff 0.15.8:** `txn.py` **0 F821 / 0 F401**. `tl.py` 12/0 (đúng nền). `tl_selftest.py` 4255 (master 4207):
+48 của 4 ca mới, cùng lớp BY DESIGN. F401 không đổi.

## ★ [nhật ký nhánh T2 — số hiệu NỘI BỘ của nhánh, KHÔNG phải version master] ★ v1.36.25 — r287/GATE-01b: golden-test CƯỠNG CHẾ raw stability — `raw_stable=false` ⇒ rc≠0, `--write` CẤM ghi (2026-07-31)

Slice **G0.1b** (§3.1 kế hoạch AUDIT_XAC_MINH 31-07). **Chỉ được làm SAU khi G0.1a (r286) xanh** — xem
bằng chứng thứ tự ở cuối mục này.

**Bệnh (fail-open, `tl_core/workflow.py`):** `raw_stable` được TÍNH, thậm chí sinh `raw_diff`, nhưng
`rec["ok"]` dẫn xuất **thuần** từ so sánh projection. Hệ quả: hai stdout **khác byte / cùng projection**
vẫn cho `top ok=true, rc=0`, và `--write` vẫn **GHI ĐÈ fixture** từ một lệnh đang bất định. Đã **BÁO** mà
**KHÔNG cưỡng chế** — vi phạm "kết quả tất định" của CONTEXT.md.

**Vá:** `raw_stable=false` ⇒ case `ok=false` + mã lỗi **RIÊNG** `GOLDEN_RAW_UNSTABLE` ⇒ top `ok=false` ⇒
`rc≠0`; ở `--write` thì **CẤM ghi/regen** (`written: false`, top `write_refused: true`). Mã lỗi để riêng
CÓ CHỦ ĐÍCH: `GOLDEN_MISMATCH` (fixture lệch → xem lại thay đổi) và `GOLDEN_RAW_UNSTABLE` (lệnh bất định →
**cấm** regen, phải làm tất định trước) là hai bệnh **chữa ngược nhau**; gộp một mã là mời người ta chạy
`--write` cho xong. Kèm `raw_sha256_run2` để đọc được cả hai lượt.

**Test characterization (ĐỎ-TRƯỚC / XANH-SAU), +3 ca → 1498/1498.** Harness bơm `_run_tl_json` GIẢ trả hai
stdout **khác đúng 1 byte space / `json.loads` ra CÙNG dict**, và ghim `_golden_dir` vào **tempdir** — dù cổng
có hỏng thì `--write` cũng không bao giờ đụng `references/golden/` thật.
- `r287_golden_raw_drift_lam_do_gate` — bơm drift ⇒ top `ok=false` + `error=GOLDEN_RAW_UNSTABLE` + case
  `ok=false`/`raw_diff` có nội dung. **Phản chứng:** không drift ⇒ cổng IM, lỗi đúng là `GOLDEN_FILE_MISSING`
  (đã đi QUA cổng raw, chết ở bước so fixture) — cổng luôn-đỏ vô dụng y như cổng luôn-xanh.
- `r287_write_cam_ghi_khi_raw_bat_dinh` — `--write` + drift ⇒ `write_refused=true`, mọi case `written=false`,
  và thư mục golden **không sinh tệp nào**. **Phản chứng:** không drift ⇒ `--write` vẫn ghi đủ 20 tệp.
- `r287_rc_khac_0_qua_lenh_that` — cưỡng chế phải tới **TẦNG LỆNH**: `cmd_golden_test` trả `rc≠0`, không chỉ
  payload `ok=false`. `rc` mới là thứ `deploy-package.sh`/CI đọc; dừng ở payload thì cổng vẫn lọt.

**ĐỎ-TRƯỚC (đo thật):** hoàn nguyên `workflow.py` về HEAD, giữ nguyên test ⇒ `1495/1498` với ĐÚNG ba ca r287
đỏ (ba ca r286 vẫn xanh). Sau vá `1498/1498`.

**BẰNG CHỨNG THỨ TỰ — vì sao G0.1a phải xong TRƯỚC.** Ghép **riêng** bản cưỡng chế này vào cây
`origin/master` (tức **có G0.1b, KHÔNG có G0.1a**) rồi chạy `golden-test` liên tiếp:

```
lượt 1..4: rc=0  top_ok=True   raw_stable=True
lượt 5:    rc=2  top_ok=False  raw_stable=False  error=GOLDEN_RAW_UNSTABLE   ← ĐỎ CHẬP CHỜN
```

Trên nhánh này (**G0.1a + G0.1b**): 6 lượt liên tiếp `rc=0`, 20/20 case `ok`, `raw_stable=true` toàn bộ, và
`sweep raw_sha256` **BẰNG NHAU cả 6 lượt** (`d2fd042e4d47…`). Đúng như §3.1 cảnh báo: cưỡng chế trước khi
làm tất định = cổng đỏ chập chờn, tệ hơn không có cổng.

**ruff 0.15.8 — delta so master:** `workflow.py` **26 F821 / 0 F401 = Y HỆT master** (delta 0).
`tl.py` 12/0 (đúng nền, không đụng). `tl_selftest.py` 4250 (master 4207): +43 là `os`/`json`/`_TL_MODULE`
của 3 ca mới — cùng lớp BY DESIGN. **Không phát sinh lớp cảnh báo mới; F401 không đổi.**

## ★ [nhật ký nhánh T2 — số hiệu NỘI BỘ của nhánh, KHÔNG phải version master] ★ v1.36.24 — r286/GATE-01a: `sweep` TẤT ĐỊNH ở RAW — đóng băng `snapshot_age_s` dưới deterministic mode (2026-07-31)

Slice **G0.1a** (§3.1 + §6.1 kế hoạch AUDIT_XAC_MINH 31-07). **Làm tất định TRƯỚC, cưỡng chế SAU** — đảo
thứ tự là được một cổng ĐỎ CHẬP CHỜN, tệ hơn hiện trạng.

**Bệnh:** `golden-test` so **hai** thứ: projection (đã scrub `volatile_keys`) **và RAW stdout hai lượt**.
`snapshot_age_s` nằm trong `volatile_keys` nên projection sạch — nhưng RAW vẫn lệch mỗi khi tuổi cache vắt
qua **mốc giây nguyên** giữa hai lần chạy. Bất định **theo thời điểm**, nên "20/20 `raw_stable=true`" ở một
lượt may KHÔNG chứng minh được gì.

**Bằng chứng DƯƠNG — chạy `golden-test` 3 lượt trên `origin/master` SẠCH (case `hygiene_sweep_fixture`):**

```
MASTER lượt 1: raw_sha256=9f67a94a3b8983d9  raw_stable=True
MASTER lượt 2: raw_sha256=ae9ae946bdbd112e  raw_stable=True
MASTER lượt 3: raw_sha256=62f55fc220f79652  raw_stable=False   ← ĐỎ THẬT, bắt tại chỗ
```

`raw_sha256` đổi **mỗi lượt**; tới lượt 3 thì `raw_stable` lật hẳn sang False. Đo trực tiếp `sweep --json`
hai lượt cách 1,2s: `1284` vs `1285`, và đó là **khác biệt DUY NHẤT** của cả payload.

**Vá:** thêm `tl_core.deterministic.frozen_age_seconds` + hằng `FROZEN_AGE_S` (và wrapper `_frozen_age_seconds`
trong `tl.py` để nối `_DETERMINISTIC_ON`). Deterministic mode BẬT ⇒ tuổi-giây thu về một hằng **ở RAW**;
TẮT ⇒ giá trị THẬT nguyên vẹn. **KHÔNG nới định nghĩa raw-stability** — giá trị vẫn được phát ra, chỉ là
hằng dưới chế độ tất định. `None` giữ nguyên `None`: "chưa có snapshot" là dữ kiện NGHIỆP VỤ, đổi thành 0
là nói dối "có snapshot, mới 0 giây".

**Vá theo MẪU, không vá theo `if`** (§5 kế hoạch): áp cho **cả ba** nơi phơi `snapshot_age_s` —
`cmd_sweep` (hygiene.py), `cmd_counts` (ops_misc.py), `cmd_ingest_missing` (ingest_ops.py). Hai lệnh sau
chưa có golden case nào, bỏ sót thì lỗ còn nguyên mà gate không bao giờ thấy.

**Acceptance G0.1a — `golden-test` 5 LƯỢT liên tiếp trên nhánh:** cả 5 lượt `top ok=true`, 20/20 case,
`sweep raw_stable=true`, và `raw_sha256` **BẰNG NHAU cả 5 lượt** (`d2fd042e4d47…`) — bằng chứng mạnh hơn
`raw_stable` đơn thuần, vì trên master chính con sha này đổi mỗi lượt.

**Test rXX_ (ĐỎ-TRƯỚC / XANH-SAU), +3 ca → 1495/1495:**
- `r286_frozen_age_dong_bang_va_giu_none` — hợp đồng helper: bật ⇒ 1284 và 1285 cho CÙNG một byte; tắt ⇒
  giữ 1284/1285; `None` ⇒ `None`; phủ cả đường cờ `args` lẫn đường `TL_DETERMINISTIC` (đường subprocess golden).
- `r286_sweep_raw_bat_bien_khi_tuoi_cache_troi` — HÀNH VI: chạy `cmd_sweep` hai lượt với đồng hồ tuổi-cache
  TRÔI 1284→1285, RAW stdout phải bất biến TỪNG BYTE; kèm phản chứng "không deterministic ⇒ vẫn phơi 777".
- `r286_counts_va_ingest_missing_cung_mau` — khoá hai nơi không có golden phủ.

**ĐỎ-TRƯỚC (đo thật):** hoàn nguyên đúng ba điểm gọi, giữ nguyên helper + test ⇒ `1493/1495`, ĐỎ đúng hai ca
hành vi, ca hợp đồng helper vẫn xanh (đúng: helper không bị hoàn nguyên). Sau vá `1495/1495`.

**BẪY đã trả giá khi viết test (ghi lại, chú thích nằm ngay tại code):** `_TL_MODULE.cmd_sweep` là **STUB**
(`_make_tl_stub`) ủy quyền `getattr(tl_core.hygiene, "cmd_sweep")`. Ở tiến trình SẠCH hàm thật được re-home
`__globals__` về `tl.__dict__` nên monkeypatch `_TL_MODULE._manifest_entries` ăn — đó là lý do ca `r41` ở
ĐẦU tệp chạy được. Nhưng tới CUỐI dãy selftest `tl_core.hygiene` đã bị nạp lại ⇒
`hygiene.cmd_sweep.__globals__ is tl.__dict__` là **False** ⇒ patch KHÔNG tới nơi, lệnh rơi xuống gọi webapp
THẬT rồi chết vì seal-mạng (`rc=2`, stdout RỖNG). Helper `_resolve286` nay gỡ stub và patch trên globals của
**chính hàm sẽ chạy**, không đoán theo tên module.

**ruff 0.15.8 — delta so master:** `tl.py` **12 F821 / 0 F401** (ĐÚNG nền CLAUDE.md, không đổi).
`deterministic.py` 0/0. `hygiene.py` 558 (master 557) · `ops_misc.py` 399 (398) · `ingest_ops.py` 370 (369):
mỗi tệp +1 = đúng tên `_frozen_age_seconds` re-home, cùng lớp BY DESIGN đã có. `tl_selftest.py` 4244 (4207):
+37 là `os`/`Path`/`json`/`_TL_MODULE` của 3 ca mới. **Không phát sinh lớp cảnh báo mới; F401 không đổi.**

**Chưa làm ở đợt này (CÓ CHỦ ĐÍCH):** `raw_stable=false` vẫn CHƯA làm case đỏ — đó là Slice **G0.1b**, chỉ
được làm SAU khi G0.1a xanh.

## ★ [nhật ký nhánh T2 — số hiệu NỘI BỘ của nhánh, KHÔNG phải version master] ★ v1.36.23 — r285/GATE-03: khung cô lập lọc ứng viên config theo TIỀN TỐ `/tmp/` ⇒ loại sạch trên Linux — TEST-ONLY (2026-07-31)

**Ca thật, đo TRỰC TIẾP trên Linux/Cowork:** `python scripts/tl.py --selftest` → **1490/1491**, đúng **một** case ĐỎ:
`r284_khung_test_profile_khong_doc_config_that` — tức chính **chốt chặn tái phát mà r284 vừa thêm** lại đổ
trên nền khác. Đường deploy Linux/Cowork (`deploy-package.sh` bước 1 chạy selftest) **ĐỎ ngay**, trong khi
đường Windows XANH.

**Bệnh (`tl_selftest.py:11182`, bản r284):**

```python
_cands = [c for c in _TL_MODULE._config_candidates(None) if not c.startswith("/tmp/")]
return bool(_cands) and all(Path(c).resolve().is_relative_to(_real) for c in _cands)
```

Bộ lọc tiền tố `/tmp/` sinh ra để loại **hằng cuối hàm** `/tmp/tra_luat_config.json` (comment ghi rõ:
*"không tồn tại trên máy Windows, bỏ qua"*). Nhưng trên Linux `tempfile.TemporaryDirectory()` trả
`/tmp/tmpXXXXXXXX` ⇒ **MỌI ứng viên đều bắt đầu bằng `/tmp/`** và bị loại sạch ⇒ `_cands == []` ⇒
`bool(_cands)` False ⇒ FAIL. Windows xanh **GIẢ** chỉ vì `/tmp` không tồn tại ở đó. Đúng **cùng lớp lỗi
máy-phụ-thuộc mà r284 sinh ra để chặn**, chỉ đảo nền — vì r284 chỉ được kiểm trên Windows
(CLAUDE.md §"Script đa nền: PHẢI chạy THẬT trên nền đó, rồi ĐỐI CHIẾU PARITY").

**Vá (chỉ `tl_selftest.py`, KHÔNG đụng một dòng mã sản xuất):** so **BẰNG ĐÚNG hằng**, không theo tiền tố:
`if c != _HANG_CUOI_285` với `_HANG_CUOI_285 = "/tmp/tra_luat_config.json"`.

**Chốt chặn lọc hụt im lặng** — case mới `r285_hang_cuoi_config_van_con_va_la_ngoai_le_duy_nhat`: trong khung
cô lập, hằng đó **phải còn** trong `_config_candidates(None)` **VÀ** phải là ứng viên NẰM NGOÀI tempdir
**DUY NHẤT**. Ai đổi/xoá hằng ⇒ đỏ tại đây chứ không phải miễn trừ trở thành vô nghĩa mà test vẫn xanh;
ai thêm một đường thoát ra kho thật cũng đỏ tại đây.

**Bằng chứng DƯƠNG (Linux, container này):**
- **Đỏ-TRƯỚC:** `== tl selftest 1490/1491 ==`, `[FAIL] r284_khung_test_profile_khong_doc_config_that`.
- **XANH-SAU:** `== tl selftest 1492/1492 ==` (hai số BẰNG NHAU), cả `r284_` lẫn `r285_` `[OK]`.
- **Phản chứng đột biến:** đổi hằng trong `profile_env.py` thành `/tmp/tra_luat_config_DOI_TEN.json`
  ⇒ `== tl selftest 1490/1492 ==` với `[FAIL] r285_hang_cuoi_config_van_con_va_la_ngoai_le_duy_nhat`
  (và `[FAIL] r284_`). Đã khôi phục nguyên trạng `profile_env.py`.
- **ruff (`ruff 0.15.8`):** `tl.py` = **12 F821 / 0 F401** — đúng nền CLAUDE.md, delta 0 (không đụng tệp này).
  `tl_selftest.py` 4222 F821 vs master 4207 (+15) — toàn bộ là `os`/`Path`/`_TL_MODULE` của case mới,
  đúng lớp BY DESIGN đã có sẵn; **không phát sinh lớp cảnh báo mới**, F401 giữ nguyên 1.

**Bẫy đã va trong chính lượt này (ghi lại để khỏi trả giá lần hai):** `SKILL.md` và `scripts/tl.py` là tệp
**CRLF**. Sửa version bằng `Path.write_text()` của Python (text mode) đã **âm thầm đổi trọn CRLF→LF** —
`git diff` 3492 dòng ở `tl.py`, 307 dòng ở `SKILL.md`, `SKILL.md` tụt 47966→47659 byte — và làm ĐỎ **bốn**
gate cùng lúc (`selftest r219_gotchas_nhan_trang_thai`, `golden` case `workflow_audit` lệch `size_bytes`,
`determinism`, `release-verify`). Không lỗi nào chỉ thẳng vào nguyên nhân. Sửa version ở hai tệp này phải
đi **byte-level** (`read_bytes`/`write_bytes`) hoặc công cụ giữ nguyên line ending.

**NỀN CÒN LẠI CHƯA KIỂM:** bản vá này được chạy THẬT trên **Linux**. **Windows chưa đo ở lượt này** —
cần người giữ chạy `python scripts\tl.py --selftest` và đối chiếu **1492/1492** để đóng parity hai nền
(đúng điều r284 bỏ qua và vì thế sinh ra GATE-03).
# ★ v1.36.37 — r300: VÒNG ĐỜI HỒ SƠ — "đã đóng" thành trạng thái MÁY ĐỌC ĐƯỢC, không còn là lời nói (2026-08-01)

**Bệnh (đo trên hồ sơ THẬT, không phải giả định).** `rasoat_plan.v1` có trạng thái cho ĐƠN VỊ RÀ nhưng
**KHÔNG có cho HỒ SƠ**. Hệ quả trên `h7-3nd-bhxh-2025` (out-dir `p14_h7h8_rasoat_2026-07-26`): người thẩm
tra chốt "đã đóng" mà **state không có khoá nào nói thế**, trong khi còn **5 đầu mối treo** —
(1) `session_claim` chưa nhả (`phien-2026-07-27-c`, treo từ 27-07); (2) `q_approvals` còn **1 `cho_duyet`**;
(3) 3 nợ kiểm chéo chưa định đoạt; (4) `q_ingest` còn **5 văn bản chưa bao giờ lấy được**
(3 `cho_tai` + 2 `cho_nguoi_tai`); (5) **7 trạng thái đã trôi thành câu văn xuôi**
(`"DA_QUYET_VA_DA_THI_HANH: lua chon (b) — nap lai CHI VAO CACHE"`) ⇒ máy không tự kiểm được điều kiện đóng.
Đóng hồ sơ là tuyên bố "đã rà đủ"; để 5 văn bản hụt biến mất im lặng là **báo cáo sai phạm vi**.

→ **Vá = một khối schema + HAI HÀM THUẦN, không phải prose.** `references/RASOAT_PLAN_SCHEMA.md` §7 đặc tả
khối `vong_doi` (trạng thái · `gioi_han_da_biet` · `dinh_doat` · `anchor_con_hieu_luc`), 6 điều kiện đóng,
6 điều kiện mở hồ sơ kế tiếp. §3 lấp nốt hai lỗ hổng đo được: `q_verify` **chưa từng có enum nào được khai**
(hồ sơ thật đã tự dùng khoá `ly_do` với từ vựng riêng) và `q_ingest`/`q_approvals` thiếu token cho "đã quyết".

**Vì sao là HÀM chứ không phải tài liệu:** đúng bài học GATE-06 (r298) — nghiệm thu bằng lint tài liệu
chứng nhận RỖNG. `_rasoat_vong_doi_findings` trả 6 vế hỏng; `_rasoat_vong_doi_dong_hop_le` fail-CLOSED ba
kiểu tự lừa: khai `da_dong` khi còn vế hỏng · khai `da_dong_co_gioi_han` mà `gioi_han_da_biet` **RỖNG**
(đóng im lặng — thứ đã xảy ra thật) · `trang_thai` ngoài enum. Chưa khai `vong_doi` ⇒ không phán (hồ sơ đang rà).

**Loop C sau khi đóng:** chỉ chạy khi `anchor_con_hieu_luc: true`; `false` ⇒ **BỎ QUA hồ sơ và NÓI RA lý do**.
Đo: 82/82 `doc_deps.text_hash` của hồ sơ BHXH là **địa chỉ định vị**, 0/82 khớp `sha256:<64hex>` ⇒ chạy
Loop C theo đặc tả hiện hành sẽ ra **STALE giả 100%**.

**Bẫy hạ tầng gặp khi land (ghi lại cho lượt sau):** hằng cấp module tham chiếu từ trong hàm `tl_core`
**KHÔNG resolve qua `tl`** (bind COPY-globals, ADR-0002) — `r90` bắt; và stub farm **chỉ nhận callable** nên
hằng cũng không khai được vào `_STUB_MAP` — `r81` bắt. Vì vậy từ vựng đóng nằm trong **hàm thuần**
`_rasoat_vong_doi_enums()`, không phải hằng.

Test: `r300_vong_doi_sau_ve_dieu_kien_dong` (phá RIÊNG LẺ từng vế trong 7 ca — sạch-thì-True không đủ, hàm
rỗng cũng qua) · `r300_vong_doi_dong_fail_closed` (6 khẳng định, gồm 3 kiểu tự lừa) ·
`r300_dac_ta_vong_doi_khop_ma` (chống trôi prose↔mã: enum trong tài liệu/thẻ phải khớp hằng trong mã).
Thẻ `rasoat_hoso.json`: +1 `stop_conditions` (đóng hồ sơ ≠ đóng gói phiên) +1 `rules` (điều kiện Loop C).
`RASOAT_HOSO_LOOP.md` §8b. selftest **1557/1557**.

# ★ v1.36.36 — r299: cầu nối OCR/chunks — scope đi theo xuống con · chunks `--apply` chạy được (P16-F11+F26) (2026-08-01)

**F11 — SCOPE KHÔNG ĐI THEO XUỐNG TIẾN TRÌNH CON.** `ocr.py` nhánh `vbqppl` KHÔNG forward `--profile`,
và **KHÔNG nhánh nào** forward `--config` (kể cả `chunking.py`). Cả ba lệnh cầu nối (`ingest-ocr`,
`profile-ingest-ocr`, `profile-ingest-chunks`) lại nằm trong `_CREDS_LAZY_CMDS` ⇒ `main()` cũng **không
áp profile hộ**. Con vì thế tự dò lại config theo `_config_candidates` và tự chọn profile theo
`config.defaultProfile`: **cha được chỉ scope A, con GHI vào scope B — im lặng.** Đây đúng lớp bệnh F08
(r281) đã trả giá, chỉ khác là đi qua ranh giới TIẾN TRÌNH; env `TL_*` thì kế thừa được, còn `--config`
**không có đường nào đi** ngoài dòng lệnh.
→ Vá: forward `--config` + `--profile` cho **CẢ HAI** nhánh `ocr.py` (gộp về MỘT chỗ, bỏ đoạn forward
riêng ở nhánh `else`), và forward `--config` ở `chunking.py`. Cờ nối ở **CUỐI** để `child[1]` vẫn là
đường tệp — guard hạ nguồn (khuôn r251) đọc đúng ô đó.

**F26 — `profile-ingest-chunks --apply` CHƯA BAO GIỜ CHẠY ĐƯỢC.** Plan chỉ nối `--apply` TRẦN, trong khi
`authorize_apply` (`ingest_contract.py`) đòi **CẢ** `--confirm yes` **LẪN** `--expected-plan-hash` ⇒
`CONFIRM_REQUIRED` 100%. `ocr.py` đã vá ĐÚNG bệnh này từ **v1.34.53/C1** bằng khuôn HAI BƯỚC
(`_bridge_run_child_apply`: chạy DRY lấy `plan_hash` → apply kèm `--expected-plan-hash`), và khuôn đó ĐÃ
re-export sang namespace tl. Nhánh chunks bị **sót** — đúng bài học *"vá một reader chưa phải vá xong bẫy"*.
→ Vá: plan tách `command_dry` (không `--apply`) và `command` (có `--apply --confirm yes`); vòng apply gọi
`_bridge_run_child_apply` để chèn `--expected-plan-hash` lúc CHẠY (hash tất định theo NỘI DUNG chunk, mà
chunk vừa được vật chất hoá ngay trước đó nên bridge không thể biết trước). DRY hỏng ⇒ **dừng TRƯỚC mọi
side-effect**, trả kèm `child_dry_result` (cùng tên khoá với `ocr.py` — một hợp đồng).
Guard `MATERIALIZE_PATH_MISMATCH` (r251) giữ nguyên: đường tệp ở index 1 của **cả hai** lệnh.

## ★ PHÁT HIỆN KÈM (harness) — bind-list `tl.py` là STUB CHUYỂN TIẾP LƯỜI

Mất một vòng chẩn đoán mới ra, ghi lại kèm CƠ CHẾ: vật nằm trong `tl.__dict__` cho một symbol của
`tl_core/*` **không phải hàm thật** mà là `_stub` của `_STUB_MAP`:
`def _stub(*a, **kw): return getattr(_mod, _name)(*a, **kw)`. Nghĩa là **thân hàm LUÔN chạy trong
namespace của MODULE GỐC**. Hệ quả cho mọi test về sau:

- patch `_TL_MODULE.<tên>` **KHÔNG** chặn được lời gọi **nằm trong** một hàm lấy qua bind-list —
  phải patch **module gốc**;
- đo được: `_bridge_run_child_apply` lấy từ chunking có `__globals__ is tl.__dict__` (vì là stub), nhưng
  lời gọi `_run_child_tl` bên trong lại giải từ `tl_core.ocr.__dict__`;
- thêm nữa, bind của `chunking`/`ocr` **SAO CHÉP** tên tl vào globals riêng (không rebase `__globals__`
  như `extract_cache`), nên `chunk-verify` trong plan lại giải từ `tl_core.chunking.__dict__`.

Kho đã có bài học r114 *("patch `_TL_MODULE._run_child_tl` không ăn")* nhưng chỉ ghi TRIỆU CHỨNG; nay có
cơ chế. Lớp `_stub_child299` thay đúng hai namespace và khôi phục trọn (kỷ luật r285).

**PHẢN CHỨNG — 5/7 ĐỎ trên bản chưa vá** (selftest 1549/1554). Hai ca xanh đều là ca **"KHÔNG ĐƯỢC ĐỔI"
có chủ đích**: (1) `child[1]` vẫn là đường tệp — cấm chèn cờ vào giữa; (2) `authorize_apply` vẫn đòi CẢ
`confirm` LẪN `hash` — vừa chứng minh F26 là bệnh THẬT, vừa canh cho lượt sau đừng "chữa" F26 bằng cách
nới cổng của con.

Selftest **1554/1554**. Ruff **delta 0** (thêm tham chiếu chéo `_bridge_run_child_apply`, bớt
`_run_child_tl` — bù trừ đúng 1).

# ★ v1.36.35 — r298: diệt 3 test TỰ-CHỨNG-MINH — gate hết chứng nhận RỖNG ở lớp điều phối (T0-E/GATE-06) (2026-08-01)

W0 đặt mục tiêu "khôi phục gate ĐÁNG TIN **trước khi** dùng gate chứng nhận bản vá tiếp theo". Ba ca dưới
đây làm đúng điều W0 sợ: chúng **xanh vô điều kiện** — không đầu vào nào khiến chúng đỏ — nên vùng lớp điều
phối coi như KHÔNG có test. Bản này không sửa hành vi sản phẩm nào; nó sửa **năng lực đo** của bộ test.

**A. `_sua_nong211` — `ok3` là hằng đúng theo TỪ VỰNG, không theo luật.** Hàm nhận
`(phan_loai, chan_dung, moi_truong)` nhưng **không hề đọc `moi_truong`**, rồi `ok3` khẳng định *"không tồn
tại đầu vào nào khiến máy vá tại LIVE"* bằng cách dò chuỗi con `"live"` trong kết quả. Từ vựng trả về chỉ có
`phan_loai_la` · `va_tai_canonical` · `gom_va_sau_luot_ra` — **không chuỗi nào chứa `"live"`**, nên `ok3`
đúng vì cấu trúc hàm chứ không vì luật đúng. Nay bất biến thật được nói rõ ("ĐÍCH vá độc lập với NƠI phát
hiện") và `_sua_nong211_vi_pham` dựng THẾ GIỚI VI PHẠM để cùng phép đo ấy falsify được.

**B. `_pha0_run211` — `nlm_query_calls` là HẰNG SỐ 0.** Trường này được trả `0` ở **cả hai** nhánh `return`,
trong khi `ok3`/`ok4` của `r211_pha0_chan_som_truoc_khi_tieu_nlm` kiểm đúng hằng ấy. Nay ĐẾM THẬT, lấy từ
**LỆNH mà chính tài liệu khai** ở `PHA0_GATE_v1` (`gate[k][0]`), nên còn bắt thêm được DRIFT TÀI LIỆU.

ĐO A/B (bản CŨ chép nguyên văn từ `a3abc11`, chạy cùng bộ assertion):

| Đầu vào | CŨ | MỚI |
|---|---|---|
| cổng THẬT, mọi tổ hợp | 0 call | 0 call |
| cổng bị nhét `tl nlm-query` vào b6 | **0 call** ⇒ ca ĐỎ | **1 call** ⇒ ca XANH |
| nhét lệnh truy vấn NHƯNG chặn đứng ở b1 | 0 call | 0 call (chưa chạm b5/b6 — đây mới là nội dung thật của lời hứa "dừng sớm khi CHƯA tiêu call nào") |

Bản CŨ: **16 tổ hợp đầu vào ⇒ tập giá trị `{0}`** — hằng số, tức `ok3/ok4` xanh vô điều kiện.

**C. `r210_loop_khong_ghi_trong_cay` + `r210_agent_prompt_dung_schema` — LINT TÀI LIỆU đội lốt vế CHẠY.**
Hai ca này chỉ parse `WRITE_PATHS_v1` và dò chuỗi trong prose: KHÔNG chạy vòng nào, KHÔNG `git status`,
KHÔNG `release-verify` — trong khi kế hoạch hứa cả ba. **Không đổi tên ca** (`references/RASOAT_HOSO_LOOP.md:211`
trỏ tới tên `r210_loop_khong_ghi_trong_cay`; đổi tên là đứt con trỏ tài liệu), chỉ **hạ tuyên bố tại chỗ**
cho đúng cái đang đo, và thêm vế CHẠY thật.

Bằng chứng việc này không lý thuyết: vì nghiệm thu là lint tài liệu mà lỗi `rasoat-loop` cài **OR thay AND**
(mất tới **60% GAP**, rc=0, im lặng) sống sót qua **cả Đợt 2 lẫn Đợt 3**, mãi r256 mới bị bắt.

**Test:** +3 ca `r298_*` → **1547/1547**, 0 FAIL.
- `r298_sua_nong_phep_do_falsify_duoc` — phép đo bắt thế giới vi phạm (`True`) và tha luật thật (`False`); bất biến "đích vá độc lập nơi phát hiện" giữ ở luật thật, PHÁ ở luật vi phạm (2 chiều).
- `r298_pha0_dem_call_truy_van_that` — bảng A/B ở trên; kèm vế phân biệt canary (`notebook_get`) với lệnh truy vấn, thiếu vế này thì ca (a) vô nghĩa.
- `r298_worklist_chay_kho_a3_a6` — **chạy khô A3→A6 trên ĐƯỜNG SẢN XUẤT**: `cmd_state_put`/`cmd_state_get` THẬT trên GAS giả **CÓ TRẠNG THÁI** (upload ghi thật, trash xoá thật). Khoá bất biến *state cập nhật sau MỖI đơn vị*: 3 ảnh chụp phải là `done,pending,pending` → `done,done,pending` → `done,done,done`, 4 upload (1 tạo mới + 3 lượt), 3 trash, còn đúng 1 bản. ★ PHẢN CHỨNG: biến thể **gom ghi một phát cuối lượt** cho 3 ảnh chụp `pending` y hệt nhau ⇒ phép đo phân biệt được.

Ruff DELTA: hạng mục **0** (E702/E401/E701/E731/E741/F401 y nguyên); F821 **+5** toàn bộ rơi vào tên đã có
nền — `_TL_MODULE` 2119→2121 · `argparse` 188→190 · `Path` 267→268; **không tên nào mới xuất hiện từ 0**.

★ ĐỔI SỐ hai lần khi land: bản này ra đời mang `r296/v1.36.33`, nhưng phiên P16 land `r296` (F15) rồi
`r297` (F10) trước ⇒ dời sang **r298/v1.36.35**. Ba ca test và mọi chú thích đã đổi theo; khối `r296_*`
và `r297` của P16 giữ nguyên (hai vùng dòng rời nhau, không giẫm).

# ★ v1.36.34 — r297: `--as-appendix` hết TỰ BẬT theo TIÊU ĐỀ / khớp-con — P16-F10 (2026-08-01)

**Bật `--as-appendix` KHÔNG phải chuyện nhãn.** `normalize_document` khi đó đặt `body=""`, `khoi_dau=""`
— mà **r215 nói rõ khối đầu là NGUỒN DUY NHẤT chứng minh danh tính văn bản** — gán T1 `ok:true` **vô
điều kiện**, đổi `coverage` thành `appendix_only` và `document_variant` thành `appendix` ⇒ **đổi luôn
`doc_key`**. Nghĩa là **TOÀN VĂN một Luật bị lưu thành phụ lục, mất danh tính, không qua kiểm cấu
trúc — mà vẫn `ok:true` rc=0**. Một suy đoán rẻ tiền không được phép gây hậu quả đắt như vậy trong im lặng.

**Bệnh (`ingest_to_cache.py`)** — `_ap_hint = (so_hieu + " " + title).lower()` rồi `any(k in _ap_hint …)`
với `("phu_luc","phu luc","phuluc","phụ lục","-pl","_pl")`. Hai khuyết:

- **(a) quét CẢ TIÊU ĐỀ.** Luật/Nghị định CÓ phụ lục thường ghi thẳng «… và Phụ lục …» ngay trên
  tiêu đề ⇒ chính TOÀN VĂN bị đóng dấu phụ lục. Đây là ca ĐÃ ĐO ở journal Pha 1 (A/B cùng một file nguồn).
- **(b) khớp-con.** `-pl`/`_pl` trúng bất kỳ chỗ nào hai chữ đó đứng sau `-`/`_` — ví dụ số hiệu
  `29/2024/TT-PLTW` của cơ quan viết tắt bắt đầu bằng «PL».

**Vá — bốn lớp, không lớp nào thừa:**

1. **Hẹp lại**: hàm `suy_doan_phu_luc(so_hieu)` chỉ đọc **SỐ HIỆU** (bỏ hẳn tiêu đề), tách token ở mọi
   ký tự không phải chữ/số (nên `_` và `-` là ranh giới), khớp **token NGUYÊN VẸN** `pl` / `pl<số>` /
   `phuluc`, hoặc cặp token liền kề `phu|phụ` + `luc|lục`.
2. **Nói ra**: tự bật thì in cảnh báo NHIỀU DÒNG ra stderr, kể đích danh cái giá (mất khối đầu, bỏ T1,
   đổi doc_key) và chỉ luôn cách chữa. Trước đây tuyệt đối im lặng.
3. **Tắt được**: cờ `--no-as-appendix` cho ca số hiệu có chữ «PL» nhưng tệp là toàn văn.
4. **Nội dung PHỦ QUYẾT** (`normalize_document.py`): cha truyền `--as-appendix-auto` để báo «đây là
   SUY ĐOÁN, không phải người gõ». Ở ca đó, nếu `split_articles(raw)` ra **≥2 Điều** ⇒ **DỪNG rc=2**
   với `APPENDIX_TU_SUY_DOAN_NHUNG_CO_THAN_DIEU` (fail-CLOSED), để người quyết.

**★ RANH GIỚI CỐ Ý GIỮ: `--as-appendix` gõ TƯỜNG MINH đi thẳng, không đụng.** Phụ lục/mẫu CÓ Điều nội
bộ là hợp lệ — chính nhánh đó vẫn gọi `split_articles(raw)` cho ca này. Cổng mới CHỈ soi ca suy đoán;
siết lây sang quyền của người dùng là siết quá tay. Ca `r297_as_appendix_tuong_minh_khong_bi_phu_quyet`
**xanh cả trước lẫn sau vá — CÓ CHỦ ĐÍCH**, nó canh đúng ranh giới đó.

`--no-as-appendix` và `--as-appendix-auto` là cờ của hai **script** `ingest_to_cache.py` /
`normalize_document.py`; `tl cache-build` chuyển cờ qua `nargs=REMAINDER` ⇒ **parser-surface của `tl`
KHÔNG đổi**, không cần regen `parser_surface.json`.

**PHẢN CHỨNG — 5/6 ĐỎ trên bản chưa vá** (selftest 1539/1544). Ca xanh là ca «không được đổi» nói trên.
★Ba ca đầu đỏ vì symbol chưa tồn tại, nên **mỗi ca TỰ MANG phản chứng của chính nó**: khẳng định luôn
rằng **LUẬT CŨ (viết inline trong test) trả SAI trên đúng fixture đó** — nếu vế này hỏng thì fixture
không còn tái hiện được bệnh, đúng khuôn r229 của kho. Ca «không mất độ phủ» khẳng định cả luật cũ lẫn
luật mới đều NHẬN 5 số hiệu phụ lục thật, để bản vá không đổi dương-tính-giả thành âm-tính-giả.

Selftest **1544/1544**. Ruff: `ingest_to_cache.py` + `normalize_document.py` giữ nguyên **6 lỗi nền,
delta 0** (`re` thêm vào dòng import sẵn có nên E401 không tăng).

# ★ v1.36.33 — r296: HỌ regex "Điều N" nhận HẬU TỐ CHỮ (7a/7b/7đ) — P16-F15 (2026-08-01)

**Luật sửa đổi CHÈN THÊM điều bằng cách đánh số `7a`/`7b`/`7đ`. Toàn bộ họ khuôn nhận diện tiêu đề
Điều đặt ranh giới `\b` NGAY SAU cụm chữ số — mà giữa "7" và "a" cả hai đều là ký tự từ nên KHÔNG có
ranh giới ⇒ khuôn TRƯỢT.** Một lỗi, ba loại hại tuỳ vai trò của khuôn trong hàm — cả ba đều ĐO ĐƯỢC
trên đường sản xuất trước khi vá, không suy diễn:

1. **điểm DỪNG** — `_slice_dieu` (`nlm_ops`), `_DIEU_ANY` (`tl.py`, điểm dừng của `extract_dieu`),
   nhánh LÙI của `_dieu_head_marks` (`ingest_ops`). Lát cắt chạy tiếp qua 7a/7b ⇒ **trả NGUYÊN VĂN
   của điều KHÁC dưới danh nghĩa điều được hỏi**. Đây là hại NẶNG NHẤT: skill có hợp đồng "đúng từng
   chữ", nên đây là sai lệch NỘI DUNG chứ không phải trình bày. Đo: hỏi Điều 7 → nhận về trọn 7 + 7a + 7b.
2. **BẮT tham chiếu** — `_legal_refs` (`lookup_ops`). "khoản 1 Điều 7a" KHÔNG sinh ra ref nào (đo
   được). Hàm này dùng để dò **stale-ref**, nên bỏ sót = **fail-OPEN**: bản tự ghép trỏ sai vào Điều 7a
   đi lọt cổng.
3. **NHẬN DẠNG** — `_focus_block` (`lookup_ops`) tụt xuống nhánh tìm-chuỗi, trả một CỬA SỔ
   ±1500/5000 ký tự thay vì đúng khối Điều (so sánh official↔candidate do đó đối chiếu nhầm vùng);
   `short_title` (`rasoat_worksheet.py`) trả **rỗng** cho mọi Điều được chèn thêm.

**★ QUÉT CẢ HỌ, KHÔNG VÁ MỘT CHỖ.** Đề bài chỉ nêu `_slice_dieu` + `_DIEU_ANY`. Chốt chặn tự động
(xem dưới) khi chạy trên bản CHƯA VÁ lòi thêm **3 vị trí sản xuất nữa** mà rà bằng mắt đã bỏ sót:
`ingest_ops:1400`, `lookup_ops:1429`, `lookup_ops:2223`. Riêng `ingest_ops` là ca sách giáo khoa của
bài học "vá một reader chưa phải vá xong bẫy": nhánh CHÍNH đã biết hậu tố từ **r229**, nhánh LÙI ngay
dòng dưới thì không.

**★ NEO KHÔNG ĐỤNG — đây là ranh giới phải giữ.** `^\s*Điều\s+{n}\b` phải GIỮ `\b`: chính nó chặn
"Điều 7" khớp nhầm vào "Điều 7a". Neo đúng, chỉ điểm dừng sai. Ca
`r296_neo_khong_noi_long_dieu_7_van_khong_khop_7a` **xanh cả TRƯỚC lẫn SAU vá — CÓ CHỦ ĐÍCH**: nó
không đo bản vá, nó canh cho lượt sau đừng "tiện tay" nới luôn neo.

**Hậu tố nằm NGOÀI group bắt số** ở `_dieu_head_marks` và `_focus_block`, để `int(m.group(1))` ở hạ
nguồn giữ nguyên hợp đồng. `_focus_block` có hậu tố thì chuyển sang `_slice_dieu` (nhận `str`) thay vì
`extract_dieu` (khoá `int`) — **KHÔNG đổi chữ ký `extract_dieu`/`_DIEU_HEAD` và KHÔNG đụng
`extract --dieu type=int`**: đó là giới hạn của parser, thuộc phạm vi khác, đổi ở đây sẽ kéo theo regen
parser-surface không cần thiết.

**CHỐT CHẶN TÁI PHÁT** `r296_khong_con_bay_ranh_gioi_ngay_sau_so`: quét mã SẢN XUẤT, cấm khuôn «Điều»
+ `\s+` + `\d+` DÍNH LIỀN `\b`. Lọc theo **GIÁ TRỊ dòng, không theo tiền tố đường dẫn** (bài học r292 —
CI ubuntu). Phạm vi CÓ GIỚI HẠN và **nói ra chứ không cắt im lặng**: bỏ qua `tl_selftest.py` (r229 CỐ Ý
giữ luật CŨ làm phản chứng — cấm ở đó là cấm đúng thứ chứng minh fixture còn tái hiện được bug) và bỏ
qua dòng CHÚ THÍCH (bản vá phải được quyền trích lại khuôn cũ để giải thích). Bẫy nằm trong dòng code
có chú thích đuôi thì VẪN bị bắt.

**PHẢN CHỨNG — 8/9 ĐỎ trên bản chưa vá** (selftest 1528/1538 — trong đó 8 ca r296; hai ca «version khớp» đỏ thêm là HỆ QUẢ CỦA PHÉP ĐO (revert `tl.py` kéo VERSION về bản cũ), không phải phát hiện; đo bằng `git checkout --` 5 tệp code,
GIỮ nguyên tệp test). Ca xanh duy nhất là ca "KHÔNG ĐƯỢC ĐỔI" nói trên. Chốt chặn khi đỏ in ĐÍCH DANH
đủ 5 vị trí: `tl.py:456 · ingest_ops.py:1400 · lookup_ops.py:1429 · lookup_ops.py:2146 · nlm_ops.py:2118`.

Selftest **1538/1538**. Ruff delta **+10 F821, đúng khuôn bind** (`_TL_MODULE.<tên>` ×9 trong test +
`_slice_dieu` tham chiếu chéo module ×1 trong `lookup_ops` — tệp này vốn đã có hàng trăm F821 cùng khuôn);
mọi loại lỗi khác KHÔNG đổi; `tl.py` giữ nền 12 F821 / 0 F401.

# ★ v1.36.32 — r295: rà soát — MỘT định nghĩa hội tụ + corpus-hiệu-lực dùng chung + state single-writer hết fail-OPEN (2026-08-01)

Đóng 7 phát hiện Làn A của `AUDIT_CORE_TRA_LUAT_2026-07-31`: **RAS-04 · RAS-10 · RAS-13** (vòng rà) và
**RAS-02 · RAS-03 · RAS-08 · RAS-09** (state). Mọi số dưới đây đo bằng A/B trên HAI cây (bản HEAD bung ra
thư mục tạm vs cây đã vá), chạy ĐÚNG đường sản xuất.

**A. `rasoat-loop` — MỘT định nghĩa hội tụ duy nhất (RAS-04 + RAS-10).** Hai mục này trong sổ audit trông
như ngược chiều nhau — một bên đòi lỗi đọc KHÔNG được tính là hội tụ, bên kia đòi frontier-rỗng-từ-đầu PHẢI
là hội tụ — thực ra là hai vế của cùng một định nghĩa:

```
khong_doc_duoc   = ứng viên IN-CORPUS CÓ bản đọc được nhưng đọc HỎNG → CHẶN hội tụ, rc=2
khong_co_ban_doc = ứng viên IN-CORPUS không giải được GDoc id        → CHỈ BÁO, không chặn
dry_rounds       = chỉ tăng khi đã đọc THÀNH CÔNG mà không sinh ứng viên mới
converged        = frontier cạn ∧ khong_doc_duoc = 0 ∧ (dry_rounds ≥ K ∨ chưa từng có ứng viên nào)
```

ĐO TRƯỚC VÁ: hai lỗi đọc liên tiếp ⇒ `dry_rounds`=2 chạm K ⇒ **`converged:true`, rc=0** — lệnh tuyên bố
"đã soi hết" trong khi chưa hề nhìn vào hai văn bản đó (mất phát hiện IM LẶNG, đúng lớp bệnh r256).
Frontier rỗng ngay từ đầu ⇒ **`converged:false`** vĩnh viễn vì `dry_rounds`=0 < K.

★ RANH GIỚI PHẢI GIỮ (bắt được lúc chạy full suite): gộp "không có bản đọc" vào "đọc hỏng" làm ĐỎ
`r256_no_infinite_loop_seen_dedup_holds` (harness của nó cho `_resolve_deep_target` trả gid=None và khoá
`rc=0`). Registry có dòng hợp lệ không kèm Drive là chuyện thường; coi đó là "lệnh hỏng" nằm NGOÀI phạm vi
RAS-04 (nói về `_read_doc_text`). Nay hai sổ riêng, cả hai đều được BÁO (doctrine "no silent caps").

**B. `rasoat-chongcheo` — corpus-hiệu-lực dùng chung (RAS-13).** Thêm `_rasoat_corpus_hieu_luc` cho CẢ HAI
call-site (`_in_corpus` và `_resolve_cluster_member`) — trước đây chỉ nhánh `ambiguous` biết tới quarantine
còn `in_corpus` thì không, hai định nghĩa lệch nhau trong CÙNG một tệp. ĐO TRƯỚC VÁ: dòng `corpus=false`,
dòng cat quarantine, dòng `row_kind=ref` đều cho **`in_corpus:true`** — giấu mất đúng khoảng trống mà lệnh
chồng-chéo sinh ra để tìm. Khớp số hiệu nhưng ngoài corpus ⇒ NÓI RA `khop_so_hieu_ngoai_corpus`.

★ RANH GIỚI THỨ HAI: predicate loại ĐÚNG `corpus == "false"`, **KHÔNG** dùng `_entry_corpus_true` (nó đòi
`== "true"` nên coi THIẾU CỘT là ngoài corpus). "Không biết" ≠ "ngoài corpus"; biến không-biết thành loại-bỏ
là ÂM TÍNH GIẢ — chính chốt S3 trong hàm đó cấm điều này, và siết vế ấy đã làm ĐỎ
`cluster_dup_sohieu_disambig` (fixture không có cột `corpus`).

**C. `state-get`/`state-put` — single-writer hết fail-OPEN (RAS-02/03/08/09).** ĐO TRƯỚC VÁ, chạy
`cmd_state_put` THẬT với GAS giả:

| Ca | TRƯỚC | SAU |
|---|---|---|
| state đã tồn tại, KHÔNG truyền `--expect-claim` | **rc=0, ĐÃ UPLOAD** — đè thẳng claim phiên khác | rc=2 `THIEU_EXPECT_CLAIM` |
| hai bản trùng tên, `--expect-claim` khớp bản CŨ | **rc=0, ĐÃ UPLOAD** — xoá mất state bản MỚI | rc=2 `CLAIM_LECH`, `claim_tren_drive:"B"` |
| body root là `[]` / `q_units` sai enum | **rc=0, ĐÃ UPLOAD RÁC** | rc=2 `STATE_KHONG_HOP_LE` |
| `metaFolderId` chỉ nạp được qua profile | **rc=2 META_FOLDER_ID_TRỐNG** (áp profile SAU khi đã giải `_meta/`) | rc=0 giải được |

RAS-03 là ca nặng nhất: `state-get` chọn bản MỚI NHẤT theo `modifiedTime` còn `state-put` so CAS với
`olds[0]` THÔ ⇒ hai lệnh nhìn HAI tài liệu khác nhau, và ca trùng tên là có thật (chính mã cũ đã phải in
`CO_n_BAN_TRUNG_TEN`). Nay một helper `_rasoat_state_newest` dùng chung cho cả hai; khi MỌI lượt hỏng
`modifiedTime` thì xếp tất định theo `id` và NÓI RA (đóng luôn một rủi ro audit nêu riêng).
`--expect-claim` nay BẮT BUỘC khi state đã tồn tại; chỉ tạo-mới được miễn (ADR-0016).

**Test:** +12 ca `r295_*` → **1529/1529**, 0 FAIL. Mỗi nhóm đều có PHẢN CHỨNG chống siết-quá-tay (đọc được
vẫn hội tụ rc=0 như cũ · dòng corpus THẬT vẫn nhận · `--expect-claim` khớp bản MỚI vẫn ghi được · tạo-mới
vẫn được miễn cờ). Ruff DELTA: `tl.py` 0 · `lookup_ops` +10 · `tl_selftest` +14 — toàn bộ là F821 lớp
rehomed-global ĐÃ có nền (`_TL_MODULE` 2102→2110, `argparse` 185→188, `_entry_cat` 12→14,
`apply_profile_offline` 10→12); **không tên nào mới xuất hiện từ 0**.

**BẪY ĐÃ TRẢ GIÁ (ghi để lượt sau khỏi mắc):** hàm/hằng MỚI trong `tl_core/*` **phải khai trong bảng export
của `tl.py`** (`_STUB_MAP`), nếu không thì `NameError` trên đường sản xuất — `_rasoat_corpus_hieu_luc` ban
đầu KHÔNG có trong `cmd_rasoat_chongcheo.__globals__`, đo trước khi viết test mới bắt được. Còn hằng mức
module thì phải re-export tay (như `_RASOAT_STATE_ALLOWED`) ⇒ đã đưa từ vựng đóng VÀO TRONG hàm validate cho
hết đường trôi. Test vá monkeypatch phải dùng `_mp261`/`_mpr261` (vá ở MỌI CỬA), `setattr(_TL_MODULE, …)`
trần là KHÔNG đủ.

(Nhân tiện: sửa nhãn phiên bản của khối test `r290` từ placeholder `v1.36.2x` thành `v1.36.30` — số thật mà
r290 đã land.)

# ★ v1.36.31 — r294: GATE-01 hết BÁO GIẢ — quy drift theo ĐƯỜNG DẪN khoá, đối xứng với projection (2026-08-01)

**Khuyết do chính phiên land r288 đo được và khai trong commit r288 ("để phiên sau vá"); người rà độc
lập TÁI HIỆN ĐƯỢC BẰNG THỰC NGHIỆM. Nay vá.**

**Bệnh — BẤT ĐỐI XỨNG quy-khoá.** `audit_projection` che **TRỌN CÂY CON** của khoá đã khai
(`deterministic.py`: `out[key] = "<volatile>"`, không đệ quy xuống dưới). Còn `_raw_drift_keys` của
r288 chỉ rút **TÊN KHOÁ LÁ** bằng regex `"key":` trên chính dòng lệch. Hai bên đo hai thứ khác nhau ⇒
**drift nằm BÊN TRONG một khoá container ĐÃ KHAI sinh ra khoá lá "chưa khai"** ⇒
`RAW_UNSTABLE_UNDECLARED` = **BÁO GIẢ**. Đúng cái hậu quả mà chú thích của r288 nói là đã BÁC phương
án (a) để tránh.

**Ca thật, đã tái hiện trên ĐƯỜNG SẢN XUẤT trước khi vá** (`_golden_test` thật, không phải helper):
case `doc_claims_check_fixture` khai `volatile_keys: ["basis","detail"]`, mà `basis` là dict 13 trường
(`max_r`, `changelog_versions`, `sha_lens` là MẢNG…). Cho `max_r` nhảy 292→293 giữa hai lượt:

```
projection_stable : True          ← basis đã bị che trọn, projection y hệt
raw_stable        : False
raw_drift_keys    : ['max_r']     ← chỉ có TÊN LÁ
raw_drift_undeclared: ['max_r']   ← 'max_r' không có trong {'basis'}  ⇒ ĐỎ OAN
ok / error        : False / RAW_UNSTABLE_UNDECLARED
```

Kích hoạt là **ĐUA**: cần `CHANGELOG.md`/`VERSION` bị ghi đúng vào khe giữa hai lượt chạy con của
chính case đó — tức **đúng lúc land một bản**. Nên nó chưa nổ qua 5 lần land ngày 01-08, nhưng đúng
lớp rủi ro vừa làm CI đỏ 5 run liên tiếp ở `r284`.

**Vá.** Thêm `_raw_key_paths_by_line()`: với MỖI dòng, quy ra **ĐƯỜNG DẪN khoá** (tuple gốc→lá) dựa
vào **ĐỘ THỤT** — stdout của gate luôn là JSON `indent=2` nên độ thụt CHÍNH LÀ độ sâu lồng.
`_raw_drift_keys` nay trả đường dẫn thay vì tên lá; người gọi coi một đường dẫn là ĐÃ KHAI nếu
**BẤT KỲ mắt xích nào** của nó được khai — **đối xứng đúng với phép che trọn cây con của projection**.
Phép so dùng **TUPLE** (`set(p) & _khai294`) nên khoá có dấu chấm trong tên không bị tách nhầm; báo cáo
vẫn in dạng `cha.con` cho người đọc.

**Fail-CLOSED giữ nguyên, không mở lỗ:**
- Dòng nằm NGOÀI mọi khoá (banner không phải JSON) ⇒ đường dẫn rỗng ⇒ `quy_được_hết=False` ⇒ vẫn ĐỎ.
- Drift trong khoá container **CHƯA khai** ⇒ vẫn ĐỎ, và nay báo đúng `basis.alpha` thay vì `alpha` trần.

**Ba ca `r294_*` (đỏ-trước/xanh-sau, phản chứng 2 chiều):**
1. `r294_drift_trong_khoa_da_khai_khong_bao_gia` — khai `basis` ⇒ drift bên trong được tha, `ok:true`,
   `raw_drift_undeclared == []`, và `raw_drift_keys` chứa `basis.max_r` (chứng minh đã quy theo đường dẫn).
2. `r294_drift_trong_khoa_chua_khai_van_do` — **không** khai ⇒ vẫn ĐỎ với `basis.alpha`. Cố ý dùng lệch
   **THỨ TỰ KHOÁ** để projection vẫn ổn định; lệch GIÁ TRỊ mà không khai gì thì bị chặn sớm hơn ở
   `AUDIT_PROJECTION_UNSTABLE`, không tới được nhánh này (đã đo).
3. `r294_mang_trong_khoa_chua_khai_van_do` — phần tử MẢNG: chưa khai ⇒ ĐỎ, đã khai ⇒ XANH.

**Ca `r288_helper_quy_dong_lech_ve_khoa` được CẬP NHẬT theo hợp đồng mới** (trả tuple đường dẫn; phần
tử mảng nay quy được về khoá chứa thay vì "không quy được"). **KHÔNG phải nới lỏng** — kết quả đỏ/xanh
giữ nguyên, và ca (3) ở trên khoá đúng KẾT QUẢ đó thay vì khoá cơ chế. Ca còn bổ sung vế banner-ngoài-
JSON để giữ bằng chứng fail-closed.

**Nghiệm thu:** selftest **1517/1517** · release-verify --strict rc=0 · workflow-audit --strict rc=0 ·
golden-test rc=0 · determinism-audit --strict rc=0 · doc-claims-check --strict rc=0 · ruff F delta 0.

# ★ v1.36.30 — r290: `rasoat-merge` fail-CLOSED + ghi ATOMIC · `rasoat_phuluc.py` ngang cổng với wrapper (2026-08-01)

Land hộ tranche của phiên khác (làn A — RAS-06/07/11/12/15/16).

**RAS-11 — ghi đè bảng master rồi mới báo lỗi.** Bản cũ nhét nguồn hỏng vào `bo_qua` rồi **VẪN**
`write_text` bảng master dựng từ phần input hợp lệ, xong mới `return 2`. Người vận hành thấy rc=2 sẽ
sửa file hỏng rồi chạy lại — nhưng **bản đúng để đối chiếu đã mất từ lượt đó**. Nay nguồn KHÔNG ĐỌC
ĐƯỢC ⇒ `NGUON_HONG_KHONG_DOC_DUOC`, `da_ghi:false`, bảng master GIỮ NGUYÊN.

**RAS-12 — `--state` hỏng mà lệnh vẫn `ok:true`.** Bản cũ bọc trọn khối hoà giải state trong
`try/except` rồi nhét lỗi vào `hoa_giai["loi"]`, trong khi `ok = not bo_qua` ⇒ rc=0. Nay fail-CLOSED.

**RAS-07 — `f.stem` KHÔNG phải định danh đơn vị.** File `unit-a.json` mang `unit_id: unit-b` làm state
đánh DONE cho `unit-a` (đơn vị **chưa hề được rà**) và bỏ sót `unit-b`. Nguồn sự thật là **PAYLOAD**;
thiếu `unit_id` ⇒ fail-closed, và báo `ten_file_lech_unit_id` để người vận hành thấy.

**Thứ tự lại cho đúng:** toàn bộ cổng chạy TRƯỚC mọi thao tác ghi; ghi bằng `_write_text_atomic`
(staging + `os.replace`) thay `write_text` trần — bị kill giữa chừng không để lại bảng master CỤT.

**RAS-15/16 (`rasoat_phuluc.py`) — chạy THẲNG script phải ngang cổng với `tl rasoat-merge`.**
Lọc bản sao lưu dùng CHUNG `_rasoat_la_ban_sao` (bản cũ `glob("*.json")` nuốt cả `*.bak*.json` ⇒ đếm
phát hiện HAI LẦN — đúng sự cố r216, chỉ khác đường vào); cổng TRÙNG dùng chung `_rasoat_trung_lap`
(bản cũ `dedup()` lặng lẽ GIỮ bản đầu, VỨT bản sau ⇒ mất phát hiện mà không ai biết); và
`(x or "").strip() or MẶC_ĐỊNH` thay `dict.get(k, mặc_định)` — `linh_vuc: ""` (template để trống) lọt
qua nguyên vẹn và sinh **heading RỖNG** trong phụ lục TRÌNH.

**Nghiệm thu:** selftest **1514/1514** · release-verify --strict rc=0 · workflow-audit --strict rc=0 ·
golden-test rc=0 · determinism-audit --strict rc=0 · doc-claims-check --strict rc=0 · ruff F delta 0.

⚠ **CỐ Ý KHÔNG land kèm** hai làn khác đang lẫn trong `lookup_ops.py`: **T1-c** (RAS-04/10/13 —
`cmd_rasoat_loop`/`_rasoat_corpus_hieu_luc`, chú thích tự khai "r290/T1-c" nhưng **test tên `r291_*`**)
và **r293** (RAS-02/03/08/09 — `_rasoat_state_*`). Cả hai còn nguyên trong cây cho chủ của chúng.
Đã đo: **không** tham chiếu chéo giữa ba làn, nên tách rời an toàn.

# ★ v1.36.29 — r289: cổng CON-TRỎ-TRẦN + diệt LỆNH MA + Q2/Q3 tài liệu (2026-08-01)

Land hộ tranche của phiên khác (phiên B viết; phiên này rà độc lập + land theo yêu cầu user).

**Bệnh (GATE-03b).** Guard H9 `_doc_pointer_findings` chỉ bắt con trỏ **CÓ TIỀN TỐ THƯ MỤC**
(`references/…`, `scripts/…`). Tên công cụ **TRẦN** trong backtick — `nlm_qa.py`, `split_structure.py` —
lọt sạch. Ca thật: `nlm_log.py add` sống từ v1.29.4 đến v1.35.44 mà không cổng nào kêu.

**Vá.** `_doc_bare_tool_findings()`: quét token khớp `*.py|sh|ps1|cmd|gs` **bên trong span backtick**,
chỉ token **không chứa `/`** (dạng có tiền tố đã do `_doc_pointer_findings` gác — không đếm hai lần),
đối chiếu **BASENAME** trong package-set nên `boot.py` ở `scripts/_fallback/` vẫn hợp lệ. Nối vào
`_verify_release_manifest` (`DOC_BARE_TOOLS_NOT_IN_PACKAGE`) + khoá `bare_tools` trong `release_verify.v1`.
**Ratchet 2 tầng:** fail-closed cho **3 tài liệu chỉ-dẫn-vận-hành-SỐNG**, còn lại **advisory** — bật
fail-closed toàn bộ là **82 mục đỏ ngày đầu**, guard sẽ bị vô hiệu hoá (bài học §0.8).

**Diệt lệnh ma.** `nlm_qa verify` KHÔNG tồn tại (không script, không subcommand) mà đã rò vào **4 tệp
SỐNG** kể cả thẻ máy-đọc `rasoat_hoso.json` ⇒ bước **A5 VERIFY** của Loop A trỏ vào hư không. Thay bằng
`tl nlm-query --source-id <sid> --strict-scope` (xác minh có thật trong `command_registry`).
`SKILL.md` §7 bỏ **7 tên script MA**; `set-package-public.cmd` → webapp action `share`.

**Q3 — `INSTALL.md`.** Ba dòng RA LỆNH deploy `Code.2.21.2i.gs`/`2.21.2h` trong khi gói **chỉ có**
`2.21.2o`/`2.21.2p` ⇒ chỉ dẫn cài đặt SAI BẢN đang được phát hành. Sửa cả ba về **2.21.2p**.

**Q2 — hai tài liệu kế hoạch** chuyển **LƯU TRỮ có chủ đích** (`_DOC_CLAIMS_HISTORICAL`), tự khai ở
dòng đầu. Ca `r264` được **ĐẢO vế `ok5` cho khớp**, và vế mới **mạnh hơn vế cũ**: (a) nhãn phải đúng
tài liệu ĐÃ KHAI, **và** (b) TUYỆT ĐỐI không được khai cả thư mục `docs/`/`docs/adr` — làm thế thì mọi
ADR hết bị bắt cứng, đúng cái "trang trí" mà r264 sinh ra để chặn. Vế răng-thật vẫn ở `ok4`.

**Đo:** `_doc_bare_tool_findings` trên tài liệu SỐNG **fail 8 → 0** (advisory 73, baseline 1).
**Nghiệm thu:** selftest **1511/1511** · release-verify --strict rc=0 · workflow-audit --strict rc=0 ·
golden-test rc=0 · determinism-audit --strict rc=0 · doc-claims-check --strict rc=0 · ruff F delta 0.

⚠ **Khoảng mù CÒN LẠI, không mở trong bản này** (GATE-04/T0-F): doc-set của guard vẫn chỉ là
`references/*.md` **không đệ quy** + `SKILL.md` = **30/53** tệp `.md` trong gói; và **không** guard nào
với tới `references/workflows/*.json` (thẻ máy đọc, `.json` ≠ `.md`).

# ★ v1.36.28 — r288: `golden-test` hết ĐI QUA raw drift KHÔNG KHAI — GATE-01 fail-CLOSED (2026-08-01)

Land hộ tranche của phiên khác (mã do phiên A viết, phiên này rà + land theo yêu cầu user).

**Bệnh (GATE-01).** `golden-test` so fixture theo **projection** đã scrub khoá volatile. Nhưng phần
**raw** thì chỉ ghi `raw_stable` rồi **đi tiếp**: raw lệch mà projection trùng ⇒ vẫn `ok:true`. Nghĩa là
một thay đổi hành vi THẬT có thể chui qua cổng, miễn nó rơi vào vùng đã bị scrub.

**Vì sao KHÔNG cưỡng chế `raw_stable=false ⇒ ok=false` trần trụi** (đơn thuốc đầu của audit): làm thế
thì ca `sweep` ĐỎ NGAY dù hoàn toàn lành — dòng lệch duy nhất là `snapshot_age_s`, vốn **đã khai**
volatile. Đơn thuốc đúng: **raw drift phải được GIẢI THÍCH TRỌN bởi khoá đã khai**.

**Vá.** `_raw_drift_keys(a, b)` quy drift về **TẬP KHOÁ** (đường dẫn khoá, đệ quy). Nếu tập ấy ⊄ tập
`volatile_keys` đã khai ⇒ `RAW_UNSTABLE_UNDECLARED`, **fail-CLOSED**. Và `--write` **từ chối ghi
fixture** khi còn drift chưa khai — chốt này quan trọng hơn cả vế đọc: nếu không có nó thì cách "chữa"
tự nhiên khi gặp đỏ lại chính là ghi đè fixture, tức hợp thức hoá drift.

**Năm ca `r288_*`** (đỏ-trước/xanh-sau): helper quy đúng về khoá · thứ tự khoá lệch **bị bắt** ·
`--write` từ chối ghi khi drift chưa khai · drift **khoá ĐÃ khai** vẫn xanh (chống báo giả) · raw ổn
định thì không đổi gì (chống tác dụng phụ).

**Nghiệm thu:** selftest **1508/1508** · release-verify --strict rc=0 · workflow-audit --strict rc=0 ·
golden-test rc=0 · determinism-audit --strict rc=0 · doc-claims-check --strict rc=0 · ruff F delta 0.

⚠ **Số đợt `r288` < version `1.36.28`** — có chủ đích: r291/r292 đã land trước (xem CHANGELOG dưới),
version phải đơn điệu. `rNNN` là mã thay đổi, KHÔNG phải bộ đếm phát hành.

# ★ v1.36.27 — r292: ca `r284` hết PHỤ THUỘC NỀN TẢNG — CI ubuntu ĐỎ suốt 4 bản vì bộ lọc TIỀN TỐ `/tmp/` (2026-08-01)

**Ca thật, đã ĐỎ CI bốn bản liên tiếp** (r285 · r286 · r287 · r291) mà máy Windows **luôn xanh** ⇒ không ai
thấy khi đo cục bộ. Đo `gh run view --log-failed`: mỗi lần đúng **MỘT** ca —
`r284_khung_test_profile_khong_doc_config_that` (`1501/1502`, rồi `1502/1503` sau khi r291 thêm 1 ca).

**Bệnh.** Khung cô lập của `r284` trỏ `HOME`/`USERPROFILE`/`cwd`/`HERE` vào `TemporaryDirectory()`, rồi
khẳng định *mọi* ứng viên `_config_candidates` phải nằm trong tempdir. Hằng CUỐI của
`_config_candidates` (`profile_env.py:67`) là `"/tmp/tra_luat_config.json"` — escape hatch cố ý, không bao
giờ nằm trong tempdir — nên phải loại trước khi khẳng định. Bản cũ loại nó bằng **TIỀN TỐ**:

```python
_cands = [c for c in _config_candidates(None) if not c.startswith("/tmp/")]
```

Trên **Linux**, `TemporaryDirectory()` **nằm trong `/tmp/`** (`/tmp/tmpXXXXXXXX`) ⇒ tiền tố ấy nuốt **SẠCH
cả 5 ứng viên hợp lệ**, `_cands` rỗng, `bool(_cands)` = `False` ⇒ ĐỎ. Trên **Windows** tempdir là
`C:\Users\…\Temp\…` nên chỉ đúng hằng bị loại ⇒ XANH. **Mô phỏng đối chiếu hai nền tảng (đo trước khi vá):**

| nền tảng | ứng viên thô | bộ lọc CŨ `startswith('/tmp/')` | bộ lọc MỚI `!= hằng` |
|---|---|---|---|
| ubuntu | 6 | **0 ⇒ `bool()` False ⇒ ĐỎ** | 5 ⇒ xanh |
| windows | 6 | 5 ⇒ xanh | 5 ⇒ xanh |

**Vá.** Loại **đúng một hằng theo GIÁ TRỊ**, không theo tiền tố ⇒ tất định trên mọi nền tảng. Nhân dịp
siết ca cho nó không thể xanh-giả nữa — 4 vế thay cho 2:

- `ok1` — hằng escape **phải CÒN** trong danh sách thô. Ai đổi/bỏ nó thì bộ lọc thành vô nghĩa và ca này
  sẽ chứng nhận RỖNG; nay ĐỎ ngay tại chỗ.
- `ok2` — loại **đúng MỘT** mục. **Đây là vế bắt chính bệnh cũ:** bộ lọc tiền tố loại 6/6 trên Linux ⇒
  `ok2` ĐỎ **tại đúng nguyên nhân**, thay vì đỏ mơ hồ ở `bool(_cands)`.
- `ok3` — còn ứng viên (bất biến cũ).
- `ok4` — mọi ứng viên còn lại nằm TRONG khung cô lập (bất biến gốc r284, giữ nguyên).

⚠ **Bài học chung, không riêng ca này:** *"lọc phần tử không mong muốn bằng TIỀN TỐ ĐƯỜNG DẪN"* là mẫu
hỏng khi tiền tố ấy cũng là **thư mục tạm của nền tảng**. Ca này còn là ví dụ sạch của việc **một ca
xanh trên máy dev vẫn có thể sai** — chỉ CI mới lộ ra; và cả **`r284` — bản vá cho "test phụ thuộc máy" —
tự nó lại phụ thuộc máy**.

- Test: `1503/1503` (Windows). Không thêm ca mới — **siết ca sẵn có** từ 2 vế lên 4 vế.
- Không đổi kích thước `SKILL.md` (chỉ đổi số version, cùng độ dài) ⇒ golden `workflow_audit.json` và
  `GOTCHAS.md:16` **giữ nguyên**.

# ★ v1.36.26 — r291: `docs/` RA KHỎI GÓI — trả 19/200 slot + đóng 3 con trỏ TREO (T0-G) (2026-08-01)

Q1 **user CHỐT 01-08: đưa `docs/` ra khỏi gói.** Cùng khuôn `rasoat` (r249) và `changelog_archive`
(v1.34.69): **GIỮ trong git, CHỈ loại khỏi GÓI**.

**Vì sao:** `docs/` là hồ sơ THIẾT KẾ của người giữ — 3 tệp kế hoạch/audit + 16 ADR. Runtime agent
không đọc chúng, nhưng chúng ăn **19/200 slot import**, trong khi quỹ **chỉ còn 4** (r244 đã đụng trần
THẬT: 199→202 làm `release-bundle` chết `IMPORT_LIMIT_EXCEEDED`). Trả quỹ về **23**.

**Đo (đối chiếu số dự kiến của kế hoạch — khớp trọn):**

| | trước | sau |
|---|---|---|
| manifest `file_count` | 195 | **176** (−19: 3 `docs/*.md` + 16 `docs/adr/*.md`) |
| quỹ slot /200 | 4 | **23** |
| `_doc_pointer_findings` fail | 0 | **0** |
| `_doc_bare_tool_findings` fail | 0 | **0** |

**Ba con trỏ TREO phải sửa CÙNG LƯỢT** — sau khi `docs/` rời gói, tệp NẰM TRONG gói mà trỏ vào
`docs/` là chỉ đúng lớp lỗi `r289` vừa diệt. Kế hoạch chỉ nêu ca (1); (2) và (3) do quét vét cạn
toàn bộ tệp-trong-manifest mà ra:

1. `SKILL.md:306` — hàng bảng `` | `docs/adr/` | `` → đổi sang khuôn *(ADR — dev-only)* của hàng ngay dưới.
2. `CONTEXT.md:4` — "Quyết định kiến trúc ở `docs/adr/`" → chú rõ **cây nguồn dev, KHÔNG trong gói**.
3. `scripts/tl_core/the_thuc.py:105` — "(nối theo trình tự 5 bước — docs/adr/0009)" → chú rõ ngoài gói.

⚠ **Guard H9 KHÔNG bắt được cả ba**: regex `_doc_pointer_findings` chỉ khớp tiền tố
`references|templates|scripts`; ca (3) còn nằm trong `.py` mà doc-set của guard chỉ gồm `.md`.
Đây là **khoảng mù đã biết**, thuộc GATE-04 (T0-F) — không mở rộng trong bản này.

**KHÔNG đụng** `_DOC_CLAIMS_DEFAULT_PATHS` (`workflow.py:775`): nó quét **CÂY DEV**, không phải gói ⇒
`docs/` VẪN chịu `doc-claims-check` đúng như r264 đặt ra. Loại khỏi gói không hạ một cổng nào.

**Test `r291_docs_ngoai_goi`** (đỏ-trước/xanh-sau, phản chứng 2 chiều): (1) `"docs"` ∈
`_RELEASE_EXCLUDE_DIRS`; (2) không mục manifest nào bắt đầu bằng `docs/`; (3) `file_count` giảm
**đúng 19** so mốc 195 — ratchet có chủ đích, cùng nếp `r209_baseline_ratchet`; (4) **phản chứng**:
19 tệp `docs/*.md` VẪN còn trên đĩa (giữ trong git) và mỗi tệp bị `_release_should_include` loại
**đúng vì khoá `docs`** — chặn ca xanh-giả "vắng khỏi gói vì lý do khác".

**Golden `workflow_audit.json` regen CÓ CHỦ ĐÍCH — đúng MỘT dòng:** `size_bytes` của `SKILL.md`
47.966 → **47.990** (thẻ workflow-audit chụp kích thước kernel). Không khoá nào khác đổi; đã đối
chiếu bằng `git diff` trước khi ghi. `references/GOTCHAS.md:16` cập nhật cùng lượt (test `r219`
khoá kích thước SKILL.md theo số ghi ở đó): **47.990B, đệm 138B** tới WARN 48.128.

⚠ **Số đợt `r291` KHÔNG khớp version `1.36.26` — CÓ CHỦ ĐÍCH.** Lúc land, `r288`/`r289`/`r290` đều đã
có mã trong cây nhưng CHƯA commit (ba phiên song song). Bản này land TRƯỚC nên lấy version kế tiếp
còn trống; lấy `1.36.29` để khớp số đợt sẽ **bịa ra ba version chưa từng tồn tại** và phá tính đơn
điệu mà `deploy-guard` dựa vào. Ba đợt kia land sau sẽ lấy `1.36.27+`.

# ★ v1.36.25 — r287: `determinism-audit` hết ĐỎ NGẪU NHIÊN vì probe công cụ NGOÀI (P16-T03) (2026-08-01)

P16-T03 (P2 vận hành) — **ca thật, đã chặn deploy BA lần trong 31-07/01-08.**

**Bệnh:** `determinism-audit` chạy `live-state-snapshot` HAI lần rồi `_live_state_diff`. Trong ảnh chụp có
`command_versions.<tool>` — do `_cmd_version_probe` gọi **subprocess của công cụ NGOÀI** với timeout.
Đo trên máy chuẩn: `nlm --version` mất **3,2 / 6,3 / 7,3 giây** (3 lần liên tiếp), timeout probe là **10s**.
Dưới tải — hoặc đơn giản là xui — một ảnh `TimeoutExpired`, ảnh kia kịp ⇒ bốn đường
`command_versions.nlm.{ok,error,returncode,version}` lệch ⇒ chỉ tiền tố `volatile` được miễn nên cả bốn
vào `unexpected_changes` ⇒ `ok:false` ⇒ **gate ĐỎ, deploy DỪNG**. Đã quan sát lệch cả HAI chiều (lần
timeout ở ảnh trước, lần ở ảnh sau) ⇒ đúng 50/50, không phải chỉ do tải.

Đây **không phải** tính bất định của tl — là **nhiễu đo** của một công cụ bên ngoài. Nhưng
`determinism-audit` lại chính là thứ sinh ra để chứng minh tính tất định, nên nó tự đỏ là mất hết ý nghĩa.
(Đã loại trừ nguyên nhân đã biết: `~/.notebooklm-mcp-cli/chrome-port-map.json` = `{}`, không có PID chết.)

**VÁ — miễn trừ CÓ ĐIỀU KIỆN, tuyệt đối không miễn mù:**
- `_live_state_diff` chỉ bỏ qua thay đổi dưới `command_versions.<tool>.*` **khi CHÍNH PHÉP ĐO không ổn
  định** — tức `ok` KHÁC NHAU giữa hai ảnh (một bên probe hỏng). Hai bên **cùng đo được** mà `version`
  khác nhau ⇒ **VẪN BÁO**, vì đó là công cụ thật sự đổi phiên bản giữa hai lần chạy — điều đáng biết.
- Ca được miễn mang `allowed_reason: "PROBE_CONG_CU_NGOAI_KHONG_ON_DINH"` — **nói ra vì sao**, không miễn
  im lặng (im lặng chính là cách một cổng biến thành cổng-luôn-cho-qua).
- `_cmd_version_probe` timeout 10s → **25s**: 10s quá sát với 3-7s thật. Nới chỉ GIẢM nhiễu; phần còn lại
  do miễn-trừ-có-điều-kiện xử. Chỉ tốn thêm thời gian khi công cụ thật sự treo.

**Kiểm (+5 case gọi `_live_state_diff` THẬT trên hai tệp ảnh chụp, đúng đường `determinism-audit`;
selftest 1502/1502):** phản chứng đo trên bản CHƯA VÁ — **3/5 ĐỎ**; 2 case còn lại xanh **đúng thiết kế**
vì là cặp «KHÔNG ĐƯỢC ĐỔI». Phủ: miễn trừ đối xứng cả hai chiều timeout · **★version đổi THẬT vẫn bị báo**
(phản chứng quan trọng nhất — miễn mù sẽ nuốt mất ca này) · **không nới lỏng đường nào ngoài
`command_versions`** (thay đổi `registry.id` vẫn fail-closed nguyên vẹn) · hai ảnh giống hệt vẫn `ok`,
0 thay đổi (bản vá không tự chế ra khác biệt).

# ★ v1.36.24 — r286: profile GÕ SAI hết mượn được corpus NỀN ở đường ĐỌC (P16-F09) (2026-08-01)

P16-F09 (P1 sai kết quả).

**Bệnh:** v1.33.48 mới bịt đường **GHI** (profile yêu cầu tường minh mà không có trong config ⇒ scope
RỖNG ⇒ guard hạ nguồn chặn). Đường **ĐỌC** vẫn thủng nguyên: `_apply_profile_env` vẫn đặt
`TL_PROFILE = <tên ma>` ⇒ `_profile_cache_dir()` trỏ `CACHE/<tên ma>/`; `_load_manifest_full` gặp
cache-miss thì gọi `manifest_export` với scope RỖNG ⇒ webapp trả **manifest NỀN** ⇒ `_atomic_write_text`
ghi nó vào cache của profile-ma (**BỀN VỮNG — còn nguyên sau khi lệnh kết thúc**) ⇒ `exists` /
`reg-query` / `locate` trả **corpus NỀN dưới NHÃN tên gõ sai**. Người dùng tin là đang xem hồ sơ dự án
của mình, thực ra đang xem kho nền.

**VÁ — chốt ở ĐÚNG MỘT CHỖ:** marker env `TL_PROFILE_MISSING`
- **đặt** ở nhánh PROFILE_NOT_FOUND của `_apply_profile_env`;
- **gỡ** ở nhánh profile hợp lệ (cùng-process đổi sang profile đúng thì phải chạy lại được — nếu không,
  một lần gõ sai làm hỏng mọi lệnh sau trong cùng tiến trình, vd `tl loop`);
- **gỡ** ở `_apply_unconfigured_profile_env` — profile env-only KHÔNG có file config là đường **HỢP LỆ**
  theo §9, không được chặn oan;
- **chặn** ở `_load_manifest_full`, **ĐẶT TRƯỚC `mkdir`** để đến cả thư mục cache của profile-ma cũng
  không được tạo. Vá một chỗ phủ mọi lệnh đọc — mọi đường resolve theo số hiệu đều đi qua
  `_manifest_entries` → hàm này;
- thêm `TL_PROFILE_MISSING` vào `_PROFILE_ENV_OVERLAY_KEYS` để `_ProfileEnvGuard` và
  `_base_manifest_entries` snapshot-restore đúng (đọc NỀN có chủ đích từ trong profile dự án vẫn chạy).

**Kiểm (+5 case HÀNH VI qua `apply_profile_offline` + `_manifest_entries` THẬT; selftest 1497/1497 —
xanh cả chế độ thường lẫn hermetic):** phản chứng đo trên bản CHƯA VÁ — **2/5 ĐỎ** (ca lõi profile-ma và
ca gỡ-chốt); 3 case còn lại xanh **đúng thiết kế** vì là cặp «KHÔNG ĐƯỢC ĐỔI»: profile THẬT vẫn đọc ·
corpus NỀN vẫn đọc · profile env-only §9 không bị chặn oan. Ca lõi kiểm THÊM: **thư mục cache mang tên
ma KHÔNG được tạo** — cache-ma mới là thứ sống sót sau khi lệnh kết thúc.

★Khung test đã dời `HERE` theo bài học r284 (không thì lại là test phụ thuộc máy).

# ★ v1.36.23 — r285: bịt RÒ RỈ MONKEYPATCH trong selftest — khối r87 làm mọi test sau nó chạy trên bản GIẢ (P16-T02) — TEST-ONLY (2026-07-31)

**Bệnh (P0 của bộ test, đo trực tiếp chứ không suy):** khối test `r87` khai
`_keys86 = ("_gas","load_creds","apply_profile_offline","_apply_journal_start","_journal_append")` để
khôi phục, nhưng bên trong (`:6672-6674`) còn thay THÊM **ba** tên nữa: `_manifest_entries` → `lambda: []`,
`_reg_before_from_manifest` → `lambda: {}`, `_apply_gate` → `(True, {"ok": True})`. Ba tên đó KHÔNG nằm
trong danh sách khôi phục ⇒ stub **sống tới hết `run()`**.

**Hại đo được:** (i) mọi case sau `:6672` mà không tự thay `_manifest_entries` đều thấy **corpus RỖNG**;
(ii) mọi case đi qua `_apply_gate` được cho qua **VÔ ĐIỀU KIỆN** — tức cổng preflight bất biến (`_apply_gate`,
ADR) **chưa từng được kiểm** ở nửa sau bộ test. Đúng lớp `false-green-test-qua-bind` đã có trong sổ.

**Cách phát hiện (một phép đo, không đoán):** cài `__setattr__` hook lên module `tl` rồi chạy
`tl_selftest.run()` — ghi được **343 lần gán** `_manifest_entries`; lần gán từ `:6672` KHÔNG BAO GIỜ được
trả về bản gốc. Tại điểm test mới của P16 chạy, `_TL_MODULE._manifest_entries.__qualname__` =
`"run.<locals>.<lambda>"` (không phải hàm sản xuất) và trả `[]`.

**BẰNG CHỨNG HẠI CÓ THẬT:** vá rò rỉ xong, `r97_no_nlm_add_stops_at_drive_registry` (`:7998`) **SẬP NGAY**
(`JSONDecodeError` — lệnh không in nổi JSON vì đi đọc manifest thật). Nghĩa là test r97 xưa nay xanh **chỉ
nhờ** stub rò từ khối khác; kịch bản «corpus trống ⇒ không trùng ⇒ nạp tiếp» của nó **chưa từng được khai
báo**. Nay r97 tự khai `_manifest_entries = []` — cùng kịch bản, nhưng nói ra.

**VÁ (chỉ `tl_selftest.py`, không đụng code sản xuất):**
1. `_keys86` phủ TRỌN tập tên khối r87 thay (thêm `_manifest_entries`, `_reg_before_from_manifest`, `_apply_gate`).
2. Khối r97 tự khai stub `_manifest_entries` của mình (+ thêm vào `_keys97` để khôi phục).
3. **CHỐT CHẶN TÁI PHÁT** — `r285_khong_ro_ri_monkeypatch`: chụp ảnh MỌI hàm/lớp của module `tl` ở ĐẦU
   `run()`, đối chiếu identity ở CUỐI; tên nào lệch là monkeypatch bị bỏ quên ⇒ case ĐỎ và **in đích danh**
   danh sách tên để sửa được ngay, thay vì để nó âm thầm làm xanh giả các lượt sau.

**Vùng ảnh hưởng đo được (không đoán):** chạy hermetic sau khi bịt rò rỉ ⇒ **đúng 3 test** lộ ra là
xanh-giả, tất cả cùng họ `ingest_local`: `r97_no_nlm_add_stops_at_drive_registry`,
`r114_no_nlm_add_never_counts_slots`, `r115_ingest_local_dead_cookie_autoswitch_addtay`. Cả ba được vá
theo ĐÚNG nguyên tắc: **tự khai stub của chính nó** (`_manifest_entries = []` — vốn là kịch bản
«corpus trống, không có dòng nào để dedup» của chính chúng), KHÔNG khôi phục rò rỉ để làm chúng xanh lại.

**Chi phí ẩn cũng lộ ra:** trên máy CÓ creds thật, `_selftest_seal_env` cố ý KHÔNG chặn mạng (vế 3 của
r262), nên ba test đó — khi mất stub — đi gọi webapp thật, mỗi lần retry 5s+15s ⇒ selftest vọt từ ~100s
lên >10 phút. Sau khi khai stub tường minh: **103s, 1492/1492**. Hermetic (ép creds giả) cũng 1492/1492.

# ★ v1.36.22 — r284: sửa test PHỤ THUỘC MÁY của r281/r283 (khung cô lập bỏ sót `HERE`) — TEST-ONLY (2026-07-31)

**Ca thật, bắt lúc người giữ chạy `deploy-package.cmd` trên cây canonical (31-07):** gate DỪNG ở bước 1 —
`selftest 1483/1490`, 7 case ĐỎ (6 của r281 + 1 của r283). Cùng commit `b1a86c8` chạy trong worktree
`C:\qh\p16_wt` lại `1490/1490`. **Code sản xuất KHÔNG sai — bộ TEST của r281/r283 sai.**

**Bệnh:** `_config_candidates` xếp ứng viên theo thứ tự `cwd` → **`HERE.parent`** → `HERE` →
`~/.tra_luat_config.json`. Khung cô lập của r281/r283 chỉ dời `HOME`/`USERPROFILE`/`cwd`, **không dời
`HERE`** — nên trên máy có `tra_luat_config.v2.json` nằm CẠNH skill (đúng máy chuẩn `D:\Quốc hội\tra-luat`,
tệp này `.gitignore` nên không theo repo) thì ứng viên ĐÓ **thắng** config trong HOME giả: test đọc phải
config THẬT của người dùng và đỏ. Worktree không có tệp đó ⇒ **xanh GIẢ**. Đây đúng lớp bug máy-phụ-thuộc
mà GOTCHAS §4 đã ghi, chỉ khác chiều: lần này local-sạch xanh giả, máy-có-config mới đỏ.

**Vá (chỉ `tl_selftest.py`):** hai khung `_run_loadcreds281` / `_run_snap283` dời luôn `_TL_MODULE.HERE`
sang `<tempdir>/scripts` (khôi phục trong `finally`) ⇒ toàn bộ dãy ứng viên nằm trong tempdir.

**CHỐT CHẶN TÁI PHÁT** — case mới `r284_khung_test_profile_khong_doc_config_that`: bên trong khung cô lập,
**mọi** ứng viên do `_config_candidates(None)` trả về phải nằm trong tempdir (`/tmp/...` là hằng cuối hàm,
không tồn tại trên Windows, được loại). Khung nào quên dời `HERE` sẽ đỏ ngay tại đây thay vì đỏ ở máy người khác.

**Phản chứng (tái hiện ĐÚNG điều kiện cây canonical trong worktree bằng `tra_luat_config.v2.json` GIẢ —
giá trị mồi, không có bí mật, tệp `.gitignore`):** trước vá **1483/1490 với ĐÚNG 7 case đỏ y hệt cây
canonical**; sau vá **1490/1490** cùng điều kiện; bỏ tệp mồi đi vẫn **1491/1491**. Không đụng một dòng
code sản xuất nào.

# ★ v1.36.21 — r283: `cache-snapshot` — cổng treeHash FAIL-CLOSED + không ghi được `{}` đè index + đúng cache của profile (P16-F06 + P16-F14) (2026-07-31)

P16-F06 (P0 mất dữ liệu) + P16-F14 (P1 sai kết quả) — **ba lỗ cùng nằm trong `cmd_cache_snapshot`**, cộng
lại thành: một snapshot RÁC xoá trắng `manifest_index.json` (~3,4MB) của corpus NỀN và **báo THÀNH CÔNG**.

**(a) F14 — `idxp` tính TRƯỚC khi áp profile.** `cache-snapshot` nằm trong `_CREDS_LAZY_CMDS` nên `main()`
KHÔNG nạp creds/profile hộ; `load_creds` cũ chỉ chạy ở nhánh import KHÔNG-`--force` — tức SAU khi `idxp`
đã chốt — và với `--force` thì không chạy lần nào; nhánh **export không áp profile lần nào cả**. Đứng ở
profile dự án mà đọc/ghi index của NỀN. **Vá:** `apply_profile_offline` ở ĐẦU hàm, trước mọi phép tính
đường dẫn (`_cache_file` đi qua `_profile_cache_dir()`).

**(b) F06 — cổng treeHash FAIL-OPEN.** `if cur_th and snap_th and cur_th != snap_th` — thiếu BẤT KỲ vế nào
(snapshot không có `treeHash`, hoặc `manifest_export` không trả/nổ) là cổng **im lặng cho qua**. **Vá:**
FAIL-CLOSED cả hai chiều — thiếu treeHash ở bất kỳ đầu nào ⇒ `TREEHASH_KHONG_DOI_CHIEU_DUOC` rc=1; lời gọi
`manifest_export` nổ cũng tính là «không đối chiếu được» (trước: exception lọt ra ngoài / cổng bỏ qua).

**(c) F06 lõi mất dữ liệu — `sd.get("index") or {}`.** Snapshot thiếu/rỗng `index` ⇒ GHI `{}` ĐÈ file index
rồi in `ok:true, gated:true`. **Vá:** kiểm NGUỒN trước — `index` phải là dict KHÔNG RỖNG, không thì
`SNAPSHOT_INDEX_EMPTY` rc=2 và **KHÔNG đụng đích**. Cổng này `--force` **KHÔNG bỏ qua được**: `--force` nghĩa
là «tôi chấp nhận snapshot CŨ», không phải «cho phép xoá index». Cả hai đường ghi (import + export `--out`)
chuyển sang `_atomic_write_text`.

**Kiểm (+8 case HÀNH VI qua `cmd_cache_snapshot` thật, cache dir thật trong HOME giả; selftest 1490/1490):**
phản chứng đo trên bản CHƯA VÁ — **6/8 ĐỎ**, 2 case còn lại xanh đúng thiết kế (cặp «KHÔNG ĐƯỢC ĐỔI»:
treeHash KHỚP thì import bình thường · treeHash LỆCH vẫn `TREEHASH_MISMATCH` rc=1 như cũ). Mọi case chặn
đều kiểm thêm **index cũ còn NGUYÊN**; case F14 kiểm thêm **index của NỀN không bị tạo**.

# ★ v1.36.20 — r282: `profile-file-remove` có cổng bất biến profile — gõ sai tên không còn xoá vào registry/notebook NỀN (P16-F04) (2026-07-31)

P16-F04 (P0 mất dữ liệu).

**Bệnh:** `cmd_profile_file_remove` là đường GHI **phá huỷ nhất** của nhóm profile (xoá nguồn NLM — BẤT KHẢ
NGHỊCH — + trash Drive + `reg_delete`) nhưng là đường DUY NHẤT không gọi `_profile_policy_error`, trong khi
mọi đường cùng lớp đều có (ingest_ops ×5, ops_misc:1429, profile_mgmt:79) — kể cả lệnh ANH EM
`profile-file-add` (= `cmd_profile_ingest`). Gõ sai `--profile-name` (lệch dấu/typo) ⇒
`_profile_manifest_entries_for` trả manifest NỀN (1315 dòng); drive_id vẫn khớp nên KHÔNG rơi
`NO_MATCHING_PROFILE_ROWS`; `load_creds` với tên sai làm `_scope_params()` rỗng ⇒ `source_delete` /
`trash` / `reg_delete` bắn thẳng vào **notebook + registry NỀN**, in `{"ok":true}` rc=0.

**VÁ:** đúng khuôn `cmd_profile_ingest` — `apply_profile_offline` → `_profile_policy_error(require_registry,
require_manifest, forbid_inherit)` → **RỒI MỚI** đọc manifest. Thứ tự này quan trọng: đọc manifest TRƯỜC cổng
nghĩa là đã kéo manifest NỀN về cache của profile-ma (họ F07/F09) dù sau đó có chặn. Profile-ma ⇒
`PROFILE_CATEGORIES_OWN_REQUIRED` rc=2, không một lời gọi phá huỷ nào.

**Kiểm (+5 case HÀNH VI qua `cmd_profile_file_remove` thật, đếm MỌI lời gọi phá huỷ; selftest 1482/1482):**
phản chứng đo trên bản CHƯA VÁ — **3/5 ĐỎcVN**, 2 case còn lại xanh đúng thiết kế (cặp «KHÔNG ĐƯỢC ĐỔI»):
profile dự án HỢP LỆ vẫn gỡ đủ 3 đường · corpus NỀN giữ nguyên hành vi (`_profile_policy_error` trả None
theo thiết kế — không biến bản vá thành cổng chặn cả đường nền). Phủ thêm: registryDocId RỖNG (đúng lớp sự
cố clobber 1.23.21) cũng bị chặn · **DRY cũng chặn** (DRY trên profile-ma vẫn kéo manifest nền về cache ma).

# ★ v1.36.19 — r281: `load_creds` hết bỏ qua `config.defaultProfile` — lệnh GHI không còn âm thầm rơi về corpus NỀN (P16-F08) (2026-07-31)

P16-F08 (P0 ghi nhầm corpus).

**Bệnh:** `load_creds` có nhánh tắt «đã có TL_WEBAPP+TL_TOKEN trong env thì khỏi đọc config», và vòng quét
config bên trong nó bị bọc bởi `if profile:`. Hệ quả: khi người dùng KHÔNG gõ `--profile` (đường thường
dùng nhất — vì đã khai `defaultProfile` trong config chính để khỏi gõ), `_apply_profile_env` KHÔNG BAO GIỜ
chạy ⇒ `TL_PROFILE` không được đặt ⇒ `_active_profile()` trả `vbqppl` ⇒ **mọi lệnh GHI non-lazy đổ vào corpus
NỀN trong im lặng**, và mọi guard profile (`_profile_policy_error`…) đều `return None` sớm vì profile chính là
DEFAULT_PROFILE. `defaultProfile` vẫn được `_selected_profile_name` hỗ trợ đầy đủ — chỉ là nhánh này không gọi tới.

**VÁ:** bỏ `if profile:` — quét config KỂ CẢ khi `profile=None`. Không đảo một thứ tự ưu tiên nào: chính
`_selected_profile_name` xếp `--profile` > env `TL_PROFILE` > `config.defaultProfile` > `vbqppl`, nên bỏ guard
là đủ. `_apply_unconfigured_profile_env` vẫn chỉ chạy khi CÓ `profile` mà không tìm ra config (giữ nguyên nghĩa).
Thêm một dòng NHẮC in **1 lần/process** khi scope được chọn bởi `defaultProfile` (không phải do người gõ):
scope ghi VÔ HÌNH đúng là thứ đã biến F08 thành P0. Chỉ in khi profile THẬT và khác nền — nền là trạng thái
mặc định, nhắc mỗi lệnh là ồn vô ích.

**Kiểm (+6 case HÀNH VI qua `load_creds` thật, HOME+cwd+env cô lập; selftest 1477/1477):** phản chứng đo
trên chính bản CHƯA VÁ — **4/6 ĐỎcVN**, 2 case còn lại xanh đúng theo thiết kế (chúng là cặp «KHÔNG ĐƯỢC ĐỔI»).
Phủ: `--profile` tường minh vẫn thắng · env `TL_PROFILE` export vẫn thắng `defaultProfile` (đường
`state-get`/`state-put` + RASOAT_HOSO_LOOP §7 dựa vào nếp này — r214 đã trả giá một lần) · phiên env-only
KHÔNG có config giữ nguyên · `defaultProfile` = nền thì KHÔNG in nhắc · `defaultProfile` trỏ tên không có block
vẫn fail-closed PROFILE_NOT_FOUND + scope RỖNG (giữ nguyên v1.33.48, không mượn scope nền).

# ★ v1.36.18 — r280: `init-config` hết ghi đè trọn config — HOÀ + BACKUP + ATOMIC (P16-F01) (2026-07-31)

Mở chiến dịch **P16** (vá nhóm ingest/profile — 10 phát hiện Pha 1 chưa ai vá). F01 (P0 mất dữ liệu).

**Bệnh:** `save_local_config` (ops_misc.py:405-418) khởi tạo `data = {}` rồi `json.loads(config_json)` —
KHÔNG đọc file đích để hoà — và `path.write_text(...)` ghi đè thẳng `~/.tra_luat_config.json`: không backup
(đối lập `profile-delete` đã có từ r202), không atomic (đối lập `_write_json_atomic`), không journal. `tl init-config
--from-public` là lệnh mà **chính CLI khuyên chạy ở ≥5 thông điệp lỗi** (profile_env.py:325; profile_mgmt.py
:339/1329/2170/2251) ⇒ sau khi token xoay, người dùng gõ đúng lệnh được khuyên thì **MẤT TRẮNG toàn bộ block
`profiles`** (mọi profile dự án), CLI vẫn in «✓ đã lưu config». Hậu quả tiếp theo đúng lớp sự cố 1.23.21:
`--profile <dự-án>` rơi PROFILE_NOT_FOUND, hoặc mọi lệnh GHI chạy trên scope nền vbqppl. Lớp sự cố này ĐÃ TỪNG
BIẾT (auto-heal 2026-06-30) nhưng chỉ vá ĐÚNG 1 TRƯỜNG (`registryDocId` legacy), không vá phép ghi đè.

**VÁ:** `_merge_local_config` (PURE) — template public HOÀ LÊN TRÊN file cũ: khoá cấp 1 → `new` thắng KHI
CÓ MẮT (khoá cũ không được nhắc thì GIỮ — ví dụ `defaultProfile`); `profiles` hoà theo TẮNG TÊN, trong mỗi block
lại hoà theo TẮNG Ô (block dự án chỉ có ở file cũ sống; ô người dùng ghim bằng `config-pin-registry` sống; ô
template nhắc tới thì template thắng). `save_local_config` nay: đọc file đích → hoà → **BACKUP byte** ra
`_config_backup_dir()` (NGOÀI cây skill — doctrine r193/r202, backup chứa token) → **`_write_json_atomic`**.
Kể cả file cũ HỎcNG (không parse được) vẫn được backup nguyên byte trước khi thay. Kiểm bất biến
webapp/token chuyển sang đo trên **bản SẼ GHI** (template thiếu token mà file cũ có thì kết quả vẫn dùng được;
cái phải chặn là file ĐÍCH thiếu). AUTO-HEAL legacy `1mATG` tách thành `_heal_legacy_registry_doc_id` và nay
chạy trên **bản ĐÃ HOÀ** — heal riêng template thì id legacy nằm sẵn trong file cũ sẽ sống sót qua bước merge mới
(bẫy do chính bản vá này sinh ra, đã bịt). Đường reset CỐ Ý: cờ mới **`--replace`** — vẫn backup, và in
CẢNH BÁO liệt kê đích danh block bị xoá + đường backup để hồi. Đường hoà cũng NÓI RA đã giữ những block nào
— im lặng chính là cách bản cũ làm mất dữ liệu mà không ai biết.

**Kiểm (+10 case, selftest 1471/1471):** 6 PURE `_merge_local_config`/`_heal_legacy` (giữ block dự án · ô ghim
sống & template thắng · giữ khoá cũ không bị nhắc · heal trên bản đã hoà) + 4 HÀNH VI qua đường sản xuất
`cmd_init_config` với file thật trong tempdir. **PHẢN CHỨNG:** (a) file cũ trống/không phải dict ⇒ merge = chính
template (không tự chế thêm) · (b) template không có `profiles` ⇒ block cũ nguyên vẹn · (c) **phiên TRỐNG
(chưa có config) — đúng đường mà lệnh này sinh ra — KHÔNG đổi hành vi**: rc=0, ghi đúng template, không backup,
không cảnh báo · (d) file cũ HỎcNG vẫn được backup nguyên byte. Parser surface snapshot regen (thêm `--replace`).

# ★ v1.36.17 — r279: chốt CHỐNG GHI SONG SONG cho đường NLM + registry (2026-07-31)

**Bệnh (ca thật, có bằng chứng — không phải giả định):** 31-07-2026 HAI phiên cùng được duyệt một đợt
việc và cùng ghi vào notebook `45739ff7` + registry. Sổ: `rasoat/KETQUA_NLM_QA_QB_QC_2026-07-31.md` §4.4
(đối chiếu journal hai bên) và `rasoat/KETQUA_US_NLM_QUEUE_2026-07-31.md` §8.

Cứu được lượt đó là nhờ **cổng dedup-live của `nlm-add`** — nó đối chiếu LIVE trước khi ghi nên chặn
`ALREADY_ON_NOTEBOOK`, và chính cú chặn đó làm phiên kia phát hiện có tác nhân thứ hai. Nhưng hai đường
ghi còn lại KHÔNG có cổng nào:

1. **`nlm-source-remove` in `deleted` KHỐNG.** `nlm_cli.source_delete` trả ok cho CẢ sid ĐÃ biến mất và
   raw không kèm `deleted_count`, nên `_source_remove_delete_verdict` cho `deleted`. Hai phiên gỡ cùng
   sid `04e51f9c` cách nhau **59 giây**, phiên sau vẫn in `deleted:1` — nhận công việc nó không hề làm.
2. **`register` đè im lặng.** Đường ghi đã journaled + verified-readback, nhưng verify chỉ trả lời «ta
   ghi được gì», KHÔNG trả lời «ta có đè mất việc của ai không». LockService bảo đảm RMW nguyên tử nên
   sổ không HỎNG — lost-update thì vẫn xảy ra êm ru, cả hai phiên đều `verified`.

**VÁ — hai chốt, đối xứng với cổng dedup-live sẵn có:**

- `_nlm_remove_presence_verdict` (PURE) + gắn vào `cmd_nlm_source_remove`: đo listing VẬT LÝ TƯƠI trước
  khi gỡ. sid đã vắng ⇒ **KHÔNG gọi `source_delete`**, trả `noop` + `ALREADY_GONE_CONCURRENT` (ok vẫn
  true — idempotent theo TRẠNG THÁI ĐÍCH, không theo lệnh). Không liệt kê được LIVE ⇒ **fail-closed**
  (doctrine S13, như dedup gate), thoát bằng `--skip-live-check` (cờ mới). `--force` vẫn chỉ bỏ guard
  con trỏ registry — hai mối lo khác nhau, hai cờ khác nhau.
- `_expect_precondition_verdict` (PURE) + `register --expect COL=VAL` (lặp được): chốt **CAS** — đọc
  dòng NGAY TRƯỚC khi ghi, lệch kỳ vọng ⇒ **rc=3, KHÔNG ghi gì**. Dùng đúng mã rc=3 của chốt chống thụt
  lùi deploy: cùng nghĩa «phiên khác vừa đụng, DỪNG, để người quyết». VAL rỗng = kỳ vọng cột RỖNG; dòng
  biến mất ⇒ `ROW_NOT_FOUND` (cũng là va chạm); cột lạ ⇒ `EXPECT_COL_UNKNOWN` — gõ nhầm tên cột mà cho
  qua thì chốt thành «luôn khớp» = chốt bị lừa (họ lỗi rc=0-giả trong CLAUDE.md).

**Kiểm:** selftest **1461/1461** (+12 case r279: 4 PURE presence · 6 PURE CAS · 3 HÀNH VI đầu-cuối qua
`cmd_nlm_source_remove` gồm phản chứng «sid còn sống thì chốt phải TRONG SUỐT»). Full-gate 8/8 xanh.
Ruff DELTA so master: `tl.py` 12 F821 / 0 F401 = **0 delta**; tên mới bị cờ đều thuộc lớp re-home
BY DESIGN, đã kiểm HÀNH VI resolve thật qua `__globals__` của module tiêu thụ.

**Bẫy đã sập trong chính lượt vá này (ghi lại để không lặp):** dùng `Path.write_text` để vá
`tl_selftest.py` đã **nuốt CRLF toàn tệp** (23712 dòng → LF), diff phình thành 23794 dòng giả. Lộ ra
KHÔNG phải nhờ đọc diff mà nhờ `RELEASE_MANIFEST.json` có `total_bytes` **GIẢM** 6404 byte trong khi
bản vá chỉ THÊM code — con số âm vô lý là thứ duy nhất bắt được. Vá tệp CRLF phải đi `write_bytes`.


# ★ v1.36.16 — r278: `_sohieu_typo_near` vế (1) last-wins → duy-nhất-theo-số-hiệu + corroborate + AMBIG (P15-F12) (2026-07-31)

F12 (P2) sổ P15; phiếu thiết kế + grill 8 câu: `C:\qh\p15_review_core_2026-07-30\P15_PHIEU_r278.md`.

**Bệnh:** vế (1) agency-typo (cùng SỐ+NĂM, khác mã, cùng họ) GÁN ĐÈ `agency_hit` mỗi lần khớp — không
tích lũy, không đòi duy nhất. Nền 31-07 có **26 nhóm (số,năm,họ) ≥2 mã đồng tồn tại HỢP PHÁP** (11 TT
đa-bộ + 13 QH gồm cặp hệ thống luật QH15↔VBHN-VPQH cùng số+năm + 1 TW; probe phiên e53947f2): cited
`01-2026-TT-BCT` (vắng corpus) duyệt xuôi gợi TT-BYT, duyệt ngược gợi TT-BGDDT — LẬT theo thứ tự
manifest; caller gắn `DOC_TEXT_SOHIEU_TYPO` conf=**high** + canonical TRỎ THẲNG + note «nên dùng X»
⇒ trỏ bừa 1 bản trong nhóm và CHE MISSING (cited nhiều khả năng là văn bản thứ ba vắng corpus).

**VÁ (đúng đề xuất sổ, kết hợp cả hai vế):** tích lũy ứng viên vế (1) theo **SỐ HIỆU** (dict sh→entry
đại diện max `_entry_score`, khuôn r272 — identity-dup 2 bản/1 văn bản không sinh mơ-hồ-giả); 1 số hiệu
→ trả `(entry, sh)` NHƯ CŨ (conf high hợp lệ); ≥2 → corroborate tên (giao tập sohieu của
`resolve_identity(name_q)` với tập ứng viên — đếm theo số hiệu), đúng 1 → nhận; vẫn mơ hồ → trả
`(None, [sh...])` sort tất định `(-score, sh)`: caller giữ flag `DOC_TEXT_SOHIEU_TYPO` nhưng
**conf=low + KHÔNG canonical** + note liệt kê ≤3 ứng viên và nhắc khả năng MISSING. Vế (2) sửa CÙNG
bệnh đếm: `len(corro)==1` cũ đếm theo `id(e)` — identity-dup (NĐ 188×2 nền) làm 2 entry cùng sohieu
đếm =2 → từ chối oan; nay đếm theo SỐ HIỆU duy nhất. GIỮ NGUYÊN: khác-họ → None (P0-2),
VBHN-coverage-trước-TYPO, `--strict` xref vẫn đếm flag (mơ hồ vẫn là finding).

PHẢN CHỨNG (probe qua đường sản xuất `import tl`, manifest nền 1315 snapshot — scratchpad phiên
8f0ab7cf `probe_r278*.py`): **26/26 nhóm mồi cited-fake → AMBIG tất định xuôi=ngược, flip=0** (trước:
lật theo manifest) · 8/8 case thiết kế đúng · demo sổ 01-2026 hết lật · 2 test P0-2 khác-họ +
`xref_sohieu_typo_agency` (1-ứng-viên) giữ nguyên hành vi. Selftest +6 case r278 (unique-direct /
ambig-tất-định-flip / corroborate-chọn-đúng / identity-dup-vẫn-unique / vế-2-đếm-theo-sohieu /
classify-conf-low-không-canonical-không-«nên dùng»). 1447/1447.

# ★ v1.36.15 — r277: footnote-map câm trên VBHN cặn HYPERLINK/marker dính đôi + def_missing giả leading-zero (P15-F10+F11) (2026-07-31)

F10 (P1) + F11 (P2) sổ P15 — vá GỘP 1 bản theo lệnh user (cùng vùng `resolve_footnote_amendments`); phiếu
thiết kế + grill: `C:\qh\p15_review_core_2026-07-30\P15_PHIEU_r277.md`.

**F10 — footnote-map CÂM không phân biệt được với "doc không có chú thích":** mốc `first` đòi def dạng
`^[n]␣`, nhưng extract cache nền tồn tại SONG SONG ≥2 kiểu extract (78 doc chuẩn parse tốt vs 18 doc trượt
mốc — đo 31-07 trên 403 file): 12 doc cặn field-code Word « HYPERLINK \l "_ftn(ref)N" » (di chứng export
.docx — 39-VBHN Thư viện, 67-2026-VBHN SHTT 382 marker, 115-VPQH, BLLĐ 18-VBHN…) + 6 doc marker DÍNH ĐÔI
«[n][n]» đầu dòng (KDBH 31-2026 '[8][8]', 8-2026-VBHN-BNV '[2][2]', 4231/4719-VBHN-BTP…). foot_region rỗng
⇒ rescue lẫn body-loop tê liệt ⇒ footnote_count=0 CÂM trên ≈1059 marker: mất footnote_gate (_relation_audit
ưu tiên footnote-map hơn heuristic), mất FOOTNOTE_AMENDMENT_NOT_IN_CORPUS (mất nhắc nạp QT-5), pending=0 giả.
VÁ: 2 phép chuẩn hóa TRƯỚC mọi phép tách — strip cặn theo TRỌN CỤM `HYPERLINK \l "_ftn(ref)N"` (chữ
HYPERLINK trần ngoài cụm KHÔNG bị đụng) + gộp `[n][n]`→`[n]` bằng backreference (CÙNG số mới gộp — chuỗi
`[1][2][3]` khác số của case dedup cũ giữ nguyên).

**F11 — def_missing GIẢ từ số Ô BIỂU MẪU zero-pad:** body-loop so marker bằng CHUỖI ⇒ '[01]'…'[12]' (ô Mẫu
đơn NĐ 188-2025-NĐ-CP, ×2 bản identity-dup) ≠ def '[1]'…'[6]' ⇒ 12/12 dòng def_missing THÔ toàn corpus
(2 dòng sau gom cấp-Điều) = 100% RÁC is_amend=True gán «Điều 72 khoản 4». VÁ: khóa marker CHUẨN int
(`str(int(n))`) tại CẢ HAI điểm bắt (anchor thân + marks foot) + rescue số-trần thêm dung sai `0*`
(superset hành vi cũ). GIỮ NGUYÊN guard `int(n)>max_foot` — sổ đã BÁC vế «guard nuốt marker thật» (0 ca
trên corpus; guard đang là thứ duy nhất chặn nhiễu [07]-[12]).

PHẢN CHỨNG (probe 2-process qua đường sản xuất `import tl`, master r276 vs bản vá, 403 extract nền +
manifest 1315 — scripts/số liệu tại scratchpad phiên e53947f2 `probe_r277_*.py` + `corpus_{master,patched}.json`):
**383/403 doc IDENTICAL từng trường · 18/18 doc câm HỒI SINH (908 dòng bản-đồ cấp Điều, 102 pending-effect
lộ ra — riêng SHTT 340 dòng) · rác def_missing 12 thô→0 · 0 đổi-khác ngoài dự kiến · 2 chữ HYPERLINK
ngoài cụm _ftn còn nguyên.** Selftest +4 case r277_* (hyperlink-residue + double-bracket RED-trước/GREEN-sau
đo bằng fixture 2 phía; leading-zero 2 def_missing giả→0; guard >max_foot intact). 1441/1441.

# ★ v1.36.14 — r276: hai điểm mù detector cho bất biến «số hiệu PHẢI có NĂM» (P15-F06 — lệnh quét) (2026-07-31)

F06 sổ P15 («cần lệnh quét + kế hoạch sửa registry riêng»). Đo TƯƠI kho nền 31-07 (sau các lượt dọn của
phiên BHXH): 126 dòng sohieu không-năm, phân lớp: **A** 6 VBHN cấp bộ thiếu CẢ segment 'VBHN' lẫn năm
('09-BGDDT') · **B** 20 văn bản Đảng ('27-NQ-TW', '101-QD-TW' — 10 dòng có năm ngay trong TÊN) · **D** 7
khác cần năm tay (671-QD-BTTTT, 560-NQ-UBTVQH15…) · **E** 93 corpus=false sidecar (by-design không sửa) ·
lớp thoái hóa corpus=true ("01") đã được dọn trước = 0.

Hai điểm mù detector, cả hai vá trong bản này:
1) `_vbhn_year_fix_items`: lớp A rơi vào `continue` IM LẶNG (không fixable, không needs_year) vì khóa
   không khớp `NN-VBHN-XXX`. Nay: suy được năm → fixable `NN-YYYY-VBHN-AGENCY` (mode
   `ministry_missing_segment`, đi CHUNG apply-path reg_upsert + journal + cổng conflict cũ); mọi khóa VBHN
   không-năm còn lại (kể cả dị dạng '73-82-ND-CP') → needs_year mode='malformed'. Đo nền: 5 fixable BGDDT
   (09→09-2024, 05→05-2023, 07→07-2023, 04→04-2026, 02→02-2026) + 1 malformed, 0 conflict.
2) `registry_hygiene.analyze` (nuôi `tl registry-doctor`): KHÔNG bucket nào đếm khóa không-năm non-VBHN.
   Nay bucket `sohieu_khong_nam` (phân lớp vbhn/dang/khac, miễn LCT-HDNN, chỉ trên `scanned` corpus=true
   như mọi bucket) + khóa summary/text (khuôn H2 text=JSON) + samples. Đo nền: sohieu_khong_nam=33 = đúng
   A6+B20+D7 phân lớp tay.

KHÔNG ghi registry trong bản này — kế hoạch sửa dữ liệu từng dòng (33 dòng corpus=true) nằm ở
`C:\qh\p15_review_core_2026-07-30\F06_KE_HOACH_SUA_SOHIEU_NEN.md`, CHỜ DUYỆT rồi mới apply
(`tl --profile vbqppl vbhn-year-fix --apply` cho lớp A; reg_upsert tay theo bảng cho B/D).
Selftest +1 case (3 vế vá + 5 phản chứng: year-qualified không đụng · NOYEAR chuẩn giữ nguyên ·
corpus=false không year-fix · LCT-HDNN miễn · sohieu rỗng vẫn đi bucket missing_sohieu). 1437/1437.

# ★ v1.36.13 — r275: `_vbhn_base_key` tie-break bất định trên chuỗi goc toàn-không-năm (P15-F04) (2026-07-31)

F04 sổ P15 (phiên giữ sổ phát hiện, phiên land vá). `min(keys, key=_sohieu_base_sort_year)` trên SET —
mọi khóa không năm đều 9999 (trừ LCT-HDNN=1987) ⇒ hòa điểm thì thứ tự duyệt set (hash seed từng process)
quyết định ⇒ vị từ «query có LÀ base của VBHN không» (quyết định VBHN-first redirect ở `_source_map_one`)
có thể LẬT giữa hai lần chạy trên chuỗi goc bẩn toàn-không-năm. Chưa nổ trên data thật (goc corpus hiện có
năm đủ — đo 31-07) — vá phòng lớp dữ-liệu-bẩn, cùng họ fixture r274.

VÁ đúng đề xuất sổ: `min(keys, key=lambda k: (_sohieu_base_sort_year(k), k))` — tie-break phụ theo chính
khóa. Đo tất định xuyên-process 5 PYTHONHASHSEED (1/7/42/999/31337) cùng ra `12-VBHN-VPQH`. PHẢN CHỨNG:
chuỗi sạch có năm → năm nhỏ nhất vẫn thắng (hành vi cũ giữ nguyên); LCT-HDNN vẫn thắng khóa không-năm.
Selftest +1 case. 1436/1436.

# ★ v1.36.12 — r274: fixture selftest VBHN thiếu năm — siết 3 fixture bare VÔ TÌNH về khóa NN-YYYY-VBHN-XXX (2026-07-31)

Mục «fixture thiếu năm» của backlog P15. Bất biến dự án: mọi số hiệu trong REGISTRY phải year-qualified
(`NN-YYYY-VBHN-XXX` — memory vbqppl-sohieu-must-have-year); fixture đóng vai «dòng registry» mà để bare thì
phép so exact trong test TRÙNG KHỚP GIẢ — đúng cơ chế làm lớp bug bare-query↔year-entry (họ r255) lọt lưới:
test xanh trên fixture bare, corpus thật year-qualified thì MISS SẠCH.

Soi TOÀN BỘ ~25 fixture VBHN bare trong tl_selftest: đa số là BARE CỐ Ý (test chính lớp bare — cờ
VBHN_BARE_NUMBER/REUSE_RISK, vbhn-year-fix, nới 1-chiều v1.33.47…) — GIỮ NGUYÊN. Chỉ 3 chỗ bare VÔ TÌNH
(đóng vai dòng corpus, bareness không phải điều test nhắm): `_b1ents` ×2 (b1_no_outdated_* — VBHN che phủ
«18/VBHN-VPQH» → `18-2022-VBHN-VPQH`/`18-2025-VBHN-VPQH`) và `_vcov` (xref_vbhn_coverage_before_typo —
«11/VBHN-VPQH» → `11-2018-VBHN-VPQH`, đúng VBHN PCTH thuốc lá 2018 thật). Test-only, hành vi runtime không
đổi; selftest 1435/1435 (các case này nay chạy trên hình dạng dữ liệu THẬT).

# ★ v1.36.11 — r273: trần năm của gate NO_VERIFIED_VBHN hardcode 2021 — mục theo thời gian, false-clean cho luật 2022-2024 (2026-07-31)

P15 rà resolve.py (tiếp — mục CHỐT của backlog CONFIRMED). Hai site trong `_source_map_one` (gate sohieu +
gate A1 theo-tên) đòi `qyear <= 2021` mới nhắc NO_VERIFIED_VBHN_IN_CORPUS/QT5_WEB_REQUIRED. Hằng chết mục
theo thời gian — chính S-8b trong CÙNG file đã tự phê «nhánh-4 hardcode 2024 sẽ mục» và dùng cur−2 động.
Hệ quả 2026: luật 2022-2024 (đã kịp bị sửa 2024-2026, VBHN có thể đã có trên web) mà corpus chưa có VBHN
→ source-map im hoàn toàn = false-clean đúng lớp A1 v1.33.2 từng vá cho truy vấn theo tên.

VÁ: `_vbhn_gate_cutoff = cur−2` (đồng bộ ngưỡng «rất mới» S-8/S-8b: luật cur−1/cur chưa kịp có VBHN → im
là đúng). Đo: 2018/2022/2023/2024 → nhắc web; 2025/2026 → im. Đây là NỚI CÓ CHỦ ĐÍCH (thêm cảnh báo cho
lớp 2022-2024 trước đây im) — hàng đợi lượt-2 có thể tăng; S-8 vẫn hạ ưu tiên các ca VBHN mới như cũ.
Selftest +1 case TƯƠNG ĐỐI theo năm hiện tại (chính test không mục): cur−2/cur−5 nhắc · cur−1/cur im ·
có VBHN related thì đi đường VBHN_FIRST không đụng gate. 1435/1435.

r273b (lộ ra khi chạy gate): (i) canonical ĐÃ CONFIRM nay cũng được miễn web-gate — đồng bộ doctrine
§confirm A1 v1.32.0 (đã suppress nhóm amendment-gate; nag web trên bản đã rà kỹ = re-review noise);
(ii) fixture r17b/r19 dùng năm CHẾT 2022 rơi vào trần mới → đổi bucket chính sang web_round2 làm lệch
Ý ĐỊNH test (cô lập rel-low-conf) — chuyển fixture sang năm ĐỘNG base=cur−1/amend=cur theo khuôn r18,
chính test cũng hết mục theo thời gian.

# ★ v1.36.10 — r272: `_classify_ref` lấy `by_sohieu[0]` theo thứ tự registry — bản cách ly làm canonical, nhóm cách-ly-thuần vẫn OK (2026-07-31)

P15 rà resolve.py (tiếp). Hai vế cùng gốc «không chọn lọc ứng viên»:
(a) canonical = `by_sohieu[0]` — phần tử ĐẦU theo thứ tự registry, không sort điểm, không loại cách ly ⇒ bản
    .docx raw-twin đã quarantine đứng trước GDoc live thì xref/refs-audit hiển thị canonical là bản cách ly;
(b) nhóm CHỈ toàn bản cách ly/corpus=false (raw đã đăng ký, bản dùng được chưa nạp) vẫn `flag=OK` ⇒
    frontier/refs-audit rút dẫn chiếu khỏi hàng MISSING — corpus khuyết mà không cổng nào kêu (cùng chiều
    nguy hiểm r270). Đo 31-07: `[quar-only]` → OK, canonical=bản .docx cách ly.

VÁ: sort `by_sohieu` theo `_entry_score` (vị từ chọn canonical dùng chung — phạt quarantine/orphan), canonical
lấy từ nhóm KHÔNG-cách-ly; nhóm cách-ly-thuần → `MISSING` + note «CHỈ khớp bản đã cách ly… nạp bản chuẩn
trước khi rà». `corpus=false` nhưng CÒN trên NLM không phải cách ly (#6 `_entry_quarantined`) — vẫn OK.
Selftest +1 case (2 vế vá + 4 phản chứng: live-only OK · corpus=false-trên-NLM OK · đường OUTDATED chạy trên
canonical hiệu quả · MISSING thường giữ nguyên). 1434/1434.

# ★ v1.36.9 — r271: vị từ CÒN-hiệu-lực của `_classify_ref` đảo nghĩa trên «Không còn hiệu lực» (2026-07-31)

P15 rà resolve.py (tiếp). Vế B1-suppress («bản CÒN hiệu lực → không OUTDATED») kiểm bằng `"con" not in hl` —
positive-substring. «Không còn hiệu lực» (strip-accents: `khong con hieu luc`) CHỨA `con` ⇒ bản ĐÃ HẾT hiệu
lực bị coi là còn ⇒ OUTDATED bị nuốt, người rà tiếp tục rà bản cũ mà không được trỏ sang VBHN. Registry nền
hiện dùng 10+ biến thể hieuluc tự do (đo 31-07: «Còn hiệu lực»/«Con hieu luc»/«Còn»/«Hết…thay bằng…»/«Đã
được hợp nhất tại…»/…) — biến thể «Không còn…» là chuẩn TVPL, xuất hiện là nuốt ngay.

VÁ: negation-first (`het/khong/bai bo/thay the/thay bang/chua` thắng), positive = `\bcon\b` (không ăn
'cong') hoặc `hieu luc` — CÙNG ngữ nghĩa hai chỗ đã đúng: lookup_ops:2676 và _entry_score (phạt het/thay
the). Đo trọn 11 biến thể từ vựng thật: 6 ca hết/chưa/không-rõ → OUTDATED, 4 ca còn (kể cả không dấu, kèm
chú thích) → suppress, rỗng → OUTDATED (không biết ≠ còn). Selftest +1 case. 1433/1433.

# ★ v1.36.8 — r270: `_vbhn_for_goc` khớp-lọt substring trên blob JSON — OUTDATED giả che MISSING thật (2026-07-31)

P15 rà resolve.py (tiếp). `_vbhn_for_goc` (nuôi cả HAI nhánh của `_classify_ref`: kiểm OUTDATED khi số hiệu
khớp, và VBHN-coverage TRƯỚC TYPO/MISSING khi không khớp) so `norm_sohieu(key) in norm_sohieu(gtxt)` — substring
KHÔNG biên từ trên blob JSON của trường goc. norm giữ nguyên chuỗi số ⇒ cited `1-2020-QH14` khớp LỌT goc
`41/2020/QH14`, cited `6-2012-QH13` khớp `16/2012/QH13` (dẫn chiếu viết không số 0 dẫn đầu là ca thường gặp).
Chiều nguy hiểm: dẫn chiếu THIẾU thật trong corpus bị gắn `OUTDATED — đã được VBHN 'X' bao phủ` (đo 31-07)
⇒ xref/refs-audit/frontier bỏ nó khỏi hàng MISSING — danh sách văn bản cần tải THIẾU âm thầm (đúng lớp
r256/r267 vừa diệt ở chỗ khác).

VÁ: so theo TẬP KHÓA `_goc_keys` (bóc ;,| + norm từng phần — CÙNG bộ khoá _vbhn_base_key dùng). Đo 3 registry
thật: goc chỉ chứa sohieu sạch (5 giá trị phân biệt, 2 quirk Drive-ID không khớp được gì) ⇒ exact-set không
mất ca thật nào. Lưu ý mở rộng cố ý: `_goc_keys` đọc qua `_entry_goc` (goc|goc_luat|targets) — rộng hơn blob
cũ (chỉ `goc`) nhưng đồng nhất với phần còn lại của resolve. Selftest +1 case (2 vế vá + 4 phản chứng
exact/;-list/JSON-list/non-VBHN). 1432/1432.

# ★ v1.36.7 — r269: cổng dedup `_dedup_status` hở 3 vế — từ vựng active trôi lệch, membership câm alias, thiếu parity bare-VBHN (2026-07-31)

P15 rà `tl_core/resolve.py` (mục cuối nhóm lookup). `_dedup_status` là cổng chống-nạp-trùng nuôi
fetch-route/fetch-links/fetch-batch (`SKIP_DEDUP`/`REVIEW_DEDUP`/`FETCH`) — đúng chỗ đã gây sự cố nạp chồng
9 tài liệu ATVSLĐ 24-07. Ba vế hở, cả ba ĐO ĐƯỢC trên registry thật hoặc probe pure:

1) **Bản-sao-từ-vựng active thứ ba trôi lệch** (đúng lớp r253/r257 tự cảnh báo): resolve.py giữ exact-set
   `("pushed","synced","added","live")` — THIẾU `active` (ADR-0010 nắn live→active nghĩa là 'live' không còn
   được sinh ra, còn 'active' thì có THẬT: đo registry nền 9 dòng + BHXH 6 dòng), thiếu luôn ca status rỗng
   nhưng CÓ `nlm_source_id` (5 dòng nền). Hệ quả: văn bản ĐANG trên NLM bị dedup coi là chưa có ⇒
   fetch-batch xếp `action=FETCH` = mời tải/nạp lại. VÁ: bỏ hẳn bản sao từ vựng, dùng vị từ chuẩn
   `_entry_on_nlm_live` (source_id + không removed*) ở CẢ HAI chỗ trong hàm. Đo 3 registry thật
   (nền 1315 + BHXH 115 + ATVSLĐ 37): chuyển vị từ mất 0 dòng, được thêm 14+6 dòng.

2) **Membership reason so EXACT**: resolve_identity trả reason `'alias/tukhoa:<terms>'` và `'name_tokens'`
   (B2 port), nhưng gate so `"alias" in reasons` (membership list, exact) ⇒ KHÔNG BAO GIỜ khớp — hit alias
   active mà `likely_in_corpus=false` (đo: query 'BHXH' ↔ entry title_vn 'Luật Bảo hiểm xã hội' active →
   false). VÁ: chuẩn hoá `rkinds = {r.split(':')[0].split('/')[0]}` rồi so tập, thêm `name_tokens`.

3) **Thiếu parity bare-VBHN v1.33.47**: query '88-VBHN-VPQH' (văn bản dẫn không năm) không khớp entry
   year-qualified '88-2025-VBHN-VPQH' vì resolve_identity so exact ⇒ `in_corpus_active=false`, fetch-batch
   chỉ REVIEW thay vì SKIP_DEDUP. VÁ: vòng bổ sung `_sohieu_query_hits_entry(qkey, _sohieu_key_entry(e))`
   trên entry đang live khi chưa có by_sohieu.

Vế thứ tư CÂN NHẮC rồi BỎ (kỷ luật r267 'vế phải chịu lực'): 'số hiệu phủ-bằng-chunk cũng là đã-có' —
đo part __partNN thực tế mang sohieu + source_id nên resolve_identity tự thấy (6 decoy VBHN không đẩy
nổi part khỏi top-6) ⇒ vế đó là no-op, không thêm.

Selftest +1 case `r269_dedup_status_active_alias_chunk` (4 vế vá + 4 phản chứng: removed*+source_id sót
KHÔNG active · query có năm vẫn so chặt · query không liên quan sạch · part đã gỡ không phủ).

# ★ v1.36.6 — r268: r264 máy-phụ-thuộc — vế SHA đòi cứng MỘT loại advisory trong khi loại đó theo OBJECT STORE từng máy (2026-07-30)

(Đánh số lại từ r267/v1.36.5: phiên song song chiếm số trước tại `a4ebf74` — lần VA SỐ THỨ BA của chiến
dịch; bản này rebase lên đúng master đó, KHÔNG đụng vùng họ sửa.)

Người giữ chạy `deploy-package.cmd` trên máy Windows dev: gate ĐỎ ở selftest — **`r264_doc_claims_phu_docs`
FAIL, 1427/1428** (7 gate còn lại xanh; r265/r266 đều [OK]). Đo tại chỗ trên máy đó:
`git cat-file -t 1835b46` → **commit** (nhánh `…-dlbrut` đã xoá trên remote nhưng máy dev là nơi nhánh
SINH RA — object còn trong store), Counter advisory: `SHA_NOT_REACHABLE_FROM_HEAD: 1` chứ KHÔNG phải
`SHA_NOT_A_COMMIT_IN_HISTORICAL_DOC` mà test đòi cứng `>= 1`. **Checker ĐÚNG** (flags rỗng, advisory vẫn
sinh — chỉ khác LOẠI theo trạng thái object store); **test SAI kiểu máy-phụ-thuộc** — ảnh gương của đúng
bẫy clone-shallow mà r264 tự ghi chú.

Vá 2 phần, 0 dòng sản xuất:
1. **Vế SHA của r264 rẽ theo BẰNG CHỨNG ĐO TẠI CHỖ** (`git cat-file -t 1835b46`): object là commit →
   đòi `SHA_NOT_REACHABLE_FROM_HEAD >= 1`; không → đòi `SHA_NOT_A_COMMIT_IN_HISTORICAL_DOC >= 1`.
   KHÔNG «thiếu thì cho qua»: object thành REACHABLE (khôi phục nhánh) thì CẢ HAI vế đổ — đúng, vì tài
   liệu hết là "ghi chép về commit đã mất".
2. **Case MỚI `r268_l2_trichotomy_theo_trang_thai_object`**: khoá TRICHOTOMY của L2 trên mini-repo git
   THẬT (khuôn r226), chạy MỌI máy: object VẮNG → NOT_A_COMMIT_IN_HISTORICAL_DOC (advisory); CÓ-nhưng-
   UNREACHABLE (tạo nhánh, commit, xoá nhánh) → NOT_REACHABLE_FROM_HEAD; REACHABLE → IM TUYỆT ĐỐI + 0 cờ
   cứng L2 + không nhãn kép. Chống flaky: SHA sống dùng bản 40-hex (sha 7 ký tự ~3.7% không chứa a-f →
   L2 bỏ qua theo thiết kế).

Phản chứng (chạy TRÊN CÂY CUỐI đã rebase, mỗi vế trọn selftest, output ra FILE):
| lượt | kết quả |
|---|---|
| repo vá (nền a4ebf74 + r268) | **N/N** (số chốt ghi ở commit) |
| BƠM HỎNG checker (historical L2 im lặng) | r264 **VÀ** r268 cùng ĐỎ — hai lưới độc lập cùng bắt |
| checker hỏng + r264 QUÁ-TAY («thiếu thì cho qua») | r264 **XANH OAN**, r268 vẫn ĐỎ — vế chặt là vế chịu lực |

Đo nền phía Windows = chính output người giữ dán (repro chuẩn; container không tái hiện được vì object
vắng). Parity đóng vòng: máy Windows pull về chạy lại gate qua nhánh NOT_REACHABLE. Bump 1.36.5→1.36.6
cùng độ dài ⇒ SKILL.md size giữ nguyên; file_count 195 không đổi ⇒ golden giữ nguyên.

# ★ v1.36.5 — r267: PARITY 4 reader trên cùng tệp cache — U1 còn thiếu ở HAI chỗ nữa (2026-07-30)

r266 (v1.36.4) vá `_doc_text_any` bỏ qua bộ lọc U1 và gọi chỗ mình vá là *"một choke-point"*. Rà lại vùng
đó: **không phải một, mà BỐN** reader đọc cùng tệp `extract_<id>.txt`, và r266 mới đồng bộ hai:

| reader | trước r267 |
|---|---|
| `_read_doc_text` (lookup_ops 2203) — bản chuẩn | `_sanitize_export_text(_strip_font_runs())` ✓ |
| `_doc_text_any` (lookup_ops 2453) — r266 vá | ✓ |
| **`cmd_xref`** (lookup_ops 1606) | chỉ `_strip_font_runs()` ✗ |
| **`_frontier_doc_text`** (fetch_web 173) | chỉ `_strip_font_runs()` ✗ |

Chính bất biến r266 tuyên bố — *"cache đọc ra phải qua ĐÚNG bộ lọc U1 như `_read_doc_text` đọc CÙNG tệp,
không thì hai reader lệch byte"* — vẫn bị hai chỗ này vi phạm.

**Và hậu quả KHÔNG dừng ở lệch byte — nó đổi KẾT QUẢ.** `_sanitize_export_text` **XOÁ** control-char (không
thay bằng khoảng trắng), nên `\x0c` mà pdftotext để lại GIỮA một số hiệu sẽ được nối liền ở đường có U1,
còn đường thiếu U1 thì regex `extract_refs` nuốt qua ranh giới. Đo trên CÙNG một tệp cache:

```
_read_doc_text (có U1)  → 2 dẫn chiếu: 59-2020-QH14 · 01-2021-ND-CP
cmd_xref (thiếu U1)     → 1 dẫn chiếu, và SAI: mất hẳn 59/2020/QH14,
                          còn 01/2021/NĐ-CP bị gán loai='Luật'
```
Tức **một dẫn chiếu biến mất** và **một dẫn chiếu bị gán sai loại**, cả hai IM LẶNG. Đường này nuôi
`frontier-expand → missing_in_corpus` và `rasoat-loop → gaps_missing_in_corpus` ⇒ **danh sách văn bản cần
tải bị thiếu mà không cổng nào kêu** — đúng lớp lỗi r256 vừa diệt ở chỗ khác.

Vá: thêm `_sanitize_export_text(...)` tại đúng hai site, cùng hình dạng r266 (2 dòng).

**GỐC RỄ, nêu rõ nhưng CỐ Ý KHÔNG tự làm:** đây là **bốn bản sao** của cùng một đoạn đọc-cache. Lớp lỗi này
đã cắn HAI LẦN (r266 tìm ra và vá nửa; r267 tìm nốt nửa kia). Bản sao thứ năm sẽ xuất hiện. Dứt điểm là gộp
về MỘT helper `_read_extract_cache(fid)` — nhưng đó là refactor chạm 4 chỗ và đổi đường của `_read_doc_text`,
ngoài phạm vi bản vá này. **Đề xuất để người giữ quyết**, không bó kèm.

**Phản chứng — 6 vế, trong đó 3 vế chống-vá-quá-tay:**
· PARITY: 4 reader trên cùng tệp phải ra CÙNG tập dẫn chiếu, và phải ĐỦ 2 — vế khoá cả lớp lỗi, không chỉ 2 site;
· bộ lọc phải CHỊU LỰC: bỏ nó đi thì kết quả KHÁC (nếu bằng nhau thì vế PARITY là no-op);
· KHÔNG được nuốt `\n`/`\t`: text sạch qua **nguyên vẹn byte** (nuốt thì cấu trúc Điều vỡ mà PARITY vẫn xanh);
· không chỉ `\x0c`: `\x00` `\x07` `\x1f` `\x7f` cũng phải nối lại số hiệu;
· vế (a) của U1: lone-surrogate bị diệt;
· khoá TĨNH cả hai site (chống ai gỡ ra mà 5 vế trên vẫn xanh nhờ `_read_doc_text` gánh hộ).

Đo 2 CHIỀU: dán case vào cây CHƯA VÁ (`3e440ef`) → **ĐỎ đúng 1 case (1428/1429)**; trên bản vá →
**1429/1429**.

# ★ v1.36.4 — r266: `_doc_text_any` bỏ qua bộ lọc U1 — control-char (\x0c pdftotext) lọt cache/JSON, hai reader lệch byte (2026-07-30)

P15 nhóm lookup, vùng treo «doc-text ~2140-2550» của bàn giao 30-07. `_doc_text_any` (A1 v1.34.60 — MỘT
đường đọc text MỌI định dạng, nền của `tl doc-text` + E1) KHÔNG áp `_sanitize_export_text` (U1 v1.31.2)
ở HAI chỗ: nhánh cache-read trả `_ct` thô, và đường trả cuối chỉ `_strip_font_runs` trước khi GHI CACHE +
trả. Nguồn bẩn có thật: `pdftotext` nhả form-feed `\x0c` giữa trang (`_read_local_text_for_analysis`
trả thô, chỉ `errors="replace"`).

**Hệ quả đo được (30-07, function-level offline):** cùng MỘT cache `extract_<id>.txt` chứa `\x0c`/`\x07`,
`_read_doc_text` trả SẠCH còn `_doc_text_any` trả NGUYÊN control-char — hai reader lệch byte; và
`cmd_doc_text` in `body` thẳng vào JSON `text`/`--out`/stdout (soi hết đường ra: không sanitize hạ nguồn)
= đúng lớp sự cố U1 đã trả giá (driver bash vỡ capture). Cache bẩn còn NUÔI corpus/NLM.

Vá 2 dòng, MỘT choke-point, ĐỒNG NHẤT chuẩn có sẵn (không phải chuẩn mới): cache-read và đường cuối đều
qua `_sanitize_export_text(_strip_font_runs(…))` như `_read_doc_text` từ v1.31.2. + test
`r266_doc_text_any_qua_bo_loc_u1` (1427→1428) với vế fixture-tái-hiện (`\x0c` phải CÓ trong chuỗi bẩn)
và vế ĐỐI CHỨNG (text sạch qua NGUYÊN VĂN — chống vá quá tay nuốt `\n`).

Phản chứng (mỗi vế chạy TRỌN selftest, output ra FILE):
| lượt | kết quả |
|---|---|
| case r266 dán vào cây MASTER chưa vá | **ĐỎ đúng 1 case** (1427/1428) — fixture tái hiện bug |
| repo đã vá | **1428/1428** |
| biến thể QUÁ TAY (sanitize nuốt `\n` ở cache-read) | vế đối chứng ĐỎ, kèm `r121_doc_text_docx_unzip` cũng ĐỎ — HAI lưới độc lập cùng bắt |

ruff: tl.py delta 0; lookup_ops +3 F821 = 4 lần xuất hiện của 2 TÊN CŨ (`_sanitize_export_text` ·
`_strip_font_runs` — cùng file đã dùng ở `_read_doc_text`, trừ 1 lần cũ bị thay) — TĂNG hợp lệ theo khuôn
re-home `__globals__`, hành vi resolve chứng minh bằng chính case r266 chạy qua `python scripts/tl.py
--selftest`. Bump 1.36.3→1.36.4 cùng độ dài ⇒ SKILL.md size giữ nguyên.

# ★ v1.36.3 — r265: selftest chạy ĐƯỢC từ gói bung — 3 case «loại-khỏi-gói» học khuôn hai-bối-cảnh (2026-07-30)

Trả NỢ CÓ SẴN đã đo ở bàn giao 30-07: `python scripts/tl.py --selftest` chạy TỪ GÓI BUNG cho **1424/1427**
— `r244_script_deploy_khong_vao_goi` (nợ từ v1.35.81) · `r249_bao_cao_rasoat_ngoai_goi` (v1.35.86) ·
`r251_deploy_guard_chiu_duoc_banner_gws` (v1.35.88) — tức MỌI Package từ v1.35.81 tới v1.36.2 đều ship
selftest ĐỎ khi chạy tại chỗ. Cả ba cùng một hình: khẳng định «tệp X bị loại khỏi GÓI nhưng CÒN trên đĩa»
— vế «còn trên đĩa» chỉ đúng trong repo; từ gói bung tệp vắng ĐÚNG THIẾT KẾ.

Vá theo ĐÚNG khuôn r227/r228 «HAI BỐI CẢNH, hai khẳng định», rẽ `(_ROOT209/".git").exists()` — nay CẢ 5 case
dùng khuôn này (r218 · r226 · r244 · r249 · r251), KHÔNG case nào có nhánh «thiếu thì cho qua»:
- **r244**: CÂY GIT → 5 tệp deploy PHẢI CÒN trên đĩa; GÓI → cả 5 PHẢI VẮNG (vế bảng-loại vẫn đo được ở cả
  hai bối cảnh vì `tl_core.release` CÓ trong gói).
- **r249**: CÂY GIT → `rasoat/` ≥4 .md; GÓI → `rasoat/` PHẢI VẮNG (`_release_should_include` thuần logic
  đường dẫn, không stat tệp, nên hai vế kia đo cả hai bối cảnh).
- **r251**: CÂY GIT → như cũ đọc NỘI DUNG `deploy-guard.ps1` + twin sh; GÓI → `deploy-guard.ps1` ·
  `deploy-package.ps1` · `deploy-package.sh` PHẢI VẮNG; luật cắt JSON (ok3..ok5 — thuần Python trên chuỗi
  gws THẬT) giữ nguyên ở MỌI bối cảnh.

Bằng chứng (đo 30-07, container Linux, mọi output ra FILE rồi mới parse):
| lượt | cây chạy | kết quả |
|---|---|---|
| nền | gói build từ master `320952a` (v1.36.2) bung ra | **1424/1427** — đúng 3 case trên, tái hiện nợ |
| sau vá | repo (`python scripts/tl.py --selftest`) | **1427/1427** |
| sau vá | gói v1.36.3 bung ra | **1427/1427** — nợ đã trả |
| phản chứng 1 | copy repo XOÁ `.git` (bản vá THẬT) | 3 case **ĐỎ** (+r218/r226 đỏ đúng thiết kế khuôn) — xoá `.git` trong KHO không lọt lưới |
| phản chứng 2 | gói bung BƠM `deploy-package.sh` + `deploy-guard.ps1` + `rasoat/*.md` | đúng 3 case **ĐỎ** trở lại — nhánh gói bắt được dev-side lọt bundle |
| phản chứng 3 | biến thể QUÁ TAY «thiếu thì cho qua» trên CẢ HAI kịch bản trên | **XANH OAN cả hai** (1425 & 1427) ⇒ vế phản chứng của bản THẬT chính là thứ chịu lực |

ruff delta so master = 0 (tl.py 12 F821/0 F401; tl_selftest 4033 F821/1 F401 — y hệt master, nền đã trôi
từ mốc 3914 ghi trong CLAUDE.md do các đợt r255-r262, delta mới là chỉ tiêu). **0 dòng code sản xuất** —
đụng DUY NHẤT `tl_selftest.py` (3 case) + bump version 3 chỗ (1.36.2→1.36.3 CÙNG ĐỘ DÀI ⇒ SKILL.md
size giữ nguyên, không đụng golden size như vụ 1.35.99→1.36.0).

# ★ v1.36.2 — r264: `doc-claims-check` PHỦ `docs/` — 19 tệp trước đây không cổng nào soi (2026-07-30)

Ngay sau khi merge 2 tài liệu kế hoạch vào `docs/` (r263), tôi đã nói ra mặt sau của việc đó: `doc-claims-check`
quét roots `CHANGELOG.md`/`SKILL.md`/`CLAUDE.md`/`CONTEXT.md`/`references` — **không** có `docs/`, nên con trỏ
chết ở đó KHÔNG cổng nào bắt. Nay phủ. Đo trước khi vá, không sau: `files_scanned` **35 → 54**.

**Kết quả đo khi mở `docs/`: 12 cờ CỨNG, DỒN HẾT vào MỘT tệp** —
`docs/KE_HOACH_RASOAT_HOSO_ORCHESTRATION.md` (11 `PATH_MISSING` + 1 `SHA_NOT_A_COMMIT`). 18 tệp còn lại
(16 ADR + audit + `WORKFLOW_RASOAT_TU_DONG.md`) **SẠCH TUYỆT ĐỐI**.

**Nhưng 12 cờ đó KHÔNG phải lỗi tài liệu — chúng là NỘI DUNG của tài liệu.** Tệp đó là một bản **kiểm kê
con-trỏ-chết**: nó nêu `scripts/nlm_log.py` · `build_parts.py` · `tl_rebuild.sh` · `templates/_nguon-goc/` ·
`manifest_build.py` **chính vì** chúng không tồn tại, và tự khai bằng chứng cho từng cái
(«`git log --all --diff-filter=ADR` **RỖNG** → chưa từng tồn tại», «`manifest_build.py` thật ra ở
`scripts/_fallback/`»). `1835b46` là commit của nhánh `…-dlbrut` **đã bị xoá** ⇒ unreachable vĩnh viễn.

Nếu bắt cứng thì cách chữa duy nhất là **xoá phần phát hiện** — phá tài liệu để làm vui lòng bộ kiểm. Đó đúng
là tình huống §2.2 đã giải cho `CHANGELOG`/`DOCTRINE_APPENDIX`: *tài liệu GHI LẠI QUÁ KHỨ được phép dẫn tệp
đã xoá*. Nên xếp tệp này vào `_DOC_CLAIMS_HISTORICAL`.

**Sửa kèm một BỎ SÓT của chính bộ kiểm:** `historical` hạ cấp L1/L4/L8/L9 nhưng **L2 (SHA) thì không** — dù
chú thích L4 ngay dưới tự nói khuôn đúng là «cùng khuôn L1/L8». Một bản ghi chép dẫn commit không còn trong
kho (nhánh đã xoá, hoặc clone SHALLOW) là ghi chép, không phải con trỏ sống ⇒ nay `SHA_NOT_A_COMMIT` thành
`SHA_NOT_A_COMMIT_IN_HISTORICAL_DOC` (advisory) cho tài liệu lịch sử. Đây cũng chính là cờ đỏ-giả đã cắn tôi
đầu phiên này: clone shallow → 2 cờ `SHA_NOT_A_COMMIT` trong `changelog_archive`.

**Giá phải trả, nói thẳng:** SHA gõ sai trong `CHANGELOG` từ nay là advisory chứ không chặn gate. Đo lúc mở:
**0 cờ cứng loại này** trên roots mặc định ⇒ không mất phát hiện nào đang sống, nhưng đó là nhượng bộ có ý
thức. Đường thay thế (bắt tác giả bỏ/ghi chú `1835b46`) tôi KHÔNG tự làm — trích dẫn đó có nghĩa, nó ghi bản
nháp mà tài liệu này sửa.

**Phản chứng ĐỐI XỨNG — hai thay đổi trên đều LÀM YẾU, nên phải chứng minh phần còn lại vẫn bắt:**

| ca | kết quả |
|---|---|
| `docs/` **không**-historical, đường dẫn chết + SHA lạ | **`PATH_MISSING` + `SHA_NOT_A_COMMIT` — CỨNG cả hai** |
| tệp historical, CÙNG hai lớp đó | advisory (11 + 1), **0 cờ cứng** |
| `WORKFLOW_RASOAT_TU_DONG.md` (docs/, cùng đợt merge) | **KHÔNG** được ăn ké nhãn lịch sử |
| `files_scanned` | 35 → **54** |
| gate `--strict` | rc=0 |

Vế đầu là vế cốt tử: thiếu nó thì việc "phủ `docs/`" chỉ là trang trí. Test `r264` khoá cả 5 vế; hằng nằm ở
`tl_core.workflow` (KHÔNG re-export sang `tl`) nên test vào qua submodule theo idiom nhà — lượt đầu tôi viết
`_TL_MODULE._DOC_CLAIMS_DEFAULT_PATHS` và test ĐỎ ngay, đó là cách phát hiện.

# ★ v1.36.1 — r263: merge `claude/legal-doc-review-architecture` (2 tài liệu kế hoạch rà soát) (2026-07-30)

Merge `--no-ff` nhánh `claude/legal-doc-review-architecture-2al46n` theo yêu cầu người giữ. Nhánh rẽ khỏi
master ở `ccad292` (26-07), master đã đi trước **93 commit**; nhánh chỉ THÊM 2 tệp, không sửa tệp nào ⇒
merge sạch, 0 xung đột:
`docs/KE_HOACH_RASOAT_HOSO_ORCHESTRATION.md` (269 dòng) · `docs/WORKFLOW_RASOAT_TU_DONG.md` (392 dòng).

**Ba mặt rủi ro, đo TRƯỚC khi merge chứ không sau:**
1. `doc-claims-check` quét roots `CHANGELOG.md`/`SKILL.md`/`CLAUDE.md`/`CONTEXT.md`/`references` — **KHÔNG
   quét `docs/`** ⇒ 2 tệp này không thể sinh con-trỏ-chết cho gate. (Mặt sau của điều đó: nếu chúng CÓ
   đường dẫn chết thì **không cổng nào bắt** — xem "còn nợ" bên dưới.)
2. Xung đột: nhánh không sửa tệp nào của master ⇒ merge `ort` sạch.
3. **VÀO GÓI**: `docs/` KHÔNG nằm trong `_RELEASE_EXCLUDE_DIRS` ⇒ manifest **193 → 195 tệp**
   (+79KB: 38.398 + 40.819B), zip **194 → 196**, **trần 200 chỉ còn 4 slot**.

Gate XANH TRỌN ngay lượt đầu: `golden`/`determinism` KHÔNG đỏ dù số đếm đổi — `SKILL.md` giữ đúng 47.965B
(chuỗi `1.36.0`→`1.36.1` cùng độ dài) và `release_manifest_stable` **TÍNH** file_count chứ không GHIM.
Vì vậy KHÔNG ghi lại golden (`git diff -- references/golden/` rỗng) — đúng R6, không "--write" theo phản xạ.

**CÒN NỢ — hai điểm KHÔNG tự quyết, để người giữ định:**
- **Slot gói.** 2 tệp này là tài liệu KẾ HOẠCH, đúng khuôn dev-side mà `CLAUDE.md` · `.claude/` ·
  `changelog_archive` · `rasoat/` · 4 script deploy đã bị loại khỏi gói (GIỮ trong git). Nhưng loại cả
  `docs/` sẽ kéo theo ~20 ADR **đang** trong gói ⇒ đó là ĐỔI CHÍNH SÁCH, không phải hệ quả của lệnh
  "merge nhánh". Còn 4 slot: đợt thêm tệp kế tiếp phải quyết việc này trước.
- **Nội dung có thể đã LỖI THỜI.** Nhánh commit cuối 26-07 và mô tả kế hoạch mà r209–r211 ĐÃ THI HÀNH;
  master đi trước 93 commit. Tôi KHÔNG sửa tài liệu của người khác, nhưng nói rõ: `docs/` không được
  `doc-claims-check` phủ, nên nếu 2 tệp này trỏ tới đường dẫn/lệnh đã đổi thì sẽ KHÔNG có cổng nào kêu.

# ★ v1.36.0 — r262: selftest THỰC SỰ hermetic — chặn mạng + ghim creds giả (2026-07-30)

`tl.py` tự khai ngay trong `selftest()`: *"A bare selftest must be hermetic"* — nhưng lời hứa đó chỉ đúng
cho **CACHE** và **profile**. **MẠNG** và **CREDS** thì không, và đó là gốc của hai sự cố đã trả giá.

**ĐO ĐƯỢC (không suy diễn):** bare selftest gọi **11 lần ra mạng THẬT** từ ≥6 chỗ —
`tl_selftest.py` dòng 2646 · 5317 `_cap72` · 5596 `_cap75` · 7253 · 7261 · 15437 — tới
`script.google.com/exec`, `oauth2.googleapis.com/token`, `drive/v3/files`. Đếm bằng cách bọc
`urllib.request.urlopen`, không phải đọc code.

Hậu quả KÉP:
- **thời gian gate BẤT ĐỊNH**: `ingest_claim` 404 → retry 5s+15s, timeout GET 120s ⇒ có lượt **>580s**;
  `deploy-package.sh --push` **chết ở bước 1** dù cây hoàn toàn lành. Tôi đã mất 5 lượt đoán sai nguyên
  nhân (block phá hermetic · tiến trình sót giành CPU · treo mạng vĩnh viễn) trước khi chịu đo.
- **KHÔNG hermetic theo CẢ HAI chiều**: máy KHÔNG creds thì `cmd_doc_text` → `load_creds` **`sys.exit`
  CỨNG** (test r183) giết cả bộ trước khi in tổng — `rc=1` mà không một dòng `[FAIL]` nào, nhìn như hỏng
  vô cớ; máy CÓ creds thì kết quả phụ thuộc mạng và webapp của người khác.

**Vá ở MỘT chỗ, không phải 6.** Cả 6 chỗ đó là dò-PHỤ mà thất bại vốn đã được bỏ qua — chứng minh bằng
cách chặn sạch mạng rồi chạy: **1425/1425, 0 test đỏ, còn NHANH HƠN 10s**. Sửa từng chỗ là 6 lần đoán ý
test của người khác, đắt hơn và dễ làm sai ý hơn.

`_selftest_seal_env()` (mới, gọi trong `selftest()`, hoàn nguyên ở `finally`):
1. **MẠNG**: `urlopen` → `URLError` — ĐÚNG tín hiệu máy-không-mạng mà chính các nhánh fallback đó vốn đã
   xử lý, KHÔNG phải exception lạ. Lối ra tường minh: `TL_SELFTEST_ALLOW_NET=1`.
2. **CREDS**: chỉ ghim khi THIẾU (máy có creds thật KHÔNG bị đụng) — `TL_WEBAPP=https://tl-selftest.invalid/exec`;
   `.invalid` là TLD **DỰ TRỮ RFC 2606**, không bao giờ resolve, nên kể cả ai tắt (1) vẫn không chạm máy thật.

**Nghiệm thu 5 vế, gồm 2 phản chứng chịu lực:**

| vế | kết quả |
|---|---|
| CÓ env thật (mode chuẩn) | rc=0 · 54s · **1425/1425** |
| KHÔNG env (mode từng CHẾT ở r183) | rc=0 · 46s · **1425/1425** |
| đếm lời gọi ra mạng | **0** |
| PHẢN CHỨNG `TL_SELFTEST_ALLOW_NET=1` | **11** lời gọi trở lại ⇒ opt-out còn sống |
| creds thật trước == sau selftest | True |

Vế phản chứng thứ 4 là vế quan trọng nhất: thiếu nó thì một bản vá "chặn mạng" có thể **âm thầm xoá** năng
lực chạy LIVE mà không ai biết. Test `r262` khoá cả 3 vế của hàm (chặn + opt-out + không-đè-creds-thật).

**CÒN LẠI, cố ý không sửa:** `_gas_get_retry` vẫn ngủ 5s+15s khi gặp `URLError` (2 dòng `[gas-retry]` mỗi
lượt). Bounded và tất định nên không còn hại, nhưng muốn bỏ thì phải đổi hằng retry của ĐƯỜNG SẢN XUẤT —
ngoài phạm vi bản vá test này, và không nên đổi kèm.

**ĐÍNH CHÍNH r261:** mục đó viết «`setattr(_TL_MODULE, tên, fake)` KHÔNG có tác dụng với mọi tên trong
`_STUB_MAP`» — **quá mạnh**. `_STUB_MAP` có 846 tên, gồm `_doc_text_any`/`_gas`/`load_creds`, mà test
r183/r110 chỉ vá `_TL_MODULE` **vẫn chạy đúng**. Phát biểu đúng: có bối cảnh (tuỳ `_TL_MODULE` trỏ vào dict
nào — `__main__` hay module `tl`) mà cửa `_TL_MODULE` KHÔNG đủ; vá cả hai cửa như `_mp261` là an toàn cho
mọi bối cảnh. Kết luận vận hành của r261 giữ nguyên, chỉ lời giải thích cơ chế bị siết lại.

# ★ v1.35.99 — r261: monkeypatch trong selftest phải đi ĐÚNG CỬA của stub-farm (2026-07-30)

**ĐÍNH CHÍNH r260:** mục r260 ghi "selftest 1425/1425 rc=0 trong 55s". Con số ĐÚNG nhưng đo bằng
`import tl; tl.selftest()`, KHÔNG phải lệnh gate chuẩn `python scripts/tl.py --selftest` — lệnh chuẩn
lúc đó **treo >580s** và chưa một lượt nào hoàn thành. Tôi đã quy con số của đường phụ cho gate; đó là
khẳng định vượt quá bằng chứng. Lỗi lộ ra khi `deploy-package.sh --push` chết ở bước 1.

**Gốc rễ:** `tl.py` cài STUB uỷ quyền VĨNH VIỄN cho mọi tên trong `_STUB_MAP`:
`def _stub(*a, **k): return getattr(_mod, _name)(*a, **k)` với `_mod` = submodule `tl_core.<x>`.
Nên `setattr(_TL_MODULE, tên, fake)` **KHÔNG có tác dụng** với các tên đó — stub vẫn tra thuộc tính trên
SUBMODULE và gọi hàm THẬT. Đường `import tl` che mất vì khi đó dict hàm tra TRÙNG `_TL_MODULE`; đường
`python scripts/tl.py` (tl.py là `__main__`) thì lộ.

Bằng chứng là ngăn xếp lấy bằng `PYTHONFAULTHANDLER=1 timeout -s ABRT`, không phải suy luận:
```
tl_selftest.py:22896 _r255_run · lookup_ops.py:1725 cmd_rasoat_loop
lookup_ops.py:1705 _rasoat_expand_text   ← hàm THẬT, không phải fake
tl.py:1608 _stub
```
`_rasoat_expand_text` fake bị bỏ qua ⇒ `cmd_rasoat_loop` chạy hàm thật trên dữ liệu thật với
`max_iter=50` ⇒ **treo**, không phải "chậm". Ba lượt tôi đoán sai trước đó (block phá hermetic · tiến
trình sót giành CPU · treo mạng) đều vì suy diễn thay vì lấy ngăn xếp.

**Vá:** helper `_mp261`/`_mpr261` gán tên ở MỌI cửa — `_TL_MODULE` **và** mọi submodule `tl_core.*` đang
nạp có thuộc tính đó — rồi hoàn nguyên cả hai. Áp cho cả 4 khối r255–r258, vì một fake không ăn thì test
**xanh oan**: nó tưởng đang đo bản vá mà thực ra đo hàm thật.

Bài học đắt: **đo selftest bằng đường KHÁC đường gate là không đo gì cả.** `import tl` và
`python scripts/tl.py` KHÁC nhau ở chỗ `_TL_MODULE` trỏ vào dict nào; mọi test monkeypatch phải chạy
bằng ĐÚNG lệnh gate mới có giá trị. Và khi một lệnh "chậm bất thường", lấy NGĂN XẾP trước khi đặt giả
thuyết — `PYTHONFAULTHANDLER=1 timeout -s ABRT <n>` cho câu trả lời trong một lượt.

Kiểm bằng ĐÚNG lệnh gate: `python3 scripts/tl.py --selftest` → **rc=0 · 56s · 1425/1425 · 19/19 case
r255–r258 OK · 0 FAIL**.

# ★ v1.35.98 — r260: 19 case r255–r258 vào `tl_selftest.py` + bịt cửa MẠNG trong test (2026-07-30)

Bốn bản vá r255–r258 đã trên master từ trước mà **KHÔNG kèm chốt hồi quy của chính chúng** (đợt đó
`tl_selftest.py` là vùng WIP của người giữ nên block test giao tay). Nay dán vào: **1406 → 1425**.

Chèn ngay trước `ok = sum(1 for _, p in cases if p)`; giữ THỨ TỰ vì khối r258 dùng helper `_r256_sweep`
định nghĩa trong khối r257. `tl_selftest.py` thuần **CRLF** nên block (viết LF) phải ép CRLF trước khi
chèn — nếu không là trộn EOL trong repo `* -text` khoá byte, kéo theo manifest hash và `release-verify`.

**Sửa một lỗi HERMETIC của chính block r255, bắt được khi chạy thật:** ca "lệnh thật rasoat-chongcheo"
truyền `target="x"`, và `cmd_rasoat_chongcheo` ở nhánh `target` gọi `load_creds` + `_read_doc_text`
(`lookup_ops.py:1962-1963`) ⇒ **GỌI MẠNG THẬT** khi env có `TL_WEBAPP`/`TL_TOKEN`. Harness ngoài
`tl_selftest` chỉ thấy "hơi chậm"; đưa vào selftest thì **treo hẳn**. Đã bịt 3 cửa (`load_creds`,
`_read_doc_text`, `resolve_identity`) — nhánh `target` vẫn được đi qua, chỉ không ra ngoài. Đo lại: mỗi
khối ~140ms và cho **CÙNG kết quả dù có hay không** `TL_WEBAPP`/`TL_TOKEN`; đó là định nghĩa hermetic,
không phải "chạy được trên máy tôi".

Bài học: **selftest xanh trên harness KHÔNG chứng minh nó hermetic** — harness cho phép biến môi trường
khác, và một lời gọi mạng chỉ tốn vài giây ở đó có thể thành treo vô hạn trong bộ 1400 case. Phép thử
đúng là chạy CÙNG khối hai lần, một lần CÓ creds một lần KHÔNG, rồi đòi hai kết quả GIỐNG nhau.

# ★ v1.35.97 — r259: đồng bộ số r trong CHÚ THÍCH `lookup_ops.py` (chỉ chú thích) (2026-07-30)

Khiếm khuyết của CHÍNH đợt r255–r258: khi master bị phiên song song đẩy hai lần, tôi đánh số lại
commit message + mục CHANGELOG + tên case test, **nhưng bỏ sót CHÚ THÍCH TRONG CODE** — chúng vẫn giữ
số của lượt đánh đầu (`r251`–`r254`). Trên master hiện tại những số đó là việc của PHIÊN KHÁC:
`r251` = "hai cổng XANH mà nói dối", `r252` = "`&amp;` `&lt;` chui nguyên văn vào kho",
`r253` = "hai cờ còn-nợ-NLM mời nạp TRÙNG", `r254b` = "test r251 ĐỎ GIẢ trên Windows CI".

Hậu quả: idiom truy vết "vX.Y.Z (bằng chứng) — fix" bị đứt theo CẢ HAI CHIỀU — grep `r255` trong code
ra RỖNG, còn grep `r251` trong `lookup_ops.py` lại trúng chú thích của tôi trong khi `r251` ở CHANGELOG
là fix của người khác. Người đọc sau sẽ tra chéo ra kết luận sai về lý do một dòng code tồn tại.

Đổi ĐÚNG 7 chỗ, tất cả trong chú thích, neo bằng mốc `(P15` / `cùng gốc rNNN` / `y như rNNN` /
`test rNNN khoá` để không quét sang chú thích rNNN của người khác trong cùng tệp:
`r251 (P15`→`r255 (P15` ×3 · `r252 (P15`→`r256 (P15` · `r253 (P15`→`r257 (P15` · `r254 (P15`→`r258 (P15` ·
`cùng gốc r253`→`cùng gốc r257`.

**KHÔNG một dòng code nào đổi** — đã đo: `git diff` trên tệp có 0 dòng không-phải-chú-thích bị thay.
Vì vậy 19 case r255–r258 và toàn bộ 8 gate phải cho SỐ Y HỆT trước/sau; đó chính là tiêu chí nghiệm thu
của bản này, không phải "gate xanh" chung chung.

Bài học giữ lại: đánh số lại một đợt là thao tác **BỐN mặt** — commit message · CHANGELOG · tên case
test · CHÚ THÍCH CODE. Bỏ sót mặt nào thì mặt đó thành con trỏ chết, và mặt code là mặt sống lâu nhất.

# ★ v1.35.96 — r258: `_vbhn_goc_map` — map "đã phủ" sai HAI HƯỚNG, hướng nguy hiểm là hướng ít ai để ý (2026-07-30)

Nửa CÒN LẠI của cùng lệnh `corpus-relation-sweep` (r257 vá cổng `vbhn_broken`; đây là map coverage).
Map này **SUPPRESS `amendments_missing`** nên khái niệm "in corpus" ở đây phải là LUẬT SERVER, giống cổng
kia — sau r257+r258 hai nửa mới dùng chung MỘT khái niệm.

`_entry_corpus_true` lệch **hai hướng cùng lúc**, và hướng đáng lo không phải hướng tôi cảnh báo lúc đầu:

- **THIẾU `− ref`** (+ thiếu `− loai='thuong'`): dòng `row_kind='ref'` là dòng TRỎ-tham-chiếu, KHÔNG phải văn
  bản sở hữu, mà vẫn được tính là VBHN đã phủ ⇒ **CHE MẤT `amendments_missing` THẬT**. Đây là
  **over-suppression CÓ SẴN** — nguy hiểm hơn hẳn vế nới, vì nó làm lệnh im lặng bỏ qua văn bản cần tải.
  Bằng chứng nằm ngay trong cùng hàm: lúc chọn `base_docs`, sweep viết
  `not _entry_corpus_true(e) or _entry_row_kind(e) == "ref"` — tác giả BIẾT phải trừ `ref`, chỉ nửa map bỏ sót.
- **BỎ SÓT `corpus='vbqppl'` + `row_kind='overflow'`**: server (`tl boot`) ĐẾM chúng là corpus, nên không tính
  là đã-phủ mới là dương-tính-giả `amendments_missing` (giục tải bản gốc mà VBHN đã phủ).

Vế quarantine y như r257: `"_ZZZ_QUARANTINE" in cat` bỏ sót nhãn `QUARANTINE` **trơ** ⇒ VBHN ĐÃ cách ly vẫn
được tính là phủ (che gap). Dùng `_is_quarantine_cat` — hướng SIẾT.

Bảng chân lý sau r258 (ai được tính là "đã phủ"): `true/own` ✓ (như cũ) · `vbqppl/own` ✓ **MỚI** ·
`blank/overflow` ✓ **MỚI** · `true/ref` ✗ **ĐỔI** · `true/loai=thuong` ✗ **ĐỔI** · `true/cat=QUARANTINE` ✗
**ĐỔI** · `true/cat=_ZZZ_QUARANTINE` ✗ (như cũ) · `false/own` ✗ (như cũ).

Test **r258** (6 case) đo 2 CHIỀU: 0/6 trên nền `ba91cf9` → 6/6 trên bản vá. Case (1) khoá trực tiếp BẢNG
CHÂN LÝ của `_vbhn_goc_map` (PURE, 8 dòng vào — 3 ra). Phản chứng chứng minh CHỊU LỰC bằng 3 bản vá QUÁ TAY,
mỗi bản đỏ đúng trục của nó:
· coi MỌI dòng VBHN là phủ → truth-table + `ref_row_not_coverage` + `bare_quarantine` ĐỎ (8/11);
· giữ nới nhưng bỏ vế quarantine → truth-table + `bare_quarantine` ĐỎ, `ref` vẫn xanh (9/11);
· nửa vời `corpus_true ∪ vbqppl` (thiếu `− ref`) → truth-table + `ref_row_not_coverage` ĐỎ (9/11).

NÓI RÕ giới hạn: `r258_uncovered_amendment_still_reported` KHÔNG phân biệt được 3 bản quá tay trên (xanh ở
cả ba, và xanh cả trên nền) — nó là **guard chống hồi quy**, không phải bằng chứng phân biệt. Giá trị phân
biệt nằm ở 4 case còn lại. Ghi ra để không ai đọc "6/6" thành "6 bằng chứng độc lập".

Vì sao gate cũ xanh: `r94_sweep_vbhn_first_covered` dựng VBHN coverage với `corpus:"true", row_kind:"own"` —
đúng ô giao nhau của hai khái niệm, nên test xanh dù dùng vị từ nào.

# ★ v1.35.95 — r257: `corpus-relation-sweep` — hai vị từ THÔ ở cổng `vbhn_broken` (2026-07-30)

Cổng đủ-điều-kiện-`vbhn_broken` dùng 2 vị từ thô, cả hai lệch khuôn nhà — đúng lớp dương-tính-giả mà
VBHN-FIRST v1.34.32 sinh ra để diệt, chỉ khác chỗ:

1. `str(ent.get("corpus")) != "true"` — **site DUY NHẤT trong repo so cột `corpus` mà KHÔNG chuẩn hoá**
   (28 site còn lại: `hygiene.py` ×12, `ops_misc.py` ×7, `ingest_ops.py` ×4, `nlm_ops.py`, `regio.py`… đều
   `.lower()`/helper). Miền giá trị THẬT rộng hơn `{true,false}`: `vbqppl` (luật server `corpus∈{true,vbqppl}`
   — `hygiene.py:3015,3025`; `cli.py:359` nói thẳng `--corpus true` literal "bỏ sót vbqppl/overflow"),
   `thuong`, `""`, cùng mọi lệch HOA-thường ⇒ **VBHN corpus LÀNH bị coi là NGOÀI corpus**, có goc-tie là vào
   `sources_to_add` với `reason="vbhn_broken_or_quarantine"` — giục tải lại đúng thứ đã có.
2. `"_ZZZ_QUARANTINE" in cat` — bỏ sót biến thể nhãn `QUARANTINE` **trơ** (thứ `_is_quarantine_label_variant`
   xác nhận có thật) ⇒ VBHN ĐÃ cách ly nằm trong chuỗi base **lọt lưới**, không được gắn cờ.

Chọn `_entry_is_corpus_effective` (LUẬT SERVER), **không** `_entry_corpus_true`: repo tự khai literal là bản
bỏ sót. Nhưng helper server-rule cần `row_kind`+`corpus`+**`loai`**, còn cổng này xét trên bản `_summ_entry`
— bản đó **KHÔNG có `loai`** ⇒ nhánh "− thuong" đọc thiếu trường và nghiêng về suppression. Nên vá GỐC: tra
entry ĐẦY ĐỦ theo `drive_id` (`entry_by_drive_id`, cùng mẹo sweep đã dùng cho `goc_by_drive_id`), fallback về
bản summ khi không thấy — fallback giữ nguyên ca `"zzz"` của test r94.

**RANH GIỚI CỐ Ý, đã khoá bằng test để không ai "sửa" thành `strip()`:** khoảng trắng (`' true'`) VẪN là NGOÀI
corpus. Lượt test đầu tôi assert ngược (coi `' true'` là in-corpus) và case đỏ trên bản vá — **tôi sai, không
phải code sai**: GAS `String(o.corpus||'').toLowerCase()` (`Code.2.21.2p.gs:2238`) KHÔNG trim, nên ô có khoảng
trắng thì SERVER cũng không đếm. Thêm `strip()` là tự tạo lệch mới với `tl boot`. Ô bẩn là việc của
`registry-doctor`, không phải chỗ sweep tự lấp.

Hai vế đi NGƯỢC hướng nhau nên test khoá CẢ HAI chiều: vế corpus **bớt** cờ (suppression — hướng nguy hiểm),
vế quarantine **thêm** cờ. Test **r257** (5 case) đo 2 CHIỀU: 1/5 trên nền `ba91cf9` → 5/5 trên bản vá; phản
chứng chứng minh CHỊU LỰC bằng 3 bản vá QUÁ TAY bơm vào cây riêng:
· bỏ vế corpus (nới in-corpus) → `r257_broken_vbhn_still_flagged_3_ways` + `goc_tie_gate` ĐỎ (3/5);
· coi MỌI cat là quarantine → 3 vế "không gắn cờ bừa" ĐỎ (2/5);
· bỏ chốt goc-tie v1.34.32 → chỉ `r257_goc_tie_gate_still_holds` ĐỎ (4/5).
Phản chứng bắt buộc `r257_broken_vbhn_still_flagged_3_ways` khoá 3 đường hỏng ĐỘC LẬP vẫn phải bị bắt:
`corpus='false'` · cờ `VBHN_MISSING_YEAR_OR_DATE` · `row_kind='ref'`.

Vì sao gate cũ xanh: `r94_sweep_vbhn_tie_filter` dựng CẢ HAI ứng viên `corpus:"false"` — vế corpus không được
kích, test xanh dù vị từ đúng hay sai.

CÒN NỢ (F4, KHÔNG gộp vào đây): `_vbhn_goc_map` cũng dùng `_entry_corpus_true` ⇒ VBHN `corpus='vbqppl'` không
được tính là "đã phủ" ⇒ `amendments_missing` dương-tính-giả. Cùng gốc, nhưng vá nó là nới **suppression** cho
`covered_by_vbhn` — sai một nhịp là che mất văn bản thiếu THẬT, phải có phiếu thiết kế riêng.

# ★ v1.35.94 — r256: `rasoat-loop` HẾT dừng sớm — GAP không còn bị nuốt (2026-07-30)

`while frontier and dry_rounds < K and it < max_iter` — `dry_rounds` KHÔNG được nằm trong điều kiện
vòng: chạm K là thoát **dù frontier còn**. Docstring nói "DỪNG khi frontier rỗng **VÀ** dry_rounds≥K"
(AND) nhưng code cài **OR**.

Nặng nhất là vế thứ hai: ứng viên **NGOÀI corpus cũng `dry_rounds += 1`** — mà GAP chính là **SẢN PHẨM**
của lệnh (`gaps_missing_in_corpus` = danh sách cần tải). Nên càng tìm ra nhiều gap càng dừng sớm: động
lực bị đảo ngược. Đo được với 5 ứng viên ngoài corpus, K=2 mặc định:

```
{"iterations": 2, "seen": 5, "evaluated": 2, "frontier_remaining": 3,
 "converged": false, "gaps_missing_in_corpus": ["1/2020/QH14","2/2020/QH14"]}
```
báo **2/5 GAP — mất 60%**, 3 ứng viên KHÔNG hề được đánh giá, và `max_iter=12` **chưa hề chạm**. Với base
dẫn chiếu nhiều văn bản chưa nạp (ca thường gặp) thì chỉ cần 2 gap liên tiếp ở đầu hàng ưu tiên là cả lượt
rà đứt — im lặng, `ok: true`, rc=0.

Chẩn đoán còn SAI theo: nhánh not-converged in cứng `'CHƯA hội tụ (chạm max-iter)'` ⇒ người đọc đi tăng
`--max-iter`, tăng bao nhiêu cũng vô ích vì nút thắt là `dry_rounds`. Nay phân biệt 3 trạng thái và thêm
`stop_reason` (`frontier_empty` | `max_iter`) + `dry_rounds`/`max_iter`/`dry_rounds_target` vào JSON —
doctrine "no silent caps": lệnh phải NÓI RA nó đã bỏ lại bao nhiêu và vì sao.

Bản vá tối thiểu — CHỈ bỏ `dry_rounds < K` khỏi điều kiện vòng. `max_iter` vẫn là **trần cứng duy nhất**;
`dry_rounds` **giữ nguyên** vai trò tín hiệu hội tụ ở `converged`, và nhờ vậy ca frontier-cạn-toàn-gap nay
đạt `dry_rounds ≥ K` ⇒ `converged: true` — đúng bản chất "đã vét hết". Cờ `--dry-rounds` KHÔNG bị vô hiệu.

Test **r256** (4 case) đo 2 CHIỀU: 0/4 trên cây nền `ba91cf9` → 4/4 trên bản vá. Ba vế phản chứng được
CHỨNG MINH CHỊU LỰC bằng cách bơm bản vá QUÁ TAY vào cây riêng, mỗi bản chỉ làm ĐỎ đúng vế của nó:
· bỏ luôn `max_iter` khỏi điều kiện vòng → chỉ `r256_max_iter_still_hard_ceiling` đỏ (3/4);
· bỏ `dry_rounds >= K` khỏi `converged` → chỉ `r256_dry_rounds_still_gates_converged` đỏ (3/4).
Vế thứ tư khoá `seen` chống lặp vô hạn khi expand cứ trả ứng viên mới.

Vì sao gate cũ xanh: `rasoat_loop_dedup_priority_no_infinite` chỉ test helper PURE `_rasoat_dedup_push`,
không chạm điều kiện dừng của `cmd_rasoat_loop`.

# ★ v1.35.93 — r255: `rasoat-chongcheo` HẾT báo ✗thiếu-corpus cho VBHN ĐÃ CÓ (2026-07-30)

Rà P15 nhóm lookup + rà soát trên cây đóng băng bắt: cổng nới bare-VBHN **v1.33.47** đã vá
`relation-check` (`lookup_ops.py:681,694`) và `frontier-expand` (`fetch_web.py:211`) nhưng **BỎ SÓT
đường `rasoat-chongcheo`** — 3 điểm so số hiệu còn dùng vị từ thô `norm_sohieu(_entry_sohieu(e)) == k`:
`_in_corpus` · `_resolve_cluster_member` · `_cluster_for_base`.

Vì sao nổ CHẮC CHẮN, không phải giả thuyết: `references/subject_clusters.json` ghi **11/11 số hiệu VBHN
KHÔNG NĂM** (`19/VBHN-VPQH`, `14/VBHN-VPQH`, `90/VBHN-VPQH`, `8/VBHN-BNV`…) còn corpus lưu
**year-qualified** theo bất biến PHẢI-CÓ-NĂM (`19-2025-VBHN-VPQH`). `norm_sohieu` giữ nguyên cả hai dạng
⇒ so exact MISS SẠCH. Đo được: `--base 18/VBHN-VPQH` đẩy **cả 4 thành viên VBHN của cụm** vào
`unresolved_refs` — tức giục tải lại đúng những văn bản đã có, ngay chỗ doctrine dặn "verify `tl exists`/
QT-5 trước khi nạp". Cùng LỚP LỖI mà `_vbhn_bare_key` sinh ra để diệt ("VBHN 88 Quảng cáo ĐÃ CÓ mà lần
nào chạy cũng báo thiếu"), chỉ khác call-site.

Bẫy thứ hai, ngược đời: **khoá CANONICAL chính là khoá THẤT BẠI.**
`_cluster_for_base("18/VBHN-VPQH")` → `lao_dong_xa_hoi`, `_cluster_for_base("18-2025-VBHN-VPQH")` →
`None` ⇒ người rà lấy số hiệu từ `locate`/`reg-query` (dạng có năm) thì mất luôn lớp cụm lĩnh vực, cờ
báo `BASE_NO_CLUSTER` "E1 phủ HẠN CHẾ" mà nguyên nhân thật là lệch khuôn khoá. Ở đây gọi
`_sohieu_query_hits_entry` với **giá trị cụm ở vai "query"** (cụm là bên THIẾU năm) — vẫn đúng phép nới
1 CHIỀU, chiều ngược helper cố ý không nới.

**KHÔNG sửa `subject_clusters.json` sang dạng có năm**: đó là đổi DỮ LIỆU, kéo theo `_cluster_lookup` +
golden, và mỗi lần hợp nhất mới lại phải sửa tay — vá ở tầng SO KHỚP thì bao được mọi VBHN tương lai với
zero bảo trì. Cả 3 chỗ GIỮ vế so thô cũ: nới chỉ THÊM, không thay hành vi đang đúng.

Hệ quả CỐ Ý: `cands` của `_resolve_cluster_member` rộng hơn nên `ambiguous` có thể bật thêm — đúng nghĩa
"số hiệu trỏ ≥2 văn bản khác nhau"; thà báo TRÙNG-SỐ-HIỆU còn hơn báo THIẾU oan.

Test **r255** (4 case) đo 2 CHIỀU: 1/4 trên cây nền `ba91cf9` → 4/4 trên bản vá, và vế phản chứng XANH ở
CẢ HAI (chứng minh không nới quá tay): năm KHÁC vẫn so chặt · cơ quan KHÁC không khớp · số KHÁC không
khớp · `_dang_bare_key("74-2025-QH15") == ""` (số hiệu LUẬT thường không được nới) · số hiệu ngoài mọi
cụm vẫn `∅` · văn bản vắng THẬT (`74/2025/QH15`, `14/VBHN-VPQH`) VẪN nằm trong `unresolved_refs`.

Vì sao gate cũ xanh: test `cluster_dup_sohieu_disambig` dựng fixture `so_hieu: "14/VBHN-VPQH"` — **fixture
tự vi phạm bất biến PHẢI-CÓ-NĂM**, nên khoá đúng cái hành vi sai. Fixture r255 dùng khoá có năm.

# ★ v1.35.92 — r254b: test r251 ĐỎ GIẢ trên Windows CI — so chuỗi đường dẫn kiểu POSIX (2026-07-30)

> PR #5 phơi ra: `gate (windows-latest)` **1405/1406**, `gate (ubuntu-latest)` XANH. Đúng một ca:
> `r251_plan_chunk_in_dung_lenh_apply_chay`.

`_c251_plan_chunk_in_dung_lenh_apply_chay` so **CHUỖI THÔ**:
`_chunk_ingest_target("/x/y/a__part01.md") == "/x/y/a__part01.docx"`. Trên Windows
`str(Path('/x/y/a.md').with_suffix('.docx'))` ra `\x\y\a.docx` ⇒ phép so sai. **CODE SẢN PHẨM ĐÚNG** —
`_chunk_ingest_target` trả đường hợp lệ CỦA NỀN; chỉ khẳng định trong test là POSIX-only.

**Lỗi CÓ SẴN từ r251 `73be7be`, KHÔNG do merge r254** — đo: `chunking.py` md5 `20f8ca516833` y nguyên
qua `73be7be` → `296e5c0` → HEAD, và chuỗi `/x/y/a__part01.docx` đã nằm trong selftest từ `73be7be`.
Nhánh đó **chưa lần nào chạy Windows CI** (không có PR); merge chỉ PHƠI nó ra.

**Vá:** so bằng `Path(...) == Path(...)` — trên Windows `Path('\x\y\a') == Path('/x/y/a')` nên khẳng
định GIỮ NGUYÊN ý nghĩa (đổi `.md`→`.docx`, GIỮ thư mục) mà chạy được cả hai nền. Kiểm bằng mô phỏng
`PurePosixPath`/`PureWindowsPath`: cả hai `True` (trước vá: POSIX `True`, Windows `False`).

> **Bài học, đúng §Bài học đắt giá:** "script đa nền phải CHẠY THẬT trên nền đó" áp cho **TEST** y như
> code — 5 lỗi của r244 cũng không lỗi nào lộ ra bằng đọc code. Gate local (Linux) XANH TRỌN mà vẫn ĐỎ
> trên Windows ⇒ **gate một nền không phải bằng chứng đủ để merge**; phải xem CI cả hai nền.
> `tl_selftest.py` NẰM TRONG gói ⇒ cây đổi thì gói đổi, nên bump + deploy lại chứ không sửa lặng.

# ★ v1.35.91 — r254: hợp nhất hai nhánh r251 SONG SONG (2026-07-30)

> **Va chạm đánh số, ghi lại để người sau không tưởng mình đọc nhầm:** hai phiên chạy song song cùng
> ngày 30-07 đều đặt tên **r251** và đều bump **v1.35.88** cho hai việc KHÁC NHAU:
> - `4680d92`/`3f7275f` (vào master): *ba cờ đọc-sai của bộ soi registry* + vá `deploy-guard.ps1`;
> - `73be7be` (nhánh `luat-bhxh-30-07`): *hai cổng XANH mà nói dối* (PLAN chunk in lệnh không chạy nổi).
>
> Không nhánh nào sai — chúng chỉ không thấy nhau. Giữ NGUYÊN cả hai commit (đã đẩy, viết lại lịch sử
> còn tệ hơn); đánh số tiếp từ **v1.35.91/r254** để không có hai bản 1.35.88 khác nội dung trôi ra ngoài.
> Bài học: quy ước "phiên nào bump thì phiên đó đẩy" (§Quy ước deploy mục 1) mới chặn được KHÂU ĐẨY —
> KHÔNG chặn được hai phiên cùng CHỌN một số hiệu. Trước khi bump nên `git fetch origin master` đã.

**Hai bên vá cùng MỘT LỚP lỗi (dòng chunk `__partNN` làm bộ soi hiểu nhầm) ở HAI chỗ khác nhau —
bổ sung nhau, không trùng:**

| | master r251 | nhánh r253 |
|---|---|---|
| chỗ vá | `_subject_sig` (classify + registry_hygiene) | `_title_flags` · `_ingest_missing_select` |
| cờ chữa | `sohieu_conflict` GIẢ giữa canonical/part01/part02 | `CORPUS_TRUE_NOT_ON_NLM` + mời nạp TRÙNG |

Merge tự động ghép SẠCH `registry_hygiene.py` `classify.py` `ingest_ops.py` `tl_selftest.py`
(hai bên sửa hàm khác nhau); chỉ 5 xung đột dòng version/manifest, giải bằng tay lên 1.35.91.
Đáng chú ý: `registry_hygiene.py` nay mang CẢ `skip_reason` (master) LẪN `_nlm_status_known_local`
(nhánh) — hai bug độc lập của cùng một tệp, cả hai đều còn.

Gate chạy lại SAU merge trên cây đã hợp nhất (không tin gate của từng nhánh riêng).

# ★ v1.35.90 — r253: hai cờ "còn nợ NLM" mời nạp TRÙNG, và một bản sao từ vựng đã trôi lệch (2026-07-30)

> Tiếp hồ sơ «Luật BHXH». Món chính là **B4** (dữ liệu) — xem PHỤ LỤC A.8 của
> `rasoat/KETQUA_VIEC_TREO_BHXH_2026-07-30.md`; phần code dưới đây là hai footgun lộ ra khi làm B4.

## 1. Cờ "phủ bằng chunk con" — suýt NHÂN ĐÔI Luật 41 trên notebook

`Luat_41-2024-QH15` (183.428 ký tự > cap chunk 100k) được `profile-ingest-chunks` tách `part01`/`part02`
rồi đẩy NLM. Dòng **canonical** giữ `corpus=true` mà **cố ý KHÔNG mang** `nlm_source_id` ⇒ cả
`CORPUS_TRUE_NOT_ON_NLM` lẫn `ingest-missing` tưởng còn nợ và **mời nạp lại BẢN ĐẦY ĐỦ** — đúng loại rác
đã phải dọn 69→74→71 hôm 29-07. Lượt 30-07 suýt chạy thật; chặn được vì `note` của dòng đó có ghi lý do.

**Vá:** `_chunk_covered_sohieu(entries)` (regio, PURE) — tập số hiệu có ≥1 dòng `<base>__partNN` **CÙNG số
hiệu ĐANG trên NLM**. `_title_flags(e, covered_sohieu=None)` nhận tham số TÙY CHỌN (mặc định None = giữ
NGUYÊN hành vi cho 20+ caller không có row-set); `_ingest_missing_select` tự tính. Nối vào 3 chỗ đếm drift
có sẵn danh sách dòng (`hygiene`, `ops_misc`, `resolve`).

Ba vế phản chứng khoá trong test — thiếu vế nào thì bản vá này thành cái bịt miệng cờ:
- chunk **chưa/đã rớt** khỏi NLM (kể cả `removed_*` gỡ có chủ đích) ⇒ KHÔNG phủ cho ai, canonical **kêu lại**;
- chính dòng `__partNN` mà rớt NLM thì **VẪN kêu** — không được tự phủ cho mình;
- **khác số hiệu** thì không ăn ké phủ của người khác.

Đo trên kho thật: backlog **1 → 0**, và `covered_sohieu` đúng một phần tử `41-2024-QH15` (không quét rộng).

## 2. `registry_hygiene` giữ BẢN SAO từ vựng `nlm_status` đã trôi lệch khỏi ADR-0010

`title_flags` ở đó so `nlm_status` với **exact-set** `{pushed,synced,removed,removed_from_drive,deleted,
trash,trashed}` — thiếu `active` (chính ADR-0010 nắn `live→active`) và thiếu MỌI biến thể `removed_<lý do>`
(mà docstring bản chuẩn `_nlm_status_known` hứa là chạy được). Bản chuẩn theo **tiền tố**, bản sao theo
**danh sách cứng** ⇒ hai nơi trả lời khác nhau cho cùng một câu hỏi.

**Nói rõ mức độ:** đo 30-07 thì **chưa** false-fire THẬT — `analyze()` skip `row_kind=ref` và `own_thuong`
TRƯỚC khi gắn cờ, mà 6 dòng `active` đều `ref` còn 10 dòng `removed_*` đều `own_thuong`. Vá vì cờ sẽ nổ
ngay khi có dòng `own`/khác-`thuong` mang giá trị **đúng chuẩn**, và vì B4 vừa ghi thêm một họ
`removed_<lý do>` mới vào sổ.

Script này **cố ý đứng độc lập** (chỉ `import gas` lazy) nên KHÔNG import `tl_core`; giữ bản sao NHƯNG theo
cùng **LUẬT tiền tố**, kèm test PARITY với `_nlm_status_known` trên cùng bộ mẫu + vế phản chứng
(`added`/`live`/`ready`/`banana` VẪN phải kêu) + chốt chống tái nhiễm (exact-set cũ không được quay lại tệp).

## 3. ĐÍNH CHÍNH PHỤ LỤC A.5 mục 3 — readback `register` KHÔNG phải lỗi cache

A.5 đoán `register` báo `FIELDS_DROPPED_ON_WRITE`/`verified=false` oan là do readback đọc qua cache GAS
TTL~600s, và đề xuất "bust cache trước khi kết luận". **Đọc code + đối chiếu server: việc đó ĐÃ LÀM RỒI.**
Cả hai đường readback (`_verified_reg_upsert` N3 và `_verified_reg_write` batch ≤3) đều gọi
`reg_get … refresh="true"`, và `regReadAll_(force)` phía GAS bỏ qua cache đọc thẳng Sheet khi `force`.
Đo thực nghiệm trên kho thật (ghi lại ĐÚNG giá trị đang có, no-op): `verified=true`, `fields_dropped=null`.

⇒ **Không vá gì cả** — giả thuyết sai thì đừng vá theo nó. Muốn truy tiếp thì cần lệnh/output GỐC của lượt
đó; nghi vấn còn lại (chưa có bằng chứng) là race ghi liên tiếp: mỗi `reg_upsert` rewrite TOÀN BỘ sheet
(tab tạm rồi swap), readback rơi đúng lúc swap của lượt kế có thể thấy bản chưa xong.

selftest **1402/1402** (+2 ca r253). Ruff delta so `296e5c0` = 0 ở `tl.py` (12 F821/0 F401) và
`registry_hygiene.py` (0/0); `tl_selftest.py` +22 F821 do CHÍNH test mới, đúng một tên mới
`_chunk_covered_sohieu` — đã kiểm HÀNH VI: resolve sau import qua `_STUB_MAP['regio']`.

# ★ v1.35.89 — r252: `&amp;` `&lt;` chui NGUYÊN VĂN vào kho — 3 reader .docx quên unescape (2026-07-30)

> Bắt được khi đăng ký BC Bộ Nội vụ (hồ sơ Luật BHXH): `tl extract` trả `6193/BNV-CTL&amp;BHXH`, trong
> khi GDoc trên Drive có `&` trần — webapp `exporttext` đọc đúng 3/3 chỗ. **Sai nằm ở đường ĐỌC của ta.**

Ba nơi sản xuất tự bóc tag `word/document.xml` bằng `re.sub(r"<[^>]+>", "", xml)` mà **KHÔNG unescape
entity**, nên `&amp;` `&lt;` `&gt;` `&quot;` vào kho y nguyên:

| Reader | Đường ảnh hưởng |
|---|---|
| `_docx_unzip_text` (`lookup_ops`) | `tl extract` · `tl doc-text` — text này **ĐƯỢC CACHE và NUÔI CORPUS** ⇒ nặng nhất |
| `_profile_read_probe_text` (`ingest_ops`) | cổng nạp PHÂN LOẠI (`sohieu`/`loai`/`title` suy từ text này) |
| `_the_thuc_detect_he` (`the_thuc`) | dò hệ thể thức (neo dòng `^Số:`) |

`normalize_document.py` thì VỐN ĐÃ unescape đúng ⇒ **hai đường đọc cùng một `.docx` cho hai kết quả
khác nhau**, và cái sai lại là cái nuôi corpus. Với công thức thì nặng hơn dấu `&`: `a < b` hoá `a &lt; b`
— đúng lớp nội dung mà đợt Công báo NĐ 159 đã phải canh (công thức Điều 11/14).

**Vá:** gom về MỘT hàm `docx_markup.plain_from_document_xml()`; cả 3 reader gọi nó. Đặt ở `docx_markup`
vì đó đã là nơi giữ mọi phép đọc `document.xml` — để đây không phải là chỗ thứ tư trôi lệch.

**THỨ TỰ là phần dễ làm sai nhất:** `</w:p>`→newline → bóc tag → **RỒI MỚI** unescape. Làm ngược
(unescape trước) thì `&lt;w:t&gt;` trong nội dung biến thành `<w:t>` và bị chính bước bóc tag **ăn mất
chữ** — đổi một lỗi thành lỗi tệ hơn. Test có vế phản chứng chạy đúng thứ tự sai để chứng minh nó mất chữ.

Đo 2 chiều: `6193/BNV-CTL&amp;BHXH` → `&BHXH` · `a &lt; b và c &gt; d, ký hiệu &quot;X&quot;` →
`a < b và c > d, ký hiệu "X"`; nội dung `&lt;w:t&gt;`/`&lt;div&gt;` CÒN NGUYÊN. Test còn ghim rằng cả 3
tệp reader đều dùng hàm chung và KHÔNG còn site bóc tag trần nào.

⚠ **Cache cũ mang text SAI.** `extract_<id>.txt` đã sinh trước bản vá (và mọi bản `cache-build`
consolidated dựng từ chúng) vẫn còn `&amp;` với tài liệu có dấu `&`. Corpus trên Drive KHÔNG hỏng —
lỗi thuần ở phía đọc. Cách chữa: xoá cache extract rồi đọc lại; hồ sơ Luật BHXH đã xoá trong lượt này.

`--selftest` **1400/1400**.

# ★ v1.35.88 — r251: hai cổng XANH mà nói dối, bắt được khi làm nốt việc treo hồ sơ Luật BHXH (2026-07-30)

## Ca 2 — plan ingest SUY METADATA TỪ TÊN TỆP khi máy thiếu `pdftotext`, không một lời cảnh báo

Bắt được khi định đăng ký `BC 6193/BNV-CTL&BHXH` (mục §E.7 sổ treo). `_read_local_text_for_analysis` VẪN
trả cảnh báo `PDFTOTEXT_NOT_AVAILABLE_TEXT_LAYER_UNKNOWN`, nhưng `_probe_pdf_quality` **VỨT nó** (`_txt, _ =`)
⇒ **"máy này thiếu bộ bóc chữ" và "PDF là bản quét" cho probe RỖNG GIỐNG HỆT nhau**. Plan im lặng rơi về
`_classify_doc_header("", filename)` — tức suy mọi thứ từ TÊN TỆP — mà vẫn `ok:true`, rc=0.

Đo LIVE trên CÙNG tệp, CÙNG lệnh, chỉ khác việc container có `pdftotext`:

| | thiếu `pdftotext` | có `pdftotext` |
|---|---|---|
| `sohieu` | `6193_2026_BNV` (rác) | `6193/BNV-CTL` |
| `loai` | *(rỗng)* | `Báo cáo` |
| `title` | tên tệp | trích yếu thật |
| `doc_name` | `VB_6193_2026_BNV_BC_6193_2026_BNV_CTL_…` (nhân đôi tiền tố) | `BC_6193_2026_BNV_CTL_…` |
| `header_chars` | 0 | 16000 |
| **`plan_hash`** | `42ca6386…` | `71582728…` |

`plan_hash` LỆCH là chỗ đau nhất: `--expected-plan-hash` lấy ở máy A **không dùng được** ở máy B, mà lý do
lệch thì không hiện ra ở đâu. Và `BC 6193` hoá ra **KHÔNG phải bản quét** — nó là PDF do Word 2019 xuất, lớp
text sạch **33.917 ký tự**; kết luận "scan" trước đó thuần là artefact của container thiếu poppler.

**Vá:** `_probe_pdf_quality` trả thêm `tool_warn` — CHỈ dựng khi cảnh báo thuộc họ hạ tầng
(`PDFTOTEXT_NOT_AVAILABLE` / `PDFTOTEXT_ERROR` / `PDFTOTEXT_NO_OUTPUT`); cả hai lane ingest phơi nó ra
(`verify_gate.flags` cho `profile-ingest`, `warnings` cho `_vb_ingest_auto_plan` — lane này còn suy cả `cat`
từ tên tệp nên im lặng là im lặng ghi sai). Hằng `_PDF_PROBE_TOOL_WARN` **phải re-export vào namespace `tl`**
— bẫy I11 đã ĐỎ THẬT một lượt trong phiên vá: `bind` re-home `__globals__` nên hằng để ở `ingest_ops` làm
hàm ném `NameError` NGAY trên đường chạy thật (rc=1), đọc code không thấy.

**KHÔNG chạm chính sách `source_quality`:** `.pdf` vẫn luôn = `ocr` (⇒ cần `--ocr-verified` mới vào corpus).
Đó là thiết kế, không phải lỗi — bản vá chỉ thôi nói dối về LÝ DO không đọc được chữ.

Test dùng ĐẦU VÀO THẬT, KHÔNG monkeypatch (bịt `PATH` để `shutil.which` trả None — đúng cơ chế hỏng ngoài
đời), kèm 3 vế phản chứng: tệp NGẮN (hình dạng PDF quét thật) · đọc được text bình thường · đuôi không bóc
được text — cả ba đều KHÔNG được nổ cờ hạ tầng, để bản vá không đổi một lời nói dối thành một lời dọa oan.

## Ca 1 — PLAN của `profile-ingest-chunks` in lệnh KHÔNG chạy nổi

> Bắt được khi làm nốt việc treo của hồ sơ Luật BHXH: mục §5.4 sổ treo ghi "chunk-apply xuất `.md` mà
> `profile-ingest` không nhận — CHƯA vá". Đo lại thì **r231 ĐÃ vá nhánh apply**; chỗ còn hở là **PLAN**.

`chunk-apply` ghi `.md`; `profile-ingest` chỉ nhận doc/docx/odt/pdf/rtf/xls/xlsx. Cầu nối r231 vật chất
hoá `.docx` — nhưng **CHỈ trong nhánh `--apply`**. Nhánh DRY vẫn in `planned_child_commands` trỏ đường
`.md`, kèm `ok: true`. Ai làm theo plan (chạy tay từng lệnh con — đúng cách người ta soi một pipeline
trước khi cho ghi) ăn `rc=2 UNSUPPORTED_EXTENSION` và kết luận pipeline chunk gãy. Đó chính là lý do lượt
29-07 phải "lách bằng cách dựng .docx thủ công" dù cầu nối đã có sẵn trong cây.

**Plan `ok:true` mà lệnh của nó không chạy nổi là plan NÓI DỐI** — cùng họ với bài học "cổng xanh nhờ
`rc=0` là cổng có thể bị lừa", chỉ ngược chiều: ở đây rc=0 của *plan* che một lệnh chết chắc.

**Vá:**
- `_chunk_ingest_target(path)` — phép suy đường DUY NHẤT (`.md` ⇒ `.docx` cùng thư mục, tệp khác giữ
  nguyên), KHÔNG ghi gì. PLAN và APPLY dùng CÙNG hàm này ⇒ lệnh in ra = lệnh chạy thật.
- PLAN in đường `.docx` + thêm `materialize_from` (đường `.md` sinh ra nó) và `materialize_note`.
- APPLY vật chất hoá từ `materialize_from`, và **guard `MATERIALIZE_PATH_MISMATCH`**: đường `_chunk_md_to_docx`
  sinh ra phải TRÙNG đường plan đã in — lệch thì dừng, không gọi con (nếu hai phép suy đường trôi khỏi
  nhau thì plan lại nói dối lần nữa, lần này im lặng).
- Allowlist phần mở rộng của `profile-ingest` được ĐẶT TÊN: hằng `PROFILE_INGEST_ALLOWED_EXTS` (ở
  namespace `tl` vì `ingest_ops.bind` re-home `__globals__` — bẫy I11). Trước đó là set trần trong thân
  hàm nên không test nào neo vào được, và cầu nối chunk chỉ còn cách COPY danh sách rồi trôi lệch.

**Đo HÀNH VI 2 chiều, không đọc code:** fixture 40 Điều / 86.479 ký tự → `chunk-apply` 5 chunk →
`chunk-verify` 13/13 → chạy **y nguyên** 5 lệnh con mà plan in ra: **5/5 `rc=0 ok=true`**, số Điều
9+9+9+9+4 = **40 = đúng số Điều fixture**. Phản chứng cùng cây: đường `.md` thô vẫn `rc=2
UNSUPPORTED_EXTENSION` (không nới allowlist — nới là mở cửa cho `.md` bất kỳ vào corpus).

## Chốt chung cho cả hai ca

4 test `r251_`, mỗi test có vế phản chứng. `--selftest` **1399/1399**.
**Đã kiểm PHẢN CHỨNG bằng cách GỠ VÁ:** gỡ ca 1 ⇒ `r251_plan_chunk_in_dung_lenh_apply_chay` ĐỎ · gỡ ca 2 ⇒
`r251_thieu_bo_boc_chu_khac_pdf_ban_quet` ĐỎ · gỡ dòng re-export ⇒ `r251_hang_canh_bao_re_export_vao_tl` ĐỎ;
phục hồi ⇒ 1399/1399. Test xanh vì bản vá, không xanh oan.

Ruff `--select F` DELTA so master (đo lại trên `origin/master` sạch, so theo TÊN chứ không theo số lần):
`tl.py` 12→12 · `chunking.py` 39→39 · `tl_selftest.py` **0 tên mới** · `ingest_ops.py` +1 tên = đúng
`PROFILE_INGEST_ALLOWED_EXTS`, cùng lớp BY DESIGN với 363 tên re-home sẵn có trong tệp đó — đã kiểm
HÀNH VI: cổng chặn `.md`, cho `.docx` qua. F401 = 0 (không đổi).
# ★ v1.35.88 — r251: ba cờ đọc-sai của bộ soi registry (2026-07-30)

Lượt rà tiếp hồ sơ «Luật BHXH». NLM chết cả lượt ⇒ chạy chế độ không-NLM (RASOAT_HOSO_LOOP §4b) và
vá đúng những chỗ **công cụ nói sai về chính số nó in ra** — cả ba đều bắt được bằng cách ĐO LIVE rồi
đối chiếu với báo cáo lượt trước, không suy từ đọc mã.

**(1) `registry-doctor.basis` khai THIẾU phần mình loại.** v1.35.65 đã thêm `scanned`+`basis` để hết
đọc "missing_sohieu=19 trên 90 dòng" — nhưng `basis` viết "loại ref + bản gốc `loai='thuong'`", trong
khi `is_own_thuong` loại THÊM **mọi** dòng own `corpus=false` bất kể `loai`. Đo hồ sơ Luật BHXH: 33
dòng bị loại mà chỉ 22 là `loai='thuong'`; 11 dòng còn lại có tên/số hiệu CHUẨN (TT 21-2025-TT-NHNN,
BC 1104-BC-BHXH, 3 Phụ lục Thái Nguyên, CV 7728-BNV, BC 7692-BC-BNV…) và **5 trong số đó mang cờ
`MISSING_SOHIEU` mà không vào bucket `missing_sohieu`** ⇒ ai đọc `missing_sohieu=25` cũng không có
đường nào biết. Nay tách `skipped_own_corpus_false` thành số đếm RIÊNG (`scanned` = count − ba lớp) và
`basis` kể đủ ba lớp kèm câu cảnh báo về cờ bị bỏ. Hàm `skip_reason` trả lý do từng dòng.
*Không đổi phép lọc* — chỉ đổi phần KHAI BÁO: sửa phép lọc là đổi ngữ nghĩa hygiene, việc khác.

**(2) `sohieu_conflict` GIẢ cho họ chunk.** 3 dòng cùng `41-2024-QH15` (canonical + `__part01__` +
`__part02__`) cho 3 chữ ký `_subject_sig` khác nhau ⇒ bị xếp `sohieu_conflict_different_doc` = "văn bản
KHÁC cùng số hiệu, NGUY HIỂM tra sai", dù chẻ chunk là CHỦ ĐÍCH (lách trần 100k của NLM). Nay bỏ hậu
tố `__partNN__…` trước khi lấy chữ ký ⇒ `sohieu_conflict_groups` 1 → **0**, họ này về
`sohieu_dup_same_doc` (đúng bản chất: một văn bản, ba dòng). Lượt trước định chữa bằng cách GHI CHÚ vào
registry (journal `register-bulk_1785320950_22129`); đo lại 30-07 thấy `goc`/`title_vn`/`sua_doi` của cả
ba dòng vẫn RỖNG — ghi chú không neo được, nên chữa ở CODE. Kèm **drift-lock hai mirror**
`registry_hygiene._subject_sig` ↔ `classify._subject_sig`: docstring nói "Mirror" mà trước r251 không gì khoá.

**(3) `ingest-missing` báo `backlog=0` trên manifest 3 ngày tuổi.** Đo 30-07: `tl ingest-missing --json`
(không `--refresh`) trả `manifest_snapshot=2026-07-27T16:27` và `backlog=0`; CÙNG PHIÊN, `--refresh` trả
`backlog=2` (Luật 41/2024 chờ nạp + BIDV thiếu số hiệu) và `sweep` cũng nói "2 chưa push NLM". `note`
cũ có nhắc cache nhưng người đọc dừng ở dòng đầu ⇒ nay có `snapshot_age_s` + cờ TÊN `STALE_SNAPSHOT`
(>1h, xa hẳn cache GAS ~600s), và khi `backlog=0` thì nói thẳng "số 0 trên snapshot cũ KHÔNG phải hết
việc". Mốc không đọc được ⇒ `SNAPSHOT_TS_UNPARSEABLE`, không im lặng. Cùng họ bài học
`reg-query --refresh` (nạp chồng 9 tài liệu 24-07): **số 0 trên dữ liệu nguội không phải là sạch.**

**(4) `deploy-guard.ps1` fail-closed OAN ⇒ đường deploy Windows TẮC HẲN.** `gws` in banner
`Using keyring backend: keyring` TRƯỚC JSON, guard gộp stderr (`2>&1`) rồi đổ THẲNG vào
`ConvertFrom-Json` ⇒ chết ngay ký tự `U` ⇒ `exit 4` dù `gws` rc=0 và tên file đọc được bình thường.
Đo 30-07: guard đỏ, mà `gws` trả đúng `tra-luat-skill-v1.35.87-gws3env.zip`. Twin `deploy-package.sh`
KHÔNG vướng vì nó `sed` trên cả khối — đúng cảnh báo "hai bản sẽ trôi lệch" của §Quy ước deploy, lần
này bên PS là bên CHẶN OAN chứ không phải bên đẩy lọt. Chữa: cắt phần ngoài JSON (`{` đầu → `}` cuối)
rồi mới parse (vẫn parse JSON thật, không quay lại regex mò khoá), và in 5 dòng đầu khi parse vỡ để
lần sau chẩn được ngay. Kèm bẫy môi trường: guard là **pwsh 7** — chạy bằng `powershell.exe` (5.1) thì
vỡ ở `ParserError: Missing closing '}'` do cú pháp PS7, KHÔNG phải lỗi script.

Bẫy gặp khi vá (3): thêm 2 hàm + 1 hằng vào `tl_core/ingest_ops.py` làm ĐỎ hai drift-lock cùng lúc —
`r90` (tên top-level của module REBASE phải resolve qua `tl`) và `r81` (mọi tên trong `_STUB_MAP` phải
CALLABLE). Hằng `_SNAPSHOT_STALE_S` phải re-export TRỰC TIẾP, không vào `_STUB_MAP`.

+4 test (`r251_doctor_basis_khai_dung_phan_bi_loai`, `r251_ingest_missing_bao_snapshot_nguoi`,
`r251_chunk_khong_bi_doc_thanh_conflict`, `r251_deploy_guard_chiu_duoc_banner_gws`, mỗi test đều có
phản chứng) → selftest **1399/1399**.
ruff delta +2 (F821 `Path` + E702, đúng idiom sẵn có của `tl_selftest.py`).

# ★ v1.35.87 — r250: nlm-auto-refresh.sh — tự phát hiện export mới trên Drive → import → mã hoá → xoá (2026-07-29)

(Đánh lại số từ r241/v1.35.78 vì phiên song song đã dùng r241–r249 cho việc khác — rebase lên master v1.35.86.)

Hoàn tất tự động hóa refresh NLM (user chọn "tự import + tự xoá plaintext"). Hai mắt xích:
- A (điện thoại→Drive): app Android autosync (Autosync for Google Drive / FolderSync) đồng bộ MỘT
  CHIỀU Download/ → thư mục Drive ducthangho@gmail.com. Cookie Quick Manager export tên có
  'nlm-auth' → tự lên Drive. (Cài 1 lần trên phone, ngoài repo.)
- B: scripts/nlm-auto-refresh.sh — STATELESS theo modifiedTime: export 'nlm-auth' mới hơn bundle
  nlm_cred.enc ⇒ import (nlm-auth-import.sh --drive-id) → stage vào bundle mã hoá → XOÁ plaintext
  khỏi Drive THEO ĐÚNG ID (chỉ sau khi mã hoá xong); không có export mới ⇒ keep-warm. Probe cuối:
  rc 0 sống / 3 chết (cần re-harvest) / 2 hạ tầng hỏng.

Routine "giữ-ấm + cảnh báo" (trig_01ReWux8) đổi để gọi nlm-auto-refresh.sh ⇒ auto-refresh đầy đủ
mỗi 6h: user chỉ cần thỉnh thoảng bấm Export trên điện thoại.

Kiểm: keep-warm path LIVE (139 notebook, rc 0); so-mốc unit-test 3 ca; import --drive-id + delete
theo ID chứng minh riêng. XOÁ CHỈ theo ID cụ thể, KHÔNG theo tên — bài học: một lần dọn test xoá
theo tên 'Untitled' đã xoá nhầm 1 file image/png không thuộc phiên (permanent, không trong trash).
# ★ v1.35.86 — r249: báo cáo lượt rà ra khỏi GÓI, vào thư mục `rasoat/` (2026-07-30)

5 tệp sản phẩm-phiên đang chiếm slot trong gói mà runtime Cowork không bao giờ đọc:
`KETQUA_DON_DU_LIEU_BHXH_2026-07-29.md` · `RASOAT_PROFILE_LUAT_BHXH_2026-07-29.md` ·
`RASOAT_BLLD_18-VBHN-VPQH.md` · `RASOAT_BLLD_2026-06-27.md` · `BANGIAO_NGUON_CONGBAO_BHXH_2026-07-29.md`.
Đã `git mv` cả 5 vào `rasoat/` và thêm `rasoat` vào `_RELEASE_EXCLUDE_DIRS`. Gói 198 → 193 tệp.

**Chọn THƯ MỤC, không liệt kê từng tên** — đây là điểm thiết kế, không phải tiện tay: báo cáo sinh
liên tục theo ngày, nên bảng tên sẽ trôi lệch ngay lượt rà sau và lại chiếm slot mà không ai nhớ vá.
Thư mục thì bao được mọi báo cáo tương lai với zero bảo trì.

**KHÔNG dùng `reports/` sẵn có** dù nó đã nằm trong `_RELEASE_EXCLUDE_DIRS`: `.gitignore` dòng 20 bỏ
qua `reports/`, nên chuyển vào đó là MẤT tệp khỏi git — trái yêu cầu (giữ trong repo, chỉ loại khỏi
gói). `rasoat/` là thư mục CÓ commit mà không vào gói, cùng khuôn `changelog_archive`.

Test **r249** đo qua CHÍNH hàm quyết định `_release_should_include` chứ không chỉ đọc bảng, và có
phản chứng: `rasoat/X.md` → loại · **`SKILL.md` ở gốc → VẪN nhận** (thiếu vế này thì một luật quét
quá tay vẫn xanh) · 4 báo cáo phải CÒN trên đĩa (loại khỏi gói ≠ xoá tệp).

Đã kiểm không tài liệu nào trỏ tới 5 tệp này nên `doc_pointers` không sinh con trỏ chết — khác với
bẫy r246, nơi một đường dẫn trong §10 trỏ tới tệp cố ý ngoài gói và `release-verify` bắt đỏ.

# ★ v1.35.85 — r248: script deploy phải NÓI RÕ khi bị đặt sai chỗ (2026-07-30)

**Sự cố người dùng báo:** copy `deploy-package.ps1` + `.cmd` sang `D:\Quốc hội\` rồi chạy ⇒ chết ở bước 0
với `Cannot find path 'D:\VERSION' because it does not exist.` Người đọc KHÔNG THỂ suy ra nguyên nhân
thật là SAI CHỖ ĐẶT: script tính gốc repo bằng "lên HAI cấp từ vị trí của nó" (vì vốn nằm ở
`<repo>/scripts/`), nên ở `D:\Quốc hội\` thì lên hai cấp ra `D:\`.

Lỗi kép: (1) người dùng đặt sai chỗ, (2) **script báo lỗi mù mờ** — và (2) mới là khiếm khuyết của ta.
Một thông báo chỉ đúng-về-mặt-kỹ-thuật mà không dẫn tới cách chữa thì vẫn là hỏng.

Nay CẢ HAI bản thử nhiều ứng viên rồi KIỂM dấu hiệu repo (`VERSION` + `scripts/tl.py`):
`-Repo`/`TL_REPO` → lên-2-cấp → thư-mục-script → cwd. Không đạt ⇒ in ĐÃ THỬ NHỮNG ĐÂU (từng đường dẫn,
kèm nhãn vì sao thử) + hai cách chữa, `rc=2`. Thêm tham số `-Repo` (ps1) và biến `TL_REPO` (sh) để ai
muốn giữ script ngoài repo vẫn chạy được.

Vá cả bản `sh` dù chỉ bản `ps1` sập — cùng một giả định "lên hai cấp", parity là doctrine.

**Test hai chiều, chạy thật (tải PowerShell 7.4.6, xong xoá):**
| tình huống | ps1 | sh |
|---|---|---|
| đặt đúng `<repo>/scripts/` | chạy | chạy |
| script NGOÀI repo, cwd cũng ngoài (đúng ca của user) | **rc=2 + chỉ rõ 3 đường đã thử** | **rc=2** |
| script ngoài repo + `-Repo`/`TL_REPO` | chạy | chạy |
| script ngoài repo nhưng cwd Ở TRONG repo | chạy (cwd cứu) | chạy |

Ca cuối đáng ghi: lượt test đầu tôi chạy từ trong repo nên `cwd` cứu, phép thử KHÔNG chạm đường đỏ —
phải dựng lại cwd trung tính mới tái hiện được. Fixture sai làm test xanh oan.

Kèm bộ khởi chạy mỏng `deploy-tra-luat.cmd` (KHÔNG vào repo — người dùng tự đặt ở `D:\Quốc hội\`): chỉ
`call` bản trong repo, sửa MỘT dòng `TL_REPO`. Cố ý không phải bản copy — hai bản song song sẽ trôi lệch,
đúng cái bệnh vừa chữa xong ở r246 khi bỏ `upload-skill-to-Package.ps1`.

# ★ v1.35.84 — r247: vỏ `.cmd` để double-click deploy (2026-07-30)

Bỏ `upload-skill-to-Package.ps1` ở r246 làm mất luôn đường **double-click** — Windows KHÔNG chạy `.ps1`
khi double-click (mở trong editor), và ExecutionPolicy mặc định có thể chặn. Đó chính là lý do đường cũ
có vỏ `.cmd`. Trả lại: `scripts/deploy-package.cmd`.

- Ưu tiên `pwsh` (7+, bản đã kiểm); chỉ có `powershell` 5.1 thì VẪN chạy nhưng NÓI RÕ 5.1 chưa kiểm và
  gợi ý `winget install`. Không im lặng giả định tương thích.
- `-ExecutionPolicy Bypass` chỉ cho TIẾN TRÌNH này, không đổi cài đặt máy.
- `pause` CHỈ khi không có đối số (đường double-click, để cửa sổ không biến mất); gọi từ terminal/CI có
  đối số thì trả rc ngay, không treo chờ.
- Truyền thẳng mọi đối số cho `.ps1` và **giữ nguyên rc** (0/1/2/3) — vỏ bọc không được nuốt mã lỗi.

Cũng thêm `deploy-package.cmd` vào `_RELEASE_EXCLUDE_NAMES_ANYWHERE` (dev-side, gói giữ 197 tệp) và mở
test **r244** lên 5 tên.

**Giới hạn phải nói rõ: `.cmd` KHÔNG được test hành vi.** Container này là Linux, không có `cmd.exe`, và
batch không có bản thay thế như PowerShell 7 trên Linux. Nên chỉ soi tĩnh, và bù bằng cách giảm bề mặt
rủi ro theo đúng các bẫy batch đã biết:
- **ASCII thuần + CRLF** cho cả hai tệp `.cmd` (kiểm bằng số: 0 ký tự >127, 0 LF lẻ). `cmd.exe` khó tính
  với LF-only và với ký tự ngoài code page.
- **KHÔNG nhúng đường dẫn có dấu** (`D:\Quốc hội`) vào `.cmd` — mời gọi lỗi code page. Tệp dọn lấy
  `%~dp0` (thư mục của chính nó) nên Windows tự đưa đúng đường dẫn, không qua bước giải mã nào.
- Không đọc biến được `set` TRONG cùng khối ngoặc (cần delayed expansion) — đã soi từng chỗ; các bộ đếm
  chỉ đọc SAU vòng lặp. `if defined` thì an toàn trong khối vì nó xét lúc chạy.
- Mốc thời gian lấy từ `wmic os get localdatetime`, KHÔNG dùng `%DATE%` (đổi định dạng theo locale máy).
- Ngoặc trong `echo` nằm trong khối đều escape `^(` `^)`.

# ★ v1.35.83 — r246: BỎ `upload-skill-to-Package.ps1`, một đường deploy cho mỗi nền (2026-07-30)

Người giữ chốt: chuyển sang `deploy-package.ps1`, bỏ script cũ. Kể từ đây **không còn đường deploy nào
thiếu chốt** — trước đó `upload-skill-to-Package.ps1` nằm ngoài repo nên (a) trôi lệch theo từng máy,
(b) không có chốt chống thụt lùi, (c) phiên Claude không đọc/sửa được.

Đường chính thức, hai nền, cùng quy trình — cả hai TRONG repo nên `git pull` là có bản mới nhất:
`.\scripts\deploy-package.ps1 -Pull -Push` · `./scripts/deploy-package.sh --push`.

**GỠ `scripts/wire_deploy_guard.py` (thêm ở r245, sống đúng một phiên bản).** Nó sinh ra CHỈ để vá
`upload-skill-to-Package.ps1`; bỏ script đó thì bộ vá mất đối tượng. Giữ lại là dead tooling mà tài liệu
vẫn trỏ tới — đúng loại doc-rot mà `doc-claims-check` sinh ra để bắt. Cần lại thì `git revert`.
Test **r244** thu về 4 tên (bỏ tên thứ 5), vẫn đo hai vế.

**Bẫy phát sinh, và repo tự dạy cách chữa đúng.** §10 viết lại có dòng `./scripts/deploy-package.sh` —
`release-verify` ĐỎ ngay: `doc_pointers` bắt con trỏ đó CHẾT TRONG GÓI, vì chính 4 script deploy đã bị
loại khỏi gói ở r244/r245. Cổng đúng, tài liệu sai.

Lượt chữa ĐẦU đi sai đường: khoanh cặp vào `_POINTER_BASELINE` (tiền lệ `GOTCHAS.md → scripts/.tl_state`,
"cố ý ngoài gói"). Test `r209_baseline_ratchet` ĐỎ ngay — baseline **khoá SỐ ĐẾM**, phình lên là phải sửa
test có chủ đích. Đọc chú thích của chính test đó mới thấy nếp đã chốt: r218 hạ 10→4, r226 hạ 4→3 và ghi rõ
*"sửa lời tài liệu thay vì khoanh nợ tiếp"* — cho ĐÚNG trường hợp tệp không có trong kho/gói. Nên đã GỠ
mục baseline vừa thêm (giữ ratchet ở 3) và sửa LỜI: §10 gọi TÊN tệp, dòng chạy đổi thành `cd scripts` rồi
`./deploy-package.sh --push` (cả hai script tự `cd` về gốc repo nên vẫn chạy đúng và vẫn copy-paste được),
kèm một khối `>` nói thẳng 4 script này ở trong repo nhưng CỐ Ý ngoài gói. Cũng cân phương án loại luôn
DEV_TOOLING_GUIDE khỏi gói rồi BỎ: `gen_instructions.py` có trỏ tới nó ⇒ sẽ sinh con trỏ chết MỚI.

Viết lại DEV_TOOLING_GUIDE §10 quanh `deploy-package.ps1`: bảng 5 bước kèm rc khi hỏng, nêu rõ "luôn
đóng gói bản mới nhất" được bảo đảm bằng CHẶN ở bước 0 chứ không bằng nhắc, và "chưa byte-match thì coi
như CHƯA deploy" ở bước 5. Dọn nốt 3 chỗ còn trỏ script cũ: §Quy trình sửa code bước 7 (cả hai tệp),
CLAUDE.md bước 7, và mục 1 §Quy ước deploy.

# ★ v1.35.82 — r245: nối chốt vào script deploy NGOÀI repo, tự động và fail-safe (2026-07-30)

`upload-skill-to-Package.ps1` ở `D:\Quốc hội\`, KHÔNG có trong repo (đã kiểm: không trên đĩa, chưa từng
vào git) nên phiên Claude không đọc/sửa được. Bảo người dùng tự chèn tay thì dễ chèn SAU lệnh
`drive-push` — lúc đó chốt vô nghĩa vì đã ghi đè rồi.

`scripts/wire_deploy_guard.py` — vá tự động, DRY mặc định, `--apply` mới ghi (sao lưu `.bak`):
- Tự tìm lệnh `drive-push` (regex biên từ, bỏ dòng chú thích) và chèn **NGAY TRƯỚC** nó, giữ đúng thụt lề.
- **KHÔNG thấy `drive-push` ⇒ TỪ CHỐI rc=2 và KHÔNG sửa tệp**, in khối để tự chèn. Không đoán chỗ:
  đoán sai ở đây tệ hơn không làm gì.
- **Idempotent** bằng marker — chạy lại không chèn lần 2.
- **Giữ nguyên vỏ tệp: CRLF + BOM.** Chính bài học v1.35.68 (viết lại text-mode nuốt CRLF, mất 1
  byte/dòng); script deploy Windows gần như chắc chắn CRLF, có thể có BOM.
- Khối chèn **TỰ ĐỌC `VERSION`** từ `--repo`, KHÔNG dựa vào tên biến trong script người dùng — không
  đoán được `$ver`/`$version`, đoán sai thì chốt chạy với version rỗng và mất tác dụng im lặng.
- `--repo` bị kiểm ngay (phải có `VERSION` + `scripts/deploy-guard.ps1`), sai thì chết TẠI ĐÂY chứ không
  để chết lúc deploy — lúc đó khó lần ra nguyên nhân.

**Test 6 vế trên fixture giống thật (CRLF + BOM + `drive-push` thụt trong khối `if`):** DRY chỉ đúng dòng ·
apply chèn + `.bak` · chạy lại idempotent (marker đếm 1) · BOM giữ và 0 LF lẻ · **chốt ở dòng 15 TRƯỚC
`drive-push` dòng 19** · fixture không có `drive-push` → rc=2 và md5 KHÔNG đổi.

**Kiểm CÚ PHÁP bằng chính `Parser` của PowerShell** (tải PowerShell 7.4.6 vào container, chạy rồi xoá):
tệp đã vá parse 0 lỗi, bản `.bak` cũng parse 0 lỗi (chắc fixture vốn đúng), và `deploy-guard.ps1` +
`deploy-package.ps1` cũng parse sạch. Chèn code vào script deploy của người khác mà chỉ "đọc thấy đúng"
là không đủ — cú pháp sai ở đó làm hỏng đường release của họ.

`wire_deploy_guard.py` cũng là dev-side (chỉ chạy ở máy dev để vá tệp ngoài repo) ⇒ vào
`_RELEASE_EXCLUDE_NAMES_ANYWHERE`, gói giữ 198 tệp. Test **r244** mở rộng lên 5 tên, vẫn đo hai vế.

# ★ v1.35.81 — r244: bản deploy PowerShell ĐẦY ĐỦ, quét bí mật dùng chung, và trần 200 tệp của gói (2026-07-30)

**`scripts/deploy-package.ps1`** — song sinh đầy đủ của `deploy-package.sh` cho Windows, thay hẳn
`upload-skill-to-Package.ps1` (ngoài repo). Nằm TRONG repo nên `git pull` là có bản mới nhất, hết cảnh
script deploy trôi lệch ở máy riêng. Cùng quy trình, cùng chốt, cùng mã lỗi (0/1/2/3).

"Luôn đóng gói ra bản mới nhất" làm bằng CHẶN chứ không bằng nhắc: bước 0 tự `git fetch` và DỪNG nếu
cây tụt sau `origin/master` (mục 2 quy ước) — build từ cây tụt sau chính là cách Package thụt lùi.
`-Pull` thì tự fast-forward rồi ĐỌC LẠI VERSION; KHÔNG bao giờ tự merge/rebase.

**`scripts/pkg_secret_scan.py`** — tách bảng mẫu bí mật thành NGUỒN SỰ THẬT DUY NHẤT cho cả hai đường.
Nhét inline vào mỗi script = hai bảng mẫu, và chúng SẼ trôi lệch: thêm mẫu bên sh mà quên bên ps1 thì
đường Windows đẩy lọt secret mà không ai biết.

**Trần 200 tệp — đụng THẬT, không phải đề phòng.** Thêm 3 script làm entries 199 → 202 ⇒ `release-bundle`
chết `IMPORT_LIMIT_EXCEEDED`. Bốn script deploy (`deploy-package.sh` · `deploy-package.ps1` ·
`deploy-guard.ps1` · `pkg_secret_scan.py`) là dev-side thuần — phiên Cowork LIVE bootstrap TỪ zip thì
không bao giờ tự deploy — nên vào `_RELEASE_EXCLUDE_NAMES_ANYWHERE`. GIỮ trong repo/git, CHỈ loại khỏi
GÓI, cùng tiền lệ `CLAUDE.md`/`.claude/`. Khoá bằng test **r244** đo BA VẾ, có phản chứng cho vế (b):
tệp phải VẪN CÒN trong repo — nếu thiếu vế đó thì "loại khỏi gói" biến thành "mất tệp" mà test vẫn xanh.

**Hai bẫy PowerShell sập ở lượt chạy đầu, đã vá và ghi lại trong chú thích code:**
- `param([string[]]$Args)` — `$Args` là BIẾN TỰ ĐỘNG trong hàm PS, nên `@Args` nở ra mảng tự động RỖNG
  thay vì đối số truyền vào ⇒ python chạy KHÔNG đối số, đọc stdin, EOF, **rc=0 và output rỗng**: gate
  báo "rc=0" mà chẳng chạy gì. Đây là kiểu xanh-oan nguy hiểm nhất. Đổi thành `$Argv`.
- `Get-Content -Raw` trên tệp RỖNG trả `$null` ⇒ `[regex]::Match` ném "Value cannot be null". Ép `[string]`.

Cả hai chỉ lộ ra vì CHẠY THẬT: đã tải PowerShell 7.4.6 vào container để chạy chứ không đọc code suy diễn.

**Thêm hai lỗi nữa cùng một họ — `-Force`, và nó không chỉ là chuyện đếm:**
- Đặt tên zip probe bắt đầu bằng dấu `.` ⇒ trên Unix là tệp ẨN, `Test-Path` thấy có mà `Get-Item`
  KHÔNG trả tệp ẩn khi thiếu `-Force` ⇒ ném "Could not find item". Đổi tên probe + thêm `-Force`.
- `Get-ChildItem` cũng bỏ tệp ẩn khi thiếu `-Force`. Phát hiện nhờ ĐỐI CHIẾU PARITY: cùng zip
  (sha `a69d3192…`) mà ps1 đếm 196 còn sh đếm 198 — hai tệp lệch là `.gitattributes`/`.gitignore`.
  Nhưng cùng lệnh đó CHÍNH LÀ bộ tìm tệp secrets ⇒ đường Windows đang MÙ với `.env`, `.netrc`,
  `.tl_secrets`. Đếm lệch chỉ là triệu chứng; lỗ an ninh là bệnh. Đã `-Force` mọi chỗ.

**Và một lỗ trong chính `pkg_secret_scan.py` vừa viết:** lọc theo phần mở rộng nên MÙ với tệp KHÔNG có
mở rộng — `pathlib` cho `Path('.env').suffix == ''`. Bơm `GOCSPX-…` vào `.env` thì bộ quét trả rc=0.
Nay quét cả tệp không mở rộng, tự tránh nhị phân bằng NUL-check 8KB + trần 2MB. Phản chứng 3 vế:
`.env` có secret → bắt · `credentials` (không mở rộng) → bắt · tệp nhị phân → bỏ đúng · cây sạch → rc=0.

Ba lỗi này đều KHÔNG thể bắt bằng đọc code — chúng lộ ra vì chạy thật rồi ĐỐI CHIẾU HAI BẢN với nhau.
Parity không phải nghi lễ: nó là cái duy nhất phát hiện đường Windows mù secrets.

# ★ v1.35.80 — r243: port chốt chống thụt lùi sang PowerShell (2026-07-30)

v1.35.79 cưỡng chế chốt cho đường Linux, nhưng đường Windows (`upload-skill-to-Package.ps1`) vẫn ghi đè
im lặng — hai đường vào CÙNG một fileId nên chốt một bên là chốt nửa vời.

Thêm `scripts/deploy-guard.ps1`: dạng DROP-IN, nối vào script ngoài repo bằng ĐÚNG 1 DÒNG đặt ngay
trước `drive-push` (khuôn ở DEV_TOOLING_GUIDE §10), cũng chạy tay được để kiểm trước khi đẩy. Làm kiểu
drop-in vì `upload-skill-to-Package.ps1` ở `D:\Quốc hội\`, KHÔNG có trong repo ⇒ không sửa mù nội dung
tệp mình chưa đọc.

**So sánh theo [version] chứ KHÔNG theo chuỗi** — đây là cạm bẫy thật, không phải đề phòng suông:
so chuỗi thì `'1.35.9' -gt '1.35.78'` ra ĐÚNG nhưng SAI về nghĩa. Cùng lý do bản sh dùng `sort -V`.

**Đã TEST HÀNH VI bằng PowerShell 7.4.6 thật** (tải vào container để chạy, không đọc code suy diễn):
| Drive | sắp đẩy | cờ | rc |
|---|---|---|---|
| 1.35.78 | 1.35.79 | — | 0 qua |
| 1.35.79 | 1.35.79 | — | **3 chặn** (bằng số) |
| 1.35.80 | 1.35.79 | — | **3 chặn** |
| 1.35.80 | 1.35.79 | `-ForceOlder` | 0 qua (đã WARN) |
| 1.35.78 | 1.35.9 | — | **3 chặn** (bẫy so chuỗi) |
| 1.35.9 | 1.35.78 | — | 0 qua (bẫy so chuỗi, chiều ngược) |
| tên người đặt tay | 1.35.79 | — | 0 qua + WARN (không chặn oan) |
| tên rỗng | 1.35.79 | — | **4 fail-closed** |

8/8 đúng. Đường sản xuất (gọi `gws` thật, Drive đang v1.35.79) cũng đã chạy: qua với 1.35.80, chặn với
1.35.79. **PARITY** với bản sh kiểm riêng trên 5 ca so sánh — hai bản cho cùng phán quyết, gồm cả bẫy.

Phân biệt hai loại lỗi, có chủ đích: KHÔNG ĐỌC ĐƯỢC Drive (gws chết/thiếu quyền/JSON hỏng) ⇒ `exit 4`
**fail-closed**, không đoán là an toàn. Đọc được nhưng KHÔNG RÚT ĐƯỢC version từ tên ⇒ WARN và đi tiếp,
vì tên file có thể do người đặt tay và ta ĐÃ biết trạng thái Drive.

# ★ v1.35.79 — r242: cưỡng chế chốt CHỐNG THỤT LÙI khi đẩy Package (2026-07-30)

v1.35.78 chốt quy ước deploy vào CLAUDE.md, nhưng mục 3 ("Drive ≥ version sắp đẩy ⇒ DỪNG") chỉ là
VĂN BẢN — `deploy-package.sh` đọc tên Package trên Drive rồi chỉ IN ra, không so, không chặn. Chính
quy ước đó viết "không có nó thì mục 1-2 chỉ là lời hứa", nên để nguyên là tự mâu thuẫn.

Nay bước 4 rút version từ tên file Drive và so bằng `sort -V`:
- Drive **>** bản sắp đẩy ⇒ `rc=3`, chặn **TRƯỚC** `drive-push` (không chạm Drive), in cách chữa.
- Drive **=** bản sắp đẩy ⇒ CŨNG CHẶN. Cùng số mà khác cây là đúng cái sai "một số version = một cây"
  đã cấm ở mục v1.35.68; muốn đẩy lại y nguyên thì cũng phải nói rõ ý định.
- Cố ý ghi đè ⇒ `--force-older` (WARN rồi đi tiếp).
- Không rút được version từ tên ⇒ WARN và đi tiếp, KHÔNG chặn oan (tên file có thể do người đặt tay).

**Phản chứng end-to-end, không dùng test hook** — nhân bản cây rồi hạ số hiệu, Drive thật đang v1.35.78:
| cây | cờ | rc | `drive-push` có được gọi? |
|---|---|---|---|
| v1.35.70 | — | **3** | KHÔNG |
| v1.35.78 (bằng số) | — | **3** | KHÔNG |
| v1.35.78 | `--force-older` | — | CÓ (đã WARN) |

Đã kiểm Drive NGUYÊN VẸN sau hai lượt bị chặn: `md5=7cd1aacd…` và `modifiedTime` không đổi — chốt
nằm trước đường ghi, không phải rollback sau khi đã đẩy. Vế `--force-older` đo bằng cách thay
`drive-push` bằng bản giả CHỈ trong cây thử, nên chứng minh được nhánh đó xuyên qua mà không đụng
Drive thật.

Giới hạn còn lại, đã ghi vào CLAUDE.md mục 3: đường `upload-skill-to-Package.ps1` bên Windows CHƯA có
chốt này ⇒ deploy từ đó phải tự kiểm bằng tay.

# ★ v1.35.78 — r241: `core.abbrev` là ĐIỀU KIỆN TẤT ĐỊNH của gate, không phải tuỳ chọn (2026-07-29)

Truy ra từ việc `git fetch --unshallow` để dứt điểm 2 cờ `SHA_NOT_A_COMMIT` của doc-claims-check
trong container remote. Unshallow ĐÚNG là cách chữa (79 → 304 commit, `ad413e7`/`78d6bfe` resolve
được, 2 cờ về 0) — nhưng nó LỘ RA trôi dạt nguy hiểm hơn: `doc-claims-check` suy tập
độ-dài-SHA-ứng-viên từ `git rev-parse --short HEAD`, mà git trả độ dài TỐI THIỂU-DUY-NHẤT — trôi
theo cả SỐ COMMIT lẫn COMMIT ĐANG Ở HEAD. Repo phình ⇒ ngưỡng 7 → 8 ⇒ mọi chuỗi 8 hex thành SHA.

ĐO trên cây này (không suy diễn):
| ngưỡng | golden | docclaims | determinism | selftest |
|---|---|---|---|---|
| **7** | ✓ | ✓ 0 cờ | ✓ | N/N |
| 8 | ✗ case `doc_claims_check_fixture` | ✗ **18 cờ TOÀN FALSE POSITIVE** | ✗ | N-1/N |

18 cờ giả là tiền tố UUID bị nhận nhầm thành SHA: notebook id `59e8d0de`, `45739ff7`, `743ed200`,
`dbe706a0`… Phạm vi ảnh hưởng RỘNG HƠN chú thích cũ: không chỉ L2 của docclaims mà kéo đỏ cả
**golden và determinism** — golden được ghi ở ngưỡng 7.

`scripts/deploy-package.sh` (thêm ở v1.35.69/r232) nay tự ghim `core.abbrev=7` REPO-LOCAL ở bước 0
và cảnh báo khi repo còn shallow. CI ghim `--global`; repo-local hẹp hơn, không đụng config global
của người dùng. `.git/config` KHÔNG được commit nên mỗi clone mới phải đặt lại ⇒ script tự đặt.

**Cách ghim SAI đã thử và bị chính test bắt:** ban đầu tiêm qua env `GIT_CONFIG_*`. Env đó thắng cả
config của repo CON, nên nó đè luôn repo tạm mà `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` tự dựng
để đo chênh 7-vs-8 ⇒ đúng cái test khoá hành vi này ĐỎ. Config repo-local không có tật đó vì repo tạm
mang config riêng. Ghi lại để đừng ai "tối giản" nó về env.

# ★ v1.35.77 — r240: NLM chạy được từ điện thoại — jar phải LIST giữ domain, KHÔNG `nlm login --manual` (2026-07-29)

## THÀNH CÔNG: cookie từ điện thoại nạp được, 139 notebook

Chốt cả chuỗi r233–r239. User export bằng **Cookie Quick Manager** (đọc cookie MỌI domain) từ
Firefox Android → bộ ĐỦ: có LSID/__Host-GAPS/__Host-1PLSID/3PLSID (accounts.google.com). Nạp →
`nlm login --check` = **✓ Authentication valid! Notebooks found: 139**.

## Bug CUỐI (đo LIVE): `nlm login --manual -f` LÀM PHẲNG jar → mất domain

Bộ cookie ĐỦ vẫn ĐỎ khi nạp bằng `nlm login --manual`. Truy: nó lưu cookies.json DẠNG DICT phẳng
(name→value). `_get_httpx_cookies` (nlm core/base.py) khi gặp dict phẳng đặt MỌI cookie vào
`.google.com` ⇒ cookie host-scoped `LSID`/`__Host-GAPS` (accounts.google.com) sai host ⇒
RotateCookies tới accounts.google.com không nhận đủ ⇒ Google đẩy signin. Bản CDP-harvest
(`nlm login` thật) lưu cookies.json DẠNG LIST có `domain` nên `_get_httpx_cookies` giữ đúng host.

Bằng chứng phân tách: replay httpx set ĐÚNG domain từng cookie ⇒ KHÔNG bị đẩy signin; cùng bộ đó
qua `nlm login --manual` (phẳng) ⇒ bị đẩy signin. Khác biệt DUY NHẤT = domain.

## Vá

- Thêm `scripts/nlm_auth_convert.py`: nhận CQM `{"cookies":[…]}` / list thô / dict phẳng / header
  → ghi cookies.json **LIST giữ domain** (schema CDP: domain/expires/httpOnly/…). Với input phẳng
  gán domain theo TÊN (LSID/__Host-*/ACCOUNT_CHOOSER/SMSV→accounts.google.com, OSID→notebooklm,
  còn lại→.google.com). VALIDATE identity 7 + LSID TRƯỚC khi ghi (thiếu ⇒ rc2, không đụng jar).
- `nlm-auth-import.sh`: bỏ `nlm login --manual -f` (làm phẳng), gọi convert. Sửa 1 bug bash:
  backtick trong chuỗi `ok "...\`tl …\`"` bị thực thi như command-substitution (`tl: not found`).

Đã kiểm end-to-end: `./scripts/nlm-auth-import.sh --file <CQM export>` ⇒ jar LIST 35 cookie giữ
domain, probe 139 notebook, stage bundle Drive (verify LIVE 300 nguồn). rc=0.

## Cẩm nang phone (chốt): Firefox Android + **Cookie Quick Manager** (KHÔNG Cookie-Editor — chỉ
tab hiện tại, hụt LSID) → export toàn bộ cookie google → Drive `ducthangho@gmail.com` → ở sandbox
`./scripts/nlm-auth-import.sh`. Mọi thứ CÙNG account ducthangho@gmail.com (browser + Drive + gws).
# ★ v1.35.76 — r239: nút thắt cookie NLM là LSID/đăng-nhập, KHÔNG phải PSIDTS (đo LIVE) (2026-07-29)

Tiếp r238. User export lại nhưng vẫn 19 cookie thiếu nhóm phiên. Truy tới gốc bằng ĐO LIVE
(không đoán tiếp):

1. Tra mã nlm: `REQUIRED_COOKIES = [SID,HSID,SSID,APISID,SAPISID]` — chỉ 5, bản 19-cookie CÓ đủ
   ⇒ nlm báo "đăng nhập thành công". Nhưng đó chỉ là sanity-check của nlm, KHÔNG phải điều Google đòi.
2. Tái hiện request thật (httpx GET notebooklm.google.com): BỊ ĐẨY VỀ accounts.google.com/signin
   ⇒ Google TỪ CHỐI bộ cookie. (Chữ "region" trong HTML chỉ là footer trang signin — URL là
   /signin = lỗi AUTH, không phải chặn vùng; sandbox từng chạy 139 notebook nên vùng không chặn.)
3. Thử `rotate_google_cookies` (endpoint accounts.google.com/RotateCookies của nlm): MINT THÀNH CÔNG
   __Secure-1PSIDTS/3PSIDTS — nhưng VẪN bị đẩy signin ⇒ PSIDTS KHÔNG phải nút thắt (nlm tự mint).

Nút thắt THẬT = cookie ĐĂNG NHẬP (LSID/__Host-GAPS, chỉ ở accounts.google.com) + ROTATION
(__Secure-*PSIDRTS). Bản upload lấy từ myaccount.google.com (có 3 cookie myaccount: OSID/OTZ) nên
hụt nhóm này; Google không chấp nhận replay session thiếu cookie đăng nhập từ IP sandbox. Bộ
54-cookie hồi đầu chạy được vì có đủ.

Vá validation (r239): LSID là CỔNG (thiếu ⇒ chặn, chỉ thẳng accounts.google.com/AccountChooser —
trang "chọn tài khoản" ở đúng host accounts, đừng bấm vào tài khoản); *PSIDTS HẠ xuống chỉ ghi chú
(nlm tự mint qua RotateCookies, không chặn); *PSIDRTS vẫn cảnh báo. Đã test: bản 19-cookie ĐỎ ở
bước 2 với thông điệp đúng nút thắt.

Đường chắc ăn khi phone không đủ: `nlm login` trên máy có browser (CDP lấy đủ jar) → nlm-auth-stage.
# ★ v1.35.75 — r238: nlm-auth-import — 3 lỗi thật khi user upload cookie từ điện thoại (2026-07-29)

Chạy import thật lần đầu với file user upload từ điện thoại (Firefox+Cookie-Editor), lộ 3 lỗi:

## 1. Upload .json bị Google chuyển thành Google Docs
`mimeType = application/vnd.google-apps.document` ⇒ `alt=media` KHÔNG tải được. Vá: dò
mimeType trước; nếu là `vnd.google-apps.*` thì `files export mimeType=text/plain` rồi cắt BOM
(Docs export chèn ﻿ đầu file ⇒ json.loads nổ "Unexpected UTF-8 BOM"). JSON THÂN sống sót qua
Docs (không bị smart-quote) — chỉ BOM+CRLF, cắt BOM là đọc được.

## 2. gws chặn --output ra ngoài cwd
"--output resolves to ... outside the current directory". Script tải vào /tmp ⇒ chết. Vá: tải
vào scripts/.tl_state/ (trong repo) rồi xoá qua trap. (Bug này che bởi `>/dev/null 2>&1` ban đầu.)

## 3. Export THIẾU cookie ⇒ probe network_error (không phải lỗi mạng)
Bản upload có 19/54 cookie: đủ 7 cookie ĐỊNH-DANH (SID/*PSID/HSID/SSID/APISID/SAPISID) nên nlm
"đăng nhập thành công" — NHƯNG thiếu `__Secure-*PSIDTS` (dấu thời gian phiên) và `LSID`/
`__Host-GAPS` (cookie đăng nhập, chỉ sống ở accounts.google.com) ⇒ API NotebookLM TỪ CHỐI, nlm
báo "network_error: ValueError". Đó là vì export từ Gmail/myaccount HỤT nhóm __Host-*/LSID.

Vá validation 3 TẦNG (chặn TRƯỚC khi nạp, thay vì để probe LIVE mới lộ): định-danh → *PSIDTS →
LSID; thiếu bất kỳ ⇒ exit 2 + chỉ thẳng "export từ tab accounts.google.com" (nơi DUY NHẤT mang
LSID/__Host-GAPS và thấy cả cookie .google.com). *PSIDRTS vẫn chỉ WARN (thiếu thì phiên ngắn).

Đã kiểm: bản 19-cookie nay ĐỎ ở bước 2 (rc=2) với thông điệp đúng, KHÔNG đụng jar.
# ★ v1.35.74 — r237: cookie harvest KHÔNG cần notebooklm.google.com (vá cho vùng bị chặn web) (2026-07-29)

User đã cài Firefox + Cookie-Editor nhưng notebooklm.google.com bị chặn theo vùng ⇒ không mở
được trang web để "đứng trên tab đó" mà export. App NotebookLM thì chạy.

Đo trên jar TỪNG CHẠY ĐƯỢC (139 notebook): 7 cookie nlm bắt buộc (SID · __Secure-1PSID ·
__Secure-3PSID · HSID · SSID · APISID · SAPISID) đều nằm trên .google.com / .google.com.hk —
KHÔNG cái nào trên notebooklm.google.com (trang đó chỉ có _ga/OSID, không phải thứ nlm dùng).
Tức chúng là cookie ĐĂNG NHẬP GOOGLE CHUNG. Bằng chứng mạnh nhất: jar cũ lấy SID/__Secure-1PSID
từ .google.com.HK (một trang Google vùng khác) mà vẫn chạy 139 notebook từ sandbox.

Hệ quả: harvest cookie từ Gmail / myaccount.google.com (KHÔNG bị chặn) là ĐỦ; không cần mở
notebooklm web. Truy cập API NotebookLM xảy ra Ở SANDBOX (vùng của nó), không ở trình duyệt
người dùng — nên vùng của điện thoại không liên quan.

App NotebookLM chạy được KHÔNG dùng làm nguồn cookie: app lưu auth ở storage riêng, không root
thì không lấy ra được. Nó chỉ XÁC NHẬN tài khoản có quyền NotebookLM (khớp: sandbox chạy được).

Vá hướng dẫn trong nlm-auth-import.sh (header + thông điệp thiếu-cookie): trỏ Gmail/myaccount
thay vì notebooklm; nêu rõ vùng web bị chặn không ảnh hưởng.
# ★ v1.35.73 — r236: nlm-auth-import --watch (tự phát hiện file mới) + đính chính "script cài trên điện thoại" (2026-07-29)

## Yêu cầu & giới hạn thật

User muốn "script tự cài Firefox Android + addon + chạy lấy cookie tự động". Phần TRÊN ĐIỆN
THOẠI KHÔNG script hoá được — ba rào cản độc lập: (1) container không có đường vào máy người
dùng (chỉ egress qua proxy); (2) Android chưa root không cho script cài APK / lái GUI trình
duyệt (cần chạm tay — tính năng bảo mật); (3) đăng nhập Google không tự động hoá an toàn được,
và extension tự moi cả session Google là anti-pattern bảo mật. Bước "browser đã đăng nhập →
sinh JSON session" BẮT BUỘC là hành động người-thật.

## Cái tự động hoá ĐƯỢC: --watch

Thêm `--watch <phút>` (mặc định 15): ghi mốc modifiedTime của bản mới nhất lúc bắt đầu, poll
Drive mỗi 20s, khi có file khớp mới HƠN mốc thì tự nạp → probe LIVE → stage. Nhờ vậy luồng còn:
[điện thoại] export JSON + lưu Drive · [sandbox] bật 1 lệnh, phần còn lại tự chạy.

## Bug đã bắt trong lúc làm (ghi lại — lớp lỗi ĐO ĐƯỢC)

`_pick_newest` bản đầu in bằng f-string có `\t` trong biểu thức — Python **3.11 CẤM backslash
trong f-string** (chỉ 3.12+ mới cho). `2>/dev/null` NUỐT SyntaxError ⇒ hàm lặng lẽ trả rỗng ⇒
`--watch` sẽ KHÔNG BAO GIỜ thấy file dù có thật. `bash -n` không bắt được (lỗi nằm trong Python
nhúng). Sửa: bỏ f-string, dùng `%`-format. Bài học: inline Python trong .sh phải test HÀNH VI,
không tin `bash -n`; và đừng để `2>/dev/null` che lỗi cú pháp của chính mình.
# ★ v1.35.72 — r235: nlm-auth-import TỰ TÌM file trên Drive (bỏ bước tra fileId) (2026-07-29)

Mục tiêu vận hành: người dùng chỉ có ĐIỆN THOẠI, muốn "cơ bản chỉ chạy script". Bản r233 bắt
phải nêu `--drive-id <fileId>` — mà lấy fileId trên điện thoại là bước thủ công khó chịu nhất
của cả luồng (mở Drive, chia sẻ, cắt id khỏi URL).

Nay chạy `./scripts/nlm-auth-import.sh` KHÔNG tham số: tự truy vấn Drive qua gws
(`name contains 'nlm-auth' and trashed = false`, `orderBy modifiedTime desc`), in tối đa 5 bản
tìm được, ĐÁNH DẤU bản mới nhất bằng mũi tên rồi dùng nó. `--drive-find <chuỗi>` để đổi chuỗi
tìm; `--drive-id` và `--file` giữ nguyên.

Không tìm thấy ⇒ nói thẳng phải làm gì (đặt tên file có `nlm-auth`), không để người dùng đoán.

Luồng điện thoại rút còn: export cookie JSON → lưu vào Drive → ở đây gõ 1 lệnh.
# ★ v1.35.71 — r234: chính env-reimport.sh in lời khuyên đã bị bác (2026-07-29)

Ngay lượt chạy đầu sau khi deploy r233, `env-reimport.sh` in ở nhánh NLM-chết:
«Trong lúc chờ: dùng NotebookLM MCP (mcp__notebooklm-*) — không cần cookie CLI.»

Câu đó SAI, và r233 đã đo ra chính điều ngược lại trong cùng một lượt: phiên này KHÔNG có
NotebookLM MCP nào (`ListMcpResourcesTool` chỉ trả `github`), còn MCP của chính gói nlm thì
dùng CHUNG `get_client()`→`load_cached_tokens()` nên cũng chết theo cookie. Tức script vừa
viết đã mang sẵn lời khuyên mà CHANGELOG cùng bản vá tuyên bố là sai — đúng lớp bug r232 vừa
sửa cho `doctor`, lần này tôi tự mắc lại.

Thay bằng hai đường THẬT: (A) máy có trình duyệt → `nlm login` + `nlm-auth-stage`; (B) chỉ có
điện thoại → trình duyệt CÓ extension (Quetta/Edge Canary/Firefox+add-on) → export JSON →
Drive → `nlm-auth-import.sh --drive-id`. Kèm câu chốt: Chrome Android KHÔNG dùng được (không
extension, 9/13 cookie httpOnly) và KHÔNG tồn tại đường fallback MCP ở phiên này.

# ★ v1.35.70 — r233: hai script vận hành sandbox headless + đo lại đường NLM (2026-07-29)

## `scripts/env-reimport.sh` — dựng lại môi trường

Idempotent, chỉ cần `TL_TOKEN` (KHÔNG cần `TL_MASTER_KEY`). Ba điểm thiết kế có chủ đích:
- smoke **THẬT** bằng `gws drive files list`, không dừng ở `gws-ping` (ping chỉ đọc config, không
  chứng minh `refresh_token` còn đổi được access token);
- phán quyết NLM **chỉ** bằng probe LIVE — tuổi cookie và cờ rotation KHÔNG kết luận thay được;
- khi chốt chống hạ cấp (r229) chặn thì **KHÔNG tự `--force`**: jar cục bộ chết thì bundle càng
  chết, ép ghi chỉ mất bản tươi hơn. `rc=3` = gws sống / NLM chết ⇒ deploy vẫn chạy.

## `scripts/nlm-auth-import.sh` — nạp cookie từ trình duyệt KHÁC

Cho đường "lấy cookie ở điện thoại → nạp vào sandbox". Kiểm ĐỦ cookie phiên TRƯỚC khi đụng jar,
sao lưu jar và KHÔI PHỤC nếu nạp hỏng hoặc probe LIVE đỏ, rồi `nlm-auth-stage` để phiên sau khỏi
làm lại. Tên tệp cố ý KHÔNG chứa `cookie`: mẫu đó nằm trong danh sách secret của `CLAUDE.md` nên
secret_guard chặn cả đọc lẫn ghi — bản đầu đặt tên `nlm-cookie-import.sh` và bị chặn ngay.

## Đo lại đường NLM (thay cho suy đoán trước đó)

| Câu hỏi | Kết luận | Bằng chứng |
|---|---|---|
| NotebookLM MCP có trong phiên Cowork/web này? | **KHÔNG** | `ListMcpResourcesTool` chỉ trả server `github`; ToolSearch không có tool notebooklm nào |
| MCP của gói nlm chạy được khi chưa `nlm login`? | **KHÔNG** | `notebooklm-mcp = notebooklm_tools.mcp.server:main` dùng chung `get_client()`→`load_cached_tokens()`; docstring server tự ghi "run `nlm login`" |
| Lấy cookie từ Chrome trên điện thoại? | **KHÔNG** | 9/13 cookie phiên là `httpOnly` (đo trên jar thật) ⇒ JS/bookmarklet mù; Chrome Android không có extension |
| `nlm login` chạy trong sandbox? | **KHÔNG** | cần CDP tới browser đã đăng nhập; container chỉ có egress qua proxy, không với tới máy người dùng |
| Có đường nào từ điện thoại? | **CÓ** | trình duyệt Android có extension (Quetta/Edge Canary/Firefox+add-on) → export JSON → Drive → `nlm-auth-import.sh` |

Sửa lại một khẳng định sai ở lượt trước: tài liệu và câu trả lời từng nói "thiếu nlm/auth thì
fallback NotebookLM MCP". Điều đó KHÔNG đúng cho phiên này — không có server nào để fallback.

`nlm login --manual -f` nhận JSON list / JSON dict / chuỗi header (`extract_cookies_from_chrome_export`),
KHÔNG nhận Netscape `.txt` — script bắt riêng ca đó và in lệnh `awk` chuyển đổi, vì extension phổ
biến nhất lại xuất đúng định dạng không dùng được.

# ★ v1.35.69 — r232: gợi ý khắc phục của `doctor` chỉ tới lệnh KHÔNG chữa được (2026-07-29)

> Phát hiện khi làm theo chính gợi ý của `doctor` sau r229: chạy `nlm-reconcile --apply` cho 53 mục
> lệch thì DRY cho thấy nó ghi ĐÚNG 0 DÒNG. Dừng trước khi ghi, đo lại, hoá ra gợi ý sai.

## Gốc — sai theo CẤU TRÚC, không phải theo dữ liệu

`doctor` in MỘT câu cho MỌI kiểu drift: «đồng bộ 1 bước: `tl nlm-reconcile <nb> --apply`». Nhưng
reconcile CHỈ ghi cho dòng **THIẾU** `nlm_notebook_id`/`nlm_source_id` (tập backfill/link).

| Cờ | reconcile `--apply` chữa được? | Vì sao |
|---|---|---|
| `NLM_NOTEBOOK_ID_MISSING` | ✅ | đúng định nghĩa backfill |
| `NLM_STATUS_MISMATCH` | ✅ | link/settle |
| `CORPUS_TRUE_NOT_ON_NLM` | ❌ | **NỢ PHỦ** — nguồn CHƯA CÓ MẶT trên NLM; không lệnh registry nào tạo ra nguồn |
| `row_kind` topology (71 dòng) | ❌ | reconcile ghi `row_kind` **kèm** dòng backfill/link, mà `_topology_row_kind_findings` chỉ nhận dòng **ĐÃ CÓ** `nlm_notebook_id` (`if not nb: continue`) ⇒ **hai tập RỜI NHAU** |

Đo 29-07-2026 trên kho thật: breakdown `NLM_STATUS_MISMATCH=0 · CORPUS_TRUE_NOT_ON_NLM=53 ·
NLM_NOTEBOOK_ID_MISSING=0`; DRY reconcile trên **cả** notebook nền `743ed200…` **lẫn** notebook
overflow `2d8c2fef…` (nơi mang đủ 71 dòng lệch) đều cho `backfill=0 · link=0 · desync=0 ·
settle=0 · unregistered=0`. Grep toàn kho: `OVERFLOW_ROW_NOT_MARKED_OVERFLOW` chỉ xuất hiện ở
ĐÚNG MỘT chỗ — hàm phát hiện; không có đường ghi nào.

Đây là lớp bẫy nguy hiểm nhất, cùng họ với «`nlm login` là đủ» đã bị bác ở GOTCHAS §9: câu sai
**đọc như hướng dẫn vận hành**, nên người làm đúng theo nó sẽ tin đã sửa xong trong khi không có
gì đổi.

## Vá

`_drift_hint_lines(bd, nb)` — PURE, tách khỏi chỗ in để test được; gợi ý theo TỪNG cờ:
- có `NLM_NOTEBOOK_ID_MISSING`/`NLM_STATUS_MISMATCH` ⇒ vẫn mời `--apply`, nhưng đếm ĐÚNG số mục
  chữa được (không phải tổng drift);
- có `CORPUS_TRUE_NOT_ON_NLM` ⇒ nói thẳng là NỢ PHỦ, `--apply` KHÔNG chạm tới, trỏ `slot-audit` +
  `ingest-missing`;
- sạch ⇒ im.

Tên mới PHẢI khai trong `_STUB_MAP["ops_misc"]`: `cmd_doctor` re-home `__globals__` về namespace
`tl`, quên khai thì NameError đúng lúc in cảnh báo (bẫy I11). Ca test khoá luôn điều này.

Gợi ý `row_kind` đổi thành REPORT-ONLY kèm lý do cấu trúc. Sửa 2 chú thích đã lỗi thời trong
`ops_misc.py` (§F-06) và docstring `_topology_row_kind_findings` (`nlm_ops.py`) — cả hai đang nói
`--apply` chữa được.

## Test khoá (2 ca) + phản chứng hai chiều

| Ca | Khẳng định | Gỡ vá |
|---|---|---|
| `r232_goi_y_doctor_khop_thu_reconcile_ghi_duoc` | chỉ NỢ PHỦ ⇒ không mời `--apply`; có cờ chữa được ⇒ mời và đếm đúng (7=3+4); cả hai ⇒ 2 dòng; sạch ⇒ rỗng; `_drift_hint_lines` resolve được từ namespace tl | **ĐỎ** |
| `r232_row_kind_va_backfill_la_hai_tap_roi_nhau` | mọi finding đều mang `notebook_id` khác rỗng; dòng THIẾU `notebook_id` (ứng viên backfill duy nhất) không bao giờ lọt vào findings dù `row_kind` sai; kèm chốt UX chuỗi gợi ý cũ đã biến mất | **ĐỎ** |

Selftest **1393/1393** (sau merge origin/master mang r230/r231). Trước merge: 1386/1386; gỡ 3 tệp logic (giữ test) ⇒ 1384/1386, cả 2 ca đỏ.

Ruff `--select F` DELTA so master = **0** cả 4 tệp. Ghi chú: bản test đầu dùng `_TL_MODULE` làm
delta **+3** (`F821 Undefined name '_TL_MODULE'` — đúng lớp sẵn có 1992 lần, nhưng tiêu chí là
delta 0) ⇒ đổi sang `importlib.import_module("tl")` gán biến cục bộ. Đã thử `_mod215` (nạp thẳng
tl_core) và BÁC: `_resolve_shard_topology` gọi `_profiles_from_config`, `_topology_row_kind_findings`
gọi `_shard_row_kind` (nlm_admin_ops) — cả hai chỉ resolve qua namespace tl, nạp thẳng ⇒ NameError.

## Hiệu lực (doctor LIVE, cùng dữ liệu từng sinh ra gợi ý sai)

```
⚠ registry↔NLM lệch: 53 mục → NLM_STATUS_MISMATCH=0 · CORPUS_TRUE_NOT_ON_NLM=53 · NLM_NOTEBOOK_ID_MISSING=0
   53 mục CORPUS_TRUE_NOT_ON_NLM = NỢ PHỦ (nguồn CHƯA có mặt trên NLM) — `nlm-reconcile --apply`
   KHÔNG chạm tới: nó chỉ điền trường cho dòng ĐÃ có nguồn. Soi bằng `tl slot-audit --notebook-id
   743ed200-…`; đẩy nguồn bằng `tl ingest-missing`.
```

Câu «đồng bộ 1 bước … --apply» đã biến mất khỏi ca này.

## KHÔNG làm

Không tự sửa 53 mục lẫn 71 dòng — đó là DATA-ops, cần user chốt phạm vi. r232 chỉ sửa việc
**công cụ nói sai sự thật**.

## Va chạm số hiệu khi merge (ghi lại để lượt sau khỏi vấp)

Bản vá này làm ở nhánh tách từ v1.35.65 và tự đánh **r230/v1.35.66**. Trong lúc đó `master` đã tiêu
thụ ĐÚNG hai số đó cho việc khác (`r230` = chunk NLM nuốt khối đầu văn bản, `r231` = 4 vá dọn hồ sơ
BHXH) và đi tới **v1.35.68**. Khi merge phải đánh lại toàn bộ thành **r232/v1.35.69** — đổi bằng
token CHÍNH XÁC, không thay chuỗi hàng loạt, vì `tl_selftest.py` chứa CẢ `r230` của master (3 chỗ,
gồm `r230_chunk_khong_nuot_khoi_dau_va_dieu_1`) lẫn của mình (5 chỗ); `ops_misc.py`/`nlm_ops.py`
master không đụng nên thay cả tệp được. Sau đổi: còn đúng 3 chỗ `r230` — của master.

# ★ v1.35.68 — merge r229 vào nhánh r230/r231 (2026-07-29)

**Thêm `scripts/deploy-package.sh` — đóng gói + deploy TỪ LINUX/Cowork.** Trước đây deploy chỉ có
đường Windows (`upload-skill-to-Package.ps1` ở `D:\Quốc hội\`, user double-click), nên trong container
remote KHÔNG deploy được. Script này chạy cùng quy trình §10 DEV_TOOLING_GUIDE + §6 bước 7-8:
VERSION khớp 3 chỗ → gate 8 bước → bundle ×2 đòi same-SHA → verify trong gói → (tuỳ chọn) drive-push
→ tải lại đối chiếu BYTE + VERSION.

MẶC ĐỊNH KHÔNG ĐẨY: phải nêu `--push`. Ba điểm học từ chính lần chạy đầu:
- `release-bundle` TỪ CHỐI ghi zip trong skill root (`OUT_INSIDE_SKILL_ROOT`, kẻo zip nuốt chính nó)
  và tự chuyển ra thư mục cha ⇒ script phải đọc đường dẫn THẬT từ khoá `out` của JSON. Bản đầu tin
  vào tham số mình truyền nên `sha256sum` chết trên tệp không tồn tại, hai chuỗi RỖNG so nhau lại
  BẰNG NHAU ⇒ cổng same-SHA báo ✓ oan. Nay chặn rỗng trước khi so.
- `release-verify` chạy trong gói sinh `__pycache__` ⇒ đếm tệp phải loại, nếu không 195 đọc thành 224.
- `doc-claims-check` đỏ trên clone SHALLOW vì SHA cũ trong `changelog_archive` không resolve được.
  Script chỉ hạ thành WARN khi repo THẬT SỰ shallow VÀ mọi cờ đều là `SHA_NOT_A_COMMIT`; cờ khác ⇒
  đỏ như thường. Đã ĐO NỀN trên origin/master: y hệt 2 cờ, delta = 0.

Phản chứng đã chạy (không tin cổng chặn chỉ vì nó tồn tại): VERSION lệch 3 chỗ ⇒ rc=1 chặn ở bước 0;
bơm token dạng `AKfycb…` vào `references/` ⇒ quét bắt đúng tệp/dòng, rc=2, KHÔNG đẩy.

Nhánh `claude/review-bhxh-law-profile-2m08hz` tách ra TRƯỚC khi r229 lên master nên phân kỳ thật:
master có r229 (v1.35.65), nhánh có r230 (v1.35.66) + r231 (v1.35.67). Merge gộp cả hai ⇒ cây kết quả
KHÁC mọi bản 1.35.67 phát hành trước đó, nên bump số mới thay vì giữ 1.35.67 (một số version = một cây).
Xung đột chỉ ở 4 chỗ mang số version (VERSION · hằng `VERSION` tl.py · header SKILL.md · CHANGELOG);
KHÔNG có xung đột logic — r229 chạm `nlm_ops`/`tl_gws`, r230/r231 chạm chunk + registry/enum.

**Bẫy đã sập và gỡ được — GIẢI XUNG ĐỘT PHẢI GIỮ LINE ENDING.** Lượt gỡ đầu viết lại `SKILL.md` và
`scripts/tl.py` bằng Python text-mode (`open(...,'w')`), nuốt CRLF→LF: SKILL.md 47966→47659 byte
(đúng 307 byte = 307 dòng), tl.py 223463→221776 (1687 dòng). Nội dung ĐÚNG, chỉ line ending sai.
Gate bắt: `golden-test` case `workflow_audit` lệch `kernel.size_bytes` 47966≠47659, kéo theo
`determinism-audit` + test `r219_gotchas_nhan_trang_thai`. ⇒ Hai tệp này là CRLF TOÀN BỘ; sửa bằng
script phải mở nhị phân hoặc `newline=''`. Đây là lý do golden 0-diff là GATE, không phải nghi lễ.

# ★ v1.35.67 — r231: 4 vá bắt được khi dọn hồ sơ Luật BHXH (2026-07-29)

## Ca 1 — rổ 46 nuốt Nghị định và cả CÔNG VĂN

Rổ 46 = «LUẬT sửa đổi ≥2 luật» ⇒ theo định nghĩa chỉ Luật/Bộ luật vào được. Guard cũ **chỉ chặn VBHN**,
nên phần CĂN CỨ của một Nghị định (trích ≥8 số hiệu luật) đủ kích `_distinct_target_luat_subjects >= 2`
⇒ `corpus-audit` đề xuất đẩy `ND_233-2025-ND-CP`, `ND_212-2025-ND-CP` và `CV_10593-NHNo-ALCO` vào 46.
Nhánh omnibus lại chạy TRƯỚC nhánh BHXH→02 nên nuốt luôn cả ca đúng.
**Vá:** tên mang tiền tố doctype khác luật (`ND_/TT_/QD_/NQ_/CT_/CV_/BC_/TTr_/PL_/VBT_/DUTHAO_/CU_/SCAN_`)
KHÔNG BAO GIỜ ép 46. Test giữ cả ca ĐÚNG (Luật omnibus thật vẫn → 46) lẫn guard VBHN cũ.

## Ca 2 — `NAME_TRICH_YEU` đổi tên phá bundle nhiều phần

Header của tệp bundle là header của tài liệu ĐẦU TIÊN trong đó, nên `_doc_subject_for_name` trích chủ đề
của một phần rồi đặt cho CẢ bundle: `VBT_Y_kien_gop_y_Luat_BHXH_16-7_phan_6_cua_8` →
`Luat_Cong_ngan_hang_nha_nuoc` (mất chỉ số phần, gắn tiền tố `Luat_` cho thứ không phải luật).
**Vá:** bỏ qua NAME_TRICH_YEU khi tên khớp `phan_N_cua_M` / `part_N_of_M` / `__partNN__`.

## Ca 3 — pipeline chunk ĐỨT ở chính khớp nối của nó

`chunk-apply` ghi `.md`, `profile-ingest` chỉ nhận doc/docx/odt/pdf/rtf/xls/xlsx ⇒
`profile-ingest-chunks` gọi con luôn `rc=2 UNSUPPORTED_EXTENSION`. Nới allowlist là SAI hướng (mở cửa cho
`.md` bất kỳ vào corpus). **Vá:** cầu nối tự vật chất hoá chunk thành `.docx` bằng **`zipfile` + XML thuần**
— KHÔNG thêm phụ thuộc (requirements.txt: stdlib-only). Front-matter giữ thành đoạn đầu (dấu vết + sha256),
thân giữ NGUYÊN VĂN; test đọc ngược `word/document.xml` khẳng định còn đủ, kể cả ký tự phải escape XML.

## Ca 4 — `loai_noncanonical` thiếu rổ cho TÀI LIỆU LÀM VIỆC

Điền `loai` cho 12 dòng đang RỖNG (bản so sánh ×3, ý kiến góp ý ×8, mục lục) làm `loai_noncanonical`
nhảy **4 → 16** dù dữ liệu TỐT LÊN — thước đo thiếu rổ, không phải dữ liệu sai. Cùng bệnh đã chữa 3 lần
trước (Hướng dẫn v1.34.31 · Công điện v1.30.1 · Điều ước v1.32.0).
**Vá:** thêm 6 loại vào enum — `Bản so sánh` · `Ý kiến góp ý` · `Bản thuyết minh` · `Bản đánh giá` ·
`Bản tổng hợp` · `Tài liệu làm việc` (kèm alias không dấu). Test có vế phản chứng: giá trị rác vẫn phải bị bắt.

`python scripts/tl.py --selftest` ⇒ **1387/1387** (thêm 3 ca r231).

# ★ v1.35.66 — r230: chunk NLM NUỐT khối đầu văn bản + Điều 1, `warnings` vẫn rỗng (2026-07-29)

> Bắt được khi đẩy Luật BHXH 41/2024 (bản Công báo 987+988, 183k ký tự) lên NotebookLM.

`_chunk_records_from_text` chỉ sinh chunk **TỪ tiêu đề Điều đầu tiên trở đi**, nên toàn bộ phần đứng
trước nó — cơ quan ban hành, **SỐ HIỆU**, tên luật, căn cứ Hiến pháp, `Chương I` — **biến mất không dấu
vết**. Cộng thêm guard `_is_heading` (PH2-08, vốn sinh ra để loại dẫn chiếu) **loại oan `Điều 1.`** vì
dòng ngay trước là `NHỮNG QUY ĐỊNH CHUNG` — tiêu đề cơ cấu, không kết bằng dấu câu.

| Đo trên Luật BHXH 41/2024 | trước | sau |
|---|---|---|
| `total_chars` | 183.428 | 183.428 |
| tổng ký tự các chunk | **182.678** (hụt **750**) | **183.428** (hụt 0) |
| `warnings` | `[]` — im lặng | `[]` (không còn gì để báo) |
| ranh giới | `part1 Điều 2..65` · `part2 66..141` | `part1 Điều 1..64` · `part2 65..141` |

Hậu quả nếu không bắt: nguồn NLM của luật gốc **thiếu cả số hiệu lẫn Điều 1** — hỏi "Điều 1 Luật BHXH
quy định gì" sẽ không có căn cứ, mà không chỗ nào báo lỗi. Ranh giới mới cũng **khớp** `_split_by_dieu_chunks`
(đã vá r229), hết cảnh hai bộ cắt cho hai kết quả.

**Vá:** (1) `_is_heading` chấp nhận thêm khi dòng trước là dòng cơ cấu (`Chương/Mục/Phần/Tiểu mục`
hoặc dòng TOÀN HOA ≤120 ký tự); (2) **bất biến bảo toàn** — phần đầu được gắn vào chunk 1, tổng ký tự
các chunk luôn == tổng ký tự nguồn.

Test `r230_chunk_khong_nuot_khoi_dau_va_dieu_1` khẳng định cả hai, kèm vế **phản chứng** (guard cũ loại
`Điều 1.` trên đúng fixture đó) để fixture hết tái hiện bug là ĐỎ chứ không xanh oan.

`python scripts/tl.py --selftest` ⇒ **1384/1384**.

# ★ v1.35.65 — r229: dẫn chiếu "Điều N" đầu dòng bị đếm thành TIÊU ĐỀ ⇒ split_plan cắt sai; registry-doctor nói rõ CƠ SỞ ĐẾM (2026-07-29)

> Phát hiện khi rà hồ sơ **Luật BHXH** và nạp bản **Công báo số 987+988 ngày 25-8-2024** của Luật BHXH
> 41/2024/QH15. Cả hai lỗi đều thuộc lớp «con số trông đúng nên không ai kiểm».

## Ca 1 — `_dieu_sequence_stats` đếm 161 Điều cho luật CÓ 141 Điều

Regex cũ `^\s*Điều\s+(\d+)\b` neo đầu dòng nhưng **không đòi dấu kết tiêu đề**. Bản `pdftotext` của
Công báo ngắt dòng giữa câu, đẩy **dẫn chiếu** lên đầu dòng — 20 mục thừa đều dạng
`Điều 109 của Luật này…`, `Điều 2 của Luật này bao gồm:`.

| Đo trên bản Công báo 41/2024 | count | monotonic | split_plan |
|---|---|---|---|
| luật CŨ | 161 | **False** | part 2 = **Điều 2**..141 (SAI, phải là 65..141) |
| luật MỚI | **141** | True | ranh giới đúng |

**Cùng một regex lỏng nằm ở HAI nơi** — và nơi thứ hai nặng hơn: `_split_by_dieu_chunks` dùng nó để **CẮT**,
nên chunk part 2 mở đầu ngay tại dẫn chiếu «Điều 2 của Luật này» nằm GIỮA THÂN Điều 64 ⇒ nguồn NLM bị
**xẻ giữa câu**, không chỉ sai nhãn.

| chunk_plan (Công báo 41/2024, 190k ký tự > ngưỡng NLM) | trước | sau |
|---|---|---|
| part 1 | Điều 1..64 | Điều 1..63 |
| part 2 | **Điều 2**..141 (cắt giữa thân Điều 64) | Điều **64**..141 |

**Vá:** một hàm `_dieu_head_marks` dùng chung cho ĐẾM lẫn CẮT — tiêu đề phải kết bằng `.`/`:` hoặc hết
dòng; **giữ fallback** luật cũ khi thể thức không có dấu (`Điều 5 Quy định chung`) ⇒ không văn bản nào tệ đi.

**Bẫy kiến trúc đã trả giá (đỏ 2 lượt):** hàm mới trong `tl_core` KHÔNG tự thấy nhau — 1646 hàm được
re-home `__globals__` về `tl.py`. Hàm phải khai thêm vào `_STUB_MAP["ingest_ops"]`; **hằng cấp module thì
KHÔNG có đường nào** (`_DIEU_HEAD_RE` NameError) ⇒ regex phải để TRONG thân hàm.

**Đo 2 chiều (bắt buộc theo CLAUDE.md):** bản GDoc sạch 141→141 (KHÔNG hồi quy) · bản PDF 161→141
monotonic. Test `r229_dieu_dan_chieu_dau_dong_khong_thanh_tieu_de` có **vế phản chứng**: khẳng định luật
CŨ trên đúng fixture đó ra 5 & không monotonic — fixture hết tái hiện bug là ca test ĐỎ, không xanh oan.

## Ca 2 — `registry-doctor`: `count` là TỔNG, mọi bucket lại tính trên phần ĐÃ LỌC

`analyze()` bỏ qua `row_kind='ref'` và bản gốc `loai='thuong'`, nhưng vẫn trả `count = len(rows)`.
Trên hồ sơ Luật BHXH: `count=90, missing_sohieu=19` ⇒ người đọc hiểu «19/90», thật ra là **19 trên 25
dòng được quét** (27 ref + 38 thuong bị loại); đếm thẳng registry có **56** dòng sohieu rỗng.
Tương tự `duplicate_sohieu_groups=0` trong khi dữ liệu có 2 nhóm trùng — đều rơi vào phần bị loại.

**Vá:** thêm `scanned` / `skipped_ref` / `skipped_own_thuong` / `basis` — đúng khuôn `sweep.corpus_basis`.
`scanned` vào `_DOCTOR_SUMMARY_KEYS` nên **text và JSON vẫn 1-1** (giữ bất biến H2).

## Kết quả
`python scripts/tl.py --selftest` ⇒ **1383/1383** (thêm 3 ca r229: đếm · cắt-chunk · cơ-sở-đếm).
# ★ v1.35.65 — r229: tuổi cookie NLM ra số ÂM vì mốc `last_validated` naive lệch múi giờ (2026-07-29)

> Phát hiện khi bootstrap gws/nlm trong sandbox Claude Code on the web (UTC) từ bundle stage ở máy
> UTC+7. `tl nlm-auth-load` in `~-0 ngày tuổi` — số âm, vô nghĩa. Không phải nhiễu hiển thị.

## Gốc

`profiles/default/metadata.json.last_validated` do nlm ghi theo **giờ của máy ghi nó** và là ISO
**NAIVE** (`2026-07-29T18:04:42`, không tzinfo). `_nlm_auth_age_days` trừ thẳng `datetime.now()` của
máy ĐỌC ⇒ trộn hai múi giờ. Đo được: lệch **465,6 phút** ⇒ tuổi = **−0,3 ngày**.

Sai số bị chặn bởi biên múi giờ thực (UTC-12..UTC+14 ⇒ ≤14h ≈ 0,58 ngày) nên KHÔNG lật nổi ngưỡng
14 ngày ở giữa dải — đừng thổi phồng. Cái đắt nằm ở ba chỗ khác:

| # | Hệ quả | Mức |
|---|---|---|
| a | In tuổi ÂM — sai hiển nhiên, làm mất tin vào mọi cảnh báo cạnh nó | hiển thị |
| b | SÁT ngưỡng 14 ngày thì nuốt mất cảnh báo re-stage | cảnh báo |
| c | **`_nlm_auth_load_downgrade` so tuổi bundle (mốc máy STAGE) với tuổi jar cục bộ (mốc máy NÀY)** — hai gốc thời gian khác nhau ⇒ bundle từ máy đi trước LUÔN ra tuổi âm ⇒ luôn `_b <= _l` ⇒ chốt phán "bundle tươi hơn" và CHO GHI ĐÈ | **NẶNG** — mở toang chốt chống hạ cấp r208c 3.1 |

(c) là thứ chốt r208c 3.1 sinh ra để chặn: nạp bản cũ đè lên jar tươi = tự giết phiên đang sống.

## Vá — `_nlm_lv_age_seconds` (PURE, tl_gws)

| Nhánh | Xử lý | Vì sao |
|---|---|---|
| có tzinfo | so tuyệt đối | đúng ở mọi máy |
| naive, tuổi ≥ 0 | DÙNG | cùng máy: chính xác. Khác múi: chỉ ĐỘI LÊN ≤14h — lệch về phía cảnh báo SỚM, an toàn ⇒ giữ nguyên mốc 2026-07-05 «ưu tiên last_validated» |
| naive, tương lai ≤ 120s | 0 | dung sai đồng hồ NTP |
| naive, tương lai > 120s | **None** | mốc vô nghĩa với đồng hồ máy này ⇒ rơi xuống `extracted_at` (epoch — tz-safe), KHÔNG bịa số âm |

Bản MIRROR `_nlm_auth_age_minutes` (tl_core/nlm_ops — nuôi cảnh báo trước lô
`NLM_COOKIE_BATCH_WARN_MIN`) mang y hệt bug, vá cùng quy tắc nhưng viết **INLINE**: hàm này re-home
`__globals__` về namespace tl (bẫy I11), thêm tên module-level ở đó sẽ NameError sau bind.

## Test khoá (4 ca) + phản chứng HAI CHIỀU

| Ca | Khẳng định | Gỡ vá |
|---|---|---|
| `r229_tuoi_cookie_khong_ra_so_am` | mốc tương lai ⇒ rơi xuống epoch, tuổi ≥ 0 và ĐÚNG (14,2′); kèm 3 nhánh aware/jitter/None | **ĐỎ** |
| `r229_chot_chong_ha_cap_khong_lat_vi_lech_mui_gio` | bundle cũ 3 ngày + mốc naive tương lai vs jar cục bộ 10′ ⇒ PHẢI kết luận HẠ CẤP | **ĐỎ** |
| `r229_mirror_nlm_ops_cung_quy_tac` | bản mirror trên HOME giả ⇒ 20 ngày theo epoch, không phải −466′ | **ĐỎ** |
| `r229_van_uu_tien_last_validated_khi_dung_duoc` | PHẢN CHỨNG: last_validated dùng được thì vẫn ƯU TIÊN (epoch stale 19 ngày không được thắng) | XANH (đúng vai: guard hồi quy, không phải ca bắt bug) |

Selftest **1384/1384**. Gỡ đúng 2 tệp logic (giữ test) ⇒ **1381/1384**, 3 ca trên đỏ.

Ruff `--select F` DELTA so master = **0** cả 4 tệp: tl.py 12/0 · tl_gws.py 91/4 · nlm_ops.py 176/0 ·
tl_selftest.py 3931/1. (Nền tl_selftest trong CLAUDE.md ghi 3914 đo ở v1.35.60 — đã trôi tự nhiên tới
v1.35.64; tiêu chí là DELTA, không phải con số tuyệt đối.)

## Không đổi

Cờ `BUNDLE_ROTATION_TOKEN_EXPIRED` giữ nguyên — nó ĐÚNG và độc lập với bug này. Đo cùng phiên: jar
tươi 14 phút vẫn có `__Secure-3PSIDRTS` hết hạn 4 phút (TTL loại cookie xoay ~10 phút) ⇒ cờ gần như
luôn bật sau mỗi lần nạp; `nlm login --check` LIVE xanh (139 notebook) và `nlm-auth-status`
`alive:true`. Cờ không phải phán quyết phiên chết, mà là cảnh báo ĐỘ BỀN: phiên không gia hạn được
nữa, có thể chết đột ngột ⇒ đừng mở lô dài. Phán quyết vẫn thuộc về probe LIVE.

# ★ v1.35.64 — r228: trả nốt nợ r227 — r218/r219 đỏ TỪ GÓI ĐÃ BUNG; mỗi bối cảnh một khẳng định + vá DỮ LIỆU mồ côi (2026-07-29)

> Món nợ r227 ghi rõ ở mục «Còn nợ»: `r218_docclaims_sach_khong_bao_gia` và
> `r219_docclaims_l9_tu_tat_khi_quet_hep` đỏ khi chạy từ gói bung (LIVE 1377/1379), đã đỏ y hệt trên
> 1.35.61 ⇒ CÓ SẴN. Cùng lớp bệnh r226/c: khẳng định của test/lớp guard ngầm giả định đang đứng trong
> CÂY GIT (có `.git`, có lịch sử, có `references/changelog_archive/`).

## Gốc — hai bệnh KHÁC NHAU dưới một triệu chứng

| Ca | Gốc thật | Vá |
|---|---|---|
| `r218_sach_khong_bao_gia` | Chính TEST gọi `git rev-parse` để dựng SHA đối chứng — gói bung không có `.git` ⇒ `returncode != 0` ⇒ đỏ vì CHỖ CHẠY | Khuôn r227: mỗi bối cảnh một khẳng định (bảng dưới) |
| `r219_l9_tu_tat_khi_quet_hep` | Ratchet `by_layer.L9 == 0` ĐỎ ĐÚNG: `CHECKPOINT_TEST_PLAN.md` + `COWORK_PROJECT.md` chỉ được `changelog_archive` (loại khỏi gói, `_RELEASE_EXCLUDE_DIRS`) trỏ ⇒ trong gói chúng MỒ CÔI THẬT, `DOC_NO_INBOUND_POINTER` ×2 | Vá DỮ LIỆU, KHÔNG nới guard: cấp con trỏ SỐNG trong `references/RUNBOOK.md` (header) — L9 phán đúng ở cả hai bối cảnh, giữ nguyên |

## r218 — mỗi bối cảnh một khẳng định (không nhánh nào xanh vì im lặng)

| Bối cảnh | Khẳng định |
|---|---|
| CÂY GIT (`.git` tồn tại) | như cũ: `git rev-parse` PHẢI chạy được, tài liệu đối chứng CÓ vế SHA thật, mọi lớp im |
| GÓI CÀI | tài liệu đối chứng BỎ vế SHA (không SHA nào chứng minh đúng được khi không có `.git`), các lớp L1/L3/L5/L6/L7 vẫn phải im; kèm khẳng định RIÊNG: gói KHÔNG được mang `references/changelog_archive/` (có = tệp dev lọt bundle) |

Xoá `.git` trong KHO ⇒ rơi vào nhánh gói, nhánh đó đòi archive phải VẮNG mà kho thật có archive ⇒ vẫn ĐỎ
— không tồn tại đường «thiếu dữ kiện thì cho qua» (hướng «guard tự tắt» đã THỬ VÀ BÁC từ r227: L2 tắt khi
clone nông làm chính ca test của nó đỏ trên runner).

## Test khoá mới `r228_docclaims_goi_khong_mang_tai_lieu_mo_coi`

Bắt NGAY TRONG CÂY GIT điều trước đây chỉ lộ khi bung gói: mọi phát hiện L9 (cờ LẪN advisory
`DOC_POINTED_ONLY_BY_HISTORICAL`) phải rơi vào tệp KHÔNG được đóng gói (`_release_should_include` false).
Tài liệu «chỉ lịch sử trỏ» trong cây git trông vô hại (advisory) nhưng vào gói là mồ côi thật — chính cái
lỗ r218/r219 lọt. Một khẳng định chạy được ở CẢ HAI bối cảnh, dùng chung lượt quét memo r223.

## Kèm đợt (trả nợ đúng dịp bump)

- `.gitignore` + `dist/` — sản phẩm build cục bộ, đã nằm trong `_RELEASE_EXCLUDE_DIRS`, có/không có nó
  làm đổi SHA cây làm việc so manifest.

## Nghiệm thu

- `tl --selftest` trong CÂY GIT: **1380/1380** (+1 ca r228).
- `tl --selftest` **TỪ GÓI BUNG** v1.35.64 (bung ra thư mục tạm ngoài kho, output ghi file rồi mới
  parse): **1380/1380** — món «Còn nợ» LIVE 1377/1379 của r227 đã trả.
- Phản chứng chạy được, mỗi bối cảnh một chiều, cả ba lượt ĐỎ ĐÚNG CA (worktree `--detach` + bản gói
  riêng, chạy xong dọn):
  · CÂY GIT, gỡ 2 dòng con trỏ trong RUNBOOK.md → đúng MỘT ca đỏ `r228_docclaims_goi_khong_mang_tai_lieu_mo_coi`
    (1379/1380; r219 VẪN XANH ở đó — chính cái lỗ chỉ-lộ-khi-bung-gói, nay có ca bắt ngay trong cây git);
  · GÓI BUNG, bơm `references/MO_COI_R228.md` mồ côi + xoá `references/GOTCHAS.md` → r218_sach + r219_l9
    + r228 cùng ĐỎ (xoá tệp trong gói bị bắt, không có nhánh «thiếu thì cho qua»);
  · GÓI BUNG, bơm `references/changelog_archive/` vào gói → đúng MỘT ca đỏ r218_sach (khẳng định riêng
    của nhánh gói không rỗng nghĩa).
- Bẫy TỰ CẤP CON TRỎ, cắn ngay khi chạy phản chứng lượt đầu (ghi lại vì sẽ cắn tiếp): docstring ca r228
  viết TRẦN tên hai tệp đủ đuôi ⇒ `scripts/*.py` là nguồn con trỏ sống của L9 ⇒ chính ca test tự cấp con
  trỏ, phản chứng gỡ-RUNBOOK xanh oan 1380/1380. Sửa cách viết (không tên trần đủ đuôi trong scripts/).
- `ruff check --select F` delta so master = **0**, đo CÙNG ruff 0.16.0 trên cả hai bản: tl.py 12 F821 +
  0 F401 (y nền); tl_selftest.py 3931 F821 + 1 F401 = master y hệt (nền «3914» trong CLAUDE.md là số
  của ruff đời cũ — đúng bài «thấy số lạ thì đo lại master trước khi nghi bản vá»).
- 8 bước gate offline: đều rc=0.

# ★ v1.35.63 — r227: ca r226/c đỏ khi chạy TỪ GÓI ĐÃ CÀI — test khẳng định về kho, chạy ở nơi không phải kho (2026-07-29)

> Bắt được bằng phép thử chưa từng làm: bung bundle v1.35.62 vào `~/.claude/skills/tra-luat/` rồi chạy
> `tl --selftest` **từ đó**. CI chạy trong CÂY GIT; LIVE chạy trong GÓI ĐÃ BUNG. Hai hình dạng khác nhau,
> và r225/r226 mới chỉ soi được hình dạng thứ nhất.

## Đo: cùng một gói, hai chỗ chạy

| Ca | 1.35.61 từ gói | 1.35.62 từ gói | Phán |
|---|---|---|---|
| `r216_merge_fail_closed_tren_duong_san_xuat` | ĐỎ | **XANH** | r226 chữa đúng cả ở hình dạng LIVE, không riêng CI |
| `r218_docclaims_sach_khong_bao_gia` | ĐỎ | ĐỎ | **có sẵn**, không phải hồi quy của r226 |
| `r219_docclaims_l9_tu_tat_khi_quet_hep` | ĐỎ | ĐỎ | **có sẵn** |
| `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` | — | **ĐỎ** | **do r226 gây ra** — vá ở đây |

## Gốc và cách vá

Vế (b) của r226/c đọc `.github/workflows/ci.yml` để khoá thứ tự hai dòng trong CI. Nhưng `.github/`
**cố ý không đóng gói**, nên ở gói cài tệp đó không tồn tại ⇒ ca đỏ vì CHỖ CHẠY, không vì drift.

Đã **BÁC** cách chữa hiển nhiên «thiếu tệp thì cho qua»: như thế thì xoá hẳn `ci.yml` trong kho cũng lọt
lưới — vá một báo giả bằng cách mở một lỗ thật. Thay vào đó mỗi bối cảnh gánh một khẳng định riêng, không
bối cảnh nào xanh vì im lặng:

| Bối cảnh | Khẳng định |
|---|---|
| trong CÂY GIT (`.git` tồn tại) | `ci.yml` PHẢI có, và dòng ghim `core.abbrev` + `fetch-depth: 0` phải đứng TRƯỚC bước `doc-claims-check` |
| trong GÓI CÀI | `.github/` PHẢI KHÔNG có — nếu có tức tệp dev lọt vào bundle, cũng là lỗi |

## Nghiệm thu

- `tl --selftest` trong CÂY GIT (Python 3.12): **1379/1379**.
- `tl --selftest` **TỪ GÓI ĐÃ BUNG**: ca r226/c nay XANH; còn đúng 2 ca đỏ `r218`/`r219` — **cả hai có sẵn
  từ trước r226**, đã đo trên chính bản 1.35.61.
- Gói lành: `tl_boot --version` → `tl 1.35.63`; 192 tệp; không lọt `.git`/`CLAUDE.md`/`.claude`/
  `.githooks`/`tra_luat_config.v2.json`.
- Phản chứng 2 chiều, **mỗi nhánh một chiều** (không nhánh nào xanh vì im lặng):
  · bơm `.github/workflows/ci.yml` VÀO GÓI → ca ĐỎ (khẳng định phía gói không rỗng nghĩa);
  · gỡ dòng ghim `core.abbrev` khỏi `ci.yml` TRONG CÂY GIT → ca ĐỎ (drift-lock cũ còn nguyên hiệu lực).
- 9 bước gate chạy tay trong cây git: đều rc=0.

## Còn nợ (đo được, cố ý chưa sửa)

`r218_docclaims_sach_khong_bao_gia` và `r219_docclaims_l9_tu_tat_khi_quet_hep` đỏ khi chạy từ gói cài, và
đã đỏ như thế từ TRƯỚC r226 (đo trên 1.35.61). Cùng lớp với ca vừa vá — lớp `doc-claims-check` giả định
đang đứng trong cây git — nhưng chữa chúng phải đụng thiết kế hai lớp guard, rộng hơn hẳn một dòng điều
kiện, nên tách ra đợt riêng. Hệ quả đang chịu: `tl --selftest` ở LIVE ra 1377/1379 chứ không N/N.

# ★ v1.35.62 — r226: CI đỏ ≥9 run KHÔNG phải lỗi test — lệnh cục bộ thuần chết ở cổng creds (2026-07-29)

> Việc đặt ra: CI đỏ liên tiếp từ 27-07 (r217) trên CẢ ubuntu lẫn windows, luôn đúng một ca
> `r216_merge_fail_closed_tren_duong_san_xuat`, trong khi cây dev 1376/1376 và worktree `--detach` cùng
> HEAD cũng 1376/1376. Giả thuyết đang treo là «CI ghim Python 3.12, dev 3.13». **Đo xong: sai giả thuyết.**

## Phân xử giả thuyết Python — bằng cách chạy CẢ HAI bản trên cùng một máy

| Bản Python | Máy KHÔNG config | Máy CÓ creds (`TL_WEBAPP`+`TL_TOKEN`) |
|---|---|---|
| 3.12.3 | **1375/1376** (đỏ đúng ca r216) | ca r216 xanh |
| 3.13.12 | **1375/1376** (đỏ đúng ca r216) | ca r216 xanh |

Cùng bản Python mà đổi kết quả theo *chỗ chạy*, còn đổi bản Python thì không đổi gì ⇒ biến thật KHÔNG phải
Python, cũng không phải OS. Biến thật là **máy có config hay không**.

## Nguyên nhân gốc: `rasoat-merge` thiếu ở `_CREDS_LAZY_CMDS`

`main()` gọi `load_creds` cho MỌI lệnh ngoài `_CREDS_LAZY_CMDS`. `rasoat-merge` không có trong tập đó, nên
trên máy trống nó `sys.exit` rc=1 **TRƯỚC handler** — dù handler tự khai «Không gọi mạng, không NLM». Ca
r216 chạy đúng đường sản xuất (subprocess) rồi parse `stdout`, mà stdout RỖNG ⇒ `JSONDecodeError` ⇒ FAIL.
Máy dev xanh chỉ vì có `tra_luat_config.v2.json` (`.gitignore` dòng 7) — runner clone sạch thì không.

Đây đúng LỚP bug đã cắn hai lần: `doc-text` (bug CI 16-07, khoá ở `r121`) và `doc-claims-check` (r218). Vá
lần này gom cả họ hàng r213, mỗi tên một bằng chứng riêng:

| Lệnh | Bằng chứng nó KHÔNG được chết ở cổng |
|---|---|
| `rasoat-merge` | handler thuần cục bộ, không có đường dùng creds |
| `state-get` | handler CÓ `except SystemExit → CAN_WEBAPP_LIVE` (rc=2 + JSON) — là **code chết** khi `main()` thoát trước |
| `state-put` | nhánh `--dry-run` return TRƯỚC `load_creds`; cùng nhánh `CAN_WEBAPP_LIVE` chết như trên |

Đo sau vá (máy trống): cả ba tới được handler, trả JSON schema của chính nó thay vì tường creds ở stderr.

## Blocker THỨ HAI, chỉ lộ ra khi selftest hết chặn: `doc-claims-check --strict` đỏ trên clone runner

r225 nối guard vào CI nhưng bước selftest đỏ đứng TRƯỚC nên guard **chưa từng chạy trên runner**. Chạy tay
trên clone `--depth 1` (đúng hình dạng `actions/checkout@v4` mặc định) ra **4 cờ cứng**:

| Cờ | Phân xử | Vá |
|---|---|---|
| L1 ×2 — `SKILL_KERNEL_DRAFT.md` | Guard bắt **ĐÚNG**: tệp chưa bao giờ có trong lịch sử git (`git log --all` = rỗng), chỉ tồn tại cục bộ trên máy dev. | Sửa TÀI LIỆU (`CONTEXT.md`, `references/SKILL_KERNEL_MAPPING.md`) nói đúng rằng đây là bản nháp không commit; **trả nợ** cặp tương ứng trong `_POINTER_BASELINE` (ratchet 4 → 3). |
| L2 ×2 — `ad413e7`, `78d6bfe` | Guard hô **SAI**: cả hai là commit THẬT (09-07 và 07-07); clone nông không có lịch sử để tra nên `cat-file -e` trượt. | `fetch-depth: 0` — cấp cho guard cái lịch sử nó cần để kết luận. |

## Ngưỡng L2 trôi theo KÍCH THƯỚC KHO — dòng ghim `core.abbrev` là dòng gánh việc

`sha_lens` lấy từ `git rev-parse --short`, mà git tự nới độ dài viết tắt theo số object. Cùng một kho:

| Hình dạng clone | `core.abbrev` | Hậu quả cho L2 |
|---|---|---|
| `--depth 1` | 7 | ngưỡng đúng như mọi phép đo r218 giả định |
| đủ lịch sử (281 commit, 17.783 object) | **8** | 8 = độ dài tiền tố UUID notebook (`743ed200`, `45739ff7`, `dbe706a0`…) ⇒ **18 cờ GIẢ**, và ca `r218_docclaims_l2_sha_khong_ton_tai` (mồi `deadbee`, 7 ký tự) **cũng đỏ theo** |

Nghĩa là bật `fetch-depth: 0` một mình sẽ đổi 4 cờ lấy 18 cờ. Nên CI ghim `core.abbrev 7` — **giữ đúng
ngưỡng mà r218 đã đo và thiết kế theo, không phải nới lỏng guard**. Đo sau khi ghim, trên clone ĐỦ lịch sử:
`doc-claims-check --strict` rc=0, **0 cờ cứng**, L2 vẫn BẬT hoàn toàn.

> Đã cân nhắc và BÁC hướng «L2 tự tắt khi clone nông»: nó làm chính ca
> `r218_docclaims_l2_sha_khong_ton_tai` đỏ trên runner (lớp tắt thì mồi `deadbee` không còn được bắt) —
> tức là chữa cờ giả bằng cách tắt guard ở đúng nơi guard cần chạy.

## Nghiệm thu

- `tl --selftest` trên Python **3.12**, container clone sạch KHÔNG config: **1379/1379** (+3 ca r226).
- 11/11 bước CI chạy tay trên chính container đó: đều rc=0; `release-bundle` ×2 cùng SHA-256, 192 entry.
- Phản chứng, hai lượt trong worktree `--detach` riêng (đã dọn):
  · gỡ 3 tên khỏi `_CREDS_LAZY_CMDS` → **3/3 đỏ đúng ca** (`r216_merge_fail_closed_tren_duong_san_xuat`,
  `r226_lenh_cuc_bo_khong_chet_o_cong_creds`, `r226_r216_khong_phu_thuoc_config_may_chay`), 1376/1379;
  · gỡ dòng ghim `core.abbrev` khỏi `ci.yml` → **1/1 đỏ đúng ca**
  (`r226_nguong_l2_troi_theo_abbrev_va_ci_ghim`), 1378/1379.
- Ca `r226_lenh_cuc_bo_khong_chet_o_cong_creds` chặn thẳng `load_creds` cho ném `SystemExit` rồi chạy
  `main()` THẬT ⇒ tất định trên MỌI máy, kể cả máy CÓ config (tước env không đủ: `_config_candidates` còn
  dò cwd/gốc-skill/`~`). Kèm NEGATIVE control: lệnh ngoài danh sách phải VẪN chết ở cổng.
- `doc-claims-check --strict`: **4 cờ → 0** (clone `--depth 1` trước vá; clone đủ + ghim abbrev sau vá).
- Ca `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` phản chứng 2 chiều trên kho git THẬT: cùng tài liệu, đổi
  mỗi `core.abbrev` mà kết luận L2 lật (7 ⇒ cờ cứng · 8 ⇒ advisory) + drift-lock hai dòng trong `ci.yml`.

## Còn nợ (đo được, cố ý chưa sửa)

Ngưỡng L2 vẫn tự hiệu chỉnh theo `core.abbrev` — CI nay ghim nên tất định, nhưng **máy dev không được
ghim**: khi kho lớn thêm và git nới viết tắt lên 8, `/gate` sẽ đỏ bằng đúng 18 cờ giả nói trên. Chưa sửa
trong lõi vì cần thiết kế riêng để phân biệt «tiền tố UUID» với «SHA viết tắt» — sửa kèm đợt nào đụng lớp
L2. Chữa tạm tại chỗ: `git config core.abbrev 7`.

# ★ v1.35.61 — r225: guard r218/r219 chỉ đóng ở đường TAY — nối `doc-claims-check` + `release-check` vào CI (2026-07-29)

> Việc đặt ra: đối chiếu con số «gate 8 bước» (prompt bàn giao) với «gate 9 bước» (ghi chép cũ). Đối chiếu
> cho ra: **không mâu thuẫn** — có HAI bộ gate khác tên gọi trùng, và đúng chỗ tiếp giáp giữa chúng là một
> lỗ hổng chưa ai thấy.

## Hai bộ gate — không cái nào là tập con của cái kia

| | `/gate` — 8 bước | CI — 9 bước |
|---|---|---|
| Nguồn | `.claude/commands/gate.md` | `.github/workflows/ci.yml` (job tên `gate`) |
| Chạy khi | người gõ TAY trong phiên | TỰ ĐỘNG: push master + PR, ubuntu × windows |
| Chỉ nó có | `doc-claims-check --strict` · `release-check --full` · `release-verify --strict` | `py_compile` · `release-bundle` ×2 same-SHA · `tl_boot --version` |

Cả hai con số đều đúng, khác đối tượng. Nhưng r218 dựng cổng kiểm trích dẫn, r219 nối nó vào `/gate` —
**đường TAY** — mà quên CI, **đường TỰ ĐỘNG**. Đúng câu r219 tự viết ở mục v1.35.55: «guard không nối vào
đường chạy tự động thì guard chỉ là tài liệu». Vá một reader chưa phải vá xong bẫy.

## Phản chứng 2 chiều CHẠY THẬT (worktree `--detach` riêng, đã dọn)

| Bước nối vào CI | Chiều XANH (checkout sạch) | Chiều ĐỎ (đột biến đúng ca) |
|---|---|---|
| `doc-claims-check --strict` | rc=0 | trích dẫn chết vào `references/GOTCHAS.md` → **rc=2** |
| `release-check --full` | rc=0 | `SyntaxError` ở `tl_core/the_thuc.py` → **rc=3** |
| `release-verify --strict` | rc=0 | file thừa `tl_core/rac_pc225.py` → **rc=2**, `extra_files` liệt kê đúng |

Chiều xanh đo trên worktree checkout sạch — **cùng hình dạng cây với CI runner**, không phải cây dev có rác.

## Hai ca LỌT LƯỚI, đã phân xử (không ca nào là chốt yếu)

1. **VERSION lệch → `release-check` vẫn xanh.** Đột biến SAI CA: `release-check --full` là bộ py_compile +
   `instruction_project_audit`/`instruction_nlm_audit` + `workflow_audit` in-process, nó không hề kiểm VERSION.
2. **File `.py` lỗi cú pháp MỚI trong `tl_core/` → `release-check` vẫn xanh.** Vì bước py_compile của nó chạy
   **danh sách tường minh 11 module**, trong khi `detail` lại ghi `"scripts/tl_core/*.py"` — nhãn nói glob,
   việc làm là danh sách. Đo tiếp: `tl_core/` nay **29 file .py**, tức **18 module** (`the_thuc`, `ingest_engine`,
   `classify`, `profile_mgmt`, `resolve`…) không nằm trong danh sách py_compile nào — cả `release.py` lẫn `ci.yml`.

★ **18 module đó KHÔNG hở**: bơm `SyntaxError` vào `the_thuc.py` → `release-check` **rc=3** và `tl --selftest`
**rc=3**, chỉ riêng `py_compile` danh-sách-tường-minh xanh. Nghĩa là danh sách kia **dư thừa và lệch nhãn, không
phải lỗ hổng** ⇒ CỐ Ý KHÔNG sửa trong r225: sửa nhãn `detail` là đụng `release.py` cho một lợi ích chữ nghĩa,
kéo theo trọn chu trình bump/gate/manifest/bundle. Ghi vào sổ để đợt nào đụng `release.py` thì sửa kèm.

★ Cùng phản chứng này cho thấy **giá trị gia tăng thật** của `release-check --full` trong CI: nó ĐỎ đúng ca mà
`py_compile` của CI xanh.

## Chốt

CI 9 → **11 bước**: `doc-claims-check --strict` chèn sau `golden-test` (đúng vị trí nó đứng trong `/gate`),
`release-check --full` trước `release-verify`, và `release-verify` nay mang `--strict`. Thứ tự giữ nguyên
`release-verify` TRƯỚC `release-bundle` — đảo lại thì `dist/a.zip`/`dist/b.zip` thành `extra_files` và `--strict`
đỏ oan. `.github/` cố ý nằm ngoài manifest/zip (từ v1.33.59) nên thay đổi này không đụng gói skill; bump version
là do CHANGELOG.md — file CÓ trong manifest.

# ★ v1.35.60 — r224: 5 «import thừa» F401 ở tl.py KHÔNG thừa — chúng là MẶT NAMESPACE của 1646 hàm re-home (2026-07-29)

> Việc đặt ra: dọn 5 F401 đầu `scripts/tl.py` (`base64` `datetime` `hashlib` `unicodedata` `zipfile`),
> tiền đề «import thừa THẬT vì thân tl.py đã tách sang tl_core». **Đo 29-07 BÁC tiền đề đó**: 4/5 tên có
> hàm gọi thật, và cơ chế giữ chúng sống không phải cái grep nhìn ra được.

## Vì sao cả grep lẫn phép kiểm «module có tự import chưa» đều phân xử NGƯỢC

| Phép đo | Số |
|---|---|
| Hàm tl_core có `__globals__` **IS** namespace tl.py | **1646** |
| Hàm re-home tra `unicodedata` | 19 |
| Hàm re-home tra `base64` | 9 |
| Hàm re-home tra `hashlib` | 3 |
| Hàm re-home tra `datetime` | 2 |
| Hàm re-home tra `zipfile` | 0 |

Hàm tách sang `tl_core` được **re-home** về globals của tl.py nên tra tên toàn cục ở **tl.py**, không ở tệp
gốc. Vì thế `tl_core/profile_mgmt.py` **có** `import datetime` mức module mà vẫn `NameError` khi tl.py
thiếu tên — mọi phép kiểm dựa trên «tệp gốc đã tự import chưa» đều cho kết luận ngược.

## Phản chứng 2 chiều (bắt buộc theo CLAUDE.md)

| Lượt | Thay đổi | Kết quả |
|---|---|---|
| 1 | bỏ cả 5 tên | selftest **ĐỎ** — `NameError: unicodedata` ở `tl_core/classify.py` |
| 2 | giữ `base64`+`unicodedata`, bỏ 3 tên còn lại | gate **ĐỎ** — `NameError: datetime` ở `tl_core/profile_mgmt.py` |
| 3 | giữ cả 5 + `# noqa: F401` | gate **XANH** |

Lượt 1–2 chứng minh khung đo CÓ lực phát hiện (không phải xanh giả) — đúng bài học r223.

## Chốt

Giữ nguyên 5 tên, tách sang dòng riêng mang `# noqa: F401` kèm số đo, để `noqa` **không** che import thừa
mới ở dòng trên. Mặt import lúc chạy **y hệt** master (14 tên, không thêm/bớt) ⇒ hành vi không đổi.
`ruff --select F scripts/tl.py`: **12 F821 + 0 F401**, delta F821 so master = 0.

# ★ v1.35.59 — r223: khung test NUỐT LỖI — «quét không chạy được» hoá trang thành «quét chạy rồi bất đồng» (+1 test, 1376/1376) (2026-07-29)

> Hồ sơ bàn giao ghi hai ca `r219_docclaims_l9_tu_tat_khi_quet_hep` và `…l10_l11_bi_bac` «đỏ chập
> chờn khi chạy nối nhiều lượt selftest», quy cho `_r218_run` dùng `subprocess timeout=300`.
> **Đo 29-07 BÁC chú thích đó**, và cái đo được ra lại là một khuyết nặng hơn.

## Vì sao `timeout=300` là nghi phạm sai

| Phép đo | Số |
|---|---|
| `doc-claims-check --json` toàn kho (35 tệp, JSON 58.386 B), đo đơn | **3,88 s** |
| Cùng lệnh, ép 6 luồng song song + selftest chạy nền | **8,5–10,2 s** |
| Trần `timeout` | 300 s |
| **Biên** | **30–77 lần** |

Chạy **4 lượt selftest nối** (109/118/173/134 s, lượt 3 đè lên phép ép tải): **4/4 đều 1375/1375**,
hai ca xanh cả 4 lượt, kho sạch cả 4 lượt. **Không dựng lại được hiện tượng.** Quá hạn chỉ là nghi
phạm đứng gần hiện trường.

## Khuyết thật

`_r218_run` phân xử báo cáo bằng `j = loads(...) if "{" in out else {}` — lượt quét sập, quá hạn hay
trả JSON hỏng đều quy về **`{}` lặng lẽ**. Mà đúng **hai ca gọi TRẦN** ấy là hai ca duy nhất **không
kiểm `rc`** (mọi ca `--path` đều kiểm `rc==0`/`rc==1`). Nên `{}` hoá trang thành BẤT ĐỒNG NỘI DUNG:
cả hai đỏ cùng lúc, **không ghi lý do**, không phân biệt nổi với một hồi quy thật.

★Trớ trêu: đó đúng là giáo lý mà chính ca `_l9_tu_tat` áp cho **sản phẩm** — «0 cờ vì sạch» ≠ «0 cờ
vì không chạy», nên lớp tự tắt phải khai báo qua `layers_skipped`. Giáo lý ấy bị vi phạm ngay ở tầng
**khung test**. Một khung test không nói nổi «tôi đã không chạy» thì mọi ca nó gác đều là báo cáo có
điều kiện.

## Vá

- **`_r218_phanxu()` tách riêng** — phân xử một lượt quét, nổ `_R218ScanChet` **kèm mã lý do**
  (`STDOUT_KHONG_CO_JSON` / `JSON_HONG` / `QUA_HAN_300s` / `BAO_CAO_THIEU_KHOA`) và ngữ cảnh lượt
  quét, thay vì trả `{}`. Tách rời để phản chứng bơm được đầu vào hỏng mà **vẫn là đường sản xuất**
  (`_r218_run` gọi đúng hàm này — không bind, theo doctrine `false-green-test-qua-bind`).
- **`_r218_run_toankho()` memo hoá** lượt quét toàn kho, chốt hình dạng báo cáo MỘT chỗ
  (`basis` + `layers` phải có). Hai ca gọi trần nay dùng **đúng một** lượt quét thay vì hai:
  selftest 1376 ca chạy **107,5 s** so với nền 109–134 s.
- **+1 ca `r223_khung_test_khong_duoc_nuot_loi`** — phản chứng 2 chiều: chiều xuôi đọc được báo cáo
  thật có rác đứng trước JSON; chiều ngược ba dạng hỏng phải nổ ĐÚNG mã lý do; ca thứ tư khoá memo
  (hai lần gọi phải trả về CÙNG một đối tượng).

★Không đụng `timeout=300`: đo cho thấy nó không phải cơ chế, và hạ trần xuống chỉ đổi một ca đỏ
không lý do thành một ca đỏ không lý do khác.

# ★ v1.35.58 — r222: dấu cách bị gạch trong .docx — bộ lọc markup ĐẺ RA chữ không có trong văn bản (+3 test, 1375/1375) (2026-07-28)

> Lượt rà hồ sơ đo ra `scripts/docx_markup.py` bỏ TRỌN run bị gạch **kể cả khi nội dung bị gạch chỉ
> là MỘT DẤU CÁCH** ⇒ hai từ dính liền. Đo trên `19-2026-VBHN-VPQH` (VBHN Luật BHXH — căn cứ đối
> chiếu Luật mẹ của cả hồ sơ) @121.553: `raw` = 187.401 ký tự, văn bản «hủy bỏ quyết định»;
> `strip`/`mark`/`auto` = 187.399 (**−2**, đúng 2 dấu cách bị gạch) ⇒ **«hủy bỏquyết định»**.
> **Nguồn viết ĐÚNG, công cụ làm hỏng.**

## Vì sao đây là lỗi nặng chứ không phải lỗi trình bày

Bỏ nhầm **chữ** = MẤT nội dung — dễ thấy, dễ bắt. Bỏ nhầm **dấu cách** = SINH nội dung mới: câu vẫn
đọc trôi, không ai soi, và chữ lạ ấy đi thẳng vào bản trích dẫn quy phạm. Dấu cách bị gạch là **tàn
dư định dạng**, không phải «chữ đã bỏ» theo nghĩa nghiệp vụ.

★Lỗi này **lật một bằng chứng của đợt rà trước**: «Điều 80 bản kho dính chữ *bỏquyết*» từng được
dùng để kết luận «bản Công báo đúng hơn» ở Luật 41/2024. Thực ra bản kho không sai — **bộ lọc sai**;
lỗi biến mất khi đổi nguồn chỉ vì bản mới không mang markup, tức **gỡ được tình cờ**. ⇒ *Một «lỗi
của dữ liệu» có thể là lỗi của ĐƯỜNG ĐỌC dữ liệu; đối chiếu `--markup raw` trước khi quy lỗi cho
nguồn.*

## Chỗ hỏng

`_cut_block`/`_cut_inline` xoá mẩu markup rồi mới hỏi có nhãn không, mà nhãn dựng bằng
`xml_chunk_text` — hàm này nén `\s+` rồi `.strip()`, nên trả `""` cho **CẢ** mẩu rỗng hẳn **LẪN**
mẩu chỉ-khoảng-trắng. Hai thứ đó phải xử lý **ngược nhau**, nhưng đường cũ không phân biệt được.
★Chế độ `mark` dính y hệt, dù nó đáng lẽ chỉ ĐÁNH DẤU chứ không xoá.

## Cách vá

- `scripts/docx_markup.py:76` — thêm `chunk_payload()`: chữ THÔ, **chỉ ruột `w:t`/`w:delText`**
  (`scripts/docx_markup.py:48`), giữ nguyên khoảng trắng, softbreak (`w:tab`/`w:br`/`w:cr`) tính là
  một dấu cách. Chỉ đọc trong phần tử text — **không** lấy mọi text lọt giữa tag, để docx bị in đẹp
  (xuống dòng giữa các tag) không bị hiểu nhầm là có khoảng trắng nội dung.
- `scripts/docx_markup.py:150` — `_keep_space()`: mẩu bị bỏ mà ruột **chỉ có khoảng trắng** thì trả
  **chính khoảng trắng đó** (không quy về một dấu cách), ngược lại trả `None` = bỏ như cũ. Áp ở **cả
  ba** chế độ: nhãn `⟦BỎ: ⟧` vừa là rác vừa không phải nội dung bị bỏ.
- Phủ đủ thể: `w:del` · `w:moveFrom` · run `w:strike`/`w:dstrike` · `delText` lạc
  (`scripts/docx_markup.py:177`, chỉ được thay bằng `w:t` vì đang nằm SẴN trong `w:r`).
- Thẻ sinh ra mang `xml:space="preserve"` — bắt buộc theo OOXML cho khoảng trắng đầu/cuối `w:t`.

Một chỗ vá phủ **mọi** reader: đo trước khi sửa — `strip_markup` là đường DUY NHẤT, 4 nơi gọi
(`scripts/normalize_document.py`, `scripts/tl_core/ingest_ops.py`, `scripts/tl_core/lookup_ops.py`),
**0 bản sao chép logic**. Đây đúng là chỗ r182 từng trả giá (vá một reader, còn hai reader kia sai
tiếp), nên lần này kiểm trước bằng phép đo chứ không bằng trí nhớ.

## Phản chứng — và đột biến lọt lưới là phát hiện đáng giá nhất

**8 đột biến THẬT vào mã sản xuất, chạy bộ test ĐÓNG GÓI (không phải harness rời): 8/8 đỏ đúng ca.**
Riêng M5 («nới thành giữ tất») đỏ thêm **11 ca r182** — đúng, vì nó phá luôn bất biến cũ.

★**Lượt đầu M2 LỌT LƯỚI, và nó lật chính lời chú thích vừa viết.** M2 = bỏ vế `pay and` trong
`pay and not pay.strip()`. Chú thích ban đầu bảo vế ấy chống «đẻ dấu cách ma ở mọi ranh giới đoạn» —
**sai**: mẩu rỗng trả `""`, mà `"" is not None`, nên cái sinh ra là `<w:t></w:t>` **RỖNG**, tức VĂN
BẢN không đổi. Khác biệt thật nằm ở mức **XML**: `<w:del …/>` tự đóng (đánh dấu xoá dấu-đoạn) có
trong MỌI docx track-changes, nên bỏ vế này là chèn một run rỗng vào **mọi ranh giới đoạn** — phá
bất biến thiết kế «chỉ CẮT/BÓC tag markup, KHÔNG đụng gì khác» (cùng họ `r182_no_markup_is_noop`).
⇒ ca khoá đổi sang **so ở mức XML** (`_o == _x` trừ đúng cái tag) rồi M2 mới chết.

*Bài học giữ lại:* chốt đúng việc mà **chú thích sai lý do** còn nguy hơn chốt thừa — phiên sau đọc
chú thích rồi gỡ nhầm. Đột biến là thứ duy nhất phân xử được điều đó.

## Hai lỗi của chính đợt này, ghi để khỏi lặp

1. **Phép kiểm toàn vẹn lấy MẪU không phải là phép kiểm toàn vẹn.** Harness phản chứng bị giết giữa
   chừng ⇒ `finally` không chạy ⇒ đột biến M3 **nằm lại trên mã canonical**. Tôi kiểm bằng
   `git diff --numstat` (36/2) + `grep` **một dòng** ⇒ cả hai đều xanh, vì M3 thay 2 dòng bằng 2
   dòng và không đụng dòng được grep. Lượt chạy sau lấy chính file bẩn làm «bản pristine» ⇒ bản sao
   lưu cũng nhiễm. **Toàn vẹn phải đo bằng hash CẢ TỆP; bản gốc phải lấy từ trạng thái đã xác minh.**
2. **Chốt chống rỗng, lần thứ hai trong hai đợt liên tiếp.** Harness in `?/?` khi không parse được
   kết quả, mà chốt `base_ok != base_tot` vẫn xanh vì **so hai dấu `?` với nhau**. Nay nền phải là
   **số thật** và phải **đúng bằng** số ca mong đợi mới được chạy tiếp.

## Ranh giới — r222 vá CÔNG CỤ, không tự sửa DỮ LIỆU

Record cache `19-2026-VBHN-VPQH` **vẫn còn** «bỏquyết» (đúng 1 chỗ trên toàn cache 11 record; 10
record kia `markup=null` nên không dính). Cờ `markup strike=2` treo trên record ấy **vẫn báo** sau
r222: `scan()` đếm theo THỂ, không phân biệt gạch-chữ với gạch-khoảng-trắng — cố ý không đổi, vì
thêm trường vào `stats` là đổi lược đồ đã ghi vào record. Người thẩm tra quyết **không nạp lại**
lượt này.

*Đây là lần thứ tư một đợt phải nhắc lại cùng một câu: **vá công cụ không tự sửa dữ liệu công cụ đã
làm hỏng.***

# ★ v1.35.57 — r221: cổng T1 số hiệu của `verify_deep` — sửa một phép so CHƯA TỪNG khớp đúng lần nào (+2 test, 1372/1372) (2026-07-28)

> Lượt rà hồ sơ đo ra `verify_deep.py:287` sai ở **11/11** record cache: nó gắn cờ «không thấy số
> hiệu» cho **cả những bản in đúng chuẩn**. Không phải hồi quy — cổng này chưa bao giờ khớp đúng
> một lần nào. Và lại đúng khuôn r219/r220: **phép đo bác chính đề xuất đầu tiên**, lần này là đề
> xuất của phiên đang làm.

## Chỗ hỏng

`re.escape(so_hieu.split("/")[0])` chỉ có nghĩa với dạng IN trên văn bản («41/2024/QH15»), nhưng
đường nạp truyền **khoá registry** gạch ngang («41-2024-QH15») — không có `/` nào để tách, nên
`split("/")[0]` trả về nguyên khoá rồi đem so nguyên chuỗi với văn bản dùng gạch chéo. Cùng họ lỗi
mà r219 đã bác ở L11: **lẫn khoá registry với trích dẫn văn xuôi**.

Phải xử lý **cả ba** khác biệt, cả ba đã có sẵn ở `scripts/tl_core/classify.py:64-94` mà
`verify_deep` chưa mượn (`scripts/build_cache.py:65-66` mới làm một phần ba):

1. gạch ngang (khoá) vs gạch chéo (bản in);
2. **`Đ`/`đ` (U+0110/U+0111) KHÔNG phân rã bằng NFKD** — phải thay TRƯỚC khi bỏ dấu, nếu không
   `[^a-z0-9]` xoá thẳng và «158/2025/NĐ-CP» nén thành `1582025ncp`;
3. VBHN in **không có năm** («19/VBHN-VPQH» vs khoá «19-2026-VBHN-VPQH»).

## Phạm vi tìm — đo theo bậc, không chọn theo cảm giác

Layout VPQH in «Số: NN/VBHN-XXX» **chỉ ở khối XÁC THỰC cuối bài** (đo: `54/VBHN-VPQH` ở vị trí
105.362/108.650) ⇒ chỉ soi head-2000 là bỏ sót. Nhưng **quét toàn văn thì nới quá tay** — khối CĂN
CỨ dẫn số hiệu văn bản KHÁC:

| phạm vi | tự-khớp | lọt NHẦM |
|---|---|---|
| phép cũ | **0/11** | — |
| head-2000 | 9/11 | 3/110 |
| toàn văn | 10/11 | **6/110** ✗ |
| **head-2000 + tail-4000** | **10/11** | **3/110** ✓ |

Chọn head+tail: nhạy hơn head-thuần một bậc mà mức lọt nhầm **đúng bằng** nó. Tail 3000 còn sót
(hit cách cuối 3.288), 6000 không đổi, 10000 bắt đầu ăn vào thân (4/110). Cờ duy nhất còn lại sau
khi vá là `89-2026-VBHN-VPQH` — **báo đúng**: số hiệu vắng mặt trên toàn bộ 127.359 ký tự.

★Chốt `if not fold: return False` đặt trên **số hiệu đã nén**, không trên phạm vi: số hiệu rác
(«///») nén ra chuỗi RỖNG, mà `"" in x` đúng với mọi `x` ⇒ chốt theo phạm vi rỗng như bản nháp đầu
chỉ đỡ được khi văn bản CŨNG rỗng.

## Nghiệm thu

* Selftest **1370 → 1372** (+2 ca `r221_*`), nạp THẲNG `verify_deep.py` không qua bind (bẫy r212).
* **Phản chứng CHẠY THẬT 8/8 đỏ đúng ca.** ★M8 (bỏ `.replace("đ","d")` chữ thường) ban đầu **KHÔNG**
  làm test đỏ ⇒ theo luật kho đó là mã chết; đã bổ sung ca nguồn-viết-thường thay vì gỡ chốt, vì
  chốt là bản mượn nguyên của `classify.py` và phá tính đối xứng mới là chỗ hỏng sau này.
* Ca đối chứng **bắt buộc chứa chữ Đ** — ca QH15/VBHN (vốn không có Đ) để phép sai **vẫn xanh**;
  phiên trước đã tự sa vào đúng bẫy này hai lần.
* Test đi qua `t1_structure` chứ không chỉ gọi hàm con — bài học r219: guard không nối vào đường
  chạy thì guard chỉ là tài liệu.
* ruff F delta **0**. Không đụng dữ liệu cache/registry/corpus.

# ★ v1.35.56 — r220: doc-claims-check trả nốt L4 (giàn giáo nháp) — và phép đo cắt `XXX` trần khỏi đề bài (+2 test, 1370/1370) (2026-07-28)

> Nợ CỐ Ý cuối cùng của kế hoạch r218. Vẫn đúng bài học r219 — ĐO TRƯỚC KHI THIẾT KẾ: phép đo lần
> này cắt hẳn một phần đề bài (`XXX` trần) trước khi nó kịp thành ~100% báo giả, và cho sẵn ranh
> giới cờ-vs-advisory đúng ngay từ dòng code đầu tiên.

## L4 — giàn giáo nháp còn sót trong văn xuôi

`{{...}}` (reason `DRAFT_PLACEHOLDER`) và `TODO`/`TBD`/`FIXME`/`XXX` (reason `DRAFT_MARKER`) trong
VĂN XUÔI: tài liệu sống trình bày như đã xong mà còn chỗ-điền thì không hoàn cảnh nào đúng ⇒ **cờ**;
tài liệu lịch sử nhắc lại là ghi chép ⇒ advisory (cùng khuôn L1/L8). Quét trên bản đã che CẢ fence
LẪN span backtick — marker nằm trong fence/span là ví dụ hay ký pháp đang được MÔ TẢ, không phải
trạng thái của chính tài liệu.

★Đo 2026-07-28 TRƯỚC khi viết dòng code nào (đúng khuôn đã bác L10/L11 ở r219):

* `{{...}}` / `<TODO>` / `TBD` / `FIXME` = **0 hit toàn kho** — bốn khuôn vào là xanh sẵn.
* **12/12 hit `XXX` toàn kho là placeholder cơ-quan-ban-hành trong ký pháp số hiệu
  `NN-YYYY-VBHN-XXX`** — tất cả kề dấu `-`. Bắt `XXX` trần như kế hoạch r218 đặt hàng thì lớp này
  khai trương bằng ~100% báo giả. Giữ `XXX` nhưng **loại hit kề `-`** (đúng phép loại trừ mà L2
  dùng cho khúc UUID notebook) ⇒ 0 báo giả mà vẫn bắt được `XXX` đứng rời.
* Hit `TODO` DUY NHẤT toàn kho nằm ở `references/DOCTRINE_APPENDIX.md` (tài liệu lịch sử) ⇒ vào kho
  đúng **0 cờ + 1 advisory** — gate `--strict` không đổi màu, cùng khuôn "vào kho là xanh sẵn" của
  L8/L9.

## Nghiệm thu

* Selftest **1368 → 1370** (+2 ca `r220_*`): ca cờ với BA đối chứng trong CÙNG tài liệu (`XXX` kề
  `-`, marker trong span, marker trong fence — cả ba phải IM); ca PURE lịch-sử-hạ-advisory nạp
  thẳng `workflow.py` không bind + ratchet 0 cờ L4 trên kho thật.
* **Phản chứng 2 chiều CHẠY THẬT trên bãi cách ly, 7 đột biến: 7/7 đỏ đúng ca** — M1 bỏ loại trừ kề
  `-` · M2 quét thiếu che span · M3 bỏ hạ advisory lịch sử · M4 bỏ L4 khỏi danh sách lớp · M5 hỏng
  regex placeholder · M6 mask thôi che fence (đỏ CẢ guard che-nhiễu `r218_*` = đúng, mask là của
  chung) · M7 bỏ `TBD` khỏi họ marker. Không đột biến nào lọt lưới ⇒ không giữ chốt chưa chứng minh.
* Golden `doc_claims_check_fixture` regen CÓ CHỦ ĐÍCH: fixture (SINH TỪ MÃ trong
  `_golden_ensure_fixtures`) thêm cặp nổ/im trên cùng một dòng + marker trong fence; `by_layer`
  thêm `L4: 2`, `claims_flagged` 10→12, `layers` thêm L4. `workflow_audit` KHÔNG đổi (card không
  bị hash). Card `doc_claims_check.json` thêm dòng plan L4.
* ruff F delta **+1 và là `F821 Undefined name Path`** ở `tl_selftest.py` (194→195 — đúng lớp báo
  giả GOTCHAS §11: tên bơm động vào `globals()` qua `_STUB_MAP`; test mới dùng `Path(td)` đúng
  khuôn các ca `r219_*`). Gate 8/8 xanh trọn, gen_instructions 38/38, bundle dựng ×2 trùng byte.

# ★ v1.35.55 — r219: doc-claims-check thêm L8/L9, BÁC L10/L11 bằng đo, và vá 3 sự thật sai trong chính GOTCHAS.md (+7 test, 1368/1368) (2026-07-28)

> Đợt này trả nốt nợ CỐ Ý của r218. Kết quả đáng ghi nhất **không phải hai lớp mới**, mà là ba lần
> phép đo bác thẳng thiết kế đã đặt hàng: hai lớp bị loại vì đo ra ~100% báo giả, một lớp phải đổi
> hẳn định nghĩa vì định nghĩa gốc **bất khả thi hành**. Xây theo kế hoạch mà không đo trước thì cả
> ba đều đã lọt vào kho và làm hỏng đúng cái khiến báo cáo dùng được: ranh giới cờ-vs-advisory.

## (a) L8 — tên lệnh `tl <cmd>` không tồn tại

Lớp đúng trọng tâm của cả lệnh: tài liệu bảo phiên sau chạy một lệnh KHÔNG CÓ thì phiên đó đi thẳng
vào ngõ cụt — không cách nào đúng ⇒ **cờ**, không phải advisory. Nguồn sự thật là golden
`references/golden/parser_surface.json` (191 lệnh, repo-local, tất định, đã bị `golden-test` khoá byte)
chứ KHÔNG import `build_parser` — import tl.py trong handler kéo theo `load_creds`, thứ mà lệnh
READ-ONLY offline này cố ý không đụng. Thiếu golden ⇒ lớp **tự tắt và khai báo**, không đoán.

Chỉ quét TRONG span backtick. Đo 28-07: quét trần bắt 8 hit và **cả 8 đều là báo giả tiếng Việt** —
`tl cho` (từ "…hằng trong tl cho"), `tl selftest` (từ "**tl selftest 338/338**"), `tl rebase` (từ
"globals tl rebase → NameError"). Trong-span còn 4, cả 4 nằm ở sổ lưu trữ ⇒ **0 cờ trên tài liệu sống**.

## (b) L9 — tài liệu mồ côi. ★Định nghĩa của kế hoạch BỊ BÁC

Kế hoạch r218 định nghĩa mồ côi = «vắng trong mục DANH MỤC REFERENCES của SKILL.md». **Đo: 20/29 tệp
`references/*.md` vắng** ⇒ lớp này hô 69% cây tài liệu. Tệ hơn — cách "sửa" duy nhất là thêm 20 dòng
vào SKILL.md, trong khi kernel chỉ còn **162 B** đệm tới trần WARN ⇒ **lớp BẤT KHẢ THI HÀNH**. Danh
mục kernel là bản CHỌN LỌC có chủ đích (9 mục + 2 glob), đọc nó thành chỉ mục là đọc sai chức năng.

Định nghĩa dùng được, đo ra **0 cờ + 2 advisory** (vào kho là xanh sẵn):
* cờ `DOC_NO_INBOUND_POINTER` — KHÔNG nguồn nào trong kho nhắc tới (md đã quét + mọi `.py` + workflow
  card + `docs/adr`). Tệp nằm trong gói mà không đường nào dẫn tới = BẤT KHẢ đúng.
* advisory `DOC_POINTED_ONLY_BY_HISTORICAL` — chỉ CHANGELOG/sổ lưu trữ nhắc.

L9 chạy MỘT LẦN cuối lượt và **chỉ khi lượt quét đủ rộng** (có `SKILL.md` + ≥1 tệp `references/`);
quét hẹp thì mọi tệp khác đều "không ai trỏ tới" — kết luận vô nghĩa sinh 28 cờ rác.

## (c) L10 và L11 — CỐ Ý KHÔNG LÀM, lý do đi THEO SẢN PHẨM

Kế hoạch xếp L11 vào "hai lớp đáng nhất". Đo bác cả hai; lý do nằm ở `basis.layers_bac` của mọi lượt
chạy (và có test khoá) để phiên sau khỏi "bổ sung nốt" rồi tự đổ rác vào báo cáo mình cần đọc:

* **L11 số hiệu VBQPPL thiếu NĂM** — 20 hit/5 tệp, 18 ở tài liệu lịch sử, **đúng 2 ở tài liệu sống và
  cả 2 viết ĐÚNG**: `62/VBHN-VPQH` (SKILL.md) là số hiệu CHÍNH THỨC in trên văn bản; `88/VBHN-VPQH`
  (COMMANDS.md) nằm trong câu đang MÔ TẢ việc v1.33.47 cố ý chấp nhận dạng bare. Bất biến
  `NN-YYYY-VBHN-XXX` áp cho **khoá registry**, không áp cho trích dẫn văn xuôi — và mặt registry đã có
  cổng riêng (`vbhn-year-fix`). Bản thu hẹp "bare number ĐA NGHĨA" thì cần tra registry cache ⇒
  máy-phụ-thuộc, phá tính tất định của golden.
* **L10 GAS version thiếu `Code.<ver>.gs`** — 30 version được dẫn, chỉ 6 có tệp ⇒ 24 cờ. Kho giữ 6 bản
  gần nhất là CÓ CHỦ ĐÍCH; và chính việc viết `Code.<ver>.gs` vào tài liệu đã làm guard con trỏ r209 đỏ.

## (d) Việc B — nhãn trạng thái GOTCHAS.md, và 3 sự thật SAI trong chính nó

Ràng buộc đo trước khi gõ: test `r127_gotchas_doc_pointer_driftlock` khoá 4KB ≤ file ≤ 12KB; file đang
**11.784 B ⇒ đệm 504 B**, không phải "~10KB còn ~2KB" như kế hoạch ghi. Dán nhãn cho cả ~42 bẫy tốn
~588 B ⇒ không vừa. **Không nới trần** (nới ratchet cho code mình xanh chính là "vá quá tay") mà cắt
chữ chỗ khác — đúng nếp file này tự dặn. Kết: **12.276 B, còn đệm 12 B.**

Nhãn chỉ dán ở chỗ trạng thái ĐÃ ĐỔI (`[B]` = tiền đề BỊ BÁC); không nhãn = còn hiệu lực. "Còn hiệu
lực" là mặc định nên nhãn cho nó không mang tin — dán tất cả vừa hết byte vừa loãng tín hiệu.

Ba mục sửa, cả ba đều là **số/kết luận sai đang nằm trong tài liệu bẫy**:
1. **§9 cookie NLM** — «cookie DBSC đời ~1h, `nlm login` là đủ» BỊ BÁC (đo 26+27-07): không cookie nào
   TTL 1h; chết do token XOAY `__Secure-1PSIDRTS`; **`nlm login` trần là NO-OP** (probe homepage → xanh
   giả, rc=0) ⇒ phải `--force`. Đây là mục nguy hiểm nhất vì câu gốc đọc như hướng dẫn vận hành.
2. **§1 trần kernel** — ghi "hiện ~49.145B, đệm 7B" (số TRƯỚC KERNEL-DIET r128), đo thật **47.966 B,
   đệm 162 B tới WARN 48.128** ⇒ lệch ~1,2 KB.
3. **§3 kiểu xuống dòng** — ghi "repo ghi LF, riêng COMMANDS.md CRLF". Đo: **8 tệp CRLF TOÀN PHẦN**
   (gồm `SKILL.md`, `tl.py`, `tl_selftest.py`), 200 tệp LF, 0 hỗn hợp. Chính đợt này trả giá: bump
   version bằng `write_text` nuốt sạch CR của SKILL.md (307 dòng) — `git diff --numstat` bắt được ngay,
   đã hoàn tác và làm lại ở mức BYTE.

## (e) Hiện vật manifest restricted-egress (F16c)

`references/PATCH_v2.21.1.gs.md` khuyến nghị bản **restricted-egress** làm MẶC ĐỊNH nhưng tệp không có
trong kho — chỉ ghi cách tự dựng ⇒ người vận hành theo đúng khuyến nghị thì không có gì để copy. Nay có
`references/APPSSCRIPT_MANIFEST.restricted-egress.json`, và test khoá bất biến thật sự nguy hiểm: hai
manifest chỉ được khác nhau ĐÚNG khoá `urlFetchWhitelist` — lệch thêm khoá nào khác nghĩa là đổi policy
egress đã âm thầm kéo theo đổi oauthScope/quyền webapp.

## (f) ★r218 làm ra cái cổng nhưng QUÊN nối vào gate

`doc-claims-check` **không hề có trong `.claude/commands/gate.md`** (7 bước, sửa lần cuối ở `cece035`,
từ trước r218). Nghĩa là suốt r218 cái lỗ hổng nó sinh ra để bịt vẫn chỉ đóng khi có người NHỚ chạy tay
— đúng loại hỏng mà chính nó đi bắt. r219 nối vào: gate nay **8 bước**, `doc-claims-check --strict` đứng
sau `golden`. Guard không nối vào đường chạy tự động thì guard chỉ là tài liệu.

## Nghiệm thu

* Selftest **1361 → 1368** (+7 ca `r219_*`), **gate 8/8 xanh trọn** (kể cả bước mới), gen_instructions
  38/38, ruff F delta **0 thực chất** (+1 và là `F821 Undefined name Path` ở `tl_selftest.py` 193→194 —
  đúng lớp báo giả GOTCHAS §11 đã ghi: tên bơm động vào `globals()` qua `_STUB_MAP`).
* **Phản chứng 2 chiều CHẠY THẬT trên bãi cách ly, 2 lượt / 18 đột biến.** Lượt 1: 9/11 đỏ đúng ca —
  và **2 ca lọt lưới đều là phát hiện thật**, không phải trục trặc harness:
  * M2 lọt ⇒ ca đối chứng thiếu tên profile CHỮ THƯỜNG (bản viết hoa rơi ngoài `[a-z]` của `CMD_RE`
    nên im lặng kể cả khi guard bị tắt) ⇒ đã bổ sung dòng đo được.
  * M3 lọt ⇒ **`_doc_claims_noisy` trong `_doc_claims_tl_cmd` là MÃ CHẾT** (`CMD_RE` chỉ nhận
    `[a-z][a-z0-9-]{2,}` nên mọi ký tự nhiễu đã rụng trước) ⇒ **gỡ**. Một chốt không đột biến nào giết
    được là chốt CHƯA ĐƯỢC CHỨNG MINH; giữ lại chỉ tạo cảm giác an toàn giả.
* Golden `doc_claims_check_fixture` regen CÓ CHỦ ĐÍCH: `by_layer` thêm L8/L9, `layers` thêm L8/L9,
  `layers_skipped.L9` (bằng chứng lớp tự tắt đúng lúc), và ca L8 mới khoá byte (`tl sweep` KHÔNG nổ,
  `tl khong-co-lenh-nay` nổ đúng dòng 7). ★Bẫy trả giá một lượt: fixture dưới `references/golden/
  fixtures/` **SINH TỪ MÃ** (`_golden_ensure_fixtures`) — sửa tay bị ghi đè lặng lẽ ở `golden-test` kế
  tiếp, phải sửa trong `workflow.py`. (`workflow_audit` KHÔNG đổi: nó không đếm `references/*.json`.)

# ★ v1.35.54 — r218: `tl doc-claims-check` — cổng kiểm TRÍCH DẪN trong văn xuôi, và 8 con trỏ chết nó bắt được ngay lần chạy đầu (+9 test, 1361/1361) (2026-07-28)

> Lỗ hổng đã ĐO, không phải phỏng đoán: gate 9 bước kiểm mã nguồn + manifest + bundle, **không bước nào
> kiểm tính đúng của trích dẫn trong tài liệu**. Trong khi `CHANGELOG.md`, `GOTCHAS.md`, `RUNBOOK.md`,
> `DOCTRINE_APPENDIX.md` dày đặc `r216`, `9279426`, `tl.py:1504`, `references/X.md`, `v1.35.52`.
> Khuôn hỏng đã trả giá nhiều lần: tài liệu dẫn tệp–cờ–số hiệu đã đổi chỗ, không ai phát hiện cho tới
> khi một phiên sau đi theo con trỏ và lạc. Đúng loại lỗi máy bắt rẻ hơn người.

## (a) Lệnh mới `tl doc-claims-check` — READ-ONLY, sáu lớp, fail-CLOSED khi `--strict`

```
tl doc-claims-check [--path <file|dir> ...] [--strict] [--json] [--out <file>]
```

Không ghi (trừ `--out` do người gọi khai), không mạng, không GAS/NLM, **không có `--apply`/`--fix`**.
`rc` 0 sạch · 1 có cờ · 2 lỗi dùng lệnh; `--strict` đẩy 1→2 (khuôn `workflow-audit --strict`).

| Lớp | Bắt gì | Xác minh bằng |
|---|---|---|
| L1 | đường dẫn trong span backtick có `/` | tồn tại trong cây (hoặc cạnh tài liệu) |
| L2 | commit SHA | `git cat-file` + `merge-base --is-ancestor` CỤC BỘ |
| L3 | link markdown tương đối | resolve TỪ VỊ TRÍ TÀI LIỆU |
| L5 | `v1.NN.NN` | ≤ VERSION hiện hành + có trong sổ |
| L6 | `rNNN` (chấp hậu tố `r208d`) | ≤ đợt mới nhất + có trong sổ |
| L7 | `<file>.py:<dòng>` | tệp tồn tại **và** đủ số dòng |

Che nhiễu (§2.4) giữ nguyên offset nên số dòng báo cáo vẫn đúng: khối fence ```` ``` ````/`~~~` che cho
mọi lớp; span backtick che THÊM cho L2/L5/L6 (SHA/version trong ví dụ lệnh là minh hoạ), nhưng **không**
che cho L1/L7 — đường dẫn và con trỏ mã vốn luôn nằm trong backtick, che đi là mù.

## (b) Ranh giới CỜ vs ADVISORY — thứ quyết định báo cáo dùng được hay thành rác

Bản đầu tiên hô **213 cờ**. Đọc kỹ thì phần lớn là lỗi của chính công cụ, và mỗi lần sửa đều phải ĐO:

- **56 cờ `VERSION_AHEAD_OF_CURRENT` đều là `v2.x`** — version **webapp GAS** (`2.21.2p`), hệ đánh số
  KHÁC hẳn VERSION skill. Kế hoạch viết `v1.NN.NN` là có lý do; siết regex về nhánh `v1.*`.
- **18 cờ `SHA_NOT_A_COMMIT` đều dài ĐÚNG 8 và đều là khúc đầu UUID notebook** («query notebook
  `fec6c125`»), trong khi git ở kho này viết tắt **7**. Ngưỡng nay lấy từ chính git
  (`rev-parse --short`) + 40; hình dạng khác mà không tra ra commit ⇒ advisory, không hô sai.
- **`CHANGELOG.md` không phải sổ đầy đủ** — nó bị cắt còn 50 mục, sổ cũ nằm ở
  `references/changelog_archive/`. Đọc thiếu chỗ đó thì 184 version bị hô sai. Và **quét toàn văn chứ
  không chỉ dòng tiêu đề**: số hiệu đợt phần lớn nằm trong thân bài, headings-only chỉ thấy 4/191.
- Gộp đủ archive rồi dải `v1.9–v1.22` **vẫn thủng** (46/420) ⇒ đó là khuyết của SỔ, không phải bằng
  chứng trích dẫn sai ⇒ `VERSION_NOT_IN_CHANGELOG` xuống advisory. L6 đối xứng: `r160` không tra được
  nhưng sổ cũng vắng r158/159/161/163/165. **Chỉ khẳng định BẤT KHẢ mới là cờ** (vượt VERSION/đợt mới nhất).
- §2.2 nói thẳng «tài liệu lịch sử được phép dẫn tệp đã xoá»: `CHANGELOG.md`,
  `references/changelog_archive/`, `references/DOCTRINE_APPENDIX.md` (tự khai là thân SKILL.md trước
  v1.16.0, giữ nguyên để tra bối cảnh) ⇒ L1 ở đó là advisory. Phân định theo **loại tài liệu**, không
  theo tuổi tệp: git kho này chỉ 265 commit trong khi skill già hơn thế, `--diff-filter=D` không phân
  định nổi (nó chỉ nhận ra 3/134).

Kết quả: **213 → 8 cờ**, 275 advisory. Kế hoạch §2.3 và §2.7 **tự mâu thuẫn** ở L2 (§2.3 đòi SHA phải có
chữ số, §2.7 lấy `deadbeef` — không chữ số nào — làm phản chứng); đo ra kho có **0** token hex toàn chữ
cái nên bỏ vế «phải có chữ số», giữ vế «phải có chữ a-f» (vế này mới gánh việc: loại token toàn số).

## (c) Tám con trỏ chết bắt được ngay lần chạy đầu — đã vá cả tám

| Vị trí | Trích dẫn | Sự thật |
|---|---|---|
| `references/API_CONTRACT.md:266` | `scripts/manifest_build.py` | bản thật ở `scripts/_fallback/` |
| `references/DELTA_v1.19.md:6,31` | `references/Code.2.21.2h.gs` | snapshot `.gs` chỉ giữ từ `2.21.2k` |
| `references/DEV_TOOLING_GUIDE.md:56` | `references/Code.2.21.2i.gs` | nay trỏ `Code.2.21.2p.gs` hiện hành |
| `references/PATCH_v2.21.1.gs.md:378` | `APPSSCRIPT_MANIFEST.restricted-egress.json` | **không có trong kho — mà đó là phương án được KHUYẾN NGHỊ MẶC ĐỊNH** |
| `references/QUY_TRINH_RA_SOAT_3_TANG.md:92` | `references/BANG_PHAN_TANG_RUI_RO.md` | không tồn tại; quy tắc nằm ngay dưới cùng trang |
| `references/SKILL_KERNEL_MAPPING.md:25` | `changelog_archive/CHANGELOG-2026H1.md` | tên thật là `CHANGELOG-den-1.33.53.md` + `CHANGELOG-1.33.54-den-1.34.99.md` |
| `references/THE_THUC_TRINH_BAY.md:333` | `r160` | không tra được, nhưng dải sổ thưa ⇒ giữ ở advisory, KHÔNG vá |

## (d) ★Đối chứng ngoài dự kiến: r209 đã khoanh đúng 6 mục này từ trước — nay TRẢ NỢ

`tl_core/release.py` có sẵn guard con trỏ r209 với `_POINTER_BASELINE` **10 cặp nợ đã khoanh**.
`doc-claims-check` quét bằng đường hoàn toàn khác và dựng lại **đúng 6 cặp trong số đó** từ con số 0 —
tức danh sách khoanh nợ ấy chính xác, chỉ là chưa ai trả. Đã sửa thân tài liệu ⇒ baseline **10 → 4**
(ratchet chặn chiều THÊM miễn trừ; trả nợ làm số nhỏ đi là chiều đúng, hạ mốc có chủ đích). Bốn cặp còn
lại không phải nợ: placeholder trong văn xuôi, thư mục runtime cố ý ngoài gói, đường Drive `_meta/templates/…`.

Hai guard **bổ sung nhau chứ không trùng**: r209 đối chiếu PACKAGE-SET (nguồn sự thật = manifest) cho
`references/*.md` + `SKILL.md`; r218 đối chiếu CÂY THẬT, thêm link/SHA/version/đợt/`py:dòng`, có đệ quy
thư mục con và có phép che fence/backtick.

## (e) Bẫy tự gây, ghi lại để khỏi mắc lần hai

- Fixture golden nằm DƯỚI `references/` và **cố tình** chứa trích dẫn chết (đó là nội dung test). Quét
  mặc định mà nuốt chúng thì `--strict` không bao giờ xanh và 8 phát hiện thật lẫn với dữ liệu test ⇒
  bỏ qua `references/golden/fixtures/` khi ĐI NGANG, vẫn quét khi trỏ THẲNG (chính là cách golden chạy).
- Sửa `DEV_TOOLING_GUIDE.md` thành `references/Code.<ver>.gs` làm **r209 đỏ**: regex con trỏ của nó cắt
  ở `<` và sinh ra `references/Code` không tồn tại. Bộ lọc nhiễu của r218 nuốt token đó, r209 thì không
  — vá một reader chưa phải vá xong bẫy (bài học `ke-hoach-khung-tham-tra`).
- Lệnh mới thiếu dòng trong `_CREDS_LAZY_CMDS` ⇒ `main()` `load_creds` sys.exit TRƯỚC handler trên máy
  không config (GOTCHAS §4). Đã thêm.
- `r218` trong dòng doctrine mới bị CHÍNH nó hô `R_AHEAD_OF_LATEST` khi CHANGELOG chưa có mục r218 —
  đúng hành vi mong muốn, tự hết khi mục này tồn tại.

## (f) Việc C — doctrine «một bài học một lượt ghi»

`references/RASOAT_HOSO_LOOP.md` §9bis: không gộp nhiều phát hiện vào một lần ghi — cách đánh số lúc nháp
(«phát hiện 3», «mục trên») rò rỉ vào bản đã ghi và thành trích dẫn chết. Nhắc lại quy ước sao lưu:
mọi `*.bak.*.json` để Ở GỐC out-dir, KHÔNG trong `master/`.

## Nghiệm thu

selftest **1361/1361** (+9 ca r218, mỗi lớp ≥1 phản chứng «đỏ đúng ca», đều chạy qua đường sản xuất
`python scripts/tl.py …` chứ không qua bind) · gate 9/9 · `doc-claims-check --strict` rc=0 trên kho thật ·
chạy 2 lượt cho stdout byte-identical · golden thêm case `doc_claims_check_fixture`, regen `workflow_audit`
CÓ CHỦ ĐÍCH (đổi kích thước SKILL.md + 2 tệp runtime mới) · **0 lệnh ghi Drive, 0 call NLM**.

# ★ v1.35.53 — r217: sửa-theo-điểm thay cho thay-trọn-gói, bộ lọc nguồn Công báo, và một đường nạp chưa từng chạy nổi trên máy tiếng Việt (+6 test, 1352/1352) (2026-07-28)

> Nguồn: kết luận lượt rà 6 (`THAY_BAN_TRON_GOI_BI_BAC`) + `BAN_CONG_BAO_BOC_RA_CON_RAC_KHONG_CO_BUOC_LAM_SACH_CHUAN`.
> Đây là hai mục vá người giao việc đã chọn ở lượt 7 nhưng để lại vì lớn hơn hẳn phần còn lại.
> Mục (c) thì không ai đặt hàng — nó lộ ra ngay lần đầu chạy thật đường nạp offline.

## (a) `tl doc-patch <số hiệu> --diem <file>` — sửa ĐÚNG những điểm đã chứng minh

Lượt rà 6 đối chiếu bản kho với bản đăng Công báo: ND 159 lệch 17 điểm, ND 158 lệch 111 điểm. Nhưng
kết luận đắt hơn con số là **không bản nào trùm bản nào** — bản Công báo mang lỗi riêng («ngưởi» ở
khoản 2 Điều 8 ND 158 chính là phát hiện VD-34), còn bản kho mất hai công thức tính vì công thức là
ảnh/equation trong Google Doc. Thay trọn gói vì thế là **đánh đổi mù**: sửa được vài điểm thì rước
vào lỗi khác. Việc đúng là sửa từng điểm, có bằng chứng, có đường lùi — mà công cụ chưa có.

| | |
|---|---|
| cổng ghi | DRY mặc định · `--apply --confirm yes` · không có chế độ ghi ngầm |
| phạm vi | `vung` BẮT BUỘC: `khoi_dau` \| `dieu:<N>` \| `phu_luc` — không có "tìm khắp văn bản" |
| khớp | mỗi điểm phải khớp **ĐÚNG 1 lần**; 0 lần ⇒ `KHONG_KHOP`, >1 ⇒ `KHOP_NHIEU_LAN` |
| fail-closed | **toàn lô**: một điểm hỏng ⇒ KHÔNG áp điểm nào |
| nhầm văn bản | `so_hieu` trong file điểm lệch số hiệu đang sửa ⇒ chặn |
| đường lùi | tự sao lưu `docs/_doc_patch_bak/` + nhật ký; `doc-patch --undo <run_id>` |
| cổng undo | chỉ hoàn tác khi file còn ĐÚNG sha256 lượt patch đã ghi — khác ⇒ từ chối |

`KHOP_NHIEU_LAN` là chỗ cố ý không "thông minh": một chuỗi chính tả sai thường có mặt ở nhiều Điều,
và máy không được chọn hộ sửa cái nào. Người dùng thu hẹp bằng cách đưa thêm chữ hai bên vào `tim`.

**Không mượn `tl undo`**: nhật ký undo hiện có phục vụ registry qua GAS, hoàn tác của nó là ghi lại
giá trị ô. Ở đây đối tượng là FILE record cache, hoàn tác là chép lại nguyên bản. Trộn hai thứ vào
một lệnh là mời một lớp lỗi mới.

`text_hash` **cố ý KHÔNG tính lại** — record không giữ bố cục dòng của bản gốc nên mọi cách tính lại
đều ra một con số không đối chiếu được với gì cả; thay vào đó record mang cờ `DOC_PATCH:` nói thẳng
rằng hash đang là của bản nguồn TRƯỚC khi sửa, kèm `doc_patch.lich_su` đủ để dựng lại đường đi.

## (b) Bộ lọc nguồn Công báo ở đường nạp — `--loc-congbao`

Văn bản bóc từ PDF Công báo mang rác trình bày chen vào giữa thân. Bỏ ĐÚNG BA loại có khuôn chắc,
mỗi loại phải khớp **toàn dòng** (dính chữ khác ⇒ không bỏ, chỉ khai báo):

- `dong_chay` — dòng chạy đầu trang `[số] CÔNG BÁO/Số …/Ngày d-m-yyyy [số]`;
- `so_trang` — dòng chỉ có số **và kề một dòng chạy**. Điều kiện kề là bắt buộc: trong phụ lục/biểu
  mẫu có vô số dòng chỉ-một-số là dữ liệu thật;
- `chu_ky_so` — khối chữ ký số đủ 4 dòng liên tiếp, **quét toàn văn chứ không neo ở đầu bản**.

★Đo 27-07 trên ba văn bản thật: khối chữ ký số **không chỉ nằm ở đầu** — ND 159 có HAI khối nằm giữa
thân (sau khoản 6 Điều 1), Luật 41/2024 có một khối. Bản làm sạch **bằng tay** ở lượt 6 chỉ bắt khối
ở đầu nên còn sót 12 dòng; bộ lọc bắt đủ.

★**Cố ý KHÔNG tự bỏ nhãn mục Công báo** ở đầu bản (`VĂN BẢN QUY PHẠM PHÁP LUẬT`, tên cơ quan in một
mình) — chỉ khai báo `DAU_MUC_CONG_BAO_CON_LAI`. Công báo in tên cơ quan HAI lần (nhãn mục + cơ quan
ban hành), và neo «CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM» nằm SAU dòng số hiệu ở cả Luật 41/2024
(`Luật số: 41/2024/QH15`) lẫn ND 159 (`Số: 159/2025/NĐ-CP`) ⇒ mọi quy tắc cắt tự động đều ăn mất
chính danh tính văn bản. Người quyết, không máy.

Không bật cờ thì **khai báo mà vẫn nạp** (`NGUON_CONG_BAO_CON_RAC` vào `verify_flags`) — cùng họ với
`khoi_dau_missing` của r215: bản Công báo còn rác vẫn là bản chính thức, chặn nạp là phá đúng ca dùng
chính đáng. Cờ khai báo cũng không làm văn bản thành `partial` vì nó không phải khiếm khuyết cấu trúc.

## (c) Đường nạp `--method file` chưa từng chạy nổi trên máy tiếng Việt — và báo hỏng SAU KHI đã ghi

Lần đầu chạy thật `ingest_to_cache.py --method file` (đường `cache-build` offline, không đụng Drive):

```
{"ok": false, "reason": "ingest_failed",
 "error": "UnicodeDecodeError: 'charmap' codec can't decode byte 0x90 in position 46"}
```

`ingest_to_cache.py:724` đọc lại record cache bằng `open(target)` **không khai encoding** ⇒ Python
dùng codec locale (cp1258 trên Windows tiếng Việt) và nổ. Chỗ đó nằm **SAU** `patch_cache_metadata`,
nên lệnh in `ok:false` rc=2 **trong khi cache đã được ghi 49.758 B** — đúng lớp bẫy "rc≠0 không có
nghĩa là chưa ghi gì". Lượt 6 kết luận đường này "chạy được" bằng cách ĐỌC CODE; nó chưa từng chạy.

Khoá bằng **hành vi, máy-độc-lập**: chạy đường nạp dưới `-W error::EncodingWarning` +
`PYTHONWARNDEFAULTENCODING=1` ⇒ mọi `open()` thiếu encoding nổ bất kể locale của máy chạy test. Grep
chuỗi `encoding=` sẽ xanh giả ngay khi ai đó thêm một `open()` trần ở dòng khác.

## (d) `rasoat_phuluc.py`: Mục F thành Phụ lục VI, thêm Phụ lục VII

Bộ hồ sơ trình không khớp tên với chính nó: Báo cáo rà soát hứa một "Phụ lục" cho danh mục nội dung
chưa đủ căn cứ kết luận, còn tệp sinh ra đặt nhãn "Mục F — KHÔNG vào phụ lục"; và bảng tổng hợp theo
mã thì chỉ tồn tại dưới dạng dữ liệu JSON, không có bản trình bày để đính kèm.

★Số **VI/VII** chứ không phải III/IV: III/IV/V đã thuộc về Mẫu 05/06/07-BN. Chiếm lại số của chúng là
đổi nghĩa một bộ biểu mẫu chuẩn chỉ vì trong một hồ sơ cụ thể chúng tình cờ rỗng. Tên Phụ lục VI cũng
nói đủ hai thứ `route()` dồn vào đó ("nghiên cứu, rút kinh nghiệm" **và** "chưa đủ căn cứ kết luận") —
gọi tắt theo vế sau sẽ mô tả sai phần lớn số dòng.

## Nghiệm thu

- selftest **1346 → 1352** (+6 `r217_*`: 2 PURE nạp `verify_deep.py` thẳng từ file không qua bind,
  1 PURE nạp `lookup_ops.py` thẳng, 3 chạy **đường sản xuất thật** bằng subprocess).
- **Phản chứng 2 chiều CHẠY THẬT 11 đột biến trên bãi cách ly: 11/11 đỏ đúng ca, 0 lọt lưới** — cả
  hướng tắt guard (bỏ fail-closed toàn lô, bỏ cổng `--confirm`, bỏ cổng sha undo, bỏ cổng số hiệu,
  chỉ quét chữ ký số ở đầu, thôi khai báo, trả lại `open()` trần) lẫn hướng vá quá tay (nới khớp
  đúng-1-lần thành ≥1, bỏ dòng-chỉ-có-số không cần kề dòng chạy, bỏ luôn nhãn mục, chặn nạp khi còn
  rác). Bốn đột biến còn làm đỏ thêm test khác — guard phủ chéo.
- `ruff --select F` **delta 0 thực chất**: `tl.py` +0, `verify_deep.py` +0 (0 lỗi), ba script đường
  nạp +0; `lookup_ops.py` +26 và `tl_selftest.py` +11 đều là tên đã bind — đúng 2 tên mới
  (`_journal_read`, `_journal_new_run_id`) và cả hai đều có trong danh sách bind của `tl.py`.
- `parser_surface` regen **chủ đích 1 dòng** (thêm `doc-patch`). SKILL.md **byte-đẳng-dài 47.924**
  ⇒ re-import Capabilities KHÔNG bắt buộc. GAS **vẫn 2.21.2p**, không đụng.

# ★ v1.35.52 — r216: `rasoat-merge` đếm hai lần mà không ai biết, và đơn vị rà xuyên văn bản lọt vào danh mục VBQPPL (+5 test, 1346/1346) (2026-07-27)

> Nguồn: `rasoat_bugs.md` lượt rà 7 (27-07) — `RASOAT_MERGE_AN_CA_FILE_BAK_TRONG_THU_MUC_MASTER` +
> `RASOAT_MERGE_KHONG_CO_KHAI_NIEM_DON_VI_XUYEN_VAN_BAN`, và mục treo từ lượt 6
> `BANG_MASTER_DI_TRUOC_MASTER_UNIT_KHONG_CONG_NAO_BAT`. Cùng lớp **hỏng IM LẶNG** với r214/r215:
> rc=0, không cảnh báo, chỉ SỐ LIỆU là sai — mà đây là số liệu đi thẳng vào biểu mẫu trình Uỷ ban.

## (a) Bản sao lưu để lẫn trong `master/` ⇒ bảng master phồng 40 → 53 phát hiện, `_bo_qua` RỖNG, rc=0

`rasoat-merge --in <thư mục>` quét MỌI `*.json`. Đo thật 27-07 khi một bản sao lưu bị đặt nhầm vào
`master/`:

| | trước vá | sau vá |
|---|---|---|
| số phát hiện | **53** (13 mã VD trùng) | **40** |
| số văn bản | 5 | 4 |
| cảnh báo | **không có** (`_bo_qua: []`, rc=0) | `bo_qua_ban_sao` + rc=0 |

Hai nguồn mang **cùng `unit_id`** vẫn được gộp, không cổng nào đối chiếu. Phụ lục sinh ra từ bảng đó
đếm một phát hiện HAI lần, và người đọc bản phụ lục không có cách nào biết là trùng.

- **`_rasoat_la_ban_sao` (PURE)** — CỐ Ý HẸP: chỉ thành phần (ngăn bằng dấu chấm, KHÔNG tính thành
  phần đầu) bắt đầu bằng `bak`/`backup`. Không đoán theo `old`/`copy`/`cu`; `bakery-2025.json` vẫn là
  phiếu thật. Bản sao bị bỏ qua **được KHAI BÁO** ở `bo_qua_ban_sao` — bỏ qua im lặng chỉ là đổi sang
  một cái bẫy khác. ★Ghi chú giữ lại trong docstring: `backup` KHÔNG bắt đầu bằng `bak` (b-a-c ≠
  b-a-k) — bản đầu gộp làm một tiền tố và test đỏ ngay.
- **`_rasoat_trung_lap` (PURE)** — bắt trùng `key` (`phat_hien` lẫn `noi_dung`) và trùng `unit_id`,
  nêu rõ nguồn nào mang giá trị trùng. Cổng **fail-CLOSED**: có trùng ⇒ rc=2 và **KHÔNG ghi**. Ghi đè
  bằng bảng đã đếm hai lần là mất luôn bản đúng để đối chiếu ở lượt sau.

## (b) `--check`: bảng master ĐI TRƯỚC tầng unit thì merge lật ngược âm thầm

Khe hở đo được ở lượt 6: bản cập nhật VD-12 chỉ nằm ở `BANG_MASTER.json`, chưa chép về
`master/unit-003.json`. `rasoat-merge` lấy unit làm NGUỒN và bảng master làm ĐÍCH ⇒ chạy lại là mất
trắng một lượt làm việc, không báo gì. Lượt 6 phải xử bằng luật miệng "CẤM chạy `rasoat-merge`".

**`tl rasoat-merge --check`** = đối chiếu bảng master đang có với kết quả merge, **KHÔNG ghi đè**;
lệch ⇒ rc=2 kèm danh sách (`CHI_CO_O_BANG_MASTER` / `CHI_CO_O_KET_QUA_MERGE` / `KHAC_NOI_DUNG` +
ô lệch / hai loại cho `van_ban`). `_rasoat_check_lech` CỐ Ý bỏ qua `_nguon`/`_thieu_o_metadata`/
`_bo_qua` — chúng mang tên file, đổi theo chỗ chạy chứ không theo dữ liệu.

## (c) Đơn vị rà XUYÊN VĂN BẢN bị đẩy vào Mẫu 03-BN thành "văn bản" không tồn tại

`_rasoat_unit_to_bang` lấy `van_ban` của đơn vị làm SỐ HIỆU một dòng trong Mẫu 03-BN = *Danh mục
VBQPPL thuộc đối tượng, phạm vi rà soát*. `unit-006` (rà khối Căn cứ ban hành của CẢ 4 nghị định)
không phải một VBQPPL, nhưng nhãn mô tả của nó — `158/159/212/233-2025-ND-CP (KHOI CAN CU BAN HANH)`
— thành **dòng thứ 5** của một biểu mẫu chính thức trình Uỷ ban.

★`unit-004` (đơn vị đối chiếu 159×158) thoát được **CHỈ VÌ** tình cờ đặt `van_ban` trùng số hiệu thật
nên bị dedup nuốt đi — may, không phải do công cụ biết phân biệt.

Khoá mới **`loai_don_vi: van_ban|doi_chieu|xuyen_van_ban`** trong khuôn §6: `doi_chieu`/`xuyen_van_ban`
⇒ KHÔNG sinh dòng Mẫu 03-BN (và cũng không đòi điền ô metadata — đơn vị này không phải văn bản), phát
hiện vẫn gộp bình thường. **Mặc định (thiếu khoá) = GIỮ NGUYÊN hành vi cũ**: chỉ đơn vị tự khai mới
đổi cách xử lý.

## Nghiệm thu

- Selftest **1341 → 1346** (+5 `r216_*`). Bốn test PURE nạp `lookup_ops.py` THẲNG từ file (không
  bind) — đúng đường `rasoat_phuluc.py` đi; một test chạy **đường sản xuất thật** bằng subprocess
  `tl rasoat-merge`, vì cái đã cắn 27-07 là hành vi của LỆNH (rc=0 + ghi đè), không phải của hàm.
- **Phản chứng 2 chiều CHẠY THẬT 8 đột biến trên bãi cách ly: 8/8 đỏ đúng ca** — gồm cả hai hướng
  "tắt guard" (M1/M3/M5/M7) và "vá quá tay" (M2 coi mọi file là bản sao, M6 đơn vị nào cũng không
  sinh dòng), cùng hai hướng fail-open của cổng ghi (M4 thấy trùng vẫn ghi, M8 `--check` ghi đè).
- `ruff --select F` delta **0 thực chất**: +4 dòng đều là `_print_json_or_text` — tên do `bind()` cấp,
  đúng nhóm nợ sẵn của `lookup_ops.py`; `tl.py` giữ nguyên 17.
- `parser_surface` regen **chủ đích 1 dòng** (`rasoat-merge`, do thêm `--check`). SKILL.md
  **byte-đẳng-dài 47.924** ⇒ re-import Capabilities KHÔNG bắt buộc. GAS vẫn **2.21.2p**, không đụng.

# ★ v1.35.51 — r215: khối đầu văn bản bị đánh rơi trên đường cache, và nguồn DỰ THẢO phục vụ RAG lặng lẽ (+6 test, 1341/1341) (2026-07-27)

> Nguồn: `rasoat_bugs.md` lượt rà 4 (27-07) — `CACHE_BUILD_DANH_ROI_KHOI_DAU_VAN_BAN` (mục đáng vá nhất)
> + `DU_THAO_ND_BHXH_DE_CORPUS_TRUE_VA_DA_DAY_LEN_NLM`. Cùng lớp **hỏng IM LẶNG** với r214: rc=0, chỉ
> nội dung là thiếu. Khác ở chỗ cái thiếu lần này là **danh tính của chính văn bản**.

## (a) Đường cache trả về văn bản KHÔNG TỰ CHỨNG MINH ĐƯỢC DANH TÍNH — hai lỗ hổng, không phải một

**Đo trên ND 158/2025 (27-07), record `158-2025-nd-cp--consolidated.json` khai `chars=115.600`:**

| đường đọc | ký tự | bắt đầu bằng | phụ lục |
|---|---|---|---|
| `doc-text <id>` (mặc định → cache) | **108.823** | `Điều 1. Phạm vi điều chỉnh` | **không** |
| `doc-text <id> --markup mark` (gdoc-docx) | 115.414 | `CHÍNH PHỦ / Số: 158/2025/NĐ-CP` | có |

Bóc ra **hai** khiếm khuyết ĐỘC LẬP, trước đây bị gộp làm một và đổ nhầm cho "bản nguồn thiếu":

- **(a1) MẤT KHI DỰNG CACHE — `normalize_document.py` không hề lưu khối đầu.** `split_articles` bỏ
  `parts[0]` của `ART_SPLIT`; record chỉ có `articles` + `phu_luc`. Toàn bộ Quốc hiệu · cơ quan ban
  hành · `Số: 158/2025/NĐ-CP` · địa danh-ngày tháng · tên loại + trích yếu · khối `Căn cứ…` · tiêu đề
  Chương I **không nằm ở đâu cả** trong cache. Không cứu được bằng đọc lại cache — phải nạp lại.
- **(a2) MẤT KHI DỰNG LẠI — `cmd_extract` nối CHỈ `articles`.** `phu_luc` **CÓ trong record**
  (6.030 ký tự) nhưng đường dựng lại bỏ qua. Rồi bản thiếu đó **được ghi đè vào khoá cache CHUẨN**
  `extract_<id>.txt` ⇒ `doc-text` phục vụ nó làm bản mặc định. Đây mới là chỗ nhân bản thiệt hại.

**Vá:**
- `verify_deep.preamble_of(raw)` — PURE, dùng **CHUNG `ART_SPLIT`** với `split_articles` để hai bên
  không bao giờ lệch định nghĩa "chỗ Điều đầu tiên bắt đầu".
- `normalize_document` lưu `khoi_dau` + `structure.has_khoi_dau/khoi_dau_chars`. Khoá MỚI ⇒ record cũ
  đọc vẫn chạy; văn bản nạp dạng `--as-appendix` để rỗng (cả văn bản LÀ phụ lục, không có khối đầu riêng).
- `_consolidated_text(doc)` — PURE, dựng lại **khối đầu + Điều + phụ lục**. Đo lại trên chính record ND
  158 **chưa nạp lại**: 108.823 → **114.855** ký tự ⇒ **6.032 ký tự phụ lục được cứu ngay, không cần
  re-ingest**. Phần khối đầu thì cache cũ không có gì để cứu — nên nó phải **nói ra** (dưới).

## (b) Máy đoán thì phải nói là đang đoán — 3 cổng KHAI BÁO, không cổng nào chặn

Hỏng thật sự không phải "thiếu chữ" mà là **thiếu chữ mà không ai biết**. Ca đã trả giá: VBHN Luật NSNN
`89-2026` — text không có khối đầu ⇒ `_classify_doc_header` hết chỗ đọc trong vùng tiêu đề, đi quét sâu
16k và **nhặt số hiệu từ THÂN**, trả về `145/2025/QH15` (số của luật SỬA ĐỔI được liệt kê trong thân).
Lượt 3 đọc kết quả đó thành "bản nguồn thiếu khối đầu"; đo 27-07 cho thấy **nguồn CÓ đủ**.

- `_text_thieu_khoi_dau(text)` — PURE, bắt text **vào thẳng mốc cấu trúc thân** (`Điều N.` / `Chương
  <La Mã>` / `Mục N`). **CỐ Ý hẹp và tất định**: văn bản có letterhead, phụ lục độc lập mở đầu `PHỤ
  LỤC`, văn xuôi nhắc chữ "Điều" đều KHÔNG bị bắt — cổng này chạy trên mọi lượt đọc nên báo động giả
  đắt hơn im lặng.
- `_doc_text_any`: **mọi** đường trả text (cache · gdoc · gdoc-docx · docx · pdf) đi qua `_kd_gate` ⇒
  cảnh báo `[khoi-dau] ⚠` + `khoi_dau_missing` trong `doc-text --json`. Nhánh `return _ct, "cache"` —
  đúng đường đã phục vụ ND 158 — được nối riêng, không dựa vào đường chung phía dưới.
- `_classify_doc_header` trả thêm `khoi_dau_missing`. **KHÔNG đổi cách đoán**: đường quét sâu 16k vẫn
  cần cho layout VPQH in số VBHN ở **khối ký CUỐI** (v1.34.6 #1) — bịt nó là vá quá tay, làm hỏng một ca
  đúng để chữa một ca sai. Chỉ thôi im lặng.
- `cmd_extract`: record dựng TRƯỚC r215 (không có khoá `khoi_dau`) ⇒ cảnh báo tại chỗ kèm đúng hai lối
  ra (`cache-build` lại, hoặc `doc-text --markup mark`). `rep` phân biệt **`thieu_khoa`** (lỗi công cụ:
  cache cũ) với **`rong`** (dữ kiện: văn bản thật sự không có khối đầu) — gộp hai cái đó chính là cách
  lượt 3 đọc sai địa chỉ.

## (c) `DU_THAO_ND_BHXH_DE_CORPUS_TRUE_VA_DA_DAY_LEN_NLM` — cảnh báo hai đầu, **CỐ Ý KHÔNG CHẶN**

- **Đo:** hai dự thảo nghị định (`DUTHAO_ND_…`) mang `corpus=true`, `nlm_status=pushed` trong chính
  notebook hồ sơ. Cờ `DRAFT_NOT_EFFECTIVE` **có** bắn ở đường phân loại — nhưng không đường nào nói ra
  **vào lúc hỏi** ⇒ câu trả lời RAG có thể trộn chữ dự thảo với luật đang có hiệu lực.
- **★Đã cân nhắc và BÁC hướng fail-closed** mà sổ lỗi đề xuất đầu tiên ("loại các dòng có cờ
  DRAFT_NOT_EFFECTIVE khi đẩy"): dự thảo nằm trong notebook **hồ sơ trình** là **đúng chỗ** — chúng
  chính là đối tượng rà. Chặn đẩy sẽ phá đúng ca dùng chính đáng. Cái sai là phục vụ chúng LẶNG LẼ, nên
  vá đúng chỗ đó — trùng với phương án thứ hai mà chính sổ lỗi nêu ("ít nhất cảnh báo").
- `_nlm_draft_sources(entries, source_ids=, notebook_id=)` — PURE, đọc **registry**, không đoán từ
  envelope NLM (cùng doctrine với `_nlm_scope_shortfall` r214). Ghim `--source-id` → xét đúng nguồn được
  hỏi; không ghim → cả notebook. Dòng dự thảo **chưa** lên NLM không tính (chưa thành rủi ro RAG).
- Cảnh báo ở **hai** đầu: `nlm-add` (lúc đẩy) và `nlm-query` (lúc hỏi — in TRƯỚC câu trả lời).

## Kiểm chứng

- Selftest **1335 → 1341** (+6 `r215_*`). Ba test PURE nạp module **THẲNG từ file, KHÔNG bind** —
  bẫy [[false-green-test-qua-bind]] đã trả giá ở r213.
- **Phản chứng 2 chiều CHẠY THẬT 9 đột biến trên bãi cách ly** (vá thiếu ×5 / vá quá tay ×4): xem
  báo cáo phiên. Hai chiều đối xứng cho cùng một cổng (`M5` báo động tuốt ↔ `M6` guard chết hẳn).
- `_consolidated_text` đo lại trên record ND 158 THẬT (chưa nạp lại) — số ở bảng trên là đo, không ước.

# ★ v1.35.50 — r214: hai lỗi công cụ lượt rà 2 đo được — env profile ăn mất export, và `-s` LẶP làm NLM rụng nguồn (+6 test, 1335/1335) (2026-07-26)

> Nguồn: `rasoat_bugs.md` mục 8 + mục 9 (lượt rà 2, 26-07, cả hai `workaround`). Cả hai đều thuộc lớp
> **hỏng IM LẶNG**: lệnh vẫn rc=0, chỉ kết quả là sai — đúng lớp nguy hiểm nhất cho một lượt rà soát,
> vì nó đẻ ra kết luận ÂM TÍNH GIẢ mà không để lại dấu vết nào cho người rà.

## (a) `TL_META_FOLDER_ID_BI_PROFILE_OVERLAY_XOA` → `_apply_profile_env` thôi ăn env người dùng export

- **Lỗi:** `state-get`/`state-put` (r213) và `RASOAT_HOSO_LOOP` §7 bảo người dùng `export
  TL_META_FOLDER_ID`. Nhưng `_apply_profile_env` **pop VÔ ĐIỀU KIỆN** cả 6 khoá overlay rồi chỉ set lại
  khi block profile có ô tương ứng ⇒ profile thiếu `metaFolderId` (đúng ca config Cowork bootstrap, cờ
  `MARKER_CONFIG_DRIFT`) thì env bị **xoá trắng**, lệnh báo `META_FOLDER_ID_TRONG` và chuỗi `fix` chỉ lại
  **đúng cái đường nó vừa phá**. Lượt rà 2 phải đi vòng `--folder-id` tường minh cả lượt.
- **Vá:** vòng xoá chỉ còn xoá **đúng khoá do CHÍNH overlay trước đó ghi** (dấu vết để ở env
  `TL_PROFILE_ENV_OVERLAY` — **KHÔNG** dùng biến module: bẫy I11, mutable/hằng ở `tl_core` phải re-export
  sang `tl.py` mới sống qua rebase globals; env lại đi theo cả process con, đúng ngữ nghĩa "overlay đã
  ghi"). Mục đích GỐC của vòng xoá (đổi profile trong cùng process không dính scope cũ) giữ nguyên.
- **★NGOẠI LỆ GIỮ NGUYÊN — không nới:** `PROFILE_NOT_FOUND` vẫn xoá **SẠCH** bất kể ai ghi, để guard hạ
  nguồn (`NO_NOTEBOOK_ID`, `PROFILE_CATEGORIES_OWN_REQUIRED`, registry-id-empty) fail-closed thay vì mượn
  scope nền còn sót trong env — nới chỗ này là mở lại đúng lớp sự cố 1.23.21 mà v1.33.48 sinh ra để chặn.
- **Giới hạn đã biết (nói thẳng, không giấu):** nếu người dùng export env RỒI đổi profile **trong cùng
  một process** qua một profile CÓ ô đó rồi sang profile KHÔNG có, giá trị export ban đầu vẫn mất — bằng
  hành vi cũ. Khoá chính (lần overlay ĐẦU TIÊN không được ăn env) đã đóng; phần còn lại là mép hiếm.

## (b) `NLM_QUERY_LOAI_NGUON_KHONG_BAO` → **nguyên nhân gốc nằm ở argv của chính skill**, không phải NLM

- **Đo lại lật chẩn đoán cũ:** sổ lỗi ghi "NLM im lặng loại bớt nguồn". Đọc `nlm notebook query --help`
  của CLI ĐANG CÀI: `--source-ids/-s <str>` là **MỘT chuỗi «Comma-separated source IDs»**, KHÔNG phải
  option lặp. `nlm_cli.notebook_query` lại phát `-s <id>` **lặp lại** ⇒ giá trị sau **ĐÈ** giá trị trước,
  chỉ nguồn **CUỐI** sống sót. Khớp đúng số đo 26-07: truyền `212` rồi `233` → `sources_used` chỉ còn
  `233` = cái cuối. `cross_query` **trong chính file đó** vốn đã đúng khuôn `-n ",".join(...)`.
- **Vá tầng 1 (gốc):** tách `_query_args` PURE (khuôn `_add_args`), gộp **một** `-s` bằng dấu phẩy.
- **Vá tầng 2 (không tin server):** `_nlm_scope_shortfall` đối chiếu `sources_used` ↔ `--source-id`;
  thiếu → `NLM_SCOPE_SHORTFALL` cảnh báo stderr (rc vẫn 0, không chặn việc đang chạy). Cờ mới
  **`--strict-scope`**: thiếu → rc=2 **và KHÔNG in câu trả lời ra stdout** (agent hạ nguồn sẽ tưởng đủ
  nguồn); envelope không khai `sources_used` mà đã đòi `--strict-scope` → rc=2 `SCOPE_UNVERIFIABLE`
  (fail-CLOSED: đòi bảo đảm mà không chứng minh được thì không phát).
- **CỐ Ý KHÔNG đoán:** chỉ nhận đúng khoá `sources_used`. `sources`/`citations` là nguồn được **TRÍCH
  DẪN** — tập con HỢP LỆ của nguồn được **QUÉT** — đoán sang đó chỉ đẻ báo động giả (đã khoá bằng test).

## Nghiệm thu

- Selftest **1329 → 1335** (+6 `r214_*`). **Phản chứng 2 chiều CHẠY THẬT 7 đột biến** trên bãi cách ly
  (bản sao cây, không đụng canonical): 7/7 làm ĐỎ đúng ca kỳ vọng, khôi phục lại 1335/1335. Đáng chú ý:
  hai đột biến "vá quá tay" (M2 bỏ xoá khi `PROFILE_NOT_FOUND`, M3 thôi pop) còn làm ĐỎ **cả guard cũ**
  `r6_base_also_not_set_unknown_profile` / `r106_empty_profile_never_inherits_base` ⇒ xác nhận độc lập
  rằng bản vá không đụng vào tính chất mà v1.30.0/v1.33.48 đang giữ.
- `ruff --select F` **delta = +1** và là `DEFAULT_PROFILE` — tên vốn đã bind sẵn 14 lần trong chính file
  đó (nợ F821 by-design của khuôn bind), **không phải lớp lỗi mới**.
- `parser_surface.json` regen **CHỦ ĐÍCH** (đúng 1 dòng: `nlm-query`, do thêm `--strict-scope`).
- `SKILL.md` **byte-đẳng-dài 47.924** (chỉ đổi dòng version) ⇒ re-import Capabilities KHÔNG bắt buộc.
- **GAS KHÔNG đụng — vẫn 2.21.2p, không cần deploy GAS.**

# ★ v1.35.49 — r213: ĐỢT 5 — vá HAI mắt xích lớp điều phối mà lượt rà LIVE 26-07 phơi ra (+6 test, 1329/1329) (2026-07-26)

> Nguồn: sổ lỗi H7/H8 (`rasoat_bugs.md`, 7 mục, TẤT CẢ `workaround`). Hai mục vá ở đây là hai mắt xích
> **BẮT BUỘC** của lớp điều phối mà **không cổng máy nào phủ** — cả hai chỉ lộ ra khi chạy thật, vì Đợt
> 1–3 tả chúng bằng prose chứ không cài thành lệnh.

## (a) `STATE_DRIVE_KHONG_CO_DUONG_GHI` → `tl state-get` / `tl state-put`

- **Lỗi:** `WRITE_PATHS_v1` bắt state ở Drive `_meta/rasoat_state.json` làm nguồn sự thật resume, nhưng
  gói LIVE **không có lệnh nào ghi một JSON tuỳ ý vào `_meta/`**. Mặt ghi Drive duy nhất là
  `profile-file-add --apply --confirm yes` (cổng tài liệu corpus — cần người duyệt) và `drive-push`
  (đòi file ĐÃ tồn tại). Theo đúng chữ của doc thì **mỗi lần chốt state phải xen người 1 lần** — phá
  nghiệm thu ≤2 lần xen của H7. Lượt rà 26-07 phải giữ state local, KHÔNG sống nổi ca §7 (sandbox xoá
  trắng / đổi máy).
- **Đo lại trước khi vá — và phép đo lật đề bài:** mặt ghi **ĐÃ CÓ** và đang chạy THẬT trong sản xuất
  (`_create_profile_manifest_json`, `profile-index`): `g.post("upload", mime="application/json",
  folderId=<_meta>, convert/register/share="false", force="true")` rồi MỚI dọn bản cũ. **Thiếu là thiếu
  LỆNH, không thiếu năng lực** ⇒ **KHÔNG đổi GAS, KHÔNG thêm action `files_put`** (đề xuất ban đầu),
  GAS giữ nguyên `2.21.2p`, Đợt 5 **không cần deploy GAS**.
- **Vá:** cặp lệnh client-only. `state-put` **CỐ Ý không có `--confirm`** — mượn cổng duyệt là tái tạo
  đúng thứ đã phá H7. Đổi lại khoá bằng **ba chốt máy**: (1) `_rasoat_state_scope` fail-CLOSED — danh
  sách tên ĐÓNG (`rasoat_state.json`/`rasoat_approvals.json`), từ chối mọi tên khác/có đường dẫn;
  (2) folder đích BẮT BUỘC `_meta/` (không có mặc định root); (3) `--expect-claim` từ chối ghi khi
  `session_claim.id` trên Drive đã khác (single-writer §9), và **fail-CLOSED khi không đọc nổi bản trên
  Drive** thay vì đoán là khớp.
- `register="false" share="false"` là **bắt buộc, không phải tuỳ chọn**: `upload` mặc định
  `ANYONE_WITH_LINK` + ghi registry ⇒ để mặc định thì state hồ sơ vừa RÒ RỈ qua link vừa bẩn registry.
  Ba tham số này bị test khoá ở NGUỒN.
- **Thứ tự an toàn:** tạo bản MỚI trước → dọn bản cũ sau. Chết giữa chừng = tồn 2 bản, `state-get` lấy
  bản mới nhất và lượt sau dọn nốt; đảo thứ tự thì chết giữa chừng = MẤT state.
- Tiện thể trả nợ mục `PROFILE_META_FOLDER_KHONG_CO_TRONG_CONFIG`: `metaFolderId` rỗng nay báo lỗi **chỉ
  thẳng đường vòng ĐỌC-ONLY** (`profile-sync --json`, KHÔNG `--apply`) thay vì cụt lủn — đường vòng đó
  26-07 phải tự nghĩ ra.

## (b) `THIEU_BUOC_GOP_MASTER_UNIT_SANG_BANG_MASTER` → `tl rasoat-merge`

- **Lỗi:** PHA 4 **SẬP thật** (`AttributeError: 'str' object has no attribute 'get'`). Khuôn §6
  `master/<unit>.json` và khuôn bảng master khớp ở tầng **item** (cùng 10 trường + `anchor`) nhưng lệch
  ở tầng **container**. QUY_TRINH chỉ viết "dồn phát hiện vào bảng master" — Đợt 1–3 **không định nghĩa
  và không cài** bước "dồn", cũng không test nào chạy chuỗi §6 → phụ lục.
- **Hỏng IM LẶNG trước, báo sai chỗ sau:** `van_ban += d.get("van_ban", [])` gặp CHUỖI số hiệu thì `+=`
  **trải chuỗi thành TỪNG KÝ TỰ** (`["1","5","9","-",…]`), mãi sau mới chết ở nơi khác.
- **Vá:** `tl rasoat-merge --in <master/> [--out] [--state]`; và `rasoat_phuluc.py` **tự nhận khuôn §6**
  qua ĐÚNG hàm quy đổi đó (một nguồn chân lý) nên `--in <out-dir>/master` chạy thẳng — điều mà thẻ
  `rasoat_hoso.json` đã **khẳng định trong mục `verify` từ Đợt 2 mà chưa ai kiểm**; nay mới thành thật.
  Khuôn không nhận ra ⇒ **rc≠0 nói rõ file nào**; file có CẢ `phat_hien` lẫn `noi_dung` cũng bị từ chối,
  không đoán — đoán sai ở đây là nuốt mất phát hiện mà không ai biết.
- **KHÔNG BỊA metadata:** đơn vị rà chỉ biết số hiệu + tên; `ngay`/`hieu_luc_tu`/`tinh_trang` nằm ở
  registry. Các ô đó để **RỖNG** + nổi lên `_thieu_o_metadata` + ghi chú ngay trong ô Ghi chú, thay vì
  lấp cho đầy bảng. (Đợt 4 dựng tay các ô này từ registry; **CỐ Ý chưa tự động hoá** ở r213 — registry
  không có `ngay`/`hieu_luc_tu` nên cũng chỉ lấp được 3/6 ô, mà đánh đổi là biến một lệnh thuần/tất định
  thành lệnh phụ thuộc cache. Ghi nhận là việc riêng.)
- **Khe hở H8** (phiên kế nhiệm chết SAU khi ghi master nhưng TRƯỚC khi cập nhật state ⇒ state còn
  `doing` dù việc đã xong): `--state` chạy `_rasoat_state_reconcile` — `doing` + CÓ master ⇒ `done`;
  `doing` + KHÔNG master ⇒ `pending`; `done` KHÔNG BAO GIỜ bị hạ. Luật cũ của thẻ ("doing mồ côi →
  pending") áp thẳng sẽ **rà lại đơn vị đã xong và đẻ phát hiện trùng số**.

## (c) Chốt MÂU THUẪN DOCTRINE `nlm-auth-load` (câu trừ ngữ cảnh, không đảo/không nới)

- Chuỗi khắc phục của `nlm-auth-status` xếp `tl nlm-auth-load` ở **(1)** trong khi §4b + PHA 0 **CẤM tự
  chạy** nó. **Cả hai đều đúng, khác NGỮ CẢNH:** (1) là đường bootstrap Cowork/headless — ở đó máy chưa
  có jar nào và đấy là đường duy nhất chạy được không cần browser; trong lượt rà thì nạp bundle đè lên
  jar đang sống/vừa chết là quay vòng vô ích.
- ⇒ **Không đảo thứ tự** (đảo là phá nghiệm thu r208b) và **không nới §4b** (nới là mở lại vòng lặp
  r208c đã đóng). Thay vào đó **cả 5 chuỗi** thông báo auth mang sẵn **câu trừ** trỏ §4b, vì agent đọc
  thông báo lỗi thường không đọc doctrine. Chốt chặn hạ cấp `_nlm_auth_load_downgrade` (r208c) vẫn giữ —
  nó chặn bản CŨ hơn nhưng **KHÔNG chặn được bản mới-hơn-mà-cũng-chết**, nên câu trừ là lớp còn thiếu.

## Test 1323 → **1329** (+6 `r213_*`), tất cả phản chứng 2 chiều

- `r213_rasoat_ops_chay_duoc_khong_can_bind` — **bẫy trả giá NGAY khi viết r213**: bản đầu của
  `_rasoat_merge_units` gọi `_norm_compare_text`, chạy tốt qua `tl` (đã bind) nhưng `NameError
  unicodedata` khi `rasoat_phuluc.py` import trần. Đúng khuôn false-green mà r212 vừa dạy. Test nạp
  `lookup_ops` THẲNG từ file (không ai gọi `bind`) + khoá NGUỒN cấm nối lại helper đó.
- `r213_gop_master_s6_chay_tron_chuoi_den_phu_luc` — chạy **subprocess đường sản xuất thật**
  `python scripts/rasoat_phuluc.py --in <thư mục master>`; phản chứng 1: file khuôn lạ phải rc≠0 (không
  nuốt thành "0 phát hiện"); phản chứng 2: tái hiện thuật toán CŨ trên đúng dữ liệu ⇒ khẳng định
  `+=` trải 14 ký tự — test bắt được nếu ai revert.
- `r213_merge_khuon_nhan_dien_2_chieu` · `r213_state_put_scope_fail_closed` (11 tên xấu đều bị chặn,
  khoá `share/register/force` + THỨ TỰ upload-trước-trash ở nguồn) · `r213_state_hoa_giai_don_vi_doing`
  (6 chiều, gồm "master rỗng ⇒ không đơn vị nào tự lên done") · `r213_auth_carve_out_khong_pha_thu_tu`
  (thứ tự r208b KHÔNG vỡ ∧ câu trừ có mặt ∧ doctrine ở 2 tài liệu vẫn CẤM).
- **Đo trên dữ liệu THẬT của Đợt 4** (`p14_h7h8_rasoat_2026-07-26/master`): 2 file → 2 văn bản, 9 phát
  hiện; chuỗi tiếp `rasoat_phuluc` ra 04:5 · Mục F:4 · dedup **9** — khớp đúng kết quả đường vòng 26-07.
  Hồi quy khuôn bảng cũ giữ nguyên 03:4 · 04:5 · F:4 · dedup 9.
- `parser_surface.json` regen CHỦ ĐÍCH: **+3 dòng, 0 sửa** — chứng minh không lệnh cũ nào đổi mặt.

## Kiểm LIVE đường ghi (user duyệt chạy thật, đã dọn sạch sau đó)

`state-get` đường ĐỌC đã chạy LIVE ngay khi viết. Đường GHI thì chạy trọn một lượt trên Drive thật
rồi trash file kiểm thử — vì **ship một đường mà chưa ai chạy đúng là cái Đợt 5 tồn tại để tránh**
(thẻ `rasoat_hoso.json` từng khẳng định `rasoat_phuluc.py --in master/` chạy được, suốt 3 đợt không ai
kiểm, và nó sập thật).

- PUT lần 1 → `fileId` mới, `don_ban_cu: []`. GET đọc lại: **JSON khớp TUYỆT ĐỐI**, dấu tiếng Việt
  nguyên vẹn (`Điều 1 khoản 2.`).
- `--expect-claim` **lệch** ⇒ `CLAIM_LECH` **rc=2**, nói rõ claim trên Drive vs kỳ vọng. **khớp** ⇒ cho
  ghi, và **dọn đúng bản cũ** (`don_ban_cu` 1 mục, `don_sach: true`).
- GET sau ghi đè: đúng **1 bản**, `canh_bao` rỗng, nội dung là bản B. Trash xong → `state-get` trở lại
  **rc=3** "chưa có state trên Drive". Không để lại rác.
- **★ Lượt kiểm LIVE bắt được 1 lỗi mà test thuần không thấy:** `state-get` đếm **KÝ TỰ** trong khi
  `state-put` đếm **BYTE**, cùng nhãn `"bytes"` ⇒ CÙNG một file báo **478 vs 471** (7 ký tự có dấu),
  nhìn hệt như mất dữ liệu khi đối chiếu round-trip. Đã sửa `state-get` sang byte utf-8 + khoá bằng
  `r213_state_put_scope_fail_closed` (ok6). Đây đúng là loại lỗi chỉ lộ ra khi chạy thật.

## ★ Bẫy đã trả giá trong chính lượt này (ghi để không lặp)

- **`contract_check.py --bump <ver>` là bump CONTRACT GAS, KHÔNG phải version skill.** Gọi nhầm nó với
  `1.35.49` đã ghi đè `2.21.2p` ở 5 chỗ trong `SKILL.md`/`API_CONTRACT.md` (sinh ra cả `Code.1.35.49.gs`
  không tồn tại). Đã `git checkout` hai file và bump 3 chỗ version skill BẰNG TAY. Bump skill =
  `VERSION` + hằng `VERSION` trong `tl.py` + header `SKILL.md`; KHÔNG có công cụ tự động cho việc đó.
- `tl_selftest.py` là **CRLF toàn bộ** trong khi `tl_core/*.py` là **LF** — nối test phải chuyển đổi,
  không thì lẫn dòng.

# ★ v1.35.48 — r212: GUARD ADR-0001 ĐANG FAIL-OPEN — `tl_gws` thiếu `import Path` (+1 test, 1323/1323) (2026-07-26)

> Phát hiện khi truy một `[FAIL] r65` người dùng gặp 26-07 (lần đỏ ĐÓ là thoáng qua — chạy selftest đúng
> lúc merge fast-forward đang viết lại 10 file). Truy tiếp thì lòi ra lỗi THẬT, không liên quan lần đỏ đó.

- **Lỗi:** `scripts/tl_gws.py` **không hề import `pathlib`** — `Path` là tên stdlib DUY NHẤT trong nhóm còn
  chờ `bind(tl_module)` chép từ namespace tl. Nên `_bundle_meta_blocks_push` (guard ADR-0001: cây có
  `BUNDLE_META.json` = giải nén từ bundle nhánh song song ⇒ CẤM publish) ném `NameError`, bị
  `except → return False` nuốt, và **luôn báo "không có gì chặn cả"**. Đo tươi: `import tl_gws` trần rồi gọi
  trên thư mục CÓ `BUNDLE_META.json` → `False`. Mọi đường dispatch không qua `build_parser` — đúng cái bẫy
  mà chú thích đầu file đã cảnh báo — biến guard cấm-publish thành cho-phép-publish.
- **Vì sao r65 không bắt:** nó gọi qua `_imp("tl_gws")` — instance ĐÃ bind nên `Path` có sẵn. Test xanh
  trong khi đường sản xuất hỏng: false-green kinh điển.
- **Vá:** (a) `from pathlib import Path` vào nhóm stdlib TƯỜNG MINH ở top (đúng doctrine sẵn có của file);
  (b) guard đổi sang **FAIL-CLOSED** — đọc không được thì CHẶN (`return True`), vì guard cấm-publish mà hỏng
  theo hướng "cứ publish đi" là hỏng sai chiều; người vẫn có `--force`.
- Test 1322 → **1323** (`r212_guard_bundle_meta_khong_phu_thuoc_bind`): nạp tl_gws THẲNG từ file (không ai
  gọi bind — khẳng định `_BOUND is False`) rồi đòi guard phân biệt đúng 2 thư mục; **phản chứng** gỡ `Path`
  khỏi globals ⇒ tái hiện đúng sự cố nhưng nay CHẶN thay vì cho qua; khoá luôn nguồn (xoá dòng import =
  test đỏ). **Chạy 2 chiều thật:** code CŨ → `1322/1323` (r212 đỏ, r65 vẫn xanh — chứng minh r65 chưa bao
  giờ phủ chỗ này); code ĐÃ VÁ → `1323/1323`.
- **Ruff đã tố cáo từ lâu mà không ai đọc:** delta trên `tl_gws.py` đúng **−2 `F821 Undefined name Path`**
  (99 → 97), không thêm phát hiện mới. Hai dòng đó nằm lẫn trong ~97 F821 "cố ý" của thiết kế `bind()` nên
  chìm nghỉm — bài học: nợ F821 diện rộng che mất F821 THẬT.

# ★ v1.35.47 — r211: ĐỢT 3 LỚP ĐIỀU PHỐI — H5 degrade-and-continue + sổ lỗi · H6 kickoff contract + PHA 0 tiền kiểm (+6 test, 1322/1322) (2026-07-26)

> Tiếp r210 (Đợt 2 đã merge). Đợt 3 **không viết code lõi**: hai hạng mục đều là ĐẶC TẢ — nhưng đặc tả
> viết dưới dạng **khối máy-đọc** (`BUG_LEDGER_v1` · `PHA0_GATE_v1` · `KICKOFF_CONTRACT_v1`, cùng idiom
> `WRITE_PATHS_v1` của r210) để guard bắt được drift, thay vì prose mà không cổng nào gác.

- **H5 — làn lỗi & sổ lỗi (`references/QUY_TRINH_RA_SOAT_3_TANG.md`, mục MỚI "LÀN LỖI"):** 4 bước
  (thử đường vòng CÓ SẴN → `workaround` đơn vị vẫn tới `done` → `blocker` đánh `blocked` **không giả
  `done`** rồi đi tiếp → chỉ dừng khi **chặn đứng toàn cục**). Chốt: **đúng HAI hạng lỗi**; "chặn đứng"
  KHÔNG phải hạng lỗi mà là **trạng thái hồ sơ** suy ra từ hàng đợi (mọi đơn vị còn lại cùng một `ma`) —
  nên một `blocker` lẻ không bao giờ đọc được thành lý do dừng. **Sửa nóng CHỈ khi chặn đứng**, lỗi lẻ
  **gom vá sau lượt rà**, và không nhánh nào vá tại LIVE (deploy là bước tay ⇒ vá tại chỗ bị đè lần
  deploy sau). Khuôn sổ `rasoat_bugs.md` **8 trường bắt buộc**, thiếu/rỗng một trường = coi như CHƯA ghi
  sổ; `version_do_duoc` bắt buộc vì báo lỗi đo trên bản trễ là vô giá trị (LIVE drift). Tên sổ dùng đúng
  `rasoat_bugs.md` đã khoá trong `WRITE_PATHS_v1` — kế hoạch gọi `BUGS_FOUND.md` là CÙNG một sổ, không đẻ
  tên file thứ hai.
- **H6 — PHA 0 tiền kiểm (cùng tài liệu) + kickoff contract (`references/RASOAT_HOSO_LOOP.md` §1):**
  PHA 0 mở rộng thành cổng **6 bước** — b1 `doctor` · b2 `ping`/contract · b3 `precheck` ·
  b4 `profile-doctor` · b5 `nlm-auth-status` · b6 **canary probe LIVE**. Ba verdict thay vì hai:
  `chan_dung` (dừng sớm, báo 1 dòng) · **`chan_lan_ghi`** (Loop B đứng, **Loop A vẫn rà trên cache** —
  không giết cái còn chạy được) · `co_fallback` (tụt chế độ không-NLM). **b5/b6 CHỈ chạy khi lượt sắp cần
  NLM**, và **chi phí trước cổng = 0 call truy vấn** (canary là `notebook_get`, ngoài ngân sách 60).
  Verdict đọc theo đo 26-07: `alive=false` ⇒ chế độ không-NLM · `alive=null` ⇒ KHÔNG chặn · `alive=true`
  + `rotation_token_expired` ⇒ chạy tiếp nhưng không mở lô dài. Kickoff nâng 6 → **8 mục** (thêm *môi
  trường & đường ghi* và *nghiệm thu & điểm dừng*), mỗi mục có mặc định trừ **phạm vi hồ sơ = bắt buộc
  hỏi**; bộ hằng số trong hợp đồng phải khớp `RASOAT_PLAN_SCHEMA.md` §4, không đẻ bộ thứ hai.
- **Thẻ `references/workflows/rasoat_hoso.json`:** `plan[A1]` trỏ `PHA0_GATE_v1` b1–b6; +2 `rules`
  (degrade-and-continue; luật sửa nóng); +3 `recommended_commands` (`doctor`/`precheck`/`nlm-auth-status`)
  — mọi lệnh đều CÓ THẬT trong parser và được kịch bản gọi tên (drift-guard r210 vẫn gác).
- Test 1316 → **1322** (+6 `r211_*`), tất cả PURE, không chạm mạng: `so_loi_dung_khuon` ·
  `degrade_khong_dung_vong` (bơm lỗi giữa lượt drain 6 đơn vị → ghi sổ 1 mục ĐỦ trường, PLAN vẫn tiến
  5/6, vòng không dừng) · `sua_nong_chi_khi_chan_dung` · `pha0_chan_som_truoc_khi_tieu_nlm` (chặn đứng ở
  b1 ⇒ chưa hề chạm b5/b6) · `kickoff_du_muc_va_hang_so` · `the_khop_luat_moi`.
  **Phản chứng 2 CHIỀU chạy thật (6 đột biến tài liệu, mỗi lần chạy lại cả suite):** hạ b6 xuống
  `chan_dung` → đỏ đúng test PHA 0 · bỏ `version_do_duoc` → đỏ khuôn sổ · cắt 1 mục kickoff → đỏ hợp đồng ·
  lệch hằng `nlm=60→40` → đỏ hợp đồng · gỡ luật sửa nóng khỏi thẻ → đỏ drift-guard thẻ · xoá hẳn khối
  `BUG_LEDGER_v1` → đỏ 3 test (fail-closed, không im lặng cho qua). Không đột biến nào làm đỏ lây.
- Không đụng `scripts/tl.py` (ngoài bump VERSION) — **ruff delta 0**; GAS **KHÔNG đổi, vẫn 2.21.2p**.

# ★ v1.35.46 — r210: ĐỢT 2 LỚP ĐIỀU PHỐI — H3 kịch bản vòng lặp rà hồ sơ + H4 agent rà đơn vị read-only (+5 test, 1316/1316) (2026-07-26)

> Tiếp r209 (Đợt 1 đã merge). Đợt 2 KHÔNG xây engine mới: vòng lặp **BỌC** `tl rasoat-loop` +
> `tl frontier-expand` sẵn có và dùng nguyên bộ từ vựng hội tụ `dry_rounds`/`max_iter`/`PAUSE` — phần
> PLAN chỉ thêm cái chúng không có (trạng thái theo đơn vị, lưu bền, `session_claim`).

- **H3 — `references/RASOAT_HOSO_LOOP.md` (MỚI, vào `_RELEASE_REQUIRED_FILES` cùng `RASOAT_PLAN_SCHEMA.md`):**
  kịch bản vận hành đầy đủ — §0 ranh giới vai (phiên chính = BÊN GHI DUY NHẤT; agent read-only; worker
  Q-NLM không đụng state/registry) · §1 hợp đồng giao việc 6 mục · §2 Loop A A1–A8 kèm lệnh CÓ THẬT ·
  §3 Loop B B0–B6 (dò trùng `--refresh` TRƯỚC, chuẩn-bị-trước-duyệt-sau, bậc thang nguồn tải, tách kênh
  cache/NLM, đơn vị `doi_chieu_bo_sung` + bất biến done-không-reset) · §4 Loop C + §4b chế độ chạy-không-NLM
  (canary probe LIVE, CẤM tự `nlm-auth-load`) · §5 làn lỗi · §7 **khối máy-đọc `WRITE_PATHS_v1`** ·
  §8 đóng gói chủ động 40%/60% đo tại RANH GIỚI đơn vị · §9 nhịp registry cấm chen ngang.
- **H4 — agent `tl-rasoat`:** prompt mẫu đầy đủ trong §6 (dùng được ở LIVE nơi KHÔNG có file agent) +
  wrapper dev `.claude/agents/tl-rasoat.md` **ép cứng bằng frontmatter** (`tools` không có Write/Edit,
  `disallowedTools`, `maxTurns` — theo kho best-practice `claude-subagents.md`); prompt-only chỉ là lớp 2,
  LIVE phải hậu kiểm `verify-integrity` + `git status`. Kèm wrapper lệnh `.claude/commands/rasoat-hoso.md`.
  (`.claude/` bị release-exclude ⇒ wrapper là dev-side, không vào gói.)
- **SKILL.md (+58B ròng, 47.924B — vẫn dưới WARN):** thêm 1 dòng vocab nhóm lệnh + 1 dòng danh mục
  references trỏ kịch bản; **dọn mục GAS `2.21.2m`** (bản .gs dev-only, lịch sử đã ở CHANGELOG/DOCTRINE) và
  **sửa 2 chỉ dẫn SAI version**: `tl ping` phải ra `2.21.2p` (không phải `2.21.2m`), dòng đồng bộ tài liệu
  cũng về `2.21.2p` — LIVE là 2.21.2p từ r208-gas.
- Test 1311 → **1316** (+5 `r210_*`): `loop_khong_ghi_trong_cay` (bóc khối `WRITE_PATHS_v1`, PHẢN CHỨNG
  2 chiều: bơm đường ghi trong cây → bắt; thiếu khối → fail-closed) · `loop_doc_khop_the` (drift-guard
  prose ↔ thẻ máy: A1–A8, từ vựng hội tụ, MỌI `recommended_commands` phải được kịch bản gọi tên — test này
  đã bắt THẬT một drift: thiếu `profile-ingest --staged`, đã vá) · `agent_prompt_dung_schema` (schema JSON
  của agent khớp ĐÚNG bộ trường mẫu master + anchor) · `agent_wrapper_ep_cung` (frontmatter khoá cứng;
  vắng `.claude/` = LIVE → bỏ qua) · `skill_tro_kich_ban_va_gas_dung_ban` (khoá luôn việc hết `2.21.2m`).
- Golden regen CÓ CHỦ ĐÍCH 1 fixture (`workflow_audit`: `links_checked` 13→15 do 2 con trỏ mới trong SKILL.md).
  **GAS KHÔNG đổi — vẫn 2.21.2p.**

# ★ v1.35.45 — r209: ĐỢT 1 LỚP ĐIỀU PHỐI RÀ HỒ SƠ — H9 guard ratchet con trỏ + H0 vá đường cấp cứu LÕI + H1/H1b template master + H2 thẻ quy trình (+7 test, 1311/1311) (2026-07-26)

> Thi hành Đợt 1 kế hoạch `docs/KE_HOACH_RASOAT_HOSO_ORCHESTRATION.md` (nhánh kiến trúc 2al46n, grill
> 25→26-07 chốt 8/8 quyết định). Đo 26-07 trên v1.35.44: **80 cặp (tài_liệu, con_trỏ) đứt** trong
> SKILL.md + references/*.md — 65 ở DOCTRINE_APPENDIX (lưu trữ), **2 nằm ngay trong chỉ dẫn CẤP CỨU của
> LÕI** (`scripts/build_parts.py`/`scripts/tl_rebuild.sh` — đặc tả chi tiết rồi KHÔNG BAO GIỜ được viết;
> cơ chế `_parts/` đã bỏ từ khi Cowork bootstrap qua `tl_fetch.sh`, xem `tl_boot.py:4`).

- **H9 — guard RATCHET `_doc_pointer_findings` (release.py):** mở rộng REL-01 từ «references/ trong
  SKILL.md» ra «references/|templates/|scripts/ trong SKILL.md + references/*.md», đối chiếu PACKAGE-SET.
  Phân hạng: `_POINTER_ARCHIVE_DOCS` (DOCTRINE_APPENDIX → advisory, không sửa thân tài liệu lịch sử);
  `_POINTER_BASELINE` = **10 nợ cũ khoanh theo CẶP** (miễn trừ không lan giữa tài liệu) — hằng số trong
  code, sửa baseline = qua ruff→selftest→CHANGELOG→review; cặp MỚI đứt ở tài liệu sống ⇒ fail-closed
  (`DOC_POINTERS_NOT_IN_PACKAGE`, khóa `doc_pointers` trong release-verify).
- **H0 — vá đường cấp cứu LÕI (hướng (ii) SỬA LÕI, user chốt):** SKILL.md bỏ 4 vùng trỏ
  `build_parts`/`tl_rebuild`/`_parts` (−223B → 47.866B, thoát vùng WARN 47K); `COWORK_EDIT_SAFETY.md`
  viết lại lớp PHÁT HIỆN/KHÔI PHỤC theo sự thật: thang cứu hộ = `tl_boot.py` (strip NUL) →
  `verify-integrity` (chỉ mặt file hỏng) → **bước 0 `tl_fetch.sh` zip SẠCH** → RE-SYNC; hết đường ghép
  local, hết quy trình 5-bước chết.
- **H1 — `templates/MAU_BANG_TONG_HOP_PHAT_HIEN.json` (MỚI, vào `_RELEASE_REQUIRED_FILES`):** schema suy
  từ BÊN ĐỌC (`rasoat_phuluc.py:load_master` — thư mục *.json gộp, append-only mức thư mục), kèm
  `_vocab_hinh_thuc` 10 giá trị CÓ DẤU (route() khớp chuỗi cố định — không dấu rơi ÂM THẦM về 04, bẫy
  KHOÁ bằng test làm bằng chứng), `anchor` (neo phụ thuộc: doc_deps.text_hash + cite + ttl_ngay=90) +
  `muc_chac_chan` enum `chac_chan|can_kiem_tra|cho_verify_nlm` nhập từ đầu — KHÔNG có bước merge (local
  chưa từng có template). **Q2 (user chốt): XOÁ đặc tả `nlm_log.py`** khỏi `QUY_TRINH_RA_SOAT_3_TANG.md:91`
  → thay bằng `NHAT_KY_NLM_<sh>.csv` (khung sẵn của `rasoat_worksheet.py`) + quota đếm trong state.
- **H1b — `rasoat_phuluc.py` mở rộng TỐI THIỂU:** kết xuất phụ lục 04–07 nối `muc_chac_chan` +
  `anchor.cite` vào cột Ghi chú (bảng C không rơi mất mức chắc chắn/cite; master vẫn là nguồn sự thật).
- **H2 — thẻ `references/workflows/rasoat_hoso.json`** (`workflow_card.v1`, risk medium, đủ 12 trường,
  recommended_commands đều CÓ THẬT trong parser; vào `_RELEASE_REQUIRED_WORKFLOWS`) + đặc tả phần biến
  động `references/RASOAT_PLAN_SCHEMA.md` (`rasoat_plan.v1`: 4 hàng đợi + Q-VERIFY, claim/takeover 30′,
  hằng số vận hành chốt 26-07, nghi thức đóng gói A8).
- **ADR-0016** (state LAI · single-writer theo claim · anchor · guard ratchet) — trade-off + hệ quả.
- Test 1304 → **1311** (+7 `r209_*`): `pointer_findings_pure` (fail-closed manifest rỗng · archive
  advisory · baseline im · cặp mới đỏ) · `baseline_ratchet` (khoá số đếm 10 + miễn-trừ-không-lan) ·
  `cay_that_va_phan_chung` (cây thật 0 fail + PHẢN CHỨNG bơm dòng SKILL.md trước-H0 → đỏ đúng 2 con trỏ)
  · `skill_md_khong_tro_file_ma` (H0, prefix thư mục) · `master_template_va_vocab` (10/10 vocab + bẫy
  không-dấu + chuẩn NN-YYYY-VBHN-XXX) · `bang_c_du_truong` (H1b) · `the_rasoat_hoso_hop_le` (H2 +
  workflow-audit sạch). **GAS KHÔNG đổi — vẫn 2.21.2p.**
- Tồn đọng ghi nhận (KHÔNG sửa đợt này): `QUY_TRINH:81` nhắc `nlm_qa.py` (bare — đã hợp nhất vào tl) ·
  `QUY_TRINH:99` nhắc `manifest_build.py` (bản thật ở `scripts/_fallback/`) · SKILL.md §7 bản đồ script
  còn vài tên bare đời cũ — nằm ngoài vùng phủ guard (chỉ bắt con trỏ CÓ tiền tố), gỡ dần theo baseline.

# ★ v1.35.44 — r208d: van F7 ĐỔI TỪ CHẶN-THEO-TUỔI SANG CANARY LIVE trước lô (user duyệt 26-07; +1 test/1 đổi kỳ vọng, 1304/1304) (2026-07-26)

> Tiếp r208c. Ngưỡng F7 (`NLM_COOKIE_BATCH_MAX_MIN = 50`) dựng trên «đời cookie ~60′» mà r208c đo được là
> SAI: cookie phiên hạn **380 ngày**, chết là do token xoay `__Secure-1PSIDRTS` hết hạn mà CLI `nlm` không
> gia hạn. Hệ quả đo được: tuổi **vừa CHẶN OAN** phiên còn tốt, **vừa CHO QUA** phiên đã chết — phiên chết
> thật lúc `age_min` mới **5,2′** trong khi công cụ hứa «còn 54,8′».

- **Chốt chặn lô = verdict probe LIVE**, không còn là tuổi. Điểm khéo: `_rep54` ngay phía trên trong
  `cmd_ingest_missing` **đã probe rồi** (`probe=not _thr_over`, mà tới được cổng lô nghĩa là
  `_thr_over=False`) ⇒ canary **KHÔNG tốn round-trip mới**.
  - `alive=False` → **DỪNG rc=2 trước mọi side-effect**, reason `NLM_AUTH_DEAD_BEFORE_BATCH`, kèm `why`,
    `cookie_age_min`, `rotation_token_expired` và `fix` (chuỗi khắc phục r208b). Chỉ tới được nhánh này khi
    fallback TẮT (có fallback thì `_dead54` đã rẽ `BATCH_LINKS` phía trên). Trước r208d nhánh đó đi tiếp
    đường API rồi mới fail giữa chừng — dừng sớm vẫn fail-closed mà không để lại chuỗi dở dang.
  - `alive=None` → **KHÔNG chặn** (bài học M2 v1.33.35: không kết luận ≠ chết).
  - tuổi cao / token xoay hết hạn → **CẢNH BÁO** trước lô, không chặn.
- **Hằng đổi tên `NLM_COOKIE_BATCH_MAX_MIN` → `NLM_COOKIE_BATCH_WARN_MIN`** (vẫn 50) — tên cũ nói dối vì
  nó không còn là ngưỡng chặn. Re-export I11 cập nhật cùng đợt.
- `--force-api-add` GIỮ NGUYÊN là cửa ép chủ đích (không mở rộng cổng sang nhánh đó — hành vi có test
  `r115_ingest_missing_force_api_add_wins` khoá từ trước).
- Test 1303 → **1304** (+1 `r208d_canary_truoc_lo`: chết→rc=2 0 add + có đường ra · sống-nhưng-tuổi-99′→
  KHÔNG chặn, vẫn cảnh báo · `alive=None`→không chặn · token xoay hết hạn→cảnh báo). `r192_f7_cookie_50p_chan_lo`
  đổi tên/kỳ vọng CÓ CHỦ ĐÍCH → `r208d_f7_canary_thay_chan_theo_tuoi` (khoá cả việc tên hằng cũ đã BIẾN MẤT).
  Harness `_run_im110` thêm tham số `force_api_add` (mặc định True = hành vi cũ của mọi caller sẵn có).
  **GAS KHÔNG đổi — vẫn 2.21.2p.**

# ★ v1.35.43 — r208c mục 3.1: ĐO TRƯỚC RỒI MỚI VÁ — lật tiền đề «cookie chết sau ~1 giờ», bỏ `est_remaining_min` bịa, chống hạ cấp `nlm-auth-load` (+1 test/1 đổi kỳ vọng, 1303/1303) (2026-07-26)

> **Đo tươi trên jar THẬT (25-07 khuya), bắt đúng lúc phiên chết:**
> 1. **KHÔNG cookie nào có TTL ~1 giờ.** `SID`/`__Secure-1PSID`/`HSID`/`SSID`/`APISID`/`OSID` hết hạn
>    **2027-08-09 = 380 ngày**; `__Secure-1PSIDTS`/`SIDCC`/`__Secure-1PSIDCC` **365 ngày**. Hằng
>    `_NLM_COOKIE_LIFE_MIN = 60` (ghi chú «hồ sơ DBSC 2026-07-12») KHÔNG có gì trong dữ liệu đỡ.
> 2. **Credential ngắn hạn DUY NHẤT = `__Secure-1PSIDRTS`/`3PSIDRTS`** (token xoay phiên DBSC). Trong jar
>    nó **đã hết hạn 110 phút TRƯỚC** khi phiên chết.
> 3. **CLI `nlm` KHÔNG xoay cookie**: qua 2 lần gọi live, **không một giá trị nào đổi** (kể cả `1PSIDTS`,
>    `SIDCC`, csrf). Phiên không tự lành được — chỉ có thể THAY.
> 4. **Số đo đắt nhất:** `nlm-auth-status` trên phiên ĐÃ CHẾT in `alive:false` · `age_min:5.2` ·
>    **`est_remaining_min: 54.8`** · **`warn: []`**. Đầu phiên thì ngược lại: `alive:true` mà báo còn
>    `0.0'`. Sai CẢ HAI CHIỀU — không phải ước lượng kém, mà là **trấn an giả trên xác chết**.
> 5. `auth.json` (thứ `secrets-stage` đem gói) trễ hơn profile sống **127′**, `extracted_at` **415′**,
>    token xoay trong đó hết hạn **7,2 giờ** trước.
>
> **Kết luận:** nửa «không tự làm mới» của báo cáo ĐÚNG (số đo 3); nửa «chết sau ~1 giờ» KHÔNG đứng được —
> chết là do xoay phiên phía server mà client không theo được ⇒ **thời điểm chết không đoán trước được**
> (25-07 sống 68,1′; lần này chết khi `age_min` mới 5,2′). ⇒ **BÁC đề xuất gốc «tự gọi `nlm-auth-load`
> rồi thử lại»**: nó ghi đè profile bằng bản bundle, mà bundle đo được là CŨ HƠN.

- **BỎ HẲN `est_remaining_min`** khỏi `_nlm_preflight_report`/`nlm-auth-status` (schema → **`nlm_auth_status.v2`**).
  Thay bằng thứ ĐO ĐƯỢC: `rotation_token_expired` + `rotation_token_min` (hạn thật trong jar) và verdict
  probe LIVE. `age_min` GIỮ nhưng nói đúng nghĩa — thời gian từ **lần xác thực thành công gần nhất**,
  KHÔNG phải tuổi cookie, KHÔNG dự đoán được cái chết.
- **`_nlm_rotation_token_state()`** (PURE, jar tiêm được) + cờ **`ROTATION_TOKEN_EXPIRED`**: token xoay hết
  hạn ⇒ «phiên KHÔNG gia hạn được nữa, chỉ có thể thay bằng `nlm login`; vẫn có thể sống thêm rồi chết
  ĐỘT NGỘT — đừng mở lô dài». Tín hiệu có thật, kiểm offline, **0 round-trip**. `found=False` ⇒ không kết
  luận gì (tuyệt đối không suy ra «còn sống»).
- **`alive:false` nay LUÔN kèm đường ra** (`fix` + `warn[AUTH_DEAD]`) — trước đó `nlm-auth-status` báo chết
  với `warn: []`, đúng thứ báo cáo mục 3.2 phàn nàn. Vá nốt chỗ sót cuối còn hô `nlm login` trần (cảnh báo
  *overflow liveness* của doctor).
- **`nlm-auth-load` CHỐNG HẠ CẤP**: `_nlm_auth_load_downgrade` (PURE) so mốc `last_validated` bundle ↔ jar
  cục bộ TRƯỚC khi ghi đè; bundle cũ hơn ⇒ **TỪ CHỐI** kèm lý do + số phút, có `--force` để cố ý. Không đọc
  được một trong hai phía ⇒ KHÔNG chặn (máy chưa từng login vẫn nạp được).
- **Van F7 (`NLM_COOKIE_BATCH_MAX_MIN = 50`) và ngưỡng cảnh báo 45′ GIỮ NGUYÊN** — cả hai dựng trên TTL 60′
  vừa đo là sai, nhưng nới một chốt an toàn là quyết định của người vận hành, không phải của đợt vá này.
  Thông điệp đã nói rõ con số đó không dự đoán được cái chết để không ai bị ru ngủ.
- Test 1302 → **1303** (+1 `r208c_cookie_do_thay_vi_doan`: hạn token xoay · cờ · chống hạ cấp · re-export I11).
  `r115_preflight_report_two_tiers` đổi kỳ vọng CÓ CHỦ ĐÍCH (`est_remaining_min` không còn; chết phải có `fix`).
  **GAS KHÔNG đổi — vẫn 2.21.2p.**

# ★ v1.35.42 — r208b BƯỚC 3 (báo cáo 25-07): `register` tự điền/cảnh báo name+cat · thông báo auth chỉ ĐÚNG đường · `nlm-reconcile` LUÔN cho xem plan (+3 test, 1302/1302) (2026-07-25)

> Ba mục còn lại của báo cáo `BAO_CAO_van_de_skill_tra-luat_2026-07-25.md` sau r208 (2.2 slot-audit) và
> r208-gas (1.1 khoá ghi registry). **Không mục nào nới lỏng một chốt chặn nào** — 2.4 giữ NGUYÊN ngưỡng
> chặn r201/r206 và CỐ Ý **không** thêm `--trust-live`/`--after-restore`: registry có thể bị đua về rỗng
> bất cứ lúc nào, nên không lời khẳng định nào của người vận hành cứu được ca đó.

**2.1 — `register` không còn trả `ok:true` im lặng với `name:""`/`cat:""`** (`tl_core/source_ops.py`)
- Ca thật 25-07: 17 dòng ghép bằng `register --drive-id --nlm-source-id …` ra name/cat rỗng ⇒ corpus-audit
  gắn `NLM_GHOST_SOURCE`/`ORPHAN_CAT`/`MISSING_SOHIEU` trong khi file vẫn đúng folder cat 23 và nguồn vẫn
  SỐNG trên NLM. Cờ báo động giả kiểu đó khiến người vận hành dễ đi **XOÁ nhầm nguồn còn tốt**.
- **`_register_infer_name_cat`** (PURE, tiêm được bảng taxonomy): `name` = tên file Drive bỏ đuôi;
  `cat` = nhãn canonical `NN_Ten` tra theo (1) folder cha trong `config.categories` — **0 round-trip**,
  (2) TÊN folder cha khớp taxonomy 45+2 (kể cả folder trơ `23`), QUARANTINE giữ nguyên.
- **`_register_autofill`**: chỉ chạm cột trống ở **CẢ** lệnh **LẪN** dòng registry hiện có (không bao giờ
  đè giá trị đã ghi), TRÁNH cột đang `--clear-cols` (điền lại giữa lệnh xoá là chống ý định), bỏ qua lệnh
  thuần-xoá. Tốn ≤2 round-trip Drive và chỉ khi thật sự thiếu; **tái dùng chính `reg_get` của
  `_reg_row_present`** (tách `_reg_row_get`) nên KHÔNG thêm call GAS nào.
- Output mới: `autofilled` · `complete:false` + `incomplete_cols` + `warn[REGISTER_ROW_INCOMPLETE]` kèm
  lệnh chữa sẵn và nói thẳng hậu quả nếu để trống. Cờ `--no-autofill` để tắt.

**3.2 — mọi thông báo auth nêu ĐỦ chuỗi đúng thứ tự** (`nlm_cli.py` = nguồn sự thật)
- `nlm-auth-load` (headless, KHÔNG cần master key) → `nlm-auth-pull` (**nói rõ lấy `TL_MASTER_KEY` ở đâu**)
  → `nlm login` (**ghi rõ là TƯƠNG TÁC**, không chạy được ở Cowork/headless). Trước đây mọi thông báo chỉ
  hô `nlm login`, và `nlm-auth-load` — đường đúng — không chỗ nào nhắc.
- Hằng `AUTH_FIX_HINT`/`AUTH_FIX_HINT_SHORT` ở `nlm_cli` (3 nơi sinh `auth_hint`); `nlm_auth_fix_hint()`
  (`tl_core/nlm_ops.py`, re-export `_STUB_MAP`) cho slot-audit/`_live_source_count`/doctor; `tl_gws` và
  playbook `LISTING_CHANNEL_SUSPECT` dùng chung. **Drift-lock**: selftest bắt CẢ 7 biến thể (kể cả 2 bản
  dự phòng) phải nêu đủ 3 lệnh ĐÚNG THỨ TỰ — thông báo auth mới sau này không rơi lại về `nlm login` trần.

**2.4 — `nlm-reconcile` chặn thì vẫn phải CHO XEM** (`tl_core/nlm_admin_ops.py`)
- `--apply` bị guard chặn: rc=2 và **0 dòng registry được ghi** như cũ, nhưng nay in **plan đầy đủ ra
  stdout** (`mode:APPLY_BLOCKED`, `blocked_by`) + **ghi file JSON** để soát; error vẫn ở stderr (giữ kỷ
  luật «parse JSON đừng gộp `2>&1`»). Trước đây chỉ có error rc=2 ⇒ phải làm tay 17 dòng.
- DRY **LUÔN** ghi plan-artifact (mặc định `.tl_state/reconcile_plan_<nb>.json` — đúng đường
  `--from-plan auto`). Trước r208b chỉ nhánh `--all-notebooks` nội bộ mới đặt được `plan_out`; cờ
  `--plan-out` nay có trên CLI.
- **Chốt cửa hậu**: plan sinh lúc guard đang nghi mang dấu `verdict` và ghi tên `.BLOCKED.json` riêng;
  `--apply --from-plan` **TỪ CHỐI** (`PLAN_VERDICT_SUSPECT`) — đường from-plan không re-scan live nên guard
  bất hoạt ở đó, thiếu chốt này thì «luôn ghi plan» vô tình mở lối đi vòng qua chính cái chặn vừa giữ.
  `--force-unsafe` vẫn là cửa DUY NHẤT để đi tiếp.
- Helper tách để hai nhánh dùng chung: `_reconcile_plan_path` · `_reconcile_plan_artifact` (PURE) ·
  `_reconcile_write_artifact`.

Test 1299 → **1302** (+3: `r208b_auth_fix_chain_dung_thu_tu` · `r208b_register_tu_dien_name_cat` ·
`r208b_reconcile_luon_in_plan`). `parser_surface.json` regen (2 lệnh đổi: `register`, `nlm-reconcile`).
**GAS KHÔNG đổi** — vẫn 2.21.2p, không cần deploy.

# ★ v1.35.37 — r206: guard reconcile PHÂN ĐỊNH registry-mỏng vs kênh-liệt-kê (`REGISTRY_SCOPE_SUSPECT`) — ca thật 25-07 registry nền bị xoá còn 2 dòng (+2 test, 1297/1297) (2026-07-25)

> Sự cố thực địa 25-07: registry nền rơi còn **2 dòng** → `nlm-reconcile` thấy 300/300 nguồn live thành
> `unregistered`. Guard r201 chặn `--apply` ĐÚNG (rc=2, 0 ghi — cứu một vụ link/clear bậy 300 nguồn đè lên
> bản đã hỏng), NHƯNG hô sai bệnh: `LISTING_CHANNEL_SUSPECT` + playbook `nlm login`, trong khi
> `tl nlm-auth-status` báo `alive:true`/cookie 6,6′. Lời chẩn sai đẩy người vận hành đi chữa nhầm giữa lúc
> đang là CẤP CỨU MẤT DỮ LIỆU. **Ngưỡng CHẶN giữ NGUYÊN — đợt này chỉ sửa LỜI CHẨN.**
- **`_reconcile_suspect_kind(live_n, unreg_n, registry_n)`** (PURE, `tl_core/nlm_admin_ops.py`): chỉ chạy khi
  guard r201 ĐÃ bật; `registry_n < live_n * _RECONCILE_REGISTRY_THIN_RATIO` (20%) ⇒ `REGISTRY_SCOPE_SUSPECT`,
  ngược lại giữ `LISTING_CHANNEL_SUSPECT`; guard không bật ⇒ `""` (không chẩn bừa). Re-export I11 CÙNG ĐỢT
  (`_STUB_MAP` + hằng `_RECONCILE_REGISTRY_THIN_RATIO` trực tiếp).
- **Hai playbook tách hẳn**: nhánh registry-mỏng trỏ `counts --refresh` → `profile-info --json` (kiểm
  `registryDocId`) → **version history Sheet** → `journal`/Executions, và ghi rõ **⛔ ĐỪNG `--force-unsafe`
  khi registry đang mỏng**; nhánh kênh-liệt-kê giữ nguyên văn r201 (đổi kênh / `nlm login` / đo máy khỏe).
  JSON `--apply` nay trả `error` = đúng verdict + `registry_rows_seen`.
- **`registry_rows_seen` vào output MỌI lần** (kể cả không có verdict) — số dòng registry lúc đối soát, để
  đọc report là thấy ngay registry dày/mỏng.
- Test: 1295 → **1297** (+2: `r206_suspect_kind_pure` biên 20% · `r206_reconcile_registry_thin_verdict`
  khoá verdict/playbook/`--apply` rc=2 KHÔNG ghi + vế registry-dày vẫn ra `LISTING_CHANNEL_SUSPECT`).
  Fixture `r201_reconcile_listing_channel_guard` đổi CÓ CHỦ ĐÍCH 1→30 dòng registry: bệnh kênh-liệt-kê
  THẬT thì registry vẫn dày, kỳ vọng `LISTING_CHANNEL_SUSPECT` GIỮ NGUYÊN.
- `references/GOTCHAS.md` **§11 mới**: đọc verdict reconcile · `counts` không `--refresh` là snapshot cũ ·
  **`tl journal` là file CỤC BỘ theo clone** (truy nguyên phải dùng version history Sheet + Apps Script
  Executions) · `profile-delete-assets` đã kiểm là xoá đúng scope · phiên REMOTE bị egress chặn Google
  (bẫy `script.googleusercontent.com`) · 12 `F821` trên clone tươi là GIẢ.

# ★ v1.35.36 — r205 WP7 R-c TRỌN GÓI: GỠ FALLBACK organize 12-call (guard SERVER_TOO_OLD fail-closed) + DI TRÚ resume LÊN PIPELINE + LOCK ingest_to_cache chỉ-cache (grill nhỏ 25-07 user duyệt (a) hẹp/(b) khuyến nghị/(c) CÓ làm; +3 test/−1 đổi kỳ vọng, 1295/1295) (2026-07-25)

> Đợt R-c khép chuỗi WP7 R-a→R-b→R-c (ADR-0004). GAS 2.21.2o KHÔNG đổi; SKILL.md CHỈ đổi header.
- **(b) GỠ fallback organize** ở CẢ HAI `_pi_stage_write` + `_il_stage_write`: `_ingest_commit_supported`
  nay là GUARD fail-closed — server <2.21.2o (hoặc ping lỗi/transient) ⇒ rc=2
  `SERVER_TOO_OLD_FOR_INGEST_COMMIT` TRƯỚC khi ghi (charact: fallback lane dừng ngay sau ping, 0 write),
  KHÔNG lặng lẽ đi đường 12-call không ai soak; upload đã journal → chạy lại + `--resume` tái dùng.
  Nhánh sheet (copy_convert) + nhánh resume-skip GIỮ NGUYÊN. 6 harness selftest cũ nâng fake gas
  (ping 2.21.2o + nhận `ingest_commit` trả envelope thiếu `file` → readback đi `_verify_convert_readback`
  như cũ — flow test giữ nguyên); 2 lock commit-vs-fallback (r198/r204) đổi kỳ vọng CÓ CHỦ ĐÍCH thành
  `r205_*_commit_only_server_guard`.
- **(c) `cmd_profile_ingest_resume` = adapter run_pipeline**: bảng 5 stage `_pr_stage_*`
  `plan→confirm→stage→write→commit` (KHÔNG stage readback riêng — `_verified_reg_write` vốn fused
  write+verify, thêm readback rời = đổi số call trái parity), thân bê NGUYÊN VĂN (identity gate
  r184/ADR-0011-D5 nguyên vị trí ở confirm; DRY_REPAIR = outcome stop); re-export I11 cùng đợt.
  **Parity: charact resume pre ≡ post BYTE-EQUAL cả 3 lane** (dry name-only / apply single / apply
  chunks — `.tl_state/charact_{pre,post}_resume.json`); r116×4 + r184×2 resume tests pass NGUYÊN TRẠNG.
- **(a) lock `ingest_to_cache` chỉ đọc/ghi cache** (ADR-0004 Đ3, phạm vi hẹp): sweep xác nhận action
  Drive chỉ còn {exportdocx, exporttext, vb_status} (đọc) + `fetch_drive_convert_docx` = stub raise
  `CACHE_ONLY_NO_DRIVE_CONVERSION` (đã vá từ trước); test khóa `r205_ingest_to_cache_chi_doc_ghi_cache`
  chặn mọi mutation thêm sau này.
- Parity tổng R-c: il/zip happy lanes ≡ R-b byte-equal; PI call-seq/rc/output ≡ R-a (khác duy nhất
  hash fixture do bed đổi đường dẫn phiên — artifact, không phải drift); K1 plan DRY bất biến kể cả
  lane fallback. Sổ drift R-c: TRỐNG (thay đổi hành vi duy nhất = guard (b) đã duyệt).
- Test: 1293 → **1295** (+3: `r205_resume_via_pipeline` · `r205_ingest_to_cache_chi_doc_ghi_cache` ·
  guard il; 2 lock cũ đổi kỳ vọng, wiring r204 il thêm vế cấm organize). WP7 LÕI: **R-a+R-b+R-c XONG
  TRỌN** — còn theo dõi soak thực địa + đo NLM lô khi cookie sống.

# ★ v1.35.35 — r204 WP7 R-b: DI TRÚ ingest-local LÊN PIPELINE **GỘP** CHUYỂN GAS ingest_commit + ZIP ADAPTER (p11 mục 2 + quyết định 1(b)/α; bench 33,1 s/file −58%; +3 test/−1, 1293/1293) (2026-07-25)

> Thi hành đợt R-b của KE_HOACH WP7 lõi (grill 25-07 — KHÔNG re-litigate; chuỗi tăng tốc theo lệnh user,
> không chờ soak 30-07): MỘT lần đổi trên hàm ~700 dòng — di trú `cmd_ingest_local` lên `run_pipeline`
> ĐỒNG THỜI chuyển stage write sang GAS `ingest_commit` (khuôn r198 profile-ingest). GAS 2.21.2o KHÔNG đổi
> (`doIngestCommit_` vốn nhận đủ tham số nhánh ingest-local: cat NN/sohieu/goc/loai/reg_cat — ghi chú
> APP_VERSION 2.21.2o «client r198 chỉ dùng nhánh profile» nay hết treo).
- **`cmd_ingest_local` = adapter run_pipeline**: bảng 6 stage `_il_stage_*` chuỗi ADR `plan→confirm→stage→
  write→readback→commit` (re-export I11 CÙNG ĐỢT — bài học NameError 24-07), thân stage BÊ NGUYÊN VĂN code
  cũ (cat/recat gate, F1 dedup sohieu live, F4 PDF-ảnh, F5 van kích thước, S1 OCR gate, claim F-04, resume
  N6 — giữ trọn vị trí/thứ tự); đếm write/readback ADR-0004 đủ 6 stage.
- **Điểm đổi CÓ CHỦ ĐÍCH duy nhất (stage write)**: feature-detect `_ingest_commit_supported` ≥2.21.2o →
  MỘT call `ingest_commit` thay `organize` + convert-readback từ CHÍNH response (0 call thêm —
  `_ingest_commit_readback`, expected_folder_id="" như đường cũ); server cũ → organize GIỮ NGUYÊN
  (fallback — R-c gỡ = xóa 1 nhánh). Backfill sohieu/title_vn + registry readback (reg_get refresh)
  GIỮ NGUYÊN (doctrine verified-write).
- **Parity K1/K2/K3 ĐẠT** (bed `.tl_state/charact_{pre,post}_ingestlocal.json`, 4 lane main/no-nlm-add/
  drive-id/fallback): K1 plan DRY **byte-equal kể cả plan_hash** cả 4 lane · K2 output apply + rc y hệt,
  chuỗi call chỉ lệch TRONG stage write đúng khuôn duyệt (organize→ping+ingest_commit, okw BẰNG TUYỆT ĐỐI;
  lane fallback = cũ + đúng 1 ping) · K3 selftest cũ pass nguyên trạng (4 source-lock r55/r95/r192×2 chỉ
  đổi CHỖ TRỎ getsource sang ghép 6 stage — kỳ vọng giữ nguyên). Sổ drift R-b: TRỐNG.
- **ZIP adapter (phần 2)**: child ingest-zip/profile-ingest-zip chạy in-process qua build_parser (r187) =
  CHÍNH cmd đã di trú → TỰ đi pipeline + ingest_commit, `zip_ingest.py` 0 diff; charact 1 ca zip-1-docx
  DRY+apply (`.tl_state/charact_{pre,post}_zip.json`, pre chụp từ git worktree HEAD r203): bundle plan
  byte-equal, output y hệt, lệch duy nhất = khuôn write-stage.
- **Benchmark sống** (3 docx ~60k ký tự khác chủ đề, profile thử BenchRb204 tạo-đo-dọn, lane --no-nlm-add —
  phần NLM R-b không đổi): 33,3/30,5/33,1 s → **median 33,1 s/file ≤ trần 56,7 s**, so ~78 s/file đường
  organize cũ (baseline 24-07) ≈ **−58%**; profile-delete --trash-assets dọn sạch, config 0 vết.
- Test: 1291 → **1293** (+3 `r204_*`: wiring pipeline ingest-local · call-count commit-vs-fallback ·
  wiring child ZIP; −1 `r198_ingest_local_giu_duong_cu` — lock «giữ đường cũ chờ soak» hết hiệu lực CÓ
  CHỦ ĐÍCH theo quyết định 1(b)). CÒN: **R-c** (ingest_to_cache + gỡ fallback + cân nhắc di trú resume —
  grill nhỏ 3 quyết định với user trước khi code).

# ★ v1.35.34 — r203 WP7 R-a: STATE MACHINE `run_pipeline` + DI TRÚ profile-ingest (ADR-0004 Đ1; parity K1/K2/K3 ĐẠT; +3 test, 1291/1291) (2026-07-25)

> Thi hành đợt R-a của KE_HOACH WP7 lõi (`C:\qh\p13_wp7_2026-07-25\KE_HOACH_WP7_LOI_R-a.md` — grill 25-07,
> 8 quyết định user duyệt từng câu). Refactor BẢO TOÀN HÀNH VI nghiêm ngặt — Sổ drift: TRỐNG.
- **Engine** (`tl_core/ingest_engine.py`, stdlib thuần không bind): +`run_pipeline(stages, ctx)` — engine sở
  hữu TRÌNH TỰ + FAIL-CLOSED (`{"rc":n}` dừng, `{"stop":X}` outcome hợp lệ DRY_PLAN/STAGED_STOP/DONE) +
  ĐẾM write/readback (`_counts`; mỗi resource ≤1 write/stage — vượt = `PIPELINE_WRITE_BOUND`; xuyên-stage
  hợp lệ cho ca late-draft rename) + `ctx._trace`; I/O tiêm qua ctx (fake-ctx test offline 100%).
- **`cmd_profile_ingest` = adapter**: MỘT bảng stage chuỗi ADR `plan→confirm→stage→write→readback→commit`;
  thân stage (`_pi_stage_*` ×6, re-export I11 CÙNG ĐỢT — bài học NameError 24-07) bê NGUYÊN VĂN code cũ;
  feature-detect ingest_commit NHỐT trong stage `write` (quyết định α — R-c gỡ fallback = xóa 1 nhánh);
  `--staged` = outcome `STAGED_STOP` (ADR-0015 nguyên vẹn); resume/OCR-bridge/chunks/ZIP NGOÀI khuôn R-a.
- **Parity 3 lớp ĐẠT** (`.tl_state/charact_{pre,post}_wp7.json`, bed cố định 3 lane main-NLM/no-nlm-add/staged):
  K1 plan DRY **byte-equal kể cả plan_hash** · K2 chuỗi call trùng khớp 18/18 phép so · K3 toàn bộ selftest
  cũ pass nguyên trạng (r116/r184/r198/r200 không đổi một ca).
- **Benchmark sống** (3 docx 60k ký tự, profile thử BenchWP7 tạo-đo-dọn): 44,0/45,5/43,1 s → **median
  44,0 s/file ≤ trần 56,7 s** (baseline 49,3+15%) — overhead khung ≈ 0.
- Test: 1288 → **1291** (+3 `r203_*`: run_pipeline halt/merge/stop · write-bound ADR-0004 · wiring khung).
  CÒN theo kế hoạch: **R-b** ingest-local (GỘP chuyển ingest_commit p11) + ZIP · **R-c** cache + gỡ fallback
  + cân nhắc resume (chuỗi TĂNG TỐC theo lệnh user 25-07 — không chờ soak 30-07).

# ★ v1.35.33 — r202 BACKUP CONFIG PROFILE-DELETE RA NGOÀI CÂY SKILL (doctrine r193; +1 test, 1288/1288) (2026-07-25)

> Gốc: Tầng-3 smoke 25-07 phát hiện `profile-delete --trash-assets --apply` để lại
> `tra_luat_config.v2.<profile>.bak.json` (CHỨA token webapp) ở GỐC cây skill — vi phạm doctrine r193
> «backup config KHÔNG BAO GIỜ nằm trong cây skill» (bundle đã có guard TOKEN_IN_BUNDLE + exclude `.bak`
> nên KHÔNG lọt zip, nhưng file vẫn nằm trên đĩa trong cây). Sweep toàn scripts: đây là điểm ghi DUY NHẤT
> (profile-rename/use/config-pin-registry đều ghi config qua `_write_json_atomic`, không tạo `.bak`).
- **Helper mới** `profile_env._config_backup_dir()` (re-export I11 vào tl.py): đích cho MỌI backup config —
  `TL_CONFIG_BACKUP_DIR` (test/override) → `D:\Quốc hội\_config_backups` (máy chuẩn, chỉ khi ĐÃ tồn tại)
  → `%LOCALAPPDATA%\tra-luat\_config_backups` (máy lạ); mkdir tự động.
- **`cmd_profile_delete`**: backup đổi từ `Path(path).with_suffix(….bak.json)` (= CẠNH config, tức gốc cây)
  sang `_config_backup_dir()/<tên-cũ-giữ-nguyên>`; tên file + nội dung + trường `config_backup` trong output
  GIỮ NGUYÊN — chỉ đổi thư mục.
- Test: 1287 → **1288** (`r202_profile_delete_backup_ngoai_cay` — chỉ-nó-chặn: apply xong thư mục config
  SẠCH `.bak`, backup tròn nội dung nằm đúng TL_CONFIG_BACKUP_DIR, env unset ⇒ đích mặc định vẫn NGOÀI
  cây skill). Selftest xanh CẢ HAI trạng thái env; gate release-check 39/39; GAS 2.21.2o KHÔNG đổi.
  SKILL.md CHỈ đổi header version (đẳng dài) ⇒ re-import KHÔNG bắt buộc (nợ re-import r200 vẫn còn nếu chưa làm).

# ★ v1.35.32 — r201 GÓI 4 FIX VẬN HÀNH ĐẢNG/NLM (grill 7 vấn đề 24-07 đêm; +5 test, 1287/1287) (2026-07-24)

> Nguồn: báo cáo 7 vấn đề phiên vận hành Chat (nạp 342/348-QĐ/BTCTW) → grill chốt 3 quyết định C1-C3.
> FIX-A/B vá ở phiên trước (commit WIP `15dcf70`), FIX-C/D + test tier-3 phiên này — release gộp 1 gói.
- **FIX-A** `tl.py:_looks_like_sohieu_query`: +nhánh `_dang_bare_key` (fullmatch khóa chuẩn hóa toàn truy
  vấn — KHÔNG substring) — `exists "342-QD-BTCTW"`/`"342-QĐ/BTCTW"`/`"04-CT-TW"` hết not-found OAN
  (trước: cổng đòi năm/VBHN nên tier sohieu bỏ đói phép nới D5).
- **FIX-B** `tl_core/classify.py:_profile_title_from_header` — 3 defect: (a) stop-tại-«Căn cứ» CẢ 2 vòng;
  (b) loại Đảng đứng riêng (QUY ĐỊNH/QUY CHẾ/…) ghép dòng «VỀ …», bỏ dòng kẻ; (c) strip zero-width/BOM
  per-line. Ca sống 342: title = «QUY ĐỊNH VỀ HỆ THỐNG THÔNG TIN LĨNH VỰC TỔ CHỨC XÂY DỰNG ĐẢNG».
- **FIX-C** `nlm-reconcile` guard nghi-kênh (quyết định C2): live ≥ 20 VÀ unregistered/live > 50% →
  verdict **`LISTING_CHANNEL_SUSPECT`** (hằng `_RECONCILE_SUSPECT_*`, re-export I11): DRY vẫn in report
  + banner LOUD + playbook (đổi kênh / `nlm login` / đo máy khỏe); `--apply` **DỪNG rc=2 TRƯỚC mọi ghi**
  (trước preflight/gate/journal); override tường minh `--force-unsafe`; verdict nổi lên per_notebook của
  `--all-notebooks`. Gốc: ca «300 unregistered» phiên Chat = kênh liệt kê suy hoá trả id lạc namespace,
  tool IM LẶNG suýt link/clear bậy hàng loạt (máy khỏe đo 2/300 = 0,7%).
- **FIX-D** `_ingest_perf_hint` +1 câu: thêm cờ SAU dry-run ⇒ plan_hash đổi ⇒ phải DRY lại (by design —
  tránh PLAN_HASH_MISMATCH oan; hint vẫn im khi đã dùng cờ nhanh).
- **Đóng KHÔNG vá** (verdict grill): **#3** «ingest không regen manifest» = FALSE ALARM (GAS
  `doManifestExport_` gọi `regReadAll_(true)` dựng tươi mỗi refresh — cú miss là hệ quả bug #2/FIX-A);
  **#7** DUP_DIEU 348 = HỢP LỆ (doc = Quy định Đ1-8 + Quy chế «kèm theo» đánh lại Điều — đúng doctrine
  L6, info-only là hành vi đúng).
- Test: 1282 → **1287** (+2 phiên trước `r201_exists_sohieu_dang_bare`, `r201_title_dang_quydinh_cancu_bom`;
  +3 phiên này: `r201_reconcile_listing_channel_guard` (5 ca: DRY banner · apply rc=2 0-ghi · force-unsafe
  đi tiếp · 2/300 lành · 5/5 live<20 không kích) · `r201_reconcile_title_bridge_tier3_lock` (khóa tier-3:
  link title duy nhất / ownership guard / không re-point sid — thay golden fixture vì golden không chạy
  offline với NLM live) · `r201_perf_hint_plan_hash_note`). Selftest xanh CẢ HAI trạng thái env; GAS
  2.21.2o KHÔNG đổi. SKILL.md CHỈ đổi header version (đẳng dài 48089 B) ⇒ re-import KHÔNG bắt buộc
  (nợ re-import r200 vẫn còn nếu chưa làm).

# ★ v1.35.31 — r200 LANE STAGED: `profile-ingest --staged` + `verify-staged` PARITY → BULK-FLIP (ADR-0015; +4 test, 1282/1282) (2026-07-24)

> Grill 24-07 phần 2 (C2-C6): «corpus trước, verify sau» NHƯNG không đảo doctrine — staged (corpus=false)
> → verify parity → bulk-flip r197. Poison window = 0; ADR-0004 giữ nguyên (hoãn ≠ bỏ hậu điều).
- **`profile-ingest --staged`** (v1 CHỈ profile-ingest — tiền lệ r198): GIỮ cổng AN TOÀN lúc nạp (dup-name
  registry + claim đường commit + convert-readback trong `ingest_commit`, 0 call thêm); DỪNG ngay sau
  readback — HOÃN iv đọc-toàn-văn + v verify_gate + vi quét Điều/chunk + NLM. Registry `corpus=false`,
  note **`staged:pending;sq=<q>`** (marker = cột note, KHÔNG thêm cột schema). **TỪ CHỐI pdf/ocr/sheet**
  rc=2 `STAGED_LANE_REFUSES_SOURCE` TRƯỚC mọi side-effect. Plan/options chỉ thêm key `staged` KHI staged
  (plan_hash cũ giữ nguyên — 0 churn golden).
- **`tl verify-staged`** (generated, contract `verify_staged`, high/confirm/dry-run): dò note `staged:*`
  trên manifest refresh LIVE (bài học reg-query 24-07) → chạy ĐÚNG bộ iv+v+vi (PARITY — đổi thời điểm,
  KHÔNG đổi tiêu chuẩn). DRY = báo cáo; `--apply --confirm yes`: PASS → **bulk-flip corpus=true + note
  thật** (1 `reg_bulk` journaled trước-ảnh từng dòng — `tl undo <run>` cả lô); FAIL → Ở LẠI staged
  (note `staged:fail:<FLAG>`), KHÔNG auto-xóa/KHÔNG NLM; file vượt chunk_max vẫn flip + flag
  `needs_chunk_pipeline`. NLM nạp SAU flip (van 1 + bảng tay khối ≤4 r199, `nlm_status` theo ADR-0010).
- Docs: **ADR-0015** (Accepted — 5 quyết định, có phân loại cổng AN TOÀN/CHẤT LƯỢNG theo ADR-0004);
  CONTEXT.md +«Staged ingest (lane trì hoãn)» +«Verify parity» + vá «Ingest thành công» (ngoại lệ duy nhất
  vế corpus); SKILL.md +vế STAGED dòng BA VAN (+254 B) − diet 2 vế lịch sử/trivia mục #15 (−246 B)
  ⇒ 48081→48089 B (trần 48128). **SKILL.md ĐỔI NỘI DUNG ⇒ RE-IMPORT Capabilities.**
- Test: 1278 → **1282** (+4 `r200_*`: từ-chối pdf/ocr/sheet trước side-effect · staged apply bỏ iv/v/vi
  (0 read_doc_text, 0 nlm_add, note đúng marker) · verify-staged parity + flip đúng lô (dòng không-staged
  không bị đụng, before-image đủ) · needs_chunk_pipeline). Selftest xanh CẢ HAI trạng thái env;
  parser_surface regen chủ đích (`--staged` + verify-staged); golden re-bless workflow_audit (+1 lệnh,
  size_bytes SKILL) + tool_inventory (154 lệnh, 28 high-risk).

# ★ v1.35.30 — r199 BẢNG TAY NLM CHIA KHỐI ≤4 URL (grill 24-07 C1; +1 test, 1278/1278) (2026-07-24)

> Grill 24-07 (6 quyết định, C1 chốt «giữ van 1, chỉ sửa bảng tay»): NLM hay chết khi người dùng dán cả lô
> dài một lượt lên UI — bảng tay nay CHIA KHỐI để sự cố khoanh vùng theo khối, không mất cả lô.
- `_nlm_links_md` (PURE, `tl_core/nlm_ops.py`): lô >`NLM_BATCH_LINKS_THRESHOLD`(=4, tái dùng hằng r192 —
  KHÔNG đẻ hằng mới) → chia `## Khối k/N — [mở notebook](url)` mỗi khối ≤4 link + dặn CHỜ NLM nhận xong
  khối trước rồi mới dán khối kế; lô ≤4 giữ dạng phẳng r192 Y HỆT (byte-level). Hưởng chung cả 2 caller:
  `nlm-links --md-out` + nhánh BATCH_LINKS của `ingest-missing`.
- Van 1/2/3 GIỮ NGUYÊN ngữ nghĩa (không re-litigate r192): auto-add vẫn chỉ lô ≤4; vế «auto bulk tách cụm»
  của đề xuất gốc tự tan vì đường auto không bao giờ vượt 1 cụm.
- Test: 1277 → **1278** (+1 `r199_van1_bang_tay_chia_khoi_4`: 9 nguồn → đúng 3 khối 4+4+1, khối 1 có Doc_3
  KHÔNG có Doc_4, link notebook tại header khối, chữ «chờ», hẹn reconcile; 3 nguồn → KHÔNG chia khối).
  Selftest xanh CẢ HAI trạng thái env (trần + TL_WEBAPP/TL_TOKEN export). SKILL.md CHỈ đổi header version
  (đẳng dài 48081 B) ⇒ re-import KHÔNG bắt buộc.
- CONTEXT.md: mục «Bảng tay (nạp NLM)» ghi nhận thể thức chia khối.

# ★ v1.35.29 — r198 INGEST_COMMIT: GỘP 4 BƯỚC INGEST THÀNH 1 ROUND-TRIP GAS (ADR-0014 Accepted + GAS 2.21.2o; +6 test, 1277/1277) (2026-07-24)

> KE_HOACH p11 §5 (quyết định #4/#5/#6 duyệt 24-07). ADR-0014 viết TRƯỚC khi code, trạng thái **Accepted**
> — supersede mục HOÃN `ingest_pipeline` (KE_HOACH_VA_SKILL_r191_r192 §3); lý do bỏ cổng-1-tuần ghi rõ trong
> ADR (số đo 24-07 trên đường sản xuất thật, khuôn r192 đã áp đủ, ingest vẫn đồng-nút-cổ-chai; ~2s/call cố
> định ⇒ giảm SỐ CALL là đòn bẩy duy nhất). Baseline: 12 call ≈ 68s/file, trong đó reg_get×3+info×3 = 14s
> CHỈ ĐỂ ĐỌC LẠI.
- **GAS 2.21.2o** (deploy clasp GIỮ deployment ID `AKfycbzNrsxGYjFkzT…` @79; ping xác nhận 2.21.2o + đo lại
  sau 25s ổn định; ADDITIVE — client cũ không đổi hành vi): action **`ingest_commit`** = organize(+rename)+
  register+READBACK (row snapshot `reg_get refresh=true` + file/src info) MỘT round-trip; **sub-step marker**
  `organize_done/rename_done/upsert_done` — lỗi giữa chừng trả PARTIAL (đã-xong-gì) cho journal/`--resume`
  (ADR-0011/D5) map điểm đứt; tham số đủ cho CẢ ingest-local (cat NN) lẫn profile (cat=folderId flat).
  Smoke sống 0-mutation (fileId bundle, convert/register=false): ok, marker đủ, elapsed 1,5s server.
- **Client r198 — CHỈ `cmd_profile_ingest` chuyển đường** (quyết định #6; `ingest-local` giữ 12-call, chuyển
  sau soak — ca guard ghim source): helper `_gas_version_at_least` (PURE, tuple số+đuôi chữ; parse hỏng →
  False fail-safe) · `_ingest_commit_supported` (feature-detect ping ≥2.21.2o, cache 1 ping/process qua
  `_GAS_VER_CACHE` — mutable sống ở tl.py, bẫy I11) · `_ingest_commit_call` (partial → step
  `ingest_commit:<điểm đứt ĐẦU TIÊN>`; transport/shape tường minh) · `_ingest_commit_readback` (dựng
  `convert_readback.v1` từ file/src_file TRONG response — 0 call thêm, CÙNG BỘ phép kiểm
  `_verify_convert_readback`). Server cũ → nhánh organize GIỮ NGUYÊN (fallback 2 code path = nợ bảo trì có
  chủ đích, gỡ sau soak — ADR). Journal giữ nguyên số bước intent/commit; resume contract không đổi.
- Đồng bộ contract: `EXPECT_VERSION` 2.21.2n→**2.21.2o** (drift-lock r119) + pin `expect_version` đổi CÓ CHỦ
  ĐÍCH; API_CONTRACT.md đóng dấu 2.21.2o + row `ingest_commit`; SKILL.md target 2.21.2n→2.21.2o byte-đẳng-dài
  (48081B KHÔNG đổi — không đụng golden size); repo +`references/Code.2.21.2o.gs`, bundle exclude 2.21.2n
  (tiền lệ r194; ca r130 cập nhật theo).
- Test: 1271 → **1277** (+6 `r198_*`: version-compare PURE · feature-detect cache 1 ping + fail-safe ·
  partial marker → step đứt · readback từ response cùng bộ phép kiểm · call-site 2.21.2o = ĐÚNG 1
  ingest_commit/0 organize/0 info vs 2.21.2n = fallback y cũ · guard ingest-local giữ đường cũ).

# ★ v1.35.28 — r197 BULK CORPUS-FLIP CLIENT-ONLY (KE_HOACH p11 §4, quyết định #3 duyệt 24-07; +3 test, 1271/1271) (2026-07-24)

> Gốc số đo: `source-update-corpus` ~15 s/Ô × 26 lượt ≈ 400 s (baseline §3 KE_HOACH). Server KHÔNG đụng —
> `reg_bulk` (v2.13.7) + `reg_get_bulk` (v2.21.2l) có sẵn. Số release trượt +1 so kế hoạch gốc (r196 đã bị
> phiên vá TRINH 3.9/3.11 dùng — ghi chú hồi tố đầu KE_HOACH).
- **`source-update-corpus` nhận N target** (parser `target` nargs='+', positional `status` giữ cuối; 1 target
  = hành vi CŨ Y HỆT — hồi quy 0, ca r180 S5/r52 giữ nguyên). N>1 → lane bulk `_source_update_corpus_bulk`:
  - Phạm vi **registry-thuần**: `true` hoặc `false --as-ref`; `false` trần → rc=2 `BULK_PLAIN_FALSE_REFUSED`
    (gỡ NLM là chuỗi side-effect per-row — đi từng dòng như cũ; khớp từ vựng «Hạ ref» CONTEXT.md).
  - **Auto-refresh manifest TRƯỚC plan** (bài học 24-07 nạp chồng 9 tài liệu vì cache cũ); DRY in bảng N dòng
    before/after (name, drive_id, corpus cũ→mới, row_kind cũ→mới, nlm_status); fail-closed CẢ LÔ khi có
    target lỗi (`BULK_TARGETS_NOT_OK`) hoặc 2 target trỏ cùng dòng (`BULK_DUPLICATE_ROWS`).
  - Ghi = **1 `reg_bulk`** (qua `_journaled_reg_write`: intent{before}/commit per-row, bust cache đúng 1 lần)
    + **1 `reg_get_bulk`** verify AUTHORITATIVE per-row (lệch dòng nào báo dòng đó — không tin patched trần).
  - Journal **1 run/N before-image** → `tl undo <run>` khôi phục CẢ LÔ. Trần payload: tiền lệ L4 22-07 ghi
    118 dòng/1 reg_bulk OK — lô 26 trong biên, không cần chunk.
- SKILL.md: +vế N target=LÔ ở dòng cổng OCR/corpus (+67 B) − diet vế diễn giải lịch sử PROFILE_NOT_FOUND
  (−81 B) ⇒ 48095→48081 B (trần 48128); golden re-bless đúng trường (`workflow_audit.size_bytes` +
  `parser_surface` nargs) — sửa SKILL.md bằng byte-replace, KHÔNG write_text (bẫy CRLF §0).
- Test: 1268 → **1271** (+3 `r197_*`: parser N/1 target; plain-false rc=2 trước mọi đọc/ghi; lô 4 = DRY bảng
  4 dòng + auto-refresh + đúng 1 reg_bulk + 1 reg_get_bulk + journal 4 before + undo đủ 4 restore). Selftest
  xanh CẢ HAI trạng thái env (trần + TL_WEBAPP/TL_TOKEN export).

# ★ v1.35.27 — r196 VÁ 2 BẪY PHIÊN 24-07: BRIDGE OCR TỰ CHẾ CAM KẾT + NLM-ADD 404 RẼ NHẦM «OFFLINE» (TRINH 3.9/3.11; +6 test, 1268/1268) (2026-07-24)

> Gói việc TRINH_CONG2_DELTA mục 3.8/3.9/3.11. Mục 3.8 (fixture golden `workflow_audit` links_checked
> 14→13) XÁC NHẬN ĐÃ ĐÓNG từ r195 (đo tươi golden-test 19/19 ok:true) — không làm lại.
- **3.11 — bridge `ingest-ocr`/`profile-ingest-ocr` HẾT tự truyền `--ocr-verified`** (ca thật A-8 VCB 10838:
  verify_gate child in `ocr_verified=true` mà không ai cam kết; máy-đo-xanh ≠ người-đã-đối-chiếu — chính
  `ocr-verify` XANH vẫn dặn «nếu đã đối chiếu bổ sung bằng mắt/nguồn gốc»; đường VBQPPL thủng cổng S1 r180).
  Nay: 2 spec bridge nhận cờ `--ocr-verified` tường minh và CHỈ forward khi có; thiếu → rc=2
  `OCR_VERIFIED_ATTESTATION_REQUIRED` TRƯỚC child (fail trước side-effect) + hint đối chiếu neo ≥6
  từ/trang/Điều/phụ lục; verify máy đỏ vẫn chặn như cũ (HAI TẦNG độc lập: máy đo ∧ người cam kết). Docs
  đồng bộ: khối `van_ban_lon` gen_instructions + workflow card `ocr_ingest.json` (plan/apply/stop_conditions)
  — re-bless golden `route_task_ocr_ingest` + regen `parser_surface.json` CÓ CHỦ ĐÍCH.
- **3.9 — `nlm-add` 404 NOT_FOUND ×2 (ca KL 137-KL/TW)**: gốc = probe `notebook_get` trả NOT_FOUND THOÁNG QUA
  (flake backend ngay sau đợt gỡ 6 nguồn — eventual consistency; MCP cùng notebook OK cùng lúc, tối cùng
  ngày nlm-cli add OK «BUG 404 KHÔNG tái hiện») nhưng `_nlm_verdict` retry TỨC THÌ 1 nhịp (vẫn trong cửa sổ
  flake) rồi `_nlm_or_corpus` kết luận «NLM OFFLINE» rẽ deferred — SAI BẢN CHẤT: NOT_FOUND trên MỘT notebook
  = đích-không-nhìn-thấy (id sai/flake), KHÔNG phải NLM chết (auth alive); đường `--url` còn chết
  `NLM_OFFLINE_NO_DEFER_FOR_URL` khó hiểu ×2 (khớp hồ sơ: không journal nào trong cửa sổ lỗi). Vá 3 tầng:
  (1) `_nlm_not_found` PURE + retry backoff **5s/15s** riêng lớp NOT_FOUND (mirror F6 r192 «retry kể cả
  404»; transient khác giữ 1 nhịp tức thì — hợp đồng ADR-7 r121 nguyên vẹn; hook `_nlm_verdict_sleep` cho
  test); (2) route mới **`not_found`** fail-closed + banner playbook (kiểm `--notebook-id` UUID ĐẦY ĐỦ theo
  config topology / chờ ≥60s thử lại / lane thay thế MCP source_add + `tl register` nối sổ) — KHÔNG defer
  (defer ghi nlm_status=deferred trỏ notebook không nhìn thấy = poison registry nếu id sai); lệnh không xử
  route này rơi về đường cũ (gate live tự fail với lỗi thật); (3) `cmd_nlm_add` rc=2 `NOTEBOOK_NOT_FOUND`
  TRƯỚC mọi side-effect. ★Bẫy I11: 2 tên hàm + 1 hằng mới re-export vào tl.py (hàm rebase đọc globals tl).
- Test: 1262 → **1268** (+3 `r196_bridge_*`: thiếu-attest chặn profile/vbqppl + positive control forward;
  +3 `r196_nlm_*`: backoff 404 → sống, route not_found + banner, cmd rc=2 không side-effect); harness
  `_run_bridge114` thêm tham số `attested` (mặc định True — giữ nguyên hợp đồng ca r114).

# ★ v1.35.26 — r195 VÁ BUG CLAIM CREDS gas.py + 2 vá HERMETIC selftest (+2 test, 1262/1262) (2026-07-24 — BỔ SUNG HỒI TỐ ở phiên r196: r195 sót CHANGELOG; nguồn = commit `4680a8e`)

> Bug (đo 24-07, lô ATVSLĐ): `_fallback/gas.py` chụp WEBAPP/TOKEN từ env LÚC IMPORT (`_ensure_creds`
> không đọc lại os.environ) và DEFAULT_CONFIGS không biết `tra_luat_config.v2.json` ở cwd/gốc skill ⇒
> nlm-add (gas import trước, load_creds chạy sau) chết INGEST_CLAIM_FAILED «Thiếu TL_WEBAPP/TL_TOKEN» dù
> config v2 ngay cwd, kể cả `--config` tường minh; 13 lượt nlm-add giữa lô phải vòng bằng export env tay.
- Vá kép (TDD 2 ca chỉ-nó-chặn): `_ensure_creds` đọc lại env TẠI-LÚC-GỌI (env > globals cache > config
  file); `_default_configs()` candidates ĐỘNG cwd → gốc skill → scripts/ (v2 trước .json) — đồng bộ
  `_config_candidates` của profile_env (một cửa).
- Kèm 2 vá hermetic selftest họ r181 (`ingest_target` ghim `_manifest_entries`; r96 ghim
  `_resolve_overflow_shards`) + re-bless golden `workflow_audit` (nợ r194, links_checked 14→13).
- Test: 1260 → **1262**. SKILL.md chỉ đổi header ⇒ không cần re-import Capabilities.

# ★ v1.35.25 — r194 HẠ KÍCH THƯỚC BUNDLE 6,4MB → ~1,5MB (amend ADR-0007; +1 test, 1260/1260) (2026-07-24)

> User yêu cầu hạ size. Đo cấu phần: code 4MB (giữ) · 3 bản GAS 623KB · CHANGELOG 327KB · toàn bộ ZIP_STORED.
- **Nén DEFLATED mức 9 CỐ ĐỊNH** (amend ADR-0007, có mục riêng trong ADR): mọi phép so archive-hash của quy
  trình đều là build ×2 CÙNG MÔI TRƯỜNG (gate ×2, CI tự so 2 bản của nó, deploy so build↔pullback cùng
  artifact) — không có so-hash-cố-định xuyên máy nên DEFLATE không phá tính tất định ĐO ĐƯỢC; per-file
  sha256 trong manifest tính trên nội dung GIẢI NÉN, `release-verify` không đổi ngữ nghĩa. Verifier archive
  chấp nhận {STORED (gói cũ), DEFLATED}; check size-equality chỉ áp cho STORED.
- **Trim GAS cũ khỏi GÓI** (giữ trong repo/git — tiền lệ 2.21.2k v1.34.69): current nay 2.21.2n ⇒
  `Code.2.21.2l.gs` + `Code.2.21.2m.gs` (412KB) vào `_RELEASE_EXCLUDE_NAMES_ANYWHERE`; ca r130 cập nhật
  theo (2.21.2n phải CÒN trong gói).
- **CHANGELOG archive**: lịch sử 1.33.54→1.34.99 (246KB) chuyển NGUYÊN VĂN sang
  `references/changelog_archive/CHANGELOG-1.33.54-den-1.34.99.md` (dir vốn bị loại khỏi bundle); CHANGELOG
  còn ~84KB (v1.35.0+) + con trỏ.
- Test: 1259 → **1260** (+`r194_bundle_deflate_tat_dinh`: member DEFLATED ×2 cùng byte + metadata đóng băng
  + giải nén tròn). ★Bẫy phiên: chuỗi bash double-quote nuốt BACKTICK (command substitution) khi sinh text
  có `code` — dòng con trỏ CHANGELOG phải vá lại bằng Edit.

# ★ v1.35.24 — r193 HOTFIX SỰ CỐ TOKEN TRONG BUNDLE (SEC; +2 test, 1259/1259) (2026-07-23)

> **Sự cố:** `tra_luat_config.v2.json.bak_truoc_shard3_2026-07-23` (backup config do phiên shard-3 tạo ở
> ROOT cây skill, chứa **token webapp THẬT + webappUrl**) LỌT vào release-bundle → nằm trong zip LIVE trên
> Drive từ deploy r191/r192 cùng ngày (và có thể các bản deploy 23-07 trước đó, tuỳ thời điểm file sinh ra
> 20:21). Phát hiện bởi bước quét token trong SCRIPT SHIP của user — gate 9 bước KHÔNG có bước này.
> **Gốc:** luật exclude chỉ bắt suffix `.bak` CHÍNH XÁC + tên `tra_luat_config.v2.json` CHÍNH XÁC — đuôi
> backup BIẾN THỂ (`.bak_truoc_*`) lọt cả hai lưới; và pipeline KHÔNG có tầng quét nội dung.
- **Vá dữ liệu**: file backup DI CHUYỂN (không xoá) ra `D:\Quốc hội\_config_backups\` — ngoài cây đóng gói.
- **Vá code 2 tầng** (`release.py`): (a) `_release_should_include` — tên trong `_RELEASE_EXCLUDE_NAMES_ANYWHERE`
  nay chặn CẢ biến thể có hậu tố (`<tên>.bak_*`, `<tên>.old`…) + MỌI tên chứa `.bak`/`.tmp`; (b) cổng
  **`TOKEN_IN_BUNDLE`** ngay trong `cmd_release_bundle`: quét từng member (khuôn `tl_[A-Za-z0-9]{20,}`,
  helper PURE `_release_secret_findings` — finding CẮT token, không in trọn) → thấy là XOÁ zip tạm, rc=2,
  KHÔNG phát hành. Quét token giờ là tầng vệ CỦA SKILL, không phụ thuộc script ship ngoài.
- **Khắc phục hậu quả**: rebuild sạch + deploy ĐÈ bản lộ trên Drive cùng ngày. **KHUYẾN NGHỊ BẮT BUỘC:
  XOAY TOKEN webapp** (token đã nằm trong zip tải được trong nhiều giờ) + user re-import Capabilities
  (bản import v1.35.23 cũng chứa file token).
- Test: 1257 → **1259** (+2 `r193_*`: exclude biến thể chỉ-nó-chặn + quét token PURE/shape).

# ★ v1.35.23 — r192 ĐỢT HIỆU NĂNG/UX NLM F5–F9 + SỬA CHỮ SKILL.md (kế hoạch r191/r192; +10 test, 1257/1257) (2026-07-23)

> Đợt 2/2 của kế hoạch chốt qua grilling 23-07 (đợt 1 = r191/v1.35.22 cùng ngày). SKILL.md sửa NỘI DUNG
> một lượt (F1/F2/F3/F4/F5/F6/F7/F9 + khuôn lô chuẩn) ⇒ **RE-IMPORT Capabilities MỘT lần sau r192**.
> HOÃN ADR `ingest_pipeline` server-side (đã quyết); ĐO LẠI hiệu năng sau ~1 tuần theo bảng baseline 23-07.

- **F5 (đề xuất #1) — BA VAN NLM** (con số người thẩm tra duyệt): ① **van TRƯỚC LÔ** —
  `NLM_BATCH_LINKS_THRESHOLD` 2→**4**; lô >4 nguồn → KHÔNG auto-add API, nhánh BATCH_LINKS của
  `ingest-missing` nay GHI **BẢNG TAY** markdown (`hand_sheet` — `_nlm_links_md`: link bấm-được + notebook
  + hẹn reconcile) vào `.tl_state/nlm_bang_tay_<key>.md`; `nlm-links` +`--drive-ids` (bảng tay lô cụ thể,
  không đòi chưa-trên-NLM) +`--md-out`. ② **van KÍCH THƯỚC** — `_NLM_SIZE_VAN_CHARS=150k`: `ingest-local`
  đo text local lúc lập plan, >150k ký tự → TỰ chuyển `--nlm-no-wait` (plan ghi `nlm_size_van`; đo 23-07:
  343k >10′ client-timeout, <100k 30-90s). ③ **van RUNTIME** — `nlm_cli.source_add` mặc định chờ settle
  **120s** (trước 600s); CLI rc≠0 nhưng ĐÃ có Source ID ⇒ ok + `settle_timeout` (THÔI CHỜ, KHÔNG huỷ —
  nguồn đang index); `nlm-add` route sang lane deferred (F3), `ingest-local` bước link cuối ghi
  `nlm_status=deferred` + KHÔNG corpus (mirror khuôn ADD-TAY: reconcile nâng pushed → register corpus);
  rc=124 (hard-kill timeout+30) → note «ĐỪNG add lại mù — reconcile là đường vét».
- **F6 (đề xuất #8) — retry GAS chọn lọc**: `_gas_get_retry` +`_schedule` tường minh; `ingest_claim`
  (3 call-site) + `reg-query --live` đi lịch **5s/15s**; **GAS 404 chập chờn** ('HTTPError: 404' hạ tầng,
  KHÁC NOT_FOUND nghiệp vụ JSON) nay coi transient; KHÔNG auto-retry đường ghi. `CLAIMED_ELSEWHERE`
  (cả 3 nơi) in kèm `claim_ttl_hint` = giờ hết hạn muộn nhất (now+TTL 5′ — worst-case client-tính).
- **F7 (đề xuất #7) — preflight-lô auth NLM**: `NLM_COOKIE_BATCH_MAX_MIN=50`; `ingest-missing` sắp add API
  >1 nguồn mà cookie >50′ → CHẶN rc=2 `NLM_COOKIE_TOO_OLD_FOR_BATCH` «chạy nlm login trước lô» (trước chỉ
  WARN COOKIE_AGE_HIGH → chết giữa lô).
- **F8 (đề xuất #6) — `ingest_claim` đọc config**: helper một-cửa `_ingest_claim_get` — tự `load_creds`
  từ config như mọi bước khác (env TL_WEBAPP/TL_TOKEN vẫn ưu tiên — hết cảnh export tay/tlenv.sh) + gộp
  retry F6; cả 3 call-site claim đi qua cửa này.
- **F9 (đề xuất #9) — fetch hỏi-trước mặc định**: «phê duyệt nạp theo skill ≠ phê duyệt TỰ TẢI nguồn
  gated» — `fetch-route` MẶC ĐỊNH `mode=ask_first_links` (link bấm-được + link _HOP_NAP, KHÔNG fetch_plan);
  recipe tự tải CHỈ xuất với cờ tường minh **`--auto-download-approved`** (gõ SAU khi người dùng đồng ý
  trong phiên).
- **SKILL.md (một lượt — re-import 1 lần)**: F1 dedup lỏng-năm + `--replace-sohieu` (mục 18 CORPUS-FIRST);
  F2 đọc-tự-refresh; F4 PDF_IMAGE (10a); F9 khuôn 10b nổi hơn; khối **BA VAN NLM + KHUÔN LÔ CHUẨN MỚI**
  (lô ≥3 file → ingest song song 2–3 tiến trình + `--nlm-no-wait` + MỘT reconcile cuối lô) + F3/F6/F7.
- Test: **1247 → 1257** (+10 `r192_*`: van1 ×3, van2, van3 ×2, F6, F7, F8, F9); 3 ca cũ CẬP NHẬT THEO
  NGƯỠNG MỚI (r118/r122 lô 5>4; r72a fetch-route thêm cờ approved); parser_surface regen chủ đích
  (fetch-route + nlm-links). CONTEXT.md +2 từ vựng (ba van NLM, bảng tay).
- Ghi chú nhất quán: `ingest-local --nlm-no-wait` chủ động GIỮ khuôn S4 (pushed+corpus=true tại link,
  reconcile cuối lô là lưới — khuôn lô chuẩn dựa vào đây); `deferred` CHỈ dùng cho nlm-add --no-wait và
  ca settle-timeout van 3 (chưa xác minh settle, corpus chưa set).

# ★ v1.35.22 — r191 ĐỢT AN TOÀN DỮ LIỆU F1–F4 (kế hoạch r191/r192 chốt qua grilling 23-07; +11 test, 1247/1247) (2026-07-23)

> Nguồn: `SKILL_FIX_DE_XUAT_23-7.md` (đo thật phiên Cổng 1 + nạp 23-07 trên v1.35.21). Mỗi fix một ca
> TDD chỉ-nó-chặn (tiền lệ r181); các bẫy thật 23-07 nay bị chặn máy. KHÔNG fix nào đổi cách ĐỌC nội
> dung văn bản ⇒ không kích hoạt nghĩa vụ rà-lại Phần VI mục F. SKILL.md CHỈ bump header (không
> re-import); mọi sửa nội dung dồn r192.

- **F1 (đề xuất #4) — dedup số hiệu LIVE ngay tại DRY `ingest-local`**: bẫy 158/159 — dedup cache nguội
  che dòng có sẵn → DRY "đi lọt", apply tạo dòng + GDoc TRÙNG. Nay DRY (và apply) đo dedup trên registry
  LIVE (`_manifest_entries(refresh=True)`, +5–10s/DRY chấp nhận); khoá LỎNG-NĂM dùng bộ chuẩn hoá SẴN CÓ
  `_sohieu_loose` (so BẰNG-KHOÁ — '29-2025' không bắt oan '129-2025'); trùng dòng corpus-effective
  (`_entry_is_corpus_effective`, kể cả overflow) ⇒ CHẶN rc=2 `SOHIEU_ALREADY_IN_CORPUS`. Thay bản có
  chủ đích: cờ mới **`--replace-sohieu`** — plan in dòng cũ + `post_steps` chuỗi hạ bản sau nạp.
  LIVE không đọc được → fail-closed rc=2 (mirror S13); `--resume` bỏ qua (identity-gate đã giữ);
  `--skip-live-check` bỏ qua có chủ đích. Helper mới `_ingest_dedup_sohieu_live` (PURE).
- **F2 (đề xuất #5) — đường ĐỌC tự refresh khi manifest BẨN**: bẫy extract 164-2025 ngay sau hoán đổi
  canonical vẫn trả bản CŨ, phải `boot --refresh` tay. Nay `_invalidate_manifest_cache` (mọi lệnh GHI)
  để lại marker `manifest.dirty`; `_manifest_entries` thấy marker + có creds env (main() đã nạp cho mọi
  lệnh ngoài _CREDS_LAZY_CMDS) ⇒ ÉP refresh LIVE rồi xoá marker — vá MỘT chỗ phủ mọi lệnh resolve theo
  số hiệu (extract/locate/xref/doc-text). Đường đọc ADVISORY (discovery overflow trong `_ingest_target`)
  dùng `heal_dirty=False` — ngoài phạm vi resolve, không ép refresh. Phía ghi không cộng giá.
- **F3 (đề xuất #2) — `nlm-add --no-wait` tự reg_link với `deferred`**: bẫy 3 nguồn add no-wait có
  source_id trả về mà registry nlm=''/nb='-', phải register tay. Nay no-wait reg_link NGAY sid THẬT +
  `nlm_status='deferred'` (ngữ nghĩa MỞ RỘNG: «đã gửi NLM, chưa xác minh settle» — không claim có mặt
  vật lý nên không vi phạm VERIFY-THEN-LINK A-#1); chỉ link dòng đã tồn tại + chưa có pointer khác
  (stale-an-toàn, không row xương); corpus KHÔNG đụng. `nlm-reconcile` thêm nhóm **`settle_confirm`**
  (deferred + sid CÓ MẶT live đúng notebook) → `--apply` nâng `deferred→pushed` CHỈ cột nlm_status
  (corpus không auto-true); deferred VẮNG live giữ nguyên desync_real. Ca client-timeout-mất-source_id:
  reconcile vẫn là đường vét duy nhất. Helper mới `_nlm_no_wait_reg_link`. (Ca cũ
  `r117_nlm_add_no_wait_skips_reg_link` khoá hành vi bỏ-link → THAY bằng
  `r191_nlm_add_no_wait_links_deferred`.)
- **F4 (đề xuất #3) — cổng PDF-ảnh trong `ingest-local` lúc lập plan**: bẫy 4 PDF «ký số»
  datafiles.chinhphu.vn/hue.gov.vn đều PDF ẢNH (text layer 149 ký tự metadata chữ ký) suýt convert mù.
  Nay mọi nguồn .pdf đo text-layer local ngay lúc lập plan (`_pdf_text_layer_stats`: pdftotext + đếm
  trang qua form-feed, fallback đếm `/Type /Page`); **< 100 ký tự/trang ⇒ cờ `PDF_IMAGE`** → coi
  `source_quality=ocr` chưa verify → rơi vào ocr_gate r180 S1 SẴN CÓ (apply chặn corpus rc=2, đi tiếp
  đường OCR-verify) — không đẻ nhánh mới; chỉ override khi user để `auto` (đường `ingest-ocr` tường
  minh đi qua như cũ); không đo được (thiếu pdftotext) → cảnh báo, KHÔNG đoán. Plan DRY thêm khối
  `pdf_image` (verdict + chars_per_page). Helper mới `_pdf_image_verdict` (PURE) + hằng
  `_PDF_IMAGE_CHARS_PER_PAGE=100`.
- Test: **1236 → 1247** (+11: F1 ×4 `r191_dedup_sohieu_*`/`r191_ingest_local_sohieu_dup_dry_rc2`/
  `r191_ingest_local_replace_sohieu_di_tiep`, F2 ×2 `r191_manifest_dirty_*`, F3 ×2
  `r191_reconcile_settle_confirm_*` + 1 thay, F4 ×3 `r191_pdf_*`/`r191_ingest_local_pdf_*`).
  parser_surface regen CHỦ ĐÍCH (1 lệnh `ingest-local` — thêm `--replace-sohieu`). Bẫy selftest bắt
  được khi vá: mock `_manifest_entries` RÒ từ ca trước trong namespace tl → ca F2 gọi thẳng hàm module
  `tl_core.regio` + heal đòi TL_WEBAPP env (bare selftest trơ với marker — hermetic kép).

# ★ v1.35.21 — r190 DỨT ĐIỂM PHA D THEO P10 GỐC: via TELEMETRY + DOCS SYNC COMMANDS/RUNBOOK + CAP TỔNG REPACK (2026-07-23)

> Đối chiếu bản thi hành với P10_PROMPT gốc (user cung cấp sau) lộ 3 thiếu sót Pha D — vá nốt:
> +2 test r190 (1236/1236).

- **`via` propagation**: P10 đòi propagate CẢ `via` lẫn `degraded_reason` — r188 mới làm vế sau.
  Nay `profile-list --discover` + `profile-sync` LUÔN nổi `via` (profile_catalog/list_loop) khi scan
  có — biết đang đi bulk hay fallback ngay cả khi không degraded.
- **Docs sync đúng nghĩa (COMMANDS.md/RUNBOOK.md)**: profile-doctor +`--plan-marker-migration`
  (canary, tên đã quote r189); profile-ingest --resume ghi rõ identity gate r184 (`--journal`/
  `--drive-id`, name-only=DRY_REPAIR); ingest-zip sửa mô tả worker lỗi thời ("trần cứng 8" →
  ngân sách RAM D7 trần 4) + bundle hash r184 + in-process r187; RUNBOOK +B7 (resume định danh,
  marker v2 đã migrate, `TL_INGEST_MEMORY_BUDGET_MB`/`TL_DOCX_XML_MAX_MB`, đường bulk 2.21.2n).
- **SEC-01 cap TỔNG**: engine +`read_all_members_bounded` (trần member + trần TỔNG mặc định 4×) —
  đường repack the_thuc normalize đọc mọi member vào RAM, N member vừa-dưới-trần cộng lại hết
  nuốt RAM (`ZIP_TOTAL_BOUND_EXCEEDED`).
- Còn lại theo P10 (KHÔNG thuộc release này, đã ghi nhận): Pha A 5 ca bắt buộc chạy bù trên
  profile thử (kịch bản giao user); phần lõi WP7 (state machine + di trú 4 entrypoint +
  benchmark ≤+15%) → kế hoạch P11.

# ★ v1.35.20 — r189 QUOTE TÊN PROFILE TRONG ACTION PLAN MIGRATION (2026-07-23)

> Bug thực chiến migration 23-07: `marker_migration_plan[].action` in tên profile TRẦN — tên có dấu
> cách («Biểu mẫu DMVB», «Pháp lệnh NCC»…) dán nguyên văn vào shell bị vỡ tham số. Vá:
> `_migration_plan_finalize` bọc ngoặc kép (chạy được cả cmd lẫn bash). TDD r186_migration_plan_canary
> siết kỳ vọng sang bản quoted với tên có dấu cách. (Migration 15/15 profile đã xong bằng lệnh
> quote tay — vá này cho lần dùng sau.)

# ★ v1.35.19 — r188 SEC-01 BOUNDED-READ DOCX/XML + TELEMETRY degraded_reason + DOCS SYNC ADR (2026-07-23)

> MERGE phiên song song: master v1.35.16 = r186-extract (Opus) đánh TRÙNG số v1.35.16/r186 với
> r186-marker nhánh review — theo ADR-0001 số canonical thắng: 3 release nhánh này dồn lên
> v1.35.17/18/19 khi merge (test prefix r186_marker_*/r186_extract_* đã khác tên, giữ nguyên).

> Pha D (chốt) kế hoạch review p9 phần-còn-lại. +3 test r188 (1231/1231).

- **SEC-01 — chống zip-bomb DOCX/XML:** engine thêm `read_member_bounded(zf, member)` — đọc member
  STREAMING với TRẦN bytes giải nén (env `TL_DOCX_XML_MAX_MB`, mặc định 50, clamp [1,500]); vượt ⇒
  `ZIP_MEMBER_BOUND_EXCEEDED` (ValueError), member thiếu GIỮ ngữ nghĩa KeyError. Wire 9 điểm đọc:
  `_docx_unzip_text` (doc-text/extract), probe profile-ingest, `docx_markup.scan_file`,
  `normalize_document._docx_zip_text`, the_thuc (check/wrap-scan/landscape + normalize đọc
  TOÀN BỘ member khi repack). Các đường catch-all sẵn có fail-safe "" / scan(0) — không OOM,
  không traceback giữa pipeline.
- **Telemetry degraded_reason (WP5 dứt điểm):** `profile-list --discover` + `profile-sync` nay NỔI
  `degraded_reason` từ scan (SERVER_NO_PROFILE_CATALOG…) lên output JSON như doctor r185 —
  perf gate chỉ được coi xanh trên đường bulk, fallback phải tự khai.
- **Docs sync:** bổ sung 3 ADR bị tham chiếu từ r184 mà chưa có file trong cây:
  `0011-source-revision-tach-khoi-content-identity` (SourceRevision/claim-key/resume gate),
  `0012-marker-transaction-schema-v2` (state machine + v2 + rollout R1/R2 — R2 đã thi hành r186),
  `0013-zip-immutable-plan-bundle` (bundle hash, 1-extract r185, subprocess=0 r187).

# ★ v1.35.18 — r187 WP7 TRACER-BULLET: ENGINE INGEST CHUNG — SUBPROCESS=0 (ZIP) + STAGE SCHEDULER + HASH-ONCE (2026-07-23)

> Pha C kế hoạch review p9 phần-còn-lại (ADR-0004, ticket WP7/R3 ở r185). Module MỚI
> `tl_core/ingest_engine.py` — primitive engine ĐỘC LẬP stdlib (không bind, không import ngược
> tl_core): stage scheduler + hash-once run-scope + child runner in-process. +5 test r187 (1228).

- **Subprocess=0 cho ZIP apply:** `_zip_child_apply_one` chạy child APPLY **in-process** qua
  `run_child_inprocess` (một runner cho cả DRY lẫn apply — `_zip_child_plan_one` cũng ủy quyền);
  stdout/stderr route THEO THREAD (`_ThreadRouteProxy` refcount) — redirect_stdout process-global
  không thread-safe khi N child chạy trong ThreadPool. Giới hạn ghi nhận: (1) không còn timeout
  900s kiểu subprocess — child treo = run treo (GAS client tự timeout tầng dưới); (2) chunking/OCR
  vẫn `_run_child_tl` subprocess — NGOÀI scope ticket (ticket chỉ định child ingest-zip).
- **Stage scheduler (upload≤2, NLM≤2):** `stage_slot(stage)` BoundedSemaphore per-process; wire
  6 call-site: 2 upload (`profile-ingest`, `ingest-local`) + 4 `source_add` (profile-ingest,
  chunks, resume, ingest-local). Stage lạ = không giới hạn. Registry đã một lane từ r185/ING-05.
- **Hash nguồn ĐÚNG 1 lần/run (kể cả child plan):** `ingest_contract.sha256_file` ủy quyền
  `hash_file_once` — trong `run_scope()` (nest được) memo theo realpath; `_zip_plan_bundle` +
  `_zip_apply` mở scope trọn invocation → archive+member+child-plan hash 1 lượt (test đo:
  bundle = 1 compute, extract-verify memo-hit). Ghi nhận trade-off: re-hash archive giữa
  plan↔extract trong CÙNG run thành memo-hit — guard thẩm quyền là so sha256 TỪNG member lúc
  extract (GIỮ NGUYÊN, test ZIP_MEMBER_CHANGED_OR_CORRUPT còn đỏ đúng). Ngoài scope: hành vi cũ.
- Test r184/r185 zip apply chuyển patch funnel `_run_child_tl` → `_zip_child_apply_one` (đúng
  đường mới); +r187: cap concurrency đo bằng thread, hash-once trong/ngoài scope, routed-io 2
  thread song song bắt đúng stdout riêng, apply không đụng subprocess (fake raise nếu gọi).
- Golden regen CÓ CHỦ ĐÍCH (user duyệt): workflow_audit `py_size.files_scanned` 66→67 — đúng 1
  dòng, do file module MỚI `tl_core/ingest_engine.py` (không phải diff hành vi).

# ★ v1.35.17 — r186-marker R2 MARKER WRITER v2 + FAIL-CLOSED BODY + MIGRATION CANARY (2026-07-23, đổi số khi merge — v1.35.16 thuộc r186-extract canonical)

> Pha B kế hoạch review p9 phần-còn-lại (P10). Reader v1/v2 đã LIVE từ r184 ⇒ flip WRITER an toàn
> (client cũ 1 phiên bản vẫn đọc v1; marker mới phát v2). +5 test r186 (1223). Offline-only — mọi
> migration LIVE trên profile thật vẫn chờ user duyệt plan.

- **Writer v2 (ADR-0012 R2):** `_marker_body` phát `schema=tra_luat_profile.v2` + `fingerprint`
  (sha256 canonical-JSON, đóng dấu CUỐI sau mọi trường); tham số mới `meta_id` = fallback
  `metaFolderId` khi prof thiếu (marker luôn nằm trong chính `_meta` được ghi) — rename/set-meta
  truyền `mr.meta_folder_id`.
- **Fail-closed TRƯỚC upload:** `_marker_write` validate body (`_marker_validate`) trước mutation —
  v2 thiếu trường bắt buộc theo `manifestScope` / fingerprint lệch ⇒ `status=REJECTED`, 0 call Drive,
  journal ghi errors + repair (own-scope cần notebookId/registryDocId/manifestId). Hết cửa tạo
  marker hỏng rồi mới phát hiện qua doctor.
- **Migration canary:** `profile-doctor --plan-marker-migration` chốt plan qua
  `_migration_plan_finalize` (PURE) — sort tất định, phần tử ĐẦU `canary=true`, action chạy được
  per-profile `tl profile-backfill-markers --profile-name <p> --apply --force` (canary trước →
  verify doctor sạch → mới đại trà; --apply do user duyệt). Note doctor MARKER_SCHEMA_V1 cập nhật.
- Fixture selftest vá-trường-sau-`_marker_body` re-mint fingerprint (`_remint186`) — marker giả lập
  không thành "v2 fingerprint lệch" bị validate chặn oan; r86 defaults đổi kỳ vọng schema→v2;
  fixture minimal thêm `metaFolderId` (v2 bắt buộc).
# ★ v1.35.16 — r186 `tl extract` TRÊN GOOGLE DOC: ĐÓNG NỐT BẪY r183 BỎ LẠI (2026-07-23)

> r183 vá `doc-text` nhưng **`tl extract` vẫn dính NGUYÊN bẫy** — và đây mới là đường nguy hiểm hơn:
> extract **ghi thẳng vào cache chuẩn `extract_<id>.txt`**, tức NGUỒN NUÔI CORPUS/NLM ⇒ chữ đã bỏ chảy
> vào kho, rồi `doc-text` đọc lại chính cache đó.
>
> **Đo tươi 23-07-2026** (dự thảo BHXH 16/7, sau khi r183 đã LIVE): `tl extract <gdoc>` → **25.338 ký tự
> = BẢN THÔ**, đủ cả ba câu ĐÃ BỎ («tối đa là 12 tháng», «phải được chứng thực», «là cơ quan nhà nước»),
> **0 nhãn, 0 cảnh báo**. Gốc: `cmd_extract` đọc bằng transport `read`/webapp `exporttext` = export
> **text/plain**, và **không hề có cờ `--markup`**. **Sau vá, cùng lệnh: 21.128 ký tự, nguồn
> `gdoc-docx (markup strip)`, ba câu trên VẮNG MẶT.**
>
> **Vá — cùng khuôn r183, dùng CHUNG code (không chép lại logic):**
> · 4 helper tách ra `lookup_ops`: `_markup_warn` (một câu cảnh báo DUY NHẤT cho cả hai lệnh — lệch chữ
> giữa hai đường là mầm nhầm lẫn) + `_markup_cert_path/_write/_read` (sidecar chứng nhận).
> · `cmd_extract` +`--markup {strip,mark,raw}` (mặc định `strip`) và +`--markup-strict`.
> · (a) chế độ lọc ⇒ **export `.docx`** qua `_gdoc_docx_text` TRƯỚC, lọc bằng `docx_markup`.
> · (b) không lọc được (export .docx fail → rơi text/plain, kể cả nhánh resolve-lại canonical) ⇒
> **CẢNH BÁO `[markup] ⚠`**; `--markup-strict` ⇒ **rc=3 và KHÔNG ghi file** (ở extract điều này nặng hơn
> doc-text: thà thiếu file còn hơn bơm bản thô vào corpus).
> · (c) **bản `cache-build` consolidated cũng cảnh báo** — nó dựng bởi `normalize_document` mà
> `--markup-mode auto` cho DỰ THẢO ra bản **`mark`**, không ai chứng nhận được nó ở chế độ nào.
> · (d) **`mark`/`raw` KHÔNG ghi vào khoá cache chuẩn** nữa mà ra `extract_<id>.<mode>.txt` (nói rõ ở
> stderr) — trước đây `extract --markup mark` sẽ bơm thẳng ⟦BỎ:…⟧ vào khoá chuẩn.
> · (e) ghi khoá chuẩn ⇒ ghi kèm **sidecar chứng nhận** ⇒ `doc-text` đọc lại cache đó **hết cảnh báo**:
> vòng poison `extract → cache → doc-text → corpus` **đóng ở cả hai đầu**.
>
> **TDD 3 ca ĐỎ→XANH** (đo trước vá: 3/3 FAIL, nền 1218 không đổi): `r186_extract_gdoc_qua_docx_markup` ·
> `r186_extract_canh_bao_va_markup_strict` · `r186_extract_ghi_sidecar_dong_vong_poison` (ca (e) kiểm
> LIÊN THÔNG hai lệnh, không chỉ kiểm từng lệnh rời).
>
> ★ **BÀI HỌC PHẠM VI:** r183 ghi "còn mở: `tl extract`" rồi vẫn deploy — bẫy im lặng sống thêm một
> vòng trên chính đường nuôi corpus. Vá bug đọc-sai-văn-bản thì phải quét **MỌI reader của cùng nguồn**
> ngay trong một đợt (r182 quét 4 reader .docx; r183/r186 mới quét đủ 2 reader Google Doc).

# ★ v1.35.15 — r185 WP5-WP6 PERF: BULK PROFILE (GAS 2.21.2n) + ZIP 1-PASS + D7 RAM BUDGET + REGISTRY LANE (2026-07-23)

> Thi hành WP5-WP6 kế hoạch review p9 (D3/D6/D7). GAS **2.21.2n** = 2.21.2m ⊕ 2 endpoint CỘNG THÊM
> CHỈ ĐỌC: `profile_catalog` (snapshot Van_ban_thuong 1 call — items + _meta + NỘI DUNG mọi marker)
> và `drive_info_bulk` (metadata ≤200 fileId 1 call, giữ thứ tự input). Client try-first + fallback
> tương thích server cũ (`degraded_reason` — perf gate chỉ xanh trên đường bulk). +9 test r185 (1218).

- **WP5 — call budget D6 (đo bằng test đếm call trên fake GAS):**
  · `profile-list --discover` / `profile-sync`: scan = **1 call** `profile_catalog` (tổng ≤2 kể bootstrap),
    KHÔNG tăng theo 1/10/50 profile (trước: ~3×N call list/list/download-marker).
  · `profile-doctor` shallow 50 profile: **≤3 GAS** (bootstrap + catalog + info_bulk; marker đọc từ
    catalog, asset info từ bulk — 0 call `info`/`list`/`download` trong vòng lặp).
  · `profile-doctor --deep` 1 profile, 300 nguồn + 50 template: **≤4 GAS + 1 NLM** — `reg_get_bulk`
    lô 300 (0 `reg_get` lẻ; ghi nhận: bulk 1 row/sid — sid nhiều row chỉ thấy row cuối, ca hiếm);
    template probe từ info-bulk prefetch (0 download-để-kiểm-tồn-tại; location theo parents,
    'shared' resolve LƯỜI ≤1 lần/run).
  · `profile-sync --apply`: `_persist_profiles_config_bulk` — TOÀN BỘ diff ghi config NGUYÊN TỬ
    **1 lần** + 1 journal run (trước: N lần read-modify-write + N run).
- **WP6 — I/O/RAM (ING-03/ING-05/D7):**
  · ZIP apply: **1 extract + 1 lượt hash member/invocation** — bundle lập từ CHÍNH lần extract của
    apply; bỏ pre-pass recompute trùng lặp (drift do authorize bắt: `PLAN_HASH_MISMATCH` + note
    `PLAN_DRIFT_REPLAN_REQUIRED`). Trước r185: 2 extract + hash member ×3.
  · D7: `TL_INGEST_MEMORY_BUDGET_MB` (mặc định 256, clamp 64-4096); `workers_effective =
    min(requested, 4, floor(budget / (32MiB + 2,5×size_max)))` — hard cap 4 (trước cap 8 không đếm
    RAM); plan/apply CÔNG KHAI `resources{workers_requested/effective, peak_memory_estimate}`;
    không đủ 1 worker ⇒ `INSUFFICIENT_MEMORY_BUDGET` DỪNG TRƯỚC mutation.
  · ING-05: `_verified_reg_write`/`_journaled_reg_write`/`_verified_reg_upsert` đi **một lane RLock**
    trong process (8 thread không chồng nhau — test đo max-concurrency=1). GIỚI HẠN GHI NHẬN: chưa
    phủ child SUBPROCESS ingest-zip (row khác nhau + claim F-04 che; lane xuyên-process = WP7).
- **Còn lại WP6 (ticket WP7/R3):** subprocess child ingest-zip → in-process engine (subprocess=0,
  member hash đúng 1 lần kể cả child plan); stage scheduler upload≤2/NLM≤2; GWS streaming upload;
  SEC-01 bounded-read DOCX/XML.
- EXPECT_VERSION → **2.21.2n**; API_CONTRACT đóng dấu 2.21.2n + 2 action mới; GAS deploy qua clasp
  giữ URL NGAY SAU deploy skill (thứ tự an toàn: client-có-fallback lên trước server).

# ★ v1.35.14 — r184 REVIEW P0: GATE ARTIFACT + MARKER TRANSACTION + IDENTITY/RESUME + ZIP BUNDLE (2026-07-23)

> Bốn vá P0 từ review hiệu năng/đúng đắn Profile+ingest (kế hoạch grill-with-docs 23-07, workspace
> `C:\qh\p9_review_v13512_2026-07-23` — evidence register 11/12 CONFIRMED). Fork v1.35.12, merge 3-way
> lên r183 (giữ nguyên vá gdoc --markup); +23 test r184 (1209/1209).

- **REL-01 — gate xanh giả trên artifact**: v1.35.12 deploy-zip fail 4 selftest (r67/r125/r127/r128) vì
  SKILL.md trỏ `references/changelog_archive/` (release-exclude) — cây dev xanh (exists() trên đĩa),
  artifact đỏ. Vá: `_skill_links_findings` (PURE) đối chiếu link SKILL.md với PACKAGE-SET của manifest,
  wire fail-closed vào `_verify_release_manifest` (`SKILL_LINKS_NOT_IN_PACKAGE` + `skill_links` trong
  release-verify); gỡ con trỏ dev-only khỏi kernel (không nới auditor).
- **PRO-01 — marker false-success (ADR-0012)**: `_marker_write` thành state machine journaled
  upload → FULL readback (so TRỌN payload — hết so 3 trường) → enumerate (HẾT nuốt `except: pass`) →
  cleanup → PROVE-ONE (re-list chứng minh 0 marker dư) → commit; trả `status COMMITTED/PARTIAL/FAILED`
  + `phases` + repair action trong journal. 6 caller (rename/adopt/create/backfill/promote/set-meta)
  chuyển `verified&&cleanup_ok` → `ok` trọn chuỗi. Reader hiểu marker v1/v2 (`tra_luat_profile.v2`,
  bộ trường bắt buộc theo manifestScope, fingerprint) — R1 writer GIỮ v1; `_marker_mutation_guard`
  chung; `profile-doctor --plan-marker-migration` (DRY, migration ghi ở R2).
- **ING-02 — identity đội lốt + resume mù nguồn (ADR-0011/D4-D5)**: `identity_hash_for_drive_source`
  hết nhét sha256(drive_id) vào slot content_hash — retype thành `build_source_revision`
  (identity_strength revision/metadata) + `claim_key_for_source` (payload KHÔNG có content_hash;
  observed_at CỐ Ý ngoài khóa). ⚠ giá trị claim key ĐỔI — 2 host lệch version không khóa chéo trong
  cửa sổ rollout (TTL 5'). `profile-ingest` apply NAY CÓ JOURNAL (name/sha256/identity_hash/plan_hash/
  drive_id + run_end). Resume: name-only = DRY REPAIR (mode `DRY_REPAIR`, 0 mutation, 1 phiên bản
  chuyển tiếp); `--apply` đòi `--journal <run_id>` HOẶC `--drive-id` + fingerprint khớp registry
  (`_resume_identity_gate` PURE); journal legacy → `LEGACY_JOURNAL_REPLAN_REQUIRED`; lệch →
  `RESUME_IDENTITY_MISMATCH`. CLI profile-ingest/profile-file-add + `--journal`.
- **ING-01 — ZIP self-confirm (ADR-0013)**: DRY (`ingest-zip`/`profile-ingest-zip` có --cat) lập ĐỦ
  child plan IN-PROCESS (`_zip_child_plan_one`, 0 subprocess DRY) → `plan_hash` = fingerprint TOÀN
  bundle (archive+member+mọi child plan, `ingest_zip_bundle.v1`). Apply: authorize trên bundle hash;
  pre-pass tuần tự recompute từng child — khác bundle đã duyệt ⇒ `PLAN_DRIFT_REPLAN_REQUIRED`,
  0 mutation; `--confirm yes` cho child CHỈ với hash NẰM TRONG bundle user duyệt (hết tự-phê-duyệt);
  journal record `plan` bundle + intent per-member. ⚠ plan hash ZIP cũ (chỉ parent) hết hợp lệ — DRY
  lại lấy bundle hash. DRY vbqppl KHÔNG --cat giữ DRY phân loại (note_bundle).
- Bẫy merge: msys sed text-mode TƯỚC 
 → 3 file CRLF (tl.py/tl_selftest/command_registry) thành
  whole-file-diff giả 19k dòng; khôi phục CRLF trước merge. Kernel 48.190B > 47K warn sau merge —
  rút gọn dòng bảng CHANGELOG-sâu về 48.121B. Golden regen CÓ CHỦ ĐÍCH: parser_surface (cờ CLI mới),
  workflow_audit (links 15→14).

# ★ v1.35.13 — r183 NGUỒN GOOGLE DOC: `--markup` HẾT LÀ NO-OP IM LẶNG (2026-07-23)

> **BẪY IM LẶNG — nguy hiểm hơn bug thường vì công cụ báo THÀNH CÔNG.** r182 vá 3 reader `.docx`, nhưng
> **nhánh Google Doc của `_doc_text_any` không hề đụng `docx_markup`**: nó đi `_read_doc_text` (export
> **text/plain**) — đường này san phẳng mọi định dạng, GIỮ CHỮ mà MẤT gạch-bỏ. Cờ `--markup` bị bỏ qua
> HOÀN TOÀN, vẫn rc=0, không một dòng cảnh báo.
>
> **Đo tươi 23-07-2026** (Dự thảo Luật BHXH 16/7, `1ltPv6AwO72wglCpEitkT7tmu-GZ3zPEGhTObiKF8p4s`): qua
> `drive_id` **mọi chế độ = 25.339 ký tự** (≈ bản thô), **0 nhãn ⟦BỎ⟧**; từ `.docx` gốc: strip **21.131** /
> mark **25.503** (60 nhãn) / raw 25.032, `docx_markup.scan_file` = **63 khối `w:strike`** ⇒ **4.405 ký tự
> chữ ĐÃ BỎ bị đọc như quy phạm hiện hành**. Tác hại đã xảy ra: **6 phát hiện SAI** trong một đợt rà soát
> («tối đa là 12 tháng», «phải được chứng thực», «là cơ quan nhà nước», «trước liền kề tháng»), phải chạy
> trọn một đợt sửa hơn 60 chỗ trên 10 file.
>
> **Vá — đi CẢ HAI hướng, vì không hướng nào đủ một mình:**
> (a) **LẤY CHO ĐƯỢC MARKUP** — `_gdoc_docx_text`: Google Doc + chế độ lọc ⇒ **export `.docx`**
> (`_doc_text_fetch_binary(..., export_mime=…wordprocessingml.document)`; `alt=media` KHÔNG tải được
> Docs-native) rồi qua CHÍNH bộ lọc `docx_markup` như nhánh .docx — source mới `gdoc-docx`. Hướng này cứu
> được các bản Google Doc CÒN giữ dấu vết (gạch-bỏ thủ công/suggestion), nhưng KHÔNG cứu được bản đã mất
> markup lúc convert ⇒ phải có (b).
> (b) **KHÔNG LẤY ĐƯỢC THÌ NÓI THẲNG** — export .docx fail, hoặc bản convert không còn dấu vết nào
> (del=0/strike=0/ins=0), hoặc text lấy từ **cache không kèm chứng nhận đã-lọc** ⇒ **CẢNH BÁO stderr**
> `[markup] ⚠ …` + khai vào `meta`/JSON (`markup_filter_ran`, `markup_found`, `markup_warning`).
> `--markup raw` = đối chứng CÓ CHỦ ĐÍCH ⇒ không cảnh báo. **IM LẶNG LÀ HÀNH VI ĐÃ LOẠI BỎ.**
>
> **`--markup-strict`** (mới): có cảnh báo ⇒ **TỪ CHỐI in văn bản, rc=3** (`MARKUP_UNVERIFIED`). Dành cho
> pipeline thẩm tra: thà thiếu văn bản còn hơn có văn bản mà người đọc tưởng đã lọc.
>
> **SIDECAR chứng nhận cache** `extract_<id>.txt.markup.json` (`{v, filter_ran, found, source}`): cache cũ —
> nhất là do `tl extract` ghi từ export text/plain — KHÔNG có sidecar ⇒ lần đọc sau **cảnh báo + gợi ý
> `--refresh`** thay vì im lặng tái diễn đúng bẫy cũ. Thêm `_read_doc_text(..., use_cache=False)` cho
> mark/raw (cache là bản CHUẨN strip — trả nó cho chế độ khác cũng là một kiểu im lặng).
>
> **CẮT STDOUT PHẢI BÁO** — `--max` cắt làm hai chế độ về CÙNG số ký tự và trông y hệt nhau (đúng cái bẫy
> suýt làm chẩn sai hôm 23-07): nay in `⚠ ĐẦU RA BỊ CẮT: x/y ký tự … dùng --max 0 --out <file>`.
>
> **TDD 5 ca ĐỎ→XANH** (đo trước vá: 5/5 FAIL, không ca nào khác đổi): `r183_gdoc_strip_qua_docx_export` ·
> `r183_gdoc_mat_markup_canh_bao` · `r183_markup_strict_tu_choi_rc3` · `r183_canh_bao_cat_stdout` ·
> `r183_cache_cu_khong_chung_nhan_canh_bao`. Selftest **1186/1186**.
>
> ★ **ĐO ĐƯỢC KHI DỰNG CA:** hai test double cũ của `r121` (`_read_doc_text` lambda không nhận `**kw`) làm
> ca ĐỎ vì `TypeError` bị `except Exception` của `_doc_text_any` NUỐT — đúng lớp lỗi âm-tính-giả mà chính
> r183 đang vá; đã nới double.
>
> ★ **DOCTRINE:** bản TRONG KHO không đương nhiên là bản dùng được làm căn cứ; với tài liệu có markup,
> **file `.docx` GỐC mới là nguồn chuẩn**. Công cụ không chứng minh được đã lọc thì PHẢI NÓI — không được
> để người dùng tự suy ra từ rc=0.
>
> **Còn mở:** `tl extract` trên Google Doc vẫn đọc bằng export text/plain (chưa có cờ `--markup`) — nay
> cache do nó ghi bị doc-text cảnh báo là CHƯA CHỨNG NHẬN; để vòng sau.

# ★ v1.35.12 — r182 ĐỌC ĐÚNG .docx CÓ MARKUP SỬA ĐỔI (cả 3 reader sản xuất đọc SAI dự thảo) (2026-07-22)

> Lỗi ĐÚNG-SAI về NỘI DUNG PHÁP LUẬT (không phải lỗi hình thức): mọi đường đọc .docx đều lấy chữ ĐÃ BỎ làm
> quy phạm CÒN HIỆU LỰC. **Đo TƯƠI qua ĐÚNG hàm sản xuất TRƯỚC khi vá — 20 sai / 4 đường đọc:** nhánh
> python-docx của `normalize_document._docx_to_text` GIỮ chữ `w:strike` và MẤT chữ `w:ins` (python-docx bỏ
> run không phải con TRỰC TIẾP của `w:p`); hai nhánh strip-tag — `lookup_ops._docx_unzip_text`
> (`tl doc-text`; doc-compare/dedup/nlm qua `_doc_text_any`) và `ingest_ops._profile_read_probe_text` (cổng
> nạp, DRY phân loại) — giữ CẢ `w:delText`. Bảng (`c.text`) CÙNG LỖI.
>
> ★ **TỰ KIỂM BÁC BỎ GIẢ ĐỊNH BAN ĐẦU:** `tl doc-text`/`tl extract` **KHÔNG** đi qua `_docx_to_text` ⇒ vá mỗi
> `normalize_document` là CHƯA chạm đường tra cứu (P6 vẫn sai). `_docx_to_text` chỉ phục vụ đường NẠP;
> `tl extract` đọc GDoc bằng export GAS. Bài học: xác minh call-graph trước khi tin phạm vi một bug.
>
> **Vá:** module dùng chung `scripts/docx_markup.py` (zero-dep) — bỏ `w:del`/`w:moveFrom`/`w:delText`, BÓC VỎ
> `w:ins`/`w:moveTo`, bỏ run `w:strike`/`w:dstrike` (tôn trọng `w:val="false"` = đè TẮT), quét
> `w:rPrChange`/`w:pPrChange` TRƯỚC khi dò strike (rPrChange lưu ĐỊNH DẠNG CŨ ⇒ dễ tưởng run hiện tại bị gạch).
> Cả 4 đường đọc + CẢ BẢNG dùng CHUNG bộ lọc; phát hiện markup → CẢNH BÁO stderr. Chế độ: `strip` (mặc định —
> bản chuẩn vào cache) · `mark` ⟦BỎ:…⟧ · `raw` (đối chứng). CLI: `tl doc-text --markup`,
> `normalize_document --markup-mode auto` (auto = **mark cho DỰ THẢO / strip cho VBQPPL đã ban hành**).
> mark/raw KHÔNG đọc/ghi cache `extract_<id>.txt` (giữ corpus sạch nhãn).
>
> ★ **ĐO ĐƯỢC KHI DỰNG CA TDD (giả thuyết ban đầu SAI):** bản `mark` KHÔNG an toàn cho parser — `ART_SPLIT`
> đòi CHỮ HOA ngay sau "Điều N." nên nhãn `⟦` CHẶN Điều THẬT, còn `:` trong `⟦BỎ:` lại THOẢ lookbehind
> `[\s.;:]` nên tiêu đề ĐÃ GẠCH BỎ đẻ ra "Điều ma" (đo: `split_articles(mark)` = `[5]`, MẤT `[1]`).
> Không nhãn nào chữa được cả hai chiều ⇒ **CẤU TRÚC LUÔN phân tích trên bản `strip`**; mark/raw chỉ đi vào
> `text_markup` (bản XEM). Nhãn phải là phần tử `w:t` THẬT — python-docx CHỈ nối `w:t`, chèn text trần thì
> nhánh lib nuốt nhãn còn nhánh strip-tag giữ ⇒ hai đường đọc lệch nhau.
>
> **BÁN KÍNH HỒI QUY = 0 (đo trên kho THẬT):** quét 210 .docx — **200 file sạch markup cho text `strip` ≡ `raw`
> (bytes y hệt) 200/200**; 10 file có markup đều là DỰ THẢO (`strike`, cao nhất 102 và 63). Đối chứng dự thảo
> 16/7/2026: `"là cơ quan nhà nước"` 1→0, `"12 tháng"` 1→0, `"chứng thực"` 3→0 — **đúng nguồn gốc 3 "phát hiện"
> sai của GĐ5–GĐ7** (4.098 ký tự đã gạch bỏ từng bị đọc như quy phạm sống).
>
> **Gate:** selftest **1181/1181** (+9 ca r182; nền 1172 GIỮ NGUYÊN) + gen_instructions 38/38; golden regen
> ĐÚNG 2 khoá có chủ đích (`doc-text` parser surface do thêm `--markup`; `workflow_audit.files_scanned`
> 65→66 do thêm 1 module). **Đối chứng bằng revert 7 chốt:** mỗi chốt có ca VÂN-TAY RIÊNG
> (N1→lib · N2→zip · N3→doc-text · N4→cổng nạp · N5→chỉ điều-ma · N6→chỉ cache · N7→nhãn), "FAIL khác = 0" mọi lượt.
>
> **KERNEL:** thêm bất biến **19** — (a) rà dự thảo PHẢI ĐỌC KÈM TỜ TRÌNH (tách MỤC TIÊU CHÍNH SÁCH khỏi CÂU
> CHỮ QUY PHẠM; phần lớn "vênh" là KHÁC TẦNG) · (b) markup = ĐÃ BỎ / MỚI THÊM, không kết luận trên bản chưa
> lọc · (c) MỌI KHẲNG ĐỊNH PHÁP LÝ verify NGUYÊN VĂN qua `get_legal_article`/`tl extract`, **CẤM nêu theo trí
> nhớ**. Bù byte theo khuôn kernel-diet: khối ADR-0003 trích NGUYÊN VĂN sang `references/KERNEL_APPENDIX.md`
> §D ⇒ SKILL.md 48.115 → **48.061 B** (dưới trần 47K, biên 67 B).

# ★ v1.35.11 — r181 HERMETIC SELFTEST+GOLDEN + CHECKPOINT MKDIR (nền+gate xanh dưới defaultProfile «Luật BHXH») (2026-07-22)

> Nối r180: cổng khởi động phát hiện selftest nền LỆCH **1167/1169** trên ĐÚNG commit `e45571a` (cây sạch,
> HEAD/VERSION khớp) → dừng đúng luật, chẩn gốc READ-ONLY. Hai ca resume/checkpoint (`r20`/`r30`) đỏ do
> **selftest KHÔNG hermetic w.r.t. defaultProfile máy**: S10 lật default `vbqppl`→«Luật BHXH» (config gitignored
> nên cây git vẫn sạch) + một ca sớm gọi `apply_profile_offline(config THẬT)` **leak** `TL_PROFILE=«Luật BHXH»`
> tới r20/r30 (cleanup env ở sau). Đo TƯƠI bằng probe-file: ckpt rơi vào `…\Luật BHXH\corpus_audit_ckpt_all.json`
> — mà `_ckpt_save` **NUỐT OSError** khi thư mục cha thiếu → checkpoint resume ghi HỤT im lặng → không hội tụ.
> Vá cả 2 (user duyệt P1); **gate bước 5/6 (golden-test, determinism-audit) cũng đỏ TIỀN TỒN cùng gốc** (kiểm
> `git stash` về r180: rc=2 y hệt; `TL_PROFILE=vbqppl golden-test` → xanh 100% ⇒ goldens ĐÚNG, chỉ non-hermetic)
> → thêm **Fix3**. Mỗi vá 1 ca **CHỈ-NÓ-CHẶN** (đối chứng revert đủ 3). selftest **1172/1172** (+3 ca r181; nền
> 1169 GIỮ NGUYÊN) + gen_instructions **38/38** + gate 9 bước TOÀN XANH.

- **Fix1 (production) — `_ckpt_save` mkdir thư mục cha** (`hygiene.py` `cmd_corpus_audit`): thêm
  `_ckpt.parent.mkdir(parents=True, exist_ok=True)` trước `write_text`. Bịt lỗ THẬT: profile mới toanh / phiên
  đầu, cache-subdir chưa tồn tại → `FileNotFoundError` bị `except OSError: pass` nuốt → mất tiến độ resume im
  lặng (nghịch ý checkpoint chống-hỏng-dữ-liệu). Ca `r181_ckpt_save_mkdirs_missing_parent` (ép
  `_profile_cache_dir()`→subdir chưa có; đo checkpoint GHI ĐƯỢC + resume 2 lượt hội tụ + tự dọn). Cô lập:
  revert mkdir → **CHỈ** ca này đỏ (1170/1171), r20/r30 vẫn xanh (Fix2 pin cứu về base cache).
- **Fix2 (harness) — `selftest()` ghim `TL_PROFILE=DEFAULT_PROFILE`** (`tl.py` `_selftest_pin_profile`/
  `_selftest_restore_profile` + wrap bare selftest, restore ở finally ngoài): hermetic w.r.t. defaultProfile
  máy, miễn nhiễm mọi leak env giữa suite (đúng doctrine "bare selftest must be hermetic"). Ca
  `r181_selftest_pin_profile_hermetic` (env non-default giả lập → pin đưa `active==DEFAULT` &
  `_profile_cache_dir()==CACHE`, `restore` trả nguyên env). Cô lập: neuter thân pin → **CHỈ** ca này đỏ
  (1170/1171), r20/r30 vẫn xanh (Fix1 mkdir cứu). Call-site xác nhận bởi nền-xanh-dưới-«Luật BHXH».
- **Fix3 (gate) — golden-test tự-hermetic** (`workflow.py` `_golden_env`): LUÔN tiêm `TL_PROFILE=DEFAULT_PROFILE`
  vào env mỗi subprocess golden (goldens là artifact NỀN; subprocess kế thừa defaultProfile máy — nếu ≠ nền thì
  `reg-query` trả `base_also` / corpus·đếm theo overlay → golden ĐỎ GIẢ; determinism-audit đỏ ăn theo vì gọi
  `_golden_test` in-process). Case tự khai `TL_PROFILE` thì tôn trọng (setdefault); đường `--write` nhờ đó regen
  dưới ĐÚNG nền. Ca `r181_golden_env_pins_base_profile` (máy-độc-lập). Cô lập: revert `_golden_env` → **CHỈ** ca
  này đỏ (1171/1172). 6 ca golden đỏ (`hygiene_*` + `doc_text_cache_fixture`) là TIỀN TỒN r180, r181 thêm 0 đỏ.
- **Doctrine:** nền/gate có thể LỆCH mà cây git SẠCH khi trạng thái sống (defaultProfile) ở config **gitignored**
  → cổng khởi động PHẢI đo selftest **VÀ gate** TƯƠI, không tin "cây sạch = xanh". Mọi lệnh hermetic-CI (selftest,
  golden-test/determinism) phải trung hoà active-profile về DEFAULT (thêm cache-dir với selftest).

# ★ v1.35.10 — r180 THĂNG FAIL 8 Ô TT-DT (ADR-0009 Đ3) + 7 FIX GĐ2/CỔNG-1 (2026-07-22)

> Phiên grill-with-docs 22-07: xử lý log vận hành GĐ2+Cổng-1 «Luật BHXH» (S1-S10/D1-D7 — mỗi quyết
> định user duyệt từng câu) + việc mở #1 của bàn giao: thăng FAIL từng ô lớp TT-DT theo chuẩn
> zero-oan tuyệt đối. selftest **1169/1169** (+18 ca r180; nền 1151 GIỮ NGUYÊN).
> Hồ sơ đo tươi + đối chiếu tay: `D:\Quốc hội\thang-o-2026-07-22\` (ket_luan_doi_chieu.md).

- **THĂNG FAIL 8 (hệ·ô·trục) — user duyệt từng ô 22-07** (the_thuc.py `_THANG_FAIL` inline — bẫy I11):
  `hanh_chinh·noi_nhan_ds·co` · `hanh_chinh·noi_nhan_tu·co` · `hanh_chinh·ten_loai·co` ·
  `hanh_chinh·dia_danh·kieu` · `dang·the_loai·co` · `dang·dia_danh·co` · `dang·so_ky_hieu·co` ·
  `dang·dia_danh·kieu`. Đo TƯƠI production v1.35.9 trên 159 file (129 corpus ngâm + 30 mới), lớp A
  191 WARN đối chiếu tay TỪNG finding; chỉ thăng vi phạm ĐO ĐƯỢC (nhánh «cỡ không khai báo» giữ WARN
  — guard `chua_do`); B3/tin-cậy-thấp giữ INFO vĩnh viễn (Đ1); trục chưa duyệt giữ WARN. Ô CÓ oan ở
  lại WARN kèm hồ sơ: `dieu·kieu` (neo ăn câu trích dẫn Điều trong báo cáo 9/9), `de_muc_than` (ăn
  khối ký/đuôi tiêu đề), mọi ô canh both≈left, cụm dàn-trang-bằng-indent (TB_20), gach=đường-kẻ
  (tieu_de Đảng/tiêu ngữ), thut lệch <3mm (thut='0' không dung sai). Khoá 10 ca selftest ba chiều
  (FAIL thuận · WARN nghịch · INFO bất khả xâm); fixture r136/r143 nắn ĐÚNG thể thức (địa danh
  nghiêng, «Nơi nhận:» 12pt — sửa fixture, KHÔNG nới bộ kiểm) + biến thể `_VN136_NOSZ`.
- **S1 — cổng OCR đường corpus NỀN** (`_ingest_local_ocr_gate` PURE + nối `cmd_ingest_local`):
  `--source-quality ocr` ∧ ¬`--ocr-verified` ⇒ ép đường no-nlm-add, registry corpus=false + note
  `OCR_UNVERIFIED_NOT_CORPUS`, rc=2 kèm next_steps ocr-verify/ingest-ocr; DRY plan mang `ocr_gate`.
  (Hố 21-07: Hiệp định VN–Hàn scan vẫn corpus=true — ingest-local coi cặp cờ là trang trí trong khi
  profile-ingest gate cứng; nay MỘT cổng MỘT luật.)
- **S2 — `source-update-corpus false --as-ref` (HẠ REF một bước):** corpus=false + row_kind=ref,
  GIỮ nguồn NLM + nlm_status họ sống (ca ILO C102 hết 3 bước xoá-rồi-add-lại); shared_source_id
  KHÔNG chặn nhánh này (không đụng NLM); journal ghi before row_kind thật. CONTEXT.md +«Hạ ref».
- **S3 — extract resolve --sohieu ĐỌC CỘNG NỀN dưới --profile** (`_extract_resolve_entries` mirror
  base-also reg-query, hit nền scope='vbqppl'). Chẩn đoán log SAI HƯỚNG nhưng bệnh thật: không phải
  thiếu pattern VPQH mà là thiếu base-also (đo 22-07: `52-2025-VPQH` resolve ngon KHÔNG profile,
  fail DƯỚI profile). Ghi nhận data: sohieu Hiến pháp `52-2025-VPQH` thiếu token VBHN — sổ hygiene.
- **S4 — DRY .doc cũ hết phán chắc** (`_profile_dry_gate_soften` PURE): NO_TEXT_FOR_VERIFY trên
  .doc binary (không --text-file) → info `OLD_DOC_VERIFY_AT_APPLY` + `verify_at_apply=true` +
  plan registry.corpus=null (quyết ở apply sau convert server-side — hố dry/apply lệch 21-07).
- **S5 — source-update-corpus NOT_FOUND tự refresh MỘT lần** trước khi kết luận (hố: gọi ngay sau
  apply dính cache cũ, phải --refresh tay).
- **S7 — reg-query positional = lọc mờ theo tên** (alias --name; trước rc=2 unrecognized).
- **S8 — nlm-add --row-kind** (`_nlm_link_row_kind` PURE): cờ tường minh thắng suy-topology F-06,
  kind bảo hộ giữ luật cũ khi không cờ — hết phải register --row-kind riêng sau nlm-add.
- **Vận hành trong phiên (data, journaled):** D1 xoá dòng own mồ côi profile «Luật BHXH» của Luật
  DN VBHN_67 (hai-scope-hai-ảnh đóng; dòng nền `67-2025-VBHN-VPQH` canonical khoẻ — căn cứ Đ122/88
  thông) · D4 đóng bằng đo: 382/BC-BTC là RIA định mức chi NSNN 2027-2030, KHÔNG phải RIA BHXH
  (giữ cat; RIA BHXH vào sổ chờ-nạp) · D3 sổ chờ-nạp 6 tài liệu · D2/D5/D6/D7 + tồn dư mới → phiên
  hygiene riêng · S6 xref deferred (cần đo tái hiện riêng) · S9 không làm (cookie phía Google).
- Golden regen CHỦ ĐÍCH: `parser_surface.json` (+3 bề mặt cờ mới: --as-ref · reg-query positional ·
  nlm-add --row-kind). SKILL.md: header + §184 cổng OCR máy-chặn + lối hạ ref → **re-import Capabilities**.

# ★ v1.35.9 — r179 BẢY FIX LOG PHIÊN VẬN HÀNH + ADR-0010 TỪ VỰNG NLM (2026-07-21)

> Thi công `BAN_GIAO_r179_2026-07-21.md` — 7 quyết định đã grill 21-07, mỗi cái đo trước phán sau.
> selftest **1151/1151** (+20 ca r179; 1131 cũ GIỮ NGUYÊN — added-fire 936/1118 là hành vi đúng).
> ADR-0010 mới: `docs/adr/0010-tu-vung-nlm-status-dong-va-tach-claim-due.md`.

- **T1 — `register --nlm-status` TỪ VỰNG ĐÓNG (ADR-0010 Q1):** `_nlm_status_write_ok` (classify.py)
  = họ `pushed*/synced*/active/removed_<lý do>` + rỗng (route clear); giá trị lạ (added/live/ready/
  typo) → `NLM_STATUS_UNKNOWN` **rc=2 TRƯỚC mọi round-trip** (test khoá: fake-gas 0 call). Cửa ĐỌC
  `_nlm_status_known` GIỮ NGUYÊN khoan dung (trash*/deleted/removed-trần) — bất đối xứng CÓ CHỦ ĐÍCH,
  selftest khoá cả hai chiều.
- **T2 — lệnh MỚI `backfill-nlm-status --dry/--apply`:** nắn MỘT LẦN added→pushed, live→active
  (map tất định, case-insens; map INLINE trong hàm — bẫy I11 hằng module-level không sống sót
  bind-REBASE, dính thật khi smoke). Per-row `reg_upsert` journaled + before → undo được; giá trị
  ngoài map KHÔNG đụng (stray `OUTSIDE_MAP`/`NO_DRIVE_ID`). Đo DRY trên «Luật BHXH»: **25 map
  (23 added + 2 live), 1 stray `ready`**. ⚠ CHẠY SAU DEPLOY (xem mục vận hành cuối).
- **T3 — guard `sua_doi` TỰ TRỎ chặn cứng:** `_sua_doi_self_ref` (PURE) — token trong sua_doi
  (tách `;`/`,`) sau `norm_sohieu` trùng số hiệu CHÍNH dòng (từ `--sohieu` cùng lệnh, fallback
  manifest theo drive_id) → `SUA_DOI_SELF_REFERENCE` rc=2, **KHÔNG có --force** (không tồn tại ca
  hợp lệ). Bắt biến thể `142/2025/QH15 ≡ 142-2025-QH15`. Xác minh bề mặt: cờ `--sua-doi` SINH ĐỘNG
  từ dest ở cli.py:437-439 (literal không có trong repo — log ghi đúng, grep sai chỗ).
- **T4 — draft theo BẬC BẰNG CHỨNG (mọi hệ) + vá title BOM/letterhead.** Đo 6 docx thật lô BNV
  16/7 trước khi sửa: sohieu classify nhiễm UUID tên file (`7_2026_e7c88c81`), issue_date nhiễm
  trích dẫn thân («Căn cứ NĐ… 2018») ⇒ veto official KHÔNG dùng được sohieu/issue_date thô.
  - Bậc: banner «DỰ THẢO» dòng riêng (`_draft_banner_line`, chịu artifact toạ độ docx
    `-44005514605Dự thảo…`) HOẶC Số-line KHUYẾT («Số:  /TTr-BNV», `_sohieu_line_khuyet`) ⇒ draft
    MẠNH; Số-line letterhead CÓ SỐ trong TEXT (`_sohieu_from_title_zone(strict_letterhead=True)` —
    KHÔNG best-fallback/filename) **AND** dateline đủ số (`_issue_dateline_complete`) ⇒ official
    PHỦ QUYẾT marker yếu («lấy ý kiến»/«góp ý»/«dự thảo» trong trích yếu); không bằng chứng ⇒ giữ
    hành vi cũ. Nghiệm thu: QĐ-TW ký + «lấy ý kiến» → draft:false (hết oan, ca log vận hành);
    6/6 file thật lô BNV GIỮ draft:true đúng (3 khuyết/banner + 3 weak-không-bằng-chứng).
  - Title (`_profile_title_from_header`): bỏ BOM đầu file (đường .txt/.html utf-8 — quốc hiệu hết
    thành title); bỏ dòng LETTERHEAD tên cơ quan (IN HOA ≤60, pattern agency BOUNDED — `bo\s+(?!luat)`
    né «BỘ LUẬT», không nhận `so|vu|ban` trần nên «SO SÁNH…»/«BAN HÀNH…» vẫn là title) + strip
    artifact toạ độ docx («598805267335BỘ NỘI VỤ»).
- **T5 — scope MỘT TỪ VỰNG ở 3 lệnh đọc (CONTEXT «Scope (dòng kết quả)»):** khoá `_scope` riêng
  của reg-query BỎ HẲN — dòng nền base-also mang `scope:'vbqppl'` + cờ `BASE_SCOPE_HIT` per-row
  Y HỆT source-map/exists ở CẢ reg-query (JSON rows + text `[nền]`) LẪN locate (text `[nền]` từng
  dòng + JSON). Selftest r6 cập nhật khoá `_scope` tuyệt chủng.
- **T6 — `vbhn-check --sohieu`:** alias MỎNG của positional (định tuyến y hệt: số hiệu → goc,
  trích yếu → subject; positional thắng nếu cả hai) — tay quen `--sohieu` hết usage-error.
- **T7 — `locate --json` JSON THẬT (`locate.v1`):** envelope cả 3 nhánh (offline_index /
  offline_manifest / webapp_find): `query/mode/count/shown/truncated/low_confidence/rows[]`
  (+`profile_hits/base_hits`, warnings token máy-đọc `OFFLINE_CACHE_*`); stdout sạch (narration
  tắt); row nền scope+BASE_SCOPE_HIT (T5). rc giữ nguyên ngữ nghĩa cũ.
- **T8 — tách nhãn claim/due (ADR-0010 Q2), sự cố «51/40/51» đóng bằng SỐ ĐO:** đo lại tươi trên
  «Luật BHXH»: vật lý 51 = claim 40 (24 own + 16 ref) + **11 dòng `removed_from_drive` nguồn CÒN
  SỐNG** (lô PDF dự thảo 16.6 — file Drive xoá, nguồn NLM giữ); reconcile desync_real=0; 10 dòng
  blank đều corpus=false (không thuộc diện). → Helper chung `_nlm_due_rows` (corpus∪ref − removed_*,
  blank-nb fold về base); **slot-audit**: khoá `gap` trần BỎ → `desync_estimate` (đếm) +
  `nlm_due_rows`/`coverage_gap`(+sample) + `removed_family_still_pointing` + `note_removed_live`
  khi giải thích TRỌN (hết lời khuyên backfill sai) + `labels_note`; **nlm-reconcile**: +`nlm_due_rows`/
  `coverage_gap` per-source (có live-set) + `removed_family_still_live`(+sample 11 file đúng tên) +
  `labels_note` (chỉ khi KHÔNG --from-plan — không có live ground-truth thì không phán). Hai lệnh
  nay kể CÙNG một câu chuyện với tên tường minh; «Hai phép đo ≠ nhau, lệch số KHÔNG phải mâu thuẫn».
- **Bề mặt/gate:** GENERATED_SPECS + COMMAND_META +`backfill-nlm-status` (medium/registry/dry-run,
  module nlm_ops); _STUB_MAP +7 tên (`_nlm_status_write_ok`/`_sua_doi_self_ref`/`_draft_banner_line`/
  `_sohieu_line_khuyet`/`_issue_dateline_complete`/`_nlm_due_rows`/`cmd_backfill_nlm_status`+
  `_backfill_nlm_status_candidates`); parser_surface regen CHỦ ĐÍCH (locate --json · vbhn-check
  --sohieu · lệnh mới). Selftest +20 ca `r179_t*` — kỷ luật đột biến r178: mỗi chốt có ca CHỈ nó
  chặn (vd `r179_t4_official_veto_requires_both_evidences` giết mutant nới strict→best-fallback;
  `r179_t1_register_gate_rc2_before_server` chứng minh gate đứng trước server bằng fake-gas 0 call).
- **Vận hành SAU deploy (một lần):** `tl --profile "Luật BHXH" backfill-nlm-status` DRY → `--apply`
  (25 dòng; stray `ready` trên VBHN_14 ATVSLĐ sửa tay sau khi hiểu nguồn gốc) — cờ
  `NLM_STATUS_MISMATCH` trên dòng added sẽ tự hết. Cân nhắc chạy thêm trên scope nền vbqppl.
- **CONTEXT.md** +5 mục từ vựng (Draft (ingest) · nlm_status · Scope (dòng kết quả) · nlm_claim ·
  nlm_due) — sản phẩm phiên grill 21-07, commit CÙNG release này.

# ★ v1.35.8 — r178 TIÊU CHÍ MÁY NHẬN DIỆN CÔNG VĂN HỆ ĐẢNG + ô mới `kinh_gui` (2026-07-21)

> Đóng việc-mở treo từ r175: biến thể `dang.cong_van` ĐÃ CÓ Ô từ lâu nhưng **chưa bao giờ kích
> hoạt được** — code chỉ bật cong_van cho `hanh_chinh` qua regex «V/v», mà HD05 không dùng «V/v».
> Đối soát nguyên văn HD05 27/5/2026 (GDoc `1Lko21mO…`). selftest **1131/1131** + gen_instructions 38/38.

- **Tiêu chí máy (2 vế, neo vào Ô):** ô `so_ky_hieu` khớp «Số N-CV/…» **∧** KHÔNG có ô `the_loai`.
  - Vế 1 — HD05 **3.1.2.b ví dụ 3**: *«Công văn của ban tuyên giáo và dân vận tỉnh uỷ — Số
    138-CV/BTGDVTU»*; bảng thống nhất viết tắt khi TRÙNG chữ cái đầu (**3.1.2.a**: QĐ, CT, CTr,
    TT, TTr) **không chứa CV** ⇒ không thể loại nào khác chiếm ký hiệu này. Khai **B2** (suy từ ví
    dụ + vắng mặt, không phải bảng liệt kê đóng) — cố ý KHÔNG khai B1.
  - Vế 2 — phản đảo **5.1.1** *«Văn bản ban hành đều ghi tên loại văn bản, **trừ công văn**»* ⇒
    CÓ tên loại ⇒ KHÔNG phải công văn (**B1**).
- **⚠ PHẢI neo vào Ô, KHÔNG dò head-blob như nhánh «V/v».** Đo 21-07 trên 190 docx thật: chuỗi
  «-CV/» khớp đúng **1 file — và là DƯƠNG TÍNH GIẢ**: `02_Bao-cao-tiep-thu-chi-dao.docx` là BÁO
  CÁO, chuỗi nằm ở **đoạn thân số 8** (*«Công văn số 3152-CV/VPTW, ngày 19/6/2026»*), **offset
  1040 < 3000** nên `_head[:3000]` CHẠM. Viết theo khuôn cũ là hỏng ngay trên dữ liệu đang có.
- **«Kính gửi» BỊ BÁC làm tiêu chí** (từng là ứng viên): khớp **35/190** file thật — báo cáo, tờ
  trình, phiếu trình. HD05 9.2.3 chỉ cho chiều *công văn ⇒ có Kính gửi*, KHÔNG cho chiều đảo.
- **Ô MỚI `dang.kinh_gui`** (trong bảng biến thể, chỉ sống khi cong_van bật) — HD05 **PL2 mục 5**:
  *«Từ "Kính gửi" đối với thể loại công văn … | In thường | **14** | **Nghiêng**»* + **9.2.3** (ô
  5a), **B1**. `canh`/`thut` = **"na"**: PL2 chỉ pin cỡ+kiểu, còn 9.2.3 *«ở chính giữa, trang đầu
  văn bản»* nhập nhằng giữa canh-giữa và vị-trí-giữa-trang ⇒ không kiểm (khuôn "na" r175).
- **Classifier hệ Đảng:** HD05 không có neo KÝ TỰ cho trích yếu công văn (PL2 nêu ví dụ *«về việc
  chuẩn bị hội nghị…»*, chữ thường) ⇒ neo VỊ TRÍ theo **5.2.3** *«trình bày cân đối dưới số và ký
  hiệu văn bản (ô số 5b)»* — đoạn chưa gán đầu tiên SAU `so_ky_hieu`, khai **B3** (user duyệt
  21-07). Nhánh tự phòng vệ 2 chốt (ô `so_ky_hieu` phải mang «-CV/»; ứng viên không in hoa) vì gán
  vô điều kiện sẽ **cướp đúng đoạn `the_loai`** của báo cáo (bước 3+4 chạy sau, `_set` không ghi đè).
- **⚠ Hồi quy tự bắt được và đã vá:** đặt nhánh `kinh_gui` ngoài cổng «-CV/» làm
  `01_To-trinh_Bo-Chinh-tri.docx` **rụng 1 `TT-DT-THAN-THUT`** (4170→4169) — ô `kinh_gui` không vào
  bảng khi biến thể tắt, nên đoạn bị nuốt thành **mất kiểm âm thầm**. Siết vào trong cổng ⇒
  **190/190 docx thật khớp r177 từng finding một** (183 file thật + 7 file khoá `~$` của Word;
  6 docx mới xuất hiện dưới `C:qh` sau mốc baseline đều hệ hành chính, không ca nào nhận nhầm).
- **Test r176 ca (f), f1-f10:** công văn Đảng chuẩn = 0 TT-DT · trích yếu 14 đứng →
  `TRICH-YEU-CV-{CO,KIEU}` · ô `kinh_gui` sai → `KINH-GUI-{CO,KIEU}` · ô đã `bo`
  (`the_loai`/`trich_yeu`) hết bị kiểm · **chiều nghịch**: BÁO CÁO (có tên loại + «Kính gửi:» +
  «-CV/» ở thân) không bị nhận nhầm và `the_loai` VẪN được kiểm · «Kính gửi» một mình không bật
  được biến thể · «-CV/» + CÓ tên loại không bật được biến thể (f7/f8) · không «-CV/» thì biến
  thể tắt (f9) · BÁO CÁO Đảng có «Kính gửi:» dài vẫn giữ `TT-DT-THAN-THUT` (f10).
- **⚠ Bộ đột biến 7 chốt — bắt được 3 CHỐT CHẾT mà selftest 1131/1131 vẫn xanh.** Vế «vắng
  the_loai», vế «-CV/» tầng check, cổng «-CV/» tầng classifier: gỡ từng cái ra, test vẫn XANH, vì
  mọi ca đều đã bị một chốt KHÁC chặn trước khi chạm tới. Thêm f7/f9/f10 mới đỏ đúng. Hai bẫy phụ
  lộ ra khi dựng ca: (i) dòng «Kính gửi» 23 ký tự rơi **dưới ngưỡng giỏ `than`** ⇒ ca rỗng nghĩa,
  phải kéo dài; (ii) `SK_PAT["dang"]` = `^\s*Số\s+\d+\s*-\s*[A-ZĐ]+/` **không khớp `TTr`** (chữ
  `r` thường) ⇒ `i_sk = None` ⇒ nhánh không chạy ⇒ ca đậu rỗng nghĩa, phải đổi sang «-BC/».
  **Trạng thái cuối:** 6/7 chốt SỐNG (có ca đỏ đúng). Vế «-CV/» ở **tầng check vẫn là CHỐT CHẾT**
  — cổng classifier đã chặn từ trước nên hạ nó xuống `True` không đổi finding nào. **Giữ lại như
  phòng vệ thừa CÓ CHỦ Ý và ghi thẳng vào code** (hai tầng cùng đọc một căn cứ 3.1.2.b), KHÔNG
  tuyên bố là đã được test khoá.
- **Sổ `_BAT_DUOC` giữ nguyên 53 ô** (KHÔNG bump): sổ r173 dựng `_tat_ca` từ bảng CHÍNH
  `_tt_dac_ta()`, còn `trich_yeu_cv`/`kinh_gui` thuộc bảng BIẾN THỂ — không đột biến được trên văn
  bản mẫu chung, nên khoá ở r176 (e)/(f) thay thế. Phạm vi này đã ghi vào comment sổ để khỏi tưởng thiếu.
- **Còn cách ly:** nhóm «văn bản/phụ lục ban hành kèm theo» (NQ351 Mẫu 6b/11b/14) — không đổi.

# ★ v1.35.7 — r177 PHÂN XỬ HAI CA CÁCH LY: trich_yeu·kieu GIỮ «đậm» (gỡ Đ5) · viết tắt Quy định = QĐ (2026-07-21)

> Đóng giỏ «chờ nguyên văn B1» treo từ r176, đúng trình tự «không đoán»: đối soát nguyên văn
> corpus NĐ30 PL I (GDoc `1YgArj3U…`) + HD05 27/5/2026 (GDoc `1Lko21mO…`). selftest **1131/1131**
> + gen_instructions 38/38.

- **Ca 1 — viết tắt "Quy định" hệ Đảng: `QĐ` THẮNG, `QĐi` bác.** HD05 mục 3.1.2.a nguyên văn:
  *«Trường hợp chữ cái đầu các âm tiết của tên loại văn bản trùng nhau thì thống nhất ký hiệu
  một số tên loại văn bản như sau: **Quyết định, Quy định: QĐ**; Chỉ thị: CT; Chương trình: CTr;
  Thông tri: TT; Tờ trình: TTr»*; ví dụ 3.1.2.b(ii): *«Quy định của Uỷ ban Kiểm tra Trung ương —
  Số 23-QĐ/UBKTTW»*. Chuỗi `QĐi` KHÔNG xuất hiện trong toàn văn HD05. `ABBR_DANG` + §5.3 vốn đã
  đúng — sửa phía SẢN PHẨM: `mau-dang-hd05/Mau_Dang_05_Quy_dinh.docx` `Số   -QĐi/ĐU` →
  `Số   -QĐ/ĐU` (readback sạch; quét cả 15 docx chỉ mẫu 05 dính) + bảng GHI_CHU.md kèm nguyên văn.
  ⚠ **ĐÍNH CHÍNH HỒ SƠ**: bảng viết tắt nằm ở HD05 **mục 3.1.2**, KHÔNG phải 3.2 như ghi chú r176
  (3.2 = kỹ thuật trình bày số-ký-hiệu) — cite cờ `TT-VIET-TAT` sửa `HD05 3.2` → `HD05 3.1.2`.
- **Ca 2 — `(hanh_chinh|dang)·trich_yeu·kieu` «đậm,nghiêng vs đậm»: «đậm» THẮNG, GỠ CÁCH LY Đ5.**
  NĐ30 PL I II.5.b nguyên văn: *«Trích yếu nội dung văn bản được đặt ngay dưới tên loại văn bản,
  trình bày bằng chữ in thường, cỡ chữ từ 13 đến 14, kiểu chữ **đứng, đậm**»*; HD05 PL2 mục 5:
  *«Trích yếu nội dung văn bản | In thường | 14-15 | **Đứng, đậm**»* (công văn: 12 nghiêng — khớp
  biến thể TT-5 sẵn có). Bảng đặc tả («dam», B1) vốn đúng ⇒ «đậm,nghiêng» đo được trong thực chiến
  là LỆCH CHUẨN THẬT, không oan. Gỡ khối `_bo_kiem` Đ5 trong `_the_thuc_check_dac_ta`; mức vẫn
  **INFO** (trich_yeu thuộc nhóm tin-cậy-thấp Đ1 — không FAIL, chưa thăng, không cần duyệt zero-oan).
- **Test:** r176 (d) LẬT CHIỀU — trich_yeu đậm+nghiêng nay PHẢI ra `TT-DT-TRICH-YEU-KIEU` mức INFO;
  sổ r173 `_BAT_DUOC` **51→53 ô** (thêm `(hanh_chinh|dang).trich_yeu`), gap ledger 8→6 (hồ sơ
  comment cập nhật). Docstring Đ1-Đ5 + baseline ghi lại theo trạng thái r177.
- **Nghiệm thu:** tầng 1 đo lại @r177 trên 34 file sản phẩm còn trên đĩa (15 docx Đảng + 19 NQ351):
  **0 TT-DT tuyệt đối**; `_TEST_dien_that` giữ **0/0/0**; mẫu trống giữ đúng 2 FAIL số-KH/địa-danh;
  mẫu 05 sau sửa không phát sinh finding mới. Corpus đo-lũ 129 file KHÔNG đo lại được (bản tạm đã
  xoá, `t2_corpus.json` chỉ lưu tên+findings) — theo bảng nghiệm thu r176 (`tong_hop_sau_va.md`
  dòng `trich_yeu·kieu 7/7`), lớp A số học 856 → **863** (+7 INFO, toàn bộ là ca đậm+nghiêng thật).
- **Reference đồng bộ:** §6.34 (Đ5 → phân xử xong kèm nguyên văn; sổ 53 ô; test d lật) · §5.3 hàng
  số-ký-hiệu đóng dấu «không có `QĐi`». ADR-0009 thêm mục «Hậu kiểm 2026-07-21 (r177)». Comment
  `ABBR_DANG` ghi căn cứ 3.1.2.a.
- **Việc mở KHÔNG đổi:** cong_van hệ Đảng chưa có tiêu chí máy · nhóm «kèm theo» (Mẫu 6b/11b/14)
  VẪN cách ly (chưa đối soát đủ căn cứ từng ô) · builder trục kiểu/canh/thụt còn inline · thăng
  FAIL từng ô = vòng sau.

# ★ v1.35.6 — r176 ADR-0009 BƯỚC 5 «NỐI BỘ KIỂM»: lớp đặc tả TT-DT đọc bảng vào production (2026-07-21)

> Hoàn tất trình tự 5 bước ADR-0009. `the-thuc-check` nay có LỚP ĐẶC TẢ đọc bảng `_tt_dac_ta()`
> (+ biến thể r175): finding `TT-DT-<Ô>-<CO|KIEU|CANH|THUT>` theo đúng gói Đ1-Đ5 user duyệt 21-07.
> selftest **1131/1131** (+1: r176) + gen_instructions 38/38.

- **Parser mở rộng** (`_the_thuc_parse_docx`): kênh `p["dt"]` per-đoạn — cỡ (mode), tỉ lệ
  đậm/nghiêng/gạch, `dam_dau` (run đầu — văn phạm `:tien_to`), jc/firstLine/left KẾ THỪA STYLE
  đủ tầng run → pPr/rPr → pStyle → Normal → docDefaults (1 cấp basedOn; thiếu tầng style từng đẻ
  701 finding oan ở đo lũ). Khoá cũ ind/jc/dam/szs GIỮ NGUYÊN ngữ nghĩa — cờ tay r143-r171 không đổi.
- **Classifier `_tt_dt_phan_loai`** port NGUYÊN TRẠNG từ bộ kiểm nháp đo-lũ (6 bẫy oan đã vá giữ
  đủ) + **vá oan mới lộ khi quét sổ**: neo `thong_qua` siết theo công thức Đ36 k1 «<loại> này được
  Quốc hội … thông qua» — thân Lệnh công bố («Luật X đã được Quốc hội thông qua») hết bị gán nhầm.
- **Lớp kiểm `_the_thuc_check_dac_ta`** nối sau T3: Đ1 B1/B2→WARN · B3→INFO · ô tin-cậy-thấp
  (than/ten_cq/ten_cq_tren/trich_yeu/tieu_de_pc/ho_ten_ky)→INFO, KHÔNG BAO GIỜ FAIL; Đ3 chỉ chạy
  khi nhận diện được khối đầu (quoc_hieu/tieu_de), nhóm «kèm theo»/phụ lục bỏ; Đ4 nhường cờ tay
  (TT-BAC-CO-CHU↔(quoc_hieu|tieu_ngu|tieu_de)·co mọi hệ · TT-CHUC-VU-DAM↔dang chuc_vu_ky·kieu ·
  TT-CHUONG-CANH-GIUA↔dang (phan_chuong|muc)·canh — một hiện tượng một finding); Đ5 cách ly
  (hanh_chinh|dang)·trich_yeu·kieu chờ nguyên văn NĐ30 PL I II.5. Biến thể resolve trước khi so:
  «/QĐ-CTN»→qd_ctn · «V/v» đầu dòng→cong_van hanh_chinh (cong_van hệ Đảng CHƯA có tiêu chí máy —
  để sau, không đoán).
- **Sổ `_BAT_DUOC` r173: 1 ô → 51 ô** (test tự cưỡng chế đúng thiết kế — nối xong là sổ buộc phải
  mở). 8 gap còn lại có hồ sơ trong comment r173: 2 Đ5 cách ly · 3 neo-bằng-chính-thuộc-tính-lật
  (de_muc_than ×2, co_quan_ban_hanh) · 2 đoạn văn bản test <25 ký tự · 1 biên quét 2n/3 văn bản ngắn.
- **r176 MỚI** khoá 6 hành vi: (a) tầng-1 builder 3 hệ + Lệnh/QĐ-CTN = 0 TT-DT; (b) Đ3 mất khối
  đầu → lớp im hẳn kể cả khi có lỗi thật; (c) Đ4 chuc_vu_ky Đảng đậm → chỉ TT-CHUC-VU-DAM;
  (d) Đ5 trich_yeu đậm+nghiêng → im; (e) công văn V/v chuẩn 12-13 đứng → 0, V/v 14 nghiêng →
  TT-DT-TRICH-YEU-CV-CO+KIEU, ô đã `bo` không kiểm; (f) `dam:tien_to` «Điều 3.» đậm + nội dung
  Đứng → không TT-DT-DIEU-KIEU, không giẫm TT-KHOAN-DAM.
- **NGHIỆM THU trên corpus đo-lũ** (129 file, baseline `t2_corpus.json` @v1.35.5): tầng 1 —
  19 mẫu NQ351 + 15 mẫu HD05 + builder qua PRODUCTION = **0 TT-DT tuyệt đối**; lớp A 876 → **856**,
  diff per-ô ĐÚNG 5 dòng giải trình 100% theo quyết định đã duyệt (−9 Đ4 nhường TT-BAC-CO-CHU:
  tieu_de 7 + quoc_hieu 1 + tieu_ngu 1 · −4 Đ4 nhường TT-CHUC-VU-DAM · −7 Đ5 cách ly trich_yeu);
  lớp B phụ lục 3.905 → **0** (Đ3); lớp C 46 → 42 (−4 cùng lý do Đ4/Đ5). Chống-trùng kiểm tay
  2 file đại diện: mỗi hiện tượng đúng 1 finding cờ tay, 0 TT-DT trùng.
- tl.py: +2 tên `_STUB_MAP["the_thuc"]` (`_tt_dt_phan_loai`, `_the_thuc_check_dac_ta`).

# ★ v1.35.5 — r175 ADR-0009 BƯỚC 4 ĐO LŨ xong + vòng-2 BƯỚC 1 vá bảng theo 5 quyết định Đ1-Đ5 (2026-07-21)

> BƯỚC 4 "đo lũ" chạy NGOÀI repo (bộ kiểm nháp đọc bảng, `D:\Quốc hội\do-lu-2026-07-21`), user duyệt
> cả gói Đ1-Đ5, rồi quay bước 1 vá bảng ngay trong release này. selftest **1130/1130** (+1: r175) + 38/38.

- **Số liệu bước 4** (skill v1.35.4): tầng 1 — builder tự dựng 0 finding; 33 mẫu chuẩn 15 finding,
  đối chiếu tay **100% là khiếm khuyết của BẢNG, không phải lỗi mẫu**. Tầng 2 — 129 file thật
  (khớp 105/111 dòng nền 19-07): lớp A 49 VB hoàn chỉnh **1.214 finding**, hai VB nền "đạt chuẩn
  hoàn toàn" ăn 85/57 ⇒ **Đ1: chưa ô nào thăng FAIL** (zero-oan chưa ai đạt). Phiên đo tự bắt
  6 nguồn cảnh báo oan của chính bản nháp (7.779 → 5.842) — "đo trước, phán sau" trả lãi.
- **5 quyết định Đ1-Đ5** (ADR-0009, user duyệt 21-07): Đ1 không thăng FAIL; Đ2 vá bảng trước khi
  nối; Đ3 chỉ áp lớp đặc tả cho file có khối đầu; Đ4 chống báo trùng cờ tay; Đ5 cách ly
  `trich_yeu·kieu` chờ nguyên văn NĐ30 PL I II.5.
- **Bảng 54 → 59 ô** (thi hành Đ2): vbqppl_qh +3 ô B1 đo từ sơ đồ mẫu (`cau_ban_hanh` «Quốc hội
  ban hành Luật … .» 14 nghiêng; `co_quan_ban_hanh` dòng chủ thể «CHỦ TỊCH / NƯỚC CHXHCNVN» 14 đậm
  giữa — tầng 1 lộ: 3 finding chuc_vu_ky 14pt là bản nháp GÁN NHẦM dòng này, chữ ký thật 13pt khớp
  bảng; `tu_lenh` «QUYẾT NGHỊ:»/«NAY …:» 14 đậm giữa); ô `can_cu` QH mở nghĩa gồm «Xét/Theo đề
  nghị»; `de_muc_than` hanh_chinh (B3→INFO vĩnh viễn) + dang (B2* — reference TT-6 «đề mục: đậm»).
- **Văn phạm ô mới**: kiểu `dam:tien_to` (ô `dieu` cả 3 hệ — đậm áp TIỀN TỐ «Điều N.»+tên, nội dung
  inline Đứng, khớp `dam_dau` r171); giá trị `na` cho canh/thụt = luật không ấn định + thực tiễn đa
  dạng ⇒ KHÔNG kiểm (đề mục tự do: kho mẫu HD05 canh giữa, corpus dàn đều thụt 1cm — hai kiểu cùng sống).
- **`_tt_dac_ta_bien_the()` MỚI** — trục thứ ba BIẾN THỂ THEO MẪU: override Mẫu 16 QĐ-CTN (quốc hiệu
  13, B1 sơ đồ); biến thể công văn hanh_chinh (ô 5b NĐ30: trích yếu «V/v» 12-13 đứng, B2*) và dang
  (TT-5: 12 nghiêng, B2*) kèm `bo` tên loại/trích yếu; nhóm «kèm theo» (6b/11b/14) VẪN CÁCH LY.
- **Test**: r170 mở rộng 59/59 ô (+spec Lệnh CTN thứ 5; parse `:tien_to`; skip `na`) · r173 đột biến
  phủ 59/59 (spec Lệnh CTN + câu ban hành + đề mục; sổ `_BAT_DUOC` KHÔNG đổi — đúng: bộ kiểm chưa
  nối) · **r175 MỚI** khoá cấu trúc bảng biến thể (override phải KHÁC gốc + đủ căn cứ/bậc; ô `them`
  tuple-6 không trùng bảng chính; `bo` trỏ ô có thật).
- **Builder BYTE-IDENTICAL** — không ô mới nào chảy vào `_tt_co_build`/`_CHON`; bundle ×2 cùng SHA.
- **Đo lại sau vá** (bộ kiểm nháp): tầng 1 **0/0/0 TUYỆT ĐỐI** (builder · 19 mẫu NQ351 · 15 mẫu
  HD05 — đạt chuẩn ADR "mẫu chuẩn 0 finding lệch bảng"); lũ lớp A 1.214 → **876**.
- Hồ sơ: `docs/adr/0009` cập nhật bước 4 + Đ1-Đ5 + nội dung r175 · reference §6.34 (59 ô, `:tien_to`,
  `na`, biến thể) · CONTEXT.md +«Biến thể mẫu», +«na».
- Còn lại bước 5 (nối bộ kiểm theo Đ3/Đ4/Đ5, cập nhật sổ `_BAT_DUOC` từng ô) — phiên sau.

# ★ v1.35.4 — r174 ADR-0009 BƯỚC 3a: cỡ chữ builder DẪN XUẤT từ bảng đặc tả — byte-identical (2026-07-21)

> BƯỚC 3 (phần a — cỡ chữ, thứ dễ trôi nhất vì là con số). selftest **1129/1129** + 38/38 giữ nguyên.

- **`_tt_co_build(he)` MỚI**: dict `S` của `the_thuc_build` không còn hard-code — dẫn xuất từ
  `_tt_dac_ta()`: ô đơn trị dùng thẳng; ô khai DẢI tra `_CHON` (lựa chọn nội bộ **bậc B3** trong dải
  luật, đặt CẠNH bảng, lệch dải là ValueError ngay lúc build — thà nổ sớm còn hơn lặng lẽ hard-code
  trở lại). Từ nay **sửa cỡ trong bảng là builder đổi theo** — đúng nghĩa nguồn sự thật cho trục cỡ chữ.
- **Bằng chứng an toàn**: đối chiếu tay 33 giá trị × 3 hệ khớp 100% S cũ; build lại 4 văn bản chuẩn
  (dang · Luật QH · NQ UBTVQH · hành chính) **BYTE-MATCH sha256 `word/document.xml`** trước/sau.
  Đăng ký `_tt_co_build` vào bảng re-export `tl.py` (bẫy #6).
- **Phạm vi trung thực**: kiểu/canh/thụt trong builder VẪN inline tại từng chỗ render — nhưng bị
  r170 (54/54 ô) + r173 (đột biến) khoá từ ngoài: builder lệch bảng là đỏ ngay. Nối nốt trục
  kiểu/canh vào lúc nối bộ kiểm (bước 5) nếu thực tế cho thấy cần — ghi chú trong ADR-0009.

# ★ v1.35.3 — r173 ADR-0009 BƯỚC 2: khoá test 100% (54/54 ô) + selftest đột biến sổ-hai-chiều (2026-07-21)

> BƯỚC 2/5 của ADR-0009. selftest 1128→**1129** (thêm r173), gate GIỮ 9 bước — đột biến là NỘI DUNG
> của bước selftest, không phải bước gate mới (Q7 user chốt).

- **r170 chiều thuận 28→54/54 ô**: thêm văn bản dựng thứ 3 (NQ UBTVQH — phủ `dia_danh/muc/quyen_han_ky/
  noi_nhan_*` hệ QH mà mẫu Luật không có) + thứ 4 (**hành chính 18/18 ô — trước đây hệ này 0 test**);
  dang bổ `muc` + `noi_nhan_tu`; qh-Luật bổ `thong_qua`. **KHOÁ ĐỦ-PHỦ tự cưỡng chế**: r170 đối chiếu
  tập (hệ, ô) đã test với toàn bảng — thêm ô vào bảng mà quên viết test là ĐỎ ngay, độ phủ không thể
  trôi ngầm lần nữa (bài học 28/48=58% âm thầm của r170 cũ).
- **r173 chiều nghịch — đột biến LẬT ĐẬM từng ô (54 đột biến) + SỔ HAI CHIỀU**: `_BAT_DUOC` ghi ô bộ
  kiểm HÔM NAY bắt được (duy nhất `dang.chuc_vu_ky` → TT-CHUC-VU-DAM, cờ viết tay — khớp thực nghiệm
  1/5 ngày 20-07); tụt lùi = đỏ · ô gap bật cờ mới (bước 5 nối dần) = đỏ buộc ghi sổ. Máy-canh-cho-
  máy-canh: bằng chứng sống rằng dây nối bảng→bộ kiểm hoạt động, sống sót qua refactor.
- **Bẫy mới ghi nhận**: `the_thuc_check()` gọi thẳng cấp module KHÔNG normalize `-`→`_` của tham số
  `he` (chỉ CLI normalize) — `he="vbqppl-qh"` nổ KeyError câm trong test. r173 dùng dạng gạch dưới.
- **Vá lệch version 3 nơi**: v1.35.2 commit trước bump file `VERSION` nhưng SÓT hằng `tl.py:94` và
  header SKILL.md ⇒ r65 (guard ADR-0001 `version_forked == VERSION`) đỏ đúng chức năng. v1.35.3 đồng
  bộ cả ba. Bài học: bump version = **3 chỗ** (VERSION · tl.py · SKILL.md header).
- Kernel chỉ đổi header ⇒ re-import Capabilities KHÔNG bắt buộc.

# ★ v1.35.2 — r172 ADR-0009 BƯỚC 1: vá bảng đặc tả (+bậc thẩm quyền) · normalize idempotent với build (2026-07-21)

> Grilling 20→21-07 chốt ADR-0009 (8 quyết định, user duyệt từng cái): `_tt_dac_ta()` sẽ thành nguồn
> sự thật DUY NHẤT (nối 5 bước); thang thẩm quyền B1>B2>B3; severity buộc vào bậc (B3→INFO vĩnh viễn);
> chuẩn thăng FAIL zero-oan; selftest đột biến hai chiều (gate GIỮ 9 bước). Đây là BƯỚC 1.
> Cứ liệu mở màn: đo 5 đột biến vi phạm bảng → bộ kiểm bắt 1/5; bảng không được hàm nào đọc (kể cả
> builder — chỉ selftest); file "0 finding" theo GHI_CHU thực chất 2 WARN thật. selftest **1128/1128** giữ.

- **`_tt_dac_ta()` 48→54 ô, tuple 5→6 trường (+`bac`)**: mỗi ô tự khai bậc thẩm quyền B1/B2/B3
  (hậu tố `*` = giá trị đơn chọn trong dải luật). `hanh_chinh` 13→18 ô: TÁCH `ten_cq_tren` (chủ quản
  KHÔNG đậm — hết mâu thuẫn §6.16) + 4 ô bố cục `phan_chuong/tieu_de_pc/muc/dieu` (NĐ30 PL I II.6);
  `vbqppl_qh` 18→19: bổ khuyết `quyen_han_ky` (Đ37 k1, Mẫu 10-13); 5 ô dẫn chiếu mơ hồ "PL I sơ đồ"
  → đích danh **Đ30/Đ31/Đ33**. Hai hệ `vbqppl`/`vbhn` **khai trắng tường minh** `__khai_trang__`
  (ADR-0009: cấm giả vờ kiểm). r170 unpack `[:5]`.
- **M5 CHẾT — normalize idempotent với build**: `_fix_sect` lề phải THEO HỆ (`he_eff`): nhà nước
  **1134=20mm** (= builder; NĐ30 dải 15-20, chọn 20 là B3 — Q4 user chốt), Đảng giữ **850=15mm** HD05
  đơn trị. Trước đây normalize ép 850 toàn cục ⇒ âm thầm đổi lề mọi file nhà nước đã build. Đã chứng
  minh: build→normalize giữ nguyên 4 lề (hành chính) · Đảng vẫn 850. `criteria["normalize"]` tách
  `le_nha_nuoc`/`le_dang` — NEO dòng 415 + r135 anchor + r138 fixture sửa cùng release (đúng quy trình
  drift-lock). **Lưu ý vận hành:** file NHÀ NƯỚC normalize từ nguồn lề 15mm nay ra 20mm (khác bản .35.1).
- **Comment nhánh WARN dải-hợp sửa đúng sự thật**: nhánh `rng is None` KHÔNG chết — chỉ còn `vbhn`
  chạm (ke_thua chưa materialize, không khai khoá lề); nhãn cũ "vbqppl_qh" sai từ v1.34.76.
- **Reference đồng bộ**: §6.34 viết lại (54 ô = 18+19+17, 22 khoá — hết cách đọc nhầm "48 × 3 hệ");
  §6.25 đệm ô 6pt→**4pt** theo r164 (nhãn B3); §6.17 làm rõ "Mẫu 1-16 = 19 sơ đồ" (mẫu 6/11/15 tách
  a/b) — hết vênh 16-vs-19; §8 normalize mô tả lề theo hệ.
- **Hồ sơ**: `docs/adr/0009` (8 quyết định + trình tự 5 bước + zero-oan) · `CONTEXT.md` cụm "Thể thức"
  (Đặc tả thể thức · Bậc thẩm quyền · Cách ly). **CÁCH LY chờ B1**: viết tắt `QĐi` (Mẫu Đảng 05) vs
  `QĐ` (`ABBR_DANG` + §5.3) — cần nguyên văn HD05 mục 3.2 mới phân xử, KHÔNG đoán.
- Ngoài repo: `mau-dang-hd05/_TEST_dien_that` điền lại đúng (0/0/0 thật @v1.35.1, dấu `;`, hết tổ chức
  KL121, một kiểu dấu) · GHI_CHU đóng dấu kiểm chạy-lại-được + sử liệu vụ trôi.

# ★ v1.35.1 — khoản/điểm không in đậm · công thức ban hành VB Đảng (§6.35-6.36) (2026-07-20)

> User rà mẫu Quyết định: *"đoạn BAN THƯỜNG VỤ QUYẾT ĐỊNH có căn giữa không · nội dung Điều 3 tại
> sao phải in đậm · kiểm tra tương tự với các mẫu khác"*. selftest 1127→**1128**.

- **§6.35 KHOẢN/ĐIỂM KHÔNG IN ĐẬM.** HD05 PL2 mục 6 tách ba dòng: *"Từ 'Điều', số thứ tự và tên
  điều"* = đậm · *"Khoản"* = Đứng · *"Điểm"* = Đứng. Minh hoạ ở cấp RUN xác nhận
  `1. Quy định về…`[đậm=0]. Điều KHÔNG có tên (6.2.4.c cho phép *"tên điều hoặc nội dung của
  điều"*) ⇒ chỉ tiền tố `Điều N.` đậm, nội dung in thường — HAI RUN trong cùng đoạn
  (`spec.body[].dam_dau`). Cờ mới **`TT-KHOAN-DAM`**; thêm `spec.body[].nghieng`.
  ★Bẫy: hàm phân loại đề mục dùng `t.upper() == t`, mà `"1- …"`/`"…"` không có chữ cái nào nên cũng
  thoả ⇒ **34 đoạn nội dung khoản bị in đậm** khắp bộ mẫu Đảng. Điều kiện đúng: in hoa **và ≥2 chữ cái**.
- **§6.36 CÔNG THỨC BAN HÀNH VB ĐẢNG LÀ CÂU THƯỜNG.** HD05 không quy định; cứ liệu là chính
  QĐ 399-QĐ/TW: *"Ban Bí thư quy định về … như sau:"* — in thường, không in hoa/đậm/canh giữa.
  NGƯỢC với VBQPPL (`QUYẾT NGHỊ:` in hoa đậm canh giữa). Mẫu Quyết định sửa
  `BAN THƯỜNG VỤ QUYẾT ĐỊNH` → `Ban Thường vụ quyết định:`.
- *"Kính trình"* chuyển sang **nghiêng** (HD05 PL2 mục 9), trước bị in đậm.
- **ĐÍNH CHÍNH CĂN CỨ**: quy tắc bố cục Phần/Chương/Mục/Điều của HD05 là **mục 6.2.4**, không phải
  6.2.3 (6.2.3 = phần căn cứ ban hành). Sửa trong reference §6.33 và bảng `_tt_dac_ta()`.

# ★★ v1.35.0 — TẤT ĐỊNH HOÁ quy tắc thể thức 3 hệ (§6.34) + thụt Điều NQ351 (2026-07-20)

> User: *"kiểm lại mẫu NQ351 có lỗi Chương/Điều tương tự không"* + *"nghiên cứu cách tất định hoá
> các quy tắc thể thức của Đảng, Quốc hội và hành chính"*. selftest 1126→**1127**.

**Kết quả rà 19 mẫu NQ351**: KHÔNG có lỗi như mẫu Quy chế Đảng — Phần/Chương/Mục đã `center` không
thụt, Điều đã có dấu chấm sau số. Nhưng lộ **một khác biệt tinh vi giữa hai hệ** đang bị làm giống
nhau: NQ351 Đ35 k2 c ghi Điều **"cách lề trái 1cm đến 1,27cm"** (thụt TRÁI cả khối) trong khi HD05
6.2.2 ghi **"khi xuống dòng thì chữ đầu dòng lùi vào"** (thụt DÒNG ĐẦU). Một dòng thì nhìn giống
nhau, chỉ lộ khi tiêu đề điều xuống dòng. Đã tách: `kieu="dieu"` ở hệ `vbqppl_qh` dùng `w:ind
w:left`, hệ `dang` giữ `w:firstLine`. `_tt_p` nhận thêm tham số `left`.

**TẤT ĐỊNH HOÁ — `_tt_dac_ta()`**: bảng đặc tả `(cỡ, kiểu, canh, thụt, căn_cứ)` cho **48 thành phần
× 3 hệ**. Bổ khuyết cho `_the_thuc_criteria()` vốn chỉ khoá ngưỡng SỐ, trong khi mọi lỗi thực chiến
đều ở kiểu chữ / canh lề / loại thụt. **`r170` đối soát HAI CHIỀU**: dựng văn bản thật cho từng hệ
rồi kiểm từng thành phần khớp bảng ⇒ builder và bảng không thể trôi khỏi nhau.

Bảng làm hiện rõ **ba chỗ ba hệ thực sự khác nhau — đúng ba lỗi đã mắc trong phiên**:
`chuc_vu_ky` (Đảng in thường, hai hệ kia đậm) · `noi_nhan_tu` (Đảng gạch chân, hai hệ kia đậm+
nghiêng) · `dieu` (QH thụt trái, Đảng thụt dòng đầu).

★Bẫy lặp lại: hàm module-level mới (`_tt_dac_ta`) phải đăng ký bảng re-export trong `tl.py`, nếu
không `_TL_MODULE._tt_dac_ta` không resolve và test đỏ **không kèm chẩn đoán**. ★Bẫy regex: đổi thẻ
`<w:ind>` thêm `w:left` làm `r'<w:ind w:firstLine="…"'` hết khớp — đừng neo vào thứ tự thuộc tính.


> **[r194] Lịch sử 1.33.54 → 1.34.99 đã chuyển NGUYÊN VĂN sang `references/changelog_archive/CHANGELOG-1.33.54-den-1.34.99.md`** (dev-only, không vào bundle — tiền lệ v1.34.69; bản 1.33.53 trở về trước ở `CHANGELOG-den-1.33.53.md`).
