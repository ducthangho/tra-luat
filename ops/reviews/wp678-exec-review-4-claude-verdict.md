verdict: changes_requested
reviewed_sha: 6a7220a6b4d11b3c173ce20812825b57dd706668
spec_sha256: f39091a1d2be7629a11eb53b7daf3f076ce91f701012f7093108a98e91d140cc
reviewer_provider: anthropic
reviewer_model: claude-opus-5-5 (subagent review-opus-max, tự khai)
execution_surface: claude_code_subagent
che_do: subagent_trong_phien_dieu_phoi

> TRẠNG THÁI LƯỢT: XONG (12:02Z–13:45Z 08-10-2026). Tệp ghi TĂNG DẦN; dòng `verdict` (giữ chỗ `blocked` fail-close trong lúc
> chạy) chốt sau §7 "Kết luận".
> Tóm tắt: 0 P1 · 0 P2 · 1 P3 — `a9-mien-refs-remotes-khong-co-ca` (P3, CÒN MỞ qua đường mới: V1 nửa `refs/remotes` của L3h,
> V2/V3/V6 cách viết phép so leaf); `khoa-t218-hep-cat-cau-truc-va-nhan` ĐÃ ĐÓNG. Tỷ lệ vá thật 3→4 theo lớp 1/2; đột biến lượt 3
> nêu đích danh 14/14 chết đúng ca. HINT: `goi/HINT.patch` sha256 `adfaab4b…b0b3` (dry-run `patch -p0 --fuzz=0` rc=0, §1.7).

