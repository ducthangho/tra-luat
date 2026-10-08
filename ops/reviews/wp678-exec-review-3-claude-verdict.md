verdict: changes_requested
reviewed_sha: 0dd86c6687ff3906f67649798b65650277d34204
spec_sha256: f39091a1d2be7629a11eb53b7daf3f076ce91f701012f7093108a98e91d140cc
reviewer_provider: anthropic
reviewer_model: claude-opus-5-5 (subagent review-opus-max, tự khai)
execution_surface: claude_code_subagent
che_do: subagent_trong_phien_dieu_phoi

> TRẠNG THÁI LƯỢT: XONG (10:42Z–11:45Z 08-10-2026). Tệp ghi TĂNG DẦN; dòng `verdict` (giữ chỗ `blocked` fail-close trong lúc
> chạy) chốt sau §7 "Kết luận".
> Tóm tắt: 0 P1 · 0 P2 · 2 P3 — `a9-mien-refs-remotes-khong-co-ca` (P3, còn mở), `khoa-t218-hep-cat-cau-truc-va-nhan` (P3, còn mở);
> `phu-nhanh-da-dang-chot-lease-id-mat-rang` ĐÃ ĐÓNG. Tỷ lệ vá thật 2→3 theo lớp 1/3. HINT: `goi/HINT.patch` sha256
> `55caec39…23b8` (dry-run `patch -p0 --fuzz=0` rc=0, §1.11).

Reviewer tự khai: Claude Opus 5.5 (model id `claude-opus-5-5`, effort max), chạy như subagent trong phiên điều phối
Claude Code. KHÔNG phải codex. Không mạng, không đăng GitHub, không commit/push; `cay-kho/` chỉ đọc. Lượt thi hành 3
(VÒNG CUỐI theo quyết định chủ kho).

## 0. Tiền kiểm (đã chạy, 10:42Z)
```
$ sha256sum SPEC.md lease.yaml luot2/VERDICT.md luot2/HINT.patch
f39091a1d2be7629a11eb53b7daf3f076ce91f701012f7093108a98e91d140cc  SPEC.md
7a981529da52ba54ccf8a153af4f92f4d8ab28feae891859cb6071bf88a9748d  lease.yaml
ab8dc510391b37d4ba8c5b214856067cfc36666c3835dfa606dc954afe3af4ba  luot2/VERDICT.md
477c360a196578fcd19a7f4fe9bbf6f53ac501e36b9980ffbc593673a15c274e  luot2/HINT.patch
$ git -C cay-kho rev-parse HEAD HEAD^{tree}
0dd86c6687ff3906f67649798b65650277d34204
4d4739ecc4ff51a4a96413bb52038b6aa3e3b270
$ git -C cay-kho status --short        # rỗng, rc=0
$ wc -l diff-l2-l3.patch diff-base-head.patch     # 115 · 1464
```
Khớp PROMPT.md (spec, VERDICT/HINT lượt 2, HEAD, tree, cây sạch, số dòng hai diff); `lease.yaml` = giá trị lượt 1/lượt 2
ghi (`7a981529…748d`). ⇒ không `blocked` vì tiền kiểm. Công cụ: Python 3.11.15 / 3.12.3 / 3.13.12 (PyYAML 6.0.1,
`get_int_max_str_digits()` = 4300 cả ba), git 2.43.0, ruff 0.15.8, GNU patch 2.7.6. Thư mục làm việc `$R/w3.25nwek`
(mktemp), HOME riêng `w3.25nwek/home` (`core.abbrev 7` `--global`), `PYTHONDONTWRITEBYTECODE=1`.

## 1. Nhật ký đo (ghi tăng dần; mọi số kèm lệnh + rc thật)

### 1.1 Vòng 3 có đúng là áp NGUYÊN VĂN `luot2/HINT.patch`, chỉ tệp test không — **có** (10:44Z)
```
$ git -C cay-kho diff 7a3a2f6 0dd86c6 | sha256sum        # a8865661…75a3 = sha256 diff-l2-l3.patch
$ git -C cay-kho diff ab457c6 0dd86c6 | sha256sum        # 962c7a60…809c = sha256 diff-base-head.patch
$ git -C cay-kho diff --numstat 7a3a2f6 0dd86c6          # 61 8 ops/lease_publish_test.py   (MỘT tệp)
$ git -C cay-kho diff --numstat ab457c6 0dd86c6          # 109 19 ops/lease_publish.py · 1047 19 ops/lease_publish_test.py
$ git -C cay-kho rev-parse 0dd86c6^ 0dd86c6^^ 0dd86c6^^^ # 7a3a2f6… · f809249… · ab457c6…
$ cd w3.25nwek/kiem_hint && git -C cay-kho archive 7a3a2f6 ops/lease_publish.py ops/lease_publish_test.py | tar -x \
    && patch -p0 --fuzz=0 < luot2/HINT.patch              # PATCH_RC=0 (3 lần "patching file", 0 .rej/.orig)
ops/lease_publish.py      ap=d8079330007ab6ba 0dd86c6=d8079330007ab6ba KHOP
ops/lease_publish_test.py ap=64b5b7a7687f2841 0dd86c6=64b5b7a7687f2841 KHOP
```
Write set vẫn đúng 2 tệp; sản phẩm `0dd86c6` = `7a3a2f6` từng byte. Vì vòng 3 = chính HINT lượt 2 (cùng model với reviewer này),
mọi kết luận dưới đo lại trên `0dd86c6`, không dựa vào phần "hai chiều" của §6 lượt 2.

### 1.2 Ruff F (đa tập (tệp, code, message)) — delta ∅ (`scripts/ruff_delta.py`, log `log/ruff.log`)
`ruff check --no-cache --select F ops/lease_publish.py ops/lease_publish_test.py --output-format json` trên ba cây `git archive`:
```
nen ab457c6 rc=1 tong=11 theo_ma={'F401': 7, 'F541': 2, 'F841': 2}
l2 7a3a2f6 rc=1 tong=11 theo_ma={'F401': 7, 'F541': 2, 'F841': 2}
ung 0dd86c6 rc=1 tong=11 theo_ma={'F401': 7, 'F541': 2, 'F841': 2}
ung - nen: 0 ∅ · nen - ung: 0 ∅ · ung - l2: 0 ∅ · l2 - ung: 0 ∅
```
Khớp lời khai điều phối "ruff F delta ∅" — **có**.

