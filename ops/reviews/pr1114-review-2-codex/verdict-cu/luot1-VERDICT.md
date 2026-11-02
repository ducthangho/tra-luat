Verdict: approve
Reviewed commit: e101b11e9586de3125f811ec4f42a89af69de8f2

Đã hoàn tất phép đo độc lập: base và head cùng 52/52 CA, 80/80 ĐỘT BIẾN, TONG DAT; delta=0, tập tên ca/đột biến giữ nguyên. Wrapper giới hạn dòng lệnh làm base đỏ đúng `p3b4_co_blob` và head xanh toàn phần. Hai đột biến đảo bản vá đều đỏ đúng ca. UTF-8, dữ liệu rỗng, quyền dùng stdin, inventory subprocess, Ruff và diff-check đạt các phép kiểm bên dưới.

| Finding P0/P1/P2/P3 | Vị trí | Lệnh tái hiện / output | Hướng vá |
|---|---|---|---|
| Không có | — | Bằng chứng từng phép đo bên dưới | — |
Chỉ thị review: yêu cầu trực tiếp của người dùng cho PR #1114, lượt 1; kho ứng viên chỉ đọc, mọi bản sao và bằng chứng nằm trong sandbox.

Neo đã đo (cwd `cay-kho`):

```text
$ git rev-parse HEAD
e101b11e9586de3125f811ec4f42a89af69de8f2
$ git rev-parse HEAD^{tree}
b2c8cab562f146cafd255fe8942c158b8c6c0f7d
$ git merge-base HEAD refs/remotes/origin/master
165b27a4bfe02e81af7bc94bda1e71c10d8c38e4
$ git diff --name-only 165b27a4bfe02e81af7bc94bda1e71c10d8c38e4 HEAD
ops/cloud_agent_creds_test.py
$ git status --short
(không có output)
$ python3 -m ruff check --select F ops/cloud_agent_creds_test.py
All checks passed!
$ git diff --check 165b27a HEAD
(không có output)
```

Không có finding P0/P1/P2/P3 trong phạm vi review. Các phần sau được ghi tăng dần khi có kết quả; dòng verdict đã được chốt sau khi tất cả lượt đo hoàn tất.

Bằng chứng tăng dần — mô phỏng trần dòng lệnh và đột biến:

Wrapper ở `bin/node`, chèn đầu `PATH`, đo `subprocess.list2cmdline(sys.argv)` bằng UTF-16 cộng NUL; từ chối khi >32767, còn lại `os.execv` Node thật. Wrapper không đọc stdin. Đây là mô phỏng giới hạn theo yêu cầu, không phải phép chạy Windows thật.

```sh
review_root=$PWD
for version in base head; do
  PATH="$review_root/bin:$PATH" REVIEW_REAL_NODE=/opt/node22/bin/node \
    NODE_LIMIT_LOG="$review_root/evidence/$version-p3b4-limit.jsonl" \
    PYTHONDONTWRITEBYTECODE=1 python3 "copies/$version/ops/cloud_agent_creds_test.py" --mot-ca p3b4_co_blob
  printf 'RC=%s\n' "$?"
done
```

Output đo độc lập (log: `evidence/base-p3b4-limit.log`, `evidence/head-p3b4-limit.log`, kèm JSONL cùng tên):

```text
base: RC=3
DO:p3b4_co_blob:node rc=206: b'WINLIMIT206: 87699 UTF-16 units including NUL > 32767; argc=3; max_arg=87545\n'
head: RC=0; stdout chỉ một newline
base argv: argc=3; arg_chars=[102,25,87545]; quoted_chars=87698
head argv (3 lời gọi): argc=2; arg_chars=[102,25]; quoted_chars=128
```

Đột biến trên tệp sao trong `copies/head/ops/`, không sửa `cay-kho`:

- `probe_no_input.py`: bỏ đúng đối số `input=json.dumps(...).encode()` trong `chay_b`.
- `probe_argv_read.py`: thay đúng `require('fs').readFileSync(0, 'utf8')` bằng `process.argv[2]` trong `JS_GIA`.

