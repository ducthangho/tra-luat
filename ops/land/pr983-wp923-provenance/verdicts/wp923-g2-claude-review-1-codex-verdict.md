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

Review nội dung trên bản sao local; không tự ghi state/receipt/lease hoặc xác nhận quyền land.

## BẢNG SĂN

Đối chiếu độc lập không phát hiện P0/P1/P2/P3; chấp nhận diff trên exact SHA nêu trên.
Ngưỡng áp dụng theo packet: chỉ approve khi không còn P0/P1/P2.

| Tiêu chí | Trạng thái và bằng chứng |
|---|---|
| N1 | passed — H1/H6: một tệp, +2/−1 chú thích; 0 dòng mã đổi, AST và các dòng không phải chú thích bằng nhau. |
| N2 | passed ở reviewed_sha — H5b: 28/28, 1070/1070 và TỔNG: ĐẠT; trùng nguyên byte cả hai log packet. Base chỉ được đối chiếu bằng log được cấp, reviewer không khai đã chạy base. |
| N3 | passed trong phạm vi quét — H4/H4b: không tìm thấy chốt nguyên byte sống của tệp; đã kiểm tên, digest, manifest và các consumer. |
| N4 | passed — H7: tự chạy trên exact HEAD, rc=0, 1731/1731. |
| N5 | not_run / KHÔNG ĐO ĐƯỢC — không có check run trong packet, không truy vấn GitHub theo chỉ thị cấm mạng. Không khẳng định CI PR xanh. |

Verdict này chấp nhận nội dung diff ở bước review trước push theo SPEC Q3; không xác nhận N5,
lease hiện hành, chuyển state hay quyền merge/land/deploy. Kho `cay-kho/` được giữ sạch.
N2 ban đầu lỗi do fixture Git tạm kế thừa yêu cầu ký commit; helper ký thử kết nối loopback
và bị sandbox chặn. Lượt H5b tắt ký riêng trong môi trường tiến trình test, không sửa cấu hình
hoặc tạo commit trong kho được review. Mọi lệnh đo và output bên dưới là kết quả chạy thật.

### HƯỚNG 0: Neo và tính toàn vẹn packet

Giả thuyết: Sai SHA, SPEC hoặc diff sẽ làm review vô hiệu.

Lệnh (cwd: `/tmp/claude-0/-home-user-tra-luat/6cf1da84-5813-5156-ad6b-b3a2dbd3ab61/scratchpad/rv1`):

```bash
git -C cay-kho rev-parse HEAD HEAD^{tree}
git -C cay-kho status --porcelain=v1
git -C cay-kho symbolic-ref -q HEAD; printf 'symbolic_ref_rc=%s (1 = detached)\n' "$?"
sha256sum SPEC.md
python - <<'PY'
import hashlib, pathlib, subprocess
repo = 'cay-kho'
base = 'e139e55883d90fd74a358230be5599c9e223d4b3'
head = '67bacb3b51ac9eda72297b10b15b798b3ca51959'
git = lambda *a: subprocess.check_output(['git', '-C', repo, *a])
assert git('rev-parse', 'HEAD').decode().strip() == head
assert hashlib.sha256(pathlib.Path('SPEC.md').read_bytes()).hexdigest() == 'a36f8d2d84d39c3587a60edcb63d4886f82e3fae097c283700718b5869eecbc1'
assert not git('status', '--porcelain=v1')
assert git('diff', base, head) == pathlib.Path('diff.patch').read_bytes()
assert git('diff', '--numstat', base, head) == pathlib.Path('numstat.txt').read_bytes()
print('head/spec/clean-worktree/diff.patch/numstat.txt: all match')
print('base_is_ancestor_rc=' + str(subprocess.run(['git', '-C', repo, 'merge-base', '--is-ancestor', base, head]).returncode))
PY
```

Output thật (exit code 0):

```text
67bacb3b51ac9eda72297b10b15b798b3ca51959
8512df452237dad95f764b23204ebd8387d69fdb
symbolic_ref_rc=1 (1 = detached)
a36f8d2d84d39c3587a60edcb63d4886f82e3fae097c283700718b5869eecbc1  SPEC.md
head/spec/clean-worktree/diff.patch/numstat.txt: all match
base_is_ancestor_rc=0
```

Kết luận: KHÔNG PHẢI LỖI — đúng HEAD/tree, SPEC và hai artifact; worktree sạch, checkout detached.

### HƯỚNG 1: N1: phạm vi và hành vi Python

Giả thuyết: Diff có thể đổi mã, hằng hoặc AST dù được khai là chỉ sửa chú thích.

Lệnh (cwd: `/tmp/claude-0/-home-user-tra-luat/6cf1da84-5813-5156-ad6b-b3a2dbd3ab61/scratchpad/rv1`):

```bash
python - <<'PY'
import ast, hashlib, subprocess
b, h = 'e139e55883d90fd74a358230be5599c9e223d4b3', '67bacb3b51ac9eda72297b10b15b798b3ca51959'
p = '.claude/dev/ci_dang_ky_test.py'
git = lambda *a: subprocess.check_output(['git', '-C', 'cay-kho', *a])
print(git('diff', '--numstat', b, h).decode().strip())
assert git('diff', '--name-only', b, h).decode().splitlines() == [p]
d = git('diff', '--no-ext-diff', '--unified=0', b, h, '--', p).decode().splitlines()
changed = [s for s in d if s[:1] in ('+', '-') and not s.startswith(('+++', '---'))]
bad = [s for s in changed if not s[1:].lstrip().startswith('#')]
print(f'added={sum(s.startswith("+") for s in changed)} deleted={sum(s.startswith("-") for s in changed)} non_comment={len(bad)}')
assert not bad
src = [git('show', f'{s}:{p}') for s in (b, h)]
trees = [ast.dump(ast.parse(s)) for s in src]
print('AST_equal=' + str(trees[0] == trees[1]))
assert trees[0] == trees[1]
code = [b'\n'.join(line for line in s.splitlines() if not line.lstrip().startswith(b'#')) for s in src]
print('non_comment_lines_byte_equal=' + str(code[0] == code[1]))
assert code[0] == code[1]
for label, data in zip(('base', 'head'), code):
    print(label + '_non_comment_sha256=' + hashlib.sha256(data).hexdigest())
PY
```

Output thật (exit code 0):

```text
2	1	.claude/dev/ci_dang_ky_test.py
added=2 deleted=1 non_comment=0
AST_equal=True
non_comment_lines_byte_equal=True
base_non_comment_sha256=fd216083e35ea07f9303c83387f4b2a9989ad32b495cd06857459c9d0bded99b
head_non_comment_sha256=fd216083e35ea07f9303c83387f4b2a9989ad32b495cd06857459c9d0bded99b
```

Kết luận: KHÔNG PHẢI LỖI — đúng một tệp, +2/−1 đều là chú thích; AST và toàn bộ các dòng không phải chú thích bằng nhau.

### HƯỚNG 2: Đúng giá trị, job và mốc Git/PR

Giả thuyết: Chú thích mới có thể trỏ nhầm job, sai timeout trên base hoặc ghi mốc không có trong lịch sử.

Lệnh (cwd: `/tmp/claude-0/-home-user-tra-luat/6cf1da84-5813-5156-ad6b-b3a2dbd3ab61/scratchpad/rv1`):