Reviewer tự khai: Claude Opus 5.5 (model id `claude-opus-5-5`, effort max), chạy như subagent trong phiên điều phối
Claude Code. KHÔNG phải codex. Không mạng, không đăng GitHub, không commit/push; `cay-kho/` chỉ đọc. Lượt thi hành 4
(lượt vượt giới hạn DUY NHẤT theo quyết định chủ kho #678 6059219849 — lời khai của PROMPT, KHÔNG ĐO ĐƯỢC từ đây).

## 0. Tiền kiểm (đã chạy, 12:02Z–12:04Z)
```
$ sha256sum SPEC.md lease.yaml luot3/VERDICT.md luot3/HINT.patch
f39091a1d2be7629a11eb53b7daf3f076ce91f701012f7093108a98e91d140cc  SPEC.md
7a981529da52ba54ccf8a153af4f92f4d8ab28feae891859cb6071bf88a9748d  lease.yaml
a6b1e3bd9b2f9d38b0fce80da2effaf7a968bb0004e2516fc556cdde9c570bd6  luot3/VERDICT.md
55caec390d086e8985f5085de2f333f84afd32fb829b48a40289b60c694f23b8  luot3/HINT.patch
$ GIT_OPTIONAL_LOCKS=0 git -C cay-kho rev-parse HEAD 'HEAD^{tree}'
6a7220a6b4d11b3c173ce20812825b57dd706668
839eeecc3c2f7bc00da16622d31b4c6a97ac8e1f
$ GIT_OPTIONAL_LOCKS=0 git -C cay-kho status --short      # rỗng, rc=0
$ wc -l diff-l3-l4.patch diff-base-head.patch              # 119 · 1549
```
Khớp PROMPT.md (spec, VERDICT/HINT lượt 3, HEAD, tree, cây sạch, số dòng hai diff); `lease.yaml` = giá trị ba lượt trước
ghi (`7a981529…748d`). ⇒ không `blocked` vì tiền kiểm. (`GIT_OPTIONAL_LOCKS=0` để `status` không ghi lại index của
`cay-kho`.) Công cụ: Python 3.11.15 / 3.12.3 / 3.13.12 (PyYAML 6.0.1, `get_int_max_str_digits()` = 4300 cả ba), 3.14 vắng;
git 2.43.0, ruff 0.15.8, GNU patch 2.7.6, shellcheck 0.9.0, actionlint 1.7.7; 4 CPU, 15 GiB. Thư mục làm việc
`$R/w4.NtdOJ8` (mktemp), HOME riêng `w4.NtdOJ8/home` (`core.abbrev 7` `--global`), `PYTHONDONTWRITEBYTECODE=1`.

## 1. Nhật ký đo (ghi tăng dần; mọi số kèm lệnh + rc thật)

### 1.1 Vòng 4 có đúng là áp NGUYÊN VĂN `luot3/HINT.patch`, chỉ tệp test không — **có** (12:04Z)
```
$ git -C cay-kho log --format='%H %P %s' -6        # 6a7220a ← 0dd86c6 ← 7a3a2f6 ← f809249 ← ab457c6 (merge PR #712)
$ git -C cay-kho diff 0dd86c6 6a7220a | sha256sum    # e44093ab…168c = sha256 diff-l3-l4.patch
$ git -C cay-kho diff ab457c6 6a7220a | sha256sum    # 784cc003…fe6a18 = sha256 diff-base-head.patch
$ git -C cay-kho diff --numstat 0dd86c6 6a7220a      # 86 1 ops/lease_publish_test.py   (MỘT tệp)
$ git -C cay-kho diff --numstat ab457c6 6a7220a      # 109 19 ops/lease_publish.py · 1132 19 ops/lease_publish_test.py
$ git -C cay-kho ls-tree 6a7220a / 0dd86c6 ops/lease_publish.py   # cùng blob ca48011 (sản phẩm không đổi từ vòng 2)
$ cd w4.NtdOJ8/kiem_hint3 && git -C cay-kho archive 0dd86c6 ops/lease_publish.py ops/lease_publish_test.py | tar -x \
    && patch -p0 --fuzz=0 < luot3/HINT.patch        # PATCH_RC=0, 2 lần "patching file", 0 .orig/.rej
ops/lease_publish.py      ap=d8079330007ab6ba 6a7220a=d8079330007ab6ba KHOP
ops/lease_publish_test.py ap=a6765161065161b1 6a7220a=a6765161065161b1 KHOP
```
Write set vẫn đúng 2 tệp; `6a7220a` = `0dd86c6` + HINT lượt 3 từng byte; sản phẩm (`ops/lease_publish.py`, blob `ca48011`) không đổi
từ `7a3a2f6`. HINT lượt 3 do CHÍNH model này viết (cùng `claude-opus-5-5`), nên mọi kết luận dưới đo lại trên `6a7220a`, không dựa
vào phần "hai chiều" §1.11 của `luot3/VERDICT.md`.

### 1.2 Ruff F (đa tập (tệp, code, message)) — delta ∅ (`scripts/ruff_delta.py`, log `log/ruff.log`, 12:13Z)
`ruff check --no-cache --select F ops/lease_publish.py ops/lease_publish_test.py --output-format json` trên ba cây `git archive`
(`w4.NtdOJ8/cay/{nen,l3,ung}`):
```
nen ab457c6 rc=1 tong=11 theo_ma={'F401': 7, 'F541': 2, 'F841': 2} theo_tep={'lease_publish.py': 2, 'lease_publish_test.py': 9}
l3 0dd86c6 rc=1 tong=11 theo_ma={'F401': 7, 'F541': 2, 'F841': 2} theo_tep={'lease_publish.py': 2, 'lease_publish_test.py': 9}
ung 6a7220a rc=1 tong=11 theo_ma={'F401': 7, 'F541': 2, 'F841': 2} theo_tep={'lease_publish.py': 2, 'lease_publish_test.py': 9}
ung - nen: 0 ∅ · nen - ung: 0 ∅ · ung - l3: 0 ∅ · l3 - ung: 0 ∅
```
Khớp lời khai điều phối "ruff F delta ∅" — **có**. (2 F841 nền là `executor_surface`/`executor_transport` của wp709, SPEC A8.)

### 1.3 Đột biến lượt 3 NÊU ĐÍCH DANH (và lượt 2, kiểm TÁI PHÁT) trên 6a7220a (12:14Z–12:23Z)
Giàn viết mới cho lượt 4 (`scripts/chay_ca.py`, `scripts/db.py`; neo gõ lại vào `scripts/db_ten.py` từ `luot3/scripts/db_r3_*.py`
đọc như DỮ LIỆU, không `runpy` tệp lượt trước): mỗi đột biến một bản sao `git archive 6a7220a ops .github` mới trong
`w4.NtdOJ8/mut` (cay-kho chỉ đọc), mỗi neo ĐÚNG 1 lần và băm tệp phải đổi (`scripts/kiem_neo.py` kiểm tĩnh trước: 37/37 neo
OK, bản đột biến parse được). Ca chạy bằng `chay_ca.py` nạp CHÍNH module test của bản sao (`ops/` vào `sys.path`). Phân hạng:
`GIET` = `TinHieuChotCa` của module **và** khung `@ca` gần chỗ ném nhất là CHÍNH ca đích (in `hàm:dòng` gọi `chot`) ·
`GIET_CA_KHAC` · `TIN_DUNG_GIA` (ngoại lệ khác) · `QUA`. Log `log/db_l3ten_312.log`, `log/db_ten_nhanh_311.log`,
`log/db_ten_nhanh_312.log`, `log/db_ten_nhanh_313.log`. Đối chứng `DC` (không đột biến): **54/54 QUA** ở 3.12 (`t218 t213 t215 t214 t219 t204 t216` + 47
`t217_*`), 53/53 ở 3.11 và 3.13 (bỏ `t216`). Cả bốn log: `GIET_CA_KHAC` 0, `TIN_DUNG_GIA` 0, `BO_QUA_NEN` 0, 0 `.pyc` mọi bản sao.

| đột biến lượt 3 (neo lượt 3) | 3.11 · 3.12 · 3.13 — ca chết · `hàm:dòng` gọi `chot` · đầu thông điệp |
|---|---|
| **L3h** `if symref:` | **GIET** đúng 1 ca `t217_a9_sai_kieu_chi_qua_ref_tuong_trung_khong_phai_HEAD` (`_a9_chot:12502` "phải rc=1 …; được rc=0"), 46 ca A9 kia QUA |
| **L3i** `if ten == "refs/remotes/origin/HEAD":` | **GIET** đúng 1 ca `t217_a9_sai_kieu_chi_o_origin_HEAD_khong_tuong_trung` (`_a9_chot:12502`) |
| G2 (L3h ∪ L3i) | GIET đúng hai ca mới ấy |
| **L1h** repr đầy đủ, dài thì reprlib | **GIET** `t218` :12276 "`_repr_an_toan`: … lá sâu bị chạm 1 lần" |
| L1i `_ = len(repr(...))` | GIET `t218` :12276 "`_repr_an_toan` …" |
| **L1k** nhãn D7/D8 `repr()[:120]`+`try` | **GIET** `t218` :12276 "`_nhan_lease_id_sai` … chạm 1 lần" |
| **L1l** D9 `repr()[:120]`+`try` | **GIET** `t218` :12276 "`_lease_id_hien_thi` … chạm 1 lần" |
| **L1m** · **L1n** đường in D7 · D8 vòng qua nhãn | **GIET** `t218` :12306 "D7/D8: … chạm 2 lần" (cả hai) |
| **L1o** · **L1p** hai đường in D9 | **GIET** `t218` :12321 "D9: … chạm 1 lần" (cả hai) |
| G3 · G3b · G3c | GIET :12276 (1 lần) · :12306 (4 lần) · :12321 (2 lần) |

Đột biến lượt 2 nêu đích danh (3.11, 3.12, 3.13; ca đích nhanh — 3.12 giống hệt 3.11 từng cặp (ca, `hàm:dòng`), `diff` rc=0): L1a/L1b GIET `t218` :12258 (vế `'x'`); L1c GIET :12244 ở 3.11, **QUA
ở 3.13** (tương đương — `reprlib` 3.13 không ném ở `int` lớn, như lượt 2/3 đã ghi; CI chạy 3.12); L1e :12293; L1f :12287; L1g
:12284 + `t213` :12070 + `t215` :12115; L2a L2b L2b2 L2b3 L2b4 L2c L2d L2e L2f GIET `t219` :11919 đúng hàng (L2d ở
`'co khoang trang'`, L2f ở `[wp-x]`, họ L2b ở `hết hạn=True`; L2e thêm `t204` :11892); L3a/L3d/L3f GIET 4 ca remote; L3b 29 ca;
L3c đúng `…_remote_khong_phai_origin`; L3e đúng `…_ref_thuong_remotes_HEAD` + `…_origin_HEAD_khong_tuong_trung`.
**Khác lượt 3: L3g (THÊM `refs/tags`, nới miền) nay GIET** `t217_a9_sai_kieu_chi_qua_ref_tuong_trung_khong_phai_HEAD` :12616 —
ca mới ghim `sorted(refs) == [alias, main]`, tức ghim đúng miền SPEC A9 "`refs/heads/*` và `refs/remotes/*`"; xem §3.
⇒ Mọi đột biến lượt 3 nêu đích danh (L3h L3i · L1h L1k L1l L1m L1n L1o L1p, kèm L1i, G2 G3 G3b G3c) chết bằng `TinHieuChotCa`
đúng ca, đúng vế ở 3.11, 3.12, 3.13. **Không lớp nào TÁI PHÁT** (đột biến lượt 2 nêu đích danh cũng chết như lượt 3 đo).

### 1.4 Câu 3 — toàn suite nền vs ứng viên, hai vế dựng trong MỘT lệnh (`scripts/do_ab.sh chinh`, log `log/ab_chinh.log`)
Một vòng lặp dựng 4 clone `--no-hardlinks` từ `cay-kho` (nền `ab457c6` / ứng viên `6a7220a` × 3.11/3.12), `checkout --detach`,
`core.abbrev 7` (repo + `.gitconfig` trong HOME riêng mỗi vế), 12:11:07Z–12:11:14Z; rồi mỗi bản Python chạy song song hai vế
`env -u GITHUB_ACTOR HOME=… TMPDIR=… PYTHONDONTWRITEBYTECODE=1 PATH=<bin có python/python3 trỏ đúng bản>:$PATH python3
ops/lease_publish_test.py` (12:11:14Z–12:27:54Z; trong lúc ấy giàn đột biến §1.3 chạy song song ở `nice -n 10`). Log nguyên văn:
```
KQ nen 3.11 rc=0 giay=421 tong_ket=[lease_publish: 201/201 đạt; đã chạy=201, bỏ qua=0] vao=201 ra=201 QUA=201 DO=0 BO_QUA=0 at_ca=201 pyc=0 porcelain_ignored=0 stderr_dong=44
KQ ung 3.11 rc=0 giay=458 tong_ket=[lease_publish: 263/263 đạt; đã chạy=263, bỏ qua=0] vao=263 ra=263 QUA=263 DO=0 BO_QUA=0 at_ca=263 pyc=0 porcelain_ignored=0 stderr_dong=44
KQ nen 3.12 rc=0 giay=501 tong_ket=[lease_publish: 201/201 đạt; đã chạy=201, bỏ qua=0] vao=201 ra=201 QUA=201 DO=0 BO_QUA=0 at_ca=201 pyc=0 porcelain_ignored=0 stderr_dong=72
KQ ung 3.12 rc=0 giay=542 tong_ket=[lease_publish: 263/263 đạt; đã chạy=263, bỏ qua=0] vao=263 ra=263 QUA=263 DO=0 BO_QUA=0 at_ca=263 pyc=0 porcelain_ignored=0 stderr_dong=72
```
(`vao`/`ra`/`QUA` đếm dòng `>>> vao`/`<<< ra` ở ĐẦU dòng — cấp suite; dòng `[A]`/`[B]` của tiến trình con trong `t125` không tính;
`porcelain_ignored` = `git status --porcelain --ignored` sau lượt.) **Delta ca đỏ = 0** ở cả hai bản; 263 = số `^@ca` đếm tĩnh.
Khớp lời khai điều phối "263/263 ở 3.11 và 3.12; nền 201/201" — **có**. stderr nền vs ứng viên sau khi chuẩn hoá tiền tố clone,
tên thư mục tạm và số dòng: `diff` rc=0 ở cả hai bản (44 = 44; 72 = 72, cùng 19 `SyntaxWarning` có sẵn từ nền).
Thời gian ca mới/sửa của vòng 4 (ứng viên 3.11 | 3.12): `t218` 0,694 | 0,698 s (lượt 3 đo 0,386 | 0,488 s trên 0dd86c6 — vòng 4
thêm hai lời gọi CLI và một kho tạm); `t217_a9_sai_kieu_chi_qua_ref_tuong_trung_khong_phai_HEAD` 0,357 | 0,350 s;
`t217_a9_sai_kieu_chi_o_origin_HEAD_khong_tuong_trung` 0,408 | 0,431 s; 47 ca `t217_*` trung bình 0,307 | 0,339 s. Ca chậm nhất
vẫn là `t125` (251,1 | 297,0 s; nền 231,6 | 279,4 s — nó chạy lại TOÀN suite hai lần nên lớn theo số ca) và `t191` (81,4 | 109,2 s;
nền 82,7 | 110,4 s, in "13 chốt"). Không ca nào chậm bất thường.

### 1.5 Tự liệt kê đường cùng cơ chế trên 6a7220a (`scripts/db_moi.py`, log `log/db_moi_31{1,2,3}.log`; hậu quả `scripts/do_a9_hau_qua.py`, log `log/a9_hau_qua_312.log`; toàn suite `scripts/do_full_db.py a9gop`, log `log/full_a9gop.log`)
**Lớp a9.** Vị từ bỏ ref của helper (`ops/lease_publish_test.py:12392`, `if ten.rsplit("/", 1)[-1] == "HEAD" and symref:`) chia
miền SPEC A9 thành 8 ô (tiền tố `heads`/`remotes` × leaf `HEAD`/khác × tượng trưng/thường); SPEC đòi bỏ ĐÚNG 2 ô (leaf `HEAD` ∧
tượng trưng), quét 6 ô kia. Ca hiện có sau vòng 4 phủ 5/6 ô phải quét (`cuc-bo`, `topic/HEAD`, `alias`→tag mới; `origin/xa`,
`upstream/xa`, `origin/topic/HEAD`, `origin/HEAD` thường mới); **ô `remotes` / leaf khác / tượng trưng không có ca nào**. Ngoài ô,
cách viết phép so leaf bằng thành ngữ chuỗi cũng không có điểm phân biệt. Đột biến (mỗi cái thay đúng dòng :12392), 47 ca `t217_*`:
```
                                                           3.11      3.12      3.13
V1  if symref and ten.startswith("refs/remotes/"):          QUA 47    QUA 47    QUA 47
V2  if ten.endswith("HEAD") and symref:                     QUA 47    QUA 47    QUA 47
V3  if "HEAD" in ten and symref:                            QUA 47    QUA 47    QUA 47
V6  if ten.rsplit("/", 1)[-1].upper() == "HEAD" and symref: QUA 47    QUA 47    QUA 47
V9  if symref and symref.startswith(("refs/heads/", "refs/remotes/")):            QUA 47 ×3   (bỏ ref tượng trưng có ĐÍCH trong miền)
V10 if symref and (leaf == "HEAD" or symref.startswith(("refs/heads/", "refs/remotes/"))):  QUA 47 ×3
V4 endswith("/HEAD") · V5 split("/")[-1] · V11 symref.startswith("refs/") · F1 mẫu "refs/heads/","refs/remotes/"   QUA 47 ×3 (TƯƠNG ĐƯƠNG)
V7 chỉ bỏ HEAD tượng trưng dưới remotes · V8 chỉ khi đúng 3 dấu "/"                                             QUA 47 ×3 (NỚI: bỏ ít hơn)
```
Hậu quả (kho tạm, `--quet-a9` qua CLI, helper = `git archive 6a7220a` + neo duy nhất, 3.12; mỗi kịch bản một kho, commit mang
`lease_id: on` CHỈ tới được qua đích ghi bên phải):
```
# S5: refs/heads/main-> | refs/remotes/upstream/alias->refs/tags/t | refs/tags/t->
# S6: refs/heads/main-> | refs/heads/xHEAD->refs/tags/t | …   S7: refs/heads/head->refs/tags/t · S8: refs/heads/HEAD-x->refs/tags/t
# S9: refs/remotes/upstream/alias->refs/remotes/upstream/xa (đích TRONG miền) · S1: refs/heads/alias->refs/tags/t (ca vòng 4)
ung  S5: rc=1 refs=['refs/heads/main', 'refs/remotes/upstream/alias'] loi=[('lease_id=True', ['refs/remotes/upstream/alias'])]
ung  S6/S7/S8/S1: rc=1 (lỗi gắn đúng ref tượng trưng)   ·   ung S9: rc=1 loi refs=[alias, xa]
V1   S5: rc=0 so_ref=1 refs=['refs/heads/main'] loi=[]          <- báo SẠCH; S6/S7/S8/S1 như ứng viên; S9 rc=1 mất `alias` khỏi refs
V2   S6: rc=0 so_ref=1 refs=['refs/heads/main'] loi=[]          <- báo SẠCH (xHEAD)
V3   S6: rc=0 · S8: rc=0                                        <- báo SẠCH (xHEAD, HEAD-x)
V6   S7: rc=0                                                   <- báo SẠCH (head)
V9/V10  S5…S8, S1: rc=1 như ứng viên; S9: rc=1 nhưng `refs/remotes/upstream/alias` vắng khỏi refs (chỉ đổi DANH SÁCH ref)
L3h  S5/S6/S7/S8/S1: rc=0 (đối chiếu: đột biến lượt 3, nay chết ở S1 nhờ ca vòng 4)
```
Toàn suite (3.12, clone `--no-hardlinks` 6a7220a + neo, dựng cả hai trong MỘT vòng lặp, 12:35:37Z–12:45:33Z):
```
DUNG G4-V1-V2-V3-V6 numstat=[1 1 ops/lease_publish_test.py] ok=True · DUNG V1-… numstat=[1 1 ops/lease_publish_test.py] ok=True
KQ V1-bo-moi-ref-tuong-trung-duoi-remotes rc=0 giay=590 tong_ket=['lease_publish: 263/263 đạt; đã chạy=263, bỏ qua=0'] vao=263 ra=263 khong_QUA=0 pyc=0 porcelain=1
KQ G4-V1-V2-V3-V6                         rc=0 giay=592 tong_ket=['lease_publish: 263/263 đạt; đã chạy=263, bỏ qua=0'] vao=263 ra=263 khong_QUA=0 pyc=0 porcelain=1
```
G4 = `if symref and (ten.startswith("refs/remotes/") or "HEAD" in ten or ten.rsplit("/", 1)[-1].upper() == "HEAD"):` (hợp V1, V3,
V6; V2 ⊂ V3). Mọi ca A9 chỉ đòi một ref CÓ/KHÔNG trong tập quét và G4 vẫn bỏ HEAD tượng trưng của đối chứng, nên G4 sống ⇒ từng
biến thể con sống. Người gọi helper: 32 dòng, min :12337 max :12975, đều trong khối A9 (`rg` trên 6a7220a); `--quet-a9` không có
người gọi nào ngoài tệp test (`rg` trên cây `git archive 6a7220a ops .github`).

**Lớp t218.** Tám chỗ định dạng `lease_id` thô trong sản phẩm (`rg lease_id … | rg '\{|repr\(|str\('` trên 6a7220a, đọc từng dòng):
thân `_repr_an_toan` :299–314, `_nhan_lease_id_sai` :319, thông điệp `_lease_id_hop_le` :336 (D1–D4 đi qua), `_lease_id_hien_thi`
:2375, in D8 :2197, in D7 :2348, in D9 :2389/:2390 và :2393/:2394 — đúng tám đường mà lính canh của vòng 4 đi qua (4 gọi thẳng, 4
qua CLI); các dòng khác in `lease_id` ĐÃ hợp lệ (:900/:909 D3, :1295 D4, :2306, :2321, :2356, :2361) hoặc thuộc sổ thu hồi (:1420,
:1461, :2166 — ngoài phạm vi §5). Cách dựng đầy đủ KHÁC `repr()` trong `_repr_an_toan` (4 ca đích, 3.11/3.12/3.13 cùng kết quả):
K1 `reprlib.repr` mặc định module GIET :12258 · K3 `json.dumps(default=str)` GIET :12276 (lính canh) + `t213` :12070 · K4
`json.dumps(default=<tên kiểu>)` (cố ý né `repr`) GIET :12284 + `t213` :12070 (nháy kép của JSON lệch định dạng nhãn) · K7 `str()`
GIET :12258 · K8 D9 `{…!s:.120}` GIET :12249 · **K2 `pprint.pformat(depth=2)` QUA 4/4** — nhưng chính nó CẮT THEO CẤU TRÚC: bom
6–9 cấp 0,000–0,007 s / 26 MiB, không lá `'x'` hay `"x"` (`scripts/do_chi_phi.py`, log `log/chi_phi_K2_312.log`; ứng viên 0,000 s /
25 MiB) ⇒ không phải lỗi, ghi §3. `GIET_CA_KHAC` 0, `TIN_DUNG_GIA` 0, 0 `.pyc` ở cả ba log.

### 1.6 Câu 2 — ca vòng 4 thêm/sửa có xanh giả, phụ thuộc thứ tự/nền, chậm bất thường không — **không** (đo được ở Linux)
- Bỏ qua lặng lẽ / vế rỗng: diff vòng 4 (`diff-l3-l4.patch`) không thêm `return` sớm, `BoQuaNen` hay nhánh "không thấy thì bỏ qua";
  mọi vế mới đi qua `chot`. Vế CLI của `t218` (D7/D8, D9) tự kiểm lời vá có hiệu lực: nó đòi đúng 2 dòng `… sai kiểu ` (fixture gốc
  có 1 `sai kiểu` + 1 `sai dạng`) và đúng 1 dòng mỗi tiền tố `CON_TRỎ_*\t<lease_id không hợp lệ: `, nên lời vá
  `_quet_lease_toan_kho` không ăn thì ca ĐỎ chứ không xanh; và §1.3 cho thấy cả bốn đường in (L1m, L1n, L1o, L1p) chết ở đúng vế
  CLI của chúng (chạm 2 · 2 · 1 · 1 lần). `_nap_cong()` dựng module MỚI mỗi lần gọi (`spec_from_file_location` + `exec_module`,
  :185–190), nên lời vá `mod._quet_lease_toan_kho` không rò sang ca khác, và được trả lại trong `finally`. Lớp `_LinhCanh` định
  nghĩa trong thân `t218`, bộ đếm đặt lại trước mỗi lần đo. Hạn lease của fixture D9 (`_yaml_that` → `lease_mau()` →
  `mai_sau()` = giờ thật + 4 h) không có mốc ngày cố định.
- Thứ tự: `scripts/db_dc.py` (log `log/dc_v4_31{1,2,3}.log`) — 9 ca (`t218`, hai ca A9 mới, đối chứng HEAD tượng trưng, hai ca
  `…/HEAD` thường, `t213`, `t215`, `t219`) chạy xuôi ×3 và NGƯỢC ×1, mỗi lượt một bản sao 6a7220a: **36/36 QUA** ở 3.11.15,
  3.12.3, 3.13.12; cộng toàn suite §1.4, nơi `t218` chạy thứ 216 và hai ca A9 mới thứ 224, 225 trên 263 (đếm dòng `<<< ra` của `ab_chinh/ung-3.12.out`).
- Nền: đo được 3 bản Python trên Linux; Windows/`nt` KHÔNG ĐO ĐƯỢC (lease cấm Windows CI). Ca mới chỉ dùng `git symbolic-ref`/
  `update-ref`/`checkout` và `_goi_main` trong tiến trình (`StringIO`, không qua CRLF); không nhánh theo `os.name`; không ca mới nào
  dùng `_chay_buoc_dang*` (`chay_buoc_` trên 0dd86c6 → 6a7220a: 30 → 30 dòng `grep -c`, 32 → 32 lần `grep -o`).
- Thời gian: §1.4 (ứng viên, A/B): `t218` 0,69–0,70 s, hai ca A9 mới 0,35–0,43 s — ngang 47 ca A9 (trung bình 0,31–0,34 s); lượt
  thứ tự trên (máy đang tải 2 suite + giàn) `t218` 0,90–1,24 s, ca A9 mới 0,33–0,67 s. Không bất thường.
- Một hệ quả đáng ghi (không phải lỗi): ca `t217_a9_sai_kieu_chi_qua_ref_tuong_trung_khong_phai_HEAD` ghim
  `sorted(refs) == [alias, main]`, nên đột biến NỚI miền L3g (thêm `refs/tags`) nay chết (lượt 3: sống 45/45). Điều này khớp SPEC A9
  ("Miền. `refs/heads/*` và `refs/remotes/*`") — ca ghim đúng miền đã đặc tả; ghi ở §3.

### 1.7 HINT lượt 4 — dựng, dry-run, áp thật, hai chiều, toàn suite (`scripts/dung_hint.py`, `scripts/db_hai_chieu.py`, `scripts/db_sau_hint.py`, `scripts/do_full_hint.sh`; log `log/hai_chieu2_31{1,2,3}.log`, `log/full_hint.log`, `log/ruff_hint2.log`, `log/a8_tinh_hint2.log`, `log/t70_t193_hint2.log`)
`dung_hint.py`: s0 = `git show 6a7220a:ops/lease_publish_test.py` → s1 (một nhóm), neo `@ca` + `def t217_a9_thieu_lease_id():`
đúng 1 lần; dấu chéo ngược dựng bằng `chr(92)` SAU khi phân tích cú pháp, rồi đo trên tệp đã ghi: dòng mới
`oid = _a9_commit(kho, {"ops/leases/y.yaml": "lease_id: on\n"})` (s1:12643) mang ĐÚNG MỘT dấu chéo, như 6 dòng cũ cùng mẫu.
**Bản nháp đầu** (sha256 `9227122b…9e9b`, mọi ca mới trỏ đích `refs/tags/t`) đã được THAY: đo trên nó, đột biến "dạy theo ca" K
(`if symref and not symref.startswith("refs/tags/"):`) sống 49/49 — vì mọi đích ngoài miền đều là tag. Bản cuối cho ca remote trỏ
`refs/pull/1/head`. Log của bản nháp giữ tên `log/hai_chieu_31{1,2,3}.log`, `log/full_hint_v1.log` (265/265 ở 3.11 và 3.12) và KHÔNG
dùng làm bằng chứng cho bản cuối.
```
# HINT sha256 adfaab4bc149c6a9fe8407f0f08f93638b72be81093d8f29807d101129dab0b3, 54 dòng, 1 nhóm, +43 −0, chỉ ops/lease_publish_test.py
# cây: git archive 6a7220a ops/lease_publish.py ops/lease_publish_test.py · cwd = gốc bản sao (w4.NtdOJ8/dryrun2.rqoi)
$ patch -p0 --fuzz=0 --dry-run < goi/HINT.patch
checking file ops/lease_publish_test.py
DRYRUN_RC=0
bam truoc=[d8079330007ab6ba a6765161065161b1 ] sau=[d8079330007ab6ba a6765161065161b1 ] KHONG_DOI orig_rej=0
$ patch -p0 --fuzz=0 < goi/HINT.patch          # áp THẬT trên bản sao khác (w4.NtdOJ8/apthat2.MOK2)
patching file ops/lease_publish_test.py
APPLY_RC=0 · TRUNG s1 TUNG BYTE · SAN PHAM KHONG DOI · orig_rej=0 · at_ca=265 · chay_buoc_ 30 dòng / 32 lần (gốc 30 / 32)
```
Nội dung: một hàm dựng kho `_a9_tuong_trung_ra_ngoai_mien(s, ten_sym, dich)` (lease `lease_id: on` CHỈ tới được qua ref `dich` ngoài
miền, `ten_sym` là ref tượng trưng trỏ tới nó) và hai ca: `t217_a9_sai_kieu_chi_qua_ref_tuong_trung_duoi_remotes_khong_phai_HEAD`
(`refs/remotes/upstream/alias` → `refs/pull/1/head`) và `t217_a9_sai_kieu_qua_ref_tuong_trung_leaf_gan_HEAD` (leaf `xHEAD`, `HEAD-x`,
`head` dưới `refs/heads/`, mỗi leaf một kho tạm và một chốt, đích `refs/tags/t`). Đếm `chay_buoc_` không đổi ⇒ không đổi `mong` của
`t70`, `SO_BO_QUA` hay literal `t193`. Ruff F cây đã vá so ứng viên: 11 = 11, thêm ∅ bớt ∅. A8 tĩnh cây đã vá (3.11, 3.12): 265 ca,
D 14, R 15, chỉ-lồng `{t70}`, G − D `{t202}`, (S) 29 → 31, 0 lần mới ĐỎ; `t70`, `t193` `1/1` ở 3.11, 3.12, 3.13.
Hai chiều (`db.py` với `HINT_TRUOC=goi/HINT.patch`: mỗi đột biến một bản sao `git archive 6a7220a ops .github` + `patch -p0 --fuzz=0`
HINT rồi neo; ca đích 49 `t217_*`): đối chứng bản đã vá **56/56 QUA** (49 `t217_*` + `t218 t213 t215 t214 t219 t204 t216`) ở 3.11,
3.12, 3.13. Đột biến (giống hệt ở ba bản; ca · `hàm:dòng` · leaf trong thông điệp):

| đột biến | kết quả trên bản đã vá |
|---|---|
| V1 bỏ mọi ref tượng trưng dưới `refs/remotes/` | GIET đúng 1 ca `…_duoi_remotes_khong_phai_HEAD` (`_a9_chot:12502` "được rc=0") |
| K bỏ ref tượng trưng trừ khi đích là tag (dạy theo ca) | GIET đúng ca remote ấy (đích `refs/pull/1/head`) |
| V2 `endswith("HEAD")` · V3 `"HEAD" in ten` | GIET đúng 1 ca `…_leaf_gan_HEAD`, leaf `refs/heads/xHEAD` |
| V3b `"/HEAD" in ten` · V3c leaf `.startswith("HEAD")` | GIET cùng ca ấy, leaf `refs/heads/HEAD-x` (chỉ leaf này bắt hai đột biến này) |
| V6 leaf `.upper() == "HEAD"` | GIET cùng ca ấy, leaf `refs/heads/head` |
| G4 (V1 ∪ V3 ∪ V6) | GIET hai ca mới |
| L3h (lượt 3) | GIET 3 ca: alias của vòng 4, remote mới, leaf mới |
| L3i · G2 · L3a · L3c · L3d · L3e (lượt 2–3) | GIET 1 · 4 · 5 · 2 · 5 · 2 ca (ca remote mới thêm vào số ca chết của G2, L3a, L3c, L3d) |
| L3g (nới: thêm `refs/tags`) | GIET 2 ca ghim miền (alias, leaf mới) — §3 |
| V9 · V10 · L (bỏ ref tượng trưng có ĐÍCH trong miền / đích là nhánh) | QUA 49/49 — chỉ đổi danh sách ref, không đổi kết luận cổng; KHÔNG nhắm (§3) |

`GIET_CA_KHAC` 0, `TIN_DUNG_GIA` 0, 0 `.pyc` ở mọi bản sao. Mỗi leaf của ca mới có ít nhất một đột biến CHỈ nó bắt (`xHEAD`←V2,
`HEAD-x`←V3b/V3c, `head`←V6), và ô `remotes` có V1, K chỉ ca remote bắt ⇒ bốn chốt phân biệt được bằng đầu vào, không phải bộ tương
đương.

Toàn suite trên bản đã vá (hai clone `--no-hardlinks` 6a7220a + `patch -p0 --fuzz=0`, DỰNG trong MỘT vòng lặp, 13:28:17Z–13:37:30Z):
```
DUNG hint 3.11 HEAD=6a7220a… numstat=[43 0 ops/lease_publish_test.py] PATCH_RC=0 · DUNG hint 3.12 … numstat=[43 0 …] PATCH_RC=0
KQ hint 3.11 rc=0 giay=485 tong_ket=[lease_publish: 265/265 đạt; đã chạy=265, bỏ qua=0] vao=265 ra=265 QUA=265 at_ca=265 pyc=0 porcelain=1 stderr_dong=44
KQ hint 3.12 rc=0 giay=549 tong_ket=[lease_publish: 265/265 đạt; đã chạy=265, bỏ qua=0] vao=265 ra=265 QUA=265 at_ca=265 pyc=0 porcelain=1 stderr_dong=72
```
stderr so ứng viên (A/B §1.4) sau khi chuẩn hoá đường dẫn/số dòng: `diff` rc=0 cả hai bản. Ca mới: remote 0,339 | 0,348 s, leaf (3 kho)
0,985 | 1,063 s (3.11 | 3.12); `t216` "giết thật=12, tín dụng giả=0, sống sót=0"; `t191` 85,0 | 109,8 s; `t125` 272,6 | 303,5 s.

### 1.8 Điểm dữ liệu cho mức P3: helper trên ảnh kho bình thường (log `log/a9_mirror.log`, `log/fsck_mirror.out`)
`git clone --mirror --no-hardlinks cay-kho` (bản sao cục bộ, KHÔNG phải mirror 480 ref của executor): 1 `refs/heads`, 17 `refs/remotes`,
42 tag, **0 ref tượng trưng** (`clone --mirror` chép `refs/remotes/origin/HEAD` thành ref THƯỜNG). `git fsck --full` 13:16:58Z–13:17:05Z
rc=0, output rỗng (0 byte). `--quet-a9` (3.12) của ứng viên: rc=0, 18 ref, 146 blob, 146 cặp, `kieu {str: 146}`, 0 lỗi; V1, V2, V3,
V6, G4, L3h cho JSON y hệt (băm map ref trùng); **L3i lệch**: 17 ref (bỏ `refs/remotes/origin/HEAD` THƯỜNG theo tên) — đúng kịch bản
mà ca vòng 4 khoá, và nó xuất hiện tự nhiên ở mirror. Tức các đường còn sống của lớp a9 không đổi kết quả trên ảnh kho bình thường.

### 1.9 A1–A10 trên 6a7220a — đo lại ở lượt này (không chép số lượt 1) (log `log/a8_tinh.log`, `log/t70_t193.log`, `log/db_a17_312.log`, `log/db_a9_312.log`; `t216` trong `ab_chinh/ung-3.1{1,2}.out`)
- **A8 tĩnh** (`scripts/tinh_a8.py`, viết mới; 3.11/3.12/3.13 cùng kết quả): nền 201 ca, D 13, R 14, chỉ-lồng `{t70}`, G 14, G − D
  `{t202}`, D − G ∅, sổ 12, D − sổ `{t199}`; ứng viên 263 ca, D 14 (+`t207`), R 15, **chỉ-lồng `{t70}`**, G 15, **G − D `{t202}` = nền**,
  D − G ∅, sổ 13, D − sổ `{t199}`; (S) 29 → 31, phần HƠN = 2 × `Name.id` `_chay_buoc_dang_that` trong thân `t207` ⇒ ĐƯỢC PHÉP, **0 lần
  mới ĐỎ**. `--chi-ca=t70_` và `--chi-ca=t193_`: `1/1` rc=0 ở 3.11, 3.12, 3.13. A8 động: ngoài phạm vi r17 (Q16). Delta suite và
  ruff: §1.4, §1.2.
- **A1–A7** (`scripts/db_a17.py`, neo gõ lại từ `luot1/scripts/db_ung.py` như dữ liệu; 3.12): R01, C01 GIET `t204` · R03 GIET `t205`,
  QUA `t178 t195 t196 t197` (đúng điều A2 dự liệu: `L` sống ở phép đếm mạng, chết ở ca trực tiếp) · C03 GIET `t205` · R04, C04 GIET
  `t206` · K01 (gỡ D1+D3) QUA `t207`, K02 (gỡ D1+D3+D6) GIET `t207` · R05 GIET `t208` · C05/C06/C07/C08 mỗi cái GIET đúng ca của nó,
  ca anh em QUA · C09 GIET `t213` · C10 GIET `t214` · C11 GIET `t215` · X02 GIET 5/5 · **N00 (thay cả sản phẩm bằng bản nền ab457c6)
  GIET 12/12** ca A1–A7 (đúng chữ "ĐỎ khi"). C02 (hàm chung `str()`): GIET 6, QUA `t209–t212` (hàm trả giá trị thô), `t213`
  `TypeError` — y như lượt 1, C02 không thuộc catalog `t216`. X03 (`_lease_id_quet` nuốt mọi ngoại lệ) QUA 5/5 — nay TƯƠNG ĐƯƠNG,
  vì sau vòng 2 `_lease_id_hop_le` chỉ ném `Chan` (`_repr_an_toan` không ném). `GIET_CA_KHAC` 0.
- **A9** (`scripts/db_a9.py`, neo gõ lại từ `luot1/scripts/db_a9.py`; 47 ca `t217_*`, 3.12): A01 bỏ băm blob · A02/A03 truthiness ·
  A04 nhận list cho `da_bi_thay_the` · A05 siết chuỗi trắng · A06 bỏ `--no-replace-objects` · A07 bỏ mọi `/HEAD` · A08 bỏ `.yml` · A09
  bỏ kiểm stderr · A10 đọc lại TÊN ref · A13 bỏ `leases_retired` · A14 nuốt lỗi parse · A15 regex trôi · A16 rc 2→1 · A17 nhận `int`:
  **mỗi cái GIET ≥ 1 ca bằng `TinHieuChotCa`**, `GIET_CA_KHAC` 0, `TIN_DUNG_GIA` 0; cộng L3a–L3i ở §1.3. Lượt quét kho thật + `git
  fsck --full`: KHÔNG ĐO ĐƯỢC ở lượt này (§5). Ngoại lệ đã biết: vế miền tượng trưng — lớp `a9-mien-refs-remotes-khong-co-ca` (§2).
- **A10**: `t216` in "catalog đột biến wp678: mẫu số=12, giết thật=12, tín dụng giả=0, sống sót=0" ở 3.11 và 3.12 (A/B §1.4); bộ độc
  lập ở trên cùng kết luận (phân hạng `TinHieuChotCa` + khung ca, không đếm mã thoát).

## 2. Hai lớp lượt 3 — trạng thái sau vòng 4

Tiêu chí đếm một đột biến sống vào lớp (giữ đúng tiêu chí lượt 3, nói thẳng để chủ kho bác được): (a) nó VIẾT LẠI điều kiện hay
lời gọi đang có trên đúng đường đang khoá theo một cách có lý do tự nhiên — rút gọn điều kiện, thành ngữ quen, đổi chỗ lời gọi —
chứ không CHÈN một nhánh riêng cho một kiểu, một giá trị hay một chuỗi mà mã không hề nhắc tới; và (b) có ít nhất một đầu vào TRONG
miền SPEC mà ở đó nó đổi kết luận của cổng (rc) so với ứng viên. Đột biến chỉ đổi DANH SÁCH ref mà không đổi kết luận, hay chỉ NỚI
(quét thừa), không tính.

| lớp lượt 3 (P lượt 3) | trạng thái sau vòng 4 | căn cứ đo |
|---|---|---|
| `a9-mien-refs-remotes-khong-co-ca` (P3) | **CÒN MỞ** — cùng cơ chế, qua đường mới; KHÔNG TÁI PHÁT (L3h, L3i chết đúng ca) | §1.3: L3h GIET đúng `…_qua_ref_tuong_trung_khong_phai_HEAD`, L3i đúng `…_o_origin_HEAD_khong_tuong_trung` ở 3.11/3.12/3.13. §1.5: **V1** `if symref and ten.startswith("refs/remotes/"):` (nửa `refs/remotes` của L3h — ô `remotes` / leaf khác / tượng trưng không có ca nào) và **V2** `endswith("HEAD")`, **V3** `"HEAD" in ten`, **V6** leaf `.upper()` (cách viết phép so leaf bằng thành ngữ chuỗi) sống 47/47 ca A9 ở ba bản và **toàn suite 263/263** (V1 riêng, và G4 = V1 ∪ V3 ∪ V6); báo SẠCH rc=0 trên S5 (`refs/remotes/upstream/alias` → tag), S6 (`refs/heads/xHEAD` → tag), S8 (`HEAD-x`), S7 (`head`) — mọi kịch bản trong miền SPEC A9 phải quét — trong khi helper ứng viên rc=1 ở cả bốn. |
| `khoa-t218-hep-cat-cau-truc-va-nhan` (P3) | **ĐÃ ĐÓNG** | §1.3: L1h, L1i (vế gọi thẳng `_repr_an_toan` :12276), L1k (`_nhan_lease_id_sai` :12276), L1l (`_lease_id_hien_thi` :12276), L1m, L1n (vế CLI D7/D8 :12306, chạm 2 lần), L1o, L1p (vế CLI D9 :12321, chạm 1 lần), G3/G3b/G3c — chết bằng `TinHieuChotCa` đúng vế ở ba bản. §1.5: tám chỗ định dạng `lease_id` thô của sản phẩm = đúng tám đường lính canh đi qua; dựng đầy đủ bằng cách KHÁC `repr()` (K1 `reprlib.repr` mặc định, K3/K4 `json.dumps`, K7 `str()`, K8 `!s:.120`) đều chết; K2 `pprint(depth=2)` sống nhưng chính nó cắt theo cấu trúc (0,007 s / 26 MiB bom 9 cấp) — không phải lỗi. |

Áp tiêu chí cho lớp a9: V1 — (a) viết lại vế leaf thành vế tiền tố, lý do tự nhiên "ref tượng trưng dưới `refs/remotes/` là con trỏ
HEAD của remote" (và là nửa còn lại của L3h mà lượt 3 đã tính); (b) S5 rc 1 → 0. V2, V3 — (a) thành ngữ quen (`endswith("HEAD")`, và
`"HEAD" in …` là bản Python của `grep -v HEAD`); (b) S6/S8 rc 1 → 0. V6 — (a) yếu nhất (refname Git phân biệt hoa/thường, gấp chữ
không có lý do), nhưng vẫn là viết lại phép so, không chèn gì; (b) S7 rc 1 → 0. K (`if symref and not symref.startswith("refs/tags/"):`)
chèn chuỗi `refs/tags/` mà mã không có ⇒ KHÔNG tính (§3), dù HINT vẫn giết nó. V9/V10/L chỉ đổi danh sách ref ⇒ KHÔNG tính (§3).

