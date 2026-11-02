verdict: approve
reviewed_head: 6e09f4b013629ae3d8d6e75f1a1c8e10aaa960b4
reviewed_sha: 6e09f4b013629ae3d8d6e75f1a1c8e10aaa960b4
reviewed_tree: ada1abd0e19f41751c5407b7bb0ecc251113316a
review_class: sensitive
provider: openai_codex
model: gpt-6.1-sol
model_family: openai
reasoning_effort: xhigh
execution_surface: codex_cli
transport: machine
review_round: 1/2

## Kết luận

**Approve trong phạm vi bản vá được review offline.** Không phát hiện P0/P1/P2/P3 mở do bản vá. Đúng delta r2: bốn job lên 150, `gate-nhanh-manh` giữ 30, snapshot topology cập nhật đúng ba giá trị và đột biến timeout vẫn có răng.

N4 **chưa chứng minh N/N toàn bộ**: bộ đường nhanh đỏ giống hệt base vì sandbox cấm bind socket Unix; registry đạt sau chuẩn hóa cấu hình Git riêng cho commit fixture. N3 thiếu shellcheck. N5 (CI lượt PR và launcher dispatch xanh trên exact head) **KHÔNG ĐO ĐƯỢC** trong bundle offline, không có run/check evidence để xác nhận; cần bằng chứng này khi xét điều kiện merge của spec. Verdict này là kết quả review code, không tự cấp merge/land/deploy hay xác nhận lease live.

## Neo và môi trường

Đã đọc `runs/2073ebe8/prompt.snapshot`, cả spec r1 và delta r2, lease offline cùng chỉ dẫn repository liên quan reviewer. Không suy authority live từ bản sao lease `wp910-r2-g2-claude`.

| Neo | Đầu lượt | Cuối lượt |
|---|---|---|
| Head SHA | `6e09f4b013629ae3d8d6e75f1a1c8e10aaa960b4` | không đổi |
| Head tree | `ada1abd0e19f41751c5407b7bb0ecc251113316a` | không đổi |
| Base SHA | `e739ac1b74024a20949425c447fb6cf025317c0e` | không đổi |
| Base tree | `e3972d62cea7830c73c6b484e54977f21cd9751e` | không đổi |
| `git status --porcelain=v1 --untracked-files=all` | rỗng ở cả hai cây | rỗng ở cả hai cây |

Lệnh neo: `git -C cay-kho rev-parse HEAD 'HEAD^{tree}'`, tương tự cho `nen`; lệnh status như bảng. Cuối lượt kiểm thêm `git diff --binary`, `git diff --cached --binary`, `git ls-files --others --ignored --exclude-standard`: đều rỗng ở cả hai cây. `git -C cay-kho diff --check e739ac1b74024a20949425c447fb6cf025317c0e HEAD`: rc=0, output rỗng. Hai clone thực tế detached HEAD đúng OID được giao, `core.abbrev=7`.

SHA-256 tự đo bằng `sha256sum evidence/spec-r1.md evidence/spec-r2.md` (đo lại cuối lượt bằng hashlib):

```text
2383ca2e540203e0b449e3f6118d84817f81984e937d463e99a7b862449a6613  evidence/spec-r1.md
c3179d006b46fa82fe144cc1200dab72dbd9e88de28159f541504a7831dde7fc  evidence/spec-r2.md
```

Cả hai khớp giá trị bắt buộc. Diff đo trực tiếp base..head khớp từng byte `evidence/diff.patch`: đúng 3 tệp, 8 dòng thêm/8 dòng bỏ (`ci.yml` 3/3; launcher 1/1; test 4/4), trong write set và ngân sách. `.claude/dev/ci_dang_ky_test.py` giữ nguyên byte.

