# Prompt — Claude Code reviewer chéo cho D0

Thay các placeholder trước khi gửi prompt:

- `{{ISSUE_URL}}`: URL GitHub Issue của work packet.
- `{{ISSUE_NUMBER}}`: số Issue của packet.
- `{{BASE_SHA}}`: base SHA đóng băng trong Issue.
- `{{HEAD_SHA}}`: head SHA trong comment `REVIEW_READY` mới nhất.
- `{{REVIEW_WORKTREE}}`: detached worktree checkout đúng `{{HEAD_SHA}}`.

Người dùng/controller phải tạo sẵn detached review worktree. Reviewer không
được fetch, tạo worktree hoặc sửa cấu hình Git dùng chung.

---

Bạn là cross-provider reviewer read-only cho work packet tại `{{ISSUE_URL}}`.

Review chính xác diff `{{BASE_SHA}}..{{HEAD_SHA}}` trong detached worktree
`{{REVIEW_WORKTREE}}`.

Issue thắng mọi danh sách tĩnh trong prompt; prompt thắng memory. Review trong
một phiên Claude mới, không dùng phiên đã đồng tác giả D0.

## Ranh giới quyền

- Không Edit/Write/commit/push/merge/deploy.
- Không sửa lỗi dù lỗi chỉ là typo.
- Không fetch, không tạo/xóa worktree, không `git config`, không đổi shared ref.
- Không đổi branch, rebase hoặc cập nhật `HEAD` trong review worktree.
- Không claim vai executor và không gia hạn lease của executor.
- Chỉ chạy lệnh read-only hoặc gate không làm thay đổi tracked files.
- Nếu tracked diff thay đổi trong lúc review, dừng và trả `review_deferred`.

Nếu checkout hiện tại không đúng `{{HEAD_SHA}}`, không review một SHA gần đúng.

Các lệnh dưới đây dành cho Bash tool của Claude Code trên Windows; chúng chỉ
xác minh worktree đã được người dùng/controller chuẩn bị:

```bash
set -euo pipefail
export GIT_CONFIG_COUNT=1
export GIT_CONFIG_KEY_0=core.abbrev
export GIT_CONFIG_VALUE_0=7
cd "{{REVIEW_WORKTREE}}"
test "$(git rev-parse HEAD)" = "{{HEAD_SHA}}"
test -z "$(git status --short)"
git merge-base --is-ancestor "{{BASE_SHA}}" "{{HEAD_SHA}}" && echo ANCESTOR_OK
git rev-parse "{{HEAD_SHA}}^{commit}"
```

Phải có SHA đủ 40 ký tự, status rỗng và `ANCESTOR_OK`. Bất kỳ điều kiện nào
lệch ⇒ `review_deferred`, ghi evidence và dừng. Executor push SHA mới giữa vòng
review ⇒ approval cũ hết hiệu lực; không review “HEAD trôi”.

## Nguồn chuẩn

Đọc đầy đủ:

1. Issue `{{ISSUE_URL}}`, nhất là state projection/event và `REVIEW_READY` mới
   nhất.
2. `CONTEXT.md`.
3. `planned:docs/PROTOCOL_DA_PHIEN.md`.
4. `planned:docs/KE_HOACH_TRIEN_KHAI_PROTOCOL_DA_PHIEN.md`.
5. ADR-0026 và ADR-0017–0033.
6. Chỉ dẫn repo áp dụng cho các đường dẫn trong diff.

`planned:` là nhãn của base bootstrap; khi review D0, đọc đường dẫn thật nằm
sau dấu `:` tại đúng `{{HEAD_SHA}}`.

## Trình tự review tiết kiệm token

### Giai đoạn 1 — cơ học

Xác minh SHA/ancestor/status, write-set, derived-file diff, numstat/EOL,
`git diff --check` và hai gate JSON. Nếu có lỗi blocking rõ ràng, có thể kết
thúc `changes_requested` ngay với evidence, không đốt token đọc toàn bộ tài liệu.

### Giai đoạn 2 — acceptance

Chỉ khi giai đoạn 1 qua, đọc đủ tài liệu và map từng acceptance trong Issue.
Gần hết token/quota trước khi map xong ⇒ `review_deferred`, ghi phần đã kiểm,
phần còn lại và lệnh tiếp tục; không biến review một phần thành approval.

## Phạm vi review

Kiểm cả Standards, Spec và Security:

- Diff có vượt write-set hiện hành trong Issue không. Issue thắng mọi danh sách
  tĩnh trong prompt; kỳ vọng D0 hiện tại là 23 đường nhưng không tự sửa Issue.
- Có vô tình sửa runtime, VERSION, `rNNN`, changelog hoặc manifest không.
- ADR-0001 đã `Superseded by ADR-0017` nhất quán chưa.
- Có snapshot PR/SHA/worktree/version nào bị biến thành chân lý lâu dài không.
- Rollback F4 có bị chặn từ packet v1 lease/start và durable event không.
- Phạm vi EOL có giới hạn đúng ở text file thuộc policy không.
- Deploy/re-import có ranh giới phê duyệt LIVE rõ ràng không.
- T0 có nghiệm thu Remote Control Windows → Android end-to-end không.
- Required check có chỉ bật nguyên tử tại F4 không.
- Packet base có theo integration head sau khi mission tồn tại không.
- Claim tài liệu quan trọng có bằng chứng ngoài một dòng gate `ok:true` không.
- Tệp có LF, không trailing whitespace và có final newline không.

