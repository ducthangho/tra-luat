# wp55 revision 3 · CROSS-REVIEW lượt 11 — reviewer `codex` · head `4085bbf`

Bạn là **reviewer độc lập**. Vai này **CHỈ ĐỌC**: không sửa tệp, không commit, không push,
không merge, không land, không deploy. Đầu ra là **verdict** + **evidence §7**.

§8 đòi reviewer khác provider với executor. Executor là `claude` ⇒ reviewer phải là `codex`.
Không phải `codex` thì **DỪNG** và báo lại.

---

## BƯỚC 0 — xác minh. Lệch bất kỳ mục nào ⇒ DỪNG, báo lại.

```bash
git rev-parse --is-shallow-repository        # ĐÒI false
git remote -v                                # ĐÒI github.com/ducthangho/tra-luat
git config core.abbrev 7

git fetch origin ops/wp55-r3-spec
git show origin/ops/wp55-r3-spec:ops/specs/wp55-r3-spec.md | sha256sum
#   ĐÒI e321f811724fae97b19d523a3e5159bc13b425cd15fc6c753c7439fe28cae22d

git fetch origin claude/wp55-r3g5-f3-03
git rev-parse origin/claude/wp55-r3g5-f3-03
#   ĐÒI 4085bbf22d565a4189977f0504dfd8e5f748bfce
#   Khác ⇒ có phiên đẩy tiếp ⇒ DỪNG, hỏi bên điều phối. (Đã xảy ra BA lượt liên tiếp.)

sha256sum ops/prompts/wp55-r3-review-11-codex-20260815.md   # ĐÒI khớp prompt_sha256_required
```

**KIỂM ĐƯỜNG GIAO VERDICT TRƯỚC KHI LÀM VIỆC.** Nhiều lượt đã hỏng ở khâu này (`403`, `gh`
không cài, MCP chưa xác thực). `git push` thì chạy. Không ghi được lên GitHub thì **vẫn
review**, ghi verdict vào kho theo mục *Giao kết quả* và nói rõ ngay ở ĐẦU báo cáo.

---

## Head này khác `1a4525a` ĐÚNG MỘT COMMIT

`4085bbf` = `1a4525a` + một commit **vá an ninh**, do **phiên điều phối** đẩy theo lệnh
trực tiếp của chủ kho — không qua lease executor. Chỉ sửa `.claude/skills/work-packet/SKILL.md`.

```bash
git diff --name-status 1a4525a20aa360476a6f59cb157c21097919c457 4085bbf22d565a4189977f0504dfd8e5f748bfce
```

Vì vậy **verdict lượt 10 vẫn còn giá trị gần như trọn vẹn** — bốn finding P1 của nó nằm
trong `packet_loop.py`, tệp mà commit này **không đụng**. Việc của bạn không phải soi lại từ
đầu, mà là:

1. **Kiểm bản vá an ninh** — nó mới, chưa ai review.
2. **Kiểm bốn finding lượt 10 có còn đúng ở `4085bbf` không**, và có chỗ nào bạn thấy khác.
3. Tìm cái lượt 10 chưa tìm ra.

---

## 1. Bản vá an ninh — soi kỹ, đây là thứ MỚI

```diff
-echo "${TEN_BIEN:+có, ${#TEN_BIEN} ký tự}${TEN_BIEN:-chưa đặt}"
+if [ -n "${TEN_BIEN:-}" ]; then echo "có, ${#TEN_BIEN} ký tự"; else echo "chưa đặt"; fi
```

Phiên điều phối đo: đặt → `có, N ký tự` (không lộ); chưa đặt/rỗng → `chưa đặt`; an toàn dưới
`set -u`; đột biến trả về dạng cũ thì **lộ token**.

Hỏi ngược:

- Còn đường nào trong **cả ba adapter** in ra giá trị biến bí mật không? `:-` `:=` `:+`
  `${!VAR}` `set -x` `env` `printenv`, in `$?` kèm biến, `echo` cả dòng lệnh, here-doc,
  `trap`, log của chính lệnh.