```text
$ PYTHONDONTWRITEBYTECODE=1 python3 copies/head/ops/probe_no_input.py --mot-ca p3b4_co_blob < /dev/null
DO:p3b4_co_blob:node rc=1: b'ader:1263:12)\n    at TracingChannel.traceSync (node:diagnostics_channel:328:14)\n    at wrapModuleLoad (node:internal/modules/cjs/loader:237:24)\n    at Function.executeUserEntryPoint [as runMain] (node:internal/modules/run_main:171:5)\n    at node:internal/main/run_main_module:36:49\n\nNode.js v22.22.0\n'
RC=3
$ PYTHONDONTWRITEBYTECODE=1 python3 copies/head/ops/probe_argv_read.py --mot-ca p3b4_co_blob < /dev/null
DO:p3b4_co_blob:node rc=1: b'ader:1263:12)\n    at TracingChannel.traceSync (node:diagnostics_channel:328:14)\n    at wrapModuleLoad (node:internal/modules/cjs/loader:237:24)\n    at Function.executeUserEntryPoint [as runMain] (node:internal/modules/run_main:171:5)\n    at node:internal/main/run_main_module:36:49\n\nNode.js v22.22.0\n'
RC=3
```

Hai mutant bị chốt của đúng ca giết; không phải `HONG`/lỗi vô can ở runner. Full logs: `evidence/mutation-no-input.log`, `evidence/mutation-argv-read.log`.

Bằng chứng tăng dần — ngữ nghĩa và encoding:

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 probes/semantics.py` (rc=0; toàn bộ output ở `evidence/semantics.log`). Probe nhập riêng module base/head, chạy Node thật; so sánh toàn bộ `ra/nk/ghi/doc/sha/md5` của 8 tình huống, đồng thời đo bytes tại biên `subprocess.run`.

```text
BASE_HEAD_SEMANTICS_EQUAL=8/8
EXTRACTED_GS_PLUS_JS_CHAY_STDIN_OR_ARGV_HITS=[]
RAW_NONASCII_UTF8 input_bytes=523 rc=0 FD0_READS=1 binary_sha_matches=True
EMPTY_STDIN rc=1 SyntaxError: Unexpected end of JSON input
EMPTY_P_WITH_STDIN_GUARD rc=0 FD0_READS=1 AGENT_CREDS_FILEID_MISMATCH
SEMANTICS_PROBES=PASS
```

| Đầu vào đo | Base và head cùng trả | Bytes JSON truyền |
|---|---|---:|
| `p=None` | `AGENT_CREDS_FILEID_MISMATCH`, không ghi | 80 |
| `p={}` | `AGENT_CREDS_FILEID_MISMATCH`, không ghi | 80 |
| `_p(b'')` | `BLOB_SIZE`, không ghi | 161 |
| `tep=b''`, md5 tương ứng, ghi `b'new'` | `ok=true`, size=3 | 125 |
| `bytes(range(256))`, fileId/prop `tệp-🙂-漢字` | `ok=true`, size=256, SHA-256 khớp | 557 |
| `nem=True` | `{"nem":"ghi lỗi"}`, nhả lock | 186 |
| blob 65536 | `ok=true`, size=65536 | 87545 |
| blob 65537 | `BLOB_SIZE`, không ghi | 87545 |

Ở cả 8 lượt, output probe ghi `utf8_decode_ok=true, ascii_only=true`: `json.dumps` mặc định escape Unicode; `.encode()` tạo bytes UTF-8. Node đọc `readFileSync(0, 'utf8')`; probe bổ sung còn gửi JSON UTF-8 không escape (`ensure_ascii=False`) và kiểm hash toàn bộ 256 giá trị byte. JS sinh ra cũng được ghi bằng `encoding='utf-8'`.

Probe đặt chốt trên `fs.readFileSync/readSync/read/readv/readvSync` và getter `process.stdin`, để lỗi nếu đọc stdin sau khi harness đã lấy JSON; đường thành công và `p={}` đều đạt `FD0_READS=1`. Quét riêng `_trich_gs()+JS_CHAY` không có `stdin`, `readFileSync`, `readSync`, `require(...)` hoặc `process.argv`. Phần `.gs` nhận tham số `p`; `JS_CHAY` dùng `st.p` đã parse. Các phép thử không phát hiện tranh chấp stdin.

Phân biệt rỗng: `p={}` và blob rỗng vẫn có envelope JSON hợp lệ và giữ nguyên lỗi nghiệp vụ. Luồng stdin 0 byte không phải JSON hợp lệ, bị từ chối bằng lỗi parse; `chay_b` bình thường luôn gửi envelope.

Lượt đầu của probe reviewer tự viết đặt sai kỳ vọng `p=None` là `EXPECT_MD5_REQUIRED`; kết quả thực tế `AGENT_CREDS_FILEID_MISMATCH` đã bác kỳ vọng đó. Chỉ sửa probe trong sandbox rồi đo lại cả hai phía; log đầu giữ ở `evidence/semantics-probe-v1.log`. Không tính sai kỳ vọng của probe là finding của PR.

Bằng chứng tăng dần — baseline toàn phần đã hoàn tất:

```sh
# cwd cay-kho (head nguyên bản)
PYTHONDONTWRITEBYTECODE=1 python3 ops/cloud_agent_creds_test.py > ../evidence/head.log 2>&1
# cwd copies/base, clone riêng checkout detached base
PYTHONDONTWRITEBYTECODE=1 python3 ops/cloud_agent_creds_test.py > ../../evidence/base.log 2>&1
```

Cả hai lệnh rc=0; output cả hai giống hệt:

```text
CA: 52/52 dat
DOT BIEN: 80/80 bi giet dung ly do
TU KIEM PHAN HANG: DAT (4 dot bien)
TONG: DAT
```

| Bản | CA | ĐỘT BIẾN | Tự kiểm phân hạng | TONG | rc |
|---|---:|---:|---|---|---:|
| Base `165b27a4bfe02e81af7bc94bda1e71c10d8c38e4` | 52/52 | 80/80 | DAT (4) | DAT | 0 |
| Head `e101b11e9586de3125f811ec4f42a89af69de8f2` | 52/52 | 80/80 | DAT (4) | DAT | 0 |
| Delta head − base | 0 | 0 | 0 | giữ DAT | 0 |

Không có dòng `BO QUA` trong hai log. Danh sách tên CA/đột biến được probe ngữ nghĩa xuất riêng ở `evidence/base-case-ids.json` và `evidence/head-case-ids.json` để đối chiếu, tránh chỉ dựa tổng số.

Kiểm wrapper đúng ở biên bằng `PYTHONDONTWRITEBYTECODE=1 python3 probes/wrapper_boundary.py` (rc=0):

```text
units=32767 rc=0 stdout='OK' stderr=''
units=32768 rc=206 stdout='' stderr='WINLIMIT206: 32768 UTF-16 units including NUL > 32767; argc=4; max_arg=32634\n'
WRAPPER_BOUNDARIES=PASS
```

Ruff cuối: cwd `cay-kho`, `RUFF_NO_CACHE=true python3 -m ruff check --select F ops/cloud_agent_creds_test.py` → `All checks passed!`, rc=0 (`evidence/ruff.log`). `GIT_OPTIONAL_LOCKS=0 git -C cay-kho diff --check 165b27a HEAD` → không output, rc=0 (`evidence/diff-check.log`). Lượt Ruff đầu đã tự tạo `.ruff_cache`; cache đó được chuyển nguyên ra `evidence/ruff-cache-created`, không để lại trong kho. Một lần thử biến `RUFF_NO_CACHE=1` bị Ruff từ chối với rc=2 (chỉ nhận `true/false`); lệnh trên dùng `true` đã đạt. Không thay mã nguồn ứng viên.

Lượt toàn phần qua wrapper và đo argv đã hoàn tất:

```sh
# Chạy riêng cho version=base và version=head, cwd copies/$version
review_root=$(cd ../.. && pwd)
PATH="$review_root/bin:$PATH" REVIEW_REAL_NODE=/opt/node22/bin/node \
  NODE_LIMIT_LOG="$review_root/evidence/$version-limit.jsonl" \
  REVIEW_AUDIT_LOG="$review_root/evidence/$version-argv.jsonl" \
  PYTHONPATH="$review_root/probes" PYTHONDONTWRITEBYTECODE=1 \
  python3 ops/cloud_agent_creds_test.py > "../../evidence/$version-limit.log" 2>&1