### 1.3 Câu 3 — toàn suite nền vs ứng viên, hai vế dựng trong MỘT lệnh (`scripts/do_ab.sh`, log `log/ab_chinh.log`)
Một vòng lặp dựng 4 clone `--no-hardlinks` từ `cay-kho` (nền ab457c6 / ứng viên 0dd86c6 × 3.11/3.12), `checkout --detach`,
`core.abbrev 7` (repo + `.gitconfig` của HOME riêng mỗi vế), 10:50:39Z–10:50:44Z; rồi mỗi bản Python chạy song song hai vế
`env -u GITHUB_ACTOR HOME=… TMPDIR=… PYTHONDONTWRITEBYTECODE=1 PATH=<bin python>:$PATH python3 ops/lease_publish_test.py`.
10:50:44Z–11:09:14Z (log nguyên văn):
```
KQ nen 3.11 rc=0 giay=432 tong_ket=[lease_publish: 201/201 đạt; đã chạy=201, bỏ qua=0] vao=201 ra=201 QUA=201 DO=0 BO_QUA=0 at_ca=201 pyc=0 porcelain=0 stderr_dong=44
KQ ung 3.11 rc=0 giay=465 tong_ket=[lease_publish: 261/261 đạt; đã chạy=261, bỏ qua=0] vao=261 ra=261 QUA=261 DO=0 BO_QUA=0 at_ca=261 pyc=0 porcelain=0 stderr_dong=44
KQ nen 3.12 rc=0 giay=596 tong_ket=[lease_publish: 201/201 đạt; đã chạy=201, bỏ qua=0] vao=201 ra=201 QUA=201 DO=0 BO_QUA=0 at_ca=201 pyc=0 porcelain=0 stderr_dong=72
KQ ung 3.12 rc=0 giay=645 tong_ket=[lease_publish: 261/261 đạt; đã chạy=261, bỏ qua=0] vao=261 ra=261 QUA=261 DO=0 BO_QUA=0 at_ca=261 pyc=0 porcelain=0 stderr_dong=72
```
(`vao`/`ra`/`QUA` đếm dòng `>>> vao`/`<<< ra` ở ĐẦU dòng — tức cấp suite; `t125` tự chạy lại toàn suite hai lần trong tiến
trình con với tiền tố `[A]`/`[B]`, nên số dòng có tiền tố gấp ba, không tính.) **Delta ca đỏ = 0** ở cả hai bản; khớp lời
khai điều phối "261/261 ở 3.11 và 3.12; nền 201/201" — **có**. stderr: 3.11 giống hệt sau khi bỏ tiền tố clone và số dòng
(`diff` rc=0); 3.12 chỉ khác TÊN thư mục tạm ngẫu nhiên (`lp_XXXX`) ở 2 dòng, cùng 19 dòng `SyntaxWarning` (nền :2945/:4938 →
ứng viên :2947/:4941, có sẵn từ nền). Ca chậm nhất (3.11, ứng viên): `t125` 253,7 s, `t191` 89,3 s, `t139` 18,6 s — đều có từ nền.
Clone đã dọn (shutil), giữ `.out`/`.err` trong `ab_chinh/`.

### 1.4 Đột biến lượt 2 NÊU ĐÍCH DANH — chạy lại trên 0dd86c6 (3.12; `scripts/db.py` + `db_r3_ten.py`, log `log/db_ten_312.log`)
Giàn (viết mới, tham khảo `luot2/scripts` như DỮ LIỆU): mỗi đột biến một bản sao `git archive 0dd86c6 ops .github` mới trong
`w3.25nwek/mut` (cay-kho chỉ đọc), neo phải xuất hiện ĐÚNG 1 lần và băm tệp phải đổi; ca chạy bằng `scripts/chay_ca.py` nạp
CHÍNH module test của bản sao. Phân hạng: `GIET` = `TinHieuChotCa` của module **và** khung của CHÍNH ca có trong traceback
(in kèm `hàm:dòng` gọi `chot`) · `GIET_CA_KHAC` = `TinHieuChotCa` nhưng không có khung của ca · `TIN_DUNG_GIA` = ngoại lệ khác ·
`QUA`. Neo lấy nguyên từ `luot2/scripts/db_r2*.py` (đọc trước). 0 `.pyc` sau MỌI bản sao.
Đối chứng `DC` (không đột biến): **57/57 QUA** (`t218 t213 t215 t214 t219 t204 t190 t191 t216 t209 t211 t212` + 45 `t217_*`),
`t191` "13 chốt", `t216` "mẫu số=12, giết thật=12, tín dụng giả=0, sống sót=0".

| đột biến (neo lượt 2) | kết quả trên 0dd86c6 — ca chết · `hàm:dòng` gọi `chot` · đoạn đầu thông điệp |
|---|---|
| L1a repr() dựng sẵn TRONG try | **GIET** `t218` :12256 "bí danh lồng: repr phải cắt theo cấu trúc, không chạm lá; được …list [[[[[['x', 'x'…" |
| L1b reprlib nới hạn mức | **GIET** `t218` :12256 (cùng vế) |
| L1c bỏ try, chỉ reprlib | **GIET** `t218` :12242 "hàm chung: int lớn phải Chan(8) có trần, được NEM ValueError" |
| L1e nhãn D8 luôn `sai kiểu` | **GIET** `t218` :12272 "D8: nhãn phải tách sai kiểu (int) / sai dạng (chuỗi) như D7" |
| L1f câu `CHAN [12]` cũ | **GIET** `t218` :12266 "D7: câu CHAN [12] không được gọi mọi lease_id lỗi là `sai kiểu`" |
| L1g đảo nhãn | **GIET** `t218` :12263, `t213` :12070, `t215` :12115 |
| L2a = R02b `if not bo_qua_han:` | **GIET** `t219` :11919 "`lease_id: true`, hết hạn=False: phải rc=8 … được rc=0" |
| L2b / L2b2 / L2b3 (miễn khi hết hạn, ba cách đọc hạn) | **GIET** `t219` :11919 "`lease_id: true`, hết hạn=True: … được rc=0" (+ `t190`/`t191` chết vì lý do vô can, như lượt 2 ghi) |
| **L2b4** (miễn khi `bo_qua_han` VÀ hết hạn, đọc hạn an toàn) | **GIET** `t219` :11919 "`lease_id: true`, hết hạn=True: … được rc=0" — 4 ca kia QUA |
| L2c (không phải str) · L2d (là str) | **GIET** `t219` :11919 (`true` / `'co khoang trang'`, hết hạn=False) |
| L2e D1 chỉ khi có tệp | **GIET** `t219` :11919, `t204` :11892 |
| **L2f** (list/dict) | **GIET** `t219` :11919 "`lease_id: [wp-x]`, hết hạn=False" |
| L3a bỏ `refs/remotes` | **GIET** 3 ca: `…_chi_o_refs_remotes`, `…_remote_khong_phai_origin`, `…_ref_thuong_remotes_HEAD` (qua `_a9_chot` :12452, rc=0 thay 1) |
| L3b bỏ `refs/heads` | GIET 28 ca |
| **L3c** chỉ `refs/remotes/origin` | **GIET** đúng 1 ca: `t217_a9_sai_kieu_chi_o_remote_khong_phai_origin` (:12452 "được rc=0") |
| L3d glob `refs/remotes/*` | GIET 3 ca remote |
| **L3e** bỏ leaf HEAD thường dưới `refs/remotes` | **GIET** đúng 1 ca: `t217_a9_sai_kieu_chi_o_ref_thuong_remotes_HEAD` (:12452 "được rc=0") |
| L3f `refs/remotes/o` | GIET 3 ca remote |
| L3g THÊM `refs/tags` (nới miền) | QUA 45/45 — nới, không phải hẹp; tags ngoài miền SPEC A9 (như lượt 2) |

Mọi đột biến lượt 2 nêu đích danh (L1a L1b L1c L1e L1f L1g · L2a L2b4 L2c L2d L2f · L3a L3c L3d L3e) chết bằng `TinHieuChotCa` của
đúng ca, đúng vế; `GIET_CA_KHAC` = 0, `TIN_DUNG_GIA` = 0 trên ca đích. ⇒ **không lớp nào TÁI PHÁT**.

