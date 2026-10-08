verdict: changes_requested
reviewed_sha: 7a3a2f6a51aef316c2fe36b5e8559d5d6acd49ee
spec_sha256: f39091a1d2be7629a11eb53b7daf3f076ce91f701012f7093108a98e91d140cc
reviewer_provider: anthropic
reviewer_model: claude-opus-5-5 (subagent review-opus-max, tự khai)
execution_surface: claude_code_subagent
che_do: subagent_trong_phien_dieu_phoi

> TRẠNG THÁI LƯỢT: XONG (09:5xZ 08-10-2026). Tệp ghi TĂNG DẦN; dòng `verdict` chốt sau §7 "Kết luận".
> Tóm tắt: 0 P1 · 1 P2 · 2 P3 — `phu-nhanh-da-dang-chot-lease-id-mat-rang` (P2, còn mở), `a9-mien-refs-remotes-khong-co-ca`
> (P3, còn mở, thu hẹp), `khoa-t218-hep-cat-cau-truc-va-nhan` (P3, mới). Lớp `thong-diep-lease-id-sai-dung-repr-tho` ĐÃ ĐÓNG.
> Tỷ lệ vá thật 1→2 theo lớp 1/3. HINT: `goi/HINT.patch` sha256 `477c360a…274e` (dry-run `patch -p0 --fuzz=0` rc=0, §6).

Reviewer tự khai: Claude Opus 5.5 (model id `claude-opus-5-5`, effort max), chạy như subagent trong phiên điều phối
Claude Code. KHÔNG phải codex. Không mạng, không đăng GitHub, không commit/push; `cay-kho/` chỉ đọc.

## 0. Tiền kiểm (đã chạy)
```
$ sha256sum SPEC.md lease.yaml luot1/*
f39091a1d2be7629a11eb53b7daf3f076ce91f701012f7093108a98e91d140cc  SPEC.md
7a981529da52ba54ccf8a153af4f92f4d8ab28feae891859cb6071bf88a9748d  lease.yaml
0c03851598e5d50da5a2cf8b8d4a7f07b1095fb4971aaabe671d970a5af6b128  luot1/HINT.patch
6438cf90a4e93ca2e737669b263426c1eb14804d8e7cb1f2c1153ce091db2cdb  luot1/VERDICT.md
sha256sum: luot1/scripts: Is a directory
$ git -C cay-kho rev-parse HEAD HEAD^{tree}
7a3a2f6a51aef316c2fe36b5e8559d5d6acd49ee
e79a7be15e5b804632fa423eaefa31a61d7cd004
$ git -C cay-kho status --short        # rỗng, rc=0
```
Khớp PROMPT.md: spec `f39091a1…40cc`, VERDICT lượt 1 `6438cf90…2cdb`, HINT lượt 1 `0c038515…b128`, HEAD, tree; cây sạch.
(`lease.yaml` = `7a981529…748d`, bằng giá trị lượt 1 ghi.) ⇒ không `blocked` vì tiền kiểm.
Công cụ: Python 3.11.15 / 3.12.3 / 3.13.12 (PyYAML 6.0.1, `get_int_max_str_digits()` = 4300 cả ba), git 2.43.0,
ruff 0.15.8, GNU patch 2.7.6, actionlint, shellcheck. Thư mục làm việc `$R/w.aDKYWW` (mktemp).

## 1. Nhật ký đo (ghi tăng dần; mọi số kèm lệnh + rc thật)

### 1.1 Vòng 2 có đúng là áp NGUYÊN VĂN HINT lượt 1 không — **có**
```
$ git -C cay-kho diff f809249 7a3a2f6 | sha256sum        # c9a052aa…8464 = sha256 diff-l1-l2.patch
$ git -C cay-kho diff ab457c6 7a3a2f6 | sha256sum        # d802ab6c…f801 = sha256 diff-base-head.patch
$ git -C cay-kho diff --numstat ab457c6 7a3a2f6          # 109 19 ops/lease_publish.py · 994 19 ops/lease_publish_test.py
$ cd w.aDKYWW/kiem_hint && git -C cay-kho archive f809249 ops/lease_publish.py ops/lease_publish_test.py | tar -x \
    && patch -p0 --fuzz=0 < luot1/HINT.patch           # PATCH_RC=0
ops/lease_publish.py      ap=ca480114…  7a3a2f6=ca480114…  KHOP
ops/lease_publish_test.py ap=893c3a0d…  7a3a2f6=893c3a0d…  KHOP
```
Write set vẫn đúng 2 tệp. Vì vòng 2 = chính HINT của lượt 1 (cùng model với reviewer này), mọi kết luận dưới đây đo lại
trên 7a3a2f6, không dựa vào phần "kiểm hành vi" của §7 lượt 1.

### 1.2 Ruff F (đa tập (tệp, code, message)) — delta ∅
`ruff check --no-cache --select F ops/lease_publish.py ops/lease_publish_test.py --output-format json` trên ba cây
`git archive` (`w.aDKYWW/cay/{nen,l1,ung}`): rc=1 cả ba; nền 11 · lượt 1 11 · ứng viên 11; ung−nen ∅, nen−ung ∅, ung−l1 ∅.
Tập nền: F401 ×7, F841 ×2, F541 ×2 (khớp lượt 1 và lời khai điều phối).

