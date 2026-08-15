# Verdict review 11

> Không thể đăng GitHub trong container (API 403, không có `gh`); verdict được giao qua tệp này để phiên điều phối đăng hộ.

```yaml
verdict: changes_requested
reviewed_sha: 4085bbf22d565a4189977f0504dfd8e5f748bfce
base_sha: fbe5ab9e1ece3b45c065879bfd59dee2554db3e2
master_sha: d5b7bccd679480f2eb9e7f7d84c518bade7f7df1
reviewer: codex
executor: claude
```

Bản vá an ninh mới đạt: diff `1a4525a20aa360476a6f59cb157c21097919c457..4085bbf22d565a4189977f0504dfd8e5f748bfce` chỉ sửa `.claude/skills/work-packet/SKILL.md`; snippet không in giá trị bí mật. Bash và dash dưới `-u` đều cho unset/rỗng → `chưa đặt`, ba khoảng trắng → `có, 3 ký tự`, secret sáu ký tự → `có, 6 ký tự`. Chuỗi chỉ khoảng trắng được xem là có giá trị, phù hợp phép kiểm `-n`; zsh và PowerShell không có trong nền nên chưa kiểm. Đây là cú pháp shell POSIX/Bash, không phải PowerShell; adapter dùng fenced block `bash`, nên không có mơ hồ shell. Chú thích mới mô tả đúng cơ chế bung giá trị của `:-`. Quét cả ba adapter không thấy đường in bí mật khác.

Không thể duyệt SHA: bốn P1 lượt 10 vẫn tái lập không đổi. Đặc biệt, AC 19 hiện tại **không thể cưỡng chế máy một cách vừa sound vừa complete**: “văn xuôi kể lại kết quả đo” là phân loại ngữ nghĩa mở, còn marker từ vựng (`rc=`, phân số, từ “đo”) không chứng minh quan hệ đó. Revision 4 phải thay ngoại lệ bằng hợp đồng cơ học hữu hạn; vá thêm heuristic tiếp tục tạo lách/bắt oan.

## Findings

### doctrine-measurement-marker-semantic-bypass — P1

`disposition: must_fix_spec_revision_4_and_code`

Lệnh tái lập neo SHA (hàm `scan` dùng chung cho mọi fixture bên dưới):

```bash
REVIEWED=4085bbf22d565a4189977f0504dfd8e5f748bfce
scan() {
  label="$1"; payload="$2"
  out=$(printf '%s\n' "$payload" | python3 <(git show "$REVIEWED":.claude/dev/packet_loop.py) doctrine-scan --root /tmp/review11-no-root --path /dev/stdin 2>&1)
  rc=$?; printf '%-32s rc=%s  %s\n' "$label" "$rc" "$(printf '%s' "$out" | head -n 1)"
}
scan direct-control $'Người có thẩm quyền'
scan ac19-real-measurement $'Đo lại cho thấy người có\nthẩm quyền vẫn trả rc=0.'
scan marker-rc-not-measure $'Tham số rc= được mô tả trước khi chép người có\nthẩm quyền là vai trò.'
scan marker-fraction-ordinary $'Một nửa (1/2) tài liệu chép người có\nthẩm quyền là vai trò.'
scan marker-other-sentence $'Đã đo chiều dài xong. Tài liệu chép người có\nthẩm quyền là vai trò.'
```

Đã đo: control `rc=6`; ca đo thật `rc=0`; cả ba ca không kể kết quả đo đều lọt `rc=0`.

### doctrine-indented-code-block-bypass — P1

`disposition: must_fix_code`

```bash
scan indented-code $'    Đo được rc=0: người có\n    thẩm quyền là vai trò.'
scan prose-control $'Đo được rc=0: người có\nthẩm quyền là vai trò.'
```

Fixture code thụt bốn dấu cách lọt `rc=0`; đối chứng khác đúng một biến (bỏ bốn dấu cách) cũng `rc=0` vì là văn xuôi AC19 hợp lệ. Kỳ vọng code `rc=6`.

### doctrine-comment-erases-fence-closer-bypass — P1

`disposition: must_fix_code`

```bash
scan comment-erases-real-closer $'```html\n<!--\n```\n-->\n\n<table><tr><td>Đo được rc=0: người có\nthẩm quyền là vai trò.</td></tr></table>'
scan closer-one-variable-control $'```html\n<!--\n```\n--x>\n\n<table><tr><td>Đo được rc=0: người có\nthẩm quyền là vai trò.</td></tr></table>'
scan table-after-closed-fence $'```html\nvo hai\n```\n<table><tr><td>Đo được rc=0: người có\nthẩm quyền là vai trò.</td></tr></table>'
```

Fixture lọt `rc=0`; đối chứng thay đúng một ký tự `-->`→`--x>` và đối chứng fence bình thường đều `rc=6`.

### doctrine-html-table-token-context-bypass — P1

