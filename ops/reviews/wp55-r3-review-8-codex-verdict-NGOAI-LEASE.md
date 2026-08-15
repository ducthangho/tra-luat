# Cross-review wp55 revision 3 / generation 6 — changes_requested

**Verdict:** `changes_requested`  
**Reviewed SHA:** `91780cb0df3c898b2ca92bc17d14107547d944c6`  
**Base SHA:** `fbe5ab9e1ece3b45c065879bfd59dee2554db3e2`  
**Spec SHA-256:** `e321f811724fae97b19d523a3e5159bc13b425cd15fc6c753c7439fe28cae22d`

Generation 6 bỏ được `PHU_NHIEU_LOP`, suite nền đạt `149/149`, và lời khai mới về
NBSP là đúng: đột biến chỉ bỏ NFKC + `_PHAN_CACH` vẫn không giết ca vì
`str.split()` còn gộp U+00A0. Tuy nhiên hai finding lượt 7 chưa được đóng ở mức tiêu
chí: miễn trừ ngắt dòng vẫn tha nhiều nội dung không phải văn xuôi kể lại kết quả đo,
còn hai mutant phối hợp mới giết lan sang các lớp doctrine không được khai là ca đích.

Ngoài ra, phần adapter được thêm ở generation 6 có một P1 độc lập: lệnh được giới thiệu
là kiểm sự tồn tại của biến bí mật mà không in nội dung lại in nguyên giá trị biến ra
stdout.

## Findings

### 1. [P1] `work-packet-secret-check-prints-secret`

**Severity:** `P1`  
**Disposition:** `code_fix_required`

`.claude/skills/work-packet/SKILL.md:63-68` nói “không bao giờ in nội dung”, nhưng
`${TEN_BIEN:-chưa đặt}` trả chính giá trị biến khi biến đã được đặt. Hai expansion bị
nối với nhau, nên stdout gồm cả độ dài lẫn secret. Đây là lệnh hướng dẫn agent chạy với
refresh token thật; một lần làm theo sẽ đưa token vào transcript/log.

Tái lập trên SHA bất biến, chỉ dùng giá trị giả:

```bash
test "$(git rev-parse HEAD)" = 91780cb0df3c898b2ca92bc17d14107547d944c6
git show 91780cb0df3c898b2ca92bc17d14107547d944c6:.claude/skills/work-packet/SKILL.md \
  | sed -n '63,68p'
env TEN_BIEN=review8_fake_secret bash -c \
  'echo "${TEN_BIEN:+có, ${#TEN_BIEN} ký tự}${TEN_BIEN:-chưa đặt}"'
echo "secret_probe_rc=$?"
```

Đầu ra thực tế:

```text
echo "${TEN_BIEN:+có, ${#TEN_BIEN} ký tự}${TEN_BIEN:-chưa đặt}"
có, 19 ký tựreview8_fake_secret
secret_probe_rc=0
```

### 2. [P1] `doctrine-line-break-exemption-bypasses-non-prose`

**Severity:** `P1`  
**Disposition:** `code_fix_required`

Đây là **cùng finding ID của lượt 7**, không phải lỗi mới được đổi tên. Hai chốt mới chỉ
bắt fence đứng đầu dòng và chỉ hỏi có ký tự chữ/số ở hai phía. AC19 miễn “văn xuôi kể
lại kết quả đo”, không miễn một chữ vô nghĩa, hai con số, bảng HTML, hay code block.

Các đường lách còn chạy được:

- `x người có\nthẩm quyền y` và `1 người có\nthẩm quyền 2` trả `rc=0`; chúng không
  phải văn xuôi kể lại phép đo. Punctuation hai phía không lọt (`rc=6`), xác nhận điều
  quyết định chỉ là `_CO_CHU`, không phải nghĩa/ngữ cảnh.
- Fence hợp lệ trong bullet và blockquote không được `_dong_khoi_ma()` nhận ra vì regex
  chạy trên dòng thô trước khi `_go_dau_dong()` gỡ `-`/`>`.
- Fence mở bằng 4 backtick bị fence 3 backtick đóng nhầm. Theo CommonMark, closing fence
  phải có ít nhất độ dài của opening fence; nội dung sau fence 3 vẫn là code nhưng scanner
  coi là ngoài code và tha.
- Indented code block 4 dấu cách và một ô bảng HTML có chữ hai phía cũng trả `rc=0`.

Lệnh tái lập độc lập, neo exact SHA:

