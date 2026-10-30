verdict: approve
reviewed_sha: 4ea2ae5e1edf152c0a0a35fcdde6f0a9e99ae7ba
reviewed_tree: 27cb43066ac33e8ae7150e9fc08ae974803b021d
base_sha: 7f19424478616b2c5d0a0c7f26839e1d1c41261b
spec_sha256: 0a694a96f02fb02c01e7707d725591dae5f4455464a77e90ca5fd22435eb1ea5

Reviewer: Codex, họ OpenAI; phiên review độc lập, chỉ đọc cây executor. Hai trục: Spec và Standards/Security. Ngưỡng áp dụng: không còn P0/P1/P2.

Mọi lệnh bên dưới đã chạy local; `review_evidence/*.log` giữ command, cwd, output và rc, `*.json` giữ kết quả có cấu trúc. Các script review và bản sao nằm ngoài `cay-kho`. Harness đặt `GIT_OPTIONAL_LOCKS=0` và `PYTHONDONTWRITEBYTECODE=1`; không đổi cấu hình ký trừ các phép thử được ghi rõ. Hàng rào SHA/tree/status/SPEC được kiểm lại sau toàn bộ phép đo; xem `review_evidence/final-source-fence.log`.

## BẢNG SĂN

### HƯỚNG 1: Neo, phạm vi diff và khác biệt AST

- Giả thuyết: patch sửa ngoài write set hoặc đổi hành vi khác ngoài đối số `_gk`.
- Lệnh: `python -B review_evidence/h1.py`; script đọc blob bằng `git -C cay-kho show <SHA>:.claude/dev/ci_dang_ky_test.py`, so AST bỏ vị trí dòng; xem mã script và log `review_evidence/h1-*.log`.
- Output thật:

```text
0a694a96f02fb02c01e7707d725591dae5f4455464a77e90ca5fd22435eb1ea5  SPEC.md
4ea2ae5e1edf152c0a0a35fcdde6f0a9e99ae7ba
27cb43066ac33e8ae7150e9fc08ae974803b021d
file:/root/.gitconfig	gpg.format ssh
file:/root/.gitconfig	gpg.ssh.program /tmp/code-sign
file:/root/.gitconfig	commit.gpgsign true
3	1	.claude/dev/ci_dang_ky_test.py
packet_diff_matches_git=true
working_target_matches_HEAD=true
AST_delta=one _gk argv list inserts ['-c', 'commit.gpgsign=false'] before *a
AST_equal_after_removing_exact_insertion=true
changed_files=1, added=3, removed=1
```

- `diff.patch` trùng byte với `git diff <base> <head>`; bản làm việc của tệp trùng blob HEAD. Hai AST bằng nhau sau khi gỡ đúng hai phần tử vừa thêm khỏi list argv của `_gk`; chú thích không thuộc AST. Đã lưu băm toàn bộ tracked files để đối chiếu cuối lượt.
- Kết luận: **KHÔNG PHẢI LỖI**. Đúng một tệp, +3/−1, dưới trần 15 dòng thêm; neo và SPEC khớp.

### HƯỚNG 2: N1 độc lập hai chiều trên clone tạm

- Giả thuyết: cấu hình phản chứng không làm base đỏ đúng `_gk commit`, hoặc head chưa thật sự xanh.
- Dựng clone bằng `python -B review_evidence/setup_copies.py`: `git clone --quiet --no-hardlinks --no-checkout <cay-kho tuyệt đối> <copies/base|head>`, `git config core.abbrev 7`, checkout detached đúng hai OID; mọi bước rc=0. Lệnh và output đầy đủ ở `review_evidence/setup-*.log`.
- Lệnh đo: `python -B review_evidence/h2.py`, thực thi hai lệnh sau trong từng clone:

