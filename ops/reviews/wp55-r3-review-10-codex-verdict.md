# Verdict review 10

```yaml
verdict: changes_requested
reviewed_sha: 1a4525a20aa360476a6f59cb157c21097919c457
base_sha: fbe5ab9e1ece3b45c065879bfd59dee2554db3e2
reviewer: codex
executor: claude
```

Không thể duyệt SHA này. Sáu finding của lượt 9 có ca hồi quy và đột biến tương ứng đều xanh trong suite, nhưng ma trận độc lập vẫn tìm được cú đánh quá thứ bảy ở cả hai chiều AC 19: ba loại “dấu hiệu phép đo” không chứng minh câu đang kể kết quả đo vẫn mở miễn trừ; khối mã thụt lề CommonMark lọt; và bộ dò bảng HTML có hai sai lệch cấu trúc mới, vừa để lọt bảng thật vừa bắt oan văn xuôi hợp lệ.

Revision 3 đã hết lượt. Finding 1 cần **SỬA SPEC ở revision 4** để biến ngoại lệ ngữ nghĩa của AC 19 thành hợp đồng cơ học có thể kiểm được, rồi sửa mã theo hợp đồng đó. Findings 2–4 là **lỗi mã**; câu chữ AC 2/19 hiện tại đã đủ để kết luận các ca đó.

## Findings

### 1. Dấu hiệu từ vựng không chứng minh cụm đang kể lại kết quả đo

- `finding_id`: `doctrine-measurement-marker-semantic-bypass`
- `severity`: `P1`
- `disposition`: `must_fix_spec_revision_4_and_code`

`_DAU_HIEU_PHEP_DO` chỉ cần thấy marker ở một trong hai dòng biên. Marker có thể là tên tham số `rc=`, phân số `1/2` trong văn xuôi thường, hoặc động từ `đo` trong một câu khác; không ca nào dưới đây kể lại **kết quả đo của cụm doctrine**, nhưng cả ba đều được tha `rc=0`. Đối chứng khẳng định doctrine không marker trả `rc=6`, còn ca AC 19 thật trả `rc=0`, nên lỗi nằm đúng ở điều kiện marker mới chứ không phải scanner đã tắt.

Residual executor khai “cố tình rắc `rc=0` vẫn qua” là giới hạn có thật nhưng mâu thuẫn trực tiếp với AC 19 hiện hành; việc để lại dấu vết dễ đọc không biến câu đó thành “văn xuôi kể lại kết quả đo”. Tuy nhiên, AC 19 đang yêu cầu phân loại ngữ nghĩa mở trên văn xuôi. Revision 4 cần chốt một ngoại lệ cơ học hữu hạn, chẳng hạn một dạng evidence/câu đo chuẩn hoặc allowlist cấu trúc cụ thể; tiếp tục thêm marker từ vựng sẽ chỉ dời cửa lọt.

Bằng chứng chạy được, neo SHA bất biến:

```bash
REVIEWED=1a4525a20aa360476a6f59cb157c21097919c457
scan() {
  label="$1"; payload="$2"
  out=$(printf '%s\n' "$payload" | python3 <(git show "$REVIEWED":.claude/dev/packet_loop.py) \
    doctrine-scan --root /tmp/review10-no-root --path /dev/stdin 2>&1)
  rc=$?
  printf '%-32s rc=%s  %s\n' "$label" "$rc" "$(printf '%s' "$out" | head -n 1)"
}
scan direct-control $'Người có thẩm quyền'
scan ac19-real-measurement $'Đo lại cho thấy người có\nthẩm quyền vẫn trả rc=0.'
scan marker-rc-not-measure $'Tham số rc= được mô tả trước khi chép người có\nthẩm quyền là vai trò.'
scan marker-fraction-ordinary $'Một nửa (1/2) tài liệu chép người có\nthẩm quyền là vai trò.'
scan marker-other-sentence $'Đã đo chiều dài xong. Tài liệu chép người có\nthẩm quyền là vai trò.'
```

Đầu ra đã đo:

```text
direct-control                   rc=6  /dev/stdin:1: [bang-vai-tro-muc-2] chép doctrine: 'người có thẩm quyền'
ac19-real-measurement            rc=0  doctrine-scan: sạch — đã quét 1 tệp, 0 chỗ chép doctrine
marker-rc-not-measure            rc=0  doctrine-scan: sạch — đã quét 1 tệp, 0 chỗ chép doctrine
marker-fraction-ordinary         rc=0  doctrine-scan: sạch — đã quét 1 tệp, 0 chỗ chép doctrine
marker-other-sentence            rc=0  doctrine-scan: sạch — đã quét 1 tệp, 0 chỗ chép doctrine
```