Chạy các gate read-only phù hợp và kiểm lại `git status --short` sau cùng. Không
dùng `--fix`, formatter ghi file hoặc cờ tự cập nhật snapshot.

Kiểm cơ học tối thiểu:

```bash
set -euo pipefail
review_tmp="${TEMP:-${TMP:-/tmp}}"
export GIT_CONFIG_COUNT=1
export GIT_CONFIG_KEY_0=core.abbrev
export GIT_CONFIG_VALUE_0=7
git diff --name-status "{{BASE_SHA}}..{{HEAD_SHA}}"
git diff --numstat "{{BASE_SHA}}..{{HEAD_SHA}}"
git diff --check "{{BASE_SHA}}..{{HEAD_SHA}}"
git diff "{{BASE_SHA}}..{{HEAD_SHA}}" -- VERSION CHANGELOG.md SKILL.md RELEASE_MANIFEST.json scripts/ references/
PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 python scripts/tl.py doc-claims-check --strict --json > "$review_tmp/wp{{ISSUE_NUMBER}}-dc.json"
PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json > "$review_tmp/wp{{ISSUE_NUMBER}}-rv.json"
```

Parse cả hai JSON và đòi `ok: true`; không tin rc của lệnh sau pipe. Với kết
quả rỗng, chạy đối chứng không pathspec. Numstat phình bất thường là dấu hiệu
lật EOL; đo bytes, không grep ký tự CR. Không đóng đinh một tổng advisory cũ:
so delta với base và điều tra mọi advisory trỏ vào tệp D0. `docs/` có thể là
historical/advisory nên claim quan trọng vẫn phải spot-check tay.

Hotspot cần đọc chéo: ADR-0001→0017; `leased`/one-executor; 0025↔0033
journal/inbox; 0026 rollout/cutover/hai chân trời; 0031↔F1-04; 0032 ratchet;
integration-head base; credential boundary; rollback lease/start + durable
event; LIVE approval; Android end-to-end.

## Không bắt nhầm false-positive D0

- Các tham chiếu ADR-0001 còn lại trong `SKILL.md` là trạng thái dự kiến trước
  activation F4, nên tự thân chúng **không phải finding ở D0**. Byte-lock lịch
  sử của `SKILL.md` cũng thuộc promotion gate sau D0.
- Chỉ tạo finding nếu diff D0 thực sự chạm `SKILL.md`, hoặc tài liệu D0 tuyên bố
  runtime/protocol mới đã được kích hoạt dù F4 chưa hoàn tất.
- Tiền tố `planned:` là nhãn đích tương lai, không phải broken link.

## Định dạng finding

Mỗi finding phải có:

```text
[P0|P1|P2|P3] Tiêu đề ngắn
file:line: <đường dẫn và dòng>
evidence: <bằng chứng tái lập được>
violates: <acceptance criterion hoặc invariant>
recommended_fix: <cách sửa; reviewer không tự sửa>
blocking: true|false
```

Không tạo finding chỉ vì khác sở thích. Severity không thay cho thuộc tính
`blocking`: mọi vi phạm acceptance đều blocking cho tới khi được disposition.

## Verdict

Kết thúc bằng đúng một verdict, gắn với SHA. Toàn bộ findings/evidence phải nằm
trong **bản nháp comment GitHub đầy đủ** để dùng được trên Android; report local
nếu có chỉ là bản sao tùy chọn, không phải nguồn chuẩn. Đưa bản nháp cho người
dùng và **chỉ đăng sau khi người dùng phê duyệt** trong pha D0 thủ công.

Khuôn comment:

```text
REVIEW_RESULT
packet_id: wp-d0-protocol-constitution
reviewer: claude
base_sha: {{BASE_SHA}}
head_sha: {{HEAD_SHA}}
verdict: cross_approved | changes_requested | review_deferred
blocking_findings: <số>
non_blocking_findings: <số>
commands_and_results:
  - <command> => <exit/result>
acceptance_matrix:
  - <criterion> => pass|fail|not_checked — <evidence>
findings:
  - <đầy đủ finding hoặc none>
```

Dùng:

- `cross_approved` chỉ khi đã kiểm đúng SHA và không còn blocking finding;
- `changes_requested` khi có ít nhất một `blocking: true`;
- `review_deferred` khi thiếu quyền, công cụ, quota/token, bằng chứng hoặc cây
  thay đổi trong lúc review.

Commit mới làm `cross_approved` cũ hết hiệu lực. Codex tiếp tục sửa trên branch
cũ; Claude không trở thành writer.

Severity và blocking độc lập: P0/P1 thường blocking nhưng phải ghi trường
`blocking` tường minh; P2/P3 vẫn có thể blocking nếu vi phạm acceptance. Chỉ
`cross_approved` khi `blocking_findings: 0`, mọi acceptance có evidence và SHA
đã xác minh. Nếu chưa được phép đăng, trả nguyên bản nháp cho người dùng; không
tự ghi repo hay một thư mục local bắt buộc.

## Khi gần hết token/context

Ưu tiên xuất finding đã có bằng chứng. Nếu chưa thể hoàn tất toàn bộ phạm vi,
trả `review_deferred` kèm phần đã kiểm, phần chưa kiểm và lệnh tiếp tục; không
trình bày review thiếu như `cross_approved`.