```sh
env GIT_CONFIG_GLOBAL=/tmp/claude-0/-home-user-tra-luat/6cf1da84-5813-5156-ad6b-b3a2dbd3ab61/scratchpad/rv3/gitcfg-ky python .claude/dev/ci_dang_ky_test.py
env GIT_CONFIG_GLOBAL=/tmp/claude-0/-home-user-tra-luat/6cf1da84-5813-5156-ad6b-b3a2dbd3ab61/scratchpad/rv3/gitcfg-ky python .claude/dev/ci_dang_ky_test.py
```

- Output base (trích cuối log `review_evidence/h2-n1-base.log`):

```text
  File "/tmp/claude-0/-home-user-tra-luat/6cf1da84-5813-5156-ad6b-b3a2dbd3ab61/scratchpad/rv3/review_evidence/copies/base/.claude/dev/ci_dang_ky_test.py", line 2445, in <module>
    raise SystemExit(main())
                     ~~~~^^
  File "/tmp/claude-0/-home-user-tra-luat/6cf1da84-5813-5156-ad6b-b3a2dbd3ab61/scratchpad/rv3/review_evidence/copies/base/.claude/dev/ci_dang_ky_test.py", line 2430, in main
    ok = not loi and tren_cay == trong_so and phan_chung()
                                              ~~~~~~~~~~^^
  File "/tmp/claude-0/-home-user-tra-luat/6cf1da84-5813-5156-ad6b-b3a2dbd3ab61/scratchpad/rv3/review_evidence/copies/base/.claude/dev/ci_dang_ky_test.py", line 2132, in phan_chung
    pathlib.Path(_k, _f).write_text(str(_i)); _gk("add", "-A"); _gk("commit", "-qm", str(_i)); _c.append(_gk("rev-parse", "HEAD"))
                                                                ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/claude-0/-home-user-tra-luat/6cf1da84-5813-5156-ad6b-b3a2dbd3ab61/scratchpad/rv3/review_evidence/copies/base/.claude/dev/ci_dang_ky_test.py", line 2126, in <lambda>
    _gk = lambda *a: subprocess.run(["git", "-C", _k, "-c", "user.name=t", "-c", "user.email=t@t", *a],
                     ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                    capture_output=True, text=True, check=True).stdout.strip()
                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.13/subprocess.py", line 578, in run
    raise CalledProcessError(retcode, process.args,
                             output=stdout, stderr=stderr)
subprocess.CalledProcessError: Command '['git', '-C', '/tmp/tmpr65kodq0', '-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-qm', '0']' returned non-zero exit status 128.
rc=1
```

- Output head (trích cuối log `review_evidence/h2-n1-head.log`):