### 2. Khối mã thụt lề CommonMark vẫn hưởng miễn trừ văn xuôi

- `finding_id`: `doctrine-indented-code-block-bypass`
- `severity`: `P1`
- `disposition`: `must_fix_code`

Một khối mã thụt bốn dấu cách chứa dấu hiệu đo và cụm cấm ngắt dòng trả `rc=0`. Đây là khối mã đứng độc lập, không phải dòng nối của danh sách nên residual về sự nhập nhằng danh sách không áp dụng. AC 2 đòi bơm một cụm cấm vào adapter phải đỏ; AC 19 chỉ tha **văn xuôi** kể kết quả đo, không tha code chép nguyên văn. Chỉ bỏ ca `cum_don_fence_thut_bon_dau_cach` khỏi ma trận không đóng được lớp này.

Bằng chứng chạy được, neo SHA bất biến:

```bash
REVIEWED=1a4525a20aa360476a6f59cb157c21097919c457
payload=$'    Đo được rc=0: người có\n    thẩm quyền là vai trò.'
set +e
printf '%s\n' "$payload" | python3 <(git show "$REVIEWED":.claude/dev/packet_loop.py) \
  doctrine-scan --root /tmp/review10-no-root --path /dev/stdin
rc=$?
printf 'rc=%s\n' "$rc"
```

Đầu ra: `doctrine-scan: sạch — đã quét 1 tệp, 0 chỗ chép doctrine`, `rc=0`; kỳ vọng `rc=6`.

### 3. Xoá comment trước khi dò fence làm mất rào đóng thật và che bảng thật

- `finding_id`: `doctrine-comment-erases-fence-closer-bypass`
- `severity`: `P1`
- `disposition`: `must_fix_code`

Trong Markdown dưới đây, dòng 1 mở fence, dòng 3 đóng fence; comment opener ở dòng 2 chỉ là nội dung literal trong code. Bảng từ dòng 6 nằm ngoài fence và phải bị nhận là bảng. Nhưng `_dong_bang_html` xoá span comment dòng 2–4 trước, xoá luôn rào đóng dòng 3; lần dò fence trên bản đã xoá vì thế coi toàn bộ đuôi là code, xoá trắng bảng, và để cụm trong bảng lọt `rc=0`. Hai đối chứng—comment bình thường trước bảng và fence đóng bình thường trước bảng—đều trả `rc=6`, neo đúng lỗi vào thứ tự tiền xử lý mới.

Bằng chứng chạy được, neo SHA bất biến:

```bash
REVIEWED=1a4525a20aa360476a6f59cb157c21097919c457
scan() {
  label="$1"; payload="$2"
  out=$(printf '%s\n' "$payload" | python3 <(git show "$REVIEWED":.claude/dev/packet_loop.py) \
    doctrine-scan --root /tmp/review10-no-root --path /dev/stdin 2>&1)
  rc=$?
  printf '%-30s rc=%s  %s\n' "$label" "$rc" "$(printf '%s' "$out" | head -n 1)"
}
scan comment-erases-real-closer $'```html\n<!--\n```\n-->\n\n<table><tr><td>Đo được rc=0: người có\nthẩm quyền là vai trò.</td></tr></table>'
scan comment-control-no-fence $'<!-- ghi chú -->\n<table><tr><td>Đo được rc=0: người có\nthẩm quyền là vai trò.</td></tr></table>'
scan table-after-closed-fence $'```html\nvo hai\n```\n<table><tr><td>Đo được rc=0: người có\nthẩm quyền là vai trò.</td></tr></table>'
```

Đầu ra đã đo:

```text
comment-erases-real-closer    rc=0  doctrine-scan: sạch — đã quét 1 tệp, 0 chỗ chép doctrine
comment-control-no-fence      rc=6  /dev/stdin:2: [bang-vai-tro-muc-2] chép doctrine: 'người có thẩm quyền'
table-after-closed-fence      rc=6  /dev/stdin:4: [bang-vai-tro-muc-2] chép doctrine: 'người có thẩm quyền'
```

### 4. Regex đếm thẻ bảng nhận token nằm trong script/thuộc tính như markup thật

- `finding_id`: `doctrine-html-table-token-context-bypass`
- `severity`: `P1`
- `disposition`: `must_fix_code`

Phép đếm lồng hiện tìm mọi chuỗi `<table`/`</table>` trên văn bản đã loại comment/code, nhưng không xét ngữ cảnh token HTML. `"</table>"` trong script hoặc trong giá trị thuộc tính làm độ sâu về 0 sớm, nên phần còn lại của bảng thật lọt `rc=0`. Chiều ngược, chuỗi `"<table>"` trong script mở một bảng ma và tước miễn trừ AC 19 của câu đo hợp lệ phía sau (`rc=6`). Đây vừa là lọt vừa là bắt oan từ cùng nguyên nhân, và suite generation 9 chỉ phủ thẻ lồng thật.

