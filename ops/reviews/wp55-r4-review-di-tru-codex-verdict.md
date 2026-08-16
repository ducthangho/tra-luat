# Verdict di trú AC 19 lên `master`

```yaml
verdict: changes_requested
reviewed_sha: 9a5b05cfd8804455dd785b8fe710736773dc78cf
base_sha: 2531366e1abc6cbca0a6c2765e40e54be38d1fb7
reviewer: codex
executor: claude
land_recommendation: do_not_land
```

**Không nên đưa commit hiện tại vào `master`.** Các gate đều đạt trên archive sạch, khối hiện tại đúng cú pháp của nguyên mẫu, và quy ước `nguồn` trỏ về commit cha là nhất quán. Tuy nhiên commit đang dùng một ngoại lệ rộng hơn mức cần thiết trong khi có cách sửa không cần ngoại lệ và không đụng cấu trúc Markdown. Hãy soạn lại commit trên đúng base, rồi review SHA mới. Nếu bản thay thế được duyệt, nên land bằng fast-forward để giữ nguyên SHA mới làm `base_sha`; không merge/squash commit `9a5b05c…`.

## Findings

### `ac19-exemption-wider-than-necessary` — P1

`disposition: must_replace_with_exemption_free_rewording`

Khối ở `9a5b05c…:CLAUDE.md` miễn dòng 77–86: 8 dòng thân cộng 2 marker. Cụm cần xử lý chỉ nằm ở dòng 83–84, nên 6/8 dòng thân không cần miễn vẫn được miễn. Đây là chi phí thật, trái mục tiêu “ngoại lệ HẸP” của AC 19 mới.

Có đường thứ ba tốt hơn: đổi đúng cách gọi trong câu đo, chẳng hạn `người có\n  thẩm quyền` thành `tên hợp lệ` hoặc `tên thuộc danh sách cho phép`. Câu vẫn nói đúng phép đo allowlist, nhưng không còn cụm doctrine, không cần khối chứng cứ, không đổi topology của danh sách và không phụ thuộc một định dạng `nguồn` còn ở trạng thái dự thảo. Đối chứng quan trọng: chỉ nối cụm thành một dòng **không** giải quyết được — scanner hiện hành trả `rc=6`; viết lại cụm trả `rc=0`.

Bằng chứng chạy được, toàn bộ nguồn neo SHA bất biến:

```bash
HEAD_SHA=9a5b05cfd8804455dd785b8fe710736773dc78cf
BASE_SHA=2531366e1abc6cbca0a6c2765e40e54be38d1fb7
PROTO_SHA=a07e9d51ffd5c4bd35b914b47fd4fc18f5871094
SCANNER_SHA=1a4525a20aa360476a6f59cb157c21097919c457

git show "$PROTO_SHA":ops/specs/wp55-r4-ac19-nguyen-mau.py > /tmp/proto-9a5b05c.py
python3 - "$HEAD_SHA" <<'PY'
import importlib.util, subprocess, sys
spec = importlib.util.spec_from_file_location("p", "/tmp/proto-9a5b05c.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
raw = subprocess.check_output(
    ["git", "show", f"{sys.argv[1]}:CLAUDE.md"], text=True, encoding="utf-8")
mien, loi = m.khoi_chung_cu(raw)
print(loi or "không lỗi", min(mien), max(mien), len(mien))
PY
# Đã đo: không lỗi 77 86 10

REFLOW_TREE=$(mktemp -d /tmp/review-9a5b05c-reflow-XXXXXX)
REWRITE_TREE=$(mktemp -d /tmp/review-9a5b05c-rewrite-XXXXXX)
git archive "$BASE_SHA" | tar -x -C "$REFLOW_TREE"
git archive "$BASE_SHA" | tar -x -C "$REWRITE_TREE"
perl -0pi -e 's/người có\n  thẩm quyền/người có thẩm quyền/' "$REFLOW_TREE/CLAUDE.md"
perl -0pi -e 's/người có\n  thẩm quyền/tên hợp lệ/' "$REWRITE_TREE/CLAUDE.md"
python3 <(git show "$SCANNER_SHA":.claude/dev/packet_loop.py) doctrine-scan --root "$REFLOW_TREE"
# Đã đo: rc=6, 1 hit tại CLAUDE.md:82
python3 <(git show "$SCANNER_SHA":.claude/dev/packet_loop.py) doctrine-scan --root "$REWRITE_TREE"
# Đã đo: rc=0, 1 tệp, 0 hit
```

## Hai quyết định thiết kế

### A — bọc trọn mục