```bash
git show 91780cb0df3c898b2ca92bc17d14107547d944c6:.claude/dev/packet_loop.py \
  > /tmp/review8-packet-loop.py
python3 - <<'PY'
import subprocess, tempfile
from pathlib import Path

script = Path('/tmp/review8-packet-loop.py')
cases = {
    'nonsense_words': 'x người có\nthẩm quyền y\n',
    'numeric_wrappers': '1 người có\nthẩm quyền 2\n',
    'punctuation_control': '. người có\nthẩm quyền !\n',
    'fence_in_bullet': '- ```\n  x người có\n  thẩm quyền y\n  ```\n',
    'fence_in_quote': '> ```\n> x người có\n> thẩm quyền y\n> ```\n',
    'fence4_short_fake_close':
        '````\ncode\n```\nx người có\nthẩm quyền y\n````\n',
    'indented_code': '    x người có\n    thẩm quyền y\n',
    'html_table_wrapped':
        '<table><tr><td>Ghi chú người có\nthẩm quyền đây.</td></tr></table>\n',
    'plain_fence_control': '```\nx người có\nthẩm quyền y\n```\n',
}
with tempfile.TemporaryDirectory(prefix='review8-doctrine-') as td:
    p = Path(td) / '.claude/skills/x/SKILL.md'
    p.parent.mkdir(parents=True)
    for name, body in cases.items():
        p.write_text(body, encoding='utf-8')
        r = subprocess.run(
            ['python3', str(script), 'doctrine-scan', '--root', td],
            capture_output=True, text=True,
        )
        print(f'{name}_rc={r.returncode}')
PY
```

Đầu ra thực tế:

```text
nonsense_words_rc=0
numeric_wrappers_rc=0
punctuation_control_rc=6
fence_in_bullet_rc=0
fence_in_quote_rc=0
fence4_short_fake_close_rc=0
indented_code_rc=0
html_table_wrapped_rc=0
plain_fence_control_rc=6
```

Hai ca fence không đóng và đóng bằng loại khác đều trả `rc=6`; vì vậy máy trạng thái
không hỏng toàn bộ. Lỗi cụ thể là nó không mang độ dài opening fence, không hiểu container
Markdown, không nhận indented code, rồi chốt “chữ hai phía” biến các ngữ cảnh bị bỏ sót
thành văn xuôi được tha. Giới hạn executor khai cho câu văn xuôi thật không bao trùm các
phản chứng cấu trúc này; còn `x/y` và `1/2` cho thấy chính tiêu chí “văn xuôi” cũng chưa
được cưỡng chế.

### 3. [P2] `doctrine-line-marker-stripping-creates-false-positives`

**Severity:** `P2`  
**Disposition:** `code_and_test_fix_required`

`_RE_DAU_DONG` kết thúc bằng `\s*`, nên nó coi `#người` là ATX heading và `1.người`
là ordered-list marker dù cả hai thiếu khoảng trắng bắt buộc. `_khuc_chuan()` gỡ các ký
tự không phải marker Markdown này ở **mọi** dòng rồi nối hai dòng, tạo ra cụm cấm vốn
không tồn tại trong nội dung hiển thị. Đây là chiều bắt-oan của chính lớp chuẩn hóa mới,
nhưng ma trận AC19 không có ca tương ứng.

Tái lập trên cùng script exact-SHA ở finding 2:

```bash
python3 - <<'PY'
import subprocess, tempfile
from pathlib import Path

script = Path('/tmp/review8-packet-loop.py')
cases = {
    'hash_tags': '#người có\n#thẩm quyền\n',
    'number_tokens': '1.người có\n2.thẩm quyền\n',
    'table_rows_control': '| người có |\n| thẩm quyền |\n',
}
with tempfile.TemporaryDirectory(prefix='review8-marker-') as td:
    p = Path(td) / '.claude/skills/x/SKILL.md'
    p.parent.mkdir(parents=True)
    for name, body in cases.items():
        p.write_text(body, encoding='utf-8')
        r = subprocess.run(
            ['python3', str(script), 'doctrine-scan', '--root', td],
            capture_output=True, text=True,
        )
        first = (r.stderr or r.stdout).splitlines()[0]
        print(f'{name}_rc={r.returncode}; {first}')
PY
```

Đầu ra thực tế:

```text
hash_tags_rc=6; .../SKILL.md:1: [bang-vai-tro-muc-2] chép doctrine: 'người có thẩm quyền'
number_tokens_rc=6; .../SKILL.md:1: [bang-vai-tro-muc-2] chép doctrine: 'người có thẩm quyền'
table_rows_control_rc=0; doctrine-scan: sạch — đã quét 1 tệp, 0 chỗ chép doctrine
```

### 4. [P2] `ac18-coordinated-mutants-kill-unrelated-classes`

**Severity:** `P2`  
**Disposition:** `test_fix_required`

