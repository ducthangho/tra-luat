---
name: work-packet
description: Thực thi MỘT work packet của protocol đa phiên (tra-luat) trên nền Claude Code. Chỉ chứa cú pháp và công cụ của nền; mọi quy tắc, schema và tiêu chí hoàn tất nằm ở docs/PROTOCOL_DA_PHIEN.md.
argument-hint: "[so-issue-packet]"
---

# Adapter `work-packet` — Claude Code

**Đọc trước, không làm theo trí nhớ:** `docs/PROTOCOL_DA_PHIEN.md` §13 (trình tự bắt buộc, điều kiện
từ chối việc, định nghĩa hoàn tất) · §3.2 (schema packet) · §5 (write set) · §7 (handoff) ·
§12 (điều kiện dừng) · §3.2.1 (spec nguồn và ba mốc Git) · §10.2.1–§10.2.3
(preflight, provenance và evidence thiếu). Quy trình sửa code của kho: `CLAUDE.md`.

Bảng lớp, cách đọc kết quả vá và phần chưa đo: protocol §8.3; công thức tỷ lệ,
lớp tái diễn và checkpoint: §12. Gợi ý reviewer và `hint_provenance`: §7/§8.

Tệp này **không tóm tắt** những mục trên. Tóm tắt là bản sao, và bản sao thì trôi lệch — ba lượt
review liên tiếp đã bắt được đúng lỗi đó ở chính adapter này. Nay có chốt cơ học:

```bash
PY="$(command -v python3 || command -v python || command -v py)"   # CLAUDE.md: nhận CẢ BA tên
"$PY" .claude/dev/packet_loop.py doctrine-scan --root . \
  --path .agents/skills/work-packet/SKILL.md \
  --path .agents/skills/cross-review/SKILL.md \
  --path .agents/skills/land-packets/SKILL.md
```

Dưới đây chỉ có cú pháp của nền.

## Lấy spec

```bash
gh api graphql -f query='{repository(owner:"ducthangho",name:"tra-luat"){issue(number:55){body}}}'
```

`gh issue view 55 --json body --jq .body` cũng lấy body; `-q` riêng không chọn JSON output.
Công thức `spec_hash` và nguồn blob: protocol §3.2.1. Ví dụ lưu bytes blob ra scratch bằng
Python (các biến Bash dưới đây do phiên điền từ assignment, không chạy nguyên placeholder):

```bash
PY="$(command -v python3 || command -v python || command -v py)"
"$PY" -c 'import hashlib,pathlib,subprocess,sys; b=subprocess.run(["git","show",sys.argv[1]+":"+sys.argv[2]],check=True,capture_output=True).stdout; pathlib.Path(sys.argv[3]).write_bytes(b); print(hashlib.sha256(b).hexdigest())' "$SPEC_OID" "$SPEC_PATH" "$SCRATCH/spec.md"
```

## Dựng worktree

```bash
git rev-parse --is-shallow-repository        # đòi false trước khi tin bất kỳ phép so lịch sử nào
git config core.autocrlf false && git config core.eol lf && git config core.abbrev 7
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPYCACHEPREFIX="$SCRATCH/pycache"
```

## Công cụ — nhánh packet KHÔNG mang công cụ của kho

`base_sha` thường cũ hơn công cụ trên nhánh chính, nên cây làm việc của packet có thể
thiếu cả bộ dựng công cụ lẫn hook phiên, và `settings.json` bản cũ có thể chưa đăng ký
`SessionStart`. Kho gắn giữa phiên thì hook cũng không chạy. Ba chuyện độc lập, mỗi
chuyện một mình đã đủ để phiên mở ra mà không có `codex`/`rg`.

Lấy công cụ TỪ NHÁNH CHÍNH, đừng chạy cả hook phiên chỉ để lấy một thứ — hook có bước
cài phụ thuộc Python và đã đo được một lần làm hỏng môi trường đang tốt:

```bash
PY="$(command -v python3 || command -v python || command -v py)"
"$PY" "$CANON/.claude/dev/launcher.py" doctor
```

