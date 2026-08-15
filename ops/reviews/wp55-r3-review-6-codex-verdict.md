# Cross-review wp55 revision 3 / generation 4 — changes_requested

**Verdict:** `changes_requested`  
**Review anchor:** `e6e4b73dc940fcd04e9030e353e0e5fe7f3f0af8`  
**Base:** `fbe5ab9e1ece3b45c065879bfd59dee2554db3e2`  
**Spec SHA-256:** `e321f811724fae97b19d523a3e5159bc13b425cd15fc6c753c7439fe28cae22d`  
**Reviewer / executor:** `codex` / `claude` — independent, cross-provider  
**Lease:** `wp55-r3-review-6-codex-20260814`, valid through `2026-08-15T20:00:00Z`

Các gate phát hành, phạm vi 6 tệp, doctrine scan trên cây sạch, full self-test và bundle determinism đều xanh. Tuy vậy, public CLI vẫn cho phép bỏ qua review accounting, một lượt quota có thể kết thúc bằng approval ở attempt 0, và doctrine scan còn hai false negative. Bộ test cũng chưa chứng minh đủ AC14/18/19. Vì vậy chưa thể approve.

## Hai trục review

| Trục | Kết quả |
|---|---|
| Standards / safety | `changes_requested` | Hai invariant của state machine bị phá qua chính public entrypoint; không thấy secret, destructive action hay scope drift trong 6 tệp. |
| Spec | `changes_requested` | Không đạt AC2, AC3/4/8, AC14, AC18 và AC19; AC20 còn thiếu điều kiện để công thức đo tự chạy được. |

## Findings

### 1. [P1] `review-transition-bypasses-record-review`

**Disposition:** `code_fix_required`

`.claude/dev/packet_loop.py:103-117` cho phép `reviewing → running` bằng `transition`, nên có thể quay lại `reviewing` mà không gọi `record-review`. Probe qua public CLI, trên đúng SHA review:

~~~text
reviewing1_rc=0
back_to_running_rc=0
reviewing2_rc=0
state=reviewing
attempts_used=1
attempt_open=true
reviews=[]
finding_counts={}
~~~

Như vậy có thể lặp review↔fix vô hạn trong cùng attempt, không tăng stable finding count và không chạm attempt/same-failure limit. Điều này trái AC3/AC4 và protocol yêu cầu verdict review điều khiển đường quay lại rework.

### 2. [P1] `void-reviewing-accepts-attempt-zero`

**Disposition:** `code_fix_required`

`.claude/dev/packet_loop.py:734-755` giảm `attempts_used` và đóng `attempt_open` nhưng không thoát state `reviewing` hay xoá `reviewing_head_sha`; `record-review` ở dòng 758+ cũng không đòi attempt đang mở và lớn hơn 0. Public-CLI probe:

~~~text
void-attempt --reason quota       rc=0   attempts_used=0, state=reviewing
begin-attempt --provider claude   rc=8   không mở được lượt từ state reviewing
record-review --verdict approve   rc=0
final: state=accepted, accepted_sha=e6e4b73..., reviews[0].attempt=0
~~~

AC8 yêu cầu trả quota mà không tiêu attempt, nhưng không cho phép packet kẹt ở `reviewing` rồi được accepted bằng review của attempt 0.

### 3. [P1] `doctrine-html-quoted-angle-bypass`

**Disposition:** `code_fix_required`

Probe thay nội dung một adapter trong cây tạm dựng từ đúng review SHA bằng:

~~~html
Ghi chú: mer<span title=">">ged:</span> PR đã vào nhánh đích
~~~

Chạy `python3 -B "$TREE/.claude/dev/packet_loop.py" doctrine-scan --root "$TREE"` trả **rc=0**. Trình duyệt render thành cụm cấm `merged: PR đã vào nhánh đích`. Regex tag tại `.claude/dev/packet_loop.py:269-274` cấm ký tự `>` ngay cả khi nó nằm hợp lệ trong quoted attribute, nên tag không bị gỡ. Đây là lớp lọt thứ 19 ngoài danh sách đóng và vi phạm chiều phản chứng của AC2/AC18.

### 4. [P1] `doctrine-common-term-fail-open`

**Disposition:** `code_fix_required`