```text
ĐỘT BIẾN p748-manh-gop-thieu-manh: ĐỎ đúng
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

- Cấu hình nền đã ghi ở H1: global `/root/.gitconfig` bật ký SSH và `commit.gpgsign=true`. N1 dùng **đường dẫn tuyệt đối** tới `gitcfg-ky`, thay global config bằng `commit.gpgsign=true` và `gpg.program=/bin/false` cho cả hai clone.
- Kết luận: **KHÔNG PHẢI LỖI**. Base đỏ đúng commit đầu tiên của `_gk` với rc 128; head rc 0 và `TỔNG: ĐẠT`.

### HƯỚNG 3: Quét toàn tệp, lời gọi gián tiếp và `tag.gpgsign`

- Giả thuyết: còn lệnh ghi commit/tag khác hoặc chuỗi workflow/fixture có thể gọi ký mà executor bỏ sót.
- Lệnh: `python -B review_evidence/h3.py`; script chạy `rg -n` với **đường dẫn tuyệt đối tới tệp**, duyệt mọi AST call của `subprocess.*`, `chay`, `_git`, `_gk`, `_chay_co_lap`, `os.system/popen`, `eval/exec`; lưu `h3-text-scan.log`, `h3-ast-calls.log`. Đọc thêm các thân hàm và chuỗi mã Python được truyền cho subprocess ở 1000–1065, 1368–1390, 1930–1970, 2250–2310.
- Output AST helper:

```text
HELPER_CALLS={"_git": [["'init'", "'-q'"], ["'add'", "'-f'", "'.codex/hooks/x_test.py'"]], "_gk": [["'init'", "'-q'"], ["'checkout'", "'-q'", "_c[0]"], ["'add'", "'-A'"], ["'commit'", "'-qm'", "str(_i)"], ["'rev-parse'", "'HEAD'"]]}
```

- Phân loại toàn bộ chỗ Git: 98 `check-ignore`; 838 `merge-base --is-ancestor`; 840 và 2122 `diff` (2122 là argv mong đợi của fake); 1332 là helper `_git` chỉ được gọi `init` và `add -f`; 2127–2134 `_gk` gọi `init`, `checkout`, `add`, `commit`, `rev-parse`. Các chuỗi 801–802/1190 là `git config` để so workflow; 1669 `git rev-parse HEAD` là chuỗi đột biến workflow. Chuỗi subprocess Python còn lại là fixture in kết quả, kiểm env, timeout/con cháu, hoặc tự gọi `--chay` với tham số sai để dừng trước chạy test thật. Không thấy `tag`, `tag -s`, `commit-tree`, merge tạo commit, alias ghi Git hoặc shell thực thi workflow trong đường đo này.
- Kiểm động bổ sung: bật **cả** `commit.gpgsign=true` và `tag.gpgsign=true`, signer `/bin/false`; dùng Python audit hook ghi mọi Git subprocess của tiến trình đang review. Lệnh thật:

```sh
env GIT_CONFIG_GLOBAL=/tmp/claude-0/-home-user-tra-luat/6cf1da84-5813-5156-ad6b-b3a2dbd3ab61/scratchpad/rv3/review_evidence/gitcfg-signing-and-tags python /tmp/claude-0/-home-user-tra-luat/6cf1da84-5813-5156-ad6b-b3a2dbd3ab61/scratchpad/rv3/review_evidence/h3_trace.py /tmp/claude-0/-home-user-tra-luat/6cf1da84-5813-5156-ad6b-b3a2dbd3ab61/scratchpad/rv3/review_evidence/copies/head/.claude/dev/ci_dang_ky_test.py /tmp/claude-0/-home-user-tra-luat/6cf1da84-5813-5156-ad6b-b3a2dbd3ab61/scratchpad/rv3/review_evidence/h3-subprocess-trace.json
```

- Output thật (`review_evidence/h3-traced-head.log`; argv đầy đủ ở `h3-subprocess-trace.json`):

```text
ĐỘT BIẾN p643-A4-hai-buoc-registry: ĐỎ đúng
PHẢN CHỨNG: 1070/1070 đỏ đúng
TỔNG: ĐẠT
AUDIT_GIT_VERBS={"add": 4, "check-ignore": 5, "checkout": 1, "commit": 3, "diff": 2, "init": 2, "merge-base": 3, "rev-parse": 3}
AUDIT_EXECUTABLES={"/root/.local/bin/actionlint": 6, "/usr/bin/python": 11, "actionlint-VANG": 1, "git": 23}
rc=0
```

- Trace thấy đúng 3 `commit`, cả 3 có `-c commit.gpgsign=false`; không thấy `tag` hay lệnh tạo commit khác. Audit hook đo tiến trình cha; các child Python đã được kiểm nội dung tĩnh, không tuyên bố trace tự bao phủ các đường chưa chạy.
- Kết luận: **KHÔNG PHẢI LỖI**. Không có fixture commit cùng hình dạng bị bỏ sót. Chưa cần chặn `tag.gpgsign` vì tệp không tạo tag; cấu hình ký tag cũng không làm head đỏ.

### HƯỚNG 4: Phản chứng bằng đột biến gỡ chốt và ép ký

- Giả thuyết: N1 xanh giả, vẫn xanh khi gỡ chặn ký hoặc đổi thành ký bắt buộc.
- Lệnh: `python -B review_evidence/h4.py`; chỉ sửa **bản sao** `review_evidence/copies/head/.claude/dev/ci_dang_ky_test.py`, xác minh neo đúng một lần, lần lượt (a) gỡ chính `"-c", "commit.gpgsign=false", ` và (b) đổi `false` thành `true`. Lưu diff từng đột biến bằng `git -C <clone> diff -- .claude/dev/ci_dang_ky_test.py` ở `h4-diff-*.log`. Mỗi biến thể chạy:

```sh
env GIT_CONFIG_GLOBAL=/tmp/claude-0/-home-user-tra-luat/6cf1da84-5813-5156-ad6b-b3a2dbd3ab61/scratchpad/rv3/gitcfg-ky python .claude/dev/ci_dang_ky_test.py
```

- Output thật (trích cuối `h4-mutant-*.log`):

```text
remove:
                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.13/subprocess.py", line 578, in run
    raise CalledProcessError(retcode, process.args,
                             output=stdout, stderr=stderr)