**Tỷ lệ vá thật 3→4.** Theo lớp: **1/2 = 50 %** (lớp t218 đóng; lớp a9 còn mở qua đường không ai chỉ). Theo đột biến lượt 3 nêu
đích danh: **14/14** chết bằng `TinHieuChotCa` đúng ca, đúng vế ở 3.11/3.12/3.13 (L3h L3i G2 · L1h L1i L1k L1l L1m L1n L1o L1p G3 G3b
G3c); cả 24 đột biến của bảng hai chiều lượt 3 (thêm L3a L3c L3d L3e · L1a L1b L1c L1e L1f L1g) cũng chết (L1c tương đương ở 3.13 như mọi
lượt). Theo đột biến lượt 2: L2a L2b L2b2 L2b3 L2b4 L2c L2d L2e L2f vẫn chết ở `t219`. **Không lớp nào TÁI PHÁT; không lỗi MỚI do vòng 4**
(§1.6); vòng 4 không đổi sản phẩm (§1.1). Lớp còn mở là **ca test hẹp hơn hợp đồng**, KHÔNG phải lỗi hành vi: helper quét đúng S5–S8
(rc=1). Hình dạng: lần thứ ba liên tiếp cho lớp này (1→2: L3c/L3e; 2→3: L3h/L3i; 3→4: V1/V2/V3/V6), mỗi bản vá ĐÚNG và CÓ RĂNG ở chỗ nó
phủ — đúng bài học "VÁ ĐÚNG CHỖ ĐƯỢC CHỈ RỒI BỎ SÓT ĐƯỜNG THỨ BA"; HINT lượt 3 (cùng model với reviewer này) phủ nửa `refs/heads` của
ô tượng trưng-leaf-khác mà bỏ nửa `refs/remotes`. HINT lượt này dựng từ bảng 8 ô (§1.5) cộng tập biên chuỗi của leaf, mỗi đường một chốt
riêng phân biệt bằng đầu vào (§1.7); sau HINT, mọi cách viết lại vị từ bỏ ref mà tôi liệt kê được hoặc chết, hoặc tương đương (V4 V5 V11 F1),
hoặc chỉ nới (V7 V8), hoặc chỉ đổi danh sách ref (V9 V10 L).