```

Output base, rc=1 (`evidence/base-limit.log`):

```text
[DO:p3b4_co_blob:node rc=206: b'WINLIMIT206: 87699 UTF-16 units including NUL > 32767; argc=3; max_arg=87545\n']
CA: 51/52 dat
[DOT BIEN KHONG BI GIET DUNG] P3B4_nguong_lon_hon_bang: HONG ca đích không xanh trên bản gốc (rc=3): DO:p3b4_co_blob:node rc=206: b'WINLIMIT206: 87699 UTF-16 units including NUL > 32767; argc=3; max_arg=87545\n'

DOT BIEN: 79/80 bi giet dung ly do
TU KIEM PHAN HANG: DAT (4 dot bien)
TONG: DO
```

Output head, rc=0 (`evidence/head-limit.log`):

```text
CA: 52/52 dat
DOT BIEN: 80/80 bi giet dung ly do
TU KIEM PHAN HANG: DAT (4 dot bien)
TONG: DAT
```

Base bị chặn ngay lượt blob **65537** đầu tiên trong `p3b4_co_blob`; probe ngữ nghĩa đo cả blob 65536 và 65537 đều thành JSON 87545 byte. Mô phỏng trả `node rc=206`, không giả nhận đã sinh được exception `FileNotFoundError` của Win32.

Đối chiếu tập pass bằng `PYTHONDONTWRITEBYTECODE=1 python3 probes/compare.py` → rc=0 (`evidence/compare.log`):

```text
cases base=52 head=52 missing=[] added=[] same_order=True
mutations base=80 head=80 missing=[] added=[] same_order=True
BASE_PASS_SET_PRESERVED=PASS
```

Độ dài mọi subprocess liên quan được kiểm bằng AST và trace động. `probes/sitecustomize.py` ghi sự kiện audit `subprocess.Popen` tại lúc spawn thật, đồng thời ghi độ dài `input` tại `subprocess.run`; kế thừa vào các tiến trình Python con. Lệnh tổng hợp: `PYTHONDONTWRITEBYTECODE=1 python3 probes/inventory.py > evidence/inventory.log`, rc=0. Trace hoàn chỉnh chứa 595 spawn base và 603 spawn head; số head lớn hơn vì base bị chặn trước hai kích thước còn lại và trước mutant P3B4. Không suy độ dài từ việc đọc tên hàm.

Đơn vị bảng: `len(subprocess.list2cmdline(argv).encode('utf-16-le')) // 2 + 1`, gồm quoting và NUL. Cột max là lớn nhất **đã đo trên toàn bộ bộ ca + đột biến với các đường dẫn của phép đo**, không phải một trần cho mọi đường dẫn/đầu vào tùy ý. Số dòng là head; các dòng base từ `chay_b` trở xuống nhỏ hơn 1.