Lập luận “không chèn comment vào giữa paragraph” là hợp lý, nhưng cái giá khai chưa đủ: hai HTML block không thụt nằm trước và sau một list item làm gián đoạn cấu trúc list bao quanh, còn vùng miễn trừ phủ thêm 6 dòng thân không liên quan. Tôi **không chạy được renderer CommonMark thật** trong môi trường này: không có `cmark`, Pandoc hay thư viện CommonMark Python/Node/Ruby; endpoint render ngoài môi trường cũng không truy cập được, và tôi không cài gói theo lệnh cấm của nhiệm vụ. Vì vậy tôi không dùng nhận định tĩnh về tight/loose hay số list node làm căn cứ finding. Finding đứng độc lập vì cách viết lại ở trên loại bỏ hoàn toàn cả thay đổi render lẫn ngoại lệ rộng.

### B — `nguồn` trỏ vị trí gốc

Quy ước này **không tự mâu thuẫn**. `2531366e1abc6cbca0a6c2765e40e54be38d1fb7` là commit cha của reviewed SHA, và:

```bash
git show 2531366e1abc6cbca0a6c2765e40e54be38d1fb7:CLAUDE.md | sed -n '82,83p'
```

trả đúng hai dòng chứa lời kể phép đo. Đây là citation về trạng thái tiền di trú, kiểm được và tránh vòng lặp hash nếu một commit phải tự ghi SHA của chính nó. Nếu cơ chế này vẫn có người dùng, spec nên chốt rõ `nguồn` là citation lịch sử và nên ưu tiên SHA 40 ký tự thay vì abbreviation 7 ký tự. Với sửa chữa được yêu cầu ở finding trên, khối này biến mất nên quyết định B không còn chặn commit thay thế.

## Gate và ranh giới review

- Bước 0: `HEAD=9a5b05cfd8804455dd785b8fe710736773dc78cf`; shallow=`false`; diff từ base đúng một tệp `CLAUDE.md`.
- Nguyên mẫu AC 19 tại `a07e9d51ffd5c4bd35b914b47fd4fc18f5871094`: rc=0; 9/9 ca; khối head không lỗi, miễn đúng 10 dòng 77–86; cụm nằm trọn trong vùng miễn.
- Nguyên mẫu **dễ dãi hơn một bản cài đặt hoàn chỉnh**: phép thử bổ sung cho thấy nó không báo orphan closer, nhận `khôngnguồn="…"` như thuộc tính `nguồn`, và nhận opener nằm trong fenced code. Khối của reviewed SHA không dựa vào ba khe này, nên đây là ranh giới/prototype debt, không phải finding thứ hai của commit.
- `eol_policy.py --all --json`: rc=0, `checked=308`, không vi phạm.
- `doc-claims-check --strict --json`: rc=0, `ok=true`, `flags=[]` (358 advisory lịch sử, không flag).
- `golden-test`: rc=0, `ok=true`, 20/20 ca.
- `release-verify` trong worktree: rc=2 chỉ vì `NHIEM_VU_DI_TRU.md` là extra. Trên `git archive` của reviewed SHA: rc=0, `checked=179`, `failed=[]`, `extra=[]`; `CLAUDE.md in manifest: false`; package hash khớp.
- Scanner hiện hành lấy từ `1a4525a20aa360476a6f59cb157c21097919c457`: rc=0 trên reviewed tree, quét 1 tệp, 0 hit.
- `git diff --check BASE HEAD`: rc=0.
- Không chạy được renderer CommonMark thật như đã nêu ở mục A. Không chạy `pip install`; không chạy thao tác ghi ngoài các thư mục `/tmp`; không commit, push, merge hay land.

## Evidence §7

```yaml
reviewed_sha: 9a5b05cfd8804455dd785b8fe710736773dc78cf
base_sha: 2531366e1abc6cbca0a6c2765e40e54be38d1fb7
verdict: changes_requested
tests:
  step_0: "pass: exact HEAD, non-shallow, diff only CLAUDE.md"
  ac19_prototype: "pass: rc=0; 9/9; exempt lines 77-86 (10 lines); phrase fully inside"
  reflow_same_phrase: "fail as alternative: current scanner rc=6"
  exemption_free_reword: "pass: current scanner rc=0"
  eol_policy: "pass: rc=0; checked=308; violations=[]"
  doc_claims_strict: "pass: rc=0; flags=[]"
  release_verify_worktree: "expected boundary: rc=2; extra=NHIEM_VU_DI_TRU.md"
  release_verify_archive: "pass: rc=0; checked=179; failed=0; extra=0"
  claude_manifest_membership: "pass: absent from 179 manifest entries"
  golden_test: "pass: rc=0; 20/20"
  current_packet_scanner: "pass: rc=0; 1 file; 0 hits"
  diff_check: "pass: rc=0"
  commonmark_renderer: "not_run: no renderer installed and external endpoint unavailable"
findings:
  - finding_id: ac19-exemption-wider-than-necessary
    severity: P1
    disposition: must_replace_with_exemption_free_rewording
land_recommendation: do_not_land
```
