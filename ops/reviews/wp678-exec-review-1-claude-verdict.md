verdict: changes_requested
reviewed_sha: f80924940c706626902090269a4f81b7e5b12da6
spec_sha256: f39091a1d2be7629a11eb53b7daf3f076ce91f701012f7093108a98e91d140cc
reviewer_provider: anthropic
reviewer_model: claude-opus-5-5 (subagent review-opus-max, tự khai)
execution_surface: claude_code_subagent
che_do: subagent_trong_phien_dieu_phoi

> TRẠNG THÁI LƯỢT: XONG (08:1xZ 08-10-2026). Tệp ghi TĂNG DẦN; dòng `verdict` được chốt sau mục 8 "Kết luận".
> Tóm tắt: 0 P1 · 3 P2 · 0 P3 — `thong-diep-lease-id-sai-dung-repr-tho`, `phu-nhanh-da-dang-chot-lease-id-mat-rang`,
> `a9-mien-refs-remotes-khong-co-ca`. HINT: `goi/HINT.patch` (dry-run `patch -p0 --fuzz=0` rc=0, §7).

Reviewer tự khai: Claude Opus 5.5 (model id `claude-opus-5-5`, effort max), chạy như subagent trong phiên
điều phối Claude Code. KHÔNG phải codex. Không mạng, không đăng GitHub, không commit/push; `cay-kho/` chỉ đọc.

## 0. Tiền kiểm (đã chạy)
```
$ sha256sum SPEC.md lease.yaml BAO_CAO_executor.md diff-base-head.patch
f39091a1d2be7629a11eb53b7daf3f076ce91f701012f7093108a98e91d140cc  SPEC.md
7a981529da52ba54ccf8a153af4f92f4d8ab28feae891859cb6071bf88a9748d  lease.yaml
42795ab19d3e3e8e1d02e0e3187b47bf15162dde8aaeac49221c946e5571726a  BAO_CAO_executor.md
d1cb3ce03b2b8b65ffa67a42db33874c64e823bed2feb8d90f1f6f9bda2b3b15  diff-base-head.patch
rc=0
$ git -C cay-kho rev-parse HEAD HEAD^{tree}
f80924940c706626902090269a4f81b7e5b12da6
ab354ef1c0c5b5aac80716999b10d039e851d420
$ git -C cay-kho status --short      # rỗng, rc=0
$ wc -l diff-base-head.patch          # 1274
```
Khớp PROMPT.md ở cả 5 điểm (spec sha đủ 64 ký tự, lease `7a981529…`, báo cáo `42795ab1…`, HEAD, tree) ⇒ không `blocked` vì tiền kiểm.

## 1. Nhật ký đo (ghi tăng dần; mọi số kèm lệnh + rc thật)

Thư mục làm việc: `$R/w.TUbSq9` (mktemp). Hai cây xuất `git archive` (không `.git`): `w.TUbSq9/cay/nen` (ab457c6),
`w.TUbSq9/cay/ung` (f809249). Băm tệp xuất: nền `lease_publish.py` sha256 `dbf3b905…8f67`, test `273ebd3f…8008`
(khớp spec); ứng viên `lease_publish.py` `efed431c…5b11` (blob `cba5e94`), test `829178d9…de73`.
Công cụ: Python 3.11.15 / 3.12.3 / 3.13.12, PyYAML 6.0.1 (cả ba), git 2.43.0, ruff 0.15.8, shellcheck, actionlint có mặt.

### 1.1 Write set
`git -C cay-kho diff --numstat ab457c6 HEAD` ⇒ `86 19 ops/lease_publish.py` · `902 18 ops/lease_publish_test.py`, đúng 2 tệp;
`git diff ab457c6 HEAD | sha256sum` = `d1cb3ce0…3b15` = băm `diff-base-head.patch` (diff `-` không lệch byte nào).

### 1.2 Ruff F (đa tập (tệp, code, message))
`ruff check --no-cache --select F ops/lease_publish.py ops/lease_publish_test.py --output-format json` trên hai cây:
rc=1 cả hai (có lỗi nền); nền 11, ứng viên 11; thêm ∅, bớt ∅ ⇒ **delta 0**. Tập nền: 2 F841 (`executor_surface`,
`executor_transport` của wp709) + 7 F401 + 2 F541 ở tệp test.

### 1.3 A8 tĩnh — script riêng của reviewer `w.TUbSq9/scripts/tinh_a8.py` (không dùng tinh.py của executor)
`python3.X -B tinh_a8.py cay/nen cay/ung`, rc=0 ở 3.11.15, 3.12.3, 3.13.12, cùng kết quả:
- nền: 201 ca, D 13, R 14, chỉ-lồng `{t70}`, G 14, G−D `{t202}`, D−G ∅, sổ 12, D−sổ `{t199}`.
- ứng viên: 256 ca, D 14 (thêm `t207`), R 15, **chỉ-lồng `{t70}`**, G 15, **G−D `{t202}` = nền**, D−G ∅, sổ 13, D−sổ `{t199}`.
- (S) r13: tổng lần chuỗi con `chay_buoc_` nền 29 → ứng viên 31; phần HƠN = 2 × `Name.id` `_chay_buoc_dang_that`
  trong thân `t207` ⇒ ĐƯỢC PHÉP; **0 lần mới ĐỎ**.
`python3.X ops/lease_publish_test.py --chi-ca=t70_` và `--chi-ca=t193_` trên cây ứng viên: rc=0, `1/1` ở cả 3.11, 3.12, 3.13.
⇒ khớp từng số lời khai executor (BAO_CAO §2 hàng A8).

