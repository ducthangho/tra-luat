---
description: Gate T0–T2 targeted-first — test component/probe trước, không lặp full exact-SHA đã có trên CI
---

Áp gate phân tầng theo `docs/PROTOCOL_DA_PHIEN.md` §10.1 và ADR-0035. Lệnh này **không phải affected-test
selector**: phiên phải lấy suite/probe bắt buộc từ Packet Spec, changed paths và risk; path/runner/security/
release/EOL chưa phân loại phải fallback `/gate`.

Trình tự:

1. Readback exact `HEAD`, tree, tracked status và CI run gắn với chính SHA đó.
2. Chạy compile/test mới/sửa, paired controls và suite component trước. Gate đỏ thì dừng vòng edit; chưa chạy full.
3. T1 push/handoff: chờ CI tạo full evidence exact-head. Không chạy một bản full local trùng lặp chỉ để lấy cùng
   tín hiệu.
4. T2 review: tải artifact `gate-evidence-<OS>-<attempt>` của run `gate`; validate exact identity bằng runner dưới.
   Reviewer vẫn chạy adversarial probes và coverage-gap tests độc lập.
5. CI thiếu/red/stale, identity không khớp, hoặc packet thuộc fallback class ⇒ chạy `/gate`.

Chạy một targeted suite có evidence (thay lệnh sau `--` bằng suite của packet):

```bash
cd /c/qh/tra-luat && P=/c/Python313/python
HEAD_SHA=$(git rev-parse HEAD)
BASE_SHA=$(git merge-base origin/master HEAD)
mkdir -p scripts/.tl_state/gate
$P .claude/dev/gate_lifecycle.py run \
  --kind targeted --name packet-component --repo . \
  --evidence scripts/.tl_state/gate/packet-component.json \
  --output scripts/.tl_state/gate/packet-component.out \
  --selected-test packet-component \
  --expected-head "$HEAD_SHA" --base-sha "$BASE_SHA" --timeout-seconds 300 \
  --positive-regex '(?m)^.*\b([1-9][0-9]*)/\1\b[^\r\n]*\r?\n?\Z' -- \
  $P path/to/component_test.py
```

Một suite mutation/subprocess nặng phải đổi `--kind targeted` thành `--kind heavy` và thêm
`--wait-seconds 900`; như vậy nó xếp hàng sau heavy gate khác trên cùng host thay vì tranh CPU/I/O.

Sau khi tải CI artifact, validate fail-closed. Phải truyền system/Python/command đúng lane mà checkpoint yêu cầu;
không dùng runtime local để giả rằng evidence Ubuntu là evidence Windows:

```bash
$P .claude/dev/gate_lifecycle.py validate \
  --evidence /path/to/tl-selftest-Linux.json \
  --output /path/to/tl-selftest-Linux.out \
  --expected-head "$HEAD_SHA" \
  --expected-tree "$(git rev-parse HEAD^{tree})" \
  --expected-base-sha "$BASE_SHA" \
  --expected-name tl-selftest \
  --expected-system Linux \
  --expected-python '<exact-artifact-python-version>' \
  --expected-system-release '<exact-artifact-system-release>' \
  --expected-machine '<exact-artifact-machine>' \
  --expected-python-implementation '<exact-artifact-python-implementation>' \
  --expected-selected-test full-selftest \
  --expected-command-json '["python","scripts/tl.py","--selftest"]' \
  --expected-positive-regex '(?m)^.*\b([1-9][0-9]*)/\1\b[^\r\n]*\r?\n?\Z' \
  --require-current-runner
```

`python_version` phải lấy từ artifact, không đoán patch version; ví dụ trên chỉ minh họa hình dạng. `reusable=false`,
artifact thiếu, tracked tree bẩn hoặc SHA/tree/runner/command/runtime lệch đều là thiếu evidence, không phải pass.