**Vắng mặt là một QUAN SÁT; "môi trường không có" là một KẾT LUẬN.** Trước khi báo với
người điều phối rằng không gọi được một CLI, phải chạy `command -v <tool>` và
`<tool> login status` trong CHÍNH phiên này, rồi loại trừ xong hai khả năng còn lại: hook
chưa chạy, và nhánh đang checkout không mang hook. Tài liệu mô tả một lần đo trong quá
khứ trên một cây khác — nó không phải quan sát về phiên đang chạy. Đã trả giá:
một phiên báo cross-review không chạy được, trong khi CLI cài được và lượt review sau đó
tìm ra một P1 thật.

Kiểm biến bí mật bằng **sự tồn tại**, không bao giờ in nội dung — biến khôi phục đăng
nhập chứa refresh token, in một lần là phải thu hồi và cấp lại:

```bash
if [ -n "${TEN_BIEN:-}" ]; then echo "có, ${#TEN_BIEN} ký tự"; else echo "chưa đặt"; fi
```

Đừng nối `${VAR:+…}` với `${VAR:-…}` trong cùng một chuỗi: `:-` chỉ thay thế khi biến
**rỗng hoặc chưa đặt**, nên ở nhánh "đã đặt" — nhánh người ta thật sự chạy — nó bung ra
**chính giá trị**. Bản trước của dòng này in `có, 27 ký tự` rồi in luôn cả token.

## Gate

Chọn lệnh theo protocol §10.1/§10.2 và Packet: `/gate-targeted` hoặc `/gate` khi scope cho phép.
`$CANON` là checkout mã canonical đã ghim, `$S` là OID của nó, `$H` là candidate có trong
object store của `$CANON`; `$SCRATCH` ở ngoài checkout. Ví dụ Bash, giữ rc cả khi bật `set -e`:

Admission này cần Linux/POSIX; Git Bash với Python native Windows không đáp ứng bộ giải
Git `/usr/bin:/bin` của checker. Nhánh không hỗ trợ và handoff theo §10.2.1. Khi dùng WSL
được cấp, probe trong distribution đã chọn; `$CANON` là clone Linux đọc được object store
(không giả định linked worktree Windows dùng được trong WSL). Bootstrap chuẩn bị clone tại
`$S`, có object `$H`; không fetch/checkout cây nguồn từ đoạn dưới.

Lưu khối sau thành `$ADMISSION_SCRIPT` ngoài checkout, chạy bằng
`bash "$ADMISSION_SCRIPT" "$CANON" "$S" "$H" "$SCRATCH"`. Bốn đối số là đường dẫn/OID
đã xác minh, không dùng đường dẫn Windows trong shell Linux:

```bash
set -eu
CANON="$1"; S="$2"; H="$3"; SCRATCH="$4"
PY="$(command -v python3 || command -v python || command -v py)"
"$PY" -B -c 'import os,shutil,sys; print(sys.executable,sys.version); g=shutil.which("git",path="/usr/bin:/bin"); print("admission git",g); sys.exit(0 if os.name=="posix" and g else "unsupported admission runtime")'
/usr/bin/git --version
"$PY" -B -c 'import yaml; print("PyYAML",yaml.__version__)'
bash --version
test "$(git -C "$CANON" rev-parse HEAD)" = "$S"
"$PY" -B -c 'import hashlib,pathlib,subprocess,sys; r,s=sys.argv[1:]; b=subprocess.run(["git","-C",r,"show",s+":ops/lease_publish.py"],check=True,capture_output=True).stdout; p=pathlib.Path(r)/"ops/lease_publish.py"; assert p.read_bytes()==b, "canonical checker bytes differ"; print("CANONICAL_CHECKER",s,hashlib.sha256(b).hexdigest())' "$CANON" "$S"
ANCESTRY_RC=0
git -C "$CANON" merge-base --is-ancestor "$S" "$H" || ANCESTRY_RC=$?
printf 'ancestor rc=%s\n' "$ANCESTRY_RC"
case "$ANCESTRY_RC" in 0) ;; 1) exit 1 ;; *) exit "$ANCESTRY_RC" ;; esac
ADMISSION_RC=0
"$PY" -B "$CANON/ops/lease_publish.py" kiem-thu-hoi-github "$H" \
  --root "$CANON" --canonical-base "$S" --nhanh-mac-dinh master \
  --receipt "$SCRATCH/local-admission.json" || ADMISSION_RC=$?
printf 'local admission rc=%s\n' "$ADMISSION_RC"
test "$ADMISSION_RC" -eq 0 || exit "$ADMISSION_RC"
git -C "$CANON" show -s --format=%B "$H" > "$SCRATCH/candidate-message.txt"
```