Adapter tạm chỉ chứa dòng `## Người có thẩm quyền`; cùng entrypoint trả **rc=0**. Cụm này nằm trong forbidden list, nhưng `.claude/dev/packet_loop.py:374-394,959-962` tha mọi bản sao không có dấu `|` hoặc cụm cùng nhóm. AC2 nêu rõ bơm *một cụm từ trong danh sách* vào adapter phải đỏ. AC19 chỉ buộc tha câu văn xuôi kể lại kết quả đo, không cho tha một heading đứng riêng chép nguyên cụm.

### 5. [P2] `ac18-mutation-not-per-class`

**Disposition:** `test_fix_required`

AC18 yêu cầu mỗi lớp có một phản chứng và một đột biến giết đúng ca đó. Nhưng `.claude/dev/packet_loop_test.py:1089-1094` chủ động loại `nbsp_phu_hai_lop` khỏi mọi mutant; mutant `ha_NFKC_ve_NFC` cũng không giết ca ligature vì `casefold()` độc lập vẫn gấp ligature. Ngoài ra runner ở dòng `1606-1621` chỉ chạy tập `phai_chet` do chính mutant khai, nên không chứng minh các ca ngoài tập vẫn sống và không chứng minh “đúng ca đó”. Suite xanh 23/23 vì tiêu chí tự khai hẹp hơn AC18.

### 6. [P2] `ac19-false-positive-matrix-incomplete`

**Disposition:** `test_fix_required`

`LOP_LACH` khai 40 lớp, nhưng `LOP_BAT_OAN` tại `.claude/dev/packet_loop_test.py:1130-1153` chỉ có 14 ca và không có ca bắt-oan riêng cho các chốt mới như bỏ nháy cong, gấp mũi tên, xoá HTML comment, hay tổ hợp dấu/thứ tự chuẩn hoá; ca được mô tả là Cf cũng không chứa ký tự Cf. Không có mapping lớp→ca để chứng minh AC19 “ít nhất một ca bắt-oan cho mỗi lớp”.

### 7. [P2] `ac14-codepage-void-attempt-uncovered`

**Disposition:** `test_fix_required`

Ma trận codepage tại `.claude/dev/packet_loop_test.py:791-817` bỏ lệnh thành công `void-attempt`, dù `.claude/dev/packet_loop.py:734-755` in stdout tiếng Việt. AC14 yêu cầu **mọi** subcommand có stdout được chạy qua cp1258 và cp1252. Việc mutant `bo_cung_hoa_stdout` giết hai ca hiện có không bù được subcommand chưa nằm trong ma trận.

### 8. [P2] `ac20-archive-tree-suite-not-self-contained`

**Disposition:** `spec_revision_required`

Với master lúc cấp lease `3d2c52d62696b0c7c190fd891115f543b0f9cb55`, đúng công thức archive+apply của AC20 cho:

~~~text
doctrine-scan: rc=0, sạch 4 tệp
packet_loop_test.py: rc=1, nền 108/109
failure: legacy_state_khong_co_lease_bi_chan -> fatal: not a git repository
~~~

Thêm `GIT_DIR` trỏ object store của kho nguồn làm suite **109/109, rc=0**; entrypoint mới vẫn lấy từ cây merged, còn object store chỉ cấp blob lịch sử `22d2cc9`, nên đây là phép đo code hợp lệ. Tuy nhiên công thức được spec quy định không tự mang điều kiện này và chạy nguyên văn thì đỏ. Cần sửa AC20 để khai rõ object store/worktree hoặc thay fixture lịch sử bằng artifact tự chứa.

## Lệnh tái lập cốt lõi — chỉ neo SHA bất biến

~~~bash
BASE=fbe5ab9e1ece3b45c065879bfd59dee2554db3e2
REVIEW=e6e4b73dc940fcd04e9030e353e0e5fe7f3f0af8
MASTER=3d2c52d62696b0c7c190fd891115f543b0f9cb55
TREE=$(mktemp -d)
git archive "$MASTER" | tar -x -C "$TREE"
git diff --binary "$BASE..$REVIEW" | git -C "$TREE" apply
python3 -B "$TREE/.claude/dev/packet_loop.py" doctrine-scan --root "$TREE"
python3 -B "$TREE/.claude/dev/packet_loop_test.py"       # rc=1, 108/109
GIT_DIR="$PWD/.git" python3 -B "$TREE/.claude/dev/packet_loop_test.py"  # rc=0, 109/109
~~~