Header khởi tạo đúng run tại `runs/2073ebe8/stderr.log:2–12` công bố Codex v0.163.0, model `gpt-6.1-sol`, reasoning effort `xhigh`, session `01a16d81-8e8f-7ab1-8373-ce1e4239e547`; bản trích [cli-header.log](cli-header.log). Header chỉ chứng minh thông số CLI công bố. Launcher ngoài khai `local_process/subprocess`; reviewer bên trong là Codex CLI theo header. Python 3.13.16, PyYAML 6.0.3, actionlint 1.7.7; shellcheck và pwsh vắng. Tool `environment_status` không được cung cấp.

Sandbox `workspace-write`; reviewer chỉ ghi `out/`, giữ `cay-kho/`, `nen/`, `kho.git/` nguyên trạng. Mọi test dùng bản sao độc lập `out/copy-base`/`out/copy-head`, `TMPDIR` tuyệt đối dưới `out/tmp`, `PYTHONDONTWRITEBYTECODE=1` và Python `-B`. Không gọi GitHub/Internet. Signer Git kế thừa trong lượt registry đầu đã thử loopback và bị sandbox từ chối; đã bỏ phụ thuộc đó chỉ cho commit fixture ở lượt chạy lại.

Kiểm kê SHA-256 toàn bộ 5.385 tệp mỗi checkout (không gồm `.git`) tại mốc giữa lượt và cuối lượt giống nhau; không có tệp mới/đổi, gồm cả ignored. Hai mốc sạch không chứng minh lịch sử chưa từng ghi rồi hoàn nguyên; các thao tác review không sửa checkout. Chứng cứ [anchors-start.json](anchors-start.json), [anchors-end.json](anchors-end.json), [content-snapshot.json](content-snapshot.json), [actual.diff](actual.diff).

## Bảng finding

| ID | Mức P0–P3 | Tệp:dòng | Bằng chứng | Hướng sửa bằng lời |
|---|---|---|---|---|
| — | — | — | Không có finding mở thuộc bản vá; các hạn chế môi trường và nợ nền nêu riêng bên dưới. | Không yêu cầu sửa sản phẩm trong lượt này. |

## Bảng N1–N4

| Kiểm tra | Kết quả | Bằng chứng độc lập |
|---|---|---|
| N1 | PASS | YAML đã parse: `ci.yml` gate 60→150 tại dòng 125, gate-ops 60→150 tại dòng 647, gate-packet-loop 120→150 tại dòng 1030; launcher 40→150 tại dòng 54. Workflow diff chỉ đúng 4 dòng timeout cấp job. |
| N2 | PASS | 12 tuple mỗi cây, 4 đổi/8 giữ nguyên; mọi cấu trúc YAML khác bằng nhau sau khi hoàn nguyên bốn giá trị trong dữ liệu sao. Job gate-nhanh-manh giữ 30; cả block 1.165 byte giữ nguyên. |
| N3 | PASS phần actionlint; shellcheck KHÔNG ĐO ĐƯỢC | `actionlint .github/workflows/ci.yml` và `actionlint .github/workflows/launcher-windows.yml` từ từng clone base/head: cả 4 rc=0, stdout/stderr rỗng, delta=0. Actionlint 1.7.7; `command -v shellcheck` không có công cụ. |
| N4 | PARTIAL; N/N toàn bộ KHÔNG ĐO ĐƯỢC | Đường nhanh base=head: 103/104 ca, 387/392 đột biến, rc=1 do cùng lỗi sandbox; không gọi là xanh. Registry sau chuẩn hóa Git fixture: base=head 24/24, 1070/1070 phản chứng, `TỔNG: ĐẠT`, rc=0. Mutant timeout đạt riêng, hai đối chứng âm đỏ đúng. |

Lệnh trích/so YAML: `PYTHONDONTWRITEBYTECODE=1 python3 -B out/check_n12.py` (rc=0), dùng `yaml.safe_load`, thu mọi timeout khai tường minh cấp job và bước của cả hai workflow (bước vắng timeout không có tuple). Không suy từ grep. Lưu đầy đủ [timeouts.json](timeouts.json), [n12.log](n12.log); bảng base/head:

| Tệp | Job | Bước | Base | Head |
|---|---|---|---:|---:|
| .github/workflows/ci.yml | chuan-bi | <job> | 20 | 20 |
| .github/workflows/ci.yml | chuan-bi | 1: actions/checkout@v4 | 10 | 10 |
| .github/workflows/ci.yml | chuan-bi | 2: phan loai diff (duong nhanh ho so - chi pull_request) | 5 | 5 |
| .github/workflows/ci.yml | gate | <job> | 60 | 150 |
| .github/workflows/ci.yml | gate-cong-cu | <job> | 150 | 150 |
| .github/workflows/ci.yml | gate-cong-cu-gop | <job> | 10 | 10 |
| .github/workflows/ci.yml | gate-ops | <job> | 60 | 150 |
| .github/workflows/ci.yml | gate-nhanh-manh | <job> | 30 | 30 |
| .github/workflows/ci.yml | gate-nhanh-gop | <job> | 10 | 10 |
| .github/workflows/ci.yml | gate-registry | <job> | 105 | 105 |
| .github/workflows/ci.yml | gate-packet-loop | <job> | 120 | 150 |
| .github/workflows/launcher-windows.yml | launcher | <job> | 40 | 150 |

Ngoài bốn timeout, parse toàn bộ workflow bằng nhau. Bộ test topology chỉ đổi snapshot gate/gate-ops/gate-packet-loop từ 60/60/120 sang 150, giữ snapshot gate-nhanh-manh=30; dòng mutant chuyển neo literal 60 sang 150. Block gate-nhanh-manh cùng SHA-256 `c1fec974b35d86b0a3ff6a8f829120c24b02e44f2384c5f59fc8fecc1256fe48`. Chứng cứ actionlint: [n3.json](n3.json), bốn log `actionlint-*.log`.

### N4: lệnh, output và giới hạn

