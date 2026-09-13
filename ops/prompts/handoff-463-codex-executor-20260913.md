# BÀN GIAO packet `GATE-TACH-JOB-CAT-CHI-PHI` (#463) — executor `claude` → executor `codex`

Soạn 13-09-2026 bởi phiên executor `claude` sau cross-review lượt 10.
**Đây là HỒ SƠ BÀN GIAO, không phải lệnh khởi động.** Đọc mục 0 trước tiên.

---

## 0. CHƯA CÓ LEASE THÌ CHƯA ĐƯỢC BẮT TAY

Lease đang hiệu lực là `gate-tach-job-cat-chi-phi-exec-2r10-claude-20260912`, và nó ghi
`executor: claude` · `provider: claude`. **Tệp này KHÔNG cấp quyền cho ai.** Theo
`docs/PROTOCOL_DA_PHIEN.md` §3.2/§4, đổi executor đòi một **lease MỚI** do **chủ kho** cấp:

- `lease_id`: `gate-tach-job-cat-chi-phi-exec-3-codex-<ngày>`
- `executor`/`provider`: `codex`
- `reviewer_provider`: **`claude`** — §8 đòi reviewer khác danh tính executor. Đảo vai so với
  bốn lượt vừa rồi (executor claude / reviewer codex).
- `thay_the_cho: [gate-tach-job-cat-chi-phi-exec-2r10-claude-20260912]`, và **bia mộ hai chiều**:
  đặt `da_bi_thay_the` vào chính tệp lease CŨ (`_kiem_bia_mo` đòi cả hai chiều).
- `spec_sha256` = `spec_hash` = `decdb1a1ae794508f0be6d680342bbf7c46b7353e0708f16b522567e8cc56d96`
  (`ops/specs/GATE-TACH-JOB-CAT-CHI-PHI.md` **revision 21**). Băm lệch ⇒ lease sai, dừng.
- **KHÔNG chép `posted_comment_id`** của lease cũ.
- `granted_on_instruction` neo vào một comment trên Issue #463 (dấu vết bền).

Trước khi cấp, đo `A9` bằng **công cụ**, không bằng lời khai:

```bash
git ls-remote --heads origin | sed 's#.*refs/heads/##' | sort            > /tmp/mc
git for-each-ref --format='%(refname:lstrip=3)' refs/remotes/origin \
    | grep -v '^HEAD$' | sort                                           > /tmp/cb
comm -23 /tmp/mc /tmp/cb        # khác rỗng ⇒ MÙ ⇒ fail-close, fetch rồi đo lại
python ops/lease_publish.py ai-dang-giu .github/workflows/ci.yml
python ops/lease_publish.py ai-dang-giu .claude/dev/ci_dang_ky_test.py
```

`CHAN [12]` nghĩa là **nhánh cục bộ tụt sau**, KHÔNG phải `NGƯỜI_GIỮ 0`; đồng bộ rồi đo lại.
Và `check rc=0` **không** thay được phép đo này. Cổng đọc từ **REF** nên **commit trước rồi mới
`check`**.

---

## 1. NEO DANH TÍNH

| trường | giá trị |
|---|---|
| kho | `github.com/ducthangho/tra-luat` |
| root commit (vân tay bền) | `394e93468fc8d84ec20938e6df8fb7ab72b2cc37` |
| nhánh packet | `claude/gate-tach-job-cat-chi-phi` |
| head bàn giao | `3bbc6b46c2fb6066fa64088308ce30fe40f87aa5` |
| base (`merge-base` với master) | `bb7013c7669da19304a8769e5b25f8c1f8951e9c` |
| spec | `ops/specs/GATE-TACH-JOB-CAT-CHI-PHI.md` r21, `decdb1a1…` — **chỉ có trên nhánh `ops/cap-lease-463`**, chưa vào master. Tìm ở `master` trước, chưa thấy thì `git fetch origin ops/cap-lease-463`. Thứ định danh tệp là **BĂM**, không phải tên nhánh. |
| verdict 4 lượt | `ops/reviews/gate-tach-job-cat-chi-phi-review-{7,8,9,10}-codex-verdict.md` + `.receipt.yaml`, cùng nhánh ấy |