## 3. Đo được, KHÔNG xếp lớp (để chủ kho tự cân)
- **L3g (THÊM `refs/tags`, nới miền) nay CHẾT** ở ca alias của vòng 4 (và ở 2 ca của HINT): các ca ghim `sorted(refs) == […]`, tức ghim
  ĐÚNG miền SPEC A9 ("`refs/heads/*` và `refs/remotes/*`"). Khớp đặc tả, không phải lỗi; nếu chủ kho muốn cho phép nới miền, đổi phép
  so đó thành "chứa".
- **V9 / V10 / L** (bỏ ref tượng trưng có ĐÍCH trong miền / đích là nhánh — "khử trùng"): QUA mọi ca A9 trước và sau HINT; hậu quả đo
  được chỉ là tên ref tượng trưng vắng khỏi `refs` (S9: rc=1 vẫn đúng, `refs/remotes/upstream/alias` vắng). Cùng loại hậu quả S2 của lượt 3
  — không đổi kết luận cổng. Muốn khoá: một ca symref trỏ VÀO miền, đòi tên symref có trong `errors[0].refs`.
- **V7 / V8** (chỉ bỏ HEAD tượng trưng dưới `refs/remotes/` / khi đúng 3 dấu `/`): QUA — bỏ ÍT hơn SPEC cho phép, tức quét thừa ô
  `heads/…/HEAD` tượng trưng; an toàn. Không ca nào ghim ô "phải bỏ" ngoài đối chứng `origin/HEAD`.