```bash
python - <<'PY'
import ast, json, subprocess, yaml
git = lambda *a: subprocess.check_output(['git', '-C', 'cay-kho', *a]).decode()
base = 'e139e55883d90fd74a358230be5599c9e223d4b3'
p = '.claude/dev/ci_dang_ky_test.py'
w = '.github/workflows/ci.yml'
print('is_shallow=' + git('rev-parse', '--is-shallow-repository').strip())
m = git('rev-parse', 'a7da463').strip()
print(git('show', '-s', '--format=%H%n%s', m).strip())
for rev in (m + '^', m, base):
    jobs = yaml.safe_load(git('show', f'{rev}:{w}'))['jobs']
    print(rev + ': ' + json.dumps({k: v.get('timeout-minutes') for k, v in jobs.items()}, ensure_ascii=False, sort_keys=True))
src = git('show', f'{base}:{p}')
node = next(n for n in ast.parse(src).body if isinstance(n, ast.FunctionDef) and n.name == 'bam_gate_nhanh')
print('base code identifying jobs:\n' + ast.get_source_segment(src, node))
print('PR merge:\n' + git('show', '-s', '--format=%H%n%P%n%s', 'ba222ff').strip())
for ancestor, descendant in ((m, base), (m, 'ba222ff^2'), ('ba222ff', base)):
    rc = subprocess.run(['git', '-C', 'cay-kho', 'merge-base', '--is-ancestor', ancestor, descendant]).returncode
    print(f'is_ancestor({ancestor}, {descendant}) rc={rc}')
    assert rc == 0
jobs = yaml.safe_load(git('show', f'{base}:{w}'))['jobs']
assert [jobs[k]['timeout-minutes'] for k in ('gate-registry', 'gate-nhanh-manh', 'gate-nhanh-gop')] == [150, 150, 10]
PY
```

Output thật (exit code 0):

```text
is_shallow=false
a7da46390177cdc2d64f516dedac19857bee86dd
wp910 r3(#910): timeout-minutes 150 cho gate-nhanh-manh, gate-registry, dot-bien-du (pha B)
a7da46390177cdc2d64f516dedac19857bee86dd^: {"chuan-bi": 20, "gate": 150, "gate-cong-cu": 150, "gate-cong-cu-gop": 10, "gate-nhanh-gop": 10, "gate-nhanh-manh": 30, "gate-ops": 150, "gate-packet-loop": 150, "gate-registry": 105}
a7da46390177cdc2d64f516dedac19857bee86dd: {"chuan-bi": 20, "gate": 150, "gate-cong-cu": 150, "gate-cong-cu-gop": 10, "gate-nhanh-gop": 10, "gate-nhanh-manh": 150, "gate-ops": 150, "gate-packet-loop": 150, "gate-registry": 150}
e139e55883d90fd74a358230be5599c9e223d4b3: {"chuan-bi": 20, "gate": 150, "gate-cong-cu": 150, "gate-cong-cu-gop": 10, "gate-nhanh-gop": 10, "gate-nhanh-manh": 150, "gate-ops": 150, "gate-packet-loop": 150, "gate-registry": 150}
base code identifying jobs:
def bam_gate_nhanh(data):
    """Ghim trọn hai job mảnh/gom chịu trách nhiệm cho cờ nhẹ của registry."""
    jobs = (data or {}).get("jobs") or {}
    goi = {k: jobs.get(k) for k in ("gate-nhanh-manh", "gate-nhanh-gop")}
    return hashlib.sha256(json.dumps(goi, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()
PR merge:
ba222ffd1615f0d74b59985b9612f725211b62f5
1797c32530fba381afd4009340a3fa558b7e37b0 a7da46390177cdc2d64f516dedac19857bee86dd
Merge pull request #917 from ducthangho/agent/wp910-g3-claude
is_ancestor(a7da46390177cdc2d64f516dedac19857bee86dd, e139e55883d90fd74a358230be5599c9e223d4b3) rc=0
is_ancestor(a7da46390177cdc2d64f516dedac19857bee86dd, ba222ff^2) rc=0
is_ancestor(ba222ff, e139e55883d90fd74a358230be5599c9e223d4b3) rc=0
```

Kết luận: KHÔNG PHẢI LỖI — bam_gate_nhanh xác định đúng hai job; base là 150/150/10; a7da463 và merge PR #917 xác nhận hai lần nâng trần, job gom giữ 10.

### HƯỚNG 3: Độ phủ quét độc lập và loại trừ ngoài phạm vi

Giả thuyết: Executor có thể bỏ sót một chú thích timeout hiện tại, nhất là dạng không dấu hoặc câu tiếp nối.

Lệnh (cwd: `/tmp/claude-0/-home-user-tra-luat/6cf1da84-5813-5156-ad6b-b3a2dbd3ab61/scratchpad/rv1`):

```bash
python - <<'PY'
import re, subprocess, unicodedata, yaml
p = '.claude/dev/ci_dang_ky_test.py'
base = 'e139e55883d90fd74a358230be5599c9e223d4b3'
src = subprocess.check_output(['git', '-C', 'cay-kho', 'show', f'{base}:{p}']).decode()
lines = src.splitlines()
fold = lambda s: ''.join(c for c in unicodedata.normalize('NFD', s.lower()) if unicodedata.category(c) != 'Mn').replace('đ', 'd')
kw = re.compile(r'timeout|minute|phut|\btran\b|\bjob\b|\bgate[-_]|\bnay\b|gioi.han|\bgiay\b|\b(?:30|90|105|150|360)\b')
comments = [(n, s) for n, s in enumerate(lines, 1) if s.lstrip().startswith('#')]
hits = [(n, s) for n, s in comments if kw.search(fold(s))]
print(f'base: total_lines={len(lines)} raw_full_line_hash_candidates={len(comments)} broad_regex_hits={len(hits)}')
for n, s in hits: print(f'{n}: {s}')
inline = [(n, s) for n, s in enumerate(lines, 1) if '#' in s and not s.lstrip().startswith('#') and kw.search(fold(s[s.index('#'):]))]
print(f'inline_or_string_candidates={len(inline)}')
for n, s in inline: print(f'{n}: {s}')
print('All contiguous full-line comment blocks containing a timeout/minute/tran-job phrase:')
blocks, block = [], []
for n, s in enumerate(lines + [''], 1):
    if s.lstrip().startswith('#'): block.append((n, s))
    elif block:
        if re.search(r'timeout|phut|tran.{0,12}job', fold(' '.join(s for _, s in block))): blocks.append(block)
        block = []
for block in blocks:
    print('BLOCK ' + str(block[0][0]) + '-' + str(block[-1][0]))
    for n, s in block: print(f'{n}: {s}')
weekly = yaml.safe_load(subprocess.check_output(['git', '-C', 'cay-kho', 'show', f'{base}:.github/workflows/ci-dot-bien-du.yml']))
print('ci-dot-bien-du.yml job timeouts:', {k: v.get('timeout-minutes') for k, v in weekly['jobs'].items()})
for n in (920, 966, 967, 968, 974, 978, 979): print(f'context {n}: {lines[n-1]}')
PY
```

Output thật (exit code 0):

