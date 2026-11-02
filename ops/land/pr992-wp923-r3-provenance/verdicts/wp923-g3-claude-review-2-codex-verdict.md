verdict: approve
reviewed_sha: 5a05d472227d8c14ffa9eedfb516aa4c494108e6
reviewed_tree: e41f180c8a03ebae611a52dc9a80a908fe6caff8
parent_1: 4ea2ae5e1edf152c0a0a35fcdde6f0a9e99ae7ba
parent_2_master: 44884446f71c89e25f9a72ac58e4f597db63c1ba
base_sha: 7f19424478616b2c5d0a0c7f26839e1d1c41261b
spec_sha256: 0a694a96f02fb02c01e7707d725591dae5f4455464a77e90ca5fd22435eb1ea5

## BẢNG SĂN

Đã kiểm chứng 8 mục của chỉ thị, thêm một hướng bảo toàn nguồn. Mọi phép đo cục bộ; mọi ghi và fixture Git nằm ngoài `cay-kho`. Không tạo commit trên cây/nhánh executor, không push, không gọi mạng. Báo cáo được tạo ở trạng thái `pending` trước kiểm tra và cập nhật sau từng hướng.

### HƯỚNG 1: Neo exact SHA và đồng nhất từng byte

- Giả thuyết: Merge thay nội dung tệp đã được approve hoặc sai neo/spec.
- Lệnh điều phối: `python -B review_evidence/review.py 1`. Lệnh con, cwd, stdout/stderr và rc thật: [h1.log](review_evidence/h1.log).
- Lệnh chính (các cờ vô hiệu external diff/textconv được giữ nguyên trong log):

```sh
git -C cay-kho rev-parse HEAD HEAD^{tree}
git -C cay-kho show -s --format=%P 5a05d472227d8c14ffa9eedfb516aa4c494108e6
git -C cay-kho show 4ea2ae5e1edf152c0a0a35fcdde6f0a9e99ae7ba:.claude/dev/ci_dang_ky_test.py
git -C cay-kho show 5a05d472227d8c14ffa9eedfb516aa4c494108e6:.claude/dev/ci_dang_ky_test.py
sha256sum SPEC.md
```

- Output thật:

```text
0a694a96f02fb02c01e7707d725591dae5f4455464a77e90ca5fd22435eb1ea5  SPEC.md
HEAD=5a05d472227d8c14ffa9eedfb516aa4c494108e6
tree=e41f180c8a03ebae611a52dc9a80a908fe6caff8
parents=4ea2ae5e1edf152c0a0a35fcdde6f0a9e99ae7ba 44884446f71c89e25f9a72ac58e4f597db63c1ba
status=(empty), rc=0
old.blob=1ad808b1050a0673d6051069a9954405e0f22423
merge.blob=1ad808b1050a0673d6051069a9954405e0f22423
old.sha256=cd357a95f176db8809b057126da9628ed3e970f8a66bd3feeaa8d955d1230709
merge.sha256=cd357a95f176db8809b057126da9628ed3e970f8a66bd3feeaa8d955d1230709
master.sha256=fa188c1efe944fae03f3d310180fff1a3afd17b38b86adbca04b8f630bccfe0c
byte_equal(old,merge,worktree)=true
source_snapshot_files_including_git=7552
```

Reviewer: Codex, họ OpenAI, thực thi bằng công cụ shell trong phiên hiện tại; review độc lập trên hai trục Spec và Standards/Security, ngưỡng không còn P0/P1/P2. Không suy model/effort hoặc assurance receipt từ chữ ký commit. Snapshot băm cả tệp làm việc và `.git` trước phép đo; mọi bản sao/object/log do reviewer tạo ở ngoài `cay-kho`.

- Kết luận: **KHÔNG PHẢI LỖI**.

### HƯỚNG 2: Q4: lịch sử master không chạm write set hoặc ci.yml

- Giả thuyết: Master đã sửa tệp được bảo vệ, kể cả sửa rồi revert trong lịch sử.
- Lệnh điều phối: `python -B review_evidence/review.py 2`. Lệnh con, cwd, stdout/stderr và rc thật: [h2.log](review_evidence/h2.log).
- Lệnh chính (các cờ vô hiệu external diff/textconv được giữ nguyên trong log):

