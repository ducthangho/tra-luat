# Cross-review wp55 revision 3 / generation 5 — changes_requested

**Verdict:** `changes_requested`  
**Reviewed SHA:** `2cccf1ea61859f1b051adb646294ead285dac39c`  
**Base SHA:** `fbe5ab9e1ece3b45c065879bfd59dee2554db3e2`  
**Spec SHA-256:** `e321f811724fae97b19d523a3e5159bc13b425cd15fc6c753c7439fe28cae22d`

Generation 5 đóng được bảy finding của lượt 6 về state machine, HTML quoted attribute,
ma trận AC14/18/19. Việc đổi ca văn xuôi một dòng từ BẮT-OAN sang LỌT là cách đọc đúng:
AC2 đòi một cụm cấm nằm trọn trên một dòng phải đỏ, còn AC19 chỉ miễn câu kể lại kết quả đo
bị ngắt dòng. Tuy nhiên chính miễn trừ ngắt dòng mới đang rộng hơn AC19: nó tha mọi cấu trúc
ngắt dòng, kể cả heading, bullet, code fence và ô bảng HTML. Ngoài ra suite tự cho phép hai
lớp AC18 không có đột biến, trái câu chữ bắt buộc của spec.

## Findings

### 1. [P1] `doctrine-line-break-exemption-bypasses-non-prose`

**Disposition:** `code_fix_required`

`_duoc_tha_vi_ngat_dong()` chỉ hỏi cụm có nằm trọn trong một dòng vật lý hay không. Nếu
không, hàm trả `True` cho mọi ngữ cảnh không phải bảng Markdown có dấu `|`. Điều này rộng
hơn AC19, vốn chỉ tha *văn xuôi kể lại kết quả đo*. Nó tạo đường lách AC2 bằng chính các
cấu trúc doctrine thường dùng.

Tái lập trên đúng SHA review (mỗi lần nội dung dưới đây là toàn bộ
`/tmp/review7probe/.claude/skills/x/SKILL.md`):

```bash
python3 .claude/dev/packet_loop.py doctrine-scan --root /tmp/review7probe
```

Các probe độc lập đều trả `rc=0` và cùng stdout:

~~~~text
doctrine-scan: sạch — đã quét 1 tệp, 0 chỗ chép doctrine
~~~~

Nội dung và rc cụ thể:

~~~~text
## Chỉ người có
## thẩm quyền
heading_rc=0

- Người có
  thẩm quyền
bullet_rc=0

<table><tr><td>Người có
thẩm quyền</td></tr></table>
html_table_rc=0

```
Người có
thẩm quyền
```
code_fence_rc=0
~~~~

Trong cả bốn ca, chuỗi phẳng chứa nguyên cụm cấm `người có thẩm quyền`; ba ca đầu còn là
heading/list/table hiển thị, không phải câu văn xuôi kể lại kết quả đo. Suite hiện chỉ có
`oan_term_ngat_dong` và `oan_claude_md_master`, nên không bắt được việc miễn trừ bị dùng
ngoài loại ngữ cảnh AC19 cho phép.

### 2. [P2] `ac18-overlap-exceptions-have-no-killing-mutant`

**Disposition:** `test_fix_required`

AC18 nói rõ: *mỗi lớp* phải có một phản chứng và một đột biến giết đúng ca đó. Suite hiện
tự tạo ngoại lệ `PHU_NHIEU_LOP` cho `ac18_nbsp_phu_hai_lop` và
`ac18_nfkc_ligature_ff`, rồi coi lớp có mặt trong ngoại lệ là đạt dù không mutant nào giết
ca. Đây không phải cách nghiệm thu được spec cho phép.

Lệnh tái lập:

```bash
GIT_DIR="$PWD/.git" python3 -B /tmp/review7-merged-2cccf1e/.claude/dev/packet_loop_test.py
```

Kết quả `rc=0`, nhưng stdout tự xác nhận khoảng trống:

```text
nền: 133/133 đạt
AC 19 — ánh xạ lớp lách → ca bắt-oan:
  ok  41/41 lớp lách đều có ca bắt-oan (19 ca riêng biệt)
AC 18 — mỗi LỚP LÁCH phải có đột biến của nó:
  ok  41 lớp lách: 39 có đột biến riêng · 2 khai PHỦ CHỒNG kèm lý do
TỔNG: ĐẠT
```