### 1.3 Câu 2 — công cụ khác có phân tích các thông điệp vòng 2 đổi không — **không** (trong kho)
Vòng 2 đổi bốn chuỗi: nhãn `lease_id sai kiểu <repr>` (D7, D8) thành `sai kiểu|sai dạng <repr có trần>`, câu
`CHAN [12]` "`mang lease_id sai kiểu`" thành "`… không hợp lệ (sai kiểu hoặc sai dạng)`", repr trong thông điệp
`_lease_id_hop_le` và D9. Tìm trên cây 7a3a2f6 (`rg -F`, bỏ `ops/{specs,reviews,prompts}`):
- `lease_id sai kiểu` / `lease_id sai dạng` / `lease_id không hợp lệ` / `lease_id phải là CHUỖI`: chỉ ở hai tệp write set.
- `mang lease_id`: ngoài `ops/lease_publish.py` chỉ có `ops/land/pr701-wp687-*` (hồ sơ land lịch sử, nghĩa khác: "bản mang
  lease_id X").
- Mã thực thi gọi `lease_publish.py`: `ops-publish-lease.yml` (bước `đăng` :204–:259) chỉ phân nhánh theo `rc` (9 ⇒ bỏ qua,
  khác 0 ⇒ `bao_chan`), không đọc thông điệp; `ops-thu-hoi-admission.yml` gọi `kiem-thu-hoi-github` (vòng 2 không chạm);
  `ops/ci_duong_nhanh.py` :511–:552 dùng `rc` và dòng CUỐI output làm chẩn đoán, không khớp chuỗi; `ops/bien_nhan_v2.py`
  không import/gọi `lease_publish` (`rg -n 'lease_publish|lease_id'` 0 dòng). Không tệp `.py/.sh/.yml` nào ngoài write set
  và ngoài thư mục hồ sơ khớp `NGƯỜI_GIỮ|KHÔNG_XÁC_ĐỊNH\t|DU_BAO:` (0 dòng). Trong hồ sơ `ops/{land,reviews,specs,handoff,
  tham-dinh}/` (10 tệp khớp mẫu rộng hơn): chỉ script đo lịch sử đọc dòng `NGƯỜI_GIỮ …` (vòng 2 không đổi) và bản sao đóng
  băng của phiên bản cũ; không tệp nào khớp các chuỗi vòng 2 đổi.
- Chuỗi lệnh cấp lease trong SPEC (:104–:112, `s5.py` nhúng ở SPEC, `git ls-files` không có `s5.py`) chỉ `grep -x -F`
  hai dòng `NGƯỜI_GIỮ 0: không có` và `S5 TỰ_KIỂM 38/38 đạt; NGƯỜI_GIỮ 0 ở 2/2 đường dẫn` — vòng 2 không đổi hai dòng ấy;
  `s5.py` thay `_lease_cham_duong`, `GOI_GIT` và gọi `main` — ba tên vòng 2 không đổi.
- Trong suite: `t213` ("sai kiểu True") và `t215` ("`DU_BAO: KHÔNG_XÁC_ĐỊNH lease_id sai kiểu 1000`") vẫn khớp vì giá trị
  không phải `str` vẫn mang nhãn `sai kiểu` (đo toàn suite ở §1.4).
Công cụ ngoài kho (scratch của phiên khác): `KHÔNG ĐO ĐƯỢC`.

### 1.4 Câu 3 — toàn suite nền vs ứng viên, hai vế dựng trong MỘT lệnh (`w.aDKYWW/scripts/do_ab.sh`, log `log/ab.log`)
Một vòng lặp dựng 4 clone `--no-hardlinks` từ `cay-kho` (nền ab457c6 / ứng viên 7a3a2f6 × 3.11/3.12), `checkout --detach`,
`core.abbrev 7` (repo + `--global` trong HOME riêng), 08:43:04Z–08:43:11Z; rồi mỗi bản Python chạy song song hai vế
`env -u GITHUB_ACTOR HOME=… TMPDIR=… PYTHONDONTWRITEBYTECODE=1 PATH=<bin python>:$PATH python3 ops/lease_publish_test.py`.

| | Python 3.11.15 (08:43:11Z–08:52:27Z) | Python 3.12.3 (08:52:27Z–09:02:57Z) |
|---|---|---|
| nền ab457c6 | **201/201**, rc=0, bỏ qua 0, vào 201 = ra 201 = `^@ca` 201, 0 `.pyc`, porcelain 0 | **201/201**, như bên trái |
| ứng viên 7a3a2f6 | **259/259**, rc=0, bỏ qua 0, vào 259 = ra 259 = `^@ca` 259, 0 `.pyc`, porcelain 0 | **259/259**, như bên trái |

Delta ca đỏ = **0** ở cả hai bản (khớp lời khai điều phối 259/259 · 201/201). `t191`: nền "14 chốt", ứng viên "13 chốt" (cả
hai bản). `t216`: `mẫu số=12, giết thật=12, tín dụng giả=0, sống sót=0`. Ba ca mới `t218`, `t219`,
`t217_a9_sai_kieu_chi_o_refs_remotes` có dòng `<<< ra … QUA` ở cả hai bản. stderr: 3.11 giống hệt sau khi bỏ số dòng;
3.12 chỉ khác TIỀN TỐ đường dẫn clone, cùng 19 dòng `SyntaxWarning` (nền :2945/:4938 → ứng viên :2947/:4941, có sẵn từ nền).

### 1.5 Lớp 1 — ma trận CLI (`scripts/do_cli.py`, log `log/cli.tsv`, 324 lượt, 08:46:14Z–08:47:56Z, rc=0, 0 `.pyc`)
Fixture tự dựng (cùng trường `lease_mau()`; kho có `origin` thật, nhánh `a` đã đẩy + fetch; `x.yaml` giữ `ops/x.md`, `y.yaml`
giữ `ops/y.md` kèm `tham_chieu_truong_lease: [vung_duoc_phep_cham]` để `con-tro-treo` in `lease_id`), `gh` giả ghi nhật ký,
`GITHUB_REPOSITORY=o/r`. Bốn biến thể `lease_id`: `lon` = `0x`+4000 `f` (int 16000 bit, `safe_load` không ném) · `bom6` =
bí danh lồng 6 cấp ×9 · `sai_dang` = `'co khoang trang'` · `ok` = `wp-ok-1`. Chín lệnh: `check`, `check --du-bao`, `body`,
`kiem-github`, `ai-dang-giu ops/x.md` (liên quan) / `ops/khac.md` (không liên quan), mỗi cái có và không `--du-bao`,
`con-tro-treo`. Ba cây `git archive` × Python 3.11.15/3.12.3/3.13.12: **mọi ô cho cùng kết quả ở cả ba bản Python**.

| biến thể · lệnh | nền ab457c6 | lượt 1 f809249 | ứng viên 7a3a2f6 |
|---|---|---|---|
| `lon` · check / check --du-bao / body / kiem-github | rc=1 Traceback | rc=1 Traceback | **rc=8**, 0 gh, ≤168 byte |
| `lon` · adg liên quan / liên quan --du-bao | rc=1 Traceback | rc=1 Traceback | **rc=12**, 1 dòng `KHÔNG_XÁC_ĐỊNH` (+2 `DU_BAO: KHÔNG_XÁC_ĐỊNH`) |
| `lon` · adg không liên quan --du-bao | rc=1 Traceback | rc=1 Traceback | **rc=0**, 2 dòng `DU_BAO: KHÔNG_XÁC_ĐỊNH` |
| `lon` · con-tro-treo | rc=1 Traceback | rc=1 Traceback | **rc=0**, 1 dòng `CON_TRỎ_TREO` (≤253 byte) |
| `bom6` · check / body / kiem-github | rc=8, 2.790.130 byte | rc=8, 2.790.163 | **rc=8, 221 byte** |
| `bom6` · adg liên quan --du-bao | rc=11, 11.160.647 byte | rc=12, 8.370.850 | **rc=12, 1.053 byte** |
| `bom6` · con-tro-treo | rc=0, 2.790.223 byte | rc=0, 2.790.248 | **rc=0, 306 byte** |
| `sai_dang` · adg liên quan | rc=11 | rc=12, nhãn `sai kiểu` | **rc=12, nhãn `sai dạng 'co khoang trang'`** |
| `ok` · cả 9 lệnh | 0/0/0/0(3 gh)/11/0/11/0/0 | giống nền | **giống nền từng ô** (rc, số dòng, số lời gọi gh, độ dài) |

`adg-khac` (không `--du-bao`) rc=0 ở cả ba cây với mọi biến thể (D7 chỉ xét lease chạm đường hỏi). ⇒ Mọi lệnh CLI của
`ops/lease_publish.py` đọc `lease_id` của lease đều kết thúc có kiểm soát, output có trần, ở cả ba bản Python; `ok` không đổi
hành vi so nền. Ngoại lệ thời gian: `con-tro-treo` với `bom6` mất 1,4–3,0 s ở CẢ BA cây (phép duyệt scalar của
`_cac_nhac_mo_ho`, có từ nền, không phải repr) — xem §3 (ngoài phạm vi).

### 1.6 Lớp 1 — liệt kê bằng máy mọi chỗ định dạng `lease_id` (`scripts/liet_ke_dinh_dang.py`, AST: f-string, `%`,
`.format`, `str()`, `repr()` có hằng `"lease_id"` hoặc tên `lease_id/lid/lease_moi/lease_cu`)
Ứng viên 17 chỗ (nền: 14 "thô?" + 11 tên biến). Lần theo nguồn gán từng tên biến: :900/:909 (`_kiem_comment_da_co`, gán
:885 qua hàm chung) · :1295 (D4, :1292) · :2173 (D8, :2149) · :833 (D6, :816) · :2201/:2356/:2361 (gán từ
`_lease_id_quet` khác `None`) · :2390/:2394 (`_lease_id_hien_thi`) · :2197/:2348/:2375 (bọc `_nhan_lease_id_sai` /
`_repr_an_toan`) · :2306 `lenh_check` và :2321 `lenh_kiem_github` in `lease['lease_id']` SAU khi `kiem()` trả về (đã qua D1)
· :1461 sau phép kiểm :1418. **Chỗ thô duy nhất còn lại: :1420 `kiem_ban_ghi_thu_hoi`** (`lease_id` của BẢN GHI SỔ thu hồi)
— SPEC §5 đặt ngoài phạm vi (§3). Thông điệp của chính `_lease_id_hop_le` (:336) dùng `_repr_an_toan(gia_tri)`.