```sh
git -C cay-kho diff --name-status 7f19424478616b2c5d0a0c7f26839e1d1c41261b 44884446f71c89e25f9a72ac58e4f597db63c1ba -- .claude/dev/ci_dang_ky_test.py .github/workflows/ci.yml
git -C cay-kho rev-list 7f19424478616b2c5d0a0c7f26839e1d1c41261b..44884446f71c89e25f9a72ac58e4f597db63c1ba
# Với từng OID do rev-list trả, harness gọi:
git -C cay-kho diff-tree --no-commit-id --name-status -r <OID>^1 <OID> -- .claude/dev/ci_dang_ky_test.py .github/workflows/ci.yml
```

- Output thật:

```text
ancestor(base,master)=true, rc=0
ancestor(master,merge)=true, rc=0
ancestor(old,merge)=true, rc=0
master_advance_commits=16
git log --full-history base..master -- target ci.yml:
44884446f71c89e25f9a72ac58e4f597db63c1ba Merge pull request #989 from ducthangho/agent/wp972-claude
02bdffa34d6475080a55308b3f45b9006be00712 Merge pull request #988 from ducthangho/claude/gallant-fermat-34kgb9
per_parent_protected_path_deltas=[["44884446f71c89e25f9a72ac58e4f597db63c1ba", "M\t.claude/dev/ci_dang_ky_test.py\n"], ["02bdffa34d6475080a55308b3f45b9006be00712", "M\t.claude/dev/ci_dang_ky_test.py\n"]]
first_parent_protected_path_deltas=[]
git diff base master -- target ci.yml: (empty), rc=0
byte_equal(base,master): target=true, ci.yml=true
Changed paths from master:
M	CHANGELOG.md
M	RELEASE_MANIFEST.json
M	SKILL.md
M	VERSION
A	ops/specs/land-81-ha-cap-r2-pr870-889-896.md
A	ops/specs/land-evidence-l7-r2-moi-do-sau.md
M	scripts/tl.py
M	scripts/tl_core/ops_misc.py
M	scripts/tl_core/profile_env.py
M	scripts/tl_core/profile_mgmt.py
M	scripts/tl_selftest.py
```

`git log --full-history` liệt kê hai merge commit. `diff-tree -r -m` có delta với cha phụ của hai merge do nhánh phụ mang phiên bản cũ; không được đánh đồng với master sửa tệp. Đã kiểm từng commit trong toàn khoảng so với cha 1: cả 16 cạnh đều không có delta ở hai đường dẫn; net diff và so byte base/master cũng rỗng/bằng nhau. Vì vậy không có sửa rồi revert trên đường tiến master hoặc commit riêng của các nhánh nhập vào.

- Kết luận: **KHÔNG PHẢI LỖI**.

### HƯỚNG 3: Diff merge so với master chỉ gồm M1

- Giả thuyết: Merge đưa thêm thay đổi ngoài M1, vượt một tệp/+3/−1 hoặc đổi BAM_GATE_*.
- Lệnh điều phối: `python -B review_evidence/review.py 3`. Lệnh con, cwd, stdout/stderr và rc thật: [h3.log](review_evidence/h3.log).
- Lệnh chính (các cờ vô hiệu external diff/textconv được giữ nguyên trong log):

```sh
git -C cay-kho diff --numstat 44884446f71c89e25f9a72ac58e4f597db63c1ba 5a05d472227d8c14ffa9eedfb516aa4c494108e6
git -C cay-kho diff 44884446f71c89e25f9a72ac58e4f597db63c1ba 5a05d472227d8c14ffa9eedfb516aa4c494108e6
git -C cay-kho diff --check 44884446f71c89e25f9a72ac58e4f597db63c1ba 5a05d472227d8c14ffa9eedfb516aa4c494108e6
```

- Output thật:

```text
3	1	.claude/dev/ci_dang_ky_test.py
packet_diff_matches_git_bytes=true
diff.patch.sha256=c83a1b9aa0cd7e601716d7caa4e2d2e7808da2c11a21b4c1eb4b5e74945de425
git diff --check: (empty), rc=0
BAM_GATE_REGISTRY=89516cf77c3ce734feadf348bfea8180254c67e8e8ec62a48e2f6ea1dc038452 (master == merge)
BAM_GATE_NHANH=fe061a50668af83b6c9b6939f881ba37a30083bc72a27b52c2e02350835d626b (master == merge)

diff --git a/.claude/dev/ci_dang_ky_test.py b/.claude/dev/ci_dang_ky_test.py
index 813668f..1ad808b 100644
--- a/.claude/dev/ci_dang_ky_test.py
+++ b/.claude/dev/ci_dang_ky_test.py
@@ -2123,7 +2123,9 @@ def phan_chung():
     _them("p643-A1-argv-git-push", _g == [["git", "merge-base", "--is-ancestor", _A, _B], _dif])
     _them("p643-A1-argv-git-pr", _h == [_dif])
     with tempfile.TemporaryDirectory() as _k:  # git THẬT: tiến, lùi (force-push), phân kỳ
-        _gk = lambda *a: subprocess.run(["git", "-C", _k, "-c", "user.name=t", "-c", "user.email=t@t", *a],
+        # #923 r3: máy có `commit.gpgsign=true` mà không ký được (sandbox Codex) ⇒ `commit` thoát 128, ca đỏ vì môi trường.
+        _gk = lambda *a: subprocess.run(["git", "-C", _k, "-c", "user.name=t", "-c", "user.email=t@t",
+                                         "-c", "commit.gpgsign=false", *a],
                                         capture_output=True, text=True, check=True).stdout.strip()
         _gk("init", "-q"); _t = pathlib.Path(_k, "ops"); _t.mkdir()
         _c = []
```

- Kết luận: **KHÔNG PHẢI LỖI**.

### HƯỚNG 4: Tree merge đúng kết quả merge tự động

- Giả thuyết: Tree merge chứa giải xung đột hoặc chỉnh tay không có trong hai cha.
- Lệnh điều phối: `python -B review_evidence/review.py 4`. Lệnh con, cwd, stdout/stderr và rc thật: [h4.log](review_evidence/h4.log).
- Lệnh chính (các cờ vô hiệu external diff/textconv được giữ nguyên trong log):

```sh
env GIT_OBJECT_DIRECTORY="/tmp/claude-0/-home-user-tra-luat/6cf1da84-5813-5156-ad6b-b3a2dbd3ab61/scratchpad/rv4/review_evidence/merge-tree-objects" \
    GIT_ALTERNATE_OBJECT_DIRECTORIES="/tmp/claude-0/-home-user-tra-luat/6cf1da84-5813-5156-ad6b-b3a2dbd3ab61/scratchpad/rv4/cay-kho/.git/objects" \
    git -C cay-kho merge-tree --write-tree 44884446f71c89e25f9a72ac58e4f597db63c1ba 4ea2ae5e1edf152c0a0a35fcdde6f0a9e99ae7ba
```

- Output thật:

```text
GIT_OBJECT_DIRECTORY=/tmp/claude-0/-home-user-tra-luat/6cf1da84-5813-5156-ad6b-b3a2dbd3ab61/scratchpad/rv4/review_evidence/merge-tree-objects
GIT_ALTERNATE_OBJECT_DIRECTORIES=/tmp/claude-0/-home-user-tra-luat/6cf1da84-5813-5156-ad6b-b3a2dbd3ab61/scratchpad/rv4/cay-kho/.git/objects
git merge-tree --write-tree 44884446f71c89e25f9a72ac58e4f597db63c1ba 4ea2ae5e1edf152c0a0a35fcdde6f0a9e99ae7ba:
e41f180c8a03ebae611a52dc9a80a908fe6caff8
rc=0
reviewed_tree=e41f180c8a03ebae611a52dc9a80a908fe6caff8
automatic_merge_tree_equal=true
```

Biến object directory được truyền cho riêng tiến trình merge-tree; không tạo object, index, ref hay worktree mới trong `cay-kho`. `merge-tree` rc 0 và chỉ trả đúng tree OID, không có thông báo xung đột.