Việc bỏ ngoại lệ và tái dựng NBSP ba đường là đúng. Khoảng trống còn lại nằm ở lời
khẳng định “đột biến giết đúng ca đó”. Suite chỉ chạy ca đích cùng ba đối chứng **máy
trạng thái** cho mọi mutant doctrine. Do đó một mutant làm hỏng nhiều lớp doctrine khác
vẫn được báo “giết 1 ca đích”.

Hai mutant phối hợp một-ca-đích đều giết lan:

- `ha_NFKC_va_bo_moi_duong_gop_nbsp` khai 1 target, nhưng còn giết
  `ac18_nfkc_hai_cham_toan_rong` và `ac18_phan_cach_en_dash`.
- `ha_NFKC_va_bo_casefold` khai 1 target, nhưng còn giết
  `ac18_nfkc_hai_cham_toan_rong` và `ac18_cf_zwnj`.

Lệnh dưới dùng chính `_cap_thay_the()` và `chay_suite()` của exact HEAD; `FAIL` nghĩa là
mutant đã giết ca:

```bash
test "$(git rev-parse HEAD)" = 91780cb0df3c898b2ca92bc17d14107547d944c6
python3 - <<'PY'
import importlib.util, tempfile
from pathlib import Path

root = Path.cwd()
spec = importlib.util.spec_from_file_location(
    'r8tests', root / '.claude/dev/packet_loop_test.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
base = (root / '.claude/dev/packet_loop.py').read_text(encoding='utf-8')
checks = {
  'ha_NFKC_va_bo_moi_duong_gop_nbsp': [
    'ac18_nbsp_phu_ba_lop', 'ac18_nfkc_hai_cham_toan_rong',
    'ac18_phan_cach_en_dash', 'ac18_cf_zwnj'],
  'ha_NFKC_va_bo_casefold': [
    'ac18_nfkc_ligature_ff', 'ac18_nfkc_hai_cham_toan_rong', 'ac18_cf_zwnj'],
}
with tempfile.TemporaryDirectory(prefix='review8-mutant-') as td:
    td = Path(td)
    for name, selected in checks.items():
        tim, thay, declared = m.MUTANTS[name]
        text = base
        for old, new in m._cap_thay_the(tim, thay):
            text = text.replace(old, new, 1)
        script = td / f'{name}.py'
        script.write_text(text, encoding='utf-8')
        got = m.chay_suite(script, td / name, chi_chay=set(selected))
        print(f'{name}: declared_targets={len(declared)}')
        for case in selected:
            print(' ', case, 'PASS' if got.get(case) is None else 'FAIL')
PY
```

Đầu ra thực tế:

```text
ha_NFKC_va_bo_moi_duong_gop_nbsp: declared_targets=1
  ac18_nbsp_phu_ba_lop FAIL
  ac18_nfkc_hai_cham_toan_rong FAIL
  ac18_phan_cach_en_dash FAIL
  ac18_cf_zwnj PASS
ha_NFKC_va_bo_casefold: declared_targets=1
  ac18_nfkc_ligature_ff FAIL
  ac18_nfkc_hai_cham_toan_rong FAIL
  ac18_cf_zwnj FAIL
```

Ba đối chứng khác họ chỉ chứng minh mutant doctrine không phá máy trạng thái; chúng không
chứng minh mutant nhắm đúng **lớp doctrine** mà AC18 yêu cầu. Mutant
`noi_mien_tru_nhu_generation_4` khai thẳng 13 target và các đối chứng thử thêm cho thấy
NFKC/AC19 không chết, nên không có finding riêng cho mutant đó.

## Gate, phạm vi và ranh giới

- Bước 0 đạt: HEAD đúng SHA; `git rev-parse --is-shallow-repository` trả `false`.
- Đã đọc trọn 344 dòng spec; SHA-256 khớp. Diff base..head đúng 6 tệp trong write-set;
  `git diff --check` trả `rc=0`.
- `python3 .claude/dev/packet_loop_test.py`: `rc=0`; nền `149/149`; AC19 `53/53`
  với 23 ca riêng; 35 mutant; AC18 báo 3 mutant phối hợp, 0 ngoại lệ.
- `doctrine-scan --root .`: `rc=0`; quét 4 tệp, 0 vi phạm.
- `doc-claims-check --strict --json`: `rc=0`; `files_scanned=82`, `flags=[]`.
- `release-verify` trên archive sạch của reviewed SHA: `rc=0`; checked=179;
  `failed=[]`, `extra_files=[]`, `errors=[]`.
- `golden-test`: `rc=0`; `case_count=20`.
- `eol_policy.py --all --json`: `rc=0`; `scanned=304`, `violations=[]`.
- `release-bundle` chạy hai lần trên archive sạch: cả hai `rc=0`, `file_count=179`,
  cùng SHA-256 `20c89545566b7682b3ecd2ac2ac0283add5af8a4d6ca377d9acbcde4487f8590`.
