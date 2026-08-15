# Verdict review 9

```yaml
verdict: changes_requested
reviewed_sha: 427021049bc8677f5915da13b8ac38a53c949b93
base_sha: fbe5ab9e1ece3b45c065879bfd59dee2554db3e2
reviewer: codex
executor: claude
```

Không thể duyệt ở SHA này. Gate nền và gate cây đã merge đều xanh, nhưng phản chứng độc lập còn tìm được cả hai chiều mà AC 18/19 yêu cầu chặn: ba đường lọt `rc=0`, hai họ bắt oan `rc=6`, cùng một hình dạng lease mà `record-lease` không sinh ra nhưng `begin-attempt` vẫn nhận.

## Findings

### 1. Miễn trừ “chữ bọc hai phía” vẫn là cửa lọt tổng quát

- `finding_id`: `doctrine-arbitrary-prose-wrapper-bypass`
- `severity`: `P1`
- `disposition`: `must_fix`

`_duoc_tha_vi_ngat_dong` chỉ đòi có một ký tự chữ trước và sau cụm. Vì vậy đúng phản ví dụ executor đã khai — `x người có\nthẩm quyền y` — trả `rc=0`, trong khi đối chứng `Người có thẩm quyền` trả `rc=6`. Chuỗi `x … y` không phải câu văn xuôi kể lại kết quả đo theo AC 19; AC 2 lại đòi bơm một cụm trong danh sách vào adapter phải đỏ. Việc phân biệt mọi câu bằng ngữ nghĩa có thể khó, nhưng không buộc phải tha mọi wrapper: ca thật có thể được neo vào dấu hiệu phép đo hẹp hơn hoặc một ngoại lệ cụ thể, kiểm được.

Bằng chứng: lệnh `doctrine-matrix` ở dưới, case `arbitrary-wrapper`: kỳ vọng `rc=6`, thực tế `rc=0`.

### 2. Bộ dò fence nhận một dòng đóng không hợp lệ và để nội dung code lọt

- `finding_id`: `doctrine-fence-invalid-closer-bypass`
- `severity`: `P1`
- `disposition`: `must_fix`