- **V4 / V5 / V11 / F1**: tương đương (mọi refname đều có `/`; `%(symref)` khác rỗng luôn bắt đầu bằng `refs/`; mẫu có `/` cuối).
- **K** (dạy theo ca: bỏ ref tượng trưng trừ khi đích là tag): chèn chuỗi mà mã không có ⇒ không xếp lớp; sống 49/49 trên bản nháp HINT
  (mọi đích là tag), chết trên HINT bản cuối (đích `refs/pull/1/head` ở ca remote).
- **K2** `pprint.pformat(depth=2)` trong `_repr_an_toan`: cắt theo cấu trúc, rẻ ⇒ ngoài lớp t218. Nó cho đầu ra NHIỀU DÒNG (`\n`), nên
  một dòng `KHÔNG_XÁC_ĐỊNH`/`DU_BAO` mang giá trị lồng sẽ bị bẻ dòng; không ca nào khoá "một dòng" cho giá trị lồng sâu. Định dạng, không
  phải chi phí; cách viết không tự nhiên cho thông điệp một dòng.
- **X03** (`_lease_id_quet` nuốt mọi ngoại lệ) nay TƯƠNG ĐƯƠNG (sau vòng 2 `_lease_id_hop_le` chỉ ném `Chan`); **C02** `t213` ra
  `TypeError` như lượt 1 (ngoài catalog `t216`).
