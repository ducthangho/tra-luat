# wp55 revision 2 · generation 3 · EXECUTOR (`claude`) — vá ba finding P1 chặn

Bạn là **executor** của work packet **wp55** (issue #55), mission #54 revision 6.
Vai này **KHÔNG** review, **KHÔNG** approve, **KHÔNG** merge, **KHÔNG** land, **KHÔNG** deploy.

> **ĐÂY LÀ ATTEMPT NỘI DUNG CUỐI CÙNG CỦA REVISION 2.** `attempts_used = 2`,
> `attempts_limit = 3`. Lượt này hỏng thì revision 2 cạn trần và packet chuyển
> `blocked`, phải mở revision mới. Vì thế: vá **cả ba** finding trong **một** lượt,
> và đo từng cái trước khi giao — đừng giao sớm rồi tính vá vòng sau, vì không còn
> vòng sau.

---

## BƯỚC 0 — xác minh danh tính TRƯỚC khi làm bất cứ gì

Sai bất kỳ mục nào ⇒ **DỪNG**, báo lại, không sửa file.

```bash
# 0a. đúng kho
git remote -v                      # phải là github.com/ducthangho/tra-luat
git rev-parse --verify HEAD        # ghi lại, sẽ đối chiếu ở 0c

# 0b. đúng prompt — tệp này, không phải bản chép trong comment
#     Tìm ở `master` trước; chưa thấy thì fetch nhánh ops đang mang nó.
sha256sum ops/prompts/wp55-r2-exec-3-claude-20260814.md
#   PHẢI ra đúng con băm mà lease khai ở `prompt_sha256_required`.
#   Lệch ⇒ bạn đang đọc một bản khác ⇒ DỪNG.

# 0c. đúng head xuất phát
git fetch origin claude/wp55-r2g2-f3-03
git rev-parse origin/claude/wp55-r2g2-f3-03
#   PHẢI = cf39109c9e5167516c53f2071e5fa7ec5c6afff5
#   Khác ⇒ có phiên khác đã đẩy ⇒ DỪNG, hỏi bên điều phối.
```

**Kiểm đường giao kết quả TRƯỚC khi làm việc.** Vòng 3 của revision 1 làm xong rồi
không ghi được verdict, và ba lease review chết vì phát hiện muộn. Chạy thử ngay:

```bash
git push --dry-run origin HEAD:refs/heads/claude/wp55-r2g2-f3-03
```

Không push được ⇒ **DỪNG** và báo, đừng làm rồi mới biết không giao được.
(Trong môi trường agent web, `gh` và `api.github.com` có thể bị 403 trong khi git
vẫn chạy — đã đo 13/14-08. Đường giao là **git push**, không phải API.)

---

## Bối cảnh: vì sao có lượt này

Cross-review lượt 4 (phiên `codex`, dưới lease `wp55-r2-review-4-codex-20260814`)
đã cho verdict **`changes_requested`** trên `cf39109c` với **ba finding P1 chặn**.

Bản verdict nguyên văn nằm trong kho, neo băm — **đọc nó, đừng chỉ đọc prompt này**:

```
ops/reviews/wp55-r2-review-4-codex-verdict.md
sha256 = d58088bec10ad36a912b64749cbe8a41af5de0b3f70033d9109f12bb6647e82f
```

Biên nhận (nơi đã đăng, và hai sai lệch của đường đăng):
`ops/reviews/wp55-r2-review-4-codex-verdict.receipt.yaml`

---

## Phạm vi — ĐÚNG 6 tệp, không hơn

```
.claude/dev/packet_loop.py
.claude/dev/packet_loop_test.py
.claude/skills/cross-review/SKILL.md
.claude/skills/land-packets/SKILL.md
.claude/skills/work-packet/SKILL.md
CLAUDE.md
```

`git status --porcelain` phải sạch ngoài 6 tệp này. **Không** bump VERSION, **không**
cấp rNNN, **không** sửa CHANGELOG / RELEASE_MANIFEST / golden, **không** đụng
`.github/**`, **không** chạm Drive/NLM/registry/secrets, **không** đụng nhánh
`claude/wp55-f3-03` hay PR #56.

**Cảnh báo tương tác với master:** master đã đi rất xa kể từ base `fbe5ab9e`, và
trong 6 tệp trên nó **chỉ chạm `CLAUDE.md`**. Sau khi sửa, kiểm lại:

```bash
git merge-tree --write-tree origin/master HEAD   # phải rc=0
```

Còn `rc=0` thì không cần rebase — rebase là việc của lúc land, và làm bây giờ sẽ
đổi head, làm vô hiệu lượt review kế tiếp trước cả khi nó bắt đầu.

---

## FINDING 1 — `lease-authority-spoof` (P1)

**Chỗ hỏng:** `.claude/dev/packet_loop.py`, `cmd_record_lease`, chốt `granted_by`
(quanh dòng 399–423 ở `cf39109c`).

```python
if nguoi_cap.lower() in PROVIDERS:      # PROVIDERS = ("claude", "codex")
    _die(RC_GUARD, ...)
```

**Vì sao sai:** đây là **danh sách CẤM**, và nó chỉ từ chối đúng hai chuỗi. Nguyên văn
reviewer: *"distinguishes spelling, not authority"* — phân biệt **cách viết**, không
phân biệt **thẩm quyền**. Reviewer đã tái lập được: `codex-dispatcher`, `ai-codex-bot`,
`cödex` đều `rc=0`, ghi được lease rồi `begin-attempt` cũng `rc=0`.

**Đã có lời giải chạy được — đọc và chép cách làm:** cùng khuyết tật ở tầng cửa đăng
đã vá xong và **đang trên master**:

```
ops/lease_publish.py        → hằng NGUOI_CO_THAM_QUYEN + hai chốt trong hàm kiem()
ops/lease_publish_test.py   → ca t02b (danh sách cho phép) và t02d (GITHUB_ACTOR)
ops/README.md               → mục "Danh sách CẤM không bao giờ đủ"
```

Đo được ở đó: ba tên tấn công `rc=0` → `rc=4`, người có thẩm quyền vẫn `rc=0`.

**Nghiệm thu — phải có ĐỦ cả ba:**

1. Đảo thành **danh sách CHO PHÉP**. `--granted-by` không nằm trong danh sách ⇒ chặn.
   Giữ chốt `PROVIDERS` cũ nếu muốn (thông điệp của nó gọi đúng tên bệnh), nhưng thứ
   **thật sự chặn** phải là danh sách cho phép.
2. Ca phản chứng bơm **đủ bốn** tên: `codex-dispatcher`, `ai-codex-bot`, `cödex`
   (dựng sẵn `U+00F6`), và bản tổ hợp dấu (`o` + `U+0308`). Cả bốn phải bị chặn.
   Cộng ca **không chặn oan**: người có thẩm quyền vẫn qua.
3. **Đột biến bắt buộc:** nới danh sách cho phép để chứa cả bốn tên tấn công ⇒ ca đích
   phải **ĐỎ**. Không có đột biến này thì không biết ca đang đo danh sách hay đo thứ khác.

**Nói thẳng giới hạn trong chú thích**, đừng khai rộng hơn: danh sách chứng minh cái
*tên* được phép, **không** chứng minh đúng người đó đã gõ. `packet_loop.py` chạy cục
bộ nên **không** có `GITHUB_ACTOR` để neo — khác `ops/lease_publish.py`. Viết đúng như
vậy; một lời khai rộng hơn thực tế chính là finding mà reviewer đã bắt.

---

## FINDING 2 — `legacy-lease-bypass` (P1)

**Chỗ hỏng:** `cmd_begin_attempt` (quanh dòng 437–450 ở `cf39109c`).

```python
lease = st.get("lease")
if lease and lease.get("expires_utc"):     # ← FAIL-OPEN
    ...kiểm hạn...
```

**Vì sao sai:** thiếu trường `lease` thì **bỏ qua toàn bộ** phép kiểm. Reviewer đã tái
lập: state do head liền trước (`22d2cc9`) sinh ra có `state: leased` mà **không có**
`lease`, và mã mới nhận nó vào `running` — không hề đi qua `record-lease`. Điều đó
**mâu thuẫn trực tiếp** với lời khai của adapter rằng `leased` chỉ tới được qua
`record-lease`.

**Nghiệm thu:**

1. `begin-attempt` phải **từ chối** state ở `leased`/`running` mà thiếu `lease`, hoặc
   `lease` hỏng/thiếu `expires_utc`. Fail-**closed**.
2. Nếu chọn cho phép nâng cấp state cũ thì phải là **đường di trú tường minh, có
   uỷ quyền** — không được nâng cấp ngầm.
3. Ca phản chứng dạng **fixture state cũ**: dựng state bằng chính entrypoint ở
   `22d2cc9` (`git show 22d2cc9:.claude/dev/packet_loop.py`), rồi chạy `begin-attempt`
   của bản mới lên nó. Đây là ca reviewer yêu cầu đích danh.
4. **Đột biến:** trả điều kiện về `if lease and lease.get("expires_utc")` ⇒ ca đích ĐỎ.

---

## FINDING 3 — `doctrine-rendering-bypass` (P1)

**Chỗ hỏng:** `_chuan_hoa` (quanh dòng 183–194 ở `cf39109c`).

```python
_TRANG_TRI = str.maketrans("", "", "`*_~")
text = unicodedata.normalize("NFC", text).casefold().translate(_TRANG_TRI)
```

**Vì sao sai:** xử lý trang trí Markdown và khoảng trắng, nhưng **không** xử lý ký tự
định dạng vô hình và HTML entity. Reviewer đo được:

```
"merged: PR đã vào nhánh đích"                  rc=6   ← bắt
"mer<zero-width-space>ged: PR đã vào nhánh đích" rc=0   ← LỌT, mà render ra ĐÚNG cụm cấm
"merged&#58; PR đã vào nhánh đích"               rc=0   ← LỌT, render ra ĐÚNG cụm cấm
```

Hai dạng lọt đều **hiển thị đúng cụm doctrine bị cấm** trong Markdown, nên tiêu chí
nghiệm thu số 2 (cấm chép doctrine bằng máy) chưa đạt.

**Nghiệm thu:**

1. Chuẩn hoá phải quy các dạng **render ra tương đương** về một mối: bỏ ký tự định
   dạng Unicode (`Cf` — gồm `U+200B`…`U+200D`, `U+FEFF`, `U+00AD`), và giải HTML
   entity một cách **an toàn**.
2. **An toàn** ở đây có nghĩa cụ thể, viết vào chú thích: giải entity **một lần**,
   không lặp tới điểm bất động — giải lặp sẽ biến `&amp;#58;` (vốn hiển thị nguyên
   văn `&#58;`, không phải dấu hai chấm) thành dấu hai chấm và sinh **dương tính giả**.