### 1.7 Lớp 1 — `_repr_an_toan` ở mức API (`scripts/do_repr_api.py`, `RLIMIT_AS` 3 GiB, log `log/repr_api_*.log`)
Ứng viên, 3.11.15 / 3.12.3 / 3.13.12, mỗi giá trị dựng qua `yaml.safe_load`: int `0x`+4000, `0b`+14000, `0`+5000 (bát phân),
lục thập phân 2600 nhóm, `-0x`+4000, chuỗi 1 MB, `!!binary` 3 MB, danh sách tự tham chiếu `&r [*r]`, `!!set` 20.000 phần tử,
`datetime` có múi, ánh xạ có KHOÁ int lớn, bom bí danh k=6…12 (9^12 lá): **không ca nào ném; mọi ca ≤ 0,015 s; độ dài
≤ 121** (bom k=12: 0,000 s, 121 ký tự, `[[[...], [...], [...], [...], ...], …`). Khác theo bản: `reprlib.repr(int lớn)`
NÉM `ValueError` ở 3.11/3.12 nhưng **KHÔNG ném ở 3.13** (trả `<int instance with roughly 4817 digits (limit at 4300) at
0x…>`), nên ở 3.13 thông điệp mang một ĐỊA CHỈ BỘ NHỚ (không tất định giữa hai lượt); 3.11/3.12 trả `<int không in được>`.

### 1.8 Lớp 1/2/3 — đột biến độc lập trên 7a3a2f6 (`scripts/do_db.py` + `db_r2.py`, `db_r2b.py`, `db_r2c.py`,
`db_doiten.py`, `db_khoa.py`; mỗi đột biến một bản `git archive 7a3a2f6 ops .github` mới trong `w.aDKYWW/mut`, không
hardlink, neo phải duy nhất; ca chạy bằng `scripts/chay_ca.py` nạp CHÍNH module test của bản sao; phân hạng GIET =
`TinHieuChotCa` của module · TIN_DUNG_GIA = ngoại lệ khác · QUA; 0 `.pyc` sau mọi đột biến)
Đối chứng xanh trước (`DC`, 3.12): 55/55 ca đích QUA trên bản sao KHÔNG đột biến (`t218 t213 t215 t209 t211 t212 t214
t219 t204 t190 t191 t216` + 43 `t217_*`), `t191` "13 chốt", `t216` 12/12.