- Đột biến chèn nhánh của lượt 3 (L2g/L2h/L2i/L2k/L2n, L1j): sản phẩm và `t219` không đổi từ vòng 3, KHÔNG đo lại ở lượt này.
- Giàn của reviewer có một lỗi đã sửa: một lần gọi job nền thứ hai chạy sai thư mục (đường dẫn tương đối) nên không ra log; chạy lại
  bằng đường dẫn tuyệt đối (`log/db_a9_312.log`). Lỗi giàn, không phải của ứng viên.

## 4. Bảng lớp (lượt 4)

| slug | P | hành vi mã hay ca test | một câu |
|---|---|---|---|
| `a9-mien-refs-remotes-khong-co-ca` | P3 | **ca test** hẹp hơn hợp đồng (helper A9 đúng) | Vòng 4 giết đúng L3h/L3i, nhưng bỏ mọi ref tượng trưng dưới `refs/remotes/` (V1, nửa remote của L3h) hay so leaf bằng `endswith("HEAD")`/`"HEAD" in`/`.upper()` (V2/V3/V6) vẫn sống 47/47 ca A9 và toàn suite 263/263, và báo sạch rc=0 khi lease sai kiểu chỉ tới được qua `refs/remotes/upstream/alias`, `refs/heads/xHEAD`, `HEAD-x` hay `head` tượng trưng trỏ ra ngoài miền — các điểm trong miền SPEC A9 mà không ca nào dựng. |