| Subprocess / vị trí | Dữ liệu argv | Max head đo được | Max stdin byte |
|---|---|---:|---:|
| test.py:51 `_git_base` / `run` | git, `-C`, path, show, SHA:path | 190 | 0 |
| test.py:73 `chay_nap` / `run` | Python, `-B`, script, tên lệnh/cờ | 76 | 0 |
| test.py:58–59 `TL_GIA` / `Popen` | Python `-c CHAU`, path nhật ký | 215 | 0 |
| test.py:58 `CHAU` / `Popen` lồng | Python `-c 'import time; time.sleep(60)'` | 50 | 0 |
| test.py:145 / `Popen` | sh, script sleep cố định | 37 | 0 |
| test.py:146 / `Popen` | Python, script exit cố định | 42 | 0 |
| test.py:151 / `Popen` | sleep, 30 | 9 | 0 |
| test.py:317 `h2_khoi_song_sot_set_e` / `run` | bash `-c`, khối hook, paths | 542 | 0 |
| test.py:538 `chay_b` / `run` | wrapper node, path `b.js` | **129** (base **87699**) | **87545** (base 0) |
| test.py:570 `p3b7_ban_va_nhanh_case` / `run` | node, `--check` | 111 | **226231** |
| test.py:587 `p3s2_stop_chay_that` / `run` | bash `-c`, command Stop | 294 | 0 |
| test.py:700 `chay_dot_bien` / `run` | Python, `-B`, test path, `--mot-ca`, tên ca | 212 | 0 |
| cloud_agent_creds.py:84 `nap` / `Popen` | Python, tl.py giả, bootstrap, cờ cố định | 105 (kể cả mutant thêm cờ); 167 ở probe Popen giả | 0 (`DEVNULL`) |
| cloud_agent_creds.py:106 `_co_musl` / `run` | ldd, `/bin/ls` | 12, probe bổ sung chạy thật | 0 |
| cloud_agent_creds.py:122 `_ban_khop` / `Popen` | path agy, `--version` | 52; path thiếu trong probe Popen giả =24 | 0 (`DEVNULL`) |
| bash_nen.py:98 `_chay` / `run` | probe bash `-c` hoặc script path | 252 | 0 |
| mutant `B7_goi_agy_install`, dòng 159 / `run` | path agy, `install` (chỉ mutant thêm) | 50 | 0 |

`test.py` trong bảng là `ops/cloud_agent_creds_test.py`. Các bản `goc_...` / `db_...` được runner tạo cũng có trong `evidence/inventory.log`; không có nhóm spawn nào ngoài bảng trên. Lời gọi `Popen` bị mock ném lỗi ở test.py:156 không sinh tiến trình, nên đo riêng trước spawn bằng `probes/extra_calls.py` thay vì gộp nó vào số spawn thật.