- Kết luận: **KHÔNG PHẢI LỖI**.

### HƯỚNG 5: Commit message không chứa dấu bỏ qua CI

- Giả thuyết: Message merge chứa nguyên văn token/trailer yêu cầu CI bỏ qua.
- Lệnh điều phối: `python -B review_evidence/review.py 5`. Lệnh con, cwd, stdout/stderr và rc thật: [h5.log](review_evidence/h5.log).
- Lệnh chính (các cờ vô hiệu external diff/textconv được giữ nguyên trong log):

```sh
git -C cay-kho show -s --format=%B 5a05d472227d8c14ffa9eedfb516aa4c494108e6
# Regex được chạy trên toàn bộ stdout, bằng Python re.I; xem h5 trong review.py.
```

- Output thật:

```text
merge commit message:
Merge origin/master vao agent/wp923-g3-claude (#923 r3, spec Q3: base troi lam thu-hoi do)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_015GtxrZWhXPHPfAPL1BXfPB

ci_skip_marker_matches=[]
```

Đã quét message đầy đủ, không phân biệt hoa/thường: năm token ngoặc vuông chuẩn của GitHub và trailer `skip-checks: true` (kể cả không có dấu cách). Không cần gọi mạng cho phép đo này.

- Kết luận: **KHÔNG PHẢI LỖI**.

### HƯỚNG 6: N1: merge xanh, master đỏ đúng _gk commit

- Giả thuyết: Master mang vào đã tự sửa lỗi ký hoặc merge không đạt phản chứng N1.
- Lệnh điều phối: `python -B review_evidence/review.py 6`. Lệnh con, cwd, stdout/stderr và rc thật: [h6.log](review_evidence/h6.log).
- Lệnh chính (các cờ vô hiệu external diff/textconv được giữ nguyên trong log):

```sh
# Chạy cùng lệnh này với cwd lần lượt là review_evidence/copies/head và copies/master:
env GIT_CONFIG_GLOBAL=/tmp/claude-0/-home-user-tra-luat/6cf1da84-5813-5156-ad6b-b3a2dbd3ab61/scratchpad/rv4/gitcfg-ky python .claude/dev/ci_dang_ky_test.py
```

- Output thật:

```text
gitcfg-ky (absolute path): /tmp/claude-0/-home-user-tra-luat/6cf1da84-5813-5156-ad6b-b3a2dbd3ab61/scratchpad/rv4/gitcfg-ky
[commit]
	gpgsign = true
[gpg]
	program = /bin/false

N1 reviewed_sha (tail):
ĐỘT BIẾN p748-manh-gop-thieu-gop: ĐỎ đúng
ĐỘT BIẾN p748-manh-gop-thieu-phan-hoach: ĐỎ đúng
ĐỘT BIẾN p748-manh-gop-bo-bien-manh: ĐỎ đúng
ĐỘT BIẾN p748-manh-gop-bo-gop-khoi-needs: ĐỎ đúng
ĐỘT BIẾN p643-A4-N-1: ĐỎ đúng
ĐỘT BIẾN p643-A4-bo-env: ĐỎ đúng
ĐỘT BIẾN p643-A4-hai-buoc-registry: ĐỎ đúng
PHẢN CHỨNG: 1070/1070 đỏ đúng
TỔNG: ĐẠT
rc=0

N1 master (stderr tail):
    raise SystemExit(main())
                     ~~~~^^
  File "/tmp/claude-0/-home-user-tra-luat/6cf1da84-5813-5156-ad6b-b3a2dbd3ab61/scratchpad/rv4/review_evidence/copies/master/.claude/dev/ci_dang_ky_test.py", line 2430, in main
    ok = not loi and tren_cay == trong_so and phan_chung()
                                              ~~~~~~~~~~^^
  File "/tmp/claude-0/-home-user-tra-luat/6cf1da84-5813-5156-ad6b-b3a2dbd3ab61/scratchpad/rv4/review_evidence/copies/master/.claude/dev/ci_dang_ky_test.py", line 2132, in phan_chung
    pathlib.Path(_k, _f).write_text(str(_i)); _gk("add", "-A"); _gk("commit", "-qm", str(_i)); _c.append(_gk("rev-parse", "HEAD"))
                                                                ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/claude-0/-home-user-tra-luat/6cf1da84-5813-5156-ad6b-b3a2dbd3ab61/scratchpad/rv4/review_evidence/copies/master/.claude/dev/ci_dang_ky_test.py", line 2126, in <lambda>
    _gk = lambda *a: subprocess.run(["git", "-C", _k, "-c", "user.name=t", "-c", "user.email=t@t", *a],
                     ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                    capture_output=True, text=True, check=True).stdout.strip()
                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.13/subprocess.py", line 578, in run
    raise CalledProcessError(retcode, process.args,
                             output=stdout, stderr=stderr)
subprocess.CalledProcessError: Command '['git', '-C', '/tmp/tmplix9613z', '-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-qm', '0']' returned non-zero exit status 128.
rc=1
```