```text
base: total_lines=2444 raw_full_line_hash_candidates=155 broad_regex_hits=28
45:     # GIU NGUYEN `\d+` — M4 dong bang hanh vi Linux, va mau nay la duong Linux di qua.
50:     # (`MAU_DAY_DU`), mau nay van giu nguyen.
759: # trần cũ. KHÔNG bảo đảm cả job dưới `timeout-minutes` (nay 105): bộ ấy còn chờ worker trống (run trên: bắt đầu sau 337 s),
760: # Windows ép N=1 ⇒ dài hơn; trần job là trần NGOÀI. Ca `p643-tran-bo-nho-hon-timeout-job` chỉ khoá trần bộ < trần job.
761: # #705 (CI-REGISTRY-NANG-TRAN-BO-DAY-DU, chủ kho Q4): 4500 → 5400, job 90 → 105 phút. `nhanh_don_duoc_test` chế độ đủ:
797: # Codex CLI lượt 1 trên feeee4ed: script thiết lập runner của `gate-registry` nằm NGOÀI `.github/` (`cai_actionlint.sh`
808: # WP748 r16: hai job nay la `targeted_mutant_gate` (NHANH_DON_DUOC_DICH, gom `--gop-dich`, tran 30 phut).
845: # #661 M4: CHỈ lượt tuần đặt biến này (ci.yml CẤM qua `loi_env_registry`); đột biến ĐỦ do job mảnh + gom (M5).
921: # GHIM (Codex CLI): cron bất kỳ lọt lịch năm (lượt 2); `name`/job id tự do lọt biểu thức hỏng (lượt 4).
978:     # WP748 r16: full_mutant_audit ~73 800 s noi tiep (g12) => 8 manh x ~2,6 h => tran 360 (tran job GitHub).
1069:     #637: `so_worker` = trần bộ ĐANG chạy; `dong_ho` = seam M1; `bao_cao` nhận JSON (không in ở
1168: # #668: bán kính đột biến của `cong_cu_test` chia `SO_MANH_G5` job mảnh + một job gom. Mọi giá trị dưới đây GHIM, so
1178: # wp879 (#879): Windows chỉ còn mảnh 0 và chỉ chạy ca nền ⇒ không ghi tệp mảnh, không tải lên, không có job gom Windows.
1200: # Nên NGỮ NGHĨA THỰC THI của job G5 cũng theo danh sách CHO PHÉP: khoá job/bước, shell, env, `with`, `runs-on`, matrix os.
1219:         # #668 F10 (Codex lượt 4, P1 — lần thứ BA của lớp này): GitHub nội suy `${{ }}` trên TOÀN thân `run` trước khi
1221:         # chú thích. Không vá theo từng biến thể nữa: thân `run` của job G5 chỉ được có ký tự IN ĐƯỢC + `\n`, và không
1409:     # ba ca này ĐỎ; đó là điều mà đột biến canh-vị-từ `r4-khong-do-duoc-thanh-dat` KHÔNG
1424:     # xuất hiện BA lần trong chính packet này: (1) khuyết tật gốc — trạng thái thứ ba
1432:     # miền mà quên ca thì bảng này hở lộ ra ngay, khác hẳn danh sách ca rời rạc.
1453:     # NOI TIEU THU gia tri, va do la bai hoc r6/#401 da tra gia ba lan trong tep nay.
1484:     # M4 cua #456 giu o tang MAU (`MOI` y het base, hai ca duoi). Lo #319 phia Linux nay DONG o tang CHE DO:
1634:     # Lớp nhận dạng: một job đúng KHÔNG được che installer ngoài miền ở job khác.
1734:     # Cùng vị từ -1 phải được tiêu thụ cả khi job phụ không có một lệnh cài nào.
1992:     # ── #668 A6: job mảnh/gom — mỗi hình dạng lệch một ca, sửa trên BẢN SAO của ci.yml thật. ──
2091:     # #668 F14: bước G5 bỏ `shell` ⇒ Windows chạy bằng pwsh ⇒ ĐỎ ở mọi job G5.
2280:                    # #705 F4: SUY từ ci.yml — hằng tay trôi khỏi trần thật thì ca thắng nhờ GIÁ TRỊ, thôi đo KIỂU.
2344:     # #705: đo trần tới communicate qua đường runtime, không chỉ giá trị hằng.
2382:     # chinh nguon lech F02 to cao. Nay ten VA ket qua o CUNG mot `_them`, khong con `zip` de cat im.
inline_or_string_candidates=7
936:     """#651 M4: lượt ĐỦ hằng tuần. Danh sách CHO PHÉP ở mọi tầng; bước so BẰNG ĐÚNG `gate-registry` của `ci.yml` (trích từ
941:     on = d.get("on", d.get(True))  # PyYAML đọc khoá trần `on` thành True
975:     """#661 M5: hai job GHIM trọn; bước python + `env` TRÍCH từ `gate-registry`; matrix và N cùng từ `SO_MANH`."""
1237:     """#668: phần RIÊNG của hai job mảnh/gom — matrix, `needs`, `if`, và bước artifact, mọi thứ so BẰNG ĐÚNG."""
1258:     vắng), vô điều kiện; trước nó chỉ lệnh thiết lập (gom: thêm đúng bước tải về). #668: job mảnh/gom qua `_loi_g5_manh_gop`."""
1915:     _j["bo"] = [{**m, "giay": 2} for m in _bc["bo"]]          # WP748 r19: giay int huu han van DUNG
2419:     try:  # tệp rỗng ⇒ None ⇒ chốt vẫn chạy và ĐỎ; chỉ lỗi đọc/phân tích mới đi nhánh này
All contiguous full-line comment blocks containing a timeout/minute/tran-job phrase:
BLOCK 757-764
757: # CI-SONG-SONG-REGISTRY-G5-MOT-LAN r1 (#637): M1–M3, M6, M7. Hằng số trong W1 theo spec M3.
758: # #643 (chủ kho chọn "b", PR #644): 3600 → 4500. Đo run 36208617323, N=2 chế độ đủ: `nhanh_don_duoc_test` 3306,45 s = 92 %
759: # trần cũ. KHÔNG bảo đảm cả job dưới `timeout-minutes` (nay 105): bộ ấy còn chờ worker trống (run trên: bắt đầu sau 337 s),
760: # Windows ép N=1 ⇒ dài hơn; trần job là trần NGOÀI. Ca `p643-tran-bo-nho-hon-timeout-job` chỉ khoá trần bộ < trần job.
761: # #705 (CI-REGISTRY-NANG-TRAN-BO-DAY-DU, chủ kho Q4): 4500 → 5400, job 90 → 105 phút. `nhanh_don_duoc_test` chế độ đủ:
762: # 3645 s xanh (run 36642392330) rồi > 4500 s ĐỎ ba lần (36696528580 ×2, 36839918701) — runner chậm 22–42 % (hai bộ vô can
763: # cùng lượt: `pretooluse_guard_test` 914 → 1213–1300 s, `subagent_ghi_detect_test` 316 → 386–400 s), KHÔNG phải bộ chậm đi
764: # (delta tại chỗ 7b308bc 4604 s / 423b4ba 4586 s). 3645 × 1,42 ≈ 5180 ⇒ 5400 chỉ dư ~4 % — MỎNG; giải pháp bền là chia mảnh.
BLOCK 808-808
808: # WP748 r16: hai job nay la `targeted_mutant_gate` (NHANH_DON_DUOC_DICH, gom `--gop-dich`, tran 30 phut).
BLOCK 978-978
978:     # WP748 r16: full_mutant_audit ~73 800 s noi tiep (g12) => 8 manh x ~2,6 h => tran 360 (tran job GitHub).
ci-dot-bien-du.yml job timeouts: {'dot-bien-du': 150, 'dot-bien-manh': 360, 'dot-bien-gop': 10}
context 920: WF_DOT_BIEN_DU = ROOT / ".github/workflows/ci-dot-bien-du.yml"
context 966:     """`==` có xét KIỂU ở mọi tầng: `False == 0`, `90.0 == 90` làm matrix/số sai kiểu lọt (Codex #661 lượt 1 F01)."""
context 967:     if type(a) is not type(b):
context 968:         return False
context 974: def _job_manh_gop(goc):
context 978:     # WP748 r16: full_mutant_audit ~73 800 s noi tiep (g12) => 8 manh x ~2,6 h => tran 360 (tran job GitHub).
context 979:     manh = {"runs-on": "ubuntu-latest", "timeout-minutes": 360, "env": env,
```