| đột biến (3.12; cột 3.11/3.13 từ `db_khoa`) | ca đích | kết quả |
|---|---|---|
| L1a `_repr_an_toan`: `repr()` dựng sẵn TRONG `try`, GIỮ trần 120 | t218 | **QUA** (sống) |
| L1b reprlib nới hạn mức (99 cấp, 10^9 phần tử), GIỮ trần | t218 | **QUA** (sống) |
| L1c bỏ `try`, chỉ reprlib | t218 | GIET ở 3.12 (`NEM ValueError`) |
| L1d `_lease_id_quet` nuốt `Exception` thay `Chan` | t218 t209 t211 t212 t213 t215 | QUA cả 6 — tương đương (hàm chung nay chỉ ném `Chan`) |
| L1e nhãn D8 luôn `sai kiểu` | t218 t213 t215 t214 + 3 ca A5 | **QUA cả 7** (sống) |
| L1f câu `CHAN [12]` trả về "mang lease_id sai kiểu" | như L1e | **QUA cả 7** (sống) |
| L1g đảo nhãn `sai kiểu`/`sai dạng` | t218 t213 t215 | GIET cả ba |
| L2a = R02b: `if not bo_qua_han:` trước D1 (giữ neo catalog) | t219 t204 t190 t191 t216 | **GIET t219** (`lease_id: true … được rc=0`), 4 ca kia QUA |
| L2b miễn D1 khi `bo_qua_han` VÀ hết hạn (qua `_doc_han`) | như trên | t219 QUA; GIET t191 vì `_la_chot` thấy lời gọi `_doc_han` MỚI (vô can) |
| L2b2 / L2b3 như L2b, đọc hạn bằng `fromisoformat` / `_phan_loai_lease` | + t174 t207 t178 | t219 QUA; t190 "chết" ở hàng (ii) "hạn hỏng dạng" (ValueError trần / rc=12) — TÍN DỤNG GIẢ: đột biến đọc hạn sớm, không phải vì D1 bị miễn |
| **L2b4** như L2b, đọc hạn AN TOÀN (hạn hỏng ⇒ coi như chưa hết hạn), không tên `_doc_*`/`_kiem_*` | t219 t204 t190 t191 t216 t174 t207 t178 t205 t206 t195–t198 t180 t177 (17 ca) | **QUA cả 17** (sống) |
| L2c miễn D1 khi `bo_qua_han` và không phải `str` | t219… | GIET t219 (`true`) |
| L2d miễn D1 khi `bo_qua_han` và là `str` | t219… | GIET t219 (`'co khoang trang'`) |
| L2e D1 chỉ khi có `tep` | t219 t204… | GIET t219, GIET t204 |
| L2f miễn D1 khi `bo_qua_han` và `lease_id` là list/dict | t219 t204 t190 t191 | QUA cả 4 (sống) |
| DT đổi tên thuần `_lease_id_hop_le`→`_kiem_lease_id_hop_le` (11 chỗ) | t191 t190 t219 t204 | GIET t191 `['_kiem_lease_id_hop_le (dòng 1079, cột 4): KHONG_CHAM']` — lời khai docstring `t191` vòng 2 **đúng** |
| L3a bỏ `"refs/remotes"` khỏi `for-each-ref` (= A11 lượt 1) | 43 `t217_*` | **GIET đúng ca mới** `t217_a9_sai_kieu_chi_o_refs_remotes` (rc=0 thay 1), 42 QUA |
| L3b bỏ `"refs/heads"` | 43 | GIET 28 |
| L3c chỉ `refs/remotes/origin` | 43 | **QUA cả 43** (sống) |
| L3d glob `refs/remotes/*` (một cấp) | 43 | GIET ca mới |
| L3e bỏ leaf `HEAD` dưới `refs/remotes` kể cả KHÔNG tượng trưng | 43 | **QUA cả 43** (sống) |
| L3f `refs/remotes/o` (khớp tiền tố tới `/`) | 43 | GIET ca mới |
| L3g THÊM `refs/tags` (nới miền) | 43 | QUA cả 43 — nới, không phải bỏ; tags ngoài miền SPEC A9 |

Hậu quả đo được của các đột biến sống:
- **L1a** (`scripts/do_repr_api.py … L1a`, 3.12, RLIMIT_AS 3 GiB): bom k=6 0,062 s / 52 MiB · k=7 0,448 s / 63 MiB · k=8
  4,053 s / 279 MiB · **k=9 43,190 s / 2187 MiB RSS** — thông điệp vẫn cắt còn 121 ký tự nên `t218` (chỉ đo `len(td) < 1000`)
  không thấy. Ứng viên k=9: 0,000 s / 52 MiB. Phần bí danh của bom k=9 dài 421 byte (k=6: 283 byte).
- **L2b4**: hợp đồng ghi ngay trên chốt hạn của `kiem()` (:1107) — "`bo_qua_han` bỏ ĐÚNG MỘT chốt — chốt HẠN" — bị vi phạm đúng
  ở miền đầu vào mà `bo_qua_han` sinh ra để phục vụ (lease đã đăng rồi mới hết hạn, `t174`); các hàng âm của `t219` đều dựng
  bằng `_yaml_that(raw)` mặc định `het_han=False`, chỉ hàng đối chứng là hết hạn.
- **L3c / L3e** (`scripts/do_a9_mien.py`, clone THƯỜNG của "máy chủ" có nhánh `topic/HEAD` mang `lease_id: on`, cộng remote
  `upstream` có nhánh `xa` mang `lease_id: yes`): ứng viên rc=1, 2 lỗi (`refs/remotes/origin/topic/HEAD`,
  `refs/remotes/upstream/xa`), 5 ref; L3c rc=1 nhưng **bỏ sót `refs/remotes/upstream/xa`** (3 ref); L3e trên clone hai
  remote bỏ sót `topic/HEAD`, trên clone MỘT remote **rc=0, `errors []`, 2 ref** — báo sạch trong khi nhánh máy chủ mang
  lease sai kiểu (cùng hình dạng lớp 3 lượt 1, miền hẹp hơn).

Đa bản Python (`db_khoa.py`, ca đích như bảng): 3.11.15 — L1a, L1b, L1e, L1f, L2b4, L3c, L3e QUA hết; L2a GIET `t219`; L3a GIET ca
mới; L1c GIET `t218` (`NEM ValueError`). 3.13.12 — như 3.11 trừ **L1c QUA** (reprlib 3.13 không ném ở int lớn ⇒ bỏ `try` là
tương đương ở 3.13; CI chạy 3.12 nên vẫn giết).
Toàn suite trên đột biến (`scripts/do_full_db.py`, clone `--no-hardlinks` mới mỗi đột biến, 3.12, `core.abbrev 7`,
09:11:54Z–09:32:13Z, log `log/full_db_312.log`): **L1a 259/259** · **L2b4 259/259** · **L1ef (= L1e + L1f gộp) 259/259** ·
**L3ce (= L3c + L3e gộp) 259/259** — mỗi lượt rc=0, vào 259 = ra 259, 0 `.pyc`, `git diff --numstat` đúng số dòng đột biến.
Chỉ khối A9 (sau :12260) gọi helper `_a9_*` (`rg`), nên 43/43 ca A9 là toàn bộ ca có thể giết L3c/L3e.

### 1.9 Hậu quả API của L2b4 (`scripts/do_api_l2b4.py`, 3.11 / 3.12 / 3.13 cùng kết quả)
`kiem(lease, None, None, bo_qua_han=True)`, lease dựng như `lease_mau()`:

| `lease_id` · hạn | nền ab457c6 | ứng viên | L2b4 |
|---|---|---|---|
| `yes` · còn hạn / hết hạn | rc0 / rc0 (lỗi gốc A1) | Chan8 / Chan8 | Chan8 / **rc0** |
| `1_000` · còn / hết | rc0 / rc0 | Chan8 / Chan8 | Chan8 / **rc0** |
| `'co khoang trang'` · còn / hết | Chan8 / Chan8 | Chan8 / Chan8 | Chan8 / **rc0** |
| `wp-ok-1` · còn / hết (đối chứng) | rc0 / rc0 | rc0 / rc0 | rc0 / rc0 |

L2b4 lùi cả hành vi NỀN ở hàng chuỗi sai dạng hết hạn (Chan8 → rc0) mà toàn suite vẫn 259/259.

### 1.10 Đường cùng cơ chế NGOÀI phạm vi (SPEC §5) — đo để chứng minh KHÔNG hồi quy (`scripts/do_ngoai_pham_vi.py`, 3.12)
| đường (sản phẩm 7a3a2f6) | nền | lượt 1 | ứng viên |
|---|---|---|---|
| `ai-dang-giu`: lease hợp lệ còn hạn, `da_bi_thay_the: 0x…` ⇒ :2356–:2357 `{lease.get('da_bi_thay_the')!r}` | rc=1 Traceback | rc=1 Traceback | rc=1 Traceback |
| `check`: `packet_issue: -0x…` ⇒ :1077 `{so!r}` | rc=1 Traceback | như nền | như nền |
| `kiem-thu-hoi-github`: bản ghi sổ `lease_id: 0x…` ⇒ :1420 `{lease_id!r}` | rc=1 Traceback | như nền | như nền |
| `check`: `granted_by: 0x…` ⇒ :1044 `str(lease["granted_by"])` | rc=1 Traceback | như nền | như nền |

Cả bốn: `ValueError: Exceeds the limit (4300 digits)…`, giống hệt ba cây. §5 SPEC: sổ thu hồi và "ép kiểu của các trường
khác" ngoài quyết định của chủ kho; lượt 1 đã khai ba trong số này là S2. Không xếp lớp; ghi ở §3 để packet sau dùng
`_repr_an_toan` đã có.

### 1.11 Đột biến lượt 1 chỉ đích danh — chạy lại trên 7a3a2f6 (không tin số lượt 1)
`scripts/db_h_luot1.py` lấy NGUYÊN neo H04–H09 từ `luot1/scripts/db_hint.py` (3.12): H04 repr thô ở hàm chung · H06
`return repr(...)` ngoài `try` · H07 D7 · H08 D8 · H09 D9 ⇒ **GIET `t218`** cả năm (`NEM ValueError` đúng vế); H05 nhãn
hàm chung luôn `sai kiểu` ⇒ GIET `t218` (vế D7), `t213`/`t215` QUA. R02b (= L2a) GIET `t219`; A11 (= L3a) GIET
`t217_a9_sai_kieu_chi_o_refs_remotes` (§1.8). ⇒ mọi đột biến lượt 1 nêu tên đều chết đúng ca bằng `TinHieuChotCa`.

### 1.12 A8 tĩnh có bị vòng 2 làm hỏng không — **không** (`scripts/tinh_a8_luot1.py` = bản sao `luot1/scripts/tinh_a8.py`,
đọc trước khi chạy; 3.11.15 / 3.12.3 / 3.13.12 cùng kết quả, rc=0, 0 `.pyc`)
nền: 201 ca, D 13, R 14, chỉ-lồng `{t70}`, G 14, G−D `{t202}`, D−G ∅, sổ 12, D−sổ `{t199}`. Ứng viên: **259 ca, D 14 (+`t207`),
R 15, chỉ-lồng `{t70}`, G 15, G−D `{t202}` = nền, D−G ∅, sổ 13, D−sổ `{t199}`; (S) 29 → 31, phần hơn = 2 × `Name.id`
`_chay_buoc_dang_that` trong thân `t207` ⇒ ĐƯỢC PHÉP; 0 lần mới ĐỎ.** Ba ca vòng 2 thêm không tham chiếu helper nào
(`mong`, `SO_BO_QUA`, literal `t193` không cần đổi); `t70`/`t193` xanh trong cả hai lượt toàn suite (§1.4).

## 2. Ba lớp lượt 1 — trạng thái sau vòng 2

| lớp lượt 1 (P lượt 1) | trạng thái | căn cứ đo |
|---|---|---|
| `thong-diep-lease-id-sai-dung-repr-tho` (P2) | **ĐÃ ĐÓNG** (hành vi) | §1.5: 9 lệnh CLI × {int lớn, bom, chuỗi sai dạng} × 3 bản Python đều kết thúc có kiểm soát, output ≤ 1053 byte, nhãn `sai dạng` đúng; §1.6: AST — mọi chỗ định dạng `lease_id` của lease đã qua hàm chung; §1.7: `_repr_an_toan` 11 dạng + bom k=6…12, 0 lần ném; §1.11: H04–H09 chết. Phần KHOÁ của bản vá hẹp hơn bản vá ⇒ tách lớp MỚI `khoa-t218-hep-cat-cau-truc-va-nhan` (§4). |
| `phu-nhanh-da-dang-chot-lease-id-mat-rang` (P2) | **CÒN MỞ** — vá đúng chỗ được chỉ, sót đường thứ ba | R02b chết ở `t219` (§1.8, 3 bản Python); nhưng L2b4 (miễn D1 khi `bo_qua_han` VÀ lease đã hết hạn) **sống toàn suite 259/259** và quan sát được ở API (§1.9) — đúng miền đầu vào mà `bo_qua_han` sinh ra để phục vụ; L2f (list/ánh xạ) sống 4 ca đích. Lời khai vòng 2 trong docstring `t190`/`t191`/`t219` ("răng của D1 trên đường `bo_qua_han` nằm ở `t219`") rộng hơn phép đo. |
| `a9-mien-refs-remotes-khong-co-ca` (P2) | **CÒN MỞ, thu hẹp** (P2 → P3) | A11/L3a chết ở ca mới (3 bản Python); L3b/L3d/L3f chết; nhưng L3c (chỉ `refs/remotes/origin`) và L3e (bỏ leaf `HEAD` không tượng trưng dưới `refs/remotes`) **sống 43/43** ca A9 ở 3 bản Python; L3e báo **rc=0 sạch** trên clone thường khi nhánh máy chủ `topic/HEAD` mang `lease_id: on` (§1.8). |