Bằng chứng chạy được, neo SHA bất biến:

```bash
REVIEWED=1a4525a20aa360476a6f59cb157c21097919c457
scan() {
  label="$1"; payload="$2"
  out=$(printf '%s\n' "$payload" | python3 <(git show "$REVIEWED":.claude/dev/packet_loop.py) \
    doctrine-scan --root /tmp/review10-no-root --path /dev/stdin 2>&1)
  rc=$?
  printf '%-31s rc=%s  %s\n' "$label" "$rc" "$(printf '%s' "$out" | head -n 1)"
}
scan closer-in-script $'<table>\n<script>const s = "</table>";</script>\n<tr><td>Đo được rc=0: người có\nthẩm quyền là vai trò.</td></tr>\n</table>'
scan closer-in-attribute $'<table>\n<tr><td data-x="</table>">x</td></tr>\n<tr><td>Đo được rc=0: người có\nthẩm quyền là vai trò.</td></tr>\n</table>'
scan opener-in-script $'Ví dụ script: <script>const s="<table>";</script> Đo được rc=0: người có\nthẩm quyền vẫn qua cổng.'
```

Đầu ra đã đo:

```text
closer-in-script               rc=0  doctrine-scan: sạch — đã quét 1 tệp, 0 chỗ chép doctrine
closer-in-attribute            rc=0  doctrine-scan: sạch — đã quét 1 tệp, 0 chỗ chép doctrine
opener-in-script               rc=6  /dev/stdin:1: [bang-vai-tro-muc-2] chép doctrine: 'người có thẩm quyền'
```

## Phán định riêng về ca đổi ma trận

Việc chuyển câu `Quyết định này thuộc về người có\nthẩm quyền...` từ bắt-oan sang lớp lọt là **đọc đúng AC**, không phải finding: câu đó khẳng định nội dung doctrine và không kể lại kết quả đo. Trên SHA được review, nó trả `rc=6`; ca cùng hình dạng nhưng thật sự kể phép đo trả `rc=0`:

```text
doctrine-assertion-no-measure  rc=6  /dev/stdin:1: [bang-vai-tro-muc-2] chép doctrine: 'người có thẩm quyền'
ac19-real-measurement          rc=0  doctrine-scan: sạch — đã quét 1 tệp, 0 chỗ chép doctrine
```

## Gate và ranh giới

- Bước 0 đạt: `git rev-parse HEAD` = `1a4525a20aa360476a6f59cb157c21097919c457`; shallow = `false`.
- Spec đọc trọn vẹn 344 dòng từ commit bất biến `1fce46a4f6094792368307826c6fb16a851b718b`; SHA-256 = `e321f811724fae97b19d523a3e5159bc13b425cd15fc6c753c7439fe28cae22d`.
- Diff `fbe5ab9e1ece3b45c065879bfd59dee2554db3e2..1a4525a20aa360476a6f59cb157c21097919c457`: đúng 6 tệp trong `write_set`; `git diff --check` rc=0.
- Packet suite: rc=0; nền `173/173`; AC 19 `66/66` lớp có ca bắt-oan; AC 18 `66/66`; `44` đột biến; `5` đột biến phối hợp; `0` ngoại lệ; khối số liệu máy in `173` ca, `44` đột biến, `66` lớp lách, `35` ca bắt-oan; `TỔNG: ĐẠT`.
- `doctrine-scan` trên checkout đã neo Bước 0: rc=0; 4 tệp; 0 hit.
- AC 20 trên master bất biến `2531366e1abc6cbca0a6c2765e40e54be38d1fb7`: archive master + apply diff base→reviewed rc=0; doctrine-scan rc=0, 4 tệp, 0 hit; suite với `GIT_DIR` rc=0, `173/173`, `TỔNG: ĐẠT`.
- `doc-claims-check --strict --json`: rc=0; `ok=true`; `flags=[]`.
- `release-verify` trực tiếp trong working tree: rc=2 chỉ vì `NHIEM_VU_REVIEW_10.md` ngoài manifest, đúng ngoại lệ nhiệm vụ. Trên archive bất biến của reviewed SHA: rc=0; checked=179; failed=0; extra=0.
- `golden-test`: rc=0; `ok=true`; 20 ca.
- `release-bundle` hai lần trên archive reviewed SHA: 2/2 rc=0; file_count=179; cùng SHA-256 `20c89545566b7682b3ecd2ac2ac0283add5af8a4d6ca377d9acbcde4487f8590`.
- EOL policy: rc=0; `ok=true`; checked=282; skipped=22; violations=0.
- `tl.py --selftest`: **ranh giới, không tính finding của packet**. Đã chạy được tới cuối nhưng rc=1, `1694/1696`; hai ca đỏ là `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` và `r268_l2_trichotomy_theo_trang_thai_object`, giống ranh giới lượt 9. Không chạy `pip install`, không suy đoán `1696/1696`.
- Không có gate nào khác bị bỏ qua. Không chạy mạng, không commit, không push, không merge/land.