Lớp `khoa-t218-hep-cat-cau-truc-va-nhan`: **ĐÃ ĐÓNG** (§2) — không còn trong bảng.

### Lớp `a9-mien-refs-remotes-khong-co-ca` (P3, CÒN MỞ)
- Biểu hiện: helper `ops/lease_publish_test.py:12389–12394` (`for-each-ref … "refs/heads", "refs/remotes"`; `if ten.rsplit("/", 1)[-1] ==
  "HEAD" and symref: continue`) — đúng; ca khoá `:12516–:12633`: ref tượng trưng duy nhất mà một ca đòi QUÉT là `refs/heads/alias` →
  `refs/tags/t` (:12614); không ca nào có ref tượng trưng dưới `refs/remotes/*` với leaf khác `HEAD`, và không ca nào có leaf "gần HEAD"
  (`xHEAD`, `HEAD-x`, `head`).
- Phép đo: §1.5 (V1/V2/V3/V6 QUA 47/47 ở 3.11/3.12/3.13; S5–S8 rc=0; V1 và G4 toàn suite 263/263 ở 3.12); §1.8 (trên ảnh kho bình
  thường các đường ấy không đổi kết quả).
- Vì sao P3 (không P2): cần ref tượng trưng TẠO TAY với tên đặc biệt, trỏ RA NGOÀI miền; clone thường chỉ có `<remote>/HEAD` tượng
  trưng, mirror không có ref tượng trưng nào (§1.8), nên ở lượt quét kho thật các đột biến này không đổi gì. Hỏng chỉ khi có thay đổi
  mã về sau, và khi ấy là âm giả của cổng TRƯỚC LAND trên đầu vào hiếm — như lượt 3 đã xếp.