**Master đã đi trước base 53 commit** nhưng **không chạm write set** (`git diff --numstat
bb7013c7..origin/master -- .github/workflows/ci.yml .claude/dev/ci_dang_ky_test.py` ⇒ RỖNG), và
`git merge-tree` cho **0 xung đột**. Merge master vào là an toàn — nhưng **đo lại**, đừng tin dòng này.

---

## 2. WRITE SET — ĐÚNG HAI ĐƯỜNG DẪN, KHÔNG HƠN

```
.github/workflows/ci.yml
.claude/dev/ci_dang_ky_test.py
```

Đường dẫn thứ BA ⇒ điều kiện dừng `S1` ⇒ **DỪNG và hỏi chủ kho**, không tự mở write set.
Đã có hai thứ bị từ chối đúng vì luật này, và reviewer xác nhận cả hai lần:

- `ops/nhanh_don_duoc_test.py` (nợ F/G của lượt 7) — **nghĩa vụ ĐỌC**, không phải quyền GHI.
- `ops/kiem_hop_dong_packet*.py` (lớp B) — công cụ đo chỉ sống ở nhánh lease, **không** mang sang head.

---

## 3. TRẠNG THÁI ĐO ĐƯỢC TẠI `3bbc6b4`

```
ĐĂNG KÝ: 21/21 · LAUNCHER WINDOWS: 4/4 · RUFF CI: 3/3
PHẢN CHỨNG: 108/108 đỏ đúng · TỔNG: ĐẠT
ruff --select F: All checks passed!     actionlint ci.yml: rc=0
A8: additions = 500 / trần 500 · đúng 2 đường dẫn
  374  88  .claude/dev/ci_dang_ky_test.py
  126   6  .github/workflows/ci.yml
```

**`A8` ĐÃ DÙNG SÁT TRẦN — 500/500, không còn một dòng dư.** Trần đã nâng **BA** lần
(300→400→430→500). **KHÔNG đề nghị lần thứ tư**; reviewer nói thẳng điều đó ở cả lượt 9 lẫn 10.
Mọi bản vá phải **trung hoà dòng hoặc âm**: thay nhánh trùng trong chính hai path, đừng nối thêm.

Cách xuống dòng đã dùng và còn dùng lại được: chú thích **lặp nguyên văn** ở hai job mới của
`ci.yml` đã đổi thành **con trỏ** về bản gốc ở job `gate` (154→126). **Bản gốc trong `gate` phải
giữ NGUYÊN VĂN** — tôi đã lỡ thay cả bản gốc một lần và phải trả lại; đo bằng
`git diff origin/master -- .github/workflows/ci.yml` và nhìn kỹ vùng `jobs.gate`.

---

## 4. VIỆC CÒN LẠI — ĐẶT CÂU HỎI BIỂU DIỄN LÊN TRƯỚC, ĐỪNG ĐẶT DANH SÁCH CỬA LÊN TRƯỚC

Verdict lượt 10: `changes_requested`, **0 P1 / 1 P2 / 0 P3**, 11 hướng săn. Finding P2 mang **đúng
stable slug** `ruff-khuon-chua-chung-minh-provisioning` của lượt 7, 8, 9 và 10 — **BỐN lượt liên
tiếp cùng một hình dạng**. Số cửa theo lượt: **3 → 4 → 8 → 9**.

Lượt 9 đã DỪNG một lần theo §12 và chủ kho quyết **rút phạm vi**: bỏ chốt env (chốt ấy do phiên
thi công tự thêm, `M7`/`A7` không đòi). Reviewer lượt 10 xác nhận quyết định ấy **ĐÃ VÁ THẬT** và
**không mất nghĩa vụ nào** mà `M7`/`A7` thực sự ghi. Ba bệnh lexer của lượt 9 cũng **ĐÃ VÁ THẬT**.

Nhưng lớp còn lại chưa đóng, và reviewer nhắc §12 nguyên văn:

> *"Cùng stable finding qua nhiều lượt vẫn cần xử lý theo §12; không biến các sửa nhỏ đã thử
> thành lời hứa hội tụ."*

**Nên việc đầu tiên KHÔNG phải vá chín cửa.** Việc đầu tiên là trả lời:

> `loi_ruff_ci` phải **nhận** miền cú pháp nào, và **từ chối** miền nào — công khai, có thể phát
> biểu thành một câu, và fail-close ngoài miền?

Ba chốt mà `M7`/`A7` đòi rất khiêm tốn: (1) mọi job cài Ruff đều ghim `ruff==0.15.15`; (2) mọi job
cài Ruff đều in probe `ruff --version` SAU dòng cài; (3) đúng MỘT job chạy `--chay`, Ruff cài CÙNG
job và TRƯỚC bước đó. `A7` chỉ đòi **4 fixture về BỐ CỤC JOB** cộng hai phản chứng cũ giữ màu.
Mọi thứ vượt quá ba câu ấy là thứ phiên trước đã tự thêm và đã phải gỡ một lần.

Chín cửa lượt 10 (để bạn biết miền nào đang thủng, **không phải danh sách việc**):

| # | cửa | chiều |
|---|---|---|
| H2 | `python -m Ruff --version`, module `ruff[all]` được nhận, Python thật `rc=1` | **nhận bằng chứng SAI** |
| H11 | `python -m ruff --help --version` `rc=0` nhưng in trợ giúp; `check --version` `rc=2` — vẫn được cấp probe | nhận sai |
| H3 | requirement có extras `!` hoặc dấu phẩy treo, pip bác, vẫn gắn `GHIM` | nhận sai |
| H10 | quote chưa đóng ⇒ Bash `rc=2`; fallback `split()` vẫn dựng argv đủ điều kiện | nhận sai |
| H4 | backslash-newline **giữa** token bị chèn space làm tách token | **bác bằng chứng ĐÚNG** |
| H5 | `$'…'` (ANSI-C quoting) còn giữ `$` trong token | bác đúng |
| H8 | một probe TRƯỚC install làm probe đúng SAU install mất hiệu lực (hàm giữ vị trí ĐẦU TIÊN) | bác đúng |
| H6 | gọi registry bằng **tên module** bị báo không có registry; đường tuyệt đối thì nhận | bác đúng |
| H9 | nhánh bước **có điều kiện** còn đọc **chuỗi con thô**, chưa dùng vị từ tên mới | chưa đồng bộ |

Reviewer đã **thử vá một phần** H2/H4/H8 trên bản sao: `374→373` dòng Python, tổng `500→499`,
`108/108` giữ nguyên. Đó là **chẩn đoán**, không phải gói vá; đừng áp mù.

**Nếu bạn kết luận rằng ba chốt không thể biểu diễn đúng trong hai path với trần 500 — hãy DỪNG
và nói ra.** Đó là câu trả lời hợp lệ, và nó đúng doctrine hơn là vá lượt thứ năm.

---

## 5. LỆNH

```bash
PY="$(command -v python3 || command -v python || command -v py)"
sed -n '1,140p' .claude/dev/launcher.py      # hợp đồng: mã thoát, 4 bẫy đa nền
"$PY" .claude/dev/launcher.py doctor         # BẮT BUỘC, trước mọi việc khác
"$PY" .claude/dev/launcher.py chuan-bi       # khi hook không chạy

"$PY" -B .claude/dev/ci_dang_ky_test.py      # đòi 108/108 và TỔNG: ĐẠT
"$PY" -m ruff check --select F .claude/dev/ci_dang_ky_test.py
actionlint .github/workflows/ci.yml
git diff --numstat $(git merge-base HEAD origin/master) -- . \
  | awk '{a+=$1; n++; print} END {print "additions="a" · duong dan="n}'
```

**KHÔNG chạy CI** — không `workflow_dispatch`, không full CI, không Windows CI — cho tới khi đủ
điều kiện merge. Windows CI có lỗi đã biết. `A1`/`A5` vì thế là **KHÔNG ĐO ĐƯỢC**, không phải "đạt".

---

## 6. BẨY BẪY ĐÃ TRẢ GIÁ TRONG BỐN LƯỢT VỪA RỒI — đừng trả lại lần nữa

1. **Đột biến phải chạy trên BẢN SAO có `ROOT` GHIM.** Thiếu ghim thì `main()` chết trước
   `phan_chung` và **mọi** mutant báo "không giết" — tín dụng GIẢ. Đã sập thật ở lượt 7.