- Bản mới có **bắt oan** không: biến đặt bằng chuỗi chỉ có khoảng trắng thì báo gì? Tên biến
  chứa ký tự lạ? Vỏ shell khác `bash` (dash/zsh/PowerShell) có cùng hành vi không? Adapter
  không nói rõ shell.
- Chú thích mới có khai đúng **hành vi** không, hay lại chỉ khai **ý định** như bản cũ — đó
  chính là lý do lỗi này sống sót qua nhiều lượt.
- Phạm vi: commit này có đụng gì ngoài **một** tệp không?

## 2. Bốn finding P1 của lượt 10 — còn đúng ở `4085bbf` không

```
doctrine-measurement-marker-semantic-bypass   P1   (disposition: must_fix_spec_revision_4_and_code)
doctrine-indented-code-block-bypass           P1
doctrine-comment-erases-fence-closer-bypass   P1
doctrine-html-table-token-context-bypass      P1
```

Bản gốc: `ops/reviews/wp55-r3-review-10-codex-verdict.md` trên nhánh
`ops/wp55-r3-review-10-verdict`. **Đọc bản gốc, đừng đọc tóm tắt này.**

Chạy lại từng ca trên `4085bbf`. Khác kết quả ⇒ đó là finding mới, nói rõ.

## 3. Trục đáng dồn sức — con lắc đã đánh quá SÁU lần

```
g4  thêm miễn trừ để thôi bắt oan     ⇒ quá rộng, heading trần lọt
g5  "chỉ tha khi ngắt dòng"           ⇒ vẫn quá rộng
g6  "chỉ tha cho VĂN XUÔI"            ⇒ vẫn lọt fence lồng cấp, bảng HTML
g7+g8 thêm chốt fence + bảng          ⇒ lọt closer sai, bảng lồng; VÀ bắt oan đuôi tệp
g9  sửa bốn cái của lượt 9            ⇒ lượt 10 tìm ra bốn cái mới
```

Mỗi lần siết một chiều thì hở chiều kia. Finding 1 của lượt 10 nói đúng chỗ đau:
**dấu hiệu từ vựng không chứng minh một cụm đang kể lại kết quả đo** — và `disposition` của
nó là `must_fix_spec_revision_4_and_code`, tức chính reviewer cũng cho rằng **spec** phải đổi.

Câu hỏi tôi muốn bạn trả lời thẳng, kể cả khi câu trả lời khó chịu:

> **AC 19 có thể cưỡng chế bằng máy không?** Nếu miễn trừ "văn xuôi kể lại kết quả đo" không
> có tiêu chí máy nào phân biệt được với văn bản chép doctrine, thì mọi lượt vá tiếp theo đều
> đang đuổi một thứ không tồn tại.

Trả lời "không" là một verdict hợp lệ và có giá trị hơn cú đánh quá thứ bảy. Có bản thảo
revision 4 đang chờ chủ kho duyệt (`ops/wp55-r4-spec-draft`) — bạn **không** bị ràng buộc
bởi nó, nhưng đọc qua để khỏi trùng công.

## 4. Hai mục đã HOÃN sang revision 4 — đừng nêu như finding mới

- `ac20-archive-tree-suite-not-self-contained`
- `same-provider-fallback-contradicts-protocol` — §8 cho `same_provider_approved` khi phía
  kia hết quota, nhưng CLI từ chối vô điều kiện. Vá là **nới một AC**, đúng thứ §12 cấm.

Chỉ nêu lại nếu bạn đo được điều **khác** với mô tả đó.

## 5. Gate — tự chạy, đừng chép

```bash
python3 .claude/dev/packet_loop_test.py
python3 .claude/dev/packet_loop.py doctrine-scan --root .
python3 scripts/tl.py --selftest                            # ĐÒI hai số BẰNG NHAU
python3 scripts/tl.py doc-claims-check --strict --json      # ĐÒI flags=[]
python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --root . --strict --json
python3 scripts/tl.py golden-test                           # KHÔNG --write
python3 .githooks/eol_policy.py --all --json                # ĐÒI violations=0
# release-bundle ×2 trên head + ×1 từ base — ĐÒI cả BA cùng sha256
git diff --name-status fbe5ab9e1ece3b45c065879bfd59dee2554db3e2 4085bbf22d565a4189977f0504dfd8e5f748bfce
```