- Hướng vá (HINT, một nhóm): hai ca, mỗi đường một chốt — `t217_a9_sai_kieu_chi_qua_ref_tuong_trung_duoi_remotes_khong_phai_HEAD`
  (`refs/remotes/upstream/alias` → `refs/pull/1/head`; giết V1, K, L3h) và `t217_a9_sai_kieu_qua_ref_tuong_trung_leaf_gan_HEAD` (leaf
  `xHEAD` · `HEAD-x` · `head`, mỗi leaf một kho tạm; giết V2/V3 · V3b/V3c · V6), cùng hàm dựng `_a9_tuong_trung_ra_ngoai_mien`.

## 5. KHÔNG ĐO ĐƯỢC
- Windows / nền `nt` thật, macOS (hệ tệp không phân biệt hoa/thường — leaf `refs/heads/head` của HINT chưa từng chạy ở đó); CI GitHub;
  máy chủ GitHub live; comment cấp quyền #678, comment quyết định #678 `6059219849` mà PROMPT dẫn, và danh tính người ký (#566).
- Lượt quét A9 trên mirror 480 ref của executor và `git fsck --full` của nó: mirror ấy không có trong `$R`; chỉ đo được trên mirror cục
  bộ 18 ref của `cay-kho` (§1.8), không thay được lượt quét trước LAND.
- Git khác 2.43.0 (CI dùng bản của `ubuntu-latest`) cho các ca ref tượng trưng mới; Python 3.14 (không có trong container).
- Toàn suite trên đột biến chỉ chạy ở 3.12 (đột biến ca đích chạy ở 3.11/3.12/3.13). Thời gian ở §1.6/§1.7 đo khi máy đang tải giàn.
- Model/effort thực sự phục vụ lượt review này (cấu hình tự khai Claude Opus 5.5 `claude-opus-5-5` effort max).
- Dọn để giữ `$R` < 2 GB (đo 1,8 GB lúc 13:2xZ): các clone `ab_chinh/{nen,ung}-3.1{1,2}`, `full_a9gop/*`, `full_hint/hint-3.1{1,2}`,
  `mirror.qSlq`, `cayhint.wju9`, `cay/l3` đã xoá bằng `shutil.rmtree` SAU khi đo; `.out`/`.err`/log giữ nguyên trong `w4.NtdOJ8`.

## 6. HINT (`goi/HINT.patch`, 54 dòng, sha256 `adfaab4bc149c6a9fe8407f0f08f93638b72be81093d8f29807d101129dab0b3`, 1 nhóm, chỉ sửa `ops/lease_publish_test.py`, đường dẫn repo-relative không tiền tố)
- Nhóm `# lop: a9-mien-refs-remotes-khong-co-ca` (`# hang: P3`), 1 hunk +43 −0, chèn trước `@ca def t217_a9_thieu_lease_id()`: hàm dựng
  `_a9_tuong_trung_ra_ngoai_mien(s, ten_sym, dich)` và hai ca ở §4. Không ca mới nào dùng `_chay_buoc_dang*` ⇒ không đổi `mong` của
  `t70`, `SO_BO_QUA`, literal `t193`; (S) 0 lần mới ĐỎ.
- Dry-run / áp thật / ruff / A8 tĩnh / hai chiều / toàn suite: §1.7 (`DRYRUN_RC=0` trên bản sao `git archive 6a7220a`, băm không đổi;
  `APPLY_RC=0`; đối chứng 56/56 và mọi đột biến V1 V2 V3 V3b V3c V6 G4 K L3h chết đúng ca ở 3.11/3.12/3.13; toàn suite **265/265** ở 3.11
  và 3.12).
- Phạm vi: chỉ lớp a9. Lớp t218 đã đóng nên không có nhóm. Quan sát §3 (V9/V10/L, L3g, K2) cố ý KHÔNG vào HINT.

## 7. Kết luận
`changes_requested` — **0 P1 · 0 P2 · 1 P3**: `a9-mien-refs-remotes-khong-co-ca` (P3, CÒN MỞ — đường mới cùng cơ chế: V1 nửa
`refs/remotes` của L3h, V2/V3/V6 cách viết phép so leaf). `khoa-t218-hep-cat-cau-truc-va-nhan` **ĐÃ ĐÓNG**. Tỷ lệ vá thật 3→4 theo lớp
**1/2 = 50 %**; đột biến lượt 3 nêu đích danh **14/14** chết đúng ca, đúng vế; không lớp nào TÁI PHÁT; không lỗi MỚI do vòng 4.

Kiểm lời khai của phiên điều phối: suite 263/263 ở 3.11 và 3.12 trên 6a7220a — **có** (§1.4); nền 201/201 — **có** (§1.4); ruff F
delta ∅ — **có** (§1.2); vòng 4 = áp NGUYÊN VĂN `luot3/HINT.patch`, chỉ tệp test — **có** (§1.1).

A1–A10 trên head này (đo lại, §1.9): A1–A7 **có** (mọi đột biến đích chết đúng ca; sản phẩm nền làm 12/12 ca ĐỎ); A8 phần tĩnh **có**
(delta suite 0, ruff ∅, `t70`/`t193` 1/1 ở 3.11/3.12/3.13, chỉ-lồng `{t70}`, G − D = nền, (S) 0 ĐỎ); A9 nghĩa vụ helper **có** cho
A01–A17 và L3a–L3i, **không** cho vế miền ref tượng trưng (lớp còn mở); lượt quét kho thật + fsck `KHÔNG ĐO ĐƯỢC` ở đây; A10 **có**
(`t216` 12/12, bộ độc lập 0 `GIET_CA_KHAC`).

Lớp còn mở là ca test hẹp hơn hợp đồng, không phải lỗi hành vi (helper đúng ở S5–S8), và ở ảnh kho bình thường nó không đổi kết quả
(§1.8). Theo quyết định chủ kho (lượt 4 là lượt vượt giới hạn DUY NHẤT; còn lớp mở ⇒ chủ kho quyết), đây là một ứng viên "chấp nhận kèm
nợ" hoặc áp `goi/HINT.patch` (1 nhóm, chỉ tệp test, dry-run `patch -p0 --fuzz=0` rc=0, toàn suite 265/265 ở 3.11 và 3.12). Mức
assurance của lượt này: `review_deferred` (subagent cùng họ executor, cùng model đã viết HINT lượt 1, 2, 3 mà vòng 2, 3, 4 áp nguyên văn);
land vẫn đòi `human_audited` của chủ kho.