Hai bản sao local độc lập, detached tại đúng OID, không dùng worktree của nguồn. Chỉ cấu hình `core.autocrlf=false` và `core.abbrev=7` trong bản sao; không đổi cấu hình ký của bản sao hay của máy. N1 dùng cùng đường dẫn global tuyệt đối cho cả hai cây. Log đầy đủ và rc từng lượt: `n1-head.json`, `n1-master.json`.

- Kết luận: **KHÔNG PHẢI LỖI**.

### HƯỚNG 7: N2 trên merge trong môi trường kế thừa và global rỗng

- Giả thuyết: Merge chỉ xanh khi ép cấu hình Git và thất bại với lệnh N2 nguyên trạng.
- Lệnh điều phối: `python -B review_evidence/review.py 7`. Lệnh con, cwd, stdout/stderr và rc thật: [h7.log](review_evidence/h7.log).
- Lệnh chính (các cờ vô hiệu external diff/textconv được giữ nguyên trong log):

```sh
# cwd: review_evidence/copies/head
python .claude/dev/ci_dang_ky_test.py
env GIT_CONFIG_GLOBAL=/dev/null python .claude/dev/ci_dang_ky_test.py
```

- Output thật:

```text
Inherited signing config (read-only):
file:/root/.gitconfig	gpg.format ssh
file:/root/.gitconfig	gpg.ssh.program /tmp/code-sign
file:/root/.gitconfig	commit.gpgsign true
file:.git/config	core.abbrev 7
inherited_GIT_CONFIG_GLOBAL_present=false

N2 python .claude/dev/ci_dang_ky_test.py (inherited, tail):
ĐỘT BIẾN p748-manh-gop-thieu-gop: ĐỎ đúng
ĐỘT BIẾN p748-manh-gop-thieu-phan-hoach: ĐỎ đúng
ĐỘT BIẾN p748-manh-gop-bo-bien-manh: ĐỎ đúng
ĐỘT BIẾN p748-manh-gop-bo-gop-khoi-needs: ĐỎ đúng
ĐỘT BIẾN p643-A4-N-1: ĐỎ đúng
ĐỘT BIẾN p643-A4-bo-env: ĐỎ đúng
ĐỘT BIẾN p643-A4-hai-buoc-registry: ĐỎ đúng
PHẢN CHỨNG: 1070/1070 đỏ đúng
TỔNG: ĐẠT
rc=0

N2 GIT_CONFIG_GLOBAL=/dev/null (tail):
ĐỘT BIẾN p748-manh-gop-thieu-gop: ĐỎ đúng
ĐỘT BIẾN p748-manh-gop-thieu-phan-hoach: ĐỎ đúng
ĐỘT BIẾN p748-manh-gop-bo-bien-manh: ĐỎ đúng
ĐỘT BIẾN p748-manh-gop-bo-gop-khoi-needs: ĐỎ đúng
ĐỘT BIẾN p643-A4-N-1: ĐỎ đúng
ĐỘT BIẾN p643-A4-bo-env: ĐỎ đúng
ĐỘT BIẾN p643-A4-hai-buoc-registry: ĐỎ đúng
PHẢN CHỨNG: 1070/1070 đỏ đúng
TỔNG: ĐẠT
rc=0
```