### 1.4b Đột biến lượt 2 nêu đích danh ở 3.11.15 và 3.13.12 (`db_r3_ten_nhanh.py`: chỉ ca đích quyết định, bỏ t190/t191; log `log/db_ten_nhanh_311.log`, `_313.log`)
3.11: **giống hệt 3.12 từng ô** (mọi L1* GIET `t218` cùng dòng; mọi L2* GIET `t219` :11919, L2b4 ở hàng `true … hết hạn=True`, L2f ở
`[wp-x]`; L3a/L3d/L3f GIET 3 ca remote, L3c đúng `…_remote_khong_phai_origin`, L3e đúng `…_ref_thuong_remotes_HEAD`; L3g QUA).
3.13: như 3.11 trừ **L1c QUA** — `reprlib` 3.13 không ném ở `int` lớn, nên "bỏ `try`" tương đương ở 3.13 (lượt 2 đã ghi; CI chạy
3.12 nên vẫn giết). 23/23 bản sao 0 `.pyc` mỗi bản Python.

### 1.5 Đột biến lượt 1 nêu đích danh H04–H09 (đọc `luot1/scripts/db_hint.py` bằng `ast.literal_eval`, KHÔNG exec; 3.12, log `log/db_l1_312.log`)
H04 repr thô ở hàm chung ⇒ GIET `t218` :12242 · H05 nhãn luôn `sai kiểu` ⇒ GIET `t218` :12263 · H06 `return repr(...)` ⇒ GIET
`t218` :12242 · H07 D7 repr thô ⇒ GIET `t218` :12260 ("NEM ValueError") · H08 D8 ⇒ GIET `t218` :12268 · H09 D9 ⇒ GIET `t218` :12247.
(`t213`, `t215` QUA ở cả sáu — đúng, ca đích là `t218`.) R02b = L2a, A11 = L3a ở §1.4.

### 1.6 Lớp 1 — tự liệt kê trục hạn × `bo_qua_han` × kiểu `lease_id` (`db_r3_moi.py`, log `log/db_moi_L2_312.log`; API `scripts/do_api_l2.py`, log `log/api_l2.log`)
Giàn có một lỗi đã sửa giữa chừng: `chay_ca.py` bản đầu không đặt `ops/` vào `sys.path` (chạy `python ops/lease_publish_test.py`
thì có), nên `t207` (import `bash_nen`) ra `TIN_DUNG_GIA ModuleNotFoundError` ở cả 8 đột biến — lỗi GIÀN, log giữ ở
`log/db_moi_L2_312_gian_thieu_syspath.log`; chạy lại sau khi sửa. Mọi ca đích ở §1.4/§1.5 và hai chiều §1.11 không import mô-đun
cạnh (đối chứng 57/57 và 54/54 QUA), nên các kết quả ấy không đổi.
Đột biến (mỗi cái chèn `if not (bo_qua_han and <đk>):` trước D1), ca đích nhanh `t219 t204 t216 t174(×2) t207 t178 t205 t206`
(t190/t191 để cho lượt toàn suite): **cả 8 QUA 9/9** —
L2g `datetime` · L2h `bytes` (`!!binary`) · L2i `set` (`!!set`) · L2ghi (ba kiểu gộp) · L2j `None`/`""` · L2k chuỗi chỉ trắng ·
L2m hạn hỏng dạng · L2n hết hạn quá 2 giờ (t219 dựng hết hạn đúng 1 giờ: `khi_truoc(1)`).
Hậu quả API, `kiem(lease, None, None, bo_qua_han=True)`, ba bản Python cho bảng giống hệt (md5 `125e2886…` cả ba), trích 3.12
(`L` = thông điệp có `lease_id`):

| `lease_id` (YAML) | kiểu | hạn | ứng viên | L2g | L2h | L2i | L2j | L2k | L2m | L2n |
|---|---|---|---|---|---|---|---|---|---|---|
| `2026-09-29T10:00:00Z` | datetime | còn 4h / hết 1h / hết 3h / hỏng | Chan8L ×4 | **rc0 rc0 rc0** Chan8 | Chan8L | Chan8L | Chan8L | Chan8L | Chan8L ×3, Chan8 | Chan8L Chan8L **rc0** Chan8L |
| `!!binary d3AtMQ==` | bytes | như trên | Chan8L ×4 | Chan8L | **rc0 rc0 rc0** Chan8 | Chan8L | Chan8L | Chan8L | …Chan8 ở hỏng | **rc0** ở hết 3h |
| `!!set {a, b}` | set | như trên | Chan8L ×4 | Chan8L | Chan8L | **rc0 rc0 rc0** Chan8 | Chan8L | Chan8L | …Chan8 ở hỏng | **rc0** ở hết 3h |
| `null` · `''` | NoneType · str | mọi hạn | Chan8L | Chan8L | Chan8L | Chan8L | **Chan8L** (BAT_BUOC chặn trước) | Chan8L | Chan8L | Chan8L |
| `'   '` | str | còn/hết 1h/hết 3h | Chan8L | … | … | … | Chan8L | **rc0 ×3** | Chan8L | **rc0** ở hết 3h |
| `yes` · `[wp-x]` | bool · list | hết 3h | Chan8L | … | … | … | … | … | … | **rc0** |
| `wp-ok-1` | str | còn/hết/hỏng | rc0 rc0 rc0 Chan8 | như ứng viên ở mọi cột |

Đọc: L2j TƯƠNG ĐƯƠNG (`BAT_BUOC` chặn `None`/`""` với thông điệp có `lease_id`); L2m tương đương ở MỨC rc (hạn hỏng ⇒
`_doc_han` vẫn `Chan(8)`, chỉ đổi thông điệp). L2g/L2h/L2i/L2k/L2n đổi rc 8 → 0 ở API. Ở CLI cả năm bị che, đọc từ mã: người gọi DUY NHẤT của
`bo_qua_han=True` là nhánh đã-có-dấu của `kiem_github` (:1280); nhánh ấy chỉ tới được khi `_do_dau_da_dang` ném `RC_DA_DANG`, mà
nó gọi `_tien_kiem_mien_dang` (D2, :1174) và `_kiem_comment_da_co` (D3, :885) TRƯỚC — cả hai ném `Chan(8)` với mọi `lease_id`
không hợp lệ, bị nuốt, rồi `kiem()` KHÔNG `bo_qua_han` chạy D1 ⇒ rc=8. Tức D1 trên đường `bo_qua_han` là lớp phòng thủ thứ ba
(đúng như L2b4 lượt 2). Phân hạng ở §2.