2. **Tín hiệu "đã giết" phải là BA bằng chứng độc lập**: giá trị trả về của `phan_chung()`, **số
   ca đã chạy** (> 0), và **tập tên** LỌT. Chỉ so tập LỌT thì một mutant **không chạy ca nào** cho
   `lot=[]` và được đọc thành "nền sạch" — P3 của lượt 8. Công cụ mẫu: `do_rang_luot9.py` trong
   gói sandbox (nó là công cụ NHÁP, hãy hỏi nó một ca **biết trước đáp án** trước khi tin).
3. **Ca đòi `bool(lỗi)` là ca không có răng.** `ruff-pin-required` từng xanh khi chốt ghim đã bị
   **xoá hẳn**, vì bỏ ghim làm cả ghim lẫn probe đỏ. Đòi **đúng loại thông điệp**.
4. **Số trong thông điệp commit phải SINH TỪ lần chạy**, đừng gõ tay. Lượt 7 bắt được commit khai
   `93/93` và `A8=439` trong khi thật là `91/91` và `438`.
5. **Vòng giám sát đọc kết luận bằng `tail` là vòng giám sát sẽ XOÁ verdict.** Dòng `verdict:` nằm
   ở DÒNG 1; `tail -n 5` luôn rỗng ⇒ tưởng chưa xong ⇒ phóng phiên mới ⇒ phiên mới `cat >
   VERDICT.md` và xoá sạch. Đã mất một verdict hoàn chỉnh vì đúng chuyện này. Dùng `grep -m1` trên
   TOÀN tệp, và **sao lưu trước mỗi lần phóng**.
6. **`launcher.py run` cho con `stdin=DEVNULL`** — truyền prompt làm ĐỐI SỐ, và `--prompt-file` phải
   đi CẶP với `--expected-prompt-sha256`.
7. **Khai phủ định phải hẹp bằng phép đo.** Lượt 9 tôi khai *"không đột biến nào giết được nhánh
   ý thức trích dẫn"*; reviewer **dựng được** một đột biến có răng, 0 dòng tăng. Câu đúng lẽ ra là
   *"với BỘ FIXTURE HIỆN CÓ thì không đo được"*. Đừng khai rộng hơn thứ đã đo.

---

## 7. CROSS-REVIEW LƯỢT SAU — reviewer là `claude`

Adapter: `.claude/skills/cross-review/SKILL.md`. Những điều đã đo được là có hiệu lực:

- Bắt reviewer ghi `VERDICT.md` **TĂNG DẦN** (ba câu bắt buộc trong prompt) — đó là thứ giữ được
  bằng chứng khi một lượt bị cắt.
- Bắt nộp **BẢNG SĂN ≥ N hướng ĐỘC LẬP**, mỗi hướng có **lệnh + output thật**. Thiếu bảng thì
  `approve` = **KHÔNG ĐO ĐƯỢC**. Nộp kèm danh sách hướng các lượt trước (7/8/9/10 có trong verdict)
  và cấm lặp y nguyên.
- Reviewer **CHẠY và ĐỘT BIẾN**, không **TỰ SOẠN** payload; hướng nào cần soạn thì **mô tả bằng
  lời**, phiên điều phối viết probe và đo hộ.
- Mirror **trong** sandbox, detached đúng `reviewed_sha`, `git config core.abbrev 7` (không ghim
  thì `doc-claims-check --strict` đỏ giả), và **đối chiếu cổng nền↔sandbox tại CÙNG một commit**
  trước khi giao.
- Phép canh hai nguồn ref chạy **TRÊN KHO NGUỒN, TRƯỚC khi clone** — trong sandbox nó vô nghĩa vì
  không có đường ra mạng.

---

## 8. XONG LÀ GÌ

`review_class = sensitive` ⇒ **`approve` TƯỜNG MINH**. *"0 P1 + 0 P2"* **KHÔNG đủ** — "vắng mặt vì
sạch" và "vắng mặt vì chưa nhìn tới" nhìn giống hệt nhau. Và `A8` phải còn đúng **2 đường dẫn,
additions ≤ 500** ở lượt đo cuối.