`disposition: must_fix_code`

```bash
scan closer-in-script $'<table>\n<script>const s = "</table>";</script>\n<tr><td>Đo được rc=0: người có\nthẩm quyền là vai trò.</td></tr>\n</table>'
scan closer-script-one-variable-control $'<table>\n<script>const s = "< table>";</script>\n<tr><td>Đo được rc=0: người có\nthẩm quyền là vai trò.</td></tr>\n</table>'
scan closer-in-attribute $'<table>\n<tr><td data-x="</table>">x</td></tr>\n<tr><td>Đo được rc=0: người có\nthẩm quyền là vai trò.</td></tr>\n</table>'
scan closer-attribute-one-variable-control $'<table>\n<tr><td data-x="< table>">x</td></tr>\n<tr><td>Đo được rc=0: người có\nthẩm quyền là vai trò.</td></tr>\n</table>'
scan opener-in-script $'Ví dụ script: <script>const s="<table>";</script> Đo được rc=0: người có\nthẩm quyền vẫn qua cổng.'
scan opener-script-one-variable-control $'Ví dụ script: <script>const s="</table>";</script> Đo được rc=0: người có\nthẩm quyền vẫn qua cổng.'
```

Hai closer giả làm bảng thật lọt `rc=0`; opener giả bắt oan `rc=6`. Các đối chứng đổi đúng một ký tự trong token giả (slash thành space, hoặc thêm slash) lần lượt cho `rc=6`, `rc=6`, `rc=0`.

## Gate và boundaries

- Bước 0: shallow=false; remote đúng; spec SHA-256 `e321f811724fae97b19d523a3e5159bc13b425cd15fc6c753c7439fe28cae22d`; reviewed ref và checkout cùng `4085bbf22d565a4189977f0504dfd8e5f748bfce`; prompt SHA-256 `7ddb25545f7bb35a1a7a436bbb872771cf4d5356733472d1f3ca75057eacecdb`. `git fetch` và ghi `core.abbrev` bị Git metadata read-only chặn; ref cục bộ vẫn khớp neo bắt buộc.
- Diff base→reviewed đúng 6 tệp; `git diff --check` rc=0.
- Packet suite checkout: rc=0; 173/173; 44 mutant; 66 lớp lách; 35 ca bắt-oan; AC18 66/66; 0 ngoại lệ; TỔNG ĐẠT. Doctrine scan: rc=0, 4 tệp, 0 hit.
- AC20 với master bất biến `d5b7bccd679480f2eb9e7f7d84c518bade7f7df1`: archive + apply base→reviewed; scan rc=0; suite rc=0, 173/173, TỔNG ĐẠT.
- `doc-claims-check --strict --json`: rc=0, `ok=true`, `flags=[]`. `release-verify`: rc=0, `ok=true`, `failed=[]`. `golden-test`: rc=0. EOL: rc=0, checked=282, violations=0.
- Release bundle head ×2 và base+patch ×1 cùng SHA-256 `20c89545566b7682b3ecd2ac2ac0283add5af8a4d6ca377d9acbcde4487f8590`.
- `tl.py --selftest`: **không chạy tới tổng kết**; rc=1 tại `r319_khong_bien_tuy_chon_thanh_chan_cung`, `ModuleNotFoundError: _cffi_backend` dẫn tới `pyo3_runtime.PanicException` từ cryptography. Không suy đoán hoặc mượn số tổng.
- Không kiểm zsh/PowerShell vì binary không có. Không có finding mới ngoài bốn finding tồn tại. Không nêu lại hai mục đã hoãn revision 4.

## Evidence §7

```yaml
reviewed_sha: 4085bbf22d565a4189977f0504dfd8e5f748bfce
base_sha: fbe5ab9e1ece3b45c065879bfd59dee2554db3e2
master_sha: d5b7bccd679480f2eb9e7f7d84c518bade7f7df1
verdict: changes_requested
security_patch: pass
tests:
  packet_suite: "pass: 173/173"
  doctrine_scan: "pass: 4 files, 0 hits"
  four_review10_findings: "fail: all reproduced unchanged"
  ac20_merged_tree: "pass: scan and 173/173 suite"
  doc_claims_strict: "pass: flags=[]"
  release_verify: pass
  golden_test: pass
  eol: "pass: violations=0"
  release_bundle: "pass: 3/3 sha256 equal"
  tl_selftest: "boundary: pyo3 PanicException; no final count"
findings:
  - {finding_id: doctrine-measurement-marker-semantic-bypass, severity: P1, disposition: must_fix_spec_revision_4_and_code}
  - {finding_id: doctrine-indented-code-block-bypass, severity: P1, disposition: must_fix_code}
  - {finding_id: doctrine-comment-erases-fence-closer-bypass, severity: P1, disposition: must_fix_code}
  - {finding_id: doctrine-html-table-token-context-bypass, severity: P1, disposition: must_fix_code}
```