3. Cả hai dạng tấn công thành **negative fixture** — reviewer yêu cầu đích danh.
4. Chuẩn hoá này dùng **CHỈ** cho `doctrine-scan`. **Đừng** đụng phép đếm finding:
   chú thích hiện có đã nêu đúng lý do — khớp rộng ở doctrine là sai về phía an toàn,
   còn khớp rộng ở `finding-id` sẽ gộp oan hai lỗi khác nhau.
5. **Đột biến:** gỡ lớp `Cf`, rồi gỡ lớp entity ⇒ mỗi lần một ca đích ĐỎ.

---

## Cổng phải xanh trước khi giao

Chạy **thật**, đọc `rc` của **từng lệnh**, không để `rc` rơi vào `tail`:

| lệnh | bằng chứng dương phải có |
|---|---|
| `python .claude/dev/packet_loop_test.py` | `N/N` với **hai số bằng nhau**, và N **lớn hơn** 48 |
| `python scripts/tl.py --selftest` | `N/N` hai số bằng nhau |
| `python scripts/tl.py doc-claims-check --strict --json` | `ok: true`, `flags` rỗng |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | `ok: true`, `failed 0`, `extra 0` |
| `python scripts/tl.py golden-test --json` | `ok: true` — **KHÔNG** `--write` |
| `git merge-tree --write-tree origin/master HEAD` | `rc=0` |
| `git diff --check` | `rc=0` |