subprocess.CalledProcessError: Command '['git', '-C', '/tmp/tmp7vfkegl7', '-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-qm', '0']' returned non-zero exit status 128.
rc=1
force-true:
                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.13/subprocess.py", line 578, in run
    raise CalledProcessError(retcode, process.args,
                             output=stdout, stderr=stderr)
subprocess.CalledProcessError: Command '['git', '-C', '/tmp/tmplmxssych', '-c', 'user.name=t', '-c', 'user.email=t@t', '-c', 'commit.gpgsign=true', 'commit', '-qm', '0']' returned non-zero exit status 128.
rc=1
```

- Khôi phục nguyên byte head trong `finally`; `git -C <clone> status --porcelain=v1 --untracked-files=all` rc 0, output rỗng (`h4-restored-status.log`). Không commit hoặc ghi vào `cay-kho`.
- Kết luận: **KHÔNG PHẢI LỖI**. Cả 2/2 đột biến bị giết đúng `_gk commit` rc 128; đối chiếu H2 cho thấy bản head nguyên vẹn xanh. Phản chứng phân biệt được có/không có chốt.

### HƯỚNG 5: N2, hằng băm và các ghim job/ci.yml

- Giả thuyết: bản vá đổi `BAM_GATE_*`, cấu hình CI hoặc phép băm, hay làm hỏng hành vi khi không có cấu hình ký phản chứng.
- Lệnh: `python -B review_evidence/h5.py`; script gọi `python review_evidence/h5_hashes.py <clone>` ở **cả base và head**, lấy hằng, băm bytes `ci.yml`, gọi chính hai hàm băm lên YAML thật và băm AST của các hàm liên quan.
- Output thật ở cả hai clone **giống hệt nhau** (`review_evidence/h5-hashes-{base,head}.log`):

```text
ci.yml.sha256=ce9a3ec0f777a5165477c73b8fc9b9c098e8c3a9f5517c7499649670e84913fb
BAM_GATE_REGISTRY=89516cf77c3ce734feadf348bfea8180254c67e8e8ec62a48e2f6ea1dc038452
BAM_GATE_NHANH=fe061a50668af83b6c9b6939f881ba37a30083bc72a27b52c2e02350835d626b
bam_gate_registry(ci.yml)=89516cf77c3ce734feadf348bfea8180254c67e8e8ec62a48e2f6ea1dc038452 MATCH
bam_gate_nhanh(ci.yml)=fe061a50668af83b6c9b6939f881ba37a30083bc72a27b52c2e02350835d626b MATCH
bam_gate_registry.AST.sha256=130c6b661fe290f0f551f556b64b4ba9c254cd8aba0a7901561b3ce1a98a3fbf
bam_gate_nhanh.AST.sha256=ead0728e8eb1f40bc932f48b74b7167a69be59c7b55a92c6f88d3a6d7c913467
loi_gate_nhanh.AST.sha256=52d03514521efd61cee7079ab55a0894155a5294050e9bab7824c651de1e1d41
loi_vung_thiet_lap.AST.sha256=a2ab553c65937d07fd2ddfebd8bb5bd5144b24968e1b839e14963f9eef7cb258
```

- N2 trong môi trường kế thừa: `cd <copies/base|head>` rồi `python .claude/dev/ci_dang_ky_test.py`, **không đặt biến cấu hình Git**. Output cuối:

```text
base:
    raise CalledProcessError(retcode, process.args,
                             output=stdout, stderr=stderr)