Lệnh AC 20 đã chạy, neo toàn bộ SHA:

```bash
MASTER=2531366e1abc6cbca0a6c2765e40e54be38d1fb7
BASE=fbe5ab9e1ece3b45c065879bfd59dee2554db3e2
REVIEWED=1a4525a20aa360476a6f59cb157c21097919c457
TREE=$(mktemp -d /tmp/wp55-r10-ac20-2531366-1a4525a.XXXXXX)
git archive "$MASTER" | tar -x -C "$TREE"
git diff --binary "$BASE".."$REVIEWED" | git -C "$TREE" apply
python3 -B "$TREE/.claude/dev/packet_loop.py" doctrine-scan --root "$TREE"
GIT_DIR="$PWD/.git" python3 -B "$TREE/.claude/dev/packet_loop_test.py"
```

## Evidence §7

```yaml
reviewed_sha: 1a4525a20aa360476a6f59cb157c21097919c457
base_sha: fbe5ab9e1ece3b45c065879bfd59dee2554db3e2
master_sha: 2531366e1abc6cbca0a6c2765e40e54be38d1fb7
spec_commit: 1fce46a4f6094792368307826c6fb16a851b718b
spec_sha256: e321f811724fae97b19d523a3e5159bc13b425cd15fc6c753c7439fe28cae22d
verdict: changes_requested
tests:
  - name: step-0-and-spec-anchor
    status: pass
    evidence: "reviewed SHA đúng; shallow=false; spec 344 dòng và SHA-256 khớp"
  - name: write-set-and-diff-check
    status: pass
    evidence: "6/6 tệp đúng write_set; git diff --check rc=0"
  - name: packet-loop-suite-reviewed-tree
    status: pass
    evidence: "rc=0; nền 173/173; 44 mutant; AC18=66/66; AC19=66/66; 0 ngoại lệ; TỔNG ĐẠT"
  - name: doctrine-scan-reviewed-tree
    status: pass
    evidence: "rc=0; 4 tệp; 0 hit"
  - name: doctrine-measurement-marker-matrix
    status: fail
    evidence: "3 câu không kể kết quả đo cùng lọt rc=0; đối chứng doctrine rc=6; ca AC19 thật rc=0"
  - name: doctrine-indented-code-block
    status: fail
    evidence: "khối mã thụt 4 dấu cách chứa cụm cấm và rc= lọt rc=0"
  - name: doctrine-comment-fence-order
    status: fail
    evidence: "comment erases real closer: rc=0; hai control cấu trúc trả rc=6"
  - name: doctrine-html-token-context-two-way
    status: fail
    evidence: "closer trong script/attribute làm bảng thật lọt rc=0; opener trong script bắt oan rc=6"
  - name: review9-lease-extra-key-regression
    status: pass
    evidence: "suite 173/173 và mutant bo_kiem_khoa_thua_trong_luoc_do_lease giết đúng ca đích"
  - name: ac20-merged-tree-doctrine
    status: pass
    evidence: "master=2531366e1abc6cbca0a6c2765e40e54be38d1fb7; apply rc=0; scan rc=0; 4 tệp; 0 hit"
  - name: ac20-merged-tree-suite
    status: pass
    evidence: "GIT_DIR được đặt; rc=0; 173/173; 44 mutant; TỔNG ĐẠT"
  - name: tl-selftest
    status: boundary
    evidence: "rc=1; 1694/1696; hai ca đỏ r226 và r268; không tính finding packet"
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
    evidence: "rc=0; checked=282; skipped=22; violations=0"
findings:
  - finding_id: doctrine-measurement-marker-semantic-bypass
    severity: P1
    disposition: must_fix_spec_revision_4_and_code
  - finding_id: doctrine-indented-code-block-bypass
    severity: P1
    disposition: must_fix_code
  - finding_id: doctrine-comment-erases-fence-closer-bypass
    severity: P1
    disposition: must_fix_code
  - finding_id: doctrine-html-table-token-context-bypass
    severity: P1
    disposition: must_fix_code
```