### 1.7 Lớp 2 — tự liệt kê ref tượng trưng / không tượng trưng và tiền tố (`db_r3_moi.py`, log `log/db_moi_L13_312.log`; hậu quả `scripts/do_a9_symref.py`, log `log/a9_symref.log`)
Trên 45 ca `t217_*` (3.12): **L3h** `if symref: continue` (bỏ MỌI ref tượng trưng) **QUA 45/45** · **L3i** `if ten ==
"refs/remotes/origin/HEAD": continue` (bỏ theo TÊN, không xét symref — thành ngữ quen của script) **QUA 45/45** · L3k1 glob
`refs/remotes/*/*` GIET đúng `t217_a9_sai_kieu_chi_o_ref_thuong_remotes_HEAD` · L3k2 glob `refs/heads/*` GIET đúng
`t217_a9_sai_kieu_chi_o_ref_thuong_topic_HEAD`. Chỉ khối A9 (:12279–:12890) gọi helper (`rg` 38 dòng, min 12279 max 12890), và
`--quet-a9` không có người gọi nào ngoài tệp test (`rg -F quet-a9` toàn kho), nên 45 ca này là mọi ca có thể giết L3h/L3i.
Hậu quả (kho tạm, `--quet-a9` qua CLI, bản helper = `git archive 0dd86c6` + neo duy nhất, 3.12):
```
# S1: for-each-ref = refs/heads/alias->refs/tags/t | refs/heads/main-> | refs/tags/t->
# S2: for-each-ref = refs/heads/alias->refs/heads/bad | refs/heads/bad-> | refs/heads/main->
# S3: for-each-ref = refs/heads/main-> | refs/remotes/upstream/HEAD->refs/remotes/upstream/xa | refs/remotes/upstream/xa->
# S4: for-each-ref = refs/heads/main-> | refs/remotes/origin/HEAD->
ung  S1: rc=1 so_ref=2 refs=['refs/heads/alias', 'refs/heads/main'] loi=[('lease_id=True', ['refs/heads/alias'])]
ung  S4: rc=1 so_ref=2 refs=['refs/heads/main', 'refs/remotes/origin/HEAD'] loi=[('lease_id=True', ['refs/remotes/origin/HEAD'])]
L3h  S1: rc=0 so_ref=1 refs=['refs/heads/main'] loi=[]                       <- báo SẠCH, lease `on` chỉ tới được qua alias
L3h  S2: rc=1 … loi=[('lease_id=True', ['refs/heads/bad'])]                  <- mất `refs/heads/alias` trong danh sách refs
L3i  S3: rc=1 so_ref=3 … loi=[('lease_id=True', ['refs/remotes/upstream/HEAD', 'refs/remotes/upstream/xa'])]  <- nới (vô hại)
L3i  S4: rc=0 so_ref=1 refs=['refs/heads/main'] loi=[]                       <- báo SẠCH, `origin/HEAD` THƯỜNG mang `on`
```
(ứng viên S2/S3 và L3h S3/S4, L3i S1/S2 giống ứng viên — log đầy đủ.) SPEC §7 A9 *Miền*: "chỉ bỏ ref có leaf HEAD VÀ là symbolic
ref; ref thường có hậu tố `/HEAD` vẫn phải quét" — S1 (ref tượng trưng tên KHÁC HEAD) và S4 (`…/HEAD` thường) đều trong miền
phải quét. Sản phẩm (helper) đúng ở cả hai; ca khoá thì không có điểm nào ở hai chỗ ấy.

### 1.8 Lớp 3 — tự liệt kê mọi trường thông điệp `t218` khoá (`db_r3_moi.py`, `db_r3_gop.py`, log `log/db_moi_L13_312.log`, `log/db_gop_L1mn_312.log`, `log/db_gop_L1op_312.log`; chi phí `scripts/do_repr_cost.py`, log `log/repr_cost_312.log`)
Ca đích `t218 t213 t215 t214` (3.12), mọi đột biến dưới **QUA 4/4**:
- **L1h** `_repr_an_toan`: `hien = repr(gia_tri)` rồi `if len(hien) > tran: hien = r.repr(gia_tri)` (trong `try`) — "ngắn thì
  repr, dài thì reprlib": đầu ra KHÔNG có lá `'x'` nên qua vế vòng 3, nhưng `repr()` đầy đủ vẫn được DỰNG.
- **L1i** `_ = len(repr(gia_tri))` rồi reprlib (tính bên lề).
- **L1k** `_nhan_lease_id_sai` (nhãn D7/D8) dùng `repr(gia_tri)[:120]` có `try` thay `_repr_an_toan`.
- **L1l** `_lease_id_hien_thi` (D9) như trên.
- **L1m** / **L1n** đường in D7 (:2348) / D8 (:2197) gọi thẳng nhãn + `repr()[:120]` có `try`, vòng qua `_nhan_lease_id_sai`.
- **L1o** / **L1p** hai đường in D9 của `con-tro-treo` (:2389 `CON_TRỎ_TREO`, :2393 `CON_TRỎ_GỢI_Ý`) như trên, vòng qua `_lease_id_hien_thi`.
- L1j nhãn: `list` thành `sai dạng` (`isinstance(gia_tri, (str, list))`) — chèn nhánh theo kiểu, xem §2.
Chi phí đo (3.12, `RLIMIT_AS` 3 GiB, mỗi đột biến một tiến trình; `la_x` = có lá `'x'` trong đầu ra):
```
ung   repr/nhan/d9/hople k=6..9  0.000s  len=121/130/146/210  la_x=False  rss_max=25MiB
L1h   repr  k=6 0.074s · k=7 0.622s · k=8 5.309s rss 273MiB · k=9 68.033s rss_max=2181MiB   len=121 la_x=False
L1h   d9    k=8 10.009s (hai lần dựng: _lease_id_quet + hiển thị)   hople k=8 5.148s          la_x=False
L1i   repr  k=8 4.569s rss 272MiB   hople k=8 4.915s                                         la_x=False
L1k   nhan  k=8 4.253s rss 272MiB   la_x=True        L1l  d9 k=8 4.321s rss 273MiB  la_x=True
L1a   repr  k=8 3.727s rss 273MiB   la_x=True  (đối chiếu: đột biến lượt 2, nay chết ở vế `'x'`)
```
(k=9 của L1h đo khi máy đang chạy 3–5 tiến trình khác; lượt 2 đo L1a k=9 43,190 s / 2187 MiB.) Vế `'x'` của vòng 3 chỉ đo
HÌNH DẠNG đầu ra của MỘT đường (thông điệp `_lease_id_hop_le` với bom); bom không đi qua D7/D8/D9 ở `t218`.

### 1.9 Câu 2 — ca vòng 3 thêm/sửa có xanh giả, phụ thuộc thứ tự/nền, chậm bất thường không — **không** (đo được ở Linux)
- Bỏ qua lặng lẽ: diff vòng 3 không thêm `return`/`BoQuaNen`/nhánh "không thấy thì bỏ qua" nào (`grep` các dòng `+` của
  `diff-l2-l3.patch`: 0); vòng lặp `t219` không thể rỗng (hằng); mọi vế mới đi qua `chot`. `chay_buoc_` 32 = 32, `^@ca` 259 → 261.
- Thứ tự: `scripts/db_r3_dc.py` (log `log/dc_v3.log`) — 7 ca (`t219`, `t218`, 3 ca remote A9, đối chứng HEAD tượng trưng,
  `topic/HEAD`) chạy xuôi ×3 và NGƯỢC ×1 trên bản sao 0dd86c6 ở 3.11.15 / 3.12.3 / 3.13.12: **28/28 QUA mỗi bản**; cộng toàn
  suite (§1.3) — tức đứng sau 258 ca khác.
- Nền: đo được 3 bản Python trên Linux; Windows/`nt` KHÔNG ĐO ĐƯỢC (lease cấm Windows CI). Ca mới chỉ dùng `git
  symbolic-ref`/`update-ref`/`checkout`, không nhánh theo `os.name`.
- Thời gian (toàn suite §1.3, ứng viên): `t219` 0,156 s (3.11) / 0,256 s (3.12); `t218` 0,386 / 0,488 s; hai ca A9 mới 0,282–0,406 s
  — ngang các ca A9 cũ cùng lượt (0,30–0,40 s). Trên 7a3a2f6 (3.12, `dc_v3.log`) `t219` 0,07–0,18 s (nửa số hàng). Không bất thường.
