# Verdict viết lại cụm trong `CLAUDE.md`

```yaml
verdict: approve
reviewed_sha: c47a439997e0191427d775636ebadbf3be7e1481
base_sha: 2531366e1abc6cbca0a6c2765e40e54be38d1fb7
reviewer: codex
executor: claude
land_recommendation: fast_forward
```

**Approve.** Commit có thể được fast-forward lên nhánh mặc định: nó dựng trực tiếp trên
đúng base, chỉ đổi hai dòng của `CLAUDE.md`, giữ đúng nghĩa của bản ghi phép đo PR #104,
và loại nhu cầu miễn trừ AC 19 mà không tạo finding mới.

## Findings

Không có finding.

## Phán định bốn điểm trọng tâm

### A — bản ghi phép đo vẫn đúng

`e344e7cf84da214f94dd7eb3365392ae4c485cca` là merge commit mang tiêu đề
`Merge pull request #104`; cây đó có `VERSION=1.36.68`. Bản vá của PR là
`39c7ef1a445435ba4c6adc13339bb95d8c660c4f`, dựng trên
`438fc3494a2907cfd49889af4a0eef472dc3d56f`.

Đo trực tiếp hàm `kiem()` ở hai cây cho kết quả:

```text
                         438fc349 (trước)   39c7ef1 (sau)
codex-dispatcher              rc=0               rc=4
ai-codex-bot                  rc=0               rc=4
cödex                         rc=0               rc=4
ducthangho                    rc=0               rc=0
```

Ở bản sau, `NGUOI_CO_THAM_QUYEN = ("ducthangho",)` và cổng kiểm tên đã chuẩn hoá có
nằm trong danh sách ấy hay không. Bộ test đúng cây merge PR #104 cũng đạt 27/27. Vì vậy
“tên thuộc danh sách cho phép vẫn `rc=0`” mô tả chính xác cơ chế và kết quả đã đo; nó
không đánh tráo vai trò hay mở rộng lời khai.

Bằng chứng tái lập, neo toàn bộ vào SHA bất biến:

```bash
git show e344e7cf84da214f94dd7eb3365392ae4c485cca:VERSION
git show --no-patch --format='%H %P %s' e344e7cf84da214f94dd7eb3365392ae4c485cca
PR104_TREE=$(mktemp -d /tmp/review-c47a439-pr104-e344e7c-XXXXXX)
git archive e344e7cf84da214f94dd7eb3365392ae4c485cca | tar -x -C "$PR104_TREE"
python3 "$PR104_TREE/ops/lease_publish_test.py"
# Đã đo: rc=0; lease_publish: 27/27 đạt
```

### B — cụm thay thế không phải cụm cấm

Danh sách tại scanner `1a4525a20aa360476a6f59cb157c21097919c457` có 28 cụm cấm;
không có `danh sách cho phép`, cũng không có cụm cấm nào nằm trong chính chuỗi thay thế.
Scanner trên reviewed tree trả `rc=0`. Cụm này là mô tả cơ chế an ninh phổ thông, không
phải nhãn vai trò hay câu doctrine đóng; nó cũng đã xuất hiện ba lần ở base, trước khi
commit thêm lần xuất hiện thứ tư. Không có căn cứ hiện hành cho thấy bản vá chỉ dời lỗi
sang một cụm sắp bị cấm.

### C — không bỏ sót hình dạng khác

Theo chính tập mục tiêu của `cmd_doctrine_scan`, cả base và head chỉ có một tệp được quét:
`CLAUDE.md` (không có Markdown nào dưới `.claude/skills/` trong hai cây). Tìm trên nội
dung lấy bằng `git show` cho cả hai hình dạng cho kết quả:

```text
base  2531366e…: một-dòng=0; xuyên-khoảng-trắng/xuống-dòng=1 (CLAUDE.md:82)
head  c47a4399…: một-dòng=0; xuyên-khoảng-trắng/xuống-dòng=0
```

Như vậy lời khai “chỗ duy nhất trên toàn bộ tệp bị scanner quét” được tái lập.

### D — đối chứng `rc=6/0` và miễn trừ

Hai tiến trình scanner được chạy riêng và đọc `$?` ngay sau từng tiến trình:

```bash
REFLOW_TREE=$(mktemp -d /tmp/review-c47a439-reflow-XXXXXX)
REWRITE_TREE=$(mktemp -d /tmp/review-c47a439-rewrite-XXXXXX)
git archive 2531366e1abc6cbca0a6c2765e40e54be38d1fb7 | tar -x -C "$REFLOW_TREE"
git archive 2531366e1abc6cbca0a6c2765e40e54be38d1fb7 | tar -x -C "$REWRITE_TREE"
perl -0pi -e 's/người có\n  thẩm quyền/người có thẩm quyền/' "$REFLOW_TREE/CLAUDE.md"
perl -0pi -e 's/người có\n  thẩm quyền/tên thuộc\n  danh sách cho phép/' "$REWRITE_TREE/CLAUDE.md"
python3 <(git show 1a4525a20aa360476a6f59cb157c21097919c457:.claude/dev/packet_loop.py) doctrine-scan --root "$REFLOW_TREE"
reflow_rc=$?
python3 <(git show 1a4525a20aa360476a6f59cb157c21097919c457:.claude/dev/packet_loop.py) doctrine-scan --root "$REWRITE_TREE"
rewrite_rc=$?
printf 'reflow_rc=%s rewrite_rc=%s\n' "$reflow_rc" "$rewrite_rc"
# Đã đo: reflow_rc=6 rewrite_rc=0
```