Output chốt của inventory:

```text
OBSERVED base rows=918 actual_spawns=595
OBSERVED head rows=934 actual_spawns=603
HEAD_NON_NODE_MAX 542 [.../copies/head/ops/cloud_agent_creds_test.py, 317, h2_khoi_song_sot_set_e]
HEAD_CHAY_B_INPUT_MAX 87545
```

Lệnh bổ sung: `PYTHONDONTWRITEBYTECODE=1 python3 probes/extra_calls.py`, rc=0 (`evidence/extra-calls.log`):

```text
CO_MUSL argv=['ldd', '/bin/ls'] units=12 rc=0
CO_MUSL_RESULT False
MOCKED_PRE_SPAWN [Python, .../copies/head/scripts/tl.py, bootstrap, --env, code, --no-nlm] units=167
MOCKED_PRE_SPAWN ['/khong-co-agy', '--version'] units=24
HELPER_AST scripts/tl_gws.py:400 _public_curl_bytes subprocess_calls=[]
HELPER_AST scripts/tl_gws.py:1119 _last_refresh_key subprocess_calls=[]
HELPER_AST scripts/gws_cred_store.py:32 encrypt subprocess_calls=[]
HELPER_AST scripts/gws_cred_store.py:42 decrypt subprocess_calls=[]
HELPER_AST scripts/_fallback/gas.py:140 get subprocess_calls=[]
HELPER_AST scripts/_fallback/gas.py:155 post subprocess_calls=[]
EXTRA_CALLS=PASS
```

Không phát hiện đường payload lớn qua argv khác trong bộ test hoặc call graph nó thực thi. Đường payload lớn thứ hai (`node --check`) đã đi qua stdin từ base. Trong `chay_gn`, gas/get/post và `_public_curl_bytes` được gắn Drive giả; các hàm helper tương ứng cũng không có subprocess trong AST đo trên source. `tl.py` do `chay_nap` gọi là fixture `TL_GIA`, không phải CLI sản xuất. Những lệnh subprocess ở các chức năng khác của module import nhưng không được bộ test gọi không được coi là đã thực thi. Trần argv cho caller/path tùy ý ngoài bộ test: **KHÔNG ĐO ĐƯỢC**; bảng chỉ cam kết các đầu vào đã chạy.

Tái tạo hai mutant bằng `PYTHONDONTWRITEBYTECODE=1 python3 probes/make_mutants.py` → rc=0:

```text
probe_no_input.py exactly_one_replacement=True
probe_argv_read.py exactly_one_replacement=True
```

Kiểm kho cuối (mọi lệnh dưới rc=0):

```text
$ GIT_OPTIONAL_LOCKS=0 git -C cay-kho diff --exit-code HEAD
(không output)
$ GIT_OPTIONAL_LOCKS=0 git -C cay-kho status --short --untracked-files=all
(không output)
$ GIT_OPTIONAL_LOCKS=0 git -C cay-kho ls-files --others --ignored --exclude-standard
(không output)
$ GIT_OPTIONAL_LOCKS=0 git -C cay-kho rev-parse HEAD
e101b11e9586de3125f811ec4f42a89af69de8f2
```

Giới hạn bằng chứng: Windows thật, exception Win32 thật và log CI `41283928240`: **KHÔNG ĐO ĐƯỢC** trong lượt này. Đã đo độc lập payload/argv, tái hiện giới hạn bằng wrapper và đối chiếu base/head như yêu cầu. Verdict này chỉ là kết quả review exact commit đã nêu; không cấp quyền merge/land.

Kiểm neo bản sao cuối: `git -C <path> rev-parse HEAD`, `git -C <path> diff --exit-code HEAD`; so bytes test bằng Python (`evidence/final-anchor.log`):

```text
candidate HEAD=e101b11e9586de3125f811ec4f42a89af69de8f2 rc=0
candidate tracked_diff_rc=0
base_copy HEAD=165b27a4bfe02e81af7bc94bda1e71c10d8c38e4 rc=0
base_copy tracked_diff_rc=0
head_copy HEAD=e101b11e9586de3125f811ec4f42a89af69de8f2 rc=0
head_copy tracked_diff_rc=0
CANDIDATE_HEAD_COPY_TEST_BYTES_EQUAL=True sha256=72e97b3a536aeb57317d5af11c2e09e087bc4f6d7db73ead27beb8f4892c52cf
base final_trace_rows=918 actual_spawns=595
head final_trace_rows=934 actual_spawns=603
```