Đọc output/receipt theo §10.2.1; ví dụ không tạo receipt workflow. Đo dependency trong runtime
đích bằng `git --version`, `"$PY" --version`, import các module command dùng, `jq --version`,
`actionlint -version` và phiên bản shell. Tập cần probe lấy từ command thật (§10.2.1).

### Ba chỗ làm cổng ĐỎ vì NƠI CHẠY, không vì mã — đo 21→24-09-2026

Cả ba đều cho một cổng đỏ trông y hệt lỗi thật. Đo trước khi đi săn:

| triệu chứng | nguyên nhân | phép đo |
|---|---|---|
| `doc-claims-check --strict` `rc=2`, cờ `SHA_NOT_A_COMMIT` trên các tiền tố 8 ký tự | `core.abbrev` của git tự nới theo số object của kho; `ci.yml` ghim **7** | cùng một cây: abbrev 8 → `rc=2`; `git config core.abbrev 7` → `rc=0`, `flags 0` |
| `packet_loop_test.py` đỏ SÁU ca (suite `rc=1`; năm ca in `rc=14` của tiến trình con kèm `ly_do_dung: workspace la git worktree`, một ca `AssertionError` rỗng) | `.git` ở toplevel là TỆP: `git worktree` LIÊN KẾT, submodule, hoặc clone `--separate-git-dir` (launcher gọi cả ba là "git worktree") | đúng tiêu chí `_probe_workspace` của launcher: `[ -f "$(git rev-parse --show-toplevel)/.git" ]` ⇒ `.git` là TỆP; đừng so chuỗi `--git-dir` với `--git-common-dir` (thư mục con của clone thường: một bên tuyệt đối, một bên tương đối ⇒ báo nhầm; submodule hay `--separate-git-dir`: hai chuỗi BẰNG nhau ⇒ bỏ sót). Dựng clone thường (`.git` là THƯ MỤC) rồi đo lại |
| `ops/cong_cu.py kiem-tra` `rc=2` và `cong_cu_test.py` `rc=1` khi chạy trọn bán kính đột biến (đích T2 BỎ QUA ⇒ `KHÔNG_ĐO_ĐƯỢC`); với `CONG_CU_TEST_BAN_KINH=manh` (có từ #668) chỉ còn `bỏ qua=1`, `rc=0` | thiếu một công cụ trong bản kê (đo được: `jsonschema` `trang_thai: DO`) | đọc `trang_thai` TỪNG mục trong JSON, đừng dừng ở `trang_thai_tong` |

Hai nếp git mà `ci.yml` đặt trước checkout và bộ chạy cục bộ phải đặt lại: `core.autocrlf=false`
cùng `core.eol=lf` (RELEASE_MANIFEST băm theo LF), và `core.abbrev=7` ở trên. Thiếu chúng thì cổng
nói thật — chỉ là nói về cây của bạn, không về bản vá.

## Cú pháp máy trạng thái

Chọn đường điều phối theo protocol §3/§4 và authority của Packet; bảng lệnh này mô tả runtime
hiện có, không thay một ngoại lệ được cấp riêng bằng việc ghi tay state.

```bash
PY="$(command -v python3 || command -v python || command -v py)"   # CLAUDE.md: nhận CẢ BA tên
"$PY"  .claude/dev/packet_loop.py init          --packet 55 --mission 54 \
                                                --executor claude --reviewer codex
# `init` CHỈ tới `awaiting_lease`. Uỷ quyền là bước RIÊNG, và người cấp KHÔNG được
# là tên một provider — agent không tự cấp lease cho chính mình.
"$PY"  .claude/dev/packet_loop.py record-lease  --packet 55 \
                                --lease-id wp55-r2-review-2-codex-20260813 \
                                --granted-by ducthangho \
                                --evidence https://github.com/o/r/issues/55#issuecomment-5281636040 \
                                --expires-utc 2026-08-13T18:30:00Z
"$PY"  .claude/dev/packet_loop.py begin-attempt --packet 55 --provider claude
"$PY"  .claude/dev/packet_loop.py next-comment  --packet 55        # in văn bản → ĐĂNG lên Issue
"$PY"  .claude/dev/packet_loop.py record-post   --packet 55 --for reviewing --comment-id 5258163128
"$PY"  .claude/dev/packet_loop.py transition    --packet 55 --to reviewing --comment-id 5258163128 \
                                                --head-sha $(git rev-parse HEAD)
"$PY"  .claude/dev/packet_loop.py void-attempt  --packet 55 --reason quota
"$PY"  .claude/dev/packet_loop.py status        --packet 55
"$PY"  .claude/dev/packet_loop.py where
```

**Lease không tự có.** `init` chỉ khai *hình dạng* của packet và dừng ở `awaiting_lease`; `leased`
chỉ đạt được qua `record-lease`, và lệnh đó chỉ **ghi hộ** một quyết định đã có ở nơi khác — nó đòi
người cấp (không được là `claude`/`codex`), dấu vết bền để đối chiếu, và hạn. Hạn được cưỡng chế
**cả lúc ghi lẫn mỗi lần mở lượt**: lease hết hạn thì `begin-attempt` thoát 8. Bản trước ghi thẳng
`leased` ngay trong `init`, nên ai gõ được `init` là tự có lease — review cross-provider tái hiện
bằng `init --packet 999999 --mission 888888` rồi `begin-attempt`, cả hai `rc=0`.

`--comment-id` là **ID GitHub trả về lúc đăng**, không phải URL. Ghi sổ bằng `record-post` trước, rồi
`transition` mới tiêu thụ được; mỗi ID dùng đúng một lần cho đúng một chuyển động. Tiến trình này
không gọi mạng nên **không xác minh** ID có thật — đọc `--help` để thấy nó bảo đảm đúng những gì.

Vào `reviewing` phải khai `--head-sha` là **exact head** đưa ra review. Bản duyệt sau đó phải neo
đúng SHA ấy, và mở lượt mới sẽ xoá mỏ neo — nên có commit mới thì bản duyệt cũ hết hiệu lực.

`--help` cho danh sách đầy đủ và ý nghĩa từng mã thoát. Mã thoát khác 0 ⇒ dừng và báo người; script
tự nói lý do trên stderr.

## Chặn cứng

```bash
PY="$(command -v python3 || command -v python || command -v py)"   # CLAUDE.md: nhận CẢ BA tên
"$PY"  .claude/dev/packet_loop.py guard --action merge
# merge | deploy | live | secrets | force-push | delete-branch | delete-worktree | edit-other-spec
```

Lệnh này không có cờ nới, và không được thêm.

## Đăng heartbeat

```bash
gh issue comment 55 --body-file heartbeat.md
```

Nhịp và nội dung tối thiểu do lease của đợt khai; đọc chính comment cấp lease, đừng nhớ theo lần trước.

### Body file và exact readback

Theo protocol §7, khi có quyền đăng Issue comment, lưu ví dụ Python dưới thành
`$SCRATCH/post_comment.py`; gọi bằng `"$PY" "$SCRATCH/post_comment.py" 55 "$SCRATCH/heartbeat.md" "$SCRATCH"`.
`-F body=@...` là cú pháp đọc file của [gh api](https://cli.github.com/manual/gh_api).
Ví dụ chỉ hỗ trợ Issue comment của kho này; review PR dùng endpoint của review.

```python
import hashlib
import json
from pathlib import Path
import subprocess
import sys

issue, body_file, out_dir = sys.argv[1:]
if not issue.isdecimal() or int(issue) < 1:
    raise SystemExit("invalid issue")
out = Path(out_dir)
body_path = Path(body_file).resolve()
body = body_path.read_bytes()
body.decode("utf-8")
repo = "repos/ducthangho/tra-luat"

def api(args, filename):
    result = subprocess.run(["gh", "api", *args], capture_output=True)
    (out / filename).write_bytes(result.stdout)
    print(filename, "rc=", result.returncode)
    result.check_returncode()
    return json.loads(result.stdout)

posted = api(["--method", "POST", f"{repo}/issues/{issue}/comments",
              "-F", "body=@" + str(body_path)], "posted.json")
comment_id = posted["id"]
if type(comment_id) is not int or comment_id < 1:
    raise SystemExit("invalid comment ID; inspect posted.json before retry")
readback = api([f"{repo}/issues/comments/{comment_id}"], "readback.json")
actual = readback["body"].encode("utf-8")
if readback["id"] != comment_id or actual != body:
    raise SystemExit("readback mismatch; preserve both responses")
print("COMMENT_READBACK", comment_id, hashlib.sha256(body).hexdigest())
```

## Đọc log CI

```bash
gh api repos/ducthangho/tra-luat/actions/jobs/<id>/logs
```

Identity/attempt/provenance và fallback endpoint: protocol §10.2.2–§10.2.3; cú pháp truy vấn
`WorkflowRun.file` nằm trong `.claude/skills/cross-review/SKILL.md`, mục “Provenance CI”.

## Ca symlink Windows native

**Đã đo** (WP748 g11, Windows 11, Python 3.13.1, head `0daeb47`, 15-10-2026): 12 ca `t20n`
`t20x` `t20zd` `t20zf` `t20q` `t20zi` `t20zj` `t20zk` `t20zl` `t20zm` `t20zn` `t20zo` của
`ops/ci_duong_nhanh_test.py`, mỗi ca một lệnh `--mot-ca`, cả 12 `rc=0`, không `WinError 1455`.
Đó là bằng chứng TARGETED trên đúng head ấy, không phải full suite.

**Hướng dẫn** (luật đọc, không phải kết quả đo). Mỗi ca một lệnh, lấy rc ngay sau lệnh:

```bash
PY="$(command -v python3 || command -v python || command -v py)"   # CLAUDE.md: nhận CẢ BA tên
"$PY" -B -c 'import yaml'   # thiếu PyYAML thì module chết lúc nạp, không phải lỗi ca
"$PY" -B ops/ci_duong_nhanh_test.py --mot-ca t20zk_kiem_re_symlink_treo_qua_bi_danh_thu_muc_do
echo "t20zk rc=$?"           # 0 = đạt (không in gì); 3 = DO; 4 = HONG
```

- Fixture dựng symlink THẬT (`Path.symlink_to`, tệp hay thư mục khai bằng `target_is_directory`;
  trên Windows đích đổi `/` thành `\`). Không có nhánh bỏ qua: không tạo được symlink ⇒ `HONG`.
- `WinError 1455` ném từ `subprocess.Popen` lúc fixture chạy `git init`, trước assertion, là lỗi
  MÔI TRƯỜNG: ghi lại, đo bộ nhớ/pagefile, dừng gate nặng song song.
- Targeted không thay full suite (`CA: N/N`, `DOT BIEN: M/M`, `TONG: DAT`) trên đúng head.
- Ngoại lệ named pipe/socket của `t20zo` (FIFO = symlink tới named pipe thật; socket = `os.stat`
  giả cho leaf `sk`, comment 6171400658) đo logic danh sách cho phép, tách khỏi bằng chứng symlink.