- AC20 tại master bất biến `2531366e1abc6cbca0a6c2765e40e54be38d1fb7`: archive + apply
  thành công; doctrine scan `rc=0`; packet suite với `GIT_DIR` nguồn `rc=0`, nền
  `149/149`, tổng `ĐẠT`.
- Tự dựng đột biến NBSP **hai** vế (NFKC→NFC + bỏ `_PHAN_CACH`) giữ ca
  `ac18_nbsp_phu_ba_lop` xanh, tức scanner vẫn trả `rc=6`; lời khai về đường thứ ba
  `str.split()` là đúng.
- Không xác nhận độc lập được khai báo `tl.py --selftest 1696/1696`. Working tree trả
  `rc=1`, `1694/1696`; một archive exact-head với object store nguồn cũng trả `rc=1`,
  `1694/1696`, cùng hai ca L2 `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` và
  `r268_l2_trichotomy_theo_trang_thai_object`. Đây là ranh giới object/git-context đã
  xuất hiện ở lượt 7 và các tệp liên quan không thuộc diff, nên không tính thành finding
  của packet.
- Không commit, push, merge, land, deploy hoặc sửa tệp packet.

## Evidence §7

```yaml
schema_version: 1
packet_id: wp55
revision: 3
generation: 6
provider: codex
role: reviewer
independent: true
executor_provider: claude
verdict: changes_requested
reviewed_sha: 91780cb0df3c898b2ca92bc17d14107547d944c6
base_sha: fbe5ab9e1ece3b45c065879bfd59dee2554db3e2
spec_sha256: e321f811724fae97b19d523a3e5159bc13b425cd15fc6c753c7439fe28cae22d
master_sha_tested: 2531366e1abc6cbca0a6c2765e40e54be38d1fb7
changed_paths_count: 6
protected_paths_changed: 0
tests:
  - name: packet_loop_test reviewed tree
    status: passed
    evidence: "rc=0; baseline=149/149; classes=53/53; mutants=35; coordinated=3; exceptions=0"
  - name: doctrine scan reviewed tree
    status: passed
    evidence: "rc=0; scanned=4; violations=0"
  - name: adapter secret probe
    status: failed
    evidence: "rc=0; stdout contains exact fake secret review8_fake_secret"
  - name: non-prose and structured line-break probes
    status: failed
    evidence: "nonsense=0; numeric=0; bullet_fence=0; quote_fence=0; fence4_short_close=0; indented_code=0; html_table=0; plain_fence_control=6"
  - name: line-marker false-positive probes
    status: failed
    evidence: "hash_tags=6; number_tokens=6; table_rows_control=0"
  - name: coordinated mutant selectivity
    status: failed
    evidence: "NBSP mutant kills target plus NFKC and separator classes; ligature mutant kills target plus NFKC and Cf classes"
  - name: NBSP two-path reconstruction
    status: passed
    evidence: "removing NFKC and PHAN_CACH alone leaves ac18_nbsp_phu_ba_lop passing; Unicode split is the third path"
  - name: merged-tree doctrine scan and packet suite
    status: passed
    evidence: "master=2531366e1abc6cbca0a6c2765e40e54be38d1fb7; rc=0/0; baseline=149/149; total=passed"
  - name: tl selftest working tree
    status: not_confirmed
    evidence: "rc=1; 1694/1696; failures=r226 L2 threshold,r268 L2 trichotomy"
  - name: tl selftest exact-head archive with source object store
    status: not_confirmed
    evidence: "rc=1; 1694/1696; same two git/object-context failures"
  - name: doc claims strict
    status: passed
    evidence: "rc=0; files_scanned=82; flags=[]"
  - name: release verify strict clean archive
    status: passed
    evidence: "rc=0; checked=179; failed=[]; extra_files=[]; errors=[]"
  - name: golden test
    status: passed
    evidence: "rc=0; case_count=20"
  - name: eol policy
    status: passed
    evidence: "rc=0; scanned=304; violations=[]"
  - name: release bundle x2 clean archive
    status: passed
    evidence: "rc=0/0; file_count=179; sha256=20c89545566b7682b3ecd2ac2ac0283add5af8a4d6ca377d9acbcde4487f8590 both runs"
findings:
  - finding_id: work-packet-secret-check-prints-secret
    severity: P1
    disposition: code_fix_required
  - finding_id: doctrine-line-break-exemption-bypasses-non-prose
    severity: P1
    disposition: code_fix_required
  - finding_id: doctrine-line-marker-stripping-creates-false-positives
    severity: P2
    disposition: code_and_test_fix_required
  - finding_id: ac18-coordinated-mutants-kill-unrelated-classes
    severity: P2
    disposition: test_fix_required
```
