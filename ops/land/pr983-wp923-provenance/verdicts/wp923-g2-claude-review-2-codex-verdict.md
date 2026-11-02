verdict: approve
reviewed_sha: bbfb96cbe6b30e0b5b1b30982eae2b5893ac2c00
reviewed_tree: 747d266c10c7ae9125f37e49ff6b60e6375c29a9
packet: wp923 r2 g2, cross-review lượt 2/2
role: reviewer
provider: openai_codex
model_family: openai
model: GPT-6 (theo khai báo runtime; snapshot/effort không đo độc lập)
execution_surface: codex_service (agent API với công cụ shell cục bộ)
transport: machine
independent_from_executor_session: true
github_submitter_identity: null
review_class: sensitive
spec_sha256: a36f8d2d84d39c3587a60edcb63d4886f82e3fae097c283700718b5869eecbc1

Chỉ review nội dung exact SHA theo prompt.snapshot; không xác nhận quyền land/deploy hoặc state/lease từ mạng.
Mọi lệnh dưới chạy tại /tmp/claude-0/-home-user-tra-luat/6cf1da84-5813-5156-ad6b-b3a2dbd3ab61/scratchpad/rv2, với GIT_OPTIONAL_LOCKS=0 và PYTHONDONTWRITEBYTECODE=1.
Helper, log và Git object mới của merge-tree ở /tmp; không thay cấu hình kho. Test có sinh artifact ignored trong cay-kho và Git freshen mtime object sẵn có; xem toàn bộ dấu vết và hoàn nguyên ở HƯỚNG 10.
Bằng chứng do reviewer tự chạy, không suy kết quả từ log executor.

## ĐỐI CHIẾU LƯỢT TRƯỚC

VERDICT_LUOT1.md: approve ở 67bacb3b51ac9eda72297b10b15b798b3ca51959; mục FINDINGS không có P0/P1/P2/P3.
Không có finding cũ cần phân loại vá. HƯỚNG 2 đo lại tính đồng nhất từng byte của write set; các hướng sau kiểm phần merge mới.

## BẢNG SĂN

Chấp nhận nội dung head merge trên exact reviewed_sha; không phát hiện finding P0/P1/P2/P3. Ngưỡng theo prompt: approve chỉ khi không còn P0/P1/P2.

| Điều kiện | Kết quả reviewer tự đo |
|---|---|
| SHA/cha/SPEC | passed — H1, H10; đúng head merge, thứ tự cha và hash SPEC đóng băng. |
| Write set so lượt 1 | passed — H2; giống từng byte, blob 813668f08437e3930e92cb96c6032452b6f043f4. |
| Master/Q4/workflow | passed — H3; đường tiến master không đổi hai tệp, có giải thích riêng các merge nhánh phụ trong full-history. |
| N1 | passed — H4; một tệp, +2/−1 chú thích; AST và byte các dòng không phải chú thích bằng master. |
| Cây merge | passed — H5; bằng kết quả merge-tree, tree 747d266c10c7ae9125f37e49ff6b60e6375c29a9. |
| N3 | passed trong phạm vi quét — H6; không có chốt băm nguyên byte sống mới. |
| Bỏ CI/timeout | passed — H7; không có dấu bỏ CI; timeout registry/mảnh/gom là 150/150/10. |
| N2 | passed — H8; rc=0, 28/28 đăng ký, 1070/1070 phản chứng; log bằng từng byte hai log packet. |
| N4 | passed sau sửa môi trường đo — H9; rc=0, 1731/1731; lần đầu 1730/1731 do override abbrev của reviewer, đã đo A/B. |
| Toàn vẹn | passed sau dọn side effect test — H10; 7910 mục khớp snapshot đầu cả byte/mode/mtime, gồm .git; không sửa nội dung tệp có sẵn. |
| N5 | not_run / KHÔNG ĐO ĐƯỢC — không gọi mạng; không khẳng định CI PR xanh. |

Các lần đo chưa đạt và nguyên nhân được giữ nguyên lệnh/output trong từng hướng; kết quả sau xử lý được ghi tiếp phía dưới.

### HƯỚNG 1: Neo exact SHA, SPEC, cha merge và mốc toàn vẹn

Giả thuyết: Review nhầm head/spec, thiếu master trong tổ tiên hoặc cây làm việc bẩn khiến các phép đo vô hiệu.

Lệnh:

````bash
git -C cay-kho rev-parse HEAD 'HEAD^{tree}'
````

Output thật (exit code 0):

````text
bbfb96cbe6b30e0b5b1b30982eae2b5893ac2c00
747d266c10c7ae9125f37e49ff6b60e6375c29a9
````

Lệnh:

````bash
git -C cay-kho log -1 --format=%P
````

Output thật (exit code 0):

````text
67bacb3b51ac9eda72297b10b15b798b3ca51959 09db70350414d767b793a71cb630e643f216a1b1
````

Lệnh:

````bash
git -C cay-kho branch --show-current
````

Output thật (exit code 0):

````text
(không có output)
````

Lệnh:

````bash
git -C cay-kho --no-optional-locks status --porcelain=v1 --untracked-files=all
````

Output thật (exit code 0):

````text
(không có output)
````

Lệnh:

````bash
sha256sum SPEC.md
````

Output thật (exit code 0):

````text
a36f8d2d84d39c3587a60edcb63d4886f82e3fae097c283700718b5869eecbc1  SPEC.md
````

Lệnh:

````bash
python - <<'PY'
import hashlib, json, os, stat, subprocess
from pathlib import Path
H = "bbfb96cbe6b30e0b5b1b30982eae2b5893ac2c00"
P = "67bacb3b51ac9eda72297b10b15b798b3ca51959"
M = "09db70350414d767b793a71cb630e643f216a1b1"
B = "e139e55883d90fd74a358230be5599c9e223d4b3"
def git(*a):
    return subprocess.check_output(["git", "-C", "cay-kho", *a]).decode().strip()
assert git("rev-parse", "HEAD") == H
assert git("log", "-1", "--format=%P").split() == [P, M]
assert hashlib.sha256(Path("SPEC.md").read_bytes()).hexdigest() == "a36f8d2d84d39c3587a60edcb63d4886f82e3fae097c283700718b5869eecbc1"
for a, b in ((B, M), (M, H), (P, H)):
    cp = subprocess.run(["git", "-C", "cay-kho", "merge-base", "--is-ancestor", a, b])
    print(f"ancestor {a} -> {b}: rc={cp.returncode}")
    assert cp.returncode == 0
assert not git("status", "--porcelain=v1", "--untracked-files=all")
root = Path("cay-kho")
snapshot = {}
for p in sorted(root.rglob("*")):
    s = p.lstat()
    item = dict(mode=stat.S_IMODE(s.st_mode), mtime_ns=s.st_mtime_ns)
    if p.is_symlink():
        item.update(kind="symlink", target=os.readlink(p))
    elif p.is_file():
        data = p.read_bytes()
        item.update(kind="file", size=len(data), sha256=hashlib.sha256(data).hexdigest())
    elif p.is_dir():
        item.update(kind="directory")
    else:
        item.update(kind="other")
    snapshot[str(p.relative_to(root))] = item
dest = Path("/tmp/wp923-r2-independent/repository-before.json")
dest.write_text(json.dumps(snapshot, sort_keys=True))
print(f"snapshot_all_repository_entries_including_dot_git={len(snapshot)}")
print("snapshot_saved=" + str(dest))
print("head_parents_spec_ancestry_clean_status=PASS")
PY
````

Output thật (exit code 0):

````text
ancestor e139e55883d90fd74a358230be5599c9e223d4b3 -> 09db70350414d767b793a71cb630e643f216a1b1: rc=0
ancestor 09db70350414d767b793a71cb630e643f216a1b1 -> bbfb96cbe6b30e0b5b1b30982eae2b5893ac2c00: rc=0
ancestor 67bacb3b51ac9eda72297b10b15b798b3ca51959 -> bbfb96cbe6b30e0b5b1b30982eae2b5893ac2c00: rc=0
snapshot_all_repository_entries_including_dot_git=7910
snapshot_saved=/tmp/wp923-r2-independent/repository-before.json
head_parents_spec_ancestry_clean_status=PASS
````

Kết luận: KHÔNG PHẢI LỖI — HEAD, thứ tự hai cha, SPEC đóng băng và ancestry đều khớp; worktree ban đầu sạch. Đã chụp byte/mode/mtime toàn kho gồm .git để đối chiếu cuối lượt.

### HƯỚNG 2: Write set giữ nguyên TỪNG BYTE so với lượt 1

Giả thuyết: Merge có thể lén thay byte của tệp đã được duyệt, kể cả thay đổi AST không thấy.

Lệnh:

````bash
python - <<'PY'
import hashlib, subprocess
from pathlib import Path
path = ".claude/dev/ci_dang_ky_test.py"
revs = {
    "old_base": "e139e55883d90fd74a358230be5599c9e223d4b3",
    "round1": "67bacb3b51ac9eda72297b10b15b798b3ca51959",
    "new_master": "09db70350414d767b793a71cb630e643f216a1b1",
    "reviewed_merge": "bbfb96cbe6b30e0b5b1b30982eae2b5893ac2c00",
}
blobs = {}
for label, rev in revs.items():
    data = subprocess.check_output(["git", "-C", "cay-kho", "show", f"{rev}:{path}"])
    oid = subprocess.check_output(["git", "-C", "cay-kho", "rev-parse", f"{rev}:{path}"]).decode().strip()
    blobs[label] = data
    print(f"{label}: blob={oid} bytes={len(data)} sha256={hashlib.sha256(data).hexdigest()}")
equal = blobs["round1"] == blobs["reviewed_merge"]
local = Path("cay-kho", path).read_bytes() == blobs["reviewed_merge"]
print(f"round1_equals_merge_every_byte={equal}")
print(f"worktree_equals_reviewed_commit_every_byte={local}")
print(f"old_base_equals_new_master_every_byte={blobs['old_base'] == blobs['new_master']}")
assert equal and local and blobs["old_base"] == blobs["new_master"]
PY
````

Output thật (exit code 0):

````text
old_base: blob=a6dc4081f9aadc46a543b6c3e3f0f85a7b113685 bytes=171085 sha256=9ff2b624c8dd00cc1ed874a91bba77af9d1c2dd81ed3884f47735f1e76dbd56c
round1: blob=813668f08437e3930e92cb96c6032452b6f043f4 bytes=171189 sha256=fa188c1efe944fae03f3d310180fff1a3afd17b38b86adbca04b8f630bccfe0c
new_master: blob=a6dc4081f9aadc46a543b6c3e3f0f85a7b113685 bytes=171085 sha256=9ff2b624c8dd00cc1ed874a91bba77af9d1c2dd81ed3884f47735f1e76dbd56c
reviewed_merge: blob=813668f08437e3930e92cb96c6032452b6f043f4 bytes=171189 sha256=fa188c1efe944fae03f3d310180fff1a3afd17b38b86adbca04b8f630bccfe0c
round1_equals_merge_every_byte=True
worktree_equals_reviewed_commit_every_byte=True
old_base_equals_new_master_every_byte=True
````

Lệnh:

````bash
git -C cay-kho diff --exit-code 67bacb3b51ac9eda72297b10b15b798b3ca51959 bbfb96cbe6b30e0b5b1b30982eae2b5893ac2c00 -- .claude/dev/ci_dang_ky_test.py
````

Output thật (exit code 0):

````text
(không có output)
````

Kết luận: KHÔNG PHẢI LỖI — OID, SHA-256 và so bytes trực tiếp đều xác nhận tệp ở head merge bằng lượt 1; bản trên đĩa bằng blob được review.

### HƯỚNG 3: Master tiến có chạm write set hoặc workflow timeout không

Giả thuyết: Q4 có thể bị vi phạm hoặc timeout đã đổi; cần phân biệt đường tiến master với nhánh phụ cũ được merge.

Lệnh:

````bash
git -C cay-kho diff --stat e139e55883d90fd74a358230be5599c9e223d4b3 09db70350414d767b793a71cb630e643f216a1b1
````

Output thật (exit code 0):

````text
 .claude/skills/cross-review/SKILL.md               |    4 +
 .claude/skills/land-packets/SKILL.md               |    6 +
 ops/land/pr945-wp899-land-evidence.yaml            |  273 +++
 ops/land/pr945-wp899-provenance/SHA256SUMS.txt     |   52 +
 .../ci-provenance-40268583877.stdout.txt           |    6 +
 .../do-1026-cebb5b2/ci-provenance-40268583877.yaml |  190 +++
 .../ci-provenance-40268583940.stdout.txt           |   27 +
 .../do-1026-cebb5b2/ci-provenance-40268583940.yaml | 1562 +++++++++++++++++
 .../diff-1f731c7-4511b1e-write-set.patch           |   15 +
 .../gate-evidence-12628631748.zip.sha256           |    1 +
 .../graphql-output-chu-kho-dan-pr945.json          |   18 +
 .../log-gate-121401313206-trich.txt                |   35 +
 .../do-1026-cebb5b2/review-11-VERDICT-dau.txt      |   12 +
 .../review-11-dinh-danh-reviewer.json              |   20 +
 .../do-1026-cebb5b2/review-11-run.json             |  102 ++
 .../do-1026-cebb5b2/tl-selftest-Linux.json         |    1 +
 .../do-1026-cebb5b2/tl-selftest-Linux.out          | 1777 ++++++++++++++++++++
 .../workflow-definition-cebb5b2.txt                |   19 +
 .../readback-artifacts-40268583877.json            |    1 +
 .../readback-artifacts-40268583940.json            |    1 +
 .../readback-check-runs-4511b1e.json               |    1 +
 .../readback-comments-945.json                     |    1 +
 .../readback-commit-cebb5b2.json                   |    1 +
 .../readback-events-945.json                       |    1 +
 .../readback-jobs-40264014854.json                 |    1 +
 .../readback-jobs-40268583877.json                 |    1 +
 .../readback-jobs-40268583940.json                 |    1 +
 .../pr945-wp899-provenance/readback-pr-945.json    |    1 +
 .../readback-reactions-pr-945.json                 |    1 +
 .../readback-review-comments-945.json              |    1 +
 .../readback-reviews-945.json                      |    1 +
 .../readback-run-40264014854.json                  |    1 +
 .../readback-run-40268583877.json                  |    1 +
 .../readback-run-40268583940.json                  |    1 +
 .../review-a-4511b1e/VERDICT.md                    |  121 ++
 .../review-a-4511b1e/dinh-danh-reviewer.json       |   28 +
 .../review-a-4511b1e/prompt.md                     |   41 +
 .../review-a-4511b1e/reviewer-D05-results.json     |   14 +
 .../review-a-4511b1e/reviewer-MUTANT_CATALOGUE.md  |  298 ++++
 .../review-a-4511b1e/reviewer-baseline.json        |   12 +
 .../review-a-4511b1e/reviewer-encoding_child.py    |    6 +
 .../reviewer-encoding_criterion.py                 |   12 +
 .../reviewer-evidence-manifest.json                |  546 ++++++
 .../reviewer-git-commit-encoding-results.json      |   85 +
 .../reviewer-git-noncommit-encoding-results.json   |   16 +
 .../reviewer-git_commit_encoding.py                |   49 +
 .../review-a-4511b1e/reviewer-identity.json        |   32 +
 .../review-a-4511b1e/reviewer-mutant-results.json  |  326 ++++
 .../review-a-4511b1e/reviewer-mutants.py           |   29 +
 .../review-a-4511b1e/reviewer-product-probes.json  |  699 ++++++++
 .../reviewer-snapshot-comparison.json              |    5 +
 .../review-a-4511b1e/reviewer-spec-provenance.json |   26 +
 .../reviewer-supplemental-results.json             |  477 ++++++
 .../review-a-4511b1e/reviewer-supplemental.py      |   37 +
 .../review-a-4511b1e/reviewer-versions.json        |   23 +
 .../review-a-4511b1e/run.json                      |  373 ++++
 ops/land/pr963-wp943-land-evidence.yaml            |    8 +
 ops/land_evidence_nguon.py                         |   36 +
 ops/land_evidence_nguon_test.py                    |  131 ++
 59 files changed, 7566 insertions(+)
````

Lệnh:

````bash
git -C cay-kho log --full-history --format='%H %s' --name-status e139e55883d90fd74a358230be5599c9e223d4b3..09db70350414d767b793a71cb630e643f216a1b1 -- .claude/dev/ci_dang_ky_test.py .github/workflows/ci.yml
````

Output thật (exit code 0):

````text
74132ce20cb1f9f74e163717908eca384f672dd0 Merge pull request #955 from ducthangho/claude/bookkeeping-945-land
600a71a8e1c2b4267c6e6d31338c1b9f0ec4e80a Merge origin/master (7129f7d) vao agent/land-evidence-l7-claude
````

Lệnh:

````bash
python - <<'PY'
import subprocess
B = "e139e55883d90fd74a358230be5599c9e223d4b3"
M = "09db70350414d767b793a71cb630e643f216a1b1"
def git(*a):
    return subprocess.check_output(["git", "-C", "cay-kho", *a])
changed = git("diff", "--name-only", B, M).decode().splitlines()
print(f"master_net_changed_paths={len(changed)}")
for path in (".claude/dev/ci_dang_ky_test.py", ".github/workflows/ci.yml"):
    history = git("log", "--full-history", "--format=%H", f"{B}..{M}", "--", path).decode().splitlines()
    before = git("rev-parse", f"{B}:{path}").decode().strip()
    after = git("rev-parse", f"{M}:{path}").decode().strip()
    print(f"{path}: net_changed={path in changed}; touching_commits={len(history)}; old_blob={before}; master_blob={after}")
    assert path not in changed and not history and before == after
assert len(changed) == 59
print("Q4_and_workflow_history=PASS")
PY
````

Output thật (exit code 1):

````text
master_net_changed_paths=59
.claude/dev/ci_dang_ky_test.py: net_changed=False; touching_commits=2; old_blob=a6dc4081f9aadc46a543b6c3e3f0f85a7b113685; master_blob=a6dc4081f9aadc46a543b6c3e3f0f85a7b113685
Traceback (most recent call last):
  File "<stdin>", line 13, in <module>
AssertionError
````

Lệnh:

````bash
git -C cay-kho log --first-parent --format='%H %s' --name-status e139e55883d90fd74a358230be5599c9e223d4b3..09db70350414d767b793a71cb630e643f216a1b1 -- .claude/dev/ci_dang_ky_test.py .github/workflows/ci.yml
````

Output thật (exit code 0):

````text
(không có output)
````

Lệnh:

````bash
git -C cay-kho log --no-merges --format='%H %s' --name-status e139e55883d90fd74a358230be5599c9e223d4b3..09db70350414d767b793a71cb630e643f216a1b1 -- .claude/dev/ci_dang_ky_test.py .github/workflows/ci.yml
````

Output thật (exit code 0):

````text
(không có output)
````

Lệnh:

````bash
python - <<'PY'
import subprocess
B = "e139e55883d90fd74a358230be5599c9e223d4b3"
M = "09db70350414d767b793a71cb630e643f216a1b1"
paths = (".claude/dev/ci_dang_ky_test.py", ".github/workflows/ci.yml")
def git(*a):
    return subprocess.check_output(["git", "-C", "cay-kho", *a]).decode().strip()
commits = git("rev-list", "--first-parent", B + ".." + M).splitlines()
print(f"master_first_parent_commits={len(commits)}")
for c in commits:
    for p in paths:
        same = git("rev-parse", c + ":" + p) == git("rev-parse", B + ":" + p)
        diff = git("diff", "--name-only", c + "^1", c, "--", p)
        print(f"{c} {p}: equals_old_base={same}; changed_vs_first_parent={bool(diff)}")
        assert same and not diff
assert not git("log", "--no-merges", "--format=%H", B + ".." + M, "--", *paths)
stale_merge = "600a71a8e1c2b4267c6e6d31338c1b9f0ec4e80a"
parents = git("show", "-s", "--format=%P", stale_merge).split()
print("side_branch_sync_merge=" + stale_merge)
print("side_branch_sync_parents=" + " ".join(parents))
cp = subprocess.run(["git", "-C", "cay-kho", "merge-base", "--is-ancestor", parents[1], B])
print(f"sync_imported_master_is_already_ancestor_of_old_base: rc={cp.returncode}")
assert cp.returncode == 0
for p in paths:
    adopted_old_master = git("rev-parse", stale_merge + ":" + p) == git("rev-parse", parents[1] + ":" + p)
    print(f"side_branch_sync {p}: equals_imported_old_master={adopted_old_master}")
    assert adopted_old_master
print("Q4_and_workflow_on_actual_master_progression=PASS")
PY
````

Output thật (exit code 0):