### 1.4 Suite A/B — hai vế dựng trong MỘT lệnh (`w.TUbSq9/scripts/do_ab.sh`, log `w.TUbSq9/ab.log`)
Một vòng lặp dựng 4 clone `--no-hardlinks` từ `cay-kho` (nền/ứng viên × 3.11/3.12), `checkout --detach`, `core.abbrev 7`
(repo + `--global` trong HOME riêng), rồi chạy `env -u GITHUB_ACTOR HOME=… TMPDIR=… PYTHONDONTWRITEBYTECODE=1 PATH=<bin python>:$PATH
python3 ops/lease_publish_test.py`, nền và ứng viên song song từng bản Python.

| | Python 3.11.15 (07:17:22Z–07:25:02Z) | Python 3.12.3 (07:25:03Z–07:33:14Z) |
|---|---|---|
| nền ab457c6 | **201/201**, rc=0, bỏ qua 0, vào 201 = ra 201, 0 `.pyc`, `status --porcelain --ignored` 0 | **201/201**, rc=0, như bên trái |
| ứng viên f809249 | **256/256**, rc=0, bỏ qua 0, vào 256 = ra 256, 0 `.pyc`, porcelain 0 | **256/256**, rc=0, như bên trái |

`^@ca` đếm tĩnh 201 / 256 = số ca chạy. Delta ca đỏ = **0** ở cả hai bản ⇒ khớp lời khai executor (§2 bảng nghiệm thu).
Dòng in của `t191`: nền `14 chốt của kiem() đều PHU…`, ứng viên `13 chốt…` (3.11 và 3.12) — xem §1.6 và §5 câu 3.
`t216`: `catalog đột biến wp678: mẫu số=12, giết thật=12, tín dụng giả=0, sống sót=0`.
SyntaxWarning 3.12 (lời khai executor §6.1) đo lại: `compile()` dưới 3.12 bắt đúng `invalid escape sequence` ở ứng viên
:2947 `\s`, :4941 `\d`; nền :2945, :4938 — khớp.

### 1.5 Đột biến ĐỘC LẬP (bộ của reviewer, không dùng mut_*.py của executor)
Dụng cụ: `w.TUbSq9/scripts/do_dot_bien.py` + đặc tả `scripts/db_ung.py`; mỗi đột biến = `cp -al` cây ứng viên rồi thay
`ops/lease_publish.py` bằng inode MỚI (tệp gốc không đổi — có `assert`), nạp CHÍNH module test của cây ấy
(`scripts/chay_ca.py`, nên `_nap_cong`, CLI và tiến trình con đều thấy bản đột biến), phân hạng theo LỚP ngoại lệ:
GIET = `TinHieuChotCa` của module · TIN_DUNG_GIA = ngoại lệ khác · QUA. Python 3.11.15, `-B`, 0 `.pyc` sau mỗi đột biến.
Đối chứng xanh trước: 18/18 ca đích QUA trên cây KHÔNG đột biến (lượt đầu lộ lỗi của chính bộ chạy — thiếu `ops/`
trên `sys.path`, `bash_nen` không nạp — đã sửa rồi chạy lại). Log: `w.TUbSq9/dot_bien_311.log`.