- Docstring/chú thích vòng 3 khai lịch sử đo của lượt 2 (259/259 trên 7a3a2f6; 43 s / 2,2 GiB; "3 ref thay vì 5") — khớp
  `luot2/VERDICT.md` §1.8. Câu "trần phải đến từ CẮT THEO CẤU TRÚC (không chạm lá)" (docstring `t218` :12225) rộng hơn phép đo
  của vế :12256 (chỉ đo đầu ra) — thuộc lớp 3, §2.

### 1.10 Toàn suite trên đột biến còn sống (`scripts/do_full_db.py`, clone `--no-hardlinks` mới mỗi mục, dựng MỌI mục trong MỘT vòng lặp trước khi chạy, 3.12, `core.abbrev 7`, HOME/TMPDIR riêng; log `log/full_gopA.log`, `log/full_gopB.log`)
```
DUNG G2-L3h-L3i       numstat=[1  1  ops/lease_publish_test.py]  ok=True 11:14:04Z
DUNG G3-L1h-L1k-L1l   numstat=[15 3  ops/lease_publish.py]       ok=True 11:14:06Z
DUNG G3b-L1m-L1n      numstat=[9  2  ops/lease_publish.py]       ok=True 11:14:08Z
KQ G2-L3h-L3i     rc=0 giay=684 tong_ket=['lease_publish: 261/261 đạt; đã chạy=261, bỏ qua=0'] vao=261 ra=261 DO=0 pyc=0 porcelain=1
KQ G3b-L1m-L1n    rc=0 giay=685 tong_ket=['lease_publish: 261/261 đạt; đã chạy=261, bỏ qua=0'] vao=261 ra=261 DO=0 pyc=0 porcelain=1
KQ G3-L1h-L1k-L1l rc=0 giay=685 tong_ket=['lease_publish: 261/261 đạt; đã chạy=261, bỏ qua=0'] vao=261 ra=261 DO=0 pyc=0 porcelain=1
```
(11:14:02Z–11:25:32Z, ba lượt song song; `porcelain=1` = đúng tệp đột biến.) G2 = `if symref or ten == "refs/remotes/origin/HEAD":`
(hợp của L3h và L3i: bỏ một tập ref LỚN hơn mỗi cái — mọi ca A9 chỉ đòi có/không có ref cụ thể, và 45/45 ca A9 QUA với từng cái
riêng ở §1.7). G3 = L1h + L1k + L1l, G3b = L1m + L1n (neo độc lập, gộp được).
Lượt thứ hai (11:25:38Z–11:36:16Z, `log/full_gopB.log`):
```
DUNG G1-L2g-L2h-L2i numstat=[2 1 ops/lease_publish.py] ok=True · DUNG G3c-L1o-L1p numstat=[9 2 ops/lease_publish.py] ok=True
KQ G3c-L1o-L1p    rc=0 giay=628 tong_ket=['lease_publish: 261/261 đạt; đã chạy=261, bỏ qua=0'] vao=261 ra=261 DO=0 pyc=0 porcelain=1
KQ G1-L2g-L2h-L2i rc=0 giay=634 tong_ket=['lease_publish: 261/261 đạt; đã chạy=261, bỏ qua=0'] vao=261 ra=261 DO=0 pyc=0 porcelain=1
```
⇒ mọi đột biến còn sống dùng làm căn cứ lớp (L3h, L3i, L1h, L1k, L1l, L1m, L1n, L1o, L1p) sống **toàn suite 261/261**; G1 (quan sát
lớp 1, §3) cũng 261/261.

### 1.11 HINT lượt 3 — dựng, dry-run, áp thật, hai chiều (`scripts/dung_hint.py`, `db_r3_hai_chieu.py`; log `log/hint_dryrun.log`, `log/hai_chieu_31{1,2,3}.log`)
`dung_hint.py`: s0 = `git show 0dd86c6:ops/lease_publish_test.py` → s1 (nhóm 1) → s2 (nhóm 2), mỗi neo đúng 1 lần; dấu chéo ngược
dựng bằng `chr(92)` SAU khi phân tích cú pháp, rồi đo `repr()` trên tệp đã ghi: các dòng mới `"lease_id: on\n"`,
`"KHÔNG_XÁC_ĐỊNH\tlease_id sai kiểu "`, `"CON_TRỎ_TREO\t<…"`, `"[vung_duoc_phep_cham]\nghi_chu: …\n"` mang ĐÚNG MỘT dấu chéo như
dòng cũ :12262/:12508. Bản nháp đầu (sha256 `4c80e211…`, chưa có vế D9 qua CLI) đã thay bằng bản cuối; log hai chiều của bản nháp
giữ tên `*_HINT_nhap1.log` / `*_HINT_tron_*.log` và KHÔNG dùng làm bằng chứng.
```
# HINT sha256 55caec390d086e8985f5085de2f333f84afd32fb829b48a40289b60c694f23b8 · cây: git archive 0dd86c6 ops/lease_publish.py ops/lease_publish_test.py · cwd = gốc bản sao
$ patch -p0 --fuzz=0 --dry-run < goi/HINT.patch
checking file ops/lease_publish_test.py
checking file ops/lease_publish_test.py
DRYRUN_RC=0
bam truoc=[d8079330007ab6ba 64b5b7a7687f2841 ] sau=[d8079330007ab6ba 64b5b7a7687f2841 ] KHONG_DOI
patching file ops/lease_publish_test.py          # áp THẬT trên bản sao khác
patching file ops/lease_publish_test.py
APPLY_RC=0 · TRUNG s2 TUNG BYTE · SAN PHAM KHONG DOI · orig_rej=0 · at_ca=263 chay_buoc_=32
```
Ruff F tệp test trước/sau HINT: 9 = 9, thêm ∅ bớt ∅ (F401 ×7, F541 ×2). `chay_buoc_` 32 = 32 ⇒ không đổi `mong`/`SO_BO_QUA`/`t193`.
Hai chiều (mỗi đột biến một bản sao `git archive 0dd86c6 ops .github` + `patch -p0 --fuzz=0` HINT rồi neo đột biến): đối chứng bản
đã vá **54/54 QUA** (`t218 t219` + 47 `t217_*` + `t213 t215 t214 t204 t216`) ở 3.11, 3.12, 3.13. Đột biến (ca chết · dòng `chot`):

| đột biến | 3.11 / 3.12 / 3.13 |
|---|---|
| L3h bỏ MỌI ref tượng trưng | GIET `t217_a9_sai_kieu_chi_qua_ref_tuong_trung_khong_phai_HEAD` (`_a9_chot` :12502, "được rc=0") — chỉ ca ấy |
| L3i bỏ theo tên `origin/HEAD` | GIET `t217_a9_sai_kieu_chi_o_origin_HEAD_khong_tuong_trung` — chỉ ca ấy |
| G2 (L3h ∪ L3i) | GIET cả hai ca mới |
| L3a / L3d · L3c · L3e (lượt 2) | GIET 4 ca remote · `…_remote_khong_phai_origin` · `…_origin_HEAD_khong_tuong_trung` + `…_ref_thuong_remotes_HEAD` |
| L1h · L1i · L1k · L1l | GIET `t218` :12276 — nhãn vế lần lượt `_repr_an_toan` · `_repr_an_toan` · `_nhan_lease_id_sai` · `_lease_id_hien_thi` ("lá sâu bị chạm 1 lần") |
| L1m · L1n (đường in D7 · D8) | GIET `t218` :12306 "D7/D8: … lá sâu bị chạm 2 lần" |
| L1o · L1p (hai đường in D9) | GIET `t218` :12321 "D9: … lá sâu bị chạm 1 lần" |
| G3 · G3b · G3c | GIET :12276 · :12306 · :12321 |
| L1a L1b · L1c · L1e · L1f · L1g (lượt 2) | GIET :12258 · :12244 (3.13: L1c QUA — tương đương, §1.4b) · :12293 · :12287 · :12284 |