Bên điều phối đã chạy trên `4085bbf`: `doctrine-scan` rc=0 · suite **173/173 ĐẠT** ·
`eol` rc=0 · phạm vi đúng **6 tệp**. **KHÔNG** chạy được `tl.py --selftest` (pyo3
`PanicException` từ `cryptography`; delta=0 trên cùng container, nhánh không đụng `scripts/`).
Lượt 9 cũng `timeout` ở mục này. **Chưa ai xác minh `1696/1696`** — nếu bạn chạy được, báo số thật.

**AC 20 — cây ĐÃ MERGE, neo SHA BẤT BIẾN:**

```bash
MASTER=$(git rev-parse origin/master)    # ghi rõ SHA này trong verdict
merged=$(mktemp -d)
git archive "$MASTER" | tar -x -C "$merged"
git diff --binary fbe5ab9e1ece3b45c065879bfd59dee2554db3e2..4085bbf22d565a4189977f0504dfd8e5f748bfce \
  | git -C "$merged" apply
python3 -B "$merged/.claude/dev/packet_loop.py" doctrine-scan --root "$merged"
GIT_DIR="$PWD/.git" python3 -B "$merged/.claude/dev/packet_loop_test.py"
```

**Mọi lệnh trong verdict phải neo SHA BẤT BIẾN** — không `origin/master`, không `HEAD`, không
tên nhánh. Lượt 5 đã vấp chỗ này.

## 6. Fixture — đăng NGUYÊN VĂN, đừng chỉ mô tả

Lượt 9 mô tả fixture bằng lời; bên điều phối dựng lại **sai** và báo nhầm là "không tái lập
được", rồi phải đính chính. Khi có fixture nguyên văn thì 7/7 khớp.

⇒ Verdict của bạn phải kèm **nội dung tệp fixture nguyên văn** cho mọi ca, không chỉ mô tả.
Và với mỗi ca lọt, kèm **đối chứng cùng-câu-khác-đúng-một-biến** — lượt 9 có một ca mà đối
chứng dùng câu khác, nên `rc=0` của nó giải thích được bằng finding KHÁC, không phải finding
đang nêu.

---

## Verdict và evidence

`approve` · `changes_requested` · `blocked`.

Mỗi finding: `finding_id` (slug kebab-case ổn định), `severity`, `disposition`, **bằng chứng
chạy được neo SHA bất biến** + **fixture nguyên văn**. Không tái lập được thì ghi rõ là
**nghi vấn**.

**Nói thẳng chỗ bạn KHÔNG chạy được.** Các lượt trước làm vậy và nhờ thế người đọc biết ranh
giới của bản review.

### Giao kết quả

Ưu tiên: review trên **PR #120** neo `commitID = 4085bbf22d565a4189977f0504dfd8e5f748bfce`,
kèm evidence §7 lên issue #55.

Không ghi được thì ghi vào kho — khuôn đã chạy được từ lượt 5:

```
ops/reviews/wp55-r3-review-11-codex-verdict.md
ops/reviews/wp55-r3-review-11-codex-verdict.receipt.yaml
```

Xuất **thẳng `stdout` ra tệp**, đừng chép tay. Push lên một nhánh `ops/**`, báo `sha256` +
số byte.

## Stop conditions

Head đổi giữa chừng · lease hết hạn · bạn không phải `codex` · BƯỚC 0 lệch · bị đòi sửa
tệp/commit/push/merge/land · không chạy được phần thiết yếu (báo `blocked` kèm lý do đo được,
đừng đoán rồi `approve`) · chạm quota (ghi lý do allowlist, **không** tiêu attempt nội dung).

Heartbeat **mỗi 30 phút** lên #55; đường ghi bị chặn thì ghi nhịp vào tệp trong kho và nói rõ.