**Đột biến chạy trên BẢN SAO TẠM**, không đụng tệp thật. Lượt chạy bị cắt giữa chừng
thì `finally` không chạy, và tệp ở lại trạng thái méo — đã có một bản vá NGƯỢC đi thẳng
vào commit theo đường này.

**Không tin `rc=0` suông.** Một cổng "xanh" có thể là cổng **vắng mặt**: đòi `N/N` hai
số bằng nhau, `"ok": true`, tệp có thật, băm khớp.

---

## Giao kết quả

1. Commit lên nhánh `claude/wp55-r2g2-f3-03`, push. Head mới thay `cf39109c`.
2. Cập nhật mô tả PR #92: nêu head mới, ba finding đã vá, số đo từng cổng, và các
   đột biến kèm ca đích bị giết. Nếu không sửa được mô tả PR thì đăng comment — và
   **nói rõ** rằng mô tả cũ đã lạc hậu ở chỗ nào, đừng để nó khai sai SHA.
3. **Đầu ra cuối cùng phải là một handoff §7** kèm: `head_sha` mới, ba `finding_id`
   với `disposition: fixed`, tên ca test khoá từng cái, tên đột biến và ca nó giết,
   và mọi giới hạn còn lại — nói thẳng, đừng làm tròn.

**KHÔNG** tự review, **KHÔNG** tự approve, **KHÔNG** merge, **KHÔNG** ghi verdict cho
chính mình. Lượt cross-review kế tiếp **bắt buộc là `codex`** (§8), trên head mới.

---

## Stop conditions — gặp thì DỪNG và báo, đừng tự xoay

- BƯỚC 0 lệch bất kỳ mục nào (kho / băm prompt / head xuất phát).
- `git push --dry-run` không chạy được.
- Lease hết hạn giữa chừng — kiểm lại `lease_expires_at_utc`, đừng chạy quá hạn rồi
  khai là còn hạn.
- Cần sửa một tệp **ngoài** 6 tệp write_set.
- `merge-tree` với master thành `rc != 0`.
- Ba finding hoá ra **không vá được trong một lượt** — báo ngay thay vì giao một nửa,
  vì đây là attempt cuối và một lượt hỏng đắt hơn một lượt chưa bắt đầu.