`_dong_khoi_ma` chỉ nhớ loại ký tự mở, không nhớ độ dài; `_RE_HANG_RAO` cũng không ràng buộc phần đuôi dòng. Do đó cả (a) ba backtick không được phép đóng fence bốn backtick và (b) dòng “``` not-a-close” không phải closing fence đều bị coi là đóng. Đoạn sau đó vẫn nằm trong fence theo cấu trúc Markdown, nhưng bị bỏ khỏi tập `trong_khoi_ma`; miễn trừ AC 19 làm cụm cấm lọt `rc=0`.

Bằng chứng: `invalid-short-closer` và `invalid-info-closer` trong `doctrine-matrix`, cả hai kỳ vọng `rc=6`, thực tế `rc=0`.

### 3. Regex bảng HTML kết thúc bảng ngoài tại thẻ đóng của bảng lồng

- `finding_id`: `doctrine-nested-html-table-bypass`
- `severity`: `P1`
- `disposition`: `must_fix`

`_RE_BANG_HTML` dùng non-greedy span tới `</table>` đầu tiên. Với bảng hợp lệ có một bảng con trong `<td>`, thẻ đóng của bảng con bị coi là thẻ đóng bảng ngoài. Các dòng còn lại của bảng ngoài không còn được đánh dấu; một câu đúng hình dạng ca AC 19 nằm trong ô sau đó được tha và trả `rc=0`. Đây là đúng chiều lọt của chốt g8, độc lập với finding về wrapper tổng quát vì payload dùng chính văn cảnh phép đo mà AC 19 phải tha ngoài bảng.

Bằng chứng: `nested-table` trong `doctrine-matrix`: kỳ vọng `rc=6`, thực tế `rc=0`.

### 4. “Fail-closed” của span mở làm bắt oan toàn bộ phần đuôi

- `finding_id`: `doctrine-structural-opener-poisons-ac19-tail`
- `severity`: `P1`
- `disposition`: `must_fix`

Hai đường mới đều tước miễn trừ AC 19 khỏi văn xuôi hợp lệ đứng sau một cấu trúc vô hại:

- Vì `_RE_HANG_RAO` dùng `^\s*`, một dòng code thụt lề bắt đầu bằng backtick bị coi là fence mở và mọi dòng tới EOF bị đánh dấu code. Case `indented-fence-poison` đổi ca AC 19 vốn `rc=0` thành `rc=6`.
- `_dong_bang_html` không loại code span. Chỉ cần literal `<table>` trong fenced code hoặc inline code, không có `</table>`, regex đánh dấu mọi dòng sau nó là bảng. Hai case `table-in-fence-poison` và `table-inline-code-poison` đều đổi cùng ca AC 19 thành `rc=6`.

Lập luận “fail-closed” không giải quyết được chiều này: AC 19 nói chuẩn hoá mạnh hơn mà bắt oan văn bản bình thường là không đạt, ngang với để lọt.

Bằng chứng: `valid-ac19` trong `doctrine-matrix` trả `rc=0`; ba case poison nêu trên đều trả `rc=6` tại chính dòng của câu hợp lệ.

### 5. Hàm schema lease vẫn nhận khóa ngoài schema

- `finding_id`: `lease-schema-allows-extra-keys`
- `severity`: `P2`
- `disposition`: `must_fix`

`_kiem_luoc_do_lease` kiểm thiếu khóa nhưng không kiểm khóa thừa. `record-lease` chỉ có thể sinh đúng bốn khóa, còn một state có đủ bốn khóa cộng `unexpected: true` vẫn mở được lượt (`rc=0`). Điều này trái bất biến AC 21 rằng `record-lease` là nguồn sự thật của toàn schema và lặp lại đúng tiêu chí “`begin-attempt` nhận state mà `record-lease` không bao giờ sinh ra được”. Khóa thừa hiện bị bỏ qua nên mức độ thấp hơn bypass thiếu khóa cũ, nhưng schema chưa thật sự khép kín.

Bằng chứng: lệnh `lease-extra-key` ở dưới, kỳ vọng mã thoát có kiểm soát khác 0, thực tế `rc=0`, `state running`.

### 6. Số đột biến khai trong gate không tái lập được

- `finding_id`: `packet-suite-mutation-count-mismatch`
- `severity`: `P2`
- `disposition`: `reconcile_evidence`

Hồ sơ khai `39 đột biến`; inventory trực tiếp của immutable test module có `len(MUTANTS) == 38`. Suite vẫn báo 58/58 lớp có mutant và 0 ngoại lệ, nên đây chưa tự nó chứng minh một lớp AC 18 bị bỏ trống; nhưng số gate giao nộp sai và suite không assert con số đã khai. Cần bổ sung mutant còn thiếu nếu 39 là chuẩn, hoặc sửa bằng chứng/đặt assertion đúng con số thực.

Bằng chứng: lệnh `mutation-inventory` ở dưới in `cases=157 mutants=38 exceptions=0`.

## Bằng chứng chạy được, neo SHA bất biến

### `doctrine-matrix`

```bash
REVIEWED=427021049bc8677f5915da13b8ac38a53c949b93
scan() {
  label="$1"; payload="$2"
  out=$(python3 <(git show "$REVIEWED":.claude/dev/packet_loop.py) \
    doctrine-scan --root /tmp/review9-khong-co-root --path /dev/stdin \
    <<< "$payload" 2>&1)
  rc=$?
  printf '%-28s rc=%s  %s\n' "$label" "$rc" "$(printf '%s' "$out" | head -n 1)"
}
scan direct-control $'Người có thẩm quyền'
scan valid-ac19 $'Đo được: ba tên tấn công rc=4, người có\nthẩm quyền vẫn rc=0.'
scan arbitrary-wrapper $'x người có\nthẩm quyền y'
scan invalid-short-closer $'````\n```\nĐo được: ba tên tấn công rc=4, người có\nthẩm quyền vẫn rc=0.\n````'
scan invalid-info-closer $'```\n``` not-a-close\nĐo được: ba tên tấn công rc=4, người có\nthẩm quyền vẫn rc=0.\n```'
scan nested-table $'<table>\n<tr><td><table></table></td></tr>\n<tr><td>Đo được: ba tên tấn công rc=4, người có\nthẩm quyền vẫn rc=0.</td></tr>\n</table>'
scan indented-fence-poison $'    ``` đây chỉ là một dòng code thụt lề\n\nĐo được: ba tên tấn công rc=4, người có\nthẩm quyền vẫn rc=0.'
scan table-in-fence-poison $'```html\n<table>\n```\n\nĐo được: ba tên tấn công rc=4, người có\nthẩm quyền vẫn rc=0.'
scan table-inline-code-poison $'Ví dụ ký hiệu `<table>` trong tài liệu.\n\nĐo được: ba tên tấn công rc=4, người có\nthẩm quyền vẫn rc=0.'
```

Đầu ra đã đo:

```text
direct-control               rc=6  /dev/stdin:1: [bang-vai-tro-muc-2] chép doctrine: 'người có thẩm quyền'
valid-ac19                   rc=0  doctrine-scan: sạch — đã quét 1 tệp, 0 chỗ chép doctrine
arbitrary-wrapper            rc=0  doctrine-scan: sạch — đã quét 1 tệp, 0 chỗ chép doctrine
invalid-short-closer         rc=0  doctrine-scan: sạch — đã quét 1 tệp, 0 chỗ chép doctrine
invalid-info-closer          rc=0  doctrine-scan: sạch — đã quét 1 tệp, 0 chỗ chép doctrine
nested-table                 rc=0  doctrine-scan: sạch — đã quét 1 tệp, 0 chỗ chép doctrine
indented-fence-poison        rc=6  /dev/stdin:3: [bang-vai-tro-muc-2] chép doctrine: 'người có thẩm quyền'
table-in-fence-poison        rc=6  /dev/stdin:5: [bang-vai-tro-muc-2] chép doctrine: 'người có thẩm quyền'
table-inline-code-poison     rc=6  /dev/stdin:3: [bang-vai-tro-muc-2] chép doctrine: 'người có thẩm quyền'
```

### `lease-extra-key`

```bash
REVIEWED=427021049bc8677f5915da13b8ac38a53c949b93
STATE_DIR=$(mktemp -d /tmp/wp55-r9-extra-lease-427021049.XXXXXX)
EXP=$(date -u -d '+4 hours' +%Y-%m-%dT%H:%M:%SZ)
python3 <(git show "$REVIEWED":.claude/dev/packet_loop.py) --state-dir "$STATE_DIR" \
  init --packet 55 --mission 54 --executor claude --reviewer codex >/dev/null