Lý do phủ chồng giải thích vì sao các mutant hiện tại không giết được ca, nhưng không thay
thế yêu cầu phải có mutant. Có thể thiết kế mutant phối hợp chỉ bỏ đúng hai đường phủ của
từng lớp. Thay “không có mutant” bằng ngoại lệ làm yếu tiêu chí so với AC18.

Việc chỉ áp chốt orphan-mutant cho `LOP_LACH` là hợp lý: câu chữ AC18 nói “mỗi lớp trong
danh sách”, không nói mọi ca chiều-tha của toàn suite phải có mutant gỡ chốt. Vấn đề là hai
lớp nằm ngay trong `LOP_LACH` vẫn đang được miễn.

## Gate và phạm vi

- Bước 0: HEAD đúng; repository không shallow; `core.abbrev` đọc lại là `7`. Lệnh ghi
  `git config core.abbrev 7` báo read-only vì `.git/config` ngoài vùng ghi, không làm lệch
  giá trị thực tế.
- Spec đã đọc trọn 344 dòng; SHA-256 khớp. Diff đúng 6 tệp thuộc write-set.
- `packet_loop_test.py`: `rc=0`, nền `133/133`, 30 mutant được báo giết ca đích.
- `doctrine-scan --root .`: `rc=0`, quét 4 tệp, 0 vi phạm.
- `doc-claims-check --strict --json`: `rc=0`, `files_scanned=82`, `flags=[]`.
- `golden-test`: `rc=0`, `case_count=20`.
- `eol_policy.py --all --json`: `rc=0`, `scanned=304`, `violations=[]`.
- `release-verify` trong working tree: `rc=2`, duy nhất vì tệp nhiệm vụ ngoài manifest
  `NHIEM_VU_REVIEW_7.md`. Chạy lại trên archive sạch của đúng reviewed SHA: `rc=0`,
  `checked_file_count=179`, `failed=[]`, `extra_files=[]`, `errors=[]`.
- AC20 tại master bất biến `2531366e1abc6cbca0a6c2765e40e54be38d1fb7`: archive + apply
  thành công; doctrine scan `rc=0`; packet suite với object store nguồn `rc=0`, `133/133`.
- Không chạy được `tl.py --selftest` đến kết quả đáng tin: working tree trả `1694/1696`
  do tệp nhiệm vụ làm thay đổi trạng thái object; archive với `GIT_DIR` trả `1689/1696`
  do ngữ cảnh git chưa tự chứa; lần thêm `GIT_WORK_TREE` dừng bằng
  `pyo3_runtime.PanicException: Python API call failed` trong `cryptography`. Vì vậy không
  xác nhận độc lập được khai báo `1696/1696`.
- Không chạy lại `release-bundle` ×3; đây là ranh giới chưa đo của lượt này.

## Evidence §7

```yaml
schema_version: 1
packet_id: wp55
revision: 3
generation: 5
provider: codex
role: reviewer
independent: true
executor_provider: claude
verdict: changes_requested
reviewed_sha: 2cccf1ea61859f1b051adb646294ead285dac39c
base_sha: fbe5ab9e1ece3b45c065879bfd59dee2554db3e2
spec_sha256: e321f811724fae97b19d523a3e5159bc13b425cd15fc6c753c7439fe28cae22d
master_sha_tested: 2531366e1abc6cbca0a6c2765e40e54be38d1fb7
changed_paths_count: 6
protected_paths_changed: 0
tests:
  - name: packet_loop_test reviewed tree
    status: passed
    evidence: "rc=0; baseline 133/133; 30 declared mutants passed"
  - name: doctrine scan reviewed tree
    status: passed
    evidence: "rc=0; scanned=4; violations=0"
  - name: doctrine non-prose split probes
    status: failed
    evidence: "heading_rc=0; bullet_rc=0; html_table_rc=0; code_fence_rc=0"
  - name: merged-tree doctrine scan and packet suite
    status: passed
    evidence: "master=2531366e1abc6cbca0a6c2765e40e54be38d1fb7; rc=0/0; baseline 133/133"
  - name: tl selftest
    status: not_confirmed
    evidence: "working tree 1694/1696 from task-file contamination; clean attempt hit cryptography pyo3 panic"
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
  - name: release bundle x3
    status: not_run
    evidence: "not run in review 7"
findings:
  - finding_id: doctrine-line-break-exemption-bypasses-non-prose
    severity: P1
    disposition: code_fix_required
  - finding_id: ac18-overlap-exceptions-have-no-killing-mutant
    severity: P2
    disposition: test_fix_required
```

Không sửa tệp packet, không commit, push, merge, land hoặc deploy trong lượt review này.