subprocess.CalledProcessError: Command '['git', '-C', '/tmp/tmpyrt_c3al', '-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-qm', '0']' returned non-zero exit status 128.
rc=1
head:
ĐỘT BIẾN p643-A4-hai-buoc-registry: ĐỎ đúng
PHẢN CHỨNG: 1070/1070 đỏ đúng
TỔNG: ĐẠT
rc=0
```

- Vì nền máy review bật ký toàn cục (H1), đo bổ sung hai cây với global rỗng, không thay `~/.gitconfig`: `GIT_CONFIG_GLOBAL=/dev/null python .claude/dev/ci_dang_ky_test.py`. Đây là phép đối chứng **có chuẩn hóa môi trường**, không đánh đồng với lệnh nguyên trạng ở trên. Output cuối (`h5-n2-neutral-*.log`):

```text
base:
ĐỘT BIẾN p643-A4-hai-buoc-registry: ĐỎ đúng
PHẢN CHỨNG: 1070/1070 đỏ đúng
TỔNG: ĐẠT
rc=0
head:
ĐỘT BIẾN p643-A4-hai-buoc-registry: ĐỎ đúng
PHẢN CHỨNG: 1070/1070 đỏ đúng
TỔNG: ĐẠT
rc=0
```

- H1 đã chứng minh toàn bộ AST ngoài list argv của `_gk` không đổi; phép đo trực tiếp ở đây xác nhận hai ghim và các hàm băm/consumer giữ nguyên. Không có diff workflow.
- Kết luận: **KHÔNG PHẢI LỖI**. Head đạt N2 nguyên trạng; base/head đều đạt khi bỏ ảnh hưởng global signing. Base nguyên trạng đỏ là đúng lỗi môi trường mà packet đang sửa, không phải hồi quy do diff.

### HƯỚNG 6: Tính đúng và idiom của chú thích mới

- Giả thuyết: chú thích sai sự thật, không có mốc packet hoặc tạo khẳng định trạng thái hiện tại dễ cũ.
- Lệnh: `python -B review_evidence/h6.py`; `tokenize` so comment của hai blob, cộng `nl -ba ... | sed -n '2120,2137p'` và `rg -n '# #643|# #668|# #705|# #923' cay-kho/.claude/dev/ci_dang_ky_test.py` (đường dẫn tường minh). Output đầy đủ ở `h6-comment-context.log`.
- Output thật từ tokenizer:

```text
added_comment_count=1
added_comment_line=2126
# #923 r3: máy có `commit.gpgsign=true` mà không ký được (sandbox Codex) ⇒ `commit` thoát 128, ca đỏ vì môi trường.
removed_comments=0
```

- Nội dung là điều kiện gây lỗi được ghi mốc `#923 r3`, không tuyên bố tình trạng hiện tại của kho. H2 đã đo base thoát 128 khi commit trong cấu hình ký không dùng được; H5 đo riêng môi trường SSH của máy review. Tiền tố `# #<issue>` và giải thích phản chứng ngay trước fixture cùng idiom các mốc #643/#668/#705 trong tệp.
- Kết luận: **KHÔNG PHẢI LỖI**. Một chú thích mới, đúng nguyên nhân đã tái hiện, có mốc bền và không làm đổi code ngoài phạm vi M1.

### HƯỚNG 7: N3, N4 local và tính toàn vẹn của cổng

- Giả thuyết: diff sạch về AST nhưng vi phạm doctrine/whitespace hoặc gây hồi quy selftest trên exact head.
- Lệnh: `python -B review_evidence/h7.py`; thực thi trong clone head sau khi H4 khôi phục sạch:

```sh
python .claude/dev/packet_loop.py doctrine-scan --root .
git -C /tmp/claude-0/-home-user-tra-luat/6cf1da84-5813-5156-ad6b-b3a2dbd3ab61/scratchpad/rv3/cay-kho diff --check 7f19424478616b2c5d0a0c7f26839e1d1c41261b 4ea2ae5e1edf152c0a0a35fcdde6f0a9e99ae7ba
git -C /tmp/claude-0/-home-user-tra-luat/6cf1da84-5813-5156-ad6b-b3a2dbd3ab61/scratchpad/rv3/cay-kho diff --check
git -C /tmp/claude-0/-home-user-tra-luat/6cf1da84-5813-5156-ad6b-b3a2dbd3ab61/scratchpad/rv3/review_evidence/copies/head rev-parse HEAD 'HEAD^{tree}'
env TL_SELFTEST_ALLOW_NET=0 python scripts/tl.py --selftest
```

- Output thật:

```text
doctrine-scan:
doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine
rc=0
git diff --check <base> <head>:
(output rỗng)
rc=0
git diff --check (cây nguồn):
(output rỗng)
rc=0
exact head/tree:
4ea2ae5e1edf152c0a0a35fcdde6f0a9e99ae7ba
27cb43066ac33e8ae7150e9fc08ae974803b021d
selftest (trích cuối):
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
== tl selftest 1729/1731 ==
rc=1
```

- Log đầy đủ: `review_evidence/h7-*.log`. `TL_SELFTEST_ALLOW_NET=0` buộc dùng cơ chế selftest offline có sẵn, không đổi mã tracked. Chỉ chạy bản sao. Lượt kế thừa đã kích hoạt signer nền thử kết nối loopback và bị sandbox chặn; xem điều tra H9, không coi đây là lượt hoàn toàn không có nỗ lực kết nối.
- Kết luận: **KHÔNG PHẢI LỖI** sau đối chứng H9. N3 đạt; N4 nguyên trạng đo được `1729/1731` (failed). H9 xác minh hai ca đỏ có sẵn trên base, và N4 đầy đủ với global rỗng đạt `1731/1731`; không ghi lượt raw này thành pass.
- Phần **CI PR/check run của N4: KHÔNG ĐO ĐƯỢC / not_run**. Packet chỉ cấp dữ liệu offline và cấm mạng; không coi tuyên bố executor là xác minh độc lập CI, không suy phép đo local thành quyền merge/land.

### HƯỚNG 8: Hàng rào exact SHA và bảo toàn cây được review

- Giả thuyết: phép đo chạm cây executor hoặc HEAD/SPEC trôi trong lượt review.
- Lệnh: `python -B review_evidence/h8.py`; so lại SHA-256 từng tracked file với snapshot đầu H1; chạy `git -C cay-kho rev-parse HEAD 'HEAD^{tree}'`, `git -C cay-kho status --porcelain=v1 --untracked-files=all --ignored=matching`, `git -C cay-kho diff --binary`, `git -C cay-kho diff --cached --binary`, `sha256sum SPEC.md`.
- Output thật (`h8-source-fence.log`, `h8-source-integrity.log`):

```text
tracked_paths_before=7356
tracked_paths_after=7356
tracked_content_changes=0
4ea2ae5e1edf152c0a0a35fcdde6f0a9e99ae7ba
27cb43066ac33e8ae7150e9fc08ae974803b021d
0a694a96f02fb02c01e7707d725591dae5f4455464a77e90ca5fd22435eb1ea5  SPEC.md
```

- Status kể cả ignored/untracked, diff và staged diff đều output rỗng. Snapshot đầu có băm tracked; không có băm ignored/untracked đầu lượt, nên không suy snapshot này thành chứng minh lịch sử mọi thao tác. Mọi thực thi code và đột biến do reviewer tạo đều ở `review_evidence/copies/`, ngoài `cay-kho`.
- Kết luận: **KHÔNG PHẢI LỖI**. Neo giữ nguyên; 7.356 tracked paths giữ nguyên nội dung; không quan sát thấy delta ở cây được review.