Lượt N2 nguyên trạng dùng đúng `python .claude/dev/ci_dang_ky_test.py`, không thêm biến môi trường, không dùng `--chay`. Máy có ký SSH global qua `/tmp/code-sign`; N1 đã xác minh fixture merge chặn ký, nên lệnh N2 không cần gọi signer đó. Đo thêm global rỗng theo chỉ thị, tách riêng khỏi kết quả kế thừa. Log đầy đủ: `n2-head-inherited.json`, `n2-head-neutral.json`.

- Kết luận: **KHÔNG PHẢI LỖI**.

### HƯỚNG 8: Master có ghim băm nguyên byte của tệp đang sửa không?

- Giả thuyết: Tệp mới/đổi từ master ghim blob OID hoặc SHA-256 của ci_dang_ky_test.py, làm M1 phá gate.
- Lệnh điều phối: `python -B review_evidence/review.py 8`. Lệnh con, cwd, stdout/stderr và rc thật: [h8.log](review_evidence/h8.log).
- Lệnh chính (các cờ vô hiệu external diff/textconv được giữ nguyên trong log):

```sh
git -C cay-kho diff --name-only -z 7f19424478616b2c5d0a0c7f26839e1d1c41261b 44884446f71c89e25f9a72ac58e4f597db63c1ba
# Với từng đường dẫn trả về, đọc nguyên blob bằng:
git -C cay-kho show 44884446f71c89e25f9a72ac58e4f597db63c1ba:<path>
# Quét OID/SHA-256 đầy đủ trong review.py h8, token hex viết tắt trong finalize.py.
```

- Output thật:

```text
Changed files scanned as complete blobs, not only added lines: 11
CHANGELOG.md
RELEASE_MANIFEST.json
SKILL.md
VERSION
ops/specs/land-81-ha-cap-r2-pr870-889-896.md
ops/specs/land-evidence-l7-r2-moi-do-sau.md
scripts/tl.py
scripts/tl_core/ops_misc.py
scripts/tl_core/profile_env.py
scripts/tl_core/profile_mgmt.py
scripts/tl_selftest.py

reviewed.blob_oid=1ad808b1050a0673d6051069a9954405e0f22423
reviewed.sha256=cd357a95f176db8809b057126da9628ed3e970f8a66bd3feeaa8d955d1230709
master.blob_oid=813668f08437e3930e92cb96c6032452b6f043f4
master.sha256=fa188c1efe944fae03f3d310180fff1a3afd17b38b86adbca04b8f630bccfe0c
exact_hash_pin_hits=[]
manifest_entries_for_target_or_ci=[]
Filename references (full changed files):
CHANGELOG.md:1609: `.claude/dev/ci_dang_ky_test.py`; khối ĐÃ RÚT (+13 kể dòng trống) đầu `ops/RUNBOOK_TACH_DANH_TINH_GITHUB.md`.
CHANGELOG.md:4297: | `.claude/dev/ci_dang_ky_test.py` | 0 | `PHẢN CHỨNG: 51/51 đỏ đúng` · `TỔNG: ĐẠT` |
CHANGELOG.md:4453: Nối vào `ci.yml` và đăng ký ở `ci_dang_ky_test.py` (22/22) — guard không nằm trên đường TỰ ĐỘNG
CHANGELOG.md:4557: ba con số trên). Khai thẳng: **không workflow nào chạy cổng ấy** — `ci_dang_ky_test.py` chỉ
```

Quét toàn bộ byte của 11 tệp mới/đổi ở master, cả băm tệp trước M1 và băm reviewed SHA; không tìm thấy pin. `RELEASE_MANIFEST.json` chỉ kê tệp gói phát hành, không kê tệp CI này hoặc `ci.yml`. Các nhắc tên trong CHANGELOG là lịch sử có sẵn. Chi tiết scan ở `h8-scan.json`; diff master để kiểm thủ công ở `master-advance.patch`.

- Kết luận: **KHÔNG PHẢI LỖI**.