````text
master_first_parent_commits=4
09db70350414d767b793a71cb630e643f216a1b1 .claude/dev/ci_dang_ky_test.py: equals_old_base=True; changed_vs_first_parent=False
09db70350414d767b793a71cb630e643f216a1b1 .github/workflows/ci.yml: equals_old_base=True; changed_vs_first_parent=False
155ac3ad933507f3fcc91f5792747153980e25f2 .claude/dev/ci_dang_ky_test.py: equals_old_base=True; changed_vs_first_parent=False
155ac3ad933507f3fcc91f5792747153980e25f2 .github/workflows/ci.yml: equals_old_base=True; changed_vs_first_parent=False
74132ce20cb1f9f74e163717908eca384f672dd0 .claude/dev/ci_dang_ky_test.py: equals_old_base=True; changed_vs_first_parent=False
74132ce20cb1f9f74e163717908eca384f672dd0 .github/workflows/ci.yml: equals_old_base=True; changed_vs_first_parent=False
c8d92ba05c3ea875d8f84d94195430302690286d .claude/dev/ci_dang_ky_test.py: equals_old_base=True; changed_vs_first_parent=False
c8d92ba05c3ea875d8f84d94195430302690286d .github/workflows/ci.yml: equals_old_base=True; changed_vs_first_parent=False
side_branch_sync_merge=600a71a8e1c2b4267c6e6d31338c1b9f0ec4e80a
side_branch_sync_parents=cb1c7074be7a85efec42f427a594a49b2315d710 7129f7de204a6f92db8e29e8a5a79383d4907029
sync_imported_master_is_already_ancestor_of_old_base: rc=0
side_branch_sync .claude/dev/ci_dang_ky_test.py: equals_imported_old_master=True
side_branch_sync .github/workflows/ci.yml: equals_imported_old_master=True
Q4_and_workflow_on_actual_master_progression=PASS
````

Kết luận: KHÔNG PHẢI LỖI — master tiến qua 4 commit first-parent, không commit nào đổi hai tệp; net diff và OID đều khớp base cũ. Phép assert full-history ban đầu thất bại vì log còn liệt kê merge nhánh phụ 600a71a và merge nhập nó 74132ce. Đo bổ sung cho thấy 600a71a chỉ đồng bộ từ master 7129f7d vốn đã là tổ tiên base cũ; không có non-merge commit nào trong range sửa hai tệp. Không diễn giải hai dòng full-history thành thay đổi mới trên master.

### HƯỚNG 4: Diff master..merge: đúng +2/−1 chú thích và AST không đổi

Giả thuyết: Merge có thể mang thêm tệp, sửa dòng mã hoặc làm patch khác nội dung lượt 1.

Lệnh:

````bash
git -C cay-kho -c core.abbrev=7 diff --numstat 09db70350414d767b793a71cb630e643f216a1b1 bbfb96cbe6b30e0b5b1b30982eae2b5893ac2c00
````

Output thật (exit code 0):

````text
2	1	.claude/dev/ci_dang_ky_test.py
````

Lệnh:

````bash
git -C cay-kho -c core.abbrev=7 diff 09db70350414d767b793a71cb630e643f216a1b1 bbfb96cbe6b30e0b5b1b30982eae2b5893ac2c00
````

Output thật (exit code 0):

````text
diff --git a/.claude/dev/ci_dang_ky_test.py b/.claude/dev/ci_dang_ky_test.py
index a6dc408..813668f 100644
--- a/.claude/dev/ci_dang_ky_test.py
+++ b/.claude/dev/ci_dang_ky_test.py
@@ -756,7 +756,7 @@ def dem_la_do(chap_nhan, o_trong_ci):
 
 # CI-SONG-SONG-REGISTRY-G5-MOT-LAN r1 (#637): M1–M3, M6, M7. Hằng số trong W1 theo spec M3.
 # #643 (chủ kho chọn "b", PR #644): 3600 → 4500. Đo run 36208617323, N=2 chế độ đủ: `nhanh_don_duoc_test` 3306,45 s = 92 %
-# trần cũ. KHÔNG bảo đảm cả job dưới `timeout-minutes` (nay 105): bộ ấy còn chờ worker trống (run trên: bắt đầu sau 337 s),
+# trần cũ. KHÔNG bảo đảm cả job dưới `timeout-minutes` (#705: 105 · #910 pha B, a7da463: 150): bộ ấy còn chờ worker trống (run trên: bắt đầu sau 337 s),
 # Windows ép N=1 ⇒ dài hơn; trần job là trần NGOÀI. Ca `p643-tran-bo-nho-hon-timeout-job` chỉ khoá trần bộ < trần job.
 # #705 (CI-REGISTRY-NANG-TRAN-BO-DAY-DU, chủ kho Q4): 4500 → 5400, job 90 → 105 phút. `nhanh_don_duoc_test` chế độ đủ:
 # 3645 s xanh (run 36642392330) rồi > 4500 s ĐỎ ba lần (36696528580 ×2, 36839918701) — runner chậm 22–42 % (hai bộ vô can
@@ -806,6 +806,7 @@ LENH_REGISTRY = frozenset({"git config --global core.autocrlf false", "git confi
                            "ruff --version", "python .claude/dev/ci_dang_ky_test.py --chay"})
 BAM_GATE_REGISTRY = "89516cf77c3ce734feadf348bfea8180254c67e8e8ec62a48e2f6ea1dc038452"
 # WP748 r16: hai job nay la `targeted_mutant_gate` (NHANH_DON_DUOC_DICH, gom `--gop-dich`, tran 30 phut).
+# #910 pha B (PR #917, a7da463): tran job manh 30 -> 150; job gom van 10.
 BAM_GATE_NHANH = "fe061a50668af83b6c9b6939f881ba37a30083bc72a27b52c2e02350835d626b"
 GOC_TAI_LIEU = frozenset({"AGENTS.md", "CHANGELOG.md", "CLAUDE.md", "CONTEXT.md", "INSTALL.md", "README.md", "SKILL.md"})
````

Lệnh:

````bash
python - <<'PY'
import ast, hashlib, subprocess
from pathlib import Path
M = "09db70350414d767b793a71cb630e643f216a1b1"
H = "bbfb96cbe6b30e0b5b1b30982eae2b5893ac2c00"
path = ".claude/dev/ci_dang_ky_test.py"
def git(*a):
    return subprocess.check_output(["git", "-C", "cay-kho", "-c", "core.abbrev=7", *a])
names = git("diff", "--name-only", M, H).decode().splitlines()
patch = git("diff", M, H)
changed = [x for x in patch.decode().splitlines() if x.startswith(("+", "-")) and not x.startswith(("+++", "---"))]
counts = (sum(x.startswith("+") for x in changed), sum(x.startswith("-") for x in changed))
print(f"changed_paths={names!r}")
print(f"added={counts[0]}; removed={counts[1]}; all_changed_lines_are_comments={all(x[1:].lstrip().startswith('#') for x in changed)}")
a, b = (git("show", f"{r}:{path}").decode() for r in (M, H))
ast_equal = ast.dump(ast.parse(a)) == ast.dump(ast.parse(b))
strip_comments = lambda s: "".join(x for x in s.splitlines(keepends=True) if not x.lstrip().startswith("#")).encode()
aa, bb = strip_comments(a), strip_comments(b)
print(f"AST_equal_to_master={ast_equal}")
print(f"non_comment_bytes_equal={aa == bb}; sha256={hashlib.sha256(aa).hexdigest()}")
expected_patch = Path("diff_vs_master.patch").read_bytes()
print(f"actual_patch_matches_executor_artifact_every_byte={patch == expected_patch}")
assert names == [path] and counts == (2, 1) and all(x[1:].lstrip().startswith("#") for x in changed)
assert ast_equal and aa == bb and patch == expected_patch
print("N1=PASS")
PY
````

Output thật (exit code 0):

````text
changed_paths=['.claude/dev/ci_dang_ky_test.py']
added=2; removed=1; all_changed_lines_are_comments=True
AST_equal_to_master=True
non_comment_bytes_equal=True; sha256=e21cc849f68036961e3c7339c472e1776b417bdfbdf33c4bdc4da9d58dd73875
actual_patch_matches_executor_artifact_every_byte=True
N1=PASS
````

Kết luận: KHÔNG PHẢI LỖI — diff chỉ có một tệp, +2/−1 đều là chú thích, AST và toàn bộ byte các dòng không phải chú thích bằng master; patch cung cấp khớp byte phép đo độc lập.

### HƯỚNG 5: Cây merge đúng kết quả merge-tree tự động

Giả thuyết: Commit merge có thể có phần tự giải quyết xung đột hoặc chỉnh nội dung ngoài hai nhánh.

Lệnh:

````bash
python - <<'PY'
import os, subprocess, tempfile
from pathlib import Path
repo = Path("cay-kho").resolve()
M = "09db70350414d767b793a71cb630e643f216a1b1"
P = "67bacb3b51ac9eda72297b10b15b798b3ca51959"
H = "bbfb96cbe6b30e0b5b1b30982eae2b5893ac2c00"
expected = subprocess.check_output(["git", "-C", str(repo), "rev-parse", H + "^{tree}"]).decode().strip()
objects = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "--git-path", "objects"]).decode().strip()
objects = Path(objects)
if not objects.is_absolute():
    objects = repo / objects
with tempfile.TemporaryDirectory(prefix="wp923-merge-objects-") as td:
    isolated = Path(td, "objects")
    isolated.mkdir()
    env = dict(os.environ, GIT_OBJECT_DIRECTORY=str(isolated),
               GIT_ALTERNATE_OBJECT_DIRECTORIES=str(objects.resolve()), GIT_OPTIONAL_LOCKS="0")
    print("object_write_directory_outside_repository=" + str(isolated))
    command = ["git", "-C", str(repo), "merge-tree", "--write-tree", M, P]
    print("actual_command=" + " ".join(command))
    cp = subprocess.run(command, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = cp.stdout.decode()
    print(f"merge_tree_exit_code={cp.returncode}")
    print("merge_tree_output:\n" + output, end="" if output.endswith("\n") else "\n")
    actual = output.splitlines()[0] if output else ""
    print("reviewed_tree=" + expected)
    print(f"automatic_merge_tree_equals_reviewed_tree={actual == expected}")
    assert cp.returncode == 0 and actual == expected
    print("no_manual_conflict_resolution_content=PASS")
PY
````

Output thật (exit code 0):

````text
object_write_directory_outside_repository=/tmp/wp923-merge-objects-hafv9m3x/objects
actual_command=git -C /tmp/claude-0/-home-user-tra-luat/6cf1da84-5813-5156-ad6b-b3a2dbd3ab61/scratchpad/rv2/cay-kho merge-tree --write-tree 09db70350414d767b793a71cb630e643f216a1b1 67bacb3b51ac9eda72297b10b15b798b3ca51959
merge_tree_exit_code=0
merge_tree_output:
747d266c10c7ae9125f37e49ff6b60e6375c29a9
reviewed_tree=747d266c10c7ae9125f37e49ff6b60e6375c29a9
automatic_merge_tree_equals_reviewed_tree=True
no_manual_conflict_resolution_content=PASS
````

Kết luận: KHÔNG PHẢI LỖI — merge-tree --write-tree 09db703 67bacb3 rc=0, tree bằng exact tree của reviewed_sha. Object mới được ghi vào thư mục tạm ngoài cay-kho. Phép đối chiếu cuối phát hiện mtime hai object có sẵn trong kho đổi; byte/mode không đổi và mtime được hoàn nguyên tại HƯỚNG 10.

### HƯỚNG 6: N3: chốt băm nguyên byte mới do master mang vào

Giả thuyết: Tệp master thêm/đổi có thể ghim OID hoặc SHA-256 cũ của ci_dang_ky_test.py, làm sửa chú thích gây đỏ gate.

Lệnh:

````bash
python - <<'PY'
import hashlib, re, subprocess
from pathlib import Path
B = "e139e55883d90fd74a358230be5599c9e223d4b3"
M = "09db70350414d767b793a71cb630e643f216a1b1"
H = "bbfb96cbe6b30e0b5b1b30982eae2b5893ac2c00"
target = ".claude/dev/ci_dang_ky_test.py"
def git(*a):
    return subprocess.check_output(["git", "-C", "cay-kho", *a])
needles = {}
for label, rev in (("master", M), ("reviewed", H)):
    data = git("show", rev + ":" + target)
    oid = git("rev-parse", rev + ":" + target).strip()
    digest = hashlib.sha256(data).hexdigest().encode()
    for kind, value in (("blob", oid), ("sha256", digest)):
        needles[label + "_" + kind] = value
        needles[label + "_" + kind + "_prefix"] = value[:7 if kind == "blob" else 12]
        print(label + "_" + kind + "=" + value.decode())
changed = git("diff", "--name-only", "--diff-filter=ACMRT", B, M).decode().splitlines()
full_tree = git("ls-tree", "-r", "--name-only", H).decode().splitlines()
all_digest_hits = []
for scope, names in (("master_new_or_changed", changed), ("reviewed_full_tree", full_tree)):
    hits = []
    for name in names:
        data = Path("cay-kho", name).read_bytes()
        for label, needle in needles.items():
            if needle in data:
                for i, line in enumerate(data.splitlines(), 1):
                    if needle in line:
                        hits.append((name, i, label))
    print(f"{scope}: scanned_files={len(names)}; full_or_prefix_digest_hits={len(hits)}")
    for hit in hits:
        print("digest_hit=" + repr(hit))
    all_digest_hits.extend(hits)
refs = []
for name in changed:
    data = Path("cay-kho", name).read_text(encoding="utf-8", errors="replace")
    for i, line in enumerate(data.splitlines(), 1):
        for match in re.finditer("ci_dang_ky_test", line):
            snippet = line[max(0, match.start()-100):match.end()+160]
            refs.append((name, i, snippet))
print(f"master_new_or_changed_filename_reference_occurrences={len(refs)}")
for name, line, snippet in refs:
    print(f"{name}:{line}: [context around occurrence] {snippet}")
out = Path("/tmp/wp923-r2-independent/n3-master-references.json")
out.write_text(__import__("json").dumps(refs, ensure_ascii=False, indent=2))
print("master_reference_scan_saved=" + str(out))
manifest = Path("cay-kho/RELEASE_MANIFEST.json").read_bytes()
print(f"release_manifest_mentions_target={b'ci_dang_ky_test' in manifest}")
print(f"release_manifest_mentions_dot_claude={b'.claude/' in manifest}")
assert not all_digest_hits
print("no_literal_blob_sha256_pin_in_master_delta_or_reviewed_tree=PASS")
PY
````

Output thật (exit code 1):

````text
master_blob=a6dc4081f9aadc46a543b6c3e3f0f85a7b113685
master_sha256=9ff2b624c8dd00cc1ed874a91bba77af9d1c2dd81ed3884f47735f1e76dbd56c
reviewed_blob=813668f08437e3930e92cb96c6032452b6f043f4
reviewed_sha256=fa188c1efe944fae03f3d310180fff1a3afd17b38b86adbca04b8f630bccfe0c
master_new_or_changed: scanned_files=59; full_or_prefix_digest_hits=0
Traceback (most recent call last):
  File "<stdin>", line 24, in <module>
  File "/usr/lib/python3.13/pathlib/_abc.py", line 625, in read_bytes
    with self.open(mode='rb') as f:
         ~~~~~~~~~^^^^^^^^^^^
  File "/usr/lib/python3.13/pathlib/_local.py", line 537, in open
    return io.open(self, mode, buffering, encoding, errors, newline)
           ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: 'cay-kho/"ops/reviews/pr896-review-5-codex/review_evidence/H\\306\\257\\341\\273\\232NG 10 - HINT tren ban sao.log"'
````

Lệnh:

````bash
python - <<'PY'
import subprocess
args = ["rg", "-n", "--hidden", "--glob", "!.git/**", "--glob", "!*.md",
        "--glob", "!ops/land/**", "--glob", "!ops/reviews/**", "--glob", "!ops/leases/**",
        "ci_dang_ky_test", "."]
cp = subprocess.run(args, cwd="cay-kho", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
print("actual_command_in_cay_kho=" + repr(args))
print(f"rg_exit_code={cp.returncode}")
print(cp.stdout.decode(), end="")
assert cp.returncode in (0, 1)
PY
````

Output thật (exit code 0):

````text
actual_command_in_cay_kho=['rg', '-n', '--hidden', '--glob', '!.git/**', '--glob', '!*.md', '--glob', '!ops/land/**', '--glob', '!ops/reviews/**', '--glob', '!ops/leases/**', 'ci_dang_ky_test', '.']
rg_exit_code=0
./.claude/dev/chay-cong-windows_test.ps1:208:                   '.claude/dev/packet_loop_test.py', '.claude/dev/ci_dang_ky_test.py',
./.claude/dev/chay-cong-windows_test.ps1:880:    Set-Content -LiteralPath (Join-Path $k '.claude/dev/ci_dang_ky_test.py') -Encoding utf8NoBOM -Value @'
./.claude/dev/chay-cong-windows_test.ps1:950:    Set-Content -LiteralPath (Join-Path $k '.claude/dev/ci_dang_ky_test.py') -Encoding utf8NoBOM -Value ($ktRo +
./.claude/dev/chay-cong-windows.ps1:94:    script kết thúc — một `ci_dang_ky_test.py --chay` gõ tay sau đó trong phiên ấy lấy kế hoạch NHẸ từ SHA CŨ.
./.claude/dev/chay-cong-windows.ps1:548:Chay-Py   'registry test'           @('.claude/dev/ci_dang_ky_test.py', '--chay')
./.claude/dev/ci_dang_ky_test.py:76:    ".claude/dev/ci_dang_ky_test.py",
./.claude/dev/ci_dang_ky_test.py:447:        module = py[:2] == ["-m", "ci_dang_ky_test"] or py[:1] == ["-mci_dang_ky_test"]
./.claude/dev/ci_dang_ky_test.py:448:        file = bool(py) and _ten_tep(py[0]) == "ci_dang_ky_test.py"
./.claude/dev/ci_dang_ky_test.py:554:    Registry: python [cờ] <đường dẫn ci_dang_ky_test.py> hoặc -m ci_dang_ky_test, đúng --chay.
./.claude/dev/ci_dang_ky_test.py:668:        if x == ".claude/dev/ci_dang_ky_test.py":
./.claude/dev/ci_dang_ky_test.py:669:            co = "python .claude/dev/ci_dang_ky_test.py --chay" in workflows
./.claude/dev/ci_dang_ky_test.py:676:    if "python .claude/dev/ci_dang_ky_test.py --chay" not in workflows:
./.claude/dev/ci_dang_ky_test.py:787:# #651 M2: `ci_dang_ky_test.py` ra khỏi vùng (bộ chọn tự canh bằng `phan_chung` mọi lượt); `.github/**` → riêng `ci.yml`.
./.claude/dev/ci_dang_ky_test.py:806:                           "ruff --version", "python .claude/dev/ci_dang_ky_test.py --chay"})
./.claude/dev/ci_dang_ky_test.py:915:            if "python .claude/dev/ci_dang_ky_test.py --chay" in _dong_lenh(b)]
./.claude/dev/ci_dang_ky_test.py:958:    reg = [b for b in ky_vong if "python .claude/dev/ci_dang_ky_test.py --chay" in _dong_lenh(b)]
./.claude/dev/ci_dang_ky_test.py:1308:            reg, wf = {".claude/dev/a_test.py"}, "python .claude/dev/ci_dang_ky_test.py --chay"
./.claude/dev/ci_dang_ky_test.py:1334:        reg_g, wf_g = {".claude/dev/a_test.py"}, "python .claude/dev/ci_dang_ky_test.py --chay"
./.claude/dev/ci_dang_ky_test.py:1517:    _reg = {"name": "test registry", "run": "python .claude/dev/ci_dang_ky_test.py --chay"}
./.claude/dev/ci_dang_ky_test.py:1544:    _tab = dict(_reg, run="python .claude/dev/ci_dang_ky_test.py\t--chay")
./.claude/dev/ci_dang_ky_test.py:1630:        ("registry-module", {"gate": {"steps": [_ruff, {"run": "python -m ci_dang_ky_test --chay"}]}}, None, 0),
./.claude/dev/ci_dang_ky_test.py:1739:                {"run": "python .claude/dev/ci_dang_ky_test.py" + _tail}]}}, None, 1))
./.claude/dev/ci_dang_ky_test.py:1981:        run="python .claude/dev/ci_dang_ky_test.py --chay\n" + b[i]["run"])))
./.claude/dev/ci_dang_ky_test.py:1988:    _them("p637-A7-nang-doi-ten-cai-truoc-probe", _hong_wf("gate-registry", lambda b, i: b.insert(i, {"name": "cài registry", "run": "python .claude/dev/ci_dang_ky_test.py --chay"})))
./.claude/dev/ci_dang_ky_test.py:2146:                          ("bo-chon-nhe", {".claude/dev/ci_dang_ky_test.py"}, CHE_DO_NHE),
./.claude/dev/ci_dang_ky_test.py:2220:                          ("bo-chon-nhe", {".claude/dev/ci_dang_ky_test.py"}, CHE_DO_NHE),
./.claude/dev/ci_dang_ky_test.py:2243:    def _buoc_reg(j): return next(b for b in j["steps"] if "ci_dang_ky_test.py --chay" in str(b.get("run", "")))
./.claude/dev/ci_dang_ky_test.py:2320:        f(next(b for b in w["jobs"]["gate-registry"]["steps"] if "ci_dang_ky_test.py --chay" in str(b.get("run", ""))), w)
./.claude/dev/ci_dang_ky_test.py:2341:    # #651 M2: bộ chọn `ci_dang_ky_test.py` được miễn có chủ đích (tự canh bằng `phan_chung`; lượt đủ hằng tuần bù).
./.claude/dev/ci_dang_ky_test.py:2344:                                                   and t != ".claude/dev/ci_dang_ky_test.py"))
./.claude/hooks/pretooluse_guard_test.py:833:# Do run 36238709647: bo nay 756,50 s tren gate-registry, ca nen chi 10,2 s. `ci_dang_ky_test.py`
./.claude/hooks/subagent_ghi_detect_test.py:1621:    `.claude/dev/ci_dang_ky_test.py` bao DO "don thu muc tam that bai" du bo `rc=0`.
./.claude/dev/doc_receipt_thu_hoi_test.py:258:    cdk = _nap(GOC / "ci_dang_ky_test.py", "ci_dang_ky_duoi_test")
./.github/workflows/ci-dot-bien-du.yml:3:# #651 (CI-REGISTRY-THU-HEP-VUNG r1) M4 — bù phần chốt nới của #651 (`ci_dang_ky_test.py`, `.github/**` trừ `ci.yml` không còn
./.github/workflows/ci-dot-bien-du.yml:5:# Chốt `loi_workflow_dot_bien_du` (`.claude/dev/ci_dang_ky_test.py`): mọi giá trị hoặc GHIM, hoặc BẰNG `gate-registry` của
./.github/workflows/ci-dot-bien-du.yml:67:        run: python .claude/dev/ci_dang_ky_test.py --chay
./.github/workflows/ci.yml:22:  # GIỮ hành vi cũ (hai nền). Cùng từ vựng với `launcher-windows.yml` — ghim ở `.claude/dev/ci_dang_ky_test.py`.
./.github/workflows/ci.yml:513:  # (`.claude/dev/ci_dang_ky_test.py`) ghim hình dạng hai job này; `N` trong `CONG_CU_TEST_MANH` phải khớp matrix.
./.github/workflows/ci.yml:953:    # `GIAY_TOI_DA_MOT_BO` (.claude/dev/ci_dang_ky_test.py). 105 vẫn cỡ theo UBUNTU, KHÔNG bảo đảm Windows.
./.github/workflows/ci.yml:1003:      # Sổ ở ci_dang_ky_test.py được đối chiếu với phép tìm tệp trên cây. Các tệp dưới
./.github/workflows/ci.yml:1015:        run: python .claude/dev/ci_dang_ky_test.py --chay
./ops/ci_provenance.py:23:CI_DANG_KY = ROOT / ".claude/dev/ci_dang_ky_test.py"
./ops/kiem_trang_quyet_dinh.sh:20:# `ci_dang_ky_test.py` chỉ quét `*_test.py` nên một `*_test.sh` KHÔNG nằm trong sổ, tức không có
./ops/ci_duong_nhanh_test.py:9:    `ci-if-cap-job-gate-ops-va-buoc-sau-g5-khong-co-cong-canh` (Q6-i chủ kho): `JOB_G5` của `ci_dang_ky_test.py` KHÔNG chứa
./ops/ci_duong_nhanh_test.py:310:                  "ops/ci_duong_nhanh_test.py", ".claude/dev/ci_dang_ky_test.py"):
./ops/ci_duong_nhanh_test.py:2435:# Doi bieu thuc (vd `always()`), bo no, hay them `if:` cap job vao job KHAC (ke ca cung bieu thuc) deu phai DO. `ci_dang_ky_test.loi_g5_workflow` canh cung khoa ay tu phia #668.
./ops/ci_duong_nhanh_test.py:2580:    return runpy.run_path(str(CAY / ".claude" / "dev" / "ci_dang_ky_test.py"))
./ops/ci_duong_nhanh_test.py:2586:    bang(DA_NOI_MUC in m["DANG_KY"], f"ci_dang_ky_test.DA_NOI phai co {DA_NOI_MUC!r}")
./ops/ci_duong_nhanh_test.py:2597:    src = (CAY / ".claude" / "dev" / "ci_dang_ky_test.py").read_text(encoding="utf-8")
./ops/ci_duong_nhanh_test.py:2598:    bang(src.count(f'"{DA_NOI_MUC}"') == 1, f"muc {DA_NOI_MUC!r} phai xuat hien dung mot lan trong ci_dang_ky_test.py")
./ops/ci_duong_nhanh_test.py:3094:    for dp in ("ops/ci_duong_nhanh.py", "ops/ci_duong_nhanh_test.py", ".claude/dev/ci_dang_ky_test.py", "ops/lease_publish.py"):
./ops/ci_duong_nhanh_test.py:3113:    return runpy.run_path(str(goc / ".claude" / "dev" / "ci_dang_ky_test.py"))
./ops/ci_duong_nhanh_test.py:3137:MA, YML, DK = "ops/ci_duong_nhanh.py", ".github/workflows/ci.yml", ".claude/dev/ci_dang_ky_test.py"
./ops/land_evidence_nguon.py:39:Không sửa hồ sơ nào. Lên CI GIÁN TIẾP: `ops/land_evidence_nguon_test.py` đăng ký trong `.claude/dev/ci_dang_ky_test.py`, ca `c11`
./ops/ci_provenance_test.py:27:CI_DANG_KY = ROOT_THAT / ".claude/dev/ci_dang_ky_test.py"
./ops/ci_provenance_test.py:145:        p = Path(thu) / "ci_dang_ky_test.py"
./ops/lease_publish_test.py:8927:    regex của t125 đọc chúng; `ci_dang_ky_test.py` kiểm DA_NOI và wiring của wrapper.
````