Kết luận: KHÔNG PHẢI LỖI — quét thô bằng regex bỏ dấu, cả ứng viên inline và toàn khối chú thích, cho đủ năm dòng liên quan 759/760/761/808/978 trên base. 760 không định lượng; 761 là lịch sử #705; 978 là trần 360 của dot-bien-manh trong workflow tuần, khớp YAML và hằng ngay dưới. Các số giây 337/3645/4500/5400 là thời gian bộ hoặc số đo lịch sử. Không thấy chú thích hiện tại khác của ci.yml cần sửa.

### HƯỚNG 4: N3: chốt byte, digest và mọi kiểu đọc tệp

Giả thuyết: Có thể tồn tại chốt nguyên byte dùng tên tệp, OID, SHA-256, tiền tố băm hoặc manifest.

Lệnh (cwd: `/tmp/claude-0/-home-user-tra-luat/6cf1da84-5813-5156-ad6b-b3a2dbd3ab61/scratchpad/rv1`):

```bash
python - <<'PY'
import ast, collections, hashlib, json, pathlib, subprocess
repo = pathlib.Path('cay-kho')
path = '.claude/dev/ci_dang_ky_test.py'
base = 'e139e55883d90fd74a358230be5599c9e223d4b3'
git = lambda *a: subprocess.check_output(['git', '-C', str(repo), *a])
blob = git('rev-parse', f'{base}:{path}').decode().strip()
sha = hashlib.sha256(git('show', f'{base}:{path}')).hexdigest()
print('base_blob_oid=' + blob + '\nbase_sha256=' + sha)
def search(label, argv, detail=False):
    r = subprocess.run(argv, cwd=repo, capture_output=True, text=True)
    assert r.returncode in (0, 1), r.stderr
    lines = r.stdout.splitlines()
    pathlib.Path('/tmp/wp923-' + label + '.txt').write_text(r.stdout)
    print(f'{label}: rc={r.returncode} lines={len(lines)}')
    if detail: print(r.stdout or '(no matches)')
    return lines
hits = search('n3-rg-name', ['rg', '-n', '--hidden', '--no-ignore', '-g', '!.git/**', '-g', '!*.md', 'ci_dang_ky_test', '.'])
print('rg hit counts by category:', dict(collections.Counter('historical_reviews_land' if s.startswith(('./ops/reviews/', './ops/land/')) else 'lease_metadata' if s.startswith('./ops/leases/') else 'other' for s in hits)))
tracked = search('n3-git-name', ['git', 'grep', '-n', '-I', 'ci_dang_ky_test', '--', ':!*.md'])
print('Other tracked paths/counts:')
for p, n in sorted(collections.Counter(s.split(':', 1)[0] for s in tracked if not s.startswith(('ops/reviews/', 'ops/land/', 'ops/leases/'))).items()): print(f'  {p}: {n}')
for label, patterns in (('n3-full-hashes', [blob, sha]), ('n3-short-hashes', [blob[:7], sha[:12]])):
    argv = ['git', 'grep', '-n', '-I', '-F']
    for pattern in patterns: argv += ['-e', pattern]
    search(label, argv + ['--'], detail=True)
manifest = json.loads((repo / 'RELEASE_MANIFEST.json').read_text())
entries = [x for x in manifest['files'] if x['path'] == path or x['path'].startswith('.claude/')]
print(f'RELEASE_MANIFEST: entries={len(manifest["files"])} .claude_entries={entries}')
for p, names in {
    'ops/ci_provenance.py': ['doc_moi'],
    'ops/ci_provenance_test.py': ['moi_tam'],
    'ops/ci_duong_nhanh_test.py': ['nap_so_dang_ky', 'k02_da_noi_dung_mot_lan_va_test_song_khop_tep', 'nap_so_dang_ky_tu'],
}.items():
    src = (repo / p).read_text()
    for n in ast.walk(ast.parse(src)):
        if isinstance(n, ast.FunctionDef) and n.name in names:
            print(f'{p}:{n.lineno}\n' + ast.get_source_segment(src, n))
print('Additional readers:')
for p, ranges in {
    '.claude/dev/doc_receipt_thu_hoi_test.py': [(258, 260)],
    '.claude/dev/chay-cong-windows_test.ps1': [(204, 211)],
    'ops/ci_duong_nhanh_test.py': [(3091, 3097)],
}.items():
    lines = (repo / p).read_text().splitlines()
    for lo, hi in ranges:
        for i in range(lo, hi + 1): print(f'{p}:{i}: {lines[i-1]}')
print('Generic test hash guard search:')
generic = search('n3-generic-guards', ['git', 'grep', '-n', '-I', '-E', 'sha256_test|test.{0,35}(sha256|hash)|(sha256|hash).{0,35}test', '--', ':!*.md', ':!ops/reviews/**', ':!ops/land/**', ':!ops/leases/**'])
print('generic guard counts by path:', dict(collections.Counter(s.split(':', 1)[0] for s in generic)))
for p in ('ops/cong_cu_test.py', 'ops/nhanh_don_duoc_test.py'):
    src = (repo / p).read_text().splitlines()
    for n in ast.parse('\n'.join(src)).body:
        if isinstance(n, ast.Assign) and any(isinstance(v, ast.Name) and v.id == 'TEP_TEST' for t in n.targets for v in ast.walk(t)):
            print(f'{p}:{n.lineno}: ' + ast.get_source_segment('\n'.join(src), n))
    for i, line in enumerate(src, 1):
        if line.startswith('TEP_TEST =') or (line.startswith('    return {') and '"sha256_test": hashlib.sha256' in line): print(f'{p}:{i}: {line}')
PY
```

Output thật (exit code 0):