### HƯỚNG 9: Hàng rào SHA/tree và nguồn read-only sau review

- Giả thuyết: Các phép đo làm đổi checkout/object/ref/config nguồn hoặc head/spec trôi.
- Lệnh điều phối: `python -B review_evidence/review.py 9`. Lệnh con, cwd, stdout/stderr và rc thật: [h9.log](review_evidence/h9.log).
- Lệnh chính (các cờ vô hiệu external diff/textconv được giữ nguyên trong log):

```sh
git -C cay-kho rev-parse HEAD HEAD^{tree}
git -C cay-kho status --porcelain=v1 --untracked-files=all --ignored=matching
git -C cay-kho diff --binary
git -C cay-kho diff --cached --binary
sha256sum SPEC.md
# So snapshot SHA-256 mọi tệp kể cả .git: review.py h9.
```

- Output thật:

```text
source_files_before=7552
source_files_after=7552
source_content_delta_including_git=[]
5a05d472227d8c14ffa9eedfb516aa4c494108e6
e41f180c8a03ebae611a52dc9a80a908fe6caff8
git status (tracked/untracked/ignored): (empty), rc=0
git diff --binary: (empty), rc=0
git diff --cached --binary: (empty), rc=0
0a694a96f02fb02c01e7707d725591dae5f4455464a77e90ca5fd22435eb1ea5  SPEC.md
```

Đối chiếu SHA-256 của mọi tệp thường và đích symlink trong `cay-kho`, gồm cả `.git`, ở đầu/cuối; không quan sát delta. Snapshot chỉ chứng minh hai mốc bằng nhau, không phải bằng chứng lịch sử mọi syscall. Sandbox thực tế là workspace-write; reviewer giữ nguồn read-only bằng phạm vi lệnh, chạy code và ghi mọi object tạm trong `review_evidence/`.

- Kết luận: **KHÔNG PHẢI LỖI**.

## FINDINGS

Không phát hiện P0/P1/P2/P3 trong phạm vi xác minh merge này; 0 finding còn mở. **approve** cho exact `reviewed_sha` nêu trên. Căn cứ: H1–H5 xác nhận bytes/phạm vi/Q4/tree/message; H6 tái hiện N1 hai chiều; H7 đạt N2; H8 không có pin băm; H9 giữ nguyên nguồn.

Đối chiếu bổ sung: `python -B review_evidence/finalize.py` (lệnh và dữ liệu ở `review_evidence/followup-audit.json`), output thật:

```text
abbreviated_hash_pin_hits_7_to_64_hex=[]
changelog_target_references: base=4, master=4, texts_equal=true
head_copy_status=(empty), rc=0; target bytes unchanged
master_copy_status=(empty), rc=0; target bytes unchanged
two master merge commits: target equals parent1 and base; differs only from parent2
```

## GIỚI HẠN

- N1 master là **failed có chủ đích**: Python rc 1, Git fixture commit rc 128. N1 merge và hai lượt N2 merge là **passed**, đều rc 0 và `TỔNG: ĐẠT`.
- CI/check run của PR #992: **not_run / KHÔNG ĐO ĐƯỢC** do chỉ thị cấm mạng. Không suy kết quả cục bộ thành CI remote xanh hay quyền merge/land.
- Lượt này xác minh merge theo 8 mục được giao; không chạy lại full `tl.py --selftest`, doctrine-scan hay bare Ruff lint (**not_run**), không coi các kiểm tra đó là đã đạt trên merge. `git diff --check` đã chạy, rc 0.
- Provider họ OpenAI theo phiên được giao, dùng shell trực tiếp. Không có chứng thực độc lập model/effort hoặc receipt launcher trong review bundle; verdict này không tự cấp state/assurance receipt. Không gọi reviewer khác.
- Hai lần assertion ban đầu của harness H2 dùng điều kiện lịch sử quá chặt (đòi log/all-parent diff rỗng). Đã phân biệt rõ cha 1/cha 2, đo lại mọi cạnh cha 1 và giữ output all-parent trong H2; lỗi giả định harness không phải finding của mã. `h2-error.json` giữ evidence lượt assertion thứ hai.