Nguyên mẫu AC 19 ở `a07e9d51ffd5c4bd35b914b47fd4fc18f5871094` đạt 9/9. Gọi
`khoi_chung_cu()` của đúng nguyên mẫu trên `c47a439…:CLAUDE.md` trả
`reviewed_exempt_lines=0`, `errors=[]`: commit không dựa vào khối chứng cứ.

## Ý kiến thiết kế cho revision 4 — không phải finding

Tôi nghiêng về phương án **(2): bỏ cơ chế miễn trừ, chốt “không cụm cấm nào được xuất
hiện, kể cả ngắt dòng”**. Căn cứ là corpus thật hiện có đúng một mục tiêu quét và không
còn người dùng miễn trừ; trên nhánh spec, ngoài nguyên mẫu, `ac19:evidence` chỉ xuất hiện
trong chính ví dụ quy phạm của spec. Ca E1 chứng minh parser xử lý một mẫu tổng hợp, chưa
chứng minh một hợp đồng miễn trừ có người dùng thật qua toàn bộ vòng đời.

Đơn giản hoá lúc này loại bỏ cả cú pháp, giới hạn khối và bề mặt parser chưa cần thiết.
Nếu sau này xuất hiện một bản ghi lịch sử thật sự không thể viết lại trung thực, cơ chế
có thể được đưa lại cùng chính ca corpus ấy và một test end-to-end. Đây chỉ là khuyến nghị
cho spec; không ảnh hưởng verdict của commit hiện tại.

## Gate và ranh giới review

- Bước 0: pass — exact HEAD/base, non-shallow, diff đúng `CLAUDE.md`, 2 thêm/2 xoá.
- `doctrine-scan` từ `1a4525a…`: rc=0; 1 tệp; 0 hit.
- `eol_policy.py --all --json`: rc=0; checked=308; violations=[]; ok=true.
- `doc-claims-check --strict --json`: rc=0; files_scanned=91; flags=[]; ok=true.
- `golden-test`: rc=0; ok=true; 20/20.
- `git diff --check BASE HEAD`: rc=0.
- `release-verify` trên worktree: rc=2 chỉ vì `NHIEM_VU_VIET_LAI.md` là extra;
  checked=179, failed=[], required_missing=[], package hash khớp.
- `release-verify` bằng `scripts/tl.py` nằm trong archive của exact reviewed SHA: rc=0;
  checked=179, failed=0, extra=0; `CLAUDE.md` không có trong manifest.
- Không truy cập GitHub/network; việc đối chiếu PR #104 dùng merge object, source và test
  đã có cục bộ tại các SHA bất biến nêu trên. Không chạy renderer CommonMark vì patch
  không đổi marker hay topology Markdown. Không cài gói, không commit, push, merge/land.

## Evidence §7

```yaml
reviewed_sha: c47a439997e0191427d775636ebadbf3be7e1481
base_sha: 2531366e1abc6cbca0a6c2765e40e54be38d1fb7
verdict: approve
tests:
  - id: step_0
    result: "pass: exact HEAD/base; shallow=false; only CLAUDE.md; 2 insertions, 2 deletions"
  - id: pr104_identity_and_version
    result: "pass: e344e7c is Merge pull request #104; VERSION=1.36.68"
  - id: pr104_gate_semantics
    result: "pass: three attack names rc 0->4; ducthangho rc 0->0; exact PR tree 27/27"
  - id: forbidden_replacement_check
    result: "pass: scanner 1a4525a has 28 entries; replacement absent and contains no entry"
  - id: scanned_corpus_both_shapes
    result: "pass: base across-whitespace=1/one-line=0; head=0/0; one target file"
  - id: reflow_same_phrase
    result: "control rejects as expected: rc=6"
  - id: exemption_free_rewrite
    result: "pass: rc=0"
  - id: ac19_prototype
    result: "pass: a07e9d5 rc=0, 9/9; reviewed tree exempt lines=0, errors=[]"
  - id: current_doctrine_scanner
    result: "pass: rc=0; files=1; hits=0"
  - id: eol_policy
    result: "pass: rc=0; checked=308; violations=[]"
  - id: doc_claims_strict
    result: "pass: rc=0; files_scanned=91; flags=[]"
  - id: golden_test
    result: "pass: rc=0; 20/20"
  - id: release_verify_worktree
    result: "expected boundary: rc=2; only extra=NHIEM_VU_VIET_LAI.md"
  - id: release_verify_exact_archive
    result: "pass: rc=0; checked=179; failed=0; extra=0; CLAUDE.md absent from manifest"
  - id: diff_check
    result: "pass: rc=0"
findings: []
land_recommendation: fast_forward
```