```text
base_blob_oid=a6dc4081f9aadc46a543b6c3e3f0f85a7b113685
base_sha256=9ff2b624c8dd00cc1ed874a91bba77af9d1c2dd81ed3884f47735f1e76dbd56c
n3-rg-name: rc=0 lines=850
rg hit counts by category: {'other': 57, 'lease_metadata': 124, 'historical_reviews_land': 669}
n3-git-name: rc=0 lines=850
Other tracked paths/counts:
  .claude/dev/chay-cong-windows.ps1: 2
  .claude/dev/chay-cong-windows_test.ps1: 3
  .claude/dev/ci_dang_ky_test.py: 25
  .claude/dev/doc_receipt_thu_hoi_test.py: 1
  .claude/hooks/pretooluse_guard_test.py: 1
  .claude/hooks/subagent_ghi_detect_test.py: 1
  .github/workflows/ci-dot-bien-du.yml: 3
  .github/workflows/ci.yml: 5
  ops/ci_duong_nhanh_test.py: 10
  ops/ci_provenance.py: 1
  ops/ci_provenance_test.py: 2
  ops/kiem_trang_quyet_dinh.sh: 1
  ops/land_evidence_nguon.py: 1
  ops/lease_publish_test.py: 1
n3-full-hashes: rc=1 lines=0
(no matches)
n3-short-hashes: rc=1 lines=0
(no matches)
RELEASE_MANIFEST: entries=192 .claude_entries=[]
ops/ci_provenance.py:128
def doc_moi(duong=CI_DANG_KY):
    """`MOI` và `bang_chung_xanh` đọc bằng IMPORT sổ đăng ký — một nguồn, không chép bảng."""
    spec = importlib.util.spec_from_file_location("ci_dang_ky_cho_provenance", duong)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return dict(m.MOI), m.bang_chung_xanh
ops/ci_provenance_test.py:142
def moi_tam(them=None):
    """Bản sao TẠM của sổ đăng ký THẬT, nối thêm mục `MOI` lúc chạy — công cụ phải thấy nó qua import, không qua bảng chép."""
    with tempfile.TemporaryDirectory(prefix="cip_moi_") as thu:
        p = Path(thu) / "ci_dang_ky_test.py"
        p.write_text(CI_DANG_KY.read_text(encoding="utf-8") + "".join(f"\nMOI[{k!r}] = {v!r}\n" for k, v in (them or {}).items()),
                     encoding="utf-8")
        yield p
ops/ci_duong_nhanh_test.py:2578
def nap_so_dang_ky():
    import runpy
    return runpy.run_path(str(CAY / ".claude" / "dev" / "ci_dang_ky_test.py"))
ops/ci_duong_nhanh_test.py:2593
def k02_da_noi_dung_mot_lan_va_test_song_khop_tep():
    m = nap_so_dang_ky()
    song, _, _ = m["tim"](CAY)
    bang(DA_NOI_MUC in song, f"tep {DA_NOI_MUC} phai ton tai o muc dinh ops/ (vi tri chuan cua test song)")
    src = (CAY / ".claude" / "dev" / "ci_dang_ky_test.py").read_text(encoding="utf-8")
    bang(src.count(f'"{DA_NOI_MUC}"') == 1, f"muc {DA_NOI_MUC!r} phai xuat hien dung mot lan trong ci_dang_ky_test.py")
ops/ci_duong_nhanh_test.py:3111
def nap_so_dang_ky_tu(goc):
    import runpy
    return runpy.run_path(str(goc / ".claude" / "dev" / "ci_dang_ky_test.py"))
Additional readers:
.claude/dev/doc_receipt_thu_hoi_test.py:258:     cdk = _nap(GOC / "ci_dang_ky_test.py", "ci_dang_ky_duoi_test")
.claude/dev/doc_receipt_thu_hoi_test.py:259:     if cdk.MOI.get(".claude/dev/doc_receipt_thu_hoi_test.py") != MAU:
.claude/dev/doc_receipt_thu_hoi_test.py:260:         raise TinHieuChotCa(f"{ten}: MOI khong dang ky dung MAU (M8)")
.claude/dev/chay-cong-windows_test.ps1:204:     Copy-Item -LiteralPath $Scr -Destination (Join-Path $k '.claude/dev/chay-cong-windows.ps1')
.claude/dev/chay-cong-windows_test.ps1:205:     Copy-Item -LiteralPath (Join-Path $GocKho 'ops/bash_nen.py') -Destination (Join-Path $k 'ops/bash_nen.py')
.claude/dev/chay-cong-windows_test.ps1:206:     Copy-Item -LiteralPath (Join-Path $GocKho '.gitignore') -Destination (Join-Path $k '.gitignore')
.claude/dev/chay-cong-windows_test.ps1:207:     foreach ($f in 'ops/lease_publish_test.py', 'ops/cong_cu.py', 'ops/cong_cu_test.py',
.claude/dev/chay-cong-windows_test.ps1:208:                    '.claude/dev/packet_loop_test.py', '.claude/dev/ci_dang_ky_test.py',
.claude/dev/chay-cong-windows_test.ps1:209:                    '.claude/dev/codex_cred_test.py', 'ops/bien_nhan_v2_test.py', '.claude/dev/idiom_py_test.py',
.claude/dev/chay-cong-windows_test.ps1:210:                    '.githooks/eol_policy_test.py', '.githooks/pre_push_test.py', '.claude/dev/gate_lifecycle_test.py',
.claude/dev/chay-cong-windows_test.ps1:211:                    '.githooks/eol_policy.py', '.github/checks/bundle_fragment_check.py', 'scripts/gen_instructions.py',
ops/ci_duong_nhanh_test.py:3091: def dung_cay_tam(thay):
ops/ci_duong_nhanh_test.py:3092:     """Bản sao TỐI THIỂU của cây: chỉ những tệp mà các ca đọc. `thay` = {đường dẫn: văn bản mới}."""
ops/ci_duong_nhanh_test.py:3093:     goc = Path(tempfile.mkdtemp(prefix="cdn_cay_"))
ops/ci_duong_nhanh_test.py:3094:     for dp in ("ops/ci_duong_nhanh.py", "ops/ci_duong_nhanh_test.py", ".claude/dev/ci_dang_ky_test.py", "ops/lease_publish.py"):
ops/ci_duong_nhanh_test.py:3095:         (goc / dp).parent.mkdir(parents=True, exist_ok=True)
ops/ci_duong_nhanh_test.py:3096:         shutil.copyfile(ROOT_THAT / dp, goc / dp)
ops/ci_duong_nhanh_test.py:3097:     (goc / ".github/workflows").mkdir(parents=True, exist_ok=True)
Generic test hash guard search:
n3-generic-guards: rc=0 lines=66
generic guard counts by path: {'.claude/hooks/pretooluse_guard.py': 1, '.github/workflows/ci.yml': 1, 'ops/cong_cu_test.py': 23, 'ops/evidence/wp685-r28-g5-attempt-1/log/B1-B4_B8_nen_python3.11.log': 1, 'ops/evidence/wp685-r28-g5-attempt-1/log/B1-B4_B8_nen_python3.12.log': 1, 'ops/evidence/wp685-r28-g5-attempt-1/log/B1-B4_B8_ung_vien_python3.11.log': 1, 'ops/evidence/wp685-r28-g5-attempt-1/log/B1-B4_B8_ung_vien_python3.12.log': 1, 'ops/evidence/wp685-r28-g5-attempt-1/log/B2_chot_tinh_python3.11.log': 1, 'ops/evidence/wp685-r28-g5-attempt-1/log/B4_san_windows.log': 1, 'ops/evidence/wp685-r28-g5-attempt-1/log/B5_AW_D_python3.11.log': 1, 'ops/evidence/wp685-r28-g5-attempt-1/log/B5_AW_D_python3.12.log': 1, 'ops/evidence/wp685-r28-g5-attempt-1/log/B5_E_python3.11.log': 1, 'ops/evidence/wp685-r28-g5-attempt-1/log/B5_E_python3.12.log': 1, 'ops/evidence/wp685-r28-g5-attempt-1/log/B6_dotbien_nen_python3.11.log': 1, 'ops/evidence/wp685-r28-g5-attempt-1/log/B6_dotbien_nen_python3.12.log': 1, 'ops/evidence/wp685-r28-g5-attempt-1/log/B6_dotbien_ung_vien_python3.11.log': 1, 'ops/evidence/wp685-r28-g5-attempt-1/log/B6_dotbien_ung_vien_python3.12.log': 1, 'ops/evidence/wp685-r28-g5-attempt-1/log/B6_ruff_nen.log': 1, 'ops/evidence/wp685-r28-g5-attempt-1/log/B6_ruff_ung_vien.log': 1, 'ops/evidence/wp685-r28-g5-attempt-1/log/B6_suite_nen_python3.11.log': 1, 'ops/evidence/wp685-r28-g5-attempt-1/log/B6_suite_nen_python3.12.log': 1, 'ops/evidence/wp685-r28-g5-attempt-1/log/B6_suite_ung_vien_python3.11.log': 1, 'ops/evidence/wp685-r28-g5-attempt-1/log/B6_suite_ung_vien_python3.12.log': 1, 'ops/evidence/wp685-r28-g5-attempt-2/chay_log.sh': 1, 'ops/evidence/wp685-r28-g5-attempt-2/chot_tinh_r12.py': 1, 'ops/lease_publish_test.py': 1, 'ops/nhanh_don_duoc_test.py': 13, 'scripts/tl_core/ingest_engine.py': 1, 'scripts/tl_selftest.py': 4}
ops/cong_cu_test.py:91: TEP_TEST = HERE / "cong_cu_test.py"
ops/cong_cu_test.py:91: TEP_TEST = HERE / "cong_cu_test.py"
ops/cong_cu_test.py:8100:     return {"sha256_test": hashlib.sha256(Path(TEP_TEST).read_bytes()).hexdigest(),
```