Từ từng cwd `out/copy-base` và `out/copy-head`, chạy đúng lệnh (TMPDIR tuyệt đối dưới `out/tmp`):

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B ops/ci_duong_nhanh_test.py
PYTHONDONTWRITEBYTECODE=1 python3 -B .claude/dev/ci_dang_ky_test.py
```

Không dùng `--chay`. Output đường nhanh, **giống nhau ở base/head**:

```text
[HONG] t20zo_la_khong_phai_tep_thuong_do: PermissionError: [Errno 1] Operation not permitted
CA: 103/104 dat · 0 do · 1 hong
DOT BIEN: 387/392 bi giet dung ly do
TU KIEM PHAN HANG: DAT (5 mau rc, 3 dot bien that)
TONG: DO
rc=1
```

Đã chạy riêng `--mot-ca t20zo_la_khong_phai_tep_thuong_do`: rc=4, traceback tại `ops/ci_duong_nhanh_test.py:1702`, `s.bind(ten)` → EPERM. Đó là fixture socket Unix; không phải timeout CI hay lỗi assertion của bản vá. Năm đột biến không đủ baseline xanh vì cùng ca này, ở cả hai cây: `symlink_treo_khong_theo_bi_danh`, `la_bo_chot_tep_thuong`, `la_cho_phep_fifo`, `la_cho_phep_socket`, `la_khong_theo_symlink`. Không sửa/skip test hay giả socket để tạo N/N. [permission-repro.log](permission-repro.log), [n4-mutation-blockers.json](n4-mutation-blockers.json), [n4-base-duong-nhanh.log](n4-base-duong-nhanh.log), [n4-head-duong-nhanh.log](n4-head-duong-nhanh.log).

Registry nguyên trạng cả hai cây rc=1, in `ĐĂNG KÝ: 24/24`, `LAUNCHER WINDOWS: 4/4 hợp đồng`, `RUFF CI: 3/3 hợp đồng`, rồi dừng trước `TỔNG:` vì commit fixture thất bại. Đo riêng cho thấy global `commit.gpgsign=true` gọi signer loopback bị cấm socket, `fatal: failed to write commit object`; [registry-git-repro.log](registry-git-repro.log). Ruff ở đây chỉ là kiểm hợp đồng workflow, không phải chạy bare Ruff lint.

Chạy lại bằng [rerun_registry.py](rerun_registry.py), vẫn cùng lệnh, chỉ bổ sung entry `commit.gpgsign=false` vào `GIT_CONFIG_COUNT` của tiến trình test, giữ entry kế thừa. Đây là chuẩn hóa cho commit fixture tạm trong `out/tmp`; không thay Git config hay mã nguồn của clone. Kết quả **cả base và head**:

```text
ĐĂNG KÝ: 24/24
PHẢN CHỨNG: 1070/1070 đỏ đúng
TỔNG: ĐẠT
rc=0
```

Chứng cứ [n4.json](n4.json) cho lượt nguyên trạng, [n4-registry-fixture-env.json](n4-registry-fixture-env.json), [n4-base-dang-ky-fixture-env.log](n4-base-dang-ky-fixture-env.log), [n4-head-dang-ky-fixture-env.log](n4-head-dang-ky-fixture-env.log). File registry head/base SHA-256 `50fb62e422543e15e73e4495d64f7b82290c4056dcd9bebe0ecdbeb5e1982f10` bằng nhau.

### N4: răng mutant timeout

Lệnh `PYTHONDONTWRITEBYTECODE=1 python3 -B out/check_mutant.py` (rc=0). Đọc chính entry `yml_gate_timeout_1_phut` và chạy harness thật trên bản sao; neo mới:

```text
(\n  gate:\n.*?\n    timeout-minutes: )150\n
```

Output thật (rút dòng log, giữ nội dung):

```text
regex matches: 1; match lies inside gate block; parsed delta: gate.timeout-minutes 150 -> 1 only
target: y13_khoa_topology_cua_ci_yml_ngoai_than_run
baseline rc: 0
mutant rc: 3
mutant stdout: DO:y13_khoa_topology_cua_ci_yml_ngoai_than_run:gate: cau hinh cap job lech khung (runs-on/needs/strategy/timeout/env/...): khac ['timeout-minutes']
production harness: GIET
```

Hai đối chứng âm sửa riêng dòng neo trong bản sao test, giữ các ca và harness: đổi literal 150 về 60; đổi tên neo `gate` sang job không tồn tại. Mỗi lượt harness trả rc=1:

```text
DOT BIEN: 0/1 bi giet dung ly do
yml_gate_timeout_1_phut: HONG RuntimeError: ha tang: neo regex phai khop DUNG MOT lan, thay 0: ...
TONG: DO
```

Vì vậy neo vô hiệu không thể được tính là GIẾT hay lặng lẽ xanh. [mutant.log](mutant.log), [mutant.json](mutant.json), [negative-anchor-stale-60.log](negative-anchor-stale-60.log), [negative-anchor-removed-job-anchor.log](negative-anchor-removed-job-anchor.log). Đây là dữ liệu phản chứng trong scratch, không phải patch sản phẩm.

## Các hướng săn độc lập

### H1 — test/công cụ khác ghim timeout cũ, đặc biệt Windows/LAND

**Giả thuyết:** còn consumer ngoài write set ghim 60/120/40, khiến Ubuntu PR xanh nhưng Windows hoặc LAND đỏ.

**Lệnh:** `rg -n --hidden --no-ignore -g '*.py' -g '*.sh' -g '*.ps1' -g '*.yaml' -g '*.yml' -g '*.json' -g '*.toml' -g '!**/.git/**' -g '!**/node_modules/**' 'timeout-minutes|BAM_GATE_[A-Z_]+' cay-kho` (174 dòng, lưu [hunt-timeout-references.log](hunt-timeout-references.log)); thêm quét timeout/60/120/40 [hunt-old-timeouts.log](hunt-old-timeouts.log) và danh sách consumer [workflow-consumers.txt](workflow-consumers.txt). Kiểm mã tại `.claude/dev/chay-cong-windows.ps1:102`, `.claude/dev/chay-cong-windows_test.ps1:388–400,1097`. Chạy `PYTHONDONTWRITEBYTECODE=1 python3 -B out/hunt.py` (rc=0): trích mặc định `HanGiay`, tính đúng biểu thức t9 bằng YAML; chạy nguyên đoạn Python nhúng `Doc-DauVanCi` của test, cho từng cây.

**Output thật:**

```text
base: HanGiay=6300; max_gate_minutes=150; max_jobs=[gate-cong-cu]; t9_equivalent_predicate=false
head: HanGiay=6300; max_gate_minutes=150; max_jobs=[gate, gate-cong-cu, gate-ops, gate-packet-loop]; t9_equivalent_predicate=false
windows_fingerprint_rc: base=0, head=0
windows_fingerprint: base == head (workflow + toàn bộ 9 job gate*)
```

Fingerprint Python của Windows bỏ timeout/strategy/needs/runs-on cấp job theo thiết kế, nên bốn thay đổi không đòi cập nhật fingerprint. t9 sẽ đỏ với mặc định 6.300 giây ở **cả base lẫn head** vì base đã có gate-cong-cu=150. Đây là nợ nền ngoài bản vá; nếu xử lý sau, chủ kho có thể cấp write set nâng mặc định và tài liệu Windows lên ít nhất 9.000 giây rồi đo native. Không đề nghị sửa ngoài spec trong packet này.

**Kết luận: KHÔNG PHẢI LỖI mới của bản vá.** Không tìm thêm chốt literal cũ liên quan trong các tham chiếu đã kiểm; tìm kiếm tĩnh không chứng minh mọi consumer động. PowerShell native/Windows/LAND đầy đủ **KHÔNG ĐO ĐƯỢC**, vắng pwsh. Bằng chứng [hunt.log](hunt.log), [hunt.json](hunt.json), `windows-fingerprint-{base,head}.log`.

### H2 — băm khác bao trùm các job vừa đổi

**Giả thuyết:** `BAM_GATE_REGISTRY` hoặc `BAM_GATE_NHANH` gián tiếp phủ gate/gate-ops/gate-packet-loop hoặc launcher, khiến file ngoài write set đỏ.

**Lệnh:** `PYTHONDONTWRITEBYTECODE=1 python3 -B out/hunt.py`, gọi thật `bam_gate_registry`, `bam_gate_nhanh`, `loi_gate_nhanh`, `loi_vung_thiet_lap` từ registry bản sao trên YAML base/head. Đọc định nghĩa tại `.claude/dev/ci_dang_ky_test.py:873–885`. Đổi từng timeout của ba job đã sửa thành 149 trên dữ liệu sao; thêm đối chứng đổi protected job gate-registry và gate-nhanh-manh thành 150.

**Output thật:**

```text
base == head:
bam_gate_registry=e2726e28ae7ecc869cd9df6c975e58f71c3c656594a509c9c2e4b9047c47bb4d
bam_gate_nhanh=301d30a212b34bcff14390a3353084a9af0385fe917c76ab33a22cdc054e2e26
pinned_hashes_match=true
changed_jobs_outside_hashes=true
protected_timeout_negative_controls_detected=true
loi_gate_nhanh=[]; loi_vung_thiet_lap=[] (assertions đã chạy)
```

**Kết luận: KHÔNG PHẢI LỖI.** Băm registry chỉ gồm gate-registry và env/defaults cấp workflow; băm nhanh chỉ gồm hai job nhanh. Cả hai giữ nguyên; launcher không thuộc đầu vào. Hai đối chứng protected làm băm lệch, nên phép đo có độ nhạy. Registry 24/24 và 1070/1070 đạt độc lập sau chuẩn hóa fixture xác nhận thêm. [hunt.py](hunt.py), [hunt.json](hunt.json).

### H3 — gate-nhanh-manh vô tình đổi dù vẫn hiển thị 30

**Giả thuyết:** timeout bằng 30 nhưng nội dung job hoặc snapshot đã trôi ở r2.

**Lệnh:** `PYTHONDONTWRITEBYTECODE=1 python3 -B out/check_n12.py`, so bytes block giữa hai job và toàn cấu trúc YAML, rồi phép băm/registry của H2.

**Output thật:**

```text
timeout tuples: base=12, head=12, changed=4, unchanged=8
gate-nhanh-manh block: byte-identical, 1165 bytes, sha256=c1fec974b35d86b0a3ff6a8f829120c24b02e44f2384c5f59fc8fecc1256fe48
N1: PASS
N2: PASS
```

**Kết luận: KHÔNG PHẢI LỖI.** Dict snapshot giữ 30, băm hai job nhanh vẫn khớp và registry không bị sửa. [n12.log](n12.log), [actual.diff](actual.diff).

### H4 — chú thích timeout cũ trong workflow

**Giả thuyết:** chú thích vẫn nói trần cũ, có thể gây hiểu sai.

**Lệnh:** đọc có số dòng `ci.yml:108–128,1014–1034`, toàn launcher; trích comment đối chiếu base/head vào [hunt-comments.json](hunt-comments.json).

**Output thật trên head (base giữ nguyên):**

```text
ci.yml:118: # Nâng tiếp 45 -> 60 theo chỉ đạo chủ kho. Nhưng A5 KHÔNG còn đòi Windows: xem đặc
ci.yml:119: # tả r3. Trần 60 là chỗ trống cho lần ĐO SAU, không phải lời hứa rằng Windows sẽ qua.
ci.yml:1028: # WP856 (chu kho, PR #866): 60 -> 120. Run 39722546630: Ubuntu 40,4 phut (truoc 22,4) sau khi
ci.yml:1029: # #856 them ma tran T1-T6; Windows van chay o phut ~46, sat tran 60.
launcher timeout 40 comments: 0 (theo mẫu quét)
```

**Kết luận: KHÔNG PHẢI LỖI cần sửa trong packet.** Ghi nhận comment gate dễ bị đọc như mô tả hiện tại; comment packet-loop có mốc WP856 nên là lịch sử. Theo chỉ thị review và write set chỉ bốn dòng timeout, chỉ ghi nhận, không mở finding P3 hay yêu cầu mở rộng phạm vi.

### H5 — timeout 150 xung đột needs hoặc giới hạn nền tảng

**Giả thuyết:** job phụ thuộc có deadline ngắn hơn, hoặc 150 không được GitHub Actions chấp nhận.

**Lệnh:** `PYTHONDONTWRITEBYTECODE=1 python3 -B out/hunt.py` trích DAG từ YAML base/head; đọc `needs` và matrix của launcher; bốn lượt actionlint N3.

**Output thật:**

```text
needs_edges: base == head
changed_job_consumers: {"gate": [], "gate-ops": [], "gate-packet-loop": []}
launcher: không có needs
actionlint: 4/4 rc=0, stdout/stderr rỗng
```

**Kết luận: KHÔNG PHẢI LỖI về needs trong cấu hình.** Cả ba job đổi ở ci.yml chỉ needs chuan-bi; không có downstream deadline job nào tác động lên chúng. Topology, điều kiện chạy, matrix và concurrency giữ nguyên. **KHÔNG ĐO ĐƯỢC** giới hạn dịch vụ GitHub hiện hành hoặc khả năng job thực sự chạy 150 phút trong môi trường của kho: không có mạng hay evidence runtime của đúng head. Không dùng actionlint hoặc một timeout 360 có sẵn trong kho làm bằng chứng thay cho giới hạn nền tảng. N5 vẫn cần bằng chứng riêng như phần kết luận.

## Phạm vi kết quả và bàn giao

Không có finding P0–P3 mở do patch; không có bản vá sản phẩm. Phần chưa đo được: ca cần bind socket Unix và 5 đột biến phụ thuộc trong N4; shellcheck; Windows/PowerShell/LAND native; giới hạn dịch vụ và CI/dispatch exact-head N5; authority/lease live. Các phần này không được khai PASS. Hai cây gốc sạch, exact SHA/tree không đổi ở cuối lượt; mọi script đo, bản sao và log do reviewer tạo nằm trong `out/`.