State-machine probes dùng cùng cách dựng cây từ `REVIEW`, `--state-dir "$(mktemp -d)"`, rồi gọi lần lượt public commands `init`, `record-lease`, `begin-attempt`, `record-post`, `transition`, `void-attempt`, `record-review`, `status`; các rc và state quan sát được đã ghi nguyên văn ở findings 1–2. Không gọi hàm nội bộ.

## Evidence §7

~~~yaml
schema_version: 1
packet_id: wp55
revision: 3
generation: 4
provider: codex
role: reviewer
session_id: wp55-r3-review-6-codex-20260815
lease_id: wp55-r3-review-6-codex-20260814
lease_record_commit: 030add230608fc65402c2b40be5fa120118e4f20
lease_expires_at_utc: 2026-08-15T20:00:00Z
independent: true
executor_provider: claude
verdict: changes_requested
reviewed_sha: e6e4b73dc940fcd04e9030e353e0e5fe7f3f0af8
base_sha: fbe5ab9e1ece3b45c065879bfd59dee2554db3e2
spec_commit: 1fce46a4f6094792368307826c6fb16a851b718b
spec_sha256: e321f811724fae97b19d523a3e5159bc13b425cd15fc6c753c7439fe28cae22d
prompt_sha256: e5719fc6e942ec3da9cf7dac66a35c05c3ae2ad86ffca17cb53b6d351e37050c
executor_evidence_commit: a168895eb203aff3b68989ddd155e57e2801b866
master_sha_at_grant: 3d2c52d62696b0c7c190fd891115f543b0f9cb55
master_sha_rechecked: 2531366e1abc6cbca0a6c2765e40e54be38d1fb7
changed_paths_count: 6
protected_paths_changed: 0

tests:
  - name: packet_loop_test exact review tree with source object store
    status: passed
    evidence: "rc=0; baseline 109/109; 23/23 declared mutants killed"
  - name: packet_loop_test exact archive tree without object store
    status: failed
    evidence: "rc=1; baseline 108/109; historical git-show fixture unavailable"
  - name: tl.py --selftest in clean exact-SHA checkout
    status: passed
    evidence: "rc=0; 1696/1696"
  - name: doc-claims-check --strict --json
    status: passed
    evidence: "rc=0; files_scanned=82; flags=[]"
  - name: release-verify --strict --json
    status: passed
    evidence: "rc=0; checked=179; failed=[]; extra_files=[]; errors=[]"
  - name: golden-test
    status: passed
    evidence: "rc=0; case_count=20; no --write"
  - name: eol_policy --all --json
    status: passed
    evidence: "rc=0; scanned=304; violations=[]"
  - name: release-bundle head twice plus base once
    status: passed
    evidence: "rc=0/0/0; all bundle_sha256=20c89545566b7682b3ecd2ac2ac0283add5af8a4d6ca377d9acbcde4487f8590"
  - name: doctrine-scan review tree and merged trees
    status: passed
    evidence: "rc=0; 4 files clean on review, grant-master merged tree, and rechecked-master merged tree"

findings:
  - finding_id: review-transition-bypasses-record-review
    severity: P1
    disposition: code_fix_required
  - finding_id: void-reviewing-accepts-attempt-zero
    severity: P1
    disposition: code_fix_required
  - finding_id: doctrine-html-quoted-angle-bypass
    severity: P1
    disposition: code_fix_required
  - finding_id: doctrine-common-term-fail-open
    severity: P1
    disposition: code_fix_required
  - finding_id: ac18-mutation-not-per-class
    severity: P2
    disposition: test_fix_required
  - finding_id: ac19-false-positive-matrix-incomplete
    severity: P2
    disposition: test_fix_required
  - finding_id: ac14-codepage-void-attempt-uncovered
    severity: P2
    disposition: test_fix_required
  - finding_id: ac20-archive-tree-suite-not-self-contained
    severity: P2
    disposition: spec_revision_required

not_run: []
delivery_path: github_connector
~~~

Không sửa file, commit, push, merge, land hoặc deploy trong lượt review này.