Không lớp nào TÁI PHÁT (đột biến lượt 1 nêu tên đều chết, §1.11). Không có lỗi HÀNH VI mới do vòng 2: biến thể `ok` giống nền
từng ô ở 9 lệnh × 3 bản Python (§1.5), không công cụ nào trong kho phân tích các chuỗi bị đổi (§1.3), A8 không đổi (§1.12),
ruff F delta ∅ (§1.2), toàn suite delta 0 (§1.4). Phần vòng 2 đưa vào mà CÓ khuyết: khoá `t218` hẹp hơn bản vá (lớp mới §4).

**Tỷ lệ vá thật 1→2.** Theo lớp: **1/3 = 33 %** (lớp 1 đóng; lớp 2, lớp 3 còn mở qua đường không ai chỉ). Theo đột biến lượt 1
nêu đích danh: 8/8 chết đúng ca (H04–H09, R02b, A11). Hai lớp mang lại slug cũ ở lượt 2 ⇒ đúng điều kiện S4 của lease
("cùng lớp finding lặp lại (PROTOCOL §12) ⇒ Review Rescue Checkpoint, hỏi chủ kho") — việc của phiên điều phối, không của
reviewer. Hình dạng chung của cả hai lớp còn mở và của lớp mới: **vá đúng chỗ được chỉ, ca khoá dựng đúng một điểm của
miền** (một hạn, một remote, một tên lá; một vị trí nhãn; độ dài thay vì cách cắt) — bài học "VÁ ĐÚNG CHỖ ĐƯỢC CHỈ RỒI BỎ
SÓT ĐƯỜNG THỨ BA" của CLAUDE.md, lần này trên chính HINT do reviewer cùng model viết ở lượt 1.

## 3. Ngoài phạm vi / quan sát (đo được, KHÔNG xếp lớp)
- Cùng cơ chế repr/`str()` thô, ngoài quyết định của chủ kho (SPEC §5), nền = lượt 1 = ứng viên (§1.10): bia mộ một chiều
  `{lease.get('da_bi_thay_the')!r}` (:2357), `packet_issue` `{so!r}` (:1077), sổ thu hồi `{lease_id!r}` (:1420) và
  `{dich!r}` (:1461), `granted_by` `str()` (:1044), `lease_expires_at_utc` `str()` trong `_doc_han` (:441, chưa đo riêng ở
  lượt này). Gợi ý cho packet kế: dùng lại `_repr_an_toan` đã có, và tránh `str()` trước kiểm kiểu.
- `con-tro-treo` với bom bí danh trong BẤT KỲ trường nào của lease còn hạn: 1,4–3,0 s ở k=6 ở cả ba cây (§1.5) — phép duyệt
  scalar `_cac_nhac_mo_ho` (:479–:496) đi hết cây bí danh; có từ nền, không phải repr, không riêng `lease_id`. Chưa đo k ≥ 7.
- Python 3.13: thông điệp của `lease_id` int lớn mang địa chỉ bộ nhớ `at 0x…` (§1.7) — không tất định giữa hai lượt chạy;
  3.11/3.12 (CI chạy 3.12) tất định. Không công cụ nào trong kho so chuỗi ấy (§1.3).
- Helper A9 (`lease_id={lid!r}` :12366, `{v!r}` :12299/:12301/:12307) vẫn dùng repr thô: `int` lớn ⇒ rc=2
  `KHONG_DO_DUOC: ValueError` (SPEC A9 cho phép "số vượt giới hạn chuyển đổi ⇒ rc=2"); bom bí danh ⇒ chuỗi lỗi nở theo
  luỹ thừa trong JSON (lượt 1 đã đo k=6). Đúng chữ SPEC A9 (vượt tài nguyên ⇒ rc=2 / OS kill ⇒ người gọi ghi KHÔNG ĐO
  ĐƯỢC), nên không xếp lớp.
- "tags" trong câu hỏi A9: tập ref của helper là `{refs/heads, refs/remotes}` (:12321–:12322) và miền SPEC A9 cũng chỉ hai
  miền ấy — `refs/tags` KHÔNG thuộc tập, nên "bỏ tags" không áp dụng; đột biến THÊM `refs/tags` (L3g) sống 43/43, đúng vì
  nới miền không trái SPEC.

## 4. Bảng lớp (lượt 2)

| slug | P | một câu |
|---|---|---|
| `phu-nhanh-da-dang-chot-lease-id-mat-rang` | P2 | Vòng 2 giết đúng đột biến được chỉ (R02b chết ở `t219`), nhưng mọi hàng âm của `t219` dựng lease CÒN hạn, nên đột biến miễn D1 khi `bo_qua_han` VÀ lease đã hết hạn — đúng đầu vào mà `bo_qua_han` sinh ra để phục vụ — sống toàn suite 259/259 dù quan sát được ở API (`kiem(..., True)` nhận `yes`/`1_000`/`'co khoang trang'` hết hạn, lùi cả nền ở hàng chuỗi). |
| `a9-mien-refs-remotes-khong-co-ca` | P3 | Bỏ `refs/remotes` nay chết ở ca mới, nhưng ca ấy dựng đúng một điểm (`origin`, lá không phải `HEAD`): thu hẹp về `refs/remotes/origin` hoặc bỏ lá `HEAD` KHÔNG tượng trưng dưới `refs/remotes` (trái chữ SPEC A9 "ref thường có hậu tố `/HEAD` vẫn phải quét") sống 43/43 ca A9 và toàn suite 259/259; bản sau báo rc=0 sạch trên clone thường khi nhánh máy chủ `topic/HEAD` mang `lease_id: on`. |
| `khoa-t218-hep-cat-cau-truc-va-nhan` (MỚI) | P3 | `t218` do vòng 2 thêm chỉ đo ĐỘ DÀI thông điệp và nhãn ở D7: đổi `_repr_an_toan` sang `repr()` dựng sẵn rồi cắt chuỗi (bom 9 cấp: 43 s / 2,2 GiB thay vì 0 s / 52 MiB), hay trả nhãn D8 về `sai kiểu` cùng câu `CHAN [12]` cũ, đều sống toàn suite 259/259. |