Kết luận: KHÔNG PHẢI LỖI — không thấy chốt nguyên byte sống: cả OID/SHA-256 đầy đủ lẫn tiền tố đều không có hit; manifest không chứa .claude. Đã đọc các consumer: import/runpy/copy và phép đếm một mục DA_NOI; các bảng sha256_test băm chính cong_cu_test.py hoặc nhanh_don_duoc_test.py, không băm tệp đang sửa. Băm workflow BAM_GATE_* ghim cấu hình job, không ghim byte nguồn Python. Kết luận giới hạn ở cây HEAD và các phép tìm đã ghi.

### HƯỚNG 4b: N3 bổ sung: tệp được băm và phép đếm nguồn

Giả thuyết: Chốt sha256_test hoặc phép đếm raw source có thể vô tình bao gồm tệp đổi chú thích.

Lệnh (cwd: `/tmp/claude-0/-home-user-tra-luat/6cf1da84-5813-5156-ad6b-b3a2dbd3ab61/scratchpad/rv1`):

```bash
python - <<'PY'
import pathlib, subprocess
p = pathlib.Path('cay-kho/ops/nhanh_don_duoc_test.py')
lines = p.read_text().splitlines()
for n in (5922, 6239, 6332): print(f'{p}:{n}: {lines[n-1]}')
hits = pathlib.Path('/tmp/wp923-n3-git-name.txt').read_text().splitlines()
historic = {s.split(':', 1)[0] for s in hits if s.startswith(('ops/reviews/', 'ops/land/'))}
print('Historical snapshot paths with name hits=' + str(len(historic)))
target = '.claude/dev/ci_dang_ky_test.py'
for rev in ('e139e55883d90fd74a358230be5599c9e223d4b3', '67bacb3b51ac9eda72297b10b15b798b3ca51959'):
    src = subprocess.check_output(['git', '-C', 'cay-kho', 'show', f'{rev}:{target}']).decode()
    print(rev + ': quoted ops/ci_duong_nhanh_test.py count=' + str(src.count('"ops/ci_duong_nhanh_test.py"')))
PY
```

Output thật (exit code 0):

```text
cay-kho/ops/nhanh_don_duoc_test.py:5922: _bam = lambda tep: hashlib.sha256(Path(tep).read_bytes()).hexdigest()   # noqa: E731
cay-kho/ops/nhanh_don_duoc_test.py:6239:     bam_dau = (_bam(__file__), _bam(TOOL))     # nguon doi GIUA luot => manh DO (khong tron hai ban)
cay-kho/ops/nhanh_don_duoc_test.py:6332:     bam = [_bam(__file__), _bam(TOOL)]
Historical snapshot paths with name hits=298
e139e55883d90fd74a358230be5599c9e223d4b3: quoted ops/ci_duong_nhanh_test.py count=1
67bacb3b51ac9eda72297b10b15b798b3ca51959: quoted ops/ci_duong_nhanh_test.py count=1
```

Kết luận: KHÔNG PHẢI LỖI — nhanh_don_duoc ghim __file__ và TOOL của chính nó; phép đếm quoted DA_NOI không đổi (1 ở cả base/head). Các hit ops/reviews/ops/land được tách thành 298 đường dẫn ảnh chụp lịch sử, không phải chốt kỳ vọng hiện tại của tệp này.

### HƯỚNG 5: N2: chạy thật trên reviewed_sha và so log base

Giả thuyết: Chạy lại có thể đỏ, đổi số ca hoặc khác output dù AST bằng nhau.

Lệnh (cwd: `/tmp/claude-0/-home-user-tra-luat/6cf1da84-5813-5156-ad6b-b3a2dbd3ab61/scratchpad/rv1`):

```bash
python - <<'PY'
import hashlib, os, pathlib, re, shutil, subprocess, sys
repo = pathlib.Path('cay-kho').resolve()
head = subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD']).decode().strip()
assert head == '67bacb3b51ac9eda72297b10b15b798b3ca51959'
print('tested_sha=' + head)
print('python=' + sys.version.split()[0])
print('actionlint=' + str(shutil.which('actionlint')))
out = pathlib.Path('/tmp/wp923-n2-reviewed.log')
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0')
with out.open('wb') as f:
    r = subprocess.run(['python', '.claude/dev/ci_dang_ky_test.py'], cwd=repo, env=env, stdout=f, stderr=subprocess.STDOUT)
print('command=python .claude/dev/ci_dang_ky_test.py (cwd=cay-kho; no --chay)')
print('returncode=' + str(r.returncode))
new = out.read_bytes()
for p in (pathlib.Path('n2_base.log'), pathlib.Path('n2_head.log'), out):
    data = p.read_bytes()
    print(f'{p}: bytes={len(data)} sha256={hashlib.sha256(data).hexdigest()}')
    lines = data.decode('utf-8', 'replace').splitlines()
    for line in lines:
        if re.match(r'^(ĐĂNG KÝ:|TRẠNG THÁI:|LAUNCHER WINDOWS:|RUFF CI:|PHẢN CHỨNG:|TỔNG:|ĐỎ:)', line): print('  ' + line)
    print('  mutation_lines=' + str(sum(line.startswith('ĐỘT BIẾN ') for line in lines)))
print('packet_base_equal_packet_head=' + str(pathlib.Path('n2_base.log').read_bytes() == pathlib.Path('n2_head.log').read_bytes()))
print('rerun_equal_packet_base=' + str(new == pathlib.Path('n2_base.log').read_bytes()))
print('rerun_equal_packet_head=' + str(new == pathlib.Path('n2_head.log').read_bytes()))
assert r.returncode == 0 and new.decode().rstrip().endswith('TỔNG: ĐẠT')
assert new == pathlib.Path('n2_base.log').read_bytes() == pathlib.Path('n2_head.log').read_bytes()
PY
```

Output thật (exit code 1):