jq --arg exp "$EXP" \
  '.state="leased" | .lease={lease_id:"wp55-r9",granted_by:"ducthangho",evidence:"issuecomment-123456",expires_utc:$exp,unexpected:true}' \
  "$STATE_DIR/wp55.json" > "$STATE_DIR/changed.json"
mv "$STATE_DIR/changed.json" "$STATE_DIR/wp55.json"
python3 <(git show "$REVIEWED":.claude/dev/packet_loop.py) --state-dir "$STATE_DIR" \
  begin-attempt --packet 55 --provider claude
```

Đầu ra: `rc=0`, `bắt đầu lượt 1/3 — state running`.

### `mutation-inventory`

```bash
REVIEWED=427021049bc8677f5915da13b8ac38a53c949b93
TREE=$(mktemp -d /tmp/wp55-r9-mutants-427021049.XXXXXX)
git archive "$REVIEWED" | tar -x -C "$TREE"
python3 - "$TREE" <<'PY'
import importlib.util, sys
from pathlib import Path
p = Path(sys.argv[1]) / ".claude/dev/packet_loop_test.py"
s = importlib.util.spec_from_file_location("review9_packet_suite", p)
m = importlib.util.module_from_spec(s)
s.loader.exec_module(m)
covered = {t for _, (_, _, cases) in m.MUTANTS.items() for t in cases}
exceptions = [name for name, _ in m.LOP_LACH if f"ac18_{name}" not in covered]
print(f"cases={len(m.CASES)} mutants={len(m.MUTANTS)} exceptions={len(exceptions)}")
PY
```

Đầu ra: `rc=0`, `cases=157 mutants=38 exceptions=0`.

## Gate và ranh giới

- Bước 0 đạt: checkout đúng `427021049bc8677f5915da13b8ac38a53c949b93`; shallow=`false`.
- Spec đọc trọn vẹn từ commit bất biến `1fce46a4f6094792368307826c6fb16a851b718b`; SHA-256 đúng `e321f811724fae97b19d523a3e5159bc13b425cd15fc6c753c7439fe28cae22d`.
- Phạm vi diff `fbe5ab9e1ece3b45c065879bfd59dee2554db3e2..427021049bc8677f5915da13b8ac38a53c949b93`: đúng 6 tệp trong `write_set`.
- Suite packet trên cây archive của reviewed SHA: `rc=0`, nền `157/157`, AC 19 `58/58` lớp ánh xạ vào 26 ca, AC 18 `58/58`, 4 mutant phối hợp, 0 ngoại lệ, `TỔNG: ĐẠT`. Inventory thực là 38 mutant, không phải 39.
- `doctrine-scan` trên cây archive của reviewed SHA: `rc=0`, 4 tệp, 0 hit.
- AC 20 với master bất biến `2531366e1abc6cbca0a6c2765e40e54be38d1fb7`: apply diff base→reviewed `rc=0`; `doctrine-scan rc=0`; suite với `GIT_DIR` của repo `rc=0`, `157/157`, `TỔNG: ĐẠT`.
- `doc-claims-check --strict --json`: `rc=0`, `ok=true`, `flags=[]`.
- `release-verify` trên archive reviewed SHA: `rc=0`, `ok=true`, `checked_file_count=179`, `failed=[]`, `extra_files=[]`. Lần chạy trực tiếp ở working tree trả `rc=2` chỉ vì `NHIEM_VU_REVIEW_9.md` ngoài manifest, đúng ngoại lệ đã báo trước, không tính finding.
- `golden-test`: `rc=0`, `ok=true`, 20 case.
- `release-bundle` hai lần trên archive reviewed SHA: cả hai `rc=0`, `file_count=179`; cùng SHA-256 `20c89545566b7682b3ecd2ac2ac0283add5af8a4d6ca377d9acbcde4487f8590`.
- EOL policy: `rc=0`, `ok=true`, checked=282, skipped=22, violations=[].
- `tl.py --selftest`: **ranh giới, không tính finding của packet**. Lệnh bắt buộc trên checkout sau Bước 0 trả `rc=1`, `1694/1696`; hai ca đỏ là `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` và `r268_l2_trichotomy_theo_trang_thai_object`. Không chạy `pip install`, không suy đoán `1696/1696`.

## Evidence §7

```yaml
reviewed_sha: 427021049bc8677f5915da13b8ac38a53c949b93
base_sha: fbe5ab9e1ece3b45c065879bfd59dee2554db3e2
master_sha: 2531366e1abc6cbca0a6c2765e40e54be38d1fb7
spec_commit: 1fce46a4f6094792368307826c6fb16a851b718b
spec_sha256: e321f811724fae97b19d523a3e5159bc13b425cd15fc6c753c7439fe28cae22d
verdict: changes_requested
tests:
  - name: step-0-and-spec-anchor
    status: pass
    evidence: "reviewed SHA đúng; shallow=false; spec SHA-256 khớp"
  - name: write-set-diff
    status: pass
    evidence: "6/6 tệp đúng write_set"
  - name: packet-loop-suite-reviewed-tree
    status: pass
    evidence: "rc=0; 157/157; AC18=58/58; AC19=58/58; TỔNG ĐẠT"
  - name: packet-suite-mutation-inventory
    status: fail
    evidence: "khai 39; đo len(MUTANTS)=38; exceptions=0"
  - name: doctrine-scan-reviewed-tree
    status: pass
    evidence: "rc=0; 4 tệp; 0 hit"
  - name: doctrine-independent-two-way-matrix
    status: fail
    evidence: "3 họ bypass rc=0; 2 họ poison-tail bắt oan rc=6; đối chứng direct rc=6 và AC19 hợp lệ rc=0"
  - name: lease-extra-key
    status: fail
    evidence: "begin-attempt nhận state có khóa ngoài schema; rc=0; state=running"
  - name: ac20-merged-tree-doctrine
    status: pass
    evidence: "master=2531366e1abc6cbca0a6c2765e40e54be38d1fb7; rc=0; 4 tệp; 0 hit"
  - name: ac20-merged-tree-suite
    status: pass
    evidence: "GIT_DIR được đặt; rc=0; 157/157; TỔNG ĐẠT"
  - name: tl-selftest
    status: boundary
    evidence: "rc=1; 1694/1696 do hai ca phụ thuộc ngữ cảnh git; không tính finding"
  - name: doc-claims-check-strict
    status: pass
    evidence: "rc=0; ok=true; flags=[]"
  - name: release-verify-archive
    status: pass
    evidence: "rc=0; checked=179; failed=0; extra=0"
  - name: golden-test
    status: pass
    evidence: "rc=0; ok=true; cases=20"
  - name: release-bundle-determinism
    status: pass
    evidence: "2/2 rc=0; sha256=20c89545566b7682b3ecd2ac2ac0283add5af8a4d6ca377d9acbcde4487f8590"
  - name: eol-policy
    status: pass
    evidence: "rc=0; checked=282; violations=0"
findings:
  - finding_id: doctrine-arbitrary-prose-wrapper-bypass
    severity: P1
    disposition: must_fix
  - finding_id: doctrine-fence-invalid-closer-bypass
    severity: P1
    disposition: must_fix
  - finding_id: doctrine-nested-html-table-bypass
    severity: P1
    disposition: must_fix
  - finding_id: doctrine-structural-opener-poisons-ac19-tail
    severity: P1
    disposition: must_fix
  - finding_id: lease-schema-allows-extra-keys
    severity: P2
    disposition: must_fix
  - finding_id: packet-suite-mutation-count-mismatch
    severity: P2
    disposition: reconcile_evidence
```
