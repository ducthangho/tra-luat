verdict: dang_lam
reviewed_sha: 06a50c5feea77c2654f31edd26efeed7eeee62f5

## BẢNG ĐO
| khẳng định | PR khai | đo được (lệnh) | khớp? |
|---|---|---|---|
| Đối tượng review và diff | 06a50c5…; base 9e9a74b; CLAUDE.md +21/-9 | preflight: HEAD/tree, cây đầy đủ, diff byte-match, numstat 21/9 | Có |
| outputs.os: push master / PR thường | [ubuntu-latest] | matrix: cả hai ca = [ubuntu-latest] | Có |
| outputs.os: PR nhãn windows / workflow_dispatch | [ubuntu-latest, windows-latest] | matrix: PR windows, dispatch master và dispatch feature đều đúng | Có |
| Mốc đo 22-10-2026 trên 9e9a74b | Cùng biểu thức tại head review | matrix: expression_same_as_9e9a74b=True; ngày commit head = 22-10-2026 | Có |
| P2 cũ master-windows-bo-sot-dispatch | Giới hạn vào Windows tự động khi push master | matrix: push master một OS, dispatch master hai OS; câu hệ quả giới hạn PR/push | Có |
| Run 39354156843 | 23 job; 23 nhãn ubuntu-latest; 0 Windows | readback: total_count=len=unique_ids=23; labels {(ubuntu-latest,):23}; Windows=0 | Có |
| Run: workflow, event, SHA, ngày | ci.yml; push master; 3a3a3ca; 20-10-2026 | readback: metadata path=.github/workflows/ci.yml; event=push; head_branch=master; 3a3a3caca5de4934ff53851feb6994c2c7b84ad5; 2026-10-20 | Có |
| Windows tự động khi push master | launcher-windows.yml; paths .claude/dev/** hoặc chính workflow | launcher: push.branches=[master]; push.paths khớp cả hai path | Có |
| Ma trận launcher cho push/PR | windows-latest + ubuntu-latest | launcher: push và pull_request hai OS; dispatch mặc định windows-only (phạm vi riêng) | Có |
| Launcher: PR nhãn windows và labeled | Job chỉ chạy nếu PR có nhãn; types chứa labeled | launcher: if và types khớp; PR còn lọc paths=.claude/dev/** | Có |
| Launcher chỉ đo lane launcher | KHÔNG phải gate ci.yml | launcher: liệt kê toàn bộ run; doctor, launcher_test, probes; không gọi battery gate của ci.yml | Có |
| Mọi workflow còn lại | ci-dot-bien-du và ops-* đều ubuntu-latest | workflows: liệt kê đủ 7 tệp tại SHA; 5 workflow còn lại, toàn bộ 5 job ubuntu-latest | Có |
| Cổng doctrine-scan | rc=0, sạch | gates: rc=0; output sạch, 0 chỗ chép doctrine | Có |
| Cổng doc-claims-check | rc=0 và ok=true | gates: rc=0; JSON ok=true | Có |
| ci.yml: mặc định pull_request, không labeled | Không khai types; gắn nhãn đơn thuần không sinh ci.yml run | events: pull_request=null, types absent; commit 3736fc0 trong PR109 đã ghi nhận cùng bẫy | Có |
| Cách dùng nhãn windows | Cần synchronize/reopened hoặc thêm types:labeled | events+matrix: workflow có pull_request mặc định; evaluator đọc nhãn khi workflow được kích hoạt | Có |
| EOL step trên lượt master | PR head contains required EOL base bị skipped | events: if đúng github.event_name==pull_request; readback push thực tế EOL=skipped | Có |
| Hai P2 lịch sử PR109 | 05170b4: điều kiện Windows; 3736fc0: labeled không kích hoạt | events: git show cả hai sửa và merge 9796f67 (PR109); không có raw comment reviewer trong bundle | Khớp sửa; comment gốc KHÔNG ĐO ĐƯỢC |
| Commit 3a3a3ca | Merge PR848 ngày 20-10-2026 | history: git show = 3a3a3caca5de4934ff53851feb6994c2c7b84ad5; hai parent; Merge pull request #848; 2026-10-20 | Có |
| Commit 3f6c694 trích đúng jobs | jobs: '23/23 success (gom windows)' | history: git show blob tại 3f6c694 và head đều có nguyên văn trích dẫn | Có |
| Packet548: tên và bỏ vế master | CI-MA-TRAN-WINDOWS-CHAY-MOI-LAN-LAND | history: d1258fe bỏ điều kiện master ở các matrix, thêm chuan-bi; 6d46e6f sửa output thành chuỗi. Cả hai là ancestor | Có |
| Codex connector P1 PR859 / r4323607674 | Bắt lỗi khai gom windows | history: có commit sửa 4ae43f0 ghi cùng nguồn, nhưng git grep tại SHA không có raw comment độc lập | KHÔNG ĐO ĐƯỢC trực tiếp comment/actor/severity |
| Sửa ở PR865 | Bản sửa gom windows | history: object 4ae43f0 tồn tại và đúng phép sửa, chưa là ancestor của head; không có PR readback tại SHA | Khớp bản sửa; số PR KHÔNG ĐO ĐƯỢC trực tiếp |
| Nội bộ CLAUDE.md | Đoạn mới không giữ doctrine mọi push master đều có Windows | consistency: quét toàn tệp mọi windows/ubuntu/ci.yml/dispatch; câu cũ dòng159 là trích lịch sử, launcher dòng803–811 đúng scope launcher | Có |
| So với protocol | Phân biệt đo CI với yêu cầu gate hai nền khi land/phát hành | consistency: §10.2.2–10.2.4 yêu cầu identity/evidence; L1043 parity Windows–Linux là nghĩa vụ, không khai trigger push master | Có |
| Đợt 14-08: khi ấy còn vế master | Ma trận cũ chọn Windows khi master | historical: ci.yml tại 9796f67 có github.ref==refs/heads/master; tại SHA review không còn | Có |
| Đợt 14-08: không dùng nhãn/dispatch, sáu lần đo Windows đầu tiên | Sáu lần merge trong đợt | historical: trích nguồn PR109 và liệt kê commit/path ngày14-08; không có đủ raw run/nhãn để chứng minh số sáu và lần đầu | KHÔNG ĐO ĐƯỢC lịch sử execution; không coi là đã xác minh |
| Nay cùng tình huống không đo Windows qua ci.yml PR/push | Không nhãn, không dispatch thì chỉ Ubuntu | matrix+historical: đúng trong phạm vi ci.yml đã giới hạn ở câu hệ quả; launcher vẫn phụ thuộc path như dòng169–172 | Có |
| Trích doctrine cũ | Bản cũ viết PR Ubuntu, master Ubuntu+Windows | scope: git show 9e9a74b:CLAUDE.md L158–166 xác nhận nguyên ý và điều kiện | Có |
| P2 cũ: cả hai vị trí | Thu hẹp L169 và L173–174 | scope: git diff b38fce8..SHA đúng hai chỗ; assertions giữ dispatch/label; matrix xác nhận phản ví dụ cũ | Có |
| Doctrine cũ gây biên bản khai sai | Tác giả kể quan hệ nguyên nhân | scope+history: chứng minh văn bản và lời khai sai cùng tồn tại; không có transcript ý định executor | Suy luận tác giả; quan hệ nhân quả KHÔNG ĐO ĐƯỢC |
| Đọc nhãn thay suy từ tên event | Nhãn từng job cho biết nền của lượt đó | readback+matrix: 23 nhãn thật; cùng ref master nhưng push/dispatch chọn OS khác; chỉ là nhận định về nhãn, không chứng minh mọi gate pass | Có |
| Muốn Windows gate: dispatch trên ref | Đường chắc chắn chọn Windows theo cấu hình | matrix+events: trigger dispatch tồn tại, không lọc ref trong output os; chưa chạy GitHub Actions thật | Có |
| Cùng ma trận OS không có nghĩa gate PR/master giống nhau | Tiêu đề chỉ mô tả outputs.os | gate_scope: LAND release-verify vẫn if ref==master, WORKER if ref!=master; title mới chỉ khai chính sách OS chung | Có |
| Protocol T3 và ADR0049 | Không hủy nghĩa vụ gate Windows trước land/phát hành | gate_scope: T3 full hai nền, ADR0049 cổng deploy tại chỗ; không mâu thuẫn với trigger ci.yml hiện hành | Có |
| Checkout chỉ đọc | Không sửa cay-kho; không network/push | sandbox_end: snapshot toàn tệp + symlink + HEAD/tree/index/config + status tracked/untracked/ignored bằng nhau; 0 added/removed/changed | Có |
| Cùng ma trận OS không có nghĩa gate PR/master giống nhau | Tiêu đề chỉ mô tả outputs.os | gate_scope: LAND release-verify vẫn if ref==master, WORKER if ref!=master; title mới chỉ khai chính sách OS chung | Có |
| Protocol T3 và ADR0049 | Không hủy nghĩa vụ gate Windows trước land/phát hành | gate_scope: T3 full hai nền, ADR0049 cổng deploy tại chỗ; không mâu thuẫn với trigger ci.yml hiện hành | Có |

## BẢNG SĂN

Đang đọc chỉ thị và chuẩn bị phép đo độc lập tại đúng SHA được yêu cầu. Không sửa `cay-kho/`, không gọi mạng.

### HƯỚNG 1: Neo exact SHA, độ đầy đủ cây và phạm vi diff

Giả thuyết: Diff hoặc checkout có thể không phải head được giao.

Lệnh (cwd=`cay-kho/`):

```bash
PYTHONDONTWRITEBYTECODE=1 python3 ../review_probe.py preflight
```

Output thật:

```text
HEAD=06a50c5feea77c2654f31edd26efeed7eeee62f5
tree=0fa694daf17e10c37fc3e61690531ade4bd528bf
is_shallow=false
core.abbrev=7
status_with_ignored=''
snapshot_hashed_files=4843
provided_diff_matches_exact_SHA=True
numstat=21	9	CLAUDE.md
HEAD_message=docs(CLAUDE.md): (c) gioi han 'Windows tren master' vao push tu dong — va P2 cross-review codex
rc=0
```

Kết luận: **KHÔNG PHẢI LỖI**.

### HƯỚNG 2: Chạy nguyên evaluator trích bằng AST trên biểu thức thật

Giả thuyết: Có thể còn nhánh Windows bị bỏ sót; P2 cũ có thể chưa đóng.

Lệnh (cwd=`cay-kho/`):

```bash
PYTHONDONTWRITEBYTECODE=1 python3 ../review_probe.py matrix
```

Output thật:

```text
AST_EXTRACTED_FUNCTION_BEGIN
def _danh_gia_bieu_thuc_chuan_bi(expr_str: str, ctx: dict) -> list[str]:
    """Evaluator tối giản cho đúng hình biểu thức của chuan-bi.
    Hình chuẩn: ( <cond> ) && '["ubuntu-latest","windows-latest"]' || '["ubuntu-latest"]'
    Fail-close: in 'KHÔNG ĐO ĐƯỢC' và raise khi gặp hình khác (kể cả bọc fromJSON ngoài).
    """
    import json
    raw = expr_str.strip()
    if raw.startswith("${{") and raw.endswith("}}"):
        raw = raw[3:-2].strip()

    m = re.fullmatch(
        r"\(\s*(?P<cond>.*?)\)\s*&&\s*(?P<t>'\[.*?\]')\s*\|\|\s*(?P<f>'\[.*?\]')",
        raw,
        re.DOTALL,
    )
    if not m:
        msg = f"KHÔNG ĐO ĐƯỢC: biểu thức không khớp hình chuẩn tối giản của chuan-bi: {raw!r}"
        print(msg)
        raise ValueError(msg)

    cond_str = m.group("cond").strip()
    try:
        true_arr = json.loads(m.group("t").strip("'"))
        false_arr = json.loads(m.group("f").strip("'"))
    except Exception as ex:
        msg = f"KHÔNG ĐO ĐƯỢC: không parse được mảng JSON trong biểu thức: {ex}"
        print(msg)
        raise ValueError(msg)

    ve_list = [v.strip() for v in cond_str.split("||")]
    cond_true = False
    for ve in ve_list:
        m_eq = re.fullmatch(r"github\.event_name\s*==\s*'([^']+)'", ve)
        if m_eq:
            if ctx.get("event_name") == m_eq.group(1):
                cond_true = True
                break
            continue

        m_ref = re.fullmatch(r"github\.ref\s*==\s*'([^']+)'", ve)
        if m_ref:
            if ctx.get("ref") == m_ref.group(1):
                cond_true = True
                break
            continue

        m_contains = re.fullmatch(
            r"contains\s*\(\s*github\.event\.pull_request\.labels\.\*\.name\s*,\s*'([^']+)'\s*\)", ve
        )
        if m_contains:
            labels = ctx.get("labels") or []
            if m_contains.group(1) in labels:
                cond_true = True
                break
            continue

        msg = f"KHÔNG ĐO ĐƯỢC: vế điều kiện không nằm trong tập tối giản hỗ trợ: {ve!r}"
        print(msg)
        raise ValueError(msg)

    return true_arr if cond_true else false_arr
AST_EXTRACTED_FUNCTION_END
REAL_EXPRESSION='${{ (github.event_name == \'workflow_dispatch\' || contains(github.event.pull_request.labels.*.name, \'windows\')) && \'["ubuntu-latest","windows-latest"]\' || \'["ubuntu-latest"]\' }}'
expression_same_as_9e9a74b=True
push master: {"event_name": "push", "ref": "refs/heads/master", "labels": []} => ["ubuntu-latest"]
PR thường: {"event_name": "pull_request", "ref": "refs/pull/870/merge", "labels": ["docs"]} => ["ubuntu-latest"]
PR windows: {"event_name": "pull_request", "ref": "refs/pull/870/merge", "labels": ["windows"]} => ["ubuntu-latest", "windows-latest"]
dispatch master: {"event_name": "workflow_dispatch", "ref": "refs/heads/master", "labels": []} => ["ubuntu-latest", "windows-latest"]
dispatch feature: {"event_name": "workflow_dispatch", "ref": "refs/heads/review-probe", "labels": []} => ["ubuntu-latest", "windows-latest"]
PR nhãn khác: {"event_name": "pull_request", "ref": "refs/pull/870/merge", "labels": ["windows-other"]} => ["ubuntu-latest"]
ci_job=chuan-bi; runs-on=ubuntu-latest; matrix={}
ci_job=gate; runs-on=${{ matrix.os }}; matrix={"os": "${{ fromJson(needs.chuan-bi.outputs.os) }}"}
ci_job=gate-cong-cu; runs-on=${{ matrix.os }}; matrix={"os": "${{ fromJson(needs.chuan-bi.outputs.os) }}", "manh": [0, 1, 2, 3, 4, 5, 6, 7]}
ci_job=gate-cong-cu-gop; runs-on=${{ matrix.os }}; matrix={"os": "${{ fromJson(needs.chuan-bi.outputs.os) }}"}
ci_job=gate-ops; runs-on=${{ matrix.os }}; matrix={"os": "${{ fromJson(needs.chuan-bi.outputs.os) }}"}
ci_job=gate-nhanh-manh; runs-on=${{ matrix.os }}; matrix={"os": "${{ fromJson(needs.chuan-bi.outputs.os) }}", "manh": [0, 1, 2, 3, 4, 5, 6, 7]}
ci_job=gate-nhanh-gop; runs-on=${{ matrix.os }}; matrix={"os": "${{ fromJson(needs.chuan-bi.outputs.os) }}"}
ci_job=gate-registry; runs-on=${{ matrix.os }}; matrix={"os": "${{ fromJson(needs.chuan-bi.outputs.os) }}"}
ci_job=gate-packet-loop; runs-on=${{ matrix.os }}; matrix={"os": "${{ fromJson(needs.chuan-bi.outputs.os) }}"}
rc=0
```

Kết luận: **KHÔNG PHẢI LỖI**.

### HƯỚNG 3: Đếm readback độc lập bằng nhãn runner và định danh run

Giả thuyết: Số 23 hoặc nhận định không Windows có thể sai, lẫn tên job với nhãn runner.

Lệnh (cwd=`cay-kho/`):

```bash
PYTHONDONTWRITEBYTECODE=1 python3 ../review_probe.py readback
```

Output thật:

```text
total_count=23; len(jobs)=23
unique_job_ids=23
labels={('ubuntu-latest',): 23}
conclusions={'success': 23}
windows_labels=0
run_id=[39354156843]
head_sha=['3a3a3caca5de4934ff53851feb6994c2c7b84ad5']
head_branch=['master']
workflow_name=['gate']
run_attempt=[1]
run_metadata={"id": 39354156843, "path": ".github/workflows/ci.yml", "event": "push", "head_sha": "3a3a3caca5de4934ff53851feb6994c2c7b84ad5", "head_branch": "master", "created_at": "2026-10-20T01:34:09Z", "run_started_at": "2026-10-20T01:34:09Z", "conclusion": "success", "run_attempt": 1}
118404992707: chuan-bi: ['ubuntu-latest']: success
118405023227: gate-packet-loop (ubuntu-latest): ['ubuntu-latest']: success
118405023277: gate (ubuntu-latest): ['ubuntu-latest']: success
118405023325: gate-ops (ubuntu-latest): ['ubuntu-latest']: success
118405023336: gate-cong-cu (ubuntu-latest, 5): ['ubuntu-latest']: success
118405023360: gate-cong-cu (ubuntu-latest, 3): ['ubuntu-latest']: success
118405023366: gate-nhanh-manh (ubuntu-latest, 1): ['ubuntu-latest']: success
118405023370: gate-cong-cu (ubuntu-latest, 7): ['ubuntu-latest']: success
118405023391: gate-nhanh-manh (ubuntu-latest, 4): ['ubuntu-latest']: success
118405023397: gate-nhanh-manh (ubuntu-latest, 5): ['ubuntu-latest']: success
118405023408: gate-nhanh-manh (ubuntu-latest, 3): ['ubuntu-latest']: success
118405023422: gate-nhanh-manh (ubuntu-latest, 7): ['ubuntu-latest']: success
118405023423: gate-nhanh-manh (ubuntu-latest, 2): ['ubuntu-latest']: success
118405023432: gate-cong-cu (ubuntu-latest, 0): ['ubuntu-latest']: success
118405023442: gate-cong-cu (ubuntu-latest, 1): ['ubuntu-latest']: success
118405023453: gate-cong-cu (ubuntu-latest, 4): ['ubuntu-latest']: success
118405023470: gate-nhanh-manh (ubuntu-latest, 0): ['ubuntu-latest']: success
118405023490: gate-cong-cu (ubuntu-latest, 2): ['ubuntu-latest']: success
118405023510: gate-cong-cu (ubuntu-latest, 6): ['ubuntu-latest']: success
118405023533: gate-nhanh-manh (ubuntu-latest, 6): ['ubuntu-latest']: success
118405274418: gate-nhanh-gop (ubuntu-latest): ['ubuntu-latest']: success
118405368195: gate-registry (ubuntu-latest): ['ubuntu-latest']: success
118413934277: gate-cong-cu-gop (ubuntu-latest): ['ubuntu-latest']: success
rc=0
```

Kết luận: **KHÔNG PHẢI LỖI**.

### HƯỚNG 4: Cò, lọc path, nhãn, ma trận và phạm vi launcher

Giả thuyết: Launcher có thể chạy cho mọi push hoặc bị mô tả sai như full gate.

Lệnh (cwd=`cay-kho/`):

```bash
PYTHONDONTWRITEBYTECODE=1 python3 ../review_probe.py launcher
```

Output thật:

```text
launcher_events={"workflow_dispatch": {"inputs": {"runner_set": {"description": "Nền cần đo trong lượt gọi tay", "required": true, "default": "windows-only", "type": "choice", "options": ["windows-only", "windows-and-ubuntu"]}}}, "push": {"branches": ["master"], "paths": [".claude/dev/**", ".github/workflows/launcher-windows.yml"]}, "pull_request": {"types": ["opened", "synchronize", "reopened", "labeled"], "paths": [".claude/dev/**"]}}
launcher_if=github.event_name != 'pull_request' || contains(github.event.pull_request.labels.*.name, 'windows')
launcher_matrix=${{ fromJSON(github.event_name == 'workflow_dispatch' && inputs.runner_set == 'windows-only' && '["windows-latest"]' || '["windows-latest","ubuntu-latest"]') }}
launcher_runs_on=${{ matrix.os }}
step=Checkout LF; run_first=git config --global core.autocrlf false
step=Su that ve nen chay; run_first=python -c "import platform,sys;print('he:',platform.system(),'| python:',sys.version.split()[0])"
step=Install tool manifest dependencies; run_first=python -m pip install --quiet PyYAML==6.0.3 jsonschema==4.26.0
step=Install and verify test tools; run_first=set -euo pipefail
step=Verify tool manifest and shellcheck canary; run_first=python ops/cong_cu.py kiem-tra --json
step=doctor; run_first=python .claude/dev/launcher.py doctor
step=Bo phan chung (day du, giu nguyen danh sach bo qua); run_first=python .claude/dev/launcher_test.py
step=Tu dot bien; run_first=python .claude/dev/launcher_test.py --dot-bien
step=Cay lam viec phai SACH sau khi chay test; run_first=$ban = git status --porcelain
step=Probe: dut ong KHONG duoc nuot ma that; run_first=# Tren Linux da do: 0 khi du cong cu, 12 khi thieu, o CA BA kieu cat ong.
step=Probe: console cp1258 + duong dan co dau tieng Viet; run_first=chcp 1258
step=Probe: t62 chay rieng (ca CHUA TUNG chay o bat ky vong nao); run_first=python -c @"
step=Probe: taskkill /T tren tien trinh do CHINH minh sinh; run_first=# Vong 2 ket luan "Access denied" la han che sandbox codex chu khong phai
launcher push runner_set=None: ['windows-latest', 'ubuntu-latest']
launcher pull_request runner_set=None: ['windows-latest', 'ubuntu-latest']
launcher workflow_dispatch runner_set=windows-only: ['windows-latest']
launcher workflow_dispatch runner_set=windows-and-ubuntu: ['windows-latest', 'ubuntu-latest']
rc=0
```

Kết luận: **KHÔNG PHẢI LỖI**.

### HƯỚNG 5: Liệt kê toàn bộ workflow tại exact SHA

Giả thuyết: Có thể còn workflow tự chạy Windows ngoài launcher.

Lệnh (cwd=`cay-kho/`):

```bash
PYTHONDONTWRITEBYTECODE=1 python3 ../review_probe.py workflows
```

Output thật:

```text
workflow_count=7
.github/workflows/ci-dot-bien-du.yml: events=['schedule', 'workflow_dispatch']
  dot-bien-du: runs-on=ubuntu-latest; uses=None; matrix={}
  dot-bien-manh: runs-on=ubuntu-latest; uses=None; matrix={"manh": [0, 1, 2, 3, 4, 5, 6, 7]}
  dot-bien-gop: runs-on=ubuntu-latest; uses=None; matrix={}
.github/workflows/ci.yml: events=['push', 'pull_request', 'workflow_dispatch']
  chuan-bi: runs-on=ubuntu-latest; uses=None; matrix={}
  gate: runs-on=${{ matrix.os }}; uses=None; matrix={"os": "${{ fromJson(needs.chuan-bi.outputs.os) }}"}
  gate-cong-cu: runs-on=${{ matrix.os }}; uses=None; matrix={"os": "${{ fromJson(needs.chuan-bi.outputs.os) }}", "manh": [0, 1, 2, 3, 4, 5, 6, 7]}
  gate-cong-cu-gop: runs-on=${{ matrix.os }}; uses=None; matrix={"os": "${{ fromJson(needs.chuan-bi.outputs.os) }}"}
  gate-ops: runs-on=${{ matrix.os }}; uses=None; matrix={"os": "${{ fromJson(needs.chuan-bi.outputs.os) }}"}
  gate-nhanh-manh: runs-on=${{ matrix.os }}; uses=None; matrix={"os": "${{ fromJson(needs.chuan-bi.outputs.os) }}", "manh": [0, 1, 2, 3, 4, 5, 6, 7]}
  gate-nhanh-gop: runs-on=${{ matrix.os }}; uses=None; matrix={"os": "${{ fromJson(needs.chuan-bi.outputs.os) }}"}
  gate-registry: runs-on=${{ matrix.os }}; uses=None; matrix={"os": "${{ fromJson(needs.chuan-bi.outputs.os) }}"}
  gate-packet-loop: runs-on=${{ matrix.os }}; uses=None; matrix={"os": "${{ fromJson(needs.chuan-bi.outputs.os) }}"}
.github/workflows/launcher-windows.yml: events=['workflow_dispatch', 'push', 'pull_request']
  launcher: runs-on=${{ matrix.os }}; uses=None; matrix={"os": "${{ fromJSON(github.event_name == 'workflow_dispatch' && inputs.runner_set == 'windows-only' && '[\"windows-latest\"]' || '[\"windows-latest\",\"ubuntu-latest\"]') }}"}
.github/workflows/ops-don-ref.yml: events=['workflow_dispatch']
  don: runs-on=ubuntu-latest; uses=None; matrix={}
.github/workflows/ops-open-pr.yml: events=['push']
  mo: runs-on=ubuntu-latest; uses=None; matrix={}
.github/workflows/ops-publish-lease.yml: events=['push']
  dang: runs-on=ubuntu-latest; uses=None; matrix={}
.github/workflows/ops-thu-hoi-admission.yml: events=['pull_request_target']
  thu-hoi: runs-on=ubuntu-latest; uses=None; matrix={}
other_workflows_all_ubuntu=7
rc=0
```

Kết luận: **KHÔNG PHẢI LỖI**.

### HƯỚNG 6: Bẫy labeled, hai P2 PR109 và bước EOL skipped

Giả thuyết: Điều kiện trigger hoặc tên/if bước EOL có thể đã thay đổi.

Lệnh (cwd=`cay-kho/`):

```bash
PYTHONDONTWRITEBYTECODE=1 python3 ../review_probe.py events
```

Output thật:

```text
ci_events={"push": {"branches": ["master"]}, "pull_request": null, "workflow_dispatch": null}
pull_request_types_explicit=False
EOL_step={"name": "PR head contains required EOL base", "if": "${{ github.event_name == 'pull_request' }}", "shell": "bash", "env": {"PR_HEAD_SHA": "${{ github.event.pull_request.head.sha }}", "EOL_BASE_SHA": "1880346d2be3c0be9a93de7624ee108d99b6c88c"}, "run": "set -eu\ntest -n \"$PR_HEAD_SHA\"\ngit cat-file -e \"${PR_HEAD_SHA}^{commit}\"\ngit cat-file -e \"${EOL_BASE_SHA}^{commit}\"\ngit merge-base --is-ancestor \"$EOL_BASE_SHA\" \"$PR_HEAD_SHA\"\n"}
Traceback (most recent call last):
  File "/tmp/claude-0/-home-user-tra-luat/008916a5-97d8-5ef4-ac28-34381e972d65/scratchpad/cr2-pr870.nqvB/cay-kho/../review_probe.py", line 231, in main
    globals()[mode]()
    ~~~~~~~~~~~~~~~^^
  File "/tmp/claude-0/-home-user-tra-luat/008916a5-97d8-5ef4-ac28-34381e972d65/scratchpad/cr2-pr870.nqvB/cay-kho/../review_probe.py", line 175, in events
    assert step['if'] == "github.event_name == 'pull_request'"
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError
rc=1
```

Kết luận: **KHÔNG ĐO ĐƯỢC**.

### HƯỚNG 10: Hai cổng bắt buộc, tách rc với bằng chứng dương

Giả thuyết: Tài liệu có thể bị doctrine-scan hoặc doc-claims-check bác.

Lệnh (cwd=`cay-kho/`):

```bash
PYTHONDONTWRITEBYTECODE=1 python3 ../review_probe.py gates
```

Output thật:

```text
COMMAND=python3 .claude/dev/packet_loop.py doctrine-scan --root .
STDOUT:
doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine

STDERR:

RC=0
KẾT LUẬN doctrine-scan: passed; 0 chỗ chép doctrine
COMMAND=python3 scripts/tl.py doc-claims-check --json
STDOUT:
{
  "ok": true,
  "schema": "doc_claims_check.v1",
  "roots": [
    "CHANGELOG.md",
    "SKILL.md",
    "CLAUDE.md",
    "CONTEXT.md",
    "references",
    "docs"
  ],
  "files_scanned": 113,
  "claims_flagged": 381,
  "flags": [],
  "advisories": [
    {
      "layer": "L1",
      "file": "CHANGELOG.md",
      "line": 119,
      "claim": "ops/reviews/wp538/",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "CHANGELOG.md",
      "line": 119,
      "claim": "ops/reviews/wp540/",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "CHANGELOG.md",
      "line": 136,
      "claim": "ops/reviews/wp540/",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "CHANGELOG.md",
      "line": 202,
      "claim": "ops/thu-hoi/_ngoai-le-closure.retired.yaml",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L8",
      "file": "CHANGELOG.md",
      "line": 300,
      "claim": "tl selftest",
      "reason": "TL_COMMAND_UNKNOWN"
    },
    {
      "layer": "L2",
      "file": "CHANGELOG.md",
      "line": 542,
      "claim": "0449ddb0",
      "reason": "SHA_LIKE_NOT_A_COMMIT",
      "detail": {
        "len": 8
      }
    },
    {
      "layer": "L2",
      "file": "CHANGELOG.md",
      "line": 542,
      "claim": "457a6568",
      "reason": "SHA_LIKE_NOT_A_COMMIT",
      "detail": {
        "len": 8
      }
    },
    {
      "layer": "L2",
      "file": "CHANGELOG.md",
      "line": 542,
      "claim": "a146d00d",
      "reason": "SHA_LIKE_NOT_A_COMMIT",
      "detail": {
        "len": 8
      }
    },
    {
      "layer": "L2",
      "file": "CHANGELOG.md",
      "line": 543,
      "claim": "04792ddf",
      "reason": "SHA_LIKE_NOT_A_COMMIT",
      "detail": {
        "len": 8
      }
    },
    {
      "layer": "L2",
      "file": "CHANGELOG.md",
      "line": 543,
      "claim": "6c8b0629",
      "reason": "SHA_LIKE_NOT_A_COMMIT",
      "detail": {
        "len": 8
      }
    },
    {
      "layer": "L2",
      "file": "CHANGELOG.md",
      "line": 564,
      "claim": "6fe742e",
      "reason": "SHA_NOT_A_COMMIT_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "CHANGELOG.md",
      "line": 1267,
      "claim": "references/golden/fixtures/",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "CHANGELOG.md",
      "line": 1786,
      "claim": "ops/thu-hoi/",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "CHANGELOG.md",
      "line": 2573,
      "claim": "ops/reviews/phep-do/",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L12",
      "file": "CHANGELOG.md",
      "line": 3725,
      "claim": "r345_cac_phep_do_cuc_bo_van_dung",
      "reason": "TEST_ID_UNKNOWN"
    },
    {
      "layer": "L12",
      "file": "CHANGELOG.md",
      "line": 3746,
      "claim": "r345_dot_bien_ba_phep_do_cuc_bo_lam_ca_dich_DO",
      "reason": "TEST_ID_UNKNOWN"
    },
    {
      "layer": "L12",
      "file": "CHANGELOG.md",
      "line": 3766,
      "claim": "r345_cac_phep_do_cuc_bo_van_dung",
      "reason": "TEST_ID_UNKNOWN"
    },
    {
      "layer": "L1",
      "file": "CHANGELOG.md",
      "line": 4093,
      "claim": "ops/reviews/x.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L12",
      "file": "CHANGELOG.md",
      "line": 4783,
      "claim": "r345_than_hook_KHONG_duoc_co_duong_mang_nao",
      "reason": "TEST_ID_UNKNOWN"
    },
    {
      "layer": "L12",
      "file": "CHANGELOG.md",
      "line": 4848,
      "claim": "r345_than_hook_KHONG_duoc_co_duong_mang_nao",
      "reason": "TEST_ID_UNKNOWN"
    },
    {
      "layer": "L12",
      "file": "CHANGELOG.md",
      "line": 5149,
      "claim": "r338_ten_goi_pip_khac_ten_module_import",
      "reason": "TEST_ID_UNKNOWN"
    },
    {
      "layer": "L12",
      "file": "CHANGELOG.md",
      "line": 5152,
      "claim": "r338_dot_bien_bo_ban_do_lam_ca_dich_DO",
      "reason": "TEST_ID_UNKNOWN"
    },
    {
      "layer": "L8",
      "file": "CHANGELOG.md",
      "line": 5201,
      "claim": "tl selftest",
      "reason": "TL_COMMAND_UNKNOWN"
    },
    {
      "layer": "L8",
      "file": "CHANGELOG.md",
      "line": 5254,
      "claim": "tl selftest",
      "reason": "TL_COMMAND_UNKNOWN"
    },
    {
      "layer": "L8",
      "file": "CHANGELOG.md",
      "line": 5297,
      "claim": "tl selftest",
      "reason": "TL_COMMAND_UNKNOWN"
    },
    {
      "layer": "L1",
      "file": "CHANGELOG.md",
      "line": 6839,
      "claim": "references/KHONG_CO_FILE.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L12",
      "file": "CHANGELOG.md",
      "line": 7190,
      "claim": "r285_hang_cuoi_config_van_con_va_la_ngoai_le_duy_nhat",
      "reason": "TEST_ID_UNKNOWN"
    },
    {
      "layer": "L12",
      "file": "CHANGELOG.md",
      "line": 7296,
      "claim": "r292_bkl_migrate_v1_dua_doc_loi_quay_lai",
      "reason": "TEST_ID_UNKNOWN"
    },
    {
      "layer": "L12",
      "file": "CHANGELOG.md",
      "line": 7298,
      "claim": "r292_bkl_reg_bulk_verdict_khong_tin_ok_tran",
      "reason": "TEST_ID_UNKNOWN"
    },
    {
      "layer": "L12",
      "file": "CHANGELOG.md",
      "line": 7300,
      "claim": "r292_bkl_main_khong_con_bao_xong_oan",
      "reason": "TEST_ID_UNKNOWN"
    },
    {
      "layer": "L12",
      "file": "CHANGELOG.md",
      "line": 7346,
      "claim": "r291_ingest_commit_verdict_doi_du_marker",
      "reason": "TEST_ID_UNKNOWN"
    },
    {
      "layer": "L12",
      "file": "CHANGELOG.md",
      "line": 7350,
      "claim": "r291_ca_hai_call_site_deu_co_cong",
      "reason": "TEST_ID_UNKNOWN"
    },
    {
      "layer": "L12",
      "file": "CHANGELOG.md",
      "line": 7352,
      "claim": "r291_stage_write_chan_commit_mot_phan",
      "reason": "TEST_ID_UNKNOWN"
    },
    {
      "layer": "L12",
      "file": "CHANGELOG.md",
      "line": 7422,
      "claim": "r290_orch_dry_khong_goi_action_ghi",
      "reason": "TEST_ID_UNKNOWN"
    },
    {
      "layer": "L12",
      "file": "CHANGELOG.md",
      "line": 7425,
      "claim": "r290_orch_apply_van_goi_changes_pull",
      "reason": "TEST_ID_UNKNOWN"
    },
    {
      "layer": "L12",
      "file": "CHANGELOG.md",
      "line": 7427,
      "claim": "r290_orch_decide_not_probed_bao_thu",
      "reason": "TEST_ID_UNKNOWN"
    },
    {
      "layer": "L12",
      "file": "CHANGELOG.md",
      "line": 7474,
      "claim": "r289_pfr_duong_xanh_van_chay_du",
      "reason": "TEST_ID_UNKNOWN"
    },
    {
      "layer": "L12",
      "file": "CHANGELOG.md",
      "line": 7476,
      "claim": "r289_pfr_ma_tran_buoc_con_hong_khong_thao_registry",
      "reason": "TEST_ID_UNKNOWN"
    },
    {
      "layer": "L12",
      "file": "CHANGELOG.md",
      "line": 7479,
      "claim": "r289_pfr_reg_delete_readback_khong_tin_ok_tran",
      "reason": "TEST_ID_UNKNOWN"
    },
    {
      "layer": "L12",
      "file": "CHANGELOG.md",
      "line": 7482,
      "claim": "r289_pfr_khong_thao_tac_nao_khong_con_bao_xanh",
      "reason": "TEST_ID_UNKNOWN"
    },
    {
      "layer": "L12",
      "file": "CHANGELOG.md",
      "line": 7491,
      "claim": "r288_helper1_chi_gan_o_noi_da_khai",
      "reason": "TEST_ID_UNKNOWN"
    },
    {
      "layer": "L12",
      "file": "CHANGELOG.md",
      "line": 7491,
      "claim": "r288_helper1_chua_gan_vao_lenh_nao",
      "reason": "TEST_ID_UNKNOWN"
    },
    {
      "layer": "L12",
      "file": "CHANGELOG.md",
      "line": 7531,
      "claim": "r288_helper1_ok_duoc_tinh_va_rc_dan_xuat",
      "reason": "TEST_ID_UNKNOWN"
    },
    {
      "layer": "L12",
      "file": "CHANGELOG.md",
      "line": 7531,
      "claim": "r288_helper1_vi_ngu_ket_qua_duong_fail_closed",
      "reason": "TEST_ID_UNKNOWN"
    },
    {
      "layer": "L12",
      "file": "CHANGELOG.md",
      "line": 7532,
      "claim": "r288_helper1_chan_mutation_phia_sau_va_ke_da_ghi",
      "reason": "TEST_ID_UNKNOWN"
    },
    {
      "layer": "L12",
      "file": "CHANGELOG.md",
      "line": 7532,
      "claim": "r288_helper1_chua_gan_vao_lenh_nao",
      "reason": "TEST_ID_UNKNOWN"
    },
    {
      "layer": "L12",
      "file": "CHANGELOG.md",
      "line": 7574,
      "claim": "r287_golden_raw_drift_lam_do_gate",
      "reason": "TEST_ID_UNKNOWN"
    },
    {
      "layer": "L12",
      "file": "CHANGELOG.md",
      "line": 7577,
      "claim": "r287_write_cam_ghi_khi_raw_bat_dinh",
      "reason": "TEST_ID_UNKNOWN"
    },
    {
      "layer": "L12",
      "file": "CHANGELOG.md",
      "line": 7579,
      "claim": "r287_rc_khac_0_qua_lenh_that",
      "reason": "TEST_ID_UNKNOWN"
    },
    {
      "layer": "L12",
      "file": "CHANGELOG.md",
      "line": 7637,
      "claim": "r286_frozen_age_dong_bang_va_giu_none",
      "reason": "TEST_ID_UNKNOWN"
    },
    {
      "layer": "L12",
      "file": "CHANGELOG.md",
      "line": 7639,
      "claim": "r286_sweep_raw_bat_bien_khi_tuoi_cache_troi",
      "reason": "TEST_ID_UNKNOWN"
    },
    {
      "layer": "L12",
      "file": "CHANGELOG.md",
      "line": 7641,
      "claim": "r286_counts_va_ingest_missing_cung_mau",
      "reason": "TEST_ID_UNKNOWN"
    },
    {
      "layer": "L12",
      "file": "CHANGELOG.md",
      "line": 7686,
      "claim": "r285_hang_cuoi_config_van_con_va_la_ngoai_le_duy_nhat",
      "reason": "TEST_ID_UNKNOWN"
    },
    {
      "layer": "L12",
      "file": "CHANGELOG.md",
      "line": 7695,
      "claim": "r285_hang_cuoi_config_van_con_va_la_ngoai_le_duy_nhat",
      "reason": "TEST_ID_UNKNOWN"
    },
    {
      "layer": "L2",
      "file": "CHANGELOG.md",
      "line": 8536,
      "claim": "e53947f2",
      "reason": "SHA_LIKE_NOT_A_COMMIT",
      "detail": {
        "len": 8
      }
    },
    {
      "layer": "L2",
      "file": "CHANGELOG.md",
      "line": 8552,
      "claim": "8f0ab7cf",
      "reason": "SHA_LIKE_NOT_A_COMMIT",
      "detail": {
        "len": 8
      }
    },
    {
      "layer": "L2",
      "file": "CHANGELOG.md",
      "line": 8582,
      "claim": "e53947f2",
      "reason": "SHA_LIKE_NOT_A_COMMIT",
      "detail": {
        "len": 8
      }
    },
    {
      "layer": "L1",
      "file": "CHANGELOG.md",
      "line": 8890,
      "claim": "scripts/nlm_log.py",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "CHANGELOG.md",
      "line": 8890,
      "claim": "templates/_nguon-goc/",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "CHANGELOG.md",
      "line": 9542,
      "claim": "rasoat/X.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "CHANGELOG.md",
      "line": 9617,
      "claim": "scripts/wire_deploy_guard.py",
      "reason": "PATH_DELETED"
    },
    {
      "layer": "L1",
      "file": "CHANGELOG.md",
      "line": 9646,
      "claim": "scripts/wire_deploy_guard.py",
      "reason": "PATH_DELETED"
    },
    {
      "layer": "L2",
      "file": "CHANGELOG.md",
      "line": 10012,
      "claim": "743ed200",
      "reason": "SHA_LIKE_NOT_A_COMMIT",
      "detail": {
        "len": 8
      }
    },
    {
      "layer": "L12",
      "file": "CHANGELOG.md",
      "line": 10293,
      "claim": "r218_sach_khong_bao_gia",
      "reason": "TEST_ID_UNKNOWN"
    },
    {
      "layer": "L12",
      "file": "CHANGELOG.md",
      "line": 10294,
      "claim": "r219_l9_tu_tat_khi_quet_hep",
      "reason": "TEST_ID_UNKNOWN"
    },
    {
      "layer": "L1",
      "file": "CHANGELOG.md",
      "line": 10328,
      "claim": "references/MO_COI_R228.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L8",
      "file": "CHANGELOG.md",
      "line": 10805,
      "claim": "tl cho",
      "reason": "TL_COMMAND_UNKNOWN"
    },
    {
      "layer": "L8",
      "file": "CHANGELOG.md",
      "line": 10805,
      "claim": "tl rebase",
      "reason": "TL_COMMAND_UNKNOWN"
    },
    {
      "layer": "L8",
      "file": "CHANGELOG.md",
      "line": 10805,
      "claim": "tl selftest",
      "reason": "TL_COMMAND_UNKNOWN"
    },
    {
      "layer": "L8",
      "file": "CHANGELOG.md",
      "line": 10887,
      "claim": "tl khong-co-lenh-nay",
      "reason": "TL_COMMAND_UNKNOWN"
    },
    {
      "layer": "L1",
      "file": "CHANGELOG.md",
      "line": 10895,
      "claim": "references/X.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "CHANGELOG.md",
      "line": 10950,
      "claim": "scripts/manifest_build.py",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "CHANGELOG.md",
      "line": 10951,
      "claim": "references/Code.2.21.2h.gs",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "CHANGELOG.md",
      "line": 10952,
      "claim": "references/Code.2.21.2i.gs",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "CHANGELOG.md",
      "line": 10954,
      "claim": "references/BANG_PHAN_TANG_RUI_RO.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "CHANGELOG.md",
      "line": 10974,
      "claim": "references/golden/fixtures/",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "CHANGELOG.md",
      "line": 11017,
      "claim": "docs/_doc_patch_bak/",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "CHANGELOG.md",
      "line": 11513,
      "claim": "scripts/build_parts.py",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "CHANGELOG.md",
      "line": 11513,
      "claim": "scripts/tl_rebuild.sh",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L12",
      "file": "CHANGELOG.md",
      "line": 11572,
      "claim": "r192_f7_cookie_50p_chan_lo",
      "reason": "TEST_ID_UNKNOWN"
    },
    {
      "layer": "L12",
      "file": "CHANGELOG.md",
      "line": 11750,
      "claim": "r198_ingest_local_giu_duong_cu",
      "reason": "TEST_ID_UNKNOWN"
    },
    {
      "layer": "L12",
      "file": "CHANGELOG.md",
      "line": 12066,
      "claim": "r117_nlm_add_no_wait_skips_reg_link",
      "reason": "TEST_ID_UNKNOWN"
    },
    {
      "layer": "L12",
      "file": "CHANGELOG.md",
      "line": 12528,
      "claim": "r179_t",
      "reason": "TEST_ID_UNKNOWN"
    },
    {
      "layer": "L2",
      "file": "SKILL.md",
      "line": 91,
      "claim": "45739ff7",
      "reason": "SHA_LIKE_NOT_A_COMMIT",
      "detail": {
        "len": 8
      }
    },
    {
      "layer": "L2",
      "file": "SKILL.md",
      "line": 91,
      "claim": "743ed200",
      "reason": "SHA_LIKE_NOT_A_COMMIT",
      "detail": {
        "len": 8
      }
    },
    {
      "layer": "L1",
      "file": "docs/KE_HOACH_RASOAT_HOSO_ORCHESTRATION.md",
      "line": 17,
      "claim": "scripts/build_parts.py",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "docs/KE_HOACH_RASOAT_HOSO_ORCHESTRATION.md",
      "line": 17,
      "claim": "scripts/nlm_log.py",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "docs/KE_HOACH_RASOAT_HOSO_ORCHESTRATION.md",
      "line": 17,
      "claim": "templates/_nguon-goc/",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L2",
      "file": "docs/KE_HOACH_RASOAT_HOSO_ORCHESTRATION.md",
      "line": 39,
      "claim": "1835b46",
      "reason": "SHA_NOT_A_COMMIT_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L5",
      "file": "docs/KE_HOACH_RASOAT_HOSO_ORCHESTRATION.md",
      "line": 44,
      "claim": "v1.35.38",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L1",
      "file": "docs/KE_HOACH_RASOAT_HOSO_ORCHESTRATION.md",
      "line": 48,
      "claim": "scripts/nlm_log.py",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "docs/KE_HOACH_RASOAT_HOSO_ORCHESTRATION.md",
      "line": 63,
      "claim": "scripts/build_parts.py",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "docs/KE_HOACH_RASOAT_HOSO_ORCHESTRATION.md",
      "line": 63,
      "claim": "scripts/build_parts.py",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "docs/KE_HOACH_RASOAT_HOSO_ORCHESTRATION.md",
      "line": 63,
      "claim": "scripts/tl_rebuild.sh",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "docs/KE_HOACH_RASOAT_HOSO_ORCHESTRATION.md",
      "line": 63,
      "claim": "scripts/tl_rebuild.sh",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "docs/KE_HOACH_RASOAT_HOSO_ORCHESTRATION.md",
      "line": 64,
      "claim": "scripts/nlm_log.py",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "docs/KE_HOACH_RASOAT_HOSO_ORCHESTRATION.md",
      "line": 64,
      "claim": "templates/_nguon-goc/",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "docs/KE_HOACH_RASOAT_HOSO_ORCHESTRATION.md",
      "line": 66,
      "claim": "scripts/manifest_build.py",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L6",
      "file": "docs/KE_HOACH_RASOAT_HOSO_ORCHESTRATION.md",
      "line": 79,
      "claim": "r207",
      "reason": "R_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "docs/KE_HOACH_RASOAT_HOSO_ORCHESTRATION.md",
      "line": 163,
      "claim": "v1.35.38",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L1",
      "file": "docs/KE_HOACH_RASOAT_HOSO_ORCHESTRATION.md",
      "line": 177,
      "claim": "scripts/nlm_log.py",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L12",
      "file": "docs/KE_HOACH_RASOAT_HOSO_ORCHESTRATION.md",
      "line": 205,
      "claim": "r208_baseline_ratchet",
      "reason": "TEST_ID_UNKNOWN"
    },
    {
      "layer": "L12",
      "file": "docs/KE_HOACH_RASOAT_HOSO_ORCHESTRATION.md",
      "line": 205,
      "claim": "r208_cay_that_tang_A_B",
      "reason": "TEST_ID_UNKNOWN"
    },
    {
      "layer": "L12",
      "file": "docs/KE_HOACH_RASOAT_HOSO_ORCHESTRATION.md",
      "line": 205,
      "claim": "r208_pointer_findings_pure",
      "reason": "TEST_ID_UNKNOWN"
    },
    {
      "layer": "L1",
      "file": "docs/KE_HOACH_RASOAT_HOSO_ORCHESTRATION.md",
      "line": 206,
      "claim": "scripts/build_parts.py",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "docs/KE_HOACH_RASOAT_HOSO_ORCHESTRATION.md",
      "line": 206,
      "claim": "scripts/tl_rebuild.sh",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L12",
      "file": "docs/KE_HOACH_RASOAT_HOSO_ORCHESTRATION.md",
      "line": 206,
      "claim": "r208_skill_md_khong_tro_file_ma",
      "reason": "TEST_ID_UNKNOWN"
    },
    {
      "layer": "L6",
      "file": "docs/WORKFLOW_RASOAT_TU_DONG.md",
      "line": 201,
      "claim": "r207",
      "reason": "R_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L2",
      "file": "docs/adr/0010-tu-vung-nlm-status-dong-va-tach-claim-due.md",
      "line": 9,
      "claim": "59e8d0de",
      "reason": "SHA_LIKE_NOT_A_COMMIT",
      "detail": {
        "len": 8
      }
    },
    {
      "layer": "L5",
      "file": "docs/research/2026-08-04-lua-chon-orchestrator-da-model-codex-claude.md",
      "line": 265,
      "claim": "v1.0.6",
      "reason": "VERSION_BELOW_CHANGELOG_FLOOR"
    },
    {
      "layer": "L5",
      "file": "docs/research/2026-08-04-lua-chon-orchestrator-da-model-codex-claude.md",
      "line": 268,
      "claim": "v1.9.0",
      "reason": "VERSION_BELOW_CHANGELOG_FLOOR"
    },
    {
      "layer": "L5",
      "file": "references/API_CONTRACT.md",
      "line": 155,
      "claim": "v1.14.0",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L2",
      "file": "references/COMMANDS.md",
      "line": 32,
      "claim": "dbe706a0",
      "reason": "SHA_LIKE_NOT_A_COMMIT",
      "detail": {
        "len": 8
      }
    },
    {
      "layer": "L2",
      "file": "references/DELTA_v1.19.md",
      "line": 99,
      "claim": "fec6c125",
      "reason": "SHA_LIKE_NOT_A_COMMIT",
      "detail": {
        "len": 8
      }
    },
    {
      "layer": "L5",
      "file": "references/DEPENDENCIES.md",
      "line": 58,
      "claim": "v1.17.24",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DEPENDENCIES.md",
      "line": 90,
      "claim": "v1.17.14",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DEPENDENCIES.md",
      "line": 97,
      "claim": "v1.17.13",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DEPENDENCIES.md",
      "line": 110,
      "claim": "v1.17.11",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DEPENDENCIES.md",
      "line": 131,
      "claim": "v1.17.20",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DEPENDENCIES.md",
      "line": 134,
      "claim": "v1.17.20",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DEPENDENCIES.md",
      "line": 136,
      "claim": "v1.17.21",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 13,
      "claim": "v1.15.6",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 26,
      "claim": "scripts/boot.py",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 55,
      "claim": "v1.15.5",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 56,
      "claim": "references/NLM_QA_POLICY.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 62,
      "claim": "scripts/nlm_log.py",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 76,
      "claim": "v1.15.4",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 85,
      "claim": "scripts/nlm_log.py",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 89,
      "claim": "v1.15.3",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 95,
      "claim": "references/BANG_PHAN_TANG_RUI_RO.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 102,
      "claim": "v1.15.2",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 115,
      "claim": "v1.15.1",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 116,
      "claim": "references/PATCH_reg_delete.gs.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 116,
      "claim": "scripts/reg_delete.py",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 120,
      "claim": "v1.15.0",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 123,
      "claim": "v1.12.0",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 124,
      "claim": "v1.13.4",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 127,
      "claim": "scripts/manifest_build.py",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 148,
      "claim": "v1.12.0",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 156,
      "claim": "v1.12.0",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 160,
      "claim": "v1.14.0",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 181,
      "claim": "references/LOCATE_SHARED_DRIVE.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 186,
      "claim": "v1.13.4",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 205,
      "claim": "scripts/backfill_keywords.py",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 214,
      "claim": "v1.10.0",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 245,
      "claim": "v1.13.3",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 257,
      "claim": "v1.13.2",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 267,
      "claim": "v1.13.1",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 279,
      "claim": "v1.13.0",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 295,
      "claim": "v1.12.9",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 397,
      "claim": "scripts/preingest_gate.py",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 416,
      "claim": "references/PATCH_v2.18.0.gs.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 421,
      "claim": "scripts/preingest_gate.py",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 425,
      "claim": "v1.12.3",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 456,
      "claim": "v1.12.2",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 467,
      "claim": "scripts/dedup_gate2.py",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 468,
      "claim": "v1.11.0",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 471,
      "claim": "scripts/split_gdoc_plain.py",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 474,
      "claim": "scripts/wizard.py",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 492,
      "claim": "v1.12.0",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 509,
      "claim": "v1.15.0",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 521,
      "claim": "v1.15.0",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 560,
      "claim": "v1.11.0",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 567,
      "claim": "scripts/nlm_dedup.py",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 588,
      "claim": "references/PATCH_nlm_dedup_v1.11.0.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 590,
      "claim": "references/tra_luat_v2_13_6_FULL.gs",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 603,
      "claim": "v1.10.6",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 606,
      "claim": "v1.10.3",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 606,
      "claim": "v1.10.4",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 634,
      "claim": "v1.10.5",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 652,
      "claim": "v1.10.3",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 669,
      "claim": "references/CONVERT_SHEETS_v2_13_5.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 671,
      "claim": "v1.10.3",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 691,
      "claim": "v1.10.1",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 696,
      "claim": "v1.10.4",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 725,
      "claim": "scripts/vbhn_audit.py",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 763,
      "claim": "scripts/push_gates.py",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 773,
      "claim": "references/tra_luat_v2_13_4_FULL.gs",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 781,
      "claim": "v1.10.1",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 791,
      "claim": "scripts/napext.py",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 820,
      "claim": "v1.10.0",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 822,
      "claim": "references/OPERATING_CHANGES_v1.10.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 823,
      "claim": "references/tra_luat_v2_13_3_FULL.gs",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 834,
      "claim": "scripts/migrate_45chude.py",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 847,
      "claim": "v1.9.13",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 847,
      "claim": "v1.9.14",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 903,
      "claim": "v1.9.13",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 906,
      "claim": "v1.9.13",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 913,
      "claim": "references/tra_luat_v2_12_1_FULL.gs",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 919,
      "claim": "v1.9.13",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 920,
      "claim": "references/tra_luat_v2_12_FULL.gs",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 932,
      "claim": "v1.9.12",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 941,
      "claim": "references/APPSSCRIPT_V2_12_REGISTRY.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 943,
      "claim": "v1.9.12",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 952,
      "claim": "scripts/traluat_checkpoint.py",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 957,
      "claim": "scripts/traluat_integrity.py",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 959,
      "claim": "references/tra_luat_fetch_to_drive_v2.8.0.gs",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 959,
      "claim": "v1.9.11",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 966,
      "claim": "v1.9.11",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 967,
      "claim": "references/APPSSCRIPT_V2_8_IMPORT.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 968,
      "claim": "scripts/nlm_push.py",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 989,
      "claim": "v1.9.10",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 990,
      "claim": "references/DRIVE_LINK_IMPORT.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 990,
      "claim": "scripts/import_drive_link.py",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1002,
      "claim": "references/NLM_QA_POLICY.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1002,
      "claim": "scripts/nlm_qa.py",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1021,
      "claim": "references/APPSSCRIPT_MANIFEST.example.json",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1021,
      "claim": "references/INGEST_PRIORITY.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1021,
      "claim": "scripts/tl_ingest_external.sh",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1021,
      "claim": "scripts/tl_lib.sh",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1024,
      "claim": "references/DRIVE_API_PRIORITY.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1044,
      "claim": "references/INGEST_PRIORITY.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1044,
      "claim": "scripts/find_sources.py",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1047,
      "claim": "references/INGEST_PRIORITY.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1047,
      "claim": "scripts/find_sources.py",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1053,
      "claim": "references/INGEST_PRIORITY.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1059,
      "claim": "references/INGEST_PRIORITY.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1114,
      "claim": "scripts/upload_folder.sh",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1127,
      "claim": "references/origin_route_appsscript.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L4",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1149,
      "claim": "TODO",
      "reason": "DRAFT_MARKER"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1150,
      "claim": "references/origin_route_appsscript.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1178,
      "claim": "references/origin_route_appsscript.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1210,
      "claim": "v1.9.11",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1212,
      "claim": "v1.9.8",
      "reason": "VERSION_BELOW_CHANGELOG_FLOOR"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1230,
      "claim": "v1.9.8",
      "reason": "VERSION_BELOW_CHANGELOG_FLOOR"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1232,
      "claim": "v1.9.8",
      "reason": "VERSION_BELOW_CHANGELOG_FLOOR"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1247,
      "claim": "v1.9.8",
      "reason": "VERSION_BELOW_CHANGELOG_FLOOR"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1249,
      "claim": "v1.9.8",
      "reason": "VERSION_BELOW_CHANGELOG_FLOOR"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1250,
      "claim": "scripts/context_budget.py",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1263,
      "claim": "v1.9.8",
      "reason": "VERSION_BELOW_CHANGELOG_FLOOR"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1265,
      "claim": "v1.9.8",
      "reason": "VERSION_BELOW_CHANGELOG_FLOOR"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1267,
      "claim": "v1.9.8",
      "reason": "VERSION_BELOW_CHANGELOG_FLOOR"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1269,
      "claim": "v1.9.8",
      "reason": "VERSION_BELOW_CHANGELOG_FLOOR"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1271,
      "claim": "v1.9.8",
      "reason": "VERSION_BELOW_CHANGELOG_FLOOR"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1273,
      "claim": "v1.9.8",
      "reason": "VERSION_BELOW_CHANGELOG_FLOOR"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1282,
      "claim": "v1.9.8",
      "reason": "VERSION_BELOW_CHANGELOG_FLOOR"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1284,
      "claim": "v1.9.8",
      "reason": "VERSION_BELOW_CHANGELOG_FLOOR"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1286,
      "claim": "v1.9.8",
      "reason": "VERSION_BELOW_CHANGELOG_FLOOR"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1296,
      "claim": "v1.9.8",
      "reason": "VERSION_BELOW_CHANGELOG_FLOOR"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1298,
      "claim": "v1.9.8",
      "reason": "VERSION_BELOW_CHANGELOG_FLOOR"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1308,
      "claim": "v1.9.8",
      "reason": "VERSION_BELOW_CHANGELOG_FLOOR"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1310,
      "claim": "v1.9.8",
      "reason": "VERSION_BELOW_CHANGELOG_FLOOR"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1323,
      "claim": "v1.9.8",
      "reason": "VERSION_BELOW_CHANGELOG_FLOOR"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1325,
      "claim": "v1.9.8",
      "reason": "VERSION_BELOW_CHANGELOG_FLOOR"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1345,
      "claim": "v1.9.7",
      "reason": "VERSION_BELOW_CHANGELOG_FLOOR"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1347,
      "claim": "v1.9.7",
      "reason": "VERSION_BELOW_CHANGELOG_FLOOR"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1349,
      "claim": "v1.9.6",
      "reason": "VERSION_BELOW_CHANGELOG_FLOOR"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1349,
      "claim": "v1.9.7",
      "reason": "VERSION_BELOW_CHANGELOG_FLOOR"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1351,
      "claim": "v1.9.6",
      "reason": "VERSION_BELOW_CHANGELOG_FLOOR"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1357,
      "claim": "v1.9.6",
      "reason": "VERSION_BELOW_CHANGELOG_FLOOR"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1358,
      "claim": "v1.9.5",
      "reason": "VERSION_BELOW_CHANGELOG_FLOOR"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1367,
      "claim": "references/bang_bieu_mau.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1367,
      "claim": "scripts/extract_tables.py",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1367,
      "claim": "v1.9.4",
      "reason": "VERSION_BELOW_CHANGELOG_FLOOR"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1375,
      "claim": "v1.9.3",
      "reason": "VERSION_BELOW_CHANGELOG_FLOOR"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1377,
      "claim": "v1.9.2",
      "reason": "VERSION_BELOW_CHANGELOG_FLOOR"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1379,
      "claim": "v1.9.1",
      "reason": "VERSION_BELOW_CHANGELOG_FLOOR"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1444,
      "claim": "scripts/help.py",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1445,
      "claim": "references/huong_dan_nhanh.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1452,
      "claim": "references/danh_muc_luat.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1473,
      "claim": "v1.9.8",
      "reason": "VERSION_BELOW_CHANGELOG_FLOOR"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1512,
      "claim": "references/INGEST_PRIORITY.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1512,
      "claim": "scripts/tl_lib.sh",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1519,
      "claim": "references/DRIVE_API_PRIORITY.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1535,
      "claim": "v1.9.11",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1553,
      "claim": "v1.9.11",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1566,
      "claim": "v1.9.10",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1578,
      "claim": "references/DRIVE_LINK_IMPORT.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1580,
      "claim": "v1.9.10",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1583,
      "claim": "references/NLM_QA_POLICY.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1599,
      "claim": "scripts/split_structure.py",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1725,
      "claim": "scripts/doctor.py",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1746,
      "claim": "v1.10.5",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1749,
      "claim": "v1.10.5",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1752,
      "claim": "v1.10.5",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1755,
      "claim": "references/CONVERT_SHEETS_v2_13_5.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1756,
      "claim": "v1.13.3",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1758,
      "claim": "v1.13.0",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1759,
      "claim": "v1.12.0",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1759,
      "claim": "v1.15.0",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1762,
      "claim": "v1.15.0",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1765,
      "claim": "v1.12.0",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1765,
      "claim": "v1.15.0",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1766,
      "claim": "v1.15.0",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1770,
      "claim": "v1.15.1",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1772,
      "claim": "references/PATCH_reg_delete.gs.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1775,
      "claim": "v1.15.1",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1776,
      "claim": "v1.13.3",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1777,
      "claim": "v1.13.4",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1778,
      "claim": "v1.13.4",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1778,
      "claim": "v1.13.4",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1779,
      "claim": "v1.13.4",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1781,
      "claim": "v1.10.6",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1785,
      "claim": "v1.10.5",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1788,
      "claim": "v1.9.11",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1792,
      "claim": "references/APPSSCRIPT_V2_8_IMPORT.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1793,
      "claim": "v1.9.10",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1795,
      "claim": "references/DRIVE_LINK_IMPORT.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1796,
      "claim": "v1.9.10",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1799,
      "claim": "references/NLM_QA_POLICY.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1804,
      "claim": "references/DRIVE_API_PRIORITY.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1807,
      "claim": "references/INGEST_PRIORITY.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1810,
      "claim": "v1.9.1",
      "reason": "VERSION_BELOW_CHANGELOG_FLOOR"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1813,
      "claim": "references/danh_muc_luat.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1822,
      "claim": "scripts/context_budget.py",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1822,
      "claim": "v1.9.8",
      "reason": "VERSION_BELOW_CHANGELOG_FLOOR"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1834,
      "claim": "references/LOCATE_SHARED_DRIVE.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1834,
      "claim": "references/OPERATING_CHANGES_v1.10.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L5",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1834,
      "claim": "v1.14.0",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1842,
      "claim": "scripts/upload_folder.sh",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1846,
      "claim": "scripts/tl_lib.sh",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1851,
      "claim": "scripts/tl_ingest_external.sh",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1853,
      "claim": "references/INGEST_PRIORITY.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1854,
      "claim": "references/APPSSCRIPT_MANIFEST.example.json",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1857,
      "claim": "scripts/appscript_client.py",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/DOCTRINE_APPENDIX.md",
      "line": 1860,
      "claim": "references/origin_route_appsscript.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L5",
      "file": "references/KERNEL_APPENDIX.md",
      "line": 12,
      "claim": "v1.22.44",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/RUNBOOK.md",
      "line": 421,
      "claim": "v1.17.24",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/RUNBOOK.md",
      "line": 568,
      "claim": "v1.12.0",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/RUNBOOK.md",
      "line": 664,
      "claim": "v1.17.24",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/STALE_RELATION_GUARD.md",
      "line": 1,
      "claim": "v1.17.24",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/VBHN_MINISTRY_YEAR_GUARD.md",
      "line": 1,
      "claim": "v1.17.18",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/VBHN_OFFICIAL_FIRST.md",
      "line": 1,
      "claim": "v1.17.14",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L5",
      "file": "references/VBHN_QT5_VERIFICATION.md",
      "line": 1,
      "claim": "v1.17.14",
      "reason": "VERSION_NOT_IN_CHANGELOG"
    },
    {
      "layer": "L2",
      "file": "references/changelog_archive/CHANGELOG-1.33.54-den-1.34.99.md",
      "line": 323,
      "claim": "45739ff7",
      "reason": "SHA_LIKE_NOT_A_COMMIT",
      "detail": {
        "len": 8
      }
    },
    {
      "layer": "L2",
      "file": "references/changelog_archive/CHANGELOG-1.33.54-den-1.34.99.md",
      "line": 323,
      "claim": "743ed200",
      "reason": "SHA_LIKE_NOT_A_COMMIT",
      "detail": {
        "len": 8
      }
    },
    {
      "layer": "L2",
      "file": "references/changelog_archive/CHANGELOG-1.33.54-den-1.34.99.md",
      "line": 988,
      "claim": "4e2bc585",
      "reason": "SHA_LIKE_NOT_A_COMMIT",
      "detail": {
        "len": 8
      }
    },
    {
      "layer": "L2",
      "file": "references/changelog_archive/CHANGELOG-1.33.54-den-1.34.99.md",
      "line": 988,
      "claim": "a1322194",
      "reason": "SHA_LIKE_NOT_A_COMMIT",
      "detail": {
        "len": 8
      }
    },
    {
      "layer": "L2",
      "file": "references/changelog_archive/CHANGELOG-1.33.54-den-1.34.99.md",
      "line": 1018,
      "claim": "dbe706a0",
      "reason": "SHA_LIKE_NOT_A_COMMIT",
      "detail": {
        "len": 8
      }
    },
    {
      "layer": "L2",
      "file": "references/changelog_archive/CHANGELOG-1.33.54-den-1.34.99.md",
      "line": 1060,
      "claim": "45739ff7",
      "reason": "SHA_LIKE_NOT_A_COMMIT",
      "detail": {
        "len": 8
      }
    },
    {
      "layer": "L2",
      "file": "references/changelog_archive/CHANGELOG-1.33.54-den-1.34.99.md",
      "line": 1882,
      "claim": "59e8d0de",
      "reason": "SHA_LIKE_NOT_A_COMMIT",
      "detail": {
        "len": 8
      }
    },
    {
      "layer": "L1",
      "file": "references/changelog_archive/CHANGELOG-1.33.54-den-1.34.99.md",
      "line": 1957,
      "claim": "references/Code.2.21.2j.gs",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L12",
      "file": "references/changelog_archive/CHANGELOG-1.33.54-den-1.34.99.md",
      "line": 2030,
      "claim": "r76_engine_stays_in_tl",
      "reason": "TEST_ID_UNKNOWN"
    },
    {
      "layer": "L12",
      "file": "references/changelog_archive/CHANGELOG-1.33.54-den-1.34.99.md",
      "line": 2116,
      "claim": "r76_engine_stays_in_tl",
      "reason": "TEST_ID_UNKNOWN"
    },
    {
      "layer": "L1",
      "file": "references/changelog_archive/CHANGELOG-1.33.54-den-1.34.99.md",
      "line": 2294,
      "claim": "references/SKILL_KERNEL_DRAFT.md",
      "reason": "PATH_DELETED"
    },
    {
      "layer": "L2",
      "file": "references/changelog_archive/CHANGELOG-1.33.54-den-1.34.99.md",
      "line": 2498,
      "claim": "dcca0cd7",
      "reason": "SHA_LIKE_NOT_A_COMMIT",
      "detail": {
        "len": 8
      }
    },
    {
      "layer": "L2",
      "file": "references/changelog_archive/CHANGELOG-den-1.33.53.md",
      "line": 107,
      "claim": "59e8d0de",
      "reason": "SHA_LIKE_NOT_A_COMMIT",
      "detail": {
        "len": 8
      }
    },
    {
      "layer": "L1",
      "file": "references/changelog_archive/CHANGELOG-den-1.33.53.md",
      "line": 2116,
      "claim": "references/Code.2.21.2i.gs",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/changelog_archive/CHANGELOG-den-1.33.53.md",
      "line": 2131,
      "claim": "references/Code.2.21.2i.gs",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/changelog_archive/CHANGELOG-den-1.33.53.md",
      "line": 2135,
      "claim": "references/Code.2.21.2i.gs",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/changelog_archive/CHANGELOG-den-1.33.53.md",
      "line": 2962,
      "claim": "scripts/_parts/",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L8",
      "file": "references/changelog_archive/CHANGELOG-den-1.33.53.md",
      "line": 3028,
      "claim": "tl regen2",
      "reason": "TL_COMMAND_UNKNOWN"
    },
    {
      "layer": "L8",
      "file": "references/changelog_archive/CHANGELOG-den-1.33.53.md",
      "line": 3073,
      "claim": "tl regen2",
      "reason": "TL_COMMAND_UNKNOWN"
    },
    {
      "layer": "L2",
      "file": "references/changelog_archive/CHANGELOG-den-1.33.53.md",
      "line": 3306,
      "claim": "743ed200",
      "reason": "SHA_LIKE_NOT_A_COMMIT",
      "detail": {
        "len": 8
      }
    },
    {
      "layer": "L1",
      "file": "references/changelog_archive/CHANGELOG-den-1.33.53.md",
      "line": 3509,
      "claim": "scripts/tl_rebuild.sh",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/changelog_archive/CHANGELOG-den-1.33.53.md",
      "line": 3587,
      "claim": "scripts/build_parts.py",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/changelog_archive/CHANGELOG-den-1.33.53.md",
      "line": 3637,
      "claim": "scripts/_parts/",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/changelog_archive/CHANGELOG-den-1.33.53.md",
      "line": 4208,
      "claim": "references/REVIEW_BLLD_V1.19.18.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/changelog_archive/CHANGELOG-den-1.33.53.md",
      "line": 4251,
      "claim": "references/FETCHER_V1.19.14.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/changelog_archive/CHANGELOG-den-1.33.53.md",
      "line": 4262,
      "claim": "references/FETCHER_V1.19.14.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/changelog_archive/CHANGELOG-den-1.33.53.md",
      "line": 4272,
      "claim": "references/TVPL_AUTODOWNLOAD_V1.19.13.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/changelog_archive/CHANGELOG-den-1.33.53.md",
      "line": 4282,
      "claim": "references/NLM_CLI_ALLREADS_V1.19.12.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L2",
      "file": "references/changelog_archive/CHANGELOG-den-1.33.53.md",
      "line": 4300,
      "claim": "cc39895d",
      "reason": "SHA_LIKE_NOT_A_COMMIT",
      "detail": {
        "len": 8
      }
    },
    {
      "layer": "L1",
      "file": "references/changelog_archive/CHANGELOG-den-1.33.53.md",
      "line": 4306,
      "claim": "references/SHARDING_V1.19.10.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L2",
      "file": "references/changelog_archive/CHANGELOG-den-1.33.53.md",
      "line": 4312,
      "claim": "45739ff7",
      "reason": "SHA_LIKE_NOT_A_COMMIT",
      "detail": {
        "len": 8
      }
    },
    {
      "layer": "L2",
      "file": "references/changelog_archive/CHANGELOG-den-1.33.53.md",
      "line": 4327,
      "claim": "59e8d0de",
      "reason": "SHA_LIKE_NOT_A_COMMIT",
      "detail": {
        "len": 8
      }
    },
    {
      "layer": "L2",
      "file": "references/changelog_archive/CHANGELOG-den-1.33.53.md",
      "line": 4327,
      "claim": "fec6c125",
      "reason": "SHA_LIKE_NOT_A_COMMIT",
      "detail": {
        "len": 8
      }
    },
    {
      "layer": "L1",
      "file": "references/changelog_archive/CHANGELOG-den-1.33.53.md",
      "line": 4331,
      "claim": "references/NLM_CLI_FASTLANE_V1.19.8.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/changelog_archive/CHANGELOG-den-1.33.53.md",
      "line": 4344,
      "claim": "references/IDENTITY_XREF_V1.19.7.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/changelog_archive/CHANGELOG-den-1.33.53.md",
      "line": 4389,
      "claim": "references/MERGE_V1.19.5.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/changelog_archive/CHANGELOG-den-1.33.53.md",
      "line": 4427,
      "claim": "references/MERGE_V1.19.2.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/changelog_archive/CHANGELOG-den-1.33.53.md",
      "line": 4427,
      "claim": "references/PROFILE_SCOPE_V1.19.2.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/changelog_archive/CHANGELOG-den-1.33.53.md",
      "line": 4451,
      "claim": "references/Code.2.21.2f.gs",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/changelog_archive/CHANGELOG-den-1.33.53.md",
      "line": 4465,
      "claim": "references/DELTA_v1.18.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/changelog_archive/CHANGELOG-den-1.33.53.md",
      "line": 4465,
      "claim": "references/MERGE_V1.18.0.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/changelog_archive/CHANGELOG-den-1.33.53.md",
      "line": 4471,
      "claim": "references/Code.2.21.2e.gs",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/changelog_archive/CHANGELOG-den-1.33.53.md",
      "line": 4474,
      "claim": "references/DELTA_v1.18.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/changelog_archive/CHANGELOG-den-1.33.53.md",
      "line": 4474,
      "claim": "references/GS_2.21.2E_MULTI_CORPUS_SLOT.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/changelog_archive/CHANGELOG-den-1.33.53.md",
      "line": 4474,
      "claim": "references/MERGE_V1.18.0.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/changelog_archive/CHANGELOG-den-1.33.53.md",
      "line": 4483,
      "claim": "references/INSTRUCTION_SKILL_BINDING.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/changelog_archive/CHANGELOG-den-1.33.53.md",
      "line": 4483,
      "claim": "references/MERGE_V1.17.26.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/changelog_archive/CHANGELOG-den-1.33.53.md",
      "line": 4508,
      "claim": "references/RA_SOAT_LESSONS_2026_06.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/changelog_archive/CHANGELOG-den-1.33.53.md",
      "line": 4516,
      "claim": "references/Code.2.21.2d.gs",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/changelog_archive/CHANGELOG-den-1.33.53.md",
      "line": 4520,
      "claim": "references/Code.2.21.2d.gs",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/changelog_archive/CHANGELOG-den-1.33.53.md",
      "line": 4533,
      "claim": "references/Code.2.21.2c.gs",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/changelog_archive/CHANGELOG-den-1.33.53.md",
      "line": 4682,
      "claim": "references/COMPARISON_HOTFIX.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/changelog_archive/CHANGELOG-den-1.33.53.md",
      "line": 4694,
      "claim": "references/SKILL_ISSUES_FIRSTRUN.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/changelog_archive/CHANGELOG-den-1.33.53.md",
      "line": 4718,
      "claim": "references/Code.2.21.1.gs",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/changelog_archive/CHANGELOG-den-1.33.53.md",
      "line": 4734,
      "claim": "references/Code.2.21.1.gs",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/changelog_archive/CHANGELOG-den-1.33.53.md",
      "line": 4747,
      "claim": "references/Code.2.21.1.gs",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/changelog_archive/CHANGELOG-den-1.33.53.md",
      "line": 4747,
      "claim": "references/PATCH_REPORT.sample.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    }
  ],
  "by_layer": {
    "L1": 0,
    "L2": 0,
    "L3": 0,
    "L4": 0,
    "L5": 0,
    "L6": 0,
    "L7": 0,
    "L8": 0,
    "L9": 0,
    "L12": 0
  },
  "advisory_count": 381,
  "layers": [
    "L1",
    "L2",
    "L3",
    "L4",
    "L5",
    "L6",
    "L7",
    "L8",
    "L9",
    "L12"
  ],
  "layers_skipped": {},
  "basis": {
    "version": "1.36.68",
    "sha_lens": [
      7,
      40
    ],
    "changelog_files": 3,
    "changelog_versions": 490,
    "changelog_rs": 351,
    "changelog_headings": 1066,
    "floor_version": "1.9.9",
    "floor_r": 10,
    "max_r": 375,
    "commands_source": "references/golden/parser_surface.json",
    "commands_known": 198,
    "test_ids_known": 1379,
    "test_id_kinds": {
      "legacy": 1309,
      "packet": 70
    },
    "layers_bac": {
      "L10": "24/30 version GAS được dẫn không có tệp .gs — kho giữ 6 bản gần nhất là có chủ đích",
      "L11": "2/2 hit ở tài liệu sống đều viết ĐÚNG (số hiệu chính thức là dạng bare); bất biến NN-YYYY-VBHN-XXX áp cho khoá registry, đã có cổng vbhn-year-fix"
    },
    "note": "tập tra cứu = CHANGELOG.md + references/changelog_archive/*.md, quét toàn văn; dưới sàn ⇒ advisory (khuyết của sổ, không phải trích dẫn sai)"
  },
  "strict": false
}

STDERR:

RC=0
KẾT LUẬN doc-claims-check: passed; ok=true
rc=0
```

Kết luận: **KHÔNG PHẢI LỖI**.

### HƯỚNG 6: Bẫy labeled, hai P2 PR109 và bước EOL skipped

Giả thuyết: Điều kiện trigger hoặc tên/if bước EOL có thể đã thay đổi.

Lệnh (cwd=`cay-kho/`):

```bash
PYTHONDONTWRITEBYTECODE=1 python3 ../review_probe.py events
```

Output thật:

```text
ci_events={"push": {"branches": ["master"]}, "pull_request": null, "workflow_dispatch": null}
pull_request_types_explicit=False
EOL_step={"name": "PR head contains required EOL base", "if": "${{ github.event_name == 'pull_request' }}", "shell": "bash", "env": {"PR_HEAD_SHA": "${{ github.event.pull_request.head.sha }}", "EOL_BASE_SHA": "1880346d2be3c0be9a93de7624ee108d99b6c88c"}, "run": "set -eu\ntest -n \"$PR_HEAD_SHA\"\ngit cat-file -e \"${PR_HEAD_SHA}^{commit}\"\ngit cat-file -e \"${EOL_BASE_SHA}^{commit}\"\ngit merge-base --is-ancestor \"$EOL_BASE_SHA\" \"$PR_HEAD_SHA\"\n"}
EOL_in_push_readback=[["gate (ubuntu-latest)", "PR head contains required EOL base", "skipped"]]
historical_PR109_commits:
05170b4431b5d68632de2d9fc517b0eef9acb680 2026-08-14T12:48:03+00:00 docs: nói CÓ ĐIỀU KIỆN câu về đo Windows — ma trận có nhãn windows và workflow_dispatch
ancestor_of_reviewed=True
3736fc0a69f38019cd54f39273e44655f38d40f6 2026-08-14T12:54:19+00:00 docs: gắn nhãn windows KHÔNG đủ cho PR đang mở — phải có cò mới
ancestor_of_reviewed=True
9796f674c0b05fad04ff7b001ba1dcb25b7f0830 2026-08-14T20:01:28+07:00 Merge pull request #109 — ba lần đọc sai tín hiệu trong một phiên
ancestor_of_reviewed=True
diff --git a/CLAUDE.md b/CLAUDE.md
index 73a2dc2..3594a64 100644
--- a/CLAUDE.md
+++ b/CLAUDE.md
@@ -138,8 +138,15 @@ Phiên dev trên máy này ≠ phiên Cowork LIVE (bootstrap từ zip Package 
   trước. **Muốn biết đã review chưa thì tìm dòng `Reviewed commit:` cho ĐÚNG commit đang xét.**
   · **(c) Gate PR và gate master KHÔNG phải một thứ.** `ci.yml` cố ý chỉ chạy `ubuntu` cho PR thường,
   còn master chạy CẢ `ubuntu` LẪN `windows` (Windows tốn gấp đôi phút, để dành cho lượt gác cổng phát
-  hành). Nên **"PR xanh" không hàm ý "master xanh"**: mỗi lần merge là lần đo Windows ĐẦU TIÊN của mã
-  đó. Kèm theo: trên lượt master, bước `PR head contains required EOL base` LUÔN `skipped` vì nó có
+  hành). Nên **"PR xanh" không hàm ý "master xanh"**: với một PR THƯỜNG — không gắn nhãn `windows`,
+  không ai gọi tay — lần merge chính là lần đo Windows ĐẦU TIÊN của mã đó. Nói CÓ ĐIỀU KIỆN vì ma
+  trận cũng kèm `windows-latest` cho PR gắn nhãn `windows` và cho `workflow_dispatch`; bỏ điều kiện
+  ấy là đánh lừa người đang xem đúng một PR như vậy (cross-review bắt được, P2 trên PR #109 — và
+  trớ trêu là đoạn ngay trên đã trích đúng điều kiện đó rồi vẫn viết câu quên nó).
+  **Muốn có Windows TRƯỚC khi merge thì có sẵn hai đường: gắn nhãn `windows`, hoặc gọi tay
+  `workflow_dispatch`.** Đợt 14-08 không dùng đường nào trong hai, nên cả sáu lần merge của đợt đúng
+  là sáu lần đo Windows đầu tiên. Kèm theo: trên lượt master, bước `PR head contains required EOL
+  base` LUÔN `skipped` vì nó có
   `if: github.event_name == 'pull_request'` — nên tiêu chí "không bước nào `skipped`" chỉ đúng cho
   lượt PR; bê nguyên sang lượt master là tự báo động giả.
   Cả ba cùng họ với bài học "cổng không nói dối, nó VẮNG MẶT": **"vắng mặt vì sạch" và "vắng mặt vì

diff --git a/CLAUDE.md b/CLAUDE.md
index 3594a64..c885bf1 100644
--- a/CLAUDE.md
+++ b/CLAUDE.md
@@ -143,10 +143,15 @@ Phiên dev trên máy này ≠ phiên Cowork LIVE (bootstrap từ zip Package 
   trận cũng kèm `windows-latest` cho PR gắn nhãn `windows` và cho `workflow_dispatch`; bỏ điều kiện
   ấy là đánh lừa người đang xem đúng một PR như vậy (cross-review bắt được, P2 trên PR #109 — và
   trớ trêu là đoạn ngay trên đã trích đúng điều kiện đó rồi vẫn viết câu quên nó).
-  **Muốn có Windows TRƯỚC khi merge thì có sẵn hai đường: gắn nhãn `windows`, hoặc gọi tay
-  `workflow_dispatch`.** Đợt 14-08 không dùng đường nào trong hai, nên cả sáu lần merge của đợt đúng
-  là sáu lần đo Windows đầu tiên. Kèm theo: trên lượt master, bước `PR head contains required EOL
-  base` LUÔN `skipped` vì nó có
+  **Muốn có Windows TRƯỚC khi merge thì đường CHẮC CHẮN là gọi tay `workflow_dispatch` trên ref đó.**
+  Gắn nhãn `windows` KHÔNG đủ cho một PR ĐANG MỞ, và đây là bẫy thật (cross-review bắt, P2 thứ hai
+  trên PR #109): `ci.yml` khai `pull_request:` mà KHÔNG khai `types:`, nên mặc định chỉ bắn ở
+  `opened`/`synchronize`/`reopened` — **`labeled` không nằm trong đó**. Gắn nhãn không tự sinh lượt
+  chạy nào; ma trận chỉ đọc nhãn ở lượt bắn KẾ TIẾP. Người làm theo sẽ gắn nhãn, thấy vẫn đúng một
+  check Ubuntu, rồi merge mà tưởng đã có Windows. Muốn dùng nhãn thì phải kèm một cò mới sau khi gắn
+  (đẩy thêm commit, hoặc đóng rồi mở lại PR) — hoặc khai `types: [..., labeled]` cho workflow.
+  Đợt 14-08 không dùng đường nào, nên cả sáu lần merge của đợt đúng là sáu lần đo Windows đầu tiên.
+  Kèm theo: trên lượt master, bước `PR head contains required EOL base` LUÔN `skipped` vì nó có
   `if: github.event_name == 'pull_request'` — nên tiêu chí "không bước nào `skipped`" chỉ đúng cho
   lượt PR; bê nguyên sang lượt master là tự báo động giả.
   Cả ba cùng họ với bài học "cổng không nói dối, nó VẮNG MẶT": **"vắng mặt vì sạch" và "vắng mặt vì

rc=0
```

Kết luận: **KHÔNG PHẢI LỖI**.

### HƯỚNG 7: Kiểm SHA lịch sử, packet548, trích biên bản và nguồn PR859/865

Giả thuyết: Tên/SHA/trích dẫn có thể bịa, hoặc lời kể đã được sửa có thể vượt chứng cứ cục bộ.

Lệnh (cwd=`cay-kho/`):

```bash
PYTHONDONTWRITEBYTECODE=1 python3 ../review_probe.py history
```

Output thật:

```text
$ git show -s --format="%H %cI %P %s" 3a3a3ca
3a3a3caca5de4934ff53851feb6994c2c7b84ad5 2026-10-20T08:34:06+07:00 94220547cd155c73392e95726e8daf353888b3aa 23bc189f28ea60f04ca1634b6fe66d02babf12ed Merge pull request #848 from ducthangho/agent/wp744-g3-claude
ancestor_of_reviewed_SHA_rc=0
$ git show -s --format="%H %cI %P %s" 3f6c694
3f6c6943ebcebc7799db6adae76f8540c07f1d7f 2026-10-20T02:09:02+00:00 db8e0cdab925bfe65b91a67414522f71ff2e45a7 land(#744): ho so land PR #848 (merge 3a3a3ca) — landed true
ancestor_of_reviewed_SHA_rc=0
$ git show -s --format="%H %cI %P %s" 9e9a74b
9e9a74b2a396ef458d25c51a5563efafbb45ba0c 2026-10-22T13:38:57+07:00 637f78029f5a5fe56d35199dd0f75c50274f2c0f 521efebab226fe3a92b2ccce4a59c27dd638edff Merge pull request #864 from ducthangho/agent/wp858-g1-claude
ancestor_of_reviewed_SHA_rc=0
$ git show -s --format="%H %cI %P %s" b38fce8
b38fce83d0e97981012072ca2a2023ac726e5b2e 2026-10-22T07:14:02+00:00 9e9a74b2a396ef458d25c51a5563efafbb45ba0c docs(CLAUDE.md): sua bai hoc (c) — ma tran os cua ci.yml khong con ve master
ancestor_of_reviewed_SHA_rc=0
$ git show -s --format="%H %cI %P %s" 06a50c5
06a50c5feea77c2654f31edd26efeed7eeee62f5 2026-10-22T08:07:07+00:00 b38fce83d0e97981012072ca2a2023ac726e5b2e docs(CLAUDE.md): (c) gioi han 'Windows tren master' vao push tu dong — va P2 cross-review codex
ancestor_of_reviewed_SHA_rc=0
$ git show -s --format="%H %cI %P %s" d1258fe
d1258fef203d6b1f87fa729775cd2d8a1b0cc552 2026-09-17T03:12:08+07:00 f27a28ffa3cc1923cf894fa12cc2758277814ce3 feat(#548): ma tran CI Windows xuat tu chuan-bi va doi tieu chuan gate (ADR-0049)
ancestor_of_reviewed_SHA_rc=0
$ git show -s --format="%H %cI %P %s" 6d46e6f
6d46e6fc16cae3b5b490f5b6ee54ddb968b092fd 2026-09-17T23:30:21+07:00 93abdf2aeb9ca3f45aa959abe8c9c291fa904c53 fix(#548): xu ly P1 — go fromJSON o chuan-bi.outputs va them chot chan output sequence
ancestor_of_reviewed_SHA_rc=0
$ git show -s --format="%H %cI %P %s" 4ae43f0
4ae43f0c1e0cf121246da64336763daa41beea57 2026-10-21T09:07:34+00:00 637f78029f5a5fe56d35199dd0f75c50274f2c0f land(#744): dinh chinh gate post-merge 3a3a3ca — chi ubuntu, khong gom windows (connector P1 #859)
ancestor_of_reviewed_SHA_rc=1
$ git show 3f6c694:ops/land/pr848-wp744-land-evidence.yaml [lọc run 39354156843]
  - {name: 'ci.yml push master — DUNG merge SHA', run_id: 39354156843, sha: 3a3a3caca5de4934ff53851feb6994c2c7b84ad5, run_attempt: 1, conclusion: success, jobs: '23/23 success (gom windows)', luc: '2026-10-20T01:34:09Z -> 02:05:32Z', kiem_gate: 'measured — do-lai-nguon-20261020/kiem-gate-3a3a3ca.txt: packet_loop.py kiem-gate suite 106643757504, 23 ten, rc=0', nguon: [readback-run-39354156843.json, readback-jobs-39354156843.json, readback-check-runs-3a3a3ca-all.json]}
$ git show 06a50c5feea77c2654f31edd26efeed7eeee62f5:ops/land/pr848-wp744-land-evidence.yaml [lọc run 39354156843]
  - {name: 'ci.yml push master — DUNG merge SHA', run_id: 39354156843, sha: 3a3a3caca5de4934ff53851feb6994c2c7b84ad5, run_attempt: 1, conclusion: success, jobs: '23/23 success (gom windows)', luc: '2026-10-20T01:34:09Z -> 02:05:32Z', kiem_gate: 'measured — do-lai-nguon-20261020/kiem-gate-3a3a3ca.txt: packet_loop.py kiem-gate suite 106643757504, 23 ten, rc=0', nguon: [readback-run-39354156843.json, readback-jobs-39354156843.json, readback-check-runs-3a3a3ca-all.json]}
$ git show 4ae43f0:ops/land/pr848-wp744-land-evidence.yaml [lọc run 39354156843]
  - {name: 'ci.yml push master — DUNG merge SHA', run_id: 39354156843, sha: 3a3a3caca5de4934ff53851feb6994c2c7b84ad5, run_attempt: 1, conclusion: success, jobs: '23/23 success, ca 23 job chi nhan ubuntu-latest (measured — readback-jobs-39354156843.json); Windows KHONG chay tren lan push nay', luc: '2026-10-20T01:34:09Z -> 02:05:32Z', kiem_gate: 'measured — do-lai-nguon-20261020/kiem-gate-3a3a3ca.txt: packet_loop.py kiem-gate suite 106643757504, 23 ten, rc=0', nguon: [readback-run-39354156843.json, readback-jobs-39354156843.json, readback-check-runs-3a3a3ca-all.json]}
  - 'launcher-windows/Windows KHONG chay cho push 3a3a3ca: ci.yml chi chon windows-latest cho workflow_dispatch hoac PR gan nhan windows; Windows khong phai dieu kien cua lease (M-3 chi doi ci.yml). Ban dau ho so ghi sai "gom windows" — connector P1 #859 r4323607674, dinh chinh o PR sau.'
$ git show --format=short d1258fe -- .github/workflows/ci.yml
commit d1258fef203d6b1f87fa729775cd2d8a1b0cc552
Author: ducthangho <ducthangho@gmail.com>

    feat(#548): ma tran CI Windows xuat tu chuan-bi va doi tieu chuan gate (ADR-0049)

diff --git a/.github/workflows/ci.yml b/.github/workflows/ci.yml
index cb025a5..cbdad03 100644
--- a/.github/workflows/ci.yml
+++ b/.github/workflows/ci.yml
@@ -32,20 +32,25 @@ concurrency:
   cancel-in-progress: ${{ github.ref != 'refs/heads/master' }}
 
 jobs:
+  chuan-bi:
+    # packet #548 (CI-MA-TRAN-WINDOWS-CHAY-MOI-LAN-LAND): nguon duy nhat cho ma tran os.
+    # Chi ubuntu-latest, khong checkout ma nguon; bo github.ref == 'refs/heads/master'.
+    runs-on: ubuntu-latest
+    outputs:
+      os: ${{ fromJSON(
+            (github.event_name == 'workflow_dispatch'
+             || contains(github.event.pull_request.labels.*.name, 'windows'))
+            && '["ubuntu-latest","windows-latest"]'
+            || '["ubuntu-latest"]') }}
+    steps:
+      - run: 'true'
+
   gate:
+    needs: chuan-bi
     strategy:
       fail-fast: false
       matrix:
-        # Windows tốn GẤP ĐÔI phút. Chạy nó ở nơi thật sự cần: trước khi vào master,
-        # khi gọi tay, hoặc khi PR được gắn nhãn `windows` (dùng cho PR đụng đường
-        # phụ thuộc nền). PR thường vẫn được Linux soi mỗi lần đẩy.
-        # KHÔNG phải nới gate: master vẫn luôn qua CẢ HAI nền trước khi phát hành.
-        os: ${{ fromJSON(
-              (github.event_name == 'workflow_dispatch'
-               || github.ref == 'refs/heads/master'
-               || contains(github.event.pull_request.labels.*.name, 'windows'))
-              && '["ubuntu-latest","windows-latest"]'
-              || '["ubuntu-latest"]') }}
+        os: ${{ fromJson(needs.chuan-bi.outputs.os) }}
     runs-on: ${{ matrix.os }}
     # r391 — NÂNG 25 -> 45 THEO CHỈ ĐẠO CHỦ KHO, và lý do phải ghi lại vì con số cũ
     # KHÔNG sai lúc nó được đặt: gate đã chậm dần tới sát trần. Đo 29-08-2026:
@@ -595,16 +600,11 @@ jobs:
     # ma trận/`timeout-minutes`/tiền tố 9 bước với `gate`, KHÔNG thêm mặt điều kiện nào; phút TÍNH
     # TIỀN tăng vì trả tiền thiết lập ba lần. Consumer `loi_ruff_ci` đọc MỌI job, không chỉ `gate`.
     # Bước `test registry` (41,0 % tổng bước Windows) sống ở đây.
+    needs: chuan-bi
     strategy:
       fail-fast: false
       matrix:
-        # Vì sao Windows có điều kiện: xem chú thích cùng chỗ ở job `gate` (bản gốc).
-        os: ${{ fromJSON(
-              (github.event_name == 'workflow_dispatch'
-               || github.ref == 'refs/heads/master'
-               || contains(github.event.pull_request.labels.*.name, 'windows'))
-              && '["ubuntu-latest","windows-latest"]'
-              || '["ubuntu-latest"]') }}
+        os: ${{ fromJson(needs.chuan-bi.outputs.os) }}
     runs-on: ${{ matrix.os }}
     timeout-minutes: 60
     env:
@@ -659,16 +659,11 @@ jobs:
     # ma trận/`timeout-minutes`/tiền tố 9 bước với `gate`, KHÔNG thêm mặt điều kiện nào; phút TÍNH
     # TIỀN tăng vì trả tiền thiết lập ba lần. Consumer `loi_ruff_ci` đọc MỌI job, không chỉ `gate`.
     # Bước `packet-loop selftest` (22,5 % tổng bước Windows) sống ở đây.
+    needs: chuan-bi
     strategy:
       fail-fast: false
       matrix:
-        # Vì sao Windows có điều kiện: xem chú thích cùng chỗ ở job `gate` (bản gốc).
-        os: ${{ fromJSON(
-              (github.event_name == 'workflow_dispatch'
-               || github.ref == 'refs/heads/master'
-               || contains(github.event.pull_request.labels.*.name, 'windows'))
-              && '["ubuntu-latest","windows-latest"]'
-              || '["ubuntu-latest"]') }}
+        os: ${{ fromJson(needs.chuan-bi.outputs.os) }}
     runs-on: ${{ matrix.os }}
     timeout-minutes: 60
     env:

$ git show --format=short 6d46e6f -- .github/workflows/ci.yml
commit 6d46e6fc16cae3b5b490f5b6ee54ddb968b092fd
Author: ducthangho <ducthangho@gmail.com>

    fix(#548): xu ly P1 — go fromJSON o chuan-bi.outputs va them chot chan output sequence

diff --git a/.github/workflows/ci.yml b/.github/workflows/ci.yml
index cbdad03..2ca2f9d 100644
--- a/.github/workflows/ci.yml
+++ b/.github/workflows/ci.yml
@@ -37,11 +37,10 @@ jobs:
     # Chi ubuntu-latest, khong checkout ma nguon; bo github.ref == 'refs/heads/master'.
     runs-on: ubuntu-latest
     outputs:
-      os: ${{ fromJSON(
-            (github.event_name == 'workflow_dispatch'
-             || contains(github.event.pull_request.labels.*.name, 'windows'))
-            && '["ubuntu-latest","windows-latest"]'
-            || '["ubuntu-latest"]') }}
+      os: ${{ (github.event_name == 'workflow_dispatch'
+               || contains(github.event.pull_request.labels.*.name, 'windows'))
+              && '["ubuntu-latest","windows-latest"]'
+              || '["ubuntu-latest"]' }}
     steps:
       - run: 'true'
 

independent_comment_readback_at_reviewed_SHA:
git grep -n -I -e 4323607674 SHA -- :!CLAUDE.md rc=1
(không có bản đọc lại độc lập của comment này trong cây review)
correction_diff_4ae43f0:
commit 4ae43f0c1e0cf121246da64336763daa41beea57
Author: Claude <noreply@anthropic.com>

    land(#744): dinh chinh gate post-merge 3a3a3ca — chi ubuntu, khong gom windows (connector P1 #859)

diff --git a/ops/land/pr848-wp744-land-evidence.yaml b/ops/land/pr848-wp744-land-evidence.yaml
index ce05a96..e9ef051 100644
--- a/ops/land/pr848-wp744-land-evidence.yaml
+++ b/ops/land/pr848-wp744-land-evidence.yaml
@@ -36,7 +36,7 @@ pre_merge_checks:
   - {name: 'Codex connector', sha: 23bc189f28ea60f04ca1634b6fe66d02babf12ed, conclusion: 'completed, has_any_findings=false', nguon: readback-comments-848.json, ghi_chu: 'measured — readback-comments-848.json comment 6276780956 (neo 23bc189, chay luc roi draft).'}
   - {name: 'thread review', conclusion: '0 review, 0 review comment', nguon: [readback-reviews-848.json, readback-review-comments-848.json]}
 post_merge_checks:
-  - {name: 'ci.yml push master — DUNG merge SHA', run_id: 39354156843, sha: 3a3a3caca5de4934ff53851feb6994c2c7b84ad5, run_attempt: 1, conclusion: success, jobs: '23/23 success (gom windows)', luc: '2026-10-20T01:34:09Z -> 02:05:32Z', kiem_gate: 'measured — do-lai-nguon-20261020/kiem-gate-3a3a3ca.txt: packet_loop.py kiem-gate suite 106643757504, 23 ten, rc=0', nguon: [readback-run-39354156843.json, readback-jobs-39354156843.json, readback-check-runs-3a3a3ca-all.json]}
+  - {name: 'ci.yml push master — DUNG merge SHA', run_id: 39354156843, sha: 3a3a3caca5de4934ff53851feb6994c2c7b84ad5, run_attempt: 1, conclusion: success, jobs: '23/23 success, ca 23 job chi nhan ubuntu-latest (measured — readback-jobs-39354156843.json); Windows KHONG chay tren lan push nay', luc: '2026-10-20T01:34:09Z -> 02:05:32Z', kiem_gate: 'measured — do-lai-nguon-20261020/kiem-gate-3a3a3ca.txt: packet_loop.py kiem-gate suite 106643757504, 23 ten, rc=0', nguon: [readback-run-39354156843.json, readback-jobs-39354156843.json, readback-check-runs-3a3a3ca-all.json]}
 bookkeeping:
   - {item: 'dong PR #747 la da thay the (khong merge)', ket_qua: 'measured — readback-pr-747.json: state closed, merged false; comment 6281281678 neu ly do wp728/#755 (readback-comment-6281281678.json)'}
   - {item: 'rut han lease wp744-r3-g3-claude', ket_qua: 'xem lease.thu_hoi_cuoi'}
@@ -108,5 +108,6 @@ no_ngoai_pham_vi:
 
 khong_do_duoc:
   - 'Log day du cac job CI KHONG luu; chi readback run/job/check-run.'
+  - 'launcher-windows/Windows KHONG chay cho push 3a3a3ca: ci.yml chi chon windows-latest cho workflow_dispatch hoac PR gan nhan windows; Windows khong phai dieu kien cua lease (M-3 chi doi ci.yml). Ban dau ho so ghi sai "gom windows" — connector P1 #859 r4323607674, dinh chinh o PR sau.'
   - 'Comment-id GitHub trich trong ba spec: reviewer Codex chay offline nen KHONG_DO_DUOC; phien executor da kiem ton tai 6091609833 6091612697 6091615222 6133771506 truoc khi push (khong luu tho).'
   - 'stderr/transcript luot review Codex KHONG luu ngoai run.json; model thuc chay KHONG_DO_DUOC tu run.json.'

LIMIT: 4ae43f0 là object sửa có trước thời điểm head, không phải ancestor của head. Không dùng nó thay nội dung HEAD. Không gọi mạng để xác minh PR865 hoặc comment r4323607674.
rc=0
```

Kết luận: **KHÔNG ĐO ĐƯỢC**.

### HƯỚNG 8: Quét toàn CLAUDE.md và đối chiếu protocol

Giả thuyết: Doctrine cũ có thể còn ở chỗ khác, hoặc mô tả runtime mâu thuẫn yêu cầu gate.

Lệnh (cwd=`cay-kho/`):

```bash
PYTHONDONTWRITEBYTECODE=1 python3 ../review_probe.py consistency
```

Output thật:

```text
FILE=CLAUDE.md
36:    Windows: `.\scripts\deploy-package.ps1 -Pull -Push` · Linux/Cowork: `./scripts/deploy-package.sh --push`.
158:   · **(c) Ma trận `os` của `ci.yml` KHÔNG phân biệt PR với master — và câu ngược lại từng nằm ở đây.**
159:   Bản cũ của mục này viết: *"PR thường chỉ chạy `ubuntu`, còn master chạy CẢ `ubuntu` LẪN `windows`"*.
160:   Câu ấy **ĐÃ CHẾT** từ packet #548 (`CI-MA-TRAN-WINDOWS-CHAY-MOI-LAN-LAND`, bỏ vế
162:   `9e9a74b`: `os` = `["ubuntu-latest","windows-latest"]` CHỈ KHI `github.event_name == 'workflow_dispatch'`
163:   HOẶC PR mang nhãn `windows`; mọi trường hợp khác — **kể cả push lên master** — là `["ubuntu-latest"]`.
164:   Bằng chứng chạy được: run `ci.yml` **39354156843** (push merge commit `3a3a3ca` lên master,
165:   20-10-2026) có **23 job, cả 23 nhãn `ubuntu-latest`**, 0 job Windows — readback giữ ở
167:   bản land (commit `3f6c694`) khai `jobs: '23/23 success (gom windows)'`; Codex connector bắt thành P1 trên PR #859 (comment
169:   **Windows tự động khi push master hiện chỉ đến từ `launcher-windows.yml`**, và CÓ ĐIỀU KIỆN: chỉ bắn
170:   khi đổi `.claude/dev/**` hoặc chính tệp workflow ấy (`paths:`), ma trận `windows-latest` + `ubuntu-latest`;
171:   PR chỉ chạy khi mang nhãn `windows` (workflow này CÓ khai `types: [..., labeled]`). Nó chỉ đo lane
172:   launcher, KHÔNG phải gate. Các workflow còn lại (`ci-dot-bien-du` `ops-*`) đều `ubuntu-latest`.
173:   Hệ quả: với một PR THƯỜNG — không nhãn `windows`, không ai gọi tay — **các lượt PR và push hậu merge
174:   của `ci.yml` theo ma trận hiện tại chỉ đo Ubuntu**; merge không còn là "lần đo Windows đầu tiên" như bản cũ viết.
175:   Muốn biết master có Windows hay không thì **đọc nhãn từng job của lượt chạy**, đừng suy từ tên sự kiện.
176:   **Muốn có Windows cho gate thì đường CHẮC CHẮN là gọi tay `workflow_dispatch` trên ref đó.**
177:   Gắn nhãn `windows` KHÔNG đủ cho một PR ĐANG MỞ, và đây là bẫy thật (cross-review bắt, P2 thứ hai
178:   trên PR #109): `ci.yml` khai `pull_request:` mà KHÔNG khai `types:`, nên mặc định chỉ bắn ở
181:   check Ubuntu, rồi merge mà tưởng đã có Windows. Muốn dùng nhãn thì phải kèm một cò mới sau khi gắn
184:   Windows đầu tiên — nay cùng tình huống thì là **không lần nào**.)
211:   **160**. Ba ref đầu là `master` + hai nhánh `claude/**`; `ops/pkg-windows` **không** nằm trong đó, mà
212:   đúng nhánh ấy giữ **cả ba** lease `LEASE-DANG-WINDOWS` đang chặn write set `PLAT-X8`. Bộ quét vẫn in
344:   đường Windows từng mù hoàn toàn với secrets trong tệp ẩn. Nay quét cả tệp không mở rộng, tránh nhị
367: - **Workflow chỉ chạy khi có người bấm là workflow KHÔNG có ai canh.** `workflow_dispatch` không chạy
370:   workflow `workflow_dispatch` phải có phản chứng chạy được ở CI, và bộ ấy phải **trích thân bước TỪ
560: Đường dùng được: `.github/workflows/ops-don-ref.yml` (`workflow_dispatch`, kích hoạt được từ phiên web
652:   `actions_run_trigger`/`get_job_logs`. Đây là đường đã dùng để merge và gọi lượt Windows
687:   Đo 06-09-2026 trên Windows: `run ... -- codex exec ...` với tên trần ⇒ `CHAN [15]: probe nang luc
737: - **Không được giả định Windows có `python3`** (bản phổ biến chỉ có `python`, `py`).
744: ## Bài học lớp "chạy được ở đây" (12-08-2026, codex đo trên Windows thật)
803:   `windows-latest`, tức bộ test **chưa từng chạy** trên Windows kể từ lúc có chốt ấy.
804:   Không ai biết, vì job Windows chỉ chạy khi PR có nhãn `windows`. Năm lượt cross-review
810:   Gắn nhãn `windows` cho PR đụng `.claude/dev/**` — nó tốn ~40 phút và trả lại thứ mà
905: cùng `.claude/dev/launcher_test.py`, CI 17-08-2026 đo được Linux bỏ qua 1 ca còn Windows bỏ qua 13. Packet nào
907: Windows. Chọn nền theo thứ packet ĐO, đừng chọn theo nền nào đang rảnh.
938:    - Windows: `deploy-package.ps1` bước 4 (gọi `scripts/deploy-guard.ps1`), từ v1.35.80. Ghi đè cố ý:
948:    Và **lane PR KHÔNG bắt được**: `ci.yml` cho `release-verify strict (lane LAND)` điều kiện `if: github.ref == 'refs/heads/master'`, còn lane WORKER sinh manifest TẠM từ chính cây nên nó **hấp thụ** mọi thay đổi nội dung ⇒ PR xanh, master ĐỎ. Muốn biết trước khi merge thì chạy ĐÚNG lệnh của lane LAND tại chỗ: `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` (đòi `ok=true` và `expected == checked`).
FILE=docs/PROTOCOL_DA_PHIEN.md
18: - **Phạm vi:** Claude Code, Codex, Google Antigravity, Windows local, cloud worker và Android
306: 4. case-fold để bắt va chạm trên Windows;
410: `executor` và `environment` là hai trường độc lập. `cloud` là mặc định vì Windows host có thể tắt. `local` chỉ
411: dùng khi cần tài nguyên cục bộ, parity Windows hoặc khi người dùng chọn rõ. Dispatcher không tự đổi môi trường;
415: Windows trực tuyến. Controller Python chạy bằng Scheduled Task dưới tài khoản ít quyền, tạo worktree rồi gọi
757: refs đã cấp. Bootstrapper xác minh path/trust trên đúng OS, longpaths nếu đường dẫn Windows
856: (B) chỉ `git add --renormalize .`; (C) tái sinh manifest/golden/derived artifact và chạy parity Windows–Linux.
866: Loader/generator ghi UTF-8 LF tường minh, không phụ thuộc newline mặc định của Windows.
884: | T3 | integration freeze/`land prepare` | full selftest và release gates trên Windows + Linux cho frozen integration SHA |
936: Windows host xanh không chứng minh WSL/Linux/container xanh; từng runtime cần probe riêng.
937: Riêng admission hiện dùng bộ giải Git với PATH `/usr/bin:/bin`: native Windows chưa được
959: test merge hoặc test Windows. Thiếu một mốc bắt buộc thì ghi thiếu, không suy để lấp receipt.
977: Job `skipped` không được cấp runner là chưa thực thi, không là Windows execution dù tên job
978: có Windows. `owner_waived` là disposition riêng chỉ khi có waiver bền của owner: nguồn/actor,
1043: Windows–Linux. Land sinh bundled test module theo thứ tự tất định, kiểm cả chế độ dev có fragment lẫn topology
1056: `/land apply <mission_id> <head_sha>` và typed `workflow_dispatch` có hai input đó. Vì vậy người dùng có thể đóng
1057: mission từ GitHub trên Android khi Windows tắt, nhưng hệ thống vẫn dừng ở `awaiting_land` cho tới phê duyệt tường
1086: | Phép đo được cấp | Có mục tiêu/phản chứng, scope và allowance hữu hạn công bố trước; ghi `used / reserved / limit`, rồi gắn kết quả với run ID/attempt và exact SHA. `workflow_dispatch` hợp lệ có thể thuộc loại này. |
1153: `working_clock` và `timeout_clock=wall`. Trên Windows, chỉ được khai working-state time từ
1291: Android trong cùng một hệ thống; GitHub Actions giữ chuỗi cloud chạy khi Windows tắt. Vì vậy registry phiên và
1337:   và bundle, fragment bị loại đúng prefix còn bundled module là required file/tái sinh cùng byte Windows–Linux;
1342: - path collision Unicode/case/separator bị bắt trên Windows lẫn Linux;
1346: - Windows host tắt không làm mất packet local, bật lại tự tiếp tục đúng generation;
1348:   không cần Windows host; stale head/actor lạ bị từ chối có audit;
1349: - renormalize cho cùng blob EOL trên Windows/Linux, manifest và full gate xanh;
1376: - GitHub hỗ trợ chạy `workflow_dispatch` thủ công và merge PR sau required checks; đây là các client mobile/web
1386:   [GitHub Mobile workflow dispatch](https://github.blog/changelog/2024-07-30-run-workflows-set-as-workflow_dispatch-manually/).
1396: - `.github/workflows/ci.yml` chưa có `permissions:` tối thiểu và đang chạy strict verify với manifest committed,
1474:   `.claude/dev/launcher.py`, `.claude/dev/gate_lifecycle.py`, `ci.yml`, `ops-publish-lease.yml`) nhắc
1488: | `ADR-0018` | EOL canonical theo loại tệp | Accepted | có nhắc: `ci.yml`×19 |
1491: | `ADR-0021` | Local controller headless trên Windows | Accepted | chưa đo |
1501: | `ADR-0031` | Test fragment thay khóa toàn cục selftest | Accepted | có nhắc: `ci.yml`×7 · `gate_lifecycle.py`×2 |
1519: | `ADR-0049` | Cổng hai nền trước phát hành, không phải mỗi lần land | Accepted | có nhắc: `ci.yml` · `deploy-package.*` |
PROTOCOL_L944-981:
944: #### 10.2.2 Identity và provenance CI
945: 
946: Mỗi bằng chứng CI phải tách và dẫn nguồn cho bốn mốc:
947: 
948: | Mốc | Dữ liệu và nguồn kiểm |
949: |---|---|
950: | Run | repository, run ID, attempt, event, run head SHA từ API của đúng run |
951: | Checkout | SHA thực sự chạy, parents và tree từ checkout/log/artifact của đúng job/attempt |
952: | Workflow definition | repository/path, exact commit OID, blob OID và SHA-256 của bytes định nghĩa |
953: | Gate output | job/check-run/context, runner/OS/runtime, command/rc, marker dương và artifact ID/hash |
954: 
955: Không đồng nhất REST run head với checkout hay workflow-definition SHA. Với synthetic merge,
956: chứng minh parents trỏ đúng head/base và tree từ checkout/log/artifact tương ứng; chỉ đo
957: `refs/pull/.../merge` hiện tại không chứng minh run cũ đã test ref ấy. Tree bằng nhau không
958: đồng nhất commit, thời điểm, workflow, loại test hoặc runtime; không tự nâng test head thành
959: test merge hoặc test Windows. Thiếu một mốc bắt buộc thì ghi thiếu, không suy để lấp receipt.
960: 
961: Trong lane GitHub, có thể đọc `WorkflowRun.file.repositoryFileUrl`, xác minh URL chứa đúng
962: repository/path và exact OID, tải blob tại OID ấy rồi băm bytes. `file` là nullable: null,
963: GraphQL errors, 403, URL chỉ chứa ref trôi hoặc không lấy được blob là `not_measured` cho
964: provenance. Không lấy REST `head_sha` hay workflow ở HEAD hiện tại thay vào. Có thể dùng
965: nguồn provenance khác chỉ khi tự chứng minh cùng run/attempt và exact definition identity.
966: Xem [schema Actions của GitHub](https://docs.github.com/en/graphql/reference/actions).
967: 
968: #### 10.2.3 Evidence thiếu, skipped và tiêu chí riêng
969: 
970: Ghi `passed`, `failed`, `skipped`, `not_run` và `not_measured` riêng. API thiếu quyền chỉ
971: cho biết endpoint/field ấy chưa đo được; giữ HTTP status và lỗi thực. Có thể thu tiếp theo
972: chuỗi GraphQL aggregate → jobs/logs → commit statuses, nhưng mỗi nguồn chỉ chứng minh phần
973: nó chứa. Paginate đủ, chọn đúng SHA/run/attempt/context/producer; statuses không tự có
974: workflow/runner/command/output. Chỉ nhận khi tổng evidence đủ identity và nội dung dương,
975: không đổi 403 hay list rỗng thành pass.
976: 
977: Job `skipped` không được cấp runner là chưa thực thi, không là Windows execution dù tên job
978: có Windows. `owner_waived` là disposition riêng chỉ khi có waiver bền của owner: nguồn/actor,
979: exact SHA, context/OS, lý do, phạm vi/hạn và điều kiện thay thế. Giữ nguyên kết quả skipped;
980: waiver không viết lại nó thành passed, không tự gỡ branch protection. Không có waiver đúng
981: scope thì required evidence còn thiếu và tiếp tục chặn gate.
PROTOCOL_L988-995:
988: #### 10.2.4 Worker gate và hoàn tất
989: 
990: Worker gate kiểm generation/spec/write-set, EOL, security paths, offline tests và manifest tạm ngoài repo. Gate
991: dùng primitive hiện có theo nghĩa tương đương:
992: 
993: ```text
994: release-manifest --root <worktree> --out <temporary-path>
995: release-verify <temporary-path> --root <worktree> --strict
PROTOCOL_L1040-1045:
1040: cổng xanh"*, đổi đối tượng: **một phép thử đo đúng MỘT thứ, bị đọc thành đo CẢ GÓI.**
1041: 
1042: Land gate đóng băng mission, rebase/integrate lần cuối, gán version/changelog/manifest và chạy parity
1043: Windows–Linux. Land sinh bundled test module theo thứ tự tất định, kiểm cả chế độ dev có fragment lẫn topology
1044: bundle chỉ có module sinh. Bundle không chứa fragment và thiếu bundled module phải fail với lỗi đích danh;
1045: behavior test dựng root giả để chứng minh exclusion đi qua đường release thật, không chỉ kiểm membership của một
INTERPRETATION: protocol yêu cầu chứng cứ theo context/OS và parity Windows–Linux khi land; không khai mọi push master tự sinh full gate Windows. Chỉ chọn runner hoặc dispatch không tự chứng minh gate đã chạy/đã pass.
rc=0
```

Kết luận: **KHÔNG PHẢI LỖI**.

### HƯỚNG 9: Đối chứng đợt 14-08, sáu merge và Windows lần đầu

Giả thuyết: Câu lịch sử có thể đã bị biến thành lời khẳng định runtime hiện hành.

Lệnh (cwd=`cay-kho/`):

```bash
PYTHONDONTWRITEBYTECODE=1 python3 ../review_probe.py historical
```

Output thật:

```text
PR109_original_text:
36:    Windows: `.\scripts\deploy-package.ps1 -Pull -Push` · Linux/Cowork: `./scripts/deploy-package.sh --push`.
127: - **HỎI CHỖ TIỆN TAY thay vì hỏi CHỖ KẾT LUẬN ĐƯỢC GHI — ba lần trong MỘT phiên (14-08-2026).**
140:   còn master chạy CẢ `ubuntu` LẪN `windows` (Windows tốn gấp đôi phút, để dành cho lượt gác cổng phát
141:   hành). Nên **"PR xanh" không hàm ý "master xanh"**: với một PR THƯỜNG — không gắn nhãn `windows`,
142:   không ai gọi tay — lần merge chính là lần đo Windows ĐẦU TIÊN của mã đó. Nói CÓ ĐIỀU KIỆN vì ma
143:   trận cũng kèm `windows-latest` cho PR gắn nhãn `windows` và cho `workflow_dispatch`; bỏ điều kiện
146:   **Muốn có Windows TRƯỚC khi merge thì đường CHẮC CHẮN là gọi tay `workflow_dispatch` trên ref đó.**
147:   Gắn nhãn `windows` KHÔNG đủ cho một PR ĐANG MỞ, và đây là bẫy thật (cross-review bắt, P2 thứ hai
151:   check Ubuntu, rồi merge mà tưởng đã có Windows. Muốn dùng nhãn thì phải kèm một cò mới sau khi gắn
153:   Đợt 14-08 không dùng đường nào, nên cả sáu lần merge của đợt đúng là sáu lần đo Windows đầu tiên.
164:   đường Windows từng mù hoàn toàn với secrets trong tệp ẩn. Nay quét cả tệp không mở rộng, tránh nhị
179: - **Không được giả định Windows có `python3`** (bản phổ biến chỉ có `python`, `py`).
186: ## Bài học lớp "chạy được ở đây" (12-08-2026, codex đo trên Windows thật)
253:    - Windows: `deploy-package.ps1` bước 4 (gọi `scripts/deploy-guard.ps1`), từ v1.35.80. Ghi đè cố ý:
merge_commits_14Aug_on_first_parent_of_PR109:
4dd1d6f 2026-08-14T14:46:34+07:00 Merge pull request #98 — v1.36.68: đăng lease bằng git, lease neo prompt kiểm được, ops/ ra khỏi kiểm kê gói
changed_paths=['.github/workflows/ops-open-pr.yml', '.github/workflows/ops-publish-lease.yml', '.mcp.json', 'CHANGELOG.md', 'RELEASE_MANIFEST.json', 'SKILL.md', 'VERSION', 'ops/README.md', 'ops/lease_publish.py', 'ops/lease_publish_test.py', 'ops/leases/wp55-r2-review-3-codex-20260814.yaml', 'ops/prompts/wp55-r2-review-3-codex-20260814.md', 'scripts/tl.py', 'scripts/tl_core/release.py']
464124d 2026-08-14T15:11:54+07:00 Merge pull request #100 — lease #4 cho wp55 vào master, t23 quét mọi lease
changed_paths=['ops/lease_publish_test.py', 'ops/leases/wp55-r2-review-4-codex-20260814.yaml', 'ops/prompts/wp55-r2-review-4-codex-20260814.md']
8492380 2026-08-14T15:41:03+07:00 Merge pull request #101 — chốt chống lặp ra khỏi commit, vào lượt chạy
changed_paths=['.github/workflows/ops-publish-lease.yml', 'CLAUDE.md', 'ops/lease_publish_test.py']
438fc34 2026-08-14T16:26:11+07:00 Merge pull request #102 — khôi phục xác thực codex qua nhiều môi trường
changed_paths=['.claude/hooks/session-start.sh', 'docs/GOI_AGENT_DA_NEN.md']
e344e7c 2026-08-14T18:35:28+07:00 Merge pull request #104 — đảo danh sách CẤM thành danh sách CHO PHÉP ở cổng đăng lease
changed_paths=['ops/README.md', 'ops/lease_publish.py', 'ops/lease_publish_test.py']
05692fe 2026-08-14T18:41:12+07:00 Merge pull request #105 — lưu verdict cross-review wp55 lượt 4 vào kho, neo băm
changed_paths=['ops/reviews/wp55-r2-review-4-codex-verdict.md']
bbbaf8f 2026-08-14T18:43:31+07:00 Merge pull request #103 — năm bài học đo được của đợt 14-08
changed_paths=['CLAUDE.md', 'docs/GOI_AGENT_DA_NEN.md']
92783f6 2026-08-14T18:54:15+07:00 Merge pull request #106 — bài học tầng vận chuyển cũng chuẩn hoá chuỗi
changed_paths=['CLAUDE.md']
624cdc0 2026-08-14T19:18:22+07:00 Merge pull request #107 — neo bộ kiểm lease vào nhánh mặc định, biên nhận cho verdict
changed_paths=['.github/workflows/ops-publish-lease.yml', 'ops/README.md', 'ops/lease_publish_test.py', 'ops/reviews/wp55-r2-review-4-codex-verdict.receipt.yaml']
3d67128 2026-08-14T19:27:57+07:00 Merge pull request #108 — sửa chốt (b) và mô hình lớp của bài học tầng vận chuyển
changed_paths=['CLAUDE.md']
ci_os_at_9796f67=${{ fromJSON( (github.event_name == 'workflow_dispatch' || github.ref == 'refs/heads/master' || contains(github.event.pull_request.labels.*.name, 'windows')) && '["ubuntu-latest","windows-latest"]' || '["ubuntu-latest"]') }}
ci_os_at_06a50c5feea77c2654f31edd26efeed7eeee62f5=${{ (github.event_name == 'workflow_dispatch' || contains(github.event.pull_request.labels.*.name, 'windows')) && '["ubuntu-latest","windows-latest"]' || '["ubuntu-latest"]' }}
LIMIT: Git tree không lưu mọi lần dispatch, nhãn PR hoặc sáu run cụ thể của phiên 14-08. Không suy sáu merge = sáu Windows execution từ matrix. Câu sáu lần vốn có từ PR109; diff mới đặt nó vào bối cảnh lịch sử.
rc=0
```

Kết luận: **KHÔNG ĐO ĐƯỢC**.

### HƯỚNG 11: Đóng lớp P2 cũ ở mọi vị trí và kiểm các lời giải thích

Giả thuyết: Bản vá có thể chỉ thay một câu, để lại diễn đạt tuyệt đối hoặc bỏ ngoại lệ.

Lệnh (cwd=`cay-kho/`):

```bash
PYTHONDONTWRITEBYTECODE=1 python3 ../review_probe.py scope
```

Output thật:

```text
PRIOR_VERDICT_SOURCE=7a2eecf:ops/reviews/pr870-review-1-codex-verdict.md (chỉ dùng làm tài liệu lượt1, không thay cây runtime của SHA review)
### master-windows-bo-sot-dispatch  [P2]  Giới hạn lời khai Windows trên master vào push tự động
TỆP/DÒNG: `CLAUDE.md:169` (liên quan cách hiểu “KHÔNG BAO GIỜ” tại 173–174).
VẤN ĐỀ: Câu nhấn mạnh “Windows trên master hiện chỉ đến từ launcher-windows.yml” khai rộng hơn cấu hình đã đo. `ci.yml` vẫn khai `workflow_dispatch`; output `chuan-bi.os` chọn Windows theo event này mà không loại `refs/heads/master`. Vì vậy cùng một ref master có thể có Windows từ gate `ci.yml`, đúng như chính dòng 176 hướng dẫn. Thiếu từ “tự động khi push” khiến người đọc lại suy phạm vi phủ Windows từ một câu doctrine thay vì đọc event/ref. Đây là P2 về thiếu điều kiện, không phải P1 cho số job/run/SHA (các số đã đo đều khớp).
ĐÃ THỬ NGHIỆM: HƯỚNG 13, evaluator nguyên hàm `ops/lease_publish_test.py:7848`, lấy biểu thức từ workflow thật: `push + refs/heads/master => [ubuntu-latest]`; `workflow_dispatch + refs/heads/master => [ubuntu-latest, windows-latest]`, `rc=0`, marker `COUNTEREXAMPLE PASS`. HƯỚNG 2/7/9 xác nhận trigger, consumers và không có chốt ref khác. Chưa tạo/chạy Actions run thật vì sandbox không mạng.
GỢI Ý VÁ: Sửa ngay L169 thành “Windows tự động khi push master …”; tại L173–174 giới hạn hệ quả vào các lượt PR/push của `ci.yml` theo ma trận đang đo. Không mở rộng thành mọi gate: protocol T3 và ADR-0049 vẫn nói tới gate Windows tại chỗ trước phát hành. `HINT.patch` là gợi ý cho hai chỗ cùng phạm vi này.
CA KHÓA: Giữ bảng năm context ở HƯỚNG 13, đặc biệt phân biệt push/master với dispatch/master; đối chiếu lại câu mới có nêu phạm vi push tự động. Không cần thêm test sản phẩm cho một sửa tài liệu.
RỦI RO BẢN VÁ: Chỉ thu hẹp mô tả; phải giữ nguyên ngoại lệ dispatch/label và điều kiện paths của launcher. Không đổi workflow, gate policy hoặc miễn nghĩa vụ gate Windows tại chỗ.
ĐỘ TIN: cao.

$ git diff b38fce8 06a50c5feea77c2654f31edd26efeed7eeee62f5 -- CLAUDE.md
diff --git a/CLAUDE.md b/CLAUDE.md
index 0a00adc..e6bbe1d 100644
--- a/CLAUDE.md
+++ b/CLAUDE.md
@@ -166,12 +166,12 @@ Phiên dev trên máy này ≠ phiên Cowork LIVE (bootstrap từ zip Package 
   `ops/land/pr848-wp744-provenance/readback-jobs-39354156843.json`. Doctrine cũ đã kịp làm một biên
   bản land (commit `3f6c694`) khai `jobs: '23/23 success (gom windows)'`; Codex connector bắt thành P1 trên PR #859 (comment
   `r4323607674`), sửa ở PR #865. Đúng bệnh mục này đang dạy: tin một câu GẦN TAY thay vì đọc nhãn job.
-  **Windows trên master hiện chỉ đến từ `launcher-windows.yml`**, và CÓ ĐIỀU KIỆN: push master chỉ bắn
+  **Windows tự động khi push master hiện chỉ đến từ `launcher-windows.yml`**, và CÓ ĐIỀU KIỆN: chỉ bắn
   khi đổi `.claude/dev/**` hoặc chính tệp workflow ấy (`paths:`), ma trận `windows-latest` + `ubuntu-latest`;
   PR chỉ chạy khi mang nhãn `windows` (workflow này CÓ khai `types: [..., labeled]`). Nó chỉ đo lane
   launcher, KHÔNG phải gate. Các workflow còn lại (`ci-dot-bien-du` `ops-*`) đều `ubuntu-latest`.
-  Hệ quả: với một PR THƯỜNG — không nhãn `windows`, không ai gọi tay — **gate của mã đó KHÔNG BAO GIỜ
-  được đo trên Windows, kể cả sau merge**; merge không còn là "lần đo Windows đầu tiên" như bản cũ viết.
+  Hệ quả: với một PR THƯỜNG — không nhãn `windows`, không ai gọi tay — **các lượt PR và push hậu merge
+  của `ci.yml` theo ma trận hiện tại chỉ đo Ubuntu**; merge không còn là "lần đo Windows đầu tiên" như bản cũ viết.
   Muốn biết master có Windows hay không thì **đọc nhãn từng job của lượt chạy**, đừng suy từ tên sự kiện.
   **Muốn có Windows cho gate thì đường CHẮC CHẮN là gọi tay `workflow_dispatch` trên ref đó.**
   Gắn nhãn `windows` KHÔNG đủ cho một PR ĐANG MỞ, và đây là bẫy thật (cross-review bắt, P2 thứ hai

BASE_OLD_QUOTE:
158:   · **(c) Gate PR và gate master KHÔNG phải một thứ.** `ci.yml` cố ý chỉ chạy `ubuntu` cho PR thường,
159:   còn master chạy CẢ `ubuntu` LẪN `windows` (Windows tốn gấp đôi phút, để dành cho lượt gác cổng phát
160:   hành). Nên **"PR xanh" không hàm ý "master xanh"**: với một PR THƯỜNG — không gắn nhãn `windows`,
161:   không ai gọi tay — lần merge chính là lần đo Windows ĐẦU TIÊN của mã đó. Nói CÓ ĐIỀU KIỆN vì ma
162:   trận cũng kèm `windows-latest` cho PR gắn nhãn `windows` và cho `workflow_dispatch`; bỏ điều kiện
163:   ấy là đánh lừa người đang xem đúng một PR như vậy (cross-review bắt được, P2 trên PR #109 — và
164:   trớ trêu là đoạn ngay trên đã trích đúng điều kiện đó rồi vẫn viết câu quên nó).
165:   **Muốn có Windows TRƯỚC khi merge thì đường CHẮC CHẮN là gọi tay `workflow_dispatch` trên ref đó.**
166:   Gắn nhãn `windows` KHÔNG đủ cho một PR ĐANG MỞ, và đây là bẫy thật (cross-review bắt, P2 thứ hai
SCOPE_FIX_ASSERTIONS=passed (cả hai vị trí của finding cũ; ngoại lệ dispatch/label vẫn còn)
AUTHOR_CAUSATION: có doctrine cũ và biên bản sai cùng tồn tại; không có transcript đủ chứng minh doctrine đã gây lời khai của executor 3f6c694.
AUTHOR_MEASUREMENT_DATE: base/head commits ngày 22-10-2026; không có transcript gốc chứng minh tác giả thực chạy phép đo vào ngày ấy.
rc=0
```

Kết luận: **KHÔNG PHẢI LỖI**.

### HƯỚNG 12: Cùng chính sách OS với sự khác nhau giữa gate PR và land

Giả thuyết: Tiêu đề mới có thể khiến quy tắc bộ bước PR và land mâu thuẫn với nhau.

Lệnh (cwd=`cay-kho/`):

```bash
PYTHONDONTWRITEBYTECODE=1 python3 ../review_probe.py gate_scope
```

Output thật:

```text
gate: {"name": "release-verify strict (lane LAND — manifest committed)", "if": "github.ref == 'refs/heads/master'", "run": "python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json"}
gate: {"name": "release-verify strict (lane WORKER — manifest TẠM ngoài repo)", "if": "github.ref != 'refs/heads/master'", "run": "set -euo pipefail\nTAM=\"$RUNNER_TEMP/tl-manifest-tam.json\"\nNKY=\"$RUNNER_TEMP/tl-manifest-tam.log\"\n# Cả hai lệnh in ~900 dòng JSON, nên đẩy ra tệp — nhưng IM LẶNG lúc ĐỎ là mất chẩn\n# đoán đúng lúc cần nhất, nên hỏng thì `cat` ra log. Đã đo: redirect chạy được cả khi\n# `RUNNER_TEMP` mang dạng Windows (ổ đĩa + dấu chéo ngược) dưới Git Bash.\npython scripts/tl.py release-manifest --root . --out \"$TAM\" --json > \"$NKY\" || { cat \"$NKY\"; exit 1; }\npython scripts/tl.py release-verify \"$TAM\" --root . --strict --json > \"$NKY\" || { cat \"$NKY\"; exit 1; }\npython - \"$TAM\" <<'PY'\nimport json, subprocess, sys\nra = subprocess.run([\"git\", \"ls-files\", \"-z\"], capture_output=True, check=True).stdout\ntheo_doi = set(ra.decode(\"utf-8\").split(chr(0))) - {\"\"}\nduong = [f[\"path\"] for f in json.load(open(sys.argv[1], encoding=\"utf-8\"))[\"files\"]]\nthua = sorted(p for p in duong if p not in theo_doi)\nfor p in thua:\n    print(\"TEP THUA trong cay, git khong theo doi:\", p)\nif thua:\n    sys.exit(1)\nprint(\"manifest tam:\", len(duong), \"tep, tat ca deu duoc git theo doi\")\nPY\n"}
PROTOCOL_T3=  gate_tier: T0 | T1 | T2 | T3 | T4 | T5
ADR0049_RELEVANT:
5: ADR này ghi nhận việc **đổi tiêu chuẩn gate**: cổng kiểm thử hai nền (Linux và Windows) trước khi phát hành được bảo đảm bằng **cổng tại chỗ của `deploy-package.*`**, KHÔNG phải bằng lane `master` của `.github/workflows/ci.yml`.
9: Từ quyết định grilling 2026-07-09 (#8), `ci.yml` chạy cả `ubuntu-latest` và `windows-latest` để bắt lớp lỗi phụ thuộc nền (mã hóa cp1258, ký tự xuống dòng, đường dẫn file). Tuy nhiên, các phép đo thực tế (16-09-2026, nền `f27a28f`) cho thấy hai bất cập lớn:
17: 1. **Đổi cò Windows trong `ci.yml`:** Bỏ điều kiện `github.ref == 'refs/heads/master'`. Windows chỉ còn kích hoạt khi gọi tay qua `workflow_dispatch` hoặc khi PR có nhãn `windows` (dành cho các thay đổi chạm mã phụ thuộc nền tảng).
23: - **Mất soi Windows tự động cho ~22 bước test:** Việc bỏ Windows khỏi mỗi lần land vào `master` đồng nghĩa ~22 bước kiểm thử trong `ci.yml` (như `lease_publish_test`, `ci_dang_ky_test`, `packet-loop selftest`) không còn được chạy tự động trên Windows sau mỗi commit vào master.
26:   - `ci.yml` dùng trigger `pull_request` mặc định (không khai `types: [labeled]`), nên gắn nhãn `windows` lên PR đang đứng yên không tự kích hoạt run mới mà chỉ ăn ở lần push kế tiếp (`synchronize`) hoặc khi tạo PR đã có nhãn.
27:   - Dưới chính sách `manual_ci_budget: 0` (cấm `workflow_dispatch`), Windows tự động không còn chạy cho `ops/**`, `scripts/**`, `.github/**` (WP541 là bằng chứng sống).
34: - Workflow `.github/workflows/launcher-windows.yml` (với `paths: .claude/dev/**`) vẫn được giữ nguyên. Mọi thay đổi chạm `.claude/dev/**` khi push vào `master` vẫn kích hoạt và tiêu tốn ~5 phút Windows (Đ6, run `35125176975`).
rc=0
```

Kết luận: **KHÔNG PHẢI LỖI**.

### HƯỚNG 13: So snapshot nội dung đầu/cuối, kể cả ignored và index

Giả thuyết: Phép đo có thể đã làm đổi checkout hoặc định danh SHA.

Lệnh (cwd=`cay-kho/`):

```bash
PYTHONDONTWRITEBYTECODE=1 python3 ../review_probe.py sandbox_end
```

Output thật:

```text
head_same=True
tree_same=True
status_same=True
diff_same=True
cached_diff_same=True
final_HEAD=06a50c5feea77c2654f31edd26efeed7eeee62f5
final_tree=0fa694daf17e10c37fc3e61690531ade4bd528bf
final_status_with_ignored=''
files_hashed=4843
added=[]
removed=[]
changed=[]
all_snapshot_equal=True
rc=0
```

Kết luận: **KHÔNG PHẢI LỖI**.

### HƯỚNG 12: Cùng chính sách OS với sự khác nhau giữa gate PR và land

Giả thuyết: Tiêu đề mới có thể khiến quy tắc bộ bước PR và land mâu thuẫn với nhau.

Lệnh (cwd=`cay-kho/`):

```bash
PYTHONDONTWRITEBYTECODE=1 python3 ../review_probe.py gate_scope
```

Output thật:

```text
gate: {"name": "release-verify strict (lane LAND — manifest committed)", "if": "github.ref == 'refs/heads/master'", "run": "python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json"}
gate: {"name": "release-verify strict (lane WORKER — manifest TẠM ngoài repo)", "if": "github.ref != 'refs/heads/master'", "run": "set -euo pipefail\nTAM=\"$RUNNER_TEMP/tl-manifest-tam.json\"\nNKY=\"$RUNNER_TEMP/tl-manifest-tam.log\"\n# Cả hai lệnh in ~900 dòng JSON, nên đẩy ra tệp — nhưng IM LẶNG lúc ĐỎ là mất chẩn\n# đoán đúng lúc cần nhất, nên hỏng thì `cat` ra log. Đã đo: redirect chạy được cả khi\n# `RUNNER_TEMP` mang dạng Windows (ổ đĩa + dấu chéo ngược) dưới Git Bash.\npython scripts/tl.py release-manifest --root . --out \"$TAM\" --json > \"$NKY\" || { cat \"$NKY\"; exit 1; }\npython scripts/tl.py release-verify \"$TAM\" --root . --strict --json > \"$NKY\" || { cat \"$NKY\"; exit 1; }\npython - \"$TAM\" <<'PY'\nimport json, subprocess, sys\nra = subprocess.run([\"git\", \"ls-files\", \"-z\"], capture_output=True, check=True).stdout\ntheo_doi = set(ra.decode(\"utf-8\").split(chr(0))) - {\"\"}\nduong = [f[\"path\"] for f in json.load(open(sys.argv[1], encoding=\"utf-8\"))[\"files\"]]\nthua = sorted(p for p in duong if p not in theo_doi)\nfor p in thua:\n    print(\"TEP THUA trong cay, git khong theo doi:\", p)\nif thua:\n    sys.exit(1)\nprint(\"manifest tam:\", len(duong), \"tep, tat ca deu duoc git theo doi\")\nPY\n"}
PROTOCOL_T3=| T3 | integration freeze/`land prepare` | full selftest và release gates trên Windows + Linux cho frozen integration SHA |
ADR0049_RELEVANT:
5: ADR này ghi nhận việc **đổi tiêu chuẩn gate**: cổng kiểm thử hai nền (Linux và Windows) trước khi phát hành được bảo đảm bằng **cổng tại chỗ của `deploy-package.*`**, KHÔNG phải bằng lane `master` của `.github/workflows/ci.yml`.
9: Từ quyết định grilling 2026-07-09 (#8), `ci.yml` chạy cả `ubuntu-latest` và `windows-latest` để bắt lớp lỗi phụ thuộc nền (mã hóa cp1258, ký tự xuống dòng, đường dẫn file). Tuy nhiên, các phép đo thực tế (16-09-2026, nền `f27a28f`) cho thấy hai bất cập lớn:
17: 1. **Đổi cò Windows trong `ci.yml`:** Bỏ điều kiện `github.ref == 'refs/heads/master'`. Windows chỉ còn kích hoạt khi gọi tay qua `workflow_dispatch` hoặc khi PR có nhãn `windows` (dành cho các thay đổi chạm mã phụ thuộc nền tảng).
23: - **Mất soi Windows tự động cho ~22 bước test:** Việc bỏ Windows khỏi mỗi lần land vào `master` đồng nghĩa ~22 bước kiểm thử trong `ci.yml` (như `lease_publish_test`, `ci_dang_ky_test`, `packet-loop selftest`) không còn được chạy tự động trên Windows sau mỗi commit vào master.
26:   - `ci.yml` dùng trigger `pull_request` mặc định (không khai `types: [labeled]`), nên gắn nhãn `windows` lên PR đang đứng yên không tự kích hoạt run mới mà chỉ ăn ở lần push kế tiếp (`synchronize`) hoặc khi tạo PR đã có nhãn.
27:   - Dưới chính sách `manual_ci_budget: 0` (cấm `workflow_dispatch`), Windows tự động không còn chạy cho `ops/**`, `scripts/**`, `.github/**` (WP541 là bằng chứng sống).
34: - Workflow `.github/workflows/launcher-windows.yml` (với `paths: .claude/dev/**`) vẫn được giữ nguyên. Mọi thay đổi chạm `.claude/dev/**` khi push vào `master` vẫn kích hoạt và tiêu tốn ~5 phút Windows (Đ6, run `35125176975`).
rc=0
```

Kết luận: **KHÔNG PHẢI LỖI**.