### Lớp `phu-nhanh-da-dang-chot-lease-id-mat-rang` (P2, CÒN MỞ)
- Biểu hiện: `ops/lease_publish_test.py` :11909–:11918 (`t219`: vòng lặp hàng âm gọi `_yaml_that(raw)` — mặc định
  `het_han=False` — chỉ hàng đối chứng :11916 là hết hạn); sản phẩm `ops/lease_publish.py` :1079 (D1 là lời gọi, ngoài vị
  từ `_la_chot`) và :1107–:1110 (hợp đồng "`bo_qua_han` bỏ ĐÚNG MỘT chốt — chốt HẠN"). Docstring vòng 2: `t190` :9416–:9418
  ("răng của chốt `lease_id` trên đường `bo_qua_han` nằm ở `t219`"), `t191` :10318–:10320, `t219` :11907–:11908 — rộng hơn
  phép đo của `t219`.
- Phép đo: §1.8 (L2b4 QUA 17 ca đích; L2b/L2b2/L2b3 chỉ "chết" vì lý do vô can — `_la_chot` thấy `_doc_han`, hoặc đổi mã
  hàng "hạn hỏng dạng" — tức tín dụng giả), toàn suite L2b4 259/259 (3.12), `db_khoa` 3.11/3.13 QUA; §1.9 bảng API.
- Hướng vá (HINT nhóm 1): mọi hàng âm của `t219` chạy cả `het_han=False` lẫn `het_han=True`, thêm hàng list `[wp-x]` và ánh
  xạ `{x: 1}`. Đo trên bản vá (§6): L2b4 GIET (`… hết hạn=True: phải rc=8 … được rc=0`), L2f GIET (`[wp-x]`), R02b/L2c/L2d vẫn
  GIET; ca vẫn xanh trên ứng viên.

### Lớp `a9-mien-refs-remotes-khong-co-ca` (P3, CÒN MỞ — thu hẹp từ P2)
- Biểu hiện: `ops/lease_publish_test.py` :12483–:12495 (ca mới của vòng 2: lease sai kiểu chỉ ở `refs/remotes/origin/xa`);
  helper :12321–:12326 (miền `refs/heads`, `refs/remotes`; chỉ bỏ `…/HEAD` khi tượng trưng). Không ca nào đặt lease sai kiểu
  dưới một remote khác `origin`, hay ở một `…/HEAD` không tượng trưng dưới `refs/remotes`.
- Phép đo: §1.8 (L3c, L3e QUA 43/43 ở 3.11/3.12/3.13; L3ce toàn suite 259/259), `do_a9_mien.py` (clone thường: L3e rc=0 sạch;
  L3c bỏ sót `refs/remotes/upstream/xa`).
- Vì sao hạ P2 → P3: đường chính (bỏ cả `refs/remotes`, ảnh hưởng mọi clone thường — lượt 1 đo 1 ref thay 482) nay có ca và
  chết; phần còn hở cần đầu vào hiếm hơn (remote thứ hai; nhánh máy chủ có lá `HEAD`), và lượt quét kho thật của executor
  chạy trên mirror (`refs/heads/*`) nơi hai đột biến này không đổi kết quả.
- Hướng vá (HINT nhóm 2): hai ca `t217_a9_sai_kieu_chi_o_remote_khong_phai_origin` (`refs/remotes/upstream/xa`) và
  `t217_a9_sai_kieu_chi_o_ref_thuong_remotes_HEAD` (`refs/remotes/origin/topic/HEAD` không tượng trưng, kèm HEAD tượng trưng
  phải bị bỏ). Đo trên bản vá: L3c GIET ca thứ nhất, L3e GIET ca thứ hai, L3a/L3d GIET cả ba ca remote.

### Lớp MỚI `khoa-t218-hep-cat-cau-truc-va-nhan` (P3) — do vòng 2 đưa vào
- Biểu hiện: `ops/lease_publish_test.py` :12239–:12243 (vế bom chỉ đòi `len(td) < 1000`), :12253–:12256 (vế D8 chỉ đếm
  tiền tố `DU_BAO: KHÔNG_XÁC_ĐỊNH lease_id `), :12248 (`_e` của D7 không được đọc). Sản phẩm đúng: `_repr_an_toan`
  :299–:314 cắt theo cấu trúc; D8 :2197 và `CHAN [12]` :2366 đã sửa nhãn.
- Phép đo: §1.7/§1.8 — L1a, L1b QUA `t218` ở 3 bản Python; L1a toàn suite 259/259; giá L1a k=9 = 43,190 s / 2187 MiB RSS
  (ứng viên 0,000 s / 52 MiB); L1e, L1f QUA 7 ca đích; L1ef toàn suite 259/259.
- Không P2: sản phẩm hiện tại đúng; hỏng chỉ khi có thay đổi sau này, và thất bại khi ấy là fail-close (chậm/hết bộ nhớ,
  hoặc nhãn sai trong chẩn đoán), không phải cấp nhầm quyền.
- Hướng vá (HINT nhóm 3): `t218` đòi thông điệp bom KHÔNG chứa lá `'x'` (cắt theo cấu trúc), đòi đúng 1 dòng D8 `sai kiểu`
  và 1 dòng D8 `sai dạng 'co khoang trang'`, đòi câu `CHAN [12]` chứa `lease_id không hợp lệ`. Đo trên bản vá: L1a, L1b,
  L1e, L1f GIET `t218` đúng vế; H-cũ (L1c ở 3.11/3.12, L1g) vẫn GIET.

## 5. KHÔNG ĐO ĐƯỢC
- Windows / nền `nt` thật; CI GitHub; máy chủ GitHub live; comment cấp quyền #678 và danh tính người ký (#566).
- Lượt quét A9 trên kho thật và `git fsck --full`: KHÔNG chạy lại ở lượt này (vòng 2 không đổi helper A9 — `diff-l1-l2.patch`
  chỉ thêm một ca; mirror `x678/mirror.git` của executor không có trong `$R`).
- Model/effort thực sự phục vụ lượt review này (cấu hình tự khai Claude Opus 5.5 `claude-opus-5-5` effort max).
- Công cụ ngoài kho có thể phân tích chuỗi thông điệp đã đổi (scratch của phiên khác).
- `con-tro-treo` với bom k ≥ 7; `_doc_han` với int lớn (chỉ đọc mã, không chạy).
- Toàn suite trên đột biến chỉ chạy ở 3.12 (đột biến ca đích chạy ở 3.11/3.12/3.13).