| đột biến | ca đích | kết quả |
|---|---|---|
| R01 gỡ HẲN D1 (`pass`) | t204 | GIET |
| R03 gỡ HẲN D2 (= `L` của #677) | t205 · t178 · t195 · t196 · t197 | GIET t205 · QUA ở bốn ca kia (khớp lời khai `L` sống ở t178/t195–t197) |
| R04 D3 thô (không chốt) | t206 | GIET |
| R05 D4 thô | t208 | GIET |
| C01 D1 `str()` rồi regex | t204 | GIET |
| C02 hàm chung `str()` | t204 t205 t206 t208 t214 t215 | GIET cả sáu (t209–t212 QUA vì hàm trả giá trị THÔ, không phải `str()`; t213 chết `TypeError` — ngoài catalog) |
| C03 D2 `(str,int)` | t205 | GIET |
| C04 D3 `str()` | t206 | GIET |
| C05 D5 toán hạng cũ / C06 D5 toán hạng quét | t211 / t212 | GIET đúng ca của nó; ca anh em QUA |
| C07 D6 lease mới / C08 D6 toán hạng quét | t210 / t209 | GIET đúng ca của nó; ca anh em QUA |
| C09 D7 `str()` khoá người giữ | t213 | GIET (rc=11, `NGƯỜI_GIỮ 1: True` — đúng hình dạng nền) |
| C10 D8 check thô / C11 D8 ai-dang-giu `str()` | t214 / t215 | GIET / GIET |
| X01 hàm chung bỏ `isinstance` (TypeError) | 11 ca | GIET ở t206 (qua `_MaVang`), TIN_DUNG_GIA ở 10 ca còn lại |
| X02 `_lease_id_quet` ép `str()` | t209 t211 t212 t213 t215 | GIET cả năm |
| X03 `_lease_id_quet` nuốt MỌI ngoại lệ | như X02 | QUA cả năm — không ca nào phân biệt `except Chan` với `except Exception` (lớp 1, §4) |
| K01 gỡ D1 + D3 | t207 | QUA (D6 ở đầu `_kiem_bia_mo` vẫn chặn) — khớp lời khai |
| K02 gỡ D1 + D3 + D6 | t207 | GIET: `rc=0`, 2 GET, 0 POST, "đã đăng trước đó — bỏ qua" — khớp lời khai |
| N00 sản phẩm = bản NỀN ab457c6 | t204–t215 + t207 | GIET cả 12 ⇒ mọi ca A1–A7 ĐỎ trên nền đúng chữ "ĐỎ khi" |
| R02 miễn D1 CHỈ ở nhánh đã-đăng (`if not bo_qua_han:`) | t204 · t190 · t191 | QUA cả ba (`t191` vẫn in "13 chốt") — xem §1.6, §5 câu 3 |
| K03 R02 + gỡ D2 + D3 `str()` + D6 `str()` | t190 · t191 | GIET t190: `(vi) lease_id sai ký tự, ĐÃ đăng, CÓ tep: mong rc=8, nhận rc=9.` |
| K04 gỡ D2 + D3 + D6, GIỮ D1 | t190 · t191 | QUA cả hai (D1 trên nhánh đã-đăng tự chặn) |

Catalog `t216` của executor (12 đột biến) dựng lại độc lập ở C01–C11 + C02: cùng kết luận 12/12 giết thật.

### 1.6 Câu 3 (t191 "14 chốt" → "13 chốt") — số đo
- `t191` định nghĩa chốt bằng `_la_chot` (ứng viên `ops/lease_publish_test.py` :9536–9542): CHỈ `raise Chan(...)` hoặc lời
  gọi tên `_kiem_*`/`_doc_*`. D1 nền là `raise Chan` trực tiếp trong `kiem()` (nền :1023) ⇒ được đếm; D1 ứng viên là lời gọi
  `_lease_id_hop_le(...)` (:1056) ⇒ KHÔNG được đếm. Đó là toàn bộ chênh 14 → 13.
- Đổi tên THUẦN (không đổi hành vi) `_lease_id_hop_le(` → `_kiem_lease_id_hop_le(` (8 chỗ) rồi chạy `t191` (log
  `w.TUbSq9/doi_ten.log`): **GIET** — `chốt của kiem() KHÔNG được t190 phủ ở nhánh đã-có-dấu: ['_kiem_lease_id_hop_le
  (dòng 1056, cột 4): KHONG_CHAM']`. ⇒ `t191` xanh ở ứng viên CHỈ nhờ tên hàm; nếu nhìn thấy D1 nó báo KHONG_CHAM.
- Đầu dò không đổi hành vi (`scripts/do_dau_do_t190.py`, ghi mỗi lời gọi `kiem(..., bo_qua_han=True)`): hàng
  `(vi) lease_id sai ký tự, ĐÃ đăng` của `t190` vào nhánh đã-có-dấu **1** lần ở nền, **0** lần ở ứng viên (các hàng khác
  giữ nguyên: `wp579-thu` 17, `KIEM-treo` 1, `MOI` 2). Lý do: D2 (`_tien_kiem_mien_dang`) nay chặn chuỗi sai regex TRƯỚC
  `_kiem_comment_da_co`, `_do_dau_da_dang` nuốt `Chan(8)` và đi đường chưa-đăng.
- Đột biến R02 (miễn D1 CHỈ khi `bo_qua_han`): `t204`, `t190`, `t191` QUA. Toàn suite với R02 (neo của catalog bị đổi
  chữ): 255/256, ca đỏ DUY NHẤT `t216` vì neo văn bản `D1-str-roi-regex` không còn — tạo tác của cách viết đột biến, không
  phải phát hiện hành vi; đo lại bằng R02b giữ nguyên neo ⇒ 256/256 (§1.8).
- Đối xứng ở NỀN: cùng đột biến (`if not bo_qua_han and not LEASE_ID.fullmatch(lease_id):`) trên sản phẩm nền ⇒ **GIET
  bởi CẢ HAI**: `t190` `(vi) lease_id sai ký tự, ĐÃ đăng, CÓ tep: mong rc=8, nhận rc=9.` và `t191` `phải thấy đúng MỘT
  chốt đã được miễn (chốt hạn), thấy [('raise Chan', 1023, 8), ('raise Chan', 1055, 8)]`.
- R02 QUAN SÁT ĐƯỢC ở API (`scripts/do_api_r02.py`, `_kiem_sach(mod, lease, None, None, True)`): `lease_id: yes`,
  `1_000`, `'co khoang trang'` ⇒ ứng viên `Chan 8`, R02 **QUA** — trái chú thích chính `kiem()` :1084 *"`bo_qua_han` bỏ
  ĐÚNG MỘT chốt — chốt HẠN, và chỉ nó"*. Qua `kiem_github` thì bị D2/D3 che.
- Tính chất ĐẦU-CUỐI vẫn được đo: K03 (R02 + gỡ D2 + D3 `str()` + D6 `str()`) ⇒ `t190` GIET `nhận rc=9`; K04 (gỡ D2+D3+D6,
  GIỮ D1) ⇒ `t190` QUA.
- Spec r17: `grep -c 't19[01]' SPEC.md` = 1 dòng, và dòng ấy (:60) chỉ nói wp709 thêm hàng `provider` vào `t190`; `t191`
  0 lần. Docstring/chú thích `t190` vế (vi) ở ứng viên (:9414–9415, :9491–9494) vẫn khai hàng `lease_id sai ký tự` là
  fixture phủ chốt regex `lease_id` (C2) ở nhánh đã-đăng và `t191` "đòi t190 phủ từng cái" — không còn đúng. BAO_CAO
  của executor không nhắc `t191` lần nào.

### 1.7 Câu 4 (D7, lease hỏng mà HẾT HẠN) — số đo (`scripts/do_d7.py`, kho tạm `_wp678_kho`, CLI thật, 3.11)
| ca (chạm `ops/x.md`) | nền | ứng viên |
|---|---|---|
| a HẾT_HẠN, `lease_id: yes` | rc=0, `HẾT_HẠN True`, `NGƯỜI_GIỮ 0` | rc=12, `KHÔNG_XÁC_ĐỊNH … sai kiểu True` |
| b HẾT_HẠN, thiếu `lease_id` | rc=0, `HẾT_HẠN <thiếu lease_id>` | rc=12, `… sai kiểu None` |
| c CÒN_HẠN, thiếu `lease_id` | rc=11, `NGƯỜI_GIỮ 1: <thiếu lease_id>` | rc=12 |
| d HẾT_HẠN, chuỗi hợp lệ (đối chứng) | rc=0 | rc=0 (giống hệt) |
| e HẾT_HẠN `yes` + CÒN_HẠN hợp lệ `wp-ok-2` | rc=11, `NGƯỜI_GIỮ 1: wp-ok-2` | rc=12 (in dòng `CÒN_HẠN wp-ok-2` nhưng không in `NGƯỜI_GIỮ`) |

Trên snapshot kho thật (bản sao `--mirror --no-hardlinks` của `x678/mirror.git` của executor, 481 nhánh, rồi clone
thường): `ai-dang-giu ops/lease_publish.py` và `… ops/lease_publish_test.py` ⇒ nền và ứng viên **stdout giống hệt từng
byte** (78 và 126 dòng), rc=11 cả bốn, `NGƯỜI_GIỮ 1: wp678-r17-g1-claude`, 0 dòng `KHÔNG_XÁC_ĐỊNH`.

### 1.8 R02b toàn suite + A9 độc lập + các lời khai khác
- R02b = R02 nhưng giữ nguyên neo văn bản của catalog `t216` (`    if not bo_qua_han:\n        _lease_id_hop_le(...)  # wp678 D1…`):
  `scripts/do_full_mut.py … R02b-… /usr/bin/python3.11` ⇒ **`lease_publish: 256/256 đạt`, rc=0**, 0 `.pyc`; `t191` in "13 chốt",
  `t216` 12/12. ⇒ đột biến SỐNG TOÀN SUITE ở ứng viên (ở nền thì `t190` + `t191` giết, §1.6).
- A9 — 20 đột biến độc lập trên CHÍNH helper (`scripts/db_a9.py`, `db_a9_b.py`; log `dot_bien_a9.log`, `a9_b.log`,
  `a11_all.log`); đối chứng xanh 42/42 `t217_*` QUA trên cây gốc. GIET đúng ca bằng `TinHieuChotCa`: bỏ băm blob · truthiness
  `thay_the_cho` · truthiness `da_bi_thay_the` · nhận list cho `da_bi_thay_the` · siết chuỗi trắng `thay_the_cho` · bỏ
  `--no-replace-objects`+biến · bỏ MỌI `/HEAD` · không bỏ HEAD tượng trưng · bỏ `.yml` · bỏ kiểm stderr · đọc lại TÊN ref
  (race) · bỏ miền `refs/heads` · bỏ `ops/leases_retired` · nuốt lỗi parse · regex A9 trôi · rc 2→1 · nuốt "không phải ánh
  xạ" · nuốt "thiếu ID" · nhận `int` (19/20). **SỐNG: A11 bỏ `"refs/remotes"` khỏi `for-each-ref` — QUA cả 42/42 ca.**
  Hậu quả A11 đo được: kho tạm có lease `lease_id: yes` CHỈ ở `refs/remotes/origin/x` ⇒ ứng viên rc=1 `['lease_id=True']`,
  A11 **rc=0, so_ref 1, so_blob 0, errors []**; clone THƯỜNG của snapshot kho thật ⇒ ứng viên 482 ref / 594 blob, A11 **1 ref /
  132 blob, rc=0**.
- A9 kho thật (bản sao snapshot `x678/mirror.git` của executor; KHÔNG phải máy chủ live): `git fsck --full` 07:34:36Z–07:34:44Z
  rc=0, output rỗng (0 byte); `python3.11 -B ops/lease_publish_test.py --quet-a9 <bản sao>` 07:34:44Z–07:34:55Z rc=0, stderr rỗng,
  sha1, 481 ref, 594 blob, 594 cặp, `leases` 594/594, `lich_su` 0/0, 594 đủ ID, `kieu {str: 594}`, errors 0 — khớp BAO_CAO §4.
  Map ref→OID của bản sao = nguồn (`diff` rỗng). Đếm độc lập (`scripts/dem_lease.py`): `refs/heads` ⇒ 594 blob yaml / 598 blob
  mọi tệp dưới `ops/leases*`; `heads+tags` ⇒ 597 yaml (3 blob chỉ qua tag `luu-tru/*`, cả 3 `str`); `heads+pull` ⇒ 605.
  Con số 597 của lease (05:3xZ, 480 ref): cách đếm của bên soạn `KHÔNG ĐO ĐƯỢC` từ đây.
- `check` 132 tệp `ops/leases/*.yaml` của ab457c6, nền vs ứng viên: trong clone CÓ `.git` (`ab/ung-3.11/repo`) ⇒ giống hệt 132/132,
  rc=8: 127, rc=10: 5 (khớp BAO_CAO §5). Lượt đầu của tôi trên cây xuất KHÔNG `.git` cho rc=8: 92, rc=12: 35, rc=10: 5 — tạo tác
  rig (`_kiem_bia_mo` cần kho git), vẫn giống hệt nền/ứng viên. Lease đang sống (`lease.yaml` + `SPEC.md` đặt vào bản sao):
  nền và ứng viên cùng rc=0 `ĐĂNG ĐƯỢC … khớp băm f39091a1d2be`.
- Lời khai §1 "`grep lease_id | grep 'str('` chỉ còn dòng chú thích :1056" — đúng (1 dòng, :1056).

## 2. Trục Spec acceptance (chữ r17)

| tiêu chí | kết luận | căn cứ đo (mục §1) |
|---|---|---|
| write set chỉ 2 tệp | **có** | §1.1 `--numstat` 2 dòng; diff = `diff-base-head.patch` từng byte |
| D1–D9 đi qua MỘT hàm (Q1/Q2) | **có** cho mọi đường đọc `lease_id` thành danh tính; **không** cho thông điệp chẩn đoán (lớp 1) | §3 liệt kê AST; §1.5 C01–C11, X02 |
| A1 (t204) | **có** | C01, R01, N00 GIET; đối chứng `'yes'`/`!!str yes`/`wp-ok-1` rc=0 (fixture qua luật danh tính wp709) |
| A2 (t178 + t205) | **có** | C03, R03 GIET t205; `L` QUA t178/t195–t197 đúng điều A2 dự liệu |
| A3 (t206 đơn vị + t207 biên) | **có** | C04/R04 GIET t206; N00 ⇒ t207 ĐỎ `rc=0`, 2 GET, 0 POST, "đã đăng trước đó"; đối chứng `fresh-id` 1 POST; K01 QUA, K02 GIET |
| A4 (t208) | **có** | R05 ⇒ thân ``**Lease `True`**`` |
| A5 (t209–t212) | **có** | C05–C08 mỗi đột biến giết đúng ca của nó, ca anh em QUA; R01 (gỡ D1) ⇒ t209–t212 vẫn QUA (không đi qua D1) |
| A6 (t213) | **có** | C09 ⇒ rc=11 `NGƯỜI_GIỮ 1: True` |
| A7 (t214, t215; nhánh "tới được") | **có** | C10, C11 GIET |
| A8 tĩnh: delta 0 (3.11 & 3.12) · ruff F delta 0 · `t70`/`t193` 1/1 · chỉ-lồng `{t70}` · G−D = nền · (S) 0 ĐỎ | **có** | §1.2–§1.4 |
| A9 helper + 42 ca + quét kho thật + fsck tiên quyết | **có** (snapshot) | §1.8 |
| A9 "ĐỎ khi: gỡ TỪNG nghĩa vụ ⇒ ca của nó ĐỎ" | **không** — vế miền `refs/remotes/*` | lớp 3 |
| A10 (ba hạng, `TinHieuChotCa`) | **có** | t216 12/12; bộ độc lập C01–C11 cùng kết luận |
| §6 mục 1 "trả `str` hoặc ném `Chan(RC_NOI_DUNG)`" | **không** cho `int` vượt giới hạn chuyển chuỗi | lớp 1 |
| §6 mục 7 docstring phải nói sự thật mới | **không** cho docstring/chú thích `t190` vế (vi) | lớp 2 |

## 3. Trục Standards + liệt kê đường đọc `lease_id` (câu 2)

Liệt kê bằng AST (`scripts/liet_ke_lease_id.py`, mọi hằng `"lease_id"`, mọi tham chiếu tuple khoá chứa nó, mọi thao tác trên
CẢ dict lease) + `rg -n lease_id` (58 dòng ứng viên / 38 nền). Mọi đường tạo DANH TÍNH đều qua `_lease_id_hop_le` (:1056 D1,
:1151 D2, :862 D3 trước `_doc_gh`, :1269 D4, :793 D6, :2126 D8) hoặc `_lease_id_quet` (:777/:782 D5, :804 D6, :2172 D8, :2322
D7, :2351 D9). Đường đọc gián tiếp còn lại và phán: `kiem()` :1016 `lease.get(k) in (None, "")` qua `BAT_BUOC` — so sánh trên
giá trị thô TRƯỚC D1 nhưng chỉ quyết "thiếu trường", ra `Chan(8)` cùng lớp/rc, không tạo danh tính ⇒ không phải lỗi;
`_cac_nhac_mo_ho` duyệt scalar có `isinstance(str)`; `yaml.safe_dump(lease)` ở D4 chạy SAU chốt; :2283/:2298 in sau `kiem()`;
:877/:886/:2142/:2146/:2150/:2333/:2338/:2340 dùng giá trị ĐÃ qua hàm. `rg 'lease_id' | rg 'str('` ⇒ chỉ chú thích :1056.
Đường còn lỗi: bốn chỗ `repr` thô (:313, :2174, :2325, :2352) và `_lease_id_quet` chỉ bắt `Chan` (:325) ⇒ lớp 1.
Cùng cơ chế nhưng NGOÀI phạm vi (§5: sổ thu hồi, trường khác; S2 — chỉ báo): `kiem_ban_ghi_thu_hoi` :1397 `{lease_id!r}`,
:1438 `{dich!r}`; `lenh_ai_dang_giu` :2334 `{lease.get('da_bi_thay_the')!r}`.

## 4. Bảng lớp

| slug | P | một câu |
|---|---|---|
| `thong-diep-lease-id-sai-dung-repr-tho` | P2 | Thông điệp chẩn đoán dựng `repr()` THÔ của `lease_id` chưa hợp lệ: `int` YAML vượt giới hạn chuyển chuỗi (`0x`+4000 hex, `safe_load` không ném) làm hàm chung và bản quét ném `ValueError`, CLI `check`/`body`/`ai-dang-giu`/`ai-dang-giu --du-bao` (cả đường dẫn KHÔNG liên quan) ra traceback rc=1 thay vì `Chan(8)`/`KHÔNG_XÁC_ĐỊNH`; bom bí danh 591 byte ⇒ stderr 2,79 triệu ký tự; chuỗi đúng kiểu sai dạng bị gắn nhãn "sai kiểu". |
| `phu-nhanh-da-dang-chot-lease-id-mat-rang` | P2 | Chốt D1 thành lời gọi `_lease_id_hop_le` (ngoài vị từ `_la_chot`) và bị D2/D3 che trên nhánh đã-có-dấu, nên đột biến "`bo_qua_han` miễn luôn D1" — bị `t190`+`t191` giết ở nền — SỐNG toàn suite 256/256 ở ứng viên dù quan sát được ở API `kiem(…, bo_qua_han=True)`; docstring `t190`/`t191` vẫn khai độ phủ cũ. |
| `a9-mien-refs-remotes-khong-co-ca` | P2 | Nghĩa vụ miền A9 `refs/remotes/*` không có ca nào: bỏ `"refs/remotes"` khỏi helper QUA 42/42 ca `t217_*`, trong khi trên clone thường helper ấy chỉ quét 1 ref/132 blob (đúng: 482/594) và báo sạch rc=0 — kể cả khi lease sai kiểu nằm ngay ở nhánh máy chủ. |

### Lớp 1 — `thong-diep-lease-id-sai-dung-repr-tho` (P2)
- Biểu hiện: `ops/lease_publish.py:313` (`… được {type(gia_tri).__name__} {gia_tri!r}`), `:317–326` (`_lease_id_quet`: `except Chan`
  — docstring "Bản KHÔNG ném"), `:2174` (D8), `:2325` (D7), `:2352` (D9); nhãn cứng "sai kiểu" ở :2174, :2325, :2343.
- Phép đo: `scripts/do_int_lon.py` (3.11/3.12/3.13: `0x`/`0b`/`0…`/lục thập phân ⇒ `int` 14769–18000 bit, `repr` ném `ValueError`;
  4301 chữ số thập phân thì chính `safe_load` ném). `scripts/do_int_lon_sp.py` (3.12, fixture `_yaml_that`/`_wp678_kho` của
  ứng viên, CLI tiến trình con): ứng viên `TRUC_TIEP _lease_id_hop_le(int lớn) -> ValueError`, `_lease_id_quet -> ValueError`;
  `check`/`body`/`ai-dang-giu ops/x.md`/`ai-dang-giu ops/khac.md --du-bao` ⇒ `(1, 'ValueError: Exceeds the limit (4300 digits)…')`
  (đối chứng `yes` ⇒ 8 / 8 / 12 / 0). Nền: cùng rc=1 ở cả bốn ⇒ KHÔNG hồi quy. A9 ⇒ rc=2 `KHONG_DO_DUOC: ValueError` (spec A9
  cho phép "số vượt giới hạn chuyển đổi ⇒ rc=2", nên A9 không thuộc lớp). `scripts/do_bom_check.py`: bom bí danh k=6 (591 byte)
  ⇒ rc=8, stderr nền 2.790.130 / ứng viên 2.790.163 ký tự; k=5 ⇒ 310.072 / 310.105 (×9 mỗi cấp). `scripts/do_nhan.py`:
  `lease_id: 'co khoang trang'` ⇒ `KHÔNG_XÁC_ĐỊNH\tlease_id sai kiểu 'co khoang trang'` và `CHAN [12]: … mang lease_id sai kiểu`.
  Đột biến X03 (`_lease_id_quet` nuốt mọi ngoại lệ) QUA 5/5 ca quét ⇒ không ca nào đo lớp ngoại lệ này.
- Theo chữ: §6 mục 1 và Q1 ("Sai ⇒ `Chan(RC_NOI_DUNG)`, tức rc=8"), §6 mục 4 ("in `KHÔNG_XÁC_ĐỊNH`") không đạt cho lớp giá trị
  này; docstring hai hàm và BAO_CAO §1 ("bản không ném") rộng hơn phép đo. Không P1: fail-close (rc≠0), nền hỏng y hệt.
- Hướng vá (HINT nhóm 1): `_repr_an_toan` (reprlib có trần + `try`, trần 120 ký tự) + `_nhan_lease_id_sai` (`sai kiểu` vs
  `sai dạng`), dùng ở :313/:2174/:2325/:2352 và thông điệp `CHAN [12]`; ca `t218`.

### Lớp 2 — `phu-nhanh-da-dang-chot-lease-id-mat-rang` (P2)
- Biểu hiện: `ops/lease_publish.py:1056` (D1 là lời gọi, không còn `raise Chan` trực tiếp); `ops/lease_publish_test.py:9536–9542`
  (`_la_chot`); `t190` docstring :9414–9415 và chú thích :9491–9494; `t191` docstring :10312–10313; BAO_CAO không nhắc `t191`.
- Phép đo: §1.6 và §1.8 (đổi tên thuần ⇒ `t191` `KHONG_CHAM`; đầu dò 1 → 0; R02b 256/256; nền: `t190`+`t191` giết; API: QUA thay vì
  `Chan 8`; K03 ⇒ `t190` vẫn giữ tính chất đầu-cuối).
- Hướng vá (HINT nhóm 2): ca `t219` gọi thẳng `kiem(…, bo_qua_han=True)` cho 10 dạng A1 + một chuỗi sai dạng ⇒ rc=8, đối chứng
  chuỗi hợp lệ hết hạn ⇒ qua; sửa docstring/chú thích `t190` (vi) và phạm vi còn hở của `t191`.

### Lớp 3 — `a9-mien-refs-remotes-khong-co-ca` (P2)
- Biểu hiện: `ops/lease_publish_test.py:12246–12247` (helper liệt kê `refs/heads`, `refs/remotes`); 42 ca `t217_*` không ca nào
  đặt lease chỉ ở `refs/remotes/*`; `x678/mut_a9.py` của executor có `bo-refs-heads` (dòng 63) mà không có đột biến đối xứng.
- Phép đo: §1.8 (A11 QUA 42/42; kho tạm ⇒ ứng viên rc=1 / A11 rc=0 so_blob 0; snapshot clone thường ⇒ 482/594 vs 1/132, cả hai rc=0).
- Hướng vá (HINT nhóm 3): ca `t217_a9_sai_kieu_chi_o_refs_remotes` (lease `on` chỉ ở `refs/remotes/origin/xa`, đòi rc=1 và
  `refs == ["refs/remotes/origin/xa"]`).

## 5. Trả lời các câu của PROMPT

1. **Spec acceptance** — §2. Mọi A1–A8 tĩnh, A10 đạt bằng phép đo độc lập; A9 đạt trừ vế "gỡ nghĩa vụ miền `refs/remotes` phải
   làm ca ĐỎ" (lớp 3). Write set đúng 2 tệp. Suite N/N hai vế dựng trong MỘT lệnh: 201/201 → 256/256 ở 3.11 và 3.12. Ruff F
   delta theo đa tập = ∅.
2. **Mọi đường đọc `lease_id`** — §3. Không đường nào còn `str()`/so sánh tạo danh tính trên giá trị chưa xác thực; đường còn
   ném lớp khác `Chan` là thông điệp `repr` thô (lớp 1). Mỗi chốt có răng riêng, giết bằng `TinHieuChotCa` đúng ca (§1.5);
   ngoại lệ: D1 trên đường `bo_qua_han` (lớp 2).
3. **`t191` 14 → 13** — KHÔNG chỉ đổi hình thức, nhưng cũng không mất tính chất qua `kiem_github`. (a) Chênh là do `_la_chot`
   không nhận tên `_lease_id_hop_le`; đổi tên thuần sang `_kiem_…` thì `t191` ĐỎ `KHONG_CHAM`. (b) Không ca nào khác đo nhánh
   đã-đăng cho `lease_id` sai: đầu dò 1 → 0 lời gọi; đột biến gỡ lời gọi ở :1056 CHỈ trên nhánh đã-đăng SỐNG toàn suite
   256/256, trong khi đột biến tương đương ở nền bị `t190` + `t191` giết, và nó quan sát được ở API `kiem(…, bo_qua_han=True)`
   (trái chú thích :1084). (c) Qua `kiem_github` hành vi giữ nguyên nhờ D2/D3 (K03/K04). Spec r17: `t190` 1 dòng (:60, hàng
   `provider` của wp709), `t191` 0 dòng; theo chữ r17 không tiêu chí A nào đỏ (A8 delta 0), nhưng §6 mục 7 (docstring phải nói
   sự thật mới) không đạt cho `t190` vế (vi), và theo phân lớp bắt buộc đây là "test không có răng" có số đo ⇒ **P2**.
4. **D7 với lease HẾT HẠN** — Đúng chữ Q3 ("một lease khác mang `lease_id` không phải chuỗi … D7 in `KHÔNG_XÁC_ĐỊNH` cho nó và
   thoát khác 0") và §6 mục 4 ("gặp lease sai kiểu thì in `KHÔNG_XÁC_ĐỊNH` và thoát khác 0"): cả hai không điều kiện theo hạn.
   Cụm "cùng hình dạng với nhánh bia mộ một chiều" có thể đọc là kéo theo điều kiện `CÒN_HẠN` của nhánh ấy — mơ hồ, nên tôi
   KHÔNG xếp lớp. Nhất quán với doctrine fail-close có sẵn: `_quet_lease_toan_kho` đã trả `KHÔNG_XÁC_ĐỊNH` TOÀN CỤC cho lease
   YAML hỏng/không phải ánh xạ bất kể hạn và đường dẫn. Đỏ oan kho thật: **không** tại snapshot đo được (stdout nền = ứng viên
   từng byte cho cả hai tệp write set; A9 594/594 `str`, 0 thiếu ID). Chi phí đã đo (§1.7): lease hỏng HẾT HẠN chạm đường dẫn ⇒
   rc 0 → 12; thiếu `lease_id` còn hạn 11 → 12; có người giữ thật + lease hỏng hết hạn ⇒ 11 → 12 (dòng `CÒN_HẠN` vẫn in). Miễn
   lease hết hạn là một quyết định mới của chủ kho, không phải lỗi của bản vá.
5. **Lời khai khác của executor** — `L` sống t178/t195–t197, chết t205: **có** (R03). `t207` chỉ đỏ khi gỡ D1+D3+D6: **có** cho
   hai tổ hợp đo (K01 QUA, K02 GIET; các tổ hợp khác không đo lại). SyntaxWarning 3.12: **có** (:2947 `\s`, :4941 `\d`; nền
   :2945, :4938). 594 vs 597: 594 **có** (bản sao snapshot, 481 nhánh); 597 `KHÔNG ĐO ĐƯỢC` (đếm khác ra 598 mọi tệp / 597 nếu
   gồm tag). A9 "27 đột biến … 31 GIẾT": các đột biến ấy không bao vế `refs/remotes` (lớp 3). `check` 132 tệp giống hệt: **có**
   (trong rig có `.git`). Ruff 11/11, A8 tĩnh, 201/201 → 256/256: **có**.

## 6. KHÔNG ĐO ĐƯỢC
- Windows / nền `nt` thật (lease cấm CI Windows); chỉ có seam mô phỏng của `t193`.
- CI GitHub (không chạy; `ci_budget`). Máy chủ GitHub live (không mạng): lượt A9 + fsck của tôi chạy trên BẢN SAO snapshot
  `x678/mirror.git` của executor, không phải `ls-remote` live; "481 = ls-remote" của executor không tái lập được.
- Comment cấp quyền #678 `6053320533` và danh tính người ký (#566).
- Cách đếm "597 blob lease" của phiên soạn lease (480 ref, 05:3xZ).
- Model/effort thực sự phục vụ lượt review này: cấu hình tự khai Claude Opus 5.5 `claude-opus-5-5` effort max; runtime không
  đường nào trong phiên trả về.
- R02b toàn suite chỉ đo ở 3.11 (3.12 chưa chạy riêng; R02 ba ca đích đo ở 3.11). Python 3.13: chỉ đo phần tĩnh và `t70`/`t193`.
- Bom bí danh chỉ đo tới k=6 (tăng ×9 mỗi cấp đo ở k=5→6); cấp lớn hơn cố ý không chạy (bộ nhớ container).
- Các script đột biến của executor (`mut_*.py`, `do_*.py`) không chạy lại; tôi dùng bộ độc lập (§1.5, §1.8), chỉ ĐỌC `mut_a9.py`
  để xác định nó thiếu đột biến `refs/remotes`.

## 7. HINT (`goi/HINT.patch`, 224 dòng, 3 nhóm, đường dẫn repo-relative không tiền tố `a/`/`b/`)
Dựng bằng `w.TUbSq9/scripts/dung_hint.py` (s0 = ứng viên → s1 → s2 → s3, mỗi neo phải duy nhất, mỗi nhóm một `# lop:`).
Nhóm 1 `thong-diep-lease-id-sai-dung-repr-tho`: `ops/lease_publish.py` (+`_repr_an_toan`, +`_nhan_lease_id_sai`, 5 chỗ dùng) và
ca `t218`. Nhóm 2 `phu-nhanh-da-dang-chot-lease-id-mat-rang`: ca `t219` + docstring/chú thích `t190`/`t191`. Nhóm 3
`a9-mien-refs-remotes-khong-co-ca`: ca `t217_a9_sai_kieu_chi_o_refs_remotes`. Không ca mới nào dùng `_chay_buoc_dang*` ⇒ không
đổi `mong`/`SO_BO_QUA`/literal `t193`.

Dry-run trên bản sao (`git archive f809249 ops/lease_publish.py ops/lease_publish_test.py`, từ gốc bản sao):
```
$ patch -p0 --fuzz=0 --dry-run < goi/HINT.patch
checking file ops/lease_publish.py
checking file ops/lease_publish_test.py
checking file ops/lease_publish_test.py
checking file ops/lease_publish_test.py
Hunk #1 succeeded at 12405 (offset -75 lines).
DRYRUN_RC=0
```
(offset −75 ở nhóm 3 vì dry-run đo mọi nhóm trên tệp GỐC; áp thật thì không offset.) Sau dry-run băm hai tệp không đổi.

Kiểm hành vi (áp THẬT trên bản sao, không trên `cay-kho`):
- Áp thật `patch -p0 --fuzz=0` trong clone git f809249 (`scripts/do_suite_hint.sh`): rc=0; toàn suite **259/259** rc=0 ở 3.11 và
  3.12 (07:59:31Z–08:08:53Z), vào 259 = ra 259, 0 `.pyc`, porcelain đúng 2 tệp (`--numstat` 28/5 và 92/1); `t216` 12/12.
- Ruff F trên cây đã vá: 11 = 11, đa tập thêm ∅ bớt ∅. A8 tĩnh trên cây đã vá (so nền): 259 ca, D 14, chỉ-lồng `{t70}`, G−D
  `{t202}`, sổ 13, (S) 29 → 31, 0 lần mới ĐỎ.
- Hai chiều (`scripts/db_hint.py`, `db_hint2.py`; log `hint_hai_chieu.log`): sản phẩm ứng viên CHƯA vá + test đã vá ⇒ `t218`
  GIET (`NEM ValueError`), `t219` và ca `refs/remotes` QUA (hành vi ứng viên vốn đúng ở hai chỗ ấy); R02b trên bản vá ⇒ `t219`
  GIET; A11 trên bản vá ⇒ ca `refs/remotes` GIET; gỡ từng chỗ vá của lớp 1 (H04 hàm chung, H05 nhãn, H06 trần, H07 D7, H08 D8,
  H09 D9, H10 bỏ trần giữ `try`) ⇒ mỗi cái giết `t218` đúng vế bằng `TinHieuChotCa`.

## 8. Kết luận
`changes_requested` — 3 lớp mở, cả ba **P2**, 0 P1, 0 P3:
`thong-diep-lease-id-sai-dung-repr-tho` · `phu-nhanh-da-dang-chot-lease-id-mat-rang` · `a9-mien-refs-remotes-khong-co-ca`.
Lõi của packet (D1–D9 qua một hàm, A1–A8, A10) đo được là đúng và có răng; không hồi quy hành vi nào so nền (bốn đường rc=1 của
lớp 1 hỏng y hệt ở nền). Mức assurance của lượt này: `review_deferred` (subagent trong phiên điều phối, cùng họ executor);
land vẫn đòi `human_audited` của chủ kho.
