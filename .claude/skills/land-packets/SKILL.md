---
name: land-packets
description: Client do NGƯỜI gọi để chuẩn bị land các packet của một mission (tra-luat) trên nền Claude Code. Chỉ chứa cú pháp và công cụ của nền; mọi quy tắc land, điều kiện uỷ quyền và tiêu chí hoàn tất nằm ở docs/PROTOCOL_DA_PHIEN.md.
argument-hint: "[so-issue-mission]"
disable-model-invocation: true
---

# Adapter `land-packets` — Claude Code

**Skill này KHÔNG tự trigger.** `disable-model-invocation: true` ở frontmatter là cách nền này cưỡng
chế điều §13 quy định — đừng gỡ.

**Đọc trước:** `docs/PROTOCOL_DA_PHIEN.md` §13 (nội dung `land prepare`, ranh giới `--apply`, deploy
là cổng riêng) · §8 (mức review được chấp nhận) · §10.2 (các thuật ngữ trạng thái, không dùng thay
nhau) · §12 (khi nào mission được đóng) · §13.1–§13.2 (fence, hạn quyền và ruleset)
· §7 (receipt vận chuyển). Quy ước deploy của kho: `CLAUDE.md`.

Tệp này **không tóm tắt** những mục trên. Chốt cơ học:

```bash
PY="$(command -v python3 || command -v python || command -v py)"   # CLAUDE.md: nhận CẢ BA tên
"$PY"  .claude/dev/packet_loop.py doctrine-scan --root .
```

Dưới đây chỉ có cú pháp của nền.

Admission trước heavy gate: dùng mục “Gate” của [work-packet](../work-packet/SKILL.md)
với runtime Linux đã probe; nhánh native Windows/handoff ở protocol §10.2.1 và
[adapter PowerShell](../../../.agents/skills/work-packet/SKILL.md). Diff/numstat và consumer
model dùng SOURCE/SCRATCH của đúng run theo [cross-review](../cross-review/SKILL.md).

## `land prepare` — mặc định, DRY

```bash
gh issue view 54 --json labels,title
gh issue list --state open --label coord:packet --json number,labels
gh pr list --state open --json number,headRefName,headRefOid,statusCheckRollup
git -C "$WORKTREE" log --oneline "origin/master..$BRANCH"
# Cú pháp gate chọn theo Packet và protocol §10.1/§10.2; /gate khi được cấp.
```

Báo cáo ra **số**, không ra cảm nhận: hai số bằng nhau, `"ok": true`, `0 failed / 0 extra`, hai lượt
bundle cùng SHA-256. Ngưỡng cụ thể của từng gate nằm ở `CLAUDE.md` và ở chính đầu ra của lệnh.

## `--apply` và deploy — KHÔNG thực thi từ đây

Trước mọi thao tác trong nhóm này:

```bash
PY="$(command -v python3 || command -v python || command -v py)"   # CLAUDE.md: nhận CẢ BA tên
"$PY"  .claude/dev/packet_loop.py guard --action merge     # hoặc deploy | live
```

Lệnh này không có cờ nới, và không được thêm. Uỷ quyền cho một exact head SHA sống trên GitHub, không
sống trong ngữ cảnh phiên — đọc §13 để biết cái gì được coi là uỷ quyền hợp lệ.

## Mốc Workflow definition khi phiên không gọi được GraphQL

Phiên Claude Code trên web nhận 403 cho GraphQL, nên `WorkflowRun.file` phải do chủ kho chạy rồi dán output.
Cú pháp lệnh đưa cho chủ kho và cách đối chiếu: mục *"Lệnh `gh api graphql` đưa cho chủ kho chạy"* của `CLAUDE.md`.
Đọc mục ấy từ `origin/master` ngay trước khi soạn lệnh — phiên mở từ trước có thể đang giữ bản cũ.

## Full ref fence và merge evidence

Protocol §5.1/§13.1 quy định phạm vi so sánh. `$SCRATCH` là thư mục ngoài checkout;
ví dụ Bash lưu toàn bộ response, không lọc `--heads`:

```bash
git ls-remote origin > "$SCRATCH/refs-new.raw"
LC_ALL=C sort "$SCRATCH/refs-new.raw" > "$SCRATCH/refs-new.sorted"
diff -u "$SCRATCH/refs-old.sorted" "$SCRATCH/refs-new.sorted"
git show -s --format='%H %P %T' "$MERGE_OID"
```

Ghi rc ngay sau từng lệnh (hoặc chạy từng lệnh riêng); `diff` rc 1 là có khác biệt,
rc lớn hơn 1 là lỗi đọc/so. Script Python sau in delta `ref / old / new` từ hai response
UTF-8 của `ls-remote` đã đọc thành công; hash là SHA-256 của các dòng `OID<TAB>ref<LF>`
sắp xếp theo ref (Unicode code point). Dùng cùng script từ adapter Codex:

```python
import hashlib
from pathlib import Path
import re
import sys

def refs(path):
    result = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        oid, ref = line.split("\t")
        if not re.fullmatch(r"[0-9a-f]{40}", oid) or ref in result:
            raise ValueError("invalid or duplicate ref")
        result[ref] = oid
    if not result:
        raise ValueError("empty remote response")
    raw = "".join(f"{result[r]}\t{r}\n" for r in sorted(result)).encode("utf-8")
    print("REFS", len(result), hashlib.sha256(raw).hexdigest())
    return result

before, after = map(refs, sys.argv[1:])
changed = sorted(r for r in before.keys() | after.keys() if before.get(r) != after.get(r))
for ref in changed:
    print(ref, before.get(ref, "ABSENT"), after.get(ref, "ABSENT"), sep="\t")
raise SystemExit(1 if changed else 0)
```

## Ruleset snapshot và payload ngoài checkout

Phạm vi authority/readback/race: protocol §13.2. Ví dụ chỉ đọc snapshot bằng
`gh api "repos/ducthangho/tra-luat/rulesets/$RULESET_ID" > "$SCRATCH/ruleset-before.json"`.
Đối chiếu [writable fields của API](https://docs.github.com/en/rest/repos/rules#update-a-repository-ruleset)
trước khi dựng payload; không có lệnh mutation trong ví dụ. Python trên snapshot vô hại:

```python
import json
from pathlib import Path
import sys

source = json.loads(Path(sys.argv[1]).read_bytes())
writable = ("name", "target", "enforcement", "bypass_actors", "conditions", "rules")
if any(key not in source for key in writable):
    raise SystemExit("snapshot incomplete for this branch/tag example")
payload = {key: source[key] for key in writable}
Path(sys.argv[2]).write_bytes((json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
```

Ví dụ giữ nguyên nested `rules`/`integration_id`; chưa tạo thay đổi. Nó chỉ chiếu sáu trường
cho shape branch/tag trên, không là validator mọi loại ruleset. Trường mới/shape khác cần
đối chiếu contract (§13.2). Readback CI/provenance dùng ví dụ “Provenance CI” của
`.claude/skills/cross-review/SKILL.md`; comment dùng “Body file và exact readback” của
`.claude/skills/work-packet/SKILL.md`. Trạng thái báo cáo theo protocol §10.2.4.
