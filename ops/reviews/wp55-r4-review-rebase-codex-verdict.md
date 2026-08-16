# Rebase verdict

`approve`

`c44b2d4c351cbe7f519e1b46aadf68d45e98af86` nên vào `master`. Phép rebase không
làm thay đổi patch đã được duyệt tại `c47a439997e0191427d775636ebadbf3be7e1481`:
hai diff giống hệt byte-for-byte, kể cả context và vị trí hunk `@@ -79,8 +79,8`.
Hai commit PR #116 giữa base cũ và base mới không sửa `CLAUDE.md`, nên không có thay
đổi nào của PR #116 bị nuốt.

Cả scanner hiện hành lẫn scanner mô phỏng hợp đồng mới (bỏ hoàn toàn nhánh miễn trừ)
đều sạch. Bốn gate bắt buộc đều qua trên một clone tạm detached đúng SHA đang review;
`release-verify` kiểm 179 tệp, `failed=0`, `extra=0`.

## Findings

Không có finding (`findings: []`), nên không có `finding_id`, `severity` hay
`disposition` cần liệt kê.

## Topology và cách land

Tại snapshot ref cục bộ dùng cho review:

- `HEAD^ = d5b7bccd679480f2eb9e7f7d84c518bade7f7df1`.
- `refs/remotes/origin/master = d5b7bccd679480f2eb9e7f7d84c518bade7f7df1`.
- Vì hai SHA bằng nhau, `fast_forward` là cách land đúng.

`refs/heads/master` cục bộ là ref stale ở `3d2c52d62696b0c7c190fd891115f543b0f9cb55`
từ lúc clone; nó không phải tip remote-tracking mà nhiệm vụ neo. Không có bằng chứng
`origin/master` đã dời trong lúc review.

Không kiểm tra được tip GitHub trực tiếp: lệnh
`git ls-remote --heads origin refs/heads/master` trả `rc=128` vì môi trường không kết
nối được proxy mạng (`127.0.0.1:37851`). Vì vậy executor phải fetch/đọc lại
`refs/heads/master` ngay trước khi land; chỉ fast-forward nếu tip vẫn là `d5b7bcc...`.

## Ghi chú môi trường thử

Archive thuần từ `git archive` không có `.git`, nên `eol_policy` và
`doc-claims-check` không thể chạy trong archive đó (`rc=2`). Hai gate này đã được chạy
lại thành công trong clone tạm detached đúng SHA. Clone tạm phải tái lập cấu hình
repo-local `core.abbrev=7`; nếu để Git tự chọn 8 ký tự thì `doc-claims-check` và fixture
golden cố ý đổi kết quả. Sau khi ghim đúng cấu hình của repository review, cả hai trả
`rc=0`.

## Evidence §7

```yaml
reviewed_sha: c44b2d4c351cbe7f519e1b46aadf68d45e98af86
base_sha: d5b7bccd679480f2eb9e7f7d84c518bade7f7df1
tests:
  - name: step_0_identity_and_scope
    command: >-
      git rev-parse HEAD && git rev-parse HEAD^ &&
      git rev-parse --is-shallow-repository &&
      git diff --name-only d5b7bccd679480f2eb9e7f7d84c518bade7f7df1 c44b2d4c351cbe7f519e1b46aadf68d45e98af86 &&
      git diff --shortstat d5b7bccd679480f2eb9e7f7d84c518bade7f7df1 c44b2d4c351cbe7f519e1b46aadf68d45e98af86
    rc: 0
    result: "HEAD/parent đúng; shallow=false; chỉ CLAUDE.md; 2 insertions, 2 deletions"
  - name: patch_identity_with_pre_rebase_approved_commit
    command: >-
      diff <(git diff d5b7bccd679480f2eb9e7f7d84c518bade7f7df1 c44b2d4c351cbe7f519e1b46aadf68d45e98af86 -- CLAUDE.md)
      <(git diff 2531366e1abc6cbca0a6c2765e40e54be38d1fb7 c47a439997e0191427d775636ebadbf3be7e1481 -- CLAUDE.md)
    rc: 0
    result: "hai patch giống hệt, gồm cả header, context và số dòng hunk"
  - name: pr_116_does_not_touch_claude_md
    command: >-
      git diff --name-status 2531366e1abc6cbca0a6c2765e40e54be38d1fb7 d5b7bccd679480f2eb9e7f7d84c518bade7f7df1 -- CLAUDE.md
    rc: 0
    result: "stdout rỗng"
  - name: doctrine_scan_current_contract
    command: >-
      python3 <(git show 1a4525a20aa360476a6f59cb157c21097919c457:.claude/dev/packet_loop.py)
      doctrine-scan --root /tmp/review-rebase-clone-8lzirO-c44b2d4c351cbe7f519e1b46aadf68d45e98af86
    rc: 0
    result: "đã quét 1 tệp, 0 chỗ chép doctrine"
  - name: doctrine_scan_without_exemption
    command: >-
      python3 <(git show 1a4525a20aa360476a6f59cb157c21097919c457:.claude/dev/packet_loop.py |
      sed '/if cum in CUM_NGON_NGU_THUONG and _duoc_tha_vi_ngat_dong(raw, kim):/d')
      doctrine-scan --root /tmp/review-rebase-clone-8lzirO-c44b2d4c351cbe7f519e1b46aadf68d45e98af86
    rc: 0
    result: "đã quét 1 tệp, 0 chỗ chép doctrine"
  - name: eol_policy
    command: "python3 .githooks/eol_policy.py --all --json"
    execution_tree: c44b2d4c351cbe7f519e1b46aadf68d45e98af86
    rc: 0
  - name: doc_claims_strict
    command: "python3 scripts/tl.py doc-claims-check --strict --json"
    execution_tree: c44b2d4c351cbe7f519e1b46aadf68d45e98af86
    repo_config: "core.abbrev=7"
    rc: 0
  - name: release_verify
    command: "python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --root . --strict --json"
    execution_tree: c44b2d4c351cbe7f519e1b46aadf68d45e98af86
    rc: 0
    result: "checked=179 failed=0 extra=0"
  - name: golden_test
    command: "python3 scripts/tl.py golden-test"
    execution_tree: c44b2d4c351cbe7f519e1b46aadf68d45e98af86
    repo_config: "core.abbrev=7"
    rc: 0
  - name: fast_forward_topology_snapshot
    command: >-
      test "$(git rev-parse c44b2d4c351cbe7f519e1b46aadf68d45e98af86^)" =
      "$(git rev-parse refs/remotes/origin/master)"
    rc: 0
  - name: live_remote_tip
    command: "git ls-remote --heads origin refs/heads/master"
    rc: 128
    result: "không chạy được vì môi trường chặn kết nối mạng"
findings: []
land_recommendation: fast_forward
```