**24/24 đột biến GIET bằng `TinHieuChotCa` đúng ca, đúng vế ở 3.11 và 3.12; 23/24 ở 3.13** (L1c tương đương); `GIET_CA_KHAC` 0,
`TIN_DUNG_GIA` 0; 0 `.pyc` ở mọi bản sao. Mỗi đường của lớp 3 có vế riêng (đột biến gỡ từng đường chết ở vế mang tên đường ấy),
tức không phải bộ tương đương.

### 1.12 Toàn suite trên bản đã áp HINT (`do_full_db.py … HINT`, clone `--no-hardlinks` 0dd86c6 + `patch -p0 --fuzz=0`; log `log/full_gopB.log`, `log/full_hint311.log`)
```
DUNG HINT: HINT PATCH_RC=0 'patching file ops/lease_publish_test.py\npatching file ops/lease_publish_test.py'
DUNG HINT HEAD=0dd86c6… numstat=[86 1 ops/lease_publish_test.py] ok=True
KQ HINT (3.12.3) rc=0 giay=634 tong_ket=['lease_publish: 263/263 đạt; đã chạy=263, bỏ qua=0'] vao=263 ra=263 DO=0 pyc=0 porcelain=1
KQ HINT (3.11.15) rc=0 giay=411 tong_ket=['lease_publish: 263/263 đạt; đã chạy=263, bỏ qua=0'] vao=263 ra=263 DO=0 pyc=0 porcelain=1
```
(3.12: 11:25:42Z–11:36:16Z; 3.11: 11:36:19Z–11:43:10Z; HINT sha256 `55caec39…23b8`, mtime 11:18:00Z — trước mọi lượt cuối.)
stderr 3.12 bản đã vá so ứng viên (`ab_chinh/ung-3.12.err`): 72 = 72 dòng, cùng 19 `SyntaxWarning`, khác duy nhất tiền tố clone ở
một dòng (`diff` sau khi chuẩn hoá đường dẫn). Ca mới/sửa trong lượt 3.12: `t219` 0,143 s, `t218` 0,690 s, hai ca A9 mới 0,323 /
0,303 s. `t70`, `t193`, `t191` ("13 chốt"), `t216` (12/12) QUA trong cả hai lượt.

## 2. Ba lớp lượt 2 — trạng thái sau vòng 3

Tiêu chí đếm một đột biến sống vào lớp (nói thẳng để chủ kho bác được): nó phải mô phỏng một thay đổi mã có lý do tự nhiên
trên đúng đường đang khoá — rút gọn điều kiện, thành ngữ quen, đổi chỗ lời gọi, "repr nếu ngắn". Đột biến CHÈN một nhánh
riêng cho một kiểu hiếm, một chuỗi con của `str` hay một hằng thời lượng mà mã không hề có thì KHÔNG tính: không mẫu hữu hạn
nào đóng được nó, và nó không đổi lớp tương đương nào của chốt. Những đột biến ấy vẫn được ĐO và ghi ở §3.

| lớp lượt 2 (P lượt 2) | trạng thái sau vòng 3 | căn cứ đo |
|---|---|---|
| `phu-nhanh-da-dang-chot-lease-id-mat-rang` (P2) | **ĐÃ ĐÓNG** | §1.4: L2a, L2b, L2b2, L2b3, **L2b4**, L2c, L2d, L2e, **L2f** đều GIET `t219` :11919 đúng hàng (họ L2b ở `hết hạn=True`, L2f ở `[wp-x]`), ở 3.11 và 3.12 (3.13: §1.4b). D1 là `isinstance(str)` + `LEASE_ID.fullmatch`, tức ba lớp tương đương (không phải `str` · `str` sai dạng · hợp lệ); `t219` nay phủ cả ba × hai trạng thái hạn. Đột biến còn sống trên trục đã liệt kê (§1.6: L2g/L2h/L2i chèn miễn trừ riêng cho `datetime`/`bytes`/`set`, L2k cho chuỗi chỉ trắng, L2n cho "hết hạn quá 2 giờ") đều là loại CHÈN NHÁNH ở trên ⇒ §3; L2j tương đương, L2m tương đương ở mức rc. |
| `a9-mien-refs-remotes-khong-co-ca` (P3) | **CÒN MỞ** — cùng cơ chế, qua đường mới (không TÁI PHÁT: L3c/L3e chết) | §1.4: L3c GIET đúng `…_remote_khong_phai_origin`, L3e GIET đúng `…_ref_thuong_remotes_HEAD` (3.11, 3.12); §1.7: **L3h** (`if symref:` — bỏ MỌI ref tượng trưng, rút gọn tự nhiên "symref chỉ là bí danh") và **L3i** (bỏ theo TÊN `refs/remotes/origin/HEAD` — thành ngữ quen) sống 45/45 ca A9 và toàn suite (§1.10), và báo sạch rc=0 trên kho có lease sai kiểu chỉ tới được qua `refs/heads/alias` → `refs/tags/t` (L3h) hoặc chỉ ở `refs/remotes/origin/HEAD` THƯỜNG (L3i) — cả hai trong miền SPEC A9 phải quét; helper hiện tại quét đúng (rc=1). |
| `khoa-t218-hep-cat-cau-truc-va-nhan` (P3) | **CÒN MỞ** — cùng cơ chế, qua đường mới (không TÁI PHÁT: L1a/L1b/L1e/L1f chết) | §1.4: L1a/L1b GIET vế `'x'` :12256, L1e GIET :12272, L1f GIET :12266 (3.11, 3.12); §1.8: **L1h** ("repr đầy đủ nếu ngắn, reprlib nếu dài") sống `t218 t213 t215 t214` và toàn suite (§1.10; L1i "tính bên lề" chỉ đo trên 4 ca đích) — đầu ra không có lá nên qua vế `'x'`, nhưng `repr()` đầy đủ vẫn được dựng: bom 8 cấp 5,3 s / 273 MiB, 9 cấp 68 s / 2,2 GiB (ứng viên 0,000 s / 25 MiB); L1k/L1l (nhãn D7/D8, D9 dùng `repr()[:120]`+`try`) và L1m/L1n/L1o/L1p (bốn đường in D7, D8, D9×2 vòng qua helper) cũng sống — `t218` chỉ đưa bom qua MỘT đường (thông điệp `_lease_id_hop_le`). Sản phẩm hiện tại cắt theo cấu trúc ở mọi đường (§1.8 dòng `ung`). |