```text
tested_sha=67bacb3b51ac9eda72297b10b15b798b3ca51959
python=3.13.17
actionlint=/root/.local/bin/actionlint
command=python .claude/dev/ci_dang_ky_test.py (cwd=cay-kho; no --chay)
returncode=1
n2_base.log: bytes=61886 sha256=ef11caf341ed192c60c62430ddb81f53d10b03304fdc871dc29c8ce22b90de88
  ĐĂNG KÝ: 28/28
  TRẠNG THÁI: chan=28 cach_ly=0
  LAUNCHER WINDOWS: 4/4 hợp đồng
  RUFF CI: 3/3 hợp đồng
  PHẢN CHỨNG: 1070/1070 đỏ đúng
  TỔNG: ĐẠT
  mutation_lines=1070
n2_head.log: bytes=61886 sha256=ef11caf341ed192c60c62430ddb81f53d10b03304fdc871dc29c8ce22b90de88
  ĐĂNG KÝ: 28/28
  TRẠNG THÁI: chan=28 cach_ly=0
  LAUNCHER WINDOWS: 4/4 hợp đồng
  RUFF CI: 3/3 hợp đồng
  PHẢN CHỨNG: 1070/1070 đỏ đúng
  TỔNG: ĐẠT
  mutation_lines=1070
/tmp/wp923-n2-reviewed.log: bytes=1911 sha256=2942ef52d79f49d241cbc54b3cb217c0d0e1311e31310720f151c15a5f557c5b
  ĐĂNG KÝ: 28/28
  TRẠNG THÁI: chan=28 cach_ly=0
  LAUNCHER WINDOWS: 4/4 hợp đồng
  RUFF CI: 3/3 hợp đồng
  mutation_lines=0
packet_base_equal_packet_head=True
rerun_equal_packet_base=False
rerun_equal_packet_head=False
Traceback (most recent call last):
  File "<stdin>", line 25, in <module>
AssertionError
```

Kết luận: KHÔNG ĐO ĐƯỢC trong môi trường mặc định — tiến trình test rc=1 trước PHẢN CHỨNG/TỔNG vì git commit của fixture tạm lỗi 128. Hai log packet trùng nhau, nhưng lượt chạy này chưa đạt và không trùng chúng. Cấu hình ký commit kế thừa được cô lập và N2 đã chạy lại thành công tại H5b; không sửa cay-kho.

### HƯỚNG 5b: N2: chạy lại sau khi cô lập cấu hình ký của fixture tạm

Giả thuyết: Lỗi N2 đầu có thể do commit.gpgsign=true toàn cục, thay vì do diff.

Lệnh (cwd: `/tmp/claude-0/-home-user-tra-luat/6cf1da84-5813-5156-ad6b-b3a2dbd3ab61/scratchpad/rv1`):

```bash
git -C cay-kho config --show-origin --get-regexp '^(commit\.gpgsign|gpg\.format)$'
python - <<'PY'
import hashlib, os, pathlib, re, subprocess
repo = pathlib.Path('cay-kho').resolve()
head = subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD']).decode().strip()
assert head == '67bacb3b51ac9eda72297b10b15b798b3ca51959'
print('tested_sha=' + head)
out = pathlib.Path('/tmp/wp923-n2-reviewed-no-sign.log')
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0',
           GIT_CONFIG_COUNT='1', GIT_CONFIG_KEY_0='commit.gpgsign', GIT_CONFIG_VALUE_0='false')
print('process-only override: commit.gpgsign=false for temporary test repositories; no config file changed')
with out.open('wb') as f:
    r = subprocess.run(['python', '.claude/dev/ci_dang_ky_test.py'], cwd=repo, env=env, stdout=f, stderr=subprocess.STDOUT)
print('command=python .claude/dev/ci_dang_ky_test.py (cwd=cay-kho; no --chay)')
print('returncode=' + str(r.returncode))
new = out.read_bytes()
print('rerun_bytes=' + str(len(new)) + ' sha256=' + hashlib.sha256(new).hexdigest())
lines = new.decode('utf-8', 'replace').splitlines()
for line in lines:
    if re.match(r'^(ĐĂNG KÝ:|TRẠNG THÁI:|LAUNCHER WINDOWS:|RUFF CI:|PHẢN CHỨNG:|TỔNG:|ĐỎ:)', line): print(line)
print('mutation_lines=' + str(sum(s.startswith('ĐỘT BIẾN ') for s in lines)))
for p in ('n2_base.log', 'n2_head.log'):
    print('byte_equal_' + p + '=' + str(new == pathlib.Path(p).read_bytes()))
assert r.returncode == 0 and new.decode().rstrip().endswith('TỔNG: ĐẠT')
assert new == pathlib.Path('n2_base.log').read_bytes() == pathlib.Path('n2_head.log').read_bytes()
PY
```

Output thật (exit code 0):

```text
file:/root/.gitconfig	gpg.format ssh
file:/root/.gitconfig	commit.gpgsign true
tested_sha=67bacb3b51ac9eda72297b10b15b798b3ca51959
process-only override: commit.gpgsign=false for temporary test repositories; no config file changed
command=python .claude/dev/ci_dang_ky_test.py (cwd=cay-kho; no --chay)
returncode=0
rerun_bytes=61886 sha256=ef11caf341ed192c60c62430ddb81f53d10b03304fdc871dc29c8ce22b90de88
ĐĂNG KÝ: 28/28
TRẠNG THÁI: chan=28 cach_ly=0
LAUNCHER WINDOWS: 4/4 hợp đồng
RUFF CI: 3/3 hợp đồng
PHẢN CHỨNG: 1070/1070 đỏ đúng
TỔNG: ĐẠT
mutation_lines=1070
byte_equal_n2_base.log=True
byte_equal_n2_head.log=True
```

Kết luận: KHÔNG PHẢI LỖI — N2 chạy thật trên exact HEAD đạt rc=0, 28/28 đăng ký và 1070/1070 phản chứng; output trùng nguyên byte n2_base.log và n2_head.log. Chỉ tắt ký cho tiến trình fixture, không sửa cấu hình hoặc nội dung kho.

### HƯỚNG 6: Câu có mốc, bảo toàn lịch sử và giới hạn write set

Giả thuyết: Bản sửa có thể viết lại câu lịch sử hoặc tạo khẳng định hiện tại mới sẽ lại cũ.

Lệnh (cwd: `/tmp/claude-0/-home-user-tra-luat/6cf1da84-5813-5156-ad6b-b3a2dbd3ab61/scratchpad/rv1`):

```bash
git -C cay-kho diff --check e139e55883d90fd74a358230be5599c9e223d4b3 67bacb3b51ac9eda72297b10b15b798b3ca51959
python - <<'PY'
import subprocess
b, h = 'e139e55883d90fd74a358230be5599c9e223d4b3', '67bacb3b51ac9eda72297b10b15b798b3ca51959'
p = '.claude/dev/ci_dang_ky_test.py'
git = lambda *a: subprocess.check_output(['git', '-C', 'cay-kho', *a]).decode()
before, after = [git('show', f'{r}:{p}').splitlines() for r in (b, h)]
for n in (758, 760, 761, 808, 978):
    line = before[n-1]
    positions = [i for i, s in enumerate(after, 1) if s == line]
    print(f'historical/context base:{n} preserved_at_head={positions}: {line}')
    assert len(positions) == 1
for n in (759, 808, 809): print(f'head:{n}: {after[n-1]}')
assert after[808] == '# #910 pha B (PR #917, a7da463): tran job manh 30 -> 150; job gom van 10.'
assert after[807] == before[807]
assert '(nay 105)' not in '\n'.join(after)
added = git('diff', '--numstat', b, h).splitlines()
print('write_set:', added)
assert len(added) == 1 and added[0].split('\t')[2] == p and int(added[0].split('\t')[0]) <= 20
print('diff_check=passed; history_preserved=True; newly_added_timeout_claims_are_anchored_to_#910_and_a7da463=True')
PY
```

Output thật (exit code 0):