### HƯỚNG 9: Phân rã selftest đỏ, đối chứng base và xác minh N4 đã chuẩn hóa

- Giả thuyết: `1729/1731` ở H7 là hồi quy do diff `_gk`, hoặc nguyên nhân ký global vẫn còn ngoài write set.
- Đọc nguyên hàm `_c226_nguong_l2_troi_theo_abbrev_va_ci_ghim` và `_c268_l2_trichotomy_theo_trang_thai_object` trong `scripts/tl_selftest.py:26947–26999` và `28552–28602`. Cả hai có helper Git tạo commit mà không chặn ký; tệp này không đổi giữa base/head (H1). Không sửa mã các helper này.
- Lệnh đối chứng nhỏ: `python -B review_evidence/h9_targets_job.py`. Script lấy **nguyên AST hai hàm test** từ từng clone bằng `ast.parse/compile`, nối `_TL_MODULE` và `_ROOT209` tới runtime tương ứng, chạy hàm thật. Wrapper `subprocess.run` chỉ quan sát rc/stderr rồi trả nguyên kết quả. Không giả lập Git hoặc kết quả test.
- Lệnh và output thực tế (bản đầy đủ trong `h9-targeted-*.log`):

```sh
python /tmp/claude-0/-home-user-tra-luat/6cf1da84-5813-5156-ad6b-b3a2dbd3ab61/scratchpad/rv3/review_evidence/h9_targeted.py /tmp/claude-0/-home-user-tra-luat/6cf1da84-5813-5156-ad6b-b3a2dbd3ab61/scratchpad/rv3/review_evidence/copies/base
python /tmp/claude-0/-home-user-tra-luat/6cf1da84-5813-5156-ad6b-b3a2dbd3ab61/scratchpad/rv3/review_evidence/h9_targeted.py /tmp/claude-0/-home-user-tra-luat/6cf1da84-5813-5156-ad6b-b3a2dbd3ab61/scratchpad/rv3/review_evidence/copies/head
env GIT_CONFIG_GLOBAL=/dev/null python /tmp/claude-0/-home-user-tra-luat/6cf1da84-5813-5156-ad6b-b3a2dbd3ab61/scratchpad/rv3/review_evidence/h9_targeted.py /tmp/claude-0/-home-user-tra-luat/6cf1da84-5813-5156-ad6b-b3a2dbd3ab61/scratchpad/rv3/review_evidence/copies/head
```

```text
base, inherited:
_c226_nguong_l2_troi_theo_abbrev_va_ci_ghim=False
_c268_l2_trichotomy_theo_trang_thai_object=False
targeted=0/2
rc=1
head, inherited:
_c226_nguong_l2_troi_theo_abbrev_va_ci_ghim=False
_c268_l2_trichotomy_theo_trang_thai_object=False
targeted=0/2
rc=1
head, GIT_CONFIG_GLOBAL=/dev/null:
FIXTURE_COMMIT rc=0 stderr=''
_c226_nguong_l2_troi_theo_abbrev_va_ci_ghim=True
FIXTURE_COMMIT rc=0 stderr=''
FIXTURE_COMMIT rc=0 stderr=''
_c268_l2_trichotomy_theo_trang_thai_object=True
targeted=2/2
rc=0
```

- Ở hai lượt inherited, trace của helper ghi cả 3 commit đều rc 128, stderr chứa `fatal: failed to write commit object`; `/tmp/code-sign` cố kết nối dịch vụ ký loopback và bị sandbox từ chối `socket: operation not permitted`. Không có kết nối thành công. Khi xác định điều này, đã dừng lượt **full base inherited** đang chạy bằng Ctrl-C qua `write_stdin` (mã thoát thật 130); không dùng lượt bị dừng làm bằng chứng pass/fail toàn suite. Các đối chứng N1 với `/bin/false` và các lượt dùng global rỗng không dùng signer này. Đây là giới hạn phát hiện sau khi chạy; không tuyên bố rằng các lệnh inherited chưa hề thử kết nối.
- N4 full trên **đúng head**, chỉ chuẩn hóa cấu hình Git, không đổi mã:

```sh
env TL_SELFTEST_ALLOW_NET=0 GIT_CONFIG_GLOBAL=/dev/null python scripts/tl.py --selftest
```

```text
  [OK] wp44_dev_topology_prefers_fragments
  [OK] wp44_release_bundle_topology_under_200
  [OK] wp44_missing_bundled_module_named
  [OK] r332_registry_coverage_duong_san_xuat
  [OK] wp42_complete_runtime_test_ids_unique
== tl selftest 1731/1731 ==
rc=0
```

- Log `h9-selftest-head-neutral.log` giữ toàn bộ 1.731 kết quả. Lượt H7 nguyên trạng giữ nguyên evidence `1729/1731`, không bị thay/xóa.
- Kết luận: **KHÔNG PHẢI LỖI** của diff. Hai ca đỏ tái hiện trên base và head do fixture cũ ngoài write set phụ thuộc signer máy. Cả hai ca và toàn bộ N4 đều xanh khi global rỗng: `1731/1731`, rc 0 trên reviewed SHA. Ghi nhận ngoài phạm vi `selftest-fixture-global-signing` tại hai helper nêu trên để bàn giao; không mở rộng M1 hoặc vá trong lượt review.

## FINDINGS

Không phát hiện P0/P1/P2/P3 trong diff: 0 lớp nguyên nhân còn mở, 0 biểu hiện còn mở. `approve` cho thay đổi mã tại exact SHA nêu trên, dựa trên 9 hướng kiểm và phép đo local. Ghi nhận ngoài phạm vi `selftest-fixture-global-signing` là lỗi môi trường có sẵn trên base, không phải finding do diff này gây ra; chi tiết và đối chứng ở H9.

## GIỚI HẠN ĐÃ KHAI

- N2 nguyên trạng trên **base** đỏ do máy review bật ký global; head nguyên trạng xanh. N2 base/head với `GIT_CONFIG_GLOBAL=/dev/null` đều xanh. Không ghi phép đối chứng đã chuẩn hóa thành kết quả môi trường nguyên trạng.
- N4 selftest nguyên trạng `1729/1731`, rc 1; cùng hai test fail trên base. N4 đầy đủ trên head với `GIT_CONFIG_GLOBAL=/dev/null` đạt `1731/1731`, rc 0. Full base inherited bị dừng (130), không coi là phép đo full suite hoàn chỉnh.
- Không gọi web/GitHub hoặc kết nối mạng thành công. Các lượt inherited đã vô tình kích hoạt signer `/tmp/code-sign` thử kết nối dịch vụ ký loopback; sandbox chặn. Khi phát hiện đã dừng lượt inherited còn lại và chuyển sang global rỗng; H9 giữ chi tiết, không che giấu nỗ lực kết nối này.
- **CI PR/check run trên reviewed SHA: KHÔNG ĐO ĐƯỢC / not_run** theo lệnh cấm mạng. Không xác nhận CI remote, không tự đăng verdict, ghi state/receipt, merge hoặc land.
- Ruff contract được bộ `ci_dang_ky_test.py` xác minh; bare Ruff lint không chạy (`not_run`), không gộp hai phép này thành “Ruff passed”.
- Phiên được giao là Codex/họ OpenAI, dùng công cụ shell qua runtime máy. Packet không cung cấp chứng thực độc lập ID model/effort, surface CLI/Desktop hay cặp identity của launcher; verdict này không tự cấp assurance/state `cross_approved`.
- Snapshot đầu/cuối băm tracked files và kiểm trạng thái Git; không chứng minh lịch sử mọi thao tác giữa hai mốc. Nội dung nguyên bản `cay-kho` không được dùng để chạy hoặc đột biến.