**Tỷ lệ vá thật 2→3.** Theo lớp: **1/3 = 33 %** (lớp 1 đóng; lớp 2, lớp 3 còn mở qua đường không ai chỉ). Theo đột biến lượt 2
nêu đích danh: **15/15** chết bằng `TinHieuChotCa` đúng ca, đúng vế (L1a L1b L1c L1e L1f L1g · L2a L2b4 L2c L2d L2f · L3a L3c L3d L3e;
L1c tương đương ở 3.13 như lượt 2 đã ghi). Theo đột biến lượt 1: H04–H09, R02b, A11 vẫn chết (§1.5). **Không lớp nào TÁI PHÁT;
không lỗi MỚI do vòng 3** (§1.9). Hai lớp còn mở đều là **ca test hẹp hơn hợp đồng**, KHÔNG phải lỗi hành vi của mã: helper A9
quét đúng S1/S4 (§1.7), `_repr_an_toan`/nhãn/D9 cắt theo cấu trúc ở mọi đường (§1.8). Hình dạng: lần thứ hai liên tiếp, bản vá
(của chính reviewer cùng model, lượt 2) đúng và CÓ RĂNG ở chỗ nó phủ, nhưng mỗi ca khoá vẫn dựng một điểm của miền — đúng bài
học "VÁ ĐÚNG CHỖ ĐƯỢC CHỈ RỒI BỎ SÓT ĐƯỜNG THỨ BA"; HINT §6 lần này tự liệt kê mọi đường đã đo được (lớp 3: thân `_repr_an_toan` + 6 đường vòng
D7/D8/D9, cộng thông điệp hàm chung; lớp 2: 2 đường) và cho MỖI đường một vế riêng (đột biến gỡ từng đường chết ở vế mang tên
đường ấy, §1.11).

## 3. Đo được, KHÔNG xếp lớp (để chủ kho tự cân)
- **Lớp 1 — đột biến chèn nhánh còn sống** (§1.6, toàn suite G1 ở §1.10): miễn D1 dưới `bo_qua_han` riêng cho `datetime`
  (`2026-09-29T10:00:00Z`), `bytes` (`!!binary`), `set` (`!!set`) — ba kiểu SafeConstructor còn lại mà `t219` không có hàng —
  đổi rc 8 → 0 ở API; ở CLI bị D2/D3 che. Muốn đóng nốt thì rẻ: thêm ba hàng vào `t219` và một phép kiểm KIỂU sau YAML cho từng
  hàng (biến `_kieu` của vòng lặp hiện KHÔNG được đọc, nên `t219` không tự chứng minh hàng `[wp-x]`/`{x: 1}` thật sự ra
  `list`/`dict` — với PyYAML 6.0.1 thì có: `yaml.safe_load` ở 3.11/3.12/3.13 cho `[wp-x]` list, `{x: 1}` dict,
  `2026-09-29T10:00:00Z` datetime, `!!binary d3AtMQ==` bytes, `!!set {a, b}` set, `2026-09-29` date). Không đưa vào HINT vì không tính là lớp (§2).
- L2k (chuỗi chỉ trắng) và L2n (hết hạn quá 2 giờ; `t219` dựng đúng một mốc 1 giờ): cùng loại chèn nhánh/hằng số.
- L1j (nhãn: `list` thành `sai dạng`) sống `t218 t213 t215 t214`: nhãn chỉ được khoá ở `int`/`bool`/`str`; chèn nhánh theo kiểu.
- L3g (THÊM `refs/tags`) sống 45/45: nới miền, không phải hẹp (như lượt 2).
- Mục ngoài phạm vi lượt 2 §3 (repr/`str()` thô ở `da_bi_thay_the`, `packet_issue`, sổ thu hồi, `granted_by`; `con-tro-treo` với bom
  ở MỌI trường; địa chỉ bộ nhớ trong thông điệp 3.13): vòng 3 không đổi sản phẩm (numstat), KHÔNG đo lại ở lượt này.
- Giàn của reviewer có một lỗi đã sửa (thiếu `ops/` trong `sys.path`, §1.6) — lỗi giàn, không phải của ứng viên.

## 4. Bảng lớp (lượt 3)

| slug | P | hành vi mã hay ca test | một câu |
|---|---|---|---|
| `a9-mien-refs-remotes-khong-co-ca` | P3 | **ca test** hẹp hơn hợp đồng (helper A9 đúng) | Vòng 3 giết đúng L3c/L3e, nhưng bỏ MỌI ref tượng trưng (L3h) hoặc bỏ theo TÊN `refs/remotes/origin/HEAD` (L3i) vẫn sống 45/45 ca A9 và toàn suite, và báo sạch rc=0 khi lease sai kiểu chỉ tới được qua ref tượng trưng tên khác HEAD hay qua `origin/HEAD` THƯỜNG — hai điểm trong miền SPEC A9 "chỉ bỏ ref có leaf HEAD VÀ tượng trưng" mà không ca nào dựng. |
| `khoa-t218-hep-cat-cau-truc-va-nhan` | P3 | **ca test** hẹp hơn hợp đồng (sản phẩm đúng) | Vế `'x'` của vòng 3 chỉ đo HÌNH DẠNG đầu ra ở MỘT đường (thông điệp `_lease_id_hop_le`): "dựng `repr()` đầy đủ, ngắn thì dùng, dài thì reprlib" (bom 9 cấp 68 s / 2,2 GiB) và sáu đường D7/D8/D9 vòng qua `_repr_an_toan` bằng `repr()`+`try` đều sống `t218` và toàn suite. |

Lớp `phu-nhanh-da-dang-chot-lease-id-mat-rang`: **ĐÃ ĐÓNG** (§2) — không còn trong bảng.

### Lớp `a9-mien-refs-remotes-khong-co-ca` (P3, CÒN MỞ)
- Biểu hiện: helper `ops/lease_publish_test.py` :12342–:12344 (`if ten.rsplit("/", 1)[-1] == "HEAD" and symref: continue`) — đúng;
  ca khoá :12466–:12548: điểm tượng trưng DUY NHẤT là `refs/remotes/origin/HEAD` → `refs/heads/main` (đối chứng, phải BỎ); điểm
  `…/HEAD` thường là `refs/heads/topic/HEAD` và `refs/remotes/origin/topic/HEAD` — không ca nào có ref tượng trưng tên KHÁC HEAD,
  không ca nào có `refs/remotes/origin/HEAD` THƯỜNG.
- Phép đo: §1.7 (L3h, L3i QUA 45/45 ở 3.12; S1/S4 rc=0 sạch), §1.10 (G2 = L3h ∪ L3i, toàn suite).
- Vì sao P3 (không P2): cần đầu vào hiếm (symref tạo tay; nhánh máy chủ tên `HEAD`); lượt quét kho thật chạy trên mirror
  (`refs/heads/*`, không symref) nơi hai đột biến không đổi kết quả.
- Hướng vá (HINT nhóm 1): hai ca, mỗi đường một chốt — `t217_a9_sai_kieu_chi_qua_ref_tuong_trung_khong_phai_HEAD`
  (`refs/heads/alias` → `refs/tags/t`) và `t217_a9_sai_kieu_chi_o_origin_HEAD_khong_tuong_trung`.

### Lớp `khoa-t218-hep-cat-cau-truc-va-nhan` (P3, CÒN MỞ)
- Biểu hiện: `ops/lease_publish_test.py` :12253–:12256 (vế `'x'` chỉ trên thông điệp `_lease_id_hop_le` với bom); D7 :12257–:12266 và
  D8 :12267–:12274 chỉ dùng `int` lớn và chuỗi sai dạng, D9 :12246–:12247 chỉ `int` lớn — bom không đi qua đường nào trong ba.
  Docstring :12225 "trần phải đến từ CẮT THEO CẤU TRÚC (không chạm lá)" — phép đo chỉ nói về ĐẦU RA.
- Phép đo: §1.8 (L1h L1i L1k L1l L1m L1n L1o L1p QUA 4/4 ca đích; giá L1h), §1.10 (G3 = L1h+L1k+L1l, G3b = L1m+L1n, G3c = L1o+L1p,
  toàn suite).