```text
historical/context base:758 preserved_at_head=[758]: # #643 (chủ kho chọn "b", PR #644): 3600 → 4500. Đo run 36208617323, N=2 chế độ đủ: `nhanh_don_duoc_test` 3306,45 s = 92 %
historical/context base:760 preserved_at_head=[760]: # Windows ép N=1 ⇒ dài hơn; trần job là trần NGOÀI. Ca `p643-tran-bo-nho-hon-timeout-job` chỉ khoá trần bộ < trần job.
historical/context base:761 preserved_at_head=[761]: # #705 (CI-REGISTRY-NANG-TRAN-BO-DAY-DU, chủ kho Q4): 4500 → 5400, job 90 → 105 phút. `nhanh_don_duoc_test` chế độ đủ:
historical/context base:808 preserved_at_head=[808]: # WP748 r16: hai job nay la `targeted_mutant_gate` (NHANH_DON_DUOC_DICH, gom `--gop-dich`, tran 30 phut).
historical/context base:978 preserved_at_head=[979]:     # WP748 r16: full_mutant_audit ~73 800 s noi tiep (g12) => 8 manh x ~2,6 h => tran 360 (tran job GitHub).
head:759: # trần cũ. KHÔNG bảo đảm cả job dưới `timeout-minutes` (#705: 105 · #910 pha B, a7da463: 150): bộ ấy còn chờ worker trống (run trên: bắt đầu sau 337 s),
head:808: # WP748 r16: hai job nay la `targeted_mutant_gate` (NHANH_DON_DUOC_DICH, gom `--gop-dich`, tran 30 phut).
head:809: # #910 pha B (PR #917, a7da463): tran job manh 30 -> 150; job gom van 10.
write_set: ['2\t1\t.claude/dev/ci_dang_ky_test.py']
diff_check=passed; history_preserved=True; newly_added_timeout_claims_are_anchored_to_#910_and_a7da463=True
```

Kết luận: KHÔNG PHẢI LỖI — dòng WP748 r16 và câu #705 còn nguyên; thông tin 150 được gắn mốc #910/a7da463, câu job gom 10 nằm trong cùng câu có mốc. Một tệp, +2/−1, không lỗi diff --check; không cần vá thêm.

### HƯỚNG 7: N4 bổ sung: tự kiểm runtime trên exact HEAD

Giả thuyết: Khai báo 1731/1731 của executor có thể không tái hiện trên commit đang review.

Lệnh (cwd: `/tmp/claude-0/-home-user-tra-luat/6cf1da84-5813-5156-ad6b-b3a2dbd3ab61/scratchpad/rv1`):

```bash
python - <<'PY'
import hashlib, os, pathlib, re, subprocess
repo = pathlib.Path('cay-kho').resolve()
head = subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD']).decode().strip()
assert head == '67bacb3b51ac9eda72297b10b15b798b3ca51959'
print('tested_sha=' + head)
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0', GIT_CONFIG_COUNT='1', GIT_CONFIG_KEY_0='commit.gpgsign', GIT_CONFIG_VALUE_0='false')
out = pathlib.Path('/tmp/wp923-tl-selftest.log')
with out.open('wb') as f:
    r = subprocess.run(['python', 'scripts/tl.py', '--selftest'], cwd=repo, env=env, stdout=f, stderr=subprocess.STDOUT)
data = out.read_bytes()
print('command=python scripts/tl.py --selftest (cwd=cay-kho)')
print('returncode=' + str(r.returncode))
print(f'log_bytes={len(data)} log_sha256={hashlib.sha256(data).hexdigest()}')
lines = data.decode('utf-8', 'replace').splitlines()
print('last 8 output lines:')
print('\n'.join(lines[-8:]))
print('lines_starting_FAIL=', sum(bool(re.match(r'^(FAIL|FAILED|ERROR|Traceback)', s)) for s in lines))
assert r.returncode == 0
assert any(re.search(r'1731/1731', s) for s in lines), 'missing expected positive count'
PY
```

Output thật (exit code 0):

```text
tested_sha=67bacb3b51ac9eda72297b10b15b798b3ca51959
command=python scripts/tl.py --selftest (cwd=cay-kho)
returncode=0
log_bytes=78392 log_sha256=0ac435059f2948c5f21795114520fdfdd996d10e0ec78e8ad34dac769e174bf4
last 8 output lines:
  [OK] wp43_bundled_generator_byte_canonical
  [OK] wp43_release_excludes_only_canonical_fragment_prefix
  [OK] wp44_dev_topology_prefers_fragments
  [OK] wp44_release_bundle_topology_under_200
  [OK] wp44_missing_bundled_module_named
  [OK] r332_registry_coverage_duong_san_xuat
  [OK] wp42_complete_runtime_test_ids_unique
== tl selftest 1731/1731 ==
lines_starting_FAIL= 0
```

Kết luận: KHÔNG PHẢI LỖI — tự chạy python scripts/tl.py --selftest trên exact HEAD, rc=0 và 1731/1731; log đầy đủ giữ ngoài repository.

### HƯỚNG 8: Toàn vẹn cuối lượt và giới hạn xác minh

Giả thuyết: Các phép đo có thể làm bẩn kho hoặc HEAD đổi trong khi review; N5 có thể bị nhận nhầm là đã xanh.

Lệnh (cwd: `/tmp/claude-0/-home-user-tra-luat/6cf1da84-5813-5156-ad6b-b3a2dbd3ab61/scratchpad/rv1`):

```bash
git -C cay-kho rev-parse HEAD HEAD^{tree}
git -C cay-kho status --porcelain=v1 --untracked-files=all
git -C cay-kho diff --exit-code HEAD --
sha256sum SPEC.md
python - <<'PY'
import pathlib, subprocess
print('Initial N2 failure, actual final traceback line:')
print(pathlib.Path('/tmp/wp923-n2-reviewed.log').read_text().splitlines()[-1])
print('N5=not_run: no network/check-run request; no CI check-run artifact supplied in packet')
repo = pathlib.Path('cay-kho')
head = subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD']).decode().strip()
assert head == '67bacb3b51ac9eda72297b10b15b798b3ca51959'
assert not subprocess.check_output(['git', '-C', str(repo), 'status', '--porcelain=v1', '--untracked-files=all'])
print('final_head_matches=True; final_worktree_clean=True')
PY
```

Output thật (exit code 0):

```text
67bacb3b51ac9eda72297b10b15b798b3ca51959
8512df452237dad95f764b23204ebd8387d69fdb
a36f8d2d84d39c3587a60edcb63d4886f82e3fae097c283700718b5869eecbc1  SPEC.md
Initial N2 failure, actual final traceback line:
subprocess.CalledProcessError: Command '['git', '-C', '/tmp/tmpwbay6kaq', '-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-qm', '0']' returned non-zero exit status 128.
N5=not_run: no network/check-run request; no CI check-run artifact supplied in packet
final_head_matches=True; final_worktree_clean=True
```

Kết luận: KHÔNG PHẢI LỖI về tính toàn vẹn — HEAD/tree/SPEC còn khớp, worktree sạch, không đổi tệp trong cay-kho. N5: KHÔNG ĐO ĐƯỢC (not_run), không có check-run artifact và không gọi API theo chỉ thị; không coi là CI passed. Lỗi N2 mặc định đã được xử lý ở H5b bằng cấu hình riêng của tiến trình fixture.

## FINDINGS

Không có finding P0/P1/P2/P3. Độ tin: cao đối với phạm vi diff và các phép đo local đã ghi; N5 chưa đo.