## 6. HINT (`goi/HINT.patch`, 123 dòng, 3 nhóm, chỉ sửa `ops/lease_publish_test.py`, đường dẫn repo-relative không tiền tố)
Dựng bằng `w.aDKYWW/scripts/dung_hint.py` (s0 = tệp test của 7a3a2f6 → s1 → s2 → s3; mỗi neo phải duy nhất; mỗi nhóm một
`# lop:` + `# hang:`). Chuỗi thoát trong mã sinh ra đã đo bằng `repr()` sau khi ghi (`"lease_id: on\n"` một dấu chéo, như
:12467). Nhóm 1 `phu-nhanh-da-dang-chot-lease-id-mat-rang` (P2) · nhóm 2 `a9-mien-refs-remotes-khong-co-ca` (P3) · nhóm 3
`khoa-t218-hep-cat-cau-truc-va-nhan` (P3). Không ca mới/sửa nào dùng `_chay_buoc_dang*` ⇒ không đổi `mong`/`SO_BO_QUA`/
literal `t193`.

Dry-run trên bản sao (`git archive 7a3a2f6 ops/lease_publish.py ops/lease_publish_test.py` vào mktemp, từ gốc bản sao;
`scripts/do_kiem_hint.py`, log `log/kiem_hint_cuoi.log`):
```
$ patch -p0 --fuzz=0 --dry-run < goi/HINT.patch
checking file ops/lease_publish_test.py
checking file ops/lease_publish_test.py
Hunk #1 succeeded at 12496 (offset -6 lines).
checking file ops/lease_publish_test.py
Hunk #1 succeeded at 12215 (offset -6 lines).
Hunk #2 succeeded at 12244 (offset -6 lines).
DRYRUN_RC=0
```
(offset −6 vì dry-run đo mọi nhóm trên tệp GỐC; nhóm 1 thêm 6 dòng phía trên.) Băm hai tệp trước = sau dry-run.
Áp THẬT trên bản sao khác: `APPLY_RC=0`, tệp test sau áp trùng TỪNG BYTE `hint/s3.py`, sản phẩm không đổi, 0 `.orig`/`.rej`;
ruff F tệp test 9 = 9 (thêm ∅ bớt ∅); chuỗi con `chay_buoc_` 32 = 32; `^@ca` 259 → 261. Ca đích trên bản đã vá (3.11 và 3.12):
55/55 QUA (`t219`, `t218`, 45 `t217_*`, `t204`, `t190`, `t191` "13 chốt", `t216` 12/12, `t213`, `t215`, `t70`, `t193`), 0 `.pyc`.

Hai chiều (`scripts/db_hai_chieu.py`, `HINT_TRUOC=goi/HINT.patch`, mỗi đột biến một bản sao mới; log `log/hai_chieu_cuoi_*.log`):
đối chứng bản đã vá 10/10 QUA ở 3.11/3.12/3.13; **15/15 đột biến GIET bằng `TinHieuChotCa` đúng ca ở 3.11 và 3.12**
(L1a/L1b/L1e/L1f/L1g/L1c → `t218`; L2a/L2b4/L2c/L2d/L2f → `t219`; L3a/L3d → ba ca remote; L3c → ca `upstream`; L3e → ca
`topic/HEAD`), 0 tín dụng giả; 3.13: 14/15 (L1c tương đương ở 3.13, §1.7).
Toàn suite trên bản đã vá (`scripts/do_ab_hint.sh`, log `log/ab_hint.log` mở đầu bằng sha256 HINT `477c360a…274e`): hai
clone `--no-hardlinks` 7a3a2f6 dựng trong MỘT vòng lặp (09:47:17Z–09:47:20Z), `PATCH_RC 0` cả hai, `--numstat` `61 8
ops/lease_publish_test.py`; chạy song song 09:47:20Z–09:56:21Z: **3.11.15 261/261 · 3.12.3 261/261**, rc=0, bỏ qua 0, vào 261 =
ra 261 = `^@ca` 261, 0 `.pyc`, porcelain 1 (đúng tệp đã vá); năm ca mới/sửa (`t218`, `t219`, ba ca remote A9) và `t70`, `t193`
QUA; `t191` "13 chốt"; `t216` 12/12. (Một lượt trước đó trên bản HINT nháp `338c0c1d…`, khác bản cuối CHỈ ở docstring
`t218`, cũng 261/261 ở cả hai bản — log `log/ab_hint_HINT_cu_338c0c1d.log`; không dùng làm bằng chứng cho bản cuối.)

## 7. Kết luận
`changes_requested` — **0 P1 · 1 P2 · 2 P3**:
`phu-nhanh-da-dang-chot-lease-id-mat-rang` (P2, còn mở) · `a9-mien-refs-remotes-khong-co-ca` (P3, còn mở, thu hẹp từ P2) ·
`khoa-t218-hep-cat-cau-truc-va-nhan` (P3, mới — khoá của vòng 2 hẹp hơn bản vá).

Kiểm lời khai của phiên điều phối: suite 259/259 ở 3.11 và 3.12 trên 7a3a2f6 — **có** (§1.4); nền 201/201 — **có**; ruff F
delta ∅ — **có** (§1.2); `t191` in "13 chốt" — **có**, và lý do "D1 là lời gọi hàm" — **có** (đổi tên thuần ⇒ `KHONG_CHAM`,
§1.8); "răng của D1 trên đường `bo_qua_han` chuyển sang `t219`" — **có MỘT PHẦN**: chỉ cho lease còn hạn (L2b4, §1.8–§1.9).

Cả ba lớp còn mở đều là KHOÁ (ca test) hẹp hơn hợp đồng; không lớp nào là lỗi hành vi của mã hiện tại: sản phẩm từ chối
`lease_id` hết hạn dưới `bo_qua_han` (§1.9), helper A9 quét đúng remote khác `origin` và `…/HEAD` thường (§1.8, `do_a9_mien`),
`_repr_an_toan` cắt theo cấu trúc (§1.7). HINT 3 nhóm, chỉ sửa tệp test, đóng cả ba khi áp: dry-run rc=0, toàn suite
261/261 ở 3.11 và 3.12, 15/15 đột biến chết đúng ca. Mức assurance của lượt này: `review_deferred` (subagent cùng họ
executor, và là cùng model đã viết HINT lượt 1); land vẫn đòi `human_audited` của chủ kho.