Lệnh:

````bash
git -C cay-kho diff --unified=5 e139e55883d90fd74a358230be5599c9e223d4b3 09db70350414d767b793a71cb630e643f216a1b1 -- ops/land_evidence_nguon.py ops/land_evidence_nguon_test.py
````

Output thật (exit code 0):

````text
diff --git a/ops/land_evidence_nguon.py b/ops/land_evidence_nguon.py
index b0cb158..5e6e382 100644
--- a/ops/land_evidence_nguon.py
+++ b/ops/land_evidence_nguon.py
@@ -25,10 +25,16 @@ LUẬT:
       bỏ qua có ghi nhận. Băm lệch ⇒ mất miễn trừ, kiểm đủ luật. Bản kỳ vọng CHÉP RIÊNG trong test: thêm tên ⇒ ĐỎ.
   L6  (#845, `ops/specs/land-evidence-landed-chua-dien-r1.md`) Chỉ khi `trang_thai_packet` là mapping CÓ khoá `landed`:
       `landed` không phải bool ⇒ ĐỎ. `landed: true` ⇒ `post_merge_checks` và `bookkeeping` phải là list KHÁC RỖNG mà mọi
       phần tử là mapping (kiểm KIỂU, không đoán chuỗi giữ chỗ — PR #840 merge suýt mang `landed: true` với hai trường ấy là
       chuỗi `CHO_DIEN`, connector P1 4309577154), và không chuỗi nào chứa `CHO_DIEN`. `landed: false` (bản nháp) ⇒ không đòi.
+  L7  (#748, `ops/specs/land-evidence-l7-assurance-thuc-thi-r1.md`) `assurance_81.reviewer_assurance_81` chuẩn hoá (bỏ khoảng
+      trắng hai đầu, viết hoa, khoảng trắng ⇒ `_`) bằng `DAT` ⇒ `assurance_81.thuc_thi` phải là mapping có `model`, `effort`,
+      `sandbox_mode`, mỗi khoá là lời khai `measured` (cùng `RE_KHAI_DO`, nên L1 tự đòi nguồn). Chặt hơn chữ đặc tả: chuẩn hoá
+      thêm NFC và nhận cả cách viết có dấu `ĐẠT` — chỉ đúng hai cách viết ấy, KHÔNG bỏ dấu đại trà (review l7a P2: `ĐẤT`, `DẠT`
+      là giá trị khác, phải để L7 không áp). Giá trị khác ⇒ không đòi. Connector P1 PR #934 (4372912640): hồ sơ khai ĐẠT
+      khi biên nhận chỉ đo model. `MIEN_TRU_L7` = 3 hồ sơ đã khai như thế (nợ `NO-L7-3-HO-SO-KHAI-DAT-THIEU-DO`), cơ chế như L5.
 
 ĐIỀU CỔNG NÀY KHÔNG LÀM (đặc tả `ngoai_pham_vi`): L1 chỉ đo "lời khai trỏ tới thứ CÓ THẬT", KHÔNG đo thứ ấy chứng minh câu
 văn — một tệp vô can vẫn làm L1 qua. Chỉ L2 đọc NỘI DUNG, và chỉ cho token số. Hồ sơ cũ đi qua miễn trừ, không được kiểm.
 Không sửa hồ sơ nào. Lên CI GIÁN TIẾP: `ops/land_evidence_nguon_test.py` đăng ký trong `.claude/dev/ci_dang_ky_test.py`, ca `c11`
 của nó gọi bộ kiểm này trên cây thật (bản trước ghi "chưa nằm trên đường CI" — cũ từ lease g2 #773, review #845 lượt 1 P3).
@@ -40,10 +46,11 @@ import datetime
 import glob
 import hashlib
 import json
 import re
 import sys
+import unicodedata
 from pathlib import Path
 
 for _s in (sys.stdout, sys.stderr):
     if hasattr(_s, "reconfigure"):
         _s.reconfigure(encoding="utf-8", errors="backslashreplace")
@@ -90,10 +97,20 @@ RE_DAI = re.compile(rf"(?<![{_KT}])[{_KT}]+")
 RE_DUOI_NGUON = re.compile(r"\.(?:json|txt|log|yaml|yml|md|sh|py|patch)$")
 RE_SO_POS = re.compile(r"(?<!\d)\d+/\d+(?!\d)|(?<![A-Za-z0-9_])hong \d+(?!\d)")
 RE_MOC = re.compile(r"\d{4}-\d{2}-\d{2}[Tt ]\d{2}:\d{2}(?::\d{2}(?:\.\d+)?)?(?:[Zz]|[+-]\d{2}:?\d{2})?(?![\d:])")
 L6_PHAN_HOAN_TAT = ("post_merge_checks", "bookkeeping")   # cây thật 19-10-2026: mọi hồ sơ landed true đã có cả hai
 L6_DAU_GIU_CHO = "CHO_DIEN"
+L7_KHOA = ("model", "effort", "sandbox_mode")
+L7_MUC_DAT = ("DAT", "ĐẠT")   # sau `_chuan_hoa_81`; dạng NFC
+# L7 — đo 2026-10-27 trên `7129f7d` (băm chụp lại sau #962/#966 sửa pr924, pr950; tên giữ nguyên như ở `f577ab5`):
+# 3 hồ sơ khai DAT mà thiếu `thuc_thi`. KHÔNG thêm tên mới; chụp lại băm chỉ khi có comment chủ kho cho phép —
+# tự chụp lại mỗi lần hồ sơ đổi là xoá đúng tín hiệu "băm lệch ⇒ mất miễn trừ".
+MIEN_TRU_L7 = {
+    "pr924-wp923-land-evidence.yaml": "f246000294972947543a1afb3d9122b43ea11f8e540c4927ebda8d7a202d8f5b",
+    "pr931-wp835-land-evidence.yaml": "31c8ce908aa08631a58993b1e431d4653b01b23b87ed59926181f2df4df485da",
+    "pr950-wp834-land-evidence.yaml": "b0ae6da9f1f919d1f6ae785ad6950b94dd37f99c0a2852d31d5aaee645a6a080",
+}
 
 
 class KhongDoDuoc(Exception):
     """Đầu vào không đo được (L4). Không bao giờ quy thành ĐẠT."""
 
@@ -283,13 +300,32 @@ def kiem_ho_so(tep, byte, goc, yaml):
                 ds = du_lieu.get(khoa)
                 if not (isinstance(ds, list) and ds and all(isinstance(x, dict) for x in ds)):
                     vp.append(f"L6 $.{khoa}: landed true mà không phải danh sách mapping khác rỗng — {str(ds)[:60]!r}")
             vp += [f"L6 {d}: landed true mà còn dấu giữ chỗ {L6_DAU_GIU_CHO} — {v[:60]!r}"
                    for d, v in nut if isinstance(v, str) and L6_DAU_GIU_CHO in v]
+    a81 = du_lieu.get("assurance_81") if isinstance(du_lieu, dict) else None
+    if isinstance(a81, dict) and _chuan_hoa_81(a81.get("reviewer_assurance_81")) in L7_MUC_DAT:   # L7
+        bam, tt7 = MIEN_TRU_L7.get(tep.name), a81.get("thuc_thi")
+        mien = bam is not None and hashlib.sha256(byte).hexdigest() == bam
+        if bam is not None:
+            ghi.append("L7 miễn trừ (băm khớp ảnh chụp, nợ NO-L7-3-HO-SO-KHAI-DAT-THIEU-DO)" if mien
+                       else "L7 mất miễn trừ: băm lệch ảnh chụp — kiểm đủ")
+        if not mien and not isinstance(tt7, dict):
+            vp.append(f"L7 $.assurance_81.thuc_thi: khai DAT mà không có mapping đo thực thi — {str(tt7)[:60]!r}")
+        elif not mien:
+            vp += [f"L7 $.assurance_81.thuc_thi.{k}: khai DAT mà không phải lời khai measured — {str(tt7.get(k))[:60]!r}"
+                   for k in L7_KHOA if not (isinstance(tt7.get(k), str) and RE_KHAI_DO.match(tt7[k]))]
     return vp, ghi
 
 
+def _chuan_hoa_81(v):
+    """`' đạt '` (NFC hay NFD) ⇒ `ĐẠT`, `'chua dat'` ⇒ `CHUA_DAT`; không phải chuỗi ⇒ None (L7 không áp)."""
+    if not isinstance(v, str):
+        return None
+    return re.sub(r"\s+", "_", unicodedata.normalize("NFC", v).strip().upper())
+
+
 def main(argv=None):
     ap = argparse.ArgumentParser(description="Cổng nguồn cho lời khai trong ops/land/*-land-evidence.yaml (#773).")
     ap.add_argument("--root", default=str(ROOT))
     ap.add_argument("--tep", nargs="+", default=None, help="chỉ kiểm các tệp này (tương đối với --root hoặc tuyệt đối)")
     a = ap.parse_args(argv)
diff --git a/ops/land_evidence_nguon_test.py b/ops/land_evidence_nguon_test.py
index 2af6930..2542dc1 100644
--- a/ops/land_evidence_nguon_test.py
+++ b/ops/land_evidence_nguon_test.py
@@ -15,10 +15,11 @@ import io
 import json
 import os
 import subprocess
 import sys
 import tempfile
+import unicodedata
 from unittest import mock
 from pathlib import Path
 
 sys.dont_write_bytecode = True
 for _s in (sys.stdout, sys.stderr):
@@ -34,10 +35,14 @@ PROV = "pr9001-thu-provenance"
 # L5 — bản kỳ vọng CHÉP RIÊNG dạng VÂN TAY: sha256 của `json.dumps(sorted(MIEN_TRU_CUTOVER.items()))` đo trên `c73af7b`
 # (16-10-2026), 28 tên. Thêm/đổi/bỏ một tên hay một băm trong bộ kiểm ⇒ c10 ĐỎ; danh sách đọc được nằm trong bộ kiểm.
 L6_TRUONG = ("post_merge_checks", "bookkeeping")   # chép riêng, không đọc từ bộ kiểm: bỏ một trường ở đó ⇒ c16 ĐỎ
 KY_VONG_SO_MIEN_TRU = 28
 KY_VONG_VAN_TAY_MIEN_TRU = "5311e7557cd75ef2f3b06371c66a4830d4970613c1e98a8fd4af732d7dab2257"
+# L7 — cùng cách chép riêng, đo trên `7129f7d` (27-10-2026): 3 hồ sơ khai DAT thiếu `thuc_thi`. Đổi danh sách ⇒ c19 ĐỎ.
+L7_KHOA = ("model", "effort", "sandbox_mode")   # chép riêng: bỏ một khoá ở bộ kiểm ⇒ c17 ĐỎ
+KY_VONG_SO_MIEN_TRU_L7 = 3
+KY_VONG_VAN_TAY_MIEN_TRU_L7 = "6b5ef08603e37239742fe5d7fe8cbe933b24e33174cf3af04c453b0e7be83574"
 
 
 class TinHieuChotCa(AssertionError):
     """Chỉ `bang()` ném lớp này ⇒ phân biệt được giết thật (chốt) với chết vì lỗi vô can."""
 
@@ -340,10 +345,94 @@ def c16_l6_landed_true_phai_co_phan_hoan_tat():
         ky(hs.format(ld, tot, bk), None, 1, f"landed {ld} không phải bool", "phải là bool")
     ky(hs.format("false", "'CHO_DIEN — POST_MERGE'", "'CHO_DIEN — BOOKKEEPING'"), None, 0, "bản nháp landed false được giữ chỗ")
     ky("post_merge_checks: 'CHO_DIEN'\n", None, 0, "không có trang_thai_packet.landed ⇒ L6 không áp")
 
 
+P7 = {"run.json": "{}"}
+DU7 = {k: "measured — run.json" for k in L7_KHOA}
+
+
+def hs7(muc, thuc_thi=None):
+    """Hồ sơ L7: `assurance_81.reviewer_assurance_81 = muc`; `thuc_thi` dict ⇒ mapping, chuỗi ⇒ vô hướng, None ⇒ không có."""
+    hs = f"assurance_81:\n  reviewer_assurance_81: {muc}\n"
+    if isinstance(thuc_thi, dict):
+        return hs + "  thuc_thi:\n" + "".join(f"    {k}: '{v}'\n" for k, v in thuc_thi.items())
+    return hs + (f"  thuc_thi: '{thuc_thi}'\n" if thuc_thi is not None else "")
+
+
+@ca
+def c17_l7_khai_dat_phai_do_thuc_thi():
+    """#748 L7: khai §8.1 DAT đòi `thuc_thi.{model,effort,sandbox_mode}` là lời khai measured (connector P1 PR #934)."""
+    ky(hs7("DAT", DU7), P7, 0, "DAT đủ ba khoá measured có nguồn")
+    ky(hs7("DAT"), P7, 1, "DAT thiếu thuc_thi", "L7 $.assurance_81.thuc_thi:")
+    ky(hs7("DAT", "measured — run.json"), P7, 1, "thuc_thi vô hướng", "L7 $.assurance_81.thuc_thi:")
+    for k in L7_KHOA:   # review l7d P3: mapping RỖNG vẫn phải kiểm đủ ba khoá
+        ky(hs7("DAT") + "  thuc_thi: {}\n", P7, 1, f"thuc_thi {{}} thiếu {k}", f"L7 $.assurance_81.thuc_thi.{k}:")
+    ky(hs7("DAT") + "thuc_thi:\n" + "".join(f"  {k}: '{v}'\n" for k, v in DU7.items()), P7, 1,
+       "thuc_thi ở GỐC không thay được thuc_thi dưới assurance_81", "L7 $.assurance_81.thuc_thi:")
+    for k in L7_KHOA:
+        ky(hs7("DAT", {x: v for x, v in DU7.items() if x != k}), P7, 1, f"thiếu {k}", f"L7 $.assurance_81.thuc_thi.{k}:")
+        for sai in ("not_measured — run.json", "da do — run.json", "measuredx run.json"):
+            ky(hs7("DAT", DU7 | {k: sai}), P7, 1, f"{k} = {sai!r}", f"L7 $.assurance_81.thuc_thi.{k}:")
+        for tho in ("null", "true", "3", "['measured — run.json']", "{a: 'measured — run.json'}"):   # review l7a P3: có mặt, không phải chuỗi
+            hs = hs7("DAT", {x: v for x, v in DU7.items() if x != k}) + f"    {k}: {tho}\n"
+            ky(hs, P7, 1, f"{k} = {tho} (không phải chuỗi)", f"L7 $.assurance_81.thuc_thi.{k}:")
+    ky(hs7("DAT", DU7 | {"model": "measured — khong-co.json"}), P7, 1, "measured không nguồn thì L1 bắt", "L1 $.assurance_81")
+    nfd = unicodedata.normalize("NFD", "đạt")
+    for muc in ("Dat", "' DAT '", "dat", "ĐẠT", "Đạt", "'  đạt  '", nfd):   # chuẩn hoá: hoa thường, khoảng trắng, NFC/NFD
+        ky(hs7(muc), P7, 1, f"biến thể {muc!r}", "L7 $.assurance_81.thuc_thi:")
+    for muc in ("CHUA_DAT", "CHUA DAT", "'chua dat'", "CHƯA ĐẠT", "DAT_MOT_PHAN", "1", "true", "null", "[DAT]",
+                "ĐẤT", "DẠT", "ĐAT", "dát"):   # review l7a P2: chữ khác dấu là giá trị KHÁC, không phải DAT
+        ky(hs7(muc), P7, 0, f"{muc!r} không phải DAT ⇒ L7 không áp")
+    for hs in ("assurance_81: DAT\n", "assurance_81: [{reviewer_assurance_81: DAT}]\n", "x: {reviewer_assurance_81: DAT}\n",
+               "reviewer_assurance_81: DAT\n", "assurance_81: {}\n", "DAT\n", "null\n",
+               "- {assurance_81: {reviewer_assurance_81: DAT}}\n"):   # review l7e P3: phạm vi áp — vị trí, có mặt, hình dạng gốc
+        try:
+            rc, ra = chay(hs, P7)
+        except Exception as e:   # traceback không phải ĐẠT
+            rc, ra = -1, f"{type(e).__name__}: {e}"
+        bang(rc == 0 and "L7" not in ra, f"L7 không áp cho {hs.strip()!r}: rc={rc} {ra[-200:]}")
+
+
+@ca
+def c18_l7_mien_tru_theo_bam():
+    hs = hs7("DAT")
+    with cay(hs, P7) as goc:
+        m = nap()
+        m.MIEN_TRU_L7[TEN] = hashlib.sha256(hs.encode()).hexdigest()
+        rc, ra = kiem(m, goc)
+        bang(rc == 0 and "L7 miễn trừ" in ra, f"băm khớp ⇒ miễn trừ L7 có ghi nhận: rc={rc} {ra[-200:]}")
+        for nd, mong in ((hs + " ", 1), (hs7("DAT", DU7), 0)):
+            (goc / "ops/land" / TEN).write_text(nd, encoding="utf-8", newline="")
+            rc, ra = kiem(m, goc)
+            bang(rc == mong and "L7 mất miễn trừ" in ra and "L7 miễn trừ" not in ra,
+                 f"băm lệch ⇒ mất miễn trừ, kiểm đủ (mong rc={mong}): rc={rc} {ra[-300:]}")
+        (goc / "ops/land" / TEN).write_text(hs, encoding="utf-8", newline="")   # review l7c P3: đĩa giữ byte được miễn trừ
+        vp, ghi = m.kiem_ho_so(goc / "ops/land" / TEN, (hs + " ").encode(), goc, __import__("yaml"))
+        bang(any(x.startswith("L7 $.assurance_81.thuc_thi:") for x in vp) and "L7 mất miễn trừ" in " ".join(ghi),
+             f"băm miễn trừ phải đo CHÍNH ảnh byte đã nạp, không đọc lại đĩa: {vp} {ghi}")
+        tep, yml = goc / "ops/land" / TEN, __import__("yaml")   # review l7d P3: miễn trừ gắn TÊN + băm, và chỉ bỏ qua L7
+        m.MIEN_TRU_L7.clear()
+        m.MIEN_TRU_L7["pr9999-khac-land-evidence.yaml"] = hashlib.sha256(hs.encode()).hexdigest()
+        vp, ghi = m.kiem_ho_so(tep, hs.encode(), goc, yml)
+        bang(any(x.startswith("L7 $.assurance_81.thuc_thi:") for x in vp) and not ghi,
+             f"cùng byte dưới TÊN khác không được miễn trừ: {vp} {ghi}")
+        for them, luat in (("x: 'measured — khong-co.json'\n", "L1"), ("trang_thai_packet: {landed: true}\n", "L6")):
+            m.MIEN_TRU_L7[TEN] = hashlib.sha256((hs + them).encode()).hexdigest()
+            vp, ghi = m.kiem_ho_so(tep, (hs + them).encode(), goc, yml)
+            bang(any(x.startswith(luat) for x in vp) and not any(x.startswith("L7") for x in vp)
+                 and "L7 miễn trừ" in " ".join(ghi), f"miễn trừ L7 không được xoá vi phạm {luat}: {vp} {ghi}")
+
+
+@ca
+def c19_l7_danh_sach_dong_bang():
+    ds = nap().MIEN_TRU_L7
+    van_tay = hashlib.sha256(json.dumps(sorted(ds.items())).encode()).hexdigest()
+    bang(len(ds) == KY_VONG_SO_MIEN_TRU_L7 and van_tay == KY_VONG_VAN_TAY_MIEN_TRU_L7,
+         f"MIEN_TRU_L7 trôi khỏi ảnh chụp: {len(ds)} tên, vân tay {van_tay[:12]}…")
+
+
 @ca
 def c12_dong_cuoi_dung_dinh_dang():
     import re
     rc, ra = chay("x: 'measured — a.json'\n", {"a.json": "{}"})
     dong = ra.rstrip("\n").splitlines()[-2:]
@@ -425,10 +514,52 @@ DOT_BIEN = (   # (tên, chuỗi gốc, chuỗi thay, TIỀN TỐ ca đích). Chu
     ("L6_O_null_thanh_hop_le", "ds = du_lieu.get(khoa)\n",
      "ds = du_lieu.get(khoa)\n                ds = [{}] if ds is None and khoa in du_lieu else ds\n", "c16"),
     ("L6_P_phan_tu_so", "all(isinstance(x, dict) for x in ds)", "all(isinstance(x, (dict, int, float)) for x in ds)", "c16"),
     ("L6_Q_list_la_trang_thai", 'if isinstance(tt, dict) and "landed" in tt:   # L6',
      'if isinstance(tt, (dict, list)) and "landed" in tt:   # L6', "c16"),
+    ("L7_bo_ca_luat", 'in L7_MUC_DAT:   # L7', 'in ():   # L7', "c17"),
+    ("L7_bo_strip", 'normalize("NFC", v).strip().upper()', 'normalize("NFC", v).upper()', "c17"),
+    ("L7_bo_viet_hoa", ".strip().upper())", ".strip())", "c17"),
+    ("L7_bo_nfc", 'unicodedata.normalize("NFC", v).strip()', 'v.strip()', "c17"),
+    ("L7_bo_cach_viet_co_dau", 'L7_MUC_DAT = ("DAT", "ĐẠT")', 'L7_MUC_DAT = ("DAT",)', "c17"),
+    ("L7_bo_dau_dai_tra", 'unicodedata.normalize("NFC", v).strip()',
+     '"".join(c for c in unicodedata.normalize("NFD", v.replace("đ", "d").replace("Đ", "D")) if not unicodedata.combining(c)).strip()', "c17"),
+    ("L7_thieu_thuc_thi_chi_ghi_chu", 'vp.append(f"L7 $.assurance_81.thuc_thi: khai', 'ghi.append(f"L7 $.assurance_81.thuc_thi: khai', "c17"),
+    ("L7_bo_kiem_khoa", "        elif not mien:\n", "        elif False:\n", "c17"),
+    ("L7_khong_doi_measured", " and RE_KHAI_DO.match(tt7[k]))]", ")]", "c17"),
+    ("L7_nhan_khong_phai_chuoi", "if not (isinstance(tt7.get(k), str) and RE_KHAI_DO.match(tt7[k]))]",
+     "if not (k in tt7 and (not isinstance(tt7[k], str) or RE_KHAI_DO.match(tt7[k])))]", "c17"),
+    ("L7_bo_model", 'L7_KHOA = ("model", "effort", "sandbox_mode")', 'L7_KHOA = ("effort", "sandbox_mode")', "c17"),
+    ("L7_bo_effort", 'L7_KHOA = ("model", "effort", "sandbox_mode")', 'L7_KHOA = ("model", "sandbox_mode")', "c17"),
+    ("L7_bo_sandbox_mode", 'L7_KHOA = ("model", "effort", "sandbox_mode")', 'L7_KHOA = ("model", "effort")', "c17"),
+    ("L7_mien_tru_bo_so_bam", "mien = bam is not None and hashlib.sha256(byte).hexdigest() == bam", "mien = bam is not None", "c18"),
+    ("L7_bam_doc_lai_dia", "and hashlib.sha256(byte).hexdigest() == bam", "and hashlib.sha256(tep.read_bytes()).hexdigest() == bam", "c18"),
+    ("L7_map_rong_bo_kiem", "        elif not mien:\n", "        elif not mien and tt7:\n", "c17"),
+    ("L7_thuc_thi_o_goc", 'a81.get("thuc_thi")', '(du_lieu.get("thuc_thi") or a81.get("thuc_thi"))', "c17"),
+    ("L7_bam_bo_ten", "mien = bam is not None and hashlib.sha256(byte).hexdigest() == bam",
+     "mien = hashlib.sha256(byte).hexdigest() in MIEN_TRU_L7.values()", "c18"),
+    ("L7_mien_xoa_vi_pham_truoc", "        if not mien and not isinstance(tt7, dict):\n",
+     "        if mien:\n            vp.clear()\n        if not mien and not isinstance(tt7, dict):\n", "c18"),
+    ("L7_mien_tru_khong_ghi", '"L7 miễn trừ (băm khớp ảnh chụp, nợ NO-L7-3-HO-SO-KHAI-DAT-THIEU-DO)" if mien', '"" if mien', "c18"),
+    # review l7e P3: phạm vi áp. Tương đương (reviewer đo, không cấp mutant): bỏ riêng `bam is not None`, bỏ thay khoảng
+    # trắng bằng `_`, thu `elif not mien` thành `elif isinstance(tt7, dict)` (mọi ảnh miễn trừ thật đều thiếu thuc_thi).
+    ("L7_dat_o_goc", 'du_lieu.get("assurance_81") if isinstance(du_lieu, dict) else None',
+     'du_lieu.get("assurance_81", du_lieu) if isinstance(du_lieu, dict) else None', "c17"),
+    ("L7_thieu_khoa_mac_dinh_dat", 'a81.get("reviewer_assurance_81")', 'a81.get("reviewer_assurance_81", "DAT")', "c17"),
+    ("L7_goc_list_mo_goi", 'du_lieu.get("assurance_81") if isinstance(du_lieu, dict) else None',
+     'du_lieu.get("assurance_81") if isinstance(du_lieu, dict) else (du_lieu[0].get("assurance_81") if isinstance(du_lieu, list)'
+     ' and du_lieu and isinstance(du_lieu[0], dict) else None)', "c17"),
+    ("L7_bo_kiem_goc_mapping", 'du_lieu.get("assurance_81") if isinstance(du_lieu, dict) else None', 'du_lieu.get("assurance_81")', "c17"),
+    ("L7_a81_list_mo_goi", '    if isinstance(a81, dict) and _chuan_hoa_81(',
+     '    a81 = a81[0] if isinstance(a81, list) and a81 and isinstance(a81[0], dict) else a81\n    if isinstance(a81, dict) and _chuan_hoa_81(', "c17"),
+    ("L7_moi_muc_deu_ap", 'in L7_MUC_DAT:   # L7', 'in L7_MUC_DAT or True:   # L7', "c17"),
+    ("L7_khong_chuoi_thanh_dat", "    if not isinstance(v, str):\n        return None\n",
+     "    if not isinstance(v, str):\n        return \"DAT\" if v is True or v == 1 else None\n", "c17"),
+    ("L7_ghi_chu_khong_can_ten", "        if bam is not None:\n            ghi.append(", "        if True:\n            ghi.append(", "c18"),
+    ("L7_khong_bao_gio_mien", "mien = bam is not None and hashlib.sha256(byte).hexdigest() == bam", "mien = False", "c18"),
+    ("L7_mat_mien_tru_khong_ghi", 'else "L7 mất miễn trừ: băm lệch ảnh chụp — kiểm đủ")', 'else "L7 kiểm đủ")', "c18"),
+    ("L7_noi_danh_sach", "MIEN_TRU_L7 = {\n", "MIEN_TRU_L7 = {\n    \"pr9999-tan-cong-land-evidence.yaml\": \"0\" * 64,\n", "c19"),
 )
 TU_KIEM = (   # (tên, gốc, thay, ca đích, hạng mong đợi)
     ("vo_can_KeyError", "def token_nguon(chuoi):\n", "def token_nguon(chuoi):\n    raise KeyError('vo can')\n", "c01", "TIN_DUNG_GIA"),
     ("chi_them_chu_thich", 'THU_MUC = "ops/land"\n', 'THU_MUC = "ops/land"  # vo hai\n', "c01", "SONG_SOT"),
 )
````

Lệnh:

````bash
python - <<'PY'
import hashlib, re, subprocess
from pathlib import Path
B = "e139e55883d90fd74a358230be5599c9e223d4b3"
M = "09db70350414d767b793a71cb630e643f216a1b1"
H = "bbfb96cbe6b30e0b5b1b30982eae2b5893ac2c00"
target = ".claude/dev/ci_dang_ky_test.py"
def git(*a):
    return subprocess.check_output(["git", "-C", "cay-kho", *a])
needles = {}
for label, rev in (("master", M), ("reviewed", H)):
    data = git("show", rev + ":" + target)
    oid = git("rev-parse", rev + ":" + target).strip()
    digest = hashlib.sha256(data).hexdigest().encode()
    for kind, value in (("blob", oid), ("sha256", digest)):
        needles[label + "_" + kind] = value
        needles[label + "_" + kind + "_prefix"] = value[:7 if kind == "blob" else 12]
        print(label + "_" + kind + "=" + value.decode())
changed = git("diff", "--name-only", "-z", "--diff-filter=ACMRT", B, M).decode().rstrip("\0").split("\0")
full_tree = git("ls-tree", "-r", "--name-only", "-z", H).decode().rstrip("\0").split("\0")
all_digest_hits = []
for scope, names in (("master_new_or_changed", changed), ("reviewed_full_tree", full_tree)):
    hits = []
    for name in names:
        data = Path("cay-kho", name).read_bytes()
        for label, needle in needles.items():
            if needle in data:
                for i, line in enumerate(data.splitlines(), 1):
                    if needle in line:
                        hits.append((name, i, label))
    print(f"{scope}: scanned_files={len(names)}; full_or_prefix_digest_hits={len(hits)}")
    for hit in hits:
        print("digest_hit=" + repr(hit))
    all_digest_hits.extend(hits)
refs = []
for name in changed:
    data = Path("cay-kho", name).read_text(encoding="utf-8", errors="replace")
    for i, line in enumerate(data.splitlines(), 1):
        for match in re.finditer("ci_dang_ky_test", line):
            snippet = line[max(0, match.start()-100):match.end()+160]
            refs.append((name, i, snippet))
print(f"master_new_or_changed_filename_reference_occurrences={len(refs)}")
for name, line, snippet in refs:
    print(f"{name}:{line}: [context around occurrence] {snippet}")
out = Path("/tmp/wp923-r2-independent/n3-master-references.json")
out.write_text(__import__("json").dumps(refs, ensure_ascii=False, indent=2))
print("master_reference_scan_saved=" + str(out))
manifest = Path("cay-kho/RELEASE_MANIFEST.json").read_bytes()
print(f"release_manifest_mentions_target={b'ci_dang_ky_test' in manifest}")
print(f"release_manifest_mentions_dot_claude={b'.claude/' in manifest}")
assert not all_digest_hits
print("no_literal_blob_sha256_pin_in_master_delta_or_reviewed_tree=PASS")
PY
````

Output thật (exit code 0):

````text
master_blob=a6dc4081f9aadc46a543b6c3e3f0f85a7b113685
master_sha256=9ff2b624c8dd00cc1ed874a91bba77af9d1c2dd81ed3884f47735f1e76dbd56c
reviewed_blob=813668f08437e3930e92cb96c6032452b6f043f4
reviewed_sha256=fa188c1efe944fae03f3d310180fff1a3afd17b38b86adbca04b8f630bccfe0c
master_new_or_changed: scanned_files=59; full_or_prefix_digest_hits=0
reviewed_full_tree: scanned_files=7259; full_or_prefix_digest_hits=0
master_new_or_changed_filename_reference_occurrences=24
.claude/skills/cross-review/SKILL.md:771: [context around occurrence] "$PY" -B -c 'import pathlib,runpy,sys; m=runpy.run_path(str(pathlib.Path(sys.argv[1])/".claude/dev/ci_dang_ky_test.py")); errors,count=m["loi_ruff_ci"](); print("RUFF_CONTRACT",count,errors); sys.exit(bool(errors) or count == 0)' "$SOURCE"
ops/land/pr945-wp899-land-evidence.yaml:19: [context around occurrence] pham_vi_land_ghi_chu: 'ops/ci_provenance.py, ops/ci_provenance_test.py, .claude/dev/ci_dang_ky_test.py — dev-side, khong vao goi phat hanh.'
ops/land/pr945-wp899-land-evidence.yaml:67: [context around occurrence]       set chi .claude/dev/ci_dang_ky_test.py doi +3 dong (2 dong MOI cua #763 vao qua merge master, 1 dong MOI cua
ops/land/pr945-wp899-land-evidence.yaml:95: [context around occurrence]     .claude/dev/ci_dang_ky_test.py NGUOI_GIU 0. Readback cua phep do ay KHONG luu trong provenance.
ops/land/pr945-wp899-land-evidence.yaml:193: [context around occurrence]       hai SHA chi 3 dong MOI tren .claude/dev/ci_dang_ky_test.py.
ops/land/pr945-wp899-provenance/do-1026-cebb5b2/diff-1f731c7-4511b1e-write-set.patch:1: [context around occurrence] diff --git a/.claude/dev/ci_dang_ky_test.py b/.claude/dev/ci_dang_ky_test.py
ops/land/pr945-wp899-provenance/do-1026-cebb5b2/diff-1f731c7-4511b1e-write-set.patch:1: [context around occurrence] diff --git a/.claude/dev/ci_dang_ky_test.py b/.claude/dev/ci_dang_ky_test.py
ops/land/pr945-wp899-provenance/do-1026-cebb5b2/diff-1f731c7-4511b1e-write-set.patch:3: [context around occurrence] --- a/.claude/dev/ci_dang_ky_test.py
ops/land/pr945-wp899-provenance/do-1026-cebb5b2/diff-1f731c7-4511b1e-write-set.patch:4: [context around occurrence] +++ b/.claude/dev/ci_dang_ky_test.py
ops/land/pr945-wp899-provenance/readback-comments-945.json:1: [context around occurrence]  Delta sau lượt ấy chỉ gồm hai phần: bản merge `origin/master` và một dòng `MOI` trong `.claude/dev/ci_dang_ky_test.py`.\n\n---\n_Generated by [Claude Code](https://claude.ai/code)_","author_association":"OWNER","reactions":{"url":"https://api.github.com/repos/ducthangho/tra
ops/land/pr945-wp899-provenance/readback-commit-cebb5b2.json:1: [context around occurrence] 5,"deletions":0},"files":[{"sha":"a76e842cfdf7b6f1f82fe10bdb229b8f83dbb193","filename":".claude/dev/ci_dang_ky_test.py","status":"modified","additions":1,"deletions":0,"changes":1,"blob_url":"https://github.com/ducthangho/tra-luat/blob/cebb5b22e1ebf369a70234662b7e9355bdd5095
ops/land/pr945-wp899-provenance/readback-commit-cebb5b2.json:1: [context around occurrence] ttps://github.com/ducthangho/tra-luat/blob/cebb5b22e1ebf369a70234662b7e9355bdd5095e/.claude%2Fdev%2Fci_dang_ky_test.py","raw_url":"https://github.com/ducthangho/tra-luat/raw/cebb5b22e1ebf369a70234662b7e9355bdd5095e/.claude%2Fdev%2Fci_dang_ky_test.py","contents_url":"https://
ops/land/pr945-wp899-provenance/readback-commit-cebb5b2.json:1: [context around occurrence] https://github.com/ducthangho/tra-luat/raw/cebb5b22e1ebf369a70234662b7e9355bdd5095e/.claude%2Fdev%2Fci_dang_ky_test.py","contents_url":"https://api.github.com/repos/ducthangho/tra-luat/contents/.claude%2Fdev%2Fci_dang_ky_test.py?ref=cebb5b22e1ebf369a70234662b7e9355bdd5095e",
ops/land/pr945-wp899-provenance/readback-commit-cebb5b2.json:1: [context around occurrence] _test.py","contents_url":"https://api.github.com/repos/ducthangho/tra-luat/contents/.claude%2Fdev%2Fci_dang_ky_test.py?ref=cebb5b22e1ebf369a70234662b7e9355bdd5095e","patch":"@@ -54,6 +54,7 @@\n     \"ops/kiem_ho_so_land_test.py\": r\"^(\\d+)/(\\d+)$\",\n     \"ops/kiem_nhan_
ops/land/pr945-wp899-provenance/readback-commit-cebb5b2.json:1: [context around occurrence] shreplace\")\n+\n+ROOT = Path(__file__).resolve().parent.parent\n+CI_DANG_KY = ROOT / \".claude/dev/ci_dang_ky_test.py\"\n+API = \"https://api.github.com\"\n+TRANG = 100\n+TRANG_TOI_DA = 1000\n+TS = r\"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\\.[0-9]+)?Z\"   
ops/land/pr945-wp899-provenance/readback-pr-945.json:1: [context around occurrence] 2f725211b62f5` |\n| write set | `ops/ci_provenance.py` · `ops/ci_provenance_test.py` · `.claude/dev/ci_dang_ky_test.py` |\n| trần | ≤ 3 tệp / ≤ 2050 dòng thêm. So `master`: 1 + 444 + 1600 = **2045** |\n| ngân sách Codex | used 11 · limit 12. Lượt connector trên PR này là lời
ops/land/pr945-wp899-provenance/readback-pr-945.json:1: [context around occurrence] ung đột. Hai tệp `ops/ci_provenance*.py` giữ nguyên byte-for-byte như lúc approve. Tệp `.claude/dev/ci_dang_ky_test.py` nhận +2 dòng `MOI` của #763 từ master.\n2. `4511b1e`: thêm lại **đúng một dòng `MOI`** cho `ops/ci_provenance_test.py`.\n\n## Gate trên head `4511b1e`\n\n|
ops/land/pr945-wp899-provenance/readback-pr-945.json:1: [context around occurrence] et dung ly do` · `TU KIEM PHAN HANG: DAT (2 dot bien)` · `TONG: DAT`, rc 0 |\n| `python .claude/dev/ci_dang_ky_test.py` | `PHẢN CHỨNG: 1070/1070 đỏ đúng` · `TỔNG: ĐẠT`, rc 0. Regex `MOI` mới khớp output thật của bộ ca |\n| tập đột biến đóng `--dot-bien-dong`, đo trên `1f731c
ops/land/pr945-wp899-provenance/readback-run-40264014854.json:1: [context around occurrence] ee5d3","message":"wp899 r4 g5 (#899): dang ky lai ops/ci_provenance_test.py vao MOI cua .claude/dev/ci_dang_ky_test.py\n\nWrite set g5 co lai tep nay (#763 da merge qua PR #930, lease wp763-r2-g1-claude rut han 01:35Z).\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.c
ops/land/pr945-wp899-provenance/review-a-4511b1e/VERDICT.md:26: [context around occurrence]  `f9f4a8d6da2d351fbcf5203256aba4e1bbf027b7..4511b1eb6168904da117791cea178aa0c80e0e47`: `.claude/dev/ci_dang_ky_test.py` +1, `ops/ci_provenance.py` +444, `ops/ci_provenance_test.py` +1600; tổng **3 tệp, +2045/-0**. Dòng MOI mới đúng một mục, cùng mẫu với land_evidence_nguon_t
ops/land/pr945-wp899-provenance/review-a-4511b1e/VERDICT.md:81: [context around occurrence] | `python -B .claude/dev/ci_dang_ky_test.py` | **1** | Lệnh **failed** vì fixture ký commit cần local signing service, socket operation not permitted. Trước lỗi có 27/27 đăng ký, launcher 4/4, Ruff CI
ops/land/pr945-wp899-provenance/review-a-4511b1e/VERDICT.md:83: [context around occurrence] | `ci_dang_ky_test.py --chay` (A9 đầy đủ); full release/legacy gate | — | **not_run**: preflight fixture registry chưa đủ năng lực ký commit. Không tắt signing, đổi quyền/trust h
ops/land/pr945-wp899-provenance/review-a-4511b1e/prompt.md:15: [context around occurrence] | write set | `ops/ci_provenance.py` · `ops/ci_provenance_test.py` · `.claude/dev/ci_dang_ky_test.py` |
ops/land_evidence_nguon.py:39: [context around occurrence] Không sửa hồ sơ nào. Lên CI GIÁN TIẾP: `ops/land_evidence_nguon_test.py` đăng ký trong `.claude/dev/ci_dang_ky_test.py`, ca `c11`
master_reference_scan_saved=/tmp/wp923-r2-independent/n3-master-references.json
release_manifest_mentions_target=False
release_manifest_mentions_dot_claude=False
no_literal_blob_sha256_pin_in_master_delta_or_reviewed_tree=PASS
````

Lệnh:

````bash
sed -n '1,95p' cay-kho/ops/ci_provenance.py; rg -n 'CI_DANG_KY|read_bytes|sha256' cay-kho/ops/ci_provenance.py; sed -n '2580,2602p' cay-kho/ops/ci_duong_nhanh_test.py; sed -n '248,266p' cay-kho/.claude/dev/doc_receipt_thu_hoi_test.py
````

Output thật (exit code 0):

````text
#!/usr/bin/env python3
"""Thu provenance CI §10.2.2 từ REST và log job — packet #899 (wp899 P-A), đặc tả `ops/specs/wp899-r4.md` (thay r3).

`thu --repo o/r --run ID --attempt N --out DIR` ghi bốn mốc TÁCH BẠCH (Run · Checkout · Gate output · Workflow definition)
vào `DIR/provenance.yaml`. Chỉ REST; mọi lời gọi mạng đi qua MỘT hàm tiêm vào `goi(url) -> (mã HTTP, byte)` để test chạy
offline. Năm trạng thái §10.2.3: thiếu dữ liệu là `not_measured`, không bao giờ là `passed`. Mốc Workflow definition luôn
`not_measured` (GraphQL bị chặn trong phiên Claude; việc của P-B). SHA checkout đọc từ LOG, không lấy `head_sha` của REST.
r3 (F02): kịch bản của bước lấy từ `run:` của workflow tại SHA checkout ĐÃ ĐO (`git cat-file blob <sha>:<path REST>`). r4 (F02):
bước của mỗi nhóm log được ĐỊNH DANH qua REST `steps[]` + vị trí (`ghep_buoc`), không tìm ứng viên trùng chữ trên toàn workflow. Gốc tin là nội dung tại SHA ấy — workflow tại SHA vốn quyết định được mọi output, công cụ không chống nó.
Thoát: 0 không mốc nào `failed` · 12 có `failed` · 2 sai đối số · 3 REST khác 2xx (in nguyên mã). LUÔN in `NOT_MEASURED: <n>`;
rc 2/3 không sinh provenance nên cả bốn mốc là chưa đo (`NOT_MEASURED: 4` kèm `PROVENANCE: khong_sinh`).
"""
import argparse, datetime, hashlib, importlib.util, json, os, re, shutil, subprocess, sys, tempfile, urllib.error, urllib.request
from pathlib import Path

import yaml

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="backslashreplace")

ROOT = Path(__file__).resolve().parent.parent
CI_DANG_KY = ROOT / ".claude/dev/ci_dang_ky_test.py"
API = "https://api.github.com"
TRANG = 100
TRANG_TOI_DA = 1000
TS = r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]+)?Z"   # ASCII: `\d` khớp cả chữ số Unicode
RE_DONG = re.compile(rf"^({TS}) ?(.*)$")
RE_SHA = re.compile(rf"^{TS} ([0-9a-f]{{40}})$")
RE_GIO = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z")
RE_ANSI = re.compile(r"\x1b\[[0-9;]*m")
RE_HEX40 = re.compile(r"^[0-9a-f]{40}$")
RE_REPO = re.compile(r"^[\w.-]+/[\w.-]+$")
LY_DO_WD = "graphql_bi_chan_trong_phien_claude; cho P-B"
KET_BUOC = ("success", "failure", "cancelled", "skipped", "neutral")
LOI_JOB = ("failure", "cancelled", "timed_out", "action_required", "startup_failure", "stale")
RE_CHECK_RUN = re.compile(r"^https://api\.github\.com/repos/[\w.-]+/[\w.-]+/check-runs/[1-9]\d*$")
# Lời gọi python DUY NHẤT tính là bằng chứng (danh sách CHO PHÉP): cả dòng logic là `[VAR=… ]python[ver] [cờ không đối số…]
# [./]<script>.py` — KHÔNG đối số sau script (r3 Q4), không nháy/toán tử/chú thích. Nhóm 1 = tiền tố `VAR=` (⇒ chặn chế độ).
RE_LOI_GOI = re.compile(r"^((?:[A-Za-z_]\w*=[\w./:-]*\s+)*)(?:[\w./-]*/)?python(?:\d+(?:\.\d+)*)?(?:\s+-[BuIsSEOqb]+)*"
                        r"\s+(?:\./)?([\w.-]+(?:/[\w.-]+)*\.py)$")
KHOA_BUOC = {"name", "id", "if", "run", "shell", "timeout-minutes", "continue-on-error"}   # CHO PHÉP; env/working-directory… ⇒ chặn

def _so(v, nho=0):
    return type(v) is int and v >= nho   # `bool` là con của `int`: `type(...) is int` loại True/False

def _chuoi(v):
    return type(v) is str and v.strip() != ""

RUN_BAT_BUOC = {"id": lambda v: _so(v, 1), "run_attempt": lambda v: _so(v, 1), "event": _chuoi, "path": _chuoi,
                "head_sha": lambda v: _chuoi(v) and bool(RE_HEX40.fullmatch(v)), "check_suite_id": lambda v: _so(v, 1)}
JOB_BAT_BUOC = {"name": _chuoi, "runner_id": lambda v: _so(v, 1), "runner_name": _chuoi, "conclusion": lambda v: v == "success",
                "labels": lambda v: type(v) is list and bool(v) and all(_chuoi(x) for x in v),
                "check_run_url": lambda v: _chuoi(v) and bool(RE_CHECK_RUN.fullmatch(v)), "steps": lambda v: type(v) is list and bool(v)
                and all(type(b) is dict and _chuoi(b.get("name")) and b.get("conclusion") in KET_BUOC for b in v)}
ART_BAT_BUOC = {"name": _chuoi, "size_in_bytes": _so, "expired": lambda v: type(v) is bool,
                "digest": lambda v: v is None or (_chuoi(v) and v.startswith("sha256:"))}
KHONG_SINH = "NOT_MEASURED: 4\nPROVENANCE: khong_sinh (ca bon moc chua do)"

class LoiRest(Exception):
    def __init__(self, ma, url):
        super().__init__(f"REST {ma} {url}")
        self.ma, self.url = ma, url

class _KhongChuyenHuong(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None

def goi_that(url):
    """GET REST. Log job trả 302 sang kho blob: theo TAY và KHÔNG mang token sang host khác."""
    tk = next((os.environ[k] for k in ("GITHUB_PAT", "GH_TOKEN", "GITHUB_TOKEN") if os.environ.get(k)), None)
    hd = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    if tk:
        hd["Authorization"] = f"Bearer {tk}"
    yeu_cau, mo = urllib.request.Request(url, headers=hd), urllib.request.build_opener(_KhongChuyenHuong).open
    for _ in range(2):   # lượt 2 (nếu có) là URL chuyển hướng: cùng hợp đồng lỗi, chuỗi trần nên không có header token
        try:
            with mo(yeu_cau, timeout=120) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            loc = e.headers.get("Location") if e.code in (301, 302, 303, 307, 308) else None
            if not loc or mo is urllib.request.urlopen:
                return e.code, b""
            yeu_cau, mo = loc, urllib.request.urlopen
        except (urllib.error.URLError, OSError) as e:
            raise LoiRest(f"khong_ket_noi ({e})", url)

def lay(goi, url):
    ma, byte = goi(url)
    if not (isinstance(ma, int) and 200 <= ma < 300):
        raise LoiRest(ma, url)
    return byte

def lay_json(goi, url):
    """(đối tượng, byte nguyên văn)."""
23:CI_DANG_KY = ROOT / ".claude/dev/ci_dang_ky_test.py"
57:                "digest": lambda v: v is None or (_chuoi(v) and v.startswith("sha256:"))}
128:def doc_moi(duong=CI_DANG_KY):
153:def _env_chan(d):   # CÓ khoá `env:` mà giá trị không phải dict (biểu thức, null — D01) hoặc có khoá `CI_DANG_KY_*` ⇒ không biết chế độ
154:    return "env" in d and (type(d["env"]) is not dict or any(str(k).startswith("CI_DANG_KY_") for k in d["env"]))
331:def thu(repo, run, attempt, goi, git, moi_tu=CI_DANG_KY, wf=git_blob):
363:        log[j["id"]] = {"sha256": hashlib.sha256(byte).hexdigest(), "bytes": len(byte), "trich": f"jobs/{j['id']}.trich.txt"}
402:def main(argv=None, goi=goi_that, git=git_cuc_bo, moi_tu=CI_DANG_KY, wf=git_blob):
439:    print(f"provenance.yaml sha256 {hashlib.sha256(tep['provenance.yaml']).hexdigest()}")
    return runpy.run_path(str(CAY / ".claude" / "dev" / "ci_dang_ky_test.py"))


@ca
def k01_so_dang_ky_nhan_muc_da_noi():
    m = nap_so_dang_ky()
    bang(DA_NOI_MUC in m["DANG_KY"], f"ci_dang_ky_test.DA_NOI phai co {DA_NOI_MUC!r}")
    loi, song, dang_ky = m["kiem"]()
    bang(not loi, f"so dang ky phai sach, duoc {loi}")
    bang(song == dang_ky and song > 0, f"so test song ({song}) phai BANG so dang ky ({dang_ky}) va > 0")


@ca
def k02_da_noi_dung_mot_lan_va_test_song_khop_tep():
    m = nap_so_dang_ky()
    song, _, _ = m["tim"](CAY)
    bang(DA_NOI_MUC in song, f"tep {DA_NOI_MUC} phai ton tai o muc dinh ops/ (vi tri chuan cua test song)")
    src = (CAY / ".claude" / "dev" / "ci_dang_ky_test.py").read_text(encoding="utf-8")
    bang(src.count(f'"{DA_NOI_MUC}"') == 1, f"muc {DA_NOI_MUC!r} phai xuat hien dung mot lan trong ci_dang_ky_test.py")


@ca
def k03_ci_goi_that_muc_da_noi():
            or any(type(e) is not str for e in kq["ev"]) or {type(kq["trang_thai"]), type(kq["tat_dinh"])} != {bool}):  # luot5 F36
        raise LoiDo(f"{ten}: probe tinh thuan hong rc={r.returncode}: {r.stderr[-200:]}")  # KHÔNG phải bằng chứng tác dụng phụ (luot4 F32)
    if kq != {"ev": [], "trang_thai": True, "tat_dinh": True}:
        raise TinHieuChotCa(f"{ten}: kiem_json co tac dung phu: {kq}")


MAU = r'^doc_receipt_thu_hoi tests: ([1-9]\d*)/(\1) ca QUA · ([1-9]\d*)/(\3) dot bien GIET$'


def ca_dang_ky(ten, mau=MAU):
    cdk = _nap(GOC / "ci_dang_ky_test.py", "ci_dang_ky_duoi_test")
    if cdk.MOI.get(".claude/dev/doc_receipt_thu_hoi_test.py") != MAU:
        raise TinHieuChotCa(f"{ten}: MOI khong dang ky dung MAU (M8)")
    for a, b, nhan in (("3/3", "2/2", True), ("3/4", "2/2", False), ("3/3", "1/2", False), ("3/4", "1/2", False),
                       ("0/0", "0/0", False), ("3/3", "0/0", False)):
        if bool(cdk.bang_chung_xanh(f"doc_receipt_thu_hoi tests: {a} ca QUA · {b} dot bien GIET", mau)) != nhan:
            raise TinHieuChotCa(f"{ten}: mau dang ky {a} · {b} phai {'nhan' if nhan else 'bac'}")
````

Lệnh:

````bash
git -C cay-kho diff --unified=3 e139e55883d90fd74a358230be5599c9e223d4b3 09db70350414d767b793a71cb630e643f216a1b1 -- .claude/skills/cross-review/SKILL.md .claude/skills/land-packets/SKILL.md
````

Output thật (exit code 0):

````text
diff --git a/.claude/skills/cross-review/SKILL.md b/.claude/skills/cross-review/SKILL.md
index b0fe009..cbc4102 100644
--- a/.claude/skills/cross-review/SKILL.md
+++ b/.claude/skills/cross-review/SKILL.md
@@ -748,6 +748,10 @@ query($id: ID!) {
 gh api graphql -F query=@"$SCRATCH/query.graphql" -f id="$RUN_NODE_ID" > "$SCRATCH/workflow-run.json"
 ```
 
+Mẫu trên chạy trong phiên có GraphQL. Phiên Claude Code trên web bị 403 nên phải nhờ chủ kho chạy; lệnh đưa
+cho chủ kho theo mục *"Lệnh `gh api graphql` đưa cho chủ kho chạy"* của `CLAUDE.md` (máy chủ kho là `cmd`, mẫu
+trên vỡ ở đó). Đọc mục ấy từ `origin/master` ngay trước khi soạn lệnh — phiên mở từ trước có thể đang giữ bản cũ.
+
 `WorkflowRun.file` nullable; cấu trúc tham chiếu ở [GitHub Actions GraphQL](https://docs.github.com/en/graphql/reference/actions).
 Phân loại missing/errors và kiểm OID của URL theo §10.2.2. Khi đã xác minh repo/path/OID,
 dùng `git -C "$SOURCE" cat-file blob "$DEFINITION_OID:$WORKFLOW_PATH"` lấy bytes và SHA-256 bằng Python;
diff --git a/.claude/skills/land-packets/SKILL.md b/.claude/skills/land-packets/SKILL.md
index d5293bd..d7c231c 100644
--- a/.claude/skills/land-packets/SKILL.md
+++ b/.claude/skills/land-packets/SKILL.md
@@ -54,6 +54,12 @@ PY="$(command -v python3 || command -v python || command -v py)"   # CLAUDE.md:
 Lệnh này không có cờ nới, và không được thêm. Uỷ quyền cho một exact head SHA sống trên GitHub, không
 sống trong ngữ cảnh phiên — đọc §13 để biết cái gì được coi là uỷ quyền hợp lệ.
 
+## Mốc Workflow definition khi phiên không gọi được GraphQL
+
+Phiên Claude Code trên web nhận 403 cho GraphQL, nên `WorkflowRun.file` phải do chủ kho chạy rồi dán output.
+Cú pháp lệnh đưa cho chủ kho và cách đối chiếu: mục *"Lệnh `gh api graphql` đưa cho chủ kho chạy"* của `CLAUDE.md`.
+Đọc mục ấy từ `origin/master` ngay trước khi soạn lệnh — phiên mở từ trước có thể đang giữ bản cũ.
+
 ## Full ref fence và merge evidence
 
 Protocol §5.1/§13.1 quy định phạm vi so sánh. `$SCRATCH` là thư mục ngoài checkout;
````

Lệnh:

````bash
sed -n '124,151p' cay-kho/ops/ci_provenance.py; cat cay-kho/ops/land/pr945-wp899-provenance/do-1026-cebb5b2/diff-1f731c7-4511b1e-write-set.patch; rg -n 'ci_dang_ky|readback-commit|diff-1f731' cay-kho/ops/land/pr945-wp899-provenance/SHA256SUMS.txt
````

Output thật (exit code 0):

````text
    sai = sorted({k for x in d[khoa] for k, hop_le in (bat_buoc or {}).items() if not hop_le(x.get(k))})
    return {"trang_thai": "passed" if d["du"] and not sai else "not_measured", "total_count": d["total_count"],
            "so_id": len(d[khoa]), "truong_sai": sai}

def doc_moi(duong=CI_DANG_KY):
    """`MOI` và `bang_chung_xanh` đọc bằng IMPORT sổ đăng ký — một nguồn, không chép bảng."""
    spec = importlib.util.spec_from_file_location("ci_dang_ky_cho_provenance", duong)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return dict(m.MOI), m.bang_chung_xanh

def git_cuc_bo(sha, goc=ROOT):
    """parents/tree của commit trong kho cục bộ; không có object (hoặc không phải commit) ⇒ None."""
    try:
        r = subprocess.run(["git", "-C", str(goc), "cat-file", "-p", sha], capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return None
    dau = r.stdout.split("\n\n", 1)[0].splitlines() if r.returncode == 0 else []
    tree = [x[5:] for x in dau if x.startswith("tree ")]
    return {"tree": tree[0], "parents": [x[7:] for x in dau if x.startswith("parent ")]} if len(tree) == 1 else None

def git_blob(sha, path, goc=ROOT):
    """Văn bản blob `<sha>:<path>` trong kho cục bộ; thiếu object/tệp, không phải blob hay không UTF-8 ⇒ None."""
    try:
        r = subprocess.run(["git", "-C", str(goc), "cat-file", "blob", f"{sha}:{path}"], capture_output=True, timeout=60)
        return r.stdout.decode("utf-8") if r.returncode == 0 else None
    except (OSError, subprocess.SubprocessError, UnicodeDecodeError):
        return None
diff --git a/.claude/dev/ci_dang_ky_test.py b/.claude/dev/ci_dang_ky_test.py
index b25b0ab..a76e842 100644
--- a/.claude/dev/ci_dang_ky_test.py
+++ b/.claude/dev/ci_dang_ky_test.py
@@ -51,7 +51,10 @@ MOI = {
     ".claude/hooks/pretooluse_guard_test.py": r"(?s)TONG: CA (\d+)/(\d+) dat · DOT BIEN \d+/\d+ bi giet.*TONG: DAT",
     ".claude/hooks/subagent_ghi_detect_test.py": r"(?s)TONG: CA (\d+)/(\d+) dat · DOT BIEN \d+/\d+ bi giet.*TONG: DAT",
     "ops/nhanh_don_duoc_test.py": r"^(\d+)/(\d+)$",
+    "ops/kiem_ho_so_land_test.py": r"^(\d+)/(\d+)$",
+    "ops/kiem_nhan_hint_test.py": r"^(\d+)/(\d+)$",
     "ops/land_evidence_nguon_test.py": r"(?ms)\A(?!.*^(?:TONG|TU KIEM PHAN HANG): DO\b).*^CA: ([1-9]\d*)/(\1) dat\nDOT BIEN: ([1-9]\d*)/\3 bi giet dung ly do\nTU KIEM PHAN HANG: DAT \(\d+ dot bien\)\nTONG: DAT\n?\Z",
+    "ops/ci_provenance_test.py": r"(?ms)\A(?!.*^(?:TONG|TU KIEM PHAN HANG): DO\b).*^CA: ([1-9]\d*)/(\1) dat\nDOT BIEN: ([1-9]\d*)/\3 bi giet dung ly do\nTU KIEM PHAN HANG: DAT \(\d+ dot bien\)\nTONG: DAT\n?\Z",
 }
 # Tap mau THAY THE, chi dung khi nen dang chay la Windows. Windows nhan HAI dang:
 #   (a) dong da cat dot bien;  (b) dong Linux day du — ai do chay tay do du van DAT (A3).
5:e824cd5b515052944226709478540b74326a4b5b2891883211d8e9c96e6ffd09  ./do-1026-cebb5b2/diff-1f731c7-4511b1e-write-set.patch
19:5a5142d4ed6b9055ffc4e3748253fdc05be792383b259fe5405c76e7119ac891  ./readback-commit-cebb5b2.json
````

Kết luận: KHÔNG PHẢI LỖI trong phạm vi quét — 59 tệp master mới/đổi và 7259 tệp tracked của head không có OID/SHA-256 master hoặc reviewed (cả đầy đủ lẫn tiền tố 7/12 ký tự). 24 lần nhắc tên ở phần master là hướng dẫn runpy và provenance/ghi chú lịch sử; metadata a76e842 trong readback-commit-cebb5b2.json là blob lịch sử, không chốt byte hiện hành. SHA256SUMS băm artifact provenance, không băm tệp nguồn. Đã đọc diff mã master, consumer AST/import/runpy và phép đếm DA_NOI; không thấy chốt nguyên byte sống mới. Lần quét toàn cây ban đầu lỗi tên Unicode được Git quote; đã sửa phép đo dùng -z và chạy lại đủ, không sửa kho.

### HƯỚNG 7: Commit message không bỏ CI; timeout chú thích còn đúng

Giả thuyết: Merge message có thể vô tình bỏ CI, hoặc job mảnh/gom sau merge không còn đúng các mốc 150/150/10.

Lệnh:

````bash
git -C cay-kho log -1 --format=%B
````

Output thật (exit code 0):

````text
Merge origin/master vao agent/wp923-g2-claude (#923, quyet dinh chu kho issuecomment-6440352875)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_015GtxrZWhXPHPfAPL1BXfPB
````

Lệnh:

````bash
python - <<'PY'
import re, subprocess
message = subprocess.check_output(["git", "-C", "cay-kho", "log", "-1", "--format=%B"]).decode()
markers = ("[skip ci]", "[ci skip]", "[no ci]", "[skip actions]", "[actions skip]")
hits = [m for m in markers if m in message.lower()]
trailers = re.findall(r"(?im)^\s*skip-checks\s*:\s*true\s*$", message)
print("bracket_skip_marker_hits=" + repr(hits))
print("skip_checks_true_trailer_hits=" + repr(trailers))
print("message_utf8_bytes=" + str(len(message.encode())))
assert not hits and not trailers
print("merge_message_has_no_literal_ci_skip_directive=PASS")
PY
````

Output thật (exit code 0):

````text
bracket_skip_marker_hits=[]
skip_checks_true_trailer_hits=[]
message_utf8_bytes=227
merge_message_has_no_literal_ci_skip_directive=PASS
````

Lệnh:

````bash
python - <<'PY'
import ast, subprocess, yaml
from pathlib import Path
path = Path("cay-kho/.claude/dev/ci_dang_ky_test.py")
wf = yaml.safe_load(Path("cay-kho/.github/workflows/ci.yml").read_text())
for job in ("gate-registry", "gate-nhanh-manh", "gate-nhanh-gop"):
    j = wf["jobs"][job]
    print(f"{job}: timeout-minutes={j['timeout-minutes']}; needs={j.get('needs')!r}")
assert [wf["jobs"][j]["timeout-minutes"] for j in ("gate-registry", "gate-nhanh-manh", "gate-nhanh-gop")] == [150, 150, 10]
source = path.read_text()
print("relevant_comments:")
for i, line in enumerate(source.splitlines(), 1):
    if line.lstrip().startswith("#") and (756 <= i <= 768 or 807 <= i <= 811):
        print(f"{i}: {line}")
main = ast.parse(source)
selected = {}
for n in main.body:
    if isinstance(n, ast.Assign):
        for target in n.targets:
            if isinstance(target, ast.Name) and target.id in ("GIAY_TOI_DA_MOT_BO", "BAM_GATE_REGISTRY", "BAM_GATE_NHANH"):
                selected[target.id] = ast.literal_eval(n.value)
print("unchanged_relevant_constants=" + repr(selected))
print("timeout_comment_values_still_match_master_jobs=PASS")
PY
````

Output thật (exit code 0):

````text
gate-registry: timeout-minutes=150; needs=['chuan-bi', 'gate-nhanh-gop']
gate-nhanh-manh: timeout-minutes=150; needs='chuan-bi'
gate-nhanh-gop: timeout-minutes=10; needs=['chuan-bi', 'gate-nhanh-manh']
relevant_comments:
757: # CI-SONG-SONG-REGISTRY-G5-MOT-LAN r1 (#637): M1–M3, M6, M7. Hằng số trong W1 theo spec M3.
758: # #643 (chủ kho chọn "b", PR #644): 3600 → 4500. Đo run 36208617323, N=2 chế độ đủ: `nhanh_don_duoc_test` 3306,45 s = 92 %
759: # trần cũ. KHÔNG bảo đảm cả job dưới `timeout-minutes` (#705: 105 · #910 pha B, a7da463: 150): bộ ấy còn chờ worker trống (run trên: bắt đầu sau 337 s),
760: # Windows ép N=1 ⇒ dài hơn; trần job là trần NGOÀI. Ca `p643-tran-bo-nho-hon-timeout-job` chỉ khoá trần bộ < trần job.
761: # #705 (CI-REGISTRY-NANG-TRAN-BO-DAY-DU, chủ kho Q4): 4500 → 5400, job 90 → 105 phút. `nhanh_don_duoc_test` chế độ đủ:
762: # 3645 s xanh (run 36642392330) rồi > 4500 s ĐỎ ba lần (36696528580 ×2, 36839918701) — runner chậm 22–42 % (hai bộ vô can
763: # cùng lượt: `pretooluse_guard_test` 914 → 1213–1300 s, `subagent_ghi_detect_test` 316 → 386–400 s), KHÔNG phải bộ chậm đi
764: # (delta tại chỗ 7b308bc 4604 s / 423b4ba 4586 s). 3645 × 1,42 ≈ 5180 ⇒ 5400 chỉ dư ~4 % — MỎNG; giải pháp bền là chia mảnh.
808: # WP748 r16: hai job nay la `targeted_mutant_gate` (NHANH_DON_DUOC_DICH, gom `--gop-dich`, tran 30 phut).
809: # #910 pha B (PR #917, a7da463): tran job manh 30 -> 150; job gom van 10.
unchanged_relevant_constants={'BAM_GATE_REGISTRY': '89516cf77c3ce734feadf348bfea8180254c67e8e8ec62a48e2f6ea1dc038452', 'BAM_GATE_NHANH': 'fe061a50668af83b6c9b6939f881ba37a30083bc72a27b52c2e02350835d626b'}
timeout_comment_values_still_match_master_jobs=PASS
````

Kết luận: KHÔNG PHẢI LỖI — không có 5 dấu skip CI dạng ngoặc hoặc trailer skip-checks:true; job registry/mảnh/gom vẫn lần lượt 150/150/10 phút. Mốc lịch sử #705 và các hằng số được bảo toàn.

### HƯỚNG 8: N2: chạy thật registry tại reviewed_sha, đối chiếu log từng byte

Giả thuyết: Head merge có thể làm đăng ký hoặc phản chứng hỏng dù tệp được sửa giữ nguyên byte.

Lệnh:

````bash
git -C cay-kho config --show-origin --get-regexp '^(commit\.gpgsign|gpg\.format|core\.abbrev)$'
````

Output thật (exit code 0):

````text
file:/root/.gitconfig	gpg.format ssh
file:/root/.gitconfig	commit.gpgsign true
file:.git/config	core.abbrev 7
````

Lệnh:

````bash
python - <<'PY'
import hashlib, os, re, shlex, subprocess, sys
from pathlib import Path
repo = Path("cay-kho").resolve()
scratch = Path("/tmp/wp923-r2-independent")
tmp = scratch / "test-tmp"
tmp.mkdir(exist_ok=True)
log = scratch / "n2-reviewed-merge.log"
trace = scratch / "n2-network-block.trace"
overrides = dict(GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_COUNT="2",
                 GIT_CONFIG_KEY_0="commit.gpgsign", GIT_CONFIG_VALUE_0="false",
                 GIT_CONFIG_KEY_1="core.abbrev", GIT_CONFIG_VALUE_1="7",
                 GIT_OPTIONAL_LOCKS="0", PYTHONDONTWRITEBYTECODE="1", TMPDIR=str(tmp),
                 TL_SELFTEST_ALLOW_NET="0")
env = dict(os.environ, **overrides)
print("process_only_test_overrides=" + repr(overrides))
head = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"]).decode().strip()
print("tested_sha=" + head)
assert head == "bbfb96cbe6b30e0b5b1b30982eae2b5893ac2c00"
cmd = ["strace", "-f", "-qq", "-e", "trace=connect,sendto,sendmsg,sendmmsg",
       "-e", "inject=connect:error=ENETUNREACH", "-e", "inject=sendto:error=ENETUNREACH",
       "-e", "inject=sendmsg:error=ENETUNREACH", "-e", "inject=sendmmsg:error=ENETUNREACH",
       "-o", str(trace), sys.executable, ".claude/dev/ci_dang_ky_test.py"]
print("test_cwd=" + str(repo))
print("actual_test_command=" + shlex.join(cmd), flush=True)
with log.open("wb") as stream:
    cp = subprocess.run(cmd, cwd=repo, env=env, stdout=stream, stderr=subprocess.STDOUT, timeout=180)
data = log.read_bytes()
text = data.decode("utf-8", "backslashreplace")
print(f"test_exit_code={cp.returncode}")
print(f"full_log={log}; bytes={len(data)}; sha256={hashlib.sha256(data).hexdigest()}")
print("positive_evidence:")
for line in text.splitlines():
    if line.startswith(("ĐĂNG KÝ:", "TRẠNG THÁI:", "LAUNCHER WINDOWS:", "RUFF CI:", "PHẢN CHỨNG:", "TỔNG:")):
        print(line)
for name in ("n2_base.log", "n2_merge.log"):
    supplied = Path(name).read_bytes()
    print(f"{name}: bytes={len(supplied)}; sha256={hashlib.sha256(supplied).hexdigest()}; reviewer_log_equals_every_byte={data == supplied}")
calls = [x for x in trace.read_text().splitlines() if re.search(r"\b(connect|sendto|sendmsg|sendmmsg)\(", x)]
print(f"network_syscalls_observed={len(calls)}; injected_block_count={sum('(INJECTED)' in x for x in calls)}")
if cp.returncode:
    print("failure_tail:\n" + "\n".join(text.splitlines()[-35:]))
assert cp.returncode == 0 and "ĐĂNG KÝ: 28/28" in text and "PHẢN CHỨNG: 1070/1070 đỏ đúng" in text and "TỔNG: ĐẠT" in text
assert data == Path("n2_base.log").read_bytes() == Path("n2_merge.log").read_bytes()
assert not calls
print("N2_independent_exact_merge_head=PASS")
PY
````

Output thật (exit code 1):

````text
process_only_test_overrides={'GIT_CONFIG_GLOBAL': '/dev/null', 'GIT_CONFIG_COUNT': '2', 'GIT_CONFIG_KEY_0': 'commit.gpgsign', 'GIT_CONFIG_VALUE_0': 'false', 'GIT_CONFIG_KEY_1': 'core.abbrev', 'GIT_CONFIG_VALUE_1': '7', 'GIT_OPTIONAL_LOCKS': '0', 'PYTHONDONTWRITEBYTECODE': '1', 'TMPDIR': '/tmp/wp923-r2-independent/test-tmp', 'TL_SELFTEST_ALLOW_NET': '0'}
tested_sha=bbfb96cbe6b30e0b5b1b30982eae2b5893ac2c00
test_cwd=/tmp/claude-0/-home-user-tra-luat/6cf1da84-5813-5156-ad6b-b3a2dbd3ab61/scratchpad/rv2/cay-kho
actual_test_command=strace -f -qq -e trace=connect,sendto,sendmsg,sendmmsg -e inject=connect:error=ENETUNREACH -e inject=sendto:error=ENETUNREACH -e inject=sendmsg:error=ENETUNREACH -e inject=sendmmsg:error=ENETUNREACH -o /tmp/wp923-r2-independent/n2-network-block.trace /usr/bin/python .claude/dev/ci_dang_ky_test.py
test_exit_code=1
full_log=/tmp/wp923-r2-independent/n2-reviewed-merge.log; bytes=247; sha256=01c79a7d47475a07737aecab58d739206fd0dcf4a572f2efdab84f037f393c00
positive_evidence:
n2_base.log: bytes=61886; sha256=ef11caf341ed192c60c62430ddb81f53d10b03304fdc871dc29c8ce22b90de88; reviewer_log_equals_every_byte=False
n2_merge.log: bytes=61886; sha256=ef11caf341ed192c60c62430ddb81f53d10b03304fdc871dc29c8ce22b90de88; reviewer_log_equals_every_byte=False
network_syscalls_observed=0; injected_block_count=0
failure_tail:
strace: test_ptrace_get_syscall_info: PTRACE_TRACEME: Operation not permitted
strace: ptrace(PTRACE_TRACEME, ...): Operation not permitted
strace: PTRACE_SETOPTIONS: Operation not permitted
strace: cleanup: waitpid(-1, __WALL): No child processes
Traceback (most recent call last):
  File "<stdin>", line 42, in <module>
AssertionError
````

Lệnh:

````bash
cat /tmp/wp923_network_guard.py
````

Output thật (exit code 0):

````text
import ctypes
import errno
import os
import sys

_lib = ctypes.CDLL("libseccomp.so.2")
_lib.seccomp_init.argtypes = [ctypes.c_uint32]
_lib.seccomp_init.restype = ctypes.c_void_p
_lib.seccomp_syscall_resolve_name.argtypes = [ctypes.c_char_p]
_lib.seccomp_syscall_resolve_name.restype = ctypes.c_int

class _Arg(ctypes.Structure):
    _fields_ = [("arg", ctypes.c_uint), ("op", ctypes.c_uint),
                ("datum_a", ctypes.c_uint64), ("datum_b", ctypes.c_uint64)]

_lib.seccomp_rule_add_array.argtypes = [ctypes.c_void_p, ctypes.c_uint32, ctypes.c_int,
                                       ctypes.c_uint, ctypes.POINTER(_Arg)]
_lib.seccomp_rule_add_array.restype = ctypes.c_int
_lib.seccomp_load.argtypes = [ctypes.c_void_p]
_lib.seccomp_load.restype = ctypes.c_int
_lib.seccomp_release.argtypes = [ctypes.c_void_p]

def network_guard():
    ctx = _lib.seccomp_init(0x7FFF0000)
    if not ctx:
        raise RuntimeError("seccomp_init failed")
    try:
        deny = 0x00050000 | errno.ENETUNREACH
        for name in (b"connect", b"sendto", b"sendmsg", b"sendmmsg"):
            nr = _lib.seccomp_syscall_resolve_name(name)
            rc = _lib.seccomp_rule_add_array(ctx, deny, nr, 0, None)
            if rc != 0:
                raise RuntimeError(f"seccomp rule {name!r}: {rc}")
        nr = _lib.seccomp_syscall_resolve_name(b"socket")
        for family in (2, 10):
            cmp = _Arg(0, 4, family, 0)
            rc = _lib.seccomp_rule_add_array(ctx, deny, nr, 1, ctypes.byref(cmp))
            if rc != 0:
                raise RuntimeError(f"seccomp socket family {family}: {rc}")
        rc = _lib.seccomp_load(ctx)
        if rc != 0:
            raise RuntimeError(f"seccomp_load: {rc}")
    finally:
        _lib.seccomp_release(ctx)

if __name__ == "__main__":
    network_guard()
    os.execv(sys.executable, [sys.executable, *sys.argv[1:]])
````

Lệnh:

````bash
python /tmp/wp923_network_guard.py -c 'from pathlib import Path; print("guarded_python_running=True"); print("\n".join(x for x in Path("/proc/self/status").read_text().splitlines() if x.startswith(("NoNewPrivs:", "Seccomp:", "Seccomp_filters:"))))'
````

Output thật (exit code 0):

````text
guarded_python_running=True
NoNewPrivs:	1
Seccomp:	2
Seccomp_filters:	2
````

Lệnh:

````bash
python - <<'PY'
import hashlib, os, re, shlex, subprocess, sys
from pathlib import Path
repo = Path("cay-kho").resolve()
scratch = Path("/tmp/wp923-r2-independent")
tmp = scratch / "test-tmp"
tmp.mkdir(exist_ok=True)
log = scratch / "n2-reviewed-merge-seccomp.log"
sys.path.insert(0, "/tmp")
from wp923_network_guard import network_guard
overrides = dict(GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_COUNT="2",
                 GIT_CONFIG_KEY_0="commit.gpgsign", GIT_CONFIG_VALUE_0="false",
                 GIT_CONFIG_KEY_1="core.abbrev", GIT_CONFIG_VALUE_1="7",
                 GIT_OPTIONAL_LOCKS="0", PYTHONDONTWRITEBYTECODE="1", TMPDIR=str(tmp),
                 TL_SELFTEST_ALLOW_NET="0")
env = dict(os.environ, **overrides)
print("process_only_test_overrides=" + repr(overrides))
head = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"]).decode().strip()
print("tested_sha=" + head)
assert head == "bbfb96cbe6b30e0b5b1b30982eae2b5893ac2c00"
cmd = [sys.executable, ".claude/dev/ci_dang_ky_test.py"]
print("test_cwd=" + str(repo))
print("actual_test_command=" + shlex.join(cmd), flush=True)
with log.open("wb") as stream:
    cp = subprocess.run(cmd, cwd=repo, env=env, stdout=stream, stderr=subprocess.STDOUT, timeout=180, preexec_fn=network_guard)
data = log.read_bytes()
text = data.decode("utf-8", "backslashreplace")
print(f"test_exit_code={cp.returncode}")
print(f"full_log={log}; bytes={len(data)}; sha256={hashlib.sha256(data).hexdigest()}")
print("positive_evidence:")
for line in text.splitlines():
    if line.startswith(("ĐĂNG KÝ:", "TRẠNG THÁI:", "LAUNCHER WINDOWS:", "RUFF CI:", "PHẢN CHỨNG:", "TỔNG:")):
        print(line)
for name in ("n2_base.log", "n2_merge.log"):
    supplied = Path(name).read_bytes()
    print(f"{name}: bytes={len(supplied)}; sha256={hashlib.sha256(supplied).hexdigest()}; reviewer_log_equals_every_byte={data == supplied}")
print("kernel_network_guard=seccomp; inherited by all test descendants")
if cp.returncode:
    print("failure_tail:\n" + "\n".join(text.splitlines()[-35:]))
assert cp.returncode == 0 and "ĐĂNG KÝ: 28/28" in text and "PHẢN CHỨNG: 1070/1070 đỏ đúng" in text and "TỔNG: ĐẠT" in text
assert data == Path("n2_base.log").read_bytes() == Path("n2_merge.log").read_bytes()
print("N2_independent_exact_merge_head=PASS")
PY
````

Output thật (exit code 0):

````text
process_only_test_overrides={'GIT_CONFIG_GLOBAL': '/dev/null', 'GIT_CONFIG_COUNT': '2', 'GIT_CONFIG_KEY_0': 'commit.gpgsign', 'GIT_CONFIG_VALUE_0': 'false', 'GIT_CONFIG_KEY_1': 'core.abbrev', 'GIT_CONFIG_VALUE_1': '7', 'GIT_OPTIONAL_LOCKS': '0', 'PYTHONDONTWRITEBYTECODE': '1', 'TMPDIR': '/tmp/wp923-r2-independent/test-tmp', 'TL_SELFTEST_ALLOW_NET': '0'}
tested_sha=bbfb96cbe6b30e0b5b1b30982eae2b5893ac2c00
test_cwd=/tmp/claude-0/-home-user-tra-luat/6cf1da84-5813-5156-ad6b-b3a2dbd3ab61/scratchpad/rv2/cay-kho
actual_test_command=/usr/bin/python .claude/dev/ci_dang_ky_test.py
test_exit_code=0
full_log=/tmp/wp923-r2-independent/n2-reviewed-merge-seccomp.log; bytes=61886; sha256=ef11caf341ed192c60c62430ddb81f53d10b03304fdc871dc29c8ce22b90de88
positive_evidence:
ĐĂNG KÝ: 28/28
TRẠNG THÁI: chan=28 cach_ly=0
LAUNCHER WINDOWS: 4/4 hợp đồng
RUFF CI: 3/3 hợp đồng
PHẢN CHỨNG: 1070/1070 đỏ đúng
TỔNG: ĐẠT
n2_base.log: bytes=61886; sha256=ef11caf341ed192c60c62430ddb81f53d10b03304fdc871dc29c8ce22b90de88; reviewer_log_equals_every_byte=True
n2_merge.log: bytes=61886; sha256=ef11caf341ed192c60c62430ddb81f53d10b03304fdc871dc29c8ce22b90de88; reviewer_log_equals_every_byte=True
kernel_network_guard=seccomp; inherited by all test descendants
N2_independent_exact_merge_head=PASS
````

Kết luận: KHÔNG PHẢI LỖI — reviewer tự chạy Python không truyền --chay trên exact merge head: rc=0, đăng ký 28/28, phản chứng 1070/1070, TỔNG: ĐẠT. Log bằng từng byte n2_base.log và n2_merge.log. Cô lập cấu hình Git toàn cục bằng GIT_CONFIG_GLOBAL=/dev/null, tắt ký và ghim core.abbrev=7 chỉ trong môi trường tiến trình fixture; không sửa cấu hình kho. Lần thử strace ban đầu bị sandbox từ chối ptrace trước khi test chạy; lần đo thành công dùng bộ lọc seccomp kế thừa qua mọi tiến trình con để cấm mạng, không cần ptrace.

### HƯỚNG 9: N4: tự chạy tl.py --selftest trên đúng merge head

Giả thuyết: Thay đổi master hoặc tương tác merge có thể phá selftest runtime chung.

Lệnh:

````bash
python - <<'PY'
import hashlib, os, re, shlex, subprocess, sys
from pathlib import Path
repo = Path("cay-kho").resolve()
scratch = Path("/tmp/wp923-r2-independent")
tmp = scratch / "test-tmp"
tmp.mkdir(exist_ok=True)
cache = scratch / "selftest-cache"
cache.mkdir(exist_ok=True)
log = scratch / "tl-selftest-reviewed-merge.log"
sys.path.insert(0, "/tmp")
from wp923_network_guard import network_guard
overrides = dict(GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_COUNT="2",
                 GIT_CONFIG_KEY_0="commit.gpgsign", GIT_CONFIG_VALUE_0="false",
                 GIT_CONFIG_KEY_1="core.abbrev", GIT_CONFIG_VALUE_1="7",
                 GIT_OPTIONAL_LOCKS="0", PYTHONDONTWRITEBYTECODE="1", TMPDIR=str(tmp),
                 TL_SELFTEST_ALLOW_NET="0", TL_CACHE_DIR=str(cache),
                 TL_WEBAPP="https://tl-selftest.invalid/exec", TL_TOKEN="tl_selftest_dummy")
env = dict(os.environ, **overrides)
print("process_only_test_overrides=" + repr(overrides))
head = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"]).decode().strip()
print("tested_sha=" + head)
assert head == "bbfb96cbe6b30e0b5b1b30982eae2b5893ac2c00"
cmd = [sys.executable, "scripts/tl.py", "--selftest"]
print("test_cwd=" + str(repo))
print("actual_test_command=" + shlex.join(cmd), flush=True)
with log.open("wb") as stream:
    cp = subprocess.run(cmd, cwd=repo, env=env, stdout=stream, stderr=subprocess.STDOUT,
                        timeout=300, preexec_fn=network_guard)
data = log.read_bytes()
text = data.decode("utf-8", "backslashreplace")
print(f"test_exit_code={cp.returncode}")
print(f"full_log={log}; bytes={len(data)}; sha256={hashlib.sha256(data).hexdigest()}")
print("actual_log_tail:\n" + "\n".join(text.splitlines()[-14:]))
summaries = re.findall(r"(?im)^.*(?:selftest|tổng|total|passed|đạt).*\b(\d+)/(\d+).*$", text)
print("summary_fraction_pairs=" + repr(summaries))
print("kernel_network_guard=seccomp; IPv4/IPv6 socket creation and connect/send syscalls denied for test and descendants")
assert cp.returncode == 0
assert any(int(a) == int(b) and int(a) > 0 for a,b in summaries)
print("N4_independent_exact_merge_head=PASS")
PY
````

Output thật (exit code 1):

````text
process_only_test_overrides={'GIT_CONFIG_GLOBAL': '/dev/null', 'GIT_CONFIG_COUNT': '2', 'GIT_CONFIG_KEY_0': 'commit.gpgsign', 'GIT_CONFIG_VALUE_0': 'false', 'GIT_CONFIG_KEY_1': 'core.abbrev', 'GIT_CONFIG_VALUE_1': '7', 'GIT_OPTIONAL_LOCKS': '0', 'PYTHONDONTWRITEBYTECODE': '1', 'TMPDIR': '/tmp/wp923-r2-independent/test-tmp', 'TL_SELFTEST_ALLOW_NET': '0', 'TL_CACHE_DIR': '/tmp/wp923-r2-independent/selftest-cache', 'TL_WEBAPP': 'https://tl-selftest.invalid/exec', 'TL_TOKEN': 'tl_selftest_dummy'}
tested_sha=bbfb96cbe6b30e0b5b1b30982eae2b5893ac2c00
test_cwd=/tmp/claude-0/-home-user-tra-luat/6cf1da84-5813-5156-ad6b-b3a2dbd3ab61/scratchpad/rv2/cay-kho
actual_test_command=/usr/bin/python scripts/tl.py --selftest
test_exit_code=1
full_log=/tmp/wp923-r2-independent/tl-selftest-reviewed-merge.log; bytes=78448; sha256=3ad2510ca229fe045679d76c20273ad9bd167e999b59c60d7ede60fb381131f5
actual_log_tail:
  [OK] wp42_test_id_index_collision_policy
  [OK] wp42_fragment_computed_test_id_rejected
  [OK] wp42_fragment_duplicate_literal_test_id_rejected
  [OK] wp42_fragment_path_mismatch_precedes_missing_run
  [OK] wp42_fragment_path_mismatch_precedes_async_run
  [OK] r285_khong_ro_ri_monkeypatch
  [OK] wp43_bundled_generator_byte_canonical
  [OK] wp43_release_excludes_only_canonical_fragment_prefix
  [OK] wp44_dev_topology_prefers_fragments
  [OK] wp44_release_bundle_topology_under_200
  [OK] wp44_missing_bundled_module_named
  [OK] r332_registry_coverage_duong_san_xuat
  [OK] wp42_complete_runtime_test_ids_unique
== tl selftest 1730/1731 ==
summary_fraction_pairs=[('12', '12'), ('1', '2'), ('2', '2'), ('1730', '1731')]
kernel_network_guard=seccomp; IPv4/IPv6 socket creation and connect/send syscalls denied for test and descendants
Traceback (most recent call last):
  File "<stdin>", line 37, in <module>
AssertionError
````

Lệnh:

````bash
sed -n '26943,26998p' cay-kho/scripts/tl_selftest.py
````

Output thật (exit code 0):

````text
    # độ dài tiền tố UUID notebook ⇒ 18 tiền tố bị hô SHA_NOT_A_COMMIT, và chính ca
    # `r218_docclaims_l2_sha_khong_ton_tai` (mồi `deadbee`, 7 ký tự) cũng đỏ theo.
    # PHẢN CHỨNG 2 CHIỀU trên kho git THẬT (không giả lập `_doc_claims_git`): cùng một tài liệu, chỉ đổi
    # `core.abbrev`, mà kết luận của L2 lật — đó là bằng chứng dòng ghim trong CI là dòng GÁNH VIỆC.
    def _c226_nguong_l2_troi_theo_abbrev_va_ci_ghim():
        import subprocess as _sp226c
        import tempfile as _tf226c
        _check = _TL_MODULE._doc_claims_check   # đường sản xuất: chính `cmd_doc_claims_check` gọi hàm này

        def _git(cwd, *args):
            return _sp226c.run(["git", "-c", "user.email=t@t", "-c", "user.name=t", *args], cwd=str(cwd),
                               capture_output=True, text=True, timeout=120).returncode
        with _tf226c.TemporaryDirectory() as _td:
            _kho = Path(_td) / "kho"
            _kho.mkdir()
            if _git(_kho, "init", "-q") != 0:
                return False
            # `abc1234`: 7 hex có chữ a-f, KHÔNG phải commit nào — đúng hình dạng L2 phải bắt khi ngưỡng=7
            (_kho / "CONTEXT.md").write_text("# T\n\nsửa ở abc1234 nhé.\n", encoding="utf-8")
            _git(_kho, "add", "-A")
            _git(_kho, "commit", "-q", "-m", "c1")

            def _l2_flags(abbrev):
                _git(_kho, "config", "core.abbrev", str(abbrev))
                _j = _check(root=_kho)
                return ([f["claim"] for f in (_j.get("flags") or []) if f.get("layer") == "L2"],
                        [x["claim"] for x in (_j.get("advisories") or []) if x.get("layer") == "L2"],
                        (_j.get("basis") or {}).get("sha_lens"))
            _f7, _a7, _len7 = _l2_flags(7)
            _f8, _a8, _len8 = _l2_flags(8)
        # ngưỡng 7 ⇒ CỜ CỨNG · ngưỡng 8 ⇒ tụt xuống advisory. Cùng tài liệu, khác chỗ chạy.
        ok1 = _f7 == ["abc1234"] and _len7 == [7, 40]
        ok2 = _f8 == [] and _a8 == ["abc1234"] and _len8 == [8, 40]
        # (b) DRIFT-LOCK đường TỰ ĐỘNG — đúng bài học r219/r225: guard không nối vào CI thì chỉ là tài
        #     liệu. Hai dòng phải CÙNG có mặt, và dòng ghim phải đứng TRƯỚC bước gọi doc-claims-check.
        #     Neo vào chính DÒNG BƯỚC (`- name: doc-claims-check…`), KHÔNG neo vào chuỗi trần
        #     `doc-claims-check` — chuỗi trần còn nằm trong các dòng chú thích phía trên, so vị trí với
        #     nó là so với một comment chứ không so với bước chạy (đã cắn đúng cái đó khi viết ca này).
        #
        # r227 — HAI BỐI CẢNH, hai khẳng định KHÁC NHAU. Bản r226 chỉ đúng một bối cảnh nên ĐỎ ở bối
        # cảnh kia: smoke-test bản ĐÃ CÀI (bung bundle ra rồi `tl --selftest` từ đó) bắt được ca này đỏ
        # vì `.github/` KHÔNG nằm trong gói — CỐ Ý, gói không mang cấu hình CI — tức đỏ do CHỖ CHẠY chứ
        # không do drift. KHÔNG chữa bằng «thiếu tệp thì cho qua»: như thế xoá ci.yml trong kho cũng
        # lọt lưới. Mỗi bối cảnh gánh một khẳng định riêng, không bối cảnh nào xanh vì im lặng:
        #   · trong CÂY GIT → ci.yml PHẢI có và đúng thứ tự (drift-lock như cũ);
        #   · trong GÓI CÀI → `.github/` PHẢI KHÔNG có (nếu có tức tệp dev lọt vào bundle — cũng là lỗi).
        _ci_p = _ROOT209 / ".github" / "workflows" / "ci.yml"
        if (_ROOT209 / ".git").exists():          # worktree để `.git` là TỆP ⇒ `.exists()` phủ cả hai
            _ci = _ci_p.read_text(encoding="utf-8", errors="replace")
            _i_pin = _ci.find("core.abbrev 7")
            _i_depth = _ci.find("fetch-depth: 0")
            _i_dcc = _ci.find("- name: doc-claims-check")
            ok3 = 0 <= _i_pin < _i_dcc and 0 <= _i_depth < _i_dcc
        else:
            ok3 = not _ci_p.exists() and not (_ROOT209 / ".github").exists()
        return ok1 and ok2 and ok3
````

Lệnh:

````bash
python - <<'PY'
import os, subprocess, sys, tempfile
from pathlib import Path
from unittest.mock import patch
repo = Path("cay-kho").resolve()
sys.path.insert(0, "/tmp")
from wp923_network_guard import network_guard
network_guard()
sys.path.insert(0, str(repo / "scripts"))
import tl
env0 = dict(os.environ, GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_COUNT="1",
            GIT_CONFIG_KEY_0="commit.gpgsign", GIT_CONFIG_VALUE_0="false",
            PYTHONDONTWRITEBYTECODE="1", GIT_OPTIONAL_LOCKS="0")
with tempfile.TemporaryDirectory(prefix="wp923-abbrev-fixture-") as td:
    root = Path(td)
    def git(*args, env=env0):
        return subprocess.check_output(["git", "-C", str(root), "-c", "user.name=t",
                                        "-c", "user.email=t@t", *args], env=env).decode().strip()
    git("init", "-q")
    (root / "CONTEXT.md").write_text("# T\n\nsửa ở abc1234 nhé.\n", encoding="utf-8")
    git("add", "-A")
    git("commit", "-q", "-m", "fixture-only")
    results = {}
    for label, forced in (("reviewer_forced_abbrev", True), ("fixture_controls_abbrev", False)):
        env = dict(env0)
        if forced:
            env.update(GIT_CONFIG_COUNT="2", GIT_CONFIG_KEY_1="core.abbrev", GIT_CONFIG_VALUE_1="7")
        else:
            env.pop("GIT_CONFIG_KEY_1", None)
            env.pop("GIT_CONFIG_VALUE_1", None)
        for local in (7, 8):
            git("config", "core.abbrev", str(local), env=env)
            with patch.dict(os.environ, env, clear=True):
                j = tl._doc_claims_check(root=root)
            result = dict(effective_abbrev=git("config", "--get", "core.abbrev", env=env),
                          sha_lens=j.get("basis", {}).get("sha_lens"),
                          flags=[f["claim"] for f in j.get("flags", []) if f.get("layer") == "L2"],
                          advisories=[a["claim"] for a in j.get("advisories", []) if a.get("layer") == "L2"])
            results[(label, local)] = result
            print(f"{label}; fixture_local_abbrev={local}; {result}")
    assert results[("reviewer_forced_abbrev", 8)]["sha_lens"] == [7, 40]
    assert results[("fixture_controls_abbrev", 8)]["sha_lens"] == [8, 40]
    assert results[("fixture_controls_abbrev", 8)]["flags"] == []
    assert results[("fixture_controls_abbrev", 8)]["advisories"] == ["abc1234"]
print("r226_failure_is_process_environment_override=PASS")
local = subprocess.check_output(["git", "-C", str(repo), "config", "--local", "--get", "core.abbrev"]).decode().strip()
print("reviewed_repository_existing_local_core_abbrev=" + local)
assert local == "7"
PY
````

Output thật (exit code 0):

````text
reviewer_forced_abbrev; fixture_local_abbrev=7; {'effective_abbrev': '7', 'sha_lens': [7, 40], 'flags': ['abc1234'], 'advisories': []}
reviewer_forced_abbrev; fixture_local_abbrev=8; {'effective_abbrev': '7', 'sha_lens': [7, 40], 'flags': ['abc1234'], 'advisories': []}
fixture_controls_abbrev; fixture_local_abbrev=7; {'effective_abbrev': '7', 'sha_lens': [7, 40], 'flags': ['abc1234'], 'advisories': []}
fixture_controls_abbrev; fixture_local_abbrev=8; {'effective_abbrev': '8', 'sha_lens': [8, 40], 'flags': [], 'advisories': ['abc1234']}
r226_failure_is_process_environment_override=PASS
reviewed_repository_existing_local_core_abbrev=7
````

Lệnh:

````bash
python - <<'PY'
import hashlib, os, re, shlex, subprocess, sys
from pathlib import Path
repo = Path("cay-kho").resolve()
scratch = Path("/tmp/wp923-r2-independent")
tmp = scratch / "test-tmp"
tmp.mkdir(exist_ok=True)
cache = scratch / "selftest-cache-unpinned"
cache.mkdir(exist_ok=True)
log = scratch / "tl-selftest-reviewed-merge-no-abbrev-env.log"
sys.path.insert(0, "/tmp")
from wp923_network_guard import network_guard
overrides = dict(GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_COUNT="1",
                 GIT_CONFIG_KEY_0="commit.gpgsign", GIT_CONFIG_VALUE_0="false",
                 GIT_OPTIONAL_LOCKS="0", PYTHONDONTWRITEBYTECODE="1", TMPDIR=str(tmp),
                 TL_SELFTEST_ALLOW_NET="0", TL_CACHE_DIR=str(cache),
                 TL_WEBAPP="https://tl-selftest.invalid/exec", TL_TOKEN="tl_selftest_dummy")
env = dict(os.environ, **overrides)
print("process_only_test_overrides=" + repr(overrides))
head = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"]).decode().strip()
print("tested_sha=" + head)
assert head == "bbfb96cbe6b30e0b5b1b30982eae2b5893ac2c00"
cmd = [sys.executable, "scripts/tl.py", "--selftest"]
print("test_cwd=" + str(repo))
print("actual_test_command=" + shlex.join(cmd), flush=True)
with log.open("wb") as stream:
    cp = subprocess.run(cmd, cwd=repo, env=env, stdout=stream, stderr=subprocess.STDOUT,
                        timeout=900, preexec_fn=network_guard)
data = log.read_bytes()
text = data.decode("utf-8", "backslashreplace")
print(f"test_exit_code={cp.returncode}")
print(f"full_log={log}; bytes={len(data)}; sha256={hashlib.sha256(data).hexdigest()}")
print("actual_log_tail:\n" + "\n".join(text.splitlines()[-14:]))
summaries = re.findall(r"(?im)^.*(?:selftest|tổng|total|passed|đạt).*\b(\d+)/(\d+).*$", text)
print("summary_fraction_pairs=" + repr(summaries))
print("kernel_network_guard=seccomp; IPv4/IPv6 socket creation and connect/send syscalls denied for test and descendants")
assert cp.returncode == 0
assert any(int(a) == int(b) and int(a) > 0 for a,b in summaries)
print("N4_independent_exact_merge_head=PASS")
PY
````

Output thật (exit code 0):

````text
process_only_test_overrides={'GIT_CONFIG_GLOBAL': '/dev/null', 'GIT_CONFIG_COUNT': '1', 'GIT_CONFIG_KEY_0': 'commit.gpgsign', 'GIT_CONFIG_VALUE_0': 'false', 'GIT_OPTIONAL_LOCKS': '0', 'PYTHONDONTWRITEBYTECODE': '1', 'TMPDIR': '/tmp/wp923-r2-independent/test-tmp', 'TL_SELFTEST_ALLOW_NET': '0', 'TL_CACHE_DIR': '/tmp/wp923-r2-independent/selftest-cache-unpinned', 'TL_WEBAPP': 'https://tl-selftest.invalid/exec', 'TL_TOKEN': 'tl_selftest_dummy'}
tested_sha=bbfb96cbe6b30e0b5b1b30982eae2b5893ac2c00
test_cwd=/tmp/claude-0/-home-user-tra-luat/6cf1da84-5813-5156-ad6b-b3a2dbd3ab61/scratchpad/rv2/cay-kho
actual_test_command=/usr/bin/python scripts/tl.py --selftest
test_exit_code=0
full_log=/tmp/wp923-r2-independent/tl-selftest-reviewed-merge-no-abbrev-env.log; bytes=78500; sha256=8ad735f968ded06f5d8eaded419ac296415e24e8e3a163f6731451a0f5796c4a
actual_log_tail:
  [OK] wp42_test_id_index_collision_policy
  [OK] wp42_fragment_computed_test_id_rejected
  [OK] wp42_fragment_duplicate_literal_test_id_rejected
  [OK] wp42_fragment_path_mismatch_precedes_missing_run
  [OK] wp42_fragment_path_mismatch_precedes_async_run
  [OK] r285_khong_ro_ri_monkeypatch
  [OK] wp43_bundled_generator_byte_canonical
  [OK] wp43_release_excludes_only_canonical_fragment_prefix
  [OK] wp44_dev_topology_prefers_fragments
  [OK] wp44_release_bundle_topology_under_200
  [OK] wp44_missing_bundled_module_named
  [OK] r332_registry_coverage_duong_san_xuat
  [OK] wp42_complete_runtime_test_ids_unique
== tl selftest 1731/1731 ==
summary_fraction_pairs=[('12', '12'), ('1', '2'), ('2', '2'), ('1731', '1731')]
kernel_network_guard=seccomp; IPv4/IPv6 socket creation and connect/send syscalls denied for test and descendants
N4_independent_exact_merge_head=PASS
````

Kết luận: KHÔNG PHẢI LỖI — tự chạy lại exact merge head rc=0, 1731/1731. Lần đầu 1730/1731 do reviewer ghim core.abbrev=7 cấp tiến trình làm fixture của r226 không đổi được sang 8; đã chứng minh A/B bằng hàm sản phẩm và bỏ riêng override ấy. Repo-local core.abbrev=7 giữ nguyên. Tắt ký chỉ trong tiến trình, TMPDIR và cache chỉ định ở /tmp, nhưng test còn sinh artifact ignored được xử lý tại HƯỚNG 10; seccomp chặn mạng cho test và tiến trình con.

### HƯỚNG 10: Toàn vẹn cuối lượt, side effect của test và giới hạn CI

Giả thuyết: Các phép đo có thể sinh artifact ignored, freshen mtime object, làm stale SHA hoặc vô tình coi CI chưa đo là xanh.

Lệnh:

````bash
sed -n '1,16p' VERDICT_LUOT1.md; tail -n 4 VERDICT_LUOT1.md
````

Output thật (exit code 0):

````text
verdict: approve
reviewed_sha: 67bacb3b51ac9eda72297b10b15b798b3ca51959
reviewed_tree: 8512df452237dad95f764b23204ebd8387d69fdb
base_sha: e139e55883d90fd74a358230be5599c9e223d4b3
spec_sha256: a36f8d2d84d39c3587a60edcb63d4886f82e3fae097c283700718b5869eecbc1
packet: wp923 r2, pha B
review_class: sensitive
role: reviewer
provider: openai_codex
model_family: openai
model: GPT-6 (theo khai báo runtime; snapshot/effort không đo độc lập)
execution_surface: codex_service (agent API với công cụ shell cục bộ)
transport: machine
independent_from_executor_session: true
github_submitter_identity: null (không đăng ra ngoài)


## FINDINGS

Không có finding P0/P1/P2/P3. Độ tin: cao đối với phạm vi diff và các phép đo local đã ghi; N5 chưa đo.
````

Lệnh:

````bash
git -C cay-kho rev-parse HEAD 'HEAD^{tree}'; git -C cay-kho log -1 --format=%P; git -C cay-kho --no-optional-locks status --porcelain=v1 --untracked-files=all; sha256sum SPEC.md
````

Output thật (exit code 0):

````text
bbfb96cbe6b30e0b5b1b30982eae2b5893ac2c00
747d266c10c7ae9125f37e49ff6b60e6375c29a9
67bacb3b51ac9eda72297b10b15b798b3ca51959 09db70350414d767b793a71cb630e643f216a1b1
a36f8d2d84d39c3587a60edcb63d4886f82e3fae097c283700718b5869eecbc1  SPEC.md
````

Lệnh:

````bash
python - <<'PY'
import hashlib, json, os, re, stat, subprocess
from pathlib import Path
selftest = Path("/tmp/wp923-r2-independent/tl-selftest-reviewed-merge-no-abbrev-env.log").read_text()
totals = re.findall(r"(?m)^== tl selftest (\d+)/(\d+) ==$", selftest)
failed_cases = re.findall(r"(?m)^\s*\[FAIL\].*$", selftest)
print("final_selftest_summary_pairs=" + repr(totals))
print("final_selftest_failed_cases=" + repr(failed_cases))
assert totals == [("1731", "1731")] and not failed_cases
root = Path("cay-kho")
before = json.loads(Path("/tmp/wp923-r2-independent/repository-before.json").read_text())
after = {}
for p in sorted(root.rglob("*")):
    s = p.lstat()
    item = dict(mode=stat.S_IMODE(s.st_mode), mtime_ns=s.st_mtime_ns)
    if p.is_symlink():
        item.update(kind="symlink", target=os.readlink(p))
    elif p.is_file():
        data = p.read_bytes()
        item.update(kind="file", size=len(data), sha256=hashlib.sha256(data).hexdigest())
    elif p.is_dir():
        item.update(kind="directory")
    else:
        item.update(kind="other")
    after[str(p.relative_to(root))] = item
added = sorted(after.keys() - before.keys())
removed = sorted(before.keys() - after.keys())
changed = sorted(k for k in before.keys() & after.keys() if before[k] != after[k])
print(f"repository_entries_before={len(before)}; after={len(after)}")
print("added=" + repr(added))
print("removed=" + repr(removed))
print("changed_bytes_mode_or_mtime=" + repr(changed))
print("includes_dot_git_objects_index_refs_config=True")
assert before == after
head = subprocess.check_output(["git", "-C", "cay-kho", "rev-parse", "HEAD"]).decode().strip()
clean = not subprocess.check_output(["git", "-C", "cay-kho", "--no-optional-locks", "status", "--porcelain=v1", "--untracked-files=all"])
print(f"final_head={head}; worktree_clean={clean}")
assert head == "bbfb96cbe6b30e0b5b1b30982eae2b5893ac2c00" and clean
actual = subprocess.check_output(["git", "-C", "cay-kho", "diff", "--stat",
                                 "e139e55883d90fd74a358230be5599c9e223d4b3",
                                 "09db70350414d767b793a71cb630e643f216a1b1"])
supplied = Path("master_mang_vao.stat").read_bytes()
print(f"master_stat_artifact_equals_actual_every_byte={actual == supplied}")
print(f"actual_master_stat_sha256={hashlib.sha256(actual).hexdigest()}")
assert actual == supplied
print("local_top_level_packet_files=" + repr(sorted(p.name for p in Path(".").iterdir() if p.is_file())))
print("N5=not_run / KHÔNG ĐO ĐƯỢC: không gọi mạng, không truy vấn check-run GitHub của reviewed_sha")
print("repository_read_only_integrity=PASS")
PY
````

Output thật (exit code 1):

````text
final_selftest_summary_pairs=[('1731', '1731')]
final_selftest_failed_cases=[]
repository_entries_before=7910; after=7934
added=['references/golden/fixtures', 'references/golden/fixtures/cache_hygiene', 'references/golden/fixtures/cache_hygiene/extract_gd_doctext60.txt', 'references/golden/fixtures/cache_hygiene/manifest.json', 'references/golden/fixtures/config_fixture.json', 'references/golden/fixtures/doc_claims', 'references/golden/fixtures/doc_claims/claims.md', 'references/golden/fixtures/dup.zip', 'references/golden/fixtures/sample_profile.txt', 'references/golden/fixtures/slip.zip', 'references/golden/fixtures/snap_a.json', 'references/golden/fixtures/snap_a2.json', 'scripts/.tl_state', 'scripts/.tl_state/nlm_list_cache_nbX.json', 'scripts/.tl_state/reconcile_plan_22222222-2222-4222-8222-222222222222.json', 'scripts/.tl_state/reconcile_plan_NB1.json', 'scripts/.tl_state/reconcile_plan_NBc.BLOCKED.json', 'scripts/.tl_state/reconcile_plan_NBc.json', 'scripts/.tl_state/reconcile_plan_NBd.BLOCKED.json', 'scripts/.tl_state/reconcile_plan_NBp.BLOCKED.json', 'scripts/.tl_state/reconcile_plan_NBp.json', 'scripts/.tl_state/reconcile_plan_base96.json', 'scripts/.tl_state/reconcile_plan_ov-reg-110.json', 'scripts/.tl_state/reconcile_plan_ovf96.json']
removed=[]
changed_bytes_mode_or_mtime=['.git/objects/74/7d266c10c7ae9125f37e49ff6b60e6375c29a9', '.git/objects/c6/fcf1c455a1aa54cd32f5faf0ab55d2722ead7b', 'references/golden', 'scripts']
includes_dot_git_objects_index_refs_config=True
Traceback (most recent call last):
  File "<stdin>", line 33, in <module>
AssertionError
````

Lệnh:

````bash
python - <<'PY'
import hashlib, json, os, stat, subprocess, tarfile
from pathlib import Path
root = Path("cay-kho")
scratch = Path("/tmp/wp923-r2-independent")
before = json.loads((scratch / "repository-before.json").read_text())
observed = json.loads((scratch / "repository-after-tests.json").read_text())
def snapshot():
    out = {}
    for p in sorted(root.rglob("*")):
        s = p.lstat()
        item = dict(mode=stat.S_IMODE(s.st_mode), mtime_ns=s.st_mtime_ns)
        if p.is_symlink():
            item.update(kind="symlink", target=os.readlink(p))
        elif p.is_file():
            data = p.read_bytes()
            item.update(kind="file", size=len(data), sha256=hashlib.sha256(data).hexdigest())
        elif p.is_dir():
            item.update(kind="directory")
        else:
            item.update(kind="other")
        out[str(p.relative_to(root))] = item
    return out
current = snapshot()
assert current == observed, "New change after side-effect audit; refuse cleanup"
added = sorted(current.keys() - before.keys())
removed = sorted(before.keys() - current.keys())
changed = sorted(k for k in before.keys() & current.keys() if before[k] != current[k])
assert not removed
assert len(added) == 24
assert all(x == "references/golden/fixtures" or x.startswith("references/golden/fixtures/")
           or x == "scripts/.tl_state" or x.startswith("scripts/.tl_state/") for x in added)
assert set(changed) == {
    ".git/objects/74/7d266c10c7ae9125f37e49ff6b60e6375c29a9",
    ".git/objects/c6/fcf1c455a1aa54cd32f5faf0ab55d2722ead7b",
    "references/golden", "scripts",
}
for name in changed:
    a, b = before[name], current[name]
    fields = [k for k in a.keys() | b.keys() if a.get(k) != b.get(k)]
    print(f"changed_entry={name}; changed_fields={fields}")
    assert fields == ["mtime_ns"]
    if a["kind"] == "file":
        print(f"unchanged_object_bytes_sha256={a['sha256']}")
ignored = subprocess.run(["git", "-C", "cay-kho", "check-ignore", "--stdin"],
                         input=("\n".join(added) + "\n").encode(),
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
ignored_names = ignored.stdout.decode().splitlines()
print(f"added_entries={len(added)}; all_ignored={set(ignored_names) == set(added)}")
assert set(ignored_names) == set(added)
archive = scratch / "test-created-ignored-artifacts.tar.gz"
with tarfile.open(archive, "w:gz") as tar:
    for name in added:
        tar.add(root / name, arcname=name, recursive=False)
print(f"artifact_archive={archive}; sha256={hashlib.sha256(archive.read_bytes()).hexdigest()}")
(scratch / "cleanup-manifest.json").write_text(json.dumps(
    dict(added={k: current[k] for k in added},
         metadata_changes={k: dict(before=before[k], after=current[k]) for k in changed}),
    ensure_ascii=False, indent=2))
deleted_files = deleted_dirs = 0
for name in sorted(added, key=lambda s: (s.count("/"), s), reverse=True):
    p = root / name
    if current[name]["kind"] == "file":
        assert p.is_file() and not p.is_symlink()
        assert hashlib.sha256(p.read_bytes()).hexdigest() == current[name]["sha256"]
        p.unlink()
        deleted_files += 1
    elif current[name]["kind"] == "directory":
        p.rmdir()
        deleted_dirs += 1
    else:
        raise AssertionError("Unexpected new special entry")
for name in changed:
    p = root / name
    os.utime(p, ns=(p.stat().st_atime_ns, before[name]["mtime_ns"]), follow_symlinks=False)
print(f"removed_only_test_created_files={deleted_files}; removed_only_new_empty_directories={deleted_dirs}")
print(f"restored_mtime_entries={len(changed)}")
final = snapshot()
(scratch / "repository-after-cleanup.json").write_text(json.dumps(final, sort_keys=True))
print(f"original_snapshot_equals_after_cleanup={before == final}")
assert before == final
print("no_preexisting_file_bytes_or_mode_changed=True")
print("test_side_effect_cleanup=PASS")
PY
````

Output thật (exit code 0):

````text
changed_entry=.git/objects/74/7d266c10c7ae9125f37e49ff6b60e6375c29a9; changed_fields=['mtime_ns']
unchanged_object_bytes_sha256=79922a72e134aeb471941d087e367b091717a202d8a9d139f0f3e6cef5d98256
changed_entry=.git/objects/c6/fcf1c455a1aa54cd32f5faf0ab55d2722ead7b; changed_fields=['mtime_ns']
unchanged_object_bytes_sha256=b372a15ab67cd2c0dd3bd7beb98dc03be4e9c0cac9f9e7ab3985d01ca75740db
changed_entry=references/golden; changed_fields=['mtime_ns']
changed_entry=scripts; changed_fields=['mtime_ns']
added_entries=24; all_ignored=True
artifact_archive=/tmp/wp923-r2-independent/test-created-ignored-artifacts.tar.gz; sha256=377740fe45e1dffc0577f3f5babc725b91cd852805109b937b2ed85d23b732be
removed_only_test_created_files=20; removed_only_new_empty_directories=4
restored_mtime_entries=4
original_snapshot_equals_after_cleanup=True
no_preexisting_file_bytes_or_mode_changed=True
test_side_effect_cleanup=PASS
````

Lệnh:

````bash
python - <<'PY'
import hashlib, json, os, re, stat, subprocess
from pathlib import Path
selftest = Path("/tmp/wp923-r2-independent/tl-selftest-reviewed-merge-no-abbrev-env.log").read_text()
totals = re.findall(r"(?m)^== tl selftest (\d+)/(\d+) ==$", selftest)
failed_cases = re.findall(r"(?m)^\s*\[FAIL\].*$", selftest)
print("final_selftest_summary_pairs=" + repr(totals))
print("final_selftest_failed_cases=" + repr(failed_cases))
assert totals == [("1731", "1731")] and not failed_cases
root = Path("cay-kho")
before = json.loads(Path("/tmp/wp923-r2-independent/repository-before.json").read_text())
after = {}
for p in sorted(root.rglob("*")):
    s = p.lstat()
    item = dict(mode=stat.S_IMODE(s.st_mode), mtime_ns=s.st_mtime_ns)
    if p.is_symlink():
        item.update(kind="symlink", target=os.readlink(p))
    elif p.is_file():
        data = p.read_bytes()
        item.update(kind="file", size=len(data), sha256=hashlib.sha256(data).hexdigest())
    elif p.is_dir():
        item.update(kind="directory")
    else:
        item.update(kind="other")
    after[str(p.relative_to(root))] = item
added = sorted(after.keys() - before.keys())
removed = sorted(before.keys() - after.keys())
changed = sorted(k for k in before.keys() & after.keys() if before[k] != after[k])
print(f"repository_entries_before={len(before)}; after={len(after)}")
print("added=" + repr(added))
print("removed=" + repr(removed))
print("changed_bytes_mode_or_mtime=" + repr(changed))
print("includes_dot_git_objects_index_refs_config=True")
assert before == after
head = subprocess.check_output(["git", "-C", "cay-kho", "rev-parse", "HEAD"]).decode().strip()
clean = not subprocess.check_output(["git", "-C", "cay-kho", "--no-optional-locks", "status", "--porcelain=v1", "--untracked-files=all"])
print(f"final_head={head}; worktree_clean={clean}")
assert head == "bbfb96cbe6b30e0b5b1b30982eae2b5893ac2c00" and clean
actual = subprocess.check_output(["git", "-C", "cay-kho", "diff", "--stat",
                                 "e139e55883d90fd74a358230be5599c9e223d4b3",
                                 "09db70350414d767b793a71cb630e643f216a1b1"])
supplied = Path("master_mang_vao.stat").read_bytes()
print(f"master_stat_artifact_equals_actual_every_byte={actual == supplied}")
print(f"actual_master_stat_sha256={hashlib.sha256(actual).hexdigest()}")
assert actual == supplied
print("local_top_level_packet_files=" + repr(sorted(p.name for p in Path(".").iterdir() if p.is_file())))
print("N5=not_run / KHÔNG ĐO ĐƯỢC: không gọi mạng, không truy vấn check-run GitHub của reviewed_sha")
print("repository_read_only_integrity=PASS")
PY
````

Output thật (exit code 0):

````text
final_selftest_summary_pairs=[('1731', '1731')]
final_selftest_failed_cases=[]
repository_entries_before=7910; after=7910
added=[]
removed=[]
changed_bytes_mode_or_mtime=[]
includes_dot_git_objects_index_refs_config=True
final_head=bbfb96cbe6b30e0b5b1b30982eae2b5893ac2c00; worktree_clean=True
master_stat_artifact_equals_actual_every_byte=True
actual_master_stat_sha256=05be3b91376e4ccb5b0f24ef2a3fecd9a6f0df2f0a7b96a0deecad372dc3c5b1
local_top_level_packet_files=['PROMPT.md', 'SPEC.md', 'VERDICT.md', 'VERDICT_LUOT1.md', 'diff_vs_master.patch', 'master_mang_vao.stat', 'n2_base.log', 'n2_merge.log']
N5=not_run / KHÔNG ĐO ĐƯỢC: không gọi mạng, không truy vấn check-run GitHub của reviewed_sha
repository_read_only_integrity=PASS
````

Kết luận: KHÔNG PHẢI LỖI của packet — lần đối chiếu đầu phát hiện 20 tệp + 4 thư mục fixture/cache ignored do phép đo sinh ra; không tệp có sẵn nào đổi byte/mode. Hai Git object sẵn có chỉ đổi mtime, thêm mtime hai thư mục cha đổi. Đã lưu archive/manifest ngoài kho, dọn đúng 24 mục mới và khôi phục 4 mtime; sau đó toàn bộ 7910 mục gồm .git khớp snapshot đầu (byte/mode/mtime), HEAD/tree/cha/SPEC vẫn đúng, worktree sạch. Selftest cuối 1731/1731, không ca FAIL; master_mang_vao.stat khớp byte phép đo thật. N5: KHÔNG ĐO ĐƯỢC (not_run), không coi CI PR đã xanh. Không có sửa mã/config/ref, commit hay push trong kho được review; không che side effect tạm của công cụ/test.

## FINDINGS

Không có finding P0/P1/P2/P3 đối với nội dung packet ở reviewed_sha. Các lỗi phép đo/môi trường và side effect tạm đã được ghi, kiểm chứng nguyên nhân hoặc hoàn nguyên trong H3/H6/H8/H9/H10; không sửa mã sản phẩm để làm test xanh.

## GIỚI HẠN XÁC MINH

N5 chưa đo: không gọi API/mạng theo chỉ thị; artifact CI lịch sử của PR khác không được dùng làm bằng chứng xanh cho head này. Verdict chỉ chấp nhận nội dung review, không xác nhận lease/state, quyền merge/land/deploy hoặc trạng thái required checks trên GitHub.

N3 giới hạn ở cây tracked hiện tại, literal tên/digest (đầy đủ và tiền tố) cùng diff/consumer đã đọc; không khẳng định chứng minh được mọi đường đọc động bên ngoài kho.

Test chạy trên đúng tracked tree của reviewed_sha. Test có tạo 20 tệp và 4 thư mục ignored trong kho; phép đo cũng ghi nhận mtime hai Git object có sẵn đổi. Đã lưu archive và manifest ngoài kho, dọn riêng mục mới và khôi phục mtime; snapshot cuối bằng snapshot đầu. Không sửa byte/mode của tệp có sẵn, config, ref; không commit/push trong cay-kho. Fixture Git tạm ở /tmp có commit để thực hiện phép thử được yêu cầu.

Cấu hình ký Git được cô lập cho tiến trình test; N4 thành công dùng core.abbrev=7 repo-local vốn có, không ép abbrev cho fixture. strace không khả dụng do ptrace bị cấm; test thành công chạy với seccomp cấm mạng kế thừa qua tiến trình con. Model/effort không có chứng thực độc lập ngoài khai báo runtime.