- Vì sao P3: sản phẩm hiện tại đúng ở mọi đường (0,000 s / 25 MiB với bom 9 cấp); hỏng chỉ khi có thay đổi sau này và khi ấy
  là fail-close (chậm/hết bộ nhớ trên đường chẩn đoán), không cấp nhầm quyền.
- Hướng vá (HINT nhóm 2): lính canh sâu hơn `maxlevel` (`__repr__` đếm số lần bị chạm) đi qua TỪNG đường: bốn hàm
  (`_repr_an_toan`, `_nhan_lease_id_sai`, `_lease_id_hien_thi`, `_lease_id_hop_le`) gọi trực tiếp, và ba đường CLI
  (`ai-dang-giu --du-bao` cho D7+D8, `con-tro-treo` cho D9×2) với `_quet_lease_toan_kho` được bọc để thay `lease_id` bằng cấu
  trúc mang lính canh (khôi phục trong `finally`).

## 5. KHÔNG ĐO ĐƯỢC
- Windows / nền `nt` thật; CI GitHub; máy chủ GitHub live; comment cấp quyền #678 và danh tính người ký (#566).
- Lượt quét A9 trên kho thật và `git fsck --full`: KHÔNG chạy lại (vòng 3 không đổi helper A9 — numstat chỉ tệp test, và ở tệp
  test vòng 3 chỉ thêm hai ca; mirror của executor không có trong `$R`).
- Model/effort thực sự phục vụ lượt review này (cấu hình tự khai Claude Opus 5.5 `claude-opus-5-5` effort max).
- Python 3.14 (không có trong container): vế `'x'` và lính canh dựa vào hành vi `reprlib` theo `maxlevel` — đo 3.11/3.12/3.13.
- Toàn suite trên đột biến chỉ chạy ở 3.12 (đột biến ca đích chạy ở 3.11/3.12/3.13). Giá k=9 của L1h (68 s) đo khi máy đang
  tải 3–5 tiến trình; không đo cô lập.
- Công cụ ngoài kho có thể phân tích chuỗi thông điệp (scratch của phiên khác) — vòng 3 không đổi chuỗi sản phẩm nào.

## 6. HINT (`goi/HINT.patch`, 123 dòng, sha256 `55caec390d086e8985f5085de2f333f84afd32fb829b48a40289b60c694f23b8`, 2 nhóm, chỉ sửa `ops/lease_publish_test.py`, đường dẫn repo-relative không tiền tố) — phương án nợ kế nhiệm
- Nhóm 1 `# lop: a9-mien-refs-remotes-khong-co-ca` (P3), 1 hunk +35: hai ca `t217_a9_sai_kieu_chi_qua_ref_tuong_trung_khong_phai_HEAD`
  và `t217_a9_sai_kieu_chi_o_origin_HEAD_khong_tuong_trung` chèn ngay sau `t217_a9_sai_kieu_chi_o_ref_thuong_remotes_HEAD`.
- Nhóm 2 `# lop: khoa-t218-hep-cat-cau-truc-va-nhan` (P3), 3 hunk trong `t218`, +51 −1 (cộng nhóm 1 +35 ⇒ +86 −1 = numstat §1.12): docstring (thay dòng cuối, thêm 2 dòng); khối lính canh `_LinhCanh`
  (`__repr__` đếm số lần bị chạm) đặt ở độ sâu 5 (> `maxlevel` 2) và gọi qua bốn hàm; khối CLI bọc `_quet_lease_toan_kho` để thay
  `lease_id` bằng cấu trúc mang lính canh rồi chạy `ai-dang-giu ops/x.md --du-bao` (D7 + D8) và `con-tro-treo` (D9 ×2), khôi
  phục trong `finally`. Không ca mới/sửa nào dùng `_chay_buoc_dang*`.
- Dry-run / áp thật / ruff / hai chiều: §1.11 (`DRYRUN_RC=0`, `APPLY_RC=0`, 24/24 đột biến chết đúng vế ở 3.11 và 3.12, 23/24 ở 3.13).
- Toàn suite trên bản đã vá: §1.12.
- Phạm vi: sản phẩm vòng 3 = 7a3a2f6 (numstat), nên bảng liệt kê bằng AST của `luot2/VERDICT.md` §1.6 (mọi chỗ định dạng `lease_id` của
  lease) vẫn đúng: thông điệp hàm chung (:336), nhãn D7 (:2348) và D8 (:2197) qua `_nhan_lease_id_sai`, D9 (:2389, :2393) qua
  `_lease_id_hien_thi`; ngoài phạm vi SPEC §5 là :1420 (sổ thu hồi). HINT đặt lính canh ở cả bốn hàm VÀ ở cả bốn đường in qua CLI,
  nên một `repr()` đầy đủ chèn ở bất kỳ chỗ nào trong các đường ấy (kể cả "tính bên lề") đều chạm lính canh.

## 7. Kết luận
`changes_requested` — **0 P1 · 0 P2 · 2 P3**: `a9-mien-refs-remotes-khong-co-ca` (P3, CÒN MỞ — đường mới cùng cơ chế) ·
`khoa-t218-hep-cat-cau-truc-va-nhan` (P3, CÒN MỞ — đường mới cùng cơ chế). `phu-nhanh-da-dang-chot-lease-id-mat-rang` **ĐÃ ĐÓNG**.
Tỷ lệ vá thật 2→3 theo lớp **1/3 = 33 %**; đột biến lượt 2 nêu đích danh **15/15** chết đúng ca, đúng vế; không lớp nào TÁI PHÁT;
không lỗi MỚI do vòng 3.

Kiểm lời khai của phiên điều phối: suite 261/261 ở 3.11 và 3.12 trên 0dd86c6 — **có** (§1.3); nền 201/201 — **có** (§1.3); ruff F
delta ∅ — **có** (§1.2); vòng 3 = áp NGUYÊN VĂN `luot2/HINT.patch`, chỉ tệp test — **có** (§1.1).

Cả hai lớp còn mở là **ca test hẹp hơn hợp đồng**, không phải lỗi hành vi: helper A9 quét đúng ref tượng trưng tên khác HEAD và
`origin/HEAD` thường (S1/S4 rc=1, §1.7); sản phẩm cắt theo cấu trúc ở mọi đường chẩn đoán (0,000 s / 25 MiB với bom 9 cấp, §1.8).
Hỏng chỉ khi có thay đổi mã về sau, và khi ấy lớp 2 thành âm giả của cổng TRƯỚC LAND trên đầu vào hiếm, lớp 3 thành chậm/hết bộ
nhớ fail-close trên đường chẩn đoán — không cấp nhầm quyền. Theo quyết định chủ kho (vòng cuối), đây là hai ứng viên "chấp nhận
kèm nợ" hay checkpoint; `goi/HINT.patch` là phương án nợ kế nhiệm: 2 nhóm, chỉ tệp test, dry-run `patch -p0 --fuzz=0` rc=0,
toàn suite **263/263** ở 3.11 và 3.12, **24/24** đột biến chết đúng vế ở 3.11/3.12 (23/24 ở 3.13, L1c tương đương).
Mức assurance của lượt này: `review_deferred` (subagent cùng họ executor, và là cùng model đã viết HINT lượt 1 lẫn lượt 2 mà vòng
2 và vòng 3 áp nguyên văn); land vẫn đòi `human_audited` của chủ kho.
