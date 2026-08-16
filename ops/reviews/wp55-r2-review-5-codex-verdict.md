Verdict: `changes_requested` cho PR #92, neo chính xác tại `546ecf9fd4dfe889d0cd3ee77b9589d8bed0465f`.

## Findings

### `merged-tree-doctrine-false-positive` — P1 / blocking

`doctrine-scan` sạch trên branch nhưng đỏ trên cây sau merge với `origin/master=3d2c52d62696b0c7c190fd891115f543b0f9cb55`.

Lệnh tái hiện:

```bash
merged_tmp=$(mktemp -d /tmp/wp55-merged.XXXXXX)
git archive origin/master | tar -x -C "$merged_tmp"
git diff --binary \
  fbe5ab9e1ece3b45c065879bfd59dee2554db3e2..546ecf9fd4dfe889d0cd3ee77b9589d8bed0465f |
  git -C "$merged_tmp" apply
python "$merged_tmp/.claude/dev/packet_loop.py" doctrine-scan --root "$merged_tmp"
```

Kết quả:

```text
/tmp/wp55-merged.../CLAUDE.md:82: [bang-vai-tro-muc-2] chép doctrine: 'người có thẩm quyền'
1 chỗ chép doctrine trong adapter...
rc=6
```

Trong khi:

```bash
git merge-tree \
  fbe5ab9e1ece3b45c065879bfd59dee2554db3e2 \
  origin/master \
  546ecf9fd4dfe889d0cd3ee77b9589d8bed0465f
```

trả `rc=0`, không có conflict marker. Đây là lỗi tương thích tích hợp, không phải merge conflict.

### `partial-lease-authority-bypass` — P1 / blocking

`record-lease` chỉ tạo lease sau khi kiểm `lease_id`, `granted_by`, `evidence` và `expires_utc`. Nhưng `begin-attempt` chỉ đòi `lease` truthy và `expires_utc`, nên chấp nhận state không thể được tạo hợp lệ qua `record-lease`.

Fixture:

```json
{
  "state": "leased",
  "lease": {
    "expires_utc": "2099-01-01T00:00:00Z"
  }
}
```

Lệnh:

```bash
python .claude/dev/packet_loop.py \
  --state-dir <fixture-dir> \
  begin-attempt --packet 55 --provider claude
```

Kết quả:

```text
bắt đầu lượt 1/3 — state running
rc=0
```

Như vậy khẳng định tại dòng 507 rằng `lease` “hợp lệ” và chỉ đạt được qua `record-lease` không được mã cưỡng chế. Một state cũ/hỏng chỉ cần giữ `expires_utc` tương lai là đi vòng qua kiểm tra thẩm quyền.

Các kiểu sai khác:

```text
lease thiếu/null/dict rỗng          rc=8
lease là chuỗi                      rc=1, Traceback
expires_utc là số                   rc=1, Traceback
expires_utc sai/thiếu timezone      rc=2
```

Hai traceback cũng cho thấy nhánh malformed chưa fail-closed có kiểm soát.

## Evidence §7

```yaml
schema_version: 1
packet_id: wp55
revision: 2
generation: 3
provider: codex
role: reviewer
session_id: wp55-r2-review-5-codex-20260814
reviewed_sha: 546ecf9fd4dfe889d0cd3ee77b9589d8bed0465f
base_sha: fbe5ab9e1ece3b45c065879bfd59dee2554db3e2
master_sha_checked: 3d2c52d62696b0c7c190fd891115f543b0f9cb55
independent_from_executor_session: true
review_axes: [spec, standards_security, malformed_state, merged_tree]
tests:
  - packet_loop_test:
      result: 54/54
      mutations_killed: 11/11
      rc: 0
  - tl_selftest_initial:
      result: 1694/1696
      rc: 1
      note: environment commit-signing hook
  - tl_selftest_with_process_local_git_override:
      command: GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false python scripts/tl.py --selftest
      result: 1696/1696
      rc: 0
  - doc_claims_check:
      ok: true
      files: 82
      flags: 0
      rc: 0
  - release_verify:
      ok: true
      expected: 179
      checked: 179
      failed: 0
      extra: 0
      rc: 0
  - golden_test:
      ok: true
      cases: 20
      rc: 0
  - doctrine_entity_probes:
      decimal: 6
      hexadecimal: 6
      named_with_semicolon: 6
      numeric_without_semicolon: 6
      nbsp: 6
      soft_hyphen: 6
      double_encoded_amp_hash_58: 0
  - merge_tree:
      rc: 0
      conflicts: 0
  - doctrine_scan_merged_tree:
      rc: 6
      findings: 1
      location: CLAUDE.md:82
findings:
  - finding_id: merged-tree-doctrine-false-positive
    severity: P1
    disposition: blocking
  - finding_id: partial-lease-authority-bypass
    severity: P1
    disposition: blocking
verdict: changes_requested
assurance: cross_approved
delivery:
  pr_review: not_posted
  issue_evidence: not_posted
  reason: gh unavailable; no GitHub connector exposed; lease is read-only with empty write_set
```

Không có tệp repo, commit hay push nào được tạo. `gh` không được cài và phiên này không có GitHub connector; cần một phiên có quyền đăng nguyên verdict này lên PR #92 và issue #55.
